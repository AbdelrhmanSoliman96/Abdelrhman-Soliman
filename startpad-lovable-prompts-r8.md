# StartPad — Lovable Prompt (Round 8)

One prompt: the authenticated verification pass that the sandbox couldn't reach.

**Precondition:** sign in once via the preview so a session exists. Every check below requires one.

If the run is too long for a single pass, split it at Phase 4 — Phases 1–3 are routing, Phases 4–6 are data consistency.

---

## Why this is the gap that matters

The logged-out half of the route table is already green: private routes deny, public routes allow. The logged-in half is the half that was actually broken — a signed-in founder landing on the full marketing page at `/`, confirmed from a screenshot showing the marketing hero, stat band, mission roadmap and closing CTA rendering underneath the **logged-in** navigation.

That redirect needs a session, so it is exactly what the sandbox could not test. Same for the session-badge fix across three surfaces and the mission runner's progress state.

Everything unverified is therefore concentrated in the one area with a known defect.

---
---

# Set 1 — Authenticated Verification

## PROMPT A — Verify the Authenticated Half of the App

```text
TASK: Run a verification pass on authenticated flows. A signed-in session now
exists in the preview. Do not fix anything until the whole pass is reported —
I want the failure list first, then we decide what to fix.

Today's date for all time-based assertions: 20 August 2026.

═══════════════════════════════════════════════════════════════
PHASE 1 — ROUTE TABLE, SIGNED IN
═══════════════════════════════════════════════════════════════

Visit each route while signed in and record where you land and which shell
renders (PUBLIC nav = About / How It Works / Knowledge Hub / Sign in / Get
started · APP nav = Dashboard / My Startup Journey / Resources / Loadout /
AI Tools / More / avatar).

  ROUTE                    EXPECTED WHEN SIGNED IN
  /                        redirect → /dashboard        ← THE KNOWN BUG
  /signin                  redirect → /dashboard
  /signup                  redirect → /dashboard
  /dashboard               renders, APP shell
  /journey                 renders, APP shell
  /journey/mission/1       renders, APP shell
  /community               renders, APP shell
  /collaboration           renders, APP shell
  /mentoring               renders, APP shell
  /ai-tools                renders, APP shell
  /resources               renders, APP shell
  /loadout                 renders, APP shell
  /profile                 renders, APP shell
  /about                   renders, APP shell (same content, app nav)
  /how-it-works            renders, APP shell
  /knowledge-hub           renders, APP shell
  /contact                 renders, APP shell
  /faq  /privacy  /terms   renders, APP shell

  Row 1 is the priority. A signed-in user must NOT see the marketing page.
  Confirm explicitly that you land on /dashboard and never see the hero
  headline, the stat band, or the "Ready to launch your startup?" CTA.

  On every SHARED route (/about through /terms), confirm:
    - The APP nav renders, not the public nav
    - No "Get started" or "Sign in" button appears anywhere on the page,
      including in-page CTA bands and the footer

═══════════════════════════════════════════════════════════════
PHASE 2 — RETURN-TO AFTER SIGN-IN
═══════════════════════════════════════════════════════════════

  1. Sign out.
  2. Navigate directly to /journey/mission/1
  3. Expect: redirect to /signin with the destination preserved
     (e.g. /signin?next=/journey/mission/1)
  4. Sign in.
  5. Expect: land on /journey/mission/1 — NOT /dashboard.

  Repeat for /loadout and /community. Report the landing route for each.

  Also confirm the destination survives a wrong-password attempt: fail the
  sign-in once, then succeed, and check you still return to the original route.

═══════════════════════════════════════════════════════════════
PHASE 3 — NO FLASH OF THE WRONG SHELL
═══════════════════════════════════════════════════════════════

  Throttle the network to Slow 3G, hard-reload /dashboard while signed in, and
  record video or a frame sequence of the first 1500ms.

  FAIL if the public nav, a "Sign in" link, or a "Get started" button paints in
  ANY frame before the app shell.
  PASS if the first painted state is either the app shell or a shell-neutral
  skeleton.

  Repeat on /about while signed in — a SHARED route is where this is most
  likely to slip, because the public shell is the natural default.

  Also: after signing out, press the browser back button. Confirm no
  authenticated view is restored from cache.

═══════════════════════════════════════════════════════════════
PHASE 4 — SESSION STATE ACROSS THREE SURFACES
═══════════════════════════════════════════════════════════════

The account holds three mentor sessions. All three are in the past as of
20 August 2026:

  Emily Rodriguez · Fundraising      · 27 May 2026, 10:00 · 30 min
  Sarah Johnson   · Product Strategy · 9 Jun 2026,  13:30 · 30 min
  Sarah Johnson   · Product Strategy · 13 Aug 2026, 13:30 · 30 min

Check ALL THREE surfaces that render sessions:
  a) Dashboard → the mentoring block
  b) /mentoring
  c) /collaboration → My Sessions tab

For each surface, record for each session: which section it appears in
(Upcoming / Past) and the exact badge text.

  EXPECTED on all three surfaces:
    - All three sessions appear under PAST, never under Upcoming
    - No badge reads "Upcoming" or "Pending"
    - Badges read one of: Completed / Didn't take place / Cancelled
    - The three surfaces agree with each other exactly

  This bug has appeared in three places across two review rounds because three
  components computed state independently. If the three surfaces disagree now,
  that tells us the shared component was not actually adopted everywhere —
  report which surface diverges.

  Also confirm every session time renders with a named timezone
  ("13:30 your time (GMT+3)") rather than a bare time.

═══════════════════════════════════════════════════════════════
PHASE 5 — COUNTERS MUST AGREE WITH BADGES
═══════════════════════════════════════════════════════════════

On the Dashboard, record the session stat row and check it against Phase 4:

  Upcoming   → expected 0
  Completed  → must equal the number of sessions actually badged Completed.
               If all three are badged "Didn't take place", Completed is 0,
               not 3.
  Mentors    → 2

  A counter must never be derived from "rows in the Past section". If
  Completed reads 3 while no session is badged Completed, the counter is still
  counting rows — report it.

═══════════════════════════════════════════════════════════════
PHASE 6 — GAMIFICATION AND PROGRESS CONSISTENCY
═══════════════════════════════════════════════════════════════

Record these values from each page and check they agree:

  VALUE            DASHBOARD   /journey   /journey/mission/1
  Missions done    ______      ______     ______
  Total points     ______      ______     ______
  Level            ______      ______     ______
  Current mission  ______      ______     ______
  Streak (days)    ______      ______     ______

  KNOWN DISCREPANCIES TO CHECK SPECIFICALLY:
    - Level previously read "Level 2, 100 XP" on the mission page and
      "Level 1, Beginner" on /journey at the same moment. Confirm they now
      match.
    - Total points previously read 175 with 0 of 15 missions complete.
      If points are still non-zero with zero completions, report what the
      points are derived from.
    - Mission 1 duration read "2-3 hours" on the mission page and "1-2 hours"
      in the AI Tools guidance panel. Confirm one value.

  PROGRESS BAR: on the Dashboard's current-mission card, confirm the journey
  progress bar renders EMPTY when the label reads "0 of 15 completed". It
  previously rendered 100% filled. Check the computed width in the DOM, not
  just visually — and audit every other progress bar in the app for the same
  defect (/journey, mission page, profile completion).

  PHASE COUNT: confirm the phase list is identical on /journey and on the
  landing page's roadmap — same names, same count, no phase name repeating.
  The landing page previously said "8 phases" and then listed twelve groups
  with Validation appearing four times.

═══════════════════════════════════════════════════════════════
REPORTING
═══════════════════════════════════════════════════════════════

Return a table, one row per check, with columns:
  Phase · Check · Expected · Actual · PASS/FAIL

Then list every FAIL with:
  - The file and component responsible, if you can identify it
  - Whether it is a data bug, a routing bug, or a rendering bug
  - Whether it is a regression or was never fixed

Do not fix anything in this pass. Report first.
```

---

## After the report

Two things to decide once you have it:

**If Phase 4 shows the three surfaces disagreeing**, the shared `SessionCard` and `useSessionState` hook were not adopted everywhere. That's the fix to insist on — not a third independent patch.

**If Phase 3 fails**, the shell is resolving after hydration. That needs the auth check moved before first render, not a loading spinner bolted on top.

Also worth adding once this passes: **a regression test for the AR → reload → EN path**, since the reload condition is what hid that i18n bug from the existing toggle suite.
