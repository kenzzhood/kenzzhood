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
# Spatial Command Center — profile narrative and proof
# ---------------------------------------------------------------------------

CANVAS_WIDTH: int = 860

POSITIONING: str = (
    "Building spatial intelligence systems where AI can see, understand, "
    "and interact with the physical world."
)

FOUNDER_THESIS: str = (
    "I work across computer vision, real-time 3D, XR, and agentic AI—"
    "turning research-heavy ideas into products people can actually use."
)

PROOF_POINTS: list[dict[str, str]] = [
    {"label": "OPERATING MODE", "value": "Founder × Engineer × Researcher"},
    {"label": "BUILDING", "value": "Spatial intelligence @ InnoXR Labs"},
    {"label": "SYSTEMS", "value": "Vision · XR · AI agents · Real-time 3D"},
]

CAPABILITY_GROUPS: list[dict[str, object]] = [
    {
        "index": "01",
        "name": "COMPUTER VISION",
        "statement": "Perception systems that turn pixels into spatial understanding.",
        "pipeline": ["capture", "infer", "reconstruct"],
        "tools": ["OpenCV", "PyTorch", "TensorFlow", "3D vision"],
    },
    {
        "index": "02",
        "name": "SPATIAL / XR",
        "statement": "Interfaces that connect digital intelligence to physical space.",
        "pipeline": ["map", "interact", "simulate"],
        "tools": ["Unity", "OpenXR", "React Native", "ROS"],
    },
    {
        "index": "03",
        "name": "AI SYSTEMS",
        "statement": "Agentic products that observe, reason, and take useful action.",
        "pipeline": ["retrieve", "reason", "act"],
        "tools": ["FastAPI", "LLMs", "RAG", "Docker"],
    },
]

RESEARCH_PIPELINE: list[dict[str, str]] = [
    {
        "step": "OBSERVE",
        "title": "Computer Vision",
        "detail": "Detection · tracking · multimodal perception",
    },
    {
        "step": "RECONSTRUCT",
        "title": "3D Intelligence",
        "detail": "Gaussian splats · geometry · scene recovery",
    },
    {
        "step": "UNDERSTAND",
        "title": "Agentic AI",
        "detail": "LLMs · memory · tool use · planning",
    },
    {
        "step": "INTERACT",
        "title": "Spatial Systems",
        "detail": "XR · robotics · real-time human interfaces",
    },
]

CASE_STUDIES: list[dict[str, object]] = [
    {
        "slug": "autoops",
        "index": "01",
        "name": "AutoOps AI",
        "category": "AUTONOMOUS OBSERVABILITY",
        "url": "https://github.com/kenzzhood/AutoOps",
        "summary": (
            "An autonomous observability engineer that instruments codebases, "
            "builds telemetry, and investigates incidents with AI-driven RCA."
        ),
        "pipeline": ["repo scan", "OTel + Splunk", "AI investigation", "remediation"],
        "stack": ["Python", "FastAPI", "OpenTelemetry", "Docker", "LLMs"],
        "signal": "Architecture-aware automation from setup to root cause",
    },
    {
        "slug": "aurafit",
        "index": "02",
        "name": "AuraFit",
        "category": "AI-NATIVE PRODUCT",
        "url": "https://github.com/kenzzhood/AuraFit",
        "summary": (
            "A full-stack fashion intelligence platform that transforms a photo "
            "and personal taste into editorial, shoppable looks."
        ),
        "pipeline": ["vision input", "preference model", "look generation", "discovery"],
        "stack": ["Next.js", "React Native", "Azure OpenAI", "Supabase"],
        "signal": "Web, mobile, multimodal AI, and product discovery in one system",
    },
    {
        "slug": "placeit-xr",
        "index": "03",
        "name": "PlaceIT XR",
        "category": "SPATIAL COMMERCE",
        "url": "https://github.com/kenzzhood/PlaceIT_XR",
        "summary": (
            "An AI-powered AR shopping assistant that understands a space, "
            "finds suitable products, and previews them in context."
        ),
        "pipeline": ["scene image", "multimodal analysis", "retrieval", "AR placement"],
        "stack": ["Flutter", "Gemini", "AR", "Computer Vision"],
        "signal": "Spatial reasoning connected directly to a useful product flow",
    },
]

# Opaque artwork remains intentional: it looks composed in both GitHub themes,
# while paired files provide native contrast for readers whose theme follows OS.
THEMES: dict[str, dict[str, str]] = {
    "dark": {
        "bg": "#080b10",
        "surface": "#0d1219",
        "surface_2": "#111821",
        "line": "#263140",
        "line_soft": "#18212c",
        "text": "#f0f4f8",
        "muted": "#8c9aaa",
        "faint": "#596777",
        "green": "#6ee7a2",
        "cyan": "#7dd3fc",
        "violet": "#c4b5fd",
        "empty": "#141b24",
    },
    "light": {
        "bg": "#f7f9fb",
        "surface": "#ffffff",
        "surface_2": "#eef3f7",
        "line": "#ccd6e0",
        "line_soft": "#e2e8ef",
        "text": "#111820",
        "muted": "#526170",
        "faint": "#7d8996",
        "green": "#18794e",
        "cyan": "#0369a1",
        "violet": "#6d5bd0",
        "empty": "#e7edf2",
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
