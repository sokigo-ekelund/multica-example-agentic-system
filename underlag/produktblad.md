# Produktblad – Bokningsportalen 2.4

> Fiktiv produkt från det fiktiva Exempelbolaget AB. Används som underlag i Supportfabriken.

Bokningsportalen är en webbtjänst för att boka mötesrum, arbetsplatser och utrustning på kontoret.
Den fungerar i webbläsaren på dator och mobil. Det finns ingen app att installera.

## Funktioner
- **Boka rum:** välj datum, tid och antal deltagare. Portalen visar vilka rum som är lediga.
- **Boka arbetsplats:** välj våningsplan på kartan och klicka på en ledig plats.
- **Boka utrustning:** projektorer, högtalare och webbkameror kan läggas till på en rumsbokning.
- **Återkommande möten:** se `funktioner.md`, avsnittet *Återkommande bokning*.
- **Avboka:** en bokning kan avbokas fram till starttiden. Se `funktioner.md`.
- **Väntelista:** ny i version 2.4. Se `release-2-4.md`.

## Integrationer
- Microsoft 365 (Outlook-kalendern)
- Google Kalender

Bokningar som görs i portalen syns i den kopplade kalendern inom 5 minuter.
Andra integrationer finns inte i dagsläget.

## Begränsningar
- En person kan ha högst 10 aktiva bokningar samtidigt.
- Rum kan bokas högst 90 dagar framåt.
- Arbetsplatser kan bokas högst 14 dagar framåt.
