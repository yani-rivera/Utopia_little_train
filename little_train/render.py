"""Fill the page template: land, one or more lines with their stations and trains, labels."""
import json
from html import escape
from pathlib import Path

from . import __project__, __version__
from .geo import ring_path
from .route import smooth_path, line_path
from . import trains

TEMPLATE = Path(__file__).with_name("template.html")


def stations_svg(stations, proj) -> str:
    out = []
    for s in stations:
        if s.get("stop") is False:          # shapes the curve only
            continue
        x, y = proj.xy(s["lon"], s["lat"])
        left = s.get("label") == "left"
        tx, anchor = (x - 9, "end") if left else (x + 9, "start")
        sub = (f'<text class="sub" x="{tx:.1f}" y="{y + 16:.1f}" text-anchor="{anchor}">{escape(s["note"])}</text>'
               if s.get("note") else "")
        out.append(f'<g class="stn"><circle cx="{x:.1f}" cy="{y:.1f}" r="4.2"/>'
                   f'<text x="{tx:.1f}" y="{y + 4.5:.1f}" text-anchor="{anchor}">{escape(s["name"])}</text>{sub}</g>')
    return "".join(out)


def line_parts(ln, path_d, proj, signal):
    lid, color = ln["id"], ln["color"]
    shown = [s for s in ln.get("stations") or [] if s.get("stop") is not False]
    svg = (f'<g id="line-{lid}">'
           f'<path class="ties" d="{path_d}"/>'
           f'<path id="planned-{lid}" class="planned" d="{path_d}" stroke="{color}"/>'
           f'<path id="done-{lid}" class="done" d="{path_d}" stroke="{color}"/>'
           f'{stations_svg(ln.get("stations") or [], proj)}</g>')
    body, half, chimney = trains.build(ln.get("style", "steam"), color, ln.get("first_class"), signal)
    k = float(ln.get("scale", 1))           # size of this line's train
    train = (f'<g id="train-{lid}" aria-hidden="true"><g transform="scale({k})">'
             f'<g id="body-{lid}" transform="translate({-half},-7)">{body}</g></g></g>')
    js = {"id": lid, "color": color, "seconds": ln.get("seconds", 12), "pause": ln.get("pause_seconds", 2),
          "half": half, "chimney": chimney * k if chimney is not None else None, "smoke": chimney is not None,
          "stations": [[round(v, 1) for v in proj.xy(s["lon"], s["lat"])] for s in shown]}
    return svg, train, js


def build_html(cfg, proj, rings, routes) -> str:
    """routes: list of (line_config, [(lon, lat), ...], smooth)."""
    lab, col = cfg["labels"], cfg["colors"]
    signal = cfg["lines"][0]["color"]
    svgs, trs, js = [], [], []
    for ln, lonlat, smooth in routes:
        pts = [proj.xy(lon, lat) for lon, lat in lonlat]
        s, t, j = line_parts(ln, smooth_path(pts) if smooth else line_path(pts), proj, signal)
        svgs.append(s); trs.append(t); js.append(j)
    legend = "".join(f'<span><i style="background:{ln["color"]}"></i>{escape(ln["name"])}</span>' for ln, _, _ in routes)
    notes = "".join(f'<p style="color:{ln["color"]}">{escape(ln["note_approximate"])}</p>'
                    for ln, _, _ in routes if ln.get("approximate") and ln.get("note_approximate"))
    values = {
        "__TITLE__": escape(cfg["title"]), "__SUBTITLE__": escape(cfg["subtitle"]),
        "__ARIA__": escape(f'{cfg["title"]}: little trains travel each line on a map of Honduras'),
        "__W__": str(proj.width), "__H__": str(proj.height),
        "__LAND_PATHS__": "".join(f'<path class="land" d="{ring_path(r, proj)}"/>' for r in rings),
        "__LINES__": "".join(svgs), "__TRAINS__": "".join(trs),
        "__LINES_JSON__": json.dumps(js, ensure_ascii=False).replace("<", "\\u003c"),
        "__LEGEND__": legend, "__APPROX_NOTES__": notes,
        "__NORTH_SEA__": escape(lab["north_sea"]), "__SOUTH_SEA__": escape(lab["south_sea"]),
        "__NSX__": f"{proj.width * 0.42:.0f}", "__NSY__": "34",
        "__SSX__": f"{proj.width * 0.40:.0f}", "__SSY__": f"{proj.height - 24:.0f}",
        "__CREDIT__": escape(lab["credit"]),
        "__PROJECT__": __project__, "__VERSION__": __version__,
    }
    values.update({f"__{k.upper()}__": v for k, v in col.items()})
    html = TEMPLATE.read_text(encoding="utf-8")
    for k in sorted(values, key=len, reverse=True):
        html = html.replace(k, values[k])
    return html
