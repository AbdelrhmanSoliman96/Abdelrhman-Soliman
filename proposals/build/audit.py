import pathlib, re
p = pathlib.Path('/home/user/Abdelrhman-Soliman/proposals/btakka-proposal.md').read_text(encoding='utf-8')
a = pathlib.Path('/home/user/Abdelrhman-Soliman/proposals/btakka-consulting-agreement.md').read_text(encoding='utf-8')
fails = []
def check(label, cond, detail=''):
    print(f'{"  OK  " if cond else " FAIL "} {label}' + (f'   {detail}' if detail and not cond else ''))
    if not cond: fails.append(label)

print('── commercial terms present and identical in both ──')
for term in ['EGP 150,000', 'EGP 30,000', 'EGP 20,000', 'EGP 70,000', 'Pre-Seed' ]:
    check(f'{term}', term in p and term in a)
check('10% success fee wording', '10%' in p and 'ten percent (10%)' in a)
check('12-month tail', 'Tail Period of twelve (12) months' in a and '12 months' in p or 'twelve (12) months' in a)

print('\n── structure counts ──')
sec7 = p[p.index('## 7. Deliverables'):p.index('## 8. What Btakka Must Provide')]
d = [int(m) for m in re.findall(r'^\| (\d+) \| ', sec7, re.M)]
check('deliverables numbered 1..37 with no gaps', d == list(range(1, 38)), f'got {d[:3]}..{d[-3:] if d else []} len={len(d)}')
check('agreement states 24 Phase 1 deliverables', 'Twenty-four (24) Phase 1 deliverables' in a)
check('agreement states 13 Phase 2 deliverables', 'thirteen (13) Phase 2 deliverables' in a)
annexA = p[p.index('## Annex A'):p.index('## Annex B')]
ids = [int(m) for m in re.findall(r'^\| (\d+) \| ', annexA, re.M)]
check('Annex A still numbered 1..36', sorted(ids) == list(range(1, 37)), f'len={len(ids)}')
check('12/12/12 ownership split in both', 'twelve prepared by the Consultant' in a and '**12**' in p)

print('\n── scenario analysis removed from the financial model ──')
bad_p = [l for l in p.splitlines() if re.search(r'scenario|sensitivity', l, re.I) and 'dilution' not in l.lower()]
bad_a = [l for l in a.splitlines() if re.search(r'scenario|sensitivity', l, re.I)
         and 'dilution' not in l.lower()]
check('no model-scenario language left in proposal', not bad_p, f'{bad_p}')
check('no model-scenario language left in agreement', not bad_a, f'{bad_a}')

print('\n── sole consultant ──')
check('no Mustafa in proposal', 'Mustafa' not in p)
check('no Mustafa in agreement', 'Mustafa' not in a)
check('no joint-acting language left', 'jointly and severally' not in a and 'acting jointly' not in a)
check('single signature block', 'THE CONSULTANT (1)' not in a and '| **THE CONSULTANT** | **THE CLIENT** |' in a)
check('clause 1 back to 1.2 / 1.3', '**1.2** Headings' in a and '**1.3** The Proposal is annexed' in a and '**1.4**' not in a)

print('\n── fee schedule: 30 / 30 / 20 / 70 ──')
for m, amt in [('M1', '30,000'), ('M2', '30,000'), ('M3', '20,000'), ('M4', '70,000')]:
    check(f'{m} = EGP {amt} in agreement', re.search(rf'\*\*{m} — [^|]+\|[^|]*\|[^|]*{re.escape(amt)}', a) is not None)
check('agreement milestone rows sum to 150,000',
      sum(int(x.replace(',','')) for x in re.findall(r'\*\*(30,000|20,000|70,000)\*\* \|', a)[:4]) == 150000,
      str(re.findall(r'\*\*(30,000|20,000|70,000)\*\* \|', a)[:4]))
check('proposal cumulative column ends at 150,000', '**EGP 150,000** |' in p)
check('no stale EGP 90,000 anywhere', '90,000' not in p and '90,000' not in a)
check('no stale "three milestones"', 'three milestones' not in p)
check('exec summary says four milestones', 'four milestones' in p)
check('M3 trigger defined in both', 'first outreach wave' in a and 'outreach wave' in p)
check('6.1 sub-paragraphs run (a)-(d)', all(f'**({c})**' in a for c in 'abcd'))
check('no dangling 6.1(c) reference', 'Clause 6.1(c)' not in a)

print('\n── delivery split ──')
check('Clause 3.7 present', '**3.7 Division of delivery.**' in a)
check('3.7 cites Annex A markers', 'marked **C** at Annex A' in a and 'marked **C+B**' in a)
check('proposal states the split', 'How delivery divides.' in p)
check('proposal points at Clause 3.7', 'Clause 3.7 of the Consulting Agreement' in p)
check('title used consistently', 'Investment & Business Expert' not in p and 'Investment & Business Expert' not in a)
check('no stale "Independent Investment Advisor"', 'Independent Investment Advisor' not in p and 'Independent Investment Advisor' not in a)

print('\n── cross-references resolve ──')
for ref, doc, name in [('Annex A', p, 'proposal'), ('Annex B', p, 'proposal'), ('Annex C', p, 'proposal')]:
    check(f'{ref} exists in {name}', f'## {ref}' in doc)
for n in range(1, 4):
    check(f'Schedule {n} exists in agreement', f'## Schedule {n}' in a)
check('Schedule 4 (drafting to-do) removed from the contract', '## Schedule 4' not in a)
check('no reference to the removed Schedule 4', 'Schedule 4' not in a and 'Schedule 4' not in p)
check('no editorial commentary left in the contract', 'commercial core of Phase 2' not in a and 'Alternative, to be selected' not in a)
check('Document Control removed', '### Document Control' not in a)
check('worked scenarios removed', 'Worked scenarios' not in a)
check('payment details renumbered to 2.3', '### 2.3 Payment details' in a and '### 2.4' not in a)
for ref in re.findall(r'Schedule (\d)', p):
    check(f'proposal cites Schedule {ref} -> exists', f'## Schedule {ref}' in a)
for ref in set(re.findall(r'Annex ([A-C])', a)):
    check(f'agreement cites Annex {ref} -> exists', f'## Annex {ref}' in p)
cl = sorted({int(m) for m in re.findall(r'Clause (\d+)', p)})
check('proposal cites only real clauses (1-19)', all(1 <= c <= 19 for c in cl), f'{cl}')

print('\n' + ('ALL CHECKS PASSED' if not fails else f'{len(fails)} FAILED: {fails}'))
