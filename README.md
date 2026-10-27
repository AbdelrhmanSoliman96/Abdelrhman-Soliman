# منصة مسار (Masar)

موقع ثابت (Static) كامل مبني من تصاميم Stitch دون أي تغيير في التصميم. كل صفحة هي نفس الـ HTML الأصلي، مع ربط الروابط بين الصفحات وطبقة تنقل مشتركة في `assets/site.js`.

## التشغيل
```
python3 -m http.server 8000   # ثم افتح http://localhost:8000
```
تحتاج الصفحات اتصالاً بالإنترنت لتحميل Tailwind CDN والخطوط (كما في التصميم الأصلي).

## الصفحات
- **الواجهة العامة:** `index` · `store` · `product` · `compare` · `knowledge` · `article` · `trust-wall` · `verify-license` · `help-center` · `privacy` · `about` · `404`
- **الشراء:** `cart-added` → `checkout` / `guest-checkout` → `payment-processing` → `order-confirmed` (و`payment-failed`)
- **الحساب:** `login` · `register` → `onboarding` → `dashboard`
- **المستثمر:** `dashboard` · `valuation` · `kpi-entry` · `billing` · `company-profile` · `executive-ops` · `ai-assistant` · `ai-generating` · `pitch-deck` · `data-room` · `vdr-upload`
- **الاستشارات:** `advisory-booking` · `consultant-portal` · `waiting-lobby` → `live-room` → `session-evaluation`
- **الإدارة:** `admin-sales` · `admin-products` · `admin-add-model` · `admin-reports` · `admin-disputes` · `admin-licenses`
- **الشركاء والمطورون:** `partner-portal` · `developers-api`
- **الهوية:** `brand-guide` · `assets/masar-logo.svg`

---

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

A national youth challenge where the entry ticket is finishing all 15 StartPad missions in one
month, launched from the Techne Summit Alexandria stage (3–5 October 2026).

| File | What it is |
|---|---|
| `output/mission_zero_playbook.html` | The plan — the mutual-value case, format, four-week structure, judging, prizes, funnel targets, timeline, budget and risks. [Published artifact](https://claude.ai/code/artifact/52089729-b58d-441f-b539-1125d5974e0e). |
| `competition/proposal.py` | Source of truth for the partnership proposal and its covering email. |
| `output/StartPad_Techne_Partnership_Proposal.docx` | Two pages to attach, plus the email to send. |

```bash
python3 scripts/build_techne_proposal_docx.py output/StartPad_Techne_Partnership_Proposal.docx
```

## The operating pack — what actually gets published

The playbook is for the team. These are the assets a participant, a judge and a landing
page need on day one.

| File | What it is |
|---|---|
| `competition/rules.py` | Source of truth for the participant-facing pack, Arabic and English. |
| `output/Mission_Zero_Rules_AR_EN.docx` | Rules, schedule, definitions of done, the published rubric, IP and data terms. Arabic first with real RTL — including `w:bidiVisual` on tables, so Arabic columns read right-to-left too. |
| `output/mission_zero_rules.html` | The page entrants read, Arabic by default. [Published artifact](https://claude.ai/code/artifact/c9f6324a-cc90-4493-b0d3-e272ba6232b4) — usable as the QR destination at the booth before the real landing page exists. |
| `output/Mission_Zero_Judging_Pack.xlsx` | Judging workbook: rubric, scoresheet with weighted formulas, shortlist, verification log, vocab. |

```bash
python3 scripts/build_rules_docx.py     output/Mission_Zero_Rules_AR_EN.docx
python3 scripts/build_rules_artifact.py output/mission_zero_rules.html
python3 scripts/build_judging_xlsx.py   output/Mission_Zero_Judging_Pack.xlsx
```

The judging workbook reads its weights out of `competition/rules.py`, so the sheet a judge
scores on cannot disagree with the rubric published to entrants. Pillar scores are entered
0–5 and the weighted total is a formula — nobody hand-computes a percentage at Demo Day.
Two columns exist because of how this competition can fail rather than because a scoring
sheet usually has them: a conflict-of-interest flag declared before scores are entered, and
a log for the verification calls placed to people finalists claim to have interviewed.

Three findings about Techne shape the plan: they already run the national youth roadshow competition
(Techne Drifts, 14 cities), their Compete track is hosting a Startup World Cup tournament with a
USD 1M headline prize, and their summit is 24 days away. So this is positioned as a **feeder into**
their track rather than a rival, eligibility structurally excludes anyone with a company, funding or
revenue, and cash is deliberately the third thing a participant hears about.

The one hard problem is fitting all 15 missions into 30 days: missions 9, 13 and 14 ask for a
prototype, an MVP and a product-market-fit test. The plan solves it by publishing narrow definitions
of done — a clickable prototype rather than code, a manual MVP with 10 real users, and a demand-signal
test rather than a self-rated PMF score — and by setting a tripwire to reduce the requirement
publicly and early if week 2 completion runs short.

Dates and figures came from live web search on 9 September 2026; the egress proxy blocked page
fetches, so reconfirm them with Techne in the first email.

---

# Founder template library — 10 tools, English and Arabic

Twenty downloadable Word files for the `/resources` page: ten templates, each in
English and Arabic, one template per file. Every file is four parts — a cover, a page
explaining the tool and citing where it came from, the fillable template itself, and a
closing page about StartPad.

| # | Template | Missions it serves |
|---|---|---|
| 1 | Lean Canvas | 5, 6, 8 |
| 2 | Business Model Canvas | 8 → 11, 15 |
| 3 | Value Proposition Canvas | 6, 11, 12 |
| 4 | Customer Persona | 2, 4 → 11, 12, 15 |
| 5 | Customer Interview Script & Evidence Log | 1, 2, 3 → 7, 10, 12, 14 |
| 6 | Importance–Frequency Matrix | 3 → 4, 5 |
| 7 | SWOT & TOWS Analysis | 5, 15 |
| 8 | PESTEL Analysis | 2, 12 |
| 9 | Competitive Moat & Five Forces | 4, 5, 15 |
| 10 | Market Sizing — TAM, SAM, SOM | 4, 12 |

```bash
pip install python-docx pillow
python3 scripts/build_template_docx.py output/templates
python3 scripts/check_docx_order.py    output          # gate before publishing
```

Source of truth is `templates/catalog_en.py` and `templates/catalog_ar.py`, with shared
page furniture in `templates/strings.py`. The Arabic is composed in Arabic, not
translated — the brand guidelines are explicit that a translation reads as one — and
both catalogues are asserted to share identical grid geometry, so a box added to one
must be added to the other.

## Brand

Taken from the 2026 brand presentation and encoded in `scripts/build_template_docx.py`:

- **Lime `#CBF24A`** is a ground, never ink. At 1.29:1 on white it cannot carry type, so
  it fills band headings and rules and sets no body copy anywhere in these files.
- **Ultraviolet `#3418E0`** carries white type at 8.9:1 and is therefore the cover surface.
- **Ink `#0B0E14`** and white do the reading.
- **Satoshi** sets Latin, **Zain** sets Arabic. Both are named in the files; Word
  substitutes if they are not installed locally, and the document still opens correctly.
- One language per asset, so English and Arabic are separate files rather than facing
  columns.
- Logo lockups live in `brand/logo/` — horizontal is the document default, white on the
  ultraviolet cover, ink on the lime closing band.

## Why there is an XML order checker

WordprocessingML property containers are `xsd:sequence`: `w:bidi` must precede
`w:spacing` and `w:jc` inside `w:pPr`, `w:bidiVisual` must precede `w:tblBorders` inside
`w:tblPr`. Word reorders silently on open, which hides the mistake; other readers are
stricter. `scripts/_ooxml.py` inserts every hand-built element at its schema position and
`scripts/check_docx_order.py` proves it, exiting non-zero so it can gate a publish step.

Running it caught genuine violations in four documents built earlier in this repo — the
playbook, the press release, the competition rules and the Techne proposal. All four
builders now go through the same helpers, and all 24 `.docx` in `output/` pass.

---

# Founder resource library — seventeen PDFs

Five guided toolkits a founder fills in, three mini whitepapers that each explain one
thing, eight reports that read a framework from the brand book as an operating tool, and
one partner review. **129 pages**, all English, all vector, built for the `/resources` page and for
printing.

| # | Document | Missions | Pages |
|---|---|---|---|
| WP 01 | The Readiness Gap | 1, 2 | 7 |
| TK 01 | The Readiness Audit | 1, 2 | 12 |
| TK 02 | The Evidence Toolkit | 2, 3, 7 | 10 |
| WP 02 | Market Sizing Without Lying | 4, 12 | 8 |
| TK 03 | The Manual MVP | 9, 13 | 10 |
| TK 04 | The Demand Signal | 13, 14 | 8 |
| TK 05 | The Application File | 15 | 8 |
| WP 03 | The Idea Is Not the Asset | 1, 3, 15 | 8 |

## The reports

Eight documents, each taking one framework the **StartPad Brand Presentation,
GrowthLabs Group, 2026** actually states and reading it as something a founder can
operate rather than as a design rule. Every report names the book on the page it
argues from, in a `bookref` block, and `check_pdfs.py` fails the build if a report
does not.

| # | Report | The framework it comes from | Pages |
|---|---|---|---|
| R 01 | Requirement, Gap, Route | Ch. 05 — the voice's sentence structure | 7 |
| R 02 | Truth, Readiness, Proof | Ch. 02 — the solution, three moves | 7 |
| R 03 | The Four Words | Ch. 02 — brand DNA | 6 |
| R 04 | Progress Is a Colour, Not a Number | Ch. 04 and 06 — mission states, product | 7 |
| R 05 | Believed or Shared | Ch. 04 — two intensities | 7 |
| R 06 | One Idea Only | Ch. 02 and 03 — the one rule, hierarchy | 7 |
| R 07 | Composed, Not Translated | Ch. 03 and 05 — the bilingual rule, the voice | 8 |
| R 08 | Warm Candour with Institutional Precision | Ch. 02 — personality | 7 |

The reports are not restatements of the book. Each takes the framework as written,
then argues what it means for somebody running a company — the failure modes of
inverting Truth/Readiness/Proof, the earned-versus-claimed test behind "lime appears
only on what has been earned", what it costs to send an energy-mode document to a
reader who has to believe it. Where the report adds something the book does not say,
it says so on the page.

Three figure types were added for them, all drawn by the book's own rules: `pillars`
(four equal columns, because the book sets the DNA words as equals and a ranked list
would say something the source does not), `states` (dormant held back, in motion
cropped by a real clip path so the crop shows the movement, resolved solid and
centred) and `progression` (the line enters, travels, turns under its own label, and
resolves at the mark).

Every file is a cover, the content, and a closing **About StartPad** page carrying the
mark and `startpad.me`. The toolkits carry ruled worksheets sized to be written on.

```bash
python3 scripts/build_whitepapers.py        # all eight, or pass slugs: tk01 wp02
python3 scripts/check_pdfs.py               # verification gate
python3 scripts/preview_whitepapers.py tk01 # page images, to look at the layout
```

Source of truth is `whitepapers/library/*.py` — one module per document, holding
metadata and a list of content blocks. `whitepapers/common.py` owns the stylesheet
and the block renderer, so restyling all eight is one edit.

## The figures

Fifty-seven infographics, generated as SVG by `whitepapers/figures.py` from data held
in the document that uses it — so a figure cannot drift away from the sentence beside
it. Nothing is a bitmap; everything stays sharp at any zoom and prints at full
resolution.

Colour is assigned by job and the palettes were checked with a validator rather than
chosen by eye. Results are recorded in `brand.CHART_PALETTE_CHECKS`:

- **Categorical** — `#3418E0 · #0087E8 · #00996B`. Sampled from the brand's own
  ultraviolet-to-lime arc, then re-stepped down in lightness until all three cleared
  3:1 on white unaided. Passes all six checks, worst all-pairs CVD ΔE 14.7.
- **Ordinal** — generated at even lightness along hue 272.6. Passes the ramp checks at
  every length the library uses. The ceiling is six steps, enforced by the checker:
  at seven, the adjacent lightness gap falls under 0.06.
- **Lime is never a data mark.** At 1.29:1 on white it cannot carry type or a value,
  which is the brand's own rule and the contrast rule agreeing.

There is no hover layer in a printed page, so every value a reader needs is on the
page as type: direct labels throughout, values outside the bar end where they could
otherwise be clipped, and text wrapped to each mark's own width rather than to an
average.

## Brand decisions worth recording

- **Calm mode.** These are documents that have to be believed rather than shared, so
  the chain pattern is not used anywhere — the guidelines exclude it from anything in
  that category.
- **The mark never sits on lime.** The horizontal lockup's symbol *is* lime, so a
  lime ground would erase the counters the mark is built from. The closing page puts
  the mark on white above the lime band.
- **The cover ribbon is white, not the spectrum.** On ultraviolet the sweep's own dark
  end disappears into the ground.
- **Typeface.** The brand specifies Satoshi, which is Fontshare-distributed and
  unreachable from this build. The PDFs embed Plus Jakarta Sans — the closest freely
  embeddable geometric grotesque, matched on the high x-height and closed apertures
  the guidelines name. Satoshi is first in every font stack, so dropping the real file
  into `brand/fonts/` and rebuilding picks it up. See `brand/fonts/README.md`.

## Verification

`scripts/check_pdfs.py` is the gate and exits non-zero on any failure. It checks page
counts, that `startpad.me` and the About page reached every file, that the document
metadata reads as StartPad rather than as the browser that rendered it, that no
forbidden phrase from the voice rules appears in the copy, that every report cites the
book it derives from, and that no figure exceeds the ordinal ramp's step ceiling.

    17 documents, 129 pages, 0 with problems

## Programme reviews

`REVIEWS` holds feedback on a partner programme. These build and get checked by the
same pipeline as everything else, but they are addressed to a named partner rather
than published, so `PUBLIC` excludes them from the resources bundle.

| # | Review | Source document | Pages |
|---|---|---|---|
| RV 01 | The Camp, Matched to the Missions | Entrepreneurship Camp Learner Journey, GrowthLabs × Cognify Academy, Sept 2026 | 2 |

A match rather than an argument: each of the camp's twenty deliverables against the
mission that receives it and the questions that mission actually asks. **Seven match
directly, four match with a divergence, five have no mission at all** (the financial
plan, the brand kit, the deck, the pitch and the Q&A card — between them 50% of the
Bazaar rubric), and four are camp-only by design. Two new missions — Costs and
Pricing after 08, Brand and Pitch after 10 — close all five from artefacts students
already make in class. Every row is checked against the pack's per-day deliverable
list and against `startpad/missions.py`, so the counts in the opening paragraph are
countable from the table below them.

It ships as **PDF and Word**, both rendered from the same `DOC` dictionary by
`build_whitepapers.py` and `build_review_docx.py`, so the words cannot drift between
the two formats.

It uses a **brief layout**: a masthead instead of a full-bleed cover, a footer band
instead of the About StartPad page, and denser type throughout — a partner note is
read once at a desk, and the generosity that makes a sixteen-page toolkit pleasant
costs a one-page note the page it has to fit on. `max_pages` in the document makes the
length a build gate: `check_pdfs.py` fails if a brief grows past the page count it was
written to, so anything added has to displace something.

Writing it narrowed one voice rule: `unlock` was on the forbidden list as marketing
jargon, but it is also the platform's real mechanic — missions unlock in order, which
is the pack's own wording. The rule now matches the jargon collocations (`unlock your`,
`unlock growth`) rather than the bare verb, so a document is not forced into a worse
word for a real product behaviour.

It also fixed a print bug the long documents had been hiding: tables carried
`break-inside: avoid`, so a table too tall for the space left jumped whole to the next
page and left half a page empty behind it. Tables now break between rows, rows still
never break, and `thead` repeats on the continuation page.

## What still needs a human

The labour-market and funnel figures in **The Readiness Gap** come from StartPad's own
market analysis rather than from a single published dataset, and the paper says so on
the page. Trace them to the underlying statistics before quoting them externally.

---

# StartPad financial model

`output/StartPad_Financial_Model.xlsx` - 26 sheets, 60 months from October 2026
to September 2031, in US dollars. Built by `scripts/build_financial_model.py`
from `finmodel/plan.py`.

Sheet order and column layout follow the reference workbook the founder
supplied: year total first, then that year's twelve months (B = Year 1,
C to N; O = Year 2, P to AA; and so on to BN), with `Input>>`, `Process>>`,
`Output>>` and `Analysis>>` dividers.

## The rule: an input is a decision, everything else is produced

An input is a decision or a rate. How many campus workshops the team runs,
who is on the payroll and what they are paid, what a cohort is priced at, how
long a ministry takes to sign, what share of proposals are won.

Everything else is an output and is typed nowhere:

```
activity -> leads -> meetings -> proposals -> contracts won
         -> mobilisation -> the contract book -> cohorts, seats, programmes
         -> revenue -> cost -> profit -> tax
```

A cohort exists in month 40 because somebody ran a workshop in month 32. Cut
the activity and the cohort disappears. **The year one spend is produced the
same way**: it is what the activity plan, the hiring plan and the cost drivers
add up to on the Expenses sheet, not a ceiling anybody typed. It lands at
**$148,425**, and the dynamic test moves it by changing the activity, which is
the proof that it is an output rather than a target.

27,021 formulas. A build gate refuses to write the file if an em dash, en
dash, middot, curly quote or ellipsis appears in any cell.

## The order the sheet runs in

Assumption Setting is laid out in the order the model uses it: basis, what is
already true, **acquisition** (online funnel, offline activity, who buys and
how long each takes, who runs the activity), **revenue** (what a won contract
turns into, pricing), **expenses** (direct cost, revenue sharing, operating
cost), working capital and funding, **tax**, assets.

## What is already true is the starting point

Five signed university memoranda (MSA, Coventry Egypt, CIC, ESLSCA, Zewail), a
competition running now with 100 participants and EGP 100,000 of prizes
already committed, 300 registered users and 2 paying ones.

The five memoranda are not a special case in the arithmetic. They enter as
contracts already signed, mobilising across the first three months, and run
through the same contract book as anything the funnel wins later. That is why
year one volume is produced rather than asserted. The live competition earns
nothing, because StartPad is paying for it.

## The team, and what it is allowed to cost

Capped at **6, 9, 12, 16 and 20**, and salaries are capped with it: the chief
executive reaches $2,000 a month in year five and not before. Year one is six
people, the team the founder named:

| Year one | Monthly gross |
|---|---|
| Chief Executive Officer | $900 |
| Chief Technology Officer | $900 |
| Chief Commercial Officer | $800 |
| Business development manager | $600 |
| Sponsorship and partnerships manager | $600 |
| Marketing manager | $600 |

Delivery is carried by certified freelancers and partner organisations, so
cohort growth cannot become payroll growth. The pool itself is an output: the
model works out how many facilitators must be certified to deliver what the
funnel sold, and charges for certifying them.

## From a won contract to a cohort

Each engine takes a share of one buyer type's contracts and delivers a fixed
number of units evenly across a contract life. A contract signed in month m
is deliverable from month m plus mobilisation and keeps delivering for its
life. Volume is the live contract book times units over life, and nothing
else.

A contract is signed with a buyer, not with an engine, so a buyer's contracts
are spread across whichever of that buyer's engines are open. Every engine is
currently open from month one, which is the founder's own setting; the gate
column on the engine table is where that is changed.

Contract life is twelve months, so a contract delivers its units inside a year
and must then be re-won. Year one additionally runs at a **delivery pace of
38%** of the full contract rate, because an institution is still localising
the curriculum and training its faculty. That pace is also where the year one
spending ceiling is held: it is a decision about how fast to go, not a budget
line.

## How long each kind of deal takes

Every channel starts in month one. Volume does not, because complexity shows
up twice: once as the sales cycle before signature, once as mobilisation
after it.

| Buyer type | Cycle | Signs | Mobilisation | First delivery |
|---|---|---|---|---|
| Accelerators and programme operators | 1 | m2 | 1 | Dec 2026 |
| Sponsors, banks, telcos | 1 | m2 | 1 | Dec 2026 |
| Institutions, universities, schools | 1 | m2 | 2 | Jan 2027 |
| CSR and corporate innovation | 1 | m2 | 2 | Jan 2027 |
| Government and national initiatives | 1 | m2 | 3 | Feb 2027 |
| NGOs, donors, development agencies | 1 | m2 | 3 | Feb 2027 |

Those one-month cycles are the founder's setting, carried over from V5. They
are the single assumption most worth revisiting: a ministry signing a national
initiative thirty days after first contact is fast.

The direct engine needs neither, which is why subscriptions carry revenue from
month one while the institutional engines are still in their cycle.

## Capacity is checked, not assumed

Each activity names the function that owns it and how many one person can run
in a month, drawing on four sources: the owning function, the founders, the
stipended ambassadors, and the certified partner organisations. Two gates must
read nil in every month, and do: activity beyond what the team can run, and
meetings beyond what it can hold.

| | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| Activity utilisation | 58% | 51% | 47% | 40% | 37% |
| Meeting utilisation | 23% | 28% | 34% | 33% | 31% |

## What it produces

| | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| Revenue | $103,587 | $598,106 | $1,085,654 | $1,759,672 | $2,483,099 |
| Total expense | $148,425 | $471,814 | $871,339 | $1,342,251 | $1,840,464 |
| Net profit | ($44,838) | $107,964 | $166,094 | $323,501 | $498,042 |
| Cash at year end | $127,330 | $185,024 | $310,257 | $609,759 | $1,079,788 |

Profitable from year two. Revenue is B2B: subscriptions at $15 a year for Pro
and $35 for Team are a reach product, and most paying accounts come free, from
learners who sat in a cohort rather than from a paid click.

Year one spends **$148,425**, which nobody typed. It is what the activity
plan, the hiring plan and the cost drivers add up to, and the dynamic test
moves it by changing the activity.

## The market size is the deck's, and is not StartPad's price list

TAM is what the buyers in this market spend on this capability in a year. It
does not shrink because StartPad decides to charge less. When the price
constants were repointed at the financial model, the market sized itself on
StartPad's own fees and halved, which is wrong on its own terms and also broke
the figure already in front of investors.

Sizing now has its own reference prices, frozen in `MARKET_REFERENCE`, and the
obtainable share is the plan's own year five revenue read from the model:

| | Plan | October 2026 deck |
|---|---|---|
| TAM | $273.4m | $273.4m |
| SAM | $89.9m | $89.9m |
| SOM, year five revenue | $2.48m | $2.48m |
| Institutional share of SAM | 81% | 81% |
| Young people reached | 17.1m | 17.1m |
| Buyers who pay | 12,079 | 12,079 |

## The plan and the model are one set of numbers

`business_plan/finlink.py` reads the recalculated workbook and hands every
figure to the business plan. The plan holds no financial numbers of its own:
volumes, prices, the cost stack, the three statements, the capacity tables,
the establishment and all five financial figures are read from the model. A
number can be wrong, but the two files cannot disagree.

The document carries a full **Financial Plan** part, from assumptions to the
three statements: method, what the model opens on, acquisition assumptions
online and offline, who buys and how long each kind takes, what a won contract
turns into, pricing, delivery pace and the year one ceiling, direct and
operating cost, working capital, funding and tax, then the income statement,
balance sheet and cash flow statement in full, the indicators, the capacity
checks, how the model is verified, and what still needs a decision.

It also carries a **Direct Engine** part for the B2C side: why a $15 a year
price settles the strategy on its own, the three stage funnel, the two routes
to a paying account and why a cohort learner converts about three times better
than a click, the online channels, the offline activity, the ambassador
network, the subscriber economics, and the three levers that would make the
engine bigger. In year five 83% of registered accounts arrive through an
institution, which is why the direct engine is a consequence of the B2B
business rather than a channel beside it.

Everything is five years. Every table, every chart and every target runs Year 1
to Year 5, including the engine mix donuts, the revenue share by engine, the
leverage bands and the podcast targets, all of which previously stopped at
year three while the model ran to five.

**All fifteen roles** on the establishment are described, each with the
purpose it exists for, the responsibilities that belong to it and nobody else,
**who it works with inside and outside the company**, and the one measure it
is held to.

## Rebuild

Order matters. The plan cannot be built before the model.

```bash
python3 scripts/build_financial_model.py
python3 scripts/recalc.py output/StartPad_Financial_Model.xlsx 1500
python3 scripts/build_business_plan_docx.py      # redraws all 45 figures
```

LibreOffice Calc must be installed for the recalculation; this container did
not ship with it. openpyxl writes formulas without cached values, so nothing
that reads values will show numbers until the workbook is recalculated.

## Every figure is the same width, on purpose

Each figure is placed in the document at the same printed width, so a point
size chosen in `charts.py` is only the point size the reader sees if every
saved figure has the same pixel width. They did not. `savefig.bbox="tight"`
cropped each one to its own content, which produced **25 different widths
across 45 figures and a 1.9x spread in apparent type size**: the leverage
diagram printed at 73% of the size it was drawn at and the market circles at
141%. That is the real reason some charts looked crowded and others oversized.

The canvas is now fixed at 7.1 inches for every figure, the constrained layout
engine fits plot content inside it, and hand-composed diagrams already fill
their own canvas. All 45 save at exactly 1420px.

A fixed canvas clips anything drawn outside it, where a tight box silently
rescued it, so `scripts/check_figure_fit.py` measures every figure against its
canvas and names the overflowing edge. It found six real clips, among them an
unwrapped footnote running two and a half inches off the leverage diagram. The
document builder refuses to run if the saved widths ever diverge again.

## Four gates, not one

A model can contain nothing but formulas and still be dead, if those formulas
point at the wrong cells. A document can quote a model and still contradict
it, if it quotes a copy.

```bash
python3 scripts/audit_financial_model.py        # 0 static, 0 hardcoded
python3 scripts/verify_financial_model.py       # 840 of 840 recompute
python3 scripts/test_model_is_dynamic.py        # 36 of 36 outputs respond
python3 scripts/check_plan_matches_model.py     # 95 of 95, plan = model = deck
python3 scripts/check_figure_fit.py             # no figure overflows its canvas
```

**The audit** reports any number outside a designated input cell, and any
number inside a formula that is not structural. Zero of each across 27,021
formulas.

**The verifier** rebuilds the entire acquisition engine a second time, in
Python, from the input cells read back out of the workbook, and compares every
month: leads, meetings, proposals, contracts signed after each buyer's cycle,
contracts mobilised after each lag, the live contract book by engine, and the
volume each engine delivers. Then every revenue line against volume times
price, direct cost against its drivers, payroll against the establishment,
every profit cross-foot, the balance sheet and cash flow identities, that no
asset depreciates below nil, and the capacity sheet. It has already caught two
real defects: a total gross assets row summing one row short, and four engines
booking year one revenue against nil delivery cost.

**The dynamic test** moves fourteen inputs at once, recalculates, and confirms
thirty-six outputs across every calculating sheet respond with the balance
check still at 0.000000.

**The plan check** proves the business plan's headline series equal the
workbook's, that both agree with the October 2026 investor deck, that every
role on the establishment has a description and no description describes a
role nobody holds, that the plan's cost roll-up adds back to the model total so a
cost line added later cannot go missing from the document, that headcount sits
inside its cap, that the balance check is nil, and that no figure on disk
predates the workbook. That last one is not a precaution: the document
renderer embeds whatever PNG is on disk, so a plan built after a model change
used to carry the previous run's charts beside the new sentences, and both
halves looked correct on their own.

## What still needs a decision

The **sales cycles** are set to one month for every buyer type. That is fast
for a ministry or a donor, and it is the assumption most likely to be
challenged in a funding conversation. Lengthening it pushes revenue right
without changing anything else.

The **cash trough** is $13,012 in month 3, against the $25,000 minimum buffer
the model itself carries. The seed lands in month 4. A larger round, or
pulling institutional days sales outstanding in from 75, closes it. Both are
inputs.

The valuation inputs on `Exit Angel and VC`, pre-money at each round, the
dilution assumed from later rounds, and the exit multiples, are negotiating
positions rather than facts. They are inputs for that reason.


## Egypt CSR, NGO and youth organisation prospect registry

116 organisations in Egypt that could fund, host or carry the One Million
Entrepreneurs initiative: corporates with CSR, corporate and family
foundations, bilateral donors and development agencies, UN agencies, NGOs,
youth organisations, national initiatives and business chambers. For each
one: what they actually fund, why they fit, what they are looking for in
return, what to ask them for, who decides, how to reach them and when.

```bash
python3 scripts/build_prospects_xlsx.py output/StartPad_Egypt_CSR_NGO_Prospects.xlsx
```

The data is in `outreach/prospects.py`; the builder only lays it out. Every
row carries a confidence rating, and no individual's name, email address or
phone number appears anywhere in the file by design.

## One Million First-Time Founders: the initiative

The sponsorship framework and the invitation list for the named initiative,
built on top of the prospect registry above. The registry asks who in Egypt
could fund entrepreneurship work at all; these two ask who we invite to
sponsor one initiative, in which of three roles, for what contribution, and
what they get back.

Three files: the invitation list, the budget, and the framework.

```bash
python3 scripts/build_initiative_xlsx.py        output/StartPad_Initiative_Sponsor_List.xlsx
python3 scripts/build_initiative_budget_xlsx.py output/StartPad_Initiative_Budget.xlsx
python3 scripts/build_initiative_docx.py        output/StartPad_Initiative_Framework.docx
```

`outreach/initiative.py` holds the roles, the three tiers, the in-kind menu,
the value each kind of partner gets, the viral mechanics, the events and
webinars, the six-month plan, the six-line budget and what StartPad gets
back. `outreach/framework.py` is the document's prose. All three builders
read the same module, so no two files can disagree about a number.

The wave is online, free to every participant, and funded entirely by the
coalition: $200,000 for one million registered entrepreneurs, which is
$0.20 a head. There are no paid in-person cohorts. Offline info sessions
happen where a partner asks for one and hosts it. StartPad contributes the
platform, the curriculum and its team's time, puts in no cash, and takes no
margin; the return prices in `startpad_return()` come from
`finmodel/plan.py` rather than from the documents.
