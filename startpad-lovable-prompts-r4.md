# StartPad — Lovable Prompts (Round 4)

Six prompts covering the About page split and the Knowledge Base content engine.

Paste one prompt per message — never concatenate, and let each finish before sending the next.

| Set | Page / area | Prompts |
|---|---|---|
| 1 | About page (pre-login vs post-login) | A |
| 2 | Knowledge Base — architecture & article template | A |
| 3 | Knowledge Base — AI content pipeline | A |
| 4 | Knowledge Base — data & charts layer | A |
| 5 | Knowledge Base — SEO foundation | A |
| 6 | Knowledge Base — conversion layer | A |

Design tokens: navy `#0A1D34` headlines, green `#047857` primary, white rounded cards with soft shadows.

---

## Read this before Set 3

You asked for AI to write articles automatically. That's buildable and Set 3 builds it — but with one gate that isn't optional.

**Google's spam policy treats mass-produced AI content whose primary purpose is ranking as "scaled content abuse."** Sites doing it get demoted or deindexed, and the penalty applies to the whole domain, not just the offending pages. Publishing straight from a model to a live URL is the exact pattern that triggers it.

**Charts built from AI-generated numbers are fabricated statistics** published under your brand. For a platform asking MENA founders to trust its judgement, that's not a small risk.

The way through both is the same, and it happens to be your biggest advantage: **you have first-party data nobody else has.** Mission submissions, rubric scores, where founders fail, how long missions actually take, which industries first-time founders choose. Wamda built its authority on funding data it collects. You can build yours on founder-progress data you already generate.

So the pipeline in Set 3 is: **AI drafts fast → a human edits and signs → real data and real sources back every chart → publish.** You keep the speed. You just don't publish unreviewed.

---
---

# Set 1 — About Page

One prompt. The About page currently serves the same content to everyone; a signed-out visitor and a founder six missions in need entirely different things from it.

## PROMPT A — Two Different About Pages

```text
PAGE: About (/about) — must render different content and different CTAs
depending on auth state.

THE PROBLEM
/about currently serves identical content to everyone. But the two audiences
want opposite things from it:

  A SIGNED-OUT VISITOR is asking "should I trust this and sign up?"
  A SIGNED-IN FOUNDER is asking "who is building this, where is it going, and
  can I influence it?"

Showing a signed-in founder a "Start free" button on the About page is the same
class of error as serving them the marketing homepage — it tells them the
product does not know who they are.

THE FIX — one route, two compositions, selected by auth state using the SHARED
route type from the routing work (Set 1 in the Round 3 prompts).

=============================================================
VERSION 1 — LOGGED OUT. Purpose: earn trust and convert.
=============================================================

1. HERO
   Headline: "We grew up watching brilliant ideas die in group chats"
   (the same line as the homepage — this is the origin story page, it belongs
   here in full)
   Subhead: one sentence on what StartPad is.

2. THE STORY — expand the existing "Why we built this" copy into the full
   version. University taught theory, YouTube taught hype, nobody taught the
   actual steps. Not in Arabic. Not for our markets. Not for free. This is the
   strongest writing on the site and the About page is where it can run long.

3. WHAT STARTPAD IS — AND ISN'T
   A short two-column block. "We're not a course. We're not an incubator. We
   don't take equity." Say what you are not; it is more persuasive than another
   feature list and it answers the question founders are actually asking.

4. THE TEAM
   Real photos, real names, real roles, LinkedIn links. This is currently
   missing entirely and it is the single biggest trust gap on the page. A
   founder deciding whether to hand you their startup idea wants to see who
   they are handing it to.

5. WHERE WE ARE — honest traction. "104 founders. 15 missions live. Built in
   Cairo." Do not inflate. See the claims work in Round 3 Set 5·A.

6. BACKED BY / BUILT WITH — only if you have something real to say. No logo
   walls implying affiliation you do not have.

7. CTA BLOCK
   Primary:   "Start free" → /signup
   Secondary: "See how it works" → /how-it-works

=============================================================
VERSION 2 — LOGGED IN. Purpose: belonging, retention, feedback.
=============================================================

1. HERO
   Headline: "You're founder #104"  (use their actual number)
   Subhead: "Here's who's building StartPad, and where it goes next."
   Personal, not promotional.

2. WHAT WE SHIPPED RECENTLY — a changelog, newest first, 5 most recent entries
   with dates. Founders who see a product improving stay. Link to a full
   /changelog page.

3. WHAT WE'RE BUILDING NEXT — a public roadmap in three columns: Now / Next /
   Exploring. No dates you cannot hold. This is the single most effective
   retention element on a page like this.

4. SHAPE IT — a feedback block that actually works:
     - "Request a feature" → a short form, not an email link
     - "Report a problem" → same
     - "Vote on what's next" → let founders upvote roadmap items
   A founder who has influenced the roadmap does not churn.

5. THE TEAM — same as logged-out, plus "Talk to us" contact routes.

6. THE COMMUNITY — live numbers that make them feel part of something:
   founders currently on each phase, missions completed this month, countries
   represented. Use real figures only.

7. CTA BLOCK — never "Start free". Instead:
   Primary:   "Continue Mission 1" → their current mission, by number and name
   Secondary: "Share feedback"
   Tertiary:  "Join the community"

RULES

- One route, one file. The auth branch happens once, at the top level — do not
  scatter isLoggedIn checks through the sections.
- Shared sections (the story, the team) are single components reused by both
  versions. Only the framing, the ordering and the CTAs differ.
- The logged-in version uses the APP shell (app nav, profile banner). The
  logged-out version uses the PUBLIC shell.
- No signup or "Get started" CTA may render anywhere in the logged-in version.
- Both versions carry the legal footer row: Privacy · Terms · Cookies · FAQ.

Apply the same pattern to /how-it-works: logged out it sells the journey and
ends in "Start free"; logged in it explains the mechanics — scoring, points,
streaks, resubmission — and ends in "Go to my journey".
```

**Why this order.** Depends on the route-type work in Round 3 Set 1·A. Do that first or the auth branch has nowhere to live.

---
---

# Set 2 — Knowledge Base Architecture

One prompt. This defines the content model and the article template before anything is generated — get this wrong and every article afterwards inherits it.

## PROMPT A — Content Architecture and the Article Template

```text
PAGE: Knowledge Base — upgrading the existing /knowledge-hub into a full
content platform. New routes: /insights (index), /insights/[slug] (article),
/insights/topic/[topic] (pillar pages), /authors/[slug].

REFERENCE STYLE
Model the article format on Wamda (wamda.com), which is the standard in this
market. Their pattern:
  - Headlines lead with the finding or the number, not a teaser
    e.g. "MENA startup funding hits $3.5 billion in September 2025, lifting
    Q3 total to $4.5 billion"
  - Data is attributed to a named source in the first paragraph
  - Analysis goes beyond the number — what it means, not just what it is
  - A regular, predictable report cadence (monthly and annual)
  - Downloadable long-form reports alongside articles

CONTENT TYPES — four, each with its own template:

  ARTICLE      800-1,500 words. A single question answered with data.
  CASE STUDY   1,200-2,000 words. One company, one decision, one outcome.
  WHITEPAPER   2,500-5,000 words. Gated or ungated, PDF download, its own
               landing page.
  REPORT       Recurring data release. Monthly or quarterly. The cadence piece.

ARTICLE TEMPLATE — build this as the single renderer for all four types, with
sections switched on or off per type. Order matters:

1. BREADCRUMB          Insights › Funding › [title]
2. CATEGORY CHIP + READ TIME
3. H1 HEADLINE         The finding itself. One H1 per page, never more.
4. STANDFIRST          1-2 sentences, larger type, muted. States the finding
                       and its source. This is what gets quoted in search
                       results and by AI assistants — write it to stand alone.
5. BYLINE ROW          Author photo, name (linked to /authors/[slug]), role,
                       published date, "Updated" date when edited.
6. KEY FINDINGS BOX    3-5 bullets at the very top, above the body. This is the
                       highest-value block on the page: it is what featured
                       snippets and AI answer engines extract. Each bullet is
                       one complete, self-contained sentence with its number.
7. BODY                H2 sections, H3 subsections. Paragraphs of 2-4 sentences.
                       No section longer than ~200 words without a subheading,
                       a chart or a pull quote.
8. INLINE CHARTS       See Set 4. Every chart carries a caption and a source
                       line directly beneath it.
9. PULL QUOTES         Full-width, large type, attributed.
10. DATA TABLE         Where a chart would lose detail. Horizontally scrollable
                       on mobile, never breaking the page.
11. METHODOLOGY BOX    Bordered, at the end of the body. Sample size, date
                       range, how the data was collected, known limitations.
                       Non-negotiable on anything with a number in it.
12. SOURCES            Numbered list, each linked. Every statistic in the body
                       carries a superscript reference to this list.
13. AUTHOR BIO         Photo, 2-3 sentences of relevant credentials, links.
14. CTA BLOCK          See Set 6. One CTA, matched to the topic.
15. RELATED ARTICLES   Three, matched by topic AND by mission relevance.

TOPIC CLUSTERS — structure the whole library as pillar-and-cluster, which is
what actually ranks:
  - A PILLAR PAGE per major topic at /insights/topic/[topic]: a comprehensive
    guide, 3,000+ words, linking out to every cluster article.
  - Suggested pillars for this audience: Fundraising in MENA · Validation and
    Product-Market Fit · Building an MVP · Go-to-Market · Legal and Company
    Setup · Hiring and Co-founders.
  - Every cluster article links UP to its pillar; the pillar links DOWN to all
    of them. This internal linking structure is a large part of why the whole
    library ranks rather than individual pages.

ARTICLE METADATA — every piece carries:
  title, slug, standfirst, content_type, topic (pillar), tags[],
  author_id, published_at, updated_at, read_time,
  related_missions[]   ← ties content to the 15 missions
  related_phase        ← Discovery, Validation, etc.
  language (en|ar), translation_of (id),
  seo_title, seo_description, og_image,
  data_sources[], review_status, reviewed_by, reviewed_at

MISSION LINKING — this is what makes the library part of the product rather
than a blog beside it:
  - Every article tags the missions it is relevant to.
  - Inside a mission, show the 2-3 matching articles in a "Recommended reading"
    block.
  - On the article, show "Relevant to Mission 4 · Validation" as a chip that
    deep-links into the mission for signed-in founders.

INDEX PAGE (/insights):
  - Featured slot at the top.
  - Filters: content type, topic, mission/phase, language.
  - Search across title, standfirst and body.
  - Cards showing type chip, headline, standfirst excerpt, author, date, read
    time, and a cover image. Generate a fallback cover — topic colour, headline
    text, type icon — so no card ever renders blank. Two Knowledge Hub cards
    currently render as empty white blocks.
```

**Why this order.** Everything downstream depends on this schema. Build the model and the template before generating a single article.

---
---

# Set 3 — AI Content Pipeline

One prompt. This is the automation you asked for, with the editorial gate that keeps it from getting the domain penalised.

## PROMPT A — AI Drafting with an Editorial Gate

```text
PAGE: Admin content pipeline — new routes at /admin/content, plus the
review_status workflow on the article model from Set 2.

THE GOAL
Automate research, drafting, chart preparation and SEO packaging so a publishable
article takes an editor 30 minutes instead of a day. Do NOT automate publishing.

WHY THE GATE EXISTS — state this in the admin UI so nobody removes it later:
Google's spam policies treat mass-produced AI content whose primary purpose is
search ranking as "scaled content abuse." The penalty applies at domain level,
not page level — one batch of auto-published articles can demote the entire
site including the product pages. Every article therefore ships with a named
human author who reviewed and edited it. That is also what satisfies E-E-A-T:
experience, expertise, authoritativeness, trust.

THE PIPELINE — six stages, with the gate at stage 5:

STAGE 1 — TOPIC DISCOVERY (automated)
  Generate a ranked backlog of topics from four inputs:
    a) FIRST-PARTY DATA (highest value — see Set 4). Questions your own
       platform data can answer that nobody else can.
    b) MISSION GAPS. For each of the 15 missions, what do founders get stuck
       on? Pull from rubric scores: which criteria fail most often, and on
       which questions.
    c) COMMUNITY QUESTIONS. Real questions asked in Community and to the AI
       Mentor, clustered by theme. These are literal search queries from your
       exact audience.
    d) SEARCH DEMAND. Keyword research per topic cluster, with volume and
       difficulty where available.
  Output: a backlog table with topic, content type, target keyword, which
  pillar it belongs to, which missions it serves, and a priority score.
  Run weekly.

STAGE 2 — RESEARCH BRIEF (automated)
  For an approved topic, assemble:
    - The specific question the piece answers
    - Target keyword and 3-5 secondary keywords
    - The 3-5 data points that must appear, each with a REAL source URL
    - Which first-party data query backs it (see Set 4)
    - Competing articles already ranking, and what they miss
    - Suggested chart types and what each would show
    - Which missions and pillar it links to
  The brief is reviewed by a human before drafting. Rejecting a bad topic here
  costs a minute; rejecting a finished draft costs an hour.

STAGE 3 — DRAFTING (automated)
  Generate against the Set 2 template. Hard rules in the system prompt:
    - Never invent a statistic. Every number comes from the brief's sourced
      list or from a first-party data query. If a number is not in the brief,
      it does not go in the article.
    - Every statistic carries an inline reference to the sources list.
    - Write the standfirst and the Key Findings box to stand alone — they are
      what search results and AI assistants extract.
    - Short paragraphs, 2-4 sentences. Descriptive H2s containing the natural
      language a founder would search.
    - MENA-specific throughout: real countries, real currencies, real
      regulatory context. Generic global startup advice is what everyone else
      publishes and it will not rank.
    - No hedging filler, no "in today's fast-paced world", no listicle padding.
  Output a draft flagged review_status = "draft".

STAGE 4 — SEO PACKAGING (automated)
  Generate: seo_title (≤60 chars), seo_description (≤155), slug, suggested
  internal links to existing articles and the pillar, alt text for every image
  and chart, and the OG share image. Flag any keyword cannibalisation against
  existing articles.

STAGE 5 — HUMAN REVIEW  ← THE GATE. Nothing publishes without passing it.
  An editor UI with a checklist that must be fully ticked before the publish
  button enables:
    [ ] Every statistic traced to its source and the source opened
    [ ] Every chart's underlying data verified
    [ ] Claims about MENA markets are accurate and current
    [ ] Added at least one insight from real experience the model could not have
    [ ] Methodology box is complete and honest about limitations
    [ ] A named author takes the byline
    [ ] Read end to end, not skimmed
  Set review_status = "reviewed", record reviewed_by and reviewed_at.
  Publishing is blocked at the API level, not just the UI, when review_status
  is not "reviewed". Make it impossible to bypass by accident.

STAGE 6 — PUBLISH AND MEASURE (automated)
  Set published_at, ping the sitemap, generate social copy for Instagram,
  LinkedIn and X. Then track per article: impressions, clicks, average
  position, time on page, scroll depth, CTA conversion. Feed the winners back
  into Stage 1 so the backlog learns.

RATE LIMIT — cap publishing at 2-3 articles per week initially, regardless of
how many drafts exist. Sudden volume spikes on a young domain are themselves a
spam signal. Quality and consistency beat volume, and the cadence matters more
than the count.

ARABIC — the pipeline must support generating an Arabic version of any article
as a linked translation, not a separate article: same translation_of id,
hreflang pairing, its own slug. Arabic drafts go through the same human gate,
reviewed by an Arabic speaker.

BUILD THE ADMIN UI with a Kanban view across the six stages, so an editor can
see what is in research, in draft, awaiting review and published.
```

**Why this order.** Needs the Set 2 schema and the Set 4 data layer to exist. Build the gate in the same pass as the automation — retrofitting it after the first penalty is the expensive path.

---
---

# Set 4 — Data & Charts

One prompt. This is where the real defensibility is: articles nobody else can write, because nobody else has the data.

## PROMPT A — First-Party Data as the Content Moat

```text
PAGE: Knowledge Base data layer, chart components, and the /insights/data
reports section.

THE OPPORTUNITY
Wamda built its authority on MENA funding data it collects and publishes on a
regular cadence. You have an equivalent asset that nobody else has: real
behavioural data on how MENA founders actually build.

You currently hold, or can derive:
  - Mission submissions and their AI rubric scores across five criteria
  - Which rubric criteria founders fail most, per mission
  - How long each mission actually takes vs its estimate
  - Attempt counts before passing
  - Which industries first-time MENA founders choose
  - Drop-off points across the 15 missions
  - Founder demographics: country, occupational status, hours available
  - Which resources and articles founders actually open at each phase
  - Community question themes by phase

That is genuinely publishable, genuinely unique, and genuinely link-worthy —
which is the only kind of content that earns backlinks and rankings.

THE FIX

1. BUILD AN ANALYTICS QUERY LAYER with pre-defined, parameterised queries the
   content pipeline can call. Each returns aggregated, anonymised results plus
   its own metadata: sample size, date range, and any exclusions.

   Start with these ten:
     - Mission completion rate by mission number
     - Average rubric score by criterion (Specificity, Depth, Evidence,
       Actionability, Relevance)
     - Most-failed criterion per mission
     - Median attempts before passing, per mission
     - Actual vs estimated time per mission
     - Founder distribution by country
     - Founder distribution by occupational status and hours available
     - Industry distribution among first-time founders
     - Drop-off rate between phases
     - Correlation between hours available and completion rate

2. PRIVACY RULES — enforce in the query layer, not in review:
     - Minimum cohort size of 20 before any figure can be published. Below
       that, the query returns "insufficient data", never a number.
     - No individual founder, company or idea identifiable in any output.
     - No cross-tabulation that could re-identify (country × industry × stage
       will isolate individuals in small markets — block it).
     - Founders must be told in the privacy policy that anonymised aggregate
       data may be published, with an opt-out.

3. ARTICLES ONLY YOU CAN WRITE — seed the backlog with these:
     - "Where MENA founders get stuck: [N] mission submissions analysed"
     - "The five things AI reviewers penalise most in founder problem
       statements"
     - "How long idea-to-MVP actually takes: data from [N] MENA founders"
     - "Students vs full-time founders: who finishes, and why"
     - "The industries MENA first-time founders are choosing in 2026"
     - "Why founders fail validation more than any other phase"
   Each of these is a link magnet. Nobody else can publish them.

4. RECURRING REPORT — this is the Wamda cadence play and it compounds:
   A quarterly "State of MENA Founder Progress" report. Same structure every
   quarter, so it becomes a reference point people cite and link to:
     - Headline findings
     - Progress data across the 15 missions
     - Founder demographics
     - What changed since last quarter
     - Downloadable PDF with its own landing page
   Give it a permanent URL that updates, plus dated archive versions.

5. CHART COMPONENTS — build a small, consistent set. Do not let the AI invent
   chart styling per article:
     Bar (horizontal for ranked categories) · Line (change over time) ·
     Stacked bar (composition) · Simple table
   Every chart must:
     - Carry a caption stating the finding, not just a title
     - Carry a source line beneath: "Source: StartPad platform data, n=[N],
       Jan-Aug 2026" or the external citation
     - Render legibly on a 390px screen — never a shrunk desktop chart
     - Reserve its space before load so it causes no layout shift (a Core Web
       Vitals factor and therefore a ranking factor)
     - Work in both light and dark themes
     - Be readable without colour alone — use pattern, label or ordering too
     - Have a text alternative for screen readers describing the finding

6. NEVER FABRICATE. Add a hard rule to the drafting prompt and the review
   checklist: a chart may only be generated from either a first-party query
   result or a cited external dataset. AI-estimated, illustrative or
   representative numbers are never published. If the data does not exist, the
   article does not make the claim.

7. EXTERNAL DATA — when citing others (Wamda funding reports, MAGNiTT, World
   Bank, national statistics offices), cite the specific report and date, link
   to it, and never present someone else's data as your own analysis.
```

**Why this order.** Build before Set 3's drafting stage goes live, so the pipeline has real data to draw on from its first article.

---
---

# Set 5 — SEO Foundation

One prompt. Technical groundwork. Without it, good articles do not get found.

## PROMPT A — SEO and AI-Search Foundation

```text
PAGE: Knowledge Base (/insights and all article routes), plus site-wide
technical SEO.

THE GOAL
Rank in Google, and get cited by AI assistants — which increasingly sit between
your audience and your content. Both reward the same things: clear structure,
real expertise, and answers that stand alone.

1. RENDERING — articles must be server-rendered or statically generated.
   Client-only rendering is the single most common reason content platforms
   fail to rank. Confirm which the app currently uses and fix it if the
   article body is not in the initial HTML response.

2. STRUCTURED DATA — JSON-LD on every page:
     - Article (or NewsArticle for the report cadence) on every article:
       headline, description, image, datePublished, dateModified, author with
       a real Person entity linked to /authors/[slug], publisher Organization
       with logo
     - BreadcrumbList on every article
     - Organization on the site, once
     - FAQPage on the FAQ page and on any article with a Q&A section
     - Dataset on the recurring reports — under-used and it helps them surface
   Validate everything in Google's Rich Results Test before shipping.

3. META — per article, never templated site-wide:
     - <title> ≤60 chars, keyword near the front, brand at the end
     - <meta description> ≤155 chars, written to earn the click
     - Canonical URL on every page
     - Open Graph and Twitter card tags
     - Auto-generated OG image: headline text on the topic colour with the
       StartPad mark. Never ship a page with no share image.

4. ARABIC AND HREFLANG — this matters more for you than for most:
     - Locale in the URL: /en/insights/... and /ar/insights/...
     - Reciprocal hreflang on both, plus x-default
     - dir="rtl" on the whole document for Arabic, using logical CSS
       properties throughout
     - Arabic articles must be genuine translations with their own slug and
       their own meta — never machine output dumped into the same page
     - Arabic-language search for MENA founder topics is far less contested
       than English. This is the cheapest ranking opportunity you have.

5. SITEMAPS AND CRAWLING
     - XML sitemap, auto-updating on publish, split by type and locale
     - Reference it in robots.txt
     - Submit to Google Search Console and Bing Webmaster Tools
     - Ensure no noindex or robots block on /insights
     - Verify AI crawlers are not blocked if you want citations in AI answers

6. INTERNAL LINKING — the pillar-and-cluster structure from Set 2 is the point.
   Every cluster article links up to its pillar; every pillar links down to all
   its clusters; every article links to 2-3 siblings. Descriptive anchor text,
   never "click here". Automate a check that flags any orphan article with no
   inbound internal link.

7. CORE WEB VITALS — a confirmed ranking factor:
     - Images: WebP or AVIF, correct width and height attributes, lazy-loaded
       below the fold, eager for the hero
     - Charts: reserve space before render so nothing shifts
     - Fonts: preloaded, font-display: swap
     - Target LCP under 2.5s, CLS under 0.1, INP under 200ms
     - Test on a mid-range Android on 4G, not a laptop on wifi — that is what
       this audience uses

8. SEMANTIC HTML — exactly one H1, headings in order with no skipped levels,
   <article> and <time datetime="">, real <figure>/<figcaption> for charts,
   descriptive alt text on every image.

9. WRITTEN FOR AI ANSWER ENGINES — increasingly how this audience finds things:
     - The Key Findings box near the top, each bullet a complete standalone
       sentence with its number
     - H2s phrased as the questions people actually ask
     - Definitions given plainly and early, in one sentence
     - Data in real HTML tables, not images of tables
     - A visible "Last updated" date — recency is weighted heavily

10. MEASUREMENT — connect Search Console and track per article: impressions,
    clicks, CTR, average position, and which queries surface it. Surface this
    in the admin content dashboard so the topic backlog in Set 3 can learn from
    what actually worked.

11. E-E-A-T — author pages at /authors/[slug] with a photo, real credentials,
    links to other work, and every article they have written. A byline pointing
    at an empty page is worse than no byline.
```

**Why this order.** Run alongside Set 2. Retrofitting rendering and structured data after 40 articles exist is far more work than building it in.

---
---

# Set 6 — Conversion Layer

One prompt. Traffic that never converts is a cost, not an asset.

## PROMPT A — CTAs That Match the Reader

```text
PAGE: All Knowledge Base articles and the /insights index.

THE PROBLEM
The existing Knowledge Hub captures nothing. A visitor reads a nine-minute
whitepaper and leaves with no relationship and no next step. Every article
currently ends in nothing.

THE FIX

1. ONE PRIMARY CTA PER ARTICLE, matched to the topic. A generic "Get started"
   after a funding article wastes the intent the article just created:

     Funding / investor topics    → "Take the Founder Readiness Assessment"
     Validation / PMF topics      → "Start Mission 4: Validation"
     Legal / company setup        → "Download the legal setup checklist"
     MVP / building topics        → "Start Mission 10: Build MVP"
     Data reports                 → "Get the next report by email"
     Case studies                 → "Start free — 15 guided missions"

   Set the CTA per article in the content model. Never fall back to a site-wide
   default without a deliberate choice.

2. CTA PLACEMENT — three points, escalating, never intrusive:
     - Inline after roughly 40% of the article: a single quiet text link to the
       related mission or resource
     - End of article: the full CTA block, the primary conversion point
     - Sticky footer bar on mobile after 50% scroll, dismissible, appearing
       once per session

3. EMAIL CAPTURE — the highest-value action for a visitor not ready to sign up:
     - A quarterly-report subscription ("Get the State of MENA Founder Progress
       report") — a real, valuable thing rather than a generic newsletter
     - Whitepaper downloads: ungate most of them, gate only the flagship
       reports. Gating everything kills the SEO value you just built, because
       gated content cannot be crawled or linked to.
     - Single field, one click, clear statement of what arrives and how often
     - Double opt-in, and covered by the privacy policy

4. AUTH-AWARE CTAs — the same principle as the About page:
     Logged out → "Start free", "Take the assessment", "Download the report"
     Logged in  → "Start Mission 4", "Ask this in Community", "Save to my
                  resources"
   Never show a signed-in founder a signup CTA. Never show a logged-out visitor
   a CTA into a private route without explaining that sign-in is needed.

5. RELATED CONTENT — three related articles at the end, matched by topic AND
   by the reader's mission if signed in. Plus "Continue reading in this topic"
   pointing at the pillar page.

6. SHARE — Instagram Stories, LinkedIn, X and WhatsApp. WhatsApp matters more
   than every other channel in this region and is usually the one omitted. Use
   the generated OG image so shared links look right.

7. MEASURE — track per article: CTA impressions, CTA clicks, email captures,
   signups attributed, and mission starts attributed. Feed this back into the
   Set 3 topic backlog so the articles that actually convert shape what gets
   written next.

8. DO NOT: interstitial popups on entry (a Google mobile penalty and a bad
   experience), more than one email capture per page, or autoplay anything.
```

**Why this order.** Last. It needs articles to attach to, but build it before publishing volume — retrofitting CTAs across 40 articles is avoidable work.

---

## Suggested sequence

| Order | What | Why |
|---|---|---|
| 1 | Round 3 Set 1·A (routing) | Set 1·A here depends on the SHARED route type |
| 2 | Set 1·A | About page split — your explicit ask, small and self-contained |
| 3 | Set 2·A | Content model and template — everything downstream inherits it |
| 4 | Set 5·A | SEO foundation — build in, don't retrofit |
| 5 | Set 4·A | Data layer — the actual moat |
| 6 | Set 3·A | AI pipeline, with the review gate |
| 7 | Set 6·A | Conversion layer |

Steps 2 and 3 can run in parallel — they touch different routes.
