"""Report 06 — One Idea Only: the hierarchy rule applied to pitches and product."""

DOC = {
    "slug": "r06-one-idea-only",
    "file": "StartPad_Report_06_One_Idea_Only",
    "kind": "report",
    "series": "StartPad Report",
    "number": "No. 06",
    "title": "One Idea Only",
    "standfirst": "The book sets a four-level hierarchy and a single rule on top of "
                  "it: if it needs explaining, it failed. Applied to a pitch or a "
                  "product, the rule is unusually unforgiving — and unusually useful.",
    "standfirst_plain": "The one-idea hierarchy and the explaining rule from the "
                        "StartPad brand book, applied to pitches and product decisions.",
    "cover_foot": "Report · Derived from Chapters 02 and 03",
    "keywords": ["pitch", "clarity", "positioning", "product", "messaging",
                 "StartPad", "MENA"],
    "missions": [6, 11, 15],
    "blocks": [

        ("label", "The source"),
        ("bookref", "If it needs explaining, it failed.",
         "Chapter 02 · The one rule"),

        ("statement", "The rule is about the reader's first second, not their patience."),
        ("lead", "It is easy to read that line as a demand for simplicity. It is "
                 "narrower than that. It says the work of understanding must not be "
                 "handed to the reader — and a founder hands it over constantly, "
                 "usually by putting two ideas where one belongs."),

        ("fig", "flow", {"steps": [
            ("Level 01", "Label",
             "Locates the reader. Never explains. “Section 3”, “Market”, “The ask”."),
            ("Level 02", "Statement",
             "Names the requirement. The one idea, in a sentence that could stand alone on the page."),
            ("Level 03", "Headline",
             "The specific claim underneath it."),
            ("Level 04", "Body",
             "Carries the reasoning. Everything a sceptic needs, and nothing that competes with the statement."),
        ], "note": "The failure is almost always a body-level sentence promoted to "
                   "statement level, where it has to compete with the real idea."},
         "<b>Four levels, one idea each page.</b> The hierarchy is not typographic "
         "decoration — it is an instruction about how many ideas may occupy a "
         "reader's attention at once."),

        ("break",),

        ("label", "01 · The two-idea slide"),
        ("statement", "The most expensive habit in a first pitch."),
        ("p", "A founder with a genuinely good second idea puts it next to the "
              "first, on the reasonable-sounding basis that both are true. What a "
              "reader experiences is not two reasons to be interested. It is a "
              "prompt to work out which one matters, which is work they did not "
              "agree to do and usually will not."),

        ("fig", "compare", {
            "left": ("One idea, carried", [
                "Pharmacies lose four hours a week to one task. We do that task.",
                "Eleven of thirty-four paid before it existed.",
                "We reach these customers through a channel nobody else uses.",
            ]),
            "right": ("Two ideas, competing", [
                "A platform for pharmacies and clinics that saves time and reduces error, with an AI layer",
                "Strong early traction and a large addressable market",
                "A unique channel and a world-class team and a defensible moat",
            ]),
        }, "<b>The right column is not more informative.</b> Each extra clause "
           "divides the attention the first clause had, so three strengths listed "
           "together land as less than one strength stated alone."),

        ("callout", "The practical test",
         "Read your slide, deck page or landing hero to somebody, then take it away "
         "and ask what it was about. If their answer contains the word “and”, "
         "there were two ideas. Whichever one they said first is the real one; the "
         "other belongs in the body."),

        ("break",),

        ("label", "02 · Applied to the product"),
        ("statement", "Explaining is a cost the product pays, not the user."),
        ("p", "The same rule reaches past communication. A feature that requires an "
              "onboarding tooltip to be understood has failed the rule, and the "
              "tooltip is the evidence rather than the solution. Founders "
              "consistently treat explanation as a fix, which converts a design "
              "problem into a permanent tax on every new user."),

        ("fig", "ladder", {"rungs": [
            ("Understood with nothing said", "The thing itself communicates its purpose. Rare, and the target."),
            ("Understood after one sentence", "Acceptable, and where most good products sit."),
            ("Needs a tooltip or a tour", "The explanation is a patch. Note it and come back to it."),
            ("Needs a call or a demo", "Real for complex products, and an active constraint on how fast you grow."),
            ("Needs you personally, every time", "Not a product yet. It is a service with software attached."),
        ], "caption_high": "EXPLAINS ITSELF", "caption_low": "NEEDS YOU"},
         "<b>How much explaining your product currently requires.</b> The bottom two "
         "rungs are legitimate early positions; the mistake is not knowing you are "
         "on them."),

        ("break",),

        ("label", "03 · Finding your one idea"),
        ("statement", "It is usually already in your evidence."),
        ("p", "Founders search for the one idea in their ambitions, where everything "
              "is equally important. It is more reliably found in the evidence: the "
              "single sentence that made somebody pay, return or introduce you to a "
              "colleague. That sentence has already been tested on a real person, "
              "which is more than any positioning exercise will give you."),

        ("work", "Worksheet · One idea", "Thirty minutes",
         "Use your interview log and your delivery log rather than your imagination.", [
             ("lines", "The sentence somebody repeated back to you, in their words", 2,
              "From your evidence log. Verbatim, not paraphrased."),
             ("lines", "The one thing people actually used it for — not the list of things it does", 2, None),
             ("lines", "Write it as a statement that could stand alone on a page", 2,
              "No “and”. If you need one, you have two ideas and must pick."),
             ("lines", "What moves down to body level as a result", 3,
              "Down, not out. The second idea is still true and still belongs in the reasoning."),
             ("lines", "Read it to somebody. What did they say it was about?", 2, None),
         ]),

        ("check", [
            ("The statement contains no “and” joining two benefits",
             "One idea. The other one moves to the body."),
            ("The label locates the reader and does not explain",
             "“The ask”, not “Why we are the right team to back”."),
            ("Nothing at body level competes with the statement",
             "If a body sentence is stronger, promote it and demote the statement."),
            ("Somebody repeated it back correctly without seeing it twice",
             "The only test that matters, and the only one that is cheap to run."),
        ]),

        ("quote", "Strip the wordmark from any image in this system. If it still "
                  "reads as StartPad, the system is working.",
         "Chapter 03 · The identity"),

        ("p", "The founder version of that test: take your name off the deck. If a "
              "reader could still tell what you do and why it is you, the one idea "
              "is carrying. If they could not, the name was doing work the argument "
              "should have been doing."),

        ("note", "The evidence this report sends you back to is produced by "
                 "<b>Toolkit 02 — The Evidence Toolkit</b> and <b>Toolkit 03 — "
                 "The Manual MVP</b>."),
    ],
}
