import json, math
from datetime import date
import final_equations as fe, proposed_metrics as pm
burns12 = [120, 125, 130, 128, 135, 140, 138, 150, 145, 160, 150, 330]
ex = {}
ex["F-A"] = fe.f_a(1200, 800, floor=200, inflation_pct=8.0)
ex["F-A_lowbase"] = fe.f_a(10, 1, floor=200, inflation_pct=0)
ex["F-B"] = fe.f_b(1200, 480, "software")
ex["F-C"] = fe.f_c(1200, -300)
ex["F-D"] = fe.f_d(-260*4, 1200*4)
ex["F-E"] = fe.f_e(400, 1900, 2400, 150)
ex["O-A"] = fe.o_a([(92, 100, True), (4, 3, False), (55, 50, True), (30, 40, True)])
ex["O-A_old"] = fe.o_a([(50, 100, True), (200, 100, True)])
ex["O-B"] = fe.o_b([100, 103, 101, 106, 108, 112])
ex["O-C"] = fe.o_c(500, 40, 3)
ex["O-D"] = fe.o_d(12, 40)
ex["O-E"] = fe.o_e(94.0, 95.0)
ex["O-F"] = fe.o_f([0.9, 1.1, 1.0, 0.8, 1.2, 1.05, 1.0, 0.5, 1.1, 1.3, 1.0, 1.02])
ex["R-A"] = fe.r_a(2400, burns12, 6)
ex["R-A_3m"] = 2400/((160+150+330)/3)
ex["R-B"] = fe.r_b(burns12[:-1] if False else [130, 128, 135, 140, 138, 150, 145, 160, 150])
ex["R-C"] = fe.r_c(date(2027, 6, 30), date(2026, 11, 17), 4.0)
ex["R-D"] = fe.r_d(6000, 2400, 0, 1500)
ex["R-F"] = fe.r_f(1500, 5000, 60, 120)
ex["M-A"] = fe.m_a([16.96, 14.0, 19.0], 6.0)
ex["M-B"] = fe.m_b([(0.6, "BBB", "stable"), (0.3, "BB", "stable"), (0.1, "B-", "negative")], cds=(300, 0.4))
ex["M-C_A"] = fe.m_c(1500, 90, 0, 0, 0, 0.5)
ex["M-C_A"] = fe.m_c(1500, local_costs=90, base_costs=0, local_rev=0, base_rev=0, shock=0.5)
ex["M-C_B"] = fe.m_c(3000, local_costs=0, base_costs=100, local_rev=60, base_rev=0, shock=0.5)
ex["pco"] = {m: pm.prob_cash_out(2400, 150, 0.25, m) for m in (0, 6, 10, 12)}
gs = {"Financial": fe.group_score("Financial", {k: ex[k]["score"] for k in ("F-A", "F-B", "F-C", "F-D", "F-E")}),
      "Operational": fe.group_score("Operational", {k: ex[k]["score"] for k in ("O-A", "O-B", "O-C", "O-D", "O-E", "O-F")}),
      "Runway": fe.group_score("Runway", {k: ex[k]["score"] for k in ("R-A", "R-B", "R-C", "R-D", "R-F")}),
      "Market": fe.group_score("Market", {"M-A": ex["M-A"]["score"], "M-B": ex["M-B"]["score"], "M-C": ex["M-C_A"]["score"]})}
ex["groups"] = {k: list(v) for k, v in gs.items()}
ex["overall"] = fe.overall({k: v[0] for k, v in gs.items()}, p_cash_out=ex["pco"][6], runway_months=ex["R-A"]["value"])
def clean(o):
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, float) and (math.isinf(o) or math.isnan(o)): return str(o)
    return o
json.dump(clean(ex), open("results_final.json", "w"), indent=1)
for k, v in ex.items(): print(k, v)
