"""Report 05 — Believed or Shared: calm mode and energy mode as a communications rule."""

DOC = {
    "slug": "r05-believed-or-shared",
    "file": "StartPad_Report_05_Believed_Or_Shared",
    "kind": "report",
    "series": "StartPad Report",
    "number": "No. 05",
    "title": "Believed or Shared",
    "standfirst": "The book splits every asset into two intensities by asking one "
                  "question: does this have to be believed, or reposted? Founders "
                  "who ask it before writing stop sending the wrong document.",
    "standfirst_plain": "The calm-mode and energy-mode distinction from the StartPad "
                        "brand book, applied to founder communications.",
    "cover_foot": "Report · Derived from Chapter 04",
    "keywords": ["founder communications", "investor updates", "marketing",
                 "pitch", "StartPad", "MENA"],
    "missions": [11, 12, 15],
    "blocks": [

        ("label", "The source"),
        ("bookref", "Same DNA, different intensity, not two brands. Anything that "
                    "has to be believed rather than shared.",
         "Chapter 04 · The language, two intensities"),

        ("statement", "One question decides the whole document."),
        ("lead", "The book divides its outputs into calm mode — documents, "
                 "certificates, partnership and institutional material — and "
                 "energy mode, for social, campaign and launch. The dividing line is "
                 "not the audience or the channel. It is whether the thing has to be "
                 "<b>believed</b> or <b>shared</b>, and those want opposite treatments."),

        ("fig", "compare", {
            "left": ("Has to be believed", [
                "An investor update or a data room",
                "An application to a programme",
                "A customer proposal or a quote",
                "A partnership memorandum",
                "Anything a lawyer or a committee will read",
            ]),
            "right": ("Has to be shared", [
                "A launch post",
                "A hiring call",
                "An event announcement",
                "A milestone your customers should see",
                "Anything whose job is to be forwarded",
            ]),
        }, "<b>Same company, same facts, opposite treatment.</b> The failure is "
           "almost never the writing — it is a document built for one column being "
           "sent to the other."),

        ("break",),

        ("label", "01 · What each mode is allowed"),
        ("statement", "Restraint is a feature of one and a fault in the other."),

        ("table", ["", "Believed", "Shared"], [
            ["Length", "As long as the evidence needs. Nothing decorative.",
             "One idea. Cut until only it is left."],
            ["Numbers", "Every one sourced, dated, with a denominator.",
             "One number, chosen because it is memorable."],
            ["Tone", "Flat. The facts carry it; adjectives subtract.",
             "Warm. It has to be worth somebody's reputation to forward."],
            ["Design", "Plain. A document that must be believed is not decorated.",
             "Loud. It is competing in a feed."],
            ["What it opens with", "The requirement, or the bad news.",
             "The thing that makes somebody stop scrolling."],
            ["Success looks like", "Nobody asks a follow-up question you cannot answer.",
             "Somebody who does not know you passes it on."],
        ]),

        ("callout", "The most common mistake in this market",
         "Sending an energy-mode document to a believed-mode reader. A deck full of "
         "adjectives, big claims and no denominators reads as a campaign to an "
         "investment committee, and a committee that thinks it is being marketed to "
         "stops reading the numbers."),

        ("h2", "The rarer mistake, and its cost"),
        ("p", "The inverse also happens: a founder writes a launch post the way they "
              "would write a memorandum. Careful, sourced, hedged — and nobody "
              "shares it, because there is nothing in it worth attaching your name "
              "to. Accuracy is not the constraint in the shared column. Being worth "
              "forwarding is."),

        ("break",),

        ("label", "02 · The DNA does not change"),
        ("statement", "Not two brands. Not two founders."),
        ("p", "The book is careful to say these are one system at two intensities. "
              "The founder equivalent matters: the claims must be identical in both "
              "modes. A shared post that says something the believed document would "
              "not support is not a different intensity — it is a different "
              "company, and in a market this small the two audiences overlap."),

        ("fig", "states", {"items": [
            ("Same claim, both modes", "The only safe position. What you post is what the data room would support, said more loudly."),
            ("Louder in public", "A claim the document would soften. Survives until somebody who read both compares them."),
            ("Different claim", "Two companies. The moment an investor sees the post and the deck together, everything else is re-read."),
        ], "note": "The book's phrase is the useful one: same DNA, different "
                   "intensity, not two brands."},
         "<b>Intensity may change; the claim may not.</b> Egypt's ecosystem is small "
         "enough that both audiences meet, usually sooner than the founder expects."),

        ("break",),

        ("label", "03 · Before you send anything"),

        ("work", "Worksheet · Mode check", "Two minutes, before sending",
         "Run this on the next thing you are about to send to somebody outside the company.", [
             ("lines", "Does this have to be believed, or shared? One word.", 1, None),
             ("lines", "If believed — which claim in it is unsourced?", 2,
              "Source it or cut it. There is no third option in this column."),
             ("lines", "If shared — what is the one idea, and what can go?", 2,
              "If you cannot name one idea, it is not ready to be shared."),
             ("lines", "Would the other mode's version of this contradict it?", 2,
              "If yes, fix the claim, not the wording."),
         ]),

        ("check", [
            ("The believed version opens with the requirement or the bad news",
             "Not with context, and not with momentum."),
            ("Every number in the believed version has a source and a denominator",
             "A number without a denominator is a claim wearing a number's clothes."),
            ("The shared version carries exactly one idea",
             "Two ideas in a post means neither is remembered."),
            ("Nothing in the shared version would need softening in the believed one",
             "Same DNA. This is the check that protects both."),
            ("Neither version contains a promise about funding",
             "The book lists this among what the brand refuses, and it is good advice for a founder."),
        ]),

        ("say", [
            ("11 of 34 paid a deposit in April.", "Incredible response from the market!"),
            ("We missed the target and here is why.", "Lots of exciting progress!"),
            ("They grew 40%; we handled the logistics.", "We grew our client 40%."),
            ("Accepted into the cohort, March.", "We're going to be huge."),
        ]),

        ("note", "The book lists what the voice refuses: hype, cheerleading, startup "
                 "romanticism, and promises about funding. All four are energy-mode "
                 "habits that leak into believed-mode documents, which is where they "
                 "do the damage."),
    ],
}
