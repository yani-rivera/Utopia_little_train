"""Outline loading and a simple map projection to SVG coordinates."""
import json
import math
from pathlib import Path


def load_rings(path) -> list[list[tuple[float, float]]]:
    """All outer and inner rings of every (Multi)Polygon, as (lon, lat) lists."""
    rings = []
    for f in json.loads(Path(path).read_text(encoding="utf-8"))["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            rings.extend([[tuple(p[:2]) for p in ring] for ring in poly])
    return rings


class Projection:
    """Equirectangular, scaled by cos(mid-latitude), fitted to a box with padding (in px)."""

    def __init__(self, rings, width=760, pad=(60, 40, 90, 40)):
        pts = [p for r in rings for p in r]
        self.w0, self.e0 = min(p[0] for p in pts), max(p[0] for p in pts)
        self.s0, self.n0 = min(p[1] for p in pts), max(p[1] for p in pts)
        self.kx = math.cos(math.radians((self.s0 + self.n0) / 2))
        top, right, bottom, left = pad
        span_x = (self.e0 - self.w0) * self.kx
        self.scale = (width - left - right) / span_x
        self.left, self.top = left, top
        self.width = width
        self.height = round(top + bottom + (self.n0 - self.s0) * self.scale)

    def xy(self, lon, lat):
        return (self.left + (lon - self.w0) * self.kx * self.scale,
                self.top + (self.n0 - lat) * self.scale)


def ring_path(ring, proj) -> str:
    pts = [proj.xy(*p) for p in ring]
    return "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
