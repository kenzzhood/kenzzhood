# Local development

## One-command setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Place a portrait at `assets/profile.jpg`, then:

```bash
python scripts/generate_all.py
```

## Individual commands

```bash
# Portrait pipeline
python scripts/prep_photo.py
python scripts/make_ascii_svg.py

# Neofetch card
python scripts/make_neofetch.py

# Banner + separator
python scripts/make_banner.py

# Live contribution graph
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py

# Latest public repos (optional)
python scripts/fetch_repos.py

# Heatmap only (mirrors CI)
python scripts/generate_all.py --heatmap-only
```

## Frozen previews

Quick Look / Finder can struggle with SMIL. Emit static frames:

```bash
STATIC=1 python scripts/make_ascii_svg.py
STATIC=1 python scripts/make_neofetch.py
```

## Tuning

Edit [`config.py`](../config.py):

- `ASCII` — grid size, density ramp, typing speed
- `NEOFETCH` — card size, fade stagger
- `HEATMAP` — cell size, diagonal reveal timing
- `COLORS` — terminal palette
- Profile content — name, role, research, stack, featured projects

## CI

[`.github/workflows/update-profile.yml`](../.github/workflows/update-profile.yml)
runs daily on Python 3.11 with `requirements-ci.txt` (requests + BeautifulSoup
only). Commits use `[skip ci]` to avoid workflow loops.
