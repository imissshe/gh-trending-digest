"""Command-line entry point: python -m trending_digest [options]."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from . import __version__
from .parser import parse_trending
from .render import render_markdown, top_by_gain

TRENDING_URL = "https://github.com/trending"
PERIODS = ("daily", "weekly", "monthly")


def fetch(period: str, language: str = "", spoken: str = "", timeout: float = 30.0) -> str:
    path = TRENDING_URL + (f"/{urllib.parse.quote(language.lower())}" if language else "")
    query = {"since": period}
    if spoken:
        query["spoken_language_code"] = spoken
    url = f"{path}?{urllib.parse.urlencode(query)}"
    req = urllib.request.Request(url, headers={"User-Agent": f"gh-trending-digest/{__version__}"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="trending-digest",
        description="Fetch GitHub Trending and print or save it as Markdown / JSON.",
    )
    p.add_argument("-p", "--period", choices=PERIODS + ("all",), default="daily",
                   help="time range (default: daily; 'all' = daily+weekly+monthly)")
    p.add_argument("-l", "--language", default="", help="programming language filter, e.g. python")
    p.add_argument("-s", "--spoken", default="", help="spoken language code, e.g. zh or en")
    p.add_argument("-n", "--limit", type=int, default=0, help="keep only the top N by stars gained")
    p.add_argument("-f", "--format", choices=("md", "json"), default="md", help="output format")
    p.add_argument("-o", "--output", type=Path, help="write to this file instead of stdout")
    p.add_argument("--from-html", type=Path, metavar="FILE",
                   help="parse a saved trending HTML page instead of fetching (offline/testing)")
    p.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    periods = PERIODS if args.period == "all" else (args.period,)
    sections = {}
    for period in periods:
        try:
            page = args.from_html.read_text(encoding="utf-8") if args.from_html else fetch(
                period, args.language, args.spoken)
        except Exception as exc:  # network errors, HTTP errors
            print(f"error: could not fetch {period} trending: {exc}", file=sys.stderr)
            return 1
        repos = parse_trending(page)
        if args.limit:
            repos = top_by_gain(repos, args.limit)
        sections[period] = repos

    if args.format == "json":
        text = json.dumps({k: [r.to_dict() for r in v] for k, v in sections.items()},
                          ensure_ascii=False, indent=2)
    else:
        text = render_markdown(sections, args.language)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
        total = sum(len(v) for v in sections.values())
        print(f"wrote {total} repos to {args.output}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
