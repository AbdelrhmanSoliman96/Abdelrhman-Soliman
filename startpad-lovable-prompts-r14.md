# StartPad — Missions Redesign (Round 14, rebuilt against the live roadmap)

A full rework of the 15 missions' question set, mapped onto the mission names and phases that are actually shipping — plus 27 questions added to deepen the journey, and a downloadable artefact for every mission.

**What changed since the first version of this document.** I originally worked from `startpad15missions.docx`. Your roadmap screen shows a different, newer set of mission names and a different phase structure. This rebuild works from the roadmap as the source of truth, and the difference turns out to matter more than a renaming exercise — five missions have changed *intent*, and four of them are still asking the old mission's questions.

---

## The live structure

| Phase | # | Mission | XP |
|---|---|---|---|
| **Discover** | 1 | Problem Analysis | 100 |
| | 2 | Problem Definition | 100 |
| | 3 | Opportunity Prioritisation | 150 |
| **Shape** | 4 | Testable Problem Statement | 150 |
| | 5 | Solution Selection | 200 |
| | 6 | Value Proposition & Assumptions | 200 |
| **Test** | 7 | First Assumption Test | 250 |
| **Model** | 8 | Business Model Canvas | 300 |
| | 9 | Build a Learning Prototype | 300 |
| | 10 | Prototype User Test | 300 |
| **Readiness** | 11 | Go-to-Market Experiment | 300 |
| | 12 | Demand & Market Validation | 350 |
| | 13 | MVP Scope & Build | 400 |
| | 14 | Early Traction Review | 450 |
| | 15 | Launch & Incubator Readiness | 500 |

**4,050 XP total.** Five contiguous phases: 3 · 3 · 1 · 3 · 5.

Two things I raised as open questions last time are now answered by this screen, and both are answered well:

- **Phases are contiguous now.** Discover 1–3, Shape 4–6, Test 7, Model 8–10, Readiness 11–15. No more phase names repeating down the roadmap. Nothing to decide.
- **Mission 10 is already renamed** to "Prototype User Test". It no longer collides with Mission 7. That prompt is retired.

---

## The finding that matters most

**Four missions are asking questions that belong to a different mission.**

The names moved. The question set didn't. Here is the drift:

| # | Question set was written for | Mission is now called | Consequence |
|---|---|---|---|
| 11 | *Service Selection* — market size, channels, pricing, sales process, launch plan | **Go-to-Market Experiment** — "define a focused route-to-market test" | Asks for an entire GTM plan when the mission asks for one experiment |
| 14 | *Product-Market Fit Test* — "rate your product-market fit 1–10" | **Early Traction Review** — "interpret early usage **without claiming product-market fit too soon**" | The mission's description warns against the exact thing its own question demands |
| 15 | *Go to Market* — launch tactics, campaign spend, users acquired, revenue | **Launch & Incubator Readiness** — "turn launch evidence into a credible next-step story" | Collects activity metrics; the mission wants a narrative and an ask |
| 6 | *Idea Description* — value prop, features, benefits, differentiation | **Value Proposition & Assumptions** — "develop problem-solution canvas" | A named visual canvas is named in the description and rendered as text boxes |

Mission 14 is the one to fix first. A founder reads *"without claiming product-market fit too soon"* at the top of the mission, then question 5 asks them to score their product-market fit out of 10. That isn't a UX flaw, it's the mission contradicting itself — and it teaches the opposite of what the title is trying to teach.

Two smaller drifts:

- **Mission 4** was plural, *Problem Statements*. It is now **Testable Problem Statement** — singular, and the word *testable* is a requirement the questions never check.
- **Mission 9** was *Build Prototype*. It is now **Build a Learning Prototype** — and nothing asks what the prototype is meant to teach, which is the only thing that makes a prototype a *learning* prototype.

---

## The original diagnosis still stands

**87 questions across 15 missions. 75 of them are blank textareas.**

That is why your testers struggled, and it is why the industry question defeated people. A blank box asks the founder to invent both the *answer* and the *shape of the answer* at the same time. Nobody knows the shape of "what area are you interested in?" until they see a list.

Three structural problems, unchanged by the renaming:

**The same question is asked up to five times.** "Who is your user" appears in M1, M2 (twice), M4 and M11. "What are your next steps" appears in M9, M10, M13, M14 and M15. Nothing carries forward, so each mission feels like starting over instead of building on the last.

**Two missions are matrices collected as text fields.** M3 and M5 are 2×2 grids. Both are currently text boxes asking founders to type numbers between 1 and 10.

**Two missions are named canvases rendered as forms.** M8 is the nine-block Business Model Canvas as nine consecutive textareas. M6's description says "problem-solution canvas" and there is no canvas.

---

## The principle

**Structure the scaffolding. Never the content.**

A dropdown of industries doesn't tell a founder what their business is — it removes the burden of inventing a taxonomy from scratch. The thinking stays theirs. What changes is that their effort goes into *the answer* instead of into *working out what the answer should look like*.

Your point about mixed cases becomes a rule: **every category question is multi-select with an open "Other" escape.** Fintech *and* healthcare is a real answer. Subscription *and* commission is a real answer. A closed single-select would force a founder to lie about their own business.

---

## The input vocabulary

Eleven types. Everything below maps to one of these.

| Type | When to use | Example |
|---|---|---|
| `chips-multi` | A known set where combinations are real | Industry, channels, revenue models |
| `chips-single` | A known set where only one is true | Problem frequency, test method |
| `slider` | A 1–10 rating | Impact, frequency, value |
| `matrix` | Two scores plotted visually | M3 and M5 |
| `canvas` | A named visual framework | M6 and M8 |
| `builder` | A sentence with blanks to fill | Problem statement, hypothesis, value proposition |
| `repeater` | A list the founder adds rows to | Competitors, features, milestones |
| `number` | A quantity, with unit and currency | Market size, price, budget |
| `upload` | File, link, or pasted text | Prototype, survey export, ad screenshot |
| `text` | One short line | A name, a link, a date |
| `textarea` | Genuinely open reflection | "What don't these numbers tell you?" |

**Every question can carry an attachment.** A founder answering a chip question may still want to attach the survey export. That's your "some answers need to upload documents" — handled as a property of every question, not as a separate question type.

**Every chip list ends with "Other →"**, which opens a text field and stores what they typed. No list is ever closed, and after a few hundred founders you'll know exactly which options your taxonomies are missing.

---

## The 15 missions, redesigned

Legend: **↩** = carried forward from an earlier mission, pre-filled and editable. **NEW** = a question that doesn't exist today.

---

### Phase: Discover

#### Mission 1 — Problem Analysis · 100 XP

| # | Question | Now | Becomes |
|---|---|---|---|
| 1 | Which areas interest you? | text | **`chips-multi`** — Fintech · Healthtech · Edtech · E-commerce · Logistics · Agritech · Proptech · Food & beverage · Travel · Media · Gaming · B2B software · Marketplace · Climate · Fashion · Fitness · HR · Legal · Insurance · Manufacturing · Energy · Other → |
| 2 | A problem you've observed | textarea | **`builder`** — "I noticed that ___ struggle with ___ when ___" + optional detail + optional photo |
| 3 | Who is affected? | text | **`chips-multi`** — Students · Young professionals · Small business owners · Freelancers · Parents · Farmers · Drivers · Patients · Teachers · Retailers · Other → — plus one line of specifics |
| 4 | What already exists? | textarea | **`repeater`** — name · link · one line on what it does |
| 5 | Where do they fall short? | textarea | **`chips-multi`** — Too expensive · Too slow · Hard to use · Not available here · Poor quality · Needs expertise · No offline mode · No Arabic · Other → — then expand |

Question 1 is the one your testers named. The 22-chip list doesn't tell anyone what industry they're in; it shows them that "fintech + healthtech" is a legitimate answer, which a single text box never does.

#### Mission 2 — Problem Definition · 100 XP

| # | Question | Becomes |
|---|---|---|
| 1 | Your primary user | **`builder`** — "[age range] [role] in [city/country] who [context]", each blank a chip set |
| 2 | Key characteristics | **`chips-multi`** — income band · tech comfort · buying power · where they spend time |
| 3 | The problem they face | ↩ **from M1 Q2**, editable — *"You said this in Mission 1. Sharpen it now that you know who you're talking about."* |
| 4 | When and where does it happen? | **`chips-multi`** — At work · At home · Commuting · Shopping · Studying · Online · In person · Other → |
| 5 | How often? | **`chips-single`** — Many times a day · Daily · Weekly · Monthly · A few times a year · Once |

#### Mission 3 — Opportunity Prioritisation · 150 XP

**Replace all seven fields with one interactive matrix.** The mission description already names the axes: *impact and frequency*.

Problems from Missions 1 and 2 arrive as draggable cards. The founder drags each onto the grid, or moves two sliders and watches the card move. A `repeater` adds more. Then `chips-single` picks the focus problem from those actually plotted, plus one line on why.

Quadrants are labelled so the exercise **teaches** rather than merely collects:

| | Low frequency | High frequency |
|---|---|---|
| **High impact** | Big bets | **Fix first** |
| **Low impact** | Park it | Quick wins |

3 inputs, down from 7 fields.

---

### Phase: Shape

#### Mission 4 — Testable Problem Statement · 150 XP

| # | Question | Becomes |
|---|---|---|
| 1 | The statement | **`builder`** — "[User] needs a way to [job] because [insight]. Today they [workaround], which costs them [impact]." |
| 2 | Who specifically? | ↩ **from M2 Q1** |
| 3 | What is the impact? | **`number` + unit** (money / hours / times per week) + `chips-multi` impact type + short note |
| 4 | How would you know it's solved? | **`repeater`** — metric · today's value · target value |
| 5 | **What would prove this statement wrong?** | **NEW · `text`** — one line. The mission is called *Testable*; nothing currently tests that. A statement you cannot falsify isn't a hypothesis, it's a belief — and this single line is what makes Mission 7 possible. |

#### Mission 5 — Solution Selection · 200 XP

**Same treatment as Mission 3.** A `repeater` of ideas, two sliders each, plotted live on a labelled 2×2. Then pick one, and one line on why.

**One thing to decide.** The roadmap calls this a *value/impact* matrix. Value and impact measure nearly the same thing, so every idea lands on a diagonal and the grid stops discriminating. The version that does useful work is **Value × Effort**:

| | Low effort | High effort |
|---|---|---|
| **High value** | **Do now** | Plan it |
| **Low value** | Quick win | Drop it |

If you want to keep the "value/impact" wording on the roadmap, the second axis should still be effort — relabel the description rather than the axis. Flagging it rather than silently changing it.

#### Mission 6 — Value Proposition & Assumptions · 200 XP

**The mission description says "problem-solution canvas". Render one.** Same treatment as Mission 8: a visual layout with tappable blocks, not a stack of text boxes.

| Block | Input |
|---|---|
| Customer segment | ↩ from M2 |
| Problem / pains | ↩ from M4 |
| Existing alternatives | ↩ from M1 Q4 |
| Gains — what "better" looks like | **`chips-multi`** — Cheaper · Faster · Less effort · More reliable · Available locally · In Arabic · More trusted · New capability · Other → |
| Your solution | **`textarea`** — genuinely open, and one of the few that should be |
| Value proposition | **`builder`** — "For [user] who [need], [name] is a [category] that [benefit]. Unlike [alternative], we [difference]." |
| Key features | **`repeater`** — feature + the benefit it delivers |
| **Assumptions** | **`repeater`** — assumption + `chips-single` risk (High / Medium / Low), auto-sorted riskiest first. This list is the direct input to Mission 7. |

The old Q3 ("what benefits will users get") is **removed** — it asked the same thing as the features question. Merged into a two-column repeater.

---

### Phase: Test

#### Mission 7 — First Assumption Test · 250 XP

The title says *First Assumption Test*, singular. The mission should be about testing **one** thing properly, not designing a research programme.

| # | Question | Becomes |
|---|---|---|
| 1 | Which assumption are you testing? | **`chips-single`** from **↩ the M6 assumption list**, sorted riskiest first. Pre-selects the top one with *"This is your riskiest assumption. Test this one unless you have a reason not to."* |
| 2 | Your hypothesis | **`builder`** — "We believe [user] will [action] because [reason]. We'll know we're right if [signal]." |
| 3 | How will you test it? | **`chips-single`** — Interviews · Survey · Landing page · Fake door · Concierge · Wizard of Oz — **each with one line explaining what it actually is**, because most first-time founders have not met these words |
| 4 | What result would prove it? | **`number`** threshold — "at least ___ out of ___ do ___" — set **before** running the test |
| 5 | What happened? | **`upload`** (survey export, notes, screenshots) + **`number`** actual result |
| 6 | What did you learn? | **`textarea`** + **`chips-single`** verdict: Confirmed · Contradicted · Inconclusive. *Inconclusive is a valid, respected answer* — say so in the helper text, or founders will fabricate a verdict. |

---

### Phase: Model

#### Mission 8 — Business Model Canvas · 300 XP

**Render the actual canvas.** Nine blocks in the real BMC layout. Tapping a block opens a focused editor; the canvas fills in visually behind it, with a "4 of 9 blocks" indicator.

| Block | Input |
|---|---|
| Value Propositions | ↩ from M6 |
| Customer Segments | ↩ from M2 |
| Channels | **`chips-multi`** — Own website · App store · Instagram · TikTok · WhatsApp · Resellers · Direct sales · Marketplace · Physical shop · Other → |
| Customer Relationships | **`chips-multi`** — Self-serve · Personal support · Community · Automated · Dedicated account · Other → |
| **Revenue Streams** | **`chips-multi`** — Subscription · One-time sale · Commission · Freemium · Advertising · Licensing · Marketplace fee · Usage-based · Other → **Multi-select matters most here.** Mixed revenue models are normal, and a single text box hides that completely. |
| Key Resources | `chips-multi` + repeater for specifics |
| Key Activities | `repeater` |
| Key Partnerships | **`repeater`** — partner + what they provide |
| Cost Structure | **`repeater`** — cost line + amount + currency, with a running monthly total |

Every block carries a one-line explanation. Most founders meeting the canvas for the first time do not know what "Key Activities" means.

#### Mission 9 — Build a Learning Prototype · 300 XP

| # | Question | Becomes |
|---|---|---|
| 1 | **What is this prototype meant to teach you?** | **NEW · `builder`** — "I want to find out whether ___". Offers ↩ the assumptions from M6 that Mission 7 did *not* test. **This is what makes it a *learning* prototype**, and it currently isn't asked at all. It goes first, before any tooling question. |
| 2 | What kind of prototype? | **`chips-single`** — Paper sketch · Clickable design · No-code app · Landing page · Slide walkthrough · Coded · Other → |
| 3 | Which features are in it? | ↩ **features from M6** as checkboxes — "which made it into the prototype?" |
| 4 | Built with | **`chips-multi`** — Figma · Canva · Bubble · Webflow · Glide · FlutterFlow · Adalo · Framer · Paper · Other → |
| 5 | The key flows | **`repeater`** — step by step |
| 6 | The prototype itself | **`upload`** — link or file. **Required.** |

*Roadmap copy note:* the card currently reads "Create prototype or Figma design". Naming one vendor in mission copy suggests Figma is expected. "Clickable prototype — Figma, Canva, or paper" is truer and less intimidating.

#### Mission 10 — Prototype User Test · 300 XP

| # | Becomes |
|---|---|
| 1 | **`number`** — how many people tested it. Under 5, show a quiet note: *"Fewer than 5 testers rarely reveals a pattern. It's still worth logging."* |
| 2 | **`chips-single`** — In person · Video call · Unmoderated · Group session |
| 3 | **`repeater`** — findings, each tagged `chips-single`: Confirmed · Contradicted · Surprising |
| 4 | **`upload`** notes or recordings + a short summary |
| 5 | **`repeater`** — changes to make, each with a priority chip |
| 6 | ↩ **back-reference to M9 Q1** — *"You built this to find out whether [X]. Did you?"* — `chips-single` Yes / No / Not yet |

---

### Phase: Readiness

#### Mission 11 — Go-to-Market Experiment · 300 XP · **respecified**

The current questions ask for market size, all channels, pricing, a sales process and a launch plan — a full go-to-market **plan**. The mission asks for a focused **test**. Those are different exercises, and the plan questions belong in Mission 12.

| # | Question | Becomes |
|---|---|---|
| 1 | Which single route are you testing? | **`chips-single`** — Instagram · TikTok · WhatsApp groups · LinkedIn · Facebook groups · Google Ads · SEO · Influencers · Events · University campus · Referral · Cold outreach · Reseller · Other → **One only**, with helper text: *"You can test more later. Testing five at once tells you nothing about any of them."* |
| 2 | Exactly who will you reach? | ↩ **from M2**, narrowed — one segment, not the whole market |
| 3 | What will you put in front of them? | **`builder`** for the offer line + **`upload`** for the ad, landing page or message |
| 4 | What counts as success? | **`chips-single`** metric (sign-ups · replies · pre-orders · waitlist joins · clicks · meetings booked) + **`number`** threshold — *set before you run it* |
| 5 | Budget and timebox | **`number` + currency** + **`number`** days |
| 6 | What happened? | **`number`** actual + **`upload`** evidence + **`textarea`** why you think so + **`chips-single`** verdict: Worth repeating · Worth changing · Worth dropping |

#### Mission 12 — Demand & Market Validation · 350 XP

Absorbs the market-sizing and pricing questions that were stranded in Mission 11.

| # | Becomes |
|---|---|
| 1 | **`chips-multi`** — validation methods used |
| 2 | **`repeater`** — demand indicator + value |
| 3 | **`repeater`** — competitor table: name · link · price · one strength · one weakness |
| 4 | **`chips-single`** pricing model + **`number` + currency** price point + **`chips-single`** willingness-to-pay response *(moved from old M11 Q3)* |
| 5 | **`number` × 3** — TAM / SAM / SOM with currency, plus **`textarea`** "how did you get to this number?" and a **bottom-up helper**: users × price × frequency, calculated live *(moved from old M11 Q1)* |
| 6 | **`chips-single`** verdict — Strong demand · Mixed signals · Weak demand — + one line |

#### Mission 13 — MVP Scope & Build · 400 XP

The word **Scope** is in the title and nothing currently scopes anything.

| # | Question | Becomes |
|---|---|---|
| 1 | **What's in, what's out?** | **NEW · two-column sorter** — every feature from M6 and M9 arrives as a card; the founder drags each into **"In the MVP"** or **"Not yet"**. **The highest-value new question in the whole set**: it makes cutting scope a visible, deliberate act instead of something that happens by accident three weeks into building. |
| 2 | Why those cuts? | **`text`** — one line |
| 3 | How will you build it? | **`chips-multi`** — No-code: Bubble / Glide / Softr / Webflow · Code: React / Next / Flutter / Laravel / Django / Node · Backend: Supabase / Firebase / AWS · Other → |
| 4 | How long? | **`number` + unit** — days or weeks |
| 5 | What got in the way? | **`chips-multi`** challenge types + a line |
| 6 | The MVP | **`upload`** — link. **Required.** |
| 7 | Can someone use it end to end? | **`chips-single`** Yes / Almost / Not yet → if not, a `repeater` of blockers |

#### Mission 14 — Early Traction Review · 450 XP · **respecified**

The mission description is *"interpret early usage without claiming product-market fit too soon"*. Every question below serves that sentence. The 1–10 self-rating is removed — it is the exact behaviour the mission exists to prevent.

| # | Question | Becomes |
|---|---|---|
| 1 | The numbers | **metric grid** — sign-ups · activated · returned in week 1 · returned in week 4 — plus **how many weeks of data** and **sample size**. Every later question is read against these two. |
| 2 | Retention | **calculated, not typed** — derived from the grid, with the arithmetic shown. Founders currently type a percentage; typed percentages are guesses. |
| 3 | **What do these numbers *not* tell you?** | **NEW · `textarea`** — the mission's whole thesis in one question |
| 4 | **What might be inflating this?** | **NEW · `chips-multi`** — Friends and family · Paid promotion · A one-off event · Press mention · Discount or incentive · Nothing I can see. **This is the anti-overclaim guard**, and it costs a founder ten seconds to answer honestly. |
| 5 | Evidence from users | **`upload`** + *optional* Sean Ellis result: ask users *"how would you feel if you could no longer use this?"* and enter the % who say **very disappointed**. Guarded: *"Needs 30+ responses to mean anything. 40% is the recognised threshold — and it's a signal, not a verdict."* |
| 6 | What you'll change next | **`repeater`** with priority |

**And remove the PMF score from the UI.** Anywhere the platform shows a product-market-fit number, replace it with **evidence strength — thin · early · promising**, computed from sample size and observation window, never from self-rating. A founder cannot award themselves product-market fit, and the platform shouldn't offer them a field in which to try.

#### Mission 15 — Launch & Incubator Readiness · 500 XP · **respecified**

Currently asks for launch tactics, campaign spend, users acquired and revenue — activity metrics. The mission asks the founder to *turn launch evidence into a credible next-step story*. That's a narrative task with an ask at the end, and the questions should build it.

| # | Question | Becomes |
|---|---|---|
| 1 | What did you launch, and when? | **`text`** + date + **`upload`** link |
| 2 | Your evidence pack | **auto-assembled** from Missions 3, 4, 7, 10, 11, 12 and 14 — the problem, the user, the assumption test, the prototype test, the GTM experiment, the demand evidence, the traction. Founder reviews, edits and adds. *Nothing is retyped.* |
| 3 | The story in one paragraph | **`builder`** — "In [time period] we [did this], which produced [result]. That tells us [insight], so next we will [step]." Replaces a blank box with the structure of a credible claim. |
| 4 | What are you asking for? | **`chips-single`** — Incubator or accelerator place · Pre-seed investment · Grant · Pilot customer · Co-founder · Not raising yet — + **`number` + currency** if funding |
| 5 | The next 90 days | **`repeater`** — milestone · date · who owns it |
| 6 | **Risks you'd name yourself** | **NEW · `repeater`** — risk + how you'd mitigate it. Every incubator panel asks this. A founder who has named their own risks reads as credible; one who hasn't reads as unprepared. |
| 7 | Generate the readiness pack | **branded PDF export** using the Round 11 template, assembling every mission's output into one document the founder can send |

---

## Questions worth adding

You asked whether we can add questions inside the same missions to raise the quality of the journey. Yes — and there's room, because the redesign above removed most of the *typing*, not the thinking. A chip question costs a founder 15 seconds; the blank box it replaced cost three minutes.

Below are 27 additions. None of them is padding: each one closes a gap that currently lets a founder finish a mission without having done the thinking the mission is for. **Priority 1** means the journey is weaker without it. **Priority 2** is real value you could defer.

| # | Mission | New question | Type | Why it earns its place | P |
|---|---|---|---|---|---|
| 1 | M1 Problem Analysis | **How do you know this problem is real?** — I've experienced it · I watched someone deal with it · I've talked to people about it · I read about it · I have data · It's a hunch | `chips-multi` | Sets the evidence culture in the first mission instead of the seventh, and gives the AI reviewer a calibration signal from minute one. "It's a hunch" must be a permitted answer — that's the honest starting point for most people | 1 |
| 2 | M1 | **Why you?** — I've lived this problem · I work in this industry · I have a relevant skill · I know these customers · I'm just interested | `chips-multi` + line | Founder–problem fit. Asked here, it's a warm-up; it becomes the first line of the Mission 15 story | 2 |
| 3 | M2 Problem Definition | **Who is *not* your user?** | `text` | One line, and it sharpens a segment more than any positive question. "Everyone" stops being answerable | 1 |
| 4 | M2 | **How do they solve it today?** — Manually · Spreadsheet · WhatsApp · A competitor's app · They pay someone · They don't | `chips-multi` | The real competitor is usually a spreadsheet, not a company. This surfaces it early and feeds Mission 12 | 1 |
| 5 | M3 Opportunity Prioritisation | **Roughly how many people have this problem?** + how confident are you | `number` + `chips-single` | Plants market sizing at the point it's cheap, so Mission 12's TAM isn't invented from nothing | 2 |
| 6 | M3 | **What did you decide *not* to work on, and why?** | `text` | Turns a ranking into a decision. Founders who can name what they dropped defend their focus better | 1 |
| 7 | M4 Testable Problem Statement | **Who would pay to have this solved — the user, or someone else?** — The user · Their employer · A government body · An advertiser · A platform · Not sure yet | `chips-single` | Payer ≠ user is the most common blind spot in the region's B2B and B2G ideas, and it stays hidden until Mission 8 asks for revenue streams. Ask it here | 1 |
| 8 | M5 Solution Selection | **What's the simplest version that would still help someone?** | `text` | The anti-scope-creep question. Its answer is the default MVP scope in Mission 13 | 1 |
| 9 | M5 | **What would have to be true for this to work?** | `repeater` | Seeds the Mission 6 assumption register instead of asking a founder to conjure assumptions from a blank page | 1 |
| 10 | M6 Value Prop & Assumptions | **If your riskiest assumption is wrong, what happens?** | `text` | Makes risk concrete. A founder who writes "the whole business doesn't work" has just found what Mission 7 must test | 1 |
| 11 | M7 First Assumption Test | **Who did you test with, and how did you find them?** — Friends and family · My network · Cold outreach · A community or group · Existing users · Recruited/paid | `chips-multi` | Sampling bias is invisible unless you ask. Ten friends saying yes is not evidence, and the reviewer can only say so if it knows | 1 |
| 12 | M7 | **What surprised you?** | `text` | The single most useful sentence in any test write-up, and it's never volunteered unless asked | 2 |
| 13 | M8 Business Model Canvas | **Unit economics** — price · cost to serve one customer · gross margin (calculated) | `number` grid | A business model canvas with no unit economics is a poster. Three numbers and one calculation make it a model | 1 |
| 14 | M8 | **Which block are you least sure about?** | `chips-single` from the nine | Names the next thing to test, and gives the platform something intelligent to recommend | 2 |
| 15 | M9 Learning Prototype | **What did you deliberately leave out?** | `text` | Pairs with the scope sorter in Mission 13 and makes omission a decision rather than an oversight | 2 |
| 16 | M9 | **What's the first thing a tester will see?** | `text` | Thirty seconds decides most prototype tests. Founders rarely plan the opening | 2 |
| 17 | M10 Prototype User Test | **Where did people get stuck?** — step · what happened | `repeater` | The findings list captures conclusions; this captures the moments. Directly actionable for Mission 13 | 1 |
| 18 | M10 | **What did you change your mind about?** | `text` | A test that changed nothing usually wasn't a test | 2 |
| 19 | M11 GTM Experiment | **What did one result cost you?** — budget ÷ results | calculated | The founder's first cost-per-acquisition number, free, from data they've already entered | 1 |
| 20 | M11 | **Could you do this ten times over?** — Yes easily · Yes with money · Yes with more people · No | `chips-single` | Separates a channel from a one-off favour. Most first GTM wins don't survive this question | 1 |
| 21 | M12 Demand & Market Validation | **How many said yes but didn't actually do anything?** | `number` + line | The say/do gap. The most important validation question there is, and it appears nowhere in the journey today | 1 |
| 22 | M12 | **What would make you walk away from this market?** | `text` | A founder who can't answer this will never stop, which is a worse outcome than stopping | 2 |
| 23 | M13 MVP Scope & Build | **What's the one thing it has to do well?** | `text` | Forces a single quality bar into a build that's otherwise a feature list | 1 |
| 24 | M13 | **How will you know someone actually used it?** — Analytics installed · Database records · I'll ask them · I'll watch · Not set up yet | `chips-multi` | Founders launch with no instrumentation and then cannot answer a single Mission 14 question. Asking here, one mission earlier, is the difference between having data and guessing | 1 |
| 25 | M14 Early Traction Review | **Which single number will you try to move next month, and to what?** | `chips-single` + `number` | Converts a review into a commitment, and gives Mission 15 something to report against | 1 |
| 26 | M15 Launch & Incubator Readiness | **What do you need that you don't have?** — Money · A co-founder · Technical help · Customers · Mentorship · Licensing or legal · Nothing right now | `chips-multi` | The honest version of "what's your ask", and it routes straight into mentoring, the community and the collaboration hub | 1 |
| 27 | M15 | **Runway** — cash available · monthly burn · months remaining (calculated) | `number` grid | Every incubator asks. A founder who has never calculated it finds out in the room, which is the worst place | 2 |

**Cost to the founder:** 27 questions, of which 21 are chips, one-liners or calculated fields. Realistically 8–12 minutes added across a journey that spans weeks. **17 are Priority 1**; if you want a smaller first pass, ship those and hold the rest.

Two ground rules for the additions:

- **None of them may block submission on their own.** They enrich the rubric; they don't become new ways to fail a mission. The Round 11 quality gate stays attached to the substantive questions only.
- **Every one of them feeds something later.** That's the test I applied — an added question that doesn't carry forward into a later mission or an export is a question that made the journey longer without making it better.

---

## Missions that should produce a downloadable artefact

This is the change that alters how the journey *feels*. Right now a mission ends in a score. It should end in **something the founder owns** — a canvas, a report, a one-pager they can send to a co-founder, a lecturer, an incubator or an investor.

Every mission produces one. Nine of them are genuinely worth downloading.

| # | Mission | Artefact | Formats |
|---|---|---|---|
| 1 | Problem Analysis | Problem landscape — the problem, who it affects, what exists today and where it falls short | PDF |
| 2 | Problem Definition | **User persona card** — the segment, characteristics, context, frequency | PDF · PNG |
| 3 | Opportunity Prioritisation | **Impact × Frequency matrix** with every problem plotted and quadrants labelled | PNG · PDF |
| 4 | Testable Problem Statement | Problem statement card — statement, impact, success metrics, falsification test | PDF · PNG |
| 5 | Solution Selection | **Value × Effort matrix** with every idea plotted | PNG · PDF |
| 6 | Value Prop & Assumptions | **Problem–solution canvas** + assumption register | PDF · PNG · CSV *(register)* |
| 7 | First Assumption Test | **Experiment report** — hypothesis, method, threshold set beforehand, result, verdict, what changed | PDF |
| 8 | Business Model Canvas | **The Business Model Canvas** — full landscape layout, all nine blocks, plus the unit economics sheet | **PDF A3 + A4 · PNG · XLSX** |
| 9 | Learning Prototype | Prototype brief — what it tests, what's in it, the flows, the link | PDF |
| 10 | Prototype User Test | Usability findings — testers, method, findings tagged, where people got stuck, changes | PDF |
| 11 | GTM Experiment | Channel experiment card — route, offer, threshold, result, cost per result, verdict | PDF · PNG |
| 12 | Demand & Market Validation | Market validation report + **competitor comparison table** + TAM/SAM/SOM chart | PDF · XLSX |
| 13 | MVP Scope & Build | **MVP scope sheet** — in / out, with the reasoning | PDF · XLSX |
| 14 | Early Traction Review | **Metrics one-pager** — funnel, retention curve, evidence strength, confounders named, next target | **PDF · PNG · XLSX** |
| 15 | Launch & Incubator Readiness | **The Readiness Pack** — every artefact above, assembled, with the story and the ask | **PDF · PPTX** |

Three of these are the ones you named, and they're the three that matter most:

**The Business Model Canvas (M8)** is the artefact founders show people. It has to be a real landscape canvas at A3 — the size it's meant to be printed and pinned — with an A4 fallback, and a PNG for putting in a deck.

**The metrics one-pager (M14)** is the artefact investors and incubators ask for. It should render the funnel and the retention curve as actual charts from the founder's own numbers, and — this is the part that makes it StartPad's rather than generic — it prints the confounders the founder named alongside the numbers. A traction sheet that says "1,200 sign-ups (paid promotion, one-off event)" is worth more than one that says "1,200 sign-ups", and it teaches the founder what honest reporting looks like.

**The Readiness Pack (M15)** is the whole journey as one sendable document. It's also the strongest retention argument the product has: fifteen missions of work becomes a thing you can hand to someone.

**Every export carries the brand.** The logo, the founder's name, the mission, the date, and a quiet "Made on StartPad · startpad.me" footer — which is the cheapest distribution the platform has, because these documents get forwarded. That uses the branded PDF template from Round 11.

**One decision for you.** Exports are an obvious Pro-tier lever — free founders could see the artefact and get a watermarked or preview version, with clean, brand-free download on Pro. That's a real revenue argument. It's also a real goodwill cost, and the Round 12 sweep set missions 1–3 as the free tier. My recommendation: **let everyone download everything, keep the StartPad footer on every export, and don't gate it.** The forwarding is worth more than the upgrades, and a founder who can't download their own canvas will screenshot it anyway. But it's your call, and it changes what gets built.

---

## What this changes, in numbers

| | Before | After |
|---|---|---|
| Questions | 87 | **114** (87 rebuilt + 27 added) |
| Blank textareas | 75 | **9** |
| Answerable by tapping | 0 | ~55 |
| Calculated fields — the founder never types a number they already gave you | 0 | 6 |
| Carried forward from an earlier mission | 0 | **13** |
| Visual/interactive exercises | 0 | **5** (two matrices, two canvases, one scope sorter) |
| Downloadable artefacts | 0 | **15** |
| Duplicate questions | 12 | 0 |
| Questions asking for something the mission's own description warns against | 1 | 0 |

More questions. Far less work. The 27 additions are chips and one-liners; the 75 textareas they sit alongside are gone.

The nine that stay open are the ones that *should* be: M1's problem detail, M6's solution description, M7's "what did you learn", M10's test summary, M11's "why do you think that happened", M12's "how did you get to this number", M13's "why those cuts", M14's "what don't these numbers tell you", M15's evidence notes. Reflection deserves a blank page. Categorisation doesn't.

The thirteen carried-forward fields:

```
M2 Q3   ← M1 Q2      problem statement
M3 cards← M1, M2     problems to prioritise
M4 Q2   ← M2 Q1      the user
M6      ← M2, M4, M1 Q4   segment, pains, alternatives
M7 Q1   ← M6         riskiest assumption
M8 VP   ← M6         value proposition
M8 seg  ← M2         customer segments
M9 Q1   ← M6, M7     untested assumptions
M9 Q3   ← M6         features
M10 Q6  ← M9 Q1      did the prototype answer its question?
M11 Q2  ← M2         narrowed segment
M13 Q1  ← M6, M9     features to scope
M15 Q2  ← M3,4,7,10,11,12,14   the evidence pack
```

---

## The roadmap screen itself

Seven notes on the screen you sent, since it's what a founder meets first.

1. **Fourteen of fifteen cards are grey and padlocked.** A new founder's first impression of the journey is a wall of locked doors. Show the first card of each phase in full colour with its phase accent, even while locked — the founder should be able to see the shape of the journey, not just its gate.
2. **No lock says how to unlock it.** Add one line per locked card: *"Unlocks after Problem Definition."* A lock with no condition reads as a paywall, especially now that pricing exists.
3. **The phase progress bars are empty grey pills.** They read as decoration. Give them a number — "0 of 3" — or drop them, since the header already says "0/3 missions".
4. **Spelling is inconsistent inside a single card.** "Opportunity Prioriti**s**ation" with the description "Priorit**iz**e problems based on impact and frequency". Pick one — British matches the title — and sweep every mission title, description and locale string.
5. **"Create prototype or Figma design"** names a vendor in mission copy. "Clickable prototype — Figma, Canva, or paper" is truer and lowers the barrier.
6. **XP is visible on locked missions, which is right** — a founder can see that Mission 15 is worth 500 and that the journey escalates. Consider showing the phase XP subtotal on each phase header too (Discover 350 · Shape 550 · Test 250 · Model 900 · Readiness 2,000).
7. **Mission 7 sits alone in a phase called Test.** One mission, 250 XP, between two three-mission phases. It's fine structurally — the assumption test genuinely is its own gate — but the card looks stranded. Give that phase a one-line explanation on the header: *"One test. The riskiest thing you believe."*

---
---

# The prompts

Eight, in build order. Paste one per message.

## PROMPT A — Build the Question Type System

```text
PAGE: All mission question screens (/missions/:id), plus the shared component
library.

THE PROBLEM

The 15 missions use 87 questions, of which 75 are blank textareas. Testers
could not answer basic questions — for example "what area are you interested
in?" — not because the question is hard, but because a blank box asks the
founder to invent the answer AND the shape of the answer at the same time.

THE FIX

Before changing any mission content, build the input component system the new
question set needs. Eleven reusable types, driven by a schema so mission
content is data, not JSX.

  chips-multi   Tappable pills, multi-select, always ending with "Other →"
                which opens a text field. Selected state uses lime background
                with near-black text (never lime text on white — it fails
                contrast at 1.29:1). Minimum 44px tap targets. Wraps on mobile.
  chips-single  Same, single selection.
  slider        1-10, ends labelled in words, current value shown large.
                Draggable and keyboard-accessible.
  matrix        A 2x2 grid. Cards dragged onto it, or positioned by two
                sliders. Quadrants labelled. See PROMPT E.
  canvas        A named-framework layout with tappable blocks. See PROMPT F.
  builder       A sentence with inline blanks. Each blank is either a chip set
                or a short input. The finished sentence reads back as prose.
  repeater      "Add another" rows. Each row is a mini-form defined per
                question. Rows reorderable and deletable.
  number        Numeric input with a unit selector, and a currency selector
                where relevant (EGP, SAR, AED, USD).
  upload        File, URL, or pasted text — all three accepted. Shows what was
                attached. Existing OCR applies.
  text          One short line.
  textarea      Long-form. Keeps the existing submission gate.

RULES FOR ALL TYPES

1. EVERY QUESTION CAN CARRY AN ATTACHMENT, whatever its type. A founder
   answering a chip question may still want to attach a screenshot or a
   document. Put a quiet "Add file or link" affordance on every question, not
   only on the ones that ask for evidence.

2. NO CHIP LIST IS EVER CLOSED. "Other →" is mandatory on every chips-multi
   and chips-single, and what the founder types there is stored, so you can
   later see which options your taxonomies are missing.

3. MULTI-SELECT IS THE DEFAULT for categories. A founder building in fintech
   AND healthtech is not an edge case, and neither is a business running
   subscription AND commission revenue. Use chips-single only where exactly
   one answer can be true (frequency, test method, verdict).

4. SCHEMA-DRIVEN. Each question is a record:
     { id, missionId, phase, order, type, label, helpText, whyItMatters,
       options[], allowOther, required, minWords, carriesFrom,
       attachmentAllowed, exampleAnswerId }
   Mission content lives in that schema. Never hardcode a question inside a
   component.

5. ARABIC. Every type works RTL and is labelled in both languages. Chip labels
   especially — a chip set is only faster than typing if the founder reads it
   instantly in their own language.

6. MOBILE FIRST. This is where missions get answered. Chips beat typing on a
   phone, which is most of the point of this change.
```

## PROMPT B — Realign Missions 11, 14 and 15 to Their Own Names

```text
PAGE: /missions/11, /missions/14, /missions/15 — and the mission schema.

THE PROBLEM

The mission names on the roadmap were updated. The questions inside them were
not. Three missions now ask for something other than what their own title and
description promise, and one of them contradicts itself outright.

  MISSION 14 "Early Traction Review"
    Description: "Interpret early usage without claiming product-market fit
    too soon."
    Question 5: "Rate your product-market fit from 1 to 10."
    The mission warns against the exact thing its own question demands.

  MISSION 11 "Go-to-Market Experiment"
    Description: "Define a focused route-to-market test."
    Questions ask for target market size, all channels, pricing, a sales
    process and a launch plan — an entire GTM plan, not one experiment.

  MISSION 15 "Launch & Incubator Readiness"
    Description: "Turn launch evidence into a credible next-step story."
    Questions collect launch tactics, campaign spend, users acquired and
    revenue — activity metrics, not a story and not an ask.

THE FIX

MISSION 14 — Early Traction Review

  Delete the 1-10 self-rating entirely. Replace the question set with:

  Q1  Metric grid: sign-ups, activated, returned week 1, returned week 4.
      PLUS two required context fields — how many weeks of data, and total
      sample size. Every other answer is read against these two.
  Q2  Retention: CALCULATED from Q1, not typed, with the arithmetic shown.
      Typed percentages are guesses.
  Q3  NEW textarea: "What do these numbers NOT tell you?"
  Q4  NEW chips-multi: "What might be inflating this?" — Friends and family ·
      Paid promotion · A one-off event · Press mention · Discount or incentive
      · Nothing I can see. This is the anti-overclaim guard.
  Q5  Upload user evidence. Optional Sean Ellis result — ask users "how would
      you feel if you could no longer use this?" and enter the % who answer
      "very disappointed". Show the guard text: "Needs 30+ responses to mean
      anything. 40% is the recognised threshold — and it is a signal, not a
      verdict."
  Q6  Repeater: what you'll change next, with priority.

  AND REMOVE THE PMF SCORE FROM THE UI EVERYWHERE. Wherever the platform
  displays a product-market-fit number, replace it with EVIDENCE STRENGTH —
  thin / early / promising — computed from sample size and observation window,
  never from self-rating. Founders cannot award themselves product-market fit
  and the platform should not offer a field in which to try.

MISSION 11 — Go-to-Market Experiment

  Q1  chips-single, ONE route only: Instagram · TikTok · WhatsApp groups ·
      LinkedIn · Facebook groups · Google Ads · SEO · Influencers · Events ·
      University campus · Referral · Cold outreach · Reseller · Other →
      Helper: "You can test more later. Testing five at once tells you nothing
      about any of them."
  Q2  Carried from Mission 2, narrowed: exactly who will you reach.
  Q3  builder for the offer line + upload the ad, landing page or message.
  Q4  chips-single success metric (sign-ups · replies · pre-orders · waitlist
      joins · clicks · meetings booked) + number threshold, set BEFORE running.
  Q5  number + currency budget, number of days timebox.
  Q6  number actual result + upload evidence + textarea why + chips-single
      verdict: Worth repeating / Worth changing / Worth dropping.

  MOVE the market-sizing and pricing questions OUT of Mission 11 and INTO
  Mission 12, where they belong — that is the demand and market mission.

MISSION 15 — Launch & Incubator Readiness

  Q1  What did you launch, and when — text + date + upload link.
  Q2  EVIDENCE PACK, auto-assembled from Missions 3, 4, 7, 10, 11, 12 and 14:
      the problem, the user, the assumption test, the prototype test, the GTM
      experiment, the demand evidence, the traction numbers. The founder
      reviews, edits and adds. NOTHING IS RETYPED.
  Q3  builder: "In [time period] we [did this], which produced [result]. That
      tells us [insight], so next we will [step]."
  Q4  chips-single, the ask: Incubator or accelerator place · Pre-seed
      investment · Grant · Pilot customer · Co-founder · Not raising yet.
      Plus number + currency if funding.
  Q5  repeater, next 90 days: milestone · date · owner.
  Q6  NEW repeater: risks you'd name yourself + how you'd mitigate each. Every
      incubator panel asks this. A founder who names their own risks reads as
      credible; one who hasn't reads as unprepared.
  Q7  Generate the readiness pack as a branded PDF using the existing document
      template, assembling every mission's output into one sendable document.

ALSO, TWO SMALLER REALIGNMENTS

  MISSION 4 is now "Testable Problem Statement", singular. Add one question:
  "What would prove this statement wrong?" — one line. A statement you cannot
  falsify is a belief, not a hypothesis, and this line is what makes Mission 7
  possible.

  MISSION 9 is now "Build a LEARNING Prototype". Add a new FIRST question,
  before any tooling question: "What is this prototype meant to teach you?" —
  a builder, "I want to find out whether ___", offering the assumptions from
  Mission 6 that Mission 7 did not test. Then in Mission 10, add a closing
  question referring back to it: "You built this to find out whether [X]. Did
  you?"
```

## PROMPT C — Carry Answers Forward Between Missions

```text
PAGE: All mission question screens, plus a new founder-profile store.

THE PROBLEM

The same question is asked up to five times across the 15 missions, because
nothing carries forward.

  "Who is your user"          M1 Q3, M2 Q1, M2 Q2, M4 Q2, M11 Q1
  "What are your features"    M6 Q2, M9 Q2, M13 Q1
  "What did you learn"        M7 Q5, M10 Q4, M14 Q3
  "What are your next steps"  M9 Q6, M10 Q5, M13, M14 Q6, M15 Q6

Each mission therefore feels like starting over, when it should feel like the
last one is being built on. Founders retype, drift, and contradict themselves.

THE FIX

1. A FOUNDER PROFILE OBJECT that accumulates across missions:
     industry[], userSegment, userPersona, problemStatement, focusProblem,
     valueProposition, features[], assumptions[], businessModel[],
     channels[], pricing, metrics[], evidence[]
   Every mission writes into it and reads from it.

2. CARRY-FORWARD FIELDS are pre-filled, editable, and framed as continuation
   rather than repetition:

     "In Mission 1 you said the problem was:
      [their exact words, in an editable field]
      Sharpen it now that you know who you're talking about."

   Never show a carried field blank. Never show it locked.

3. TRACK WHAT CHANGED. When a founder edits a carried answer, keep both
   versions. At the end of the journey, show how their problem statement
   evolved from Mission 1 to Mission 4 to Mission 15. That is one of the most
   satisfying things a guided product can show someone about their own work.

4. THESE THIRTEEN FIELDS CARRY:
     M2 Q3   ← M1 Q2                  problem statement
     M3 cards← M1, M2                 problems to prioritise
     M4 Q2   ← M2 Q1                  the user
     M6      ← M2, M4, M1 Q4          segment, pains, alternatives
     M7 Q1   ← M6 assumptions         riskiest assumption, sorted first
     M8 VP   ← M6                     value proposition
     M8 seg  ← M2                     customer segments
     M9 Q1   ← M6, M7                 untested assumptions
     M9 Q3   ← M6                     features
     M10 Q6  ← M9 Q1                  did the prototype answer its question
     M11 Q2  ← M2                     narrowed segment
     M13 Q1  ← M6, M9                 features to scope
     M15 Q2  ← M3,4,7,10,11,12,14     the evidence pack

5. REMOVE THE DUPLICATE. Mission 6's "what benefits will users get" asks the
   same thing as "list your key features". Merge into one repeater with a
   feature column and a benefit column.

6. Mission 10 has already been renamed from "Solution Hypothesis Test" to
   "Prototype User Test" — no action needed, noting it so nobody reverts it.
```

## PROMPT D — The Answering Experience

```text
PAGE: /missions/:id — the mission question screen.

THE PROBLEM

All of a mission's questions render on one long page as a stack of blank
boxes. That is what makes the missions feel like homework, and it is why
testers gave up rather than asked for help.

THE FIX

1. ONE QUESTION AT A TIME on mobile; two or three on desktop. A stepper at the
   top shows position ("Question 3 of 5") and allows jumping. Each question
   gets room to breathe.

2. EVERY QUESTION CARRIES THREE THINGS ABOVE THE INPUT:
     - The question, in plain language
     - "Why this matters" — one sentence, collapsible, expanded the first
       time and collapsed thereafter
     - An estimated time — "about 2 minutes"

3. "SEE AN EXAMPLE" ON EVERY QUESTION — an anonymised real answer that scored
   well, shown in a panel, NEVER pre-filled into the field. Founders cannot
   hit a standard they have never seen. This is the single highest-value item
   in this prompt.

4. INSTANT, QUIET FEEDBACK. When an answer meets the bar, a small tick and
   "Ready". Not a score, not a celebration — a signal that they can move on.
   When it doesn't, say what's missing in one line.

5. MOMENTUM, NOT CONFETTI. After each question, a small progress movement and
   the next question sliding in. Something bigger on mission completion. Do
   not celebrate trivial actions — this audience finds that patronising faster
   than most.

6. SAVE STATE VISIBLY. "Saved 2 minutes ago" near the stepper. Leaving and
   returning restores exact position. Never lose an answer.

7. SHOW THE THREAD. One line at the top of each mission connecting it to the
   last: "In Mission 2 you defined your user as [X]. This mission turns that
   into a problem statement you can test."

8. LET THEM SEE THE WHOLE MISSION. A "view all questions" toggle for founders
   who want to read ahead. Some people need the map before the first step.

9. ARABIC AND RTL throughout — stepper direction, chip wrapping, slider
   direction, matrix axes.

10. NEVER MORE THAN ONE PRIMARY BUTTON on screen. The mission page currently
    shows "Resubmit for Review" in three places.

11. ROADMAP SCREEN, same visit:
    - Every locked mission states its unlock condition: "Unlocks after Problem
      Definition." A lock with no condition reads as a paywall.
    - Show the first card of each phase in full colour even while locked, so
      the founder sees the shape of the journey rather than a wall of grey.
    - Phase progress pills get a number ("0 of 3") or are removed — as empty
      grey bars they read as decoration.
    - Fix the spelling inconsistency: "Opportunity PrioritiSation" with the
      description "PrioritiZe problems...". Pick British throughout and sweep
      all mission titles, descriptions and locale strings.
    - Change Mission 9's description from "Create prototype or Figma design"
      to "Clickable prototype — Figma, Canva, or paper". Don't name one vendor
      in mission copy.
    - Add a one-line explanation to the Test phase header, which holds a
      single mission: "One test. The riskiest thing you believe."
```

## PROMPT E — Turn Missions 3 and 5 Into Real Matrices

```text
PAGE: /missions/3 and /missions/5.

THE PROBLEM

Both missions are 2x2 matrices being collected as text fields.

Mission 3 "Opportunity Prioritisation" — its own description says "prioritise
problems based on impact and frequency" — currently asks: Problem 1
(textarea), Importance 1-10 (text), Frequency 1-10 (text), Problem 2
(textarea), Importance (text), Frequency (text), Which will you focus on
(textarea). Seven fields to fill in what is visibly a grid.

Mission 5 "Solution Selection" is the same shape with ideas.

THE FIX — one interactive matrix component, used by both.

1. CARDS COME FROM EARLIER MISSIONS where possible. Mission 3 pulls the
   problems described in Missions 1 and 2. Mission 5 starts with a repeater,
   because the ideas are new.

2. "ADD ANOTHER" lets founders add more cards. No fixed slots of two.

3. EACH CARD IS POSITIONED either by dragging onto the grid or by two sliders
   — dragging on desktop, sliders on mobile where dragging is fiddly. Both
   update the same values.

4. THE QUADRANTS ARE LABELLED, so the exercise teaches rather than collects:

     Mission 3 — Impact x Frequency
       high impact / high frequency   "Fix first"
       low impact  / high frequency   "Quick wins"
       high impact / low frequency    "Big bets"
       low / low                      "Park it"

     Mission 5 — Value x Effort
       high value / low effort        "Do now"
       high value / high effort       "Plan it"
       low value  / low effort        "Quick win"
       low value  / high effort       "Drop it"

   NOTE ON MISSION 5's AXES: the roadmap description currently says
   "value/impact matrix". Value and impact measure almost the same thing, so
   every idea lands on a diagonal and the grid stops discriminating between
   options. Build it as Value x EFFORT and update the roadmap description to
   match. If the "value/impact" wording must stay for other reasons, keep the
   wording but keep effort as the second axis.

5. WHEN A CARD LANDS IN A QUADRANT, NAME IT BACK: "Fix first — this one is
   both painful and constant." That single line is the lesson.

6. THE FINAL QUESTION becomes a chips-single choosing from the cards actually
   plotted, defaulting to whichever sits highest-right, plus one short line:
   why this one.

7. EXPORT the finished matrix as an image into the mission recap and the PDF
   report.

8. Fully keyboard-accessible, and usable at 390px width.
```

## PROMPT F — Build the Two Canvases

```text
PAGE: /missions/6 and /missions/8.

THE PROBLEM

Two missions are named visual frameworks rendered as stacks of blank text
areas. The visual structure is the entire pedagogical point in both cases, and
in both cases it has been removed.

  Mission 8 "Business Model Canvas" — a famous NINE-BLOCK visual tool,
  currently nine consecutive textareas.

  Mission 6 "Value Proposition & Assumptions" — its own description says
  "develop problem-solution canvas", and there is no canvas anywhere in it.

THE FIX

MISSION 8 — render the real Business Model Canvas layout:

     ┌──────────┬──────────┬──────────┬──────────┬──────────┐
     │  Key     │  Key     │  Value   │ Customer │ Customer │
     │ Partners │Activities│  Props   │Relations │ Segments │
     │          ├──────────┤          ├──────────┤          │
     │          │  Key     │          │ Channels │          │
     │          │Resources │          │          │          │
     ├──────────┴──────────┼──────────┴──────────┴──────────┤
     │   Cost Structure    │        Revenue Streams          │
     └─────────────────────┴─────────────────────────────────┘

  On mobile this stacks vertically in the same order, each block showing its
  name and a one-line explanation.

  TAPPING A BLOCK opens a focused editor for that block only, with the canvas
  filling in visually behind it. Show "4 of 9 blocks complete".

  INPUT TYPE PER BLOCK — not nine identical textareas:

    Value Propositions      carried from Mission 6, editable
    Customer Segments       carried from Mission 2, editable
    Channels                chips-multi: Own website · App store · Instagram ·
                            TikTok · WhatsApp · Resellers · Direct sales ·
                            Marketplace · Physical shop · Other →
    Customer Relationships  chips-multi: Self-serve · Personal support ·
                            Community · Automated · Dedicated account · Other →
    REVENUE STREAMS         chips-multi: Subscription · One-time sale ·
                            Commission · Freemium · Advertising · Licensing ·
                            Marketplace fee · Usage-based · Other →
                            MULTI-SELECT IS ESSENTIAL HERE. Mixed revenue
                            models are normal and a single text box hides that
                            entirely.
    Key Resources           chips-multi + repeater for specifics
    Key Activities          repeater
    Key Partnerships        repeater: partner + what they provide
    Cost Structure          repeater: cost line + amount + currency, with a
                            running monthly total shown

MISSION 6 — render a problem-solution canvas, as the description promises:

    Customer segment        carried from Mission 2
    Problem / pains         carried from Mission 4
    Existing alternatives   carried from Mission 1 Q4
    Gains                   chips-multi: Cheaper · Faster · Less effort · More
                            reliable · Available locally · In Arabic · More
                            trusted · New capability · Other →
    Your solution           textarea — genuinely open, one of the few
    Value proposition       builder: "For [user] who [need], [name] is a
                            [category] that [benefit]. Unlike [alternative],
                            we [difference]."
    Key features            repeater: feature + the benefit it delivers
    ASSUMPTIONS             repeater: assumption + chips-single risk
                            (High/Medium/Low), AUTO-SORTED riskiest first.
                            This list is the direct input to Mission 7, so its
                            order matters.

FOR BOTH CANVASES

1. EACH BLOCK CARRIES A ONE-LINE EXPLANATION. Most founders meeting these
   frameworks for the first time do not know what "Key Activities" means:
   "Key Activities — the things your business must do every week for the model
   to work."

2. EXPORT the completed canvas as an image and as a branded PDF using the
   existing document template.

3. Once a block is filled, show a short orientation signal rather than a
   score: "Revenue Streams: 2 selected · Cost Structure not yet filled". The
   rubric still assesses the whole mission; this is orientation, not grading.

4. RTL layout for Arabic — the canvas mirrors, and block order reverses.
```

## PROMPT G — Add 27 Questions That Close Real Gaps

```text
PAGE: The mission schema, and every mission question screen.

THE PROBLEM

A founder can currently complete a mission without having done the thinking
the mission exists for. Nothing asks how they know the problem is real.
Nothing asks who is NOT their user. Nothing asks whether the person who has
the problem is the person who would pay. Nothing asks how they will know
anyone used their MVP — so by Mission 14 they have no data and cannot answer
a single traction question.

THE FIX

Add these questions to the existing missions. All are chips, one-liners or
calculated fields — roughly 8-12 minutes added across a journey that runs for
weeks.

PRIORITY 1 — ship these first (17)

  M1  "How do you know this problem is real?" chips-multi:
      I've experienced it · I watched someone deal with it · I've talked to
      people about it · I read about it · I have data · It's a hunch
      "It's a hunch" MUST be a permitted answer. It is the honest starting
      point for most founders and the rubric should not punish it in Mission 1.

  M2  "Who is NOT your user?" — one line.
  M2  "How do they solve it today?" chips-multi: Manually · Spreadsheet ·
      WhatsApp · A competitor's app · They pay someone · They don't.
      Carry this into Mission 12 — the real competitor is usually a
      spreadsheet, not a company.

  M3  "What did you decide NOT to work on, and why?" — one line.

  M4  "Who would pay to have this solved — the user, or someone else?"
      chips-single: The user · Their employer · A government body · An
      advertiser · A platform · Not sure yet.
      Carry into Mission 8 Revenue Streams and Mission 12 pricing.

  M5  "What's the simplest version that would still help someone?" — one line.
      Carry into Mission 13 as the default MVP scope.
  M5  "What would have to be true for this to work?" repeater.
      Pre-fills the Mission 6 assumption register.

  M6  "If your riskiest assumption is wrong, what happens?" — one line.

  M7  "Who did you test with, and how did you find them?" chips-multi:
      Friends and family · My network · Cold outreach · A community or group ·
      Existing users · Recruited or paid.
      Sampling bias is invisible unless asked. Pass this to the AI reviewer:
      ten friends saying yes is not evidence and the feedback should say so.

  M8  UNIT ECONOMICS block: price · cost to serve one customer · gross margin
      (calculated, not typed). A canvas with no unit economics is a poster.

  M10 "Where did people get stuck?" repeater: step + what happened.

  M11 "What did one result cost you?" — CALCULATED, budget ÷ results. The
      founder's first cost-per-acquisition number, from data already entered.
  M11 "Could you do this ten times over?" chips-single: Yes easily · Yes with
      money · Yes with more people · No. Separates a channel from a favour.

  M12 "How many said yes but didn't actually do anything?" number + line.
      The say/do gap — the most important validation question there is, and it
      appears nowhere in the journey today.

  M13 "What's the one thing it has to do well?" — one line.
  M13 "How will you know someone actually used it?" chips-multi: Analytics
      installed · Database records · I'll ask them · I'll watch · Not set up
      yet. If they pick "not set up yet", surface a link to the toolkit.
      This one question is the difference between Mission 14 having data and
      Mission 14 being guesswork.

  M14 "Which single number will you try to move next month, and to what?"
      chips-single metric + number target. Carry into Mission 15.

  M15 "What do you need that you don't have?" chips-multi: Money · A
      co-founder · Technical help · Customers · Mentorship · Licensing or
      legal · Nothing right now. Route each answer to the relevant part of the
      platform — mentoring, the collaboration hub, the community, the toolkit.

PRIORITY 2 — valuable, deferrable (10)

  M1  "Why you?" chips-multi + line — founder-problem fit, reused in M15.
  M3  "Roughly how many people have this problem?" number + confidence chips.
  M7  "What surprised you?" — one line.
  M8  "Which block are you least sure about?" chips-single from the nine.
  M9  "What did you deliberately leave out?" — one line.
  M9  "What's the first thing a tester will see?" — one line.
  M10 "What did you change your mind about?" — one line.
  M12 "What would make you walk away from this market?" — one line.
  M15 RUNWAY grid: cash available · monthly burn · months remaining
      (calculated).

TWO RULES FOR ALL 27

1. NONE OF THEM BLOCKS SUBMISSION ON ITS OWN. They enrich the rubric; they do
   not become new ways to fail a mission. The existing quality gate stays
   attached to the substantive questions only.

2. EVERY ONE FEEDS SOMETHING LATER — a later mission, the AI reviewer's
   context, or a downloadable artefact. Wire the carry-forward at the same
   time as the question. A question that feeds nothing made the journey longer
   without making it better.
```

## PROMPT H — Make Every Mission Produce a Downloadable Artefact

```text
PAGE: Every mission completion screen, plus a new "My Documents" page in the
app shell.

THE PROBLEM

A mission currently ends in a score. The founder does hours of real work —
a business model, a matrix, an experiment, a set of metrics — and leaves with
a number. There is nothing to keep, nothing to send to a co-founder, a
lecturer, a mentor or an incubator, and nothing that reminds them the work
existed.

THE FIX

Every mission produces a downloadable artefact, generated from the answers the
founder already gave. Nothing is re-entered.

  M1  Problem landscape                          PDF
  M2  User persona card                          PDF · PNG
  M3  Impact x Frequency matrix, plotted         PNG · PDF
  M4  Problem statement card                     PDF · PNG
  M5  Value x Effort matrix, plotted             PNG · PDF
  M6  Problem-solution canvas + assumption
      register                                   PDF · PNG · CSV
  M7  Experiment report                          PDF
  M8  BUSINESS MODEL CANVAS + unit economics     PDF A3 + A4 · PNG · XLSX
  M9  Prototype brief                            PDF
  M10 Usability findings                         PDF
  M11 Channel experiment card                    PDF · PNG
  M12 Market validation report + competitor
      table + TAM/SAM/SOM chart                  PDF · XLSX
  M13 MVP scope sheet (in / out)                 PDF · XLSX
  M14 METRICS ONE-PAGER                          PDF · PNG · XLSX
  M15 THE READINESS PACK                         PDF · PPTX

THE THREE THAT MATTER MOST

1. MISSION 8 — THE BUSINESS MODEL CANVAS
   A real landscape canvas at A3, the size it is meant to be printed and
   pinned, with an A4 fallback and a PNG for slide decks. All nine blocks in
   the correct BMC positions, the founder's content inside them, unit
   economics as a strip beneath. Not a list of headings with paragraphs.

2. MISSION 14 — THE METRICS ONE-PAGER
   Render the funnel and the retention curve as ACTUAL CHARTS from the
   founder's own numbers. Then — and this is the part that makes it StartPad's
   rather than generic — PRINT THE CONFOUNDERS THE FOUNDER NAMED ALONGSIDE THE
   NUMBERS. "1,200 sign-ups (paid promotion, one-off event)" is worth more
   than "1,200 sign-ups", and it teaches the founder what honest reporting
   looks like. Include the sample size and the observation window on the face
   of the document. Never print a product-market-fit score.

3. MISSION 15 — THE READINESS PACK
   Every artefact above, assembled into one document, with the founder's
   story, their ask, their 90-day plan and the risks they named. Also export
   as PPTX so it can be presented. This is the strongest retention argument
   the product has: fifteen missions of work becomes a thing you can hand to
   someone.

RULES FOR ALL EXPORTS

1. USE THE EXISTING BRANDED PDF TEMPLATE. Logo, founder name, mission name,
   date, and a quiet "Made on StartPad · startpad.me" footer on every page.
   These documents get forwarded — that footer is the cheapest distribution
   the platform has.

2. GENERATE ON DEMAND, NOT ON COMPLETION. Regenerate whenever the founder
   edits an answer, and stamp the version date so an old PDF is identifiable.

3. "MY DOCUMENTS" — a page in the app shell listing every artefact the founder
   has generated, newest first, grouped by phase, each re-downloadable and
   showing when it was last regenerated. Link to it from the dashboard and
   from each mission recap.

4. ARABIC. Every artefact renders RTL with the Arabic type stack when the
   founder's locale is Arabic — including the canvas, which mirrors, and the
   charts, whose axis labels and legends must not stay left-to-right inside an
   RTL page.

5. SHOW THE ARTEFACT BEFORE THE SCORE on the mission completion screen. The
   thing they made, then how it was assessed. That order matters.

6. FREE VERSUS PRO — build it ungated. Everyone can download everything, with
   the StartPad footer on every export. Do not watermark and do not paywall
   downloads. A founder who cannot download their own canvas will screenshot
   it, and the forwarding is worth more than the upgrades. If this is later
   reversed, it is a config flag, not a rebuild — so put it behind one.
```

---

## Sequence

| # | Prompt | Why here |
|---|---|---|
| 1 | **A** — input components | Everything else needs these to exist |
| 2 | **B** — realign 11, 14, 15 | Correctness before polish. Mission 14 currently contradicts itself |
| 3 | **C** — carry-forward | Cheap, and removes 12 duplicate questions |
| 4 | **G** — the 27 added questions | Same schema pass as B and C. Doing it separately means touching every mission twice |
| 5 | **D** — answering experience | The shell the new inputs live in, plus the roadmap fixes |
| 6 | **E** — the two matrices | Self-contained, high visible impact |
| 7 | **F** — the two canvases | The biggest build, and the most distinctive |
| 8 | **H** — downloadable artefacts | Needs E and F to exist, because it exports what they render |

A, B, C and G are one coherent schema pass and could ship in about a week — that alone removes most of the friction your testers hit. E, F and H are the ones founders will talk about, and H is the one they'll forward.

---

## One inconsistency to fix outside the missions

The LinkedIn "About" copy from the branding round describes **eight phases** — Discovery, Analysis, Ideation, Validation, Business Model, Development, Strategy, Launch. The live roadmap has **five**: Discover, Shape, Test, Model, Readiness. I've corrected `brand/linkedin/overview-copy.md` to match the roadmap. If that copy is already published on LinkedIn, it needs updating there too — and it's worth checking anywhere else the phase list appears: the About page, How It Works, the Help Centre, and the marketing homepage.
