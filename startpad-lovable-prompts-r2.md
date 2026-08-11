# StartPad — Lovable Prompts (Round 2)

12 prompts targeting defects found in the five live screens reviewed on 11 Aug 2026.
**R01 is the same-day bug sweep — run it first.**
Paste one prompt per message; do not concatenate them.

Round 1 prompts (strategy, new pages): `startpad-lovable-prompts.md`.
Full round 2 review: `startpad-screen-review-r2.html`.

---

## R01 — Bug sweep — ship today

```text
Fix these six defects in StartPad. They are all visible in production right now.

1. MENTORING DATES: sessions dated in the past are displayed under "Your Upcoming Sessions" with an "upcoming" badge. Today is 11 Aug 2026 and sessions from 27 May and 9 June are shown as upcoming. Derive session status from the timestamp at render time, never from a stored status field. Split the page into "Upcoming" and "Past" sections, sort ascending within each, and hide the Past section when empty.

2. BLANK BUTTON: in the final CTA band on the landing page ("Your startup starts here") there is a white button with no label, next to "Go to dashboard". Find it and either give it its correct label or remove it.

3. TEST DATA: delete the seeded projects in the Collaboration Hub — "projx", "dasd" with description "dsad". Add a real empty state for when no projects exist.

4. PLURALISATION: the Community stats show "1 Total Posts". Use Intl.PluralRules for all counts across the app. Note Arabic has six plural forms, so never suffix "s" directly.

5. DELETE BUTTON: the project Delete button is a full-width saturated red primary button — the loudest element on the page. Move it into an overflow (⋯) menu in the card header as tertiary text, and add a confirm dialog naming the consequence.

6. LOGGED-IN HOMEPAGE: authenticated users currently land on the full marketing homepage. Redirect them to /dashboard.

Report what you changed for each.
```

## R02 — Navigation & chrome diet

```text
The logged-in shell has roughly 180px of fixed chrome before any content — an 88px nav plus a 90px profile banner — on every page. Fix it.

NAVIGATION
- Reduce to 5 top-level items: Dashboard, Journey, Community, Mentors, Resources. Everything else goes into the avatar menu.
- Move "Sign out" OUT of the top bar and into the avatar dropdown. It is currently a permanent top-level item sitting next to the user's own name.
- The "More" dropdown must not show a permanent active state. Active state belongs on the current page only — if the current page lives inside More, highlight it in the open dropdown.
- "Loadout" is unclear as a label. Either rename it to what it contains, or keep it and add a one-line description in the dropdown and mobile menu.
- One language switcher only. There are currently two (nav "ENGLISH", footer "English") with inconsistent casing.
- On mobile: a bottom tab bar with those 5 items, and everything else in a sheet behind the avatar.

PROFILE BANNER
- Never render it on the public landing page.
- Put the three missing fields (Country, Industry, Startup stage) as inline dropdowns INSIDE the banner. Three taps and it's done and gone permanently — do not send the user to a separate checklist for 30 seconds of work.
- Dismissal persists for the session at minimum; "Remind me later" persists for 7 days.
- Collapse to a single slim line once above 80%.
```

## R03 — Fix Arabic post rendering

```text
Arabic posts in the Community feed render inside a left-to-right container. The Arabic body text is right-aligned but the card around it is not — the category chip, author row, timestamp, hashtags, and view/like/comment icons all stay LTR. The hashtag chip renders the "#" on the wrong side with a stranded full stop.

FIX
- Detect the dominant script of each post at render and set dir="rtl" or dir="ltr" on the ENTIRE post card, not just the text node.
- All internal spacing must use logical CSS properties (margin-inline-start, padding-inline-end, text-align: start) so the card mirrors correctly as a unit.
- Hashtags in Arabic posts render with "#" leading in reading order — the RTL container handles this once direction is set on the right element.
- Wrap mixed-direction fragments (an English product name inside an Arabic sentence) in <bdi> so they don't scramble the surrounding line.
- Arabic body text needs its own type treatment: roughly 1.1x the font size and 1.2x the line-height of the Latin equivalent, using an Arabic-native family (IBM Plex Sans Arabic, Noto Sans Arabic, or Cairo).
- Keep the existing "Translate to English" toggle — it's excellent — and add the reverse for English posts when the viewer's locale is Arabic.

Test with the existing post "الأغذيه الصحيه من الأرض للفضاء" and with a post mixing Arabic and English.
```

## R04 — Landing page restructure

```text
Restructure the StartPad landing page. The copy is strong but buried and the product is invisible.

MOVE THE BEST LINE UP
"We grew up watching brilliant ideas die in group chats" is currently ~60% down the page in "Why we built this". It is the most persuasive sentence on the site. Build the hero around it. The current headline ("StartPad turns ideas into startups") could describe any product — demote or replace it.

SHOW THE PRODUCT
There is currently not a single screenshot, mission map, or interactive element on the entire page. Add:
- An interactive element in the hero: the visitor types their idea in one sentence and gets a live AI score with one strength, one risk, and a suggested first mission. Works with no account.
- The 15 missions as a visual path, with names, outcomes and time estimates — replacing the "Our mission / Our vision" block, which moves to /about.

FIX THE NUMBERS
- "15+" contradicts "15 step-by-step missions" and "Fifteen real missions" elsewhere on the same page. Use 15 everywhere.
- The stat row is 15+ / 24/7 / 100% / MENA — "MENA" is not a statistic. Replace with a real figure (countries, founders, missions completed this month).
- Add source lines to the 400M+ / 70% / $3.5B market stats.

OTHER
- Compress the 3-line hero subhead to one line.
- "100% FREE TO START" implies a paid tier with no pricing page. Either commit to free or ship /pricing and link it in nav and footer.
- Footer social: lead with Instagram and TikTok, add a WhatsApp channel, keep LinkedIn for mentors. Facebook is close to irrelevant for this audience.

Keep: the "MADE IN EGYPT · BUILT FOR MENA" eyebrow, the two-tone headline, "Built in Cairo. Designed for the entire Arab world.", and the green identity. Those all work.
```

## R05 — Rebuild Mentoring

```text
The Mentoring page shows bookings and nothing else — there is no way to find or book a mentor from it. Rebuild it.

PRIMARY ACTION IS FINDING A MENTOR
- Page leads with "Find a mentor" and a browsable directory. Existing bookings are secondary, below it.
- Directory filters: country, language (Arabic / English / both), expertise, startup stage, available this week.
- Mentor cards: photo, name, role, languages, expertise chips, typical response time, founders helped, next available slot.

SESSION CARDS — every card must carry:
- Date and time IN THE FOUNDER'S TIMEZONE, with the timezone named: "1:30 PM your time (GMT+3)". Currently no timezone is shown at all, across a region spanning GMT+1 to GMT+4.
- Session length, language, and mentor photo.
- One clear action: Join (when live), Add to calendar, Reschedule, Cancel.
- Whole card is clickable to a detail view.

STATUS
Replace the current ambiguous "upcoming" / "pending" badges — both green, both ticked, neither explained — with a real state machine: requested → confirmed → completed → cancelled → no-show. Each state gets a distinct colour AND shape, plus an action when one is needed ("Waiting for Sarah to confirm" + a nudge button).

MENTOR ROSTER
Current mentors are Emily Rodriguez and Sarah Johnson. The homepage promises mentors who understand the MENA market. Prioritise showing MENA-based mentors and mentors who speak Arabic — surface language and country prominently on every card.

PREP AND FOLLOW-UP
- 24h before: auto-generate a one-page brief from the founder's mission progress, send to the mentor, and show the founder 3 suggested questions.
- After: rate the call, capture 3 action items, push them into the founder's current mission as tasks.
```

## R06 — Rebuild the Collaboration Hub card

```text
The Collaboration Hub has two project cards with completely different anatomy — one has a single giant "Join" button, the other has five small buttons plus a full-width red Delete. Unify them.

ONE CARD COMPONENT
Constant elements always in the same position: project name, status badge, description, member count, activity date, and "Looking for" chips. Only the action area changes by viewer role.
- Not a member → "Join" (primary)
- Member → "Open project"
- Owner → "Open project" + a "Your project" badge + an overflow (⋯) menu containing Settings and Delete

REPLACE THE FIVE BUTTONS
Team, Files, Whiteboard, Video calls, Activity should be TABS INSIDE the project, not buttons on the card. If any of these aren't built yet, remove the entry entirely — a dead button costs more trust than a missing feature.

MISSING ESSENTIALS
- "Looking for" chips on every project: designer, developer, marketer, co-founder. This is the entire purpose of a collaboration hub and it's currently absent.
- Filters on those chips, plus country and startup stage. Plus search.
- Label the date and prefer relative time: "Active 3 days ago" not a bare "Aug 5, 2026".
- "No description." becomes an inline prompt for the owner ("Add a description so people know what you're building") and is hidden entirely from everyone else.

Equal card heights in the grid regardless of content length.
```

## R07 — Scope Community to missions

```text
The Community feed has no connection to what founders are actually doing. Someone on Mission 3 opens it and sees an unrelated post from 19 days ago. Fix the structure.

FEED SCOPING
- Default tab: "My mission" — posts from founders currently on the same mission as the viewer.
- Other tabs: "My circle" (their cohort) and "All".
- Every post shows the author's current mission as a chip. This is what makes a thin early community feel alive: it turns "1 post" into "3 founders are on Mission 3 right now".

REMOVE THE EMPTINESS SIGNALS
- Delete the four stat cards (1 Total Posts / 1 Discussions / 0 Questions / 0 Answered). Four large cards whose only message is that nobody is here.
- Hide "Top Contributors" until there are at least 10 contributors.
- Hide per-post view/like/comment counts below a threshold (say 10 views) — "4 views, 0 comments" discourages the next person from posting.

COMPOSER
- Drop the generic centred "New Post" button. Keep the three intent-led Quick Actions (Ask a Question / Share an Idea / Showcase Project) and make them the primary way to post.
- Each opens a short structured form with real fields, never a blank box. Category is set by the intent automatically — currently an idea pitch is filed under "Help & Support" because the user had to guess.

LAYOUT
When the feed has fewer than 3 posts, drop the right sidebar below the content and let the feed run full width. Currently one post leaves two thirds of the column empty while the sidebar runs past it.

SEEDING
Add mission-linked weekly prompts posted automatically ("Everyone on Mission 3: what did your first customer interview teach you?") so the feed is never empty.
```

## R08 — Colour hierarchy pass

```text
One green is doing eleven jobs across StartPad — primary buttons, active nav, links, stat figures, tag chips, status badges, icons, progress fills and section eyebrows are all the same saturated green. When everything is emphasised nothing leads, which is why a red Delete button currently wins every screen it's on.

ESTABLISH A HIERARCHY
- Full-strength green: exactly ONE primary action per screen. Nothing else.
- Secondary actions: outlined, green text on transparent.
- Tertiary actions: plain text, no container.
- Tag chips, eyebrows and metadata: neutral grey, not green.
- Stat figures: ink colour, not green. Let the number carry the weight through size and a monospace tabular face.
- Semantic colours (success / warning / danger) are a separate set from the brand green and are used ONLY for state, never for emphasis.

DESTRUCTIVE ACTIONS
Never a filled primary button. Text or outline in danger colour, in an overflow menu, with a confirm dialog naming the consequence.

Audit every screen after the change: there should be exactly one obvious "what do I do here" target per page. Also verify 4.5:1 contrast on white text over the green — check the actual value, it's a common failure at this saturation.
```

## R09 — No page ends in emptiness

```text
Mentoring, Community and the Collaboration Hub all end abruptly with half a screen or more of blank space. Every page must end with a next step.

- Mentoring: after the session list, show "Mentors available this week" matched to the founder's stage and country.
- Community: after the feed, show mission-linked prompts to post, and founders on the same mission to follow.
- Collaboration Hub: after the project grid, show "Projects looking for your skills" based on the founder's profile.
- Journey history (empty): beneath the existing empty state, show a greyed-out sample recap card so the founder can see what they'll get — the answers, the AI score, the evidence. Demonstrating the value beats explaining the absence.

Also fix the floating chat bubble: it currently overlaps the Trending Tags card on Community. Give it a safe-area offset, shrink or hide it on scroll, and ensure it never collides with a mobile bottom tab bar.
```

## R10 — Information architecture cleanup

```text
StartPad currently has overlapping destinations that founders can't distinguish. Consolidate.

CURRENT OVERLAPS
- "Dashboard" vs "My Startup Journey" vs "Journey history" — three names, unclear boundaries.
- "My Sessions" in the Collaboration Hub vs sessions on the Mentoring page — two homes for scheduled things.
- "Team Chat" in the Collaboration Hub vs Community — two homes for conversation.

TARGET STRUCTURE
- Dashboard = what to do right now. One next-action card, then progress.
- Journey = the 15 missions, with "History" as a TAB inside it, not a separate destination.
- Mentors = find, book and manage every mentor session. The only home for scheduled 1:1s.
- Community = all public conversation. Project team chat stays inside its project.
- Projects = the Collaboration Hub, with Team / Files / Chat as tabs inside each project.

VOCABULARY
Pick one word per concept and use it in the nav label, page title, empty state and buttons. Currently "recap" and "submissions" describe the same object in two consecutive lines on Journey history. Build a short glossary and enforce it across all copy.
```

## R11 — Verify Arabic UI end to end

```text
StartPad has a language switcher labelled ENGLISH, and per-post content translation in Community — but I need the full interface verified in Arabic.

Switch the app to Arabic and check every screen, then fix what breaks:
- Does the entire interface translate, or only some strings? List anything still in English.
- Does dir="rtl" apply to the whole document — nav, banner, cards, forms, dropdowns, modals, toasts?
- Are directional icons mirrored (arrows, chevrons, progress fills, the mission path)? Logos, clocks and phone numbers must NOT mirror.
- Is an Arabic-native font loaded (IBM Plex Sans Arabic / Noto Sans Arabic / Cairo) at its own scale — ~1.1x size and ~1.2x line-height versus Latin? Never rely on a Latin font's Arabic fallback.
- Are dates, numbers and currency formatted per locale via Intl?
- Do mixed-direction strings (an English startup name in an Arabic sentence) render correctly with <bdi>?
- Is the locale in the URL (/ar/*), persisted per user, with hreflang tags?
- Consolidate the two language switchers (nav "ENGLISH", footer "English") into one.

Report every screen that breaks. Given this audience, half-working RTL is worse than English-only.
```

## R12 — Mobile audit

```text
Every StartPad screen I've reviewed is desktop, but the audience is overwhelmingly on phones. Audit and fix the full app at 390px width.

- The logged-in shell currently has ~180px of fixed chrome (88px nav + 90px profile banner). On a phone that's close to half the viewport. Collapse the nav to a bottom tab bar with 5 items and make the banner a single slim dismissible line.
- Convert every centred modal to a bottom sheet, draggable to dismiss.
- The Collaboration Hub's 5-button grid and the Community 4-card stat row must reflow, not shrink.
- The Mentoring session cards must stack with time, timezone and the primary action all visible without horizontal scroll.
- Every tap target 44x44px minimum, with spacing between adjacent targets. The Delete button in particular must not sit adjacent to a common action.
- The floating chat bubble must not overlap the bottom tab bar or any primary action.
- No horizontal page scroll anywhere.
- Test the landing page: it's currently very long on desktop and will be enormous on mobile. Compress it and add a sticky bottom CTA.

Report each screen with a before/after and list what you changed.
```
