"""Offline-channel assumption engine for the financial-model agent.

Turns (country, industry, deal type, channel) into funnel assumptions with ranges and provenance.
All base values and ratings in config/ are expert PRIORS (v0.1), not market statistics. Replace with CRM actuals via blend().
Stdlib only. Deterministic (fixed seed).
"""
import json, math, os, random, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
def _load(n): return json.load(open(os.path.join(HERE, "config", n), encoding="utf-8"))
COUNTRIES, INDUSTRIES, MODEL = _load("countries.json"), _load("industries.json"), _load("model.json")
CH, DT = MODEL["channels"], MODEL["deal_types"]

def logit(p): return math.log(p/(1-p))
def sigm(x): return 1/(1+math.exp(-x))

def _norm(name, table, aliases, kind):
    key = str(name).strip()
    for k in table:
        if k.lower() == key.lower(): return k
    a = aliases.get(key.lower())
    if a: return a
    raise ValueError(f"Unknown {kind}: {name!r}. Supported: {', '.join(table)}")
def norm_country(n): return _norm(n, COUNTRIES["countries"], COUNTRIES["aliases"], "country")
def norm_industry(n): return _norm(n, INDUSTRIES["industries"], INDUSTRIES["aliases"], "industry")

def _z(c, i):
    z = {f"c_{k}": COUNTRIES["countries"][c][k]-3 for k in COUNTRIES["factor_defs"]}
    z.update({f"i_{k}": INDUSTRIES["industries"][i][k]-3 for k in INDUSTRIES["factor_defs"]})
    return z
FACTOR_LABEL = {**{f"c_{k}": f"Country: {v}" for k, v in COUNTRIES["factor_defs"].items()},
                **{f"i_{k}": f"Industry: {v}" for k, v in INDUSTRIES["factor_defs"].items()}}
# map short keys used in channels.json (c_evt, i_cyc ...) to factor keys
def _shift(coefs, z):
    contrib = [(f, z[f], b, b*z[f]) for f, b in coefs.items() if z[f] != 0]
    return sum(c[3] for c in contrib), sorted(contrib, key=lambda t: -abs(t[3]))

def season(country, year, month, family):
    s, ram = MODEL["seasonality"], COUNTRIES["countries"][country]["ram"]
    first, last = dt.date(year, month, 1), (dt.date(year+(month==12), month % 12+1, 1) - dt.timedelta(days=1))
    days = (last - first).days + 1
    vol, cyc = 1.0, 1.0
    w = MODEL["ramadan_windows"].get(str(year))
    if w:
        a, b = dt.date.fromisoformat(w[0]), dt.date.fromisoformat(w[1])
        ov = max(0, (min(b, last) - max(a, first)).days + 1)/days
        vol *= 1 - ov*ram*(1 - s["ramadan_volume"]); cyc *= 1 + ov*ram*(s["ramadan_cycle"]-1)
    e = MODEL["eid_adha"].get(str(year))
    if e:
        a = dt.date.fromisoformat(e); b = a + dt.timedelta(days=4)
        ov = max(0, (min(b, last) - max(a, first)).days + 1)/days
        vol *= 1 - ov*ram*(1 - s["eid_volume"])
    if month in s["summer_months"]:
        vol *= s["summer_volume"]; cyc *= s["summer_cycle"]
    return {"volume": vol, "cycle": cyc}

def assume(country, industry, deal_type, channel, actuals=None, rng_seed=7, draws=4000):
    """Return base assumptions with P10/P90, drivers and provenance for one combination."""
    c, i = norm_country(country), norm_industry(industry)
    if deal_type not in DT: raise ValueError(f"Unknown deal type {deal_type!r}. Supported: {', '.join(DT)}")
    if channel not in CH: raise ValueError(f"Unknown channel {channel!r}. Supported: {', '.join(CH)}")
    out = dict(country=c, industry=i, deal_type=deal_type, channel=channel, channel_name=CH[channel]["name"], unit=CH[channel]["unit"], warnings=[])
    allowed = DT[deal_type]["channels"]
    if allowed != "all" and channel not in allowed:
        out["status"] = "NOT_APPLICABLE"; out["warnings"].append(f"{deal_type} is not modelled for channel {channel}."); return out
    gate = COUNTRIES["countries"][c]["gate"]
    if gate == "review_required":
        out["status"] = "REVIEW_REQUIRED"
        out["warnings"].append(f"{c}: compliance/operability review required before any assumptions are used (sanctions, conflict or access constraints). No numbers produced.")
        return out
    if gate == "elevated": out["warnings"].append(f"{c}: elevated operating risk; treat ranges as wide and confirm with local team.")
    z, ch, d = _z(c, i), CH[channel], DT[deal_type]
    sh = {}; drivers = {}
    for st in "VQOWT":
        sh[st], drivers[st] = _shift(ch[st], z)
    if d["gov_v"]: sh["V"] += d["gov_v"]*z["c_gov"]
    lead = ch["lead"]*d["V"]*math.exp(sh["V"])
    q, o, w = (sigm(logit(ch[k]) + d[k] + sh[S]) for k, S in (("q", "Q"), ("o", "O"), ("w", "W")))
    cyc = ch["cyc"]*d["T"]*math.exp(sh["T"])
    # uncertainty
    sig = MODEL["uncertainty_sigma"]; s0 = math.sqrt(sig[COUNTRIES["countries"][c]["tier"]]**2 + sig["industry_add"]**2)
    prov = "prior"; n_eff = 0
    pc = MODEL["blend_pseudocounts"]
    if actuals:
        for k, key in (("q", "qualified_rate"), ("o", "opportunity_rate"), ("w", "win_rate")):
            a = actuals.get(key)
            if a:
                p = {"q": q, "o": o, "w": w}[k]; p = (p*pc["rate"] + a["successes"])/(pc["rate"] + a["trials"])
                if k == "q": q = p
                elif k == "o": o = p
                else: w = p
                n_eff = max(n_eff, a["trials"])
        a = actuals.get("leads_per_unit")
        if a: lead = (lead*pc["volume_units"] + a["leads"])/(pc["volume_units"] + a["units"]); n_eff = max(n_eff, a["units"]*5)
        a = actuals.get("cycle_days")
        if a: cyc = (cyc*pc["cycle_n"] + a["mean"]*a["n"])/(pc["cycle_n"] + a["n"]); n_eff = max(n_eff, a["n"])
        prov = "company_actuals" if n_eff >= 50 else "blended"
        s0 = s0/math.sqrt(1 + n_eff/pc["rate"])
    rate = lambda p: dict(base=p, p10=sigm(logit(p)-1.2816*s0), p90=sigm(logit(p)+1.2816*s0))
    pos = lambda v: dict(base=v, p10=v*math.exp(-1.2816*s0), p90=v*math.exp(1.2816*s0))
    r = random.Random(rng_seed); ds = []
    for _ in range(draws):
        ds.append(lead*math.exp(r.gauss(0, s0)) * sigm(logit(q)+r.gauss(0, s0)) * sigm(logit(o)+r.gauss(0, s0)) * sigm(logit(w)+r.gauss(0, s0)))
    ds.sort(); dpu = lead*q*o*w
    out.update(status="OK", provenance=prov, sigma=round(s0, 3),
               leads_per_unit=pos(lead), qualified_rate=rate(q), opportunity_rate=rate(o), win_rate=rate(w), cycle_days=pos(cyc),
               ramp_months=ch["ramp"],
               deals_per_unit=dict(base=dpu, p10=ds[int(.1*draws)], p90=ds[int(.9*draws)]),
               units_per_deal=1/dpu, leads_per_deal=1/(q*o*w),
               drivers={k: [dict(factor=FACTOR_LABEL[f], rating=z[f]+3, effect=round(100*(math.exp(e)-1), 1) if k in "VT" else round(e, 3)) for f, _, _, e in v[:3]] for k, v in drivers.items()})
    out["drivers_note"] = "effect = % change vs neutral for volume (V) and cycle (T); logit shift for rates (Q,O,W)."
    return out

def blend(*a, **k): return assume(*a, **k)

def forecast(plan, acv=None):
    """plan: list of dict(country, industry, deal_type, channel, month 'YYYY-MM', units, partner_age_months optional).
    Returns monthly leads/qualified/opps/deals (base, p10, p90) with deals lagged by cycle time."""
    months = {}
    def add(m, k, v):
        months.setdefault(m, dict(leads=0, qualified=0, opps=0, deals=0, deals_p10=0, deals_p90=0))[k] += v
    lagw = [(.6, .15), (.8, .25), (1.0, .30), (1.2, .20), (1.5, .10)]
    for row in plan:
        a = assume(row["country"], row["industry"], row["deal_type"], row["channel"])
        if a["status"] != "OK": raise ValueError(f"{row['country']}/{row['channel']}: {a['status']} {a['warnings']}")
        y, m = map(int, row["month"].split("-")); s = season(a["country"], y, m, a["channel"])
        ramp = 1.0
        if a["ramp_months"] and row.get("partner_age_months") is not None: ramp = min(1.0, row["partner_age_months"]/a["ramp_months"])
        u = row["units"]*ramp
        lead = u*a["leads_per_unit"]["base"]*s["volume"]; qd = lead*a["qualified_rate"]["base"]; op = qd*a["opportunity_rate"]["base"]
        dl = op*a["win_rate"]["base"]; cyc_m = a["cycle_days"]["base"]*s["cycle"]/30
        k = dl/a["deals_per_unit"]["base"] if a["deals_per_unit"]["base"] else 0
        key = row["month"]; add(key, "leads", lead); add(key, "qualified", qd); add(key, "opps", op)
        for mult, wt in lagw:
            lag = cyc_m*mult; lo = int(lag); fr = lag - lo
            for off, share in ((lo, 1-fr), (lo+1, fr)):
                if share <= 0: continue
                t = (y*12 + m - 1) + off; ky = f"{t//12:04d}-{t % 12 + 1:02d}"
                add(ky, "deals", dl*wt*share)
                add(ky, "deals_p10", u*s["volume"]*a["deals_per_unit"]["p10"]*wt*share); add(ky, "deals_p90", u*s["volume"]*a["deals_per_unit"]["p90"]*wt*share)
    out = [dict(month=k, **{kk: round(v, 2) for kk, v in vv.items()}) for k, vv in sorted(months.items())]
    if acv:
        for r in out: r["revenue_base"] = round(r["deals"]*acv, 2)
    return out

def matrix_rows():
    for c in COUNTRIES["countries"]:
        for i in INDUSTRIES["industries"]:
            for dtp, d in DT.items():
                for ch in (CH if d["channels"] == "all" else d["channels"]):
                    a = assume(c, i, dtp, ch, draws=300)
                    if a["status"] == "OK":
                        yield [c, i, dtp, ch, round(a["leads_per_unit"]["base"], 2), round(a["qualified_rate"]["base"], 3), round(a["opportunity_rate"]["base"], 3),
                               round(a["win_rate"]["base"], 3), round(a["cycle_days"]["base"]), round(a["deals_per_unit"]["base"], 4),
                               round(a["deals_per_unit"]["p10"], 4), round(a["deals_per_unit"]["p90"], 4), a["provenance"], "|".join(a["warnings"])]
                    else:
                        yield [c, i, dtp, ch, "", "", "", "", "", "", "", "", a["status"], "|".join(a["warnings"])]

if __name__ == "__main__":
    import argparse, csv, sys
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("assume"); [a.add_argument(x) for x in ("country", "industry", "deal_type", "channel")]
    sub.add_parser("matrix")
    args = p.parse_args()
    if args.cmd == "assume": print(json.dumps(assume(args.country, args.industry, args.deal_type, args.channel), indent=1))
    else:
        w = csv.writer(sys.stdout); w.writerow("country industry deal_type channel leads_per_unit qualified_rate opportunity_rate win_rate cycle_days deals_per_unit p10 p90 provenance_or_status warnings".split())
        w.writerows(matrix_rows())
