"""Render parsed trending repos as Markdown."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from .parser import Repo

PERIOD_LABEL = {"daily": "今日 / Today", "weekly": "本周 / This week", "monthly": "本月 / This month"}


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def render_markdown(sections: dict[str, list[Repo]], language: str = "", now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    title = "GitHub Trending"
    if language:
        title += f" · {language}"
    lines = [f"# {title}", "", f"_Updated {now:%Y-%m-%d %H:%M} UTC_", ""]
    for period, repos in sections.items():
        lines += [f"## {PERIOD_LABEL.get(period, period)}", ""]
        if not repos:
            lines += ["_No repositories found._", ""]
            continue
        lines += ["| # | Repository | Language | ⭐ Stars | 📈 Gained | Description |",
                  "|---|---|---|---:|---:|---|"]
        for i, r in enumerate(repos, 1):
            lines.append(
                f"| {i} | [{r.name}]({r.url}) | {_cell(r.language) or '-'} | {r.stars:,} | "
                f"+{r.stars_gained:,} | {_cell(r.description) or '-'} |"
            )
        lines.append("")
    return "\n".join(lines)


def top_by_gain(repos: Iterable[Repo], n: int) -> list[Repo]:
    return sorted(repos, key=lambda r: r.stars_gained, reverse=True)[:n]
