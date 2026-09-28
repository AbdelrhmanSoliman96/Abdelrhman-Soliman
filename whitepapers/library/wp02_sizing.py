"""Market Sizing Without Lying — TAM, SAM and SOM done from the bottom up."""

DOC = {
    "slug": "wp02-market-sizing",
    "file": "StartPad_Whitepaper_02_Market_Sizing_Without_Lying",
    "kind": "whitepaper",
    "series": "StartPad Whitepaper",
    "number": "No. 02",
    "title": "Market Sizing Without Lying",
    "standfirst": "The market slide is the most-skipped page in every application, "
                  "because almost all of them are the same number taken from the "
                  "same report. Here is the version that is worth reading.",
    "standfirst_plain": "How to size a market from the bottom up, what TAM, SAM and "
                        "SOM actually mean, and why the big number hurts you.",
    "cover_foot": "Fifteen minutes · Read before you write the market slide",
    "keywords": ["market sizing", "TAM", "SAM", "SOM", "bottom-up", "pitch deck",
                 "MENA", "Egypt"],
    "missions": [4, 12],
    "blocks": [

        ("label", "01 · The problem with the big number"),
        ("statement", "Everybody has the same market, and everybody got it from the same report."),
        ("lead", "A reviewer reading a hundred applications will see the same regional "
                 "market figure fifteen times, cited to the same consultancy, "
                 "sometimes with the same typo. It carries no information about the "
                 "applicant, which is why it is skipped."),

        ("p", "There is a worse problem underneath. A market figure lifted from a "
              "report was produced to answer somebody else's question, using a "
              "definition of the category that is almost certainly not yours. When a "
              "reviewer asks what that number includes and the founder cannot say, "
              "the damage is not to the slide — it is to everything else the "
              "founder has claimed."),

        ("quote", "The number is not the point. What the number is made of is the point.",
         "What is actually being assessed"),

        ("h2", "What the reader is really checking"),
        ("p", "Nobody believes your projections and nobody expects to. The market "
              "section is a test of whether you understand the mechanics of your own "
              "business: who pays, how often, how much, and how many of them there "
              "are within reach. A founder who has built the number from those four "
              "quantities knows things a founder who copied it does not."),

        ("break",),

        ("label", "02 · The three numbers"),
        ("statement", "Total, reachable, winnable — and only the third is a forecast."),

        ("fig", "nested", {"layers": [
            ("TAM", "Total addressable market", "Everybody",
             "Everyone who has the problem, if you had no limits at all. Context, never a plan."),
            ("SAM", "Serviceable addressable market", "Reachable",
             "The part you could actually serve with your model, geography, language and channel."),
            ("SOM", "Serviceable obtainable market", "Winnable",
             "What you can realistically take in three years, given your channel and your capacity."),
        ], "note": "They nest. SOM is inside SAM is inside TAM — which is why three "
                   "bars would be the wrong picture: they cannot be added up."},
         "<b>The three sizes, and what each one is for.</b> Most applications give "
         "the first and stop, which is the equivalent of answering “how far can "
         "you run” with the circumference of the earth."),

        ("table", ["", "Question it answers", "How it is used against you"], [
            ["TAM", "Is this category big enough to matter at all?",
             "A huge TAM with no SOM reads as a founder who has not thought about execution."],
            ["SAM", "Given how you actually reach people, what is in range?",
             "A SAM equal to the TAM means you have not defined your channel."],
            ["SOM", "What will you actually have in three years?",
             "The only number anyone will hold you to. Make it defensible, not flattering."],
        ]),

        ("break",),

        ("label", "03 · The method"),
        ("statement", "Build it from a number you can count, upward."),
        ("p", "Top-down sizing starts with a total and applies percentages to it. "
              "Every step is a guess multiplied by another guess, and the result "
              "inherits all of them. Bottom-up starts with something you have "
              "actually observed and multiplies it out. It produces smaller numbers "
              "and it is the only method a careful reader trusts."),

        ("fig", "flow", {"steps": [
            ("Step 01", "Count one unit",
             "One shop, one building, one campus, one clinic. Something you can physically go and count."),
            ("Step 02", "Measure the behaviour",
             "How many in that unit have the problem, how often, and what they spend on it now."),
            ("Step 03", "Count the units",
             "How many shops, buildings, campuses exist in your city, then your country."),
            ("Step 04", "Multiply, then discount",
             "Units times behaviour gives SAM. Then apply your real reach to get SOM."),
            ("Step 05", "Write every assumption down",
             "Each one with where it came from. This list is worth more than the total."),
            ("Step 06", "Test the two that matter most",
             "Change each assumption by half and double. If the answer barely moves, it was not load-bearing."),
        ]}, "<b>Bottom-up, in six steps.</b> Steps five and six are what separate a "
            "number from an argument, and they are the steps almost nobody does."),

        ("h2", "A worked shape"),
        ("p", "The arithmetic matters less than the form, so here is the form with "
              "placeholder quantities. Every line is something a founder could go and "
              "establish in an afternoon, and every line is challengeable on its own "
              "— which is precisely the point."),

        ("kv", [
            ("Observed unit", "One pharmacy in one district"),
            ("Behaviour, measured", "Roughly 9 of its customers a week ask for this"),
            ("Price they pay now", "About 40 EGP each, to a competitor or a workaround"),
            ("Unit value per year", "9 × 52 × 40 EGP — stated as arithmetic, not as a conclusion"),
            ("Units in the city", "Counted from a public register, with the register named"),
            ("SAM", "Unit value × units in the city, for the cities you can actually serve"),
            ("SOM", "SAM × the share your channel can reach in three years, with the channel named"),
        ]),

        ("callout", "The sentence that makes this work",
         "“I counted nine a week in one pharmacy in Faisal, over three weeks in "
         "March. Here is the tally sheet.” Nothing in a consultancy report can "
         "compete with that, because the reviewer cannot check the report and can "
         "check you."),

        ("break",),

        ("label", "04 · Four ways it goes wrong"),
        ("statement", "Each one is visible from across the room."),

        ("num", [
            ("01", "The one per cent argument",
             "“If we capture just 1% of a very large number…”. It contains no "
             "mechanism, which is what makes it the single fastest way to lose a "
             "reader. Nobody captures one per cent of anything by aiming at it."),
            ("02", "The market that is not your market",
             "Quoting the size of all e-commerce when you sell one category to one "
             "city. The bigger figure is not more impressive; it is less relevant, "
             "and the gap between the two is what gets noticed."),
            ("03", "Revenue confused with value",
             "The number of people who have the problem multiplied by what you wish "
             "they would pay. If nobody currently spends anything on this, say so "
             "plainly — creating a new budget line is a real strategy and a "
             "different one."),
            ("04", "A SOM that is a percentage of a guess",
             "If SOM is “five per cent of SAM” and SAM came from a report, the "
             "forecast is two guesses deep. Build SOM from capacity instead: how many "
             "can you actually serve, with the people and channel you will have?"),
        ]),

        ("fig", "compare", {
            "left": ("What a reviewer can check", [
                "A tally you took yourself, with dates",
                "A public register, named, with the count",
                "A price somebody is paying today",
                "Your channel's actual reach last month",
            ]),
            "right": ("What they cannot", [
                "A regional total from a paid report",
                "A growth rate with no base year",
                "“Industry standard conversion rates”",
                "A three-year forecast with no mechanism",
            ]),
        }, "<b>Checkability is the whole test.</b> The left column produces smaller "
           "numbers and more credibility, and credibility is the thing in short supply."),

        ("break",),

        ("label", "05 · What to put on the page"),
        ("statement", "Three lines, then the assumptions."),
        ("p", "The market section of an application should be short, because its job "
              "is narrow. Three numbers with their definitions, then the list of "
              "assumptions, then the one assumption you have tested and what happened "
              "when you tested it."),

        ("ol", [
            "<b>SOM first.</b> The number you will be held to, with the years it "
            "covers and the channel it assumes.",
            "<b>SAM second</b>, with the boundary stated — which cities, which "
            "language, which segment.",
            "<b>TAM last and briefly</b>, as context only, sourced honestly, including "
            "when the source is your own estimate.",
            "<b>Then the assumptions</b>, as a numbered list, each with where it came "
            "from. Four to six of them.",
            "<b>Then the one you tested</b>, and what the test returned. This is the "
            "line that gets remembered.",
        ]),

        ("fig", "ribbon", {"active": [4, 12]},
         "<b>Where this sits.</b> Missions 04 and 12. The counting in step one of the "
         "method is the same counting Mission 04 asks for, so the two can be done "
         "together."),

        ("h2", "A note on sources"),
        ("p", "No market figures are quoted in this paper on purpose. Any number "
              "printed here would be out of date by the time it was read, and would "
              "then be copied into applications — which is the practice the paper "
              "argues against. The method is durable; the numbers are yours to count."),

        ("note", "The companion worksheet is the <b>Market Sizing</b> template in the "
                 "StartPad template library, which lays out the bottom-up build and "
                 "the assumption list as fields to fill in."),
    ],
}
