---
title: Breadth test 001 — bildanalysens räckvidd över 12 miljöer
description: Mäta hit/miss-rate och användbarhet av AI-inventering på 10–12 olika bildtyper
category: ux-validation
status: planning
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

Fyll i efter att analysen körts. En rad per bild. Användbarhet 1–5 där:
- **5** = direkt användbar med små korrigeringar
- **4** = bra startpunkt, någon halvtimmes korrigering räcker
- **3** = bättre än tomt formulär men kräver omarbete
- **2** = mest brus, ärligare att börja från noll
- **1** = vilseledande, riskerar göra slutresultatet sämre

| ID | Miljö | Lat (s) | Identifierade material (kort) | Missar | Hallucinationer | Användb. | Kommentar |
|---|---|---|---|---|---|---|---|
| B-01 | Kök / pentry |  |  |  |  | /5 |  |
| B-02 | Tegelvägg |  |  |  |  | /5 |  |
| B-03 | Kontorsrum |  |  |  |  | /5 |  |
| B-04 | Glaspartier |  |  |  |  | /5 |  |
| B-05 | Dörrar (rad) |  |  |  |  | /5 |  |
| B-06 | Undertak + arm. |  |  |  |  | /5 |  |
| B-07 | Träpanel / parkett |  |  |  |  | /5 |  |
| B-08 | Badrum / våtrum |  |  |  |  | /5 |  |
| B-09 | Rörig lokal |  |  |  |  | /5 |  |
| B-10 | Dåligt ljus |  |  |  |  | /5 |  |
| B-11 | Blandade material |  |  |  |  | /5 |  |
| B-12 | Närbild material |  |  |  |  | /5 |  |

Rå JSON per bild finns under `test-images/breadth-001/results/B-XX.json`.

## Summary

Fyll i efter att tabellen är klar.

### Vad fungerade bäst?

_(t.ex. "B-01, B-07, B-08 fick 5/5 — välbelysta miljöer med distinkta objekt")_

### Vad fungerade sämst?

_(t.ex. "B-10 och B-12 fick 1–2/5 — AI:n hallucinerade material som inte syns")_

### Vilka material/objekt verkar svåra?

_(materialgrupper, inte enskilda bilder — t.ex. "glas-kvantifiering", "räkna identiska dörrar", "akustikplattor vs gips")_

### Genomsnittlig latency

_(median + max — relevant för hypotesens 30s-tröskel)_

### Hallucinationsmönster

_(systematiska fel? T.ex. "AI:n gissar alltid 'ek' på trä även när det är furu")_

### Är hypotesen fortfarande stark?

_(Konfidens: stark / svag / kollapsad. Motivera kort.)_

## Decision

### Nästa minsta slice — kandidater

Välj **en** efter resultaten:

1. **Redigerbar tabell** — om bredden är OK och nästa friction är att korrigera AI:ns output. Liten frontend-slice, ingen backend-ändring.
2. **CSV-export** — om användbarheten är genomgående hög nog att data faktiskt ska användas vidare.
3. **Riktad prompt-iteration** — om vi ser systematiska missar som en bättre prompt kan fixa. Billigast om det funkar.
4. **Multibild per analys** — om svagheten är att en bild aldrig fångar hela rummet. Större förändring.
5. **Stoppa här** — om hypotesen kollapsar för flera kategorier är det möjligen fel produkt.

_Decision: TBD_

## Time Budget

- Foto/källsamling: 20 min
- Köra 12 analyser: 15 min (estimat: ~10s per bild × 12 + overhead)
- Fylla i tabellen: 30 min
- Summary + decision: 15 min

**Total: ~80 min. Stopp vid 2 h oavsett.**
