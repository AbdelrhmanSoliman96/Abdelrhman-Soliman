"""
Review 01 — the camp's content matched to the StartPad missions.

A partner note, not a published founder resource. It stays out of the public
resources bundle and is addressed to GrowthLabs, Cognify Academy and the host
university.

It is a map rather than an argument: every deliverable the camp's design pack lists,
against the mission that receives it and the questions that mission actually asks.
Checked against `startpad/missions.py` — titles and question sets — and against the
pack's own per-day deliverable list, so the counts at the top are countable from the
table below them.
"""

PACK = "Entrepreneurship Camp Learner Journey, GrowthLabs Group × Cognify Academy, September 2026"

DOC = {
    "slug": "rv01-camp-integration",
    "file": "StartPad_Review_01_Content_Match",
    "kind": "review",
    "layout": "brief",
    "max_pages": 2,
    "series": "StartPad Programme Review",
    "number": "No. 01",
    "title": "The Camp, Matched to the Missions",
    "standfirst": "Every deliverable the camp produces, against the mission that "
                  "receives it — and what to do about the four that have nowhere to go.",
    "standfirst_plain": "Each Future Founders camp deliverable matched to the "
                        "StartPad mission that receives it.",
    "cover_foot": "For GrowthLabs, Cognify Academy and the university",
    "keywords": ["curriculum mapping", "StartPad missions", "entrepreneurship "
                 "education", "camp content", "GrowthLabs"],
    "missions": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "blocks": [

        ("p", "The camp's twenty deliverables were matched one by one to the fifteen "
              "missions and to the questions each mission actually asks. <b>Seven "
              "match directly</b> and need nothing. <b>Four match with a "
              "divergence</b> the facilitator should know about before Day 1. "
              "<b>Five have no mission and should</b> — between them they are 50% "
              "of the Bazaar rubric. The remaining four are camp-only by design and "
              "need no mission at all."),

        ("table", ["Day", "What the camp produces", "Mission", "What that mission asks for", "Match"], [
            ["1", "Problem cards", "01 Problem Analysis",
             "Area, the problem, who is affected, what solutions exist and their limits", "Partial"],
            ["1", "Chosen problem on Impact × Frequency", "03 Importance/Frequency Matrix",
             "Three problems, each scored for importance and frequency", "Direct"],
            ["1", "First persona", "02 Problem Definition",
             "Primary user, characteristics, the problem, when and where, how often", "Direct"],
            ["1", "Team charter", "—", "Roles and working rules stay in the workbook", "Camp only"],
            ["2", "Interview log", "—",
             "Feeds mission 04; no mission stores the interviews themselves", "Camp only"],
            ["2", "Testable problem statement", "04 Problem Statements",
             "The statement, who faces it, its impact, how success is measured", "Direct"],
            ["2", "Chosen solution, value × effort", "05 Idea Selection",
             "Three ideas, each scored for value and <b>impact</b>", "Partial"],
            ["2", "Value proposition", "06 Idea Description",
             "Value proposition, 3–5 key features, benefits, differentiation, assumptions", "Partial"],
            ["2", "Assumption test plan", "07 Solution Hypothesis Test",
             "The hypothesis, how it will be tested, what would prove it", "Direct"],
            ["3", "Test verdict", "07 Solution Hypothesis Test",
             "Test results and what was learned — the same mission, finished", "Direct"],
            ["3", "Simplified Business Model Canvas", "08 Business Model Canvas",
             "Value propositions, segments, channels, relationships, revenue, resources", "Direct"],
            ["3", "One-page financial plan", "<b>none</b>",
             "Unit cost, price, margin and break-even have no field anywhere in the fifteen", "<b>Missing</b>"],
            ["4", "Prototype", "09 Build Prototype",
             "Type of prototype, features, user flows, <b>tools and technology used</b>", "Partial"],
            ["4", "User-test notes", "10 Solution Hypothesis Test (Prototype)",
             "How many tested it, how, key findings, feedback, improvements", "Direct"],
            ["4", "Brand kit", "<b>none</b>",
             "Name, logo, colours and tagline have no mission", "<b>Missing</b>"],
            ["5", "Pitch deck", "<b>none</b>", "No mission records a deck", "<b>Missing</b>"],
            ["5", "Rehearsed pitch", "<b>none</b>",
             "No mission records the pitch itself", "<b>Missing</b>"],
            ["5", "Q&amp;A card", "<b>none</b>",
             "No mission records the three prepared answers", "<b>Missing</b>"],
            ["6", "Public pitch", "—", "The Bazaar itself; judged live", "Camp only"],
            ["6", "Booth", "—", "Built and judged on the day, nothing to store", "Camp only"],
        ]),

        ("h2", "The four partial matches, and what to tell facilitators"),

        ("table", ["Deliverable", "The divergence", "What to say on the day"], [
            ["Problem cards → 01",
             "Mission 01 also asks what solutions already exist and their limits. The camp does not teach competitor work.",
             "Answer from what you already know; you will revisit it after the interviews."],
            ["Chosen solution → 05",
             "The camp plots value × <b>effort</b>. Mission 05 asks for value and <b>impact</b> scores.",
             "Give your value score; for impact, use how much it would help the person you interviewed."],
            ["Value proposition → 06",
             "Mission 06 asks for 3–5 key features. Product work is Day 4.",
             "Write what the thing would do, not how it is built. You will revise it after the prototype."],
            ["Prototype → 09",
             "Mission 09 asks what tools and technology were used, of students building with paper and card.",
             "Cardboard, paper and scissors is a complete answer to that question."],
        ]),

        ("h2", "Closing the five that are missing"),

        ("num", [
            ("01", "Add a Costs and Pricing mission after 08",
             "Unit cost, price with its justification, margin and break-even — the "
             "exact artefacts Day 3 already produces. It also fills a hole we have "
             "outside this camp: there is no finance mission anywhere in the fifteen."),
            ("02", "Add a Brand and Pitch mission after 10",
             "Name, logo, tagline, the deck outline and the three Q&amp;A answers — "
             "four of the five missing deliverables in one mission. Day 4 and Day 5 "
             "already produce all of it, so neither mission adds homework."),
            ("03", "Adopt the pack's mission names",
             "Seven of the ten titles in the pack are not what a student sees on "
             "screen, and the pack's are clearer — adopting them also fixes our own "
             "collision, where 07 and 10 both read as “Solution Hypothesis Test”."),
        ]),

        ("note", "Matched against the <b>Entrepreneurship Camp Learner Journey</b> "
                 "pack, September 2026, and our own mission titles and question sets. "
                 "The twenty deliverables are the pack's own per-day lists. The 50% is "
                 "the published Bazaar weights for business and finance logic, brand "
                 "and booth, pitch delivery, and Q&amp;A. Missions 11–15 sit outside "
                 "the camp and are not matched here."),
    ],
}
