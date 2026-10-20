"""
Verify the financial model independently.

The audit proves there are no static values. The dynamic test proves the cells
are connected. Neither proves the cells are connected to the RIGHT things: a
formula can point one row off and still be a formula, still recalculate, and
still be wrong.

So this recomputes the model a second time, in Python, from the plan and from
the input values read back out of the workbook, and compares. Where the two
disagree, one of them is wrong, and the difference says where to look.

    python scripts/verify_financial_model.py output/StartPad_Financial_Model.xlsx
"""
import os
import math
import sys

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import _fm as F                                                 # noqa: E402
from finmodel import plan as P                                  # noqa: E402

TOL = 0.5          # dollars
RTOL = 1e-7

results = []


def check(name, expected, actual, tol=TOL):
    ok = abs((expected or 0) - (actual or 0)) <= max(
        tol, abs(expected or 0) * RTOL)
    results.append((ok, name, expected, actual))
    return ok


class Sheet:
    """Read a sheet by row label, with both values and formulas available."""

    def __init__(self, wv, wf, name):
        self.v, self.f = wv[name], wf[name]
        self.rows = {}
        for r in range(1, self.f.max_row + 1):
            t = self.f.cell(r, 1).value
            if isinstance(t, str) and t.strip():
                self.rows.setdefault(t.strip(), []).append(r)

    def row(self, label, nth=0):
        return self.rows[label][nth]

    def m(self, label, month, nth=0):
        return self.v.cell(self.row(label, nth), F.mcol(month)).value or 0

    def y(self, label, year, nth=0):
        return self.v.cell(self.row(label, nth), F.ycol(year)).value or 0

    def c(self, label, col, nth=0):
        return self.v.cell(self.row(label, nth), col).value or 0


def main(path):
    wv = load_workbook(path, data_only=True)
    wf = load_workbook(path)
    A = Sheet(wv, wf, "Assumption Setting")
    REV = Sheet(wv, wf, "Revenue Streams")
    TOT = Sheet(wv, wf, "Total Revenue")
    ACQ = Sheet(wv, wf, "Acquisitions")
    EXP = Sheet(wv, wf, "Expenses")
    PAY = Sheet(wv, wf, "Payroll")
    DEP = Sheet(wv, wf, "Depreciation and Amortization")
    CAP = Sheet(wv, wf, "Capital Expenditure")
    IS = Sheet(wv, wf, "Income Statement")
    BS = Sheet(wv, wf, "Balance Sheet")
    CF = Sheet(wv, wf, "Cash Flow Statement")

    def ass(label, col=3, nth=0):
        return A.c(label, col, nth)

    FUNCTIONS = list(dict.fromkeys(fn for fn, *_ in P.ROLES))

    # ------------------------------------------------ the whole engine
    # Rebuild the acquisition engine from scratch in Python, from the input
    # cells read back out of the workbook, and compare every month. This is
    # the check that matters now that volume is an output: if a formula
    # points one row off, these numbers diverge.
    nm = F.MONTHS
    yof = [0] + [F.year_of(m) for m in range(1, nm + 1)]

    on = {}
    for key, lbl, budgets, *_ in P.ONLINE_CHANNELS:
        on[key] = dict(label=lbl,
                       budget=[ass(lbl, 2 + y) for y in range(1, 6)],
                       cpc=ass(lbl, 8), org=ass(lbl, 9), ref=ass(lbl, 10),
                       s1=ass(lbl, 11))
    off = {}
    for key, lbl, *_ in P.OFFLINE_CHANNELS:
        off[key] = dict(label=lbl,
                        acts=[ass(lbl, 2 + y) for y in range(1, 6)],
                        cost=ass(lbl, 8), signups=ass(lbl, 9),
                        leads=ass(lbl, 10))
    buy = {}
    for key, lbl, *_ in P.BUYERS:
        buy[key] = dict(label=lbl, share=ass(lbl, 3), l2m=ass(lbl, 4),
                        m2p=ass(lbl, 5), p2w=ass(lbl, 6),
                        cycle=int(ass(lbl, 7)), mob=int(ass(lbl, 8)))
    eng = {}
    for key, lbl, buyer, *_ in P.ENGINES:
        eng[key] = dict(label=lbl, buyer=buyer, share=ass(lbl, 3),
                        units=ass(lbl, 4), life=int(ass(lbl, 5)),
                        gate=int(ass(lbl, 6)))
    s2 = [ass("Stage 2, lead to registered account", 2 + y)
          for y in range(1, 6)]
    s3o = [ass("Stage 3, registered to paid, reached online", 2 + y)
           for y in range(1, 6)]
    s3i = [ass("Stage 3, registered to paid, reached through an institution",
               2 + y) for y in range(1, 6)]
    uplift = [ass("Win rate uplift as references accumulate", 2 + y)
              for y in range(1, 6)]
    made = [ass("Mission Zero seasons produced per year", 2 + y)
            for y in range(1, 6)]
    inbound_rate = ass("Institutional enquiries per 1,000 accounts reached "
                       "directly")
    open_n = {}
    for key, n, _why in P.OPENING_CONTRACTS:
        open_n[key] = ass("Already signed: " + eng[key]["label"])
    open_w = [ass(f"Share of them mobilising in month {i + 1}")
              for i in range(len(P.OPENING_MOBILISATION))]

    z = lambda: [0.0] * (nm + 1)
    on_leads, off_leads, off_signups, leads = z(), z(), z(), z()
    reg_on, reg_off = z(), z()
    prop = {k: z() for k in buy}
    meet = {k: z() for k in buy}
    signed = {k: z() for k in buy}
    mobbed = {k: z() for k in buy}
    new = {k: z() for k in eng}
    active = {k: z() for k in eng}
    volume = {k: z() for k in eng}

    for m in range(1, nm + 1):
        y = yof[m]
        on_leads[m] = sum(c["budget"][y - 1] / c["cpc"]
                          * (1 + c["org"] + c["ref"]) * c["s1"]
                          for c in on.values() if c["cpc"])
        off_signups[m] = sum(c["acts"][y - 1] * c["signups"]
                             for c in off.values())
        off_leads[m] = sum(c["acts"][y - 1] * c["leads"]
                           for c in off.values())
        reg_on[m] = on_leads[m] * s2[y - 1]
        reg_off[m] = off_signups[m] * s2[y - 1]
        leads[m] = off_leads[m] + (reg_on[m] + reg_off[m]) / 1000 \
            * inbound_rate
        for k, b in buy.items():
            meet[k][m] = leads[m] * b["share"] * b["l2m"]
            prop[k][m] = meet[k][m] * b["m2p"]
            j = m - b["cycle"]
            signed[k][m] = (prop[k][j] * b["p2w"] * uplift[y - 1]
                            if j >= 1 else 0.0)
            j = m - b["mob"]
            mobbed[k][m] = signed[k][j] if j >= 1 else 0.0
        for bkey, b in buy.items():
            es = [k for k, e in eng.items() if e["buyer"] == bkey]
            open_share = sum(eng[k]["share"] for k in es
                             if m >= eng[k]["gate"])
            for k in es:
                e = eng[k]
                v = (mobbed[bkey][m] * e["share"] / open_share
                     if m >= e["gate"] and open_share else 0.0)
                if k in open_n and m <= len(open_w):
                    v += open_n[k] * open_w[m - 1]
                new[k][m] = v
        for k, e in eng.items():
            gone = new[k][m - e["life"]] if m - e["life"] >= 1 else 0.0
            active[k][m] = active[k][m - 1] + new[k][m] - gone
            volume[k][m] = active[k][m] * e["units"] / e["life"]
            if k == "podcast_seasons":
                volume[k][m] = min(volume[k][m], made[y - 1] / 12)

    for m in (1, 4, 9, 14, 20, 27, 33, 41, 50, 60):
        check(f"total institutional leads month {m} recompute",
              leads[m], ACQ.m("Total institutional leads", m), tol=0.001)
        for k, b in buy.items():
            check(f"{k} contracts signed month {m} recompute",
                  signed[k][m],
                  ACQ.m("Contracts signed, after the sales cycle", m,
                        nth=list(buy).index(k)), tol=0.001)
            check(f"{k} contracts mobilised month {m} recompute",
                  mobbed[k][m],
                  ACQ.m("Contracts mobilised, ready to deliver", m,
                        nth=list(buy).index(k)), tol=0.001)
        for k, e in eng.items():
            check(f"{k} contracts live month {m} recompute",
                  active[k][m],
                  ACQ.m(e["label"] + ", contracts live", m), tol=0.001)
            check(f"{k} volume month {m} recompute",
                  volume[k][m], REV.m(e["label"], m), tol=0.001)

    for y in range(1, 6):
        for k, e in eng.items():
            check(f"{k} volume year {y} recompute",
                  sum(volume[k][m] for m in F.months_of(y)),
                  REV.y(e["label"], y), tol=0.001)

    # No volume before the gate, and the opening contracts are the five
    # memoranda rather than a funnel win.
    for k, e in eng.items():
        if e["gate"] > 1:
            worst = max(REV.m(e["label"], m) for m in range(1, e["gate"]))
            results.append((worst <= 1e-9,
                            f"{k} delivers nothing before its gate month "
                            f"{e['gate']}", 0, worst))
    check("the five memoranda mobilise in full over the first three months",
          open_n["uni_cohorts_eg"],
          sum(new["uni_cohorts_eg"][m] for m in range(1, 4))
          - sum(mobbed["inst"][m] * eng["uni_cohorts_eg"]["share"]
                / sum(eng[k]["share"] for k, e in eng.items()
                      if e["buyer"] == "inst" and m >= e["gate"])
                for m in range(1, 4)), tol=0.001)

    # --------------------------------------------------- revenue by line
    price = {
        "University cohort programmes": "University cohort, all in programme fee",
        "Faculty licences": "Faculty licence, annual",
        "School cohorts": "School cohort",
        "School licences": "School licence, annual",
        "Technical and vocational cohorts": "Technical and vocational cohort",
        "National initiative seats": "National initiative seat",
        "Train the trainer cohorts": "Train the trainer cohort",
        "NGO and donor programmes": "NGO or donor programme",
        "Sponsored competitions": "Sponsored competition season",
        "Corporate and CSR programmes": "Corporate or CSR programme",
        "Mission Zero sponsorship": "Mission Zero season sponsorship",
    }
    vol_for = {
        "University cohort programmes": None,
        "Faculty licences": "Faculty licences",
        "School cohorts": "School cohorts",
        "School licences": "School licences",
        "Technical and vocational cohorts": "Technical and vocational cohorts",
        "National initiative seats": "National initiative seats",
        "Train the trainer cohorts": "Train the trainer cohorts",
        "NGO and donor programmes": "NGO and donor programmes",
        "Sponsored competitions": "Competitions, sponsored",
        "Corporate and CSR programmes": "Corporate and CSR programmes",
        "Mission Zero sponsorship": "Mission Zero seasons carrying a sponsor",
    }
    DUP = ("Faculty licences", "School cohorts", "School licences",
           "Technical and vocational cohorts", "National initiative seats",
           "Train the trainer cohorts", "NGO and donor programmes",
           "Corporate and CSR programmes")
    for y in range(1, 6):
        p_col = 2 + y
        for stream, pl in price.items():
            pr = ass(pl, p_col)
            if stream == "University cohort programmes":
                vol = (REV.y("University cohorts, Egypt", y)
                       + REV.y("University cohorts, Saudi Arabia", y))
            else:
                vol = REV.y(vol_for[stream], y)
            check(f"{stream} year {y} equals volume times price",
                  vol * pr,
                  REV.y(stream, y, nth=1 if stream in DUP else 0))

    # ------------------------------------------------- revenue cross foot
    for y in range(1, 6):
        inst = sum(REV.y(s, y, nth=1 if s in DUP else 0)
                   for s in price) + REV.y("Programme and incubator seats", y,
                                           nth=1)
        check(f"institutional revenue year {y} is the sum of its lines",
              inst, REV.y("Institutional and sponsor revenue", y))
        check(f"total revenue year {y} is institutional plus subscriptions",
              inst + REV.y("Subscription revenue recognised", y),
              TOT.y("Total revenue", y))
        check(f"income statement revenue year {y} matches Total Revenue",
              TOT.y("Total revenue", y), IS.c("Total revenue", 2 + y))

    # ------------------------------------------------------ the funnel
    for y in (1, 3, 5):
        for m in (F.months_of(y)[0], F.months_of(y)[-1]):
            lbl = "Short video, TikTok, Instagram, Facebook"
            spend = ACQ.m(lbl, m)
            cpc, org = ass(lbl, 8), ass(lbl, 9)
            ref, s1 = ass(lbl, 10), ass(lbl, 11)
            paid = spend / cpc if cpc else 0
            check(f"short video paid clicks, month {m}", paid,
                  ACQ.m("Paid clicks", m), tol=0.01)
            check(f"short video total clicks, month {m}",
                  paid * (1 + org + ref),
                  ACQ.m("Total clicks after organic and referral", m),
                  tol=0.01)
            check(f"short video leads, month {m}", paid * (1 + org + ref) * s1,
                  ACQ.m("Stage 1, leads", m), tol=0.01)
            check(f"registered from online leads, month {m}",
                  ACQ.m("Total online leads", m) * s2[y - 1],
                  ACQ.m("Registered accounts from online leads", m), tol=0.01)
            check(f"new paid accounts, month {m}",
                  ACQ.m("Registered accounts from institutions", m)
                  * s3i[y - 1]
                  + (ACQ.m("Registered accounts from online leads", m)
                     + ACQ.m("Registered accounts from offline sign ups", m))
                  * s3o[y - 1],
                  ACQ.m("Stage 3, new paid accounts", m), tol=0.01)

    # ------------------------------------------------------ direct cost
    for y in range(1, 6):
        rate = ass("Facilitator day rate", 2 + y)
        per = ass("Facilitators per cohort")
        days = ass("Delivery days, university cohort")
        uni = (REV.y("University cohorts, Egypt", y)
               + REV.y("University cohorts, Saudi Arabia", y))
        check(f"university facilitation year {y}", uni * rate * per * days,
              EXP.y("Facilitation, university cohorts", y))
        pd_share = ass("Party 1, share of cohorts delivered by certified "
                       "partners", 2 + y)
        pd_rate = ass("Party 1, the partner's share of that cohort fee")
        base = (REV.y("University cohort programmes", y)
                + REV.y("School cohorts", y, nth=1)
                + REV.y("Technical and vocational cohorts", y, nth=1))
        check(f"delivery partner revenue share year {y}",
              base * pd_share * pd_rate,
              EXP.y("Revenue share, certified delivery partners", y))

    # --------------------------------------------------------- payroll
    burden = PAY.v.cell(PAY.row("Employer burden on gross salary"), 3).value
    for y in range(1, 6):
        expected = sum(r[3][y - 1] * r[4][y - 1] for r in P.ROLES) \
            * 12 * (1 + burden)
        check(f"payroll year {y} equals establishment times salary",
              expected, PAY.y("Total payroll", y))
        check(f"headcount year {y} equals the plan",
              sum(r[4][y - 1] for r in P.ROLES),
              PAY.y("Total headcount", y), tol=0.001)
        check(f"headcount year {y} is within the cap",
              min(sum(r[4][y - 1] for r in P.ROLES), P.HEADCOUNT_CAP[y - 1]),
              PAY.y("Total headcount", y), tol=0.001)

    # ------------------------------------------------- profit cross foot
    for y in range(1, 6):
        rev = TOT.y("Total revenue", y)
        cogs = EXP.y("Total direct cost", y)
        gp = EXP.y("Gross profit", y)
        opex = EXP.y("Operating cost before depreciation", y)
        dna = EXP.y("Depreciation and amortisation", y)
        check(f"gross profit year {y} is revenue less direct cost",
              rev - cogs, gp)
        check(f"EBITDA year {y} is gross profit less operating cost",
              gp - opex, EXP.y("EBITDA", y))
        check(f"EBIT year {y} is EBITDA less depreciation",
              EXP.y("EBITDA", y) - dna, EXP.y("EBIT, operating profit", y))
        check(f"total expenses year {y} is direct plus operating",
              cogs + opex + dna, EXP.y("Total expenses, direct and operating",
                                       y))
        tax = IS.c("Corporate income tax", 2 + y)
        check(f"net profit year {y} is profit before tax plus tax",
              IS.c("Profit before tax", 2 + y) + tax,
              IS.c("Net profit for the year", 2 + y))
        check(f"tax year {y} is the rate on taxable profit",
              -IS.c("Taxable profit", 2 + y) * ass("Corporate income tax rate"),
              tax)

    # ---------------------------------------------------- balance sheet
    for y in range(1, 6):
        col = 3 + y
        check(f"balance sheet balances, year {y}",
              0, BS.c("CHECK, total assets less liabilities and equity", col),
              tol=0.01)
        check(f"cash on the balance sheet equals the cash flow, year {y}",
              CF.m("Cash at the end of the month", F.months_of(y)[-1]),
              BS.c("Cash and cash equivalents", col))
        check(f"retained earnings year {y} is cumulative net profit",
              sum(IS.c("Net profit for the year", 2 + k)
                  for k in range(1, y + 1)),
              BS.c("Retained earnings", col))
        seed = ass("Seed round raised")
        seed_m = ass("Month the seed round lands")
        check(f"share capital year {y} is opening cash plus the seed",
              ass("Opening cash") + (seed if F.months_of(y)[-1] >= seed_m
                                     else 0),
              BS.c("Share capital", col))
        check(f"total assets year {y} is the sum of its lines",
              BS.c("Cash and cash equivalents", col)
              + BS.c("Trade receivables", col)
              + BS.c("Property and equipment, net", col)
              + BS.c("Intangible assets, net", col),
              BS.c("Total assets", col))

    # -------------------------------------------------------- cash flow
    for y in range(1, 6):
        for m in (F.months_of(y)[0], F.months_of(y)[-1]):
            opening = (ass("Opening cash") if m == 1
                       else CF.m("Cash at the end of the month", m - 1))
            check(f"closing cash month {m} is opening plus the movement",
                  opening + CF.m("Net movement in cash", m),
                  CF.m("Cash at the end of the month", m))
            check(f"net movement month {m} is the three activities",
                  CF.m("Net cash from operating activities", m)
                  + CF.m("Net cash used in investing activities", m)
                  + CF.m("Net cash from financing activities", m),
                  CF.m("Net movement in cash", m))

    # ------------------------------------------- go to market capacity
    # Volume is already the funnel's own output. What this block proves is
    # the other half: that the people exist to run the activity, and that the
    # delivery network the plan implies is sized from the plan rather than
    # guessed.
    GTM = Sheet(wv, wf, "GTM Capacity and Timing")
    sample = (1, 6, 13, 24, 30, 42, 55, 60)

    for m in sample:
        total_fn = sum(GTM.m(fn, m) for fn in FUNCTIONS)
        check(f"headcount by function month {m} is the establishment",
              PAY.m("Total headcount", m), total_fn)

    for i, (key, label, function, own, fnd, amb, prt) in enumerate(
            P.ACTIVITY_CAPACITY):
        for m in sample:
            expected = (GTM.m(function, m) * ass(label, 3, 1)
                        + GTM.m("Leadership", m) * ass(label, 4, 1)
                        + GTM.m("Campus ambassadors on a stipend", m)
                        * ass(label, 5, 1)
                        + GTM.m("Certified delivery partner organisations", m)
                        * ass(label, 6, 1))
            check(f"capacity for {key} month {m} is the four sources of "
                  f"people times their quotas",
                  expected,
                  GTM.m("Capacity, the people who can run it", m, nth=i))
            check(f"activity planned for {key} month {m} is what the "
                  f"Acquisitions sheet runs",
                  ACQ.m(label, m), GTM.m(label + ", planned", m))

    for m in sample:
        expected = sum(ACQ.m("Meetings held", m, nth=i)
                       for i in range(len(P.BUYERS)))
        check(f"meetings the funnel generates month {m} is the buyer types "
              f"added up",
              expected, GTM.m("Meetings the funnel generates", m))
        check(f"meeting capacity month {m} is heads times their quotas",
              PAY.m("Commercial heads", m)
              * ass("Meetings per commercial head per month")
              + GTM.m("Leadership", m)
              * ass("Meetings per founder per month")
              + GTM.m("Growth and Content", m)
              * ass("Meetings per growth and content head per month"),
              GTM.m("Meetings the team can hold", m))

        # The delivery network is sized from the cohorts the funnel sold.
        days = ((REV.m("University cohorts, Egypt", m)
                 + REV.m("University cohorts, Saudi Arabia", m))
                * ass("Delivery days, university cohort")
                + REV.m("School cohorts", m)
                * ass("Delivery days, school cohort")
                + REV.m("Technical and vocational cohorts", m)
                * ass("Delivery days, technical cohort")
                ) * ass("Facilitators per cohort")
        check(f"facilitator days needed month {m} is cohorts times days "
              f"times facilitators",
              days, GTM.m("Facilitator days the cohort plan needs", m))
        req = days / ass("Delivery days one certified facilitator gives per "
                         "month")
        check(f"facilitators required month {m} is days over days given",
              req, GTM.m("Certified facilitators the plan requires", m))
        check(f"the certified pool month {m} is the requirement plus the "
              f"buffer, rounded up",
              math.ceil(req * ass("Spare capacity held in the certified "
                                  "pool") - 1e-9),
              GTM.m("Certified facilitators in the pool", m))
        pdc = (REV.m("All in person cohorts delivered", m)
               * ass("Party 1, share of cohorts delivered by certified "
                     "partners", 2 + F.year_of(m)))
        check(f"partner organisations month {m} are the cohorts they "
              f"deliver over what one delivers",
              math.ceil(pdc / ass("Cohorts one certified partner "
                                  "organisation delivers per month") - 1e-9),
              GTM.m("Certified delivery partner organisations", m))

    # The two capacity gates. Both must read nil in every month, or the plan
    # is running activity nobody is free to do.
    for label in ("Activity the plan asks for beyond what the team can run",
                  "Meetings asked for beyond capacity"):
        worst = max(GTM.m(label, m) for m in range(1, 61))
        results.append((worst <= 0.001,
                        f"capacity gate, {label.lower()}, reads nil in every "
                        f"month", 0, worst))

    # Signature and first delivery are arithmetic on the cycle and the
    # mobilisation period, counted from a first day of activity in month one.
    for i, (bkey, label, share, l2m, m2p, p2w, cyc, mob, why) in enumerate(
            P.BUYERS):
        check(f"{bkey} signs in month one plus its sales cycle",
              GTM.c(label, 2) + GTM.c(label, 3), GTM.c(label, 4))
        check(f"{bkey} mobilisation period is the assumption",
              mob, GTM.c(label, 5))
        check(f"{bkey} first delivery is signature plus mobilisation",
              GTM.c(label, 4) + mob, GTM.c(label, 6))

    # ----------------------------------------------- assets never negative
    for y in range(1, 6):
        m = F.months_of(y)[-1]
        gross = CAP.m("Total gross assets", m)
        accum = DEP.m("Total accumulated depreciation", m)
        nbv = DEP.m("Total net book value", m)
        check(f"net book value year {y} is cost less accumulated",
              gross - accum, nbv)
        results.append((nbv >= -0.01,
                        f"net book value year {y} is not negative", 0, nbv))
        results.append((accum <= gross + 0.01,
                        f"accumulated depreciation year {y} does not exceed "
                        f"cost", gross, accum))

    failed = [r for r in results if not r[0]]
    print(f"checks run:    {len(results)}")
    print(f"checks passed: {len(results) - len(failed)}")
    if failed:
        print(f"\nFAILED {len(failed)}:")
        for ok, name, exp, act in failed[:40]:
            print(f"  {name}\n      expected {exp:,.4f}   workbook "
                  f"{act:,.4f}   difference {(act or 0) - (exp or 0):,.4f}")
        return 1
    print("\nAll checks passed: every figure recomputes from the cells it "
          "claims to come from.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1
                  else "output/StartPad_Financial_Model.xlsx"))
