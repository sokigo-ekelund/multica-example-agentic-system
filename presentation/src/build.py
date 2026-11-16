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

GRAY = 'fill="rgba(92,107,114,0.10)" stroke="#8A979D"'
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


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    mall = open(sys.argv[1], encoding="utf-8").read()
    ut = sys.argv[2] if len(sys.argv) > 2 else OUT_DEFAULT

    head = mall[: mall.index("<body>") + len("<body>")]
    head = re.sub(r"<title>.*?</title>", "<title>Fabriker med Multica</title>", head, flags=re.S)
    logo = re.search(r'<img[^>]*src="(data:[^"]+)"', mall).group(1)
    tail = mall[mall.index('<div class="progress"'):]

    # Processmodellen återanvänds från mallen, generaliserad bort från "Claude".
    sek = mall[mall.index("<!-- 04 PROCESS MODEL -->"):]
    svg = sek[sek.index("<svg"): sek.index("</svg>") + len("</svg>")]
    svg = svg.replace("Claude utför stegen", "människa eller agent").replace("memo · tabell", "beslut · produkt")
    svg = svg.replace("connectors, sök", "system, API:er")

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

    with open(ut, "w", encoding="utf-8") as f:
        f.write(head + '\n<div class="deck" id="deck">\n\n' + slides + "\n</div>\n" + tail)
    print(f"Skrev {ut} ({n} bilder)")


if __name__ == "__main__":
    main()
