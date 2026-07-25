# Architecture

This repository is a **GitHub profile README** generator. Animations live entirely
inside self-contained SVG files; the `README.md` only embeds them via `<img>`.

GitHub strips `<script>` and most inline CSS from markdown, but SVGs loaded as
images still run **SMIL** and **CSS keyframe** animations.

```
┌─────────────────────────────────────────────────────────────┐
│  README.md (terminal layout, HTML tables for columns)       │
│   ├─ assets/banner.svg                                      │
│   ├─ assets/contribution-graph.svg  ← daily refresh         │
│   ├─ assets/ascii-profile.svg       ← regenerate on photo   │
│   └─ assets/neofetch.svg            ← regenerate on config  │
└─────────────────────────────────────────────────────────────┘
              ▲                         ▲
              │                         │
     scripts/*.py (local)     .github/workflows/update-profile.yml
              │                         │
              └──────── config.py ──────┘
```

## Pipelines

| Asset | Scripts | When |
|-------|---------|------|
| ASCII portrait | `prep_photo.py` → `make_ascii_svg.py` | Photo changes |
| Neofetch card | `make_neofetch.py` | Profile/config changes |
| Banner / separator | `make_banner.py` | Rarely |
| Contribution graph | `fetch_contributions.py` → `render_heatmap_svg.py` | Daily (CI) |
| Latest repos | `fetch_repos.py` | Optional |

## Constraints

- **No JavaScript** in the README
- **No GitHub token** / GraphQL for contributions
- **No third-party stats services**
- Only external request: scrape GitHub's public contributions HTML
- Everything generated locally (or in Actions) and committed

## Config

All identity, colours, fonts, animation timings, and SVG sizes live in
[`config.py`](../config.py).
