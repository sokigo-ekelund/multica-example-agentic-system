# Bygg tavlan: modellen som ett workflow i Multica

I Multica är ett **workflow** en uppsättning steg (kolumner) för ett projekt. För varje steg väljer du:

- **Handoff:** *No handoff*, *Hand to an agent* eller *Hand to a member*.
- **When done, move to:** vart ärendet går när steget är klart.
- **If rejected, send back to:** vart ärendet går om steget underkänns.
- **Handoff instructions:** en kort text som agenten får när den tar över.

Det är exakt modellens pilar. Bygg så här (ca 5 min).

## 1. Skapa workflowet
*Projektet Supportfabriken → Workflow → New workflow.* Utgå gärna från mallen **Delivery** och döp
om stegen, eller börja tomt. Döp workflowet till **Fabriksmodellen**.

## 2. Stegen

| # | Steg (kolumn) | Handoff | When done → | If rejected → | Rutan i modellen |
|---|---|---|---|---|---|
| 1 | **Inkorg** | No handoff | Validera in | – | Trigger & Uppdrag |
| 2 | **Validera in** | Agent: *Intag* | Arbetet | Inkorg | Validera in / Avvisa |
| 3 | **Arbetet** | Agent: *Skribent* | Validera ut | – | Arbetet |
| 4 | **Validera ut** | Agent: *Granskare* | Människa | Arbetet | Validera ut / Omtag |
| 5 | **Människa** | Member: *du själv* | Levererad | Arbetet | Human-in-the-loop |
| 6 | **Levererad** | No handoff | – | – | Leverans |

Använd dessutom status **Blocked** för eskalerade ärenden (handoff till *dig*) och **Cancelled**
för avvisade ärenden som inte ska kompletteras.

> Om ett ärende *avvisas* i Validera in skickas det tillbaka till **Inkorg**, alltså till beställaren
> för komplettering. Det är modellens "avvisa eller skicka tillbaka".

## 3. Handoff instructions (klistra in)

**Validera in → Intag**
```
Validera uppdraget med skillen validera-in. GODKÄNT IN: markera steget som klart (→ Arbetet).
AVVISAT: underkänn steget (→ Inkorg) och skriv vad som saknas. ESKALERAT: sätt status Blocked
och @-nämn den som skapade ärendet.
```

**Arbetet → Skribent**
```
Skriv artikeln med skillen skriv-artikel. Om det finns en UNDERKÄNT-kommentar är detta ett omtag:
åtgärda varje punkt. Markera steget som klart när UTKAST-kommentaren är skriven (→ Validera ut).
```

**Validera ut → Granskare**
```
Granska med skillen granska. GODKÄNT UT: markera steget som klart (→ Människa).
UNDERKÄNT: underkänn steget (→ Arbetet) med numrerad feedback, men bara om du har underkänt
färre än 2 gånger tidigare. Annars, eller vid regelkonflikt: ESKALERAT, sätt status Blocked
och @-nämn den som skapade ärendet.
```

## 4. Koppla workflowet till projektet
*Projektet → Workflow → välj Fabriksmodellen.* Det startar inga agenter. Inget händer förrän ett
ärende flyttas till en kolumn med agent-handoff.

## 5. Koppla underlaget
Agenterna behöver se mapparna `underlag/` och `leveranser/`. Under *Projektet → Resources* gör du något av följande:
- **Lokal mapp** (bara i Desktop-appen): välj den här repo-mappen. Läget **worktree** isolerar varje körning
  på en egen git-gren. Läget **in place** skriver direkt i mappen, vilket är enklast att visa i en demo.
- **Git-repo:** lägg till repots URL om det ligger på GitHub eller motsvarande.

---

## Plan B: utan workflow
Om workflowet beter sig annorlunda i din version av Multica fungerar fabriken ändå. Varje agent har en
reservväg i sina instruktioner och lämnar över med `multica issue assign <ÄRENDE> --to "<agent>"`.
Starta då ett ärende genom att **tilldela det till Intag**. Tavlan blir mindre tydlig, men kommentarerna
visar hela kedjan.
