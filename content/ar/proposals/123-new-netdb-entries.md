---
title: "إدخالات netDB جديدة"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "مفتوح"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
toc: true
---

## الحالة

تم الانتهاء من أجزاء من هذا الاقتراح، وتم تنفيذه في الإصدار 0.9.38 و0.9.39.   تم الآن تحديث المواصفات الخاصة بالهياكل المشتركة، وI2CP، وI2NP، وغيرها لتعكس التغييرات المدعومة حاليًا.

الأجزاء المكتملة لا تزال عرضة لمراجعات طفيفة.   أما الأجزاء الأخرى من هذا الاقتراح فهي لا تزال قيد التطوير وعرضة لمراجعات جوهرية.

تُعد ميزة البحث عن الخدمة (الأنواع 9 و11) ذات أولوية منخفضة وغير مجدولة، وقد يتم فصلها إلى اقتراح منفصل.

## نظرة عامة

هذا تحديث وتجميع للإقتراحات الأربعة التالية:

- 110 LS2
- 120 Meta LS2 للدعم الكبير للاتصال المتعدد (multihoming)
- 121 LS2 مشفر
- 122 البحث عن خدمة بدون مصادقة (anycasting)

هذه الاقتراحات مستقلة إلى حد كبير، ولكن من أجل الحفاظ على الاتساق، نحدد ونستخدم تنسيقًا مشتركًا لعدة منها.

الاقتراحات التالية مرتبطة إلى حد ما:

- 140 الاتصال المتعدد الخفي (incompatible with this proposal)
- 142 قالب تشفير جديد (للتشفير التماثلي الجديد)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 لـ LS2 المشفر
- 150 بروتوكول مزرعة الثوم (Garlic Farm Protocol)
- 151 ECDSA Blinding

## الاقتراح

يحدد هذا الاقتراح 5 أنواع جديدة من DatabaseEntry وعملية تخزينها واسترجاعها من قاعدة بيانات الشبكة، بالإضافة إلى طريقة توقيعها والتحقق من هذه التوقيعات.

### الأهداف

- التوافق العكسي
- إمكانية استخدام LS2 مع دعم الاتصال المتعدد القديم
- لا يتطلب تشفيرًا أو بنيات أولية جديدة للدعم
- الحفاظ على فصل التشفير عن التوقيع؛ دعم جميع الإصدارات الحالية والمستقبلية
- تمكين مفاتيح التوقيع الخارجية (offline keys) بشكل اختياري
- تقليل دقة الطوابع الزمنية لتقليل التعرف (fingerprinting)
- تمكين تشفير جديد للوجهات
- تمكين دعم الاتصال المتعدد على نطاق واسع
- إصلاح مشكلات متعددة في LS المشفر الحالي
- دعم اختياري للتعمية (blinding) لتقليل الرؤية من قبل الخوادم الممتلئة (floodfills)
- يدعم التشفير إما مفتاحًا واحدًا أو مفاتيح قابلة للإبطال متعددة
- البحث عن الخدمة لتسهيل البحث عن outproxies، وتشغيل تمهيد DHT للتطبيقات، واستخدامات أخرى
- عدم كسر أي شيء يعتمد على تجزئة الوجهة الثنائية بحجم 32 بايت، مثل bittorrent
- إضافة مرونة إلى leasesets من خلال الخصائص، كما هو الحال في routerinfos.
- وضع طابع النشر والانتهاء المتغير في الرأس، بحيث يعمل حتى إذا كانت المحتويات مشفرة (لا يتم اشتقاق الطابع الزمني من أقرب إيجار)
- جميع الأنواع الجديدة تعيش في نفس مساحة DHT والمواقع نفسها مثل leasesets الحالية، بحيث يمكن للمستخدمين التحول من LS القديم إلى LS2، أو التبديل بين LS2 وMeta وEncrypted، دون تغيير الوجهة أو التجزئة.
- يمكن تحويل وجهة حالية لاستخدام مفاتيح خارجية، أو العودة إلى مفاتيح داخلية، دون تغيير الوجهة أو التجزئة.

### غير الأهداف / خارج النطاق

- خوارزمية جديدة لتدوير DHT أو توليد عشوائي مشترك
- نوع التشفير الجديد ونظام التشفير من طرف إلى طرف لاستخدام هذا النوع سيكون في اقتراح منفصل. لا يتم تحديد أو مناقشة أي تشفير جديد هنا.
- تشفير جديد لـ RIs أو بناء الأنفاق. سيكون ذلك في اقتراح منفصل.
- طرق تشفير ونقل واستقبال رسائل I2NP DLM / DSM / DSRM. لا تتغير.
- كيفية إنشاء ودعم Meta، بما في ذلك الاتصال بين الراوترات، والإدارة، والتبديل عند الفشل، والتنسيق. قد تُضاف الدعم إلى I2CP أو i2pcontrol أو بروتوكول جديد. قد يتم أو لا يتم توحيد ذلك.
- كيفية تنفيذ وإدارة أنفاق ذات صلاحية أطول، أو إلغاء الأنفاق الحالية. هذا أمر صعب للغاية، وبدونه لا يمكن تحقيق إيقاف تشغيل سلس معقول.
- تغييرات نموذج التهديد
- تنسيق التخزين الخارجي، أو طرق تخزين/استرجاع/مشاركة البيانات.
- تفاصيل التنفيذ غير مناقشة هنا ويتم تركها لكل مشروع.

### التبرير

يُضيف LS2 حقولًا لتغيير نوع التشفير وللتغيرات المستقبلية في البروتوكول.

يُصلح LS2 المشفر عدة مشكلات أمنية في LS المشفر الحالي باستخدام تشفير غير متماثل لمجموعة الإيجارات بأكملها.

يوفر Meta LS2 دعمًا مرنًا وفعالًا وواسع النطاق للاتصال المتعدد.

توفر سجلات وقائمة الخدمة خدمات البث (anycast) مثل البحث عن الأسماء وتمهيد DHT.

### أنواع بيانات NetDB

تُستخدم أرقام الأنواع في رسائل I2NP Database Lookup/Store.

تشير العمود "end-to-end" إلى ما إذا كانت الاستعلامات/الاستجابات تُرسل إلى وجهة في رسالة ثوم (Garlic Message).

الأنواع الحالية:

| NetDB Data | Lookup Type | Store Type |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
الأنواع الجديدة:

| NetDB Data     | Lookup Type | Store Type | Std. LS2 Header? | Sent end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | yes              | yes              |
| Encrypted LS2  | 1           | 5          | no               | no               |
| Meta LS2       | 1           | 7          | yes              | no               |
| Service Record | n/a         | 9          | yes              | no               |
| Service List   | 4           | 11         | no               | no               |
### ملاحظات

- تُستخدم أنواع الاستعلام حاليًا في البتات 3-2 في رسالة Database Lookup. أي أنواع إضافية تتطلب استخدام البت 4.

- جميع أنواع التخزين فردية لأن البتات العليا في حقل النوع في رسالة Database Store تُهمل من قبل الراوترات القديمة. نفضل أن يفشل التحليل كـ LS بدلاً من RI مضغوط.

- هل يجب أن يكون النوع صريحًا أم ضمنيًا أم لا شيء في البيانات المشمولة بالتوقيع؟

### عملية البحث/التخزين

قد تُعاد الأنواع 3 و5 و7 كاستجابة لاستعلام leaseset قياسي (النوع 1).   لا يُعاد النوع 9 كاستجابة لاستعلام.   يُعاد النوع 11 كاستجابة لاستعلام جديد من نوع البحث عن الخدمة (النوع 11).

فقط النوع 3 يمكن إرساله في رسالة ثوم من عميل إلى عميل.

### التنسيق

الأنواع 3 و7 و9 تستخدم تنسيقًا مشتركًا::

```text
Standard LS2 Header
- as defined below

Type-Specific Part
- as defined below in each part

Standard LS2 Signature:
- Length as implied by sig type of signing key
```
رأس LS2 القياسي

الجزء المحدد حسب النوع

### اعتبارات الخصوصية/الأمان

التوقيع القياسي لـ LS2:

## رأس LS2 القياسي

لا يبدأ النوع 5 (المشفر) بـ Destination وله تنسيق مختلف. انظر أدناه.

### التنسيق

```
Standard LS2 Header:
  - Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Destination (387+ bytes)
  - Published timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Expires (2 bytes, big endian) (offset from published timestamp in seconds, 18.2 hours max)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bit 1: If 0, a standard published leaseset.
           If 1, an unpublished leaseset. Should not be flooded, published, or
           sent in response to a query. If this leaseset expires, do not query the
           netdb for a new one, unless bit 2 is set.
    Bit 2: If 0, a standard published leaseset.
           If 1, this unencrypted leaseset will be blinded and encrypted when published.
           If this leaseset expires, query the blinded location in the netdb for a new one.
           If this bit is set to 1, set bit 1 to 1 also.
           As of release 0.9.42.
    Bits 3-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type, and public key,
    by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
```
### التبرير

  - كما هو محدد أدناه

  - كما هو محدد أدناه لكل جزء

  - الطول حسب نوع التوقيع لمفتاح التوقيع

- غير منشور/منشور: للاستخدام عند إرسال تخزين قاعدة بيانات من طرف إلى طرف، قد يرغب الراوتر المرسل في الإشارة إلى أن هذا leaseset لا ينبغي إرساله للآخرين. نحن نستخدم حاليًا أساليب تقديرية للحفاظ على هذه الحالة.

### المشكلات

- منشور: يحل محل المنطق المعقد المطلوب لتحديد "الإصدار" لـ leaseset. حاليًا، الإصدار هو انتهاء صلاحية آخر إيجار، ويجب على الراوتر الناشر زيادة هذا الانتهاء بـ 1 مللي ثانية على الأقل عند نشر leaseset يزيل فقط إيجارًا أقدم.

- الانتهاء: يسمح بانتهاء صلاحية إدخال netdb يكون أبكر من انتهاء آخر إيجار له. قد لا يكون مفيدًا لـ LS2، حيث من المتوقع أن تظل leasesets بحد أقصى 11 دقيقة، ولكن لأنواع جديدة أخرى، يكون ضروريًا (انظر Meta LS وService Record أدناه).

- مفاتيح خارجية اختيارية، لتقليل تعقيد التنفيذ الأولي/المطلوب.

### ملاحظات

- يمكن تقليل دقة الطابع الزمني أكثر (10 دقائق؟) لكن سيكون يجب إضافة رقم إصدار. قد يكسر ذلك الاتصال المتعدد، ما لم نكن نملك تشفيرًا يحافظ على الترتيب؟ ربما لا يمكن فعل ذلك بدون طوابع زمنية على الإطلاق.

- بديل: طابع زمني بـ 3 بايت (العصر / 10 دقائق)، إصدار بـ 1 بايت، انتهاء بـ 2 بايت

- هل النوع صريح أم ضمني في البيانات / التوقيع؟ "ثوابت" النطاق للتوقيع؟

## أنواع DatabaseEntry الجديدة

### LeaseSet 2

النوع 11 (Service List) هو تجميع لعدة سجلات خدمة ولديه تنسيق مختلف. انظر أدناه.

- يجب ألا ينشر الراوترات leaseset أكثر من مرة في الثانية. إذا فعلوا ذلك، يجب أن يزيدوا بشكل اصطناعي الطابع الزمني للنشر بـ 1 على leaseset المنشور سابقًا.

قيد المراجعة (TBD)

    Standard LS flag (1)
تستخدم الأنواع 3 و7 و9 رأس LS2 القياسي، كما هو محدد أدناه:

    Standard LS2 type (3)
التغييرات من LeaseSet الحالي:

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
البحث باستخدام

    10 minutes, as in a regular LS.
التخزين باستخدام

    Destination

### التنسيق

```
Standard LS2 Header as specified above

  Standard LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of key sections to follow (1 byte, max TBD)
  - Key sections:
    - Encryption type (2 bytes, big endian)
    - Encryption key length (2 bytes, big endian)
      This is explicit, so floodfills can parse LS2 with unknown encryption types.
    - Encryption key (number of bytes specified)
  - Number of lease2s (1 byte)
  - Lease2s (40 bytes each)
    These are leases, but with a 4-byte instead of an 8-byte expiration,
    seconds since the epoch (rolls over in 2106)

  Standard LS2 Signature:
  - Signature
    If flag indicates offline keys, this is signed by the transient pubkey,
    otherwise, by the destination pubkey
    Length as implied by sig type of signing key
    The signature is of everything above.
```
### التبرير

- يمكن لتنفيذات الراوترات تخزين المفاتيح المؤقتة والتوقيع مؤقتًا لتجنب التحقق في كل مرة. على وجه الخصوص، يمكن لخوادم التعبئة (floodfills)، والراوترات في كلا طرفي الاتصالات طويلة الأمد، الاستفادة من هذا.

- المفاتيح والتوقيع الخارجي مناسبان فقط للوجهات طويلة الأمد، أي الخوادم، وليس العملاء.

### المناقشة

التخزين في

مدة الانتهاء النموذجية

ينشر بواسطة

- إضافة الطابع الزمني للنشر، وطابع انتهاء الصلاحية، والعلامات، والخصائص
- إضافة نوع التشفير
- إزالة مفتاح الإبطال

يستمر هذا الاقتراح في استخدام المفتاح العمومي في leaseset كمفتاح تشفير من طرف إلى طرف، ويترك الحقل العمومي في الوجهة غير مستخدم، كما هو الحال الآن. لا يتم تحديد نوع التشفير في شهادة مفتاح الوجهة، وستبقى 0.

- الخصائص: التوسع المستقبلي والمرونة. توضع أولًا في حال كانت ضرورية لتحليل البيانات المتبقية.

### مشكلات التشفير الجديدة

البديل المرفوض هو تحديد نوع التشفير في شهادة مفتاح الوجهة، واستخدام المفتاح العمومي في الوجهة، وعدم استخدام المفتاح العمومي في leaseset. لا نخطط للقيام بذلك.

- أزواج متعددة من نوع التشفير/المفتاح العمومي تسهل الانتقال إلى أنواع تشفير جديدة. الطريقة الأخرى هي نشر leasesets متعددة، ربما باستخدام نفس الأنفاق، كما نفعل الآن لوجهات DSA وEdDSA. يمكن تحديد نوع التشفير الوارد في النفق باستخدام آلية session tag الحالية، و/أو فك التشفير التجريبي باستخدام كل مفتاح. قد توفر أطوال الرسائل الواردة أيضًا دليلًا.

- موقع المفتاح العمومي الفعلي لا يتغير.
- يمكن تغيير نوع التشفير أو المفتاح العمومي دون تغيير الوجهة.
- إزالة حقل الإبطال غير المستخدم
- التوافق الأساسي مع أنواع DatabaseEntry الأخرى في هذا الاقتراح
- السماح بأنواع تشفير متعددة

- موقع المفتاح العمومي ونوع التشفير يختلف عن RouterInfo
- يحافظ على المفتاح العمومي غير المستخدم في leaseset
- يتطلب التنفيذ عبر الشبكة؛ في البديل، يمكن استخدام أنواع تشفير تجريبية، إذا سمح بها خوادم التعبئة (لكن انظر الاقتراحات 136 و137 حول دعم أنواع توقيع تجريبية). قد يكون الاقتراح البديل أسهل في التنفيذ والاختبار لأنواع التشفير التجريبية.

### ملاحظات

- يمثل نوع التشفير مزيجًا  
  من المنحنى، وطول المفتاح، ونظام التشفير من طرف إلى طرف،  
  بما في ذلك KDF وMAC، إن وجد.

- أدرجنا حقل طول المفتاح، بحيث يكون LS2  
  قابلاً للتحليل والتحقق من قبل خادم التعبئة حتى لأنواع التشفير غير المعروفة.

- أول نوع تشفير جديد مقترح سيكون  
  على الأرجح ECIES/X25519. كيف يستخدم من طرف إلى طرف  
  (إما نسخة معدلة قليلاً من ElGamal/AES+SessionTag  
  أو شيء جديد تمامًا، مثل ChaCha/Poly) سيتم تحديده  
  في اقتراح أو أكثر منفصلة.  
  انظر أيضًا اقتراحات ECIES 144 و145.

### LS2 المشفر

مزايا LS2:

- تغيرت مدة انتهاء الإيجارات من 8 بايت إلى 4 بايت.

عيوب LS2:

بعض هذا خارج نطاق هذا الاقتراح،   لكن وضع الملاحظات هنا مؤقتًا لأننا لا نملك   اقتراح تشفير منفصل بعد.   انظر أيضًا اقتراحات ECIES 144 و145.

- إذا نفذنا الإبطال في يوم ما، يمكننا فعل ذلك بحقل انتهاء صفر، أو إيجارات صفرية، أو كليهما. لا حاجة لمفتاح إبطال منفصل.

الأهداف:

    Standard LS flag (1)
لا يُرسل LS2 المشفر أبدًا في رسالة ثوم من طرف إلى طرف.   استخدم LS2 القياسي كما هو موضح أعلاه.

    Encrypted LS2 type (5)
التغييرات من LeaseSet المشفر الحالي:

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
البحث باستخدام

    10 minutes, as in a regular LS, or hours, as in a meta LS.
التخزين باستخدام

    Destination


### التعريفات

التخزين في

مدة الانتهاء النموذجية

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

ينشر بواسطة

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

نحدد الدوال التالية المقابلة للقطع البنائية التشفيرية المستخدمة   لـ LS2 المشفر:

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


CSRNG(n)

    The RedDSA signature scheme (corresponding to SigType 11) with key blinding.
    It has the following functions:

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    SIGN(privkey, m)
        Returns a signature by the private key privkey over the given message m.

    VERIFY(pubkey, m, sig)
        Verifies the signature sig against the public key pubkey and message m. Returns
        true if the signature is valid, false otherwise.

    It must also support the following key blinding operations:

    GENERATE_ALPHA(data, secret)
        Generate alpha for those who know the data and an optional secret.
        The result must be identically distributed as the private keys.

    BLIND_PRIVKEY(privkey, alpha)
        Blinds a private key, using a secret alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Blinds a public key, using a secret alpha.
        For a given keypair (privkey, pubkey) the following relationship holds::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

H(p, d)

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

STREAM

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### التنسيق

SIG

- تكون مفاتيح التشفير مرتبة حسب تفضيل الخادم، الأكثر تفضيلًا أولًا. السلوك الافتراضي للعميل هو اختيار أول مفتاح بدعم نوع تشفير مدعوم. قد يستخدم العملاء خوارزميات اختيار أخرى بناءً على دعم التشفير، والأداء النسبي، وعوامل أخرى.

DH

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

HKDF(salt, ikm, info, n)

يتكون تنسيق LS2 المشفر من ثلاث طبقات متداخلة:

#### الطبقة 0 (الخارجية)

التنسيق العام يبدو كالتالي::

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

لاحظ أن LS2 المشفر معتم. لا يوجد Destination في الرأس.   موضع تخزين DHT هو SHA-256(sig type || المفتاح العمومي المعتم)، ويتم تدويره يوميًا.

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

لا يستخدم رأس LS2 القياسي المحدد أعلاه.

    Length as implied by sig type

النوع

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

نوع توقيع المفتاح العمومي المعتم

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

المفتاح العمومي المعتم

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

الطابع الزمني للنشر

    Present if flag indicates offline keys

    Expires timestamp
        4 bytes, big endian

        Seconds since epoch, rolls over in 2106

    Transient sig type
        2 bytes, big endian

    Transient signing public key
        Length as implied by sig type

    Signature
        Length as implied by blinded public key sig type

        Over expires timestamp, transient sig type, and transient public key.

        Verified with the blinded public key.

الانتهاء

    2 bytes, big endian

العلامات

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

بيانات المفتاح المؤقت

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### الطبقة 1 (الوسطى)

lenOuterCiphertext

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

outerCiphertext

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 000.

    ephemeralPublicKey
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

التوقيع

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 001.

    authSalt
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes


العلامات

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### الطبقة 2 (الداخلية)

بيانات مصادقة عميل DH

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

بيانات مصادقة عميل PSK

    LeaseSet2 data for the given type.

    Includes the header and signature.


### استخلاص مفتاح التعمية

innerCiphertext

النوع

#### الأهداف

- إضافة التعمية (blinding)
- السماح بأنواع توقيع متعددة
- لا يتطلب أي بنيات تشفير أولية جديدة
- تشفير اختياري لكل مستلم، قابل للإبطال
- دعم تشفير LS2 القياسي وMeta LS2 فقط

#### الأمان

البيانات

#### التعريفات

نستخدم المخطط التالي لتعمية المفتاح،   استنادًا إلى Ed25519 و[ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf).   التوقيعات Re25519 على منحنى Ed25519، باستخدام SHA-512 للتجزئة.

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

لا نستخدم [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3)،   الذي له أهداف تصميم مشابهة، لأن مفاتيحه العامة المعتمة   قد تكون خارج المجموعة الفرعية من الدرجة الأولية، مع آثار أمنية غير معروفة.

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

يتطلب أمان مخطط التعمية أن يكون   توزيع alpha هو نفسه توزيع المفاتيح الخاصة غير المعتمة.   ومع ذلك، عند تعمية مفتاح خاص Ed25519 (sig type 7)   إلى مفتاح خاص Red25519 (sig type 11)، يكون التوزيع مختلفًا.   لتحقيق متطلبات [zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)،   يجب استخدام Red25519 (sig type 11) للمفاتيح غير المعتمة أيضًا، بحيث   "مزيج مفتاح عام مُعاد تعيينه وتوقيعات تحت هذا المفتاح لا يكشف المفتاح الذي تم إعادة تعيينه منه."   نسمح بالنوع 7 للوجهات الحالية، لكن نوصي   بالنوع 11 للوجهات الجديدة التي ستكون مشفرة.

    Convert a private key to public, as in Ed25519 (mulitply by G)

B

    A 32-byte random number known to those who know the destination.

L

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

DERIVE_PUBLIC(a)

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

alpha

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

GENERATE_ALPHA(destination, date, secret)

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

a

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

A

    Flip the order of the input bytes to little-endian

a'

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### حسابات التعمية

A'

LEOS2IP(x)

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret is optional, else zero-length
  A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of blinded public key A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD from the current date UTC
  secret = UTF-8 encoded string
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // treat seed as a 64 byte little-endian value
  alpha = seed mod L
```
H*(x)

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // If for a Ed25519 private key (type 7)
  seed = destination's signing private key
  a = left half of SHA512(seed) and clamped as usual for Ed25519
  // else, for a Red25519 private key (type 11)
  a = destination's signing private key
  // Addition using scalar arithmentic
  blinded signing private key = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  blinded signing public key = A' = DERIVE_PUBLIC(a')
```
يجب توليد سر جديد alpha ومفاتيح معتمة جديدة كل يوم (UTC).   يتم حساب السر alpha والمفاتيح المعتمة كما يلي.

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
GENERATE_ALPHA(destination, date, secret)، للجميع:

#### التوقيع

BLIND_PRIVKEY()، لمالك نشر leaseset:

BLIND_PUBKEY()، للعملاء الذين يسترجعون leaseset:

كلا طريقتي حساب A' تعطيان نفس النتيجة، كما هو مطلوب.

يتم توقيع leaseset غير المعتم بواسطة مفتاح التوقيع الخاص غير المعتم Ed25519 أو Red25519   ويتم التحقق منه باستخدام مفتاح التوقيع العام غير المعتم Ed25519 أو Red25519 (sig types 7 أو 11) كما هو معتاد.

#### حسابات التوقيع/التحقق

إذا كان مفتاح التوقيع العام خارجيًا،   يتم توقيع leaseset غير المعتم بواسطة مفتاح التوقيع الخاص المؤقت غير المعتم Ed25519 أو Red25519   ويتم التحقق منه باستخدام مفتاح التوقيع العام المؤقت Ed25519 أو Red25519 (sig types 7 أو 11) كما هو معتاد.   انظر أدناه لمزيد من الملاحظات حول المفاتيح الخارجية لـ leasesets المشفرة.

لتوقيع leaseset المشفر، نستخدم Red25519، استنادًا إلى [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)   لتوقيع والتحقق باستخدام مفاتيح معتمة.   التوقيعات Red25519 على منحنى Ed25519، باستخدام SHA-512 للتجزئة.

Red25519 مطابق تمامًا لـ Ed25519 باستثناء ما هو محدد أدناه.

تستخدم الجزء الخارجي من leaseset المشفر مفاتيح وتوقيعات Red25519.

Red25519 مطابق تقريبًا لـ Ed25519. هناك فرقان:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
مفاتيح Red25519 الخاصة تُولد من أرقام عشوائية ثم يجب أن تُختزل mod L، حيث L معرف أعلاه.   مفاتيح Ed25519 الخاصة تُولد من أرقام عشوائية ثم "تُشبك" باستخدام   القناع البتّي للبايتات 0 و31. لا يتم ذلك لـ Red25519.   الدوال GENERATE_ALPHA() و BLIND_PRIVKEY() المعرفة أعلاه تولد   مفاتيح Red25519 صحيحة باستخدام mod L.

```text
// same as in Ed25519
```
### التشفير والمعالجة

#### استخلاص بيانات الاعتماد الفرعية

في Red25519، حساب r للتوقيع يستخدم بيانات عشوائية إضافية،   ويستخدم قيمة المفتاح العام بدلاً من تجزئة المفتاح الخاص.   بسبب البيانات العشوائية، كل توقيع Red25519 مختلف، حتى   عند توقيع نفس البيانات بنفس المفتاح.

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
التوقيع:

التحقق:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
كجزء من عملية التعمية، نحتاج إلى ضمان أن LS2 المشفر يمكن فك تشفيره فقط من قبل شخص يعرف المفتاح العام للتوقيع للوجهة المقابلة.   الوجهة الكاملة غير مطلوبة.   لتحقيق ذلك، نستخلص بيانات اعتماد من المفتاح العام للتوقيع:

#### تشفير الطبقة 1

تضمن سلسلة التخصيص أن بيانات الاعتماد لا تتصادم مع أي تجزئة تستخدم   كمفتاح بحث DHT، مثل تجزئة الوجهة العادية.

```text
outerInput = subcredential || publishedTimestamp
```
للمفتاح المعتم، يمكننا بعد ذلك استخلاص بيانات اعتماد فرعية:

```text
outerSalt = CSRNG(32)
```
تُدرج بيانات الاعتماد الفرعية في عمليات استخلاص المفتاح أدناه، مما يربط   تلك المفاتيح بمعرفة مفتاح التوقيع العام للوجهة.

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
أولاً، يتم إعداد الإدخال لعملية استخلاص المفتاح:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### فك تشفير الطبقة 1

بعد ذلك، يتم توليد salt عشوائي:

```text
outerSalt = outerCiphertext[0:31]
```
ثم يتم استخلاص المفتاح المستخدم لتشفير الطبقة 1:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
أخيرًا، يتم تشفير وتوثيق نص الطبقة 1:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### تشفير الطبقة 2

يتم تحليل salt من نص الطبقة 1 المشفر:

ثم يتم استخلاص المفتاح المستخدم لتشفير الطبقة 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### فك تشفير الطبقة 2

أخيرًا، يتم فك تشفير نص الطبقة 1 المشفر:

عند تمكين مصادقة العميل، ``authCookie`` يتم حسابه كما هو موضح أدناه.   عند تعطيل مصادقة العميل، ``authCookie`` هو مصفوفة بايتات فارغة.

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### مصادقة العميل الفردية

يستمر التشفير بطريقة مشابهة للطبقة 1:

عند تمكين مصادقة العميل، ``authCookie`` يتم حسابه كما هو موضح أدناه.   عند تعطيل مصادقة العميل، ``authCookie`` هو مصفوفة بايتات فارغة.

#### مصادقة عميل DH

يستمر فك التشفير بطريقة مشابهة للطبقة 1:

عند تمكين مصادقة العميل لوجهة، يحافظ الخادم على قائمة   بالعملاء الذين يسمح لهم بفك تشفير بيانات LS2 المشفرة. البيانات المخزنة لكل عميل   تعتمد على آلية المصادقة، وتشمل شكلًا من أشكال مواد المفتاح التي يولدها كل   عميل ويرسلها إلى الخادم عبر آلية آمنة خارج النطاق.

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
هناك بديلين لتنفيذ مصادقة العميل الفردية:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
يولد كل عميل زوج مفاتيح DH ``[csk_i, cpk_i]``، ويرسل المفتاح العام ``cpk_i``   إلى الخادم.

معالجة الخادم ^^^^^^^^^^^^^^^^^ يولد الخادم ``authCookie`` جديدًا وزوج مفاتيح DH عابر:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
ثم لكل عميل مصرح له، يشفر الخادم ``authCookie`` إلى مفتاحه العام:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### مصادقة عميل المفتاح المشترك مسبقًا (PSK)

يضع الخادم كل زوج ``[clientID_i, clientCookie_i]`` في الطبقة 1 من   LS2 المشفر، مع ``epk``.

معالجة العميل ^^^^^^^^^^^^^^^^^ يستخدم العميل مفتاحه الخاص لاستخلاص معرف العميل المتوقع ``clientID_i``،   ومفتاح التشفير ``clientKey_i``، وIV التشفير ``clientIV_i``:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
ثم يبحث العميل في بيانات المصادقة للطبقة 1 عن إدخال يحتوي   ``clientID_i``. إذا وُجد إدخال مطابق، يفك تشفيره للحصول على   ``authCookie``:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
يولد كل عميل مفتاحًا سريًا بطول 32 بايت ``psk_i``، ويرسله إلى الخادم.   بديلًا، يمكن للخادم توليد مفتاح سري، وإرساله إلى عميل أو أكثر.

معالجة الخادم ^^^^^^^^^^^^^^^^^ يولد الخادم ``authCookie`` جديدًا وملح:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
ثم لكل عميل مصرح له، يشفر الخادم ``authCookie`` إلى مفتاحه المشترك مسبقًا:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### اعتبارات الأمان

يضع الخادم كل زوج ``[clientID_i, clientCookie_i]`` في الطبقة 1 من   LS2 المشفر، مع ``authSalt``.

معالجة العميل ^^^^^^^^^^^^^^^^^ يستخدم العميل مفتاحه المشترك مسبقًا لاستخلاص معرف العميل المتوقع ``clientID_i``،   ومفتاح التشفير ``clientKey_i``، وIV التشفير ``clientIV_i``:

ثم يبحث العميل في بيانات المصادقة للطبقة 1 عن إدخال يحتوي   ``clientID_i``. إذا وُجد إدخال مطابق، يفك تشفيره للحصول على   ``authCookie``:

توفر آلية مصادقة العميل أعلاه خصوصية لعضوية العميل.   الكيان الذي يعرف فقط الوجهة يمكنه رؤية عدد العملاء المشتركين في أي وقت،   ولكن لا يمكنه تتبع أي عملاء يتم إضافتهم أو إبطالهم.

- تشفير كل شيء لأغراض الأمان
- تشفير آمن، ليس فقط باستخدام AES.
- تشفير لكل مستلم

يجب على الخوادم عشوَنة ترتيب العملاء في كل مرة تولد فيها LS2 مشفرة، لمنع   العملاء من معرفة موضعهم في القائمة والاستدلال على متى تمت إضافة أو إبطال عملاء آخرين.

- طبقة خارجية تحتوي على المعلومات النصية الضرورية للتخزين والاسترجاع.
- طبقة وسطى تتعامل مع مصادقة العميل.
- طبقة داخلية تحتوي على بيانات LS2 الفعلية.

قد يختار الخادم إخفاء عدد العملاء المشتركين عن طريق إدراج إدخالات عشوائية   في قائمة بيانات المصادقة.

- يجب أن يكون مفتاح التوقيع العام في الوجهة غير المعتمة  
  Ed25519 (sig type 7) أو Red25519 (sig type 11)؛  
  لا تُدعم أنواع توقيع أخرى
- إذا كان مفتاح التوقيع العام خارجيًا، يجب أن يكون المفتاح العمومي للتوقيع المؤقت أيضًا Ed25519
- تعمية المفتاح بسيطة حسابيًا
- استخدام بنيات تشفيرية موجودة
- لا يمكن فك تعمية المفاتيح العامة المعتمة
- يجب أن تكون المفاتيح العامة المعتمة على منحنى Ed25519 والمجموعة الفرعية من الدرجة الأولية
- يجب معرفة مفتاح التوقيع العام للوجهة  
  (الوجهة الكاملة غير مطلوبة) لاستخلاص المفتاح العام المعتم
- توفير اختياري لسر إضافي مطلوب لاستخلاص المفتاح العام المعتم

مزايا مصادقة عميل DH ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- أمان المخطط لا يعتمد فقط على تبادل مواد مفتاح العميل خارج النطاق. لا يحتاج المفتاح الخاص للعميل إلى مغادرة جهازه، وبالتالي فإن الخصم الذي يمكنه اعتراض التبادل خارج النطاق، ولكن لا يمكنه كسر خوارزمية DH، لا يمكنه فك تشفير LS2 المشفر، أو تحديد مدة وصول العميل.

### LS مشفر مع عناوين Base 32

عيوب مصادقة عميل DH ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

مزايا مصادقة عميل PSK ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

### LS مشفر مع مفاتيح خارجية

عيوب مصادقة عميل PSK ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

انظر الاقتراح 149.

لا يمكنك استخدام LS2 مشفر لـ bittorrent، بسبب ردود الإعلان المدمجة التي تكون 32 بايت.   تحتوي الـ 32 بايت فقط على التجزئة. لا يوجد مجال للإشارة إلى أن   leaseset مشفر، أو أنواع التوقيع.

### ملاحظات

- يتطلب عمليات DH N + 1 في جانب الخادم لـ N عملاء.
- يتطلب عملية DH واحدة في جانب العميل.
- يتطلب من العميل توليد مفتاح سري.

- لا يتطلب عمليات DH.
- يسمح للخادم بتوليد مفتاح سري.
- يسمح للخادم بمشاركة نفس المفتاح مع عملاء متعددين، إذا رغب.

- أمان المخطط يعتمد بشكل حاسم على التبادل خارج النطاق لمواد مفتاح العميل. الخصم الذي يعترض التبادل لعميل معين يمكنه فك تشفير أي LS2 مشفر لاحقًا يتم التفويض له، وكذلك تحديد متى يتم إبطال وصول العميل.

- الخدمة التي تستخدم leasesets مشفرة ستنشر النسخة المشفرة إلى  
  خوادم التعبئة. ومع ذلك، من أجل الكفاءة، سترسل leasesets غير مشفرة إلى  
  العملاء في رسالة الثوم المغلفة، بعد المصادقة (عبر قائمة بيضاء، على  
  سبيل المثال).

- قد تحد خوادم التعبئة الحد الأقصى للحجم إلى قيمة معقولة لمنع الإساءة.

### Meta LS2

لـ leasesets المشفرة مع مفاتيح خارجية، يجب أيضًا توليد المفاتيح الخاصة المعتمة خارجيًا،   واحد لكل يوم.

بما أن كتلة التوقيع الخارجية اختيارية موجودة في جزء النص الواضح لـ leaseset المشفر،   يمكن لأي شخص يقوم بجمع بيانات من خوادم التعبئة استخدام هذا لتتبع leaseset (ولكن ليس فك تشفيره)   على مدى عدة أيام.   لمنع ذلك، يجب على مالك المفاتيح توليد مفاتيح مؤقتة جديدة   لكل يوم أيضًا.   يمكن توليد المفاتيح المؤقتة والمعتمة مسبقًا، وتسليمها إلى الراوتر   دفعة واحدة.

لا يوجد تنسيق ملف محدد في هذا الاقتراح لتغليف مفاتيح مؤقتة و   معتمة متعددة وتوفيرها للعميل أو الراوتر.   لا يوجد تحسين لبروتوكول I2CP محدد في هذا الاقتراح لدعم   leasesets مشفرة مع مفاتيح خارجية.

يُستخدم هذا لاستبدال الاتصال المتعدد. مثل أي leaseset، يتم توقيعه من قبل   المنشئ. هذا قائمة موثقة من تجزئات الوجهة.

يُعد Meta LS2 أعلى، وربما عقدًا وسيطة،   لهيكل شجري.   يحتوي على عدد من الإدخالات، كل منها يشير إلى LS أو LS2 أو Meta LS2 آخر   لدعم الاتصال المتعدد على نطاق واسع.   قد يحتوي Meta LS2 على مزيج من إدخالات LS وLS2 وMeta LS2.   أوراق الشجر في الشجرة تكون دائمًا LS أو LS2.   الشجرة عبارة عن DAG؛ الحلقات ممنوعة؛ يجب على العملاء الذين يقومون بالبحث اكتشاف الحلقات ورفض اتباعها.

قد يكون لـ Meta LS2 مدة انتهاء أطول بكثير من LS أو LS2 قياسي.   قد يكون للطبقة العليا انتهاء بعد تاريخ النشر بعدة ساعات.   سيتم فرض الحد الأقصى لوقت الانتهاء من قبل خوادم التعبئة والعملاء، وسيتم تحديده لاحقًا.

حالة الاستخدام لـ Meta LS2 هي الاتصال المتعدد على نطاق واسع، ولكن بدون   مزيد من الحماية لتتبع ارتباط الراوترات بـ leasesets (عند إعادة التشغيل) مما   يوفره الآن مع LS أو LS2.   هذا يعادل حالة استخدام "فيسبوك"، التي ربما لا تحتاج   إلى حماية التتبع. ربما تحتاج هذه الحالة إلى مفاتيح خارجية،   التي تُوفر في الرأس القياسي في كل عقدة من الشجرة.

بروتوكول الواجهة الخلفية للتنسيق بين الراوترات الطرفية، والوسيطة ووكلاء توقيع Meta LS الرئيسيين   غير محدد هنا. المتطلبات بسيطة جدًا - فقط التحقق من أن الطرف متصل،   وإعادة نشر LS كل بضع ساعات. التعقيد الوحيد هو اختيار   ناشرين جدد لـ Meta LS في المستوى العلوي أو الوسيط عند الفشل.

دمج leasesets حيث تُجمع الإيجارات من راوترات متعددة، وتُوقع، وتُنشر   في leaseset واحد موثق في الاقتراح 140، "الاتصال المتعدد الخفي".   هذا الاقتراح غير قابل للتطبيق كما هو مكتوب، لأن اتصالات البث لن تكون   "ثابتة" على راوتر واحد، انظر http://zzz.i2p/topics/2335 .

بروتوكول الواجهة الخلفية، والتفاعل مع داخليات الراوتر والعميل، سيكون   معقدًا جدًا للاتصال المتعدد الخفي.

    Standard LS flag (1)
لتجنب إغراق خادم التعبئة لـ Meta LS في المستوى العلوي، يجب أن يكون الانتهاء   بضع ساعات على الأقل. يجب على العملاء تخزين Meta LS في المستوى العلوي، والحفاظ عليه   عبر إعادة التشغيل إذا لم ينتهِ.

    Meta LS2 type (7)
نحتاج إلى تحديد خوارزمية للعملاء للتنقل في الشجرة، بما في ذلك خطط الاستبدال،   حتى يتم توزيع الاستخدام. بعض دالة المسافة بالتجزئة، التكلفة، والعشوائية.   إذا كان للعقدة كل من LS أو LS2 وMeta LS، نحتاج إلى معرفة متى يُسمح   باستخدام تلك leasesets، ومتى نستمر في التنقل في الشجرة.

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
البحث باستخدام

    Hours. Max 18.2 hours (65535 seconds)
التخزين باستخدام

    "master" Destination or coordinator, or intermediate coordinators

### التنسيق

```
Standard LS2 Header as specified above

  Meta LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of entries (1 byte) Maximum TBD
  - Entries. Each entry contains: (40 bytes)
    - Hash (32 bytes)
    - Flags (2 bytes)
      TBD. Set all to zero for compatibility with future uses.
    - Type (1 byte) The type of LS it is referencing;
      1 for LS, 3 for LS2, 5 for encrypted, 7 for meta, 0 for unknown.
    - Cost (priority) (1 byte)
    - Expires (4 bytes) (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Number of revocations (1 byte) Maximum TBD
  - Revocations: Each revocation contains: (32 bytes)
    - Hash (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
التخزين في

### ملاحظات

- بعد فك التشفير، يجب إجراء عدة فحوصات، بما في ذلك أن  
  الطابع الزمني والانتهاء الداخليين يتطابقان مع تلك الموجودة في المستوى العلوي.

- تم اختيار ChaCha20 على AES. بينما تكون السرعات متشابهة إذا كان  
  دعم AES متوفرًا في العتاد، فإن ChaCha20 أسرع بـ 2.5-3 مرات عندما  
  لا يكون دعم AES متوفرًا، مثل على أجهزة ARM منخفضة المستوى.

- لا نهتم كثيرًا بالسرعة لدرجة استخدام BLAKE2b المفتاح. لديه حجم مخرجات  
  كبيرًا بما يكفي لاستيعاب أكبر n نحتاجه (أو يمكننا استدعائه مرة واحدة لكل  
  مفتاح مرغوب به مع وسيطة عداد). BLAKE2b أسرع بكثير من SHA-256، و  
  BLAKE2b المفتاح سيخفض العدد الإجمالي لاستدعاءات دالة التجزئة.  
  ومع ذلك، انظر الاقتراح 148، حيث يُقترح أن ننتقل إلى BLAKE2b لأسباب أخرى.  
  انظر [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### سجل الخدمة

مدة الانتهاء النموذجية

ينشر بواسطة

العلامات والخصائص: للاستخدام المستقبلي

    n/a, see Service List
هذا سجل فردي يشير إلى أن الوجهة تشارك في   خدمة. يُرسل من المشارك إلى خادم التعبئة. لا يُرسل   فرديًا أبدًا بواسطة خادم التعبئة، ولكن فقط كجزء من قائمة الخدمة. يُستخدم سجل الخدمة   أيضًا لإبطال المشاركة في الخدمة، عن طريق ضبط   الانتهاء على صفر.

    Service Record type (9)
هذا ليس LS2 لكنه يستخدم تنسيق الرأس والتوقيع القياسي لـ LS2.

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
البحث باستخدام

    Hours. Max 18.2 hours (65535 seconds)
التخزين باستخدام

    Destination

### التنسيق

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### ملاحظات

- الخدمة الموزعة التي تستخدم هذا سيكون لديها "رئيسي" واحد أو أكثر مع  
  المفتاح الخاص لوجهة الخدمة. سيحددون (خارج النطاق)  
  القائمة الحالية للوجهات النشطة وسينشرون Meta LS2. من أجل  
  التكرار، يمكن لعدة رؤساء أن يشتركوا (أي ينشروا في وقت واحد)  
  Meta LS2.

- يمكن لخدمة موزعة أن تبدأ بوجهة واحدة أو تستخدم  
  الاتصال المتعدد القديم، ثم تنتقل إلى Meta LS2. يمكن لاستعلام LS قياسي أن يعيد  
  أيًا من LS أو LS2 أو Meta LS2.

- عندما تستخدم خدمة Meta LS2، ليس لديها أنفاق (إيجارات).

### قائمة الخدمة

التخزين في

مدة الانتهاء النموذجية

ينشر بواسطة

هذا لا يشبه LS2 ويستخدم تنسيقًا مختلفًا.

تُنشأ قائمة الخدمة وتُوقع بواسطة خادم التعبئة. إنها غير موثقة   بمعنى أن أي شخص يمكنه الانضمام إلى خدمة بنشر سجل خدمة إلى   خادم تعبئة.

تحتوي قائمة الخدمة على سجلات خدمة قصيرة، وليس سجلات خدمة كاملة. هذه   تحتوي على توقيعات ولكن فقط تجزئات، وليس وجهات كاملة، لذلك لا يمكن التحقق منها دون   الوجهة الكاملة.

    Service List lookup type (11)
الأمان، إن وُجد، ورغبة قوائم الخدمة قيد المراجعة.   يمكن لخوادم التعبئة تقييد النشر، والاستعلامات، إلى قائمة بيضاء من الخدمات،   لكن تلك القائمة البيضاء قد تختلف حسب التنفيذ، أو تفضيل المشغل.   قد لا يكون من الممكن تحقيق توافق على قائمة بيضاء مشتركة أساسية   عبر التنفيذات.

    Service List type (11)
إذا تم تضمين اسم الخدمة في سجل الخدمة أعلاه،   فقد يعترض مشغلو خوادم التعبئة؛ إذا تم تضمين التجزئة فقط،   فلا يوجد تحقق، ويمكن

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
البحث باستخدام

    Hours, not specified in the list itself, up to local policy
التخزين باستخدام

    Nobody, never sent to floodfill, never flooded.

### التنسيق

يتكون تنسيق LS2 المشفر من ثلاث طبقات متداخلة:

```
- Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Hash of the service name (implicit, in the Database Store message)
  - Hash of the Creator (floodfill) (32 bytes)
  - Published timestamp (8 bytes, big endian)

  - Number of Short Service Records (1 byte)
  - List of Short Service Records:
    Each Short Service Record contains (90+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Expires (4 bytes, big endian) (offset from published in ms)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Number of Revocation Records (1 byte)
  - List of Revocation Records:
    Each Revocation Record contains (86+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Signature of floodfill (40+ bytes)
    The signature is of everything above.
```
للتحقق من توقيع قائمة الخدمات:

- إذا كان الانتهاء جميع أصفار، يجب على خادم التعبئة إبطال السجل وعدم  
  تضمينه في قائمة الخدمة بعد الآن.

للتحقق من توقيع كل سجل خدمة قصير:

- التخزين: قد يقيد خادم التعبئة التخزين الصارم لهذه السجلات  
  ويحد من عدد السجلات المخزنة لكل تجزئة وانتهائها. قد تُستخدم  
  قائمة بيضاء من التجزئات.

للتحقق من توقيع كل سجل إبطال:

- أي نوع netdb آخر عند نفس التجزئة له أولوية، لذلك لا يمكن لسجل الخدمة أبدًا  
  أن يكتب فوق LS/RI، لكن LS/RI سيكتب فوق جميع سجلات الخدمة عند تلك التجزئة.

### ملاحظات

- نستخدم طول التوقيع بدلاً من نوع التوقيع حتى نتمكن من دعم أنواع توقيع غير معروفة.

- لا يوجد تاريخ انتهاء لقائمة الخدمات، ويمكن للمستلمين اتخاذ قرارهم الخاص بناءً على السياسة أو انتهاء صلاحية السجلات الفردية.

- لا تُبثّ قوائم الخدمة عبر flooding، بل تُبثّ سجلات الخدمة الفردية فقط. كل
  floodfill ينشئ قائمة خدمة ويوقّعها ويخزّنها مؤقتًا. ويستخدم floodfill
  سياسة خاصة به لمدة التخزين المؤقت والحد الأقصى لعدد سجلات الخدمة والإلغاء.

## التغييرات المطلوبة في مواصفات الهياكل المشتركة

### شهادات المفاتيح

خارج نطاق هذا الاقتراح. يُضاف إلى اقتراحَي ECIES رقم 144 و145.

### هياكل وسيطة جديدة

إضافة هياكل جديدة لـ Lease2 وMetaLease وLeaseSet2Header وOfflineSignature. سارية اعتبارًا من الإصدار 0.9.38.

### أنواع NetDB الجديدة

إضافة هياكل لكل نوع leaseSet جديد، مدمجة مما ورد أعلاه. بالنسبة إلى LeaseSet2 وEncryptedLeaseSet وMetaLeaseSet، سارية اعتبارًا من الإصدار 0.9.38. وبالنسبة إلى Service Record وService List، فهي أولية وغير مجدولة.

### نوع توقيع جديد

أضف RedDSA_SHA512_Ed25519 من النوع 11. المفتاح العام 32 بايت؛ المفتاح الخاص 32 بايت؛ التجزئة 64 بايت؛ التوقيع 64 بايت.

## التغييرات المطلوبة في مواصفات التشفير

خارج نطاق هذا المقترح. راجع المقترحين 144 و145.

## التغييرات المطلوبة في I2NP

أضف ملاحظة: لا يمكن نشر LS2 إلا إلى floodfills ذات حد أدنى من الإصدار.

### رسالة البحث في قاعدة البيانات

أضف نوع البحث عن قائمة الخدمات

### التغييرات

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### رسالة تخزين قاعدة البيانات

أضف جميع أنواع المخازن الجديدة.

### التغييرات

```
Type byte: Type field, currently bit 0, expands to bits 3-0.
  Type 3 is defined as a LS2 store.
  Type 5 is defined as a encrypted LS2 store.
  Type 7 is defined as a meta LS2 store.
  Type 9 is defined as a service record store.
  Type 11 is defined as a service list store.
  Other types are undefined and invalid.

  Add note: All new types may only be published to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
## التغييرات المطلوبة في I2CP

### خيارات I2CP

خيارات جديدة تُفسَّر من جهة router، وتُرسَل في SessionConfig Mapping:

```

  i2cp.leaseSetType=nnn       The type of leaseset to be sent in the Create Leaseset Message
                              Value is the same as the netdb store type in the table above.
                              Interpreted client-side, but also passed to the router in the
                              SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetOfflineExpiration=nnn  The expiration of the offline signature, ASCII,
                                      seconds since the epoch.

  i2cp.leaseSetTransientPublicKey=[type:]b64  The base 64 of the transient private key,
                                              prefixed by an optional sig type number
                                              or name, default DSA_SHA1.
                                              Length as inferred from the sig type

  i2cp.leaseSetOfflineSignature=b64   The base 64 of the offline signature.
                                      Length as inferred from the destination
                                      signing public key type

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn   The type of authentication for encrypted LS2.
                              0 for no per-client authentication (the default)
                              1 for DH per-client authentication
                              2 for PSK per-client authentication

  i2cp.leaseSetPrivKey=b64    A base 64 private key for the router to use to
                              decrypt the encrypted LS2,
                              only if per-client authentication is enabled
```
خيارات جديدة تُفسَّر على جانب العميل:

```

  i2cp.leaseSetType=nnn     The type of leaseset to be sent in the Create Leaseset Message
                            Value is the same as the netdb store type in the table above.
                            Interpreted client-side, but also passed to the router in the
                            SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn       The type of authentication for encrypted LS2.
                                  0 for no per-client authentication (the default)
                                  1 for DH per-client authentication
                                  2 for PSK per-client authentication

  i2cp.leaseSetBlindedType=nnn   The sig type of the blinded key for encrypted LS2.
                                 Default depends on the destination sig type.

  i2cp.leaseSetClient.dh.nnn=b64name:b64pubkey   The base 64 of the client name (ignored, UI use only),
                                                 followed by a ':', followed by the base 64 of the public
                                                 key to use for DH per-client auth. nnn starts with 0

  i2cp.leaseSetClient.psk.nnn=b64name:b64privkey   The base 64 of the client name (ignored, UI use only),
                                                   followed by a ':', followed by the base 64 of the private
                                                   key to use for PSK per-client auth. nnn starts with 0
```
### إعدادات الجلسة

لاحظ أنه بالنسبة للتوقيعات دون اتصال، فإن الخيارات i2cp.leaseSetOfflineExpiration وi2cp.leaseSetTransientPublicKey وi2cp.leaseSetOfflineSignature مطلوبة، ويتم التوقيع باستخدام المفتاح الخاص للتوقيع المؤقت.

### رسالة طلب LeaseSet

من router إلى العميل. دون تغييرات. تُرسل الـ leases بطوابع زمنية من 8 بايت، حتى إذا كان leaseSet المُعاد سيكون LS2 بطوابع زمنية من 4 بايت. لاحظ أن الاستجابة قد تكون Create Leaseset أو Create Leaseset2 Message.

### رسالة طلب Leaseset متغير

من router إلى العميل. دون تغييرات. تُرسل الـ leases بطوابع زمنية من 8 بايت، حتى إذا كان leaseSet المُعاد سيكون LS2 بطوابع زمنية من 4 بايت. لاحظ أن الاستجابة قد تكون Create Leaseset أو Create Leaseset2 Message.

### إنشاء رسالة Leaseset2

من العميل إلى router. رسالة جديدة، تُستخدم بدلاً من Create Leaseset Message.

### التبرير

- لكي يتمكن router من تحليل store type، يجب أن يكون النوع موجودًا في الرسالة، ما لم يكن قد مُرّر إلى router مسبقًا ضمن إعدادات الجلسة. وبالنسبة لكود التحليل الشائع، يكون من الأسهل تضمينه في الرسالة نفسها.

- لكي يعرف router نوع المفتاح الخاص وطوله،
  يجب أن يقع بعد lease set، ما لم يكن parser يعرف النوع مسبقًا
  في إعدادات الجلسة.
  وبالنسبة لكود parsing الشائع، من الأسهل معرفته من الرسالة نفسها.

- المفتاح الخاص للتوقيع، الذي عُرّف سابقًا لأغراض الإبطال ولم يُستخدم، غير موجود في LS2.

### نوع الرسالة

نوع الرسالة الخاص بـ Create Leaseset2 Message هو 41.

### التنسيق

```
Session ID
  Type byte: Type of lease set to follow
             Type 1 is a LS
             Type 3 is a LS2
             Type 5 is a encrypted LS2
             Type 7 is a meta LS2
  LeaseSet: type specified above
  Number of private keys to follow (1 byte)
  Encryption Private Keys: For each public key in the lease set,
                           in the same order
                           (Not present for Meta LS2)
                           - Encryption type (2 bytes, big endian)
                           - Encryption key length (2 bytes, big endian)
                           - Encryption key (number of bytes specified)
```
### ملاحظات

- الحد الأدنى لإصدار router هو 0.9.39.
- كان هناك إصدار أولي بنوع الرسالة 40 في 0.9.38، لكن التنسيق تغيّر.
  النوع 40 مهجور وغير مدعوم.

### المشكلات

يلزم إجراء مزيد من التغييرات لدعم LS المشفرة وmeta LS.

### رسالة معلومات التعتيم

من العميل إلى router. رسالة جديدة.

### التبرير

- يحتاج الrouter إلى معرفة ما إذا كانت الوجهة مُعمّاة.
  وإذا كانت مُعمّاة وتستخدم مصادقة سرية أو مصادقة خاصة بكل عميل،
  فإنه يحتاج إلى تلك المعلومات أيضًا.

- يؤدي Host Lookup لعنوان b32 بصيغة جديدة ("b33") إلى إبلاغ الـ router بأن العنوان مُعمّى، لكن لا توجد آلية لتمرير المفتاح السري أو الخاص إلى الـ router في رسالة Host Lookup. ورغم أنه يمكننا توسيع رسالة Host Lookup لإضافة تلك المعلومات، فإنه من الأنظف تعريف رسالة جديدة.

- نحتاج إلى طريقة برمجية تتيح للعميل إبلاغ router.
  وإلا فسيضطر المستخدم إلى تكوين كل وجهة يدويًا.

### الاستخدام

قبل أن يرسل العميل رسالة إلى وجهة معمّاة، يجب عليه إما البحث عن "b33" في رسالة Host Lookup، أو إرسال رسالة Blinding Info. وإذا كانت الوجهة المعمّاة تتطلب سرًا أو مصادقة لكل عميل، فيجب على العميل إرسال رسالة Blinding Info.

لا يرسل الـ router أي رد على هذه الرسالة.

### نوع الرسالة

نوع الرسالة الخاصة بـ Blinding Info Message هو 42.

### التنسيق

```
Session ID
  Flags:       1 byte
               Bit order: 76543210
               Bit 0: 0 for everybody, 1 for per-client
               Bits 3-1: Authentication scheme, if bit 0 is set to 1 for per-client, otherwise 000
                         000: DH client authentication (or no per-client authentication)
                         001: PSK client authentication
               Bit 4: 1 if secret required, 0 if no secret required
               Bits 7-5: Unused, set to 0 for future compatibility
  Type byte:   Endpoint type to follow
               Type 0 is a Hash
               Type 1 is a host name String
               Type 2 is a Destination
               Type 3 is a Sig Type and Signing Public Key
  Blind Type:  2 byte blinded sig type (big endian)
  Expiration:  4 bytes, big endian, seconds since epoch
  Endpoint:    Data as specified above
               For type 0: 32 byte binary hash
               For type 1: host name String
               For type 2: binary Destination
               For type 3: 2 byte sig type (big endian)
                           Signing Public Key (length as implied by sig type)
  Private Key: Only if flag bit 0 is set to 1
               A 32-byte ECIES_X25519 private key
  Secret:      Only if flag bit 4 is set to 1
               A secret String
```
### ملاحظات

- الحد الأدنى لإصدار الـ router هو 0.9.43

### المشكلات

### رسالة رد المضيف (enc)

لدعم عمليات البحث عن أسماء المضيفين "b33" وإرجاع مؤشر إذا كان الـ router لا يملك المعلومات المطلوبة، نعرّف رموز نتائج إضافية لرسالة Host Reply Message، على النحو التالي:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
القيم من 1 إلى 255 معرّفة بالفعل كأخطاء، لذا لا توجد مشكلة في التوافق العكسي.

### رسالة إعادة التوجيه Meta

من router إلى العميل. رسالة جديدة.

### التبرير

لا يعرف العميل مسبقًا أن Hash معينًا سيُحل إلى Meta LS.

إذا أعاد بحث leaseset الخاص بـ Destination قيمة Meta LS، فسيجري router التحليل التكراري. بالنسبة للـ datagrams، لا يحتاج جانب العميل إلى معرفة ذلك؛ ومع ذلك، في streaming، حيث يتحقق البروتوكول من Destination في SYN ACK، يجب أن يعرف ما هو Destination "الحقيقي". لذلك، نحتاج إلى رسالة جديدة.

### الاستخدام

يحتفظ الـ router بذاكرة مؤقتة للـ destination الفعلي المستخدم من meta LS. عندما يرسل العميل رسالة إلى destination يُحلّ إلى meta LS، يتحقق الـ router من الذاكرة المؤقتة بحثًا عن الـ destination الفعلي المستخدم آخر مرة. إذا كانت الذاكرة المؤقتة فارغة، يختار الـ router destination من meta LS، ويبحث عن الـ leaseset. إذا نجح البحث عن الـ leaseset، يضيف الـ router ذلك الـ destination إلى الذاكرة المؤقتة، ويرسل إلى العميل Meta Redirect Message. ويُجرى ذلك مرة واحدة فقط، ما لم ينتهِ صلاحية الـ destination ويجب تغييره. وعلى العميل أيضًا تخزين المعلومات مؤقتًا إذا لزم الأمر. ولا تُرسل Meta Redirect Message ردًّا على كل SendMessage.

لا يرسل الـ router هذه الرسالة إلا إلى clients ذات الإصدار 0.9.47 أو أحدث.

لا يرسل العميل ردًا على هذه الرسالة.

### نوع الرسالة

نوع الرسالة الخاص بـ Meta Redirect Message هو 43.

### التنسيق

```
Session ID (2 bytes) The value from the Send Message.
  Message ID generated by the router (4 bytes)
  4 byte nonce previously generated by the client
               (the value from the Send Message, may be zero)
  Flags:       2 bytes, bit order 15...0
               Unused, set to 0 for future compatibility
               Bit 0: 0 - the destination is no longer meta
                      1 - the destination is now meta
               Bits 15-1: Unused, set to 0 for future compatibility
  Original Destination (387+ bytes)
  (following fields only present if flags bit 0 is 1)
  MFlags:      2 bytes
               Unused, set to 0 for future compatibility
               From the Meta Lease for the actual Destination
  Expiration:  4 bytes, big endian, seconds since epoch
               From the Meta Lease for the actual Destination
  Cost (priority) 1 byte
               From the Meta Lease for the actual Destination
  Actual (real) Destination (387+ bytes)
```
### تغييرات لدعم Meta

كيفية توليد Meta ودعمها، بما في ذلك التواصل والتنسيق بين routers، خارج نطاق هذا المقترح. انظر المقترح ذي الصلة 150.

### تغييرات لدعم Offline Keys

لا يمكن التحقق من التوقيعات غير المتصلة في streaming أو repliable datagrams. راجع الأقسام أدناه.

## تغييرات مطلوبة في ملف المفتاح الخاص

تنسيق ملف المفتاح الخاص (eepPriv.dat) ليس جزءًا رسميًا من مواصفاتنا، لكنه موثّق في [javadocs Java I2P](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) وتدعمه تنفيذات أخرى. يتيح ذلك قابلية نقل المفاتيح الخاصة إلى تنفيذات مختلفة.

ثمة حاجة إلى تغييرات لتخزين المفتاح العام العابر ومعلومات التوقيع دون اتصال.

### التغييرات

```
If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key
    (length as specified by transient sig type)
```
### التغييرات المطلوبة في واجهة سطر الأوامر لملف المفتاح الخاص

إضافة دعم للخيارات التالية:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## التغييرات المطلوبة في البث

لا يمكن التحقق من التوقيعات غير المتصلة حالياً أثناء البث. يُضيف التغيير أدناه كتلة التوقيع غير المتصل إلى الخيارات. يتجنب ذلك الحاجة إلى استرداد هذه المعلومات عبر I2CP.

### التغييرات

```
Add new option:
  Bit:          11
  Flag:         OFFLINE_SIGNATURE
  Option order: 4
  Option data:  Variable bytes
  Function:     Contains the offline signature section from LS2.
                FROM_INCLUDED must also be set.
                Expires timestamp
                (4 bytes, big endian, seconds since epoch, rolls over in 2106)
                Transient sig type (2 bytes, big endian)
                Transient signing public key (length as implied by sig type)
                Signature of expires timestamp, transient sig type,
                and public key, by the destination public key,
                length as implied by destination public key sig type.

  Change option:
  Bit:          3
  Flag:         SIGNATURE_INCLUDED
  Option order: Change from 4 to 5

  Add information about transient keys to the
  Variable Length Signature Notes section:
  The offline signature option does not needed to be added for a CLOSE packet if
  a SYN packet containing the option was previously acked.
  More info TODO
```
### ملاحظات

- البديل هو مجرد إضافة علامة، واسترداد المفتاح العام العابر عبر I2CP
  (انظر أقسام Host Lookup / Host Reply Message أعلاه)

## التغييرات المطلوبة في Repliable Datagram

لا يمكن التحقق من التوقيعات غير المتصلة في معالجة الحزم القابلة للرد. يتطلب الأمر علامة (flag) تشير إلى أن التوقيع تم خارج الخط، ولكن لا يوجد مكان لوضع هذه العلامة. وسيتطلب ذلك رقم (ذلك) رقم بروتوكول وتنسيقاً جديداً بالكامل.

### التغييرات

```
Define new protocol 19 - Repliable datagram with options?
  - Destination (387+ bytes)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bits 1-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type,
    and public key, by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
  - Data
```
### ملاحظات

- البديل هو مجرد إضافة flag، واسترداد المفتاح العام العابر عبر I2CP
  (انظر أقسام Host Lookup / Host Reply Message أعلاه)
- أي خيارات أخرى ينبغي أن نضيفها الآن بعد أن أصبح لدينا flag bytes؟

## التغييرات المطلوبة في SAM V3

يجب تحسين SAM ليدعم التوقيعات دون اتصال في DESTINATION base 64.

### التغييرات

```
Note that in the SESSION CREATE DESTINATION=$privkey,
  the $privkey raw data (before base64 conversion)
  may be optionally followed by the Offline Signature as specified in the
  Common Structures Specification.

  If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key (length as specified by transient sig type)
```
لاحظ أن التوقيعات دون اتصال مدعومة فقط في STREAM و RAW، وليس في DATAGRAM (حتى نعرّف بروتوكول DATAGRAM جديدًا).

لاحظ أن SESSION STATUS سيُعيد Signing Private Key مكوّنًا من أصفار فقط، وبيانات Offline Signature كما وردت تمامًا في SESSION CREATE.

لاحظ أنه لا يجوز استخدام DEST GENERATE و SESSION CREATE DESTINATION=TRANSIENT لإنشاء وجهة موقعة دون اتصال.

### المشكلات

هل نرفع الإصدار إلى 3.4، أم نتركه عند 3.1/3.2/3.3 بحيث يمكن إضافته دون اشتراط كل أمور 3.2/3.3؟

التغييرات الأخرى تُحدد لاحقًا. انظر قسم I2CP Host Reply Message أعلاه.

## التغييرات المطلوبة في BOB

سيتعين تحسين BOB لدعم التوقيعات دون اتصال و/أو Meta LS. هذه أولوية منخفضة، ومن المحتمل ألا يتم تحديدها أو تنفيذها أبدًا. SAM V3 هو الواجهة المفضلة.

## النشر والترحيل والتوافق

تُنشر LS2 (بخلاف LS2 المشفّرة) في الموقع نفسه ضمن DHT الذي تُنشر فيه LS1. لا توجد طريقة لنشر LS1 وLS2 معًا، إلا إذا كانت LS2 في موقع مختلف.

يُنشر LS2 المشفّر عند الـ hash الخاص بنوع المفتاح المُعمّى وبيانات المفتاح. ثم يُستخدم هذا الـ hash لتوليد «routing key» اليومي، كما في LS1.

لن يُستخدم LS2 إلا عند الحاجة إلى ميزات جديدة (تشفير جديد، LS مشفّر، meta، إلخ). لا يمكن نشر LS2 إلا إلى floodfills بإصدار محدد أو أعلى.

ستعرف الخوادم التي تنشر LS2 أن أي عملاء يتصلون يدعمون LS2. ويمكنها إرسال LS2 داخل garlic.

لن يرسل العملاء LS2 داخل garlics إلا إذا كانوا يستخدمون التشفير الجديد. هل سيستخدم العملاء المشتركون LS1 إلى أجل غير مسمى؟ TODO: كيف يمكن الحصول على عملاء مشتركين يدعمون كلاً من التشفير القديم والجديد؟

## الطرح

يتضمن 0.9.38 دعم floodfill لـ LS2 القياسي، بما في ذلك offline keys.

يتضمن 0.9.39 دعم I2CP لـ LS2 وEncrypted LS2، وتوقيع/تحقق sig type 11، ودعم floodfill لـ Encrypted LS2 (sig types 7 و11، دون مفاتيح دون اتصال)، وتشفير/فك تشفير LS2 (دون تفويض لكل عميل).

من المقرر أن يتضمن الإصدار 0.9.40 دعم تشفير/فك تشفير LS2 مع تفويض لكل عميل، ودعم floodfill وI2CP لـ Meta LS2، ودعم LS2 المشفّر بمفاتيح دون اتصال، ودعم b32 لـ LS2 المشفّر.

## شكر وتقدير

يتأثر تصميم LS2 المشفّر بشكل كبير بـ[واصفات الخدمات المخفية v3 الخاصة بـTor](https://spec.torproject.org/rend-spec-v3)، التي كانت لها أهداف تصميم مشابهة.

## المراجع

* ["توقيعات عالية السرعة وعالية الأمان" بواسطة Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe و Bo-Yin Yang](https://ed25519.cr.yp.to/)
* [KEYBLIND-PROOF](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)
* [KEYBLIND-REFS](https://gitlab.torproject.org/tpo/core/tor/-/issues/8106)
* [PRNG-REFS](http://projectbullrun.org/dual-ec/ext-rand.html)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
* [RFC-7539-S2.4](https://tools.ietf.org/html/rfc7539#section-2.4)
* [TOR-REND-SPEC-V3](https://spec.torproject.org/rend-spec-v3)
* [UNSCIENTIFIC-KDF-SPEEDS](https://www.lvh.io/posts/secure-key-derivation-performance.html)
* [ZCASH](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)
