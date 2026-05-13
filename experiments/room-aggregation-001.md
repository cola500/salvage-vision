---
title: Room aggregation 001 — gruppering per zon + samlad inventering för Hallvägen 21
description: Minsta möjliga slice för att testa multi-bild zonbaserad inventering med manuell mapping, AI-analys per bild, och dublett-heuristik
category: workflow-validation
status: confirmed
last_updated: 2026-05-13
sections:
  - Hypothesis
  - Vad som byggdes
  - Förenklingar vi medvetet gjorde
  - Test-procedur
  - Observationer
  - Vad blev bra
  - Vad blev grötigt
  - Dedup-smärtan
  - Workflow-känsla
  - Nästa största risk
  - Decision
---

# Room aggregation 001 — gruppering per zon + samlad inventering

Bygger på dataset från [`field-test-candidate-001.md`](field-test-candidate-001.md):
10 bilder + planritning från Hallvägen 21, plan 4 (Slakthusområdet).

## Hypothesis

> En användare kan manuellt gruppera bilder per rum/zon och få ett mer
> användbart återbruksunderlag än att titta på 10 separata
> bildanalyser sida vid sida.

Underhypoteser vi vill testa empiriskt:

- **Hjälper ritningen som referens** för att tilldela zoner?
- **Hjälper zonbaserad gruppering** att göra summan begriplig?
- **Hur stort är dedup-problemet** när två bilder visar samma kök/möbler?
- **Känns workflowet närmare ett verkligt återbruksbesök** än
  single-bild-flowet?

## Vad som byggdes

Tre nya endpoints i `app.py` (befintliga `/`, `/analyze`, `/save`,
`/saved` orörda):

| Endpoint | Syfte |
|---|---|
| `GET /dataset/<filename>` | Serverar planritning + bilder från `test-datasets/field-test-001/` (whitelist) |
| `POST /analyze-dataset/<filename>` | Läser bild från disk och anropar Claude Vision — ingen klient-roundtrip |
| `GET /rooms` | Hela det nya UI:t inline (HTML/CSS/JS i en sträng) |

UI-sektioner (alla på en sida):

1. **Planritning** — `<embed>` PDF-preview överst
2. **Bilder (10)** — grid av kort med thumbnail, filnamn, zon-dropdown,
   "Analysera"-knapp per bild, "Analysera alla otaganalysade"-knapp
3. **Per zon** — aggregeringstabell per zon med items från alla bilder
   tilldelade den zonen; per rad: contenteditable celler, möjlig-
   dublett-flag, ✕-knapp för borttagning, 🔗-knapp för manuell dublett-
   markering
4. **Samlad inventering** — sammanställning över alla zoner exklusive
   OUTSIDE_LOCAL, exklusive borttagna och dublettmarkerade

Hårdkodade zoner: `KONTOR`, `MÖTE`, `SAMTAL`, `PENTRY_PAUS`, `ENTRÉ`,
`OUTSIDE_LOCAL`.

Dublett-heuristik (JS, körs per zon):
- Tokenize `material` och `object` (lowercase, splittas på whitespace,
  tokens < 3 tecken filtreras bort)
- Jaccard-similaritet mellan items inom samma zon
- Flagga om `(j_material + j_object) / 2 ≥ 0.4`
- Endast flagga — användaren bestämmer själv om det är en dublett

## Förenklingar vi medvetet gjorde

- **Inget drag/drop** — bara dropdown för zontilldelning. Drag/drop är
  dyrt att få rätt och tillförde inget för hypotesen.
- **Hårdkodade zoner i kod** — ingen CRUD, ingen settings-page. Slicen
  testar gruppering, inte zon-hantering.
- **In-memory state** — laddar om sidan = börja om. Ingen `/save`
  för zon-aggregerad data (befintliga `/save` är för single-bild).
- **Inget `Project` / `Location` / `Capture` i kod** — vi använder en
  platt struktur i klienten. Domänmodellen från README finns *som
  målbild* för senare, men inte i denna slice.
- **Ingen sammanslagning av dubletter** — användaren tar bort eller
  markerar manuellt. Automatisk merge är en egen slice (om någonsin).
- **Samma PROMPT** som single-bild-flowet — vi testar workflow, inte
  prompt.
- **Sekventiell analys, en bild i taget** *eller* "Analysera alla" som
  kör 3 parallellt (för att inte trigga rate limits eller blockera UI:t).
- **Inget skydd för path traversal utöver whitelist** — endpoint
  validerar att filename är i listan över kända filer.

## Test-procedur

1. Starta appen med `ANTHROPIC_API_KEY` satt (från
   `~/Development/equinet/.env`)
2. Öppna `http://localhost:5050/rooms`
3. Granska planritningen i preview
4. Tilldela zon till var och en av de 10 bilderna med dropdown
   (utifrån mapping i `field-test-candidate-001.md`)
5. Klicka "Analysera alla otaganalysade"
6. Vänta ut alla analyser
7. Granska per-zon-aggregering
8. Markera/ta bort minst en uppenbar dublett (mellan img-04/img-08
   för pentry)
9. Korrigera minst en cell
10. Granska samlad inventering

## Observationer

### Oväntat fynd: Anthropic 5 MB-gräns på bilder

Första testkörningen failade på **5 av 10 bilder** med:

> `image exceeds 5 MB maximum: 5779140 bytes > 5242880 bytes`

Lokalguidens bilder är 3–4.5 MB JPEG → 4–6 MB base64. Hälften ramlade
över. Användaren såg mock-svar med felmeddelande i `_source`.

**Fix**: Lade till `Pillow` som dep + en liten `_compress_for_api()`-
helper som downsizar till max 1920 px och re-encodar JPEG 85 om
base64-uppskattningen överskrider gränsen. Endast `/analyze-dataset`
ändrad — `/analyze` orörd. Den klassiska "lekstuga håller inte
verkligheten"-lärdomen, värd att backloggas för single-bild-flowet
också.

Efter fix: **10 av 10 lyckades på 33 s** med `claude-sonnet-4-6`
(3 parallella requests).

### Per-zon resultat (efter analys)

| Zon | Bilder | Items | Dublett-flaggor |
|---|---|---|---|
| KONTOR | 1 (img-10) | 8 | 0 |
| MÖTE | **0** | 0 | — |
| SAMTAL | 3 (img-01, img-03, img-05) | 22 | **0** |
| PENTRY_PAUS | 3 (img-04, img-06, img-08) | 23 | **7** |
| ENTRÉ | 1 (img-07) | 7 | 0 |
| OUTSIDE_LOCAL | 2 (img-02, img-09) | 13 | 2 |
| **Total (exkl. OUTSIDE_LOCAL)** | **8 bilder** | **60 items** | — |

### Manuella operationer testade (alla fungerar)

- Redigera cell → state uppdaterad, total live-uppdaterad ✓
- Markera som dublett (🔗) → rad nedtonad, exkluderad från total ✓
- Ta bort (✕) → rad strikethrough, exkluderad från total ✓
- Live-räkning av "live items" per zon ✓
- OUTSIDE_LOCAL exkluderas automatiskt från total ✓

## Vad blev bra

- **Sidlayouten håller** trots 10 bilder + 6 zoner + 60+ items.
  Planritning överst, bilder, zoner, total — flödet är logiskt och
  varje sektion ryms på rimlig skärmhöjd.
- **Planritningen som referens** är ovärderlig. Att se zon-namnen
  bokstavligt på ritningen gör tilldelningen i dropdown trivial. Utan
  ritningen skulle "är det här PENTRY/PAUS eller KONTOR?" varit
  gissningsarbete.
- **Per-zon-aggregeringen är begriplig.** Att se alla
  pentry-observationer från tre olika bilder samtidigt är *mycket*
  mer användbart än att hoppa mellan tre rå JSON-svar.
- **Färgkodningen på zoner** (gul KONTOR, blå MÖTE, grön SAMTAL, etc)
  bär lågt visuellt brus men hjälper ögat att kategorisera snabbt
  både i kort, tabellrubriker och total-tabellen.
- **3 parallella analyser** är en bra balans — 10 bilder på 33 s.
  Sekventiellt skulle blivit ~90 s (för mycket väntan); 10 parallella
  riskerar rate limits. 3 är sweet spot.
- **`OUTSIDE_LOCAL`-zonen** visade sig vara värdefull. Trapphus och
  husets entré (img-02, img-09) togs ändå med i bildurvalet, och
  utan denna zon hade deras 13 observationer förorenat
  lokal-totalen. *Att kunna märka bilder som "inte mitt material"
  är en feature jag inte hade sett komma.*

## Vad blev grötigt

- **23 items i PENTRY_PAUS från 3 bilder.** Det är *mycket* för en
  liten pentry. AI:n listar alla möbler, alla armaturer, alla
  apparater, vägg och golv från varje bild. Aggregeringen blir
  visuellt tung och redundant utan att alla dubletter flaggas (se
  nedan).
- **Bara *en* SAMTAL-zon trots att ritningen har två samtalsrum.**
  Mitt mapping-förslag klumpade ihop allt SAMTAL-aktigt i en zon —
  vilket är vad datamodellen tillåter idag. För en riktig
  inventering vill man veta vilket av de två som inventeras. Här
  brister den platta zon-modellen.
- **Total-tabellen är 60 rader.** Skummbart men inte sammanställt —
  det är fortfarande en summering av observationer, inte en
  *konsolidered* lokal-inventering. Användaren måste manuellt slå
  ihop "Köksskåp ca 4–5 löpmeter" från img-04 och img-08 till en
  rad. Vi har inget verktyg för det än.

## Dedup-smärtan

Heuristikens precision verkar bra, recall svår att mäta utan
ground truth.

**Heuristiken (Jaccard på material+object, threshold 0.4) fångade
faktiska dubletter:**

- `img-04` ↔ `img-08`: båda visar samma kök. Heuristiken flaggade
  5 par (köksskåp ↔ köksskåp; bänkskiva ↔ diskbänk; matbord ↔
  matbord; stolar; m.fl.) — exakt vad vi förväntade oss.
- `img-02` ↔ `img-09`: båda visar samma trapphus från olika vinklar.
  2 flaggor (träräcken, terrazzogolv).

**Heuristiken flaggade INTE — och det var rätt:**

- SAMTAL (img-01, img-03, img-05) → 0 flaggor. När jag granskar
  råa observationer är dessa **tre olika rum/zoner** med olika
  fokus: img-01 (träportar + glas-rumsavdelare), img-03 (mörka
  pivot-dörrar + kopiator), img-05 (ribbpanel + soffa + lerkonst).
  Materialet är olika, objekten är olika — heuristiken har rätt.
- img-06 (pentry-kafféhörn) vs img-04/08 (samma pentry men annan
  vinkel) → 0 flaggor mellan img-06 och de andra. Råobservationer:
  img-06 fokuserar på vinglas, kaffemaskin, vattenkokare,
  fönsterbänk — som *inte* listas i img-04/08. Korrekt: olika
  fokus i samma rum = inte dubletter, utan komplementära
  observationer.

**Smärtpunkter:**

1. **Kvantiteter dubbel räknas inte automatiskt.** Om img-04 och
   img-08 båda säger "ca 5 löpmeter bänkrad" så markeras det som
   dublett — men användaren ska *välja en*, inte addera. Vi har
   ingen UI för "behåll img-04:s siffra, kasta img-08:s".
   Markera-som-dublett ger samma effekt men semantiken är otydlig.
2. **AI:n beskriver samma sak olika.** "Köksskåp under- och
   överskåp" vs "Köksskåp (över- och underskåp samt höga skåp)"
   blir Jaccard ~0.5 — *precis* över tröskeln, men ord-stävning
   som "höga" eller "stommar" får poängen att svänga. Threshold
   0.4 räcker idag men är skört.
3. **Olika typsignaturer för samma material.** "Trä (mahogny eller
   liknande rödbrunt trä)" vs "Trä (samma som dörrarna, mörkbrun)"
   beskriver samma trä, men Jaccard skiljer dem. AI:n är inte
   konsekvent över bilder, även med samma prompt.

## Workflow-känsla

**Närmare ett riktigt återbruksbesök än single-bild-flowet** — men
fortfarande tech-demo i några avseenden.

**Vad känns autentiskt:**

- Att börja med planritning för orientering är hur konsulten
  faktiskt jobbar.
- Att tilldela bilder per zon känns naturligt — det är vad man gör
  mentalt redan idag.
- Att se en aggregerad lista per zon känns som ett steg närmare
  "ett underlag man kan skicka vidare", inte bara "rådata från
  10 bildanalyser".

**Vad känns fortfarande som demo:**

- Bilder är förvalda och hårdkodade — i verklig session laddar
  användaren upp egna bilder från mobilen.
- Inga "Project" eller "Location" som container — vi har bara
  zoner för exakt denna lokal.
- Inga `Assessment` (värde, hinder/möjlighet) eller `ReuseOption`
  fält. Aggregeringen är observation-nivå, inte beslutsnivå.
- Mängdberäkningarna är fortfarande AI:ns gissningar — ingen
  korrigering mot ritningens skalstreck.

## Nästa största risk

**Skalning + zon-hierarki.** Tre konkreta saker:

1. **23 items i PENTRY från 3 bilder** är obekväma att granska men
   görbart. Vid 5 bilder per rum × 8 zoner ≈ 40 bilder och
   potentiellt 200+ items. Då bryts visuell skanning, och
   O(n²)-dedup-heuristiken inom en zon börjar kosta märkbart.
2. **"En zon" räcker inte.** Ritningen visar 2 SAMTAL-rum men vi
   har bara en SAMTAL-zon. Vid större lokaler (kontor med 5
   kontorslandskap-zoner, 3 mötesrum) blir det orent.
   `Location` med `parent` (Project → Plan → Rum → Zon) blir
   relevant snabbare än vi anade.
3. **Annonsbias-luckan kvarstår.** Vi hade tre bilder av pentry,
   noll av MÖTE — det största rummet. Workflowet kan inte
   kompensera för dåligt bildurval. En "checklista per zon: ta
   bild av denna" innan eller under fältarbetet är troligen
   nästa-nästa-slice.

Andra risker som inte är *största* men värda att notera:

- **Bildkomprimering är inte versionshanterad.** Vi vet inte
  exakt vad som skickas till Anthropic — användaren ser
  originalet i UI:t, men API:n får en omkomprimerad version.
- **`/analyze` (single-bild) har samma 5 MB-bug** — bör fixas
  vid nästa tillfälle, men inte i denna slice.
- **PDF-preview** funkar i Chrome via `<embed>` men kan strula
  i Safari/Firefox. Fallback-länk finns.

## Decision

**Slicen är validerad.** Hypotesen håller: manuell zonbaserad
gruppering ger ett mer användbart underlag än 10 separata
bildanalyser.

**Nästa naturliga steg, prioriterad ordning:**

1. **Konsolideringssteg per zon** — UI för att slå ihop dubletter
   till en rad istället för att bara markera. Det är där den
   största "manuell jobb"-friktionen är efter denna slice.
2. **Hierarkisk Location-modell** — minst Project → Room → Image,
   så vi kan ha "SAMTAL höger" och "SAMTAL söder" separat. Inte
   stort, men berör datamodellen.
3. **Foton tagna i fält** istället för annonsfoton — testa om
   bias-luckan försvinner när användaren själv styr urvalet.
4. **Backlog**: prompt-hint så AI:n är mer konsekvent i sin
   material-namngivning (för att förbättra dedup-recall);
   tidsmätning människa vs AI för en samlad inventering;
   "checklista per zon".

**Ingenting av detta påbörjas innan användaren bestämmer.**
