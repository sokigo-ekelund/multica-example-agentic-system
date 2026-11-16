---
name: validera-in
description: Grindvaktskontroll innan arbete startar. Avgör om ett uppdrag i Supportfabriken är tydligt, inom fabrikens område och har tillräckligt underlag. Används av agenten Intag i steget Validera in.
---

# Validera in

## Förutsättningar
- Du har tillgång till ärendets titel, beskrivning och kommentarer.
- Mappen `underlag/` finns i arbetskatalogen. Om den saknas: ESKALERA med motiveringen
  "Projektet saknar underlag. Kontrollera att repot är kopplat som resurs."

## Steg – gå igenom i ordning
1. **Rätt sak?** Handlar uppdraget om en hjälpartikel för Bokningsportalen?
   - Nej → AVVISAT ("utanför fabrikens område").
2. **Tydlig fråga?** Kan du formulera *den fråga artikeln ska besvara* i en mening?
   - Nej → AVVISAT och be om förtydligande.
3. **Regelkonflikt?** Kräver uppdraget något som regelboken förbjuder, till exempel löften utöver
   supportpolicyn, ersättning, juridik eller personuppgifter?
   - Ja → ESKALERAT. Ange vilken regel det gäller.
4. **Underlag?** Sök i `underlag/` efter information som besvarar frågan. Läs filerna. Gissa inte från filnamnen.
   - Inget relevant underlag → AVVISAT och ange vad som saknas.
   - Delvis underlag → GODKÄNT IN bara om kärnfrågan kan besvaras. Skriv annars AVVISAT.
5. **Storlek?** Är det *en* artikel? Om uppdraget kräver flera artiklar → skriv i beslutet att det
   bör gå till Orkestrator. Beslutet blir ESKALERAT.

## Leverans – mall för kommentaren

```
## VALIDERA IN: <GODKÄNT IN | AVVISAT | ESKALERAT>

**Frågan artikeln ska besvara:** <en mening>
**Relevant underlag:** <filnamn, eller "saknas">

| Kontroll | Resultat |
|---|---|
| Rätt sak | ✅ / ❌ |
| Tydlig fråga | ✅ / ❌ |
| Ingen regelkonflikt | ✅ / ❌ (regel nr X) |
| Underlag finns | ✅ / ⚠️ delvis / ❌ |
| Lagom storlek | ✅ / ❌ |

**Motivering / vad som behöver kompletteras:** <kort>
```
