"""The Readiness Audit — score yourself against what programmes actually ask for."""

DOC = {
    "slug": "tk01-readiness-audit",
    "file": "StartPad_Toolkit_01_The_Readiness_Audit",
    "kind": "toolkit",
    "series": "StartPad Toolkit",
    "number": "No. 01",
    "title": "The Readiness Audit",
    "standfirst": "Four requirements, scored honestly, in about an hour. "
                  "It tells you which one to spend the next month on and "
                  "it will not flatter you.",
    "standfirst_plain": "A scored self-audit against the four requirements every "
                        "programme, competition and first cheque asks for.",
    "cover_foot": "One hour · Print this and write on it",
    "keywords": ["founder readiness", "self assessment", "accelerator application",
                 "startup", "Egypt", "MENA"],
    "missions": [1, 2],
    "blocks": [

        ("label", "How to use this"),
        ("statement", "Met, or not met. There is no partly."),
        ("lead", "This audit is only useful if it is uncomfortable. Every requirement "
                 "below is scored against evidence somebody else could check, not "
                 "against how confident you feel. A generous score costs you a month "
                 "you spend building the wrong thing."),

        ("num", [
            ("01", "Print it, or fill it on screen",
             "Every field is a real field. Writing the answer down is part of the "
             "exercise — an answer you can only say out loud is not yet an answer."),
            ("02", "Answer from evidence, not memory",
             "Where a field asks for a number, go and count it. Where it asks for a "
             "name, use the actual name. “Several people” scores zero."),
            ("03", "Score at the end, not as you go",
             "Scoring each section as you write it pulls the later answers toward the "
             "total you want. Fill in all four first, then score."),
        ]),

        ("fig", "ribbon", {"active": [1, 2]},
         "<b>Where this sits.</b> This is the work of missions 01 and 02. The result "
         "tells you which of the missions after them is worth your month."),

        ("callout", "One hour, once",
         "This is not a document to keep updating. Do it once, act on the weakest "
         "requirement for a month, then do it again from a blank copy and compare. "
         "The gap between the two copies is the only progress measure that matters here."),

        ("break",),

        ("label", "The four requirements"),
        ("statement", "What is actually being asked."),
        ("p", "Programmes vary enormously in what they fund and almost not at all in "
              "what they screen for. The four below are the screen, in the order they "
              "are usually applied. Failing the first makes the other three "
              "irrelevant, which is why the audit runs in this order."),

        ("table", ["", "The requirement", "What a reader is checking"], [
            ["01", "A named problem, and a named person who has it",
             "That you can describe one person, not a market, and say what goes wrong for them today."],
            ["02", "Evidence you did not make up",
             "That something in your answer could be verified without contacting you."],
            ["03", "Something that exists",
             "That you have built or run something, however small and however manual."],
            ["04", "A reason it is you",
             "That there is an access, skill or history that makes you a better bet than the next applicant."],
        ]),

        ("p", "Each requirement below is scored <b>0 to 5</b>. The anchors are printed "
              "next to the scale so the number means the same thing every time you do "
              "this. Twenty is the maximum and nobody starting out scores it."),

        ("break",),

        ("label", "Requirement 01"),
        ("h1", "A named problem, and a named person who has it"),
        ("p", "The most common first-screen failure is a problem described at the "
              "level of a population. “Young people in Egypt struggle to find "
              "work” is a headline, not a problem statement. A problem statement "
              "names somebody and says what specifically goes wrong for them, when, "
              "and what it costs them."),

        ("work", "Worksheet 1A · The person", "Requirement 01",
         "Write about one real person you have actually met. If you cannot, that is "
         "the finding, and the score is zero.", [
             ("lines", "Their name, or initials if you prefer", 1,
              "A real person. Not a persona and not a composite."),
             ("lines", "What they do, in one line", 1, None),
             ("lines", "The last time this problem happened to them, and what happened", 3,
              "A specific occasion with a date, not a general tendency."),
             ("lines", "What it cost them — money, hours, or an outcome they lost", 2, None),
             ("lines", "What they do about it today, without you", 2,
              "Everyone already does something. The something is your real competitor."),
         ]),

        ("work", "Worksheet 1B · The problem statement", "Requirement 01",
         "Now write it as one sentence a stranger could repeat back to you correctly.", [
             ("box", "When [person] is [situation], they [what goes wrong], which costs them [cost]. Today they [current workaround].", 26, None),
         ]),

        ("fig", "bands", {"segments": [
            (0, 2, "0–1", "No named person, or the problem is stated at population level."),
            (2, 4, "2–3", "A named person exists, but the problem is described in general terms."),
            (4, 5, "4", "One person, one occasion, a cost you can state."),
            (5, 6, "5", "The above, and they told you, unprompted, before you asked."),
        ], "scale_max": 6},
         "<b>Score requirement 01.</b> Write your score in the box on the scoring "
         "page. The jump from 3 to 4 is the whole requirement: a general truth "
         "becomes a specific incident."),

        ("break",),

        ("label", "Requirement 02"),
        ("h1", "Evidence you did not make up"),
        ("p", "This is the requirement founders most often believe they have met. The "
              "test is simple and it is not about how convinced you are: could "
              "somebody check your answer without contacting you, and would what they "
              "found match what you said?"),

        ("fig", "compare", {
            "left": ("Counts", [
                "Conversations, dated, with who said what",
                "A waiting list with real names on it",
                "Money taken before the thing existed",
                "A log from a service you ran by hand",
                "A supplier or partner who agreed in writing",
            ]),
            "right": ("Does not count", [
                "“Everyone I spoke to loved it”",
                "A survey your friends answered",
                "A market size from a consultancy report",
                "Sign-ups to a page offering something free",
                "A letter of intent that binds nobody",
            ]),
        }, "<b>The line is verifiability, not enthusiasm.</b> Everything on the right "
           "can be true and still prove nothing, because it survives regardless of "
           "whether the problem is real."),

        ("work", "Worksheet 2A · Count it", "Requirement 02",
         "Numbers only. If you have to estimate, the answer is zero — go and count "
         "it before you fill this in.", [
             ("lines", "People you have spoken to about this problem, in person or on a call", 1,
              "Not messages. A conversation where they talked more than you did."),
             ("lines", "Of those, how many raised the problem before you described it", 1,
              "This is the single most predictive number on the page."),
             ("lines", "People who have given you something — money, a commitment, their time on a waiting list", 1, None),
             ("lines", "The date of your most recent conversation", 1,
              "Evidence more than three months old is history, not evidence."),
         ]),

        ("work", "Worksheet 2B · The strongest single piece", "Requirement 02",
         "One piece of evidence, described so a stranger could go and verify it.", [
             ("lines", "What it is", 2, None),
             ("lines", "Who could confirm it, and how they would be reached", 2,
              "If the answer is “only me”, it is not evidence yet."),
             ("lines", "What it would take to make it stronger this month", 2, None),
         ]),

        ("fig", "bands", {"segments": [
            (0, 2, "0–1", "Nothing countable, or evidence you produced yourself."),
            (2, 4, "2–3", "Real conversations, but you raised the problem every time."),
            (4, 5, "4", "Ten or more, several of whom raised it unprompted."),
            (5, 6, "5", "The above, plus somebody gave you money, time or a commitment."),
        ], "scale_max": 6},
         "<b>Score requirement 02.</b> Unprompted mentions and money are the two "
         "signals that cannot be manufactured by asking nicely."),

        ("break",),

        ("label", "Requirement 03"),
        ("h1", "Something that exists"),
        ("p", "This requirement is widely misread as “a working product”. It "
              "is not. What a reader wants to know is whether you convert intent into "
              "an artefact, because most people never do. A spreadsheet you run by "
              "hand for four real users clears this bar. A beautiful deck does not."),

        ("work", "Worksheet 3 · What exists", "Requirement 03", None, [
             ("lines", "What you have built or run, in one line", 1,
              "Manual counts. Paper counts. A group chat you moderate counts."),
             ("lines", "How many people other than you have used it, and when", 1, None),
             ("lines", "What it does today that it did not do a month ago", 2, None),
             ("lines", "Where a stranger could see it or try it", 1,
              "A link, a file, a place. Not a description."),
         ]),

        ("fig", "bands", {"segments": [
            (0, 2, "0–1", "Nothing exists outside documents and conversations."),
            (2, 4, "2–3", "Something exists but only you have used it."),
            (4, 5, "4", "Real people other than you have used it at least once."),
            (5, 6, "5", "People came back to it without being asked."),
        ], "scale_max": 6},
         "<b>Score requirement 03.</b> The bar is use by somebody else, not polish. A "
         "rough thing five people used beats a finished thing nobody has touched."),

        ("break",),

        ("label", "Requirement 04"),
        ("h1", "A reason it is you"),
        ("p", "The weakest possible answer is enthusiasm, because every applicant has "
              "it. The strongest is something a competitor would have to spend real "
              "time or money to acquire: access to the people with the problem, a "
              "skill that is scarce where you are, or a history with the problem that "
              "gives you judgement nobody can look up."),

        ("work", "Worksheet 4 · The unfair part", "Requirement 04", None, [
             ("lines", "Access you have that a stranger does not — to customers, a place, a network, data", 2, None),
             ("lines", "A skill you have that is genuinely scarce in this market", 2, None),
             ("lines", "Your history with this problem", 2,
              "Having lived it counts for a great deal. Say so plainly if you have."),
             ("lines", "How long it would take a well-funded stranger to get what you have", 1,
              "If the answer is under a month, this is not yet an advantage."),
         ]),

        ("fig", "bands", {"segments": [
            (0, 2, "0–1", "Interest and commitment, which everyone has."),
            (2, 4, "2–3", "A relevant skill or background, but nothing hard to acquire."),
            (4, 5, "4", "Access or a history a stranger would need months to build."),
            (5, 6, "5", "The above, and it is already producing results you can point at."),
        ], "scale_max": 6},
         "<b>Score requirement 04.</b> The time-to-copy question at the bottom of the "
         "worksheet is the score. Everything else is context for it."),

        ("break",),

        ("label", "Scoring"),
        ("statement", "Add the four. Read the band. Do not negotiate."),

        ("work", "Your score", "All four requirements", None, [
             ("lines", "01  A named problem and a named person         / 5", 1, None),
             ("lines", "02  Evidence you did not make up               / 5", 1, None),
             ("lines", "03  Something that exists                      / 5", 1, None),
             ("lines", "04  A reason it is you                         / 5", 1, None),
             ("lines", "Total                                         / 20", 1,
              "And the date. You will want it when you do this again."),
         ]),

        ("fig", "bands", {"segments": [
            (0, 7, "0–6", "Applying now wastes the application. Work on your lowest requirement for one month."),
            (7, 13, "7–12", "One real gap. You know which it is — it is the lowest number on your sheet."),
            (13, 17, "13–16", "Applying is reasonable. Close the lowest requirement while you wait to hear."),
            (17, 21, "17–20", "Apply, and to more than one place. Your constraint is no longer readiness."),
        ], "scale_max": 21},
         "<b>The bands.</b> They are deliberately blunt. A score of twelve is not "
         "“almost thirteen” — it is one gap, and the gap has a name."),

        ("h2", "What to do with the result"),
        ("p", "Take the <b>lowest</b> of your four scores, not the total. The total "
              "tells you whether to apply; the lowest score tells you what to do "
              "tomorrow. A founder who spends a month on their weakest requirement "
              "almost always moves further than one who spends it on their strongest."),

        ("table", ["Your lowest score is", "Spend the month on", "The companion resource"], [
            ["Requirement 01", "Twenty conversations with people who have the problem, and one problem statement that survives them",
             "Toolkit 02 — The Evidence Toolkit"],
            ["Requirement 02", "Counting, dating and recording what you already have, then adding to it deliberately",
             "Toolkit 02 — The Evidence Toolkit"],
            ["Requirement 03", "Running the service by hand for ten people, with no product built",
             "Toolkit 03 — The Manual MVP"],
            ["Requirement 04", "Finding the access or skill you already have and making it produce something visible",
             "Toolkit 05 — The Application File"],
        ]),

        ("say", [
            ("You are missing two of the four.", "You've got this."),
            ("Requirement 02 is where most people stall.", "Your journey starts here."),
            ("Twelve out of twenty, dated 14 March.", "You're nearly there."),
            ("You finished it. We just kept the file.", "We built a founder."),
        ]),

        ("note", "Do this again in a month from a blank copy. Do not look at the old "
                 "one until the new one is finished — comparing as you write is how "
                 "a score stops being honest."),
    ],
}
