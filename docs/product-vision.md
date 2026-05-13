---
title: Product vision — Salvage Vision
description: Visionen från lokal till återbruksbeslut med människa i loopen, observationer som inte är fakta, och stegvis byggnation
category: external-doc
status: draft
last_updated: 2026-05-13
sections:
  - Visionen
  - Människa-i-loopen
  - Observationer ≠ fakta
  - Stegvis byggnation
  - MVP — vad vi har idag
  - Medellång sikt — om hypoteserna håller
  - Långt bort — möjliga riktningar
  - Vad vi medvetet inte bygger
---

# Product vision — Salvage Vision

## Visionen

Från en bild på en lokal till ett underlag som påverkar nya ritningar —
utan att människan ska göra all datainmatning, och utan att AI:n ska
få fatta beslutet.

Inte "AI gör återbruksinventeringar". Snarare: **människan behåller
bedömningen, AI:n tar datainmatningen och håller ordning på fragmenten**.

## Människa-i-loopen

Varje del av flödet ska vara byggt så att:

- AI-output är **alltid ett förslag**, aldrig fakta.
- Användaren ska kunna **bekräfta, korrigera eller avvisa** varje
  observation.
- Bedömningar (värde, hinder/möjlighet, skick) görs av människa —
  AI ger utkast eller stödjer underlag.
- Återbruksbeslut är **människans**, inte systemets.

Det är inte en begränsning som ska avvecklas på sikt — det är
designprincipen som gör verktyget tillitsvärdigt i en bransch som är
försiktig med beslut.

## Observationer ≠ fakta

Datamodellen skiljer på olika lager:

| Lager | Vad det är |
|---|---|
| **Capture** | Källan — en bild, video-frame eller anteckning |
| **Observation** | Ett påstående om att något syns. Har källa (AI/människa/sensor) och osäkerhet |
| **MaterialItem** | Den konsoliderade bilden av vad som finns. Byggd av många observationer |
| **Assessment** | Värde, hinder/möjlighet — domänbedömning |
| **ReuseOption** | Möjlig återbruks­väg med krav |
| **DesignScenario** | Hur material kan informera ny ritning |

Skillnaden mellan `Observation` och `MaterialItem` är central: en
enskild AI-tolkning av en bild är *aldrig* en sanning om lokalen.
Sanning byggs över tid genom fler observationer — fler bilder,
mänsklig bekräftelse, kompletterande data.

## Stegvis byggnation

Workflowet ska följa hur en konsult faktiskt jobbar:

```
1. Fånga lokal          →  Capture (bilder, video, anteckningar)
2. Identifiera material →  Observation → utkast på MaterialItem
3. Korrigera / validera →  Människa bekräftar eller skriver om
4. Bedöm värde + hinder →  Assessment (med stöd, ej automatik)
5. Skapa återbrukskandidater → ReuseOption
6. Påverka ny design    →  DesignScenario
```

Idag är steg 1–3 byggda. Steg 4–6 finns i datamodellen men inte i koden
— och de byggs *inte* förrän vi vet att 1–3 håller mot riktig data.

## MVP — vad vi har idag

- Bild → AI-utkast → strukturerad inventeringslista (steg 1–2)
- Användaren kan korrigera AI:ns output cell-för-cell (steg 3)
- Flera bilder kan grupperas per zon, summeras till lokal-total
- Möjliga dubletter flaggas automatiskt
- In-memory, single-user, lokalt

Det är inte en produkt. Det är ett verktyg för att testa hypoteserna.

## Medellång sikt — om hypoteserna håller

Det vi tror är nästa stora steg, *givet att fältprov bekräftar att
workflowet håller*:

- **Konsolidering per zon** — kombinera dubletter till en rad istället
  för att bara markera
- **Project / Location-hierarki** — ett kontor kan ha 8 rum, ett rum
  kan ha 4 bilder, allt hör ihop
- **Multi-bild-merge** — slå ihop tre bilder av samma rum till en
  konsistent lista
- **Mobil-fältverktyg** — ta bilder direkt i lokalen, inte bara
  ladda upp
- **Assessment-fält** — värde, hinder, skick som förstklassiga fält
- **CSV / Excel-export** — för dem som vill ta data vidare i sina
  befintliga verktyg
- **Coverage-checklista** — påminnelse om vilka zoner som ännu ej
  är fotade

Inte allt på en gång. Varje del bör bekräftas mot riktig användning
innan nästa byggs.

## Långt bort — möjliga riktningar

Det här är *inte* roadmap. Det är möjligheter som hypoteser kan leda
till. Inget byggs förrän vi har data som visar att det är värt det.

- **Multi-user samarbete** — arkitekt + återbruks­konsult +
  fastighetsägare i samma inventering
- **Materialbank-koppling** — direktkoppling till befintliga
  marketplaces (CCBuild, Återhuset, etc)
- **CAD/BIM-integration** — importera ritningar direkt från
  arkitektens verktyg
- **Spatial mapping** — automatisk koppling mellan bild och zon
  via metadata eller landmärken
- **CO₂-beräkning** — koppla material­mängd till klimatdeklaration
- **Förslag på ny design** — AI som föreslår layout baserat på
  befintliga material
- **Skick-bedömning från foto** — när vision-modeller blir bättre

## Vad vi medvetet inte bygger

- **Automatisk beslutsfattning** — människan beslutar, alltid
- **Mass-produktion av inventeringar** — kvalitet före volym
- **"AI-driven återbruksinventering"-marknadsföring** — det är fel
  framing av värdet
- **Egen marknadsplats** — andra gör det bättre
- **Pris-prediktion** — för känsligt utan transparens

Visionen är **att assistera proffsen**, inte ersätta dem.
