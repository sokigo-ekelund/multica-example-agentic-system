---
name: automat
description: Styr Bensinautomatens simulerade maskinvara (kortläsare, pump, kassa) via det deterministiska skriptet automat.py. Används av agenterna Terminal, Pump och Kassa. All hantering av kort, PIN, belopp och liter går genom skriptet.
---

# Automat

Bensinautomatens "hårdvara" är ett skript. Agenten bestämmer *vad* som ska göras och skriver
kommentarer. Skriptet gör själva kontrollerna och räknar alla belopp. **Räkna aldrig själv.**

## Så kör du skriptet
Kör alltid från projektmappen, alltså mappen där `underlag/` finns:
```
python3 skills/automat/scripts/automat.py <kommando> <ÄRENDE> [flaggor]
```
Om mappen `skills/` inte finns i projektmappen kör du skriptet från den här skillens mapp,
`python3 <skillens-mapp>/scripts/automat.py`, men fortfarande med projektmappen som aktuell mapp.

`<ÄRENDE>` är ärendets ID i Multica, till exempel `MINW-12`. Använd samma ID i alla steg.

## Läs utfallet
Sista raden är alltid `RESULTAT: <UTFALL> – <skäl>`. Klistra in den raden i din kommentar.

| Exit-kod | Betyder | Vad du gör |
|---|---|---|
| 0 | Gick bra | Fortsätt |
| 1 | Nekat av en regel | Följ agentinstruktionen (t.ex. Kort nekat) |
| 2 | Avvikelse eller stopp | Eskalera till en människa. Gör inget mer |
| 3 | Fel användning | Rätta kommandot. Om det inte går: eskalera |

Alla kommandon tål att köras igen. Om ett steg redan är gjort säger skriptet det i stället för att göra om det.

## Kommandon per steg

**Kortterminal (Terminal)**
```
python3 skills/automat/scripts/automat.py kontrollera-text < ärendetext.txt
python3 skills/automat/scripts/automat.py kort <ÄRENDE> --kort TEST-4242 --pin "fel, korrekt"
python3 skills/automat/scripts/automat.py reservera <ÄRENDE>
```
Spara ärendets beskrivning i en temporär fil och kör `kontrollera-text` på den **innan** du gör något annat.

**Pump (Pump)**
```
python3 skills/automat/scripts/automat.py tanka <ÄRENDE> --bransle "Bensin 95" --liter 40 [--avbrott-vid 12.4]
python3 skills/automat/scripts/automat.py erbjud <ÄRENDE>
```
`--liter` är den mängd kunden vill ha. Vid fulltank anger du hur mycket tanken tar. Skriptet stoppar
pumpen när reservationen är nådd. Använd `--avbrott-vid` bara om ärendet beskriver ett pumpfel.

**Kassa (Kassa)**
```
python3 skills/automat/scripts/automat.py spolarvatska <ÄRENDE> ja|nej
python3 skills/automat/scripts/automat.py avsluta <ÄRENDE>
python3 skills/automat/scripts/automat.py avsluta <ÄRENDE> --trots-avbrott   # bara efter BESLUT: debitera
python3 skills/automat/scripts/automat.py hav <ÄRENDE>                       # bara efter BESLUT: häv
```

**Alla:** `status <ÄRENDE>` visar var tankningen står och dess logg. `oppna` listar öppna reservationer.

## Kommentarer
Använd mallarna i `references/kommentarer.md`.
