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
        for key, txt in [("u_prod", "Product and AI engineering"), ("u_grow", "Community, growth and sales"), ("u_ai", "AI agents, cloud and delivery"), ("u_ops", "Leadership, operations, legal")]:
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
fig, ax = plt.subplots(figsize=(8, 4.6))
for pname, cname in C.PRICE_COVER.items():
    price = C.PRICE[pname][0]
    tot = C.coverage_score(C.COVER[cname][6])[2]
    is_a = pname.startswith("Angelsta")
    ax.scatter(tot, price, s=160 if is_a else 70, color=GOLD if is_a else (TEAL if C.PRICE[pname][1] == "Founder" else DEEP), edgecolor="white", zorder=3)
    ax.annotate(pname, (tot, price), xytext=(5, 3), textcoords="offset points", fontsize=7.5, color=DEEP if not is_a else "#7a5c00", fontweight="bold" if is_a else "normal")
ax.set_yscale("log")
ax.set_xlabel("Modules covered, of 11 (full = 1, partial = 0.5)")
ax.set_ylabel("Entry price, USD per month, log scale")
ax.set_title("Value map: more of the workflow for less, Angelsta sits bottom right")
ax.axvline(5.5, color=GREY, lw=0.6, ls="--")
ax.text(5.6, ax.get_ylim()[1] * 0.7, "covers both sides", fontsize=7.5, color=GREY)
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
    w = 8 * max(v / mx, 0.18)
    ax.add_patch(FancyBboxPatch(((10 - w) / 2, 2.2 - i * 0.95), w, 0.75, boxstyle="round,pad=0.02", fc=[MINT, TEAL, DEEP][i], ec="none"))
    ax.text(5, 2.575 - i * 0.95, f"{nm}: {v:,.0f}", ha="center", va="center", color="white" if i else DEEP, fontsize=10, fontweight="bold")
ax.set_xlim(0, 10)
ax.set_ylim(0, 3.1)
ax.set_title("The freemium funnel in 2029, from the model: free drives the network, paid plans monetise it")
save(fig, "p11_funnel.png")

# ================================================================ COMPETITOR CHARTS
REGCOL = {"Egypt and GCC": GOLD, "GCC": TEAL, "MENA serving": "#3E8E7E", "Global and GCC": MINT, "Africa": "#B5651D",
          "Emerging markets": "#5B7C99", "Global": DEEP}
# c1 positioning scatter
fig, ax = plt.subplots(figsize=(9, 6))
rng = np.random.default_rng(7)
for nm, (reg, hq, fd, side, cat, th, code, src) in C.COVER.items():
    fx, ix, tot = C.coverage_score(code)
    jx, jy = (0, 0) if nm == "Angelsta" else rng.uniform(-0.12, 0.12, 2)
    ax.scatter(fx + jx, ix + jy, s=60 + tot * 35, color=REGCOL.get(reg, GREY), alpha=0.85, edgecolor="white", zorder=3)
    ax.annotate(nm, (fx + jx, ix + jy), xytext=(4, 3), textcoords="offset points", fontsize=7, fontweight="bold" if nm == "Angelsta" else "normal")
ax.axhline(2.5, color=GREY, lw=0.6, ls="--")
ax.axvline(3, color=GREY, lw=0.6, ls="--")
ax.set_xlim(-0.4, 6.6)
ax.set_ylim(-0.4, 5.6)
ax.set_xlabel("Founder side coverage: data room, cap table, ESOP, model and valuation, KPIs, deal pipeline (of 6)")
ax.set_ylabel("Investor side coverage: portfolio, startup tracking, matching, investor cap table, exits (of 5)")
for (x, y, t) in [(0.1, 5.35, "Investor tools"), (4.6, 5.35, "Two sided operating systems"), (0.1, -0.25, "Point solutions"), (4.6, -0.25, "Founder tools")]:
    ax.text(x, y, t, fontsize=9, color=GREY, fontweight="bold")
handles = [plt.Line2D([], [], marker="o", ls="", color=c, label=r) for r, c in REGCOL.items()]
ax.legend(handles=handles, frameon=False, fontsize=7.5, loc="center left", bbox_to_anchor=(1, 0.5), title="Region")
ax.set_title("Competitive positioning: bubble size is total modules covered")
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
mk = [("Egypt", "Month 1", "Home market\nEGP list, 60%"), ("Qatar", "Month 4", "Doha manager,\nQFC or QSTP entity"), ("Saudi Arabia", "Month 10", "Founder led,\nentity month 13"),
      ("UAE", "Month 13", "DIFC and ADGM\nfund managers"), ("Kuwait, Bahrain,\nOman", "Month 19", "Country lead\nUAE and GCC")]
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
fig, ax = plt.subplots(figsize=(6, 4))
vals = [D["u_prod"], D["u_grow"], D["u_ai"], D["u_ops"]]
labs = ["Product and AI engineering", "Community, growth and sales", "AI agents, cloud and delivery", "Leadership, operations, legal"]
w, _ = ax.pie(vals, colors=[TEAL, DEEP, MINT, SAND], startangle=90, wedgeprops=dict(width=0.38, edgecolor="white"))
ax.text(0, 0, f"{money(D['ask'])}\npre-seed", ha="center", va="center", fontsize=12, fontweight="bold", color=DEEP)
ax.legend(w, [f"{l}: {money(v)}" for l, v in zip(labs, vals)], frameon=False, fontsize=8, loc="center left", bbox_to_anchor=(1, 0.5))
ax.set_title("The ask, built from year one expenses, and where it goes")
save(fig, "c12_use_of_funds.png")
print("charts written to", OUT, json.dumps({k: D[k] for k in ["ask", "seed", "pre", "own"]}))
