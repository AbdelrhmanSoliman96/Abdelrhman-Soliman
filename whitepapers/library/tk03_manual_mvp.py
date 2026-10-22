"""The Manual MVP — thirty days, ten users, nothing built."""

DOC = {
    "slug": "tk03-manual-mvp",
    "file": "StartPad_Toolkit_03_The_Manual_MVP",
    "kind": "toolkit",
    "series": "StartPad Toolkit",
    "number": "No. 03",
    "title": "The Manual MVP",
    "standfirst": "Thirty days, ten real users, and no product. Deliver the service "
                  "by hand first — it is faster, it teaches you more, and it is "
                  "the version you can afford to be wrong about.",
    "standfirst_plain": "How to run your first product manually for ten real users in "
                        "thirty days, without writing code.",
    "cover_foot": "Thirty days · No code required",
    "keywords": ["MVP", "concierge MVP", "no-code", "prototype", "product",
                 "startup", "MENA"],
    "missions": [9, 13],
    "blocks": [

        ("label", "The idea"),
        ("statement", "The first version should be a person, not a product."),
        ("lead", "Almost everything you need to learn in the first month is about "
                 "what people actually want done, in what order, and what they will "
                 "tolerate. None of that requires software. All of it is obscured by "
                 "building software, because building takes long enough that you stop "
                 "asking."),

        ("p", "A manual first version is not a lesser version. It is a different "
              "instrument, built to answer a different question. Software answers "
              "“can this scale”. A person with a notebook answers “does "
              "anybody want this” — which is the question you actually have."),

        ("fig", "flow", {"steps": [
            ("Pattern 01", "Concierge",
             "You do the whole job by hand and the user knows it. Slowest per user, and by far the most informative."),
            ("Pattern 02", "Wizard of Oz",
             "The user sees a product; behind it, you are doing the work. Tests the interface as well as the service."),
            ("Pattern 03", "Piecemeal",
             "Stitch existing tools together — a form, a sheet, a chat group. Nothing built, everything running."),
        ], "note": "Most first months should be concierge. The other two are what you "
                   "move to once you know what the job actually is."},
         "<b>Three ways to run a product that does not exist.</b> They differ in how "
         "much the user can see, not in how real the service is. In all three, "
         "somebody genuinely gets their problem solved."),

        ("callout", "What this is not",
         "This is not a landing page with a waiting list. A page measures curiosity. "
         "A manual service measures whether the thing you would build actually helps "
         "— and it produces a customer, which a page never does."),

        ("break",),

        ("label", "01 · Scoping"),
        ("h1", "Cut it until one person can run it in a day"),
        ("p", "The most common failure of a manual first version is that it is still "
              "too big. If you cannot personally deliver it for ten people using "
              "hours you actually have, it is not scoped yet. Cut scope, not quality: "
              "serve fewer people, in a smaller place, solving a narrower slice."),

        ("fig", "compare", {
            "left": ("Cut these", [
                "Anyone outside one neighbourhood, campus or building",
                "Every feature that is not the one they described",
                "Payments, until somebody has asked to pay",
                "Accounts, logins, dashboards and settings",
                "Everything that only matters at a hundred users",
            ]),
            "right": ("Keep these", [
                "The one thing that goes wrong for them today",
                "A way for them to reach you that they already use",
                "A record of what you did for each person",
                "The promise you made about when it would be done",
                "A way for them to come back tomorrow",
            ]),
        }, "<b>Scope is subtraction.</b> Everything in the left column is work that "
           "will be needed eventually and teaches you nothing this month."),

        ("work", "Worksheet 1 · The manual service spec", "Before day one",
         "One page. If it does not fit, it is not scoped.", [
             ("lines", "The one job you are doing for people, in a sentence", 2, None),
             ("lines", "Who exactly — how would you recognise an eligible person?", 2,
              "Narrow is good. “Students in one faculty” beats “students”."),
             ("lines", "How they ask you for it", 1,
              "Use a channel they already have open. A WhatsApp number beats an app."),
             ("lines", "What you do, step by step, by hand", 4,
              "Write every step. This list becomes the specification if you ever build it."),
             ("lines", "What they get, and by when", 2,
              "A promise with a time in it. This is the only thing you must not break."),
             ("lines", "The hours per user this will cost you", 1,
              "Multiply by ten. If that number is larger than your month, cut again."),
         ]),

        ("break",),

        ("label", "02 · Thirty days"),
        ("h1", "Two users a week, then everything at once"),

        ("fig", "timeline", {"phases": [
            ("Scope and set up", 0, 4, "Write the spec, open the channel, tell nobody yet."),
            ("First two users", 4, 5, "Deliberately over-serve them. Learn where the job really is."),
            ("Rewrite the spec", 9, 2, "You will be wrong about at least one step. Fix it before scaling the error."),
            ("Users three to ten", 11, 14, "Two a week. Log every delivery on the day it happens."),
            ("Hold and watch", 25, 4, "Stop recruiting. See who comes back without being asked."),
            ("Decide", 29, 1, "Build, change, or stop — against the numbers, not the feeling."),
        ], "span_label": "Thirty days", "unit": "day"},
         "<b>Thirty days, six phases.</b> The hold in the last week is the most "
         "valuable part and the part founders skip: a service nobody returns to "
         "while you are still pushing it has told you something."),

        ("callout", "Over-serve the first two, deliberately",
         "Do things that could never scale. Deliver it personally, on a Friday, at "
         "their office. You are not testing the economics this month — you are "
         "finding out what the job actually is, and the only way to find that is to "
         "do it all yourself once."),

        ("break",),

        ("label", "03 · The delivery log"),
        ("h1", "One row per delivery, on the day"),
        ("p", "This log is the difference between a month of favours and a month of "
              "evidence. It is also the specification for whatever you build next: "
              "every step you performed by hand is a step the software will have to "
              "perform, and every step you kept skipping is one it will not."),

        ("table", ["Column", "What goes in it"], [
            ["Date", "The day you delivered, not the day they asked."],
            ["Who", "Name or initials."],
            ["What they asked for", "In their words, not your categories."],
            ["What you actually did", "Every step, including the ones you improvised."],
            ["Time it took you", "Honestly. This is your future unit cost."],
            ["What went wrong", "Something always does. This is the most useful column."],
            ["Did they come back?", "And whether you had to ask them to."],
        ]),

        ("work", "Delivery log · rows 1–4", "Copy this page three times", None, [
             ("lines", "1.  Date · Who · Asked for · Time taken", 2, None),
             ("lines", "    What I did, and what went wrong", 3, None),
             ("lines", "2.  Date · Who · Asked for · Time taken", 2, None),
             ("lines", "    What I did, and what went wrong", 3, None),
             ("lines", "3.  Date · Who · Asked for · Time taken", 2, None),
             ("lines", "    What I did, and what went wrong", 3, None),
         ]),

        ("break",),

        ("label", "04 · What counts as done"),
        ("h1", "Existence is use by somebody else"),
        ("p", "There is a ladder here, and knowing which rung you are on is worth "
              "more than moving up it quickly. Most first-time founders describe "
              "themselves two rungs above where they actually are, which is why "
              "readers of applications discount what they are told."),

        ("fig", "ladder", {"rungs": [
            ("People came back without being asked", "The only rung that predicts anything. Everything below it can be produced by effort and goodwill."),
            ("Ten people used it, once", "Real, countable, and enough for an application. This is the target for thirty days."),
            ("Two people used it", "A pilot. Informative for you, not yet evidence for anyone else."),
            ("It works, and only you have used it", "A demo. Common, and routinely described as an MVP."),
            ("It is designed and described", "A document. Nothing has been tested yet."),
        ], "caption_high": "REAL", "caption_low": "CLAIMED"},
         "<b>Where you actually are.</b> Find your rung honestly. A founder who says "
         "“two people used it, and neither came back” is more credible than one "
         "who says “we have an MVP”, and is treated accordingly."),

        ("work", "Worksheet 2 · The thirty-day decision", "Day thirty", None, [
             ("lines", "People who used it at least once", 1, None),
             ("lines", "People who came back without being asked", 1,
              "The number that matters. Zero is a finding, not a failure."),
             ("lines", "Median time it took you per delivery", 1, None),
             ("lines", "The step that broke most often", 2,
              "This is the first thing worth automating, and possibly the only thing."),
             ("lines", "What you would build, now, in one sentence — and what you no longer would", 3, None),
             ("lines", "Build, change the service, or stop", 2, None),
         ]),

        ("callout", "The one thing to automate first",
         "Not the thing that is most interesting to build. The step in your log that "
         "broke most often, or took longest. If those are different steps, take the "
         "one that broke — slow is survivable, broken is not."),

        ("fig", "ribbon", {"active": [9, 13]},
         "<b>Where this sits.</b> Missions 09 and 13. The delivery log from this "
         "month is the input to Mission 14 and to <b>Toolkit 04 — The Demand "
         "Signal</b>."),

        ("note", "Nothing in this toolkit requires you to write code, register a "
                 "company, or spend money. If your version of it does, the scope is "
                 "still too big — go back to Worksheet 1 and cut again."),
    ],
}
