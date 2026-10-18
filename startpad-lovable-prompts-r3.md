# StartPad — Lovable Prompts (Round 3)

Twelve prompts from the 19 August review, grouped by **the page they fix**.

Each set opens with a framing note and closes with a **Why this order**. Paste one prompt per message — never concatenate, and let each finish before sending the next.

**Run Set 2 · Prompt A first.** You are collecting phone numbers and storing AI transcripts with no privacy policy.

| Set | Page / area | Prompts |
|---|---|---|
| 1 | Auth routing (whole app) | A |
| 2 | Legal & help pages (new) | A, B |
| 3 | User profile | A |
| 4 | Sessions + placeholder data (whole app) | A, B |
| 5 | Landing page | A |
| 6 | Mission runner & gamification | A |
| 7 | AI Tools | A |
| 8 | Resources & Knowledge Hub | A |
| 9 | Sign in / Sign up | A |
| 10 | Dashboard | A |

Design tokens: navy `#0A1D34` headlines, green `#047857` primary, white rounded cards with soft shadows.
Outstanding from Round 2 and still not done: **Set 5·A** (app nav diet), **Set 7·A** (Arabic audit), **Set 7·B** (mobile audit).

---
---

# Set 1 — Auth Routing

One prompt, and it closes the issue you raised directly. The two navigation shells are already correct; what's missing is enforcement at the route level.

## PROMPT A — Separate Pre-Login and Post-Login for Real

```text
PAGE: Whole app — routing and shell selection.

THE PROBLEM
The public shell and the app shell are already built correctly and they already
differ. But the ROUTE is not guarded, so a signed-in user still lands on the
full marketing homepage.

Confirmed: the marketing page at "/" renders with the LOGGED-IN navigation
(Dashboard, My Startup Journey, Resources, Loadout, AI Tools, More, Abdelrhman,
Sign out) — hero, stat band, "Everything you need to launch", the mission
roadmap, "Why we built this", mission and vision, "Built different", "Why MENA?
Why now?", closing CTA and footer. Roughly twelve screens of sales pitch for
someone who already signed up.

The CTAs are auth-aware ("Go to dashboard" instead of "Start free"), so the
components know. The route doesn't.

THE FIX — implement this exact route table:

  ROUTE                    LOGGED OUT              LOGGED IN
  /                        marketing page          redirect → /dashboard
  /dashboard               redirect → /signin      app shell
  /journey  /journey/*     redirect → /signin      app shell
  /community               redirect → /signin      app shell
  /collaboration           redirect → /signin      app shell
  /mentoring               redirect → /signin      app shell
  /ai-tools                redirect → /signin      app shell
  /resources               redirect → /signin      app shell
  /loadout                 redirect → /signin      app shell
  /profile /settings       redirect → /signin      app shell
  /signin  /signup         auth page               redirect → /dashboard
  /about /how-it-works     public shell            APP shell, same content
  /knowledge-hub /*        public shell            APP shell, same content
  /readiness-assessment    public shell            APP shell, same content
  /privacy /terms /faq     public shell            APP shell, same content

RULES

1. THREE ROUTE TYPES, declared per route — not inferred inside components:
     PUBLIC_ONLY   — signin, signup. Logged-in users are redirected away.
     PRIVATE       — dashboard, journey, community, etc. Logged-out redirected.
     SHARED        — marketing, about, knowledge hub, legal pages. Both allowed,
                     but the SHELL switches to match auth state.
   "/" is a special case: SHARED for logged-out, redirect for logged-in.

2. RETURN-TO. When a logged-out user hits a private route, send them to
   /signin?next=/the/original/path and return them there after sign-in. Never
   dump them on the dashboard having lost where they were going.

3. NO FLASH. The wrong shell must never paint, even for one frame. Resolve auth
   before the first render — server-side, or with a route-level loader that
   holds a skeleton in the shell-neutral layout. Do NOT default to the public
   shell and swap after hydration.

4. ONE SHELL DECISION, ONE PLACE. A single layout component reads auth state and
   picks the nav. No component anywhere else should branch on "is the user
   logged in" to decide which nav to show.

5. The profile-completion banner renders ONLY inside the app shell. It must
   never appear on the marketing page, the legal pages, or the auth screens.

6. SIGN OUT redirects to "/" and clears state so the back button cannot restore
   an authenticated view.

TEST AND REPORT — walk every row of the table in both states and tell me the
result for each. Specifically confirm: signed in, visiting "/" lands on
/dashboard; signed out, visiting /journey/mission/1 lands on signin and returns
to that mission afterwards.
```

**Why this order.** Standalone and self-contained. Do it early — several later prompts add new public pages, and they need the route table to exist first.

---
---

# Set 2 — Legal & Help Pages

Two prompts. **Prompt A is the most urgent item in this entire document** — not because it's hard, but because you are collecting personal data today with nothing published. Prompt B is the FAQ and help layer you asked for.

## PROMPT A — Privacy Policy, Terms, Cookies and Signup Consent

```text
PAGE: New pages at /privacy, /terms, /cookies — plus the signup form and the
site footer.

THE PROBLEM
StartPad collects first name, last name, PHONE NUMBER, email and password at
sign-up, then stores AI conversation transcripts, mission answers, uploaded
screenshots, PDFs and documents. There is no privacy policy, no terms of
service, and no consent checkbox anywhere in the flow. The footer offers only
About and Contact.

This is a compliance problem, not a nice-to-have:
- Egypt's Personal Data Protection Law (Law 151 of 2020) requires a privacy
  notice and a stated lawful basis before collection.
- Saudi PDPL and the UAE federal data protection law require the same.
- Google Sign-In and Apple Sign-In BOTH require a published privacy policy in
  their developer terms — the current OAuth integrations are out of compliance.
- App stores reject submissions without one.

THE FIX

1. CREATE /privacy — a real privacy policy covering, at minimum:
     - Who the data controller is (StartPad, by GrowthLabs) and how to contact
       them: hello@startpad.me
     - What is collected: account data (name, email, phone, password hash, date
       of birth, occupation status), usage data, mission answers and uploaded
       files, AI conversation transcripts, device and analytics data, OAuth
       profile data from Google and Apple
     - The lawful basis for each category
     - THIRD PARTIES that receive data — name them: the AI model provider, the
       email provider, analytics, Typeform and Google Forms if survey export is
       used, and any hosting or storage provider
     - Whether data leaves the user's country, and the safeguard used
     - Retention periods per category
     - User rights: access, correction, deletion, portability, objection, and
       withdrawal of consent — with a working route to exercise them
     - Children: state the minimum age (see Set 3) and how minors are handled
     - A "last updated" date

2. CREATE /terms — acceptable use, account rules, IP (make explicit that the
   founder owns their mission answers and uploaded content), AI output
   disclaimer (guidance, not professional legal/financial advice), mentor
   session conduct, termination, liability, governing law.

3. CREATE /cookies — what is set, by whom, for what, and how to opt out. If any
   non-essential cookie or analytics tag fires, add a consent banner that
   genuinely blocks them until accepted. Do not ship a banner that only
   pretends.

4. SIGNUP CONSENT — directly above the "Create Account" button:
     [ ] I agree to the Terms of Service and Privacy Policy
   An UNTICKED checkbox, both words linked, opening in a new tab. The button
   stays disabled until it is ticked. Implied consent is not sufficient under
   Egypt's PDPL. Store the consent timestamp and the policy version against the
   user record.
   Add the same consent line under the Google and Apple buttons as text:
   "By continuing you agree to our Terms and Privacy Policy."

5. FOOTER — add a legal row on EVERY page, public and app:
     Privacy Policy · Terms of Service · Cookie Policy · Contact
   Keep it visually quiet — small, muted, below the existing links.

6. ACCOUNT DELETION — a working "Delete my account" in profile settings that
   actually deletes or anonymises, with a confirmation step and a stated
   timeframe. A privacy policy promising deletion with no mechanism is worse
   than no policy.

Write these in plain, readable English, not boilerplate legalese — the audience
is 20-year-old founders. Add a short plain-language summary box at the top of
the privacy policy: "The short version: we collect X, we use it for Y, we never
sell it, and you can delete it any time."

IMPORTANT: I am drafting structure and coverage, not giving legal advice. Have
a lawyer qualified in Egypt and the GCC review these before launch.
```

## PROMPT B — FAQ and Help Centre

```text
PAGE: New pages at /faq and /help — plus entry points from the footer, the app
shell, and the existing chat bubble.

THE PROBLEM
There is no FAQ, no help centre, and no self-serve support anywhere in StartPad.
The only support surface is a floating chat bubble that presumably reaches a
human. That does not scale, and it means every founder with a basic question
either waits or leaves.

THE FIX

1. CREATE /faq — a searchable, accordion FAQ grouped into six sections. Write
   real answers, not placeholders:

   GETTING STARTED
     - What is StartPad and who is it for?
     - Is it really free? What, if anything, costs money?
     - Do I need an idea before I start?
     - How long does the whole journey take?
     - Can I use StartPad in Arabic?
     - Do I need a co-founder or a team?

   THE MISSIONS
     - What are the 15 missions and what order do they go in?
     - How long does one mission take?
     - What happens if I fail a mission? Can I resubmit?
     - What score do I need to pass? (state the 70% threshold)
     - How does the AI score my answers? What are the five criteria?
     - Can I skip a mission or go out of order?
     - What are points, levels, XP and streaks for?

   AI TOOLS
     - Which AI tools are available and what does each do?
     - Does the AI see my mission answers? (be direct about this)
     - Is my data used to train AI models? (answer honestly)
     - Can the AI answer in Arabic?
     - What does "What this tool will use — 2 of 4 ready" mean?

   MENTORS AND COMMUNITY
     - How do I book a mentor? Is it free?
     - What timezone are session times shown in?
     - What happens if I miss a session or need to reschedule?
     - Who can see my community posts?
     - What are the community rules?

   ACCOUNT AND PRIVACY
     - Why do you ask for my phone number?
     - Why do you ask for my age?
     - How do I change my email or password?
     - How do I delete my account and what happens to my data?
     - Who can see my profile?
     - Is my startup idea confidential?

   PROGRAMS AND INVESTORS
     - How does "Apply to programs & investors" work?
     - Do you take equity? (answer plainly — this is the question founders
       most want answered and least expect a straight answer to)
     - Do you introduce founders to investors directly?

2. CREATE /help — a fuller help centre with the same content organised as
   browsable articles, plus a search box, plus "Still need help? Contact us"
   with the email and expected response time.

3. ENTRY POINTS
     - Footer: FAQ and Help links in the legal row.
     - App shell: "Help" in the avatar dropdown menu.
     - Chat bubble: before opening a human conversation, show the three most
       relevant FAQ answers for the current page. Most questions never need a
       person.
     - Mission pages: a "?" next to the score explaining the rubric, deep-linked
       to the relevant FAQ answer.

4. CONTEXTUAL HELP. Each FAQ answer carries an anchor so any page can deep-link
   to it. The AI Tools readiness counter links to its explanation. The mission
   score links to the scoring criteria answer.

5. Every FAQ answer must be written to be translated later — short sentences,
   no idioms, no wordplay.

Tell me which answers you could not write because the underlying behaviour is
undecided. Those are product decisions I need to make, and I would rather see
the list than have them invented.
```

**Why this order.** A is compliance and blocks nothing else — ship it today. B needs the footer row from A to exist, and its answers will surface undecided product questions worth knowing about early.

---
---

# Set 3 — User Profile

One prompt covering both fields you asked for, plus the consequence each carries.

## PROMPT A — Add Date of Birth and Current Status

```text
PAGE: User profile (/profile or /settings), the profile-completion banner, and
the sign-up flow.

THE REQUIREMENT
Add two fields to the user profile: age, and current occupational status.

THE FIX

1. STORE DATE OF BIRTH, NOT AGE.
   An age integer is wrong within twelve months and cannot correct itself.
   Store date_of_birth as a date; derive age at read time.
     - Field label: "Date of birth"
     - Input: a proper date picker with a year selector that starts near the
       likely range, not a spinner starting at the current year
     - Helper text: "We use this to tailor missions and to meet legal
       requirements. It is never shown publicly."
     - NEVER display date of birth on a public profile. Show nothing, or an age
       band ("22") if there is a genuine product reason.

2. MINIMUM AGE — decide and enforce it.
   This is the consequence of collecting DOB: the moment you know age, you know
   when a user is a minor, and a Gen Z founder platform WILL have 16- and
   17-year-olds.
     - Set a minimum age (16 is a common floor; 18 avoids most complexity).
     - Validate at sign-up: under the minimum, block account creation with a
       clear, non-punitive message.
     - If you allow 16–17: they need guardian consent under Egypt's PDPL, Saudi
       PDPL and GDPR-equivalent regimes, and you should gate mentor video calls,
       public posting and any investor introduction behind an adult account.
     - Reflect whichever you choose in the privacy policy (Set 2·A) and the FAQ.
   Tell me which minimum you implemented so I can confirm it is the right call.

3. CURRENT STATUS — a single-select field.
     Label: "What are you doing right now?"
     Options, in this order:
       Student
       Recent graduate
       Employed full-time
       Employed part-time
       Freelancer / self-employed
       Founder (full-time)
       Founder (alongside another commitment)
       Between roles
       Other
     Store as a stable enum key, not the display string, so it survives
     translation into Arabic.

4. ADD ONE MORE FIELD — it is what makes status useful rather than decorative:
     Label: "How many hours a week can you give to your startup?"
     Options: Under 5 · 5–10 · 10–20 · 20+ · Full-time
   Together, status and hours are the strongest predictor you will have of who
   finishes the journey.

5. USE THEM. Do not collect data you do not act on:
     - PACE THE WEEKLY GOAL. The Journey page currently sets a flat goal of
       3 missions per week for everyone. A student in exam season and a
       full-time founder should not get the same target. Derive the weekly goal
       from hours available.
     - Adjust the mission time estimates shown ("1-2 hours") against the
       founder's availability.
     - Use status for community matching — "founders like you" — alongside the
       existing mission-based matching.
     - Never use age for matching or ranking.

6. WHERE THE FIELDS LIVE.
   The profile-completion banner currently reads "You're 63% there" and lists
   Country, Industry, Startup stage. Add date of birth, current status and
   hours to the SAME completion set — do not create a second nag. And implement
   the R2 recommendation while you are in there: put the fields INLINE in the
   banner as dropdowns rather than sending the user to a separate checklist.
   Six quick fields, done in under a minute, banner gone permanently.

7. Do NOT add these to the sign-up form. Sign-up is already five fields plus a
   phone number. Collect these after first login, in the banner.

8. Every new field must be editable later, must appear in the data export, and
   must be covered by the privacy policy from Set 2·A.
```

**Why this order.** Run after Set 2·A so the privacy policy already covers the new categories, and so the minor-handling decision is reflected in a published document rather than retrofitted.

---
---

# Set 4 — Sessions & Placeholder Data

Two prompts. Prompt A fixes one bug that appears in three separate places — fix it centrally or it will stay broken. Prompt B removes five instances of visible fake content.

## PROMPT A — One Session Component, One Derived State

```text
PAGE: Dashboard ("Past sessions"), Mentoring, and Collaboration Hub → My
Sessions. The same bug renders in all three.

THE PROBLEM
Today is 19 August 2026. All three surfaces show the same three sessions with
the same wrong badges:

  Emily Rodriguez — Fundraising     — May 27, 10:00 AM, 30 min — "Upcoming"
  Sarah Johnson  — Product Strategy — Jun 9,  1:30 PM,  30 min — "Upcoming"
  Sarah Johnson  — Product Strategy — Aug 13, 1:30 PM,  30 min — "Pending"

All three are in the past. Two are badged "Upcoming". On the Dashboard they sit
under a heading that literally says "Past sessions" — so the section is derived
correctly while the badge inside it is not.

The Dashboard also shows "Completed 3" in its stat row while no session carries
a completed state. That counter is counting rows in the past section rather than
sessions that completed.

This was reported in Round 2 and half-fixed: the sectioning landed, the badge
did not. It is now visible in three places, which means it is being rendered by
three components.

THE FIX

1. ONE SHARED COMPONENT. Build a single <SessionCard> and a single
   useSessionState() hook. Dashboard, Mentoring and Collaboration Hub all
   consume them. No surface computes session state on its own.

2. DERIVE STATE AT RENDER — never read a stored status field for time-based
   state:

     function deriveSessionState(session, now = new Date()) {
       if (session.cancelledAt) return "cancelled";
       if (session.endsAt < now) {
         return session.attended ? "completed" : "no_show";
       }
       if (session.startsAt <= now && now <= session.endsAt) return "live";
       if (!session.confirmedAt) return "awaiting_confirmation";
       return "confirmed";
     }

3. SIX STATES, each with its own colour AND its own icon shape so the
   difference survives for colour-blind users:

     live                  → green pulse dot  "Live now"
     confirmed             → green tick       "Confirmed"
     awaiting_confirmation → amber clock      "Waiting for [mentor] to confirm"
     completed             → grey tick        "Completed"
     no_show               → grey slash       "Didn't take place"
     cancelled             → grey cross       "Cancelled"

4. EVERY COUNTER DERIVES FROM THE SAME FUNCTION. "Upcoming", "Completed" and
   any other session tally must be computed from deriveSessionState, so a
   counter and a badge can never disagree again.

5. TIMEZONE — still missing everywhere. Every session time must render in the
   founder's timezone with the zone named: "Thu 13 Aug · 1:30 PM your time
   (GMT+3)". Store in UTC, detect from the browser, allow an override in
   profile settings. StartPad serves GMT+1 to GMT+4; a bare "1:30 PM" is a
   missed call waiting to happen.

6. SECTIONING. Upcoming section: live, confirmed, awaiting_confirmation, sorted
   soonest first. Past section: completed, no_show, cancelled, sorted most
   recent first, collapsed behind "Show past sessions (3)". Hide either section
   entirely when empty.

Report which of the three existing sessions ends up in which state, on all
three pages.
```

## PROMPT B — Remove Every Piece of Placeholder Content

```text
PAGE: Collaboration Hub (Projects and Team Chat), Dashboard, AI Tools survey
history.

THE PROBLEM
Five separate places ship visible fake or test content to real users:

1. COLLABORATION HUB → TEAM CHAT is labelled "Local demo", shows one seeded
   message ("Welcome! Use this space to coordinate with your collaborators."),
   offers a working-looking message input, and says underneath: "Live realtime
   chat per project coming next." A founder can type into a box that goes
   nowhere.

2. DASHBOARD → Collaboration hub lists a workspace called "Master".

3. COLLABORATION HUB → Projects previously showed "projx" and "dasd" with
   description "dsad" — confirm these are gone.

4. AI TOOLS → Create Your Survey → Generation history shows four runs with
   topic "ds" and audience "wdsdsas", plus one called "Ghh".

5. AI TOOLS → the current survey form is prefilled with topic "ds" and target
   audience "wdsdsas".

THE FIX

1. REMOVE THE TEAM CHAT TAB ENTIRELY until realtime chat actually works. A
   feature that visibly does not work costs far more trust than a feature that
   is not there yet. If you want to signal it is coming, a single line on the
   Projects tab — "Team chat is coming to projects soon" — does the job without
   an input box that discards what people type.

2. PURGE all seeded rows: "Master", "projx", "dasd", the "ds"/"Ghh" survey
   history entries. Clear the prefilled survey form fields.

3. ADD A SEED-DATA GUARD that fails the production build:
   - Tag every seeded record with a `is_seed` flag or a known seed namespace.
   - A build/deploy check that refuses to ship if seed records exist in the
     production database.
   - This is the third round in which placeholder data has reached a live
     screen. A guard is cheaper than remembering.

4. REAL EMPTY STATES wherever the seed data was hiding one. Follow the pattern
   already used on Journey history, which is the best empty state in the
   product — icon, plain heading, one line explaining what will appear, one
   clear action:
     Projects:        "No projects yet" / "Start one and find people to build it
                      with — or join a project that needs your skills."
     Survey history:  "No surveys yet" / "Generate your first set of questions
                      above and it will be saved here."

5. While in the Collaboration Hub: one member of "Founders on your mission" in
   Community renders as "H7s2btr5r" — a raw username among real names and
   photos. Require a display name at sign-up, or fall back to initials plus
   country rather than showing the handle.
```

**Why this order.** A is a shared-component refactor and should land before anything else touches session UI. B is deletion and empty states — fast, safe, ship alongside.

---
---

# Set 5 — Landing Page

One prompt. There are currently two different landing pages in circulation that contradict each other, plus a logo wall that is a genuine legal risk.

## PROMPT A — Merge the Two Landing Pages and Fix the Claims

```text
PAGE: Landing page (/).

THE PROBLEM — TWO VERSIONS EXIST AND THEY DISAGREE

Version A:
  Headline: "Turn your idea into a launched startup in 15 guided missions"
  "15 missions. 5 PHASES. One launched startup."
  Stats: 10+ business models done / 3+ MVPs shipped / 3+ startups launched
  A third-party logo wall, 9 feature cards, testimonials
  Closing CTA: "Join thousands of entrepreneurs..."

Version B:
  Headline: "We grew up watching brilliant ideas die in group chats"
  "15 missions. 8 PHASES. One launched startup." — then lists TWELVE groups,
  with "Validation" appearing four times and "Development" twice
  Stats: 15 / 24-7 / 100% / 104
  An interactive "Describe your idea in one sentence" box
  Mission and vision blocks, "Built different", "Why MENA? Why now?"

Meanwhile the Journey page lists EIGHT phases: Discovery, Analysis, Ideation,
Validation, Business Model, Development, Strategy, Launch.

THE FIX

1. PICK ONE PAGE. Keep Version B's headline — "We grew up watching brilliant
   ideas die in group chats" is the strongest sentence you have. Keep Version
   B's interactive idea box; it is the best element on either page. Carry over
   Version A's testimonials.

2. ONE CANONICAL PHASE LIST, matching the Journey page exactly: Discovery,
   Analysis, Ideation, Validation, Business Model, Development, Strategy,
   Launch — eight phases, each appearing ONCE, with the missions grouped under
   them summing to 15. Fix the roadmap that currently repeats Validation four
   times. Then use that same list on the landing page, the Journey page and
   anywhere else phases appear, from a single shared config.

3. REMOVE THE LOGO WALL. The section headed "BUILT ON THE GROWTH & STARTUP
   FRAMEWORKS BEHIND" showing Reforge, Slack, HubSpot, Google and Amazon must
   go. A logo wall reads as customers, partners or investors regardless of the
   caption, and using those trademarks in a way that implies affiliation is
   actionable — all four enforce actively. It also fails with your audience:
   anyone who recognises Reforge knows you are not affiliated with it.
   Replace with a plain text line naming the actual methodologies:
   "Built on jobs-to-be-done, lean validation and growth-loop frameworks."
   True, defensible, and free.

4. FIX EVERY CONTRADICTORY OR UNSUPPORTABLE NUMBER:
     - "Join thousands of entrepreneurs" in the closing CTA, on a page whose
       hero says "Founders 104+". DELETE. Replace with "Join the 104 founders
       already building."
     - "Join founders from 50+ countries" — 104 founders across 50+ countries
       averages two per country. Use the real number of countries.
     - "methodologies used by 2,500+ successful startups and validated by
       industry experts" — unsourced. Cut it or cite it.
     - The traction footnote reads "Includes the founding cohort baseline" —
       you have written a disclaimer explaining that your traction numbers
       include numbers that are not traction. Show the real figures without a
       baseline, or remove the section. "3 MVPs shipped" is honest and fine.
   104 real founders is a good number for an early product and it is the one
   you can prove. Every unsupportable claim beside it makes the provable one
   look invented too.

5. PRICING. "100% Free to Start" implies a paid tier and there is no pricing
   page anywhere. Either change it to "100% free" and mean it, or build
   /pricing and link it from the nav and footer.

6. CUT THE FEATURE CARDS from nine to five. Promote "Apply to programs &
   investors" and "Early traction engine" — the two most compelling and
   currently in positions seven and nine. Drop "Proven framework" and "Solid
   build toolkit", which say the least.

7. TESTIMONIALS: change the heading from "Loved by founders" to "What early
   founders say" — more honest at this stage and, for this audience, more
   persuasive. Add each founder's progress: "completed 6 of 15 missions". That
   is proof rather than praise.

8. Add the legal footer row from Set 2·A: Privacy · Terms · Cookies · FAQ.

KEEP: the "MADE IN EGYPT · BUILT FOR MENA" eyebrow, the two-tone headline, the
interactive idea box, "Built in Cairo. Designed for the entire Arab world.",
the mission roadmap concept, and the current social set (Instagram, TikTok, X,
LinkedIn).
```

**Why this order.** Second only to the legal pages. The trademark exposure and the self-contradiction are both live on your highest-traffic page.

---
---

# Set 6 — Mission Runner & Gamification

One prompt. The mission runner is the best thing in the product; these are consistency fixes, not a rebuild.

## PROMPT A — Make Progress, Level and Points Agree

```text
PAGE: Mission runner (/journey/mission/1), My Startup Journey, Dashboard.

CONTEXT
The mission runner's AI evaluation is genuinely strong — per-criterion rubric
with weighted bands, the actual evidence quotes used, a named weakest criterion,
and a concrete list of blockers with inline Fix buttons. Do not change any of
that. These are consistency problems around it.

THE PROBLEMS

1. THREE PROGRESS INDICATORS DISAGREE ON ONE SCREEN.
   The mission page simultaneously shows:
     "5 of 5 tasks completed"
     "Progress saved 100%"
     "5 of 5 answered — almost done, this is where the good ideas get sharp"
   directly above:
     "Attempt 1 · Score 20%"
     "Needs Improvement (70% required)"
     "6 things to fix before you can submit"
   The founder is told they are finished and blocked at the same time.

2. LEVEL DISAGREES ACROSS PAGES. The mission page shows "Level 2, 100 XP
   earned, 20 XP to next level". My Startup Journey shows "Level 1, Beginner,
   0 achievements". Both are live at the same moment.

3. 175 POINTS WITH 0 OF 15 MISSIONS COMPLETE, shown on three pages.

4. MISSION LENGTH STATED TWO WAYS. The mission header says "2-3 hours"; the
   AI Tools guidance panel says "1-2 hours" for the same Mission 1.

5. STREAK COUNTS THE WRONG THING. Journey shows "Mission Streak: 1 day" and
   "Longest Streak: 4" with 0 of 15 missions completed. A four-day streak with
   zero completed work means the streak counts logins.

THE FIX

1. SEPARATE COMPLETENESS FROM QUALITY. They are different axes and must never
   be shown as one. Replace the three competing indicators with one status line:
     "5 of 5 answered · Not yet passing — 20% of the 70% needed"
   Completeness answers "have I filled everything in". Quality answers "is it
   good enough". Never let a completeness signal imply the mission is done.

2. ONE SOURCE OF TRUTH for level, XP, points and achievements — a single
   selector that every page reads. Mission page, Journey and Dashboard must
   never compute these independently.

3. MAKE POINTS EXPLAINABLE. Total points becomes tappable, opening a breakdown
   of where each point came from. If 175 points exist with no completed mission,
   the breakdown must say why. An unexplained score in a gamified product is
   worth less than no score.

4. ONE MISSION CONFIG. Duration, difficulty, points, phase and objectives all
   read from a single per-mission record. No page hardcodes any of them.

5. STREAKS COUNT WORK, NOT VISITS. A streak day requires a meaningful action —
   a submitted answer, a completed task, a mission attempt. Opening the tab is
   not progress, and a streak you can maintain by loading a page teaches
   nothing. Recompute "Longest streak" under the new rule.

6. STAGE THE FAILURE FEEDBACK. A first-time founder currently sees a red 20%,
   "Needs Improvement", a red rationale block, a red six-item blocker list, and
   five criteria bars mostly at 0% — all at once. The feedback is correct, but
   the shape is a rejection letter.
   Lead with ONE next action:
     "Start with Question 1 — replace 'sda' with the actual industry you care
      about. That alone moves Specificity from 20% to passing."
   Then "See the full assessment →" expands everything currently shown. Keep
   the rigour; stage the delivery.

7. ADD A WORKED EXAMPLE. For each question, let the founder open "What does a
   strong answer look like?" showing an anonymised example that scores 70%+ on
   that criterion. Founders cannot hit a standard they have never seen.

8. SHOW WHAT CHANGED BETWEEN ATTEMPTS. On attempt 2 and later, show the
   per-criterion delta from the previous attempt so the founder can see whether
   their edits worked.
```

**Why this order.** After the session and placeholder work. It touches shared gamification state, so it is worth doing as one focused pass rather than piecemeal.

---
---

# Set 7 — AI Tools

One prompt. Strong tools, confusing shell.

## PROMPT A — Bring AI Tools Into the Design System

```text
PAGE: AI Tools (/ai-tools) — all six tabs.

THE PROBLEMS

1. THE PURPLE BREAKS THE DESIGN SYSTEM. A full-bleed green-to-purple gradient
   banner sits at the top, and the primary buttons inside are purple —
   "Generate Template", "Generate Questions", "Read Guide", "Generate AI
   Questions". Nothing else in StartPad is purple. It reads as a different
   product bolted on.

2. "WHAT THIS TOOL WILL USE — 2 OF 4 READY" IS NEVER EXPLAINED. The counter
   changes per tab (2 of 4, 2 of 3, 1 of 3), sits behind a collapsed accordion,
   and nothing tells the founder what is missing or how to fix it. It is the
   first thing on the screen and it reads as a warning.

3. TWO NAVIGATION SYSTEMS FOR FIVE TOOLS. A six-item tab bar (Start Here ·
   AI Mentor · Ask AI Coach · Create Your Survey · Publish & Collect · My Next
   Steps) sits above a grid of five tool cards whose "Try Now" buttons go to
   those same tabs.

4. "MY NEXT STEPS" IS GENERIC. "Complete the required fields · Review your
   responses · Get feedback from peers · Submit when ready", with Pro Tips
   reading "Take your time" and "Be specific in your responses" — two tabs away
   from an AI Mentor giving genuinely specific coaching.

THE FIX

1. REMOVE THE PURPLE GRADIENT. Use the same page header pattern as every other
   app page: navy H1, muted subtitle, white background. If AI features need a
   visual signature, put it on the "AI-Powered" badge alone — not a full-bleed
   gradient and a second primary colour. All primary buttons become green
   #047857.

2. EXPLAIN OR REMOVE THE READINESS COUNTER. If it stays, expand it by default
   and name each gap with a fix action:
     "Your industry — not set yet.  Add it →"
     "Your target customer — not set yet.  Add it →"
     "Mission 1 answers — ready ✓"
   If you cannot make each line actionable, remove the counter entirely and let
   the tools degrade quietly.

3. ONE NAVIGATION. Keep the five tool cards as the entry point and drop the tab
   bar, OR keep the tabs and make "Start Here" a genuine overview — what the
   tools do together, which to use when — rather than a duplicate menu. Do not
   ship both.

4. MAKE "MY NEXT STEPS" SPECIFIC OR CUT IT. Generate it from the founder's
   actual state: current mission, lowest-scoring rubric criterion, unanswered
   questions, unattached evidence. "Your Specificity score is 20% — the fastest
   fix is Question 1" is worth reading. "Take your time" is not, and sitting
   beside genuinely specific coaching it devalues both.

5. PURGE THE TEST DATA — see Set 4·B. Generation history contains "ds",
   "wdsdsas" and "Ghh"; the survey form is prefilled with the same.

6. KEEP AND PROMOTE: the survey generator is the strongest tool here. Eight
   questions, each with a type chip and a "Why this question" rationale, with
   real export paths to Typeform, Google Forms, CSV, JSON and Excel. The
   AI Mentor's "Where you left off" recap with a dated summary is also
   excellent — surface that on the Dashboard too.

7. CONNECT THE TOOLS TO THE MISSION. The survey generator produces exactly what
   Mission 1 needs as evidence. Add "Attach to Mission 1" on generated output so
   it flows straight into the mission submission instead of the founder
   copying it across.
```

**Why this order.** Self-contained and visual. Run it after the data bugs — it changes a lot of surface area and is easier to review when nothing underneath is moving.

---
---

# Set 8 — Resources & Knowledge Hub

One prompt covering both content libraries.

## PROMPT A — Make the Libraries Credible and Connected

```text
PAGE: Resource Library (/resources) and Knowledge Hub (/knowledge-hub).

THE PROBLEMS

1. HALF THE "RESOURCES" ARE SEARCH LINKS. The page promises "32 curated
   resources", but many items — Customer Discovery Guide, Customer Interview
   Guide, Growth Hacking for Startups, Financial Projections Spreadsheet, UX
   Research Methods, Startup Legal Essentials and others — carry a "Search
   Online" button instead of "Open Resource". A Google search is not a curated
   resource.

2. UNATTRIBUTED RATINGS. All 32 items carry a star rating between 4.2 and 4.9,
   with no review count, no reviewer, and no way for a founder to rate
   anything.

3. DUPLICATES. "Pitch Deck Template" appears three times (Sequoia, Fundraising,
   Growth). "Startup Legal Checklist" twice. "Lean Startup Methodology" twice.
   "Financial Planning" and "Financial Projections" spreadsheets overlap.

4. NEITHER LIBRARY CONNECTS TO THE MISSIONS. "Customer Discovery Guide" and
   "Problem-Solution Canvas Template" are exactly what Mission 1 needs. "A
   Practical Guide to Validating Product-Market Fit" in the Knowledge Hub is
   exactly what the Validation phase needs. Nothing links in either direction.

5. TWO KNOWLEDGE HUB CARDS HAVE NO COVER IMAGE — "Talk: Building in Hard
   Markets" and "Your First 100 Customers" render as blank white blocks, while
   "Welcome to the StartPad Knowledge Hub" gets a plain icon.

6. NO ARABIC CONTENT AND NO LANGUAGE FILTER in either library.

THE FIX

1. EITHER HOST IT OR DROP IT. Every resource must open something real — a
   hosted template, a PDF, a direct link to the actual artefact. Remove
   "Search Online" entirely. If an item has no real destination, delete it and
   reduce the count honestly: "18 curated resources" that all work beats 32
   where half are searches. Also ensure "Download Complete Toolkit" never
   exports rows that are only search queries.

2. RATINGS: let founders rate resources and show the count ("4.6 · 23 ratings"),
   or remove the stars. Unattributed ratings read as decoration and undermine
   the ones that might be real.

3. DE-DUPLICATE. One pitch deck template, one legal checklist, one lean startup
   guide, one financial spreadsheet. If two genuinely differ, make the
   difference explicit in the title.

4. TAG EVERYTHING TO A MISSION OR PHASE. Then:
     - Show a "Used in Mission 1" / "Relevant to Validation" chip on each card.
     - Add a mission filter alongside the existing category and type filters.
     - Inside each mission, surface the two or three matching resources and
       articles in a "Recommended for this mission" block.
   This is what turns two content libraries into part of the product rather
   than two things sitting beside it.

5. FALLBACK COVERS. Generate a cover for any item without artwork — category
   colour, title text, category icon. No card should ever render blank.

6. LANGUAGE FILTER in both libraries, and a translation path for the
   highest-traffic pieces. Thirteen Knowledge Hub items and 32 resources, all
   English, on a platform built for Arabic-speaking founders.

7. CAPTURE THE READER. A visitor reads a nine-minute whitepaper and leaves with
   no relationship. Add an email capture at the end of each article and ONE
   contextual CTA tied to the topic — a funding article ends with the Founder
   Readiness Assessment, not a generic "Get started".
```

**Why this order.** Independent of everything else. Point 4 is the high-value item — the cross-linking is worth more than the cleanup.

---
---

# Set 9 — Sign In / Sign Up

One prompt. The form is well-built; the policy around it is weak.

## PROMPT A — Password Policy and Auth Screen Polish

```text
PAGE: Sign up and Sign in (/signup, /signin).

CONTEXT
The form itself is good — Google and Apple above the fold, a clear divider, a
proper country-code selector defaulting to EG +20, a password reveal toggle,
and "Forgot your password?" on sign-in. These are policy and copy fixes.

THE FIXES

1. PASSWORD MINIMUM IS SIX CHARACTERS. The field reads "Create a password
   (min 6 chars)". That is below every current guideline — NIST recommends a
   minimum of eight with no forced composition rules. This product will hold
   business plans, financial projections and uploaded documents.
     - Raise the minimum to 8.
     - Add a strength meter that responds as the user types.
     - Check against a breached-password list (Have I Been Pwned k-anonymity
       API) and warn on a match.
     - Do NOT add forced composition rules (one uppercase, one symbol) — they
       reduce real-world strength. Length and a breach check are what matter.

2. THE PASSWORD HINT APPEARS TWICE, VERBATIM. "Create a password (min 6 chars)"
   is both the placeholder AND the helper text below the field. Keep the rule
   in the helper text only; leave the placeholder empty.

3. PHONE NUMBER IS REQUIRED AND UNEXPLAINED. Five fields plus a phone number is
   heavy for a free product, and phone is the field this audience is most
   reluctant to give.
     - Make it optional at sign-up.
     - Collect it later at mentor booking, where a reason exists and the founder
       can see it.
     - If it must stay required, add one line under the field explaining why.

4. THE SIGN IN TAB STILL SAYS "JOIN STARTPAD". Both tabs share the heading
   "Join StartPad" and the subtitle "Start your entrepreneurial journey" — even
   when signing in to an existing account.
     Sign Up: "Join StartPad" / "Start your entrepreneurial journey"
     Sign In: "Welcome back"  / "Pick up where you left off"

5. ADD THE CONSENT CHECKBOX from Set 2·A above "Create Account", and the
   consent line under the Google and Apple buttons.

6. CONFIRM PASSWORD: with a reveal toggle already present, the confirm field is
   redundant friction. Consider removing it and relying on the toggle plus a
   working password reset.

7. ERROR HANDLING: show validation inline per field on blur, never only on
   submit. On sign-in failure use one generic message ("Email or password is
   incorrect") — never reveal whether an email is registered.

8. Add a "next" parameter so a user redirected here from a private route
   returns to where they were going after signing in — see Set 1·A.
```

**Why this order.** After Set 2·A, so the consent checkbox has real documents to link to.

---
---

# Set 10 — Dashboard

One prompt. Right primary action, wrong density.

## PROMPT A — Fix the Progress Bar and Cut the Emptiness

```text
PAGE: Dashboard (/dashboard).

THE PROBLEMS

1. THE PROGRESS BAR IS 100% FILLED AT "0 OF 15 COMPLETED". The Current mission
   card shows a completely solid bar directly above text reading "0 of 15
   completed". Either the width is hardcoded or it is being fed something other
   than the completion ratio. The first thing a new founder sees is a finished
   journey they have not started.

2. ROUGHLY 60% OF THE PAGE ENUMERATES ABSENCES. Three separate blocks say the
   founder has no sessions — "Session reminders: Nothing scheduled this week",
   "Upcoming sessions: No sessions booked yet", and the "Upcoming 0" stat card.
   Plus two empty analytics panels ("Not enough activity yet in this range"),
   plus an empty KPI panel.

3. ANALYTICS ARE SCOPED "ON THIS DEVICE". "Tools opened per day on this device"
   is a local-storage metric that dies when the founder moves from laptop to
   phone — which this audience does constantly. The number is never
   trustworthy.

4. "INVESTED (USD) 0" is shown to a founder who has not finished Mission 1.

THE FIX

1. PROGRESS BAR: width from completed / total. At zero, render an empty track
   with a visible rail — never a filled bar. Audit every other progress bar in
   the app for the same defect.

2. COLLAPSE THE THREE SESSION BLOCKS INTO ONE. A single "Mentoring" card
   showing the next session, or one empty state with a "Book a mentor" action.
   Not three.

3. HIDE EMPTY PANELS. Any analytics or KPI panel with no data collapses to a
   single compact row — "Tool usage · not started yet" — expandable if the
   founder wants it. A dashboard's job is to show what to do next, not to list
   what has not happened.

4. FIX OR REMOVE DEVICE-SCOPED ANALYTICS. Move tool-usage events server-side,
   keyed to the account. If that is not feasible now, remove the panel rather
   than showing a number you have to disclaim.

5. STAGE-GATE THE METRICS. Hide any metric that cannot be non-zero at the
   founder's current stage — "Invested (USD)" at Mission 1 sets an expectation
   the product does not yet meet. Reveal metrics as the journey unlocks them.

6. SURFACE THE NEXT STREAK REWARD. The Journey page has a genuinely good
   mechanic — unlock mission templates at 3 days, expert tips at 5, bonus
   resources at 7, a mentor discount at 10 — and the Dashboard does not mention
   it. "2 days to unlock expert tips" is a far better reason to return than a
   streak number.

7. SURFACE THE AI MENTOR RECAP. The AI Mentor has a "Where you left off" panel
   with a dated summary of exactly what the founder was doing. That belongs on
   the Dashboard, next to "Continue mission".

8. PURGE the "Master" workspace — see Set 4·B.

KEEP: "Current mission · Pick up right where you left off" with a single
"Continue mission" button is exactly the right primary action. The 7/30/90/
All-time range filter is a mature touch. Do not lose either.
```

**Why this order.** Last of the substantive sets. It depends on Set 4·A (sessions) and Set 6·A (points and progress) already being correct, or you will fix the same numbers twice.

---

## Suggested sequence

| Order | What | Why |
|---|---|---|
| 1 | Set 2·A | Legal exposure — collecting phone numbers and AI transcripts with no policy |
| 2 | Set 5·A | Trademark risk and a page contradicting itself |
| 3 | Set 4·A | One bug in three places — fix centrally |
| 4 | Set 1·A | Your explicit ask, now confirmed broken |
| 5 | Set 4·B | Five instances of visible fake content |
| 6 | Set 2·B | FAQ and Help Centre |
| 7 | Set 3·A | Profile fields — after the privacy policy covers them |
| 8 | Set 9·A | Auth screen polish + consent checkbox |
| 9 | Set 6·A | Mission runner and gamification consistency |
| 10 | Set 7·A | AI Tools into the design system |
| 11 | Set 8·A | Library credibility and mission cross-linking |
| 12 | Set 10·A | Dashboard density |
| 13 | R2 Set 5·A, 7·A, 7·B | Still outstanding: app nav diet, Arabic audit, mobile audit |

Items 1–5 are all same-day work and could ship in one session.
