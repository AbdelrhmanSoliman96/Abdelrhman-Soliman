# Startpad — Lovable Prompts

24 copy-paste prompts to enhance, fix and extend startpad.me for a Gen Z (MENA) audience.
Run **P00 first** — it sets the design system every later prompt refers back to.
Paste one prompt per message; do not concatenate them.

Full review with reasoning, journey audit and page inventory: `startpad-ux-review.html`.

---

## P00 — Master context — run this first

```text
You are building Startpad — a gamified launchpad that guides Gen Z founders in the MENA region from idea to launch through 15 missions, with AI tools, mentors and a community.

Set up the foundations before building any page:

DESIGN SYSTEM
- Mobile-first. Every screen is designed for a 390px viewport first, then scaled up. Bottom sheets instead of centered modals on mobile. Bottom tab nav with max 5 items, thumb-reachable.
- Colors: one high-energy accent used sparingly on a quiet neutral ground. Separate semantic colors for success / warning / danger. Full dark mode via CSS custom properties on :root — dark mode is a first-class theme, not an afterthought.
- Type: a confident sans with strong weight contrast (700/800 headlines set tight, 400 body at 16-17px minimum on mobile). A monospace face for XP, timers, mission codes and progress numbers, with tabular numerals.
- Motion: only for mission completion, XP increments, and unlocks. 200-300ms, spring easing. Everything else instant. Fully disabled under prefers-reduced-motion.
- Accessibility: WCAG 2.2 AA. 4.5:1 text contrast, 44x44px minimum tap targets, visible focus rings, real labels on every input, keyboard-operable dialogs with focus trapping.
- Every list and async surface needs four designed states: empty, loading (skeletons shaped like the content), error (says what happened + how to retry), and offline.

VOICE
Direct, warm, peer-level. Never corporate, never imitation slang. Buttons say exactly what happens. Errors name the problem and the fix.

TECH
React + TypeScript + Tailwind + shadcn/ui. Supabase for auth and data. All colors and spacing as design tokens — no hardcoded hex values in components. Build the token file and the base component set (Button, Card, Sheet, Input, Badge, Progress, Skeleton, Toast) before any page.

Confirm the token file and base components, then stop. I'll send pages one at a time.
```

## P01 — Landing page rebuild

```text
Rebuild the Startpad landing page (/) to convert a 21-year-old founder arriving from Instagram or a friend's WhatsApp link.

ABOVE THE FOLD (mobile first)
- Headline: "Launch your startup in 15 missions." Subhead in one line, no paragraph.
- An INTERACTIVE element, not a static image: an input where a visitor types their startup idea in one sentence and gets a live AI validation score in ~3 seconds — score out of 100, one strength, one risk, one suggested first mission. It must work with NO account.
- Two-path CTA: "I have an idea" and "I don't have an idea yet" — these route to different first missions.
- Sticky bottom CTA bar on mobile that appears after the hero scrolls out.

BELOW THE FOLD, in this order
1. The 15 missions as a visual path — names, outcomes, time estimates. Make it scrollable horizontally on mobile and clickable to /missions.
2. Peer proof strip: real founder faces with age, city, what they're building, which mission they're on. Live counter of missions completed this week.
3. What you walk away with: the concrete artifacts (validated problem, landing page, pitch deck, first 10 users), shown as objects, not bullet points.
4. Mentors: faces, countries, languages they speak.
5. Pricing summary with a link to /pricing. State clearly what's free forever.
6. FAQ answering: is it free, is it in Arabic, do I need an idea, how long does it take, who owns my idea.

Language switcher (English / العربية) in the header, persisted. LCP under 2.5s on 3G — no heavy hero video, lazy-load everything below the fold.
```

## P02 — /try — no-account mission zero

```text
Create /try — a complete first mission that a visitor can finish WITHOUT creating an account. This is the most important conversion surface in the product.

FLOW (one question per screen, 4 steps, ~5 minutes total)
1. "What problem are you trying to solve?" — free text, with 3 example answers shown as tappable chips to reduce blank-page paralysis.
2. "Who has this problem?" — free text + quick-select chips (students, small business owners, parents, freelancers, gamers).
3. "How do they solve it today?" — free text.
4. AI generates a one-page "Idea Snapshot": sharpened problem statement, target segment, 3 riskiest assumptions, a validation score out of 100, and the 3 next missions to run.

RULES
- Progress saved to localStorage after every step. Refreshing must never lose input.
- Visible step indicator (1 of 4) and a working back button.
- Stream the AI output with a real status line ("reading your idea…", "checking assumptions…"), never a bare spinner.
- The account wall appears ONLY at the end, framed as "Save your Idea Snapshot" — with the snapshot visible and blurred-but-readable behind it. On signup, migrate the localStorage session into the new account so nothing is lost.
- Let them download the snapshot as an image and share it to WhatsApp / Instagram Stories without an account.

Works fully in Arabic RTL.
```

## P03 — Auth & account creation

```text
Rebuild signup and login for a MENA mobile audience.

METHOD ORDER (top to bottom)
1. Continue with Google
2. Continue with Apple
3. Continue with phone number — OTP via SMS, with country picker defaulting to the user's detected country (EG, SA, AE, JO, KW first in the list)
4. Email + password, collapsed under "More options"

RULES
- Signup asks for ONE identifier. No name, no country, no company, no "how did you hear about us" at this step.
- If an anonymous /try session exists in localStorage, migrate it into the new account immediately after auth and land the user on their saved Idea Snapshot — never on an empty dashboard.
- OTP input: 6 separate boxes, auto-advance, paste-from-SMS support, auto-submit on the last digit, a visible countdown before "Resend code" becomes tappable.
- Every error names the problem and the next step: "That code expired. Send a new one?" with the button inline. Never "Invalid request".
- Loading states on every button, disabled while pending, no double-submit.
- Login and signup are the same screen — detect whether the identifier exists and adapt.

Full Arabic RTL, including the phone number field (number stays LTR inside an RTL layout).
```

## P04 — Onboarding wizard

```text
Build /onboarding — it must end with the founder holding a real artifact within 10 minutes of signup, not with a filled-in profile.

STRUCTURE — one question per screen, large tap targets, step counter, working back button, "skip for now" on everything non-essential:
1. "What are you building?" — or "I'm still figuring it out", which routes to the idea-discovery path below.
2. Stage — visual cards: just an idea / talking to users / building it / already launched.
3. Country — flags, MENA countries first.
4. What you want from Startpad — multi-select: validate my idea, find co-founder, get first users, raise money, learn.
5. → Straight into their first mission. NOT a dashboard.

IDEA DISCOVERY PATH (for "still figuring it out")
Ask: what are you good at, what communities are you part of, what annoys you weekly, what have you built before. Then AI generates 5 candidate startup directions grounded in MENA market context, each with a one-line why-now. They pick one and it becomes their idea.

Each question states why it's being asked ("so we can match you to mentors in your country"). Answers save immediately — closing the tab mid-flow and returning resumes at the same step.
```

## P05 — Dashboard / mission control

```text
Rebuild the logged-in home (/app). It answers exactly one question: what do I do right now?

LAYOUT, in strict priority order
1. NEXT ACTION CARD — the largest element on screen. Mission number and name, the specific next task in plain language, estimated minutes, one primary button ("Start — 12 min"). If a mission is in progress, show "Continue" and the step they're on.
2. Progress row beneath it: missions completed out of 15 as a horizontal path, current streak, XP. Monospace tabular numerals. Tapping the path opens /app/map.
3. "Your startup" card: name, one-line description, stage — editable inline.
4. Recent artifacts: the things they've produced, tappable to view or share.
5. Community strip: 3 posts from founders on the same mission, with a compose prompt.
6. Mentor strip: 2 mentors matched to their stage and country, with next available slot.

RULES
- Never a grid of equal-weight cards. The hierarchy must be unmistakable at a glance.
- If they haven't started, the whole screen is one card: "Start mission 1."
- If a mission has been untouched for 72h, the next-action card offers a smaller version: "Just do step 1 — 3 minutes."
- Mobile: bottom tab nav — Home, Missions, Community, Mentors, Profile.
- Skeleton loading shaped like the real cards. Never a full-page spinner.
```

## P06 — /missions — public curriculum map

```text
Create /missions — a public, crawlable page showing all 15 missions. Visible without an account. This is both a trust surface and the main SEO surface.

For each mission show: number, name, the outcome in one sentence, estimated time, the artifact it produces, and which AI tools it uses. Group them into three phases (Validate / Build / Launch) with a phase intro.

- Desktop: a vertical path with connected nodes and alternating content.
- Mobile: a single-column stepped list with a connecting line.
- Each mission links to /missions/:slug — its own public page with a fuller description, an example artifact from a real founder, and a "start this mission" CTA.
- Server-render for SEO. Unique title and meta description per mission page. Add FAQ and Course schema.org structured data.
- A "start from mission 1" CTA fixed at the bottom on mobile.

Full Arabic version at /ar/missions with RTL layout — the path direction mirrors correctly.
```

## P07 — Mission runner + AI panel

```text
Rebuild the mission screen (/app/mission/:id) as a step runner. This is the core loop of the product.

STRUCTURE
- Every mission is 3-6 steps. Each step is ONE task, completable in under 5 minutes, on a phone, in portrait.
- Header: mission name, step X of Y, a thin progress bar, and a close button that saves and exits without confirmation dialogs.
- Body: the task explained in 2 sentences max, a worked example collapsed behind "see an example", and the input — text, checklist, upload, or multi-field depending on the step.
- Autosave every field on blur and every 5 seconds. A subtle "saved" indicator. Refreshing or losing connection must never lose input.
- Footer: "Next step" primary button, always thumb-reachable and never covered by the keyboard.

AI PANEL
Docked at the bottom (a sheet on mobile, a right rail on desktop). It already knows the founder's idea, stage and country — it never asks them to re-explain. It opens with 3 suggested actions specific to THIS step, e.g. "sharpen this problem statement", "write 5 interview questions for this segment". Output streams token by token, lands in an EDITABLE field, and offers: regenerate, make shorter, translate to Arabic, use this. One line under the panel stating what's sent to the AI.

COMPLETION MOMENT
On finishing the last step: a full-screen celebration (respecting prefers-reduced-motion) showing the artifact they produced, XP earned with an animated counter, what unlocks next, and a generated share card with one-tap sharing to WhatsApp / Instagram Stories / X. Two buttons: "Next mission" and "Back to dashboard". Never just a toast.
```

## P08 — Progress, XP, streaks, badges

```text
Build the progression system across the app.

- XP awarded per completed step and per completed mission. Every XP award is tied to a real artifact produced — never for logging in or clicking around.
- Streak = days with at least one completed step. Show a flame with the day count in monospace tabular numerals. A "streak freeze" that forgives one missed day per week, granted automatically and explained plainly.
- Badges are receipts, not stickers: "Talked to 10 customers", "Shipped a landing page", "First paying user". Each badge shows the evidence behind it.
- /app/map: the 15 missions as a path with four node states — locked, available, in progress, complete. Each state distinguishable by shape and icon, not by color alone. Locked missions still show their name, outcome, and exactly what unlocks them. Never a blank grey padlock.
- Progress ring component with an animated increment on change, disabled under prefers-reduced-motion.
- No public shaming mechanics: no visible "you're behind", no red decay meters. Motivation only, never guilt.
```

## P09 — Public founder profile

```text
Create the public founder profile at /@:username — the highest-value new page in the product. It's a status object, a growth loop and an SEO surface at once.

CONTENT
- Header: avatar, name, city + country flag, one-line bio, the startup name and stage.
- Progress: missions completed out of 15 as a visual path, badges earned, member since, current streak.
- Published artifacts: only the ones the founder explicitly chose to make public — idea snapshot, landing page link, pitch deck, traction numbers.
- Actions for visitors: "Give feedback" (opens a short form), "Follow", and share.
- Optional "looking for" chips: co-founder, first users, mentor, funding.

RULES
- Every field is private by default with a clear per-item toggle in settings. Never publish anything without an explicit opt-in.
- Server-rendered with per-profile meta tags and a dynamically generated Open Graph image (startup name, founder name, missions completed) so the link looks designed when pasted into WhatsApp or X.
- The founder gets a "your profile is live — share it" prompt after completing mission 3, not before.
- Works in Arabic RTL with Arabic names rendering correctly.
```

## P10 — Share card generator

```text
Build a share card generator used at every milestone.

TRIGGERS: mission completed, badge earned, all 15 missions finished, first paying user logged.

OUTPUT — rendered client-side on canvas, no external services:
- 1080x1920 for Instagram / WhatsApp Stories
- 1200x630 for X and LinkedIn

DESIGN
On-brand, genuinely postable — this has to survive being seen next to a friend's photos. Founder name and avatar, startup name, the milestone in large type, progress (e.g. "9 of 15 missions"), and a small startpad.me mark. Offer 3 color variants so it doesn't look identical every time a founder posts.

SHARING
One tap to WhatsApp, Instagram Stories, X, LinkedIn, plus "download image" and "copy link". Use the Web Share API where available, with explicit fallbacks. Track share_card_generated and share_completed with the platform.

Arabic version with correct Arabic typography and RTL composition — not a mirrored Latin layout.
```

## P11 — Launch Wall

```text
Create /launched — a public wall of every startup that has completed all 15 missions.

- Card grid: startup logo or generated monogram, name, one-line description, founder name and photo, country flag, launch month, and a link to the product.
- Filters: country, industry, month. Search by name.
- Each card links to the startup's public page: the full story, the founder profile, the artifacts they made public, and the mission timeline showing how long each phase took.
- Sort by newest, with a "just launched" badge for the last 7 days.
- Server-rendered with structured data — this page should rank and should be linkable by journalists and investors.
- Empty state before you have launches: show founders currently on missions 12-15 as "launching soon" with their progress. Never show an empty grid.
- A "you could be here" CTA at the bottom for logged-out visitors.
```

## P12 — Mentors directory & booking

```text
Rebuild the mentors experience.

/mentors — DIRECTORY
Filters that match how founders actually think: country, language (Arabic / English / both), expertise (product, fundraising, growth, tech, legal), stage they help with, and "available this week". Each card shows photo, name, current role, languages as flags, expertise chips, typical response time, number of founders helped, and the next available slot.

/mentors/:slug — PROFILE
Bio, background, what they help with, what they explicitly don't help with, session length and price (or "free"), languages, availability calendar, and reviews from founders with the mission they were on at the time.

BOOKING
- Slots shown in the FOUNDER's timezone, with the timezone named explicitly.
- Booking asks one question: "What do you want help with?" — pre-filled from their current mission.
- Confirmation on screen + email + WhatsApp, with add-to-calendar links.
- A visible booking state machine everywhere the booking appears: requested → confirmed → completed → cancelled / no-show. Ambiguity here is the top complaint in every mentorship product.
- Auto-generate a one-page prep brief from the founder's mission progress and send it to the mentor 24h before the call. Give the founder 3 suggested questions.
- Post-call screen: rate the call, capture 3 action items, and turn those items into tasks inside their current mission.
```

## P13 — Community feed & cohort circles

```text
Build /community as an in-app experience, not a link out to Discord.

FEED
Scoped by default to founders on the same mission as the viewer, with tabs: My mission · My circle · All. Each post shows the author's avatar, name, country flag, and which mission they're on — the mission context is what makes this valuable.

POSTING
Never a blank composer. Offer structured prompts: "Share an artifact for feedback", "Ask a question", "Share a win", "Looking for a co-founder". Each prompt opens a short form with fields, not an empty box — this multiplies participation, especially from founders posting in a second language.

CIRCLES
Auto-group founders who started in the same month into circles of 8-15, with a shared progress board showing everyone's mission count, and a weekly check-in prompt. Small groups drive far more accountability than a global feed.

SAFETY
Report and block on every post and profile, visible community rules, rate limits for accounts under 24h old, and a moderation queue. Build this before scaling, not after.

Reactions and threaded replies. Arabic and English posts in the same feed, each rendering in its correct direction — detect per post, don't force one direction on the container.
```

## P14 — Pricing page

```text
Create a public /pricing page — visible without an account.

- Two or three plans maximum. State exactly what is free forever, in plain language, at the top.
- Prices in local currency, auto-detected by country, with a manual switcher: EGP, SAR, AED, USD. Show the monthly price as the default with an annual toggle that names the actual saving.
- "No card required for the free plan" stated explicitly next to the free CTA.
- A verified student tier: university email verification, with the discount stated up front.
- A comparison table listing what's included per plan, phrased as outcomes ("unlimited AI generations", "2 mentor calls per month"), not as feature names.
- FAQ: can I cancel anytime (yes, one tap, and say where the button is), what happens to my work if I downgrade (it stays), do you store my idea, is there a refund.
- ZERO dark patterns: no fake countdowns, no fake scarcity, no pre-checked upsells, no card capture for a free trial.
- Payment methods shown as logos: cards, Apple Pay, and the regional rails — Fawry and Vodafone Cash for Egypt, mada for Saudi.
```

## P15 — Momentum paywall

```text
Build the in-app upgrade screen (/upgrade) and its trigger logic.

TRIGGER: immediately AFTER a mission is completed — never mid-mission, never on app open, never as an interstitial blocking work.

SCREEN
- Opens by naming what they just achieved: "You've validated the problem. 4 missions done."
- Then what's next and what it needs: "Mentor calls and the AI pitch deck builder are on Pro."
- A short, concrete list of what unlocks — outcomes, not features.
- Price in local currency, monthly and annual, plus a one-time "founder pass" option for people who won't commit to a subscription.
- An explicit line: "Your progress and artifacts stay yours either way."
- A visible, non-hidden dismiss. Once dismissed, don't show it again for at least 3 missions.

Track paywall_viewed with the triggering mission id, paywall_dismissed, and upgrade_completed. Full Arabic RTL.
```

## P16 — Arabic & RTL

```text
Implement full Arabic support as a first-class locale, not a toggle.

ROUTING & SEO
Locale in the URL (/ar/*), persisted per user, with hreflang tags and per-locale meta. Language switcher in the header and in settings.

LAYOUT
dir="rtl" on the document. Replace every directional CSS property with a logical one — margin-inline-start, padding-inline-end, inset-inline, text-align: start. Mirror directional icons (arrows, chevrons, progress direction, the mission path). Do NOT mirror logos, clocks, phone numbers, or media playback controls.

TYPOGRAPHY
Load an Arabic-native family (IBM Plex Sans Arabic, Noto Sans Arabic, or Cairo) with its OWN size and line-height scale — Arabic needs roughly 1.1x the font size and 1.2x the line-height of the Latin equivalent to feel correct. Never rely on a Latin font's Arabic fallback.

CONTENT
Copy written natively in Arabic in the register young MENA founders actually use — not machine-translated English. Keep widely-used English startup terms in Latin script where that's how people actually say them (MVP, pitch deck, product-market fit) rather than forcing awkward translations.

DETAILS
Numbers, dates and currency formatted per locale via Intl. Mixed-direction content (an English startup name inside an Arabic sentence) must render correctly — use bdi elements. Forms, validation messages, toasts and the AI panel all fully RTL.

Test every single screen in Arabic before shipping — half-done RTL reads worse to this audience than English-only.
```

## P17 — Mobile shell & PWA

```text
Make Startpad feel like an app on a phone.

- Bottom tab navigation, 5 items max: Home, Missions, Community, Mentors, Profile. Active state clear, 44x44px minimum targets, safe-area insets respected on notched devices.
- Replace every centered modal with a bottom sheet on mobile, draggable to dismiss.
- Primary actions always thumb-reachable and never obscured by the on-screen keyboard.
- Ship as an installable PWA: manifest, icons, offline app shell, and an install prompt shown after the 2nd mission completion — never on first visit.
- Web push notifications with a permission request that is asked in-context, explaining the value first ("get a nudge when your mentor replies"), never on page load.
- Offline: cached shell, queued writes that sync on reconnect, and a clear "you're offline — your work is saved locally" banner.
- Optimize for mid-range Android on 3G: LCP under 2.5s, images in WebP/AVIF with explicit dimensions, code-split routes, no layout shift.
```

## P18 — Notifications & lifecycle

```text
Build a behaviour-triggered notification system — push and email, never a calendar-based blast.

TRIGGERS
- Mission started but not finished after 24h → "You're 2 steps from finishing mission 3."
- Streak about to break (evening, local time) → one nudge only.
- A mentor replied or confirmed a booking.
- Someone commented on or reacted to a published artifact.
- A circle member completed a mission you're also on.
- 7 days inactive → the smallest possible re-entry: "One 3-minute step to get back in."

RULES
- Every notification names one concrete next action and deep-links straight to it.
- Hard cap: 3 per week per user, deduplicated, and never between 11pm and 8am local time.
- Granular controls in /settings with a single global mute.
- Email templates work on mobile, in dark mode, and in Arabic RTL.
- Track sent / opened / actioned per trigger type so low performers can be switched off.
```

## P19 — Referral & invite

```text
Create /invite — a referral loop built for how this audience actually shares.

- Personal referral link plus a pre-written share message, WhatsApp-first (WhatsApp is the primary channel in this region, not email).
- Two-sided reward, stated plainly: the friend gets something on signup, the referrer gets something when the friend completes mission 1 — not on mere signup, so the loop rewards real activation.
- A generated invite card image with the founder's name and startup on it.
- Progress tracker: invited / joined / activated, with the reward state per person.
- Surface the invite CTA contextually — after a mission completion and on the profile — not as a permanent banner.
- A separate /campus page for a university ambassador program: what ambassadors get, an application form, and a leaderboard of universities by founders launched. This is the natural growth channel for MENA Gen Z.
```

## P20 — State kit — empty, loading, error, offline

```text
Design and implement all four states for every list, feed and async surface in the app.

EMPTY: a simple on-brand illustration, one encouraging line, and exactly one action. Examples — Artifacts: "Nothing here yet. Finish mission 1 and this fills up." + "Start mission 1". Community: "Be the first founder on this mission to post." + a composer prompt. Mentors with filters applied: "No mentors match those filters" + a clear-filters button.

LOADING: skeletons shaped like the actual content, never a centered full-page spinner. For AI generation, show a real status line that changes ("reading your idea…", "checking the market…") rather than a generic loader.

ERROR: name what happened and how to fix it, with a retry button that actually retries. Never "An error occurred". Preserve any text the user had typed.

OFFLINE: a persistent banner, "your work is saved locally", disabled actions that require the network clearly marked, and automatic sync on reconnect.

Also build an on-brand 404 that routes back into the current mission, and a session-expired state that returns the user exactly where they were after re-auth.
```

## P21 — Accessibility pass

```text
Run a WCAG 2.2 AA pass across the entire app and fix what fails.

- Contrast: every text/background pair at 4.5:1 (3:1 for text 24px+), in BOTH light and dark themes. Audit muted greys and text on the accent color specifically — those are where it usually fails.
- Tap targets: 44x44px minimum, with adequate spacing between adjacent targets.
- Focus: a visible focus ring on every interactive element, logical tab order, focus trapped in dialogs and sheets, and focus returned to the trigger on close.
- Forms: a real label on every input (placeholder is not a label), errors linked via aria-describedby and announced, and required fields marked in text, not by color.
- Motion: all gamification animation disabled under prefers-reduced-motion, including confetti and counters.
- Screen readers: meaningful alt text, aria-live on progress and XP changes, semantic headings in order, skip-to-content link, and no information conveyed by color alone (mission node states need shape or icon differences too).
- Test with keyboard only and with VoiceOver on iOS, in both English and Arabic.
```

## P22 — Analytics instrumentation

```text
Instrument the product so we can find the drop-off.

EVENTS: landing_viewed, try_started, try_step_completed, try_completed, signup_started, signup_completed, onboarding_completed, mission_started, mission_step_completed, mission_completed, artifact_created, ai_generation_requested, share_card_generated, share_completed, mentor_viewed, mentor_booked, mentor_call_completed, community_post_created, paywall_viewed, paywall_dismissed, upgrade_completed, notification_clicked.

PROPERTIES on every event: mission_id, step_index, locale (en/ar), device type, country, plan, days_since_signup.

DASHBOARDS
1. Activation funnel: landing → try_started → try_completed → signup → mission 1 complete.
2. Per-mission completion rate across all 15 — this chart shows exactly which mission is killing retention.
3. Time to first artifact, as a distribution.
4. D1 / D7 / D30 return, split by locale and country.
5. Share rate per completed mission.

Respect consent: no tracking before the user accepts, and a working opt-out in /settings.
```

## P23 — Trust, settings & account control

```text
Build the trust surfaces. This audience is the most fraud-aware cohort online and checks these before paying.

/trust — one page, plain language, no legalese wall:
- What data we collect and why.
- What happens to your idea: is it sent to an AI model, is it used for training, who can see it. Be specific.
- Who owns what you create — the founder does. Say it in one sentence at the top.
- How to delete your account and everything in it.
- Contact for a real human.

/settings — sections: Profile (with per-item public/private toggles for the public profile), Language (English / العربية), Notifications (granular per trigger plus global mute), Billing (current plan, one-tap cancel with the button plainly visible — no retention maze), Data & privacy (export my data, delete account with clear consequences and no guilt-tripping copy).

Every destructive action has a confirm step that names the consequence exactly ("This deletes your 9 artifacts and cannot be undone").
```

## P24 — Final QA sweep

```text
Run a full QA pass over Startpad and fix everything you find. Report what you fixed.

1. MOBILE: every screen at 390px width. No horizontal scroll anywhere. No primary action hidden behind the keyboard. All tap targets 44px+. Safe areas respected.
2. ARABIC: every screen at /ar. Correct RTL layout, mirrored directional icons, Arabic type scale applied, no clipped or overlapping text, mixed-direction content rendering correctly.
3. DARK MODE: every screen. No unreadable text, no invisible borders, no white flash on load, no color defined only inside a media query.
4. STATES: force empty, loading, error and offline on every list and async surface. Confirm each is designed, not default.
5. DATA LOSS: refresh mid-mission, lose connection mid-form, close the tab during onboarding. Nothing typed should ever be lost.
6. AUTH EDGE CASES: expired OTP, wrong code 3 times, existing account via a different method, anonymous session migration on signup.
7. PERFORMANCE: Lighthouse on mobile throttled to 3G. LCP under 2.5s, CLS under 0.1. Fix the worst offenders.
8. COPY: no lorem, no placeholder text, no "An error occurred", no untranslated strings in the Arabic build.

Give me a list of what was broken and what you changed.
```
