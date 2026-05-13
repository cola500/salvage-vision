---
title: Field test candidate 001 — Hallvägen 21, plan 4 (Slakthusområdet)
description: Kandidat-utvärdering av en publik kontorslokalannons med planritning och 10 interiörbilder för nästa experiment (ritning + flera bilder + samlad inventering per rum)
category: dataset-evaluation
status: confirmed-as-candidate
last_updated: 2026-05-13
sections:
  - Källa
  - Varför denna kandidat
  - Vad vi laddade ner
  - Rum / zoner enligt planritningen
  - Föreslagen bild-till-zon-mapping
  - Material som sannolikt går att identifiera
  - Vad som sannolikt blir svårt
  - Reflektion — räcker datasetet?
---

# Field test candidate 001 — Hallvägen 21, plan 4

## Källa

| | |
|---|---|
| **Annons** | https://www.lokalguiden.se/lokal/hallvägen-21-söderort |
| **Adress** | Hallvägen 21, Slakthusområdet (Stockholm Söderort) |
| **Lokaltyp** | Kontor |
| **Yta** | ca 186 kvm, plan 4 |
| **Planritning** | PDF (1,3 MB) — separat fil |
| **Interiörbilder publicerade** | 12 st (varav 10 nedladdade) |
| **Bild-CDN** | `static.lokalguiden.se` — direkta URL:er, inga signaturer/expiry, ingen autentisering |

Annonsen är publik och bilderna serveras direkt utan watermarks från en
statisk CDN. **Inga signed URLs** noterades — länkarna förefaller stabila
över tid, men risk för att de byts om annonsen redigeras.

## Varför denna kandidat

Uppfyller kriterierna från instruktionen med god marginal:

| Kriterium | Status | Kommentar |
|---|---|---|
| Lokaltyp = kontor / butik / restaurang | ✓ | Kontor |
| Storlek 50–300 kvm | ✓ | 186 kvm — mitt i spannet |
| Planritning publikt tillgänglig | ✓ | PDF med namngivna zoner |
| 5–15 interiörbilder | ✓ | 12 i annonsen, 10 laddade |
| 2–6 rum/zoner | ✓ | 6 distinkta zoner |
| Olika material synliga | ✓ | terrazzo, trä, kakel, glas, betong, snickerier |
| Inte ett megaprojekt | ✓ | En våning, en hyresenhet |

Två extra fördelar utöver kriterierna:

- **Namngivna zoner i ritningen** (KONTOR, MÖTE, SAMTAL, PENTRY/PAUS, WC,
  HWC, STÄD, ENTRÉ). Gör verifieringen av bild-till-zon-mapping enkel.
- **Varierande materialspråk i bilderna**: terrazzogolv, ek/teaklister
  i snickerier, vit målning, mörkgrå köksluckor med vit kakelbakvägg,
  vit glas-blockvägg som rumsavdelare, träpanel i ett SAMTAL-rum.
  Det är realistisk material-bredd, inte ett enhetligt minimalistkontor.

## Vad vi laddade ner

Allt under `test-datasets/field-test-001/` (gitignored).

| Fil | Storlek | Källa |
|---|---|---|
| `planritning.pdf` | 1,3 MB | `customer/315/14a1c9a981df3445ae87d81fa083e6a4.pdf` |
| `img-01.jpg` – `img-10.jpg` | 3,0–4,5 MB var | `customer/315/<hash>.jpg` (10 av 12) |

Bilderna serveras i full upplösning (~3-5 MB per st), så datasetet är
~38 MB totalt. Filnamnen är sekventiella (01–10) — original-hash finns
inte kvar i filnamnet eftersom de inte är meningsfulla.

## Rum / zoner enligt planritningen

```
                       HWC   WC      KONTOR (öppet landskap
   STÄD   PENTRY/PAUS                med skrivbord-öar +
                                     ovalt konferenshörn)
            ENTRÉ
                       MÖTE          SAMTAL (höger)
   HISS                (stort
   (trapphus)          ovalt
                       8-sits)       SAMTAL (söder, runt)
```

8 zoner totalt:

1. **KONTOR** — öppet landskap (största ytan, ~50 % av lokalen)
2. **MÖTE** — stort ovalt mötesrum centralt
3. **SAMTAL (höger)** — litet samtalsrum med skrivbord/fåtölj
4. **SAMTAL (söder)** — litet samtalsrum med runt bord
5. **PENTRY/PAUS** — kök + matbord (4-sits)
6. **WC** + **HWC** — två toaletter, HWC med dusch
7. **STÄD** — förråd
8. **ENTRÉ** — entrézon innanför lokalens dörr

Plus de **gemensamma utrymmena utanför själva lokalen** (HISS, trapphus,
husets entré) — *viktigt*: två av tio bilder visar dessa, inte
hyresenheten.

## Föreslagen bild-till-zon-mapping

Detta är **min initialgissning utifrån bilderna** — ska verifieras i
själva experimentet, inte tas som facit.

| Bild | Mest sannolik zon | Innehåll i korthet |
|---|---|---|
| `img-01` | SAMTAL (söder?) + KONTOR-utkant | Två trädörrar (samtalsrum), grå fåtöljer, terrazzo + matta |
| `img-02` | **Utanför lokalen** — husets entré | Trädörr, hiss, spiraltrappa, terrazzo |
| `img-03` | SAMTAL (höger) + KONTOR | Glas-blockvägg, samtalsrum med skärm + fåtölj, whiteboard + kopiator i bakgrund |
| `img-04` | PENTRY/PAUS | Matbord (4-sits), mörkgrå köksluckor, vit kakelbakvägg |
| `img-05` | SAMTAL (söder?) — det med soffa | Träpanel-väggar, "hålkonst", grå soffa |
| `img-06` | PENTRY/PAUS (kafféhörn) | Vinglas-hänga, kaffemaskiner, parkett, fönster |
| `img-07` | ENTRÉ (in i lokalen) + HWC/WC-zon | Trädörr in, glas-blockvägg, kakelblock, KONTOR i bakgrund |
| `img-08` | PENTRY/PAUS (alternativ vinkel) | Samma kök som img-04 från annat håll |
| `img-09` | **Utanför lokalen** — trapphus | Spiraltrappa, fönster, gjutna trappsteg |
| `img-10` | KONTOR + SAMTAL (höger) | Loungehörn, glas-vägg in till SAMTAL, dörr till annan zon |

### Aggregerat per zon

| Zon | Antal bilder |
|---|---|
| KONTOR (öppet landskap) | 3–4 (delvis synligt) |
| MÖTE (stort centralt) | **0** — saknas helt |
| SAMTAL (totalt 2 rum) | 4 |
| PENTRY/PAUS | 3 |
| WC / HWC | **0** |
| STÄD | **0** |
| ENTRÉ (lokalens egen) | 1 (img-07) |
| Utanför lokalen (trapphus) | 2 (img-02, img-09) |

## Material som sannolikt går att identifiera

Sett över alla bilder, sannolika återbruks-relevanta material:

| Material / objekt | Bilder | Återbruksrelevans |
|---|---|---|
| Terrazzogolv (gjutet) | img-01, img-03, img-07 | Svår demonterbart men värdefullt |
| Heltäckningsmatta (kontorsmatta, grå) | img-01, img-05, img-10 | Förbrukningsmaterial — låg återbruksvärde |
| Parkett / trägolv | img-04, img-06 | Hög potential |
| Träportaler / -lister i ek/teak | img-01, img-03, img-04, img-07 | Hög potential |
| Glas-blockvägg (vit-glas) | img-03, img-07 | Specifikt — kan demonteras |
| Vit kakelbakvägg (pentry) | img-04, img-08 | Medel — beror på skick |
| Mörkgrå köksluckor (MDF/laminat) | img-04, img-08 | Medel |
| Träpanel-vägg (lodrät trä) | img-05 | Hög potential — distinkt material |
| Köksinstallation (blandare, ugn, micro, etc) | img-04, img-06, img-08 | Vit hushållsapparat-marknad |
| Möbler (fåtöljer, soffor, bord, stolar) | img-01, img-03, img-04, img-05, img-10 | Bra för återbruksmarknad |
| Armaturer (taklampor, spotlights) | flera | Lågmedel — beror på modell |
| Whiteboard, kopiator, skärmar | img-03 | Lös inventarie — säljbart |

## Vad som sannolikt blir svårt

1. **MÖTE saknas helt i bildurvalet.** Lokalens största inneslutna rum
   har ingen bild. Det är ett tydligt gap — och en lärdom om att
   annonsbilder typiskt visar de "vackra" zonerna (pentry, lounge), inte
   funktionella rum (möte, WC, förråd).

2. **Inga bilder av WC/HWC eller STÄD.** Lokal-totalen kan inte
   bedömas utifrån endast detta dataset. Samma annons-bias som ovan.

3. **2 av 10 bilder ligger utanför själva lokalen** (trapphus, entré).
   AI:n kommer förmodligen inte veta att img-02 och img-09 inte är
   hyresenhetens material. Det är ett intressant test: kan vi
   *manuellt* filtrera bort dem före AI-analys, och om inte — hur fel
   blir den samlade inventeringen?

4. **Överlappande bilder.** img-04 och img-08 är båda PENTRY/PAUS från
   olika vinklar. Båda visar samma matbord, samma kök. Detta är ett
   bra testfall för **deduplicering**: en framtida AI-pipeline måste
   inte räkna samma matbord två gånger.

5. **Möbler vs fasta installationer.** Hyresgästen kommer troligen ta
   med sig möbler. Vad räknas som "lokalens material" och vad är lös
   inventarie? Annonser markerar inte detta — det är en domänfråga som
   AI:n inte kan svara på utan kontext.

6. **Rumsidentifiering från bild ensam är svårt.** SAMTAL-rummen är
   distinkta från KONTOR (slutna med dörr), men *vilket* av de två
   SAMTAL-rummen en bild visar går knappast att avgöra utan ritningen.

## Reflektion — räcker datasetet?

### Räcker det för **nästa experiment**?

**Ja, för det vi vill testa just nu** (ritning + flera bilder + samlad
inventering per rum). Vi har:

- En tydlig ritning med namngivna zoner — referens vid utvärdering
- Tillräckligt med bilder för att gruppera (10 st över ~5 zoner)
- Realistiska material och möbelmix
- Faktiska gap (MÖTE, WC, STÄD saknas) som är **realistiska** —
  så ser annonser ut

Att MÖTE saknas är inte ett brott — det är *datapunkten*: i en
verklig användarsituation kommer användaren ofta ha ojämn täckning
av lokalen.

### Vad saknas i datasetet?

- **Närbilder på material.** Annonsfotografer tar översiktsbilder.
  Vi vet från breadth-test-001 att AI:n hanterar närbilder svagare
  än rumsöversikter — men vi har inga närbilder här att testa.
- **Mått och kontext.** Ritningen har en skalstreck (0–3 m) men
  AI:n får ingen meta-information om bilderna (vilken zon, vilken
  vinkel). Det är *bra* eftersom det matchar verklig användning,
  men gör utvärderingen svårare.
- **Användarens kommentarer.** I en verklig session skulle
  besökaren säga "den här bilden är från mötesrummet". Vi måste
  simulera den input manuellt under utvärderingen.

### Behöver vi ett riktigt fältprov i fysisk lokal senare?

**Ja — men inte ännu.** Detta dataset räcker för att testa:

1. Om AI:n kan producera ett bildvis-inventeringsutkast (vi har redan
   visat det)
2. Om en användare kan **gruppera bilder per zon** med ritningen som
   referens
3. Om vi kan sammanställa en **lokal-total inventering** från 10
   bilder (manuellt — vi har inte multi-bild-merge i koden)
4. Var den manuella aggregeringen blir grötig och vad som behöver
   automatiseras (dedup, zon-aggregering, sammanslagning)

En fysisk lokal behövs senare för:

- **Närbilder och mått** (mängd-kalibrering)
- **Skick-bedömning** (foton ljuger om slitage)
- **Material under ytan** (vad finns bakom innerväggen?)
- **Tidsmätning människa vs AI-assisted** med riktig användare
- **Hinder/möjlighet-bedömning** med kontext från projektet

Men det blir **nästa-nästa-experiment**, efter att vi sett vad detta
dataset säger om grupperings- och aggregeringsproblemet.

### Sannolika lärdomar från experimentet

- AI hanterar enskilda bilder OK, men summan av 10 bilder blir
  fragmenterad utan struktur (vi har inte Location/MaterialItem-modell
  i koden)
- Deduplicering är ett *större* problem än vi anade (img-04 + img-08
  pentry; img-03 + img-10 samma SAMTAL-rum från olika håll)
- Bildurvalets bias (annonsbilder = "vackra zoner") betyder att
  fältdata kommer ha **systematiska luckor** även när användaren
  tycker hen "tog bilder överallt"
- Det stora MÖTE-rummet är ironiskt nog det mest centrala — och vi
  har ingen bild. Argument för att fältarbete med checklista per zon
  är värdefullt
