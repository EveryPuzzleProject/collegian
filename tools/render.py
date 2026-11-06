#!/usr/bin/env python3
"""Render the Daily Collegian status page, site/index.html (plus copies of
puzzles.tsv and exceptions.tsv), from puzzles.tsv and exceptions.tsv. Runs in
CI on every push to main; locally:

    python tools/render.py

The Collegian is in copyright: the page shows metadata only (date, page,
state) and links each issue to its page in the Pennsylvania Newspaper Archive,
never page images, clues or grids.
"""
import calendar
import collections
import csv
import datetime as dt
import html
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = "https://everypuzzleproject.org/"
REPO = "https://github.com/EveryPuzzleProject/collegian"
ISSUES = REPO + "/issues"
BLOG = "https://blitz.xwordapp.com/blog/collegian.html"
BLITZ = "https://github.com/EveryPuzzleProject/blitz"
XD = "https://github.com/century-arcade/xdformat"
GAMES = "https://everypuzzleproject.org/games/"
ARCHIVE = "https://panewsarchive.psu.edu/lccn/sn85054904/"
# The archive has no issues in this stretch, so the run's true start is unknown.
GAP = (dt.date(1975, 12, 20), dt.date(1976, 3, 10))

# puzzles.tsv status -> (label, colour), in display order.
STATES = {
    "found": ("Puzzle located", "#3f8f5f"),
    "absent": ("No puzzle that day", "#c9a46a"),
    "unsure": ("Under review", "#3b6fb6"),
}
# exceptions.tsv kind -> short public description; unknown kinds fall back to the note.
KINDS = {
    "no-puzzle": "No crossword was printed; the next day's paper apologized and reprinted the grid.",
    "reprint-stub": "The front page reprints the grid left out of the day before, with no clues "
                    "(\"We can't think of anything else you could possibly need\"). The issue's regular puzzle is on page 4.",
    "ephemera": "A help-wanted ad in the puzzle's place: Mike Shenk \"has secured a job with GAMES Magazine\" "
                "and the paper is looking for \"two or three bright, witty persons to take his place\".",
    "flag-on-import": "A puzzle titled \"Nazism\" whose black squares form a swastika, with clues on Nazi Germany. "
                      "It will be kept, under its title, and flagged when it's imported.",
}


def e(s) -> str:
    return html.escape(str(s or ""))


def read(name: str) -> list[dict]:
    with open(ROOT / name, encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE) if r.get("date")]


def issue_url(date: str, seq: str = "") -> str:
    """The issue's page in the archive (its puzzle page when seq is known)."""
    return f"{ARCHIVE}{date}/ed-1/" + (f"seq-{seq}/" if seq and seq != "-" else "")


def nice(d: dt.date) -> str:
    return f"{d.day} {d:%B} {d.year}"


def main() -> None:
    rows = sorted(read("puzzles.tsv"), key=lambda r: r["date"])
    exceptions = read("exceptions.tsv")
    by_date = {r["date"]: r for r in rows}
    count = collections.Counter(r["status"] for r in rows)
    label = lambda s: STATES.get(s, (s, ""))[0]
    total = len(rows)
    found, absent, unsure = count["found"], count["absent"], count["unsure"]
    first_d, last_d = dt.date.fromisoformat(rows[0]["date"]), dt.date.fromisoformat(rows[-1]["date"])

    def cell(d: dt.date) -> str:
        pos = f'style="grid-column:{d.weekday() + 1};grid-row:{week_row(d)}"'
        r = by_date.get(d.isoformat())
        if r is None:
            if GAP[0] <= d <= GAP[1]:
                return f'<span class="day gap" {pos} title="{nice(d)}: no issues in the archive"></span>'
            return f'<span class="day none" {pos}></span>'
        st = r["status"]
        t = f"{nice(d)}: {label(st)}" + (f", page {r['page']}" if r["page"] else "")
        href = r["archive_url"] or issue_url(r["date"])
        return f'<a class="day st-{e(st)}" {pos} href="{e(href)}" title="{e(t)}" aria-label="{e(t)}"></a>'

    def week_row(d: dt.date) -> int:
        first = d.replace(day=1)
        while first.weekday() > 4:  # a month starting on a weekend starts its grid on the Monday after
            first += dt.timedelta(days=1)
        start = first - dt.timedelta(days=first.weekday())  # Monday of the month's first weekday's week
        return (d - start).days // 7 + 1

    def month(y: int, m: int) -> str:
        days = [dt.date(y, m, n) for n in range(1, calendar.monthrange(y, m)[1] + 1)]
        days = [d for d in days if d.weekday() < 5]  # the paper ran Monday to Friday
        ms = [by_date[d.isoformat()] for d in days if d.isoformat() in by_date]
        n = sum(r["status"] == "found" for r in ms)
        note = f"{n} of {len(ms)}" if ms else ("archive gap" if any(GAP[0] <= d <= GAP[1] for d in days) else "no issues")
        return (f'<div class="month"><div class="mh">{calendar.month_abbr[m]}<small>{note}</small></div>'
                f'<div class="cal">{"".join(cell(d) for d in days)}</div></div>')

    years = []
    for y in range(first_d.year, last_d.year + 1):
        hi = last_d.month if y == last_d.year else 12
        ys = [r for r in rows if r["date"].startswith(str(y))]
        yn = sum(r["status"] == "found" for r in ys)
        years.append(f'<section class="year"><h3>{y} <small>{yn} puzzles in {len(ys)} issues</small></h3>'
                     f'<div class="months">{"".join(month(y, m) for m in range(1, hi + 1))}</div></section>')

    bar = "".join(f'<span class="st-{s}" style="width:{100 * count[s] / total:.3f}%" title="{e(label(s))}: {count[s]}"></span>'
                  for s in STATES if count[s])
    legend = "".join(f'<span><i class="sw st-{s}"></i><b>{count[s]}</b> {e(label(s).lower())}</span>' for s in STATES) + \
        '<span><i class="sw none"></i>no issue in the archive</span>' \
        '<span><i class="sw gap"></i>archive gap</span>'

    groups = collections.defaultdict(list)  # kind -> rows, in first-seen order
    for x in exceptions:
        groups[x["kind"]].append(x)

    def ex_link(x) -> str:
        d = dt.date.fromisoformat(x["date"])
        page = f", p. {x['seq']}" if x["seq"] and x["seq"] != "-" else ""
        return f'<a href="{e(issue_url(x["date"], x["seq"]))}">{e(nice(d))}{page}</a>'

    ex_items = "\n".join(
        f'<li><span class="dates">{", ".join(ex_link(x) for x in xs)}</span><br>{e(KINDS.get(kind, xs[0]["note"]))}</li>'
        for kind, xs in sorted(groups.items(), key=lambda kv: kv[1][0]["date"]))

    states_css = "\n".join(f".st-{s} {{ background:{c}; }}" for s, (_, c) in STATES.items())

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Daily Collegian crosswords</title>
<meta name="description" content="Every Puzzle Project: an index of Mike Shenk's daily crosswords in Penn State's Daily Collegian, 1976–1981.">
<style>
:root {{ --bg:#fbfaf7; --fg:#1d1d1b; --muted:#6b6a65; --line:#e3e0d8; --card:#fff; --accent:#8a1c1c; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#161614; --fg:#ecebe6; --muted:#a3a19a; --line:#34332f; --card:#1f1f1c; --accent:#e07a6a; }} }}
:root[data-theme="dark"] {{ --bg:#161614; --fg:#ecebe6; --muted:#a3a19a; --line:#34332f; --card:#1f1f1c; --accent:#e07a6a; }}
* {{ box-sizing:border-box }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:16px/1.55 Georgia, "Times New Roman", serif }}
main {{ max-width:960px; margin:0 auto; padding:24px 16px 64px }}
nav.top {{ font:14px system-ui, sans-serif; display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap }}
h1 {{ font-size:2.1rem; line-height:1.2; margin:20px 0 10px }}
h2 {{ margin:40px 0 10px; font-size:1.35rem; border-bottom:2px solid var(--fg); padding-bottom:4px }}
h3 {{ margin:24px 0 8px; font-size:1.1rem }} h3 small {{ font:13px system-ui, sans-serif; color:var(--muted); margin-left:6px }}
a {{ color:var(--accent) }} .muted {{ color:var(--muted) }} .lede {{ font-size:1.1rem; max-width:44em }}
.sans {{ font-family:system-ui, sans-serif }} .note {{ font:14px system-ui, sans-serif; color:var(--muted); max-width:52em }}
.stats {{ display:flex; flex-wrap:wrap; gap:12px 36px; margin:16px 0 0 }}
.stat {{ font:700 40px/1 Georgia, serif }} .stat small {{ display:block; font:500 14px system-ui, sans-serif; color:var(--muted); margin-top:6px }}
.bar {{ display:flex; gap:2px; height:16px; border-radius:8px; overflow:hidden; background:var(--line); margin:18px 0 10px }}
.bar span {{ display:block; height:100% }}
.legend {{ display:flex; flex-wrap:wrap; gap:6px 18px; font:14px system-ui, sans-serif; color:var(--muted) }}
.legend b {{ color:var(--fg); font-weight:600 }}
.sw {{ display:inline-block; width:12px; height:12px; border-radius:2px; margin-right:6px; vertical-align:-1px }}
{states_css}
.none {{ box-shadow:inset 0 0 0 1px var(--line) }}
.gap {{ background:repeating-linear-gradient(135deg, var(--muted) 0 1.5px, transparent 1.5px 4px); opacity:.55 }}
.months {{ display:flex; flex-wrap:wrap; gap:14px 14px }}
.month {{ width:62px }}
.mh {{ font:600 13px system-ui, sans-serif; margin-bottom:4px }} .mh small {{ display:block; white-space:nowrap; font-weight:400; font-size:11px; color:var(--muted) }}
.cal {{ display:grid; grid-template-columns:repeat(5, 10px); grid-auto-rows:10px; gap:3px }}
.day {{ display:block; border-radius:2px }}
a.day:hover, a.day:focus {{ outline:2px solid var(--fg); outline-offset:1px }}
.exceptions {{ padding-left:20px; font-family:system-ui, sans-serif; font-size:15px }} .exceptions li + li {{ margin-top:10px }}
.exceptions .dates {{ font-weight:600 }}
.cta {{ background:var(--card); border:1px solid var(--line); border-left:4px solid var(--accent); padding:14px 20px }}
.cta ul, .next {{ margin:0; padding-left:20px }} .cta li + li, .next li + li {{ margin-top:8px }}
footer {{ margin-top:48px; font:13px system-ui, sans-serif; color:var(--muted) }}
@media (max-width:560px) {{ h1 {{ font-size:1.6rem }} .stat {{ font-size:32px }} .months {{ gap:12px 10px }} }}
</style></head><body><main>
<nav class="top"><a href="{HOME}">← Every Puzzle Project</a><a href="{REPO}">EveryPuzzleProject/collegian on GitHub</a></nav>

<h1>Mike Shenk's crosswords in <i>The Daily Collegian</i>, {first_d.year}–{last_d.year}</h1>
<p class="lede">Mike Shenk, who later edited the <i>Wall Street Journal</i> crossword, was a Penn State student when the
<i>Collegian</i> started running his daily puzzle; the first with his byline is 12 March 1976. The archive has no issues from
December 1975 to March 1976, so the true start of the run falls somewhere in that gap and can't be pinned down. In June 1981 the
paper ran a help-wanted ad in the puzzle's place: he had left for <a href="{GAMES}"><i>GAMES</i></a> magazine. We've found which page the
crossword is on in every issue the archive holds, the first step to preserving the puzzles and making them searchable as
<a href="{XD}">xd</a> files.</p>
<p class="note">The <i>Collegian</i> is in copyright, so this page holds no images. Every square links to the issue in the
<a href="{ARCHIVE}">Pennsylvania Newspaper Archive</a>, which is open to all, with page images. More in the
<a href="{BLOG}">blog post</a>.</p>

<h2>Coverage</h2>
<div class="stats">
<div class="stat">{total}<small>issues in the archive</small></div>
<div class="stat">{found}<small>puzzle located</small></div>
<div class="stat">{absent}<small>no puzzle that day</small></div>
<div class="stat">{unsure}<small>under review</small></div>
</div>
<div class="bar">{bar}</div>
<div class="legend">{legend}</div>
<p class="note">Every issue has been looked at by a person. Most of the days without a puzzle are summer-session issues.</p>

<h2>Issue by issue</h2>
<p class="note" style="margin:0">One square per weekday, Monday to Friday across. Hover a square for its date and page; click it to open
the page in the archive.</p>
{"".join(years)}

<h2>Exceptions</h2>
<ul class="exceptions">
{ex_items}
</ul>

<h2>What's next</h2>
<ol class="next sans">
<li>Fetch the puzzle page images from the archive.</li>
<li>Collect the answers, which were printed in the next day's classifieds.</li>
<li>Read each puzzle into an <a href="{XD}">xd</a> file.</li>
</ol>

<h2>How you can help</h2>
<div class="cta sans"><ul>
<li><b>Have <i>Collegian</i> issues from December 1975 to March 1976?</b> They're missing from the archive, and Shenk's first puzzles
may be in them. <a href="{ISSUES}">Open an issue</a>.</li>
<li><b>Know of Mike Shenk puzzles elsewhere</b> from these years? <a href="{ISSUES}">Open an issue</a> too.</li>
</ul></div>

<footer>Part of the <a href="{HOME}">Every Puzzle Project</a>. Data: <a href="{REPO}">EveryPuzzleProject/collegian</a>
(<a href="puzzles.tsv">puzzles.tsv</a>, <a href="exceptions.tsv">exceptions.tsv</a>), written by the <a href="{BLITZ}">blitz</a> tools.
More in the <a href="{BLOG}">blog post</a>. Generated {dt.date.today().isoformat()}.</footer>
</main></body></html>
"""
    out = ROOT / "site"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8", newline="\n")
    for name in ("puzzles.tsv", "exceptions.tsv"):
        shutil.copy(ROOT / name, out / name)
    print(f"site/index.html: {total} issues, {dict(count)}, {len(exceptions)} exceptions")


if __name__ == "__main__":
    main()
