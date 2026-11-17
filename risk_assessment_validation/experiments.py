"""Numerical experiments behind the validation review. Synthetic or illustrative inputs only; results are written to results.json."""
import json, math, random, datetime as dt, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import raw_metrics as r, proposed_metrics as p

R = {}
# 1 reference company: all 20 raw metrics (illustrative inputs, thousand USD)
inp = dict(rev_t=1200, rev_prev=800, cogs=480, ebitda=-300, op_profit=-340, ocf=-260, debt=400, assets=1900,
           kpi_actual=92, kpi_target=100, kpi_prev=88, c_start=500, c_new=90, c_lost=40, c_end=550, qleads=200, conv=48, qopps=60, won=15,
           on_time=940, orders=1000, miss=3, valid=12, cash=2400, burns=[140, 150, 160], burn_m=160, burn_prev=150,
           assess=dt.date(2026, 11, 17), need=dt.date(2027, 6, 30), required=6000, resources=2400, external=3600, total_req=6000, committed=1500, target_raise=5000,
           size_end=160, size_start=100, years=3, fx_t=50.0, fx_prev=31.0)
ex = {}
ex["F-A"] = r.f_a_revenue_growth(inp["rev_t"], inp["rev_prev"]); ex["F-B"] = r.f_b_gross_margin(inp["rev_t"], inp["cogs"]); ex["F-C"] = r.f_c_ebitda_margin(inp["ebitda"], inp["rev_t"])
ex["F-D"] = r.f_d_ocf_margin(inp["ocf"], inp["rev_t"]); ex["F-E"] = r.f_e_debt_ratio(inp["debt"], inp["assets"])
ex["O-A"] = r.o_a_achievement(inp["kpi_actual"], inp["kpi_target"], True); ex["O-B"] = r.o_b_kpi_trend(inp["kpi_actual"], inp["kpi_prev"])
ex["O-C"] = (r.o_c_retention(inp["c_end"], inp["c_new"], inp["c_start"]), r.o_c_churn(inp["c_lost"], inp["c_start"]))
ex["O-D"] = (r.o_d_lead_conversion(inp["conv"], inp["qleads"]), r.o_d_win_rate(inp["won"], inp["qopps"])); ex["O-E"] = r.o_e_on_time(inp["on_time"], inp["orders"]); ex["O-F"] = r.o_f_miss_rate(inp["miss"], inp["valid"])
ex["R-A"] = r.r_a_runway(inp["cash"], inp["burns"]); ex["R-B"] = r.r_b_burn_trend(inp["burn_m"], inp["burn_prev"])
ex["R-C"] = (r.r_c_days_to_need(inp["need"], inp["assess"]), r.r_c_months_to_need(inp["need"], inp["assess"]))
ex["R-D"] = (r.r_d_funding_gap(inp["required"], inp["resources"]), r.r_d_gap_ratio(inp["required"], inp["resources"])); ex["R-E"] = r.r_e_external_dependency(inp["external"], inp["total_req"])
ex["R-F"] = (r.r_f_progress(inp["committed"], inp["target_raise"]), r.r_f_days_remaining(inp["need"], inp["assess"]))
ex["M-A"] = r.m_a_cagr(inp["size_end"], inp["size_start"], inp["years"]); ex["M-C"] = r.m_c_fx_change(inp["fx_t"], inp["fx_prev"])
R["reference_inputs"] = {k: (str(v) if isinstance(v, dt.date) else v) for k, v in inp.items()}; R["reference_outputs"] = ex

# 2 identities
R["identity_rd_re"] = dict(required=6000, resources=2400, gap_ratio=r.r_d_gap_ratio(6000, 2400), ext_dep=r.r_e_external_dependency(3600, 6000),
                           committed=1000, gap_ratio_with_committed=r.r_d_gap_ratio(6000, 2400 + 1000), ext_dep_strict=r.r_e_external_dependency(3600, 6000))
R["identity_rc_rf_days"] = dict(days_to_need=r.r_c_days_to_need(inp["need"], inp["assess"]), days_remaining=r.r_f_days_remaining(inp["need"], inp["assess"]))
R["identity_retention_churn"] = [(500, 90, 40, 550, r.o_c_retention(550, 90, 500), r.o_c_churn(40, 500))]

# 3 runway noise
cash = 2000
burns12 = [120, 125, 130, 128, 135, 140, 138, 150, 145, 160, 150, 330]
burns_dip = [120, 125, 130, 128, 135, 140, 138, 150, 145, 150, 150, 20]
def rw(b): return dict(w3=cash/(sum(b[-3:])/3), w6=cash/(sum(b[-6:])/6), w12=cash/(sum(b)/12), avg3=sum(b[-3:])/3, avg12=sum(b)/12)
R["runway_spike"] = rw(burns12); R["runway_dip"] = rw(burns_dip); R["burns12"] = burns12; R["burns_dip"] = burns_dip; R["runway_cash"] = cash
R["runway_dip"]["overstate_pct"] = 100*(R["runway_dip"]["w3"]/R["runway_dip"]["w12"] - 1)
R["burn_cv_6"] = p.burn_cv(burns12[-6:]); R["burn_cv_dip"] = p.burn_cv(burns_dip[-6:])
R["burn_trend_mom_spike"] = r.r_b_burn_trend(330, 150); R["burn_trend_mom_back"] = r.r_b_burn_trend(150, 330)
R["stress"] = {s: p.stressed_runway(2400, 150, s) for s in (0, 20, 40)}
R["opex_cov"] = p.opex_coverage_months(2400, 200)

# 4 FX
R["fx_table"] = [(fp, fx, r.m_c_fx_change(fx, fp), p.fx_log_change(fx, fp), p.fx_local_value_change(r.m_c_fx_change(fx, fp))) for fp, fx in ((31.0, 50.0), (3.75, 3.75), (1.0, 1.25), (1.0, 2.0))]
R["fx_shock_A"] = dict(base=p.net_burn_base_ccy(120, 30, 60, 0, 0.0), shocked=p.net_burn_base_ccy(120, 30, 60, 0, 0.5))
R["fx_shock_B"] = dict(base=p.net_burn_base_ccy(30, 120, 100, 0, 0.0), shocked=p.net_burn_base_ccy(30, 120, 100, 0, 0.5))
R["fx_runway"] = dict(cashA=1500, A0=1500/R["fx_shock_A"]["base"], A1=1500/R["fx_shock_A"]["shocked"], B0=1500/R["fx_shock_B"]["base"], B1=1500/R["fx_shock_B"]["shocked"])

# 5 O-A aggregation
R["oa_agg"] = dict(ratios=[0.5, 2.0], arithmetic=(0.5 + 2.0)/2, geometric=p.geo_mean([0.5, 2.0]), capped=((p.capped(0.5) + p.capped(2.0))/2))
R["oa_lower"] = [(0.03, a, r.o_a_achievement(a, 0.03, False)) for a in (0.06, 0.04, 0.03, 0.015, 0.005)]

# 6 funnel sample size
R["wilson"] = {"12/40": p.wilson(12, 40), "30/100": p.wilson(30, 100), "3/12": p.wilson(3, 12), "9/30": p.wilson(9, 30)}

# 7 weight sensitivity (synthetic cohort, rank-percentile mapping)
rng = np.random.default_rng(2026); N = 12
raw = np.column_stack([rng.normal(60, 40, N), rng.normal(55, 20, N), rng.normal(-60, 50, N), rng.normal(-70, 60, N), rng.uniform(0, 60, N)])
higher_better = [True, True, True, True, False]
def pct_rank(x, hb):
    order = x.argsort().argsort(); s = order/(len(x) - 1)*100
    return s if hb else 100 - s
S = np.column_stack([pct_rank(raw[:, j], higher_better[j]) for j in range(5)])
w0 = np.array([25, 20, 25, 20, 10])/100.0
base_score = S @ w0; base_rank = (-base_score).argsort().argsort() + 1
def spearman(a, b): return float(np.corrcoef(a.argsort().argsort(), b.argsort().argsort())[0, 1])
res = {}
for alpha in (20, 60):
    rhos = []; moved = np.zeros(N); top3_same = 0; draws = 5000
    for _ in range(draws):
        w = rng.dirichlet(alpha*w0); sc = S @ w; rk = (-sc).argsort().argsort() + 1
        rhos.append(spearman(-sc, -base_score)); moved += (abs(rk - base_rank) >= 2)
        top3_same += set(np.argsort(-sc)[:3]) == set(np.argsort(-base_score)[:3])
    res[alpha] = dict(rho_mean=float(np.mean(rhos)), rho_p5=float(np.percentile(rhos, 5)), moved2=(moved/draws).tolist(), top3=top3_same/draws, wcv=float(np.mean(np.std(rng.dirichlet(alpha*w0, 4000), axis=0)/w0)))
R["weight_sens"] = dict(res={str(k): v for k, v in res.items()}, base_rank=base_rank.tolist(), base_score=base_score.tolist(), n=N)
# single-factor dominance: how rank changes if one factor's weight doubles
dom = []
for j, name in enumerate(["F-A", "F-B", "F-C", "F-D", "F-E"]):
    w = w0.copy(); w[j] *= 2; w /= w.sum(); sc = S @ w; dom.append((name, spearman(-sc, -base_score)))
R["weight_doubling"] = dom

# 8 cash-out probability
dist = p.runway_distribution(2400, 150, 0.25)
R["runway_dist"] = dict(p10=dist[int(.1*len(dist))], p50=dist[int(.5*len(dist))], p90=dist[int(.9*len(dist))], mean=sum(dist)/len(dist))
R["cashout_curve"] = [(s, p.prob_cash_out(2400, 150, 0.25, s, p_success=1.0, n=8000), p.prob_cash_out(2400, 150, 0.25, s, p_success=0.65, n=8000)) for s in range(0, 15, 2)]
R["cashout_burn_cv"] = [(cv, p.prob_cash_out(2400, 150, cv, 8, p_success=1.0, n=8000)) for cv in (0.10, 0.25, 0.50)]

# 9 PD from CDS, revenue weighted
lam, pd1 = p.pd_from_cds(300, 0.40, 1); lam5, pd5 = p.pd_from_cds(300, 0.40, 5); lam3, pd3 = p.pd_from_cds(300, 0.30, 1)
R["cds"] = dict(lam=lam, pd1=pd1, pd5=pd5, pd1_rec30=pd3, weighted=p.revenue_weighted_pd([0.6, 0.3, 0.1], [0.01, 0.03, 0.08]))
# 10 coverage / freshness
w_fin = [25, 20, 25, 20, 10]; comp = [True, True, False, False, True]
R["coverage"] = dict(c=p.coverage_score(w_fin, comp), fresh=[p.freshness(a, 180) for a in (0, 90, 180, 365)])
# 11 other modules
R["modules"] = dict(hhi=p.hhi([0.5, 0.2, 0.15, 0.1, 0.05]), top1=0.5, dso=p.dso(300, 1200, 365), cac_payback=p.cac_payback_months(6000, 800, 0.7), ltv=p.ltv(800, 0.7, 0.02),
                    dil=[(pre, p.dilution(6000, pre)) for pre in (24000, 16800, 12000)], burn_multiple=p.burn_multiple(1800, 900))
# 12 edge cases
R["edge"] = dict(fa_neg_literal=100*(-50 - (-100))/(-100), fa_tiny=100*(10 - 1)/1, retention_ok=True, oa_inf_note="actual to 0 gives target/actual to infinity", pd_peg=r.m_c_fx_change(3.75, 3.75))
json.dump(R, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json"), "w"), indent=1, default=str)
print(json.dumps({k: R[k] for k in ("reference_outputs", "runway_spike", "runway_dip", "fx_runway", "oa_agg", "wilson", "runway_dist", "cds", "coverage", "modules", "edge")}, indent=1, default=str)[:6000])
print(R["weight_sens"]["res"]); print(R["weight_doubling"]); print(R["cashout_curve"]); print(R["cashout_burn_cv"])
