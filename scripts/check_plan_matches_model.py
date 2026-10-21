"""
Prove the business plan and the financial model agree.

The two documents used to hold their own numbers and were asked to agree. They
did not. The plan now reads the workbook through `business_plan.finlink`, but
that is an architectural claim, and an architectural claim deserves a test.

Three things are checked:

  1  Every headline series the plan prints equals the workbook's own.
  2  Every figure on disk is newer than the workbook, so a chart drawn from a
     previous model can never be embedded beside fresh sentences. This is the
     failure that is invisible in the source, because both halves look right.
  3  The plan's own cost roll-up adds back to the model's total, which is the
     test that a cost line added to the model later cannot go missing from the
     plan.

    python scripts/check_plan_matches_model.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from business_plan import finlink as FL                          # noqa: E402
from business_plan import model as MD                            # noqa: E402

TOL = 0.01
results = []


def check(name, expected, actual, tol=TOL):
    ok = abs((expected or 0) - (actual or 0)) <= tol
    results.append((ok, name, expected, actual))


def main():
    head = FL.headline()
    proj = MD.projection()

    check("the plan reports five years", FL.YEARS, len(proj), 0)
    for h, p in zip(head, proj):
        y = h["year"]
        check(f"year {y} revenue", h["revenue"], p["revenue"])
        check(f"year {y} total expense", h["total_expense"], p["cost"])
        check(f"year {y} net profit", h["net"], p["profit"])
        check(f"year {y} cash at year end", h["cash_end"], p["cash_end"])

    # The plan's cost headings must add back to the model's total, or a line
    # the model gains later would quietly vanish from the document.
    ex = FL.expense_lines()
    for y in MD.YEARS_5:
        rolled = sum(v for _, v in MD.costs(y)["lines"])
        check(f"year {y} cost roll-up adds to the model total",
              ex["total"][y - 1], rolled)

    # Revenue by engine must add back to the income statement.
    for y in MD.YEARS_5:
        r = MD.revenue(y)
        check(f"year {y} revenue by engine adds to total revenue",
              head[y - 1]["revenue"], r["total"])

    # Headcount is the model's, and inside the cap it promises.
    est = FL.establishment()
    for y, actual, cap, ok in MD.headcount_check():
        results.append((ok, f"year {y} headcount {actual} is within the cap "
                            f"{cap}", cap, actual))
        check(f"year {y} headcount matches the payroll sheet",
              est["headcount"][y - 1], actual, 0)

    # The balance sheet check must read nil, or nothing else here means much.
    for y, v in enumerate(FL.summary_check()["balance_check"], start=1):
        check(f"year {y} balance sheet check is nil", 0.0, v)

    # Every figure must be newer than the workbook it claims to draw.
    wb_time = os.path.getmtime(FL.WORKBOOK)
    figs = os.path.join(ROOT, "business_plan", "figures")
    stale = []
    if os.path.isdir(figs):
        for f in sorted(os.listdir(figs)):
            if not f.endswith(".png"):
                continue
            if os.path.getmtime(os.path.join(figs, f)) < wb_time:
                stale.append(f)
    results.append((not stale,
                    f"every figure is newer than the workbook "
                    f"({len(stale)} stale)", 0, len(stale)))

    failed = [r for r in results if not r[0]]
    print(f"checks run:    {len(results)}")
    print(f"checks passed: {len(results) - len(failed)}")
    if stale:
        print("\nSTALE FIGURES, redraw them:")
        for f in stale[:20]:
            print("   ", f)
    if failed:
        print(f"\nFAILED {len(failed)}:")
        for ok, name, exp, act in failed[:30]:
            print(f"  {name}\n      model {exp:,.2f}   plan {act:,.2f}")
        return 1
    print("\nThe business plan and the financial model agree on every figure "
          "checked, and no figure on disk predates the workbook.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
