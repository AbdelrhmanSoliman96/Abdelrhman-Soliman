"""
Find figures whose content falls outside the canvas they are saved in.

Every figure is placed in the document at the same printed width, so each one
is saved at a fixed canvas size and a point size chosen in `charts.py` is the
point size the reader sees. That only works if nothing is drawn outside the
canvas: with a fixed bounding box, anything that overflows is silently
clipped rather than silently rescued.

This measures, for each figure, the tight bounding box matplotlib would have
used and compares it with the canvas. Overflow on any edge is a clip. It also
reports figures that waste a lot of vertical space, because a short figure
stretched to the text column is a figure with oversized type.

    python scripts/check_figure_fit.py
"""
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

warnings.filterwarnings("ignore")

import matplotlib                                                # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                  # noqa: E402

from business_plan import charts as C                            # noqa: E402

TOL = 0.015          # inches; below this is rounding, not overflow


def main():
    saved = C._save
    captured = {}

    def capture(fig, name):
        # Apply exactly what _save applies, or the measurement describes a
        # figure that is never written: the constrained engine is what makes
        # room for long tick labels and for legends under the axes.
        if not getattr(fig, "_startpad_canvas", False):
            try:
                fig.set_layout_engine("constrained")
            except Exception:
                fig.tight_layout()
        fig.canvas.draw()
        bb = fig.get_tightbbox(fig.canvas.get_renderer())
        w, h = fig.get_size_inches()
        captured[name] = (bb.x0, bb.y0, bb.x1, bb.y1, w, h,
                          getattr(fig, "_startpad_canvas", False))
        return saved(fig, name)

    C._save = capture
    for fn in C.ALL:
        fn()
    C._save = saved

    bad, waste = [], []
    for name, (x0, y0, x1, y1, w, h, is_canvas) in sorted(captured.items()):
        over = {}
        if x0 < -TOL:
            over["left"] = -x0
        if y0 < -TOL:
            over["bottom"] = -y0
        if x1 > w + TOL:
            over["right"] = x1 - w
        if y1 > h + TOL:
            over["top"] = y1 - h
        if over:
            bad.append((name, w, h, over))
        elif is_canvas:
            slack = h - (y1 - y0)
            if slack > 0.45:
                waste.append((name, h, slack))

    print(f"figures checked: {len(captured)}")
    print(f"\nCONTENT OUTSIDE THE CANVAS, WHICH WILL BE CLIPPED: {len(bad)}")
    for name, w, h, over in bad:
        edges = ", ".join(f"{k} by {v:.2f}in" for k, v in sorted(over.items()))
        print(f"  {name:28s} canvas {w:.2f}x{h:.2f}in   {edges}")

    print(f"\nHAND-DRAWN CANVASES WITH LARGE EMPTY MARGINS: {len(waste)}")
    for name, h, slack in waste:
        print(f"  {name:28s} canvas height {h:.2f}in, {slack:.2f}in unused")

    if bad:
        print("\nFix by wrapping the overflowing text, shrinking the element, "
              "or growing the canvas.")
        return 1
    print("\nEvery figure fits inside the canvas it is saved in.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
