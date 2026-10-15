(function(){
  var LS=window.localStorage, page=document.body.dataset.page;
  function get(k,d){try{return JSON.parse(LS.getItem(k))||d}catch(e){return d}}
  function set(k,v){try{LS.setItem(k,JSON.stringify(v))}catch(e){}}
  function toast(msg){
    var t=document.createElement('div');t.textContent=msg;
    t.style.cssText='position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#0B132B;color:#fff;padding:12px 22px;border-radius:12px;border:1px solid #D97706;z-index:9999;font:500 14px "IBM Plex Sans Arabic",sans-serif;box-shadow:0 12px 32px rgba(0,0,0,.3)';
    document.body.appendChild(t);setTimeout(function(){t.remove()},2600);
  }
  function txt(el){return (el.textContent||'').replace(/\s+/g,' ').trim()}
  function renderBadge(){
    var n=get('masar_cart',[]).length;
    document.querySelectorAll('a[href="checkout.html"] span').forEach(function(s){
      if(/^\d+$/.test(txt(s))) s.textContent=n;
    });
  }
  function addToCart(){var c=get('masar_cart',[]);c.push({id:Date.now(),from:page});set('masar_cart',c);renderBadge();}
  document.addEventListener('DOMContentLoaded',function(){
    renderBadge();
    var f=document.querySelector('footer');
    if(f&&['dashboard','copilot','kpi','admin','admin-products','admin-users'].indexOf(page)<0){
      var d=document.createElement('div');d.style.cssText='text-align:center;padding:12px;font-size:13px;opacity:.8';
      d.innerHTML='<a href="journey.html" style="margin:0 10px;color:#F59E0B">رحلة المستخدم</a><a href="brand.html" style="margin:0 10px;color:#F59E0B">دليل الهوية</a><a href="legal.html" style="margin:0 10px;color:#F59E0B">الشروط والخصوصية</a>';
      f.appendChild(d);
    }
    if(page==='index'||page==='store'){
      document.querySelectorAll('h3,h4').forEach(function(h){
        var card=h.closest('article')||h.parentElement;
        if(card&&card.querySelector('button')){h.style.cursor='pointer';h.addEventListener('click',function(){location.href='product.html'});}
      });
    }
  });
  document.addEventListener('click',function(e){
    var b=e.target.closest('button,a[href="#"]');if(!b)return;
    var t=txt(b);
    if(/(إضافة إلى السلة|شراء وتحميل|تحميل فوري|شراء وتنزيل|شراء النموذج)/.test(t)&&['checkout','dashboard','admin-products'].indexOf(page)<0){
      e.preventDefault();addToCart();
      if(/ومتابعة|فور|الآن|شراء/.test(t)){location.href='checkout.html'}else toast('تمت الإضافة إلى السلة');
      return;
    }
    if(page==='login'&&/تسجيل الدخول إلى لوحة التحكم|الدخول السريع|Google|LinkedIn/.test(t)){e.preventDefault();location.href='dashboard.html';return}
    if(/إتمام الدفع الآمن/.test(t)){e.preventDefault();set('masar_cart',[]);location.href='success.html';return}
    if(page==='index'&&/معاينة حية/.test(t)){location.href='product.html';return}
    if(/طلب استشارة وبناء نموذج خاص/.test(t)){location.href='about.html';return}
    if(/بدء تجربة لوحة المؤشرات/.test(t)){location.href='login.html';return}
    if(/انضم إلى القائمة التنفيذية|تأكيد الاشتراك/.test(t)){e.preventDefault();toast('تم تسجيل اشتراكك في القائمة التنفيذية');return}
    if(/إرسال طلب الاستشارة/.test(t)){e.preventDefault();toast('تم إرسال طلبك. سيتواصل معك مستشار مسار خلال 24 ساعة');return}
    if(/نسخ المفتاح/.test(t)){var k=b.parentElement&&b.parentElement.textContent.match(/MSR-[A-Z0-9-]+/);if(k&&navigator.clipboard)navigator.clipboard.writeText(k[0]);toast('تم نسخ مفتاح الترخيص');return}
    if(/^print/.test(t)){window.print();return}
    if(/تحميل|تنزيل|تصدير|Google Drive|Dropbox/.test(t)){e.preventDefault();toast('جارٍ تجهيز الملف… (نسخة تجريبية)');return}
    if(/حفظ|تطبيق|اعتماد ونشر|مزامنة|تحديث السلة/.test(t)&&/dashboard|copilot|kpi|admin/.test(page||'')){toast('تم الحفظ بنجاح')}
  });
})();
