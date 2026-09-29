# StartPad — Calibrating the Pass Mark (Round 16)

Making missions hard enough to mean something and easy enough to finish.

---

## The measurement you already have

The Mission 1 screenshot is the most useful calibration data in the product. The founder submitted this:

```
fdsfdsdsdfdfsdsadsds dad dad dada dad da da dad d ad a d ad a da da d ad a da d ad a d ad
```

and scored **20 out of 100**.

That single number tells you where the floor is. Pure nonsense — no words, no meaning, no attempt — lands at 20. Which means:

- **The scale is being used from 20 to 100, not 0 to 100.** A fifth of the range is unreachable, so every real answer is compressed into the top 80.
- **The distance from nonsense to passing is 50 points.** It should be 70.
- Large language models are reluctant to award a zero. Asked to rate something out of 5, they give 1 rather than 0 almost every time, because the training data rewards hedging. Nobody chose 20; it's an artefact.

And nonsense isn't the real threat anyway.

---

## The answer that actually beats the rubric

Gibberish is easy to catch. This is not:

> *"Our target users are young people who want a better and more convenient experience. Current solutions are expensive and don't meet their needs. We will provide an easy-to-use platform that solves this problem."*

Grammatical. On topic. Right length. Uses the vocabulary of the question. And completely empty — it contains no fact about any business, and it would sit unchanged in a submission from any founder in any industry in any country.

**That is what "passing with a random answer" actually looks like**, and a rubric that only screens for nonsense will wave it through.

### The substitution test

One sentence separates a real answer from a plausible one:

> **Could this be pasted into another founder's submission, in a different industry, without changing a word?**

If yes, it's generic, whatever it scores on grammar. This works as an instruction to the model *and* as a cheap local heuristic, because generic answers share a measurable trait: **no proper nouns, no numbers, no named place, no named segment.** An answer containing none of those is almost never specific, in Arabic or English.

---

## Two failure modes, opposite directions

You named both. They need different mechanisms, and confusing them is why most rubrics end up either trivial or brutal.

| | Too easy | Too hard |
|---|---|---|
| **Looks like** | Generic answers pass; founders learn nothing; the badge is worthless | Real effort scores 45; founder tries twice; leaves |
| **Caused by** | Averaging that hides a zero · a 20-point floor · no specificity requirement | Grading the idea instead of the work · demanding evidence too early · feedback naming five fixes |
| **Fixed by** | Gates before scoring · per-criterion floors · the substitution test | Phase-weighted criteria · one named fix at a time · never judging the business |

**A mission is not an exam.** It asks whether the founder did the work, not whether their idea is any good. A brilliant answer about a doomed business must score well. The moment the rubric starts grading business quality it becomes an idea judge — which it isn't competent to be, and which will crush exactly the first-time founders StartPad exists for.

---

## The design

### Layer 1 — Gates, before anything reaches the model

Three binary checks, in the browser, costing nothing. Failing one means the submission is **not scored at all and no attempt is consumed.**

| Gate | Passes when | Founder sees |
|---|---|---|
| **Real answer** | Not gibberish, not placeholder, not a keyboard run | "This doesn't look like a finished answer yet." |
| **Substance** | Meets the stated minimum — genuinely 2–3 sentences, not 200 words | "About two or three sentences is enough here." |
| **Evidence** *(only where the mission requires it)* | At least one file, link or pasted note attached | "This mission needs one piece of evidence — a screenshot, link or interview notes." |

This is where random answers stop. Not in the rubric — at the door, before you pay for a model call. The gate specified in Round 11 exists; the screenshot proves it isn't running on this field.

### Layer 2 — Five criteria, weighted by phase

Same five criteria everywhere, so the score means one thing across the journey. What changes is the weighting, and that is where the difficulty curve lives.

| Phase | Specificity | Depth | Evidence | Actionability | Relevance |
|---|---|---|---|---|---|
| **Discover** (1–3) | 30 | 20 | **10** | 10 | 30 |
| **Shape** (4–6) | 25 | 25 | 15 | 15 | 20 |
| **Test** (7) | 20 | 20 | **30** | 15 | 15 |
| **Model** (8–10) | 20 | 25 | 20 | 20 | 15 |
| **Readiness** (11–15) | 20 | 20 | **30** | 20 | 10 |

A founder in Mission 1 has no evidence yet, so evidence is worth 10 and cannot fail them. By Mission 7 the entire mission *is* evidence, so it's worth 30. **The bar rises without the pass mark moving**, which is the point — 70 means the same thing in Mission 1 and Mission 15, and no founder can shop for the easy mission.

### Layer 3 — A floor, so averaging can't hide a hole

Averaging five criteria lets a founder score `5, 5, 5, 5, 0` — 80% — with one criterion completely absent. That's how a submission with no evidence at all passes an evidence-weighted mission.

> **Pass = weighted score ≥ 70 AND no criterion weighted 20 or above scores below 2 out of 5.**

Two out of five is a low bar. It means "you attempted this." The floor doesn't make the mission harder; it stops one strength papering over one absence.

### Layer 4 — Anchors, or the model will drift

The single most effective calibration technique is putting scored examples in the rubric prompt. Written descriptions of quality levels are interpreted differently on every call. Examples are not.

Here is the ladder for the exact question in your screenshot — *"What are the limitations of current solutions?"*

| Score | Answer | Why |
|---|---|---|
| **0** | `dsad` · `fdsfds dad dad dada` | Not an answer. Never reaches the model — Gate 1 stops it. |
| **1** | "They are expensive and slow." | True of every product ever built. Names nothing. **Fails the substitution test.** |
| **3** | "Existing budgeting apps are English-only and don't connect to Egyptian banks, so users type every transaction in by hand." | Names a market, a concrete failure, and a consequence. No evidence behind it. |
| **5** | "The three apps students named to me all require a credit card at sign-up. Six of the nine students I spoke to in Cairo don't have one, so they never got past registration." | Specific, sourced, quantified, and the consequence is observed rather than assumed. |

**Every question in all 15 missions needs this ladder.** It is the largest piece of work in this round and the one that decides whether any of the rest matters.

A 3 passes. That is deliberate — 70 should be reachable by a founder who thought carefully and hasn't yet done fieldwork. A 5 requires having talked to someone.

---

## Consistency

A founder who resubmits identical text and receives a different score loses trust in the whole system, permanently.

1. **Temperature 0** on every rubric call, with a versioned prompt.
2. **Cache by the answer hash.** Round 15 already computes `scoredHash` per answer. If the hash is unchanged, return the stored score and **never call the model.** Identical text becomes incapable of scoring differently, and re-reviews cost only what actually changed.
3. **Borderline band 66–74** — score twice and take the lower. Passing by rounding luck is worse than failing honestly.
4. **Bank passing questions.** A question scoring well is marked Ready and isn't re-scored on resubmission. A founder fixing question 3 shouldn't risk question 1 coming back lower for no reason.

---

## Protecting the other side

Six rules that keep it from becoming too hard. Each one is testable.

1. **Never grade the business.** Not the idea, not the market, not whether it will work. Only whether the founder did the thinking the question asks for.
2. **Never require evidence a founder can't have yet.** That's what the phase weights are for.
3. **Never penalise language.** Grammar, spelling and vocabulary are not criteria. An Arabic answer and an English answer of equal substance score identically — verify this with paired submissions, don't assume it.
4. **Name one fix, not five.** The screenshot shows three feedback rows plus a banner plus a highest-gain card. One founder, one next action.
5. **The feedback must be sufficient.** If a founder does exactly what the feedback says, the result must reach 70. Feedback that names three fixes which together still land at 62 is lying to them. **This is machine-checkable** — apply the named fixes to a stored answer and re-score.
6. **Cap the effort.** If the question says two or three sentences, two or three good sentences must be able to score 4. A rubric that quietly rewards length teaches founders to pad, and padding is the enemy of every criterion you're measuring.

---

## How you'll know it's calibrated

You cannot tune this by feel. You need labelled answers.

**Build a calibration set**: for each of the 15 missions, 20 real answers scored by a human — 5 nonsense, 5 generic-but-plausible, 5 borderline, 5 genuinely good. Draw them from actual submissions, anonymised.

The rubric is calibrated when:

| Band | Expected | Must not |
|---|---|---|
| Nonsense | Blocked at the gate, never scored | Reach the model |
| Generic | **25–45** | Reach 70 |
| Borderline | 55–75 | — |
| Good | 75–95 | Score below 70 |

Then **freeze it as a regression test.** Every change to a rubric prompt reruns the set, and a change that moves more than two answers across the pass line does not ship without someone looking at why. This extends the eval harness from Round 7 rather than building a second one.

**The number to watch in production:** the share of founders who pass Mission 1 within three attempts. Below 60% it's too hard and you're losing people at the front door. Above 90% it's too easy and the badge means nothing. **Somewhere around 75% is the target** — most people get there, and getting there took a real second attempt.

---
---

# The prompts

Five, in order. Paste one per message.

## PROMPT A — Gates Before Scoring

```text
PAGE: /missions/:id — the answer field and the submission path, plus the
scoring service.

THE PROBLEM

A founder submitted "fdsfdsdsdfdfsdsadsds dad dad dada dad da da dad" and
received a score of 20 out of 100. Nonsense reached the model, was graded,
consumed an attempt, and cost an API call to be told what the browser could
have determined for free.

Worse, 20 is now the floor of the scale. Every genuine answer is compressed
into the top 80 points, and the distance from nonsense to the 70 pass mark is
only 50 points instead of 70.

THE FIX — three binary gates that run BEFORE any model call. Failing a gate
means the submission is NOT SCORED and NO ATTEMPT IS CONSUMED.

GATE 1 — IS THIS A REAL ANSWER?
  Run the existing quality check (dictionary hit rate, adjacent-key runs,
  repeated-token ratio, long character runs) on blur, not only on submit.
  Add short-repeated-fragment detection: "dad dad dada dad da da dad" passes a
  word count and fails everything else.
  Message: "This doesn't look like a finished answer yet."
  Neutral tone. Some founders type a placeholder intending to come back.

GATE 2 — IS THERE ENOUGH SUBSTANCE?
  Meet the stated minimum for that question, and no more. If the question says
  two to three sentences, two good sentences must pass.
  Message: "About two or three sentences is enough here."
  DO NOT make this a length race. See PROMPT B rule 6.

GATE 3 — IS THERE EVIDENCE, where the mission requires it?
  Only on questions flagged evidenceRequired. At least one file, link or
  pasted note.
  Message: "This mission needs one piece of evidence — a screenshot, link, or
  interview notes."

RULES

1. GATES BLOCK SUBMISSION, NEVER SAVING. Drafts persist exactly as typed.

2. GATE FAILURES COST NOTHING. No attempt increment, no model call, no score
   written. A founder who typed a placeholder has not used up a try.

3. SURFACE FAILURES IN THE READINESS BAR, not as a modal:
     "Question 3 and question 5 don't read as real answers yet."

4. LOCALE-AWARE. The checks run against Arabic and English dictionaries and
   keyboard layouts. An Arabic answer must never fail a gate an equivalent
   English answer would pass.

5. LOG EVERY GATE FAILURE with the question id and which gate. That log tells
   you which questions are confusing enough that founders type placeholders —
   which is a content problem, not a founder problem.
```

## PROMPT B — The Rubric: Weights, Floors and a Zero That Works

```text
PAGE: The mission scoring service and the rubric prompt templates.

THE PROBLEM

Three things make the current rubric both too soft and too blunt.

  1. Nonsense scores 20. Language models are reluctant to award a zero — asked
     to rate out of 5 they return 1 rather than 0 almost every time. Nobody
     chose 20; it is an artefact of that reluctance, and it eats a fifth of
     the scale.

  2. The five criteria appear to be averaged evenly, in every mission. So
     Evidence is weighted the same in Mission 1 — where a founder cannot
     possibly have any — as in Mission 7, which is entirely about evidence.

  3. Averaging hides a hole. A founder scoring 5, 5, 5, 5, 0 averages 80 and
     passes with one criterion completely absent.

THE FIX

1. WEIGHT THE CRITERIA BY PHASE. Same five criteria everywhere so the score
   means one thing across the journey; the weights carry the difficulty curve.

                  Specificity  Depth  Evidence  Actionability  Relevance
     Discover  1-3     30        20       10         10            30
     Shape     4-6     25        25       15         15            20
     Test      7       20        20       30         15            15
     Model     8-10    20        25       20         20            15
     Readiness 11-15   20        20       30         20            10

   THE PASS MARK STAYS 70 EVERYWHERE. Do not vary the threshold per mission —
   70 must mean the same thing in Mission 1 and Mission 15, and a varying
   threshold lets founders shop for the easy mission.

2. ADD A FLOOR:

     pass = weightedScore >= 70
            AND every criterion weighted >= 20 in this phase scores >= 2 of 5

   Two out of five means "you attempted this". The floor does not raise
   difficulty; it stops one strength papering over one absence.

3. MAKE ZERO REACHABLE. In the rubric prompt, state the bottom of the scale
   explicitly and give an example that IS a zero:

     "0 means the response contains no attempt to answer the question —
      placeholder text, repeated characters, or text unrelated to what was
      asked. Award 0 without hesitation when it applies. Example of a 0:
      'dsad'."

4. ADD THE SUBSTITUTION TEST as an explicit instruction. This is the single
   most important line in the rubric:

     "Before scoring Specificity, apply this test: could this answer be pasted
      into a different founder's submission, in a different industry and a
      different country, without changing a single word? If yes, Specificity
      scores at most 1, however well written it is."

   Generic-but-plausible answers are the real threat, not gibberish. An answer
   like 'Our target users are young people who want a better and more
   convenient experience' is grammatical, on-topic, correctly long, and
   completely empty.

5. ANCHOR EVERY QUESTION WITH SCORED EXAMPLES. Written descriptions of quality
   drift on every call; examples do not. Each question carries a 0 / 1 / 3 / 5
   ladder embedded in its rubric prompt. For Mission 1 Q5, "What are the
   limitations of current solutions?":

     0  "dsad"
        Not an answer. Blocked by the gate, never scored.
     1  "They are expensive and slow."
        True of every product ever built. Fails the substitution test.
     3  "Existing budgeting apps are English-only and don't connect to
        Egyptian banks, so users type every transaction in by hand."
        Names a market, a concrete failure and a consequence.
     5  "The three apps students named to me all require a credit card at
        sign-up. Six of the nine students I spoke to in Cairo don't have one,
        so they never got past registration."
        Specific, sourced, quantified, consequence observed not assumed.

   A 3 PASSES. That is deliberate: 70 must be reachable by a founder who
   thought carefully and has not yet done fieldwork. A 5 requires having
   talked to someone.

   This ladder is needed for every question in all 15 missions. It is the
   largest task in this round and the one that determines whether any of the
   rest matters.

6. SIX RULES THAT KEEP IT FROM BECOMING TOO HARD:

   a. NEVER GRADE THE BUSINESS. Not the idea, not the market, not whether it
      will work. Only whether the founder did the thinking the question asks
      for. A brilliant answer about a doomed business scores well. The moment
      this rubric judges business quality it becomes an idea judge, which it
      is not competent to be.

   b. NEVER REQUIRE EVIDENCE A FOUNDER CANNOT HAVE YET. The phase weights
      handle this; do not let the prompt reintroduce it in words.

   c. NEVER PENALISE LANGUAGE. Grammar, spelling and vocabulary are not
      criteria. An Arabic answer and an English answer of equal substance
      score identically.

   d. NAME ONE FIX, NOT FIVE. The current mission page shows three feedback
      rows, a red banner and a highest-gain card at once. Return the single
      highest-gain change. Keep the rest available behind "see the full
      assessment".

   e. THE FEEDBACK MUST BE SUFFICIENT. If a founder does exactly what the
      feedback says, the result must reach 70. Feedback naming three fixes
      that together still land at 62 is lying to them.

   f. CAP THE EFFORT. If the question asks for two or three sentences, two or
      three good sentences must be able to score 4. A rubric that quietly
      rewards length teaches founders to pad, and padding degrades every
      criterion being measured.
```

## PROMPT C — Make the Same Answer Always Score the Same

```text
PAGE: The mission scoring service.

THE PROBLEM

A founder who resubmits identical text and receives a different score loses
trust in the entire assessment, permanently — and they will test this,
because a low score is the natural thing to retry.

THE FIX

1. TEMPERATURE 0 on every rubric call. Version the rubric prompt and store the
   version with each score, so an old score can be explained.

2. CACHE BY ANSWER HASH — DO NOT CALL THE MODEL FOR UNCHANGED TEXT.
   Round 15 already computes scoredHash = hash(answerValue + evidenceIds) per
   answer. If the hash is unchanged, return the stored score. Identical text
   becomes structurally incapable of scoring differently, and a resubmission
   costs only what actually changed.

3. BORDERLINE BAND. Any weighted score between 66 and 74 is scored twice and
   the LOWER result is used. Passing by rounding luck is worse than failing
   honestly, and this band is where nearly all the variance lands.

4. BANK PASSING QUESTIONS. A question scoring at or above the bar is marked
   Ready and is NOT re-scored on resubmission. A founder fixing question 3
   must never have question 1 come back lower for no reason they can see.

5. SHOW WHAT MOVED, per criterion, on every re-review:

     Attempt 2 · 65 / 100      up 45
       Question 5   Specificity  1 -> 4
                    Depth        1 -> 3
                    Evidence     0 -> 2   (screenshot attached)
       Question 1   banked, not re-scored

   If a criterion went DOWN, say so and name it. A rewrite losing specificity
   is the most common way a second attempt scores worse, and a founder will
   not spot it alone.

6. STORE THE FULL RESULT — per-criterion scores, the rubric version, the
   prompt hash, latency and token count. Without that record you cannot
   investigate a disputed score or measure a rubric change.
```

## PROMPT D — The Calibration Set

```text
PAGE: The evaluation harness (extend the existing one — do not build a second).

THE PROBLEM

There is currently no way to answer "is the pass mark set correctly?" other
than opinion. Any change to a rubric prompt could be making missions harder or
easier and nobody would know until founders started churning.

THE FIX

1. BUILD A LABELLED SET. For each of the 15 missions, 20 real answers scored
   by a human, drawn from actual submissions and anonymised:

     5  nonsense / placeholder
     5  generic but plausible — grammatical, on topic, empty
     5  borderline — genuine effort, unclear whether it should pass
     5  genuinely good

   The generic five are the most important and the hardest to collect. They
   are the answers that beat a rubric. Write them deliberately if real ones
   are scarce.

2. THE RUBRIC IS CALIBRATED WHEN:

     Nonsense    blocked at the gate, never scored   must never reach the model
     Generic     scores 25-45                        must never reach 70
     Borderline  scores 55-75                        no hard rule
     Good        scores 75-95                        must never fall below 70

3. FREEZE IT AS A REGRESSION TEST. Every rubric prompt change reruns the whole
   set. A change that moves more than two answers across the pass line does
   not ship until someone has looked at why.

4. TEST LANGUAGE PARITY EXPLICITLY. Twenty paired answers — the same substance
   written in Arabic and in English. The score difference must be within 5
   points. Do not assume this; measure it.

5. TEST FEEDBACK SUFFICIENCY. Take a stored borderline answer, apply exactly
   the fixes the feedback named, re-score it. If it does not reach 70, the
   feedback was insufficient and that is a bug in the rubric, not in the
   founder.

6. WATCH ONE PRODUCTION NUMBER: the share of founders who pass Mission 1
   within three attempts.

     below 60%   too hard — you are losing people at the front door
     around 75%  the target
     above 90%   too easy — the badge means nothing

   Chart it per mission. Any mission where the pass rate drops below 50% has
   a content problem, not a founder problem.
```

## PROMPT E — Show the Founder the Bar

```text
PAGE: /missions/:id — the question screen.

THE PROBLEM

Founders are being asked to hit a standard they have never seen. The page
tells them what a good answer needs — "Write 2-3 sentences explaining what
specifically fails" — which is genuinely helpful, and then leaves them to
guess what that looks like in practice.

The single cheapest way to raise scores is to show the bar. Not the answer —
the bar.

THE FIX

1. "SEE AN EXAMPLE" ON EVERY QUESTION, opening a panel with the anchor ladder
   from the rubric — the same examples the model is scored against:

     A weak answer    "They are expensive and slow."
                      Why: true of every product ever built.

     A passing answer "Existing budgeting apps are English-only and don't
                      connect to Egyptian banks, so users type every
                      transaction in by hand."
                      Why: names a market, a concrete failure, a consequence.

     A strong answer  "The three apps students named to me all require a
                      credit card at sign-up. Six of the nine students I spoke
                      to in Cairo don't have one, so they never got past
                      registration."
                      Why: specific, sourced, quantified.

   NEVER PRE-FILL AN EXAMPLE INTO THE FIELD. Show it in a panel the founder
   reads and closes. The examples must be from a DIFFERENT industry than the
   founder's, so they cannot be copied — a fintech founder sees a logistics
   example.

2. SHOW THE SUBSTITUTION TEST as a live self-check under the field, once the
   founder has typed something:

     "Could another founder in a different industry submit this same answer?
      If yes, add a name, a number or a place."

   One sentence, and it is the whole of specificity.

3. SHOW THE FLOOR, NOT JUST THE TOTAL. Replace the bare "20%" with the
   per-criterion picture, so a founder can see they are failing one thing
   rather than everything:

     Specificity   ██░░░  1/5   ← your weakest
     Depth         ██░░░  1/5
     Evidence      ░░░░░  0/5   ← nothing attached yet
     Actionability ███░░  2/5
     Relevance     ████░  3/5

   A founder looking at that knows what to do. A founder looking at "20%"
   knows only that they failed.

4. STATE THE DISTANCE PLAINLY:
     "You need 70. You're at 42. Fixing question 3 alone should get you there."
   Only say that when it is true — see PROMPT D rule 5.

5. ARABIC. Every anchor example exists in both languages, written natively in
   each. A translated example is not an example of good Arabic writing.
```

---

## Sequence

| # | Prompt | Why here |
|---|---|---|
| 1 | **A** — the gates | Stops random answers and costs nothing. Fixes the 20-point floor immediately |
| 2 | **B** — weights, floors, anchors | The calibration itself. The anchor ladders are the bulk of the work |
| 3 | **C** — consistency | Cheap once Round 15's hashes exist, and it makes B measurable |
| 4 | **D** — the calibration set | You cannot verify B without it |
| 5 | **E** — showing the bar | The largest single lift in pass rates, and it needs B's anchors to exist |

A is a day and removes the floor. B is the real work — 15 missions of anchor ladders — and nothing else in this round matters without it.

---

## Two decisions for you

**Should Mission 1 be easier than the rest?** I've recommended 70 everywhere, with the phase weights doing the work — Evidence is only 10% in Discover, so Mission 1 is already gentler without a special rule. The alternative is dropping Mission 1 to 60 outright. The argument for it: Mission 1 attempt 2 is where a founder decides whether this platform is for them, and a founder who fails it twice never comes back. The argument against: they learn the bar is low and are shocked at Mission 4. I'd hold at 70 and watch the pass rate instead — if it sits below 60% after a hundred founders, lower it with evidence rather than in advance.

**What happens at three failed attempts?** Right now, nothing — they can keep going forever. I'd keep it unlimited but change what's offered: after three attempts with no meaningful improvement, replace the resubmit helper line with an offer of the AI Mentor or a mentor session on that specific question. A fourth blind attempt helps nobody and costs you a model call. Whether that mentor session is free or paid is a pricing question, not a rubric one — but it's the moment a founder is most likely to pay for help, and most likely to leave if they don't get it.
