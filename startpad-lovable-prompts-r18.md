# StartPad — Community Post Card & Feed (Round 18)

Four prompts rebuilding the community page, worked from the "Problem—Solution Fit" post.

---

## What the screen shows

One post, and it fills the entire viewport. That single fact is most of the problem — but there are seven distinct issues in this one card, and three of them are rendering bugs rather than design choices.

### 1. The image pushes everything else off-screen

The illustration takes roughly **three quarters of the visible card height**, and it's letterboxed inside a grey band with wide empty gutters on both sides. Whatever engagement controls exist — replies, reactions, save, share — are below the fold, pushed there by an image with no height cap.

A feed where one post fills one screen is not a feed. A founder scrolling for two minutes sees three posts.

### 2. The body text is truncated mid-sentence, with no way to expand

It ends on **"Customers are willing to…"** — cut in the middle of the fifth point, mid-word. There's no "Show more" control visible. The reader is left with an incomplete list and no way to finish it.

### 3. The author wrote a list. It renders as a run-on paragraph

Look at the body: `It means: → The problem is real, not assumed. → Your target customers experience it frequently. → The problem is painful enough to demand a solution. → Your solution addresses the problem better than existing alternatives. → Customers are willing to…`

Those arrows are line breaks that didn't survive. Someone typed five bullet points and the renderer stripped the newlines and ran them together. **This is a content bug, not a styling preference** — and it affects every post anyone writes with structure.

### 4. The text colour changes mid-sentence for no reason

Parts of the paragraph render in a teal/blue, parts in near-black, and the switches don't follow any semantic pattern — "one question every startup needs to answer" is coloured, "Problem—Solution Fit" is coloured, "a strong startup" is coloured, "The problem is real, not assumed" is coloured. None of them are links.

This reads as a broken rich-text renderer or a keyword-highlighting feature misfiring. Either way it makes the post look like it was pasted from somewhere and half-styled.

### 5. No author, no time

Nothing on this card says **who wrote it or when**. A post without a face and a timestamp isn't a community post — it's a CMS article with a comment box. And it's the difference between "a founder like me wrote this" and "the platform is broadcasting at me."

### 6. "General" is the only piece of metadata

The single category on the post is the least informative label available. Meanwhile the post is *specifically* about problem–solution fit, which is **Mission 6 — Value Proposition & Assumptions**, whose own description says "develop problem-solution canvas."

**That connection is the entire point of StartPad's community and it isn't made.** A founder currently on Mission 6 should see this post surfaced, badged, and linked to the mission they're stuck on.

### 7. The language controls sit in the middle of the content

`EN` and `Translate to Arabic` are wedged between the body text and the image. They're utility controls placed in the reading flow, and the `EN` pill's purpose is ambiguous — is it a label saying "this post is in English", or a button that switches to English?

The bilingual intent is right and worth keeping. The placement isn't.

---

## The card, rebuilt

```
┌────────────────────────────────────────────────────────────────┐
│  ⬤  Ahmed K.  ·  Founder, Cairo                          ⋯     │
│      Mission 6 · Value Proposition & Assumptions  ·  2d        │
├────────────────────────────────────────────────────────────────┤
│  Problem—Solution Fit                             [ Insight ]  │
│                                                                │
│  Before you think about scaling, fundraising, or acquiring      │
│  thousands of users, there's one question every startup needs   │
│  to answer: are we actually solving a problem people care       │
│  about?                                                         │
│                                                                │
│  Problem–Solution Fit means:                                    │
│    •  The problem is real, not assumed                          │
│    •  Your target customers experience it frequently            │
│    •  The problem is painful enough to demand a solution        │
│    •  Your solution beats the existing alternatives             │
│    •  Customers are willing to pay for it                       │
│                                                     Show more ⌄ │
├────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │   [ diagram — capped at 320px, click to expand ]         │  │
│  └──────────────────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────────────────┤
│  ♥ 34    💬 12 replies    ↗ Share    ⌂ Save         عربي ⇄ EN  │
├────────────────────────────────────────────────────────────────┤
│  You're on Mission 6 right now — this is the canvas you're      │
│  building.                                  Open Mission 6 →    │
└────────────────────────────────────────────────────────────────┘
```

Three things moved, and each one earns its place:

- **The author moved to the top**, with their mission, so the post has a person and a stage attached before a word is read.
- **The language toggle moved to the action row**, where every other utility control lives.
- **The mission strip is new**, and it only appears when the post's mission matches the reader's current mission. That's the line that turns a feed into a workspace.

---
---

# The prompts

Four, in order. Paste one per message.

## PROMPT A — Rebuild the Post Card

```text
PAGE: /community — the post card component, used in the feed and on the
single-post page.

THE PROBLEM

One post fills the entire viewport. The image has no height cap and takes
roughly three quarters of the visible card, letterboxed inside a grey band
with wide empty gutters, which pushes every engagement control below the
fold. A founder scrolling for two minutes sees three posts.

The body text truncates mid-sentence — "Customers are willing to…" — cut in
the middle of the fifth point, with no visible control to expand it.

And nothing on the card says WHO wrote it or WHEN. A post without an author
and a timestamp is not a community post; it is a CMS article.

THE FIX

1. CARD HEADER — add it, it does not currently exist:

     ⬤  Ahmed K.  ·  Founder, Cairo                             ⋯
         Mission 6 · Value Proposition & Assumptions  ·  2d

   - Avatar 40px, name, then role and city from the profile
   - The author's CURRENT MISSION, because that is what tells a reader
     whether this person is two steps ahead of them or two behind
   - Relative time: "2d", "4h", "just now". Absolute date on hover
   - Overflow menu on the right: Report · Copy link · Mute this author

2. CAP THE IMAGE.

     max-height: 320px desktop, 240px mobile
     object-fit: contain, on a neutral surface — not the current grey band
     border-radius matching the card, full card width, no side gutters

   If the natural aspect ratio is taller than 4:5, show the top of the image
   with a soft fade at the bottom and an "Expand" affordance.

   CLICK OPENS A LIGHTBOX with pinch-zoom on mobile. These posts carry
   diagrams with small labels — a capped thumbnail is unreadable, so the
   zoom is not optional.

3. TRUNCATE ON A LINE BOUNDARY, NEVER MID-WORD.

     4 lines collapsed on mobile, 6 on desktop
     "Show more ⌄" / "Show less ⌃" — always present when content is clipped
     Expansion is inline. It does NOT navigate away.

   Never cut inside a list item. If the clip point lands inside one, clip
   before it and let the count speak: "Show more — 3 more points".

4. ACTION ROW, below the image, always visible without scrolling on a
   standard post:

     ♥ 34    💬 12 replies    ↗ Share    ⌂ Save            عربي ⇄ EN

   Counts are always shown, including zero — "0 replies" is an invitation,
   a hidden control is not.

5. MOVE THE LANGUAGE CONTROL OUT OF THE CONTENT FLOW. The "EN" pill and
   "Translate to Arabic" button currently sit between the body text and the
   image, interrupting the reading. They belong in the action row. See
   PROMPT D for how the control itself should behave.

6. CATEGORY PILL moves up beside the title and gets a real taxonomy. See
   PROMPT B.

7. CARD DENSITY TARGET: a post with a title, four lines of body and one
   image fits in about 520px on desktop. Three posts should be reachable
   without scrolling on a 1080px screen.
```

## PROMPT B — Fix the Body Rendering, and Scope the Feed to the Journey

```text
PAGE: /community — the post body renderer, the composer, and the feed filters.

THE PROBLEM — PART ONE, A BUG

The author of the "Problem—Solution Fit" post wrote a list. It renders as a
run-on paragraph:

  "It means: → The problem is real, not assumed. → Your target customers
   experience it frequently. → The problem is painful enough to demand a
   solution. → Your solution addresses the problem better than existing
   alternatives. → Customers are willing to…"

Those arrows are line breaks that did not survive storage or rendering. Every
structured post anyone writes is being flattened this way.

Second bug on the same paragraph: THE TEXT COLOUR CHANGES MID-SENTENCE with
no semantic pattern. "one question every startup needs to answer",
"Problem—Solution Fit", "a strong startup" and "The problem is real, not
assumed" all render in a teal/blue while the surrounding text is near-black.
None of them are links. Check the rich-text renderer and any
keyword-highlighting pass — one of them is emitting spans it should not.

THE FIX — PART ONE

1. PRESERVE STRUCTURE END TO END. Store the body as restricted markdown —
   paragraphs, unordered and ordered lists, bold, italic, inline code, links,
   blockquote. Nothing else. Render it properly; do not strip newlines.

2. MIGRATE WHAT IS ALREADY BROKEN. Write a one-off pass over existing posts:
   a run of " → " or " - " or " • " inside a paragraph, three or more times,
   becomes a real list. Log every post it changes so it can be reviewed.

3. GIVE THE COMPOSER A LIST BUTTON, so authors stop typing arrows to get the
   structure the editor should provide.

4. ONE TEXT COLOUR FOR BODY COPY. Colour is reserved for links and for the
   mission badge. Fix whatever is currently emitting coloured spans mid
   paragraph.

THE PROBLEM — PART TWO, THE BIGGER ONE

This post's only metadata is a category reading "General" — the least
informative label available. Meanwhile the post is specifically about
problem–solution fit, which is MISSION 6, whose own description reads
"develop problem-solution canvas".

That connection is what the community is for, and it is not being made.

THE FIX — PART TWO

1. EVERY POST CARRIES AN OPTIONAL MISSION TAG. The composer asks once:
   "Which mission is this about?" — a picker listing all 15 by name, plus
   "Not about a specific mission". Default it to the author's current mission.

2. REPLACE THE "GENERAL" CATEGORY with a small, real taxonomy. Six types,
   each a different kind of contribution:

     Question        I'm stuck and need help
     Insight         something I learned that might help you
     Win             something that worked
     Feedback wanted here's my work, tell me what's wrong with it
     Resource        a tool, template or link
     Introduction    who I am and what I'm building

   The "Problem—Solution Fit" post is an Insight. "General" tells a reader
   nothing about whether to open it.

3. FEED FILTERS, as chips across the top, in this order:

     [ My mission ]  [ Everything ]  [ Questions ]  [ Wins ]  [ Feedback wanted ]

   "MY MISSION" IS THE DEFAULT for a logged-in founder who has started the
   journey. Everything else is one tap away. A founder stuck on Mission 6
   should open the community and see Mission 6 conversations first — that is
   the whole premise, and a chronological firehose buries it.

4. MISSION CONTEXT STRIP on any post whose mission matches the reader's
   current mission:

     "You're on Mission 6 right now — this is the canvas you're building."
                                                    [ Open Mission 6 → ]

   Show it only on a match. Shown on every post it becomes furniture.

5. THE REVERSE LINK. On each mission page, show the three most useful recent
   community posts tagged to that mission. The community feeds the journey
   and the journey feeds the community, or neither is worth opening.
```

## PROMPT C — Turn the Feed From a Broadcast Into a Conversation

```text
PAGE: /community — the feed, the post card and the composer.

THE PROBLEM

The post reads as a lesson, not a discussion. It states five facts about
problem–solution fit and ends. There is no question, nothing asked of the
reader, and nothing to disagree with.

A feed of well-written broadcasts gets read and not answered, and a community
that is only read is a blog with avatars.

THE FIX

1. EVERY POST ENDS WITH SOMETHING TO ANSWER. In the composer, a required
   field for Question, Insight and Feedback-wanted posts:

     "What do you want from the community?"
       · Tell me if this matches your experience
       · Help me decide between two options
       · Review my work
       · Nothing — just sharing

   It renders under the body as a quiet line: "Ahmed is asking: does this
   match your experience?" and it is what the reply box is labelled with.

2. THE REPLY BOX IS OPEN, NOT A BUTTON. On the single-post page the composer
   is visible and focused-ready, pre-labelled with the ask above. A reply
   behind a click is a reply that does not happen.

3. SEED THE FIRST REPLY ON EVERY POST — genuinely, not artificially. When a
   post has no replies after four hours, surface it to three founders on the
   same mission:

     "Ahmed asked something about the mission you're on. 2 min to answer."

   Never fabricate replies, never auto-generate them. Prompt real people.

4. SHOW WHO IS IN THE ROOM. Under the action row:

     "8 founders on Mission 6 read this today"

   Only when true, only with a real number. It is the single strongest
   signal that anyone is out there.

5. REPLIES FROM PEOPLE FURTHER ALONG GET A QUIET MARKER — "Mission 11" next
   to their name. Not a rank, not a badge, not points. Just their stage, so
   a reader knows the answer comes from someone two phases ahead.

6. ONE PRIMARY BUTTON PER SCREEN. Reply is primary. Everything else — share,
   save, follow — is a text link or an icon. This rule was broken on the
   mission page and should not be re-broken here.

7. WHAT NOT TO DO. No leaderboards, no post streaks, no "top contributor of
   the week", no badges for volume. This audience reads that as gamified
   noise faster than most, and it rewards posting over helping. The existing
   XP system already covers motivation; the community does not need a second
   one.
```

## PROMPT D — Bilingual, RTL and Brand

```text
PAGE: /community — all views.

THE PROBLEM

The "EN" pill and the "Translate to Arabic" button sit between the body text
and the image, interrupting the reading. And the "EN" pill's purpose is
ambiguous: is it a label saying the post is in English, or a button that
switches to English?

The bilingual intent is exactly right for this audience. The execution puts a
utility control in the middle of the content.

THE FIX

1. ONE CONTROL, IN THE ACTION ROW, showing the destination not the state:

     Post is in English, reader's locale is Arabic:   "عربي ⇄"
     Post is in Arabic, reader's locale is English:   "English ⇄"
     Post is already in the reader's language:        nothing at all

   Remove the separate "EN" pill. The language of a post is evident from
   reading it; a pill stating it is noise. If a language marker is genuinely
   needed for scanning, put a small "AR" or "EN" in the card header beside
   the timestamp, not below the body.

2. TRANSLATE IN PLACE. The body is replaced, the button becomes "Show
   original ⇄", and the choice persists for that reader across the session.
   Do not open a modal and do not navigate away.

3. MARK MACHINE TRANSLATION HONESTLY, in one quiet line under the translated
   body:

     "Translated automatically · Show original"

   A founder reading a translated technical explanation needs to know it was
   translated, because the mistakes will be in the vocabulary that matters.

4. FULL RTL when the reader's locale is Arabic: card direction, avatar side,
   action row order, the "Show more" chevron, and the mission strip arrow all
   mirror. The post body takes dir="auto" per block, so an Arabic reply under
   an English post renders correctly without mirroring the whole card.

5. COMPOSE IN EITHER LANGUAGE, and the composer's direction follows what is
   being typed, not the interface locale. A founder on the Arabic interface
   writing an English post should not fight the text field.

6. BRAND. Apply the current tokens throughout — the page background here is a
   cream/yellow that belongs to neither palette:

     page background   paper #F4F4F2
     card surface      #FFFFFF with a 1px #E5E5E2 border
     body text         ink #0B0D10
     secondary text    #5B6068
     primary action    indigo #3418E0 with white text
     mission strip     lime #CBF24A background with ink text

   NEVER lime text on white — it measures 1.29:1 and fails every contrast
   threshold. Lime is a fill that carries near-black text. Indigo on white is
   8.9:1 and is the accessible action colour.

7. MINIMUM 44px TAP TARGETS on every action-row control, and the row must not
   wrap to two lines at 390px width.
```

---

## Sequence

| # | Prompt | Why here |
|---|---|---|
| 1 | **A** — the post card | The image cap and the header are what make the feed usable at all |
| 2 | **B** — rendering and mission scoping | Two live bugs, plus the connection the community exists for |
| 3 | **C** — conversation | Only worth doing once posts are readable and findable |
| 4 | **D** — bilingual and brand | Cheapest, and safe to ship alongside any of the others |

A and B are the ones that change whether the page works. C is the one that changes whether anyone comes back.

---

## Two things worth checking before building

**The coloured text may not be a styling bug.** If there's an AI pass that highlights key phrases in posts, then what I read as a broken renderer is a feature behaving badly — the highlights follow no pattern a reader can learn, so they land as noise. If that feature exists, either make the rule legible (highlight defined terms only, and make them tappable for a definition) or turn it off.

**Check whether the post has an author at all.** If these posts are seeded editorial content published under no name, then adding an author header needs a decision first: publish them under a real StartPad team member, or mark them clearly as "StartPad Editorial" with a distinct card treatment. What should not happen is editorial content sitting in the feed looking like a founder wrote it.
