"""Report 01 — Requirement, Gap, Route, the book's sentence structure as a decision engine."""

DOC = {
    "slug": "r01-requirement-gap-route",
    "file": "StartPad_Report_01_Requirement_Gap_Route",
    "kind": "report",
    "series": "StartPad Report",
    "number": "No. 01",
    "title": "Requirement, Gap, Route",
    "standfirst": "The brand book gives StartPad a sentence structure. It turns out "
                  "to be a decision engine: the same three moves that make a screen "
                  "honest make a founder's week honest.",
    "standfirst_plain": "How the requirement-gap-route structure from the StartPad "
                        "brand book works as a decision tool for founders.",
    "cover_foot": "Report · Derived from Chapters 02 and 05",
    "keywords": ["decision making", "founder", "prioritisation", "readiness",
                 "StartPad", "MENA"],
    "missions": [1, 2, 6],
    "blocks": [

        ("label", "The source"),
        ("bookref", "Programs ask for four things. You have two. Missions six and "
                    "nine close the gap. Then you apply with a file, not a hope.",
         "Chapter 05 · The voice, sentence structure"),

        ("statement", "Three moves, and the order is the whole thing."),
        ("lead", "The book writes that sentence as a voice rule — how a StartPad "
                 "screen should talk. Read it again and it is not a style. It is a "
                 "complete decision: what is being asked, what is missing, and the "
                 "shortest route between the two. Founders who make decisions in "
                 "that order make different decisions."),

        ("fig", "flow", {"steps": [
            ("Move 01", "Requirement",
             "What is actually being asked of you, stated by whoever is asking. Not what you think matters."),
            ("Move 02", "Gap",
             "Which specific parts of it you do not have. Named, counted, and not softened."),
            ("Move 03", "Route",
             "The shortest path that closes those specific parts. Everything else is deferred, not dropped."),
        ], "note": "Inverting any two of these produces a recognisable failure mode, "
                   "set out on the next page."},
         "<b>The structure, as the book states it.</b> Each move is useless without "
         "the one before it — a route with no gap is a to-do list, and a gap with "
         "no requirement is an anxiety."),

        ("h2", "Why founders skip to the route"),
        ("p", "Because the route is the only one of the three that feels like "
              "progress. It is visible, it can be scheduled, and it postpones the "
              "uncomfortable move, which is naming the gap. A founder who starts at "
              "the route is not lazy; they are avoiding a sentence they do not want "
              "to write down."),

        ("break",),

        ("label", "01 · The failure modes"),
        ("statement", "Each wrong order has a name and a symptom."),

        ("table", ["The order taken", "What it produces", "How to recognise it"], [
            ["Route first", "A busy week that changes nothing",
             "You can list what you did and not what it closed."],
            ["Gap first, no requirement", "Anxiety, and work on the wrong weakness",
             "You are fixing what you are worst at rather than what is asked."],
            ["Requirement first, no gap", "Copying whoever applied last year",
             "Your plan would be identical if your situation were different."],
            ["All three, wrong requirement", "A closed gap nobody asked about",
             "You met the bar and were still declined, with no reason given."],
        ]),

        ("callout", "The requirement is not yours to decide",
         "This is the move founders resist hardest. The requirement belongs to "
         "whoever is doing the judging — the programme, the customer, the "
         "committee. You are allowed to disagree with it. You are not allowed to "
         "substitute your own and then be surprised."),

        ("h2", "Getting the requirement from the source"),
        ("num", [
            ("01", "Read what they actually publish",
             "Application forms, rubrics, past cohorts. Most programmes state their "
             "screen plainly and are read as if they had not."),
            ("02", "Ask someone who was declined",
             "They will tell you the reason more freely than someone who got in, and "
             "the reason is the requirement, stated by the only test that counts."),
            ("03", "Count what the accepted had",
             "Not what they say now. What they had at the point of applying — "
             "usually much less than their current description implies."),
        ]),

        ("break",),

        ("label", "02 · Naming the gap"),
        ("statement", "A gap you cannot count is a feeling."),
        ("p", "The book's example sentence is precise in a way that is easy to miss: "
              "<b>four things</b>, <b>you have two</b>. Not “some gaps remain”. "
              "The counting is what makes the next move possible, because a route "
              "can only be built against a definite thing."),

        ("fig", "compare", {
            "left": ("A named gap", [
                "Four asked for; I have two; the missing two are evidence and a working thing",
                "Eleven of the twenty conversations happened; nine have not",
                "They require a prototype; mine exists on paper and has not been shown to anyone",
                "The form asks for traction; my strongest number has no denominator",
            ]),
            "right": ("A felt gap", [
                "I am not ready yet",
                "I need to do more customer research",
                "The product needs work",
                "We need more traction",
            ]),
        }, "<b>Both columns describe the same founder.</b> Only the left one can be "
           "turned into next week, because only the left one has a finish line."),

        ("work", "Worksheet · One decision, in three moves", "Fifteen minutes",
         "Take the decision you have been circling for a fortnight and run it "
         "through the structure. Write in this order and do not skip ahead.", [
             ("lines", "1.  The requirement — what is being asked, by whom", 2,
              "In their words. If you cannot quote it, go and find it first."),
             ("lines", "2.  The gap — which parts I do not have, counted", 3,
              "Numbers where numbers are possible. “Two of four”, not “some”."),
             ("lines", "3.  The route — the shortest thing that closes them", 3,
              "If the route has more than three steps, the gap was not narrow enough."),
             ("lines", "4.  What I am deferring, deliberately", 2,
              "Deferred is not dropped. Writing it down is what stops it coming back as guilt."),
         ]),

        ("break",),

        ("label", "03 · The structure as a habit"),
        ("statement", "It is a weekly review, not a one-off exercise."),
        ("p", "The book applies this structure to every screen, not to an onboarding "
              "flow. The equivalent for a founder is every week, not every quarter. "
              "Three lines on a Friday afternoon, against the same requirement, is "
              "enough to catch a month spent closing a gap nobody asked about."),

        ("fig", "progression", {"stages": [
            ("Enter", "You arrive with a requirement you did not set and a gap you have not counted."),
            ("Travel", "Weekly: the same three lines, against the same requirement, until the count moves."),
            ("Turn", "The point the evidence changes the requirement itself. It happens, and it is not failure."),
            ("Resolve", "The gap reaches zero, and you apply with a file rather than a hope."),
        ], "note": "The book's progression line is one founder. The turn is the part "
                   "most plans do not allow for."},
         "<b>One line, four movements.</b> The turn matters: a founder who never "
         "revises the requirement is following a map rather than reading a market."),

        ("say", [
            ("You are missing two of the four.", "You've got this."),
            ("Mission 09 is where most people stall.", "Your journey starts here."),
            ("The gap is nine conversations, not “more research”.", "We need more traction."),
            ("I am deferring the website until March.", "We're working on everything."),
        ]),

        ("note", "The counting this report asks for is the subject of <b>Toolkit 01 "
                 "— The Readiness Audit</b>, which scores the four requirements "
                 "programmes actually screen for."),
    ],
}
