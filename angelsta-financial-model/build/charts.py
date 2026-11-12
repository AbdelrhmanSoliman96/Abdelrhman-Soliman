"""Charts and infographics for the pricing strategy and the competitor report. Usage: python charts.py model.xlsx outdir"""
import os
import sys
import json
import openpyxl
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import params as P
import competitors as C

TEAL, DEEP, MINT, SAND, GREY, RED, GOLD = "#0E5A5F", "#0D2B30", "#7FB7AA", "#D9CBB0", "#8A939C", "#C0504D", "#C9A227"
PAL = [DEEP, TEAL, MINT, "#3E8E7E", SAND, GOLD, "#5B7C99", "#A3C4BC", "#B5651D", GREY]
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#B0B7BE", "axes.titleweight": "bold", "axes.titlesize": 11, "axes.titlecolor": DEEP,
                     "savefig.dpi": 200, "savefig.bbox": "tight", "text.parse_math": False})

model, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
wb = openpyxl.load_workbook(model, data_only=True)
YRS = ["2027", "2028", "2029", "2030", "2031"]
YCOL = [2, 15, 28, 41, 54]


def row(sheet, startswith, cols=YCOL):
    ws = wb[sheet]
    for r in ws.iter_rows(min_row=1, max_row=ws.max_row):
        v = r[0].value
        if isinstance(v, str) and v.strip().startswith(startswith):
            return [ws.cell(r[0].row, c).value or 0 for c in cols]
    raise KeyError(startswith)


def fixlog(fig):
    fmt = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}")
    for ax in fig.axes:
        for axis, sc in [(ax.xaxis, ax.get_xscale()), (ax.yaxis, ax.get_yscale())]:
            if sc == "log":
                axis.set_major_formatter(fmt)
                axis.set_minor_formatter(matplotlib.ticker.NullFormatter())


def place_labels(ax, pts, fontsize=7.5, bold=(), colors=None):
    """Greedy label placement. pts: list of (x, y, label, marker_size_pts). No overlaps between labels, markers or the frame."""
    fig = ax.figure
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    trans = ax.transData
    axbox = ax.get_window_extent(rend)
    marker_boxes = []
    for x, y, lab, s in pts:
        px, py = trans.transform((x, y))
        r = (s ** 0.5) / 2 * fig.dpi / 72 * 1.05
        marker_boxes.append(matplotlib.transforms.Bbox([[px - r, py - r], [px + r, py + r]]))
    placed = []
    cands = [(7, 3, "left"), (7, -11, "left"), (-7, 3, "right"), (-7, -11, "right"), (0, 9, "center"), (0, -16, "center"),
             (12, 12, "left"), (12, -20, "left"), (-12, 12, "right"), (-12, -20, "right"), (22, 2, "left"), (-22, 2, "right"),
             (0, 22, "center"), (0, -28, "center"), (26, 22, "left"), (-26, 22, "right"), (26, -30, "left"), (-26, -30, "right"),
             (40, 6, "left"), (-40, 6, "right"), (0, 36, "center"), (0, -40, "center")]
    order = sorted(range(len(pts)), key=lambda i: (-pts[i][3], -pts[i][1]))
    for i in order:
        x, y, lab, s = pts[i]
        best, best_score = None, None
        for dx, dy, ha in cands:
            t = ax.annotate(lab, (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, fontsize=fontsize,
                            fontweight="bold" if lab in bold else "normal", color=(colors or {}).get(lab, DEEP), zorder=5)
            bb = t.get_window_extent(rend).expanded(1.04, 1.12)
            score = sum(bb.overlaps(p) for p in placed) * 10 + sum(bb.overlaps(mb) for j, mb in enumerate(marker_boxes) if j != i) * 3
            if bb.x0 < axbox.x0 or bb.x1 > axbox.x1 or bb.y0 < axbox.y0 or bb.y1 > axbox.y1:
                score += 50
            if best_score is None or score < best_score:
                if best is not None:
                    best[0].remove()
                best, best_score = (t, bb, dx, dy), score
            else:
                t.remove()
            if score == 0:
                break
        t, bb, dx, dy = best
        if abs(dx) > 14 or abs(dy) > 18:
            t.arrow_patch = None
            ax.annotate("", (x, y), xytext=(dx, dy + 3), textcoords="offset points", arrowprops=dict(arrowstyle="-", color=GREY, lw=0.5), zorder=4)
        placed.append(bb)


def save(fig, name):
    fixlog(fig)
    fig.savefig(os.path.join(OUT, name))
    plt.close(fig)


def money(v):
    return f"${v / 1e6:.1f}m" if abs(v) >= 1e6 else f"${v / 1e3:.0f}k"


# ---------------------------------------------------------------- data from the model
D = {}
D["rev"] = row("Total Revenue", "Total revenue")
D["arr"] = row("Total Revenue", "Annual recurring revenue")
for k, lab in [("pro", "Pro"), ("team", "Team"), ("ang", "Angel"), ("inst", "Institutional, base"), ("ix", "Institutional, extra"), ]:
    D[k] = row("Total Revenue", lab)
ws = wb["Total Revenue"]
customs = [r[0].row for r in ws.iter_rows() if isinstance(r[0].value, str) and r[0].value.strip() == "Custom"]
D["sc"] = [ws.cell(customs[0], c).value or 0 for c in YCOL]
D["ic"] = [ws.cell(customs[1], c).value or 0 for c in YCOL]
D["geo"] = {lab: row("Revenue Streams", f"Subscription revenue, {lab}") for _, lab, *_ in P.GEO}
D["ebitda"] = row("Income Statement", "EBITDA", cols=[3, 4, 5, 6, 7])
D["cash"] = row("Financial Indicators", "Cash at year end", cols=[3, 4, 5, 6, 7])
D["paid"] = row("Financial Indicators", "Paying accounts at year end", cols=[3, 4, 5, 6, 7])
D["regs"] = row("Acquisitions", "New registrations, founders and investors")
D["fact"] = row("Acquisitions", "Newly activated founder workspaces")
D["iact"] = row("Acquisitions", "Newly activated investor accounts")
D["newp"] = row("Acquisitions", "New paying accounts")
fu = wb["Funding and Use of Funds"]
for r in fu.iter_rows():
    v = r[0].value
    if isinstance(v, str):
        for key, txt in [("ask", "THE PRE-SEED ASK"), ("seed", "SEED ROUND, sized"), ("y1", "Total cash required in year one")]:
            if v.startswith(txt):
                D[key] = fu.cell(r[0].row, 3).value
        for key, txt in [("u_mkt", "Marketing and community"), ("u_sales", "Sales and customer success"), ("u_prod", "Product and AI engineering"), ("u_ai", "AI agents, cloud and delivery"), ("u_ops", "Leadership, operations, legal")]:
            if v.startswith(txt):
                D[key] = fu.cell(r[0].row, 5).value
va = wb["Valuation"]
for r in va.iter_rows():
    v = r[0].value
    if isinstance(v, str) and v.startswith("Pre money valuation we are asking"):
        D["pre"] = va.cell(r[0].row, 3).value
    if isinstance(v, str) and v.startswith("Equity the pre-seed buys"):
        D["own"] = va.cell(r[0].row, 3).value
json.dump(D, open(os.path.join(OUT, "model_numbers.json"), "w"), indent=1, default=float)

# ================================================================ PRICING CHARTS
# p1 price ladder
fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
for ax, (side, d) in zip(axes, [("Founders, per company", P.STARTUP), ("Investors, per account", P.INVESTOR)]):
    tiers = list(d.keys())
    mo = [d[t]["monthly"][0] for t in tiers]
    an = [d[t]["annual"][0] for t in tiers]
    x = np.arange(len(tiers))
    b1 = ax.bar(x - 0.2, mo, 0.4, color=MINT, label="Monthly plan")
    b2 = ax.bar(x + 0.2, an, 0.4, color=DEEP, label="Annual plan, per month")
    for b in list(b1) + list(b2):
        if b.get_height() > 0:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height(), f"${b.get_height():,.0f}", ha="center", va="bottom", fontsize=7.5)
    ax.set_xticks(x, [t if t != "Custom" else "Custom, from" for t in tiers])
    ax.set_title(side)
    ax.set_ylabel("USD per month")
    ax.legend(frameon=False, fontsize=8)
fig.suptitle("Angelsta price list: every plan monthly or annual, annual saves about 17 per cent", fontsize=11, color=DEEP, fontweight="bold")
save(fig, "p1_price_ladder.png")

# p2 annual savings
fig, ax = plt.subplots(figsize=(8, 3))
names, sav = [], []
for side, d in [("Founder", P.STARTUP), ("Investor", P.INVESTOR)]:
    for t, v in d.items():
        if t == "Free":
            continue
        names.append(f"{side} {t}")
        sav.append((v["monthly"][0] - v["annual"][0]) * 12)
bars = ax.barh(names, sav, color=[TEAL if "Founder" in n else DEEP for n in names])
for b, s in zip(bars, sav):
    ax.text(b.get_width(), b.get_y() + b.get_height() / 2, f"  ${s:,.0f} a year", va="center", fontsize=8)
ax.invert_yaxis()
ax.set_xlabel("Saving from choosing the annual plan, USD per year")
ax.set_title("What the annual plan saves each customer")
save(fig, "p2_annual_savings.png")


# p3 / p4 competitor price comparison
def price_bar(side, fname, title, log=False):
    items = sorted([(k, v[0]) for k, v in C.PRICE.items() if v[1] == side], key=lambda t: t[1])
    fig, ax = plt.subplots(figsize=(8, 0.32 * len(items) + 1))
    cols = [GOLD if k.startswith("Angelsta") else (TEAL if side == "Founder" else DEEP) for k, _ in items]
    bars = ax.barh([k for k, _ in items], [v for _, v in items], color=cols)
    for b, (k, v) in zip(bars, items):
        ax.text(b.get_width(), b.get_y() + b.get_height() / 2, f" ${v:,.0f}", va="center", fontsize=7.5)
    if log:
        ax.set_xscale("log")
    ax.set_xlabel("Entry paid plan, USD per month (annual billing where offered)")
    ax.set_title(title)
    save(fig, fname)


price_bar("Founder", "p3_founder_prices.png", "Founder side: entry price of paid plans, Angelsta in gold")
price_bar("Investor", "p4_investor_prices.png", "Investor side: entry price of paid plans, log scale, Angelsta in gold", log=True)

# p5 value map
fig, ax = plt.subplots(figsize=(10, 5.6))
pts, cols = [], {}
for pname, cname in C.PRICE_COVER.items():
    price = C.PRICE[pname][0]
    tot = C.coverage_score(C.COVER[cname][6])[2]
    is_a = pname.startswith("Angelsta")
    size = 190 if is_a else 80
    ax.scatter(tot, price, s=size, color=GOLD if is_a else (TEAL if C.PRICE[pname][1] == "Founder" else DEEP), edgecolor="white", zorder=3)
    pts.append((tot, price, pname, size))
    if is_a:
        cols[pname] = "#7a5c00"
ax.set_yscale("log")
ax.set_xlim(0.5, 12.2)
ax.set_ylim(15, 3000)
place_labels(ax, pts, fontsize=8, bold={"Angelsta Pro", "Angelsta Institutional"}, colors=cols)
ax.set_yscale("log")
ax.set_xlabel("Modules covered, of 11 (full = 1, partial = 0.5)")
ax.set_ylabel("Entry price, USD per month, log scale")
ax.set_title("Value map: more of the workflow for less, Angelsta sits bottom right")
ax.axvline(5.5, color=GREY, lw=0.6, ls="--")
ax.text(5.6, 2200, "covers both sides", fontsize=8, color=GREY)
ax.legend(handles=[plt.Line2D([], [], marker="o", ls="", color=TEAL, label="Founder side product"), plt.Line2D([], [], marker="o", ls="", color=DEEP, label="Investor side product"),
                   plt.Line2D([], [], marker="o", ls="", color=GOLD, label="Angelsta")], frameon=False, fontsize=8, loc="upper right")
save(fig, "p5_value_map.png")

# p6 regional effective prices
fig, ax = plt.subplots(figsize=(8, 3.4))
mk = ["Egypt", "Qatar", "Saudi Arabia", "UAE", "Kuwait, Bahrain,\nOman", "Rest of MENA\nand Africa", "Rest of world"]
idx = [g[3] for g in P.GEO]
pro = [P.STARTUP["Pro"]["annual"][0] * i for i in idx]
inst = [P.INVESTOR["Institutional"]["annual"][0] * i for i in idx]
x = np.arange(len(mk))
ax2 = ax.twinx()
b1 = ax.bar(x - 0.2, pro, 0.4, color=MINT, label="Founder Pro, annual, USD per month")
b2 = ax2.bar(x + 0.2, inst, 0.4, color=DEEP, label="Investor Institutional, annual, USD per month")
for b, v in zip(b1, pro):
    ax.text(b.get_x() + b.get_width() / 2, v, f"${v:.0f}", ha="center", va="bottom", fontsize=7)
for b, v in zip(b2, inst):
    ax2.text(b.get_x() + b.get_width() / 2, v, f"${v:.0f}", ha="center", va="bottom", fontsize=7, color=DEEP)
ax.set_xticks(x, mk, rotation=15, fontsize=8)
ax.set_ylabel("Pro, USD")
ax2.set_ylabel("Institutional, USD")
ax2.spines["right"].set_visible(True)
ax.set_title("Price by market: Egypt list at 60 per cent, rest of MENA and Africa at 70 per cent")
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.set_ylim(0, max(pro) * 1.3)
ax2.set_ylim(0, max(inst) * 1.3)
ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=2)
save(fig, "p6_regional_prices.png")

# p7 revenue by plan
fig, ax = plt.subplots(figsize=(8, 3.8))
series = [("Founder Pro", D["pro"], MINT), ("Founder Team", D["team"], "#3E8E7E"), ("Founder Custom", D["sc"], TEAL),
          ("Investor Angel", D["ang"], SAND), ("Investor Institutional", [a + b for a, b in zip(D["inst"], D["ix"])], DEEP), ("Investor Custom", D["ic"], GOLD)]
bottom = np.zeros(5)
for nm, vals, col in series:
    ax.bar(YRS, vals, bottom=bottom, color=col, label=nm)
    bottom += np.array(vals)
for i, tot in enumerate(bottom):
    ax.text(i, tot, money(tot), ha="center", va="bottom", fontsize=8, fontweight="bold")
ax.set_ylabel("Revenue, USD")
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: money(v)))
ax.legend(frameon=False, fontsize=7.5, ncol=3, loc="upper left")
ax.set_title("Revenue by plan from the financial model, base case")
save(fig, "p7_revenue_by_plan.png")

# p8 revenue by geography
fig, ax = plt.subplots(figsize=(8, 3.8))
bottom = np.zeros(5)
for (lab, vals), col in zip(D["geo"].items(), PAL):
    short = {"Egypt": "Egypt", "Qatar": "Qatar", "Saudi Arabia": "Saudi Arabia", "United Arab Emirates": "UAE", "Kuwait": "Kuwait, Bahrain, Oman", "Rest of MENA and Africa": "Rest of MENA and Africa", "Rest of the world": "Rest of world"}
    ax.bar(YRS, vals, bottom=bottom, color=col, label=short.get(lab.split(",")[0], lab))
    bottom += np.array(vals)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: money(v)))
ax.legend(frameon=False, fontsize=7.5, ncol=4, loc="upper left")
ax.set_title("Subscription revenue by market: Egypt first, then Qatar, then the GCC, plus self serve worldwide")
save(fig, "p8_revenue_by_market.png")

# p9 unit economics
fig, ax = plt.subplots(figsize=(8, 3))
plans = [("Founder Pro", 0.75 * 59 + 0.25 * 49, P.AI_USE["S-Pro"], 0), ("Founder Team", 0.65 * 149 + 0.35 * 124, P.AI_USE["S-Team"], 0),
         ("Investor Angel", 0.75 * 79 + 0.25 * 65, P.AI_USE["I-Angel"], 0), ("Investor Institutional", 0.3 * 599 + 0.7 * 499, P.AI_USE["I-Inst"], 25)]
names = [p[0] for p in plans]
cost = [p[2] * P.AI_COST_PER_CREDIT[0] + 2.7 + p[3] + p[1] * 0.029 for p in plans]
price = [p[1] for p in plans]
gm = [1 - c / pr for c, pr in zip(cost, price)]
ax.barh(names, price, color=MINT, label="Effective price")
ax.barh(names, cost, color=RED, label="Cost to serve")
for i, (pr, g) in enumerate(zip(price, gm)):
    ax.text(pr, i, f"  ${pr:,.0f}, gross margin {g:.0%}", va="center", fontsize=8)
ax.invert_yaxis()
ax.set_xlim(0, max(price) * 1.45)
ax.set_xlabel("USD per account per month, 2027")
ax.legend(frameon=False, fontsize=8, loc="lower right")
ax.set_title("Unit economics by plan: AI inference, hosting, support and payments")
save(fig, "p9_unit_economics.png")


# infographic helpers
def box(ax, x, y, w, h, text, fc, tc="white", fs=8.5, bold=True):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec="none"))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=tc, fontsize=fs, fontweight="bold" if bold else "normal", wrap=True)


def arrow(ax, x1, y1, x2, y2, col=GREY):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=col, lw=1.4))


# p10 upgrade ladders
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4.4)
ax.axis("off")
lad = [("FOUNDERS", 2.6, [("Free", "$0\nset up, 15 stakeholders", MINT, DEEP), ("Pro", "$59 or $49\nopening a round", "#3E8E7E", "white"),
                          ("Team", "$149 or $124\nfunded, reporting", TEAL, "white"), ("Custom", "from $479 or $399\ngroups, SSO", DEEP, "white")]),
       ("INVESTORS", 0.35, [("Free", "$0\n5 holdings", MINT, DEEP), ("Angel", "$79 or $65\n40 holdings", SAND, DEEP),
                            ("Institutional", "$599 or $499\n5 seats, 50 companies", TEAL, "white"), ("Custom", "from $1,799 or $1,499\nmulti fund, LP portal", DEEP, "white")])]
for side, y, steps in lad:
    ax.text(0.05, y + 1.35, side, fontsize=10, fontweight="bold", color=DEEP)
    for i, (nm, sub, fc, tc) in enumerate(steps):
        x = 0.1 + i * 2.5
        box(ax, x, y, 2.1, 1.15, f"{nm}\n{sub}", fc, tc, fs=8.3)
        if i < 3:
            arrow(ax, x + 2.12, y + 0.57, x + 2.48, y + 0.57)
ax.text(5, 4.3, "Upgrade paths: each step is triggered by a limit the customer can see. Monthly or annual price per month", ha="center", fontsize=10.5, fontweight="bold", color=DEEP)
save(fig, "p10_upgrade_paths.png")

# p11 funnel, year three
i3 = 2
stages = [("Registrations, both sides", D["regs"][i3]), ("Activated accounts", D["fact"][i3] + D["iact"][i3]), ("New paying accounts", D["newp"][i3])]
fig, ax = plt.subplots(figsize=(8, 3.2))
ax.axis("off")
mx = stages[0][1]
for i, (nm, v) in enumerate(stages):
    w = 8 * [1.0, 0.72, 0.5][i]
    ax.add_patch(FancyBboxPatch(((10 - w) / 2, 2.2 - i * 0.95), w, 0.75, boxstyle="round,pad=0.02", fc=[MINT, TEAL, DEEP][i], ec="none"))
    ax.text(5, 2.575 - i * 0.95, f"{nm}: {v:,.0f}", ha="center", va="center", color="white" if i else DEEP, fontsize=10, fontweight="bold")
ax.set_xlim(0, 10)
ax.set_ylim(0, 3.1)
ax.set_title("The freemium funnel in 2029, from the model: free drives the network, paid plans monetise it")
save(fig, "p11_funnel.png")

# ================================================================ COMPETITOR CHARTS
REGCOL = {"Egypt and GCC": GOLD, "GCC": TEAL, "MENA serving": "#3E8E7E", "Global and GCC": MINT, "Africa": "#B5651D",
          "Emerging markets": "#5B7C99", "Global": DEEP}
# c1 positioning scatter, co-located competitors merged into one bubble
fig, ax = plt.subplots(figsize=(9.6, 8.2))
groups = {}
for nm, (reg, hq, fd, side, cat, th, code, src) in C.COVER.items():
    fx, ix, tot = C.coverage_score(code)
    groups.setdefault((fx, ix), []).append((nm, reg, tot))
pts, cols = [], {}
for (fx, ix), items in groups.items():
    tot = items[0][2]
    reg = items[0][1]
    size = 90 + tot * 45 + (len(items) - 1) * 40
    ax.scatter(fx, ix, s=size, color=REGCOL.get(reg, GREY), alpha=0.9, edgecolor="white", lw=1.2, zorder=3)
    lab = " / ".join(i[0] for i in items)
    pts.append((fx, ix, lab, size))
    if items[0][0] == "Angelsta":
        cols[lab] = "#7a5c00"
ax.axhline(2.5, color=GREY, lw=0.6, ls="--")
ax.axvline(3, color=GREY, lw=0.6, ls="--")
ax.set_xlim(-0.6, 6.8)
ax.set_ylim(-0.6, 5.7)
ax.set_xlabel("Founder side coverage, of 6: data room, cap table, ESOP, model and valuation, KPIs, deal pipeline", fontsize=9)
ax.set_ylabel("Investor side coverage, of 5: portfolio, tracking, matching, investor cap table, exits", fontsize=9)
for (x, y, t) in [(-0.5, 5.45, "INVESTOR TOOLS"), (3.15, 5.45, "TWO SIDED OPERATING SYSTEMS"), (-0.5, -0.5, "POINT SOLUTIONS"), (5.2, -0.5, "FOUNDER TOOLS")]:
    ax.text(x, y, t, fontsize=9, color="#B0B7BE", fontweight="bold")
place_labels(ax, pts, fontsize=9, bold={"Angelsta"}, colors=cols)
handles = [plt.Line2D([], [], marker="o", ls="", color=c, label=r) for r, c in REGCOL.items()]
ax.legend(handles=handles, frameon=False, fontsize=9, loc="upper center", bbox_to_anchor=(0.5, -0.09), ncol=4, title="Region")
ax.set_title("Competitive positioning: founder side against investor side coverage\nBubble size is total modules covered; competitors with identical coverage share a bubble", fontsize=11)
save(fig, "c1_positioning.png")

# c2 heatmap
names = list(C.COVER.keys())
mat = np.array([[{"F": 1.0, "P": 0.5, "N": 0.0}[ch] for ch in C.COVER[n][6]] for n in names])
fig, ax = plt.subplots(figsize=(9, 10))
from matplotlib.colors import ListedColormap
ax.imshow(mat, cmap=ListedColormap(["#EEF2F3", MINT, TEAL]), aspect="auto", vmin=0, vmax=1)
ax.set_xticks(range(11), C.MODULES, rotation=40, ha="right", fontsize=8)
ax.set_yticks(range(len(names)), names, fontsize=7.5)
ax.axvline(5.5, color="white", lw=3)
for i in range(len(names)):
    for j in range(11):
        ax.text(j, i, {1.0: "F", 0.5: "P", 0.0: ""}[mat[i, j]], ha="center", va="center", fontsize=6.5, color="white" if mat[i, j] == 1 else DEEP)
ax.set_title("Module coverage, 11 modules: founder side left, investor side right\nF full, P partial, blank not offered", fontsize=10)
ax.spines[:].set_visible(False)
save(fig, "c2_heatmap.png")

# c3 scores stacked
fig, ax = plt.subplots(figsize=(9, 4.8))
nm_s = sorted(C.SCORES, key=lambda n: C.SCORES[n][8])
left = np.zeros(len(nm_s))
for d, dim in enumerate(C.SCORE_DIMS):
    vals = np.array([C.SCORES[n][d] for n in nm_s])
    ax.barh(nm_s, vals, left=left, color=PAL[d % len(PAL)], label=dim)
    left += vals
for i, n in enumerate(nm_s):
    ax.text(left[i], i, f" {C.SCORES[n][8]:.1f}", va="center", fontsize=8, fontweight="bold")
ax.set_xlabel("Score out of 40, eight dimensions scored 1 to 5")
ax.legend(frameon=False, fontsize=7, ncol=4, loc="lower center", bbox_to_anchor=(0.5, -0.32))
ax.set_title("Competitive scoring from the primary research")
save(fig, "c3_scores.png")

# c4 radar top five
top = ["Visible", "Trackify", "Equidam", "Standard Metrics", "MAGNiTT"]
ang = np.linspace(0, 2 * np.pi, len(C.SCORE_DIMS), endpoint=False).tolist()
ang += ang[:1]
fig = plt.figure(figsize=(7, 6))
ax = plt.subplot(111, polar=True)
for n, col in zip(top, [DEEP, "#B5651D", GOLD, TEAL, MINT]):
    v = list(C.SCORES[n][:8])
    v += v[:1]
    ax.plot(ang, v, color=col, lw=1.6, label=n)
    ax.fill(ang, v, color=col, alpha=0.06)
ax.set_xticks(ang[:-1], C.SCORE_DIMS, fontsize=8)
ax.set_ylim(0, 5)
ax.legend(frameon=False, fontsize=8, loc="upper right", bbox_to_anchor=(1.3, 1.1))
ax.set_title("The five highest scoring competitors, by dimension", pad=18)
save(fig, "c4_radar.png")

# c5 category x region counts
cats = sorted(set(d[4] for d in C.DIRECTORY if d[1] != "Everywhere"))
regs = ["Egypt", "Qatar", "GCC", "MENA", "Africa", "Emerging markets", "Global"]


def reg_group(r):
    if r.startswith("Egypt"):
        return "Egypt"
    if r == "Qatar":
        return "Qatar"
    if r in ("GCC", "Global and GCC"):
        return "GCC"
    if r in ("MENA", "MENA serving"):
        return "MENA"
    if r == "Africa":
        return "Africa"
    if r == "Emerging markets":
        return "Emerging markets"
    return "Global"


cnt = np.zeros((len(cats), len(regs)))
for d in C.DIRECTORY:
    if d[1] == "Everywhere":
        continue
    cnt[cats.index(d[4]), regs.index(reg_group(d[1]))] += 1
fig, ax = plt.subplots(figsize=(9, 6))
ax.imshow(cnt, cmap=matplotlib.colors.LinearSegmentedColormap.from_list("t", ["#F4F7F7", TEAL]), aspect="auto")
ax.set_xticks(range(len(regs)), regs, fontsize=8)
ax.set_yticks(range(len(cats)), cats, fontsize=8)
for i in range(len(cats)):
    for j in range(len(regs)):
        if cnt[i, j]:
            ax.text(j, i, int(cnt[i, j]), ha="center", va="center", fontsize=8, color="white" if cnt[i, j] > 3 else DEEP)
ax.set_title(f"Market map: {len(C.DIRECTORY)} competitors, alternatives and partners by category and region")
ax.spines[:].set_visible(False)
save(fig, "c5_market_map.png")

# c6 ecosystem funding
fig, ax = plt.subplots(figsize=(8, 3.4))
labs = [e[0] for e in C.ECOSYSTEM]
vals = [e[1] for e in C.ECOSYSTEM]
bars = ax.bar(labs, vals, color=[DEEP, TEAL, TEAL, GOLD, GOLD, "#B5651D"])
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v, f"${v:,.0f}m", ha="center", va="bottom", fontsize=8)
ax.set_ylabel("USD millions, 2025")
ax.tick_params(axis="x", labelsize=8)
ax.set_title("Where the capital is: 2025 startup funding by market, Angelsta's first two markets in gold")
save(fig, "c6_ecosystem.png")

# c7 competitor funding
fig, ax = plt.subplots(figsize=(8, 3))
fs = sorted(C.FUNDING, key=lambda t: t[1])
bars = ax.barh([f[0] for f in fs], [f[1] for f in fs], color=TEAL)
for b, f_ in zip(bars, fs):
    ax.text(b.get_width(), b.get_y() + b.get_height() / 2, f" ${f_[1]:.1f}m", va="center", fontsize=8)
ax.set_xscale("log")
ax.set_xlabel("Disclosed funding, USD millions, log scale")
ax.set_title("Regional and emerging market competitors are thinly funded")
save(fig, "c7_competitor_funding.png")

# c8 comparables
fig, axes = plt.subplots(1, 2, figsize=(11, 3.6), gridspec_kw={"wspace": 0.75})
ax = axes[0]
bars = ax.barh([d[0] for d in C.DEALS][::-1], [d[2] for d in C.DEALS][::-1], color=DEEP)
for b, d in zip(bars, C.DEALS[::-1]):
    ax.text(b.get_width(), b.get_y() + b.get_height() / 2, f" ${d[2]:,}m, {d[1]}", va="center", fontsize=7.5)
ax.set_xscale("log")
ax.set_xlim(50, 20000)
ax.set_title("Disclosed transactions, USD m")
ax = axes[1]
labs = [m[0] for m in C.MULTIPLES]
vals = [m[1] for m in C.MULTIPLES]
bars = ax.barh(labs[::-1], vals[::-1], color=[GOLD if "Angelsta" in l else MINT for l in labs[::-1]])
for b, v in zip(bars, vals[::-1]):
    ax.text(b.get_width(), b.get_y() + b.get_height() / 2, f" {v:.1f}x", va="center", fontsize=8)
ax.tick_params(axis="y", labelsize=8)
ax.set_title("Revenue multiples, 2026")
fig.suptitle("Comparables: what buyers pay for private markets and SaaS businesses", fontsize=11, color=DEEP, fontweight="bold")
save(fig, "c8_comparables.png")

# c9 workflow chain infographic
steps = [("Financial\nmodel", ["Causal", "Jirav", "Forecastr"]), ("Valuation", ["Equidam", "Eqvista", "Carta"]), ("Cap table\nand ESOP", ["Carta", "RasMal", "Govy"]),
         ("Data room", ["DocSend", "Papermark", "Clara"]), ("Fundraising\nand matching", ["Foundersuite", "OpenVC", "Visible"]),
         ("Diligence", ["Trackify", "Lemina", "Dynamo"]), ("Portfolio\nmonitoring", ["Standard Metrics", "Vestberry", "Pentugram"]), ("Market\ndata", ["MAGNiTT", "PitchBook", "Dealroom"])]
fig, ax = plt.subplots(figsize=(11, 4.2))
ax.axis("off")
ax.set_xlim(0, 11)
ax.set_ylim(0, 4.2)
for i, (st, comps) in enumerate(steps):
    x = 0.15 + i * 1.35
    box(ax, x, 2.55, 1.2, 0.85, st, TEAL if i < 5 else DEEP, fs=8)
    if i < len(steps) - 1:
        arrow(ax, x + 1.2, 2.97, x + 1.33, 2.97)
    for j, c in enumerate(comps):
        ax.text(x + 0.6, 2.25 - j * 0.3, c, ha="center", fontsize=7, color=GREY)
box(ax, 0.15, 0.2, 10.6, 0.6, "Angelsta: one shared record across every step, founder side and investor side, with the AI agents and the community on top", GOLD, DEEP, fs=9)
ax.text(5.5, 3.85, "The fragmented workflow today: a different product at every step", ha="center", fontsize=11, fontweight="bold", color=DEEP)
save(fig, "c9_workflow.png")

# c10 roadmap
mk = [("Egypt", "Month 1", "Home market, Cairo team\nEGP list, 60%"), ("Qatar", "Month 4", "Sold from Cairo,\nQatar entity month 13"), ("Saudi Arabia", "Month 10", "Founder led,\nentity month 25"),
      ("UAE", "Month 13", "Cairo account executives,\nDIFC and ADGM funds"), ("Kuwait, Bahrain,\nOman", "Month 19", "Self serve\nand partners")]
fig, ax = plt.subplots(figsize=(11, 3.6))
ax.axis("off")
ax.set_xlim(0, 11)
ax.set_ylim(0, 3.6)
ax.plot([0.5, 10.5], [1.9, 1.9], color=MINT, lw=3, zorder=1)
for i, (m, w, d) in enumerate(mk):
    x = 1.0 + i * 2.2
    ax.scatter(x, 1.9, s=420, color=GOLD if i < 2 else TEAL, zorder=2)
    ax.text(x, 1.9, str(i + 1), ha="center", va="center", color="white", fontweight="bold")
    ax.text(x, 2.45, m, ha="center", fontsize=9.5, fontweight="bold", color=DEEP)
    ax.text(x, 2.95, w, ha="center", fontsize=8.5, color=TEAL)
    ax.text(x, 1.0, d, ha="center", fontsize=7.5, color=GREY)
box(ax, 0.5, 0.05, 10, 0.45, "From day one: self serve sign up and card billing from any country, global list price, rest of MENA and Africa at 70 per cent", DEEP, fs=8.5)
ax.text(5.5, 3.4, "Market entry: Egypt, then Qatar, then the GCC, with the whole world able to subscribe", ha="center", fontsize=11, fontweight="bold", color=DEEP)
save(fig, "c10_roadmap.png")

# c11 threat by region
levels = ["Critical", "High", "Moderate", "Low", "Partner"]
cnt = {l: [0] * len(regs) for l in levels}
for d in C.DIRECTORY:
    if d[1] == "Everywhere":
        continue
    if d[5] in cnt:
        cnt[d[5]][regs.index(reg_group(d[1]))] += 1
fig, ax = plt.subplots(figsize=(8, 3.4))
bottom = np.zeros(len(regs))
for l, col in zip(levels, [RED, GOLD, MINT, "#D5DCDF", TEAL]):
    ax.bar(regs, cnt[l], bottom=bottom, color=col, label=l)
    bottom += np.array(cnt[l])
ax.legend(frameon=False, fontsize=8, ncol=5, loc="upper left")
ax.set_ylabel("Number of companies")
ax.tick_params(axis="x", labelsize=8)
ax.set_title("Threat level by region: the critical threats are regional equity platforms and Visible")
save(fig, "c11_threats.png")

# c12 use of funds donut
fig, ax = plt.subplots(figsize=(8, 4.4))
keys = ["u_mkt", "u_sales", "u_prod", "u_ai", "u_ops"]
labs = ["Marketing and community", "Sales and customer success", "Product and AI engineering", "AI agents, cloud and delivery", "Leadership, operations, legal and set up"]
vals = [D[k] for k in keys]
w, _ = ax.pie(vals, colors=[GOLD, TEAL, DEEP, MINT, SAND], startangle=90, counterclock=False, wedgeprops=dict(width=0.38, edgecolor="white"))
ax.text(0, 0, f"{money(D['ask'])}\npre-seed", ha="center", va="center", fontsize=13, fontweight="bold", color=DEEP)
tot = sum(vals)
ax.legend(w, [f"{l}: {money(v)}, {v / tot:.0%}" for l, v in zip(labs, vals)], frameon=False, fontsize=9, loc="center left", bbox_to_anchor=(1, 0.5))
ax.set_title("Use of funds: marketing and community is the largest line")
save(fig, "c12_use_of_funds.png")

# c13 break even infographic: monthly revenue against monthly cost, first 36 months
ws_ = wb["Total Revenue"]
rev_row = next(r[0].row for r in ws_.iter_rows() if isinstance(r[0].value, str) and r[0].value.strip() == "Total revenue")
ex = wb["Expenses"]
cost_row = next(r[0].row for r in ex.iter_rows() if isinstance(r[0].value, str) and r[0].value.startswith("Total cash cost, direct and operating"))
mcols = [3 + (k // 12) * 13 + k % 12 for k in range(36)]
rv = [ws_.cell(rev_row, cc).value or 0 for cc in mcols]
cs = [ex.cell(cost_row, cc).value or 0 for cc in mcols]
be = next((k + 1 for k in range(36) if rv[k] > cs[k]), None)
D["be_month"] = be
fig, ax = plt.subplots(figsize=(10, 4))
xs = np.arange(1, 37)
ax.fill_between(xs, rv, cs, where=np.array(rv) < np.array(cs), color=RED, alpha=0.12, interpolate=True, label="Burn, funded by the pre-seed")
ax.fill_between(xs, rv, cs, where=np.array(rv) >= np.array(cs), color=TEAL, alpha=0.15, interpolate=True, label="Profit")
ax.plot(xs, rv, color=TEAL, lw=2.2, label="Monthly revenue")
ax.plot(xs, cs, color=DEEP, lw=2.2, ls="--", label="Monthly cash cost")
if be:
    ax.axvline(be, color=GOLD, lw=1.5)
    ax.text(be + 0.3, max(cs) * 0.95, f"Break even, month {be}\n{['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][(be - 1) % 12]} {2027 + (be - 1) // 12}", fontsize=9, fontweight="bold", color="#7a5c00")
for k in (12, 24):
    ax.axvline(k + 0.5, color="#D5DCDF", lw=0.8)
ax.text(6.5, ax.get_ylim()[1] * 0.02, "2027", ha="center", color=GREY)
ax.text(18.5, ax.get_ylim()[1] * 0.02, "2028", ha="center", color=GREY)
ax.text(30.5, ax.get_ylim()[1] * 0.02, "2029", ha="center", color=GREY)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: money(v)))
ax.set_xlabel("Month from launch")
ax.legend(frameon=False, fontsize=8, loc="upper left")
ax.set_title("Break even inside year two: monthly revenue crosses monthly cost")
save(fig, "c13_break_even.png")
json.dump(D, open(os.path.join(OUT, "model_numbers.json"), "w"), indent=1, default=float)

print("charts written to", OUT, json.dumps({k: D[k] for k in ["ask", "seed", "pre", "own"]}))
