"""Generate fashion-flat line drawings (front + back) for the Wrap/skirt trouser
and the Flap trouser as SVG, then render to PNG with headless Chromium.

Usage: python3 scripts/line_drawings.py
Outputs: output/wrap-trouser-line.{svg,png}, output/flap-trouser-line.{svg,png}
"""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "output"
BG = "#f6f3ea"
HEAD = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 180 1024 1140" width="1024" height="1140">' \
       f'<rect y="180" width="1024" height="1140" fill="{BG}"/>'
BOLD = 'fill="none" stroke="#111" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"'
MID = 'fill="none" stroke="#222" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"'
THIN = 'fill="none" stroke="#777" stroke-width="1.1" stroke-linecap="round" opacity=".7"'
STITCH = 'fill="none" stroke="#666" stroke-width="1.2" stroke-dasharray="7 5"'


def p(d, style=BOLD):
    return f'<path d="{d}" {style}/>'


def button(x, y):
    return (f'<circle cx="{x}" cy="{y}" r="12" fill="{BG}" stroke="#111" stroke-width="2.4"/>'
            f'<circle cx="{x}" cy="{y}" r="8.5" fill="none" stroke="#111" stroke-width="1"/>'
            f'<path d="M{x-4},{y-4} L{x+4},{y+4} M{x+4},{y-4} L{x-4},{y+4}" stroke="#111" stroke-width="1.6"/>')


def wrap_front(dx=0):
    g = [f'<g transform="translate({dx},0)">']
    # silhouette: waist, right side, hem, centre gap, left side
    g.append(p("M178,255 L400,243 L402,322 C420,520 462,900 478,1232 "
               "C430,1262 340,1262 286,1246 L284,520 L283,1246 "
               "C230,1272 170,1262 135,1254 L38,1222 C90,900 150,500 178,255 Z"))
    # waistband lower edge
    g.append(p("M178,293 L395,284", MID))
    # wrap panel arch (overlap edge) from right hip to left leg, then straight to hem
    g.append(p("M402,322 C355,345 300,372 262,415 C225,460 207,520 203,600 "
               "C185,800 150,1050 135,1254"))
    g.append(p("M283,385 L284,1246", MID))                     # centre crease
    g.append(p("M262,415 C238,455 224,515 220,590", THIN))      # fold shading
    # hem stitching
    g.append(p("M52,1205 C120,1232 200,1240 280,1228", STITCH))
    g.append(p("M292,1228 C360,1240 430,1232 468,1214", STITCH))
    # drape lines
    for d in ("M250,640 C240,800 215,1000 190,1200", "M330,700 C345,900 372,1050 392,1220",
              "M90,700 C80,900 70,1050 62,1190", "M440,600 C448,800 456,1000 462,1190"):
        g.append(p(d, THIN))
    # buttons
    for x, y in ((345, 275), (378, 270), (350, 308), (382, 303)):
        g.append(button(x, y))
    g.append('</g>')
    return "".join(g)


def wrap_back(dx=0):
    g = [f'<g transform="translate({dx},0)">']
    g.append(p("M168,255 L408,255 C430,520 470,900 482,1232 C430,1262 340,1262 290,1246 "
               "L285,560 L280,1246 C225,1272 170,1262 130,1254 L34,1222 C85,900 140,500 168,255 Z"))
    # elastic waistband with gathers
    g.append(p("M168,255 C250,242 330,242 408,255 L412,312 C330,300 250,300 164,312 Z", MID))
    for x in range(184, 404, 18):
        g.append(p(f"M{x},262 C{x+3},282 {x-3},296 {x},308", THIN))
    # centre-back seam, welt pocket
    g.append(p("M287,312 L285,560", MID))
    g.append(p("M338,380 L418,378 M338,398 L418,396 M338,380 L338,398 M418,378 L418,396", MID))
    g.append(p("M52,1205 C120,1232 200,1240 276,1228", STITCH))
    g.append(p("M294,1228 C360,1240 430,1232 470,1214", STITCH))
    for d in ("M230,640 C220,800 200,1000 180,1200", "M360,640 C372,850 390,1050 405,1220"):
        g.append(p(d, THIN))
    g.append('</g>')
    return "".join(g)


def flap_front(dx=0):
    g = [f'<g transform="translate({dx},0)">']
    # silhouette (high-rise wide leg, cuffed hem)
    g.append(p("M150,250 L378,250 C396,520 440,900 470,1222 L290,1226 L264,560 "
               "L238,1226 L48,1222 C80,900 128,520 150,250 Z"))
    # waistband + belt loops
    g.append(p("M150,250 L378,250 L380,300 L150,300 Z", MID))
    for x in (172, 356):
        g.append(p(f"M{x},244 L{x},306", MID))
    # fly + button
    g.append(p("M262,300 L262,420 C262,436 280,436 290,420 L290,300", MID))
    g.append(p("M262,360 L290,360", THIN))
    # inverted pleats at waistband
    g.append(p("M205,300 C196,380 180,470 168,560", MID))
    g.append(p("M325,300 C334,380 348,470 360,560", MID))
    # side drape flaps (left & right) with pointed knee hem
    g.append(p("M150,300 C122,420 98,520 96,610 C100,640 120,650 140,628 "
               "C155,560 175,460 205,300", MID))
    g.append(p("M378,300 C406,420 430,520 432,610 C428,640 408,650 388,628 "
               "C373,560 353,460 325,300", MID))
    # diagonal seam from flap tip to hem
    g.append(p("M140,628 C165,800 195,930 222,1060", THIN))
    g.append(p("M388,628 C363,800 333,930 306,1060", THIN))
    # side pockets (slant, hidden under flap)
    g.append(p("M205,300 C215,360 225,400 232,430", THIN))
    g.append(p("M325,300 C315,360 305,400 298,430", THIN))
    # cuffs + pinstripe hints
    g.append(p("M52,1180 L236,1184 M292,1184 L466,1180", MID))
    for x in range(190, 345, 22):
        g.append(p(f"M{x},470 L{x-4},1150", THIN))
    g.append('</g>')
    return "".join(g)


def flap_back(dx=0):
    g = [f'<g transform="translate({dx},0)">']
    g.append(p("M150,250 L378,250 C396,520 440,900 470,1222 L290,1226 L264,560 "
               "L238,1226 L48,1222 C80,900 128,520 150,250 Z"))
    g.append(p("M150,250 L378,250 L380,300 L150,300 Z", MID))
    for x in (172, 356):
        g.append(p(f"M{x},244 L{x},306", MID))
    g.append(p("M264,300 L264,560", MID))
    # back darts
    g.append(p("M200,300 C204,360 208,400 214,440 M328,300 C324,360 320,400 314,440", MID))
    g.append(p("M52,1180 L236,1184 M292,1184 L466,1180", MID))
    for x in range(180, 360, 24):
        g.append(p(f"M{x},470 L{x-4},1150", THIN))
    g.append('</g>')
    return "".join(g)


def build(name, front, back):
    svg = HEAD + front(0) + back(500) + "</svg>"
    # shrink both garments into the 1024 canvas side by side
    svg = svg.replace('<rect y="180" width="1024" height="1140"', '<rect y="180" width="1024" height="1140"', 1)
    OUT.mkdir(exist_ok=True)
    (OUT / f"{name}.svg").write_text(svg)
    return OUT / f"{name}.svg"


def render(svg_path):
    import subprocess
    subprocess.run(["/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--disable-gpu",
                    "--hide-scrollbars", "--window-size=1024,1400",
                    f"--screenshot={svg_path.with_suffix('.png')}", svg_path.as_uri()],
                   check=True, capture_output=True)
    from PIL import Image
    png = svg_path.with_suffix(".png")
    Image.open(png).crop((0, 0, 1024, 1140)).save(png)


if __name__ == "__main__":
    for name, f, b in (("wrap-trouser-line", wrap_front, wrap_back),
                       ("flap-trouser-line", flap_front, flap_back)):
        render(build(name, f, b))
