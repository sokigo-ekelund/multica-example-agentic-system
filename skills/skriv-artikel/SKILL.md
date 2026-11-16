---
name: skriv-artikel
description: Skriver en hjälpartikel för Bokningsportalen utifrån underlag i mappen underlag/, enligt Supportfabrikens stilguide och mall. Används av agenten Skribent i steget Arbetet, både första gången och vid omtag.
---

# Skriv hjälpartikel

## Förutsättningar
- Ärendet har passerat Validera in. Det finns en kommentar *VALIDERA IN: GODKÄNT IN*.
- Kommentaren anger frågan artikeln ska besvara och vilket underlag som är relevant.

## Steg
1. Läs frågan och den relevanta underlagsfilen i `underlag/` i sin helhet.
2. **Omtag?** Om det finns en kommentar *UNDERKÄNT* från Granskaren: lista dess punkter och åtgärda
   var och en. Behåll resten av artikeln.
3. Läs `references/stilguide.md`.
4. Skriv artikeln enligt `assets/mall.md`:
   - Rubriken är frågan, formulerad som användaren skulle säga den.
   - Under *Sammanfattning* skriver du svaret i 1–2 meningar.
   - Under *Så gör du* skriver du numrerade steg med ett moment per steg.
   - *Bra att veta* är valfritt och innehåller begränsningar eller vanliga misstag. Allt ska finnas i underlaget.
   - Under *Källor* listar du underlagsfilerna, en per rad, som `underlag/filnamn.md`.
5. Kontrollera själv att varje påstående finns i underlaget. Stryk det som inte gör det.
6. Spara filen och lägg in den som kommentar *UTKAST vN* (se agentinstruktionen).

## Kontroll innan du lämnar över
- Högst 250 ord, rubrikerna exakt enligt mallen och minst en källa.
- Inga ord från listan över förbjudna ord i stilguiden.
