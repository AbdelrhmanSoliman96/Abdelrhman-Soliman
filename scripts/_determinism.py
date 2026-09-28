"""
Make the generated .xlsx / .docx byte-reproducible.

Both formats are ZIP containers, and both bake wall-clock time into the output in
two places: the `docProps/core.xml` created/modified properties, and the mtime on
every ZIP entry. Neither carries information about the document's content, but both
make the file differ on every rebuild — which turns these committed deliverables
into permanent noise in `git status`.

`FIXED_TIMESTAMP` pins the document properties; `normalize_zip` rewrites the archive
with a constant entry timestamp. Together they make a rebuild from unchanged sources
produce a byte-identical file.
"""
import datetime
import os
import re
import shutil
import zipfile

# Arbitrary fixed point. 1980-01-01 is the earliest a ZIP entry can encode.
FIXED_TIMESTAMP = datetime.datetime(2024, 1, 1, 0, 0, 0)
FIXED_W3CDTF = "2024-01-01T00:00:00Z"
ZIP_DATE_TIME = (1980, 1, 1, 0, 0, 0)

# openpyxl stamps dcterms:modified at save time and ignores wb.properties.modified,
# so the value has to be pinned here, after the library is done with the file.
_DCTERMS = re.compile(
    rb"(<dcterms:(?:created|modified)\b[^>]*>)[^<]*(</dcterms:(?:created|modified)>)"
)


def _pin_core_props(data):
    return _DCTERMS.sub(rb"\g<1>" + FIXED_W3CDTF.encode() + rb"\g<2>", data)


def normalize_zip(path):
    """
    Rewrite `path` in place so a rebuild from unchanged sources is byte-identical:
    a constant timestamp on every ZIP entry, and fixed created/modified values in
    docProps/core.xml.
    """
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as src:
        infos = src.infolist()
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
            for info in infos:
                data = src.read(info.filename)
                if info.filename == "docProps/core.xml":
                    data = _pin_core_props(data)
                new = zipfile.ZipInfo(info.filename, date_time=ZIP_DATE_TIME)
                new.compress_type = info.compress_type
                new.external_attr = info.external_attr
                new.internal_attr = info.internal_attr
                new.create_system = info.create_system
                dst.writestr(new, data)
    shutil.move(tmp, path)
    os.utime(path, (FIXED_TIMESTAMP.timestamp(), FIXED_TIMESTAMP.timestamp()))
    return path
