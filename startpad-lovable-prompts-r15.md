# StartPad — The Resubmit Loop (Round 15)

Fixing the AI review submit action, and rebuilding the mission page around it.

Worked from the Mission 1 screenshot at Attempt 1, score 20%, question 5 of 5.

---

## What's actually wrong

You asked about the submit button appearing at the bottom on a second attempt. That's the visible symptom. Underneath it there are **four separate defects**, and they compound — which is why the page feels wrong rather than just looking wrong.

### 1. There are two "Resubmit for Review" buttons on one screen

One in the yellow attempt banner near the top, one at the very bottom. They carry the **same label**, and they're in **different visual states** — the top one is solid indigo, the bottom one is faded. A founder now has to work out which button is the real one, and whether the faded one means "disabled" or "already pressed".

### 2. The button invites an action the page then refuses

The top banner says **"Refine your answers and resubmit."** Two thirds of the way down, in red: **"Fill the remaining questions to unlock review."** And the counter says **"1 of 5 answered."**

So the page asks for a resubmit, offers a button for it, and separately states that resubmitting is not possible. Whichever button the founder presses, the page has already told them it won't work.

### 3. "20%" means two different things, five times

Counted on the one screen:

| Where | Value | What it actually means |
|---|---|---|
| Mission progress bar, top | 0% | Journey progress — 0 of 15 missions |
| "1 of 5 tasks completed" | 20% | Completion |
| "Attempt 1 · Score 20%" | 20% | AI score |
| "1 of 5 answered" badge | 20% | Completion |
| "QUESTION 5 OF 5 · 20%" | 20% | Unclear — score or completion |
| "20% · Needs Improvement (70% required)" | 20% | AI score |

Completion happens to equal the score right now — both 20 — which is the worst possible coincidence, because a founder learns the wrong mapping and then can't unlearn it. When they answer a second question, completion jumps to 40% while the score stays 20 and the page appears to contradict itself.

### 4. The score on screen is out of date and doesn't say so

Score 20% is from attempt 1. The founder is now editing the answers that produced it. Every "20%" on the page is describing text that no longer exists in the field.

This is the same class of bug as the duplicated components in Round 9: **a value is stored when it should be derived.** A score is only valid for the exact answers it was computed from. The moment one character changes, it's history — and the page should say so rather than keep presenting it as current.

### And three more the screenshot shows

**The gibberish gate isn't firing.** The field contains `fdsfdsdsdfdfsdsadsds dad dad dada dad da...` with a word counter reading **26 / 25 words** — which presents as a pass. The AI feedback then complains about placeholder text `'sda'`, `'dsad'`. So nonsense reached the model, consumed an attempt and an API call, and came back with a score. The client-side check specified in Round 11 should have caught that before the request left the browser.

**The word counter rewards the wrong thing.** "26 / 25 words" tells a founder they're done. The gate is quality, not volume, and the counter is the only signal that looks like a completion meter.

**The sticky bottom nav is sitting on top of the content.** It overlaps the AI feedback rows. Anything sticky added below will collide with it unless the page reserves the space.

---

## The principle

**One mission. One primary action. One place it lives.**

At any moment there is exactly one thing the founder should do next, the page says what it is, and there is exactly one button for it. Everything else on the page is secondary or it's information.

---

## The state machine

Every mission attempt is in exactly one of five states, and the primary action is a pure function of that state. No component decides on its own whether to render a submit button.

```js
const PRIMARY_ACTION = {
  draft: {
    show:   false,                                  // absent, not disabled
    status: "Question 5 of 5 — answer this to send for review",
    cta:    { label: "Go to question 5", kind: "link" },
  },
  ready: {
    show:   true,
    status: "All 5 answered.",
    cta:    { label: "Send for AI review", kind: "primary", enabled: true },
  },
  reviewing: {
    show:   true,
    status: "Reviewing your answers — about 30 seconds",
    cta:    { label: "Reviewing…", kind: "primary", enabled: false },
  },
  returned: {
    show:   true,
    status: ({ edited }) => edited > 0
      ? `${edited} answer${edited > 1 ? "s" : ""} edited since attempt 1`
      : "Attempt 1 scored 20 out of 100. Edit at least one answer to resubmit.",
    cta:    { label: "Resubmit for review", kind: "primary", enabled: "hasEdits" },
  },
  passed: {
    show:   true,
    status: "Passed with 78 out of 100.",
    cta:    { label: "Continue to Mission 2", kind: "primary", enabled: true },
    secondary: { label: "Improve my answers", kind: "link" },
  },
};
```

**In `draft`, the submit button does not exist.** Not greyed out — absent. A disabled primary button is an unanswered question the interface refuses to explain. The status line says what's missing and links straight to it.

**In `returned`, the button enables only when something changed.** That is the rule you asked about directly:

```js
const isStale = a => a.scoredHash && a.scoredHash !== hash(a.value, a.evidenceIds);

const edited      = answers.filter(isStale).length;
const canResubmit = allRequiredAnswered && edited > 0;
```

Resubmitting identical text costs the founder an attempt and costs you an API call to be told the same thing twice. When `edited === 0`, the button stays disabled and the status line says exactly why — in the status line, never in a tooltip, because a founder on a phone cannot hover.

---

## Where the button lives

**One sticky action bar**, pinned above the bottom navigation, present on every mission screen.

```
┌─────────────────────────────────────────────────────────────┐
│  ▲  2 answers edited since attempt 1                        │
│     2 need more detail · 1 piece of evidence needed         │
│                                        [ Resubmit for review ]│
└─────────────────────────────────────────────────────────────┘
│  Dashboard   My Startup Journey   Resources   Toolbox  …     │
└─────────────────────────────────────────────────────────────┘
```

- The **▲ handle expands** the readiness detail — which answers, what each still needs, each row jumping to that question. That content already exists on your page as the band reading *"2 answers need more detail · 2 answers don't read as real answers yet · 1 piece of evidence needed"*. It's good, and it's stranded at the bottom where a founder mid-answer never sees it.
- **Remove both existing buttons** — the one in the yellow banner and the one at the page bottom. The yellow banner keeps its text and gets a link to the weakest answer instead.
- **Reserve the space.** `padding-bottom: calc(var(--nav-h) + var(--action-bar-h))` on the mission page, so nothing is ever covered. The nav is currently overlapping the feedback rows.

That is the "bottom appearing on a second attempt" done properly: it's always there, it always says the true state, and there's only one of it.

---

## Stale scores

The moment an answer changes, everything computed from it is marked out of date. Nothing is deleted — the founder should still see what they scored — but nothing pretends to be current either.

| Element | Fresh | After an edit |
|---|---|---|
| Question score badge | `Depth 1 · Specificity 2` | ~~`Depth 1`~~ **Edited — not yet scored** |
| Mission score banner | `20 out of 100 · needs 70` | `Last score 20 out of 100 (attempt 1). You've edited 2 answers, so this is out of date.` |
| Question pill in the stepper | filled | outlined with a dot |
| Highest-gain fix card | shown | shown, marked `from attempt 1` |

The AI feedback rows stay visible after an edit — a founder rewriting an answer needs the critique in front of them, not cleared the instant they touch the field.

---

## Never print a bare percentage again

| Thing | Never | Always |
|---|---|---|
| Questions answered | `20%` | **`1 of 5 answered`** |
| Mission score | `20%` | **`Score 20 / 100 · needs 70`** |
| Journey progress | `0%` | **`0 of 15 missions`** |
| Question quality | `20%` | per-criterion bars — no single number |
| XP to next level | a bar | **`20 XP to next level`** |

Counts don't collide. Percentages do.

---

## Getting more out of the loop

The review cycle is the most valuable thing on the platform and it currently gives back less than it could.

**Move the highest-gain fix to the top.** *"Do this first — your highest-gain fix: [Relevance] Replace all placeholder text with actual industry and problem descriptions"* is the single most useful element on the page, and it's below the fold beneath a 5-question form. It belongs directly under the score banner with a button that jumps to that question.

**Show the delta after a resubmit.** This is what makes a second attempt feel like progress rather than a retry:

```
Attempt 2 · 65 / 100      ▲ 45
  Question 5   Depth        1 → 3   ▲
               Specificity  2 → 4   ▲
               Evidence     0 → 2   ▲  (screenshot attached)
  Question 1   unchanged
```

**Keep an attempt history.** `Attempt 1 · 20 · 12 Sep` → `Attempt 2 · 65 · 14 Sep`, each openable to see what was written. Founders should be able to watch their own thinking sharpen — and this is the same versioning the carry-forward work in Round 14 needs.

**Predict readiness before spending an attempt.** Run the cheap local checks — length, gibberish, evidence attached, placeholder detection — and show an honest forecast in the action bar: *"2 answers likely to score low on Depth."* Not a fake score. A warning that saves a wasted round trip.

**Wire up the thumbs.** The feedback rows already have 👍/👎. Route those into a review queue so the rubric prompts actually improve. Collecting signal and discarding it is worse than not asking.

**Make the download the artefact.** The page already names a **Founder artifact: "Problem observation brief"**. "Download full report (PDF)" should produce exactly that — the Mission 1 artefact from Round 14 — not a copy of the assessment. Three download CTAs currently compete: *Mission handout*, *See the full assessment*, *Download full report (PDF)*. Two of those are the same thing.

---

## The page has too many bands

Counting from the screenshot, a founder passes through **nine full-width sections** before reaching question 5: mission header, objectives, curriculum band, learning support, tools, task progress, attempt banner, AI mentor, assumption loop, answered counter, level and badges.

Proposed structure:

```
┌──────────────────────────────────────────┬───────────────┐
│ Mission header  · phase · points ·       │               │
│                   attempt                │  Mission brief │
├──────────────────────────────────────────┤  (collapsed   │
│ SCORE BANNER (returned only)             │   on return)  │
│   20 / 100 · needs 70                    │               │
│   ▸ Do this first — highest-gain fix     │  Objectives   │
│     [Go to question 3]                   │  Learning     │
├──────────────────────────────────────────┤  outcome      │
│                                          │  Tools        │
│   QUESTION 5 OF 5                        │  AI Mentor    │
│   one question, room to breathe          │  Assumptions  │
│   why this matters · what a good          │               │
│   answer needs · evidence · feedback     │               │
│                                          │               │
├──────────────────────────────────────────┴───────────────┤
│ ▲ readiness summary          [ Resubmit for review ]     │  sticky
├──────────────────────────────────────────────────────────┤
│ Dashboard  My Startup Journey  Resources  …              │  nav
└──────────────────────────────────────────────────────────┘
```

On mobile the right rail becomes one collapsed **"Mission brief"** accordion above the question, closed by default after the first visit.

**Move the XP and badge band.** *Level 2 · 100 XP · First Move · Momentum · Evidence Attached · Deep Diver · Mission Ready* currently sits between the progress counter and the question the founder is trying to answer — and it carries a disclaimer: *"Practice mission rewards participation and completeness. It does not increase your evidence strength or mission review score."* An element that needs a line explaining it doesn't count shouldn't be interrupting the work. Show it on the completion screen and on the dashboard.

---
---

# The prompts

Six, in order. Paste one per message.

## PROMPT A — One Submit Action, Driven by State

```text
PAGE: /missions/:id — the mission detail and answering page.

THE PROBLEM

There are two "Resubmit for Review" buttons on the mission page: one in the
yellow attempt banner near the top, one at the bottom of the page. They carry
the same label and render in different visual states, so a founder cannot tell
which is real or whether the faded one is disabled or already pressed.

Worse, the page contradicts itself. The top banner says "Refine your answers
and resubmit." Further down, in red, it says "Fill the remaining questions to
unlock review," and the counter says "1 of 5 answered." The page offers an
action and separately states that the action is impossible.

THE FIX

1. DELETE BOTH BUTTONS. Every "Resubmit for Review" currently rendered on the
   mission page is removed. The yellow attempt banner keeps its text and gets
   a text link to the weakest-scoring answer instead of a button.

2. ONE COMPONENT, <MissionPrimaryAction>, RENDERED IN EXACTLY ONE PLACE — a
   sticky action bar pinned above the bottom navigation. No other component in
   the mission tree may render a submit control. Add an ESLint rule or a test
   that fails the build if a second one appears, the same guard pattern used
   for the duplicate-component problem in a previous round.

3. THE ACTION IS A PURE FUNCTION OF ATTEMPT STATE. Five states:

   draft       Not all required questions answered.
               NO SUBMIT BUTTON AT ALL — absent, not greyed out.
               Status line: "Question 5 of 5 — answer this to send for review"
               with a link that jumps straight to it.
               A disabled primary button is an unanswered question the
               interface is refusing to explain.

   ready       All required answered, never submitted.
               Button: "Send for AI review" — enabled.
               Status: "All 5 answered."

   reviewing   Submitted, awaiting the model.
               Button: "Reviewing…" — disabled.
               Status: "Reviewing your answers — about 30 seconds"

   returned    Scored below the 70 threshold.
               Button: "Resubmit for review".
               ENABLED ONLY IF AT LEAST ONE ANSWER HAS CHANGED since the last
               submission. See rule 4.

   passed      Scored 70 or above.
               Button: "Continue to Mission 2" — enabled.
               Secondary text link: "Improve my answers".

4. THE RESUBMIT RULE — this is the core of this prompt:

     const isStale = a =>
       a.scoredHash && a.scoredHash !== hash(a.value, a.evidenceIds);

     const edited      = answers.filter(isStale).length;
     const canResubmit = allRequiredAnswered && edited > 0;

   When edited === 0, the button is disabled and the STATUS LINE says why:
     "Attempt 1 scored 20 out of 100. Edit at least one answer to resubmit."
   NEVER put that explanation in a tooltip. Most founders answer these on a
   phone and cannot hover.

   When edited > 0:
     "2 answers edited since attempt 1"

   Resubmitting unchanged text costs the founder an attempt and costs you an
   API call to be told the same thing twice.

5. LAYOUT. The sticky bottom navigation currently OVERLAPS the page content —
   in the current build it sits on top of the AI feedback rows. Give the
   mission page:
     padding-bottom: calc(var(--nav-h) + var(--action-bar-h));
   and stack the action bar directly above the nav. Nothing may ever be
   covered.

6. RTL. The action bar mirrors for Arabic — status text and button swap sides.
```

## PROMPT B — Mark Scores Stale the Moment an Answer Changes

```text
PAGE: /missions/:id, and the mission scoring store.

THE PROBLEM

The page shows "Attempt 1 · Score 20%" in three places while the founder is
actively editing the answers that produced that score. Every 20% on screen is
describing text that no longer exists in the field.

This is a stored value that should be derived. A score is only valid for the
exact answers it was computed from. One character changes and it is history.

THE FIX

1. STORE A HASH WITH EVERY SCORE. When the AI returns a result, persist
   scoredHash = hash(answerValue + attachedEvidenceIds) alongside the score,
   per question. An answer is stale when its current hash differs.

2. RENDER STALE STATE EVERYWHERE THE SCORE APPEARS — do not delete the old
   score, do not present it as current:

     Question score badge
       fresh   "Depth 1 · Specificity 2 · Evidence 0"
       stale   old numbers struck through, plus "Edited — not yet scored"

     Mission score banner
       fresh   "Score 20 out of 100 · needs 70"
       stale   "Last score 20 out of 100 (attempt 1). You've edited 2
                answers, so this score is out of date."

     Question pill in the stepper
       fresh   filled
       stale   outlined with a dot

     Highest-gain fix card
       stale   still shown, labelled "from attempt 1"

3. KEEP THE AI FEEDBACK VISIBLE AFTER AN EDIT. A founder rewriting an answer
   needs the critique in front of them. Do not clear the feedback rows the
   moment they type.

4. NEVER PRINT A BARE PERCENTAGE. The current page shows "20%" five times
   meaning two different things — completion and score — which happen to be
   equal right now, so founders learn the wrong mapping. Replace:

     questions answered    "20%"  ->  "1 of 5 answered"
     mission score         "20%"  ->  "Score 20 / 100 · needs 70"
     journey progress      "0%"   ->  "0 of 15 missions"
     question quality      "20%"  ->  per-criterion bars, no single number
     XP to next level      a bar  ->  "20 XP to next level"

   Counts do not collide. Percentages do.

5. Also fix the stepper disagreement: the pill row currently shows question 4
   ticked while the counter says "1 of 5 answered" and question 5 contains
   text. Every completion indicator reads from one derived selector —
   answeredCount — and nothing computes its own.
```

## PROMPT C — The Readiness Bar

```text
PAGE: /missions/:id — the sticky action bar from PROMPT A.

THE PROBLEM

The page already knows exactly what is blocking review. It says so, at the
very bottom, under everything:

  "2 answers need more detail · 2 answers don't read as real answers yet ·
   1 piece of evidence needed"

That is the most actionable sentence on the page and a founder answering
question 5 never sees it.

THE FIX

1. MOVE IT INTO THE STICKY ACTION BAR, as a collapsed summary line under the
   status line. Always visible, on every question.

     ▲  2 answers edited since attempt 1
        2 need more detail · 1 piece of evidence needed
                                        [ Resubmit for review ]

2. THE HANDLE EXPANDS to a checklist, each row naming the question and what it
   still needs, each row jumping to that question:

     Question 1   Needs 2-3 sentences on what specifically fails   →
     Question 3   Doesn't read as a real answer yet                →
     Question 5   No evidence attached — Evidence scores 0         →

   Rows clear themselves as the founder fixes each one, so the bar visibly
   empties. That emptying is the motivation.

3. THE EVIDENCE ROW IS THE HIGHEST-VALUE ONE. The existing copy is already
   good — "Evidence is what moves your Evidence score above 0. One screenshot,
   link, or set of interview notes is enough." Repeat that line in the
   checklist, because a founder who attaches one screenshot moves a whole
   criterion off zero and most never realise it.

4. PREDICT, HONESTLY. Run the cheap local checks — length, placeholder
   detection, gibberish, evidence attached — and show a forecast:
     "2 answers likely to score low on Depth."
   Never show a predicted number. A forecast that saves a wasted attempt is
   useful; a fake score is not.

5. On mobile the bar is one line plus the handle. It must never take more than
   ~72px collapsed.
```

## PROMPT D — Attempt History and Score Deltas

```text
PAGE: /missions/:id and the mission completion screen.

THE PROBLEM

The page says "Attempt 1" and nothing else. After a resubmit it will say
"Attempt 2" and nothing else. A founder who rewrites five answers and moves
from 20 to 65 sees a new number with no sense of what they did to earn it —
which is the entire lesson of the exercise.

THE FIX

1. SHOW THE DELTA ON EVERY RE-REVIEW RESULT:

     Attempt 2 · 65 / 100      up 45
       Question 5   Depth        1 -> 3
                    Specificity  2 -> 4
                    Evidence     0 -> 2   (screenshot attached)
       Question 1   unchanged

   Per-criterion, not just the total. The total tells them they improved; the
   criteria tell them what improving looked like.

2. ATTEMPT HISTORY, on the mission page:

     Attempt 1 · 20 / 100 · 12 Sep    ▸
     Attempt 2 · 65 / 100 · 14 Sep    ▸

   Each opens read-only: what they wrote, what the AI said. Founders should be
   able to watch their own thinking sharpen. This is the same answer
   versioning the carry-forward work needs, so build it once.

3. IF A CRITERION WENT DOWN, SAY SO PLAINLY and name it. A rewrite that loses
   specificity is the most common way a second attempt scores worse, and the
   founder will not spot it alone.

4. AFTER THREE ATTEMPTS WITH NO IMPROVEMENT, change the offer. Do not block
   them — replace the resubmit button's helper line with:
     "Three attempts, similar scores. The AI Mentor can walk through question
      3 with you before you try again."
   and surface the mentor. A fourth blind attempt helps nobody and costs you
   a model call.

5. WIRE UP THE THUMBS. The feedback rows already carry thumbs up and down.
   Route those into a review queue keyed to the rubric prompt that produced
   the line. Collecting that signal and discarding it is worse than not
   asking.
```

## PROMPT E — Stop Nonsense Reaching the Model

```text
PAGE: /missions/:id — the answer field and the submit path.

THE PROBLEM

The screenshot shows a field containing:

  "fdsfdsdsdfdfsdsadsds dad dad dada dad da da dad d ad a d ad a da da d ad a
   da d ad a d ad"

with a word counter reading "26 / 25 words", which presents as a pass. The AI
feedback then reports placeholder text — 'sda', 'dsad'. So nonsense was
accepted, submitted, scored, and an attempt was consumed.

The client-side quality gate specified previously is either not running on
this field or is not blocking submission. Every one of these costs a model
call to return a result the browser could have predicted for free.

THE FIX

1. RUN THE GATE ON BLUR, NOT ONLY ON SUBMIT. When a founder leaves a field
   whose content fails the check, show inline, in a neutral tone:

     "This doesn't look like a finished answer yet. Two or three sentences on
      what specifically fails — and for whom — is enough."

   Neutral, not scolding. Some founders type a placeholder deliberately,
   intending to return.

2. THE CHECK, as previously specified — dictionary hit rate, adjacent-key
   runs, repeated-token ratio, long character runs — plus one addition this
   screenshot demands: FLAG SHORT REPEATED FRAGMENTS. "dad dad dada dad da da
   dad" passes a word count and fails every other test.

3. BLOCK SUBMISSION while any required answer fails the check, and say which:
     "Question 3 and question 5 don't read as real answers yet."
   The readiness bar already carries this line — reuse it, don't write a
   second one.

4. FIX WHAT THE WORD COUNTER IMPLIES. "26 / 25 words" reads as a completed
   objective, and it is the only element on the page shaped like a progress
   meter. Change it to a quiet minimum indicator:
     below   "25 words minimum"
     met     "25 word minimum met" — grey, no tick, no colour change
   Never style it as a target reached. The gate is quality; volume is a floor.

5. LET THEM SAVE ANYWAY. Failing the gate blocks SUBMISSION, never saving.
   Drafts persist exactly as typed.
```

## PROMPT F — Rebuild the Mission Page Layout

```text
PAGE: /missions/:id

THE PROBLEM

A founder on question 5 scrolls past nine full-width sections to reach it:
mission header, objectives, curriculum band, learning support, tools, task
progress, attempt banner, AI mentor, assumption loop, answered counter, and a
level-and-badges band. The question — the only thing they came to do — is
below all of it.

THE FIX

1. THE STRUCTURE:

   ┌──────────────────────────────────────────┬───────────────┐
   │ Mission header · phase · points · attempt│               │
   ├──────────────────────────────────────────┤ MISSION BRIEF │
   │ SCORE BANNER (returned state only)       │ (collapsed on │
   │   Score 20 / 100 · needs 70              │  return       │
   │   Do this first — your highest-gain fix  │  visits)      │
   │   [Go to question 3]                     │               │
   ├──────────────────────────────────────────┤ Objectives    │
   │                                          │ Learning      │
   │   QUESTION 5 OF 5                        │ outcome       │
   │   one question, room to breathe          │ Tools         │
   │   why this matters                       │ AI Mentor     │
   │   what a good answer needs               │ Assumptions   │
   │   the field                              │               │
   │   add evidence                           │               │
   │   AI feedback for this answer            │               │
   │                                          │               │
   ├──────────────────────────────────────────┴───────────────┤
   │ ▲ readiness summary        [ Resubmit for review ]       │ sticky
   ├──────────────────────────────────────────────────────────┤
   │ Dashboard  My Startup Journey  Resources  Toolbox  …     │ nav
   └──────────────────────────────────────────────────────────┘

   On mobile the right rail becomes ONE collapsed "Mission brief" accordion
   above the question, closed by default after the first visit. Everything in
   it is reference material — needed once, not on every scroll.

2. MOVE THE HIGHEST-GAIN FIX TO THE TOP. "Do this first — your highest-gain
   fix: [Relevance] Replace all placeholder text with actual industry and
   problem descriptions" is the single most useful element on the page and it
   currently sits below a five-question form. Put it directly under the score
   banner with a button that jumps to the question it refers to.

3. MOVE THE XP AND BADGE BAND OFF THE ANSWERING SCREEN. "Level 2 · 100 XP ·
   First Move · Momentum · Evidence Attached · Deep Diver · Mission Ready"
   currently interrupts the page between the progress counter and the
   question. It carries its own disclaimer — "Practice mission rewards
   participation and completeness. It does not increase your evidence
   strength or mission review score." An element that needs a line explaining
   it does not count should not be interrupting the work. Show it on the
   mission completion screen and on the dashboard.

4. CONSOLIDATE THE DOWNLOADS. Three compete right now: "Mission handout",
   "See the full assessment", "Download full report (PDF)". The last two are
   the same document. Keep two, clearly different:
     - "Mission handout" — the brief, before starting
     - "Download your Problem observation brief (PDF)" — the FOUNDER ARTIFACT
       the curriculum band already names. Make the download produce that
       artefact, not a copy of the assessment. The assessment stays on screen
       behind "See the full assessment", which expands in place.

5. KEEP THESE — they are the best things on the page:
     "Welcome back — resuming at question 5."
     "Why this matters" with the time estimate
     "What a good answer needs" with the concrete instruction
     "Evidence is what moves your Evidence score above 0."
     "We read the text inside images and PDFs so the AI Mentor can reference
      them."
     The per-criterion feedback rows with thumbs
   Do not lose any of them in the restructure.

6. ONE PRIMARY BUTTON ON SCREEN AT ANY TIME. Everything else is a text link or
   a secondary. Count them after the rebuild — if there are two filled indigo
   buttons visible at once, one of them is wrong.
```

---

## Sequence

| # | Prompt | Why here |
|---|---|---|
| 1 | **A** — one submit action | The bug you reported. Fixes the duplicate button and the resubmit rule |
| 2 | **B** — stale scores | A is only honest if the score it sits next to is honest |
| 3 | **E** — the quality gate | Cheapest win. Stops paying for reviews of placeholder text |
| 4 | **C** — the readiness bar | Needs A's bar to exist |
| 5 | **D** — attempt history | The value layer. Needs B's hashes |
| 6 | **F** — the layout | Largest change, and the others settle what goes in it |

A alone fixes what you reported. A + B + E is a day's work and removes every contradiction on the current screen.

---

## One decision for you

**What happens when a founder passes.** Right now the threshold is 70 and a returned attempt can be resubmitted indefinitely. Once someone scores 78, should the mission stay open for improvement?

My recommendation: **yes, but quietly.** Primary action becomes "Continue to Mission 2"; "Improve my answers" stays as a text link. A founder who wants 90 should be able to chase it — but the platform should never imply that 78 isn't good enough to move on, because the cost of a founder stalling on Mission 1 polishing a passing answer is far higher than the benefit of the extra points.
