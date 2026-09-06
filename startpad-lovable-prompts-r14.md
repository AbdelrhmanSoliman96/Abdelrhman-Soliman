# StartPad — Missions Redesign (Round 14)

A full rework of the 15 missions' question set, plus five prompts to build it.

Worked from `startpad15missions.docx`. The journey PDF wouldn't yield text (image-based), so if it contains flow rules I haven't accounted for, send them and I'll fold them in.

---

## The diagnosis, in one number

**87 questions across 15 missions. 75 of them are blank textareas.**

That is the whole problem. Your users aren't struggling because the questions are wrong — most are the right questions. They're struggling because every question is a blank box, and a blank box asks the founder to invent both the *answer* and the *format of the answer* at the same time.

Mission 8 is the clearest case: the Business Model Canvas is a famous **nine-block visual tool**, and it currently renders as **nine consecutive empty text areas**. The canvas is the entire point of the exercise, and it's been flattened into a form.

Three more structural findings:

**The same question is asked five times.** "Who is your user" appears as M1 Q3, M2 Q1, M2 Q2, M4 Q2 and M11 Q1. "What are your next steps" appears in M9, M10, M13, M14 and M15. Nothing carries forward, so each mission feels like starting over rather than building on the last.

**Two missions have identical titles.** Mission 7 and Mission 10 are both "Solution Hypothesis Test". A founder cannot tell them apart on the roadmap.

**Two missions are matrices rendered as text fields.** M3 (Importance/Frequency) and M5 (Value/Impact) are literally 2×2 matrices. Both are currently six text boxes asking the founder to type numbers between 1 and 10.

---

## The principle

**Structure the scaffolding. Never the content.**

A dropdown for industry doesn't tell a founder what their business is — it removes the burden of inventing a taxonomy from scratch. The thinking stays theirs. What changes is that they spend their effort on *the answer* rather than on *working out what shape the answer should be*.

And your point about mixed cases is exactly right, so it's a rule: **every category question is multi-select with an "Other" free-text escape.** Fintech *and* healthcare is a real answer. Subscription *and* commission is a real answer. A closed single-select would force a lie.

---

## The input vocabulary

Eleven types. Everything below maps to one of these.

| Type | When to use | Example |
|---|---|---|
| `chips-multi` | A known set where combinations are real | Industry, channels, revenue models |
| `chips-single` | A known set where only one is true | Problem frequency, launch readiness |
| `slider` | A 1–10 rating | Importance, impact, PMF score |
| `matrix` | Two scores plotted visually | M3 and M5 |
| `canvas` | A named visual framework | M8 Business Model Canvas |
| `builder` | A sentence with blanks to fill | Problem statement, value proposition |
| `repeater` | A list the founder adds rows to | Competitors, features, next steps |
| `number` | A quantity, with unit and currency | Market size, price, revenue |
| `upload` | File, link, or pasted text | Prototype, survey results, evidence |
| `text` | One short line | A name, a link |
| `textarea` | Genuinely open reflection | "What did you learn?" |

**Every question type can carry an attachment.** A founder answering "what were your test results" should be able to attach the survey export alongside their words, not instead of them.

**Every chip list ends with "Other →"** which opens a text field. No list is ever closed.

---

## The 15 missions, redesigned

Legend: **↩** = carried forward from an earlier mission, pre-filled and editable.

### Mission 1 — Problem Analysis

| # | Question | Now | Becomes |
|---|---|---|---|
| 1 | What area are you interested in? | text | **`chips-multi`** — Fintech · Healthtech · Edtech · E-commerce · Logistics · Agritech · Proptech · Food & beverage · Travel · Media · Gaming · B2B software · Marketplace · Climate · Fashion · Fitness · HR · Legal · Insurance · Manufacturing · Energy · Other |
| 2 | Describe a problem you've observed | textarea | **`builder`** — "I noticed that ___ struggle with ___ when ___" + optional detail + optional photo |
| 3 | Who is affected? | text | **`chips-multi`** — Students · Young professionals · Small business owners · Freelancers · Parents · Farmers · Drivers · Patients · Teachers · Retailers · Other — plus one line of specifics |
| 4 | What solutions exist? | textarea | **`repeater`** — name + link + one line on what it does |
| 5 | What are their limitations? | textarea | **`chips-multi`** — Too expensive · Too slow · Hard to use · Not available here · Poor quality · Needs expertise · No offline · No Arabic · Other — then expand |

### Mission 2 — Problem Definition

| # | Question | Becomes |
|---|---|---|
| 1 | Who is your primary user? | **`builder`** — "[age range] [role] in [city/country] who [context]", each blank a chip set |
| 2 | Key characteristics | **`chips-multi`** — income band, tech comfort, buying power, where they spend time |
| 3 | What problem do they face? | ↩ **from M1 Q2**, editable — "You said this in Mission 1. Sharpen it now." |
| 4 | When/where does it happen? | **`chips-multi`** — At work · At home · Commuting · Shopping · Studying · Online · In person · Other |
| 5 | How often? | **`chips-single`** — Many times a day · Daily · Weekly · Monthly · A few times a year · Once |

### Mission 3 — Importance/Frequency Matrix

**Replace all 7 fields with one interactive matrix.**

Problems from M1 and M2 appear as draggable cards. The founder drags each onto a 2×2 grid, or sets two sliders and watches the card move. `repeater` to add more problems. Then `chips-single` to pick the focus problem from those plotted.

The quadrants are labelled so the output teaches: **Fix first** (high/high) · **Quick wins** (low importance, high frequency) · **Big bets** (high importance, low frequency) · **Ignore for now**.

### Mission 4 — Problem Statements

| # | Question | Becomes |
|---|---|---|
| 1 | Main problem statement | **`builder`** — "[User] needs a way to [job] because [insight]. Today they [workaround], which costs them [impact]." |
| 2 | Who specifically? | ↩ **from M2 Q1** |
| 3 | What is the impact? | **`number` + unit** (money / hours / times per week) + `chips-multi` impact type + short note |
| 4 | How will you measure success? | **`repeater`** — metric · current value · target value |

### Mission 5 — Idea Selection

**Same treatment as Mission 3.** A `repeater` of ideas, two sliders each (Value, Effort), plotted live on a 2×2 with quadrants labelled **Do now** · **Plan it** · **Quick win** · **Drop**. Then pick one, and one line on why.

### Mission 6 — Idea Description

| # | Question | Becomes |
|---|---|---|
| 1 | Value proposition | **`builder`** — "For [user] who [need], [name] is a [category] that [benefit]. Unlike [alternative], we [difference]." |
| 2 | Key features | **`repeater`** — feature + the benefit it delivers (this absorbs the old Q3) |
| 3 | ~~What benefits?~~ | **Removed** — merged into Q2. It was asking the same thing twice. |
| 4 | How is this different? | **`chips-multi`** — Cheaper · Faster · Easier · Local · Arabic-first · Better quality · Trusted · New capability · Other + a line |
| 5 | What assumptions are you making? | **`repeater`** — assumption + `chips-single` risk (High/Medium/Low). Feeds directly into Mission 7. |

### Mission 7 — Solution Hypothesis Test

| # | Question | Becomes |
|---|---|---|
| 1 | Main hypothesis | **`builder`** — "We believe [user] will [action] because [reason]. We'll know we're right if [signal]." Riskiest assumption from M6 offered as the starting point. |
| 2 | How will you test it? | **`chips-single`** — Interviews · Survey · Landing page · Fake door · Concierge · Wizard of Oz — each with a one-line explanation of what it is |
| 3 | What would prove it? | **`number`** threshold — "at least ___ out of ___ do ___" |
| 4 | Test results | **`upload`** (survey export, notes, screenshots) + **`number`** actual result |
| 5 | What did you learn? | **`textarea`** — keep open. This one should be. |

### Mission 8 — Business Model Canvas

**Render the actual canvas.** Nine blocks in the real BMC layout, not nine text areas. Tapping a block opens a focused editor; the canvas fills in visually as they go, with a "4 of 9 blocks" indicator.

| Block | Input |
|---|---|
| Value Propositions | ↩ from M6 Q1 |
| Customer Segments | ↩ from M2 |
| Channels | **`chips-multi`** — Own website · App store · Instagram · TikTok · WhatsApp · Resellers · Direct sales · Marketplace · Physical shop · Other |
| Customer Relationships | **`chips-multi`** — Self-serve · Personal support · Community · Automated · Dedicated account · Other |
| **Revenue Streams** | **`chips-multi`** — Subscription · One-time sale · Commission · Freemium · Advertising · Licensing · Marketplace fee · Usage-based · Other. **Multi-select matters here** — mixed models are normal, and the current single box hides that. |
| Key Resources | `chips-multi` + repeater |
| Key Activities | `repeater` |
| Key Partnerships | **`repeater`** — partner + what they provide |
| Cost Structure | **`repeater`** — cost line + amount + currency, with a running monthly total |

Export the completed canvas as a branded PDF (uses the template from Round 11).

### Mission 9 — Build Prototype

| # | Becomes |
|---|---|
| 1 | **`chips-single`** — Paper sketch · Figma clickable · No-code app · Landing page · Slide walkthrough · Coded · Other |
| 2 | ↩ features from M6, as checkboxes: "which made it into the prototype?" |
| 3 | **`repeater`** — user flows, step by step |
| 4 | **`chips-multi`** — Figma · Canva · Bubble · Webflow · Glide · FlutterFlow · Adalo · Framer · Paper · Other |
| 5 | **`upload`** — link or file. **Required.** |
| 6 | **`repeater`** — three next steps, each with a date |

### Mission 10 — Prototype Testing *(rename — currently duplicates Mission 7's title)*

| # | Becomes |
|---|---|
| 1 | **`number`** — how many people tested it |
| 2 | **`chips-single`** — In person · Video call · Unmoderated · Group session |
| 3 | **`repeater`** — findings, each tagged `chips-single`: Confirmed · Contradicted · Surprising |
| 4 | **`upload`** notes or recordings + short summary |
| 5 | **`repeater`** — improvements with priority chips |

### Mission 11 — Service Selection

| # | Becomes |
|---|---|
| 1 | ↩ target market from M2 + **`number`** size estimate |
| 2 | **`chips-multi`** — Instagram · TikTok · WhatsApp · X · LinkedIn · Facebook groups · Google Ads · SEO · Influencers · Events · University campus · Referral · Cold outreach · Other |
| 3 | **`chips-single`** pricing model + **`number` + currency** price point |
| 4 | **`repeater`** — sales process steps |
| 5 | **`repeater`** — launch plan with dates, rendered as a timeline |

### Mission 12 — Market Validation

| # | Becomes |
|---|---|
| 1 | **`chips-multi`** — validation methods used |
| 2 | **`repeater`** — demand indicator + value |
| 3 | **`repeater`** — competitor table: name · link · price · one strength · one weakness |
| 4 | **`chips-single`** response + **`number`** willingness to pay |
| 5 | **`number` × 3** — TAM / SAM / SOM, each with currency, plus "how did you get to this number?" |

### Mission 13 — Build MVP

| # | Becomes |
|---|---|
| 1 | ↩ features from M6/M9 as checkboxes |
| 2 | **`chips-multi`** — No-code: Bubble/Glide/Softr/Webflow · Code: React/Next/Flutter/Laravel/Django/Node · Backend: Supabase/Firebase/AWS · Other |
| 3 | **`number` + unit** — days or weeks |
| 4 | **`chips-multi`** challenge types + a line |
| 5 | **`upload`** — link to the MVP. **Required.** |
| 6 | **`chips-single`** — Yes / Almost / Not yet → if not, a `repeater` of blockers |

### Mission 14 — Product-Market Fit Test

| # | Becomes |
|---|---|
| 1 | **`chips-single`** sentiment + short note |
| 2 | **metric grid** — signups · activated · retained day 7 · retained day 30, each a number |
| 3 | **`upload`** feedback + summary |
| 4 | **`number` %** retention, with a helper showing the calculation |
| 5 | **Replace the 1–10 self-rating with the Sean Ellis test.** Ask users: *"How would you feel if you could no longer use this?"* — Very disappointed / Somewhat / Not disappointed. Enter the % who said very disappointed. **40% is the recognised PMF threshold.** A founder rating their own PMF out of 10 measures optimism; this measures fit. |
| 6 | **`repeater`** improvements with priority |

### Mission 15 — Go to Market

| # | Becomes |
|---|---|
| 1 | **`chips-multi`** launch tactics + a line |
| 2 | **`repeater`** — campaign: channel · spend · result |
| 3 | **metric grid** — launch results |
| 4 | **`number`** users acquired |
| 5 | **`number` + currency** revenue |
| 6 | **`repeater`** growth next steps with dates |

---

## What this changes, in numbers

| | Before | After |
|---|---|---|
| Blank textareas | 75 | **11** |
| Questions answerable by tapping | 0 | ~40 |
| Questions carried forward | 0 | 9 |
| Visual/interactive exercises | 0 | 3 (two matrices, one canvas) |
| Duplicate questions | 12 | 0 |

The eleven remaining textareas are the ones that *should* be open — "what did you learn", "why did you choose this". Reflection deserves a blank page. Categorisation doesn't.

---
---

# The prompts

Five, in order. Paste one per message.

## PROMPT A — Build the Question Type System

```text
TASK: The 15 missions currently use 87 questions, of which 75 are blank
textareas. Before changing any mission content, build the input component
system that the new question set needs.

BUILD THESE ELEVEN INPUT TYPES as reusable components, driven by a schema so
mission content is data, not JSX:

  chips-multi   Tappable pills, multi-select, always ending with "Other →"
                which opens a text field. Selected state uses lime background
                with near-black text. Minimum 44px tap targets. Wraps to
                multiple lines on mobile.
  chips-single  Same, single selection.
  slider        1-10, with the ends labelled in words, current value shown
                large. Draggable and keyboard-accessible.
  matrix        A 2x2 grid. Cards are dragged onto it, or positioned by two
                sliders. Quadrants are labelled. See Prompt C.
  canvas        A named-framework layout with tappable blocks. See Prompt D.
  builder       A sentence with inline blanks. Each blank is either a chip
                set or a short input. The finished sentence reads back as
                prose.
  repeater      "Add another" rows. Each row is a mini-form defined per
                question. Rows are reorderable and deletable.
  number        Numeric input with a unit selector, and a currency selector
                where relevant (EGP, SAR, AED, USD).
  upload        File, URL, or pasted text — all three accepted. Shows what
                was attached. Existing OCR applies.
  text          One short line.
  textarea      Long-form. Keep the existing gate from Round 11.

RULES FOR ALL TYPES

1. EVERY question can carry an attachment, regardless of its type. A founder
   answering a chip question may still want to attach a screenshot. Put a
   quiet "Add file or link" affordance on every question.

2. NO CHIP LIST IS EVER CLOSED. "Other →" is mandatory on every chips-multi
   and chips-single, and what the founder types there is stored, so you can
   later see which options are missing from your taxonomies.

3. MULTI-SELECT IS THE DEFAULT for categories. A founder building in fintech
   AND healthcare is not an edge case, and neither is a business running
   subscription AND commission revenue. Only use chips-single where exactly
   one answer can be true (frequency, readiness).

4. SCHEMA-DRIVEN. Each question is a record:
     { id, missionId, order, type, label, helpText, whyItMatters,
       options[], allowOther, required, minWords, carriesFrom,
       attachmentAllowed, exampleAnswerId }
   Mission content lives in that schema. Never hardcode a question in a
   component.

5. ARABIC. Every type must work RTL and be labelled in both languages. Chip
   labels especially — a chip set is only faster than typing if the founder
   reads it instantly in their own language.

6. MOBILE FIRST. This is where these are answered. Chips beat typing on a
   phone, which is most of the point.
```

## PROMPT B — Carry Answers Forward Between Missions

```text
TASK: The same question is currently asked up to five times across the 15
missions, because nothing carries forward.

  "Who is your user"       — M1 Q3, M2 Q1, M2 Q2, M4 Q2, M11 Q1
  "What are your features" — M6 Q2, M9 Q2, M13 Q1
  "What did you learn"     — M7 Q5, M10 Q4, M14 Q3
  "What are your next steps" — M9 Q6, M10 Q5, M13, M14 Q6, M15 Q6

Each mission therefore feels like starting over, when it should feel like the
last one is being built on.

THE FIX

1. A FOUNDER PROFILE OBJECT that accumulates across missions:
     industry[], userSegment, userPersona, problemStatement,
     valueProposition, features[], assumptions[], businessModel[],
     channels[], pricing, metrics[]
   Every mission writes into it and reads from it.

2. CARRY-FORWARD FIELDS are pre-filled and editable, and clearly framed as a
   continuation rather than a repeat:

     "In Mission 1 you said the problem was:
      [their exact words, in an editable field]
      Sharpen it now that you know your user better."

   Never show a carried field as blank. Never show it as locked.

3. TRACK WHAT CHANGED. When a founder edits a carried answer, keep both
   versions. At the end of the journey they can see how their problem
   statement evolved from Mission 1 to Mission 4 — that is one of the most
   satisfying things a guided product can show someone.

4. THESE NINE FIELDS CARRY (see the redesign doc):
     M2 Q3 ← M1 Q2      M4 Q2 ← M2 Q1      M8 VP ← M6 Q1
     M8 Segments ← M2   M9 Q2 ← M6 Q2      M11 Q1 ← M2
     M13 Q1 ← M6/M9     M3 cards ← M1/M2   M7 Q1 ← M6 Q5 (riskiest assumption)

5. REMOVE THE DUPLICATE. M6 Q3 ("what benefits will users get") asks the same
   thing as M6 Q2 ("list key features"). Merge into one repeater with a
   feature column and a benefit column.

6. RENAME MISSION 10. It is currently titled "Solution Hypothesis Test",
   identical to Mission 7. Rename to "Prototype Testing" everywhere — the
   roadmap, the mission page, the schema and both locale files.
```

## PROMPT C — Turn Missions 3 and 5 Into Real Matrices

```text
TASK: Missions 3 and 5 are 2x2 matrices being collected as text fields.

Mission 3 currently asks: Problem 1 (textarea), Importance 1-10 (text),
Frequency 1-10 (text), Problem 2 (textarea), Importance (text), Frequency
(text), Which will you focus on (textarea). Seven fields to fill in a grid.

Mission 5 is the same shape with ideas, value and impact.

THE FIX — one interactive matrix component, used by both.

  1. Cards come from earlier missions where possible. Mission 3 pulls the
     problems the founder described in Missions 1 and 2. Mission 5 pulls
     nothing — ideas are new — so it starts with a repeater.

  2. "Add another" lets them add more cards. No fixed slots of two.

  3. Each card is positioned EITHER by dragging it onto the grid OR by two
     sliders — dragging on desktop, sliders on mobile where dragging is
     fiddly. Both update the same values.

  4. THE QUADRANTS ARE LABELLED, so the exercise teaches rather than just
     collects:

       Mission 3 — Importance × Frequency
         high/high  "Fix first"
         low imp/high freq  "Quick wins"
         high imp/low freq  "Big bets"
         low/low    "Ignore for now"

       Mission 5 — Value × Effort
         high value/low effort   "Do now"
         high value/high effort  "Plan it"
         low value/low effort    "Quick win"
         low value/high effort   "Drop it"

  5. When a card lands in a quadrant, name it back: "Fix first — this is
     both painful and constant." That single line is the lesson.

  6. The final question becomes a chips-single choosing from the cards
     actually plotted, defaulting to whatever sits highest-right. Then one
     short line: why this one.

  7. Export the finished matrix as an image into the mission recap and the
     PDF report.

  8. Fully keyboard-accessible, and the matrix must be readable and usable at
     390px width.
```

## PROMPT D — Make Mission 8 an Actual Business Model Canvas

```text
TASK: Mission 8 is the Business Model Canvas — a nine-block visual framework —
currently rendered as nine consecutive blank textareas. The visual structure
is the entire pedagogical point and it has been removed.

THE FIX

1. RENDER THE REAL CANVAS LAYOUT:

     ┌──────────┬──────────┬──────────┬──────────┬──────────┐
     │  Key     │  Key     │  Value   │ Customer │ Customer │
     │ Partners │Activities│  Props   │Relations │ Segments │
     │          ├──────────┤          ├──────────┤          │
     │          │  Key     │          │ Channels │          │
     │          │Resources │          │          │          │
     ├──────────┴──────────┼──────────┴──────────┴──────────┤
     │   Cost Structure    │        Revenue Streams          │
     └─────────────────────┴─────────────────────────────────┘

   On mobile this stacks vertically, in the same order, with the block name
   and a one-line explanation on each.

2. TAPPING A BLOCK opens a focused editor for that block only. The canvas
   fills in visually behind it. Show "4 of 9 blocks complete".

3. INPUT TYPE PER BLOCK — not nine identical textareas:

     Value Propositions      carried from Mission 6, editable
     Customer Segments       carried from Mission 2, editable
     Channels                chips-multi: Own website · App store · Instagram
                             · TikTok · WhatsApp · Resellers · Direct sales ·
                             Marketplace · Physical shop · Other
     Customer Relationships  chips-multi: Self-serve · Personal support ·
                             Community · Automated · Dedicated account · Other
     REVENUE STREAMS         chips-multi: Subscription · One-time sale ·
                             Commission · Freemium · Advertising · Licensing ·
                             Marketplace fee · Usage-based · Other
                             MULTI-SELECT IS ESSENTIAL HERE. Mixed revenue
                             models are normal and the current single box
                             hides that entirely.
     Key Resources           chips-multi + repeater for specifics
     Key Activities          repeater
     Key Partnerships        repeater: partner + what they provide
     Cost Structure          repeater: cost line + amount + currency, with a
                             running monthly total shown

4. EACH BLOCK CARRIES A ONE-LINE EXPLANATION, because most founders meeting
   the canvas for the first time do not know what "Key Activities" means:
     "Key Activities — the things your business must do every week for the
      model to work."

5. EXPORT the completed canvas as an image and as a branded PDF, using the
   document template from Round 11.

6. Once a block is filled, show a short quality signal rather than a score —
   "Revenue Streams: 2 selected, cost structure not yet filled". The rubric
   still assesses the whole mission; this is orientation, not grading.
```

## PROMPT E — The Answering Experience

```text
TASK: Rebuild how a founder moves through a mission's questions. Currently
all questions render on one long page as a stack of blank boxes, which is
what makes the missions feel like homework.

1. ONE QUESTION AT A TIME on mobile; two or three on desktop. A stepper at
   the top shows position ("Question 3 of 5") and lets them jump. Each
   question gets its own screen with room to breathe.

2. EVERY QUESTION CARRIES THREE THINGS ABOVE THE INPUT:
     - The question itself, in plain language
     - "Why this matters" — one sentence, collapsible, on by default the
       first time and collapsed thereafter
     - An estimated time — "about 2 minutes"

3. "SEE AN EXAMPLE" ON EVERY QUESTION — an anonymised real answer that scored
   well, shown in a panel, never pre-filled into the field. Founders cannot
   hit a standard they have not seen. This is the single highest-value
   addition in this prompt.

4. INSTANT, QUIET FEEDBACK. When an answer meets the bar, a small green tick
   and "Ready" appears. Not a score, not a celebration — just a signal that
   they can move on. When it does not, say what is missing in one line.

5. MOMENTUM, NOT CONFETTI. After each question, a small progress movement and
   the next question sliding in. On mission completion, something bigger.
   Avoid celebrating trivial actions — this audience finds that patronising
   faster than most.

6. SAVE STATE VISIBLY. "Saved 2 minutes ago" near the stepper. Leaving and
   returning restores exact position. Never lose an answer.

7. SHOW THE THREAD. At the top of each mission, one line connecting it to the
   last: "In Mission 2 you defined your user as [X]. This mission turns that
   into a problem statement you can test."

8. LET THEM SEE THE WHOLE MISSION. A "view all questions" toggle for founders
   who want to read ahead before starting. Some people need the map first.

9. ARABIC AND RTL throughout — the stepper direction, the chip wrapping, the
   slider direction, the matrix axes.

10. NEVER MORE THAN ONE PRIMARY BUTTON on screen. Currently the mission page
    has "Resubmit for Review" in three places.
```

---

## Sequence

| # | Prompt | Why here |
|---|---|---|
| 1 | A — input components | Everything else needs these to exist |
| 2 | B — carry-forward + renames | Cheap, and removes 12 duplicate questions |
| 3 | E — the answering experience | The shell the new inputs live in |
| 4 | C — the two matrices | Self-contained, high visible impact |
| 5 | D — the canvas | The biggest single build |

A and B could ship in a week and would already remove most of the friction your testers hit. C and D are the ones founders will talk about.

---

## Two decisions for you

**Mission 14's PMF question.** I've proposed replacing "rate your product-market fit 1–10" with the Sean Ellis test — asking *users* how disappointed they'd be to lose the product, and recording the percentage who say "very disappointed". 40% is the recognised threshold. It's a real measurement rather than founder self-assessment, but it requires the founder to actually survey users, which is more work. Your call whether Mission 14 should demand that.

**Phase structure.** Validation is currently missions 7, 10, 12 and 14 — scattered rather than contiguous, while Business Model, Strategy and Launch have one mission each. That's what produces a roadmap where phase names repeat. Worth deciding whether the phases should be re-cut into contiguous blocks before you rebuild the roadmap UI, because the two are hard to separate later.
