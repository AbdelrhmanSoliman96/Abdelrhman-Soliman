"""The Readiness Gap — why 80,000 becomes 1,000."""

DOC = {
    "slug": "wp01-readiness-gap",
    "file": "StartPad_The_Readiness_Gap",
    "kind": "whitepaper",
    "series": "StartPad Whitepaper",
    "number": "No. 01",
    "title": "The Readiness Gap",
    "standfirst": "Eighty thousand people a year register interest in building "
                  "something in Egypt. About a thousand end up with a company. "
                  "The loss is not motivation and it is not ideas.",
    "standfirst_plain": "Why most people who want to build a company in Egypt never "
                        "reach the programmes built to help them, and what closes the gap.",
    "cover_foot": "Twelve minutes · Read before Mission 01",
    "keywords": ["founder readiness", "Egypt", "MENA", "startup ecosystem",
                 "accelerators", "entrepreneurship"],
    "missions": [1, 2],
    "blocks": [

        ("label", "01 · The ground"),
        ("statement", "Entrepreneurship here is not a lifestyle choice."),
        ("lead", "In a labour market this tight, starting something is often the "
                 "rational option rather than the romantic one. That changes who is "
                 "trying, how much room they have to fail, and what they need before "
                 "anyone will meet them."),

        ("fig", "stat_row", {"tiles": [
            ("18.3%", "Youth unemployment, and rising", "StartPad market analysis, 2026"),
            ("77%", "Of young people outside the labour force", "StartPad market analysis, 2026"),
            ("−53%", "Formal private employment, over six years", "StartPad market analysis, 2026"),
        ]}, "<b>The conditions people are starting from.</b> These are not three "
            "readings of the same thing. The first says jobs are scarce; the second "
            "says most young people have stopped looking; the third says the formal "
            "private sector has been shrinking while they did.",
         "Source: StartPad market analysis, 2026. Re-verify against the primary "
         "labour statistics before quoting externally."),

        ("p", "Read together, those three figures describe a population for whom "
              "building something is not a detour from a career. It is the career. "
              "That is a different starting point from the one most startup "
              "programming is designed around, and it has a practical consequence: "
              "these founders cannot afford a year of learning in public. They need "
              "to know where they stand now."),

        ("h2", "The number that matters more"),
        ("p", "Interest is not the constraint. Every year roughly eighty thousand "
              "people in Egypt register interest with the ecosystem — they sign "
              "up, they apply, they show up to a session, they join a list. Roughly "
              "a thousand of them end the year holding a company."),

        ("fig", "funnel", {"stages": [
            ("Register interest with the ecosystem", 80000, "80,000"),
            ("Become companies, per year", 1000, "1,000"),
        ], "note": "One in eighty. The step that loses the other seventy-nine is not "
                   "a step anybody runs a programme for."},
         "<b>Eighty thousand in, a thousand out.</b> The attrition is not spread "
         "evenly across a pipeline. It happens almost entirely before the first "
         "formal gate, among people who never submitted anything at all.",
         "Source: StartPad market analysis, 2026."),

        ("break",),

        ("label", "02 · Where the gap sits"),
        ("statement", "Nobody serves the person who is not yet a founder."),
        ("p", "Every serious institution in this market begins one step after where "
              "its audience is standing. National platforms connect founders to the "
              "ecosystem, in Arabic, at no cost — and they are good at it. "
              "Accelerators select. Funds invest. The newer AI co-founder products "
              "sell features to people already building."),
        ("p", "All of them assume a founder. None of them make one. The step between "
              "wanting to build something and being someone a programme will meet is "
              "the whole business, and it is unattended."),

        ("fig", "compare", {
            "left": ("What the person actually needs first", [
                "To know which specific requirements they fail, by name",
                "A route that closes those gaps in a sensible order",
                "Evidence they can hand to someone else",
                "Someone to tell them the truth before the encouragement",
            ]),
            "right": ("What the market currently offers them", [
                "Connection to programmes that will decline them",
                "Curriculum, sold by the hour, with no diagnosis",
                "Feature lists that assume a company already exists",
                "Encouragement, which costs nothing and proves nothing",
            ]),
        }, "<b>The mismatch is one of sequence, not of quality.</b> Everything in the "
           "right-hand column is useful — to somebody who has already cleared the "
           "step in the left-hand column."),

        ("callout", "The practical test",
         "Ask any programme what proportion of applications they reject at the first "
         "screen, and why. The answers are remarkably consistent, and remarkably "
         "boring: no evidence of demand, no clarity about who the customer is, "
         "nothing built, nothing measured. None of those are failures of ambition."),

        ("h2", "Why the gap is invisible"),
        ("p", "A person who never applies leaves no record. They do not appear in a "
              "rejection rate, they do not fill in an exit survey, and they do not "
              "complain, because they usually conclude the problem was them. The "
              "ecosystem's own data therefore cannot see its largest loss."),
        ("p", "This is why the gap persists despite genuine effort and real money "
              "being spent on it. It is not that anyone has decided to ignore these "
              "people. It is that the measurement stops at the door they never "
              "reached."),

        ("break",),

        ("label", "03 · What readiness is made of"),
        ("statement", "Four things get asked for, in almost every room."),
        ("p", "Programmes, competitions, grant committees and first-cheque investors "
              "in this region vary enormously in what they fund and almost not at all "
              "in what they ask for at the first screen. Stripped of house style, the "
              "questions reduce to four."),

        ("num", [
            ("01", "A named problem, and a named person who has it",
             "Not a market, not a segment, not “young people in Egypt”. One "
             "describable person, and what specifically goes wrong for them today."),
            ("02", "Evidence you did not make up",
             "Conversations you actually had, counted and dated. A waiting list. A "
             "pre-order. A usage log. Anything a stranger could check."),
            ("03", "Something that exists",
             "A prototype, a manual service, a spreadsheet you run by hand for real "
             "users. It does not have to be software and it does not have to scale."),
            ("04", "A reason it is you",
             "Access, a skill, a history with the problem. The weakest answer is "
             "enthusiasm; the strongest is an unfair advantage you can name in a line."),
        ]),

        ("p", "Nothing on that list requires funding, a co-founder, a company, or a "
              "single line of code. All four can be built by one person with a "
              "notebook and a month. That is the good news buried in the eighty "
              "thousand: the gap is not made of resources. It is made of sequence "
              "and of nobody telling you which of the four you are missing."),

        ("fig", "compare", {
            "left": ("Counts as evidence", [
                "Twenty conversations, dated, with who said what",
                "A waiting list with names on it",
                "Someone who paid before the thing existed",
                "A usage log from a service you ran by hand",
            ]),
            "right": ("Does not count as evidence", [
                "\u201cEveryone I spoke to loved it\u201d",
                "A survey you wrote and your friends answered",
                "Market size taken from a consultancy report",
                "Sign-ups to a page that promised something free",
            ]),
        }, "<b>The second requirement is where founders lose.</b> Almost everyone "
           "arrives believing they have evidence. The test is not whether you "
           "believe it \u2014 it is whether a stranger could check it without "
           "taking your word for anything."),

        ("break",),

        ("label", "04 · What closes it"),
        ("statement", "Requirement, gap, route — in that order."),
        ("p", "The order matters more than any individual step. Told the route first, "
              "a founder optimises for the route. Told the requirement first, they "
              "optimise for the requirement, which is the thing actually being judged."),

        ("fig", "flow", {"steps": [
            ("Step 01", "Truth",
             "Where you stand against what programmes actually ask for. Stated plainly, before any encouragement."),
            ("Step 02", "Readiness",
             "Structured missions that close the specific gaps found, in the order that matters. A route, not a curriculum."),
            ("Step 03", "Proof",
             "A credential the ecosystem can check without asking you. You apply with a file, not a hope."),
        ]}, "<b>Three moves, always in this order.</b> Each one is worthless without "
            "the one before it: a route with no diagnosis is a course, and proof with "
            "no route is a certificate."),

        ("h2", "Why proof is the part that is missing"),
        ("p", "Diagnosis exists in this market, informally. Routes exist, in the form "
              "of curricula. What does not exist is a way for a founder to carry the "
              "result of either to a third party who did not watch them do it."),
        ("p", "Everything a first-time founder builds in their first six months is "
              "currently unverifiable by anyone but them. Twenty interviews and a "
              "signed waiting list look exactly like a confident claim about twenty "
              "interviews and a signed waiting list. A credential that a programme "
              "can check without contacting the holder is the only thing that "
              "separates the two."),

        ("quote", "You finished it. The platform just kept the file.", "The distinction that matters"),

        ("break",),

        ("label", "05 · If this is you"),
        ("statement", "The first month is diagnostic, not productive."),
        ("p", "The most common mistake made by someone in the eighty thousand is to "
              "start building. It feels like progress, it is measurable, and it "
              "postpones the uncomfortable question of whether anyone wants the "
              "thing. A month spent on requirements one and two costs almost nothing "
              "and changes what you build."),

        ("fig", "ribbon", {"active": [1, 2]},
         "<b>Where this sits.</b> Missions 01 and 02 do the diagnostic work this "
         "paper argues for. Everything after them is only worth doing once those two "
         "have an answer."),

        ("h3", "Three things to do this week"),
        ("ol", [
            "Write down the four requirements and mark yourself honestly against "
            "each. Not “partly” — met or not met.",
            "For every requirement you marked as met, write the evidence a stranger "
            "could check. If you cannot, it is not met.",
            "Pick the single weakest of the four and spend the month on it alone.",
        ]),

        ("callout", "The one rule",
         "If your answer to any of the four requires you to be in the room "
         "explaining it, it is not yet an answer. The whole point of a file is that "
         "it works without you."),

        ("h2", "A note on these figures"),
        ("p", "The labour-market and funnel figures in this paper come from "
              "StartPad's own market analysis rather than from a single published "
              "dataset. They are directional and they are the basis on which the "
              "platform was built. Anyone citing them externally — in a pitch, an "
              "article or an application — should trace them to the underlying "
              "statistics first. Proving rather than claiming applies to us too."),

        ("note", "This paper is part of the StartPad founder resource library. The "
                 "companion toolkit, <b>The Readiness Audit</b>, turns the four "
                 "requirements into a scored worksheet you can complete in an hour."),
    ],
}
