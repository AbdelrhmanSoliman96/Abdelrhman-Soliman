/* Masar — shared navigation & flow layer.
   Pages keep their original markup/styles; this file only wires up links,
   buttons and the multi-step flows (login, registration, checkout, session). */
(function () {
  'use strict';

  var page = document.body.getAttribute('data-page') || '';
  var go = function (url, delay) {
    if (delay) setTimeout(function () { location.href = url; }, delay);
    else location.href = url;
  };

  // Text of an element without Material-icon ligature names noise (kept simple: match substrings).
  var txt = function (el) { return (el.textContent || '').replace(/\s+/g, ' ').trim(); };

  // ---- Rules: [regex on element text, destination] (first match wins) ----
  var LINK_RULES = [
    [/تسجيل الخروج|logout/, 'login.html'],
    [/طلب انضمام مستثمر|إنشاء حساب جديد|إنشاء حساب$/, 'register.html'],
    [/تسجيل الدخول الفوري|تسجيل الدخول/, 'login.html'],
    [/نسيت كلمة المرور|الدعم|المساعدة|الأسئلة الشائعة|اتصال/, 'help-center.html'],
    [/شروط الاستخدام|شروط الخدمة|الشروط والأحكام|الإفصاح|الخصوصية|الامتثال|التراخيص والامتثال|PDPL|بروتوكول الأمان|سياسة الجودة|الاعتماد التنظيمي|الحوكمة/, 'privacy.html'],
    [/حجز جلسة|طلب مستشار|عرض جدول المواعيد|جدولة جلسة|جدولة موعد/, 'advisory-booking.html'],
    [/محادثة مشفرة/, 'help-center.html'],
    [/الانتقال إلى لوحة تحكم المستثمر|لوحة التحكم والمؤشرات|الرجوع إلى قمرة/, 'dashboard.html'],
    [/استعراض محضر الجلسة|VDR/, 'data-room.html'],
    [/إلغاء العملية والعودة/, 'dashboard.html'],
    [/عرض مكتبة الأبحاث|قراءة التقرير|دليل جولات|كيف تبني|مقارنة بين صكوك|أهم 10|استراتيجيات تسعير|الامتثال للأنظمة|كيف تصيغ|دراسة المعايير|قطاع التقنية المالية|التطوير العقاري|الذكاء الاصطناعي والحوكمة/, 'article.html'],
    [/استعراض النموذج|استعراض نموذج|استعراض حاسبة|عرض كل النماذج|تصفح متجر|متجر النماذج|دراسات الجدوى|نماذج التقييم|هياكل التدفقات|قوالب العروض|حاسبة العائد|مولّد دراسات|محاكي جولات|مصفوفة مؤشرات/, 'store.html'],
    [/حفظ ومتابعة/, 'dashboard.html'],
    [/عرض سجل كافة المعاملات|سجل السداد/, 'billing.html'],
    [/إدارة كافة الإشعارات/, 'company-profile.html']
  ];

  var BUTTON_RULES = [
    // purchase flow
    [/متابعة الدفع السريع/, 'guest-checkout.html'],
    [/إتمام الدفع|الدفع الآمن|الدفع الفوري|متابعة الدفع|إعادة تفويض|الدفع عبر Apple Pay/, 'payment-processing.html'],
    [/شراء وتحميل|شراء فوري|شراء النموذج|اقتنِ|امتلاك النموذج|تأكيد الاشتراك الاستراتيجي/, 'checkout.html'],
    [/إضافة إلى السلة|أضف إلى السلة/, 'cart-added.html'],
    [/بدء محادثة|محادثة$|طلب استشارة وبناء نموذج خاص|حجز استشارة هاتفية/, 'help-center.html'],
    // sessions
    [/الدخول لغرفة الاستشارة/, 'waiting-lobby.html'],
    [/انضمام الآن لغرفة الاستشارة/, 'live-room.html'],
    [/^call_end$/, 'session-evaluation.html'],
    [/استعراض ملفات VDR|إيداع في VDR|الانتقال المباشر إلى غرفة البيانات|folder_shared/, 'data-room.html'],
    // admin
    [/إضافة نموذج مالي|إضافة نموذج|رفع ملف دراسة/, 'admin-add-model.html'],
    [/اعتماد ونشر في المتجر|نشر النموذج الآن/, 'admin-products.html'],
    // misc
    [/تقييم شركات SaaS|عقود استثمار ملائكي|نموذج التدفق النقدي DCF/, 'store.html'],
    [/ملف الإكسل|فحص النموذج المالي التفاعلي/, 'valuation.html']
  ];

  var firstMatch = function (rules, s) {
    for (var i = 0; i < rules.length; i++) if (rules[i][0].test(s)) return rules[i][1];
    return null;
  };

  // Links that still point to "#": resolve by text, otherwise make them inert (no jump to top).
  document.querySelectorAll('a[href="#"]').forEach(function (a) {
    var dest = firstMatch(LINK_RULES, txt(a));
    if (dest) a.setAttribute('href', dest);
    else a.addEventListener('click', function (e) { e.preventDefault(); });
  });
  // In-page anchors (#section-1 …) are kept as-is.

  // Buttons without their own behaviour: navigate when a rule matches.
  document.querySelectorAll('button').forEach(function (b) {
    if (b.hasAttribute('onclick') || (b.type === 'submit' && b.form)) return;
    var dest = firstMatch(BUTTON_RULES, txt(b));
    if (!dest) return;
    var wrap = b.closest('a');
    if (wrap) { if (wrap.getAttribute('href') === '#' || !wrap.getAttribute('href')) wrap.setAttribute('href', dest); return; }
    b.addEventListener('click', function () { go(dest, 250); });
  });

  // Footer "© / logo" brand links and product cards in the store open the product page.
  if (page === 'store' || page === 'index') {
    document.querySelectorAll('h3, h4').forEach(function (h) {
      var card = h.closest('article, [class*="rounded-xl"]');
      if (!card || card.dataset.wired) return;
      var hasBuy = /شراء وتحميل|معاينة/.test(txt(card));
      if (!hasBuy) return;
      card.dataset.wired = '1';
      h.style.cursor = 'pointer';
      h.addEventListener('click', function () { go('product.html'); });
    });
  }

  // ---- Page-specific flows ----
  var after = function (name, fn) {
    var orig = window[name];
    window[name] = function () {
      var r = typeof orig === 'function' ? orig.apply(this, arguments) : undefined;
      fn.apply(this, arguments);
      return r;
    };
  };

  switch (page) {
    case 'login':
      after('simulateSignIn', function () { go('dashboard.html', 1500); });
      document.querySelectorAll('button[type="button"]').forEach(function (b) {
        if (/نفاذ|Google|LinkedIn/.test(txt(b))) b.addEventListener('click', function () { window.simulateSignIn && window.simulateSignIn(); });
      });
      break;

    case 'register':
      var rf = document.querySelector('form');
      if (rf) rf.addEventListener('submit', function (e) { e.preventDefault(); go('onboarding.html', 400); });
      document.querySelectorAll('button[type="button"]').forEach(function (b) {
        if (/نفاذ|Google|LinkedIn/.test(txt(b))) b.addEventListener('click', function () { go('onboarding.html', 300); });
      });
      break;

    case 'onboarding':
      document.querySelectorAll('button[onclick]').forEach(function (b) {
        if (/الرجوع للخطوة السابقة/.test(txt(b))) b.addEventListener('click', function () { go('register.html', 200); });
      });
      break;

    case 'payment-processing':
      // The page animates a 3-second countdown; continue to the confirmation screen afterwards.
      go('order-confirmed.html', 5200);
      break;

    case 'ai-generating':
      go('ai-assistant.html', 14000);
      break;

    case 'checkout':
    case 'guest-checkout':
      document.querySelectorAll('button').forEach(function (b) {
        if (/طلب فاتورة تحويل/.test(txt(b))) b.addEventListener('click', function () { go('payment-processing.html', 250); });
      });
      break;

    case 'waiting-lobby':
      var jb = document.getElementById('join-room-btn');
      if (jb) jb.addEventListener('click', function () { go('live-room.html', 1400); });
      break;

    case 'session-evaluation':
      document.querySelectorAll('button').forEach(function (b) {
        if (/تم الاعتماد والتوقيع الرقمي/.test(txt(b))) b.addEventListener('click', function () { go('dashboard.html', 1500); });
      });
      break;

    case 'live-room':
      document.querySelectorAll('button').forEach(function (b) {
        if (/توثيق المحضر واعتماده/.test(txt(b))) b.addEventListener('click', function () { go('session-evaluation.html', 600); });
      });
      break;

    case '404':
      var si = document.querySelector('input[type="text"]');
      var sb = Array.prototype.filter.call(document.querySelectorAll('button'), function (b) { return /بحث فوري/.test(txt(b)); })[0];
      if (sb && si) sb.addEventListener('click', function () { go('knowledge.html' + (si.value.trim() ? '?q=' + encodeURIComponent(si.value.trim()) : ''), 150); });
      break;
  }
})();
