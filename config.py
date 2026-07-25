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
BANNER_SVG: Path = ASSETS_DIR / "banner.svg"
SEPARATOR_SVG: Path = ASSETS_DIR / "separator.svg"

CONTRIBUTIONS_JSON: Path = DATA_DIR / "contributions.json"
REPOS_JSON: Path = DATA_DIR / "repos.json"
QUOTES_JSON: Path = DATA_DIR / "quotes.json"

# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------

GITHUB_USERNAME: str = "kenzzhood"
NAME: str = "Goutham Srinath"
ROLE: str = "Founder & CEO"
COMPANY: str = "InnoXR Labs"
PROMPT_HOST: str = "kenzzhood@github"

ABOUT: str = (
    "Building AI-powered Spatial Computing, Computer Vision, XR, "
    "and Generative AI products."
)

RESEARCH_INTERESTS: list[str] = [
    "Computer Vision",
    "Gaussian Splatting",
    "3D Reconstruction",
    "Spatial Computing",
    "Robotics",
    "Generative AI",
    "LLMs",
    "AI Agents",
]

LANGUAGES: list[str] = [
    "Python",
    "C++",
    "TypeScript",
    "JavaScript",
    "C#",
    "Java",
]

FRAMEWORKS: list[str] = [
    "React",
    "React Native",
    "FastAPI",
    "Unity",
    "OpenCV",
    "PyTorch",
    "TensorFlow",
    "ROS",
    "Docker",
]

CURRENTLY_BUILDING: list[str] = [
    "AI-powered XR experiences @ InnoXR Labs",
    "Computer vision pipelines for spatial apps",
    "Generative AI agent tooling",
]

OPEN_SOURCE: list[str] = [
    "Vision / XR demos and research tools",
    "Observability CLI experiments (AutoOps)",
]

STARTUP: str = "InnoXR Labs — Spatial Computing × AI"

# Featured projects shown in the README (manual curation).
FEATURED_PROJECTS: list[dict[str, str]] = [
    {
        "name": "AutoOps",
        "desc": "Autonomous observability CLI — Splunk + OpenTelemetry + AI RCA",
        "url": "https://github.com/kenzzhood/AutoOps",
    },
    {
        "name": "Atoms Vision Audit",
        "desc": "Computer-vision delivery & quality audit tooling",
        "url": "https://github.com/kenzzhood/Atoms-Vision-Audit",
    },
    {
        "name": "AuraFit",
        "desc": "AI fitness experience",
        "url": "https://github.com/kenzzhood/AuraFit",
    },
    {
        "name": "MOOTVR",
        "desc": "VR moot-court simulator for law students",
        "url": "https://github.com/kenzzhood/MOOTVR",
    },
    {
        "name": "Health Intellect",
        "desc": "Unified AI healthcare records & consults",
        "url": "https://github.com/kenzzhood/Health-Intellect",
    },
    {
        "name": "3D Hand Tracking",
        "desc": "Real-time 3D hand tracking experiments",
        "url": "https://github.com/kenzzhood/3D-Hand-Tracking",
    },
]

CONTACT: dict[str, str] = {
    "github": "https://github.com/kenzzhood",
    "company": "https://innoxrlabs.com",
    "email": "hello@innoxrlabs.com",
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
