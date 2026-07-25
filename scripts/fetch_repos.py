#!/usr/bin/env python3
"""
Fetch recent public GitHub repositories (unauthenticated API) into data/repos.json.

Used to optionally refresh the "Latest repos" section. Falls back gracefully on
rate limits or network failures.

Usage
-----
    python scripts/fetch_repos.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

import requests

from common import ensure_parent, setup_logging
from config import (
    GITHUB_REPOS_API,
    GITHUB_USERNAME,
    REPO_FETCH_LIMIT,
    REPOS_JSON,
    REQUEST_TIMEOUT,
    USER_AGENT,
)

logger = setup_logging("fetch_repos")


def fetch_repos(limit: int = REPO_FETCH_LIMIT) -> list[dict[str, Any]]:
    """Return a list of recent non-fork public repos."""
    params = {
        "sort": "updated",
        "direction": "desc",
        "per_page": min(max(limit * 2, 10), 100),
        "type": "owner",
    }
    try:
        resp = requests.get(
            GITHUB_REPOS_API,
            params=params,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/vnd.github+json",
            },
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
    except requests.Timeout as exc:
        raise RuntimeError(f"GitHub API timed out after {REQUEST_TIMEOUT}s") from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"GitHub API request failed: {exc}") from exc

    repos_raw = resp.json()
    repos: list[dict[str, Any]] = []
    for repo in repos_raw:
        if repo.get("fork"):
            continue
        if repo.get("name") == GITHUB_USERNAME:
            continue  # skip the profile repo itself
        repos.append(
            {
                "name": repo.get("name"),
                "description": repo.get("description") or "",
                "url": repo.get("html_url"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count", 0),
                "updated_at": repo.get("updated_at"),
            }
        )
        if len(repos) >= limit:
            break
    return repos


def save_repos(repos: list[dict[str, Any]], out: Path = REPOS_JSON) -> dict[str, Any]:
    """Write repos payload to disk."""
    payload = {
        "username": GITHUB_USERNAME,
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repos": repos,
    }
    ensure_parent(out)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    logger.info("wrote %s (%d repos)", out, len(repos))
    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=REPO_FETCH_LIMIT)
    parser.add_argument("--output", type=Path, default=REPOS_JSON)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        repos = fetch_repos(limit=args.limit)
        save_repos(repos, out=args.output)
    except RuntimeError as exc:
        logger.error("%s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        logger.exception("unexpected failure: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
