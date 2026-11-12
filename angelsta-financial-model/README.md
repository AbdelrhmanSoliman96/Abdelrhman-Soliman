# Angelsta financial model, 2027 to 2031

| File | What it is |
|---|---|
| `Angelsta_Financial_Model_2027-2031_v1.0.xlsx` | 28-sheet operational model in the Btakka layout: monthly for 60 months, three statements, funding, valuation, stress tests |
| `Angelsta_Pricing_Strategy.docx` | Freemium pricing strategy for founders and investors, with market research and sources; the model's pricing inputs come from it |
| `build/` | Python scripts that generate both files (`python build.py out.xlsx`, `python make_pricing_doc.py out.docx`) |

## Base case headlines (USD)

| | 2027 | 2028 | 2029 | 2030 | 2031 |
|---|---|---|---|---|---|
| Revenue | 36k | 320k | 1.21m | 3.12m | 6.56m |
| ARR at year end | 91k | 537k | 1.77m | 4.20m | 8.38m |
| EBITDA | (300k) | (646k) | (485k) | 655k | 3.18m |
| Paying accounts | 61 | 285 | 800 | 1,762 | 3,356 |
| Employees | 17 | 32 | 46 | 58 | 67 |

- **Pre-seed ask: USD 450k**, built by the model from year-one cash cost (USD 366k), less opening cash, plus a 3-month buffer.
- Pre-money USD 2.4m (weighted across five valuation methods), so the round sells 15.8%.
- The model sizes a seed round of USD 700k in month 15. EBITDA turns positive in month 36, and no Series A is required in the base case.
- Every check on the Summary sheet reads nil, including the balance sheet, payroll, revenue and use of funds.

The opening position (section 2 of Assumption Setting) holds placeholders until the 31 December 2026 figures are confirmed.
