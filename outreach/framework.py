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
BUDGET_TOTAL, BUDGET_LINES = I.budget()
FOUNDERS, COHORTS = I.bought()


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
                 f"NGOs and development partners, and the youth foundations "
                 f"whose members fill the country's campuses, to carry one "
                 f"ambition together: that a first-time founder in Egypt "
                 f"should be given a method rather than a motivational "
                 f"speech."),
        ("p", "A young Egyptian with an idea today has two options. They can "
              "read, watch and guess, which is what almost all of them do, "
              "or they can win a place in an accelerator, which almost none "
              "of them will. Between those two there is nothing: no "
              "structured path from a problem worth solving to a first "
              "customer, in Arabic, that an ordinary student in Minya or "
              "Assiut can start on a Tuesday evening."),
        ("p", "StartPad is that path. Fifteen missions take a founder from a "
              "problem they have observed to a tested model, a prototype and "
              "a launch. Every submission is reviewed. The first three "
              "missions are free, for everyone, permanently. The rest is "
              "what sponsorship pays for."),
        ("h2", "What this document is"),
        ("p", "A framework, not a brochure. It sets out the three partner "
              "roles and what each gives and gets, the sponsorship tiers and "
              "the in-kind menu, the six-month plan for 2027 and why that "
              "window and not another, the arithmetic behind every number "
              "quoted, the rules that govern the ideas bank, and the "
              "governance a partner is signing into."),
        ("p", "It is written to be checked. Every figure in it is derived "
              "from a stated assumption with its driver written next to it, "
              "and none of them is a measured result, because the initiative "
              "has not run yet."),
        ("h2", f"Wave 1 at a glance"),
        ("kpi", [
            (n(F["People reached"]), "people reached"),
            (n(F["Registered founders"]), "first-time founders registered"),
            (n(F["Sponsored full journeys, all 15 missions"]),
             "through all 15 missions"),
            (n(F["Ideas in the bank"]), "ideas in the bank"),
        ]),
        ("kpi", [
            (n(F["Cohorts run"]), "in-person cohorts"),
            (n(F["Ventures trading at month 12"]), "ventures trading at "
                                                   "month 12"),
            (usd(BUDGET_TOTAL), f"budget at {I.TARGET_FILL:.0%} coalition "
                                f"fill"),
            ("6", f"months, {I.WAVE.split(', ')[1]}"),
        ]),
        ("note", f"<b>The million is not a six-month number, and this "
                 f"document will not pretend otherwise.</b> Wave 1 registers "
                 f"about {n(F['Registered founders'])} first-time founders. "
                 f"The million is crossed in the fourth wave, in 2029, on "
                 f"these rates, and Section 11 shows the whole path. A "
                 f"partner who signs believing the million arrives in August "
                 f"2027 becomes a problem at month six, so the number is "
                 f"stated plainly before anybody signs."),
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
        ("p", "Missions 01 to 03 are free to everybody in Egypt, forever, "
              "with no sponsor and no institution needed. That is "
              "deliberate: the free tier is how the initiative reaches a "
              "million people, and it is also the filter that tells us which "
              "of them are serious before anybody spends money on them."),
        ("h2", "The three layers"),
        ("deflist", [
            ("The platform, for everyone",
             "The fifteen missions, the tool library, the review, and the "
             "progress record. Arabic first. Works on a phone, because that "
             "is what the participant has."),
            ("The cohort, for those a sponsor pays for",
             "Six days in a room with a certified facilitator, missions "
             "every evening, and a showcase at the end. This is the part "
             "that changes completion rates, and it is the part that costs "
             "money."),
            ("The community, for everyone",
             "Chapters on campuses, ambassadors in governorates, and Mission "
             "Zero, the founder podcast, which is how a student in a city "
             "with no startup scene finds out that any of this exists."),
        ]),
        ("h2", "What the institution or sponsor receives"),
        ("p", "A cohort report: every participant named, what they built, "
              "what they completed, the facilitator's assessment and the "
              "showcase result. It is the artefact the buyer keeps, and in "
              "practice it closes more conversations than any description of "
              "the platform does."),
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
            "member, up to ten certified facilitators, its own data, its "
            "name on the national map, and places at the showcase.",
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
        ("lead", "Four cash tiers, an in-kind route into any of them, and a "
                 "charter for community supporters. Slots are capped, "
                 "because a tier anybody can buy is not worth buying, and a "
                 "coalition of forty equal logos gives nobody a reason to be "
                 "first."),
        ("table",
         ["Tier", "USD", "EGP", "Slots", "What it buys"],
         [[t["name"],
           usd(t["price"]) if t["price"] else "No cash",
           egp(t["price"]) if t["price"] else "",
           str(t["slots"]) if t["slots"] else "Uncapped",
           (f"{n(t['founders'])} founders through all 15 missions"
            + (f", and {t['cohorts']} in-person cohorts"
               if t["cohorts"] else "")) if t["price"] else t["gives"]]
          for t in I.TIERS],
         [2.8, 1.8, 2.4, 1.3, 8.3]),
        ("p", f"Every price above is the sum of what it buys, at "
              f"{usd(I.SEAT_PRICE, 2)} a sponsored founder and "
              f"{usd(I.COHORT_PRICE)} an in-person cohort of "
              f"{I.COHORT_SEATS}. There is no overhead percentage hidden "
              f"in it: the shared costs sit inside those two unit "
              f"prices and are the lines in the budget table in "
              f"Section 11."),
        ("p", f"Full coalition value if every capped slot sells is "
              f"{usd(I.target_money())}, which is "
              f"{egp(I.target_money())}. The wave is planned and budgeted "
              f"at {I.TARGET_FILL:.0%} of that, which is "
              f"{usd(BUDGET_TOTAL)} or {egp(BUDGET_TOTAL)}, and every "
              f"number in this document is quoted at that fill rather than "
              f"at the optimistic one."),
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
        ("note", "The four highest-value items on this list are reach, "
                 "venues, connectivity and company formation. Reach because "
                 "it is the initiative's scarcest input; venues because "
                 "every cohort needs a room for six days and a sponsor with "
                 "branches in nine governorates solves delivery in nine "
                 "governorates; connectivity because it is the difference "
                 "between a registered account and a completed mission in a "
                 "low-income governorate; and company formation because "
                 "registration is the step most first-time founders stall "
                 "on, after everything else has gone right."),
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
        ("p", "Because a six-month wave ends while the coalition still "
              "remembers why it joined, produces a closing report inside one "
              "reporting year, and lets a partner decide about the next wave "
              "on evidence rather than on faith. The wave is designed to be "
              "extended, not repeated from scratch: the facilitator pool, "
              "the chapters and the content all persist, which is why the "
              "second wave costs less per founder than the first."),
        ("h2", "Before the wave"),
        ("table",
         ["When", "What happens", "Why it is there"],
         [[when, what, why] for when, what, why in I.PRE_WAVE],
         [2.6, 3.6, 10.4]),
        ("h2", "The wave"),
        ("table",
         ["Month", "What it is", "What happens", "By month end"],
         [[f"{label}\n{when}", title, body,
           f"{n(F['Registered founders'] * reg)} registered"
           + (f"\n{n(F['Cohorts run'] * coh)} cohorts"
              if F["Cohorts run"] * coh >= 1 else "")]
          for label, when, title, body, reg, coh in I.MONTHS],
         [1.9, 2.3, 9.4, 3.0]),
        ("note", "<b>Month three is planned as an online month.</b> "
                 "Egyptian university exams run through May and into "
                 "mid-June. Campus activity stops whether or not a "
                 "programme plans for it, so the wave moves to the NGO "
                 "networks, the youth centres and online delivery, and the "
                 "mid-wave report is written in the month when nobody is "
                 "available to be trained anyway."),
    ]),

    ("The arithmetic", [
        ("lead", "Every number quoted in this document is built from the "
                 "coalition rather than asserted. This section shows the "
                 "construction so a partner can disagree with an assumption "
                 "rather than with a conclusion."),
        ("h2", "Where the reach comes from"),
        ("table",
         ["Channel", "Partners", "Reach each", "Register", "Why"],
         [[label, n(num), n(per), f"{rate:.0%}", why]
          for label, num, per, rate, why in I.CHANNELS]
         + [["Total", "", n(I.reach()), f"{I.registered()/I.reach():.0%}",
             "Weighted by channel, not assumed."]],
         [3.0, 1.8, 2.2, 1.8, 7.8]),
        ("h2", "The funnel"),
        ("table",
         ["Stage", "Wave 1", "What it means"],
         [[label, n(value), why] for label, value, why in I.funnel()],
         [4.2, 2.0, 10.4]),
        ("h2", "The conversion rates, and why each one"),
        ("table",
         ["Rate", "Assumed", "Why"],
         [[label, f"{value:.0%}", why] for label, value, why in I.RATES],
         [4.6, 2.0, 10.0]),
        ("h2", "What it costs, and what it buys"),
        ("p", f"The whole wave, at {I.TARGET_FILL:.0%} coalition fill. "
              f"Programme management is the balancing line rather than a "
              f"guess: every other line is a real quantity at a real "
              f"price, and if the sponsorship raised moves, the thing that "
              f"flexes is how much coordination the wave can afford, not "
              f"how many founders it serves."),
        ("table",
         ["Budget line", "USD", "EGP", "Share"],
         [[label, usd(value), egp(value), f"{value / BUDGET_TOTAL:.0%}"]
          for label, value, _ in BUDGET_LINES]
         + [["Total", usd(BUDGET_TOTAL), egp(BUDGET_TOTAL), "100%"]],
         [7.6, 2.6, 3.4, 1.6]),
        ("p", f"The two unit prices this rests on are not invented for "
              f"this document. {usd(I.SEAT_PRICE, 2)} a sponsored founder "
              f"is the national initiative seat price in the company's "
              f"financial model, year one, described there as priced for a "
              f"ministry buying tens of thousands. "
              f"{usd(I.COHORT_PRICE)} for an in-person cohort of "
              f"{I.COHORT_SEATS} is the model's own direct cost of $1,770 "
              f"plus the field, which Section 12 itemises."),
        ("h2", "Cost per outcome"),
        ("p", "The numbers a partner's finance function will ask for, and "
              "the ones most programmes cannot produce."),
        ("table",
         ["Measure", "USD", "EGP"],
         [[label, usd(value, 2), f"{I.egp(value):,.2f}"]
          for label, value in I.unit_costs()],
         [9.6, 3.0, 4.0]),
        ("note", f"<b>The sponsored founder and the in-person seat are "
                 f"prices, not averages.</b> They are what a partner pays "
                 f"and what the wave spends, and they are equal because "
                 f"the wave takes no margin: the surplus on the budget "
                 f"above is nil by design. StartPad's own return is "
                 f"elsewhere, and Section 14 sets it out rather than "
                 f"leaving a partner to wonder about it."),
        ("h2", "And when is the million"),
        ("table",
         ["Wave", "When", "Where", "What it adds"],
         [[wave, when, where, why]
          for wave, when, where, why in I.PATH_TO_MILLION],
         [1.8, 3.4, 3.4, 8.0]),
        ("p", "Anything faster than this needs either a national initiative "
              "that mandates participation across the university and "
              "technical education systems, or a step change in "
              "sponsorship. Both are possible. Neither is assumed here."),
    ]),

    ("Operations in the field", [
        ("lead", "A budget written in Cairo for a programme that runs in "
                 "Qena is wrong in one predictable way: it leaves out the "
                 "cost of getting there. This section is that cost, stated "
                 "in full, because it is the difference between a "
                 "governorate programme that happens and one that is "
                 "announced."),
        ("h2", f"What an in-person cohort actually costs"),
        ("table",
         ["Line", "USD", "EGP", "Field", "Note"],
         [[label, usd(value), f"{I.egp(value):,.0f}",
           "Yes" if label in I.FIELD_LINES else "", note]
          for label, value, note in I.COHORT_BREAKDOWN]
         + [["Total", usd(I.COHORT_PRICE), f"{I.egp(I.COHORT_PRICE):,.0f}",
             "", f"{I.COHORT_SEATS} seats, six delivery days"]],
         [5.4, 1.8, 2.0, 1.2, 6.2]),
        ("kpi", [
            (usd(I.field_cost()), "field cost in every cohort"),
            (f"{I.field_cost() / I.COHORT_PRICE:.0%}",
             "of the cohort price"),
            (usd(COHORTS * I.field_cost()),
             f"across {n(COHORTS)} cohorts in the wave"),
            ("8", "days away for six delivery days"),
        ]),
        ("h2", "The rules that make it work"),
        ("deflist", I.FIELD_POLICY),
        ("note", f"<b>The single highest-value thing a governorate partner "
                 f"can do is donate the room.</b> It takes $260 off every "
                 f"cohort, and that saving goes straight back into founders "
                 f"sponsored rather than into a surplus. A university, a "
                 f"corporate branch or a youth centre with a hall is worth "
                 f"more to this initiative in kind than most of them would "
                 f"write a cheque for."),
    ]),

    ("Every event in the wave", [
        ("lead", "The events are not decoration. They are how 150 chapters "
                 "activate in the same week, how twelve governorates get "
                 "opened, and how a wave ends with something a partner can "
                 "photograph and report. This is every one of them, with "
                 "what it costs."),
        ("table",
         ["Event", "How many", "Each", "Total", "When"],
         [[label, n(count), usd(cost), usd(count * cost), when]
          for label, count, cost, when, _ in I.EVENTS]
         + [["Total", "", "", usd(I.events_total()), I.WAVE]],
         [5.0, 1.8, 1.8, 2.2, 5.8]),
        ("h2", "What each one is for"),
        ("deflist", [(label, why) for label, _, _, _, why in I.EVENTS]),
        ("p", f"That is {usd(I.events_total() / FOUNDERS, 2)} of every "
              f"sponsored founder's {usd(I.SEAT_PRICE, 2)}, and the second "
              f"largest line in the budget after delivery. It is also the "
              f"line most likely to be cut by somebody reading quickly, "
              f"which would be a mistake: a chapter that has been visited "
              f"activates, and a chapter that has only been emailed does "
              f"not."),
        ("note", f"<b>Beside these, every one of the {n(COHORTS)} cohorts "
                 f"ends with its own showcase</b> for its participants and "
                 f"its host institution, with the host's own students "
                 f"presenting. Those sit inside the "
                 f"{usd(I.COHORT_PRICE)} cohort cost rather than in the "
                 f"events line, which is why the events table does not "
                 f"list thirty showcases."),
    ]),

    ("What StartPad gets back", [
        ("lead", "A partner is entitled to ask what the company running "
                 "this gets out of it, and a framework that does not "
                 "answer invites the worst assumption. The answer is that "
                 "wave one takes no margin from sponsorship at all, and "
                 "the return is somewhere else."),
        ("h2", "No margin on the sponsorship"),
        ("p", f"The budget in Section 11 balances to nil. Every dollar "
              f"raised is spent on delivery, events, platform, content, "
              f"measurement and the coordination to run it. The programme "
              f"management line of {usd(dict((l, v) for l, v, _ in BUDGET_LINES)['Programme management and coordination'])} "
              f"pays for a programme manager, a field coordinator and "
              f"part-time admin at Egyptian salaries. It is cost recovery, "
              f"not profit."),
        ("h2", "What the company puts in that nobody pays for"),
        ("table",
         ["Line", "USD", "EGP", "What it is"],
         [[label, usd(value), f"{I.egp(value):,.0f}", note]
          for label, value, note in I.STARTPAD_INVESTMENT]
         + [["Total",
             usd(sum(v for _, v, _ in I.STARTPAD_INVESTMENT)),
             f"{I.egp(sum(v for _, v, _ in I.STARTPAD_INVESTMENT)):,.0f}",
             "Time and engineering, not recovered"]],
         [4.2, 1.8, 2.2, 8.4]),
        ("h2", "What comes back in the twelve months after the wave"),
        ("p", "Priced at the financial model's own prices, so a reader "
              "with both documents cannot find two different numbers for "
              "the same product."),
        ("table",
         ["Line", "USD", "How it is counted"],
         [[label, usd(value), note]
          for label, value, note in I.startpad_return()]
         + [["Total",
             usd(sum(v for _, v, _ in I.startpad_return())),
             "Twelve months after the wave closes"]],
         [5.6, 2.2, 8.8]),
        ("kpi", [
            (usd(sum(v for _, v, _ in I.STARTPAD_INVESTMENT)),
             "StartPad puts in"),
            (usd(sum(v for _, v, _ in I.startpad_return())),
             "comes back in 12 months"),
            (f"{sum(v for _, v, _ in I.startpad_return()) / sum(v for _, v, _ in I.STARTPAD_INVESTMENT):.1f}x",
             "on what the company put in"),
            ("0", "margin taken from sponsorship"),
        ]),
        ("h2", "And what is not in that number"),
        ("deflist", I.startpad_assets()),
        ("note", "<b>Why this is in a document sent to sponsors.</b> "
                 "Because a sponsor who discovers it later will assume the "
                 "worst version of it, and because the return being real "
                 "is what makes the initiative durable. A programme the "
                 "operator loses money on for six months is a campaign. A "
                 "programme that builds the operator's capability while it "
                 "serves the sponsor's purpose is an institution, and it "
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
            "A sample cohort report, and the template of the closing report "
            "they will receive.",
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
