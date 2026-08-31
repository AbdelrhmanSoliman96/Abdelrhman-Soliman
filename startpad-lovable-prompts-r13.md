# StartPad — Lovable Prompts (Round 13)

Four prompts: token migration, component rollout, social assets, and the font pipeline.

Extracted from the brand guidelines PDF you uploaded. (The Google Drive folder is blocked by this environment's network policy, so everything below comes from the PDF itself — if the folder holds additional rules, send them and I'll fold them in.)

---

## What the guidelines contain

**Two typefaces: Satoshi for Latin, Zain for Arabic.** The PDF only embedded Zain, so my first read of this was wrong — the font packages settle it. Verified from the font binaries:

| | Satoshi | Zain |
|---|---|---|
| Latin A–Z a–z | 100% | 100% |
| Latin Extended-A | 89.8% | 7.8% |
| **Arabic (U+0600–06FF)** | **0%** | 42.6% |
| Arabic Presentation Forms-B | 0% | 61.8% |
| Arabic-Indic digits | 0% | 100% |
| Styles supplied | 10 (incl. italics) | 8 |
| Shaping tables (GSUB/GPOS) | present | present |
| Licence | **ITF / Fontshare — proprietary** | SIL OFL 1.1 |

Satoshi has no Arabic at all, and its geometric letterforms match the new `STARTPAD` wordmark. Zain has the Arabic and the Arabic-Indic digits. So it's a bilingual pairing, not one family doing both.

**Palette**, by frequency of use in the document:

| Role | Hex | Notes |
|---|---|---|
| Brand lime | `#CBF24A` | The mark. 66 uses. |
| Ink / near-black | `#0B0D10` | Wordmark and headings. 198 uses. |
| White | `#FFFFFF` | 237 uses. |
| Indigo | `#3418E0` | Secondary accent. 59 uses — a real system colour, not decoration. |
| Grey 500 | `#8A8F98` | 58 uses. |
| Paper | `#F4F4F2` | Off-white page ground. |
| Surface | `#EDEDEA` | |
| Grey 400 | `#A5A9AF` | |
| Grey 600 | `#5B6068` | |
| Grey 700 | `#3D424A` | |
| Cyan | `#00D4F0` / `#00A8C4` | Sparingly used. |

There's also a gradient running indigo → blue → cyan → teal → green → lime (`#3418E0` … `#CBF24A`), appearing once as a single swatch.

---

## The one thing that will break if you miss it

**Lime on white is a contrast ratio of 1.29:1.** WCAG AA requires 4.5:1 for text. Lime text on a white background is very close to invisible, and lime is your primary brand colour — so the natural instinct (make the buttons lime, make the links lime) produces an unusable site.

The numbers:

| Pairing | Ratio | Verdict |
|---|---|---|
| Lime `#CBF24A` on white | **1.29:1** | Fails everything. Never use. |
| Lime on ink `#0B0D10` | **15.1:1** | Excellent |
| Ink `#0B0D10` on lime | **15.1:1** | Excellent — this is the button |
| Indigo `#3418E0` on white | **8.9:1** | Excellent |
| White on indigo | **8.9:1** | Excellent |

So the working system is:

- **Lime is a surface, not ink.** It fills things — buttons, highlights, badges — and always carries **near-black text on top**. It is never text, never a border on white, never an icon on white.
- **Indigo is the accessible action colour.** White on indigo, or indigo as a link on white. It carries anything lime can't.
- **Near-black is the body ink.**

That's not a limitation of the brand — the logo already does exactly this, lime mark beside near-black wordmark. It just has to be stated explicitly or it will be got wrong across forty components.

---
---

## PROMPT A — Migrate the Design Tokens

```text
TASK: The brand has changed. Replace the entire colour and type system with
the new one. Tokens first — no component work in this prompt.

OLD (remove every trace):
  navy    #0A1D34
  green   #047857
  and any hardcoded variants of them

NEW PALETTE — define as CSS custom properties in one file, and mirror into the
Tailwind config so utilities are generated:

  BRAND
    --lime            #CBF24A     primary brand — a SURFACE colour, see rules
    --ink             #0B0D10     near-black, body and headings
    --indigo          #3418E0     accessible action colour
    --cyan            #00D4F0     accent, sparing
    --cyan-deep       #00A8C4

  NEUTRALS
    --white           #FFFFFF
    --paper           #F4F4F2     page background
    --surface         #EDEDEA     cards, raised areas
    --grey-400        #A5A9AF
    --grey-500        #8A8F98     secondary text
    --grey-600        #5B6068
    --grey-700        #3D424A

  GRADIENT (one swatch, from the guidelines)
    --gradient-brand: linear-gradient(90deg, #3418E0, #2B6BFF, #12B2F5,
                      #06DCC5, #4CE885, #CBF24A);

CONTRAST RULES — encode these, don't leave them to judgement:

  1. LIME IS NEVER TEXT AND NEVER AN ICON ON A LIGHT BACKGROUND.
     Lime on white measures 1.29:1. WCAG AA needs 4.5:1. It is effectively
     invisible.
  2. LIME IS A FILL. Anything lime carries --ink on top of it (15.1:1).
     Primary button = lime background, near-black label.
  3. INDIGO IS THE ACCESSIBLE ACTION COLOUR — white on indigo, or indigo as a
     link on white, both 8.9:1. Use it wherever a coloured element must sit on
     a light ground: links, focus rings, inline actions, chart series.
  4. Never place lime on cyan, lime on paper, or lime on any neutral lighter
     than --grey-600.

  Add a build-time or lint check that fails on --lime used as a text or border
  colour against a light background. This rule will otherwise be broken within
  a week.

SEMANTIC TOKENS — map roles, so components never reference raw brand colours:

    --bg-page          --paper
    --bg-surface       --white
    --bg-raised        --surface
    --text-primary     --ink
    --text-secondary   --grey-500
    --text-muted       --grey-400
    --border           --surface
    --action-primary-bg      --lime
    --action-primary-text    --ink
    --action-secondary-bg    --indigo
    --action-secondary-text  --white
    --link             --indigo
    --focus-ring       --indigo

  Keep success / warning / danger as a SEPARATE semantic set. Do not press lime
  into service as "success" — a brand colour doing double duty as a state
  colour is how the previous green ended up meaning eleven different things.

TYPOGRAPHY — two self-hosted families, resolved automatically by script.

  Satoshi carries Latin. Zain carries Arabic. Satoshi contains ZERO Arabic
  glyphs, so an Arabic page set in Satoshi renders as empty boxes.

  Do NOT branch fonts per locale in components. Use ONE family name and let
  unicode-range pick the right file per character — this also handles mixed
  strings (an English product name inside an Arabic sentence) correctly, with
  no conditional logic anywhere:

    /* Latin → Satoshi */
    @font-face {
      font-family: 'StartPad Sans';
      src: url('/fonts/Satoshi-Regular.woff2') format('woff2');
      font-weight: 400; font-style: normal; font-display: swap;
      unicode-range: U+0000-05FF, U+2000-206F, U+20A0-20CF, U+2100-214F;
    }
    /* Arabic → Zain */
    @font-face {
      font-family: 'StartPad Sans';
      src: url('/fonts/Zain-Regular.woff2') format('woff2');
      font-weight: 400; font-style: normal; font-display: swap;
      unicode-range: U+0600-06FF, U+0750-077F, U+08A0-08FF,
                     U+FB50-FDFF, U+FE70-FEFF;
    }
    /* repeat both blocks for every weight used */

    --font-display: 'StartPad Sans', system-ui, sans-serif;
    --font-body:    'StartPad Sans', system-ui, sans-serif;

  USE ONLY WEIGHTS BOTH FAMILIES HAVE. Satoshi ships Light 300, Regular 400,
  Medium 500, Bold 700, Black 900. Zain ships ExtraLight 200, Light 300,
  Regular 400, Bold 700, ExtraBold 800, Black 900 — it has NO 500. If the UI
  uses Medium, Arabic will synthesise or snap to another weight and look
  visibly different from the English.
    Permitted weights: 300, 400, 700, 900. Do not use 500.

  - Remove every previous Arabic stack — IBM Plex Sans Arabic, Noto Sans
    Arabic, Cairo. Zain replaces all of them.
  - Arabic still needs its own size and leading scale (~1.1x size, ~1.2x
    line-height) — set it on [lang="ar"], not in the font declaration.
  - Satoshi is NOT on Google Fonts and Zain must match it, so BOTH are
    self-hosted. Do not load either from a CDN.
  - The wordmark is ALL CAPS with wide tracking ("STARTPAD"). That is the LOGO
    lockup only — do not apply caps-and-tracking to headings.

DARK MODE
  Ink #0B0D10 becomes the page ground, paper and surface invert to dark greys,
  and lime stays lime — it is designed for dark grounds and performs best there.
  Indigo needs lightening on dark to stay legible; derive a --indigo-light
  rather than reusing #3418E0 on near-black.

DELIVERABLE FOR THIS PROMPT: the token files and the Tailwind config only,
plus a single swatch page at /styleguide rendering every token with its hex,
its contrast ratio against the grounds it is allowed on, and a pass/fail mark.
Do not touch components yet.
```

---
---

## PROMPT B — Roll the Brand Through the Product

```text
TASK: Apply the new tokens across every component and page. Audit-driven —
find every hardcoded colour first, then replace.

STEP 1 — AUDIT
  Search the codebase and both locale files for:
    #0A1D34, #047857, and every near variant
    any hex literal in a component (they should all be tokens)
    "navy", "emerald", "green-" utility classes
    inline style colour values
    SVG fills in icons and illustrations
    chart colour arrays
    email template colours
    the OG share image generator
  List every hit with file and line BEFORE changing anything. Report the count.

STEP 2 — LOGO REPLACEMENT
  The mark and wordmark have both changed. The old mark was a navy road/arrow
  forming an S with a teal leaf; the new one is a lime interlocking S/P form.
  The wordmark changed from "StartPad" title case to "STARTPAD" all caps.

  Replace every instance:
    - Public nav and app nav
    - Footer
    - Favicon and all touch icons (16, 32, 180, 192, 512)
    - The auth pages
    - The PDF export template (Round 11 Prompt B)
    - Email templates
    - OG / social share images
    - Loading and splash states
    - The manifest and any app-store assets

  Produce and store: SVG primary, SVG horizontal lockup, SVG mark-only,
  and a mono version. Check nothing still references the old asset path.

STEP 3 — COMPONENT MAPPING
  Work through these in order, using semantic tokens only:

    Buttons     primary   = lime bg + ink text
                secondary = indigo bg + white text
                tertiary  = ink text, no fill
                destructive stays in the danger set, never lime
    Links       indigo, underline on hover
    Focus rings indigo, 2px, 2px offset — visible on every interactive element
    Nav         ink on paper; active item marked with a lime underline or a
                lime pill carrying ink text, never lime text
    Cards       white on paper, --surface border
    Badges      lime bg + ink text for positive; the semantic set for states
    Progress    lime fill on a --surface track
    Charts      indigo → cyan → lime as the series order; that is the
                gradient's own sequence and it stays distinguishable in
                greyscale
    Inputs      --surface border, indigo focus ring
    Mission
    roadmap     completed = lime fill; current = indigo outline;
                locked = grey. Keep the two lock states distinct (Round 12).

STEP 4 — THE GRADIENT
  Use it sparingly — a hero band, the OG image, a report cover. Never behind
  body text. Never as a button fill; a gradient button cannot guarantee a
  contrast ratio across its own width.

STEP 5 — VERIFY
  - Run an automated contrast check across every rendered page. Report any
    pairing below 4.5:1 for text or 3:1 for UI. Zero failures is the bar.
  - Confirm no lime text or lime icon sits on any light ground anywhere.
  - Check both light and dark, both English and Arabic.
  - Screenshot every page before and after and report the list.

STEP 6 — ANYTHING WITH THE OLD BRAND BAKED IN
  Illustrations, the Knowledge Hub cover images, the AI Tools gradient header
  (which is currently purple and was already off-system), the empty-state
  icons. List what needs redrawing rather than recolouring.
```

---
---

## PROMPT C — Social Media Assets and Profiles

```text
TASK: Produce the social profile assets and copy for the new brand, and list
what needs uploading where.

CURRENT CHANNELS: Instagram, TikTok, X, LinkedIn (per the site footer).

═══════════════════════════════════════════════════════════════
1. PROFILE IMAGE — one design, all platforms
═══════════════════════════════════════════════════════════════

  The lime mark alone, centred, on near-black #0B0D10.
  - Mark occupies ~60% of the frame; the rest is breathing room
  - Every platform crops to a circle — keep the mark well inside a centred
    circular safe area, and test it cropped, not square
  - Never put the full wordmark in a profile image; "STARTPAD" is unreadable
    at 40px
  - Export at 1000×1000 PNG, plus 400×400 and 200×200

═══════════════════════════════════════════════════════════════
2. COVER IMAGES — per platform, exact dimensions
═══════════════════════════════════════════════════════════════

  LinkedIn company banner    1128 × 191   (very wide, very short)
  X header                   1500 × 500
  Facebook (if used)         820 × 312
  YouTube (if used)          2560 × 1440, safe area 1546 × 423

  DESIGN, one concept adapted per ratio:
    Ground:   near-black #0B0D10
    Element:  the brand gradient as a thin band or an abstract path across
              the lower third — this is where the gradient earns its place
    Left:     horizontal lockup — lime mark + white "STARTPAD"
    Right:    one line, in Zain Black, white:
                "From idea to launched startup — in 15 guided missions"
    Optional: a small lime chip reading "Built in Cairo · For MENA founders"

  RULES
    - LinkedIn's 1128×191 is extremely short. Do not shrink the wide design
      into it — lay it out separately, logo left, one short line right.
    - Every platform overlays the profile picture on the cover, usually lower
      left. Keep that corner empty in every version.
    - Mobile crops covers harder than desktop. Keep all content inside the
      centre 60% horizontally.
    - Produce an Arabic version of each with the layout mirrored RTL.

═══════════════════════════════════════════════════════════════
3. BIO COPY — written to each platform's character limit
═══════════════════════════════════════════════════════════════

  INSTAGRAM (150 chars)
    From idea to launched startup — 15 guided missions, AI feedback, and
    mentors who know MENA. Built in Cairo 🇪🇬
    → startpad.me

  TIKTOK (80 chars)
    15 missions from idea to launch. Built in Cairo, for MENA founders.

  X (160 chars)
    Turning ideas into startups across MENA — 15 guided missions with AI
    feedback and real mentors. Built in Cairo. startpad.me

  LINKEDIN TAGLINE (120 chars)
    The guided path from idea to launched startup, built for MENA founders.

  LINKEDIN ABOUT (~2,000 chars — write in full, structured as):
    Para 1  the group-chats origin line, adapted
    Para 2  what StartPad is: 15 missions, AI evaluation, mentors, community
    Para 3  who it's for and where
    Para 4  what's free and what's paid — be accurate, see Round 12
    Close   startpad.me

  Produce an Arabic version of every bio. Not a translation of the English —
  written natively, at the same character limits, which are tighter in Arabic
  than a word-for-word rendering allows.

═══════════════════════════════════════════════════════════════
4. POST TEMPLATES — so the brand survives daily posting
═══════════════════════════════════════════════════════════════

  Three reusable templates, each in 1080×1080 and 1080×1920:
    a) Quote / insight  — near-black ground, lime accent rule, Zain Black text
    b) Data point       — one big number in lime on near-black, source line
                          beneath (ties to the first-party data work)
    c) Founder feature  — photo, name, city, their mission number

  Every template: logo bottom-left, generous margins, and text large enough
  to read in a feed at thumbnail size. Deliver as editable files, not flats.

═══════════════════════════════════════════════════════════════
5. UPLOAD CHECKLIST
═══════════════════════════════════════════════════════════════

  Per platform: profile image · cover image · bio · link in bio · pinned post.
  Also update: the OG share image the site generates, the favicon set, the PDF
  template logo, email header logo, and any app-store listing.

  Report which assets you produced and which need a designer.
```

---

---
---

## PROMPT D — Build the Font Pipeline

```text
TASK: Prepare and self-host both font families. The supplied packages are
desktop formats — shipping them to the browser as-is would be a mistake.

WHAT WAS SUPPLIED
  Zain      8 TTF files   (SIL OFL 1.1, OFL.txt included)
  Satoshi  10 OTF files   (Indian Type Foundry / Fontshare, NO licence file)
  2.0 MB total, no WOFF2.

1. CONVERT TO WOFF2 — required, not optional.
   TTF and OTF on the web are roughly 2x the size of WOFF2 and are not the web
   format. Your audience is mobile-first on 4G in MENA; this is the single
   biggest performance item in the rebrand.
     woff2_compress Satoshi-Regular.otf   → Satoshi-Regular.woff2
   Convert only the weights actually used: 300, 400, 700, 900 for each family,
   plus italics only if the design genuinely uses them. Eight files, not
   eighteen.

2. SUBSET.
   Satoshi: keep Latin, Latin Extended-A, punctuation, currency symbols.
   Zain: keep Arabic, Arabic Presentation Forms-B, Arabic-Indic digits, and
   basic Latin (Arabic pages still contain Latin product names and URLs).
   Drop unused blocks. Subsetting plus WOFF2 should take the total web payload
   from ~2 MB to roughly 150-250 KB across all weights.

   CAUTION: do not over-subset Zain. Arabic shaping needs the GSUB and GPOS
   tables and the full set of contextual forms — a naive subset that strips
   them produces disconnected letterforms, which is the classic broken-Arabic
   bug. Use a subsetter with layout-feature awareness (pyftsubset with
   --layout-features='*') and verify visually afterwards.

3. PRELOAD only the two files needed for first paint — Satoshi Regular and
   Satoshi Black — with <link rel="preload" as="font" crossorigin>. Do not
   preload the Arabic files on an English page; unicode-range already prevents
   them downloading.

4. LICENSING — resolve before launch.
   Zain is SIL OFL 1.1. Ship OFL.txt alongside the font files in the deployed
   asset directory. That is a condition of the licence.

   Satoshi is NOT open source. Its embedded licence reads: "This Font Software
   is protected under domestic and international trademark and copyright law."
   It comes from Indian Type Foundry via Fontshare, whose terms permit free
   personal and commercial use including web embedding — but:
     - No licence file was included in the package. Download the Fontshare
       licence from fontshare.com/terms and keep it with the fonts.
     - Confirm self-hosting and web embedding are covered for commercial use
       before shipping, and keep a dated copy of the terms you relied on.
     - Satoshi cannot be redistributed the way an OFL font can, so do not
       commit it to a public repository without checking that first.
   Flag this to whoever owns legal. It is a five-minute check now and an
   awkward one later.

5. VERIFY, in the browser, not just in the build:
     - An English page renders in Satoshi
     - An Arabic page renders in Zain, correctly SHAPED and CONNECTED
     - A mixed string ("StartPad — منصة رواد الأعمال") renders each script in
       its own family, on one line, with correct bidirectional order
     - Arabic-Indic digits render if you use them
     - No FOIT: text is visible during load via font-display: swap
     - Network panel: only the needed files download per locale
     - Total font payload under 300 KB

  Report the final file list, per-file sizes, and the total.
```

---

## Two things worth confirming

**Is the AI Tools purple header staying?** It was already outside the old system, and the new brand has its own indigo `#3418E0`. Simplest path is to fold that page into the new tokens and drop the bespoke gradient — otherwise you have two unrelated purples.

**Weight scale.** Satoshi and Zain overlap on 300 / 400 / 700 / 900 only — Zain has no Medium 500. Decide now whether the UI lives inside those four weights, because adding 500 later means Arabic silently diverges from English on every screen that uses it.
