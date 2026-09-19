"""The Demand Signal — what counts as traction before you have revenue."""

DOC = {
    "slug": "tk04-demand-signal",
    "file": "StartPad_Toolkit_04_The_Demand_Signal",
    "kind": "toolkit",
    "series": "StartPad Toolkit",
    "number": "No. 04",
    "title": "The Demand Signal",
    "standfirst": "Interest is free, which is why everybody has it. A signal is "
                  "something that cost the other person something. This is how to "
                  "design one, run it, and read the result without flattering yourself.",
    "standfirst_plain": "How to design and run a demand test that produces evidence a "
                        "stranger would accept, before you have revenue.",
    "cover_foot": "Two weeks per test · Run one at a time",
    "keywords": ["traction", "demand validation", "product market fit", "experiments",
                 "startup metrics", "MENA"],
    "missions": [13, 14],
    "blocks": [

        ("label", "The test"),
        ("statement", "If it cost them nothing, it told you nothing."),
        ("lead", "Every demand signal can be ranked by one question: what did the "
                 "person give up to produce it? A click costs a second. A phone "
                 "number costs a little privacy. A deposit costs money and the "
                 "embarrassment of asking for it back. The ranking is the whole "
                 "method."),

        ("fig", "ladder", {"rungs": [
            ("They paid, before it existed", "The strongest signal available to anyone. A small amount taken seriously beats a large amount promised."),
            ("They came back, unprompted", "Return without a reminder. Almost impossible to manufacture, which is why it counts."),
            ("They did work for you", "Filled a long form, gave you data, brought a colleague. Effort is a currency."),
            ("They gave a way to be reached", "A phone number or a real email. Costs a little, and is checkable."),
            ("They said yes to a question", "Free to give, pleasant to say, and predicts almost nothing."),
            ("They clicked, or liked it", "A measure of your headline, not of your product."),
        ], "caption_high": "COSTS THEM MOST", "caption_low": "COSTS THEM NOTHING"},
         "<b>Signals, ranked by what they cost the person giving them.</b> Read your "
         "own evidence against this ladder before you put it in an application — a "
         "reader will."),

        ("p", "This ranking is also the reason a waiting list of two thousand can be "
              "worth less than eleven people who paid. Programmes and investors have "
              "seen enough of both to price them correctly, and describing the "
              "waiting list as traction in front of someone who knows the difference "
              "costs you more than saying nothing."),

        ("break",),

        ("label", "01 · Designing a test"),
        ("h1", "One question, one number, one decision, written first"),
        ("p", "A test you designed after seeing the result is not a test. Write the "
              "four lines below before you run anything, and keep the paper. The "
              "discipline is not bureaucratic — it is the only defence against "
              "reading a disappointing result as an encouraging one."),

        ("num", [
            ("01", "The question",
             "One sentence, answerable yes or no. “Will people in this building pay "
             "50 EGP for this to be done on a Friday?”"),
            ("02", "The number that answers it",
             "Decide what you will count. Not three numbers — one."),
            ("03", "The threshold, decided now",
             "The value above which you continue and below which you stop. Write the "
             "actual number before you start."),
            ("04", "What you will do either way",
             "Both branches, written down. If both branches say “keep going”, "
             "you have not designed a test."),
        ]),

        ("work", "Worksheet 1 · Test design", "Fill this in before you run anything",
         "Sign and date it. Yes, really — a dated page is much harder to quietly "
         "revise once the result is in.", [
             ("lines", "The question, answerable yes or no", 2, None),
             ("lines", "The one number I will count", 1, None),
             ("lines", "How many people will be given the chance", 1,
              "The denominator. A result with no denominator is not a rate."),
             ("lines", "My threshold — at or above this I continue", 1, None),
             ("lines", "What I do if it comes in below", 2,
              "Be specific. “Rethink” is not an action."),
             ("lines", "Date and signature", 1, None),
         ]),

        ("callout", "How big should the threshold be?",
         "For a first test with ten to thirty people, pick a number that would "
         "surprise a sceptical friend. Small samples cannot detect small effects, so "
         "a threshold of “one or two” tells you nothing you did not already "
         "believe. If the honest threshold is small, run the test on more people."),

        ("break",),

        ("label", "02 · Four tests that work with no product"),
        ("h1", "Each costs the person something different"),

        ("fig", "flow", {"steps": [
            ("Test 01", "The pre-order",
             "Ask for a small payment now for delivery later. Refund anyone who asks, immediately and without friction."),
            ("Test 02", "The manual offer",
             "Offer to do it by hand this week, at a price. Counts how many say yes and then actually turn up."),
            ("Test 03", "The reachable list",
             "Collect phone numbers, then call them. The signal is not the sign-up — it is who answers."),
            ("Test 04", "The unprompted return",
             "Stop all reminders for two weeks. Count who comes back on their own."),
        ], "note": "Run one at a time. Two tests in one fortnight produce a result you "
                   "cannot attribute to either."},
         "<b>Four tests, ranked by cost to the participant.</b> All four can be run "
         "with no product, no company and no budget beyond your own time."),

        ("callout", "On taking money before you can deliver",
         "It is the strongest signal and it carries a real obligation. Take small "
         "amounts, say plainly what they are buying and when, refund instantly on "
         "request, and keep a record of every payment and every refund. A test that "
         "leaves somebody out of pocket is not a test, it is a debt."),

        ("break",),

        ("label", "03 · Reading the result"),
        ("h1", "Rates, not counts — and the denominator in the same sentence"),
        ("p", "“Thirty people signed up” is not a result. Thirty out of forty is "
              "a strong result; thirty out of four thousand is a weak one; and the "
              "sentence is identical until the denominator is in it. Write every "
              "number as a fraction, always, including in your own notes."),

        ("fig", "compare", {
            "left": ("Say this", [
                "11 of 34 people paid a 50 EGP deposit",
                "6 of 10 came back in a fortnight with no reminder",
                "Median cost they described: 4 hours a week",
                "3 of 20 asked to pay before I offered a price",
            ]),
            "right": ("Never say this", [
                "Strong early traction",
                "Great feedback from users",
                "Significant interest from the market",
                "Validated demand",
            ]),
        }, "<b>The left column is checkable and the right column is not.</b> A reader "
           "who sees the right column assumes the left column would have been worse, "
           "because a founder with good numbers prints the numbers."),

        ("work", "Worksheet 2 · The result", "After the test", None, [
             ("lines", "The number, as a fraction, with the denominator", 1, None),
             ("lines", "My threshold was", 1,
              "Copy it from Worksheet 1 without looking at the result first."),
             ("lines", "Above or below?", 1, None),
             ("lines", "What I said I would do in that case", 2, None),
             ("lines", "What I am actually going to do — and if it differs, why", 3,
              "Differing is allowed. Differing without writing down why is how founders fool themselves."),
         ]),

        ("h2", "Three ways a result lies"),
        ("num", [
            ("01", "You asked people who like you",
             "Friends, family and classmates will say yes to almost anything. Their yes "
             "is affection, correctly measured. Run the test again on strangers."),
            ("02", "You changed the offer halfway",
             "Dropping the price or adding a feature mid-test means the number at the "
             "end answers a question you never asked. Start again."),
            ("03", "You counted the enthusiastic and forgot the silent",
             "Everyone who was given the chance belongs in the denominator, including "
             "the people who ignored you. Especially those."),
        ]),

        ("fig", "ribbon", {"active": [13, 14]},
         "<b>Where this sits.</b> Missions 13 and 14. One designed test with a written "
         "threshold answers Mission 14 better than any self-assessment of fit."),

        ("note", "Fit is not a score you give yourself. It is a set of numbers with "
                 "denominators, taken from tests you designed before you saw the "
                 "results. Keep the signed worksheets — they are the most credible "
                 "part of an early application."),
    ],
}
