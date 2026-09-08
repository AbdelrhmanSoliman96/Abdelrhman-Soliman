# -*- coding: utf-8 -*-
"""
StartPad × GrowthLabs — LEAP launch press release. Arabic and English.

Single source of truth for the release copy. The .docx, the .md exports and the
press-kit page are all generated from this file, so no version of the release can
drift from another.

BLOCK TYPES
  ("h",  text)                 section heading
  ("p",  text)                 body paragraph
  ("b",  [text, ...])          bullet list
  ("q",  quote, attribution)   pull quote with attribution
  ("kv", [(label, value)])     fact table (notes to editors, contacts)

FACT PROVENANCE
Figures about LEAP 2026 and about GrowthLabs came from live web searches during
drafting and are cited in NOTES_SOURCES. Figures about StartPad's own product come
from the founder's own mission and tool-library source files in this repository.
Anything the founder still has to supply is written as a [BRACKETED PLACEHOLDER]
so it cannot be published by accident.
"""

RELEASE_DATE_AR = "الرياض، المملكة العربية السعودية — 8 سبتمبر 2026"
RELEASE_DATE_EN = "RIYADH, SAUDI ARABIA — 8 September 2026"

# --------------------------------------------------------------------------- AR

AR = {
    "lang": "ar",
    "dir": "rtl",
    "kicker": "للنشر الفوري",
    "headline": (
        "«ستارتباد» تنطلق من الرياض خلال LEAP… وGrowthLabs تتبنّى المنصة "
        "بالكامل في صفقة احتضان استراتيجي غير نقدية"
    ),
    "subhead": (
        "منصة تحوّل فكرة رائد الأعمال إلى شركة جاهزة للاستثمار عبر 15 مهمة موجَّهة "
        "ومكتبة تضم أكثر من 120 أداة — والمؤسس عبدالرحمن سليمان يواصل قيادة المنتج "
        "داخل منظومة GrowthLabs"
    ),
    "dateline": RELEASE_DATE_AR,
    "blocks": [
        ("p",
         "أعلنت StartPad (ستارتباد) عن إطلاقها الرسمي من على منصة LEAP في الرياض، "
         "بوصفها منصة تأسيس الشركات الناشئة التي تنقل رائد الأعمال من الفكرة الأولى "
         "إلى شركة منظَّمة ومُتحقَّق من جدواها وجاهزة لدخول برامج الاحتضان والاستثمار، "
         "عبر مسار عملي من 15 مهمة موجَّهة."),
        ("p",
         "وبالتزامن مع الإطلاق، أعلنت GrowthLabs — الشركة المتخصصة في بناء البنية "
         "الرقمية لمنظومات ريادة الأعمال في الشرق الأوسط وشمال أفريقيا — عن تبنّي "
         "StartPad بالكامل وضمّها إلى منظومتها، في صفقة احتضان استراتيجي غير نقدية "
         "يواصل بموجبها المؤسس عبدالرحمن سليمان قيادة المنتج."),
        ("p",
         "ويأتي الإعلان من قلب أكبر تجمّع تقني في المنطقة؛ إذ استقطبت نسخة هذا العام "
         "من LEAP في مركز الرياض للمعارض والمؤتمرات بملهم أكثر من 1,800 شركة تقنية، "
         "وما يزيد على 600 شركة ناشئة، ونحو 1,900 مستثمر وممثل لصناديق رأس المال "
         "الجريء، إلى جانب أكثر من 1,000 متحدث."),

        ("h", "أولًا: ما هي StartPad وماذا تقدّم"),
        ("p",
         "تنطلق StartPad من ملاحظة تتكرر في كل منظومة ريادة أعمال بالمنطقة: الغالبية "
         "العظمى من الأفكار لا تُرفض من برامج الاحتضان لأنها أفكار رديئة، بل لأنها تصل "
         "غير مُختبَرة. يملك المؤسس رؤية واضحة وشغفًا حقيقيًا، لكنه لا يملك دليلًا واحدًا "
         "على أن المشكلة التي يحلّها موجودة فعلًا، ولا لغة مشتركة يتحدث بها إلى مستثمر."),
        ("p",
         "تعالج StartPad هذه الفجوة بتحويل رحلة التأسيس إلى مسار من 15 مهمة متتابعة، "
         "تمتد من تحليل المشكلة وتعريفها، مرورًا باختيار الفكرة واختبار فرضية الحل "
         "وبناء نموذج العمل والنموذج الأولي، وصولًا إلى بناء المنتج الأدنى القابل "
         "للتطبيق واختبار ملاءمة المنتج للسوق ثم الانطلاق إلى السوق. ولا تُفتح المهمة "
         "التالية قبل أن يستوفي المؤسس شروط المهمة التي تسبقها."),
        ("p", "وفي كل مهمة يجد المؤسس بين يديه:"),
        ("b", [
            "مكتبة أدوات تضم أكثر من 120 أداة تفاعلية — من مصفوفة الأهمية والتكرار "
            "وبطاقة تقييم الفكرة، إلى تحجيم السوق ونموذج العمل والقوائم المالية "
            "وجدول الملكية — كل أداة معروضة داخل المهمة التي تحتاجها، لا في قائمة "
            "منفصلة يبحث فيها.",
            "تقييم بالذكاء الاصطناعي لكل إجابة وفق معايير معلنة: قوة الدليل، والوضوح، "
            "والعمق، وقابلية التنفيذ. الهدف أن يُقاس تقدّم المؤسس بما أثبته، لا بما "
            "يظنّه عن نفسه.",
            "محتوى تعليمي مُنسَّق لكل مهمة — مواد مرئية ومقروءة مختارة تشرح الإطار "
            "الفكري وراء المهمة قبل الشروع فيها.",
            "مخرجات جاهزة للاستخدام تتولّد من إجابات المؤسس نفسها: ملخص تنفيذي، "
            "وعرض تقديمي للمستثمرين، ونموذج مالي، وملف جاهزية استثمارية.",
            "دعم كامل للغتين العربية والإنجليزية، بتصميم يراعي اتجاه الكتابة من "
            "اليمين إلى اليسار.",
        ]),
        ("p",
         "ورؤية StartPad أن تصبح نقطة البداية الافتراضية لكل مؤسس في المنطقة: أن يكون "
         "لكل صاحب فكرة — في القاهرة أو الرياض أو عمّان أو الدوحة — مسار واضح ومجاني "
         "الدخول ينقله من «لديّ فكرة» إلى «لديّ أدلة»، فلا تموت فكرة جيدة لغياب "
         "الخريطة وحدها."),
        ("q",
         "بنينا StartPad لأننا رأينا العدد نفسه من الأفكار الجيدة يتعثّر عند النقطة "
         "نفسها: صاحب الفكرة يعرف إلى أين يريد الوصول، لكنه لا يملك خريطة لليوم "
         "التالي. المهمة الأولى في StartPad لا تسأل المؤسس عن حلمه، بل تسأله عمّن "
         "تحدّث معه هذا الأسبوع وماذا سمع منه. هذا الفارق الصغير هو ما يصنع شركات "
         "قابلة للاستثمار.",
         "عبدالرحمن سليمان، مؤسس StartPad"),

        ("h", "ثانيًا: احتضان كامل للمشروع… بلا مقابل نقدي"),
        ("p",
         "بموجب الاتفاق، انضمت StartPad بالكامل إلى منظومة GrowthLabs ضمن هيكل قائم "
         "على تبادل الحصص والدمج التشغيلي، دون أي مقابل نقدي مدفوع للمؤسس. ويصف "
         "الطرفان الصفقة بأنها تبنٍّ كامل للمشروع واحتضان له داخل منظومة قائمة، لا "
         "عملية بيع؛ إذ لم يخرج المؤسس من المنتج، بل دخل به إلى بنية تحتية أوسع."),
        ("p",
         "ويواصل عبدالرحمن سليمان قيادة StartPad بوصفها خط منتج قائمًا بذاته داخل "
         "GrowthLabs، مع احتفاظ المنصة باسمها وهويتها وخارطة طريقها المستقلة."),
        ("p",
         "وهذا الهيكل غير النقدي ليس استثناءً في سياسة GrowthLabs، بل امتداد لنهج "
         "معلن؛ فقد أتمّت الشركة في وقت سابق من هذا العام ضمّ منصة Startup Gate في "
         "صفقة بقيمة 35 مليون جنيه مصري (نحو 657 ألف دولار) قامت هي الأخرى على تبادل "
         "الحصص ومكافآت مرتبطة بالأداء بدلًا من الدفع النقدي."),
        ("q",
         "لم أتقاضَ مقابلًا نقديًا عن StartPad، وهذا كان اختيارًا لا اضطرارًا. ما احتاجته "
         "المنصة في هذه المرحلة ليس شيكًا، بل بنية تحتية وأسواقًا وفرقًا تعرف كيف تُدار "
         "برامج ريادة الأعمال على أرض الواقع. GrowthLabs قدّمت ذلك بالضبط، وجاء هيكل "
         "الصفقة معبّرًا عن الأولوية: احتضان المشروع وتبنّيه، لا شراؤه.",
         "عبدالرحمن سليمان، مؤسس StartPad"),
        ("p",
         "وبانضمام StartPad تكتمل سلسلة منتجات GrowthLabs الثلاث في رحلة واحدة متصلة: "
         "StartPad تُهيّئ المؤسس لأول مرة، وCatalystOS يُشغّل البرامج التي تُنمّيه، "
         "وStartup Gate يربطه بالسوق والمستثمرين — من الفكرة الأولى إلى التوسّع، "
         "بمسار واحد بدلًا من برامج متفرقة لا يجمعها رابط."),
        ("q",
         "[اقتباس مقترح — يحتاج اعتماد المتحدث] StartPad تُكمل الحلقة الأولى في "
         "منظومتنا. كنا نملك الأدوات التي تُدار بها البرامج والشبكة التي تربط "
         "المؤسسين بالسوق، وكان ينقصنا ما يسبق ذلك كله: المكان الذي يتعلّم فيه "
         "المؤسس كيف يبني شركة قبل أن يطرق باب أي برنامج. رأينا في StartPad وفي "
         "عبدالرحمن هذا المكان، فاخترنا أن نتبنّاه لا أن نشتريه.",
         "إسلام محمد، مؤسس GrowthLabs"),

        ("h", "ثالثًا: عن GrowthLabs وماذا تقدّم"),
        ("p",
         "تعمل GrowthLabs على بناء البنية الرقمية لمنظومات ريادة الأعمال؛ أي الطبقة "
         "البرمجية التي تُدار بها الحاضنات والمسرّعات والجامعات والجهات التنموية "
         "والمستثمرون في الشرق الأوسط وشمال أفريقيا. وبدلًا من أن تتعامل كل جهة مع "
         "أدوات متفرقة لإدارة المتقدمين وتقييم الشركات وقياس الأثر، تقدّم GrowthLabs "
         "هذه الوظائف في منظومة واحدة."),
        ("p", "وتقوم المنظومة على ثلاثة منتجات:"),
        ("b", [
            "StartPad — تُهيّئ المؤسسين لأول مرة وتنقلهم من الفكرة إلى الجاهزية.",
            "CatalystOS — نظام تشغيل الحاضنات والمسرّعات: إدارة الدفعات، وتقييم "
            "الشركات، ومطابقة المرشدين، وتتبّع الأداء وقياس الأثر.",
            "Startup Gate — شبكة تربط المؤسسين بالمستثمرين والسوق.",
        ]),
        ("p", "وتشمل مؤشرات الشركة المعلنة:"),
        ("b", [
            "أكثر من 5,000 شركة ناشئة مدعومة.",
            "أكثر من 60 برنامجًا دوليًا شُغّلت عبر المنصة.",
            "حضور في أسواق تشمل مصر والسعودية وقطر والأردن وباكستان وأمريكا الجنوبية.",
            "خطة توسّع في خمس دول جديدة في الخليج وأفريقيا بحلول نهاية 2026.",
            "سبعة برامج ابتكار مؤسسي مزمع إطلاقها ضمن استراتيجية 2026، إلى جانب أول "
            "مجتمع ريادي عابر للحدود في المنطقة.",
        ]),

        ("h", "التوافر"),
        ("p",
         "StartPad متاحة الآن عبر startpad.me باللغتين العربية والإنجليزية. "
         "[يُستكمل: نموذج الاشتراك، وتفاصيل الطرح للجهات والشركاء، وأي عرض خاص "
         "مرتبط بالإطلاق.]"),

        ("h", "نبذة عن StartPad"),
        ("p",
         "StartPad منصة لتأسيس الشركات الناشئة تنقل المؤسس من الفكرة إلى شركة جاهزة "
         "للاستثمار عبر 15 مهمة موجَّهة، مدعومة بمكتبة تضم أكثر من 120 أداة وتقييم "
         "بالذكاء الاصطناعي قائم على الأدلة. تأسست على يد عبدالرحمن سليمان، وهي اليوم "
         "جزء من منظومة GrowthLabs. للمزيد: startpad.me"),

        ("h", "نبذة عن GrowthLabs"),
        ("p",
         "GrowthLabs شركة تبني البنية الرقمية لمنظومات ريادة الأعمال، وتمكّن الحاضنات "
         "والمسرّعات والجامعات والجهات التنموية والمستثمرين عبر منتجاتها StartPad "
         "وCatalystOS وStartup Gate. أسسها إسلام محمد، وقد دعمت أكثر من 5,000 شركة "
         "ناشئة عبر أكثر من 60 برنامجًا دوليًا. للمزيد: growthlabs.app"),

        ("h", "للتواصل الإعلامي"),
        ("kv", [
            ("StartPad", "عبدالرحمن سليمان، المؤسس — [البريد الإلكتروني] — [الهاتف]"),
            ("GrowthLabs", "[اسم مسؤول التواصل] — [البريد الإلكتروني] — [الهاتف]"),
            ("الموقع", "startpad.me · growthlabs.app"),
            ("لينكدإن", "linkedin.com/in/abdelrhman-soliman96 · "
                        "linkedin.com/company/growthlabs-vi"),
        ]),

        ("h", "ملاحظات للمحرّرين"),
        ("b", [
            "الصفقة غير نقدية بالكامل: لم يُدفع أي مقابل نقدي للمؤسس، والهيكل قائم "
            "على تبادل الحصص والدمج التشغيلي.",
            "يواصل المؤسس قيادة StartPad داخل GrowthLabs، وتحتفظ المنصة باسمها "
            "وهويتها.",
            "أرقام LEAP الواردة أعلاه أرقام معلنة عن نسخة هذا العام من الحدث في مركز "
            "الرياض للمعارض والمؤتمرات بملهم.",
            "الصور والشعارات ومواد الهوية متاحة عند الطلب.",
        ]),
    ],
}

# --------------------------------------------------------------------------- EN

EN = {
    "lang": "en",
    "dir": "ltr",
    "kicker": "FOR IMMEDIATE RELEASE",
    "headline": (
        "StartPad launches at LEAP in Riyadh as GrowthLabs fully adopts the "
        "platform in a non-cash strategic incubation deal"
    ),
    "subhead": (
        "A founder platform that turns an idea into an investable company across 15 "
        "guided missions and a library of 120+ tools — founder Abdelrhman Soliman "
        "continues to lead the product inside GrowthLabs"
    ),
    "dateline": RELEASE_DATE_EN,
    "blocks": [
        ("p",
         "StartPad has officially launched from the LEAP stage in Riyadh as a "
         "company-formation platform that carries a founder from a first idea to a "
         "structured, evidence-backed company ready to enter incubation and raise "
         "capital — through a practical path of 15 guided missions."),
        ("p",
         "Alongside the launch, GrowthLabs — the company building the digital "
         "infrastructure behind entrepreneurship ecosystems across MENA — announced "
         "that it has fully adopted StartPad into its ecosystem in a non-cash "
         "strategic incubation deal, under which founder Abdelrhman Soliman "
         "continues to lead the product."),
        ("p",
         "The announcement comes from the region's largest technology gathering. "
         "This year's edition of LEAP, at the Riyadh Exhibition and Convention "
         "Centre in Malham, drew more than 1,800 technology companies, over 600 "
         "startups, some 1,900 investors and venture capital representatives, and "
         "more than 1,000 speakers."),

        ("h", "1. What StartPad is, and what it offers"),
        ("p",
         "StartPad begins from an observation that repeats across every "
         "entrepreneurship ecosystem in the region: the vast majority of ideas are "
         "not rejected by incubation programmes because they are bad ideas, but "
         "because they arrive untested. The founder has a clear vision and real "
         "conviction — and not a single piece of evidence that the problem they are "
         "solving actually exists, nor a shared language in which to speak to an "
         "investor."),
        ("p",
         "StartPad closes that gap by turning company formation into a sequence of "
         "15 missions, running from problem analysis and definition, through idea "
         "selection, solution-hypothesis testing, the business model and the "
         "prototype, to building an MVP, testing product-market fit and going to "
         "market. The next mission does not open until the one before it has been "
         "answered properly."),
        ("p", "Inside every mission, a founder gets:"),
        ("b", [
            "A library of 120+ interactive tools — from the importance/frequency "
            "matrix and the idea scorecard to market sizing, the business model, "
            "financial statements and the cap table — each surfaced inside the "
            "mission that needs it, rather than buried in a separate menu.",
            "AI evaluation of every answer against stated criteria: strength of "
            "evidence, clarity, depth and feasibility. Progress is measured by what "
            "a founder has proven, not by how they rate themselves.",
            "Curated learning material for each mission — selected video and reading "
            "that teaches the thinking behind the mission before the founder starts "
            "it.",
            "Ready-to-use outputs generated from the founder's own answers: an "
            "executive summary, an investor deck, a financial model and an "
            "investment-readiness file.",
            "Full Arabic and English support, designed for right-to-left reading.",
        ]),
        ("p",
         "StartPad's vision is to become the default starting point for every "
         "founder in the region: that anyone with an idea — in Cairo, Riyadh, Amman "
         "or Doha — has a clear, free-to-enter path from \"I have an idea\" to \"I "
         "have evidence\", so that no good idea dies for want of a map alone."),
        ("q",
         "We built StartPad because we kept watching the same good ideas stall at "
         "the same point: the founder knows where they want to get to, but has no "
         "map for the next day. StartPad's first mission does not ask a founder "
         "about their dream. It asks who they spoke to this week, and what they "
         "heard. That small difference is what produces investable companies.",
         "Abdelrhman Soliman, Founder of StartPad"),

        ("h", "2. A full adoption of the project — with no cash changing hands"),
        ("p",
         "Under the agreement, StartPad has joined the GrowthLabs ecosystem in full, "
         "through a structure based on an equity swap and operational integration, "
         "with no cash consideration paid to the founder. Both sides describe the "
         "deal as an adoption and full incubation of the project inside an existing "
         "ecosystem rather than a sale: the founder has not exited the product, he "
         "has brought it into a larger infrastructure."),
        ("p",
         "Abdelrhman Soliman continues to lead StartPad as a standalone product line "
         "within GrowthLabs, and the platform keeps its own name, identity and "
         "roadmap."),
        ("p",
         "The non-cash structure is not an exception in GrowthLabs' approach but an "
         "extension of a stated one: earlier this year the company completed its "
         "acquisition of Startup Gate in a deal valued at EGP 35 million "
         "(approximately USD 657,000) that was likewise built on an equity swap and "
         "performance-linked earn-outs rather than a cash payment."),
        ("q",
         "I took no cash for StartPad, and that was a choice rather than a "
         "constraint. What the platform needed at this stage was not a cheque — it "
         "was infrastructure, markets, and teams who know how entrepreneurship "
         "programmes actually run on the ground. GrowthLabs offered exactly that, "
         "and the structure of the deal reflected the priority: to adopt and "
         "incubate the project, not to buy it.",
         "Abdelrhman Soliman, Founder of StartPad"),
        ("p",
         "With StartPad added, GrowthLabs' three products complete a single "
         "continuous journey: StartPad prepares first-time founders, CatalystOS runs "
         "the programmes that grow them, and Startup Gate connects them to the market "
         "and to investors — from first idea to scale, as one path rather than a set "
         "of disconnected programmes."),
        ("q",
         "[PROPOSED QUOTE — REQUIRES SPEAKER APPROVAL] StartPad completes the first "
         "link in our ecosystem. We had the tools that run programmes and the network "
         "that connects founders to the market. What we did not have was what comes "
         "before all of it: the place where a founder learns how to build a company "
         "before knocking on any programme's door. We saw that place in StartPad and "
         "in Abdelrhman — so we chose to adopt it rather than buy it.",
         "Islam Mohamed, Founder of GrowthLabs"),

        ("h", "3. About GrowthLabs, and what it offers"),
        ("p",
         "GrowthLabs builds the digital infrastructure of entrepreneurship "
         "ecosystems — the software layer that incubators, accelerators, "
         "universities, development institutions and investors across MENA run on. "
         "Instead of each organisation stitching together separate tools for "
         "applications, startup assessment and impact measurement, GrowthLabs "
         "delivers those functions as one system."),
        ("p", "The ecosystem rests on three products:"),
        ("b", [
            "StartPad — prepares first-time founders and moves them from idea to "
            "readiness.",
            "CatalystOS — the operating system for incubators and accelerators: "
            "cohort management, startup assessment, mentor matching, performance "
            "tracking and impact measurement.",
            "Startup Gate — the network connecting founders to investors and to the "
            "market.",
        ]),
        ("p", "The company's stated figures include:"),
        ("b", [
            "More than 5,000 startups supported.",
            "More than 60 international programmes run on the platform.",
            "A presence in markets including Egypt, Saudi Arabia, Qatar, Jordan, "
            "Pakistan and South America.",
            "Plans to expand into five new countries across the Gulf and Africa by "
            "the end of 2026.",
            "Seven flagship corporate innovation programmes planned under its 2026 "
            "strategy, alongside the region's first cross-border entrepreneurial "
            "community.",
        ]),

        ("h", "Availability"),
        ("p",
         "StartPad is available now at startpad.me in Arabic and English. "
         "[TO COMPLETE: pricing model, institutional and partner availability, and "
         "any launch offer.]"),

        ("h", "About StartPad"),
        ("p",
         "StartPad is a company-formation platform that moves a founder from idea to "
         "investable company across 15 guided missions, supported by a library of "
         "120+ tools and evidence-based AI evaluation. Founded by Abdelrhman "
         "Soliman, it is now part of the GrowthLabs ecosystem. More: startpad.me"),

        ("h", "About GrowthLabs"),
        ("p",
         "GrowthLabs builds the digital infrastructure of entrepreneurship "
         "ecosystems, powering incubators, accelerators, universities, development "
         "institutions and investors through its StartPad, CatalystOS and Startup "
         "Gate products. Founded by Islam Mohamed, it has supported more than 5,000 "
         "startups across more than 60 international programmes. More: "
         "growthlabs.app"),

        ("h", "Media contact"),
        ("kv", [
            ("StartPad", "Abdelrhman Soliman, Founder — [EMAIL] — [PHONE]"),
            ("GrowthLabs", "[COMMS CONTACT] — [EMAIL] — [PHONE]"),
            ("Web", "startpad.me · growthlabs.app"),
            ("LinkedIn", "linkedin.com/in/abdelrhman-soliman96 · "
                         "linkedin.com/company/growthlabs-vi"),
        ]),

        ("h", "Notes to editors"),
        ("b", [
            "The transaction is entirely non-cash: no cash consideration was paid to "
            "the founder; the structure is an equity swap plus operational "
            "integration.",
            "The founder continues to lead StartPad within GrowthLabs, and the "
            "platform retains its name and identity.",
            "LEAP figures cited above are the published figures for this year's "
            "edition at the Riyadh Exhibition and Convention Centre, Malham.",
            "Images, logos and brand assets are available on request.",
        ]),
    ],
}

VERSIONS = [AR, EN]

# Sources consulted while drafting, for fact-checking before distribution.
NOTES_SOURCES = [
    ("LEAP attendance and exhibitor figures",
     "https://www.wamda.com/2026/08/leap-2026-opens-riyadh-fifth-edition"),
    ("LEAP venue and programme",
     "https://onegiantleap.com/"),
    ("GrowthLabs products and positioning",
     "https://growthlabs.app/"),
    ("GrowthLabs / Startup Gate deal, structure and company figures",
     "https://www.wamda.com/2026/05/growthlabs-acquires-startup-gate-build-unified-startup-infrastructure-mena"),
    ("Startup Gate deal reported as a share swap, non-cash",
     "https://enterpriseam.com/egypt/2026/05/20/growthlabs-takes-over-startup-gate-via-share-swap/"),
    ("Startup Gate deal value in EGP and USD",
     "https://www.zawya.com/en/economy/north-africa/egypt-growthlabs-acquires-startup-gate-in-deal-nearly-658-776-qrfdogp4"),
    ("StartPad positioning within the GrowthLabs continuum",
     "https://startpad.me/"),
]
