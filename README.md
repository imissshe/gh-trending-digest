# gh-trending-digest

[![CI](https://github.com/imissshe/gh-trending-digest/actions/workflows/ci.yml/badge.svg)](https://github.com/imissshe/gh-trending-digest/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

把 [GitHub Trending](https://github.com/trending) 抓下来，整理成 Markdown 表格或 JSON。纯 Python 标准库，零依赖。
A tiny, dependency-free Python CLI that turns GitHub Trending into a Markdown table or JSON.

👉 每日自动更新的榜单 / Auto-updated digest: [trending.md](trending.md)

## 功能 / Features

- 今日 / 本周 / 本月热门，或三者合并 — daily, weekly, monthly, or all three
- 按编程语言、自然语言（如 `zh`）过滤 — filter by programming or spoken language
- 按新增 star 数排序取前 N — keep the top N by stars gained
- 输出 Markdown 或 JSON，打印或写入文件 — Markdown or JSON, to stdout or a file
- GitHub Actions 每天自动刷新 `trending.md` — a scheduled workflow refreshes `trending.md` daily

## 用法 / Usage

```bash
git clone https://github.com/imissshe/gh-trending-digest
cd gh-trending-digest

python -m trending_digest                      # 今日热门 / today's trending
python -m trending_digest -p weekly -n 10      # 本周新增 star 最多的 10 个
python -m trending_digest -l python -p monthly # 本月 Python 热门
python -m trending_digest -s zh                # 中文项目
python -m trending_digest -p all -o trending.md
python -m trending_digest -f json > trending.json
```

也可以安装成命令 / Or install as a command:

```bash
pip install .
trending-digest -p weekly -n 5
```

| 参数 Option | 说明 Description |
|---|---|
| `-p, --period` | `daily` / `weekly` / `monthly` / `all` |
| `-l, --language` | 编程语言 programming language, e.g. `python`, `rust` |
| `-s, --spoken` | 自然语言代码 spoken language code, e.g. `zh`, `en` |
| `-n, --limit` | 只保留新增 star 最多的 N 个 keep top N by stars gained |
| `-f, --format` | `md` 或 or `json` |
| `-o, --output` | 输出文件 output file |
| `--from-html` | 解析本地保存的页面（离线测试）parse a saved page offline |

## 输出示例 / Example output

| # | Repository | Language | ⭐ Stars | 📈 Gained | Description |
|---|---|---|---:|---:|---|
| 1 | [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) | Python | 48,344 | +2,371 | DeepTutor: Lifelong Personalized Tutoring. |

## 测试 / Tests

```bash
python -m unittest discover -s tests -v
```

## 说明 / Notes

GitHub 没有官方 Trending API，本工具解析公开网页，页面改版时可能需要调整解析规则。
GitHub has no official Trending API; this tool parses the public page, so a page redesign may need a parser update.

## License

[MIT](LICENSE)
