# -*- coding: utf-8 -*-
"""
The English half of the StartPad template library.

Ten downloadable tools, one file each. Every entry carries the same six parts:
what it is, why it earns its place, where it sits in the fifteen missions, where
it actually comes from, how to fill it in, and what "done well" looks like.

ON REFERENCES
The brief asked for a scientific reference on every template. Where a tool has a
clean scholarly origin it is cited plainly. Where the popular attribution is
wrong — SWOT is the loud example — the entry says so rather than repeating the
myth, because a readiness platform that issues proof cannot be careless about
provenance.

GRID SPEC
Each "grid" is a list of rows; each row a list of boxes:
    {"t": title, "q": prompt, "w": columns spanned, "h": rows spanned,
     "cm": row height in centimetres, "head": True for a band heading}
Column count per grid is given by "cols".
"""

EN = {

# ---------------------------------------------------------------- 1 ----------
"lean-canvas": {
 "name": "Lean Canvas",
 "tagline": "A whole business model on one page, built around the risk that kills it",
 "produces": "One page you can hand to anyone, with the riskiest part named",
 "what":
   "The Lean Canvas is a one-page business model for a company that does not exist "
   "yet. It replaces the business plan at the stage where a plan would be fiction. "
   "Where a traditional plan describes a future, this describes a set of guesses — "
   "and puts the most dangerous ones where you cannot avoid looking at them.",
 "purpose": [
   "Force a whole model into one page, so gaps become visible instead of hiding in "
   "paragraphs.",
   "Put Problem and Customer Segments first, because everything else is downstream "
   "of getting those two right.",
   "Surface the assumption that would sink the business, so you test that one first "
   "rather than the one that is easiest to test.",
   "Give you a single artefact an investor, a mentor or a programme reviewer can "
   "read in two minutes.",
 ],
 "missions": "Missions 5, 6 and 8 — idea selection, idea description, and the "
             "business model. Revisit it after Mission 12.",
 "ref_primary": "Maurya, A. (2012). Running Lean: Iterate from Plan A to a Plan "
                "That Works. 2nd ed. O'Reilly.",
 "ref_origin": "Adapted by Ash Maurya from the Business Model Canvas (Osterwalder "
               "& Pigneur, 2010), replacing four blocks — Key Partners, Key "
               "Activities, Key Resources and Customer Relationships — with "
               "Problem, Solution, Key Metrics and Unfair Advantage, on the "
               "argument that a startup's risk sits in problem and solution, not "
               "in operations it does not have yet.",
 "ref_further": [
   "Blank, S. (2013). Why the Lean Start-Up Changes Everything. Harvard Business "
   "Review, 91(5).",
   "Ries, E. (2011). The Lean Startup. Crown Business.",
 ],
 "how": [
   "Fill Customer Segments and Problem first, together. A problem with no named "
   "person attached is not a problem yet.",
   "Write Existing Alternatives inside the Problem box — what they do today, "
   "including doing nothing. This is your real competitor.",
   "Leave Solution until last among the top boxes. It is the block founders are "
   "most attached to and least sure about.",
   "Write the Unique Value Proposition as one sentence a customer would repeat to "
   "a friend, not a slogan.",
   "Circle the single box you are least sure about. That is your next experiment, "
   "and it belongs in Mission 7.",
   "Date the canvas. Fill a fresh one after each round of interviews rather than "
   "editing this one — the difference between versions is your learning.",
 ],
 "done_well": [
   "Every box is filled, and at least one says 'we do not know yet' out loud.",
   "The Problem box names what people do today instead of your product.",
   "Customer Segments names a specific group, not 'young people in Egypt'.",
   "You can point at the riskiest box without hesitating.",
 ],
 "cols": 10,
 "grid": [
  [{"t":"Problem","q":"The top three problems your customer has. Under each, write the existing alternative — what they do about it today, including nothing.","w":2,"h":2,"cm":7.0},
   {"t":"Solution","q":"The top three features. One line each. No more.","w":2,"h":1,"cm":3.5},
   {"t":"Unique Value Proposition","q":"One clear, compelling sentence that says why you are different and worth attention. Underneath: the high-level concept — 'the X for Y'.","w":2,"h":2,"cm":7.0},
   {"t":"Unfair Advantage","q":"Something that cannot be easily copied or bought. If you have none yet, write 'none yet' — that is an honest answer at this stage.","w":2,"h":1,"cm":3.5},
   {"t":"Customer Segments","q":"Who exactly. Name the segment and, separately, your early adopters — the sharpest version of that person.","w":2,"h":2,"cm":7.0}],
  [{"t":"Key Metrics","q":"The single number that tells you whether this is working. Not signups.","w":2,"h":1,"cm":3.5},
   {"t":"Channels","q":"Your path to customers. Free and paid. Which one will you test first?","w":2,"h":1,"cm":3.5}],
  [{"t":"Cost Structure","q":"What it costs to run the next three months. Fixed and variable. Be specific in EGP.","w":5,"h":1,"cm":4.0},
   {"t":"Revenue Streams","q":"Who pays, for what, how much, and how often. If nobody pays yet, write what you will charge and why.","w":5,"h":1,"cm":4.0}],
 ],
},

# ---------------------------------------------------------------- 2 ----------
"business-model-canvas": {
 "name": "Business Model Canvas",
 "tagline": "The nine building blocks of how an organisation creates, delivers and captures value",
 "produces": "A complete model of how the business runs, not only what it sells",
 "what":
   "The Business Model Canvas describes an entire business on one sheet through "
   "nine blocks. It is the more operational sibling of the Lean Canvas: where Lean "
   "Canvas is built for a company that does not exist, this one is built for a "
   "company that has to actually run — partners, activities, resources and "
   "relationships included.",
 "purpose": [
   "Show the whole machine at once, so you can see which parts you have not thought "
   "about at all.",
   "Separate value creation from value capture — many first models create real value "
   "and capture none of it.",
   "Make the cost side visible next to the revenue side on the same page.",
   "Give a shared language for a team or a mentor to argue about the model rather "
   "than the wording.",
 ],
 "missions": "Mission 8 primarily, feeding Missions 11 and 15.",
 "ref_primary": "Osterwalder, A. & Pigneur, Y. (2010). Business Model Generation. "
                "Wiley.",
 "ref_origin": "The nine blocks come from Alexander Osterwalder's doctoral thesis, "
               "The Business Model Ontology (University of Lausanne, 2004), "
               "supervised by Yves Pigneur — an attempt to give 'business model' a "
               "precise, comparable structure rather than leaving it a loose term.",
 "ref_further": [
   "Osterwalder, A., Pigneur, Y. & Tucci, C. (2005). Clarifying Business Models. "
   "Communications of the AIS, 16.",
   "Teece, D. J. (2010). Business Models, Business Strategy and Innovation. Long "
   "Range Planning, 43(2-3).",
 ],
 "how": [
   "Start at Customer Segments on the right, then Value Propositions. Work "
   "right-to-left; the left side exists to serve the right.",
   "Use one sticky note or one line per item. If a block needs a paragraph, it is "
   "two items.",
   "For each Value Proposition, draw a line to the segment it serves. Any "
   "proposition with no segment is a feature you like.",
   "Fill Revenue Streams before Cost Structure. Knowing what you can charge changes "
   "what you are willing to spend.",
   "Mark every block that is currently an assumption with a small (A).",
   "Count the (A)s. A model with more than half its blocks assumed is a hypothesis, "
   "and should be described as one.",
 ],
 "done_well": [
   "All nine blocks are filled and no block contains more than five items.",
   "Every value proposition is attached to a named segment.",
   "Revenue streams state the amount and frequency, not just the mechanism.",
   "Assumptions are marked, counted and honestly described.",
 ],
 "cols": 10,
 "grid": [
  [{"t":"Key Partners","q":"Who you need but will not build. Suppliers, distributors, institutions. What do they give you, and what do you give back?","w":2,"h":2,"cm":7.0},
   {"t":"Key Activities","q":"What the business must do well, every week, for the value proposition to hold.","w":2,"h":1,"cm":3.5},
   {"t":"Value Propositions","q":"What you deliver, and which customer problem it settles. One proposition per segment.","w":2,"h":2,"cm":7.0},
   {"t":"Customer Relationships","q":"What kind of relationship each segment expects — self-service, personal, community — and what it costs to maintain.","w":2,"h":1,"cm":3.5},
   {"t":"Customer Segments","q":"Who you create value for. Separate the segments that behave differently; do not merge them for tidiness.","w":2,"h":2,"cm":7.0}],
  [{"t":"Key Resources","q":"The assets the model cannot run without. People, technology, licence, data, capital.","w":2,"h":1,"cm":3.5},
   {"t":"Channels","q":"How each segment hears about you, buys, receives and gets support. Mark which are yours and which are borrowed.","w":2,"h":1,"cm":3.5}],
  [{"t":"Cost Structure","q":"What the model costs to operate. Which costs are fixed, which scale with customers, and what is the largest single line?","w":5,"h":1,"cm":4.0},
   {"t":"Revenue Streams","q":"What each segment pays for, the pricing mechanism, the amount and the frequency.","w":5,"h":1,"cm":4.0}],
 ],
},

# ---------------------------------------------------------------- 3 ----------
"value-proposition-canvas": {
 "name": "Value Proposition Canvas",
 "tagline": "Fit between what the customer is trying to do and what you have built",
 "produces": "A stated fit — and a list of the places where there is none",
 "what":
   "The Value Proposition Canvas zooms into two blocks of the Business Model Canvas "
   "— Customer Segments and Value Propositions — and asks whether they actually "
   "meet. The customer side is observed, never invented. The product side is "
   "designed to answer it. Fit is the moment a specific pain reliever lines up with "
   "a pain the customer already told you about.",
 "purpose": [
   "Stop the common failure where a product solves a problem nobody ranked as "
   "important.",
   "Separate what a customer is trying to get done from the features you built.",
   "Rank pains and gains rather than listing them, so you build against severity.",
   "Give a defensible answer to 'why would anyone switch to this?'",
 ],
 "missions": "Missions 6 and 11, and again in Mission 12 once you have market "
             "evidence.",
 "ref_primary": "Osterwalder, A., Pigneur, Y., Bernarda, G. & Smith, A. (2014). "
                "Value Proposition Design. Wiley.",
 "ref_origin": "Built on the jobs-to-be-done lens — the idea that customers 'hire' "
               "a product to make progress in a circumstance — developed by "
               "Clayton Christensen and colleagues, and on Anthony Ulwick's "
               "outcome-driven work on measuring the importance and satisfaction "
               "of desired outcomes.",
 "ref_further": [
   "Christensen, C. M., Hall, T., Dillon, K. & Duncan, D. S. (2016). Know Your "
   "Customers' Jobs to Be Done. Harvard Business Review, 94(9).",
   "Ulwick, A. (2002). Turn Customer Input into Innovation. Harvard Business "
   "Review, 80(1).",
 ],
 "how": [
   "Fill the customer side first, and fill it only with things people actually said "
   "in interviews. Anything you inferred, mark with a question mark.",
   "Write jobs as verbs in a situation: 'get paid by a client who keeps delaying', "
   "not 'invoicing'.",
   "Rank pains from severe to moderate, and gains from essential to nice. Unranked "
   "lists hide the decision.",
   "Only then design the product side, item by item, against the ranked pains.",
   "Draw a line from each pain reliever to the exact pain it answers. Unlinked "
   "items are features you wanted to build.",
   "Write the fit statement at the bottom in one sentence, and check it against a "
   "real customer.",
 ],
 "done_well": [
   "Every item on the customer side traces to a specific interview.",
   "Pains and gains are ranked, not just listed.",
   "At least one severe pain has a matching reliever — and the match is not a "
   "stretch.",
   "The fit statement survives being read aloud to a customer without explanation.",
 ],
 "cols": 6,
 "grid": [
  [{"t":"CUSTOMER PROFILE — what you observed","q":"","w":3,"h":1,"cm":0.8,"head":True},
   {"t":"VALUE MAP — what you designed","q":"","w":3,"h":1,"cm":0.8,"head":True}],
  [{"t":"Customer jobs","q":"What are they trying to get done? Functional, social and emotional. Write each as a verb in a situation.","w":3,"h":1,"cm":5.5},
   {"t":"Products and services","q":"What you offer, listed plainly. Which job does each one serve?","w":3,"h":1,"cm":5.5}],
  [{"t":"Pains","q":"What goes wrong, costs them, or blocks the job. Rank: severe / moderate / mild.","w":3,"h":1,"cm":5.5},
   {"t":"Pain relievers","q":"Exactly how you remove or reduce each pain. Draw a line to the pain it answers.","w":3,"h":1,"cm":5.5}],
  [{"t":"Gains","q":"The outcomes and benefits they want. Rank: essential / expected / desired.","w":3,"h":1,"cm":5.5},
   {"t":"Gain creators","q":"How you produce those outcomes. Be concrete — 'faster' is not a gain creator.","w":3,"h":1,"cm":5.5}],
  [{"t":"Fit statement","q":"In one sentence: our [offer] helps [segment] who want to [job] by [pain reliever / gain creator], unlike [existing alternative].","w":6,"h":1,"cm":3.2}],
 ],
},

# ---------------------------------------------------------------- 4 ----------
"customer-persona": {
 "name": "Customer Persona",
 "tagline": "One specific person, built from evidence, that the whole team can picture",
 "produces": "A persona with the interview count that backs it printed on its face",
 "what":
   "A persona is a single fictional person assembled from real research, standing "
   "in for a segment that behaves the same way. Its job is to end arguments: when a "
   "team disagrees about a feature, the persona settles it. A persona invented in a "
   "meeting does the opposite — it makes a guess feel like a fact, which is why this "
   "template asks for the evidence on the page.",
 "purpose": [
   "Replace 'the user' with someone specific enough to disagree with.",
   "Carry research into every later decision without re-reading the transcripts.",
   "Expose the segments you are quietly designing for and the ones you are ignoring.",
   "Make an unfounded persona obvious, by printing its evidence base next to it.",
 ],
 "missions": "Missions 2 and 4, reused in Missions 11, 12 and 15.",
 "ref_primary": "Cooper, A. (1999). The Inmates Are Running the Asylum. Sams.",
 "ref_origin": "Alan Cooper developed personas while designing software in the "
               "1980s, and set them out formally in 1999. The method was later "
               "tightened by Pruitt and Adlin, who insisted personas be grounded "
               "in and traceable to primary data rather than composed from "
               "impressions.",
 "ref_further": [
   "Pruitt, J. & Adlin, T. (2006). The Persona Lifecycle. Morgan Kaufmann.",
   "Chapman, C. N. & Milham, R. P. (2006). The Personas' New Clothes: "
   "Methodological and Practical Arguments Against a Popular Method. Proceedings "
   "of the Human Factors and Ergonomics Society.",
 ],
 "how": [
   "Do not open this template until you have completed at least five interviews "
   "with the same kind of person.",
   "Build the persona from patterns that appeared in three or more of them. "
   "One vivid interview is an anecdote.",
   "Give them a name and an age, and keep the details that change a decision. Drop "
   "the ones that do not.",
   "Use a real quote, word for word, from a real interview. Never write the quote "
   "yourself.",
   "Fill the evidence box honestly: how many interviews, when, and where these "
   "people were found.",
   "Write one persona per file. Two personas in one document always collapse into "
   "an average of both.",
 ],
 "done_well": [
   "The evidence box names a real number of real interviews.",
   "The quote is verbatim and slightly awkward, the way real speech is.",
   "Someone outside the team could use it to reject a feature idea.",
   "Nothing in it is there only because it sounded good.",
 ],
 "cols": 4,
 "grid": [
  [{"t":"Persona name and age","q":"A real first name, an age, and the one line that captures them.","w":2,"h":1,"cm":3.0},
   {"t":"Segment","q":"Which customer segment does this person represent, and roughly how many people are like them?","w":2,"h":1,"cm":3.0}],
  [{"t":"Who they are","q":"Work, study, income, city, living situation — only what affects the decision you are designing for.","w":2,"h":1,"cm":5.0},
   {"t":"A day in their life","q":"Walk through the part of the day where your problem shows up. Where are they, what device, who else is there?","w":2,"h":1,"cm":5.0}],
  [{"t":"What they are trying to get done","q":"Their jobs, in their words. Functional and emotional.","w":2,"h":1,"cm":5.0},
   {"t":"What gets in the way","q":"Frustrations, costs, the workaround they have settled for. Which one did they complain about first?","w":2,"h":1,"cm":5.0}],
  [{"t":"What good looks like to them","q":"The outcome they would call a success — in their terms, not your metrics.","w":2,"h":1,"cm":5.0},
   {"t":"Where you can reach them","q":"Platforms, places, people they trust. Where do they already go to solve this?","w":2,"h":1,"cm":5.0}],
  [{"t":"In their own words","q":"One verbatim quote from a real interview. Keep the hesitation and the grammar.","w":4,"h":1,"cm":3.2}],
  [{"t":"Evidence behind this persona","q":"How many interviews, on what dates, recruited how. Which parts of this persona are still assumption?","w":4,"h":1,"cm":3.2}],
 ],
},

# ---------------------------------------------------------------- 5 ----------
"interview-script-log": {
 "name": "Customer Interview Script & Evidence Log",
 "tagline": "Questions that survive contact with a polite stranger, and a log that proves you asked them",
 "produces": "A usable script and a logged, checkable record of every conversation",
 "what":
   "Two things in one file: a script that keeps you asking about the customer's "
   "past instead of your idea's future, and a log that records each conversation in "
   "a form somebody else can verify. Most first-time founders do not fail at "
   "interviewing because they are shy. They fail because they pitch, and people are "
   "kind.",
 "purpose": [
   "Get truthful answers by asking about behaviour that already happened rather than "
   "intentions that have not.",
   "Stop the interview from turning into a demo, which teaches you nothing.",
   "Produce a record — names, dates, channels — that turns a claim into evidence.",
   "Make consent explicit before you write down anything about another person.",
 ],
 "missions": "Missions 1, 2 and 3, and again in Missions 7, 10, 12 and 14.",
 "ref_primary": "Fitzpatrick, R. (2013). The Mom Test: How to Talk to Customers and "
                "Learn If Your Business Is a Good Idea When Everyone Is Lying to "
                "You. Founder Centric.",
 "ref_origin": "The underlying discipline is customer discovery, set out by Steve "
               "Blank as the first step of customer development — the founder "
               "leaves the building and tests the hypotheses before building. "
               "The Mom Test is the practical rule set that keeps those "
               "conversations honest.",
 "ref_further": [
   "Blank, S. (2005). The Four Steps to the Epiphany. K&S Ranch.",
   "Portigal, S. (2013). Interviewing Users. Rosenfeld Media.",
 ],
 "how": [
   "Do not describe your idea. If they ask, say you are researching the problem and "
   "will show them later.",
   "Ask about the last time it happened, not whether it usually happens. Memory of a "
   "specific event is far more reliable than a general claim.",
   "Follow every complaint with 'what did you do about it?' — behaviour, not opinion.",
   "Ask what it cost them: money, hours, missed work, an argument. Magnitude "
   "separates a nuisance from a problem.",
   "Say nothing after a question for five seconds. The second sentence is usually the "
   "true one.",
   "Fill the log within an hour, while you still remember the tone. Log the "
   "consent tick at the same time.",
 ],
 "done_well": [
   "You can quote three specific things people said that you did not expect.",
   "At least one interview changed your mind about something.",
   "Every row of the log is complete, including consent.",
   "Nobody was asked whether they 'would use' your product.",
 ],
 "cols": 2,
 "grid": [
  [{"t":"THE SCRIPT","q":"","w":2,"h":1,"cm":0.8,"head":True}],
  [{"t":"Opening — 20 seconds","q":"Who you are, that you are researching a problem not selling, how long it will take, and permission to take notes.","w":2,"h":1,"cm":3.0}],
  [{"t":"Warm-up — their context","q":"Two questions about their situation and role. Nothing about your idea.","w":2,"h":1,"cm":3.0}],
  [{"t":"The last time it happened","q":"Write three questions about a specific recent occurrence. 'Tell me about the last time you had to…'","w":2,"h":1,"cm":4.2}],
  [{"t":"What they did about it","q":"Three questions about the workaround, the tool, the person they asked, or the decision to do nothing.","w":2,"h":1,"cm":4.2}],
  [{"t":"What it cost them","q":"Two questions about magnitude — time, money, consequence, how often.","w":2,"h":1,"cm":3.6}],
  [{"t":"Close","q":"Who else should I speak to? May I come back to you? Consent to be contacted for verification.","w":2,"h":1,"cm":3.0}],
 ],
 "log": {
   "title": "EVIDENCE LOG",
   "note": "One row per conversation. Complete it within the hour. Consent must be "
           "ticked before any detail is written down.",
   "cols": ["#","First name","City","Date","Channel","Consent","The problem in their words","What surprised you","What they did about it"],
   "widths": [0.9, 2.2, 1.9, 1.9, 1.9, 1.5, 4.2, 3.4, 3.4],
   "rows": 14,
 },
},

# ---------------------------------------------------------------- 6 ----------
"importance-frequency-matrix": {
 "name": "Importance–Frequency Matrix",
 "tagline": "Which problem to solve first, decided on evidence instead of enthusiasm",
 "produces": "A ranked problem list and one problem chosen, with the reason written down",
 "what":
   "A grid that scores each candidate problem on how much it matters when it happens "
   "and how often it happens, then places it in one of four quadrants. A severe "
   "problem that occurs twice a year and a mild one that occurs daily are different "
   "businesses. This template stops you choosing between them by instinct.",
 "purpose": [
   "Turn a list of problems into a ranked list with a defensible order.",
   "Expose the rare-but-painful problems that feel urgent in an interview and do not "
   "support a business.",
   "Record the current workaround for each problem — the thing you are really "
   "competing with.",
   "Leave a written reason for the problem you chose, so a later pivot is a decision "
   "rather than a drift.",
 ],
 "missions": "Mission 3 directly; feeds Missions 4 and 5.",
 "ref_primary": "Ulwick, A. (2002). Turn Customer Input into Innovation. Harvard "
                "Business Review, 80(1). — the opportunity algorithm, which scores "
                "desired outcomes by importance and satisfaction.",
 "ref_origin": "The two-axis prioritisation grid is a working adaptation rather "
               "than a single named theory. Its closest scholarly anchors are "
               "Ulwick's outcome-driven innovation, which ranks outcomes by "
               "importance against satisfaction, and the Kano model, which shows "
               "that attributes differ in kind and not only in degree. "
               "Substituting frequency for satisfaction suits early-stage work, "
               "where satisfaction data does not exist yet.",
 "ref_further": [
   "Kano, N., Seraku, N., Takahashi, F. & Tsuji, S. (1984). Attractive Quality and "
   "Must-Be Quality. Journal of the Japanese Society for Quality Control, 14(2).",
   "Bettencourt, L. A. & Ulwick, A. W. (2008). The Customer-Centered Innovation "
   "Map. Harvard Business Review, 86(5).",
 ],
 "how": [
   "List only problems you heard in interviews. A problem you thought of does not "
   "get a row.",
   "Score importance 1–5 on consequence when it occurs, and frequency 1–5 on how "
   "often. Use the interview evidence, not your impression.",
   "Write the current workaround for every row. If there is no workaround, check "
   "the problem is real.",
   "Plot each problem in the quadrant grid on the next page.",
   "Choose one problem from the top-right quadrant and write the reason underneath.",
   "Keep the rejected problems. They are your second and third options if the first "
   "fails validation.",
 ],
 "done_well": [
   "Every row traces to a named interview.",
   "Scores differ from each other — if everything is a 5, nothing was measured.",
   "The chosen problem sits in the high-importance, high-frequency quadrant, or the "
   "exception is argued explicitly.",
   "The workaround column is complete.",
 ],
 "cols": 2,
 "grid": [
  [{"t":"HOW TO SCORE","q":"","w":2,"h":1,"cm":0.8,"head":True}],
  [{"t":"Importance 1–5","q":"1 = mildly annoying · 3 = costs real time or money · 5 = blocks something they must do. Judge by what it cost them, not how loudly they said it.","w":1,"h":1,"cm":3.0},
   {"t":"Frequency 1–5","q":"1 = once a year or less · 3 = monthly · 5 = daily or more. Count occurrences they described, not ones they expect.","w":1,"h":1,"cm":3.0}],
 ],
 "log": {
   "title": "PROBLEM SCORING",
   "note": "One row per problem heard in interviews. Score = importance × frequency.",
   "cols": ["#","The problem, in their words","Who has it","Importance 1–5","Frequency 1–5","Score","What they do today instead"],
   "widths": [0.9, 5.4, 2.8, 2.1, 2.1, 1.5, 5.0],
   "rows": 10,
 },
 "grid2_title": "THE MATRIX",
 "cols2": 2,
 "grid2": [
  [{"t":"High importance · Low frequency","q":"Real pain, rare. Usually a service or an insurance-shaped product, not a daily tool. Plot problems here.","w":1,"h":1,"cm":6.0},
   {"t":"High importance · High frequency  ←  build here","q":"Severe and constant. This is where a first product belongs. Plot problems here.","w":1,"h":1,"cm":6.0}],
  [{"t":"Low importance · Low frequency","q":"Ignore. Politely.","w":1,"h":1,"cm":6.0},
   {"t":"Low importance · High frequency","q":"Frequent irritation. Can work as a free hook, rarely as a paid product on its own. Plot problems here.","w":1,"h":1,"cm":6.0}],
  [{"t":"The problem we are taking forward, and why","q":"Name it, give its score, and write the reason in two sentences. Date this.","w":2,"h":1,"cm":3.6}],
 ],
},
}

# ---------------------------------------------------------------- 7 ----------
EN["swot-tows"] = {
 "name": "SWOT & TOWS Analysis",
 "tagline": "Four lists are a warm-up; the pairings are the actual work",
 "produces": "A SWOT that ends in four strategies, not four lists",
 "what":
   "SWOT sets your internal strengths and weaknesses against external opportunities "
   "and threats. On its own it produces four columns and no decision, which is why "
   "it has a poor reputation. This template includes the step that rescues it: the "
   "TOWS matrix, which pairs the quadrants into strategies — use this strength on "
   "that opportunity, defend this weakness against that threat.",
 "purpose": [
   "Separate what is inside your control from what is not, which founders routinely "
   "mix.",
   "Force each entry to be specific enough to act on.",
   "Convert the four lists into four strategy types through deliberate pairing.",
   "Give a mentor or a committee a structure they already know how to read.",
 ],
 "missions": "Mission 5, and revisited before Mission 15.",
 "ref_primary": "Weihrich, H. (1982). The TOWS Matrix: A Tool for Situational "
                "Analysis. Long Range Planning, 15(2), 54-66.",
 "ref_origin": "SWOT is widely credited to Albert Humphrey at Stanford Research "
               "Institute in the 1960s, developing from an earlier SOFT framework. "
               "The frequent claim that it originated at Harvard with Learned, "
               "Christensen, Andrews and Guth (1965) is not supported: that book "
               "uses the four words but never presents SWOT as a tool, and Guth "
               "himself denied the attribution. Recent historical work in Long "
               "Range Planning and the Journal of Management History traces the "
               "line from SOFT to SWOT. Treat any confident single-origin story "
               "with suspicion.",
 "ref_further": [
   "Puyt, R. W., Lie, F. B. & Wilderom, C. P. M. (2023). The Origins of SWOT "
   "Analysis. Long Range Planning, 56(3).",
   "Learned, E., Christensen, C. R., Andrews, K. & Guth, W. (1965). Business "
   "Policy: Text and Cases. Irwin. — the LCAG framework, often miscited as SWOT.",
 ],
 "how": [
   "Fix the subject first. SWOT of what — the company, one product, one market? An "
   "unfixed subject produces unusable lists.",
   "Strengths and weaknesses are internal and present tense. If you cannot change "
   "it, it belongs on the right-hand side.",
   "Opportunities and threats are external and future-facing. Name the source: a "
   "regulation, a competitor, a cost, a behaviour change.",
   "Be specific. 'Good team' is not a strength; 'two engineers who have shipped a "
   "payments integration before' is.",
   "Cap each quadrant at five entries, ranked. A list of twelve is a way of "
   "avoiding the ranking.",
   "Do the TOWS pairings. This is the part that produces decisions, and the part "
   "most people skip.",
 ],
 "done_well": [
   "Nothing appears in two quadrants at once.",
   "Every entry is specific enough that someone could disagree with it.",
   "All four TOWS boxes contain a real action with an owner.",
   "At least one pairing surprised you.",
 ],
 "cols": 2,
 "grid": [
  [{"t":"Subject of this analysis","q":"The company, product or market this SWOT is about, and the date. One subject only.","w":2,"h":1,"cm":2.4}],
  [{"t":"Strengths — internal, present","q":"What you have that others do not. Team, access, cost position, relationships, data, speed. Rank the top five.","w":1,"h":1,"cm":6.5},
   {"t":"Weaknesses — internal, present","q":"What you lack or do badly. Be honest; this page is not a pitch. Rank the top five.","w":1,"h":1,"cm":6.5}],
  [{"t":"Opportunities — external, future","q":"Shifts you could ride: regulation, behaviour, cost, a gap a competitor left. Name the source of each.","w":1,"h":1,"cm":6.5},
   {"t":"Threats — external, future","q":"What could damage the plan: an incumbent, a rule, a price, a platform you depend on. Name the source of each.","w":1,"h":1,"cm":6.5}],
 ],
 "grid2_title": "TOWS — THE PAIRINGS THAT PRODUCE STRATEGY",
 "cols2": 2,
 "grid2": [
  [{"t":"SO — strength on opportunity","q":"Which strength lets you take which opportunity faster than anyone else? Write the action and who owns it.","w":1,"h":1,"cm":5.5},
   {"t":"WO — fix a weakness to reach an opportunity","q":"Which weakness is blocking an opportunity worth the cost of fixing? What is the fix?","w":1,"h":1,"cm":5.5}],
  [{"t":"ST — strength against threat","q":"Which strength reduces which threat? What would you do the week the threat arrives?","w":1,"h":1,"cm":5.5},
   {"t":"WT — weakness exposed to threat","q":"Where a weakness meets a threat, you avoid, insure or exit. Which is it, and by when?","w":1,"h":1,"cm":5.5}],
  [{"t":"The one thing this analysis changes","q":"If this SWOT changes nothing in your plan, it was a writing exercise. What is different now?","w":2,"h":1,"cm":3.2}],
 ],
}

# ---------------------------------------------------------------- 8 ----------
EN["pestel"] = {
 "name": "PESTEL Analysis",
 "tagline": "The six outside forces that will act on your plan whether you look at them or not",
 "produces": "Six scanned factors, three that matter, and a watch list with dates",
 "what":
   "PESTEL scans the macro environment a business sits inside: political, economic, "
   "social, technological, environmental and legal. It is not a strategy tool — it "
   "is an input. Its value is catching the force that makes a plan impossible, or "
   "suddenly possible, before you have spent a year on the plan.",
 "purpose": [
   "Surface the regulation, cost or platform dependency that decides the business "
   "before the product does.",
   "Separate forces you can plan around from forces you can only watch.",
   "Anchor market assumptions to something outside your own optimism.",
   "Produce a watch list with dates, so a macro change registers when it happens "
   "rather than a year later.",
 ],
 "missions": "Missions 2 and 12, and before any funding conversation.",
 "ref_primary": "Aguilar, F. J. (1967). Scanning the Business Environment. "
                "Macmillan.",
 "ref_origin": "Aguilar, then at Harvard Business School, proposed ETPS — "
               "Economic, Technical, Political, Social — as a taxonomy for the "
               "external information managers actually use. It was later reordered "
               "to PEST and extended with Legal and Environmental factors as "
               "compliance and sustainability became material, giving PESTEL. The "
               "extensions have no single author.",
 "ref_further": [
   "Fahey, L. & Narayanan, V. K. (1986). Macroenvironmental Analysis for Strategic "
   "Management. West Publishing.",
   "Porter, M. E. (1980). Competitive Strategy. Free Press. — for the industry "
   "layer that sits beneath the macro layer.",
 ],
 "how": [
   "Set the boundary: which country, which market, which time horizon. PESTEL "
   "without a boundary generates infinite factors.",
   "Write only factors with a plausible path to your business. 'Inflation' is "
   "background; 'import duty on the component we need' is a factor.",
   "For each, state the direction and the effect on you: what changes, and whether "
   "it helps or hurts.",
   "Mark each factor as watch, plan or act. Most are watch — that is the correct "
   "result, not a failure.",
   "Pick the three that would actually change your plan and write them at the "
   "bottom.",
   "Give each of those three a source to check and a date to check it. A scan with "
   "no review date expires silently.",
 ],
 "done_well": [
   "Every factor names a concrete thing, with a direction.",
   "Each factor is tagged watch, plan or act.",
   "The three that matter are identified and justified.",
   "The watch list has named sources and review dates.",
 ],
 "cols": 3,
 "grid": [
  [{"t":"Scope","q":"Country, market, and time horizon this scan covers. Date it.","w":3,"h":1,"cm":2.2}],
  [{"t":"Political","q":"Government priorities, subsidies, procurement, stability, trade posture. What is changing, and does it help or hurt?","w":1,"h":1,"cm":6.0},
   {"t":"Economic","q":"Inflation, currency, credit, purchasing power, employment. What does it do to your price and your cost?","w":1,"h":1,"cm":6.0},
   {"t":"Social","q":"Demographics, education, habits, trust, who decides in a household. What behaviour is shifting?","w":1,"h":1,"cm":6.0}],
  [{"t":"Technological","q":"Infrastructure, device and payment penetration, platforms you depend on, what just got cheap.","w":1,"h":1,"cm":6.0},
   {"t":"Environmental","q":"Resources, climate pressure, energy cost and reliability, waste rules, customer expectations.","w":1,"h":1,"cm":6.0},
   {"t":"Legal","q":"Licensing, company formation, data protection, consumer and labour law, sector regulation. Name the actual instrument.","w":1,"h":1,"cm":6.0}],
  [{"t":"The three that change the plan","q":"Which three factors would make you do something different? Say what you would do.","w":2,"h":1,"cm":4.0},
   {"t":"Watch list","q":"For each of the three: the source you will check, and the date you will check it.","w":1,"h":1,"cm":4.0}],
 ],
}

# ---------------------------------------------------------------- 9 ----------
EN["moat-five-forces"] = {
 "name": "Competitive Moat & Five Forces",
 "tagline": "Why this stays yours after it works",
 "produces": "An honest read of the industry, and a named moat with a time horizon",
 "what":
   "Two linked questions. First: how much profit does this industry allow anyone to "
   "keep — Porter's five forces. Second: what would stop a better-funded competitor "
   "taking your position once you have proved it works — the moat. Early-stage "
   "founders usually answer the second with 'execution', which is not a moat; it is "
   "the absence of one.",
 "purpose": [
   "Judge the structure of the industry before blaming yourself for its margins.",
   "Identify who actually captures the value: you, the platform, or the buyer.",
   "Name a moat that is a property of the business rather than an attribute of the "
   "team.",
   "Answer the investor question 'what stops someone copying this?' with something "
   "checkable.",
 ],
 "missions": "Missions 4 and 5, and again before Mission 15.",
 "ref_primary": "Porter, M. E. (1979). How Competitive Forces Shape Strategy. "
                "Harvard Business Review, 57(2), 137-145.",
 "ref_origin": "Porter's five forces come from industrial organisation economics, "
               "particularly the structure-conduct-performance tradition. The "
               "resource-based view supplies the other half: Barney's VRIN test "
               "(valuable, rare, inimitable, non-substitutable) explains why some "
               "advantages last. 'Moat' is Warren Buffett's investing metaphor for "
               "the same idea, not an academic term — useful shorthand, weak "
               "evidence on its own.",
 "ref_further": [
   "Barney, J. (1991). Firm Resources and Sustained Competitive Advantage. Journal "
   "of Management, 17(1), 99-120.",
   "Porter, M. E. (2008). The Five Competitive Forces That Shape Strategy. Harvard "
   "Business Review, 86(1). — Porter's own revision.",
 ],
 "how": [
   "Define the industry narrowly enough to be real. 'Technology' has no five "
   "forces; 'last-mile delivery for pharmacies in Greater Cairo' does.",
   "Rate each force high, medium or low, and write the reason. The reason matters "
   "more than the rating.",
   "For buyers and suppliers, ask who can walk away more cheaply. That is where the "
   "power sits.",
   "In the moat table, mark only what you have today. Aspirations go in the last "
   "column with a date.",
   "Apply the VRIN test to anything you claimed: is it valuable, rare, hard to "
   "imitate, and hard to substitute?",
   "If every moat row is empty, say so. An honest 'none yet, here is the plan' "
   "reads better than a claimed moat a reviewer can puncture in one question.",
 ],
 "done_well": [
   "Each force has a rating and a one-sentence reason.",
   "The moat table distinguishes what you have from what you intend.",
   "At least one row survives the VRIN test, or you state plainly that none does.",
   "'Execution' and 'first mover' appear nowhere as a moat.",
 ],
 "cols": 3,
 "grid": [
  [{"t":"Industry, defined narrowly","q":"The specific market this analysis covers. Segment, geography, buyer type.","w":3,"h":1,"cm":2.2}],
  [{"t":"Threat of new entrants","q":"How hard is it to start? Capital, licence, brand, distribution. Who could enter next year? Rating and reason.","w":3,"h":1,"cm":4.6}],
  [{"t":"Bargaining power of buyers","q":"Are buyers concentrated, price-sensitive, able to switch cheaply? Rating and reason.","w":1,"h":1,"cm":5.6},
   {"t":"Competitive rivalry","q":"How many, how similar, how fast growing is the market, how are they competing — price or something else? Rating and reason.","w":1,"h":1,"cm":5.6},
   {"t":"Bargaining power of suppliers","q":"Few suppliers, unique inputs, a platform you cannot leave? Rating and reason.","w":1,"h":1,"cm":5.6}],
  [{"t":"Threat of substitutes","q":"What else solves this job, including a spreadsheet, a WhatsApp group, or doing nothing? Rating and reason.","w":3,"h":1,"cm":4.6}],
 ],
 "log": {
   "title": "THE MOAT",
   "note": "Mark only what you have today. VRIN: valuable, rare, inimitable, "
           "non-substitutable — all four, or it is not a moat.",
   "cols": ["Moat type","Do you have it today?","Evidence","Passes VRIN?","How long does it hold — and what would you do to build it"],
   "widths": [4.2, 3.0, 4.6, 2.6, 6.2],
   "rows": 0,
   "seed": [
     ["Network effects — each user makes it better for the next","","","",""],
     ["Switching costs — leaving is expensive or painful","","","",""],
     ["Cost advantage — you can serve cheaper, structurally","","","",""],
     ["Intangible assets — brand, licence, patent, exclusivity","","","",""],
     ["Efficient scale — the market only supports one or two","","","",""],
     ["Data — accumulating and hard to replicate","","","",""],
     ["Distribution — a channel others cannot access","","","",""],
   ],
 },
}

# --------------------------------------------------------------- 10 ----------
EN["market-sizing"] = {
 "name": "Market Sizing — TAM, SAM, SOM",
 "tagline": "A number you can defend, built from the bottom up",
 "produces": "Three sized figures, the arithmetic behind them, and the assumption that breaks them",
 "what":
   "TAM is everyone who could ever buy this. SAM is the part you could serve with "
   "your model, in your geography. SOM is what you could realistically win in three "
   "years. The purpose is not a big number — it is a defensible one. A bottom-up "
   "figure with visible arithmetic beats a top-down figure taken from a report, "
   "every time, in front of anyone who has done this before.",
 "purpose": [
   "Show whether the business can ever be large enough to be worth the years it "
   "will take.",
   "Replace a cited market report with arithmetic a reader can check line by line.",
   "Expose the one assumption the whole number rests on.",
   "Give a realistic three-year target instead of '1% of a huge market', which "
   "signals inexperience immediately.",
 ],
 "missions": "Missions 4 and 12, and required for any pitch.",
 "ref_primary": "Blank, S. & Dorf, B. (2012). The Startup Owner's Manual. K&S "
                "Ranch. — market size and type in customer discovery.",
 "ref_origin": "The bottom-up method is Fermi estimation: decompose an unknown "
               "quantity into quantities you can estimate or count, and multiply. "
               "The discipline is old and comes from physics, not business — its "
               "value here is that every step is inspectable, so a reader can "
               "challenge one assumption instead of rejecting the whole figure.",
 "ref_further": [
   "Mullins, J. (2003). The New Business Road Test. FT Prentice Hall.",
   "Weinstein, L. & Adam, J. (2008). Guesstimation. Princeton University Press.",
 ],
 "how": [
   "Do the bottom-up calculation first: number of potential customers x price x "
   "purchase frequency per year. Show every figure.",
   "Source each figure. A government statistic, a census, a platform's published "
   "number, or your own count — with the date.",
   "Do a top-down estimate separately as a sanity check. If the two differ by more "
   "than 10x, one of them is wrong; find out which.",
   "Work in EGP and give the USD equivalent with the rate and date you used.",
   "State the assumption the whole number depends on — usually price or adoption "
   "rate — and what the number becomes if you halve it.",
   "Set SOM against a real constraint: your channel, your capacity, your funding. "
   "Not a percentage of SAM.",
 ],
 "done_well": [
   "Every number has a source and a date next to it.",
   "The arithmetic is visible and a reader can redo it.",
   "SOM is justified by a constraint, not by a percentage.",
   "The breaking assumption is named, with the halved case shown.",
 ],
 "cols": 3,
 "grid": [
  [{"t":"TAM — total addressable market","q":"Everyone who could buy this, anywhere, if you had no limits. Definition, number, and how you got it.","w":3,"h":1,"cm":4.4}],
  [{"t":"SAM — serviceable available market","q":"The part your model and geography can actually reach. What did you exclude, and why?","w":3,"h":1,"cm":4.4}],
  [{"t":"SOM — serviceable obtainable market","q":"What you can realistically win in three years, limited by channel, capacity or capital. Name the constraint.","w":3,"h":1,"cm":4.4}],
 ],
 "log": {
   "title": "BOTTOM-UP CALCULATION",
   "note": "Customers x price x frequency. Every figure gets a source and a date.",
   "cols": ["Step","Figure","Where it came from","Date of source","Running total"],
   "widths": [6.0, 3.0, 5.4, 2.6, 3.4],
   "rows": 0,
   "seed": [
     ["Population or universe of the segment","","","",""],
     ["% that fit the definition","","","",""],
     ["= Potential customers","","","",""],
     ["Price per purchase (EGP)","","","",""],
     ["Purchases per customer per year","","","",""],
     ["= Annual market value (EGP)","","","",""],
     ["Top-down sanity check — same figure, different route","","","",""],
   ],
 },
 "grid2_title": "WHAT BREAKS THE NUMBER",
 "cols2": 2,
 "grid2": [
  [{"t":"The assumption everything rests on","q":"Which single figure, if wrong, changes the answer most? Usually price or adoption.","w":1,"h":1,"cm":4.4},
   {"t":"Halve it — what happens?","q":"Recalculate with that assumption cut in half. Is the business still worth doing?","w":1,"h":1,"cm":4.4}],
  [{"t":"Currency and date","q":"EGP figures, the USD rate used, and the date. Market numbers age faster than founders expect.","w":2,"h":1,"cm":2.6}],
 ],
}
