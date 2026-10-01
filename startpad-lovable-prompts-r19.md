# StartPad — Pricing Page (Round 19)

Four prompts: the currency control collision, the missing Team plan, card layout, and page structure.

---

## The bug you're pointing at

Between "Prices shown for Egypt" and the plan cards there's a currency control, and **the "COMPLETE JOURNEY" ribbon is drawn on top of it.** Only the tail of it is readable — `…urrency   Egyptian Pound (EGP)` — the label is clipped behind the badge.

This is the standard ribbon-overlap failure: the badge is absolutely positioned with a negative offset and a higher stacking order, the card grid has no top padding to make room for it, and the currency row sits in the space the badge expands into. Nothing reserved the space, so the badge took it.

But the collision is the smaller half of the problem. There are **two currency affordances saying the same thing in different places**, and they disagree about what they even control:

- **"Prices shown for Egypt"** — left-aligned, plain grey text, not obviously interactive. It names a **country**.
- **The clipped dropdown** — right-aligned, behind the badge. It names a **currency**.

And the footnote underneath admits they aren't independent: *"Payment is taken by our current provider, in Egyptian Pounds for Egypt and in US Dollars elsewhere."*

**So currency is derived from country, not chosen.** If that dropdown lets a founder in Riyadh pick SAR and they are then charged in USD, the page made a promise checkout breaks. One control, labelled for what it actually changes.

### The FX exposure underneath it

`EGP 740` is the headline, `Based on $15.00 USD` is the small grey line, and the footnote says *"Local amounts are approximate."*

The Egyptian pound has lost more than 70% of its value since early 2022 across repeated devaluations. An approximate converted price on a page that doesn't say when it was converted will drift from what the provider actually charges — and a founder who sees EGP 740 and is billed EGP 780 raises a dispute. The rule that fixes it: **the big number is always the number they will actually be charged.**

---

## What's missing

**There is no Team plan**, and three things on the page point at one that isn't there:

- **"For educational institutions"** sits in the footer, with no price, no card and no CTA
- The FAQ asks **"What if my university sponsors StartPad?"**
- The plan grid shows two cards in a viewport wide enough for three, with large empty margins either side

And one product distinction has to be settled before any of it is built:

| | **Team** | **Cohort / Institution** |
|---|---|---|
| Who | 2–5 co-founders | A university, incubator or accelerator |
| Journeys | **One** — shared | **Many** — one per startup |
| Needs | Shared workspace, who-did-what | Admin dashboard, cohort analytics, branding, invoicing |
| Buys | Self-serve, by card | Sales conversation, by invoice |

**These are different products.** A founding team shares one Business Model Canvas; a cohort of twenty startups has twenty of them. Building "Team" as "Sprint × N seats" works for the first and fails the second.

---

## Everything else the screen shows

**The Free Explorer card is stretched to the Sprint's height**, leaving roughly 250px of empty white below its four bullets. Equal-height cards with unequal content is a flexbox default nobody chose — and the emptiness makes Free look thin rather than making Sprint look generous.

**The promo code box is above the plans**, before a founder knows what they're buying, and its button reads **"Sign in to apply"** — so it cannot be used by the person seeing it. Prime space above the fold, spent on a dead end.

**The comparison table mostly repeats the cards.** Nine of its eleven rows restate card bullets. Two earn their place: *Missions available — 1–3 of 15* and *Mentor sessions — Paid per session: never gated*, which is an honest and unusual thing to publish. With a third plan the table becomes genuinely useful; with two it's duplication.

**"—" for "not included"** reads as "unknown", not "no".

**"Join 124+ MENA founders already building with StartPad"** is a real, small, verifiable number and exactly the right kind of proof — in roughly 10px grey text where nobody will read it.

**"one-time"** is the single most important word on the Sprint card, and it's set inline at the size of a footnote next to a large price.

---
---

# The prompts

Four, in order. Paste one per message.

## PROMPT A — Fix the Currency Control

```text
PAGE: /pricing — the currency row above the plan cards, and the price block
inside each card.

THE PROBLEM

The "COMPLETE JOURNEY" ribbon on the Founder Sprint card is drawn on top of
the currency selector. Only the tail of the control is readable —
"…urrency  Egyptian Pound (EGP)" — because the badge is absolutely positioned
with a negative offset and a higher stacking order, and the card grid has no
top padding reserving space for it.

There are also TWO affordances describing the same thing, in two places, that
disagree about what they control:

  "Prices shown for Egypt"        left, plain text, names a COUNTRY
  "Currency: Egyptian Pound (EGP)" right, clipped,   names a CURRENCY

And the footnote below the cards says they are not independent: "Payment is
taken by our current provider, in Egyptian Pounds for Egypt and in US Dollars
elsewhere."

So currency is DERIVED from country, not chosen. If a founder in Riyadh can
select SAR here and is then charged in USD, this page made a promise that
checkout breaks.

THE FIX

1. STOP THE OVERLAP BY CONSTRUCTION, not by z-index tuning:

     - The currency control gets its OWN ROW, in normal document flow, with
       its own margin-bottom. Nothing absolutely positioned may enter it.
     - The card grid gets padding-top equal to at least half the badge
       height plus 8px, so the ribbon expands into reserved space.
     - The badge stays inside its card: position absolute, top 0,
       transform translateY(-50%), with the card overflow visible.
     - Do not raise the currency control's z-index to win. Reserve the space
       instead — a z-index fix breaks again the next time a badge changes
       size.

2. ONE CONTROL, LABELLED FOR WHAT IT ACTUALLY CHANGES. Replace both
   affordances with a single country selector, with the currency shown as a
   consequence rather than a second choice:

     Showing prices for  [ Egypt  ⌄ ]  ·  charged in Egyptian Pound (EGP)

   Right-aligned above the grid on desktop, full width above the grid on
   mobile. The country list carries flags and is searchable.

3. THE BIG NUMBER IS ALWAYS THE NUMBER THEY WILL BE CHARGED. This is the
   rule that prevents disputes:

     Egypt      EGP 740   large     "≈ $15.00 USD"   small
     Everywhere $15.00    large     "≈ EGP 740"      small
     else                           (local, clearly marked approximate)

   Never show a large local figure that is not the billing amount. A founder
   in Saudi Arabia must see $15.00 as the headline, because that is what
   their card will be charged.

4. DATE THE CONVERSION. Under the secondary figure:

     "Converted at today's rate · 1 Oct 2026"

   Refresh daily, store the rate with the quote. The Egyptian pound has lost
   more than 70% of its value since early 2022 — an undated approximate
   price drifts away from the charged amount, and the founder who notices
   files a dispute rather than an email.

5. IF THE DISPLAYED AND CHARGED AMOUNTS DIVERGE BY MORE THAN 2% at checkout,
   show the charge amount and a one-line explanation before the payment
   button, not after it:

     "The rate moved since you opened this page. You'll be charged EGP 762."

6. DETECTION IS A DEFAULT, NEVER A LOCK. Detect by IP, let the founder
   change it, remember the choice for the session and on the account. If
   detection and the account's saved country disagree, the account wins.

7. ON MOBILE the control stacks above the cards at full width with a 44px
   tap target, and the badge still must not overlap it.
```

## PROMPT B — Add the Team Plan

```text
PAGE: /pricing — the plan grid, and a new /pricing/teams page.

THE PROBLEM

There is no Team plan, and three things on this page point at one that does
not exist:

  - "For educational institutions" sits in the footer with no price, no card
    and no call to action
  - The FAQ asks "What if my university sponsors StartPad?"
  - Two cards sit centred in a viewport wide enough for three, with large
    empty margins on both sides

FIRST, A PRODUCT DECISION THAT HAS TO BE MADE BEFORE BUILDING

Two different buyers are being conflated, and they need different things:

  TEAM         2-5 co-founders building ONE startup.
               They share ONE journey. One Business Model Canvas, one set of
               mission answers, multiple contributors.
               Needs: shared workspace, who-did-what, no duplicate work.
               Buys: self-serve, by card.

  COHORT       A university, incubator or accelerator with 10-100 founders
               across MANY startups.
               Each startup has its OWN journey. Twenty teams, twenty
               canvases, twenty sets of answers.
               Needs: admin dashboard, cohort progress, export, branding,
               invoicing.
               Buys: through a conversation, by invoice.

Building "Team" as "Sprint multiplied by N seats" serves the first and fails
the second completely. Build the Team card now, self-serve; make Cohort a
contact route for now and a product later.

THE FIX

1. THREE CARDS. Free Explorer · Founder Sprint (highlighted) · Team Sprint.
   Equal width, Sprint keeps the ribbon and the border.

2. THE TEAM CARD:

     Team Sprint
     For co-founders building together

     from $12 per founder                       ← per seat, one-time
     Minimum 3 seats · 12 weeks · no renewal

     [ seat stepper: − 3 + ]   Total $36.00

     [ Start as a team ]

     Everything in Founder Sprint, for every member, plus:
       ✓ One shared journey — answers, canvases and evidence in one place
       ✓ See who contributed what, on every mission
       ✓ Assign missions to team members
       ✓ One shared readiness pack with every contributor credited
       ✓ Team dashboard: progress, gaps and who is blocked

3. SEAT PRICING LADDER — these numbers are a recommendation, put them in
   config so they can be changed without a deploy:

     const TEAM_PRICING = {
       currency: 'USD',
       individual: 15.00,
       tiers: [
         { minSeats: 3,  pricePerSeat: 12.00 },   // 20% off
         { minSeats: 10, pricePerSeat: 10.50 },   // 30% off
         { minSeats: 20, pricePerSeat: null  },   // "Talk to us"
       ],
       minSeats: 3,
       maxSelfServeSeats: 19,
     };

   The stepper recalculates the total live and shows the saving against
   buying individually: "You're saving $9 against 3 individual Sprints."
   At 20 seats the button becomes "Talk to us about a cohort".

4. COHORT ROW, under the three cards — one strip, not a fourth card, because
   it is not self-serve:

     For universities, incubators and accelerators
     Run a cohort of 20 to 100 founders with an admin dashboard, cohort
     progress tracking and invoicing.          [ Talk to us → ]

   Link it to /pricing/teams, and link "For educational institutions" in the
   footer to the same place. Right now that footer link is the only trace of
   this entire motion.

5. ANSWER THE FAQ THAT ALREADY EXISTS. "What if my university sponsors
   StartPad?" currently sits in the accordion with no plan behind it. Its
   answer should now point at the cohort route, and say plainly what happens
   to a founder whose institution buys for them — do they keep their work
   when the cohort ends? Say so.

6. CARD ORDER ON MOBILE: Founder Sprint first, then Free Explorer, then
   Team. The highlighted plan should not be the second thing a founder
   scrolls past.
```

## PROMPT C — Card Layout and Price Presentation

```text
PAGE: /pricing — the plan cards.

THE PROBLEM

The Free Explorer card is stretched to match the Founder Sprint card's
height, leaving roughly 250px of empty white space below its four bullets.
Nobody chose that — it is the flexbox default for equal-height cards with
unequal content, and it makes the free plan look thin rather than making the
paid plan look generous.

And "one-time" — the single most important word on the Sprint card, because
it answers the subscription anxiety that the FAQ's first question is also
about — is set inline at footnote size beside a large price.

THE FIX

1. CARDS ALIGN AT THE TOP, NOT STRETCHED TO EQUAL HEIGHT.

     align-items: start   on the grid

   A shorter plan is allowed to be a shorter card. If a uniform bottom edge
   is wanted for visual reasons, fill it with something real — not with
   nothing:

     "Ready for the full journey?  Compare plans ↓"

2. PRICE BLOCK, with the qualifier given its own line and real weight:

     EGP 740
     one-time · 12 weeks · no automatic renewal
     ≈ $15.00 USD · converted at today's rate

   "one-time" belongs on its own line directly under the number, not inline
   beside it. Three of the six FAQ questions are about what happens after
   payment; this line answers them before they are asked.

3. ADD A UNIT ANCHOR under the price. Fifteen dollars for twelve weeks is
   remarkably cheap and the page never says so:

     "About EGP 62 a week"

   Not a fake crossed-out price. A true restatement that makes the number
   land.

4. GROUP THE SPRINT'S FEATURES. Ten bullets plus a sub-header currently read
   as one long list. Three groups of three or four, each with a small
   heading:

     THE JOURNEY        all 15 missions · points, streaks, achievements ·
                        full community · journey analytics
     THE AI             evidence versioning, OCR, unlimited re-submission ·
                        worked examples on your weakest area · Mission
                        Mentor that remembers your history · AI Tools suite
     WHAT YOU KEEP      full Toolbox and canvases · PDF reports for every
                        mission · full resource library

   "WHAT YOU KEEP" matters most and is currently buried at the bottom of the
   list. The hero already promises "Your work remains yours" — group the
   features that deliver it under that promise.

5. SHORTEN THE BULLETS. Several run to three lines:

     before  "Full Toolbox: every interactive tool & canvas across strategy,
              research, product, GTM, financial, fundraising, cap table &
              team"
     after   "Full Toolbox — every canvas and calculator"   with the list
             on hover or in the comparison table

6. FREE EXPLORER NEEDS A CEILING STATED, not just a floor. Add one quiet
   line under its bullets so the boundary is honest before signup rather
   than discovered at mission 4:

     "Free Explorer covers missions 1-3. Missions 4-15 need the Sprint."

7. KEEP THE BADGE INSIDE THE CARD and reserve space for it in the grid — see
   PROMPT A rule 1. The ribbon currently escapes its card and lands on the
   control above it.
```

## PROMPT D — Page Structure

```text
PAGE: /pricing — section order, the promo box, the comparison table, the FAQ
and the proof.

THE PROBLEM

The promo code box sits ABOVE the plans, before a founder knows what they are
buying, and its button reads "Sign in to apply" — so the person looking at it
cannot use it. The most valuable space on the page delivers a dead end.

Meanwhile the strongest proof on the page — "Join 124+ MENA founders already
building with StartPad" — is roughly 10px of grey text in the hero. It is a
real, small, verifiable number, which is exactly the kind that earns trust,
and it is set where nobody will read it.

THE FIX

1. MOVE THE PROMO BOX. It belongs at checkout. If it must stay on this page,
   put it BELOW the comparison table as a single quiet line:

     "Have a promo or institution code?  Apply it at checkout."

   Never show an input whose only button asks the user to sign in. Either it
   works where it stands or it should not stand there.

2. SECTION ORDER:

     1  Hero — headline, one line of support, the founder count
     2  Country / currency row
     3  Three plan cards
     4  Cohort strip
     5  Compare plans
     6  Why the Sprint exists
     7  Proof — one founder quote
     8  Questions founders ask
     9  Promo line + legal footnote

3. RAISE THE FOUNDER COUNT. "124+ MENA founders are building with StartPad"
   as a readable line directly under the headline, at body size. And keep
   the real number — an exact small number is worth more than a rounded
   large one, especially to the people this page is written for.

4. ADD ONE FOUNDER QUOTE, between "Why the Sprint exists" and the FAQ. Real
   name, real company, real city, photo. One is enough. If there is no
   quotable founder yet, leave the section out entirely rather than filling
   it with a placeholder.

5. FIX THE COMPARISON TABLE. Nine of its eleven rows restate the card
   bullets. With a third plan it becomes genuinely useful — keep it, and:

     - Add the Team column
     - Replace "—" with "Not included". An em-dash reads as "unknown", and
       on a pricing page ambiguity is read as evasion
     - Keep "Mentor sessions — Paid per session: never gated" exactly as it
       is. Publishing that is unusual and it builds more trust than any
       feature row on the page
     - Make the header row sticky on scroll
     - On mobile, one plan column at a time with a segmented control, not a
       horizontally scrolling table

6. OPEN THE FIRST FAQ BY DEFAULT. "Is Founder Sprint a subscription?" is the
   question everyone has, and answering it without a click removes the
   anxiety that makes people leave.

   Keep "Does buying the Sprint mean my idea is validated?" — a pricing page
   that volunteers that question is doing something most do not, and the
   answer should stay as honest as the question.

7. ADD THE REFUND PROMISE ABOVE THE FOLD. There is a Refund Policy link in
   the footer and nothing near the buy button. One line under the Sprint
   CTA, stating the actual policy in plain words.

8. ACCESSIBILITY SWEEP ON THIS PAGE:
     - The small grey lines in the lime hero ("Free to explore · One payment
       for the Sprint · Your work remains yours") need checking at 4.5:1
       against the lime. Darken to near-black if they fail
     - Never lime text on white anywhere — 1.29:1, fails everything. Lime is
       a fill carrying near-black text
     - Every plan card is reachable and purchasable by keyboard, including
       the seat stepper, which needs arrow-key support
     - The country selector is a real combobox with a label, not a styled
       div
```

---

## Sequence

| # | Prompt | Why here |
|---|---|---|
| 1 | **A** — the currency control | The reported bug, and the FX rule that prevents payment disputes |
| 2 | **B** — the Team plan | Needs the grid fixed first; three cards also solve the empty margins |
| 3 | **C** — card layout and price | Applies to all three cards, so it comes after the third exists |
| 4 | **D** — page structure | Cheapest, and independent of the other three |

A is half a day. B is the one that adds revenue, and the product decision inside it — Team versus Cohort — matters more than the card.

---

## One decision, and one number to check

**Team or Cohort first?** I've specified Team as self-serve now and Cohort as a contact route. If most of your inbound is actually universities and incubators rather than co-founder pairs, invert it: make the cohort strip the third card with "Talk to us", and defer the seat stepper. The footer link and the existing FAQ both suggest institutions are already asking — your inbox will say which.

**The seat prices are mine, not yours.** $12 at 3+ seats and $10.50 at 10+ are sensible ladders off a $15 individual price, and they're in a config object so you can change them in one place. But check them against what a cohort actually costs you to support before publishing — a university buying 40 seats generates admin and support load that an individual founder does not.
