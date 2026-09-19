"""
The resource library.

Eight documents: five guided toolkits a founder fills in, and three mini whitepapers
that explain one thing each. Every document is a plain dictionary of metadata plus a
list of content blocks, so the words live apart from the design and either can change
without touching the other.
"""

from . import tk01_readiness, tk02_evidence, tk03_manual_mvp, tk04_demand, tk05_file
from . import wp01_gap, wp02_sizing, wp03_idea

LIBRARY = [
    wp01_gap.DOC,
    tk01_readiness.DOC,
    tk02_evidence.DOC,
    wp02_sizing.DOC,
    tk03_manual_mvp.DOC,
    tk04_demand.DOC,
    tk05_file.DOC,
    wp03_idea.DOC,
]

TOOLKITS = [d for d in LIBRARY if d["kind"] == "toolkit"]
WHITEPAPERS = [d for d in LIBRARY if d["kind"] == "whitepaper"]
