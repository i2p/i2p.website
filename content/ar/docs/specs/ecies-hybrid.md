---
title: "PQ Hybrid ECIES-X25519-AEAD-Ratchet"
description: "المتغير الهجين لما بعد الكم لبروتوكول التشفير ECIES باستخدام ML-KEM"
slug: "ecies-hybrid"
category: "البروتوكولات"
lastUpdated: "2026-04"
accurateFor: "0.9.69"
---

## ملاحظة

التطبيق والاختبار والطرح قيد التقدم في تطبيقات router المختلفة. راجع توثيق تلك التطبيقات لمعرفة الحالة.

## نظرة عامة

هذا هو المتغير الهجين PQ لبروتوكول ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). إنه المرحلة الأولى من اقتراح PQ الشامل [Prop169](/proposals/169-pq-crypto/) التي تمت الموافقة عليها. راجع ذلك الاقتراح للأهداف العامة ونماذج التهديد والتحليل والبدائل والمعلومات الإضافية.

تحتوي هذه المواصفة فقط على الاختلافات عن [ECIES](/docs/specs/ecies/) القياسي ويجب قراءتها بالتزامن مع تلك المواصفة.

## التصميم

نحن ندعم معيار NIST FIPS 203 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) الذي يستند إلى خوارزمية CRYSTALS-Kyber، ولكن ليس متوافقًا معها.

المصافحات المختلطة محددة كما هو موضح في [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### تبادل المفاتيح

نُعرِّف تبادل مفاتيح هجين لـ Ratchet. يوفر PQ KEM مفاتيح مؤقتة فقط، ولا يدعم مباشرة عمليات التصافح بالمفاتيح الثابتة مثل Noise IK.

نحدد المتغيرات الثلاثة لـ ML-KEM كما هو موضح في [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)، لما مجموعه 3 أنواع تشفير جديدة. الأنواع المختلطة (Hybrid types) تُعرّف فقط بالتركيب مع X25519.

أنواع التشفير الجديدة هي:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
</table>
ستكون النفقات الإضافية كبيرة. أحجام الرسائل النموذجية 1 و 2 (لـ IK) تبلغ حاليًا حوالي 100 بايت (قبل أي حمولة إضافية). وسيزداد هذا بمقدار 8 إلى 15 مرة حسب الخوارزمية.

### مطلوب تشفير جديد

- ML-KEM (سابقاً CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- SHA3-128 (سابقاً Keccak-256) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) يُستخدم فقط لـ SHAKE128
- SHA3-256 (سابقاً Keccak-512) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 و SHAKE256 (امتدادات XOF لـ SHA3-128 و SHA3-256)
  [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

متجهات الاختبار لـ SHA3-256 و SHAKE128 و SHAKE256 متوفرة في [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

لاحظ أن مكتبة Java bouncycastle تدعم جميع ما سبق. دعم مكتبة C++ متوفر في OpenSSL 3.5 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

## المواصفة

### الهياكل المشتركة

انظر مواصفات الهياكل المشتركة [COMMON](/docs/specs/common-structures/) لأطوال المفاتيح والمعرفات.

### أنماط المصافحة

تستخدم المصافحات أنماط المصافحة الخاصة بـ [Noise](https://noiseprotocol.org/noise.html).

يتم استخدام خريطة الأحرف التالية:

- e = مفتاح مؤقت لمرة واحدة
- s = مفتاح ثابت
- p = حمولة الرسالة
- e1 = مفتاح PQ مؤقت لمرة واحدة، يُرسل من Alice إلى Bob
- ekem1 = نص KEM المشفر، يُرسل من Bob إلى Alice

التعديلات التالية على XK وIK للسرية الأمامية المختلطة (hfs) محددة كما هو موضح في [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 5:

```
IK:                         IKhfs:
<- s                        <- s
...                         ...
-> e, es, s, ss, p          -> e, es, e1, s, ss, p
<- tag, e, ee, se, p        <- tag, e, ee, ekem1, se, p
<- p                        <- p
p ->                        p ->

e1 and ekem1 are encrypted. See pattern definitions below.
NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
نمط e1 معرّف كما يلي، كما هو محدد في [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 4:

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
يتم تعريف نمط ekem1 كما يلي، كما هو محدد في [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 4:

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
### عمليات ML-KEM المُعرَّفة

نحدد الوظائف التالية المقابلة لكتل البناء التشفيرية المستخدمة كما هو معرف في [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

**(encap_key, decap_key) = PQ_KEYGEN()**

تقوم Alice بإنشاء مفاتيح التغليف وفك التغليف. يتم إرسال مفتاح التغليف في رسالة NS. تختلف أحجام encap_key و decap_key بناءً على متغير ML-KEM.

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)**

يحسب Bob النص المشفر والمفتاح المشترك، باستخدام النص المشفر المستلم في رسالة NS. يتم إرسال النص المشفر في رسالة NSR. يختلف حجم النص المشفر بناءً على متغير ML-KEM. إن kem_shared_key دائماً 32 بايت.

**kem_shared_key = DECAPS(ciphertext, decap_key)**

تحسب Alice المفتاح المشترك، باستخدام النص المشفر المستلم في رسالة NSR. إن kem_shared_key يكون دائماً 32 بايت.

لاحظ أن كل من encap_key والنص المشفر مشفران داخل كتل ChaCha/Poly في رسائل مصافحة Noise رقم 1 و 2. سيتم فك تشفيرهما كجزء من عملية المصافحة.

يتم خلط kem_shared_key في مفتاح التسلسل باستخدام MixHash(). انظر أدناه للتفاصيل.

### دالة اشتقاق المفتاح لمصافحة Noise

#### نظرة عامة

يتم تعريف المصافحة الهجينة في [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). تحتوي الرسالة الأولى، من Alice إلى Bob، على e1، مفتاح التغليف، قبل محتوى الرسالة. يتم التعامل مع هذا كمفتاح ثابت إضافي؛ استدع EncryptAndHash() عليه (كـ Alice) أو DecryptAndHash() (كـ Bob). ثم قم بمعالجة محتوى الرسالة كالمعتاد.

الرسالة الثانية، من Bob إلى Alice، تحتوي على ekem1، النص المشفر، قبل حمولة الرسالة. يتم التعامل معها كمفتاح ثابت إضافي؛ استدعِ EncryptAndHash() عليها (كـ Bob) أو DecryptAndHash() (كـ Alice). ثم، احسب kem_shared_key واستدعِ MixKey(kem_shared_key). ثم قم بمعالجة حمولة الرسالة كالمعتاد.

#### معرفات Noise

هذه هي سلاسل تهيئة Noise:

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Alice KDF لرسالة NS

بعد نمط الرسالة 'es' وقبل نمط الرسالة 's'، أضف:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### Bob KDF لرسالة NS

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### Bob KDF لرسالة NSR

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
#### Alice KDF لرسالة NSR

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
#### KDF للـ split()

غير متغير

### تنسيق الرسالة

#### تنسيق NS

التغييرات: احتوى ratchet الحالي على المفتاح الثابت في قسم ChaCha الأول، والحمولة في القسم الثاني. مع ML-KEM، يوجد الآن ثلاثة أقسام. القسم الأول يحتوي على المفتاح العام PQ المشفر. القسم الثاني يحتوي على المفتاح الثابت. القسم الثالث يحتوي على الحمولة.

التنسيق المشفر:

```
+----+----+----+----+----+----+----+----+
|                                       |
+         New Session Ephemeral         +
|            Public Key                 |
+            32 bytes                   +
|      Encoded with Elligator2          |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for encap_key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for Static Key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
التنسيق المفكوك التشفير:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|            (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
الأحجام:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">pl len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">96+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">912+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1296+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1360+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1680+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
لاحظ أن الحمولة يجب أن تحتوي على كتلة DateTime، لذا فإن الحد الأدنى لحجم الحمولة هو 7. يمكن حساب الحد الأدنى لأحجام NS وفقاً لذلك.

#### تنسيق NSR

التغييرات: ratchet الحالي يحتوي على payload فارغ للقسم الأول من ChaCha، و payload في القسم الثاني. مع ML-KEM، هناك الآن ثلاثة أقسام. القسم الأول يحتوي على النص المشفر PQ المشفر. القسم الثاني يحتوي على payload فارغ. القسم الثالث يحتوي على payload.

التنسيق المشفر:

```
+----+----+----+----+----+----+----+----+
|       Session Tag 8 bytes             |
+----+----+----+----+----+----+----+----+
|                                       |
+       Ephemeral Public Key            +
|            32 bytes                   |
+      Encoded with Elligator2          +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for ciphertext Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+   (MAC) for key Section (no data)     +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
التنسيق المفكوك التشفير:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

empty

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
الأحجام:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">72+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">856+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1176+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1656+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
لاحظ أنه بينما ستحتوي NSR عادة على payload غير صفري، فإن مواصفة ratchet [ECIES](/docs/specs/ecies/) لا تتطلب ذلك، لذا الحد الأدنى لحجم payload هو 0. يمكن حساب الحد الأدنى لأحجام NSR وفقاً لذلك.

## تحليل النفقات العامة

### تبادل المفاتيح

زيادة الحجم (بايت):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (NS)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (NSR)</th>
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
السرعة:

السرعات كما ذكرها [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Relative speed</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 DH/keygen</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">baseline</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2.25x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1.5x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1x (same)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">XK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH (keygen + 3 DH)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower</td>
</tr>
</table>
## تحليل الأمان

يتم تلخيص فئات الأمان لـ NIST في [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) الشريحة 10. المعايير الأولية: يجب أن تكون فئة الأمان الدنيا لـ NIST هي 2 للبروتوكولات الهجينة و3 لـ PQ-only.

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

هذه كلها بروتوكولات مختلطة. ربما نحتاج إلى تفضيل MLKEM768؛ MLKEM512 ليس آمناً بما فيه الكفاية.

فئات الأمان NIST [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

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
## تفضيلات النوع

النوع الموصى به للدعم الأولي، بناءً على فئة الأمان وطول المفتاح، هو:

MLKEM768_X25519 (النوع 6)

## ملاحظات التنفيذ

### دعم المكتبة

مكتبات Bouncycastle و BoringSSL و WolfSSL تدعم MLKEM الآن. دعم OpenSSL متوفر في إصدارهم 3.5 في 8 أبريل 2025 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Tunnels مشتركة

يجب أن يكون التصنيف/الكشف التلقائي لبروتوكولات متعددة على نفس tunnels ممكناً بناءً على فحص طول الرسالة 1 (رسالة الجلسة الجديدة). باستخدام MLKEM512_X25519 كمثال، طول الرسالة 1 أكبر بـ 816 بايت من بروتوكول ratchet الحالي، والحد الأدنى لحجم الرسالة 1 (مع تضمين حمولة DateTime فقط) هو 919 بايت. معظم أحجام الرسالة 1 مع ratchet الحالي لديها حمولة أقل من 816 بايت، لذلك يمكن تصنيفها كـ ratchet غير هجين. الرسائل الكبيرة هي على الأرجح POSTs والتي تكون نادرة.

لذا الاستراتيجية الموصى بها هي:

- إذا كانت الرسالة 1 أقل من 919 بايت، فهي بروتوكول ratchet الحالي.
- إذا كانت الرسالة 1 أكبر من أو تساوي 919 بايت، فهي على الأرجح MLKEM512_X25519. جرب MLKEM512_X25519 أولاً، وإذا فشل، جرب بروتوكول ratchet الحالي.

هذا يجب أن يسمح لنا بدعم standard ratchet و hybrid ratchet بكفاءة على نفس الوجهة، تماماً كما دعمنا سابقاً ElGamal و ratchet على نفس الوجهة. لذلك، يمكننا الانتقال إلى بروتوكول MLKEM hybrid بسرعة أكبر بكثير مما لو لم نكن قادرين على دعم البروتوكولات المزدوجة لنفس الوجهة، لأنه يمكننا إضافة دعم MLKEM للوجهات الموجودة.

التركيبات المطلوبة المدعومة هي:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

التركيبات التالية قد تكون معقدة، وهي غير مطلوبة للدعم، ولكن قد تكون كذلك، اعتماداً على التنفيذ:

- أكثر من MLKEM واحد
- ElG + واحد أو أكثر من MLKEM
- X25519 + واحد أو أكثر من MLKEM
- ElG + X25519 + واحد أو أكثر من MLKEM

ليس مطلوباً دعم خوارزميات MLKEM متعددة (على سبيل المثال، MLKEM512_X25519 و MLKEM_768_X25519) على نفس الوجهة. اختر واحدة فقط. يعتمد على التنفيذ.

ليس مطلوباً دعم ثلاث خوارزميات (على سبيل المثال X25519، MLKEM512_X25519، و MLKEM769_X25519) على نفس الوجهة. قد تكون استراتيجية التصنيف والإعادة المحاولة معقدة جداً. قد يكون التكوين وواجهة المستخدم للتكوين معقدين جداً. يعتمد على التنفيذ.

ليس مطلوباً دعم خوارزميات ElGamal والهجينة على نفس الوجهة. ElGamal عفا عليه الزمن، و ElGamal + الهجين فقط (بدون X25519) لا يحمل معنى كبير. أيضاً، رسائل الجلسة الجديدة الخاصة بـ ElGamal والهجين كلاهما كبيرة الحجم، لذا ستضطر استراتيجيات التصنيف غالباً إلى تجربة كلا التشفيرين، مما سيكون غير فعال. يعتمد على التطبيق.

يمكن للعملاء استخدام نفس مفاتيح X25519 الثابتة أو مفاتيح مختلفة لبروتوكولي X25519 والهجين على نفس الأنفاق، حسب التنفيذ.

### السرية المستقبلية

تسمح مواصفات ECIES برسائل Garlic في حمولة New Session Message، مما يمكّن من تسليم 0-RTT للحزمة الأولى من التدفق، عادة HTTP GET، مع leaseset الخاص بالعميل. ومع ذلك، فإن حمولة New Session Message لا تملك سرية أمامية (forward secrecy). نظراً لأن هذا الاقتراح يركز على تعزيز السرية الأمامية لآلية ratchet، فقد تؤجل التطبيقات أو يجب أن تؤجل تضمين حمولة التدفق، أو رسالة التدفق الكاملة، حتى أول Existing Session Message. هذا سيكون على حساب تسليم 0-RTT. قد تعتمد الاستراتيجيات أيضاً على نوع حركة البيانات أو نوع tunnel، أو على GET مقابل POST، على سبيل المثال. يعتمد على التطبيق.

### حجم الجلسة الجديدة

سيؤدي MLKEM إلى زيادة كبيرة جداً في حجم رسالة الجلسة الجديدة، كما هو موضح أعلاه. قد يقلل هذا بشكل كبير من موثوقية تسليم رسالة الجلسة الجديدة عبر الأنفاق، حيث يجب تجزئتها إلى عدة رسائل tunnel بحجم 1024 بايت. نجاح التسليم يتناسب طردياً مع العدد الأسي للأجزاء. قد تستخدم التطبيقات استراتيجيات مختلفة للحد من حجم الرسالة، على حساب تسليم 0-RTT. يعتمد على التطبيق.

## المراجع

- [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
- [COMMON](/docs/specs/common-structures/)
- [ECIES](/docs/specs/ecies/)
- [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [FORUM](http://zzz.i2p/topics/3294)
- [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
- [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
- [Noise](https://noiseprotocol.org/noise.html)
- [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
- [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
- [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
- [Prop169](/proposals/169-pq-crypto/)
