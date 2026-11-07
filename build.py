"""Build the little-train page.

    python build.py --config config.yaml
"""
import argparse
from pathlib import Path

import yaml

from little_train import __project__, __version__, provenance
from little_train.geo import load_rings, Projection
from little_train.render import build_html
from little_train.route import from_geojson


def main():
    ap = argparse.ArgumentParser(description=f"{__project__} v{__version__}")
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))

    rings = load_rings(cfg["outline"])
    proj = Projection(rings)
    routes, inputs = [], [cfg["outline"]]
    for ln in cfg["lines"]:
        if ln.get("geojson"):                 # digitized line: draw it as it is
            routes.append((ln, from_geojson(ln["geojson"]), False)); inputs.append(ln["geojson"])
        else:                                 # stations only: smooth curve through them
            routes.append((ln, [(s["lon"], s["lat"]) for s in ln["stations"]], True))

    out = Path(cfg["output"])
    out.write_text(build_html(cfg, proj, rings, routes), encoding="utf-8")
    provenance.write(out.parent, args.config, inputs, {
        "output": out.name,
        "lines": [{"id": ln["id"], "route": "digitized line" if ln.get("geojson") else "approximate, through stations",
                   "stations": len(ln.get("stations") or [])} for ln in cfg["lines"]]})
    print(f"{__project__} v{__version__} → {out} ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
