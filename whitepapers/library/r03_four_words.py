"""Report 03 — Truth, Proof, Progress, Restraint as founder operating principles."""

DOC = {
    "slug": "r03-four-words",
    "file": "StartPad_Report_03_The_Four_Words",
    "kind": "report",
    "series": "StartPad Report",
    "number": "No. 03",
    "title": "The Four Words",
    "standfirst": "Truth, Proof, Progress, Restraint. The book puts four words "
                  "underneath everything StartPad does. They work as well "
                  "underneath a company as underneath a brand.",
    "standfirst_plain": "The four DNA words from the StartPad brand book, read as "
                        "operating principles for a founder and their team.",
    "cover_foot": "Report · Derived from Chapter 02",
    "keywords": ["operating principles", "company values", "founder", "culture",
                 "StartPad", "MENA"],
    "missions": [1, 11, 15],
    "blocks": [

        ("label", "The source"),
        ("bookref", "Four words underneath everything. Truth. Proof. Progress. Restraint.",
         "Chapter 02 · Brand DNA"),

        ("statement", "Values that can be failed are worth having."),
        ("lead", "Most stated company values cannot be failed. Integrity, "
                 "excellence, innovation — nobody has ever been caught breaching "
                 "them, because there is no act that would count. The four below are "
                 "different: each one forbids something specific and common, which "
                 "is what makes them usable."),

        ("fig", "pillars", {"items": [
            ("01", "Truth",
             "Names the requirement before the encouragement. Bad news arrives unsoftened.",
             "Did you state the gap before you stated the plan?"),
            ("02", "Proof",
             "Proves rather than claims. Every number sourced, every status earned.",
             "Could a stranger check your last claim without asking you?"),
            ("03", "Progress",
             "Makes progress visible from outside. Movement is the thing the system displays.",
             "Can somebody tell you moved this month without being told?"),
            ("04", "Restraint",
             "Never takes credit for the launch. The founder progressed; the platform stayed.",
             "Whose name is on the outcome when it goes well?"),
        ], "note": "The book gives the first line of each. The founder test is this "
                   "report's addition — a value with no test is a poster."},
         "<b>Four words, each with something it forbids.</b> Read the tests rather "
         "than the words: the test is the part that can be failed on a Tuesday."),

        ("break",),

        ("label", "01 · Truth"),
        ("statement", "Bad news arrives unsoftened."),
        ("p", "The operational form of this is narrow and hard: when something has "
              "gone wrong, the first sentence says so. Not the third sentence, after "
              "two of context. Founders invert this almost universally, and the "
              "inversion is expensive because the reader learns to wait for the bad "
              "news rather than to read the good."),

        ("say", [
            ("We missed the target. Here is why and here is the plan.", "Lots of exciting progress this month!"),
            ("Two of the four are not done.", "Great momentum across the board."),
            ("The pilot failed. We are stopping it.", "We're iterating on the pilot."),
            ("I was wrong about the customer.", "We've learned so much."),
        ]),

        ("callout", "Why this one pays",
         "A founder who leads with bad news is believed when they lead with good "
         "news. That is the entire mechanism, and it is the cheapest credibility "
         "available to somebody with no track record."),

        ("h2", "02 · Proof"),
        ("statement", "Every number sourced, every status earned."),
        ("p", "The discipline here is a habit rather than a principle: a number "
              "never travels without its source and its denominator. Once that is "
              "automatic, an investor update and an application stop being writing "
              "tasks and become assembly tasks, because the sourcing already "
              "happened when the number was first written down."),

        ("fig", "compare", {
            "left": ("Sourced", [
                "11 of 34 paid a deposit — payment log, April",
                "6 of 10 returned unprompted — delivery log, weeks 4 to 6",
                "Median 4 hours a week — as stated in 17 interviews",
            ]),
            "right": ("Unsourced", [
                "Roughly a third converted",
                "Most users come back",
                "It saves people a lot of time",
            ]),
        }, "<b>The right column is what the left column decays into</b> in about a "
           "fortnight, if the source is not written down at the moment the number is."),

        ("break",),

        ("label", "03 · Progress"),
        ("statement", "Visible from outside, without being announced."),
        ("p", "The book's formulation is precise: <i>makes progress visible from "
              "outside</i>. Not reports progress — makes it visible. The difference "
              "is who has to do the work. A founder whose progress requires a monthly "
              "email to be perceived has built something opaque; one whose repository, "
              "changelog or public list moves on its own has not."),

        ("fig", "ladder", {"rungs": [
            ("Somebody noticed before you told them", "The only rung that is genuinely visible from outside."),
            ("A public artefact that moves on its own", "A changelog, a list, a shipped thing with a date on it."),
            ("A monthly update that people read", "Visible, but you are carrying it."),
            ("A monthly update nobody reads", "The most common, and functionally invisible."),
            ("Progress you would have to be asked about", "Real work. Nobody knows."),
        ], "caption_high": "VISIBLE FROM OUTSIDE", "caption_low": "INVISIBLE"},
         "<b>Ranked by who does the work of noticing.</b> Most founders sit on the "
         "fourth rung and conclude that the market is not paying attention."),

        ("h2", "04 · Restraint"),
        ("statement", "The founder progressed; the platform stayed."),
        ("p", "This is the strangest of the four to find in a brand book, because it "
              "instructs the brand not to claim its own results. For a founder the "
              "equivalent is about a team: when it goes well, the person who did it "
              "is named, and when it goes badly, you are. It costs nothing and it is "
              "almost never done, which is why it is noticed."),

        ("p", "It also has a commercial form. Restraint is what stops a founder "
              "claiming their customer's outcome as their own — the difference "
              "between “we grew their revenue 40%” and “they grew 40%; we "
              "handled the logistics”. The second is more credible and, in a small "
              "market where the customer will be asked, considerably safer."),

        ("break",),

        ("label", "Using them"),
        ("statement", "Four questions, once a month."),

        ("work", "Worksheet · The four tests", "Monthly, ten minutes",
         "Answer from the month that just ended, not the one you intend to have.", [
             ("lines", "Truth — the worst thing that happened, and who I told first", 2,
              "If nobody was told, that is the answer to the test."),
             ("lines", "Proof — a claim I made this month, and its source", 2, None),
             ("lines", "Progress — what somebody outside could see moved, unprompted", 2, None),
             ("lines", "Restraint — a result I took credit for that somebody else produced", 2,
              "The honest answer is rarely “none”."),
         ]),

        ("callout", "Do not adopt all four at once",
         "Pick the one you failed most clearly this month and run it for a quarter. "
         "Four new disciplines starting on the same Monday is how a values exercise "
         "becomes a document nobody opens again."),

        ("note", "The book lists five behaviours alongside these four words, one of "
                 "which — speaking the way your audience speaks, composed rather "
                 "than translated — is a communications discipline rather than an "
                 "operating one, and is the subject of <b>Report 07</b>."),
    ],
}
