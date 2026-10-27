"""The Application File — what you hand over instead of hoping."""

DOC = {
    "slug": "tk05-application-file",
    "file": "StartPad_Toolkit_05_The_Application_File",
    "kind": "toolkit",
    "series": "StartPad Toolkit",
    "number": "No. 05",
    "title": "The Application File",
    "standfirst": "Apply with a file, not a hope. Everything a reviewer needs, "
                  "assembled so it works without you in the room — which is "
                  "exactly how it will be read.",
    "standfirst_plain": "How to assemble the one-pager, evidence appendix and cover "
                        "note that a programme or first cheque actually reads.",
    "cover_foot": "A weekend · Assemble once, reuse everywhere",
    "keywords": ["accelerator application", "pitch", "one pager", "fundraising",
                 "programme application", "MENA"],
    "missions": [15],
    "blocks": [

        ("label", "The situation"),
        ("statement", "Your file is read for ninety seconds, by somebody tired."),
        ("lead", "A reviewer working through a hundred applications is not looking "
                 "for reasons to say yes. They are looking for reasons to stop "
                 "reading, because stopping is how the pile gets smaller. Everything "
                 "below is built around that fact rather than around what would be "
                 "pleasant to believe."),

        ("p", "This has a practical consequence that most applicants miss: the file "
              "is not a persuasion document. It is a verification document. Your job "
              "is to make four claims and make each one instantly checkable. "
              "Persuasion happens later, in a room, if the file has done its job."),

        ("fig", "flow", {"steps": [
            ("Part 01", "The one-pager",
             "Four claims, one page, no decoration. This is the only part most readers will finish."),
            ("Part 02", "The evidence appendix",
             "The numbers behind each claim, with dates and denominators. Read only if the one-pager survived."),
            ("Part 03", "The cover note",
             "Six lines saying why this programme, specifically. Written last, and never reused unchanged."),
        ]}, "<b>Three parts, read in this order and usually not all of them.</b> Build "
            "them in reverse: the evidence first, then the page it supports, then the "
            "note that points at it."),

        ("break",),

        ("label", "01 · The one-pager"),
        ("h1", "Four claims, in the order they are checked"),
        ("p", "The structure below is not a style preference. It follows the order a "
              "reviewer's questions arrive in, which means each section answers the "
              "question the previous one just raised. Reordering it makes the reader "
              "hold questions open, and a tired reader with open questions stops."),

        ("table", ["Section", "What it says", "Length"], [
            ["The problem", "One named person, one situation, what it costs them.", "Two lines"],
            ["The evidence", "How many people, how you know, and one quote.", "Three lines"],
            ["What exists", "What you have built or run, and who has used it.", "Two lines"],
            ["Why you", "The access, skill or history that is hard to copy.", "Two lines"],
            ["The ask", "What you want from this programme specifically.", "One line"],
        ]),

        ("callout", "The thing to delete first",
         "The paragraph about how large the market is. A reviewer already knows the "
         "market is large — that is why they run the programme. It is the only "
         "section of an application that is identical across every applicant, so it "
         "carries no information about you at all."),

        ("work", "Worksheet 1 · The one-pager", "Draft it here first",
         "Write it by hand before you type it. The constraint of the ruled lines does "
         "most of the editing for you.", [
             ("lines", "The problem — named person, situation, cost", 2, None),
             ("lines", "The evidence — number, how, and one verbatim quote", 3,
              "Fractions with denominators. “11 of 34”, not “many”."),
             ("lines", "What exists — what you built or ran, and who used it", 2, None),
             ("lines", "Why you — the part that is hard to copy", 2, None),
             ("lines", "The ask — from this programme, specifically", 1, None),
         ]),

        ("break",),

        ("label", "02 · The evidence appendix"),
        ("h1", "Every claim, with the number that supports it"),
        ("p", "The appendix exists so that a reviewer who wants to check one thing "
              "can find it in ten seconds. It is not a longer version of the "
              "one-pager and it should contain almost no prose. One row per claim, "
              "each with a date, a number and a source a person could follow up."),

        ("table", ["Claim on the one-pager", "The number", "Where it came from", "Date"], [
            ["People have this problem", "17 of 20 raised it unprompted", "Evidence log, Toolkit 02", "March"],
            ["It costs them real money", "Median 4 hours a week, as stated", "Evidence log, column 7", "March"],
            ["Something exists", "10 deliveries, by hand", "Delivery log, Toolkit 03", "April"],
            ["People want it enough to pay", "11 of 34 paid a deposit", "Test worksheet, Toolkit 04", "May"],
            ["They come back", "6 of 10 returned with no reminder", "Delivery log, weeks 4–6", "May"],
        ]),

        ("p", "Rows like these are what a reviewer means when they ask how you know. "
              "Note what they are made of: counts, denominators and dates, all of "
              "which came out of work you did anyway if you have used the earlier "
              "toolkits in this library. The appendix is an assembly job, not a "
              "writing job."),

        ("check", [
            ("Every number has a denominator", "“30 sign-ups” becomes “30 of 210”, or it comes out."),
            ("Every claim has a date", "A reviewer discounts undated evidence to zero, and is right to."),
            ("Every row names a source somebody could check", "A log, a receipt, a person who agreed to be contacted."),
            ("Nothing appears here that is not on the one-pager", "The appendix supports claims; it does not add new ones."),
            ("No adjectives", "Strong, significant, huge, validated. Delete each one and see if the row still says anything."),
            ("It fits on one page", "If it does not, you are explaining rather than evidencing."),
        ]),

        ("break",),

        ("label", "03 · The cover note"),
        ("h1", "Six lines that could not have been sent to anyone else"),
        ("p", "The cover note is the only part of the file that is specific to the "
              "reader, and it is the part most applicants reuse unchanged. A note "
              "that names the programme's actual focus, one thing they have backed "
              "before, and what you want from them specifically is rare enough to be "
              "worth the twenty minutes it takes."),

        ("work", "Worksheet 2 · The cover note", "One per programme", None, [
             ("lines", "Why this programme — something true about them, not about you", 2,
              "If the sentence would work for three other programmes, it is not this line."),
             ("lines", "The single strongest number from your appendix", 1, None),
             ("lines", "What you want from them that is not money", 2,
              "Access, a specific mentor, a customer introduction, a licence question answered."),
             ("lines", "What you will have done by the time they decide", 1,
              "Shows the work continues whether or not they say yes. It nearly always helps."),
         ]),

        ("say", [
            ("11 of 34 paid a 50 EGP deposit in April.", "We have strong early traction."),
            ("Six of ten came back with no reminder.", "Users love the product."),
            ("I ran it by hand for ten people in Shubra.", "We have built an MVP."),
            ("I want an introduction to two pharmacy chains.", "We are seeking funding to scale."),
        ]),

        ("break",),

        ("label", "04 · Before you send it"),
        ("h1", "The checks that catch most rejections"),

        ("check", [
            ("Someone who has never heard of you read the one-pager and explained it back correctly",
             "If they got the problem wrong, the file failed, not the reader."),
            ("Every number on the page also appears in the appendix, identically",
             "A mismatch between the two is the fastest way to lose a reviewer's trust."),
            ("The file opens without you", "No password, no request-access link, no format nobody has. A PDF."),
            ("Your name and a way to reach you are on page one", "This is missed more often than it sounds."),
            ("You have answered the actual questions asked", "Programmes ask specific things. Answering a different question reads as a mass send."),
            ("The strongest evidence is in the first five lines", "The reader may not reach line six."),
            ("You could defend every claim in a room, from the appendix alone", "If you cannot, remove the claim rather than soften it."),
        ]),

        ("callout", "If you are not ready, send it anyway — to one place",
         "A rejection with a reason is worth a month of guessing. Apply to one "
         "programme you expect to be declined by, ask for the reason, and treat the "
         "answer as the next month's brief. Apply to ten at once and you learn "
         "nothing ten times."),

        ("fig", "ribbon", {"active": [15]},
         "<b>Where this sits.</b> Mission 15. The file assembles from the logs and "
         "worksheets produced in missions 02, 03, 09, 13 and 14 — which is why it "
         "takes a weekend rather than a month."),

        ("note", "Keep the file in one folder with the logs it cites. When somebody "
                 "asks how you know, the answer should be a file you can send in "
                 "under a minute, not a conversation you have to schedule."),
    ],
}
