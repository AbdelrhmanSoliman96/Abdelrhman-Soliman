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

## v0.4 additions (research-driven flow)

- **Business models** (8): each changes what a conversion is and shifts the funnel (`assume(..., business_model="MARKETPLACE")`).
- **Researched ratings**: evidence from the agent's research replaces prior ratings (`rating_overrides={"c_fric": 5}`); label becomes `researched`.
- **Event size and reliability**: `event_inputs={"attendees": 38000, "icp_share": 0.12}` and per-row `reliability`.
- **Partner activation**: plan `signed_partners`; engine converts to active partners with ramp-up.
- **Awareness (halo) effect**: `forecast_detail(plan, halo=True)` adds cross-channel lift (capped, credited to the source channel, no double counting).
- 19 tests. Full description: `docs/Research_Driven_Channel_Assumptions_Flow.pdf`.

- Per-industry worked examples (28 industries x KSA, UAE, Egypt): `docs/Industry_Examples_KSA_UAE_Egypt_Step_by_Step.pdf`.
