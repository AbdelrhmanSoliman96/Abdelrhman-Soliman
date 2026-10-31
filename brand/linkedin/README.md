# StartPad — LinkedIn covers

Rendered with headless Chromium from `cover-source.html`, using the real
Satoshi files and the logo extracted from the brand guidelines PDF.

## Files

| File | Size | Notes |
|---|---|---|
| `..._CompanyCover_Mark_1128x191.png` | 1128×191 | Mark + message. **Recommended.** |
| `..._CompanyCover_Lockup_1128x191.png` | 1128×191 | Message left, full lockup right |
| `..._CompanyCover_1128x191.png` | 1128×191 | Message only |
| `..._ProfileCover_1584x396.png` | 1584×396 | Personal profile background |

`@2x` versions included — upload those, LinkedIn downscales cleanly.

## Safe areas

- **Company cover:** the page logo overlays the lower-left, so the left
  272px is kept clear.
- **Profile cover:** the profile photo overlays the lower-left, so the
  message starts at x=560.
- Nothing critical sits in the outer 15% — LinkedIn crops harder on mobile.

## Brand

Ground `#0B0D10` · lime `#CBF24A` for the highlight, kicker and chip ·
grey-400 `#A5A9AF` for the supporting line · bottom rule is the brand
gradient `#3418E0` → `#CBF24A`.

Type is Satoshi: Black 900 headline, Bold 700 kicker, Medium 500 sub.
Lime is only ever used on the near-black ground, never as text on light.

## Logo assets

Extracted from the guidelines PDF at full resolution with transparency,
in `../logo/`:

- `StartPad_Lockup_Horizontal_Dark_2001x507.png` — for light backgrounds
- `StartPad_Lockup_Horizontal_Reversed_2001x507.png` — wordmark recoloured
  to white, mark untouched, for dark backgrounds
- `StartPad_Mark_369x507.png` — mark only

These are raster. Ask whoever produced the guidelines for the source SVG
or AI file before using them anywhere they'll be scaled up — favicons,
print, or large-format.

## Re-rendering

    npm install playwright
    NODE_PATH=./node_modules node render.js

For an Arabic version: set `dir="rtl"` on the stage, swap the copy, and
change `font-family` to `'Zain'` — it is already loaded in the source.
