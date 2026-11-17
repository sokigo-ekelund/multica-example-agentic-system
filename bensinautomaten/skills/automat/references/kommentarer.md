# Kommentarsmallar

Håll kommentarerna korta, som texten på en automatdisplay. Klistra alltid in skriptets `RESULTAT:`-rad.

## Kortterminal
```
## KORTTERMINAL: <GODKÄNT | NEKAT | STOPPAD>

| Kontroll | Resultat |
|---|---|
| Inga kortnummer eller PIN-koder i ärendet (regel 2) | ✅ / ❌ |
| Ingen fara vid pumpen (regel 1) | ✅ / ❌ |
| Uppgifter kompletta (kort, PIN-försök, bränsle, mängd) | ✅ / ❌ |
| Kort och PIN | <RESULTAT-raden> |
| Reservation | <RESULTAT-raden> |

<En mening till kunden, t.ex. "Välj bränsle och lyft munstycket." eller "Kortet nekades: täckning saknas.">
```

## Pump
```
## PUMP: <TANKAT | AVVIKELSE>

<RESULTAT-raden från tanka>

**Spolarvätska:** <fråga till kunden | erbjuds inte: skäl från erbjud>
```
Om spolarvätska erbjuds, avsluta med frågan på en egen rad:
`> 🧴 Vill du köpa spolarvätska 4 l för 89,00 kr? Svara **ja** eller **nej** i en kommentar.`
(Priset tar du från skriptets utdata.)

## Kassa
```
## KASSA: <KVITTO | AVVIKELSE>

<RESULTAT-raden från avsluta eller hav>

<kvittot inom ``` som skriptet skrev ut>
```

## Avvikelse (alla steg)
```
## AVVIKELSE – stationsföreståndaren tar över

**Vad hände:** <RESULTAT-raden>
**Reservation:** <belopp> kr är fortfarande reserverat (eller: ingen reservation)
**Svara med en av:**
- `BESLUT: debitera` – kunden betalar för det som tankats
- `BESLUT: häv` – hela reservationen hävs, ingen debitering
```
