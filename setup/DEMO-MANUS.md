# Demomanus (ca 30–40 min)

> **Generalrepetera kvällen innan.** Agenterna är stokastiska: samma uppdrag kan ta olika vägar.
> Kör alla fyra uppdragen en gång i förväg och spara skärmdumpar eller länkar som reserv.
> En körning tar några minuter, så starta nästa uppdrag medan du pratar om det förra.

## 0. Visa tavlan tom (3 min)
- Visa kolumnerna och peka på modellen: *Inkorg → Validera in → Arbetet → Validera ut → Människa → Levererad*.
- Öppna en agent och visa att den bara består av **instruktioner + skills + runtime**.
  Agenten är ingen magi. Den är en arbetsbeskrivning.
- Visa workspace-kontexten: **regelboken** som alla agenter får i varje körning.

## 1. Happy path: `01 Hur bokar jag ett möte som återkommer varje vecka?` (8 min)
1. Dra ärendet från *Inkorg* till *Validera in*. Intag startar.
2. Öppna ärendet och visa kommentaren **VALIDERA IN: GODKÄNT IN** med kontrolltabellen.
3. Ärendet glider vidare till *Arbetet*. Visa **UTKAST v1** och filen i `leveranser/`.
4. I *Validera ut* visar du att Granskaren kör **kontrollskriptet**.
   Det är deterministiskt, medan modellen inte är det. Visa checklistan.
5. Ärendet landar hos **dig**. Läs artikeln och flytta den till *Levererad*.

**Poäng:** fyra rutor, fyra ansvar och full spårbarhet i kommentarerna.

**Demonstrera omtag:** om artikeln gick igenom direkt kan du *underkänna* den i steget Människa
med en kommentar, till exempel "Lägg till hur man avbokar ett enskilt tillfälle i serien". Ärendet går
tillbaka till *Arbetet* och Skribenten gör ett omtag.

## 2. Avvisat: `02 Artikel om export till Power BI` (5 min)
1. Dra till *Validera in*.
2. Intag **avvisar** eftersom underlaget saknas. Ärendet går tillbaka till Inkorg med en lista över vad som behöver kompletteras.

**Poäng:** det billigaste felet är det som aldrig påbörjas. En agent utan Validera in hade *hittat på*
en Power BI-guide, och den hade sett trovärdig ut.

## 3. Eskalerat: `03 Artikel: vad gäller vid driftstopp?` (5 min)
1. Dra till *Validera in*.
2. Intag ser en **regelkonflikt** (löfte om 100 % och ersättning) och eskalerar till dig (*Blocked*).

**Poäng:** regelboken styr före, under och efter arbetet. Om Intag ändå släpper igenom uppdraget
fångar Granskaren och skriptet de förbjudna orden. Det ger två skyddsnät.

## 4. Fraktalt: `04 Startpaket för nya användare` (10 min)
1. **Tilldela** ärendet till *Orkestrator* i stället för att dra det till Validera in.
2. Orkestratorn skriver en **PLAN** och skapar tre **sub-issues**. Varje sub-issue går genom *hela* tavlan.
3. Godkänn de tre artiklarna en i taget i steget Människa.
4. När alla är klara väcks Orkestratorn, sätter ihop översikten och lämnar helheten till dig för godkännande.

**Poäng:** samma modell på två nivåer. *Arbetet* i det stora uppdraget består av tre små kompletta fabriker.
Byt "artikel" mot "funktion" så har du Canellas mjukvarufabrik. Byt mot "avdelningens kvartalsmål" så har du
en organisation.

## 5. Avslutning: från demo till egen fabrik (5 min)
- Peka på [README → Gör om det till din egen fabrik](../README.md#gör-om-det-till-din-egen-fabrik): fyra filer att byta.
- **Taket för omtag fanns inte i verktyget.** Det står i Granskarens instruktioner. De viktigaste
  reglerna i en fabrik bygger du själv.
- **Lärdomar:** gå igenom Granskarens förslag på lärdomar. Vilka ska in i regelboken?
- **Bonus:** en *Autopilot* kan skapa ärenden på ett schema, till exempel "varje måndag 09:00: gå igenom
  veckans supportfrågor". Då har fabriken också en automatisk trigger.
