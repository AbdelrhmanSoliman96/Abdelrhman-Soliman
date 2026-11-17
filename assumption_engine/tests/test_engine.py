import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import engine as e

class T(unittest.TestCase):
    def test_normalisation(self):
        self.assertEqual(e.norm_country("Uae"), "UAE"); self.assertEqual(e.norm_country("KSA"), "Saudi Arabia")
        self.assertEqual(e.norm_industry("ecommerce"), "E-Commerce")
        with self.assertRaises(ValueError): e.norm_country("Atlantis")
    def test_all_files_covered(self):
        import csv
        d = os.path.join(os.path.dirname(__file__), "..", "data")
        for row in csv.DictReader(open(os.path.join(d, "countries_list.csv"))): e.norm_country(row["country"])
        for row in csv.DictReader(open(os.path.join(d, "industries_list.csv"))): e.norm_industry(row["industry"])
    def test_rates_bounded(self):
        for c in e.COUNTRIES["countries"]:
            for i in e.INDUSTRIES["industries"]:
                for ch in e.CH:
                    a = e.assume(c, i, "B2B_ENT", ch, draws=50)
                    if a["status"] == "OK":
                        for k in ("qualified_rate", "opportunity_rate", "win_rate"):
                            self.assertTrue(0 < a[k]["p10"] <= a[k]["base"] <= a[k]["p90"] < 1)
    def test_relationship_markets_favour_warm_over_cold(self):
        ksa = e.assume("KSA", "E-Commerce", "B2B_ENT", "BD_WARM")["deals_per_unit"]["base"] / e.assume("KSA", "E-Commerce", "B2B_ENT", "BD_COLD")["deals_per_unit"]["base"]
        uae = e.assume("UAE", "E-Commerce", "B2B_ENT", "BD_WARM")["deals_per_unit"]["base"] / e.assume("UAE", "E-Commerce", "B2B_ENT", "BD_COLD")["deals_per_unit"]["base"]
        self.assertGreater(ksa, 0); self.assertGreater(ksa/uae, 0.9)
    def test_ksa_beats_egypt_partnership_b2b(self):
        k = e.assume("KSA", "E-Commerce", "B2B_ENT", "PAR_STRATEGIC"); g = e.assume("Egypt", "E-Commerce", "B2B_ENT", "PAR_STRATEGIC")
        self.assertGreater(k["win_rate"]["base"], g["win_rate"]["base"]); self.assertLess(k["cycle_days"]["base"], g["cycle_days"]["base"])
    def test_gates(self):
        for c in ("Iran", "Syria", "Sudan", "Yemen", "Libya"): self.assertEqual(e.assume(c, "AI", "B2B_ENT", "BD_WARM")["status"], "REVIEW_REQUIRED")
        self.assertTrue(e.assume("Iraq", "AI", "B2B_ENT", "BD_WARM")["warnings"])
    def test_b2c_not_for_bd(self):
        self.assertEqual(e.assume("UAE", "Gaming", "B2C", "BD_COLD")["status"], "NOT_APPLICABLE")
    def test_blend_moves_to_actuals(self):
        p = e.assume("Egypt", "SaaS", "B2B_ENT", "BD_WARM"); b = e.assume("Egypt", "SaaS", "B2B_ENT", "BD_WARM", actuals={"win_rate": {"successes": 2, "trials": 40}})
        self.assertLess(b["win_rate"]["base"], p["win_rate"]["base"]); self.assertEqual(b["provenance"], "blended"); self.assertLess(b["sigma"], p["sigma"])
    def test_deterministic(self):
        self.assertEqual(e.assume("KSA", "SaaS", "B2B_ENT", "EVT_EXHIBIT"), e.assume("KSA", "SaaS", "B2B_ENT", "EVT_EXHIBIT"))
    def test_ramadan_reduces_volume(self):
        self.assertLess(e.season("Saudi Arabia", 2027, 2, "x")["volume"], e.season("Saudi Arabia", 2027, 10, "x")["volume"])
    def test_forecast_conserves_deals(self):
        plan = [dict(country="UAE", industry="SaaS", deal_type="B2B_ENT", channel="BD_WARM", month="2027-04", units=20)]
        f = e.forecast(plan); a = e.assume("UAE", "SaaS", "B2B_ENT", "BD_WARM")
        self.assertAlmostEqual(sum(r["deals"] for r in f), 20*a["deals_per_unit"]["base"]*e.season("UAE", 2027, 4, "x")["volume"], delta=0.1)

    def test_business_model_changes_numbers_and_outcome(self):
        a = e.assume("Egypt", "E-Commerce", "B2B_SMB", "EVT_EXHIBIT"); b = e.assume("Egypt", "E-Commerce", "B2B_SMB", "EVT_EXHIBIT", business_model="MARKETPLACE")
        self.assertNotEqual(a["leads_per_unit"]["base"], b["leads_per_unit"]["base"]); self.assertEqual(b["outcome"], "onboarded merchant or supplier")
        with self.assertRaises(ValueError): e.assume("Egypt", "SaaS", "B2B_SMB", "BD_WARM", business_model="NOPE")
    def test_rating_overrides_label_researched(self):
        base = e.assume("KSA", "FinTech", "B2B_ENT", "EVT_EXHIBIT"); r = e.assume("KSA", "FinTech", "B2B_ENT", "EVT_EXHIBIT", rating_overrides={"c_evt": 3})
        self.assertEqual(r["provenance"], "researched"); self.assertLess(r["leads_per_unit"]["base"], base["leads_per_unit"]["base"]); self.assertLess(r["sigma"], base["sigma"])
        with self.assertRaises(ValueError): e.assume("KSA", "FinTech", "B2B_ENT", "EVT_EXHIBIT", rating_overrides={"c_evt": 9})
    def test_event_inputs_scale_leads(self):
        base = e.assume("KSA", "FinTech", "B2B_ENT", "EVT_EXHIBIT"); big = e.assume("KSA", "FinTech", "B2B_ENT", "EVT_EXHIBIT", event_inputs={"attendees": 100000, "icp_share": 0.10})
        self.assertAlmostEqual(big["leads_per_unit"]["base"]/base["leads_per_unit"]["base"], 2.0, places=3)
    def test_activation_between_0_and_1(self):
        for ch in ("PAR_RESELLER", "PAR_STRATEGIC", "PAR_REFERRAL"): self.assertTrue(0 < e.activation_rate("UAE", "SaaS", ch) < 1)
    def test_halo_adds_leads_capped_and_attributed(self):
        plan = [dict(country="KSA", industry="FinTech", deal_type="B2B_ENT", channel="EVT_EXHIBIT", month="2027-03", units=2),
                dict(country="KSA", industry="FinTech", deal_type="B2B_ENT", channel="BD_COLD", month="2027-03", units=20),
                dict(country="KSA", industry="FinTech", deal_type="B2B_ENT", channel="BD_COLD", month="2027-04", units=20)]
        off = e.forecast_detail(plan, halo=False); on = e.forecast_detail(plan, halo=True)
        self.assertGreater(sum(r["deals"] for r in on["months"]), sum(r["deals"] for r in off["months"]))
        self.assertAlmostEqual(sum(on["assists"].values()), sum(r["deals_halo"] for r in on["months"]), places=2)
        for r in on["rows"]: self.assertLessEqual(r["up"], e.MODEL["halo"]["cap"] + 1e-9)
        self.assertEqual(sum(r["leads_halo"] for r in off["months"]), 0)
    def test_halo_is_within_same_country_and_industry_only(self):
        plan = [dict(country="KSA", industry="FinTech", deal_type="B2B_ENT", channel="EVT_EXHIBIT", month="2027-03", units=2),
                dict(country="Egypt", industry="FinTech", deal_type="B2B_ENT", channel="BD_COLD", month="2027-03", units=20)]
        self.assertEqual(sum(r["leads_halo"] for r in e.forecast_detail(plan)["months"]), 0)
    def test_reliability_scales_units(self):
        p = dict(country="UAE", industry="SaaS", deal_type="B2B_ENT", channel="EVT_EXHIBIT", month="2027-04", units=2)
        a = sum(r["deals"] for r in e.forecast([p])); b = sum(r["deals"] for r in e.forecast([dict(p, reliability=0.7)]))
        self.assertAlmostEqual(b/a, 0.7, places=2)
    def test_signed_partners_use_activation(self):
        p = dict(country="UAE", industry="SaaS", deal_type="B2B_ENT", channel="PAR_RESELLER", month="2027-04", signed_partners=10, partner_age_months=6)
        r = e.forecast_detail([p], halo=False)["rows"][0]; self.assertAlmostEqual(r["u"], 10*e.activation_rate("UAE", "SaaS", "PAR_RESELLER"), places=6)
if __name__ == "__main__": unittest.main()
