"""The 20 raw metrics of the Angelsta 'Raw Metric Methodology' (review edition, 12 Nov 2026), implemented exactly as written.
A zero or invalid denominator raises NonComputable (the methodology says: never substitute zero). No scoring is done here."""
import datetime as dt

class NonComputable(ValueError):
    pass

def _need(cond, why):
    if not cond: raise NonComputable(why)

# ---- 01 Financial
def f_a_revenue_growth(rev_t, rev_prev):
    _need(rev_prev is not None and rev_prev > 0, "previous-period revenue missing, zero or not a meaningful base")
    return 100.0*(rev_t - rev_prev)/rev_prev
def f_b_gross_margin(revenue, cogs):
    _need(revenue is not None and revenue > 0, "revenue zero or missing")
    return 100.0*(revenue - cogs)/revenue
def f_c_ebitda_margin(ebitda, revenue):
    _need(revenue is not None and revenue > 0, "revenue zero or missing")
    return 100.0*ebitda/revenue
def f_c_operating_margin(operating_profit, revenue):
    _need(revenue is not None and revenue > 0, "revenue zero or missing")
    return 100.0*operating_profit/revenue
def f_d_ocf_margin(ocf, revenue):
    _need(revenue is not None and revenue > 0, "revenue zero or missing")
    return 100.0*ocf/revenue
def f_e_debt_ratio(total_debt, total_assets):
    _need(total_assets is not None and total_assets > 0, "assets zero or missing")
    return 100.0*total_debt/total_assets

# ---- 02 Operational and KPI
def o_a_achievement(actual, target, higher_is_better=True):
    if higher_is_better:
        _need(target is not None and target > 0, "target undefined or non-positive")
        return actual/target
    _need(actual is not None and actual > 0 and target is not None and target > 0, "actual or target undefined or non-positive")
    return target/actual
def o_b_kpi_trend(kpi_t, kpi_prev):
    _need(kpi_prev is not None and kpi_prev != 0, "previous KPI is zero or missing")
    return 100.0*(kpi_t - kpi_prev)/abs(kpi_prev)
def o_c_retention(customers_end, new_customers, customers_start):
    _need(customers_start is not None and customers_start > 0, "no opening customers")
    return 100.0*(customers_end - new_customers)/customers_start
def o_c_churn(customers_lost, customers_start):
    _need(customers_start is not None and customers_start > 0, "no opening customers")
    return 100.0*customers_lost/customers_start
def o_d_lead_conversion(converted_qualified_leads, qualified_leads):
    _need(qualified_leads is not None and qualified_leads > 0, "no qualified leads")
    return 100.0*converted_qualified_leads/qualified_leads
def o_d_win_rate(closed_won, qualified_opportunities):
    _need(qualified_opportunities is not None and qualified_opportunities > 0, "no qualified opportunities")
    return 100.0*closed_won/qualified_opportunities
def o_e_on_time(on_time, total):
    _need(total is not None and total > 0, "no orders")
    return 100.0*on_time/total
def o_e_defect_rate(defective, total):
    _need(total is not None and total > 0, "no units")
    return 100.0*defective/total
def o_e_digital_success(successful, total):
    _need(total is not None and total > 0, "no requests")
    return 100.0*successful/total
def o_f_miss_rate(periods_missing, valid_periods):
    _need(valid_periods is not None and valid_periods > 0, "no valid scored periods")
    return 100.0*periods_missing/valid_periods

# ---- 03 Runway and funding
DAYS_PER_MONTH = 30.4369  # = 365.2425 / 12, rounded to 4 decimals (Gregorian mean month)
def r_a_net_burn(cash_outflows, operating_cash_inflows):
    return cash_outflows - operating_cash_inflows
def r_a_runway(available_cash, burns_last_three):
    _need(len(burns_last_three) == 3, "three completed months required")
    avg = sum(burns_last_three)/3.0
    _need(avg > 0, "average net burn <= 0: no finite constant-burn runway")
    return available_cash/avg
def r_b_burn_trend(burn_m, burn_prev):
    _need(burn_prev is not None and burn_prev != 0, "previous burn is zero or missing")
    return 100.0*(burn_m - burn_prev)/abs(burn_prev)
def r_c_days_to_need(need_date, assessment_date):
    return (need_date - assessment_date).days
def r_c_months_to_need(need_date, assessment_date):
    return r_c_days_to_need(need_date, assessment_date)/DAYS_PER_MONTH
def r_d_funding_gap(cash_required, available_resources):
    return cash_required - available_resources
def r_d_gap_ratio(cash_required, available_resources):
    _need(cash_required is not None and cash_required > 0, "required cash zero or missing")
    return 100.0*(cash_required - available_resources)/cash_required
def r_e_external_dependency(external_required, total_required):
    _need(total_required is not None and total_required > 0, "total required funding <= 0")
    return 100.0*external_required/total_required
def r_f_progress(committed_capital, target_raise):
    _need(target_raise is not None and target_raise > 0, "no raise target")
    return 100.0*committed_capital/target_raise
def r_f_days_remaining(need_date, assessment_date):
    return (need_date - assessment_date).days

# ---- 04 Market and country
def m_a_cagr(size_end, size_start, years):
    _need(size_start is not None and size_start > 0 and years is not None and years > 0, "start size <= 0 or no interval")
    return 100.0*((size_end/size_start)**(1.0/years) - 1.0)
def m_b_country_rating(provider, country, as_of, grade, outlook=None):
    """Categorical lookup. No arithmetic raw ratio exists."""
    return dict(provider=provider, country=country, as_of=as_of, grade=grade, outlook=outlook)
def m_c_fx_change(fx_t, fx_prev):
    """FX quoted as local-currency units per 1 unit of base currency; positive = local depreciation."""
    _need(fx_prev is not None and fx_prev > 0, "prior rate missing")
    return 100.0*(fx_t - fx_prev)/fx_prev

WEIGHTS = {"Financial": dict(A=25, B=20, C=25, D=20, E=10), "Operational": dict(A=25, B=20, C=20, D=15, E=10, F=10),
           "Runway": dict(A=30, B=10, C=15, D=20, E=15, F=10), "Market": dict(A=40, B=35, C=25)}
