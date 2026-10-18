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
PAD = 0.075         # inches of padding inside a chip
LINE = 1.52         # line spacing multiple


def _canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig, ax


def _wrap(text, size, width_in):
    """Break text to a pixel width without ever dropping a word."""
    cols = max(4, int(width_in * 72 / (size * _CHAR_W)))
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
            block += _lines_h(_wrap(title, tsize, inner), tsize) + (0.035 if body else 0)
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
        tl = _wrap(title, tsize, inner)
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

def fig_pl():
    yrs = M.projection()
    fig, ax = plt.subplots(figsize=(7.1, 3.0))
    x = range(len(yrs))
    w = 0.33
    ax.bar([i - w / 2 for i in x], [y["revenue"] for y in yrs], w,
           color=UV, label="Revenue", zorder=3)
    ax.bar([i + w / 2 for i in x], [y["cost"] for y in yrs], w,
           color=HAIR, label="Operating cost", zorder=3)
    top = max(y["revenue"] for y in yrs)
    for i, y in enumerate(yrs):
        ax.text(i - w / 2, y["revenue"] * 1.025, _money(y["revenue"]), ha="center",
                fontsize=8, color=INK, fontweight="bold")
        ax.text(i + w / 2, y["cost"] * 1.025, _money(y["cost"]), ha="center",
                fontsize=8, color=INK2)
        p = y["profit"]
        col = "#B4231F" if p < 0 else "#0F7A4B"
        ax.text(i, -top * 0.135, f"{'−' if p < 0 else '+'}{_money(abs(p))}",
                ha="center", fontsize=9, fontweight="bold", color=col)
    ax.text(-0.70, -top * 0.135, "Result", ha="left", fontsize=8, color=MUTED)
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"Year {y['year']}" for y in yrs], fontsize=9, color=INK)
    ax.set_ylim(0, top * 1.14)
    ax.yaxis.set_major_formatter(lambda v, p: f"${v/1e6:,.0f}m" if v else "0")
    _clean(ax, grid="y")
    ax.legend(frameon=False, fontsize=8, loc="upper left", labelcolor=INK2)
    return _save(fig, "pl")


# =====================================================================
#  9 · Subscriptions, as a consequence of the engines
# =====================================================================

def fig_subscription_sources():
    """Where paying founders come from. Almost none of them are strangers."""
    s = M.subscriptions(1)
    rows = sorted(s["rows"], key=lambda r: -r["paid"])
    fig, ax = plt.subplots(figsize=(7.1, 2.55))
    for i, r in enumerate(rows):
        organic = r["name"].startswith("Organic")
        ax.barh(i, r["paid"], 0.52, color="#C9CEDB" if organic else UV, zorder=3)
        ax.text(r["paid"] + 3, i, f"{r['paid']:,.0f} paying",
                va="center", fontsize=7.8, color=INK, fontweight="bold")
        ax.text(r["paid"] + 3, i - 0.30,
                f"from {r['reached']:,} reached, at {r['conversion']*100:.0f}%",
                va="center", fontsize=6.6, color=MUTED)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r["name"] for r in rows], fontsize=8.0, color=INK)
    ax.invert_yaxis()
    ax.set_xlim(0, max(r["paid"] for r in rows) * 1.55)
    ax.set_xlabel("Paying subscribers, year one")
    _clean(ax, grid="x")
    inst = sum(r["paid"] for r in rows if not r["name"].startswith("Organic"))
    ax.text(max(r["paid"] for r in rows) * 1.5, len(rows) - 0.35,
            f"{inst/s['paid']*100:.0f}% arrive through an organisation",
            ha="right", fontsize=7.6, color=INK2, fontweight="bold")
    return _save(fig, "subscription_sources")


def fig_cohort_ramp():
    """Delivery load against the facilitator capacity it needs, all twelve quarters."""
    cap = M.facilitator_capacity()
    fig, ax = plt.subplots(figsize=(7.1, 3.1))
    x = range(len(cap))
    uni = [c["uni"] for c in cap]
    sch = [c["school"] for c in cap]
    tv = [c["tvet"] for c in cap]
    ax.bar(x, uni, 0.62, color=UV, label="University cohorts", zorder=3)
    ax.bar(x, sch, 0.62, bottom=uni, color="#0096DF", label="School cohorts",
           zorder=3)
    ax.bar(x, tv, 0.62, bottom=[a + b for a, b in zip(uni, sch)], color="#00D3A4",
           label="Technical cohorts", zorder=3)
    ax2 = ax.twinx()
    ax2.plot(list(x), [c["facilitators"] for c in cap], color=INK, linewidth=1.7,
             marker="o", markersize=3.6, zorder=5, label="Facilitators required")
    for i, c in enumerate(cap):
        if i in (0, 3, 7, 11):
            ax2.text(i, c["facilitators"] + 4, f"{c['facilitators']:.0f}",
                     ha="center", fontsize=7.2, color=INK, fontweight="bold")
    ax2.set_ylim(0, max(c["facilitators"] for c in cap) * 1.45)
    ax2.set_ylabel("Facilitators required", color=INK2, fontsize=8.2)
    ax2.spines["top"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.spines["right"].set_color(HAIR)
    ax2.tick_params(labelsize=7.4)
    ax.set_xticks(list(x))
    ax.set_xticklabels([c["label"].replace(" ", "\n") for c in cap], fontsize=6.4,
                       color=INK2)
    ax.set_ylabel("Cohorts in the quarter")
    ax.set_ylim(0, max(c["total"] for c in cap) * 1.3)
    _clean(ax, grid="y")
    for b in (3.5, 7.5):
        ax.axvline(b, color=HAIR, linewidth=0.9, zorder=1)
    ax.legend(frameon=False, fontsize=7.2, loc="upper left", labelcolor=INK2)
    return _save(fig, "cohort_ramp")


def fig_headcount():
    by_fn, totals = M.headcount()
    fns = list(by_fn.keys())
    fig, ax = plt.subplots(figsize=(7.1, 3.2))
    x = range(3)
    bottoms = [0, 0, 0]
    cols = [UV, "#0071ED", "#00ABD4", "#00DC91", "#A1EE58", LIME, "#C9CEDB",
            "#8E96A8"]
    for fn, c in zip(fns, cols):
        vals = [by_fn[fn]["y1"], by_fn[fn]["y2"], by_fn[fn]["y3"]]
        ax.bar(x, vals, 0.5, bottom=bottoms, color=c, label=fn,
               edgecolor=WHITE, linewidth=1.1, zorder=3)
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    for i, t in enumerate([totals["y1"], totals["y2"], totals["y3"]]):
        ax.text(i, t + 1.6, f"{t} people", ha="center", fontsize=9.5,
                fontweight="bold", color=INK)
    ax.set_xticks(list(x))
    ax.set_xticklabels(["Year 1", "Year 2", "Year 3"], fontsize=9, color=INK)
    ax.set_ylabel("Establishment at year end")
    ax.set_ylim(0, totals["y3"] * 1.18)
    _clean(ax, grid="y")
    ax.legend(frameon=False, fontsize=7.6, loc="upper left", labelcolor=INK2)
    return _save(fig, "headcount")


# =====================================================================
#  9 · Where a cohort's $7,500 goes
def fig_gtm_moves():
    """The five moves, and what each one unlocks."""
    moves = [
        ("MOVE 01", "Universities", "Entrepreneurship centres, capstones, deans",
         "Access to students and credibility"),
        ("MOVE 02", "Ambassadors", "Campus teams, workshops, competitions",
         "Founders who start Mission 01"),
        ("MOVE 03", "Content", "Reels, founder podcast, community",
         "Reach beyond the campuses we are on"),
        ("MOVE 04", "Partners", "Programmes, NGOs, youth organisations",
         "Funded cohorts at scale"),
        ("MOVE 05", "KSA", "Running in parallel since September 2026",
         "Two markets from year one"),
    ]
    W, H = 7.1, 2.15
    fig, ax = _canvas(W, H)
    gap = 0.11
    w = (W - 4 * gap) / 5
    for i, (tag, title, body, unlock) in enumerate(moves):
        x = i * (w + gap)
        _chip(ax, x, 1.02, w, 1.10, title, body, SPECTRUM[i * 2], tag=tag,
              tsize=9.4, vcentre=True)
        _chip(ax, x, 0.03, w, 0.86, None, unlock, WASH, tag="UNLOCKS", bsize=7.0,
              vcentre=True)
        if i < 4:
            _arrow(ax, x + w + 0.01, 1.57, x + w + gap - 0.01, 1.57)
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
    """Year-one establishment, by reporting line."""
    by_fn, totals = M.headcount()
    W, H = 7.1, 3.25
    fig, ax = _canvas(W, H)
    _chip(ax, 2.20, 2.46, 2.70, 0.66, "Chief Executive Officer",
          "Institutional relationships · fundraising · runs Day 01 onboarding",
          UV, tsize=9.2, bsize=6.4, centre=True, vcentre=True)

    units = [("Chief Technology Officer", ["Product and Engineering"]),
             ("Chief Operating Officer", ["Delivery", "Curriculum and Content",
                                          "Operations and Finance"]),
             ("Head of Institutional Sales and KSA Country Manager",
              ["Institutional Sales"]),
             ("Head of Demand Generation", ["Demand Generation"])]
    gap = 0.12
    w = (W - 3 * gap) / 4
    for i, (title, fns) in enumerate(units):
        x = i * (w + gap)
        people = sum(by_fn[f]["y1"] for f in fns)
        _chip(ax, x, 1.74, w, 0.58, title, None, "#DDE3F6", tsize=7.4)
        _arrow(ax, W / 2, 2.44, x + w / 2, 2.35)
        ax.text(x + w - PAD, 1.80, f"{people}", fontsize=8.6, color=UV,
                fontweight="bold", ha="right", va="bottom", zorder=4)
        y = 1.62
        for f in fns:
            ax.add_patch(FancyBboxPatch((x, y - 0.34), w, 0.34,
                                        boxstyle="round,pad=0,rounding_size=0.05",
                                        facecolor=WASH, edgecolor="none", zorder=3))
            fl = _wrap(f, 6.8, w - 2 * PAD - 0.16)
            ax.text(x + PAD, y - 0.17, "\n".join(fl), fontsize=6.8, color=INK,
                    va="center", zorder=4, linespacing=1.3)
            ax.text(x + w - PAD, y - 0.17, str(by_fn[f]["y1"]), fontsize=7.2,
                    color=UV, fontweight="bold", va="center", ha="right", zorder=4)
            y -= 0.42
    ax.text(W / 2, 0.10, f"Year one: {totals['y1']} employees, plus a certified "
            f"freelance facilitator pool and {M.AMBASSADORS[1]} campus ambassadors",
            fontsize=7.2, color=INK2, ha="center")
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
    """The named national programmes StartPad is built to plug into."""
    items = [
        ("One Million Entrepreneurs", "Ministry of Planning · Rowad 2030",
         "One million entrepreneurs qualified by 2030, with Banque Misr and NBE"),
        ("1 Million Qualified Innovators", "Higher Education · UNDP · MBRF · ICESCO",
         "Launched in Cairo, April 2025. Future skills for one million young people"),
        ("MSMEDA governorate programme", "Qetar El Kheir · 22 governorates",
         "Free training reaching founders outside the urban technology hubs"),
        ("One Million International Licences", "With Cisco · announced May 2026",
         "Accredited technical and professional certification at national scale"),
    ]
    W, H = 7.1, 1.82
    fig, ax = _canvas(W, H)
    gap = 0.13
    w = (W - 3 * gap) / 4
    for i, (name, who, what) in enumerate(items):
        x = i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, 0.06), w, 1.70,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=WASH, edgecolor="none", zorder=2))
        ax.add_patch(Rectangle((x, 1.64), w, 0.12, color=SPECTRUM[i * 2], zorder=3))
        y = 1.50
        nl = _wrap(name, 7.8, w - 2 * PAD)
        ax.text(x + PAD, y, "\n".join(nl), fontsize=7.8, fontweight="bold",
                color=INK, va="top", zorder=4, linespacing=1.4)
        y -= _lines_h(nl, 7.8) + 0.04
        wl = _wrap(who, 6.5, w - 2 * PAD)
        ax.text(x + PAD, y, "\n".join(wl), fontsize=6.5, color=UV, va="top",
                zorder=4, linespacing=1.4)
        y -= _lines_h(wl, 6.5) + 0.05
        ax.text(x + PAD, y, "\n".join(_wrap(what, 6.8, w - 2 * PAD)), fontsize=6.8,
                color=INK2, va="top", zorder=4, linespacing=1.45)
    return _save(fig, "ngo_initiatives")




ALL = [fig_segments, fig_tam_sam, fig_engine_mix, fig_roadmap, fig_gates,
       fig_quarterly_volumes, fig_customer_journey, fig_channel_mix,
       fig_swot, fig_porter, fig_pestle, fig_moat, fig_school_ladder,
       fig_engine_economics, fig_deal_sizes, fig_pipeline,
       fig_university_ladder, fig_initiative_scale, fig_initiative_model,
       fig_competition_model, fig_subscription_sources, fig_cohort_ramp,
       fig_headcount, fig_gtm_moves, fig_institution_workflow,
       fig_bootcamp_map, fig_org_chart, fig_phases, fig_flywheel,
       fig_ngo_initiatives]


def build_all():
    return [f() for f in ALL]


if __name__ == "__main__":
    for p in build_all():
        print("wrote", os.path.basename(p))
