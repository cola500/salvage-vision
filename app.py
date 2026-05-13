# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "flask",
#     "anthropic",
# ]
# ///
"""AI-assisterad återbruksinventering — experiment.

Kör: uv run app.py
Sätt ANTHROPIC_API_KEY för riktiga AI-anrop, annars fallbackar till mock.
"""
import base64
import json
import os

import anthropic
from flask import Flask, jsonify, request

app = Flask(__name__)
SAVED = []

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
  <caption>Klicka i en cell för att redigera. Ändringar sparas när du klickar "Spara inventering".</caption>
  <thead><tr><th>Material</th><th>Objekt</th><th>Mängd</th><th>Återbrukspotential</th></tr></thead>
  <tbody id="result-body"></tbody>
</table>

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
      ['material', 'object', 'quantity', 'reuse_potential'].forEach(k => {
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
</script>
</body>
</html>"""


if __name__ == "__main__":
    print("Återbruksinventering körs på http://localhost:5050")
    print("ANTHROPIC_API_KEY:", "satt" if os.environ.get("ANTHROPIC_API_KEY") else "SAKNAS — mock-läge")
    app.run(debug=False, port=5050)
