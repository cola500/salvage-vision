---
title: Demo script 001 — 5–10 min walkthrough
description: Manus för att visa Salvage Vision-prototypen för arkitekter, återbruks-konsulter eller fastighetsfolk
category: external-doc
status: draft
last_updated: 2026-05-13
sections:
  - Förberedelser
  - 0:00–1:00 Intro
  - 1:00–2:00 Problemet
  - 2:00–7:00 Demo
  - 7:00–8:00 Begränsningar
  - 8:00–10:00 Frågor till åhöraren
---

# Demo script 001 — 5–10 min walkthrough

Demon bygger på `/rooms`-flowet med Hallvägen 21-datasetet (publik
kontorsannons från Lokalguiden, 186 kvm, 8 zoner, 10 bilder + ritning).

## Förberedelser

- Appen körs med `ANTHROPIC_API_KEY` satt (claude-sonnet-4-6, inte mock)
- Browser öppen på `http://localhost:5050/rooms`
- 10 bilder + planritning ligger förladdade i
  `test-datasets/field-test-001/`
- Valfritt: kör analyzen förhand så latency inte sänker tempot

## 0:00–1:00 — Intro

> "Tack för att du tar tid. Det här är en prototyp — inte en färdig
> produkt. Jag vill visa fem minuter, sen ställa några konkreta frågor."

Säg explicit i öppningen:

- Detta är **experiment-kod**, inte produkt
- Vi har inte byggt värde-/hinder-/skick-bedömning eller ritningskoppling
  — det är vision
- Vi pratar med folk för att förstå om vi går åt rätt håll

## 1:00–2:00 — Problemet

> "Återbruksinventering är ett moment som alla i en ombyggnad rör vid.
> Det börjar typiskt med någon som står i en lokal med ett tomt
> formulär. Mycket tid går åt till att skriva ner uppenbarheter innan
> man kan börja bedöma värde."

Lista de fem frågorna kort:

1. Vad finns här?
2. Vad är det värt?
3. Hinder eller möjlighet?
4. Hur påverkar det den nya designen?
5. Hur sänker vi tröskeln för icke-experter?

> "Vår hypotes är att AI kan hjälpa med fråga 1 och utkast på 2–3 — så
> människan får tid till själva bedömningen. Den här prototypen testar
> om det funkar."

## 2:00–7:00 — Demo

### Visa ritningen (30 sek)

> "Det här är en publik kontorslokalannons från Lokalguiden — Hallvägen
> 21 i Slakthusområdet, 186 kvm, med planritning. Den har 8 zoner:
> KONTOR, MÖTE, två SAMTAL, PENTRY/PAUS, WC, HWC, STÄD och ENTRÉ."

Peka på zonerna i ritningen.

### Visa bildurvalet + zon-tilldelning (1 min)

> "Annonsen har 12 bilder. Vi har laddat 10 av dem. Notera att två är
> trapphus — *utanför* själva lokalen. Det är en datapunkt: foton i
> verkligheten kommer ofta vara felaktigt vinklade."

Klicka på en bild → modal öppnar i fullskärm.

> "Användaren tilldelar varje bild en zon via dropdown. I dagsläget
> manuellt. I framtiden kanske AI hjälper, men det är inte byggt."

Visa hur en bild flyttas mellan zoner.

### Kör AI-analysen (30 sek — hoppa om förladdat)

Klicka "Analysera alla otaganalysade".

> "10 bilder, ungefär 30 sekunder med Claude Sonnet 4.6. Tre parallella
> requests."

Vänta tills färgindikatorn på korten blir grön.

### Visa aggregeringen (1 min)

Scrolla till "Per zon".

> "Här ser vi observationerna grupperade per zon. KONTOR har 1 bild
> med 8 items. PENTRY/PAUS har 3 bilder med 23 items — det är där
> dublett-problemet börjar."

Hovra över en av de gula "möjlig dublett"-flaggorna.

> "Heuristiken är enkel — ord-overlap mellan material och objekt. Den
> flaggar att img-04 och img-08 båda beskriver samma kök. Det är *våra*
> dubletter — vi har inte automatisk merge ännu. Användaren bestämmer."

Markera en rad med 🔗 → "Markera som dublett". Visa att den blir
nedtonad och försvinner från samlad inventering.

### Visa coverage-gapet (1 min)

> "Och här — MÖTE: 0 items, 0 bilder. Ritningen har ett stort
> mötesrum men annonsen fotade aldrig det. Det är annonsbias — och
> det är något AI inte kan kompensera för. Värdefull information
> finns inte med."

> "WC och HWC: 0 bilder. Förråd: 0 bilder. Tre av åtta zoner är
> osynliga. En verklig återbruksinventering kan inte stå sig på
> såna här data."

> "Det är *exakt* den insikten vi behöver — att människan i fält
> behöver en checklista per zon, inte bara 'ta bra bilder'."

### Visa samlad inventering (30 sek)

Scrolla till "Samlad inventering".

> "Här är totalbilden — 60 items över 5 zoner, exklusive
> utanför-lokalen, exklusive borttagna eller markerade som dubletter.
> Per rad: zon, objekt, material, mängd, återbrukspotential, och
> källan."

> "Det är inte ett beslutsunderlag. Det är råmaterial för någon som
> kan bedöma värde och hinder. Det jobbet är fortfarande människans."

## 7:00–8:00 — Begränsningar

Var ärlig om vad som *inte* funkar:

- "Borde finnas"-hallucinationer kvarstår — kylskåp som inte syns,
  rotting-taklampor som egentligen är stolar
- Material-feltolkning på metaller — koppar kallas stål
- Mängd-uppskattning är osäker, särskilt från närbilder
- Inget värde-/hinder-/skick-fält ännu — det är vision, inte byggt
- Inget multi-bild-merge — bara markering
- Inga inkomstkällor, ingen prissättning, inget affärsmodell —
  det är en prototyp

> "Vi tror inte att AI ersätter ert jobb. Vi tror den flyttar er tid
> från datainmatning till bedömning. Frågan är om ni håller med."

## 8:00–10:00 — Frågor till åhöraren

Sluta med konkreta frågor — inte "vad tycker du om idén?". Skriv ner
svaren — det är hela poängen med demon.

1. **Hur jobbar du själv idag?** Excel, block, anteckningar på
   ritning?
2. **Var lägger du mest tid?** Datainmatning eller bedömning?
3. **Vad i det här skulle du faktiskt använda?** Och vad är fel?
4. **Vad saknas?** Vilket fält, vilken yta, vilken bedömning?
5. **Vem skulle du vilja att gjorde inventeringen?** Du själv, en
   yngre arkitekt, byggherren, en specialist?
6. **Vilken kvalitetsnivå krävs** för att du skulle skicka detta
   vidare som underlag?
7. **Vad är värsta tänkbara utfallet** av ett dåligt AI-utkast?

Lyssna, anteckna. Försök undvika att sälja — målet är att lära.
