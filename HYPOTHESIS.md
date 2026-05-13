---
title: AI-assisterad återbruksinventering
description: Verifiera om en bild kan ge ett användbart inventeringsutkast på under 30 sekunder
category: ux-validation
status: confirmed
last_updated: 2026-05-13
sections: [Hypothesis, Test, Success Criteria, Time Budget, Result]
---

# AI-assisterad återbruksinventering

## Hypothesis
En användare (arkitekt/inventeringskonsult) kan ta en bild av ett rum/material och få ett användbart första inventeringsutkast på under 30 sekunder — snabbare och bättre än att börja från ett tomt formulär.

## Test
Single-file Flask-app med:
- Upload av en bild
- POST /analyze → Claude Sonnet 4.6 vision → strukturerad JSON (material, objekt, mängd, återbrukspotential)
- Visning som tabell + rå JSON
- Spara till in-memory lista

Fallback till hårdkodat mock-svar om API-nyckel saknas eller anrop failar (så demon alltid funkar).

## Success Criteria
- Tid från upload till lista < 30s (timer i UI mäter exakt)
- Listan har ≥3 plausibla rader
- Minst en rad är korrekt nog att korrigera istället för skriva om från scratch
- Mock-fallback triggas tydligt om nyckel saknas (källa visas i UI)

## Time Budget
15 min build. Stopp vid 20 min oavsett.

## Result

- **Status**: **Confirmed** — Claude Sonnet 4.6 levererar ett användbart inventeringsutkast på under 15s, och utkastet är bra nog att korrigera istället för skriva om.

- **What we learned**:
  - **Tid**: Under 15s från upload till lista — klart under 30s-budgeten. Marginalen ger utrymme för bättre bilder och eventuell efterbearbetning utan att spräcka loopen.
  - **Kvalitet**: Listan trafficker rätt på majoriteten — användaren bedömde den som "klart användbar" och bättre startpunkt än tomt formulär. Det är hypotesens kärnvärde.
  - **API-detalj**: Sonnet 4.6 stöder inte längre assistant-message-prefill ("conversation must end with a user message"). Vi tog bort prefill och löste det med tolerant JSON-parsning (`find('{')` → `rfind('}')`). Bra att ha för andra Claude-projekt.
  - **Mock-fallbacken räddade demon** vid API-felet — användaren såg felmeddelandet i UI:t men flödet stannade aldrig. Värdefullt mönster för framtida prototyper.
  - **Rå JSON under tabellen** var rätt val — gjorde det möjligt att direkt se varför något var fel och bedöma AI-svaret.
  - **Port 5000** är blockerad av macOS AirPlay — använd annan port (5050 fungerar).

- **Decision**: **Keep & expand** — hypotesen håller. Nästa naturliga steg om vi vill ta detta vidare:
  1. **Testa bredd**: kör 5–10 bilder av olika scenarier (kök, kontor, badrum, tegelvägg, takinstallation) och mät hit/miss-rate systematiskt.
  2. **Användarvalidering**: visa demon för 1–2 arkitekter/inventeringskonsulter — fråga "skulle du börja från detta utkast eller tomt formulär?"
  3. **Nästa slice**: redigerbar lista (cellklick → ändra) och exportera till CSV/Excel — det är vad användare sannolikt behöver direkt efter "det funkade".
  4. **Inte ännu**: persistent databas, auth, projekt, CO₂-beräkning, mängd-kalibrering. Bevisa värdet bredare först.

