import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import date
import final_equations as fe

def test_anchored_both_directions():
    assert fe.anchored(80, 80, -10) == 0 and fe.anchored(-10, 80, -10) == 100 and fe.anchored(5, 0, 10) == 50
    assert fe.anchored(150, 80, -10) == 0 and fe.anchored(-50, 80, -10) == 100
def test_low_base_cannot_score_best():
    r = fe.f_a(10, 1, floor=200); assert "LOW_BASE" in r["flags"][0] and r["score"] > 0
def test_negative_base_blocked_not_flipped():
    assert not fe.f_a(-50, -100, floor=1)["computable"]
def test_cost_coverage_defined_at_zero_revenue():
    r = fe.f_c(0, -100); assert r["computable"] and r["value"] == 0 and r["score"] == 100
def test_o_a_cap_and_geometric():
    r = fe.o_a([(50, 100, True), (200, 100, True)]); assert abs(r["value"] - math.sqrt(0.75)) < 1e-12
    assert fe.achievement(0, 3, higher_is_better=False) == 1.5
def test_runway_robust_to_spike():
    burns = [120, 125, 130, 128, 135, 140, 138, 150, 145, 160, 150, 330]
    r = fe.r_a(2400, burns, 6); assert r["value"] == 16.0 and r["window_range"][0][1] < 12
def test_merged_gap_removes_double_count():
    r = fe.r_d(6000, 2400, 0, 1500); assert r["strict_dependency"] == 60 and r["committed_share"] == 25 and r["value"] == 35
def test_pace_and_target_reached():
    assert abs(fe.r_f(1500, 5000, 60, 120)["value"] - 6/7) < 1e-12 and fe.r_f(5000, 5000, 10, 10)["flags"] == ["TARGET_REACHED"]
def test_rating_score_monotone():
    sc = [fe.rating_score(r) for r in fe.NOTCH]; assert sc == sorted(sc) and sc[0] == 0 and sc[-1] == 100
def test_fx_direction_depends_on_exposure():
    a = fe.m_c(1500, 90, 0, 0, 0, 0.5); b = fe.m_c(3000, 0, 100, 60, 0, 0.5)
    assert a["value"] > 0 and b["value"] < 0 and a["score"] < b["score"]
def test_overall_veto_and_missing_groups():
    s, band, v = fe.overall({"Financial": 20, "Operational": 20, "Runway": 20, "Market": None}, p_cash_out=0.6)
    assert s >= 80 and band == "High" and v
def test_group_score_coverage():
    s, cov = fe.group_score("Financial", {"F-A": 40, "F-B": None, "F-C": 20, "F-D": None, "F-E": None}); assert abs(cov - 0.5) < 1e-12 and abs(s - 30) < 1e-12
def test_wilson_lower_bound_used():
    r = fe.o_d(12, 40); assert r["lower"] < r["value"] < r["upper"]
def test_weights_sum():
    assert all(sum(v.values()) == 100 for v in fe.W.values()) and sum(fe.GW.values()) == 100

import unittest
class Final(unittest.TestCase): pass
for _n, _f in list(globals().items()):
    if _n.startswith("test_") and callable(_f): setattr(Final, _n, (lambda f: lambda self: f())(_f))
if __name__ == "__main__": unittest.main()
