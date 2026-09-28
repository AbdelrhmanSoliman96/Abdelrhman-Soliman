"""
Review 01 — where the camp content and the platform journey do not line up.

A one-page partner note, not a published founder resource. It stays out of the public
resources bundle and is addressed to GrowthLabs, Cognify Academy and the host
university.

Scope is deliberately narrow: content and journey only. Every claim is checked
against the camp's design pack and `startpad/missions.py` — the mission titles, the
questions each mission actually asks, and the Bazaar rubric's published weights.

It is written to one page, which is a hard constraint rather than a style: the
content below was cut to fit it, and anything added has to displace something.
"""

PACK = "Entrepreneurship Camp Learner Journey, GrowthLabs Group × Cognify Academy, September 2026"

DOC = {
    "slug": "rv01-camp-integration",
    "file": "StartPad_Review_01_Content_Journey_Gap",
    "kind": "review",
    "layout": "brief",
    # A hard limit, enforced by scripts/check_pdfs.py: anything added here has to
    # displace something, or the build fails.
    "max_pages": 1,
    "series": "StartPad Programme Review",
    "number": "No. 01",
    "title": "Half the Rubric Has No Mission",
    "standfirst": "Where the camp's content and the platform's journey part company — "
                  "and the three changes that close it.",
    "standfirst_plain": "Content and journey alignment between the Future Founders "
                        "camp and the StartPad mission sequence.",
    "cover_foot": "For GrowthLabs, Cognify Academy and the university",
    "keywords": ["curriculum alignment", "StartPad missions", "entrepreneurship "
                 "education", "camp content", "GrowthLabs"],
    "missions": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "blocks": [

        ("p", "The sequencing is right — teaching order was bent so missions unlock "
              "in order. The problem is content, not order. Four of the seven Bazaar "
              "criteria, <b>50% of the score</b>, measure work no mission has a field "
              "for; two missions ask for work the camp has not taught yet; and two "
              "hand students a different tool from the one they were given in class "
              "three hours earlier."),

        ("table", ["Day", "What the camp produces", "Missions", "Where content and journey part"], [
            ["1", "Impact × Frequency matrix, persona", "01–03",
             "We call the same matrix <b>Importance</b>/Frequency. Mission 01 also asks what solutions exist and their limits — competitor work the camp never teaches."],
            ["2", "Problem statement, solution on value × <b>effort</b>, value proposition, test plan", "04–06, 07",
             "Mission 05 scores solutions on value × <b>impact</b> — a different axis, the same evening. Mission 06 wants 3–5 product features; product work is Day 4."],
            ["3", "Unit cost, price, margin, break-even", "08",
             "<b>No mission records finance.</b> The canvas has one Revenue Streams box. Four hours and 15% of the rubric land nowhere."],
            ["4", "Prototype, user test, brand kit", "09–10",
             "<b>No mission records branding</b> — an hour of Day 4 and 10% of the rubric. Mission 09 asks what technology stack was used, of students building in cardboard."],
            ["5", "Pitch deck, rehearsed pitch, Q&amp;A", "catch-up only",
             "<b>No mission records the pitch.</b> A whole day and 25% of the rubric: the largest gap in the map."],
        ]),

        ("num", [
            ("01", "Add the two missions the camp already does the work for",
             "<b>Costs and Pricing</b> after mission 08, <b>Brand and Pitch</b> after "
             "10. Both fill from artefacts made in class, so neither adds homework, "
             "and together they take the unrecorded half of the rubric to nothing."),
            ("02", "Change mission 05 from value × impact to value × effort",
             "The camp's axis is the better one: a fifteen-year-old can estimate "
             "effort and cannot estimate impact before collecting the evidence."),
            ("03", "Move the competitor questions from mission 01 to mission 04",
             "On night one they are guesswork. After the interviews they are "
             "answerable, and the camp has taught something to answer them with."),
        ]),

        ("note", "Also: seven of the ten mission titles in the pack are not what a "
                 "student sees on screen, and the pack's are clearer. Missions 11–15 "
                 "are never taught, and two do not fit this age as written. Checked "
                 "against the <b>Entrepreneurship Camp Learner Journey</b> pack, "
                 "September 2026, and our own mission and question list; the 50% is "
                 "the published Bazaar weights for finance, brand, pitch and Q&amp;A."),
    ],
}
