"""Parse the HTML of https://github.com/trending into plain dicts (stdlib only)."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, asdict

_ARTICLE_RE = re.compile(r'<article class="Box-row">(.*?)</article>', re.S)
_NAME_RE = re.compile(r'<h2[^>]*>\s*<a[^>]*href="/([^"/]+/[^"/]+)"', re.S)
_DESC_RE = re.compile(r'<p class="col-9[^"]*">(.*?)</p>', re.S)
_LANG_RE = re.compile(r'itemprop="programmingLanguage">([^<]+)<', re.S)
_STARS_RE = re.compile(r'href="/[^"]+/stargazers"[^>]*>.*?</svg>\s*([\d,]+)', re.S)
_FORKS_RE = re.compile(r'href="/[^"]+/forks"[^>]*>.*?</svg>\s*([\d,]+)', re.S)
_GAIN_RE = re.compile(r'([\d,]+)\s+stars?\s+(today|this week|this month)', re.S)
_TAG_RE = re.compile(r"<[^>]+>")


@dataclass
class Repo:
    name: str
    url: str
    description: str
    language: str
    stars: int
    forks: int
    stars_gained: int
    period: str

    def to_dict(self) -> dict:
        return asdict(self)


def _int(text: str | None) -> int:
    return int(text.replace(",", "")) if text else 0


def _clean(text: str) -> str:
    return " ".join(html.unescape(_TAG_RE.sub("", text)).split())


def parse_trending(page: str) -> list[Repo]:
    """Return the repositories listed on a GitHub Trending HTML page."""
    repos: list[Repo] = []
    for block in _ARTICLE_RE.findall(page):
        name_m = _NAME_RE.search(block)
        if not name_m:
            continue
        name = name_m.group(1).strip()
        desc_m = _DESC_RE.search(block)
        lang_m = _LANG_RE.search(block)
        stars_m = _STARS_RE.search(block)
        forks_m = _FORKS_RE.search(block)
        gain_m = _GAIN_RE.search(block)
        repos.append(
            Repo(
                name=name,
                url=f"https://github.com/{name}",
                description=_clean(desc_m.group(1)) if desc_m else "",
                language=lang_m.group(1).strip() if lang_m else "",
                stars=_int(stars_m.group(1) if stars_m else None),
                forks=_int(forks_m.group(1) if forks_m else None),
                stars_gained=_int(gain_m.group(1) if gain_m else None),
                period=gain_m.group(2) if gain_m else "",
            )
        )
    return repos
