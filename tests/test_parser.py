import unittest
from pathlib import Path

from trending_digest.parser import parse_trending
from trending_digest.render import render_markdown, top_by_gain

FIXTURE = Path(__file__).with_name("fixture_daily.html")


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.repos = parse_trending(FIXTURE.read_text(encoding="utf-8"))

    def test_parses_repos(self):
        self.assertGreater(len(self.repos), 5)
        for r in self.repos:
            self.assertRegex(r.name, r"^[\w.-]+/[\w.-]+$")
            self.assertTrue(r.url.startswith("https://github.com/"))
            self.assertGreaterEqual(r.stars, r.stars_gained)

    def test_period_detected(self):
        self.assertTrue(all(r.period == "today" for r in self.repos))

    def test_render_and_sort(self):
        top = top_by_gain(self.repos, 3)
        self.assertEqual(len(top), 3)
        self.assertGreaterEqual(top[0].stars_gained, top[-1].stars_gained)
        md = render_markdown({"daily": top})
        self.assertIn("| # | Repository |", md)
        self.assertIn(top[0].url, md)

    def test_empty_page(self):
        self.assertEqual(parse_trending("<html></html>"), [])


if __name__ == "__main__":
    unittest.main()
