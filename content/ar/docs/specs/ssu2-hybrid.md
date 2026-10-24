---
title: "PQ Hybrid SSU2"
description: "النسخة الهجينة المقاومة للحوسبة الكمية من بروتوكول النقل SSU2 باستخدام ML-KEM"
slug: "ssu2-hybrid"
lastupdated: "2026-10"
category: "وسائل النقل"
accurateFor: "0.9.71"
---

### الحالة

النسخة التجريبية الثاني 2026، الإصدار الرسمي الربع الثالث 2026

## نظرة عامة

هذا هو البديل الهجين ما بعد الكمي (Post-Quantum) لبروتوكول النقل SSU2، كما تم تصميمه في الاقتراح 169. راجع ذلك الاقتراح للحصول على خلفية إضافية.

يُعرَّف PQ Hybrid SSU2 فقط على نفس العنوان والمنفذ الخاصين بـ SSU2 القياسي. لا يُسمح بالتشغيل على منفذ مختلف، أو بدون دعم SSU2 القياسي، ولن يُسمح بذلك لعدة سنوات قادمة، حين يتم إيقاف SSU2 القياسي رسمياً.

تُوثّق هذه المواصفة فقط التغييرات المطلوبة على معيار SSU2 القياسي لدعم PQ Hybrid. راجع مواصفة SSU2 للاطلاع على تفاصيل التنفيذ الأساسية.

## التصميم

نحن ندعم معيار NIST FIPS 203 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) الذي يستند إلى خوارزمية CRYSTALS-Kyber، لكنه غير متوافق معها.

### تبادل المفاتيح

يوفر PQ KEM مفاتيح مؤقتة (ephemeral) فحسب، ولا يدعم مباشرةً عمليات المصافحة القائمة على المفاتيح الثابتة مثل Noise XK و IK. أنواع التشفير هي ذاتها المستخدمة في PQ Hybrid Ratchet، وهي محددة في وثيقة الهياكل المشتركة [/docs/specs/common-structures/](/docs/specs/common-structures/)، وكما هو الحال في [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)، لا تُعرَّف الأنواع الهجينة (Hybrid) إلا بالاقتران مع X25519.

أنواع التشفير هي:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">SSU2 Version</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
</table>
### التوليفات القانونية

تُشار أنواع التشفير الجديدة في RouterAddresses. سيستمر نوع التشفير في شهادة المفتاح (key certificate) في كونه من النوع 4.

## المواصفات

### أنماط المصافحة

تستخدم عمليات المصافحة (Handshakes) أنماط المصافحة الخاصة بـ [Noise Protocol](https://noiseprotocol.org/noise.html).

يُستخدم تعيين الحروف التالي:

- e = مفتاح مؤقت أحادي الاستخدام (one-time ephemeral key)
- s = مفتاح ثابت (static key)
- p = حمولة الرسالة (message payload)
- e1 = مفتاح PQ مؤقت أحادي الاستخدام، يُرسل من Alice إلى Bob
- ekem1 = النص المشفر KEM (KEM ciphertext)، يُرسل من Bob إلى Alice

التعديلات التالية على XK وIK لضمان السرية الأمامية الهجينة (hfs) مُحددة كما هو موضح في [مواصفات Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 5:

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
يُعرَّف نمط e1 على النحو التالي، كما هو محدد في [مواصفات Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 4:

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
يُعرَّف نمط ekem1 على النحو التالي، كما هو محدد في [مواصفات Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 4:

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### دالة اشتقاق مفتاح مصافحة Noise

#### نظرة عامة

يُعرَّف المصافحة الهجينة في [مواصفات Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). تحتوي الرسالة الأولى، المرسلة من Alice إلى Bob، على e1، وهو مفتاح التغليف (encapsulation key)، قبل حمولة الرسالة. يُعامَل هذا المفتاح باعتباره مفتاحاً ثابتاً إضافياً؛ استدعِ EncryptAndHash() عليه (بوصفك Alice) أو DecryptAndHash() (بوصفك Bob). ثم قم بمعالجة حمولة الرسالة كالمعتاد.

الرسالة الثانية، من Bob إلى Alice، تحتوي على ekem1، وهو النص المشفر (ciphertext)، قبل حمولة الرسالة. يُعامَل هذا كمفتاح ثابت إضافي؛ قم باستدعاء EncryptAndHash() عليه (بوصفك Bob) أو DecryptAndHash() (بوصفك Alice). ثم احسب kem_shared_key واستدعِ MixKey(kem_shared_key). بعد ذلك، قم بمعالجة حمولة الرسالة كالمعتاد.

#### عمليات ML-KEM المحددة

نُعرِّف الدوال التالية المقابلة للوحدات البنائية التشفيرية المستخدمة كما هو محدد في [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

لاحظ أن كلاً من encap_key والنص المشفر (ciphertext) مشفّران داخل كتل ChaCha/Poly في رسائل مصافحة Noise رقم 1 و2. وسيتم فكّ تشفيرهما كجزء من عملية المصافحة.

يتم دمج kem_shared_key في مفتاح السلسلة باستخدام MixHash(). راجع القسم أدناه للاطلاع على التفاصيل.

#### دالة اشتقاق المفاتيح (KDF) لأليس للرسالة 1

بعد نمط رسالة 'es' وقبل الحمولة، أضف:

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
#### اشتقاق المفتاح (KDF) لـ Bob في الرسالة 1

بعد نمط رسالة 'es' وقبل الحمولة، أضف:

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
#### دالة اشتقاق المفاتيح (KDF) الخاصة ببوب للرسالة 2

بالنسبة لـ XK: بعد نمط رسالة 'ee' وقبل الحمولة، أضف:

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### دالة اشتقاق المفاتيح (KDF) لأليس للرسالة 2

بعد نمط رسالة 'ee'، أضف:

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### دالة اشتقاق المفاتيح (KDF) للرسالة 3

unchanged

#### دالة اشتقاق المفاتيح (KDF) لعملية split()

unchanged

### تفاصيل المصافحة

#### معرّفات Noise

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

لاحظ أن MLKEM-1024 غير مدعوم في SSU2، إذ إن المفاتيح كبيرة جداً بحيث لا تتناسب مع حزمة البيانات (datagram) القياسية البالغة 1500 بايت.

#### رأس طويل

الترويسة الطويلة (Long Header) حجمها 32 بايت. تُستخدم قبل إنشاء الجلسة، في رسائل طلب الرمز (Token Request) وطلب الجلسة (SessionRequest) وإنشاء الجلسة (SessionCreated) وإعادة المحاولة (Retry). كما تُستخدم أيضاً في رسائل اختبار النظير (Peer Test) وثقب المسبار (Hole Punch) الخارجة عن نطاق الجلسة.

في الرسائل التالية، اضبط حقل ver (الإصدار) في الترويسة الطويلة على 3 أو 4، للإشارة إلى MLKEM-512 أو MLKEM-768.

- (0) طلب الجلسة (Session Request)
- (1) تم إنشاء الجلسة (Session Created)
- (9) إعادة المحاولة (Retry)
- (10) طلب الرمز (Token Request)
- (11) اختراق الجدار (Hole Punch)

في الرسائل التالية، اضبط حقل ver (الإصدار) في الترويسة الطويلة على القيمة 2 كالمعتاد، حتى في حال دعم MLKEM-512 أو MLKEM-768. يجوز للتطبيقات أيضاً ضبط هذه القيمة على 3 أو 4 إذا كان الطرف الآخر يدعم ذلك، غير أن هذا ليس إلزامياً. ينبغي للتطبيقات قبول أي قيمة تتراوح بين 2 و4.

- (7) اختبار النظير (رسائل خارج الجلسة من 5 إلى 7)

النقاش: قد لا يكون تعيين حقل الإصدار إلى 3 أو 4 ضرورياً بشكل صارم لجميع أنواع الرسائل، إلا أن القيام بذلك يُساعد في الكشف المبكر عن الإخفاقات المتعلقة باتصالات ما بعد الكم (post-quantum) غير المدعومة. يجب أن تحمل رسائل طلب الرمز المميز وإعادة المحاولة (النوعان 9 و10) الإصدارين 3/4 للاتساق. قد لا تستوجب رسائل Hole Punch (النوع 11) هذه المعالجة، غير أننا سنتبع النمط ذاته لتحقيق التوحيد. أما رسائل Peer Test (النوع 7) فهي خارج نطاق الجلسة ولا تشير إلى نية بدء جلسة جديدة.

- طلب التتابع (Relay Request)
- استجابة التتابع (Relay Response)
- مقدمة التتابع (Relay Intro)
- اختبار النظير (Peer Test)

قبل تشفير الترويسة:

قبل تشفير الرأس:

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### رأس قصير

unchanged

#### طلب الجلسة SessionRequest (النوع 0)

التغييرات: يحتوي SSU2 الحالي على بيانات الكتلة فقط في قسم ChaCha. مع ML-KEM، سيحتوي قسم ChaCha أيضاً على المفتاح العام المشفّر للتشفير ما بعد الكمومي (PQ).

تغيير KDF للحماية من الانتحال: لمعالجة المشكلات المطروحة في المقترح 165 [Prop165]_، ولكن بحل مختلف، نقوم بتعديل KDF لطلب الجلسة (Session Request). يقتصر هذا التعديل على جلسات PQ فقط. يبقى KDF لجلسات غير PQ دون تغيير.

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
المحتويات الخام:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
البيانات غير المشفرة (علامة مصادقة Poly1305 غير مُدرجة):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
الأحجام، باستثناء التحميل الزائد لبروتوكول IP:

| النوع | رمز النوع | طول X | طول الرسالة 1 | طول الرسالة 1 المشفرة | طول الرسالة 1 المفككة | طول مفتاح PQ | طول pl |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
ملاحظة: رموز الأنواع مخصصة للاستخدام الداخلي فقط. ستظل الـ routers من النوع 4، وسيُشار إلى دعمها في عناوين الـ router.

الحد الأدنى لـ MTU لـ MLKEM768_X25519: 1318 لـ IPv4 و1338 لـ IPv6. انظر أدناه.

التغييرات: يحتوي SSU2 الحالي فقط على الحمولة في قسم واحد من نوع ChaCha. مع ML-KEM، سيكون هناك قسم جديد من نوع ChaCha قبل الحمولة، ويحتوي على النص المشفر الكمي (PQ ciphertext) المشفر.

#### SessionCreated (النوع 1)

التغييرات: يحتوي SSU2 الحالي فقط على الحمولة في قسم ChaCha واحد. مع ML-KEM، سيكون هناك قسم ChaCha جديد قبل الحمولة، يحتوي على نص مشفر كمي (PQ) مشفر.

المحتويات الخام:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
البيانات غير المشفرة (علامة مصادقة Poly1305 غير مُدرجة):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
الأحجام، باستثناء التحميل الزائد لبروتوكول IP:

| النوع | رمز النوع | طول Y | طول Msg 2 | طول Msg 2 المشفّر | طول Msg 2 بعد فك التشفير | طول PQ CT | طول pl |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | غير متاح | كبير جدًا | | | | |
ملاحظة: رموز الأنواع مخصصة للاستخدام الداخلي فقط. ستظل الـ routers من النوع 4، وسيُشار إلى دعمها في عناوين الـ router.

الحد الأدنى لـ MTU لـ MLKEM768_X25519: 1318 لـ IPv4 و1338 لـ IPv6. انظر أدناه.

الحجم الأقصى: لا تمتلك آليس حتى الآن معلومات الموجه الخاصة ببوب ولا تعرف الحد الأقصى لوحدة النقل (MTU) المنشور لديه. بالنسبة لهذه الرسالة، استخدم حدًا أقصى مؤقتًا لوحدة النقل (MTU) على النحو التالي: بالنسبة لـ MLKEM512_X25519، استخدم الحد الأقصى بين 1280 أو حجم SessionRequest المستلم كقيمة لـ MTU. وبالنسبة لـ MLKEM768_X25519، استخدم الحد الأقصى بين (1318 للبروتوكول IPv4 أو 1338 للبروتوكول IPv6) أو حجم SessionRequest المستلم كقيمة لـ MTU. إن حجم الرأس في SessionCreated أصغر من حجم الرأس في SessionRequest، لأن النص المشفر باستخدام MLKEM أصغر من المفتاح العام لـ MLKEM. وهذا يسمح بمجموعة من أحجام الحشو في SessionCreated حتى لو كان هناك حشو ضئيل أو معدوم في SessionRequest.

#### SessionConfirmed (النوع 2)

unchanged

#### دالة اشتقاق المفاتيح (KDF) لمرحلة البيانات

unchanged

#### التتابع واختبار النظير

تحتوي الكتل التالية على حقول الإصدار. ستبقى عند الإصدار 2 (للحفاظ على التوافق مع Bob غير-PQ)، ولن تتغير إلى الإصدار 3/4 في حالة PQ.

* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)

#### العناوين المنشورة

في جميع الحالات، استخدم اسم نقل SSU2 كالمعتاد. لا يتم دعم MLKEM-1024.

استخدم نفس العنوان/المنفذ كما في الحالة غير-PQ وغير المحجوبة بجدار الحماية. يُدعم أحد متغيري PQ أو كلاهما. في عنوان router، انشر v=2 (كالمعتاد) والمعامل الجديد pq=[3|4|3,4|4,3] للإشارة إلى MLKEM 512/768/كليهما. يجب على الـ routers التي تمتلك MTU أقل من الحد الأدنى المحدد أدناه ألا تنشر معامل "pq" يحتوي على "4". انشر 4,3 للإشارة إلى تفضيل MLKEM-768 أو 3,4 للإشارة إلى تفضيل MLKEM-512. الإصدار الفعلي يعود إلى المُبادر، وقد لا يُراعى التفضيل. يجب على الـ routers التي تمتلك MTU أقل من الحد الأدنى المحدد أدناه ألا تتصل باستخدام MLKEM768. ستتجاهل الـ routers القديمة معامل pq وتتصل بدون PQ كالمعتاد.

العنوان/المنفذ المختلف كغير PQ، أو PQ فقط، غير المحجوب بجدار ناري غير مدعوم. لن يتم تنفيذ هذا حتى يتم تعطيل SSU2 غير PQ، بعد عدة سنوات من الآن. عند تعطيل غير PQ، يتم دعم أحد متغيري PQ أو كليهما. في عنوان router، قم بنشر v=[3|4|3,4|4,3] للإشارة إلى MLKEM 512/768/كليهما. ستتحقق الrouters الأقدم من معامل v وتتخطى هذا العنوان باعتباره غير مدعوم.

العناوين المحجوبة بجدار الحماية (لا يتم نشر عنوان IP): في عنوان الـ router، يتم نشر `v=2` (كالمعتاد). يجب نشر المعامل `pq` في العناوين المحجوبة بجدار الحماية، لدعم عملية الـ relay.

يمكن لـ Alice الاتصال بـ Bob الذي يدعم التشفير الكمي (PQ) باستخدام المتغير الكمي الذي ينشره Bob، بغض النظر عما إذا كانت Alice تُعلن دعمها للتشفير الكمي في معلومات router الخاصة بها، أو ما إذا كانت تُعلن عن نفس المتغير.

#### MTU

توخَّ الحذر حتى لا تتجاوز الـ MTU (الحد الأقصى لحجم وحدة النقل) عند استخدام MLKEM768. الحد الأدنى للـ MTU الخاص بـ MLKEM768_X25519 هو 1318 لـ IPv4 و1338 لـ IPv6 (بافتراض حمولة دنيا مقدارها 10 بايت مع كتلة DateTime وكتلة Padding أو RelayTagRequest). الحد الأدنى للـ MTU في SSU2 بشكل عام هو 1280، لذلك قد لا يستخدم جميع الأقران MLKEM768. لا تنشر أو تستخدم MLKEM768 إذا كان الـ MTU الفعلي أقل من الحد الأدنى، سواء محليًا أو كما يُعلن عنه من قِبَل النظير. احرص على عدم تضمين حجم الحشو (padding) بما يؤدي إلى تجاوز الرسالة الأولى أو الثانية للـ MTU المحلي أو البعيد.

## تحليل الحمل الزائد (Overhead)

### تبادل المفاتيح

زيادة الحجم (بالبايت):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (Msg 1)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (Msg 2)</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+784</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1104</td>
</tr>
</table>
## تحليل الأمان

يمكن الاطلاع على ملخص فئات الأمان الخاصة بـ NIST في الشريحة 10 من [عرض NIST](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf). المعايير الأولية: يجب أن يكون الحد الأدنى لفئة أمان NIST لدينا هو 2 للبروتوكولات الهجينة، و3 للبروتوكولات الكمية فقط (PQ-only).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Category</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Secure As</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES128</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA256</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES192</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA384</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES256</td>
</tr>
</table>
### المصافحات (Handshakes)

هذه كلها بروتوكولات هجينة. يجب أن تُفضّل التطبيقات استخدام MLKEM768؛ إذ إن MLKEM512 ليس آمناً بما يكفي.

فئات أمان NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Algorithm</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Security Category</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
</table>
## ملاحظات التنفيذ

### دعم المكتبة

تدعم مكتبات Bouncycastle وBoringSSL وWolfSSL كلاً من MLKEM وMLDSA الآن. أما دعم OpenSSL فسيكون متاحاً في الإصدار 3.5 المقرر في 8 أبريل 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### تحديد حركة المرور الواردة

نقوم بتعيين البت الأكثر أهمية (MSB) للمفتاح المؤقت (key[31] & 0x80) في طلب الجلسة للإشارة إلى أن هذا اتصال هجين. يتيح لنا ذلك تشغيل كلٍّ من NTCP القياسي و NTCP الهجين على نفس المنفذ. يُدعم متغيّر هجين واحد فقط للاتصالات الواردة (inbound)، ويتم الإعلان عنه في عنوان router. على سبيل المثال: pq=3 أو pq=4.

## توافق الـ Router

### أسماء وسائل النقل

بصفتك أليس، لإنشاء اتصال PQ (كمّي ما بعد الكلاسيكي)، وقبل تطبيق التعتيم، قم بتعيين X[31] |= 0x80. هذا يجعل X مفتاحًا عامًا غير صالح لـ X25519. بعد التعتيم، سيقوم AES-CBC بتعشيئه عشوائيًا. سيكون البت الأكثر أهمية (MSB) من X عشوائيًا بعد التعتيم.

## المراجع

* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
