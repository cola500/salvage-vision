---
title: Salvage Vision — prototype demo (mock data)
description: Statisk GitHub Pages-demo av Salvage Vision-prototypen — körs utan backend, utan API-nyckel, med förinspelad Claude Vision-output
category: demo
status: published-ready
last_updated: 2026-05-14
sections:
  - Vad är detta
  - Köra lokalt
  - Publicera på GitHub Pages
  - Filstruktur
  - Mock-data — vad är fejk och vad är riktigt
  - Säkerhet och privacy
---

# Salvage Vision — prototype demo (mock data)

Statisk frontend-only version av `/rooms`-flowet, byggd för att kunna
publiceras på GitHub Pages eller köras lokalt utan att starta Flask,
utan API-nyckel, och utan att göra några live-anrop mot Anthropic.

## Vad är detta

En interaktiv demo som visar:

- Planritning + 10 interiörbilder från en publik kontorslokalannons
  (Hallvägen 21, Lokalguiden)
- Manuell zon-tilldelning per bild (förvald för demo)
- "Analys" som visar förinspelad output från `claude-sonnet-4-6` med
  simulerad latency
- Per-zon-aggregering med dublett-flagging
- Redigera, ta bort eller markera observationer som dubletter
- Samlad inventering som uppdateras live

Allt klient-side. Ingen backend. Ingen nyckel.

## Köra lokalt

PDF-preview och `fetch('./data/...')` kräver en statisk server (kan
inte köras via `file://`-protokoll). Enklast:

```sh
cd docs-demo
python3 -m http.server 5051
```

Sen i webbläsaren: <http://localhost:5051/>.

Andra alternativ som funkar:
- `npx serve docs-demo`
- `caddy file-server --listen :5051 --root docs-demo`
- Valfri statisk webbserver

## Publicera på GitHub Pages

GitHub Pages stöder tre källor:

1. **`/docs/` på huvudbranchen** — krockar med vårt befintliga `docs/`
   (problem-statement, vision, etc), så används inte här.
2. **Rotmappen på huvudbranchen** — för stort av en miljö för bara en
   demo, vi vill inte att `index.html` ligger i repo-roten.
3. **GitHub Actions med valfri källmapp** — det vi rekommenderar för
   `docs-demo/`.

### Alternativ A — minsta möjliga workflow (rekommenderat)

Skapa `.github/workflows/pages.yml` i repo-roten med:

```yaml
name: Deploy docs-demo to GitHub Pages
on:
  push:
    branches: [main]
    paths: ['docs-demo/**', '.github/workflows/pages.yml']
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: true
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./docs-demo
      - id: deployment
        uses: actions/deploy-pages@v4
```

Sen i GitHub: **Settings → Pages → Source: GitHub Actions**.

Första pushen efter att workflowet är på plats publicerar demon.

### Alternativ B — flytta `docs-demo/` till `gh-pages`-branch

Skapa en separat `gh-pages`-branch som bara innehåller innehållet i
`docs-demo/`. Mer hantverk men kräver inget Actions-workflow. Hoppa
över om alternativ A funkar.

## Filstruktur

```
docs-demo/
├── README.md                  ← du läser den
├── index.html                 ← hela demon (HTML + CSS + JS inline)
├── data/
│   └── mock-analysis.json     ← förinspelade Claude Vision-svar
└── assets/
    ├── planritning.pdf        ← 1.3 MB PDF (Hallvägen 21 entréplan)
    └── img-01.jpg ... img-10.jpg  ← 10 interiörbilder, max 1200 px, JPEG 80
```

Totalt ~2.6 MB. Liten nog för GitHub Pages utan friktion.

## Mock-data — vad är fejk och vad är riktigt

| | Status |
|---|---|
| Bilderna | **Riktiga** — kopior från Lokalguidens publika annons för Hallvägen 21, komprimerade till 1200 px |
| Planritningen | **Riktig** — original PDF från Lokalguiden |
| AI-analysen | **Riktig output, mockad uppspelning** — `claude-sonnet-4-6` kördes mot bilderna 2026-05-14, resultatet sparades i `data/mock-analysis.json` och spelas upp med simulerad latency |
| Zon-tilldelningen | **Förvald** — varje bild har en sannolik zon i `default_zone_mapping`. Användaren kan ändra. |
| Dublett-heuristiken | **Riktig kod** — Jaccard-similarity körs live i klienten på den mock-laddade datan |
| Edit / remove / mark-as-dup | **Riktig** — all mutation sker i klienten, ingen lagring |

Mock-uppspelningen ger en realistisk demo eftersom output kommer från
samma modell man skulle använda i produktion — bara fångad tidigare
istället för i realtid. Latency simuleras med 700–1100 ms per bild för
att inte vara *för* snabb att se trovärdig ut.

## Säkerhet och privacy

- **Ingen `ANTHROPIC_API_KEY`** finns i `docs-demo/` — verifierat med grep
- **Inga fetches mot live API** — endast `fetch('./data/mock-analysis.json')` (relativ, samma host)
- **Inga absoluta paths** — fungerar på vilken GitHub Pages-subpath som helst
- **Inga cookies, ingen state mellan sessioner, ingen analytics**
- **Inga tracking-pixels eller tredjepartsskript**

Bilderna är publika från Lokalguidens annons. Användning för demonstrativa,
icke-kommersiella syften.

## Detta är experiment, inte produkt

Texten på sidan är medveten om att detta är prototyp:

- "Prototype demo — Salvage Vision" i bannern överst
- "MOCK DATA"-tag bredvid titeln
- "Mocked Claude Vision output"-pill bredvid bild-grid
- Footer som anger när datan fångades och var bilderna kommer ifrån

Inga claims om att verktyget är klart, säljbart eller produktionsmässigt.
