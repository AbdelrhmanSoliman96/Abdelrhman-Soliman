# LEAP — Proposal & Contract System

A working kit built from the three **Company Profile · 2026** decks (master, real estate,
investment & business). Purpose: go from an enquiry to a signed engagement without rewriting
anything from scratch, and without losing the firm's positioning or its protections along the way.

## Files

| File | What it is | When you open it |
|---|---|---|
| `01-company-brief.md` | The study — identity, positioning, the three practices, methodology, credentials, portfolio, leadership, brand voice, and the gaps still to fill | Writing any bio, pitch, deck or "why us" section |
| `02-service-catalog.md` | All 17 services as paste-able scope blocks: scope, deliverables, client inputs, duration, effort, fee basis — plus the fee build-up method | Scoping and pricing an engagement |
| `03-proposal-template-ar.md` | Proposal template, Arabic, brand-voiced | Egyptian and GCC clients |
| `03-proposal-template-en.md` | Same structure in English | International clients, funds, family offices |
| `04-consulting-agreement-ar.md` | Full consultancy services agreement, Arabic | The contract that follows an accepted proposal |
| `04-consulting-agreement-en.md` | Same agreement in English, identical clause numbering | Bilingual execution |
| `05-annexes.md` | NDA, change order, success-fee addendum, retainer addendum, third-party reliance letter, short-form engagement letter | Attachments and special situations |

## The workflow

```
Enquiry
  └─ 1. Sign the mutual NDA                      → 05-annexes.md §1
     2. Scope it: pick service blocks            → 02-service-catalog.md §A–D
     3. Price it: effort × rate, pick fee model  → 02-service-catalog.md §F
     4. Write the proposal                       → 03-proposal-template-[ar|en].md
     5. On acceptance, issue the agreement       → 04-consulting-agreement-[ar|en].md
        · Schedule A  = proposal §03, §04, §05, §08  (verbatim)
        · Schedule B  = proposal §09                 (verbatim)
        · Schedule D  = proposal §07                 (verbatim)
        · Add success fee / retainer addendum   → 05-annexes.md §3, §4
     6. Mobilisation paid → kick-off → the clock starts
     7. Scope changes only by change order       → 05-annexes.md §2
```

**The one rule that matters:** the proposal's scope, fees and input list must appear **word for
word** in the agreement's schedules. Every scope dispute in advisory work starts with a gap between
what was proposed and what was signed.

## Five clauses never to drop

Whatever else gets negotiated away, these are what stand between a feasibility study and a claim:

1. **No guarantee** (agreement §9) — projections are estimates on stated assumptions; no warranty of
   IRR, absorption, valuation, financing or transaction outcome.
2. **Reliance limits** (§10) — prepared for the client alone, for one stated purpose; third parties
   get a reliance letter or nothing.
3. **Liability cap** (§16) — capped at fees paid, indirect loss excluded, 12-month claim window.
4. **IP on payment** (§11) — methodologies and model architectures stay with the firm; the client's
   licence starts when the last invoice clears.
5. **Non-solicitation** (§17) — a two-principal firm sells named people; keep them.

## Before the first contract goes out

- [ ] Fill in the legal entity details — registered name, form, commercial register, tax card, VAT
- [ ] Fill in bank details for the payment clause (EGP and USD)
- [ ] Set the day rates in `02-service-catalog.md` §F and Schedule C — keep them in a private file
- [ ] Decide the default liability cap and check it against any professional indemnity cover
- [ ] Confirm the licensing position on remunerated capital raising in each market — FRA (Egypt),
      CMA (KSA), SCA (UAE). This governs whether `05-annexes.md` §3 can be used at all
- [ ] Have counsel qualified in the governing jurisdiction review both agreement language versions
- [ ] Confirm the Arabic-prevails language clause is what you want (agreement §22.9 / البند 23/9)

## Notes on sources

Everything factual comes from the three decks. `leapassociate.com` was unreachable from the
environment these files were written in (blocked by the network egress proxy), so where the site
says something different, the site wins — update `01-company-brief.md` accordingly.

The agreement and annexes are **drafting templates, not legal advice**. They are built around the
firm's actual risk profile — staged studies, models relied on for capital decisions, success-fee
mandates, placed personnel — but they need a qualified lawyer's review before first use.
