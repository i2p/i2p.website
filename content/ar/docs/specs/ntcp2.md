---
title: "بروتوكول النقل NTCP2"
description: "نقل TCP قائم على Noise (إطار بروتوكولات للتشفير) للروابط بين router وrouter"
slug: "ntcp2"
lastUpdated: "2025-10"
accurateFor: "0.9.66"
type: docs
---

## نظرة عامة

يستبدل NTCP2 بروتوكول النقل NTCP القديم بمصافحة مبنية على Noise تقاوم بصمة حركة المرور، وتشفّر حقول الطول، وتدعم مجموعات التشفير الحديثة. قد تُشغِّل Routers بروتوكول NTCP2 جنبًا إلى جنب مع SSU2 باعتبارهما بروتوكولي النقل الإلزاميين في شبكة I2P. أُعلن إهمال NTCP (الإصدار 1) في الإصدار 0.9.40 (مايو 2019) وأُزيل بالكامل في 0.9.50 (مايو 2021).

## إطار عمل بروتوكول Noise

يستخدم NTCP2 Noise Protocol Framework (إطار عمل بروتوكول Noise) [المراجعة 33، 2017-10-04](https://noiseprotocol.org/noise.html) مع امتدادات خاصة بـ I2P:

- **النمط**: `Noise_XK_25519_ChaChaPoly_SHA256`
- **المعرّف الموسَّع**: `Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256` (لتهيئة KDF (دالة اشتقاق المفاتيح))
- **دالة DH (ديفي-هيلمان)**: X25519 (RFC 7748) - مفاتيح بطول 32 بايت، ترميز little-endian (أصغر البايت أولاً)
- **خوارزمية التشفير**: AEAD_CHACHA20_POLY1305 (RFC 7539/RFC 8439)
  - nonce (قيمة غير متكررة) بطول 12 بايت: أول 4 بايت صفر، وآخر 8 بايت عداد (little-endian)
  - الحد الأقصى لقيمة nonce: 2^64 - 2 (يجب إنهاء الاتصال قبل الوصول إلى 2^64 - 1)
- **دالة التجزئة**: SHA-256 (مخرج بطول 32 بايت)
- **MAC (كود توثيق الرسالة)**: Poly1305 (وسم مصادقة بطول 16 بايت)

### امتدادات خاصة بـ I2P

1. **تمويه AES**: مفاتيح مؤقتة مُشفَّرة بـ AES-256-CBC باستخدام تجزئة router الخاصة ببوب وIV (متجه التهيئة) المنشور
2. **حشو عشوائي**: حشو نص صريح في الرسالتين 1-2 (مُوثَّق)، وحشو AEAD (مصادقة وتشفير مع بيانات إضافية) في الرسالة 3 فما بعدها (مُشفَّر)
3. **تمويه الطول بـ SipHash-2-4**: أطوال الأطر المكوّنة من بايتين تُجرى لها عملية XOR (أو الحصري) مع خرج SipHash
4. **بنية الإطار**: أطر مسبوقة بالطول لمرحلة البيانات (توافق التدفق عبر TCP)
5. **حمولات قائمة على الكتل**: تنسيق بيانات مُنظَّم بكتل ذات أنواع محددة

## تسلسل المصافحة

```
Alice (Initiator)             Bob (Responder)
SessionRequest  ──────────────────────►
                ◄────────────────────── SessionCreated
SessionConfirmed ──────────────────────►
```
### مصافحة بثلاث رسائل

1. **SessionRequest** - المفتاح المؤقت المموَّه لـ Alice، خيارات، تلميحات الحشو
2. **SessionCreated** - المفتاح المؤقت المموَّه لـ Bob، خيارات مُشفَّرة، حشو
3. **SessionConfirmed** - المفتاح الثابت المُشفَّر لـ Alice و RouterInfo (إطاران من نوع AEAD)

### أنماط رسائل Noise (إطار عمل لبروتوكولات المصافحة والتشفير)

```
XK(s, rs):           Authentication   Confidentiality
  <- s               (Bob's static key known in advance)
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
**مستويات المصادقة:** - 0: بلا مصادقة (يمكن لأي طرف أن يكون قد أرسل) - 2: مصادقة المرسِل مقاومة لانتحال الهوية عند اختراق المفتاح (KCI)

**مستويات السرية:** - 1: مستلم مؤقت (سرية أمامية، دون مصادقة للمستلم) - 2: مستلم معروف، سرية أمامية في حال اختراق المُرسِل فقط - 5: سرية أمامية قوية (مؤقت-مؤقت + مؤقت-ثابت DH (ديفي-هيلمان))

## مواصفات الرسائل

### اصطلاحات المفاتيح

- `RH_A` = تجزئة Router الخاصة بـ Alice (32 بايت، SHA-256)
- `RH_B` = تجزئة Router الخاصة بـ Bob (32 بايت، SHA-256)
- `||` = عامل الضم
- `byte(n)` = بايت واحد بقيمة n
- جميع الأعداد الصحيحة متعددة البايت تكون **big-endian** (ترتيب البايتات من الأكثر أهمية أولاً) ما لم يُنص على خلاف ذلك
- مفاتيح X25519 تكون **little-endian** (ترتيب البايتات من الأقل أهمية أولاً) (32 بايت)

### التشفير المُصادَق (ChaCha20-Poly1305)

**دالة التشفير:**

```
AEAD_ChaCha20_Poly1305(key, nonce, associatedData, plaintext)
  → (ciphertext || MAC)
```
**المعلمات:** - `key`: مفتاح تشفير بطول 32 بايت من KDF (دالة اشتقاق المفاتيح) - `nonce`: 12 بايت (4 بايتات صفرية + عدّاد بطول 8 بايت، little-endian (ترتيب البايت الأدنى أولاً)) - `associatedData`: تجزئة بطول 32 بايت في مرحلة المصافحة؛ بطول صفر في مرحلة البيانات - `plaintext`: البيانات المراد تشفيرها (0+ بايت)

**المخرجات:** - النص المُشفّر: نفس طول النص الواضح - MAC (رمز مصادقة الرسالة): 16 بايت (وسم مصادقة Poly1305)

**إدارة Nonce (عدد يُستخدم مرة واحدة):** - يبدأ العداد من 0 لكل مثيل للتشفير - يزداد مع كل عملية AEAD (مصادقة وتشفير ببيانات إضافية) في ذلك الاتجاه - عدادات منفصلة لـ Alice→Bob و Bob→Alice في مرحلة البيانات - يجب إنهاء الاتصال قبل أن يصل العداد إلى 2^64 - 1

## الرسالة 1: SessionRequest (طلب جلسة)

تبدأ أليس الاتصال ببوب.

**عمليات Noise (إطار لبروتوكولات المصافحة التشفيرية)**: `e, es` (توليد المفاتيح المؤقتة وتبادلها)

### التنسيق الخام

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted X (32B)      +
|    Key: RH_B, IV: Bob's published IV  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (X + options)       |
+    k from KDF-1, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**قيود الحجم:** - الحد الأدنى: 80 بايت (32 AES + 48 AEAD) - الحد الأقصى: 65535 بايت إجماليًا - **حالة خاصة**: حد أقصى 287 بايت عند الاتصال بعناوين "NTCP" (اكتشاف الإصدار)

### المحتوى بعد فك التشفير

```
+----+----+----+----+----+----+----+----+
|                                       |
+    X (Alice ephemeral public key)     +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### كتلة الخيارات (16 بايت، big-endian (البايت الأعلى أولاً))

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id      : 1 byte  - Network ID (2 for mainnet, 16-254 for testnets)
ver     : 1 byte  - Protocol version (currently 2)
padLen  : 2 bytes - Padding length in this message (0-65455)
m3p2len : 2 bytes - Length of SessionConfirmed part 2 frame
Rsvd    : 2 bytes - Reserved, set to 0
tsA     : 4 bytes - Unix timestamp (seconds since epoch)
Reserved: 4 bytes - Reserved, set to 0
```
**الحقول الحرجة:** - **Network ID** (منذ 0.9.42): الرفض السريع للاتصالات بين الشبكات - **m3p2len**: الحجم الدقيق للرسالة 3 الجزء 2 (يجب أن يتطابق عند الإرسال)

### دالة اشتقاق المفاتيح (KDF-1)

**تهيئة البروتوكول:**

```
protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
h = SHA256(protocol_name)
ck = h  // Chaining key initialized to hash
```
**عمليات MixHash:**

```
h = SHA256(h)                    // Null prologue
h = SHA256(h || rs)              // Bob's static key (known)
h = SHA256(h || e.pubkey)        // Alice's ephemeral key X
// h is now the associated data for message 1 AEAD
```
**عملية MixKey (مزج المفتاح) (نمط es):**

```
dh_result = X25519(Alice.ephemeral_private, Bob.static_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 1
// ck is retained for message 2 KDF
```
### ملاحظات التنفيذ

1. **تمويه AES**: يُستخدم لمقاومة فحص الحزم العميق (DPI) فقط؛ أي شخص يملك تجزئة router الخاصة ببوب وIV (متجه التهيئة) يمكنه فك تشفير X
2. **منع إعادة التشغيل**: يجب على بوب تخزين قيم X مؤقتاً (أو نظائرها المشفّرة) لمدة لا تقل عن 2*D ثانية (D = أقصى انحراف للساعة)
3. **التحقق من الطابع الزمني**: يجب على بوب رفض الاتصالات التي يكون فيها |tsA - current_time| > D (عادةً D = 60 ثانية)
4. **التحقق من المنحنى**: يجب على بوب التحقق من أن X نقطة صالحة على X25519
5. **الرفض السريع**: يجوز لبوب التحقق من X[31] & 0x80 == 0 قبل فك التشفير (مفاتيح X25519 الصالحة تكون البت الأكثر أهمية (MSB) فيها غير مُعيَّن)
6. **التعامل مع الأخطاء**: عند أي فشل، يُغلق بوب الاتصال بإرسال TCP RST بعد مهلة عشوائية وقراءة بايت عشوائي
7. **التخزين المؤقت**: يجب على أليس تفريغ الرسالة بالكامل (بما في ذلك الحشو) دفعة واحدة لتحقيق الكفاءة

## الرسالة 2: SessionCreated (تم إنشاء الجلسة)

بوب يرد على أليس.

**عمليات Noise (إطار بروتوكول للتشفير)**: `e, ee` (ديفي-هيلمان مؤقت-مؤقت)

### التنسيق الخام

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted Y (32B)      +
|    Key: RH_B, IV: AES state from msg1 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (Y + options)       |
+    k from KDF-2, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### المحتوى مفكوك التشفير

```
+----+----+----+----+----+----+----+----+
|                                       |
+    Y (Bob ephemeral public key)       +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### كتلة الخيارات (16 بايت، big-endian (ترتيب البايت الأعلى أهمية أولاً))

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Rsvd    : 2 bytes - Reserved, set to 0
padLen  : 2 bytes - Padding length in this message
Reserved: 10 bytes - Reserved, set to 0
tsB     : 4 bytes - Unix timestamp (seconds since epoch)
```
### دالة اشتقاق المفتاح (KDF-2)

**عمليات MixHash:**

```
h = SHA256(h || encrypted_payload_msg1)  // 32-byte ciphertext
if (msg1_padding_length > 0):
    h = SHA256(h || padding_from_msg1)
h = SHA256(h || e.pubkey)                // Bob's ephemeral key Y
// h is now the associated data for message 2 AEAD
```
**عملية MixKey (مزج المفتاح) (نمط ee):**

```
dh_result = X25519(Bob.ephemeral_private, Alice.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 2
// ck is retained for message 3 KDF
```
**تنظيف الذاكرة:**

```
// Overwrite ephemeral keys after ee DH
Alice.ephemeral_public = zeros(32)
Alice.ephemeral_private = zeros(32)  // Bob side
Bob.received_ephemeral = zeros(32)    // Bob side
```
### ملاحظات التنفيذ

1. **تسلسل AES**: يستخدم تشفير Y حالة AES-CBC من الرسالة 1 (دون إعادة ضبط)
2. **منع إعادة التشغيل**: يجب على Alice تخزين قيم Y مؤقتًا لمدة لا تقل عن 2*D ثانية
3. **التحقق من الطابع الزمني**: يجب على Alice رفض الحالات التي يتحقق فيها |tsB - current_time| > D
4. **التحقق من المنحنى**: يجب على Alice التحقق من أن Y نقطة X25519 (منحنى إهليلجي قياسي لتبادل المفاتيح) صالحة
5. **معالجة الأخطاء**: تقوم Alice بالإغلاق عبر TCP RST (إشارة إعادة ضبط في TCP) عند أي فشل
6. **التخزين المؤقت**: يجب على Bob إرسال الرسالة كاملة دفعة واحدة

## الرسالة 3: SessionConfirmed (تأكيد الجلسة)

تؤكد أليس الجلسة وترسل RouterInfo (معلومات الـ router).

**عمليات Noise**: `s, se` (إفشاء المفتاح الثابت وDH ثابت-مؤقت)

### بنية من جزأين

تتكون الرسالة 3 من **إطارَي AEAD (تشفير موثَّق مع بيانات مرتبطة) منفصلين**:

1. **الجزء 1**: إطار ثابت بطول 48 بايت مع مفتاح أليس الثابت المُشفّر
2. **الجزء 2**: إطار بطول متغير يحتوي على RouterInfo (بيانات تعريف router في I2P)، وخيارات، وحشو

### التنسيق الخام

```
+----+----+----+----+----+----+----+----+
|    ChaChaPoly Frame 1 (48 bytes)      |
+    Plaintext: Alice static key (32B)  +
|    k from KDF-2, n=1, ad=h            |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame 2 (variable)      +
|    Length specified in msg1.m3p2len   |
+    k from KDF-3, n=0, ad=h            +
|    Plaintext: RouterInfo + padding    |
+                                       +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**قيود الحجم:** - الجزء 1: بالضبط 48 بايت (32 نص صريح + 16 MAC (رمز تحقق الرسالة)) - الجزء 2: الطول محدد في الرسالة 1 (حقل m3p2len) - الحد الأقصى الإجمالي: 65535 بايت (الجزء 1 أقصاه 48، لذا الجزء 2 أقصاه 65487)

### المحتوى المفكوك التشفير

**الجزء الأول:**

```
+----+----+----+----+----+----+----+----+
|                                       |
+    S (Alice static public key)        +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**الجزء 2:**

```
+----+----+----+----+----+----+----+----+
|    Block: RouterInfo (required)       |
+    Type=2, contains Alice's RI         +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
|    Block: Options (optional)          |
+    Type=1, padding parameters          +
|                                       |
+----+----+----+----+----+----+----+----+
|    Block: Padding (optional)          |
+    Type=254, random data               +
|    MUST be last block if present      |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### دالة اشتقاق المفاتيح (KDF-3)

**الجزء 1 (نمط s):**

```
h = SHA256(h || encrypted_payload_msg2)  // 32-byte ciphertext
if (msg2_padding_length > 0):
    h = SHA256(h || padding_from_msg2)

// Encrypt static key with message 2 cipher key
ciphertext = AEAD_ChaCha20_Poly1305(k_msg2, n=1, h, Alice.static_public)
h = SHA256(h || ciphertext)  // 48 bytes (32 + 16)
// h is now the associated data for message 3 part 2
```
**الجزء 2 (se pattern):**

```
dh_result = X25519(Alice.static_private, Bob.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 3 part 2
// ck is retained for data phase KDF

ciphertext = AEAD_ChaCha20_Poly1305(k, n=0, h, payload)
h = SHA256(h || ciphertext)
// h is retained for SipHash KDF
```
**تنظيف الذاكرة:**

```
// Overwrite Bob's ephemeral key after se DH
Alice.received_ephemeral = zeros(32)  // Alice side
Bob.ephemeral_public = zeros(32)       // Bob side
Bob.ephemeral_private = zeros(32)      // Bob side
```
### ملاحظات التنفيذ

1. **التحقق من RouterInfo (معلومات الـrouter)**: على Bob التحقق من صحة التوقيع والطابع الزمني واتساق المفتاح
2. **مطابقة المفتاح**: على Bob التحقق من أن المفتاح الثابت لـ Alice في الجزء 1 يطابق المفتاح في RouterInfo
3. **موقع المفتاح الثابت**: ابحث عن معلمة "s" المطابقة في NTCP أو NTCP2 RouterAddress (عنوان الـrouter)
4. **ترتيب الكُتل**: يجب أن يكون RouterInfo أولاً، وOptions ثانياً (إن وُجدت)، وPadding أخيراً (إن وُجد)
5. **تخطيط الطول**: يجب على Alice التأكد من أن m3p2len في الرسالة 1 يطابق تماماً طول الجزء 2
6. **التخزين المؤقت**: يجب على Alice تفريغ الجزأين معاً كإرسال TCP واحد
7. **التسلسل الاختياري**: يجوز لـ Alice إلحاق data phase frame (إطار طور البيانات) فوراً لتحسين الكفاءة

## مرحلة البيانات

بعد اكتمال المصافحة، تستخدم جميع الرسائل إطارات AEAD (تعمية مصادقة مع بيانات مرتبطة) بطول متغيّر مع حقول طول مموّهة.

### دالة اشتقاق المفاتيح (مرحلة البيانات)

**دالة التقسيم (Noise):**

```
// Generate transmit and receive keys
zerolen = ""  // Zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)

// Alice transmits to Bob
k_ab = HMAC-SHA256(temp_key, byte(0x01))

// Bob transmits to Alice  
k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))

// Cleanup
ck = zeros(32)
temp_key = zeros(32)
```
**اشتقاق مفتاح SipHash (دالة تجزئة مُفتاحية):**

```
// Generate additional symmetric key for SipHash
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))

// "siphash" is 7 bytes US-ASCII
temp_key2 = HMAC-SHA256(ask_master, h || "siphash")
sip_master = HMAC-SHA256(temp_key2, byte(0x01))

// Alice to Bob SipHash keys
temp_key3 = HMAC-SHA256(sip_master, zerolen)
sipkeys_ab = HMAC-SHA256(temp_key3, byte(0x01))
sipk1_ab = sipkeys_ab[0:7]   // 8 bytes, little-endian
sipk2_ab = sipkeys_ab[8:15]  // 8 bytes, little-endian
sipiv_ab = sipkeys_ab[16:23] // 8 bytes, IV

// Bob to Alice SipHash keys
sipkeys_ba = HMAC-SHA256(temp_key3, sipkeys_ab || byte(0x02))
sipk1_ba = sipkeys_ba[0:7]   // 8 bytes, little-endian
sipk2_ba = sipkeys_ba[8:15]  // 8 bytes, little-endian
sipiv_ba = sipkeys_ba[16:23] // 8 bytes, IV
```
### بنية الإطار

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+    ChaChaPoly Frame         +
|    Encrypted Block Data               |
+    k_ab (Alice→Bob) or k_ba (Bob→Alice)|
|    Nonce starts at 0, increments      |
+    No associated data (empty string)  +
|                                       |
~           .   .   .                   ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Poly1305 MAC (16 bytes)            |
+----+----+----+----+----+----+----+----+
```
**قيود الإطار:** - الحد الأدنى: 18 بايت (2 طول مموّه + 0 نص صريح + 16 MAC (رمز المصادقة على الرسائل)) - الحد الأقصى: 65537 بايت (2 طول مموّه + 65535 إطار) - مُوصى به: بضعة كيلوبايت لكل إطار (لتقليل الكمون لدى المتلقي)

### تمويه الطول باستخدام SipHash (خوارزمية تجزئة مصادِقة خفيفة)

**الغرض**: منع تعرّف التفتيش العميق للحزم (DPI) على حدود الإطارات

**الخوارزمية:**

```
// Initialization (per direction)
IV[0] = sipiv  // From KDF

// For each frame:
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]  // First 2 bytes of IV
ObfuscatedLength = ActualLength XOR Mask[n]

// Send 2-byte ObfuscatedLength, then ActualLength bytes
```
**فك الترميز:**

```
// Receiver maintains identical IV chain
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]
ActualLength = ObfuscatedLength XOR Mask[n]
// Read ActualLength bytes (includes 16-byte MAC)
```
**ملاحظات:** - سلاسل IV (مُتّجه التهيئة) منفصلة لكل اتجاه (Alice→Bob و Bob→Alice) - إذا أعاد SipHash (خوارزمية تجزئة) قيمة uint64، فاستخدم أقل بايتين أهمية كقناع - حوّل uint64 إلى IV التالي كبايتات بالترتيب الصغير (little-endian)

### تنسيق الكتلة

يحتوي كل إطار على صفر أو أكثر من الكتل:

```
+----+----+----+----+----+----+----+----+
|Type| Length  |       Data              |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1 byte  - Block type identifier
Length: 2 bytes - Big-endian, data size (0-65516)
Data  : Variable length payload
```
**حدود الحجم:** - أقصى حجم للإطار: 65535 بايت (بما في ذلك MAC) - أقصى مساحة للكتلة: 65519 بايت (الإطار - MAC بحجم 16 بايت) - أقصى حجم لكتلة واحدة: 65519 بايت (ترويسة بحجم 3 بايت + بيانات بحجم 65516)

### أنواع الكتل

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Time synchronization (4-byte timestamp)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding parameters, dummy traffic</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo delivery/flooding</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP message with shortened header</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Explicit connection close</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental features</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Random padding (must be last)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future extensions</td></tr>
  </tbody>
</table>
**قواعد ترتيب الكتل:** - **الرسالة 3 الجزء 2**: RouterInfo، Options (اختياري)، Padding (اختياري) - لا توجد أنواع أخرى - **مرحلة البيانات**: بأي ترتيب باستثناء:   - يجب أن تكون Padding آخر كتلة إذا وُجدت   - يجب أن تكون Termination آخر كتلة (باستثناء Padding) إذا وُجدت - يُسمح بكتلات I2NP متعددة لكل إطار - لا يُسمح بكتلات Padding متعددة لكل إطار

### نوع الكتلة 0: DateTime (التاريخ والوقت)

مزامنة الوقت لاكتشاف انحراف الساعة.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

Type     : 0
Length   : 4 (big-endian)
Timestamp: 4 bytes, Unix seconds (big-endian)
```
**التنفيذ**: قرّب إلى أقرب ثانية لمنع تراكم انحياز الساعة.

### نوع الكتلة 1: الخيارات

معلمات الحشو وتشكيل حركة المرور.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
+----+----+----+----+----+----+----+    +
|         more_options (TBD)            |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1
Length: 12+ bytes (big-endian)
```
**نسب الحشو** (عدد بنقطة ثابتة 4.4، القيمة/16.0): - `tmin`: أدنى نسبة حشو للإرسال (0.0 - 15.9375) - `tmax`: أقصى نسبة حشو للإرسال (0.0 - 15.9375) - `rmin`: أدنى نسبة حشو للاستقبال (0.0 - 15.9375) - `rmax`: أقصى نسبة حشو للاستقبال (0.0 - 15.9375)

**أمثلة:** - 0x00 = 0% حشو - 0x01 = 6.25% حشو - 0x10 = 100% حشو (نسبة 1:1) - 0x80 = 800% حشو (نسبة 8:1)

**حركة المرور الوهمية:** - `tdmy`: الحد الأقصى المستعد لإرساله (2 بايت، متوسط بايت/ثانية) - `rdmy`: المطلوب استلامه (2 بايت، متوسط بايت/ثانية)

**إدراج التأخير:** - `tdelay`: الحد الأقصى المستعد لإدراجه (2 بايت، متوسط بالميلي ثانية) - `rdelay`: التأخير المطلوب (2 بايت، متوسط بالميلي ثانية)

**الإرشادات:** - تشير القيم الدنيا إلى مستوى مقاومة تحليل حركة المرور المرغوب - تشير القيم القصوى إلى قيود عرض النطاق الترددي - على المرسل احترام الحد الأقصى الذي حدده المستقبل - قد يراعي المرسل الحد الأدنى الذي حدده المستقبل ضمن القيود - لا توجد آلية إنفاذ؛ قد تختلف التنفيذات

### نوع الكتلة 2: RouterInfo (معلومات الـ router)

تسليم RouterInfo من أجل تعبئة netdb والنشر الواسع.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type : 2
Length: Flag (1 byte) + RouterInfo size
Flag : Bit 0 = flood request (1) or local store (0)
       Bits 1-7 = Reserved, set to 0
```
**الاستخدام:**

**في الرسالة 3 الجزء 2** (مصافحة): - ترسل أليس RouterInfo (بيانات تعريف الـ Router في I2P) إلى بوب - بتّ Flood عادةً 0 (تخزين محلي) - RouterInfo غير مضغوطة بـ gzip

**في مرحلة البيانات:** - يمكن لأي من الطرفين إرسال RouterInfo (بنية بيانات معلومات Router في I2P) المحدَّثة لديه - Flood bit (بت التحكم بآلية Flood) = 1: طلب توزيع عبر floodfill (إذا كان المستلم floodfill) - Flood bit = 0: تخزين محلي في netdb فقط

**متطلبات التحقق:** 1. تحقق من أن نوع التوقيع مدعوم 2. تحقق من توقيع RouterInfo 3. تحقق من أن الطابع الزمني يقع ضمن الحدود المقبولة 4. في مرحلة المصافحة: تحقق من تطابق المفتاح الثابت مع معلمة "s" في عنوان NTCP2 5. في مرحلة البيانات: تحقق من تطابق تجزئة الـ router مع نظير الجلسة 6. أغرق فقط RouterInfos ذات العناوين المنشورة

**ملاحظات:** - لا توجد آلية ACK (إقرار الاستلام؛ استخدم I2NP DatabaseStore مع رمز الرد إذا لزم الأمر) - قد تحتوي على RouterInfos لطرف ثالث (استخدام floodfill) - غير مضغوطة باستخدام gzip (على عكس I2NP DatabaseStore)

### نوع الكتلة 3: رسالة I2NP

رسالة I2NP ذات ترويسة مختصرة بطول 9 بايت.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg_id         |
+----+----+----+----+----+----+----+----+
|   expiration  |     I2NP payload      |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type      : 3
Length    : 9 + payload_size (big-endian)
Type      : 1 byte, I2NP message type
Msg_ID    : 4 bytes, big-endian, I2NP message ID
Expiration: 4 bytes, big-endian, Unix timestamp (seconds)
Payload   : I2NP message body (length = size - 9)
```
**الاختلافات عن NTCP1:** - وقت الانتهاء: 4 بايت (ثواني) مقابل 8 بايت (ميلي ثانية) - الطول: محذوف (يمكن اشتقاقه من طول الكتلة) - المجموع الاختباري: محذوف (AEAD (تشفير موثَّق مع بيانات مرتبطة) يوفر سلامة البيانات) - الترويسة: 9 بايت مقابل 16 بايت (انخفاض بنسبة 44%)

**التجزئة:** - رسائل I2NP يجب ألا تُجزأ عبر الكتل - رسائل I2NP يجب ألا تُجزأ عبر الإطارات - يُسمح بوجود عدة كتل I2NP لكل إطار

### نوع الكتلة 4: الإنهاء

إغلاق الاتصال بشكل صريح مع رمز السبب.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |  valid_frames_recv    |
+----+----+----+----+----+----+----+----+
| (continued) |rsn |   additional_data   |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type            : 4
Length          : 9+ bytes (big-endian)
Valid_Frames_Recv: 8 bytes, big-endian (receive nonce value)
                  0 if error in handshake phase
Reason          : 1 byte (see table below)
Additional_Data : Optional (format unspecified, for debugging)
```
**رموز الأسباب:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Phase</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data phase AEAD failure</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible signature type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Clock skew</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding violation</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD framing error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Payload format error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 1 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 2 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 3 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Intra-frame read timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo signature verification fail</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Static key parameter mismatch</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Banned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
  </tbody>
</table>
**القواعد:** - يجب أن تكون كتلة الإنهاء آخر كتلة غير الحشو في الإطار - كتلة إنهاء واحدة كحد أقصى لكل إطار - على المرسل إغلاق الاتصال بعد الإرسال - على المستلم إغلاق الاتصال بعد الاستلام

**معالجة الأخطاء:** - أخطاء المصافحة: عادةً يُغلَق الاتصال عبر TCP RST (بدون كتلة إنهاء) - أخطاء AEAD (التشفير المصادق المرتبط بالبيانات) في مرحلة البيانات: مهلة عشوائية + قراءة عشوائية، ثم إرسال الإنهاء - راجع قسم "AEAD Error Handling" لإجراءات الأمان

### نوع الكتلة 254: حشو

حشو عشوائي لمقاومة تحليل حركة المرور.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |     random_data       |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type: 254
Length: 0-65516 bytes (big-endian)
Data: Cryptographically random bytes
```
**القواعد:** - يجب أن تكون كتلة الحشو الأخيرة في الإطار إذا وُجدت - يُسمح بحشو بطول صفري - كتلة حشو واحدة فقط لكل إطار - يُسمح بالإطارات التي تحتوي على الحشو فقط - ينبغي الالتزام بالمعلمات المتفق عليها من كتلة الخيارات

**الحشو في الرسائل 1-2:** - خارج إطار AEAD (المصادقة والتشفير مع البيانات المرتبطة) (نص واضح) - مُتضمَّن في سلسلة تجزئة الرسالة التالية (مُوثَّق) - يتم اكتشاف العبث عند فشل AEAD للرسالة التالية

**الحشو في الرسالة 3+ ومرحلة البيانات:** - داخل إطار AEAD (مشفّر ومُوثَّق) - يُستخدم لتشكيل حركة المرور وتمويه الحجم

## معالجة أخطاء AEAD (التشفير المصادق مع بيانات مرتبطة)

**المتطلبات الأمنية الحرجة:**

### مرحلة المصافحة (الرسائل 1-3)

**حجم الرسالة المعروف:** - أحجام الرسائل محددة مسبقاً أو مُعيّنة سلفاً - فشل مصادقة AEAD (التشفير المصادق مع بيانات مرتبطة) غير ملتبس

**استجابة Bob لفشل الرسالة 1:** 1. اضبط مهلة عشوائية (النطاق يعتمد على التنفيذ، يُقترَح 100-500 مللي ثانية) 2. اقرأ عدداً عشوائياً من البايتات (النطاق يعتمد على التنفيذ، يُقترَح 1KB-64KB) 3. أغلق الاتصال باستخدام TCP RST (إشارة إعادة ضبط TCP) (من دون استجابة) 4. أدرِج عنوان IP المصدر في القائمة السوداء مؤقتاً 5. تتبّع حالات الفشل المتكررة لفرض حظر طويل الأمد

**استجابة أليس لفشل الرسالة 2:** 1. أغلق الاتصال فوراً باستخدام TCP RST 2. لا ترسل أي رد إلى بوب

**استجابة بوب لفشل الرسالة 3:** 1. إغلاق الاتصال فورًا باستخدام TCP RST (إشارة إعادة الضبط في TCP) 2. عدم الرد على أليس

### مرحلة البيانات

**حجم الرسالة المموَّه:** - حقل الطول مموَّه بـSipHash - قد يدل طول غير صالح أو فشل في AEAD (تعمية مصادق عليها مع بيانات مرتبطة) على:   - استطلاع من مهاجم   - فساد في الشبكة   - عدم تزامن IV (متجه التهيئة) الخاص بـSipHash   - نظير خبيث

**الاستجابة لخطأ AEAD (تشفير موثَّق مع بيانات مرتبطة) أو خطأ في الطول:** 1. اضبط مهلة عشوائية (مقترح 100-500ms) 2. اقرأ عدداً عشوائياً من البايتات (مقترح 1KB-64KB) 3. أرسل كتلة إنهاء مع رمز السبب 4 (فشل AEAD) أو 9 (خطأ في التأطير) 4. أغلق الاتصال

**منع Decryption Oracle (هجوم الأوراكل لفك التشفير):** - لا تفصح مطلقًا للنظير عن نوع الخطأ قبل انقضاء مهلة عشوائية - لا تتجاوز مطلقًا التحقق من الطول قبل فحص AEAD - عامِل الطول غير الصالح معاملة فشل AEAD نفسه - استخدم مسار معالجة أخطاء متطابقًا لكلا الخطأين

**اعتبارات التنفيذ:** - قد تستمر بعض التنفيذات في العمل بعد أخطاء AEAD (تشفير مصادق مع بيانات مرتبطة) إذا كانت نادرة - قم بإنهاء بعد تكرار الأخطاء (الحد المقترح: 3-5 أخطاء في الساعة) - وازن بين التعافي من الأخطاء والأمان

## RouterInfo (بيانات تعريف الـ router) المنشور

### تنسيق عنوان Router

يتم الإعلان عن دعم NTCP2 من خلال إدخالات RouterAddress (عنوان الـrouter) المنشورة مع خيارات محددة.

**نمط النقل:** - `"NTCP2"` - NTCP2 فقط على هذا المنفذ - `"NTCP"` - كلا من NTCP وNTCP2 على هذا المنفذ (اكتشاف تلقائي)   - **ملاحظة**: تمّت إزالة دعم NTCP (v1) في 0.9.50 (مايو 2021)   - نمط "NTCP" أصبح الآن مهجورًا؛ استخدم "NTCP2"

### الخيارات المطلوبة

**جميع عناوين NTCP2 المنشورة:**

1. **`host`** - عنوان IP (IPv4 أو IPv6) أو اسم المضيف
   - الصيغة: صيغة IP القياسية أو اسم نطاق
   - قد يُترك في حالات الصادر فقط أو routers المخفية

2. **`port`** - رقم منفذ TCP
   - الصيغة: عدد صحيح، 1-65535
   - قد يُهمَل في routers المخصصة للاتصالات الصادرة فقط أو المخفية

3. **`s`** - مفتاح عام ثابت (X25519)
   - الصيغة: مرمّز بـ Base64، 44 محرف
   - الترميز: أبجدية Base64 الخاصة بـ I2P
   - المصدر: مفتاح عام X25519 بطول 32 بايت، ليتل إنديان (ترتيب بايتات صغير النهاية)

4. **`i`** - متجه التهيئة لـ AES
   - التنسيق: مُرمَّز بـ Base64، 24 حرفًا
   - الترميز: أبجدية Base64 الخاصة بـ I2P
   - المصدر: IV بطول 16 بايت، big-endian (ترتيب البايت الكبير)

5. **`v`** - إصدار البروتوكول
   - الصيغة: عدد صحيح أو أعداد صحيحة مفصولة بفواصل
   - الحالي: `"2"`
   - المستقبلي: `"2,3"` (يجب أن تكون بترتيب رقمي)

**خيارات اختيارية:**

6. **`caps`** - القدرات (منذ 0.9.50)
   - الصيغة: سلسلة من أحرف القدرات
   - القيم:
     - `"4"` - قدرة اتصال صادر عبر IPv4
     - `"6"` - قدرة اتصال صادر عبر IPv6
     - `"46"` - كلاهما IPv4 وIPv6 (الترتيب الموصى به)
   - غير مطلوب إذا كان `host` منشورًا
   - مفيد لـ routers المخفية/المحمية بجدار ناري

7. **`cost`** - أولوية العنوان
   - التنسيق: عدد صحيح، 0-255
   - القيم الأقل = أولوية أعلى
   - مقترح: 5-10 للعناوين العادية
   - مقترح: 14 للعناوين غير المنشورة

### أمثلة على مدخلات RouterAddress

**عنوان IPv4 المُعلن:**

```
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Router مخفي (صادر فقط):**

```
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
    <caps>4</caps>
  </options>
</Address>
```
**Router ثنائي المكدس:**

```
<!-- IPv4 Address -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>

<!-- IPv6 Address (same keys, same port) -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>2001:db8::1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**قواعد مهمة:** - يجب أن تستخدم عناوين NTCP2 المتعددة التي تشترك في الـ**منفذ نفسه** قيم `s` و`i` و`v` **متطابقة** - قد تستخدم المنافذ المختلفة مفاتيح مختلفة - يُستحسن أن تنشر routers ثنائية المكدس عناوين IPv4 وIPv6 منفصلة

### عنوان NTCP2 غير منشور

**بالنسبة إلى Routers ذات الاتصالات الصادرة فقط:**

إذا كان الـ router لا يقبل اتصالات NTCP2 الواردة ولكنه يُنشئ اتصالات صادرة، فيجب عليه رغم ذلك نشر RouterAddress (عنوان الـ router) مع:

```xml
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
  </options>
</Address>
```
**الغرض:** - يتيح لـ Bob التحقق من المفتاح الثابت الخاص بـ Alice أثناء المصافحة - مطلوب للتحقق من RouterInfo (معلومات الـ router) في الرسالة 3 الجزء 2 - لا حاجة إلى `i` أو `host` أو `port` (صادر فقط)

**بديل:** - أضف `s` و `v` إلى عنوان "NTCP" أو SSU المنشور مسبقًا

### تدوير المفتاح العام وIV (متجه التهيئة)

**سياسة أمنية حرجة:**

**القواعد العامة:** 1. **لا تقم أبداً بالتدوير أثناء كون router قيد التشغيل** 2. **قم بتخزين المفتاح وIV (متجه التهيئة) بشكل دائم** عبر عمليات إعادة التشغيل 3. **تتبّع فترات التوقف السابقة** لتحديد أهلية التدوير

**الحد الأدنى لمدة التوقف قبل التدوير:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Min Downtime</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published NTCP2 address</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 month</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Many routers cache RouterInfo</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published SSU only (no NTCP2)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 day</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Moderate caching</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">No published addresses (hidden)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2 hours</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal impact</td></tr>
  </tbody>
</table>
**مشغّلات إضافية:** - تغيير عنوان IP المحلي: قد يحدث تدوير بغضّ النظر عن انقطاع الخدمة - Router "rekey" (new Router Hash): إنشاء مفاتيح جديدة

**المسوغات:** - يمنع كشف أوقات إعادة التشغيل عبر تغييرات المفاتيح - يتيح لـ RouterInfos (ملفات تعريف router) المخزّنة مؤقتًا أن تنقضي بشكل طبيعي - يحافظ على استقرار الشبكة - يقلّل محاولات الاتصال الفاشلة

**التنفيذ:** 1. خزّن المفتاح وIV (متجه التهيئة) والطابع الزمني لآخر إيقاف تشغيل بشكل دائم 2. عند بدء التشغيل، احسب downtime = current_time - last_shutdown 3. إذا كان downtime > الحد الأدنى لنوع الـ router، فقد يتم التدوير 4. إذا تغيّر IP أو كان هناك إعادة توليد للمفاتيح، فقد يتم التدوير 5. وبخلاف ذلك، أعِد استخدام المفتاح وIV السابقين

**تدوير IV (متجه التهيئة):** - يخضع لنفس قواعد تدوير المفتاح - يظهر فقط في العناوين المنشورة (وليس في routers المخفية) - يُوصى بتغيير IV كلما تغيّر المفتاح

## اكتشاف الإصدار

**السياق:** عند تعيين `transportStyle="NTCP"` (قديم)، يدعم Bob كلًا من NTCP v1 و v2 على المنفذ نفسه ويجب أن يكتشف إصدار البروتوكول تلقائيًا.

**خوارزمية الكشف:**

```
1. Wait for at least 64 bytes (minimum NTCP2 message 1 size)

2. If received ≥ 288 bytes:
   → Connection is NTCP version 1 (NTCP1 message 1 is 288 bytes)

3. If received < 288 bytes:
   
   Option A (conservative, pre-NTCP2 majority):
   a. Wait additional short time (e.g., 100-500ms)
   b. If total received ≥ 288 bytes → NTCP1
   c. Otherwise → Attempt NTCP2 decode
   
   Option B (aggressive, post-NTCP2 majority):
   a. Attempt NTCP2 decode immediately:
      - Decrypt first 32 bytes (X key) with AES-256-CBC
      - Verify valid X25519 point (X[31] & 0x80 == 0)
      - Verify AEAD frame
   b. If decode succeeds → NTCP2
   c. If decode fails → Wait for more data or NTCP1
```
**فحص MSB (البِت الأكثر أهمية) السريع:** - قبل فك تشفير AES، تحقّق: `encrypted_X[31] & 0x80 == 0` - المفاتيح الصحيحة لـ X25519 تكون البِت الأعلى فيها مُصفّرة - يشير الفشل على الأرجح إلى NTCP1 (نسخة أقدم من بروتوكول النقل في I2P) (أو هجوم) - نفّذ مقاومة الاستقصاء (مهلة عشوائية + قراءة) عند الفشل

**متطلبات التنفيذ:**

1. **مسؤولية أليس:**
   - عند الاتصال بعنوان "NTCP"، اقصر الرسالة 1 على 287 بايت كحد أقصى
   - قم بتخزين الرسالة 1 مؤقتًا وتفريغها بالكامل دفعة واحدة
   - يزيد احتمال التسليم ضمن حزمة TCP واحدة

2. **مسؤوليات بوب:**
   - تخزين البيانات المستلمة مؤقتاً قبل تحديد الإصدار
   - تنفيذ التعامل الصحيح مع انتهاء المهلة
   - استخدام TCP_NODELAY للكشف السريع عن الإصدار
   - تخزين وتفريغ الرسالة 2 كاملة دفعة واحدة بعد تحديد الإصدار

**اعتبارات الأمان:** - هجمات التجزئة: ينبغي أن يكون Bob مقاومًا لتجزئة TCP - هجمات الاستطلاع: تنفيذ تأخيرات عشوائية وقراءات بايت عند حالات الفشل - منع هجمات حجب الخدمة (DoS): تقييد عدد الاتصالات المعلقة المتزامنة - مهل القراءة: لكل عملية قراءة وإجماليًا (حماية "slowloris" — هجوم يُبقي الاتصال مفتوحًا عبر إرسال بيانات بطيئة جدًا)

## إرشادات انحراف الساعة

**حقول الطابع الزمني:** - الرسالة 1: `tsA` (الطابع الزمني الخاص بـ Alice) - الرسالة 2: `tsB` (الطابع الزمني الخاص بـ Bob) - الرسالة 3+: كتل DateTime (تاريخ/وقت) اختيارية

**الانحراف الأقصى (D):** - المعتاد: **±60 ثانية** - قابل للتهيئة حسب كل تنفيذ - إذا كان الانحراف > D فعادةً ما يكون قاتلاً

### معالجة بوب (الرسالة 1)

```
1. Receive tsA from Alice
2. skew = tsA - current_time
3. If |skew| > D:
   a. Still send message 2 (allows Alice to calculate skew)
   b. Include tsB in message 2
   c. Do NOT initiate handshake completion
   d. Optionally: Temporary ban Alice's IP
   e. After message 2 sent, close connection

4. If |skew| ≤ D:
   a. Continue handshake normally
```
**التبرير:** إرسال الرسالة 2 حتى في حالة الانحراف الزمني (skew) يمكّن أليس من تشخيص مشكلات الساعة.

### معالجة أليس (الرسالة 2)

```
1. Receive tsB from Bob
2. RTT = (current_time_now - tsA_sent)
3. adjusted_skew = (tsB - current_time_now) - (RTT / 2)
4. If |adjusted_skew| > D:
   a. Close connection immediately
   b. If local clock suspect: Adjust clock or use external time source
   c. If Bob's clock suspect: Temporary ban Bob
   d. Log for operator review
5. If |adjusted_skew| ≤ D:
   a. Continue handshake normally
   b. Optionally: Track skew for time synchronization
```
**ضبط RTT (زمن الرحلة ذهابًا وإيابًا):** - اطرح نصف RTT من الانحراف المحسوب - يأخذ في الحسبان تأخير انتشار الشبكة - تقدير أكثر دقة للانحراف

### معالجة بوب (الرسالة 3)

```
1. If message 3 received (unlikely if skew exceeded in message 1)
2. Recalculate skew = tsA_received - current_time
3. If |adjusted_skew| > D:
   a. Send termination block (reason code 7: clock skew)
   b. Close connection
   c. Ban Alice for period (e.g., 1-24 hours)
```
### مزامنة الوقت

**كتل التاريخ والوقت (مرحلة البيانات):** - أرسل كتلة التاريخ والوقت دورياً (النوع 0) - يمكن للمستلم استخدامها لضبط الساعة - قرّب الطابع الزمني إلى أقرب ثانية (لتجنّب الانحياز)

**مصادر الوقت الخارجية:** - NTP (بروتوكول وقت الشبكة) - مزامنة ساعة النظام - وقت إجماع شبكة I2P

**استراتيجيات ضبط الساعة:** - إذا كانت الساعة المحلية غير دقيقة: اضبط وقت النظام أو استخدم إزاحة زمنية - إذا كانت ساعات النظراء غير دقيقة باستمرار: أشِر إلى وجود مشكلة لدى النظير - تتبّع إحصاءات الانحراف الزمني لمراقبة صحة الشبكة

## خصائص الأمان

### السرية الأمامية

**تم تحقيقه عبر:** - تبادل مفاتيح ديفي-هيلمان المؤقت (X25519 — منحنى إهليليجي لتبادل المفاتيح) - ثلاث عمليات DH: es, ee, se (Noise XK pattern — نمط المصافحة XK ضمن إطار Noise) - تُتلف المفاتيح المؤقتة بعد إتمام المصافحة

**تدرّج السرّية:** - الرسالة 1: المستوى 2 (سرّية أمامية في حال اختراق المُرسِل) - الرسالة 2: المستوى 1 (مستلم مؤقت) - الرسالة 3+: المستوى 5 (سرّية أمامية قوية)

**السرية التامة للأمام (Perfect Forward Secrecy):** - اختراق المفاتيح الثابتة طويلة الأجل لا يؤدي إلى كشف مفاتيح الجلسات السابقة - كل جلسة تستخدم مفاتيح مؤقتة فريدة - لا يُعاد استخدام المفاتيح الخاصة المؤقتة أبداً - تنظيف الذاكرة بعد اتفاق المفاتيح

**القيود:** - الرسالة 1 تكون عرضة للخطر إذا تم اختراق مفتاح Bob الثابت (لكن توجد سرية أمامية في مواجهة اختراق Alice) - هجمات إعادة الإرسال ممكنة للرسالة 1 (يخفف أثرها عبر الطابع الزمني وذاكرة التخزين المؤقت لإعادة الإرسال)

### المصادقة

**المصادقة المتبادلة:** - تمت مصادقة أليس بمفتاح ثابت في الرسالة 3 - تمت مصادقة بوب عبر امتلاكه مفتاحاً خاصاً ثابتاً (ضمنياً نتيجة المصافحة الناجحة)

**مقاومة Key Compromise Impersonation (KCI) (انتحال الهوية عند اختراق المفتاح):** - مستوى المصادقة 2 (مقاوم لـ KCI) - لا يستطيع المهاجم انتحال شخصية Alice حتى مع المفتاح الخاص الثابت لـ Alice (من دون المفتاح المؤقت لـ Alice) - لا يستطيع المهاجم انتحال شخصية Bob حتى مع المفتاح الخاص الثابت لـ Bob (من دون المفتاح المؤقت لـ Bob)

**التحقق من المفتاح الثابت:** - تعرف Alice مفتاح Bob الثابت مسبقاً (من RouterInfo (معلومات الـrouter)) - يتحقق Bob من أن مفتاح Alice الثابت يطابق RouterInfo في الرسالة 3 - يمنع هجمات الرجل في الوسط

### مقاومة تحليل حركة المرور

**إجراءات مضادة لفحص الحزم العميق (DPI):** 1. **تمويه AES:** المفاتيح المؤقتة مشفّرة، وتبدو عشوائية 2. **تمويه الطول باستخدام SipHash:** أطوال الإطارات ليست نصاً عادياً 3. **حشو عشوائي:** أحجام الرسائل متغيرة، بلا أنماط ثابتة 4. **إطارات مشفّرة:** جميع الحمولة مُشفَّرة باستخدام ChaCha20

**منع هجوم إعادة الإرسال:** - التحقق من الطابع الزمني (±60 ثانية) - ذاكرة تخزين مؤقت للإعادة للمفاتيح المؤقتة (مدة الحياة 2*D) - زيادة قيمة Nonce (قيمة فريدة تُستخدم مرة واحدة) تمنع إعادة إرسال الحزم ضمن الجلسة

**مقاومة التحسس:** - مهلات زمنية عشوائية عند فشل AEAD (تشفير موثّق مع بيانات مرتبطة) - قراءة بايتات عشوائية قبل إغلاق الاتصال - عدم إرسال ردود عند فشل المصافحة - حظر عنوان IP عند تكرار حالات الفشل

**إرشادات الحشو:** - الرسائل 1-2: حشو بنص غير مشفّر (مصدَّق) - الرسالة 3+: حشو مُشفَّر داخل إطارات AEAD (التشفير المصادق مع بيانات مرتبطة) - معلمات الحشو المتفق عليها (Options block - حقل الخيارات) - مسموح بإطارات الحشو فقط

### التخفيف من هجمات حجب الخدمة

**حدود الاتصالات:** - الحد الأقصى للاتصالات النشطة (يعتمد على التنفيذ) - الحد الأقصى لعمليات المصافحة المعلقة (مثلًا، 100-1000) - حدود الاتصالات لكل عنوان IP (مثلًا، 3-10 متزامنة)

**حماية الموارد:** - تقييد معدل عمليات DH (مكلفة) - مهلات القراءة لكل مقبس وإجماليًا - حماية من "Slowloris" (هجوم إبقاء اتصالات HTTP مفتوحة ببطء) (حدود زمنية إجمالية) - إدراج عناوين IP في القائمة السوداء بسبب الإساءة

**الرفض السريع:** - عدم تطابق معرّف الشبكة → إغلاق فوري - X25519 point (نقطة على منحنى إهليلجي X25519) غير صالحة → فحص سريع لـMSB قبل فك التشفير - الطابع الزمني خارج النطاق → إغلاق من دون إجراء أي حسابات - فشل AEAD (مصادقة وتشفير مرتبطان بالبيانات) → لا استجابة، تأخير عشوائي

**مقاومة الاستطلاع:** - مهلة عشوائية: 100-500ms (يعتمد على التنفيذ) - قراءة عشوائية: 1KB-64KB (يعتمد على التنفيذ) - لا تُقدَّم معلومات عن الأخطاء إلى المهاجم - الإغلاق عبر TCP RST (بدون مصافحة FIN)

### الأمن التشفيري

**الخوارزميات:** - **X25519**: أمان بمستوى 128-بت، ديفي-هيلمان بمنحنيات إهليلجية (Curve25519) - **ChaCha20**: تشفير تدفقي بمفتاح بطول 256-بت - **Poly1305**: رمز مصادقة الرسائل آمن من منظور نظرية المعلومات - **SHA-256**: مقاومة تصادم 128-بت، ومقاومة صورة أولية 256-بت - **HMAC-SHA256**: دالة عشوائية زائفة (PRF) لاشتقاق المفاتيح

**أحجام المفاتيح:** - مفاتيح ثابتة: 32 بايت (256 بت) - مفاتيح عابرة: 32 بايت (256 بت) - مفاتيح التشفير: 32 بايت (256 بت) - MAC: 16 بايت (128 بت)

**المشكلات المعروفة:** - إعادة استخدام nonce (رقم يُستخدم مرة واحدة) في ChaCha20 كارثية (يُمنَع بزيادة العداد) - تعاني X25519 من مشكلات المجموعات الفرعية الصغيرة (يُخفَّف أثرها عبر التحقق من صحة المنحنى) - SHA-256 مُعرَّض نظرياً لهجوم تمديد الطول (غير قابل للاستغلال في HMAC)

**لا توجد ثغرات معروفة (حتى أكتوبر 2025):** - Noise Protocol Framework (إطار عمل لبناء بروتوكولات قنوات آمنة) خضع لتحليل واسع النطاق - ChaCha20-Poly1305 مُعتمد في TLS 1.3 - X25519 معيار في البروتوكولات الحديثة - لا توجد هجمات عملية على التصميم

## المراجع

### المواصفات الأساسية

- **[مواصفة NTCP2](/docs/specs/ntcp2/)** - المواصفة الرسمية لـ I2P
- **[المقترح 111](/proposals/111-ntcp-2/)** - وثيقة التصميم الأصلية مع المبررات
- **[إطار عمل بروتوكول Noise](https://noiseprotocol.org/noise.html)** - المراجعة 33 (2017-10-04)

### معايير التشفير

- **[RFC 7748](https://www.rfc-editor.org/rfc/rfc7748)** - المنحنيات الإهليلجية للأمن (X25519)
- **[RFC 7539](https://www.rfc-editor.org/rfc/rfc7539)** - ChaCha20 و Poly1305 لبروتوكولات IETF
- **[RFC 8439](https://www.rfc-editor.org/rfc/rfc8439)** - ChaCha20-Poly1305 (يحل محل RFC 7539)
- **[RFC 2104](https://www.rfc-editor.org/rfc/rfc2104)** - HMAC: تجزئة بمفتاح لمصادقة الرسائل
- **[SipHash](https://www.131002.net/siphash/)** - SipHash-2-4 لتطبيقات دوال التجزئة

### المواصفات ذات الصلة بـ I2P

- **[مواصفة I2NP](/docs/specs/i2np/)** - تنسيق رسائل بروتوكول شبكة I2P
- **[البنى المشتركة](/docs/specs/common-structures/)** - تنسيقات RouterInfo و RouterAddress
- **[نقل SSU](/docs/legacy/ssu/)** - نقل UDP (الأصلي، الآن SSU2)
- **[المقترح 147](/proposals/147-transport-network-id-check/)** - فحص معرّف شبكة النقل (0.9.42)

### مراجع التنفيذ

- **[I2P Java](https://github.com/i2p/i2p.i2p)** - التنفيذ المرجعي (Java)
- **[i2pd](https://github.com/PurpleI2P/i2pd)** - تنفيذ بلغة C++
- **[ملاحظات إصدار I2P](/blog/)** - سجل الإصدارات والتحديثات

### السياق التاريخي

- **[Station-To-Station Protocol (STS)](https://en.wikipedia.org/wiki/Station-to-Station_protocol)** - مصدر إلهام لـ Noise framework (إطار للمصافحات التشفيرية)
- **[obfs4](https://gitlab.com/yawning/obfs4)** - Pluggable transport (وسيلة نقل قابلة للإضافة لإخفاء حركة المرور) (سابقة لإخفاء الطول باستخدام SipHash)

## إرشادات التنفيذ

### المتطلبات الإلزامية

**لأغراض الامتثال:**

1. **تنفيذ المصافحة كاملة:**
   - ادعم الرسائل الثلاث جميعًا بسلاسل KDF (دالة اشتقاق المفاتيح) الصحيحة
   - تحقّق من صحة جميع وسوم AEAD (التشفير الموثق مع بيانات مرتبطة)
   - تحقّق من أن نقاط X25519 (خوارزمية لتبادل المفاتيح على منحنى بيضوي) صالحة

2. **تنفيذ مرحلة البيانات:**
   - تمويه طول SipHash (في كلا الاتجاهين)
   - جميع أنواع الكتل: 0 (DateTime)، 1 (Options)، 2 (RouterInfo)، 3 (I2NP)، 4 (Termination)، 254 (Padding)
   - إدارة nonce (عدد يستخدم مرة واحدة) بشكل صحيح (عدادات منفصلة)

3. **ميزات الأمان:**
   - منع إعادة الإرسال (تخزين المفاتيح المؤقتة في الذاكرة لمدة 2*D)
   - التحقق من صحة الطابع الزمني (الافتراضي ±60 ثانية)
   - حشو عشوائي في الرسائل 1-2
   - التعامل مع أخطاء AEAD (تشفير موثَّق مع بيانات مرتبطة) بمهلات زمنية عشوائية

4. **نشر RouterInfo (معلومات router):**
   - نشر المفتاح الثابت ("s")، و IV (متجه التهيئة) ("i")، والإصدار ("v")
   - تدوير المفاتيح وفقًا للسياسة
   - دعم حقل القدرات ("caps") لـ routers المخفية

5. **توافق الشبكة:**
   - دعم حقل معرّف الشبكة (حالياً 2 للشبكة الرئيسية)
   - التشغيل البيني مع تنفيذات Java وi2pd الحالية
   - التعامل مع كل من IPv4 وIPv6

### الممارسات الموصى بها

**تحسين الأداء:**

1. **استراتيجية التخزين المؤقت:**
   - فرّغ الرسائل كاملة دفعة واحدة (الرسائل 1، 2، 3)
   - استخدم TCP_NODELAY لرسائل المصافحة
   - جمّع عدة كتل بيانات في إطارات منفردة
   - حدّد حجم الإطار ببضعة كيلوبايت (لتقليل كمون المستقبِل)

2. **إدارة الاتصالات:**
   - إعادة استخدام الاتصالات كلما أمكن
   - طبّق تجميع الاتصالات
   - راقب صحة الاتصال (DateTime blocks)

3. **إدارة الذاكرة:**
   - تصفير البيانات الحساسة بعد الاستخدام (المفاتيح المؤقتة، نتائج DH)
   - تقييد المصافحات المتزامنة (منع DoS (حجب الخدمة))
   - استخدام مجمعات الذاكرة للتخصيصات المتكررة

**تعزيز الأمان:**

1. **مقاومة الفحص الاستكشافي:**
   - مهلات عشوائية: 100-500ms
   - قراءات بايت عشوائية: 1KB-64KB
   - وضع عناوين IP في القائمة السوداء عند تكرار الإخفاقات
   - عدم تقديم تفاصيل الأخطاء للأقران

2. **حدود الموارد:**
   - الحد الأقصى للاتصالات لكل عنوان IP: 3-10
   - الحد الأقصى لعمليات المصافحة المعلقة: 100-1000
   - مهلات القراءة: 30-60 ثانية لكل عملية
   - المهلة الإجمالية للاتصال: 5 دقائق لمرحلة المصافحة

3. **إدارة المفاتيح:**
   - التخزين الدائم للمفتاح الثابت و IV (المتجه الأوّلي)
   - التوليد العشوائي الآمن (مولّد أرقام عشوائية تشفيرية)
   - الالتزام بسياسات التدوير بصرامة
   - عدم إعادة استخدام المفاتيح المؤقتة مطلقًا

**المراقبة والتشخيص:**

1. **المقاييس:**
   - معدلات نجاح/فشل المصافحة
   - معدلات أخطاء AEAD (تشفير مُصادَق مع بيانات مرتبطة)
   - توزيع انحراف الساعة
   - إحصائيات مدة الاتصال

2. **التسجيل:**
   - سجّل حالات فشل المصافحة مع رموز الأسباب
   - سجّل أحداث انحراف الساعة
   - سجّل عناوين IP المحظورة
   - لا تُسجّل مطلقًا بيانات المفاتيح الحساسة

3. **الاختبار:**
   - اختبارات الوحدات لسلاسل KDF
   - اختبارات التكامل مع تنفيذات أخرى
   - Fuzzing (اختبار الإدخالات العشوائية) لمعالجة الحزم
   - اختبارات التحميل لمقاومة هجمات حجب الخدمة (DoS)

### المزالق الشائعة

**أخطاء حرجة يجب تجنبها:**

1. **إعادة استخدام Nonce (عدد يُستخدم لمرة واحدة):**
   - لا تعِد ضبط عدّاد nonce أثناء الجلسة
   - استخدم عدّادات منفصلة لكل اتجاه
   - أنهِ الجلسة قبل الوصول إلى 2^64 - 1

2. **تدوير المفاتيح:**
   - لا تقم بتدوير المفاتيح مطلقًا أثناء تشغيل router
   - لا تعِد استخدام المفاتيح المؤقتة عبر الجلسات مطلقًا
   - اتبع قواعد الحد الأدنى لوقت التوقف

3. **التعامل مع الطوابع الزمنية:**
   - لا تقبل أبدًا الطوابع الزمنية المنتهية الصلاحية
   - اضبط دائمًا وفقًا لـ RTT (زمن الذهاب والإياب) عند حساب الانحراف
   - قرّب الطوابع الزمنية من نوع DateTime إلى الثواني

4. **أخطاء AEAD (تشفير موثق مع بيانات مرتبطة):**
   - لا تكشف مطلقاً نوع الخطأ للمهاجم
   - استخدم دائماً مهلة عشوائية قبل الإغلاق
   - عامِل الطول غير الصالح كأنه فشل AEAD

5. **الحشو:**
   - لا ترسل الحشو أبداً خارج الحدود المتفق عليها
   - ضع دائماً كتلة الحشو في النهاية
   - لا تستخدم عدة كتل حشو ضمن إطار واحد

6. **RouterInfo (بيانات التعريف الخاصة بـ Router في I2P):**
   - تحقّق دائمًا من تطابق المفتاح الثابت مع RouterInfo
   - لا تقم أبدًا بنشر RouterInfos من دون عناوين منشورة
   - تحقّق دائمًا من صحة التواقيع

### منهجية الاختبار

**اختبارات الوحدات:**

1. **البدائيات التشفيرية:**
   - متجهات اختبار لـ X25519 وChaCha20 وPoly1305 وSHA-256
   - متجهات اختبار لـ HMAC-SHA256
   - متجهات اختبار لـ SipHash-2-4

2. **سلاسل KDF (دالة اشتقاق المفاتيح):**
   - اختبارات الإجابات المعروفة لجميع الرسائل الثلاث
   - التحقق من انتقال مفتاح السلسلة
   - اختبار توليد SipHash IV (متجه التهيئة)

3. **تحليل الرسائل:**
   - فك ترميز الرسائل الصالحة
   - رفض الرسائل غير الصالحة
   - الشروط الحدّية (فارغة، الحجم الأقصى)

**اختبارات التكامل:**

1. **المصافحة:**
   - عملية تبادل بثلاث رسائل ناجحة
   - رفض انحراف الساعة
   - اكتشاف هجوم إعادة الإرسال
   - رفض المفتاح غير الصالح

2. **مرحلة البيانات:**
   - نقل رسائل I2NP
   - تبادل RouterInfo
   - معالجة الحشو
   - رسائل الإنهاء

3. **التشغيل البيني:**
   - اختبار مقابل Java I2P
   - اختبار مقابل i2pd
   - اختبار IPv4 وIPv6
   - اختبار routers المعلنة والمخفية

**اختبارات الأمان:**

1. **الاختبارات السلبية:**
   - علامات AEAD (تشفير موثق مع بيانات مرتبطة) غير صالحة
   - رسائل أُعيد تشغيلها
   - هجمات انحراف الساعة
   - إطارات سيئة التشكيل

2. **اختبارات DoS (حجب الخدمة):**
   - إغراق الاتصالات
   - هجمات Slowloris (إبقاء الاتصال مفتوحاً ببطء)
   - استنزاف وحدة المعالجة المركزية (DH (تبادل المفاتيح Diffie-Hellman) مفرط)
   - استنزاف الذاكرة

3. **Fuzzing (اختبار الإدخال العشوائي):**
   - رسائل مصافحة عشوائية
   - إطارات مرحلة البيانات عشوائية
   - أنواع الكتل وأحجامها عشوائية
   - قيم تشفيرية غير صالحة

### الترحيل من NTCP (بروتوكول النقل عبر TCP الخاص بـ I2P)

**بخصوص دعم NTCP القديم (تمت إزالته الآن):**

أُزيل NTCP (الإصدار 1) في I2P 0.9.50 (مايو 2021). يجب أن تدعم جميع التنفيذات الحالية NTCP2. ملاحظات تاريخية:

1. **الفترة الانتقالية (2018-2021):**
   - 0.9.36: تم تقديم NTCP2 (معطّل افتراضيًا)
   - 0.9.37: تم تمكين NTCP2 افتراضيًا
   - 0.9.40: أُعلن إهمال NTCP
   - 0.9.50: تمت إزالة NTCP

2. **اكتشاف الإصدار:**
   - transportStyle "NTCP" كان يدلّ على أن كلا الإصدارين مدعومان
   - transportStyle "NTCP2" كان يدلّ على دعم NTCP2 فقط
   - اكتشاف تلقائي عبر حجم الرسالة (287 مقابل 288 بايت)

3. **الحالة الحالية:**
   - يتعيّن على جميع routers دعم NTCP2
   - قيمة "NTCP" لـ transportStyle أصبحت متقادمة
   - استخدم قيمة "NTCP2" لـ transportStyle حصراً

## الملحق أ: Noise XK Pattern (نمط المصافحة XK في بروتوكول Noise)

**النمط القياسي لـ Noise XK (ضمن إطار بروتوكول Noise):**

```
XK(s, rs):
  <- s
  ...
  -> e, es
  <- e, ee
  -> s, se
```
**التفسير:**

- `<-` : رسالة من المستجيب (Bob) إلى البادئ (Alice)
- `->` : رسالة من البادئ (Alice) إلى المستجيب (Bob)
- `s` : مفتاح ثابت (مفتاح هوية طويل الأمد)
- `rs` : مفتاح ثابت بعيد (المفتاح الثابت للطرف النظير، معروف مسبقًا)
- `e` : مفتاح مؤقت (خاص بالجلسة، يُولَّد عند الطلب)
- `es` : DH مؤقت-ثابت (ديفي-هيلمان) (مؤقت Alice × ثابت Bob)
- `ee` : DH مؤقت-مؤقت (مؤقت Alice × مؤقت Bob)
- `se` : DH ثابت-مؤقت (ثابت Alice × مؤقت Bob)

**تسلسل الاتفاق على المفاتيح:**

1. **ما قبل الرسالة:** تعرف أليس المفتاح العام الثابت لبوب (من RouterInfo)
2. **الرسالة 1:** ترسل أليس مفتاحًا مؤقتًا، وتجري es DH (تبادل المفاتيح ديفي-هيلمان)
3. **الرسالة 2:** يرسل بوب مفتاحًا مؤقتًا، ويجري ee DH
4. **الرسالة 3:** تكشف أليس عن المفتاح الثابت، وتجري se DH

**خصائص الأمان:**

- تمت مصادقة أليس: نعم (عن طريق الرسالة 3)
- تمت مصادقة بوب: نعم (بامتلاك مفتاح خاص ثابت)
- السرية الأمامية: نعم (تم إتلاف المفاتيح المؤقتة)
- مقاومة KCI (انتحال الهوية بعد اختراق المفتاح): نعم (مستوى المصادقة 2)

## الملحق ب: ترميز Base64

**أبجدية Base64 الخاصة بـ I2P:**

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~
```
**الاختلافات عن Base64 القياسي:** - الرمزان 62-63: `-~` بدلًا من `+/` - الحشو: نفسه (`=`) أو يُحذَف بحسب السياق

**الاستخدام في NTCP2:** - مفتاح ثابت ("s"): 32 بايت → 44 محرف (بدون حشو) - IV (متجه التهيئة) ("i"): 16 بايت → 24 محرف (بدون حشو)

**مثال على الترميز:**

```python
# 32-byte static key (hex): 
# f4489e1bb0597b39ca6cbf5ad9f5f1f09043e02d96cb9aa6a63742b3462429aa

# I2P Base64 encoded:
# 9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=
```
## الملحق C: تحليل التقاط الحزم

**تحديد حركة مرور NTCP2:**

1. **مصافحة TCP:**
   - تسلسل TCP القياسي SYN، SYN-ACK، ACK
   - منفذ الوجهة عادةً 8887 أو ما شابهه

2. **الرسالة 1 (SessionRequest، طلب جلسة):**
   - أول بيانات تطبيق من أليس
   - 80-65535 بايت (عادةً بضع مئات)
   - يبدو عشوائياً (مفتاح مؤقت مُشفّر بـ AES)
   - 287 بايت كحد أقصى عند الاتصال بعنوان "NTCP"

3. **الرسالة 2 (SessionCreated - إنشاء الجلسة):**
   - استجابة من بوب
   - 80-65535 بايت (عادةً بضع مئات)
   - يبدو عشوائياً أيضاً

4. **الرسالة 3 (SessionConfirmed — تأكيد الجلسة):**
   - من أليس
   - 48 بايت + متغير (حجم RouterInfo + الحشو)
   - عادةً 1-4 كيلوبايت

5. **مرحلة البيانات:**
   - إطارات بطول متغير
   - حقل الطول مموه (يبدو عشوائياً)
   - حمولة مشفرة
   - الحشو يجعل الحجم غير متوقع

**مراوغة DPI (فحص الحزم العميق):** - لا رؤوس نصية غير مشفّرة - لا أنماط ثابتة - حقول الطول مموهة - الحشو العشوائي يعطّل الاستدلالات القائمة على الحجم

**مقارنة مع NTCP:** - تكون الرسالة 1 في NTCP دائمًا بحجم 288 بايت (يمكن التعرّف عليها) - يختلف حجم الرسالة 1 في NTCP2 (غير قابلة للتعرّف عليها) - كان لدى NTCP أنماط يمكن التعرّف عليها - تم تصميم NTCP2 لمقاومة DPI (فحص الحزم العميق)

## الملحق د: تاريخ الإصدارات

**المعالم الرئيسية:**

- **0.9.36** (أغسطس 23, 2018): تم تقديم NTCP2، ومعطّل افتراضيًا
- **0.9.37** (أكتوبر 4, 2018): تم تفعيل NTCP2 افتراضيًا
- **0.9.40** (مايو 20, 2019): أصبح NTCP مهملًا
- **0.9.42** (أغسطس 27, 2019): إضافة حقل معرّف الشبكة (الاقتراح 147)
- **0.9.50** (مايو 17, 2021): إزالة NTCP، وإضافة دعم للقدرات
- **2.10.0** (سبتمبر 9, 2025): أحدث إصدار مستقر

**استقرار البروتوكول:** - لا تغييرات كاسرة للتوافق منذ 0.9.50 - تحسينات مستمرة في مقاومة الاستقصاء - تركيز على الأداء والموثوقية - يجري تطوير التشفير ما بعد الكم (غير مفعّل افتراضياً)

**حالة النقل الحالية:** - NTCP2: نقل TCP إلزامي - SSU2: نقل UDP إلزامي - NTCP (v1): أُزيل - SSU (v1): أُزيل
