---
title: Retro 001 — dagens arbete 2026-05-13
description: Retrospektiv över första intensiva arbetsdagen — sju slices från CLAUDE.md till README v2 med domänmodell
category: retrospective
status: confirmed
last_updated: 2026-05-13
sections:
  - Vad vi gjorde
  - Vad som gick bra
  - Vad som var svårare än väntat
  - Lärdomar — domän
  - Lärdomar — metod
  - Beslut framåt
  - Risker att hålla ögon på
---

# Retro 001 — dagens arbete 2026-05-13

Första intensiva arbetsdagen i salvage-vision. Sju commits (åtta inklusive
synology-helper-uppdateringen), tio slices i hypotes-driven loop. Retron
skrevs samma dag direkt efter sista commiten.

## Vad vi gjorde

| # | Slice | Outcome |
|---|---|---|
| 1 | `CLAUDE.md` — repo-specifik guidance | Lade fundament för konsekvent arbetsstil |
| 2 | Breadth test scaffold | Strukturerad mall innan datainsamling |
| 3 | Breadth test (7 bilder) | Snitt **3.6/5**, tre felmönster identifierade |
| 4 | Prompt iteration 001 | Snitt **4.0/5**, dubbelräkning + närbild-extrapolation **eliminerade** |
| 5 | Redigerbar tabell (UI-slice) | Minimal contenteditable, +26 rader |
| 6 | E2E mot live API | 9.4 s, alla edits landar i `/saved` |
| 7 | Push till NAS git-server | Repo `salvage-vision.git` skapat på `/volume1/git/` |
| 8 | Synology-helper tabell-uppdatering | Konsistens i ops-dokumentationen |
| 9 | README v1 | Grundläggande projektdokumentation |
| 10 | README v2 | Omformulering till beslutsstöd + domänmodell |

## Vad som gick bra

- **Hypotes-driven slicing levererade konsekvent.** Varje slice hade ett
  mätbart utfall (snittbetyg, halverade hallucinationer, alla 3 edits
  landar, etc). Vi visste alltid om vi var "klar" eller inte.
- **Mock-fallbacken sparade tid och pengar.** UI-testet av redigerbar
  tabell kördes utan API-anrop. Det är ett designval värt att hålla.
- **Prompt-iterationen mätte sig själv mot tidigare data.** Att vi hade
  kvar v1-JSON från breadth-testet gjorde jämförelsen rättvis i stället
  för anekdotisk.
- **NAS-pushen var triviell tack vare befintlig dokumentation** i
  synology-helper. Bra exempel på "dokumentera mönster en gång,
  återanvänd". Värt att replikera.
- **README växte i två steg.** v1 var bredare basversion, v2
  introducerade domänmodell + beslutsstöd-framing utan att skriva om
  historien. Iterativ skrift fungerar för docs likaväl som kod.

## Vad som var svårare än väntat

- **"Borde finnas"-hallucinationerna var envisare än prognosen.** Kylskåp
  (B-01) och rotting-taklampa (B-04) överlevde tre regler *och* fick
  "high" confidence av modellen själv. Textbaserade regler räcker inte
  mot bias som modellen *tror på*. Few-shot är troligen rätt nästa
  intervention — men det är ett rejält post i backlog, inte en quick fix.
- **Manuell bildbedömning skalar inte.** Att läsa varje bild + jämföra
  mot JSON tog signifikant tid för 7 bilder. För fältprovet med 10–20
  bilder behöver vi en mer systematisk metod — antingen ett
  bedömningsformulär, eller dela upp arbetet (Johan tar
  bedömningsrundan, Claude aggregerar siffrorna).
- **Filer med mellanslag i namn** ("B-02-skåp ugn micro.jpeg") bet i
  några shell-loops. Triviala att fixa med quoting, men värt att
  standardisera filnamn utan space framöver.
- **API-nyckelns placering** (i `equinet/.env`) var inte uppenbar för
  Claude första gången. Andra gången gick det snabbt. Värt en rad i
  `CLAUDE.md`.

## Lärdomar — domän

1. **`confidence` från en LLM är inte en pålitlig
   hallucinationsindikator.** Modellen markerar sina egna kompletteringar
   med samma säkerhet som verkliga observationer. Vi kan visa fältet i
   UI:t, men det är inte ett "filtrera bort osäkra"-verktyg utan
   kvalifikation.
2. **AI är duglig på "vad är detta", svagare på "hur mycket", oduglig
   på "vad är det värt".** De tre frågorna kräver olika typer av stöd.
   Bildanalys → råmaterial, inte beslutsunderlag.
3. **Närbilder är systematiskt svåra.** Regel B löste de testade fallen,
   men vi har ingen anledning att tro att alla fragment-fall är lösta.
   Värt att medvetet testa i fältprovet.
4. **Domänmodellen avslöjade kodens platta natur.** Vi har `items[]`
   direkt, ingen Project/Location/Assessment. Det är OK för en validering
   av steg 1–3 i flödet, men gör att multi-bild-merge blir nästa
   naturliga arkitektur-steg, inte ett "lättadderat" tillägg.

## Lärdomar — metod

1. **Time budgets respekteras lättast när varje slice är en hypotes.**
   Vi stannade aldrig för att "det skulle se klart ut" — vi stannade när
   hypotesen var avgjord. Det är skillnaden mellan prototyp och produkt.
2. **Iterativ dokumentation funkar.** README v1 → v2 utan att skriva om
   historien. Samma princip vi använder för kod tycks gälla för docs.
3. **NAS-remote är låg friktion när dokumentationen finns.** Att inte ha
   en GitHub-bas är ingen blockerare.

## Beslut framåt

- **Nästa session: fältprovet** (10–20 bilder från en riktig lokal).
  Inte börja bygga Project/Location-struktur i kod förrän vi sett om
  bildanalysen ens håller skalad.
- **Backlog: few-shot-prompt** (efter fältprovet, inte före).
- **Liten åtgärd för nästa session:** lägg en rad i `CLAUDE.md` om att
  API-nyckeln finns i `~/Development/equinet/.env`. Sparar en fråga
  nästa gång.
- **Pending push:** salvage-vision och synology-helper har varsin lokal
  commit som inte är pushad till NASen vid retrons skrivande. Beslut om
  push tas separat.

## Risker att hålla ögon på

- Hypotesen "AI-utkast > tomt formulär" är validerad på snitt 4.0/5 över
  **enskilda bilder**. Vi vet inte ännu om det håller över **en hel
  lokal**. Fältprovet är den första riktiga risken för hypotesen.
- "Borde finnas"-biasen är fortfarande aktiv. Om fältprovet visar att
  den biten driver mätbart förtroende-bortfall hos en bedömare, blir
  few-shot inte längre "framtida" — det blir blockerande.
