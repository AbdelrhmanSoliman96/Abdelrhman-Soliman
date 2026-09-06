# StartPad — Facebook page covers

Rendered with headless Chromium from `cover-source.html`, using the real
Satoshi and Zain files and the logo extracted from the brand guidelines.

## Files

| File | Use |
|---|---|
| `..._Cover_Lockup_1640x624.png` | Lockup above the headline. **Recommended.** |
| `..._Cover_Mark_1640x624.png` | Mark-led, headline dominant |
| `..._Cover_Arabic_1640x624.png` | Arabic, RTL, set in Zain |

820×312 versions included. **Upload the 1640×624** — it is Facebook's
recommended size and downscales cleanly to every crop.

## Why everything is centred

Facebook's crop rules differ from LinkedIn's in two ways that matter:

1. **The profile photo moves.** It overlays the lower-LEFT on desktop and
   the bottom-CENTRE on mobile. So the whole bottom band is unusable, not
   just one corner.
2. **Mobile crops the sides.** Desktop shows 820×312; mobile shows a
   narrower, relatively taller crop of the centre.

So all content sits inside a centred ~600px column and is lifted to 42%
height — clear of the profile photo on both layouts, and safe against the
mobile side-crop. The lower third is intentionally empty.

## Brand

Ground `#0B0D10` · lime `#CBF24A` on the highlight and kicker · grey-400
`#A5A9AF` supporting line · bottom rule is the brand gradient
`#3418E0` → `#CBF24A`. Lime only ever appears on the near-black ground.

Type: Satoshi Black 900 / Bold 700 / Medium 500 for English; Zain Black
900 / Regular 400 for Arabic. Western digits used in both, matching the
rest of the brand.

## Re-rendering

    npm install playwright
    NODE_PATH=./node_modules node render.js
