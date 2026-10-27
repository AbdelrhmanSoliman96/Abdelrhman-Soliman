"""
Why nobody finishes mission 01, and what to do about it.

The paid conversion problem is not a pricing problem. It is three problems
stacked, and they have to be fixed in order:

  1  ACTIVATION.  Mission 01 asks a stranger who signed up ninety seconds
     ago for five written answers and says it will take two to three hours.
     That is the single largest leak in the product. Nobody converts to paid
     from a mission they never finished.

  2  HABIT.  Nothing brings a user back tomorrow. No nudge they will
     actually see, no peer who notices they stopped, no deadline.

  3  WILLINGNESS AND ABILITY TO PAY.  $15 is priced in dollars and taken by
     card. A large share of the target market has neither a dollar budget
     nor an international card, and a payment that fails is indistinguishable
     from a user who did not want to buy.

Most teams attack the third and discount their way downwards. The money is
in the first.

Everything below is an experiment with a metric, not an opinion. The lift
ranges are what this class of change usually produces in consumer products
in this market; they are planning numbers, not promises, and the only one
that matters is the one measured on this product.
"""

# ---------------------------------------------------------------- the leak
DIAGNOSIS = [
    ("Mission 01 is a wall, not a door",
     "Five open written questions and a stated time of two to three hours, "
     "shown to somebody who has just registered and has no idea yet. The "
     "first thing a new user is asked to do should take ninety seconds and "
     "give them something back. Right now the first thing they are asked "
     "to do is an essay."),
    ("The reward comes after the work, and it should come before",
     "A user gets points and a review after finishing a mission. They need "
     "something to hold after the first sentence they type, not after the "
     "first hour."),
    ("It is a blank page",
     "Every question is an empty box. Most first-time founders do not have "
     "an idea, they have an interest. A blank box asks them to be a founder "
     "before the product has made them one."),
    ("It is written for a keyboard",
     "The target user is on a phone, typing Arabic. Long-form text input on "
     "a phone in Arabic is slow and most people abandon it. The product "
     "asks for about 1,500 words across the first three missions."),
    ("Nothing brings them back",
     "No WhatsApp, no deadline, no peer, no streak. In this market an email "
     "sequence is close to a no-op: the open rate on transactional email to "
     "Egyptian students is a fraction of a WhatsApp read rate."),
    ("The paywall sits at mission 04, which is before anybody is invested",
     "A user who has finished three missions has a problem statement. A "
     "user who has finished five has chosen an idea. The second one has "
     "something to lose, and loss is what people pay to avoid."),
    ("The price is in dollars and the checkout wants a card",
     "The checkout offers valU, Visa and Mastercard. It does not offer "
     "Fawry, Vodafone Cash, InstaPay or Meeza. For a student in Assiut that "
     "is not a price objection, it is a closed door, and it shows up in the "
     "data as low conversion rather than as failed payments."),
    ("Nobody knows where the drop happens",
     "Mission-level analytics cannot tell you that users leave on question "
     "three of mission 01. Until the funnel is instrumented at the level of "
     "the individual field, every fix below is a guess."),
]

# ------------------------------------------------------- what to measure
INSTRUMENTATION = [
    ("Signup to first action", "Event",
     "Time from account created to the first field saved. If the median is "
     "above three minutes, the first screen is wrong.", "Week 1"),
    ("Step-level drop-off inside every mission", "Event",
     "One event per question saved, not one per mission submitted. This is "
     "the single most valuable thing on this list and it does not exist "
     "today.", "Week 1"),
    ("Drop-off by device and by input length", "Segment",
     "Phone against desktop, and completion against the number of "
     "characters the question expects. The correlation will be obvious and "
     "it will tell you which questions to cut.", "Week 1"),
    ("Cohort retention curve by signup week", "Cohort",
     "D1, D3, D7, D14, D30. Without this you cannot tell whether a change "
     "helped or whether a good week of traffic arrived.", "Week 2"),
    ("Paywall view to checkout start to payment attempt to success",
     "Funnel",
     "Four separate events. Most teams measure the first and the last and "
     "call the gap a conversion problem.", "Week 2"),
    ("Payment failure rate by method and by bank", "Funnel",
     "The number nobody measures. In this market a failed card rate of 30 "
     "to 60 per cent is normal and invisible.", "Week 2"),
    ("Review latency", "Event",
     "Minutes from submission to review returned. If it is measured in "
     "hours the loop is broken, because the user has closed the app.",
     "Week 2"),
    ("Source to completion, not source to signup", "Segment",
     "Which acquisition channel brings people who finish. Ambassadors, "
     "chapters and paid traffic will look completely different, and the "
     "cheapest signup is often the worst user.", "Week 3"),
]


# ------------------------------------------------------------ experiments
# (theme, name, hypothesis, what actually changes, primary metric, effort,
#  low lift, high lift, confidence, run in)
E = [
    # -------------------------------------------- A, the first ten minutes
    ("A. The first ten minutes",
     "Ninety-second first action",
     "Users leave because the first thing asked of them is an essay.",
     "Replace the mission 01 form as the landing screen with one screen: "
     "pick a field from twelve tiles, then write one sentence about a "
     "problem you have seen. Nothing else. Mission 01's remaining "
     "questions come after.",
     "Share of signups completing a first action within 10 minutes",
     "S", 2.0, 4.0, "High", "Weeks 3-4"),
    ("A. The first ten minutes",
     "Reward before work",
     "People need to hold something before they will invest an hour.",
     "The moment that one sentence is saved, generate a problem card: "
     "their name, their problem written back to them properly, in Arabic, "
     "designed to be screenshotted and posted.",
     "First action to mission 01 completed",
     "S", 1.3, 1.8, "High", "Weeks 3-4"),
    ("A. The first ten minutes",
     "Kill the blank page",
     "Most first-time founders have an interest, not an idea, and a blank "
     "box asks them to be a founder before the product has made them one.",
     "A bank of 100 real Egyptian problems by sector. Pick one, change it, "
     "make it yours. Starting from somebody else's problem is how most "
     "good ideas actually begin.",
     "First action completion rate",
     "M", 1.4, 2.2, "High", "Weeks 3-5"),
    ("A. The first ten minutes",
     "Arabic voice input",
     "The user is on a phone typing Arabic, which is slow, and the product "
     "asks for about 1,500 words in the first three missions.",
     "Record a voice note to answer any question. Transcribe it, show the "
     "text, let them edit. Speaking for forty seconds is a tenth of the "
     "effort of typing for ten minutes.",
     "Mission completion rate on mobile",
     "M", 1.5, 2.5, "Medium", "Weeks 4-6"),
    ("A. The first ten minutes",
     "Phone number, not email",
     "An email address you cannot reach is a user you have lost.",
     "Sign up with a phone number and an OTP. Email optional. This is the "
     "precondition for every nudge experiment in theme C.",
     "Share of users reachable on WhatsApp",
     "S", 1.0, 1.0, "High", "Weeks 3-4"),

    # ------------------------------------------------- B, mission mechanics
    ("B. Mission mechanics",
     "AI writes the first draft",
     "Editing is an order of magnitude easier than writing, and the "
     "product already has the user's one sentence.",
     "For every question, the AI proposes a draft answer built from what "
     "the user has already said. The user edits or replaces it. Never show "
     "an empty box again.",
     "Mission completion rate",
     "M", 1.8, 3.0, "High", "Weeks 4-6"),
    ("B. Mission mechanics",
     "Honest, smaller time labels",
     "'2-3 hours' on mission 01 is a reason not to start today.",
     "Break each mission into steps of five minutes or less with "
     "save-and-resume, and label it '4 steps, about 12 minutes' rather "
     "than in hours.",
     "Mission start rate",
     "S", 1.3, 1.9, "High", "Weeks 3-4"),
    ("B. Mission mechanics",
     "Cut mission 01 from five questions to two",
     "The first mission should prove the product works, not extract a "
     "business plan.",
     "Mission 01 keeps the field and the problem. The user, the existing "
     "solutions and their limitations move into mission 02, which is "
     "where they belong anyway.",
     "Mission 01 completion rate",
     "S", 1.5, 2.2, "High", "Weeks 3-4"),
    ("B. Mission mechanics",
     "Instant review",
     "A review that arrives hours later arrives after the user has closed "
     "the app, and the loop never closes.",
     "Return the AI review in under sixty seconds, in the same session, "
     "with one specific thing to improve and one thing done well.",
     "Mission 01 to mission 02 started",
     "M", 1.4, 2.0, "High", "Weeks 4-6"),
    ("B. Mission mechanics",
     "Resume where they stopped",
     "Users come back to a home screen and have to find their way again.",
     "Any return goes straight to the exact question they stopped on, with "
     "what they wrote still there.",
     "Return session to step completed",
     "S", 1.2, 1.5, "Medium", "Weeks 4-5"),

    # --------------------------------------------------------- C, the comeback
    ("C. Nudges and the comeback",
     "WhatsApp instead of email",
     "In this market a WhatsApp message is read and an email is not.",
     "A sequence on WhatsApp: one hour, day 1, day 3, day 7, day 14. Every "
     "message names their own problem back to them rather than saying "
     "'continue your journey'.",
     "Day 7 return rate",
     "M", 2.0, 3.5, "High", "Weeks 5-7"),
    ("C. Nudges and the comeback",
     "Answer by replying",
     "The cheapest possible next step is a reply to a message they are "
     "already reading.",
     "The nudge contains the actual next question. Replying to the "
     "WhatsApp writes the answer into the mission. No app, no login, no "
     "typing in a browser.",
     "Steps completed per active user",
     "L", 1.8, 3.0, "Medium", "Weeks 6-9"),
    ("C. Nudges and the comeback",
     "A weekly progress message",
     "People finish things they can see themselves progressing on.",
     "Every Thursday: what you did, where you are of fifteen, how many "
     "people in your governorate are ahead of you.",
     "Week 2 to week 3 retention",
     "S", 1.2, 1.6, "Medium", "Weeks 5-6"),
    ("C. Nudges and the comeback",
     "Day 30 win-back with a sponsored seat",
     "A lapsed user is cheaper to recover than a new one is to acquire.",
     "A message offering a sponsored full-access seat from a named partner "
     "that expires in 72 hours.",
     "Reactivation rate of 30-day lapsed users",
     "S", 1.0, 1.0, "Medium", "Weeks 7-8"),

    # ---------------------------------------------------------- D, other people
    ("D. Other people",
     "A group of twenty who started the same week",
     "Peer presence is the strongest completion lever in free online "
     "learning, and it costs nothing.",
     "Auto-assign every new user to a WhatsApp or Telegram group of twenty "
     "who registered the same week, with a named host from the chapter or "
     "ambassador network.",
     "Mission 03 completion rate",
     "M", 1.8, 2.8, "High", "Weeks 5-8"),
    ("D. Other people",
     "Weekly open office hours",
     "A live human answering the question you are stuck on converts "
     "stalling into finishing.",
     "One hour a week, Arabic, open to everybody, top questions answered "
     "live, recorded. This is the webinar line in the initiative budget "
     "doing double duty.",
     "Attendee completion rate against non-attendees",
     "S", 1.3, 1.8, "Medium", "Weeks 5-7"),
    ("D. Other people",
     "Finish mission 03 with a partner",
     "A commitment made to another person is kept more often than one made "
     "to an app.",
     "At the end of mission 01, invite a friend to be your partner. Both "
     "see each other's progress. This doubles as the referral loop.",
     "Mission 03 completion, and invitations sent",
     "M", 1.4, 2.0, "Medium", "Weeks 6-8"),
    ("D. Other people",
     "Deadlines: challenge weeks",
     "An open-ended course is finished by nobody. A deadline converts "
     "intention into action.",
     "A seven-day national challenge every six weeks, with one shareable "
     "output and a named end date.",
     "Missions completed during challenge weeks against baseline",
     "M", 1.5, 2.5, "High", "Weeks 6-12"),

    # --------------------------------------------------- E, paywall and offer
    ("E. The paywall and the offer",
     "Move the paywall from mission 04 to after mission 05",
     "A user at mission 04 is curious. A user who has chosen an idea at "
     "mission 05 has something to lose.",
     "Free through mission 05. The lock lands at the point of commitment, "
     "when the next step is to build rather than to think.",
     "Paid conversion per registered user",
     "M", 1.5, 2.5, "Medium", "Weeks 9-11"),
    ("E. The paywall and the offer",
     "Sell the outcome, not the content",
     "Nobody in this market pays for twelve more lessons. They pay for a "
     "certificate, a review and a stage.",
     "Reframe Pro as: a reviewed and certified venture, entry to the "
     "national showcase, and the investor-ready pack at the end. The "
     "missions come with it.",
     "Paywall view to checkout start",
     "S", 1.4, 2.2, "High", "Weeks 9-10"),
    ("E. The paywall and the offer",
     "48 hours of everything, then the lock",
     "Loss aversion beats gain framing, reliably.",
     "After mission 03, unlock all fifteen missions for 48 hours. When it "
     "closes, the user has seen what they are losing rather than imagining "
     "what they would gain.",
     "Paid conversion within 7 days of trial end",
     "M", 1.6, 2.6, "Medium", "Weeks 10-12"),
    ("E. The paywall and the offer",
     "Scarce sponsored seats",
     "A free seat from a named bank is both a discount and a reason to act "
     "this week.",
     "'142 sponsored seats left this week from [partner]'. Real scarcity, "
     "real partner, counted down honestly.",
     "Paywall view to activation of any kind",
     "S", 1.3, 2.0, "Medium", "Weeks 9-11"),
    ("E. The paywall and the offer",
     "Buy for three",
     "Buying together is normal here and a group purchase drags two more "
     "users past the paywall.",
     "A team price for three friends at a lower per-person rate, with a "
     "shared progress view.",
     "Paid users per paying transaction",
     "M", 1.2, 1.8, "Low", "Weeks 11-12"),

    # ------------------------------------------------------- F, how they pay
    ("F. Price and payment",
     "Price in pounds, not dollars",
     "A dollar price reads as a foreign product and forces a mental "
     "conversion at the worst possible moment.",
     "Show EGP everywhere, charge in EGP, and never show a dollar figure "
     "to a consumer.",
     "Paywall view to checkout start",
     "S", 1.2, 1.6, "High", "Weeks 7-8"),
    ("F. Price and payment",
     "Fawry, Vodafone Cash, InstaPay and Meeza",
     "The checkout takes valU, Visa and Mastercard. Most of the target "
     "market has none of the three, and a payment that cannot be attempted "
     "looks exactly like a user who did not want to buy.",
     "Add Fawry reference codes, Vodafone Cash, InstaPay and Meeza through "
     "a local gateway. Measure the failure rate of every method "
     "separately.",
     "Checkout start to payment success",
     "M", 2.0, 4.0, "High", "Weeks 7-10"),
    ("F. Price and payment",
     "Find the real price",
     "$15 is roughly EGP 800, which for a student is a week of part-time "
     "work. The price was set in dollars for a model, not tested on a "
     "market.",
     "A price ladder: EGP 299, EGP 399, EGP 499, against the current "
     "equivalent. Measure revenue per registered user, not conversion "
     "rate, so a cheaper price has to earn its place.",
     "Revenue per registered user",
     "S", 1.3, 2.2, "Medium", "Weeks 10-12"),
    ("F. Price and payment",
     "Pay in two",
     "Instalments are how this market buys everything above a few hundred "
     "pounds.",
     "Two payments, with valU already in the checkout and Sympl or Aman "
     "beside it for smaller tickets.",
     "Paid conversion at the higher price points",
     "M", 1.2, 1.7, "Medium", "Weeks 10-12"),
    ("F. Price and payment",
     "Settle what Pro actually is",
     "The financial model carries Pro as $15 a year and the team describes "
     "it as $15 once. Those are different businesses and only one of them "
     "has recurring revenue.",
     "Decide, then make the product, the checkout and the financial model "
     "say the same thing. If it is one-time, the subscription line in the "
     "plan needs rebuilding.",
     "Nothing. This is a decision, not a test.",
     "S", 1.0, 1.0, "High", "Week 7"),
]

EXPERIMENTS = [
    dict(theme=t, name=n, hypothesis=h, change=c, metric=m, effort=e,
         low=lo, high=hi, confidence=conf, when=w)
    for t, n, h, c, m, e, lo, hi, conf, w in E
]


# -------------------------------------------------- the first ten minutes
# What the new user actually sees, screen by screen. The current product
# puts a five-question form here. This is the replacement.
FIRST_TEN = [
    ("0:00", "Sign up", "Phone number and an OTP. No email, no password, "
     "no profile. Every field here costs users and none of them is needed "
     "yet.", "15 seconds"),
    ("0:15", "Pick a field", "Twelve tiles: food, farming, delivery, "
     "education, health, fashion, crafts, tourism, services, retail, tech, "
     "other. One tap. No typing.", "10 seconds"),
    ("0:25", "One sentence", "'Tell us one problem you have seen in "
     "[field].' One box, one sentence, voice note allowed. Three real "
     "examples sit underneath it, and tapping one fills the box so it can "
     "be edited rather than written.", "60 seconds"),
    ("1:25", "The card", "The AI writes their problem back to them "
     "properly, in Arabic, on a card with their name on it. Share, save, "
     "or carry on. This is the first thing they own and it arrives before "
     "they have done any real work.", "15 seconds"),
    ("1:40", "One question back", "The AI asks one sharp question about "
     "their problem. Answering it completes mission 01. They are now a "
     "user who has finished something.", "90 seconds"),
    ("3:10", "The map", "Fifteen missions, where they are, what the end "
     "looks like, and what the certificate is. Shown once, after the first "
     "win rather than before it.", "20 seconds"),
    ("3:30", "The group", "'Twenty people started this week. Join them.' "
     "One tap into a WhatsApp group with a named host.", "15 seconds"),
    ("3:45", "The partner", "'Who are you building this with?' One invite, "
     "which is also the referral loop.", "30 seconds"),
]

# ---------------------------------------------------------------- nudges
# Drafts, in English, to be written properly in Egyptian Arabic. Every one
# names the user's own problem back to them, because a message that could
# have been sent to anybody gets read by nobody.
NUDGES = [
    ("+1 hour", "The card again",
     "Here is your problem card again, [name]. One question and mission 01 "
     "is done: [the AI's question]. Reply here and I will save it for you.",
     "Users who stopped before finishing mission 01"),
    ("Day 1", "The specific next step",
     "You said [their problem, quoted back]. The next step is to name who "
     "exactly it hurts. Two minutes: [link straight to the question they "
     "stopped on].",
     "Everybody who has not finished mission 02"),
    ("Day 3", "Somebody like them",
     "[Name] in [their governorate] started the same week as you and has "
     "finished three missions. Yours is waiting here: [deep link].",
     "Stalled for 48 hours"),
    ("Day 7", "The free tier ends well, not with a wall",
     "You have finished [n] of fifteen. Missions 01 to 03 gave you a "
     "problem worth solving. Here is what mission 04 does with it: "
     "[one line]. [link]",
     "Finished mission 03"),
    ("Day 14", "The deadline",
     "The [month] challenge closes Thursday. Finish mission [n] before "
     "then and your idea goes into the governorate showcase. [link]",
     "Any active user during a challenge week"),
    ("Day 30", "The sponsored seat",
     "[Partner] has funded 142 full seats this week. One is yours if you "
     "want it, and it expires Friday: [link].",
     "Lapsed 30 days"),
    ("On payment failure", "The thing nobody sends",
     "Your payment did not go through, and it is almost certainly the card "
     "rather than you. You can pay with Fawry at any kiosk with this code: "
     "[code], or with Vodafone Cash on [number].",
     "Every failed payment, within five minutes"),
]

# ------------------------------------------------------------- the maths
# Illustrative. Replace the 'now' column with the real numbers the moment
# the instrumentation in INSTRUMENTATION is live, which is the only reason
# week one of the plan exists.
FUNNEL = [
    ("Registered", 10_000, 10_000,
     "The denominator. Unchanged by any of this."),
    ("First action within 10 minutes", 0.30, 0.60,
     "Theme A. The ninety-second first action, the problem bank and the "
     "card."),
    ("Mission 01 completed", 0.55, 0.72,
     "Theme B. Two questions instead of five, an AI first draft, instant "
     "review."),
    ("Mission 03 completed", 0.40, 0.55,
     "Themes C and D. WhatsApp that names their own problem, a group of "
     "twenty, a deadline."),
    ("Reached the paywall", 0.85, 0.88,
     "Mostly mechanical once mission 03 is finished."),
    ("Started checkout", 0.12, 0.18,
     "Theme E. Paywall after mission 05, sold as a certificate and a "
     "stage rather than as twelve more lessons."),
    ("Payment succeeded", 0.45, 0.80,
     "Theme F, and the quietest number in the product. Fawry, Vodafone "
     "Cash, InstaPay and Meeza instead of a card most of the market does "
     "not have."),
]

FUNNEL_WARNING = (
    "Six improvements multiplied together is how a plan lies to the person "
    "who wrote it. Each target below is modest on its own and the compound "
    "is not: it takes paid conversion from well under one per cent to about "
    "three. Treat the compound as the direction, not the forecast. Half of "
    "it would still be the difference between a product that does not sell "
    "and one that does, and the two single largest contributors are the "
    "first row and the last, which are an onboarding screen and a payment "
    "method rather than anything to do with price.")

# ------------------------------------------------------------- the plan
PLAN = [
    ("Weeks 1-2", "Instrument, and change nothing else",
     "Step-level events on every question, cohort curves, and the four-step "
     "payment funnel with failures by method. Resist every temptation to "
     "ship a fix this fortnight. Shipping before measuring is how a team "
     "spends a quarter and cannot say whether it worked.",
     "The real version of the FUNNEL sheet"),
    ("Weeks 3-6", "Fix the first ten minutes",
     "Themes A and B together, because they are the same problem: the "
     "ninety-second first action, the problem bank, two questions in "
     "mission 01, the AI first draft, honest time labels, instant review.",
     "First action within 10 minutes, and mission 01 completion"),
    ("Weeks 5-8", "Make them come back",
     "Theme C and the first half of D. WhatsApp sequences, groups of "
     "twenty, weekly office hours. This runs over the top of the "
     "activation work rather than after it.",
     "Day 7 return rate, mission 03 completion"),
    ("Weeks 7-10", "Fix how they pay",
     "Theme F, which is engineering rather than experimentation. Price in "
     "pounds, add Fawry, Vodafone Cash, InstaPay and Meeza, and measure "
     "the failure rate of every method. Settle whether Pro is one-time or "
     "annual in week 7 and tell the financial model.",
     "Checkout start to payment success"),
    ("Weeks 9-12", "Then, and only then, touch the paywall and the price",
     "Theme E and the price ladder. By now the funnel above the paywall "
     "works, so a paywall test measures the paywall rather than measuring "
     "a broken product.",
     "Revenue per registered user"),
]

RULES = [
    ("One change at a time, above the paywall",
     "Activation changes interact. Ship them one at a time with a week "
     "between, or the quarter ends with six changes and no knowledge."),
    ("Measure revenue per registered user, not conversion rate",
     "A cheaper price always converts better. Only one of those two "
     "numbers pays salaries."),
    ("Never test a price before the funnel above it works",
     "A price test on a broken funnel measures the funnel."),
    ("A failed payment is not a lost sale yet",
     "Message them within five minutes with a Fawry code. This single "
     "message is usually worth more than any price experiment on this "
     "list."),
    ("Watch the users who finish, not the ones who sign up",
     "The cheapest acquisition channel is usually the worst, and a chart "
     "of signups by channel will tell you the opposite of the truth."),
    ("Nothing here replaces talking to twenty of them",
     "Call twenty users who stopped at mission 01 and ask what they were "
     "doing when they stopped. An afternoon of that is worth more than "
     "this entire file."),
]
