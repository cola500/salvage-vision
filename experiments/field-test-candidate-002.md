---
title: Field test candidate 002 — Wagnshuset, Hufvudsta Gård (Solna)
description: Kandidat-utvärdering av en publik kontorsannons från 1825-byggnad — kvalitativt bättre material men kvantitativt sämre bildurval än field-test-001
category: dataset-evaluation
status: rejected-as-primary
last_updated: 2026-05-13
sections:
  - Källa
  - Vad vi laddade ner
  - Granskning av bildurvalet
  - Rum / zoner enligt planritningen
  - Föreslagen bild-till-zon-mapping
  - Material som sannolikt går att identifiera
  - Jämförelse med field-test-001 (Hallvägen 21)
  - Risker / gap
  - Rekommendation
  - Bredare lärdom från sökandet
---

# Field test candidate 002 — Wagnshuset, Hufvudsta Gård

Kort version: **bättre material än Hallvägen, sämre bildurval. Inte ett tydligt
uppgraderat testdataset — men en värdefull data­punkt om annons­bias.**

## Källa

| | |
|---|---|
| **Annons** | https://www.lokalguiden.se/lokal/1-hufvudsta-gård-wagnshuset |
| **Adress** | Wagnshuset, Hufvudsta Gård, Kvarteret Brännerit (Solna) |
| **Lokaltyp** | Kontor / butik / vård — flexibel användning |
| **Yta** | ca 120 kvm, entréplan |
| **Byggår** | **1825** (synligt på gaveln i img-13), renoverad 2024 |
| **Planritning** | PDF, separat fil — `Relationshandlingar: Vagnshuset ENTRÉPLAN, 1/100`, daterad 2018-07-10 av ICON Architecture |
| **Bilder i annonsen** | 15 stycken |
| **Bild-CDN** | `static.lokalguiden.se/uploads/customer/392/...` — direkta URL:er |

## Vad vi laddade ner

Allt under `test-datasets/field-test-002/` (gitignored).

| Fil | Storlek | Innehåll |
|---|---|---|
| `planritning.pdf` | 211 KB | Två relationsritningar av entréplanet |
| `img-01.jpg` – `img-14.jpg` | 28–308 KB var | Annonsbilder (mix av interiör + exteriör) |
| `img-15.png` | 44 KB | Logotyp "NEW PROPERTY" — inte en bild av lokalen |

**Filstorlek är 10–100× mindre än Hallvägens bilder** (Hallvägen: 3–4.5 MB
per st). Wagnshuset levererar i thumbnail-upplösning — typiskt
640×480 till 800×600. Vilket är ett tveeggat svärd:

- **Plus**: Inga problem med Anthropics 5 MB-gräns; ingen kompression behövs;
  snabbare upload till API.
- **Minus**: Lägre upplösning = mindre material­detalj. Texturer (foger,
  slitage, ådring) blir svårare för AI:n att skilja på. Kan **dölja**
  återbruksrelevanta egenskaper.

## Granskning av bildurvalet

Detta är där datasetet brister. Av 15 "bilder":

| Kategori | Antal | Bilder |
|---|---|---|
| **Interiörbilder** | **7** | img-01, 03, 04, 05, 06, 07, 14 |
| Exteriör / fasad / omgivning | 6 | img-02, 09, 10, 11, 12, 13 |
| Lithografi (översikt av hela gården) | 1 | img-08 |
| Logotyp (mäklarens varumärke) | 1 | img-15 |

**Hallvägen 21 hade 10/12 interiörbilder. Wagnshuset har 7/15.** Per bild
mindre informativ för en återbruksinventering.

### Per interiörbild

| ID | Sannolik zon | Innehåll i korthet |
|---|---|---|
| `img-01` | ÖPPET KONTOR + KÖK i bakgrund | **Stor 1800-talskakelugn** i färggrant blommönstrat kakel, takbjälkar i grovt trä, vita målade golvplankor, glasade rumsavskiljare |
| `img-03` | MÖTE/KONFERENS | Konferensbord, orange stolar, stor TV-skärm, takbjälkar, glasvägg, vita golvplankor |
| `img-04` | KONTOR (insidan av rummet) | Trä-pardörrar (gamla, ramade), AC-enhet på vägg, fönster, vita golvplankor, takbjälkar |
| `img-05` | KÖK / PENTRY | Vita köksluckor (undermöbler), inbyggd svart micro/ugn, fönster, radiator, **stege och röd brandsläckare i bild** (renovering pågår?) |
| `img-06` | Hall / mot WC | Pardörrar, glimt av **kakel i WC-rummet genom dörröppningen**, vita golvplankor |
| `img-07` | KONTOR (alternativ vinkel?) | Trä-pardörrar, fönster, radiator, brandsläckare, white­boards, takbjälkar |
| `img-14` | ÖPPET KONTOR + MÖTE | Översiktsbild — glasvägg in till MÖTE-rummet, KÖK i bakgrund, människor som arbetar, takbjälkar, hela golvet i bild |

## Rum / zoner enligt planritningen

Planritningen visar **8 namngivna zoner** + 1 elsutrymme:

1. **ÖPPET KONTOR** (två sektioner i öst och väst — möjligen samma rum delat eller två zoner)
2. **KONTOR** (eget rum, östra delen)
3. **MÖTE/KONFERENS** (mitten av lokalen)
4. **KÖK**
5. **SKRUBB** (städ/förråd)
6. **SERVER** (server­rum, västra hörnet)
7. **WC** (två toaletter, södra väggen)
8. **EL** (litet elsutrymme intill WC)

Skalstreck 0–10 m visar att lokalen är ca 24 × 10 m, vilket stämmer med ~120
kvm för en del av planen (lokalen är en del av en större L-formad byggnad —
nedre delen av ritningen visar resten av planet, troligen andra hyresgäster).

## Föreslagen bild-till-zon-mapping

| Bild | Förmodad zon | Användbarhet |
|---|---|---|
| img-01 | ÖPPET KONTOR (väst, med kakelugn) | **Hög** — kakelugn är *guld* för återbruk |
| img-03 | MÖTE/KONFERENS | Hög |
| img-04 | KONTOR (eller hall till) | Medel — pardörrar synliga |
| img-05 | KÖK | Hög — fasta installationer |
| img-06 | Hall mot WC | **Hög** — bara *en* glimt av WC, men det är allt vi har |
| img-07 | KONTOR | Medel |
| img-14 | Översikt (flera zoner) | Hög — visar relation mellan rum |
| img-02, 09–13 | OUTSIDE_LOCAL | Låg — kullersten, fasad, sjö |
| img-08 | OUTSIDE_LOCAL (lithografi) | Mycket låg — översiktsteckning av hela gården |
| img-15 | OUTSIDE_LOCAL (eller exkludera) | Inget — logotyp |

### Per-zon-täckning

| Zon | Antal bilder |
|---|---|
| ÖPPET KONTOR (väst med kakelugn) | 1 (img-01) |
| ÖPPET KONTOR (öst) | 0 |
| KONTOR | 2 (img-04, img-07) |
| MÖTE/KONFERENS | 1 (img-03) |
| KÖK | 1 (img-05) |
| SKRUBB | 0 |
| SERVER | 0 |
| WC | 1/2 (glimt i img-06) |
| EL | 0 |
| Översiktsbild | 1 (img-14) |
| **Inte i lokalen** | **8** (img-02, 08–13, 15) |

## Material som sannolikt går att identifiera

Stora plus: Wagnshuset har **synligt 1800-talsmaterial** som är mycket
intressantare för återbruk än Hallvägens "vit kakel + grå mosaik".

| Material / objekt | Bilder | Återbruksrelevans |
|---|---|---|
| **Kakelugn** med blommönstrat kakel | img-01 | **Mycket hög** — sällsynt, värdefullt |
| **Synliga takbjälkar** i grovt sågat trä | alla interiör | **Mycket hög** — original 1800-tal sannolikt |
| **Vita målade golvplankor** (gamla, breda) | alla interiör | **Hög** — om original, värdefulla |
| **Trä-pardörrar** (gamla, ramade med glas) | img-04, img-06, img-07 | **Hög** — antikvariska |
| Gula puts-fasaden | img-09, img-12 | Inte återbruks-relevant men "konstitutionellt skyddat" |
| Gröna fönsterluckor (utsida) | img-09, img-10, img-12 | Medel — om de demonteras |
| Kakel i WC (skymt) | img-06 | Medel — för lite synligt |
| Vit-lackade köksluckor (modernt) | img-05 | Låg — IKEA-stil |
| Inbyggd ugn/micro (modernt) | img-05 | Medel |
| Radiatorer (vita) | img-05, img-07 | Medel |
| Brandsläckare (lös inventarie) | img-05, img-07 | Marginell |

## Jämförelse med field-test-001 (Hallvägen 21)

| Kriterium | Hallvägen 21 | Wagnshuset | Vinnare |
|---|---|---|---|
| Storlek (kvm) | 186 | 120 | Hallvägen (mer att inventera) |
| Byggår | Nyrenoverat kontorshotell | **1825**, ren. 2024 | **Wagnshuset** (återbruksrelevans) |
| Bilder totalt | 12 | 15 | Wagnshuset |
| **Interiörbilder** | **10** | **7** | **Hallvägen** |
| Planritning | PDF, 1.3 MB, namngivna zoner | PDF, 211 KB, namngivna zoner | Lika |
| Bildupplösning | Full (3–4.5 MB/st) | Thumbnail (28–308 KB) | **Hallvägen** (mer material­detalj) |
| Zoner i ritning | 8 | 8–9 | Lika |
| Zoner faktiskt täckta i bilder | 5/8 | 5/9 | Lika (båda har annonsbias) |
| WC i bilder | 0 (helt utelämnat) | 1 (glimt i img-06) | **Wagnshuset** (knappast, men något) |
| MÖTE i bilder | 0 (utelämnat) | 1 (img-03) | **Wagnshuset** |
| Stylad vs verklig | Stylad kontorshotell-feel | Renoverad 2024 men med synligt 1825-material | **Wagnshuset** |
| **Unika återbruksmaterial** (kakelugn, takbjälkar, gamla dörrar) | nej | **ja** | **Wagnshuset** |
| Annonsbias-grad | Måttlig (8/10 interiör är bra) | **Hög** (7/15 = 47 %) | **Hallvägen** |

### Slutsats av jämförelse

- **Wagnshuset vinner på domän-relevans** (1800-talsmaterial, kakelugn,
  WC och MÖTE faktiskt fotade)
- **Hallvägen vinner på antal interiörbilder och bildupplösning**

Det är inte en knockout. Det är en bytesaffär.

## Risker / gap

1. **Annonsbias-problemet är värre här.** 8 av 15 bilder är inte ens
   inomhus i lokalen. AI:n kommer producera "lokal-irrelevant" output
   om vi kör alla 15 — sjöbilder, husfasader, en logotyp. Lärdomen
   från `field-test-001` om OUTSIDE_LOCAL gäller dubbelt här.
2. **Lägre upplösning kan dölja material.** 28–80 KB-bilder är
   thumbnails. Många återbruksrelevanta detaljer (ådring, foger,
   slitage, varumärken) kan vara osynliga för AI:n på dessa.
3. **Renovering pågår i img-05.** Stege och brandsläckare i förgrund —
   bilderna är tagna *under* renovering, inte efter. Det kan göra
   "samlad inventering"-bedömningen mer rörig (vad är permanent,
   vad är tillfälligt?).
4. **Endast en glimt av WC.** Bättre än Hallvägens noll, men
   fortfarande inte tillräckligt för att inventera WC ordentligt.
5. **Servrum + skrubb + el helt utelämnade.** Tre av åtta zoner
   saknas — samma annonsbias-mönster som Hallvägen.

## Rekommendation

**Använd inte Wagnshuset som nytt primärt testdataset.** Det är inte
*tydligt bättre* än Hallvägen — det är ett sidsteg där vi byter
bildantal mot material­kvalitet.

Tre vägar framåt, i fallande ordning av sannolikt värde:

### A. Gå till fysisk lokal istället

Stoppa jakten på publika annonser. Annonser är designade för uthyrning,
inte för inventering — annonsbiasen är *inbyggd i marknaden*. Egna
foton från en riktig lokal (med ROT-relevans) ger:

- Full kontroll över bildurval — WC, förråd, undertak, allt
- Verklig upplösning (mobilen ger 4–8 MB)
- Närbilder på material vid behov
- Möjlighet att gå tillbaka och fota om

Det är **dataset-frågan vi egentligen vill svara**: håller workflowet
mot verklig användning? Annonsdataset svarar inte på det.

### B. Kombinera två dataset

Behåll `field-test-001` (Hallvägen) som primärt för zon-aggregeringen
och kör en kompletterande mini-test mot Wagnshusets 7 interiörbilder
specifikt för att se hur AI:n hanterar 1800-talsmaterial (kakelugn,
takbjälkar, gamla pardörrar). Det är en separat hypotes ("klarar AI
äldre material lika bra som modernt?") som är värd att besvara.

### C. Fortsätt leta publik annons

Om vi ändå vill stanna i annons-världen, lägg fokus på objekt med
**byggnadsbeskrivning + relationsritningar** (typ vad arkitekter får
tillgång till). De finns sällan publikt men dyker upp ibland i
mäklarbroschyrer för större objekt.

**Vår rekommendation: alternativ A** (fysisk lokal). Vi har redan
validerat workflowet mot annons-data i `room-aggregation-001` —
nästa naturliga steg är att verifiera mot data som inte är
mäklar-curaterad.

## Bredare lärdom från sökandet

Värdefullaste fyndet från detta arbete är inte själva datasetet —
det är **att svenska publika lokalannonser systematiskt är dåliga
testdataset för återbruksinventering**:

- **De flesta annonser har 1–3 bilder.** Lokalguiden, Objektvision —
  båda dominerade av minimala bildurval.
- **Restaurang- och butikssegmentet är extremt magert** — vad som
  borde vara mest intressant för återbruk (kakel, snickerier,
  bardiskar, ventilation) syns sällan.
- **Annonsbias är universell**, inte specifik för Hallvägen. Wagnshuset
  visar samma mönster i en mer ärlig form: fina exteriörer, WC och
  förråd utelämnade.
- **Objektvision blockerar Cloudflare** för automatisk fetch — kräver
  headless browser om man vill in. En större användare än vi kan
  förmodligen lösa det, men det är friction i sig.
- **Större mäklarsajter (Newsec, Croisette, JLL, Savills)** har mer
  bildmaterial men oftast bara för stora moderna objekt — vilket
  är *exakt motsatsen* till vad ombyggnads-/återbruksdomänen behöver.

Detta är värt att backloggas för domän-förståelsen: **om vi någonsin
bygger en produkt av detta är dataset-akkvisitionen en bottleneck**,
inte AI-kvaliteten.
