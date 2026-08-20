# StartPad — Lovable Prompts (Round 5)

Three prompts. A dashboard layout rebuild, the engagement widgets that replace the usage charts, and the Loadout fixes that feed them.

Paste one prompt per message.

| Set | Page | Prompts |
|---|---|---|
| 1 | Dashboard | A — layout rebuild · B — engagement widgets |
| 2 | Loadout | A — sticky collision + tool data for the dashboard |

---

## What's already fixed on the dashboard

Worth noting before the criticism, because a lot landed since the last round: the **"Where you left off" recap** is surfaced, the **next streak reward** is showing, usage analytics moved from *"on this device"* to **"across your account"**, the KPI panel now carries **real numbers**, **"Invested (USD)"** is gone, mentoring is **one consolidated block with a timezone selector** (Cairo GMT+3), past sessions are **collapsed behind a toggle**, "Completed" correctly reads **0**, the progress bar is **correctly empty at 0 of 15**, and the **legal footer row** is in place.

The remaining problems are layout and content selection, which is exactly what you identified.

---
---

# Set 1 — Dashboard

Two prompts. A rebuilds the grid and fixes three visible layout defects. B replaces the two low-value charts with the engagement content you asked for.

## PROMPT A — Rebuild the Dashboard Layout

```text
PAGE: Dashboard (/dashboard) — layout and visual hierarchy.

THE PROBLEMS — three are visible layout defects, one is structural.

1. A ~500px EMPTY COLUMN. The "Community & groups" card sits in a right-hand
   column spanning from the Current mission row all the way down past the KPI
   section. It contains a heading, a subtitle, one button and the sentence
   "You haven't joined a group yet." — then roughly 500 vertical pixels of
   nothing. It is the emptiest element on the page and it occupies a third of
   the width for four rows.

2. TWO BUTTONS ARE FLOATING IN THE WRONG CARD. "Export PDF" and "Open Loadout"
   render at the bottom of the Community & groups card, but they belong to
   "Your KPI performance". They are visually inside a card they have nothing to
   do with. This is a grid-placement bug, not a styling choice.

3. NO VISUAL HIERARCHY. Every block is a white rounded card with the same
   border, the same radius, the same shadow and the same padding — the primary
   action, the stat tiles, the charts, the workspace list and the mentoring
   block all carry identical visual weight. Nothing leads, so the eye has no
   entry point.

4. THE GRID IS FIGHTING ITSELF. A 2/3 + 1/3 split is applied to rows whose
   content does not want that ratio, producing the empty column in problem 1.
   Then rows 4 onward abandon the split and go full width, so the page changes
   structure halfway down.

THE FIX — rebuild on an explicit 12-column grid with defined row bands.

TARGET LAYOUT (desktop, 12 columns, 24px gutters):

┌──────────────────────────────────────────────────────────────────┐
│ BAND 1 — CONTINUE (full width, tinted, most prominent on page)   │
│ ┌────────────────────────────────────┬───────────────────────┐   │
│ │ cols 1-8                           │ cols 9-12             │   │
│ │ Mission 1 of 15 · Discovery        │  🔥 2-day streak      │   │
│ │ Problem Analysis                   │  1 day to unlock      │   │
│ │ "Where you left off" recap (2-3    │  Mission templates    │   │
│ │  lines, clamped)                   │  [progress pips]      │   │
│ │ [Continue mission →] [Ask mentor]  │                       │   │
│ └────────────────────────────────────┴───────────────────────┘   │
├──────────────────────────────────────────────────────────────────┤
│ BAND 2 — STAT TILES (4 × 3 cols, compact, each a link)           │
│ Journey 1/15 · Points 175 · Streak 2 days · Tools used 3         │
├──────────────────────────────────────────────────────────────────┤
│ BAND 3 — YOUR NUMBERS (full width, 3 × 4 cols)                   │
│ Product Roadmap 2.6% · Cost Structure · Income Statement         │
│ [Export PDF]  [Open Loadout →]   ← inside THIS card, right-aligned│
├──────────────────────────────────────────────────────────────────┤
│ BAND 4 — YOUR TOOLKIT (see Prompt B)                             │
│ ┌──────────────────────────┬───────────────────────────────┐     │
│ │ cols 1-7  Pick up a tool │ cols 8-12  Coverage by category│    │
│ └──────────────────────────┴───────────────────────────────┘     │
├──────────────────────────────────────────────────────────────────┤
│ BAND 5 — WHERE YOU'RE ACTIVE (4 equal cards, 3 cols each)        │
│ Journey · Community · Collaboration · Mentoring                  │
├──────────────────────────────────────────────────────────────────┤
│ BAND 6 — DO THIS NEXT (full width, 3 suggested actions)          │
└──────────────────────────────────────────────────────────────────┘

RULES

1. MERGE "Current mission" and "Where you left off" into ONE card. They are
   currently two stacked cards saying the same thing — mission name, then a
   recap of that mission. One card: mission identity, the recap, the actions.
   Clamp the recap to three lines with "Read more".

2. BAND 1 IS VISUALLY DISTINCT from everything below it. Give it a tinted
   background (a light green wash), slightly more padding, and the only
   full-strength green primary button on the page. This is the entry point;
   it should be obvious within half a second of the page loading.

3. FIX THE FLOATING BUTTONS. "Export PDF" and "Open Loadout" move inside the
   "Your KPI performance" card, right-aligned in its header or footer. They
   must never render inside the Community card.

4. KILL THE EMPTY COLUMN. Community is not a sidebar — it becomes one of four
   equal cards in Band 5. No card on this page may be taller than its content
   needs. Nothing spans multiple rows.

5. THREE LEVELS OF CARD, not one:
     Level 1 — Band 1 only. Tinted background, larger padding, primary CTA.
     Level 2 — Bands 3, 4, 5. White card, 1px border, subtle shadow.
     Level 3 — Band 2 stat tiles. No shadow, lighter border, compact padding.
   Different weights are what create hierarchy; identical cards are why the
   page currently reads flat.

6. EVERY CARD ENDS IN AN ACTION. A card with no next step is a dead end. Each
   Band 5 card carries one link in its footer.

7. NO CARD SHOWS ONLY AN ABSENCE. If a section has no data, it shows the
   single most useful action instead — Community with no groups shows
   "Founders on your mission" with three avatars and "Join the conversation",
   not "You haven't joined a group yet."

8. SECTION HEADINGS. Bands 4, 5 and 6 get a small section label above them
   ("Your toolkit", "Where you're active", "Do this next") so the page reads as
   four zones rather than fourteen floating cards.

9. MOBILE (390px): every band stacks to one column in the order above. Band 2
   becomes a 2×2 grid, not four full-width rows. Band 5 becomes a horizontal
   scroll strip of four cards. Band 1 stays first and stays tinted.

10. PURGE the workspace called "master" — it is test data and has survived
    three rounds of review. Add the seed-data build guard from Round 3
    Set 4·B.

11. The dashboard should fit in roughly two viewport heights on desktop. It is
    currently around four, most of it empty.
```

## PROMPT B — Replace the Usage Charts with Real Engagement

```text
PAGE: Dashboard (/dashboard) — Bands 4, 5 and 6 from Prompt A.

THE PROBLEM
The two charts currently on the dashboard — "Usage trend: tools opened per day
across your account" and "Most used tools" — measure the wrong thing. "How many
times did I open a tab" is not a question a founder has. They take up a full
row and answer nothing actionable.

Meanwhile the Loadout holds 114 tools across 9 categories, the founder has real
numbers in three of them, and none of that is usable from the dashboard.

Replace both charts with the following.

=================================================================
BAND 4 — YOUR TOOLKIT
=================================================================

LEFT (cols 1-7) — "Pick up where you left off"
  A list of the tools the founder has actual data in, each row showing the
  headline OUTPUT, not a usage count:

    Income Statement (P&L)     Gross profit    $321,374    [Open →]
    Cost Structure & Budget    Monthly burn    $360,443    [Open →]
    Product Roadmap Progress   Completion      2.6%        [Open →]

  Each row: tool name, the metric label, the current value in tabular figures,
  last-edited relative time, and a link. Sort by most recently edited.
  This is the single most useful block you can put on this page — it turns the
  dashboard into a way back into work rather than a report about work.

  Below the list: "Recommended for Mission 1 · Discovery" — 2-3 tools from the
  Loadout tagged to the founder's current mission, with the one-line "Why it
  matters" copy the Loadout cards already carry.

RIGHT (cols 8-12) — "Toolkit coverage"
  A horizontal bar chart, one row per Loadout category, showing tools used out
  of tools available:

    Financial Statements      ███░░░░░░░  3 / 10
    Metrics & Unit Economics  ░░░░░░░░░░  0 / 23
    Go-To-Market              ░░░░░░░░░░  0 / 15
    Strategy & Frameworks     ░░░░░░░░░░  0 / 16
    Market & Customer Res.    ░░░░░░░░░░  0 / 16
    Product & Roadmap         █░░░░░░░░░  1 / 9
    Team & Operations         ░░░░░░░░░░  0 / 12
    Cap Table & Deal Terms    ░░░░░░░░░░  0 / 6
    Fundraising & Investor    ░░░░░░░░░░  0 / 7

  This answers a real question — "what haven't I looked at yet" — and it makes
  the breadth of the Loadout visible, which the current charts do not. Clicking
  a row opens that Loadout category.
  Sort by completion descending so progress sits at the top.
  Add a "Favourites (0)" row at the bottom linking to the Loadout favourites
  view, with a prompt to star tools — the feature exists and is unused.

=================================================================
BAND 5 — WHERE YOU'RE ACTIVE  (4 equal cards, 3 columns each)
=================================================================

Each card: icon + title, two or three live figures, one visual element, one
action link. Equal height. No card shows only an empty state.

CARD 1 — JOURNEY
  Mission 1 of 15 · Discovery
  A compact 8-segment phase bar showing the phases, current one highlighted
  Next up: Problem Definition
  → "Open journey"

CARD 2 — COMMUNITY
  Replaces the current empty "Community & groups" card entirely.
  "8 founders on Mission 1"  — a row of 4 overlapping avatars, +4 more
  Your posts: 1 · Replies: 0
  Latest in your circle: the most recent post title, one line, clamped
  → "Open community"
  Never render "You haven't joined a group yet." as the card's whole content.

CARD 3 — COLLABORATION
  Workspaces: 1 · Members: 1
  The workspace name and its status chip
  If none: "Start a project and find collaborators" + [New project]
  → "Open hub"

CARD 4 — MENTORING
  Next session, or the empty state.
  Times shown in Cairo (GMT+3)  ← keep the timezone selector, it's good
  Past sessions: 3 · Mentors: 2
  → "Book a mentor"

AI TOOLS gets a slim full-width strip beneath Band 5 rather than a fifth card:
  "AI Mentor · last used 19 Aug"   "3 surveys generated"   → "Open AI Tools"

=================================================================
BAND 6 — DO THIS NEXT
=================================================================

Three concrete, generated actions — the closing block of the page, so it never
ends in empty space. Derive each from real state, ordered by impact:

  1. From the mission: "Answer question 1 of Mission 1 — it's the lowest-scoring
     criterion in your last attempt"        [Go →]
  2. From the toolkit: "You've filled in the P&L but not Burn Rate & Runway —
     it takes 5 minutes and uses numbers you already entered"   [Open →]
  3. From the profile: "Add your country, industry and startup stage"  [Add →]
     (this replaces the persistent 63% banner — see note below)

Rules for this band: never more than three, each must be completable in under
ten minutes, and each disappears once done. If fewer than three are available,
show fewer — do not pad.

=================================================================
GENERAL
=================================================================

- All figures use tabular numerals so columns align.
- Charts: reserve height before data loads so nothing shifts on load.
- Every chart legible at 390px — not a shrunk desktop chart.
- Charts readable without colour alone; label values directly on the bars.
- Both themes supported.
- Keep the 7 / 30 / 90 / All-time range filter, and make it actually change
  the toolkit and engagement figures, not just the charts.

NOTE ON THE PROFILE BANNER: with "Do this next" carrying profile completion as
item 3, the persistent 63% banner across every page becomes redundant. Remove
it from the app shell — this closes Round 2 Set 5·A, which is still open.
```

**Why this order.** A establishes the grid; B fills bands 4–6. Doing B first would place good widgets into the broken layout.

---
---

# Set 2 — Loadout

One prompt. A real overlap bug, plus the data the dashboard needs.

## PROMPT A — Fix the Sticky Collision and Expose Tool State

```text
PAGE: Loadout (/loadout).

THE PROBLEM

1. TWO STICKY ELEMENTS COLLIDE. The top navigation and the Category/Framework
   filter bar are both sticky. On scroll the nav renders on top of the filter
   bar, completely covering the search field and partially covering the Category
   and Framework dropdowns. The page becomes unfilterable while scrolled.

2. THE DASHBOARD CANNOT SEE TOOL STATE. There is no exposed record of which
   tools a founder has opened, which they have entered data into, what the
   headline output of each is, or when it was last edited. The dashboard needs
   all four (see Set 1 Prompt B).

3. FAVOURITES ARE UNUSED. Every tool card has a star, the sidebar shows
   "Favorites 0", and nothing anywhere prompts a founder to use it.

THE FIX

1. STICKY STACKING — one sticky context, not two competing ones:
     - Nav is sticky at top: 0, with the highest z-index.
     - The filter bar is sticky at top: [nav height], with a lower z-index.
     - Use a CSS custom property (--nav-height) so the offset cannot drift.
     - Set scroll-margin-top on category anchors to nav height + filter height,
       so jumping to a category does not land under the chrome.
     - Verify at 390px, where the nav may wrap to a taller height.

   Check every other page for the same collision — anywhere a page has its own
   sticky sub-header, this pattern will repeat.

2. PERSIST TOOL STATE per user, per tool:
     tool_id, opened_at, last_edited_at, has_data (bool),
     headline_metric_label, headline_metric_value, completion_pct
   The headline metric is defined per tool in its config — Income Statement →
   gross profit; Cost Structure → total monthly burn; Product Roadmap →
   completion %. Expose it through an endpoint the dashboard reads.

3. TAG EVERY TOOL TO MISSIONS AND PHASES, the same way Round 3 Set 8·A asks for
   resources and articles. Then:
     - The dashboard can show "Recommended for Mission 1".
     - The Loadout can show a "Used in Mission 4" chip on each card.
     - Missions can surface their 2-3 relevant tools inline.
   With 114 tools across 9 categories, mission tagging is what makes the
   library navigable rather than overwhelming.

4. MAKE FAVOURITES DISCOVERABLE: a one-time inline hint on first visit ("Star
   the tools you'll come back to"), and surface the favourites count on the
   dashboard toolkit card.

5. SHOW STATE ON THE CARDS. A tool the founder has data in should say so —
   a subtle "In progress · edited 2 days ago" line and a filled state on the
   card border. With 114 tools, being able to see at a glance which ones you
   have touched matters more than any filter.

6. ADD A "RECENTLY OPENED" ROW at the top of the Loadout, above the category
   list, mirroring the dashboard's "Pick up where you left off".

KEEP: the "Why it matters" line on every card is genuinely excellent — it is
the best microcopy in the product and it is what makes 114 tools approachable
rather than intimidating. The framework attribution chips (MoSCoW, RICE,
Nielsen, TCO) are equally good. Do not lose either.
```

**Why this order.** Point 2 is a dependency for Set 1 Prompt B — the dashboard toolkit band cannot be built until tool state is exposed. Run this first or in parallel.

---

## Suggested sequence

| Order | What | Why |
|---|---|---|
| 1 | Set 2·A | Fixes a real overlap bug and unblocks the dashboard toolkit band |
| 2 | Set 1·A | Rebuild the grid before adding anything to it |
| 3 | Set 1·B | Fill bands 4–6 with the engagement content |

All three are same-week work. Set 2·A points 1 and 2 could ship today.
