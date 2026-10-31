# StartPad — Lovable Prompts (Round 12)

Four prompts for the move from free to paid.

| Set | Scope | Prompt |
|---|---|---|
| 1 | Pricing in the public shell | A |
| 2 | The "free" claim sweep — whole platform | A |
| 3 | Billing page (Pro / Team) | A |
| 4 | Legal, FAQ and Help updates | A |

---

## Three things to decide before you build any of this

### 1. What happens to the 103 founders who joined when it was free?

Your landing page has been saying "100% Free to Start" and showing all 15 missions. People signed up on that basis. Moving missions 4–15 behind Pro takes something away from them.

**Grandfather them.** Give every account created before the pricing launch permanent free access to all 15 missions, and tell them directly: *"You joined before we introduced paid plans. All 15 missions stay free on your account, permanently."*

The cost is near zero — 103 accounts — and the alternative is your entire founding cohort discovering the product they were promised now costs money. That's the kind of thing people post about, and this audience posts. It may also matter legally in some jurisdictions where a material change to terms requires notice and consent.

### 2. Pricing is in USD, for a MENA audience

$10/month is roughly 500 EGP. For an Egyptian student — one of the occupational statuses you're about to collect — that is a significant monthly commitment, and card penetration among under-25s in the region is low.

Worth resolving before launch: local currency display (EGP, SAR, AED), local payment methods (Fawry, mada, Apple Pay), regional price parity rather than a flat USD figure, and a student rate. A product positioned as *"Built in Cairo, designed for the Arab world"* priced only in dollars is a mismatch your audience will notice.

### 3. The urgency styling works against you

The red **"⚡ LIMITED TIME — 50% OFF PRO & TEAM ⚡"** banner and the diagonal "SAVE 50%" ribbons are the visual language of discount spam. They clash with the restrained navy-and-green identity everywhere else in the product, and for a platform whose value is rigorous judgement, pressure-selling aesthetics undercut the thing you're selling.

"Limited time" also has no end date, which reads as permanent fake urgency — and permanent urgency stops working while still costing trust.

**Keep the discount, drop the theatrics.** A quiet line — *"Launch pricing — 50% off until 31 October"* — with a real date does the same job and matches the rest of the product. Prompt 1·A includes this.

One small thing: the pricing page says **103+ founders**, the landing page says **104+**. Same number, two places, two values.

---
---

# Set 1 — Pricing in the Public Shell

## PROMPT A — Add Pricing to the Navigation and Fix the Page

```text
PAGE: Public navigation, footer, and the pricing page (/pricing).

PART 1 — NAVIGATION

The pricing page exists but is not linked from the public navigation. A visitor
can only reach it if someone sends them the URL.

  a) Add "Pricing" to the public nav, in this order:
       About · How It Works · Pricing · Knowledge Hub · Founder Readiness
       Assessment
     Pricing sits third — after the two pages that explain what StartPad is,
     before the content pages. A visitor should understand the product before
     they see the price.

  b) Use the ONE shared public nav component. Every public page gets the same
     items — the contact page currently renders a reduced set, which is the
     bug this would otherwise repeat.

  c) Add Pricing to the footer's Quick Links.

  d) ROUTE TYPE: /pricing is SHARED. Logged out → public shell. Logged in →
     app shell, and the CTAs change (see part 3).

PART 2 — FIX THE PAGE

  a) REPLACE THE URGENCY STYLING. Remove the red "⚡ LIMITED TIME — 50% OFF
     PRO & TEAM ⚡" banner and the diagonal "SAVE 50%" corner ribbons. They
     read as discount-spam and clash with the navy/green identity used
     everywhere else.
     Replace with one quiet line beneath the plan toggle:
       "Launch pricing — 50% off until 31 October 2026"
     Use a REAL date. "Limited time" with no deadline is permanent fake
     urgency; it stops working and costs trust while it does.
     Keep the strikethrough original price and the "50% OFF" chip on each
     card — those are honest and useful.

  b) FIX THE FOUNDER COUNT. This page says "103+ MENA founders"; the landing
     page says "104+". Derive both from one source.

  c) CURRENCY. Prices show in USD only. Add local currency display for EGP,
     SAR and AED based on the visitor's country, with USD as the fallback.
     If regional pricing is not decided yet, at minimum show the converted
     local amount alongside the dollar figure so the cost is legible.

  d) ADD A COMPARISON TABLE below the three cards. The current cards repeat
     the same lines across Pro and Team, which makes the difference hard to
     see. A feature-by-plan table with ticks reads faster.

  e) ADD PRICING FAQs at the foot of the page — the questions that block a
     purchase:
       What happens to my work if I downgrade?
       Can I switch between monthly and annual?
       Do you refund? What's the policy?
       What payment methods do you accept?
       Is there a student rate?
       What happens when the launch discount ends — does my price go up?
     Answer that last one plainly. It is the question a careful buyer asks
     first.

  f) KEEP: the "Mentor sessions are paid per-session and available on every
     plan — booking is never gated behind a tier" line. It is clear and it
     pre-empts a real worry.

PART 3 — AUTH-AWARE CTAs

  Use the AuthAwareCTA component. On a signed-in view the buttons must
  reflect the founder's actual plan:

    Signed out          → "Start free — no card required" / "Get started with Pro"
    Signed in, Free     → "Upgrade to Pro" / "Upgrade to Team"
    Signed in, Pro      → Pro card shows "Your current plan" (not a button);
                          Team shows "Upgrade to Team"
    Signed in, Team     → Team card shows "Your current plan"

  Never show "Get started with Pro" to someone already paying for Pro.
```

---
---

# Set 2 — The "Free" Claim Sweep

## PROMPT A — Make Every Claim Match the New Pricing

```text
PAGE: Whole platform — every surface that describes what StartPad costs or
what a founder gets.

THE PROBLEM
The product was built and marketed as free. It now has paid tiers where the
Free plan includes only missions 1–3. Every "free" claim written before this
change is now either wrong or misleading, and they are scattered across the
marketing site, the app, the AI prompts and the translation files.

DO THIS AS AN AUDIT, NOT A GUESS. Search the codebase and all locale files for
every instance of: "free", "100%", "forever", "no cost", "all 15", "15
missions", "complete journey", "everything", "unlimited", and the Arabic
equivalents. List every hit with its file and line before changing anything.

KNOWN OFFENDERS — fix these and report anything else the audit finds:

  LANDING PAGE
    - The stat band reads "100% · FREE TO START". Now inaccurate as a
      headline claim.
    - The hero floating card reads "Pricing · 100% Free to Start".
    - "15 missions. 8 phases. One launched startup." — true of the product,
      but a visitor reads it as what they get for free.
    - The mission roadmap displays all 15 missions with no indication that
      12 of them require Pro.

  Suggested replacements — accurate and still attractive:
    "Free to start · Missions 1-3 free, no card required"
    "Start free. Upgrade when you're ready to go past Mission 3."

  IN-APP
    - The journey roadmap shows missions 4-15 as locked. A lock now means two
      different things: "not reached yet" and "requires Pro". USE TWO
      DISTINCT VISUAL STATES with different icons — a founder must be able
      to tell at a glance which is which. A padlock that means both is the
      single most confusing thing this change can introduce.
    - Any copy promising "all 15 missions" to a Free user.
    - The mission runner: when a Free user reaches Mission 4, show a clear,
      non-hostile upgrade screen — what they've done so far, what Pro adds,
      the price, and a way back to their completed work.

  AI PROMPTS
    - The AI Mentor and coaching prompts may reference features the founder's
      plan does not include. Pass the plan into the context layer so the AI
      never recommends a Pro-only tool to a Free user. That is a bad
      experience and it reads as a bait-and-switch.

  KNOWLEDGE HUB / RESOURCE LIBRARY / EMAILS
    - Any article, guide, onboarding email or notification that says the
      platform is free.

  ARABIC
    - Every fix must land in the Arabic locale file too. A stale Arabic
      string promising free access is the same problem, harder to spot.

GRANDFATHERING — implement before any of the above ships:
  Every account created before the pricing launch date keeps full access to
  all 15 missions, permanently. Add a `legacy_full_access` flag, set it for
  existing accounts, and honour it everywhere the plan gate is checked.
  Then email them: "You joined before we introduced paid plans. All 15
  missions stay free on your account, permanently."
  Show it in the app too — a quiet "Founding member · full access" badge on
  their billing page.

REPORT: every file changed, and any claim you found that you were unsure how
to reword.
```

---
---

# Set 3 — Billing

## PROMPT A — Build the Billing Page

```text
PAGE: New route /settings/billing, inside the app shell. Reachable from the
avatar menu and from settings.

Every signed-in user sees it — Free users too, since it is where they upgrade.

SECTION 1 — CURRENT PLAN
  - Plan name and what it includes, in one line
  - Price and billing period ("$10/mo, billed monthly" or "$100/yr, billed
    annually")
  - Next billing date and the amount that will be charged
  - If a discount applies: "Launch pricing — 50% off. Renews at $20/mo from
    31 Oct 2027." State the post-discount price explicitly. A customer who
    discovers the real price at renewal churns and disputes.
  - For legacy accounts: "Founding member — all 15 missions, free,
    permanently"
  - Buttons: Upgrade · Change plan · Cancel

SECTION 2 — PAYMENT METHOD
  - Card brand and last four digits, expiry, "Update payment method"
  - NEVER store card numbers. The payment processor holds them; you store a
    token. Say so in the privacy policy.
  - Expiry warning 30 days out
  - Billing address and tax ID field where VAT registration applies

SECTION 3 — PAYMENT HISTORY
  A table, newest first: date, description, amount, status (Paid / Failed /
  Refunded), and a download link per row.
  - Invoices download as branded PDFs using the shared document template from
    Round 11 Prompt B — logo, metadata, meaningful filename.
  - Invoices must carry: invoice number, both parties, line items, tax
    breakdown, currency, payment method and date. These get filed for
    accounting; a receipt without a tax line is not usable.
  - Empty state for Free users: "No payments yet."

SECTION 4 — CHANGE PLAN
  Upgrade:
    - Takes effect immediately
    - Show the prorated amount charged today, itemised, BEFORE confirming
    - Access unlocks straight away
  Downgrade:
    - Takes effect at the end of the current period, not immediately — they
      paid for it
    - Show exactly what they lose and WHEN: "You'll keep Pro until 31 Oct.
      After that, missions 4-15 lock and your Loadout entries become
      read-only."
    - Nothing is deleted. State that plainly: "Your work is kept. Upgrading
      again restores access to everything."
  Monthly ↔ annual:
    - Show the saving in money, not just "2 months free"
  Team seats:
    - Add and remove members, show seats used (3 of 5), show the cost of
      going over, handle invitations and removals

SECTION 5 — CANCEL
  - Reachable in two clicks. Do not bury it — burying cancellation triggers
    chargebacks and, in several jurisdictions, consumer-protection breaches.
  - Show what happens and when: access continues to the period end
  - One optional exit question ("What made you cancel?") — one field, skippable
  - Offer a downgrade to Free as an alternative, once, without pressure
  - Confirm by email

CROSS-CUTTING
  - FAILED PAYMENTS: retry schedule, in-app banner, email, and a grace period
    before access is removed. Never remove access silently on the first
    failed charge — most failures are expired cards, not intent to leave.
  - TAX: VAT applies in Egypt (14%), Saudi (15%) and the UAE (5%). Compute by
    the customer's country, show tax as a separate line, and put it on the
    invoice.
  - CURRENCY: display in the customer's currency and be explicit about what
    currency the charge is made in.
  - A downgrade or cancellation must never delete mission answers, uploaded
    evidence, or Loadout data. Read-only, never destroyed.
```

---
---

# Set 4 — Legal, FAQ and Help

## PROMPT A — Update Every Document for Subscriptions

```text
PAGE: /terms, /privacy, /cookies, /faq, /help — all now out of date, because
they were written for a free product.

TERMS OF SERVICE — add a subscriptions section covering:
  - The plans, what each includes, and that contents may change with notice
  - Billing cycle, auto-renewal, and the renewal price after any discount
  - How to cancel, and when access ends
  - REFUND POLICY. You need one, stated plainly. Consumer protection law in
    Egypt, Saudi and the UAE gives buyers rights here, and app-store and
    card-scheme rules require a policy too. A 14-day refund on first purchase
    is a reasonable, defensible default.
  - Price changes: how much notice existing subscribers get (30 days is the
    norm) and their right to cancel before it applies
  - Taxes: prices exclusive or inclusive of VAT, stated once, clearly
  - Failed payment and what happens to access
  - Team plans: who the account holder is, who can add or remove seats, and
    what happens to a removed member's work
  - Grandfathered accounts: state that legacy full access is permanent

PRIVACY POLICY — add:
  - The payment processor as a named third party, with what it receives
  - What billing data StartPad stores: name, billing address, tax ID, card
    token, last four digits, transaction history — and explicitly NOT full
    card numbers
  - Retention for financial records — usually longer than other data because
    of accounting law, so it needs its own line
  - Whether payment data crosses borders, and the safeguard

COOKIE POLICY — add any cookies set by the payment processor and the checkout
flow, including fraud-prevention cookies, which are usually classed as
essential but must still be disclosed.

FAQ — a Pricing and Billing section. Answer the blocking questions honestly:
  Is StartPad still free?          — Yes to start: missions 1-3, no card.
  What do I get on Free?
  What does Pro add?
  What happens to my work if I downgrade or cancel?
  Can I get a refund?
  What payment methods work in Egypt / Saudi / UAE?
  Is there a student rate?
  Will my price go up when the launch discount ends?
  I joined before pricing existed — what happens to my account?
  Are mentor sessions included?    — No: paid per session on every plan.
  How do Team seats work?

HELP CENTRE — add a Billing section:
  How to upgrade · how to downgrade · how to cancel · how to update your card
  · how to get an invoice · what to do if a payment fails · how to manage
  Team seats

CONSISTENCY
  - Every one of these documents must state the same prices, the same refund
    window and the same renewal terms. Pull the prices from one config so the
    documents cannot drift from the pricing page.
  - Update the "Last updated" date on each.
  - Translate all of it into Arabic. A billing dispute conducted against an
    English-only terms page, with a customer who bought through an Arabic
    interface, is a bad position to be in.
```

---

## Suggested order

| # | What | Why |
|---|---|---|
| 1 | Grandfathering (in Set 2·A) | Must ship before or with the paywall, not after |
| 2 | Set 2·A — the free-claim sweep | The product currently promises what it no longer gives |
| 3 | Set 1·A — nav and pricing page | Nobody can find the page today |
| 4 | Set 4·A — legal and FAQ | Required before taking money |
| 5 | Set 3·A — billing page | Needed the moment the first subscription exists |

Items 1, 2 and 4 all need to be true before you charge anyone. Item 3 can follow within days, but not weeks — a paying customer with no way to see an invoice or cancel is a support and compliance problem from day one.
