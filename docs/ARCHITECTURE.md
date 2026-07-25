# Architecture

This repository generates a proof-driven GitHub profile from a single content
and design source: [`config.py`](../config.py).

The README is semantic HTML and Markdown. All visual assets are local,
self-contained SVG files with accessible titles, descriptions, one-shot CSS
motion, and reduced-motion fallbacks.

```text
config.py
   ├── make_hero_svg.py ─────────── hero-dark/light.svg
   ├── make_capabilities_svg.py ─── capabilities + research SVGs
   ├── make_projects_svg.py ─────── linked case-study SVGs
   ├── render_readme.py ─────────── README.md
   └── fetch_contributions.py
          └── render_heatmap_svg.py ── contribution-dark/light.svg
```

`generate_all.py` orchestrates the complete local build.
`validate_profile.py` checks XML validity, accessibility metadata, local asset
references, forbidden script/external visual dependencies, and contribution
data sanity.

## Content model

- **Positioning:** founder thesis and proof points
- **Capabilities:** computer vision, spatial/XR, and AI systems
- **Research:** observe → reconstruct → understand → interact
- **Case studies:** problem framing, architecture pipeline, stack, and signal
- **Telemetry:** contribution activity scraped from the public GitHub page

Each major visual has a dark and light variant. The README selects the
appropriate file with `<picture>` and `prefers-color-scheme`.

## Update paths

- A portrait change runs `prep_photo.py`, then regenerates the hero.
- A narrative, project, or design change updates `config.py`, then runs the
  complete generator.
- GitHub Actions refreshes contribution JSON and both telemetry assets daily.

## Constraints

- No JavaScript in the README or SVGs
- No GitHub token or GraphQL dependency for contributions
- No hosted profile-stat widgets or external image dependencies
- The only dynamic external request scrapes GitHub's public contribution page
- Generated README and SVG assets remain committed for reliable rendering
