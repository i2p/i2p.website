---
title: "مواصفة تشفير ECIES-X25519-AEAD-Ratchet (آلية السقاطة الأمنية)"
description: "مخطط التشفير المتكامل بالمنحنى الإهليلجي لـ I2P (X25519 + AEAD (تشفير موثق مع بيانات مرتبطة))"
slug: "ecies"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## نظرة عامة

### الغرض

ECIES-X25519-AEAD-Ratchet (آلية تشفير حديثة من طرف إلى طرف) هو بروتوكول التشفير الحديث من طرف إلى طرف الخاص بـ I2P، ويستبدل نظام ElGamal/AES+SessionTags (منظومة قديمة لتبادل المفاتيح والتشفير باستخدام وسوم الجلسة). يوفر سرية أمامية، وتشفيراً موثقاً، وتحسينات كبيرة في الأداء والأمن.

### أهم التحسينات مقارنةً بـ ElGamal/AES+SessionTags

- **مفاتيح أصغر**: مفاتيح بطول 32 بايت مقابل مفاتيح عامة ElGamal بطول 256 بايت (انخفاض بنسبة 87.5%)
- **السرية الآنية (Forward Secrecy)**: تُتحقق من خلال DH ratcheting (آلية التدرّج) (غير متاحة في البروتوكول القديم)
- **تشفير حديث**: X25519 DH، ChaCha20-Poly1305 AEAD (تشفير موثَّق مرتبط بالبيانات)، SHA-256
- **تشفير موثَّق**: مصادقة مدمجة عبر بنية AEAD
- **بروتوكول ثنائي الاتجاه**: جلسات واردة/صادرة مُقترنة مقابل البروتوكول القديم أحادي الاتجاه
- **وسوم فعّالة**: وسوم جلسة بحجم 8 بايت مقابل وسوم 32 بايت (انخفاض بنسبة 75%)
- **تمويه حركة المرور**: ترميز Elligator2 يجعل المصافحات غير قابلة للتمييز عن البيانات العشوائية

### حالة النشر

- **الإصدار الأولي**: الإصدار 0.9.46 (25 مايو 2020)
- **نشر الشبكة**: مكتمل اعتبارًا من عام 2020
- **الحالة الحالية**: ناضجة، منتشرة على نطاق واسع (أكثر من 5 سنوات في بيئة الإنتاج)
- **دعم router**: يتطلب الإصدار 0.9.46 أو أعلى
- **متطلبات floodfill**: اعتماد يقارب 100% لعمليات الاستعلام المشفرة

### حالة التنفيذ

**مُنفّذ بالكامل:** - رسائل الجلسة الجديدة (NS) مع الربط - رسائل رد الجلسة الجديدة (NSR) - رسائل الجلسة القائمة (ES) - آلية DH ratchet (آلية ترس لتدوير المفاتيح تدريجياً) - آليات ratchet لوسم الجلسة والمفاتيح المتماثلة - كتل DateTime وNextKey وACK وACK Request وGarlic Clove وPadding

**غير مُنفّذة (اعتباراً من الإصدار 0.9.50):** - كتلة MessageNumbers (النوع 6) - كتلة Options (النوع 5) - كتلة Termination (النوع 4) - استجابات تلقائية على مستوى البروتوكول - وضع مفتاح ثابت قيمته صفر - جلسات الإرسال المتعدد

**ملاحظة**: حالة التنفيذ لإصدارات 1.5.0 حتى 2.10.0 (2021-2025) تتطلب التحقق، إذ قد أضيفت بعض الميزات.

---

## أساس البروتوكول

### إطار عمل بروتوكول Noise

يعتمد ECIES-X25519-AEAD-Ratchet (مجموعة تشفير تعتمد على ECIES وX25519 مع AEAD وآلية Ratchet) على [إطار عمل بروتوكول Noise](https://noiseprotocol.org/) (المراجعة 34، 2018-07-11)، وتحديداً نمط المصافحة **IK** (تفاعلي، مفتاح ثابت بعيد معروف) مع امتدادات خاصة بـ I2P.

### مُعرِّف بروتوكول Noise

```
Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256
```
**مكونات المعرّف:** - `Noise` - الإطار الأساسي - `IK` - نمط مصافحة تفاعلي مع مفتاح ثابت معروف للطرف البعيد - `elg2` - ترميز Elligator2 (تقنية إخفاء نقاط المنحنى الإهليلجي) للمفاتيح المؤقتة (امتداد I2P) - `+hs2` - يتم استدعاء MixHash قبل الرسالة الثانية لمزج الوسم (امتداد I2P) - `25519` - دالة X25519 لـ Diffie-Hellman - `ChaChaPoly` - خوارزمية تشفير AEAD ChaCha20-Poly1305 - `SHA256` - دالة تجزئة SHA-256

### نمط المصافحة في Noise

**ترميز نمط IK:**

```
<- s                    (Bob's static key known to Alice)
...
-> e, es, s, ss         (Alice sends ephemeral, DH es, static key, DH ss)
<- e, ee, se            (Bob sends ephemeral, DH ee, DH se)
```
**معاني الرموز:** - `e` - نقل المفتاح المؤقت - `s` - نقل المفتاح الثابت - `es` - DH (تبادل المفاتيح ديفي-هيلمان) بين مفتاح أليس المؤقت ومفتاح بوب الثابت - `ss` - DH بين مفتاح أليس الثابت ومفتاح بوب الثابت - `ee` - DH بين مفتاح أليس المؤقت ومفتاح بوب المؤقت - `se` - DH بين مفتاح بوب الثابت ومفتاح أليس المؤقت

### خصائص الأمان في Noise (إطار عمل لبروتوكولات تبادل المفاتيح)

باستخدام مصطلحات Noise (إطار بروتوكول لتأسيس جلسات مشفّرة)، يوفّر نمط IK (نمط مصافحة في Noise):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Authentication Level</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Confidentiality Level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;1 (NS)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;1 (sender auth, KCI vulnerable)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;2 (NSR)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;4 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transport (ES)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;5 (strong forward secrecy)</td>
    </tr>
  </tbody>
</table>
**مستويات المصادقة:** - **المستوى 1**: يتم توثيق الحمولة على أنها تعود إلى مالك المفتاح الثابت الخاص بالمرسل، لكنها تظل عرضة لهجوم Key Compromise Impersonation (KCI؛ انتحال الهوية نتيجة اختراق المفتاح) - **المستوى 2**: مقاومة لهجمات KCI بعد NSR (إعادة تهيئة الجلسة)

**مستويات السرية:** - **المستوى 2**: سرية أمامية إذا تم اختراق المفتاح الثابت للمرسل لاحقاً - **المستوى 4**: سرية أمامية إذا تم اختراق المفتاح المؤقت للمرسل لاحقاً - **المستوى 5**: سرية أمامية تامة بعد حذف كلا المفتاحين المؤقتين

### الاختلافات بين IK و XK

يختلف نمط IK عن نمط XK المستخدم في NTCP2 وSSU2:

1. **أربع عمليات DH (تبادل المفاتيح ديفي‑هيلمان)**: يستخدم IK أربع عمليات DH (es، ss، ee، se) مقابل ثلاث لـ XK
2. **المصادقة الفورية**: تتم مصادقة Alice في الرسالة الأولى (المستوى 1 للمصادقة)
3. **سرية مستقبلية أسرع**: تتحقق السرية المستقبلية الكاملة (المستوى 5) بعد الرسالة الثانية (1‑RTT، رحلة ذهاب وإياب واحدة)
4. **المفاضلة**: حمولة الرسالة الأولى غير محمية بالسرية المستقبلية (على عكس XK حيث تكون جميع الحمولات محمية بالسرية المستقبلية)

**الخلاصة**: يتيح IK إيصال استجابة Bob خلال ذهاب وإياب واحد (1-RTT) مع سرية أمامية كاملة، لكن على حساب أن الطلب الأولي لا يتمتع بسرية أمامية.

### مفاهيم Signal Double Ratchet (آلية تدوير المفاتيح المزدوجة)

تتضمّن ECIES (نظام تشفير متكامل قائم على المنحنيات البيضوية) مفاهيم من [خوارزمية Signal Double Ratchet](https://signal.org/docs/specifications/doubleratchet/):

- **DH Ratchet** (آلية تدوير مفاتيح تعتمد على DH): يوفّر السرّية المستقبلية عبر تبادل مفاتيح DH جديدة بشكل دوري
- **Symmetric Key Ratchet** (آلية تدوير لمفاتيح التشفير المتماثلة): يشتق مفاتيح جلسة جديدة لكل رسالة
- **Session Tag Ratchet** (آلية تدوير لوسوم الجلسة): يولّد وسوم جلسة للاستخدام لمرة واحدة بشكل حتمي

**أهم الفروقات عن Signal:** - **ratcheting أقل تكرارًا**: يقوم I2P بالـ ratcheting فقط عند الحاجة (ratcheting: آلية تحديث المفاتيح تدريجية) مثل قرب نفاد الوسوم أو وفق السياسة - **وسوم الجلسة (Session Tags) بدلًا من تشفير الرؤوس**: يستخدم وسومًا حتمية بدلًا من رؤوس مُشفّرة - **ACKs صريحة**: يستخدم كتل ACK ضمن القناة (in-band) بدل الاعتماد فقط على حركة المرور العكسية (ACKs: إقرارات استلام) - **ratchets منفصلة للوسوم والمفاتيح**: أكثر كفاءةً لدى المستقبِل (يمكنه تأجيل حساب المفتاح)

### امتدادات I2P لـ Noise (إطار بروتوكولات للتبادل الآمن)

1. **ترميز Elligator2** (خوارزمية ترميز تُخفي المفاتيح لتبدو عشوائية): مفاتيح مؤقتة مُرمَّزة بحيث لا يمكن تمييزها عن العشوائي
2. **علامة مُضافة قبل NSR**: إضافة علامة الجلسة قبل رسالة NSR لأغراض الترابط
3. **تنسيق حمولة محدد**: بنية حمولة قائمة على الكتل لجميع أنواع الرسائل
4. **تغليف I2NP**: جميع الرسائل مُغلّفة ضمن رؤوس I2NP Garlic Message
5. **مرحلة بيانات منفصلة**: رسائل النقل (ES) تختلف عن مرحلة بيانات Noise القياسية

---

## البدائيات التشفيرية

### ديفي-هيلمان X25519

**المواصفة**: [RFC 7748](https://tools.ietf.org/html/rfc7748)

**الخصائص الرئيسية:** - **حجم المفتاح الخاص**: 32 بايت - **حجم المفتاح العام**: 32 بايت - **حجم السر المشترك**: 32 بايت - **Endianness (نظام ترتيب البايتات)**: Little-endian - **المنحنى**: Curve25519

**العمليات:**

### X25519 GENERATE_PRIVATE()

ينشئ مفتاح خاص عشوائي بطول 32 بايت:

```
privkey = CSRNG(32)
```
### X25519 DERIVE_PUBLIC(privkey)

يشتق المفتاح العام المقابل:

```
pubkey = curve25519_scalarmult_base(privkey)
```
يُرجع مفتاحًا عامًا بطول 32 بايت بترتيب little-endian (حيث تكون البايت الأقل أهمية أولًا).

### X25519 DH(privkey, pubkey)

ينفّذ اتفاق المفاتيح Diffie-Hellman:

```
sharedSecret = curve25519_scalarmult(privkey, pubkey)
```
يُرجِع سرًا مشتركًا بطول 32 بايت.

**ملاحظة أمنية**: يجب على المنفذين التحقق من أن السر المشترك ليس كله أصفاراً (مفتاح ضعيف). ارفضوا وألغوا المصافحة إذا حدث ذلك.

### ChaCha20-Poly1305 AEAD (تشفير مصادق مع بيانات مصاحبة)

**المواصفة**: [RFC 7539](https://tools.ietf.org/html/rfc7539) القسم 2.8

**المعلمات:** - **حجم المفتاح**: 32 بايت (256 بت) - **حجم Nonce (رقم يستخدم مرة واحدة)**: 12 بايت (96 بت) - **حجم MAC**: 16 بايت (128 بت) - **حجم الكتلة**: 64 بايت (داخلي)

**تنسيق الـ Nonce (عدد يُستخدم مرة واحدة):**

```
Byte 0-3:   0x00 0x00 0x00 0x00  (always zero)
Byte 4-11:  Little-endian counter (message number N)
```
**بناء AEAD (التشفير الموثّق مع بيانات مرتبطة):**

يجمع AEAD (تشفير مُصادَق مع بيانات إضافية) بين خوارزمية التشفير التدفقي ChaCha20 وخوارزمية Poly1305 للمصادقة (MAC):

1. ولّد تيار المفتاح ChaCha20 من المفتاح وnonce (عدد يُستخدم مرة واحدة)
2. شفّر النص الصريح عبر XOR (أو "أو الحصرية") مع تيار المفتاح
3. احسب MAC من نوع Poly1305 على (البيانات المرتبطة || النص المُشفَّر)
4. ألحِق MAC بطول 16 بايت بالنص المُشفَّر

### ChaCha20-Poly1305 (خوارزمية AEAD: تشفير مصادق ببيانات مرتبطة) تشفير(k, n, plaintext, ad)

يشفّر النص الصريح مع المصادقة:

```python
# Inputs
k = 32-byte cipher key
n = 12-byte nonce (first 4 bytes zero, last 8 bytes = message number)
plaintext = data to encrypt (0 to 65519 bytes)
ad = associated data (optional, used in MAC calculation)

# Output
ciphertext = chacha20_encrypt(k, n, plaintext)
mac = poly1305(ad || ciphertext, poly1305_key_gen(k, n))
return ciphertext || mac  # Total length = len(plaintext) + 16
```
**الخصائص:** - النص المُعمّى بطولٍ مساوٍ للنص الصريح (تعمية تيارية) - المخرَج يساوي plaintext_length + 16 بايت (يتضمن MAC (رمز التوثيق)) - المخرَج بأكمله لا يمكن تمييزه عن بيانات عشوائية إذا كان المفتاح سرياً - MAC يوفّر التوثيق لكلٍّ من البيانات المرتبطة والنص المُعمّى

### ChaCha20-Poly1305 فك التشفير(k, n, ciphertext, ad)

يفكّ التشفير ويتحقق من المصادقة:

```python
# Split ciphertext and MAC
ct_without_mac = ciphertext[0:-16]
received_mac = ciphertext[-16:]

# Verify MAC
expected_mac = poly1305(ad || ct_without_mac, poly1305_key_gen(k, n))
if not constant_time_compare(received_mac, expected_mac):
    raise AuthenticationError("MAC verification failed")

# Decrypt
plaintext = chacha20_decrypt(k, n, ct_without_mac)
return plaintext
```
**متطلبات أمنية حرجة:** - يجب أن تكون Nonces (عدد يُستخدم مرة واحدة) فريدة لكل رسالة مع نفس المفتاح - يجب ألا يُعاد استخدام Nonces (فشل كارثي إذا أُعيد استخدامها) - يجب أن يستخدم التحقق من رمز مصادقة الرسالة (MAC) مقارنة بزمن ثابت لمنع هجمات التوقيت - يجب أن يؤدي فشل التحقق من MAC إلى رفض الرسالة بالكامل (من دون أي فك تشفير جزئي)

### دالة التجزئة SHA-256

**المواصفة**: NIST FIPS 180-4

**الخصائص:** - **حجم المخرجات**: 32 بايت (256 بت) - **حجم الكتلة**: 64 بايت (512 بت) - **مستوى الأمان**: 128 بت (مقاومة التصادم)

**العمليات:**

### SHA-256 H(p, d)

تجزئة SHA-256 مع سلسلة تخصيص:

```
H(p, d) := SHA256(p || d)
```
حيث يرمز `||` إلى عملية الربط، و`p` هي سلسلة التخصيص، و`d` هي البيانات.

### SHA-256 MixHash(d)

يحدّث قيمة التجزئة الجارية بالبيانات الجديدة:

```
h = SHA256(h || d)
```
يُستخدم طوال Noise handshake (بروتوكول المصافحة ضمن إطار Noise) للحفاظ على تجزئة سجل المصافحة.

### اشتقاق المفاتيح باستخدام HKDF (دالة لاشتقاق المفاتيح المعتمدة على HMAC)

**المواصفة**: [RFC 5869](https://tools.ietf.org/html/rfc5869)

**الوصف**: دالة اشتقاق مفاتيح مبنية على HMAC باستخدام SHA-256

**المعلمات:** - **دالة التجزئة**: HMAC-SHA256 - **طول الملح**: حتى 32 بايت (حجم خرج SHA-256) - **طول الخرج**: متغير (حتى 255 * 32 بايت)

**دالة HKDF (دالة اشتقاق مفاتيح مبنية على HMAC):**

```python
def HKDF(salt, ikm, info, length):
    """
    Args:
        salt: Salt value (32 bytes max for SHA-256)
        ikm: Input key material (any length)
        info: Context-specific info string
        length: Desired output length in bytes
    
    Returns:
        output: Derived key material (length bytes)
    """
    # Extract phase
    prk = HMAC-SHA256(salt, ikm)
    
    # Expand phase
    n = ceil(length / 32)
    t = b''
    okm = b''
    for i in range(1, n + 1):
        t = HMAC-SHA256(prk, t || info || byte(i))
        okm = okm || t
    
    return okm[0:length]
```
**أنماط الاستخدام الشائعة:**

```python
# Generate two keys (64 bytes total)
keydata = HKDF(chainKey, sharedSecret, "KDFDHRatchetStep", 64)
nextRootKey = keydata[0:31]
chainKey = keydata[32:63]

# Generate session tag (8 bytes)
tagdata = HKDF(chainKey, CONSTANT, "SessionTagKeyGen", 64)
nextChainKey = tagdata[0:31]
sessionTag = tagdata[32:39]

# Generate symmetric key (32 bytes)
keydata = HKDF(chainKey, ZEROLEN, "SymmetricRatchet", 64)
nextChainKey = keydata[0:31]
sessionKey = keydata[32:63]
```
**سلاسل المعلومات المستخدمة في ECIES:** - `"KDFDHRatchetStep"` - اشتقاق مفتاح DH ratchet (آلية السقاطة) - `"TagAndKeyGenKeys"` - تهيئة مفاتيح سلسلتي الوسوم والمفاتيح - `"STInitialization"` - تهيئة ratchet لوسم الجلسة - `"SessionTagKeyGen"` - توليد وسم الجلسة - `"SymmetricRatchet"` - توليد مفاتيح متناظرة - `"XDHRatchetTagSet"` - مفتاح مجموعة وسوم DH ratchet - `"SessionReplyTags"` - توليد مجموعة وسوم NSR - `"AttachPayloadKDF"` - اشتقاق مفتاح حمولة NSR

### ترميز Elligator2 (مخطط ترميز لإخفاء مفاتيح المنحنيات الإهليلجية)

**الغرض**: ترميز المفاتيح العامة لـ X25519 بحيث تكون غير قابلة للتمييز عن سلاسل عشوائية موزعة توزيعاً منتظماً بطول 32 بايت.

**المواصفة**: [ورقة Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf)

**المشكلة**: تمتلك مفاتيح X25519 (خوارزمية لتبادل المفاتيح على منحنى Curve25519) العامة القياسية بنية يمكن التعرف عليها. يمكن للمراقب تمييز رسائل المصافحة برصد هذه المفاتيح، حتى لو كان المحتوى مُشفّراً.

**الحل**: يوفّر Elligator2 تقابلاً بين ~50% من مفاتيح X25519 العامة الصالحة وسلاسل بطول 254 بت تبدو عشوائية.

**توليد المفاتيح باستخدام Elligator2 (تقنية لتمويه شكل المفاتيح العامة لتبدو عشوائية):**

### Elligator2 GENERATE_PRIVATE_ELG2()

ينشئ مفتاحاً خاصاً يقابل مفتاحاً عاماً قابلاً للترميز باستخدام Elligator2 (خوارزمية لتمثيل المفاتيح العامة بشكل غير قابل للتمييز):

```python
while True:
    privkey = CSRNG(32)
    pubkey = DERIVE_PUBLIC(privkey)
    
    # Test if public key is Elligator2-encodable
    try:
        encoded = ENCODE_ELG2(pubkey)
        # Success - this key pair is suitable
        return privkey
    except NotEncodableError:
        # Try again with new random key
        continue
```
**مهم**: تقريباً 50٪ من المفاتيح الخاصة المُولَّدة عشوائياً ستنتج مفاتيح عامة غير قابلة للترميز. يجب التخلص منها ومحاولة التوليد من جديد.

**تحسين الأداء**: أنشئ المفاتيح مسبقاً في خيط يعمل في الخلفية للحفاظ على مجمّع من أزواج مفاتيح ملائمة، وتجنّب التأخيرات أثناء المصافحة.

### Elligator2 ENCODE_ELG2(pubkey)

يرمّز مفتاحًا عامًا إلى 32 بايت تبدو عشوائية:

```python
def ENCODE_ELG2(pubkey):
    """
    Encodes X25519 public key using Elligator2.
    
    Args:
        pubkey: 32-byte X25519 public key (little-endian)
    
    Returns:
        encoded: 32-byte encoded key indistinguishable from random
    
    Raises:
        NotEncodableError: If pubkey cannot be encoded
    """
    # Perform Elligator2 representative calculation
    # Returns 254-bit value (31.75 bytes)
    encodedKey = elligator2_encode(pubkey)
    
    # Add 2 random bits to MSB to make full 32 bytes
    randomByte = CSRNG(1)
    encodedKey[31] |= (randomByte & 0xc0)
    
    return encodedKey
```
**تفاصيل الترميز:** - Elligator2 (خوارزمية ترميز) تنتج 254 بت (ليست 256 كاملة) - أعلى بتّين من البايت 31 عبارة عن حشو عشوائي - تكون النتيجة موزعة توزيعاً منتظماً على مساحة من 32 بايت - ينجح في ترميز ما يقارب 50% من مفاتيح X25519 العامة الصالحة (خوارزمية تبادل مفاتيح على المنحنى البيضوي)

### Elligator2 (خوارزمية إخفاء التمثيل على المنحنى الإهليلجي - الإصدار 2) DECODE_ELG2(encodedKey)

يُعاد فك الترميز إلى المفتاح العام الأصلي:

```python
def DECODE_ELG2(encodedKey):
    """
    Decodes Elligator2-encoded key back to X25519 public key.
    
    Args:
        encodedKey: 32-byte encoded key
    
    Returns:
        pubkey: 32-byte X25519 public key (little-endian)
    """
    # Mask out 2 random padding bits from MSB
    encodedKey[31] &= 0x3f
    
    # Perform Elligator2 representative inversion
    pubkey = elligator2_decode(encodedKey)
    
    return pubkey
```
**خصائص الأمان:** - المفاتيح المُرمَّزة غير قابلة للتمييز حسابيًا عن البايتات العشوائية - لا يمكن لأي اختبار إحصائي اكتشاف المفاتيح المُرمَّزة بـ Elligator2 (خوارزمية ترميز تُخفي المفاتيح لتبدو كبيانات عشوائية) بشكل موثوق - فك الترميز حتمي (المفتاح المُرمَّز نفسه يُنتج دائمًا المفتاح العام نفسه) - الترميز تقابلي بالنسبة لنحو ~50% من المفاتيح في المجموعة الفرعية القابلة للترميز

**ملاحظات التنفيذ:** - خزّن المفاتيح المرمَّزة في مرحلة التوليد لتجنّب إعادة الترميز أثناء المصافحة - يمكن استخدام المفاتيح غير المناسبة الناتجة عن توليد Elligator2 (خوارزمية تمويه نقاط المنحنيات الإهليلجية) مع NTCP2 (الذي لا يتطلب Elligator2) - يُعدّ توليد المفاتيح في الخلفية أساسيًا للأداء - يتضاعف متوسط زمن التوليد بسبب معدل رفض يبلغ 50%

---

## تنسيقات الرسائل

### نظرة عامة

تعرّف ECIES (مخطط التشفير المتكامل بالمنحنيات الإهليلجية) ثلاثة أنواع من الرسائل:

1. **جلسة جديدة (NS)**: رسالة المصافحة الأولية من Alice إلى Bob
2. **رد الجلسة الجديدة (NSR)**: رد المصافحة من Bob إلى Alice
3. **جلسة قائمة (ES)**: جميع الرسائل اللاحقة في كلا الاتجاهين

تُغلَّف جميع الرسائل بصيغة I2NP Garlic Message (صيغة رسالة I2NP من نوع Garlic) مع طبقات تشفير إضافية.

### حاوية رسالة Garlic (تقنية تجميع الرسائل في I2P) الخاصة بـ I2NP

تُغلَّف جميع رسائل ECIES (مخطط تشفير متكامل يعتمد على المنحنيات الإهليلجية) ضمن رؤوس I2NP Garlic Message القياسية:

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
```
**الحقول:** - `type`: 0x26 (Garlic Message، رسالة Garlic في I2P) - `msg_id`: معرّف رسالة I2NP بطول 4 بايت - `expiration`: طابع زمني Unix بطول 8 بايت (بالميلي ثانية) - `size`: حجم الحمولة بطول 2 بايت - `chks`: مجموع تحقق بطول 1 بايت - `length`: طول البيانات المشفّرة بطول 4 بايت - `encrypted data`: حمولة مشفّرة بـ ECIES

**الغرض**: يوفّر تعريف الرسائل وتوجيهها على طبقة I2NP. يتيح حقل `length` للمستلمين معرفة الحجم الإجمالي للحمولة المشفّرة.

### رسالة جلسة جديدة (NS)

تبدأ رسالة New Session جلسة جديدة من Alice إلى Bob. وتأتي بثلاثة أنواع:

1. **مع الربط** (1b): يتضمن المفتاح الثابت الخاص بـ Alice للاتصال ثنائي الاتجاه
2. **من دون ربط** (1c): يستبعد المفتاح الثابت للاتصال أحادي الاتجاه
3. **أحادي الاستخدام** (1d): نمط رسالة واحدة من دون إنشاء جلسة

### رسالة NS مع ربط (النوع 1b)

**حالة الاستخدام**: التدفق، datagrams (وحدات بيانات شبكية مستقلة) قابلة للرد، أي بروتوكول يتطلب ردودًا

**الطول الإجمالي**: 96 + payload_length بايت

**التنسيق**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         Static Key Section            +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+    (MAC) for Static Key Section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**تفاصيل الحقل:**

**المفتاح العام المؤقت** (32 بايت، نص واضح [غير مُشفَّر]): - المفتاح العام X25519 أحادي الاستخدام الخاص بأليس - مُرمَّز باستخدام Elligator2 (غير قابل للتمييز عن العشوائيّة) - يُولَّد جديدًا لكل رسالة NS (لا يُعاد استخدامه إطلاقًا) - بصيغة little-endian (ترتيب البايتات من الأقل أهمية إلى الأكثر)

**قسم المفتاح الثابت** (32 بايت مُشفَّرة، 48 بايت مع MAC): - يتضمن المفتاح العمومي الثابت X25519 الخاص بـ Alice (32 بايت) - مُشفَّر باستخدام ChaCha20 - مُوثَّق عبر Poly1305 MAC (16 بايت) - يُستخدم من قبل Bob لربط الجلسة بوجهة Alice

**قسم الحمولة** (مشفّر بطول متغير، +16 بايت MAC): - يحتوي على garlic cloves (كتل بيانات ضمن garlic encryption) وكتل أخرى - يجب أن يتضمن كتلة DateTime كأول كتلة - يتضمن عادةً كتل Garlic Clove مع بيانات التطبيق - قد يتضمن كتلة NextKey من أجل ratchet (آلية تدوير المفاتيح التقدّمية) فوري - يُشفّر باستخدام ChaCha20 - مُوثَّق بواسطة Poly1305 MAC (16 بايت)

**خصائص الأمان:** - يوفر المفتاح المؤقت مكوّن السرية الأمامية - يثبت المفتاح الثابت هوية Alice (مقترنة بالوجهة) - يحتوي كلا الجزأين على رموز مصادقة الرسائل (MACs) منفصلة لفصل المجالات - تُجري المصافحة إجمالًا عمليتي ديفي-هيلمان (DH) (es, ss)

### رسالة NS بدون ربط (Type 1c)

**حالة الاستخدام**: داتاغرامات خام حيث لا يُتوقع أو لا يُرغب في ردّ

**الطول الإجمالي**: 96 + payload_length بايت

**التنسيق**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|           All zeros                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**الاختلاف الرئيسي**: قسم Flags (قسم الأعلام) يحتوي على 32 بايت من الأصفار بدلاً من مفتاح ثابت.

**التعرّف**: يحدّد بوب نوع الرسالة بفك تشفير القسم المكوّن من 32 بايت والتحقق مما إذا كانت جميع البايتات أصفاراً: - جميعها أصفار → جلسة غير مربوطة (type 1c) - ليست كلها أصفاراً → جلسة مربوطة بمفتاح ثابت (type 1b)

**الخصائص:** - عدم وجود مفتاح ثابت يعني عدم الارتباط بوجهة أليس - لا يمكن لبوب إرسال ردود (لا وجهة معروفة) - يُجري عملية DH (ديفي-هيلمان) واحدة فقط (es) - يتبع نمط Noise "N" بدلاً من "IK" - أكثر كفاءة عندما لا تكون الردود مطلوبة أبداً

**قسم الأعلام** (محجوز للاستخدام مستقبلاً): حاليًا جميعها أصفار. قد تُستخدم للتفاوض على الميزات في الإصدارات المستقبلية.

### رسالة NS لمرة واحدة (النوع 1d)

**حالة الاستخدام**: رسالة مجهولة واحدة دون جلسة أو توقع رد

**الطول الإجمالي**: 96 + payload_length بايت

**التنسيق**: مطابق لـ NS من دون ربط (النوع 1c)

**تمييز**:  - قد يرسل Type 1c عدة رسائل في الجلسة نفسها (تتبعها رسائل ES) - يرسل Type 1d رسالة واحدة فقط من دون إنشاء جلسة - عملياً، قد تتعامل عمليات التنفيذ معهما بوصفهما متماثلتين في البداية

**الخصائص:** - أقصى قدر من إخفاء الهوية (لا مفتاح ثابت، ولا جلسة) - لا يحتفظ أي من الطرفين بأي حالة للجلسة - يتبع نمط Noise "N" (بروتوكول Noise) - عملية DH واحدة (تبادُل ديفي-هيلمان) (es)

### رسالة رد جلسة جديدة (NSR)

يرسل Bob رسالة NSR واحدة أو أكثر استجابةً لرسالة NS الخاصة بـ Alice. تُكمِل NSR مصافحة Noise IK (نمط IK ضمن بروتوكول Noise) وتؤسّس جلسة ثنائية الاتجاه.

**الطول الإجمالي**: 72 + payload_length بايت

**التنسيق**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+        Ephemeral Public Key           +
|                                       |
+            32 bytes                   +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+  (MAC) for Key Section (empty)        +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**تفاصيل الحقل:**

**وسم الجلسة** (8 بايت، نص غير مُشفّر): - مُولَّد من مجموعة علامات NSR (انظر أقسام KDF) - يربط هذا الرد برسالة NS الخاصة بأليس - يتيح لأليس تحديد أي NS يستجيب له هذا الـ NSR - استخدام لمرة واحدة (لا يُعاد استخدامه)

**مفتاح عام مؤقت** (32 بايت، نص صريح): - المفتاح العام X25519 الخاص بـ Bob للاستخدام لمرة واحدة - مُرمَّز باستخدام Elligator2 - يُولَّد حديثًا لكل رسالة NSR (نوع رسالة) - ويجب أن يكون مختلفًا لكل NSR تُرسَل

**Key Section MAC** (رمز التحقق من الرسالة لقسم المفاتيح) (16 بايت): - يوثق بيانات فارغة (ZEROLEN) - جزء من بروتوكول Noise IK (نمط se) - يستخدم سجل التجزئة كبيانات مرتبطة - حاسم لربط NSR بـ NS

**قسم الحمولة** (طول متغير): - يحتوي على garlic cloves (وحدات رسائل garlic ضمن I2P) وكتل - يتضمن عادةً ردود طبقة التطبيق - قد يكون فارغًا (NSR يقتصر على ACK) - الحد الأقصى للحجم: 65519 بايت (65535 - 16 بايت MAC)

**رسائل NSR متعددة:**

قد يرسل Bob عدة رسائل NSR استجابةً لرسالة NS واحدة:
- لكل NSR مفتاح مؤقت فريد
- لكل NSR وسم جلسة فريد
- تستخدم Alice أول NSR يتم استلامه لإتمام المصافحة
- تُعد رسائل NSR الأخرى لأغراض التكرار (في حال فقدان الحزم)

**التوقيت الحرج:** - يجب أن تتلقى أليس NSR واحدة قبل إرسال رسائل ES - يجب أن يتلقى بوب رسالة ES واحدة قبل إرسال رسائل ES - تنشئ NSR مفاتيح جلسة ثنائية الاتجاه عبر عملية split()

**خصائص الأمان:** - يُتمّ Noise IK handshake (نمط IK للمصافحة في بروتوكول Noise) - يُجري عمليتين إضافيتين من DH (تبادل المفاتيح ديفي-هيلمان) (ee, se) - إجمالي 4 عمليات DH عبر NS+NSR (اختصاران تقنيان لرسائل/مراحل محددة في هذا السياق) - يحقق المصادقة المتبادلة (المستوى 2) - يوفر سرية أمامية ضعيفة (المستوى 4) لحمولة NSR

### رسالة جلسة قائمة (ES)

تستخدم جميع الرسائل بعد مصافحة NS/NSR تنسيق Existing Session (جلسة قائمة). تُستخدم رسائل ES في كلا الاتجاهين من قبل كلٍ من Alice وBob.

**الطول الإجمالي**: 8 + payload_length + 16 بايت (الحد الأدنى 24 بايت)

**التنسيق**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**تفاصيل الحقل:**

**وسم الجلسة** (8 بايت، نص غير مُشفَّر): - مُولَّد من مجموعة الوسوم الصادرة الحالية - يُعرّف الجلسة ورقم الرسالة - يبحث المستقبِل عن الوسم للعثور على مفتاح الجلسة والـ nonce (عدد عشوائي يُستخدم مرة واحدة) - للاستخدام لمرة واحدة (يُستخدم كل وسم مرة واحدة فقط) - التنسيق: أول 8 بايت من خرج HKDF (دالة اشتقاق مفاتيح مبنية على HMAC)

**قسم الحمولة** (طول متغير): - يحتوي على garlic cloves وكتل - لا توجد كتل مطلوبة (قد يكون فارغًا) - الكتل الشائعة: Garlic Clove, NextKey, ACK, ACK Request, Padding - الحجم الأقصى: 65519 بايت (65535 - MAC بطول 16 بايت)

**MAC** (رمز تحقق الرسائل) (16 بايت): - وسم مصادقة Poly1305 - يُحسَب على كامل الحمولة - البيانات المرتبطة: وسم الجلسة بطول 8 بايت - يجب التحقق منه بشكل صحيح، وإلا ستُرفَض الرسالة

**عملية الاستعلام عن الوسم:**

1. يقوم المستقبِل باستخراج وسم بطول 8 بايت
2. يبحث عن الوسم في جميع مجموعات الوسوم الواردة الحالية
3. يسترجع مفتاح الجلسة المرتبط ورقم الرسالة N
4. ينشئ nonce (عدد يُستخدم مرة واحدة): `[0x00, 0x00, 0x00, 0x00, N (8 bytes little-endian)]`
5. يفك تشفير الحمولة باستخدام AEAD (تشفير مصادق مع بيانات مرتبطة) مع اعتبار الوسم بيانات مرتبطة
6. يزيل الوسم من مجموعة الوسوم (استخدام لمرة واحدة)
7. يعالج الكتل المفكوك تشفيرها

**تعذّر العثور على Session Tag (وسم الجلسة):**

إذا لم يُعثر على الوسم في أي مجموعة وسوم: - قد تكون رسالة NS (اختصار لبروتوكول Noise Session) → محاولة فك تشفير NS - قد تكون رسالة NSR (رد Noise Session) → محاولة فك تشفير NSR - قد تكون ES (جلسة ElGamal) خارج الترتيب → الانتظار قليلًا لتحديث مجموعة الوسوم - قد يكون هجوم إعادة الإرسال → الرفض - قد تكون بيانات تالفة → الرفض

**حمولة فارغة:**

قد تكون لرسائل ES حمولات فارغة (0 بايت):
- تعمل كـ ACK (تأكيد استلام) صريح عند استقبال طلب ACK
- توفر استجابة على مستوى البروتوكول دون بيانات التطبيق
- لا تزال تستهلك session tag (وسم الجلسة)
- مفيدة عندما لا تكون لدى الطبقة الأعلى بيانات فورية لإرسالها

**خصائص الأمان:** - سرية أمامية كاملة (المستوى 5) بعد استلام NSR - تشفير مُصادَق عبر AEAD (تشفير مصادق مع بيانات مرتبطة) - يعمل الوسم كبيانات مرتبطة إضافية - حد أقصى 65535 رسالة لكل مجموعة وسوم قبل الحاجة إلى ratchet (آلية تدوير المفاتيح)

---

## دوال اشتقاق المفاتيح

يوثّق هذا القسم جميع عمليات اشتقاق المفاتيح (KDF) المستخدمة في ECIES، مبيّناً الاشتقاقات التشفيرية كاملةً.

### الاصطلاحات والثوابت

**الثوابت:** - `ZEROLEN` - مصفوفة بايت بطول صفري (سلسلة فارغة) - `||` - عامل الربط

**المتغيرات:** - `h` - الهاش التراكمي لسجل الرسائل (32 بايت) - `chainKey` - مفتاح التسلسل لـ HKDF (وظيفة اشتقاق مفتاح عبر دالة هاش) (32 بايت) - `k` - مفتاح تشفير متماثل (32 بايت) - `n` - Nonce (عدد يُستخدم لمرة واحدة) / رقم الرسالة

**المفاتيح:** - `ask` / `apk` - المفتاح الخاص/العام الثابت لأليس - `aesk` / `aepk` - المفتاح الخاص/العام المؤقت لأليس - `bsk` / `bpk` - المفتاح الخاص/العام الثابت لِبوب - `besk` / `bepk` - المفتاح الخاص/العام المؤقت لِبوب

### دوال اشتقاق المفاتيح لرسائل NS

### دالة اشتقاق المفاتيح 1: المفتاح الابتدائي للسلسلة

يُجرى مرة واحدة عند تهيئة البروتوكول (يمكن حسابه مسبقًا):

```python
# Protocol name (40 bytes, ASCII, no null termination)
protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"

# Initialize hash
h = SHA256(protocol_name)

# Initialize chaining key
chainKey = h

# MixHash with empty prologue
h = SHA256(h)

# State: chainKey and h initialized
# Can be precalculated for all outbound sessions
```
**النتيجة:** - `chainKey` = مفتاح السلسلة الابتدائي لجميع KDFs (دوال اشتقاق المفاتيح) اللاحقة - `h` = سجل التجزئة الابتدائي

### KDF 2: مزج المفتاح الثابت لبوب

ينفذ Bob هذا مرة واحدة (يمكن حسابه مسبقًا لجميع الجلسات الواردة):

```python
# Bob's static keys (published in LeaseSet)
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

# Mix Bob's public key into hash
h = SHA256(h || bpk)

# State: h updated with Bob's identity
# Can be precalculated by Bob for all inbound sessions
```
### KDF (دالة اشتقاق المفاتيح) 3: توليد المفتاح المؤقت لأليس

تُنشئ أليس مفاتيح جديدة لكل رسالة NS:

```python
# Generate ephemeral key pair suitable for Elligator2
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

# Mix ephemeral public key into hash
h = SHA256(h || aepk)

# Elligator2 encode for transmission
elg2_aepk = ENCODE_ELG2(aepk)

# State: h updated with Alice's ephemeral key
# Send elg2_aepk as first 32 bytes of NS message
```
### KDF 4: قسم المفتاح الثابت في NS (نمط المصافحة في Noise) (es DH، تبادل مفاتيح ديفي-هيلمان الزائل-الساكن)

يشتق مفاتيح لتشفير المفتاح الثابت الخاص بـ Alice:

```python
# Perform first DH (ephemeral-static)
sharedSecret = DH(aesk, bpk)  # Alice computes
# Equivalent: sharedSecret = DH(bsk, aepk)  # Bob computes

# Derive cipher key from shared secret
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption parameters
nonce = 0
associated_data = h  # Current hash transcript

# Encrypt static key section
if binding_requested:
    plaintext = apk  # Alice's static public key (32 bytes)
else:
    plaintext = bytes(32)  # All zeros for unbound

ciphertext = ENCRYPT(k, nonce, plaintext, associated_data)
# ciphertext = 32 bytes encrypted + 16 bytes MAC = 48 bytes

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Static key section encrypted, h updated
# Send ciphertext (48 bytes) as next part of NS message
```
### KDF 5: قسم حمولة NS (ss DH (تبادل ديفي-هيلمان بين مفاتيح ساكنة)، مرتبط فقط)

بالنسبة للجلسات المربوطة، أجرِ عملية DH (تبادل مفاتيح ديفي-هيلمان) ثانية لتشفير الحمولة:

```python
if binding_requested:
    # Alice's static keys
    ask = GENERATE_PRIVATE()  # Alice's long-term key
    apk = DERIVE_PUBLIC(ask)
    
    # Perform second DH (static-static)
    sharedSecret = DH(ask, bpk)  # Alice computes
    # Equivalent: sharedSecret = DH(bsk, apk)  # Bob computes
    
    # Derive cipher key
    keydata = HKDF(chainKey, sharedSecret, "", 64)
    chainKey = keydata[0:31]
    k = keydata[32:63]
    
    nonce = 0
    associated_data = h
else:
    # Unbound: reuse keys from static key section
    # chainKey and k unchanged
    nonce = 1  # Increment nonce (reusing same key)
    associated_data = h

# Encrypt payload
payload = build_payload()  # DateTime + Garlic Cloves + etc.
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Payload encrypted, h contains complete NS transcript
# Save chainKey and h for NSR processing
# Send ciphertext as final part of NS message
```
**ملاحظات مهمة:**

1. **Bound مقابل Unbound**: 
   - Bound ينفذ عمليتين DH (es + ss)
   - Unbound ينفذ عملية DH واحدة (es فقط)
   - Unbound يزيد قيمة nonce (عدد يُستخدم مرة واحدة) بدلاً من اشتقاق مفتاح جديد

2. **سلامة عدم إعادة استخدام المفتاح**:
   - nonces (nonce: عدد يُستخدم مرة واحدة) مختلفة (0 مقابل 1) تمنع إعادة استخدام المفتاح/nonce
   - بيانات مقترنة مختلفة (h مختلف) توفر فصل المجالات

3. **سجل التجزئة**:
   - `h` يحتوي الآن على: protocol_name, empty prologue, bpk, aepk, static_key_ciphertext, payload_ciphertext
   - هذا السجل يربط جميع أجزاء رسالة NS معًا

### دالة اشتقاق المفاتيح لمجموعة وسوم الرد الخاصة بـ NSR

ينشئ Bob علامات لرسائل NSR:

```python
# Chain key from NS payload section
# chainKey = final chainKey from NS KDF

# Generate tagset key
tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)

# Initialize NSR tagset (see DH_INITIALIZE below)
tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

# Get tag for this NSR
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG  # 8 bytes

# State: tag available for NSR message
# Send tag as first 8 bytes of NSR
```
### دوال اشتقاق المفاتيح لرسالة NSR

### KDF (وظيفة اشتقاق مفاتيح) 6: توليد المفتاح المؤقت لـ NSR (اختصار تقني خاص بالمواصفة)

بوب يولّد مفتاحًا مؤقتًا جديدًا لكل NSR:

```python
# Mix tag into hash (I2P extension to Noise)
h = SHA256(h || tag)

# Generate ephemeral key pair
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

# Mix ephemeral public key into hash
h = SHA256(h || bepk)

# Elligator2 encode for transmission
elg2_bepk = ENCODE_ELG2(bepk)

# State: h updated with tag and Bob's ephemeral key
# Send elg2_bepk as bytes 9-40 of NSR message
```
### KDF 7: قسم مفاتيح NSR (ee و se DH)

يشتق مفاتيح لقسم مفاتيح NSR:

```python
# Perform third DH (ephemeral-ephemeral)
sharedSecret_ee = DH(aesk, bepk)  # Alice computes
# Equivalent: sharedSecret_ee = DH(besk, aepk)  # Bob computes

# Mix ee into chain
keydata = HKDF(chainKey, sharedSecret_ee, "", 32)
chainKey = keydata[0:31]

# Perform fourth DH (static-ephemeral)
sharedSecret_se = DH(ask, bepk)  # Alice computes
# Equivalent: sharedSecret_se = DH(besk, apk)  # Bob computes

# Derive cipher key from se
keydata = HKDF(chainKey, sharedSecret_se, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption of empty data (key section has no payload)
nonce = 0
associated_data = h
ciphertext = ENCRYPT(k, nonce, ZEROLEN, associated_data)
# ciphertext = 16 bytes (MAC only, no plaintext)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Key section encrypted, chainKey contains all 4 DH results
# Send ciphertext (16 bytes MAC) as bytes 41-56 of NSR
```
**هام جدًا**: هذا يُكمل Noise IK handshake (مصافحة Noise بنمط IK). `chainKey` يحتوي الآن على مساهمات من جميع عمليات DH الأربع (تبادل المفاتيح ديفي-هيلمان) (es, ss, ee, se).

### KDF (دالة اشتقاق المفتاح) 8: قسم حمولة NSR

يشتق مفاتيح لتشفير حمولة NSR:

```python
# Split chainKey into bidirectional keys
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]   # Alice → Bob key
k_ba = keydata[32:63]  # Bob → Alice key

# Initialize ES tagsets for both directions
tagset_ab = DH_INITIALIZE(chainKey, k_ab)  # Alice → Bob
tagset_ba = DH_INITIALIZE(chainKey, k_ba)  # Bob → Alice

# Derive NSR payload key (Bob → Alice)
k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)

# Encrypt NSR payload
nonce = 0
associated_data = h  # Binds payload to entire NSR
payload = build_payload()  # Usually application reply
ciphertext = ENCRYPT(k_nsr, nonce, payload, associated_data)

# State: Bidirectional ES sessions established
# tagset_ab and tagset_ba ready for ES messages
# Send ciphertext as bytes 57+ of NSR message
```
**ملاحظات مهمة:**

1. **عملية التقسيم**: 
   - ينشئ مفاتيح مستقلة لكل اتجاه
   - يمنع إعادة استخدام المفتاح بين Alice→Bob و Bob→Alice

2. **ربط الحمولة في NSR**:
   - تستخدم `h` كبيانات مرتبطة لربط الحمولة بالمصافحة
   - توفر KDF (دالة اشتقاق المفاتيح) منفصلة ("AttachPayloadKDF") فصل المجالات

3. **جاهزية ES**:
   - بعد NSR، يمكن للطرفين إرسال رسائل ES
   - يجب على أليس استلام رسالة NSR قبل إرسال ES
   - يجب على بوب استلام رسالة ES قبل إرسال ES

### دوال اشتقاق المفاتيح (KDFs) لرسائل ES (مؤقت-ثابت)

رسائل ES (نوع رسائل خاص بـ I2P) تستخدم مفاتيح جلسة مولدة مسبقاً من tagsets (مجموعات الوسوم):

```python
# Sender gets next tag and key
tagsetEntry = outbound_tagset.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG     # 8 bytes
k = tagsetEntry.SESSION_KEY       # 32 bytes
N = tagsetEntry.INDEX             # Message number

# Construct nonce (12 bytes)
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD encryption
associated_data = tag  # Tag is associated data
payload = build_payload()
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Send: tag || ciphertext (8 + len(ciphertext) bytes)
```
**عملية الاستقبال:**

```python
# Extract tag
tag = message[0:8]

# Look up tag in inbound tagsets
tagsetEntry = inbound_tagset.GET_SESSION_KEY(tag)
if tagsetEntry is None:
    # Not an ES message, try NS/NSR decryption
    return try_handshake_decryption(message)

k = tagsetEntry.SESSION_KEY
N = tagsetEntry.INDEX

# Construct nonce
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD decryption
associated_data = tag
ciphertext = message[8:]
try:
    payload = DECRYPT(k, nonce, ciphertext, associated_data)
except AuthenticationError:
    # MAC verification failed, reject message
    return reject_message()

# Process payload blocks
process_payload(payload)

# Remove tag from tagset (one-time use)
inbound_tagset.remove(tag)
```
### الدالة DH_INITIALIZE

ينشئ tagset (مجموعة وسوم) لاتجاه واحد:

```python
def DH_INITIALIZE(rootKey, k):
    """
    Initializes a tagset with session tag and symmetric key ratchets.
    
    Args:
        rootKey: Chain key from previous DH ratchet (32 bytes)
        k: Key material from split() or DH ratchet (32 bytes)
    
    Returns:
        tagset: Initialized tagset object
    """
    # Derive next root key and chain key
    keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)
    nextRootKey = keydata[0:31]
    chainKey_tagset = keydata[32:63]
    
    # Derive separate chain keys for tags and keys
    keydata = HKDF(chainKey_tagset, ZEROLEN, "TagAndKeyGenKeys", 64)
    sessTag_ck = keydata[0:31]   # Session tag chain key
    symmKey_ck = keydata[32:63]  # Symmetric key chain key
    
    # Create tagset object
    tagset = Tagset()
    tagset.nextRootKey = nextRootKey
    tagset.sessTag_chainKey = sessTag_ck
    tagset.symmKey_chainKey = symmKey_ck
    tagset.lastIndex = -1
    
    return tagset
```
**سياقات الاستخدام:**

1. **NSR Tagset (مجموعة الوسوم)**: `DH_INITIALIZE(chainKey_from_NS, tagsetKey_NSR)`
2. **ES Tagsets**: `DH_INITIALIZE(chainKey_from_NSR, k_ab or k_ba)`
3. **Ratcheted Tagsets (بآلية السقاطة)**: `DH_INITIALIZE(nextRootKey_from_previous, tagsetKey_from_DH)`

---

## آليات السقاطة

تستخدم ECIES (مخطط التشفير المتكامل بالمنحنيات الإهليلجية) ثلاث آليات راتشِت متزامنة لتوفير السرية الأمامية وإدارة فعّالة للجلسات.

### نظرة عامة حول Ratchet (آلية تقدّم أحاديّة الاتجاه في التشفير)

**ثلاثة أنواع من Ratchet (آلية تقدّم أحادي الاتجاه في التشفير):**

1. **DH Ratchet (آلية تدوير الحالة الأمنية)**: يجري تبادلات مفاتيح Diffie-Hellman لتوليد مفاتيح جذرية جديدة
2. **Session Tag Ratchet**: يشتق وسوم جلسة أحادية الاستخدام بشكل حتمي
3. **Symmetric Key Ratchet**: يشتق مفاتيح جلسة لتشفير الرسائل

**العلاقة:**

```
DH Ratchet (periodic)
    ↓
Creates new tagset
    ↓
Session Tag Ratchet (per message) ← synchronized → Symmetric Key Ratchet (per message)
    ↓                                                      ↓
Session Tags (8 bytes each)                      Session Keys (32 bytes each)
```
**الخصائص الرئيسية:**

- **المرسل**: يولّد الوسوم والمفاتيح عند الطلب (لا حاجة للتخزين)
- **المتلقي**: يولّد مسبقًا الوسوم لنافذة التطلّع المسبق (يتطلب تخزينًا)
- **المزامنة**: فهرس الوسم يحدد فهرس المفتاح (N_tag = N_key)
- **السرية الأمامية**: تتحقق عبر DH ratchet الدوري (آلية ترقية مفاتيح تعتمد على ديفي‑هيلمان)
- **الكفاءة**: يمكن للمتلقي تأجيل حساب المفتاح حتى استلام الوسم

### DH Ratchet (آلية السقاطة القائمة على ديفي-هيلمان لتدوير المفاتيح)

توفر سقاطة ديفي-هيلمان السرية الأمامية من خلال تبادل مفاتيح مؤقتة جديدة بشكل دوري.

### تواتر DH Ratchet (آلية تبديل المفاتيح باستخدام ديفي-هيلمان)

**الشروط المطلوبة لِـ Ratchet (آلية تدوير المفاتيح):** - اقتراب نفاد مجموعة الوسوم (الوسم 65535 هو الحد الأقصى) - سياسات خاصة بالتنفيذ:   - عتبة عدد الرسائل (مثلًا، كل 4096 رسالة)   - عتبة زمنية (مثلًا، كل 10 دقائق)   - عتبة حجم البيانات (مثلًا، كل 100 ميغابايت)

**الـ Ratchet الأولى الموصى بها (آلية التدرّج)**: حوالي رقم الوسم 4096 لتجنّب بلوغ الحدّ

**القيم القصوى:** - **أقصى معرّف tag set (مجموعة وسوم)**: 65535 - **أقصى معرّف مفتاح**: 32767 - **أقصى عدد للرسائل لكل tag set**: 65535 - **الحد الأقصى النظري للبيانات لكل جلسة**: ~6.9 تيرابايت (64K مجموعات وسوم × 64K رسالة × بمتوسط 1730 بايت)

### معرّفات الوسوم والمفاتيح في DH Ratchet (آلية التقدّم المرحلي باستخدام ديفي-هيلمان)

**مجموعة العلامات الأولية** (بعد المصافحة): - معرّف مجموعة العلامات: 0 - لم تُرسل كتل NextKey بعد - لم تُعيَّن أي معرّفات مفاتيح

**بعد الـ Ratchet الأول (آلية تدوير المفاتيح)**: - معرّف مجموعة الوسوم: 1 = (1 + معرّف مفتاح أليس + معرّف مفتاح بوب) = (1 + 0 + 0) - تُرسل أليس NextKey بمعرّف مفتاح 0 - يردّ بوب بـ NextKey بمعرّف مفتاح 0

**مجموعات الوسوم اللاحقة**: - معرّف مجموعة الوسوم = 1 + معرّف مفتاح المرسِل + معرّف مفتاح المستلِم - مثال: مجموعة الوسوم 5 = (1 + sender_key_2 + receiver_key_2)

**جدول تطوّر مجموعة الوسوم:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tag Set ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Sender Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Receiver Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial tag set (post-NSR)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">First ratchet (both generate new keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Pattern repeats</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65534</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32766</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Second-to-last tag set</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Final tag set</td>
    </tr>
  </tbody>
</table>
\* = تم توليد مفتاح جديد في هذه الـ ratchet (آلية تجديد المفاتيح تدريجيًا)

**قواعد مُعرّف المفتاح:** - تكون المعرّفات متسلسلة بدءًا من 0 - لا تزداد المعرّفات إلا عند إنشاء مفتاح جديد - الحد الأقصى لمعرّف المفتاح هو 32767 (15 بت) - بعد معرّف المفتاح 32767، يلزم بدء جلسة جديدة

### تدفق الرسائل في DH Ratchet (آلية الراتشيت القائمة على ديفي-هيلمان)

**الأدوار:** - **Tag Sender (مرسل الوسم)**: يمتلك مجموعة Tag الصادرة، ويرسل الرسائل - **Tag Receiver**: يمتلك مجموعة Tag الواردة، ويتلقى الرسائل

**النمط:** مرسِل الوسوم يُطلِق ratchet (آلية تدوير مفاتيح تدريجية) عندما تشارف مجموعة الوسوم على النفاد.

**مخطط تدفق الرسائل:**

```
Tag Sender                         Tag Receiver

       ... using tag set #0 ...

(Tag set #0 approaching exhaustion)
(Generate new key #0)

NextKey forward, request reverse, with key #0  -------->
(Repeat until NextKey ACK received)
                                   (Generate new key #0)
                                   (Perform DH: sender_key_0 × receiver_key_0)
                                   (Create inbound tag set #1)

        <---------------           NextKey reverse, with key #0
                                   (Repeat until tag from tag set #1 received)

(Receive NextKey with key #0)
(Perform DH: sender_key_0 × receiver_key_0)
(Create outbound tag set #1)


       ... using tag set #1 ...


(Tag set #1 approaching exhaustion)
(Generate new key #1)

NextKey forward, with key #1        -------->
(Repeat until NextKey ACK received)
                                   (Reuse existing key #0)
                                   (Perform DH: sender_key_1 × receiver_key_0)
                                   (Create inbound tag set #2)

        <--------------            NextKey reverse, id 0 (ACK)
                                   (Repeat until tag from tag set #2 received)

(Receive NextKey with id 0)
(Perform DH: sender_key_1 × receiver_key_0)
(Create outbound tag set #2)


       ... using tag set #2 ...


(Tag set #2 approaching exhaustion)
(Reuse existing key #1)

NextKey forward, request reverse, id 1  -------->
(Repeat until NextKey received)
                                   (Generate new key #1)
                                   (Perform DH: sender_key_1 × receiver_key_1)
                                   (Create inbound tag set #3)

        <--------------            NextKey reverse, with key #1

(Receive NextKey with key #1)
(Perform DH: sender_key_1 × receiver_key_1)
(Create outbound tag set #3)


       ... using tag set #3 ...

       (Pattern repeats: even-numbered tag sets
        use forward key, odd-numbered use reverse key)
```
**أنماط Ratchet (آلية تدوير المفاتيح المتدرّجة):**

**إنشاء مجموعات وسوم ذات أرقام زوجية** (2, 4, 6, ...): 1. يولّد المرسل مفتاحًا جديدًا 2. يرسل المرسل كتلة NextKey (كتلة المفتاح التالي) بالمفتاح الجديد 3. يرسل المستقبل كتلة NextKey بمعرّف المفتاح القديم (ACK) 4. ينفّذ كلاهما DH (تبادل مفاتيح ديفي-هيلمان) باستخدام (مفتاح المرسل الجديد × مفتاح المستقبل القديم)

**إنشاء مجموعات وسوم ذات أرقام فردية** (3، 5، 7، ...): 1. يطلب المرسل المفتاح العكسي (يرسل NextKey مع علم الطلب) 2. يولد المستقبل مفتاح جديد 3. يرسل المستقبل كتلة NextKey بالمفتاح الجديد 4. يجري الطرفان DH (تبادل المفاتيح ديفي-هيلمان) باستخدام (مفتاح المرسل القديم × مفتاح المستقبل الجديد)

### تنسيق كتلة NextKey (المفتاح التالي)

انظر قسم تنسيق الحمولة للحصول على المواصفة المفصلة لكتلة NextKey.

**العناصر الأساسية:** - **بايت الأعلام**:   - البت 0: وجود المفتاح (1) أو المعرّف فقط (0)   - البت 1: المفتاح العكسي (1) أو المفتاح الأمامي (0)   - البت 2: طلب المفتاح العكسي (1) أو بدون طلب (0) - **معرّف المفتاح**: 2 بايت، بترتيب بايت كبير (0-32767) - **المفتاح العام**: 32 بايت X25519 (إذا كان البت 0 = 1)

**أمثلة على كتل NextKey:**

```python
# Sender initiates ratchet with new key (key ID 0, tag set 1)
NextKey(flags=0x01, key_id=0, pubkey=sender_key_0)

# Receiver replies with new key (key ID 0, tag set 1)
NextKey(flags=0x03, key_id=0, pubkey=receiver_key_0)

# Sender ratchets again with new key (key ID 1, tag set 2)
NextKey(flags=0x01, key_id=1, pubkey=sender_key_1)

# Receiver ACKs with old key ID (tag set 2)
NextKey(flags=0x02, key_id=0)

# Sender requests reverse key (tag set 3)
NextKey(flags=0x04, key_id=1)

# Receiver sends new reverse key (key ID 1, tag set 3)
NextKey(flags=0x03, key_id=1, pubkey=receiver_key_1)
```
### دالة اشتقاق المفاتيح لـ DH Ratchet

عند تبادل مفاتيح جديدة:

```python
# Tag sender generates or reuses key
if generating_new:
    sender_sk = GENERATE_PRIVATE()
    sender_pk = DERIVE_PUBLIC(sender_sk)
else:
    # Reuse existing key pair
    sender_pk = existing_sender_pk

# Tag receiver generates or reuses key
if generating_new:
    receiver_sk = GENERATE_PRIVATE()
    receiver_pk = DERIVE_PUBLIC(receiver_sk)
else:
    # Reuse existing key pair
    receiver_pk = existing_receiver_pk

# Both parties perform DH
sharedSecret = DH(sender_sk, receiver_pk)

# Derive tagset key
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)

# Get next root key from previous tagset
rootKey = previous_tagset.nextRootKey

# Initialize new tagset
new_tagset = DH_INITIALIZE(rootKey, tagsetKey)

# Tag sender: outbound tagset
# Tag receiver: inbound tagset
```
**التوقيت الحرج:**

**مرسِل الوسوم:** - ينشئ مجموعة وسوم صادرة جديدة فورًا - يبدأ استخدام الوسوم الجديدة فورًا - يحذف مجموعة الوسوم الصادرة القديمة

**مستقبل الوسوم:** - ينشئ مجموعة وسوم واردة جديدة - يحتفظ بمجموعة الوسوم الواردة القديمة لمدة سماح (3 دقائق) - يقبل الوسوم من كلتا مجموعتي الوسوم القديمة والجديدة خلال فترة السماح - يحذف مجموعة الوسوم الواردة القديمة بعد انتهاء فترة السماح

### إدارة حالة DH Ratchet (آلية التدوير باستخدام ديفي-هيلمان)

**حالة المرسل:** - مجموعة الوسوم الصادرة الحالية - معرّف مجموعة الوسوم ومعرّفات المفاتيح - مفتاح الجذر التالي (للـ ratchet التالي، آلية تدوير/ترقية المفاتيح) - عدد الرسائل في مجموعة الوسوم الحالية

**حالة المستقبِل:** - مجموعة/مجموعات الوسوم الواردة الحالية (قد يكون عددها 2 خلال فترة السماح) - أرقام الرسائل السابقة (PN) لاكتشاف الفجوات - نافذة استباقية للوسوم المُولَّدة مسبقًا - المفتاح الجذري التالي (لـ ratchet التالية - آلية تدوير المفاتيح تدريجيًا)

**قواعد انتقال الحالة:**

1. **قبل أول عملية Ratchet (آلية تدوير المفاتيح)**:
   - استخدام مجموعة الوسوم 0 (من NSR)
   - لم يتم تعيين أي معرّفات مفاتيح

2. **بدء Ratchet (آلية السقاطة التشفيرية)**:
   - ولِّد مفتاحًا جديدًا (إذا كان المرسِل هو من يتولّى التوليد في هذه الجولة)
   - أرسل كتلة NextKey في رسالة ES
   - انتظر رد NextKey قبل إنشاء مجموعة وسوم صادرة جديدة

3. **استلام طلب Ratchet (آلية التقدّم المتدرّج)**:
   - توليد مفتاح جديد (إذا كان المتلقي هو المولِّد في هذه الجولة)
   - إجراء DH (تبادل المفاتيح ديفي–هيلمان) مع المفتاح المستلَم
   - إنشاء مجموعة وسوم واردة جديدة
   - إرسال رد NextKey
   - الاحتفاظ بمجموعة الوسوم الواردة القديمة لفترة سماح

4. **إكمال Ratchet (آلية تدوير المفاتيح المتتابعة)**:
   - استلام استجابة NextKey
   - إجراء DH (تبادل مفاتيح ديفي-هيلمان)
   - إنشاء مجموعة وسوم صادرة جديدة
   - بدء استخدام الوسوم الجديدة

### Session Tag Ratchet (آلية تقدّم أحاديّ الاتجاه لوسوم الجلسة)

تولّد session tag ratchet (آلية المسنن لعلامات الجلسة) علامات جلسة للاستخدام لمرة واحدة بطول 8 بايت بشكل حتمي.

### الغرض من Session Tag Ratchet (آلية التدوير التدريجي لوسوم الجلسة)

- يستبدل نقل الوسوم الصريح (أرسل ElGamal وسومًا بطول 32 بايت)
- يُمكّن المُستقبِل من توليد الوسوم مسبقًا لنافذة التطلّع المسبق
- يُولِّد المُرسِل عند الطلب (من دون الحاجة إلى تخزين)
- يتزامن مع symmetric key ratchet (آلية تبديل مفاتيح متماثلة تدريجية) عبر فهرس

### صيغة Session Tag Ratchet (آلية السقاطة الخاصة بوسم الجلسة)

**التهيئة:**

```python
# From DH_INITIALIZE
sessTag_ck = initial_chain_key  # 32 bytes

# Initialize session tag ratchet
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
sessTag_chainKey = keydata[0:31]    # First chain key
SESSTAG_CONSTANT = keydata[32:63]   # Constant for all tags in this tagset
```
**توليد الوسم (للوسم N):**

```python
# Generate tag N
keydata = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata[0:31]  # Chain key for next tag
tag_N = keydata[32:39]              # Session tag (8 bytes)

# Chain continues for each tag
# tag_0, tag_1, tag_2, ..., tag_65535
```
**التسلسل الكامل:**

```python
# Tag 0
keydata_0 = HKDF(sessTag_chainKey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_0 = keydata_0[0:31]
tag_0 = keydata_0[32:39]

# Tag 1
keydata_1 = HKDF(sessTag_chainKey_0, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_1 = keydata_1[0:31]
tag_1 = keydata_1[32:39]

# Tag N
keydata_N = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata_N[0:31]
tag_N = keydata_N[32:39]
```
### تنفيذ المرسل لـ Session Tag Ratchet (آلية السقاطة لوسوم الجلسة)

```python
class OutboundTagset:
    def __init__(self, sessTag_ck):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
    
    def get_next_tag(self):
        # Increment index
        self.index += 1
        
        if self.index > 65535:
            raise TagsetExhausted("Ratchet required")
        
        # Generate tag
        keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
        self.chainKey = keydata[0:31]
        tag = keydata[32:39]
        
        return (tag, self.index)
```
**عملية المرسل:** 1. استدعِ `get_next_tag()` لكل رسالة 2. استخدم الوسم المعاد في رسالة ES 3. احفظ المؤشر N لتتبع ACK (إقرار) المحتمل 4. لا يلزم تخزين الوسم (يتم إنشاؤه عند الطلب)

### تنفيذ المستقبِل لآلية Ratchet (آلية تصعيد تشفيرية) لوسم الجلسة

```python
class InboundTagset:
    def __init__(self, sessTag_ck, look_ahead=32):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
        self.look_ahead = look_ahead
        self.tags = {}  # Dictionary: tag -> index
        
        # Pre-generate initial tags
        self.extend(look_ahead)
    
    def extend(self, count):
        """Generate 'count' more tags"""
        for _ in range(count):
            self.index += 1
            
            if self.index > 65535:
                return  # Cannot exceed maximum
            
            # Generate tag
            keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
            self.chainKey = keydata[0:31]
            tag = keydata[32:39]
            
            # Store tag
            self.tags[tag] = self.index
    
    def lookup_tag(self, tag):
        """Look up tag and return index"""
        if tag in self.tags:
            index = self.tags[tag]
            # Remove tag (one-time use)
            del self.tags[tag]
            return index
        return None
    
    def check_and_extend(self):
        """Extend if tag count is low"""
        current_count = len(self.tags)
        if current_count < self.look_ahead // 2:
            # Extend to restore window
            self.extend(self.look_ahead - current_count)
```
**عملية المُستقبِل:** 1. توليد الوسوم مسبقًا لنافذة التطلّع المسبق (على سبيل المثال، 32 وسمًا) 2. تخزين الوسوم في جدول تجزئة أو قاموس 3. عند وصول الرسالة، ابحث عن الوسم للحصول على الفهرس N 4. إزالة الوسم من التخزين (استخدام لمرة واحدة) 5. توسيع النافذة إذا انخفض عدد الوسوم تحت العتبة

### استراتيجية النظر المسبق لـ Session Tag (وسم الجلسة)

**الغرض**: الموازنة بين استهلاك الذاكرة والتعامل مع الرسائل غير المتسلسلة

**أحجام Look-Ahead (التطلّع المسبق) الموصى بها:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tagset Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Initial Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Maximum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ES tagset</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted tagsets</td>
    </tr>
  </tbody>
</table>
**التطلّع المسبق التكيّفي:**

```python
# Dynamic look-ahead based on highest tag received
look_ahead = min(tsmax, tsmin + N // 4)

# Example:
# tsmin = 24, tsmax = 160
# N = 0:   look_ahead = min(160, 24 + 0/4) = 24
# N = 100: look_ahead = min(160, 24 + 100/4) = 49
# N = 500: look_ahead = min(160, 24 + 500/4) = 149
# N = 544: look_ahead = min(160, 24 + 544/4) = 160
```
**الاقتطاع من الخلف:**

```python
# Trim tags far behind highest received
trim_behind = look_ahead // 2

# If highest received tag is N=100, trim tags below N=50
```
**حساب الذاكرة:**

```python
# Per tag: 8 bytes (tag) + 2 bytes (index) + overhead ≈ 16 bytes
# Look-ahead of 160 tags ≈ 2.5 KB per inbound tagset

# With multiple sessions:
# 100 inbound sessions × 2.5 KB = 250 KB total
```
### معالجة التسليم خارج الترتيب لـ Session Tag (وسم الجلسة)

**السيناريو**: تصل الرسائل بترتيب غير متسلسل

```
Expected: tag_5, tag_6, tag_7, tag_8
Received: tag_5, tag_7, tag_6, tag_8
```
**سلوك المتلقي:**

1. استلم tag_5:
   - ابحث: تم العثور عليه في الفهرس 5
   - عالج الرسالة
   - أزل tag_5
   - أعلى قيمة مستلمة: 5

2. استلام tag_7 (خارج الترتيب):
   - البحث: عُثر عليه عند الفهرس 7
   - معالجة الرسالة
   - إزالة tag_7
   - أعلى ما تم استلامه: 7
   - ملاحظة: tag_6 ما يزال في التخزين (لم يُستلم بعد)

3. استلام tag_6 (مؤجّل):
   - البحث: وُجد عند الفهرس 6
   - معالجة الرسالة
   - إزالة tag_6
   - أعلى ما تم استلامه: 7 (لم يتغير)

4. تلقي tag_8:
   - إجراء بحث: تم العثور عليه عند الفهرس 8
   - معالجة الرسالة
   - إزالة tag_8
   - أعلى رقم مُستلَم: 8

**إدارة النافذة:** - تتبّع أعلى فهرس تم استلامه - الحفاظ على قائمة بالفهارس المفقودة (الفجوات) - توسيع النافذة استنادًا إلى أعلى فهرس - اختياري: إسقاط الفجوات القديمة بعد انتهاء المهلة الزمنية

### Symmetric Key Ratchet (آلية تدوير المفتاح المتماثل)

تُولِّد symmetric key ratchet (آلية تدوير مفاتيح متماثلة) مفاتيح تشفير بطول 32 بايت متزامنة مع وسوم الجلسة.

### غرض Symmetric Key Ratchet (آلية التحديث المتدرّج للمفتاح المتماثل)

- يوفر مفتاح تشفير فريد لكل رسالة
- متزامن مع session tag ratchet (آلية تدوير مفاتيح وسوم الجلسة) (نفس الفهرس)
- يمكن للمرسل توليده عند الطلب
- يمكن للمستقبِل تأجيل التوليد حتى استلام الوسم

### صيغة Ratchet (آلية السقاطة في التشفير) للمفتاح المتماثل

**التهيئة:**

```python
# From DH_INITIALIZE
symmKey_ck = initial_chain_key  # 32 bytes

# No additional initialization needed
# Unlike session tag ratchet, no constant is derived
```
**توليد المفاتيح (للمفتاح N):**

```python
# Generate key N
SYMMKEY_CONSTANT = ZEROLEN  # Empty string
keydata = HKDF(symmKey_chainKey_(N-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata[0:31]  # Chain key for next key
key_N = keydata[32:63]              # Session key (32 bytes)
```
**التسلسل الكامل:**

```python
# Key 0
keydata_0 = HKDF(symmKey_ck, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
key_0 = keydata_0[32:63]

# Key 1
keydata_1 = HKDF(symmKey_chainKey_0, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_1 = keydata_1[0:31]
key_1 = keydata_1[32:63]

# Key N
keydata_N = HKDF(symmKey_chainKey_(N-1), ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata_N[0:31]
key_N = keydata_N[32:63]
```
### تنفيذ المُرسِل Symmetric Key Ratchet (آلية ترقية المفاتيح المتماثلة)

```python
class OutboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Fast-forward to desired index if needed
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            if self.index == index:
                return keydata[32:63]
        
        # Should not reach here if called correctly
        raise ValueError("Key already generated")
```
**عملية المرسل:** 1. احصل على الوسم التالي مع فهرسه N 2. ولّد مفتاحاً للفهرس N 3. استخدم المفتاح لتشفير الرسالة 4. لا حاجة إلى تخزين المفتاح

### تنفيذ مستقبل Symmetric Key Ratchet (آلية السقاطة للمفتاح المتماثل)

**الاستراتيجية 1: التوليد المؤجل (موصى بها)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = {}  # Optional: cache recently used keys
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Check cache first (optional optimization)
        if index in self.cache:
            key = self.cache[index]
            del self.cache[index]
            return key
        
        # Fast-forward to desired index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                return keydata[32:63]
        
        raise ValueError("Index already passed")
```
**عملية التوليد المؤجَّل:** 1. استلم رسالة ES مع وسم 2. ابحث عن الوسم للحصول على الفهرس N 3. ولّد المفاتيح من 0 حتى N (إن لم تكن مُولَّدة مسبقًا) 4. استخدم المفتاح N لفك تشفير الرسالة 5. أصبح مفتاح السلسلة الآن متموضعًا عند الفهرس N

**المزايا:** - استهلاك ضئيل للذاكرة - يتم إنشاء المفاتيح فقط عند الحاجة - تنفيذ بسيط

**العيوب:** - يجب توليد جميع المفاتيح من 0 إلى N عند أول استخدام - لا يمكنه التعامل مع الرسائل خارج الترتيب من دون التخزين المؤقت

**الاستراتيجية 2: التوليد المسبق باستخدام Tag Window (نافذة الأوسمة) (بديل)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.keys = {}  # Dictionary: index -> key
    
    def extend(self, count):
        """Pre-generate 'count' more keys"""
        for _ in range(count):
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            key = keydata[32:63]
            self.keys[self.index] = key
    
    def get_key(self, index):
        """Retrieve pre-generated key"""
        if index in self.keys:
            key = self.keys[index]
            del self.keys[index]
            return key
        return None
```
**عملية التوليد المسبق:** 1. ولّد مسبقًا مفاتيح مطابقة لنافذة الوسوم (على سبيل المثال: 32 مفتاحًا) 2. خزّن المفاتيح مفهرسة حسب رقم الرسالة 3. عند استلام الوسم، ابحث عن المفتاح المقابل 4. وسّع النافذة مع استخدام الوسوم

**المزايا:** - يتعامل مع الرسائل الخارجة عن الترتيب بشكل طبيعي - استرجاع سريع للمفاتيح (من دون تأخير في التوليد)

**العيوب:** - استهلاك ذاكرة أعلى (32 بايت لكل مفتاح مقابل 8 بايت لكل وسم) - يجب الحفاظ على تزامن المفاتيح مع الوسوم

**مقارنة الذاكرة:**

```python
# Look-ahead of 160:
# Tags only:  160 × 16 bytes = 2.5 KB
# Tags+Keys:  160 × (16 + 32) bytes = 7.5 KB
# 
# For 100 sessions:
# Tags only:  250 KB
# Tags+Keys:  750 KB
```
### مزامنة Ratchet (آلية ترقية المفاتيح تدريجياً) المتماثل باستخدام وسوم الجلسة

**متطلب حاسم**: يجب حتمًا أن يساوي فهرس وسم الجلسة فهرس المفتاح المتماثل

```python
# Sender
tag, index = outbound_tagset.get_next_tag()
key = outbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
ciphertext = ENCRYPT(key, nonce, payload, tag)

# Receiver
index = inbound_tagset.lookup_tag(tag)
key = inbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
plaintext = DECRYPT(key, nonce, ciphertext, tag)
```
**أنماط الفشل:**

إذا تعطّلت المزامنة:
- استخدام مفتاح خاطئ لفك التشفير
- فشل التحقق من MAC (رمز مصادقة الرسالة)
- يتم رفض الرسالة

**الوقاية:** - استخدم دائمًا نفس الفهرس لكلٍ من الوسم والمفتاح - لا تتجاوز الفهارس مطلقًا في أي من آليات ratchet (آلية تدوير المفاتيح المتتابعة في التشفير) - تعامل مع الرسائل الخارجة عن الترتيب بحذر

### بناء Nonce (رقم يُستخدم لمرة واحدة) لِـ Ratchet (آلية تدوير مفاتيح متدرّجة) المتماثل

Nonce (رقم يُستخدم مرة واحدة) يُشتق من رقم الرسالة:

```python
def construct_nonce(index):
    """
    Construct 12-byte nonce for ChaCha20-Poly1305
    
    Args:
        index: Message number (0-65535)
    
    Returns:
        nonce: 12-byte nonce
    """
    # First 4 bytes are always zero
    nonce = bytearray(12)
    nonce[0:4] = b'\x00\x00\x00\x00'
    
    # Last 8 bytes are little-endian message number
    nonce[4:12] = index.to_bytes(8, byteorder='little')
    
    return bytes(nonce)
```
**أمثلة:**

```python
index = 0:     nonce = 0x00000000 0000000000000000
index = 1:     nonce = 0x00000000 0100000000000000
index = 255:   nonce = 0x00000000 FF00000000000000
index = 256:   nonce = 0x00000000 0001000000000000
index = 65535: nonce = 0x00000000 FFFF000000000000
```
**الخصائص المهمة:** - Nonces (nonce: قيمة تُستخدم مرة واحدة) فريدة لكل رسالة ضمن مجموعة الوسوم - لا تتكرر Nonces إطلاقاً (الوسوم المُستخدمة لمرة واحدة تضمن ذلك) - عداد بطول 8 بايت يتيح 2^64 رسالة (نستخدم 2^16 فقط) - يتوافق تنسيق nonce مع البناء القائم على العدّاد وفق RFC 7539

---

## إدارة الجلسات

### سياق الجلسة

يجب أن تنتمي جميع الجلسات الواردة والصادرة إلى سياق محدد:

1. **سياق Router**: جلسات لـ router ذاته
2. **سياق الوجهة**: جلسات لوجهة محلية محددة (تطبيق عميل)

**قاعدة حاسمة**: لا يجوز مطلقًا مشاركة الجلسات بين السياقات لمنع هجمات الارتباط.

**التنفيذ:**

```python
class SessionKeyManager:
    """Context for managing sessions (router or destination)"""
    def __init__(self, context_id):
        self.context_id = context_id
        self.inbound_sessions = {}   # far_end_dest -> [sessions]
        self.outbound_sessions = {}  # far_end_dest -> session
        self.static_keypair = generate_keypair()  # Context's identity
    
    def get_outbound_session(self, destination):
        """Get or create outbound session to destination"""
        if destination not in self.outbound_sessions:
            self.outbound_sessions[destination] = create_outbound_session(destination)
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session, destination=None):
        """Add inbound session, optionally bound to destination"""
        if destination:
            if destination not in self.inbound_sessions:
                self.inbound_sessions[destination] = []
            self.inbound_sessions[destination].append(session)
        else:
            # Unbound session
            self.inbound_sessions[None].append(session)
```
**تنفيذ I2P بلغة جافا:**

في Java I2P، يوفر الصنف `SessionKeyManager` هذه الوظائف: - مثيل واحد لـ`SessionKeyManager` لكل router - مثيل واحد لـ`SessionKeyManager` لكل وجهة محلية - إدارة منفصلة لجلسات ECIES وElGamal ضمن كل سياق

### ربط الجلسة

**الربط** يقرن جلسة بوجهة بعيدة محددة.

### الجلسات المرتبطة

**الخصائص:** - تضمين المفتاح الثابت للمرسل في رسالة NS - يمكن للمستلم تحديد وجهة المرسل - يتيح اتصالاً ثنائي الاتجاه - جلسة صادرة واحدة لكل وجهة - قد توجد عدة جلسات واردة (أثناء الانتقالات)

**حالات الاستخدام:** - اتصالات تدفقية (مشابهة لـ TCP) - datagrams (حزم بيانات غير متصلة) قابلة للرد - أي بروتوكول يتطلب طلب/استجابة

**عملية الربط:**

```python
# Alice creates bound outbound session
outbound_session = OutboundSession(
    destination=bob_destination,
    static_key=alice_static_key,
    bound=True
)

# Alice sends NS with static key
ns_message = build_ns_message(
    ephemeral_key=alice_ephemeral_key,
    static_key=alice_static_key,  # Included for binding
    payload=data
)

# Bob receives NS
bob_receives_ns(ns_message)
# Bob extracts Alice's static key
alice_static_key = decrypt_static_key_section(ns_message)

# Bob looks up Alice's destination (from bundled LeaseSet)
alice_destination = lookup_destination_by_static_key(alice_static_key)

# Bob creates bound inbound session
inbound_session = InboundSession(
    destination=alice_destination,
    bound=True
)

# Bob pairs with outbound session
outbound_session = OutboundSession(
    destination=alice_destination,
    bound=True
)
```
**المزايا:** 1. **ديفي-هيلمان مؤقت-مؤقت**: يستخدم الرد ee DH (سرّية أمامية كاملة) 2. **استمرارية الجلسة**: تحافظ Ratchets (آلية السقاطة) على الارتباط بالوجهة نفسها 3. **الأمان**: يمنع اختطاف الجلسة (موثَّق بمفتاح ثابت) 4. **الكفاءة**: جلسة واحدة لكل وجهة (من دون تكرار)

### جلسات غير مرتبطة

**الخصائص:** - لا يوجد مفتاح ثابت في رسالة NS (قسم الأعلام كله أصفار) - لا يستطيع المستلم تحديد هوية المرسل - اتصال أحادي الاتجاه فقط - يُسمح بإنشاء عدة جلسات إلى نفس الوجهة

**حالات الاستخدام:** - رزم بيانات خام (أرسل وانسَ) - نشر مجهول الهوية - مراسلة بأسلوب البث

**الخصائص:** - أكثر إخفاءً للهوية (لا تحديد لهوية المرسل) - أكثر كفاءة (1 DH مقابل 2 DH في عملية المصافحة) - لا يمكن الرد (المستلم لا يعرف أين يرد) - لا يوجد session ratcheting (ترقية مفاتيح الجلسة تدريجياً؛ استخدام لمرة واحدة أو استخدام محدود)

### إقران الجلسة

**الإقران** يربط جلسة واردة بجلسة صادرة لتمكين الاتصال ثنائي الاتجاه.

### إنشاء جلسات مقترنة

**وجهة نظر أليس (الطرف البادئ):**

```python
# Create outbound session to Bob
outbound_session = create_outbound_session(bob_destination)

# Create paired inbound session
inbound_session = create_inbound_session(
    paired_with=outbound_session,
    bound_to=bob_destination
)

# Link them
outbound_session.paired_inbound = inbound_session
inbound_session.paired_outbound = outbound_session

# Send NS message
send_ns_message(outbound_session, payload)
```
**منظور بوب (المستجيب):**

```python
# Receive NS message
ns_message = receive_ns_message()

# Create inbound session
inbound_session = create_inbound_session_from_ns(ns_message)

# If NS contains static key (bound):
if ns_message.has_static_key():
    alice_destination = extract_destination(ns_message)
    inbound_session.bind_to(alice_destination)
    
    # Create paired outbound session
    outbound_session = create_outbound_session(alice_destination)
    
    # Link them
    outbound_session.paired_inbound = inbound_session
    inbound_session.paired_outbound = outbound_session

# Send NSR
send_nsr_message(inbound_session, outbound_session, payload)
```
### فوائد إقران الجلسة

1. **تأكيدات الاستلام داخل القناة (In-band ACKs)**: يمكن تأكيد الرسائل من دون clove مستقل (وحدة فرعية ضمن رسالة مجمّعة في I2P)
2. **التبديل التدريجي للمفاتيح الفعّال (Ratcheting: آلية تدوير مفاتيح تدريجية في التشفير)**: يتقدّم في كلا الاتجاهين معاً
3. **التحكم في التدفق**: يمكن تنفيذ ضغط عكسي عبر الجلسات المقترنة
4. **اتساق الحالة**: أسهل في الحفاظ على حالة متزامنة

### قواعد إقران الجلسات

- قد تكون الجلسة الصادرة غير مقترنة (NS غير مرتبط)
- يجب أن تكون الجلسة الواردة لـ NS المرتبط مقترنة
- يتم الإقران عند إنشاء الجلسة، وليس بعد ذلك
- الجلسات المقترنة لها نفس ارتباط الوجهة
- Ratchets (آليات تدوير المفاتيح التشفيرية) تحدث بشكل مستقل ولكن يجري تنسيقها

### دورة حياة الجلسة

### دورة حياة الجلسة: مرحلة الإنشاء

**إنشاء جلسة صادرة (Alice):**

```python
def create_outbound_session(destination, bound=True):
    session = OutboundSession()
    session.destination = destination
    session.bound = bound
    session.state = SessionState.NEW
    session.created_time = now()
    
    # Generate keys for NS message
    session.ephemeral_keypair = generate_elg2_keypair()
    if bound:
        session.static_key = context.static_keypair.public_key
    
    # Will be populated after NSR received
    session.outbound_tagset = None
    session.inbound_tagset = None
    
    return session
```
**إنشاء جلسة واردة (Bob):**

```python
def create_inbound_session_from_ns(ns_message):
    session = InboundSession()
    session.state = SessionState.ESTABLISHED
    session.created_time = now()
    
    # Extract from NS
    session.remote_ephemeral_key = ns_message.ephemeral_key
    session.remote_static_key = ns_message.static_key
    
    if session.remote_static_key:
        session.bound = True
        session.destination = lookup_destination(session.remote_static_key)
    else:
        session.bound = False
        session.destination = None
    
    # Generate keys for NSR
    session.ephemeral_keypair = generate_elg2_keypair()
    
    # Create tagsets from KDF
    session.inbound_tagset = create_tagset_from_nsr()
    session.outbound_tagset = create_tagset_from_nsr()
    
    return session
```
### دورة حياة الجلسة: المرحلة النشطة

**انتقالات الحالة:**

```
NEW (outbound only)
  ↓
  NS sent
  ↓
PENDING_REPLY (outbound only)
  ↓
  NSR received
  ↓
ESTABLISHED
  ↓
  ES messages exchanged
  ↓
ESTABLISHED (ongoing)
  ↓
  (optional) RATCHETING
  ↓
ESTABLISHED
```
**صيانة الجلسة النشطة:**

```python
def maintain_active_session(session):
    # Update last activity time
    session.last_activity = now()
    
    # Check for ratchet needed
    if session.outbound_tagset.needs_ratchet():
        initiate_ratchet(session)
    
    # Check for incoming ratchet
    if received_nextkey_block():
        process_ratchet(session)
    
    # Trim old tags from inbound tagset
    session.inbound_tagset.expire_old_tags()
    
    # Check session health
    if session.idle_time() > SESSION_TIMEOUT:
        mark_session_idle(session)
```
### دورة حياة الجلسة: مرحلة انتهاء الصلاحية

**قيم مهلة الجلسة:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Session Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Sender Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Receiver Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Old tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">After ratchet</td>
    </tr>
  </tbody>
</table>
**منطق انتهاء الصلاحية:**

```python
def check_session_expiration():
    for session in active_sessions:
        # Outbound session expiration (sender)
        if session.is_outbound():
            if session.idle_time() > 8 * 60:  # 8 minutes
                expire_outbound_session(session)
        
        # Inbound session expiration (receiver)
        else:
            if session.idle_time() > 10 * 60:  # 10 minutes
                expire_inbound_session(session)
    
    # Old tagsets (after ratchet)
    for tagset in old_tagsets:
        if tagset.age() > 3 * 60:  # 3 minutes
            delete_tagset(tagset)
```
**قاعدة حرجة**: يجب أن تنتهي الجلسات الصادرة قبل الجلسات الواردة لمنع عدم التزامن.

**إنهاء سلس:**

```python
def terminate_session(session, reason=0):
    # Send Termination block (if implemented)
    send_termination_block(session, reason)
    
    # Mark session for deletion
    session.state = SessionState.TERMINATED
    
    # Keep session briefly for final messages
    schedule_deletion(session, delay=30)  # 30 seconds
    
    # Notify paired session
    if session.paired_session:
        session.paired_session.mark_remote_terminated()
```
### رسائل NS متعددة

**السيناريو**: فُقدت رسالة NS الخاصة بأليس أو فُقد رد NSR.

**سلوك أليس:**

```python
class OutboundSession:
    def __init__(self):
        self.ns_messages_sent = []
        self.ns_timer = None
        self.max_ns_attempts = 5
    
    def send_ns_message(self, payload):
        # Generate new ephemeral key for each NS
        ephemeral_key = generate_elg2_keypair()
        
        ns_message = build_ns_message(
            ephemeral_key=ephemeral_key,
            static_key=self.static_key,
            payload=payload
        )
        
        # Store state for this NS
        ns_state = {
            'ephemeral_key': ephemeral_key,
            'chainkey': compute_chainkey(ns_message),
            'hash': compute_hash(ns_message),
            'tagset': derive_nsr_tagset(ns_message),
            'sent_time': now()
        }
        self.ns_messages_sent.append(ns_state)
        
        # Send message
        send_message(ns_message)
        
        # Set timer for retry
        if not self.ns_timer:
            self.ns_timer = set_timer(1.0, self.on_ns_timeout)
    
    def on_ns_timeout(self):
        if len(self.ns_messages_sent) >= self.max_ns_attempts:
            # Give up
            fail_session("No NSR received after {self.max_ns_attempts} attempts")
            return
        
        # Retry with new NS message
        send_ns_message(self.payload)
    
    def on_nsr_received(self, nsr_message):
        # Cancel timer
        cancel_timer(self.ns_timer)
        
        # Find which NS this NSR responds to
        tag = nsr_message.tag
        for ns_state in self.ns_messages_sent:
            if tag in ns_state['tagset']:
                # This NSR corresponds to this NS
                self.active_ns_state = ns_state
                break
        
        # Process NSR and complete handshake
        complete_handshake(nsr_message, self.active_ns_state)
        
        # Discard other NS states
        self.ns_messages_sent = []
```
**خصائص مهمة:**

1. **مفاتيح مؤقتة فريدة**: تستخدم كل NS (جلسة اتصال) مفتاحًا مؤقتًا مختلفًا
2. **مصافحات مستقلة**: تنشئ كل NS حالة مصافحة مستقلة
3. **ارتباط NSR**: يحدد وسم NSR (استجابة NS) NS المقصود بالاستجابة
4. **تنظيف الحالة**: تُزال حالات NS غير المستخدمة بعد نجاح NSR

**منع الهجمات:**

لمنع استنزاف الموارد:

```python
# Limit NS sending rate
max_ns_rate = 5 per 10 seconds per destination

# Limit total NS attempts
max_ns_attempts = 5

# Limit total pending NS states
max_pending_ns = 10 per context
```
### رسائل NSR متعددة

**السيناريو**: يرسل بوب عدة NSRs (رسائل تقنية في I2P مخصّصة لحمل بيانات الرد) (على سبيل المثال، تقسيم بيانات الرد عبر عدة رسائل).

**سلوك بوب:**

```python
class InboundSession:
    def send_nsr_replies(self, payload_chunks):
        # One NS received, multiple NSRs to send
        for chunk in payload_chunks:
            # Generate new ephemeral key for each NSR
            ephemeral_key = generate_elg2_keypair()
            
            # Get next tag from NSR tagset
            tag = self.nsr_tagset.get_next_tag()
            
            nsr_message = build_nsr_message(
                tag=tag,
                ephemeral_key=ephemeral_key,
                payload=chunk
            )
            
            send_message(nsr_message)
        
        # Wait for ES message from Alice
        self.state = SessionState.AWAITING_ES
```
**سلوك أليس:**

```python
class OutboundSession:
    def on_nsr_received(self, nsr_message):
        if self.state == SessionState.PENDING_REPLY:
            # First NSR received
            complete_handshake(nsr_message)
            self.state = SessionState.ESTABLISHED
            
            # Create ES sessions
            self.es_outbound_tagset = derive_es_outbound_tagset()
            self.es_inbound_tagset = derive_es_inbound_tagset()
            
            # Send ES message (ACK)
            send_es_message(empty_payload)
        
        elif self.state == SessionState.ESTABLISHED:
            # Additional NSR received
            # Decrypt and process payload
            payload = decrypt_nsr_payload(nsr_message)
            process_payload(payload)
            
            # These NSRs are from other NS attempts, ignore handshake
```
**تنظيف بوب:**

```python
class InboundSession:
    def on_es_received(self, es_message):
        # First ES received from Alice
        # This confirms which NSR Alice used
        
        # Clean up other handshake states
        for other_ns_state in self.pending_ns_states:
            if other_ns_state != self.active_ns_state:
                delete_ns_state(other_ns_state)
        
        # Delete unused NSR tagsets
        for tagset in self.nsr_tagsets:
            if tagset != self.active_nsr_tagset:
                delete_tagset(tagset)
        
        self.state = SessionState.ESTABLISHED
```
**الخصائص المهمة:**

1. **السماح بعدة NSR (مصطلح تقني يُترك بالإنجليزية)**: يمكن لـ Bob إرسال عدة NSR لكل NS (مصطلح تقني يُترك بالإنجليزية)
2. **مفاتيح مؤقتة مختلفة**: يجب أن يستخدم كل NSR مفتاحًا مؤقتًا فريدًا
3. **نفس tagset (مجموعة وسوم للتشفير) الخاصة بـ NSR**: تستخدم جميع NSR الخاصة بـ NS نفس tagset
4. **أول ES (مصطلح تقني يُترك بالإنجليزية) يفوز**: يحدد أول ES من Alice أي NSR نجح
5. **تنظيف بعد ES**: يتخلص Bob من الحالات غير المستخدمة بعد استلام ES

### آلة حالات الجلسة

**مخطط الحالة الكامل:**

```
                    Outbound Session                    Inbound Session

                         NEW
                          |
                     send NS
                          |
                   PENDING_REPLY -------------------- receive NS ---> ESTABLISHED
                          |                                                |
                   receive NSR                                        send NSR
                          |                                                |
                    ESTABLISHED <---------- receive ES ------------- AWAITING_ES
                          |                     |                          |
                    ┌─────┴─────┐               |                    receive ES
                    |           |               |                          |
              send ES      receive ES           |                    ESTABLISHED
                    |           |               |                          |
                    └─────┬─────┘               |                ┌─────────┴─────────┐
                          |                     |                |                   |
                          |                     |          send ES              receive ES
                          |                     |                |                   |
                          |                     |                └─────────┬─────────┘
                          |                     |                          |
                          └─────────────────────┴──────────────────────────┘
                                              ACTIVE
                                                |
                                         idle timeout
                                                |
                                             EXPIRED
```
**أوصاف الحالات:**

- **NEW**: تم إنشاء جلسة صادرة، لم يتم إرسال NS (رسالة بدء الجلسة) بعد
- **PENDING_REPLY**: تم إرسال NS، في انتظار NSR (رد بدء الجلسة)
- **AWAITING_ES**: تم إرسال NSR، في انتظار أول ES (رسالة بيانات مُشفّرة) من Alice
- **ESTABLISHED**: اكتملت المصافحة، ويمكن إرسال/استقبال ES
- **ACTIVE**: يتم تبادل رسائل ES بنشاط
- **RATCHETING**: DH ratchet (آلية تبديل مفاتيح تدريجية باستخدام Diffie-Hellman) قيد التنفيذ (جزء فرعي من ACTIVE)
- **EXPIRED**: انتهت مهلة الجلسة، بانتظار الحذف
- **TERMINATED**: تم إنهاء الجلسة بشكل صريح

---

## تنسيق الحمولة

يستخدم قسم الحمولة في جميع رسائل ECIES (مخطط تشفير متكامل بالمنحنيات البيضوية) (NS وNSR وES) تنسيقاً قائماً على الكتل مشابهاً لـ NTCP2.

### بنية الكتلة

**التنسيق العام:**

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**الحقول:**

- `blk`: 1 بايت - رقم نوع الكتلة
- `size`: 2 بايت - حجم حقل البيانات بصيغة Big-endian (ترتيب البايتات من الأكثر أهمية إلى الأقل) (0-65516)
- `data`: طول متغير - بيانات خاصة بالكتلة

**القيود:**

- الحد الأقصى لإطار ChaChaPoly (خوارزمية ChaCha20-Poly1305): 65535 بايت
- Poly1305 MAC (رمز مصادقة الرسالة): 16 بايت
- الحد الأقصى لإجمالي الكتل: 65519 بايت (65535 - 16)
- الحد الأقصى للكتلة الواحدة: 65519 بايت (بما في ذلك ترويسة بطول 3 بايت)
- الحد الأقصى لبيانات الكتلة الواحدة: 65516 بايت

### أنواع الكتل

**أنواع الكتل المُعرَّفة:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Required in NS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">9+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session termination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">21+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session options</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageNumbers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PN value</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NextKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 or 35 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH ratchet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message acknowledgment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK Request</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Request ACK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic Clove</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Application data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-223</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Testing features</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Traffic shaping</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future extension</td>
    </tr>
  </tbody>
</table>
**التعامل مع الكتلة غير المعروفة:**

يجب على عمليات التنفيذ تجاهل الكتل ذات أرقام النوع غير المعروفة واعتبارها حشواً. وهذا يضمن التوافق مع الإصدارات المستقبلية.

### قواعد ترتيب الكتل

### ترتيب رسائل NS

**إلزامي:** - يجب أن تكون كتلة DateTime هي الأولى

**المسموح:** - Garlic Clove (عُنصر فرعي داخل رسالة Garlic في I2P) (type 11) - الخيارات (type 5) - إذا كانت مُنفّذة - الحشو (type 254)

**محظور:** - NextKey, ACK, ACK Request, Termination, MessageNumbers

**مثال لحمولة NS صالحة:**

```
DateTime (0) | Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
### ترتيب رسائل NSR

**مطلوب:** - لا شيء (قد تكون الحمولة فارغة)

**مسموح:** - Garlic Clove (مصطلح تقني في I2P: جزء من آلية garlic encryption) (النوع 11) - الخيارات (النوع 5) - إذا كانت منفذة - الحشو (النوع 254)

**محظور:** - DateTime, NextKey, ACK, ACK Request, Termination, MessageNumbers

**مثال على حمولة NSR صالحة:**

```
Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
أو

```
(empty - ACK only)
```
### ترتيب رسائل ES

**مطلوب:** - لا شيء (قد تكون الحمولة فارغة)

**مسموح (بأي ترتيب):** - Garlic Clove (وحدة ضمن رسالة Garlic) (النوع 11) - NextKey (النوع 7) - ACK (النوع 8) - ACK Request (النوع 9) - Termination (النوع 4) - إن تم تنفيذها - MessageNumbers (النوع 6) - إن تم تنفيذها - Options (النوع 5) - إن تم تنفيذها - Padding (النوع 254)

**القواعد الخاصة:** - يجب أن تكون كتلة Termination (إنهاء) هي الأخيرة (باستثناء Padding (حشو)) - يجب أن تكون كتلة Padding هي الأخيرة - مسموح بوجود عدة Garlic Cloves (أجزاء رسالة Garlic) - مسموح بما يصل إلى 2 من كتل NextKey (المفتاح التالي) (اتجاه أمامي وعكسي) - غير مسموح بوجود عدة كتل Padding

**أمثلة على حمولات ES الصالحة:**

```
Garlic Clove (11) | ACK (8) | Padding (254)
```
```
NextKey (7) | Garlic Clove (11) | Garlic Clove (11)
```
```
NextKey (7) forward | NextKey (7) reverse | Garlic Clove (11)
```
```
ACK Request (9) | Garlic Clove (11) | Termination (4) | Padding (254)
```
### كتلة التاريخ والوقت (النوع 0)

**الغرض**: طابع زمني لمنع هجمات إعادة الإرسال والتحقق من انحراف الساعة

**الحجم**: 7 بايت (ترويسة 3 بايت + بيانات 4 بايت)

**التنسيق:**

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+
```
**الحقول:**

- `blk`: 0
- `size`: 4 (big-endian (ترتيب البايتات الكبير أولاً))
- `timestamp`: 4 بايتات - طابع زمني يونكس بالثواني (غير موقّع، big-endian)

**تنسيق الطابع الزمني:**

```python
timestamp = int(time.time())  # Seconds since 1970-01-01 00:00:00 UTC
# Wraps around in year 2106 (4-byte unsigned maximum)
```
**قواعد التحقق:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60      # 5 minutes
MAX_CLOCK_SKEW_FUTURE = 2 * 60    # 2 minutes

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        return False  # Too far in future
    
    if age > MAX_CLOCK_SKEW_PAST:
        return False  # Too old
    
    return True
```
**منع إعادة الإرسال:**

```python
class ReplayFilter:
    def __init__(self, duration=5*60):
        self.duration = duration  # 5 minutes
        self.seen_messages = BloomFilter(size=100000, false_positive_rate=0.001)
        self.cleanup_timer = RepeatTimer(60, self.cleanup)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Check timestamp validity
        if not validate_datetime(timestamp):
            return False
        
        # Check if ephemeral key seen recently
        if ephemeral_key in self.seen_messages:
            return False  # Replay attack
        
        # Add to seen messages
        self.seen_messages.add(ephemeral_key)
        return True
    
    def cleanup(self):
        # Expire old entries (Bloom filter automatically ages out)
        pass
```
**ملاحظات التنفيذ:**

1. **NS Messages** (رسائل NS): يجب أن تكون كتلة DateTime هي الأولى
2. **NSR/ES Messages** (رسائل NSR/ES): عادةً لا يتم تضمين DateTime
3. **Replay Window** (نافذة إعادة الإرسال): الحد الأدنى الموصى به هو 5 دقائق
4. **Bloom Filter** (مرشح بلوم): موصى به لاكتشاف إعادة الإرسال بكفاءة
5. **Clock Skew** (انحراف الساعة): اسمح بـ 5 دقائق في الماضي وبدقيقتين في المستقبل

### Garlic Clove Block (كتلة فصّ الثوم) (النوع 11)

**الغرض**: يغلّف رسائل I2NP لإيصالها

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration  |
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**الحقول:**

- `blk`: 11
- `size`: الحجم الكلي لـ clove (وحدة فرعية ضمن رسالة مركّبة في I2P) (متغيّر)
- `Delivery Instructions`: كما هو محدد في مواصفة I2NP
- `type`: نوع رسالة I2NP (1 بايت)
- `Message_ID`: معرّف رسالة I2NP (4 بايت)
- `Expiration`: طابع زمني يونكس بالثواني (4 بايت)
- `I2NP Message body`: بيانات رسالة بطول متغيّر

**تنسيقات تعليمات التسليم:**

**التسليم المحلي** (1 بايت):

```
+----+
|0x00|
+----+
```
**تسليم الوجهة** (33 بايت):

```
+----+----+----+----+----+----+----+----+
|0x01|                                  |
+----+        Destination Hash         +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**تسليم Router** (33 بايت):

```
+----+----+----+----+----+----+----+----+
|0x02|                                  |
+----+         Router Hash              +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**تسليم Tunnel** (37 بايت):

```
+----+----+----+----+----+----+----+----+
|0x03|         Tunnel ID                |
+----+----+----+----+----+              +
|           Router Hash                 |
+              32 bytes                 +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**ترويسة رسالة I2NP** (9 بايت إجمالاً):

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
     |                                   |
```
- `type`: نوع رسالة I2NP (تخزين قاعدة البيانات، استعلام قاعدة البيانات، بيانات، إلخ)
- `msg_id`: معرّف الرسالة بطول 4 بايت
- `expiration`: طابع زمني يونكس بطول 4 بايت (بالثواني)

**فروق مهمة مقارنةً بتنسيق ElGamal Clove:**

1. **بدون شهادة**: تم إغفال حقل الشهادة (غير مستخدم في ElGamal (خوارزمية تشفير بمفتاح عام))
2. **بدون معرّف Clove**: تم إغفال معرّف Clove (كان دائمًا 0)
3. **بدون انتهاء صلاحية Clove**: يستخدم انتهاء صلاحية رسالة I2NP بدلًا من ذلك
4. **ترويسة مضغّطة**: ترويسة I2NP بحجم 9 بايت مقابل تنسيق ElGamal الأكبر
5. **كل Clove كتلة منفصلة**: لا توجد بنية CloveSet

**عدة Cloves (فصوص رسائل ضمن garlic encryption):**

```python
# Multiple Garlic Cloves in one message
payload = [
    build_datetime_block(),
    build_garlic_clove(i2np_message_1),
    build_garlic_clove(i2np_message_2),
    build_garlic_clove(i2np_message_3),
    build_padding_block()
]
```
**أكثر أنواع رسائل I2NP شيوعًا ضمن الفصوص:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishing LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requesting LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK (legacy, avoid in ECIES)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Streaming data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Nested garlic messages</td>
    </tr>
  </tbody>
</table>
**معالجة الفصوص:**

```python
def process_garlic_clove(clove_data):
    # Parse delivery instructions
    delivery_type = clove_data[0]
    
    if delivery_type == 0x00:
        # Local delivery
        offset = 1
    elif delivery_type == 0x01:
        # Destination delivery
        dest_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x02:
        # Router delivery
        router_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x03:
        # Tunnel delivery
        tunnel_id = struct.unpack('>I', clove_data[1:5])[0]
        router_hash = clove_data[5:37]
        offset = 37
    
    # Parse I2NP header
    i2np_type = clove_data[offset]
    msg_id = struct.unpack('>I', clove_data[offset+1:offset+5])[0]
    expiration = struct.unpack('>I', clove_data[offset+5:offset+9])[0]
    
    # Extract I2NP body
    i2np_body = clove_data[offset+9:]
    
    # Process message
    process_i2np_message(i2np_type, msg_id, expiration, i2np_body)
```
### كتلة NextKey (النوع 7)

**الغرض**: تبادل المفاتيح عبر DH ratchet (آلية السقاطة القائمة على ديفي-هيلمان)

**التنسيق (المفتاح موجود - 38 بايت):**

```
+----+----+----+----+----+----+----+----+
| 7  |   35    |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+     Next DH Ratchet Public Key        +
|              32 bytes                 |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+
```
**التنسيق (معرّف المفتاح فقط - 6 بايت):**

```
+----+----+----+----+----+----+
| 7  |    3    |flag|  key ID |
+----+----+----+----+----+----+
```
**الحقول:**

- `blk`: 7
- `size`: 3 (المعرّف فقط) أو 35 (مع المفتاح)
- `flag`: 1 بايت - بتات العلم
- `key ID`: 2 بايت - مُعرِّف المفتاح بصيغة Big-endian (ترتيب البايتات من الأعلى إلى الأدنى) (0-32767)
- `Public Key`: 32 بايت - مفتاح X25519 عام بصيغة little-endian (ترتيب البايتات من الأدنى إلى الأعلى)، إذا كان بت العلم 0 = 1

**بتات العلم:**

```
Bit 7 6 5 4 3 2 1 0
    | | | | | | | |
    | | | | | | | +-- Bit 0: Key present (1) or ID only (0)
    | | | | | | +---- Bit 1: Reverse key (1) or forward key (0)
    | | | | | +------ Bit 2: Request reverse key (1) or no request (0)
    | | | | |
    +-+-+-+-+-------- Bits 3-7: Reserved (set to 0)
```
**أمثلة على الأعلام:**

```python
# Forward key present
flags = 0x01  # Binary: 00000001

# Reverse key present
flags = 0x03  # Binary: 00000011

# Forward key ID only (ACK)
flags = 0x00  # Binary: 00000000

# Reverse key ID only (ACK)
flags = 0x02  # Binary: 00000010

# Forward key ID with reverse request
flags = 0x04  # Binary: 00000100
```
**قواعد مُعرّف المفتاح:**

- المعرّفات متسلسلة: 0, 1, 2, ..., 32767
- يزداد المعرّف (بمقدار واحد) فقط عند توليد مفتاح جديد
- يُستخدم المعرّف نفسه لعدة رسائل حتى الـ ratchet (آلية تبديل المفاتيح في التشفير) التالية
- الحد الأقصى للمعرّف هو 32767 (يجب بدء جلسة جديدة بعدها)

**أمثلة الاستخدام:**

```python
# Initiating ratchet (sender generates new key)
nextkey = NextKeyBlock(
    flags=0x01,           # Key present, forward
    key_id=0,
    public_key=sender_new_pk
)

# Replying to ratchet (receiver generates new key)
nextkey = NextKeyBlock(
    flags=0x03,           # Key present, reverse
    key_id=0,
    public_key=receiver_new_pk
)

# Acknowledging ratchet (no new key from sender)
nextkey = NextKeyBlock(
    flags=0x02,           # ID only, reverse
    key_id=0
)

# Requesting reverse ratchet
nextkey = NextKeyBlock(
    flags=0x04,           # Request reverse, forward ID
    key_id=1
)
```
**منطق المعالجة:**

```python
def process_nextkey_block(block):
    flags = block.flags
    key_id = block.key_id
    
    key_present = (flags & 0x01) != 0
    is_reverse = (flags & 0x02) != 0
    request_reverse = (flags & 0x04) != 0
    
    if key_present:
        public_key = block.public_key
        
        if is_reverse:
            # Reverse key received
            perform_dh_ratchet(receiver_key=public_key, key_id=key_id)
            # Sender should ACK with own key ID
        else:
            # Forward key received
            perform_dh_ratchet(sender_key=public_key, key_id=key_id)
            # Receiver should reply with reverse key
            send_reverse_key(generate_new_key())
    
    else:
        # Key ID only (ACK)
        if is_reverse:
            # Reverse key ACK
            confirm_reverse_ratchet(key_id)
        else:
            # Forward key ACK
            confirm_forward_ratchet(key_id)
    
    if request_reverse:
        # Sender requests receiver to generate new key
        send_reverse_key(generate_new_key())
```
**عدّة كتل NextKey (المفتاح التالي):**

قد تحتوي رسالة ES (نوع رسالة ضمن I2P) واحدة على ما يصل إلى 2 من كتل NextKey عندما يكون كلا الاتجاهين يجريان ratcheting (آلية تبديل المفاتيح تدريجيًا) في الوقت نفسه:

```python
# Both directions ratcheting
payload = [
    NextKeyBlock(flags=0x01, key_id=2, public_key=forward_key),  # Forward
    NextKeyBlock(flags=0x03, key_id=1, public_key=reverse_key),  # Reverse
    build_garlic_clove(data)
]
```
### كتلة ACK (تأكيد الاستلام) (النوع 8)

**الغرض**: تأكيد استلام الرسائل ضمن القناة نفسها

**التنسيق (ACK (إقرار وصول) واحد - 7 بايت):**

```
+----+----+----+----+----+----+----+
| 8  |    4    |tagsetid |   N     |
+----+----+----+----+----+----+----+
```
**التنسيق (ACKs متعددة - تأكيدات الاستلام):**

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|            more ACKs                  |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**الحقول:**

- `blk`: 8
- `size`: 4 * عدد ACKs (تأكيدات الاستلام) (الحد الأدنى 4)
- لكل ACK:
  - `tagsetid`: 2 بايت - معرّف مجموعة الوسوم بصيغة Big-endian (ترتيب البايتات من الأعلى أهمية إلى الأقل) (0-65535)
  - `N`: 2 بايت - رقم الرسالة بصيغة Big-endian (0-65535)

**تحديد معرّف مجموعة الوسوم:**

```python
# Tag set 0 (initial, after NSR)
tagset_id = 0

# After first ratchet (tag set 1)
# Both Alice and Bob sent key ID 0
tagset_id = 1 + 0 + 0 = 1

# After second ratchet (tag set 2)
# Alice sent key ID 1, Bob still using key ID 0
tagset_id = 1 + 1 + 0 = 2

# After third ratchet (tag set 3)
# Alice still using key ID 1, Bob sent key ID 1
tagset_id = 1 + 1 + 1 = 3
```
**مثال واحد لـ ACK (إقرار الاستلام):**

```python
# ACK message from tag set 5, message number 127
ack_block = ACKBlock(
    tagset_id=5,
    message_number=127
)

# Wire format (7 bytes):
# 08 00 04 00 05 00 7F
# |  |  |  |  |  |  |
# |  |  |  |  |  |  +-- N (127)
# |  |  |  |  +--------- N high byte
# |  |  |  +------------ tagset_id (5)
# |  |  +--------------- tagset_id high byte
# |  +------------------ size (4)
# +--------------------- type (8)
```
**مثال لعدة ACKs (تأكيدات الاستلام):**

```python
# ACK three messages
ack_block = ACKBlock([
    (tagset_id=3, N=42),
    (tagset_id=3, N=43),
    (tagset_id=4, N=0)
])

# Wire format (15 bytes):
# 08 00 0C 00 03 00 2A 00 03 00 2B 00 04 00 00
#                (ts=3, N=42) (ts=3, N=43) (ts=4, N=0)
```
**المعالجة:**

```python
def process_ack_block(block):
    num_acks = block.size // 4
    
    for i in range(num_acks):
        offset = i * 4
        tagset_id = struct.unpack('>H', block.data[offset:offset+2])[0]
        message_num = struct.unpack('>H', block.data[offset+2:offset+4])[0]
        
        # Mark message as acknowledged
        mark_acked(tagset_id, message_num)
        
        # May trigger retransmission timeout cancellation
        cancel_retransmit_timer(tagset_id, message_num)
```
**متى يجب إرسال ACKs (تأكيدات الاستلام):**

1. **طلب إقرار (ACK) صريح**: الرد دائماً على كتلة طلب ACK
2. **تسليم LeaseSet**: عندما يضمّن المرسل LeaseSet في الرسالة
3. **إنشاء الجلسة**: قد يرسل ACK لـ NS/NSR (مع أن البروتوكول يفضّل ACK الضمني عبر ES)
4. **تأكيد Ratchet (آلية تدوير المفاتيح)**: قد يرسل ACK عند استلام NextKey
5. **طبقة التطبيقات**: حسب ما يتطلبه بروتوكول الطبقة الأعلى (مثلاً، Streaming)

**توقيت ACK:**

```python
class ACKManager:
    def __init__(self):
        self.pending_acks = []
        self.ack_timer = None
    
    def request_ack(self, tagset_id, message_num):
        self.pending_acks.append((tagset_id, message_num))
        
        if not self.ack_timer:
            # Delay ACK briefly to allow higher layer to respond
            self.ack_timer = set_timer(0.1, self.send_acks)  # 100ms
    
    def send_acks(self):
        if self.pending_acks and not has_outbound_data():
            # No higher layer data, send explicit ACK
            send_es_message(build_ack_block(self.pending_acks))
        
        # Otherwise, ACK will piggyback on next ES message
        self.pending_acks = []
        self.ack_timer = None
```
### كتلة طلب ACK (تأكيد الاستلام) (النوع 9)

**الغرض**: طلب تأكيد استلام ضمن نفس القناة (in-band) للرسالة الحالية

**التنسيق:**

```
+----+----+----+----+
| 9  |    1    |flg |
+----+----+----+----+
```
**الحقول:**

- `blk`: 9
- `size`: 1
- `flg`: 1 بايت - أعلام (جميع البتات غير مستخدمة حالياً، مُعيَّنة إلى 0)

**الاستخدام:**

```python
# Request ACK for this message
payload = [
    build_ack_request_block(),
    build_garlic_clove(important_data)
]
```
**استجابة المتلقي:**

عند استلام ACK Request (طلب تأكيد الاستلام):

1. **مع بيانات فورية**: تضمين كتلة ACK (إقرار) في الاستجابة الفورية
2. **بدون بيانات فورية**: ابدأ مؤقّتًا (على سبيل المثال، 100 مللي ثانية) وأرسل ES فارغة مع ACK (إقرار) إذا انتهت مهلة المؤقّت
3. **Tag Set ID (معرّف مجموعة الوسوم)**: استخدم tagset ID الوارد الحالي
4. **رقم الرسالة**: استخدم رقم الرسالة المرتبط بـ session tag (وسم الجلسة) المستلم

**المعالجة:**

```python
def process_ack_request(message):
    # Extract message identification
    tagset_id = message.tagset_id
    message_num = message.message_num
    
    # Schedule ACK
    schedule_ack(tagset_id, message_num)
    
    # If no data to send immediately, start timer
    if not has_pending_data():
        set_timer(0.1, lambda: send_ack_only(tagset_id, message_num))
```
**متى ينبغي استخدام ACK Request (طلب تأكيد الاستلام):**

1. **الرسائل الحرِجة**: رسائل يجب تأكيد استلامها
2. **تسليم LeaseSet**: عند تضمين LeaseSet
3. **Session Ratchet (آلية الراتشِت للجلسة)**: بعد إرسال كتلة NextKey
4. **نهاية الإرسال**: عندما لا يملك المُرسِل مزيدًا من البيانات لإرسالها لكنه يريد تأكيدًا

**متى لا يُنصح باستخدامه:**

1. **بروتوكول التدفق**: تتولى طبقة التدفق التعامل مع ACKs (إشعارات الاستلام)
2. **رسائل عالية التكرار**: تجنّب طلب ACK لكل رسالة (عبء إضافي)
3. **Datagrams غير مهمة**: عادةً لا تحتاج raw datagrams (رزم بيانات عديمة الاتصال) إلى ACKs

### كتلة الإنهاء (النوع 4)

**الحالة**: غير منفذ

**الغرض**: إنهاء الجلسة بشكل منظّم

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               ...                     ~
+----+----+----+----+----+----+----+----+
```
**الحقول:**

- `blk`: 4
- `size`: 1 بايت أو أكثر
- `rsn`: 1 بايت - رمز السبب
- `addl data`: بيانات إضافية اختيارية (يعتمد التنسيق على السبب)

**رموز الأسباب:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Additional Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Resource exhaustion</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implementation-specific</td>
    </tr>
  </tbody>
</table>
**الاستخدام (عند التنفيذ):**

```python
# Normal session close
termination = TerminationBlock(
    reason=0,
    additional_data=b''
)

# Session termination due to received termination
termination = TerminationBlock(
    reason=1,
    additional_data=b''
)
```
**القواعد:**

- يجب أن تكون آخر كتلة باستثناء Padding (الحشو)
- يجب أن يأتي Padding (الحشو) بعد Termination (الإنهاء) إذا وُجد
- غير مسموح في رسائل NS أو NSR
- مسموح فقط في رسائل ES

### كتلة الخيارات (النوع 5)

**الحالة**: غير مُنفّذ

**الغرض**: التفاوض على معلمات الجلسة

**الصيغة:**

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**الحقول:**

- `blk`: 5
- `size`: 21 بايتاً أو أكثر
- `ver`: 1 بايت - نسخة البروتوكول (يجب أن تكون 0)
- `flg`: 1 بايت - الأعلام (جميع البتات غير مستخدمة حالياً)
- `STL`: 1 بايت - طول وسم الجلسة (يجب أن يكون 8)
- `STimeout`: 2 بايت - مهلة خمول الجلسة بالثواني (big-endian، ترتيب البايتات من الأكثر أهمية إلى الأقل)
- `SOTW`: 2 بايت - نافذة الوسوم الصادرة لدى المرسِل (big-endian)
- `RITW`: 2 بايت - نافذة الوسوم الواردة لدى المستقبِل (big-endian)
- `tmin`, `tmax`, `rmin`, `rmax`: 1 بايت لكل منها - معلمات الحشو (بصيغة 4.4 ذات نقطة ثابتة)
- `tdmy`: 2 بايت - أقصى مقدار من حركة المرور الوهمية المستعد لإرساله (بايت/ثانية، big-endian)
- `rdmy`: 2 بايت - حركة المرور الوهمية المطلوبة (بايت/ثانية، big-endian)
- `tdelay`: 2 بايت - أقصى تأخير داخل الرسالة مستعد لإدراجه (مللي ثانية، big-endian)
- `rdelay`: 2 بايت - التأخير داخل الرسالة المطلوب (مللي ثانية، big-endian)
- `more_options`: متغير - امتدادات مستقبلية

**معلمات الحشو (تمثيل ثابت الفاصلة 4.4):**

```python
def encode_padding_ratio(ratio):
    """
    Encode padding ratio as 4.4 fixed-point
    
    ratio: 0.0 to 15.9375
    returns: 0x00 to 0xFF
    """
    return int(ratio * 16)

def decode_padding_ratio(encoded):
    """
    Decode 4.4 fixed-point to ratio
    
    encoded: 0x00 to 0xFF
    returns: 0.0 to 15.9375
    """
    return encoded / 16.0

# Examples:
# 0x00 = 0.0 (no padding)
# 0x01 = 0.0625 (6.25% padding)
# 0x10 = 1.0 (100% padding - double traffic)
# 0x80 = 8.0 (800% padding - 9x traffic)
# 0xFF = 15.9375 (1593.75% padding)
```
**التفاوض حول نافذة الوسوم:**

```python
# SOTW: Sender's recommendation for receiver's inbound window
# RITW: Sender's declaration of own inbound window

# Receiver calculates actual inbound window:
inbound_window = calculate_window(
    sender_suggestion=SOTW,
    own_constraints=MAX_INBOUND_TAGS,
    own_resources=available_memory()
)

# Sender uses:
# - RITW to know how far ahead receiver will accept
# - Own SOTW to hint optimal window size
```
**القيم الافتراضية (عندما لا يتم التفاوض على الخيارات):**

```python
DEFAULT_OPTIONS = {
    'version': 0,
    'session_tag_length': 8,
    'session_timeout': 600,  # 10 minutes
    'sender_outbound_tag_window': 160,
    'receiver_inbound_tag_window': 160,
    'tmin': 0x00,  # No minimum padding
    'tmax': 0x10,  # Up to 100% padding
    'rmin': 0x00,  # No minimum requested
    'rmax': 0x10,  # Up to 100% requested
    'tdmy': 0,     # No dummy traffic
    'rdmy': 0,     # No dummy traffic requested
    'tdelay': 0,   # No delay
    'rdelay': 0    # No delay requested
}
```
### كتلة أرقام الرسائل (النوع 6)

**الحالة**: غير مُنفّذ

**الغرض**: الإشارة إلى آخر رسالة مُرسلة في مجموعة الوسوم السابقة (يتيح الكشف عن الفجوات)

**التنسيق:**

```
+----+----+----+----+----+
| 6  |    2    |  PN    |
+----+----+----+----+----+
```
**الحقول:**

- `blk`: 6
- `size`: 2
- `PN`: 2 بايت - رقم آخر رسالة لمجموعة الوسوم السابقة (big-endian (ترتيب بايت كبير), 0-65535)

**تعريف PN (الرقم السابق):**

PN هو فهرس آخر وسم تم إرساله ضمن مجموعة الوسوم السابقة.

**الاستخدام (عند التنفيذ):**

```python
# After ratcheting to new tag set
# Old tag set: sent messages 0-4095
# New tag set: sending first message

payload = [
    MessageNumbersBlock(PN=4095),
    build_garlic_clove(data)
]
```
**مزايا المتلقي:**

```python
def process_message_numbers(pn_value):
    # Receiver can now:
    
    # 1. Determine if any messages were skipped
    highest_received_in_old_tagset = 4090
    if pn_value > highest_received_in_old_tagset:
        missing_count = pn_value - highest_received_in_old_tagset
        # 5 messages were never received
    
    # 2. Delete tags higher than PN from old tagset
    for tag_index in range(pn_value + 1, MAX_TAG_INDEX):
        delete_tag(old_tagset, tag_index)
    
    # 3. Expire tags ≤ PN after grace period (e.g., 2 minutes)
    schedule_deletion(old_tagset, delay=120)
```
**القواعد:**

- يجب ألا يُرسَل ضمن مجموعة الوسوم 0 (لا توجد مجموعة وسوم سابقة)
- يُرسَل فقط ضمن رسائل ES
- يُرسَل فقط في أول رسالة أو رسائل من مجموعة وسوم جديدة
- قيمة PN من منظور المُرسِل (آخر وسم أرسله المُرسِل)

**العلاقة بـ Signal:**

في خوارزمية Signal Double Ratchet، تكون PN ضمن رأس الرسالة. في ECIES (مخطط التشفير المتكامل بالمنحنيات الإهليلجية)، تكون داخل الحمولة المشفّرة وهي اختيارية.

### كتلة الحشو (النوع 254)

**الغرض**: مقاومة تحليل حركة المرور وتمويه حجم الرسائل

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**الحقول:**

- `blk`: 254
- `size`: 0-65516 بايت (big-endian: ترتيب البايت من الأكثر أهمية إلى الأقل)
- `padding`: بيانات عشوائية أو أصفار

**القواعد:**

- يجب أن تكون آخر كتلة في الرسالة
- لا يُسمح بوجود كتل حشو متعددة
- قد يكون بطول صفري (ترويسة من 3 بايت فقط)
- قد تكون بيانات الحشو أصفارًا أو بايتات عشوائية

**الحشو الافتراضي:**

```python
DEFAULT_PADDING_MIN = 0
DEFAULT_PADDING_MAX = 15

def generate_default_padding():
    size = random.randint(DEFAULT_PADDING_MIN, DEFAULT_PADDING_MAX)
    data = random.bytes(size)  # or zeros
    return PaddingBlock(size, data)
```
**استراتيجيات مقاومة تحليل حركة المرور:**

**الاستراتيجية 1: حجم عشوائي (الافتراضي)**

```python
# Add 0-15 bytes random padding to each message
padding_size = random.randint(0, 15)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**الاستراتيجية 2: التقريب إلى مضاعف**

```python
# Round total message size to next multiple of 64
target_size = ((message_size + 63) // 64) * 64
padding_size = target_size - message_size - 3  # -3 for block header
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**الاستراتيجية 3: أحجام الرسائل الثابتة**

```python
# Always send 1KB messages
TARGET_MESSAGE_SIZE = 1024
padding_size = TARGET_MESSAGE_SIZE - message_size - 3
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**الاستراتيجية 4: الحشو المتفاوض عليه (كتلة الخيارات)**

```python
# Calculate padding based on negotiated parameters
# tmin, tmax from Options block
min_padding = int(payload_size * tmin_ratio)
max_padding = int(payload_size * tmax_ratio)
padding_size = random.randint(min_padding, max_padding)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**رسائل الحشو فقط:**

قد تتكوّن الرسائل بالكامل من حشو (من دون بيانات تطبيق):

```python
# Dummy traffic message
payload = [
    PaddingBlock(random.randint(100, 500), random.bytes(...))
]
```
**ملاحظات التنفيذ:**

1. **حشو صفري بالكامل**: مقبول (سيُشفَّر بواسطة ChaCha20)
2. **حشو عشوائي**: لا يوفّر أماناً إضافياً بعد التشفير لكنه يستهلك إنتروبيا أكثر
3. **الأداء**: قد يكون إنشاء الحشو العشوائي مكلفاً حسابياً؛ فكّر في استخدام الأصفار
4. **الذاكرة**: كتل الحشو الكبيرة تستهلك عرض النطاق الترددي؛ كن حذراً بشأن الحجم الأقصى

---

## دليل التنفيذ

### المتطلبات الأساسية

**مكتبات التشفير:**

- **X25519**: libsodium، NaCl، أو Bouncy Castle
- **ChaCha20-Poly1305**: libsodium، OpenSSL 1.1.0+، أو Bouncy Castle
- **SHA-256**: OpenSSL، Bouncy Castle، أو الدعم المدمج في اللغة
- **Elligator2** (مخطط لإخفاء نقاط المنحنى الإهليلجي): دعم المكتبات محدود؛ قد يتطلب تنفيذًا مخصصًا

**تنفيذ Elligator2:**

Elligator2 (تقنية تشفيرية لتمثيل نقاط المنحنيات الإهليلجية كبيانات عشوائية لإخفاء المفاتيح العامة) ليست مُطبَّقة على نطاق واسع. الخيارات:

1. **OBFS4**: وسيلة النقل القابلة للإضافات الخاصة بـTor تتضمن تنفيذ Elligator2 (خوارزمية لإخفاء تمثيل نقاط المنحنى الإهليلجي لتبدو عشوائية)
2. **تنفيذ مخصص**: استنادًا إلى [ورقة Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf)
3. **kleshni/Elligator**: تنفيذ مرجعي على GitHub

**ملاحظة Java I2P:** تستخدم Java I2P مكتبة net.i2p.crypto.eddsa مع إضافات Elligator2 (خوارزمية لتمويه نقاط المنحنيات الإهليلجية) مخصصة.

### ترتيب التنفيذ الموصى به

**المرحلة 1: التشفير الأساسي** 1. توليد مفاتيح X25519 DH (ديفي‑هيلمان) وتبادلها 2. تشفير/فك تشفير ChaCha20-Poly1305 AEAD (تشفير موثّق مع بيانات مرتبطة) 3. تجزئة SHA-256 و MixHash (مزج التجزئة) 4. اشتقاق المفاتيح باستخدام HKDF (وظيفة اشتقاق مفاتيح معتمدة على HMAC) 5. ترميز/فك ترميز Elligator2 (خوارزمية إخفاء نقاط المنحنى الإهليلجي) (يمكن استخدام متجهات اختبار في البداية)

**المرحلة 2: تنسيقات الرسائل** 1. رسالة NS (غير مقيّدة) - أبسط تنسيق 2. رسالة NS (مقيّدة) - يضيف مفتاحاً ثابتاً 3. رسالة NSR 4. رسالة ES 5. تحليل الكتل وتوليدها

**المرحلة 3: إدارة الجلسة** 1. إنشاء الجلسة وتخزينها 2. إدارة مجموعة الوسوم (المرسل والمتلقّي) 3. ratchet لوسوم الجلسة (آلية تعاقب لتدوير المفاتيح تدريجياً) 4. ratchet للمفتاح المتماثل 5. استعلام الوسوم وإدارة النافذة

**المرحلة 4: DH Ratcheting (سقاطة ديفي-هيلمان)** 1. التعامل مع كتلة NextKey 2. KDF (دالة اشتقاق المفاتيح) لسقاطة DH 3. إنشاء مجموعة الوسوم بعد السقاطة 4. إدارة مجموعات وسوم متعددة

**المرحلة 5: منطق البروتوكول** 1. آلة حالة NS/NSR/ES (أنواع رسائل تفاوض الجلسة) 2. منع إعادة التشغيل (DateTime، مرشّح بلوم) 3. منطق إعادة الإرسال (عدّة NS/NSR) 4. معالجة ACK

**المرحلة 6: التكامل** 1. معالجة I2NP Garlic Clove (فص الثوم) 2. تجميع LeaseSet 3. تكامل بروتوكول التدفق 4. تكامل بروتوكول الداتاغرام

### تنفيذ المرسِل

**دورة حياة الجلسة الصادرة:**

```python
class OutboundSession:
    def __init__(self, destination, bound=True):
        self.destination = destination
        self.bound = bound
        self.state = SessionState.NEW
        
        # Keys for NS message
        self.ephemeral_keypair = generate_elg2_keypair()
        if bound:
            self.static_key = context.static_keypair
        
        # Will be populated after NSR
        self.outbound_tagset = None
        self.outbound_keyratchet = None
        self.inbound_tagset = None
        self.inbound_keyratchet = None
        
        # Timing
        self.created_time = now()
        self.last_activity = now()
        
        # Retransmission
        self.ns_attempts = []
        self.ns_timer = None
    
    def send_initial_message(self, payload):
        """Send NS message"""
        # Build NS message
        ns_message = self.build_ns_message(payload)
        
        # Send
        send_to_network(self.destination, ns_message)
        
        # Track for retransmission
        self.ns_attempts.append({
            'message': ns_message,
            'time': now(),
            'ephemeral_key': self.ephemeral_keypair,
            'kdf_state': self.save_kdf_state()
        })
        
        # Start timer
        self.ns_timer = set_timer(1.0, self.on_ns_timeout)
        self.state = SessionState.PENDING_REPLY
    
    def build_ns_message(self, payload):
        """Construct NS message"""
        # KDF initialization
        chainKey, h = self.initialize_kdf()
        
        # Ephemeral key section
        elg2_ephemeral = ENCODE_ELG2(self.ephemeral_keypair.public_key)
        h = SHA256(h || self.destination.static_key)
        h = SHA256(h || self.ephemeral_keypair.public_key)
        
        # es DH
        es_shared = DH(self.ephemeral_keypair.private_key, 
                       self.destination.static_key)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Encrypt static key section
        if self.bound:
            static_section = self.static_key.public_key
        else:
            static_section = bytes(32)
        
        static_ciphertext = ENCRYPT(k_static, 0, static_section, h)
        h = SHA256(h || static_ciphertext)
        
        # ss DH (if bound)
        if self.bound:
            ss_shared = DH(self.static_key.private_key, 
                          self.destination.static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        else:
            k_payload = k_static
            nonce = 1
        
        # Build payload blocks
        payload_data = self.build_ns_payload(payload)
        
        # Encrypt payload
        payload_ciphertext = ENCRYPT(k_payload, nonce, payload_data, h)
        h = SHA256(h || payload_ciphertext)
        
        # Save KDF state for NSR processing
        self.ns_chainkey = chainKey
        self.ns_hash = h
        
        # Assemble message
        return elg2_ephemeral + static_ciphertext + payload_ciphertext
    
    def build_ns_payload(self, application_data):
        """Build NS payload blocks"""
        blocks = []
        
        # DateTime block (required, first)
        blocks.append(build_datetime_block())
        
        # Garlic Clove(s) with application data
        blocks.append(build_garlic_clove(application_data))
        
        # Optionally bundle LeaseSet
        if should_send_leaseset():
            blocks.append(build_garlic_clove(build_leaseset_store()))
        
        # Padding
        blocks.append(build_padding_block(random.randint(0, 15)))
        
        return encode_blocks(blocks)
    
    def on_nsr_received(self, nsr_message):
        """Process NSR and establish ES session"""
        # Cancel retransmission timer
        cancel_timer(self.ns_timer)
        
        # Parse NSR
        tag = nsr_message[0:8]
        elg2_bob_ephemeral = nsr_message[8:40]
        key_section_mac = nsr_message[40:56]
        payload_ciphertext = nsr_message[56:]
        
        # Find corresponding NS attempt
        ns_state = self.find_ns_by_tag(tag)
        if not ns_state:
            raise ValueError("NSR tag doesn't match any NS")
        
        # Restore KDF state
        chainKey = ns_state['chainkey']
        h = ns_state['hash']
        
        # Decode Bob's ephemeral key
        bob_ephemeral = DECODE_ELG2(elg2_bob_ephemeral)
        
        # Mix tag and Bob's ephemeral into hash
        h = SHA256(h || tag)
        h = SHA256(h || bob_ephemeral)
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(self.static_key.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Verify key section MAC
        try:
            DECRYPT(k_key_section, 0, key_section_mac, h)
        except AuthenticationError:
            raise ValueError("NSR key section MAC verification failed")
        
        h = SHA256(h || key_section_mac)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Decrypt NSR payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        try:
            payload = DECRYPT(k_nsr, 0, payload_ciphertext, h)
        except AuthenticationError:
            raise ValueError("NSR payload MAC verification failed")
        
        # Process NSR payload blocks
        self.process_payload_blocks(payload)
        
        # Session established
        self.state = SessionState.ESTABLISHED
        self.last_activity = now()
        
        # Send ES message (implicit ACK)
        self.send_es_ack()
    
    def send_es_message(self, payload):
        """Send ES message"""
        if self.state != SessionState.ESTABLISHED:
            raise ValueError("Session not established")
        
        # Get next tag and key
        tag, index = self.outbound_tagset.get_next_tag()
        key = self.outbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Build payload blocks
        payload_data = self.build_es_payload(payload)
        
        # AEAD encryption
        ciphertext = ENCRYPT(key, nonce, payload_data, tag)
        
        # Assemble message
        es_message = tag + ciphertext
        
        # Send
        send_to_network(self.destination, es_message)
        
        # Update activity
        self.last_activity = now()
        
        # Check if ratchet needed
        if self.outbound_tagset.should_ratchet():
            self.initiate_ratchet()
```
### تنفيذ المستقبِل

**دورة حياة الجلسة الواردة:**

```python
class InboundSession:
    def __init__(self):
        self.state = None
        self.bound = False
        self.destination = None
        
        # Keys
        self.remote_ephemeral_key = None
        self.remote_static_key = None
        self.ephemeral_keypair = None
        
        # Tagsets
        self.inbound_tagset = None
        self.outbound_tagset = None
        
        # Timing
        self.created_time = None
        self.last_activity = None
        
        # Paired session
        self.paired_outbound = None
    
    @staticmethod
    def try_decrypt_ns(message):
        """Attempt to decrypt as NS message"""
        # Parse NS structure
        elg2_ephemeral = message[0:32]
        static_ciphertext = message[32:80]  # 32 + 16
        payload_ciphertext = message[80:]
        
        # Decode ephemeral key
        try:
            alice_ephemeral = DECODE_ELG2(elg2_ephemeral)
        except:
            return None  # Not a valid Elligator2 encoding
        
        # Check replay
        if is_replay(alice_ephemeral):
            return None
        
        # KDF initialization
        chainKey, h = initialize_kdf()
        
        # Mix keys
        h = SHA256(h || context.static_keypair.public_key)
        h = SHA256(h || alice_ephemeral)
        
        # es DH
        es_shared = DH(context.static_keypair.private_key, alice_ephemeral)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Decrypt static key section
        try:
            static_data = DECRYPT(k_static, 0, static_ciphertext, h)
        except AuthenticationError:
            return None  # Not a valid NS message
        
        h = SHA256(h || static_ciphertext)
        
        # Check if bound or unbound
        if static_data == bytes(32):
            # Unbound
            alice_static_key = None
            k_payload = k_static
            nonce = 1
        else:
            # Bound - perform ss DH
            alice_static_key = static_data
            ss_shared = DH(context.static_keypair.private_key, alice_static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        
        # Decrypt payload
        try:
            payload = DECRYPT(k_payload, nonce, payload_ciphertext, h)
        except AuthenticationError:
            return None
        
        h = SHA256(h || payload_ciphertext)
        
        # Create session
        session = InboundSession()
        session.state = SessionState.ESTABLISHED
        session.created_time = now()
        session.last_activity = now()
        session.remote_ephemeral_key = alice_ephemeral
        session.remote_static_key = alice_static_key
        session.bound = (alice_static_key is not None)
        session.ns_chainkey = chainKey
        session.ns_hash = h
        
        # Extract destination if bound
        if session.bound:
            session.destination = extract_destination_from_payload(payload)
        
        # Process payload
        session.process_payload_blocks(payload)
        
        return session
    
    def send_nsr_reply(self, reply_payload):
        """Send NSR message"""
        # Generate NSR tagset
        tagsetKey = HKDF(self.ns_chainkey, ZEROLEN, "SessionReplyTags", 32)
        nsr_tagset = DH_INITIALIZE(self.ns_chainkey, tagsetKey)
        
        # Get tag
        tag, _ = nsr_tagset.get_next_tag()
        
        # Mix tag into hash
        h = SHA256(self.ns_hash || tag)
        
        # Generate ephemeral key
        self.ephemeral_keypair = generate_elg2_keypair()
        bob_ephemeral = self.ephemeral_keypair.public_key
        elg2_bob_ephemeral = ENCODE_ELG2(bob_ephemeral)
        
        # Mix ephemeral key
        h = SHA256(h || bob_ephemeral)
        
        chainKey = self.ns_chainkey
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(context.static_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Encrypt key section (empty)
        key_section_ciphertext = ENCRYPT(k_key_section, 0, ZEROLEN, h)
        h = SHA256(h || key_section_ciphertext)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Build reply payload
        payload_data = build_payload_blocks(reply_payload)
        
        # Encrypt payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        payload_ciphertext = ENCRYPT(k_nsr, 0, payload_data, h)
        
        # Assemble NSR
        nsr_message = tag + elg2_bob_ephemeral + key_section_ciphertext + payload_ciphertext
        
        # Send
        send_to_network(self.destination, nsr_message)
        
        # Wait for ES
        self.state = SessionState.AWAITING_ES
        self.last_activity = now()
    
    def on_es_received(self, es_message):
        """Process first ES message"""
        if self.state == SessionState.AWAITING_ES:
            # First ES received, confirms session
            self.state = SessionState.ESTABLISHED
        
        # Process ES message
        self.process_es_message(es_message)
    
    def process_es_message(self, es_message):
        """Decrypt and process ES message"""
        # Extract tag
        tag = es_message[0:8]
        ciphertext = es_message[8:]
        
        # Look up tag
        index = self.inbound_tagset.lookup_tag(tag)
        if index is None:
            raise ValueError("Tag not found")
        
        # Get key
        key = self.inbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Decrypt
        try:
            payload = DECRYPT(key, nonce, ciphertext, tag)
        except AuthenticationError:
            raise ValueError("ES MAC verification failed")
        
        # Process blocks
        self.process_payload_blocks(payload)
        
        # Update activity
        self.last_activity = now()
```
### تصنيف الرسائل

**تمييز أنواع الرسائل:**

```python
def classify_message(message):
    """Determine message type"""
    
    # Minimum lengths
    if len(message) < 24:
        return None  # Too short
    
    # Check for session tag (8 bytes)
    tag = message[0:8]
    
    # Try ES decryption first (most common)
    session = lookup_session_by_tag(tag)
    if session:
        return ('ES', session)
    
    # Try NSR decryption (tag + Elligator2 key)
    if len(message) >= 72:
        # Check if bytes 8-40 are valid Elligator2
        try:
            nsr_ephemeral = DECODE_ELG2(message[8:40])
            nsr_session = find_pending_nsr_by_tag(tag)
            if nsr_session:
                return ('NSR', nsr_session)
        except:
            pass
    
    # Try NS decryption (starts with Elligator2 key)
    if len(message) >= 96:
        try:
            ns_ephemeral = DECODE_ELG2(message[0:32])
            ns_session = InboundSession.try_decrypt_ns(message)
            if ns_session:
                return ('NS', ns_session)
        except:
            pass
    
    # Check ElGamal/AES (for dual-key compatibility)
    if len(message) >= 514:
        if (len(message) - 2) % 16 == 0:
            # Might be ElGamal NS
            return ('ELGAMAL_NS', None)
        elif len(message) % 16 == 0:
            # Might be ElGamal ES
            return ('ELGAMAL_ES', None)
    
    return None  # Unknown message type
```
### أفضل الممارسات لإدارة الجلسات

**تخزين الجلسة:**

```python
class SessionKeyManager:
    def __init__(self):
        # Outbound sessions (one per destination)
        self.outbound_sessions = {}  # destination -> OutboundSession
        
        # Inbound sessions (multiple per destination during transition)
        self.inbound_sessions = []  # [InboundSession]
        
        # Session tag lookup (fast path for ES messages)
        self.tag_to_session = {}  # tag -> InboundSession
        
        # Limits
        self.max_inbound_sessions = 1000
        self.max_tags_per_session = 160
    
    def get_outbound_session(self, destination):
        """Get or create outbound session"""
        if destination not in self.outbound_sessions:
            session = OutboundSession(destination)
            self.outbound_sessions[destination] = session
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session):
        """Add new inbound session"""
        # Check limits
        if len(self.inbound_sessions) >= self.max_inbound_sessions:
            self.expire_oldest_session()
        
        self.inbound_sessions.append(session)
        
        # Add tags to lookup table
        self.register_session_tags(session)
    
    def register_session_tags(self, session):
        """Register session's tags in lookup table"""
        for tag in session.inbound_tagset.get_all_tags():
            self.tag_to_session[tag] = session
    
    def lookup_tag(self, tag):
        """Fast tag lookup"""
        return self.tag_to_session.get(tag)
    
    def expire_sessions(self):
        """Periodic session expiration"""
        now_time = now()
        
        # Expire outbound sessions
        for dest, session in list(self.outbound_sessions.items()):
            if session.idle_time(now_time) > 8 * 60:
                del self.outbound_sessions[dest]
        
        # Expire inbound sessions
        expired = []
        for session in self.inbound_sessions:
            if session.idle_time(now_time) > 10 * 60:
                expired.append(session)
        
        for session in expired:
            self.remove_inbound_session(session)
    
    def remove_inbound_session(self, session):
        """Remove inbound session and clean up tags"""
        self.inbound_sessions.remove(session)
        
        # Remove tags from lookup
        for tag in session.inbound_tagset.get_all_tags():
            if tag in self.tag_to_session:
                del self.tag_to_session[tag]
```
**إدارة الذاكرة:**

```python
class TagMemoryManager:
    def __init__(self, max_memory_kb=10240):  # 10 MB default
        self.max_memory = max_memory_kb * 1024
        self.current_memory = 0
        self.max_tags_per_session = 160
        self.min_tags_per_session = 32
    
    def calculate_tag_memory(self, session):
        """Calculate memory used by session tags"""
        tag_count = len(session.inbound_tagset.tags)
        # Each tag: 8 bytes (tag) + 2 bytes (index) + 32 bytes (key, optional)
        # + overhead
        bytes_per_tag = 16 if session.defer_keys else 48
        return tag_count * bytes_per_tag
    
    def check_pressure(self):
        """Check if under memory pressure"""
        return self.current_memory > (self.max_memory * 0.9)
    
    def handle_pressure(self):
        """Reduce memory usage when under pressure"""
        if not self.check_pressure():
            return
        
        # Strategy 1: Reduce look-ahead windows
        for session in all_sessions:
            if session.look_ahead > self.min_tags_per_session:
                session.reduce_look_ahead(self.min_tags_per_session)
        
        # Strategy 2: Trim old tags aggressively
        for session in all_sessions:
            session.inbound_tagset.trim_behind(aggressive=True)
        
        # Strategy 3: Refuse new ratchets
        for session in all_sessions:
            if session.outbound_tagset.should_ratchet():
                session.defer_ratchet = True
        
        # Strategy 4: Expire idle sessions early
        expire_idle_sessions(threshold=5*60)  # 5 min instead of 10
```
### استراتيجيات الاختبار

**اختبارات الوحدة:**

```python
def test_x25519_dh():
    """Test X25519 key exchange"""
    alice_sk = GENERATE_PRIVATE()
    alice_pk = DERIVE_PUBLIC(alice_sk)
    
    bob_sk = GENERATE_PRIVATE()
    bob_pk = DERIVE_PUBLIC(bob_sk)
    
    # Both sides compute same shared secret
    alice_shared = DH(alice_sk, bob_pk)
    bob_shared = DH(bob_sk, alice_pk)
    
    assert alice_shared == bob_shared

def test_elligator2_encode_decode():
    """Test Elligator2 roundtrip"""
    sk = GENERATE_PRIVATE_ELG2()
    pk = DERIVE_PUBLIC(sk)
    
    encoded = ENCODE_ELG2(pk)
    decoded = DECODE_ELG2(encoded)
    
    assert decoded == pk

def test_chacha_poly_encrypt_decrypt():
    """Test ChaCha20-Poly1305 AEAD"""
    key = CSRNG(32)
    nonce = construct_nonce(42)
    plaintext = b"Hello, I2P!"
    ad = b"associated_data"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    decrypted = DECRYPT(key, nonce, ciphertext, ad)
    
    assert decrypted == plaintext

def test_session_tag_ratchet():
    """Test session tag generation"""
    sessTag_ck = CSRNG(32)
    tagset = SessionTagRatchet(sessTag_ck)
    
    # Generate 100 tags
    tags = [tagset.get_next_tag() for _ in range(100)]
    
    # All tags should be unique
    assert len(set(tags)) == 100
    
    # Each tag should be 8 bytes
    for tag in tags:
        assert len(tag) == 8
```
**اختبارات التكامل:**

```python
def test_ns_nsr_handshake():
    """Test NS/NSR handshake"""
    # Alice creates outbound session
    alice_session = OutboundSession(bob_destination, bound=True)
    
    # Alice sends NS
    ns_message = alice_session.build_ns_message(b"Hello Bob")
    
    # Bob receives NS
    bob_session = InboundSession.try_decrypt_ns(ns_message)
    assert bob_session is not None
    assert bob_session.bound == True
    
    # Bob sends NSR
    nsr_message = bob_session.build_nsr_message(b"Hello Alice")
    
    # Alice receives NSR
    alice_session.on_nsr_received(nsr_message)
    assert alice_session.state == SessionState.ESTABLISHED
    
    # Both should have matching ES tagsets
    # (Cannot directly compare, but can test by sending ES messages)

def test_es_bidirectional():
    """Test ES messages in both directions"""
    # (After NS/NSR handshake)
    
    # Alice sends ES to Bob
    es_alice_to_bob = alice_session.send_es_message(b"Data from Alice")
    
    # Bob receives ES
    bob_session.process_es_message(es_alice_to_bob)
    
    # Bob sends ES to Alice
    es_bob_to_alice = bob_session.send_es_message(b"Data from Bob")
    
    # Alice receives ES
    alice_session.process_es_message(es_bob_to_alice)

def test_dh_ratchet():
    """Test DH ratchet"""
    # (After established session)
    
    # Alice initiates ratchet
    alice_session.initiate_ratchet()
    nextkey_alice = build_nextkey_block(
        flags=0x01,
        key_id=0,
        public_key=alice_new_key
    )
    
    # Send to Bob
    bob_session.process_nextkey_block(nextkey_alice)
    
    # Bob replies
    nextkey_bob = build_nextkey_block(
        flags=0x03,
        key_id=0,
        public_key=bob_new_key
    )
    
    # Send to Alice
    alice_session.process_nextkey_block(nextkey_bob)
    
    # Both should now be using new tagsets
    assert alice_session.outbound_tagset.id == 1
    assert bob_session.inbound_tagset.id == 1
```
**متجهات الاختبار:**

نفذ متجهات الاختبار من المواصفة:

1. **Noise IK Handshake** (مصافحة بروتوكول Noise بنمط IK): استخدم متجهات الاختبار القياسية لـ Noise
2. **HKDF** (دالة اشتقاق المفاتيح القائمة على HMAC): استخدم متجهات الاختبار من RFC 5869
3. **ChaCha20-Poly1305** (خوارزمية تشفير ومصادقة AEAD): استخدم متجهات الاختبار من RFC 7539
4. **Elligator2** (تقنية لإخفاء تمثيل نقاط المنحنى الإهليلجي): استخدم متجهات الاختبار من الورقة البحثية لـ Elligator2 أو OBFS4

**اختبارات قابلية التشغيل البيني:**

1. **Java I2P**: اختبر مقابل التنفيذ المرجعي لـ Java I2P
2. **i2pd**: اختبر مقابل تنفيذ i2pd بلغة C++
3. **التقاطات الحزم**: استخدم dissector (المحلّل) في Wireshark (إن توفّر) للتحقق من تنسيقات الرسائل
4. **عبر التنفيذات**: أنشئ test harness (إطار اختبار) يمكنه الإرسال والاستقبال بين التنفيذات

### اعتبارات الأداء

**توليد المفاتيح:**

توليد مفاتيح Elligator2 (خوارزمية تمويه للمفاتيح العامة) مكلف حسابيًا (معدل رفض 50%):

```python
class KeyPool:
    """Pre-generate keys in background thread"""
    def __init__(self, pool_size=10):
        self.pool = Queue(maxsize=pool_size)
        self.generator_thread = Thread(target=self.generate_keys, daemon=True)
        self.generator_thread.start()
    
    def generate_keys(self):
        while True:
            if not self.pool.full():
                keypair = generate_elg2_keypair()
                # Also compute encoded form
                encoded = ENCODE_ELG2(keypair.public_key)
                self.pool.put((keypair, encoded))
            else:
                sleep(0.1)
    
    def get_keypair(self):
        try:
            return self.pool.get(timeout=1.0)
        except Empty:
            # Pool exhausted, generate inline
            return generate_elg2_keypair()
```
**البحث عن الوسم:**

استخدم جداول التجزئة للبحث عن الوسوم بزمن O(1):

```python
class FastTagLookup:
    def __init__(self):
        self.tag_to_session = {}  # Python dict is hash table
    
    def add_tag(self, tag, session, index):
        # 8-byte tag as bytes is hashable
        self.tag_to_session[tag] = (session, index)
    
    def lookup_tag(self, tag):
        return self.tag_to_session.get(tag)
```
**تحسين الذاكرة:**

تأجيل توليد المفتاح المتماثل:

```python
class DeferredKeyRatchet:
    """Only generate keys when needed"""
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = LRUCache(maxsize=32)  # Cache recent keys
    
    def get_key(self, index):
        # Check cache first
        if index in self.cache:
            return self.cache[index]
        
        # Generate keys up to index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                key = keydata[32:63]
                self.cache[index] = key
                return key
```
**المعالجة الدفعية:**

معالجة عدة رسائل دفعة واحدة:

```python
def process_message_batch(messages):
    """Process multiple messages efficiently"""
    results = []
    
    # Group by type
    ns_messages = []
    nsr_messages = []
    es_messages = []
    
    for msg in messages:
        msg_type = classify_message(msg)
        if msg_type[0] == 'NS':
            ns_messages.append(msg)
        elif msg_type[0] == 'NSR':
            nsr_messages.append(msg)
        elif msg_type[0] == 'ES':
            es_messages.append(msg)
    
    # Process in batches
    # ES messages are most common, process first
    for msg in es_messages:
        results.append(process_es_message(msg))
    
    for msg in nsr_messages:
        results.append(process_nsr_message(msg))
    
    for msg in ns_messages:
        results.append(process_ns_message(msg))
    
    return results
```
---

## اعتبارات أمنية

### نموذج التهديد

**قدرات الخصم:**

1. **مراقب سلبي**: يمكنه رصد جميع حركة المرور على الشبكة
2. **مهاجم نشط**: يمكنه حقن الرسائل، وتعديلها، وإسقاطها، وإعادة إرسالها
3. **عقدة مخترقة**: قد يختَرِق router أو وجهة
4. **تحليل حركة المرور**: يمكنه إجراء تحليل إحصائي لأنماط حركة المرور

**أهداف الأمان:**

1. **السرية**: محتوى الرسائل مخفي عن المُراقِب
2. **التحقق من الهوية**: تم التحقق من هوية المرسِل (للجلسات المرتبطة)
3. **السرية الأمامية**: تظل الرسائل السابقة سرية حتى إذا تم اختراق المفاتيح
4. **منع إعادة التشغيل**: لا يمكن إعادة تشغيل الرسائل القديمة
5. **تمويه حركة المرور**: مصافحات لا يمكن تمييزها عن بيانات عشوائية

### افتراضات التشفير

**افتراضات الصعوبة:**

1. **X25519 CDH**: تُعدّ مسألة ديفي‑هيلمان الحسابية صعبة حسابياً على المنحنى Curve25519
2. **ChaCha20 PRF**: ChaCha20 عبارة عن دالة شبه عشوائية
3. **Poly1305 MAC**: Poly1305 غير قابلة للتزوير تحت هجوم الرسائل المختارة
4. **SHA-256 CR**: SHA-256 مقاومة للتصادمات
5. **HKDF Security**: HKDF يستخلص ويُوسّع مفاتيح موزعة توزيعاً منتظماً

**مستويات الأمان:**

- **X25519**: ~128-بت من الأمن (رتبة المنحنى 2^252)
- **ChaCha20**: مفاتيح 256-بت، أمن 256-بت
- **Poly1305**: أمن 128-بت (احتمال التصادم)
- **SHA-256**: مقاومة التصادم 128-بت، مقاومة الصورة الأولية 256-بت

### إدارة المفاتيح

**توليد المفاتيح:**

```python
# CRITICAL: Use cryptographically secure RNG
def CSRNG(length):
    # GOOD: os.urandom, secrets.token_bytes (Python)
    # GOOD: /dev/urandom (Linux)
    # GOOD: BCryptGenRandom (Windows)
    # BAD: random.random(), Math.random() (NOT cryptographically secure)
    return os.urandom(length)

# CRITICAL: Validate keys
def validate_x25519_key(pubkey):
    # Check for weak keys (all zeros, small order points)
    if pubkey == bytes(32):
        raise WeakKeyError("All-zero public key")
    
    # Perform DH to check for weak shared secrets
    test_shared = DH(test_private_key, pubkey)
    if test_shared == bytes(32):
        raise WeakKeyError("Results in zero shared secret")
```
**تخزين المفاتيح:**

```python
# CRITICAL: Protect private keys
class SecureKeyStorage:
    def __init__(self):
        # Store in memory with protection
        self.keys = {}
        
        # Option 1: Memory locking (prevent swapping to disk)
        # mlock(self.keys)
        
        # Option 2: Encrypted storage
        # self.encryption_key = derive_from_password()
    
    def store_key(self, key_id, private_key):
        # Option: Encrypt before storage
        # encrypted = encrypt(private_key, self.encryption_key)
        # self.keys[key_id] = encrypted
        self.keys[key_id] = private_key
    
    def delete_key(self, key_id):
        # Securely wipe memory
        if key_id in self.keys:
            key = self.keys[key_id]
            # Overwrite with zeros before deletion
            for i in range(len(key)):
                key[i] = 0
            del self.keys[key_id]
```
**تدوير المفاتيح:**

```python
# CRITICAL: Rotate keys regularly
class KeyRotationPolicy:
    def __init__(self):
        self.max_messages_per_tagset = 4096  # Ratchet before 65535
        self.max_tagset_age = 10 * 60       # 10 minutes
        self.max_session_age = 60 * 60      # 1 hour
    
    def should_ratchet(self, tagset):
        return (tagset.messages_sent >= self.max_messages_per_tagset or
                tagset.age() >= self.max_tagset_age)
    
    def should_replace_session(self, session):
        return session.age() >= self.max_session_age
```
### إجراءات التخفيف من الهجمات

### تدابير التخفيف من هجمات إعادة الإرسال

**التحقق من صحة التاريخ والوقت:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60
MAX_CLOCK_SKEW_FUTURE = 2 * 60

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        raise ReplayError("Timestamp too far in future")
    
    if age > MAX_CLOCK_SKEW_PAST:
        raise ReplayError("Timestamp too old")
    
    return True
```
**مرشح بلوم لرسائل NS:**

```python
class ReplayFilter:
    def __init__(self, capacity=100000, error_rate=0.001, duration=5*60):
        self.bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
        self.duration = duration
        self.entries = []  # (timestamp, ephemeral_key)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Validate timestamp
        if not validate_datetime(timestamp):
            return False
        
        # Check Bloom filter
        if ephemeral_key in self.bloom:
            # Potential replay (or false positive)
            # Check exact match in entries
            for ts, key in self.entries:
                if key == ephemeral_key:
                    return False  # Definite replay
        
        # Add to filter
        self.bloom.add(ephemeral_key)
        self.entries.append((timestamp, ephemeral_key))
        
        # Expire old entries
        self.expire_old_entries()
        
        return True
    
    def expire_old_entries(self):
        now = int(time.time())
        self.entries = [(ts, key) for ts, key in self.entries
                       if now - ts < self.duration]
```
**وسم الجلسة للاستخدام مرة واحدة:**

```python
def process_session_tag(tag):
    # Look up tag
    entry = tagset.lookup_tag(tag)
    if entry is None:
        raise ValueError("Invalid session tag")
    
    # CRITICAL: Remove tag immediately (one-time use)
    tagset.remove_tag(tag)
    
    # Use associated key
    return entry.key, entry.index
```
### إجراءات التخفيف من Key Compromise Impersonation (KCI) (انتحال الهوية نتيجة اختراق المفتاح)

**المشكلة**: مصادقة رسائل NS معرّضة لهجوم KCI (انتحال الهوية عند انكشاف المفتاح) (مستوى المصادقة 1)

**التخفيف**:

1. انتقل إلى NSR (مستوى المصادقة 2) بأسرع ما يمكن
2. لا تثق بـحمولة NS في العمليات الحرجة أمنياً
3. انتظر تأكيد NSR قبل تنفيذ إجراءات لا رجعة فيها

```python
def process_ns_message(ns_message):
    # NS authenticated at Level 1 (KCI vulnerable)
    # Do NOT perform security-critical operations yet
    
    # Extract sender's static key
    sender_key = ns_message.static_key
    
    # Mark session as pending Level 2 authentication
    session.auth_level = 1
    session.sender_key = sender_key
    
    # Send NSR
    send_nsr_reply(session)

def process_first_es_message(es_message):
    # Now we have Level 2 authentication (KCI resistant)
    session.auth_level = 2
    
    # Safe to perform security-critical operations
    process_security_critical_operation(es_message)
```
### تدابير التخفيف من هجمات حجب الخدمة

**الحماية من إغراق NS:**

```python
class NSFloodProtection:
    def __init__(self):
        self.ns_count = defaultdict(int)  # source -> count
        self.ns_timestamps = defaultdict(list)  # source -> [timestamps]
        
        self.max_ns_per_source = 5
        self.rate_window = 10  # seconds
        self.max_concurrent_ns = 100
    
    def check_ns_allowed(self, source):
        # Global limit
        total_pending = sum(self.ns_count.values())
        if total_pending >= self.max_concurrent_ns:
            return False
        
        # Per-source rate limit
        now = time.time()
        timestamps = self.ns_timestamps[source]
        
        # Remove old timestamps
        timestamps = [ts for ts in timestamps if now - ts < self.rate_window]
        self.ns_timestamps[source] = timestamps
        
        # Check rate
        if len(timestamps) >= self.max_ns_per_source:
            return False
        
        # Allow NS
        timestamps.append(now)
        self.ns_count[source] += 1
        return True
    
    def on_session_established(self, source):
        # Decrease pending count
        if self.ns_count[source] > 0:
            self.ns_count[source] -= 1
```
**حدود تخزين الوسوم:**

```python
class TagStorageLimit:
    def __init__(self, max_tags=1000000):
        self.max_tags = max_tags
        self.current_tags = 0
    
    def can_create_session(self, look_ahead):
        if self.current_tags + look_ahead > self.max_tags:
            return False
        return True
    
    def add_tags(self, count):
        self.current_tags += count
    
    def remove_tags(self, count):
        self.current_tags -= count
```
**الإدارة التكيفية للموارد:**

```python
class AdaptiveResourceManager:
    def __init__(self):
        self.load_level = 0  # 0 = low, 1 = medium, 2 = high, 3 = critical
    
    def adjust_parameters(self):
        if self.load_level == 0:
            # Normal operation
            return {
                'max_look_ahead': 160,
                'max_sessions': 1000,
                'session_timeout': 10 * 60
            }
        
        elif self.load_level == 1:
            # Moderate load
            return {
                'max_look_ahead': 80,
                'max_sessions': 800,
                'session_timeout': 8 * 60
            }
        
        elif self.load_level == 2:
            # High load
            return {
                'max_look_ahead': 32,
                'max_sessions': 500,
                'session_timeout': 5 * 60
            }
        
        else:  # load_level == 3
            # Critical load
            return {
                'max_look_ahead': 16,
                'max_sessions': 200,
                'session_timeout': 3 * 60
            }
```
### مقاومة تحليل حركة المرور

**ترميز Elligator2 (تقنية ترميز تجعل نقاط المنحنى الإهليلجي تبدو كبيانات عشوائية):**

يضمن أن رسائل المصافحة غير قابلة للتمييز عن العشوائية:

```python
# NS and NSR start with Elligator2-encoded ephemeral keys
# Observer cannot distinguish from random 32-byte string
```
**استراتيجيات الحشو:**

```python
# Resist message size fingerprinting
def add_padding(payload, strategy='random'):
    if strategy == 'random':
        # Random padding 0-15 bytes
        size = random.randint(0, 15)
    
    elif strategy == 'round':
        # Round to next 64-byte boundary
        target = ((len(payload) + 63) // 64) * 64
        size = target - len(payload) - 3  # -3 for block header
    
    elif strategy == 'fixed':
        # Always 1KB messages
        size = 1024 - len(payload) - 3
    
    return build_padding_block(size)
```
**هجمات التوقيت:**

```python
# CRITICAL: Use constant-time operations
def constant_time_compare(a, b):
    """Constant-time byte string comparison"""
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    
    return result == 0

# CRITICAL: Constant-time MAC verification
def verify_mac(computed_mac, received_mac):
    if not constant_time_compare(computed_mac, received_mac):
        # Always take same time regardless of where comparison fails
        raise AuthenticationError("MAC verification failed")
```
### مزالق التنفيذ

**الأخطاء الشائعة:**

1. **إعادة استخدام Nonce (عدد يُستخدم مرة واحدة)**: لا تُعِد أبدًا استخدام أزواج (key, nonce)
   ```python
   # BAD: Reusing nonce with same key
   ciphertext1 = ENCRYPT(key, nonce, plaintext1, ad1)
   ciphertext2 = ENCRYPT(key, nonce, plaintext2, ad2)  # CATASTROPHIC

# جيد: nonce (رقم يُستخدم مرة واحدة) فريد لكل رسالة    ciphertext1 = ENCRYPT(key, nonce1, plaintext1, ad1)    ciphertext2 = ENCRYPT(key, nonce2, plaintext2, ad2)

   ```

2. **Ephemeral Key Reuse**: Generate fresh ephemeral key for each NS/NSR
   ```python
# سيئ: إعادة استخدام مفتاح مؤقت    ephemeral_key = generate_elg2_keypair()    send_ns_message(ephemeral_key)    send_ns_message(ephemeral_key)  # سيئ

# جيد: مفتاح جديد لكل رسالة    send_ns_message(generate_elg2_keypair())    send_ns_message(generate_elg2_keypair())

   ```

3. **Weak RNG**: Use cryptographically secure random number generator
   ```python
# سيئ: مولّد أرقام عشوائية غير تشفيري    import random    key = bytes([random.randint(0, 255) for _ in range(32)])  # غير آمن

# جيد: مولّد أرقام عشوائية آمن تشفيرياً    import os    key = os.urandom(32)

   ```

4. **Timing Attacks**: Use constant-time comparisons
   ```python
# سيئ: مقارنة تتوقف مبكرًا    if computed_mac == received_mac:  # تسريب عبر التوقيت

       pass
   
# جيد: مقارنة بزمن ثابت    if constant_time_compare(computed_mac, received_mac):

       pass
   ```

5. **Incomplete MAC Verification**: Always verify before using data
   ```python
# سيئ: فك التشفير قبل التحقق    plaintext = chacha20_decrypt(key, nonce, ciphertext)    mac_ok = verify_mac(mac, plaintext)  # فات الأوان    if not mac_ok:

       return error
   
# جيد: AEAD (التشفير المصادق مع بيانات مرتبطة) يتحقق قبل فك التشفير    try:

       plaintext = DECRYPT(key, nonce, ciphertext, ad)  # Verifies MAC first
except AuthenticationError:

       return error
   ```

6. **Key Deletion**: Securely wipe keys from memory
   ```python
# سيئ: حذف بسيط    del private_key  # لا يزال في الذاكرة

# جيد: الكتابة فوق البيانات قبل الحذف    for i in range(len(private_key)):

       private_key[i] = 0
del private_key

   ```

### Security Audits

**Recommended Audits:**

1. **Cryptographic Review**: Expert review of KDF chains and DH operations
2. **Implementation Audit**: Code review for timing attacks, key management, RNG usage
3. **Protocol Analysis**: Formal verification of handshake security properties
4. **Side-Channel Analysis**: Timing, power, and cache attacks
5. **Fuzzing**: Random input testing for parser robustness

**Test Cases:**

```python
# حالات اختبار حرجة أمنياً

def test_nonce_uniqueness():

    """Ensure nonces are never reused"""
    nonces = set()
    for i in range(10000):
        nonce = construct_nonce(i)
        assert nonce not in nonces
        nonces.add(nonce)

def test_key_isolation():

    """Ensure sessions don't share keys"""
    session1 = create_session(destination1)
    session2 = create_session(destination2)
    
    assert session1.key != session2.key

def test_replay_prevention():

    """Ensure replay attacks are detected"""
    ns_message = create_ns_message()
    
    # First delivery succeeds
    assert process_ns_message(ns_message) == True
    
    # Replay fails
    assert process_ns_message(ns_message) == False

def test_mac_verification():

    """Ensure MAC verification is enforced"""
    key = CSRNG(32)
    nonce = construct_nonce(0)
    plaintext = b"test"
    ad = b"test_ad"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    
    # Correct MAC verifies
    assert DECRYPT(key, nonce, ciphertext, ad) == plaintext
    
    # Corrupted MAC fails
    corrupted = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])
    with pytest.raises(AuthenticationError):
        DECRYPT(key, nonce, corrupted, ad)
```

---

## Configuration and Deployment

### I2CP Configuration

**Enable ECIES Encryption:**

```properties
# ECIES فقط (مُوصى به لعمليات النشر الجديدة)

i2cp.leaseSetEncType=4

# ثنائي المفتاح (ECIES (مخطط تشفير مدمج يعتمد المنحنيات الإهليلجية) + ElGamal (مخطط تشفير بالمفتاح العام) للتوافق)

i2cp.leaseSetEncType=4,0

# ElGamal فقط (خوارزمية تشفير بالمفتاح العام؛ قديم، غير موصى به)

i2cp.leaseSetEncType=0

```

**LeaseSet Type:**

```properties
# LS2 القياسي (الإصدار الثاني من leaseSet، والأكثر شيوعًا)

i2cp.leaseSetType=3

# LS2 مُشفّر (blinded destinations، وجهات محجوبة الهوية)

i2cp.leaseSetType=5

# Meta LS2 (وجهات متعددة)

i2cp.leaseSetType=7

```

**Additional Options:**

```properties
# مفتاح ثابت لـ ECIES (نظام تشفير مدمج يعتمد على المنحنيات الإهليلجية) (اختياري، يُولَّد تلقائياً إذا لم يتم تحديده)

# مفتاح عام X25519 (خوارزمية لتبادل المفاتيح على منحنى بيضاوي) بطول 32 بايت، مُرمَّز بترميز Base64

i2cp.leaseSetPrivateKey=<base64-encoded-key>

# نوع التوقيع (لـ LeaseSet)

i2cp.leaseSetSigningPrivateKey=<base64-encoded-key> i2cp.leaseSetSigningType=7  # Ed25519

```

### Java I2P Configuration

**router.config:**

```properties
# ECIES (مخطط التشفير المتكامل بالمنحنيات الإهليلجية) بين Router و Router

i2p.router.useECIES=true

```

**Build Properties:**

```java
// لعملاء I2CP (جافا) Properties props = new Properties(); props.setProperty("i2cp.leaseSetEncType", "4"); props.setProperty("i2cp.leaseSetType", "3");

I2PSession session = i2pClient.createSession(props);

```

### i2pd Configuration

**i2pd.conf:**

```ini
[الحدود]

# حد الذاكرة لجلسات ECIES (مخطط تشفير متكامل باستخدام المنحنيات الإهليلجية)

ecies.memory = 128M

[ecies]

# تفعيل ECIES (مخطط التشفير المتكامل بالمنحنيات الإهليلجية)

enabled = true

# ECIES (مخطط تشفير متكامل بالمنحنيات الإهليلجية) فقط أو ثنائي المفتاح

compatibility = true  # true = ثنائي المفاتيح, false = ECIES فقط (مخطط تشفير متكامل بالمنحنيات الإهليلجية)

```

**Tunnels Configuration:**

```ini
[my-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# ECIES (مخطط تشفير متكامل بالمنحنيات الإهليلجية) فقط

ecies = true

```

### Compatibility Matrix

**Router Version Support:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">ECIES Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">LS2 Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Dual-Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&lt; 0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38-0.9.45</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LS2 only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.46-0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>

**Destination Compatibility:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Destination Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Can Connect To</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requires 0.9.46+ routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Maximum compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
  </tbody>
</table>

**FloodFill Requirements:**

- **ECIES-only destinations**: Require majority of floodfills on 0.9.46+ for encrypted lookups
- **Dual-key destinations**: Work with any floodfill version
- **Current status**: Near 100% floodfill adoption as of 2025

### Migration Guide

**Migrating from ElGamal to ECIES:**

**Step 1: Enable Dual-Key Mode**

```properties
# إضافة ECIES (نظام التشفير المتكامل بالمنحنيات الإهليلجية) مع الإبقاء على ElGamal (خوارزمية إل‑غامال)

i2cp.leaseSetEncType=4,0

```

**Step 2: Monitor Connections**

```bash
# تحقق من أنواع الاتصال

i2prouter.exe status

# أو

http://127.0.0.1:7657/peers

```

**Step 3: Switch to ECIES-Only (after testing)**

```properties
# إزالة ElGamal (خوارزمية تشفير)

i2cp.leaseSetEncType=4

```

**Step 4: Restart Application**

```bash
# أعد تشغيل I2P router أو التطبيق

systemctl restart i2p

# أو

i2prouter.exe restart

```

**Rollback Plan:**

```properties
# عُد إلى ElGamal (خوارزمية تشفير) فقط إذا ظهرت مشاكل

i2cp.leaseSetEncType=0

```

### Performance Tuning

**Session Limits:**

```properties
# الحد الأقصى للجلسات الواردة

i2p.router.maxInboundSessions=1000

# الحد الأقصى للجلسات الصادرة

i2p.router.maxOutboundSessions=1000

# مهلة الجلسة (ثوانٍ)

i2p.router.sessionTimeout=600

```

**Memory Limits:**

```properties
# حد تخزين الوسوم (KB)

i2p.ecies.maxTagMemory=10240  # 10 ميغابايت

# نافذة النظر المسبق

i2p.ecies.tagLookAhead=160 i2p.ecies.tagLookAheadMin=32

```

**Ratchet Policy:**

```properties
# رسائل ما قبل ratchet (آلية تدوير المفاتيح التدرّجية للتشفير)

i2p.ecies.ratchetThreshold=4096

# الوقت قبل ratchet (آلية السقاطة التشفيرية) (بالثواني)

i2p.ecies.ratchetTimeout=600  # 10 minutes

```

### Monitoring and Debugging

**Logging:**

```properties
# فعّل تسجيل تصحيح الأخطاء لـ ECIES (نظام التشفير المتكامل بالمنحنيات الإهليلجية)

logger.i2p.router.transport.ecies=DEBUG

```

**Metrics:**

Monitor these metrics:

1. **NS Success Rate**: Percentage of NS messages receiving NSR
2. **Session Establishment Time**: Time from NS to first ES
3. **Tag Storage Usage**: Current memory usage for tags
4. **Ratchet Frequency**: How often sessions ratchet
5. **Session Lifetime**: Average session duration

**Common Issues:**

1. **NS Timeout**: No NSR received
   - Check destination is online
   - Check floodfill availability
   - Verify LeaseSet published correctly

2. **High Memory Usage**: Too many tags stored
   - Reduce look-ahead window
   - Decrease session timeout
   - Implement aggressive expiration

3. **Frequent Ratchets**: Sessions ratcheting too often
   - Increase ratchet threshold
   - Check for retransmissions

4. **Session Failures**: ES messages failing to decrypt
   - Verify tag synchronization
   - Check for replay attacks
   - Validate nonce construction

---

## References

### Specifications

1. **ECIES Proposal**: [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)
2. **I2NP**: [I2NP Specification](/docs/specs/i2np/)
3. **Common Structures**: [Common Structures Specification](/docs/specs/common-structures/)
4. **NTCP2**: [NTCP2 Specification](/docs/specs/ntcp2/)
5. **SSU2**: [SSU2 Specification](/docs/specs/ssu2/)
6. **I2CP**: [I2CP Specification](/docs/specs/i2cp/)
7. **ElGamal/AES+SessionTags**: [ElGamal/AES Specification](/docs/legacy/elgamal-aes/)

### Cryptographic Standards

1. **Noise Protocol Framework**: [Noise Specification](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11)
2. **Signal Double Ratchet**: [Signal Specification](https://signal.org/docs/specifications/doubleratchet/)
3. **RFC 7748**: [Elliptic Curves for Security (X25519)](https://tools.ietf.org/html/rfc7748)
4. **RFC 7539**: [ChaCha20 and Poly1305 for IETF Protocols](https://tools.ietf.org/html/rfc7539)
5. **RFC 5869**: [HKDF (HMAC-based Key Derivation Function)](https://tools.ietf.org/html/rfc5869)
6. **RFC 2104**: [HMAC: Keyed-Hashing for Message Authentication](https://tools.ietf.org/html/rfc2104)
7. **Elligator2**: [Elligator Paper](https://elligator.cr.yp.to/elligator-20130828.pdf)

### Implementation Resources

1. **Java I2P**: [i2p.i2p Repository](https://github.com/i2p/i2p.i2p)
2. **i2pd (C++)**: [i2pd Repository](https://github.com/PurpleI2P/i2pd)
3. **OBFS4 (Elligator2)**: [obfs4proxy Repository](https://gitlab.com/yawning/obfs4)

### Additional Information

1. **I2P Website**: [/](/)
2. **I2P Forum**: [https://i2pforum.net](https://i2pforum.net)
3. **I2P Wiki**: [https://wiki.i2p-projekt.de](https://wiki.i2p-projekt.de)

---

## Appendix A: KDF Summary

**All KDF Operations in ECIES:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Info String</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Initial ChainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">protocol_name</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">(none - SHA256)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">h, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Static Key Section</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, es_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Payload Section (bound)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ss_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionReplyTags"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR ee DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ee_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR se DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, se_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Split</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ab, k_ba</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ba</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"AttachPayloadKDF"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_nsr</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Initialize</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">rootKey, k</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"KDFDHRatchetStep"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">nextRootKey, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tag and Key Chain Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"TagAndKeyGenKeys"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck, symmKey_ck</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Init</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"STInitialization"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionTagKeyGen"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, tag</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric Key Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SymmetricRatchet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sharedSecret</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"XDHRatchetTagSet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
  </tbody>
</table>

---

## Appendix B: Message Size Calculator

**Calculate message sizes for capacity planning:**

```python
def calculate_ns_size(payload_size, bound=True):

    """Calculate New Session message size"""
    ephemeral_key = 32
    static_section = 32 + 16  # encrypted + MAC
    payload_encrypted = payload_size + 16  # + MAC
    
    return ephemeral_key + static_section + payload_encrypted

def calculate_nsr_size(payload_size):

    """Calculate New Session Reply message size"""
    tag = 8
    ephemeral_key = 32
    key_section_mac = 16
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + ephemeral_key + key_section_mac + payload_encrypted

def calculate_es_size(payload_size):

    """Calculate Existing Session message size"""
    tag = 8
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + payload_encrypted

# أمثلة

print("NS (bound, 1KB payload):", calculate_ns_size(1024, bound=True), "bytes")

# الناتج: 1120 بايت

print("NSR (حمولة 1KB):", calculate_nsr_size(1024), "بايت")

# الناتج: 1096 بايت

print("ES (حمولة 1KB):", calculate_es_size(1024), "بايت")

# الناتج: 1048 بايت

```

---

## Appendix C: Glossary

**AEAD**: Authenticated Encryption with Associated Data - encryption mode that provides both confidentiality and authenticity

**Authentication Level**: Noise protocol security property indicating strength of sender identity verification

**Binding**: Association of a session with a specific far-end destination

**ChaCha20**: Stream cipher designed by Daniel J. Bernstein

**ChainKey**: Cryptographic key used in HKDF chains to derive subsequent keys

**Confidentiality Level**: Noise protocol security property indicating strength of forward secrecy

**DH**: Diffie-Hellman key agreement protocol

**Elligator2**: Encoding technique to make elliptic curve points indistinguishable from random

**Ephemeral Key**: Short-lived key used only for a single handshake

**ES**: Existing Session message (used after handshake completion)

**Forward Secrecy**: Property ensuring past communications remain secure if keys are compromised

**Garlic Clove**: I2NP message container for end-to-end delivery

**HKDF**: HMAC-based Key Derivation Function

**IK Pattern**: Noise handshake pattern where initiator sends static key immediately

**KCI**: Key Compromise Impersonation attack

**KDF**: Key Derivation Function - cryptographic function for generating keys from other keys

**LeaseSet**: I2P structure containing a destination's public keys and tunnel information

**LS2**: LeaseSet version 2 with encryption type support

**MAC**: Message Authentication Code - cryptographic checksum proving authenticity

**MixHash**: Noise protocol function for maintaining running hash transcript

**NS**: New Session message (initiates new session)

**NSR**: New Session Reply message (response to NS)

**Nonce**: Number used once - ensures unique encryption even with same key

**Pairing**: Linking an inbound session with an outbound session for bidirectional communication

**Poly1305**: Message authentication code designed by Daniel J. Bernstein

**Ratchet**: Cryptographic mechanism for deriving sequential keys

**Session Tag**: 8-byte one-time identifier for existing session messages

**Static Key**: Long-term key associated with a destination's identity

**Tag Set**: Collection of session tags derived from a common root

**X25519**: Elliptic curve Diffie-Hellman key agreement using Curve25519

---