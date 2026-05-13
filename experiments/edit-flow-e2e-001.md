---
title: Edit flow E2E — validerat med riktig Claude Vision
description: End-to-end-verifiering av redigerbar tabell mot riktig Sonnet 4.6, inte mock
category: implementation-validation
status: confirmed
last_updated: 2026-05-13
sections: [Hypothesis, Method, Results, Decision]
---

# Edit flow E2E — validerat med riktig Claude Vision

## Hypothesis

> Redigerbar-tabell-slicen (commit `c89c355`) fungerar end-to-end med
> riktig AI-analys — inte bara med mock-svar. Användaren kan analysera
> en bild, korrigera AI:ns output i tabellen och spara korrigerade
> värden via `/save`.

## Method

Testat via Playwright mot körande app:

1. App startad med riktig `ANTHROPIC_API_KEY` (från equinet/.env)
2. Bekräftat att `_source: "claude-sonnet-4-6"` — inte mock
3. Uppladdning av `test-images/breadth-001/B-03-badrum toa dusch.jpeg`
4. Klick på "Analysera bild"
5. Tre redigeringar:
   - `items[0].material`: "Porslin/keramik" → "Porslin (vit, ren)"
   - `items[3].quantity`: "ca 2–3 kvm (kan ej bedömas exakt)" → "ca 3 kvm"
   - `items[4].reuse_potential`: "Låg" → "Medium"
6. Klick på "Spara inventering"
7. Verifiering via `GET /saved`

## Results

| Mått | Värde |
|---|---|
| Source | `claude-sonnet-4-6` ✓ (inte mock) |
| Latency (analys) | 9.4 s — under 30 s tröskeln |
| Items returnerade | 6 |
| Redigeringar gjorda | 3 (material, quantity, reuse_potential) |
| Raw JSON-pane sync | Uppdaterad live för alla 3 ✓ |
| Färgklass-byte vid reuse_potential | `low` (rosa) → `med` (gul) ✓ |
| Övriga radernas klasser | Oförändrade ✓ |
| `/saved` innehöll redigerade värden | Alla 3 OK ✓ |
| Buggar observerade | Inga |

## Decision

**Slicen är validerad end-to-end mot riktig modell.** Redigerbar tabell
fungerar som tänkt med Claude-genererad data, inte bara mock.

Vad detta upplåser för nästa steg:
- Vi kan nu mäta *vilka* fel användaren faktiskt korrigerar i UI:t —
  bättre underlag för framtida `prompt-iteration-002` (few-shot mot
  "borde finnas"-hallucinationer) än manuell jämförelse av JSON-output.
- In-memory `/save` räcker för fortsatt validering; persistent lagring
  väntar tills vi har ett tydligt behov.
