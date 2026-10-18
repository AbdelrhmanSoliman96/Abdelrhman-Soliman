# منصة مسار (Masar)

موقع ثابت (Static) كامل مبني من تصاميم Stitch دون أي تغيير في التصميم. كل صفحة هي نفس الـ HTML الأصلي، مع ربط الروابط بين الصفحات وطبقة تنقل مشتركة في `assets/site.js`.

## التشغيل
```
python3 -m http.server 8000   # ثم افتح http://localhost:8000
```
تحتاج الصفحات اتصالاً بالإنترنت لتحميل Tailwind CDN والخطوط (كما في التصميم الأصلي).

## الصفحات
- **الواجهة العامة:** `index` · `store` · `product` · `compare` · `knowledge` · `article` · `trust-wall` · `verify-license` · `help-center` · `privacy` · `about` · `404`
- **الشراء:** `cart-added` → `checkout` / `guest-checkout` → `payment-processing` → `order-confirmed` (و`payment-failed`)
- **الحساب:** `login` · `register` → `onboarding` → `dashboard`
- **المستثمر:** `dashboard` · `valuation` · `kpi-entry` · `billing` · `company-profile` · `executive-ops` · `ai-assistant` · `ai-generating` · `pitch-deck` · `data-room` · `vdr-upload`
- **الاستشارات:** `advisory-booking` · `consultant-portal` · `waiting-lobby` → `live-room` → `session-evaluation`
- **الإدارة:** `admin-sales` · `admin-products` · `admin-add-model` · `admin-reports` · `admin-disputes` · `admin-licenses`
- **الشركاء والمطورون:** `partner-portal` · `developers-api`
- **الهوية:** `brand-guide` · `assets/masar-logo.svg`
