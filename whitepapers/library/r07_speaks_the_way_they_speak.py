"""Report 07 — Speaks the Way They Speak: composed, not translated."""

DOC = {
    "slug": "r07-composed-not-translated",
    "file": "StartPad_Report_07_Composed_Not_Translated",
    "kind": "report",
    "series": "StartPad Report",
    "number": "No. 07",
    "title": "Composed, Not Translated",
    "standfirst": "The book refuses to translate its Arabic. The reason is "
                  "commercial rather than sentimental, and it decides how a founder "
                  "in this region should write everything a customer reads.",
    "standfirst_plain": "The composed-not-translated language rule from the StartPad "
                        "brand book, applied to how founders write for MENA customers.",
    "cover_foot": "Report · Derived from Chapters 03 and 05",
    "keywords": ["localisation", "Arabic", "copywriting", "customer communication",
                 "Egypt", "MENA", "StartPad"],
    "missions": [6, 11, 12],
    "blocks": [

        ("label", "The source"),
        ("bookref", "Speaks the way they speak — Egyptian colloquial, composed not "
                    "translated. If it reads as a translation, it was written wrong.",
         "Chapter 05 · The voice"),

        ("statement", "A translation is detectable, and being detected is the cost."),
        ("lead", "The rule is not about respect and it is not about reach. It is "
                 "about a specific signal: text that has been translated reads as "
                 "translated, and a reader who notices concludes that they were not "
                 "the audience the thing was made for. That conclusion is expensive "
                 "and it is arrived at in about two seconds."),

        ("p", "The book goes further than most brands would dare, setting Arabic at "
              "hero scale with English small and precisely aligned beneath it — "
              "explicitly a translation register, not two equal languages competing. "
              "It also rules that everyday assets carry one language only. Both "
              "decisions are worth a founder's attention, because both cost "
              "something and were taken anyway."),

        ("break",),

        ("label", "01 · What translation leaks"),
        ("statement", "Structure survives translation. That is the problem."),
        ("p", "Words translate; sentence shape does not. A paragraph composed in "
              "English and rendered into Arabic keeps English clause order, English "
              "hedging and English idiom underneath the Arabic vocabulary. Native "
              "readers do not need to identify what is wrong to register that "
              "something is."),

        ("fig", "compare", {
            "left": ("Composed", [
                "Written first in the language the reader uses",
                "Idiom that belongs to the reader's city, not to a dictionary",
                "Length set by what the language needs to say it",
                "Checked by somebody who would use it in conversation",
            ]),
            "right": ("Translated", [
                "Written in English, then converted",
                "Idiom that is technically correct and used by nobody",
                "Length inherited from the English original",
                "Checked for accuracy rather than for naturalness",
            ]),
        }, "<b>The right column is usually accurate.</b> Accuracy is not what is "
           "being judged — belonging is, and a reader makes that judgement before "
           "they finish the first line."),

        ("callout", "The cheapest test available",
         "Read your Arabic copy out loud to somebody who speaks it daily and watch "
         "their face, not their notes. Hesitation is the finding. If they say "
         "“it's correct, but nobody says it like that”, it was translated, and "
         "that sentence is worth more than any review round."),

        ("break",),

        ("label", "02 · One language per asset"),
        ("statement", "Bilingual everything is a decision nobody made."),
        ("p", "The default in this region is to put both languages on everything, "
              "which feels safe and is rarely chosen deliberately. The book takes the "
              "opposite position for everyday assets: one language each. The reason "
              "is that a bilingual asset is half wasted on every reader, and the half "
              "they are not reading is competing for the space that would have made "
              "the half they are reading land."),

        ("table", ["Asset", "The book's rule", "The founder equivalent"], [
            ["Everyday asset — a post, an ad, a page",
             "One language per asset.",
             "Two versions, each composed. Not one with both languages stacked."],
            ["Hero — a campaign line, a headline",
             "Arabic large, English small beneath, precisely aligned.",
             "Lead in the language of the market you are selling to."],
            ["Institutional — a contract, a data room",
             "Whatever the reader requires, plainly.",
             "English for most regional investors; Arabic where the counterparty works in it."],
        ]),

        ("p", "The practical objection is cost: two composed versions is more work "
              "than one translated pair. It is, and the work is the point. A founder "
              "who cannot afford two composed versions should pick one language and "
              "do it properly rather than produce two halves."),

        ("break",),

        ("label", "03 · Where this decides revenue"),
        ("statement", "Your customers do not read your deck. They read your form."),
        ("p", "Founders pour attention into investor-facing English and leave the "
              "customer-facing Arabic to whoever had time. It is exactly backwards: "
              "the deck is read once by somebody who is paid to read carefully, and "
              "the form, the error message and the confirmation are read by every "
              "customer at the moment they decide whether to trust you."),

        ("fig", "ladder", {"rungs": [
            ("The moment money is asked for", "A checkout line or a price. Composed, or the hesitation costs the sale."),
            ("Error and failure messages", "Read at the worst moment. A translated apology reads as indifference."),
            ("The form fields and their labels", "The most-read text you own, and usually the least edited."),
            ("Onboarding and confirmations", "Sets whether the thing feels made for them."),
            ("Marketing copy", "Where all the attention goes, and the least consequential of the five."),
        ], "caption_high": "MOST CONSEQUENTIAL", "caption_low": "LEAST"},
         "<b>Ranked by what a badly composed line actually costs.</b> The order is "
         "close to the inverse of where most founders spend their editing time."),

        ("work", "Worksheet · The composition audit", "One hour",
         "Go through the product and the funnel, not the marketing site.", [
             ("lines", "The five pieces of text a customer is most likely to read", 3,
              "Count, do not guess. Your analytics or your own funnel will tell you."),
             ("lines", "Which of those five were composed, and which were translated", 2, None),
             ("lines", "The one that sits closest to the moment money is asked for", 1, None),
             ("lines", "Who will compose it — name a person, not a service", 1,
              "Somebody who speaks it daily and is allowed to change the meaning, not just the words."),
             ("lines", "What I will stop translating entirely", 2,
              "One language done properly beats two done halfway, and costs less."),
         ]),

        ("callout", "On the founder writing it themselves",
         "If you speak the language your customers use, write the customer-facing "
         "text yourself, badly, and have somebody tidy it. That produces better copy "
         "than a professional translation of your English, because the structure "
         "starts in the right place."),

        ("say", [
            ("Written the way a customer would say it.", "Fully localised for the MENA market."),
            ("One language, done properly.", "Available in English and Arabic."),
            ("Somebody who uses it daily read it aloud.", "Reviewed by a native speaker."),
            ("We do not translate the checkout.", "Our platform supports multiple languages."),
        ]),

        ("note", "The book pairs this rule with a typographic one: Arabic is set in "
                 "Zain, chosen on its own terms rather than bent to mimic the Latin, "
                 "because forcing an Arabic face to match a geometric construction "
                 "always reads as a compromise. The same instinct applies to the "
                 "words."),
    ],
}
