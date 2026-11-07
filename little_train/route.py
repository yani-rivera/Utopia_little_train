"""The railway line: from a digitized GeoJSON line, or a smooth curve through stations."""
import json
from pathlib import Path


def from_geojson(path) -> list[tuple[float, float]]:
    for f in json.loads(Path(path).read_text(encoding="utf-8"))["features"]:
        g = f["geometry"]
        if g["type"] == "LineString":
            return [tuple(p[:2]) for p in g["coordinates"]]
        if g["type"] == "MultiLineString":
            return [tuple(p[:2]) for part in g["coordinates"] for p in part]
    raise ValueError(f"{path}: no LineString found")


def smooth_path(pts) -> str:
    """Catmull-Rom spline through projected points, as an SVG cubic Bézier path."""
    if len(pts) < 3:
        return "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    d = [f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"]
    p = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}")
    return "".join(d)


def line_path(pts) -> str:
    return "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
