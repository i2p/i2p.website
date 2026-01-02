---
title: "LeaseSet مشفر"
description: "تنسيق LeaseSet خاضع للتحكم في الوصول لـ Destinations الخاصة (وجهات I2P)"
slug: "encryptedleaseset"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## نظرة عامة

تحدد هذه الوثيقة آليات blinding (الإعماء التشفيري)، والتشفير، وفك التشفير لـ LeaseSet2 (LS2) المشفَّر. توفر LeaseSets المشفَّرة نشرًا خاضعًا للتحكم في الوصول لمعلومات الخدمات المخفية في قاعدة بيانات شبكة I2P.

**الميزات الأساسية:** - تدوير يومي للمفاتيح لتحقيق السرية الأمامية - ترخيص العملاء ثنائي المستويات (DH-based القائم على Diffie-Hellman، وPSK-based المعتمد على المفتاح المُشترك مسبقاً) - تشفير ChaCha20 لتحسين الأداء على الأجهزة التي تفتقر إلى عتاد AES - تواقيع Red25519 مع key blinding (إعماء المفتاح) - عضوية عملاء تحافظ على الخصوصية

**الوثائق ذات الصلة:** - [مواصفة الهياكل المشتركة](/docs/specs/common-structures/) - بنية LeaseSet المشفرة - [الاقتراح 123: إدخالات netDB الجديدة](/proposals/123-new-netdb-entries/) - خلفية حول LeaseSets المشفرة - [وثائق قاعدة بيانات الشبكة](/docs/specs/common-structures/) - استخدام NetDB

---

## سجل الإصدارات وحالة التنفيذ

### الجدول الزمني لتطوير البروتوكول

**ملاحظة مهمة حول ترقيم الإصدارات:**   تستخدم I2P مخططين منفصلين لترقيم الإصدارات: - **إصدار API/Router:** سلسلة 0.9.x (يُستخدم في المواصفات التقنية) - **إصدار المنتج:** سلسلة 2.x.x (يُستخدم للإصدارات العامة)

تشير المواصفات التقنية إلى إصدارات واجهة برمجة التطبيقات (API) (مثل 0.9.41)، في حين يرى المستخدمون النهائيون إصدارات المنتج (مثل 2.10.0).

### معالم التنفيذ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill support for standard LS2, offline keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full encrypted LS2 support, Red25519 (sig type&nbsp;11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.40</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Per-client authorization, encrypted LS2 with offline keys, B32 support</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Protocol finalized as stable</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2.10.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest Java implementation (API version 0.9.61)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>i2pd 2.58.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full C++ implementation compatibility</td></tr>
  </tbody>
</table>
### الحالة الحالية

- ✅ **حالة البروتوكول:** مستقر ولم يتغير منذ يونيو 2019
- ✅ **Java I2P:** مُنفّذ بالكامل في الإصدار 0.9.40+
- ✅ **i2pd (C++):** مُنفّذ بالكامل في الإصدار 2.58.0+
- ✅ **التشغيل البيني:** كامل بين التنفيذات
- ✅ **نشر الشبكة:** جاهز للإنتاج مع خبرة تشغيلية تزيد على 6 سنوات

---

## تعريفات التشفير

### الترميز والاصطلاحات

- `||` يدل على الربط
- `mod L` يدل على الاختزال المعياري وفق رتبة Ed25519
- جميع مصفوفات البايت تكون بترتيب بايت الشبكة (big-endian: البايت الأكثر أهمية أولاً) ما لم يُنص على خلاف ذلك
- القيم ذات الترتيب little-endian (البايت الأقل أهمية أولاً) يُشار إليها صراحة

### CSRNG(n) (مولد أعداد عشوائية آمن تشفيرياً)

**مولِّد أرقام عشوائية آمن تشفيرياً**

يُنتج `n` بايتًا من بيانات عشوائية آمنة من الناحية التشفيرية، مناسبة لتوليد مادة المفتاح.

**متطلبات الأمان:** - يجب أن يكون آمناً تشفيرياً (مناسب لتوليد المفاتيح) - يجب أن يكون آمناً عند انكشاف تسلسلات بايت متجاورة على الشبكة - ينبغي لعمليات التنفيذ أن تقوم بتجزئة المخرجات القادمة من مصادر قد لا يُوثَق بها

**المراجع:** - [اعتبارات أمان PRNG](http://projectbullrun.org/dual-ec/ext-rand.html) - [مناقشة مطوري Tor](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)

### H(p, d)

**تجزئة SHA-256 مع التخصيص**

دالة تجزئة مع domain separation (فصل النطاقات) تأخذ: - `p`: سلسلة التخصيص (توفّر فصل النطاقات) - `d`: البيانات المطلوب تجزئتها

**التنفيذ:**

```
H(p, d) := SHA-256(p || d)
```
**الاستخدام:** يوفّر فصلًا تشفيريًا للمجالات لمنع هجمات التصادم بين الاستخدامات البروتوكولية المختلفة لـ SHA-256.

### تدفق: ChaCha20 (خوارزمية تشفير تيارية)

**شفرة تدفقية: ChaCha20 كما هو محدد في RFC 7539 القسم 2.4**

**المعلمات:** - `S_KEY_LEN = 32` (مفتاح بطول 256-بت) - `S_IV_LEN = 12` (nonce (عدد فريد لمرة واحدة) بطول 96-بت) - العداد الابتدائي: `1` (تسمح RFC 7539 بالقيمة 0 أو 1؛ يوصى باستخدام 1 لسياقات AEAD (مصادقة وتشفير البيانات المقترنة))

**ENCRYPT(k, iv, plaintext)**

يشفّر النص الصريح باستخدام: - `k`: مفتاح تشفير بطول 32 بايت - `iv`: nonce (قيمة تُستخدم مرة واحدة) بطول 12 بايت (يجب أن تكون فريدة لكل مفتاح) - يعيد نصاً مُشفّراً بنفس حجم النص الصريح

**خاصية أمنية:** يجب أن يكون كامل النص المشفّر غير قابل للتمييز عن العشوائية إذا كان المفتاح سريًا.

**فك التشفير(k, iv, ciphertext)**

يفك تشفير النص المُشفّر باستخدام: - `k`: مفتاح تشفير بطول 32 بايت - `iv`: عدد يُستخدم مرة واحدة بطول 12 بايت - يُرجع النص الصريح

**مبررات التصميم:** تم اختيار ChaCha20 بدلًا من AES للأسباب التالية:
- أسرع بمقدار 2.5-3x من AES على الأجهزة التي لا يتوفر فيها تسريع عتادي
- يسهل تحقيق تنفيذ بزمن ثابت (constant-time)
- أمان وسرعة قابِلان للمقارنة عند توفر AES-NI

**المراجع:** - [RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539) - ChaCha20 و Poly1305 لبروتوكولات IETF

### التوقيع: Red25519 (خوارزمية توقيع رقمية)

**مخطط التوقيع: Red25519 (SigType 11) مع إعماء المفتاح**

Red25519 مبني على تواقيع Ed25519 على منحنى Ed25519، باستخدام SHA-512 للتجزئة، مع دعم key blinding (إعماء المفتاح) كما هو محدد في ZCash RedDSA.

**الدوال:**

#### DERIVE_PUBLIC(privkey)

يُعيد المفتاح العام المقابل للمفتاح الخاص المُعطى. - يستخدم الضرب العددي القياسي في Ed25519 على النقطة الأساسية

#### SIGN(privkey, m)

يُرجِع توقيعًا باستخدام المفتاح الخاص `privkey` على الرسالة `m`.

**اختلافات توقيع Red25519 عن Ed25519:** 1. **Nonce عشوائي (عدد يُستخدم مرة واحدة):** يستخدم 80 بايتًا من البيانات العشوائية الإضافية

   ```
   T = CSRNG(80)  // 80 random bytes
   r = H*(T || publickey || message)
   ```
هذا يجعل كل توقيع Red25519 (خوارزمية توقيع) فريدًا، حتى مع الرسالة والمفتاح نفسيهما.

2. **توليد المفاتيح الخاصة:** تُولَّد مفاتيح Red25519 الخاصة من أعداد عشوائية وتُختزَل وفق `mod L`، بدلاً من استخدام نهج bit-clamping الخاص بـ Ed25519.

#### تحقق(pubkey, m, sig)

يتحقق من التوقيع `sig` مقابل المفتاح العام `pubkey` والرسالة `m`. - يُرجع `true` إذا كان التوقيع صالحًا، و`false` خلاف ذلك - عملية التحقق مطابقة لـ Ed25519

**عمليات إعماء المفاتيح:**

#### GENERATE_ALPHA(data, secret)

يولّد قيمة ألفا لأجل key blinding (إعماء المفتاح). - `data`: يحتوي عادةً على المفتاح العام للتوقيع وأنواع التوقيع - `secret`: سر إضافي اختياري (بطول صفري إذا لم يُستخدم) - النتيجة موزَّعة بنفس توزيع مفاتيح Ed25519 الخاصة (بعد إجراء اختزال mod L)

#### BLIND_PRIVKEY(privkey, alpha)

يُعمّي مفتاحاً خاصاً باستخدام السر `alpha`. - التنفيذ: `blinded_privkey = (privkey + alpha) mod L` - يستخدم حسابات scalar (عدد قياسي) ضمن الحقل

#### BLIND_PUBKEY(pubkey, alpha)

يُعمّي مفتاحاً عاماً باستخدام السر `alpha`. - التنفيذ: `blinded_pubkey = pubkey + DERIVE_PUBLIC(alpha)` - يستخدم جمع عناصر المجموعة (النقاط) على المنحنى

**خاصية حرجة:**

```
BLIND_PUBKEY(pubkey, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))
```
**اعتبارات أمنية:**

من مواصفة بروتوكول ZCash القسم 5.4.6.1: لأسباب أمنية، يجب أن يكون توزيع alpha مطابقاً لتوزيع unblinded private keys (المفاتيح الخاصة بعد إزالة الإعماء). وهذا يضمن أن "مزيج مفتاح عام أُعيدت عشوائيته والتوقيع أو التوقيعات المُولَّدة باستخدام ذلك المفتاح لا يكشف المفتاح الذي أُعيدت عشوائيته منه".

**أنواع التواقيع المدعومة:** - **النوع 7 (Ed25519):** مدعوم للوجهات الحالية (للتوافق مع الإصدارات الأقدم) - **النوع 11 (Red25519):** موصى به للوجهات الجديدة التي تستخدم التشفير - **Blinded keys (مفاتيح معمية):** استخدم دائمًا النوع 11 (Red25519)

**المراجع:** - [مواصفة بروتوكول ZCash](https://zips.z.cash/protocol/protocol.pdf) - القسم 5.4.6 RedDSA - [مواصفة I2P Red25519](/docs/specs/red25519-signature-scheme/)

### DH (تبادل المفاتيح ديفي-هيلمان): X25519

**ديفي-هيلمان على المنحنيات الإهليلجية: X25519**

نظام اتفاق مفاتيح بالمفتاح العام قائم على Curve25519.

**المعلمات:** - المفاتيح الخاصة: 32 بايت - المفاتيح العامة: 32 بايت - مخرجات السرّ المشترك: 32 بايت

**الدوال:**

#### GENERATE_PRIVATE()

يُولِّد مفتاحاً خاصاً جديداً بطول 32 بايت باستخدام CSRNG (مولّد أرقام عشوائية آمن تشفيرياً).

#### DERIVE_PUBLIC(privkey)

يشتق مفتاحًا عامًا بطول 32 بايت من المفتاح الخاص المُعطى. - يستخدم الضرب العددي على Curve25519 (منحنى بيضوي للتشفير)

#### DH(privkey, pubkey)

ينفّذ اتفاقية تبادل المفاتيح Diffie-Hellman. - `privkey`: مفتاح خاص محلي بطول 32 بايت - `pubkey`: مفتاح عام بعيد بطول 32 بايت - يعيد: سر مشترك بطول 32 بايت

**خصائص الأمان:** - افتراض ديفي-هيلمان الحسابي على Curve25519 - السرية الأمامية عند استخدام المفاتيح المؤقتة - يتطلب تنفيذًا بزمن ثابت لمنع هجمات التوقيت

**المراجع:** - [RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748) - المنحنيات البيضوية للأمن

### HKDF (دالة اشتقاق المفاتيح المستندة إلى HMAC)

**دالة اشتقاق المفاتيح المستندة إلى HMAC**

يستخلص ويُوسِّع المادة المفتاحية من المادة المفتاحية المُدخلة.

**المعلمات:** - `salt`: بحد أقصى 32 بايت (عادةً 32 بايت لـ SHA-256) - `ikm`: مادة مفتاح الإدخال (أي طول، ينبغي أن تتمتع بإنتروبيا جيدة) - `info`: معلومات خاصة بالسياق (فصل المجالات) - `n`: طول المخرجات بالبايت

**التنفيذ:**

يستخدم HKDF (مشتق المفاتيح القائم على HMAC) كما هو محدد في RFC 5869 مع: - **دالة التجزئة:** SHA-256 - **HMAC:** كما هو محدد في RFC 2104 - **طول الملح (Salt):** بحد أقصى 32 بايت (HashLen، أي طول ناتج التجزئة، لـ SHA-256)

**نمط الاستخدام:**

```
keys = HKDF(salt, ikm, info, n)
```
**فصل المجالات:** يوفر معامل `info` فصلًا تشفيريًا للمجالات بين الاستخدامات المختلفة لـ HKDF (دالة اشتقاق المفاتيح المعتمدة على HMAC) في البروتوكول.

**قيم معلومات مُتحقَّق منها:** - `"ELS2_L1K"` - تشفير الطبقة 1 (الخارجية) - `"ELS2_L2K"` - تشفير الطبقة 2 (الداخلية) - `"ELS2_XCA"` - تفويض العميل DH (تبادل المفاتيح ديفي-هيلمان) - `"ELS2PSKA"` - تفويض العميل PSK (مفتاح مُشترك مُسبقًا) - `"i2pblinding1"` - توليد ألفا

**المراجع:** - [RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869) - مواصفة HKDF - [RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104) - مواصفة HMAC

---

## مواصفة التنسيق

يتكوّن LS2 (الإصدار الثاني من leaseSet) المشفّر من ثلاث طبقات متداخلة:

1. **الطبقة 0 (الخارجية):** معلومات نصية صريحة للتخزين والاسترجاع
2. **الطبقة 1 (الوسطى):** بيانات مصادقة العميل (مشفرة)
3. **الطبقة 2 (الداخلية):** بيانات LeaseSet2 الفعلية (مشفرة)

**الهيكل العام:**

```
Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature
```
**مهم:** تستخدم LS2 المُشفَّرة مفاتيح مُعمّاة بالإعماء. Destination (الوجهة) ليست في الترويسة. موقع التخزين في DHT هو `SHA-256(sig type || blinded public key)`، ويُدوَّر يومياً.

### الطبقة 0 (الخارجية) - نص صريح

لا تستخدم الطبقة 0 ترويسة LS2 القياسية. لديها تنسيق مخصص محسّن لـ blinded keys (مفاتيح مُعمّاة بطريقة التعمية العمياء).

**البنية:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Not in header, from DatabaseStore message field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, always <code>0x000b</code> (Red25519 type 11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 blinded public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch (rolls over in 2106)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, offset from published in seconds (max 65,535 &asymp; 18.2 hours)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Bit flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Transient Key Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present if flag bit&nbsp;0 is set</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, length of outer ciphertext</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">outerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;1 data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 signature over all preceding data</td></tr>
  </tbody>
</table>
**حقل الأعلام (2 بايت، البتات 15-0):** - **البت 0:** مؤشر المفاتيح غير المتصلة   - `0` = لا توجد مفاتيح غير متصلة   - `1` = توجد مفاتيح غير متصلة (تليها بيانات مفاتيح مؤقتة) - **البتات 1-15:** محجوزة، يجب أن تكون 0 لضمان التوافق المستقبلي

**بيانات مفتاح مؤقتة (موجودة إذا كان البت 0 في العلم يساوي 1):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Signing Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length implied by signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signed by blinded public key; covers expires timestamp, transient sig type, and transient public key</td></tr>
  </tbody>
</table>
**التحقق من التوقيع:** - **من دون مفاتيح غير متصلة:** تحقق باستخدام blinded public key (مفتاح عام أعمى) - **مع مفاتيح غير متصلة:** تحقق باستخدام مفتاح عام مؤقت

يغطي التوقيع جميع البيانات من Type وحتى outerCiphertext (شاملًا الطرفين).

### الطبقة 1 (الوسطى) - تخويل العميل

**فك التشفير:** انظر قسم [تشفير الطبقة 1](#layer-1-encryption).

**البنية:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Authorization flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Auth Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present based on flags</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">innerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;2 data (remainder)</td></tr>
  </tbody>
</table>
**حقل الأعلام (1 بايت، البتات 7-0):** - **البت 0:** وضع التخويل   - `0` = بدون تخويل لكل عميل (الجميع)   - `1` = تخويل لكل عميل (يتبع قسم التخويل) - **البتات 3-1:** مخطط المصادقة (فقط إذا كان البت 0 = 1)   - `000` = مصادقة عميل DH (Diffie-Hellman)   - `001` = مصادقة عميل PSK (مفتاح مُشترك مسبقًا)   - البقية محجوزة - **البتات 7-4:** غير مستخدمة، يجب أن تكون 0

**بيانات تفويض العميل DH (الأعلام = 0x01, البتات 3-1 = 000):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ephemeralPublicKey</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Server's ephemeral X25519 public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**مدخلة authClient (40 بايت):** - `clientID_i`: 8 بايت - `clientCookie_i`: 32 بايت (authCookie مشفّر)

**بيانات تفويض عميل PSK (مفتاح مُشترك مُسبقاً) (الأعلام = 0x03، البتات 3-1 = 001):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authSalt</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Salt for PSK key derivation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**مدخلة authClient (40 بايت):** - `clientID_i`: 8 بايت - `clientCookie_i`: 32 بايت (authCookie مشفّر)

### الطبقة 2 (الداخلية) - بيانات LeaseSet

**فك التشفير:** راجع قسم [Layer 2 Encryption](#layer-2-encryption).

**البنية:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>3</code> (LS2) or <code>7</code> (Meta LS2)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Complete LeaseSet2 or MetaLeaseSet2</td></tr>
  </tbody>
</table>
تحتوي الطبقة الداخلية على البنية الكاملة لـ LeaseSet2 بما في ذلك: - ترويسة LS2 - معلومات الـ Lease (سجل اتصال مؤقت في I2P) - توقيع LS2

**متطلبات التحقق:** بعد فك التشفير، يجب على التنفيذات التحقق مما يلي: 1. أن الطابع الزمني الداخلي يطابق الطابع الزمني الخارجي المنشور 2. أن وقت الانتهاء الداخلي يطابق وقت الانتهاء الخارجي 3. أن يكون توقيع LS2 صالحًا (الإصدار الثاني من LeaseSet) 4. أن تكون بيانات الـ Lease مكوّنة بشكل سليم

**المراجع:** - [مواصفات الهياكل المشتركة](/docs/specs/common-structures/) - تفاصيل تنسيق LeaseSet2

---

## اشتقاق مفتاح الإعماء

### نظرة عامة

يستخدم I2P مخططاً جمعياً لإعماء المفاتيح مبنياً على Ed25519 (خوارزمية توقيع بيضوية Ed25519) وZCash RedDSA (متغير EdDSA المستخدم في ZCash). تُدوَّر المفاتيح المُعمّاة يومياً (منتصف الليل بتوقيت UTC) لتحقيق السرية الأمامية.

**الأساس المنطقي للتصميم:**

اختارت I2P صراحةً عدم استخدام نهج الملحق A.2 في ملف rend-spec-v3.txt الخاص بـ Tor. وفقًا للمواصفة:

> "نحن لا نستخدم الملحق A.2 من ملف المواصفات rend-spec-v3.txt الخاص بـ Tor، الذي له أهداف تصميم مشابهة، لأن مفاتيحه العامة المُعمّاة (blinded) قد تكون خارج المجموعة الفرعية ذات الرتبة الأولية، مع تبعات أمنية غير معروفة."

الإعماء الجمعي في I2P يضمن بقاء المفاتيح المُعمّاة بأسلوب الإعماء ضمن المجموعة الفرعية ذات الرتبة الأولية لمنحنى Ed25519.

### التعريفات الرياضية

**معاملات Ed25519:** - `B`: نقطة الأساس في Ed25519 (المولِّد) = `2^255 - 19` - `L`: رتبة Ed25519 = `2^252 + 27742317777372353535851937790883648493`

**المتغيرات الأساسية:** - `A`: مفتاح توقيع عام بطول 32 بايت غير أعمى (داخل Destination، أي الوجهة في I2P) - `a`: مفتاح توقيع خاص بطول 32 بايت غير أعمى - `A'`: مفتاح توقيع عام بطول 32 بايت أعمى (يُستخدم في LeaseSet مُشفّر) - `a'`: مفتاح توقيع خاص بطول 32 بايت أعمى - `alpha`: عامل العمى بطول 32 بايت (سري)

**الدوال المساعدة:**

#### LEOS2IP(x)

"من سلسلة بايتات بتنسيق Little-Endian (النهاية الصغرى) إلى عدد صحيح"

يحوّل مصفوفة بايت مُرتّبة وفق little-endian إلى تمثيل عدد صحيح.

#### H*(x)

"التجزئة والاختزال"

```
H*(x) = (LEOS2IP(SHA512(x))) mod L
```
نفس العملية كما في توليد مفاتيح Ed25519 (خوارزمية توقيع رقمية على منحنى بيضوي).

### جيل ألفا

**التدوير اليومي:** يجب توليد alpha جديدة و blinded keys (مفاتيح مُعمّاة بتقنية الإعماء) كل يوم عند منتصف الليل حسب UTC (00:00:00 UTC).

**خوارزمية GENERATE_ALPHA(destination, date, secret):**

```python
# Input parameters
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes, big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes, big endian) 
     # Always 0x000b (Red25519)
datestring = "YYYYMMDD" (8 bytes ASCII from current UTC date)
secret = optional UTF-8 encoded string (zero-length if not used)

# Computation
keydata = A || stA || stA'  # 36 bytes total
seed = HKDF(
    salt=H("I2PGenerateAlpha", keydata),
    ikm=datestring || secret,
    info="i2pblinding1",
    n=64
)

# Treat seed as 64-byte little-endian integer and reduce
alpha = seed mod L
```
**تم التحقق من البارامترات:** - تخصيص الملح: "I2PGenerateAlpha" - قيمة info في HKDF: "i2pblinding1" - المخرجات: 64 بايت قبل الاختزال - توزيع Alpha: بنفس توزيع مفاتيح Ed25519 الخاصة بعد `mod L`

### إعماء المفتاح الخاص

**خوارزمية BLIND_PRIVKEY(a, alpha):**

بالنسبة لمالك الوجهة الذي ينشر LeaseSet المُشفَّرة:

```python
# For Ed25519 private key (type 7)
if sigtype == 7:
    seed = destination's signing private key (32 bytes)
    a = left_half(SHA512(seed))  # 32 bytes
    a = clamp(a)  # Ed25519 clamping
    
# For Red25519 private key (type 11)
elif sigtype == 11:
    a = destination's signing private key (32 bytes)
    # No clamping for Red25519

# Additive blinding using scalar arithmetic
blinded_privkey = a' = (a + alpha) mod L

# Derive blinded public key
blinded_pubkey = A' = DERIVE_PUBLIC(a')
```
**حاسم:** إن اختزال `mod L` ضروري للحفاظ على العلاقة الجبرية الصحيحة بين المفتاحين الخاص والعام.

### إعماء المفتاح العام

**خوارزمية BLIND_PUBKEY(A, alpha):**

بالنسبة للعملاء الذين يسترجعون ويتحققون من LeaseSet المشفَّر:

```python
alpha = GENERATE_ALPHA(destination, date, secret)
A = destination's signing public key (32 bytes)

# Additive blinding using group elements (curve points)
blinded_pubkey = A' = A + DERIVE_PUBLIC(alpha)
```
**التكافؤ الرياضي:**

كلتا الطريقتين تعطيان النتيجة نفسها:

```
BLIND_PUBKEY(A, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(a, alpha))
```
وذلك لأن:

```
A' = A + [alpha]B
   = [a]B + [alpha]B
   = [a + alpha]B  (group operation)
   = DERIVE_PUBLIC(a + alpha mod L)
```
### التوقيع باستخدام Blinded Keys (مفاتيح مُطبَّق عليها الإعماء)

**توقيع LeaseSet غير أعمى:**

يتم توقيع الـ unblinded (غير مُعمّى) LeaseSet (المُرسَل مباشرةً إلى العملاء الموثَّقين) باستخدام: - توقيع Standard Ed25519 (النوع 7) أو Red25519 (النوع 11) - مفتاح توقيع خاص unblinded - يتم التحقق باستخدام مفتاح عام unblinded

**باستخدام المفاتيح غير المتصلة:** - موقّع بواسطة مفتاح خاص مؤقت unblinded (مزال العمى في سياق التوقيعات العمياء) - يُتحقَّق منه باستخدام مفتاح عام مؤقت unblinded - يجب أن يكون كلاهما من النوع 7 أو 11

**توقيع LeaseSet المشفرة:**

الجزء الخارجي من LeaseSet المشفَّر يستخدم تواقيع Red25519 مع blinded keys (مفاتيح مُعمّاة بالإعماء).

**خوارزمية التوقيع Red25519:**

```python
# Generate per-signature random nonce
T = CSRNG(80)  # 80 random bytes

# Calculate r (differs from Ed25519)
r = H*(T || blinded_pubkey || message)

# Rest is same as Ed25519
R = [r]B
S = (r + H(R || A' || message) * a') mod L
signature = R || S  # 64 bytes total
```
**الاختلافات الأساسية عن Ed25519:** 1. يستخدم 80 بايت من البيانات العشوائية `T` (وليس تجزئة المفتاح الخاص) 2. يستخدم قيمة المفتاح العام مباشرةً (وليس تجزئة المفتاح الخاص) 3. كل توقيع فريد حتى مع نفس الرسالة والمفتاح

**التحقق:**

مماثل لـ Ed25519:

```python
# Parse signature
R = signature[0:32]
S = signature[32:64]

# Verify equation: [S]B = R + [H(R || A' || message)]A'
return [S]B == R + [H(R || A' || message)]A'
```
### اعتبارات أمنية

**توزيع ألفا:**

من أجل الأمان، يجب أن يكون توزيع alpha مطابقاً لتوزيع المفاتيح الخاصة غير المعمية. عند إجراء blinding (تقنية الإعماء في التشفير) من Ed25519 (type 7) إلى Red25519 (type 11)، تختلف التوزيعات قليلاً.

**توصية:** استخدم Red25519 (type 11) لكلٍ من المفاتيح غير المُعمّاة (بالإعماء) والمفاتيح المُعمّاة (بالإعماء) لتلبية متطلبات ZCash: "إن اقتران مفتاح عام أُعيدت عشوائيته والتوقيع(ات) باستخدام ذلك المفتاح لا يكشف المفتاح الذي أُعيدت منه عشوائيته."

**دعم النوع 7:** Ed25519 (خوارزمية توقيع رقمية بيضوية) مدعوم للتوافق مع الإصدارات السابقة للوجهات القائمة، لكن يُوصى باستخدام النوع 11 للوجهات المشفّرة الجديدة.

**فوائد التدوير اليومي:** - السرية المستقبلية: اختراق blinded key (المفتاح المُعمّى) اليوم لا يكشف مفتاح الأمس - عدم قابلية الربط: التدوير اليومي يمنع التتبع طويل الأمد عبر DHT - فصل المفاتيح: مفاتيح مختلفة لفترات زمنية مختلفة

**المراجع:** - [ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf) - القسم 5.4.6.1 - [Tor Key Blinding Discussion](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html) - [Tor Ticket #8106](https://trac.torproject.org/projects/tor/ticket/8106)

---

## التشفير والمعالجة

### اشتقاق بيانات الاعتماد الفرعية

قبل التشفير، نشتق credential (بيانات اعتماد) وsubcredential (بيانات اعتماد فرعية) لربط الطبقات المشفرة بشرط معرفة المفتاح العام للتوقيع الخاص بالوجهة.

**الهدف:** ضمان أن فك تشفير LeaseSet المُشفَّر لا يمكن إلا لمن يعرفون المفتاح العام للتوقيع الخاص بالوجهة. لا حاجة إلى الوجهة الكاملة.

#### حساب بيانات الاعتماد

```python
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes big endian)
     # Always 0x000b (Red25519)

keydata = A || stA || stA'  # 36 bytes

credential = H("credential", keydata)  # 32 bytes
```
**فصل المجالات:** تضمن سلسلة التخصيص `"credential"` ألا تتصادم قيمة التجزئة هذه مع أي مفاتيح استعلام في DHT (جدول تجزئة موزع) أو مع استخدامات أخرى للبروتوكول.

#### حساب بيانات الاعتماد الفرعية

```python
blindedPublicKey = A' (32 bytes, from blinding process)

subcredential = H("subcredential", credential || blindedPublicKey)  # 32 bytes
```
**الغرض:** يقوم subcredential (اعتماد فرعي) بربط الـ LeaseSet المشفّر بـ: 1. Destination (الوجهة) المحددة (عبر credential) 2. blinded key (مفتاح مُعمّى بالإعماء) المحدد (عبر blindedPublicKey) 3. اليوم المحدد (عبر التدوير اليومي لـ blindedPublicKey)

هذا يمنع هجمات إعادة الإرسال والربط عبر أيام مختلفة.

### تشفير الطبقة الأولى

**السياق:** تحتوي الطبقة 1 على بيانات تفويض العميل ويتم تشفيرها باستخدام مفتاح مشتق من subcredential (بيانات اعتماد فرعية).

#### خوارزمية التشفير

```python
# Prepare input
outerInput = subcredential || publishedTimestamp
# publishedTimestamp: 4 bytes from Layer 0

# Generate random salt
outerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

outerKey = keys[0:31]    # 32 bytes (indices 0-31 inclusive)
outerIV = keys[32:43]    # 12 bytes (indices 32-43 inclusive)

# Encrypt and prepend salt
outerPlaintext = [Layer 1 data]
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
**الناتج:** `outerCiphertext` هو `32 + len(outerPlaintext)` بايت.

**خصائص الأمان:** - الملح يضمن أزواج مفتاح/متجه تهيئة (IV) فريدة حتى مع نفس بيانات الاعتماد الفرعية - سلسلة السياق `"ELS2_L1K"` توفّر فصل المجالات - ChaCha20 يوفّر أمانًا دلاليًا (نصًا مشفّرًا غير قابل للتمييز عن العشوائي)

#### خوارزمية فك التشفير

```python
# Parse salt from ciphertext
outerSalt = outerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV (same process as encryption)
outerInput = subcredential || publishedTimestamp
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",
    n=44
)

outerKey = keys[0:31]    # 32 bytes
outerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
**التحقق:** بعد فك التشفير، تحقّق من أن بنية الطبقة 1 مُشكّلة بشكل صحيح قبل المتابعة إلى الطبقة 2.

### تشفير الطبقة الثانية

**السياق:** تحتوي الطبقة 2 على بيانات LeaseSet2 الفعلية وتكون مشفّرة بمفتاح مشتق من authCookie (إذا كانت المصادقة لكل عميل مفعّلة) أو سلسلة فارغة (إذا لم تكن كذلك).

#### خوارزمية التشفير

```python
# Determine authCookie based on authorization mode
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Prepare input
innerInput = authCookie || subcredential || publishedTimestamp

# Generate random salt
innerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Encrypt and prepend salt
innerPlaintext = [Layer 2 data: LS2 type byte + LeaseSet2 data]
innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
**المخرجات:** `innerCiphertext` طوله `32 + len(innerPlaintext)` بايتًا.

**ربط المفتاح:** - إذا لم تكن هناك مصادقة للعميل: يكون الارتباط فقط بـ subcredential و timestamp - إذا كانت مصادقة العميل مفعّلة: يكون الارتباط أيضاً بـ authCookie (مختلف لكل عميل مخوّل)

#### خوارزمية فك التشفير

```python
# Determine authCookie (same as encryption)
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Parse salt from ciphertext
innerSalt = innerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV
innerInput = authCookie || subcredential || publishedTimestamp
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",
    n=44
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
**التحقق:** بعد فك التشفير: 1. التحقق من أن بايت نوع LS2 صالح (3 أو 7) 2. تحليل بنية LeaseSet2 3. التحقق من أن الطابع الزمني الداخلي يطابق الطابع الزمني المنشور الخارجي 4. التحقق من أن تاريخ الانقضاء الداخلي يطابق تاريخ الانقضاء الخارجي 5. التحقق من توقيع LeaseSet2

### ملخص طبقة التشفير

```
┌─────────────────────────────────────────────────┐
│ Layer 0 (Plaintext)                             │
│ - Blinded public key                            │
│ - Timestamps                                    │
│ - Signature                                     │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Layer 1 (Encrypted with subcredential)  │   │
│  │ - Authorization flags                   │   │
│  │ - Client auth data (if enabled)         │   │
│  │                                          │   │
│  │  ┌────────────────────────────────┐     │   │
│  │  │ Layer 2 (Encrypted with        │     │   │
│  │  │          authCookie + subcred) │     │   │
│  │  │ - LeaseSet2 type               │     │   │
│  │  │ - LeaseSet2 data               │     │   │
│  │  │ - Leases                       │     │   │
│  │  │ - LS2 signature                │     │   │
│  │  └────────────────────────────────┘     │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```
**تدفق فك التشفير:** 1. تحقّق من توقيع الطبقة 0 باستخدام blinded public key (مفتاح عام بتعمية عمياء) 2. فك تشفير الطبقة 1 باستخدام subcredential (اعتماد فرعي) 3. قم بمعالجة بيانات التفويض (إن وُجدت) للحصول على authCookie (ملف تعريف ارتباط المصادقة) 4. فك تشفير الطبقة 2 باستخدام authCookie وsubcredential 5. تحقّق وحلّل LeaseSet2

---

## تفويض لكل عميل

### نظرة عامة

عند تمكين التفويض على مستوى العميل، يحتفظ الخادم بقائمة بالعملاء المخوَّلين. يمتلك كل عميل بيانات مفاتيح يجب نقلها بأمان عبر out-of-band (خارج القناة الاعتيادية).

**آليتان للتخويل:** 1. **تخويل العميل بطريقة DH (Diffie-Hellman):** أكثر أمانًا، يستخدم اتفاقية تبادل المفاتيح X25519 2. **تخويل باستخدام PSK (Pre-Shared Key):** أبسط، يستخدم مفاتيح متناظرة

**خصائص الأمان الشائعة:** - خصوصية عضوية العملاء: يمكن للمراقبين رؤية عدد العملاء لكن لا يمكنهم تحديد عملاء بعينهم - إضافة/سحب العملاء بشكل مجهول: لا يمكن تتبّع وقت إضافة عملاء محدّدين أو إزالتهم - احتمال تصادم معرّف العميل المكوّن من 8 بايت: ~1 من كل 18 كوينتيليون (مهمل)

### تفويض عميل DH (Diffie-Hellman - تبادل المفاتيح ديفي-هيلمان)

**نظرة عامة:** يولّد كل عميل زوج مفاتيح X25519 ويرسل مفتاحه العام إلى الخادم عبر قناة آمنة خارج النطاق. يستخدم الخادم تبادل مفاتيح ديفي-هيلمان المؤقت لتشفير قيمة authCookie فريدة لكل عميل.

#### توليد مفاتيح العميل

```python
# Client generates keypair
csk_i = GENERATE_PRIVATE()  # 32-byte X25519 private key
cpk_i = DERIVE_PUBLIC(csk_i)  # 32-byte X25519 public key

# Client sends cpk_i to server via secure out-of-band channel
# Client KEEPS csk_i secret (never transmitted)
```
**ميزة أمنية:** لا يغادر المفتاح الخاص للعميل جهازه مطلقًا. لا يستطيع خصمٌ يعترض الإرسال خارج القناة فك تشفير LeaseSets المُشفَّرة المستقبلية من دون كسر X25519 DH (خوارزمية تبادل المفاتيح ديفي-هيلمان X25519).

#### المعالجة على الخادم

```python
# Server generates new auth cookie and ephemeral keypair
authCookie = CSRNG(32)  # 32-byte cookie

esk = GENERATE_PRIVATE()  # 32-byte ephemeral private key
epk = DERIVE_PUBLIC(esk)  # 32-byte ephemeral public key

# For each authorized client i
for cpk_i in authorized_clients:
    # Perform DH key agreement
    sharedSecret = DH(esk, cpk_i)  # 32 bytes
    
    # Derive client-specific encryption key
    authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
    okm = HKDF(
        salt=epk,  # Ephemeral public key as salt
        ikm=authInput,
        info="ELS2_XCA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**بنية بيانات الطبقة 1:**

```
ephemeralPublicKey (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
**توصيات الخادم:** - أنشئ زوج مفاتيح مؤقت جديد لكل LeaseSet مشفّر منشور - اجعل ترتيب العملاء عشوائياً لمنع التتبع القائم على الموضع - فكّر في إضافة إدخالات وهمية لإخفاء العدد الحقيقي للعملاء

#### معالجة العميل

```python
# Client has: csk_i (their private key), destination, date, secret
# Client receives: encrypted LeaseSet with epk in Layer 1

# Perform DH key agreement with server's ephemeral public key
sharedSecret = DH(csk_i, epk)  # 32 bytes

# Derive expected client identifier and decryption key
cpk_i = DERIVE_PUBLIC(csk_i)  # Client's own public key
authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=epk,
    ikm=authInput,
    info="ELS2_XCA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
**التعامل مع أخطاء العميل:** - إذا لم يتم العثور على `clientID_i`: تم سحب تفويض العميل أو لم يُخوَّل قط - إذا فشل فك التشفير: بيانات تالفة أو مفاتيح غير صحيحة (نادر جدًا) - ينبغي للعملاء إعادة الجلب دوريًا لاكتشاف سحب التفويض

### تفويض العميل عبر PSK (مفتاح مُسبق المشاركة)

**نظرة عامة:** يمتلك كل عميل مفتاحاً متناظراً مشتركاً مسبقاً بطول 32 بايت. يقوم الخادم بتشفير نفس authCookie باستخدام PSK (مفتاح مشترك مسبقاً) الخاص بكل عميل.

#### توليد المفاتيح

```python
# Option 1: Client generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Client sends psk_i to server via secure out-of-band channel

# Option 2: Server generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Server sends psk_i to one or more clients via secure out-of-band channel
```
**ملاحظة أمنية:** يمكن مشاركة PSK (مفتاح مشترك مُسبقًا) نفسه بين عدة عملاء عند الرغبة (مما يُنشئ تفويضًا من نوع "مجموعة").

#### معالجة الخادم

```python
# Server generates new auth cookie and salt
authCookie = CSRNG(32)  # 32-byte cookie
authSalt = CSRNG(32)     # 32-byte salt

# For each authorized client i
for psk_i in authorized_clients:
    # Derive client-specific encryption key
    authInput = psk_i || subcredential || publishedTimestamp
    
    okm = HKDF(
        salt=authSalt,
        ikm=authInput,
        info="ELS2PSKA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**بنية بيانات الطبقة 1:**

```
authSalt (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
#### معالجة العميل

```python
# Client has: psk_i (their pre-shared key), destination, date, secret
# Client receives: encrypted LeaseSet with authSalt in Layer 1

# Derive expected client identifier and decryption key
authInput = psk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=authSalt,
    ikm=authInput,
    info="ELS2PSKA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
### المقارنة والتوصيات

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">DH Authorization</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">PSK Authorization</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Exchange</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Asymmetric (X25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric (shared secret)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Security</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Higher (forward secrecy)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Lower (depends on PSK secrecy)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Client Privacy</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Private key never transmitted</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK must be transmitted securely</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Performance</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 DH operations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">No DH operations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Sharing</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">One key per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Can share key among multiple clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Revocation Detection</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary cannot tell when revoked</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary can track revocation if PSK intercepted</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">High security requirements</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Performance-critical or group access</td></tr>
  </tbody>
</table>
**التوصية:** - **Use DH authorization** (تفويض باستخدام Diffie-Hellman) للتطبيقات عالية الأمان حيث تكون السرية الأمامية مهمة - **Use PSK authorization** (تفويض بالمفتاح المشترك مسبقاً) عندما يكون الأداء بالغ الأهمية أو عند إدارة مجموعات العملاء - **لا تُعِد استخدام PSKs** عبر خدمات مختلفة أو فترات زمنية مختلفة - **استخدم دائمًا قنوات آمنة** لتوزيع المفاتيح (مثل Signal, OTR, PGP)

### الاعتبارات الأمنية

**خصوصية عضوية العميل:**

كلتا الآليتين توفّران الخصوصية لعضوية العميل من خلال: 1. **معرّفات العميل المشفّرة:** clientID بطول 8 بايت مُشتق من ناتج HKDF (دالة اشتقاق مفاتيح مستندة إلى HMAC) 2. **ملفات تعريف الارتباط غير القابلة للتمييز:** تبدو جميع قيم clientCookie بطول 32 بايت عشوائية 3. **لا توجد بيانات وصفية خاصة بعميل معيّن:** لا توجد طريقة لتحديد أي إدخال يعود إلى أي عميل

يمكن للمراقب أن يرى:
- عدد العملاء المصرّح لهم (من الحقل `clients`)
- التغيرات في عدد العملاء مع مرور الوقت

لا يمكن للمراقب رؤية: - أي العملاء المحددين مخولون - متى تتم إضافة عملاء محددين أو حذفهم (إذا بقي العدد كما هو) - أي معلومات تحدد هوية العميل

**توصيات بشأن العشوائية:**

يُستحسن أن تُعيد الخوادم ترتيب العملاء بصورة عشوائية في كل مرة تُولِّد فيها LeaseSet مُشفّراً:

```python
import random

# Before serializing
auth_entries = [(clientID_i, clientCookie_i) for each client]
random.shuffle(auth_entries)
# Now serialize in randomized order
```
**الفوائد:** - يمنع العملاء من معرفة موقعهم في القائمة - يمنع هجمات الاستدلال القائمة على التغيرات في الموضع - يجعل إضافة/إبطال العملاء غير قابلة للتمييز

**إخفاء عدد العملاء:**

يجوز أن تقوم الخوادم بإدراج إدخالات وهمية عشوائية:

```python
# Add dummy entries
num_dummies = random.randint(0, max_dummies)
for _ in range(num_dummies):
    dummy_id = CSRNG(8)
    dummy_cookie = CSRNG(32)
    auth_entries.append((dummy_id, dummy_cookie))

# Randomize all entries (real + dummy)
random.shuffle(auth_entries)
```
**التكلفة:** تزيد المدخلات الوهمية حجم LeaseSet المشفّر (40 بايت لكلٍّ منها).

**تدوير AuthCookie (ملف تعريف الارتباط الخاص بالمصادقة):**

ينبغي أن تقوم الخوادم بإنشاء authCookie جديد: - في كل مرة يتم فيها نشر LeaseSet مشفر (كل بضع ساعات عادة) - مباشرة بعد إلغاء تفويض عميل - وفق جدول منتظم (مثلاً يومياً) حتى إن لم تطرأ أي تغييرات على العملاء

**الفوائد:** - يحد من التعرض إذا تم اختراق authCookie - يضمن أن العملاء الذين أُلغيت صلاحياتهم يفقدون الوصول بسرعة - يوفر سرية أمامية للطبقة الثانية

---

## العنونة بـ Base32 لـ LeaseSets المشفرة

### نظرة عامة

عناوين I2P التقليدية بصيغة base32 تحتوي فقط على تجزئة Destination (الوجهة) (32 بايت → 52 حرفًا). وهذا غير كافٍ بالنسبة إلى LeaseSets المشفّرة للأسباب التالية:

1. يحتاج العملاء إلى **المفتاح العام غير المُعمّى (non-blinded public key)** لاشتقاق المفتاح العام المُعمّى (blinded public key)
2. يحتاج العملاء إلى **أنواع التوقيع (signature types)** (غير مُعمّى ومُعمّى) للاشتقاق الصحيح للمفاتيح
3. لا توفّر التجزئة وحدها هذه المعلومات

**الحل:** صيغة base32 (ترميز بقاعدة 32) جديدة تتضمن المفتاح العام وأنواع التوقيع.

### مواصفة صيغة العنوان

**البنية بعد فك الترميز (35 بايت):**

```
┌─────────────────────────────────────────────────────┐
│ Byte 0   │ Byte 1  │ Byte 2  │ Bytes 3-34          │
│ Flags    │ Unblind │ Blinded │ Public Key          │
│ (XOR)    │ SigType │ SigType │ (32 bytes)          │
│          │ (XOR)   │ (XOR)   │                     │
└─────────────────────────────────────────────────────┘
```
**أول 3 بايتات (XOR (أو الحصري) مع المجموع الاختباري):**

تحتوي أول 3 بايتات على بيانات وصفية طُبِّق عليها XOR (أو الحصري) مع أجزاء من قيمة فحص CRC-32:

```python
# Data structure before XOR
flags = 0x00           # 1 byte (reserved for future use)
unblinded_sigtype = 0x07 or 0x0b  # 1 byte (7 or 11)
blinded_sigtype = 0x0b  # 1 byte (always 11)

# Compute CRC-32 checksum of public key
checksum = crc32(pubkey)  # 4-byte CRC-32 of bytes 3-34

# XOR first 3 bytes with parts of checksum
data[0] = flags XOR (checksum >> 24) & 0xFF
data[1] = unblinded_sigtype XOR (checksum >> 16) & 0xFF  
data[2] = blinded_sigtype XOR (checksum >> 8) & 0xFF

# Bytes 3-34 contain the unmodified 32-byte public key
data[3:34] = pubkey
```
**خصائص المجموع الاختباري:** - يستخدم متعدد الحدود القياسي CRC-32 - معدل السلبية الكاذبة: ~1 من كل 16 مليون - يكتشف أخطاء الكتابة في العناوين - لا يمكن استخدامه للمصادقة (غير آمن تشفيرياً)

**التنسيق المُرمَّز:**

```
Base32Encode(35 bytes) || ".b32.i2p"
```
**الخصائص:** - إجمالي عدد الأحرف: 56 (35 بايت × 8 بت ÷ 5 بت لكل حرف) - اللاحقة: ".b32.i2p" (مطابقة لـ base32 التقليدية) - الطول الإجمالي: 56 + 8 = 64 حرفًا (باستثناء null terminator (محرف الإنهاء الفارغ))

**ترميز Base32:** - الأبجدية: `abcdefghijklmnopqrstuvwxyz234567` (المعيار RFC 4648) - يجب أن تكون 5 بتات غير مستخدمة في النهاية تساوي 0 - غير حساس لحالة الأحرف (تقليدياً بالأحرف الصغيرة)

### توليد العناوين

```python
import struct
from zlib import crc32
import base64

def generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype):
    """
    Generate base32 address for encrypted LeaseSet.
    
    Args:
        pubkey: 32-byte public key (bytes)
        unblinded_sigtype: Unblinded signature type (7 or 11)
        blinded_sigtype: Blinded signature type (always 11)
    
    Returns:
        String address ending in .b32.i2p
    """
    # Verify inputs
    assert len(pubkey) == 32, "Public key must be 32 bytes"
    assert unblinded_sigtype in [7, 11], "Unblinded sigtype must be 7 or 11"
    assert blinded_sigtype == 11, "Blinded sigtype must be 11"
    
    # Compute CRC-32 of public key
    checksum = crc32(pubkey) & 0xFFFFFFFF  # Ensure 32-bit unsigned
    
    # Prepare metadata bytes
    flags = 0x00
    
    # XOR metadata with checksum parts
    byte0 = flags ^ ((checksum >> 24) & 0xFF)
    byte1 = unblinded_sigtype ^ ((checksum >> 16) & 0xFF)
    byte2 = blinded_sigtype ^ ((checksum >> 8) & 0xFF)
    
    # Construct 35-byte data
    data = bytes([byte0, byte1, byte2]) + pubkey
    
    # Base32 encode (standard alphabet)
    # Python's base64 module uses uppercase by default
    b32 = base64.b32encode(data).decode('ascii').lower().rstrip('=')
    
    # Construct full address
    address = b32 + ".b32.i2p"
    
    return address
```
### تحليل العناوين

```python
import struct
from zlib import crc32
import base64

def parse_encrypted_b32_address(address):
    """
    Parse base32 address for encrypted LeaseSet.
    
    Args:
        address: String address ending in .b32.i2p
    
    Returns:
        Tuple of (pubkey, unblinded_sigtype, blinded_sigtype)
    
    Raises:
        ValueError: If address is invalid or checksum fails
    """
    # Remove suffix
    if not address.endswith('.b32.i2p'):
        raise ValueError("Invalid address suffix")
    
    b32 = address[:-8]  # Remove ".b32.i2p"
    
    # Verify length (56 characters for 35 bytes)
    if len(b32) != 56:
        raise ValueError(f"Invalid length: {len(b32)} (expected 56)")
    
    # Base32 decode
    # Add padding if needed
    padding_needed = (8 - (len(b32) % 8)) % 8
    b32_padded = b32.upper() + '=' * padding_needed
    
    try:
        data = base64.b32decode(b32_padded)
    except Exception as e:
        raise ValueError(f"Invalid base32 encoding: {e}")
    
    # Verify decoded length
    if len(data) != 35:
        raise ValueError(f"Invalid decoded length: {len(data)} (expected 35)")
    
    # Extract public key
    pubkey = data[3:35]
    
    # Compute CRC-32 for verification
    checksum = crc32(pubkey) & 0xFFFFFFFF
    
    # Un-XOR metadata bytes
    flags = data[0] ^ ((checksum >> 24) & 0xFF)
    unblinded_sigtype = data[1] ^ ((checksum >> 16) & 0xFF)
    blinded_sigtype = data[2] ^ ((checksum >> 8) & 0xFF)
    
    # Verify expected values
    if flags != 0x00:
        raise ValueError(f"Invalid flags: {flags:#x} (expected 0x00)")
    
    if unblinded_sigtype not in [7, 11]:
        raise ValueError(f"Invalid unblinded sigtype: {unblinded_sigtype} (expected 7 or 11)")
    
    if blinded_sigtype != 11:
        raise ValueError(f"Invalid blinded sigtype: {blinded_sigtype} (expected 11)")
    
    return pubkey, unblinded_sigtype, blinded_sigtype
```
### مقارنة مع Base32 التقليدي

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Traditional B32</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Encrypted LS2 B32</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Content</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256 hash of Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Public key + signature types</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Decoded Size</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">35 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Encoded Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">52 characters</td><td style="border:1px solid var(--color-border); padding:0.5rem;">56 characters</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Suffix</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Total Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">60 chars</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 chars</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">None</td><td style="border:1px solid var(--color-border); padding:0.5rem;">CRC-32 (XOR'd into first 3 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Regular destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted LeaseSet destinations</td></tr>
  </tbody>
</table>
### قيود الاستخدام

**عدم التوافق مع BitTorrent:**

لا يمكن استخدام عناوين LS2 المشفّرة مع ردود الإعلان المدمجة الخاصة بـ BitTorrent:

```
Compact announce reply format:
┌────────────────────────────┐
│ 32-byte destination hash   │  ← Only hash, no signature types
│ 2-byte port                │
└────────────────────────────┘
```
**المشكلة:** التنسيق الموجز يحتوي فقط على التجزئة (32 بايت)، ولا يوفّر مساحة لأنواع التوقيع أو معلومات المفتاح العام.

**الحل:** استخدم ردود announce (رسالة الإعلان في متتبّع BitTorrent) الكاملة أو متتبّعات قائمة على HTTP تدعم العناوين الكاملة.

### تكامل دفتر العناوين

إذا كان لدى عميل Destination الكامل (معرّف الوجهة في I2P) في دفتر عناوين:

1. خزّن Destination (الوجهة) الكامل (يتضمن المفتاح العام)
2. ادعم البحث العكسي حسب التجزئة
3. عند مواجهة LS2 مشفّر، استرجع المفتاح العام من دفتر العناوين
4. لا حاجة إلى صيغة base32 جديدة إذا كان Destination الكامل معروف مسبقًا

**تنسيقات دفتر العناوين التي تدعم LS2 المُشفَّر:** - hosts.txt مع سلاسل الوجهة الكاملة - قواعد بيانات SQLite مع عمود الوجهة - تنسيقات JSON/XML مع بيانات الوجهة الكاملة

### أمثلة على التنفيذ

**مثال 1: توليد عنوان**

```python
# Ed25519 destination example
pubkey = bytes.fromhex('a' * 64)  # 32-byte public key
unblinded_type = 7   # Ed25519
blinded_type = 11    # Red25519 (always)

address = generate_encrypted_b32_address(pubkey, unblinded_type, blinded_type)
print(f"Address: {address}")
# Output: 56 base32 characters + .b32.i2p
```
**مثال 2: التحليل والتحقق**

```python
address = "abc...xyz.b32.i2p"  # 56 chars + suffix

try:
    pubkey, unblinded, blinded = parse_encrypted_b32_address(address)
    print(f"Public Key: {pubkey.hex()}")
    print(f"Unblinded SigType: {unblinded}")
    print(f"Blinded SigType: {blinded}")
except ValueError as e:
    print(f"Invalid address: {e}")
```
**مثال 3: التحويل من Destination (الوجهة في I2P)**

```python
def destination_to_encrypted_b32(destination):
    """
    Convert full Destination to encrypted LS2 base32 address.
    
    Args:
        destination: I2P Destination object
    
    Returns:
        Base32 address string
    """
    # Extract public key and signature type from destination
    pubkey = destination.signing_public_key  # 32 bytes
    sigtype = destination.sig_type  # 7 or 11
    
    # Blinded type is always 11 (Red25519)
    blinded_type = 11
    
    # Generate address
    return generate_encrypted_b32_address(pubkey, sigtype, blinded_type)
```
### اعتبارات الأمان

**الخصوصية:** - يكشف عنوان Base32 المفتاح العام - هذا مقصود ومطلوب من أجل البروتوكول - لا يكشف المفتاح الخاص ولا يعرّض الأمان للخطر - المفاتيح العامة معلومات علنية بطبيعتها

**مقاومة التصادم:** - يوفر CRC-32 32 بتًا فقط من مقاومة التصادم - غير آمن من الناحية التشفيرية (يُستخدم للكشف عن الأخطاء فقط) - لا تعتمد إطلاقًا على المجموع الاختباري للمصادقة - لا يزال التحقق الكامل من الوجهة مطلوبًا

**التحقق من صحة العنوان:** - تحقق دائمًا من المجموع الاختباري (checksum) قبل الاستخدام - ارفض العناوين ذات أنواع التوقيع غير الصالحة - تحقق من أن المفتاح العام يقع على المنحنى (خاص بالتنفيذ)

**المراجع:** - [المقترح 149: B32 لـ LS2 المشفّر](/proposals/149-b32-encrypted-ls2/) - [مواصفة عنونة B32](/docs/specs/b32-for-encrypted-leasesets/) - [مواصفة التسمية لـ I2P](/docs/overview/naming/)

---

## دعم المفاتيح غير المتصلة

### نظرة عامة

تتيح المفاتيح غير المتصلة بالإنترنت إبقاء مفتاح التوقيع الرئيسي غير متصل بالإنترنت (التخزين البارد)، بينما يُستخدم مفتاح توقيع مؤقت للعمليات اليومية. يُعدّ ذلك بالغ الأهمية للخدمات عالية الأمان.

**متطلبات خاصة بـ LS2 المشفّر:** - يجب توليد المفاتيح المؤقتة دون اتصال بالإنترنت - يجب توليد المفاتيح الخاصة المُعمّاة (blinded) مسبقاً (مفتاح واحد يومياً) - تُسلَّم كلّ من المفاتيح المؤقتة والمفاتيح المُعمّاة على دفعات - لم يُحدَّد بعد معيار موحّد لصيغة الملف (TODO في المواصفة)

### بنية المفاتيح دون اتصال

**بيانات المفتاح المؤقتة للطبقة 0 (عندما يكون بت العلم 0 = 1):**

```
┌───────────────────────────────────────────────────┐
│ Expires Timestamp       │ 4 bytes (seconds)       │
│ Transient Sig Type      │ 2 bytes (big endian)    │
│ Transient Signing Pubkey│ Variable (sigtype len)  │
│ Signature (by blinded)  │ 64 bytes (Red25519)     │
└───────────────────────────────────────────────────┘
```
**تغطية التوقيع:** يغطي التوقيع في كتلة المفتاح غير المتصل: - الطابع الزمني لانتهاء الصلاحية (4 بايتات) - نوع التوقيع المؤقت (2 بايتين)   - مفتاح التوقيع العام المؤقت (متغير)

يتم التحقق من هذا التوقيع باستخدام **blinded public key** (مفتاح عام خضع لتقنية التعمية العمياء)، مما يثبت أن الكيان الذي يمتلك blinded private key (مفتاح خاص خضع لتقنية التعمية العمياء) قد أجاز هذا المفتاح المؤقت.

### عملية توليد المفاتيح

**بالنسبة إلى LeaseSet مُشفَّر بمفاتيح غير متصلة:**

1. **أنشئ أزواج مفاتيح مؤقتة** (بدون اتصال، في التخزين البارد):
   ```python
   # For each day in future
   for date in future_dates:
       # Generate daily transient keypair
       transient_privkey = generate_red25519_privkey()  # Type 11
       transient_pubkey = derive_public(transient_privkey)

       # Store for later delivery
       keys[date] = (transient_privkey, transient_pubkey)
   ```

2. **Generate daily blinded keypairs** (offline, in cold storage):
   ```python
# لكل يوم    for date in future_dates:

       # Derive alpha for this date
       datestring = date.strftime("%Y%m%d")  # "YYYYMMDD"
       alpha = GENERATE_ALPHA(destination, datestring, secret)
       
       # Blind the signing private key
       a = destination_signing_privkey  # Type 7 or 11
       blinded_privkey = BLIND_PRIVKEY(a, alpha)  # Result is type 11
       blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
       
       # Store for later delivery
       blinded_keys[date] = (blinded_privkey, blinded_pubkey)
   ```

3. **Sign transient keys with blinded keys** (offline):
   ```python
for date in future_dates:

       transient_pubkey = keys[date][1]
       blinded_privkey = blinded_keys[date][0]
       
       # Create signature data
       expires = int((date + timedelta(days=1)).timestamp())
       sig_data = struct.pack('>I', expires)  # 4 bytes
       sig_data += struct.pack('>H', 11)     # Transient type (Red25519)
       sig_data += transient_pubkey          # 32 bytes
       
       # Sign with blinded private key
       signature = RED25519_SIGN(blinded_privkey, sig_data)
       
       # Package for delivery
       offline_sig_blocks[date] = {
           'expires': expires,
           'transient_type': 11,
           'transient_pubkey': transient_pubkey,
           'signature': signature
       }
   ```

4. **Package for delivery to router:**
   ```python
# لكل تاريخ    delivery_package[date] = {

       'transient_privkey': keys[date][0],
       'transient_pubkey': keys[date][1],
       'blinded_privkey': blinded_keys[date][0],
       'blinded_pubkey': blinded_keys[date][1],
       'offline_sig_block': offline_sig_blocks[date]
}

   ```

### Router Usage

**Daily Key Loading:**

```python
# عند منتصف الليل بتوقيت UTC (أو قبل النشر)

date = datetime.utcnow().date()

# حمّل مفاتيح اليوم

today_keys = load_delivery_package(date)

transient_privkey = today_keys['transient_privkey'] transient_pubkey = today_keys['transient_pubkey'] blinded_privkey = today_keys['blinded_privkey'] blinded_pubkey = today_keys['blinded_pubkey'] offline_sig_block = today_keys['offline_sig_block']

# استخدم هذه المفاتيح لـ LeaseSet المشفّر لهذا اليوم

```

**Publishing Process:**

```python
# 1. أنشئ LeaseSet2 داخلي

inner_ls2 = create_leaseset2(

    destinations, leases, expires, 
    signing_key=transient_privkey  # Use transient key
)

# 2. تشفير الطبقة الثانية

layer2_ciphertext = encrypt_layer2(inner_ls2, authCookie, subcredential, timestamp)

# 3. أنشئ الطبقة الأولى مع بيانات التخويل

layer1_plaintext = create_layer1(authorization_data, layer2_ciphertext)

# 4. شفّر الطبقة 1

layer1_ciphertext = encrypt_layer1(layer1_plaintext, subcredential, timestamp)

# 5. أنشئ الطبقة 0 مع كتلة توقيع دون اتصال

layer0 = create_layer0(

    blinded_pubkey,
    timestamp,
    expires,
    flags=0x0001,  # Bit 0 set (offline keys present)
    offline_sig_block=offline_sig_block,
    layer1_ciphertext=layer1_ciphertext
)

# 6. وقّع الطبقة 0 باستخدام مفتاح خاص مؤقت

signature = RED25519_SIGN(transient_privkey, layer0)

# 7. ألحِق التوقيع ثم انشر

encrypted_leaseset = layer0 + signature publish_to_netdb(encrypted_leaseset)

```

### Security Considerations

**Tracking via Offline Signature Block:**

The offline signature block is in plaintext (Layer 0). An adversary scraping floodfills could:
- Track the same encrypted LeaseSet across multiple days
- Correlate encrypted LeaseSets even though blinded keys change daily

**Mitigation:** Generate new transient keys daily (in addition to blinded keys):

```python
# ولّد كلاً من المفاتيح المؤقتة الجديدة والمفاتيح المُعمّاة الجديدة يومياً

for date in future_dates:

    # New transient keypair for this day
    transient_privkey = generate_red25519_privkey()
    transient_pubkey = derive_public(transient_privkey)
    
    # New blinded keypair for this day
    alpha = GENERATE_ALPHA(destination, datestring, secret)
    blinded_privkey = BLIND_PRIVKEY(signing_privkey, alpha)
    blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
    
    # Sign new transient key with new blinded key
    sig = RED25519_SIGN(blinded_privkey, transient_pubkey || metadata)
    
    # Now offline sig block changes daily
```

**Benefits:**
- Prevents tracking across days via offline signature block
- Provides same security as encrypted LS2 without offline keys
- Each day appears completely independent

**Cost:**
- More keys to generate and store
- More complex key management

### File Format (TODO)

**Current Status:** No standardized file format defined for batch key delivery.

**Requirements for Future Format:**

1. **Must support multiple dates:**
   - Batch delivery of 30+ days worth of keys
   - Clear date association for each key set

2. **Must include all necessary data:**
   - Transient private key
   - Transient public key
   - Blinded private key
   - Blinded public key
   - Pre-computed offline signature block
   - Expiration timestamps

3. **Should be tamper-evident:**
   - Checksums or signatures over entire file
   - Integrity verification before loading

4. **Should be encrypted:**
   - Keys are sensitive material
   - Encrypt file with router's key or passphrase

**Proposed Format Example (JSON, encrypted):**

```json
{   "version": 1,   "destination_hash": "base64...",   "keys": [

    {
      "date": "2025-10-15",
      "transient": {
        "type": 11,
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "blinded": {
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "offline_sig_block": {
        "expires": 1729123200,
        "signature": "base64..."
      }
    }
],   "signature": "base64..."  // Signature over entire structure }

```

### I2CP Protocol Enhancement (TODO)

**Current Status:** No I2CP protocol enhancement defined for offline keys with encrypted LeaseSet.

**Requirements:**

1. **Key delivery mechanism:**
   - Upload batch of keys from client to router
   - Acknowledgment of successful key loading

2. **Key expiration notification:**
   - Router notifies client when keys running low
   - Client can generate and upload new batch

3. **Key revocation:**
   - Emergency revocation of future keys if compromise suspected

**Proposed I2CP Messages:**

```
UPLOAD_OFFLINE_KEYS   - مجموعة من بيانات المفاتيح المشفّرة   - الفترة الزمنية المشمولة

OFFLINE_KEY_STATUS   - عدد الأيام المتبقية   - تاريخ انتهاء صلاحية المفتاح التالي

REVOKE_OFFLINE_KEYS     - نطاق التواريخ للإلغاء   - مفاتيح جديدة للاستبدال (اختياري)

```

### Implementation Status

**Java I2P:**
- ✅ Offline keys for standard LS2: Fully supported (since 0.9.38)
- ⚠️ Offline keys for encrypted LS2: Implemented (since 0.9.40)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**i2pd (C++):**
- ✅ Offline keys for standard LS2: Fully supported
- ✅ Offline keys for encrypted LS2: Fully supported (since 2.58.0)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**References:**
- [Offline Signatures Proposal](/proposals/123-new-netdb-entries/)
- [I2CP Specification](/docs/specs/i2cp/)

---

## Security Considerations

### Cryptographic Security

**Algorithm Selection:**

All cryptographic primitives are based on well-studied algorithms:
- **ChaCha20:** Modern stream cipher, constant-time, no timing attacks
- **SHA-256:** NIST-approved hash, 128-bit security level
- **HKDF:** RFC 5869 standard, proven security bounds
- **Ed25519/Red25519:** Curve25519-based, ~128-bit security level
- **X25519:** Diffie-Hellman over Curve25519, ~128-bit security level

**Key Sizes:**
- All symmetric keys: 256 bits (32 bytes)
- All public/private keys: 256 bits (32 bytes)
- All nonces/IVs: 96 bits (12 bytes)
- All signatures: 512 bits (64 bytes)

These sizes provide adequate security margins against current and near-future attacks.

### Forward Secrecy

**Daily Key Rotation:**

Encrypted LeaseSets rotate keys daily (UTC midnight):
- New blinded public/private key pair
- New storage location in DHT
- New encryption keys for both layers

**Benefits:**
- Compromising today's blinded key doesn't reveal yesterday's
- Limits exposure window to 24 hours
- Prevents long-term tracking via DHT

**Enhanced with Ephemeral Keys:**

DH client authorization uses ephemeral keys:
- Server generates new ephemeral DH keypair for each publication
- Compromising ephemeral key only affects that publication
- True forward secrecy even if long-term keys compromised

### Privacy Properties

**Destination Blinding:**

The blinded public key:
- Is unlinkable to the original destination (without knowing the secret)
- Changes daily, preventing long-term correlation
- Cannot be reversed to find the original public key

**Client Membership Privacy:**

Per-client authorization provides:
- **Anonymity:** No way to identify which clients are authorized
- **Untraceability:** Cannot track when specific clients added/revoked
- **Size obfuscation:** Can add dummy entries to hide true count

**DHT Privacy:**

Storage location rotates daily:
```
location = SHA-256(sig_type || blinded_public_key)

```

This prevents:
- Correlation across days via DHT lookups
- Long-term monitoring of service availability
- Traffic analysis of DHT queries

### Threat Model

**Adversary Capabilities:**

1. **Network Adversary:**
   - Can monitor all DHT traffic
   - Can observe encrypted LeaseSet publications
   - Cannot decrypt without proper keys

2. **Floodfill Adversary:**
   - Can store and analyze all encrypted LeaseSets
   - Can track publication patterns over time
   - Cannot decrypt Layer 1 or Layer 2
   - Can see client count (but not identities)

3. **Authorized Client Adversary:**
   - Can decrypt specific encrypted LeaseSets
   - Can access inner LeaseSet2 data
   - Cannot determine other clients' identities
   - Cannot decrypt past LeaseSets (with ephemeral keys)

**Out of Scope:**

- Malicious router implementations
- Compromised router host systems
- Side-channel attacks (timing, power analysis)
- Physical access to keys
- Social engineering attacks

### Attack Scenarios

**1. Offline Keys Tracking Attack:**

**Attack:** Adversary tracks encrypted LeaseSets via unchanging offline signature block.

**Mitigation:** Generate new transient keys daily (in addition to blinded keys).

**Status:** Documented recommendation, implementation-specific.

**2. Client Position Inference Attack:**

**Attack:** If client order is static, clients can infer their position and detect when other clients added/removed.

**Mitigation:** Randomize client order in authorization list for each publication.

**Status:** Documented recommendation in specification.

**3. Client Count Analysis Attack:**

**Attack:** Adversary monitors client count changes over time to infer service popularity or client churn.

**Mitigation:** Add random dummy entries to authorization list.

**Status:** Optional feature, deployment-specific trade-off (size vs. privacy).

**4. PSK Interception Attack:**

**Attack:** Adversary intercepts PSK during out-of-band exchange and can decrypt all future encrypted LeaseSets.

**Mitigation:** Use DH client authorization instead, or ensure secure key exchange (Signal, OTR, PGP).

**Status:** Known limitation of PSK approach, documented in specification.

**5. Timing Correlation Attack:**

**Attack:** Adversary correlates publication times across days to link encrypted LeaseSets.

**Mitigation:** Randomize publication times, use delayed publishing.

**Status:** Implementation-specific, not addressed in core specification.

**6. Long-term Secret Compromise:**

**Attack:** Adversary compromises the blinding secret and can compute all past and future blinded keys.

**Mitigation:** 
- Use optional secret parameter (not empty)
- Rotate secret periodically
- Use different secrets for different services

**Status:** Secret parameter is optional; using it is highly recommended.

### Operational Security

**Key Management:**

1. **Signing Private Key:**
   - Store offline in cold storage
   - Use only for generating blinded keys (batch process)
   - Never expose to online router

2. **Blinded Private Keys:**
   - Generate offline, deliver in batches
   - Rotate daily automatically
   - Delete after use (forward secrecy)

3. **Transient Private Keys (with offline keys):**
   - Generate offline, deliver in batches
   - Can be longer-lived (days/weeks)
   - Rotate regularly for enhanced privacy

4. **Client Authorization Keys:**
   - DH: Client private keys never leave client device
   - PSK: Use unique keys per client, secure exchange
   - Revoke immediately upon client removal

**Secret Management:**

The optional secret parameter in `GENERATE_ALPHA`:
- SHOULD be used for high-security services
- MUST be transmitted securely to authorized clients
- SHOULD be rotated periodically (e.g., monthly)
- CAN be different for different client groups

**Monitoring and Auditing:**

1. **Publication Monitoring:**
   - Verify encrypted LeaseSets published successfully
   - Monitor floodfill acceptance rates
   - Alert on publication failures

2. **Client Access Monitoring:**
   - Log client authorization attempts (without identifying clients)
   - Monitor for unusual patterns
   - Detect potential attacks early

3. **Key Rotation Auditing:**
   - Verify daily key rotation occurs
   - Check blinded key changes daily
   - Ensure old keys are deleted

### Implementation Security

**Constant-Time Operations:**

Implementations MUST use constant-time operations for:
- All scalar arithmetic (mod L operations)
- Private key comparisons
- Signature verification
- DH key agreement

**Memory Security:**

- Zero sensitive key material after use
- Use secure memory allocation for keys
- Prevent keys from being paged to disk
- Clear stack variables containing key material

**Random Number Generation:**

- Use cryptographically secure RNG (CSRNG)
- Properly seed RNG from OS entropy source
- Do not use predictable RNGs for key material
- Verify RNG output quality periodically

**Input Validation:**

- Validate all public keys are on the curve
- Check all signature types are supported
- Verify all lengths before parsing
- Reject malformed encrypted LeaseSets early

**Error Handling:**

- Do not leak information via error messages
- Use constant-time comparison for authentication
- Do not expose timing differences in decryption
- Log security-relevant events properly

### Recommendations

**For Service Operators:**

1. ✅ **Use Red25519 (type 11)** for new destinations
2. ✅ **Use DH client authorization** for high-security services
3. ✅ **Generate new transient keys daily** when using offline keys
4. ✅ **Use the optional secret parameter** in GENERATE_ALPHA
5. ✅ **Randomize client order** in authorization lists
6. ✅ **Monitor publication success** and investigate failures
7. ⚠️ **Consider dummy entries** to hide client count (size trade-off)

**For Client Implementers:**

1. ✅ **Validate blinded public keys** are on prime-order subgroup
2. ✅ **Verify all signatures** before trusting data
3. ✅ **Use constant-time operations** for cryptographic primitives
4. ✅ **Zero key material** immediately after use
5. ✅ **Implement proper error handling** without information leaks
6. ✅ **Support both Ed25519 and Red25519** destination types

**For Network Operators:**

1. ✅ **Accept encrypted LeaseSets** in floodfill routers
2. ✅ **Enforce reasonable size limits** to prevent abuse
3. ✅ **Monitor for anomalous patterns** (extremely large, frequent updates)
4. ⚠️ **Consider rate limiting** encrypted LeaseSet publications

---

## Implementation Notes

### Java I2P Implementation

**Repository:** https://github.com/i2p/i2p.i2p

**Key Classes:**
- `net.i2p.data.LeaseSet2` - LeaseSet2 structure
- `net.i2p.data.EncryptedLeaseSet` - Encrypted LS2 implementation
- `net.i2p.crypto.eddsa.EdDSAEngine` - Ed25519/Red25519 signatures
- `net.i2p.crypto.HKDF` - HKDF implementation
- `net.i2p.crypto.ChaCha20` - ChaCha20 cipher

**Configuration:**

Enable encrypted LeaseSet in `clients.config`:
```properties
# تفعيل LeaseSet المشفّر (بنية بيانات تنشر معلومات الاتصال الخاصة بوجهة داخل I2P)

i2cp.encryptLeaseSet=true

# اختياري: تمكين تخويل العميل

i2cp.enableAccessList=true

# اختياري: استخدم DH authorization (مصادقة باستخدام تبادل المفاتيح ديفي–هيلمان؛ الإعداد الافتراضي هو PSK (مفتاح مُشترك مُسبقاً))

i2cp.accessListType=0

# اختياري: سر الإعماء (موصى به بشدة)

i2cp.blindingSecret=your-secret-here

```

**API Usage Example:**

```java
// أنشئ LeaseSet مشفّر EncryptedLeaseSet els = new EncryptedLeaseSet();

// تعيين الوجهة els.setDestination(destination);

// تمكين التخويل لكل عميل على حدة els.setAuthorizationEnabled(true); els.setAuthType(EncryptedLeaseSet.AUTH_DH);

// أضف العملاء المصرّح لهم (مفاتيح DH العامة — خوارزمية ديفي-هيلمان) for (byte[] clientPubKey : authorizedClients) {

    els.addClient(clientPubKey);
}

// اضبط معلمات الإعماء (blinding) els.setBlindingSecret("your-secret");

// وقّع وانشر els.sign(signingPrivateKey); netDb.publish(els);

```

### i2pd (C++) Implementation

**Repository:** https://github.com/PurpleI2P/i2pd

**Key Files:**
- `libi2pd/LeaseSet.h/cpp` - LeaseSet implementations
- `libi2pd/Crypto.h/cpp` - Cryptographic primitives
- `libi2pd/Ed25519.h/cpp` - Ed25519/Red25519 signatures
- `libi2pd/ChaCha20.h/cpp` - ChaCha20 cipher

**Configuration:**

Enable in tunnel configuration (`tunnels.conf`):
```ini
[my-hidden-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# تفعيل LeaseSet المشفّر

encryptleaseset = true

# اختياري: نوع تخويل العميل (0=DH, 1=PSK)

authtype = 0

# اختياري: Blinding secret (سر الإعماء)

secret = السر-الخاص-بك-هنا

# اختياري: العملاء المصرح لهم (واحد في كل سطر، مفاتيح عامة مرمزة بترميز base64)

client.1 = base64-encoded-client-pubkey-1 client.2 = base64-encoded-client-pubkey-2

```

**API Usage Example:**

```cpp
// إنشاء LeaseSet مشفّر auto encryptedLS = std::make_shared<i2p::data::EncryptedLeaseSet>(

    destination,
    blindingSecret
);

// تفعيل التخويل لكل عميل
encryptedLS->SetAuthType(i2p::data::AUTH_TYPE_DH);

// إضافة العملاء المصرح لهم for (const auto& clientPubKey : authorizedClients) {

    encryptedLS->AddClient(clientPubKey);
}

// وقّع وانشر encryptedLS->Sign(signingPrivKey); netdb.Publish(encryptedLS);

```

### Testing and Debugging

**Test Vectors:**

Generate test vectors for implementation verification:

```python
# متجه الاختبار 1: Key blinding (إعماء المفتاح)

destination_pubkey = bytes.fromhex('a' * 64) sigtype = 7 blinded_sigtype = 11 date = "20251015" secret = ""

alpha = generate_alpha(destination_pubkey, sigtype, blinded_sigtype, date, secret) print(f"Alpha: {alpha.hex()}")

# المتوقع: (تحقق بالمقارنة مع التنفيذ المرجعي)

```

**Unit Tests:**

Key areas to test:
1. HKDF derivation with various inputs
2. ChaCha20 encryption/decryption
3. Red25519 signature generation and verification
4. Key blinding (private and public)
5. Layer 1/2 encryption/decryption
6. Client authorization (DH and PSK)
7. Base32 address generation and parsing

**Integration Tests:**

1. Publish encrypted LeaseSet to test network
2. Retrieve and decrypt from client
3. Verify daily key rotation
4. Test client authorization (add/remove clients)
5. Test offline keys (if supported)

**Common Implementation Errors:**

1. **Incorrect mod L reduction:** Must use proper modular arithmetic
2. **Endianness errors:** Most fields are big-endian, but some crypto uses little-endian
3. **Off-by-one in array slicing:** Verify indices are inclusive/exclusive as needed
4. **Missing constant-time comparisons:** Use constant-time for all sensitive comparisons
5. **Not zeroing key material:** Always zero keys after use

### Performance Considerations

**Computational Costs:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Cost</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per publication</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 point add + 1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 X25519 ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N = number of clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 X25519 op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 DH ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Only HKDF + ChaCha20</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature (Red25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 signature op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Similar cost to Ed25519</td></tr>
  </tbody>
</table>

**Size Overhead:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded public key</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH ephemeral pubkey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if DH auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK salt</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if PSK auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline sig block</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈100 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if offline keys)</td></tr>
  </tbody>
</table>

**Typical Sizes:**

- **No client auth:** ~200 bytes overhead
- **With 10 DH clients:** ~600 bytes overhead
- **With 100 DH clients:** ~4200 bytes overhead

**Optimization Tips:**

1. **Batch key generation:** Generate blinded keys for multiple days in advance
2. **Cache subcredentials:** Compute once per day, reuse for all publications
3. **Reuse ephemeral keys:** Can reuse ephemeral DH key for short period (minutes)
4. **Parallel client encryption:** Encrypt client cookies in parallel
5. **Fast path for no auth:** Skip authorization layer entirely when disabled

### Compatibility

**Backward Compatibility:**

- Ed25519 (type 7) destinations supported for unblinded keys
- Red25519 (type 11) required for blinded keys
- Traditional LeaseSets still fully supported
- Encrypted LeaseSets do not break existing network

**Forward Compatibility:**

- Reserved flag bits for future features
- Extensible authorization scheme (3 bits allow 8 types)
- Version field in various structures

**Interoperability:**

- Java I2P and i2pd fully interoperable since:
  - Java I2P 0.9.40 (May 2019)
  - i2pd 2.58.0 (September 2025)
- Encrypted LeaseSets work across implementations
- Client authorization works across implementations

---

## References

### IETF RFCs

- **[RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104)** - HMAC: Keyed-Hashing for Message Authentication (February 1997)
- **[RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869)** - HMAC-based Extract-and-Expand Key Derivation Function (HKDF) (May 2010)
- **[RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539)** - ChaCha20 and Poly1305 for IETF Protocols (May 2015)
- **[RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748)** - Elliptic Curves for Security (January 2016)

### I2P Specifications

- **[Common Structures Specification](/docs/specs/common-structures/)** - LeaseSet2 and EncryptedLeaseSet structures
- **[Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/)** - Background and design of LeaseSet2
- **[Proposal 146: Red25519](/proposals/146-red25519/)** - Red25519 signature scheme specification
- **[Proposal 149: B32 for Encrypted LS2](/proposals/149-b32-encrypted-ls2/)** - Base32 addressing for encrypted LeaseSets
- **[Red25519 Specification](/docs/specs/red25519-signature-scheme/)** - Detailed Red25519 implementation
- **[B32 Addressing Specification](/docs/specs/b32-for-encrypted-leasesets/)** - Base32 address format
- **[Network Database Documentation](/docs/specs/common-structures/)** - NetDB usage and operations
- **[I2CP Specification](/docs/specs/i2cp/)** - I2P Client Protocol

### Cryptographic References

- **[Ed25519 Paper](http://cr.yp.to/papers.html#ed25519)** - "High-speed high-security signatures" by Bernstein et al.
- **[ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf)** - Section 5.4.6: RedDSA signature scheme
- **[Tor Rendezvous Specification v3](https://spec.torproject.org/rend-spec)** - Tor's onion service specification (for comparison)

### Security References

- **[Key Blinding Security Discussion](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)** - Tor Project mailing list discussion
- **[Tor Ticket #8106](https://trac.torproject.org/projects/tor/ticket/8106)** - Key blinding implementation discussion
- **[PRNG Security](http://projectbullrun.org/dual-ec/ext-rand.html)** - Random number generator security considerations
- **[Tor PRNG Discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)** - Discussion of PRNG usage in Tor

### Implementation References

- **[Java I2P Repository](https://github.com/i2p/i2p.i2p)** - Official Java implementation
- **[i2pd Repository](https://github.com/PurpleI2P/i2pd)** - C++ implementation
- **[I2P Website](/)** - Official I2P project website
- **[I2P Specifications](/docs/specs/)** - Complete specification index

### Version History

- **[I2P Release Notes](/en/blog)** - Official release announcements
- **[Java I2P Releases](https://github.com/i2p/i2p.i2p/releases)** - GitHub release history
- **[i2pd Releases](https://github.com/PurpleI2P/i2pd/releases)** - GitHub release history

---

## Appendix A: Cryptographic Constants

### Ed25519 / Red25519 Constants

```python
# نقطة الأساس لـ Ed25519 (المولِّد)

B = 2**255 - 19

# رتبة Ed25519 (حجم الحقل العددي)

L = 2**252 + 27742317777372353535851937790883648493

# قيم أنواع التوقيع

SIGTYPE_ED25519 = 7    # 0x0007 SIGTYPE_RED25519 = 11  # 0x000b

# أحجام المفاتيح

PRIVKEY_SIZE = 32  # بايت PUBKEY_SIZE = 32   # بايت SIGNATURE_SIZE = 64  # بايت

```

### ChaCha20 Constants

```python
# معاملات ChaCha20 (خوارزمية تشفير تياري)

CHACHA20_KEY_SIZE = 32   # bytes (256 bits) CHACHA20_NONCE_SIZE = 12  # bytes (96 bits) CHACHA20_INITIAL_COUNTER = 1  # RFC 7539 permits 0 or 1

```

### HKDF Constants

```python
# معاملات HKDF (دالة اشتقاق المفاتيح المعتمدة على HMAC)

HKDF_HASH = "SHA-256" HKDF_SALT_MAX = 32  # بايت (HashLen)

# سلاسل info النصية الخاصة بـ HKDF (دالة اشتقاق مفاتيح مستندة إلى HMAC) (فصل المجالات)

HKDF_INFO_ALPHA = b"i2pblinding1" HKDF_INFO_LAYER1 = b"ELS2_L1K" HKDF_INFO_LAYER2 = b"ELS2_L2K" HKDF_INFO_DH_AUTH = b"ELS2_XCA" HKDF_INFO_PSK_AUTH = b"ELS2PSKA"

```

### Hash Personalization Strings

```python
# سلاسل تخصيص SHA-256

HASH_PERS_ALPHA = b"I2PGenerateAlpha" HASH_PERS_RED25519 = b"I2P_Red25519H(x)" HASH_PERS_CREDENTIAL = b"credential" HASH_PERS_SUBCREDENTIAL = b"subcredential"

```

### Structure Sizes

```python
# أحجام الطبقة 0 (الخارجية)

BLINDED_SIGTYPE_SIZE = 2   # بايت BLINDED_PUBKEY_SIZE = 32   # بايت (خاصة بـ Red25519) PUBLISHED_TS_SIZE = 4      # بايت EXPIRES_SIZE = 2           # بايت FLAGS_SIZE = 2             # بايت LEN_OUTER_CIPHER_SIZE = 2  # بايت SIGNATURE_SIZE = 64        # بايت (Red25519)

# أحجام كتل المفاتيح في وضع عدم الاتصال

OFFLINE_EXPIRES_SIZE = 4   # بايت OFFLINE_SIGTYPE_SIZE = 2   # بايت OFFLINE_SIGNATURE_SIZE = 64  # بايت

# أحجام الطبقة 1 (الوسطى)

AUTH_FLAGS_SIZE = 1        # بايت EPHEMERAL_PUBKEY_SIZE = 32  # بايتات (مصادقة DH) AUTH_SALT_SIZE = 32        # بايتات (مصادقة PSK) NUM_CLIENTS_SIZE = 2       # بايتات CLIENT_ID_SIZE = 8         # بايتات CLIENT_COOKIE_SIZE = 32    # بايتات AUTH_CLIENT_ENTRY_SIZE = 40  # بايتات (CLIENT_ID + CLIENT_COOKIE)

# العبء الإضافي للتشفير

SALT_SIZE = 32  # بايت (يُضاف في المقدمة إلى كل طبقة مُشفّرة)

# عنوان Base32 (ترميز أساس 32)

B32_ENCRYPTED_DECODED_SIZE = 35  # بايت B32_ENCRYPTED_ENCODED_LEN = 56   # محارف B32_SUFFIX = ".b32.i2p"

```

---

## Appendix B: Test Vectors

### Test Vector 1: Alpha Generation

**Input:**
```python
# المفتاح العام للوجهة (Ed25519)

A = bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') stA = 0x0007  # Ed25519 stA_prime = 0x000b  # Red25519 date = "20251015" secret = ""  # Empty secret

```

**Computation:**
```python
keydata = A || bytes([0x00, 0x07]) || bytes([0x00, 0x0b])

# keydata = 36 بايت

salt = SHA256(b"I2PGenerateAlpha" + keydata) ikm = b"20251015" info = b"i2pblinding1"

seed = HKDF(salt, ikm, info, 64) alpha = LEOS2IP(seed) mod L

```

**Expected Output:**
```
(تحقق مقابل التنفيذ المرجعي) alpha = [قيمة سداسية عشرية بطول 64 بايت]

```

### Test Vector 2: ChaCha20 Encryption

**Input:**
```python
key = bytes([i for i in range(32)])  # 0x00..0x1f nonce = bytes([i for i in range(12)])  # 0x00..0x0b plaintext = b"Hello, I2P!"

```

**Computation:**
```python
ciphertext = ChaCha20_Encrypt(key, nonce, plaintext, counter=1)

```

**Expected Output:**
```
النص المشفّر = [تحقّق بمطابقته مع متجهات الاختبار الخاصة بـ RFC 7539]

```

### Test Vector 3: HKDF

**Input:**
```python
salt = bytes(32)  # كلها أصفار ikm = b"test input keying material" info = b"ELS2_L1K" n = 44

```

**Computation:**
```python
keys = HKDF(salt, ikm, info, n)

```

**Expected Output:**
```
keys = [قيمة سداسية عشرية بطول 44 بايت]

```

### Test Vector 4: Base32 Address

**Input:**
```python
pubkey = bytes.fromhex('bbbb' + 'bb' * 30)  # 32 بايت unblinded_sigtype = 11  # Red25519 blinded_sigtype = 11    # Red25519

```

**Computation:**
```python
address = generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype)

```

**Expected Output:**
```
address = [56 محارف base32].b32.i2p

# تحقّق من أن التحقق من المجموع الاختباري يتم بشكل صحيح

```

---

## Appendix C: Glossary

**Alpha (α):** The secret blinding factor used to blind public and private keys. Generated from the destination, date, and optional secret.

**AuthCookie:** A 32-byte random value encrypted for each authorized client, used as input to Layer 2 encryption.

**B (Base Point):** The generator point for the Ed25519 elliptic curve.

**Blinded Key:** A public or private key that has been transformed using the alpha blinding factor. Blinded keys cannot be linked to the original keys without knowing alpha.

**ChaCha20:** A stream cipher providing fast, secure encryption without requiring AES hardware support.

**ClientID:** An 8-byte identifier derived from HKDF output, used to identify authorization entries for clients.

**ClientCookie:** A 32-byte encrypted value containing the authCookie for a specific client.

**Credential:** A 32-byte value derived from the destination's public key and signature types, binding encryption to knowledge of the destination.

**CSRNG:** Cryptographically Secure Random Number Generator. Must provide unpredictable output suitable for key generation.

**DH (Diffie-Hellman):** A cryptographic protocol for securely establishing shared secrets. I2P uses X25519.

**Ed25519:** An elliptic curve signature scheme providing fast signatures with 128-bit security level.

**Ephemeral Key:** A short-lived cryptographic key, typically used once and then discarded.

**Floodfill:** I2P routers that store and serve network database entries, including encrypted LeaseSets.

**HKDF:** HMAC-based Key Derivation Function, used to derive multiple cryptographic keys from a single source.

**L (Order):** The order of the Ed25519 scalar field (approximately 2^252).

**Layer 0 (Outer):** The plaintext portion of an encrypted LeaseSet, containing blinded key and metadata.

**Layer 1 (Middle):** The first encrypted layer, containing client authorization data.

**Layer 2 (Inner):** The innermost encrypted layer, containing the actual LeaseSet2 data.

**LeaseSet2 (LS2):** Second version of I2P's network database entry format, introducing encrypted variants.

**NetDB:** The I2P network database, a distributed hash table storing router and destination information.

**Offline Keys:** A feature allowing the main signing key to remain in cold storage while a transient key handles daily operations.

**PSK (Pre-Shared Key):** A symmetric key shared in advance between two parties, used for PSK client authorization.

**Red25519:** An Ed25519-based signature scheme with key blinding support, based on ZCash RedDSA.

**Salt:** Random data used as input to key derivation functions to ensure unique outputs.

**SigType:** A numeric identifier for signature algorithms (e.g., 7 = Ed25519, 11 = Red25519).

**Subcredential:** A 32-byte value derived from the credential and blinded public key, binding encryption to a specific encrypted LeaseSet.

**Transient Key:** A temporary signing key used with offline keys, with a limited validity period.

**X25519:** An elliptic curve Diffie-Hellman protocol over Curve25519, providing key agreement.

---

## Document Information

**Status:** This document represents the current stable encrypted LeaseSet specification as implemented in I2P since June 2019. The protocol is mature and widely deployed.

**Contributing:** For corrections or improvements to this documentation, please submit issues or pull requests to the I2P specifications repository.

**Support:** For questions about implementing encrypted LeaseSets:
- I2P Forum: https://i2pforum.net/
- IRC: #i2p-dev on OFTC
- Matrix: #i2p-dev:matrix.org

**Acknowledgments:** This specification builds on work by the I2P development team, ZCash cryptography research, and Tor Project's key blinding research.