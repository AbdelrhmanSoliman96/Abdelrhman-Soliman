# Build scripts

The Markdown files in `proposals/` are the source of truth. The Word and HTML
versions are generated from them — edit the Markdown, then regenerate.

```sh
# Word
python3 md2docx.py ../btakka-proposal.md            ../Btakka_Investment_Readiness_Proposal.docx "Proposal (1 of 2)"
python3 md2docx.py ../btakka-consulting-agreement.md ../Btakka_Consulting_Agreement.docx          "Consulting Agreement (2 of 2)" agreement

# HTML (published as Artifacts)
python3 build2.py
```

The trailing `agreement` argument switches on the designed title page in
`coverpage.py`: the Markdown cover block is skipped and replaced with a
typeset title page, and the reference block is written into Word's
first-page footer so it anchors to the bottom margin rather than relying
on a guessed run of blank paragraphs.

Requires `python-docx` and `markdown`.
