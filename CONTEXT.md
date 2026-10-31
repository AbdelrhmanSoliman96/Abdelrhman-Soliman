# CONTEXT — StartPad & LEAP

**Hand-off file. Paste or attach this at the start of a new chat and work can continue without re-establishing anything.**

Last updated: 31 Oct 2026 · Repo `AbdelrhmanSoliman96/Abdelrhman-Soliman` · Branch `claude/startpad-ux-genz-review-wzg9vx`

---

## How to use this file

Everything below is settled fact unless marked **OPEN**. Don't re-derive it, don't re-ask about it, and don't re-review screens already reviewed — check the round index first.

New work continues the numbering: the next round is **R20**.

---

## Two separate workstreams

| | **StartPad** | **LEAP Consulting** |
|---|---|---|
| What | Gamified platform guiding MENA founders through 15 missions, idea → launched startup | Cairo consultancy, strategy + finance + data science |
| Built on | Lovable (React/TypeScript) | — |
| Deliverable | Lovable prompts (R1–R19) | Pricing methodology documents |
| Language | English | Arabic |

They share a repo and nothing else.

---
---

# PART 1 — StartPad

## The product

**Tagline:** *Structure Today, Scale Tomorrow.* · **Domain:** startpad.me · **Operator:** GrowthLabs
**Audience:** first-time founders in Egypt, Saudi, UAE and the wider Arab world — students, employed people, side-project builders.
**Scale as published:** 124+ founders · 114 toolkit calculators · 2 mentors.

### The 15 missions — NAMES AND PHASES ARE FIXED

The user instructed explicitly: **do not rename missions or phases, do not reorder, do not merge, do not add.** Only the questions inside them change.

| Phase | # | Mission | XP |
|---|---|---|---|
| **Discover** | 1 | Problem Analysis | 100 |
| | 2 | Problem Definition | 100 |
| | 3 | Opportunity Prioritisation | 150 |
| **Shape** | 4 | Testable Problem Statement | 150 |
| | 5 | Solution Selection | 200 |
| | 6 | Value Proposition & Assumptions | 200 |
| **Test** | 7 | First Assumption Test | 250 |
| **Model** | 8 | Business Model Canvas | 300 |
| | 9 | Build a Learning Prototype | 300 |
| | 10 | Prototype User Test | 300 |
| **Readiness** | 11 | Go-to-Market Experiment | 300 |
| | 12 | Demand & Market Validation | 350 |
| | 13 | MVP Scope & Build | 400 |
| | 14 | Early Traction Review | 450 |
| | 15 | Launch & Incubator Readiness | 500 |

**4,050 XP total.** Five contiguous phases: 3 · 3 · 1 · 3 · 5.

> An older 8-phase structure (Discovery / Analysis / Ideation / Validation / Business Model / Development / Strategy / Launch) appears in some marketing copy. **It is obsolete.** Corrected in `brand/linkedin/overview-copy.md`; may still be live on LinkedIn and other pages.

### AI assessment

Five criteria — **specificity, depth, evidence, actionability, relevance** — pass mark **70%**. Unlimited resubmission.

**Measured fact worth keeping:** submitted gibberish (`fdsfdsdsdfdfsdsadsds dad dad dada…`) scored **20/100**. So the usable scale runs 20–100, not 0–100, and the gap from nonsense to pass is 50 points instead of 70. R16 exists to fix this.

### Pricing as published

| Plan | Price | Covers |
|---|---|---|
| Free Explorer | EGP 0 / free forever | Missions 1–3, community, dashboard |
| Founder Sprint | **$15 USD** one-time (shown as EGP 740) · 12 weeks · no renewal | All 15 missions, AI tools, toolbox, PDF exports, resource library |
| **Team** | **does not exist yet** | R19 specifies it |

Payment is taken **in EGP for Egypt, USD everywhere else**. Mentor sessions are paid per session and never gated — that line is published and should stay.

### Brand system (R13)

| Token | Hex | Use |
|---|---|---|
| Lime | `#CBF24A` | **Fill only**, carrying near-black text |
| Ink | `#0B0D10` | Text, dark surfaces |
| Indigo | `#3418E0` | The accessible action colour |
| Paper | `#F4F4F2` | Page background |
| Surface | `#EDEDEA` | Cards |
| Cyan | `#00D4F0` | Accent |
| Greys | `#8A8F98` `#A5A9AF` `#5B6068` `#3D424A` | |

**Contrast measurements that govern usage:**
- lime on white = **1.29:1** → fails everything. Never lime text on white.
- lime on ink = **15.1:1** ✓
- indigo on white = **8.9:1** ✓

**Type:** Satoshi (Latin) + Zain (Arabic), resolved by `unicode-range`. Weights **300/400/700/900 only** — Zain has no 500. Satoshi contains **0% Arabic coverage** (verified by parsing the binaries); the two-font stack is required.

Logo files in `brand/logo/`. Social covers in `brand/linkedin/` and `brand/facebook/`.

---

## Round index

Each round is `startpad-lovable-prompts-rN.md` + `.html` in the repo root.

| R | Subject | Contents |
|---|---|---|
| 1 | First UX review | `startpad-lovable-prompts.md`, `startpad-ux-review.html` |
| 2 | 5 logged-in screens | 41 findings, 6 bugs, 15 prompts in 7 page-scoped sets |
| 3 | 17 screens | Privacy, FAQ, profile fields (age + status), **public vs authenticated route split**. Contains the canonical route table |
| 4 | About split + Knowledge Base | AI content pipeline with editorial gate, first-party data layer, SEO |
| 5 | Dashboard rebuild | 12-column / 6-band grid |
| 6 | Contact page | Email + form only, no location or phone |
| 7 | AI output quality | Context layer, output contracts, banned-phrase list, eval harness |
| 8 | Authenticated verification | Six-phase pass |
| 9 | Closing 6 failures | Root-caused to one pattern: canonical implementation exists while a duplicate ships. Lint/hook/build guards |
| 10 | Referral rebuild | "Bring a founder" |
| 11 | Submission gate + branded PDFs | Gibberish detector, logo on every export |
| 12 | Free → paid sweep | Pricing nav, grandfathering, billing page, legal updates |
| 13 | Rebrand | Colours, type system, font pipeline |
| 14 | Missions redesign | 87 questions / 75 blank textareas diagnosed. **Rebuilt against the live roadmap** |
| 15 | Resubmit loop | Two duplicate submit buttons, stale scores, `scoredHash` |
| 16 | Pass-mark calibration | Gates before scoring, phase-weighted criteria, anchor ladders, calibration set |
| 17 | **The question bank** | All **136 questions** across 15 missions, 15 input types, finance thread |
| 18 | Community page | Post card rebuild, two rendering bugs, mission scoping |
| 19 | Pricing page | Currency control collision, Team plan, card layout |

### Published artifacts (links the user has)

| | |
|---|---|
| R14 | https://claude.ai/code/artifact/9f23d4b0-2be9-414a-bc42-6245f0ce82e5 |
| R15 | https://claude.ai/artifact/Mo4JHtVuFMiE7W8VmLpTmV |
| R16 | https://claude.ai/artifact/9s7xTCh4DmAbvxSCzzKtoG |
| R17 | https://claude.ai/artifact/CeSoQKo1GD9KLEGPkWCwQ8 |
| R18 | https://claude.ai/artifact/KTPE8PrcxuAiqNghoJe6A1 |
| R19 | https://claude.ai/artifact/4enEksR5JSbVvFTiVW1wUR |
| LEAP | https://claude.ai/artifact/CmE9UT2fWD1ZMViEEeqBBh |

R2–R13 were published too; those URLs aren't recorded here. The `.md` and `.html` files are all in the repo.

---

## Decisions and principles that carry forward

**"Structure the scaffolding. Never the content."** (R17) A list of industries doesn't tell a founder what their business is — it removes the burden of inventing a taxonomy. Never pre-fill an answer, never suggest a conclusion.

**Multi-select is the default for categories.** Fintech *and* healthtech is a real answer. Subscription *and* commission is a real answer. Every list ends in an open **"Other →"**.

**Every question can carry an attachment**, whatever its input type.

**Never grade the business.** The rubric measures whether the founder did the thinking, not whether the idea is good. A brilliant answer about a doomed business scores well.

**"Not sure yet", "It's a hunch", "No revenue yet", "Inconclusive"** must all be selectable without penalty. Punishing honesty teaches founders to invent numbers.

**One primary button per screen.** Broken on the mission page (three "Resubmit for Review"), flagged repeatedly.

**No leaderboards, streaks-as-pressure, or "top contributor".** The XP system covers motivation; a second one rewards volume over substance. This audience reads gamified noise faster than most.

**Prompt format** the user asked for and every round follows:
```
PAGE: <route>
THE PROBLEM   — what's wrong, with observed evidence
THE FIX       — numbered, with real copy strings and config objects
```
Closing with a sequence table explaining the order.

**Deliverable pattern per round:** write `.md` → generate `.html` → publish artifact → `SendUserFile` the `.md` → summarise in chat. Commit and push each round.

---

## OPEN — decisions waiting on the user

| From | Decision |
|---|---|
| **R15** | When a founder passes (≥70), does the mission stay open for improvement? *Recommended: yes but quietly — primary becomes "Continue to Mission 2", "Improve my answers" stays a text link.* |
| **R16** | Mission 1 threshold — hold at 70, or drop to 60? *Recommended: hold at 70, let the phase weights do the work, lower it with evidence if the pass rate sits below 60% after ~100 founders.* |
| **R16** | What happens at 3 failed attempts? *Recommended: keep unlimited but route to the AI Mentor instead of a fourth blind attempt.* |
| **R17** | Mission 5's matrix is labelled *value/impact*. Those measure nearly the same thing, so ideas land on a diagonal. *Value × Effort* discriminates properly. **Left unchanged per the no-renaming instruction** — it's a one-line axis change whenever they want it. |
| **R19** | **Team or Cohort first?** Team = 2–5 co-founders sharing ONE journey, self-serve. Cohort = university/incubator with MANY journeys, admin dashboard, invoicing. Different products. |
| **R19** | Seat prices ($12 at 3+, $10.50 at 10+, off a $15 individual) are a recommendation in a config object, not validated against actual support cost. |
| **R18** | Do community posts have an author at all? If they're seeded editorial, decide: publish under a real team member, or mark as "StartPad Editorial" with a distinct card. |
| **R18** | Is the mid-paragraph coloured text a broken renderer, or an AI keyword-highlighting feature misfiring? |

---

## OPEN — never done

- **R2 Set 5·A — app nav diet.** Nav still carries 9 items with Sign out at top level.
- **R2 Set 7·A — Arabic audit.** Never run.
- **R2 Set 7·B — mobile audit.** **No mobile screen has ever been reviewed.** Every round has worked from desktop screenshots.
- Arabic variants of the LinkedIn covers (offered, not requested).
- Profile picture 1000×1000, lime mark on near-black, circular safe area (offered, not requested).

---

## Corrections made — don't reintroduce

- **Satoshi has no Arabic.** An earlier claim that Zain could cover both and the second font could be dropped was wrong; parsing the binaries disproved it. R13 was corrected in place.
- **Mission 10 was already renamed** by the user to "Prototype User Test". An earlier prompt asked for the rename — retired.
- **Phases are already contiguous.** An earlier open question about re-cutting them is resolved by the live roadmap.
- **The 8-phase marketing description is obsolete.** It's 5.

---
---

# PART 2 — LEAP Consulting

Separate client, Arabic deliverables.

**Who:** Cairo consultancy at the intersection of strategy, finance and data science. Serves founders, angels, VCs and family offices across Egypt, MENA and global markets. Two service lines:
1. **Real estate development** — 32 services, existing fee methodology (GCC, SAR)
2. **Investment & fundraising advisory** — 24 services across 7 practice areas

### Delivered

`LEAP-Investment-Advisory-Pricing-Methodology.{md,html,pdf,docx}` — a fee and duration methodology for the 24 investment services, built on the logic of their existing real-estate methodology.

**Core formula:** effort days × day rate × complexity × market × **stage** × timeline × language = professional fees, + direct expenses.

**Day rates (USD):** Partner 1,600 · Engagement Manager 1,000 · Senior Analyst 620 · Analyst 380. Cost/day 625 / 390 / 240 / 150. Margin ~61% per level, target realised margin **50%** (vs 45% in the real-estate line).

**24 services · 278 effort days · 2–7 weeks · $6,500–21,100.**

**Six deliberate departures from the real-estate methodology, each argued:**
1. USD base, not SAR — EGP has lost **70%+** since 2022; a 3-month engagement priced in EGP transfers FX risk to LEAP
2. Market coefficient widens to **0.70–1.30** (vs 0.95–1.05) — avg deal size: Saudi $23.7M, UAE $9.2M, Egypt $3.0M in 2025
3. New **stage** coefficient (0.85 seed → 1.50 fund)
4. Complexity narrowed to 0.80–1.75 so stage isn't double-counted
5. Direct expenses 4% not 5% — desk work, not site visits
6. **Advance 50% not 40%** — pre-revenue clients may not be able to pay if the round doesn't close; editable files withheld until settlement

**Success fees:** tiered in tranches 6% → 2%. Seven rules including never standalone, 50% retainer credit, tied to funds arriving not term sheet, 9-month tail limited to a **named written investor list**, 8% overall cap.

**Regulatory stop-rule:** fundraising is a regulated activity — FRA licensing in Egypt, "arranging" is CMA-licensed in Saudi. Services are framed as advisory, with a mandatory legal review before any engagement approaches the arranging threshold.

### OPEN — LEAP

- Base market: Saudi 1.00 kept for consistency with their real-estate doc. Revisit if >70% of engagements are Egyptian.
- Target margin 50% needs verification against their actual utilisation rate.
- **Should success fees be activated at all?** Recommended: defer a year, use monthly retainers for round management until the regulatory review settles in all three markets.
- Price benchmarks used are predominantly US/European — no published MENA advisory fee survey exists. Their own lost/won proposals are the better data.

---
---

# PART 3 — Working notes

## Repo

```
startpad-lovable-prompts-r{1..19}.{md,html}   the rounds
startpad-screen-review-r2.html                R2 review
startpad-review-r3.html                       R3 review
startpad-ux-review.html                       R1 review
brand/logo/                                   extracted PNGs with alpha
brand/linkedin/                               4 covers @1x/@2x, overview copy AR+EN
brand/facebook/                               3 covers @1x/@2x
LEAP-Investment-Advisory-Pricing-Methodology.{md,html,pdf,docx}
build_leap_docx.js                            Arabic RTL docx generator
build_finstreet_analysis.js                   competitive analysis docx
Finstreet_Competitive_Analysis.docx
tools/md-to-html.py                           md → styled HTML (LTR | --rtl | --print)
tools/html-to-pdf.js                          print HTML → A4 PDF
```

## Commands

```bash
# English round document
python3 tools/md-to-html.py startpad-lovable-prompts-r20.md \
        startpad-lovable-prompts-r20.html "StartPad — <subject>"

# Arabic document
python3 tools/md-to-html.py doc.md doc.html "العنوان" --rtl

# PDF (needs the print HTML + fonts + playwright — see below)
python3 tools/md-to-html.py doc.md /tmp/print.html "t" --print
node tools/html-to-pdf.js /tmp/print.html out.pdf "FOOTER TEXT"

# Word, Arabic RTL
node build_leap_docx.js doc.md out.docx
```

## Environment — this container resets

**`node_modules` and the scratchpad are wiped on reset.** Every one of these had to be redone mid-session at least once:

```bash
# node packages — run node FROM the repo root or require() fails
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install playwright docx

# PDF reading — pypdf is broken (_cffi_backend / cryptography panic). Use poppler:
apt-get update -qq && apt-get install -y -qq poppler-utils
pdftotext -layout in.pdf out.txt     # handles Arabic correctly

# Arabic fonts for PDF rendering (none installed by default):
curl -sS -A "Mozilla/5.0" \
  "https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;500;600;700" -o /tmp/ar.css
# then fetch each .ttf URL into ~/.fonts/NotoSansArabic-{400,500,600,700}.ttf && fc-cache -f

# LibreOffice, for verifying docx renders (installs fine):
apt-get install -y -qq --no-install-recommends libreoffice-writer
soffice --headless --convert-to pdf --outdir /tmp/check file.docx
```

- Chromium: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`
- **Reachable:** Google Fonts, npm, apt
- **Blocked:** GitHub raw, finstreet.ae, angelsta.net, wamda.com, adgm.com, semafor.com, tracxn.com
- A local checkout once reset to an old commit while the remote was ahead — `git fetch` + `git rebase origin/<branch>` recovered it.

## Git

Branch **`claude/startpad-ux-genz-review-wzg9vx`** only. Commit messages end with:

```
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018m7f2Ed2N79SkUG5JbZd3z
```

Never put a model identifier in commits, PRs, code comments or pushed artifacts.

## Verify arithmetic before publishing

Every pricing table, fee calculation and question count in this project has been checked with a script before shipping — and doing so caught real errors (prompt counts, day totals, DXA column sums). Keep doing it. `docx` column widths must sum to the content width exactly (9360 DXA for A4 with 0.9" margins; 9026 for 1").
