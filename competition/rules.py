# -*- coding: utf-8 -*-
"""
Mission Zero — the participant-facing pack, in Arabic and English.

This is what goes live on day one: the rules, the published rubric, the month's
schedule, and the landing-page copy. The plan in the playbook is for the team;
this file is for the 19-year-old deciding whether to enter.

Three things here are not negotiable and are stated in both languages, in the
body and again in the summary, because they are the questions every young
Egyptian founder actually asks before signing up:

  1. The idea stays theirs. No assignment, no right of first refusal.
  2. Entry is free, and always will be.
  3. A machine does not pick the winners.

BLOCK TYPES
  ("h",  text)                       section heading
  ("p",  text)                       paragraph
  ("b",  [text, ...])                bullets
  ("n",  [text, ...])                numbered list
  ("t",  [headers], [[cells], ...])  table
  ("cal", [(when, what, detail)])    schedule rows
"""

VERSION = "v1.0 — 13 September 2026"

DATES = {
    "register_open": ("21 سبتمبر 2026", "21 September 2026"),
    "launch": ("3–5 أكتوبر 2026 — تكني سميت الإسكندرية",
               "3–5 October 2026 — Techne Summit Alexandria"),
    "missions_open": ("4 أكتوبر 2026", "4 October 2026"),
    "deadline": ("4 نوفمبر 2026، 11:59 مساءً بتوقيت القاهرة",
                 "4 November 2026, 23:59 Cairo time"),
    "judging": ("5–12 نوفمبر 2026", "5–12 November 2026"),
    "demo_day": ("أواخر نوفمبر 2026", "late November 2026"),
}

# --------------------------------------------------------------------------- AR

AR = {
    "lang": "ar",
    "dir": "rtl",
    "name": "المهمة صفر",
    "tagline": "من فكرة… إلى شركة قابلة للاستثمار في شهر واحد",
    "doc_title": "قواعد المسابقة ومعايير التقييم",
    "version_line": "الإصدار 1.0 — 13 سبتمبر 2026",

    "hero": {
        "eyebrow": "بالشراكة مع تكني سميت الإسكندرية",
        "h1": "المهمة صفر",
        "sub": "تحدٍّ وطني لرواد الأعمال الشباب: أكمل مهام StartPad الخمس عشرة في شهر، "
               "واصعد على المسرح.",
        "cta": "سجّل مجانًا",
        "points": [
            "١٥ مهمة موجَّهة تنقلك من «عندي فكرة» إلى «عندي دليل».",
            "أكثر من ١٢٠ أداة، وتقييم يقيس ما أثبتّه لا ما تظنّه.",
            "جوائز بقيمة ١٠٠,٠٠٠ جنيه، ومقعد احتضان، ودخول مضمون لمسار "
            "المنافسة في تكني سميت 2027.",
        ],
        "reassurance": "المشاركة مجانية. فكرتك تظل ملكك. ولا يختار الفائزين برنامج آلي.",
    },

    "blocks": [
        ("h", "ما هي المهمة صفر"),
        ("p",
         "«المهمة صفر» تحدٍّ وطني مفتوح لرواد الأعمال الشباب في مصر. المشاركة فيه ليست "
         "بعرض تقديمي، بل بإنجاز: تُكمل مهام منصة StartPad الخمس عشرة خلال شهر واحد، "
         "من تحليل المشكلة حتى الانطلاق إلى السوق. من يُكملها جميعًا يدخل التقييم، "
         "وأفضل عشرة يعرضون مشاريعهم أمام لجنة تحكيم في يوم العرض النهائي."),
        ("p",
         "أُطلق التحدي من على مسرح تكني سميت الإسكندرية، وتنظّمه StartPad التابعة "
         "لمجموعة GrowthLabs."),

        ("h", "التواريخ"),
        ("cal", [
            ("21 سبتمبر", "فتح التسجيل", "التسجيل مجاني عبر startpad.me"),
            ("3–5 أكتوبر", "الإطلاق من الإسكندرية",
             "جناح التحدي طوال أيام القمة، وورشة «المهمة الأولى مباشرة»"),
            ("4 أكتوبر", "بدء المهام", "تُفتح المهام الخمس عشرة لجميع المسجَّلين"),
            ("4 نوفمبر", "الموعد النهائي للتسليم", "11:59 مساءً بتوقيت القاهرة — لا تمديد"),
            ("5–12 نوفمبر", "التقييم", "فرز آلي، ثم لجنة بشرية، ثم تحقق هاتفي"),
            ("أواخر نوفمبر", "يوم العرض والجوائز", "عشرة عروض، وثلاثة فائزين"),
        ]),

        ("h", "من يحق له المشاركة"),
        ("t", ["الشرط", "التفصيل"], [
            ["العمر", "من 18 إلى 30 عامًا في تاريخ إغلاق التسجيل"],
            ["الإقامة", "مقيم في جمهورية مصر العربية"],
            ["الفريق", "من فرد واحد إلى أربعة، مع قائد واحد مُسمّى يملك الحساب"],
            ["مرحلة المشروع",
             "بدون شركة مسجَّلة، وبدون تمويل خارجي، وبدون إيرادات — هذا تحدٍّ لمن لم "
             "يبدأ بعد"],
            ["عدد المشاركات", "مشاركة واحدة لكل شخص"],
            ["رسوم الاشتراك", "لا توجد. المشاركة مجانية بالكامل"],
        ]),
        ("p",
         "لا يحق المشاركة لموظفي StartPad وGrowthLabs وتكني وأفراد أسرهم المباشرين، "
         "ولا لأعضاء لجنة التحكيم."),

        ("h", "كيف تشارك"),
        ("n", [
            "سجّل عبر startpad.me — بريد إلكتروني ورقم هاتف وبيانات أساسية.",
            "أنشئ حسابك وابدأ المهمة الأولى.",
            "أكمل المهام الخمس عشرة قبل الموعد النهائي.",
            "اضغط «تسليم نهائي». لا تُقيَّم المشاركة قبل التسليم، حتى لو اكتملت المهام.",
        ]),

        ("h", "الشهر: أربعة أسابيع"),
        ("t", ["الأسبوع", "المهام", "نقطة المراجعة", "الجلسة المباشرة"], [
            ["الأول\n4–11 أكتوبر", "1–5 · تحليل المشكلة حتى اختيار الفكرة",
             "بيان مشكلة مدعوم بـ 5 مقابلات موثَّقة", "«كيف تُجري مقابلة مع شخص لا تعرفه»"],
            ["الثاني\n12–18 أكتوبر", "6–8 · وصف الفكرة حتى نموذج العمل",
             "نموذج عمل مكتمل", "«نموذج عملك يجب أن ينبع من أدلتك»"],
            ["الثالث\n19–26 أكتوبر", "9–12 · النموذج الأولي حتى التحقق من السوق",
             "نموذج أولي تفاعلي جُرِّب مع 5 مستخدمين", "«نموذج أولي بلا برمجة، في عطلة أسبوع»"],
            ["الرابع\n27 أكتوبر – 4 نوفمبر", "13–15 · المنتج الأدنى حتى الانطلاق للسوق",
             "التسليم النهائي", "«منتج أدنى يدوي، وكيف تعرض في ثلاث دقائق»"],
        ]),
        ("p",
         "نقاط المراجعة ليست استبعادًا. من تأخّر يستطيع اللحاق والتسليم في موعده. "
         "وظيفتها أن تمنحك إيقاعًا أسبوعيًا واضحًا، وأن تُظهر لك موقعك على لوحة المتصدرين."),

        ("h", "ما الذي يُحتسب إنجازًا"),
        ("p",
         "أربع مهام تحتاج تعريفًا دقيقًا حتى لا يظن أحد أن المطلوب بناء تطبيق كامل في "
         "شهر. هذا ما نقبله — وهو ما يفعله المؤسس الرشيق في هذه المرحلة فعلًا:"),
        ("t", ["المهمة", "يُقبل", "غير مطلوب"], [
            ["9 · بناء النموذج الأولي",
             "نموذج تفاعلي (Figma أو أي أداة بلا برمجة)، أو نموذج ورقي مصوَّر، أو عرض "
             "مُخطَّط — مع عرضه على 5 أشخاص على الأقل",
             "أي كود مكتوب"],
            ["13 · بناء المنتج الأدنى",
             "منتج أدنى يدوي: صفحة هبوط بتسجيلات حقيقية، أو خدمة تُقدَّم يدويًا، أو خدمة "
             "عبر واتساب أو نموذج — مع 10 مستخدمين أو تسجيلات حقيقية على الأقل",
             "منتج منشور، أو تطبيق على المتاجر، أو مدفوعات"],
            ["14 · اختبار ملاءمة المنتج للسوق",
             "اختبار إشارة طلب على 20 مستخدمًا مستهدفًا: سؤال شون إيليس، أو تحويل طلب "
             "مسبق أو قائمة انتظار، أو اختبار نية شرائية",
             "درجة ملاءمة حقيقية — لا أحد يحقق ملاءمة المنتج للسوق في أربعة أسابيع، "
             "ولن نطلب منك تقييم نفسك من عشرة"],
            ["15 · الانطلاق إلى السوق",
             "خطة 90 يومًا بقناة واحدة محددة وميزانية وهدف — مع اختبار قناة واحدة فعليًا "
             "خلال الشهر",
             "حملات منفَّذة أو إنفاق إعلاني"],
        ]),

        ("h", "كيف تُقيَّم المشاركات"),
        ("p",
         "التقييم مصمَّم على افتراض أن البعض سيحاول الكتابة لإرضاء المُقيِّم الآلي بدل "
         "التحدث إلى عملاء حقيقيين. لذلك:"),
        ("n", [
            "التقييم الآلي يفرز ولا يحكم. يُمرّر نحو 25% من المشاركات إلى المراجعة "
            "البشرية، ولا يختار الفائزين.",
            "الأدلة مطلوبة كسجلات لا كنصوص: كل مقابلة تُسجَّل باسم أول ومدينة وتاريخ "
            "وقناة تواصل وإقرار موافقة. بلا سجل، لا درجة على هذا السؤال.",
            "نتصل هاتفيًا بعيّنة عشوائية (10%) من الأشخاص الذين قابلهم المتأهلون "
            "للنهائيات، للتأكد من أن المقابلة جرت فعلًا.",
            "نفحص التكرار والتشابه بين المشاركات.",
            "لجنة بشرية تقيّم القائمة القصيرة دون معرفة الأسماء أو الجامعات.",
            "العرض المباشر هو الفيصل: ثلاث دقائق عرض، وأربع دقائق أسئلة.",
        ]),

        ("h", "معايير التقييم المعلنة"),
        ("t", ["المعيار", "الوزن", "ما الذي يمنح الدرجة"], [
            ["قوة الأدلة", "30%",
             "محادثات حقيقية مع أشخاص حقيقيين، موثَّقة — وكم غيّرت إجاباتهم رأيك"],
            ["ما بنيته واختبرته", "20%",
             "نموذج أولي ومنتج أدنى يدوي وُضعا فعلًا أمام مستخدمين، وماذا كانت النتيجة"],
            ["عمق إنجاز المهام", "20%", "خمس عشرة مهمة مُجابة بعمق، لا خمس عشرة إجابة من سطر"],
            ["وضوح المشكلة وتماسك النموذج", "15%",
             "شخص محدد بمشكلة محددة، ونموذج عمل ينبع من الأدلة لا يسبقها"],
            ["العرض والإجابات", "15%", "في النهائيات فقط: الوضوح تحت الأسئلة"],
        ]),

        ("h", "الجوائز"),
        ("t", ["المركز", "الجائزة النقدية", "ما هو أهم من النقود"], [
            ["الأول", "50,000 جنيه",
             "مقعد في دفعة الاحتضان القادمة لدى GrowthLabs · دخول مضمون لمسار المنافسة "
             "في تكني سميت 2027 · مساحة عرض في قمة 2027 · ست جلسات إرشاد"],
            ["الثاني", "30,000 جنيه",
             "دخول مضمون لمسار المنافسة 2027 · أربع جلسات إرشاد · تذاكر قمة 2027"],
            ["الثالث", "20,000 جنيه", "أربع جلسات إرشاد · تذاكر قمة 2027"],
            ["العشرة الأوائل", "—",
             "العرض على مسرح تكني · ملف موثَّق على Startup Gate · جلسة إرشاد"],
            ["كل من أكمل المهام", "—",
             "شهادة موقَّعة من تكني وStartPad، وملف أدلة موثَّق دائم"],
        ]),
        ("p",
         "تُدفع الجوائز النقدية بتحويل بنكي لقائد الفريق المُسمّى، مقابل بطاقة رقم قومي "
         "سارية وإيصال موقَّع. توزيع الجائزة داخل الفريق مسؤولية الفريق وحده. وقد تخضع "
         "الجوائز لأي استقطاعات يفرضها القانون المصري."),
        ("p",
         "تُمنح كذلك جائزتان تقديريتان: «أفضل جامعة» و«أفضل محافظة»، وتُحتسبان بنسبة "
         "الإكمال لا بعدد الفائزين."),

        ("h", "فكرتك ملكك — دائمًا"),
        ("p",
         "كل ما ترفعه على المنصة يظل ملكك أنت. لا تتنازل عن أي حق من حقوق الملكية "
         "الفكرية بمشاركتك، ولا يوجد في هذه القواعد حق أولوية أو أفضلية لنا أو لشركائنا "
         "في الاستثمار في مشروعك أو الحصول على حصة فيه."),
        ("p",
         "ما نطلبه فقط هو إذن باستخدام اسمك وصورتك واسم مشروعك ووصفه العام في التغطية "
         "الإعلامية للتحدي ونتائجه. ولا نشارك بيانات تواصلك مع أي راعٍ أو طرف ثالث."),

        ("h", "بياناتك"),
        ("p",
         "نجمع الاسم وتاريخ الميلاد والبريد الإلكتروني ورقم الهاتف والمحافظة والجامعة "
         "(اختياري)، وإجاباتك على المهام. تخضع المعالجة لقانون حماية البيانات الشخصية "
         "المصري رقم 151 لسنة 2020."),
        ("b", [
            "الغرض: إدارة التحدي، والتواصل معك، والتقييم، وإعلان النتائج.",
            "مدة الاحتفاظ: 24 شهرًا من تاريخ يوم العرض، ثم تُحذف بيانات التواصل.",
            "بيانات من قابلتهم: تُستخدم للتحقق فقط، ولا تُستخدم للتسويق إطلاقًا — "
            "ويجب أن تحصل على موافقتهم قبل تسجيل بياناتهم.",
            "حقوقك: الاطلاع والتصحيح والحذف وسحب الموافقة، عبر بريد التحدي.",
        ]),

        ("h", "أسباب الاستبعاد"),
        ("b", [
            "تقديم بيانات شخصية غير صحيحة، أو عدم استيفاء شروط الأهلية.",
            "اختلاق مقابلات أو أدلة — وهذا هو السبب الأول والأخطر.",
            "نسخ مشاركة أخرى أو محتوى منشورًا دون إسناد.",
            "أكثر من مشاركة واحدة للشخص نفسه.",
            "إساءة معاملة المشاركين الآخرين أو فريق التحدي أو لجنة التحكيم.",
        ]),
        ("p", "قرار الاستبعاد يُبلَّغ كتابةً مع السبب، ويخضع لحق التظلّم أدناه."),

        ("h", "التظلّم"),
        ("p",
         "لك أن تتظلّم من النتيجة أو من قرار الاستبعاد خلال 72 ساعة من إعلانه، برسالة "
         "إلى بريد التحدي تشرح الأساس. يُنظر التظلّم من شخص لم يشارك في القرار الأصلي، "
         "ويُرد عليه خلال 7 أيام. قرار لجنة التحكيم في الجولة النهائية نهائي."),

        ("h", "تعديل القواعد"),
        ("p",
         "قد نضطر لتعديل هذه القواعد. أي تعديل يُنشر على الصفحة نفسها مع تاريخه ويُرسل "
         "إلى كل المسجَّلين. ولن يُعدَّل معيار تقييم أو شرط إكمال بعد بدء التقييم — "
         "وإن اقتضى الأمر تخفيف شرط الإكمال، يُعلن ذلك مبكرًا وللجميع، لا عند التحكيم."),

        ("h", "أسئلة متكررة"),
        ("t", ["السؤال", "الإجابة"], [
            ["هل أحتاج فكرة جاهزة قبل التسجيل؟",
             "لا. المهام من 1 إلى 5 مصمَّمة لمن يصل بلا فكرة محددة."],
            ["هل أحتاج أن أعرف البرمجة؟", "لا. ولا سطر واحد. راجع «ما الذي يُحتسب إنجازًا»."],
            ["هل يمكنني المشاركة وأنا طالب؟", "نعم، وهذا هو الجمهور الأساسي للتحدي."],
            ["هل يمكن لفريقي أن يكون من محافظات مختلفة؟", "نعم."],
            ["ماذا لو تأخرت أسبوعًا؟",
             "تستطيع اللحاق. لا يوجد استبعاد قبل الموعد النهائي."],
            ["هل تأخذون حصة من شركتي؟", "لا. لا حصة ولا حق أولوية ولا أي التزام."],
            ["هل التقييم بالذكاء الاصطناعي وحده؟",
             "لا. التقييم الآلي يفرز فقط؛ لجنة بشرية تقيّم القائمة القصيرة، والعرض "
             "المباشر هو الفيصل."],
        ]),

        ("h", "التواصل"),
        ("p", "بريد التحدي: [البريد الإلكتروني] · واتساب: [الرقم] · startpad.me"),
    ],
}

# --------------------------------------------------------------------------- EN

EN = {
    "lang": "en",
    "dir": "ltr",
    "name": "Mission Zero",
    "tagline": "From an idea to an investable company, in one month",
    "doc_title": "Competition rules and judging criteria",
    "version_line": "Version " + VERSION,

    "hero": {
        "eyebrow": "In partnership with Techne Summit Alexandria",
        "h1": "Mission Zero",
        "sub": "A national challenge for young founders: finish all fifteen StartPad "
               "missions in one month, and earn the stage.",
        "cta": "Enter free",
        "points": [
            "15 guided missions that take you from “I have an idea” to “I have "
            "evidence”.",
            "120+ tools, and scoring that measures what you proved rather than what you "
            "believe.",
            "EGP 100,000 in prizes, an incubation seat, and guaranteed entry to the "
            "Techne Summit 2027 competition track.",
        ],
        "reassurance": "Free to enter. Your idea stays yours. And no software picks the "
                       "winners.",
    },

    "blocks": [
        ("h", "What Mission Zero is"),
        ("p",
         "Mission Zero is a national challenge open to young founders in Egypt. You do "
         "not enter with a pitch — you enter by finishing. Complete all fifteen StartPad "
         "missions within one month, from problem analysis through to go-to-market. "
         "Everyone who finishes is judged; the best ten pitch to a panel at Demo Day."),
        ("p",
         "The challenge is launched from the Techne Summit Alexandria stage and run by "
         "StartPad, a GrowthLabs company."),

        ("h", "Dates"),
        ("cal", [
            ("21 Sept", "Registration opens", "Free, at startpad.me"),
            ("3–5 Oct", "Launch, in Alexandria",
             "Challenge stand across all three summit days, plus the “Mission 1 "
             "Live” workshop"),
            ("4 Oct", "Missions open", "All fifteen unlock for every registered entrant"),
            ("4 Nov", "Submission deadline", "23:59 Cairo time — no extension"),
            ("5–12 Nov", "Judging",
             "Automated filter, then a human panel, then verification calls"),
            ("Late Nov", "Demo Day and prizes", "Ten pitches, three winners"),
        ]),

        ("h", "Who can enter"),
        ("t", ["Rule", "Detail"], [
            ["Age", "18 to 30 on the closing date"],
            ["Residency", "Resident in the Arab Republic of Egypt"],
            ["Team", "One to four people, with one named lead who holds the account"],
            ["Stage",
             "No registered company, no external funding, no revenue — this challenge is "
             "for people who have not started yet"],
            ["Entries", "One per person"],
            ["Entry fee", "None. Free to enter, always"],
        ]),
        ("p",
         "Employees of StartPad, GrowthLabs and Techne, their immediate families, and "
         "members of the judging panel may not enter."),

        ("h", "How to enter"),
        ("n", [
            "Register at startpad.me — email, phone and a few basic details.",
            "Create your account and start Mission 1.",
            "Complete all fifteen missions before the deadline.",
            "Press “Final submission”. Nothing is judged until you submit, even "
            "if every mission is finished.",
        ]),

        ("h", "The month: four weeks"),
        ("t", ["Week", "Missions", "Checkpoint", "Live clinic"], [
            ["1\n4–11 Oct", "1–5 · problem analysis to idea selection",
             "A problem statement backed by 5 logged interviews",
             "“How to interview a stranger”"],
            ["2\n12–18 Oct", "6–8 · idea description to business model",
             "A completed Business Model Canvas",
             "“Your canvas has to follow from your evidence”"],
            ["3\n19–26 Oct", "9–12 · prototype to market validation",
             "A clickable prototype tested with 5 users",
             "“Prototyping without code, in a weekend”"],
            ["4\n27 Oct – 4 Nov", "13–15 · MVP to go-to-market", "Final submission",
             "“Manual MVPs, and how to pitch in three minutes”"],
        ]),
        ("p",
         "Checkpoints are not eliminations. If you fall behind you can catch up and still "
         "submit on time. They exist to give the month a visible weekly rhythm and to show "
         "you where you stand on the leaderboard."),

        ("h", "What counts as complete"),
        ("p",
         "Four missions need a precise definition so nobody thinks they must build a "
         "finished app in a month. Here is what we accept — and it is what a lean founder "
         "should actually be doing at this stage:"),
        ("t", ["Mission", "Accepted", "Not required"], [
            ["9 · Build Prototype",
             "A clickable prototype (Figma or any no-code builder), a photographed paper "
             "prototype, or a scripted walkthrough — shown to at least 5 people",
             "Any written code"],
            ["13 · Build MVP",
             "A manual MVP: a landing page with real sign-ups, a concierge service "
             "delivered by hand, or a WhatsApp or form-based service — with at least 10 "
             "real users or sign-ups",
             "A deployed product, an app store listing, payments"],
            ["14 · Product-Market Fit Test",
             "A demand-signal test on 20 target users: the Sean Ellis question, a "
             "pre-order or waitlist conversion, or a paid-intent test",
             "A real PMF score — nobody has product-market fit in four weeks, and we will "
             "not ask you to rate yourself out of ten"],
            ["15 · Go to Market",
             "A 90-day plan with one named channel, a budget and a target — plus one "
             "channel actually tested during the month",
             "Executed campaigns or ad spend"],
        ]),

        ("h", "How entries are judged"),
        ("p",
         "Judging is built on the assumption that some entrants will write for the "
         "automated scorer instead of talking to real customers. So:"),
        ("n", [
            "Automated scoring filters, it does not decide. It passes roughly 25% of "
            "entries to human review and picks no winners.",
            "Evidence is required as logs, not prose: every interview carries a first "
            "name, city, date, channel and a consent confirmation. No log, no marks on "
            "that question.",
            "We telephone a random 10% of the people interviewed by finalists, to confirm "
            "the interview actually happened.",
            "We check for duplicate and templated entries.",
            "A human panel scores the shortlist without names or universities attached.",
            "The live pitch decides: three minutes to present, four minutes of questions.",
        ]),

        ("h", "The published rubric"),
        ("t", ["Pillar", "Weight", "What earns the marks"], [
            ["Evidence", "30%",
             "Real conversations with real people, logged — and how much their answers "
             "changed your mind"],
            ["Built and tested", "20%",
             "A prototype and a manual MVP actually put in front of users, and what came "
             "back"],
            ["Depth of mission completion", "20%",
             "Fifteen missions answered at depth, not fifteen one-line answers"],
            ["Problem clarity and model coherence", "15%",
             "A specific person with a specific problem, and a business model that follows "
             "from the evidence rather than preceding it"],
            ["Pitch and answers", "15%", "Finals only: clarity under questioning"],
        ]),

        ("h", "Prizes"),
        ("t", ["Place", "Cash", "What matters more"], [
            ["First", "EGP 50,000",
             "A seat in the next GrowthLabs incubation cohort · guaranteed entry to the "
             "Techne Summit 2027 competition track · exhibition space at Summit 2027 · "
             "six mentor sessions"],
            ["Second", "EGP 30,000",
             "Guaranteed 2027 track entry · four mentor sessions · Summit 2027 passes"],
            ["Third", "EGP 20,000", "Four mentor sessions · Summit 2027 passes"],
            ["Top ten", "—",
             "Pitch on a Techne stage · a verified profile on Startup Gate · one mentor "
             "session"],
            ["Everyone who finishes", "—",
             "A certificate co-signed by Techne and StartPad, and a permanent verified "
             "evidence profile"],
        ]),
        ("p",
         "Cash prizes are paid by bank transfer to the named team lead, against a valid "
         "national ID and a signed receipt. How a team splits its prize is the team's own "
         "business. Prizes may be subject to any deductions Egyptian law requires."),
        ("p",
         "Two further recognitions are awarded on completion rate rather than on winners: "
         "Best University and Best Governorate."),

        ("h", "Your idea is yours — always"),
        ("p",
         "Everything you put on the platform remains yours. Entering assigns no "
         "intellectual property, and nothing in these rules gives us or our partners any "
         "right of first refusal, any option to invest, or any claim to equity in what you "
         "build."),
        ("p",
         "All we ask is permission to use your name, photograph, and your project's name "
         "and general description in coverage of the challenge and its results. We do not "
         "share your contact details with any sponsor or third party."),

        ("h", "Your data"),
        ("p",
         "We collect your name, date of birth, email, phone number, governorate, "
         "university (optional), and your mission answers. Processing is governed by "
         "Egypt's Personal Data Protection Law 151 of 2020."),
        ("b", [
            "Purpose: running the challenge, contacting you, judging, and announcing "
            "results.",
            "Retention: 24 months from Demo Day, after which contact details are deleted.",
            "People you interviewed: used for verification only, never for marketing — and "
            "you must obtain their consent before logging their details.",
            "Your rights: access, correction, deletion and withdrawal of consent, through "
            "the challenge email.",
        ]),

        ("h", "Grounds for disqualification"),
        ("b", [
            "False personal details, or failing the eligibility rules.",
            "Fabricated interviews or evidence — the first and most serious ground.",
            "Copying another entry, or published material, without attribution.",
            "More than one entry by the same person.",
            "Abuse of other entrants, the challenge team, or the judges.",
        ]),
        ("p",
         "Disqualification is communicated in writing with the reason, and is subject to "
         "the appeal below."),

        ("h", "Appeals"),
        ("p",
         "You may appeal a result or a disqualification within 72 hours of it being "
         "announced, by email to the challenge address, setting out the grounds. The "
         "appeal is reviewed by someone who took no part in the original decision and "
         "answered within 7 days. The panel's decision in the final round is final."),

        ("h", "Changes to these rules"),
        ("p",
         "We may have to change these rules. Any change is published on this page with its "
         "date and sent to every registered entrant. No judging criterion or completion "
         "requirement will be changed once judging has begun — and if a completion "
         "requirement has to be relaxed, it will be announced early and to everyone, never "
         "at judging time."),

        ("h", "Frequently asked"),
        ("t", ["Question", "Answer"], [
            ["Do I need an idea before I register?",
             "No. Missions 1 to 5 are designed for people who arrive without one."],
            ["Do I need to know how to code?",
             "No — not one line. See “What counts as complete”."],
            ["Can I enter as a student?", "Yes. Students are the core audience."],
            ["Can my team be spread across governorates?", "Yes."],
            ["What if I fall a week behind?",
             "You can catch up. Nobody is eliminated before the deadline."],
            ["Do you take equity in my company?",
             "No. No equity, no right of first refusal, no obligation of any kind."],
            ["Is it judged by AI alone?",
             "No. Automated scoring only filters; a human panel scores the shortlist, and "
             "the live pitch decides."],
        ]),

        ("h", "Contact"),
        ("p", "Challenge email: [EMAIL] · WhatsApp: [NUMBER] · startpad.me"),
    ],
}

VERSIONS = [AR, EN]
