---
title: "تشفير هجين باستخدام ECIES-X25519-AEAD-Ratchet (آلية تدوير المفاتيح تدريجياً)"
description: "صيغة هجينة لما بعد الكم من بروتوكول التشفير ECIES (مخطط التشفير المتكامل القائم على المنحنيات الإهليلجية) باستخدام ML-KEM (آلية تغليف مفاتيح قائمة على شبكيات الوحدات، من تقنيات ما بعد الكم)"
slug: "ecies-hybrid"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## حالة التنفيذ

**النشر الحالي:** - **i2pd (تنفيذ C++)**: مُنفَّذ بالكامل في الإصدار 2.58.0 (سبتمبر 2025) مع دعم ML-KEM-512 وML-KEM-768 وML-KEM-1024. يتم تمكين تشفير طرف إلى طرف ما بعد الكمّي افتراضيًا عند توفّر OpenSSL 3.5.0 أو أحدث. - **Java I2P**: لم يُنفَّذ بعد حتى الإصدار 0.9.67 / 2.10.0 (سبتمبر 2025). تمت الموافقة على المواصفة ويُخطَّط لتنفيذها في الإصدارات المستقبلية.

تصف هذه المواصفة الوظائف المعتمدة المطبّقة حالياً في i2pd والمخطَّط تنفيذها في تنفيذات Java I2P.

## نظرة عامة

هذا هو المتغيّر الهجين بعد الكمّ (post-quantum) لبروتوكول ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). وهو يمثّل المرحلة الأولى من المقترح 169 [Prop169](/proposals/169-pq-crypto/) المزمع اعتمادها. راجع ذلك المقترح للاطّلاع على الأهداف العامة، ونماذج التهديد، والتحليل، والبدائل، ومعلومات إضافية.

حالة المقترح 169: **مفتوح** (تمت الموافقة على المرحلة الأولى لتنفيذ هجين لـ ECIES (مخطط تشفير قائم على المنحنيات الإهليلجية)).

تتضمن هذه المواصفة فقط الفروقات عن معيار [ECIES](/docs/specs/ecies/) (مخطط تشفير متكامل على المنحنيات الإهليلجية)، ويجب قراءتها بالاقتران مع تلك المواصفة.

## التصميم

نستخدم معيار NIST FIPS 203 [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) المستند إلى، ولكنه غير متوافق مع، CRYSTALS-Kyber (خوارزمية تبادل مفاتيح ما بعد الكم) (الإصدارات 3.1 و3 والأقدم).

تجمع المصافحات الهجينة بين خوارزمية X25519 Diffie-Hellman (لتبادل المفاتيح) الكلاسيكية وآليات تغليف المفاتيح ML-KEM لما بعد الكمّي. يعتمد هذا النهج على مفاهيم السرية الأمامية الهجينة الموثّقة في أبحاث PQNoise وعلى تطبيقات مماثلة في TLS 1.3 وIKEv2 وWireGuard.

### تبادل المفاتيح

نعرّف تبادل مفاتيح هجيني للـ Ratchet (آلية تدوير المفاتيح). يوفّر Post-quantum KEM (آلية تغليف المفاتيح لما بعد الكم) مفاتيح مؤقتة فقط ولا يدعم مباشرة المصافحات ذات المفاتيح الثابتة مثل Noise IK (نمط مصافحة في إطار عمل Noise).

نُعرّف متغيرات ML-KEM الثلاثة (آلية تغليف المفاتيح القائمة على الشبكيات النمطية) كما هو محدد في [FIPS203](https://csrc.nist.gov/pubs/fips/203/final)، ليصبح لدينا في المجموع 3 أنواع تشفير جديدة. لا تُعرَّف الأنواع الهجينة إلا بالاقتران مع X25519.

أنواع التشفير الجديدة هي:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Security Level</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Variant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 1 (AES-128 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-512</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 3 (AES-192 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-768 (Recommended)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 5 (AES-256 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-1024</td>
    </tr>
  </tbody>
</table>
**ملاحظة:** MLKEM768_X25519 (Type 6) هو المتغيّر الافتراضي الموصى به، إذ يوفّر أمانًا قويًا ما بعد الكمّ مع تكلفة إضافية معقولة.

الحجم الإضافي كبير مقارنةً بتشفير X25519 (آلية تبادل مفاتيح مبنية على منحنى Curve25519) فقط. أحجام الرسالتين 1 و2 النموذجية (لنمط IK، وهو نمط مصافحة في بروتوكول Noise) تبلغ حاليًا نحو 96–103 بايت (قبل الحمولة الإضافية). وسيزداد ذلك بنحو 9–12 ضعفًا مع MLKEM512 (عائلة ML‑KEM، معيار تبادل مفاتيح مقاوم للكم صادر عن NIST)، و13–16 ضعفًا مع MLKEM768، و17–23 ضعفًا مع MLKEM1024، وذلك بحسب نوع الرسالة.

### مطلوب تشفير جديد

- **ML-KEM** (المعروف سابقًا باسم CRYSTALS-Kyber) [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) - معيار آلية تغليف المفاتيح القائمة على الشبكات النمطية
- **SHA3-256** (المعروف سابقًا باسم Keccak-512) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - جزء من معيار SHA-3
- **SHAKE128 و SHAKE256** (امتدادات XOF لـ SHA3؛ دالة بإخراج قابل للتمديد) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - دوال بإخراج قابل للتمديد

تتوفر متجهات الاختبار لـ SHA3-256 وSHAKE128 وSHAKE256 في [برنامج NIST للتحقق من صحة الخوارزميات التشفيرية](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program).

**دعم المكتبات:** - Java: مكتبة Bouncycastle الإصدار 1.79 وما بعده تدعم جميع متغيرات ML-KEM (آلية تغليف المفاتيح القائمة على الشبكات النمطية) ودوال SHA3/SHAKE - C++: يتضمن OpenSSL 3.5 وما بعده دعماً كاملاً لـ ML-KEM (صدر في أبريل 2025) - Go: تتوفر عدة مكتبات لتنفيذ ML-KEM وSHA3

## المواصفات

### البُنى المشتركة

راجِع [مواصفة البنى المشتركة](/docs/specs/common-structures/) للاطلاع على أطوال المفاتيح والمعرّفات.

### أنماط المصافحة

تستخدم عمليات المصافحة أنماط المصافحة الخاصة بـ [Noise Protocol Framework](https://noiseprotocol.org/noise.html) مع تعديلات خاصة بـ I2P لتحقيق أمان هجين لما بعد الكم.

يُستخدَم التعيين التالي للأحرف:

- **e** = مفتاح مؤقّت لمرة واحدة (X25519)
- **s** = مفتاح ثابت
- **p** = حمولة الرسالة
- **e1** = مفتاح PQ (ما بعد الكم) مؤقّت لمرة واحدة، مُرسَل من Alice إلى Bob (رمز خاص بـ I2P)
- **ekem1** = النص المُشفَّر لـ KEM (آلية تغليف المفاتيح)، مُرسَل من Bob إلى Alice (رمز خاص بـ I2P)

**ملاحظة مهمة:** أسماء الأنماط "IKhfs" و"IKhfselg2" والرموز "e1" و"ekem1" هي تعديلات خاصة بـ I2P غير موثقة في مواصفة إطار عمل بروتوكول Noise الرسمية. تمثل هذه تعريفات مخصصة لدمج ML-KEM (آلية تغليف المفاتيح - KEM - ما بعد الكم) ضمن نمط IK في Noise. وبينما يُعترف على نطاق واسع بالنهج الهجين X25519 + ML-KEM في أبحاث التشفير ما بعد الكم وبروتوكولات أخرى، فإن التسميات المحددة المستخدمة هنا خاصة بـ I2P.

تُطبَّق التعديلات التالية على IK لتحقيق سرية أمامية هجينة:

```
Standard IK:              I2P IKhfs (Hybrid):
<- s                      <- s
...                       ...
-> e, es, s, ss, p        -> e, es, e1, s, ss, p
<- e, ee, se, p           <- e, ee, ekem1, se, p
<- p                      <- p
p ->                      p ->

Note: e1 and ekem1 are encrypted within ChaCha20-Poly1305 AEAD blocks.
Note: e1 (ML-KEM public key) and ekem1 (ML-KEM ciphertext) have different sizes.
```
يُعرَّف نمط **e1** كما يلي:

```
For Alice (sender):
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++
MixHash(ciphertext)

For Bob (receiver):
// DecryptAndHash(ciphertext)
encap_key = DECRYPT(k, n, ciphertext, ad)
n++
MixHash(ciphertext)
```
يُعرَّف النمط **ekem1** (مصطلح تقني) كما يلي:

```
For Bob (receiver of encap_key):
(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
MixHash(ciphertext)

// MixKey
MixKey(kem_shared_key)

For Alice (sender of encap_key):
// DecryptAndHash(ciphertext)
kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
MixHash(ciphertext)

// MixKey
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
MixKey(kem_shared_key)
```
### العمليات المعرّفة لـ ML-KEM

نعرّف الدوال التالية المقابلة للّبنات الأساسية التشفيرية كما هو محدد في [FIPS203](https://csrc.nist.gov/pubs/fips/203/final).

**(encap_key, decap_key) = PQ_KEYGEN()** : تُنشئ أليس مفاتيح التغليف وفكّ التغليف. يُرسَل مفتاح التغليف في رسالة NS. أحجام المفاتيح:   - ML-KEM-512: encap_key = 800 بايت، decap_key = 1632 بايت   - ML-KEM-768: encap_key = 1184 بايت، decap_key = 2400 بايت   - ML-KEM-1024: encap_key = 1568 بايت، decap_key = 3168 بايت

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)** : يحسب بوب النص المشفّر والمفتاح المشترك باستخدام مفتاح التغليف المستلَم في رسالة NS. يُرسَل النص المشفّر في رسالة NSR. أحجام النص المشفّر:   - ML-KEM-512: 768 بايت   - ML-KEM-768: 1088 بايت   - ML-KEM-1024: 1568 بايت

يبلغ طول kem_shared_key دائمًا **32 بايت** في جميع المتغيرات الثلاثة.

**kem_shared_key = DECAPS(ciphertext, decap_key)** : تحسب أليس المفتاح المشترك باستخدام ciphertext المستلَم في رسالة NSR. يبلغ طول kem_shared_key دائمًا **32 بايت**.

**مهم:** كلٌ من encap_key وciphertext يُشفَّران داخل كُتَل ChaCha20-Poly1305 (خوارزمية AEAD للتشفير والمصادقة) في رسالتي المصافحة الخاصة بـ Noise (بروتوكول للتبادل الآمن) 1 و2. سيتم فكّ تشفيرهما كجزء من عملية المصافحة.

يُدمج kem_shared_key ضمن مفتاح السلسلة باستخدام MixKey(). راجع التفاصيل أدناه.

### KDF (دالة اشتقاق المفاتيح) لمصافحة Noise

#### نظرة عامة

تجمع المصافحة الهجينة بين X25519 ECDH الكلاسيكي وML-KEM ما بعد الكم. تحتوي الرسالة الأولى، من Alice إلى Bob، على e1 (مفتاح تغليف ML-KEM) قبل حمولة الرسالة. يُعامَل ذلك كمواد مفتاحية إضافية؛ استدعِ EncryptAndHash() عليه (بصفتك Alice) أو DecryptAndHash() (بصفتك Bob). ثم عالِج حمولة الرسالة كالمعتاد.

الرسالة الثانية، من Bob إلى Alice، تحتوي على ekem1 (ML-KEM ciphertext، نص مُشفّر بخوارزمية ML-KEM) قبل حمولة الرسالة. يُعامَل هذا كمادة مفتاحية إضافية؛ استدعِ EncryptAndHash() عليها (بوصفك Bob) أو DecryptAndHash() (بوصفك Alice). ثم احسب kem_shared_key واستدعِ MixKey(kem_shared_key). بعد ذلك عالِج حمولة الرسالة كالمعتاد.

#### معرّفات Noise (إطار عمل بروتوكولي للتشفير)

هذه هي سلاسل تهيئة Noise (إطار عمل بروتوكول لتبادل المفاتيح الآمن) (الخاصة بـ I2P):

- `Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256`

#### دالة اشتقاق المفاتيح لأليس لرسالة NS

بعد نمط الرسالة 'es' وقبل نمط الرسالة 's' أضِف:

```
This is the "e1" message pattern:
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++

// MixHash(ciphertext)
h = SHA256(h || ciphertext)

End of "e1" message pattern.

NOTE: For the next section (payload for XK or static key for IK),
the keydata and chain key remain the same,
and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF (دالة اشتقاق المفاتيح) الخاصة بـ Bob لرسالة NS

بعد نمط الرسالة 'es' وقبل نمط الرسالة 's'، أضف:

```
This is the "e1" message pattern:

// DecryptAndHash(encap_key_section)
// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
encap_key = DECRYPT(k, n, encap_key_section, ad)
n++

// MixHash(encap_key_section)
h = SHA256(h || encap_key_section)

End of "e1" message pattern.

NOTE: For the next section (payload for XK or static key for IK),
the keydata and chain key remain the same,
and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF (دالة اشتقاق المفاتيح) الخاصة ببوب لرسالة NSR

بعد نمط الرسالة 'ee' وقبل نمط الرسالة 'se'، أضف:

```
This is the "ekem1" message pattern:

(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

// MixHash(ciphertext)
h = SHA256(h || ciphertext)

// MixKey(kem_shared_key)
keydata = HKDF(chainKey, kem_shared_key, "", 64)
chainKey = keydata[0:31]

End of "ekem1" message pattern.
```
#### خوارزمية اشتقاق المفاتيح الخاصة بأليس لرسالة NSR

بعد نمط الرسالة 'ee' وقبل نمط الرسالة 'ss'، أضف:

```
This is the "ekem1" message pattern:

// DecryptAndHash(kem_ciphertext_section)
// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

// MixHash(kem_ciphertext_section)
h = SHA256(h || kem_ciphertext_section)

// MixKey(kem_shared_key)
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
keydata = HKDF(chainKey, kem_shared_key, "", 64)
chainKey = keydata[0:31]

End of "ekem1" message pattern.
```
#### دالة اشتقاق المفاتيح (KDF) لـ split()

تبقى الدالة split() دون تغيير عن المواصفات القياسية لـ ECIES (مخطط تشفير متكامل باستخدام المنحنيات الإهليلجية). بعد إتمام المصافحة:

```
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]
k_ba = keydata[32:63]
```
هذه هي مفاتيح الجلسة ثنائية الاتجاه للتواصل المستمر.

### تنسيق الرسالة

#### تنسيق NS (New Session - جلسة جديدة)

**التغييرات:** يحتوي ratchet (آلية ترقية المفاتيح تدريجياً) الحالي على المفتاح الثابت في قسم ChaCha20-Poly1305 الأول وعلى الحمولة في القسم الثاني. مع ML-KEM، أصبح هناك الآن ثلاثة أقسام. يحتوي القسم الأول على المفتاح العام لـ ML-KEM المُشفَّر (encap_key). يحتوي القسم الثاني على المفتاح الثابت. يحتوي القسم الثالث على الحمولة.

**أحجام الرسائل:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ key len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">912+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">880+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1296+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1264+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1680+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1648+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
**ملاحظة:** يجب أن تحتوي الحمولة على كتلة DateTime (حد أدنى 7 بايت: نوع بطول 1 بايت، حجم بطول 2 بايت، طابع زمني بطول 4 بايت). يمكن حساب أحجام NS الدنيا وفقاً لذلك. وعليه، فإن الحد الأدنى العملي لحجم NS هو 103 بايت لـ X25519 ويتراوح من 919 إلى 1687 بايت للمتغيرات الهجينة.

تُعزى زيادات الحجم بمقادير 816، و1200، و1584 بايت في المتغيرات الثلاثة لـ ML-KEM إلى المفتاح العام لـ ML-KEM إضافةً إلى Poly1305 MAC (رمز تحقق الرسالة) بحجم 16 بايت للتشفير الموثَّق.

#### تنسيق NSR (New Session Reply - استجابة الجلسة الجديدة)

**التغييرات:** ratchet (آلية تدوير المفاتيح تدريجياً) الحالي يحتوي على حمولة فارغة في القسم الأول من ChaCha20-Poly1305 (خوارزمية تشفير ومصادقة)، وتكون الحمولة في القسم الثاني. مع ML-KEM (آلية تغليف مفاتيح قائمة على شبكات معيارية)، أصبح هناك الآن ثلاثة أقسام. يحتوي القسم الأول على نص ML-KEM المُشفّر. يحتوي القسم الثاني على حمولة فارغة. يحتوي القسم الثالث على الحمولة.

**أحجام الرسائل:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ ct len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">72+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">856+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">824+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">784+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1176+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1144+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1104+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1656+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1624+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1584+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
تُعزى زيادات الحجم البالغة 784 و1104 و1584 بايت في المتغيرات الثلاثة لـ ML-KEM إلى نص ML-KEM المُعمّى، إضافةً إلى Poly1305 MAC بحجم 16 بايت للتشفير الموثّق.

## تحليل العبء الإضافي

### تبادل المفاتيح

الكلفة الإضافية للتشفير الهجين كبيرة مقارنةً بـ X25519 فقط:

- **MLKEM512_X25519**: زيادة في حجم رسالة المصافحة بنحو 9-12x (NS: 9.5x, NSR: 11.9x)
- **MLKEM768_X25519**: زيادة في حجم رسالة المصافحة بنحو 13-16x (NS: 13.5x, NSR: 16.3x)
- **MLKEM1024_X25519**: زيادة في حجم رسالة المصافحة بنحو 17-23x (NS: 17.5x, NSR: 23x)

هذه الزيادة في العبء مقبولة مقابل فوائد الأمن ما بعد الكم المضافة. تختلف معاملات الضرب بحسب نوع الرسالة لأن أحجام الرسائل الأساسية تختلف (الحد الأدنى لـ NS: 96 بايت، ولـ NSR: 72 بايت).

### اعتبارات عرض النطاق الترددي

لعملية إنشاء جلسة نموذجية بحمولات دنيا: - X25519 فقط: ~200 بايت إجمالاً (NS + NSR) - MLKEM512_X25519: ~1,800 بايت إجمالاً (زيادة بمقدار 9 أضعاف) - MLKEM768_X25519: ~2,500 بايت إجمالاً (زيادة بمقدار 12.5 ضعفاً) - MLKEM1024_X25519: ~3,400 بايت إجمالاً (زيادة بمقدار 17 ضعفاً)

بعد إنشاء الجلسة، يستخدم تشفير الرسائل المستمر نفس تنسيق نقل البيانات كما في الجلسات المعتمدة على X25519 فقط، لذا لا يوجد عبء إضافي للرسائل اللاحقة.

## تحليل الأمان

### المصافحات

توفر المصافحة الهجينة كلاً من الأمان التقليدي (X25519) وأمان ما بعد الكم (ML-KEM). يجب على المهاجم كسر **كلا** من ECDH التقليدي وKEM لما بعد الكم للمساس بمفاتيح الجلسة.

يوفّر هذا: - **الأمان الحالي**: يوفّر X25519 ECDH أمانًا ضد المهاجمين التقليديين (مستوى أمان 128-بت) - **الأمان المستقبلي**: يوفّر ML-KEM أمانًا ضد المهاجمين الكمّيين (يختلف باختلاف مجموعة المعلمات) - **الأمان الهجين**: يجب كسر كلاهما لاختراق الجلسة (مستوى الأمان = الأعلى بين المكوّنين)

### مستويات الأمان

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variant</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NIST Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Classical Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Hybrid Security</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-128 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-192 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
  </tbody>
</table>
**ملاحظة:** مستوى الأمان الهجين محدود بأضعف المكوّنين. في جميع الحالات، توفّر X25519 (منحنى بيضاوي للاتفاق على المفاتيح) أمانًا تقليديًا بقوة 128-بت. إذا توفر حاسوب كمي ذو صلة بالتشفير، فسيعتمد مستوى الأمان على مجموعة معلمات ML-KEM (آلية تغليف مفاتيح لما بعد الكم) المختارة.

### السرية الأمامية

النهج الهجين يحافظ على خصائص السرية المستقبلية. يتم اشتقاق مفاتيح الجلسة من كلٍ من تبادل مفاتيح X25519 المؤقت وتبادل مفاتيح ML-KEM المؤقت. إذا تم إتلاف المفاتيح الخاصة المؤقتة لـ X25519 أو ML-KEM بعد إتمام المصافحة، فلن يكون بالإمكان فك تشفير الجلسات السابقة حتى لو تم اختراق المفاتيح الثابتة طويلة الأمد.

يوفّر نمط IK سرية أمامية كاملة (Noise Confidentiality level 5: مستوى السرية في بروتوكول Noise، المستوى 5) بعد إرسال الرسالة الثانية (NSR).

## تفضيلات النوع

يجب أن تدعم التنفيذات عدة أنواع هجينة وأن تتفاوض على أقوى متغيّر مدعوم بشكل متبادل. يجب أن يكون ترتيب التفضيل:

1. **MLKEM768_X25519** (مجموعة اتفاق مفاتيح هجينة تجمع MLKEM (تشفير بعد-كمومي قائم على الشبكات) وX25519 (خوارزمية منحنى بيضوي لتبادل المفاتيح)) (النوع 6) - الافتراضي الموصى به، أفضل توازن بين الأمان والأداء
2. **MLKEM1024_X25519** (النوع 7) - أعلى مستوى أمان للتطبيقات الحساسة
3. **MLKEM512_X25519** (النوع 5) - خط أساس للأمان بعد-الكمومي للسيناريوهات ذات الموارد المحدودة
4. **X25519** (النوع 4) - تقليدي فقط، حلّ احتياطي للتوافق

**التبرير:** يُنصح باعتماد MLKEM768_X25519 كالإعداد الافتراضي لأنه يوفّر أمان NIST Category 3 (المعهد الوطني للمعايير والتقنية) (ما يعادل AES-192)، وهو ما يُعد حماية كافية ضد الحواسيب الكمّية مع الحفاظ على أحجام رسائل معقولة. يوفّر MLKEM1024_X25519 مستوى أمان أعلى، ولكن مع عبءٍ إضافي أعلى بكثير.

## ملاحظات التنفيذ

### دعم المكتبات

- **Java**: تدعم مكتبة Bouncycastle الإصدار 1.79 (أغسطس 2024) وما بعده جميع متغيّرات ML-KEM (آلية تغليف المفاتيح القائمة على الشبكات المعيارية) المطلوبة ووظائف SHA3/SHAKE. استخدم `org.bouncycastle.pqc.crypto.mlkem.MLKEMEngine` للامتثال لمعيار FIPS 203.
- **C++**: يتضمن OpenSSL 3.5 (أبريل 2025) وما بعده دعم ML-KEM عبر واجهة EVP_KEM. هذا إصدار دعم طويل الأجل (LTS) تتم صيانته حتى أبريل 2030.
- **Go**: تتوفر عدة مكتبات من جهات خارجية لدعم ML-KEM وSHA3، بما في ذلك مكتبة CIRCL من Cloudflare.

### استراتيجية الترحيل

ينبغي على التنفيذات: 1. دعم كلٍ من X25519-only (خوارزمية تبادل مفاتيح على منحنى بيضوي) والمتغيرات الهجينة لـ ML-KEM (خوارزمية تبادل مفاتيح مغلّفة معيارية ما بعد-كمومية) خلال الفترة الانتقالية 2. تفضيل المتغيرات الهجينة عندما يدعمها كلا الطرفين 3. الحفاظ على خيار الرجوع إلى X25519-only لأغراض التوافق الخلفي 4. مراعاة قيود عرض النطاق الترددي للشبكة عند اختيار المتغير الافتراضي

### Tunnels المشتركة

قد تؤثر زيادة أحجام الرسائل في الاستخدام المشترك للـ tunnel. ينبغي على عمليات التنفيذ أن تراعي: - تجميع المصافحات قدر الإمكان لتخفيف الكلفة الإضافية - استخدام أزمنة انتهاء أقصر للجلسات الهجينة لتقليل الحالة المخزّنة - مراقبة استخدام النطاق الترددي وضبط المعلمات وفقاً لذلك - تطبيق ضبط الازدحام لحركة إنشاء الجلسات

### اعتبارات حجم الجلسة الجديدة

نظرًا لكون رسائل المصافحة أكبر حجمًا، قد تحتاج عمليات التنفيذ إلى: - زيادة أحجام المخازن المؤقتة لتفاوض الجلسة (الحد الأدنى الموصى به 4KB) - ضبط قيم المهلة للاتصالات الأبطأ (مراعاة أن الرسائل أكبر بحوالي ~3-17x) - النظر في ضغط بيانات الحمولة في رسائل NS/NSR - تنفيذ آلية التعامل مع التجزئة إذا تطلبت ذلك طبقة النقل

### الاختبار والتحقق

يجب على التنفيذات التحقق مما يلي: - صحة توليد المفاتيح بـ ML-KEM (مخطط تبادل مفاتيح قائم على الشبكيات ومقاوم للحوسبة الكمّية)، وعمليتي التغليف وفك التغليف - دمج kem_shared_key بشكل صحيح ضمن Noise KDF (وظيفة اشتقاق المفاتيح في إطار Noise) - تطابق حسابات حجم الرسائل مع المواصفة - قابلية التشغيل البيني مع تنفيذات أخرى لـ I2P router - سلوك التراجع عند عدم توفر ML-KEM

متجهات الاختبار لعمليات ML-KEM (آلية تغليف المفاتيح القائمة على الشبكات المعيارية) متاحة في NIST [برنامج التحقق من صحة خوارزميات التشفير](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program).

## توافق الإصدارات

**ترقيم إصدارات I2P:** يحافظ I2P على رقمَي إصدار متوازيين: - **إصدار الـ Router**: بصيغة 2.x.x (مثلًا، 2.10.0 صدر في سبتمبر 2025) - **إصدار واجهة برمجة التطبيقات/البروتوكول**: بصيغة 0.9.x (مثلًا، 0.9.67 يتوافق مع router 2.10.0)

تُشير هذه المواصفة إلى إصدار البروتوكول 0.9.67، الذي يتوافق مع إصدار router 2.10.0 وما بعده.

**مصفوفة التوافق:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.58.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (512/768/1024)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deployed September 2025</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67 / 2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not yet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Planned for future release</td>
    </tr>
  </tbody>
</table>
## المراجع

- **[ECIES]**: [مواصفة ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/)
- **[Prop169]**: [المقترح 169: التشفير ما بعد الكم](/proposals/169-pq-crypto/)
- **[FIPS203]**: [NIST FIPS 203 - معيار ML-KEM](https://csrc.nist.gov/pubs/fips/203/final)
- **[FIPS202]**: [NIST FIPS 202 - معيار SHA-3](https://csrc.nist.gov/pubs/fips/202/final)
- **[Noise]**: [إطار عمل بروتوكول Noise](https://noiseprotocol.org/noise.html)
- **[COMMON]**: [مواصفة الهياكل المشتركة](/docs/specs/common-structures/)
- **[RFC7539]**: [RFC 7539 - ChaCha20 و Poly1305](https://www.rfc-editor.org/rfc/rfc7539)
- **[RFC5869]**: [RFC 5869 - HKDF](https://www.rfc-editor.org/rfc/rfc5869)
- **[OpenSSL]**: [وثائق OpenSSL 3.5 لـ ML-KEM](https://docs.openssl.org/3.5/man7/EVP_KEM-ML-KEM/)
- **[Bouncycastle]**: [مكتبة Bouncycastle للتشفير بلغة Java](https://www.bouncycastle.org/)

---
