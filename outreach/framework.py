"""
The initiative framework document.

Content only. Every number in it is computed in outreach/initiative.py and
pulled in here by name, so the document and the sponsor workbook cannot
disagree about the funnel, the budget or the month targets.

Block types, rendered by scripts/build_initiative_docx.py:

    ("h1", title)                 a numbered section, starts a page
    ("h2", title) / ("h3", title) headings inside a section
    ("lead", text)                the opening paragraph of a section
    ("p", text)                   body text, <b>bold</b> allowed
    ("bullets", [...])            unordered list
    ("numbers", [...])            ordered list
    ("deflist", [(term, body)])   term with a rule and a body
    ("table", heads, rows, widths)
    ("kpi", [(value, label)])     a row of figure tiles
    ("note", text)                a shaded aside
    ("quote", text)               a large pull quote
    ("pb",)                       page break before the next block
"""

from outreach import initiative as I
from startpad.missions import MISSIONS

F = dict((k, v) for k, v, _ in I.funnel())
BUDGET_TOTAL = I.budget_total()


def n(v, dp=0):
    return f"{v:,.{dp}f}"


def usd(v, dp=0):
    return f"${v:,.{dp}f}"


def egp(v):
    return f"EGP {I.egp(v):,.0f}"


TITLE = I.NAME
SUBTITLE = f"{I.STRAPLINE}  |  {I.WAVE}"

SECTIONS = [

    ("The initiative", [
        ("lead", f"{I.NAME} invites Egyptian corporates with a CSR budget, "
                 f"NGOs and development partners, and the youth "
                 f"foundations whose members fill the country's campuses, "
                 f"to fund one thing together: a method, free, in Arabic, "
                 f"in the hands of a million young Egyptians inside six "
                 f"months."),
        ("p", "A young Egyptian with an idea today has two options. They "
              "can read, watch and guess, which is what almost all of them "
              "do, or they can win a place in an accelerator, which almost "
              "none of them will. Between those two there is nothing: no "
              "structured path from a problem worth solving to a first "
              "customer that an ordinary student in Minya or Assiut can "
              "start on a Tuesday evening."),
        ("p", "StartPad is that path. Fifteen missions take a founder from "
              "a problem they have observed to a tested model, a prototype "
              "and a launch plan, with every submission reviewed. For this "
              "wave the whole thing is free to every participant, and the "
              "coalition pays for it."),
        ("h2", "What this document is"),
        ("p", "A framework, not a brochure. It sets out the three partner "
              "roles and what each gives and gets, three sponsorship "
              "tiers, how a million is actually reached, the budget in six "
              "lines, the six-month plan for 2027 and why that window, the "
              "rules that govern the ideas bank, and the governance a "
              "partner is signing into."),
        ("p", "It is written to be checked. Every figure is derived from a "
              "stated assumption with its driver written next to it, and "
              "none of them is a measured result, because the initiative "
              "has not run yet."),
        ("h2", "Wave 1 at a glance"),
        ("kpi", [
            (n(F["Registered entrepreneurs"]), "entrepreneurs registered"),
            (usd(BUDGET_TOTAL), "total cost of the wave"),
            (usd(BUDGET_TOTAL / F["Registered entrepreneurs"], 2),
             "per entrepreneur"),
            ("6", "months, March to August 2027"),
        ]),
        ("kpi", [
            (n(F["All 15 missions completed"]),
             "finish all fifteen missions"),
            (n(F["Ideas in the bank"]), "ideas in the bank"),
            ("$0", "of StartPad's own cash"),
            ("0", "paid in-person cohorts"),
        ]),
        ("h2", "The three things that make this possible"),
        ("deflist", [
            ("It is free, and it is online",
             "Every participant gets all fifteen missions for nothing. "
             "There are no paid cohorts in this wave. A cohort serves "
             "twenty-five people for three thousand dollars; a webinar "
             "serves twenty thousand for five hundred, and the platform "
             "serves everybody for the cost of the review."),
            ("It spreads rather than being bought",
             f"{n(I.seed_total())} registrations come from the partners' "
             f"own channels, the chapters and the ambassadors. The rest "
             f"comes from the referral loop built into the product. "
             f"Section 12 is that loop, and the viral coefficient of "
             f"{I.VIRAL_K:.2f} is the riskiest number in this document."),
            ("It is funded entirely by the coalition",
             "StartPad contributes the platform, the curriculum and its "
             "team's time, all of which it already pays for. It puts in no "
             "cash and takes no margin. Section 14 says what it gets "
             "instead, because a partner should not have to guess."),
        ]),
        ("note", f"<b>Offline happens where a partner wants it.</b> This "
                 f"wave runs no bootcamps of its own. It runs "
                 f"{n(I.WEBINARS)} live webinars in Arabic, and info "
                 f"sessions wherever a partner asks for one and hosts it "
                 f"in their own venue with their own people. The "
                 f"initiative supplies the kit and trains the host. Where "
                 f"those sessions happen, and how many, is a partner's "
                 f"recommendation rather than our plan."),
    ]),

    ("What a first-time founder actually gets", [
        ("lead", "The thing being sponsored is a method, not an event. This "
                 "section is what a participant does, because every partner "
                 "will be asked by somebody inside their own organisation "
                 "what the money bought."),
        ("h2", "Fifteen missions"),
        ("p", "A founder moves through fifteen missions in five phases: "
              "discovery, analysis, model, build and launch. Each mission "
              "asks a small number of hard questions, each one is submitted, "
              "and each submission is reviewed against a rubric rather than "
              "ticked off. A founder who finishes has a tested problem, a "
              "defined user, a business model, a prototype and a launch "
              "plan, and the evidence trail that produced each one."),
        ("p", "Missions 01 to 03 are free to everybody in Egypt forever, "
              "with or without this initiative. For the six months of the "
              "wave the other twelve are free too. That is what makes a "
              "million possible: nothing that asks for a payment on the "
              "first screen has ever spread in this market."),
        ("h2", "The three layers, all of them free"),
        ("deflist", [
            ("The platform, for everyone",
             "The fifteen missions, the tool library, the review and the "
             "progress record. Arabic first. Works on a phone, because "
             "that is what the participant has."),
            ("Live webinars, for everyone",
             f"{n(I.WEBINARS)} across the wave, one a week, in Arabic, "
             f"recorded and left on the platform. A partner's name sits on "
             f"the ones they fund. This is the layer that replaces the "
             f"bootcamp, and it reaches a thousand times as many people "
             f"for the same money."),
            ("Info sessions, where a partner hosts one",
             "An evening in a room, run by a trained host from the "
             "partner's own team or a chapter's leadership, using a kit we "
             "supply. We pay for the kit, not for the room. Where they "
             "happen and how many is the partner's call."),
            ("The community, for everyone",
             "Chapters on campuses, 1,000 ambassadors in the governorates, "
             "and Mission Zero, the founder podcast, which is how a "
             "student in a city with no startup scene finds out that any "
             "of this exists."),
        ]),
        ("h2", "What a partner receives"),
        ("p", "A dashboard they can see weekly with their own line in it, "
              "the quarterly direction report on what young Egyptians are "
              "building, and a closing report with completion rates, "
              "governorate and gender disaggregation and SDG mapping, "
              "written to go straight into their own annual report."),
    ]),

    ("The three roles", [
        ("lead", "Three kinds of organisation carry this initiative, and "
                 "they are asked for three different things. Conflating "
                 "them is the commonest way a coalition fails: a student "
                 "organisation asked for sponsorship goes quiet, and a "
                 "corporate asked only for reach never commits a budget."),
        ("table",
         ["Role", "Who", "What they give", "What they get"],
         [[name, r["who"], r["gives"], r["gets"]]
          for name, r in I.ROLES.items()],
         [2.4, 4.4, 4.6, 5.2]),
        ("h2", "Community supporters are never asked for money"),
        ("p", "This is written into the charter and it is not a courtesy. A "
              "student organisation's currency is its members, its chapters "
              "and its leadership's time, and all three are worth more to "
              "this initiative than any cheque it could write. Enactus "
              "Egypt, INJAZ, AIESEC, the Hult Prize chapters and the "
              "technical student branches bring the single highest "
              "converting channel in the whole plan, because the invitation "
              "arrives from somebody the student already knows."),
        ("h2", "Who is not asked to sponsor, and why"),
        ("deflist", [(cat, why) for cat, why in I.NOT_INVITED.items()]),
        ("p", "A ministry that lends its name, opens its institutions and "
              "counts the participants towards its own national target is "
              "worth considerably more than its budget, and asking it for "
              "money slows everything else down. The patron relationships "
              "are secured before the coalition is announced, in the "
              "pre-wave months set out in Section 10."),
    ]),

    ("Why a CSR sponsor joins", [
        ("lead", "A corporate CSR team is not short of good causes. It is "
                 "short of programmes that produce a number it can report, "
                 "an asset it still has afterwards, and a reason for its own "
                 "business to care. This section is the case, and the first "
                 "three items are the ones that are not available anywhere "
                 "else in Egypt."),
        ("deflist", I.VALUES["CSR sponsor"]),
        ("note", "<b>The direction report and the ideas bank are the "
                 "differentiator.</b> Any organisation can sponsor training. "
                 "Nobody in Egypt can currently tell a partner what hundreds "
                 "of thousands of young people are trying to build, by "
                 "sector and by governorate, because nobody has the sample. "
                 "A partner that has it can design its accelerator around "
                 "demand that already exists instead of guessing, which is "
                 "why that single benefit is usually worth more than the "
                 "sponsorship costs."),
    ]),

    ("Why an NGO or development partner joins", [
        ("lead", "An NGO is being asked for reach, staff time, venues and "
                 "beneficiary networks, and in most cases for no money at "
                 "all. What it gets back is capability it keeps, evidence it "
                 "can use with its own donors, and access to a room full of "
                 "corporate budgets."),
        ("deflist", I.VALUES["NGO and development partner"]),
        ("note", "<b>The transition nobody can evidence.</b> Productive "
                 "families grants, savings groups and vocational training "
                 "all stop at exactly the point where a business has to be "
                 "designed, and that is where the fifteen missions start. "
                 "An organisation that can show beneficiaries moving from a "
                 "grant to a trading business has the strongest sentence "
                 "available in its next proposal, and almost none of them "
                 "can write it today."),
    ]),

    ("Why a youth foundation joins", [
        ("lead", "A youth foundation or student organisation is asked for "
                 "its members, its chapters and ten of its leadership. It is "
                 "never asked for money. What it gets is a member benefit it "
                 "can name, a credential its leadership keeps, and a "
                 "national stage."),
        ("deflist", I.VALUES["Community supporter"]),
        ("h2", "The chapter charter"),
        ("p", "Each community supporter signs a one-page charter rather than "
              "a sponsorship agreement. It says what the chapter does, what "
              "it receives, that no money is asked for in either direction, "
              "and that it renews annually, because student leadership turns "
              "over every summer and a relationship that is not re-signed "
              "each year quietly stops existing."),
        ("bullets", [
            "<b>The chapter provides</b> a named lead, a host venue for at "
            "least two sessions in the wave, and the invitation to its own "
            "members.",
            "<b>The chapter receives</b> the full programme free for every "
            "member, up to ten of its leadership trained as hosts, its "
            "own data, its place on the national leaderboard, and places "
            "at the demo day.",
            "<b>Neither side pays the other.</b> If a chapter wants to raise "
            "its own sponsorship, the initiative will write to its prospects "
            "in support.",
        ]),
    ]),

    ("The ideas bank, and the rules that govern it", [
        ("lead", "The ideas bank is the asset the initiative leaves behind, "
                 "and it is the part that would be most damaging to get "
                 "wrong. A programme that harvests young people's ideas for "
                 "its sponsors is not a programme, it is an extraction, and "
                 "it would deserve to fail. These rules are published to "
                 "participants and written into every sponsorship "
                 "agreement."),
        ("deflist", I.IDEAS_BANK),
        ("quote", "The founder owns the idea. Sponsorship buys direction "
                  "and distribution, never ownership and never a right of "
                  "first refusal."),
    ]),

    ("Sponsorship packages", [
        ("lead", "Three cash tiers, an in-kind route into any of them, and "
                 "a charter for community supporters. Slots are capped, "
                 "because a tier anybody can buy is not worth buying, and "
                 "because a coalition of forty equal logos gives nobody a "
                 "reason to be first."),
        ("table",
         ["Tier", "USD", "EGP", "Slots", "Who it is for"],
         [[t["name"],
           usd(t["price"]) if t["price"] else "No cash",
           egp(t["price"]) if t["price"] else "",
           str(t["slots"]) if t["slots"] else "Uncapped",
           t["gives"]] for t in I.TIERS],
         [2.8, 1.8, 2.4, 1.3, 8.3]),
        ("p", f"The wave costs {usd(BUDGET_TOTAL)}, which is "
              f"{egp(BUDGET_TOTAL)}. The three cash tiers raise "
              f"{usd(I.target_money())} if every slot sells, so the "
              f"coalition can lose four or five conversations and still "
              f"fund everything in Section 11. There is no surplus at any "
              f"fill: anything above the budget goes to ambassadors and to "
              f"reach, not to a margin."),
        ("note", "<b>Nobody buys a number of participants.</b> Every "
                 "participant is free, so a tier is not a quantity of "
                 "people. It is a position in a national coalition, a set "
                 "of webinars under a partner's name, and first sight of "
                 "what a million young Egyptians are trying to build."),
    ] + [b for t in I.TIERS for b in [
        ("h2", f"{t['name']}"),
        ("p", f"<b>{usd(t['price']) if t['price'] else 'No cash'}</b>"
              f"{'  |  ' + egp(t['price']) if t['price'] else ''}"
              f"{'  |  ' + str(t['slots']) + ' slots' if t['slots'] else ''}"
              f"  |  {t['role']}"),
        ("bullets", t["benefits"]),
    ]]),

    ("In-kind support", [
        ("lead", "In-kind is valued at its market or rate card value and "
                 "credited at the cash tier it matches, with every benefit "
                 "of that tier. A broadcaster giving airtime worth "
                 "$75,000 is a Lead Partner. For a media owner, a venue "
                 "owner or a telco this is usually faster than a cash "
                 "approval, and for several of them it is the only "
                 "realistic route."),
        ("table",
         ["What we accept", "Who has it", "Why it matters", "Value"],
         [[what, who, why, val] for what, who, why, val in I.INKIND],
         [3.2, 3.4, 8.0, 2.0]),
        ("note", "<b>Reach is the one that decides whether this "
                 "works.</b> A telecom partner messaging its own "
                 "subscriber base, a bank putting a banner in its app, a "
                 "retailer mailing its customers: that is where the first "
                 "half of the million comes from, it costs the partner "
                 "almost nothing, and no amount of cash buys an equivalent "
                 "audience in Egypt. After reach, the three that matter "
                 "are connectivity, because a data bundle is the "
                 "difference between a registered account and a completed "
                 "mission in a low-income governorate; venues, because an "
                 "info session needs a room for an evening and a sponsor "
                 "with branches in nine governorates can host in nine "
                 "governorates; and company formation, because "
                 "registration is the step most first-time founders stall "
                 "on after everything else has gone right."),
    ]),

    ("The six months, and why this window", [
        ("lead", f"{I.WAVE}. The window is chosen around the Egyptian year "
                 f"rather than around a financial one, because the "
                 f"participants are students and the calendar decides what "
                 f"is possible."),
        ("h2", "Why not January"),
        ("p", "Ramadan falls in February and the first days of March 2027, "
              "with Eid al-Fitr in the first half of March. A wave launched "
              "in January loses its second month to a season in which no "
              "campus activity happens and no corporate approval moves. "
              "Launching immediately after Eid puts the first month into "
              "the strongest part of the spring term instead. Religious "
              "dates here are approximate and should be confirmed nearer "
              "the time."),
        ("h2", "Why six months and not twelve"),
        ("p", "Because a viral wave either fires in its first eight weeks "
              "or it does not, and twelve months of a loop that is not "
              "firing is twelve months of spending. Six months ends while "
              "the coalition still remembers why it joined, produces a "
              "closing report inside one reporting year, and lets a "
              "partner decide what comes next on evidence rather than on "
              "faith."),
        ("h2", "Before the wave"),
        ("table",
         ["When", "What happens", "Why it is there"],
         [[when, what, why] for when, what, why in I.PRE_WAVE],
         [2.6, 3.6, 10.4]),
        ("h2", "The wave"),
        ("table",
         ["Month", "What it is", "What happens", "Registered by month end"],
         [[f"{label}\n{when}", title, body,
           n(F["Registered entrepreneurs"] * reg)]
          for label, when, title, body, reg in I.MONTHS],
         [1.9, 2.3, 9.4, 3.0]),
        ("note", "<b>Month three is the one to plan for, not to hope "
                 "through.</b> Egyptian university exams run through May "
                 "and into mid-June, and campus activity stops whether or "
                 "not a programme expects it. The wave moves to the NGO "
                 "networks, the youth centres and partner-hosted info "
                 "sessions, runs its second challenge week in the "
                 "governorates, and writes the mid-wave report in the "
                 "month when nobody is on a campus anyway."),
    ]),

    ("The arithmetic", [
        ("lead", "Every number quoted in this document is built rather "
                 "than asserted. This section shows the construction, so a "
                 "partner can disagree with an assumption instead of with "
                 "a conclusion."),
        ("h2", "Where the first half million comes from"),
        ("table",
         ["Channel", "How many", "Each", "Registrations", "Why"],
         [[label, n(num), n(per), n(num * per), why]
          for label, num, per, why in I.SEED]
         + [["Total", "", "", n(I.seed_total()),
             "Before anybody shares anything."]],
         [3.0, 1.5, 1.5, 2.2, 8.4]),
        ("h2", "And where the other half comes from"),
        ("p", f"The referral loop in Section 12. At a viral coefficient of "
              f"{I.VIRAL_K:.2f}, every registered entrepreneur brings "
              f"{I.VIRAL_K:.2f} more across the wave, which multiplies the "
              f"seed by {1 / (1 - I.VIRAL_K):.2f} and gives "
              f"{n(F['Registered entrepreneurs'])} registered "
              f"entrepreneurs. That coefficient is the single number most "
              f"worth arguing about in this document, and Section 12 is "
              f"the argument for it."),
        ("h2", "The funnel"),
        ("table",
         ["Stage", "Wave 1", "What it means"],
         [[label, n(value), why] for label, value, why in I.funnel()],
         [4.2, 2.0, 10.4]),
        ("h2", "The rates, and why each one"),
        ("table",
         ["Rate", "Assumed", "Why"],
         [[label, f"{value:.0%}", why] for label, value, why in I.RATES],
         [4.6, 2.0, 10.0]),
        ("h2", "The budget, in six lines"),
        ("table",
         ["Line", "USD", "EGP", "Share"],
         [[label, usd(value), egp(value), f"{value / BUDGET_TOTAL:.0%}"]
          for label, value, _ in I.BUDGET]
         + [["Total", usd(BUDGET_TOTAL), egp(BUDGET_TOTAL), "100%"]],
         [7.6, 2.6, 3.4, 1.6]),
        ("p", "Six lines, because the wave does six things: it runs a "
              "platform, it makes content and webinars, it feeds a "
              "community of ambassadors and chapters, it holds events, it "
              "measures itself, and it is coordinated by four people. "
              "There is no seventh line and no contingency dressed up as "
              "one."),
        ("h2", "Cost per outcome"),
        ("table",
         ["Measure", "USD", "EGP"],
         [[label, usd(value, 2), f"{I.egp(value):,.2f}"]
          for label, value in I.unit_costs()],
         [9.6, 3.0, 4.0]),
        ("note", f"<b>Twenty cents a head.</b> That is not a number a "
                 f"corporate programme can reach on its own, and it is the "
                 f"whole argument for a coalition. The one to compare "
                 f"against anything else a partner funds is "
                 f"{usd(BUDGET_TOTAL / F['All 15 missions completed'], 2)} "
                 f"per entrepreneur who finishes all fifteen missions, "
                 f"because that is a person who took an idea to a tested "
                 f"model, a prototype and a launch plan."),
        ("h2", "And what comes after the million"),
        ("table",
         ["Wave", "When", "What it is", "What it adds"],
         [[wave, when, where, why]
          for wave, when, where, why in I.PATH_TO_MILLION],
         [2.2, 3.4, 3.4, 7.6]),
    ]),

    ("How it goes viral", [
        ("lead", f"A million people is not a budget line. Nobody on the "
                 f"invitation list has enough money to buy a million "
                 f"registrations in Egypt, and if they did the people "
                 f"bought would not finish anything. The million has to "
                 f"spread, and this section is how."),
        ("h2", "Half of it is seeded, half of it is referred"),
        ("p", f"{n(I.seed_total())} registrations come from the coalition "
              f"itself: a telecom partner messaging its own base, a bank "
              f"in its app, 150 chapters inviting their members, 1,000 "
              f"ambassadors with codes, eighteen NGO networks, and the "
              f"podcast. The other {n(F['Registered entrepreneurs'] - I.seed_total())} "
              f"come from the people already in."),
        ("kpi", [
            (n(I.seed_total()), "seeded by partners"),
            (f"{I.VIRAL_K:.2f}", "viral coefficient"),
            (f"{1 / (1 - I.VIRAL_K):.2f}x", "multiplier"),
            (n(F["Registered entrepreneurs"]), "registered"),
        ]),
        ("h2", "The nine mechanics"),
        ("deflist", I.VIRAL_LOOPS),
        ("note", "<b>The loop is in the product, not in a campaign.</b> "
                 "Mission 04 opens when a founder brings two others who "
                 "finish mission 01, and every mission finished generates "
                 "a card in Arabic designed to be posted. A referral "
                 "scheme bolted on at launch does not produce a "
                 "coefficient like this. One built into the thing itself "
                 "might, and the measurement starts in week one so the "
                 "coalition knows by April rather than by August."),
        ("h2", "What a partner has to commit to for this to work"),
        ("bullets", [
            "<b>A messaging calendar, agreed at signature.</b> Not when "
            "somebody gets round to it. One telecom push in week one is "
            "worth more than six months of organic traffic.",
            "<b>Their own channels, not just their logo.</b> The app "
            "banner, the SMS, the branch posters, the employee mail. This "
            "is the contribution that matters most and it costs the "
            "partner nothing.",
            "<b>Permission to name them.</b> A coalition that cannot be "
            "named cannot be shared, and the initiative spreads on being "
            "shared.",
        ]),
    ]),

    ("Everything that happens live", [
        ("lead", "There are no paid in-person cohorts in this wave. That "
                 "is the decision that makes a million affordable, and "
                 "this is what replaces them."),
        ("h2", "Events"),
        ("table",
         ["Event", "How many", "Each", "Total", "When"],
         [[label, n(count), usd(cost), usd(count * cost), when]
          for label, count, cost, when, _ in I.EVENTS]
         + [["Total", "", "", usd(I.events_total()), I.WAVE]],
         [5.0, 1.8, 1.8, 2.2, 5.8]),
        ("h2", "Live delivery and content"),
        ("table",
         ["Item", "How many", "Each", "Total", "When"],
         [[label, n(count), usd(cost), usd(count * cost), when]
          for label, count, cost, when, _ in I.DELIVERY]
         + [["Total", "", "", usd(I.delivery_total()), I.WAVE]],
         [5.0, 1.8, 1.8, 2.2, 5.8]),
        ("h2", "What each one is for"),
        ("deflist", [(label, why) for label, _, _, _, why in I.EVENTS]
                    + [(label, why)
                       for label, _, _, _, why in I.DELIVERY]),
        ("note", f"<b>Offline info sessions are the partners' to "
                 f"propose.</b> {n(I.INFO_SESSIONS)} of them are budgeted, "
                 f"at {usd(I.INFO_SESSION_KIT)} each, which pays for a kit "
                 f"and for training the host. The venue, the people and "
                 f"the catering come from whoever asks for the session. "
                 f"Three hundred of them together cost less than two "
                 f"in-person cohorts would have, and they reach a hundred "
                 f"times as many people."),
    ]),

    ("What StartPad gets back", [
        ("lead", "A partner is entitled to ask what the company running "
                 "this gets out of it, and a framework that does not "
                 "answer invites the worst assumption. The answer is that "
                 "StartPad puts in no cash and takes no margin, and the "
                 "return is somewhere else."),
        ("h2", "No cash in, no margin out"),
        ("p", f"The budget in Section 11 is {usd(BUDGET_TOTAL)} and the "
              f"coalition raises {usd(BUDGET_TOTAL)}. There is no line in "
              f"it for StartPad, no management fee beyond the four people "
              f"who run the programme at Egyptian salaries, and no "
              f"surplus at any level of fill. If the coalition raises more "
              f"than the budget, the extra goes to ambassadors and reach."),
        ("h2", "What the company contributes instead"),
        ("deflist", I.STARTPAD_CONTRIBUTION),
        ("h2", "What comes back in the twelve months after the wave"),
        ("p", "Priced at the financial model's own prices, so a reader "
              "with both documents cannot find two different numbers for "
              "the same product."),
        ("table",
         ["Line", "USD", "How it is counted"],
         [[label, usd(value), note]
          for label, value, note in I.startpad_return()]
         + [["Total", usd(sum(v for _, v, _ in I.startpad_return())),
             "Twelve months after the wave closes"]],
         [5.6, 2.2, 8.8]),
        ("kpi", [
            ("$0", "of StartPad cash in"),
            ("$0", "margin taken"),
            (usd(sum(v for _, v, _ in I.startpad_return())),
             "commercial revenue in the 12 months after"),
            (n(F["Registered entrepreneurs"]),
             "entrepreneurs the company now knows"),
        ]),
        ("h2", "And what is not in that number"),
        ("deflist", I.startpad_assets()),
        ("note", "<b>Why this is in a document sent to sponsors.</b> "
                 "Because a partner who discovers it later will assume the "
                 "worst version of it, and because the return being real "
                 "is what makes the initiative durable. A programme the "
                 "operator loses money on for six months is a campaign. A "
                 "programme that builds the operator's capability while it "
                 "serves the partners' purpose is an institution, and it "
                 "will still be running in 2029."),
    ]),

    ("Governance, measurement and risk", [
        ("lead", "A coalition of twenty organisations needs to know who "
                 "decides what, who is accountable when something fails, "
                 "and what it will be told and when. This section is what a "
                 "partner is signing into."),
        ("h2", "Who decides what"),
        ("deflist", I.GOVERNANCE),
        ("h2", "What gets measured, and when partners see it"),
        ("table",
         ["What", "How often", "Where", "Detail"],
         [[what, often, where, detail]
          for what, often, where, detail in I.MEASUREMENT],
         [3.0, 2.2, 2.4, 9.0]),
        ("h2", "What could go wrong"),
        ("table",
         ["Risk", "How it is handled", "Status"],
         [[risk, how, status] for risk, how, status in I.RISKS],
         [3.8, 10.4, 2.4]),
        ("note", "<b>The risk that ends the initiative is a safeguarding "
                 "failure involving a minor.</b> It is handled with a named "
                 "lead, a written policy, vetting for everyone who works "
                 "with under-18s, no identified data on under-18s under any "
                 "sponsorship tier, and a reporting route that reaches the "
                 "steering committee in the same week. A partner should ask "
                 "to see the policy before signing, and will be given it."),
    ]),

    ("How to join", [
        ("lead", "Four steps, two weeks for a corporate, longer for a "
                 "foundation board. The first step is twenty minutes and "
                 "does not involve a deck."),
        ("numbers", [f"<b>{title}</b>  {body}" for title, body in I.JOIN]),
        ("h2", "What a partner should ask for before signing"),
        ("bullets", [
            "The safeguarding policy and the name of the safeguarding lead.",
            "The data protection policy, the consent text participants see, "
            "and the ideas bank rules in Section 7.",
            "The dashboard they will see weekly, and the template of the "
            "closing report they will receive.",
            "The current coalition: who has signed, at what tier, and which "
            "governorates and sectors are already taken.",
            "The assumptions behind Section 11, which are in the workbook "
            "that accompanies this document and are editable.",
        ]),
        ("h2", "What the initiative will ask them for"),
        ("bullets", [
            "A named counterpart who can make a decision, not only relay "
            "one.",
            "Their own reporting requirements, in writing, before the wave "
            "starts rather than at month five.",
            "Their governorate or sector preference, so the coalition can "
            "be assembled without two partners claiming the same ground.",
            "For in-kind partners, the rate card or market value they want "
            "the contribution credited at.",
        ]),
        ("quote", "Three Founding Partners, and the rest of the coalition "
                  "sells itself. That is the whole critical path."),
    ]),

    ("Appendix: the fifteen missions", [
        ("lead", "What a participant actually does, in order. Missions 01 "
                 "to 03 are free to everybody in Egypt."),
        ("table",
         ["#", "Mission", "Phase", "Time", "What it produces"],
         [[f"{m['id']:02d}", m["title"], m["phase"], m["time"], m["summary"]]
          for m in MISSIONS],
         [1.0, 3.6, 2.2, 1.8, 8.0]),
    ]),
]
