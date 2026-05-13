---
title: Validated learnings — Salvage Vision
description: Vad vi empiriskt har verifierat, separerat från observationer, hypoteser och grundantaganden
category: external-doc
status: draft
last_updated: 2026-05-13
sections:
  - Verifierat — med data
  - Observerat — men inte systematiskt mätt
  - Hypoteser vi ännu inte verifierat
  - Antaganden vi behöver testa
---

# Validated learnings — Salvage Vision

Denna doc skiljer mellan **vad vi har data på** och **vad vi tror**. Det
är viktigt — speciellt när vi pratar med proffs som måste fatta beslut
på verifierade fakta, inte AI-prat.

## Verifierat — med data

Saker vi *har* mätt och kan visa källa på.

| Lärdom | Hur det mättes | Källa |
|---|---|---|
| Claude Sonnet 4.6 producerar användbara inventeringsutkast | 7 bilder, snittbetyg 3.6/5 → 4.0/5 efter prompt-iteration | `breadth-test-001`, `prompt-iteration-001` |
| Latency per bild håller under 30 s med god marginal | Min 4 s, max 12 s, median 8–10 s | `breadth-test-001`, `prompt-iteration-001` |
| En restriktiv prompt eliminerade dubbelräkning helt | 3 fall → 0 fall | `prompt-iteration-001` |
| En restriktiv prompt eliminerade närbild-extrapolation | 2 av 2 fall fixade | `prompt-iteration-001` |
| En restriktiv prompt halverade hallucinationer | 4 fall → 2 fall (–50 %) | `prompt-iteration-001` |
| Användaren kan korrigera AI:ns output in-place | E2E mot live API, alla 3 redigeringstyper landar korrekt i `/saved` | `edit-flow-e2e-001` |
| `confidence`-fältet är *inte* en pålitlig hallucinationsindikator | Modellen markerar egna kompletteringar med "high" | `prompt-iteration-001` |
| Manuell zon-gruppering ger användbart underlag | 10 bilder → 60 items över 5 zoner på 33 s, dubletter rätt-flaggade | `room-aggregation-001` |
| Dublett-heuristiken (Jaccard ≥ 0.4) flaggar rätt par | Img-04 ↔ Img-08 samma kök fångades, 5 av 7 flaggor träffade | `room-aggregation-001` |
| Anthropic vision-API har 5 MB-gräns på base64 | 5 av 10 bilder failade utan kompression | `room-aggregation-001` |
| Publika lokalannonser har systematisk bildurvalsbias | Hallvägen: 0/8 zoner med WC/MÖTE i bilderna. Wagnshuset: 8/15 bilder är inte ens i lokalen | `field-test-candidate-001`, `field-test-candidate-002` |

Alla källor är experiment-loggar i `experiments/`-mappen i repot.

## Observerat — men inte systematiskt mätt

Saker vi har sett upprepat men inte mätit med tal.

- **Närbilder är systematiskt svårare** — AI vill alltid gissa hela
  rummets storlek från en fragmentbild.
- **Material-feltolkning på metaller** — koppar och patinerad brons
  kallas konsekvent stål eller gjutjärn.
- **"Borde finnas"-hallucinationer** — kylskåp som inte syns, taklampor
  förväxlat med rottingstolar. Allt med hög confidence.
- **AI:n är inte konsekvent i material­namngivning** — samma material
  i olika bilder beskrivs olika ord.
- **Bildurvalets bias kostar i fält** — om WC inte är fotad finns den
  inte i inventeringen.
- **Annonsbias är inte plattform­specifik** — det är hur marknadsföring
  fungerar i hela branschen.
- **Planritning som referens hjälper** — utan ritning blir
  zon-tilldelning gissningsarbete.
- **Färgkodning av zoner i UI** hjälper visuell skanning utan att
  vi mätte det formellt.

## Hypoteser vi ännu inte verifierat

Saker vi tror men inte har data på. Var och en är en kandidat för
nästa experiment.

| Hypotes | Hur vi skulle kunna testa det |
|---|---|
| AI-utkast är snabbare än tomt formulär | Tidsmätning människa vs AI-assisted för en hel lokal |
| Workflowet håller skalat till 30–50 bilder | Fältprov i större lokal |
| En icke-expert kan producera trovärdigt underlag | Användartest med arkitekt utan återbrukserfarenhet |
| Few-shot examples eliminerar "borde finnas"-bias | Iterera prompten med konkreta exempel |
| Dublett-heuristiken skalar till hundratals items | Större zon-aggregeringstest |
| Multi-bild-merge är värt jobbet | Bygga och mäta jämfört med manuell konsolidering |
| Riktiga foton från fält är "bättre" än annonsbilder | Jämförelse, samma lokal båda dataset-typerna |
| Konsoliderings-UI minskar dublett-friktion mätbart | Bygga en första version och mäta korrigeringstid |

## Antaganden vi behöver testa

Saker som *inte är hypoteser* utan grundpremisser för hela projektet.
Om de visar sig vara fel behöver vi tänka om från början.

- **Det finns ett verkligt problem** — att återbruksinventering är
  fragmenterat och dyrt nog att ett verktyg skulle ha värde.
- **AI-assistans accepteras av branschen** — inte avvisas som "vi vill
  inte bli ersatta".
- **Bildfoto är rätt input-format** — inte 3D-scan, LiDAR, eller annat.
- **Användaren vill ha ett verktyg** — inte en tjänst där någon annan
  gör jobbet åt dem.
- **Domänmodellen** (Project → Location → Capture → Observation →
  MaterialItem → Assessment → ReuseOption → DesignScenario) matchar
  hur proffsen faktiskt tänker.
- **Värde vs hinder/möjlighet** är meningsfulla dikotomier — eller
  är det mer än två kategorier?

Att vi *inte* vet detta gör det viktigt att prata med riktiga arkitekter
och återbruks­konsulter *innan* vi bygger mer produkt.
