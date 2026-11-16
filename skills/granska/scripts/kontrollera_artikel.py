#!/usr/bin/env python3
"""Deterministisk kontroll av en hjälpartikel (Validera ut).

Modellen är stokastisk – det här skriptet är det inte. Samma artikel ger
alltid samma resultat.

Användning:
    python3 kontrollera_artikel.py leveranser/SUP-1-artikel.md [--underlag underlag] [--max-ord 250]

Avslutas med kod 0 om allt är OK, annars 1.
"""
import argparse
import os
import re
import sys

OBLIGATORISKA = ["Sammanfattning", "Så gör du", "Källor"]
TILLATNA = OBLIGATORISKA + ["Bra att veta"]
FORBJUDNA = [
    r"garanterar", r"garanterat", r"100\s?%", r"alltid", r"aldrig fel",
    r"enkelt", r"bara att", r"revolutionerande",
]
EPOST = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


def kontrollera(text: str, underlag: str, max_ord: int):
    resultat = []  # (ok, beskrivning)
    rader = text.splitlines()

    # 1. Huvudrubrik
    h1 = [r for r in rader if r.startswith("# ")]
    resultat.append((len(h1) == 1, f"Exakt en huvudrubrik (#) – hittade {len(h1)}"))

    # 2. Avsnittsrubriker i rätt ordning
    h2 = [r[3:].strip() for r in rader if r.startswith("## ")]
    okanda = [h for h in h2 if h not in TILLATNA]
    resultat.append((not okanda, "Bara tillåtna avsnitt" + (f" – okända: {okanda}" if okanda else "")))
    saknas = [h for h in OBLIGATORISKA if h not in h2]
    resultat.append((not saknas, "Obligatoriska avsnitt finns" + (f" – saknas: {saknas}" if saknas else "")))
    ordning = [h for h in h2 if h in OBLIGATORISKA]
    resultat.append((ordning == [h for h in OBLIGATORISKA if h in ordning],
                     "Avsnitten står i rätt ordning (Sammanfattning → Så gör du → Källor)"))

    # 3. Numrerade steg under "Så gör du"
    steg = avsnitt(rader, "Så gör du")
    numrerade = [r for r in steg if re.match(r"^\s*\d+\.\s", r)]
    resultat.append((len(numrerade) >= 2, f"Minst två numrerade steg under 'Så gör du' – hittade {len(numrerade)}"))

    # 4. Längd
    antal_ord = len(re.findall(r"\w+", text))
    resultat.append((antal_ord <= max_ord, f"Högst {max_ord} ord – artikeln har {antal_ord}"))

    # 5. Förbjudna ord (källistan undantas inte – den ska inte innehålla sådana ord heller)
    traffar = sorted({m.group(0) for p in FORBJUDNA for m in re.finditer(rf"(?<!\w){p}(?!\w)", text, re.IGNORECASE)})
    resultat.append((not traffar, "Inga förbjudna ord" + (f" – hittade: {traffar}" if traffar else "")))

    # 6. Personuppgifter (enkel kontroll)
    epost = EPOST.findall(text)
    resultat.append((not epost, "Inga e-postadresser" + (f" – hittade: {epost}" if epost else "")))

    # 7. Källor finns och pekar på riktiga filer
    kallor = [r.strip().lstrip("-* ").strip("`") for r in avsnitt(rader, "Källor") if r.strip().startswith(("-", "*"))]
    resultat.append((len(kallor) >= 1, f"Minst en källa listad – hittade {len(kallor)}"))
    for k in kallor:
        sokvag = k if os.path.isabs(k) or k.startswith(underlag) else os.path.join(underlag, os.path.basename(k))
        resultat.append((os.path.isfile(sokvag), f"Källan finns: {k}"))

    return resultat


def avsnitt(rader, rubrik):
    """Returnerar raderna under '## rubrik' fram till nästa rubrik."""
    ut, inne = [], False
    for r in rader:
        if r.startswith("## ") or r.startswith("# "):
            inne = r[3:].strip() == rubrik
            continue
        if inne:
            ut.append(r)
    return ut


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("artikel")
    p.add_argument("--underlag", default="underlag")
    p.add_argument("--max-ord", type=int, default=250)
    a = p.parse_args()

    if not os.path.isfile(a.artikel):
        print(f"❌ Hittar inte artikeln: {a.artikel}")
        return 1

    with open(a.artikel, encoding="utf-8") as f:
        text = f.read()

    resultat = kontrollera(text, a.underlag, a.max_ord)
    for ok, besk in resultat:
        print(("✅ " if ok else "❌ ") + besk)
    fel = sum(1 for ok, _ in resultat if not ok)
    print(f"\nMaskinkontroll: {'alla OK' if fel == 0 else f'{fel} fel'}")
    return 0 if fel == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
