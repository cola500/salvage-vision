---
title: Problem statement — återbruksinventering idag
description: Varför återbruksinventering i ombyggnadsprojekt är fragmenterat och tidskrävande, och var AI-assistering potentiellt kan hjälpa
category: external-doc
status: draft
last_updated: 2026-05-13
sections:
  - Problemet
  - Varför är det svårt idag
  - Hur det verkar göras nu
  - Observerade friktioner
  - Varför AI-assistering kan vara relevant
  - Vad vi inte vet ännu
---

# Problem statement — återbruksinventering idag

## Problemet

I varje ombyggnads- eller rivningsprojekt sker en återbruksinventering.
Den ska svara på fem frågor om en befintlig lokal:

1. **Vad finns här?** — Vilka material och objekt finns i lokalen?
2. **Vad är det värt?** — Ekonomiskt, miljömässigt, för planeten?
3. **Hinder eller möjlighet?** — Är det blockerande eller en resurs?
4. **Hur påverkar det den nya designen?** — Kan befintligt informera ny layout?
5. **Hur sänker vi tröskeln för icke-experter?**

Idag svarar man oftast manuellt på fråga 1, specialister på 2–4, och
fråga 5 sällan alls. Vår hypotes är att stora delar av fråga 1 plus
utkast på 2–3 kan AI-assisteras — och att det förflyttar var människans
tid läggs.

## Varför är det svårt idag

Återbruksinventering är fortfarande till stor del manuellt:

- **Tidskrävande**: någon står i lokalen, skriver i ett tomt formulär.
- **Kompetenskrävande**: vad är värdefullt? Vad är ett hinder? Det är
  inte uppenbart för en lekman.
- **Skala-känsligt**: större lokal = exponentiellt mer arbete.
- **Subjektivt**: tre inventeringar av samma lokal kan se olika ut.

Branschen drivs nu av nya krav (klimatdeklaration vid nybyggnad,
EU-taxonomi, Boverkets riktlinjer för cirkulär ekonomi), men metodiken
har inte hunnit med. Det är fortfarande "konsult-i-lokal-med-block".

## Hur det verkar göras nu

Vi har sett tre vanliga arbetsstilar i samtal och egen testning:

- **Klassiskt formulär** — Excel eller Word-mall, en rad per material
  eller objekt.
- **Ritningsmarkering** — anteckningar direkt på en utskriven
  planritning.
- **Foto + notebook** — bilder på platsen, anteckningar senare på
  kontoret.

Gemensamt: **datainmatning är primär arbetsuppgift**. Bedömning sker
parallellt med inmatning, vilket gör att man ofta gör båda halvbra
istället för någondera helbra.

## Observerade friktioner

Inte vetenskapligt fastställt — det här är vad vi sett i första samtal
och egen testning:

1. **Tom-formulär-friktionen** — att börja från noll i ett kalkylark
   är demoraliserande på en stor lokal.
2. **"Var var jag?"-friktionen** — efter en timme blir det svårt att
   hålla reda på vilka rum som inventerats.
3. **Dublettrisken** — samma sak i flera rum, eller från flera bilder,
   blir lätt räknat fel.
4. **Tröskeln för icke-experter** — en arkitekt utan
   återbrukserfarenhet vågar inte göra en bedömning, så hen anlitar
   en specialist eller hoppar över det.
5. **Bias mot det "vackra"** — när bilder tas i fält fokuserar man
   oftast på de tydliga objekten. WC, förråd och installationer
   hamnar i skuggan, även om de innehåller material.

## Varför AI-assistering kan vara relevant

Modern vision-AI har de senaste åren gått från "kanske känna igen katt
eller hund" till att kunna producera ett strukturerat första
inventeringsutkast från en bild på under 30 sekunder. Det är *inte*
färdigt beslutsunderlag — men det adresserar tom-formulär-friktionen
och tröskeln för icke-experter.

Värdet ligger inte i att AI ersätter expertbedömningen. Värdet är att
den:

- **flyttar arbete** från datainmatning till granskning och korrigering
- **gör icke-experter användbara** som "fototagare med checklista"
- **håller koll** på vilka zoner som har täckts (människan glömmer,
  AI:n inte)
- **flaggar dubletter** istället för att de tyst räknas dubbelt

AI:n är **inte** bra på värdebedömning, hinder/möjlighet, eller
skick-bedömning från foto. Den är **bra på** vad-finns-här — och inte
ens där alltid pålitlig.

## Vad vi inte vet ännu

Det här är hypoteser, inte fakta:

- **Räcker AI-utkastet för icke-experten?** Vågar en arkitekt utan
  återbrukserfarenhet skicka AI-utkast vidare som underlag, eller
  ringer hen ändå en specialist?
- **Hur stor är bildurvalsbiasen i fält?** Vi vet från publika
  annonser att bildurvalet är vinklat. Är samma sak sant när
  användaren fotar själv?
- **Vad är "tillräckligt bra" för beslutsfattare?** AI ger 4/5 i
  snitt på enskilda bilder. Är det tillräckligt för att fatta
  ekonomiska beslut på?
- **Var slutar AI-stöd och börjar mänsklig expertbedömning?**
  Skick, hinder, värde — vilka delar är genuint människo-arbete?
- **Skalar workflowet?** Vi har testat 10 bilder. Hur ser 50 ut?
  100? Vid vilken volym bryts den manuella granskningen?
- **Vem är användaren?** Arkitekt, specialist, byggherre eller
  fastighetsägare? Värdet ser olika ut för var och en.

Det här är frågor vi bygger nästa experiment för att besvara — inte
påståenden vi redan har svar på.
