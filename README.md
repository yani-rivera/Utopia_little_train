# Still Dreaming of the Train

Little trains travelling the railways Honduras keeps drawing: from E. G. Squier's interoceanic
railway of the 1850s, Caribbean to Pacific, to a fast line from Palmerola to Campo Marte in 2026.
One dream, drawn again and again.

Built with **little_train**, a small builder that turns a config into one self-contained web page
(no outside scripts or fonts): each line gets its own train, colour and timing; stations light up
as the train passes; the steam train puffs smoke, and its first-class wagon has wifi and AC.

**Version 0.3.0** (2026-11-07)

## The lines

| Line | Train | Route |
|---|---|---|
| Interoceanic Railway, as Squier drew it (1850s) | steam, with a first-class wagon | Puerto Cortés → San Pedro → Lake Yojoa → Comayagua → Goascorán → Gulf of Fonseca |
| Palmerola to Campo Marte, my utopia (2026) | fast | Palmerola → Zambrano → Támara → Campo Marte |

**Both routes are approximate for now:** smooth curves through the towns they pass. They will be
redrawn from digitized lines: Squier's from the georeferenced 1850s map, and the utopia from the
least-cost alignment made for the #30DayMapChallenge 2026 (Day 8, Utopia).

## Make it

```bash
pip install pyyaml
python build.py --config config.yaml
open train.html
```

Each build writes `train.html` and a `provenance.json` with the code version, the config's SHA-256
and the SHA-256 of every input.

## Configure it (`config.yaml`)

- `title`, `subtitle`, `labels`, `colors`: the page's words and palette.
- `lines`: one entry per railway:
  - `geojson`: a digitized LineString (preferred); otherwise `stations` are joined by a smooth curve.
  - `stations`: `name`, `lat`, `lon`; `note` adds a small line under the name; `label: left` puts
    the name on the left; `stop: false` shapes the curve without a station dot.
  - `style`: `steam` (with smoke) or `fast`; `scale` sizes the train; `first_class` adds the golden
    wagon (its text shows on hover).
  - `seconds`, `pause_seconds`: one journey, and the rest at the end of the line.
  - `approximate` and `note_approximate`: say on the page when a route is not exact.

To add a line, for example the stretch actually built by 1894, add one more entry to `lines`.

## Structure

```
build.py                 command line
config.yaml              everything the page shows
little_train/geo.py      outline loading, map projection
little_train/route.py    lines from GeoJSON, or smooth curves through stations
little_train/trains.py   the trains (steam, fast, first-class wagon)
little_train/render.py   fills the page template
little_train/template.html  the page: map, trains, animation
little_train/provenance.py  provenance.json
data/honduras.geojson    outline
```

## Sources and licences

- **Outline:** Natural Earth 1:50m, public domain.
- **Squier's line:** after E. G. Squier, *Map of Honduras and San Salvador, Central America: showing
  the line of the proposed Honduras Interoceanic Railway*, drawn by D. C. Hitchcock, engraved by
  J. Schedler. American Geographical Society Library, University of Wisconsin–Milwaukee Libraries.
  A 19th-century work in the public domain; the route here is approximate.
- **Palmerola to Campo Marte:** Yanira A. Rivera, #30DayMapChallenge 2026 (Utopia).
- **Code:** MIT.

Map: Yanira A. Rivera · ORCID [0000-0003-3309-5256](https://orcid.org/0000-0003-3309-5256).
Built with AI-assisted code (Claude, Anthropic).
