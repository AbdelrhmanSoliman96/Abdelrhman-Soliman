"""
The resource library.

Sixteen documents in three series, all rendered by the same pipeline:

* **Toolkits** (5) — a founder fills them in. Worksheets, logs, decisions.
* **Whitepapers** (3) — each explains one thing, with no worksheet.
* **Reports** (8) — each takes one framework from the StartPad brand book and reads
  it as an operating tool for founders rather than as a design rule. Every one names
  the book on the page it argues from.

Every document is a plain dictionary of metadata plus a list of content blocks, so
the words live apart from the design and either can change without touching the other.
"""

from . import tk01_readiness, tk02_evidence, tk03_manual_mvp, tk04_demand, tk05_file
from . import wp01_gap, wp02_sizing, wp03_idea
from . import (r01_requirement_gap_route, r02_truth_readiness_proof, r03_four_words,
               r04_progress_is_a_colour, r05_believed_or_shared, r06_one_idea_only,
               r07_speaks_the_way_they_speak, r08_warm_candour)

LIBRARY = [
    # whitepapers and toolkits, in the order a founder meets them
    wp01_gap.DOC,
    tk01_readiness.DOC,
    tk02_evidence.DOC,
    wp02_sizing.DOC,
    tk03_manual_mvp.DOC,
    tk04_demand.DOC,
    tk05_file.DOC,
    wp03_idea.DOC,
    # reports, in the order the frameworks appear in the book
    r01_requirement_gap_route.DOC,
    r02_truth_readiness_proof.DOC,
    r03_four_words.DOC,
    r08_warm_candour.DOC,
    r06_one_idea_only.DOC,
    r04_progress_is_a_colour.DOC,
    r05_believed_or_shared.DOC,
    r07_speaks_the_way_they_speak.DOC,
]

TOOLKITS = [d for d in LIBRARY if d["kind"] == "toolkit"]
WHITEPAPERS = [d for d in LIBRARY if d["kind"] == "whitepaper"]
REPORTS = [d for d in LIBRARY if d["kind"] == "report"]
