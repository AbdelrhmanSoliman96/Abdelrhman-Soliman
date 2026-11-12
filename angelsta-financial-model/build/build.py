import sys
import openpyxl
from xl import resolve_all, BRAND
from model_inputs import build_inputs
from model_process import build_payroll, build_acquisitions, build_gtm, build_revenue, build_total_revenue
from model_output import (build_capex, build_da, build_expenses, build_income, build_cashflow, build_balance,
                          build_indicators, build_funding)
from model_analysis import (build_bep, build_pb, build_sens, build_stress, build_valuation, build_exit, build_summary,
                            build_market, build_actuals, build_divider, build_cover, CONTENTS)

ORDER = ["Cover", "Summary", "Market Research", "Input>>", "Assumption Setting", "Capital Expenditure", "Actuals", "Process>>",
         "Acquisitions", "GTM Capacity and Timing", "Revenue Streams", "Total Revenue", "Payroll", "Depreciation and Amortization",
         "Expenses", "Output>>", "Income Statement", "Balance Sheet", "Cash Flow Statement", "Financial Indicators",
         "Funding and Use of Funds", "Analysis>>", "BEP Analysis", "PB Analysis", "Sensitivity", "Stress Test", "Exit Angel and VC", "Valuation"]

wb = openpyxl.Workbook()
wb.remove(wb.active)
W = {n: wb.create_sheet(n) for n in ORDER}
REG = {}
A = build_inputs(W["Assumption Setting"])
REG["Assumption Setting"] = A.k
build_payroll(W["Payroll"], A, REG)
build_acquisitions(W["Acquisitions"], A, REG)
build_gtm(W["GTM Capacity and Timing"], A, REG)
build_revenue(W["Revenue Streams"], A, REG)
build_total_revenue(W["Total Revenue"], A, REG)
build_capex(W["Capital Expenditure"], A, REG)
build_da(W["Depreciation and Amortization"], A, REG)
build_expenses(W["Expenses"], A, REG)
build_income(W["Income Statement"], A, REG)
build_cashflow(W["Cash Flow Statement"], A, REG)
build_balance(W["Balance Sheet"], A, REG)
build_indicators(W["Financial Indicators"], A, REG)
build_funding(W["Funding and Use of Funds"], A, REG)
build_bep(W["BEP Analysis"], A, REG)
build_pb(W["PB Analysis"], A, REG)
build_sens(W["Sensitivity"], A, REG)
build_stress(W["Stress Test"], A, REG)
build_valuation(W["Valuation"], A, REG)
build_exit(W["Exit Angel and VC"], A, REG)
build_summary(W["Summary"], A, REG)
build_market(W["Market Research"], A, REG)
build_actuals(W["Actuals"], A, REG)
grp = dict(CONTENTS)
for d, key in [("Input>>", "Input"), ("Process>>", "Process"), ("Output>>", "Output"), ("Analysis>>", "Analysis")]:
    build_divider(W[d], key, grp[key])
build_cover(W["Cover"], A, REG)
for n in ["Summary"]:
    W[n].sheet_properties.tabColor = BRAND
resolve_all(wb, REG)
wb.calculation.fullCalcOnLoad = True
wb.save(sys.argv[1])
print("saved", sys.argv[1])
