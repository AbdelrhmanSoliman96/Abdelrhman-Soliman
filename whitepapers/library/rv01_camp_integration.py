"""
Review 01 — founder's feedback on the Entrepreneurship Camp StartPad integration.

This is a partner review, not a published founder resource. It stays out of the
public resources bundle and is addressed to GrowthLabs, Cognify Academy and the
host university.

Every figure in it is taken from the pack itself or checked against
`startpad/missions.py`. Where a number is an inference rather than something the
pack states, the page says so.
"""

PACK = "Entrepreneurship Camp Learner Journey, GrowthLabs Group × Cognify Academy, September 2026"

DOC = {
    "slug": "rv01-camp-integration",
    "file": "StartPad_Review_01_Camp_Integration_Feedback",
    "kind": "review",
    "series": "StartPad Programme Review",
    "number": "No. 01",
    "title": "One Account, Five Students",
    "standfirst": "Feedback on the Future Founders camp and its StartPad "
                  "integration — what the pack gets right, and the nine gaps "
                  "between where it stands and every student learning from the "
                  "platform rather than five teams using it.",
    "standfirst_plain": "Founder's review of the Future Founders Entrepreneurship "
                        "Summer Camp design pack and its StartPad integration.",
    "cover_foot": "Review · For GrowthLabs, Cognify Academy and the university",
    "keywords": ["programme review", "StartPad integration", "entrepreneurship "
                 "education", "youth", "camp", "GrowthLabs"],
    "missions": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "blocks": [

        ("label", "Summary"),
        ("statement", "The camp is well designed. The integration is not yet a platform integration."),
        ("lead", "The pack is the most carefully sequenced youth programme I have "
                 "read in this market, and one of its decisions — reordering what "
                 "is taught so the homework unlocks in the right order — is better "
                 "than anything we would have specified ourselves. What follows is "
                 "not a criticism of the curriculum. It is about the difference "
                 "between StartPad being present in the camp and every student "
                 "learning from it."),

        ("p", "As written, twenty to thirty students will share five to seven "
              "accounts, split ten missions between them, and be assessed on work "
              "that carries no StartPad weight at all. Most of them will leave "
              "without having personally completed a mission. That is a design "
              "outcome, not a risk — it follows from three decisions in the pack, "
              "and all three are reversible before Day 1."),

        ("fig", "stat_row", {"tiles": [
            ("5–7", "Accounts for 20–30 students", "Pack, Part 4: one shared team account"),
            ("0%", "Of the Bazaar rubric is StartPad work", "Pack, Part 1: seven criteria, none of them the platform"),
            ("10/15", "Missions in scope; five never opened", "Pack, Part 4 · startpad/missions.py"),
        ]}, "<b>Three numbers that decide the rest of this review.</b> None of them "
            "is a judgement — each is stated in the pack or follows directly from "
            "what it states."),

        ("break",),

        ("label", "01 · What the pack gets right"),
        ("statement", "Say this part first, because it is the part worth keeping."),

        ("num", [
            ("01", "The sequencing decision",
             "Solution selection and value proposition were moved to Day 2 so that "
             "missions 05 and 06 unlock before mission 08. Teaching order was bent to "
             "fit the platform rather than the reverse. That is unusual and it is correct."),
            ("02", "Work first, platform second",
             "Teams produce the artefact in class, then enter it at home. The platform "
             "records work that already exists rather than generating homework of its "
             "own. This is the right relationship and it should survive every change below."),
            ("03", "The thresholds are set before the test",
             "Day 2 requires a success threshold written in advance, and Day 3 scores "
             "the verdict against it. A published rubric visible from Day 1. A common "
             "gap column that names “threshold set after the results”. This is the "
             "evidence discipline the platform exists to teach, already in the room."),
            ("04", "Six open decisions, listed rather than assumed",
             "Naming what is unresolved is the hardest part of a programme document "
             "and the pack does it plainly. Two of the six are the subject of this review."),
        ]),

        ("callout", "The one line I would not change",
         "“Assessment adds no extra burden for students, because most evidence is "
         "a team artefact that already exists in the day's flow.” That principle is "
         "why the camp will run well. The recommendations below are written to stay "
         "inside it."),

        ("break",),

        ("label", "02 · The central gap"),
        ("statement", "A student can finish this camp having completed two missions."),

        ("bookref", "Each team works from one shared team account. Teams split "
                    "homework missions among members, so no single student carries "
                    "the load.",
         "Part 4, confirmed design decisions, and Part 1, daily rhythm", PACK, "From the pack"),

        ("p", "Those two sentences are individually sensible and together they "
              "produce the problem. Thirty students in six teams is five per team. "
              "Ten missions split five ways is two missions each. A student who does "
              "exactly what the pack asks will personally complete two of the "
              "platform's fifteen missions — and will have watched, rather than "
              "done, the other eight."),

        ("p", "The certificate confirms it. A student receives it for attending five "
              "of six days and speaking in the pitch. Neither condition involves "
              "StartPad. A rational fifteen-year-old reads that correctly and lets a "
              "teammate log in."),

        ("fig", "compare", {
            "left": ("What the camp measures", [
                "The team's in-class deliverable, at each checkpoint",
                "The team's Bazaar score, on seven criteria",
                "The individual's attendance and speaking turn",
                "The individual's exit tickets and participation",
            ]),
            "right": ("What StartPad measures", [
                "Whether a team account submitted a mission",
                "Nothing about which student did it",
                "Nothing that reaches the Bazaar rubric",
                "Nothing that survives the last day",
            ]),
        }, "<b>The two columns never meet.</b> StartPad artefacts are handed to "
           "judges in advance and no rubric criterion scores them, so the platform "
           "contributes nothing to the only summative assessment in the camp."),

        ("callout", "Why this matters more here than in an adult programme",
         "The platform's product is a personal, verifiable credential — proof that "
         "a named individual did the work. A shared team account cannot issue one, "
         "because there is no individual in it. Run as written, the camp produces "
         "six credentials for thirty students, and they are not credentials of "
         "anything a third party could check."),

        ("break",),

        ("label", "03 · Nine gaps"),
        ("statement", "Ranked by how many students each one leaves out."),

        ("table", ["", "Gap", "Who it excludes", "Fix owner"], [
            ["01", "One shared team account", "Every student but one per mission", "StartPad"],
            ["02", "StartPad carries no assessment weight", "Every student, by incentive", "Camp + StartPad"],
            ["03", "Home access is still an open decision", "Whichever students lack a device — unknown, and the ones who need this most", "University"],
            ["04", "Missions 11–15 out of scope, with no Day 7", "Every student, after the Bazaar", "StartPad"],
            ["05", "Seven of ten mission names do not match the product", "Every student, on Day 1 night", "Camp pack"],
            ["06", "Delivery language undecided", "Unknown; likely the least confident readers", "University + StartPad"],
            ["07", "Ages 13–17 against a platform written for 18–30", "Every student, in tone and in the evaluator", "StartPad"],
            ["08", "No facilitator view of platform progress", "Facilitators, and so every student", "StartPad"],
            ["09", "Nothing is returned to the student after Day 6", "Every student", "StartPad"],
        ]),

        ("h2", "Gap 05, in detail, because it is the cheapest to fix"),
        ("p", "The pack names ten missions. Seven of those names are not what a "
              "student will see when they open the platform that evening. A "
              "thirteen-year-old told to complete “03 Opportunity "
              "Prioritisation” will open StartPad and find “Importance/Frequency "
              "Matrix”. This is a fifteen-minute fix and it will otherwise generate "
              "support questions on the first night, which is the worst possible night."),

        ("table", ["#", "What the student sees in StartPad", "What the pack calls it"], [
            ["01", "Problem Analysis", "Problem Analysis — matches"],
            ["02", "Problem Definition", "Problem Definition — matches"],
            ["03", "Importance/Frequency Matrix", "Opportunity Prioritisation"],
            ["04", "Problem Statements", "Testable Problem Statement"],
            ["05", "Idea Selection", "Solution Selection"],
            ["06", "Idea Description", "Value Proposition &amp; Assumptions"],
            ["07", "Solution Hypothesis Test", "First Assumption Test"],
            ["08", "Business Model Canvas", "Business Model Canvas — matches"],
            ["09", "Build Prototype", "Build a Learning Prototype"],
            ["10", "Solution Hypothesis Test (Prototype)", "Prototype User Test"],
        ]),

        ("note", "Checked against the platform's own mission list rather than from "
                 "memory. Note also that missions 07 and 10 carry nearly the same "
                 "name in the product — a naming problem on our side, not the "
                 "pack's, and one the camp's clearer names would actually solve. "
                 "The right fix is for the product to adopt the pack's names, not "
                 "the other way round."),

        ("break",),

        ("label", "04 · The coverage gap"),
        ("statement", "The camp stops at ten. The credential lives at fifteen."),

        ("fig", "ribbon", {"active": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
         "<b>Missions the camp reaches, and the five it does not.</b> Service "
         "Selection, Market Validation, Build MVP, Product-Market Fit Test and Go to "
         "Market are where the platform's own value sits — and where a student is "
         "left standing on the evening of Day 6, with no route named."),

        ("p", "This is defensible for a six-day camp and it should not be solved by "
              "cramming five more missions into two weeks. It should be solved by "
              "deciding what Day 7 is. At present the pack sends a report to the "
              "university within a week and sends nothing at all to the student."),

        ("fig", "states", {"items": [
            ("Where students are on Day 7", "Ten of fifteen missions, on an account they share with four other people, with no personal record."),
            ("Where the pack leaves them", "A certificate for attendance and a paragraph in a report the university reads."),
            ("Where they could be", "A personal account carrying their own completed missions, and a named next step into missions 11–15."),
        ]}, "<b>The third state costs one email and a migration script.</b> It is "
            "the difference between a camp that used a platform and a platform that "
            "gained thirty founders."),

        ("break",),

        ("label", "05 · What closes them"),
        ("statement", "Three changes carry seven of the nine gaps."),

        ("fig", "flow", {"steps": [
            ("Change 01", "Individual accounts inside a team",
             "Every student gets a personal login. The team keeps a shared workspace, and each mission records which student submitted it."),
            ("Change 02", "One rubric criterion, worth ten per cent",
             "“Evidence trail” on the Bazaar rubric, scored from the platform artefacts the judges already receive in advance."),
            ("Change 03", "A Day 7 email to every student",
             "Their own completed missions, their own account, and missions 11–15 unlocked, with the first one named."),
        ], "note": "None of these adds classroom time, which is the constraint the "
                   "pack is rightly protective of."},
         "<b>Three changes, in the order they should be made.</b> The first is the "
         "one that makes the other two mean anything."),

        ("h3", "Change 01 — individual accounts inside a team workspace"),
        ("p", "This is ours to build and it is the whole review. A team workspace "
              "that holds the shared artefact, with a personal login per student and "
              "an attribution line on every submission, keeps everything the pack "
              "wants — teams split the load, nobody carries it alone — while making "
              "the individual visible. The facilitator's homework check then shows "
              "who has done nothing, which is currently invisible by design."),

        ("h3", "Change 02 — give the platform ten per cent of the rubric"),
        ("p", "Not for our benefit. A rubric that scores the evidence trail rewards "
              "exactly the discipline the camp already teaches on Day 2 and asks "
              "about on Day 3, and it is the only criterion of the seven that cannot "
              "be produced on the last night. Judges already receive the artefacts; "
              "at present they are given material they are not asked to score."),

        ("table", ["Criterion", "Weight now", "Proposed", "Why"], [
            ["Problem and customer evidence", "20%", "20%", "Unchanged."],
            ["Solution and prototype", "20%", "20%", "Unchanged."],
            ["Business and finance logic", "15%", "15%", "Unchanged."],
            ["Brand and booth", "10%", "10%", "Unchanged."],
            ["Pitch delivery", "15%", "10%", "The most coachable criterion and the most rehearsed; five points move well."],
            ["Q&amp;A", "10%", "10%", "Unchanged."],
            ["Teamwork", "10%", "5%", "Already measured daily in the observation log, so it is double counted."],
            ["<b>Evidence trail</b>", "—", "<b>10%</b>", "Scored from the StartPad artefacts judges already hold. Cannot be produced the night before."],
        ]),

        ("h3", "Change 03 — decide what Day 7 is"),
        ("p", "The post-camp report goes to the university within a week. A student "
              "gets a certificate and nothing else. One email, sent the same week, "
              "that hands each student their own account with their own missions on "
              "it, and names the next mission, converts a two-week camp into an "
              "entry point. Without it the camp is a good camp and the platform was "
              "a homework system."),

        ("break",),

        ("label", "06 · The two open decisions that are ours"),
        ("statement", "Home access and language are on the university's list. They should be on ours."),

        ("bookref", "Do all students have a device and internet at home? If not, the "
                    "university could offer a supervised 30-minute homework slot "
                    "after class.",
         "Part 1, open decisions", PACK, "From the pack"),

        ("p", "This is listed as a question for the university and it is really a "
              "product question. If the whole StartPad integration is homework-only "
              "and homework requires a device at home, then the students without one "
              "are excluded from the platform entirely — and they are, reliably, "
              "the students the platform was built for. The supervised slot is the "
              "right answer and it should be the default rather than the fallback, "
              "with one device per team as the Day 1 kit list already assumes."),

        ("p", "Language is the same shape of problem. The pack says StartPad already "
              "supports Arabic, and asks whether the camp runs in English. If the "
              "classroom is one language and the platform is the other, every student "
              "translates their own work at nine in the evening, alone, at thirteen. "
              "My recommendation is that both run in Arabic, with English terms kept "
              "where the industry uses them, and that the decision is made before the "
              "workbook is printed rather than after."),

        ("h2", "Age, honestly"),
        ("p", "The platform's stated audience is eighteen to thirty. These students "
              "are thirteen to seventeen. Missions 07 and 10 ask for tests with real "
              "people, which the pack correctly wraps in safeguarding rules, and the "
              "AI evaluator has never been calibrated on a fourteen-year-old's "
              "answer. Nothing here blocks the camp, and the evaluator's tone is "
              "worth one deliberate pass before Day 1 — unsoftened truth is our "
              "house style with adults and needs a different setting for a child."),

        ("break",),

        ("label", "07 · What I would do first"),
        ("statement", "If only one thing changes, make it the accounts."),

        ("check", [
            ("Individual logins inside a team workspace, with per-mission attribution",
             "Ours. This is the gap; everything else is downstream of it."),
            ("The pack's mission names adopted in the product",
             "Ours, and a fifteen-minute change. The pack's names are better than the product's."),
            ("One rubric criterion for the evidence trail, at ten per cent",
             "Camp, with our input. Judges already hold the material."),
            ("A supervised homework slot as the default, not the fallback",
             "University. Removes the device question from the critical path."),
            ("Both the camp and the platform in the same language, decided before printing",
             "University and us, together, before the workbook goes to print."),
            ("An evaluator tone pass for ages 13–17",
             "Ours. One afternoon, before Day 1."),
            ("A facilitator view showing per-student progress",
             "Ours. The homework check currently happens by looking at a phone."),
            ("A Day 7 email: their account, their missions, the next one named",
             "Ours. Turns a camp into an entry point."),
        ]),

        ("callout", "The measure I would hold us to",
         "Not missions completed and not XP earned — both are already in the "
         "post-camp report and both are team numbers. The measure is how many of the "
         "twenty to thirty students hold a personal account with at least one mission "
         "they completed themselves, ninety days after the Bazaar. Today that number "
         "would be zero, and nothing in the pack is at fault for that. It is ours."),

        ("note", "All figures in this review are taken from the design pack or "
                 "checked against the platform's own mission list. The five-per-team "
                 "and two-missions-per-student figures are arithmetic on the pack's "
                 "stated ranges of 20–30 students and 5–7 teams, not numbers the "
                 "pack gives."),
    ],
}
