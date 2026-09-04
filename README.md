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
