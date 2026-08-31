# StartPad — LinkedIn covers

Rendered with headless Chromium from `cover-source.html`, using the real
Satoshi and Zain files. Palette taken from the brand guidelines PDF.

## Files

| File | Size | Use |
|---|---|---|
| `StartPad_LinkedIn_CompanyCover_1128x191.png` | 1128×191 | Company page cover |
| `StartPad_LinkedIn_CompanyCover_Wordmark_1128x191.png` | 1128×191 | Company page, wordmark variant |
| `StartPad_LinkedIn_ProfileCover_1584x396.png` | 1584×396 | Personal profile background |

`@2x` versions are provided for retina. Upload the @2x file — LinkedIn
downscales cleanly and the result is sharper on high-DPI screens.

## Colours used

- Ground `#0B0D10`
- Lime `#CBF24A` — headline highlight, kicker, chip
- Grey-400 `#A5A9AF` — supporting line
- Bottom rule: the brand gradient, `#3418E0` → `#CBF24A`

Lime never appears as body text on a light ground; on this near-black
ground it measures well above AA.

## Type

Satoshi throughout — Black 900 for the headline and wordmark, Bold 700
for the kicker, Medium 500 for the supporting line. Zain is loaded in the
source file and ready for an Arabic version.

## Safe areas

- **Company cover:** the page logo overlays the lower-left. The left 272px
  is deliberately empty.
- **Profile cover:** the profile photo overlays the lower-left. Content
  starts at x=560 to clear it.
- LinkedIn crops covers harder on mobile — nothing critical sits in the
  outer 15% on either side.

## Swapping in the real logo

The lime tile in the profile version is a **placeholder**. Open
`cover-source.html`, replace the contents of `<div class="mark">` with the
real logo SVG, then re-render:

    npm install playwright
    NODE_PATH=./node_modules node render.js

To produce an Arabic version, set `dir="rtl"` on the stage, swap the copy,
and change `font-family` to `'Zain'` — the file is already loaded.
