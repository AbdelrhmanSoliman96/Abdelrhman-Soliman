"""
The StartPad business model, on one page.

Built before the financial model rather than after it, so that what the model
counts and what the business actually does can be checked against each other
before any arithmetic is written.

Three pages:
    1  The business model canvas — the nine blocks
    2  The acquisition architecture — six buyer types, every channel, and the
       three-stage funnel that turns a click into a paid account
    3  Named programmes and activities, with their durations

Brand and drawing helpers come from business_plan/charts.py, so this is the
same visual system as the plan's figures.

    python scripts/build_business_model_canvas.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib                                              # noqa: E402
matplotlib.use("Agg")                                          # noqa: E402
import matplotlib.pyplot as plt                                # noqa: E402
from matplotlib.backends.backend_pdf import PdfPages           # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle       # noqa: E402

from business_plan import charts as C                          # noqa: E402
from business_plan import model as M                           # noqa: E402

A3_W, A3_H = 16.54, 11.69
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "output")

PAD = 0.14


def page(w=A3_W, h=A3_H):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig, ax


def title_bar(ax, w, y, title, subtitle, kicker=None):
    if kicker:
        ax.text(0.4, y + 0.92, kicker, fontsize=8.5, color=C.UV,
                fontweight="bold", va="bottom")
    ax.text(0.4, y + 0.40, title, fontsize=23, color=C.INK, fontweight="bold",
            va="bottom")
    ax.text(0.4, y + 0.12, subtitle, fontsize=9.5, color=C.MUTED, va="bottom")
    ax.add_patch(Rectangle((0.4, y + 0.02), w - 0.8, 0.022, color=C.UV,
                           zorder=3))


def _block_height(items, title, inner, title_size, body_size, note):
    """How tall this block's content actually is, at this body size."""
    h = 0.30 + C._lines_h(C._wrap(title, title_size, inner - 0.45, bold=True),
                          title_size) + 0.14
    for item in items:
        if isinstance(item, tuple):
            head, body = item
            h += C._lines_h(C._wrap(head, body_size, inner - 0.14, bold=True),
                            body_size) + 0.015
            h += C._lines_h(C._wrap(body, body_size - 0.5, inner - 0.14),
                            body_size - 0.5) + 0.085
        else:
            h += C._lines_h(C._wrap(item, body_size, inner - 0.16),
                            body_size) + 0.055
    if note:
        h += C._lines_h(C._wrap(note, body_size - 0.8, inner),
                        body_size - 0.8) + 0.14
    return h + 0.12


def block(ax, x, y, w, h, num, title, items, accent=C.UV, body_size=7.4,
          title_size=10.2, note=None):
    """
    One canvas block: a numbered heading and a list.

    The body size is reduced until the measured content fits the box. A canvas
    is a fixed grid, so a block that overflows lands on the heading of the one
    below it — which is exactly what happened before this measured.
    """
    inner = w - 2 * PAD
    while (body_size > 5.9
           and _block_height(items, title, inner, title_size, body_size, note)
           > h):
        body_size -= 0.15
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor=C.WASH, edgecolor="none", zorder=2))
    ax.add_patch(Rectangle((x, y + h - 0.10), w, 0.10, color=accent, zorder=3))
    inner = w - 2 * PAD
    ty = y + h - 0.30
    ax.text(x + PAD, ty, num, fontsize=7.2, color=accent, fontweight="bold",
            va="top", zorder=4)
    tl = C._wrap(title, title_size, inner - 0.45, bold=True)
    ax.text(x + PAD + 0.42, ty, "\n".join(tl), fontsize=title_size, color=C.INK,
            fontweight="bold", va="top", zorder=4, linespacing=1.28)
    yy = ty - C._lines_h(tl, title_size) - 0.14
    for item in items:
        if isinstance(item, tuple):
            head, body = item
            hl = C._wrap(head, body_size, inner - 0.14, bold=True)
            ax.add_patch(Rectangle((x + PAD, yy - C._lines_h(hl, body_size)
                                    - 0.012), 0.028,
                                   C._lines_h(hl, body_size) + 0.01,
                                   color=accent, zorder=4))
            ax.text(x + PAD + 0.10, yy, "\n".join(hl), fontsize=body_size,
                    color=C.INK, fontweight="bold", va="top", zorder=4,
                    linespacing=1.34)
            yy -= C._lines_h(hl, body_size) + 0.015
            bl = C._wrap(body, body_size - 0.5, inner - 0.14)
            ax.text(x + PAD + 0.10, yy, "\n".join(bl), fontsize=body_size - 0.5,
                    color=C.INK2, va="top", zorder=4, linespacing=1.38)
            yy -= C._lines_h(bl, body_size - 0.5) + 0.085
        else:
            bl = C._wrap(item, body_size, inner - 0.16)
            ax.text(x + PAD, yy, "·", fontsize=body_size, color=accent,
                    fontweight="bold", va="top", zorder=4)
            ax.text(x + PAD + 0.13, yy, "\n".join(bl), fontsize=body_size,
                    color=C.INK2, va="top", zorder=4, linespacing=1.38)
            yy -= C._lines_h(bl, body_size) + 0.055
    if note:
        nl = C._wrap(note, body_size - 0.8, inner)
        ax.text(x + PAD, y + 0.10 + C._lines_h(nl, body_size - 0.8),
                "\n".join(nl), fontsize=body_size - 0.8, color=C.MUTED,
                va="top", zorder=4, linespacing=1.38, style="italic")
    return yy


# =====================================================================
#  PAGE 1 — THE CANVAS
# =====================================================================
def page_canvas():
    fig, ax = page()
    title_bar(ax, A3_W, 10.45, "StartPad — Business Model Canvas",
              "Egypt and Saudi Arabia · the model the financial model is built "
              "to count · October 2026 onwards",
              "BEFORE THE NUMBERS")

    m = 0.4
    usable = A3_W - 2 * m
    gap = 0.11
    vp_w = 3.55
    col_w = (usable - 4 * gap - vp_w) / 4
    top_y, top_h = 3.42, 6.82
    bot_y, bot_h = 0.40, 2.90
    half = (top_h - gap) / 2

    xs = []
    x = m
    for i in range(5):
        xs.append(x)
        x += (vp_w if i == 2 else col_w) + gap

    # ---- 1 Key Partners
    block(ax, xs[0], top_y, col_w, top_h, "01", "Key Partners", [
        ("Certified delivery partners",
         "INJAZ Egypt, Misr El Kheir, Life Makers, regional training providers "
         "— they run cohorts under licence and keep 40% of the fee"),
        ("Youth and channel organisations",
         "Enactus Egypt, INJAZ, Hult Prize chapters, AIESEC — campus footprint "
         "StartPad will never build itself"),
        ("Government and initiative owners",
         "Rowad 2030, MSMEDA, ITIDA, Ministry of Technical Education · "
         "Monsha'at, TVTC, Misk, Hadaf"),
        ("Donors and international organisations",
         "ILO (Start and Improve Your Business), UNDP, GIZ, UNICEF, British "
         "Council, Drosos, Sawiris"),
        ("Competition sponsors",
         "Orange Egypt, ExxonMobil Egypt, National Bank of Egypt, Banque Misr, "
         "Central Bank FinYology"),
        ("Universities and incubators",
         "AUC Venture Lab, Nahdet El Mahrousa, university entrepreneurship "
         "centres"),
        ("Bought, not hired",
         "Accounting and legal firms, the Mission Zero freelance crew, the "
         "Arabic translation panel, safeguarding accreditation"),
    ], accent=C.UV)

    # ---- 2 Key Activities / Key Resources
    block(ax, xs[1], top_y + half + gap, col_w, half, "02", "Key Activities", [
        "Own the standard: curriculum in three variants, assessment, "
        "certification and audit",
        "Certify facilitators and partner organisations — then audit them "
        "every term",
        "Deliver cohorts through the certified network, not through employees",
        "Operate competitions: entry, qualification, mentor matching, judging",
        "Produce Mission Zero — three seasons a year, twelve episodes each",
        "Build the platform and the bilingual AI mentor",
        "Institutional business development across six buyer types",
        "Write bids, proposals and donor logframes",
    ], accent="#0071ED")

    block(ax, xs[1], top_y, col_w, half, "03", "Key Resources", [
        "The platform: 15 missions, AI co-founder, 121 mapped tools, admin "
        "workspace, per-participant evidence record",
        "Bilingual MENA curriculum — university, school and technical variants",
        "The certification standard and assessment, which is the defensible "
        "asset",
        "The certified facilitator pool and partner network",
        "Institutional relationships and the cohort evidence record",
        "The Mission Zero library and the annual readiness report",
        f"A capped team: {M.headcount()[1]['y1']} people in year one rising to "
        f"{M.headcount()[1]['y5']} in year five",
    ], accent="#0096DF")

    # ---- 4 Value Propositions
    block(ax, xs[2], top_y, vp_w, top_h, "04", "Value Propositions", [
        ("To the young person — a method, not advice",
         "Fifteen sequenced missions where the next one opens only when the "
         "last passes review. An AI co-founder inside every mission. Not a "
         "course: a path with a gate."),
        ("To the university or school — the outcome they are measured on",
         "Employability and entrepreneurship results they are accountable for "
         "and have no way to produce, delivered and evidenced, with a cohort "
         "report per student."),
        ("To the ministry or initiative — delivery capacity they do not own",
         "A published target of a million entrepreneurs needs a build stage "
         "and a per-participant record. Trainer certification is the only "
         "version of this that reaches national scale."),
        ("To the donor — indicators, not activities",
         "An evidence record their monitoring function accepts without "
         "re-work, mapped to the ILO methodology they already use."),
        ("To the sponsor — something to report",
         "A decade of funding competitions has produced attendance figures and "
         "photographs. We give a measurable outcome per participant and a "
         "report they can publish."),
        ("To the partner organisation — a standard to deliver under",
         "Curriculum, platform, certification and audit. They keep the "
         "relationship and the larger share of the fee."),
    ], accent=C.UV, body_size=7.8)

    # ---- 5 Customer Relationships / 6 Channels
    block(ax, xs[3], top_y + half + gap, col_w, half, "05",
          "Customer Relationships", [
        ("Land and expand",
         "Funded pilot → delivered cohort → faculty or school licence → "
         "renewal. The report, not the pitch, is the sales document."),
        ("Certified licence, with an audit that bites",
         "Partners are certified, sampled each term, and can lose the licence"),
        ("Named account management",
         "Renewals owned from year five; before that, by the signing head"),
        ("Community and standing",
         "Ambassadors earn status; founders appear on Mission Zero"),
        ("Resident in Saudi Arabia",
         "A country manager in Riyadh — the relationship precedes the product"),
    ], accent="#00C8B6")

    block(ax, xs[3], top_y, col_w, half, "06", "Channels", [
        ("Offline — these create sign-ups and leads",
         "Campus workshops · ambassador network · competitions · events and "
         "fairs · partner sessions · direct outreach by the heads"),
        ("Online — these create reach",
         "Short video (TikTok, Instagram, Facebook) · paid social · "
         "influencers and student creators · Mission Zero · webinars · SEO "
         "and content"),
        ("One destination",
         "Every channel lands on Mission 01. Activation is finishing it, not "
         "opening an account."),
        ("Institutional route",
         "Enter at the edge — one campus, one branch, one chapter — never at "
         "head office"),
    ], accent="#00D3A4")

    # ---- 7 Customer Segments
    block(ax, xs[4], top_y, col_w, top_h, "07", "Customer Segments", [
        ("WHO PAYS", ""),
        ("Universities and faculties",
         "Entrepreneurship centres, capstone coordinators, deans, student "
         "activities"),
        ("Schools and technical institutes",
         "Private, international and applied-technology schools; TVET colleges"),
        ("National initiatives and government",
         "Ministries, agencies and programme offices with published targets"),
        ("NGOs, donors and foundations",
         "With a youth employability or entrepreneurship mandate and a budget"),
        ("Competition sponsors and corporates",
         "Banks, telcos and CSR or innovation budget holders"),
        ("Incubators and accelerators",
         "Buying better-prepared applicants, per seat"),
        ("WHO USES IT", ""),
        ("First-time founders, 18-30",
         "Students and graduates with an idea or a graduation project"),
        ("Secondary and technical students, 15-18",
         "Reached through schools, never sold to directly"),
        ("Micro and small enterprise owners",
         "Reached through banks, NGOs and government programmes"),
    ], accent="#8FD92F", body_size=7.2)

    # ---- 8 Cost Structure / 9 Revenue Streams
    cost_w = (usable - gap) * 0.46
    rev_w = usable - gap - cost_w
    block(ax, m, bot_y, cost_w, bot_h, "08", "Cost Structure", [
        ("Direct — moves with every cohort and seat",
         "Facilitator fees (certified freelancers, never employees) · "
         "materials and showcases · seat provisioning, support and AI "
         "inference · competition and event delivery · programme delivery"),
        ("Revenue share — three counterparties",
         "Certified delivery partners on partner-delivered cohorts · youth and "
         "channel organisations on competitions and programme seats · "
         "aggregators and payment processing on initiative seats and "
         "subscriptions"),
        ("Indirect — does not move with a cohort",
         "Payroll for a capped team · offline and online marketing · Mission "
         "Zero production · rent and utilities · cloud and AI · travel · "
         "outsourced finance, legal and audit · safeguarding · partner "
         "enablement and audit · depreciation and amortisation"),
    ], accent="#C2185B", body_size=7.6)

    block(ax, m + cost_w + gap, bot_y, rev_w, bot_h, "09", "Revenue Streams", [
        ("Education", "University cohort programmes · faculty licences · "
                      "school cohorts · school licences · technical and "
                      "vocational cohorts · programme and incubator seats"),
        ("Public", "National initiative seats, priced per participant · "
                   "train-the-trainer certification, plus the per-seat licence "
                   "behind every certified trainer · NGO and donor programmes"),
        ("Commercial", "Sponsored competitions · corporate and CSR programmes · "
                       "Mission Zero season and episode sponsorship"),
        ("Direct", "Founder subscriptions — Pro and Team. The smallest line, "
                   "and a consequence of the other engines rather than a "
                   "channel of its own"),
    ], accent="#8FD92F", body_size=7.6,
        note="Somebody other than the beneficiary pays in every stream but the "
             "last. That asymmetry is the business model.")
    return fig


# =====================================================================
#  PAGE 2 — THE ACQUISITION ARCHITECTURE
# =====================================================================
DRIVERS = {
    "INSTITUTIONS":
        "Offline activity and inbound produce leads; three conversion stages with a four-month lag give contracts signed. Contracts x deliveries per contract = cohorts; cohorts x the year's price.",
    "SPONSORS":
        "Competition seasons a year x the season fee, plus Mission Zero seasons x the sponsorship fee. The driver is the number of sponsors won, never audience size.",
    "NGOs AND DONORS":
        "Proposals entered at design phase x win rate, lagged twelve to eighteen months. Programmes won x the programme fee, delivered across several sites.",
    "GOVERNMENT INITIATIVES":
        "Funded pilots open seat blocks: seats a quarter x price per seat. Then certification cohorts x fee, and the per-seat licence every certified trainer carries behind them.",
    "CSR AND CORPORATE":
        "Reference programmes produce annual budget lines; budget lines won x the programme fee, on the corporate budget calendar.",
    "B2C FOUNDERS":
        "Two sources, modelled apart: the reach the other five buyers have already paid for, and an online funnel of spend / CPC -> click -> lead -> account -> paid. Annual plans billed up front, recognised monthly, churned monthly.",
}


def page_acquisition():
    fig, ax = page()
    title_bar(ax, A3_W, 10.45, "Acquisition architecture",
              "Six buyer types, every channel offline and online, and the "
              "three-stage funnel each one runs through",
              "WHAT THE FINANCIAL MODEL WILL COUNT")
    m = 0.4
    usable = A3_W - 2 * m

    # ---------------- the three-stage funnel, across the top
    ax.text(m, 10.02, "THE FUNNEL — THREE STAGES, MEASURED SEPARATELY",
            fontsize=9, color=C.UV, fontweight="bold", va="top")
    stages = [
        ("SPEND", "Cost per click", "Budget by channel ÷ CPC = paid clicks. "
         "Organic and referral traffic are then taken as a stated percentage "
         "of paid, never assumed free."),
        ("STAGE 1", "Click → lead", "A click becomes a lead: an identified "
         "person or institution. Rate differs by channel — a webinar "
         "registrant is not a video view."),
        ("STAGE 2", "Lead → registered account",
         "A lead opens an account on the platform. For institutions this is "
         "the meeting-to-proposal step instead."),
        ("STAGE 3", "Registered → paid",
         "The account converts: a subscription for a founder, a signed "
         "contract for an institution, a seat order for a funder."),
    ]
    sw = (usable - 3 * 0.12) / 4
    for i, (tag, head, body) in enumerate(stages):
        x = m + i * (sw + 0.12)
        fillc = C.spec(i, 4)
        ink, sub = C._ink_for(fillc)
        ax.add_patch(FancyBboxPatch((x, 8.52), sw, 1.34,
                                    boxstyle="round,pad=0,rounding_size=0.06",
                                    facecolor=C.WASH, edgecolor="none",
                                    zorder=2))
        ax.add_patch(FancyBboxPatch((x, 9.34), sw, 0.52,
                                    boxstyle="round,pad=0,rounding_size=0.06",
                                    facecolor=fillc, edgecolor="none", zorder=3))
        ax.add_patch(Rectangle((x, 9.34), sw, 0.1, color=fillc, zorder=3))
        ax.text(x + PAD, 9.80, tag, fontsize=7, color=sub, fontweight="bold",
                va="top", zorder=4)
        ax.text(x + PAD, 9.66, head, fontsize=10.5, color=ink,
                fontweight="bold", va="top", zorder=4)
        bl = C._wrap(body, 7.4, sw - 2 * PAD)
        ax.text(x + PAD, 9.22, "\n".join(bl), fontsize=7.4, color=C.INK2,
                va="top", zorder=4, linespacing=1.4)
        if i < 3:
            C._arrow(ax, x + sw + 0.01, 9.60, x + sw + 0.11, 9.60)

    # ---------------- buyer types and their channels
    ax.text(m, 8.22, "SIX BUYER TYPES — EACH WITH ITS OWN CHANNELS, CYCLE AND "
            "UNIT", fontsize=9, color=C.UV, fontweight="bold", va="top")
    buyers = [
        ("INSTITUTIONS", "Universities, schools, technical institutes",
         "Campus workshops · direct outreach by the heads · events and "
         "conferences · ambassador intelligence · inbound from content",
         "Lead → first meeting → proposal or funded pilot → signed contract",
         "Sold per cohort, then per faculty or school licence",
         "4-month cycle"),
        ("SPONSORS", "Banks, telcos, corporates funding competitions",
         "Competition organisers introduce them · direct outreach · the "
         "annual readiness report · LinkedIn and the decision-maker cut of "
         "Mission Zero",
         "Lead → brief → season proposal → sponsorship contract",
         "Sold per competition season, and per Mission Zero season",
         "3-5 month cycle, annual calendar"),
        ("NGOs AND DONORS", "Foundations, INGOs, development agencies",
         "Partner sessions inside their cohorts · donor events · "
         "the ILO methodology mapping · existing grantees",
         "Design-phase conversation → named in the proposal → grant awarded → "
         "delivery",
         "Sold as a programme, against a logframe",
         "12-18 months, must start early"),
        ("GOVERNMENT INITIATIVES", "Ministries, agencies, national programmes",
         "Enter through one university, one governorate branch or one "
         "patronised competition — never head office",
         "Funded pilot → cohort report → priced seat block → trainer "
         "certification",
         "Sold per seat, then per certified trainer",
         "9-15 months"),
        ("CSR AND CORPORATE", "Innovation and CSR budget holders",
         "A reference programme a committee can circulate · sponsor "
         "relationships · corporate volunteer networks",
         "Lead → case study → CSR committee → annual budget line",
         "Sold as a custom programme",
         "Annual budget cycle"),
        ("B2C FOUNDERS", "Students, graduates, micro-enterprise owners",
         "Short video · paid social · influencers · Mission Zero · webinars · "
         "SEO — and, far more productively, the cohorts, seats and "
         "competitions the other five buyers pay for",
         "Click → free account → Mission 01 activation → Pro or Team",
         "Sold per subscription, annual plan",
         "Days, not months"),
    ]
    bw = (usable - 2 * 0.12) / 3
    bh = 3.46
    for i, (name, who, chans, funnel, unit, cycle) in enumerate(buyers):
        x = m + (i % 3) * (bw + 0.12)
        y = 4.42 - (i // 3) * (bh + 0.16)
        accent = C.spec(i, 6)
        ax.add_patch(FancyBboxPatch((x, y), bw, bh,
                                    boxstyle="round,pad=0,rounding_size=0.06",
                                    facecolor=C.WASH, edgecolor="none",
                                    zorder=2))
        ax.add_patch(Rectangle((x, y + bh - 0.10), bw, 0.10, color=accent,
                               zorder=3))
        yy = y + bh - 0.30
        ax.text(x + PAD, yy, name, fontsize=10.6, color=C.INK,
                fontweight="bold", va="top", zorder=4)
        yy -= 0.235
        wl = C._wrap(who, 7.4, bw - 2 * PAD)
        ax.text(x + PAD, yy, "\n".join(wl), fontsize=7.4, color=accent,
                va="top", zorder=4, linespacing=1.36)
        yy -= C._lines_h(wl, 7.4) + 0.12
        for lab, txt in (("CHANNELS", chans), ("FUNNEL", funnel),
                         ("UNIT SOLD", unit), ("MODEL DRIVER", DRIVERS[name])):
            ax.text(x + PAD, yy, lab, fontsize=6.3, color=C.UV,
                    fontweight="bold", va="top", zorder=4)
            yy -= 0.145
            tl = C._wrap(txt, 7.3, bw - 2 * PAD)
            ax.text(x + PAD, yy, "\n".join(tl), fontsize=7.3, color=C.INK2,
                    va="top", zorder=4, linespacing=1.38)
            yy -= C._lines_h(tl, 7.3) + 0.085
        ax.add_patch(FancyBboxPatch((x + PAD, y + 0.12), bw - 2 * PAD, 0.30,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=accent, edgecolor="none",
                                    zorder=3))
        ink, _ = C._ink_for(accent)
        ax.text(x + bw / 2, y + 0.27, cycle, fontsize=7.6, color=ink,
                fontweight="bold", ha="center", va="center", zorder=4)

    note = ("Every stream but the last is paid for by somebody other than the "
            "person who benefits. The financial model therefore drives B2C "
            "subscriptions from the reach the other five buyers have already "
            "paid for, plus an online funnel of its own — never from a "
            "standalone consumer budget.")
    nl = C._wrap(note, 8.4, usable)
    ax.text(m, 0.52, "\n".join(nl), fontsize=8.4, color=C.MUTED, va="top",
            linespacing=1.45, style="italic")
    return fig


def table(ax, x, y_top, w, heads, widths, rows, accent=C.UV, size=7.4,
          head_size=7.2):
    """A measured table: row heights come from the wrapped text, not a guess."""
    cols = [w * f for f in widths]
    xs, cx = [], x
    for cw in cols:
        xs.append(cx)
        cx += cw
    y = y_top
    ax.add_patch(Rectangle((x, y - 0.26), w, 0.26, color=accent, zorder=3))
    for i, h in enumerate(heads):
        ax.text(xs[i] + 0.09, y - 0.09, h, fontsize=head_size,
                color=C._ink_for(accent)[0], fontweight="bold", va="top",
                zorder=4)
    y -= 0.26
    for ri, row in enumerate(rows):
        wrapped = [C._wrap(str(cell), size, cols[i] - 0.18,
                           bold=(i == 0)) for i, cell in enumerate(row)]
        h = max(C._lines_h(wl, size) for wl in wrapped) + 0.13
        if ri % 2 == 0:
            ax.add_patch(Rectangle((x, y - h), w, h, color=C.WASH, zorder=2))
        for i, wl in enumerate(wrapped):
            ax.text(xs[i] + 0.09, y - 0.065, "\n".join(wl), fontsize=size,
                    color=C.INK if i == 0 else C.INK2,
                    fontweight="bold" if i == 0 else "normal",
                    va="top", zorder=4, linespacing=1.36)
        y -= h
    return y


# =====================================================================
#  PAGE 3 — NAMED PROGRAMMES AND ACTIVITIES, WITH DURATIONS
# =====================================================================
ACTIVITIES = [
    ("University cohort", "6 delivery days across 2 weeks; report issued "
     "within 5 working days", "Per cohort of 25", "Engine 1"),
    ("School cohort", "4 delivery days across 2 weeks", "Per cohort of 30",
     "Engine 2"),
    ("Technical and vocational cohort", "5 delivery days across 2 weeks",
     "Per cohort of 30", "Engine 2"),
    ("Faculty licence", "12 months, renewable", "Per faculty, per year",
     "Engine 1"),
    ("School licence", "12 months, renewable", "Per school, per year",
     "Engine 2"),
    ("National initiative seat block", "12-month seat licence per participant; "
     "provisioned in tranches", "Per seat", "Engine 3"),
    ("Train-the-trainer certification", "5-day certification plus one "
     "supervised delivery — about one quarter", "Per certification cohort, "
     "plus a per-seat licence behind every trainer", "Engine 3"),
    ("NGO or donor programme", "6 to 9 months, usually several sites",
     "Per programme, against a logframe", "Engine 4"),
    ("Sponsored competition season", "3 to 5 months: entry, campus rounds, a "
     "build cohort between rounds, then the final", "Per season, paid by the "
     "sponsor", "Engine 5"),
    ("Corporate or CSR programme", "3 to 6 months", "Per programme",
     "Engine 6"),
    ("Programme and incubator seats", "12-month partner agreement, seats drawn "
     "per intake", "Per seat", "Engine 7"),
    ("Mission Zero season", "12 episodes over about 16 weeks; three seasons a "
     "year", "Per season or per episode, to a sponsor", "Engine 5 / demand"),
    ("Founder subscription", "Annual plan, billed in advance, recognised "
     "monthly", "Per account — Pro or Team", "Engine 8"),
    ("Facilitator certification", "Observe, co-deliver, then one scored "
     "supervised delivery; recertified each term", "A cost, not a revenue line",
     "Capacity"),
    ("Partner organisation certification", "A certification cohort plus one "
     "supervised delivery — about a quarter; audited on sample each term",
     "A cost, and the licence that follows", "Capacity"),
    ("Campus ambassador term", "One academic term; roughly 7 active months a "
     "year", "A stipend, not a salary", "Demand"),
    ("Annual readiness report", "Published once a year, with a quarterly data "
     "note", "A cost that opens institutional doors", "Demand"),
]

PROGRAMMES = [
    ("Rowad 2030 — One Million Entrepreneurs", "Egypt",
     "Ministry of Planning and Economic Development. A three-stage online "
     "curriculum with the Rowad Meter data platform; universities including "
     "Alexandria have signed protocols funding seats.", "Running to 2030",
     "Seats, then trainer certification"),
    ("MSMEDA governorate programme", "Egypt",
     "Micro, Small and Medium Enterprise Development Agency — service centres "
     "across the governorates.", "Continuous", "Seats and certification"),
    ("ITIDA and the Ministry of Communications", "Egypt",
     "National digital-skills and youth-innovation programmes; patron of "
     "Startup Teen.", "Annual cycles", "Seats"),
    ("Central Bank of Egypt — FinYology", "Egypt",
     "More than thirty Egyptian universities; FinTech Got Talent is its annual "
     "showcase, now in its third edition.", "Annual, academic year",
     "Build cohorts, then the season"),
    ("Applied technology schools reform", "Egypt",
     "Ministry of Technical Education and Training — technical secondary "
     "schools converting, with employer partners.", "Multi-year",
     "Cohorts, then trainer certification"),
    ("Enactus Egypt National Competition", "Egypt",
     "Thirty to thirty-five university teams reach the national final. Orange "
     "Egypt has sponsored it for seventeen consecutive years; ExxonMobil Egypt "
     "is a long-standing supporter.", "Annual season, 4-5 months",
     "Platform and build cohorts"),
    ("INJAZ Egypt — Company Program", "Egypt and the Arab region",
     "A six-month student venture programme with school and university tracks, "
     "ending in the Youth Entrepreneurship Celebration, now in its nineteenth "
     "edition and feeding INJAZ Al-Arab.", "6 months per cycle",
     "Delivery partner licence"),
    ("Startup Teen (iSchool)", "Egypt",
     "Ages 13 to 18, combining entrepreneurship with AI. First edition: 800+ "
     "students from 40 schools in 140 teams, under MCIT patronage.",
     "Annual season", "School-variant training track"),
    ("Egypt Entrepreneurship Rally", "Egypt",
     "Run with AASTMT and sponsored by the National Bank of Egypt since 2019.",
     "Annual", "Platform and the sponsor's report"),
    ("Rowad Domiat", "Egypt",
     "Governorate competition run by the ILO with ICSB, backed by Methanex "
     "Egypt, built on the ILO Start and Improve Your Business methodology.",
     "Annual", "Platform, and the ILO mapping"),
    ("Hult Prize on-campus programme", "Egypt and KSA",
     "Student competition run through university chapters, campus rounds "
     "feeding regional finals.", "Annual, campus round 6-10 weeks",
     "Campus round as a cohort"),
    ("Monsha'at Academy", "KSA",
     "The SME authority's online academy — more than two hundred training "
     "events across planning, finance, marketing, e-commerce and franchising, "
     "with no build stage after them.", "Continuous catalogue",
     "Capstone cohorts, then seats"),
    ("Misk Foundation and the MISK SDG Innovation Competition", "KSA",
     "Youth education and entrepreneurship since 2011; the SDG competition is "
     "run with UNDP.", "Annual", "Cohorts, platform, programmes"),
    ("TVTC", "KSA",
     "336,150 trainees across 314 institutions in 2024, under a Vision 2030 "
     "mandate connecting training to self-employment.", "Academic year",
     "Trainer certification at scale"),
    ("Hadaf and the Social Development Bank", "KSA",
     "Subsidised training and finance for job-seekers and micro-enterprise "
     "owners, with per-beneficiary funding already in place.", "Continuous",
     "Seat rider, as a screening instrument"),
    ("Entrepreneurship World Cup — Saudi round", "KSA",
     "Global competition with a national Saudi round reaching students and "
     "early-stage founders.", "Annual", "Build track and qualification"),
]


def page_activities():
    fig, ax = page()
    title_bar(ax, A3_W, 10.45, "Activity catalogue",
              "What is actually sold, how long each one runs, and which engine "
              "it feeds",
              "WHAT THE FINANCIAL MODEL WILL SCHEDULE")
    m = 0.4
    usable = A3_W - 2 * m
    table(ax, m, 10.08, usable,
          ["Activity", "Duration", "How it is sold", "Engine"],
          [0.22, 0.33, 0.33, 0.12], ACTIVITIES, accent=C.UV, size=8.2,
          head_size=8.0)
    note = ("Duration matters because it decides when cash arrives, not only "
            "when work happens. A donor programme contracted in one quarter is "
            "delivered across the next three; a competition season is bought "
            "once a year or not at all; an annual subscription is collected up "
            "front and earned a month at a time. The financial model schedules "
            "each of these on its own clock rather than spreading everything "
            "evenly.")
    nl = C._wrap(note, 8.6, usable)
    ax.text(m, 1.30, "\n".join(nl), fontsize=8.6, color=C.MUTED, va="top",
            linespacing=1.5, style="italic")
    return fig


def page_programmes():
    fig, ax = page()
    title_bar(ax, A3_W, 10.45, "Named programmes",
              "The real programmes each engine attaches to — targets, not "
              "signed partners, and no revenue is attributed to any one of them",
              "WHERE THE DEMAND ALREADY EXISTS")
    m = 0.4
    usable = A3_W - 2 * m
    table(ax, m, 10.08, usable,
          ["Programme", "Market", "What it already runs", "Cadence",
           "What StartPad supplies"],
          [0.19, 0.09, 0.37, 0.14, 0.21], PROGRAMMES, accent="#0096DF",
          size=8.0, head_size=8.0)
    note = ("The common shape is worth naming: every one of these has a target "
            "or a mandate it cannot meet with the delivery capacity it owns. "
            "That gap — between a published commitment and the means to "
            "deliver it — is the demand this model counts.")
    nl = C._wrap(note, 8.6, usable)
    ax.text(m, 1.05, "\n".join(nl), fontsize=8.6, color=C.MUTED, va="top",
            linespacing=1.5, style="italic")
    return fig


def build():
    os.makedirs(OUT, exist_ok=True)
    pages = [page_canvas(), page_acquisition(), page_activities(),
             page_programmes()]
    pdf_path = os.path.join(OUT, "StartPad_Business_Model_Canvas.pdf")
    with PdfPages(pdf_path) as pdf:
        for f in pages:
            pdf.savefig(f, dpi=200)
    names = ["canvas", "acquisition", "activities", "programmes"]
    pngs = []
    for f, n in zip(pages, names):
        p = os.path.join(OUT, f"StartPad_BMC_{n}.png")
        f.savefig(p, dpi=150)
        pngs.append(p)
        plt.close(f)
    return pdf_path, pngs


if __name__ == "__main__":
    pdf, pngs = build()
    print("wrote", pdf)
    for p in pngs:
        print("wrote", p)
