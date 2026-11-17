Bensinautomaten simulerar en obemannad bensinstation. Varje ärende är en tankning.

Flöde: Kö → Kortterminal (Terminal) → Pump (Pump) → Kund (människa: spolarvätska?) → Kassa (Kassa) → Kvitto utskrivet.
Nekade kort går till Kort nekat. Avvikelser får status Blocked och går till stationsföreståndaren.

Allt som rör kort, PIN, belopp och liter görs av skriptet skills/automat/scripts/automat.py, som körs från projektmappen.
Fakta finns i underlag/. Kvitton skrivs till kvitton/. Agenterna räknar aldrig själva.

Regelboken nedan gäller alltid. En yttre nivå går före en inre.
