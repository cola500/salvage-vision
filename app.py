# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "flask",
#     "anthropic",
#     "Pillow",
# ]
# ///
"""AI-assisterad återbruksinventering — experiment.

Kör: uv run app.py
Sätt ANTHROPIC_API_KEY för riktiga AI-anrop, annars fallbackar till mock.
"""
import base64
import io
import json
import mimetypes
import os
from pathlib import Path

import anthropic
from flask import Flask, jsonify, request, send_from_directory
from PIL import Image

# Anthropic vision API har en 5 MB-gräns på base64-payloaden.
# Råa JPEGs över ~3.75 MB ramlar över efter base64-expansion (×4/3).
ANTHROPIC_IMAGE_BYTES_LIMIT = 5_000_000
COMPRESS_MAX_DIMENSION = 1920
COMPRESS_QUALITY = 85


def _compress_for_api(image_bytes):
    """Returnera (bytes, media_type). Komprimerar endast om över gränsen."""
    if len(image_bytes) * 4 // 3 < ANTHROPIC_IMAGE_BYTES_LIMIT:
        return image_bytes, None  # None = behåll original media_type
    img = Image.open(io.BytesIO(image_bytes))
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    if max(img.size) > COMPRESS_MAX_DIMENSION:
        img.thumbnail((COMPRESS_MAX_DIMENSION, COMPRESS_MAX_DIMENSION))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=COMPRESS_QUALITY, optimize=True)
    return buf.getvalue(), "image/jpeg"

app = Flask(__name__)
SAVED = []

DATASET_DIR = Path(__file__).parent / "test-datasets" / "field-test-001"
DATASET_IMAGES = [f"img-{i:02d}.jpg" for i in range(1, 11)]
DATASET_FILES = set(DATASET_IMAGES) | {"planritning.pdf"}

ZONES = ["KONTOR", "MÖTE", "SAMTAL", "PENTRY_PAUS", "ENTRÉ", "OUTSIDE_LOCAL"]

MOCK = {
    "items": [
        {"material": "Tegel (rött)", "object": "Innervägg", "quantity": "ca 8 kvm", "reuse_potential": "Hög"},
        {"material": "Trä (ek)", "object": "Köksbänk", "quantity": "1 st, ca 3 löpmeter", "reuse_potential": "Medium"},
        {"material": "Rostfritt stål", "object": "Diskbänk med blandare", "quantity": "1 st", "reuse_potential": "Hög"},
        {"material": "MDF (lackat)", "object": "Köksluckor", "quantity": "ca 12 st", "reuse_potential": "Låg"},
    ]
}

PROMPT = """Du är expert på återbruksinventering inom bygg och fastighet.
Analysera bilden och identifiera material/objekt som potentiellt kan återbrukas.

VIKTIGA REGLER:

1. Synlighet — lista BARA det som faktiskt syns i bilden.
   - Lägg inte till föremål för att de "borde" finnas i ett kök/badrum/rum.
   - Om en yta är skymd eller utanför bildens kant — lista den inte.
   - Hellre färre poster än hittepå.

2. Närbild och fragment — extrapolera inte.
   - Om bilden är en närbild eller bara visar ett fragment av yta/objekt:
     kvantifiera endast det som faktiskt syns.
   - Skriv quantity som "kan ej bedömas från närbild" om total mängd eller
     yta inte går att avgöra från bilden.
   - Gissa inte hela rummets storlek från ett golvfragment.

3. Ingen dubbelräkning — samma yta eller objekt = exakt en post.
   - Ett golv är EN post, inte "parkett" + "lack" + "undergolv".
   - En spiselkrans är EN post, inte två motstridiga materialposter.
   - Om materialet är osäkert, skriv osäkerheten inom samma post
     (t.ex. material: "trä (ek eller björk, osäkert)").

4. Osäkerhet — markera tydligt när du är osäker.
   - Hellre "osäkert" eller "kan ej bedömas" än kvalificerad gissning.
   - Använd confidence-fältet (low | medium | high) för att signalera
     hur säker du är på posten som helhet.

Returnera ENDAST ett JSON-objekt — ingen markdown, inga code-fences, ingen
text före eller efter. Börja svaret direkt med { och avsluta med }.

Schema:
{
  "items": [
    {
      "material": "...",
      "object": "...",
      "quantity": "...",
      "reuse_potential": "Låg" | "Medium" | "Hög",
      "confidence": "low" | "medium" | "high"
    }
  ]
}

Var konkret och realistisk i mängd när bilden tillåter (t.ex. "ca 12 kvm",
"1 st", "ca 3 löpmeter"). Lista 3–8 objekt — färre om bara få syns.
Svara på svenska."""


ROOMS_HTML = """<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<title>Room aggregation — Hallvägen 21</title>
<style>
  body { font-family: -apple-system, system-ui, sans-serif; max-width: 1200px; margin: 1rem auto; padding: 0 1rem; color: #222; }
  nav a { font-size: .9rem; color: #555; text-decoration: none; }
  nav a:hover { text-decoration: underline; }
  h1 { font-size: 1.4rem; margin: .25rem 0; }
  h2 { font-size: 1.1rem; margin-top: 2rem; border-bottom: 2px solid #eee; padding-bottom: .25rem; }
  h3 { font-size: 1rem; margin-top: 1rem; }
  .intro { color: #666; font-size: .9rem; margin: .25rem 0 1rem 0; }

  .planritning embed { width: 100%; height: 400px; border: 1px solid #ddd; }
  .fallback { font-size: .8rem; color: #888; margin-top: .25rem; }

  .actions-bar { display: flex; gap: .75rem; align-items: center; margin: .75rem 0; }
  .actions-bar button { padding: .5rem 1rem; font-size: .95rem; cursor: pointer; }
  .actions-bar .progress { font-size: .85rem; color: #555; }

  .img-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: .75rem; }
  .img-card { border: 2px solid #eee; padding: .5rem; border-radius: 4px; display: flex; flex-direction: column; gap: .4rem; }
  .img-card img { width: 100%; height: 130px; object-fit: cover; border-radius: 2px; cursor: zoom-in; }
  .img-modal { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
               background: rgba(0,0,0,.85); z-index: 1000; cursor: zoom-out;
               align-items: center; justify-content: center; }
  .img-modal img { max-width: 95vw; max-height: 95vh; box-shadow: 0 0 30px rgba(0,0,0,.5); }
  .img-card .filename { font-family: monospace; font-size: .75rem; color: #555; }
  .img-card select { font-size: .85rem; padding: .25rem; }
  .img-card .analyze-row { display: flex; gap: .5rem; align-items: center; font-size: .8rem; }
  .img-card button { padding: .25rem .5rem; font-size: .8rem; cursor: pointer; }
  .img-card .status { color: #666; font-size: .75rem; flex: 1; }
  .img-card.analyzed { border-color: #4caf50; }
  .img-card.error { border-color: #f44336; }
  .img-card.analyzing { border-color: #2196f3; }

  .zone-KONTOR { background: #fff3cd; }
  .zone-MÖTE { background: #d1ecf1; }
  .zone-SAMTAL { background: #d4edda; }
  .zone-PENTRY_PAUS { background: #f8d7da; }
  .zone-ENTRÉ { background: #e2d4f7; }
  .zone-OUTSIDE_LOCAL { background: #dcdcdc; color: #555; }
  .zone- { background: #fff; }
  .zone-none { background: #fff; }

  .zone-section { margin-top: 1rem; }
  .zone-section h3 .label { padding: .2rem .5rem; border-radius: 3px; }
  .zone-section h3 .count { font-weight: normal; font-size: .85rem; color: #555; margin-left: .5rem; }
  .empty-zone { color: #888; font-size: .85rem; font-style: italic; padding: .25rem 0; }

  table { width: 100%; border-collapse: collapse; font-size: .85rem; margin-top: .25rem; }
  th, td { border: 1px solid #ddd; padding: .35rem .5rem; text-align: left; vertical-align: top; }
  th { background: #f4f4f4; }
  td[contenteditable] { cursor: text; }
  td[contenteditable]:focus { outline: 2px solid #4c8bf5; outline-offset: -2px; background: #fff; }
  tr.removed td { text-decoration: line-through; opacity: .5; }
  tr.user-dup td { opacity: .65; background: #fafafa; }
  .dup-flag { background: #ffe082; padding: .1rem .35rem; border-radius: 2px; font-size: .72rem; color: #6d4c00; }
  .row-actions { white-space: nowrap; }
  .row-actions button { font-size: .8rem; padding: .15rem .4rem; margin-left: .25rem; cursor: pointer; }
  .src-label { font-family: monospace; font-size: .75rem; color: #777; }

  .total { margin-top: 2rem; padding: 1rem; background: #f8f8f8; border-radius: 4px; }
  .total h2 { margin-top: 0; }

  pre { background: #f8f8f8; padding: .75rem; overflow: auto; font-size: .72rem; max-height: 300px; }
</style>
</head>
<body>
<nav><a href="/">← Single-bild-flow</a></nav>
<h1>Room-based aggregation — Hallvägen 21, plan 4</h1>
<p class="intro">Tilldela varje bild en zon, kör AI-analys, granska samlad inventering per zon. In-memory — laddar du om sidan börjar du om.</p>

<section class="planritning">
  <h2>Planritning</h2>
  <embed src="/dataset/planritning.pdf" type="application/pdf">
  <div class="fallback">
    Om PDF:en inte visas: <a href="/dataset/planritning.pdf" target="_blank">öppna i ny flik</a>.
    Zoner i ritningen: KONTOR (öppet landskap), MÖTE (stort centralt), SAMTAL (2 st), PENTRY/PAUS, WC, HWC, STÄD, ENTRÉ.
  </div>
</section>

<section>
  <h2>Bilder (10)</h2>
  <div class="actions-bar">
    <button id="analyze-all">Analysera alla otaganalysade</button>
    <span class="progress" id="progress"></span>
  </div>
  <div class="img-grid" id="img-grid"></div>
</section>

<section>
  <h2>Per zon</h2>
  <div id="zones"></div>
</section>

<section class="total">
  <h2>Samlad inventering</h2>
  <p style="color:#666; font-size:.85rem; margin:0 0 .5rem 0">Exklusive OUTSIDE_LOCAL, exklusive borttagna och dublettmarkerade.</p>
  <div id="total"></div>
</section>

<h2>State (rå JSON)</h2>
<pre id="raw">(tom)</pre>

<div class="img-modal" id="img-modal"><img id="img-modal-img" alt="förstorad bild"></div>

<script>
const IMAGES = __IMAGES_JSON__;
const ZONES = __ZONES_JSON__;

const state = {
  images: IMAGES.map(file => ({
    file, zone: '', items: null, status: 'idle', error: null, source: null,
  })),
};
window.state = state;

function el(tag, opts, children) {
  opts = opts || {};
  const node = document.createElement(tag);
  if (opts.className) node.className = opts.className;
  if (opts.text !== undefined) node.textContent = opts.text;
  if (opts.attrs) for (const k in opts.attrs) node.setAttribute(k, opts.attrs[k]);
  if (opts.dataset) for (const k in opts.dataset) node.dataset[k] = opts.dataset[k];
  if (opts.on) for (const ev in opts.on) node.addEventListener(ev, opts.on[ev]);
  (children || []).forEach(c => c && node.appendChild(c));
  return node;
}

function renderImageGrid() {
  const grid = document.getElementById('img-grid');
  grid.innerHTML = '';
  state.images.forEach((img, idx) => {
    const cls = 'img-card ' + (img.status === 'analyzed' ? 'analyzed' : img.status === 'analyzing' ? 'analyzing' : img.status === 'error' ? 'error' : '');
    const card = el('div', { className: cls });
    const imgEl = el('img', {
      attrs: { src: '/dataset/' + img.file, alt: img.file, title: 'Klicka för att förstora' },
      on: { click: () => openImgModal('/dataset/' + img.file) },
    });
    card.appendChild(imgEl);
    card.appendChild(el('div', { className: 'filename', text: img.file }));

    const select = el('select', { className: 'zone-' + (img.zone || 'none') });
    select.appendChild(el('option', { text: '(ingen zon)', attrs: { value: '' } }));
    ZONES.forEach(z => {
      const opt = el('option', { text: z.replace('_', '/'), attrs: { value: z } });
      if (z === img.zone) opt.selected = true;
      select.appendChild(opt);
    });
    select.addEventListener('change', e => {
      state.images[idx].zone = e.target.value;
      renderAll();
    });
    card.appendChild(select);

    const analyzeRow = el('div', { className: 'analyze-row' });
    const aBtn = el('button', {
      text: img.status === 'analyzed' ? 'Kör om' : 'Analysera',
      on: { click: () => analyzeOne(idx) },
    });
    if (img.status === 'analyzing') aBtn.disabled = true;
    analyzeRow.appendChild(aBtn);
    let statusText = '';
    if (img.status === 'analyzing') statusText = 'analyserar…';
    else if (img.status === 'analyzed') statusText = '✓ ' + img.items.length + ' items';
    else if (img.status === 'error') statusText = '✕ ' + img.error;
    analyzeRow.appendChild(el('span', { className: 'status', text: statusText }));
    card.appendChild(analyzeRow);

    grid.appendChild(card);
  });
}

function renderZones() {
  const container = document.getElementById('zones');
  container.innerHTML = '';

  ZONES.forEach(zone => {
    const imgsInZone = state.images.filter(i => i.zone === zone);
    const allItems = [];
    imgsInZone.forEach(img => {
      (img.items || []).forEach((it, itemIdx) => {
        allItems.push(Object.assign({}, it, { _source: img.file, _imgIdx: state.images.indexOf(img), _itemIdx: itemIdx }));
      });
    });
    const liveCount = allItems.filter(i => !i.removed && !i.user_duplicate).length;
    const dupPairs = findDuplicates(allItems);

    const section = el('div', { className: 'zone-section' });
    const h3 = el('h3');
    h3.appendChild(el('span', { className: 'label zone-' + zone, text: zone.replace('_', '/') }));
    h3.appendChild(el('span', { className: 'count', text: imgsInZone.length + ' bild' + (imgsInZone.length === 1 ? '' : 'er') + ', ' + liveCount + ' live items' }));
    section.appendChild(h3);

    if (allItems.length === 0) {
      section.appendChild(el('div', { className: 'empty-zone', text: '(inga bilder tilldelade ännu, eller inga analyserade)' }));
      container.appendChild(section);
      return;
    }

    const table = el('table');
    table.appendChild(el('thead', {}, [
      el('tr', {}, [
        el('th', { text: 'Objekt' }),
        el('th', { text: 'Material' }),
        el('th', { text: 'Mängd' }),
        el('th', { text: 'Återbruk' }),
        el('th', { text: 'Conf.' }),
        el('th', { text: 'Källa' }),
        el('th', { text: 'Status' }),
        el('th', { text: '' }),
      ]),
    ]));

    const tbody = el('tbody');
    allItems.forEach((it, aggIdx) => {
      const classes = [];
      if (it.removed) classes.push('removed');
      if (it.user_duplicate) classes.push('user-dup');
      const tr = el('tr', { className: classes.join(' ') });

      ['object', 'material', 'quantity', 'reuse_potential'].forEach(key => {
        const td = el('td', { text: it[key] || '', attrs: { contenteditable: 'true' } });
        td.dataset.imgIdx = it._imgIdx;
        td.dataset.itemIdx = it._itemIdx;
        td.dataset.key = key;
        tr.appendChild(td);
      });
      tr.appendChild(el('td', { text: it.confidence || '-', attrs: { style: 'font-size:.75rem; color:#555' } }));
      tr.appendChild(el('td', { className: 'src-label', text: it._source }));

      const statusTd = el('td');
      const dupHits = dupPairs.filter(p => p[0] === aggIdx || p[1] === aggIdx);
      if (dupHits.length > 0 && !it.removed) {
        const otherIdxs = dupHits.map(p => p[0] === aggIdx ? p[1] : p[0]);
        const otherSrcs = otherIdxs.map(i => allItems[i]._source).filter((v, i, a) => a.indexOf(v) === i).join(', ');
        statusTd.appendChild(el('span', { className: 'dup-flag', text: 'möjlig dublett (' + otherSrcs + ')' }));
      }
      if (it.user_duplicate) statusTd.appendChild(el('span', { text: ' markerad som dublett', attrs: { style: 'font-size:.72rem; color:#888; margin-left:.25rem' } }));
      tr.appendChild(statusTd);

      const actions = el('td', { className: 'row-actions' });
      actions.appendChild(el('button', {
        text: it.removed ? '↶' : '✕',
        attrs: { title: it.removed ? 'Återställ' : 'Ta bort' },
        on: { click: () => toggleRemoved(it._imgIdx, it._itemIdx) },
      }));
      actions.appendChild(el('button', {
        text: it.user_duplicate ? '◌' : '🔗',
        attrs: { title: it.user_duplicate ? 'Avmarkera som dublett' : 'Markera som dublett' },
        on: { click: () => toggleUserDuplicate(it._imgIdx, it._itemIdx) },
      }));
      tr.appendChild(actions);

      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    section.appendChild(table);
    container.appendChild(section);
  });
}

function renderTotal() {
  const allActive = [];
  state.images.forEach(img => {
    if (img.zone === 'OUTSIDE_LOCAL' || !img.zone) return;
    (img.items || []).forEach(it => {
      if (it.removed || it.user_duplicate) return;
      allActive.push(Object.assign({}, it, { _source: img.file, _zone: img.zone }));
    });
  });

  const container = document.getElementById('total');
  container.innerHTML = '';
  if (allActive.length === 0) {
    container.appendChild(el('div', { text: 'Ingen samlad inventering ännu — tilldela zoner och kör analys.', attrs: { style: 'color:#888' } }));
    return;
  }

  container.appendChild(el('div', { text: 'Totalt ' + allActive.length + ' aktiva observationer över ' + new Set(allActive.map(i => i._zone)).size + ' zoner.', attrs: { style: 'font-weight:bold; margin-bottom:.5rem' } }));

  const table = el('table');
  table.appendChild(el('thead', {}, [
    el('tr', {}, [
      el('th', { text: 'Zon' }),
      el('th', { text: 'Objekt' }),
      el('th', { text: 'Material' }),
      el('th', { text: 'Mängd' }),
      el('th', { text: 'Återbruk' }),
      el('th', { text: 'Källa' }),
    ]),
  ]));
  const tbody = el('tbody');
  allActive.forEach(it => {
    tbody.appendChild(el('tr', {}, [
      el('td', { className: 'zone-' + it._zone, text: it._zone.replace('_', '/') }),
      el('td', { text: it.object || '' }),
      el('td', { text: it.material || '' }),
      el('td', { text: it.quantity || '' }),
      el('td', { text: it.reuse_potential || '' }),
      el('td', { className: 'src-label', text: it._source }),
    ]));
  });
  table.appendChild(tbody);
  container.appendChild(table);
}

function renderRaw() {
  document.getElementById('raw').textContent = JSON.stringify(state, null, 2);
}

function renderAll() {
  renderImageGrid();
  renderZones();
  renderTotal();
  renderRaw();
}

function toggleRemoved(imgIdx, itemIdx) {
  const item = state.images[imgIdx].items[itemIdx];
  item.removed = !item.removed;
  renderAll();
}
function toggleUserDuplicate(imgIdx, itemIdx) {
  const item = state.images[imgIdx].items[itemIdx];
  item.user_duplicate = !item.user_duplicate;
  renderAll();
}

async function analyzeOne(idx) {
  const img = state.images[idx];
  img.status = 'analyzing';
  img.error = null;
  renderImageGrid();
  try {
    const r = await fetch('/analyze-dataset/' + img.file, { method: 'POST' });
    const data = await r.json();
    if (data.error) throw new Error(data.error);
    img.items = (data.items || []).map(it => Object.assign({}, it, { removed: false, user_duplicate: false }));
    img.source = data._source;
    img.status = 'analyzed';
  } catch (e) {
    img.status = 'error';
    img.error = e.message || String(e);
  }
  renderAll();
}

async function analyzeAll() {
  const pending = state.images.map((img, idx) => idx).filter(idx => state.images[idx].status !== 'analyzed' && state.images[idx].status !== 'analyzing');
  const progress = document.getElementById('progress');
  const total = pending.length;
  let done = 0;
  progress.textContent = 'analyserar… 0/' + total;
  const concurrency = 3;
  async function worker() {
    while (pending.length > 0) {
      const next = pending.shift();
      if (next === undefined) return;
      await analyzeOne(next);
      done += 1;
      progress.textContent = 'analyserar… ' + done + '/' + total;
    }
  }
  await Promise.all(Array.from({ length: concurrency }, () => worker()));
  progress.textContent = 'klar — ' + done + ' analyserade';
}

document.addEventListener('input', e => {
  const td = e.target;
  if (!td.dataset || td.dataset.imgIdx === undefined) return;
  const imgIdx = parseInt(td.dataset.imgIdx, 10);
  const itemIdx = parseInt(td.dataset.itemIdx, 10);
  const key = td.dataset.key;
  const item = state.images[imgIdx].items[itemIdx];
  item[key] = td.textContent;
  renderTotal();
  renderRaw();
});

function tokenize(str) {
  return new Set(
    (str || '').toLowerCase()
      .replace(/[^a-zåäöéèüçñ0-9 ]/g, ' ')
      .split(/\\s+/)
      .filter(t => t.length >= 3)
  );
}

function jaccard(a, b) {
  const A = tokenize(a), B = tokenize(b);
  if (A.size === 0 || B.size === 0) return 0;
  let intersect = 0;
  A.forEach(x => { if (B.has(x)) intersect++; });
  const union = new Set([...A, ...B]).size;
  return intersect / union;
}

function findDuplicates(items) {
  const dups = [];
  for (let i = 0; i < items.length; i++) {
    if (items[i].removed) continue;
    for (let j = i + 1; j < items.length; j++) {
      if (items[j].removed) continue;
      if (items[i]._source === items[j]._source) continue;
      const mj = jaccard(items[i].material, items[j].material);
      const oj = jaccard(items[i].object, items[j].object);
      const score = (mj + oj) / 2;
      if (score >= 0.4) dups.push([i, j, score]);
    }
  }
  return dups;
}

const imgModal = document.getElementById('img-modal');
const imgModalImg = document.getElementById('img-modal-img');
function openImgModal(src) {
  imgModalImg.src = src;
  imgModal.style.display = 'flex';
}
imgModal.addEventListener('click', () => { imgModal.style.display = 'none'; });
document.addEventListener('keydown', e => { if (e.key === 'Escape') imgModal.style.display = 'none'; });

document.getElementById('analyze-all').addEventListener('click', analyzeAll);
renderAll();
</script>
</body>
</html>"""


@app.post("/analyze")
def analyze():
    f = request.files.get("image")
    if not f:
        return jsonify({"error": "no image"}), 400

    media_type = f.mimetype or "image/jpeg"
    img_b64 = base64.b64encode(f.read()).decode()

    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return jsonify({**MOCK, "_source": "mock (ingen ANTHROPIC_API_KEY)"})

    try:
        client = anthropic.Anthropic(api_key=key)
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": img_b64}},
                        {"type": "text", "text": PROMPT},
                    ],
                },
            ],
        )
        text = msg.content[0].text
        start, end = text.find("{"), text.rfind("}")
        data = json.loads(text[start : end + 1])
        data["_source"] = "claude-sonnet-4-6"
        return jsonify(data)
    except Exception as e:
        return jsonify({**MOCK, "_source": f"mock (API-fel: {type(e).__name__}: {e})"})


@app.post("/save")
def save():
    data = request.get_json(force=True)
    SAVED.append(data)
    return jsonify({"ok": True, "count": len(SAVED)})


@app.get("/saved")
def saved():
    return jsonify(SAVED)


@app.get("/dataset/<path:filename>")
def serve_dataset(filename):
    if filename not in DATASET_FILES:
        return "not found", 404
    return send_from_directory(DATASET_DIR, filename)


@app.post("/analyze-dataset/<path:filename>")
def analyze_dataset(filename):
    if filename not in DATASET_IMAGES:
        return jsonify({"error": "unknown dataset file"}), 400
    path = DATASET_DIR / filename
    if not path.exists():
        return jsonify({"error": "file missing on disk"}), 404

    media_type = mimetypes.guess_type(str(path))[0] or "image/jpeg"
    image_bytes, new_media_type = _compress_for_api(path.read_bytes())
    if new_media_type:
        media_type = new_media_type
    img_b64 = base64.b64encode(image_bytes).decode()

    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return jsonify({**MOCK, "_source": "mock (ingen ANTHROPIC_API_KEY)"})

    try:
        client = anthropic.Anthropic(api_key=key)
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": img_b64}},
                        {"type": "text", "text": PROMPT},
                    ],
                },
            ],
        )
        text = msg.content[0].text
        start, end = text.find("{"), text.rfind("}")
        data = json.loads(text[start : end + 1])
        data["_source"] = "claude-sonnet-4-6"
        return jsonify(data)
    except Exception as e:
        return jsonify({**MOCK, "_source": f"mock (API-fel: {type(e).__name__}: {e})"})


@app.get("/rooms")
def rooms():
    images_json = json.dumps(DATASET_IMAGES)
    zones_json = json.dumps(ZONES)
    return ROOMS_HTML.replace("__IMAGES_JSON__", images_json).replace("__ZONES_JSON__", zones_json)


@app.get("/")
def index():
    return """<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<title>Återbruksinventering</title>
<style>
  body { font-family: -apple-system, system-ui, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; }
  h1 { font-size: 1.4rem; }
  .row { display: flex; gap: 1rem; align-items: center; margin: 1rem 0; }
  button { padding: .6rem 1rem; font-size: 1rem; cursor: pointer; }
  button:disabled { opacity: .5; cursor: wait; }
  #preview { max-width: 280px; max-height: 200px; border: 1px solid #ddd; display: none; }
  #timer { font-family: monospace; font-size: 1.1rem; color: #444; }
  table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
  th, td { border: 1px solid #ddd; padding: .5rem; text-align: left; font-size: .95rem; }
  th { background: #f4f4f4; }
  .high { background: #d4edda; }
  .med { background: #fff3cd; }
  .low { background: #f8d7da; }
  td[contenteditable] { cursor: text; }
  td[contenteditable]:focus { outline: 2px solid #4c8bf5; outline-offset: -2px; background: #fff; }
  caption { caption-side: top; text-align: left; font-size: .85rem; color: #666; padding-bottom: .25rem; }
  pre { background: #f8f8f8; padding: 1rem; overflow: auto; font-size: .8rem; }
  #status { color: #666; font-size: .9rem; }
  #saved-msg { color: green; font-weight: bold; }
  .source { font-size: .8rem; color: #888; margin-top: .5rem; }
  #preview { cursor: zoom-in; }
  .img-modal { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
               background: rgba(0,0,0,.85); z-index: 1000; cursor: zoom-out;
               align-items: center; justify-content: center; }
  .img-modal img { max-width: 95vw; max-height: 95vh; box-shadow: 0 0 30px rgba(0,0,0,.5); }
</style>
</head>
<body>
<h1>Återbruksinventering — bild till lista</h1>

<div class="row">
  <input type="file" id="file" accept="image/*">
</div>
<img id="preview">

<div class="row">
  <button id="analyze" disabled>Analysera bild</button>
  <span id="timer"></span>
  <span id="status"></span>
</div>

<table id="result-table" style="display:none">
  <caption>Klicka i en cell för att redigera. Ändringar sparas när du klickar "Spara inventering". Klicka på bilden för att förstora.</caption>
  <thead><tr><th>Objekt</th><th>Material</th><th>Mängd</th><th>Återbrukspotential</th></tr></thead>
  <tbody id="result-body"></tbody>
</table>

<div class="img-modal" id="img-modal"><img id="img-modal-img" alt="förstorad bild"></div>

<div class="source" id="source"></div>

<div class="row" style="display:none" id="save-row">
  <button id="save">Spara inventering</button>
  <span id="saved-msg"></span>
</div>

<h3 style="margin-top:2rem">Rå JSON</h3>
<pre id="raw">(inget än)</pre>

<script>
const fileInput = document.getElementById('file');
const preview = document.getElementById('preview');
const analyzeBtn = document.getElementById('analyze');
const saveBtn = document.getElementById('save');
const timer = document.getElementById('timer');
const status = document.getElementById('status');
const raw = document.getElementById('raw');
const tableEl = document.getElementById('result-table');
const tbody = document.getElementById('result-body');
const saveRow = document.getElementById('save-row');
const savedMsg = document.getElementById('saved-msg');
const sourceEl = document.getElementById('source');

let lastResult = null;
let timerId = null;

tbody.addEventListener('input', (e) => {
  const td = e.target;
  if (!td.dataset || td.dataset.idx === undefined || !lastResult || !lastResult.items) return;
  const idx = parseInt(td.dataset.idx, 10);
  const key = td.dataset.key;
  lastResult.items[idx][key] = td.textContent;
  if (key === 'reuse_potential') {
    const tr = td.parentElement;
    tr.classList.remove('high', 'med', 'low');
    const v = td.textContent.toLowerCase();
    if (v.startsWith('hög')) tr.classList.add('high');
    else if (v.startsWith('med')) tr.classList.add('med');
    else if (v.startsWith('låg')) tr.classList.add('low');
  }
  raw.textContent = JSON.stringify(lastResult, null, 2);
  savedMsg.textContent = '';
});

fileInput.addEventListener('change', () => {
  const f = fileInput.files[0];
  if (!f) return;
  preview.src = URL.createObjectURL(f);
  preview.style.display = 'block';
  analyzeBtn.disabled = false;
  status.textContent = '';
  savedMsg.textContent = '';
});

analyzeBtn.addEventListener('click', async () => {
  const f = fileInput.files[0];
  if (!f) return;

  analyzeBtn.disabled = true;
  tableEl.style.display = 'none';
  saveRow.style.display = 'none';
  raw.textContent = '(analyserar...)';
  sourceEl.textContent = '';
  savedMsg.textContent = '';

  const start = Date.now();
  timer.textContent = '0.0 s';
  timerId = setInterval(() => {
    timer.textContent = ((Date.now() - start) / 1000).toFixed(1) + ' s';
  }, 100);

  const form = new FormData();
  form.append('image', f);

  try {
    const r = await fetch('/analyze', { method: 'POST', body: form });
    const data = await r.json();
    clearInterval(timerId);
    const elapsed = ((Date.now() - start) / 1000).toFixed(1);
    timer.textContent = elapsed + ' s';
    status.textContent = elapsed < 30 ? '✓ under 30s' : '⚠ över 30s';

    lastResult = data;
    raw.textContent = JSON.stringify(data, null, 2);
    sourceEl.textContent = 'Källa: ' + (data._source || 'okänd');

    tbody.innerHTML = '';
    (data.items || []).forEach((it, idx) => {
      const tr = document.createElement('tr');
      const pot = (it.reuse_potential || '').toLowerCase();
      if (pot.startsWith('hög')) tr.classList.add('high');
      else if (pot.startsWith('med')) tr.classList.add('med');
      else if (pot.startsWith('låg')) tr.classList.add('low');
      ['object', 'material', 'quantity', 'reuse_potential'].forEach(k => {
        const td = document.createElement('td');
        td.textContent = it[k] || '';
        td.contentEditable = 'true';
        td.dataset.idx = idx;
        td.dataset.key = k;
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    tableEl.style.display = 'table';
    saveRow.style.display = 'flex';
  } catch (e) {
    clearInterval(timerId);
    status.textContent = 'fel: ' + e.message;
  } finally {
    analyzeBtn.disabled = false;
  }
});

saveBtn.addEventListener('click', async () => {
  if (!lastResult) return;
  const r = await fetch('/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(lastResult),
  });
  const d = await r.json();
  savedMsg.textContent = `✓ sparad (totalt ${d.count} inventeringar)`;
});

const imgModal = document.getElementById('img-modal');
const imgModalImg = document.getElementById('img-modal-img');
preview.addEventListener('click', () => {
  if (!preview.src) return;
  imgModalImg.src = preview.src;
  imgModal.style.display = 'flex';
});
imgModal.addEventListener('click', () => { imgModal.style.display = 'none'; });
document.addEventListener('keydown', e => { if (e.key === 'Escape') imgModal.style.display = 'none'; });
</script>
</body>
</html>"""


if __name__ == "__main__":
    print("Återbruksinventering körs på http://localhost:5050")
    print("ANTHROPIC_API_KEY:", "satt" if os.environ.get("ANTHROPIC_API_KEY") else "SAKNAS — mock-läge")
    app.run(debug=False, port=5050)
