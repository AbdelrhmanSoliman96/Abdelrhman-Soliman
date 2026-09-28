"""
Infographics, as parametric SVG.

Every figure in the resource library is generated from data held in the document that
uses it, so a figure cannot drift away from the sentence beside it. Nothing here is
drawn by hand and nothing is a bitmap: each figure is vector, so it stays sharp when
a founder zooms in on a phone or prints the page.

Mark specification, applied uniformly
-------------------------------------
* bars are capped at 22px thick, with a 4px rounded data-end and a square baseline
* touching marks are separated by a 2px gap in the surface colour, never by a stroke
* gridlines are 1px, solid and recessive; there is never a second axis
* labels are selective, and a label is placed inside a mark only when the measured
  string fits with padding on both sides — otherwise it moves outside
* text never wears the data colour; identity comes from the mark beside the text
* colour is assigned by job: ordinal for stages, categorical for identity,
  emphasis-plus-grey when one item is the point

These are printed pages, so there is no hover layer to fall back on. That raises the
bar on direct labelling: every value a reader needs is on the page as type.
"""

from . import brand as B

W = 642            # the content column, in CSS px: 170mm at 96dpi
GAP = 2            # the surface gap that separates touching marks
BAR_MAX = 22       # bar thickness cap
RADIUS = 4         # rounded data-end

# Plus Jakarta Sans, measured across the ASCII range at weight 500. Used to decide
# whether a label fits inside a mark; deliberately a slight over-estimate so the
# decision errs toward moving the label out rather than clipping it.
_CHAR_W = 0.545


def text_width(s, size):
    return len(str(s)) * size * _CHAR_W


def wrap(s, size, width):
    """
    Break a string to a pixel width, and never drop a word.

    Every figure that lays out prose uses this and then sizes its container to the
    result. Capping the line count instead would silently truncate a sentence
    mid-word, which is the one layout failure a reader cannot detect or recover
    from — the page looks deliberate and the meaning is gone.
    """
    words, line, lines = str(s).split(), "", []
    for wd in words:
        probe = (line + " " + wd).strip()
        if text_width(probe, size) > width and line:
            lines.append(line)
            line = wd
        else:
            line = probe
    lines.append(line)
    return lines


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _svg(height, body, label=None):
    return (
        f'<svg class="fig" viewBox="0 0 {W} {height}" width="100%" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{esc(label or "figure")}">{body}</svg>'
    )


def _t(x, y, s, size=9, fill=None, weight=500, anchor="start", cls=""):
    fill = fill or B.INK_SECONDARY
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" class="{cls}">{esc(s)}</text>'
    )


def _rule(x1, y, x2, colour=None, width=1):
    colour = colour or B.CHART_GRID
    return (f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" '
            f'stroke="{colour}" stroke-width="{width}"/>')


def _bar(x, y, w, h, fill, r=RADIUS, side="right"):
    """A bar with a rounded data-end and a square baseline."""
    w = max(w, 0.6)
    if w <= r * 2:
        return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"/>'
    if side == "right":
        return (f'<path d="M{x:.1f} {y:.1f} H{x + w - r:.1f} A{r} {r} 0 0 1 {x + w:.1f} {y + r:.1f} '
                f'V{y + h - r:.1f} A{r} {r} 0 0 1 {x + w - r:.1f} {y + h:.1f} H{x:.1f} Z" fill="{fill}"/>')
    return (f'<path d="M{x + w:.1f} {y:.1f} H{x + r:.1f} A{r} {r} 0 0 0 {x:.1f} {y + r:.1f} '
            f'V{y + h - r:.1f} A{r} {r} 0 0 0 {x + r:.1f} {y + h:.1f} H{x + w:.1f} Z" fill="{fill}"/>')


def _col(x, y, w, h, fill, r=RADIUS):
    """A column: rounded cap, square foot."""
    h = max(h, 0.6)
    if h <= r * 2:
        return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"/>'
    return (f'<path d="M{x:.1f} {y + h:.1f} V{y + r:.1f} A{r} {r} 0 0 1 {x + r:.1f} {y:.1f} '
            f'H{x + w - r:.1f} A{r} {r} 0 0 1 {x + w:.1f} {y + r:.1f} V{y + h:.1f} Z" fill="{fill}"/>')


# The documented ordinal ramp's endpoints, in OKLCH. Steps between them are
# generated at even lightness rather than blended in RGB, because the ordinal rule
# is about lightness spacing and an RGB blend does not space evenly in lightness.
_RAMP_HUE = 272.6
_RAMP_L_LO, _RAMP_L_HI = 0.44, 0.76
MAX_ORDINAL_STEPS = 6   # beyond six, adjacent steps fall under the 0.06 lightness gap


def _oklch_rgb(L, C, H):
    """OKLCH to linear-light sRGB, unclamped, so the caller can test for gamut."""
    import math
    h = math.radians(H)
    a, b = C * math.cos(h), C * math.sin(h)
    m = [[1, 0.3963377774, 0.2158037573],
         [1, -0.1055613458, -0.0638541728],
         [1, -0.0894841775, -1.2914855480]]
    lms = [(m[i][0] * L + m[i][1] * a + m[i][2] * b) ** 3 for i in range(3)]
    n = [[4.0767416621, -3.3077115913, 0.2309699292],
         [-1.2684380046, 2.6097574011, -0.3413193965],
         [-0.0041960863, -0.7034186147, 1.7076147010]]
    return [sum(n[i][j] * lms[j] for j in range(3)) for i in range(3)]


def _oklch_hex(L, C, H):
    """
    OKLCH to a hex, with the chroma reduced until the colour is inside sRGB.

    Holding the hue and the lightness and giving up only chroma is what keeps the
    ramp a single hue with evenly spaced lightness, which is what the ordinal rule
    actually checks.
    """
    lo, hi = 0.0, C
    for _ in range(24):
        mid = (lo + hi) / 2
        if all(-1e-4 <= v <= 1 + 1e-4 for v in _oklch_rgb(L, mid, H)):
            lo = mid
        else:
            hi = mid
    out = []
    for v in _oklch_rgb(L, lo, H):
        v = max(0.0, min(1.0, v))
        v = 12.92 * v if v <= 0.0031308 else 1.055 * (v ** (1 / 2.4)) - 0.055
        out.append(max(0, min(255, round(v * 255))))
    return "#%02X%02X%02X" % tuple(out)


def _ordinal(i, n):
    """
    Pick an ordinal step so the ramp is walked end to end, whatever n is.

    Snapping to the nearest documented step gives two adjacent items the same
    colour once n exceeds the ramp length — a collapse exactly where the reader is
    being asked to see an order. Generating the step at an even lightness along the
    ramp's own hue keeps the single hue and the monotone, evenly spaced lightness
    the ordinal rule requires. The documented steps in brand.CHART_ORDINAL are the
    n = 5 case of this same construction, to within a rounding step.
    """
    if n <= 1:
        return B.CHART_ORDINAL[0]
    L = _RAMP_L_LO + (_RAMP_L_HI - _RAMP_L_LO) * i / (n - 1)
    return _oklch_hex(L, 0.30, _RAMP_HUE)


def _on_fill(fill):
    """White or ink on a fill, chosen by luminance so a label always clears contrast."""
    r, g, b = (int(fill[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    lum = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    return B.INK if lum > 0.42 else "#FFFFFF"


# --------------------------------------------------------------------- ribbon

def ribbon(active=()):
    """
    The fifteen-mission sweep, with the missions this document serves picked out.

    This is the brand's own ordinal device: position on the sweep is the meaning, so
    the reader places the document in the journey without reading a word. The dormant
    stops are held back rather than recoloured, which is the state rule from ch. 04.
    """
    active = set(active)
    h = 46   # every ribbon carries a figcaption, so it needs no caption of its own
    cell = (W - 14 * GAP) / 15
    out = []
    for i, colour in enumerate(B.MISSION_SPECTRUM):
        x = i * (cell + GAP)
        on = (i + 1) in active
        out.append(f'<rect x="{x:.1f}" y="14" width="{cell:.1f}" height="16" fill="{colour}" '
                   f'opacity="{1 if on else 0.22}" rx="2"/>')
        if on:
            out.append(_t(x + cell / 2, 43, f"{i + 1:02d}", 8.5, B.INK, 700, "middle"))
    out.append(_t(0, 8, "MISSION 01", 7.5, B.INK_FAINT, 600))
    out.append(_t(W, 8, "MISSION 15", 7.5, B.INK_FAINT, 600, "end"))
    return _svg(h, "".join(out), "The fifteen mission spectrum")


# --------------------------------------------------------------------- funnel

def funnel(stages, note=None):
    """
    An ordered narrowing: [(label, value, display), ...], widest first.

    Stage order is the meaning, so the colour job is ordinal — one hue, stepping
    darker as the funnel narrows — and every stage is direct-labelled, because a
    printed page has no tooltip to fall back on.
    """
    n = len(stages)
    row = 46
    h = 26 + n * row + (34 if note else 10)
    top = stages[0][1]
    out = []
    lab_w = 176
    track = W - lab_w - 96
    for i, (label, value, display) in enumerate(stages):
        y = 26 + i * row
        frac = (value / top) if top else 0
        w = max(track * frac, 3)
        colour = _ordinal(i, n)
        out.append(_bar(lab_w, y, w, BAR_MAX, colour))
        out.append(_t(0, y + 15, label, 9.4, B.INK, 600))
        # the value rides outside the bar end, always, so it can never be clipped
        out.append(_t(lab_w + w + 10, y + 15, display, 9.4, B.INK, 700))
        if i < n - 1:
            nxt = stages[i + 1][1]
            drop = (1 - nxt / value) * 100 if value else 0
            out.append(_t(0, y + 33, f"{drop:.1f}% do not continue", 8, B.INK_FAINT, 500))
    out.append(_t(0, 10, "STAGE", 7.5, B.INK_FAINT, 600))
    if note:
        out.append(_rule(0, h - 26, W))
        out.append(_t(0, h - 12, note, 8.2, B.INK_MUTED, 500))
    return _svg(h, "".join(out), "Funnel")


# ----------------------------------------------------------------------- bars

def bars(rows, unit="", emphasis=None, axis_max=None, note=None):
    """
    Horizontal bars, one series. [(label, value, display), ...].

    When `emphasis` names a row, that row carries the accent and every other row goes
    grey: one series being the point is emphasis, not identity, so no categorical
    hue is spent on it. Otherwise the whole series takes one hue — a single series
    needs no legend, because the caption already names what is plotted.
    """
    n = len(rows)
    row = 32
    h = 24 + n * row + (30 if note else 8)
    lab_w = 210
    track = W - lab_w - 92
    top = axis_max or max(r[1] for r in rows) or 1
    out = [_rule(lab_w, 16, lab_w + track, B.HAIRLINE)]
    for i, (label, value, display) in enumerate(rows):
        y = 24 + i * row
        w = max(track * value / top, 2)
        if emphasis is None:
            colour = B.CHART_EMPHASIS
        else:
            colour = B.CHART_EMPHASIS if label == emphasis else B.CHART_RECEDE
        out.append(_bar(lab_w, y, w, BAR_MAX - 2, colour))
        out.append(_t(0, y + 14, label, 9.2, B.INK, 600))
        out.append(_t(lab_w + w + 9, y + 14, display, 9.2, B.INK, 700))
    if unit:
        out.append(_t(lab_w, 10, unit.upper(), 7.5, B.INK_FAINT, 600))
    if note:
        out.append(_t(0, h - 8, note, 8.2, B.INK_MUTED, 500))
    return _svg(h, "".join(out), "Bar chart")


# ------------------------------------------------------------------- stat row

def stat_row(tiles):
    """
    A KPI row: [(value, label, source), ...]. Two to four tiles.

    A handful of headline numbers is a stat row, not a chart — there is no magnitude
    to compare across them, only figures to state. The source sits under each one,
    because a number without a source is a claim.
    """
    n = len(tiles)
    gap = 14
    tw = (W - gap * (n - 1)) / n
    labels = [wrap(label, 8.6, tw - 28) for _, label, _ in tiles]
    h = 70 + max(len(l) for l in labels) * 12 + 28
    out = []
    for i, (value, label, source) in enumerate(tiles):
        x = i * (tw + gap)
        out.append(f'<rect x="{x:.1f}" y="0" width="{tw:.1f}" height="{h}" fill="{B.WASH}" rx="3"/>')
        out.append(f'<rect x="{x:.1f}" y="0" width="{tw:.1f}" height="3" fill="{B.ULTRAVIOLET}" rx="1.5"/>')
        size = 30 if text_width(value, 30) < tw - 28 else 22
        out.append(_t(x + 14, 48, value, size, B.INK, 700))
        for j, ln in enumerate(labels[i]):
            out.append(_t(x + 14, 68 + j * 12, ln, 8.6, B.INK_SECONDARY, 500))
        out.append(_t(x + 14, h - 12, source, 7.4, B.INK_FAINT, 500))
    return _svg(h, "".join(out), "Key figures")


# ----------------------------------------------------------------------- ladder

def ladder(rungs, caption_low="WEAKEST", caption_high="STRONGEST"):
    """
    An ordered ladder, weakest at the foot: [(title, detail), ...].

    Rung order is the meaning, so the rungs take the ordinal ramp and the reader sees
    the order in the colour as well as in the position.
    """
    n = len(rungs)
    row = 44
    h = 30 + n * row + 8
    out = [_t(0, 10, caption_high, 7.5, B.INK_FAINT, 600),
           _t(0, h - 2, caption_low, 7.5, B.INK_FAINT, 600)]
    for i, (title, detail) in enumerate(rungs):
        colour = _ordinal(n - 1 - i, n)
        y = 22 + i * row
        out.append(f'<rect x="0" y="{y}" width="5" height="{row - GAP * 3}" fill="{colour}" rx="2.5"/>')
        out.append(_t(18, y + 13, title, 9.8, B.INK, 700))
        out.append(_t(18, y + 27, detail, 8.6, B.INK_MUTED, 500))
    return _svg(h, "".join(out), "Ranked ladder")


# ---------------------------------------------------------------------- nested

def nested(layers, note=None):
    """
    Concentric part-of-a-part: [(abbr, title, display, detail), ...], largest first.

    Nesting is the point — SAM is inside TAM, not beside it — so these are drawn as
    containment rather than as three bars, which would let a reader add them up.

    The boxes share a bottom edge and step in from the top left, which guarantees
    each label a clear band above the box nested inside it. Drawing them concentric
    on all four sides looks tidier and puts every outer label under an inner box.
    """
    n = len(layers)
    box_w, box_h = W * 0.56, 216
    step_x, step_y = 36, 46
    col_x = W * 0.62
    col_w = W - col_x
    rows = []
    for abbr, title, display, detail in layers:
        words, line, lines = detail.split(), "", []
        for wd in words:
            probe = (line + " " + wd).strip()
            if text_width(probe, 8.4) > col_w and line:
                lines.append(line); line = wd
            else:
                line = probe
        lines.append(line)
        rows.append(lines)

    block = max(len(r) for r in rows) * 11 + 22
    h = max(box_h + 16, 12 + n * block) + (26 if note else 6)

    out = []
    for i, (abbr, title, display, detail) in enumerate(layers):
        x, y = i * step_x, 8 + i * step_y
        w, bh = box_w - i * step_x * 2, box_h - i * step_y
        colour = _ordinal(i, n)
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{bh:.1f}" '
                   f'fill="{colour}" rx="4"/>')
        ink = _on_fill(colour)
        out.append(_t(x + 13, y + 20, abbr, 11.5, ink, 800))
        out.append(_t(x + 13, y + 36, display, 12.5, ink, 700))
        ly = 20 + i * block
        out.append(f'<rect x="{col_x:.1f}" y="{ly - 10:.1f}" width="3" height="11" '
                   f'fill="{colour}" rx="1.5"/>')
        out.append(_t(col_x + 10, ly, title, 9.4, B.INK, 700))
        for j, ln in enumerate(rows[i]):
            out.append(_t(col_x, ly + 14 + j * 11, ln, 8.4, B.INK_MUTED, 500))
    if note:
        out.append(_rule(0, h - 20, W))
        out.append(_t(0, h - 6, note, 8.2, B.INK_MUTED, 500))
    return _svg(h, "".join(out), "Nested market sizing")


# -------------------------------------------------------------------- timeline

def timeline(phases, span_label, unit="day"):
    """
    A single track cut into phases: [(name, start, length, detail), ...].

    One row, not a Gantt of parallel bars: these are sequential phases of one
    founder's month, and drawing them stacked would imply they run at the same time.
    """
    total = max(p[1] + p[2] for p in phases)
    h = 34 + len(phases) * 34 + 30
    out = [_t(0, 10, span_label.upper(), 7.5, B.INK_FAINT, 600)]
    track_y = 18
    for i, (name, start, length, detail) in enumerate(phases):
        x = W * start / total
        w = W * length / total - GAP
        colour = _ordinal(i, len(phases))
        out.append(f'<rect x="{x:.1f}" y="{track_y}" width="{max(w, 2):.1f}" height="14" '
                   f'fill="{colour}" rx="3"/>')
        label = f"{unit} {start + 1}" if length == 1 else f"{unit}s {start + 1}–{start + length}"
        ly = 52 + i * 34
        out.append(f'<rect x="0" y="{ly - 11}" width="4" height="26" fill="{colour}" rx="2"/>')
        out.append(_t(14, ly, f"{name}", 9.6, B.INK, 700))
        out.append(_t(14, ly + 13, detail, 8.4, B.INK_MUTED, 500))
        out.append(_t(W, ly, label, 8.4, B.INK_FAINT, 600, "end"))
    return _svg(h, "".join(out), "Timeline")


# ---------------------------------------------------------------------- matrix

def matrix(x_label, y_label, quads, note=None):
    """
    A two-by-two: quads is [top-left, top-right, bottom-left, bottom-right], each
    (title, detail, verdict). The quadrant a reader should act on carries the accent;
    the others stay in wash, because the contrast is the argument.

    Cell height is computed from the longest quadrant's wrapped text, so a long
    entry makes the whole grid taller rather than losing its last sentence.
    """
    gutter = 40
    cell = (W - gutter - GAP) / 2
    pad = 14
    wrapped = [wrap(d, 8.5, cell - pad * 2) for _, d, _ in quads]
    cell_h = max(72, 46 + max(len(w) for w in wrapped) * 12 + 10)
    h = cell_h * 2 + GAP + 34 + (22 if note else 0)

    out = []
    for idx, (cx, cy) in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)]):
        title, _, verdict = quads[idx]
        x = gutter + cx * (cell + GAP)
        y = cy * (cell_h + GAP)
        hot = verdict == "act"
        fill = B.ULTRAVIOLET if hot else B.WASH
        ink = "#FFFFFF" if hot else B.INK
        muted = "#D7D2FA" if hot else B.INK_MUTED
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell:.1f}" '
                   f'height="{cell_h:.1f}" fill="{fill}" rx="4"/>')
        out.append(_t(x + pad, y + 24, title, 10.4, ink, 700))
        for j, ln in enumerate(wrapped[idx]):
            out.append(_t(x + pad, y + 44 + j * 12, ln, 8.5, muted, 500))

    mid = (cell_h * 2 + GAP) / 2
    out.append(f'<text x="12" y="{mid:.1f}" font-size="7.5" font-weight="600" '
               f'fill="{B.INK_FAINT}" text-anchor="middle" '
               f'transform="rotate(-90 12 {mid:.1f})">{esc(y_label.upper())}</text>')
    out.append(_t(gutter + (W - gutter) / 2, cell_h * 2 + GAP + 20,
                  x_label.upper(), 7.5, B.INK_FAINT, 600, "middle"))
    if note:
        out.append(_t(0, h - 4, note, 8.2, B.INK_MUTED, 500))
    return _svg(h, "".join(out), "Two by two matrix")


# ------------------------------------------------------------------------ flow

def flow(steps, note=None):
    """
    A route: [(step, title, detail), ...] read left to right, wrapped in rows of
    three. The connector is the brand's progression line — it enters, travels, turns
    and resolves — rather than an arrow borrowed from outside the system.
    """
    per_row = 3 if len(steps) != 4 else 2
    rows = (len(steps) + per_row - 1) // per_row
    gap_x = 22
    bw = (W - gap_x * (per_row - 1)) / per_row
    wrapped = [wrap(d, 8.2, bw - 26) for _, _, d in steps]
    bh = 58 + max(len(w) for w in wrapped) * 11 + 10
    h = rows * bh + (rows - 1) * 18 + (22 if note else 0)
    out = []
    for i, (step, title, detail) in enumerate(steps):
        r, c = divmod(i, per_row)
        x = c * (bw + gap_x)
        y = r * (bh + 18)
        colour = _ordinal(i, len(steps))
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="{bh}" fill="{B.WASH}" rx="4"/>')
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="3.5" fill="{colour}" rx="1.75"/>')
        out.append(_t(x + 13, y + 26, step, 7.5, B.INK_FAINT, 700))
        out.append(_t(x + 13, y + 43, title, 10, B.INK, 700))
        for j, ln in enumerate(wrapped[i]):
            out.append(_t(x + 13, y + 58 + j * 11, ln, 8.2, B.INK_MUTED, 500))
        if c < per_row - 1 and i < len(steps) - 1:
            mx = x + bw + 4
            out.append(f'<path d="M{mx:.1f} {y + bh / 2:.1f} H{mx + 14:.1f}" stroke="{B.INK_FAINT}" '
                       f'stroke-width="2" stroke-linecap="round" fill="none"/>')
    if note:
        out.append(_t(0, h - 4, note, 8.2, B.INK_MUTED, 500))
    return _svg(h, "".join(out), "Process flow")


# --------------------------------------------------------------------- compare

def compare(left, right):
    """
    Two columns set against each other: (title, [items]) each. Used where the
    argument is a contrast — what counts and what does not — and a chart would
    invent a magnitude that is not in the data.
    """
    cw = (W - 18) / 2
    wrapped = [[wrap(i, 8.8, cw - 20) for i in side[1]] for side in (left, right)]
    row_h = max(len(w) for side in wrapped for w in side) * 11 + 19
    items = max(len(left[1]), len(right[1]))
    h = 44 + items * row_h
    out = []
    for k, (title, rows) in enumerate((left, right)):
        x = k * (cw + 18)
        accent = B.ULTRAVIOLET if k == 0 else B.INK_FAINT
        out.append(f'<rect x="{x:.1f}" y="0" width="{cw:.1f}" height="26" fill="{accent}" rx="3"/>')
        out.append(_t(x + 13, 17, title.upper(), 8.4, "#FFFFFF", 700))
        for j, item in enumerate(rows):
            y = 44 + j * row_h
            lines = wrapped[k][j]
            for m, ln in enumerate(lines):
                out.append(_t(x + 2, y + m * 11, ln, 8.8, B.INK if k == 0 else B.INK_MUTED, 500))
            out.append(_rule(x, y + row_h - 14, x + cw, B.HAIRLINE))
    return _svg(h, "".join(out), "Comparison")


# ----------------------------------------------------------------------- bands

def bands(segments, marker_label=None, marker_at=None, scale_max=100):
    """
    A scored scale cut into verdict bands: [(from, to, name, verdict), ...].

    A single ratio against a limit is a meter, not a pie and not a gauge. The bands
    carry the ordinal ramp; the reader's own score can be written onto the track.
    """
    y = 22
    laid = []
    tallest = 0
    for i, (lo, hi, name, verdict) in enumerate(segments):
        x = W * lo / scale_max
        w = W * (hi - lo) / scale_max - GAP
        # Each band's copy wraps to ITS OWN width. Wrapping every band to the average
        # lets a narrow band's text run on underneath its neighbour, which is the one
        # collision a reader cannot recover from.
        words, line, lines_ = verdict.split(), "", []
        for wd in words:
            probe = (line + " " + wd).strip()
            if text_width(probe, 8.2) > w - 6 and line:
                lines_.append(line); line = wd
            else:
                line = probe
        lines_.append(line)
        laid.append((x, w, name, lines_, _ordinal(i, len(segments))))
        tallest = max(tallest, len(lines_))

    h = y + 40 + tallest * 11 + 6
    out = [_t(0, 10, "YOUR SCORE", 7.5, B.INK_FAINT, 600)]
    for x, w, name, lines_, colour in laid:
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{max(w, 2):.1f}" height="26" fill="{colour}" rx="3"/>')
        ink = _on_fill(colour)
        # The band label already carries the score range, so no second range is drawn
        # beneath it: two ranges on one band read as a contradiction.
        if text_width(name, 8.6) < w - 16:
            out.append(_t(x + 10, y + 17, name, 8.6, ink, 700))
            first = y + 40
        else:
            out.append(_t(x, y + 40, name, 8.6, B.INK, 700))
            first = y + 51
        for j, ln in enumerate(lines_):
            out.append(_t(x, first + j * 11, ln, 8.2, B.INK_MUTED, 500))
    if marker_at is not None:
        mx = W * marker_at / scale_max
        out.append(f'<path d="M{mx:.1f} {y - 6} l5 -7 h-10 Z" fill="{B.INK}"/>')
        if marker_label:
            out.append(_t(mx, y - 16, marker_label, 8.2, B.INK, 700, "middle"))
    return _svg(h, "".join(out), "Score bands")


# ----------------------------------------------------------------------- stack

def stack(segments, total_label, note=None):
    """
    One bar, part to whole: [(name, value, display), ...].

    Segments touch, so each is separated from its neighbour by the 2px surface gap
    rather than by a stroke, and a segment is labelled inside only when the string
    measurably fits. A legend is always present, because there are two or more parts.
    """
    total = sum(s[1] for s in segments)
    h = 132
    out = [_t(0, 11, total_label.upper(), 7.5, B.INK_FAINT, 600)]
    x = 0.0
    for i, (name, value, display) in enumerate(segments):
        w = W * value / total - (GAP if i < len(segments) - 1 else 0)
        colour = _ordinal(i, len(segments))
        out.append(f'<rect x="{x:.1f}" y="20" width="{max(w, 1.5):.1f}" height="30" fill="{colour}"/>')
        ink = _on_fill(colour)
        if text_width(display, 9) < w - 14:
            out.append(_t(x + 8, 39, display, 9, ink, 700))
        x += w + GAP
    for i, (name, value, display) in enumerate(segments):
        ly = 72 + i * 19
        colour = _ordinal(i, len(segments))
        out.append(f'<rect x="0" y="{ly - 8}" width="10" height="10" fill="{colour}" rx="2"/>')
        out.append(_t(18, ly, name, 8.8, B.INK_SECONDARY, 500))
        out.append(_t(W, ly, display, 8.8, B.INK, 700, "end"))
    if note:
        out.append(_t(0, h - 2, note, 8.2, B.INK_MUTED, 500))
    return _svg(h, "".join(out), "Part to whole")


# ------------------------------------------------------------------ pillars

def pillars(items, note=None):
    """
    Four (or three) named principles side by side: [(n, word, meaning, test), ...].

    The brand book sets its four DNA words as four equal columns under one rule, and
    the equality is the point — none of them outranks another. Drawing them as a
    ranked list or a pyramid would say something the source does not.
    """
    n = len(items)
    gap = 12
    cw = (W - gap * (n - 1)) / n
    meanings = [wrap(m, 8.4, cw - 24) for _, _, m, _ in items]
    tests = [wrap(t, 8.2, cw - 24) for _, _, _, t in items]
    body = max(len(m) for m in meanings) * 11
    h = 58 + body + 16 + max(len(t) for t in tests) * 11 + 22 + (20 if note else 0)
    out = []
    for i, (num, word, meaning, test) in enumerate(items):
        x = i * (cw + gap)
        colour = _ordinal(i, n)
        out.append(f'<rect x="{x:.1f}" y="0" width="{cw:.1f}" height="4" fill="{colour}" rx="2"/>')
        out.append(_t(x, 22, num, 7.5, B.INK_FAINT, 700))
        out.append(_t(x, 42, word, 14, B.INK, 800))
        for j, ln in enumerate(meanings[i]):
            out.append(_t(x, 58 + j * 11, ln, 8.4, B.INK_SECONDARY, 500))
        ty = 58 + body + 14
        out.append(_rule(x, ty - 8, x + cw, B.HAIRLINE))
        out.append(_t(x, ty + 4, "THE FOUNDER TEST", 6.8, B.INK_FAINT, 700))
        for j, ln in enumerate(tests[i]):
            out.append(_t(x, ty + 17 + j * 11, ln, 8.2, B.INK_MUTED, 500))
    if note:
        out.append(_t(0, h - 4, note, 8.2, B.INK_MUTED, 500))
    return _svg(h, "".join(out), "Principles")


# ------------------------------------------------------------------- states

def states(items, note=None):
    """
    The three mission states, drawn by the book's own rules: [(name, meaning), ...].

    Dormant is held back at low opacity because nothing has been earned and the
    surface says so; in motion takes a mid-spectrum hue and is cropped off its frame,
    so movement is shown by the crop rather than by an arrow; resolved is solid lime,
    whole and centred, the only state that gets to be still.
    """
    n = len(items)
    gap = 14
    cw = (W - gap * (n - 1)) / n
    wrapped = [wrap(m, 8.6, cw - 8) for _, m in items]
    panel = 84
    h = panel + 26 + max(len(w) for w in wrapped) * 11 + (20 if note else 6)
    out = []
    for i, (name, meaning) in enumerate(items):
        x = i * (cw + gap)
        if i == 0:                       # dormant
            fill, opacity, ink = B.WASH, "1", B.INK_FAINT
        elif i == n - 1:                 # resolved
            fill, opacity, ink = B.LIME, "1", B.INK
        else:                            # in motion
            fill, opacity, ink = _ordinal(i, n + 1), "1", "#FFFFFF"
        out.append(f'<rect x="{x:.1f}" y="0" width="{cw:.1f}" height="{panel}" '
                   f'fill="{fill}" opacity="{opacity}" rx="4"/>')
        # the mark stands in as a block: held back, cropped, or whole and centred
        if i == 0:
            out.append(f'<rect x="{x + 18:.1f}" y="26" width="30" height="30" '
                       f'fill="{B.INK}" opacity="0.14" rx="3"/>')
        elif i == n - 1:
            out.append(f'<rect x="{x + cw / 2 - 17:.1f}" y="25" width="34" height="34" '
                       f'fill="{B.INK}" rx="3"/>')
        else:
            # Cropped hard and pushed off the frame: the movement is shown by the
            # crop, not by an arrow. The clip is a real clipPath bound to the
            # panel's own rectangle, so the mark is cut by the frame rather than
            # merely drawn to look as though it were.
            cid = f"crop{i}"
            out.append(f'<clipPath id="{cid}"><rect x="{x:.1f}" y="0" '
                       f'width="{cw:.1f}" height="{panel}" rx="4"/></clipPath>')
            out.append(f'<g clip-path="url(#{cid})">'
                       f'<rect x="{x + cw - 24:.1f}" y="20" width="46" height="46" '
                       f'fill="#FFFFFF" opacity="0.94" rx="4"/></g>')
        out.append(_t(x + 14, panel - 14, name.upper(), 8.2, ink, 700))
        for j, ln in enumerate(wrapped[i]):
            out.append(_t(x, panel + 20 + j * 11, ln, 8.6, B.INK_MUTED, 500))
    if note:
        out.append(_t(0, h - 4, note, 8.2, B.INK_MUTED, 500))
    return _svg(h, "".join(out), "Three states")


# --------------------------------------------------------------- progression

def progression(stages, note=None):
    """
    The progression line: [(label, meaning), ...] for enter, travel, turn, resolve.

    One line that enters, travels, turns and resolves at the mark. The turn is drawn
    where its own label sits, so the picture and the caption agree; its radius is the
    counter width, which is why the line reads as the same object the monogram is
    built from rather than as a decoration applied to it. One line is one founder.
    """
    n = len(stages)
    col_w = W / n
    wrapped = [wrap(m, 8.4, col_w - 14) for _, m in stages]
    y_hi, y_lo, radius = 22, 56, 14
    body_top = 78
    h = body_top + max(len(w) for w in wrapped) * 11 + (22 if note else 6)

    # the turn happens under the third column, and the line resolves under the last
    x_turn = (n - 2) * col_w
    x_end = (n - 1) * col_w + 22

    d = (f"M0 {y_lo} H{x_turn - radius:.1f} "
         f"A{radius} {radius} 0 0 0 {x_turn:.1f} {y_lo - radius:.1f} "
         f"V{y_hi + radius:.1f} "
         f"A{radius} {radius} 0 0 1 {x_turn + radius:.1f} {y_hi:.1f} "
         f"H{x_end:.1f}")
    out = [f'<path d="{d}" fill="none" stroke="{B.ULTRAVIOLET}" stroke-width="5" '
           f'stroke-linecap="round" stroke-linejoin="round"/>',
           f'<circle cx="{x_end + 9:.1f}" cy="{y_hi}" r="9" fill="{B.LIME}"/>']
    for i, (label, meaning) in enumerate(stages):
        x = i * col_w
        out.append(_t(x, 12, label.upper(), 7.5, B.INK_FAINT, 700))
        for j, ln in enumerate(wrapped[i]):
            out.append(_t(x, body_top + j * 11, ln, 8.4, B.INK_MUTED, 500))
    if note:
        out.append(_rule(0, h - 16, W))
        out.append(_t(0, h - 4, note, 8.2, B.INK_MUTED, 500))
    return _svg(h, "".join(out), "The progression line")


BUILDERS = {
    "ribbon": ribbon, "funnel": funnel, "bars": bars, "stat_row": stat_row,
    "ladder": ladder, "nested": nested, "timeline": timeline, "matrix": matrix,
    "flow": flow, "compare": compare, "bands": bands, "stack": stack,
    "pillars": pillars, "states": states, "progression": progression,
}
