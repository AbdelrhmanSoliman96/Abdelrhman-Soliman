# -*- coding: utf-8 -*-
"""
Source of truth for the Techne partnership proposal (the DOCX to attach) and the
outreach email that carries it.

Deliberately short. This is read by a partnerships team seventeen days out from
their own event, so it opens with the ask and keeps to two pages. The full
reasoning lives in the Mission Zero playbook, linked at the end.
"""

TITLE = "The StartPad Youth Track at Techne Summit 2026"
SUBTITLE = ("A proposal to run a national youth qualification challenge as an official "
            "track — funded, produced and staffed by StartPad")
META = [
    ("From", "Abdelrhman Soliman, Founder, StartPad (a GrowthLabs company)"),
    ("To", "Techne — Partnerships / Programming"),
    ("Date", "9 September 2026"),
    ("Ask", "A workshop slot in Cairo, a 30-minute stage slot in Alexandria on 5 October, "
            "and track naming"),
]

BLOCKS = [
    ("h", "In one paragraph"),
    ("p",
     "StartPad turns a first idea into an evidence-backed company through 15 guided missions. "
     "We would like to run a national youth challenge on that structure as an official track at "
     "Techne Summit 2026 — launched from your stage in Cairo on 26–27 September, with a live "
     "final in Alexandria on 5 October. We fund the EGP 100,000 prize pool, produce the "
     "programming and staff it. We are asking Techne for stage time, track naming and reach."),

    ("h", "Why this complements Compete rather than competing with it"),
    ("p",
     "Techne's Compete track and the Startup World Cup tournament serve teams with a prototype, "
     "traction and an investment case. This track serves the stage before that: students and "
     "first-time founders with no registered company, no funding and no revenue — explicitly "
     "excluded by our own eligibility rules, so the two fields cannot overlap."),
    ("p",
     "It is a feeder, not a rival. Our top ten finishers enter Techne's Compete track in 2027, "
     "having already completed eight missions of documented customer work — a better-prepared "
     "cohort than a cold application round produces."),

    ("h", "What Techne gets"),
    ("b", [
        "Fully produced youth programming at no cost and no operational load on your team.",
        "EGP 100,000 in prizes funded by StartPad, awarded under joint Techne × StartPad branding.",
        "Techne co-branding on every certificate and on the track inside the platform — visibility "
        "that continues long after the summit closes.",
        "A scored, auditable qualification pipeline you can reuse for Techne Drifts, replacing "
        "ad-hoc screening with a published rubric.",
        "Aggregated data on youth entrepreneurship by governorate — the kind of outcome reporting "
        "a summit held under the auspices of MCIT and ITIDA can use directly.",
        "Free StartPad licences for all Techne Drifts participants for twelve months.",
    ]),

    ("h", "What we are asking for"),
    ("b", [
        "Official track status and naming: the StartPad Youth Track at Techne Summit 2026.",
        "A 45-minute workshop slot in Cairo on 26 or 27 September (“Mission 1 Live” — every "
        "attendee completes their first mission in the room, on their phone).",
        "A 30-minute stage slot in Alexandria on 5 October for the live final.",
        "Booth or activation space in both cities, comped or discounted against the programming "
        "we deliver.",
        "Listing in the agenda and event app, two mailer mentions and three social posts.",
        "Two judges from your network, and an introduction to ITIDA or TIEC for a third.",
        "Introductions into the Techne Drifts cities and their university contacts.",
        "First option to host the Demo Day at a Drift stop in late November.",
    ]),

    ("h", "How it runs"),
    ("b", [
        "26–27 Sept, Cairo — launch, workshop, and recruitment of a 40-team sprint cohort.",
        "28 Sept – 2 Oct — sprint week: Missions 1 to 4, with online office hours.",
        "5 Oct, Alexandria — six teams pitch on stage; the national challenge opens from the same "
        "stage.",
        "6 Oct – 16 Nov — the national challenge: Missions 1 to 8, ending at a completed Business "
        "Model Canvas.",
        "Late Nov — Demo Day: top ten pitch, EGP 50,000 / 30,000 / 20,000 awarded.",
    ]),
    ("p",
     "Judging is deliberately not left to software. Automated scoring only filters the field; a "
     "blind human panel scores the shortlist, customer interviews are logged and randomly "
     "verified, and the live pitch decides. Participants keep all intellectual property in their "
     "ideas — there is no assignment clause and no right of first refusal."),

    ("h", "Who is behind it"),
    ("p",
     "StartPad is part of GrowthLabs, which builds the digital infrastructure of entrepreneurship "
     "ecosystems and has supported more than 5,000 startups across more than 60 international "
     "programmes, alongside CatalystOS and Startup Gate."),

    ("h", "Next step"),
    ("p",
     "A 20-minute call this week. Given that your own event is seventeen days away, we have "
     "prepared everything to run with or without changes — if a stage slot is not available this "
     "year, we would rather agree a 2027 track now than add to your load in September."),
]

CONTACT = [
    ("Abdelrhman Soliman", "Founder, StartPad"),
    ("Email", "[EMAIL]"),
    ("Phone / WhatsApp", "[PHONE]"),
    ("Web", "startpad.me  ·  growthlabs.app"),
    ("Full plan", "[PLAYBOOK LINK]"),
]

EMAIL_SUBJECT = ("Youth track at Techne Summit 2026 — we fund the prizes and produce it, "
                 "you keep the stage")

EMAIL_BODY = """Dear [NAME],

Techne Drifts already runs the national youth roadshow, and Compete already serves startups with
traction. There is a gap between them: the student who has an idea and has never spoken to a
customer. We would like to fill it at Techne Summit 2026, as your track.

StartPad turns a first idea into an evidence-backed company through 15 guided missions. We want to
run a national youth challenge on that structure, launched from your stage in Cairo on 26-27
September with a live final in Alexandria on 5 October.

We fund the EGP 100,000 prize pool, produce the programming and staff it. What we are asking for is
stage time, track naming and reach:

- a 45-minute workshop slot in Cairo, where every attendee completes their first mission in the room
- a 30-minute stage slot in Alexandria on 5 October for the final
- booth space, agenda listing, and introductions into the Drifts cities

What you get: youth programming at no cost, joint branding on every certificate, a scored
qualification pipeline you can reuse for Drifts, governorate-level data on youth entrepreneurship
for your MCIT and ITIDA reporting, and free StartPad licences for all Drifts participants for a
year. Our top ten enter Compete in 2027 — this feeds your track rather than competing with it.

Eligibility excludes anyone with a registered company, funding or revenue, so we cannot draw
entrants away from Compete or the Startup World Cup tournament.

The two-page proposal is attached. Could we take 20 minutes this week? I know exactly how close
your event is, so if a slot is not possible this year I would rather use the call to agree a 2027
track than add to your September.

Best regards,

Abdelrhman Soliman
Founder, StartPad (a GrowthLabs company)
[PHONE] · startpad.me
"""
