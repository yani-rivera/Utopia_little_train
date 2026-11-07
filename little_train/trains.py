"""The little trains, drawn facing right with the line's centre at y = 7.

Each function returns (svg, half_length, chimney_x or None). `half_length` centres the train
on the line; `chimney_x` (from the centre) is where smoke comes out.
"""
from html import escape

GOLD = "#c9a227"


def _first_class(x: float, label: str, signal: str) -> str:
    """A golden wagon with three windows, a tiny wifi signal and an AC snowflake on the roof."""
    win = "".join(f'<rect x="{x + 2.5 + 4.2 * i:.1f}" y="4" width="2.6" height="2.6" rx=".4" fill="#fff6dc"/>' for i in range(3))
    wifi = (f'<g fill="none" stroke="{signal}" stroke-width=".9" stroke-linecap="round">'
            f'<path d="M{x + 5.5},-1.2 Q{x + 8},-3.6 {x + 10.5},-1.2"/><path d="M{x + 4},-2.6 Q{x + 8},-6.4 {x + 12},-2.6"/></g>'
            f'<circle cx="{x + 8}" cy="0.2" r=".8" fill="{signal}"/>')
    ac = ('<g stroke="#4a9fd0" stroke-width=".8" stroke-linecap="round">'
          f'<path d="M{x + 13.6},-4.6 V-0.6"/><path d="M{x + 11.9},-3.6 L{x + 15.3},-1.6"/><path d="M{x + 11.9},-1.6 L{x + 15.3},-3.6"/></g>')
    return (f'<g class="first"><title>{escape(label)}</title>'
            f'<rect x="{x}" y="2" width="16" height="9" rx="1.8" fill="{GOLD}" stroke="var(--train)" stroke-width="1.2"/>'
            f'{win}<rect x="{x}" y="8.2" width="16" height=".9" fill="var(--train)" opacity=".35"/>{wifi}{ac}'
            f'<circle cx="{x + 4}" cy="12" r="2" fill="var(--train)"/><circle cx="{x + 12}" cy="12" r="2" fill="var(--train)"/>'
            f'<rect x="{x + 16}" y="7" width="2" height="1.5" fill="var(--train)"/></g>')


def steam(first_class: str | None, signal: str):
    """Two wagons, an optional first-class wagon, and a steam engine with a chimney."""
    wagon = lambda x: (f'<rect x="{x}" y="3" width="14" height="8" rx="1.5" fill="var(--paper)" stroke="var(--train)" stroke-width="1.2"/>'
                       f'<circle cx="{x + 4}" cy="12" r="2" fill="var(--train)"/><circle cx="{x + 10}" cy="12" r="2" fill="var(--train)"/>'
                       f'<rect x="{x + 14}" y="7" width="2" height="1.5" fill="var(--train)"/>')
    parts = [wagon(0), wagon(16)]
    ex = 32
    if first_class:
        parts.append(_first_class(32, first_class, signal))
        ex = 50
    parts.append(f'<g transform="translate({ex},0)">'
                 '<rect x="0" y="2" width="9" height="9" rx="1" fill="var(--train)"/>'
                 '<rect x="9" y="5" width="11" height="6" rx="1.5" fill="var(--train)"/>'
                 '<rect x="15" y="0" width="3" height="5" fill="var(--train)"/>'
                 '<rect x="1.5" y="3.5" width="4" height="3" fill="var(--paper)"/>'
                 '<circle cx="4" cy="12" r="2.3" fill="var(--train)"/><circle cx="12" cy="12" r="2.3" fill="var(--train)"/>'
                 '<circle cx="18" cy="12" r="2" fill="var(--train)"/></g>')
    half = (ex + 20) / 2
    return "".join(parts), half, ex + 16.5 - half


def fast(color: str, first_class: str | None, signal: str):
    """A sleek fast train in the line's colour: two cars and a rounded nose, no smoke."""
    car = lambda x: (f'<rect x="{x}" y="3" width="17" height="8" rx="2.5" fill="{color}" stroke="var(--train)" stroke-width="1"/>'
                     f'<rect x="{x + 2}" y="4.5" width="13" height="2.4" rx="1" fill="#e9f4f8"/>'
                     f'<circle cx="{x + 4}" cy="12" r="1.6" fill="var(--train)"/><circle cx="{x + 13}" cy="12" r="1.6" fill="var(--train)"/>')
    parts = [car(0)]
    x = 18
    if first_class:
        parts.append(_first_class(x, first_class, signal))
        x += 19
    parts.append(car(x))
    nose = x + 18
    parts.append(f'<path d="M{nose},3 H{nose + 8} Q{nose + 17},4 {nose + 18},11 H{nose} Z" fill="{color}" stroke="var(--train)" stroke-width="1"/>'
                 f'<path d="M{nose + 9},4.6 Q{nose + 14},5.2 {nose + 15.5},8 H{nose + 9} Z" fill="#e9f4f8"/>'
                 f'<circle cx="{nose + 5}" cy="12" r="1.6" fill="var(--train)"/>')
    return "".join(parts), (nose + 18) / 2, None


def build(style: str, color: str, first_class: str | None, signal: str):
    if style == "fast":
        return fast(color, first_class, signal)
    return steam(first_class, signal)
