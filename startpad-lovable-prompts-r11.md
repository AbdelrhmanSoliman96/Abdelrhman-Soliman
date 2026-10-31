# StartPad — Lovable Prompts (Round 11)

Two prompts: enforce real answers and evidence before submission, and brand every PDF export.

| Prompt | Scope |
|---|---|
| A | Mission submission gate |
| B | Branded PDF template across every export |

---

## The decision

Submission is gated. A founder cannot submit or resubmit until every question has a genuine answer and at least one piece of evidence is attached. That is the rule.

What this prompt does is make the gate **learnable instead of punitive** — the requirements are visible before they type, checked live as they write, and stated per question. The current version hides the rules until submit time, then tells the founder the wrong reason for the block.

One thing to watch after shipping: a hard gate on Mission 1 will reduce completion rate. That is the trade you're choosing — better answers from fewer people. Section 10 adds the telemetry so you can see the size of it and tune the thresholds rather than guess.

---
---

## PROMPT A — Require Real Answers and Evidence Before Submission

```text
PAGE: Mission runner (/mission/[n]) — the submission gate, the per-question
state, and the progress counters.

═══════════════════════════════════════════════════════════════
1. FIX THE CONTRADICTION FIRST
═══════════════════════════════════════════════════════════════

The page currently shows five signals that disagree:

  "5 of 5 tasks completed"              — 100%
  "5 of 5 answered · Last one. Finish strong and send it for review"
  "Progress saved 100%"
  "Fill the remaining questions to unlock review"   ← red, at Question 5
  "5 things to fix before you can submit"           ← every question listed
  [Resubmit for Review]                             ← disabled

All five questions contain text, so the counters read them as answered. None
passes the quality gate, so the button is disabled. Two different definitions
of the word "answered" in one screen.

  a) ONE DEFINITION. A question is "answered" only when it passes the gate.
     Every counter, progress bar and status line uses that definition. Nothing
     on this page counts non-empty text as answered.

  b) The counter reads "3 of 5 ready to submit", not "5 of 5 answered".

  c) DELETE the message "Fill the remaining questions to unlock review." It
     describes a condition that is not what is blocking. Replace with the real
     reason: "2 answers need more detail · 1 evidence file needed".

  d) The progress bar reflects questions PASSING, not questions containing
     characters.

═══════════════════════════════════════════════════════════════
2. WHAT COUNTS AS A REAL ANSWER — three layers
═══════════════════════════════════════════════════════════════

  LAYER 1 — LENGTH, PER QUESTION (not one global minimum)

  A blanket word count is wrong. "Fintech for gig workers in Egypt" is six
  words and is an excellent answer to "What industry are you interested in?".
  The same six words would be a poor answer to "What are the limitations of
  current solutions?".

  So: define min_words PER QUESTION in the mission schema, matched to what a
  good answer to THAT question actually requires. Suggested starting values
  for Mission 1:

    Q1  What area/industry are you interested in?        min 4 words
    Q2  Describe a specific problem you've observed      min 25 words
    Q3  Who is affected by this problem?                 min 15 words
    Q4  What solutions currently exist?                  min 25 words
    Q5  What are the limitations of current solutions?   min 25 words

  Store these in the mission config alongside the existing objectives and
  point values. Never hardcode a single number in the component.

  LAYER 2 — GIBBERISH DETECTION (client-side, instant, free)

  Length alone is gameable: "asdasd asdasd asdasd asdasd asdasd" passes any
  word count. Reject text that fails these heuristics:

    function looksLikeGibberish(text, locale) {
      const tokens = text.toLowerCase().match(/[\p{L}]+/gu) || [];
      if (tokens.length === 0) return true;

      // a) dictionary hit rate — real words vs invented strings
      const meaningful = tokens.filter(t => t.length > 2);
      const known = meaningful.filter(t => DICTIONARY[locale].has(t));
      const hitRate = meaningful.length ? known.length / meaningful.length : 0;

      // b) keyboard-adjacency runs — asdf, qwer, zxcv, and the Arabic
      //    layout equivalents
      const kbRuns = countAdjacentKeyRuns(text, locale);

      // c) repeated-token ratio
      const repeatRatio = 1 - (new Set(tokens).size / tokens.length);

      // d) character runs — aaaa, ....
      const charRun = /(.)\1{3,}/.test(text);

      return hitRate < 0.5 || kbRuns > 1 || repeatRatio > 0.6 || charRun;
    }

  This catches "sda", "dsad", "wdsdsas", "Ghh" — the exact strings currently
  in the database — without an API call.

  LAYER 3 — SEMANTIC CHECK (cheap model, on blur, not per keystroke)

  Layers 1 and 2 miss "I don't know yet" and "not sure about this one", which
  are real words of sufficient length. Run a fast, cheap classifier on blur
  that labels each answer:

    genuine_attempt | placeholder | evasion | off_topic

  Only genuine_attempt passes. Cache the result against a hash of the answer
  so re-checking unchanged text costs nothing. Use the cheap model here — this
  is classification, not evaluation. Never route it to the rubric model.

═══════════════════════════════════════════════════════════════
3. EVIDENCE IS REQUIRED — but broaden what counts
═══════════════════════════════════════════════════════════════

  At least one piece of evidence per mission before submission. Keep that.

  But "attach a file" is too narrow. A founder who ran three phone interviews
  has notes, not a screenshot. Accept any of:

    - A file: screenshot, PDF, deck, spreadsheet (already supported)
    - A LINK: a survey result, an article, a public post, a form response page
    - PASTED TEXT: interview notes, a conversation transcript, quotes
      (minimum ~50 words, and it goes through the same gibberish check)

  Label it "Add evidence" with the three options, not "Attach file".

  Say what it is for, once, above the control:
    "Evidence is what moves your Evidence score above 0. One screenshot,
     link, or set of interview notes is enough."

═══════════════════════════════════════════════════════════════
4. SHOW THE RULES BEFORE THEY TYPE, NOT AFTER THEY FAIL
═══════════════════════════════════════════════════════════════

  This is the difference between a gate that teaches and a gate that
  frustrates. Right now the requirements are invisible until the founder
  hits a disabled button.

  a) Under each question, BEFORE any typing, show what a passing answer needs:
       "At least 2-3 sentences. Name the specific industry and who it affects."
     Derive the sentence from the question's min_words and its rubric criteria.

  b) A LIVE counter under each field as they type:
       "18 / 25 words"  →  turns green and becomes "Ready ✓" when it passes
     Update on input, debounced. The founder should never be surprised.

  c) The existing "Ask AI Mentor · Not sure how to answer? The mentor will
     explain what a strong answer looks like" is exactly right. Surface it
     more prominently on any question that has failed the gate.

═══════════════════════════════════════════════════════════════
5. PER-QUESTION STATE, SHOWN INLINE
═══════════════════════════════════════════════════════════════

  Four states, each visible on the question itself and in the question
  stepper at the top:

    empty        grey    — nothing written
    too_short    amber   — "12 more words needed"
    needs_work   amber   — failed gibberish or semantic check:
                           "This doesn't look like a real answer yet"
    ready        green   — passes the gate

  The stepper dots (1-5) carry the same colours, so the founder can see at a
  glance which questions still need work without scrolling.

  Move the blocking reasons OUT of the list at the bottom of the page and ON
  TO each question. A list of five identical red bullets at the very bottom
  is the least useful place to put per-question feedback. Keep a short summary
  line above the submit button — "2 answers need more detail · evidence
  needed" — linking to the first failing question.

═══════════════════════════════════════════════════════════════
6. APPLY THE GATE TO THE FIRST SUBMISSION TOO
═══════════════════════════════════════════════════════════════

  The current account shows "Attempt 1 · Score 20%" — meaning "sda" and "dsad"
  WERE accepted and scored once, and are now blocked on resubmit. The founder
  experiences: "I submitted this before and got a score; now I can't submit it
  again."

  The gate must run identically on the first submission and every resubmission.
  Same rules, same messages, same states.

  For accounts that already have a low-quality attempt scored, do not delete
  their history — show the attempt, and show the gate on the next one.

═══════════════════════════════════════════════════════════════
7. ARABIC
═══════════════════════════════════════════════════════════════

  All three layers must work in Arabic:
    - Word counting must handle Arabic tokenisation, not split on spaces alone
    - The dictionary check needs an Arabic wordlist
    - Keyboard-adjacency detection needs the Arabic layout, not QWERTY
    - The semantic classifier must be prompted to evaluate Arabic natively,
      not by translating first
  A gate that rejects valid Arabic answers is far worse than no gate.

═══════════════════════════════════════════════════════════════
8. NEVER LOSE THEIR WORK
═══════════════════════════════════════════════════════════════

  - Failing answers still autosave. The gate blocks submission, never saving.
  - "Clear draft" needs a confirm dialog — it currently sits one click away
    from a page full of work.
  - Navigating away and returning restores everything, including failing
    answers and their state.

═══════════════════════════════════════════════════════════════
9. ONE ESCAPE HATCH
═══════════════════════════════════════════════════════════════

  If a founder fails the gate three times on the same question, offer help
  rather than a fourth rejection:

    "Stuck on this one? [Ask the AI Mentor] or [see an example answer]"

  The example is an anonymised real answer that scored well on this question.
  This is the single most effective thing you can add — founders cannot hit a
  standard they have never seen.

═══════════════════════════════════════════════════════════════
10. MEASURE THE COST OF THE GATE
═══════════════════════════════════════════════════════════════

  A hard gate will reduce Mission 1 completion. Instrument it so you can see
  by how much and tune rather than guess:

    - Gate rejections per question — which question fails most
    - Which layer rejected (length / gibberish / semantic)
    - Time from first gate failure to successful submission
    - ABANDONMENT: founders who hit the gate and never return within 7 days
    - Mission 1 completion rate, before and after this ships

  Put these on the admin dashboard. If abandonment on Question 2 spikes, its
  min_words is probably too high — that is a config change, not a redesign,
  which is why the thresholds live in the mission schema.
```

---

## After it ships

Two numbers tell you whether the gate is working:

**Average first-attempt score should rise.** If founders are forced to write real answers, attempt 1 should stop scoring 20%. If it doesn't move, the gate is filtering effort but not quality.

**Mission 1 abandonment should not spike.** If it does, the thresholds are too high or the requirements still aren't visible early enough — check which layer is rejecting most before changing any numbers.

---
---

## PROMPT B — One Branded PDF Template for Every Export

```text
PAGE: Every PDF, Markdown and CSV export in the product.

THE PROBLEM
Exports are generated in several places with no shared template and no
branding. A founder downloads their mission assessment, sends it to a mentor
or an investor, and it arrives as an unbranded document that could have come
from anywhere.

These files travel further than any screen in the product — they get emailed,
posted in WhatsApp groups, and attached to applications. They are the only
part of StartPad that reaches people who have never visited the site.

KNOWN EXPORT POINTS — audit for more:
  Mission assessment    "Download full report (PDF)" · "Export PDF" ·
                        "Export Markdown"
  Dashboard KPIs        "Export PDF"
  Loadout / Toolbox     downloadable canvases and models
  Resource Library      "Export CSV" · "Download Complete Toolkit"
  AI Tools              survey question exports (CSV, JSON)
  Knowledge Base        whitepaper and report PDFs (planned)

═══════════════════════════════════════════════════════════════
1. ONE SHARED TEMPLATE, NOT PER-EXPORT BRANDING
═══════════════════════════════════════════════════════════════

Build a single PDF document service that every export calls. Branding each
export separately is how they drift apart — the same pattern that produced
two Level systems and two roadmaps in this codebase.

  createPdf({
    docType,        // 'assessment' | 'kpi' | 'canvas' | 'report' | 'toolkit'
    title,          // "Mission 1: Problem Analysis — Assessment"
    subtitle,       // "Attempt 2 · Scored 74%"
    founderName,    // for personal documents
    locale,         // 'en' | 'ar'  → drives direction and fonts
    coverPage,      // boolean — long documents only
    sections        // the content
  })

No component generates its own PDF. If one does today, migrate it.

═══════════════════════════════════════════════════════════════
2. ASSET REQUIREMENTS
═══════════════════════════════════════════════════════════════

  - Primary logo as SVG (vector — it must stay sharp at any print size and
    when someone zooms in a PDF reader). A raster logo in a PDF looks cheap
    the moment it is magnified.
  - PNG at 3x as a fallback for renderers that mishandle SVG.
  - TWO LOCKUPS. The supplied mark is stacked (icon above wordmark), which is
    right for a cover page but too tall for a running header. Produce a
    HORIZONTAL lockup — icon left, wordmark right — for headers and footers.
    If one does not exist yet, that is the one asset to make before this ships.
  - A mono/single-colour version for any page where the document background
    is not white.
  - Store in one place, referenced by the template only.

═══════════════════════════════════════════════════════════════
3. PAGE FURNITURE
═══════════════════════════════════════════════════════════════

  HEADER (every page except the cover)
    Left:   horizontal logo lockup, ~24px tall
    Right:  document title, muted, smaller
    A hairline rule beneath, in the navy at low opacity

  FOOTER (every page)
    Left:   startpad.me
    Centre: "Page X of Y"
    Right:  generated date, e.g. "Generated 20 Aug 2026"
    Same hairline rule above

  COVER PAGE — for the full assessment report, whitepapers and the quarterly
  report only. Not for a one-page KPI export.
    Stacked logo, centred, upper third
    Document title
    Subtitle: mission name, attempt number, score
    Founder name and date
    "Structure Today, Scale Tomorrow." as a quiet strapline at the foot

  Keep the furniture light. This is a founder's working document, not a
  brochure — the logo should be present and unmistakable, never dominant.

═══════════════════════════════════════════════════════════════
4. TYPOGRAPHY AND COLOUR — match the product
═══════════════════════════════════════════════════════════════

  - Embed the fonts. A PDF that falls back to Helvetica on the recipient's
    machine loses the identity entirely.
  - Navy #0A1D34 for headings, green #047857 for accents and scores, neutral
    grey for body.
  - Score badges, rubric bars and criterion colours must match what the
    founder saw on screen. A 74% that is green in the app and grey in the PDF
    reads as two different results.

═══════════════════════════════════════════════════════════════
5. PDF METADATA — often skipped, always visible
═══════════════════════════════════════════════════════════════

  Set on every document:
    Title     "Mission 1: Problem Analysis — Assessment"
    Author    the founder's name
    Creator   "StartPad"
    Producer  "StartPad"
    Subject   one line describing the document
    Keywords  mission name, phase, StartPad

  This is what shows in a PDF reader's title bar, in email previews, and in
  search results. An untitled document displays as the raw filename.

═══════════════════════════════════════════════════════════════
6. FILENAMES
═══════════════════════════════════════════════════════════════

  Never "download.pdf" or "report.pdf". Use:

    StartPad_Mission-1_Assessment_Abdelrhman_2026-08-20.pdf
    StartPad_KPI-Summary_Abdelrhman_2026-08-20.pdf
    StartPad_Burn-Rate-Runway_2026-08-20.pdf

  Pattern: StartPad_[Document]_[Founder]_[ISO date]. Sanitise the name for
  filesystem-unsafe characters, and transliterate Arabic names rather than
  emitting non-ASCII filenames that break on some systems.

═══════════════════════════════════════════════════════════════
7. ARABIC DOCUMENTS
═══════════════════════════════════════════════════════════════

  When locale is Arabic:
    - The whole document is RTL: header logo moves right, page numbers mirror,
      tables and bars reverse
    - Embed an Arabic-native font (IBM Plex Sans Arabic, Noto Sans Arabic or
      Cairo) — never rely on a Latin font's Arabic fallback, which in PDF
      frequently renders as disconnected letterforms or empty boxes
    - Test that Arabic text is SELECTABLE and SEARCHABLE in the output, not
      rasterised. Many PDF generators silently convert Arabic to images.
    - Latin fragments inside Arabic text (a startup name, a URL) must not
      scramble — verify bidirectional handling explicitly

═══════════════════════════════════════════════════════════════
8. LAYOUT INTEGRITY
═══════════════════════════════════════════════════════════════

  - Never split a rubric criterion block across two pages
  - Never leave a heading alone at the foot of a page
  - Tables repeat their header row on every page they span
  - Charts render as vector where possible, at print resolution otherwise
  - Long founder answers wrap and flow rather than clipping — a truncated
    answer in an exported assessment is a real failure

═══════════════════════════════════════════════════════════════
9. NON-PDF EXPORTS
═══════════════════════════════════════════════════════════════

  MARKDOWN — cannot carry a logo, but should still be identifiable:
    A title line, the founder name, the date, and a link back to startpad.me
    at the top; a one-line attribution at the foot.

  CSV — a comment header row before the data:
    # StartPad — Resource Library export — 20 Aug 2026 — startpad.me
    Confirm the target tools tolerate it; if not, put the attribution in the
    filename and in a final row instead.

═══════════════════════════════════════════════════════════════
10. VERIFY
═══════════════════════════════════════════════════════════════

  Generate one of each document type in both English and Arabic and confirm:
    - The logo renders sharp at 400% zoom
    - Fonts are embedded (check document properties)
    - Metadata is populated
    - Arabic text is selectable, not an image
    - Page numbers are correct on multi-page documents
    - The filename is meaningful
    - Nothing is clipped or split across a page break

  Report which export points you migrated and which, if any, still generate
  their own PDFs.
```
