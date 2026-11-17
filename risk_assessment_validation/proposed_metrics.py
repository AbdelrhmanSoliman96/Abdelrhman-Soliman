"""Proposed supplementary equations from the validation review. None replaces a raw metric; all need methodology approval."""
import math, random, statistics as st
from raw_metrics import NonComputable, _need

# --- Financial
def log_growth(rev_t, rev_prev):
    _need(rev_t > 0 and rev_prev > 0, "both revenues must be positive"); return 100.0*math.log(rev_t/rev_prev)
def midpoint_growth(rev_t, rev_prev):
    _need(rev_t + rev_prev > 0, "sum must be positive"); return 100.0*(rev_t - rev_prev)/((rev_t + rev_prev)/2.0)
def cmgr(end, start, months):
    _need(start > 0 and months > 0, "bad base"); return 100.0*((end/start)**(1.0/months) - 1.0)
def real_growth(nominal_pct, inflation_pct): return 100.0*((1 + nominal_pct/100.0)/(1 + inflation_pct/100.0) - 1.0)
def cost_coverage(revenue, ebitda):
    cash_costs = revenue - ebitda; _need(cash_costs > 0, "cash costs must be positive"); return revenue/cash_costs
def ocf_to_ebitda(ocf, ebitda):
    _need(ebitda > 0, "EBITDA must be positive"); return ocf/ebitda
def debt_service_coverage(ocf_before_interest, interest, scheduled_principal):
    ds = interest + scheduled_principal; _need(ds > 0, "no debt service"); return ocf_before_interest/ds
def cash_to_debt_due_12m(cash, debt_due_12m):
    _need(debt_due_12m > 0, "no debt due"); return cash/debt_due_12m
# --- Operational
def geo_mean(xs):
    _need(all(x > 0 for x in xs) and xs, "positive values required"); return math.exp(sum(math.log(x) for x in xs)/len(xs))
def capped(x, cap=1.5): return min(x, cap)
def ambition_ratio(target, prior_actual, higher_is_better=True):
    _need(prior_actual > 0 and target > 0, "positive values required"); return target/prior_actual if higher_is_better else prior_actual/target
def nrr(mrr_start, expansion, contraction, churned):
    _need(mrr_start > 0, "no opening MRR"); return 100.0*(mrr_start + expansion - contraction - churned)/mrr_start
def grr(mrr_start, contraction, churned):
    _need(mrr_start > 0, "no opening MRR"); return 100.0*(mrr_start - contraction - churned)/mrr_start
def annualize_monthly_churn(m_pct): return 100.0*(1 - (1 - m_pct/100.0)**12)
def retention_reconciles(start, new, lost, end): return start + new - lost == end
def wilson(k, n, z=1.96):
    _need(n > 0, "no observations"); p = k/n; d = 1 + z*z/n
    c = (p + z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return max(0.0, c - h), min(1.0, c + h)
def pipeline_coverage(open_qualified_pipeline_value, remaining_target):
    _need(remaining_target > 0, "no remaining target"); return open_qualified_pipeline_value/remaining_target
def error_budget_consumed(sli, slo):
    _need(slo < 1, "SLO must be below 100%"); return (1 - sli)/(1 - slo)
def severity_weighted_miss(actuals, targets, higher_is_better=True):
    sev = []
    for a, t in zip(actuals, targets):
        r = (a/t) if higher_is_better else (t/a)
        if r < 1: sev.append(1 - r)
    return (sum(sev)/len(sev)) if sev else 0.0
def longest_miss_streak(flags):
    best = cur = 0
    for f in flags:
        cur = cur + 1 if f else 0; best = max(best, cur)
    return best
# --- Runway
def stressed_runway(cash, avg_burn, stress_pct):
    b = avg_burn*(1 + stress_pct/100.0); _need(b > 0, "burn must be positive"); return cash/b
def opex_coverage_months(cash, monthly_cash_costs):
    _need(monthly_cash_costs > 0, "no costs"); return cash/monthly_cash_costs
def runway_window_range(cash, burns):
    outs = []
    for w in (3, 6, 12):
        if len(burns) >= w:
            avg = sum(burns[-w:])/w
            if avg > 0: outs.append((w, cash/avg))
    return outs
def burn_cv(burns):
    m = st.mean(burns); _need(m > 0, "mean burn must be positive"); return st.pstdev(burns)/m
def burn_trend_3m(burns):
    _need(len(burns) >= 6, "six months required"); a = sum(burns[-3:])/3; b = sum(burns[-6:-3])/3
    _need(b != 0, "prior mean is zero"); return 100.0*(a - b)/abs(b)
def burn_multiple(net_burn, net_new_arr):
    _need(net_new_arr > 0, "net new ARR must be positive"); return net_burn/net_new_arr
def raise_slack_months(months_to_need, expected_months_to_close): return months_to_need - expected_months_to_close
def standardized_gap(cash, avg_burn, horizon_months, reserve_months, committed=0.0):
    required = avg_burn*horizon_months + avg_burn*reserve_months
    return required - cash - committed, required
def gap_coverage(committed, gap):
    _need(gap > 0, "no gap to cover"); return committed/gap
def pace_ratio(committed, target, elapsed_days, remaining_days):
    _need(elapsed_days > 0 and remaining_days > 0 and target > committed, "pace undefined")
    return (committed/elapsed_days)/((target - committed)/remaining_days)
def prob_cash_out(cash, burn_mean, burn_cv_, start_raise_month, close_median=4.0, close_sigma=0.45, p_success=0.65, n=20000, seed=11, horizon=60):
    """Probability that cash runs out before new money arrives. The raise starts at start_raise_month; time to close is lognormal;
    a raise that fails never delivers money. Monthly burn is lognormal with the given mean and coefficient of variation."""
    r = random.Random(seed); hit = 0; sigma = math.sqrt(math.log(1 + burn_cv_**2)); mu = math.log(burn_mean) - sigma**2/2
    for _ in range(n):
        cum = 0.0; m = 0; runout = float(horizon)
        while m < horizon:
            b = r.lognormvariate(mu, sigma)
            if cum + b >= cash: runout = m + (cash - cum)/b; break
            cum += b; m += 1
        close = start_raise_month + r.lognormvariate(math.log(close_median), close_sigma)
        if not ((r.random() < p_success) and (runout >= close)): hit += 1
    return hit/n
def runway_distribution(cash, burn_mean, burn_cv_, n=20000, seed=5, horizon=120):
    r = random.Random(seed); sigma = math.sqrt(math.log(1 + burn_cv_**2)); mu = math.log(burn_mean) - sigma**2/2; out = []
    for _ in range(n):
        cum = 0.0; m = 0; ro = float(horizon)
        while m < horizon:
            b = r.lognormvariate(mu, sigma)
            if cum + b >= cash: ro = m + (cash - cum)/b; break
            cum += b; m += 1
        out.append(ro)
    out.sort(); return out
# --- Market
def real_cagr(nominal_cagr_pct, inflation_cagr_pct): return 100.0*((1 + nominal_cagr_pct/100.0)/(1 + inflation_cagr_pct/100.0) - 1.0)
def dispersion_cv(values): m = st.mean(values); return st.pstdev(values)/m if m else float("nan")
def pd_from_cds(spread_bp, recovery, horizon_years=1.0):
    lam = (spread_bp/10000.0)/(1 - recovery); return lam, 1 - math.exp(-lam*horizon_years)
def revenue_weighted_pd(shares, pds): return sum(s*p for s, p in zip(shares, pds))
def fx_log_change(fx_t, fx_prev): _need(fx_t > 0 and fx_prev > 0, "positive rates required"); return 100.0*math.log(fx_t/fx_prev)
def fx_local_value_change(change_pct): return 100.0*(-(change_pct/100.0)/(1 + change_pct/100.0))
def realized_vol_annual(daily_rates, trading_days=252):
    rets = [math.log(b/a) for a, b in zip(daily_rates[:-1], daily_rates[1:])]; return 100.0*st.stdev(rets)*math.sqrt(trading_days)
def net_burn_base_ccy(local_costs, base_costs, local_revenue, base_revenue, local_depreciation):
    """Monthly net burn in base currency when local currency depreciates by s (local units per base unit rise by s)."""
    k = 1 + local_depreciation; return (local_costs/k + base_costs) - (local_revenue/k + base_revenue)
# --- Additional modules (outside the 20 factors; need approval)
def hhi(shares): return sum(s*s for s in shares)
def dso(receivables, revenue, days): _need(revenue > 0, "no revenue"); return receivables/revenue*days
def cash_conversion_cycle(dso_, dio_, dpo_): return dso_ + dio_ - dpo_
def cac_payback_months(cac, arpa_monthly, gross_margin): _need(arpa_monthly*gross_margin > 0, "no margin"); return cac/(arpa_monthly*gross_margin)
def ltv(arpa_monthly, gross_margin, monthly_churn): _need(monthly_churn > 0, "no churn"); return arpa_monthly*gross_margin/monthly_churn
def dilution(raise_amount, pre_money): return raise_amount/(pre_money + raise_amount)
def coverage_score(weights, computable): return sum(w for w, c in zip(weights, computable) if c)/sum(weights)
def freshness(age_days, tau_days): return math.exp(-age_days/tau_days)
