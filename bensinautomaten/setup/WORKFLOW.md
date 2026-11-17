# Bygg tavlan: bensinautomaten som ett workflow i Multica

Samma princip som för Supportfabriken (se [../../setup/WORKFLOW.md](../../setup/WORKFLOW.md)):
varje kolumn är ett steg, och för varje steg väljer du handoff, *When done → move to* och *If rejected → send back to*.

## 1. Skapa workflowet
*Projektet Bensinautomaten → Workflow → New workflow.* Döp det till **Tankning**.

## 2. Stegen

| # | Steg (kolumn) | Handoff | When done → | If rejected → | Rutan i modellen |
|---|---|---|---|---|---|
| 1 | **Kö** | No handoff | Kortterminal | – | Trigger & uppdrag |
| 2 | **Kortterminal** | Agent: *Terminal* | Pump | Kort nekat | Validera in / avvisa |
| 3 | **Pump** | Agent: *Pump* | Kund | – | Arbetet |
| 4 | **Kund** | Member: *du själv* | Kassa | – | Människa mitt i flödet |
| 5 | **Kassa** | Agent: *Kassa* | Kvitto utskrivet | – | Validera ut |
| 6 | **Kvitto utskrivet** | No handoff | – | – | Leverans |
| 7 | **Kort nekat** | No handoff | – | – | Avvisat uppdrag |

Status **Blocked** betyder *avvikelse: stationsföreståndaren tar över*. Det är du.

> **Varför ingen människa före leveransen?** I Supportfabriken godkänner en människa varje artikel.
> Här vore det absurt om stationsföreståndaren godkände varje tankning. Människan kommer in
> **vid avvikelser**. Var människan ska in i flödet är ett riskbeslut, inte en självklarhet.

## 3. Handoff instructions (klistra in)

**Kortterminal → Terminal**
```
Validera tankningen med skillen automat: kontrollera-text, fara, uppgifter, kort och reservation.
GODKÄNT: markera steget som klart (→ Pump). NEKAT: underkänn steget (→ Kort nekat).
STOPPAD: sätt status Blocked och @-nämn den som skapade ärendet.
```

**Pump → Pump**
```
Tanka med skillen automat (tanka, sedan erbjud). Ställ frågan om spolarvätska en gång om skriptet
säger ERBJUD. Markera steget som klart (→ Kund). Vid AVVIKELSE: sätt status Blocked och @-nämn den
som skapade ärendet.
```

**Kund → du**
```
Svara ja eller nej på frågan om spolarvätska i en kommentar och markera steget som klart.
Om ingen fråga ställdes markerar du bara steget som klart.
```

**Kassa → Kassa**
```
Avsluta med skillen automat. Registrera kundens svar om spolarvätska, kör avsluta och klistra in
kvittot. Finns ett BESLUT från en människa verkställer du det. Markera steget som klart
(→ Kvitto utskrivet). Vid AVVIKELSE: sätt status Blocked och @-nämn den som skapade ärendet.
```

## 4. Avvikelser: så tar du över
1. Ärendet får status **Blocked** och du blir @-nämnd. Läs avvikelsekommentaren.
2. Skriv en kommentar: `BESLUT: häv` (ingen debitering) eller `BESLUT: debitera` (kunden betalar det som tankats).
3. **Flytta ärendet till Kassa.** Kassan verkställer beslutet och skriver kvittot.

Vid STOPPAD i kortterminalen, till exempel rökning eller ett kortnummer i ärendet, finns ingen
reservation. Då avslutar du bara ärendet (Cancelled).

## 5. Koppla mappen
*Projektet → Resources → Local folders → Choose folder…* och välj mappen **`bensinautomaten/`**.
Välj läget **Edit directly** (in place).

> **Inte "Run in parallel".** Alla tankningar delar tillstånd i `tillstand/`. Ett spärrat kort ska
> vara spärrat även vid nästa tankning. I worktree-läget får varje körning en egen kopia, och då
> glömmer automaten mellan stegen.

---

## Plan B: utan workflow
Starta en tankning genom att **tilldela ärendet till Terminal**. Varje agent lämnar över med
`multica issue assign` enligt reservvägen i sina instruktioner. Pumpen lämnar till dig. Du svarar och
tilldelar ärendet till **Kassa**.
