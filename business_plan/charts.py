"""
Every figure in the business plan, generated from the model.

No chart here carries a number that was typed twice. Each one imports the model,
asks it for a result and draws that, so a changed assumption redraws the page
rather than leaving a stale picture beside a fresh sentence.

Mark specification, applied uniformly
-------------------------------------
* ultraviolet is the data colour; lime is ground and never carries type
  (it measures 1.29:1 against white, so type on lime is unreadable)
* one axis only, gridlines 0.6px and recessive, no chart junk, no 3-D, no shadows
* every value a reader needs is on the page as type — these are printed pages and
  there is no hover layer to fall back on
* a label goes inside a mark only when it fits with padding, otherwise outside
* when one item is the point, it is coloured and everything else is grey
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

from . import model as M

# ----------------------------------------------------------------- palette
LIME = "#CBF24A"
UV = "#3418E0"
INK = "#0B0E14"
INK2 = "#3A4050"
MUTED = "#6B7285"
FAINT = "#9AA0AF"
HAIR = "#E2E4EA"
WASH = "#F5F6F8"
WHITE = "#FFFFFF"

# Ultraviolet to lime, fifteen stops; the business plan uses a five-stop subset.
SPECTRUM = ["#3418E0", "#005AEE", "#0087E8", "#00ABD4", "#00C8B6",
            "#00DC91", "#6CEA6B", "#A1EE58", "#CBF24A"]


def spec(i, n):
    """Pick stop i of n along the sweep, so a set of any size spans it evenly."""
    if n <= 1:
        return SPECTRUM[0]
    return SPECTRUM[round(i * (len(SPECTRUM) - 1) / (n - 1))]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "text.color": INK,
    "axes.edgecolor": HAIR,
    "axes.labelcolor": INK2,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.facecolor": WHITE,
})

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")


def _save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{name}.png")
    fig.savefig(path, facecolor=WHITE)
    plt.close(fig)
    return path


def _money(v):
    if v >= 1e6:
        return f"${v/1e6:,.1f}m"
    if v >= 1e3:
        return f"${v/1e3:,.0f}k"
    return f"${v:,.0f}"


def _clean(ax, grid="x"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(HAIR)
    if grid:
        ax.grid(axis=grid, color=HAIR, linewidth=0.6, zorder=0)
        ax.set_axisbelow(True)


# =====================================================================
#  1 · TAM / SAM / SOM
# =====================================================================

#
# Every diagram below is drawn on a coordinate system where one data unit is one
# inch, so a chip's width can be converted to a character count and the text inside
# it can be broken to fit. Wrapping by measurement rather than by hand is the whole
# reason these diagrams survive an edit to their own content.
#
_CHAR_W = 0.565     # mean glyph width as a fraction of point size, DejaVu Sans,
                    # deliberately over-estimated so a label breaks rather than clips
_CHAR_W_BOLD = 0.625  # DejaVu Sans Bold is wider, and every chip title is bold
PAD = 0.075         # inches of padding inside a chip
LINE = 1.52         # line spacing multiple


def _canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig, ax


def _wrap(text, size, width_in, bold=False):
    """Break text to a pixel width without ever dropping a word."""
    cols = max(4, int(width_in * 72 / (size * (_CHAR_W_BOLD if bold else _CHAR_W))))
    out = []
    for para in str(text).split("\n"):
        line = ""
        for word in para.split():
            trial = f"{line} {word}".strip()
            if len(trial) <= cols or not line:
                line = trial
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def _lines_h(lines, size):
    return len(lines) * size * LINE / 72


def _ink_for(fill):
    """Pick type colour by measured luminance, never by eye.

    This is what keeps type off lime: lime measures 1.29:1 against white, so white
    type on lime is unreadable. The rule is in the brand, and here it is enforced
    rather than remembered.
    """
    h = fill.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return (INK, "#2A3040") if lum > 0.55 else (WHITE, "#E7E9F6")


def _chip(ax, x, y, w, h, title, body, fill, tsize=8.4, bsize=7.1, tag=None,
          tcol=None, bcol=None, centre=False, vcentre=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=0.05",
                                facecolor=fill, edgecolor="none", zorder=3))
    auto_t, auto_b = _ink_for(fill)
    tcol = tcol or auto_t
    bcol = bcol or auto_b
    inner = w - 2 * PAD
    tx = x + w / 2 if centre else x + PAD
    ha = "center" if centre else "left"
    if vcentre:
        # Measure the whole stack first, then start it so the block sits on the
        # chip's centre line rather than hanging from its top edge.
        block = 0.0
        if tag:
            block += 6.3 * LINE / 72
        if title:
            block += (_lines_h(_wrap(title, tsize, inner, bold=True), tsize)
                      + (0.035 if body else 0))
        if body:
            block += _lines_h(_wrap(body, bsize, inner), bsize)
        ty = y + h / 2 + block / 2
    else:
        ty = y + h - PAD
    if tag:
        ax.text(tx, ty, tag, fontsize=6.3, color=bcol, fontweight="bold",
                va="top", ha=ha, zorder=4)
        ty -= 6.3 * LINE / 72
    if title:
        tl = _wrap(title, tsize, inner, bold=True)
        ax.text(tx, ty, "\n".join(tl), fontsize=tsize, fontweight="bold",
                color=tcol, va="top", ha=ha, zorder=4, linespacing=LINE)
        ty -= _lines_h(tl, tsize) + 0.035
    if body:
        bl = _wrap(body, bsize, inner)
        ax.text(tx, ty, "\n".join(bl), fontsize=bsize, color=bcol,
                va="top", ha=ha, zorder=4, linespacing=LINE)


def _arrow(ax, x1, y1, x2, y2, col="#C3C8D6"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=8, color=col,
                                 linewidth=1.0, zorder=2))


ENGINE_COLOURS = [UV, "#0071ED", "#0096DF", "#00B8C8", "#00D3A4", "#2CE086",
                  "#A1EE58", "#D5D8E0"]
ENGINE_1LINE = ["University cohorts and licences", "Schools and technical education",
                "National initiatives and government", "NGO, donor and foundations",
                "Sponsored competitions", "Corporate and CSR programmes",
                "Programme and incubator seats", "Founder subscriptions"]


# =====================================================================
#  1 · The population we serve
# =====================================================================

def fig_segments():
    m = M.market()
    rows = sorted(m["segments"], key=lambda r: -r[1])
    fig, ax = plt.subplots(figsize=(7.1, 2.6))
    for i, (label, val) in enumerate(rows):
        ax.barh(i, val / 1e6, 0.54, color=spec(i, len(rows)), zorder=3)
        ax.text(val / 1e6 + 0.08, i, f"{val/1e6:,.2f}m", va="center",
                fontsize=8.2, color=INK, fontweight="bold")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.2, color=INK)
    ax.invert_yaxis()
    ax.set_xlim(0, max(r[1] for r in rows) / 1e6 * 1.22)
    ax.set_xlabel("People, millions")
    _clean(ax, grid="x")
    ax.text(max(r[1] for r in rows) / 1e6 * 1.2, len(rows) - 0.35,
            f"{m['people']/1e6:,.1f}m in total, Egypt and Saudi Arabia",
            ha="right", fontsize=7.8, color=INK2, fontweight="bold")
    return _save(fig, "segments")


# =====================================================================
#  2 · TAM and SAM, engine by engine
# =====================================================================

def fig_tam_som():
    """
    TAM, SAM and SOM as nested circles, the way the investor deck shows them.

    Areas are proportional to value, not radii, because a reader compares the
    area of a disc. The labels sit stacked down the middle rather than inside
    their own ring, since the inner rings are too small to hold type at this
    ratio: SOM is under one percent of TAM by area.
    """
    m = M.market()
    vals = [("TAM", m["tam"], UV, WHITE,
             "Every buyer in Egypt and KSA, at today's prices, per year"),
            ("SAM", m["sam"], "#00C8B6", INK,
             f"What the engines can reach, {m['inst_share']*100:.0f}% of it "
             f"institutional"),
            ("SOM", m["som"], "#CBF24A", INK,
             f"Year five plan revenue, {m['som_share']*100:.1f}% of SAM")]
    big = vals[0][1]
    fig, ax = plt.subplots(figsize=(7.1, 4.0))
    ax.set_aspect("equal")
    # Area proportional, so radius goes as the square root.
    radii = [(v / big) ** 0.5 for _, v, _, _, _ in vals]
    for (name, v, col, ink, _), r in zip(vals, radii):
        # Nested and bottom-aligned, which is how the deck draws them.
        ax.add_patch(plt.Circle((0, r - 1.0), r, color=col, zorder=3))
    for i, ((name, v, col, ink, _), r) in enumerate(zip(vals, radii)):
        y = (r - 1.0) + r - 0.085
        # A ring only carries its own label when it is tall enough to hold
        # two lines of type with padding. SOM is under one percent of TAM by
        # area, so it never is: it gets a leader out to the right instead.
        if 2 * r > 0.30:
            ax.text(0, y, " ".join(name), ha="center", va="top", fontsize=8.0,
                    color=ink, fontweight="bold", zorder=6)
            ax.text(0, y - 0.085, _money(v), ha="center", va="top",
                    fontsize=14.5, color=ink, fontweight="bold", zorder=6)
        else:
            cy = r - 1.0
            ax.plot([r * 0.9, 0.46], [cy, cy], color=INK, linewidth=0.8,
                    zorder=6)
            ax.text(0.50, cy + 0.035, " ".join(name), ha="left", va="bottom",
                    fontsize=7.6, color=INK, fontweight="bold", zorder=6)
            ax.text(0.50, cy - 0.02, _money(v), ha="left", va="top",
                    fontsize=12.5, color=INK, fontweight="bold", zorder=6)
    ax.set_xlim(-1.08, 2.45)
    ax.set_ylim(-1.12, 1.12)
    ax.axis("off")
    # The side notes are advanced by the number of lines each one actually
    # wrapped to, so a long note cannot run into the heading below it.
    yy = 0.86
    for name, v, col, ink, note in vals:
        lines = _wrap(note, 8.0, 1.24)
        ax.text(1.16, yy, name, fontsize=7.6, color=MUTED, fontweight="bold",
                va="top")
        ax.text(1.16, yy - 0.105, "\n".join(lines), fontsize=8.0, color=INK,
                va="top", linespacing=1.45)
        yy -= 0.105 + len(lines) * 0.098 + 0.10
    return _save(fig, "tam_som")


def fig_tam_sam():
    m = M.market()
    rows = m["rows"]
    fig, ax = plt.subplots(figsize=(7.1, 3.8))
    h = 0.36
    for i, (r, c) in enumerate(zip(rows, ENGINE_COLOURS)):
        ax.barh(i + h / 2, r["tam"] / 1e6, h, color=HAIR, zorder=3)
        ax.barh(i - h / 2, r["sam"] / 1e6, h, color=c, zorder=4)
        ax.text(r["tam"] / 1e6 + 1.0, i + h / 2, f"${r['tam']/1e6:,.1f}m",
                va="center", fontsize=7.4, color=MUTED)
        ax.text(r["sam"] / 1e6 + 1.0, i - h / 2, f"${r['sam']/1e6:,.1f}m",
                va="center", fontsize=7.6, color=INK, fontweight="bold")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(ENGINE_1LINE, fontsize=8.0, color=INK)
    ax.invert_yaxis()
    ax.set_xlabel("USD millions a year")
    ax.set_xlim(0, max(r["tam"] for r in rows) / 1e6 * 1.2)
    _clean(ax, grid="x")
    ax.legend([Rectangle((0, 0), 1, 1, color=HAIR),
               Rectangle((0, 0), 1, 1, color=UV)],
              ["TAM — the whole universe", "SAM — fits, reachable, has a budget"],
              frameon=False, fontsize=7.8, loc="lower right", labelcolor=INK2)
    return _save(fig, "tam_sam")


def fig_engine_mix():
    yrs = M.projection()
    fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.7))
    for ax, y in zip(axes, yrs):
        vals = [y["lines"][k] for k in M.ENGINE_NAMES]
        ax.pie(vals, colors=ENGINE_COLOURS, startangle=90,
               wedgeprops=dict(width=0.42, edgecolor=WHITE, linewidth=1.5))
        ax.text(0, 0.12, f"Year {y['year']}", ha="center", va="center",
                fontsize=9.5, fontweight="bold", color=INK)
        ax.text(0, -0.16, f"{y['institutional_share']*100:.0f}%", ha="center",
                va="center", fontsize=8, color=MUTED)
        ax.text(0, -1.34, "institutional", ha="center", fontsize=7.4, color=INK2)
    axes[1].legend(ENGINE_1LINE, frameon=False, fontsize=6.4, ncol=4,
                   loc="upper center", bbox_to_anchor=(0.5, -0.04),
                   labelcolor=INK2, handlelength=1.0, columnspacing=0.8)
    return _save(fig, "engine_mix")


# =====================================================================
#  3 · The roadmap — when each engine switches on
# =====================================================================

def fig_roadmap():
    """Twelve quarters. An engine's bar starts at its gate, not at day one."""
    qs = M.QUARTERS
    gates = M.ENGINE_GATES
    Q = M.QUARTERLY
    series = [
        ("University cohorts", "uni_cohorts_eg", "uni_cohorts_ksa"),
        ("Faculty licences", "uni_licences", None),
        ("School and technical cohorts", "school_cohorts", "tvet_cohorts"),
        ("Sponsored competitions", "competitions", None),
        ("NGO and donor programmes", "ngo_programmes", None),
        ("National initiative seats", "initiative_seats", None),
        ("Corporate and CSR programmes", "corporates", None),
        ("Programme and incubator seats", "programmes", None),
    ]
    W, H = 7.1, 3.95
    fig, ax = _canvas(W, H)
    left = 2.05
    cell = (W - left - 0.06) / 12
    top = H - 0.52

    # Year bands and quarter labels
    for yi, (y0, y1) in enumerate([(0, 4), (4, 8), (8, 12)]):
        x = left + y0 * cell
        ax.add_patch(Rectangle((x, top + 0.30), (y1 - y0) * cell - 0.04, 0.16,
                               color=[UV, "#0096DF", "#00D3A4"][yi], zorder=3))
        ax.text(x + ((y1 - y0) * cell) / 2, top + 0.54, f"YEAR {yi+1}",
                fontsize=6.6, color=INK2, fontweight="bold", ha="center")
    for i, (label, phase, _) in enumerate(qs):
        x = left + i * cell
        ax.text(x + cell / 2, top + 0.20, label.split()[0], fontsize=5.9,
                color=MUTED, ha="center", va="top")
        ax.text(x + cell / 2, top + 0.07, phase, fontsize=5.9, color=INK2,
                ha="center", va="top", fontweight="bold")

    rowh = (top - 0.42) / len(series)
    for r, (name, k1, k2) in enumerate(series):
        y = top - 0.24 - (r + 1) * rowh
        vals = [Q[k1][i] + (Q[k2][i] if k2 else 0) for i in range(12)]
        peak = max(vals) or 1
        ax.text(left - 0.10, y + rowh * 0.42, name, fontsize=7.1, color=INK,
                ha="right", va="center")
        first = next((i for i, v in enumerate(vals) if v > 0), None)
        for i, v in enumerate(vals):
            x = left + i * cell
            if v <= 0:
                ax.add_patch(Rectangle((x + 0.02, y + rowh * 0.30), cell - 0.05,
                                       rowh * 0.26, color="#EFF1F5", zorder=2))
                continue
            hgt = rowh * (0.22 + 0.48 * (v / peak))
            ax.add_patch(FancyBboxPatch((x + 0.02, y + rowh * 0.16), cell - 0.05, hgt,
                                        boxstyle="round,pad=0,rounding_size=0.02",
                                        facecolor=spec(r, len(series)),
                                        edgecolor="none", zorder=3))
        if first is not None:
            # The gate marker sits on the first active bar, inside its own row.
            # Placing it above the bar drifts it into the row above and reads as
            # belonging to the wrong engine.
            cy = y + rowh * 0.40
            ax.add_patch(plt.Circle((left + first * cell + cell / 2, cy),
                                    0.055, color=INK, zorder=6))
            ax.text(left + first * cell + cell / 2, cy, "G", fontsize=5.0,
                    color=WHITE, ha="center", va="center", fontweight="bold",
                    zorder=7)
    ax.text(left, 0.11, "G  marks the gate — the quarter an engine can first earn, "
            "once its prerequisite is met.  Bar height is volume;  a grey cell "
            "means the engine is not yet open.",
            fontsize=6.5, color=MUTED, va="center")
    return _save(fig, "roadmap")


def fig_gates():
    """What has to be true before each engine can sell anything."""
    gates = M.ENGINE_GATES[:8]
    W, H = 7.1, 4.3
    fig, ax = _canvas(W, H)
    rowh = (H - 0.18) / len(gates)
    for i, (name, qi, prereq, why) in enumerate(gates):
        y = H - 0.08 - (i + 1) * rowh
        ax.add_patch(FancyBboxPatch((0, y + 0.04), W, rowh - 0.08,
                                    boxstyle="round,pad=0,rounding_size=0.04",
                                    facecolor=WASH if i % 2 else "#FFFFFF",
                                    edgecolor="none", zorder=2))
        ax.add_patch(Rectangle((0, y + 0.04), 0.07, rowh - 0.08,
                               color=spec(i, len(gates)), zorder=3))
        ax.text(0.17, y + rowh - 0.18, name, fontsize=8.0, fontweight="bold",
                color=INK, va="top", zorder=4)
        q = M.QUARTERS[qi]
        ax.text(0.17, y + rowh - 0.36, f"Opens {q[0]} · {q[1]} quarter",
                fontsize=6.5, color=UV, va="top", zorder=4, fontweight="bold")
        ax.text(2.35, y + rowh - 0.18,
                "\n".join(_wrap("GATE  " + prereq, 6.8, 4.55)),
                fontsize=6.8, color=INK, va="top", zorder=4, linespacing=1.45)
        gl = len(_wrap("GATE  " + prereq, 6.8, 4.55))
        ax.text(2.35, y + rowh - 0.20 - gl * 6.8 * 1.45 / 72,
                "\n".join(_wrap(why, 6.5, 4.55)),
                fontsize=6.5, color=MUTED, va="top", zorder=4, linespacing=1.45)
    return _save(fig, "gates")


def fig_quarterly_volumes():
    """What the company is physically delivering, quarter by quarter."""
    Q = M.QUARTERLY
    fig, ax = plt.subplots(figsize=(7.1, 3.0))
    x = range(12)
    uni = [Q["uni_cohorts_eg"][i] + Q["uni_cohorts_ksa"][i] + Q["uni_pilots"][i]
           for i in x]
    sch = [Q["school_cohorts"][i] for i in x]
    tv = [Q["tvet_cohorts"][i] for i in x]
    comp = [Q["competitions"][i] for i in x]
    ngo = [Q["ngo_programmes"][i] for i in x]
    series = [("University cohorts", uni, UV), ("School cohorts", sch, "#0096DF"),
              ("Technical cohorts", tv, "#00C8B6"),
              ("Competitions", comp, "#6CEA6B"), ("NGO programmes", ngo, LIME)]
    bottoms = [0] * 12
    for name, vals, c in series:
        ax.bar(x, vals, 0.62, bottom=bottoms, color=c, label=name,
               edgecolor=WHITE, linewidth=0.8, zorder=3)
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    for i in x:
        if bottoms[i]:
            ax.text(i, bottoms[i] + 2.5, f"{bottoms[i]:.0f}", ha="center",
                    fontsize=6.8, color=INK, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels([q[0].replace(" ", "\n") for q in M.QUARTERS], fontsize=6.4,
                       color=INK2)
    ax.set_ylabel("Delivery events in the quarter")
    ax.set_ylim(0, max(bottoms) * 1.16)
    _clean(ax, grid="y")
    for b in (3.5, 7.5):
        ax.axvline(b, color=HAIR, linewidth=0.9, zorder=1)
    ax.legend(frameon=False, fontsize=7.2, loc="upper left", labelcolor=INK2)
    return _save(fig, "quarterly_volumes")


# =====================================================================
#  4 · Marketing — the customer journey
# =====================================================================

def fig_customer_journey():
    """Two journeys, because there are two customers and only one of them pays."""
    W, H = 7.1, 3.25
    fig, ax = _canvas(W, H)
    inst = [("AWARE", "Hears of us", "A founder story, a competition on a "
             "neighbouring campus, a ministry naming us"),
            ("INTERESTED", "Takes the meeting", "A cohort report from an "
             "institution like theirs"),
            ("EVALUATING", "Runs a pilot", "A free cohort, their students, "
             "their room"),
            ("COMMITTED", "Signs", "One contract: bootcamp, workshops, seats"),
            ("ADVOCATE", "Renews and refers", "Their own report, and a named "
             "peer who asks about it")]
    youth = [("AWARE", "Sees it", "A reel, an ambassador, a workshop, a "
              "competition poster"),
             ("JOINS", "Free account", "One tap, no payment"),
             ("ACTIVATES", "Finishes Mission 01", "Live, in a room, with a "
              "facilitator"),
             ("PROGRESSES", "Missions 02–10", "Inside a paid cohort or a "
              "sponsored seat"),
             ("PAYS", "Pro or Team", "To finish 11–15 after the programme ends")]
    gap = 0.09
    w = (W - 1.15 - 4 * gap) / 5
    for ri, (title, rows, col) in enumerate(
            [("THE BUYER", inst, UV), ("THE YOUNG PERSON", youth, "#00B8C8")]):
        ytop = H - 0.18 - ri * 1.62
        ax.text(0, ytop - 0.14, title, fontsize=7.0, color=col, fontweight="bold",
                va="top")
        for i, (stage, act, trigger) in enumerate(rows):
            x = 1.15 + i * (w + gap)
            _chip(ax, x, ytop - 1.44, w, 1.26, act, trigger,
                  spec(i, 5) if ri == 0 else WASH, tag=stage, tsize=8.0, bsize=6.3)
            if i < 4:
                _arrow(ax, x + w + 0.01, ytop - 0.80, x + w + gap - 0.01, ytop - 0.80)
    ax.text(0, 0.22, "The two journeys meet in the room: the buyer's pilot is the "
            "young person's activation.", fontsize=6.9, color=MUTED, va="center")
    return _save(fig, "customer_journey")


def fig_channel_mix():
    """Where institutional pipeline comes from, and what each channel is for."""
    rows = [("Ambassador intelligence", 26, "Which campus has budget this term"),
            ("Founder stories and podcast", 21, "Makes a dean take the meeting"),
            ("Competitions on campus", 18, "Enters through the door with no budget"),
            ("Ecosystem events and conferences", 15, "Where partnerships start"),
            ("Referral from an existing partner", 12, "The cheapest meeting we get"),
            ("Direct outreach", 8, "Works only once the others have warmed it")]
    fig, ax = plt.subplots(figsize=(7.1, 2.6))
    for i, (label, val, why) in enumerate(rows):
        ax.barh(i, val, 0.5, color=spec(i, len(rows)), zorder=3)
        ax.text(val + 0.7, i + 0.07, f"{val}%", va="center", fontsize=8,
                color=INK, fontweight="bold")
        ax.text(val + 3.4, i + 0.07, why, va="center", fontsize=6.9, color=MUTED)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=8, color=INK)
    ax.invert_yaxis()
    ax.set_xlim(0, 52)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.text(0, -0.95, "Share of year-one institutional pipeline by origin",
            fontsize=6.9, color=MUTED)
    return _save(fig, "channel_mix")


# =====================================================================
#  5 · Strategic analysis
# =====================================================================

def fig_swot():
    quad = [
        ("STRENGTHS", UV, [
            "A sequenced method with a review gate, not a content library",
            "Bilingual and MENA-composed, not translated",
            "The institutional workspace and cohort report — a reporting line",
            "Eight engines, so no single buyer type is existential"]),
        ("WEAKNESSES", "#0096DF", [
            "Delivery depends on certified facilitators who do not exist yet",
            "No signed national programme to point to on day one",
            "Founder-dependent: the CEO personally opens every cohort",
            "Unproven at school age, where safeguarding rules differ"]),
        ("OPPORTUNITIES", "#00D3A4", [
            "Public million-scale targets with no delivery capacity behind them",
            "Egypt's technical education reform needs employability content",
            "Competitions are run everywhere and run badly",
            "Capital concentrating in the Gulf while founders concentrate in Egypt"]),
        ("THREATS", LIME, [
            "A university builds its own programme in-house",
            "Consultancies and event agencies cut price on the cohort",
            "A government programme contracts a single incumbent",
            "Currency and budget shocks hitting CSR and donor spend first"]),
    ]
    W, H = 7.1, 3.9
    fig, ax = _canvas(W, H)
    gap = 0.12
    w = (W - gap) / 2
    h = (H - gap) / 2
    for i, (title, col, items) in enumerate(quad):
        x = (i % 2) * (w + gap)
        y = H - h if i < 2 else 0
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=WASH, edgecolor="none", zorder=2))
        ax.add_patch(Rectangle((x, y + h - 0.12), w, 0.12, color=col, zorder=3))
        ax.text(x + PAD, y + h - 0.26, title, fontsize=8.2, fontweight="bold",
                color=INK, va="top", zorder=4)
        yy = y + h - 0.52
        for it in items:
            lines = _wrap(it, 6.9, w - 2 * PAD - 0.14)
            ax.text(x + PAD, yy, "▪", fontsize=6.0, color=col, va="top", zorder=4)
            ax.text(x + PAD + 0.14, yy, "\n".join(lines), fontsize=6.9,
                    color=INK2, va="top", zorder=4, linespacing=1.45)
            yy -= _lines_h(lines, 6.9) + 0.07
    return _save(fig, "swot")


def fig_porter():
    forces = [
        ("Rivalry among existing competitors", "MODERATE",
         "Training consultancies and in-house university programmes compete on "
         "price and relationship, not on method. No regional platform does what "
         "StartPad does.", 0.55),
        ("Threat of new entrants", "MODERATE TO HIGH",
         "The software is replicable. The certified facilitator pool, the "
         "bilingual curriculum and the institutional relationships are not — and "
         "they take years.", 0.65),
        ("Bargaining power of buyers", "HIGH",
         "Universities and ministries are slow, price-sensitive and used to being "
         "courted. Mitigated by the pilot-to-licence ladder and switching cost "
         "once a cohort record exists.", 0.78),
        ("Bargaining power of suppliers", "LOW TO MODERATE",
         "Facilitators are the supply, and they can be hired by consultancies. "
         "Certification, tiering and a career path are the defence.", 0.42),
        ("Threat of substitutes", "MODERATE",
         "Free content, generic AI tools and short courses. None of them produce "
         "a reportable cohort record, which is what the buyer is actually "
         "purchasing.", 0.50),
    ]
    W, H = 7.1, 3.5
    fig, ax = _canvas(W, H)
    rowh = (H - 0.10) / len(forces)
    for i, (name, level, body, score) in enumerate(forces):
        y = H - 0.05 - (i + 1) * rowh
        ax.add_patch(FancyBboxPatch((0, y + 0.05), W, rowh - 0.10,
                                    boxstyle="round,pad=0,rounding_size=0.04",
                                    facecolor=WASH if i % 2 else WHITE,
                                    edgecolor="none", zorder=2))
        ax.text(PAD, y + rowh - 0.20, name, fontsize=7.6, fontweight="bold",
                color=INK, va="top", zorder=4)
        ax.text(PAD, y + rowh - 0.38, level, fontsize=6.4, color=UV,
                fontweight="bold", va="top", zorder=4)
        # intensity meter
        mx, mw = 2.05, 1.05
        ax.add_patch(Rectangle((mx, y + rowh / 2 - 0.045), mw, 0.09,
                               color="#E4E7EE", zorder=3))
        ax.add_patch(Rectangle((mx, y + rowh / 2 - 0.045), mw * score, 0.09,
                               color=spec(int(score * 8), 9), zorder=4))
        ax.text(3.32, y + rowh - 0.18, "\n".join(_wrap(body, 6.8, W - 3.42)),
                fontsize=6.8, color=INK2, va="top", zorder=4, linespacing=1.45)
    return _save(fig, "porter")


def fig_pestle():
    items = [
        ("POLITICAL", "Both states have made youth entrepreneurship a stated "
         "national priority with named programmes and budgets.政 policy "
         "direction is a tailwind; political attention also means procurement "
         "scrutiny."),
        ("ECONOMIC", "EGP devaluation cuts the cost base faster than local "
         "willingness to pay. Gulf capital is deepening while Egyptian funding "
         "tightens — which is the case for serving both."),
        ("SOCIAL", "A very young population, high graduate unemployment and "
         "strong social legitimacy for entrepreneurship as a route out. Family "
         "approval still favours employment, which the Bazaar is designed to "
         "address."),
        ("TECHNOLOGICAL", "Near-universal smartphone access among the target age "
         "group; AI review makes one-to-many mentoring possible at a price the "
         "market can bear."),
        ("LEGAL", "Egypt's Law 6 of 2025 incentivises informal businesses to "
         "formalise. Student data, safeguarding and child-protection rules bind "
         "the schools engine and are a compliance cost, not an afterthought."),
        ("ENVIRONMENTAL", "Low direct footprint. Climate and green-economy themes "
         "are increasingly required in donor and CSR logframes, and the mission "
         "content accommodates them."),
    ]
    W, H = 7.1, 3.25
    fig, ax = _canvas(W, H)
    gap = 0.11
    w = (W - 2 * gap) / 3
    h = (H - gap) / 2
    for i, (title, body) in enumerate(items):
        x = (i % 3) * (w + gap)
        y = H - h if i < 3 else 0
        _chip(ax, x, y, w, h - 0.02, title, body.replace("政 ", ""),
              spec(i, 6) if i < 3 else WASH, tsize=7.6, bsize=6.6)
    return _save(fig, "pestle")


def fig_moat():
    """What is actually defensible, ordered by how long it takes to copy."""
    rows = [("The certified facilitator pool", 36,
             "Years to recruit, certify and retain in two markets"),
            ("Institutional relationships and renewals", 30,
             "Procurement cycles cannot be shortcut"),
            ("The cohort evidence record", 24,
             "Switching means abandoning the history a dean reports on"),
            ("Bilingual MENA-composed curriculum", 18,
             "Composed, not translated — and dialect-specific"),
            ("The AI review rubric, tuned on real cohorts", 14,
             "Improves with every cohort; a cold start cannot match it"),
            ("The platform itself", 6, "The least defensible layer, and the one "
                                       "most people mistake for the moat")]
    fig, ax = plt.subplots(figsize=(7.1, 2.6))
    for i, (label, months, why) in enumerate(rows):
        ax.barh(i, months, 0.5, color=spec(i, len(rows)), zorder=3)
        ax.text(months + 0.6, i + 0.06, f"{months} mo", va="center", fontsize=7.6,
                color=INK, fontweight="bold")
        ax.text(months + 4.0, i + 0.06, why, va="center", fontsize=6.8, color=MUTED)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.8, color=INK)
    ax.invert_yaxis()
    ax.set_xlim(0, 86)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.text(0, -0.95, "Estimated months for a well-funded competitor to replicate",
            fontsize=6.9, color=MUTED)
    return _save(fig, "moat")


# =====================================================================
#  6 · Engine 2 — the schools ladder
# =====================================================================

def fig_school_ladder():
    su = M.school_unit_economics()
    tu = M.tvet_unit_economics()
    steps = [
        ("FORMAT 01", "School club", "A term-long after-school programme on the "
         "missions, run by a trained teacher.", "Platform seats"),
        ("FORMAT 02", "School cohort",
         f"{su['days']} in-person days for {su['size']} students, ending in a "
         f"public showcase.", _money(su["price"])),
        ("FORMAT 03", "Technical institute",
         f"{tu['days']} days with an employability frame — a trade turned into a "
         f"business.", _money(tu["price"])),
        ("FORMAT 04", "Whole-school licence",
         "Every student for an academic year, with teacher certification.",
         _money(M.PRICE_SCHOOL_LICENCE)),
    ]
    W, H = 7.1, 2.35
    fig, ax = _canvas(W, H)
    gap = 0.13
    w = (W - 3 * gap) / 4
    for i, (tag, title, body, price) in enumerate(steps):
        x = i * (w + gap)
        _chip(ax, x, 0.66, w, 1.52, title, body, spec(i, 4), tag=tag, tsize=9.4,
              bsize=6.9)
        _chip(ax, x, 0.06, w, 0.50, price, None, WASH, tsize=10.5, centre=True,
              vcentre=True, tcol=UV)
        if i < 3:
            _arrow(ax, x + w + 0.012, 1.42, x + w + gap - 0.012, 1.42)
    return _save(fig, "school_ladder")


def fig_engine_economics():
    rows = M.engine_economics()
    rows = sorted(rows, key=lambda r: -r["ltv"])
    fig, ax = plt.subplots(figsize=(7.1, 3.3))
    y = range(len(rows))
    for i, r in enumerate(rows):
        c = UV if r["name"] != "Founder subscriptions" else "#C9CEDB"
        ax.barh(i, r["ltv"], 0.5, color=c, zorder=3)
        ax.barh(i, -r["cac"], 0.5, color="#D98682", zorder=3)
        ax.text(r["ltv"] + 1_800, i, _money(r["ltv"]), va="center",
                fontsize=7.8, color=INK, fontweight="bold")
        ax.text(-r["cac"] - 1_800, i, _money(r["cac"]), va="center", ha="right",
                fontsize=7.4, color="#8A3330")
    ax.axvline(0, color=INK, linewidth=1.0, zorder=5)
    ax.set_yticks(list(y))
    ax.set_yticklabels([r["name"] for r in rows], fontsize=8.2, color=INK)
    ax.invert_yaxis()
    lo = -max(r["cac"] for r in rows) * 2.6
    hi = max(r["ltv"] for r in rows) * 1.25
    ax.set_xlim(lo, hi)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.text(lo * 0.5, -0.78, "COST TO WIN", fontsize=6.8, color="#8A3330",
            fontweight="bold", ha="center")
    ax.text(hi * 0.35, -0.78, "LIFETIME GROSS PROFIT", fontsize=6.8, color=UV,
            fontweight="bold", ha="center")
    ax.set_ylim(len(rows) - 0.4, -1.15)
    return _save(fig, "engine_economics")


def fig_deal_sizes():
    """Deal size against how many of them there are — why the mix is the mix."""
    rows = M.engine_economics()
    fig, ax = plt.subplots(figsize=(7.1, 2.4))
    names = [r["name"] for r in rows]
    vals = [r["value"] for r in rows]
    order = sorted(range(len(rows)), key=lambda i: -vals[i])
    for pos, i in enumerate(order):
        c = ENGINE_COLOURS[min(pos, 5)]
        ax.barh(pos, vals[i], 0.52, color=UV if names[i] != "Founder subscriptions"
                else "#C9CEDB", zorder=3)
        ax.text(vals[i] + 2_200, pos, f"{_money(vals[i])} a year", va="center",
                fontsize=7.8, color=INK, fontweight="bold")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([names[i] for i in order], fontsize=8.2, color=INK)
    ax.invert_yaxis()
    ax.set_xlim(0, max(vals) * 1.32)
    ax.set_xlabel("Annual value of one customer, USD")
    _clean(ax, grid="x")
    ax.xaxis.set_major_formatter(lambda v, p: f"${v/1000:,.0f}k" if v else "0")
    return _save(fig, "deal_sizes")


# =====================================================================
#  4 · The institutional pipeline — the funnel the company actually runs
# =====================================================================

def fig_pipeline():
    stages = M.pipeline()
    fig, ax = _canvas(7.1, 2.4)
    top = stages[0][1]
    for i, (label, val) in enumerate(stages):
        w = (val / top) * 3.0
        y = (len(stages) - i - 1) * 0.56 + 0.20
        ax.add_patch(FancyBboxPatch((3.45, y), w, 0.44,
                                    boxstyle="round,pad=0,rounding_size=0.04",
                                    facecolor=spec(i, len(stages)), edgecolor="none",
                                    zorder=3))
        ax.text(3.37, y + 0.22, label, ha="right", va="center", fontsize=8.2,
                color=INK)
        txt = f"{val:,}"
        if i:
            txt += f"   ({val/stages[i-1][1]*100:,.0f}%)"
        ax.text(3.45 + w + 0.1, y + 0.22, txt, ha="left", va="center",
                fontsize=8.2, fontweight="bold", color=INK)
    ax.text(3.45, 0.04, "Year one. Every stage is a number a named person owns.",
            fontsize=7.0, color=MUTED, va="center")
    return _save(fig, "pipeline")


# =====================================================================
#  5 · Engine 1 — the university ladder
# =====================================================================

def fig_university_ladder():
    """How one campus relationship grows from a free pilot to a faculty licence."""
    ue = M.cohort_unit_economics()
    steps = [
        ("STEP 01", "Free pilot", "One cohort, no fee. The cohort report it "
         "produces is the sales document for everything after it.", "$0"),
        ("STEP 02", "First paid cohort", "25 students, six bootcamp days, seats, "
         "judging and the report.", _money(ue["price"])),
        ("STEP 03", "Parallel groups", "100-plus students run as four cohorts in "
         "the same term.", _money(ue["price"] * 4)),
        ("STEP 04", "Faculty licence", "Every student in the faculty, for an "
         "academic year.", _money(M.PRICE_FACULTY_LICENCE)),
    ]
    W, H = 7.1, 2.35
    fig, ax = _canvas(W, H)
    gap = 0.13
    w = (W - 3 * gap) / 4
    for i, (tag, title, body, price) in enumerate(steps):
        x = i * (w + gap)
        _chip(ax, x, 0.66, w, 1.52, title, body, spec(i, len(steps)), tag=tag,
              tsize=9.6, bsize=6.9)
        _chip(ax, x, 0.06, w, 0.50, price, None, WASH, tsize=11.5, centre=True,
              vcentre=True, tcol=UV)
        if i < 3:
            _arrow(ax, x + w + 0.012, 1.42, x + w + gap - 0.012, 1.42)
    return _save(fig, "university_ladder")

def fig_initiative_scale():
    """National targets, what is addressable, and what we plan to take."""
    seats = {y: M.plan("initiative_seats", y) for y in (1, 2, 3)}
    bars = [
        ("Stated national targets\n(Egypt programmes alone)", 3_000_000, HAIR),
        ("Addressable seats a year\nacross both markets", M.INITIATIVE_SEATS_PER_YEAR,
         "#A8C8F0"),
        (f"What one provider could serve\n({M.FILTER_INITIATIVE_SHARE*100:.0f}%)",
         M.INITIATIVE_SEATS_PER_YEAR * M.FILTER_INITIATIVE_SHARE, "#0071ED"),
        ("StartPad, year three", seats[3], UV),
        ("StartPad, year one", seats[1], LIME),
    ]
    fig, ax = plt.subplots(figsize=(7.1, 2.6))
    for i, (label, val, c) in enumerate(bars):
        ax.barh(i, val, 0.54, color=c, zorder=3)
        ax.text(val + 48_000, i, f"{val:,.0f} seats", va="center", fontsize=7.8,
                color=INK, fontweight="bold")
    ax.set_yticks(range(len(bars)))
    ax.set_yticklabels([b[0] for b in bars], fontsize=7.6, color=INK)
    ax.invert_yaxis()
    ax.set_xlim(0, bars[0][1] * 1.2)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    return _save(fig, "initiative_scale")


def fig_initiative_model():
    """How a sponsored-seat programme is actually delivered."""
    steps = [
        ("01", "Co-design", "The initiative's objective, our missions, and the "
         "reporting format their own donor expects."),
        ("02", "Certify their trainers", "Train-the-trainer cohorts put delivery "
         "in the programme's hands — the only way to reach tens of thousands."),
        ("03", "Provision in bulk", "Seats issued by governorate or region, with "
         "no facilitator needed for the platform itself."),
        ("04", "Report to the donor", "Participation, progress and evidence per "
         "participant, exported in their format."),
    ]
    W, H = 7.1, 1.98
    fig, ax = _canvas(W, H)
    gap = 0.12
    w = (W - 3 * gap) / 4
    for i, (tag, title, body) in enumerate(steps):
        x = i * (w + gap)
        _chip(ax, x, 0.10, w, 1.76, title, body, spec(i, len(steps)), tag=tag,
              tsize=9.2, bsize=6.8)
        if i < 3:
            _arrow(ax, x + w + 0.012, 0.98, x + w + gap - 0.012, 0.98)
    return _save(fig, "initiative_model")


# =====================================================================
#  7 · Engine 3 — competitions, as a revenue line
# =====================================================================

def fig_competition_model():
    """Who pays, what they buy, and what it leaves behind."""
    W, H = 7.1, 2.65
    fig, ax = _canvas(W, H)
    _chip(ax, 0, 1.62, 2.05, 0.92, "The sponsor pays",
          "A bank, a telco, a ministry, a university or a foundation with a youth "
          "budget and a brand to put on it.", UV, tsize=9.4, bsize=6.8)
    _chip(ax, 2.52, 1.62, 2.05, 0.92, "StartPad runs it",
          "Entry is a free account. Qualifying rounds are the Discovery missions, "
          "scored by the platform.", "#0087E8", tsize=9.4, bsize=6.8)
    _chip(ax, 5.05, 1.62, 2.05, 0.92, "Judges see real work",
          "Reviewed artefacts and evidence, not slides. Finalists arrive "
          "prepared.", "#00C8B6", tsize=9.4, bsize=6.8)
    for x in (2.14, 4.66):
        _arrow(ax, x, 2.08, x + 0.3, 2.08)

    outcomes = [("Revenue", _money(M.PRICE_COMPETITION[1]), "per competition"),
                ("Entrants reached", "700", "typical, each with an account"),
                ("Gross margin",
                 f"{(1 - M.COMPETITION_DIRECT/M.PRICE_COMPETITION[1])*100:.0f}%",
                 "after judging and event cost"),
                ("Leaves behind", "Two relationships",
                 "a university and a sponsor, for the next deal")]
    gap = 0.13
    w = (W - 3 * gap) / 4
    for i, (label, value, sub) in enumerate(outcomes):
        x = i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, 0.10), w, 1.26,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=WASH, edgecolor="none", zorder=2))
        ax.text(x + PAD, 1.22, label.upper(), fontsize=6.3, color=MUTED,
                fontweight="bold", va="top", zorder=4)
        ax.text(x + PAD, 0.98, value, fontsize=14, color=UV, fontweight="bold",
                va="top", zorder=4)
        ax.text(x + PAD, 0.58, "\n".join(_wrap(sub, 6.7, w - 2 * PAD)),
                fontsize=6.7, color=INK2, va="top", zorder=4, linespacing=1.45)
    return _save(fig, "competition_model")


# =====================================================================
#  8 · Revenue, cost and the path to breakeven
# =====================================================================

# =====================================================================
#  9 · Subscriptions, as a consequence of the engines
# =====================================================================

def fig_subscription_sources():
    """
    Where paying founders come from, and at what rate.

    Two routes, drawn at the same scale: a learner who sat in a cohort, and a
    stranger who arrived from a click. The first converts several times better
    than the second, which is the whole reason the direct engine is a
    consequence of the institutional business rather than a channel beside it.
    """
    FL = M.FL
    b = FL.book()
    y = 1
    inst = b.year("Acquisitions", "Registered accounts from institutions", y)
    online = b.year("Acquisitions", "Registered accounts from online leads", y)
    offline = b.year("Acquisitions",
                     "Registered accounts from offline sign ups", y)
    r_inst = b.assumption("Stage 3, registered to paid, reached through an "
                          "institution", 3)
    r_online = b.assumption("Stage 3, registered to paid, reached online", 3)
    rows = [
        ("Reached through an institution", inst, r_inst, UV),
        ("Reached by StartPad's own channels", online + offline, r_online,
         "#C9CEDB"),
    ]
    paid_total = sum(v * r for _, v, r, _ in rows)
    fig, ax = plt.subplots(figsize=(7.1, 2.5))
    top = max(v for _, v, _, _ in rows)
    for i, (name, reached, rate, col) in enumerate(rows):
        ax.barh(i, reached, 0.46, color=col, zorder=3)
        paid = reached * rate
        ax.text(reached + top * 0.02, i + 0.10,
                f"{paid:,.0f} paying accounts", va="center", fontsize=8.0,
                color=INK, fontweight="bold")
        ax.text(reached + top * 0.02, i - 0.18,
                f"from {reached:,.0f} registered, at {rate*100:.1f}%",
                va="center", fontsize=6.9, color=MUTED)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.0, color=INK)
    ax.invert_yaxis()
    ax.set_xlim(0, top * 1.62)
    ax.set_xlabel("Registered accounts, year one")
    _clean(ax, grid="x")
    share = (rows[0][1] * rows[0][2] / paid_total) if paid_total else 0.0
    ax.set_title(f"{share*100:.0f}% of paying accounts arrive through an "
                 f"organisation, not a click",
                 fontsize=7.8, color=INK2, loc="left", pad=8)
    return _save(fig, "subscription_sources")


def fig_cohort_ramp():
    """
    Delivery load against certified capacity, five years.

    Two questions on one page. The bars answer the easy one, how many cohorts
    are delivered. The lines answer the honest one: whether the certified pool
    can actually staff them. The plan is only credible where the dashed line
    stays above the solid one, and it does, in every year, because the pool is
    sized from the load rather than assumed.
    """
    cap = M.facilitator_capacity()
    fig, ax = plt.subplots(figsize=(7.1, 3.3))
    x = list(range(len(cap)))
    cohorts = [c["total"] for c in cap]
    ax.bar(x, cohorts, 0.5, color=UV, label="Cohorts delivered", zorder=3)
    for i, v in enumerate(cohorts):
        # Inside the bar, because the right hand scale puts its own labels in
        # the space just above the bar top and the two used to collide.
        if v > max(cohorts) * 0.14:
            ax.text(i, v * 0.5, f"{v:,.0f}", ha="center", va="center",
                    fontsize=9.0, fontweight="bold", color=WHITE, zorder=6)
        else:
            ax.text(i, v + max(cohorts) * 0.02, f"{v:,.0f}", ha="center",
                    va="bottom", fontsize=9.0, fontweight="bold", color=INK,
                    zorder=6)
    ax2 = ax.twinx()
    need = [c["days"] for c in cap]
    have = [c["available"] for c in cap]
    ax2.plot(x, need, color=INK, linewidth=1.8, marker="o", markersize=4.0,
             zorder=6, label="Facilitator days the plan needs")
    ax2.plot(x, have, color="#C2185B", linewidth=1.6, linestyle=(0, (4, 2)),
             marker="s", markersize=3.6, zorder=5,
             label="Days the certified pool gives")
    for i, c in enumerate(cap):
        ax2.text(i, have[i] + max(have) * 0.045,
                 f"{c['utilisation']*100:.0f}% used", ha="center",
                 fontsize=6.8, color="#C2185B", zorder=7)
    ax2.set_ylim(0, max(have) * 1.30)
    ax2.set_ylabel("Facilitator days in the year", color=INK2, fontsize=8.2)
    ax2.spines["top"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.spines["right"].set_color(HAIR)
    ax2.tick_params(labelsize=7.4)
    ax.set_xticks(x)
    ax.set_xticklabels([c["label"] for c in cap], fontsize=8.4, color=INK)
    ax.set_ylabel("Cohorts in the year")
    ax.set_ylim(0, max(cohorts) * 1.30)
    _clean(ax, grid="y")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=7.2,
              loc="upper center", bbox_to_anchor=(0.5, -0.10), ncol=3,
              labelcolor=INK2, columnspacing=1.4, handlelength=1.5)
    return _save(fig, "cohort_ramp")


def fig_headcount():
    """
    The establishment across five years, against its own cap.

    The cap is the point of this chart, so it is drawn: a step line at six, nine,
    twelve, sixteen and twenty. Bars that touch it and never cross it are the
    whole argument that this plan can be staffed.
    """
    by_fn, totals = M.headcount()
    fns = totals["order"]
    years = list(M.YEARS_5)
    fig, ax = plt.subplots(figsize=(7.1, 3.35))
    x = list(range(len(years)))
    bottoms = [0] * len(years)
    cols = [UV, "#0071ED", "#00ABD4", "#00D3A4", "#A1EE58"]
    for fn, c in zip(fns, cols):
        vals = [by_fn[fn][f"y{y}"] for y in years]
        ax.bar(x, vals, 0.52, bottom=bottoms, color=c, label=fn,
               edgecolor=WHITE, linewidth=1.1, zorder=3)
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    caps = [M.HEADCOUNT_CAP[y] for y in years]
    ax.step([i - 0.5 for i in x] + [x[-1] + 0.5], caps + [caps[-1]],
            where="post", color="#C2185B", linewidth=1.5,
            linestyle=(0, (4, 2)), zorder=6, label="The cap this plan commits to")
    for i, y in enumerate(years):
        ax.text(i, totals[f"y{y}"] + 0.7, f"{totals[f'y{y}']}", ha="center",
                fontsize=10.5, fontweight="bold", color=INK, zorder=7)
    ax.set_xticks(x)
    ax.set_xticklabels([f"Year {y}" for y in years], fontsize=9, color=INK)
    ax.set_ylabel("Employees at year end")
    ax.set_ylim(0, max(caps) * 1.30)
    _clean(ax, grid="y")
    ax.legend(frameon=False, fontsize=7.4, loc="upper left", labelcolor=INK2)
    return _save(fig, "headcount")


# =====================================================================
#  9 · Where a cohort's $7,500 goes
def fig_gtm_moves():
    """The five moves, and what each one unlocks."""
    moves = [
        ("MOVE 01", "Universities", "Entrepreneurship centres, capstones, deans",
         "Delivered cohorts, and the reports every other engine is sold on"),
        ("MOVE 02", "Competitions", "Enactus, INJAZ, bank-sponsored seasons",
         "Hundreds of entrants per deal, paid for by a sponsor"),
        ("MOVE 03", "Mission Zero", "The podcast, the readiness report, ambassadors",
         "Institutions that call first, and curriculum as a by-product"),
        ("MOVE 04", "Certified partners", "Youth NGOs, training providers, chapters",
         "Delivery capacity that is not payroll"),
        ("MOVE 05", "Public programmes", "Initiatives, ministries, donors",
         "Seats and trainer certification at national scale"),
    ]
    W, H = 7.1, 2.24
    fig, ax = _canvas(W, H)
    gap = 0.11
    w = (W - 4 * gap) / 5
    for i, (tag, title, body, unlock) in enumerate(moves):
        x = i * (w + gap)
        _chip(ax, x, 1.06, w, 1.14, title, body, spec(i, 5), tag=tag,
              tsize=9.2, vcentre=True)
        _chip(ax, x, 0.03, w, 0.92, None, unlock, WASH, tag="UNLOCKS", bsize=6.8,
              vcentre=True)
        if i < 4:
            _arrow(ax, x + w + 0.01, 1.63, x + w + gap - 0.01, 1.63)
    return _save(fig, "gtm_moves")


def fig_institution_workflow():
    """Map to Report: the six steps that turn a meeting into a cohort report."""
    steps = [
        ("01", "Map", "The right person at each of the four doors", "Week −4"),
        ("02", "Meet", "Agree the objective and the cohort size", "Week −3"),
        ("03", "Sign", "One contract: bootcamp, workshops, seats", "Week −2"),
        ("04", "Set up", "Admin account, cohort, students invited", "Week −1"),
        ("05", "Run", "6 bootcamp days, missions every evening", "Weeks 1–2"),
        ("06", "Report", "Bazaar, certificates, cohort report, renew", "Week 3"),
    ]
    W, H = 7.1, 1.92
    fig, ax = _canvas(W, H)
    gap = 0.10
    w = (W - 5 * gap) / 6
    for i, (tag, title, body, when) in enumerate(steps):
        x = i * (w + gap)
        _chip(ax, x, 0.34, w, 1.34, title, body, SPECTRUM[i], tag=tag, tsize=9.2,
              bsize=6.7, vcentre=True)
        ax.text(x + w / 2, 0.14, when, fontsize=6.8, color=MUTED, ha="center")
        if i < 5:
            _arrow(ax, x + w + 0.01, 1.00, x + w + gap - 0.01, 1.00)
    return _save(fig, "institution_workflow")


def fig_bootcamp_map():
    """Learn it in the room, build it on StartPad that evening."""
    days = [
        ("DAY 01", "Idea generation", "01–03", "Accounts live"),
        ("DAY 02", "Market research", "04–06", "01–03 in"),
        ("DAY 03", "Business finance", "07–08", "04–06 in"),
        ("DAY 04", "Prototype and brand", "09–10", "07–08 in"),
        ("DAY 05", "Pitch skills", "Catch up 01–10", "09–10 in"),
        ("DAY 06", "Projects Bazaar", "Judges' pack", "Cohort report"),
        ("BEYOND", "Keep building", "11–15", "Progress"),
    ]
    W, H = 7.1, 2.30
    fig, ax = _canvas(W, H)
    left = 0.62
    gap = 0.08
    w = (W - left - 6 * gap) / 7
    bands = [("In the room", 1.28, 0.68), ("On StartPad", 0.60, 0.56),
             ("Admin view", 0.06, 0.44)]
    for label, y, h in bands:
        ax.text(left - 0.10, y + h / 2, label, fontsize=6.9, color=MUTED,
                fontweight="bold", ha="right", va="center")
    for i, (tag, inclass, missions, admin) in enumerate(days):
        x = left + i * (w + gap)
        last = i == len(days) - 1
        ax.text(x + w / 2, 2.22, tag, fontsize=6.6, ha="center", va="top",
                fontweight="bold", color=UV if last else MUTED)
        _chip(ax, x, 1.28, w, 0.68, inclass, None, WASH if last else SPECTRUM[i],
              tsize=7.6, centre=True, vcentre=True)
        _chip(ax, x, 0.60, w, 0.56, missions, None, "#EEF3FB", tsize=7.5,
              tcol=UV, centre=True, vcentre=True)
        _chip(ax, x, 0.06, w, 0.44, None, admin, WASH, bsize=6.4, centre=True,
              vcentre=True)
        if not last:
            for yy in (1.62, 0.88, 0.28):
                _arrow(ax, x + w + 0.006, yy, x + w + gap - 0.006, yy)
    return _save(fig, "bootcamp_map")


def fig_org_chart():
    """
    The year-one establishment: six people, and what is deliberately not there.

    The grey notes matter more than the boxes. A chart showing only the six would
    hide that operations, finance, design and the school engine are each carried
    by somebody whose title says something else — which is the honest cost of a
    six-person year one.
    """
    by_fn, totals = M.headcount()
    W, H = 7.1, 3.34
    fig, ax = _canvas(W, H)
    _chip(ax, 2.00, 2.64, 3.10, 0.62, "Chief Executive Officer",
          "Institutional relationships · hosts Mission Zero · carries operations, "
          "finance and the quality gates until year four",
          UV, tsize=9.2, bsize=6.3, centre=True, vcentre=True)

    units = [
        ("Chief Technology Officer", ["Senior full-stack engineer"],
         "Design, data and product management sit with the CTO until years "
         "four and five"),
        ("Head of Curriculum and Certification", [],
         "Certifies and audits the facilitator pool rather than employing it"),
        ("Head of Partnerships — Egypt", [],
         "Also carries competitions, schools and corporate sponsors through "
         "year one"),
        ("Head of Growth and Content", [],
         "Mission Zero, the ambassador network and the annual readiness report"),
    ]
    gap = 0.12
    w = (W - 3 * gap) / 4
    note_top = 1.26
    for i, (title, reports, note) in enumerate(units):
        x = i * (w + gap)
        _chip(ax, x, 1.90, w, 0.58, title, None, "#DDE3F6", tsize=7.4,
              vcentre=True)
        _arrow(ax, W / 2, 2.62, x + w / 2, 2.52)
        for j, r in enumerate(reports):
            _arrow(ax, x + w / 2, 1.88, x + w / 2, 1.80)
            _chip(ax, x, 1.38, w, 0.40, None, r, WASH, bsize=6.9, vcentre=True)
        ax.text(x + PAD, note_top, "\n".join(_wrap(note, 6.3, w - 2 * PAD)),
                fontsize=6.3, color=MUTED, va="top", zorder=4, linespacing=1.46)

    ax.add_patch(Rectangle((0, 0.60), W, 0.012, color=HAIR, zorder=2))
    ax.text(0, 0.66, "NOT ON THE PAYROLL — and this is the design, not a gap",
            fontsize=6.3, color=UV, fontweight="bold", va="bottom", zorder=4)
    off = [("Certified facilitator pool",
            f"{M.QUARTERLY['certified_facilitators'][3]} certified by the end of "
            f"year one. Every cohort runs on this pool."),
           ("Certified delivery partners",
            f"{M.stock('delivery_partners', 1)} organisations in year one. They "
            f"deliver; StartPad audits."),
           ("Campus ambassadors",
            f"{M.AMBASSADORS[1]} on a small stipend. Demand generation, never "
            f"delivery.")]
    cw = (W - 2 * 0.12) / 3
    for i, (t, b) in enumerate(off):
        _chip(ax, i * (cw + 0.12), 0.04, cw, 0.52, t, b, LIME, tsize=7.2,
              bsize=6.2)
    return _save(fig, "org_chart")


def fig_phases():
    """Year one, four phases, two markets."""
    phases = [
        ("Q4 2026", "Land", "Get in the door in both markets",
         "First university pilots, ambassadors recruited",
         "First programme partners, Riyadh team hired"),
        ("Q1 2027", "Prove", "Show the first results",
         "Cohort reports, first competition",
         "First cohorts, first campus pilots"),
        ("Q2 2027", "Expand", "Turn results into deals",
         "Programmes, NGOs, more campuses",
         "More universities, youth initiatives"),
        ("Q3 2027", "Scale", "Renew and plan year two",
         "Licence renewals, podcast season two",
         "First Riyadh competition, renewals"),
    ]
    W, H = 7.1, 3.05
    fig, ax = _canvas(W, H)
    gap = 0.13
    w = (W - 3 * gap) / 4
    for i, (q, name, aim, eg, ksa) in enumerate(phases):
        x = i * (w + gap)
        ax.text(x + PAD, 2.96, q, fontsize=6.9, color=MUTED, fontweight="bold",
                va="top")
        _chip(ax, x, 2.04, w, 0.76, name, aim, SPECTRUM[i * 2], tsize=10.4,
              bsize=6.9, vcentre=True)
        _chip(ax, x, 1.06, w, 0.84, "Egypt", eg, WASH, tsize=7.4, bsize=6.8,
              vcentre=True)
        _chip(ax, x, 0.08, w, 0.84, "Saudi Arabia", ksa, WASH, tsize=7.4,
              bsize=6.8, vcentre=True)
        if i < 3:
            _arrow(ax, x + w + 0.01, 2.42, x + w + gap - 0.01, 2.42)
    return _save(fig, "phases")


def fig_flywheel():
    """Why it compounds: the loop that makes the next cohort cheaper to win."""
    import math
    nodes = ["Universities open campuses", "Ambassadors run workshops",
             "Founders complete missions", "Stories become content",
             "Partners fund cohorts"]
    W, H = 5.2, 3.25
    fig, ax = _canvas(W, H)
    cx, cy, R = W / 2, H / 2 + 0.05, 1.16
    pts = []
    for i in range(len(nodes)):
        a = math.pi / 2 - i * 2 * math.pi / len(nodes)
        pts.append((cx + R * math.cos(a), cy + R * math.sin(a) * 0.90))
    for i, (x, y) in enumerate(pts):
        nx, ny = pts[(i + 1) % len(pts)]
        ax.add_patch(FancyArrowPatch((x, y), (nx, ny), arrowstyle="-|>",
                                     mutation_scale=10, color="#C3C8D6",
                                     linewidth=1.2, zorder=1,
                                     connectionstyle="arc3,rad=-0.21",
                                     shrinkA=30, shrinkB=30))
    for i, ((x, y), label) in enumerate(zip(pts, nodes)):
        fill = SPECTRUM[i * 2]
        ax.add_patch(plt.Circle((x, y), 0.40, color=fill, zorder=3))
        tcol, _ = _ink_for(fill)
        ax.text(x, y, "\n".join(_wrap(label, 6.6, 0.70)), fontsize=6.6, color=tcol,
                ha="center", va="center", fontweight="bold", linespacing=1.35,
                zorder=4)
    ax.text(cx, cy + 0.10, "Growth comes\nfrom the loop", fontsize=8.4, color=INK,
            ha="center", va="center", fontweight="bold", linespacing=1.5)
    ax.text(cx, cy - 0.28, "not from paid reach", fontsize=6.9, color=MUTED,
            ha="center", va="center")
    return _save(fig, "flywheel")


def fig_ngo_initiatives():
    """
    The named public programmes, with the route into each.

    Built from the plan's own named-target table rather than typed here, so the
    figure and the prose cannot drift apart.
    """
    items = M.NAMED_INITIATIVES[:6]
    W = 7.1
    gap = 0.12
    w = (W - 2 * gap) / 3
    cells = []
    for row in items:
        org, market, runs, supply, plays, route = row
        name = org.split(" — ")[0].split(", and ")[0]
        sub = org.split(" — ")[1] if " — " in org else market
        cells.append((name, f"{market} · {sub}" if sub != market else market,
                      supply, plays))
    rowh = []
    for name, sub, supply, plays in cells:
        nl = _wrap(name, 8.0, w - 2 * PAD)
        sl = _wrap(sub, 6.3, w - 2 * PAD)
        bl = _wrap(supply, 6.7, w - 2 * PAD)
        rowh.append(0.30 + _lines_h(nl, 8.0) + _lines_h(sl, 6.3)
                    + _lines_h(bl, 6.7))
    h1 = max(rowh[:3])
    h2 = max(rowh[3:])
    H = h1 + h2 + gap + 0.06
    fig, ax = _canvas(W, H)
    for i, (name, sub, supply, plays) in enumerate(cells):
        col, row = i % 3, i // 3
        x = col * (w + gap)
        hh = h1 if row == 0 else h2
        top = H - 0.03 - (0 if row == 0 else h1 + gap)
        ax.add_patch(FancyBboxPatch((x, top - hh), w, hh,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=WASH, edgecolor="none", zorder=2))
        ax.add_patch(Rectangle((x, top - 0.11), w, 0.11, color=spec(i, 6),
                               zorder=3))
        y = top - 0.20
        nl = _wrap(name, 8.0, w - 2 * PAD)
        ax.text(x + PAD, y, "\n".join(nl), fontsize=8.0, fontweight="bold",
                color=INK, va="top", zorder=4, linespacing=1.36)
        y -= _lines_h(nl, 8.0) + 0.028
        sl = _wrap(sub, 6.3, w - 2 * PAD)
        ax.text(x + PAD, y, "\n".join(sl), fontsize=6.3, color=UV, va="top",
                zorder=4, linespacing=1.4)
        y -= _lines_h(sl, 6.3) + 0.04
        ax.text(x + PAD, y, "\n".join(_wrap(supply, 6.7, w - 2 * PAD)),
                fontsize=6.7, color=INK2, va="top", zorder=4, linespacing=1.45)
        ax.text(x + w - PAD, top - hh + 0.06, plays, fontsize=6.4, color=UV,
                fontweight="bold", ha="right", va="bottom", zorder=4)
    return _save(fig, "ngo_initiatives")


def fig_team_arc():
    """
    Six people to twenty, and the reason for each step.

    The card height is measured from the longest card rather than fixed, because
    the whole point of this figure is the reasoning underneath each number and a
    clipped reason would defeat it.
    """
    arc = [
        ("YEAR 1", "6", "Build it and open the first doors",
         "Chief executive, chief technology officer, one engineer, curriculum, "
         "Egyptian partnerships and growth. Operations sits with the CEO."),
        ("YEAR 2", "9", "A second market, and a network to deliver",
         "A resident Riyadh country manager, a second engineer, and the partner "
         "network manager the entire operating model depends on."),
        ("YEAR 3", "12", "Public money, and the volume it brings",
         "Government and donors, a delivery coordinator to hold the calendar, "
         "and a bids associate so the heads can keep selling."),
        ("YEAR 4", "16", "Hand operations over at last",
         "A chief operating officer, an AI and data engineer, a schools and "
         "technical head, and a second coordinator."),
        ("YEAR 5", "20", "Keep what has been won",
         "Renewals, student success, a designer and a curriculum producer — the "
         "first roles that protect an existing book rather than win a new one."),
    ]
    W = 7.1
    gap = 0.10
    w = (W - 4 * gap) / 5
    inner = w - 2 * PAD
    numh = 0.92
    bodyh = max(_lines_h(_wrap(t, 7.6, inner, bold=True), 7.6) + 0.05
                + _lines_h(_wrap(b, 6.7, inner), 6.7) for _, _, t, b in arc) + 0.16
    H = numh + bodyh + 0.14
    fig, ax = _canvas(W, H)
    for i, (tag, n, title, body) in enumerate(arc):
        x = i * (w + gap)
        fill = spec(i, 5)
        ink, sub = _ink_for(fill)
        ax.add_patch(FancyBboxPatch((x, H - numh - 0.02), w, numh,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=fill, edgecolor="none", zorder=3))
        ax.text(x + PAD, H - 0.10, tag, fontsize=6.3, color=sub,
                fontweight="bold", va="top", zorder=4)
        ax.text(x + PAD, H - 0.28, n, fontsize=21, color=ink, fontweight="bold",
                va="top", zorder=4)
        ax.text(x + w - PAD, H - numh + 0.06, "people", fontsize=6.6, color=sub,
                ha="right", va="bottom", zorder=4)
        _chip(ax, x, 0.04, w, bodyh, title, body, WASH, tsize=7.6, bsize=6.7)
        if i < 4:
            _arrow(ax, x + w + 0.005, H - numh / 2 - 0.02,
                   x + w + gap - 0.005, H - numh / 2 - 0.02)
    return _save(fig, "team_arc")


def fig_leverage():
    """
    Why twelve people can stand behind three hundred cohorts.

    Four bands, three bars each — year one palest, year three solid. The bands
    share one scale, which is the only way the ratio between the employee bar and
    the cohort bar reads honestly rather than being asserted in a caption.
    """
    rows = M.leverage()
    bands = [("StartPad employees", "staff", UV),
             ("Certified facilitators", "pool", "#0096DF"),
             ("Certified partner organisations", "partners", "#00C8B6"),
             ("Cohorts delivered in the year", "cohorts", "#8FD92F")]
    W = 7.1
    labw, rpad = 2.16, 0.92
    barh, bargap, bandgap = 0.115, 0.026, 0.20
    nrows = len(rows)
    bandh = nrows * barh + (nrows - 1) * bargap
    footer = 0.74
    H = footer + len(bands) * (bandh + bandgap) + 0.06
    fig, ax = _canvas(W, H)
    barw = W - labw - rpad
    maxv = max(r["cohorts"] for r in rows)
    top = H - 0.06
    for label, key, col in bands:
        ax.text(0, top - bandh / 2, "\n".join(_wrap(label, 7.5, labw - 0.14)),
                fontsize=7.5, color=INK, va="center", zorder=4, linespacing=1.35)
        for ri, r in enumerate(rows):
            yy = top - barh - ri * (barh + bargap)
            v = r[key]
            w = max(0.030, barw * v / maxv)
            # The alpha ramp has to span however many years there are, not a
            # hardcoded three, or a fourth year raises IndexError.
            alpha = 0.34 + 0.66 * (ri / max(1, nrows - 1))
            ax.add_patch(Rectangle((labw, yy), w, barh, color=col,
                                   alpha=alpha, zorder=3))
            ax.text(labw + w + 0.06, yy + barh / 2,
                    f"Y{r['year']}  {v:,.0f}", fontsize=6.4, color=INK2,
                    va="center", zorder=4)
        top -= bandh + bandgap

    ax.add_patch(Rectangle((0, footer - 0.10), W, 0.012, color=HAIR, zorder=2))
    ax.text(0, footer - 0.30, "Learners reached per employee", fontsize=7.5,
            color=INK, va="center", zorder=4)
    step = (W - labw) / nrows
    for ri, r in enumerate(rows):
        ax.text(labw + ri * step, footer - 0.30,
                f"Y{r['year']}  {r['learners_per_employee']:,.0f}",
                fontsize=8.4, color=UV, fontweight="bold", va="center",
                zorder=4)
    ax.text(0, 0.08, "Every cohort in this plan is delivered by a certified "
            "facilitator or a certified partner organisation, never by an "
            "employee. Headcount therefore tracks the number of partners to "
            "audit, not the number of cohorts to run.",
            fontsize=6.5, color=MUTED, va="center", zorder=4)
    return _save(fig, "leverage")


def fig_engagement_plays():
    """
    The six ways in, ordered by how little the counterparty has to risk.

    Each card carries who is approached and how the money moves, because an
    engagement model that names neither the person nor the invoice is a diagram
    of a hope. Card height is measured from the longest card's content rather
    than guessed, so nothing overflows when the wording changes.
    """
    plays = [(c, n, who, money)
             for c, n, who, _ask, money, _pre, _len in M.ENGAGEMENT_PLAYS]
    W = 7.1
    gap = 0.13
    w = (W - gap) / 2
    inner = w - 2 * PAD
    head = 0.52

    def body_h(who, money):
        h = 0.0
        for txt in (who, money):
            h += 0.105                                    # the small caps label
            h += _lines_h(_wrap(txt, 6.6, inner), 6.6)
            h += 0.045
        return h

    ch = head + max(body_h(p[2], p[3]) for p in plays) + 0.10
    H = 3 * ch + 2 * gap + 0.04
    fig, ax = _canvas(W, H)
    for i, (code, name, who, money) in enumerate(plays):
        cx = (i % 2) * (w + gap)
        cy = H - 0.02 - (i // 2 + 1) * ch - (i // 2) * gap
        fill = spec(i, 6)
        ink, sub = _ink_for(fill)
        ax.add_patch(FancyBboxPatch((cx, cy), w, ch,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=WASH, edgecolor="none", zorder=2))
        ax.add_patch(FancyBboxPatch((cx, cy + ch - head), w, head,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=fill, edgecolor="none", zorder=3))
        ax.add_patch(Rectangle((cx, cy + ch - head), w, 0.06, color=fill,
                               zorder=3))
        ax.text(cx + PAD, cy + ch - 0.08, code, fontsize=6.4, color=sub,
                fontweight="bold", va="top", zorder=5)
        ax.text(cx + PAD, cy + ch - 0.21, name, fontsize=9.4, color=ink,
                fontweight="bold", va="top", zorder=5)
        y = cy + ch - head - 0.07
        for lab, txt in (("WHO IS APPROACHED", who), ("HOW THE MONEY MOVES", money)):
            ax.text(cx + PAD, y, lab, fontsize=5.9, color=UV, fontweight="bold",
                    va="top", zorder=4)
            y -= 0.105
            tl = _wrap(txt, 6.6, inner)
            ax.text(cx + PAD, y, "\n".join(tl), fontsize=6.6, color=INK2,
                    va="top", zorder=4, linespacing=1.42)
            y -= _lines_h(tl, 6.6) + 0.045
    return _save(fig, "engagement_plays")


def fig_engagement_route():
    """
    How StartPad gets inside a programme it does not own.

    The same five steps every time, which is the point: the route is a repeatable
    procedure rather than a series of lucky introductions.
    """
    steps = [
        ("01", "Find the edge", "Enter at one campus, one branch, one chapter — "
         "never at head office, which cannot authorise a first.", "Week 0"),
        ("02", "Fund the proof", "One cohort at StartPad's cost, inside their "
         "programme, with their name on the report.", "Weeks 1–8"),
        ("03", "Publish it", "The report, a Mission Zero episode recorded there, "
         "and the showcase their leadership attends.", "Week 9"),
        ("04", "Price the block", "Take the report upward and ask for seats or a "
         "season — a line in their budget, not a new programme.", "Months 3–9"),
        ("05", "Certify them", "Their trainers, their facilitators, our standard "
         "and our audit. Volume without headcount.", "Months 9–18"),
    ]
    W, H = 7.1, 2.08
    fig, ax = _canvas(W, H)
    gap = 0.11
    w = (W - 4 * gap) / 5
    for i, (num, title, body, when) in enumerate(steps):
        x = i * (w + gap)
        fill = spec(i, 5)
        ink, sub = _ink_for(fill)
        ax.add_patch(FancyBboxPatch((x, 0.40), w, 1.64,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=WASH, edgecolor="none", zorder=2))
        ax.add_patch(Rectangle((x, 1.92), w, 0.12, color=fill, zorder=3))
        ax.text(x + PAD, 1.84, num, fontsize=6.6, color=UV, fontweight="bold",
                va="top", zorder=4)
        tl = _wrap(title, 8.6, w - 2 * PAD)
        ax.text(x + PAD, 1.70, "\n".join(tl), fontsize=8.6, color=INK,
                fontweight="bold", va="top", zorder=4, linespacing=1.3)
        yy = 1.70 - _lines_h(tl, 8.6) - 0.05
        ax.text(x + PAD, yy, "\n".join(_wrap(body, 6.7, w - 2 * PAD)),
                fontsize=6.7, color=INK2, va="top", zorder=4, linespacing=1.45)
        _chip(ax, x, 0.04, w, 0.30, None, when, fill, bsize=6.6, centre=True,
              vcentre=True)
        if i < 4:
            _arrow(ax, x + w + 0.005, 1.20, x + w + gap - 0.005, 1.20)
    return _save(fig, "engagement_route")


def fig_named_targets():
    """
    The named organisations, by engine, each tagged with the plays that open it.

    Nothing in this plan's revenue is attributed to any one of these. They are
    here so a reader can check that the market described has real buyers running
    real programmes, and that there is a stated route into each. Column heights
    are measured from the wrapped content — including the column heading, which
    wraps to two lines in two of the three columns — so no entry can fall
    outside its own panel.
    """
    groups = [
        ("National initiatives and government", M.NAMED_INITIATIVES, UV),
        ("Sponsored competitions and youth organisations", M.NAMED_COMPETITIONS,
         "#0096DF"),
        ("Delivery partners, donors and sponsors", M.NAMED_PARTNERS, "#00C8B6"),
    ]
    W = 7.1
    gap = 0.14
    colw = (W - 2 * gap) / 3
    inner = colw - 2 * PAD
    BAR, HEADGAP, ENTRYGAP, FOOT = 0.11, 0.07, 0.185, 0.12

    cols = []
    for title, items, col in groups:
        head = _wrap(title, 7.6, inner, bold=True)
        entries = []
        for row in items:
            org, market, plays = row[0], row[1], row[4]
            name = (org.split(" — ")[0].split(", under")[0]
                       .split(" and the ")[0].split(", and ")[0])
            entries.append((_wrap(name, 7.0, inner - 0.12), f"{market}  ·  {plays}"))
        h = (BAR + 0.09 + _lines_h(head, 7.6) + HEADGAP
             + sum(_lines_h(e[0], 7.0) + ENTRYGAP for e in entries) + FOOT)
        cols.append((head, entries, col, h))

    H = max(c[3] for c in cols) + 0.06
    fig, ax = _canvas(W, H)
    for gi, (head, entries, col, h) in enumerate(cols):
        x = gi * (colw + gap)
        top = H - 0.03
        ax.add_patch(FancyBboxPatch((x, top - h), colw, h,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=WASH, edgecolor="none", zorder=2))
        ax.add_patch(Rectangle((x, top - BAR), colw, BAR, color=col, zorder=3))
        y = top - BAR - 0.09
        ax.text(x + PAD, y, "\n".join(head), fontsize=7.6, color=INK,
                fontweight="bold", va="top", zorder=4, linespacing=1.32)
        y -= _lines_h(head, 7.6) + HEADGAP
        for lines, meta in entries:
            lh = _lines_h(lines, 7.0)
            ax.add_patch(Rectangle((x + PAD, y - lh - 0.075), 0.035, lh + 0.055,
                                   color=col, zorder=4))
            ax.text(x + PAD + 0.10, y, "\n".join(lines), fontsize=7.0, color=INK,
                    va="top", zorder=4, linespacing=1.38)
            ax.text(x + PAD + 0.10, y - lh - 0.012, meta, fontsize=6.1, color=UV,
                    va="top", zorder=4)
            y -= lh + ENTRYGAP
    return _save(fig, "named_targets")


def fig_podcast():
    """
    Mission Zero: the chain by which a podcast becomes institutional pipeline.

    Drawn as a chain rather than a funnel because each link produces the next and
    the last one feeds the first — a founder featured becomes the reason the next
    founder agrees.
    """
    chain = M.PODCAST["chain"]
    W = 7.1
    H = 0.60 + len(chain) * 0.455
    fig, ax = _canvas(W, H)
    ax.text(0, H - 0.09, f"{M.PODCAST['name']}  ·  {M.PODCAST['arabic']}",
            fontsize=11.5, color=INK, fontweight="bold", va="top", zorder=4)
    ax.text(0, H - 0.33, "\n".join(_wrap(M.PODCAST["premise"], 7.0, W)),
            fontsize=7.0, color=MUTED, va="top", zorder=4, linespacing=1.45)
    y = H - 0.60
    lw = 3.52
    for i, (step, effect) in enumerate(chain):
        fill = spec(i, len(chain))
        ink, sub = _ink_for(fill)
        ax.add_patch(FancyBboxPatch((0, y - 0.40), lw, 0.40,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=fill, edgecolor="none", zorder=3))
        ax.text(0.10, y - 0.20, "\n".join(_wrap(step, 7.3, lw - 0.26)[:2]),
                fontsize=7.3, color=ink, fontweight="bold", va="center", zorder=4,
                linespacing=1.35)
        ax.add_patch(FancyBboxPatch((lw + 0.30, y - 0.40), W - lw - 0.30, 0.40,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=WASH, edgecolor="none", zorder=3))
        ax.text(lw + 0.40, y - 0.20,
                "\n".join(_wrap(effect, 7.0, W - lw - 0.52)[:2]), fontsize=7.0,
                color=INK2, va="center", zorder=4, linespacing=1.35)
        _arrow(ax, lw + 0.05, y - 0.20, lw + 0.26, y - 0.20)
        if i < len(chain) - 1:
            _arrow(ax, lw / 2, y - 0.41, lw / 2, y - 0.52)
        y -= 0.455
    return _save(fig, "podcast")


def fig_podcast_targets():
    """What the podcast is held to, year by year. Views are last on purpose."""
    tg = M.PODCAST["targets"]
    fig, ax = plt.subplots(figsize=(7.1, 2.85))
    labels = [t[0] for t in tg]
    y = list(range(len(labels)))[::-1]
    width = 0.26
    for j, (yr, col) in enumerate(zip((1, 2, 3), [UV, "#0096DF", "#00D3A4"])):
        vals = [t[1 + j] for t in tg]
        mx = [max(t[1], t[2], t[3]) for t in tg]
        norm = [v / m if m else 0 for v, m in zip(vals, mx)]
        ax.barh([yy + (1 - j) * width for yy in y], norm, width, color=col,
                label=f"Year {yr}", zorder=3)
        for yy, nv, v in zip(y, norm, vals):
            ax.text(nv + 0.012, yy + (1 - j) * width, f"{v:,}", fontsize=6.6,
                    color=INK2, va="center", zorder=4)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7.2, color=INK)
    ax.set_xlim(0, 1.20)
    ax.set_xticks([])
    for s in ("top", "right", "bottom", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.legend(frameon=False, fontsize=7.2, loc="lower right", labelcolor=INK2,
              ncol=3)
    ax.text(0, len(labels) - 0.15, "Each row is scaled to its own year-three "
            "value, so the shape of the growth is comparable across metrics "
            "measured in different units.", fontsize=6.4, color=MUTED)
    return _save(fig, "podcast_targets")


# =====================================================================
#  FINANCIAL PLAN FIGURES
# =====================================================================
#
# These five read the financial model through the bridge, so they cannot show
# anything the workbook does not say. Every one of them is laid out by
# measurement: a label goes inside a bar only when the bar is wide or tall
# enough to hold it with padding, and outside it otherwise.

def _fin():
    return M.FL


def _year_labels():
    return [f"Y{y}" for y in M.YEARS_5]


def _stack_labels(values, gap):
    """
    Label positions for several points sharing one x, never closer than `gap`.

    Returns a list of y positions in the same order as `values`. Points are
    walked from the lowest up and each label is pushed above the one below it
    when it would otherwise collide, which is the only way three series on one
    scale can be labelled without the type touching.
    """
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    last = None
    for i in order:
        y = values[i] + gap * 0.55
        if last is not None and y - last < gap:
            y = last + gap
        out[i] = y
        last = y
    return out


def fig_fin_revenue_mix():
    """
    Revenue by family across five years.

    Stacked, because the question the page asks is what share of the business
    each family carries, not what each one is worth on its own. A segment
    label is only drawn when the segment is tall enough to hold it.
    """
    FL = _fin()
    fams = FL.revenue_by_family()
    order = [f for f in ("Education", "Public", "Commercial", "Direct")
             if f in fams]
    totals = [sum(fams[f][i] for f in order) for i in range(FL.YEARS)]
    fig, ax = plt.subplots(figsize=(7.1, 3.5))
    x = list(range(FL.YEARS))
    bottoms = [0.0] * FL.YEARS
    cols = [UV, "#0087E8", "#00C8B6", "#A1EE58"]
    top = max(totals) if totals else 1.0
    for fam, c in zip(order, cols):
        vals = fams[fam]
        ax.bar(x, vals, 0.54, bottom=bottoms, color=c, label=fam,
               edgecolor=WHITE, linewidth=1.1, zorder=3)
        for i, v in enumerate(vals):
            # Only label a segment that is at least a tenth of the tallest
            # column: below that the type collides with the segment above.
            if v > top * 0.10:
                ink = INK if c == "#A1EE58" else WHITE
                ax.text(i, bottoms[i] + v / 2, _money(v), ha="center",
                        va="center", fontsize=7.6, color=ink, zorder=6)
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    for i, t in enumerate(totals):
        ax.text(i, t + top * 0.035, _money(t), ha="center", fontsize=10,
                fontweight="bold", color=INK, zorder=7)
    ax.set_xticks(x)
    ax.set_xticklabels([f"Year {y}" for y in M.YEARS_5], fontsize=9,
                       color=INK)
    ax.set_ylabel("Revenue")
    ax.set_ylim(0, top * 1.20)
    ax.set_yticklabels([])
    ax.tick_params(axis="y", length=0)
    _clean(ax, grid="y")
    ax.legend(frameon=False, fontsize=7.6, loc="upper left", ncol=2,
              labelcolor=INK2)
    return _save(fig, "fin_revenue_mix")


def fig_fin_cost_stack():
    """
    What the money goes on each year, against the revenue it produces.

    Cost is stacked and revenue is a line, because the comparison is the
    point: the year the line clears the stack is the year the company turns.
    """
    FL = _fin()
    head = FL.headline()
    rev = [h["revenue"] for h in head]
    groups = [M.costs(y)["lines"] for y in M.YEARS_5]
    names = [k for k, _ in groups[0]]
    fig, ax = plt.subplots(figsize=(7.1, 3.6))
    x = list(range(FL.YEARS))
    bottoms = [0.0] * FL.YEARS
    # Six headings need six colours a reader can tell apart in print; the two
    # adjacent blues in the house ramp were indistinguishable at legend size.
    cols = [UV, "#0071ED", "#00ABD4", "#00DC91", "#A1EE58", "#C9CEDA"]
    light = {"#00DC91", "#A1EE58", "#C9CEDA"}
    top = max(max(rev), max(sum(v for _, v in g) for g in groups))
    for idx, name in enumerate(names):
        vals = [dict(g)[name] for g in groups]
        c = cols[idx % len(cols)]
        ax.bar(x, vals, 0.54, bottom=bottoms, color=c, label=name,
               edgecolor=WHITE, linewidth=1.0, zorder=3)
        for i, v in enumerate(vals):
            if v > top * 0.085:
                ink = INK if c in light else WHITE
                ax.text(i, bottoms[i] + v / 2, _money(v), ha="center",
                        va="center", fontsize=7.2, color=ink, zorder=6)
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    ax.plot(x, rev, color="#C2185B", linewidth=2.0, marker="o",
            markersize=5, zorder=8, label="Revenue")
    for i, v in enumerate(rev):
        # Always above, and above the stack as well as the point, so the
        # label can never land on a segment or on the axis labels below.
        y = max(v, bottoms[i]) + top * 0.045
        ax.text(i, y, _money(v), ha="center", va="bottom", fontsize=8.6,
                fontweight="bold", color="#C2185B", zorder=9)
    ax.set_xticks(x)
    ax.set_xticklabels([f"Year {y}" for y in M.YEARS_5], fontsize=9,
                       color=INK)
    ax.set_ylim(0, top * 1.16)
    ax.set_yticklabels([])
    ax.tick_params(axis="y", length=0)
    ax.set_ylabel("Cost, stacked, against revenue")
    _clean(ax, grid="y")
    # Below the axes: seven entries will not fit beside the bars without
    # covering year five.
    ax.legend(frameon=False, fontsize=7.4, loc="upper center",
              bbox_to_anchor=(0.5, -0.09), ncol=4, labelcolor=INK2,
              handlelength=1.4, columnspacing=1.4)
    return _save(fig, "fin_cost_stack")


def fig_fin_cash():
    """
    Cash across sixty months, with the trough marked.

    A line, not bars: the shape is the argument, and the one number a reader
    needs is the lowest point and the month it happens in.
    """
    FL = _fin()
    cp = FL.cash_profile()
    cash = cp["monthly"]
    x = list(range(1, len(cash) + 1))
    fig, ax = plt.subplots(figsize=(7.1, 3.2))
    ax.axhline(0, color=HAIR, linewidth=0.9, zorder=1)
    ax.fill_between(x, cash, 0, color=UV, alpha=0.10, zorder=2)
    ax.plot(x, cash, color=UV, linewidth=1.9, zorder=4)
    ti, tv = cp["trough_month"], cp["trough"]
    ax.plot([ti], [tv], marker="o", markersize=6, color="#C2185B", zorder=6)
    top = max(cash)
    ax.annotate(f"Trough {_money(tv)}\nmonth {ti}",
                xy=(ti, tv), xytext=(ti + 4, tv + top * 0.20),
                fontsize=8.2, color="#C2185B",
                arrowprops=dict(arrowstyle="-", color="#C2185B",
                                linewidth=0.9))
    sm = cp["seed_month"]
    ax.axvline(sm, color=MUTED, linewidth=0.9, linestyle=(0, (3, 3)),
               zorder=3)
    ax.text(sm + 0.8, top * 0.94, f"Seed {_money(cp['seed'])}\nlands month "
                                  f"{sm}", fontsize=7.6, color=MUTED,
            va="top")
    ax.set_xlim(0, len(cash) + 1)
    ax.set_ylim(min(0, min(cash)) - top * 0.06, top * 1.12)
    ax.set_xticks([y * 12 - 6 for y in M.YEARS_5])
    ax.set_xticklabels([f"Year {y}" for y in M.YEARS_5], fontsize=8.6,
                       color=INK)
    ax.tick_params(axis="x", length=0)
    ax.set_ylabel("Cash at month end")
    ax.set_yticks([0, top / 2, top])
    ax.set_yticklabels(["0", _money(top / 2), _money(top)], fontsize=8)
    _clean(ax, grid="y")
    return _save(fig, "fin_cash")


def fig_fin_funnel():
    """
    Year one, from spend to signature.

    A horizontal bar per stage, widths proportional to the count, with the
    conversion from the stage above printed on the right so the page carries
    the rate as well as the number.
    """
    FL = _fin()
    f = FL.funnel()
    bs = FL.buyers()
    stages = [
        ("Marketing spend", f["marketing"][0], True),
        ("Institutional leads", f["leads"][0], False),
        ("Meetings held", sum(b["meetings"][0] for b in bs), False),
        ("Proposals and bids", sum(b["proposals"][0] for b in bs), False),
        ("Contracts signed", f["signed"][0], False),
    ]
    counts = [v for _, v, is_money in stages if not is_money]
    top = max(counts) if counts else 1.0
    fig, ax = plt.subplots(figsize=(7.1, 3.1))
    rows = stages[1:]
    yy = list(range(len(rows)))[::-1]
    cols = [UV, "#0071ED", "#00ABD4", "#00D3A4"]
    for i, ((label, v, _), c) in enumerate(zip(rows, cols)):
        y = yy[i]
        ax.barh(y, v, height=0.56, color=c, zorder=3)
        txt = f"{v:,.0f}"
        # Inside the bar when it is wide enough to hold the number with
        # padding, outside it when it is not.
        if v > top * 0.22:
            ax.text(v - top * 0.015, y, txt, ha="right", va="center",
                    fontsize=9.4, fontweight="bold", color=WHITE, zorder=6)
        else:
            ax.text(v + top * 0.015, y, txt, ha="left", va="center",
                    fontsize=9.4, fontweight="bold", color=INK, zorder=6)
        if i:
            prev = rows[i - 1][1]
            rate = (v / prev) if prev else 0.0
            ax.text(top * 1.12, y, f"{rate*100:,.0f}% of the stage above",
                    ha="left", va="center", fontsize=7.8, color=MUTED,
                    zorder=6)
    ax.set_yticks(yy)
    ax.set_yticklabels([r[0] for r in rows], fontsize=9, color=INK)
    ax.set_xlim(0, top * 1.55)
    ax.set_xticks([])
    ax.set_title(f"Year one. {_money(stages[0][1])} of marketing spend, "
                 f"{rows[-1][1]:,.0f} contracts signed",
                 fontsize=8.6, color=INK2, loc="left", pad=10)
    _clean(ax, grid=None)
    ax.spines["bottom"].set_visible(False)
    return _save(fig, "fin_funnel")


def fig_fin_margin():
    """
    Gross margin, EBITDA margin and net margin across five years.

    Three lines on one percentage scale, because the shape of the three
    together is what says whether the business scales or merely grows.
    """
    FL = _fin()
    head = FL.headline()
    x = list(range(FL.YEARS))
    series = [("Gross margin", [h["gross_margin"] for h in head], UV),
              ("EBITDA margin", [h["ebitda_margin"] for h in head], "#00ABD4"),
              ("Net margin", [h["net_margin"] for h in head], "#C2185B")]
    fig, ax = plt.subplots(figsize=(7.1, 3.1))
    ax.axhline(0, color=HAIR, linewidth=0.9, zorder=1)
    lo = min(min(v) for _, v, _ in series)
    hi = max(max(v) for _, v, _ in series)
    span = max(hi - lo, 0.05)
    for name, vals, c in series:
        ax.plot(x, vals, color=c, linewidth=1.9, marker="o", markersize=4.6,
                label=name, zorder=4)
    # Labels are placed per column rather than per series, so three values
    # that sit close together are spread instead of printed on top of one
    # another.
    gap = span * 0.115
    tops = []
    for i in range(len(x)):
        col = [vals[i] for _, vals, _ in series]
        ys = _stack_labels(col, gap)
        tops.append(max(ys))
        for (name, vals, c), y in zip(series, ys):
            ax.text(i, y, f"{vals[i]*100:,.0f}%", ha="center", va="bottom",
                    fontsize=7.8, color=c, zorder=6)
    ax.set_xticks(x)
    ax.set_xticklabels([f"Year {y}" for y in M.YEARS_5], fontsize=9,
                       color=INK)
    ax.set_ylim(lo - span * 0.16, max(max(tops), hi) + span * 0.20)
    ax.set_yticklabels([])
    ax.tick_params(axis="y", length=0)
    ax.set_ylabel("Margin")
    _clean(ax, grid="y")
    ax.legend(frameon=False, fontsize=7.6, loc="upper center",
              bbox_to_anchor=(0.5, -0.09), ncol=3, labelcolor=INK2,
              handlelength=1.4)
    return _save(fig, "fin_margin")


ALL = [fig_tam_som, fig_fin_revenue_mix, fig_fin_cost_stack, fig_fin_cash,
       fig_fin_funnel, fig_fin_margin,
       fig_segments, fig_tam_sam, fig_engine_mix, fig_roadmap, fig_gates,
       fig_quarterly_volumes, fig_customer_journey, fig_channel_mix, fig_swot,
       fig_porter, fig_pestle, fig_moat, fig_school_ladder,
       fig_engine_economics, fig_deal_sizes, fig_pipeline,
       fig_university_ladder, fig_initiative_scale, fig_initiative_model,
       fig_competition_model, fig_subscription_sources,
       fig_cohort_ramp, fig_headcount, fig_gtm_moves, fig_institution_workflow,
       fig_bootcamp_map, fig_org_chart, fig_phases, fig_flywheel,
       fig_ngo_initiatives, fig_team_arc, fig_leverage, fig_engagement_plays,
       fig_engagement_route, fig_named_targets, fig_podcast,
       fig_podcast_targets]


def build_all():
    return [f() for f in ALL]


if __name__ == "__main__":
    for p in build_all():
        print("wrote", os.path.basename(p))
