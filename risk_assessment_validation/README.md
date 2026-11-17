# Risk methodology validation harness

Reference implementation used by `docs/Angelsta_Risk_Methodology_Validation_Review.pdf`.

- `raw_metrics.py`: the 20 raw metrics of the Angelsta Raw Metric Methodology (review edition, 12 Nov 2026), exactly as written. Invalid denominators raise `NonComputable` (never zero).
- `proposed_metrics.py`: supplementary equations and new-module equations proposed in the review. None replaces a raw metric; all need methodology approval.
- `tests/test_metrics.py`: 21 tests (`python3 -I -m unittest discover -s risk_assessment_validation/tests`).
- `experiments.py`: simulations on synthetic or illustrative data; writes `results.json`.
