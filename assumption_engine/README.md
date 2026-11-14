# Offline channel assumption engine (v0.1)

Turns (country, industry, deal type, channel) into funnel assumptions for the financial-model agent:
leads per activity, qualified / opportunity / win rates, sales-cycle days, partner ramp-up, P10-P90 range, drivers and provenance.

**All base funnels and 1-5 factor ratings in `config/` are expert priors, not market statistics.** Review them with your regional BD team and
replace them with CRM actuals (see `blend` via `assume(..., actuals=...)`). Full explanation: `docs/Assumption_Engine_Developer_Build_Guide.pdf (build steps) and docs/Offline_Channel_Assumption_Engine_Flow_and_Logic.pdf (overview)`.

```bash
python3 engine.py assume "Saudi Arabia" "E-Commerce" B2B_ENT PAR_STRATEGIC   # one combination
python3 engine.py matrix > data/matrix_base.csv                              # every valid combination
python3 -I -m unittest discover -s tests                                     # 11 tests
```

Scope: the 20 countries in `data/countries_list.csv` and 28 industries in `data/industries_list.csv`. Gated countries
(Libya, Iran, Syria, Sudan, Yemen) return `REVIEW_REQUIRED` and no numbers until compliance review.
