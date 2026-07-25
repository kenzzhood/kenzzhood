"""
Central configuration for the GitHub profile README generator.

All colours, sizes, animation timings, and profile content live here so scripts
stay thin and everything is tunable from one place.
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT: Path = Path(__file__).resolve().parent
ASSETS_DIR: Path = ROOT / "assets"
DATA_DIR: Path = ROOT / "data"
SCRIPTS_DIR: Path = ROOT / "scripts"

PROFILE_PHOTO: Path = ASSETS_DIR / "profile.jpg"
PROFILE_PREPPED: Path = ASSETS_DIR / "profile-prepped.png"
ASCII_SVG: Path = ASSETS_DIR / "ascii-profile.svg"
NEOFETCH_SVG: Path = ASSETS_DIR / "neofetch.svg"
CONTRIBUTION_SVG: Path = ASSETS_DIR / "contribution-graph.svg"
CONTRIBUTION_DARK_SVG: Path = ASSETS_DIR / "contribution-dark.svg"
CONTRIBUTION_LIGHT_SVG: Path = ASSETS_DIR / "contribution-light.svg"
BANNER_SVG: Path = ASSETS_DIR / "banner.svg"
SEPARATOR_SVG: Path = ASSETS_DIR / "separator.svg"
HERO_DARK_SVG: Path = ASSETS_DIR / "hero-dark.svg"
HERO_LIGHT_SVG: Path = ASSETS_DIR / "hero-light.svg"
CAPABILITIES_DARK_SVG: Path = ASSETS_DIR / "capabilities-dark.svg"
CAPABILITIES_LIGHT_SVG: Path = ASSETS_DIR / "capabilities-light.svg"
RESEARCH_DARK_SVG: Path = ASSETS_DIR / "research-dark.svg"
RESEARCH_LIGHT_SVG: Path = ASSETS_DIR / "research-light.svg"
PROJECTS_DIR: Path = ASSETS_DIR / "projects"

CONTRIBUTIONS_JSON: Path = DATA_DIR / "contributions.json"
REPOS_JSON: Path = DATA_DIR / "repos.json"
QUOTES_JSON: Path = DATA_DIR / "quotes.json"

# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------

GITHUB_USERNAME: str = "kenzzhood"
NAME: str = "Goutham Srinath K."
ROLE: str = "AI / XR Engineer"
COMPANY: str = "InnoXR Labs"
PROMPT_HOST: str = "kenzzhood@github"
LOCATION: str = "Bengaluru, India"

SLOGANS: list[str] = [
    "Making Retail Intelligent",
    "Your Vision, Our Technology",
]

ABOUT: str = (
    "I build production systems across computer vision, spatial computing, "
    "XR, and multimodal AI—from research prototypes to shipped products."
)

INCUBATED_AT: str = "IITMIC · NSRCEL · iTNT · Sathyabama"

CERTIFICATION: str = "Unity Certified Associate — Game Developer"

RESEARCH_INTERESTS: list[str] = [
    "Computer Vision",
    "Gaussian Splatting",
    "3D Reconstruction",
    "Spatial Computing",
    "Holography",
    "LLMs",
    "AR / VR / MR",
]

LANGUAGES: list[str] = [
    "Python",
    "C++",
    "C#",
    "TypeScript",
    "JavaScript",
    "Dart",
    "Java",
]

FRAMEWORKS: list[str] = [
    "Unity",
    "Next.js",
    "React",
    "FastAPI",
    "Flutter",
    "Azure OpenAI",
    "LangChain",
    "Hugging Face",
    "Docker",
]

CONTACT: dict[str, str] = {
    "github": "https://github.com/kenzzhood",
    "company": "https://innoxrlabs.com",
    "email": "gtkgoutham@gmail.com",
    "linkedin": "https://www.linkedin.com/in/goutham-srinath-380446288",
    "portfolio": "https://goutham.netlify.app",
}

PUBLICATION: dict[str, str] = {
    "title": (
        "MILES: Multimodal Intelligent Assistant for 3D Model Generation "
        "and Holographic Interaction Using Voice and Gesture Control"
    ),
    "url": "https://doi.org/10.1109/RMKMATE69073.2026.11518707",
    "venue": "IEEE, 2026",
}

# ---------------------------------------------------------------------------
# Visual profile system
# ---------------------------------------------------------------------------

CANVAS_WIDTH: int = 860

POSITIONING: str = (
    "Computer vision, XR, and multimodal AI systems—"
    "designed, built, and shipped end to end."
)

FOUNDER_THESIS: str = (
    f"Founder, {COMPANY}. Incubated at {INCUBATED_AT}."
)

PROOF_POINTS: list[dict[str, str]] = [
    {"label": "Focus", "value": "Computer Vision · XR · Multimodal AI"},
    {"label": "Shipped", "value": "AuraFit · AutoOps · MILES · Wander Lens"},
    {"label": "Certified", "value": CERTIFICATION},
]

CAPABILITY_GROUPS: list[dict[str, object]] = [
    {
        "index": "01",
        "name": "Vision & 3D",
        "statement": "Turn product media and scenes into interactive spatial assets.",
        "pipeline": ["capture", "reconstruct", "render"],
        "tools": ["OpenCV", "Gaussian Splats", "Blender", "Unity"],
    },
    {
        "index": "02",
        "name": "Spatial / XR",
        "statement": "Ship AR, VR, and holographic experiences people actually use.",
        "pipeline": ["sense", "interact", "deploy"],
        "tools": ["Unity", "ARCore", "MediaPipe", "Flutter"],
    },
    {
        "index": "03",
        "name": "AI Products",
        "statement": "Full-stack systems that reason, retrieve, and take useful action.",
        "pipeline": ["ingest", "reason", "act"],
        "tools": ["FastAPI", "LLMs", "RAG", "Azure OpenAI"],
    },
]

RESEARCH_PIPELINE: list[dict[str, str]] = [
    {
        "step": "See",
        "title": "Computer Vision",
        "detail": "Perception for retail, travel, and XR",
    },
    {
        "step": "Rebuild",
        "title": "3D Assets",
        "detail": "Gaussian splats · photogrammetry",
    },
    {
        "step": "Reason",
        "title": "Multimodal AI",
        "detail": "LLMs · RAG · voice & gesture",
    },
    {
        "step": "Touch",
        "title": "Spatial UX",
        "detail": "AR · holography · retail interfaces",
    },
]

CASE_STUDIES: list[dict[str, object]] = [
    {
        "slug": "miles",
        "index": "01",
        "name": "HoloInteract / MILES",
        "category": "IEEE · holographic AI",
        "url": "https://github.com/kenzzhood/MILES",
        "summary": (
            "Interactive holography with MediaPipe hand tracking and "
            "RAG-guided multimodal AI for education and product showcases."
        ),
        "pipeline": ["gesture", "3D hologram", "LLM guidance", "interact"],
        "stack": ["Unity", "MediaPipe", "FastAPI", "LLMs", "Gaussian Splatting"],
        "signal": "IEEE-published multimodal 3D + holographic interaction system",
    },
    {
        "slug": "aurafit",
        "index": "02",
        "name": "AuraFit",
        "category": "Full-stack AI product",
        "url": "https://github.com/kenzzhood/AuraFit",
        "summary": (
            "Fashion intelligence platform that turns one photo and style prefs "
            "into six editorial looks with real shoppable product links."
        ),
        "pipeline": ["photo in", "GPT-4o + vision", "look board", "product crawl"],
        "stack": ["Next.js", "Expo", "Azure OpenAI", "Prisma", "pgvector", "Playwright"],
        "signal": "Web studio + React Native app + self-hosted discovery crawler",
    },
    {
        "slug": "autoops",
        "index": "03",
        "name": "AutoOps AI",
        "category": "Open-source CLI · PyPI",
        "url": "https://github.com/kenzzhood/AutoOps",
        "summary": (
            "Autonomous observability CLI that scans a codebase, instruments it, "
            "bootstraps Splunk + OpenTelemetry, and runs AI-driven RCA."
        ),
        "pipeline": ["scan", "instrument", "collect evidence", "remediate"],
        "stack": ["Python", "FastAPI", "Splunk", "OpenTelemetry", "Docker", "LLMs"],
        "signal": "Published as autoops-ai on PyPI with multi-provider LLM support",
    },
    {
        "slug": "wander-lens",
        "index": "04",
        "name": "Wander Lens",
        "category": "AI travel · AR",
        "url": "https://github.com/kenzzhood/Wander_Lens",
        "summary": (
            "Social travel companion with RAG itineraries, matchmaking, and "
            "AR memories plus Gaussian Splatting food previews."
        ),
        "pipeline": ["plan", "match", "AR explore", "3D preview"],
        "stack": ["Hugging Face", "Unity", "ARCore", "Firebase", "LLMs"],
        "signal": "RAG trip planning connected to spatial AR experiences",
    },
]

# Paired theme tokens — restrained, GitHub-native contrast.
THEMES: dict[str, dict[str, str]] = {
    "dark": {
        "bg": "#0d1117",
        "surface": "#151b23",
        "surface_2": "#1c2330",
        "line": "#30363d",
        "line_soft": "#21262d",
        "text": "#e6edf3",
        "muted": "#8b949e",
        "faint": "#6e7681",
        "green": "#3fb950",
        "cyan": "#58a6ff",
        "violet": "#a371f7",
        "empty": "#161b22",
    },
    "light": {
        "bg": "#ffffff",
        "surface": "#f6f8fa",
        "surface_2": "#eef2f6",
        "line": "#d0d7de",
        "line_soft": "#e6ebf1",
        "text": "#1f2328",
        "muted": "#656d76",
        "faint": "#8c959f",
        "green": "#1a7f37",
        "cyan": "#0969da",
        "violet": "#8250df",
        "empty": "#ebedf7",
    },
}

# ---------------------------------------------------------------------------
# Theme — modern hacker terminal (monochrome, GitHub dark compatible)
# ---------------------------------------------------------------------------

COLORS: dict[str, str] = {
    "bg": "#0d1117",
    "bg2": "#111722",
    "frame": "#30363d",
    "muted": "#8b949e",
    "ink": "#c9d1d9",
    "bright": "#e6edf3",
    "accent": "#3fb950",  # classic terminal green — single accent
    "dim_accent": "#238636",
    "cursor": "#c9d1d9",
    "gold": "#d2a8ff",  # reserved for rare highlights (streaks)
    # traffic-light titlebar dots (kept subtle / standard)
    "dot_red": "#ff5f56",
    "dot_yellow": "#ffbd2e",
    "dot_green": "#27c93f",
}

# GitHub contribution green palette (none → brightest)
CONTRIB_PALETTE: list[str] = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]

FONT_FAMILY: str = (
    "'JetBrains Mono', 'SFMono-Regular', ui-monospace, Menlo, Consolas, monospace"
)

# ---------------------------------------------------------------------------
# ASCII portrait
# ---------------------------------------------------------------------------

ASCII: dict[str, object] = {
    "cols": 100,
    "rows": 53,
    "cell_w": 8,
    "cell_h": 15,
    "ramp": " .`:-=+*cs#%@",  # bright (sparse) → dark (dense)
    "contrast": 1.05,
    "brightness": 1.0,
    "gamma": 1.18,
    "white_floor": 0.80,
    "pad": 20,
    "titlebar_h": 30,
    "status_h": 30,
    "row_dur": 0.11,
    "stagger": 0.11,
    "clahe_clip": 2.6,
    "clahe_tile": 8,
    "global_alpha": 1.05,
    "global_beta": 18,
}

# ---------------------------------------------------------------------------
# Neofetch card
# ---------------------------------------------------------------------------

NEOFETCH: dict[str, object] = {
    "width": 490,
    "height": 420,
    "pad": 20,
    "titlebar_h": 30,
    "line_h": 20.5,
    "key_width": 92,
    "fade_dur": 0.40,
    "stagger": 0.06,
    "initial_delay": 0.15,
}

# ---------------------------------------------------------------------------
# Contribution graph
# ---------------------------------------------------------------------------

HEATMAP: dict[str, object] = {
    "cell": 12,
    "gap": 3,
    "pad": 22,
    "left_label_w": 30,
    "top_label_h": 20,
    "titlebar_h": 30,
    "stats_h": 88,
    "col_t": 0.018,
    "row_t": 0.045,
    "cell_dur": 0.42,
}

# ---------------------------------------------------------------------------
# Networking
# ---------------------------------------------------------------------------

USER_AGENT: str = "kenzzhood-profile-readme/1.0 (+https://github.com/kenzzhood)"
REQUEST_TIMEOUT: int = 30
CONTRIBUTIONS_URL: str = (
    f"https://github.com/users/{GITHUB_USERNAME}/contributions"
)
GITHUB_REPOS_API: str = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
REPO_FETCH_LIMIT: int = 8
