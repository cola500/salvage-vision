---
title: Prompt iteration 001 — restriktiv prompt mot tre felmönster
description: Mäta om uppstramad prompt minskar hallucinationer, dubbelräkning och kvantitetsextrapolation utan att försämra de starka bilderna
category: prompt-engineering
status: confirmed
last_updated: 2026-05-13
sections: [Hypothesis, Changes, Method, Results, Summary, Decision]
---

# Prompt iteration 001 — restriktiv prompt mot tre felmönster

## Hypothesis

> En mer restriktiv prompt minskar hallucinationer (regel A), dubbelräkning (regel C) och felaktig kvantifiering från närbild (regel B), utan att försämra användbarheten på de starka bilderna (B-02, B-03).

Förväntat utfall före data:
- **B-01** (kylskåp-hallucination) — försvinner med regel A
- **B-04** (rottingstol → taklampa) — försvinner med regel A
- **B-05** (motstridig spiselkrans) — försvinner med regel C
- **B-06** (extrapolerad kvm + undergolv) — kraftigt förbättrad av regel B + A
- **B-02, B-03** (5/5) — bör hålla samma nivå; risken är att prompten gör AI:n mer återhållsam och tappar 1–2 plausibla poster
- **B-07** (koppar feltolkat som stål) — osäkert; det är ett kunskapsfel snarare än ett scen-fel

## Changes

Ändrade endast `PROMPT` i `app.py`. Inget annat. UI:t visar fortfarande bara
de fyra ursprungliga fälten (material, object, quantity, reuse_potential) —
det nya `confidence`-fältet hamnar i rå JSON men renderas inte i tabellen.

Diff i sammandrag:
- Lade till 4 numrerade regler (Synlighet, Närbild, Dubbelräkning, Osäkerhet)
- Lade till `confidence: "low" | "medium" | "high"` i schemat
- Tonade ner "var konkret i mängd" — den gäller nu *när bilden tillåter*
- Tillät "färre om bara få syns" i stället för strikt 3–8

## Method

1. Stoppa ev. tidigare app-instans
2. Starta appen med samma `ANTHROPIC_API_KEY` (samma modell: `claude-sonnet-4-6`)
3. Kör samma 7 bilder från `test-images/breadth-001/`
4. Spara nya resultat i `test-images/breadth-001/results-v2/`
5. Jämför mot v1-resultaten i `test-images/breadth-001/results/`
6. Bedöm efter samma kriterier som breadth-test-001:
   - hallucinationer (objekt som inte syns)
   - dubbelräkning (samma yta listad flera gånger)
   - kvantitetsfel (extrapolerat från fragment, orimliga m²)
   - användbarhet 1–5

## Results

Kört 2026-05-13. Rå JSON i `test-images/breadth-001/results-v2/`.

### Per bild (före → efter)

| ID | Miljö | Användb. v1 | Användb. v2 | Hallucinationer (före → efter) | Dubbelräkning (före → efter) | Kvantitetsfel (före → efter) | Kommentar |
|---|---|---|---|---|---|---|---|
| B-01 | Kök (rörig bänk) | 3 | **3.5** | Kylskåp (—) → Kylskåp **kvar med "high" confidence** | "Vit kakelvägg" → borttagen ✓ | Bänkskiva: "3 löpmeter" → "2–3 löpmeter **synligt**" ✓; golv: "ca 8 kvm" → "synlig yta ca 4–6 kvm" ✓ | Synlighetsregeln tog bort kakelvägg, men det envisa "borde finnas ett kylskåp" sitter kvar — och nu med **felaktigt hög confidence** |
| B-02 | Kök (ugnar + skåp) | 5 | **5** | Inga → inga ✓ | Inga → inga ✓ | Inga → bättre kvantifierad ("synligt"/"kan ej bedömas exakt") ✓ | Behöll det starka resultatet, mer hedgade kvantiteter — ingen försämring |
| B-03 | Badrum / dusch | 5 | **4.5** | Inga → inga ✓ | Inga → inga ✓ | Kvm: precis → "kan ej bedömas exakt" ✓ | Tappade detaljen "mosaik finns även som bakvägg i dusch" och handduk-posten — *liten* regression i observationsnoggrannhet |
| B-04 | Vardagsrum | 3 | **3** | "Rotting-taklampa" → **kvar med "high" confidence**. Ny: "Högt brunt skåp" (osäkert om syns) | Inga → inga | Parkett: "20 kvm" → "20–25 kvm synligt" ✓ | Försvann: gardiner, rosa pall. "Borde finnas en taklampa när det finns rotting" — samma misstag som B-01 |
| B-05 | Öppen spis | 3.5 | **4** | — | **Motstridig spiselkrans löst** — nu en post: "vit puts/målad MDF inkl. svart stenskiva (marmor eller skiffer, osäkert)" ✓ | Tegelyta: "1,2 kvm" → "ca 0,4 kvm synlig tegelyta" ✓ | **Regel C funkade exakt som tänkt.** Osäkerhet skrivs i samma post i stället för två motstridiga rader |
| B-06 | Närbild parkett | 2.5 | **4.5** | "Betong undergolv" → **borttagen** ✓ | "Parkett" + "lack/finish" + "undergolv" som tre poster → **en post** ✓ | "15–20 kvm" → **"kan ej bedömas från närbild – synlig yta ca 3–4 kvm"** ✓ | **Regel B funkade perfekt.** Från 5 fabricerade poster till en ärlig observation. Största vinsten i hela testet |
| B-07 | Närbild tegel | 3.5 | **3.5** | Lintel "natursten/betonghäll" → kvar men nu med "low" confidence ✓ | Inga → inga | Tegelräkning: "40–50 st" → "kan ej bedömas från närbild" ✓ | Metallhuven kallas fortfarande "stål/gjutjärn" trots att den är **koppar/patinerad brons**. Promptändring kan inte fixa material-felkänning |

### Aggregerad jämförelse

| Mått | v1 (original prompt) | v2 (uppstramad prompt) | Δ |
|---|---|---|---|
| Snittanvändbarhet | 3.6 / 5 | **4.0 / 5** | **+0.4** |
| Andel ≥ 4/5 | 2 / 7 (29 %) | 4 / 7 (57 %) | +28 pp |
| Andel < 3/5 | 1 / 7 (14 %) | 0 / 7 (0 %) | -14 pp |
| Snitt latency | 8.2 s | **9.6 s** | +1.4 s (fortfarande långt under 30 s) |
| Min latency | 6.7 s | 4.0 s (B-06 — färre poster) | -2.7 s |
| Max latency | 11.0 s | 12.4 s | +1.4 s |
| Hallucinerade objekt — totalt | 4 | 2 | -50 % |
| Dubbelräknade ytor — totalt | 3 | 0 | **-100 %** |
| Närbild-extrapolation | 2 av 2 bilder drabbade | 0 av 2 | **eliminerat** |

### Confidence-fältet — observation

AI:n använder `confidence` konsekvent: "high" på fasta installationer, "medium" på material-osäkerhet, "low" på vaga tolkningar (lintel i B-07). **Men**: de kvarvarande hallucinationerna (kylskåp B-01, taklampa B-04) markeras **felaktigt med "high" confidence**. Confidence är alltså inte en pålitlig hallucinationsindikator i sin nuvarande form — modellen "tror på" sina egna kompletteringar lika starkt som faktiska observationer.

## Summary

### Blev hallucinationerna färre?

**Ja, halverat** (4 → 2). Regel A tog bort fyra fall:
- Vit kakelvägg (B-01)
- "Lampa" hallucination i B-01 (försvann tyst)
- Pall rosa (B-04 — gränsfall)
- "Betong undergolv" (B-06)

**Två kvarstår** med envis "high confidence":
- Kylskåp i B-01
- Rotting-taklampa i B-04

Båda följer samma mönster: AI:n verkar **tolka en svår-att-se-sak som det objekt som "brukar" finnas där**. Kylskåp som en otydlig vit yta i bakgrunden, taklampa som ett rotting-objekt (egentligen en stol). Det är inte ren hallucination — det är feltolkning som AI:n inte själv kan flagga eftersom den "ser" objektet med hög konfidens.

### Blev kvantifieringen bättre?

**Ja, dramatiskt.** Tre tydliga vinster:
1. **Närbilder fixade** (B-06 från 15–20 kvm-gissning till "kan ej bedömas").
2. **"Synligt"-hedging** används konsekvent på alla bilder ("synlig yta ca 4–6 kvm", "ca 0,4 kvm synlig tegelyta").
3. **Inga dubbelräknade ytor** (0 fall mot 3 i v1).

### Blev något sämre?

**Två små regressions:**
- B-03 tappade observationen att mosaiken finns även som bakvägg i duschen — möjligen en bieffekt av "färre poster om bara få syns".
- B-04 tappade gardinerna (faktiskt synliga) — samma trolighet, AI:n blev *för* återhållsam.

Båda är acceptabla — användaren kan lägga till en saknad post snabbare än hen kan ta bort en hallucinerad.

Snitt-latency ökade marginellt (8.2 → 9.6 s) eftersom prompten är längre och svaren mer ordrika. Fortfarande långt under 30 s.

### Snittbetyg

**3.6 → 4.0 av 5 (+11 % relativt).** Spridningen krympte också — nu ingen bild under 3/5 (v1 hade B-06 på 2.5).

### Är hypotesen bekräftad?

**Ja.** En restriktiv prompt minskar tre av de fyra observerade felkategorierna (hallucinationer, dubbelräkning, kvantitetsextrapolation). Den fjärde — **material-feltolkning** (koppar → stål, B-07) — är ett kunskaps-/visuellt feature-problem som inte kan lösas genom prompt-engineering.

## Decision

### Är nästa slice fortfarande redigerbar tabell?

**Ja — gå vidare till redigerbar tabell.**

Argument:
- Snittet är nu 4.0/5. De flesta poster är *korrekta* — den naturliga friction-punkten är *korrigering*, inte *generering*.
- De två kvarvarande hallucinationerna (kylskåp, taklampa) markeras med "high" confidence — det är hardcoded "borde finnas"-priors som modellen inte själv kan slå av. Ytterligare promptregler skulle ha avtagande avkastning och riskerar att AI:n blir så återhållsam att den missar saker som faktiskt syns (jfr regressionerna i B-03, B-04).
- Redigerbar tabell ger oss data på *vilka* fel användaren faktiskt korrigerar — vilket är bättre underlag för nästa promptiteration än fler manuella jämförelser.

### Behöver prompten itereras en gång till?

**Inte just nu.** Men spara följande som backlog för `prompt-iteration-002` *efter* redigerbar tabell ger oss riktig användardata:

- Få-shot exempel på vad som *inte* ska listas (kylskåp som "borde finnas", rotting-taklampa när det är rotting-stol). Few-shot kan adressera "borde finnas"-bias som textbaserade regler inte räcker till för.
- Material-osäkerhet på metaller (koppar/brons/patinerad stål är notoriskt svårt) — be AI:n explicit ange "metall, exakt typ osäker" som default i stället för att gissa.

### Confidence-fältet — vad gör vi med det?

UI:t renderar det inte i dagsläget. Förslag: **låt det vara i rå JSON tills redigerbar tabell byggs**, då kan vi visa det som en färgad indikator (eller filter "visa bara high-confidence"). Det är användbar signal — *när vi har en plats att visa den*.

### Konkret rekommendation

1. **Granska prompt-ändringen** i `app.py` och experimentloggen.
2. Om OK: commit prompt-iteration-001.
3. Nästa slice: redigerbar tabell (klick i cell → ändra → spara tillbaka). Liten frontend-slice, ingen backend-ändring.

