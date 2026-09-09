# Startpad — Mission ↔ Tool Mapping

Maps every tool in the Startpad Tool Library onto the 15 missions of the
[startpad.me](https://startpad.me/) founder journey, and pairs each mission with curated
video and reading material.

**122 unique tools · 15 missions · 196 tool placements · 96 curated resources**

## Deliverables (`output/`)

| File | What it is |
|---|---|
| `Startpad_Mission_Tool_Matrix.xlsx` | 7 sheets: the mapping, a 122×15 coverage grid, a reverse tool→mission index, the Founder Toolkit shelves, the resource library, and 12 findings. |
| `Startpad_Mission_Playbook.docx` | The content/facilitator guide. One section per mission: questions, tools with rationale, resources, and a "done well" bar the AI evaluator can be tuned against. |
| `seed/*.csv` | Four CSVs shaped for direct import into Postgres: `tools`, `mission_tools`, `mission_resources`, `founder_toolkit`. Slugs are deterministic. |
| `startpad_mission_atlas.html` | Interactive browser for the whole mapping — [published artifact](https://claude.ai/code/artifact/c5c5f9e4-4f37-41a7-9034-c7ecd6c2cb78). |

## The three roles

Every tool is placed in one of three ways inside a mission, or on an always-available shelf
outside the mission flow. Nothing is left unplaced.

- **Core** — the founder cannot answer the mission's questions well without it. Render on the
  mission screen, already open.
- **Supporting** — recommended; sharpens or de-risks the answer. One click away in a rail.
- **Stretch** — optional, for a second pass. Collapsed under "go deeper".

Each placement also names the specific mission question (`Q1`…`Qn`) the tool's output should
populate, so the platform can pre-fill an answer field from the tool.

## Headline findings

1. The library holds **122 unique tools, not 123** — `Term Sheet Analyzer` is cross-listed on
   two tabs and counted twice.
2. **21 tools have no home in the 15 missions** — almost the entire fundraising block, most of
   the finance statements, and the team/governance tools. A founder who only follows missions
   never opens the Cap Table, the Pitch Deck template, or the Legal Checklist. Fix: a Founder
   Toolkit shelf plus a proposed Mission 16, "Raise Your Round".
3. **Missions 7 and 10 share a title** (`Solution Hypothesis Test`) and are indistinguishable in
   a sidebar. Rename M10 to "Prototype Hypothesis Test".
4. **Mission 13 ships an MVP with no analytics requirement**, then Mission 14 asks for retention
   and a PMF score. Gate M13 Q6 on an event taxonomy.
5. **Mission 14 asks founders to self-rate PMF 1-10** — exactly the unfalsifiable answer the
   platform's Evidence rubric pillar is built to catch. Replace with the Sean Ellis 40% survey.
6. **Nine tools are Core in three or more missions.** Make them stateful across missions — a
   Mission 2 persona should appear pre-filled in Missions 4, 11 and 12.

All 12 findings, with recommendations, are on the `Gaps & Recommendations` sheet, in the
playbook, and in the artifact's Findings tab.

## Source of truth

The mapping lives in Python so the four output formats can never drift apart:

```
startpad/tools.py       122 tools: category, description, framework reference, source tab
startpad/missions.py    the 15 missions, the mapping, and the Founder Toolkit shelves
startpad/resources.py   96 curated resources
```

## Rebuild

```bash
pip install openpyxl python-docx
python3 scripts/build_xlsx.py     output/Startpad_Mission_Tool_Matrix.xlsx
python3 scripts/build_docx.py     output/Startpad_Mission_Playbook.docx
python3 scripts/build_csv.py      output/seed
python3 scripts/build_artifact.py output/startpad_mission_atlas.html
```

All four outputs are byte-reproducible: rebuilding from unchanged sources produces
identical files, so a rebuild never shows up as a spurious diff. `.xlsx` and `.docx` are
ZIP containers that would otherwise bake wall-clock time into every entry and into
`docProps/core.xml`; `scripts/_determinism.py` pins both.

## Link verification — read before publishing resources

Every resource URL was returned by a **live web search** during compilation; none were written
from memory. The compiling environment's egress proxy blocked direct page fetches, so the links
are **search-index verified, not fetch-verified**. Titles marked `(T)` are as they appeared in
the search index and may differ slightly from the live page.

Run one check from an unrestricted network before publishing any of these to startpad.me, and
quarterly after. The checker flags YouTube videos that return HTTP 200 but are actually
unavailable, and exits non-zero so it can gate a publish step in CI:

```bash
python3 scripts/check_links.py
```

## Inputs

- `startpad15missions.md` — the 15 missions
- `Startpad — Tool Library (123 tools, Functional Categories).xlsx`
- `Startpad — Pitch Deck & One-Pager Template.docx`
- `startpaduserjourney.pdf` — the end-to-end user journey

---

# MENA Startup Programme Scout

A second deliverable in this repo: a scrape-ready registry of the organisations running
startup programmes across **Egypt, the GCC and the wider MENA region** (Israel excluded
per scoping).

**133 programme rows · 122 unique entities · 17 markets · 203 URLs queued for scraping**

## Deliverables

| File | What it is |
|---|---|
| `output/MENA_Startup_Programs_Scout.xlsx` | 6 sheets: READ ME FIRST, PROGRAMS, ENTITIES, **SCRAPE_CONFIG**, VOCAB, COVERAGE & GAPS. Dropdown validation on the controlled-vocabulary columns so hand-added rows stay machine-readable. |
| `output/scout/programs.csv` | The same programme table as flat CSV. |
| `scripts/scout_scraper.py` | Reads SCRAPE_CONFIG and reports programmes, flagging anything new. |

## How the automation works

`SCRAPE_CONFIG` is the machine-readable half of the workbook. The scraper reads it, visits
each enabled URL, and **auto-discovers** content rather than relying on hand-written CSS
selectors — which would have been written blind and would silently break:

1. **RSS / Atom** — declared `<link rel=alternate>`, or a guessed `/feed`, `/rss`, `/atom.xml`
2. **sitemap.xml** — filtered to programme-looking paths (one level of index expansion)
3. **JSON-LD** — schema.org `Event` / `Course` / `NewsArticle` / `ItemList`
4. **HTML heuristic** — repeated link structures matching programme wording, English *and* Arabic

The tier that fired is recorded per row, so you can see how each source was read. If a site
later publishes a feed, it is picked up automatically with no code change.

`state.json` holds a fingerprint of every item ever seen, so anything new lands in
`output/scout/new_programs.csv`. **Add a row to SCRAPE_CONFIG and the next run picks it up.**

Politeness is built in: robots.txt honoured per host, one request at a time with a delay,
a real User-Agent, and a cap on items per source.

```bash
pip install requests beautifulsoup4 lxml openpyxl
python3 scripts/build_scout_xlsx.py output/MENA_Startup_Programs_Scout.xlsx
python3 scripts/scout_scraper.py --verify-only     # resolve every URL, record status
python3 scripts/scout_scraper.py                   # full discovery pass
python3 scripts/scout_scraper.py --since-last      # only what is new
python3 scripts/scout_scraper.py --country Egypt --priority 1
```

## Verification status — read before relying on a row

Every URL came from a **live web search**. None were written from memory. But the compiling
environment's egress proxy blocked *every* outbound request (verified against flat6labs.com,
magnitt.com, wamda.com, itida.gov.eg, hub71.com, oasis500.com, sheraa.ae, startupqatar.qa),
so **no page was ever opened**.

**Three expansion-and-verification passes have been run.** Each weak entity was re-queried by
name, and a URL was kept only when it came back as an actual indexed search-result *link*
rather than being named in prose. That moved the confidence split from
`high` 46 / `medium` 17 / `low` 25 to **`high` 98 / `medium` 23 / `low` 12**, and grew the
registry from 88 rows to **133**.

Verification caught three factual errors that would otherwise have shipped:

- **Cairo Angels has rebranded to Acasia** — the row is renamed.
- **Wa'ed** resolves at `waed.com`, not the `waed.net` an article's prose gave.
- **212Founders** resolves at `.co`, not the `.ma` cited in a Morocco funding guide.

TIEC and Startup Egypt also turned out to run their own government domains (`tiec.gov.eg`,
`startup.gov.eg`) rather than sitting under ITIDA as first assumed.

One row carries a **security caution**: Endeavor Egypt's `endeavoreg.org` resolves, but its
`/contact/` page returned a gambling-spam page title in search results, suggesting part of the
domain may be compromised or parked.

Twelve rows remain `low` — EdVentures, Innoventures, Egypt Fund of Funds, Nclude, KAUST
Innovation Fund, Riyadh Valley Company, SVC, Badir, The Garage, Startupbootcamp Dubai, Oman's
Ithraa and Kuwait's National Fund — with no official domain returned as an indexed link. Each
carries a profile, government or coverage URL as a working placeholder and says so. Several are
major institutions whose own sites are simply poorly indexed: **SVC and The Garage are certainly
real — it is the URL, not the entity, that is unconfirmed.**

Run `--verify-only` from a normal network first; it writes an `http_status` back for every source.

The scraper's four parser tiers were tested offline against fixtures (JSON-LD extraction,
HTML heuristic including Arabic, noise exclusion, fingerprint stability) and the error path
was exercised by the blocked network — failures log per source rather than aborting the run.

---

# StartPad × GrowthLabs — LEAP launch press release

A third deliverable: the bilingual launch announcement for StartPad at LEAP, and for
GrowthLabs' full, **non-cash** adoption of the platform.

| File | What it is |
|---|---|
| `press/release.py` | Source of truth for the copy, Arabic and English. |
| `output/StartPad_LEAP_Launch_Press_Release.docx` | Both languages in one document — Arabic first with real RTL, English after, fact-check sources last. |
| `press/startpad_leap_launch_ar.md`, `..._en.md` | Plain-text copy for wire submission forms, email and LinkedIn. |
| `press/fact_check_sources.md` | Where each figure came from. |
| `output/startpad_press_kit.html` | The press-kit page — [published artifact](https://claude.ai/code/artifact/28a2e66e-5e91-4017-bb4f-0967e6387f3d). |

```bash
pip install python-docx
python3 scripts/build_press_docx.py     output/StartPad_LEAP_Launch_Press_Release.docx
python3 scripts/build_press_md.py       press
python3 scripts/build_press_artifact.py output/startpad_press_kit.html
```

## Two things to check before it goes out

**Placeholders.** Anything still to be supplied is written in `[SQUARE BRACKETS]` —
media contacts, pricing, and the proposed GrowthLabs quote, which needs its speaker's
approval. The press-kit page marks them in bronze so none can slip through.

**Figures.** Every number came from a live web search at drafting time, listed in
`press/fact_check_sources.md`. As with the rest of this repo, the egress proxy blocked
direct page fetches, so confirm them against the live pages before distribution.

---

# Mission Zero — the StartPad × Techne youth competition

A national youth challenge where the entry ticket is finishing StartPad missions, launched at
Techne Summit 2026 (Cairo 26–27 Sept, Alexandria 3–5 Oct).

| File | What it is |
|---|---|
| `output/mission_zero_playbook.html` | The plan — format, eligibility, judging, prizes, funnel targets, timeline, budget and risks. [Published artifact](https://claude.ai/code/artifact/52089729-b58d-441f-b539-1125d5974e0e). |
| `competition/proposal.py` | Source of truth for the partnership proposal and its covering email. |
| `output/StartPad_Techne_Partnership_Proposal.docx` | Two pages to attach, plus the email to send. |

```bash
python3 scripts/build_techne_proposal_docx.py output/StartPad_Techne_Partnership_Proposal.docx
```

The plan turns on three findings about Techne: they already run the national youth roadshow
competition (Techne Drifts, 14 cities), their Compete track is hosting a Startup World Cup
tournament with a USD 1M headline prize, and their summit is 17 days away. So this is positioned as
a **feeder into** their track rather than a rival to it, the summit is used as the launchpad rather
than the finale, and cash is deliberately the third thing a participant hears about.

Dates and figures came from live web search on 9 September 2026; the egress proxy blocked page
fetches, so reconfirm them with Techne in the first email.
