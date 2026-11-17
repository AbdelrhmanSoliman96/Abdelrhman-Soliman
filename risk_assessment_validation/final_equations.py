"""Recommended (final) equations for the 20 Angelsta raw metrics, with scoring.
Every function returns a dict: value (the fixed metric), score (0 = lowest risk, 100 = highest, or None), flags (list), computable (bool).
Anchors (best, worst) are PROPOSALS that need calibration and methodology-owner approval."""
import math, statistics as st
from datetime import date
import proposed_metrics as pm

def anchored(x, best, worst):
    """Linear risk score between two anchors, clipped to 0..100. Works whichever side is 'best'."""
    if best == worst: raise ValueError("anchors must differ")
    return 100.0*min(1.0, max(0.0, (x - best)/(worst - best)))
def NC(why): return dict(value=None, score=None, flags=["NOT_COMPUTABLE: " + why], computable=False)
def OK(value, score, flags=None, **extra): d = dict(value=value, score=score, flags=flags or [], computable=True); d.update(extra); return d

ANCH = {"F-A": (80.0, -10.0), "F-C": (1.0, 0.3), "F-D": (0.0, -100.0), "F-E1": (10.0, 80.0), "F-E2": (3.0, 0.5),
        "O-A": (1.0, 0.6), "O-B": (3.0, -3.0), "O-C": (10.0, 50.0), "O-D": (30.0, 10.0), "O-E": (0.5, 2.0), "O-F1": (0.0, 60.0), "O-F2": (0.0, 30.0),
        "R-A": (18.0, 6.0), "R-B1": (0.10, 0.60), "R-B2": (-10.0, 30.0), "R-C": (6.0, -3.0), "R-D": (0.0, 70.0), "R-F": (1.2, 0.4),
        "M-A": (15.0, -2.0), "M-C": (0.0, -40.0)}
GM_ANCH = {"software": (75.0, 40.0), "platform": (70.0, 30.0), "ecommerce": (40.0, 10.0), "services": (50.0, 15.0), "hardware": (45.0, 10.0)}
NOTCH = ["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "BB-", "B+", "B", "B-", "CCC+", "CCC", "CCC-", "CC", "C"]

# ---------------- Financial
def f_a(rev_t, rev_prev_same_period, floor, inflation_pct=0.0):
    """Real year-on-year growth in constant currency; midpoint growth if the base is below the materiality floor."""
    if rev_prev_same_period is None or rev_prev_same_period < 0 or rev_t < 0: return NC("negative or missing revenue")
    if rev_prev_same_period >= floor:
        g = 100.0*(rev_t - rev_prev_same_period)/rev_prev_same_period; fl = []
    else:
        if rev_t + rev_prev_same_period == 0: return NC("no revenue in either period")
        g = 100.0*(rev_t - rev_prev_same_period)/((rev_t + rev_prev_same_period)/2.0); fl = ["LOW_BASE: midpoint growth used"]
    real = 100.0*((1 + g/100.0)/(1 + inflation_pct/100.0) - 1.0)
    scored = min(real, 50.0) if fl else real   # a low base can never earn the best score
    return OK(real, anchored(scored, *ANCH["F-A"]), fl, nominal=g)
def f_b(revenue, cogs, model="software"):
    if revenue <= 0: return NC("no revenue")
    gm = 100.0*(revenue - cogs)/revenue; b, w = GM_ANCH[model]; return OK(gm, anchored(gm, b, w), [], model=model)
def f_c(revenue, ebitda):
    """Cost coverage = revenue / cash operating costs, cash operating costs = revenue - EBITDA (EBITDA = operating profit + D&A + impairment only)."""
    costs = revenue - ebitda
    if costs <= 0: return OK(float("inf"), 0.0, ["PROFITABLE"], margin=100.0*ebitda/revenue if revenue else None)
    cov = revenue/costs; m = 100.0*ebitda/revenue if revenue > 0 else None
    return OK(cov, anchored(cov, *ANCH["F-C"]), [], margin=m)
def f_d(ocf_12m, revenue_12m):
    if revenue_12m <= 0: return NC("no trailing revenue")
    m = 100.0*ocf_12m/revenue_12m; return OK(m, anchored(m, *ANCH["F-D"]))
def f_e(debt_corrected, assets, cash, debt_due_12m):
    if assets <= 0: return NC("no assets")
    ratio = 100.0*debt_corrected/assets; s1 = anchored(ratio, *ANCH["F-E1"])
    cover = 3.0 if debt_due_12m <= 0 else min(3.0, cash/debt_due_12m); s2 = anchored(cover, *ANCH["F-E2"])
    return OK(dict(debt_ratio=ratio, near_term_cover=cover), 0.5*s1 + 0.5*s2, [], s1=s1, s2=s2)
# ---------------- Operational
def achievement(actual, target, higher_is_better=True, cap=1.5):
    if target <= 0: return None
    if higher_is_better: a = actual/target
    else: a = cap if actual == 0 else target/actual
    return min(a, cap)
def o_a(pairs, cap=1.5):
    """pairs: list of (actual, target, higher_is_better). Geometric mean of capped achievements."""
    vals = [achievement(a, t, h, cap) for a, t, h in pairs]; vals = [v for v in vals if v is not None and v > 0]
    if not vals: return NC("no valid KPI")
    g = math.exp(sum(math.log(v) for v in vals)/len(vals)); return OK(g, anchored(g, *ANCH["O-A"]), [], n=len(vals))
def o_b(series):
    """Monthly growth rate from an OLS slope of ln(KPI) on time over the last 6 observations."""
    s = series[-6:]
    if len(s) < 4 or any(v <= 0 for v in s): return NC("need 4+ positive observations")
    n = len(s); xs = list(range(n)); xm = sum(xs)/n; ys = [math.log(v) for v in s]; ym = sum(ys)/n
    b = sum((x - xm)*(y - ym) for x, y in zip(xs, ys))/sum((x - xm)**2 for x in xs); g = 100.0*(math.exp(b) - 1.0)
    return OK(g, anchored(g, *ANCH["O-B"]), [] if n == 6 else ["SHORT_SERIES"])
def o_c(customers_start, customers_lost, months_in_period, reconciles=True):
    if customers_start <= 0: return NC("no starting customers")
    c = customers_lost/customers_start; m = 1 - (1 - c)**(1.0/months_in_period); ann = 100.0*(1 - (1 - m)**12)
    return OK(ann, anchored(ann, *ANCH["O-C"]), [] if reconciles else ["RECONCILIATION_FAILED"], monthly=100*m)
def o_d(k, n, window=None):
    if n <= 0: return NC("no qualified opportunities")
    lo, hi = pm.wilson(k, n); lo, hi = lo*100, hi*100; return OK(100.0*k/n, anchored(lo, *ANCH["O-D"]), ["SMALL_SAMPLE"] if n < 40 else [], lower=lo, upper=hi, n=n)
def o_e(sli_pct, slo_pct):
    if slo_pct >= 100: return NC("SLO of 100% leaves no error budget")
    b = (100.0 - sli_pct)/(100.0 - slo_pct); return OK(b, anchored(b, *ANCH["O-E"]))
def o_f(achievements, streak_threshold=3):
    """achievements: list of Actual/Target (direction-adjusted) per valid period; < 1 is a miss."""
    n = len(achievements)
    if n == 0: return NC("no scored periods")
    miss_rate = 100.0*sum(1 for a in achievements if a < 1)/n; swm = 100.0*sum(max(0.0, 1 - a) for a in achievements)/n
    streak = pm.longest_miss_streak([a < 1 for a in achievements]); sc = 0.5*anchored(miss_rate, *ANCH["O-F1"]) + 0.5*anchored(swm, *ANCH["O-F2"])
    fl = []
    if streak >= streak_threshold: sc = min(100.0, sc + 10.0); fl.append("MISS_STREAK")
    if n < 12: fl.append("SHORT_HISTORY")
    return OK(dict(miss_rate=miss_rate, severity_weighted=swm, streak=streak), sc, fl)
# ---------------- Runway & funding
def r_a(cash, burns, window=6):
    """Robust runway = cash / median of the last `window` monthly net burns; reports the 3M, 6M, 12M range and the +20% stress."""
    b = burns[-window:]
    if len(b) < 3: return NC("need 3+ months of burn")
    med = st.median(b)
    if med <= 0: return OK(float("inf"), 0.0, ["CASH_FLOW_POSITIVE"], opex_cover_needed=True)
    rw = cash/med; rng = pm.runway_window_range(cash, burns)
    return OK(rw, anchored(rw, *ANCH["R-A"]), [], stressed20=cash/(med*1.2), window_range=rng, median_burn=med)
def r_b(burns):
    if len(burns) < 6: return NC("need 6 months of burn")
    cv = pm.burn_cv(burns[-6:]); tr = pm.burn_trend_3m(burns)
    return OK(dict(cv=cv, trend3m=tr), 0.5*anchored(cv, *ANCH["R-B1"]) + 0.5*anchored(tr, *ANCH["R-B2"]))
def r_c(need_date, assess_date, expected_close_months=4.0):
    m = (need_date - assess_date).days/30.4369; sl = pm.raise_slack_months(m, expected_close_months)
    return OK(sl, anchored(sl, *ANCH["R-C"]), ["PAST_DUE"] if m <= 0 else [], months_to_need=m)
def r_d(required, cash, internal_cf, committed):
    """Merged R-D + R-E. strict dependency = (required - cash - internal CF)/required; residual gap ratio = strict dependency - committed share."""
    if required <= 0: return NC("no required cash")
    strict = max(0.0, 100.0*(required - cash - internal_cf)/required); cs = 100.0*committed/required; res = max(0.0, strict - cs)
    return OK(res, anchored(res, *ANCH["R-D"]), [], strict_dependency=strict, committed_share=cs)
def r_f(committed, target, elapsed_days, remaining_days):
    if target <= 0 or elapsed_days <= 0 or remaining_days <= 0: return NC("raise not in progress")
    if committed >= target: return OK(float("inf"), 0.0, ["TARGET_REACHED"])
    p = pm.pace_ratio(committed, target, elapsed_days, remaining_days); return OK(p, anchored(p, *ANCH["R-F"]))
# ---------------- Market & country
def m_a(nominal_cagr_pct_by_source, inflation_pct):
    v = nominal_cagr_pct_by_source
    if not v: return NC("no sources")
    nom = st.median(v); real = pm.real_cagr(nom, inflation_pct); fl = []
    if len(v) < 2: fl.append("SINGLE_SOURCE")
    elif pm.dispersion_cv(v) > 0.5: fl.append("HIGH_DISPERSION")
    return OK(real, anchored(real, *ANCH["M-A"]), fl)
def rating_score(rating, outlook=None):
    if rating not in NOTCH: raise ValueError("unknown rating")
    n = NOTCH.index(rating) + 1 + {"negative": 0.5, "stable": 0.0, "positive": -0.5, None: 0.0}[outlook]; n = min(21, max(1, n))
    return 100.0*(n - 1)/20.0
def m_b(exposures, cds=None):
    """exposures: list of (revenue share, rating, outlook). Revenue-weighted notch score; CDS-implied PD reported when a spread exists."""
    if not exposures or abs(sum(e[0] for e in exposures) - 1.0) > 1e-9: return NC("shares must sum to 1")
    s = sum(e[0]*rating_score(e[1], e[2]) for e in exposures); extra = {}
    if cds: lam, pd1 = pm.pd_from_cds(*cds); extra = dict(pd1=pd1)
    return OK(s, s, [], **extra)
def m_c(cash, local_costs, base_costs, local_rev, base_rev, shock):
    """Change in runway (%) when the local currency depreciates by `shock` (fraction). Cash held in base currency."""
    b0 = pm.net_burn_base_ccy(local_costs, base_costs, local_rev, base_rev, 0.0); b1 = pm.net_burn_base_ccy(local_costs, base_costs, local_rev, base_rev, shock)
    if b0 <= 0 or b1 <= 0: return OK(0.0, 0.0, ["BURN_NOT_POSITIVE"])
    r0, r1 = cash/b0, cash/b1; ch = 100.0*(r1 - r0)/r0; return OK(ch, anchored(ch, *ANCH["M-C"]), [], runway_before=r0, runway_after=r1)
# ---------------- Aggregation
W = {"Financial": {"F-A": 25, "F-B": 20, "F-C": 25, "F-D": 20, "F-E": 10}, "Operational": {"O-A": 25, "O-B": 20, "O-C": 20, "O-D": 15, "O-E": 10, "O-F": 10},
     "Runway": {"R-A": 30, "R-B": 10, "R-C": 15, "R-D": 35, "R-F": 10}, "Market": {"M-A": 40, "M-B": 35, "M-C": 25}}
GW = {"Financial": 25, "Operational": 20, "Runway": 35, "Market": 20}
def group_score(name, scores):
    """Weighted mean of computable factors; returns (score, coverage)."""
    w = W[name]; tot = sum(w.values()); got = {k: v for k, v in scores.items() if v is not None and k in w}
    if not got: return None, 0.0
    cov = sum(w[k] for k in got)/tot; return sum(w[k]*v for k, v in got.items())/sum(w[k] for k in got), cov
def overall(group_scores, p_cash_out=None, runway_months=None):
    """Weighted mean of group scores plus veto rules. Returns (score, band, vetoes)."""
    got = {k: v for k, v in group_scores.items() if v is not None}; tot = sum(GW[k] for k in got); s = sum(GW[k]*v for k, v in got.items())/tot
    vet = []
    if runway_months is not None and runway_months < 3: vet.append("runway under 3 months")
    if p_cash_out is not None and p_cash_out > 0.5: vet.append("probability of cash-out above 50%")
    if vet: s = max(s, 80.0)
    band = "Low" if s < 25 else "Moderate" if s < 50 else "Elevated" if s < 75 else "High"
    return s, band, vet
def confidence(coverage, ages_days, tau=90.0):
    fr = [pm.freshness(a, tau) for a in ages_days] or [1.0]; return coverage*sum(fr)/len(fr)
