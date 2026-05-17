# Salvage Vision — AI-assisterat beslutsstöd för materialåterbruk

> Hypotesdriven prototyp som hjälper någon utan återbrukskompetens att gå från foto av en lokal till ett trovärdigt inventeringsutkast på under 30 sekunder.

<img width="1235" height="599" alt="Screenshot 2026-05-17 at 21 26 39" src="https://github.com/user-attachments/assets/296db83a-e127-44f3-90dd-ab0a79ef78d5" />

<img width="1226" height="467" alt="Screenshot 2026-05-17 at 21 26 59" src="https://github.com/user-attachments/assets/752b8a15-2a29-48a4-ab44-5f448b302775" />

Återbruksinventering i ombyggnadsprojekt är manuellt, tidsödslande och kräver specialistkompetens — vilket gör att den ofta hoppas över. Den här prototypen utforskar om AI kan ta tillräckligt mycket av första utkastet att tröskeln sänks från "expert behövs" till "en arkitekt med en mobiltelefon räcker".

Projektet är **experiment, inte produkt** — varje slice bevisar eller dödar en specifik hypotes innan nästa byggs. Hittills validerat: bild → strukturerad lista är användbart (snitt 4.0/5 över 7 testbilder, latency 6.7–11 s).

## Vad detta repo visar

- **Hypotesdriven AI-produktutveckling i renkultur** — `HYPOTHESIS.md`, `experiments/` med datapunkter per slice, validated learnings med commit-referenser.
- **Domän framför teknik** — README beskriver problemet (5 frågor en beslutsfattare måste ha svar på) innan en enda kodrad nämns.
- **Vertikala slices** — steg 1-3 av flödet (fånga → identifiera → korrigera) är byggt; steg 4-6 (värde, hinder, design) finns som domänmodell men inte kod. Det är avsiktligt: bevisa hållbarhet innan vi bygger ovanpå.
- **Breadth-tests som beslutsverktyg** — `experiments/001` testade 7 bilder och rapporterade snitt-score + variansobservation, inte bara "fungerade".
- **AI som arbetspartner, inte som leverans** — målet är beslutsstöd för människor, inte att eliminera människor.

---
## Problemet

Återbruksinventering är ett nyckelmoment i hållbar ombyggnad — men idag
manuellt, tidsödslande och kräver expertkompetens. För att gå från en
befintlig lokal till ett genomtänkt återbruksbeslut behöver
beslutsfattaren svar på fem frågor:

| # | Fråga | Vad vi vill kunna svara |
|---|---|---|
| 1 | **Vad finns här?** | Material och objekt i lokalen — typ, mängd, skick |
| 2 | **Vad är det värt?** | Ekonomiskt och miljömässigt värde, återbrukspotential |
| 3 | **Hinder eller möjlighet?** | Blockerar materialet ombyggnaden, eller är det en resurs vi bör spara? |
| 4 | **Hur påverkar det den nya designen?** | Kan befintligt material informera ritningar, planlösning, materialval? |
| 5 | **Hur sänker vi tröskeln?** | Hur kan någon *utan* djup återbrukskompetens få ett trovärdigt beslutsunderlag? |

Idag löses #1 manuellt med formulär, #2–#4 av specialister, och #5 sällan
alls. Hypotesen är att AI kan ta en *betydande del* av #1 plus utgöra
första utkast på #2–#3, så att människan kan fokusera på bedömning och
designkonsekvens istället för datainmatning.

## From local capture to reuse decision

Flödet vi designar mot (inte hela byggt än):

```
  1. Fånga lokal              →   Capture (bild, video-frame, anteckning)
  2. Identifiera material     →   Observation → MaterialItem (AI-utkast)
  3. Korrigera / validera     →   Människa bekräftar eller skriver om
  4. Bedöm värde + hinder     →   Assessment (värde, komplexitet, hinder/möjlighet)
  5. Skapa återbrukskandidater →  ReuseOption (väg, krav, validering)
  6. Påverka ny design        →   DesignScenario (senare lager)
```

Idag är steg 1–3 implementerade som första slice (bild → AI-utkast →
redigerbar tabell → spara). Steg 4–6 finns bara som domänmodell och
arkitektur — inte som funktionalitet. Det är avsiktligt: vi bevisar att
steg 1–3 håller innan vi bygger ovanpå.

## Hypotes (confirmed)

Kärnhypotesen som validerats hittills är den smalaste delen av problemet:

> En användare kan ta en bild av ett rum/material och få ett användbart
> första inventeringsutkast på under 30 sekunder — snabbare och bättre
> än att börja från ett tomt formulär.

Bekräftande slices så här långt:

| Slice | Commit | Resultat |
|---|---|---|
| Initial vision-slice | `bfb79f4` | Bild → strukturerad lista, mock-fallback |
| Breadth-test 001 (7 bilder) | `5f645c0` | 7/7 bilder ≥ 2.5/5, snitt **3.6/5**, latency 6.7–11 s |
| Prompt-iteration 001 (restriktiv prompt) | `ca14cc7` | Snitt **4.0/5**, dubbelräkning eliminerad, hallucinationer halverade |
| Redigerbar tabell + E2E mot live API | `c89c355`, `0718215` | Användaren kan korrigera in-place; redigerade värden landar i `/saved` |

Detaljer i [`HYPOTHESIS.md`](HYPOTHESIS.md) och [`experiments/`](experiments/).

Det här är **steg 1–3 i flödet ovan**. Resten av problemet — värde,
hinder, design — är ännu inte validerat empiriskt och måste behandlas
som öppna hypoteser tills vi har data.

## Domänmodell (konceptuell)

Modellen är **inte implementerad** i kod idag (in-memory `SAVED` är
plattare än så). Den finns här för att styra hur vi designar nästa
slices så att de inte målar oss in i ett hörn.

| Entity | Vad det är | Centrala fält | Relationer |
|---|---|---|---|
| **Project** | Ett ombyggnads-/rivningsprojekt | name, status | har många Location |
| **Location / Room / Zone** | Plats inom Project (lokal, rum, zon, vägg) | name, type, parent | har många Capture |
| **Capture** | Observationskälla | type (`image` / `video_frame` / `note`), source, timestamp | ger upphov till många Observation |
| **Observation** | Ett påstående om att något *syns* | source (`ai-vision` / `human` / `sensor`), confidence, visible_evidence | föreslår en MaterialItem |
| **MaterialItem** | Ett fysiskt material/objekt i lokalen | type, object/category, quantity_estimate, unit, condition, uncertainty | har många Observation, en Assessment, ev. flera ReuseOption |
| **Assessment** | Värde- och hinderbedömning | reuse_potential, value_estimate, removal_complexity, risk, obstacle_or_opportunity | hör till MaterialItem |
| **ReuseOption** | Möjlig återbruksväg | possible_reuse, constraints, required_validation | hör till MaterialItem |
| **DesignScenario** | Hur befintliga material kan informera ny design | description, materials_used, layout_implication | senare scenario-lager |

### Relationer i text

```
Project
  └─ Location / Room / Zone
       └─ Capture  (image | video_frame | note)
            └─ Observation  (ai-vision | human | sensor; confidence)
                 └→ föreslår → MaterialItem
                                 ├─ Assessment  (värde, hinder/möjlighet)
                                 └─ ReuseOption (väg, krav, validering)
                                       ↑
                                  DesignScenario  (senare lager — ej MVP)
```

Viktigt:

- **Flera Observation kan peka på samma MaterialItem.** Det är hur vi
  förbättrar kvantitet och säkerhet över tid utan att skriva om data.
- **Capture är källan, MaterialItem är konsensusbilden.** En enskild AI-
  observation är inte sanning — den är ett *förslag*. Mängden konsensus
  växer när människa bekräftar eller fler bilder bekräftar samma sak.
- **Assessment är separat från MaterialItem.** Värde, hinder och risk är
  domänbedömningar som kan ändras utan att vi rör materialets identitet.

## Arkitekturprinciper

Sju principer som styr designval på nästa slices:

1. **AI-output är observationsförslag, inte fakta.** Allt som kommer från
   `/analyze` är en `Observation` med `source: ai-vision` och `confidence`,
   inte en bekräftad `MaterialItem`. Människan eller fler observationer
   gör det till konsensus.
2. **Mängd, yta och volym ska kunna förbättras över tid.** En första
   bild ger grov uppskattning. Fler bilder + mätningar + korrigeringar
   ska kunna förfina utan att skriva om historiken.
3. **Osäkerhet ska modelleras explicit.** Confidence på Observation och
   uncertainty på MaterialItem ska bäras genom hela kedjan — inte gömmas
   bakom punktestimat som ser för säkra ut.
4. **En människa ska kunna korrigera och bekräfta.** Korrigering är en
   förstklassig operation, inte en undantagshantering. Redigerbar tabell
   i dagens slice är den minimala formen av detta.
5. **Flera observationer kan peka på samma material.** Modellen tillåter
   många-till-ett från Observation till MaterialItem från dag ett — även
   om vi i dagens slice bara har en bild per inventering.
6. **Deduplicering är en separat senare förmåga.** Vi *tillåter*
   dubbletter på input-sidan. Att slå ihop "soffan i bild A" och "soffan
   i bild B" är en egen slice — inte en sidoeffekt av ingest.
7. **Ritningar/design är senare scenario-lager, inte MVP.**
   DesignScenario finns i modellen så vi kan se framåt, men byggs inte
   förrän steg 1–5 håller på riktig data.

## Validated learnings

Vad vi har **empiriskt verifierat** så här långt:

| Lärdom | Hur det mättes | Status |
|---|---|---|
| Claude Sonnet 4.6 vision producerar användbara inventeringar | 7 bilder, snittbetyg 3.6/5 → 4.0/5 efter prompt-iteration | ✓ |
| Latency håller under 30 s med god marginal | Min 4 s, max 12 s, median 8–10 s | ✓ |
| Restriktiv prompt eliminerar dubbelräkning | 3 fall → 0 fall (–100 %) | ✓ |
| Restriktiv prompt eliminerar närbild-extrapolation | 2 av 2 bilder fixade | ✓ |
| Restriktiv prompt halverar hallucinationer | 4 fall → 2 fall (–50 %) | ✓ |
| Användaren kan korrigera AI:ns output in-place | E2E mot live API, alla 3 edit-typer i `/saved` | ✓ |
| `confidence`-fältet är *inte* en pålitlig hallucinationsindikator | Modellen ger "high" även på "borde finnas"-hallucinationer | ✗ |

Vad vi har **observerat men inte mätt systematiskt**:

- **Närbilder utan kontext**: AI vill alltid gissa hela rummets storlek.
  Regel B i prompten löste de testade fallen, men fragment ger fortfarande
  ofta fel kvantitet.
- **Material-feltolkning på metaller**: koppar/patinerad brons kallas
  stål/gjutjärn. Kunskaps-/visuellt problem, kan inte promptbasen-lösas.
- **"Borde finnas"-bias**: AI lägger till objekt som *brukar* finnas
  (kylskåp i kök, taklampa i rum där det finns rotting) — och markerar
  dem med high confidence. Few-shot examples är troligen rätt nästa
  intervention.

## Demo-flöde (vad som funkar idag)

Detta är **steg 1–3 i flödet ovan** — inte hela kedjan.

1. Starta appen (se [Köra](#köra))
2. Öppna `http://localhost:5050`
3. Välj en bild — kök, badrum, golv, vad som helst
4. Klicka **Analysera bild** → vänta ~8–10 s
5. Tabellen fylls med rader (material, objekt, mängd, återbrukspotential)
6. **Klicka i en cell för att korrigera** AI:ns gissning
7. Klicka **Spara inventering** — håller listan i minnet
8. `GET /saved` returnerar alla sparade inventeringar

Värde, hinder/möjlighet, återbruksvägar och designkonsekvens *finns inte
i appen idag* — bara i domänmodellen.

## Tech stack

- **Python 3.11+** med `uv` — PEP 723 inline-deps i `app.py`, ingen `requirements.txt`
- **Flask** — HTTP-server + inline HTML/JS för UI i en sträng
- **Anthropic SDK** — modell `claude-sonnet-4-6` (vision)
- **Ingen databas, ingen build-step, ingen extern frontend-bundler**
- Hela appen ligger i `app.py` (≈ 300 rader)

## Köra

```sh
# Med riktig AI
ANTHROPIC_API_KEY=sk-... uv run app.py

# Utan nyckel — appen fallbackar till hårdkodat mock-svar
uv run app.py
```

App körs på **http://localhost:5050**. Port 5000 är blockerad av macOS
AirPlay — använd inte den.

## Projektstruktur

```
salvage-vision/
├── app.py                       ← hela appen (Flask + inline UI)
├── HYPOTHESIS.md                ← ursprunglig hypotes + resultat
├── CLAUDE.md                    ← repo-specifik Claude Code-guidning
├── README.md                    ← du läser den
├── experiments/
│   ├── breadth-test-001.md      ← 7 bilder, snitt 3.6/5
│   ├── prompt-iteration-001.md  ← uppstramad prompt → snitt 4.0/5
│   └── edit-flow-e2e-001.md     ← E2E-validering mot live API
└── test-images/                 ← lokala bilder (gitignored)
    └── breadth-001/
```

## Arbetsmetod — varför små vertikala slices

Varje slice ska:

1. **Testa en explicit hypotes** med klart success-kriterium
2. **Vara liten nog att bygga på 15–30 min**
3. **Logga resultat** i frontmatter-format (Hypothesis / Test / Success
   Criteria / Time Budget / Result)
4. **Respektera time budgets** — "15 min build, stopp vid 20" betyder
   att vi *inte* stoppar bara för att det ska *se* klart ut

Varför: prototyper är dyra att bygga klart. Vi vill veta så snabbt som
möjligt om hypotesen håller eller dör. Vad vi medvetet *inte* gör ännu:
databas, auth, deployment, persistent state, polerat UI, export. Det
kommer när vi har bevisat att kärnvärdet finns.

## Köra experiment

### Breadth-test

1. Lägg 10–12 bilder i `test-images/breadth-001/` med namnschema
   `B-XX-kort-beskrivning.jpg`
2. Starta appen med `ANTHROPIC_API_KEY` satt
3. Kör curl-loopen från [`experiments/breadth-test-001.md`](experiments/breadth-test-001.md)
   under sektionen *How to Run* — sparar JSON + latency per bild
4. Fyll i tabellen + summary i experimentloggen

### Prompt-iteration

1. Ändra `PROMPT` i `app.py`
2. Kör om samma bildset
3. Jämför mot tidigare körning
4. Skriv resultat i `experiments/prompt-iteration-NNN.md` enligt
   mönstret i [`prompt-iteration-001.md`](experiments/prompt-iteration-001.md)

## Nuvarande begränsningar (medvetna)

- **Ingen persistent lagring** — `SAVED` är in-memory, försvinner vid omstart
- **Ingen auth** — vem som helst på localhost kan POSTa
- **Inget export-format** — CSV/Excel väntar
- **Inget multibild-stöd** — en bild i taget, ingen merge/dedup
- **`confidence` visas inte i UI** — finns i rå JSON men inte i tabellen
- **Ingen Project / Location / Assessment / ReuseOption i kod** —
  domänmodellen är konceptuell, koden är platt (`items[]` direkt)
- **"Borde finnas"-hallucinationer kvar** — kräver few-shot examples
- **Material-feltolkning** (koppar → stål) — kunskaps-problem, inte promptbart

## Open questions

Det här är frågor vi *inte* har svar på än, och som styr vilka
experiment som är mest värda att köra:

| # | Fråga | Varför den är öppen |
|---|---|---|
| 1 | Hur fångar vi en lokal *tillräckligt bra* utan att det blir tungt? | En bild räcker inte för en hel lokal. 50 bilder är för mycket arbete. Vad är miniminivån? |
| 2 | Hur bedömer vi mängd/yta/volym på ett trovärdigt sätt? | AI:ns kvantitetsgissningar är osäkra. Krävs det laser, fotogrammetri, eller bara fler bilder? |
| 3 | Vad kräver mänsklig expertbedömning? | Är skick, lim, asbest-risk, säljbarhet sådant vi *aldrig* ska låta AI avgöra själv? |
| 4 | Vad är ett hinder vs en möjlighet? | Samma material kan vara båda beroende på projekt. Hur modellerar vi det? |
| 5 | Hur kopplas materialbank till nya ritningar? | DesignScenario är vag. Behöver vi CAD-import, eller räcker textbeskrivning som AI kan resonera om? |
| 6 | Vilken kvalitetsnivå krävs för att beslutsfattare ska *lita* på underlaget? | Snitt 4.0/5 i breadth-test är "användbart utkast" — räcker det för en återbruks-investeringsbeslut? |

## Next experiment

**Fältprov — en riktig lokal, 10–20 bilder, samlad inventering.**

### Syfte

Pröva om dagens flöde (bild → AI-utkast → korrigering → spara) håller
när det skalas från **enskilda bilder** till **en hel lokal**. Och —
viktigare — *vad som saknas* för att gå från bildanalys till
beslutsunderlag.

### Metod

1. **Välj lokal** — en riktig miljö (rivnings-/ROT-objekt, eget hem,
   kontor som ska byggas om). Det ska vara meningsfullt, inte en
   möblerad lägenhet utan ändringsplan.
2. **Tag 10–20 bilder** från samma lokal, grupperade per rum/zon:
   - Översiktsbilder per rum
   - Närbilder på material och fasta installationer
   - Detaljbilder på problematiska eller värdefulla element
3. **Kör varje bild** genom dagens `/analyze`
4. **Sammanställ manuellt** till en lokal-inventering (extern, t.ex.
   markdown eller kalkylark — vi har inte multi-bild i koden än)
5. **Notera per bild**: vad AI:n fick rätt, vad den missade, vad som
   var dubbelräknat mellan bilder, vad människan behövde lägga till
6. **Dokumentera bristerna** — vad gick från "bildanalys är OK" till
   "men det är inte beslutsunderlag ännu"?

### Vad vi vill lära oss

- **Hur bra blir summan?** Är 10 bilders inventering bättre eller sämre
  än 10 × en bilds — eller bara fragmenterad?
- **Var blir dedupliceringen ett problem?** Räknar AI:n samma soffa
  som syns i flera bilder två gånger?
- **Vilka frågor från [Problemet](#problemet) ovan kan vi börja besvara
  med det vi har?** Specifikt #2 (värde) och #3 (hinder/möjlighet) —
  syns något som hjälper människan att svara, eller är det helt off?
- **Vad är det första som behöver byggas?** Multi-bild merge?
  Assessment-fält? Project/Location-struktur? Vilket lager *blockerar*
  fältarbetet mest?

### Förväntat utfall

Sannolika lärdomar (att verifiera):

- AI:ns bildvis-analys håller — men sammanställningen blir grötig utan
  Project/Location/MaterialItem-struktur i koden
- Mängd-/yta-uppskattning är fortfarande svagaste länken
- Människan behöver lägga till värde- och hinder-omdömen (steg 4 i
  flödet) eftersom AI inte har den domänkunskapen ännu

Om detta håller — nästa slice efter fältprovet är troligen
**multi-image inventory merge** med minimal Location-struktur.

## Future experiments

Längre fram, ordning beslutas baserat på fältprovets utfall:

| # | Experiment | Vad vi vill veta |
|---|---|---|
| 1 | Multi-image inventory merge | Kan vi slå ihop 3–5 bilder av samma rum till en konsistent MaterialItem-lista? |
| 2 | Deduplicering mellan bilder | Räknar AI:n samma objekt två gånger om det syns i flera bilder? |
| 3 | Tidsmätning människa vs AI-assisted workflow | Är AI-utkastet *verkligen* snabbare än att skriva från noll? Med vilken kvalitetsförlust? |
| 4 | Few-shot mot "borde finnas"-bias | Kan exempel i prompten döda kylskåp- och taklampa-hallucinationerna? |
| 5 | Confidence-färgkodning i UI | Om vi visar `confidence` som radfärg/ikon — använder korrigeraren det? |
| 6 | Första Assessment-slice | Lägga till värde + hinder/möjlighet som redigerbara fält. Vad räcker som första MVP-fält? |
| 7 | Projekt/Location-struktur | Minimal hierarki: projekt → rum → bilder → items. När blir det viktigt? |
| 8 | DesignScenario-prototyp | Kan AI ge tre alternativa idéer för hur befintligt material kan användas i ny layout? |

## Konventioner

- **Commits**: Conventional commits (`feat:`, `test:`, `docs:`, `chore:`).
  Subject kort, body på svenska. Endast med uttrycklig "commit"-instruktion.
- **Branch-strategi**: Direkt på `main` så länge detta är solo-prototyp.
- **Experimentloggar**: Frontmatter med `status: planning / in-progress / confirmed / rejected`.
- **Time budgets respekteras** — stopp vid satt gräns oavsett om allt är klart.
- **Mock-fallback i `/analyze`** är *avsiktlig* — demon ska aldrig stanna
  vid saknad nyckel eller API-fel.

## Status

Projektet är i **prototypfas**. Hypotes-driven utveckling. Vi har
validerat **steg 1–3 i flödet** ("from local capture to reuse decision").
Steg 4–6 finns som domänmodell och arkitektur men är ännu inte byggda.
Nästa beslut sker baserat på utfall av kommande experiment, inte
roadmap-planering.

För Claude Code-specifik guidning (port-fällor, prompt-detaljer,
arbetsstil): se [`CLAUDE.md`](CLAUDE.md).
