import sys, os, math, datetime as dt, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import raw_metrics as r, proposed_metrics as p

class Raw(unittest.TestCase):
    def test_weights_sum_and_count(self):
        for g, w in r.WEIGHTS.items(): self.assertEqual(sum(w.values()), 100, g)
        self.assertEqual(sum(len(w) for w in r.WEIGHTS.values()), 20)
    def test_financial(self):
        self.assertAlmostEqual(r.f_a_revenue_growth(120, 100), 20.0); self.assertAlmostEqual(r.f_b_gross_margin(200, 80), 60.0)
        self.assertAlmostEqual(r.f_c_ebitda_margin(-50, 200), -25.0); self.assertAlmostEqual(r.f_d_ocf_margin(-30, 300), -10.0); self.assertAlmostEqual(r.f_e_debt_ratio(150, 600), 25.0)
        for fn, args in ((r.f_a_revenue_growth, (10, 0)), (r.f_b_gross_margin, (0, 0)), (r.f_e_debt_ratio, (5, 0))):
            with self.assertRaises(r.NonComputable): fn(*args)
    def test_o_a_both_directions(self):
        self.assertAlmostEqual(r.o_a_achievement(80, 100, True), 0.8); self.assertAlmostEqual(r.o_a_achievement(4, 3, False), 0.75)
        with self.assertRaises(r.NonComputable): r.o_a_achievement(0, 3, False)
    def test_o_b_sign_semantics(self):
        self.assertAlmostEqual(r.o_b_kpi_trend(3, 2), 50.0); self.assertAlmostEqual(r.o_b_kpi_trend(-1, -2), 50.0)
        with self.assertRaises(r.NonComputable): r.o_b_kpi_trend(1, 0)
    def test_retention_churn_identity(self):
        self.assertAlmostEqual(r.o_c_retention(1050, 200, 1000), 85.0); self.assertAlmostEqual(r.o_c_churn(150, 1000), 15.0)
        for s, n, l in ((1000, 200, 150), (500, 40, 90)):
            e = s + n - l; self.assertAlmostEqual(r.o_c_retention(e, n, s) + r.o_c_churn(l, s), 100.0)
    def test_runway(self):
        self.assertAlmostEqual(r.r_a_runway(2400, [140, 150, 160]), 16.0)
        with self.assertRaises(r.NonComputable): r.r_a_runway(1000, [-10, 5, 3])
    def test_burn_trend(self):
        self.assertAlmostEqual(r.r_b_burn_trend(180, 150), 20.0); self.assertAlmostEqual(r.r_b_burn_trend(5, -10), 150.0)
        with self.assertRaises(r.NonComputable): r.r_b_burn_trend(5, 0)
    def test_days_month_convention(self):
        self.assertAlmostEqual(r.DAYS_PER_MONTH, 365.2425/12, places=3)
        self.assertEqual(r.r_c_days_to_need(dt.date(2027, 6, 30), dt.date(2026, 11, 17)), 225)
    def test_gap_and_external(self):
        self.assertAlmostEqual(r.r_d_funding_gap(6000, 2400), 3600); self.assertAlmostEqual(r.r_d_gap_ratio(6000, 2400), 60.0); self.assertAlmostEqual(r.r_d_gap_ratio(6000, 7000), -16.6667, places=3)
    def test_rd_re_identity_when_external_equals_gap(self):
        req, res = 6000.0, 2400.0
        self.assertAlmostEqual(r.r_d_gap_ratio(req, res), r.r_e_external_dependency(req - res, req))
    def test_fx_and_cagr(self):
        self.assertAlmostEqual(r.m_c_fx_change(50, 31), 61.2903, places=3); self.assertAlmostEqual(r.m_a_cagr(160, 100, 3), 17.0, delta=0.2)
        with self.assertRaises(r.NonComputable): r.m_a_cagr(1, 0, 2)

class Proposed(unittest.TestCase):
    def test_log_growth_symmetry(self): self.assertAlmostEqual(p.log_growth(200, 100), -p.log_growth(100, 200))
    def test_geo_mean_vs_arithmetic(self):
        self.assertAlmostEqual(p.geo_mean([0.5, 2.0]), 1.0); self.assertGreater((0.5 + 2.0)/2, 1.0)
    def test_wilson_bounds(self):
        lo, hi = p.wilson(0, 10); self.assertEqual(lo, 0.0); self.assertGreater(hi, 0)
        lo, hi = p.wilson(12, 40); self.assertTrue(0 < lo < 0.3 < hi < 1)
    def test_error_budget(self): self.assertAlmostEqual(p.error_budget_consumed(0.998, 0.999), 2.0)
    def test_stressed_runway(self): self.assertAlmostEqual(p.stressed_runway(2400, 150, 40), 2400/210)
    def test_fx_asymmetry(self):
        self.assertAlmostEqual(p.fx_local_value_change(100.0), -50.0); self.assertAlmostEqual(p.fx_local_value_change(25.0), -20.0)
    def test_net_burn_fx_shock(self):
        base = p.net_burn_base_ccy(100, 20, 40, 0, 0.0); shocked = p.net_burn_base_ccy(100, 20, 40, 0, 0.5)
        self.assertLess(shocked, base)   # local costs shrink in base currency
        self.assertGreater(p.net_burn_base_ccy(20, 100, 100, 0, 0.5), p.net_burn_base_ccy(20, 100, 100, 0, 0.0))  # local revenue, base costs: burn rises
    def test_pd_from_cds(self):
        lam, pd = p.pd_from_cds(300, 0.40); self.assertAlmostEqual(lam, 0.05); self.assertAlmostEqual(pd, 1 - math.exp(-0.05))
    def test_prob_cash_out_monotone(self):
        a = p.prob_cash_out(2400, 150, 0.25, 2, n=4000); b = p.prob_cash_out(2400, 150, 0.25, 12, n=4000); self.assertLess(a, b)
    def test_gap_and_pace(self):
        gap, req = p.standardized_gap(2400, 150, 12, 3, committed=0); self.assertAlmostEqual(req, 2250); self.assertAlmostEqual(gap, -150)
        self.assertGreater(p.pace_ratio(1000, 3000, 60, 60), 0)
if __name__ == "__main__": unittest.main()
