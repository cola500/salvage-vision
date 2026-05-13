# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Vad detta projekt är

En liten validering — hypotes-driven prototyp i en enda fil (`app.py`) som testar om Claude vision kan göra ett användbart återbruksinventeringsutkast från en bild på under 30 sekunder. Hypotesen är **confirmed**, se `HYPOTHESIS.md` för status och nästa naturliga slices.

Detta är **inte** en produkt-app — det är experiment-kod. Stora arkitekturella tillägg (databas, auth, projektmodell, CSV-export) ska inte införas innan vidare hypotes-validering beslutats. Se `HYPOTHESIS.md` § "Decision" för vad som är medvetet utelämnat.

## Köra

```sh
uv run app.py            # startar på http://localhost:5050
ANTHROPIC_API_KEY=sk-... uv run app.py   # riktiga AI-anrop, annars mock-fallback
```

Beroenden ligger som PEP 723-inline-metadata i `app.py` (Flask, anthropic) — ingen `requirements.txt`, `pyproject.toml` eller venv behövs. `uv` löser det.

Det finns inga tester, ingen linter och inget byggsteg — verifiering sker manuellt i webb-UI:t (timer + tabell + rå JSON).

## Saker som lätt biter

- **Port 5050, inte 5000**: macOS AirPlay äter 5000. Behåll 5050 om du inte explicit byter.
- **Claude Sonnet 4.6 stöder inte assistant-message-prefill** ("conversation must end with a user message"). `app.py` löser det med tolerant JSON-parsning: `text[text.find("{") : text.rfind("}") + 1]`. Behåll mönstret — lägg inte tillbaka prefill.
- **Mock-fallback är medveten och viktig**: saknad API-nyckel eller API-fel returnerar `MOCK` med ett `_source`-fält som UI:t visar. Demon ska aldrig stanna — om du ändrar felhantering, bryt inte den garantin.
- **In-memory state**: `SAVED`-listan försvinner vid omstart. Det är avsiktligt för denna slice.
- **Modell-ID**: `claude-sonnet-4-6`. Lita inte på training-data när du byter modell — verifiera aktuellt ID innan ändring.

## Arbetsstil i denna repo

- `HYPOTHESIS.md` följer ett strukturerat format (frontmatter + Hypothesis / Test / Success Criteria / Time Budget / Result). Om du skapar nya hypotes-dokument: håll samma form.
- Time budgets i `HYPOTHESIS.md` är riktiga — respektera dem. "15 min build, stopp vid 20" betyder att vi inte ska bygga in ny scope mitt i en slice.
- Hela UI:t (HTML/CSS/JS) ligger som en sträng i `index()`. Det är medvetet för denna single-file-slice. Splitta inte ut det utan att först förankra att projektet ska växa.
