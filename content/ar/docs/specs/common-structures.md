---
title: "الهياكل الشائعة"
description: "أنواع البيانات المشتركة وتنسيقات التسلسل المستخدمة عبر مواصفات I2P"
slug: "common-structures"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## نظرة عامة

يحدد هذا المستند هياكل البيانات الأساسية المستخدمة عبر جميع بروتوكولات I2P، بما في ذلك [I2NP](/docs/specs/i2np/)، [I2CP](/docs/specs/i2cp/)، [SSU2](/docs/specs/ssu2/)، [NTCP2](/docs/specs/ntcp2/) وغيرها. تضمن هذه الهياكل المشتركة قابلية التشغيل البيني بين تطبيقات I2P المختلفة وطبقات البروتوكول.

### التغييرات الرئيسية منذ 0.9.58

- أُعلِن تقادم ElGamal و DSA-SHA1 لهويات Router (استخدم X25519 + EdDSA)
- دعم ML-KEM لما بعد الكم في مرحلة الاختبار التجريبي (اختياري اعتبارًا من 2.10.0)
- تم توحيد خيارات سجل الخدمة ([Proposal 167](/proposals/167-service-records/), تم تنفيذها في 0.9.66)
- تم إقرار مواصفات الحشو القابل للضغط نهائيًا ([Proposal 161](/ar/proposals/161-ri-dest-padding/), تم تنفيذها في 0.9.57)

---

## مواصفات الأنواع المشتركة

### عدد صحيح

**الوصف:** يمثّل عددًا صحيحًا غير سالب بترتيب بايتات الشبكة (big-endian؛ حيث يأتي البايت الأعلى أهمية أولًا).

**المحتويات:** من 1 إلى 8 بايتات تمثل عدداً صحيحاً غير موقّع.

**الاستخدام:** أطوال الحقول، وأعداد العناصر، ومعرّفات الأنواع، والقيم الرقمية في جميع بروتوكولات I2P.

---

### التاريخ

**الوصف:** طابع زمني يمثل عدد الميلي ثانية منذ حقبة Unix (نقطة البداية الزمنية في أنظمة Unix) (1 يناير 1970 00:00:00 GMT).

**المحتويات:** عدد صحيح بطول 8 بايت (unsigned long)

**القيم الخاصة:** - `0` = تاريخ غير معرّف أو فارغ - القيمة القصوى: `0xFFFFFFFFFFFFFFFF` (السنة 584,942,417,355)

**ملاحظات التنفيذ:** - دائمًا المنطقة الزمنية UTC/GMT - الدقة على مستوى الميلي ثانية مطلوبة - تُستخدم لانتهاء صلاحية الـlease (مدة الإيجار)، ونشر RouterInfo (معلومات الـRouter)، والتحقق من صحة الطابع الزمني

---

### سلسلة نصية

**الوصف:** سلسلة نصية مرمّزة بترميز UTF-8 مع بادئة تحدد الطول.

**التنسيق:**

```
+----+----+----+----+----+----+
|len | UTF-8 encoded data...   |
+----+----+----+----+----+----+

len :: Integer (1 byte)
       Value: 0-255 (string length in bytes, NOT characters)

data :: UTF-8 encoded bytes
        Length: 0-255 bytes
```
**القيود:** - الحد الأقصى للطول: 255 بايت (وليس عدد المحارف - تُحتسب تسلسلات UTF-8 متعددة البايت على أنها عدة بايتات) - قد يكون الطول صفراً (سلسلة فارغة) - لا يتضمن محرف الإنهاء null - السلسلة ليست منتهية بـ null

**هام:** قد تستخدم تسلسلات UTF-8 عدة بايتات لكل حرف. قد تتجاوز سلسلة تحتوي على 100 حرف الحد البالغ 255 بايت إذا كانت تستخدم أحرف متعددة البايت.

---

## بُنى مفاتيح التشفير

### المفتاح العام

**الوصف:** مفتاح عام للتشفير غير المتماثل. يعتمد نوع المفتاح وطوله على السياق أو يُحدَّدان في شهادة مفتاح.

**النوع الافتراضي:** ElGamal (خوارزمية تشفير بالمفتاح العام) (مهمل لهويات Router اعتبارًا من 0.9.58)

**الأنواع المدعومة:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only (unused field)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">800</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1184</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1088</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**متطلبات التنفيذ:**

1. **X25519 (النوع 4) - المعيار الحالي:**
   - يُستخدم لتشفير ECIES-X25519-AEAD-Ratchet
   - إلزامي لهويات Router منذ 0.9.48
   - ترميز Little-endian (الترتيب الأصغر أولاً) (على خلاف الأنواع الأخرى)
   - راجع [ECIES](/docs/specs/ecies/) و[ECIES-ROUTERS](/docs/specs/ecies/#routers)

2. **ElGamal (خوارزمية تشفير) (Type 0) - قديمة:**
   - مُهمَّلة لهويات Router اعتبارًا من 0.9.58
   - لا تزال صالحة للوجهات (الحقل غير مستخدم منذ 0.6/2005)
   - تستخدم أعدادًا أولية ثابتة مُعرَّفة في [مواصفة ElGamal](/docs/specs/cryptography/)
   - يُحافَظ على الدعم للتوافق مع الإصدارات الأقدم

3. **MLKEM (ما بعد الكمّ) - بيتا:**
   - نهج هجين يجمع بين ML-KEM (آلية تغليف المفاتيح القائمة على الشبكات المعيارية) وX25519
   - غير مُفعّلة افتراضياً في 2.10.0
   - يتطلب تفعيلها يدوياً عبر Hidden Service Manager
   - انظر [ECIES-HYBRID](/docs/specs/ecies/#hybrid) و[Proposal 169](/proposals/169-pq-crypto/)
   - أكواد النوع والمواصفات قابلة للتغيير

**JavaDoc (توثيق جافا):** [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)

---

### المفتاح الخاص

**الوصف:** مفتاح خاص لفك التشفير غير المتماثل، يتوافق مع أنواع PublicKey.

**التخزين:** يُستدل على النوع والطول من السياق أو يتم تخزينهما بشكل منفصل في هياكل البيانات/ملفات المفاتيح.

**الأنواع المدعومة:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1632</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2400</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3168</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**ملاحظات أمنية:** - يجب إنشاء المفاتيح الخاصة باستخدام مولدات أعداد عشوائية آمنة من الناحية التشفيرية - تستخدم مفاتيح X25519 الخاصة scalar clamping (تقييد السكالار) كما هو معرّف في RFC 7748 - يجب محو المادة المفتاحية من الذاكرة بشكل آمن عند عدم الحاجة إليها

**توثيق JavaDoc:** [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)

---

### SessionKey (مفتاح الجلسة)

**الوصف:** مفتاح متناظر لتشفير وفك تشفير AES-256 ضمن tunnel وgarlic encryption الخاصة بـ I2P.

**المحتوى:** 32 بايت (256 بت)

**الاستخدام:** - تشفير طبقة tunnel (AES-256/CBC with IV) - تشفير رسائل garlic - تشفير الجلسة من طرف إلى طرف

**التوليد:** يجب استخدام مولّد أعداد عشوائية آمن تشفيرياً.

**توثيق JavaDoc:** [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)

---

### SigningPublicKey (المفتاح العام للتوقيع)

**الوصف:** المفتاح العمومي للتحقق من صحة التوقيع. يتم تحديد النوع والطول في شهادة المفتاح الخاصة بـ Destination (الوجهة في I2P) أو يُستدل عليهما من السياق.

**النوع الافتراضي:** DSA_SHA1 (مهمل اعتبارًا من 0.9.58)

**الأنواع المدعومة:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (MLDSA)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 169</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65280-65534</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Testing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Never production</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65535</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future expansion</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td></tr>
  </tbody>
</table>
**متطلبات التنفيذ:**

1. **EdDSA_SHA512_Ed25519 (Type 7) - المعيار الحالي:**
   - الإعداد الافتراضي لجميع هويات Router والوجهات الجديدة منذ أواخر 2015
   - يستخدم منحنى Ed25519 مع تجزئة SHA-512
   - مفاتيح عامة بطول 32 بايت، وتواقيع بطول 64 بايت
   - ترميز Little-endian (ترتيب البايت من الأصغر إلى الأكبر) (على خلاف معظم الأنواع الأخرى)
   - أداء عالٍ وأمن قوي

2. **RedDSA_SHA512_Ed25519 (النوع 11) - متخصص:**
   - يُستخدم حصراً مع leasesets المشفَّرة (مجموعات الإيجارات في I2P) وعمليات الإعماء
   - لا يُستخدم مطلقاً في Router Identities أو Destinations القياسية
   - الفروق الرئيسية عن EdDSA:
     - توليد المفاتيح الخاصة بالاختزال المعياري (بدلاً من clamping أي تقييد البتّات)
     - التواقيع تتضمن 80 بايتاً من البيانات العشوائية
     - تستخدم المفاتيح العامة مباشرةً (وليس تجزئات المفاتيح الخاصة)
   - راجع [مواصفة Red25519](//docs/specs/red25519-signature-scheme/

3. **DSA_SHA1 (Type 0) - قديمة:**
   - مُعلنة كمهجورة لهويات Router اعتباراً من 0.9.58
   - غير مُستحسنة للوجهات الجديدة
   - DSA بطول 1024-بت مع SHA-1 (نقاط ضعف معروفة)
   - الإبقاء على الدعم لأغراض التوافق فقط

4. **مفاتيح متعددة العناصر:**
   - عندما يتكون من عنصرين (مثل: نقاط ECDSA (خوارزمية التوقيع الرقمي باستخدام المنحنيات البيضوية) X,Y)
   - يُحشى كل عنصر إلى الطول/2 بأصفار بادئة
   - مثال: مفتاح ECDSA بحجم 64 بايت = 32 بايت لـ X + 32 بايت لـ Y

**توثيق JavaDoc:** [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)

---

### SigningPrivateKey

**الوصف:** مفتاح خاص لإنشاء التواقيع، المقابل لأنواع SigningPublicKey (مفتاح التوقيع العام).

**التخزين:** يتم تحديد النوع والطول وقت الإنشاء.

**الأنواع المدعومة:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**متطلبات الأمان:** - التوليد باستخدام مصدر عشوائي آمن تشفيرياً - الحماية بضوابط وصول ملائمة - محوها بأمان من الذاكرة عند الانتهاء - بالنسبة إلى EdDSA (خوارزمية التوقيع الرقمي على منحنيات إدواردز): بذرة بحجم 32 بايت يُجرى لها تجزئة باستخدام SHA-512، وتصبح أول 32 بايت قيمة سكالار (scalar) مع تطبيق clamping (تقييد البتّات وفق المواصفات) - بالنسبة إلى RedDSA (متغير يستخدم الاختزال المعياري في توليد المفاتيح): توليد مفاتيح مختلف (اختزال معياري بدلاً من clamping)

**JavaDoc (توثيق جافا):** [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)

---

### التوقيع

**الوصف:** توقيع تشفيري على البيانات، باستخدام خوارزمية التوقيع المقابلة لنوع SigningPrivateKey.

**النوع والطول:** يتم استنتاجهما من نوع المفتاح المستخدم للتوقيع.

**الأنواع المدعومة:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**ملاحظات التنسيق:** - التواقيع متعددة العناصر (مثلاً، قيم ECDSA R,S) تُستكمل كل قيمة إلى طول length/2 بإضافة أصفار بادئة - تستخدم EdDSA و RedDSA ترميز little-endian (ترتيب البايتات من الأقل أهمية إلى الأكثر أهمية) - تستخدم جميع الأنواع الأخرى ترميز big-endian (ترتيب البايتات من الأكثر أهمية إلى الأقل أهمية)

**التحقق:** - استخدم SigningPublicKey المقابل - اتبع مواصفات خوارزمية التوقيع لنوع المفتاح - تحقق من أن طول التوقيع يطابق الطول المتوقع لنوع المفتاح

**JavaDoc (توثيق Java):** [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)

---

### تجزئة

**الوصف:** تجزئة SHA-256 للبيانات، تُستخدم في جميع أنحاء I2P للتحقق من السلامة والتعرّف.

**المحتوى:** 32 بايت (256 بت)

**الاستخدام:** - تجزئات Router Identity (مفاتيح قاعدة بيانات الشبكة) - تجزئات الوجهة (مفاتيح قاعدة بيانات الشبكة) - تحديد بوابة Tunnel ضمن Leases - التحقق من سلامة البيانات - توليد معرف Tunnel

**الخوارزمية:** SHA-256 كما هو محدد في FIPS 180-4

**JavaDoc (توثيق جافا):** [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)

---

### وسم الجلسة

**الوصف:** رقم عشوائي يُستخدم لتحديد هوية الجلسة والتشفير القائم على الوسوم.

**مهم:** يختلف حجم وسم الجلسة بحسب نوع التشفير: - **ElGamal/AES+SessionTag:** 32 بايت (قديم) - **ECIES-X25519:** 8 بايت (المعيار الحالي)

**المعيار الحالي (ECIES - مخطط التشفير المتكامل بالمنحنى الإهليلجي):**

```
Contents: 8 bytes
Usage: Ratchet-based encryption for Destinations and Routers
```
راجع [ECIES](/docs/specs/ecies/) و[ECIES-ROUTERS](/docs/specs/ecies/#routers) للاطلاع على المواصفات التفصيلية.

**قديم (ElGamal/AES — خوارزميتا تشفير):**

```
Contents: 32 bytes
Usage: Deprecated encryption scheme
```
**التوليد:** يجب استخدام مولِّد أرقام عشوائية آمن تشفيرياً.

**جافا دوك:** [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)

---

### TunnelId

**الوصف:** مُعرّف فريد لموضع router داخل tunnel. تمتلك كل قفزة في tunnel قيمة TunnelId (معرّف النفق) خاصة بها.

**التنسيق:**

```
Contents: 4-byte Integer (unsigned 32-bit)
Range: Generally > 0 (zero reserved for special cases)
```
**الاستخدام:** - يحدد اتصالات tunnel الواردة/الصادرة عند كل router - TunnelId مختلف عند كل قفزة في سلسلة الـ tunnel - يُستخدم في هياكل Lease (بنية بيانات في I2P) لتحديد tunnel البوابة

**قيم خاصة:** - `0` = محجوزة لاستخدامات خاصة في البروتوكول (تجنّب استخدامها في التشغيل العادي) - TunnelIds (معرّفات tunnel) صالحة محليًا لكل router

**JavaDoc:** [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)

---

## مواصفات الشهادات

### شهادة

**الوصف:** حاوية للإيصالات، أو لإثبات العمل، أو للبيانات الوصفية التشفيرية المستخدمة على امتداد I2P.

**التنسيق:**

```
+----+----+----+----+----+----+-//
|type| length  | payload
+----+----+----+----+----+----+-//

type :: Integer (1 byte)
        Values: 0-5 (see types below)

length :: Integer (2 bytes, big-endian)
          Size of payload in bytes

payload :: data
           length -> $length bytes
```
**الحجم الإجمالي:** 3 بايت كحد أدنى (NULL certificate — شهادة فارغة)، وحتى 65538 بايت كحد أقصى

### أنواع الشهادات

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NULL</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default/empty certificate</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HASHCASH</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (was for proof-of-work)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HIDDEN</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (hidden routers don't advertise)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SIGNED</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 or 72</td><td style="border:1px solid var(--color-border); padding:0.5rem;">43 or 75</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (DSA signature ± destination hash)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MULTIPLE</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (multiple certificates)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KEY</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4+</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7+</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Current</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies key types (see below)</td></tr>
  </tbody>
</table>
### شهادة المفتاح (النوع 5)

**المقدمة:** الإصدار 0.9.12 (ديسمبر 2013)

**الغرض:** يحدد أنواع مفاتيح غير افتراضية ويخزّن بيانات مفاتيح زائدة تتجاوز بنية KeysAndCert القياسية بحجم 384 بايت.

**بنية الحمولة:**

```
+----+----+----+----+----+----+----+----+-//
|SPKtype|CPKtype| Excess SPK data     |
+----+----+----+----+----+----+----+----+-//
              | Excess CPK data...    |
+----+----+----+----+----+----+----+----+

SPKtype :: Signing Public Key Type (2 bytes)
           See SigningPublicKey table above

CPKtype :: Crypto Public Key Type (2 bytes)
           See PublicKey table above

Excess SPK data :: Signing key bytes beyond 128 bytes
                   Length: 0 to 65531 bytes

Excess CPK data :: Crypto key bytes beyond 256 bytes
                   Length: 0 to remaining space
```
**ملاحظات التنفيذ الحرجة:**

1. **ترتيب أنواع المفاتيح:**
   - **تحذير:** يأتي نوع مفتاح التوقيع قبل نوع مفتاح التشفير
   - هذا غير بديهي ولكنه مُحافَظ عليه لأغراض التوافق
   - الترتيب: SPKtype, CPKtype (ليس CPKtype, SPKtype)

2. **تخطيط بيانات المفاتيح في KeysAndCert (هيكل المفاتيح والشهادة):**
   ```
   [Crypto Public Key (partial/complete)]
   [Padding (if total key lengths < 384)]
   [Signing Public Key (partial/complete)]
   [Certificate Header (3 bytes)]
   [Key Certificate (4+ bytes)]
   [Excess Signing Key Data]
   [Excess Crypto Key Data]
   ```

3. **حساب بيانات المفاتيح الزائدة:**
   - إذا كان Crypto Key > 256 بايت: Excess = (Crypto Length - 256)
   - إذا كان Signing Key > 128 بايت: Excess = (Signing Length - 128)
   - Padding = max(0, 384 - Crypto Length - Signing Length)

**أمثلة (ElGamal Crypto Key، مفتاح تشفير بخوارزمية إل-غامال):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Total SPK Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Padding</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Excess in Cert</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Structure Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 11 = 398</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 135 = 522</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 391 = 778</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
  </tbody>
</table>
**متطلبات هوية Router:** - تم استخدام شهادة NULL حتى الإصدار 0.9.15 - شهادة المفتاح مطلوبة لأنواع المفاتيح غير الافتراضية منذ 0.9.16 - تم دعم مفاتيح التشفير X25519 منذ 0.9.48

**متطلبات الوجهة:** - شهادة NULL (فارغة) أو شهادة مفتاح (حسب الحاجة) - شهادة مفتاح مطلوبة لأنواع مفاتيح التوقيع غير الافتراضية منذ 0.9.12 - حقل المفتاح العام للتشفير غير مستخدم منذ 0.6 (2005) ولكنه يجب أن يظل موجوداً

**تحذيرات مهمة:**

1. **شهادة NULL مقابل KEY:**
   - تُسمح شهادة KEY ذات الأنواع (0,0) التي تحدد ElGamal+DSA_SHA1، ولكن يُنصَح بتجنّبها
   - استخدم دائمًا شهادة NULL لـ ElGamal+DSA_SHA1 (التمثيل المعياري)
   - شهادة KEY ذات (0,0) أطول بمقدار 4 بايتات وقد تتسبب في مشكلات توافق
   - قد لا تتعامل بعض عمليات التنفيذ مع شهادات KEY ذات (0,0) بشكل صحيح

2. **التحقق من البيانات الزائدة:**
   - يجب على عمليات التنفيذ التحقق من أن طول الشهادة يتطابق مع الطول المتوقع لكل نوع من أنواع المفاتيح
   - رفض الشهادات التي تحتوي على بيانات زائدة لا تتوافق مع أنواع المفاتيح
   - حظر وجود بيانات لاحقة عشوائية بعد بنية الشهادة الصالحة

**JavaDoc (توثيق الشيفرة في جافا):** [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)

---

### التعيين

**الوصف:** مجموعة خصائص مفتاح-قيمة تُستخدم للتهيئة والبيانات الوصفية.

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+

size :: Integer (2 bytes, big-endian)
        Total number of bytes that follow (not including size field)
        Range: 0 to 65535

key_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

= :: Single byte (0x3D, '=' character)

val_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

; :: Single byte (0x3B, ';' character)

[Repeat key_string = val_string ; for additional entries]
```
**حدود الحجم:** - طول المفتاح: 0-255 بايت (+ 1 بايت للطول) - طول القيمة: 0-255 بايت (+ 1 بايت للطول) - إجمالي حجم التعيين: 0-65535 بايت (+ 2 بايت لحقل الحجم) - الحد الأقصى لحجم البنية: 65537 بايت

**متطلب حاسم للفرز:**

عند ظهور التعيينات في **البنى الموقّعة** (RouterInfo, RouterAddress, Destination properties, I2CP SessionConfig)، يجب ترتيب المدخلات حسب المفتاح لضمان ثبات التوقيع:

1. **طريقة الفرز:** ترتيب معجمي باستخدام قيم نقاط الرمز في Unicode (يعادل Java String.compareTo())
2. **حساسية حالة الأحرف:** المفاتيح والقيم عمومًا حساسة لحالة الأحرف (تبعًا للتطبيق)
3. **المفاتيح المكررة:** غير مسموح بها في البنى الموقعة (سيؤدي إلى فشل التحقق من التوقيع)
4. **ترميز الأحرف:** مقارنة على مستوى البايت باستخدام UTF-8

**لماذا يعد الفرز مهمًا:** - يتم حساب التواقيع على التمثيل بالبايتات - تؤدي ترتيبات المفاتيح المختلفة إلى تواقيع مختلفة - لا تتطلب التعيينات غير الموقعة الفرز ولكن ينبغي أن تتبع الاتفاقية نفسها

**ملاحظات التنفيذ:**

1. **ازدواجية الترميز:**
   - كلا المحدِّدين `=` و`;` وكذلك بايتات طول السلسلة موجودة
   - هذا غير فعّال لكنه مُبقى للحفاظ على التوافق
   - بايتات الطول هي المرجع المعتمد؛ المحدِّدات مطلوبة لكنها زائدة عن الحاجة

2. **دعم المحارف:**
   - على الرغم مما تذكره الوثائق، فإن `=` و `;` مدعومان فعلًا داخل السلاسل النصية (تتعامل بايتات الطول مع ذلك)
   - ترميز UTF-8 يدعم يونيكود بالكامل
   - **تحذير:** I2CP يستخدم UTF-8، لكن I2NP تاريخيًا لم يكن يتعامل مع UTF-8 بشكل صحيح
   - استخدم ASCII لتعيينات I2NP متى أمكن لتحقيق أقصى قدر من التوافق

3. **سياقات خاصة:**
   - **RouterInfo/RouterAddress:** يجب ترتيبها، من دون تكرارات
   - **I2CP SessionConfig:** يجب ترتيبها، من دون تكرارات  
   - **تعيينات التطبيقات:** يوصى بالترتيب ولكن ليس مطلوبًا دائمًا

**مثال (خيارات RouterInfo):**

```
Mapping size: 45 bytes
Sorted entries:
  caps=L       (capabilities)
  netId=2      (network ID)
  router.version=0.9.67
```
**JavaDoc (توثيق Java):** [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)

---

## مواصفة البنية المشتركة

### المفاتيح والشهادة

**الوصف:** بنية أساسية تجمع مفتاح التشفير، مفتاح التوقيع، والشهادة. تُستخدَم بوصفها كلًا من RouterIdentity وDestination.

**البنية:**

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-//

public_key :: PublicKey (partial or full)
              Default: 256 bytes (ElGamal)
              Other sizes: As specified in Key Certificate

padding :: Random data
           Length: 0 bytes or as needed
           CONSTRAINT: public_key + padding + signing_key = 384 bytes

signing_key :: SigningPublicKey (partial or full)
               Default: 128 bytes (DSA_SHA1)
               Other sizes: As specified in Key Certificate

certificate :: Certificate
               Minimum: 3 bytes (NULL certificate)
               Common: 7 bytes (Key Certificate with default keys)

TOTAL LENGTH: 387+ bytes (never assume exactly 387!)
```
**محاذاة المفاتيح:** - **المفتاح العام للتشفير:** محاذى عند البداية (البايت 0) - **الحشو:** في الوسط (عند الحاجة) - **المفتاح العام للتوقيع:** محاذى عند النهاية (من البايت 256 إلى البايت 383) - **الشهادة:** تبدأ عند البايت 384

**حساب الحجم:**

```
Total size = 384 + 3 + key_certificate_length

For NULL certificate (ElGamal + DSA_SHA1):
  Total = 384 + 3 = 387 bytes

For Key Certificate (EdDSA + X25519):
  Total = 384 + 3 + 4 = 391 bytes

For larger keys (e.g., RSA_4096):
  Total = 384 + 3 + 4 + excess_key_data_length
```
### إرشادات توليد الحشو ([المقترح 161](/ar/proposals/161-ri-dest-padding/))

**إصدار التنفيذ:** 0.9.57 (يناير 2023، الإصدار 2.1.0)

**الخلفية:** - بالنسبة للمفاتيح غير ElGamal+DSA، الحشو موجود في البنية الثابتة بحجم 384 بايت - بالنسبة إلى الوجهات (Destinations)، لم يُستخدم حقل المفتاح العام بحجم 256 بايت منذ الإصدار 0.6 (2005) - يجب توليد الحشو بحيث يكون قابلاً للضغط مع الحفاظ على الأمان

**المتطلبات:**

1. **الحد الأدنى للبيانات العشوائية:**
   - استخدم ما لا يقل عن 32 بايتًا من بيانات عشوائية آمنة من الناحية التشفيرية
   - يوفر هذا مقدارًا كافيًا من entropy (مقدار العشوائية) للأمان

2. **استراتيجية الضغط:**
   - كرّر 32 بايت على امتداد حقل الحشو/المفتاح العام
   - تستخدم بروتوكولات مثل I2NP Database Store (رسالة تخزين قاعدة البيانات ضمن I2NP)، Streaming SYN (طلب SYN لبدء الاتصال في طبقة Streaming)، وSSU2 handshake (عملية المصافحة في SSU2) الضغط
   - توفير كبير في استهلاك عرض النطاق الترددي دون المساس بالأمان

3. **أمثلة:**

**هوية الـRouter (X25519 + EdDSA، خوارزميات تشفير منحنيات بيضاوية):**

```
Structure:
- 32 bytes X25519 public key
- 320 bytes padding (10 copies of 32-byte random data)
- 32 bytes EdDSA public key
- 7 bytes Key Certificate

Compression savings: ~288 bytes when compressed
```
**الوجهة (ElGamal-unused + EdDSA):**

```
Structure:
- 256 bytes unused ElGamal field (11 copies of 32-byte random data, truncated to 256)
- 96 bytes padding (3 copies of 32-byte random data)
- 32 bytes EdDSA public key  
- 7 bytes Key Certificate

Compression savings: ~320 bytes when compressed
```
4. **لماذا يعمل هذا:**
   - تجزئة SHA-256 للبنية الكاملة لا تزال تتضمن كل الإنتروبيا (Entropy)
   - يعتمد توزيع DHT لقاعدة بيانات الشبكة فقط على التجزئة
   - مفتاح التوقيع (32 بايت EdDSA/X25519) يوفّر 256 بتًا من الإنتروبيا
   - 32 بايتًا إضافية من بيانات عشوائية مكررة = 512 بتًا من الإنتروبيا الإجمالية
   - أكثر من كافٍ لتحقيق قوة تشفيرية

5. **ملاحظات التنفيذ:**
   - يجب تخزين ونقل البنية الكاملة بحجم 387+ بايت
   - تجزئة SHA-256 محسوبة على البنية الكاملة غير المضغوطة
   - يُطبَّق الضغط على طبقة البروتوكول (I2NP, Streaming, SSU2)
   - متوافق رجعياً مع جميع الإصدارات منذ 0.6 (2005)

**JavaDoc (توثيق جافا):** [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)

---

### RouterIdentity (هوية router)

**الوصف:** يعرّف router بشكل فريد ضمن شبكة I2P. بنية مطابقة لـ KeysAndCert (مفاتيح وشهادة).

**التنسيق:** انظر بنية KeysAndCert أعلاه

**المتطلبات الحالية (اعتبارًا من 0.9.58):**

1. **أنواع المفاتيح الإلزامية:**
   - **التشفير:** X25519 (النوع 4، 32 بايت)
   - **التوقيع:** EdDSA_SHA512_Ed25519 (النوع 7، 32 بايت)
   - **الشهادة:** Key Certificate (شهادة المفتاح) (النوع 5)

2. **أنواع المفاتيح المهملة:**
   - ElGamal (type 0) تم إهماله لـ Router Identities اعتبارًا من 0.9.58
   - DSA_SHA1 (type 0) تم إهماله لـ Router Identities اعتبارًا من 0.9.58
   - لا ينبغي إطلاقًا استخدامها مع أي router جديد

3. **الحجم النموذجي:**
   - X25519 + EdDSA مع شهادة المفتاح = 391 بايت
   - 32 بايت لمفتاح عام X25519
   - 320 بايت حشو (قابل للضغط حسب [Proposal 161](/ar/proposals/161-ri-dest-padding/))
   - 32 بايت لمفتاح عام EdDSA
   - 7 بايت شهادة (ترويسة 3 بايت + أنواع المفاتيح 4 بايت)

**التطور التاريخي:** - قبل 0.9.16: كانت الشهادة دائمًا NULL (ElGamal + DSA_SHA1) - 0.9.16-0.9.47: تمت إضافة دعم Key Certificate (شهادة المفاتيح) - 0.9.48+: تم دعم مفاتيح تشفير X25519 - 0.9.58+: تم إهمال ElGamal و DSA_SHA1

**مفتاح قاعدة البيانات الشبكية:** - RouterInfo مفهرس بواسطة تجزئة SHA-256 لـ RouterIdentity الكامل - التجزئة محسوبة على البنية كاملة المؤلفة من 391+ بايت (بما في ذلك الحشو)

**انظر أيضًا:** - إرشادات توليد الحشو ([المقترح 161](/ar/proposals/161-ri-dest-padding/)) - مواصفة شهادة المفتاح أعلاه

**JavaDoc (توثيق Java):** [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)

---

### الوجهة

**الوصف:** مُعرِّف نقطة نهاية للتسليم الآمن للرسائل. مماثل من حيث البنية لـ KeysAndCert، لكن بدلالات استخدام مختلفة.

**التنسيق:** راجع بنية KeysAndCert أعلاه

**الاختلاف الجوهري عن RouterIdentity:** - **حقل المفتاح العام غير مُستخدَم وقد يحتوي على بيانات عشوائية** - لم يُستخدم هذا الحقل منذ الإصدار 0.6 (2005) - كان يُستخدم في الأصل لتشفير I2CP-to-I2CP القديم (معطَّل) - يُستخدم حالياً فقط كـ IV (متجه التهيئة) لتشفير LeaseSet المُهمل

**التوصيات الحالية:**

1. **مفتاح التوقيع:**
   - **موصى به:** EdDSA_SHA512_Ed25519 (النوع 7، 32 بايت)
   - بديل: أنواع ECDSA للتوافق مع الإصدارات الأقدم
   - تجنب: DSA_SHA1 (مهمل، غير مستحسن)

2. **مفتاح التشفير:**
   - الحقل غير مستخدَم لكنه يجب أن يكون موجودًا
   - **موصى به:** املأه ببيانات عشوائية وفقًا لـ [Proposal 161](/ar/proposals/161-ri-dest-padding/) (قابلة للضغط)
   - الحجم: دائمًا 256 بايت (فتحة ElGamal (خوارزمية التشفير ElGamal)، على الرغم من أنه لا يُستَخدَم لـ ElGamal)

3. **الشهادة:**
   - شهادة NULL لـ ElGamal + DSA_SHA1 (للاستخدام المتقادِم فقط)
   - شهادة المفتاح (Key Certificate) لجميع أنواع مفاتيح التوقيع الأخرى

**الوجهة النموذجية الحديثة:**

```
Structure:
- 256 bytes unused field (random data, compressible)
- 96 bytes padding (random data, compressible)
- 32 bytes EdDSA signing public key
- 7 bytes Key Certificate

Total: 391 bytes
Compression savings: ~320 bytes
```
**مفتاح التشفير الفعلي:** - مفتاح التشفير الخاص بالوجهة موجود في **LeaseSet**، وليس في الوجهة - يحتوي LeaseSet على المفاتيح العامة للتشفير الحالية - راجع مواصفات LeaseSet2 لمعالجة مفاتيح التشفير

**مفتاح قاعدة بيانات الشبكة:** - LeaseSet (مجموعة عقود الوصول في I2P) مفهرس بواسطة تجزئة SHA-256 للوجهة الكاملة - تُحتسب التجزئة على البنية الكاملة بحجم 387+ بايت

**JavaDoc (توثيق جافا):** [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)

---

## هياكل قاعدة بيانات الشبكة

### Lease (عنصر في leaseSet يحدد tunnel صالحاً حتى وقت انتهاء معين)

**الوصف:** يأذن لـ tunnel معيّن باستلام الرسائل الموجّهة إلى Destination (الوجهة). وهو جزء من تنسيق LeaseSet الأصلي (النوع 1).

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of the gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at the gateway router

end_date :: Date (8 bytes)
            Expiration timestamp in milliseconds since epoch
```
**إجمالي الحجم:** 44 بايت

**الاستخدام:** - يُستخدم فقط في LeaseSet الأصلي (النوع 1، مهمل) - بالنسبة إلى LeaseSet2 والمتغيرات اللاحقة، استخدم Lease2 بدلاً من ذلك

**توثيق JavaDoc:** [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)

---

### LeaseSet (النوع 1)

**الوصف:** صيغة LeaseSet الأصلية. تتضمن tunnels المصرَّح بها والمفاتيح الخاصة بـ Destination (الوجهة). مخزَّنة في قاعدة بيانات الشبكة. **الحالة: مهملة** (استخدم LeaseSet2 بدلاً من ذلك).

**البنية:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

encryption_key :: PublicKey (256 bytes, ElGamal)
                  Used for end-to-end ElGamal/AES+SessionTag encryption
                  Generated anew at each router startup (not persistent)

signing_key :: SigningPublicKey (128+ bytes)
               Same type as Destination signing key
               Used for LeaseSet revocation (unimplemented)
               Generated anew at each router startup (not persistent)

num :: Integer (1 byte)
       Number of Leases to follow
       Range: 0-16

leases :: Array of Lease structures
          Length: $num × 44 bytes
          Each Lease is 44 bytes

signature :: Signature (40+ bytes)
             Length determined by Destination signing key type
             Signed by Destination's SigningPrivateKey
```
**التخزين في قاعدة البيانات:** - **نوع قاعدة البيانات:** 1 - **المفتاح:** تجزئة SHA-256 للوجهة - **القيمة:** البنية الكاملة لـ LeaseSet (بنية بيانات عقود المسارات الواردة في I2P)

**ملاحظات مهمة:**

1. **المفتاح العام لـ Destination (الوجهة في I2P) غير مستخدم:**
   - حقل المفتاح العام للتشفير في Destination غير مستخدم
   - مفتاح التشفير في LeaseSet هو مفتاح التشفير الفعلي

2. **مفاتيح مؤقتة:**
   - `encryption_key` مؤقت (يُعاد توليده عند بدء تشغيل router)
   - `signing_key` مؤقت (يُعاد توليده عند بدء تشغيل router)
   - لا يتم الاحتفاظ بأيّ من المفتاحين بين عمليات إعادة التشغيل

3. **الإبطال (غير مُنفَّذ):**
   - كان `signing_key` معدّاً لإبطال LeaseSet
   - لم تُنفَّذ آلية الإبطال مطلقاً
   - كان المقصود استخدام LeaseSet بصفر عقود (zero-lease) للإبطال، لكنه غير مُستَخدَم

4. **إدارة الإصدارات/الطابع الزمني:**
   - لا يحتوي LeaseSet على حقل طابع زمني `published` صريح
   - الإصدار هو أبكر وقت لانتهاء صلاحية جميع leases (عنصر تسليم مؤقت في I2P)
   - يجب أن يكون انتهاء صلاحية lease في LeaseSet الجديد أبكر ليتم قبوله

5. **نشر أوقات انتهاء الـ lease (مدخل يحدد نفقًا ووقت انتهاءه):**
   - قبل 0.9.7: تم نشر جميع الـ leases بنفس وقت الانتهاء (الأبكر)
   - 0.9.7+: تم نشر أوقات انتهاء كل lease الفعلية بشكل منفصل
   - هذا تفصيل تنفيذي، وليس جزءًا من المواصفة

6. **صفر Leases:**
   - يُسمح تقنياً بـ LeaseSet يحتوي على صفر Leases
   - مخصّص للإبطال (غير منفذ)
   - غير مستخدم عملياً
   - متغيرات LeaseSet2 تتطلب Lease واحداً على الأقل

**إيقاف الدعم:** تم إيقاف دعم LeaseSet من النوع 1. ينبغي للتنفيذات الجديدة استخدام **LeaseSet2 (النوع 3)** الذي يوفّر: - حقل طابع زمني للنشر (إدارة إصدارات أفضل) - دعم مفاتيح تشفير متعددة - إمكانية التوقيع دون اتصال - تواريخ انتهاء صلاحية الـ lease بطول 4 بايت (بدلاً من 8 بايت) - خيارات أكثر مرونة

**توثيق Java (JavaDoc):** [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)

---

## أنواع LeaseSet

### Lease2 (الإصدار الثاني من هيكل البيانات Lease في I2P)

**الوصف:** تنسيق Lease (سجل مؤقت للنفق) مُحسَّن بحقل انتهاء صلاحية من 4 بايت. يُستخدم في LeaseSet2 (النوع 3) وMetaLeaseSet (النوع 7).

**المقدمة:** الإصدار 0.9.38 (انظر [المقترح 123](/proposals/123-new-netdb-entries/))

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at gateway

end_date :: 4-byte timestamp (seconds since epoch)
            Rolls over in year 2106
```
**إجمالي الحجم:** 40 بايت (أصغر بـ 4 بايت من Lease الأصلي (سجل نفق وارد في I2P))

**المقارنة مع Lease الأصلية (مكوّن في I2P):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1pxsolid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease (Type&nbsp;1)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2 (Type&nbsp;3+)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expiration Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes (ms)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes (seconds)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Precision</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Millisecond</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Second</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rollover</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;292,277,026,596</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;2106</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Used In</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet (deprecated)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, MetaLeaseSet</td></tr>
  </tbody>
</table>
**JavaDoc (توثيق جافا):** [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)

---

### توقيع دون اتصال

**الوصف:** بنية اختيارية للمفاتيح العابرة الموقعة مسبقًا، مما يتيح نشر LeaseSet دون الحاجة إلى الوصول عبر الإنترنت إلى مفتاح التوقيع الخاص بالوجهة (Destination).

**المقدمة:** الإصدار 0.9.38 (انظر [المقترح 123](/proposals/123-new-netdb-entries/))

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4-byte timestamp (seconds since epoch)
           Expiration of transient key validity
           Rolls over in year 2106

sigtype :: 2-byte signature type
           Type of transient_public_key (see SigningPublicKey types)

transient_public_key :: SigningPublicKey
                        Length determined by sigtype
                        Temporary signing key for LeaseSet

signature :: Signature
             Length determined by Destination's signing key type
             Signature of (expires || sigtype || transient_public_key)
             Signed by Destination's permanent SigningPrivateKey
```
**الغرض:** - يُتيح إنشاء LeaseSet دون اتصال - يحمي المفتاح الرئيسي للوجهة من التعرض عبر الإنترنت - يمكن إبطال المفتاح المؤقت بنشر LeaseSet جديد دون توقيع غير متصل

**سيناريوهات الاستخدام:**

1. **وجهات عالية الأمان:**
   - مفتاح التوقيع الرئيسي مخزّن دون اتصال (HSM (وحدة أمن عتادية)، التخزين البارد)
   - تُولَّد المفاتيح المؤقتة دون اتصال لفترات زمنية محدودة
   - اختراق مفتاح مؤقت لا يعرّض المفتاح الرئيسي للخطر

2. **نشر LeaseSet مُشفّر:**
   - EncryptedLeaseSet يمكن أن يتضمن توقيعًا غير متصل
   - المفتاح العام المُعمّى + التوقيع غير المتصل يوفّران أمانًا إضافيًا

**اعتبارات الأمان:**

1. **إدارة انتهاء الصلاحية:**
   - اضبط مدة انتهاء صلاحية معقولة (من أيام إلى أسابيع، وليس سنوات)
   - أنشئ مفاتيح مؤقتة جديدة قبل تاريخ الانتهاء
   - مدة انتهاء أقصر = أمان أفضل، وصيانة أكثر

2. **توليد المفاتيح:**
   - أنشئ مفاتيح مؤقتة دون اتصال في بيئة آمنة
   - وقّع باستخدام المفتاح الرئيسي دون اتصال
   - انقل فقط المفتاح المؤقت الموقّع + التوقيع إلى الـrouter المتصل

3. **الإبطال:**
   - انشر LeaseSet جديداً من دون توقيع غير متصل لإبطاله ضمنياً
   - أو انشر LeaseSet جديداً بمفتاح مؤقت مختلف

**التحقق من التوقيع:**

```
Data to sign: expires (4 bytes) || sigtype (2 bytes) || transient_public_key

Verification:
1. Extract Destination from LeaseSet
2. Get Destination's SigningPublicKey
3. Verify signature over (expires || sigtype || transient_public_key)
4. Check that current time < expires
5. If valid, use transient_public_key to verify LeaseSet signature
```
**ملاحظات التنفيذ:** - يختلف الحجم الإجمالي حسب sigtype (نوع التوقيع) ونوع مفتاح توقيع Destination (الوجهة) - الحد الأدنى للحجم: 4 + 2 + 32 (مفتاح EdDSA) + 64 (توقيع EdDSA) = 102 بايت - الحد الأقصى العملي للحجم: ~600 بايت (مفتاح RSA-4096 مؤقت + توقيع RSA-4096)

**متوافق مع:** - LeaseSet2 (النوع 3) - EncryptedLeaseSet (النوع 5) - MetaLeaseSet (النوع 7)

**انظر أيضًا:** [Proposal 123](/proposals/123-new-netdb-entries/) للاطلاع على بروتوكول التوقيع غير المتصل بالتفصيل.

---

### LeaseSet2Header (رأس LeaseSet2 في I2P)

**الوصف:** بنية ترويسة مشتركة لـ LeaseSet2 (النوع 3) و MetaLeaseSet (النوع 7).

**المقدمة:** الإصدار 0.9.38 (انظر [الاقتراح 123](/proposals/123-new-netdb-entries/))

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

published :: 4-byte timestamp (seconds since epoch)
             Publication time of this LeaseSet
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published timestamp
           Maximum: 65535 seconds (18.2 hours)

flags :: 2 bytes (bit flags)
         See flag definitions below

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 is set
                     Variable length
```
**الحد الأدنى للحجم الإجمالي:** 395 بايت (من دون توقيع غير متصل بالإنترنت)

**تعريفات الأعلام (ترتيب البتات: 15 14 ... 3 2 1 0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bit</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline Keys</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = No offline keys, 1 = Offline signature present</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unpublished</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard published, 1 = Unpublished (client-side only)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard, 1 = Will be blinded when published</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3-15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Must be 0 for compatibility</td></tr>
  </tbody>
</table>
**تفاصيل العلم:**

**البت 0 - المفاتيح غير المتصلة:** - `0`: لا يوجد توقيع غير متصل؛ استخدم مفتاح توقيع Destination للتحقق من توقيع LeaseSet - `1`: تأتي بنية OfflineSignature (توقيع غير متصل) بعد حقل الأعلام

**البت 1 - غير منشور:** - `0`: LeaseSet منشور قياسي، يجب توزيعه إلى floodfills - `1`: LeaseSet غير منشور (على جانب العميل فقط)   - يجب ألّا يتم توزيعه أو نشره أو إرساله استجابةً للاستعلامات   - إذا انتهت صلاحيته، فلا تستعلم netdb عن بديل (إلّا إذا كان البت 2 مُفعّلاً أيضًا)   - يُستخدم لـ tunnels محلية أو للاختبار

**البت 2 - Blinded (مُعمّى) (منذ 0.9.42):** - `0`: LeaseSet قياسي - `1`: سيتم تعمية هذا LeaseSet غير المشفّر وتشفيره عند النشر   - النسخة المنشورة ستكون EncryptedLeaseSet (النوع 5)   - إذا انتهت صلاحيته، استعلم عن **blinded location** في netdb لاستبداله   - يجب أيضًا ضبط البت 1 إلى 1 (غير منشور + blinded)   - يُستخدم للخدمات الخفية المُشفّرة

**حدود انتهاء الصلاحية:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">LeaseSet Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Actual Time</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 (type 3)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈11 minutes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet (type 7)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈18.2 hours</td></tr>
  </tbody>
</table>
**متطلبات الطابع الزمني المنشور:**

لم يكن LeaseSet (type 1) يحتوي على حقل published، مما كان يستلزم البحث عن أقرب وقت لانتهاء صلاحية الـ lease لأغراض تحديد الإصدار. تضيف LeaseSet2 طابعًا زمنيًا صريحًا باسم `published` بدقة ثانية واحدة.

**ملاحظة تنفيذية حرجة:** - يجب على Routers تقييد معدل نشر LeaseSet ليكون **أبطأ بكثير من مرة واحدة في الثانية** لكل Destination (الوجهة) - إذا كان النشر أسرع، فتأكد من أن كل LeaseSet جديد لديه وقت `published` متأخراً بما لا يقل عن ثانية واحدة - سترفض Floodfills الـ LeaseSet إذا لم يكن وقت `published` أحدث من الإصدار الحالي - الفاصل الزمني الأدنى الموصى به: 10–60 ثانية بين عمليات النشر

**أمثلة حسابية:**

**LeaseSet2 (بحد أقصى 11 دقيقة):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 660 (seconds)
Actual expiration = 1704067200 + 660 = 1704067860 (2024-01-01 00:11:00 UTC)
```
**MetaLeaseSet (بحد أقصى 18.2 ساعة):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 65535 (seconds)
Actual expiration = 1704067200 + 65535 = 1704132735 (2024-01-01 18:12:15 UTC)
```
**إدارة الإصدارات:** - يُعتبر LeaseSet "أحدث" إذا كان الطابع الزمني لـ `published` أكبر - تقوم Floodfills بتخزين ونشر أحدث إصدار فقط - توخَّ الحذر عندما يتطابق أقدم Lease (مدخل ضمن LeaseSet) مع أقدم Lease في LeaseSet السابق

---

### LeaseSet2 (النوع 3)

**الوصف:** تنسيق LeaseSet حديث بمفاتيح تشفير متعددة، وتواقيع غير متصلة بالإنترنت، وسجلات خدمة. المعيار الحالي لخدمات I2P المخفية.

**المقدمة:** الإصدار 0.9.38 (انظر [المقترح 123](/proposals/123-new-netdb-entries/))

**البنية:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes (varies with offline signature)

options :: Mapping
           Key-value pairs for service records and metadata
           Length: 2+ bytes (size field + data)

numk :: Integer (1 byte)
        Number of encryption keys
        Range: 1 to (implementation-defined maximum, typically 8)

keytype :: 2-byte encryption type
           See PublicKey type table

keylen :: 2-byte key length
          Must match keytype specification

encryption_key :: PublicKey
                  Length: keylen bytes
                  Type: keytype

[Repeat keytype/keylen/encryption_key for each key]

num :: Integer (1 byte)
       Number of Lease2s
       Range: 1-16 (at least one required)

leases :: Array of Lease2 structures
          Length: $num × 40 bytes

signature :: Signature
             Length determined by signing key type
             Signed over entire structure including database type prefix
```
**تخزين قاعدة البيانات:** - **نوع قاعدة البيانات:** 3 - **المفتاح:** تجزئة SHA-256 لـ Destination (الوجهة) - **القيمة:** البنية الكاملة لـ LeaseSet2

**حساب التوقيع:**

```
Data to sign: database_type (1 byte, value=3) || complete LeaseSet2 data

Verification:
1. Prepend database type byte (0x03) to LeaseSet2 data
2. If offline signature present:
   - Verify offline signature against Destination key
   - Verify LeaseSet2 signature against transient key
3. Else:
   - Verify LeaseSet2 signature against Destination key
```
### ترتيب أولوية مفتاح التشفير

**بالنسبة إلى LeaseSet المنشور (الخادم):** - تُدرَج المفاتيح وفق ترتيب تفضيل الخادم (الأكثر تفضيلاً أولاً) - ينبغي على العملاء الذين يدعمون أنواعاً متعددة احترام تفضيل الخادم - اختر أول نوع مدعوم من القائمة - عموماً، تكون أنواع المفاتيح ذات الأرقام الأعلى (الأحدث) أكثر أماناً/كفاءة - الترتيب الموصى به: سرد المفاتيح بترتيب عكسي حسب رمز النوع (الأحدث أولاً)

**مثال على تفضيل الخادم:**

```
numk = 2
Key 0: X25519 (type 4, 32 bytes)         [Most preferred]
Key 1: ElGamal (type 0, 256 bytes)       [Legacy compatibility]
```
**بالنسبة إلى LeaseSet غير المنشور (العميل):** - ترتيب المفاتيح عملياً لا يهم (نادراً ما تُحاوَل الاتصالات إلى العملاء) - اتبع نفس الاصطلاح للحفاظ على الاتساق

**اختيار مفتاح العميل:** - احترام تفضيل الخادم (اختيار أول نوع مدعوم) - أو استخدام تفضيل يحدده التنفيذ - أو تحديد تفضيل مركّب بناءً على قدرات الطرفين

### تعيين الخيارات

**المتطلبات:** - يجب ترتيب الخيارات حسب المفتاح (ترتيب معجمي، ترتيب البايتات وفق UTF-8) - يضمن الفرز ثبات التوقيع - غير مسموح بالمفاتيح المكررة

**التنسيق القياسي ([المقترح 167](/proposals/167-service-records/)):**

اعتبارًا من API 0.9.66 (يونيو 2025، الإصدار 2.9.0)، تتبع خيارات سجل الخدمة تنسيقًا موحدًا. راجع [المقترح 167](/proposals/167-service-records/) للاطلاع على المواصفة الكاملة.

**تنسيق خيار سجل الخدمة:**

```
Key: _service._proto
Value: record_type ttl [priority weight] port target [appoptions]

service :: Symbolic name of service (lowercase, [a-z0-9-])
           Examples: smtp, http, irc, mumble
           Use standard identifiers from IANA Service Name Registry
           or Linux /etc/services when available

proto :: Transport protocol (lowercase, [a-z0-9-])
         "tcp" = streaming protocol
         "udp" = repliable datagrams
         Protocol indicators for raw datagrams may be defined later

record_type :: "0" (self-reference) or "1" (SRV record)

ttl :: Time to live in seconds (positive integer)
       Recommended minimum: 86400 (one day)
       Prevents frequent re-queries

For record_type = 0 (self-reference):
  port :: I2CP port number (non-negative integer)
  appoptions :: Optional application-specific data (no spaces or commas)

For record_type = 1 (SRV record):
  priority :: Lower value = more preferred (non-negative integer)
  weight :: Relative weight for same priority, higher = more likely (non-negative)
  port :: I2CP port number (non-negative integer)
  target :: Hostname or b32 of destination (lowercase)
            Format: "example.i2p" or "aaaaa...aaaa.b32.i2p"
            Recommend b32 unless hostname is "well known"
  appoptions :: Optional application-specific data (no spaces or commas)
```
**أمثلة على سجلات الخدمة:**

**1. خادم SMTP يشير إلى نفسه:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "0 999999 25"

Meaning: This destination provides SMTP service on I2CP port 25
```
**2. خادم SMTP خارجي واحد:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p"

Meaning: SMTP service provided by bbbb...bbbb on port 25
         TTL = 1 day, single server (priority=0, weight=0)
```
**3. خوادم SMTP متعددة (موازنة التحميل):**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p,1 86400 1 0 25 cccc...cccc.b32.i2p"

Meaning: Two SMTP servers
         bbbb...bbbb (priority=0, preferred)
         cccc...cccc (priority=1, backup)
```
**4. خدمة HTTP مع خيارات التطبيق:**

```
Option: "_http._tcp" = "0 86400 80 tls=1.3;cert=ed25519"

Meaning: HTTP on port 80 with TLS 1.3 and EdDSA certificates
```
**توصيات TTL (مدة الحياة):** - الحد الأدنى: 86400 ثانية (يوم واحد) - TTL أطول يقلّل حمل الاستعلامات على netdb - تحقيق توازن بين تقليل الاستعلامات ونشر تحديثات الخدمة - للخدمات المستقرة: 604800 (7 أيام) أو أطول

**ملاحظات التنفيذ:**

1. **مفاتيح التشفير (اعتبارًا من 0.9.44):**
   - ElGamal (خوارزمية إلجامال للتشفير) (النوع 0، 256 بايت): توافق مع الإصدارات القديمة
   - X25519 (خوارزمية تبادل مفاتيح بيضوية) (النوع 4، 32 بايت): المعيار الحالي
   - MLKEM variants (خوارزمية تشفير مقاومة للكمّ): بعد-كمومي (بيتا، غير نهائي)

2. **التحقق من طول المفتاح:**
   - Floodfills والعملاء يجب أن يكونوا قادرين على تحليل أنواع مفاتيح غير معروفة
   - استخدم الحقل keylen لتخطي المفاتيح غير المعروفة
   - لا تفشل عملية التحليل إذا كان نوع المفتاح غير معروف

3. **الطابع الزمني للنشر:**
   - راجع ملاحظات LeaseSet2Header بخصوص الحدّ من المعدّل
   - حد أدنى لفاصل زمني مقداره ثانية واحدة بين عمليات النشر
   - موصى به: 10-60 ثانية بين عمليات النشر

4. **ترحيل نوع التشفير:**
   - دعم مفاتيح متعددة يتيح انتقالاً تدريجياً
   - أدرِج كلاً من المفاتيح القديمة والجديدة خلال فترة الانتقال
   - أزِل المفتاح القديم بعد انقضاء فترة كافية لترقية العملاء

**توثيق JavaDoc:** [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)

---

### MetaLease (مصطلح تقني ضمن I2P)

**الوصف:** بنية Lease (مدخل خدمة في I2P) لـ MetaLeaseSet يمكنها الإشارة إلى LeaseSets أخرى بدلًا من tunnels. تُستخدم لموازنة الأحمال والتكرار.

**المقدمة:** الإصدار 0.9.38، ومقرّر العمل به في 0.9.40 (انظر [المقترح 123](/proposals/123-new-netdb-entries/))

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of:
             - Gateway RouterIdentity (for type 1), OR
             - Another MetaLeaseSet destination (for type 3/5/7)

flags :: 3 bytes
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Entry type (see table below)
         Bits 23-4: Reserved (must be 0)

cost :: 1 byte (0-255)
        Lower value = higher priority
        Used for load balancing

end_date :: 4-byte timestamp (seconds since epoch)
            Expiration time
            Rolls over in year 2106
```
**إجمالي الحجم:** 40 بايت

**نوع الإدخال (بتات الأعلام 3-0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown/invalid entry</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet (type 1, deprecated)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet2 (type 3)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to EncryptedLeaseSet (type 5)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align-center?">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to another MetaLeaseSet (type 7)</td></tr>
  </tbody>
</table>
**سيناريوهات الاستخدام:**

1. **موازنة الأحمال:**
   - MetaLeaseSet (مجموعة إيجار ميتا) مع مدخلات MetaLease (إيجار ميتا) متعددة
   - يشير كل إدخال إلى LeaseSet2 (مجموعة الإيجار الإصدار 2) مختلف
   - يختار العملاء بناءً على حقل التكلفة

2. **التكرار:**
   - مدخلات متعددة تشير إلى LeaseSets احتياطية
   - آلية بديلة إذا كان LeaseSet الأساسي غير متاح

3. **ترحيل الخدمة:**
   - MetaLeaseSet تشير إلى LeaseSet جديد
   - يتيح انتقال سلس بين Destinations (عناوين I2P)

**استخدام حقل التكلفة:** - تكلفة أقل = أولوية أعلى - تكلفة 0 = أعلى أولوية - تكلفة 255 = أدنى أولوية - ينبغي للعملاء تفضيل الإدخالات ذات التكلفة الأقل - قد تُوزَّع الأحمال عشوائياً بين الإدخالات متساوية التكلفة

**المقارنة مع Lease2:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">MetaLease</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by flags (3 bytes) + cost (1 byte)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Points To</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specific tunnel</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet or MetaLeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Usage</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Direct tunnel reference</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection/load balancing</td></tr>
  </tbody>
</table>
**توثيق JavaDoc:** [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)

---

### MetaLeaseSet (النوع 7)

**الوصف:** نوع من LeaseSet يحتوي على مدخلات MetaLease (مدخل فوقي)، مما يوفر توجيهاً غير مباشراً إلى LeaseSets أخرى. يُستخدم لموازنة الحمل، والتكرار، وترحيل الخدمات.

**المقدمة:** تم التعريف في الإصدار 0.9.38، مُجدول للعمل في 0.9.40 (انظر [المقترح 123](/proposals/123-new-netdb-entries/))

**الحالة:** المواصفة مكتملة. ينبغي التحقق من حالة النشر في بيئة الإنتاج باستخدام إصدارات I2P الحالية.

**البنية:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes

options :: Mapping
           Length: 2+ bytes (size + data)
           MUST be sorted by key

num :: Integer (1 byte)
       Number of MetaLease entries
       Range: 1 to (implementation-defined, recommend 1-16)

metaleases :: Array of MetaLease structures
              Length: $num × 40 bytes

numr :: Integer (1 byte)
        Number of revocation hashes
        Range: 0 to (implementation-defined, recommend 0-16)

revocations :: Array of Hash structures
               Length: $numr × 32 bytes
               SHA-256 hashes of revoked LeaseSet Destinations
```
**تخزين قاعدة البيانات:** - **نوع قاعدة البيانات:** 7 - **المفتاح:** تجزئة SHA-256 لـ Destination (الوجهة في I2P) - **القيمة:** البنية الكاملة لـ MetaLeaseSet (مجموعة leaseSet الوصفية)

**حساب التوقيع:**

```
Data to sign: database_type (1 byte, value=7) || complete MetaLeaseSet data

Verification:
1. Prepend database type byte (0x07) to MetaLeaseSet data
2. If offline signature present in header:
   - Verify offline signature against Destination key
   - Verify MetaLeaseSet signature against transient key
3. Else:
   - Verify MetaLeaseSet signature against Destination key
```
**سيناريوهات الاستخدام:**

**1. موازنة الحمل:**

```
MetaLeaseSet for primary.i2p:
  MetaLease 0: cost=0, points to server1.i2p LeaseSet2
  MetaLease 1: cost=0, points to server2.i2p LeaseSet2
  MetaLease 2: cost=0, points to server3.i2p LeaseSet2

Clients randomly select among equal-cost entries
```
**2. التبديل التلقائي عند الفشل:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to primary.i2p LeaseSet2
  MetaLease 1: cost=100, points to backup.i2p LeaseSet2

Clients prefer cost=0 (primary), fall back to cost=100 (backup)
```
**3. ترحيل الخدمة:**

```
MetaLeaseSet for old-domain.i2p:
  MetaLease 0: cost=0, points to new-domain.i2p LeaseSet2

Transparently redirects clients from old to new destination
```
**4. معمارية متعددة الطبقات:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to region1-meta.i2p (another MetaLeaseSet)
  MetaLease 1: cost=0, points to region2-meta.i2p (another MetaLeaseSet)

Each region MetaLeaseSet points to regional servers
Allows hierarchical load balancing
```
**قائمة الإبطال:**

تتيح قائمة الإبطال لـ MetaLeaseSet (هيكل بيانات يجمع عدة LeaseSets) إبطال LeaseSets المنشورة سابقًا بصورة صريحة:

- **الغرض:** تحديد وجهات معيّنة على أنها لم تعد صالحة
- **المحتويات:** تجزئات SHA-256 لهياكل الوجهة المُبطلة
- **الاستخدام:** يجب على العملاء عدم استخدام LeaseSets التي تظهر تجزئة وجهتها في قائمة الإبطال
- **القيمة النموذجية:** فارغة (numr=0) في معظم عمليات النشر

**مثال على الإبطال:**

```
Service migrates from dest-v1.i2p to dest-v2.i2p:
  MetaLease 0: points to dest-v2.i2p
  Revocations: [hash(dest-v1.i2p)]

Clients will use v2 and ignore v1 even if cached
```
**التعامل مع انتهاء الصلاحية:**

MetaLeaseSet (نوع بيانات في I2P) يستخدم LeaseSet2Header بحد أقصى expires=65535 ثانية (~18.2 ساعة):

- أطول بكثير من LeaseSet2 (حد أقصى ~11 دقيقة)
- مناسب للإحالة غير المباشرة الثابتة نسبياً
- يمكن أن يكون انتهاء صلاحية LeaseSets المُشار إليها أقصر
- يجب على العملاء التحقق من انتهاء صلاحية كل من MetaLeaseSet وLeaseSets المُشار إليها

**تعيين الخيارات:**

- استخدم نفس تنسيق خيارات LeaseSet2
- يمكن أن تتضمن سجلات الخدمة ([Proposal 167](/proposals/167-service-records/))
- يجب ترتيبها حسب المفتاح
- تصف سجلات الخدمة عادةً الخدمة النهائية، وليس indirection structure (بنية التوجيه غير المباشر)

**ملاحظات تنفيذ العميل:**

1. **عملية الحل:**
   ```
   1. Query netdb for MetaLeaseSet using SHA-256(Destination)
   2. Parse MetaLeaseSet, extract MetaLease entries
   3. Sort entries by cost (lower = better)
   4. For each entry in cost order:
      a. Extract LeaseSet hash from tunnel_gw field
      b. Determine entry type from flags
      c. Query netdb for referenced LeaseSet (may be another MetaLeaseSet)
      d. Check revocation list
      e. Check expiration
      f. If valid, use the LeaseSet; else try next entry
   ```

2. **التخزين المؤقت:**
   - خزّن مؤقتاً كلّاً من MetaLeaseSet (مجموعة إيجارات وصفية) وLeaseSets المشار إليها
   - تحقّق من انتهاء الصلاحية في كلا المستويين
   - راقب نشر إصدار محدّث من MetaLeaseSet

3. **Failover (التحويل التلقائي عند الفشل):**
   - إذا فشل الإدخال المفضّل، جرّب الخيار التالي الأقل تكلفة
   - فكّر في وسم الإدخالات الفاشلة كغير متاحة مؤقتًا
   - أعد التحقق دوريًا للتحقق من التعافي

**حالة التنفيذ:**

[المقترح 123](/proposals/123-new-netdb-entries/) يشير إلى أن بعض الأجزاء لا تزال "قيد التطوير." ينبغي على المنفذين: - التحقق من جاهزية الإنتاج في إصدار I2P المستهدف - اختبار دعم MetaLeaseSet (نوع «LeaseSet» فوقي/تجميعي في I2P) قبل النشر - التحقق من وجود مواصفات محدّثة في إصدارات I2P الأحدث

**JavaDoc (توثيق Java):** [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)

---

### EncryptedLeaseSet (النوع 5)

**الوصف:** LeaseSet مشفّر و blinded (إعماء) لتعزيز الخصوصية. لا يظهر سوى المفتاح العام blinded والبيانات الوصفية؛ أما الـ leases (سجلات الربط المؤقتة) الفعلية ومفاتيح التشفير فهي مشفّرة.

**المقدمة:** تم تعريفه في 0.9.38، أصبح فعّالًا في 0.9.39 (انظر [المقترح 123](/proposals/123-new-netdb-entries/))

**البنية:**

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

sigtype :: 2-byte signature type
           Type of blinded_public_key
           MUST be RedDSA_SHA512_Ed25519 (type 11)

blinded_public_key :: SigningPublicKey (32 bytes for RedDSA)
                      Blinded version of Destination signing key
                      Used to verify signature on EncryptedLeaseSet

published :: 4-byte timestamp (seconds since epoch)
             Publication time
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published
           Maximum: 65535 seconds (18.2 hours)
           Practical maximum for LeaseSet data: ~660 seconds (~11 min)

flags :: 2 bytes
         Bit 0: Offline signature present (0=no, 1=yes)
         Bit 1: Unpublished (0=published, 1=client-side only)
         Bits 15-2: Reserved (must be 0)

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 = 1
                     Variable length

len :: 2-byte integer
       Length of encrypted_data
       Range: 1 to 65535

encrypted_data :: Encrypted payload
                  Length: len bytes
                  Contains encrypted LeaseSet2 or MetaLeaseSet

signature :: Signature (64 bytes for RedDSA)
             Length determined by sigtype
             Signed by blinded_public_key or transient key
```
**تخزين قاعدة البيانات:** - **نوع قاعدة البيانات:** 5 - **المفتاح:** تجزئة SHA-256 لـ **الوجهة المُعمّاة** (ليست الوجهة الأصلية) - **القيمة:** البنية الكاملة لـ EncryptedLeaseSet

**الفروقات الجوهرية مقارنةً بـ LeaseSet2:**

1. **لا يستخدم بنية LeaseSet2Header** (يحتوي على حقول متشابهة لكن بتخطيط مختلف)
2. **مفتاح عام مُعمّى** بدلاً من Destination الكامل (معرّف الوجهة في I2P)
3. **حمولة مُشفّرة** بدلاً من leases (سجلات المسار في I2P) والمفاتيح غير المشفّرة
4. **مفتاح قاعدة البيانات هو تجزئة لـ Destination المُعمّى**، وليس Destination الأصلي

**حساب التوقيع:**

```
Data to sign: database_type (1 byte, value=5) || complete EncryptedLeaseSet data

Verification:
1. Prepend database type byte (0x05) to EncryptedLeaseSet data
2. If offline signature present (flags bit 0 = 1):
   - Verify offline signature against blinded public key
   - Verify EncryptedLeaseSet signature against transient key
3. Else:
   - Verify EncryptedLeaseSet signature against blinded public key
```
**متطلب نوع التوقيع:**

**يجب استخدام RedDSA_SHA512_Ed25519 (النوع 11):** - مفاتيح عامة معمّاة بطريقة الإعماء (blinding) بطول 32 بايت - تواقيع بطول 64 بايت - مطلوب لضمان خصائص الأمان المتعلقة بالإعماء - راجع [مواصفة Red25519](//docs/specs/red25519-signature-scheme/

**الفروق الرئيسية عن EdDSA:** - المفاتيح الخاصة باستخدام الاختزال المعياري (وليس clamping: تعديل بتّات المفتاح الخاص بفرض قيود ثابتة) - تتضمن التواقيع 80 بايتًا من البيانات العشوائية - تستخدم المفاتيح العامة مباشرة (وليس التجزئات) - تمكّن عملية إعماء آمنة

**الإعماء والتشفير:**

راجع [مواصفة EncryptedLeaseSet](/docs/specs/encryptedleaseset/) (نوع مشفّر من الـ leaseSet) للاطلاع على التفاصيل الكاملة:

**1. إعماء المفتاح:**

```
Blinding process (daily rotation):
  secret = HKDF(original_signing_private_key, date_string, "i2pblinding1")
  alpha = SHA-256(secret) mod L (where L is Ed25519 group order)
  blinded_private_key = alpha * original_private_key
  blinded_public_key = alpha * original_public_key
```
**2. موقع قاعدة البيانات:**

```
Client publishes to:
  Key = SHA-256(blinded_destination)
  
Where blinded_destination uses:
  - Blinded public key (signing key)
  - Same unused public key field (random)
  - Same certificate structure
```
**3. طبقات التشفير (ثلاث طبقات):**

**الطبقة 1 - طبقة المصادقة (وصول العملاء):** - التشفير: ChaCha20 (شيفرة تدفقية) - اشتقاق المفاتيح: HKDF مع أسرار خاصة بكل عميل - يمكن للعملاء المُصادَقين فك تشفير الطبقة الخارجية

**الطبقة 2 - طبقة التشفير:** - التشفير: ChaCha20 - المفتاح: مشتق من DH (تبادل المفاتيح ديفي-هيلمان) بين العميل والخادم - يتضمن LeaseSet2 أو MetaLeaseSet الفعلي

**الطبقة 3 - LeaseSet الداخلي:** - نسخة كاملة من LeaseSet2 أو MetaLeaseSet - يتضمن جميع tunnels ومفاتيح التشفير والخيارات - لا يمكن الوصول إليه إلا بعد فك التشفير بنجاح

**اشتقاق مفتاح التشفير:**

```
Client has: ephemeral_client_private_key
Server has: ephemeral_server_public_key (in encrypted_data)

Shared secret = X25519(client_private, server_public)
Encryption key = HKDF(shared_secret, context_info, "i2pblinding2")
```
**عملية الاكتشاف:**

**للعملاء المصرَّح لهم:**

```
1. Client knows original Destination
2. Client computes current blinded Destination (based on current date)
3. Client computes database key: SHA-256(blinded_destination)
4. Client queries netdb for EncryptedLeaseSet using blinded key
5. Client decrypts layer 1 using authorization credentials
6. Client decrypts layer 2 using DH shared secret
7. Client extracts inner LeaseSet2/MetaLeaseSet
8. Client uses tunnels from inner LeaseSet for communication
```
**للعُملاء غير المصرّح لهم:** - لا يمكنهم فك التشفير حتى لو عثروا على EncryptedLeaseSet - لا يمكنهم تحديد Destination (الوجهة في I2P) الأصلية من الإصدار المُعمّى - لا يمكنهم ربط EncryptedLeaseSets عبر فترات تعمية مختلفة (تدوير يومي)

**أوقات انتهاء الصلاحية:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Content Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet (outer)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full 2-byte expires field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 sec (≈11 min)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actual lease data practical maximum</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection can be longer-lived</td></tr>
  </tbody>
</table>
**الطابع الزمني للنشر:**

نفس المتطلبات مثل LeaseSet2Header: - يجب أن يزداد بمقدار ثانية واحدة على الأقل بين عمليات النشر - تقوم Floodfills برفضه إذا لم يكن أحدث من الإصدار الحالي - موصى به: 10–60 ثانية بين عمليات النشر

**تواقيع دون اتصال مع LeaseSets المشفّرة:**

اعتبارات خاصة عند استخدام التواقيع غير المتصلة (offline signatures): - Blinded public key (المفتاح العام المموّه) يتبدّل يوميًا - يجب إعادة توليد Offline signature يوميًا باستخدام blinded key جديد - أو استخدم Offline signature على LeaseSet الداخلية، وليس على EncryptedLeaseSet الخارجية - راجع ملاحظات [المقترح 123](/proposals/123-new-netdb-entries/)

**ملاحظات التنفيذ:**

1. **تفويض العميل:**
   - يمكن تفويض عدة عملاء بمفاتيح مختلفة
   - يمتلك كل عميل مُفوَّض بيانات اعتماد لفك التشفير فريدة
   - إبطال تفويض العميل بتغيير مفاتيح التفويض

2. **تدوير المفاتيح اليومي:**
   - تتغيّر Blinded keys (مفاتيح مُعمّاة بغرض الإخفاء) عند منتصف الليل بتوقيت UTC
   - يجب على العملاء إعادة حساب blinded Destination (الوجهة المعمّاة) يومياً
   - تصبح EncryptedLeaseSets (LeaseSets مشفّرة) القديمة غير قابلة للاكتشاف بعد التدوير

3. **خصائص الخصوصية:**
   - لا يمكن لـ Floodfills تحديد Destination (الوجهة) الأصلية
   - لا يمكن للعملاء غير المصرّح لهم الوصول إلى الخدمة
   - لا يمكن ربط فترات التعمية المختلفة
   - لا توجد بيانات وصفية بنص صريح باستثناء أوقات الانتهاء

4. **الأداء:**
   - يجب على العملاء إجراء حساب blinding (الإعماء) اليومي
   - يضيف التشفير ثلاثي الطبقات حملاً حسابياً إضافياً
   - ينبغي النظر في التخزين المؤقت لـ LeaseSet الداخلي بعد فك التشفير

**الاعتبارات الأمنية:**

1. **إدارة مفاتيح التفويض:**
   - توزيع بيانات اعتماد تفويض العملاء بشكل آمن
   - استخدام بيانات اعتماد فريدة لكل عميل لتمكين الإبطال الدقيق
   - تدوير مفاتيح التفويض بشكل دوري

2. **مزامنة الساعة:**
   - يعتمد الـ blinding (إعماء/تعمية لأغراض الخصوصية) اليومي على تواريخ UTC المتزامنة
   - قد يتسبب انحراف الساعة في فشل عمليات البحث
   - فكّر في دعم blinding لليوم السابق/التالي للتسامح مع انحراف الساعة

3. **تسرب البيانات الوصفية:**
   - حقلا Published و expires يكونان نصاً صريحاً (غير مُشفَّر)
   - قد يكشف تحليل الأنماط خصائص الخدمة
   - اجعل فترات النشر عشوائية إذا كان ذلك مصدر قلق

**JavaDoc:** [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)

---

## هياكل Router

### RouterAddress (عنوان الـrouter)

**الوصف:** يحدّد معلومات الاتصال الخاصة بـ router عبر بروتوكول نقل محدّد.

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-//-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

cost :: Integer (1 byte)
        Relative cost, 0=free, 255=expensive
        Typical values:
          5-6: SSU2
          10-11: NTCP2

expiration :: Date (8 bytes)
              MUST BE ALL ZEROS (see critical note below)

transport_style :: String (1-256 bytes)
                   Transport protocol name
                   Current values: "SSU2", "NTCP2"
                   Legacy: "SSU", "NTCP" (removed)

options :: Mapping
           Transport-specific configuration
           Common options: "host", "port"
           Transport-specific options vary
```
**حرج - حقل انتهاء الصلاحية:**

⚠️ **يجب ضبط حقل انتهاء الصلاحية إلى جميع الأصفار (8 بايتات صفرية).**

- **السبب:** منذ الإصدار 0.9.3، تؤدي قيمة انتهاء الصلاحية غير صفرية إلى فشل التحقق من التوقيع
- **التاريخ:** كان حقل انتهاء الصلاحية غير مستخدم في الأصل، وكان دائمًا null
- **الحالة الحالية:** تم التعرف على الحقل مرة أخرى اعتبارًا من 0.9.12، لكن يجب انتظار ترقية الشبكة
- **التنفيذ:** يُعيَّن دائمًا إلى 0x0000000000000000

أي قيمة انتهاء صلاحية غير صفرية ستؤدي إلى فشل التحقق من توقيع RouterInfo (بنية معلومات الـ router في I2P).

### بروتوكولات النقل

**البروتوكولات الحالية (اعتبارًا من الإصدار 2.10.0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>SSU2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54 (May 2022)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>NTCP2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36 (Aug 2018)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50 (May 2021)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use NTCP2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0 (Dec 2023)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use SSU2</td></tr>
  </tbody>
</table>
**قيم أنماط النقل:** - `"SSU2"`: النقل الحالي المعتمد على UDP - `"NTCP2"`: النقل الحالي المعتمد على TCP - `"NTCP"`: قديمة، أُزيلت (لا تستخدم) - `"SSU"`: قديمة، أُزيلت (لا تستخدم)

### الخيارات المشتركة

تتضمن جميع بروتوكولات النقل عادةً:

```
"host" = IPv4 or IPv6 address or hostname
"port" = Port number (1-65535)
```
### خيارات خاصة بـ SSU2

راجع [مواصفة SSU2](/docs/specs/ssu2/) للحصول على التفاصيل الكاملة.

**الخيارات المطلوبة:**

```
"host" = IP address (IPv4 or IPv6)
"port" = UDP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Introduction key X25519 (Base64, 44 characters = 32 bytes)
"v" = "2" (protocol version)
```
**خيارات اختيارية:**

```
"caps" = Capability string (e.g., "B" for bandwidth tier)
"ihost0", "ihost1", ... = Introducer IP addresses
"iport0", "iport1", ... = Introducer ports  
"ikey0", "ikey1", ... = Introducer static keys (Base64, 44 chars)
"itag0", "itag1", ... = Introducer relay tags
"iexp0", "iexp1", ... = Introducer expiration timestamps
"mtu" = Maximum transmission unit (default 1500, min 1280)
"mtu6" = IPv6 MTU (if different from IPv4)
```
**مثال على SSU2 RouterAddress:**

```
cost: 5
expiration: 0x0000000000000000
transport_style: "SSU2"
options:
  host=198.51.100.42
  port=12345
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=QW5vdGhlciBTYW1wbGUgS2V5IGZvciBJbnRyb2R1Y3Rpb24=
  v=2
  caps=BC
  mtu=1472
```
### الخيارات الخاصة بـ NTCP2

انظر [مواصفة NTCP2](/docs/specs/ntcp2/) للاطلاع على التفاصيل الكاملة.

**الخيارات المطلوبة:**

```
"host" = IP address (IPv4 or IPv6)
"port" = TCP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Initialization vector (Base64, 24 characters = 16 bytes)
"v" = "2" (protocol version)
```
**خيارات اختيارية (منذ 0.9.50):**

```
"caps" = Capability string
```
**مثال على NTCP2 (بروتوكول نقل في I2P) RouterAddress:**

```
cost: 10
expiration: 0x0000000000000000
transport_style: "NTCP2"
options:
  host=198.51.100.42
  port=23456
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=U2FtcGxlIElWIGhlcmU=
  v=2
```
### ملاحظات التنفيذ

1. **قيم التكلفة:**
   - UDP (SSU2) عادة أقل تكلفة (5-6) بفضل الكفاءة
   - TCP (NTCP2) عادة أعلى تكلفة (10-11) بسبب الحمل الإضافي
   - التكلفة الأقل = وسيلة النقل المفضلة

2. **عناوين متعددة:**
   - قد تقوم Routers بنشر عدة إدخالات RouterAddress
   - بروتوكولات نقل مختلفة (SSU2 وNTCP2)
   - إصدارات IP مختلفة (IPv4 وIPv6)
   - يختار العملاء بناءً على التكلفة والقدرات

3. **اسم المضيف مقابل IP:**
   - تُفضَّل عناوين IP لتحسين الأداء
   - يتم دعم أسماء المضيف، لكنها تضيف عبئًا إضافيًا لاستعلام DNS
   - فكّر في استخدام IP لـ RouterInfos (بيانات تعريف router في I2P) المنشورة

4. **ترميز Base64:**
   - يتم ترميز جميع المفاتيح والبيانات الثنائية باستخدام Base64
   - Base64 القياسي (RFC 4648)
   - بدون padding (حشو) أو أحرف غير قياسية

**JavaDoc (توثيق جافا):** [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)

---

### RouterInfo

**الوصف:** معلومات منشورة كاملة عن router، مخزنة في قاعدة بيانات الشبكة (netDb). تتضمن الهوية والعناوين والقدرات.

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-//-+----+----+----+
|psiz| options                          |
+----+----+----+----+-//-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

router_ident :: RouterIdentity
                Length: 387+ bytes (typically 391 for X25519+EdDSA)

published :: Date (8 bytes)
             Publication timestamp (milliseconds since epoch)

size :: Integer (1 byte)
        Number of RouterAddress entries
        Range: 0-255

addresses :: Array of RouterAddress
             Variable length
             Each RouterAddress has variable size

peer_size :: Integer (1 byte)
             Number of peer hashes (ALWAYS 0)
             Historical, unused feature

options :: Mapping
           Router capabilities and metadata
           MUST be sorted by key

signature :: Signature
             Length determined by router_ident signing key type
             Typically 64 bytes (EdDSA)
             Signed by router_ident's SigningPrivateKey
```
**تخزين قاعدة البيانات:** - **نوع قاعدة البيانات:** 0 - **المفتاح:** تجزئة SHA-256 لـ RouterIdentity - **القيمة:** البنية الكاملة لـ RouterInfo

**الطابع الزمني المنشور:** - تاريخ/وقت بحجم 8 بايت (ميلي ثانية منذ epoch (بداية زمن يونكس)) - يُستخدم لإدارة إصدارات RouterInfo - Routers تنشر RouterInfo جديدًا بشكل دوري - تحتفظ Floodfills بأحدث إصدار استنادًا إلى الطابع الزمني المنشور

**فرز العناوين:** - **تاريخيًا:** كانت routers القديمة جدًا تتطلب فرز العناوين حسب SHA-256 لبياناتها - **حاليًا:** الفرز غير مطلوب، ولا يستحق التنفيذ لأغراض التوافق - يمكن أن تكون العناوين بأي ترتيب

**حقل حجم النظير (تاريخي):** - **دائمًا 0** في I2P الحديثة - كان مقصودًا للمسارات المقيّدة (غير مُنفّذة) - لو تم تنفيذه، لَتَبِعَه ذلك العدد من تجزئات Router - قد تكون بعض التطبيقات القديمة قد اشترطت قائمة نظراء مُرتّبة

**تعيين الخيارات:**

يجب ترتيب الخيارات بحسب اسم المفتاح. تشمل الخيارات القياسية:

**خيارات القدرات:**

```
"caps" = Capability string
         Common values:
           f = Floodfill (network database)
           L or M or N or O = Bandwidth tier (L=lowest, O=highest)
           R = Reachable
           U = Unreachable/firewalled
           Example: "fLRU" = Floodfill, Low bandwidth, Reachable, Unreachable
```
**خيارات الشبكة:**

```
"netId" = Network ID (default "2" for main I2P network)
          Different values for test networks

"router.version" = I2P version string
                   Example: "0.9.67" or "2.10.0"
```
**الخيارات الإحصائية:**

```
"stat_uptime" = Uptime in milliseconds
"coreVersion" = Core I2P version
"router.version" = Full router version string
```
انظر [وثائق RouterInfo لقاعدة بيانات الشبكة](/docs/specs/common-structures/#routerInfo) (RouterInfo: سجل معلومات router) للاطلاع على القائمة الكاملة للخيارات القياسية.

**حساب التوقيع:**

```
Data to sign: Complete RouterInfo structure from router_ident through options

Verification:
1. Extract RouterIdentity from RouterInfo
2. Get SigningPublicKey from RouterIdentity (type determines algorithm)
3. Verify signature over all data preceding signature field
4. Signature must match signing key type and length
```
**RouterInfo (بيانات تعريف الـrouter) الحديثة النموذجية:**

```
RouterIdentity: 391 bytes (X25519+EdDSA with Key Certificate)
Published: 8 bytes
Size: 1 byte (typically 1-4 addresses)
RouterAddress × N: Variable (typically 200-500 bytes each)
Peer Size: 1 byte (value=0)
Options: Variable (typically 50-200 bytes)
Signature: 64 bytes (EdDSA)

Total: ~1000-2500 bytes typical
```
**ملاحظات التنفيذ:**

1. **عناوين متعددة:**
   - Routers عادةً تنشر من 1 إلى 4 عناوين
   - متغيرات IPv4 وIPv6
   - بروتوكولات النقل SSU2 و/أو NTCP2
   - كل عنوان مستقل

2. **إدارة الإصدارات:**
   - يحتوي RouterInfo (بيانات تعريف الـ router في I2P) الأحدث على طابعٍ زمني لحقل `published` أحدث من السابق
   - تعيد routers النشر كل ~2 ساعة أو عند تغيّر العناوين
   - تخزّن Floodfills (عُقَد floodfill في I2P) وتبثّ أحدث إصدار فقط

3. **التحقق:**
   - تحقق من التوقيع قبل قبول RouterInfo (هيكل معلومات Router)
   - تحقق من أن حقل انتهاء الصلاحية كله أصفار في كل RouterAddress (عنوان Router)
   - تحقق من أن خريطة الخيارات مرتبة حسب المفتاح
   - تحقق من أن أنواع الشهادات والمفاتيح معروفة/مدعومة

4. **قاعدة بيانات الشبكة:**
   - تقوم Floodfills بتخزين RouterInfo مفهرساً حسب Hash(RouterIdentity)
   - تُخزَّن لمدة تقارب يومين بعد آخر نشر
   - Routers ترسل استعلامات إلى floodfills لاكتشاف Routers أخرى

**JavaDoc:** [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

---

## ملاحظات التنفيذ

### ترتيب البايتات (Endianness)

**الافتراضي: Big-Endian (ترتيب بايتات الشبكة)**

تستخدم معظم بُنى I2P ترتيب البايتات big-endian (الأعلى أهمية أولاً): - جميع أنواع الأعداد الصحيحة (1-8 بايت) - الطوابع الزمنية للتواريخ - TunnelId - بادئة طول السلسلة - أنواع الشهادات وأطوالها - رموز نوع المفتاح - حقول حجم التعيين

**استثناء: Little-Endian (ترتيب البايت الصغير أولاً)**

تستخدم أنواع المفاتيح التالية ترميز **little-endian** (ترتيب البايتات من الأصغر إلى الأكبر): - مفاتيح التشفير **X25519** (النوع 4) - مفاتيح التوقيع **EdDSA_SHA512_Ed25519** (النوع 7) - مفاتيح التوقيع **EdDSA_SHA512_Ed25519ph** (النوع 8) - مفاتيح التوقيع **RedDSA_SHA512_Ed25519** (النوع 11)

**التنفيذ:**

```java
// Big-endian (most structures)
int value = ((bytes[0] & 0xFF) << 24) | 
            ((bytes[1] & 0xFF) << 16) |
            ((bytes[2] & 0xFF) << 8) | 
            (bytes[3] & 0xFF);

// Little-endian (X25519, EdDSA, RedDSA)
int value = (bytes[0] & 0xFF) | 
            ((bytes[1] & 0xFF) << 8) |
            ((bytes[2] & 0xFF) << 16) | 
            ((bytes[3] & 0xFF) << 24);
```
### ترقيم إصدارات البنية

**لا تفترض أحجامًا ثابتة أبدًا:**

العديد من البُنى ذات طول متغير: - RouterIdentity (معرف Router): 387+ بايت (ليس دائما 387) - Destination: 387+ بايت (ليس دائما 387) - LeaseSet2 (الإصدار 2 من LeaseSet): يتفاوت بشكل ملحوظ - Certificate: 3+ بايت

**اقرأ دائمًا حقول الحجم:** - طول الشهادة عند البايتين 1-2 - حجم التعيين في البداية - KeysAndCert (مجموعة المفاتيح والشهادة) يُحسب دائمًا على أنه 384 + 3 + certificate_length

**تحقق من البيانات الزائدة:** - منع البيانات اللاحقة غير المرغوب فيها بعد البُنى الصالحة - التحقق من أن أطوال الشهادات تطابق أنواع المفاتيح - فرض الأطوال المتوقعة بدقة للأنواع ذات الحجم الثابت

### التوصيات الحالية (أكتوبر 2025)

**بالنسبة لهويات Router الجديدة:**

```
Encryption: X25519 (type 4, 32 bytes)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/ar/proposals/161-ri-dest-padding/)
```
**بالنسبة إلى الوجهات الجديدة:**

```
Unused Public Key Field: 256 bytes random (compressible)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/ar/proposals/161-ri-dest-padding/)
```
**بالنسبة إلى LeaseSets الجديدة (وصف لمسارات الدخول إلى وجهة في I2P):**

```
Type: LeaseSet2 (type 3)
Encryption Keys: X25519 (type 4, 32 bytes)
Leases: At least 1, typically 3-5
Options: Include service records per [Proposal 167](/proposals/167-service-records/)
Signature: EdDSA (64 bytes)
```
**للخدمات المشفرة:**

```
Type: EncryptedLeaseSet (type 5)
Blinding: RedDSA_SHA512_Ed25519 (type 11)
Inner LeaseSet: LeaseSet2 (type 3)
Rotation: Daily blinding key rotation
Authorization: Per-client encryption keys
```
### ميزات مهملة - لا تستخدم

**التشفير المهمل:** - ElGamal (النوع 0) لهويات Router (مهمل منذ 0.9.58) - تشفير ElGamal/AES+SessionTag (وسم الجلسة) (استخدم ECIES-X25519)

**خيارات التوقيع المهملة:** - DSA_SHA1 (type 0) لهويات Router (مهمل منذ 0.9.58) - متغيرات ECDSA (types 1-3) للتنفيذات الجديدة - متغيرات RSA (types 4-6) باستثناء ملفات SU3

**تنسيقات الشبكة المتوقفة عن الاستخدام:** - LeaseSet من النوع 1 (استخدم LeaseSet2) - Lease (44 بايت, استخدم Lease2) - تنسيق انتهاء صلاحية Lease الأصلي

**وسائط النقل المهملة:** - NTCP (أزيل في 0.9.50) - SSU (أزيل في 2.4.0)

**الشهادات المهملة:** - HASHCASH (النوع 1) - HIDDEN (النوع 2) - SIGNED (النوع 3) - MULTIPLE (النوع 4)

### اعتبارات أمنية

**توليد المفاتيح:** - استخدم دائماً مولدات أعداد عشوائية آمنة تشفيرياً - لا تعاود استخدام المفاتيح عبر سياقات مختلفة - احمِ المفاتيح الخاصة بضوابط التحكم في الوصول المناسبة - امسح بيانات المفاتيح من الذاكرة بشكل آمن عند الانتهاء

**التحقق من التوقيع:** - تحقّق دائمًا من التواقيع قبل الوثوق بالبيانات - تحقّق من أن طول التوقيع يطابق نوع المفتاح - تحقّق من أن البيانات الموقعة تتضمن الحقول المتوقعة - بالنسبة إلى الخرائط المرتبة، تحقّق من ترتيب الفرز قبل التوقيع/التحقق

**التحقق من صحة الطابع الزمني:** - تحقق من أن الأوقات المنشورة معقولة (ليست في مستقبل بعيد) - تحقق من أن تواريخ انتهاء فترات الإيجار لم تنقضِ - راعِ سماحية انحراف الساعة (±30 ثانية عادةً)

**قاعدة بيانات الشبكة:** - التحقق من صحة جميع الهياكل قبل التخزين - فرض حدود للحجم لمنع هجمات حجب الخدمة (DoS) - تقييد معدل الاستعلامات وعمليات النشر - التحقق من أن مفاتيح قاعدة البيانات تطابق تجزئات الهياكل

### ملاحظات التوافق

**التوافق مع الإصدارات السابقة:** - لا يزال دعم ElGamal و DSA_SHA1 قائماً لـ routers القديمة - تظل أنواع المفاتيح المهملة تعمل، لكن غير مستحسنة - الحشو القابل للضغط ([المقترح 161](/ar/proposals/161-ri-dest-padding/)) متوافق رجوعياً حتى الإصدار 0.6

**التوافق المستقبلي:** - يمكن تحليل أنواع المفاتيح غير المعروفة باستخدام حقول الطول - يمكن تجاوز أنواع الشهادات غير المعروفة باستخدام الطول - يجب التعامل مع أنواع التواقيع غير المعروفة بسلاسة - لا ينبغي أن يفشل المنفذون عند مواجهة ميزات اختيارية غير معروفة

**استراتيجيات الترحيل:** - دعم كلٍ من أنواع المفاتيح القديمة والجديدة خلال فترة الانتقال - يمكن لـ LeaseSet2 إدراج عدة مفاتيح تشفير - التواقيع غير المتصلة تمكّن تدوير المفاتيح بأمان - يتيح MetaLeaseSet ترحيل الخدمة بشفافية

### الاختبار والتحقق

**التحقّق من البنية:** - تحقّق من أن جميع حقول الطول ضمن النطاقات المتوقعة - تحقّق من أن البُنى ذات الطول المتغير تُحلَّل بشكل صحيح - تحقّق من أن التواقيع يتم التحقق من صحتها بنجاح - اختبر مع البُنى ذات الحد الأدنى والحد الأقصى للحجم

**الحالات الحدّية:** - سلاسل نصية بطول صفري - تعيينات فارغة - الحدّين الأدنى والأقصى لعدد الإيجارات - شهادة ذات حمولة بطول صفري - تراكيب كبيرة جداً (قريبة من الأحجام القصوى)

**التشغيل البيني:** - الاختبار مقابل التطبيق الرسمي لـ Java I2P - التحقق من التوافق مع i2pd - الاختبار باستخدام محتويات متنوعة لقاعدة بيانات الشبكة - التحقق مقابل متجهات اختبار معروفة بأنها صحيحة

---

## المراجع

### المواصفات

- [بروتوكول I2NP](/docs/specs/i2np/)
- [بروتوكول I2CP](/docs/specs/i2cp/)
- [نقل SSU2](/docs/specs/ssu2/)
- [نقل NTCP2](/docs/specs/ntcp2/)
- [بروتوكول Tunnel](/docs/specs/implementation/)
- [بروتوكول الداتاغرام](/docs/api/datagrams/)

### علم التشفير

- [نظرة عامة على التشفير](/docs/specs/cryptography/)
- [تشفير ElGamal/AES](/docs/legacy/elgamal-aes/)
- [تشفير ECIES-X25519](/docs/specs/ecies/)
- [ECIES لـ Routers](/docs/specs/ecies/#routers)
- [ECIES الهجين (ما بعد الكمّ)](/docs/specs/ecies/#hybrid)
- [تواقيع Red25519](/docs/specs/red25519-signature-scheme/)
- [LeaseSet مشفّر](/docs/specs/encryptedleaseset/)

### مقترحات

- [المقترح 123: مدخلات netDB الجديدة](/proposals/123-new-netdb-entries/)
- [المقترح 134: أنواع تواقيع GOST](/proposals/134-gost/)
- [المقترح 136: أنواع تواقيع تجريبية](/proposals/136-experimental-sigtypes/)
- [المقترح 145: ECIES-P256](/proposals/145-ecies/)
- [المقترح 156: ECIES Routers](/proposals/156-ecies-routers/)
- [المقترح 161: توليد الحشو](/ar/proposals/161-ri-dest-padding/)
- [المقترح 167: سجلات الخدمة](/proposals/167-service-records/)
- [المقترح 169: التشفير ما بعد الكمّي](/proposals/169-pq-crypto/)
- [فهرس جميع المقترحات](/proposals/)

### قاعدة بيانات الشبكة

- [نظرة عامة على قاعدة بيانات الشبكة (netDb)](/docs/specs/common-structures/)
- [الخيارات القياسية لـ RouterInfo](/docs/specs/common-structures/#routerInfo)

### مرجع JavaDoc لواجهة برمجة التطبيقات

- [حزمة البيانات الأساسية](http://docs.i2p-projekt.de/javadoc/net/i2p/data/)
- [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)
- [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)
- [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)
- [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)
- [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)
- [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)
- [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)
- [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)
- [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)
- [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)
- [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)
- [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)
- [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)
- [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)
- [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)
- [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)
- [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)
- [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)
- [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)
- [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)
- [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)
- [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)
- [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

### المعايير الخارجية

- **RFC 7748 (X25519):** المنحنيات الإهليلجية للأمان
- **RFC 7539 (ChaCha20):** ChaCha20 وPoly1305 لبروتوكولات IETF
- **RFC 4648 (Base64):** ترميزات البيانات Base16 وBase32 وBase64
- **FIPS 180-4 (SHA-256):** معيار التجزئة الآمنة
- **FIPS 204 (ML-DSA):** معيار التوقيع الرقمي القائم على Module-Lattice (شبكات الوحدات)
- [سجل خدمات IANA](http://www.dns-sd.org/ServiceTypes.html)

### موارد المجتمع

- [موقع I2P](/)
- [منتدى I2P](https://i2pforum.net)
- [GitLab الخاص بـ I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)
- [مرآة I2P على GitHub](https://github.com/i2p/i2p.i2p)
- [فهرس الوثائق التقنية](/docs/)

### معلومات الإصدار

- [إصدار I2P 2.10.0](/ar/blog/2025/09/08/i2p-2.10.0-release/)
- [سجل الإصدارات](https://github.com/i2p/i2p.i2p/blob/master/history.txt)
- [سجل التغييرات](https://github.com/i2p/i2p.i2p/blob/master/debian/changelog)

---

## الملحق: جداول مرجعية سريعة

### مرجع سريع لأنواع المفاتيح

**المعيار الحالي (مُوصى به لجميع عمليات التنفيذ الجديدة):** - **التشفير:** X25519 (النوع 4، 32 بايت، ترتيب بايت صغير) - **التوقيع:** EdDSA_SHA512_Ed25519 (النوع 7، 32 بايت، ترتيب بايت صغير)

**قديم (مدعوم ولكن مُهمَل):** - **التشفير:** ElGamal (خوارزمية تشفير غير متناظرة) (النوع 0، 256 بايت، big-endian) - **التوقيع:** DSA_SHA1 (خوارزمية توقيع رقمي تعتمد SHA-1) (النوع 0، خاص 20 بايت / عام 128 بايت، big-endian)

**متخصص:** - **التوقيع (LeaseSet مشفر):** RedDSA_SHA512_Ed25519 (النوع 11، 32 بايت، بترتيب بايت صغير)

**ما بعد الكمومي (بيتا، غير نهائي):** - **تشفير هجين:** متغيرات MLKEM_X25519 (الأنواع 5-7) - **تشفير ما بعد الكمومي الخالص:** متغيرات MLKEM (خوارزمية تغليف مفاتيح ما بعد كمومي) (لم تُخصَّص رموز أنواع بعد)

### مرجع سريع لحجم البنية

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Minimum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Integer</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Date</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SessionKey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelId</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Certificate</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,538 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KeysAndCert</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterIdentity</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1200 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈800 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterAddress</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈150 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈300 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
  </tbody>
</table>
### مرجع سريع لأنواع قاعدة البيانات

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(RouterIdentity)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use LeaseSet2 instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Blinded Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Defined</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Verify production status</td></tr>
  </tbody>
</table>
### مرجع سريع لبروتوكول النقل

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Port Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1pxsolid var(--color-border); padding:0.5rem;">Removed in 2.4.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed in 0.9.50</td></tr>
  </tbody>
</table>
### مرجع سريع لمعالم الإصدارات

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">API</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6.x</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2005</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination encryption disabled</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2013</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Key Certificates introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA support added</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router Key Certificates</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Aug 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, X25519 for Destinations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet working</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jul 2020</td><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 for Router Identities</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2021</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP removed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2022</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jan 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 161](/ar/proposals/161-ri-dest-padding/) padding (release 2.1.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mar 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/DSA deprecated for RIs (2.2.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jun 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 167](/proposals/167-service-records/) service records (2.9.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ML-KEM beta support (2.10.0)</td></tr>
  </tbody>
</table>
---
