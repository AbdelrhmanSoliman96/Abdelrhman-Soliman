# -*- coding: utf-8 -*-
"""Small SVG chart kit for an RTL Arabic print report."""
import json, math

INK, INK2, MUTE, GRID, SURF = "#16212C", "#4A5561", "#7C8691", "#E3E6EA", "#FFFFFF"
NAVY, COPPER = "#12304A", "#C97A1E"
S1, S2, S3, S4 = "#2A6DB0", "#C97A1E", "#1E9A84", "#B0486A"
SER = [S1, S2, S3, S4]
GOOD, WARN, BAD = "#2E7D4F", "#C98A00", "#B23A3A"


def num(v, d=0):
    if v is None: return ""
    s = f"{abs(v):,.{d}f}"
    return f"({s})" if v < 0 else s


def T(x, y, s, a="m", size=9, fill=INK2, w=400, extra=""):
    anchor = {"m": "middle", "r": "start", "l": "end"}[a]
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" fill="{fill}" font-weight="{w}" {extra}>{s}</text>'


def svg(w, h, body, cls=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" class="chart {cls}" '
            f'style="direction:rtl" font-family="IBM Plex Sans Arabic, sans-serif">{body}</svg>')


def nice_max(v):
    if v <= 0: return 1
    e = 10 ** math.floor(math.log10(v))
    for m in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if v <= m * e: return m * e
    return 10 * e


def rbar(x, y, w, h, fill, r=3):
    """bar with rounded top (or bottom when h negative-drawn)"""
    if h < r * 2: r = max(0, h / 2)
    return (f'<path d="M{x:.1f},{y + h:.1f} L{x:.1f},{y + r:.1f} Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f} '
            f'L{x + w - r:.1f},{y:.1f} Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + r:.1f} L{x + w:.1f},{y + h:.1f} Z" fill="{fill}"/>')


def legend(items, x, y, gap=110):
    out = ""
    for i, (lab, col) in enumerate(items):
        xx = x - i * gap
        out += f'<rect x="{xx - 10}" y="{y - 8}" width="10" height="10" rx="2" fill="{col}"/>' + T(xx - 15, y + 1, lab, "r", 8.5)
    return out


def bars(cats, series, w=640, h=300, unit="", d=1, stacked=False, labels=True, ymax=None, colors=None, legend_gap=130, neg=False, total_labels=False):
    """series: list of (name, values). RTL: first category drawn on the right."""
    colors = colors or SER
    ml, mr, mt, mb = 20, 46, 34 if len(series) > 1 else 16, 34
    pw, ph = w - ml - mr, h - mt - mb
    n = len(cats)
    if stacked:
        tops = [sum(max(s[1][i], 0) for s in series) for i in range(n)]
        lows = [sum(min(s[1][i], 0) for s in series) for i in range(n)]
    else:
        tops = [max(s[1][i] for s in series) for i in range(n)]
        lows = [min(s[1][i] for s in series) for i in range(n)]
    hi = ymax or nice_max(max(tops) * 1.08)
    lo = -nice_max(-min(lows) * 1.15) if min(lows) < 0 else 0
    sy = lambda v: mt + ph * (hi - v) / (hi - lo)
    out = ""
    ticks = 4
    for i in range(ticks + 1):
        v = lo + (hi - lo) * i / ticks
        out += f'<line x1="{ml}" x2="{w - mr}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" stroke="{GRID}" stroke-width="1"/>'
        out += T(w - mr + 6, sy(v) + 3, num(v, d if (hi - lo) < 20 else 0), "l", 8, MUTE)
    if lo < 0:
        out += f'<line x1="{ml}" x2="{w - mr}" y1="{sy(0):.1f}" y2="{sy(0):.1f}" stroke="{MUTE}" stroke-width="1"/>'
    band = pw / n
    ltr = all(any(ch.isdigit() for ch in c) for c in cats)
    for i, c in enumerate(cats):
        cx = (ml + band * (i + .5)) if ltr else (w - mr - band * (i + .5))
        out += T(cx, h - mb + 16, c, "m", 8.5, INK2)
        if stacked:
            bw = min(46, band * .55); accp = 0; accn = 0
            for k, (_, vals) in enumerate(series):
                v = vals[i]
                if v >= 0:
                    y0, y1 = sy(accp + v), sy(accp); accp += v
                else:
                    y0, y1 = sy(accn), sy(accn + v); accn += v
                hh = max(0, y1 - y0 - 1.5)
                last = (k == len(series) - 1)
                out += rbar(cx - bw / 2, y0, bw, hh, colors[k], 3 if last else 0)
            if total_labels:
                out += T(cx, sy(accp) - 5, num(accp, d), "m", 8.5, INK, 600)
        else:
            m = len(series); bw = min(40, band * .7 / m)
            for k, (_, vals) in enumerate(series):
                v = vals[i]
                bx = cx + ((k - m / 2) if ltr else (m / 2 - k - 1)) * (bw + 2) + 1
                if v >= 0:
                    out += rbar(bx, sy(v), bw, sy(0) - sy(v), colors[k])
                    if labels: out += T(bx + bw / 2, sy(v) - 5, num(v, d), "m", 8.5, INK, 600)
                else:
                    out += f'<rect x="{bx:.1f}" y="{sy(0):.1f}" width="{bw:.1f}" height="{sy(v) - sy(0):.1f}" fill="{colors[k]}" rx="2"/>'
                    if labels: out += T(bx + bw / 2, sy(v) + 12, num(v, d), "m", 8.5, INK, 600)
    if len(series) > 1:
        out += legend([(s[0], colors[k]) for k, s in enumerate(series)], w - mr, 14, legend_gap)
    if unit: out += T(ml, 14, unit, "l", 8, MUTE)
    return svg(w, h, out)


def lines(cats, series, w=640, h=290, unit="", d=1, ymin=0, ymax=None, colors=None, legend_gap=150, end_labels=True, dashed=()):
    colors = colors or SER
    ml, mr, mt, mb = 28, 46, 34, 32
    pw, ph = w - ml - mr, h - mt - mb
    hi = ymax or nice_max(max(max(s[1]) for s in series) * 1.08)
    lo = ymin
    sy = lambda v: mt + ph * (hi - v) / (hi - lo)
    n = len(cats)
    sx = lambda i: ml + 18 + (pw - 36) * i / (n - 1)
    out = ""
    for i in range(5):
        v = lo + (hi - lo) * i / 4
        out += f'<line x1="{ml}" x2="{w - mr}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" stroke="{GRID}"/>' + T(w - mr + 6, sy(v) + 3, num(v, d), "l", 8, MUTE)
    for i, c in enumerate(cats): out += T(sx(i), h - mb + 16, c, "m", 8.5)
    for k, (name, vals) in enumerate(series):
        pts = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(vals))
        dash = ' stroke-dasharray="5 4"' if k in dashed else ''
        out += f'<polyline points="{pts}" fill="none" stroke="{colors[k]}" stroke-width="2" stroke-linejoin="round"{dash}/>'
        for i, v in enumerate(vals):
            out += f'<circle cx="{sx(i):.1f}" cy="{sy(v):.1f}" r="3.5" fill="{colors[k]}" stroke="#fff" stroke-width="1.5"/>'
        if end_labels:
            for i in (0, n - 1):
                out += T(sx(i), sy(vals[i]) - 8, num(vals[i], d), "m", 8.5, INK, 600)
    out += legend([(s[0], colors[k]) for k, s in enumerate(series)], w - mr, 14, legend_gap)
    if unit: out += T(ml, 14, unit, "l", 8, MUTE)
    return svg(w, h, out)


def hbars(items, w=640, unit="", d=0, color=S1, label_w=190, row=30, colors=None, vmax=None, suffix=""):
    """items: list of (label, value). Labels on the right (RTL)."""
    h = row * len(items) + 26
    hi = vmax or max(v for _, v in items) * 1.15
    x0 = w - label_w; pw = x0 - 60
    out = ""
    for i, (lab, v) in enumerate(items):
        y = 10 + i * row
        bw = pw * v / hi
        col = colors[i] if colors else color
        out += T(w - 4, y + row / 2 + 1, lab, "r", 9, INK)
        out += f'<rect x="{x0 - bw:.1f}" y="{y + 5}" width="{bw:.1f}" height="{row - 12}" rx="3" fill="{col}"/>'
        out += T(x0 - bw - 6, y + row / 2 + 1, num(v, d) + suffix, "r", 9, INK, 600)
    out += f'<line x1="{x0}" x2="{x0}" y1="8" y2="{h - 16}" stroke="{MUTE}"/>'
    if unit: out += T(10, h - 4, unit, "l", 8, MUTE)
    return svg(w, h, out)


def ranges(items, w=640, unit="", label_w=200, row=32, vmax=None, marks=None):
    """items: (label, lo, hi, color). range bars."""
    h = row * len(items) + 30
    hi = vmax or max(i[2] for i in items) * 1.12
    x0 = w - label_w; pw = x0 - 30
    sx = lambda v: x0 - pw * v / hi
    out = ""
    for i in range(5):
        v = hi * i / 4
        out += f'<line x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="6" y2="{h - 22}" stroke="{GRID}"/>' + T(sx(v), h - 8, num(v), "m", 8, MUTE)
    for i, (lab, a, b, col) in enumerate(items):
        y = 8 + i * row
        out += T(w - 4, y + row / 2 + 1, lab, "r", 9, INK)
        out += f'<rect x="{sx(b):.1f}" y="{y + 7}" width="{sx(a) - sx(b):.1f}" height="{row - 16}" rx="{(row - 16) / 2}" fill="{col}"/>'
        out += T(sx(b) - 6, y + row / 2 + 1, (f"{num(a)} - {num(b)}" if b > a * 1.05 else num(a)), "r", 8.5, INK, 600)
    if unit: out += T(w - 4, h - 8, unit, "r", 8, MUTE)
    return svg(w, h, out)


def waterfall(steps, w=640, h=300, d=1, unit=""):
    """steps: (label, value, kind) kind in 'total','delta'"""
    ml, mr, mt, mb = 16, 44, 18, 46
    pw, ph = w - ml - mr, h - mt - mb
    acc, tops = 0, []
    spans = []
    for lab, v, kind in steps:
        if kind == 'total': a, b = 0, v; acc = v
        else: a, b = acc, acc + v; acc += v
        spans.append((a, b))
    hi = nice_max(max(max(a, b) for a, b in spans) * 1.1); lo = min(0, min(min(a, b) for a, b in spans))
    if lo < 0: lo = -nice_max(-lo * 1.1)
    sy = lambda v: mt + ph * (hi - v) / (hi - lo)
    out = ""
    for i in range(5):
        v = lo + (hi - lo) * i / 4
        out += f'<line x1="{ml}" x2="{w - mr}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" stroke="{GRID}"/>' + T(w - mr + 6, sy(v) + 3, num(v, d), "l", 8, MUTE)
    band = pw / len(steps); bw = min(44, band * .6)
    for i, ((lab, v, kind), (a, b)) in enumerate(zip(steps, spans)):
        cx = w - mr - band * (i + .5)
        col = NAVY if kind == 'total' else (S3 if v >= 0 else S4)
        y0, y1 = sy(max(a, b)), sy(min(a, b))
        out += f'<rect x="{cx - bw / 2:.1f}" y="{y0:.1f}" width="{bw:.1f}" height="{max(1.5, y1 - y0):.1f}" rx="2.5" fill="{col}"/>'
        out += T(cx, y0 - 5, num(v, d), "m", 8.5, INK, 600)
        words = lab.split("|")
        for j, wd in enumerate(words): out += T(cx, h - mb + 15 + j * 12, wd, "m", 8, INK2)
        if i < len(steps) - 1:
            nx = w - mr - band * (i + 1.5)
            out += f'<line x1="{cx - bw / 2:.1f}" x2="{nx + bw / 2:.1f}" y1="{sy(b):.1f}" y2="{sy(b):.1f}" stroke="{MUTE}" stroke-dasharray="2 2"/>'
    if unit: out += T(ml, 12, unit, "l", 8, MUTE)
    return svg(w, h, out)


def tornado(items, base, w=640, d=1, unit="", row=30, label_w=200):
    """items: (label, low_val, high_val) outcome values; sorted by spread."""
    items = sorted(items, key=lambda t: -abs(t[2] - t[1]))
    h = row * len(items) + 44
    lo = min(min(a, b) for _, a, b in items); hi = max(max(a, b) for _, a, b in items)
    pad = (hi - lo) * .16; lo -= pad; hi += pad
    x1 = w - label_w; x0 = 20
    sx = lambda v: x0 + 26 + (x1 - x0 - 52) * (v - lo) / (hi - lo)
    out = ""
    for i, (lab, a, b) in enumerate(items):
        y = 26 + i * row
        out += T(w - 4, y + row / 2 + 1, lab, "r", 9, INK)
        for v, col in ((a, S4), (b, S3)):
            xa, xb = sorted((sx(v), sx(base)))
            out += f'<rect x="{xa:.1f}" y="{y + 6}" width="{max(1, xb - xa):.1f}" height="{row - 13}" rx="2.5" fill="{col}"/>'
        out += T(sx(min(a, b)) - 5, y + row / 2 + 1, num(min(a, b), d), "r", 8.5, INK, 600)
        out += T(sx(max(a, b)) + 5, y + row / 2 + 1, num(max(a, b), d), "l", 8.5, INK, 600)
    out += f'<line x1="{sx(base):.1f}" x2="{sx(base):.1f}" y1="20" y2="{h - 18}" stroke="{INK}" stroke-width="1.2"/>'
    out += T(sx(base), h - 5, f"الحالة الأساسية: {num(base, d)}", "m", 8.5, INK, 600)
    out += legend([("أثر سلبي", S4), ("أثر إيجابي", S3)], w - 4, 12, 80)
    if unit: out += T(x0, 12, unit, "l", 8, MUTE)
    return svg(w, h, out)


def histogram(values, bins=28, w=640, h=280, mark0=True, unit="", pcts=None):
    lo, hi = min(values), max(values)
    step = (hi - lo) / bins
    counts = [0] * bins
    for v in values: counts[min(bins - 1, int((v - lo) / step))] += 1
    ml, mr, mt, mb = 20, 20, 22, 34
    pw, ph = w - ml - mr, h - mt - mb
    cm = max(counts)
    sx = lambda v: ml + pw * (v - lo) / (hi - lo)
    out = ""
    for i, c in enumerate(counts):
        a = lo + i * step
        col = S4 if a + step / 2 < 0 else S1
        bh = ph * c / cm
        out += f'<rect x="{sx(a) + 1:.1f}" y="{mt + ph - bh:.1f}" width="{pw / bins - 2:.1f}" height="{bh:.1f}" rx="1.5" fill="{col}"/>'
    out += f'<line x1="{ml}" x2="{w - mr}" y1="{mt + ph}" y2="{mt + ph}" stroke="{MUTE}"/>'
    for i in range(6):
        v = lo + (hi - lo) * i / 5
        out += T(sx(v), h - mb + 15, num(v, 0), "m", 8, MUTE)
    if mark0 and lo < 0 < hi:
        out += f'<line x1="{sx(0):.1f}" x2="{sx(0):.1f}" y1="{mt - 4}" y2="{mt + ph}" stroke="{INK}" stroke-dasharray="4 3"/>' + T(sx(0), mt - 8, "صفر", "m", 8.5, INK, 600)
    for lab, v in (pcts or []):
        out += f'<line x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="{mt + 10}" y2="{mt + ph}" stroke="{COPPER}" stroke-width="1.5"/>' + T(sx(v), mt + 6, lab, "m", 8.5, INK, 600)
    if unit: out += T(w - mr, h - 4, unit, "r", 8, MUTE)
    return svg(w, h, out)


def geo_path(geom, proj):
    d = ""
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    for poly in polys:
        for ring in poly:
            pts = [proj(lon, lat) for lon, lat in ring[::3]]
            d += "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z "
    return d
