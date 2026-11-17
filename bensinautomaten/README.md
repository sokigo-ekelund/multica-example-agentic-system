# Bensinautomaten – en "fabrik" där varje ärende är en tankning

En obemannad bensinautomat körd i Multica. Kunden sätter in kortet och slår PIN-koden. Kortet kontrolleras
och ett belopp reserveras. Pumpen tankar, kunden erbjuds spolarvätska, tankningen avslutas, det som inte
används hävs och ett kvitto skrivs ut.

Det är samma modell som [Supportfabriken](../README.md), men med en process som alla redan kan och
med pengar som måste stämma på öret.

```
Kö ──► Kortterminal ──► Pump ──► Kund ──► Kassa ──► Kvitto utskrivet
       (Terminal)       (Pump)   (du:     (Kassa)
           │                     spolar-     │
           ▼                     vätska?)    ▼
       Kort nekat                         Blocked ──► Stationsföreståndaren (du) ──BESLUT──► Kassa
```

| Steg | Agent | Rutan i modellen |
|---|---|---|
| Kortterminal | **Terminal**: kontrollerar fara, kortnummer i text, kort, PIN och reserverar belopp | Validera in |
| Pump | **Pump**: tankar inom reservationen och erbjuder spolarvätska en gång | Arbetet |
| Kund | **du**: svarar ja eller nej | Människa mitt i flödet |
| Kassa | **Kassa**: slutbelopp, hävning och kvitto | Validera ut |
| Avvikelse | **du** som stationsföreståndare: `BESLUT: häv` eller `BESLUT: debitera` | Eskalera |

## Två saker Bensinautomaten visar som Supportfabriken inte visar

1. **En språkmodell ska aldrig räkna pengar.** Allt som rör kort, PIN, liter och kronor görs av ett
   deterministiskt skript, [`skills/automat/scripts/automat.py`](skills/automat/scripts/automat.py).
   Agenterna bestämmer vad som ska göras, och skriptet gör det. Samma indata ger alltid samma kvitto.
2. **Människan finns bara vid avvikelser.** I Supportfabriken godkänner en människa varje artikel.
   Här kommer stationsföreståndaren bara in när något går fel. Var människan ska in i flödet är ett
   riskbeslut.

## Vad finns här?

| Mapp / fil | Vad det är |
|---|---|
| [`regelbok/REGELBOK.md`](regelbok/REGELBOK.md) | Regelboken i fyra nivåer: humana, legala, organisatoriska, arbete/team |
| [`agenter/`](agenter/) | Instruktioner för Terminal, Pump och Kassa |
| [`skills/automat/`](skills/automat/) | Skillen med automatskriptet och kommentarsmallar |
| [`underlag/`](underlag/) | Fiktivt kortregister (bara testkort), prislista och fakta om stationen |
| [`demo-tankningar/`](demo-tankningar/) | Sex tankningar som visar olika vägar. Facit står under strecket |
| [`kvitton/`](kvitton/) | Kvitton som skriptet skriver (git-ignorerade) |
| `tillstand/` | Skapas av skriptet: reservationer och spärrade kort (git-ignorerad) |
| [`setup/`](setup/) | Setup-skript, tavelguide och demomanus |

## Kom igång

Förutsättningarna är desamma som för Supportfabriken: Multica Desktop, ett inloggat AI-verktyg och
Multica CLI. Se [huvud-README](../README.md#kom-igång-ca-20-minuter).

```bash
./bensinautomaten/setup/setup.sh     # skill, tre agenter, projekt och sex demotankningar
```

Därefter:
1. Koppla mappen `bensinautomaten/` till projektet i läget **Edit directly**.
   Se [setup/WORKFLOW.md](setup/WORKFLOW.md#5-koppla-mappen) för varför det måste vara det läget.
2. Bygg tavlan enligt [setup/WORKFLOW.md](setup/WORKFLOW.md) (ca 5 min).
3. Kör demon enligt [setup/DEMO-MANUS.md](setup/DEMO-MANUS.md).

Prova skriptet utan Multica:

```bash
cd bensinautomaten
python3 skills/automat/scripts/automat.py kort PROV-1 --kort TEST-4242 --pin korrekt
python3 skills/automat/scripts/automat.py reservera PROV-1
python3 skills/automat/scripts/automat.py tanka PROV-1 --bransle "Bensin 95" --liter 40
python3 skills/automat/scripts/automat.py spolarvatska PROV-1 ja
python3 skills/automat/scripts/automat.py avsluta PROV-1
python3 skills/automat/scripts/automat.py nollstall --ja
```

## Testkort

| Kort | Vad som händer |
|---|---|
| `TEST-4242` | Giltigt, 5 000 kr disponibelt |
| `TEST-7777` | Giltigt, spärras efter tre fel PIN |
| `TEST-1881` | Giltigt men bara 300 kr disponibelt, så reservationen nekas |
| `TEST-2020` | Utgånget |
| `TEST-0666` | Spärrat |

PIN-koder förekommer aldrig. Ärenden anger bara utfallet av varje försök, till exempel `fel, korrekt`.
Det följer regel 2 i regelboken och gör demon säker att köra i en molntjänst.
