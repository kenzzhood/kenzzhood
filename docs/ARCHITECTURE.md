# Architecture

The public profile is intentionally text-first. It uses GitHub's native
typography and spacing instead of decorative dashboards, badges, remote
widgets, or animated artwork.

```text
resume-backed content
   └── scripts/render_readme.py
          └── README.md
                 └── scripts/validate_profile.py
```

`generate_all.py` renders and validates the README. Legacy artwork generators
remain in the repository for historical reference but are not part of the
public profile or active build.

## Constraints

- Factual claims are sourced from the current résumé.
- Projects and publication titles link to verified public destinations.
- No JavaScript, decorative images, badge walls, or hosted stat widgets.
- The public phone number is intentionally omitted; email is the contact path.
- Content hierarchy must remain readable on mobile without custom layout code.
