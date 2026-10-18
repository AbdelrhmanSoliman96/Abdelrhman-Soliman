import markdown, re, pathlib, html as ihtml, sys

DOCS = {
 'proposal': dict(
    src='/home/user/Abdelrhman-Soliman/proposals/btakka-proposal.md',
    out='/home/user/Abdelrhman-Soliman/proposals/btakka-proposal.html',
    anchor='# THE ENGAGEMENT', end='*End of proposal.*',
    title='Btakka Engagement Proposal'),
 'agreement': dict(
    src='/home/user/Abdelrhman-Soliman/proposals/btakka-consulting-agreement.md',
    out='/home/user/Abdelrhman-Soliman/proposals/btakka-consulting-agreement.html',
    anchor='# CONSULTING AGREEMENT', end='@@NO-TRAILING-BLOCK@@',
    title='Btakka Consulting Agreement'),
}

def build(key):
    cfg = DOCS[key]
    raw = pathlib.Path(cfg['src']).read_text(encoding='utf-8')
    body_md = raw[raw.index(cfg['anchor']):].split(cfg['end'])[0].rstrip().rstrip('-').rstrip()
    body = markdown.markdown(body_md, extensions=['tables','attr_list','sane_lists'], output_format='html5')

    seen, toc = {}, []
    def slug(t):
        s = re.sub(r'<[^>]+>', '', t)
        s = re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()[:60] or 'section'
        n = seen.get(s, 0); seen[s] = n + 1
        return s if n == 0 else f'{s}-{n}'
    def head_repl(m):
        lvl, attrs, text = m.group(1), m.group(2), m.group(3)
        sid = slug(text)
        if lvl in ('1','2'):
            toc.append((lvl, sid, re.sub(r'<[^>]+>', '', text)))
        return f'<h{lvl} id="{sid}"{attrs}>{text}</h{lvl}>'
    body = re.sub(r'<h([12345])([^>]*)>(.*?)</h\1>', head_repl, body, flags=re.S)

    body = body.replace('<table>', '<div class="tw"><table>').replace('</table>', '</table></div>')

    def cell_chip(m):
        v = m.group(1).strip()
        key2 = {'C':'own-c','B':'own-b','C+B':'own-cb'}.get(v)
        return f'<td><span class="own {key2}">{v}</span></td>' if key2 else m.group(0)
    body = re.sub(r'<td>(?:<strong>)?(C\+B|C|B)(?:</strong>)?</td>', cell_chip, body)

    def prio_chip(m):
        v, tail = m.group(1), m.group(2)
        cls = {'High':'p-hi','Medium':'p-md','Low':'p-lo'}[v]
        opt = '<span class="opt">optional</span>' if 'optional' in tail else ''
        return f'<td><span class="prio {cls}">{v}</span>{opt}</td>'
    body = re.sub(r'<td>(High|Medium|Low)((?:\s*<em>\(optional\)</em>)?)</td>', prio_chip, body)
    body = body.replace('<td>☐</td>', '<td class="cbx">☐</td>')
    body = re.sub(r'\[([^\[\]<>]{0,55})\]', lambda m: f'<span class="slot">[{m.group(1)}]</span>', body)

    parts, cur = [], None
    for lvl, sid, txt in toc:
        if lvl == '1':
            cur = {'id': sid, 'label': txt, 'items': []}; parts.append(cur)
        elif cur is not None:
            cur['items'].append((sid, txt))

    out = []
    for p in parts:
        out.append(f'<li class="toc-part"><a href="#{p["id"]}">{ihtml.escape(p["label"].title())}</a><ul>')
        for sid, txt in p['items']:
            m = re.match(r'^(\d+|Annex [A-F]|Schedule \d+)\.?\s*[—-]?\s*(.*)$', txt)
            if m:
                lead, rest = m.group(1), m.group(2)
                lead = lead.replace('Annex ', '').replace('Schedule ', 'S')
            else:
                lead, rest = '', txt
            out.append(f'<li><a href="#{sid}"><span class="cn">{ihtml.escape(lead)}</span>'
                       f'<span class="ct">{ihtml.escape(rest)}</span></a></li>')
        out.append('</ul></li>')

    tpl = pathlib.Path(f'tpl-{key}.html').read_text(encoding='utf-8')
    html = tpl.replace('{{TOC}}', '\n'.join(out)).replace('{{BODY}}', body)
    pathlib.Path(cfg['out']).write_text(html, encoding='utf-8')
    print(f'{key}: {len(html)} chars | {len(parts)} groups | {sum(len(p["items"]) for p in parts)} sections')

for k in sys.argv[1:] or DOCS: build(k)
