"""
Emit CSVs shaped for direct import into the Startpad Postgres schema.

  tools.csv             -> a `tools` table (one row per tool)
  mission_tools.csv     -> a `mission_tools` join table (mission_id, tool_slug, role)
  mission_resources.csv -> a `mission_resources` table
  founder_toolkit.csv   -> shelf assignments for tools outside the mission flow

Slugs are deterministic so re-running the build produces stable keys.
"""
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from startpad.missions import ALWAYS_AVAILABLE, MAPPING, MISSIONS  # noqa: E402
from startpad.resources import BY_MISSION, FOUNDATION, FUNDRAISING  # noqa: E402
from startpad.tools import CATEGORY_TAB, TOOLS, TOOL_BY_NAME  # noqa: E402


def slug(name):
    s = name.lower()
    s = s.replace("&", " and ").replace("/", " ").replace("—", " ").replace("·", " ")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)


def write(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    return path, len(rows)


def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    written = []

    # tools.csv
    rows = []
    for name, cat, does, ref in TOOLS:
        rows.append([slug(name), name, cat, does, ref, CATEGORY_TAB[cat]])
    written.append(write(os.path.join(outdir, "tools.csv"),
                         ["tool_slug", "tool_name", "category", "description",
                          "framework_reference", "source_tab"], rows))

    # mission_tools.csv
    rows = []
    for m in MISSIONS:
        block = MAPPING[m["id"]]
        for role in ("core", "supporting", "stretch"):
            for order, (tool, why, feeds) in enumerate(block.get(role, []), start=1):
                rows.append([m["id"], m["title"], slug(tool), tool, role, order, why, feeds])
    written.append(write(os.path.join(outdir, "mission_tools.csv"),
                         ["mission_id", "mission_title", "tool_slug", "tool_name",
                          "role", "sort_order", "rationale", "feeds_question"], rows))

    # mission_resources.csv
    rows = []

    def add(mid, mlabel, items):
        for order, (kind, title, source, url, length, lang, why) in enumerate(items, start=1):
            rows.append([mid, mlabel, order, kind, title, source, url, length, lang, why])

    add("", "foundation", FOUNDATION)
    for m in MISSIONS:
        add(m["id"], m["title"], BY_MISSION.get(m["id"], []))
    add("16", "Raise Your Round (proposed)", FUNDRAISING)
    written.append(write(os.path.join(outdir, "mission_resources.csv"),
                         ["mission_id", "mission_title", "sort_order", "resource_type",
                          "title", "source", "url", "length", "language", "rationale"], rows))

    # founder_toolkit.csv
    rows = []
    for shelf, items in ALWAYS_AVAILABLE.items():
        for order, (tool, why) in enumerate(items, start=1):
            _, cat, _, _ = TOOL_BY_NAME[tool]
            rows.append([shelf, order, slug(tool), tool, cat, why])
    written.append(write(os.path.join(outdir, "founder_toolkit.csv"),
                         ["shelf", "sort_order", "tool_slug", "tool_name",
                          "category", "rationale"], rows))
    return written


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output/seed"
    for path, n in build(out):
        print(f"wrote {path}  ({n} rows)")
