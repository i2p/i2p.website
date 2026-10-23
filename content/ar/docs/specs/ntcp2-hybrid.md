---
title: "PQ Hybrid NTCP2"
description: "المتغير الهجين لما بعد الكم من بروتوكول النقل NTCP2 باستخدام ML-KEM"
slug: "ntcp2-hybrid"
lastupdated: "2026-10"
category: "وسائل النقل"
accurateFor: "0.9.71"
---

### الحالة

بيتا الربع الأول 2026، الإصدار الربع الثاني 2026

## نظرة عامة

هذا هو المتغير الهجين لما بعد الحوسبة الكمية لبروتوكول النقل NTCP2، كما هو مصمم في الاقتراح 169. راجع ذلك الاقتراح للحصول على خلفية إضافية.

PQ Hybrid NTCP2 معرّف فقط على نفس العنوان والمنفذ المستخدم لـ NTCP2 العادي. التشغيل على منفذ مختلف، أو بدون دعم NTCP2 العادي، غير مسموح، ولن يكون كذلك لعدة سنوات، عندما يتم إهمال NTCP2 العادي.

هذه المواصفة توثق فقط التغييرات المطلوبة على NTCP2 المعياري لدعم PQ Hybrid. راجع مواصفة NTCP2 للحصول على تفاصيل التنفيذ الأساسية.

## التصميم

نحن ندعم معيار NIST FIPS 203 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) الذي يستند إلى خوارزمية CRYSTALS-Kyber، ولكن ليس متوافقًا معها.

### تبادل المفاتيح

يوفر PQ KEM مفاتيح مؤقتة فقط، ولا يدعم بشكل مباشر عمليات المصافحة ذات المفاتيح الثابتة مثل Noise XK وIK. أنواع التشفير هي نفسها المستخدمة في PQ Hybrid Ratchet وهي محددة في وثيقة الهياكل المشتركة [/docs/specs/common-structures/](/docs/specs/common-structures/)، كما هو موضح في [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)، الأنواع الهجينة محددة فقط بالتزامن مع X25519.

أنواع التشفير هي:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 Version</th>
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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
### التركيبات القانونية

يتم الإشارة إلى أنواع التشفير الجديدة في RouterAddresses. سيستمر نوع التشفير في شهادة المفتاح بكونه من النوع 4.

## المواصفات

### أنماط المصافحة

تستخدم المصافحات أنماط مصافحة [Noise Protocol](https://noiseprotocol.org/noise.html).

يتم استخدام تطابق الحروف التالي:

- e = مفتاح مؤقت لمرة واحدة
- s = مفتاح ثابت
- p = حمولة الرسالة
- e1 = مفتاح PQ مؤقت لمرة واحدة، يُرسل من Alice إلى Bob
- ekem1 = نص KEM المشفر، يُرسل من Bob إلى Alice

التعديلات التالية على XK و IK للسرية الأمامية المختلطة (hfs) محددة كما هو موضح في [مواصفات Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 5:

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
يتم تعريف نمط e1 كما يلي، كما هو محدد في [مواصفات Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 4:

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
يتم تعريف نمط ekem1 كما يلي، كما هو محدد في [مواصفات Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 4:

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
### دالة اشتقاق المفاتيح لمصافحة Noise

#### نظرة عامة

يتم تعريف المصافحة الهجينة في [مواصفات Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). الرسالة الأولى، من Alice إلى Bob، تحتوي على e1، مفتاح التغليف، قبل محتوى الرسالة. يتم التعامل مع هذا كمفتاح ثابت إضافي؛ استدعي EncryptAndHash() عليه (كـ Alice) أو DecryptAndHash() (كـ Bob). ثم عالج محتوى الرسالة كالمعتاد.

الرسالة الثانية، من Bob إلى Alice، تحتوي على ekem1، النص المشفر، قبل حمولة الرسالة. يتم التعامل مع هذا كمفتاح ثابت إضافي؛ استدعي EncryptAndHash() عليه (كـ Bob) أو DecryptAndHash() (كـ Alice). ثم، احسب kem_shared_key واستدعي MixKey(kem_shared_key). ثم عالج حمولة الرسالة كالمعتاد.

#### عمليات ML-KEM المُعرَّفة

نُعرّف الوظائف التالية المقابلة للبلوك البنائية التشفيرية المستخدمة كما هو محدد في [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

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

لاحظ أن كلاً من encap_key والنص المشفر يتم تشفيرهما داخل كتل ChaCha/Poly في رسائل Noise handshake 1 و 2. سيتم فك تشفيرهما كجزء من عملية المصافحة.

يتم خلط kem_shared_key في المفتاح المتسلسل باستخدام MixHash(). انظر أدناه للتفاصيل.

#### Alice KDF للرسالة 1

بعد نمط الرسالة 'es' وقبل البيانات النافعة، أضف:

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
#### Bob KDF للرسالة 1

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
#### Bob KDF للرسالة 2

بالنسبة لـ XK: بعد نمط الرسالة 'ee' وقبل الحمولة، أضف:

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
#### Alice KDF للرسالة 2

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
#### KDF للرسالة 3 (XK فقط)

غير متغير

#### KDF لـ split()

غير متغير

### تفاصيل Handshake

#### معرفات Noise

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) طلب الجلسة (SessionRequest)

التغييرات: يحتوي NTCP2 الحالي فقط على الخيارات في قسم ChaCha. مع ML-KEM، سيحتوي قسم ChaCha أيضًا على المفتاح العام المشفر للتشفير ما بعد الكمي (PQ).

حتى يمكن دعم NTCP2 مع PQ وبدون PQ على نفس عنوان router ونفس المنفذ، نستخدم البت الأكثر أهمية من قيمة X (المفتاح العام المؤقت X25519) للإشارة إلى أنه اتصال PQ. هذا البت يكون دائماً غير مُعيَّن للاتصالات غير PQ.

بالنسبة لأليس، بعد تشفير الرسالة بواسطة Noise، ولكن قبل تشويش AES للمتغير X، قم بتعيين X[31] |= 0x7f.

بالنسبة لبوب، بعد إلغاء التشويش AES للـ X، اختبر X[31] & 0x80. إذا كانت البت مضبوطة، امحها باستخدام X[31] &= 0x7f، وفك التشفير عبر Noise كاتصال PQ. إذا كانت البت غير مضبوطة، فك التشفير عبر Noise كاتصال غير PQ كالمعتاد.

بالنسبة لـ PQ NTCP2 المُعلن عنه على عنوان router مختلف ومنفذ مختلف، هذا غير مطلوب.

للحصول على معلومات إضافية، راجع قسم العناوين المنشورة أدناه.

المحتويات الخام:

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
البيانات غير المشفرة (علامة المصادقة Poly1305 غير مُظهرة):

```
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
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
ملاحظة: يجب تعيين حقل الإصدار في كتلة خيارات الرسالة 1 إلى 2، حتى لاتصالات PQ.

الأحجام:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1264+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1232</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
</table>
ملاحظة: أكواد الأنواع للاستخدام الداخلي فقط. ستبقى أجهزة router من النوع 4، وسيتم الإشارة إلى الدعم في عناوين أجهزة router.

#### 2) SessionCreated

المحتويات الخام:

المحتويات الخام:

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  -           16 bytes                    -
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
الأحجام:

```
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
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
الأحجام:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">784</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1168+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1104</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
</table>
ملاحظة: أكواد الأنواع للاستخدام الداخلي فقط. ستبقى أجهزة router من النوع 4، وسيتم الإشارة إلى الدعم في عناوين أجهزة router.

#### 3) SessionConfirmed

دون تغيير

#### دالة اشتقاق المفتاح (KDF) (لمرحلة البيانات)

غير متغير

#### العناوين المنشورة

استخدم نفس العنوان/المنفذ كما هو الحال مع non-PQ، non-firewalled. يتم دعم متغير PQ واحد فقط. في عنوان router، انشر v=2 (كالمعتاد) والمعامل الجديد pq=[3|4|5] للإشارة إلى MLKEM 512/768/1024. تقوم Alice بتعيين MSB للمفتاح المؤقت (key[31] & 0x80) في طلب الجلسة للإشارة إلى أن هذا اتصال مختلط. انظر أعلاه. ستتجاهل routers الأقدم معامل pq وتتصل non-pq كالمعتاد.

عنوان/منفذ مختلف كـ non-PQ، أو PQ-only، non-firewalled غير مدعوم. لن يتم تنفيذ هذا حتى يتم تعطيل non-PQ NTCP2، بعد عدة سنوات من الآن. عندما يتم تعطيل non-PQ، قد يتم دعم متغيرات PQ متعددة، ولكن واحد فقط لكل عنوان. عندما يتم دعمه، في عنوان الـ router، انشر v=[3|4|5] للإشارة إلى MLKEM 512/768/1024. Alice لا تقوم بتعيين MSB للمفتاح المؤقت. أجهزة الـ router الأقدم ستتحقق من معامل v وتتخطى هذا العنوان كغير مدعوم.

العناوين المحمية بجدار الحماية (لا يوجد IP منشور): في عنوان router، انشر v=2 (كالمعتاد). لا حاجة لنشر معامل pq.

يمكن لـ Alice الاتصال بـ PQ Bob باستخدام متغير PQ الذي ينشره Bob، سواء كانت Alice تعلن عن دعم pq في معلومات router الخاص بها أم لا، أو ما إذا كانت تعلن عن نفس المتغير.

في المواصفة الحالية، يتم تعريف الرسائل 1 و 2 لتحتوي على كمية "معقولة" من الحشو، مع نطاق موصى به من 0-31 بايت، ولا يتم تحديد حد أقصى.

#### الحد الأقصى للحشو

حتى API 0.9.68 (الإصدار 2.11.0)، نفذت Java I2P حداً أقصى قدره 256 بايت للحشو للاتصالات غير PQ، ولكن هذا لم يكن موثقاً سابقاً. اعتباراً من API 0.9.69 (الإصدار 2.12.0)، تنفذ Java I2P نفس الحد الأقصى للحشو للاتصالات غير PQ كما هو الحال مع MLKEM-512. انظر الجدول أدناه.

استخدم حجم الرسالة المحدد كحد أقصى للحشو، أي أن الحد الأقصى للحشو سيضاعف حجم الرسالة لاتصالات PQ، كما يلي:

زيادة الحجم (بايت):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message Max Padding</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">non-PQ (thru 0.9.68)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">non-PQ (as of 0.9.69)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-512</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-768</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-1024</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Session Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1264</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Session Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1168</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648</td>
</tr>
</table>
## تحليل الحمولة الإضافية

### تبادل المفاتيح

تم تلخيص فئات الأمان NIST في [عرض NIST](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) الشريحة 10. المعايير الأولية: يجب أن تكون فئة الأمان NIST الدنيا لدينا 2 للبروتوكولات المختلطة و 3 لـ PQ فقط.

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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
</tr>
</table>
## تحليل الأمان

هذه كلها بروتوكولات مختلطة. يجب أن تفضل التطبيقات MLKEM768؛ فإن MLKEM512 ليس آمناً بما فيه الكفاية.

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
### المصافحات

فئات الأمان NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

مكتبات Bouncycastle و BoringSSL و WolfSSL تدعم الآن MLKEM و MLDSA. دعم OpenSSL سيكون متاحاً في إصدارهم 3.5 في 8 أبريل 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
## ملاحظات التنفيذ

### دعم المكتبة

نحن نعين البت الأكثر أهمية (MSB) للمفتاح المؤقت (key[31] & 0x80) في طلب الجلسة للإشارة إلى أن هذا اتصال هجين. هذا يسمح لنا بتشغيل كل من NTCP القياسي و NTCP الهجين على نفس المنفذ. يتم دعم نوع هجين واحد فقط للاتصالات الواردة، ويتم الإعلان عنه في عنوان router. على سبيل المثال، pq=3 أو pq=4.

### تحديد حركة البيانات الواردة

كـ Alice، لاتصال PQ، قبل التشويش، اضبط X[31] |= 0x80. هذا يجعل X مفتاحًا عامًا غير صالح لـ X25519. بعد التشويش، سيقوم AES-CBC بجعله عشوائيًا. ستكون MSB الخاصة بـ X عشوائية بعد التشويش.

#### التشويش

كـ Bob، اختبر إذا كان (X[31] & 0x80) != 0 بعد إلغاء التشويش. إذا كان كذلك، فإنه اتصال PQ.

الحد الأدنى لإصدار router المطلوب لـ NTCP2-PQ لم يتم تحديده بعد.

ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى أجهزة router من النوع 4، وسيتم الإشارة إلى الدعم في عناوين router.

ملاحظة: أكواد الأنواع للاستخدام الداخلي فقط. ستبقى أجهزة router من النوع 4، وسيتم الإشارة إلى الدعم في عناوين أجهزة router.

## توافق Router

### أسماء النقل

في جميع الحالات، استخدم اسم النقل NTCP2 كالمعتاد. أجهزة router الأقدم ستتجاهل معامل pq وتتصل بـ NTCP2 القياسي كالمعتاد.

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
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
