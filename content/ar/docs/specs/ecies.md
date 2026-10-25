---
title: "ECIES-X25519-AEAD-Ratchet"
description: "مخطط التشفير المتكامل للمنحنى الإهليلجي للتشفير الشامل في I2P"
slug: "ecies"
aliases:
  - "/ar/docs/specs/ecies-x25519-aead-ratchet"
  - "/ar/docs/specs/ecies-x25519-aead-ratchet/"
category: "البروتوكولات"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
---

## ملاحظة

اكتمل نشر الشبكة. خاضع لمراجعات طفيفة. انظر [Prop144](/proposals/144-ecies-x25519/) للاقتراح الأصلي، بما في ذلك مناقشة الخلفية والمعلومات الإضافية.

الميزات التالية غير مطبقة اعتبارًا من الإصدار 0.9.66:

- كتل MessageNumbers وOptions وTermination
- استجابات طبقة البروتوكول
- مفتاح ثابت صفري
- البث المتعدد

بالنسبة لإصدار MLKEM PQ Hybrid من هذا البروتوكول، راجع [ECIES-HYBRID](/docs/specs/ecies-hybrid/).

## نظرة عامة

هذا هو بروتوكول التشفير الجديد من النهاية إلى النهاية لاستبدال ElGamal/AES+SessionTags [ElG-AES](/docs/specs/elgamal-aes/).

يعتمد على الأعمال السابقة كما يلي:

- مواصفات الهياكل المشتركة [Common](/docs/specs/common-structures/)
- مواصفات [I2NP](/docs/specs/i2np/) بما في ذلك LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/specs/elgamal-aes/)
- <http://zzz.i2p/topics/1768> نظرة عامة على التشفير غير المتماثل الجديد
- نظرة عامة على التشفير منخفض المستوى [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- ECIES <http://zzz.i2p/topics/2418>
- [NTCP2](/docs/specs/ntcp2/) [Prop111](/proposals/111-ntcp2/)
- 123 إدخالات netDb جديدة
- 142 قالب التشفير الجديد
- بروتوكول [Noise](https://noiseprotocol.org/noise.html)
- خوارزمية [Signal](https://signal.org/docs/specifications/doubleratchet/) double ratchet

يدعم تشفيراً جديداً للاتصال من طرف إلى طرف، ومن وجهة إلى وجهة.

يستخدم التصميم مصافحة Noise ومرحلة البيانات التي تدمج التشفير المزدوج المتسلسل الخاص بـ Signal.

جميع المراجع إلى Signal و Noise في هذه المواصفة هي لمعلومات خلفية فقط. معرفة بروتوكولات Signal و Noise ليست مطلوبة لفهم أو تنفيذ هذه المواصفة.

هذه المواصفة مدعومة اعتباراً من الإصدار 0.9.46.

## المواصفات

يستخدم التصميم مصافحة Noise ومرحلة البيانات التي تتضمن التشفير المزدوج (double ratchet) الخاص بـ Signal.

### ملخص التصميم التشفيري

هناك خمسة أجزاء من البروتوكول تحتاج إلى إعادة تصميم:

- 1\) يتم استبدال تنسيقات حاوية الجلسة الجديدة والموجودة بتنسيقات جديدة.
- 2\) يتم استبدال ElGamal (مفاتيح عامة 256 بايت، مفاتيح خاصة 128 بايت) بـ ECIES-X25519 (مفاتيح عامة وخاصة 32 بايت)
- 3\) يتم استبدال AES بـ AEAD_ChaCha20_Poly1305 (مختصر كـ ChaChaPoly أدناه)
- 4\) سيتم استبدال SessionTags برقمات (ratchets)، وهي في الأساس مولد أرقام عشوائي مزيف متزامن تشفيريًا.
- 5\) يتم استبدال حمولة AES، كما هو محدد في مواصفة ElGamal/AES+SessionTags، بتنسيق كتلة مشابه لذلك في NTCP2.

كل واحد من التغييرات الخمسة له قسم خاص به أدناه.

### نوع التشفير

نوع التشفير (المستخدم في LS2) هو 4. يشير هذا إلى مفتاح عام X25519 بحجم 32 بايت little-endian، والبروتوكول من النهاية إلى النهاية المحدد هنا.

نوع التشفير 0 هو ElGamal. أنواع التشفير 1-3 محجوزة لـ ECIES-ECDH-AES-SessionTag، انظر الاقتراح 145 [Prop145](/proposals/145-ecies-ecdh-aes/).

### إطار عمل بروتوكول Noise

يوفر هذا البروتوكول المتطلبات بناءً على إطار عمل Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (المراجعة 34، 2018-07-11). يحتوي Noise على خصائص مشابهة لبروتوكول Station-To-Station [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol)، والذي يعتبر أساساً لبروتوكول [SSU](/docs/transport/ssu/). في اصطلاحات Noise، Alice هي المُبادِرة، وBob هو المُجيب.

هذه المواصفة مبنية على بروتوكول Noise وهو Noise_IK_25519_ChaChaPoly_SHA256. (المعرف الفعلي لدالة اشتقاق المفتاح الأولي هو "Noise_IKelg2_25519_ChaChaPoly_SHA256" للإشارة إلى امتدادات I2P - انظر قسم KDF 1 أدناه) يستخدم بروتوكول Noise هذا البدائيات التالية:

- نمط المصافحة التفاعلية: IK أليس ترسل مفتاحها الثابت إلى بوب فوراً (I) أليس تعرف مفتاح بوب الثابت مسبقاً (K)
- نمط المصافحة أحادية الاتجاه: N أليس لا ترسل مفتاحها الثابت إلى بوب (N)
- دالة DH: X25519 X25519 DH بطول مفتاح 32 بايت كما هو محدد في [RFC-7748](https://tools.ietf.org/html/rfc7748).
- دالة التشفير: ChaChaPoly AEAD_CHACHA20_POLY1305 كما هو محدد في [RFC-7539](https://tools.ietf.org/html/rfc7539) القسم 2.8. nonce بحجم 12 بايت، مع تعيين أول 4 بايتات إلى صفر. مطابق لذلك في [NTCP2](/docs/specs/ntcp2/).
- دالة التجمع (Hash): SHA256 تجمع قياسي بحجم 32 بايت، مستخدم بشكل واسع في I2P.

#### إضافات إلى الإطار

تحدد هذه المواصفة التحسينات التالية لـ Noise_IK_25519_ChaChaPoly_SHA256. هذه التحسينات تتبع عموماً الإرشادات الواردة في القسم 13 من [NOISE](https://noiseprotocol.org/noise.html).

1) المفاتيح المؤقتة غير المشفرة مُرمزة بـ

    [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf).
2) يتم إضافة بادئة للرد مع علامة نص واضح. 3) تنسيق الحمولة محدد للرسائل 1 و 2 ومرحلة البيانات.

    Of course, this is not defined in Noise.

جميع الرسائل تتضمن رأس رسالة [I2NP](/docs/specs/i2np/) Garlic Message. مرحلة البيانات تستخدم تشفيراً مشابهاً لمرحلة بيانات Noise، لكنه غير متوافق معها.

### أنماط المصافحة

تستخدم المصافحات أنماط المصافحة من [Noise](https://noiseprotocol.org/noise.html).

يتم استخدام تطابق الأحرف التالي:

- e = مفتاح مؤقت لاستخدام واحد
- s = مفتاح ثابت
- p = حمولة الرسالة

جلسات One-time و Unbound تشبه نمط Noise N.

```
<- s
...
e es p ->
```
الجلسات المقيدة مشابهة لنمط Noise IK.

```
<- s
...
e es s ss p ->
<- tag e ee se
<- p
p ->
```
#### خصائص الأمان

باستخدام مصطلحات Noise، يكون تسلسل التأسيس والبيانات كما يلي: (خصائص أمان الحمولة من [Noise](https://noiseprotocol.org/noise.html) )

```
IK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es, s, ss           1                2
  <- e, ee, se              2                4
  ->                        2                5
  <-                        2                5
```
#### الاختلافات عن XK

مصافحات IK لها عدة اختلافات عن مصافحات XK المستخدمة في [NTCP2](/docs/specs/ntcp2/) و [SSU2](/docs/specs/ssu2/).

- أربع عمليات DH إجمالية مقارنة بثلاث عمليات لـ XK
- مصادقة المرسل في الرسالة الأولى: يتم مصادقة الحمولة كمنتمية لمالك المفتاح العام للمرسل، على الرغم من أن المفتاح قد يكون مخترقًا (Authentication 1) يتطلب XK رحلة ذهاب وإياب أخرى قبل مصادقة Alice.
- سرية أمامية كاملة (Confidentiality 5) بعد الرسالة الثانية. يمكن لـ Bob إرسال حمولة فورًا بعد الرسالة الثانية مع سرية أمامية كاملة. يتطلب XK رحلة ذهاب وإياب أخرى للحصول على السرية الأمامية الكاملة.

باختصار، يتيح IK تسليم حمولة الاستجابة من بوب إلى أليس في 1-RTT مع سرية أمامية كاملة، ولكن حمولة الطلب ليست سرية أمامية.

### الجلسات

بروتوكول ElGamal/AES+SessionTag أحادي الاتجاه. في هذه الطبقة، لا يعرف المستقبِل مصدر الرسالة. الجلسات الصادرة والواردة غير مترابطة. الإقرارات تتم خارج النطاق باستخدام DeliveryStatusMessage (مغلفة في GarlicMessage) في الفص.

في هذه المواصفة، نحدد آليتين لإنشاء بروتوكول ثنائي الاتجاه - "الإقران" و"الربط". توفر هذه الآليات كفاءة وأمانًا محسنين.

#### سياق الجلسة

كما هو الحال مع ElGamal/AES+SessionTags، يجب أن تكون جميع الجلسات الواردة والصادرة في سياق معين، إما سياق الـ router أو السياق لوجهة محلية معينة. في Java I2P، يُطلق على هذا السياق اسم Session Key Manager.

يجب عدم مشاركة الجلسات بين السياقات، حيث أن ذلك سيسمح بالربط بين الوجهات المحلية المختلفة، أو بين وجهة محلية و router.

عندما يدعم وجهة معينة كلاً من ElGamal/AES+SessionTags وهذه المواصفة، فإن كلا النوعين من الجلسات قد يتشاركان السياق. انظر القسم 1ج) أدناه.

#### ربط الجلسات الواردة والصادرة

عندما يتم إنشاء جلسة صادرة في المنشئ (أليس)، يتم إنشاء جلسة واردة جديدة وإقرانها مع الجلسة الصادرة، إلا إذا لم تكن هناك حاجة لرد (مثل البيانات الخام).

يتم دائماً إقران جلسة واردة جديدة مع جلسة صادرة جديدة، إلا إذا لم يكن هناك رد مطلوب (مثل البيانات الخام).

إذا تم طلب رد مرتبط بوجهة أو router بعيدة، فإن الجلسة الصادرة الجديدة تلك ترتبط بتلك الوجهة أو router، وتحل محل أي جلسة صادرة سابقة إلى تلك الوجهة أو router.

ربط الجلسات الواردة والصادرة يوفر بروتوكولاً ثنائي الاتجاه مع القدرة على تدوير مفاتيح DH.

#### ربط الجلسات والوجهات

هناك جلسة صادرة واحدة فقط إلى وجهة أو router معين. قد تكون هناك عدة جلسات واردة حالية من وجهة أو router معين. بشكل عام، عندما يتم إنشاء جلسة واردة جديدة، ويتم استقبال حركة البيانات على تلك الجلسة (والتي تعمل كإقرار استلام)، فإن أي جلسات أخرى سيتم تمييزها لتنتهي صلاحيتها بسرعة نسبية، خلال دقيقة أو نحو ذلك. يتم فحص قيمة الرسائل المرسلة السابقة (PN)، وإذا لم تكن هناك رسائل غير مستلمة (ضمن حجم النافذة) في الجلسة الواردة السابقة، فقد يتم حذف الجلسة السابقة فوراً.

عندما يتم إنشاء جلسة صادرة في المنشئ (أليس)، فإنها ترتبط بالوجهة البعيدة (بوب)، وأي جلسة واردة مقترنة ستكون مرتبطة أيضًا بالوجهة البعيدة. مع تطور الجلسات، تستمر في الارتباط بالوجهة البعيدة.

عند إنشاء جلسة واردة في المتلقي (بوب)، يمكن ربطها بوجهة الطرف البعيد (أليس)، وذلك حسب اختيار أليس. إذا أدرجت أليس معلومات الربط (مفتاحها الثابت) في رسالة الجلسة الجديدة، فستكون الجلسة مربوطة بتلك الوجهة، وسيتم إنشاء جلسة صادرة مربوطة بنفس الوجهة. مع تقدم الجلسات عبر آلية ratchet، تستمر في كونها مربوطة بوجهة الطرف البعيد.

#### فوائد الربط والإقران

للحالة الشائعة، حالة البث المتدفق، نتوقع من Alice و Bob استخدام البروتوكول كما يلي:

- تقوم أليس بربط جلسة الإرسال الجديدة الخاصة بها بجلسة استقبال جديدة، وكلاهما مرتبط بالوجهة البعيدة (بوب).
- تقوم أليس بتضمين معلومات الربط والتوقيع، وطلب الرد، في رسالة الجلسة الجديدة المرسلة إلى بوب.
- يقوم بوب بربط جلسة الاستقبال الجديدة الخاصة به بجلسة إرسال جديدة، وكلاهما مرتبط بالوجهة البعيدة (أليس).
- يرسل بوب ردًا (إقرار) إلى أليس في الجلسة المقترنة، مع ratchet إلى مفتاح DH جديد.
- تقوم أليس بعمل ratchet إلى جلسة إرسال جديدة بمفتاح بوب الجديد، مقترنة بجلسة الاستقبال الموجودة.

من خلال ربط جلسة واردة بوجهة بعيدة، وإقران الجلسة الواردة بجلسة صادرة مربوطة بنفس الوجهة، نحقق فائدتين رئيسيتين:

1) الرد الأولي من Bob إلى Alice يستخدم DH مؤقت-مؤقت

2\) بعد أن تتلقى أليس رد بوب وتقوم بالتحديث، جميع الرسائل اللاحقة من أليس إلى بوب تستخدم DH مؤقت-مؤقت.

#### إقرارات الرسائل

في ElGamal/AES+SessionTags، عندما يتم تجميع leaseSet كقطعة garlic، أو يتم تسليم العلامات، فإن router المرسِل يطلب إشعار استلام (ACK). هذه قطعة garlic منفصلة تحتوي على رسالة DeliveryStatus. للأمان الإضافي، يتم تغليف رسالة DeliveryStatus في رسالة Garlic. هذه الآلية خارج النطاق من منظور البروتوكول.

في البروتوكول الجديد، نظراً لأن الجلسات الواردة والصادرة مقترنة، يمكننا الحصول على ACKs داخل النطاق. لا حاجة لـ clove منفصل.

إقرار الاستلام الصريح هو ببساطة رسالة جلسة موجودة بدون كتلة I2NP. ومع ذلك، في معظم الحالات، يمكن تجنب إقرار الاستلام الصريح، حيث توجد حركة مرور عكسية. قد يكون من المرغوب فيه للتنفيذات أن تنتظر وقتاً قصيراً (ربما مائة ميلي ثانية) قبل إرسال إقرار استلام صريح، لإعطاء طبقة streaming أو طبقة التطبيق وقتاً للاستجابة.

ستحتاج التطبيقات أيضًا إلى تأجيل إرسال أي ACK حتى بعد معالجة كتلة I2NP، حيث أن رسالة Garlic قد تحتوي على رسالة Database Store مع leaseSet. سيكون leaseSet حديث ضروريًا لتوجيه ACK، وسيكون الوجهة البعيدة (الموجودة في leaseSet) ضرورية للتحقق من المفتاح الثابت المربوط.

#### مهلة انتهاء الجلسة

يجب أن تنتهي صلاحية الجلسات الصادرة دائماً قبل الجلسات الواردة. عندما تنتهي صلاحية جلسة صادرة ويتم إنشاء جلسة جديدة، سيتم إنشاء جلسة واردة مقترنة جديدة أيضاً. إذا كانت هناك جلسة واردة قديمة، فسيُسمح لها بانتهاء الصلاحية.

### البث المتعدد

سيتم تحديده لاحقاً

### التعريفات

نُعرِّف الدوال التالية المقابلة للكتل البنائية التشفيرية المستخدمة.

ZEROLEN

مصفوفة بايت فارغة (طولها صفر)

CSRNG(n)

مخرجات n-byte من رقم عشوائي آمن تشفيرياً

    generator.

H(p, d)

دالة hash SHA-256 التي تأخذ سلسلة تخصيص p وبيانات

    d, and produces an output of length 32 bytes. As defined in
    [NOISE](https://noiseprotocol.org/noise.html). || below means append.

    Use SHA-256 as follows:

        H(p, d) := SHA-256(p || d)

MixHash(d)

دالة hash SHA-256 التي تأخذ hash سابق h وبيانات جديدة d،

    and produces an output of length 32 bytes. || below means append.

    Use SHA-256 as follows:

        MixHash(d) := h = SHA-256(h || d)

STREAM

ChaCha20/Poly1305 AEAD كما هو محدد في

    [RFC-7539](https://tools.ietf.org/html/rfc7539). S_KEY_LEN = 32 and S_IV_LEN =
    12.

    ENCRYPT(k, n, plaintext, ad)

    :   Encrypts plaintext using the cipher key k, and nonce n which
        MUST be unique for the key k. Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16
        bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if
        the key is secret.

    DECRYPT(k, n, ciphertext, ad)

    :   Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional. Returns the plaintext.

DH

نظام اتفاق المفتاح العام X25519. مفاتيح خاصة من 32 بايت، عامة

    keys of 32 bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()

    :   Generates a new private key.

    DERIVE_PUBLIC(privkey)

    :   Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()

    :   Generates a new private key that maps to a public key suitable
        for Elligator2 encoding. Note that half of the
        randomly-generated private keys will not be suitable and must be
        discarded.

    ENCODE_ELG2(pubkey)

    :   Returns the Elligator2-encoded public key corresponding to the
        given public key (inverse mapping). Encoded keys are little
        endian. Encoded key must be 256 bits indistinguishable from
        random data. See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)

    :   Returns the public key corresponding to the given
        Elligator2-encoded public key. See Elligator2 section below for
        specification.

    DH(privkey, pubkey)

    :   Generates a shared secret from the given private and public
        keys.

HKDF(salt, ikm, info, n)

دالة اشتقاق المفاتيح المشفرة التي تأخذ مفتاح إدخال معين

    material ikm (which should have good entropy but is not required to
    be a uniformly random string), a salt of length 32 bytes, and a
    context-specific 'info' value, and produces an output of n bytes
    suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using
    the HMAC hash function SHA-256 as specified in
    [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32
    bytes max.

MixKey(d)

استخدم HKDF() مع chainKey سابق وبيانات جديدة d، وقم بتعيين الجديد

    chainKey and k. As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows:

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]

### 1) تنسيق الرسالة

#### مراجعة تنسيق الرسائل الحالي

رسالة Garlic كما هو محدد في [I2NP](/docs/specs/i2np/) كما يلي. بما أن الهدف التصميمي هو أن المحطات الوسطية لا يمكنها التمييز بين التشفير الجديد والقديم، فإن هذا التنسيق لا يمكن تغييره، حتى لو كان حقل الطول زائداً عن الحاجة. يُظهر التنسيق مع الرأسية الكاملة 16-بايت، على الرغم من أن الرأسية الفعلية قد تكون بتنسيق مختلف، اعتماداً على وسيلة النقل المستخدمة.

عند فك التشفير، تحتوي البيانات على سلسلة من Garlic Cloves وبيانات إضافية، تُعرف أيضاً باسم Clove Set.

راجع [I2NP](/docs/specs/i2np/) للتفاصيل والمواصفات الكاملة.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### مراجعة تنسيق البيانات المشفرة

في ElGamal/AES+SessionTags، هناك تنسيقان للرسائل:

1\) جلسة جديدة: - كتلة ElGamal بحجم 514 بايت - كتلة AES (128 بايت كحد أدنى، مضاعف للعدد 16)

2\) الجلسة الموجودة: - علامة الجلسة 32 بايت - كتلة AES (128 بايت كحد أدنى، مضاعف للعدد 16)

هذه الرسائل محاطة برسالة I2NP garlic، والتي تحتوي على حقل الطول، لذلك الطول معروف.

يحاول المستقبل أولاً البحث عن أول 32 بايت كـ Session Tag. إذا وُجدت، يقوم بفك تشفير كتلة AES. إذا لم توجد، وكانت البيانات بطول (514+16) على الأقل، يحاول فك تشفير كتلة ElGamal، وإذا نجح، يقوم بفك تشفير كتلة AES.

#### علامات الجلسة الجديدة والمقارنة مع Signal

في Signal Double Ratchet، يحتوي الرأس على:

- DH: المفتاح العام الحالي للـ ratchet
- PN: طول رسالة السلسلة السابقة
- N: رقم الرسالة

"سلاسل الإرسال" الخاصة بـ Signal تعادل تقريباً مجموعات العلامات لدينا. باستخدام علامة الجلسة، يمكننا التخلص من معظم ذلك.

في الجلسة الجديدة، نضع المفتاح العام فقط في الرأس غير المشفر.

في الجلسة الموجودة، نستخدم علامة جلسة للرأس. علامة الجلسة مرتبطة بالمفتاح العام الحالي للـ ratchet، ورقم الرسالة.

في كل من الجلسة الجديدة والجلسة الموجودة، PN و N موجودان في النص المشفر.

في Signal، الأمور تتطور باستمرار. يتطلب مفتاح DH العام الجديد من المستقبِل أن يتطور ويرسل مفتاحاً عاماً جديداً مرة أخرى، والذي يعمل أيضاً كإقرار استلام للمفتاح العام المستلم. هذا سيكون عدداً كبيراً جداً من عمليات DH بالنسبة لنا. لذلك نفصل بين إقرار استلام المفتاح المستلم وإرسال مفتاح عام جديد. أي رسالة تستخدم علامة جلسة مُولَّدة من مفتاح DH العام الجديد تشكل إقرار استلام. نرسل مفتاحاً عاماً جديداً فقط عندما نرغب في إعادة تشفير المفاتيح.

العدد الأقصى من الرسائل قبل أن يجب على DH التقدم هو 65535.

عند تسليم مفتاح جلسة، نشتق "مجموعة العلامات" منه، بدلاً من الاضطرار إلى تسليم علامات الجلسة أيضاً. يمكن أن تحتوي مجموعة العلامات على ما يصل إلى 65536 علامة. ومع ذلك، يجب على المستقبلين تنفيذ استراتيجية "النظر للأمام"، بدلاً من توليد جميع العلامات المحتملة في آن واحد. قم بتوليد N علامة كحد أقصى بعد آخر علامة جيدة تم استلامها. قد تكون N 128 كحد أقصى، لكن 32 أو حتى أقل قد يكون خياراً أفضل.

### 1أ) تنسيق الجلسة الجديد

مفتاح عام لجلسة جديدة لمرة واحدة (32 بايت) بيانات مشفرة و MAC (البايتات المتبقية)

قد تحتوي رسالة الجلسة الجديدة على المفتاح العام الثابت للمرسل أو قد لا تحتوي عليه. إذا تم تضمينه، فإن الجلسة العكسية ترتبط بذلك المفتاح. يجب تضمين المفتاح الثابت إذا كانت الردود متوقعة، أي للتدفق والرسائل الرقمية القابلة للرد عليها. لا يجب تضمينه للرسائل الرقمية الخام.

رسالة الجلسة الجديدة مشابهة لنمط Noise [NOISE](https://noiseprotocol.org/noise.html) أحادي الاتجاه "N" (إذا لم يتم إرسال المفتاح الثابت)، أو النمط ثنائي الاتجاه "IK" (إذا تم إرسال المفتاح الثابت).

### 1b) تنسيق الجلسة الجديدة (مع الربط)

الطول هو 96 + طول الحمولة. التنسيق المشفر:

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
+         Static Key                    +
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
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Static Key encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### مفتاح الجلسة المؤقت الجديد

المفتاح المؤقت يتكون من 32 بايت، مُرمز باستخدام Elligator2. هذا المفتاح لا يُعاد استخدامه أبداً؛ يتم إنشاء مفتاح جديد مع كل رسالة، بما في ذلك عمليات إعادة الإرسال.

#### المفتاح الثابت

عند فك التشفير، مفتاح X25519 الثابت لأليس، 32 بايت.

#### الحمولة

الطول المشفر هو ما تبقى من البيانات. الطول المفكوك التشفير أقل بـ 16 من الطول المشفر. يجب أن تحتوي الحمولة على كتلة DateTime وعادة ما تحتوي على كتلة واحدة أو أكثر من كتل Garlic Clove. راجع قسم الحمولة أدناه للتنسيق والمتطلبات الإضافية.

### 1c) تنسيق الجلسة الجديد (بدون ربط)

إذا لم تكن هناك حاجة لرد، فلن يتم إرسال مفتاح ثابت.

الطول هو 96 + طول الحمولة. التنسيق المشفر:

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
|                                       |
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
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### مفتاح الجلسة المؤقت الجديد

مفتاح Alice المؤقت. المفتاح المؤقت يبلغ 32 بايت، مُرمز باستخدام Elligator2، little endian. هذا المفتاح لا يُعاد استخدامه أبداً؛ يتم إنشاء مفتاح جديد مع كل رسالة، بما في ذلك إعادة الإرسال.

#### قسم الأعلام البيانات المفكوكة التشفير

يحتوي قسم الـ Flags على لا شيء. يكون دائماً 32 بايت، لأنه يجب أن يكون بنفس طول الـ static key لرسائل New Session مع الربط. يحدد Bob ما إذا كانت static key أم قسم flags عن طريق اختبار ما إذا كانت الـ 32 بايت جميعها أصفار.

TODO هل هناك حاجة لأي flags هنا؟

#### الحمولة

الطول المشفر هو ما تبقى من البيانات. الطول المفكوك التشفير أقل بـ 16 من الطول المشفر. يجب أن تحتوي الحمولة على كتلة DateTime وعادة ما تحتوي على كتلة واحدة أو أكثر من كتل Garlic Clove. انظر قسم الحمولة أدناه للتنسيق والمتطلبات الإضافية.

### 1d) تنسيق لمرة واحدة (بدون ربط أو جلسة)

إذا كان من المتوقع إرسال رسالة واحدة فقط، فلا حاجة لإعداد جلسة أو مفتاح ثابت.

الطول هو 96 + طول البيانات المحملة. التنسيق المشفر:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       Ephemeral Public Key            |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
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
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### مفتاح الجلسة الجديدة لمرة واحدة

المفتاح لمرة واحدة يتكون من 32 بايت، مُرمز بـ Elligator2، ترتيب البايت الأصغر أولاً. هذا المفتاح لا يُعاد استخدامه أبداً؛ يتم توليد مفتاح جديد مع كل رسالة، بما في ذلك إعادة الإرسال.

#### قسم الأعلام البيانات المفكوكة التشفير

يحتوي قسم Flags على لا شيء. يكون دائماً 32 بايت، لأنه يجب أن يكون بنفس طول المفتاح الثابت لرسائل الجلسة الجديدة مع الربط. يحدد Bob ما إذا كانت 32 بايت هي مفتاح ثابت أم قسم flags عن طريق اختبار ما إذا كانت الـ 32 بايت كلها أصفار.

TODO هل هناك حاجة لأي flags هنا؟

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+             All zeros                 +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

zeros:: All zeros, 32 bytes.
```
#### الحمولة

الطول المشفر هو باقي البيانات. الطول المفكوك التشفير أقل بـ 16 من الطول المشفر. يجب أن تحتوي الحمولة على كتلة DateTime وعادة ما تحتوي على كتلة واحدة أو أكثر من كتل Garlic Clove. راجع قسم الحمولة أدناه للتنسيق والمتطلبات الإضافية.

### 1f) دوال اشتقاق المفاتيح لرسالة الجلسة الجديدة

#### KDF لـ ChainKey الأولي

هذا هو [NOISE](https://noiseprotocol.org/noise.html) القياسي لـ IK مع اسم بروتوكول معدل. لاحظ أننا نستخدم نفس المهيئ لكل من نمط IK (الجلسات المقيدة) ونمط N (الجلسات غير المقيدة).

يتم تعديل اسم البروتوكول لسببين. أولاً، للإشارة إلى أن المفاتيح المؤقتة مُرمّزة باستخدام Elligator2، وثانياً، للإشارة إلى أن MixHash() يتم استدعاؤها قبل الرسالة الثانية لخلط قيمة العلامة.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
 (40 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set chainKey = h

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections
```
#### KDF لمحتويات قسم الأعلام/المفتاح الثابت المشفرة

```
This is the "e" message pattern:

// Bob's X25519 static keys
// bpk is published in leaseset
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

// Bob static public key
// MixHash(bpk)
// || below means append
h = SHA256(h || bpk);

// up until here, can all be precalculated by Bob for all incoming connections

// Alice's X25519 ephemeral keys
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

// Alice ephemeral public key
// MixHash(aepk)
// || below means append
h = SHA256(h || aepk);

// h is used as the associated data for the AEAD in the New Session Message
// Retain the Hash h for the New Session Reply KDF
// eapk is sent in cleartext in the
// beginning of the New Session message
elg2_aepk = ENCODE_ELG2(aepk)
// As decoded by Bob
aepk = DECODE_ELG2(elg2_aepk)

End of "e" message pattern.

This is the "es" message pattern:

// Noise es
sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, flags/static key section, ad)

End of "es" message pattern.

This is the "s" message pattern:

// MixHash(ciphertext)
// Save for Payload section KDF
h = SHA256(h || ciphertext)

// Alice's X25519 static keys
ask = GENERATE_PRIVATE()
apk = DERIVE_PUBLIC(ask)

End of "s" message pattern.
```
#### KDF لقسم الحمولة (مع مفتاح Alice الثابت)

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
#### KDF لقسم الحمولة (بدون مفتاح Alice الثابت)

لاحظ أن هذا نمط Noise "N"، لكننا نستخدم نفس مُهيئ "IK" كما هو الحال مع الجلسات المربوطة.

لا يمكن تحديد ما إذا كانت رسائل الجلسة الجديدة تحتوي على المفتاح الثابت لأليس أم لا حتى يتم فك تشفير المفتاح الثابت وفحصه لتحديد ما إذا كان يحتوي على جميع الأصفار. لذلك، يجب على المستقبل استخدام آلة الحالة "IK" لجميع رسائل الجلسة الجديدة. إذا كان المفتاح الثابت يحتوي على جميع الأصفار، فيجب تخطي نمط الرسالة "ss".

```
chainKey = from Flags/Static key section
k = from Flags/Static key section
n = 1
ad = h from Flags/Static key section
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1g) تنسيق رد الجلسة الجديدة

يمكن إرسال رد واحد أو أكثر من New Session Replies استجابةً لرسالة New Session واحدة. كل رد مسبوق بعلامة، والتي يتم إنشاؤها من TagSet للجلسة.

رد الجلسة الجديدة يتكون من جزأين. الجزء الأول هو إتمام مصافحة Noise IK مع علامة مسبقة. طول الجزء الأول هو 56 بايت. الجزء الثاني هو حمولة مرحلة البيانات. طول الجزء الثاني هو 16 + طول الحمولة.

الطول الإجمالي هو 72 + طول الحمولة. التنسيق المشفر:

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
+  (MAC) for Key Section (no data)      +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Tag :: 8 bytes, cleartext

Public Key :: 32 bytes, little endian, Elligator2, cleartext

MAC :: Poly1305 message authentication code, 16 bytes
       Note: The ChaCha20 plaintext data is empty (ZEROLEN)

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### علامة الجلسة

يتم إنتاج العلامة في Session Tags KDF، كما هو مُهيأ في DH Initialization KDF أدناه. هذا يربط الرد بالجلسة. لا يتم استخدام Session Key من DH Initialization.

#### مفتاح الجلسة الجديدة المؤقت للرد

مفتاح Bob المؤقت. المفتاح المؤقت يتكون من 32 بايت، مُرمز بـ Elligator2، little endian. هذا المفتاح لا يُعاد استخدامه أبداً؛ يتم توليد مفتاح جديد مع كل رسالة، بما في ذلك إعادة الإرسال.

#### الحمولة

الطول المشفر هو ما تبقى من البيانات. الطول المفكوك التشفير أقل بـ 16 من الطول المشفر. ستحتوي الحمولة عادة على كتلة واحدة أو أكثر من كتل Garlic Clove. راجع قسم الحمولة أدناه للتنسيق والمتطلبات الإضافية.

#### KDF لمجموعة علامات الرد

يتم إنشاء علامة واحدة أو أكثر من TagSet، والذي يتم تهيئته باستخدام KDF أدناه، باستخدام chainKey من رسالة الجلسة الجديدة.

```
// Generate tagset

tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
    tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
#### KDF لمحتويات القسم المشفر لمفتاح الرد

```
// Keys from the New Session message
// Alice's X25519 keys
// apk and aepk are sent in original New Session message
// ask = Alice private static key
// apk = Alice public static key
// aesk = Alice ephemeral private key
// aepk = Alice ephemeral public key
// Bob's X25519 static keys
// bsk = Bob private static key
// bpk = Bob public static key

// Generate the tag
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG

// MixHash(tag)
h = SHA256(h || tag)

This is the "e" message pattern:

// Bob's X25519 ephemeral keys
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

// Bob's ephemeral public key
// MixHash(bepk)
// || below means append
h = SHA256(h || bepk);

// elg2_bepk is sent in cleartext in the
// beginning of the New Session message
elg2_bepk = ENCODE_ELG2(bepk)
// As decoded by Bob
bepk = DECODE_ELG2(elg2_bepk)

End of "e" message pattern.

This is the "ee" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from original New Session Payload Section
sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
keydata = HKDF(chainKey, sharedSecret, "", 32)
chainKey = keydata[0:31]

End of "ee" message pattern.

This is the "se" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
sharedSecret = DH(ask, bepk) = DH(besk, apk)
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

End of "se" message pattern.

// MixHash(ciphertext)
h = SHA256(h || ciphertext)

chainKey is used in the ratchet below.
```
#### KDF لمحتويات القسم المشفر للحمولة

هذا مشابه لرسالة الجلسة الموجودة الأولى، بعد التقسيم، ولكن بدون علامة منفصلة. بالإضافة إلى ذلك، نستخدم الـ hash من الأعلى لربط الحمولة برسالة NSR.

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
### ملاحظات

قد يتم إرسال عدة رسائل NSR كرد، كل منها بمفاتيح مؤقتة فريدة، اعتماداً على حجم الاستجابة.

مطلوب من Alice و Bob استخدام مفاتيح مؤقتة جديدة لكل رسالة NS و NSR.

يجب على Alice تلقي إحدى رسائل NSR من Bob قبل إرسال رسائل Existing Session (ES)، ويجب على Bob تلقي رسالة ES من Alice قبل إرسال رسائل ES.

يتم استخدام `chainKey` و `k` من قسم NSR Payload الخاص بـ Bob كمدخلات لـ ES DH Ratchets الأولية (كلا الاتجاهين، انظر DH Ratchet KDF).

يجب على Bob الاحتفاظ فقط بالجلسات الموجودة لرسائل ES المستلمة من Alice. أي جلسات أخرى تم إنشاؤها للاتصالات الواردة والصادرة (لعدة NSRs) يجب تدميرها فوراً بعد استلام أول رسالة ES من Alice لجلسة معينة.

### 1h) تنسيق الجلسة الموجودة

علامة الجلسة (8 بايتات) البيانات المشفرة وMAC (انظر القسم 3 أدناه)

#### التنسيق

مشفر:

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### الحمولة

الطول المشفّر هو باقي البيانات. الطول المفكوك هو أقل بـ 16 من الطول المشفّر. راجع قسم الحمولة أدناه للتنسيق والمتطلبات.

#### KDF

```
See AEAD section below.

// AEAD parameters for Existing Session payload
k = The 32-byte session key associated with this session tag
n = The message number N in the current chain, as retrieved from the associated Session Tag.
ad = The session tag, 8 bytes
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 2) ECIES-X25519

التنسيق: مفاتيح عامة وخاصة بحجم 32 بايت، little-endian.

### 2a) Elligator2

في مصافحات Noise القياسية، تبدأ رسائل المصافحة الأولية في كل اتجاه بمفاتيح مؤقتة يتم إرسالها في نص واضح. نظرًا لأن مفاتيح X25519 الصالحة قابلة للتمييز عن البيانات العشوائية، قد يميز المهاجم في المنتصف هذه الرسائل عن رسائل الجلسة الموجودة التي تبدأ بعلامات جلسة عشوائية. في [NTCP2](/docs/specs/ntcp2/) ([Prop111](/proposals/111-ntcp2/))، استخدمنا وظيفة XOR منخفضة التكلفة باستخدام المفتاح الثابت خارج النطاق لتشويش المفتاح. ومع ذلك، نموذج التهديد هنا مختلف؛ لا نريد السماح لأي مهاجم في المنتصف باستخدام أي وسيلة لتأكيد وجهة حركة البيانات، أو تمييز رسائل المصافحة الأولية عن رسائل الجلسة الموجودة.

لذلك، يتم استخدام [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) لتحويل المفاتيح المؤقتة في رسائل New Session و New Session Reply بحيث تصبح غير قابلة للتمييز عن السلاسل النصية العشوائية المنتظمة.

#### تنسيق

مفاتيح عامة وخاصة بحجم 32 بايت. المفاتيح المُرمزة تستخدم ترتيب البايت الصغير (little endian).

كما هو معرّف في [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf)، فإن المفاتيح المُرمزة غير قابلة للتمييز عن 254 بت عشوائي. نحن نحتاج إلى 256 بت عشوائي (32 بايت). لذلك، يتم تعريف الترميز وفك الترميز كما يلي:

التشفير:

```
ENCODE_ELG2() Definition

// Encode as defined in Elligator2 specification
encodedKey = encode(pubkey)
// OR in 2 random bits to MSB
randomByte = CSRNG(1)
encodedKey[31] |= (randomByte & 0xc0)
```
فك التشفير:

```
DECODE_ELG2() Definition

// Mask out 2 random bits from MSB
encodedKey[31] &= 0x3f
// Decode as defined in Elligator2 specification
pubkey = decode(encodedKey)
```
#### ملاحظات

Elligator2 يضاعف متوسط وقت توليد المفاتيح، حيث أن نصف المفاتيح الخاصة ينتج عنها مفاتيح عامة غير مناسبة للترميز باستخدام Elligator2. كما أن وقت توليد المفاتيح غير محدود مع توزيع أسي، حيث يجب على المولد الاستمرار في المحاولة حتى يتم العثور على زوج مفاتيح مناسب.

يمكن إدارة هذا العبء الإضافي عن طريق القيام بتوليد المفاتيح مسبقاً، في خيط منفصل، للحفاظ على مجموعة من المفاتيح المناسبة.

يقوم المولد بتنفيذ دالة ENCODE_ELG2() لتحديد مدى الملاءمة. لذلك، ينبغي على المولد أن يحفظ نتيجة ENCODE_ELG2() حتى لا يضطر إلى حسابها مرة أخرى.

بالإضافة إلى ذلك، يمكن إضافة المفاتيح غير المناسبة إلى مجموعة المفاتيح المستخدمة لـ [NTCP2](/docs/specs/ntcp2/)، حيث لا يتم استخدام Elligator2. قضايا الأمان لفعل ذلك لا تزال قيد التحديد.

### 3) AEAD (ChaChaPoly)

AEAD باستخدام ChaCha20 و Poly1305، نفس المستخدم في [NTCP2](/docs/specs/ntcp2/). هذا يتوافق مع [RFC-7539](https://tools.ietf.org/html/rfc7539)، والذي يُستخدم أيضاً بشكل مماثل في TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

#### مدخلات الجلسة الجديدة ورد الجلسة الجديدة

المدخلات لدوال التشفير/فك التشفير لكتلة AEAD في رسالة جلسة جديدة:

```
k :: 32 byte cipher key
     See New Session and New Session Reply KDFs above.

n :: Counter-based nonce, 12 bytes.
     n = 0

ad :: Associated data, 32 bytes.
      The SHA256 hash of the preceding data, as output from mixHash()

data :: Plaintext data, 0 or more bytes
```
#### مدخلات الجلسة الموجودة

المدخلات لدوال التشفير/فك التشفير لكتلة AEAD في رسالة جلسة موجودة:

```
k :: 32 byte session key
     As looked up from the accompanying session tag.

n :: Counter-based nonce, 12 bytes.
     Starts at 0 and incremented for each message when transmitting.
     For the receiver, the value
     as looked up from the accompanying session tag.
     First four bytes are always zero.
     Last eight bytes are the message number (n), little-endian encoded.
     Maximum value is 65535.
     Session must be ratcheted when N reaches that value.
     Higher values must never be used.

ad :: Associated data
      The session tag

data :: Plaintext data, 0 or more bytes
```
#### التنسيق المشفر

مخرجات دالة التشفير، مدخلات دالة فك التشفير:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### ملاحظات

- نظرًا لأن ChaCha20 هو شيفرة تدفق، فلا حاجة لحشو النصوص الواضحة.
  يتم تجاهل بايتات التدفق المفتاحي الإضافية.
- يتم الاتفاق على مفتاح الشيفرة (256 بت) بواسطة
  SHA256 KDF. تفاصيل KDF لكل رسالة موجودة في أقسام
  منفصلة أدناه.
- إطارات ChaChaPoly لها حجم معروف لأنها مغلفة في
  رسالة بيانات I2NP.
- لجميع الرسائل، الحشو موجود داخل إطار البيانات المُصادق عليه.

#### معالجة أخطاء AEAD

يجب تجاهل جميع البيانات المستلمة التي تفشل في التحقق من AEAD. لا يتم إرجاع أي استجابة.

### 4) آليات التشفير المتقدمة (Ratchets)

ما زلنا نستخدم علامات الجلسة كما كان من قبل، لكننا نستخدم آلية ratchets لتوليدها. كانت لعلامات الجلسة أيضاً خيار إعادة التشفير الذي لم ننفذه أبداً. إذن الأمر يشبه double ratchet لكننا لم ننفذ الجزء الثاني أبداً.

هنا نحدد شيئاً مماثلاً لـ Double Ratchet الخاص بـ Signal. يتم إنتاج session tags بشكل حتمي ومتطابق على جانبي المستقبل والمرسل.

باستخدام آلية ratchet للمفتاح المتماثل/العلامة، نتخلص من استخدام الذاكرة لتخزين علامات الجلسة على جانب المرسل. كما نتخلص من استهلاك عرض النطاق الترددي لإرسال مجموعات العلامات. الاستخدام على جانب المستقبل لا يزال كبيراً، لكن يمكننا تقليله أكثر حيث سنقوم بتقليص علامة الجلسة من 32 بايت إلى 8 بايت.

نحن لا نستخدم تشفير الرأس كما هو محدد (واختياري) في Signal، بل نستخدم علامات الجلسة بدلاً من ذلك.

باستخدام DH ratchet، نحقق السرية الأمامية (forward secrecy)، والتي لم يتم تنفيذها مطلقاً في ElGamal/AES+SessionTags.

ملاحظة: المفتاح العام لمرة واحدة للجلسة الجديدة ليس جزءاً من الـ ratchet، وظيفته الوحيدة هي تشفير مفتاح DH ratchet الأولي لأليس.

#### أرقام الرسائل

يتعامل Double Ratchet مع الرسائل المفقودة أو غير المرتبة من خلال تضمين علامة في رأس كل رسالة. يبحث المستقبل عن فهرس العلامة، وهذا هو رقم الرسالة N. إذا كانت الرسالة تحتوي على كتلة Message Number مع قيمة PN، يمكن للمستقبل حذف أي علامات أعلى من تلك القيمة في مجموعة العلامات السابقة، مع الاحتفاظ بالعلامات المتخطاة من مجموعة العلامات السابقة في حالة وصول الرسائل المتخطاة لاحقاً.

#### نموذج التنفيذ

نقوم بتعريف هياكل البيانات والدوال التالية لتنفيذ هذه الـ ratchets.

TAGSET_ENTRY

إدخال واحد في TAGSET.

    INDEX

    :   An integer index, starting with 0

    SESSION_TAG

    :   An identifier to go out on the wire, 8 bytes

    SESSION_KEY

    :   A symmetric key, never goes on the wire, 32 bytes

TAGSET

مجموعة من TAGSET_ENTRIES.

    CREATE(key, n)

    :   Generate a new TAGSET using initial cryptographic key material
        of 32 bytes. The associated session identifier is provided. The
        initial number of of tags to create is specified; this is
        generally 0 or 1 for an outgoing session. LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)

    :   Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()

    :   Generate one more TAGSET_ENTRY, unless the maximum number
        SESSION_TAGS have already been generated. If LAST_INDEX is
        greater than or equal to 65535, return. ++ LAST_INDEX Create a
        new TAGSET_ENTRY with the LAST_INDEX value and the calculated
        SESSION_TAG. Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may be
        deferred and calculated in GET_SESSION_KEY(). Calls EXPIRE()

    EXPIRE()

    :   Remove tags and keys that are too old, or if the TAGSET size
        exceeds some limit.

    RATCHET_TAG()

    :   Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()

    :   Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION

    :   The associated session.

    CREATION_TIME

    :   When the TAGSET was created.

    LAST_INDEX

    :   The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()

    :   Used for outgoing sessions only. EXTEND(1) is called if there
        are no remaining TAGSET_ENTRIES. If EXTEND(1) did nothing, the
        max of 65535 TAGSETS have been used, and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)

    :   Used for incoming sessions only. Returns the TAGSET_ENTRY
        containing the sessionTag. If found, the TAGSET_ENTRY is
        removed. If the SESSION_KEY calculation was deferred, it is
        calculated now. If there are few TAGSET_ENTRIES remaining,
        EXTEND(n) is called.

#### 4أ) DH Ratchet

Ratchets ولكن ليس بالسرعة التي يقوم بها Signal. نحن نفصل بين إقرار المفتاح المُستلم وتوليد المفتاح الجديد. في الاستخدام النموذجي، ستقوم Alice و Bob بعمل ratchet (مرتين) فوراً في New Session، ولكن لن يقوموا بعمل ratchet مرة أخرى.

لاحظ أن ratchet مخصص لاتجاه واحد، وينتج سلسلة ratchet جديدة لعلامة الجلسة / مفتاح الرسالة لذلك الاتجاه. لتوليد مفاتيح لكلا الاتجاهين، عليك تطبيق ratchet مرتين.

تقوم بالـ ratchet في كل مرة تولد وترسل فيها مفتاحاً جديداً. تقوم بالـ ratchet في كل مرة تستقبل فيها مفتاحاً جديداً.

تقوم أليس بعملية ratchet واحدة عند إنشاء جلسة صادرة غير مرتبطة، ولا تنشئ جلسة واردة (غير المرتبطة تعني غير قابلة للرد عليها).

يقوم Bob بعمل ratchet مرة واحدة عند إنشاء جلسة واردة غير مرتبطة، ولا ينشئ جلسة صادرة مقابلة (غير المرتبطة غير قابلة للرد).

تستمر Alice في إرسال رسائل New Session (NS) إلى Bob حتى تستقبل إحدى رسائل New Session Reply (NSR) الخاصة به. ثم تستخدم نتائج KDF الخاصة بقسم Payload في رسالة NSR كمدخلات لـ session ratchets (انظر DH Ratchet KDF)، وتبدأ في إرسال رسائل Existing Session (ES).

لكل رسالة NS مستلمة، ينشئ Bob جلسة واردة جديدة، باستخدام نتائج KDF من قسم الحمولة للرد كمدخلات لـ ES DH Ratchet الوارد والصادر الجديد.

لكل رد مطلوب، يرسل بوب إلى أليس رسالة NSR مع الرد في الحمولة. يُطلب من بوب استخدام مفاتيح مؤقتة جديدة لكل رسالة NSR.

يجب على Bob استقبال رسالة ES من Alice في إحدى الجلسات الواردة، قبل إنشاء وإرسال رسائل ES في الجلسة الصادرة المقابلة.

يجب على أليس استخدام مؤقت لاستقبال رسالة NSR من بوب. إذا انتهت صلاحية المؤقت، يجب إزالة الجلسة.

لتجنب هجوم KCI و/أو استنزاف الموارد، حيث يقوم المهاجم بإسقاط ردود NSR الخاصة بـ Bob للحفاظ على إرسال Alice لرسائل NS، يجب على Alice تجنب بدء جلسات جديدة مع Bob بعد عدد معين من المحاولات بسبب انتهاء صلاحية المؤقت.

تقوم أليس وبوب كل منهما بعمل DH ratchet لكل كتلة NextKey مستلمة.

تقوم أليس وبوب بتوليد مجموعات علامات جديدة ومفتاحين متماثلين بعد كل DH ratchet. لكل رسالة ES جديدة في اتجاه معين، تقوم أليس وبوب بتقديم علامة الجلسة و symmetric key ratchets.

تكرار DH ratchets بعد المصافحة الأولية يعتمد على التنفيذ. بينما يضع البروتوكول حداً أقصى قدره 65535 رسالة قبل أن يُطلب ratchet، قد يوفر استخدام ratcheting أكثر تكراراً (بناءً على عدد الرسائل، الوقت المنقضي، أو كليهما) أماناً إضافياً.

بعد KDF المصافحة النهائية على الجلسات المرتبطة، يجب على Bob و Alice تشغيل دالة Noise Split() على CipherState الناتج لإنشاء مفاتيح متماثلة مستقلة ومفاتيح سلسلة العلامات للجلسات الواردة والصادرة.

##### معرفات مجموعة المفاتيح والعلامات

تُستخدم أرقام معرفات المفاتيح ومجموعات العلامات لتحديد المفاتيح ومجموعات العلامات. تُستخدم معرفات المفاتيح في كتل NextKey لتحديد المفتاح المرسل أو المستخدم. تُستخدم معرفات مجموعات العلامات (مع رقم الرسالة) في كتل ACK لتحديد الرسالة التي يتم الإقرار بها. تنطبق معرفات المفاتيح ومجموعات العلامات على مجموعات العلامات لاتجاه واحد. يجب أن تكون أرقام معرفات المفاتيح ومجموعات العلامات متسلسلة.

في مجموعات العلامات الأولى المستخدمة لجلسة في كل اتجاه، يكون معرف مجموعة العلامات هو 0. لم يتم إرسال أي كتل NextKey، لذا لا توجد معرفات مفاتيح.

لبدء DH ratchet، يرسل المُرسِل كتلة NextKey جديدة بمعرف مفتاح 0. يرد المُستقبِل بكتلة NextKey جديدة بمعرف مفتاح 0. ثم يبدأ المُرسِل في استخدام مجموعة علامات جديدة بمعرف مجموعة علامات 1.

يتم إنشاء مجموعات العلامات اللاحقة بطريقة مشابهة. بالنسبة لجميع مجموعات العلامات المستخدمة بعد تبادلات NextKey، فإن رقم مجموعة العلامات هو (1 + معرف مفتاح أليس + معرف مفتاح بوب).

تبدأ معرفات مجموعة المفاتيح والعلامات من 0 وتزداد تسلسلياً. الحد الأقصى لمعرف مجموعة العلامات هو 65535. الحد الأقصى لمعرف المفتاح هو 32767. عندما تكون مجموعة العلامات على وشك النفاد، يجب على مرسل مجموعة العلامات بدء تبادل NextKey. عندما تكون مجموعة العلامات 65535 على وشك النفاد، يجب على مرسل مجموعة العلامات بدء جلسة جديدة عن طريق إرسال رسالة New Session.

مع حد أقصى لحجم الرسالة المتدفقة يبلغ 1730، وبافتراض عدم وجود إعادة إرسال، فإن الحد الأقصى النظري لنقل البيانات باستخدام مجموعة علامات واحدة هو 1730 * 65536 ~= 108 ميجابايت. سيكون الحد الأقصى الفعلي أقل بسبب إعادة الإرسال.

الحد الأقصى النظري لنقل البيانات مع جميع مجموعات العلامات الـ 65536 المتاحة، قبل أن تضطر الجلسة للتجاهل والاستبدال، هو 64K * 108 MB ~= 6.9 TB.

##### تدفق رسائل DH RATCHET

يجب أن يبدأ تبديل المفاتيح التالي لمجموعة العلامات من قبل مرسل تلك العلامات (مالك مجموعة العلامات الصادرة). سيرد المستقبل (مالك مجموعة العلامات الواردة). بالنسبة لحركة مرور HTTP GET النموذجية في طبقة التطبيق، سيرسل Bob المزيد من الرسائل وسيقوم بالتسلسل أولاً عن طريق بدء تبديل المفاتيح؛ يوضح الرسم البياني أدناه ذلك. عندما تقوم Alice بالتسلسل، يحدث نفس الشيء في الاتجاه المعاكس.

مجموعة العلامات الأولى المستخدمة بعد مصافحة NS/NSR هي مجموعة العلامات 0. عندما تكون مجموعة العلامات 0 على وشك النفاد، يجب تبادل مفاتيح جديدة في كلا الاتجاهين لإنشاء مجموعة العلامات 1. بعد ذلك، يتم إرسال مفتاح جديد في اتجاه واحد فقط.

لإنشاء مجموعة العلامات 2، يرسل مُرسِل العلامة مفتاحاً جديداً ويرسل مُستقبِل العلامة معرف مفتاحه القديم كإقرار. كلا الطرفين يقوم بعملية DH.

لإنشاء مجموعة العلامات 3، يرسل مُرسِل العلامة معرف مفتاحه القديم ويطلب مفتاحاً جديداً من مُستقبِل العلامة. يقوم كلا الطرفين بتنفيذ DH.

يتم إنشاء مجموعات العلامات اللاحقة كما هو الحال بالنسبة لمجموعات العلامات 2 و 3. رقم مجموعة العلامات هو (1 + معرف مفتاح المرسل + معرف مفتاح المستقبل).

```
Tag Sender                    Tag Receiver

                 ... use tag set #0 ...


(Tagset #0 almost empty)
(generate new key #0)

Next Key, forward, request reverse, with key #0  -------->
(repeat until next key received)

                            (generate new key #0, do DH, create IB Tagset #1)

        <-------------      Next Key, reverse, with key #0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #1)


                 ... use tag set #1 ...


(Tagset #1 almost empty)
(generate new key #1)

Next Key, forward, with key #1        -------->
(repeat until next key received)

                            (reuse key #0, do DH, create IB Tagset #2)

        <--------------     Next Key, reverse, id 0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #2)


                 ... use tag set #2 ...


(Tagset #2 almost empty)
(reuse key #1)

Next Key, forward, request reverse, id 1  -------->
(repeat until next key received)

                            (generate new key #1, do DH, create IB Tagset #3)

        <--------------     Next Key, reverse, with key #1

(do DH, create OB Tagset #3)
(reuse key #1, do DH, create IB Tagset #3)



                 ... use tag set #3 ...



     After tag set 3, repeat the above
     patterns as shown for tag sets 2 and 3.

     To create a new even-numbered tag set, the sender sends a new key
     to the receiver. The receiver sends his old key ID
     back as an acknowledgement.

     To create a new odd-numbered tag set, the sender sends a reverse request
     to the receiver. The receiver sends a new reverse key to the sender.
```
بعد اكتمال DH ratchet للـ tagset الصادر، وإنشاء tagset صادر جديد، يجب استخدامه فوراً، ويمكن حذف الـ tagset الصادر القديم.

بعد اكتمال DH ratchet للـ tagset الواردة، وإنشاء tagset واردة جديدة، يجب على المستقبل الاستماع للعلامات في كلا من الـ tagsets، وحذف الـ tagset القديمة بعد فترة قصيرة، حوالي 3 دقائق.

ملخص مجموعة العلامات وتطور معرف المفتاح موجود في الجدول أدناه. * تشير إلى أنه تم إنشاء مفتاح جديد.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">New Tag Set ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Sender key ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Rcvr key ID</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65534</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32766</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
</tr>
</table>
يجب أن تكون أرقام معرفات مجموعة المفاتيح والعلامات متسلسلة.

##### DH INITIALIZATION KDF

هذا هو تعريف DH_INITIALIZE(rootKey, k) لاتجاه واحد. ينشئ مجموعة علامات، و"مفتاح جذر تالي" ليتم استخدامه لـ DH ratchet لاحق إذا لزم الأمر.

نستخدم تهيئة DH في ثلاثة أماكن. أولاً، نستخدمها لإنشاء مجموعة علامات لردود الجلسة الجديدة. ثانياً، نستخدمها لإنشاء مجموعتي علامات، واحدة لكل اتجاه، للاستخدام في رسائل الجلسة الموجودة. وأخيراً، نستخدمها بعد DH Ratchet لإنشاء مجموعة علامات جديدة في اتجاه واحد لرسائل الجلسة الموجودة الإضافية.

```
Inputs:
1) rootKey = chainKey from Payload Section
2) k from the New Session KDF or split()

// KDF_RK(rk, dh_out)
keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

// Output 1: The next Root Key (KDF input for the next DH ratchet)
nextRootKey = keydata[0:31]
// Output 2: The chain key to initialize the new
// session tag and symmetric key ratchets
// for the tag set
ck = keydata[32:63]

// session tag and symmetric key chain keys
keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
sessTag_ck = keydata[0:31]
symmKey_ck = keydata[32:63]
```
##### DH RATCHET KDF

يُستخدم هذا بعد تبادل مفاتيح DH الجديدة في كتل NextKey، قبل استنفاد مجموعة العلامات.

```
// Tag sender generates new X25519 ephemeral keys
// and sends rapk to tag receiver in a NextKey block
rask = GENERATE_PRIVATE()
rapk = DERIVE_PUBLIC(rask)

// Tag receiver generates new X25519 ephemeral keys
// and sends rbpk to Tag sender in a NextKey block
rbsk = GENERATE_PRIVATE()
rbpk = DERIVE_PUBLIC(rbsk)

sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
rootKey = nextRootKey // from previous tagset in this direction
newTagSet = DH_INITIALIZE(rootKey, tagsetKey)
```
#### 4ب) Session Tag Ratchet

آليات Ratchet لكل رسالة، كما هو الحال في Signal. آلية ratchet لعلامة الجلسة متزامنة مع آلية ratchet للمفتاح المتماثل، لكن آلية ratchet لمفتاح المستقبل قد "تتأخر" لتوفير الذاكرة.

ينتقل المرسل مرة واحدة لكل رسالة يتم إرسالها. لا يجب تخزين علامات إضافية. يجب على المرسل أيضًا الاحتفاظ بعداد لـ 'N'، وهو رقم الرسالة في السلسلة الحالية. يتم تضمين قيمة 'N' في الرسالة المرسلة. راجع تعريف كتلة رقم الرسالة.

يجب على المستقبل التقدم بواسطة الـ ratchet بحد أقصى حجم النافذة وتخزين العلامات في "مجموعة علامات"، والتي ترتبط بالجلسة. بمجرد الاستقبال، يمكن التخلص من العلامة المخزنة، وإذا لم تكن هناك علامات سابقة غير مستقبلة، فيمكن تقديم النافذة. يجب على المستقبل الاحتفاظ بقيمة 'N' المرتبطة بكل علامة جلسة، والتحقق من أن الرقم في الرسالة المرسلة يطابق هذه القيمة. راجع تعريف كتلة رقم الرسالة.

##### KDF

هذا هو تعريف RATCHET_TAG().

```
Inputs:
1) Session Tag Chain key sessTag_ck
   First time: output from DH ratchet
   Subsequent times: output from previous session tag ratchet

Generated:
2) input_key_material = SESSTAG_CONSTANT
   Must be unique for this tag set (generated from chain key),
   so that the sequence isn't predictable, since session tags
   go out on the wire in plaintext.

Outputs:
1) N (the current session tag number)
2) the session tag (and symmetric key, probably)
3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

Initialization:
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
// Output 1: Next chain key
sessTag_chainKey = keydata[0:31]
// Output 2: The constant
SESSTAG_CONSTANT = keydata[32:63]

// KDF_ST(ck, constant)
keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_0 = keydata_0[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_0 = keydata_0[32:39]

// repeat as necessary to get to tag_n
keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_n = keydata_n[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_n = keydata_n[32:39]
```
#### 4c) آلية تدوير المفتاح المتماثل

Ratchets لكل رسالة، كما في Signal. كل مفتاح متماثل له رقم رسالة مرتبط وعلامة جلسة. ratchet مفتاح الجلسة متزامن مع ratchet العلامة المتماثلة، لكن ratchet مفتاح المستقبل قد "يتأخر" لتوفير الذاكرة.

يتقدم المرسل ratchet مرة واحدة لكل رسالة يتم إرسالها. لا حاجة لتخزين مفاتيح إضافية.

عندما يحصل المستقبل على session tag، إذا لم يكن قد قام بالفعل بتقديم symmetric key ratchet إلى المفتاح المرتبط، يجب عليه "اللحاق" بالمفتاح المرتبط. سيقوم المستقبل على الأرجح بتخزين المفاتيح مؤقتاً لأي علامات سابقة لم يتم استلامها بعد. بمجرد الاستلام، يمكن التخلص من المفتاح المخزن، وإذا لم تكن هناك علامات سابقة غير مستلمة، فيمكن تقديم النافذة.

من أجل الكفاءة، فإن آليات التدوير لعلامات الجلسة والمفاتيح المتماثلة منفصلة بحيث يمكن لآلية تدوير علامات الجلسة أن تتقدم على آلية تدوير المفاتيح المتماثلة. هذا يوفر أيضاً أماناً إضافياً، نظراً لأن علامات الجلسة تنتقل عبر الشبكة.

##### KDF

هذا هو تعريف RATCHET_KEY().

```
Inputs:
1) Symmetric Key Chain key symmKey_ck
   First time: output from DH ratchet
   Subsequent times: output from previous symmetric key ratchet

Generated:
2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
   No need for uniqueness. Symmetric keys never go out on the wire.
   TODO: Set a constant anyway?

Outputs:
1) N (the current session key number)
2) the session key
3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

// KDF_CK(ck, constant)
SYMMKEY_CONSTANT = ZEROLEN
// Output 1: Next chain key
keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
// Output 2: The symmetric key
k_0 = keydata_0[32:63]

// repeat as necessary to get to k[n]
keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
// Output 1: Next chain key
symmKey_chainKey_n = keydata_n[0:31]
// Output 2: The symmetric key
k_n = keydata_n[32:63]
```
### 5) الحمولة

هذا يحل محل تنسيق قسم AES المحدد في مواصفات ElGamal/AES+SessionTags.

يستخدم هذا نفس تنسيق الكتلة كما هو محدد في مواصفة [NTCP2](/docs/specs/ntcp2/). أنواع الكتل الفردية محددة بشكل مختلف.

هناك مخاوف من أن تشجيع المطورين على مشاركة الكود قد يؤدي إلى مشاكل في التحليل. يجب على المطورين النظر بعناية في الفوائد والمخاطر لمشاركة الكود، والتأكد من أن قواعد الترتيب والكتل الصالحة مختلفة للسياقين.

#### قسم الحمولة البيانات المفكوكة التشفير

الطول المشفر هو الجزء المتبقي من البيانات. الطول المفكوك التشفير أقل بـ 16 من الطول المشفر. جميع أنواع الكتل مدعومة. المحتويات النموذجية تشمل الكتل التالية:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Block Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Number</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Block Length</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DateTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Termination (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Options (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21+</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Number (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Next Key</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3 or 35</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic Clove</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Padding</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
</table>
#### البيانات غير المشفرة

يوجد صفر أو أكثر من الكتل في الإطار المشفر. كل كتلة تحتوي على معرف من بايت واحد، وطول من بايتين، وصفر أو أكثر من بايتات البيانات.

لضمان القابلية للتوسعة، يجب على المستقبلات تجاهل الكتل ذات أرقام الأنواع غير المعروفة، والتعامل معها كحشو.

البيانات المشفرة تصل إلى 65535 بايت كحد أقصى، بما في ذلك رأس المصادقة بحجم 16 بايت، لذا فإن الحد الأقصى للبيانات غير المشفرة هو 65519 بايت.

(علامة المصادقة Poly1305 غير مُعرَضة):

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
~               .   .   .               ~

blk :: 1 byte
       0 datetime
       1-3 reserved
       4 termination
       5 options
       6 previous message number
       7 next session key
       8 ack
       9 ack request
       10 reserved
       11 Garlic Clove
       224-253 reserved for experimental features
       254 for padding
       255 reserved for future extension
size :: 2 bytes, big endian, size of data to follow, 0 - 65516
data :: the data

Maximum ChaChaPoly frame is 65535 bytes.
Poly1305 tag is 16 bytes
Maximum total block size is 65519 bytes
Maximum single block size is 65519 bytes
Block type is 1 byte
Block length is 2 bytes
Maximum single block data size is 65516 bytes.
```
#### قواعد ترتيب الكتل

في رسالة الجلسة الجديدة، يكون كتلة DateTime مطلوبة، ويجب أن تكون الكتلة الأولى.

الكتل الأخرى المسموحة:

- Garlic Clove (النوع 11)
- الخيارات (النوع 5)
- الحشو (النوع 254)

في رسالة الرد على الجلسة الجديدة، لا توجد كتل مطلوبة.

الكتل المسموحة الأخرى:

- Garlic Clove (النوع 11)
- الخيارات (النوع 5)
- الحشو (النوع 254)

لا يُسمح بأي كتل أخرى. الحشو، إذا كان موجوداً، يجب أن يكون الكتلة الأخيرة.

في رسالة الجلسة الموجودة، لا توجد كتل مطلوبة، والترتيب غير محدد، باستثناء المتطلبات التالية:

الإنهاء، إن وُجد، يجب أن يكون الكتلة الأخيرة باستثناء الحشو. الحشو، إن وُجد، يجب أن يكون الكتلة الأخيرة.

قد تكون هناك عدة كتل Garlic Clove في إطار واحد. قد يكون هناك ما يصل إلى كتلتين من نوع Next Key في إطار واحد. لا يُسمح بوجود عدة كتل Padding في إطار واحد. أنواع الكتل الأخرى ربما لن تحتوي على كتل متعددة في إطار واحد، لكن هذا غير محظور.

#### التاريخ والوقت

انتهاء صلاحية. يساعد في منع إعادة التشغيل. يجب على بوب التحقق من أن الرسالة حديثة، باستخدام هذه الطابع الزمني. يجب على بوب تنفيذ مرشح بلوم أو آلية أخرى لمنع هجمات إعادة التشغيل، إذا كان الوقت صحيحًا. يمكن لبوب أيضًا استخدام فحص سابق لكشف إعادة التشغيل للمفتاح المؤقت المكرر (سواء قبل أو بعد فك تشفير Elligator2) لكشف وإسقاط رسائل NS المكررة الحديثة قبل فك التشفير. عمومًا يتم تضمينه في رسائل الجلسة الجديدة فقط.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
#### فص الثوم

clove واحد مفكوك للتشفير من نوع Garlic كما هو محدد في [I2NP](/docs/specs/i2np/)، مع تعديلات لإزالة الحقول غير المستخدمة أو الزائدة عن الحاجة. تحذير: هذا التنسيق مختلف بشكل كبير عن التنسيق المخصص لـ ElGamal/AES. كل clove هو كتلة حمولة منفصلة. لا يجوز تجزئة Garlic Cloves عبر الكتل أو عبر إطارات ChaChaPoly.

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration   
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

size :: size of all data to follow

Delivery Instructions :: As specified in
       the Garlic Clove section of [I2NP]_.
       Length varies but is typically 1, 33, or 37 bytes

type :: I2NP message type

Message_ID :: 4 byte `Integer` I2NP message ID

Expiration :: 4 bytes, seconds since the epoch
```
ملاحظات:

- يجب على المنفذين التأكد من أنه عند قراءة كتلة، البيانات المشوهة أو
  الضارة لن تتسبب في تجاوز القراءات إلى الكتلة التالية.
- تنسيق Clove Set المحدد في [I2NP](/docs/specs/i2np/) غير
  مستخدم. كل clove موجود في كتلته الخاصة.
- رأس رسالة I2NP يبلغ 9 بايت، بتنسيق مطابق لذلك
  المستخدم في [NTCP2](/docs/specs/ntcp2/).
- الشهادة ومعرف الرسالة وانتهاء الصلاحية من تعريف Garlic Message
  في [I2NP](/docs/specs/i2np/) غير مضمنة.
- الشهادة ومعرف Clove وانتهاء الصلاحية من تعريف Garlic Clove
  في [I2NP](/docs/specs/i2np/) غير مضمنة.

#### الإنهاء

التنفيذ اختياري. إسقاط الجلسة. يجب أن يكون هذا آخر كتلة غير مبطنة في الإطار. لن يتم إرسال المزيد من الرسائل في هذه الجلسة.

غير مسموح في NS أو NSR. يتم تضمينه فقط في رسائل الجلسة الموجودة.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 1 or more
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       others: optional, impementation-specific
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### الخيارات

غير مُنفَّذ، لمزيد من الدراسة. تمرير الخيارات المحدثة. تتضمن الخيارات معاملات متنوعة للجلسة. راجع قسم تحليل طول علامة الجلسة أدناه للحصول على مزيد من المعلومات.

قد يكون طول كتلة الخيارات متغيراً، حيث قد تكون more_options موجودة.

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 5
size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
ver :: Protocol version, must be 0
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
STL :: Session tag length (must be 8), other values unimplemented
STimeout :: Session idle timeout (seconds), big endian
SOTW :: Sender Outbound Tag Window, 2 bytes big endian
RITW :: Receiver Inbound Tag Window 2 bytes big endian

tmin, tmax, rmin, rmax :: requested padding limits
    tmin and rmin are for desired resistance to traffic analysis.
    tmax and rmax are for bandwidth limits.
    tmin and tmax are the transmit limits for the router sending this options block.
    rmin and rmax are the receive limits for the router sending this options block.
    Each is a 4.4 fixed-point float representing 0 to 15.9375
    (or think of it as an unsigned 8-bit integer divided by 16.0).
    This is the ratio of padding to data. Examples:
    Value of 0x00 means no padding
    Value of 0x01 means add 6 percent padding
    Value of 0x10 means add 100 percent padding
    Value of 0x80 means add 800 percent (8x) padding
    Alice and Bob will negotiate the minimum and maximum in each direction.
    These are guidelines, there is no enforcement.
    Sender should honor receiver's maximum.
    Sender may or may not honor receiver's minimum, within bandwidth constraints.

tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
rdelay: Requested intra-message delay, 2 bytes big endian, msec average

more_options :: Format undefined, for future use
```
SOTW هو توصية المرسل للمستقبل بخصوص نافذة العلامات الواردة للمستقبل (أقصى نظرة مسبقة). RITW هو إعلان المرسل عن نافذة العلامات الواردة (أقصى نظرة مسبقة) التي يخطط لاستخدامها. كل طرف يقوم بعد ذلك بتعيين أو تعديل النظرة المسبقة بناءً على حد أدنى أو أقصى أو حساب آخر.

ملاحظات:

- نأمل ألا يكون دعم طول علامة الجلسة غير الافتراضي مطلوبًا أبدًا.
- نافذة العلامة هي MAX_SKIP في وثائق Signal.

المشاكل:

- تفاوض الخيارات قيد التحديد.
- الإعدادات الافتراضية قيد التحديد.
- خيارات الحشو والتأخير منسوخة من NTCP2، لكن هذه الخيارات
  لم يتم تنفيذها أو دراستها بشكل كامل هناك.

#### أرقام الرسائل

التنفيذ اختياري. الطول (عدد الرسائل المرسلة) في مجموعة العلامات السابقة (PN). يمكن للمستقبل حذف العلامات الأعلى من PN من مجموعة العلامات السابقة فوراً. يمكن للمستقبل إنهاء صلاحية العلامات الأقل من أو المساوية لـ PN من مجموعة العلامات السابقة بعد وقت قصير (مثل دقيقتان).

```
+----+----+----+----+----+
| 6  |  size   |  PN    |
+----+----+----+----+----+

blk :: 6
size :: 2
PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.
```
ملاحظات:

- أقصى PN هو 65535.
- تعاريف PN تساوي تعريف Signal، ناقص واحد.
  هذا مشابه لما يفعله Signal، ولكن في Signal، PN و N موجودان في
  الرأس. هنا، هما في نص الرسالة المشفر.
- لا تُرسل هذا البلوك في مجموعة العلامات 0، لأنه لم تكن هناك مجموعة علامات
  سابقة.

#### مفتاح Diffie-Hellman العام التالي للـ Ratchet

مفتاح DH ratchet التالي موجود في الحمولة، وهو اختياري. نحن لا نقوم بعملية ratchet في كل مرة. (هذا مختلف عن signal، حيث يكون في الرأس، ويُرسل في كل مرة)

للـ ratchet الأول، Key ID = 0.

غير مسموح في NS أو NSR. يتم تضمينه فقط في رسائل الجلسة الموجودة.

```
+----+----+----+----+----+----+----+----+
| 7  |  size   |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+                                       +
|     Next DH Ratchet Public Key        |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

blk :: 7
size :: 3 or 35
flag :: 1 byte flags
        bit order: 76543210
        bit 0: 1 for key present, 0 for no key present
        bit 1: 1 for reverse key, 0 for forward key
        bit 2: 1 to request reverse key, 0 for no request
               only set if bit 1 is 0
        bits 7-2: Unused, set to 0 for future compatibility
key ID :: The key ID of this key. 2 bytes, big endian
          0 - 32767
Public Key :: The next X25519 public key, 32 bytes, little endian
              Only if bit 0 is 1
```
ملاحظات:

- معرف المفتاح هو عداد متزايد للمفتاح المحلي المستخدم لمجموعة العلامات تلك،
  ويبدأ من 0.
- يجب ألا يتغير المعرف إلا إذا تغير المفتاح.
- قد لا يكون ضرورياً بشكل صارم، لكنه مفيد لتتبع الأخطاء.
  Signal لا يستخدم معرف مفتاح.
- الحد الأقصى لمعرف المفتاح هو 32767.
- في الحالة النادرة التي تتحرك فيها مجموعات العلامات في كلا الاتجاهين
  في نفس الوقت، سيحتوي الإطار على كتلتي Next Key، واحدة للمفتاح
  الأمامي وواحدة للمفتاح العكسي.
- أرقام معرفات المفتاح ومجموعة العلامات يجب أن تكون متسلسلة.
- انظر قسم DH Ratchet أعلاه للتفاصيل.

#### إقرار

يتم إرسال هذا فقط إذا تم استلام كتلة طلب إقرار. قد تكون عدة إقرارات موجودة للإقرار على رسائل متعددة.

غير مسموح في NS أو NSR. مُضمن فقط في رسائل الجلسة الموجودة.

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|             more acks                 |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 8
size :: 4 * number of acks to follow, minimum 1 ack
for each ack:
tagsetid :: 2 bytes, big endian, from the message being acked
N :: 2 bytes, big endian, from the message being acked
```
ملاحظات:

- معرف مجموعة العلامات و N يحددان بشكل فريد الرسالة التي يتم إقرارها.
- في مجموعات العلامات الأولى المستخدمة لجلسة في كل اتجاه، معرف مجموعة العلامات هو 0.
- لم يتم إرسال كتل NextKey، لذا لا توجد معرفات مفاتيح.
- لجميع مجموعات العلامات المستخدمة بعد تبادلات NextKey، رقم مجموعة العلامات هو (1 + معرف مفتاح Alice + معرف مفتاح Bob).

#### طلب الإقرار

طلب إقرار استلام داخل النطاق. لاستبدال رسالة DeliveryStatus خارج النطاق في Garlic Clove.

إذا تم طلب إقرار صريح، فسيتم إرجاع معرف tagset الحالي ورقم الرسالة (N) في كتلة الإقرار.

غير مسموح في NS أو NSR. يُتضمن فقط في رسائل الجلسة الموجودة.

```
+----+----+----+----+
|  9 |  size   |flg |
+----+----+----+----+

blk :: 9
size :: 1
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
```
#### الحشو

جميع الحشو (padding) داخل إطارات AEAD. TODO يجب أن يلتزم الحشو داخل AEAD تقريباً بالمعاملات المتفاوض عليها. TODO أرسلت Alice معاملات الحد الأدنى/الأقصى المطلوبة للإرسال/الاستقبال في رسالة NS. TODO أرسل Bob معاملات الحد الأدنى/الأقصى المطلوبة للإرسال/الاستقبال في رسالة NSR. يمكن إرسال خيارات محدّثة أثناء مرحلة البيانات. راجع معلومات كتلة الخيارات أعلاه.

إذا كان موجوداً، يجب أن يكون هذا آخر كتلة في الإطار.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 254
size :: 2 bytes, big endian, 0-65516
padding :: zeros or random data
```
ملاحظات:

- الحشو بالأصفار مقبول، حيث سيتم تشفيره.
- استراتيجيات الحشو سيتم تحديدها لاحقاً.
- الإطارات التي تحتوي على حشو فقط مسموحة.
- الحشو الافتراضي هو 0-15 بايت.
- انظر كتلة الخيارات لتفاوض معامل الحشو
- انظر كتلة الخيارات لمعاملات الحشو الدنيا/العليا
- استجابة router عند انتهاك الحشو المتفاوض عليه تعتمد على التطبيق.

#### أنواع الكتل الأخرى

يجب على التطبيقات تجاهل أنواع الكتل غير المعروفة لضمان التوافق المستقبلي.

#### العمل المستقبلي

- طول الحشو إما أن يُحدد على أساس كل رسالة على حدة وتقديرات توزيع الطول، أو يجب إضافة تأخيرات عشوائية. هذه التدابير المضادة يجب تضمينها لمقاومة DPI، حيث أن أحجام الرسائل ستكشف بخلاف ذلك أن حركة I2P يتم نقلها بواسطة بروتوكول النقل. مخطط الحشو الدقيق هو مجال للعمل المستقبلي، يوفر الملحق أ مزيدًا من المعلومات حول الموضوع.

## أنماط الاستخدام النموذجية

### HTTP GET

هذه هي حالة الاستخدام الأكثر شيوعاً، ومعظم حالات الاستخدام للبث غير HTTP ستكون مطابقة لهذه الحالة أيضاً. يتم إرسال رسالة أولية صغيرة، يتبعها رد، ثم يتم إرسال رسائل إضافية في كلا الاتجاهين.

طلب HTTP GET عادةً يتسع في رسالة I2NP واحدة. ترسل Alice طلباً صغيراً مع رسالة Session جديدة واحدة، مع تجميع reply leaseset. تتضمن Alice تدوير فوري لمفتاح جديد. يتضمن توقيعاً للربط بالوجهة. لا يُطلب إقرار استلام.

يقوم Bob بتدوير المفاتيح فوراً.

أليس تقوم بالـ ratchet فوراً.

يستمر مع تلك الجلسات.

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5
```
### HTTP POST

أليس لديها ثلاثة خيارات:

1) إرسال الرسالة الأولى فقط (حجم النافذة = 1)، كما في HTTP GET. ليس

    recommended.
2) الإرسال حتى نافذة التدفق، ولكن باستخدام نفس Elligator2-encoded

    cleartext public key. All messages contain same next public key
    (ratchet). This will be visible to OBGW/IBEP because they all start
    with the same cleartext. Things proceed as in 1). Not recommended.
3) التطبيق الموصى به. إرسال حتى نافذة streaming، ولكن باستخدام

    different Elligator2-encoded cleartext public key (session) for
    each. All messages contain same next public key (ratchet). This will
    not be visible to OBGW/IBEP because they all start with different
    cleartext. Bob must recognize that they all contain the same next
    public key, and respond to all with the same ratchet. Alice uses
    that next public key and continues.

تدفق رسائل الخيار 3:

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack
```
### Datagram قابل للرد

رسالة واحدة، مع توقع رد واحد. يمكن إرسال رسائل أو ردود إضافية.

مشابه لـ HTTP GET، ولكن مع خيارات أصغر لحجم نافذة علامة الجلسة ومدة البقاء. ربما لا تطلب ratchet.

```
Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message
```
### عدة Raw Datagrams

رسائل مجهولة متعددة، لا تتطلب ردود.

في هذا السيناريو، تطلب Alice جلسة، ولكن بدون ربط. يتم إرسال رسالة جلسة جديدة. لا يتم تجميع reply LS. يتم تجميع reply DSM (هذه هي حالة الاستخدام الوحيدة التي تتطلب DSMs مجمعة). لا يتم تضمين مفتاح تالي. لا يتم طلب reply أو ratchet. لا يتم إرسال ratchet. تحدد الخيارات نافذة session tags إلى صفر.

```
Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->
```
### حزمة بيانات خام واحدة

رسالة مجهولة واحدة، بدون توقع رد.

يتم إرسال رسالة لمرة واحدة. لا يتم تجميع reply LS أو DSM. لا يتم تضمين مفتاح تالي. لا يتم طلب رد أو ratchet. لا يتم إرسال ratchet. تقوم الخيارات بتعيين نافذة علامات الجلسة إلى الصفر.

```
Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message
```
### الجلسات طويلة المدى

قد تقوم الجلسات طويلة المدى بعملية ratchet، أو طلب ratchet، في أي وقت، للحفاظ على السرية الأمامية من تلك النقطة الزمنية. يجب على الجلسات القيام بعملية ratchet عندما تقترب من حد الرسائل المرسلة لكل جلسة (65535).

## اعتبارات التنفيذ

### الدفاع

كما هو الحال مع بروتوكول ElGamal/AES+SessionTag الحالي، يجب على التطبيقات تحديد تخزين session tag والحماية ضد هجمات استنزاف الذاكرة.

تتضمن بعض الاستراتيجيات الموصى بها:

- حد أقصى صارم على عدد علامات الجلسة المخزنة
- انتهاء صلاحية قوي للجلسات الواردة الخاملة عند التعرض لضغط الذاكرة
- حد أقصى على عدد الجلسات الواردة المرتبطة بوجهة واحدة في الطرف البعيد
- تقليل تكيفي لنافذة علامات الجلسة وحذف العلامات القديمة غير المستخدمة عند التعرض لضغط الذاكرة
- رفض التقدم التدريجي عند الطلب، في حالة التعرض لضغط الذاكرة

### المعاملات

المعاملات والمهلات الزمنية المُوصى بها:

- حجم tagset الخاص بـ NSR: 12 tsmin و tsmax
- حجم tagset 0 الخاص بـ ES: tsmin 24، tsmax 160
- حجم tagset (1+) الخاص بـ ES: 160 tsmin و tsmax
- مهلة tagset الخاص بـ NSR: 3 دقائق للمستقبل
- مهلة tagset الخاص بـ ES: 8 دقائق للمرسل، 10 دقائق للمستقبل
- إزالة tagset السابق الخاص بـ ES بعد: 3 دقائق
- التطلع المسبق لـ tagset للعلامة N: min(tsmax, tsmin + N/4)
- تقليم tagset خلف العلامة N: min(tsmax, tsmin + N/4) / 2
- إرسال المفتاح التالي عند العلامة: 4096
- إرسال المفتاح التالي بعد مدة حياة tagset: TBD
- استبدال الجلسة إذا تم استلام NS بعد: 3 دقائق
- أقصى انحراف للساعة: -5 دقائق إلى +2 دقيقة
- مدة مرشح إعادة تشغيل NS: 5 دقائق
- حجم الحشو: 0-15 بايت (استراتيجيات أخرى TBD)

### التصنيف

فيما يلي توصيات لتصنيف الرسائل الواردة.

#### X25519 فقط

على tunnel يُستخدم حصرياً مع هذا البروتوكول، قم بالتحديد كما يتم حالياً مع ElGamal/AES+SessionTags:

أولاً، تعامل مع البيانات الأولية كعلامة جلسة، وابحث عن علامة الجلسة. إذا تم العثور عليها، قم بفك التشفير باستخدام البيانات المخزنة المرتبطة بتلك علامة الجلسة.

إذا لم يتم العثور عليه، تعامل مع البيانات الأولية كمفتاح عام DH ونونس. قم بتنفيذ عملية DH و KDF المحددة، وحاول فك تشفير البيانات المتبقية.

#### X25519 مشترك مع ElGamal/AES+SessionTags

في tunnel يدعم كلاً من هذا البروتوكول و ElGamal/AES+SessionTags، قم بتصنيف الرسائل الواردة كما يلي:

بسبب عيب في مواصفة ElGamal/AES+SessionTags، لا يتم حشو كتلة AES إلى طول عشوائي غير mod-16. لذلك، فإن طول رسائل الجلسة الموجودة mod 16 دائماً 0، وطول رسائل الجلسة الجديدة mod 16 دائماً 2 (لأن كتلة ElGamal طولها 514 بايت).

إذا لم يكن باقي قسمة الطول على 16 يساوي 0 أو 2، فتعامل مع البيانات الأولية كعلامة جلسة، وابحث عن علامة الجلسة. إذا وُجدت، قم بفك التشفير باستخدام البيانات المخزنة المرتبطة بتلك علامة الجلسة.

إذا لم يتم العثور عليه، وكان باقي القسمة على 16 ليس 0 أو 2، عامل البيانات الأولية كمفتاح عام DH و nonce. قم بإجراء عملية DH و KDF المحددة، وحاول فك تشفير البيانات المتبقية. (بناءً على خليط حركة المرور النسبية، والتكاليف النسبية لعمليات X25519 و ElGamal DH، قد يتم تنفيذ هذه الخطوة أخيراً بدلاً من ذلك)

وإلا، إذا كان باقي القسمة على 16 يساوي 0، فتعامل مع البيانات الأولية كعلامة جلسة ElGamal/AES، وابحث عن علامة الجلسة. إذا تم العثور عليها، فك التشفير باستخدام البيانات المخزنة المرتبطة بتلك علامة الجلسة.

إذا لم يتم العثور عليه، وكانت البيانات بطول 642 (514 + 128) بايت على الأقل، وكان باقي القسمة على 16 يساوي 2، تعامل مع البيانات الأولية كـ ElGamal block. حاول فك تشفير البيانات المتبقية.

لاحظ أنه إذا تم تحديث مواصفات ElGamal/AES+SessionTag للسماح بالحشو غير المضاعف لـ 16، فسيتعين القيام بالأمور بطريقة مختلفة.

### إعادة الإرسال وانتقالات الحالة

طبقة ratchet لا تقوم بإعادة الإرسال، وباستثناء حالتين، لا تستخدم مؤقتات للإرسال. المؤقتات مطلوبة أيضاً لانتهاء مهلة tagset.

تُستخدم مؤقتات الإرسال فقط لإرسال NSR وللرد بـ ES عندما يحتوي ES المستلم على طلب ACK. المهلة الزمنية الموصى بها هي ثانية واحدة. في جميع الحالات تقريباً، ستقوم الطبقة العليا (datagram أو streaming) بالرد، مما يجبر إرسال NSR أو ES، ويمكن إلغاء المؤقت. إذا تم تشغيل المؤقت، أرسل حمولة فارغة مع NSR أو ES.

#### استجابات طبقة Ratchet

تعتمد التنفيذات الأولية على الحركة ثنائية الاتجاه في الطبقات العليا. أي أن التنفيذات تفترض أن الحركة في الاتجاه المعاكس ستُنقل قريباً، مما سيفرض أي استجابة مطلوبة في طبقة ECIES.

ومع ذلك، قد تكون بعض حركة البيانات أحادية الاتجاه أو ذات نطاق ترددي منخفض جداً، بحيث لا توجد حركة بيانات في طبقة أعلى لإنتاج استجابة في الوقت المناسب.

استلام رسائل NS و NSR يتطلب استجابة؛ استلام كتل ACK Request و Next Key يتطلب أيضاً استجابة.

يجب على التطبيقات بدء مؤقت عند استلام إحدى هذه الرسائل التي تتطلب استجابة، وتوليد استجابة "فارغة" (بدون كتلة Garlic Clove) في طبقة ECIES إذا لم يتم إرسال حركة بيانات عكسية خلال فترة زمنية قصيرة (مثل ثانية واحدة).

قد يكون من المناسب أيضًا استخدام مهلة زمنية أقصر حتى للاستجابات لرسائل NS و NSR، لتحويل الحركة إلى رسائل ES الفعالة في أسرع وقت ممكن.

#### ربط NS لـ NSR

في طبقة ratchet، بصفته Bob، فإن Alice معروفة فقط بالمفتاح الثابت. رسالة NS مُصادق عليها ([Noise](https://noiseprotocol.org/noise.html) IK sender authentication 1). ومع ذلك، هذا غير كافٍ لتتمكن طبقة ratchet من إرسال أي شيء إلى Alice، حيث أن توجيه الشبكة يتطلب Destination كامل.

قبل أن يتم إرسال NSR، يجب اكتشاف Destination الكامل الخاص بأليس إما بواسطة طبقة ratchet أو بروتوكول قابل للرد من طبقة أعلى، إما [Datagrams](/docs/specs/datagrams/) قابلة للرد أو [Streaming](/docs/specs/streaming/). بعد العثور على Leaseset لذلك Destination، سيحتوي ذلك Leaseset على نفس المفتاح الثابت الموجود في NS.

عادةً، ستستجيب الطبقة العليا، مما يجبر البحث في قاعدة بيانات الشبكة عن leaseSet الخاص بأليس باستخدام Destination Hash الخاص بأليس. سيتم العثور على ذلك الـ leaseSet محلياً في معظم الأحيان، لأن الـ NS احتوى على كتلة Garlic Clove، التي تحتوي على رسالة Database Store، التي تحتوي على leaseSet الخاص بأليس.

لكي يكون Bob مستعداً لإرسال NSR من طبقة ratchet، وربط الجلسة المعلقة بـ Destination الخاص بـ Alice، يجب على Bob "التقاط" الـ Destination أثناء معالجة حمولة NS. إذا تم العثور على رسالة Database Store تحتوي على Leaseset بمفتاح يطابق المفتاح الثابت في NS، فإن الجلسة المعلقة تصبح الآن مرتبطة بذلك الـ Destination، ويعرف Bob أين يرسل أي NSR إذا انتهت صلاحية مؤقت الاستجابة. هذا هو التنفيذ الموصى به.

تصميم بديل هو الحفاظ على ذاكرة تخزين مؤقت أو قاعدة بيانات حيث يتم ربط المفتاح الثابت بـ Destination. أمان وعملية هذا النهج موضوع للدراسة الإضافية.

لا تتطلب هذه المواصفة ولا غيرها بصرامة أن تحتوي كل NS على Leaseset الخاص بأليس. ومع ذلك، من الناحية العملية، يجب أن تحتوي عليها. مهلة انتهاء صلاحية مرسل ES tagset الموصى بها (8 دقائق) أقصر من مهلة انتهاء صلاحية Leaseset القصوى (10 دقائق)، لذا قد تكون هناك نافذة صغيرة حيث تكون الجلسة السابقة قد انتهت صلاحيتها، وتعتقد أليس أن بوب ما زال يملك Leaseset صالحة لها، ولا ترسل Leaseset جديدة مع NS الجديدة. هذا موضوع يحتاج لمزيد من الدراسة.

#### رسائل NS متعددة

إذا لم يتم استقبال استجابة NSR قبل أن ترسل الطبقة العليا (datagram أو streaming) المزيد من البيانات، وربما كإعادة إرسال، يجب على Alice أن تكوّن NS جديدة، باستخدام مفتاح مؤقت جديد. لا تعيد استخدام المفتاح المؤقت من أي NS سابقة. يجب على Alice أن تحتفظ بحالة المصافحة الإضافية ومجموعة علامات الاستقبال المشتقة، لاستقبال رسائل NSR كرد على أي NSR تم إرسالها.

قد تقوم التطبيقات بتحديد العدد الإجمالي لرسائل NS المرسلة، أو معدل إرسال رسائل NS، إما عن طريق وضع رسائل الطبقات العليا في طابور أو إسقاطها قبل إرسالها.

في حالات معينة، عند التعرض لحمولة عالية، أو تحت سيناريوهات هجوم معينة، قد يكون من المناسب لـ Bob أن يضع في طابور انتظار، أو يُسقط، أو يحد من رسائل NS الظاهرة دون محاولة فك التشفير، لتجنب هجوم استنزاف الموارد.

لكل NS مستقبل، ينشئ Bob مجموعة علامات NSR صادرة، يرسل NSR، يقوم بعملية split()، وينشئ مجموعات علامات ES الواردة والصادرة. ومع ذلك، لا يرسل Bob أي رسائل ES حتى يتم استقبال أول رسالة ES على مجموعة العلامات الواردة المقابلة. بعد ذلك، يمكن لـ Bob تجاهل جميع حالات المصافحة ومجموعات العلامات لأي NS آخر مستقبل أو NSR مُرسل، أو السماح لها بانتهاء الصلاحية قريباً. لا تستخدم مجموعات علامات NSR لرسائل ES.

إنه موضوع للدراسة المستقبلية إذا كان بإمكان Bob اختيار إرسال رسائل ES تخمينياً فوراً بعد NSR، حتى قبل استلام أول ES من Alice. في سيناريوهات وأنماط حركة مرور معينة، يمكن أن يوفر هذا عرض نطاق ومعالج كبيرين. قد تستند هذه الاستراتيجية على استدلالات مثل أنماط حركة المرور، أو نسبة رسائل ES المستلمة في tagset الجلسة الأولى، أو بيانات أخرى.

#### رسائل NSR متعددة

لكل رسالة NS مُستقبلة، حتى يتم استقبال رسالة ES، يجب على Bob الرد برسالة NSR جديدة، سواء بسبب إرسال حركة بيانات من الطبقة الأعلى، أو انتهاء مؤقت إرسال NSR.

كل NSR يستخدم حالة المصافحة ومجموعة العلامات المقابلة للـ NS الواردة. يجب على Bob الحفاظ على حالة المصافحة ومجموعة العلامات لجميع رسائل NS المستلمة، حتى يتم استلام رسالة ES.

يمكن للتطبيقات أن تحد من العدد الإجمالي لرسائل NSR المرسلة، أو معدل إرسال رسائل NSR، إما عن طريق وضع رسائل الطبقة العليا في طابور الانتظار أو إسقاطها قبل إرسالها. يمكن تطبيق هذه القيود إما عند حدوثها بسبب رسائل NS الواردة، أو حركة البيانات الصادرة الإضافية للطبقة العليا.

في حالات معينة، عند التحميل العالي، أو في سيناريوهات هجوم محددة، قد يكون من المناسب لـ Alice أن تضع في الطابور، أو تتجاهل، أو تحدد رسائل NSR دون محاولة فك التشفير، لتجنب هجوم استنزاف الموارد. هذه القيود قد تكون إما إجمالية عبر جميع الجلسات، أو لكل جلسة، أو كلاهما.

عندما تتلقى Alice رسالة NSR، تقوم Alice بعملية split() لاشتقاق مفاتيح جلسة ES. يجب على Alice ضبط مؤقت، وإرسال رسالة ES فارغة إذا لم ترسل الطبقة العليا أي بيانات، عادةً في غضون ثانية واحدة.

قد يتم إزالة مجموعات علامات NSR الواردة الأخرى قريباً أو السماح لها بالانتهاء، لكن يجب على أليس الاحتفاظ بها لفترة قصيرة، لفك تشفير أي رسائل NSR أخرى يتم استلامها.

### منع إعادة التشغيل

يجب على Bob تنفيذ Bloom filter أو آلية أخرى لمنع هجمات إعادة التشغيل NS، إذا كان DateTime المضمن حديثاً، ورفض رسائل NS حيث يكون DateTime قديماً جداً. قد يستخدم Bob أيضاً فحص كشف إعادة التشغيل المبكر للمفتاح المؤقت المكرر (إما قبل أو بعد فك تشفير Elligator2) لاكتشاف وإسقاط رسائل NS المكررة الحديثة قبل فك التشفير.

رسائل NSR و ES لديها حماية أساسية من إعادة التشغيل لأن علامة الجلسة تُستخدم مرة واحدة فقط.

رسائل garlic لديها أيضاً منع إعادة التشغيل إذا كان الـ router ينفذ مرشح Bloom على مستوى الـ router بناءً على معرف رسالة I2NP.

## التغييرات ذات الصلة

عمليات البحث في قاعدة البيانات من وجهات ECIES: راجع [Prop154](/proposals/154-ratchet/)، والتي تم دمجها الآن في [I2NP](/docs/specs/i2np/) للإصدار 0.9.46.

تتطلب هذه المواصفة دعم LS2 لنشر المفتاح العام X25519 مع leaseset. لا توجد حاجة لتغييرات في مواصفات LS2 الموجودة في [I2NP](/docs/specs/i2np/). تم تصميم وتحديد وتنفيذ جميع الدعم في [Prop123](/proposals/123-new-netdb-entries/) المنفذ في الإصدار 0.9.38.

تتطلب هذه المواصفة تعيين خاصية في خيارات I2CP لتفعيلها. تم تصميم وتحديد وتنفيذ جميع الدعم في [Prop123](/proposals/123-new-netdb-entries/) المنفذ في الإصدار 0.9.38.

الخيار المطلوب لتمكين ECIES هو خاصية I2CP واحدة لـ I2CP أو BOB أو SAM أو i2ptunnel.

القيم النموذجية هي i2cp.leaseSetEncType=4 لـ ECIES فقط، أو i2cp.leaseSetEncType=4,0 لمفاتيح ECIES و ElGamal المزدوجة.

## التوافق

أي router يدعم LS2 مع المفاتيح المزدوجة (0.9.38 أو أعلى) يجب أن يدعم الاتصال بالوجهات التي تحتوي على مفاتيح مزدوجة.

الوجهات التي تستخدم ECIES فقط تتطلب تحديث معظم floodfills إلى الإصدار 0.9.46 للحصول على ردود البحث المشفرة. راجع [Prop154](/proposals/154-ratchet/).

الوجهات التي تستخدم ECIES فقط يمكنها الاتصال فقط بالوجهات الأخرى التي تستخدم ECIES فقط، أو التي تستخدم مفاتيح مزدوجة.

## المراجع

- [Common](/docs/specs/common-structures/)
- [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- [Datagrams](/docs/specs/datagrams/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ElG-AES](/docs/specs/elgamal-aes/)
- [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) - انظر أيضاً [مقال Elligator](https://www.imperialviolet.org/2013/12/25/elligator.html) وكود OBFS4
- [GARLICSPEC](/docs/overview/garlic-routing/)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop111](/proposals/111-ntcp2/)
- [Prop123](/proposals/123-new-netdb-entries/)
- [Prop142](/proposals/142-ecies-template/)
- [Prop144](/proposals/144-ecies-x25519/)
- [Prop145](/proposals/145-ecies-ecdh-aes/)
- [Prop152](/proposals/152-ecies-config/)
- [Prop153](/proposals/153-chacha20-layer/)
- [Prop154](/proposals/154-ratchet/)
- [RFC-2104](https://tools.ietf.org/html/rfc2104)
- [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
- [RFC-5869](https://tools.ietf.org/html/rfc5869)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [Signal](https://signal.org/docs/specifications/doubleratchet/)
- [SSU](/docs/transport/ssu/)
- [SSU2](/docs/specs/ssu2/)
- [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) - Diffie, W.; van Oorschot P. C.; Wiener M. J., المصادقة وتبادل المفاتيح المصادق عليها
- [Streaming](/docs/specs/streaming/)
