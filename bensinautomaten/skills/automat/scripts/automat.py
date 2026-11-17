#!/usr/bin/env python3
"""Bensinautomatens maskinvara – simulerad och deterministisk.

Agenterna fattar beslut och skriver kommentarer. Allt som rör kort, PIN, pengar och
liter görs av det här skriptet. En språkmodell ska aldrig räkna pengar.

    python3 automat.py kort        <ÄRENDE> --kort TEST-4242 --pin "fel, korrekt"
    python3 automat.py reservera   <ÄRENDE> [--belopp 1500]
    python3 automat.py tanka       <ÄRENDE> --bransle "Bensin 95" --liter 40 [--avbrott-vid 12.4]
    python3 automat.py erbjud      <ÄRENDE>            ryms spolarvätska i reservationen?
    python3 automat.py spolarvatska <ÄRENDE> ja|nej
    python3 automat.py avsluta     <ÄRENDE> [--trots-avbrott]
    python3 automat.py hav         <ÄRENDE>            häv hela reservationen (människans beslut)
    python3 automat.py status      <ÄRENDE>
    python3 automat.py oppna                           öppna reservationer
    python3 automat.py kontrollera-text < arende.txt   letar kortnummer och PIN-koder i text
    python3 automat.py nollstall --ja                  tömmer tillstånd och kvitton (bara för människor)

Utfallet står alltid på sista raden: RESULTAT: <GODKÄNT|NEKAT|KLART|AVVIKELSE|...> – <skäl>
Exit-kod: 0 = gick bra, 1 = nekat/regel stoppade, 2 = avvikelse som ska eskaleras, 3 = fel användning.

Data läses från <rot>/underlag/ och tillstånd sparas i <rot>/tillstand/. Kvitton skrivs till
<rot>/kvitton/. Roten är --rot, annars $BENSIN_ROT, annars aktuell mapp om den har underlag/,
annars bensinautomaten-mappen som skriptet ligger i.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

PIN_TAK = 3


# ---------------------------------------------------------------- hjälpare
def hitta_rot(arg):
    for kandidat in (arg, os.environ.get("BENSIN_ROT"), os.getcwd(), os.path.join(os.getcwd(), "bensinautomaten")):
        if kandidat and (Path(kandidat) / "underlag" / "kortregister.json").exists():
            return Path(kandidat).resolve()
    standard = Path(__file__).resolve().parents[3]
    if (standard / "underlag" / "kortregister.json").exists():
        return standard
    sys.exit("Hittar inte underlag/kortregister.json. Kör från bensinautomaten-mappen eller ange --rot.")


def kr(ore):
    """12345 öre -> '123,45'; 150000 -> '1 500,00'."""
    tecken = "-" if ore < 0 else ""
    ore = abs(ore)
    heltal = f"{ore // 100:,}".replace(",", " ")
    return f"{tecken}{heltal},{ore % 100:02d}"


def liter(cl):
    return f"{cl // 100},{cl % 100:02d}"


def till_ore(kronor):
    return int(round(float(kronor) * 100))


def maskera(kort):
    return "**** " + kort[-4:]


def resultat(utfall, skal, kod):
    print(f"RESULTAT: {utfall} – {skal}")
    sys.exit(kod)


class Automat:
    def __init__(self, rot):
        self.rot = rot
        self.tillstand = rot / "tillstand"
        self.kvitton = rot / "kvitton"
        self.priser = json.loads((rot / "underlag" / "prislista.json").read_text(encoding="utf-8"))
        self.register = json.loads((rot / "underlag" / "kortregister.json").read_text(encoding="utf-8"))["kort"]

    # -- lagring
    def _fil(self, arende):
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,40}", arende):
            resultat("FEL", f"ogiltigt ärende-ID '{arende}'", 3)
        return self.tillstand / f"{arende}.json"

    def las(self, arende, krav=True):
        f = self._fil(arende)
        if not f.exists():
            if krav:
                resultat("FEL", f"{arende} har ingen tankning. Börja med kommandot 'kort'.", 3)
            return {"arende": arende, "logg": []}
        return json.loads(f.read_text(encoding="utf-8"))

    def spara(self, t, handelse):
        self.tillstand.mkdir(exist_ok=True)
        t["logg"].append({"tid": dt.datetime.now().isoformat(timespec="seconds"), "handelse": handelse})
        self._fil(t["arende"]).write_text(json.dumps(t, ensure_ascii=False, indent=2), encoding="utf-8")

    def kortstatus(self):
        f = self.tillstand / "kort.json"
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}

    def spara_kortstatus(self, s):
        self.tillstand.mkdir(exist_ok=True)
        (self.tillstand / "kort.json").write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")

    def alla(self):
        if not self.tillstand.exists():
            return []
        return [json.loads(f.read_text(encoding="utf-8")) for f in sorted(self.tillstand.glob("*.json"))
                if f.name != "kort.json"]

    # -- belopp
    def pris(self, bransle):
        for namn, pris in self.priser["bransle_kr_per_liter"].items():
            if bransle.strip().lower() in (namn.lower(), namn.split()[-1].lower()):
                return namn, till_ore(pris)
        giltiga = ", ".join(self.priser["bransle_kr_per_liter"])
        resultat("NEKAT", f"okänt bränsle '{bransle}'. Giltiga: {giltiga}", 1)

    def spolarvatska_pris(self):
        namn, pris = next(iter(self.priser["tillval"].items()))
        return namn, till_ore(pris)

    def summa(self, t):
        s = t.get("tankat", {}).get("belopp_ore", 0)
        if t.get("spolarvatska") == "ja":
            s += self.spolarvatska_pris()[1]
        return s

    def utrymme(self, t):
        return t["reservation_ore"] - self.summa(t)


# ---------------------------------------------------------------- kommandon
def cmd_kort(a, m):
    t = m.las(a.arende, krav=False)
    if t.get("kort"):
        print(f"Kortet är redan kontrollerat för {a.arende}: {maskera(t['kort'])}.")
        resultat("GODKÄNT", "redan kontrollerat tidigare", 0)
    kort = a.kort.strip().upper()
    info = m.register.get(kort)
    if info is None:
        resultat("NEKAT", "kortet finns inte i kortregistret", 1)
    status = m.kortstatus()
    ks = status.setdefault(kort, {"fel_i_rad": 0, "sparrat": False})
    print(f"Kort: {maskera(kort)}")
    if info["status"] != "giltigt" or ks["sparrat"]:
        resultat("NEKAT", "kortet är spärrat", 1)
    if info["giltigt_till"] < dt.date.today().strftime("%Y-%m"):
        resultat("NEKAT", f"kortet gick ut {info['giltigt_till']}", 1)

    forsok = [f.strip().lower() for f in re.split(r"[,;]", a.pin) if f.strip()]
    if not forsok or any(f not in ("korrekt", "ok", "fel") for f in forsok):
        resultat("FEL", "--pin ska vara en lista med 'korrekt' eller 'fel', t.ex. \"fel, korrekt\"", 3)
    for nr, f in enumerate(forsok, 1):
        if f in ("korrekt", "ok"):
            ks["fel_i_rad"] = 0
            print(f"PIN-försök {nr}: korrekt")
            m.spara_kortstatus(status)
            t["kort"] = kort
            m.spara(t, f"kort {maskera(kort)} godkänt efter {nr} PIN-försök")
            resultat("GODKÄNT", f"PIN korrekt vid försök {nr}", 0)
        ks["fel_i_rad"] += 1
        print(f"PIN-försök {nr}: fel ({ks['fel_i_rad']} av {PIN_TAK} i rad)")
        if ks["fel_i_rad"] >= PIN_TAK:
            ks["sparrat"] = True
            m.spara_kortstatus(status)
            resultat("NEKAT", f"{PIN_TAK} fel PIN i rad – kortet är nu spärrat", 1)
    m.spara_kortstatus(status)
    resultat("NEKAT", "ingen korrekt PIN angavs", 1)


def cmd_reservera(a, m):
    t = m.las(a.arende)
    if "reservation_ore" in t:
        print(f"Reservation finns redan: {kr(t['reservation_ore'])} kr.")
        resultat("GODKÄNT", "redan reserverat tidigare", 0)
    if not t.get("kort"):
        resultat("NEKAT", "kortet är inte godkänt", 1)
    tak = till_ore(m.priser["max_reservation_kr"])
    belopp = till_ore(a.belopp) if a.belopp is not None else tak
    if belopp <= 0 or belopp > tak:
        resultat("NEKAT", f"belopp {kr(belopp)} kr är utanför 0–{kr(tak)} kr", 1)
    upptaget = sum(x["reservation_ore"] for x in m.alla()
                   if x.get("kort") == t["kort"] and x.get("status") == "reserverat" and x["arende"] != t["arende"])
    disponibelt = till_ore(m.register[t["kort"]]["disponibelt_kr"]) - upptaget
    print(f"Disponibelt på kortet: {kr(disponibelt)} kr")
    if disponibelt < belopp:
        resultat("NEKAT", f"täckning saknas för reservation på {kr(belopp)} kr", 1)
    t.update(reservation_ore=belopp, status="reserverat")
    m.spara(t, f"reserverat {kr(belopp)} kr")
    resultat("GODKÄNT", f"{kr(belopp)} kr reserverat – pumpen kan starta", 0)


def cmd_tanka(a, m):
    t = m.las(a.arende)
    if "tankat" in t:
        x = t["tankat"]
        print(f"Redan tankat: {liter(x['cl'])} l {x['bransle']} för {kr(x['belopp_ore'])} kr.")
        resultat("AVVIKELSE" if x.get("avbrott") else "KLART", "tankningen är redan gjord", 2 if x.get("avbrott") else 0)
    if t.get("status") != "reserverat":
        resultat("NEKAT", "ingen reservation – pumpen får inte starta", 1)
    namn, pris = m.pris(a.bransle)
    onskat_cl = int(round(float(a.liter) * 100))
    max_cl = t["reservation_ore"] * 100 // pris
    while round(max_cl * pris / 100) > t["reservation_ore"]:
        max_cl -= 1
    cl, stopp = onskat_cl, None
    if cl > max_cl:
        cl, stopp = max_cl, "reservationen är nådd"
    avbrott = None
    if a.avbrott_vid is not None:
        avbrott_cl = int(round(float(a.avbrott_vid) * 100))
        if avbrott_cl < cl:
            cl, avbrott = avbrott_cl, f"pumpen stannade vid {liter(avbrott_cl)} l"
    belopp = int(round(cl * pris / 100))
    t["tankat"] = {"bransle": namn, "pris_ore": pris, "cl": cl, "belopp_ore": belopp,
                   "onskat_cl": onskat_cl, "stopp": stopp, "avbrott": avbrott}
    m.spara(t, f"tankat {liter(cl)} l {namn} = {kr(belopp)} kr" + (f" ({avbrott or stopp})" if avbrott or stopp else ""))
    print(f"{namn}: {liter(cl)} l × {kr(pris)} kr/l = {kr(belopp)} kr")
    if stopp:
        print(f"Kunden ville ha {liter(onskat_cl)} l – pumpen stoppade: {stopp}.")
    if avbrott:
        resultat("AVVIKELSE", avbrott + ". Eskalera till stationsföreståndaren.", 2)
    resultat("KLART", f"{liter(cl)} l tankat, kvar i reservationen {kr(m.utrymme(t))} kr", 0)


def cmd_erbjud(a, m):
    t = m.las(a.arende)
    if "tankat" not in t:
        resultat("NEKAT", "tanka först", 1)
    namn, pris = m.spolarvatska_pris()
    if t.get("spolarvatska"):
        resultat("ERBJUD INTE", f"kunden har redan svarat '{t['spolarvatska']}' – vi frågar inte igen", 1)
    if t["tankat"].get("avbrott"):
        resultat("ERBJUD INTE", "tankningen avbröts", 1)
    if m.utrymme(t) < pris:
        resultat("ERBJUD INTE", f"{namn} ({kr(pris)} kr) ryms inte – {kr(m.utrymme(t))} kr kvar i reservationen", 1)
    resultat("ERBJUD", f"{namn} för {kr(pris)} kr ryms i reservationen", 0)


def cmd_spolarvatska(a, m):
    t = m.las(a.arende)
    svar = a.svar.lower()
    if "tankat" not in t:
        resultat("NEKAT", "tanka först", 1)
    if t.get("spolarvatska"):
        kod = 0 if t["spolarvatska"] == svar else 1
        resultat("KLART" if kod == 0 else "NEKAT", f"svaret '{t['spolarvatska']}' är redan registrerat och ändras inte", kod)
    namn, pris = m.spolarvatska_pris()
    if svar == "ja" and m.utrymme(t) < pris:
        t["spolarvatska"] = "nej"
        m.spara(t, "spolarvätska nekad – ryms inte i reservationen")
        resultat("NEKAT", f"{namn} ryms inte i reservationen – registrerat som nej", 1)
    t["spolarvatska"] = svar
    m.spara(t, f"spolarvätska: {svar}")
    resultat("KLART", f"spolarvätska: {svar}", 0)


def skriv_kvitto(m, t, rubrik_rader):
    namn_sv, pris_sv = m.spolarvatska_pris()
    b = 38
    rad = lambda v, h="": f"{v:<{b - len(h)}}{h}" if h else v
    streck = "-" * b
    ut = ["BENSINAUTOMATEN · STATION 7".center(b), "Exempelvägen 1, Exempelstad".center(b), streck,
          rad("Ärende", t["arende"]), rad("Datum", dt.datetime.now().strftime("%Y-%m-%d %H:%M")),
          rad("Kort", maskera(t["kort"])), streck]
    ut += rubrik_rader(rad, namn_sv, pris_sv)
    ut += ["Tack och välkommen åter!".center(b), ""]
    m.kvitton.mkdir(exist_ok=True)
    fil = m.kvitton / f"{t['arende']}.txt"
    fil.write_text("\n".join(ut), encoding="utf-8")
    print("\n".join(ut))
    return fil


def cmd_avsluta(a, m):
    t = m.las(a.arende)
    if t.get("status") in ("avslutat", "hävt"):
        print((m.kvitton / f"{t['arende']}.txt").read_text(encoding="utf-8"))
        resultat("KLART", f"tankningen är redan {t['status']}", 0)
    if "tankat" not in t:
        resultat("NEKAT", "ingen tankning att avsluta", 1)
    x = t["tankat"]
    if x.get("avbrott") and not a.trots_avbrott:
        resultat("AVVIKELSE", f"{x['avbrott']}. En människa avgör: avsluta --trots-avbrott eller hav.", 2)
    if not t.get("spolarvatska"):
        if m.utrymme(t) >= m.spolarvatska_pris()[1] and not x.get("avbrott"):
            resultat("NEKAT", "kundens svar om spolarvätska saknas. Registrera med 'spolarvatska ja|nej' först.", 1)
        t["spolarvatska"] = "nej"
    total = m.summa(t)
    if total > t["reservation_ore"]:
        resultat("AVVIKELSE", f"summan {kr(total)} kr överstiger reservationen {kr(t['reservation_ore'])} kr", 2)
    hav = t["reservation_ore"] - total
    moms = total - int(round(total / (1 + m.priser["moms_procent"] / 100)))

    def rader(rad, namn_sv, pris_sv):
        r = [rad(f"{x['bransle']} {liter(x['cl'])} l × {kr(x['pris_ore'])}", kr(x["belopp_ore"]))]
        if t["spolarvatska"] == "ja":
            r.append(rad(namn_sv, kr(pris_sv)))
        if x.get("avbrott"):
            r.append(f"OBS: {x['avbrott']}")
        return r + ["-" * 38, rad("ATT BETALA", kr(total)), rad(f"  varav moms {m.priser['moms_procent']} %", kr(moms)),
                    rad("Reserverat", kr(t["reservation_ore"])), rad("Hävt", kr(hav)), "-" * 38]

    t.update(status="avslutat", debiterat_ore=total, havt_ore=hav)
    fil = skriv_kvitto(m, t, rader)
    m.spara(t, f"avslutat: debiterat {kr(total)} kr, hävt {kr(hav)} kr")
    resultat("KLART", f"debiterat {kr(total)} kr, hävt {kr(hav)} kr, kvitto {fil.relative_to(m.rot)}", 0)


def cmd_hav(a, m):
    t = m.las(a.arende)
    if t.get("status") != "reserverat":
        resultat("NEKAT", f"inget öppet att häva (status: {t.get('status', 'ingen reservation')})", 1)

    def rader(rad, *_):
        return ["INGEN DEBITERING", rad("Reserverat", kr(t["reservation_ore"])),
                rad("Hävt", kr(t["reservation_ore"])), "-" * 38]

    t.update(status="hävt", debiterat_ore=0, havt_ore=t["reservation_ore"])
    fil = skriv_kvitto(m, t, rader)
    m.spara(t, f"hela reservationen hävd ({kr(t['reservation_ore'])} kr)")
    resultat("KLART", f"hela reservationen hävd, kvitto {fil.relative_to(m.rot)}", 0)


def cmd_status(a, m):
    t = m.las(a.arende)
    print(json.dumps({k: v for k, v in t.items() if k != "logg"}, ensure_ascii=False, indent=2))
    for h in t["logg"]:
        print(f"  {h['tid']}  {h['handelse']}")
    resultat("STATUS", t.get("status", "kort kontrollerat"), 0)


def cmd_oppna(a, m):
    oppna = [t for t in m.alla() if t.get("status") == "reserverat"]
    for t in oppna:
        print(f"{t['arende']:<12} {maskera(t['kort'])}  {kr(t['reservation_ore']):>10} kr")
    resultat("STATUS", f"{len(oppna)} öppna reservationer", 0)


def luhn(siffror):
    s, alt = 0, False
    for c in reversed(siffror):
        d = int(c) * (2 if alt else 1)
        s += d - 9 if d > 9 else d
        alt = not alt
    return s % 10 == 0


def cmd_kontrollera_text(a, m):
    text = sys.stdin.read()
    fynd = []
    for match in re.finditer(r"(?:\d[ -]?){13,19}", text):
        siffror = re.sub(r"\D", "", match.group())
        if 13 <= len(siffror) <= 19 and luhn(siffror):
            fynd.append(f"möjligt kortnummer som slutar på {siffror[-4:]}")
    if re.search(r"(?i)\b(pin|pinkod|pin-kod)\b[^\n\d]{0,20}\d{4,6}\b", text):
        fynd.append("möjlig PIN-kod")
    if fynd:
        resultat("STOPP", "; ".join(fynd) + ". Upprepa aldrig värdet. Eskalera.", 2)
    resultat("GODKÄNT", "inga kortnummer eller PIN-koder i texten", 0)


def cmd_nollstall(a, m):
    if not a.ja:
        resultat("FEL", "lägg till --ja. Kommandot raderar alla tankningar och kvitton.", 3)
    n = 0
    for mapp, monster in ((m.tillstand, "*.json"), (m.kvitton, "*.txt")):
        if mapp.exists():
            for f in mapp.glob(monster):
                f.unlink()
                n += 1
    resultat("KLART", f"{n} filer raderade", 0)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--rot")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("kort"); s.add_argument("arende"); s.add_argument("--kort", required=True); s.add_argument("--pin", required=True)
    s = sub.add_parser("reservera"); s.add_argument("arende"); s.add_argument("--belopp", type=float)
    s = sub.add_parser("tanka"); s.add_argument("arende"); s.add_argument("--bransle", required=True)
    s.add_argument("--liter", type=float, required=True); s.add_argument("--avbrott-vid", type=float)
    s = sub.add_parser("erbjud"); s.add_argument("arende")
    s = sub.add_parser("spolarvatska"); s.add_argument("arende"); s.add_argument("svar", choices=["ja", "nej"])
    s = sub.add_parser("avsluta"); s.add_argument("arende"); s.add_argument("--trots-avbrott", action="store_true")
    s = sub.add_parser("hav"); s.add_argument("arende")
    s = sub.add_parser("status"); s.add_argument("arende")
    sub.add_parser("oppna")
    sub.add_parser("kontrollera-text")
    s = sub.add_parser("nollstall"); s.add_argument("--ja", action="store_true")
    a = p.parse_args()
    m = Automat(hitta_rot(a.rot))
    globals()["cmd_" + a.cmd.replace("-", "_")](a, m)


if __name__ == "__main__":
    main()
