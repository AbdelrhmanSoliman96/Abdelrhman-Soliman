# StartPad — Lovable Prompts (Round 7)

Six prompts on AI output quality and performance.

| Set | Area | Prompts |
|---|---|---|
| 1 | Context & output contracts | A — context layer · B — output contracts |
| 2 | The generic surfaces | A — rewrite them · B — upgrade evaluator & mentor |
| 3 | Performance | A — latency, caching, model routing |
| 4 | Measurement | A — eval harness |

---

## The good news: you already have the standard

Two AI surfaces in StartPad are genuinely excellent, and they prove the model isn't the problem.

**The mission evaluator:**

> *"You wrote 'sda', which is a placeholder and lacks any industry context. The weakest criterion is Depth."*
> *"[Specificity] Replace generic phrasing with concrete names, numbers, and user segments (e.g. '25-35 year old SaaS PMs in KSA' instead of 'users')."*
> *"[Depth] Answer the 'so what' — link each point to its impact on the founder, the user, or the business model."*

**The survey generator:**

> *"Why this question: Establish an upper bound for value-based pricing strategies using the Van Westendorp model."*

Both quote the founder's own words, name a specific method, and give a concrete rewrite. Neither could have been written without knowing who the founder is.

**Now compare the guidance surfaces, two tabs away:**

> *"Focus on the mission objectives · Gather relevant data · Document your findings · Validate with real users"*
> *"Complete the required fields · Review your responses · Get feedback from peers · Submit when ready"*
> *Pro tips: "Take your time to think through each question" · "Be specific in your responses" · "Use data to back up your claims" · "Research before answering"*

Every one of those sentences would be identical for any founder, on any mission, in any country. They are what the model produces when it has been given nothing to work with.

**So this is not a model problem. It's three fixable things:** the generic surfaces aren't receiving context, they aren't constrained by an output contract, and nothing measures whether their output is any good. That's what these six prompts fix.

---
---

# Set 1 — Context and Output Contracts

Two prompts. These are the foundation — every other AI improvement depends on them.

## PROMPT A — Build the Context Layer

```text
PAGE: All AI surfaces — AI Mentor, Ask AI Coach, My Next Steps, AI-Powered
Suggestions, Create Your Survey, mission evaluation, and the per-question
"Ask AI Mentor" helper.

THE PROBLEM
Output quality across these surfaces varies enormously, and the pattern is
exact: the surfaces that receive founder context produce specific, useful
answers; the surfaces that don't produce filler.

The mission evaluator writes: "You wrote 'sda', which is a placeholder and
lacks any industry context. The weakest criterion is Depth."
"My Next Steps" writes: "Complete the required fields. Review your responses."

Same model. Different context.

There is also a "What this tool will use — 2 of 4 ready" indicator, which shows
context assembly exists but is incomplete and unexplained.

THE FIX — one shared context builder that every AI call uses. No surface
assembles its own.

BUILD getFounderContext(userId, surface, options) RETURNING:

  IDENTITY
    first_name, country, city
    occupational_status, hours_available_per_week   (from the profile work)
    preferred_language (en|ar)
    account_age_days

  THE VENTURE  — the single most important block, and the most likely to be
  missing today
    idea_one_liner            ← from Mission 1 or the landing-page idea box
    industry, target_customer
    problem_statement
    startup_stage
    Anything the founder has written about what they are building.

  JOURNEY STATE
    current_mission (number, name, phase, objectives)
    missions_completed, total_points, current_level
    attempts_on_current_mission
    last_submission_scores    ← per rubric criterion
    weakest_criterion         ← the single best steer available
    strongest_criterion
    days_since_last_activity

  THEIR OWN WORDS  — the highest-value context in the whole payload
    current_mission_answers[] ← verbatim, per question
    previous_attempt_answers[] with the scores each received
    evidence_files_attached[] (names, types, extracted text)

  HISTORY
    last_3_ai_exchanges (summarised, not verbatim)
    advice_already_given[]    ← so the AI never repeats itself
    tools_used_in_loadout[] with their headline values
    resources_opened[]

  MARKET
    Region-specific facts for their country: currency, common legal structures,
    relevant regulators, active local accelerators and funds.

RULES

1. NEVER CALL A MODEL WITHOUT CONTEXT. If the context is too thin to produce a
   specific answer, the surface asks ONE clarifying question instead of
   generating filler. "What industry are you working in? I'll tailor this."
   beats four generic bullets, every time.

2. DECLARE REQUIRED CONTEXT PER SURFACE. Each surface states which fields it
   needs. If a required field is missing, that surface either asks for it or
   renders a prompt to fill it in — it never proceeds with a generic answer.

3. FIX THE "2 OF 4 READY" INDICATOR. Expand it by default and name each gap
   with a one-click fix:
     "Your industry — not set.        Add it →"
     "Your target customer — not set. Add it →"
     "Mission 1 answers — ready ✓"
   A readiness counter the founder cannot act on is just a warning label.

4. TOKEN BUDGET. Cap the context payload (roughly 2,000 tokens) and prioritise:
   the founder's own words first, journey state second, identity third, market
   facts last. Summarise history rather than including it verbatim.

5. CACHE the stable parts (identity, mission definition, market facts) and
   rebuild only the volatile parts (answers, scores) per call. See Set 3.

6. LOG the exact context sent with every AI call, so a bad answer can be
   diagnosed as a context problem or a prompt problem.
```

## PROMPT B — Output Contracts and the Banned-Phrase Rule

```text
PAGE: All AI surfaces.

THE PROBLEM
Where output is unconstrained prose, the model produces filler. Where it is
constrained to a structure with required fields, it produces specifics. The
mission evaluator is constrained — it must return a score per criterion, the
weakest criterion, evidence quotes, and concrete fixes. That is exactly why it
is good.

"Pro Tips" is unconstrained, and returns "Take your time to think through each
question."

THE FIX

1. EVERY AI SURFACE RETURNS STRUCTURED JSON, never free prose. Define a schema
   per surface with required fields that CANNOT be filled generically. Example
   for "My Next Steps":

     {
       "next_action": {
         "what": "Rewrite your answer to Question 1",
         "why": "Specificity scored 20% — the lowest of your five criteria",
         "how": "Replace 'sda' with the industry you actually care about",
         "example": "Fintech for gig workers in Egypt",
         "quote_from_their_work": "sda",
         "expected_gain": "Specificity 20% → ~60%",
         "time_estimate_minutes": 5,
         "deep_link": "/journey/mission/1?q=1"
       },
       "then": [ ...two more, same shape... ]
     }

   Note which fields make generic output impossible: quote_from_their_work
   forces grounding in what they actually wrote, expected_gain forces the model
   to reason about their scores, and example forces concreteness.

2. THE GROUNDING RULE — every piece of feedback must reference something the
   founder actually produced: a quote from their answer, a score they received,
   a tool value they entered, a mission they completed. If the model cannot
   ground a statement, it must not make it.

3. BANNED PHRASES — a hard blocklist checked after generation. If a match is
   found, regenerate once with the violation named; if it fails twice, surface
   nothing rather than filler. Seed the list with the phrases currently
   shipping:

     "take your time"            "be specific"
     "research before"           "use data to back up"
     "review your responses"     "complete the required fields"
     "get feedback from peers"   "submit when ready"
     "gather relevant data"      "document your findings"
     "it's important to"         "consider the following"
     "in today's"                "make sure to"
     "focus on the mission objectives"

   Add to the list whenever a generic phrase is spotted in production.

4. THE SPECIFICITY TEST — build it into every system prompt as the final check:

     "Before returning, ask: could this exact sentence have been written for a
      different founder, on a different mission, in a different country? If
      yes, rewrite it until the answer is no."

5. MENA SPECIFICITY, REQUIRED:
     - Use real currencies (EGP, SAR, AED), not "$" by default
     - Reference real regional context: Egypt's FRA, Saudi's SAGIA, ADGM and
       DIFC free zones, Flat6Labs, Falak, 500 MENA
     - Use regional companies as examples, not Airbnb and Uber
     - Never give US-centric legal or tax advice
   A founder in Cairo should be able to tell the advice was written for them.

6. FEW-SHOT EXAMPLES in every system prompt: two examples of excellent output
   and one of poor output labelled as such. Draw the excellent examples from
   the mission evaluator's actual output — it is already the standard.

7. LENGTH DISCIPLINE. Cap each field. A "why" is one sentence; a "how" is one
   or two. Long AI output is usually padded AI output.

8. ARABIC — when preferred_language is Arabic, generate natively in Arabic
   rather than translating English output. Translated startup advice reads as
   translated, and this audience notices.
```

**Why this order.** A before B — output contracts are only enforceable once the context exists to satisfy them.

---
---

# Set 2 — The Generic Surfaces

Two prompts. A rewrites the four worst offenders. B raises the two that are already good.

## PROMPT A — Rewrite the Generic Surfaces

```text
PAGE: AI Tools → "My Next Steps" and "AI-Powered Suggestions"; the mission
page's Key Points and Pro Tips panels.

THE PROBLEM — the exact text currently shipping:

  Mission page, "Key Points":
    "Focus on the mission objectives"
    "Gather relevant data"
    "Document your findings"
    "Validate with real users"

  "Recommended Next Steps":
    "Complete the required fields"
    "Review your responses"
    "Get feedback from peers"
    "Submit when ready"

  "Pro Tips":
    "Take your time to think through each question"
    "Be specific in your responses"
    "Use data to back up your claims"
    "Research before answering"

Twelve bullets. Not one references the founder, their idea, their mission,
their scores, or their country. Every one would be identical for every user.
They sit two tabs from an AI Mentor giving genuinely specific coaching, which
makes both look worse.

THE FIX

1. DELETE ALL THREE PANELS in their current form. Replace with ONE panel,
   generated from real state via the Set 1 context layer:

     ┌────────────────────────────────────────────────────────┐
     │ What to do next                                        │
     │                                                        │
     │ 1. Rewrite your answer to Question 1                    │
     │    Specificity scored 20% — your lowest criterion.      │
     │    You wrote "sda". Replace it with the industry you    │
     │    actually care about, e.g. "Fintech for gig workers   │
     │    in Egypt."                                            │
     │    ~5 min · Specificity 20% → ~60%      [Fix it →]      │
     │                                                        │
     │ 2. Attach one piece of evidence                         │
     │    Evidence scored 0%. One screenshot of a customer     │
     │    conversation would move it.                          │
     │    ~10 min · Evidence 0% → ~40%        [Attach →]       │
     └────────────────────────────────────────────────────────┘

   Rules: maximum three items, each completable in under fifteen minutes, each
   naming the specific gap and the expected gain, each deep-linked to the exact
   place to act. Items disappear when done. Fewer than three is fine — padding
   is not.

2. "AI-POWERED SUGGESTIONS" currently offers "Industry Research Template",
   "User Interview Questions" and "First-Time Founder Guide" — reasonable, but
   identical for everyone. Make each one carry a reason drawn from their state:
     "Industry Research Template — your Evidence score is 0% across two
      attempts. This template produces the kind of source the reviewer accepts."
   If a suggestion cannot be justified from their state, don't show it.

3. THE PRIORITY RULE — order by expected score gain, not by category. The
   founder should never have to work out which of three suggestions matters
   most; that is the product's job.

4. NEVER SHOW ADVICE ALREADY GIVEN. Track advice_already_given[] in context and
   exclude it. Repeating a suggestion the founder has already acted on is the
   fastest way to make the AI feel mechanical.

5. If the context genuinely cannot support a specific suggestion, render the
   gap instead: "Add your industry and I'll tailor these to it. [Add industry]"
   That is more useful than four generic bullets, and it is honest.
```

## PROMPT B — Raise the Evaluator and the Mentor

```text
PAGE: Mission evaluation (the rubric scorer) and AI Mentor.

CONTEXT
These two are the best AI surfaces in the product. Do not rebuild them. These
are targeted upgrades.

THE EVALUATOR — currently returns five criteria with bands, weights, evidence
quotes, a weakest-criterion call and a fix list. Add:

1. A WORKED EXAMPLE PER CRITERION. Founders cannot hit a standard they have
   never seen. For the question they are weakest on, offer "What does a strong
   answer look like?" showing an anonymised real answer that scored 80%+ on
   that criterion, with the passing parts highlighted and annotated.

2. ATTEMPT DELTAS. On attempt 2 and later, show the per-criterion change from
   the previous attempt — "Specificity 20% → 65% (+45)" — so the founder can
   see whether their edits worked. Without this, resubmission is guesswork.

3. CALIBRATION. Run the same submission through the evaluator three times and
   compare. If scores vary by more than about five points, tighten the rubric
   prompt: add explicit band definitions with example answers at each band
   boundary, and lower the temperature. A scorer that disagrees with itself
   cannot be trusted, and founders will notice across attempts.

4. STAGE THE DELIVERY. A first-timer currently sees a red 20%, a red rationale
   block, a six-item blocker list and five bars mostly at 0% — simultaneously.
   The content is correct; the shape is a rejection letter. Lead with the one
   highest-gain fix, then "See the full assessment →". Keep the rigour.

5. CONFIDENCE. Where the evaluator is unsure — a short answer, an ambiguous
   response — say so rather than scoring confidently: "Hard to assess from this
   much text. Add two more sentences and I'll give you a real score."

THE AI MENTOR — currently carries mission context and a dated "Where you left
off" recap. Add:

6. MEMORY ACROSS SESSIONS. It should know what it advised last time and follow
   up: "Last week I suggested three empathy interviews. How did they go?" This
   is the single biggest difference between a chatbot and a mentor.

7. PUSH BACK ON VAGUE ANSWERS. The landing page promises the AI "pushes back on
   vague answers." Make it real: when a founder gives a thin answer in chat,
   the mentor asks one sharpening question rather than accepting it and moving
   on.

8. REFUSE TO DO THE WORK. When asked "write my problem statement for me", it
   should decline and ask the two questions that would let the founder write it
   themselves. A platform whose value is teaching founders to think cannot have
   an AI that thinks for them.

9. CITE THE SOURCE. When the mentor references a framework, name it and link to
   the matching Loadout tool or Knowledge Hub article. The survey generator
   already does this well ("using the Van Westendorp model") — extend the
   pattern.

10. STAY IN SCOPE. Politely redirect questions unrelated to the founder's
    journey rather than answering them. A general-purpose chatbot inside a
    guided product dilutes the product.
```

**Why this order.** A first — it fixes what is visibly poor. B is refinement of what already works.

---
---

# Set 3 — Performance

## PROMPT A — Latency, Caching and Model Routing

```text
PAGE: All AI surfaces — the request path, not the prompts.

THE GOAL
Perceived speed matters more than raw speed. A streaming answer that starts in
400ms feels faster than a complete one delivered silently in 2 seconds.

1. STREAM EVERYTHING USER-FACING. AI Mentor, Ask AI Coach and mission feedback
   all stream token by token. Never show a spinner while a long answer
   generates in silence.

2. ROUTE BY TASK — do not send every call to the same model:

     Fast / cheap model:
       - Classification and tagging (which mission, which topic, which category)
       - Short suggestions and title generation
       - Translation of already-generated content
       - The readiness/context checks

     Strong model:
       - Mission rubric evaluation  (accuracy matters most here — never
         downgrade this one to save cost)
       - AI Mentor coaching turns
       - Survey question generation

   Make the routing table explicit in config, not scattered through the code,
   so it can be tuned without a refactor.

3. PROMPT CACHING. The system prompt, rubric definitions, mission definitions,
   few-shot examples and market facts are stable across calls — cache them and
   send only the volatile context per request. On a rubric prompt with several
   worked examples this is a large latency and cost saving.

4. PARALLELISE INDEPENDENT CALLS. Scoring five rubric criteria is five
   independent judgements — run them concurrently rather than sequentially, then
   assemble. This alone can cut evaluation time substantially.

5. PRECOMPUTE ON IDLE. Generate "What to do next" when a submission is scored,
   not when the founder opens the tab. By the time they arrive, it is ready.

6. OPTIMISTIC AND PROGRESSIVE UI:
     - Show the criteria skeleton immediately, fill each bar as its score lands
     - Render the next-action card before the full breakdown finishes
     - Reserve height for every AI block so nothing shifts on arrival

7. TIMEOUTS AND FALLBACKS. Every call gets a timeout. On failure, show a real
   message with a retry — never a spinner that never resolves, and never a
   silently degraded generic answer. If the evaluator fails, say so; do not
   return a guessed score.

8. DEBOUNCE AND DEDUPE. Cancel in-flight requests when the founder edits again.
   Hash the input and return the cached result for an identical resubmission
   rather than paying to re-score unchanged text.

9. RATE LIMIT PER USER, with a clear message when hit. Protects cost and
   prevents one user degrading everyone's latency.

10. MEASURE, PER SURFACE: time to first token, total completion time, token
    count in and out, cost per call, error rate, timeout rate. Put it on an
    admin dashboard. You cannot tune what you cannot see.

11. BUDGET PER CALL. Cap max output tokens per surface. Unbounded generation is
    both the main cost driver and the main cause of padded answers — the
    performance fix and the quality fix are the same fix here.
```

**Why this order.** Independent of Sets 1 and 2 — can run in parallel. Item 3 and item 4 give the largest wins for the least work.

---
---

# Set 4 — Measurement

## PROMPT A — An Evaluation Harness

```text
PAGE: Admin — new route /admin/ai-quality.

THE PROBLEM
There is currently no way to know whether an AI output is good, whether a
prompt change improved or degraded things, or whether the evaluator is
consistent. Every improvement is therefore a guess, and every prompt edit risks
silently breaking something that worked.

THE FIX

1. BUILD A GOLDEN SET — 20-30 real test cases per surface, drawn from actual
   founder submissions (anonymised). For the evaluator, deliberately include:
     - An excellent answer that should score 85%+
     - A borderline answer near the 70% threshold
     - A weak-but-genuine answer
     - Keyboard mash ("sda", "dsad") that must score near zero
     - An answer in Arabic
     - An answer mixing Arabic and English
     - A very short answer where the right response is "not enough to assess"

2. SCORE EVERY OUTPUT against fixed criteria:
     Specific    — does it reference the founder's actual words or scores?
     Actionable  — could they act on it in the next 15 minutes?
     Grounded    — is every claim traceable to their input?
     Regional    — is it relevant to a MENA founder specifically?
     Concise     — no padding, no filler phrases?
     Clean       — zero banned-phrase matches?

3. RUN ON EVERY PROMPT CHANGE, as a regression suite. Report per-criterion
   scores before and after. Block deployment if any criterion drops. Treat
   prompts as code: version them, review changes, and never edit a live prompt
   without running the suite.

4. CONSISTENCY CHECK — run the same input three times. Flag any surface whose
   scores vary by more than five points. Consistency is a hard requirement for
   the evaluator specifically, because founders compare attempts.

5. IN-PRODUCT SIGNAL. The thumbs up/down on AI suggestions already exists —
   wire it to a dashboard showing per-surface satisfaction over time. Add an
   optional one-line "what was wrong with this?" on thumbs-down. Route
   low-rated outputs into the golden set as new test cases.

6. THE BANNED-PHRASE MONITOR. Scan production AI output continuously and alert
   when a blocked phrase escapes. Every escape is a prompt bug.

7. COST AND LATENCY per surface on the same dashboard, so quality gains that
   cost 3x latency are visible rather than discovered later.

8. A/B PROMPTS. Support running two prompt versions concurrently on a traffic
   split, compared on the criteria above plus real behaviour — did the founder
   act on the suggestion, did their next attempt score higher. Downstream
   behaviour is the only quality measure that fully counts.
```

**Why this order.** Last to build, but the thing that keeps everything above from regressing. Build the golden set as soon as Set 2 ships, so you have a baseline to measure against.

---

## Suggested sequence

| Order | What | Why |
|---|---|---|
| 1 | Set 1·A | Context layer — nothing else works without it |
| 2 | Set 1·B | Output contracts and the banned-phrase list |
| 3 | Set 2·A | Rewrite the twelve generic bullets — most visible win |
| 4 | Set 3·A | Performance — items 3 and 4 first |
| 5 | Set 2·B | Evaluator and mentor upgrades |
| 6 | Set 4·A | Eval harness, to hold the gains |

Sets 1 and 3 can run in parallel — one changes what goes into the model, the other changes how the call is made.
