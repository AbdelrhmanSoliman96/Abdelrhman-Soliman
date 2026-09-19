"""The Evidence Toolkit — twenty conversations in fourteen days."""

DOC = {
    "slug": "tk02-evidence",
    "file": "StartPad_Toolkit_02_The_Evidence_Toolkit",
    "kind": "toolkit",
    "series": "StartPad Toolkit",
    "number": "No. 02",
    "title": "The Evidence Toolkit",
    "standfirst": "Twenty conversations in fourteen days, recorded so that somebody "
                  "who was not there can check them. This is the requirement most "
                  "founders think they have already met.",
    "standfirst_plain": "How to run, script and log twenty customer conversations in "
                        "fourteen days, and how to read what they tell you.",
    "cover_foot": "Fourteen days · Run it once, properly",
    "keywords": ["customer discovery", "customer interviews", "evidence",
                 "problem validation", "startup", "MENA"],
    "missions": [2, 3, 7],
    "blocks": [

        ("label", "The point of this"),
        ("statement", "A conversation you cannot count is not evidence."),
        ("lead", "Most founders have already had these conversations. What they have "
                 "not done is count them, date them, record who said what, and keep "
                 "the record somewhere a stranger could read it. That difference is "
                 "the entire requirement."),

        ("p", "Twenty is not a magic number and it is not statistically significant. "
              "It is the point at which you stop hearing new things, which is the "
              "only thing you are listening for. Fourteen days is not a deadline for "
              "its own sake either: spread these over three months and the early "
              "conversations describe a different world from the late ones, and you "
              "cannot compare them."),

        ("fig", "timeline", {"phases": [
            ("Build the list", 0, 3, "Forty names, so twenty conversations survive the no-shows."),
            ("First five", 3, 3, "Deliberately rough. You are testing the script, not gathering data."),
            ("Rewrite the script", 6, 1, "Cut every question the first five answered the same way."),
            ("The next fifteen", 7, 6, "Two a day. Log each one within the hour."),
            ("Read the log", 13, 1, "Alone, in one sitting, with the log and nothing else."),
        ], "span_label": "Fourteen days", "unit": "day"},
         "<b>Fourteen days, five phases.</b> The rewrite on day seven is not optional. "
         "A script that survives twenty conversations unchanged was not asking "
         "anything that could have surprised you."),

        ("callout", "Before you start",
         "Decide now what result would make you stop. Write it down. A founder who "
         "has not decided in advance what disconfirmation looks like will not "
         "recognise it when twenty people hand it to them."),

        ("break",),

        ("label", "01 · Recruiting"),
        ("h1", "Forty names to get twenty conversations"),
        ("p", "Half of the people who agree will not show up, and that is normal "
              "rather than a sign of anything. Build the list at twice the size you "
              "need and the fourteen days survive contact with reality."),

        ("fig", "funnel", {"stages": [
            ("Names on the list", 40, "40"),
            ("Asked", 40, "40"),
            ("Agreed", 26, "26"),
            ("Actually happened", 20, "20"),
        ], "note": "Plan for this shape rather than being surprised by it. The drop "
                   "between agreed and happened is almost entirely scheduling."},
         "<b>The recruiting funnel.</b> The numbers are a planning assumption, not a "
         "measurement — track your own and you will know your real ratio by the "
         "second week."),

        ("h2", "Where the names come from, in order of usefulness"),
        ("num", [
            ("01", "People you have already watched have the problem",
             "Colleagues, family, the shop you buy from. You are not looking for "
             "strangers — you are looking for accuracy."),
            ("02", "One degree out, through someone who will introduce you",
             "An introduction converts several times better than a cold message and "
             "costs you one favour."),
            ("03", "Where the problem is already being discussed",
             "A Facebook group, a WhatsApp group, a building, a market, a queue. "
             "People complaining about something are pre-qualified."),
            ("04", "Cold outreach, last",
             "It works, but the response rate will make your fourteen days slip. "
             "Use it to top up, not to start."),
        ]),

        ("callout", "What to say when you ask",
         "“I am trying to understand how [specific situation] actually works. I "
         "am not selling anything and I am not going to ask you to sign up to "
         "anything. Twenty minutes, this week?” — and then honour both promises "
         "exactly. Selling in a research call costs you the next introduction."),

        ("break",),

        ("label", "02 · The script"),
        ("h1", "Ask about the past, never about the future"),
        ("p", "People are generous and they want to help, which makes them "
              "unreliable about what they would do. They are far more reliable about "
              "what they did. Every question below is built to keep the conversation "
              "in the past tense, where the answers are made of memory rather than "
              "imagination."),

        ("say", [
            ("Tell me about the last time that happened.", "Would you use something that did this?"),
            ("What did you do about it?", "Do you think this is a good idea?"),
            ("What did that cost you — money, or hours?", "How much would you pay for it?"),
            ("Who else did you talk to about it?", "Would you recommend it to a friend?"),
            ("What did you try before that?", "Does that sound useful to you?"),
        ]),

        ("p", "The right-hand column is not merely useless. It is actively "
              "misleading, because a yes costs the person nothing and buys them a "
              "pleasant end to the conversation. Every founder who has been told "
              "twenty times that their idea is great and then launched to silence "
              "asked the questions on the right."),

        ("work", "The script card", "Print one per conversation",
         "Five questions, in this order. Do not add a sixth until you have run five "
         "conversations and found something the five do not reach.", [
             ("lines", "1.  Tell me about the last time [the situation] happened.", 2,
              "Then stop talking. The silence after this question is where the value is."),
             ("lines", "2.  What did you do about it?", 2, None),
             ("lines", "3.  What did that cost you?", 2,
              "Push for a number — pounds, or hours. “A lot” is not an answer."),
             ("lines", "4.  What had you tried before that?", 2, None),
             ("lines", "5.  Who else has this problem, and could you introduce me?", 2,
              "This question is how the list of forty keeps growing."),
         ]),

        ("callout", "The rule that makes the rest work",
         "Do not describe your idea until the person has finished describing their "
         "problem. The moment they know what you are building, every subsequent "
         "answer is shaped to be kind to you. If you must describe it, do it in the "
         "last two minutes, and mark the log to say you did."),

        ("break",),

        ("label", "03 · The log"),
        ("h1", "One row per conversation, filled in within the hour"),
        ("p", "The log is the deliverable. The conversations are not evidence until "
              "they are written down in a form somebody else could audit — which is "
              "exactly what a programme, a judge or an investor is checking when they "
              "ask how you know."),

        ("table", ["Column", "What goes in it", "Why it is there"], [
            ["#", "1 to 20", "So the count is a count and not an impression."],
            ["Date", "The date of the conversation", "Evidence has an age. Three months old is history."],
            ["Who", "Name or initials, and what they do", "Makes the row checkable."],
            ["Source", "How you reached them", "Tells you which recruiting channel actually worked."],
            ["Problem raised unprompted?", "Yes or no", "The single most predictive column on the sheet."],
            ["Last occurrence", "When it last happened to them", "Separates a live problem from a remembered one."],
            ["Cost", "Money or hours, as stated", "Turns severity into something comparable."],
            ["Current workaround", "What they do today", "Your real competitor, in their words."],
            ["Quote", "One sentence, verbatim", "The only thing that will survive into your application."],
            ["Would they talk again?", "Yes or no", "Your follow-up list, and your verification list."],
        ]),

        ("work", "Evidence log · rows 1–5", "Copy this page four times",
         "Fill this in within an hour of each conversation. A log written at the end "
         "of the week is a reconstruction, and reconstructions flatter the founder.", [
             ("lines", "1.  Date · Who · Unprompted? · Cost · Workaround", 3, None),
             ("lines", "    Quote", 2, None),
             ("lines", "2.  Date · Who · Unprompted? · Cost · Workaround", 3, None),
             ("lines", "    Quote", 2, None),
             ("lines", "3.  Date · Who · Unprompted? · Cost · Workaround", 3, None),
             ("lines", "    Quote", 2, None),
         ]),

        ("break",),

        ("label", "04 · Reading it"),
        ("h1", "Two questions, asked of the whole log at once"),
        ("p", "Read the log in one sitting, at the end, with nothing else open. You "
              "are asking two things of it: how badly does this hurt, and how often "
              "does it happen. Those two answers place the problem, and the placement "
              "tells you whether to build anything at all."),

        ("fig", "matrix", {
            "x_label": "How often it happens",
            "y_label": "How much it costs them",
            "quads": [
                ("Expensive, rare", "A real problem that people will pay to solve and "
                 "then not think about for a year. Hard to build a habit on. Workable "
                 "if the price is high enough.", "hold"),
                ("Expensive, frequent", "Build here. People are already spending money "
                 "or hours on a workaround, repeatedly, which means the budget and the "
                 "habit both already exist.", "act"),
                ("Cheap, rare", "Nothing to build. If your log lands here, the finding "
                 "is that this is not a business, and finding that out in fourteen "
                 "days is a good outcome.", "hold"),
                ("Cheap, frequent", "An annoyance rather than a problem. Solvable, and "
                 "usually solved by free tools. Charging for it is the hard part.", "hold"),
            ],
        }, "<b>Place the problem, then decide.</b> Only one quadrant is worth a year "
           "of your life, and the log tells you which one you are in without you "
           "having to guess."),

        ("h2", "The three numbers that decide it"),
        ("kv", [
            ("Unprompted mentions", "Out of twenty. Under five and the problem is "
             "yours rather than theirs."),
            ("Median stated cost", "In pounds or hours. If people cannot name a cost, "
             "they do not experience this as a problem."),
            ("People who asked you to follow up", "Unprompted, at the end. This is the "
             "earliest honest demand signal you will get."),
        ]),

        ("work", "The decision", "End of day fourteen",
         "Write this before you talk to anyone about the result. A decision made out "
         "loud with a friend present is a decision made to sound reasonable.", [
             ("lines", "Unprompted mentions, out of twenty", 1, None),
             ("lines", "Median cost, as stated by them", 1, None),
             ("lines", "Which quadrant the log puts you in", 1, None),
             ("lines", "The problem statement, rewritten now that you have heard twenty people", 3,
              "Compare it to the one you started with. If nothing changed, you were not listening."),
             ("lines", "Continue, change the problem, or stop — and why", 3, None),
         ]),

        ("callout", "Stopping is a result",
         "A log of twenty conversations that says nobody has this problem is worth "
         "more than a year spent building for nobody, and it is worth more in an "
         "application than a vague success. Programmes are unusually interested in "
         "founders who can show they changed their mind because of evidence."),

        ("note", "The log from this toolkit is the input to <b>Toolkit 04 — The "
                 "Demand Signal</b>, and the quotes are what fill the evidence "
                 "section of <b>Toolkit 05 — The Application File</b>. Keep it."),
    ],
}
