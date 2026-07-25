# Local development

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Place the source portrait at `assets/profile.jpg`, then run:

```bash
python scripts/generate_all.py
```

For normal content/design changes, reuse the preprocessed portrait and current
contribution data:

```bash
python scripts/generate_all.py --skip-photo --skip-network
```

## Individual commands

```bash
# Portrait pipeline
python scripts/prep_photo.py

# Identity hero
python scripts/make_hero_svg.py

# Capability and research maps
python scripts/make_capabilities_svg.py

# Linked flagship case-study cards
python scripts/make_projects_svg.py

# Public contribution telemetry
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py

# README composition and checks
python scripts/render_readme.py
python scripts/validate_profile.py

# Daily telemetry path (mirrors CI)
python scripts/generate_all.py --heatmap-only
```

## Tuning

Edit [`config.py`](../config.py):

- `POSITIONING`, `FOUNDER_THESIS`, and `PROOF_POINTS` define the narrative.
- `CAPABILITY_GROUPS` and `RESEARCH_PIPELINE` define technical range.
- `CASE_STUDIES` defines project proof and link targets.
- `THEMES` defines paired dark/light visual tokens.
- Legacy `ASCII`, `NEOFETCH`, and `HEATMAP` sections remain available for the
  older standalone generators.

All major artwork uses a shared 860-pixel viewBox and scales down inside
GitHub. Animations are restrained, one-shot, and disabled when the reader
prefers reduced motion.

## Validation

`validate_profile.py` fails when:

- a required generated SVG is missing or invalid XML,
- an asset lacks accessible metadata,
- a script or external SVG dependency appears,
- README references are broken or externally hosted, or
- contribution data is incomplete or malformed.

## CI

[`.github/workflows/update-profile.yml`](../.github/workflows/update-profile.yml)
runs daily on Python 3.11 with `requirements-ci.txt` (requests + BeautifulSoup
only). It refreshes both telemetry themes, validates the profile, and commits
only when public contribution data changed.
