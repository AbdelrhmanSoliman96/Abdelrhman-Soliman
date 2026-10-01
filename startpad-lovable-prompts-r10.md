# StartPad — Lovable Prompts (Round 10)

Two prompts rebuilding the referral program.

---

## Why the current version can't work

The card says: *"Invite friends and earn 500 bonus points for each person who joins."* Five things are wrong with that, and only one of them is design.

**1. Points have no exchange rate.** This account shows 175 points that nobody can trace to anything. Points don't unlock, buy, or mean anything yet. Offering 500 more of an unbacked currency is not an incentive — it's an IOU from a bank with no reserves.

**2. "Friends" is the wrong ask.** A 22-year-old in Cairo does not have friends casually looking for a startup platform. Asking them to spam a group chat costs social capital and returns nothing. The ask has to be something they'd *want* to send.

**3. The reward is one-sided.** The referrer gets 500 points; the person invited gets nothing. That means the referrer has to make the pitch empty-handed. Every referral program that works gives the sender something to *give*.

**4. It rewards signups, not founders.** "For each person who joins" is an invitation to create fake accounts. It also pulls in people who never build anything, which makes your community worse, not better.

**5. The empty state advertises failure.** "Friends referred: 0 · Bonus points earned: 0." And the referral code box renders empty — either it isn't generating or it's a rendering bug.

---

## The reframe

**Founders don't want points. They want a co-founder, a teammate, or an audience.**

You already have the Collaboration Hub, where projects need designers, developers and marketers. You already have "My circle" in Community. You already have a working unlock ladder in streak rewards — *unlock mission templates at 3 days, mentor discount at 10*.

So this shouldn't be a referral program at all. It should be **recruiting**, and it should pay in the things that are actually scarce on StartPad: mentor time, priority, status, and access.

Rename it, reward both sides, gate it on real effort, and give people something worth posting.

---
---

## PROMPT A — Rebuild the Referral Program as "Bring a Founder"

```text
PAGE: Referral program (currently a card reading "Invite friends and earn 500
bonus points for each person who joins").

THE PROBLEM
Points are not a reward — this product has no exchange rate for them, and one
account already shows 175 points that no code derives. "Friends" is the wrong
ask for this audience. The reward is one-sided, so the referrer pitches
empty-handed. And rewarding signups invites fake accounts and pulls in people
who never build.

Rebuild it around what founders actually want and what StartPad can actually
give.

═══════════════════════════════════════════════════════════════
1. RENAME AND REFRAME
═══════════════════════════════════════════════════════════════

  Not "Referral Program". Not "Invite friends".

  Title:    "Bring a founder"
  Subtitle: "Building alone is the hardest way to do it. Bring someone who's
             building too — you both get more out of it."

  Two entry points, because they are genuinely different intents:

    A) "Bring a co-founder"  → they join YOUR project in the Collaboration Hub
       directly. This solves a real problem the product already has: projects
       sitting there with "Looking for: designer" and nobody to fill it.

    B) "Bring a founder"     → they start their own journey, and you both
       appear in each other's "My circle" in Community.

  Option A is the one that makes this a product feature rather than a
  marketing loop. Lead with it.

═══════════════════════════════════════════════════════════════
2. REWARD BOTH SIDES — the invited person gets something too
═══════════════════════════════════════════════════════════════

  The person sending the invite must have something to GIVE. That is what
  makes the ask socially easy instead of socially expensive.

    THEY GET:  their first mentor session unlocked, no streak required
               (normally gated behind a 10-day streak)
    YOU GET:   one mentor session credit

  Say this explicitly on the share message: "Here's a free mentor session —
  I've got one for you." That is a gift, not a favour request.

═══════════════════════════════════════════════════════════════
3. A MILESTONE LADDER, NOT PER-HEAD POINTS
═══════════════════════════════════════════════════════════════

  Per-head rewards have no finish line. Milestones do, and the existing streak
  reward system already proves this pattern works here.

    1 founder   → 1 mentor session credit for each of you
    3 founders  → your own private group in Community
                  + "Squad Builder" badge on your profile
    5 founders  → your project featured in the Collaboration Hub for a month
                  + priority mentor booking
    10 founders → permanent "Founding Community Builder" badge
                  + a call with the StartPad team

  Rules for the ladder:
    - Only promise what you can deliver. Do NOT include investor
      introductions, funding, or anything you do not control.
    - Show progress as a bar with the next unlock named:
      "2 of 3 — one more founder unlocks your private group"
    - Never show "0 referred". Show the ladder with the first rung highlighted
      and what it unlocks.

═══════════════════════════════════════════════════════════════
4. QUALIFY ON EFFORT, NOT ON SIGNUP
═══════════════════════════════════════════════════════════════

  A referral counts when the invited person SUBMITS THEIR FIRST MISSION —
  not when they create an account.

  Why this matters:
    - It cannot be farmed with throwaway accounts; a mission submission takes
      real work
    - It aligns the incentive: you want founders who build, not signups
    - It gives you an honest activation metric

  Show the in-between state clearly, because it is motivating rather than
  discouraging:
    "Amr joined · working on Mission 1 — your credit unlocks when he submits"

  ANTI-ABUSE:
    - One reward per unique invited account, ever
    - Block self-referral: same device fingerprint, same IP cluster, same
      phone number, email aliasing (plus-addressing, dot tricks)
    - Cap at 10 qualified referrals per user per month
    - Flag for manual review: 3+ referrals from one IP in 24h, or accounts
      whose submissions are near-identical
    - Reversible — if an account is later found fraudulent, the credit is
      revoked and the referrer notified

═══════════════════════════════════════════════════════════════
5. FIX WHAT'S BROKEN
═══════════════════════════════════════════════════════════════

  - The referral code box renders EMPTY. Either the code isn't generating or
    it isn't rendering. Fix it, and generate codes at account creation so one
    always exists.
  - Codes should be human-readable and speakable, not a UUID:
    "ABDELRHMAN-K3F" or similar. People say these out loud.
  - The copy button needs a confirmed state ("Copied") — it currently gives
    no feedback.
  - Prefer a full link over a bare code: startpad.me/join/ABDELRHMAN-K3F.
    A code alone requires the recipient to know where to type it.

═══════════════════════════════════════════════════════════════
6. WHERE IT LIVES
═══════════════════════════════════════════════════════════════

  Not a page nobody visits. Surface it where the intent already exists:

    - Collaboration Hub → on any project with unfilled "Looking for" roles:
      "Know a designer? Bring them in →"
    - Community → in "Founders on your mission": "Know someone starting out?"
    - After a mission is passed → the moment of highest satisfaction and the
      best time to ask
    - Profile / settings → the full ladder page

  Do NOT put it in the main nav. It is contextual, not a destination.
```

---
---

## PROMPT B — Make It Worth Sharing

```text
PAGE: Referral share flow — the assets and channels.

THE PROBLEM
The current flow offers a bare referral code. Nobody shares a code. This
audience shares images, links with good previews, and WhatsApp messages.

═══════════════════════════════════════════════════════════════
1. THE SHARE ARTIFACT — a founder card, not a code
═══════════════════════════════════════════════════════════════

  Generate a shareable image the founder would actually want to post, because
  it says something about THEM rather than about StartPad:

    ┌─────────────────────────────┐
    │  [avatar]                   │
    │  Abdelrhman                 │
    │  Building in Cairo 🇪🇬        │
    │                             │
    │  Mission 4 of 15            │
    │  ████████░░░░░░  Validation │
    │                             │
    │  "Fintech for gig workers"  │
    │                             │
    │  Join me on StartPad        │
    │  startpad.me/join/ABD-K3F   │
    └─────────────────────────────┘

  Rules:
    - Two sizes: 1080×1920 (Instagram/WhatsApp Story) and 1200×630 (link
      preview). Story format first — that is where this audience posts.
    - It shows THEIR progress, THEIR idea, THEIR city. Self-expression is why
      people share; a branded ad is not.
    - Available in Arabic with correct RTL layout and an Arabic-native font.
    - Generated server-side so it works when shared, and cached per user with
      a regeneration trigger when their mission changes.
    - Never include anything private — no scores, no rubric feedback, no email.

═══════════════════════════════════════════════════════════════
2. CHANNELS — WhatsApp first
═══════════════════════════════════════════════════════════════

  In MENA, WhatsApp is the channel. It is usually the one omitted.

    [WhatsApp]  ← primary, largest, first
    [Instagram Story]  [Copy link]  [X]  [LinkedIn]

  Pre-fill the WhatsApp message — do not make them write it:

    "I'm building a startup through StartPad — 15 guided missions, AI
     feedback, free. I've got a free mentor session to give you if you start.
     startpad.me/join/ABD-K3F"

  Make it editable before sending. A pre-filled message people can adjust
  converts far better than either a blank box or an unchangeable template.

═══════════════════════════════════════════════════════════════
3. THE LANDING PAGE FOR AN INVITED PERSON
═══════════════════════════════════════════════════════════════

  startpad.me/join/[code] must NOT be the generic marketing homepage. It is a
  personal invitation and should read like one:

    "Abdelrhman invited you to StartPad"
    [their avatar, their city, the mission they're on]

    "You get a free mentor session when you start — Abdelrhman's gift."

    → [Accept the invite]  (into signup, with the code attached)

    Below: what StartPad is, in three lines. The 15-mission path. Nothing
    else. This page has one job.

  If the invite is for a specific PROJECT (option A in Prompt A), show the
  project instead: its name, description, the role that's open, and who's
  already on the team.

  Carry the code through signup so attribution survives OAuth, and attach it
  to the account at creation — never rely on a cookie alone.

═══════════════════════════════════════════════════════════════
4. THE PAGE ITSELF — replace the current card
═══════════════════════════════════════════════════════════════

  Order, top to bottom:

    1. The ladder with progress — the next unlock named, not a count of zero
    2. The share block — the generated card preview, then the channel buttons
    3. Your link, with a copy button that confirms
    4. Who you've brought — avatars, their status ("working on Mission 1",
       "qualified ✓"), so it feels like a team rather than a tally
    5. Rules in plain language: when a referral counts, the monthly cap, and
       what each unlock gives

  When the founder has brought nobody yet, section 4 shows the ladder's first
  rung and what it unlocks — never "0 friends referred".

═══════════════════════════════════════════════════════════════
5. MEASURE
═══════════════════════════════════════════════════════════════

  Track: share-block views, shares by channel, invite-page visits, signups,
  and QUALIFIED referrals (first mission submitted). The gap between signups
  and qualified is the number that tells you whether the program is bringing
  founders or just accounts.

  If WhatsApp doesn't dominate the channel split in this region, something is
  wrong with the flow — check it early.
```

---

## Two things to decide before building

**Can you actually deliver a mentor session per qualified referral?** With two mentors currently in the system, ten referrals means ten sessions. If the supply isn't there, use priority booking or an AI Mentor deep-dive as the first rung instead, and put the real session higher up the ladder. An unlock you can't honour is worse than a smaller one you can.

**Does "Squad Builder" fit the voice?** It's gaming-adjacent, which matches "Loadout" — but "Loadout" was already flagged as a label nobody can guess. Pick one register and stay in it rather than having two half-committed metaphors.
