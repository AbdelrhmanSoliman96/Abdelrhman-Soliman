const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, PageBreak,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, LevelFormat,
  TableOfContents, Footer, PageNumber, convertInchesToTwip
} = require("docx");
const fs = require("fs");

const NAVY = "10243E";
const TEAL = "0E7C6B";
const GREY = "5A6472";
const RULE = "C7CED6";
const WASH = "EDF1F5";
const AMBER = "9A5B00";
const CRIT = "A32338";

const CW = 9026; // content width in DXA (A4 minus 1" margins)

// ---------- helpers ----------
const P = (text, opts = {}) =>
  new Paragraph({
    spacing: { before: opts.before ?? 0, after: opts.after ?? 120, line: 276 },
    alignment: opts.align,
    indent: opts.indent,
    border: opts.border,
    children: [new TextRun({
      text, bold: opts.bold, italics: opts.italics, size: opts.size ?? 21,
      color: opts.color ?? "1A1A1A", font: "Calibri"
    })]
  });

const RichP = (runs, opts = {}) =>
  new Paragraph({
    spacing: { before: opts.before ?? 0, after: opts.after ?? 120, line: 276 },
    alignment: opts.align,
    indent: opts.indent,
    children: runs.map(r => new TextRun({
      text: r.t, bold: r.b, italics: r.i, size: r.size ?? 21,
      color: r.c ?? "1A1A1A", font: "Calibri"
    }))
  });

const Bullet = (text, opts = {}) =>
  new Paragraph({
    numbering: { reference: "bullets", level: opts.level ?? 0 },
    spacing: { after: 90, line: 276 },
    children: [new TextRun({ text, size: 21, color: "1A1A1A", font: "Calibri" })]
  });

const RichBullet = (runs, opts = {}) =>
  new Paragraph({
    numbering: { reference: "bullets", level: opts.level ?? 0 },
    spacing: { after: 90, line: 276 },
    children: runs.map(r => new TextRun({
      text: r.t, bold: r.b, italics: r.i, size: 21, color: r.c ?? "1A1A1A", font: "Calibri"
    }))
  });

const H1 = (text) => new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 180 } });
const H2 = (text) => new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 140 } });
const H3 = (text) => new Paragraph({ text, heading: HeadingLevel.HEADING_3, spacing: { before: 220, after: 110 } });

const cell = (content, o = {}) => new TableCell({
  width: { size: o.w, type: WidthType.DXA },
  shading: o.fill ? { type: ShadingType.CLEAR, color: "auto", fill: o.fill } : undefined,
  margins: { top: 90, bottom: 90, left: 120, right: 120 },
  verticalAlign: "top",
  children: (Array.isArray(content) ? content : [content]).map(t =>
    new Paragraph({
      spacing: { after: 0, line: 260 },
      alignment: o.align,
      children: [new TextRun({
        text: t, bold: o.bold, size: o.size ?? 19,
        color: o.color ?? (o.head ? "FFFFFF" : "1A1A1A"), font: "Calibri"
      })]
    })
  )
});

const table = (widths, rows) => new Table({
  columnWidths: widths,
  width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
  borders: {
    top: { style: BorderStyle.SINGLE, size: 2, color: RULE },
    bottom: { style: BorderStyle.SINGLE, size: 2, color: RULE },
    left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
    right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
    insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: RULE },
    insideVertical: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }
  },
  rows
});

const headRow = (widths, labels) => new TableRow({
  tableHeader: true,
  children: labels.map((l, i) => cell(l, { w: widths[i], fill: NAVY, head: true, bold: true, size: 18 }))
});

const spacer = (h = 120) => new Paragraph({ spacing: { after: h }, children: [] });

const rule = () => new Paragraph({
  spacing: { before: 60, after: 200 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: TEAL } },
  children: []
});

const calloutBox = (title, body, accent = TEAL) => table([CW], [
  new TableRow({
    children: [new TableCell({
      width: { size: CW, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, color: "auto", fill: WASH },
      margins: { top: 160, bottom: 160, left: 200, right: 200 },
      borders: { left: { style: BorderStyle.SINGLE, size: 18, color: accent } },
      children: [
        new Paragraph({
          spacing: { after: 80 },
          children: [new TextRun({ text: title, bold: true, size: 21, color: NAVY, font: "Calibri" })]
        }),
        ...body.map(b => new Paragraph({
          spacing: { after: 60, line: 270 },
          children: [new TextRun({ text: b, size: 20, color: "1A1A1A", font: "Calibri" })]
        }))
      ]
    })]
  })
]);

// ---------- document ----------
const doc = new Document({
  creator: "AngelSta",
  title: "Competitive Analysis — Finstreet",
  description: "Competitive analysis of Finstreet and gap analysis versus AngelSta",
  styles: {
    default: {
      document: { run: { font: "Calibri", size: 21, color: "1A1A1A" } }
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, color: NAVY, font: "Calibri" },
        paragraph: { spacing: { before: 360, after: 160 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, color: TEAL, font: "Calibri" },
        paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 1 }
      },
      {
        id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 21, bold: true, color: NAVY, font: "Calibri" },
        paragraph: { spacing: { before: 220, after: 100 }, outlineLevel: 2 }
      }
    ]
  },
  numbering: {
    config: [{
      reference: "bullets",
      levels: [
        {
          level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 360, hanging: 200 } } }
        },
        {
          level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 200 } } }
        }
      ]
    }]
  },
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [
            new TextRun({ text: "Competitive Analysis — Finstreet  |  ", size: 16, color: GREY, font: "Calibri" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GREY, font: "Calibri" })
          ]
        })]
      })
    },
    children: [
      // ===================== COVER =====================
      spacer(1600),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "COMPETITIVE ANALYSIS", bold: true, size: 20, color: TEAL, font: "Calibri", characterSpacing: 60 })]
      }),
      new Paragraph({
        spacing: { after: 100 },
        children: [new TextRun({ text: "Finstreet", bold: true, size: 68, color: NAVY, font: "Calibri" })]
      }),
      new Paragraph({
        spacing: { after: 400 },
        children: [new TextRun({
          text: "Market position, regulatory perimeter, and gap analysis versus AngelSta",
          size: 26, color: GREY, font: "Calibri"
        })]
      }),
      rule(),
      table([2200, 6826], [
        new TableRow({ children: [
          cell("Subject", { w: 2200, bold: true, color: GREY, size: 18 }),
          cell("Finstreet Limited (finstreet.ae) — Abu Dhabi, UAE", { w: 6826, size: 19 })
        ]}),
        new TableRow({ children: [
          cell("Prepared for", { w: 2200, bold: true, color: GREY, size: 18 }),
          cell("AngelSta — MENA investor platform", { w: 6826, size: 19 })
        ]}),
        new TableRow({ children: [
          cell("Date", { w: 2200, bold: true, color: GREY, size: 18 }),
          cell("August 2026", { w: 6826, size: 19 })
        ]}),
        new TableRow({ children: [
          cell("Classification", { w: 2200, bold: true, color: GREY, size: 18 }),
          cell("Internal — competitive intelligence", { w: 6826, size: 19 })
        ]}),
        new TableRow({ children: [
          cell("Headline finding", { w: 2200, bold: true, color: GREY, size: 18 }),
          cell("Adjacent infrastructure operator, not a direct competitor — but the single most important company for AngelSta to understand", { w: 6826, size: 19, bold: true, color: NAVY })
        ]})
      ]),

      new Paragraph({ children: [new PageBreak()] }),

      // ===================== CONTENTS =====================
      H1("Contents"),
      new TableOfContents("Contents", { hyperlink: true, headingStyleRange: "1-2" }),
      new Paragraph({ children: [new PageBreak()] }),

      // ===================== 1. EXEC SUMMARY =====================
      H1("1. Executive summary"),

      P("Finstreet and AngelSta both describe themselves in the language of MENA private capital markets. They are not, on current evidence, competing for the same customer, the same transaction, or the same regulatory permission. Reading Finstreet as a head-on competitor would lead to the wrong strategy.", { after: 160 }),

      P("Finstreet is regulated financial market infrastructure. It operates a multilateral trading facility, a central securities depository, a digital settlement facility and a private financing platform under eight licences from the Financial Services Regulatory Authority in Abu Dhabi Global Market. Its customers are professional clients — sovereign wealth funds, large family offices and institutional asset managers. Its market thesis is secondary liquidity: an estimated US$600 billion of private assets across Asia, Europe and the Middle East seeking exits. It is owned by Rorix Holdings, part of International Holding Company, the most valuable listed holding company in the Middle East.", { after: 160 }),

      P("AngelSta is a pre-launch investor platform for angels and high-net-worth individuals, with a regulatory application in progress and a seed round being raised. Its market is primary capital formation — getting money into MENA companies at the earliest stage — and its constraint is deal origination and investor trust, not settlement infrastructure.", { after: 200 }),

      calloutBox("The core distinction", [
        "Finstreet is building the plumbing for institutions to trade large private assets that already exist.",
        "AngelSta is building the front door for individuals to fund companies that do not yet exist at scale.",
        "These share vocabulary, geography and a regulator. They do not share a customer, a ticket size, or a transaction type."
      ]),

      spacer(200),

      H2("What this means strategically"),

      RichBullet([
        { t: "Threat level today: low-to-moderate. ", b: true },
        { t: "Finstreet's professional-client permissions structurally prevent it from serving most of AngelSta's target investors without new authorisations. The segments are separated by regulation, not just by choice." }
      ]),
      RichBullet([
        { t: "Threat level over three to five years: material. ", b: true },
        { t: "The top of AngelSta's HNW segment overlaps with the bottom of Finstreet's professional-client definition. If that band proves valuable, Finstreet's parent has effectively unlimited capital to pursue it." }
      ]),
      RichBullet([
        { t: "The most valuable read is not competitive at all. ", b: true },
        { t: "Finstreet owns rails — custody, settlement, depository — that AngelSta will eventually need and should never build. This is a credible partnership or integration vector, and it is worth exploring before it is foreclosed by a competitor." }
      ]),
      RichBullet([
        { t: "The urgent gap is regulatory, and it is on the critical path. ", b: true },
        { t: "Finstreet holds eight licences; AngelSta holds an application. In a seed round targeting MENA capital markets, time-to-licence is the question investors will press hardest, and Finstreet is the benchmark they will measure against." }
      ]),

      new Paragraph({ children: [new PageBreak()] }),

      // ===================== 2. METHOD =====================
      H1("2. Method and evidence base"),

      P("This analysis was compiled from regulatory filings, company announcements, and press coverage. One material limitation should be stated plainly at the outset.", { after: 140 }),

      calloutBox("Research limitation", [
        "The finstreet.ae website could not be retrieved directly — the domain is blocked by the network egress policy of the research environment used for this analysis. The same applies to angelsta.net.",
        "The Finstreet profile below is therefore built from primary regulatory sources (ADGM/FSRA public registers), company and exchange announcements, and named-source press interviews. These are in several respects more reliable than marketing copy, but they will not capture current website positioning, pricing, or any product launched without an announcement.",
        "Recommendation: have someone with unrestricted access capture finstreet.ae in full — every page, pricing, onboarding flow, and terms — and re-run Section 6 against it. That pass would materially sharpen the product-level gaps."
      ], AMBER),

      spacer(180),

      P("Confidence is marked throughout as follows:", { after: 120 }),
      table([1600, 7426], [
        headRow([1600, 7426], ["Confidence", "Basis"]),
        new TableRow({ children: [
          cell("High", { w: 1600, bold: true, color: TEAL }),
          cell("Regulatory register entries, official announcements, or direct quotation from a named executive.", { w: 7426 })
        ]}),
        new TableRow({ children: [
          cell("Medium", { w: 1600, bold: true, color: NAVY }),
          cell("Consistent reporting across multiple independent outlets, without a primary source seen directly.", { w: 7426 })
        ]}),
        new TableRow({ children: [
          cell("Inferred", { w: 1600, bold: true, color: AMBER }),
          cell("Analytical judgement drawn from the above. Reasoning is given so it can be challenged.", { w: 7426 })
        ]})
      ]),

      spacer(160),
      P("The AngelSta side of the comparison reflects positions confirmed by the AngelSta team in August 2026: regulatory application in progress, target investors are angels and high-net-worth individuals, and the company is pre-launch and raising a seed round. Public signals — the issuer application route and a capped cohort of 500 investor seats — are noted where relevant and marked as such.", { after: 120 }),

      new Paragraph({ children: [new PageBreak()] }),

      // ===================== 3. FINSTREET PROFILE =====================
      H1("3. Finstreet: company profile"),

      H2("3.1 Corporate structure and ownership"),
      P("Finstreet Limited is an operating company of Rorix Holdings, which sits within International Holding Company (IHC). Confidence: high.", { after: 140 }),
      P("IHC is the largest listed holding company in the Middle East by market capitalisation, reported at AED 892.8 billion as of 30 September 2024. It was founded in 1998 as part of a UAE initiative to diversify into non-oil sectors, and is chaired by Sheikh Tahnoon bin Zayed Al Nahyan. Confidence: high.", { after: 140 }),
      P("The practical consequence is that Finstreet is not a venture-funded startup in any meaningful competitive sense. It is a strategic infrastructure initiative of a sovereign-adjacent holding company, with the balance sheet, political access and time horizon that implies. Finstreet's own funding has not been publicly disclosed, and given the ownership structure it may never be a meaningful figure. Confidence: inferred.", { after: 140 }),

      H2("3.2 Leadership"),
      P("Sunidhi Pasan is co-founder and Group Chief Executive Officer. Pasan speaks for the company publicly, including a February 2026 interview with Semafor and an appearance at the Milken Institute Global Conference 2025. Confidence: high.", { after: 140 }),

      H2("3.3 Regulatory perimeter"),
      P("This is the most important section of the profile, and the dimension on which Finstreet is furthest ahead of any early-stage entrant. Finstreet secured eight licences to operate within ADGM, structured across three regulated entities supervised by the FSRA. Confidence: high.", { after: 160 }),

      table([2500, 3626, 2900], [
        headRow([2500, 3626, 2900], ["Regulated entity", "Function", "What it enables"]),
        new TableRow({ children: [
          cell("Finstreet Global Markets Ltd", { w: 2500, bold: true, color: NAVY }),
          cell("Multilateral Trading Facility (MTF). Secondary market trading venue for professional clients, including securities primary-listed on other exchanges.", { w: 3626 }),
          cell("Operating an order book. Matching buyers and sellers of private and public securities as a venue, not as a broker.", { w: 2900 })
        ]}),
        new TableRow({ children: [
          cell("Finstreet Capital Ltd", { w: 2500, bold: true, color: NAVY, fill: WASH }),
          cell("Advisory and Private Financing Platform (PFP).", { w: 3626, fill: WASH }),
          cell("Arranging and advising on deals; running a primary private-capital raising channel.", { w: 2900, fill: WASH })
        ]}),
        new TableRow({ children: [
          cell("Finstreet Global Clearing and Settlement Ltd", { w: 2500, bold: true, color: NAVY }),
          cell("Central Securities Depository (CSD), international custodian, and Digital Settlement Facility (DSF).", { w: 3626 }),
          cell("Holding assets, recording ownership, and settling trades — including tokenised instruments.", { w: 2900 })
        ]})
      ]),

      spacer(160),
      P("Two things about this structure deserve emphasis. First, holding the venue, the depository and the settlement layer together is unusual — most participants own one, not all three. Finstreet can therefore close the full lifecycle of a private-asset transaction inside its own perimeter. Second, an MTF authorisation for professional clients is a specific and constrained permission. It is not a licence to serve retail investors, and extending into that segment would require different authorisations, different disclosure obligations, and different conduct rules. Confidence: high on the first point, inferred on the second.", { after: 140 }),

      H2("3.4 Product architecture"),
      P("Finstreet describes a suite spanning four functions, launched at Abu Dhabi Finance Week and positioned as the first regulated digital venue of its kind for trading both private and public securities. Confidence: high.", { after: 140 }),
      Bullet("Multilateral Trading Facility — the trading venue itself, for professional clients."),
      Bullet("Central Securities Depository — record of ownership and asset servicing."),
      Bullet("Digital Settlement Facility — settlement, including for tokenised instruments."),
      Bullet("Private Financing Platform — primary capital raising."),
      spacer(80),
      P("Together these are pitched as bridging primary and secondary markets, giving private company shareholders liquidity options and opening alternative investments to professional investors. Confidence: high.", { after: 140 }),

      H2("3.5 Technology approach"),
      P("Finstreet operates a hybrid model, combining conventional market infrastructure with blockchain-based components, and tokenisation is central to its external positioning. The stated framing is regulated tokenisation — combining tokenised instruments with investor protection — rather than tokenisation as a route around regulation. Confidence: high.", { after: 140 }),

      H2("3.6 Partnerships and alliances"),
      P("The partner roster is the clearest signal of Finstreet's intended altitude. Confidence: high.", { after: 140 }),
      table([2600, 6426], [
        headRow([2600, 6426], ["Counterparty", "Nature of relationship"]),
        new TableRow({ children: [
          cell("BlackRock", { w: 2600, bold: true }),
          cell("MoU announced at Abu Dhabi Finance Week to explore tokenised markets and next-generation financial architecture.", { w: 6426 })
        ]}),
        new TableRow({ children: [
          cell("Franklin Templeton", { w: 2600, bold: true, fill: WASH }),
          cell("Named by the CEO as a product development partner.", { w: 6426, fill: WASH })
        ]}),
        new TableRow({ children: [
          cell("Ninety One", { w: 2600, bold: true }),
          cell("MoU to expand opportunities in financial markets innovation.", { w: 6426 })
        ]}),
        new TableRow({ children: [
          cell("OKX Ventures / ADI Foundation", { w: 2600, bold: true, fill: WASH }),
          cell("Alliance to drive global adoption of tokenised products.", { w: 6426, fill: WASH })
        ]}),
        new TableRow({ children: [
          cell("BlockBooster / ADI Foundation", { w: 2600, bold: true }),
          cell("Ecosystem development for regulated tokenised products.", { w: 6426 })
        ]})
      ]),
      spacer(140),
      P("A seed-stage company cannot assemble this list. It is worth understanding not as a target to match but as evidence of the segment Finstreet has chosen — and, by omission, the segment it has not.", { after: 140 }),

      H2("3.7 Target customer and market thesis"),
      P("Finstreet's stated customers are long-term institutional holders: sovereign wealth funds, large family offices and institutional asset managers. Its thesis, articulated by Pasan in February 2026, is that roughly US$600 billion in private assets across Asia, Europe and the Middle East are seeking exits, and that these holders need a transparent way to manage liquidity, adjust exposure and redeploy capital without depending on one-off bilateral deals. Confidence: high.", { after: 140 }),

      H2("3.8 Strategic intent"),
      P("The ambition described publicly is to shift Abu Dhabi from being a capital allocator to being an intermediary — the venue where global buyers and sellers of private assets transact, rather than simply a source of cheque-writing capital. Confidence: high.", { after: 140 }),
      P("This is a sovereign-scale positioning objective, and it explains the shape of everything else: the licence stack, the institutional partners, and the professional-client focus all serve it. Confidence: inferred.", { after: 140 }),

      new Paragraph({ children: [new PageBreak()] }),

      // ===================== 4. ANGELSTA =====================
      H1("4. AngelSta: current position"),

      P("Stated by the AngelSta team, August 2026:", { after: 140 }),
      Bullet("Regulatory status: licence application in progress; not yet authorised."),
      Bullet("Target investors: angel investors and high-net-worth individuals."),
      Bullet("Stage: pre-launch, raising a seed round."),
      spacer(120),
      P("Publicly visible signals, noted for completeness and not independently verified:", { after: 140 }),
      Bullet("Positioning language referencing the next decade of MENA capital markets."),
      Bullet("An issuer route — companies apply to be listed on the platform."),
      Bullet("A capped investor cohort, described as a maximum of 500 seats."),
      spacer(160),
      P("The 500-seat cap is worth isolating because it is a genuine strategic choice rather than a constraint. It signals curation and scarcity: a closed, vetted investor community rather than an open venue. Finstreet's model is the opposite — an open regulated venue where any qualifying professional client may participate. These are different businesses with different defensibility. AngelSta's moat, if the model works, is the quality and exclusivity of the network; Finstreet's is the licence stack and the infrastructure. Confidence: inferred.", { after: 140 }),

      new Paragraph({ children: [new PageBreak()] }),

      // ===================== 5. HEAD TO HEAD =====================
      H1("5. Head-to-head comparison"),
      P("The purpose of this table is to show separation, not to score a contest. On most rows the two companies are not measured against the same thing.", { after: 180 }),

      table([2100, 3463, 3463], [
        headRow([2100, 3463, 3463], ["Dimension", "Finstreet", "AngelSta"]),
        new TableRow({ children: [
          cell("Core business", { w: 2100, bold: true, color: NAVY }),
          cell("Regulated financial market infrastructure — venue, depository, settlement.", { w: 3463 }),
          cell("Investor platform — origination, curation, distribution.", { w: 3463 })
        ]}),
        new TableRow({ children: [
          cell("Primary market", { w: 2100, bold: true, color: NAVY, fill: WASH }),
          cell("Secondary liquidity for existing large private assets.", { w: 3463, fill: WASH }),
          cell("Primary capital formation into early-stage companies.", { w: 3463, fill: WASH })
        ]}),
        new TableRow({ children: [
          cell("Investor type", { w: 2100, bold: true, color: NAVY }),
          cell("Professional clients only — SWFs, large family offices, institutional managers.", { w: 3463 }),
          cell("Angels and high-net-worth individuals.", { w: 3463 })
        ]}),
        new TableRow({ children: [
          cell("Issuer type", { w: 2100, bold: true, color: NAVY, fill: WASH }),
          cell("Holders of substantial private and public securities.", { w: 3463, fill: WASH }),
          cell("Companies applying to list and raise.", { w: 3463, fill: WASH })
        ]}),
        new TableRow({ children: [
          cell("Regulatory status", { w: 2100, bold: true, color: NAVY }),
          cell("Eight licences; three FSRA-regulated entities in ADGM.", { w: 3463 }),
          cell("Application in progress.", { w: 3463, color: CRIT })
        ]}),
        new TableRow({ children: [
          cell("Access model", { w: 2100, bold: true, color: NAVY, fill: WASH }),
          cell("Open regulated venue for qualifying professionals.", { w: 3463, fill: WASH }),
          cell("Closed, curated cohort — reported 500 seats.", { w: 3463, fill: WASH })
        ]}),
        new TableRow({ children: [
          cell("Ownership / capital", { w: 2100, bold: true, color: NAVY }),
          cell("Rorix Holdings / IHC — parent market cap AED 892.8bn (Sept 2024).", { w: 3463 }),
          cell("Independent; raising seed.", { w: 3463 })
        ]}),
        new TableRow({ children: [
          cell("Geography", { w: 2100, bold: true, color: NAVY, fill: WASH }),
          cell("ADGM-domiciled; global institutional reach across Asia, Europe, Middle East.", { w: 3463, fill: WASH }),
          cell("MENA-focused.", { w: 3463, fill: WASH })
        ]}),
        new TableRow({ children: [
          cell("Technology", { w: 2100, bold: true, color: NAVY }),
          cell("Hybrid conventional and blockchain; regulated tokenisation.", { w: 3463 }),
          cell("Platform software; infrastructure dependency to be determined.", { w: 3463 })
        ]}),
        new TableRow({ children: [
          cell("Institutional partners", { w: 2100, bold: true, color: NAVY, fill: WASH }),
          cell("BlackRock, Franklin Templeton, Ninety One, OKX Ventures, ADI Foundation.", { w: 3463, fill: WASH }),
          cell("Not publicly disclosed.", { w: 3463, fill: WASH })
        ]}),
        new TableRow({ children: [
          cell("Status", { w: 2100, bold: true, color: NAVY }),
          cell("Launched; subsidiaries operational.", { w: 3463 }),
          cell("Pre-launch.", { w: 3463 })
        ]})
      ]),

      new Paragraph({ children: [new PageBreak()] }),

      // ===================== 6. GAP ANALYSIS =====================
      H1("6. Gap analysis"),
      P("The gaps run in both directions. Treating this as a list of AngelSta's deficiencies would miss the more useful half of the analysis.", { after: 180 }),

      H2("6.1 Where Finstreet leads — gaps AngelSta must close"),

      table([2300, 4526, 2200], [
        headRow([2300, 4526, 2200], ["Gap", "Assessment", "Priority"]),
        new TableRow({ children: [
          cell("Regulatory authorisation", { w: 2300, bold: true, color: NAVY }),
          cell("Eight licences versus an application in progress. This is the difference between being able to hold client assets and being able to introduce parties. Until authorisation lands, AngelSta's product surface is constrained by what an unlicensed entity may lawfully do — and that constraint shapes the whole roadmap.", { w: 4526 }),
          cell("Critical — on the critical path", { w: 2200, bold: true, color: CRIT })
        ]}),
        new TableRow({ children: [
          cell("Settlement and custody", { w: 2300, bold: true, color: NAVY, fill: WASH }),
          cell("Finstreet owns depository, custody and settlement. AngelSta has no equivalent and should not build one — the cost and licensing burden are prohibitive at seed stage. The gap is real but the correct response is to source it, not to close it.", { w: 4526, fill: WASH }),
          cell("High — resolve by partnership", { w: 2200, bold: true, color: AMBER, fill: WASH })
        ]}),
        new TableRow({ children: [
          cell("Institutional credibility", { w: 2300, bold: true, color: NAVY }),
          cell("A partner list including BlackRock and Franklin Templeton, and a parent with a near-trillion-dirham market capitalisation, confer trust that cannot be manufactured. For a platform asking individuals to commit capital, trust is the product.", { w: 4526 }),
          cell("High", { w: 2200, bold: true, color: AMBER })
        ]}),
        new TableRow({ children: [
          cell("Capital depth", { w: 2300, bold: true, color: NAVY, fill: WASH }),
          cell("Effectively unlimited versus a seed round. AngelSta cannot win any contest decided by balance sheet, and should avoid picking one.", { w: 4526, fill: WASH }),
          cell("Structural — design around it", { w: 2200, bold: true, color: GREY, fill: WASH })
        ]}),
        new TableRow({ children: [
          cell("Operating track record", { w: 2300, bold: true, color: NAVY }),
          cell("Live and operational versus pre-launch. Every month before launch is a month of compounding reference customers Finstreet accumulates and AngelSta does not.", { w: 4526 }),
          cell("High — time-sensitive", { w: 2200, bold: true, color: AMBER })
        ]})
      ]),

      spacer(220),
      H2("6.2 Where Finstreet leaves room — gaps AngelSta can exploit"),

      P("Finstreet's choices are coherent and deliberate, which means the ground it has not taken is unlikely to be taken soon. Each of the following is a structural consequence of its model, not an oversight.", { after: 160 }),

      table([2300, 4526, 2200], [
        headRow([2300, 4526, 2200], ["Opening", "Assessment", "Durability"]),
        new TableRow({ children: [
          cell("The angel and HNW segment", { w: 2300, bold: true, color: NAVY }),
          cell("Finstreet's MTF serves professional clients. Most angel investors do not meet that threshold. Serving them requires different permissions, different disclosure and different conduct obligations — a regulatory project, not a product decision.", { w: 4526 }),
          cell("Durable — protected by licensing", { w: 2200, bold: true, color: TEAL })
        ]}),
        new TableRow({ children: [
          cell("Early-stage primary capital", { w: 2300, bold: true, color: NAVY, fill: WASH }),
          cell("The US$600bn secondaries thesis is about exits from large existing positions. Nothing in Finstreet's public positioning addresses seed-stage companies raising their first institutional money. That is a different asset, a different diligence process and a different economics.", { w: 4526, fill: WASH }),
          cell("Durable — different market", { w: 2200, bold: true, color: TEAL, fill: WASH })
        ]}),
        new TableRow({ children: [
          cell("Origination and deal flow", { w: 2300, bold: true, color: NAVY }),
          cell("Infrastructure does not originate. Finstreet provides a venue; someone still has to find, vet and present the opportunities. This is precisely what a curated investor platform does, and it is the layer where relationships beat balance sheets.", { w: 4526 }),
          cell("Durable — different capability", { w: 2200, bold: true, color: TEAL })
        ]}),
        new TableRow({ children: [
          cell("Community and curation", { w: 2300, bold: true, color: NAVY, fill: WASH }),
          cell("A capped cohort of vetted investors is a network business. Open regulated venues are explicitly not that — they are obliged toward non-discriminatory access. Finstreet cannot replicate a closed community without contradicting its own model.", { w: 4526, fill: WASH }),
          cell("Durable — model conflict", { w: 2200, bold: true, color: TEAL, fill: WASH })
        ]}),
        new TableRow({ children: [
          cell("Regional and linguistic reach", { w: 2300, bold: true, color: NAVY }),
          cell("Finstreet is Abu Dhabi-centred and institution-facing, competing globally for institutional flow. A platform built for Arabic-speaking investors across Egypt, Saudi Arabia, Jordan and the Levant is addressing a market Finstreet's model does not reach.", { w: 4526 }),
          cell("Moderate — contestable later", { w: 2200, bold: true, color: AMBER })
        ]}),
        new TableRow({ children: [
          cell("Ticket size", { w: 2300, bold: true, color: NAVY, fill: WASH }),
          cell("Institutional infrastructure carries a fixed cost per transaction that makes small tickets uneconomic. The economics of a US$25,000 angel cheque and a US$25 million secondary are not the same business.", { w: 4526, fill: WASH }),
          cell("Durable — unit economics", { w: 2200, bold: true, color: TEAL, fill: WASH })
        ]})
      ]),

      spacer(220),
      H2("6.3 The contested band"),

      P("One area genuinely overlaps and deserves attention rather than comfort.", { after: 140 }),

      calloutBox("Where the two models actually meet", [
        "Under ADGM rules, a sufficiently wealthy individual can be classified as a Professional Client by assessment. The top of AngelSta's high-net-worth segment therefore sits inside the bottom of Finstreet's addressable base.",
        "This band — wealthy individuals who qualify as professional clients and want access to private assets — is the one place the two companies could compete for the same person.",
        "AngelSta's advantage there is curation, community and early-stage access. Finstreet's is regulatory certainty and institutional-grade custody. AngelSta should expect to win on the former and should not attempt to compete on the latter."
      ], AMBER),

      new Paragraph({ children: [new PageBreak()] }),

      // ===================== 7. THREAT =====================
      H1("7. Competitive threat assessment"),

      table([2600, 1800, 4626], [
        headRow([2600, 1800, 4626], ["Threat vector", "Rating", "Reasoning"]),
        new TableRow({ children: [
          cell("Direct customer competition today", { w: 2600, bold: true, color: NAVY }),
          cell("Low", { w: 1800, bold: true, color: TEAL }),
          cell("Different investor class, different asset, different ticket size. Separated by regulatory perimeter, not merely by positioning.", { w: 4626 })
        ]}),
        new TableRow({ children: [
          cell("Move down-market into HNW", { w: 2600, bold: true, color: NAVY, fill: WASH }),
          cell("Moderate", { w: 1800, bold: true, color: AMBER, fill: WASH }),
          cell("Requires new permissions and a different conduct regime — slow, but entirely affordable for this parent if the segment proves attractive.", { w: 4626, fill: WASH })
        ]}),
        new TableRow({ children: [
          cell("Talent and partner capture", { w: 2600, bold: true, color: NAVY }),
          cell("Moderate", { w: 1800, bold: true, color: AMBER }),
          cell("Competing for the same scarce regulatory, market-infrastructure and compliance talent in a small Gulf market, against a far larger balance sheet.", { w: 4626 })
        ]}),
        new TableRow({ children: [
          cell("Regulatory precedent setting", { w: 2600, bold: true, color: NAVY, fill: WASH }),
          cell("Moderate", { w: 1800, bold: true, color: AMBER, fill: WASH }),
          cell("Finstreet is shaping how ADGM thinks about digital private-market venues. That precedent may help AngelSta by clearing a path, or hinder it by setting institution-scale expectations for any applicant.", { w: 4626, fill: WASH })
        ]}),
        new TableRow({ children: [
          cell("Infrastructure dependency", { w: 2600, bold: true, color: NAVY }),
          cell("Watch", { w: 1800, bold: true, color: NAVY }),
          cell("If AngelSta ultimately settles through Finstreet rails, Finstreet becomes both supplier and potential competitor. Manageable, but it should be a conscious decision rather than a default.", { w: 4626 })
        ]}),
        new TableRow({ children: [
          cell("Narrative crowding in fundraising", { w: 2600, bold: true, color: NAVY, fill: WASH }),
          cell("High", { w: 1800, bold: true, color: CRIT, fill: WASH }),
          cell("Investors hearing 'MENA private capital markets' will name Finstreet. AngelSta needs a one-sentence answer to why it is not the same thing. This is the most immediate practical impact of Finstreet's existence.", { w: 4626, fill: WASH })
        ]})
      ]),

      new Paragraph({ children: [new PageBreak()] }),

      // ===================== 8. RECOMMENDATIONS =====================
      H1("8. Strategic implications"),

      H2("8.1 Sharpen the category boundary before the seed round closes"),
      P("The most immediate cost of Finstreet's existence is not lost customers — it is confusion in investor meetings. AngelSta needs a rehearsed, one-sentence distinction. Something in the shape of: Finstreet builds the exchange for institutions to trade large private assets; AngelSta builds the network that funds companies before they are large enough to be one. Whatever the final wording, it should be settled and consistent across the deck, the site and the team.", { after: 160 }),

      H2("8.2 Treat time-to-licence as the primary operating metric"),
      P("Everything durable about AngelSta's model — holding client money, listing issuers, facilitating investment — sits behind authorisation. Finstreet's eight licences are the benchmark a regulator and an investor will both have in mind. The seed narrative should present a specific regulator, a specific permission set, a dated timeline and a named regulatory lead. Vagueness here is expensive.", { after: 160 }),

      H2("8.3 Evaluate Finstreet as infrastructure, not only as a rival"),
      P("Custody, settlement and depository are exactly the capabilities a seed-stage platform should rent rather than build. Opening an exploratory conversation costs little and clarifies a great deal — including how Finstreet views the angel segment, which is itself valuable intelligence. The risk of supplier concentration is real and should be weighed, but it is a smaller risk than attempting to build regulated settlement infrastructure on a seed round.", { after: 160 }),

      H2("8.4 Build the moat where infrastructure cannot follow"),
      P("Finstreet's structural weakness in AngelSta's market is that it has no origination and no community, and its model actively prevents it from developing either. AngelSta's defensibility should concentrate there: quality of vetted deal flow, the strength and exclusivity of the investor cohort, and the trust that comes from curation. The 500-seat cap is a sound instinct — it should be treated as a strategic asset and protected, not relaxed under growth pressure.", { after: 160 }),

      H2("8.5 Monitor the contested band deliberately"),
      P("Set a standing review — quarterly is sufficient — on whether Finstreet begins describing individual investors, lowering minimums, or seeking retail-adjacent permissions. Those are the leading indicators of a move into AngelSta's segment, and they would appear in regulatory filings and announcements well before they appear in the product.", { after: 160 }),

      new Paragraph({ children: [new PageBreak()] }),

      // ===================== 9. WATCH LIST =====================
      H1("9. Watch list"),
      P("Specific, checkable signals. Each would change part of this analysis.", { after: 160 }),

      table([4200, 2400, 2426], [
        headRow([4200, 2400, 2426], ["Signal to watch", "Where it appears", "What it would mean"]),
        new TableRow({ children: [
          cell("Finstreet applying for retail or additional client-category permissions", { w: 4200 }),
          cell("ADGM/FSRA public register", { w: 2400 }),
          cell("Direct move into AngelSta's segment. Escalate.", { w: 2426, bold: true, color: CRIT })
        ]}),
        new TableRow({ children: [
          cell("Published minimum ticket sizes falling materially", { w: 4200, fill: WASH }),
          cell("finstreet.ae, announcements", { w: 2400, fill: WASH }),
          cell("Down-market intent.", { w: 2426, fill: WASH, color: AMBER, bold: true })
        ]}),
        new TableRow({ children: [
          cell("Language shifting from 'professional clients' to 'investors' or 'individuals'", { w: 4200 }),
          cell("Website, press, interviews", { w: 2400 }),
          cell("Early positioning signal, usually precedes filings.", { w: 2426, bold: true, color: AMBER })
        ]}),
        new TableRow({ children: [
          cell("Launch of an early-stage or venture-focused product line", { w: 4200, fill: WASH }),
          cell("Announcements, ADFW", { w: 2400, fill: WASH }),
          cell("Direct overlap on asset class.", { w: 2426, fill: WASH, bold: true, color: CRIT })
        ]}),
        new TableRow({ children: [
          cell("Other IHC or Rorix entities entering venture or angel investing", { w: 4200 }),
          cell("IHC disclosures", { w: 2400 }),
          cell("Group-level entry without Finstreet's constraints.", { w: 2426, bold: true, color: AMBER })
        ]}),
        new TableRow({ children: [
          cell("AngelSta's own authorisation granted", { w: 4200, fill: WASH }),
          cell("Regulator register", { w: 2400, fill: WASH }),
          cell("Removes the largest single gap in this analysis.", { w: 2426, fill: WASH, bold: true, color: TEAL })
        ]})
      ]),

      new Paragraph({ children: [new PageBreak()] }),

      // ===================== 10. SOURCES =====================
      H1("10. Sources"),
      P("All sources accessed August 2026. Regulatory register entries and official announcements are treated as primary.", { after: 160 }),

      H3("Regulatory"),
      Bullet("ADGM FSRA public register — Finstreet Global Markets Limited (ref. 240055): adgm.com/public-registers/fsra/firms/financial-firms/finstreet-global-markets-limited-240055"),
      Bullet("ADGM FSRA public register — Finstreet Global Clearing and Settlement Limited (ref. 240056): adgm.com/public-registers/fsra/firms/financial-firms/finstreet-global-clearing-and-settlement-limited-240056"),
      Bullet("ADGM FSRA public register — Finstreet Capital Limited (ref. 220148): adgm.com/public-registers/fsra/firms/financial-firms/finstreet-capital-limited-220148"),

      H3("Company and exchange announcements"),
      Bullet("ADGM — Finstreet Launches First-of-its-Kind International Securities Financial Market Infrastructure at ADFW: adgm.com/media/announcements/finstreet-launches-financial-market-infrastructure-at-adfw"),
      Bullet("Zawya — Finstreet to launch first regulated digital venue in ADGM for trading both Private and Public Securities"),
      Bullet("Zawya — BlackRock and IHC Group entities Finstreet Limited and ADI Foundation"),
      Bullet("Zawya — Finstreet Limited and Ninety One sign MoU to expand opportunities in financial markets innovation"),
      Bullet("Zawya — Finstreet, ADI and OKX Ventures sign MoU to drive global adoption of tokenized products"),
      Bullet("PR Newswire — ADI Foundation and Finstreet Partner with BlockBooster for Regulated Tokenized Products"),

      H3("Press and interviews"),
      Bullet("Semafor (24 February 2026) — Finstreet sees UAE as crossroads in private capital boom (interview with Sunidhi Pasan): semafor.com/article/02/24/2026/finstreet-sees-uae-as-crossroads-in-private-capital-boom"),
      Bullet("Forbes Middle East — IHC-owned Finstreet launches first regulated digital trading platform on ADGM"),
      Bullet("Khaleej Times — Finstreet launches first-of-its-kind international securities financial market infrastructure at ADFW"),
      Bullet("Gulf Business — Rorix Holdings' Finstreet unveils regulated digital trading platform at ADGM"),
      Bullet("Economy Middle East — Finstreet to launch first regulated digital market in ADGM for private, public securities"),
      Bullet("Markets Media — First regulated digital venue to launch in Abu Dhabi for private and public securities"),
      Bullet("Milken Institute Global Conference 2025 — speaker profile, Sunidhi Pasan"),

      H3("Company profile databases"),
      Bullet("Tracxn — Finstreet company profile"),
      Bullet("Crunchbase — Sunidhi Pasan, Group CEO and Founder, Finstreet"),
      Bullet("Dun & Bradstreet — Finstreet Limited company profile, Abu Dhabi"),

      H3("AngelSta"),
      Bullet("Positions confirmed directly by the AngelSta team, August 2026."),
      Bullet("Public signals from angelsta.net as surfaced in search indexes; the site itself could not be retrieved directly (see Section 2)."),

      spacer(280),
      rule(),
      RichP([
        { t: "Prepared for AngelSta, August 2026. ", b: true, c: NAVY },
        { t: "This document reflects publicly available information as at the date of writing and the analytical judgements of its author. Section 2 sets out the limits of the evidence base; conclusions marked as inferred should be tested before they are relied upon for material decisions.", c: GREY }
      ], { after: 0 })
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("Finstreet_Competitive_Analysis.docx", buf);
  console.log("written:", buf.length, "bytes");
});
