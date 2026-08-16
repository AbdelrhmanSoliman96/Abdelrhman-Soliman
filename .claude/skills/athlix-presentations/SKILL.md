---
name: athlix-presentations
description: "Build ANY Athlix presentation (.pptx) in Ali's preferred style — the dark tech-registry aesthetic, standard grids and card system, RTL/Arabic and LTR/English production rules, FrutigerLT Arabic + Poppins typography, logo usage, and every PowerPoint pitfall learned the hard way. Always check the project's local files first for media, logos, and reference material before asking or generating. Use whenever creating or editing slides for أثلِكس / Athlix, regardless of which deck, language, or how many slides. Read alongside athlix-brand-identity."
---

# Athlix Presentations — Ali's Deck Style

Applies to **any** Athlix presentation, new or existing, Arabic or English. This skill captures *how Ali likes decks built* — never the state of a specific file (slide counts, per-slide decisions, and file inventories are session context, not skill content; do not write them back here). Read **alongside** `athlix-brand-identity`, which owns colours, typography, logo rules, tone, and values.

---

# 1 · The signature look

Dark, technical, "national data registry" aesthetic. Slide canvas **1440 × 810**.

**Background** — 45° diagonal gradient `#0A0A1F` → `#120E2B` → `#061C33`. These three are *outside* the 13 approved brand colours; they are an approved exception for deck backgrounds only. Flag before using them anywhere else, don't silently extend.

**Node mesh** (background texture) — ~30 nodes + ~35 connecting lines. Lines `#14C2F3` at 10%, weight 0.75, no glow. Every 5th node large: 8pt `#09D9D8` at 20%; the rest 4.5pt `#14C2F3` at 10%. Glow only on large nodes near the top or bottom edge — radius 6, intensity 22%. Any node behind a title or logo dims to 5%.

**Top bar** — height 44, fill `#0A0A1F`, `#14C2F3` 30% rule beneath. Three 8pt squares top-right; a decorative `athlix://` path in Consolas 11pt at left (**not** the website — never rewrite it when changing the domain).

**Identity block** — «أثلِكس» 20pt white top-left area; small X mark beside it; tagline 13pt `#3CEF70` beneath.

**Titles** — 30pt white, right-aligned (RTL), near the top. Subtitle 15pt `#A2DDF8` under it.

**Cards** — 60pt outer margins, 24pt gutters. Fill white @4%, border `#14C2F3` @18%, 4pt vertical `#14C2F3` accent bar on the **right** edge (RTL). Card header band `#14C2F3` @11% with a 26% bottom rule.

**Text hierarchy** — card titles 18–20pt white; body 14–16pt `#A2DDF8`. Nothing under 14pt. Latin numerals throughout. Parallel rows top-aligned.

**Icons** — vector only, 22–34pt, `#14C2F3`, no background or border, placed at the end opposite the title.

**Footer** — `#14C2F3` 22% rule near the bottom. Page number left; site + document label right.

**Cover / section-divider slides** — no top bar, no footer: full-bleed gradient, centred lockup, title. Check any cover for inherited chrome and strip it.

**Colour discipline** — the 13 approved brand colours only (see `athlix-brand-identity`), including line/border colours, not just fills. Green `#3CEF70` is reserved for status indicators and the tagline.

---

# 2 · Typography

Arabic: **FrutigerLT Arabic** (approved 12 Aug 2026) — the weight is part of the family name:
- headings/emphasis → `FrutigerLT Arabic 65 Bold`
- body/regular → `FrutigerLT Arabic 55 Roman`
- muted/secondary → `FrutigerLT Arabic 45 Light`

Latin: **Poppins**. Logo wordmark only: Good Timing W00 Light.

Alinma Display and Tajawal are retired. If either appears in an existing file, flag it and offer a font sweep. Before any sweep, verify the exact installed family names in PowerPoint's own font list — file names on disk (`FrutigerLT Arabic65Bold`, `FrutigerLTArabic45Light`, `FrutigerLTArabic55Roman`) have inconsistent spacing and may differ from the internal family names.

---

# 3 · Standard grids (1440 × 810, RTL baseline)

**Icon sheet** — 8 cols × 3 rows = 24 icons.
`cellW = 165`, `cellX = 1380 − 165 − c*165`, rows `y = 230 + r*170`.
Icon 52pt at `x + 56.5`, `y + 14`. Label box `x, y + 78, 165 × 24`, 14pt `#A2DDF8`, `algn="ctr" rtl="0"`, English one-word names, no descriptions.
Title `620,64,760,48` 30pt white; subtitle `620,116,760,26` 16pt `#A2DDF8`.

**Card grid (3 cols)** — `w = 424`, `x = 956 / 508 / 60`, gutter 24.
**Card grid (4 cols)** — `w = 312`, `x = 1068 / 732 / 396 / 60`.
**Swatch grid (7 cols)** — `w = 171`, gap 20, `x = 1380 − 171 − c*191`.

**Hairline rules** — `#14C2F3` @ 16–22% alpha, 1pt.

---

# 3b · English / LTR decks

Everything in this skill applies to English decks too — same aesthetic, colours, cards, icons, pitfalls — with the direction mirrored:

- **Mirror all geometry:** titles left-aligned, card accent bar on the **left** edge, grids laid left→right (recompute the §3 x-values mirrored around the 1440 canvas; same widths and gutters).
- **Font:** Poppins throughout (Bold → headings, Regular → body, Light → muted), replacing FrutigerLT Arabic role-for-role.
- **Skip §5 entirely** — no `rtl` flags, no `ar-SA`, no number-reversal workarounds. Plain LTR text.
- Bilingual decks: apply each language's rules per text run; the slide direction follows its primary language.

---

# 4 · Media, logos & source material — project files FIRST

**Rule 1 — local project files are the first stop for ALL media.** Before asking Ali for any image, logo, pattern, or visual asset — and before generating or drawing a substitute — **search the project's local files first** (the Claude Project knowledge / mounted project directory, e.g. `/mnt/project/`, and any files uploaded this session). Only if the needed asset is genuinely not there: say so explicitly and ask Ali — never silently generate a replacement.

**Rule 2 — PDFs in the project are working material, not just references.** Use them two ways as fits the task:
- **Ideas & content:** extract concepts, structure, wording, and data from them to inform the slides.
- **Images:** crop/extract images, logos, diagrams, or visual elements directly out of PDF pages (render the page, crop the region, use as PNG) when suitable for the deck.

**Rule 3 — when Ali says "work on X":** review the relevant local project files for X first, and build the slides from what's actually in them — don't work from memory or assumptions while a source file is sitting in the project.

**Logo usage:** on the dark gradient always use a white/`-w` transparent PNG variant; never a white-matted JPG. Clear space = 0.5× logo height on all four sides. The bilingual stacked lockup (player + `Athlix` + `أثلِكس`) is the primary choice for covers and title slides. The rounded-square app-icon tile is for app-store mockups only — never placed on the gradient as if transparent, never recoloured. If no logo file is found in the project or session, ask Ali to upload one — a logo is never redrawn or approximated.

**Official contact details** for closing slides and footers: **AthlixTalent.com** · +966 54 0000 500 · info@AthlixTalent.com · Riyadh – Saudi Arabia. Any older domain (athlix.sa, www.athlix.com) is obsolete — sweep it out if found.

---

# 5 · RTL / Arabic production rules (mandatory for Arabic decks)

1. Every Arabic paragraph: `rtl="1"` on `<a:pPr>`; every run: `lang="ar-SA"` on `<a:rPr>` / `<a:endParaRPr>`. A file missing these *displays* fine but corrupts the moment the user clicks into edit mode.
2. **Arabic-Indic page numbers** («٠٢») render reversed in an RTL paragraph — set `rtl="0"` on that paragraph only.
3. **Numbers inside Arabic runs reverse** (`1440 × 810` → `810 × 1440`). Any run containing digits, `×`, or `·` needs `lang="en-US"` **and** `rtl="0"`. A single bare number inside Arabic prose is fine.
4. **`rtl="0"` doesn't always take** inside layout placeholders. When it fails, keep `rtl="1"` and join the Latin token with non-breaking spaces (`&#160;`): `+966&#160;54&#160;0000&#160;500`.
5. **Never use bidi control characters** (`U+202A`/`U+202C`, `&#8234;`/`&#8236;`) — they render as visible tofu boxes.
6. Write text only via `edit_slide_xml` / `edit_slide_text` with `rtl="1"` and `lang="ar-SA"`; Office.js `textRange.text` strips formatting and breaks RTL.

---

# 6 · PowerPoint pitfalls (learned the hard way — never relearn)

**Template & layouts**
1. **Layouts get pruned.** PowerPoint deletes any layout no slide uses on the next export/import cycle — `preserve="1"` does NOT reliably prevent it. Keep a slide on each layout or re-verify the list.
2. **Layout file numbers are unstable.** Locate a layout by `<p:cSld name="...">`, never by filename.
3. **Changing a slide's layout does not remove its shapes.** Build reusable pages from *placeholders* if the layout may change later.
4. **Placeholder prompt text never renders** in exports or presentation mode — an empty layout-based slide screenshots blank. Not a bug.

**Editing order**
5. **`edit_slide_text` re-imports the slide and resets shape positions** set earlier via Office.js on that slide. Text edits **first**, then re-apply `.top`/`.left` in a following `execute_office_js`.

**Shapes & charts**
6. **`varyColors`** — PowerPoint injects `<c:varyColors val="1"/>` into bar/line charts on reimport. Set it to `0` for bar/line; leave `1` for pie/doughnut.
7. **Helper arg-count bugs are fatal, not cosmetic.** A wrong argument in a `body` slot injects a raw number into `<p:txBody>`; the slide reimports as `InvalidArgument` with no hint of the cause.
8. **`leftRightArrow` in a square box renders as a plain diamond.** Use a wide box (~96×40) with `adj1=45000, adj2=28000`.
9. **`circularArrow` is unreliable** — renders as a headless arc. Use `uturnArrow`.

**Icons**
10. **Icons are `Graphic` type, not `Image`.** Filter `shape.type === "Graphic"`.
11. **`insert_icon` chains slide IDs** — passing the same (stale) `slide_id` to several parallel calls works. Batch 4–6 per turn.
12. **`insert_icon` only accepts ids returned by `search_icons` in the current session.** A remembered id fails with `NotFoundError`.
13. **Some icons ignore the `color` parameter or ship near-black** (`Icons_NoSign`, `Icons_OnlineMeeting_M`). Swap the id, or draw the mark as vector shapes.
14. **Prefer `_M` (mono) variants throughout a sheet** — one solid-filled icon among line icons is immediately visible.
15. **Recolour existing SVG icons** by injecting `<style type="text/css" id="iconRecolor">path,rect,circle,polygon,ellipse,line,polyline{fill:#14C2F3;stroke:#14C2F3;}</style>` after the `<svg>` tag. Never use HTML comments in sandbox code.
16. **Microsoft's `Icons_Football` is American football.** Use `Icons_Soccer_M`, `Icons_SoccerPlayer_M`, `Icons_SoccerGoal_M`.

**Verification**
17. **`verify_slides` contrast warnings ignore alpha** — white @4% over the dark gradient reports as "white on white". Only recolour text sitting on a genuinely **solid** light fill.
18. The visual reviewer over-reports low contrast on muted `#A2DDF8` chrome and "empty band at the bottom" on standard-grid pages. Confirm against the screenshot before acting.
19. Ignore font-size complaints from the downscaled render — check real values with `read_slide_text`.

**Duplication & sweeps**
20. **Duplicating a page carries its icons too.** After `duplicate_slide`, delete shapes where `type === "Graphic"` before inserting the new set.
21. **Deck-wide string changes** (domain, product name, font name): sweep **all** `*.xml` parts in one pass — inventory with a regex first, then replace. Layout chrome and slide content are different surfaces — scan both.

---

# 7 · Working rhythm

For each new page: duplicate the nearest finished page (or build from a layout's placeholders) → one `execute_office_js` to strip old content shapes by name prefix or type → one `edit_slide_xml` to lay out every frame and write every text run and alpha tint → `verify_slide_visual`.

Name every shape with a stable prefix (`card.`, `gd.`, `ico.`, `act.`, `pf.`, `mx.`, `og.`, `jn.`) so the next duplicate-and-clear cycle can find and remove them precisely.

Done when: geometry matches §1 and §3 (or its §3b mirror for English), every colour is one of the 13 (or an explicitly-flagged exception), no cover slide carries header/footer chrome, no text is under 14pt, all media came from project files (or Ali was asked), and `verify_slide_visual` reports no overlap or overflow.