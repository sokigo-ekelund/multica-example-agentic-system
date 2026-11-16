---
name: granska
description: Oberoende granskning (Validera ut) av en hjälpartikel i Supportfabriken. Kör ett deterministiskt kontrollskript och går igenom en checklista mot källorna. Används av agenten Granskare.
---

# Granska (Validera ut)

## Förutsättningar
- Det finns ett utkast: en fil i `leveranser/` för ärendet, eller en kommentar *UTKAST vN*.
- Om utkastet bara finns som kommentar sparar du det först till en temporär fil, så att skriptet kan köras.

## Steg
1. **Maskinkontroll.** Kör kontrollskriptet från den här skillens mapp:
   ```
   python3 <skillens-mapp>/scripts/kontrollera_artikel.py leveranser/<fil>.md --underlag underlag
   ```
   Skriptet är deterministiskt och ger samma svar varje gång. Varje ❌ betyder automatiskt UNDERKÄNT.
   Om skriptet inte går att köra noterar du det och gör kontrollerna för hand.
2. **Faktakontroll.** Ta varje påstående i artikeln och leta upp stödet i underlagsfilerna.
   Ett påstående utan stöd betyder UNDERKÄNT. Ett påstående som lovar mer än supportpolicyn betyder ESKALERAT.
3. **Checklista.** Gå igenom `references/checklista.md` punkt för punkt.
4. **Omtagsräkning.** Räkna dina tidigare kommentarer med *UNDERKÄNT* på ärendet.
5. **Beslut** enligt agentinstruktionen: GODKÄNT UT, UNDERKÄNT (omtag n av 2) eller ESKALERAT.

## Leverans – mall för kommentaren

```
## VALIDERA UT: <GODKÄNT UT | UNDERKÄNT (omtag n av 2) | ESKALERAT>

**Granskat:** <fil eller UTKAST vN>
**Maskinkontroll:** <✅ alla OK | ❌ antal fel>  (klistra in skriptets utdata)

| Checklista | Resultat |
|---|---|
| 1. Svarar på frågan | ✅ / ❌ |
| ... | |

**Feedback till Skribent** (bara vid UNDERKÄNT, numrerad och åtgärdbar):
1. ...

**Skäl till eskalering** (bara vid ESKALERAT): <taket nått / regelkonflikt regel X / osäkerhet>

**Förslag på lärdom** (vid UNDERKÄNT och ESKALERAT): <vad i regelbok, underlag eller skill hade förhindrat detta?>
```
