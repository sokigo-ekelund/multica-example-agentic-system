# Den fraktala modellen – och hur den blir en tavla i Multica

## Modellen i korthet

Allt målmedvetet arbete följer samma grundstruktur, oavsett om det utförs av en människa eller
en AI-agent och oavsett skala:

1. **Trigger & Uppdrag (+ underlag):** något sätter igång arbetet.
2. **Validera in:** gör vi rätt sak, och räcker underlaget? Om inte: **avvisa**.
3. **Arbetet:** utförs med *verktyg*, *kunskap*, *processer* och *förutsättningar*.
4. **Validera ut:** håller resultatet? Om inte: **omtag** (max 2). Hög risk eller regelkonflikt: **eskalera**.
5. **Människa:** granskar och beslutar (*human-in-the-loop*).
6. **Leverans.**

Över allt detta ligger **regelboken**, som gäller före, under och efter arbetet.

Modellen är **fraktal**. Ett stort uppdrag bryts ner i deluppdrag inuti *Arbetet*, och varje
deluppdrag är en egen miniatyr av samma modell.

> Det vanligaste misstaget när man bygger agentiska system är att bara automatisera rutan
> *Arbetet*. Fabriken blir pålitlig först när de andra rutorna också finns.

## Från modell till Multica

| Modellen | I Multica | I det här repot |
|---|---|---|
| Trigger & Uppdrag | Ett **issue** på tavlan. Kan också skapas automatiskt av en **Autopilot** (schema eller webhook). | `demo-uppdrag/` |
| Underlag | Issue-beskrivningen plus projektets **resurser** (repo eller mapp) | `underlag/` |
| Regelbok | **Workspace-kontext** och projektbeskrivning. Når alla agenter i varje körning. | `regelbok/REGELBOK.md` |
| Validera in | Kolumn med överlämning till agenten **Intag** | `agenter/intag.md`, `skills/validera-in/` |
| Avvisa | Kolumnen *Avvisad*. Ärendet går tillbaka till beställaren. | – |
| Arbetet | Kolumn med överlämning till agenten **Skribent** | `agenter/skribent.md`, `skills/skriv-artikel/` |
| · Verktyg | AI-kodverktyget (runtime), filer, MCP-kopplingar, skript | `skills/granska/scripts/` |
| · Kunskap | **Skills** med referensfiler | `skills/*/references/` |
| · Processer | Stegen i skillen, och för stora uppdrag **sub-issues** | `SKILL.md` → "Steg" |
| · Förutsättningar | Kontrolleras av Intag innan arbetet startar | `skills/validera-in/` |
| Validera ut | Kolumn med överlämning till agenten **Granskare**. *Om underkänt → skicka tillbaka till Arbetet.* | `agenter/granskare.md`, `skills/granska/` |
| Tak för omtag | **Finns inte inbyggt i Multica.** Det står i Granskarens instruktioner. | `agenter/granskare.md` |
| Eskalera | Granskaren lämnar över till en människa | – |
| Människa | Kolumn med överlämning till **en medlem** (dig) | – |
| Leverans | Status *Levererad* + artikeln som kommentar och som fil | `leveranser/` |
| Fraktal nedbrytning | **Sub-issues** (med *stages*). Föräldern väcks när ett steg är klart. Eller en **Squad** med ledare. | `agenter/orkestrator.md` |

## Tre saker som är värda att stanna vid

**1. Taket för omtag måste du bygga själv.**
Agenter i Multica kan lämna över till varandra i all oändlighet. Multica slår ihop dubbla körningar
men stoppar inte loopar. Regeln "max två omtag, sedan en människa" är alltså en del av *regelboken*,
inte av verktyget. Det gäller för de flesta agentplattformar.

**2. Alla rutor behöver inte vara en egen agent (System 1 och System 2).**
För ett litet, invant uppdrag räcker det att *Validera in* är första steget i utförarens skill.
Det motsvarar System 1. För ett stort eller riskfyllt uppdrag ska det vara en *egen* agent som
inte är lojal mot sitt eget arbete. Det motsvarar System 2. Samma sak gäller *Validera ut*:
den som skrivit något är dålig på att underkänna det.

**3. En fabrik ska bli bättre över tid.**
Varje omtag och eskalering är en signal om att regelboken, underlaget eller skillen behöver
förbättras. Granskaren föreslår därför en *lärdom* när något går fel. Människan avgör om den
ska in i regelboken.

## Samma modell, andra skalor

| Skala | Trigger & Uppdrag | Arbetet | Validera ut | Människa |
|---|---|---|---|---|
| Arbetsmoment (det här repot) | Kundfråga | Skriva en artikel | Checklista + skript | Supportansvarig |
| Medarbetare | Veckans ärenden | Flera arbetsmoment i följd | Egen kontroll + kollega | Chef |
| Avdelning | Kvartalsmål | Många parallella flöden (sub-issues) | Uppföljning | Avdelningschef |
| Mjukvarufabrik | Ärende i backloggen | Skriva och testa kod | Tester + kodgranskning | Tech lead |
| Företag | Strategiskt beslut | Projekt och avdelningar | Revision | Styrelse |
