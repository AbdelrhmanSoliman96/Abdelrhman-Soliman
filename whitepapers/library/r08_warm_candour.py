"""Report 08 — Warm Candour with Institutional Precision: the two-register voice."""

DOC = {
    "slug": "r08-warm-candour",
    "file": "StartPad_Report_08_Warm_Candour",
    "kind": "report",
    "series": "StartPad Report",
    "number": "No. 08",
    "title": "Warm Candour with Institutional Precision",
    "standfirst": "Two registers in one voice. The warmth is what makes people "
                  "stay; the precision is what makes them believed. Drop either "
                  "and a founder becomes a cheerleader, or a form.",
    "standfirst_plain": "The two-register voice from the StartPad brand book, applied "
                        "to how founders talk to customers, teams and investors.",
    "cover_foot": "Report · Derived from Chapter 02",
    "keywords": ["founder voice", "communication", "credibility", "investor relations",
                 "team", "StartPad", "MENA"],
    "missions": [11, 12, 15],
    "blocks": [

        ("label", "The source"),
        ("bookref", "Two registers in one voice. The warmth is what makes people "
                    "stay; the precision is what makes them believed. Drop either "
                    "and the brand becomes something else — a cheerleader, or a form.",
         "Chapter 02 · Personality"),

        ("statement", "Most founders have exactly one of the two."),
        ("lead", "The book's formulation is useful because it names both failure "
                 "modes rather than one. The warm founder with no precision is "
                 "liked and not funded. The precise founder with no warmth is "
                 "credible and joined by nobody. Both are common, and neither "
                 "notices, because each one's strength keeps producing enough "
                 "encouragement to hide the missing half."),

        ("fig", "matrix", {
            "x_label": "Precision",
            "y_label": "Warmth",
            "quads": [
                ("The cheerleader", "Liked, followed, invited to speak. Numbers with "
                 "no denominators and claims with no sources. Raises slowly or not "
                 "at all, and usually concludes that investors here are too "
                 "conservative.", "hold"),
                ("Warm candour with precision", "Says the uncomfortable thing and is "
                 "still somebody people want to work with. Sourced numbers, named "
                 "gaps, no hedging. Rare, and immediately recognisable in a room.", "act"),
                ("The absentee", "Neither. Usually a founder who has stopped "
                 "communicating because the last update was hard to write. The "
                 "silence is read as worse news than the news would have been.", "hold"),
                ("The form", "Accurate, sourced, complete, and nobody stays. Hires "
                 "badly, loses co-founders, and cannot understand why the numbers "
                 "are not enough on their own.", "hold"),
            ],
        }, "<b>Two registers, four positions.</b> The top-right quadrant is not a "
           "compromise between the other two — it is both at full strength, which "
           "is why it is uncommon."),

        ("break",),

        ("label", "01 · What warmth actually is"),
        ("statement", "Not enthusiasm. Attention."),
        ("p", "Warmth is routinely mistaken for energy, which is why founders try to "
              "produce it with exclamation marks. In the book's own terms the "
              "emotional core is removing anxiety and overthinking — warm before "
              "it is precise, and never precious about the hustle. That is a "
              "description of attention paid to somebody else's state, not of the "
              "speaker's mood."),

        ("bookref", "The uncle who came back from Saudi and worries about their "
                    "interests.",
         "Chapter 02 · The idea, emotional core"),

        ("p", "The figure in that line is warm because he is on your side and will "
              "tell you something you do not want to hear. He is not warm because he "
              "is encouraging. For a founder writing to a team or a customer, the "
              "test is whether the reader finishes less anxious — not whether they "
              "finish more excited."),

        ("fig", "compare", {
            "left": ("Warmth", [
                "Naming the thing the reader is already worried about",
                "Saying what happens next, with a date",
                "Admitting the part you do not know",
                "Addressing one person, not a list",
            ]),
            "right": ("Enthusiasm mistaken for warmth", [
                "Exclamation marks",
                "“Exciting news” as an opening",
                "Emoji standing in for a tone you did not set",
                "Thanking people for their patience instead of explaining the delay",
            ]),
        }, "<b>The left column lowers the reader's anxiety.</b> The right column "
           "raises it slightly, because a reader who is worried and is being "
           "cheered at concludes the news is bad."),

        ("break",),

        ("label", "02 · What precision actually is"),
        ("statement", "Numbers that survive being checked."),
        ("p", "Precision in this sense is not formality and it is not length. A "
              "founder can be precise in three sentences: what the number is, where "
              "it came from, and over what base. What makes writing imprecise is "
              "almost never vocabulary — it is a missing denominator, a missing "
              "date, or an adjective standing where a figure should be."),

        ("say", [
            ("11 of 34 paid a 50 EGP deposit in April.", "Strong early traction."),
            ("We are four weeks behind. The new date is 12 May.", "Slight delay, nothing major."),
            ("I do not know yet. I will know by Thursday.", "We're looking into it."),
            ("Two of the four requirements are not met.", "We're making great progress."),
        ]),

        ("p", "Read that table in the other direction and it is also the warmth "
              "table. The left column is warmer than the right, because each line "
              "gives the reader something to hold. This is the point the book is "
              "making by insisting on one voice rather than two: at full strength "
              "the registers stop being in tension."),

        ("break",),

        ("label", "03 · Where each one is missing"),
        ("statement", "You are probably warm in one channel and precise in another."),
        ("p", "The most useful version of this diagnosis is per audience rather "
              "than overall. Most founders are warm with their team and precise "
              "with investors, or the reverse, and the gap is invisible to them "
              "because no single reader sees both."),

        ("work", "Worksheet · Two registers, four audiences", "Twenty minutes",
         "Take the last real message you sent to each and mark it for both "
         "registers. Use actual sent messages, not what you intend to send.", [
             ("lines", "Customers — warm? precise? which is missing?", 2, None),
             ("lines", "Team — warm? precise? which is missing?", 2,
              "Precision is the one usually missing here, and it reads as indecision."),
             ("lines", "Investors or a programme — warm? precise?", 2,
              "Warmth is the one usually missing here, and it costs you the benefit of the doubt."),
             ("lines", "Suppliers and partners — warm? precise?", 2, None),
             ("lines", "The audience where the gap is widest, and the one change I will make", 2, None),
         ]),

        ("callout", "The refusals are part of the voice",
         "The book lists what this personality refuses: hype, cheerleading, startup "
         "romanticism, and promises about funding. A founder who adopts the two "
         "registers and keeps the four refusals has a voice that is unusual in this "
         "market and costs nothing to maintain."),

        ("fig", "progression", {"stages": [
            ("Enter", "One register, usually whichever came naturally, applied to everybody."),
            ("Travel", "You notice the audience where it is failing — normally after it has cost something."),
            ("Turn", "You add the missing register to that audience specifically, rather than changing your personality."),
            ("Resolve", "One voice at two intensities, and no reader who sees two of your messages sees two people."),
        ]}, "<b>Adding a register, not replacing one.</b> Founders who try to become "
            "a different person in front of investors are detected almost "
            "immediately; founders who add precision to the voice they already have "
            "are not."),

        ("note", "The intensity a document is written at — believed or shared — "
                 "is a separate decision from the register, and is the subject of "
                 "<b>Report 05 — Believed or Shared</b>."),
    ],
}
