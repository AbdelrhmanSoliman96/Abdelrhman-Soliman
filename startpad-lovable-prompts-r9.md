# StartPad — Lovable Prompts (Round 9)

Three prompts closing the six failures from the authenticated verification pass.

---

## The six failures are three problems

Read the FAIL list again and a pattern shows up. **Three of the six share one root cause: a correct implementation exists, and something else was built beside it instead of using it.**

| Failure | Canonical version | Duplicate that shipped instead |
|---|---|---|
| Auth CTAs leak on 5 pages | Auth-aware pattern on About / How-It-Works / Contact | Raw `navigate(PATHS.signup)` in KnowledgeArticlePage, 3 GuidePages, ReadinessAssessment |
| Dashboard mentoring diverges | `MentorsSection.tsx` — uses the shared `useSessionState` hook | `ActivityBand.tsx:126` — recomputes `upcoming` from raw dates, no badges |
| Session stat row missing | `MentorsSection.tsx` — has `counts.upcoming` / `counts.completed` | Nothing renders it; the file is imported nowhere |
| Phase count mismatch | `MissionRoadmap.tsx` — derives 8 phases from real mission data | `RoadmapJourney.tsx` — hardcodes 5, plus a stale `landing.json` string saying 8 |

`MentorsSection.tsx` being **dead code with the correct logic in it** is the clearest statement of the problem. The shared component was built exactly as specified, then a second component was written that reimplemented the same thing worse, and that one won.

The remaining two are different in kind:

- **175 points with zero completions** is a stale DB row (`user_progress.total_score`) that no client code derives. A data problem.
- **Two "Level" scales** is a genuine product ambiguity, not a bug. It needs a decision before it needs code.

So: **Prompt A** deletes the duplicates and adds guards so this cannot recur. **Prompt B** fixes the stale score. **Prompt C** resolves Level.

---
---

## PROMPT A — Adopt the Canonical Implementations, Delete the Duplicates

```text
TASK: Three failures from the verification pass share one root cause — a
correct implementation exists and a duplicate was built beside it. Fix all
three by adopting the canonical version and deleting the duplicate, then add
guards so it cannot happen again.

═══════════════════════════════════════════════════════════════
1. AUTH CTAs LEAKING TO SIGNED-IN USERS
═══════════════════════════════════════════════════════════════

Signed-in users see "Get started" / sign-up CTAs on five pages. The auth-aware
pattern was applied to About, How-It-Works and Contact only.

Offending call sites:
  src/features/knowledge/KnowledgeArticlePage.tsx:178
  src/features/guides/GuidePage.tsx:148
    (renders GuideStartupIdeas, GuideValidateStartupIdea,
     GuideBusinessPlanGenerator)
  src/pages/ReadinessAssessment.tsx:359

DO NOT patch these five individually — that is how the problem started.

  a) Extract ONE <AuthAwareCTA> component from whichever of About /
     How-It-Works / Contact has the cleanest implementation. Props:
       signedOutLabel, signedOutTo, signedInLabel, signedInTo, variant
     It reads auth state internally. No caller branches on it.

  b) Replace all five call sites with it. Suggested targets:
       Knowledge article  → signed out: "Start free"  signed in: "Back to my mission"
       Guides             → signed out: "Start free"  signed in: "Go to dashboard"
       Readiness          → signed out: "Start free"  signed in: "Go to dashboard"

  c) Migrate About / How-It-Works / Contact onto the same component so there
     is exactly one implementation in the codebase.

  d) ADD A LINT RULE that fails the build on any raw navigate(PATHS.signup),
     navigate(PATHS.signin), or <Link to={PATHS.signup}> outside
     AuthAwareCTA and the auth pages themselves. This is the guard — without
     it the sixth page will leak next month.

  e) Then grep the whole codebase for signup/signin navigation and report
     every remaining call site, so we know the five were the complete set.

═══════════════════════════════════════════════════════════════
2. DASHBOARD MENTORING SURFACE + MISSING STAT ROW
═══════════════════════════════════════════════════════════════

src/features/dashboard/MentorsSection.tsx already uses the shared
useSessionState hook and already exposes counts.upcoming / counts.completed.
It is imported nowhere — dead code.

src/features/overview/ActivityBand.tsx:126 renders the mentoring surface
instead, computing upcoming itself with raw `new Date(session_date) > now`,
with no state badges and no Upcoming/Past sections.

  a) ADOPT MentorsSection. Render it wherever the mentoring surface belongs.
  b) DELETE the bespoke session logic from ActivityBand.tsx — including the
     raw date comparison at line 126 and the "past: N · mentors: N" counts.
     Counting rows in the past section is the original bug wearing a new
     label; counts must come from the shared hook's derived states.
  c) The stat row must read: Upcoming (from derived state), Completed (only
     sessions actually badged Completed — with three no_show sessions this is
     0, not 3), Mentors.
  d) Confirm all THREE surfaces — dashboard, /mentoring, /collaboration →
     My Sessions — now render from the same component and agree exactly.

  e) ADD A GUARD: a unit test asserting that any component rendering mentor
     sessions imports useSessionState. Or simpler and stronger — export the
     raw session rows only through the hook, so no component can reach the
     unprocessed dates.

  ALSO ANSWER: /dashboard renders no mentoring block while /overview does.
  What is the intended difference between these two routes? If they are
  meant to be one page, say so and I will spec the merge.

═══════════════════════════════════════════════════════════════
3. PHASE COUNT MISMATCH
═══════════════════════════════════════════════════════════════

src/components/MissionRoadmap.tsx derives 8 phases from real mission data.
src/components/RoadmapJourney.tsx hardcodes 5 (discovery / validation / model
/ build / launch), and the landing page renders "15 missions. 5 phases."
A stale landing.json string still says "15 missions, 8 phases" — so the
landing page currently disagrees with the dashboard AND with itself.

  a) The derived 8 are canonical: Discovery, Analysis, Ideation, Validation,
     Business Model, Development, Strategy, Launch.
  b) DELETE the hardcoded array in RoadmapJourney.tsx. Derive from the same
     mission data MissionRoadmap uses, via a shared selector.
  c) Fix the stale landing.json heading, and derive the count from the data
     rather than writing a number into a translation string. A hardcoded
     count in a copy file will drift again the moment a phase is added.
  d) Check the Arabic translation file for the same stale string.

  e) ADD A BUILD GUARD, alongside the existing mission-schema guard: fail if
     any phase list is defined outside the canonical mission data.

═══════════════════════════════════════════════════════════════
REPORT
═══════════════════════════════════════════════════════════════

For each of the three: what you deleted, what now renders, and the guard you
added. Then confirm the full grep from 1(e) found no further leaks.
```

---
---

## PROMPT B — Reconcile the Stale Score

```text
TASK: user_progress.total_score reads 175 for this account while
mission_submissions and user_achievements are both empty. No client code
derives it — it is an orphaned value from an earlier award path.

This is the same class of bug as the session dates: a derived value was
stored, then drifted away from what it was derived from.

  a) DECIDE WHERE POINTS COME FROM and write it down. Points should be a
     function of things that actually happened:
       completed missions × their point value
       + achievements earned
     Nothing else.

  b) DERIVE IT AT READ TIME rather than storing it, matching the pattern
     already used for session state. If a stored column is needed for query
     performance, it must be recomputed by a database trigger on every
     submission and achievement write — never updated by client code.

  c) BACKFILL: recompute total_score for every user from their actual
     submissions and achievements. Report how many rows changed and by how
     much — if many accounts carry inflated scores, that is worth knowing
     before anyone sees a number drop.

  d) MAKE IT EXPLAINABLE. Total points becomes tappable, opening a breakdown
     of where each point came from. If the breakdown cannot account for the
     total, the total is wrong — and the breakdown is what makes that
     visible instead of silent.

  e) AUDIT for the same pattern elsewhere. Any stored column holding a value
     derivable from other rows — streak counts, achievement counts, mission
     completion counts, tool usage totals — is the same bug waiting. List
     what you find; do not fix them in this pass.
```

---
---

## PROMPT C — Resolve the Two Level Scales

This one needs a product decision before code. My recommendation is in the prompt; override it if you disagree.

```text
TASK: Two incompatible systems are both called "Level":

  src/components/ProgressTracker.tsx:37-41
    Level from completed missions → currently Level 1, "Beginner"

  src/features/missions/questXp.ts + QuestRewards.tsx
    Level from per-attempt XP at 60 XP/level → currently Level 2

Both render simultaneously on different pages. This is not a rendering bug —
it is two different ideas about what progress means, and it needs a decision.

RECOMMENDATION — one "Level", derived from completions:

  Per-attempt XP rewards effort; completions reward outcome. For a product
  whose core value is a rigorous 70%-to-pass evaluation, rewarding attempts
  is backwards: a founder can accumulate XP by resubmitting without ever
  improving, and the number stops meaning anything. It also puts the two
  systems in direct conflict — one says you are progressing while the other
  says you have completed nothing, which is exactly what the account shows
  today.

  So:
    a) LEVEL = f(completed missions). One definition, one selector, read by
       every surface. ProgressTracker's is canonical.
    b) Keep the XP mechanic but RENAME it and scope it — "Mission XP",
       visible only inside a mission, showing effort within that mission.
       Never displayed as "Level" and never shown on the dashboard or
       journey page.
    c) Delete the 60-XP-per-level scale entirely, or fold it into the
       mission-local display only.
    d) Confirm dashboard, /journey and the mission page all read the same
       selector and show the same number.

  If you would rather keep XP as the headline progression, that is a
  defensible choice — but then completions must stop being called "Level"
  too, and XP must only be awarded for improvement (a higher score than the
  previous attempt), not for submitting.

  Tell me which you are implementing before you write it.
```

---

## Where I'd start

**Prompt A**, and specifically the auth CTA leak inside it. It is user-visible today on five pages, the fix is mechanical, and the lint rule in step 1(d) is what stops the pattern recurring — which matters more than the five pages themselves.

Prompts A and B can run in parallel; C needs your decision first.

## Two things worth confirming separately

**`/journey` now redirects to `/dashboard`, and `/journey/mission/1` to `/mission/1`.** If the journey page and dashboard were deliberately merged, that resolves the three-overlapping-names problem from Round 2 and is a good outcome — but the app nav still shows "Dashboard" and "My Startup Journey" as separate items pointing at the same place. Worth confirming it was intentional.

**`founder_timezone` is NULL on all three session rows**, so times fall back to the browser's detected zone. That works today but shifts if a founder travels or uses a different device. The profile field exists — it just isn't being populated.

## Still genuinely blocked

Phase 3's slow-3G frame capture and the DOM progress-bar widths can't be code-verified — a `width: 100%` bar with a same-colour fill computes as 0% in the formula and still renders full. Those need the browser session whenever an admin can mint one.
