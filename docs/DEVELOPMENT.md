# Local development

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

The active profile has no runtime dependencies. Generate and validate it with:

```bash
python scripts/generate_all.py
```

Or run each step separately:

```bash
python scripts/render_readme.py
python scripts/validate_profile.py
```

## Editing

Edit the résumé-backed content in `scripts/render_readme.py`, regenerate, and
review the resulting `README.md`.

The profile uses native Markdown and a small amount of semantic HTML for the
centered identity block. Keep sections factual, concise, and ordered by
professional relevance.

## Validation

`validate_profile.py` fails when:

- a required résumé section is missing,
- a verified project, publication, or professional link is missing,
- decorative image markup or scripts are introduced, or
- the README grows beyond the profile's concise content budget.
