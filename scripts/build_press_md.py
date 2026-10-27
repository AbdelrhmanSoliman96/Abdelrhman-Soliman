# -*- coding: utf-8 -*-
"""
Export the press release to Markdown, one file per language.

This is the copy-paste format: what gets pasted into a wire submission form, an
email to a journalist, or a LinkedIn post. Plain text with light Markdown only —
wire services strip anything richer.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from press.release import NOTES_SOURCES, VERSIONS  # noqa: E402


def render(v):
    out = ["**%s**" % v["kicker"], "", "# %s" % v["headline"], "",
           "### %s" % v["subhead"], "", "**%s**" % v["dateline"], ""]
    for block in v["blocks"]:
        kind = block[0]
        if kind == "h":
            out += ["## %s" % block[1], ""]
        elif kind == "p":
            out += [block[1], ""]
        elif kind == "b":
            out += ["- %s" % i for i in block[1]] + [""]
        elif kind == "q":
            out += ["> “%s”" % block[1], ">", "> **— %s**" % block[2], ""]
        elif kind == "kv":
            out += ["**%s:** %s" % (k, val) for k, val in block[1]] + [""]
    out += ["", "###", ""]
    return "\n".join(out).rstrip() + "\n"


def build(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    written = []
    for v in VERSIONS:
        path = os.path.join(out_dir, "startpad_leap_launch_%s.md" % v["lang"])
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(render(v))
        written.append(path)

    path = os.path.join(out_dir, "fact_check_sources.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("# Fact-check sources\n\n"
                 "Every figure in the release came from these pages during drafting, "
                 "not from memory. Re-check them against the live pages before "
                 "distribution.\n\n")
        fh.write("\n".join("- %s — <%s>" % (lbl, url) for lbl, url in NOTES_SOURCES))
        fh.write("\n")
    written.append(path)
    return written


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "press"
    for p in build(target):
        print("wrote", p, os.path.getsize(p), "bytes")
