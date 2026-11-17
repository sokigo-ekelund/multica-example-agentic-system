# Supportfabriken – ett exempel på en agentisk fabrik i Multica

Det här repot är en **startpunkt** för den som vill bygga sin första "fabrik" av AI-agenter.
Fabriken är liten med flit: den tar emot en kundfråga och levererar en färdig, granskad
hjälpartikel. Den bygger på samma modell som en mjukvarufabrik. Det enda som skiljer är
vad som tillverkas.

> **Poängen är inte artiklarna.** Poängen är att se *hela* arbetsflödet på en tavla:
> uppdrag → validera in → arbetet → validera ut → människa → leverans. Läs [MODELL.md](MODELL.md).

```
 Inkorg ──► Validera in ──► Arbetet ──► Validera ut ──► Människa ──► Levererad
            (Intag)         (Skribent)  (Granskare)     (du)
               │                ▲            │  │
               ▼                └── omtag ───┘  └── eskalera ──► Människa
            Avvisad              (max 2)
```

## Vad finns här?

| Mapp / fil | Vad det är | Rutan i modellen |
|---|---|---|
| [`regelbok/REGELBOK.md`](regelbok/REGELBOK.md) | Regler som gäller alla agenter, hela tiden | Regelbok |
| [`agenter/`](agenter/) | Instruktioner för fyra agenter: Intag, Skribent, Granskare, Orkestrator | Vem som gör vad |
| [`skills/`](skills/) | Tre skills (SKILL.md + checklistor, mallar och ett kontrollskript) | Kunskap · Processer · Verktyg |
| [`underlag/`](underlag/) | Fiktiv produktinformation om *Bokningsportalen*. Det enda agenterna får hämta fakta från | Underlag · Källor |
| [`demo-uppdrag/`](demo-uppdrag/) | Fyra uppdrag som visar olika vägar genom flödet | Trigger & Uppdrag |
| [`leveranser/`](leveranser/) | Här hamnar färdiga artiklar | Leverans |
| [`setup/`](setup/) | Setup-skript, klickguide för tavlan och manus för demon | – |
| [`bensinautomaten/`](bensinautomaten/) | En andra "fabrik": en bensinautomat där varje ärende är en tankning. Visar deterministiska verktyg för pengar och en människa bara vid avvikelser | Hela modellen igen |
| [`presentation/`](presentation/) | Workshoppresentationen (HTML + PDF). Bläddra med ← → och tryck F för helskärm | – |

## Kom igång (ca 20 minuter)

**Du behöver:**

1. **Multica**: ladda ner Desktop-appen från <https://multica.ai/download> och logga in.
   Appen startar en lokal *daemon* som kör agenterna på din dator.
2. **Ett AI-kodverktyg som du redan är inloggad i**, till exempel Claude Code (`claude`), Codex (`codex`),
   GitHub Copilot CLI (`copilot`), Cursor Agent (`cursor-agent`) eller OpenCode (`opencode`).
   Starta verktyget en gång i terminalen och logga in. Multica hittar det sedan automatiskt.
   I Multica kallas kombinationen *dator + verktyg* för en **runtime**.
3. **Multica CLI** (för setup-skriptet): `brew install multica-ai/tap/multica`, sedan `multica setup`.
   Har du bara Desktop-appen kan du göra allt för hand via [setup/MANUELL-SETUP.md](setup/MANUELL-SETUP.md).

**Sedan:**

```bash
git clone <det här repot> && cd <repot>
./setup/setup.sh            # skapar skills, agenter, projekt och demo-uppdrag
```

Kör `DRY_RUN=1 ./setup/setup.sh` först om du bara vill se vilka kommandon som körs.

Till sist bygger du tavlan, alltså kolumnerna och vem som tar över i varje steg, i appen enligt
[setup/WORKFLOW.md](setup/WORKFLOW.md). Det tar ungefär fem minuter.

Kör sedan demo-uppdragen i den ordning som [setup/DEMO-MANUS.md](setup/DEMO-MANUS.md) beskriver.

## Gör om det till din egen fabrik

Allt som är specifikt för supportartiklar ligger i fyra filer. Byt ut dem och behåll strukturen:

1. **Underlaget:** lägg dina egna källor i `underlag/`.
2. **Regelboken:** vad gäller hos er? Skriv om `regelbok/REGELBOK.md`.
3. **Arbetet:** skriv om `skills/skriv-artikel/` till ert arbetsmoment, till exempel
   "skriv offertsvar", "sammanfatta remiss" eller "implementera ärende".
4. **Kontrollen:** skriv om `skills/granska/references/checklista.md` och kontrollskriptet.

Agenterna *Intag* och *Granskare* fungerar nästan oförändrade för de flesta typer av arbete.
Det är medvetet: att validera in och validera ut är generiska förmågor.

**En mjukvarufabrik** är samma sak: Skribenten blir *Utvecklare*, underlaget blir kodbasen
och ärendet, och kontrollskriptet blir testsviten. Tavlan ser likadan ut.

**En bensinautomat** är också samma sak. Se [`bensinautomaten/`](bensinautomaten/): varje ärende är en
tankning. Kortterminalen validerar in, pumpen gör arbetet och kassan validerar ut. Där räknar ett skript
alla pengar, och en människa kommer bara in vid avvikelser.

## Säkerhet: läs detta innan du kör

- Agenterna kör **på din dator med dina behörigheter**. Multica startar till exempel Claude Code
  utan behörighetsfrågor. Låt agenterna arbeta i den här mappen och använd bara fiktiv data.
- Ärendetexter och kommentarer lagras i Multicas molntjänst om du inte kör Multica på egen server.
  Lägg **inga** kunduppgifter, personuppgifter eller affärshemligheter i en workshopmiljö.
- Lägg aldrig lösenord eller API-nycklar i agenternas miljövariabler. De lagras i klartext.
- Använd gärna en **egen workspace** för workshopen, så att regelboken inte påverkar annat.
