---
name: reel-maker
description: Turns a topic into a ready-to-shoot reel pack (hook, script, on-screen text, caption, call-to-action, test plan) using what 199 real reels have in common. Use for new reels, reel critiques or rewrites, adapting a reference reel, and reel post-mortems.
---

# Reel Maker

Supplied by the user. The reference files this text points to (references/hook-bank.md, script-templates.md, cta-and-caption.md, test-loop.md, evidence.md) were not supplied and are not in this repo. Brand rules in the Angelsta agent brief override anything below (for example, no engagement-bait keyword offers).

## What the evidence does and does not support

- The same hook got wildly different results (491K vs 5.1K; 1.26M vs 5.5K). Audience size and reel age dominate views. A hook is necessary, not sufficient. Never promise views.
- No craft choice separated a creator's best reel from their worst (hook length, question vs claim, duration, music, captions, cuts). The recipe below is table stakes. Differentiate on topic, specificity and proof.
- Two things did show up: a one-word comment keyword offer (median comments/views 1.6% vs 0.1%), and putting that call-to-action as line 1 of the post caption (1.9% vs 1.0%).

## How to work

Ask at most two questions, otherwise assume and state assumptions: topic, audience, what the viewer can get, on camera or screen-only, target length, goal.
Modes: new reel (produce the Reel Pack), critique/rewrite (score against the checklist, change as little as possible), adapt a reference (extract structure, write fresh wording, never reuse sentences), post-mortem.

## The recipe

- Length: median 41 s, middle half 29–52 s. Spoken words median 139 (98–184), about 3.4 words/second for a fast speaker.
- Hook: one sentence, median 13 words (9–17), mostly a bold claim, also shown as on-screen text at the start.
- Structure: hook, setup, value, proof, call-to-action. Proof beat in 69%, call-to-action beat in 89%.
- Captions: bold sans-serif, usually white, centred, word by word, one highlight colour.
- Editing: jump cuts ~60%, zoom-ins ~64%, sound effects ~51%, music 28%.
- Post caption: median 75 words, median 5 hashtags at the end.

## Hook

State one specific payoff or stake in the first sentence and prove it visually in the first frame: specific thing + surprising result + stake or cost, 17 words or fewer. Write 5 variants across at least 3 archetypes (gap, scarcity, gatekeeper warning, price anchor, rank claim, discovery, curiosity question, stakes, contrarian, instant tip, first-person proof, skit). Give each: spoken line, on-screen text at second 0, first-frame visual. Make one noun and one number concrete. Recommend one.

## Hold attention

Word budget: 15–30 s ≈ 85 words, 30–45 s ≈ 135, 45–60 s ≈ 175, 60–90 s ≈ 230. Change what is on screen every 3–4 s. Show the result before the explanation, or by mid-reel. One idea per beat. Finish with the payoff, then the call-to-action in the last two sentences.

## Convert

One short keyword tied to the topic, said in the last spoken sentence, shown on screen, and line 1 of the caption. A "like for more" or "send this to X" also worked. (Angelsta brief: no engagement bait, so use a clean closing statement instead.)

## Honesty and risk

Every claim in the hook must be shown in the reel. 40 of 200 reviewed reels were rated low credibility for staged screens, invented numbers or unsupported claims. Do not invent demos, statistics, earnings or screens. Disclose sponsorships.

## Reel Pack output format

```
# Reel pack: <working title>
Assumptions / Angle / Length
## Hooks (lead with #N): table of spoken, on-screen text at second 0, first-frame visual, archetype
## Script: table of beat, spoken, on-screen/visual, seconds
## Edit notes
## Post caption (copy-paste)
## Keyword
## Pre-publish checklist
## Test plan
```

Optional video production: when a finished video is requested, hand the pack to the available video workflow. In this repo the reel is rendered by `angelsta-social/post3/reel/` (voice with Piper, music synthesised, frames with Playwright, encode with ffmpeg).
