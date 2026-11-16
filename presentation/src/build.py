#!/usr/bin/env python3
"""Bygger presentationen genom att återanvända stil, typsnitt, logga och navigering
från en befintlig presentation i samma mall.

    python3 presentation/src/build.py <mall.html> [utfil.html]

Mallen är den befintliga HTML-presentationen (t.ex. claude-skills-agenter-juridik_4.html).
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DEFAULT = os.path.join(HERE, "..", "fabriker-med-multica.html")

FONT_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;700&display=swap" '
             'rel="stylesheet">')

GRAY ='fill="rgba(92,107,114,0.10)" stroke="#8A979D"'
WHITE = 'fill="#FFFFFF" stroke="#232323"'
FOCAL = 'fill="rgba(62,177,200,0.10)" stroke="#3EB1C8" stroke-width="2"'


def fractal_rows():
    steps = [("Uppdrag", GRAY), ("Validera in", WHITE), ("Arbetet", FOCAL),
             ("Validera ut", WHITE), ("Människa", GRAY), ("Leverans", WHITE)]
    out = ['<g font-family="Gotham,sans-serif" text-anchor="middle">']
    for y in (40, 240, 440):
        for i, (namn, stil) in enumerate(steps):
            x = 250 + i * 190
            out.append(f'<rect x="{x}" y="{y}" width="150" height="64" rx="6" {stil}/>')
            out.append(f'<text x="{x + 75}" y="{y + 38}" fill="#232323" font-size="16" font-weight="500">{namn}</text>')
            if i < len(steps) - 1:
                out.append(f'<line x1="{x + 152}" y1="{y + 32}" x2="{x + 186}" y2="{y + 32}" '
                           f'stroke="#5C6B72" stroke-width="1.5" marker-end="url(#f-arrow)"/>')
    out.append("</g>")
    return "\n  ".join(out)


def board():
    cols = [
        ("Inkorg", "ingen", "inbox"),
        ("Validera in", "agent · Intag", "agent"),
        ("Arbetet", "agent · Skribent", "agent"),
        ("Validera ut", "agent · Granskare", "focal"),
        ("Människa", "medlem · du", "human"),
        ("Levererad", "–", "inbox"),
    ]
    cards = {
        0: [("SUP-6", "Ny kundfråga", "väntar", "#5C6B72"),
            ("SUP-2", "Export till Power BI", "avvisad – komplettera", "#C2410C")],
        1: [("SUP-7", "Teams-länk", "Intag kontrollerar …", "#5C6B72")],
        2: [("SUP-4", "Startpaket", "Orkestrator · 3 sub-issues", "#5C6B72"),
            ("SUP-8", "Avboka ett tillfälle", "skriver UTKAST v1", "#5C6B72")],
        3: [("SUP-1", "Återkommande möte", "omtag 1 av 2", "#1F7488")],
        4: [("SUP-3", "Driftstopp", "ESKALERAT · regel 4–6", "#1F7488")],
        5: [("SUP-5", "Väntelistan", "✓ godkänd av människa", "#5C6B72")],
    }
    styles = {
        "inbox": 'fill="rgba(35,35,35,0.03)" stroke="rgba(35,35,35,0.18)"',
        "agent": WHITE,
        "focal": 'fill="#FFFFFF" stroke="#3EB1C8" stroke-width="2"',
        "human": GRAY,
    }
    out = ['<g font-family="Gotham,sans-serif">']
    for i, (namn, handoff, typ) in enumerate(cols):
        x = 35 + i * 224
        cx = x + 105
        out.append(f'<rect x="{x}" y="96" width="210" height="374" rx="8" fill="#F6F8F9" stroke="rgba(35,35,35,0.06)"/>')
        out.append(f'<rect x="{x}" y="20" width="210" height="64" rx="6" {styles[typ]}/>')
        out.append(f'<text x="{cx}" y="47" fill="#232323" font-size="18" font-weight="500" text-anchor="middle">{namn}</text>')
        out.append(f'<text x="{cx}" y="69" fill="#5C6B72" font-size="12" font-family="Consolas,monospace" '
                   f'letter-spacing="0.03em" text-anchor="middle">{html.escape(handoff)}</text>')
        if i < len(cols) - 1:
            out.append(f'<line x1="{x + 211}" y1="52" x2="{x + 222}" y2="52" stroke="#5C6B72" '
                       f'stroke-width="1.5" marker-end="url(#b-arrow)"/>')
        for k, (nr, titel, status, farg) in enumerate(cards.get(i, [])):
            y = 110 + k * 96
            out.append(f'<rect x="{x + 12}" y="{y}" width="186" height="82" rx="6" fill="#FFFFFF" stroke="rgba(35,35,35,0.18)"/>')
            out.append(f'<text x="{x + 24}" y="{y + 22}" fill="#1F7488" font-size="12" font-family="Consolas,monospace">{nr}</text>')
            out.append(f'<text x="{x + 24}" y="{y + 45}" fill="#232323" font-size="14" font-weight="500">{html.escape(titel)}</text>')
            out.append(f'<text x="{x + 24}" y="{y + 67}" fill="{farg}" font-size="12">{html.escape(status)}</text>')
    out.append("</g>")
    return "\n  ".join(out)


REGELNIVAER = [
    ("1 · HUMANA", "Du ska inte skada människor."),
    ("2 · LEGALA", "Du får inte skapa något som profilerar människor."),
    ("3 · ORGANISATORISKA", "Inga personuppgifter utan godkännande från CISO."),
    ("4 · ARBETE / TEAM", "ASD-STD100 (~80 %) och god svenska · diagram med skillen från diagramdesign.dev"),
]


def regelbok_i_nivaer(svg: str) -> str:
    """Byter mallens enkla regelboksruta mot fyra nästlade nivåer.

    Yttersta nivån (humana) är bredast och ligger överst. Varje nivå inåt
    smalnar av – den ärver nivån ovanför och får inte strida mot den.
    """
    start = svg.index("<!-- Regelbok (focal) -->")
    slut = svg.index("<!-- Uppdrag -->")
    x0, bredd, inset, h, y0 = 232, 896, 20, 24, 12
    ut = ['<!-- Regelbok i fyra nivåer -->',
          '<text x="40" y="34" fill="#232323" font-size="18" font-weight="500" text-anchor="start">Regelbok</text>',
          '<text x="40" y="55" fill="#5C6B72" font-size="13" text-anchor="start">gäller före, under</text>',
          '<text x="40" y="72" fill="#5C6B72" font-size="13" text-anchor="start">och efter arbetet</text>',
          '<rect x="40" y="84" width="88" height="18" rx="3" fill="#FFFFFF" stroke="#C9D2D6" stroke-width="0.8"/>'
          '<text x="84" y="97" fill="#5C6B72" font-size="11" font-family="Consolas,monospace" letter-spacing="0.03em" text-anchor="middle">guardrails</text>']
    for i, (niva, regel) in enumerate(REGELNIVAER):
        x, w, y = x0 + i * inset, bredd - 2 * i * inset, y0 + i * h
        alfa = (0.05, 0.09, 0.14, 0.20)[i]
        ut.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFFFFF"/>')
        ut.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="rgba(62,177,200,{alfa})" '
                  f'stroke="#3EB1C8" stroke-width="{1.5 if i == 0 else 0.8}"/>')
        ut.append(f'<text x="{x + 14}" y="{y + 16}" fill="#1F7488" font-size="11" font-weight="500" '
                  f'letter-spacing="0.08em" text-anchor="start">{niva}</text>')
        ut.append(f'<text x="{x0 + 3 * inset + 170}" y="{y + 16.5}" fill="#232323" font-size="13" '
                  f'text-anchor="start">{html.escape(regel)}</text>')
    ut.append(f'<text x="{x0 + bredd + 14}" y="{y0 + 16}" fill="#5C6B72" font-size="12" font-style="italic" '
              f'text-anchor="start">yttre nivå</text>')
    ut.append(f'<text x="{x0 + bredd + 14}" y="{y0 + 32}" fill="#5C6B72" font-size="12" font-style="italic" '
              f'text-anchor="start">går före inre</text>')
    svg = svg[:start] + "\n    ".join(ut) + "\n\n    " + svg[slut:]

    # Regelbokens "droppar" börjar nu under nivåerna, och en ny droppe når även Människa.
    for x, y2 in (("304", "256"), ("480", "216"), ("840", "256")):
        gammal = f'<line x1="{x}" y1="96" x2="{x}" y2="{y2}"'
        assert gammal in svg, gammal
        svg = svg.replace(gammal, f'<line x1="{x}" y1="{y0 + 4 * h}" x2="{x}" y2="{y2}"')
    svg = svg.replace(
        "<!-- main flow -->",
        f'<line x1="1048" y1="{y0 + 4 * h}" x2="1048" y2="256" stroke="#A9B4B9" stroke-width="1.2" '
        f'stroke-dasharray="2,4" marker-end="url(#p-soft)"/>\n  <!-- main flow -->', 1)
    return svg


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    mall = open(sys.argv[1], encoding="utf-8").read()
    ut = sys.argv[2] if len(sys.argv) > 2 else OUT_DEFAULT

    head = mall[: mall.index("<body>") + len("<body>")]
    head = re.sub(r"<title>.*?</title>", "<title>Fabriker med Multica</title>", head, flags=re.S)
    # Gotham är licensierat och får inte spridas med repot. Mallens inbäddade typsnitt
    # tas bort; ett lokalt installerat Gotham används om det finns, annars Montserrat.
    head, antal = re.subn(r"@font-face\{font-family:'Gotham';[^}]*\}", "", head)
    assert antal == 4, f"Väntade 4 Gotham-typsnitt i mallen, hittade {antal}"
    head = head.replace("</head>", FONT_LINK + "\n</head>", 1)
    logo = re.search(r'<img[^>]*src="(data:[^"]+)"', mall).group(1)
    tail = mall[mall.index('<div class="progress"'):]

    # Processmodellen återanvänds från mallen, generaliserad bort från "Claude".
    sek = mall[mall.index("<!-- 04 PROCESS MODEL -->"):]
    svg = sek[sek.index("<svg"): sek.index("</svg>") + len("</svg>")]
    svg = svg.replace("Claude utför stegen", "människa eller agent").replace("memo · tabell", "beslut · produkt")
    svg = svg.replace("connectors, sök", "system, API:er")
    svg = regelbok_i_nivaer(svg)

    slides = open(os.path.join(HERE, "slides.html"), encoding="utf-8").read()
    slides = (slides.replace("{{PROCESS_SVG}}", svg)
                    .replace("{{FRACTAL_ROWS}}", fractal_rows())
                    .replace("{{BOARD}}", board())
                    .replace("{{LOGO}}", logo))
    n = 1

    def foot(_):
        nonlocal n
        n += 1
        return f'<div class="foot"><img src="{logo}" alt="Sokigo"><span>{n:02d}</span></div>'

    slides = re.sub(r"\{\{FOOT\}\}", foot, slides)
    assert "{{" not in slides, "Oersatt platshållare kvar"

    doc = head + '\n<div class="deck" id="deck">\n\n' + slides + "\n</div>\n" + tail
    doc = doc.replace("font-family:'Gotham'", "font-family:'Gotham','Montserrat'")
    doc = doc.replace('font-family="Gotham,sans-serif"', 'font-family="Gotham,Montserrat,sans-serif"')
    doc = doc.replace("font-family:Gotham,sans-serif", "font-family:Gotham,Montserrat,sans-serif")
    assert "base64,T1RUTw" not in doc, "Inbäddat OTF-typsnitt kvar"
    with open(ut, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Skrev {ut} ({n} bilder)")


if __name__ == "__main__":
    main()
