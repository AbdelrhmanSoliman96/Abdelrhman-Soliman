"""
Review 01 — founder's feedback on the Entrepreneurship Camp StartPad integration.

A three-page partner brief, not a published founder resource. It stays out of the
public resources bundle and is addressed to GrowthLabs, Cognify Academy and the host
university.

It is written against the delivery plan rather than the design pack alone: StartPad
is open for one month alongside the camp and every student gets their own account.
That is a better arrangement than the pack describes, and it moves the problem.
Every figure is taken from the pack or checked against `startpad/missions.py`; where
a number is arithmetic on the pack's ranges rather than something it states, the page
says so.
"""

PACK = "Entrepreneurship Camp Learner Journey, GrowthLabs Group × Cognify Academy, September 2026"

DOC = {
    "slug": "rv01-camp-integration",
    "file": "StartPad_Review_01_Camp_Integration_Feedback",
    "kind": "review",
    "layout": "brief",
    "series": "StartPad Programme Review",
    "number": "No. 01",
    "title": "Two Ideas, One Fortnight",
    "standfirst": "Feedback on the Future Founders camp now that StartPad is open "
                  "for a month and every student has their own account. The "
                  "arrangement is right. It creates one collision that has to be "
                  "resolved before Day 1, and it makes the second half of the month "
                  "the most valuable part of the programme.",
    "standfirst_plain": "Founder's feedback on the Future Founders camp and its "
                        "StartPad integration, under one month of access with "
                        "individual student accounts.",
    "cover_foot": "For GrowthLabs, Cognify Academy and the university",
    "keywords": ["programme review", "StartPad integration", "entrepreneurship "
                 "education", "youth", "camp", "GrowthLabs"],
    "missions": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "blocks": [

        ("statement", "The month is the programme. The camp is its first two weeks."),
        ("p", "Opening the platform for a month and giving every student their own "
              "account is better than what the design pack describes, and it removes "
              "the concern I would otherwise have led with: under the pack, twenty "
              "to thirty students share five to seven team accounts and split ten "
              "missions between them, with no personal record of anything. That is "
              "gone. Everything below follows from what replaces it."),

        ("fig", "stat_row", {"tiles": [
            ("1 account", "Per student, not per team", "Delivery plan, September 2026"),
            ("30 days", "Of access; the camp uses 6 of them", "Delivery plan · pack, Part 1"),
            ("2 ideas", "A team venture and a personal one, in the same fortnight",
             "The collision this brief is about"),
        ]}, "<b>What changed, and what it created.</b> The first two figures are the "
            "improvement. The third is the consequence nobody has decided about yet."),

        ("h2", "The collision"),
        ("p", "The camp is team-based: students form teams on Day 1, carry one "
              "venture through six modules, and pitch it at the Bazaar. The platform "
              "is now personal: each student has an account and can execute their "
              "own idea. Those are two different ventures competing for the same two "
              "weeks, and a fourteen-year-old will not resolve it on their own — "
              "they will do whichever one is graded, which is the team's."),

        ("p", "The pack's elegance depends on the two being the same thing — teams "
              "produce the artefact in class and enter that work at home, so the "
              "platform records work that already exists instead of generating more. "
              "If the account holds a different idea, that elegance is gone and the "
              "homework doubles, for the age group least able to absorb it."),

        ("h2", "What I would do: same venture for six days, own idea for the rest of the month"),

        ("fig", "timeline", {"phases": [
            ("Camp, week 1", 0, 1, "Days 1–3. Personal accounts; every student logs the team's venture themselves. Missions 01–08."),
            ("Camp, week 2", 1, 1, "Days 4–6 and the Bazaar. Missions 09–10 and catch-up."),
            ("Open weeks 3–4", 2, 2, "Either continue the team venture into missions 11–15, or start a personal idea at mission 01. The student chooses."),
        ], "span_label": "The month", "unit": "week"},
         "<b>The month, as I would run it.</b> One venture while the camp is "
         "running, because the camp's design depends on it; the choice opens the day "
         "after the Bazaar, when there is time to take it."),

        ("p", "This keeps every benefit of the personal account — own record, own "
              "submissions, own credential — while class and homework stay the same "
              "piece of work. It also gives the second half of the month a job. At "
              "present the fortnight after the Bazaar has nothing designed into it, "
              "and it is the half where a student first builds something of their own."),

        ("callout", "The sentence to put in the Day 1 onboarding",
         "“For the next two weeks your account holds your team's venture, and you "
         "enter your own part of it. After the Bazaar the account is yours for "
         "another two weeks — carry the team's idea further, or start your own from "
         "mission one.” Said on Day 1, it removes the ambiguity for the whole month."),

        ("h2", "Six things to settle before Day 1"),

        ("table", ["", "What", "Why it matters now", "Owner"], [
            ["01", "Update Part 4 of the pack",
             "It still states one shared team account as a confirmed decision, and facilitators run what the pack says.",
             "Camp"],
            ["02", "Fix the mission names",
             "Seven of the ten names in the pack are not what a student sees on screen — checked against the platform, not from memory. Fifteen minutes, or support questions on the first night.",
             "StartPad"],
            ["03", "Give the Bazaar rubric one StartPad criterion",
             "None of the seven criteria scores platform work, so it is worth nothing to a student's grade. Judges already hold the artefacts and are not asked to score them.",
             "Camp"],
            ["04", "Make the supervised homework slot the default",
             "Home device access is still an open question, and with individual accounts it is one device per student. The students without one are the ones this platform exists for.",
             "University"],
            ["05", "Decide the language before the workbook prints",
             "If the classroom runs in English and the platform in Arabic, every student translates their own work alone at nine in the evening, at thirteen.",
             "University + StartPad"],
            ["06", "Tone-check the evaluator for ages 13–17",
             "Our stated audience is 18–30 and the evaluator has never been calibrated on a fourteen-year-old's answer.",
             "StartPad"],
        ]),

        ("p", "Items 02 and 06 are ours and both are small. Item 03 is the one I "
              "would argue for hardest: a criterion scoring the evidence trail "
              "rewards exactly the discipline the camp teaches on Day 2 and checks "
              "on Day 3, and it is the only thing on the rubric that cannot be "
              "produced the night before the Bazaar."),

        ("h2", "Day 31"),
        ("p", "One month of access needs a stated end, and it is a brand decision "
              "rather than a billing one. If the account locks and the student loses "
              "their submissions, we will have taught thirty young people that a "
              "platform takes your work back — the opposite of what we say on our "
              "first screen, and worse than not running the integration at all."),

        ("kv", [
            ("The account", "Stays open and free at whatever mission they reached. It does not lock."),
            ("The artefacts", "Stay theirs, sealed and dated. Nothing is withdrawn."),
            ("The credential", "Issued for what was actually completed, however far that got."),
            ("The last email", "Names the next mission. Silence is the one outcome to avoid."),
        ]),

        ("h2", "The measure I would hold us to"),
        ("p", "Not missions completed and not XP — both are already in the post-camp "
              "report. The measure is how many of the students hold a personal "
              "account with at least one mission they completed themselves, ninety "
              "days after the Bazaar. The one-month, one-account decision makes that "
              "number possible; the six items above make it more than zero."),

        ("note", "Written against the <b>Entrepreneurship Camp Learner Journey</b> "
                 "pack, September 2026; figures are from it or checked against the "
                 "platform's mission list. What the pack gets right is untouched: "
                 "teaching order bent to fit mission order, thresholds set before "
                 "tests, work produced in class first."),
    ],
}
