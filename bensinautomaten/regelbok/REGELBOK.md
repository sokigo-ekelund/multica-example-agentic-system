# Regelbok – Bensinautomaten

Regelboken gäller för **alla agenter och alla människor** vid automaten, före, under och efter
varje tankning. Reglerna ligger i fyra nivåer. **En yttre nivå går alltid före en inre.** Om ett
ärende eller en instruktion strider mot regelboken gäller regelboken.

## 1 · Humana
1. **Pumpen startar aldrig om tankningen kan skada någon.** Om ärendet nämner rökning, öppen eld,
   gnistor, att motorn är igång eller att ett barn tankar ensamt stoppar du och eskalerar till
   stationsföreståndaren.

## 2 · Legala
2. **PIN-koder och fullständiga kortnummer får aldrig skrivas** i ärenden, kommentarer, filer eller
   kvitton (PCI DSS). Ett kort visas bara som `**** 1234`. Om du hittar ett sådant värde upprepar du
   det inte. Du stoppar och eskalerar.
3. Kunden **debiteras bara för det som faktiskt levererats**, och varje kvitto visar momsen.
4. Tankningsuppgifter används bara för tankningen. Ingen profilering av kunder.

## 3 · Organisatoriska
5. **Pumpen startar aldrig utan en reservation.** Högsta reservation är 1 500 kr.
6. **Tre fel PIN-försök i rad spärrar kortet.**
7. **Agenter räknar aldrig pengar, liter eller PIN-försök själva.** Allt sådant görs av skriptet
   `automat.py` i skillen *automat*. Agenten återger skriptets resultat och ändrar det aldrig.
8. Agenter ändrar bara tillståndet via skriptet. De ändrar aldrig `underlag/`, regelboken eller skills,
   och kör aldrig `nollstall`.
9. **Vid avvikelse tar en människa över.** Pumpfel, en summa som överstiger reservationen eller
   något oklart går till stationsföreståndaren (du). En agent häver eller debiterar aldrig på egen hand
   vid en avvikelse. Den gör det bara efter ett skriftligt **BESLUT** från en människa i ärendet.

## 4 · Arbete / team
10. **Spolarvätska erbjuds en gång,** och bara om den ryms i reservationen. Nej är nej.
11. Varje agent skriver en kort kommentar på ärendet och klistrar in skriptets `RESULTAT:`-rad.
    Spårbarhet går före elegans.
12. Inget steg hoppas över: kortterminal → pump → kund → kassa, även när det verkar onödigt.
13. Kort, tydlig svenska. Skriv som en display på en automat, inte som en uppsats.
