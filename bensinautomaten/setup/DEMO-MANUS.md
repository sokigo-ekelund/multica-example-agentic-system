# Demomanus: Bensinautomaten (ca 25 min)

> **Nollställ före varje genrep:** `python3 skills/automat/scripts/automat.py nollstall --ja`
> (från mappen `bensinautomaten/`). Annars är kort 7777 fortfarande spärrat från förra gången.
> Facit för varje tankning står under strecket i filerna i `demo-tankningar/`.

## 0. Varför en bensinautomat? (2 min)
- Alla vet hur den fungerar, så ingen behöver förstå domänen. Alla ser direkt när något går fel.
- Samma modell som Supportfabriken: kortterminal = *validera in*, pump = *arbetet*,
  kassa = *validera ut*, kvitto = *leverans*.
- Visa regelboken i fyra nivåer i projektbeskrivningen.

## 1. Vanlig tankning: `Tankning: 40 l Bensin 95, kort 4242` (6 min)
1. Dra ärendet från *Kö* till *Kortterminal*. Visa kontrolltabellen och `1 500,00 kr reserverat`.
2. Pumpen tankar 40,00 l och **frågar om spolarvätska**. Ärendet hamnar hos dig i *Kund*.
3. Svara `ja` och markera steget som klart. Kassan skriver kvittot: 828,60 kr, och 671,40 kr hävs.
4. Visa filen `kvitton/<ärende>.txt`.

**Poäng:** ingen agent har räknat ett enda öre. Det gör `automat.py`. **En språkmodell ska aldrig
räkna pengar.** Den bestämmer vad som ska göras, och ett deterministiskt verktyg gör det.

## 2. Fel PIN tre gånger: `Tankning: fel PIN tre gånger, kort 7777` (3 min)
Kortterminalen nekar och kortet spärras. Ärendet går till *Kort nekat*, och pumpen startar aldrig.

**Bonus:** skapa en ny tankning med samma kort och `PIN-försök: korrekt`. Den nekas också, eftersom
automaten minns. Det är därför mappen måste köras i läget *Edit directly*.

## 3. Täckning saknas: `Tankning: täckning saknas, kort 1881` (2 min)
PIN är rätt vid andra försöket, men reservationen nekas. **Poäng:** validera in är fler kontroller än en.

## 4. Fulltank över gränsen: `Tankning: fulltank Diesel, kort 4242` (4 min)
Pumpen stoppar vid 77,76 l = 1 499,99 kr. Spolarvätska erbjuds inte, eftersom bara 0,01 kr finns kvar.
I *Kund* markerar du bara steget som klart.

**Poäng:** regel 5 (organisatorisk) och regel 10 (team) hålls av skriptet, inte av agentens goda vilja.

## 5. Pumpfel: `Tankning: pumpfel mitt i, kort 4242` (5 min)
1. Pumpen stannar vid 12,40 l. Ärendet blir **Blocked** och du blir @-nämnd.
2. Skriv `BESLUT: häv` och flytta ärendet till *Kassa*. Kassan häver 1 500 kr och skriver ett kvitto
   utan debitering.

**Poäng:** människan finns bara vid avvikelser. Agenten verkställer, men människan beslutar.

## 6. Rökning: `Tankning: kunden röker vid pumpen, kort 4242` (3 min)
Kortterminalen stoppar **innan kortet läses**. Den humana nivån går före allt annat.

**Övning till publiken:** skriv en egen tankning där någon har skrivit in en PIN-kod i ärendet
(till exempel "PIN 1234"). Vad händer? Kortterminalen kör `kontrollera-text`, stoppar och upprepar
aldrig värdet. Det är den legala nivån.

## Avslutning
- Supportfabriken och Bensinautomaten har **samma tavla men olika risker**. Därför sitter människan på
  olika ställen.
- Det deterministiska skriptet är bensinautomatens viktigaste del. Fråga publiken: vilket "kontrollskript"
  skulle er fabrik behöva?
