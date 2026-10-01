# StartPad — Lovable Prompts (Round 6)

Two prompts. The contact page rebuild you asked for, and the cross-page consistency problems it exposed.

| Set | Page | Prompts |
|---|---|---|
| 1 | Contact | A |
| 2 | Public shell (every public page) | A |

---

## Why stripping this page is the right call

You asked to remove the location, the numbers, and everything except the email and the form. That instinct fixes more than clutter — the elements you want gone are the ones actively costing credibility:

**"San Francisco, CA · Remote-first"** appears twice on a page belonging to a product whose homepage says *"MADE IN EGYPT · BUILT FOR MENA"* and *"Built in Cairo. Designed for the entire Arab world."* A MENA founder checking whether this is really a regional platform lands here and finds a San Francisco address. That single line undermines your whole positioning.

**The LinkedIn card is fabricated social proof.** "2,800+ followers", a "Recent post" with "142 · 28 comments · 15 reposts" — hardcoded numbers that will never update and cannot be verified. The follower count also sits oddly beside "104+ founders" on the homepage.

**"Empowering entrepreneurs worldwide"** and **"the #1 gamified platform"** are the third and fourth contradictions on one page — worldwide against MENA-focused, and an unsupportable superiority claim.

Removing all of it is the fastest credibility win available.

---
---

# Set 1 — Contact Page

## PROMPT A — Strip the Contact Page and Give It an Exit

```text
PAGE: Contact (/contact).

THE PROBLEMS

1. WRONG LOCATION. The page states "San Francisco, CA · Remote-first" in the
   contact row, and "San Francisco, CA" again in the sidebar card. StartPad's
   homepage says "MADE IN EGYPT · BUILT FOR MENA" and "Built in Cairo. Designed
   for the entire Arab world." A visitor checking whether this is genuinely a
   regional platform finds a US address on the contact page.

2. FABRICATED SOCIAL PROOF. The right-hand card shows "2,800+ followers" and a
   "Recent post" with "142 · 28 comments · 15 reposts". These are hardcoded,
   will never update, and cannot be verified. Remove the entire card.

3. UNSUPPORTABLE CLAIMS. "We're building the #1 gamified platform for aspiring
   entrepreneurs" and "Empowering entrepreneurs worldwide" — a superiority
   claim and a geography claim, both contradicting the MENA positioning.

4. TWO DIFFERENT EMAIL ADDRESSES ON ONE PAGE. contact@startpad.me in the body,
   hello@startpad.me in the footer. A visitor cannot tell which is real.

5. A PROMISE YOU MAY NOT KEEP. "Response: Within 24 hours" is a commitment with
   no stated support capacity behind it.

6. NO WAY FORWARD. The page dead-ends. A visitor who came here, got their
   answer, and is now interested has no route to signing up.

7. NO CONSENT ON THE FORM. It collects name, email and a free-text message with
   no link to the privacy policy and no consent line — the same gap as the
   signup form.

8. TWO DIFFERENT SOCIAL SETS. "FOLLOW US" at the top shows LinkedIn, Instagram,
   YouTube. The footer shows Instagram, TikTok, X, LinkedIn. Different networks
   in each.

9. A ~500px HERO holding one heading and one sentence.

THE FIX — rebuild as a single-column page. Remove far more than you add.

DELETE ENTIRELY:
  - The location row and every mention of San Francisco
  - The whole right-hand LinkedIn card: follower count, recent post,
    engagement numbers, "#1 gamified platform", "Empowering entrepreneurs
    worldwide", "Follow on LinkedIn"
  - The "Response: Within 24 hours" claim
  - The "FOLLOW US" social row near the top (the footer already has social —
    one set, not two)
  - The "Back to home" link (the logo does this)

NEW STRUCTURE, top to bottom, single column, max-width 640px, centred:

1. COMPACT HEADER — roughly a third of the current height.
     H1: "Contact us"
     One line: "Questions, feedback, or partnership ideas — send us a message
     and we'll get back to you."
   Drop the "Get in touch" pill above the heading; the H1 already says it.

2. DEFLECT FIRST — a quiet single line above the form:
     "Looking for a quick answer? Most questions are covered in the FAQ →"
   This links to /faq. It costs one line and removes a large share of the
   messages you would otherwise answer by hand.

3. THE FORM — the centre of the page and effectively its whole content:
     Name *          — text
     Email *         — email, validated
     Subject *       — a SELECT, not free text. Free text produces a mailbox
                       you cannot triage. Options:
                         General question
                         Problem or bug
                         Partnership or collaboration
                         Press or media
                         Applying to be a mentor
                         Feedback or feature request
                         Something else
     Message *       — textarea, minimum 20 characters
     [ ] I agree to the Privacy Policy   ← unticked, link opens in a new tab,
                                            submit disabled until ticked
     [Send message]  — full-width, green #047857

   Behaviour:
     - Inline validation per field on blur, never only on submit
     - Disabled button with a spinner while sending
     - SUCCESS: replace the form with a confirmation — "Message sent. We'll
       reply to [their email]." Do not just show a toast and leave the form
       full of their text.
     - FAILURE: keep everything they typed, show what went wrong, and give
       the email address as a fallback
     - Spam protection: a honeypot field plus rate limiting. Do not add a
       visible CAPTCHA — it costs more conversions than it saves at this
       volume.
     - Route submissions by the Subject value to the right inbox.

4. EMAIL FALLBACK — one quiet line beneath the form:
     "Prefer email? hello@startpad.me"
   PICK ONE ADDRESS and use it here, in the footer, in the privacy policy and
   everywhere else. Two addresses on one page is the problem; which one you
   keep matters less than that only one exists.

5. CTA BAND — the page must not dead-end. Auth-aware, using the SHARED route
   type from the routing work:

   LOGGED OUT:
     Heading: "Ready to start building?"
     Line:    "Join the founders working through 15 guided missions."
     Buttons: [Get started →]  (primary)   [Sign in]  (secondary)

   LOGGED IN:
     Heading: "Back to your journey"
     Buttons: [Continue Mission 1 →]  (primary)   [Go to dashboard] (secondary)
     Never show "Get started" or "Sign in" to a signed-in user.

6. FOOTER — the existing one, unchanged. It already carries the legal row and
   the social set.

RULES
  - No numbers anywhere on this page. No follower counts, no response times,
    no engagement metrics.
  - No location.
  - One email address.
  - One social icon set, in the footer only.
  - The form is the page. Everything else is a header, one deflection line,
    one fallback line and one CTA band.
```

**Why this order.** Self-contained and small. The CTA band needs the auth-aware routing from Round 3 Set 1·A; everything else can ship immediately.

---
---

# Set 2 — Public Shell Consistency

One prompt. Comparing the contact page against the other public pages surfaced four inconsistencies that affect every public route.

## PROMPT A — Make the Public Shell Consistent

```text
PAGE: The public shell — every logged-out page (/, /about, /how-it-works,
/knowledge-hub, /contact, /faq, /privacy, /terms, /cookies).

THE PROBLEMS — found by comparing the contact page with the landing page and
the Knowledge Hub.

1. THE PUBLIC NAV IS DIFFERENT ON DIFFERENT PAGES.
     Landing and Knowledge Hub:
       About · How It Works · Knowledge Hub · Founder Readiness Assessment
       · English · Sign in · Get started
     Contact page:
       English · About · Contact · Sign in · Get started
   How It Works, Knowledge Hub and the Founder Readiness Assessment vanish on
   the contact page, and the language switcher moves from the right to the
   left of the nav items. A visitor who reaches Contact loses the routes to
   your two best pre-signup pages.

2. TWO DIFFERENT LOGOS. The contact page's top nav shows a rocket icon with
   "StartPad" in one typeface; the footer on the same page shows the S-swirl
   mark with the wordmark beneath. The rest of the app uses the S-swirl. Pick
   one and use it everywhere.

3. TWO LANGUAGE SWITCHERS ON ONE PAGE — one in the nav, one in the footer,
   with different casing ("English" vs "English"). This was raised in Round 2
   and is still open.

4. TWO EMAIL ADDRESSES — contact@startpad.me and hello@startpad.me, both live
   on the contact page.

THE FIX

1. ONE PUBLIC NAV COMPONENT, used by every public route, with one item list:
     About · How It Works · Knowledge Hub · Founder Readiness Assessment
     ────────────────────────────────────
     [language]  Sign in  [Get started →]
   Contact does not need to be in the top nav — it is in the footer. But
   How It Works, Knowledge Hub and the Assessment must appear on every public
   page, because they are what convert a visitor.
   Highlight the current page as active. No page may render its own variant.

2. ONE LOGO ASSET, one lockup, used in the nav and the footer at different
   sizes. Delete the rocket variant.

3. ONE LANGUAGE SWITCHER — keep the nav one, remove the footer one.

4. ONE EMAIL ADDRESS everywhere: nav, footer, contact page, privacy policy,
   terms, FAQ, and any transactional email. Pick it and search the codebase
   for the other.

5. ONE FOOTER COMPONENT across public and app routes, carrying the legal row
   that is already correct: FAQ · Help centre · Privacy Policy · Terms of
   Service · Cookie Policy · Contact · Last updated.

6. AUDIT EVERY PUBLIC PAGE against this shell and report which ones were
   rendering their own nav, logo or footer variant. Where one page diverges,
   others usually do too.
```

**Why this order.** Run alongside Set 1·A — the contact page rebuild touches the same shell, and fixing both together avoids doing the nav twice.

---

## Suggested sequence

| Order | What | Why |
|---|---|---|
| 1 | Set 1·A | Removes three credibility contradictions and gives the page an exit |
| 2 | Set 2·A | Fixes the shell inconsistencies the contact page exposed |

Both are same-day. Set 1·A's CTA band depends on Round 3 Set 1·A being done; if it isn't, ship the logged-out version and add the auth branch after.
