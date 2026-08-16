---
name: project-continuity
description: Use this skill for ANY multi-session project — whenever the user asks to create or update a project document, status file, roadmap, plan, or spec; whenever a session STARTS on an existing project (questions like "وين وصلنا؟"/"where were we?"/"catch me up" are a trigger); whenever a work session wraps up a meaningful chunk of work; whenever the user says "خلصنا"/"وقفة"/"حدث الوثيقة"/"we're done for now"/"update the docs"; whenever the user expresses worry about losing context, forgetting progress, or a fresh chat not knowing where things stand; and whenever you are about to edit, rename, or replace any project file. Proactively apply this even if the user doesn't ask — anytime documentation is the thing standing between "this project makes sense to whoever opens it next" and "this project only makes sense inside one conversation's memory." Applies equally to app/product specs, business plans, research, legal work, or any long-running multi-session effort.
---

# Project Continuity — Living Documentation Discipline

## The core principle: chat is not storage

Claude has no memory across separate conversations. Anything said in chat but not written to a file **does not exist** for the next session. The only thing that carries a project forward is its files. Documentation fails at continuity for specific, preventable reasons:

1. **Drift**: work gets done, but the tracking doc isn't updated — the next session reads a stale picture.
2. **Buried deferrals**: "let's do that later" gets said, but never lands anywhere attached to the decision point it belongs to.
3. **Wrong-doc edits**: a file gets edited (or replaced) based on an assumption about its role, corrupting a document that served a different purpose.
4. **Version confusion**: multiple copies of the same doc with different names accumulate, and nobody knows which is current.

This skill is a structural fix, not a reminder to "try harder": **the discipline is written into the documents themselves**, so any fresh reader — human or AI — picks it up just by opening the file.

---

## Protocol 1 — Session OPEN (orientation before action)

When a session starts on an existing project (especially on "where were we?"-type questions), do this **before doing any work**:

1. **Read the Master Roadmap first** (see structure below) — not memory summaries, not chat history alone. The roadmap is the authoritative "where are we."
2. **Cross-check recent conversation history** if available (search past chats): the roadmap may lag behind the very last session's final minutes. If chat history shows work *after* the roadmap's last update, flag the gap explicitly.
3. **State the current position to the user** in a few sentences: what's closed, what's the agreed next step, what's still open — with one flag for anything ambiguous or stale.
4. **Do not begin new work until the user confirms** the stated position (or corrects it). Starting work on a wrong assumption of "where we are" wastes more time than a one-line confirmation.

## Protocol 2 — Session CLOSE (capture before goodbye)

When a session wraps meaningful work (or the user signals a stop: "خلصنا", "وقفة", "we're done"), do this **without being asked**:

1. **Update the doc first, then report.** Never give the user a verbal status summary of the session while leaving the doc stale — the doc update comes first, the chat summary quotes from it. A status that exists only in chat is a status that doesn't exist.
2. Check off everything completed this session.
3. **Sweep the session for deferrals**: anything said as "later / not now / next time / بعدين" gets an inline deferred tag under the exact item it belongs to (see below), dated.
4. **Sweep for closures too**: any previously-deferred item that got resolved this session gets closed with a date — don't leave resolved items looking open.
5. Append one entry to the **cumulative changelog** (see below).
6. Tell the user: here's what closed, here's what's next, here's what's still deferred — and hand them the updated file(s).

---

## The structure: one Master Roadmap section, always at the top

Every multi-session project gets **one canonical section — "Master Roadmap" / "خارطة الطريق"** at the very top of the primary tracking doc. Detailed specs and notes live below; this section is what any reader sees first. It contains:

### A) The mandatory protocol, written into the file itself

Don't just follow the protocols — write them as an instruction inside the doc, addressed to whoever reads it next:

> **⚠️ Mandatory for any session reading this file:** (1) On open: read this section fully and confirm the current position with the user before doing new work. (2) On close: update this section — check off completions, close resolved deferrals with dates, tag new deferrals inline, append a changelog entry — BEFORE giving the user any session summary.

This makes the discipline self-propagating: it doesn't depend on any particular session remembering it.

### B) Source-of-truth map (which doc owns what)

If the project has more than one document, add a 2–4 row table stating each doc's exclusive role, e.g.:

| Doc | Owns | Never contains |
|---|---|---|
| decisions doc | what/why (product & policy decisions) | any progress/status language |
| status doc | how far implementation actually got | restated decisions |
| technical doc | schemas, methods, integrations | either of the above |

Every future edit checks this table first — it's the primary defense against wrong-doc edits.

### C) The hierarchical checklist — full scope, consistent markers

A nested checklist covering the *entire* project scope (all phases/modules, including not-yet-started ones), so a reader sees the whole shape of the work. Use consistent markers:

- ✅ done (per the project's definition of done — see below)
- 🔵 in progress
- ⛔ not started
- ➖ decided-but-not-built (a decision exists, no implementation — a *distinct* state from deferred)
- 🔜 deferred (with inline note)

### D) Definition of done — project-specific, written down

Every project defines what "✅" actually requires, and writes it in the roadmap. Examples: "built AND screenshot-confirmed", "merged AND tests passing", "signed by counterparty". Without this, "done" silently means different things to different sessions. Never mark ✅ on a weaker standard than the written one.

### E) Inline deferred tags — with a full lifecycle

When something is postponed, attach it **directly under the checklist item it belongs to** — never only in a detached "open items" list:

```
🔜 Deferred: [what/why] — [date deferred]
```

And when it resolves:

```
~~🔜 Deferred: [what/why] — [date]~~ → Closed [date]: [how]
```

**Periodic sweep**: whenever the open-items count is reviewed, actively ask the user which items have since closed in the real world — deferred lists rot silently, and stale "open" items are as misleading as stale "done" markers.

### F) Cumulative changelog

A dated, append-only log at the bottom of the roadmap (Update 1, 2, 3…), one short entry per session: what changed, in a few lines. This is the cheapest possible time-machine — it lets any reader reconstruct *when* something became true, which a checklist alone cannot show.

---

## File-editing safety rules (learned the hard way)

These apply to **any** edit, rename, or replacement of an existing project file:

1. **Confirm the doc's role before editing it.** If there's any chance the file serves a broader purpose than the current task (e.g., it might be overall project context, not just this workstream), ask — don't assume from the filename or from how it was used this session.
2. **Preserve a copy of the original before modifying** — hand the user an untouched backup first, or keep the pristine content recoverable, before producing an edited version.
3. **Never silently replace.** Any suggestion to overwrite a file states: what changes, what's affected, and waits for explicit confirmation. "Upload this instead of that" is never said casually.
4. **One canonical filename per doc.** Edited versions ultimately carry the same name as the original (replacement, not accumulation). If a temporary suffix like `_UPDATED` is unavoidable, explicitly instruct the user which file to delete and what to rename — and at the next session open, check that the rename actually happened. Two live versions of one doc is a defect, not a convenience.
5. **Prefer surgical edits over rewrites** for docs with broad roles: list the specific changes made (numbered), and state explicitly what was NOT touched.

## Verify claims against artifacts

A written "done" is a claim, not a fact — especially once it ages. When about to *rely* on a status marker (skip something marked done, resume something marked deferred) and the stakes are non-trivial, **check the actual artifact** (the file, the code, the screen) rather than trusting the last text description. Text drifts; the artifact doesn't lie. Build this in as a periodic habit, not a one-time audit.

## Don't duplicate shared components

If the same underlying thing exists in variants (one screen for two user types, one doc in two formats), prefer a single artifact with a variant switch over two copies — duplicated copies drift silently. When this comes up, document it as a standing rule in the project so it isn't relearned twice.

---

## Adopting this on an existing project mid-stream

1. Read what exists; reconstruct full scope (all phases, not just the active one).
2. **Propose** the Master Roadmap section — show the shape, confirm scope, don't insert silently.
3. Migrate existing "open items"/TODO lists into inline tags under the roadmap; kill the parallel detached list.
4. Build the source-of-truth map with the user (which doc owns what) — this often surfaces role ambiguities that were accidents waiting to happen.
5. Add the mandatory-protocol text so it self-propagates.

## Triggered in practice

- Session opens with "وين وصلنا؟" → read roadmap → cross-check recent chats → state position → wait for confirmation → only then work.
- User: "that's it for today" → update doc first (completions, deferrals in, closures out, changelog entry), then summarize from it.
- User mid-conversation: "let's handle X later" → note it now; it lands as an inline tag at the next close protocol — never left to evaporate in chat history.
- User: "update the doc" on a file whose role isn't 100% clear → ask what the doc covers before touching it; back it up; propose changes; wait.
- User: "did we actually finish X?" and a doc says done → if it matters, verify against the real artifact before confirming.
- User closes several open items verbally ("كلها انقفلت إلا وحدة") → that's a close-protocol trigger for the doc even mid-session: record the closures with dates now, don't just acknowledge in chat.
