# Fonts

`PlusJakartaSans-Variable.woff2` — latin subset, weights 300–800 in one variable file.
Licensed under the SIL Open Font License 1.1, which permits embedding in documents.

## Why it is here

The brand specifies **Satoshi** for Latin. Satoshi is distributed by Fontshare, which
this build environment cannot reach, so the PDFs in `output/resources/` embed Plus
Jakarta Sans — the closest freely embeddable geometric grotesque, matching Satoshi on
the two properties the guidelines call out: a high x-height and closed apertures.

`whitepapers/brand.py` names Satoshi first in every font stack. Drop a Satoshi
`.woff2` into this folder, point `SATOSHI_FILE` at it, and rebuild: the documents pick
up the real face with no other change.
