---
title: "طبقة النقل"
description: "فهم طبقة النقل الخاصة بـ I2P - أساليب الاتصال من نقطة إلى نقطة بين routers بما في ذلك NTCP2 وSSU2"
slug: "transport"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. نظرة عامة

تُشير **آلية النقل** في I2P إلى طريقة للاتصال المباشر من نقطة إلى نقطة بين routers. تضمن هذه الآليات السرّية وسلامة البيانات مع التحقق من مصادقة router.

يعمل كل بروتوكول نقل باستخدام أنماط اتصال تتضمن المصادقة، والتحكم في التدفق، والإقرارات، وقدرات إعادة الإرسال.

---

## 2. بروتوكولات النقل الحالية

يدعم I2P حالياً بروتوكولي نقل أساسيين:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport with modern encryption (as of 0.9.36)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Secure Semireliable UDP with modern encryption (as of 0.9.56)</td>
    </tr>
  </tbody>
</table>
### 2.1 بروتوكولات النقل القديمة (مهملة)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by NTCP2; removed in 0.9.62</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by SSU2; removed in 0.9.62</td>
    </tr>
  </tbody>
</table>
---

## 3. خدمات النقل

يوفر النظام الفرعي للنقل الخدمات التالية:

### 3.1 تسليم الرسائل

- تسليم موثوق لرسائل [I2NP](/docs/specs/i2np/) (تتولى وسائط النقل التعامل مع مراسلة I2NP حصريًا)
- التسليم بالترتيب **غير مضمون** على نحوٍ شامل
- اصطفاف الرسائل القائم على الأولوية

### 3.2 إدارة الاتصالات

- إنشاء الاتصالات وإغلاقها
- إدارة حدود الاتصالات مع فرض العتبات
- تتبّع حالة كل نظير
- فرض قائمة حظر النظراء بشكل آلي ويدوي

### 3.3 تهيئة الشبكة

- عناوين router متعددة لكل طبقة نقل (دعم IPv4 وIPv6 منذ الإصدار v0.9.8)
- فتح منافذ جدار الحماية عبر UPnP
- دعم اجتياز NAT (ترجمة عناوين الشبكة)/جدار الحماية
- اكتشاف عنوان IP المحلي عبر أساليب متعددة

### 3.4 الأمان

- تشفير لاتصالات نقطة-إلى-نقطة
- التحقق من صحة عناوين IP وفقًا للقواعد المحلية
- تحديد توافق الساعة (حل احتياطي عبر NTP)

### 3.5 إدارة عرض النطاق الترددي

- حدود عرض النطاق الترددي الوارد والصادر
- اختيار وسيلة النقل المثلى للرسائل الصادرة

---

## 4. عناوين النقل

يحافظ النظام الفرعي على قائمة بنقاط اتصال router:

- طريقة النقل (NTCP2, SSU2)
- عنوان IP
- رقم المنفذ
- معلمات اختيارية

يمكن أن تكون هناك عناوين متعددة لكل طريقة نقل.

### 4.1 تكوينات العناوين الشائعة

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Configuration</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hidden</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers with no published addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Firewalled</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers publishing SSU2 addresses with "introducer" peer lists for NAT traversal</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unrestricted</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers advertising both NTCP2 and SSU2 addresses on IPv4 and/or IPv6</td>
    </tr>
  </tbody>
</table>
---

## 5. اختيار النقل

يختار النظام transports (بروتوكولات النقل) لـ[رسائل I2NP](/docs/specs/i2np/) بشكل مستقل عن بروتوكولات الطبقات العليا. تستخدم عملية الاختيار **نظام مزايدة** يقدّم فيه كل transport عروضًا، حيث يفوز العرض ذو القيمة الأدنى.

### 5.1 عوامل تحديد قيمة العرض

- إعدادات تفضيلات النقل
- اتصالات النظراء القائمة
- أعداد الاتصالات الحالية مقابل قيم العتبة
- سجل محاولات الاتصال الأخيرة
- قيود حجم الرسائل
- قدرات النقل في RouterInfo الخاصة بالنظير
- مباشرة الاتصال (مباشر مقابل المعتمد على introducer، نظير وسيط للتعريف بالاتصال)
- تفضيلات النقل المعلن عنها من قِبل النظير

عمومًا، يحافظ جهازان من نوع router على اتصالات أحادية النقل بالتزامن، رغم أن اتصالات متعددة النقل المتزامنة ممكنة.

---

## 6. NTCP2

**NTCP2** (بروتوكول النقل الجديد 2) هو وسيلة النقل الحديثة المعتمدة على TCP لـ I2P، طُرحت في الإصدار 0.9.36.

### 6.1 الميزات الرئيسية

- مبني على **Noise Protocol Framework** (إطار بروتوكول للتفاوض على المفاتيح، نمط Noise_XK)
- يستخدم X25519 لتبادل المفاتيح
- يستخدم ChaCha20/Poly1305 للتشفير المصادَق
- يستخدم BLAKE2s للتجزئة
- إخفاء البروتوكول لمقاومة DPI (فحص الحزم العميق)
- حشو اختياري لمقاومة تحليل المرور

### 6.2 إنشاء الاتصال

1. **طلب الجلسة** (Alice → Bob): مفتاح X25519 مؤقت + حمولة مشفرة
2. **تم إنشاء الجلسة** (Bob → Alice): مفتاح مؤقت + تأكيد مشفر
3. **تأكيد الجلسة** (Alice → Bob): مصافحة نهائية مع RouterInfo

تُشفَّر كل البيانات اللاحقة باستخدام مفاتيح جلسة مستمدة من المصافحة.

راجع [مواصفة NTCP2](/docs/specs/ntcp2/) للتفاصيل الكاملة.

---

## 7. SSU2

**SSU2** (Secure Semireliable UDP 2) هو بروتوكول نقل حديث قائم على UDP لـ I2P، تم تقديمه في الإصدار 0.9.56.

### 7.1 الميزات الرئيسية

- يعتمد على **Noise Protocol Framework** (نمط Noise_XK)
- يستخدم **X25519** لتبادل المفاتيح
- يستخدم **ChaCha20/Poly1305** للتشفير المُصادَّق
- تسليم شبه موثوق مع إقرارات استلام انتقائية
- اجتياز NAT عبر hole punching (تقنية فتح ثغرة اتصال عبر NAT) و relay/introduction (الترحيل/التعريف)
- دعم ترحيل الاتصال
- اكتشاف MTU للمسار

### 7.2 مزايا مقارنةً بـ SSU (قديم)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU (Legacy)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 + ChaCha20/Poly1305</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Header encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (ChaCha20)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fixed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted, rotatable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Basic introduction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced hole punching + relay</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Obfuscation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved (variable padding)</td>
    </tr>
  </tbody>
</table>
انظر [مواصفة SSU2](/docs/specs/ssu2/) (بروتوكول النقل عبر UDP في I2P من الجيل الثاني) للاطلاع على التفاصيل الكاملة.

---

## 8. اجتياز NAT

كلتا وسيلتي النقل تدعمان اجتياز NAT للسماح لـ routers الموجودة خلف جدار ناري بالمشاركة في الشبكة.

### 8.1 مقدمة عن SSU2

عندما يتعذر على router استقبال الاتصالات الواردة مباشرةً:

1. ينشر router عناوين **introducer** (وسيط التعريف) في RouterInfo (معلومات router)
2. يرسل النظير المتصل طلب تعارف إلى introducer
3. يقوم introducer بتمرير معلومات الاتصال إلى router خلف جدار ناري
4. يبدأ router خلف جدار ناري اتصالاً صادراً (hole punch، فتح ثغرة عبر NAT)
5. يتم تأسيس اتصال مباشر

### 8.2 NTCP2 وجدران الحماية

يتطلب NTCP2 إمكانية استقبال اتصالات TCP الواردة. يمكن لـ Routers خلف NAT أن:

- استخدم UPnP لفتح المنافذ تلقائياً
- قم بتهيئة إعادة توجيه المنافذ يدوياً
- اعتمد على SSU2 للاتصالات الواردة مع استخدام NTCP2 للاتصالات الصادرة

---

## 9. تمويه البروتوكول

كلتا وسيلتي النقل الحديثتين تتضمنان ميزات تمويه:

- **حشو عشوائي** في رسائل المصافحة
- **رؤوس مشفّرة** لا تكشف بصمات البروتوكول
- **رسائل بطول متغير** لمقاومة تحليل حركة المرور
- **لا أنماط ثابتة** في إنشاء الاتصال

> **ملاحظة**: التمويه على مستوى طبقة النقل يُكمل، لكنه لا يحل محل إخفاء الهوية الذي توفره بنية tunnel في I2P.

---

## 10. التطوير المستقبلي

تشمل الأبحاث والتحسينات المخططة ما يلي:

- **وسائط نقل قابلة للإضافة** – ملحقات تمويه متوافقة مع Tor
- **نقل قائم على QUIC** – استكشاف فوائد بروتوكول QUIC
- **تحسين حدود الاتصالات** – بحث في الحدود المثلى لاتصالات الأقران
- **استراتيجيات حشو معززة** – مقاومة محسّنة لتحليل حركة المرور

---

## 11. المراجع

- [مواصفة NTCP2](/docs/specs/ntcp2/) – نقل TCP قائم على Noise (إطار عمل لتصميم بروتوكولات التشفير)
- [مواصفة SSU2](/docs/specs/ssu2/) – UDP شبه موثوق وآمن 2
- [مواصفة I2NP](/docs/specs/i2np/) – رسائل بروتوكول شبكة I2P
- [الهياكل الشائعة](/docs/specs/common-structures/) – RouterInfo وهياكل العناوين
- [مناقشة NTCP التاريخية](/docs/ntcp/) – تاريخ تطوير النقل القديم
- [توثيق SSU القديم](/docs/legacy/ssu/) – المواصفة الأصلية لـ SSU (مهملة)
