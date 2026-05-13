---
title: Breadth test 001 — bildanalysens räckvidd över 12 miljöer
description: Mäta hit/miss-rate och användbarhet av AI-inventering på 10–12 olika bildtyper
category: ux-validation
status: confirmed
last_updated: 2026-05-13
sections: [Hypothesis, Test Set, How to Run, Results, Summary, Decision]
---

# Breadth test 001 — bildanalysens räckvidd över 12 miljöer

## Hypothesis

Den bekräftade hypotesen i [HYPOTHESIS.md](../HYPOTHESIS.md) testade ett enskilt scenario. Här breddtestar vi:

> **Claude vision ger ett användbart inventeringsutkast (≥3/5) på majoriteten av rimliga bildtyper en användare faktiskt skickar in — inklusive svåra fall som dåligt ljus, röriga lokaler och närbilder på material.**

Förväntat utfall (hypotes före data):
- **Starkt** på: kök, dörrar, träpanel, glaspartier (tydliga, välkända objekt)
- **Medel** på: tegelvägg, kontor, badrum, undertak (kräver materialigenkänning)
- **Svagt** på: dåligt ljus, rörig lokal, närbild (kontextfattigt)

Det vi vill veta är var brytpunkten ligger och om de svaga fallen ändå är "korrigerbara" (= bättre än tomt formulär).

## Test Set

12 kategorier, 1 bild per kategori. ID `B-01` till `B-12`.

| ID | Kategori | Varför vi testar | Bildkälla — förslag |
|---|---|---|---|
| B-01 | Kök / pentry | Baseline, många distinkta objekt | Eget foto, eller Wikimedia "kitchen interior" |
| B-02 | Tegelvägg | Bedömer rätt mängd kvm? | Eget foto av rivningsvägg, eller Wikimedia "brick wall interior" |
| B-03 | Kontorsrum | Möbler + golv + tak samtidigt | Eget foto, eller Unsplash "open office" |
| B-04 | Glaspartier | Glas är notoriskt svårt att kvantifiera | Eget foto av kontorsskärm/dörr i glas |
| B-05 | Dörrar (rad) | Räknar AI:n rätt antal? | Eget foto av korridor med dörrar |
| B-06 | Undertak + armaturer | Akustikplattor + lysrör — typiskt ROT-material | Eget foto, undertak i kontor |
| B-07 | Träpanel / parkett | Materialigenkänning (ek vs furu vs lamell) | Eget foto eller Wikimedia "parquet floor" |
| B-08 | Badrum / våtrum | Kakel + porslin + blandare blandade | Eget foto, eller Wikimedia "bathroom interior" |
| B-09 | Rörig lokal | Halvtömd, kartonger, möbler huller om buller | Eget foto från riv- eller flyttobjekt |
| B-10 | Dåligt ljus | Underexponerat, kvällsljus | Eget foto, ta medvetet utan blixt |
| B-11 | Blandade material | Tegel + trä + metall i samma bild | Eget foto av t.ex. industrilokal |
| B-12 | Närbild på material | Bara textur, ingen kontext | Eget foto, fyll bildrutan med ett material |

### Bildkällor — rekommendation

**Egna foton är att föredra** för B-02, B-05, B-06, B-09, B-10, B-11. Verklig återbruksinventering sker i halvrivna, dammiga, dåligt belysta miljöer — stockbilder är systematiskt för proffsiga och underskattar svårighetsgraden.

**Stockbilder funkar** för B-01, B-03, B-07, B-08 om du vill snabba upp testet. Wikimedia Commons (CC-licens) är säkrast för commit. Unsplash/Pexels är OK med kreditering.

**Inga bilder här ännu.** Jag har inte laddat ner stockbilder eftersom (a) du sa "max 12, ladda inte ner stora mängder" och (b) hypotesen testas bättre med dina egna foton. Säg till om du vill att jag fetchar några specifika.

### Filnamnskonvention

`B-XX-kort-beskrivning.jpg` — t.ex. `B-01-kok-villa.jpg`, `B-09-rorig-kontorslokal.jpg`. Underlättar matching mot tabellen nedan.

## How to Run

Förutsätter att appen körs (`uv run app.py` med `ANTHROPIC_API_KEY` satt) på port 5050.

Kör alla bilder i mappen och spara JSON + latency per bild:

```sh
mkdir -p test-images/breadth-001/results
for f in test-images/breadth-001/B-*.{jpg,jpeg,png,JPG,JPEG,PNG}; do
  [ -f "$f" ] || continue
  name=$(basename "$f")
  base="${name%.*}"
  echo "=== $name ==="
  curl -s -F "image=@$f" \
       -w "\n--- latency: %{time_total}s ---\n" \
       -o "test-images/breadth-001/results/${base}.json" \
       http://localhost:5050/analyze \
    | tee "test-images/breadth-001/results/${base}.latency.txt"
  python3 -m json.tool "test-images/breadth-001/results/${base}.json" | head -40
  echo
done
```

Latency-rad sparas separat i `.latency.txt` så du kan klippa in värdet i tabellen utan att fippla i terminalen.

## Results

Kört 2026-05-13 med `claude-sonnet-4-6`. **7 av planerade 12 bilder** — användaren prioriterade kök, badrum, vardagsrum, eldstad och närbilder. Kontor, dörrar, undertak och dåligt ljus utelämnades.

Användbarhet 1–5 där:
- **5** = direkt användbar med små korrigeringar
- **4** = bra startpunkt, någon halvtimmes korrigering räcker
- **3** = bättre än tomt formulär men kräver omarbete
- **2** = mest brus, ärligare att börja från noll
- **1** = vilseledande, riskerar göra slutresultatet sämre

| ID | Miljö | Lat (s) | Identifierade material (kort) | Missar | Hallucinationer | Användb. | Kommentar |
|---|---|---|---|---|---|---|---|
| B-01 | Kök (rörig bänk) | 8.5 | Vita skåp/lådor, mörk bänkskiva, schackrutigt golv, vit kakelvägg, handtag (~10 st) | Espressomaskin, skärbräda, fönster | **Kylskåp** (finns inte i bild); möjligen "överskåp" som inte syns | 3/5 | Får fasta installationerna rätt, men hittar på ett kylskåp och kakel-area är osäker |
| B-02 | Kök (skåp + ugn + micro) | 7.9 | Samsung ugn, Samsung micro, vita högskåp, lådor, svart fällstol, schackrutigt golv | Inget viktigt | Inga | **5/5** | Imponerande — märkeskänner Samsung-produkterna. Distinkta objekt + god belysning = bästa läget |
| B-03 | Badrum / dusch | 7.7 | Toalett, glasduschvägg, duschsystem (stång+blandare+handdusch), vit storformatskakel, brun mosaik (golv+bakvägg!) | Vägghängd korg (mindre relevant) | Inga | **5/5** | Bästa observationen i hela testet — noterar att mosaiken finns både på golv och bakvägg i dusch |
| B-04 | Vardagsrum (parkett, möbler, fönster) | 11.0 | Ekparkett **fiskbensmönster** (~20 kvm), sideboard, bokhylla, gardiner, tavla | Soffan, plantan i kruka, fönsterglas | **"Hängande taklampa i rotting/bambu"** — det är en rottingstol, inte en lampa | 3/5 | Får parketten med mönsterdetalj rätt, men förväxlar rottingstol med taklampa. Visar bias mot att lista en "lampa" |
| B-05 | Öppen spis + dekoration | 8.9 | Mässingskandelabrar, björkved, läderpuff, tegelinfodring, vit målad spiselkrans, gnistskydd | Svart förvaringsskåp ovan, parkett | **Intern motsägelse**: listar både "natursten/skiffer spiselkrans" och "Trä/MDF spiselkransram målad vit" för samma objekt | 3.5/5 | Hyfsat på lösa föremål, fastnar på två motstridiga rader för samma spiselkrans |
| B-06 | Närbild parkettgolv | 6.7 | Ekparkett (~1 kvm faktiskt synlig) | — | **Extrapolerar till "15–20 kvm"** trots att bara golvyta i närbild syns. **Hittar på "betong undergolv"** som inte kan ses. Listar "lack/finish" som separat post med samma 15–20 kvm = dubbelräkning | 2.5/5 | Sämsta resultatet. Närbild → AI gissar hela rummets storlek. Klassisk närbildsfalla |
| B-07 | Närbild tegel + eldstad | 6.8 | Eldstadstegel (~40–50 st räknade), kalkbruksfog, ved i eldstaden | Vitmålad sockel | "Stål/gjutjärn rökkanal" — den böjda metalldelen ser ut som **koppar/patinerad bronsplåt**, inte stål. "Betonghäll lintel" — osäkert om det är överliggare eller bara annan tegelrad | 3.5/5 | Tegelräkning förvånansvärt bra. Metallmaterial fel — kan vara ett mönster på patinerad metall |

Rå JSON per bild finns under `test-images/breadth-001/results/B-XX-*.json`.

### Latency-statistik

- **Min**: 6.7 s (B-06, närbild)
- **Median**: 7.9 s
- **Max**: 11.0 s (B-04, många objekt)
- **Genomsnitt**: 8.2 s
- **Alla 7 < 30 s tröskeln** ✓

### Användbarhetsfördelning

- **5/5**: 2 (B-02, B-03 — välbelysta fasta installationer)
- **3.5/5**: 2 (B-05, B-07)
- **3/5**: 2 (B-01, B-04)
- **2.5/5**: 1 (B-06 närbild)
- **Snitt**: **3.6/5**
- **Andel ≥ 3**: 6/7 (86 %)

## Summary

### Vad fungerade bäst?

**B-02 (kök med inbyggnadsugnar) och B-03 (badrum) — båda 5/5.** Gemensamt: välbelyst miljö, fasta installationer med tydliga konturer, distinkta material. B-03 noterade till och med att mosaiken används både som golv och som bakvägg i duschen — en observation som visar genuin scenförståelse, inte bara objektigenkänning.

Materialkategorier som AI:n hanterar väl:
- **Vit slätbehandlat snickeri** (kökslådor, högskåp)
- **Stora kakelytor** (väggkakel, golvklinker)
- **Klassisk parkett** — identifierar både material (ek) och mönster (fiskben)
- **Märkesvaror med synlig logo** (Samsung-produkterna)

### Vad fungerade sämst?

**B-06 (närbild parkettgolv) — 2.5/5.** Hela utan-kontext-närbildens problem på en bild: AI:n gissade 15–20 kvm trots att bara ~1 kvm syns, hittade på ett "betong undergolv" som inte kan ses, och dubbelräknade golvet som både "parkett" och "lack/finish".

### Vilka material/objekt verkar svåra?

1. **Metaller** — koppar/brons (B-07) feltolkat som stål/gjutjärn. Patinerad metall är troligen ett återkommande systemfel.
2. **Kvantifiering från närbild** (B-06) — AI:n vägrar svara "okänt", extrapolerar i stället till hela rummet.
3. **Objekt vs lampa-bias** (B-04) — rottingstol blev "hängande taklampa i rotting". Verkar finnas en bias att alltid lista en taklampa när det finns rotting i bilden.
4. **Närbilds-kontext** (B-06, B-07) — överliggare/lintel-gissning i B-07 är vag eftersom det inte går att se vad som är konstruktion och vad som är annan tegelrad.

### Genomsnittlig latency

**Median 7.9 s, max 11.0 s, snitt 8.2 s.** Hela testet långt under 30 s-tröskeln. Marginalen finns och 30 s håller även om en bild skulle ta 2–3× snittet.

### Hallucinationsmönster

Tre tydliga mönster — alla värda att försöka adressera i prompten:

1. **"Komplettera scenen"** — AI:n lägger till saker som "borde" finnas:
   - B-01: kylskåp som inte syns
   - B-04: taklampa (förväxlar rottingstol)
   - B-06: betong undergolv
2. **Dubbelräkning av samma yta** — B-06 listar både "parkett 15–20 kvm" och "ytbehandlat trägolv 15–20 kvm" som separata poster. B-05 har samma problem med spiselkransen (skiffer vs MDF för samma föremål).
3. **Extrapolation från fragment** — närbildens svaghet (B-06). AI:n gissar hela rummet i stället för att rapportera "närbild, kan ej bedöma yta".

### Är hypotesen fortfarande stark?

**Stark — med en tydlig nyans.**

- ✓ 7/7 körningar lyckades och returnerade strukturerad JSON
- ✓ 6/7 ≥ 3/5 användbarhet — bättre än tomt formulär
- ✓ Latency med god marginal under 30 s
- ✓ Material- och objektigenkänning är dugligt nog att vara en startpunkt

**Nyansen**: Den ursprungliga hypotesens "användbar startpunkt" gäller, men **kvantitetsangivelserna är hypotesens svaga punkt**. AI:n är trygg på vad något *är*, mindre trygg på *hur mycket*. För återbruksinventering där kvantitet driver CO₂-beräkning och försäljningsvärde är det inte trivialt.

## Decision

### Nästa minsta slice — rekommendation

**Förslag: Riktad prompt-iteration (kandidat 3) som första slice — billigast och adresserar de tre största observerade felmönstren direkt.**

Konkreta promptregler att testa:

1. *"Lista bara material och objekt som faktiskt syns i bilden. Lägg inte till föremål för att 'komplettera' rummet."* → adresserar kylskåps-hallucinationen (B-01) och betong-undergolv (B-06).
2. *"Om bilden är en närbild eller fragment, ange kvantitet endast för det som syns. Skriv 'närbild — kvantitet kan ej bedömas' i quantity-fältet om hela ytan inte är synlig."* → adresserar B-06.
3. *"Dela inte upp samma yta i flera poster. Ett golv är en post, inte 'parkett + lack + undergolv'."* → adresserar dubbelräkning.

Nästa slice efter prompt-iterationen (ordning):

1. **Redigerbar tabell** — efter prompt-iteration vet vi vilken kvarvarande felgrad användaren behöver korrigera. Om snittet ligger kvar runt 3.6/5 är celledit den naturliga next slice.
2. **Multibild per analys** — först om vi ser att enskilda bilder systematiskt missar saker som syns i sidobilder.
3. **CSV-export** — först när användbarheten är stabilt ≥ 4/5 och det finns ett mottagarsystem.

### Kvarvarande osäkerhet — gap från detta test

Testet täckte 7/12 planerade kategorier. Innan vi går vidare i produktriktning, fundera på om följande är värda att testa i `breadth-test-002`:

- **Dåligt ljus** (kvällsbelysning, motljus) — det realistiska ROT-scenariot
- **Undertak + armaturer** — vanligaste ROT-fyndet i kommersiella lokaler
- **Dörrar i rad** — för att se om AI:n räknar identiska objekt korrekt
- **Riktigt rörig miljö** (kartonger, halvtömt, möbler på varandra) — B-04 var en variation men inte extrem

Om prompt-iterationen löser kvantifieringsproblemen kan dessa förmodligen vänta.

_Decision: **Prompt-iteration först** (15–20 min slice), därefter beslut om redigerbar tabell baserat på utfall._

## Time Budget

- Foto/källsamling: 20 min
- Köra 12 analyser: 15 min (estimat: ~10s per bild × 12 + overhead)
- Fylla i tabellen: 30 min
- Summary + decision: 15 min

**Total: ~80 min. Stopp vid 2 h oavsett.**
