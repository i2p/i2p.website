---
title: "إدخالات netDB جديدة"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "مفتوح"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## الحالة

أجزاء من هذا الاقتراح مكتملة، ومُنفذة في الإصدارين 0.9.38 و 0.9.39. مواصفات Common Structures و I2CP و I2NP والمواصفات الأخرى محدثة الآن لتعكس التغييرات المدعومة حالياً.

الأجزاء المكتملة لا تزال عرضة لمراجعات طفيفة. الأجزاء الأخرى من هذا الاقتراح لا تزال قيد التطوير وعرضة لمراجعات جوهرية.

البحث عن الخدمة (الأنواع 9 و 11) هي منخفضة الأولوية وغير مجدولة، وقد يتم فصلها إلى اقتراح منفصل.

## نظرة عامة

هذا تحديث وتجميع للاقتراحات الأربعة التالية:

- 110 LS2
- 120 Meta LS2 للاستضافة المتعددة الضخمة
- 121 LS2 مشفر
- 122 البحث عن الخدمة غير المصادق عليه (anycasting)

هذه المقترحات مستقلة في الغالب، ولكن من أجل الوضوح نقوم بتعريف واستخدام تنسيق موحد لعدة منها.

الاقتراحات التالية مترابطة إلى حد ما:

- 140 Invisible Multihoming (غير متوافق مع هذا الاقتراح)
- 142 New Crypto Template (لتشفير متماثل جديد)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 for Encrypted LS2
- 150 Garlic Farm Protocol
- 151 ECDSA Blinding

## اقتراح

هذا الاقتراح يحدد 5 أنواع جديدة من DatabaseEntry والعملية لتخزينها في واسترجاعها من قاعدة بيانات الشبكة، بالإضافة إلى طريقة توقيعها والتحقق من تلك التوقيعات.

### Goals

- متوافق مع الإصدارات السابقة
- LS2 قابل للاستخدام مع الاستضافة المتعددة القديمة
- لا تتطلب تشفير أو أساسيات جديدة للدعم
- الحفاظ على فصل التشفير والتوقيع؛ دعم جميع الإصدارات الحالية والمستقبلية
- تمكين مفاتيح التوقيع غير المتصلة الاختيارية
- تقليل دقة الطوابع الزمنية لتقليل بصمات الأصابع
- تمكين التشفير الجديد للوجهات
- تمكين الاستضافة المتعددة الضخمة
- إصلاح مشاكل متعددة مع LS المشفر الموجود
- إخفاء اختياري لتقليل الرؤية بواسطة floodfills
- المشفر يدعم كلاً من المفتاح الواحد والمفاتيح المتعددة القابلة للإلغاء
- البحث عن الخدمة لتسهيل البحث عن outproxies، وتشغيل تطبيق DHT،
  والاستخدامات الأخرى
- عدم كسر أي شيء يعتمد على hashes الوجهة الثنائية 32-byte، مثل bittorrent
- إضافة مرونة إلى leasesets عبر الخصائص، كما لدينا في routerinfos
- وضع الطابع الزمني المنشور والانتهاء المتغير في الرأس، حتى يعمل حتى
  إذا كان المحتوى مشفراً (لا تستمد الطابع الزمني من أقرب lease)
- جميع الأنواع الجديدة تعيش في نفس مساحة DHT ونفس المواقع مثل leasesets الموجودة،
  بحيث يمكن للمستخدمين الانتقال من LS القديم إلى LS2،
  أو التغيير بين LS2 وMeta وEncrypted،
  دون تغيير الوجهة أو hash
- يمكن تحويل وجهة موجودة لاستخدام المفاتيح غير المتصلة،
  أو العودة إلى المفاتيح المتصلة، دون تغيير الوجهة أو hash

### Non-Goals / Out-of-scope

- خوارزمية تدوير DHT جديدة أو توليد عشوائي مشترك
- نوع التشفير الجديد المحدد ونظام التشفير من النهاية إلى النهاية
  لاستخدام هذا النوع الجديد سيكون في اقتراح منفصل.
  لا يتم تحديد أو مناقشة أي تشفير جديد هنا.
- تشفير جديد لـ RIs أو بناء الأنفاق.
  سيكون ذلك في اقتراح منفصل.
- طرق تشفير ونقل واستقبال رسائل I2NP DLM / DSM / DSRM.
  لا يتم التغيير.
- كيفية توليد ودعم Meta، بما في ذلك التواصل بين الـ router في الخلفية، والإدارة، والتعافي من الأعطال، والتنسيق.
  قد يتم إضافة الدعم إلى I2CP، أو i2pcontrol، أو بروتوكول جديد.
  قد يتم توحيد هذا أو لا.
- كيفية تنفيذ وإدارة الأنفاق طويلة الانتهاء فعلياً، أو إلغاء الأنفاق الموجودة.
  هذا صعب للغاية، وبدونه، لا يمكن الحصول على إغلاق سلس معقول.
- تغييرات نموذج التهديد
- تنسيق التخزين غير المتصل، أو طرق تخزين/استرجاع/مشاركة البيانات.
- تفاصيل التنفيذ لا تُناقش هنا وتُترك لكل مشروع.

### Justification

LS2 يضيف حقول لتغيير نوع التشفير وللتغييرات المستقبلية في البروتوكول.

يعمل LS2 المشفر على إصلاح عدة مشاكل أمنية موجودة في LS المشفر الحالي من خلال استخدام التشفير غير المتماثل لمجموعة leases بأكملها.

يوفر Meta LS2 تعدد الاستضافة المرن والفعال والمؤثر واسع النطاق.

سجل الخدمة وقائمة الخدمة توفر خدمات anycast مثل البحث عن الأسماء وتهيئة DHT الأولية.

### الأهداف

أرقام الأنواع تُستخدم في رسائل I2NP Database Lookup/Store Messages.

يشير عمود الطرف إلى الطرف إلى ما إذا كانت الاستعلامات/الاستجابات يتم إرسالها إلى Destination في Garlic Message.

الأنواع الموجودة:

| NetDB Data | Lookup Type | Store Type |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
أنواع جديدة:

| NetDB Data     | Lookup Type | Store Type | Std. LS2 Header? | Sent end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | yes              | yes              |
| Encrypted LS2  | 1           | 5          | no               | no               |
| Meta LS2       | 1           | 7          | yes              | no               |
| Service Record | n/a         | 9          | yes              | no               |
| Service List   | 4           | 11         | no               | no               |
### الأهداف غير المطلوبة / خارج النطاق

- أنواع البحث حالياً هي البتات 3-2 في رسالة البحث في قاعدة البيانات.
  أي أنواع إضافية ستتطلب استخدام البت 4.

- جميع أنواع المتاجر فردية لأن البتات العلوية في حقل نوع رسالة Database Store Message
  يتم تجاهلها بواسطة الموجهات القديمة.
  نفضل أن يفشل التحليل كـ LS بدلاً من RI مضغوط.

- هل يجب أن يكون النوع صريحًا أم ضمنيًا أم لا هذا ولا ذاك في البيانات المشمولة بالتوقيع؟

### مبرر

الأنواع 3 و 5 و 7 قد يتم إرجاعها استجابة لبحث leaseset قياسي (النوع 1). النوع 9 لا يتم إرجاعه أبداً استجابة للبحث. النوع 11 يتم إرجاعه استجابة لنوع بحث خدمة جديد (النوع 11).

يمكن إرسال النوع 3 فقط في رسالة Garlic من عميل إلى عميل.

### أنواع بيانات NetDB

الأنواع 3 و 7 و 9 جميعها لها تنسيق مشترك::

رأس LS2 المعياري - كما هو محدد أدناه

الجزء الخاص بالنوع - كما هو محدد أدناه في كل جزء

التوقيع القياسي LS2:   - الطول كما هو مضمن في نوع التوقيع لمفتاح التوقيع

النوع 5 (المُشفر) لا يبدأ بـ Destination وله تنسيق مختلف. انظر أدناه.

النوع 11 (قائمة الخدمات) هو تجميع لعدة Service Records وله تنسيق مختلف. انظر أدناه.

### ملاحظات

سيتم تحديدها لاحقاً

## Standard LS2 Header

الأنواع 3 و 7 و 9 تستخدم رأس LS2 المعياري، المحدد أدناه:

### عملية البحث/التخزين

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
### تنسيق

- غير منشور/منشور: للاستخدام عند إرسال database store من نقطة إلى نقطة،
  قد يرغب الـ router المرسل في الإشارة إلى أن هذا الـ leaseset يجب ألا يُرسل
  إلى آخرين. نحن نستخدم حالياً heuristics للحفاظ على هذه الحالة.

- منشور: يستبدل المنطق المعقد المطلوب لتحديد 'الإصدار' الخاص بـ
  leaseset. حالياً، الإصدار هو انتهاء صلاحية آخر lease منتهي الصلاحية،
  ويجب على router النشر زيادة انتهاء الصلاحية هذا بما لا يقل عن 1ms عند
  نشر leaseset يزيل فقط lease أقدم.

- Expires: يسمح بانتهاء صلاحية إدخال netDb قبل انتهاء صلاحية آخر leaseset منتهي الصلاحية الخاص به. قد لا يكون مفيداً لـ LS2، حيث من المتوقع أن تبقى leasesets بحد أقصى 11 دقيقة لانتهاء الصلاحية، ولكن للأنواع الجديدة الأخرى، فهو ضروري (انظر Meta LS وService Record أدناه).

- المفاتيح غير المتصلة اختيارية، لتقليل تعقيد التنفيذ الأولي/المطلوب.

### اعتبارات الخصوصية/الأمان

- يمكن تقليل دقة الطوابع الزمنية أكثر (10 دقائق؟) ولكن سيتعين إضافة رقم الإصدار. قد يؤدي هذا إلى كسر multihoming، ما لم يكن لدينا تشفير يحافظ على الترتيب؟ ربما لا يمكننا الاستغناء عن الطوابع الزمنية تماماً.

- البديل: طابع زمني 3 بايت (epoch / 10 دقائق)، إصدار 1-بايت، انتهاء الصلاحية 2-بايت

- هل النوع صريح أم ضمني في البيانات / التوقيع؟ ثوابت "Domain" للتوقيع؟

### Notes

- يجب على الـ routers عدم نشر LS أكثر من مرة واحدة في الثانية.
  إذا فعلوا ذلك، يجب عليهم زيادة الطابع الزمني المنشور بشكل اصطناعي بمقدار 1
  عن الـ LS المنشور سابقاً.

- يمكن لتنفيذات الـ router تخزين المفاتيح المؤقتة والتوقيع في الذاكرة المؤقتة لتجنب التحقق في كل مرة. على وجه الخصوص، يمكن أن تستفيد الـ floodfills والـ routers في كلا طرفي الاتصالات طويلة المدى من هذا.

- المفاتيح غير المتصلة والتوقيع مناسبان فقط للوجهات طويلة المدى،
  أي الخوادم وليس العملاء.

## New DatabaseEntry types

### تنسيق

التغييرات من LeaseSet الموجود:

- إضافة الطابع الزمني للنشر، الطابع الزمني لانتهاء الصلاحية، العلامات، والخصائص
- إضافة نوع التشفير
- إزالة مفتاح الإلغاء

البحث باستخدام

    Standard LS flag (1)
متجر مع

    Standard LS2 type (3)
احفظ في

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
انتهاء الصلاحية النموذجي

    10 minutes, as in a regular LS.
نُشر بواسطة

    Destination

### التبرير

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
### المشاكل

- الخصائص: التوسع المستقبلي والمرونة.
  يتم وضعها أولاً في حالة الحاجة إليها لتحليل البيانات المتبقية.

- أزواج متعددة من نوع التشفير/المفتاح العام
  لتسهيل الانتقال إلى أنواع تشفير جديدة. الطريقة الأخرى للقيام بذلك
  هي نشر عدة leasesets، ربما باستخدام نفس الأنفاق،
  كما نفعل الآن لوجهات DSA و EdDSA.
  يمكن التعرف على نوع التشفير الواردة في النفق
  باستخدام آلية session tag الموجودة،
  و/أو فك التشفير التجريبي باستخدام كل مفتاح. أطوال الرسائل الواردة
  قد توفر أيضاً دليلاً.

### ملاحظات

تستمر هذه المقترحة في استخدام المفتاح العام في الـ leaseset لمفتاح التشفير من النهاية إلى النهاية، وتترك حقل المفتاح العام في الـ Destination غير مستخدم، كما هو الحال الآن. نوع التشفير غير محدد في شهادة مفتاح الـ Destination، وسيبقى 0.

البديل المرفوض هو تحديد نوع التشفير في شهادة مفتاح الوجهة، واستخدام المفتاح العام في الوجهة، وعدم استخدام المفتاح العام في leaseSet. لا نخطط للقيام بذلك.

فوائد LS2:

- موقع المفتاح العام الفعلي لا يتغير.
- نوع التشفير، أو المفتاح العام، قد يتغير دون تغيير الوجهة.
- يزيل حقل الإلغاء غير المستخدم
- توافق أساسي مع أنواع DatabaseEntry الأخرى في هذا الاقتراح
- يسمح بأنواع تشفير متعددة

عيوب LS2:

- موقع المفتاح العام ونوع التشفير يختلف عن RouterInfo
- يحتفظ بمفتاح عام غير مستخدم في leaseset
- يتطلب تطبيقاً عبر الشبكة؛ كبديل، يمكن استخدام أنواع التشفير التجريبية،
  إذا سمحت بذلك floodfills
  (لكن انظر الاقتراحات ذات الصلة 136 و 137 حول دعم أنواع sig التجريبية).
  الاقتراح البديل قد يكون أسهل للتطبيق والاختبار لأنواع التشفير التجريبية.

### New Encryption Issues

بعض هذا خارج نطاق هذا الاقتراح، لكن نضع الملاحظات هنا الآن حيث لا يوجد لدينا اقتراح تشفير منفصل بعد. انظر أيضاً اقتراحات ECIES 144 و 145.

- يمثل نوع التشفير المزيج
  من المنحنى وطول المفتاح ونظام التشفير من طرف إلى طرف،
  بما في ذلك KDF و MAC، إن وجد.

- لقد قمنا بتضمين حقل طول المفتاح، بحيث يكون LS2 قابلاً للتحليل والتحقق بواسطة floodfill حتى لأنواع التشفير غير المعروفة.

- نوع التشفير الجديد الأول المقترح سيكون على الأرجح
  ECIES/X25519. كيفية استخدامه من النهاية إلى النهاية
  (إما نسخة معدلة قليلاً من ElGamal/AES+SessionTag
  أو شيء جديد تماماً، مثل ChaCha/Poly) سيتم تحديده
  في اقتراح واحد أو أكثر منفصل.
  انظر أيضاً اقتراحي ECIES رقم 144 و145.

### LeaseSet 2

- انتهاء الصلاحية 8-byte في leases تم تغييره إلى 4 bytes.

- إذا قمنا بتنفيذ الإلغاء في أي وقت، يمكننا القيام بذلك باستخدام حقل انتهاء صلاحية بقيمة صفر،
  أو صفر leases، أو كليهما. لا حاجة لمفتاح إلغاء منفصل.

- مفاتيح التشفير مرتبة حسب تفضيل الخادم، الأكثر تفضيلاً أولاً.
  السلوك الافتراضي للعميل هو اختيار المفتاح الأول الذي يحتوي على
  نوع تشفير مدعوم. قد تستخدم العملاء خوارزميات اختيار أخرى
  بناءً على دعم التشفير والأداء النسبي وعوامل أخرى.

### تنسيق

الأهداف:

- إضافة التعمية (blinding)
- السماح بأنواع متعددة من التوقيعات
- عدم الحاجة إلى أي عمليات تشفير أساسية جديدة
- تشفير اختياري لكل مستقبل، قابل للإلغاء
- دعم تشفير Standard LS2 و Meta LS2 فقط

الـ LS2 المشفر لا يتم إرساله أبداً في رسالة garlic من نقطة إلى أخرى. استخدم الـ LS2 القياسي كما هو موضح أعلاه.

التغييرات من LeaseSet المشفر الموجود:

- تشفير كامل الرسالة للأمان
- التشفير الآمن، وليس باستخدام AES فقط.
- التشفير لكل مستقبِل

البحث باستخدام

    Standard LS flag (1)
احفظ مع

    Encrypted LS2 type (5)
احفظ في

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
انتهاء الصلاحية المعتاد

    10 minutes, as in a regular LS, or hours, as in a meta LS.
نُشر بواسطة

    Destination


### المبرر

نحدد الوظائف التالية المقابلة للكتل البنائية التشفيرية المستخدمة لـ LS2 المشفرة:

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

STREAM

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


SIG

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

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### المناقشة

يتكون تنسيق LS2 المشفر من ثلاث طبقات متداخلة:

- طبقة خارجية تحتوي على المعلومات النصية العادية اللازمة للتخزين والاسترجاع.
- طبقة وسطى تتعامل مع مصادقة العميل.
- طبقة داخلية تحتوي على بيانات LS2 الفعلية.

التنسيق الإجمالي يبدو كما يلي::

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

ملاحظة أن LS2 المشفر مخفي. الوجهة ليست في الرأس. موقع تخزين DHT هو SHA-256(نوع التوقيع || المفتاح العام المخفي)، ويتم تدويره يومياً.

لا يستخدم رأس LS2 القياسي المحدد أعلاه.

#### Layer 0 (outer)

النوع

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

نوع توقيع المفتاح العام المُعمى

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

مفتاح عام مُعمّى

    Length as implied by sig type

الطابع الزمني للنشر

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

ينتهي في

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

الأعلام

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

بيانات المفاتيح المؤقتة

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

lenOuterCiphertext

    2 bytes, big endian

outerCiphertext

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

التوقيع

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Layer 1 (middle)

الأعلام

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

بيانات مصادقة عميل DH

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

بيانات مصادقة عميل PSK

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


innerCiphertext

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Layer 2 (inner)

النوع

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

البيانات

    LeaseSet2 data for the given type.

    Includes the header and signature.


### مشاكل التشفير الجديدة

نستخدم المخطط التالي لإخفاء المفاتيح، بناءً على Ed25519 و[ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf). توقيعات Re25519 تتم عبر منحنى Ed25519، باستخدام SHA-512 للهاش.

نحن لا نستخدم [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3)، والذي له أهداف تصميم مماثلة، لأن المفاتيح العامة المعماة الخاصة به قد تكون خارج المجموعة الفرعية ذات الترتيب الأولي، مما يحمل آثارًا أمنية غير معروفة.

#### Goals

- مفتاح التوقيع العام في الوجهة غير المُعمّاة يجب أن يكون
  Ed25519 (نوع التوقيع 7) أو Red25519 (نوع التوقيع 11)؛
  لا يتم دعم أنواع توقيعات أخرى
- إذا كان مفتاح التوقيع العام غير متصل، فإن مفتاح التوقيع العام المؤقت يجب أن يكون Ed25519 أيضاً
- التعمية حاسوبياً بسيطة
- استخدام العمليات التشفيرية الموجودة
- المفاتيح العامة المُعمّاة لا يمكن إلغاء تعميتها
- المفاتيح العامة المُعمّاة يجب أن تكون على منحنى Ed25519 والمجموعة الفرعية ذات الترتيب الأولي
- يجب معرفة مفتاح التوقيع العام للوجهة
  (الوجهة الكاملة غير مطلوبة) لاشتقاق المفتاح العام المُعمّى
- اختيارياً توفير سر إضافي مطلوب لاشتقاق المفتاح العام المُعمّى

#### Security

أمان مخطط التعمية (blinding scheme) يتطلب أن يكون توزيع alpha نفس توزيع المفاتيح الخاصة غير المعماة. ومع ذلك، عندما نقوم بتعمية مفتاح Ed25519 خاص (sig type 7) إلى مفتاح Red25519 خاص (sig type 11)، يكون التوزيع مختلفاً. لتلبية متطلبات [zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)، يجب استخدام Red25519 (sig type 11) للمفاتيح غير المعماة أيضاً، بحيث "لا يكشف الجمع بين مفتاح عام معاد العشوائية والتوقيع(ات) تحت ذلك المفتاح عن المفتاح الذي تمت إعادة عشوائيته منه." نحن نسمح بالنوع 7 للوجهات الموجودة، لكننا نوصي بالنوع 11 للوجهات الجديدة التي ستكون مشفرة.

#### Definitions

ب

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

L

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

DERIVE_PUBLIC(a)

    Convert a private key to public, as in Ed25519 (mulitply by G)

alpha

    A 32-byte random number known to those who know the destination.

GENERATE_ALPHA(destination, date, secret)

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

a

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

أ

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

أ'

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

A'

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

LEOS2IP(x)

    Flip the order of the input bytes to little-endian

H*(x)

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Blinding Calculations

يجب إنشاء secret alpha وblinded keys جديدة كل يوم (UTC). يتم حساب الـ secret alpha والـ blinded keys كما يلي.

GENERATE_ALPHA(destination, date, secret)، لجميع الأطراف:

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
BLIND_PRIVKEY()، لمالك النشر الخاص بـ leaseset:

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
BLIND_PUBKEY()، للعملاء الذين يسترجعون الـ leaseset:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
كلا الطريقتين لحساب A' تعطيان نفس النتيجة، كما هو مطلوب.

#### Signing

يتم توقيع الـ leaseset غير المُعمّى بواسطة المفتاح الخاص للتوقيع Ed25519 أو Red25519 غير المُعمّى ويتم التحقق منه باستخدام المفتاح العام للتوقيع Ed25519 أو Red25519 غير المُعمّى (أنواع التوقيع 7 أو 11) كالمعتاد.

إذا كان المفتاح العام للتوقيع غير متصل، يتم توقيع الـ leaseset غير المخفي بواسطة المفتاح الخاص المؤقت للتوقيع Ed25519 أو Red25519 غير المخفي والتحقق منه باستخدام المفتاح العام المؤقت للتوقيع Ed25519 أو Red25519 غير المخفي (أنواع التوقيع 7 أو 11) كالمعتاد. انظر أدناه للحصول على ملاحظات إضافية حول المفاتيح غير المتصلة للـ leaseset المشفرة.

لتوقيع مجموعة الإيجار المشفرة (encrypted leaseset)، نستخدم Red25519، المبني على [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) للتوقيع والتحقق باستخدام مفاتيح معماة (blinded keys). توقيعات Red25519 تتم عبر منحنى Ed25519، باستخدام SHA-512 للتشفير التجميعي (hash).

Red25519 مطابق تماماً لمعيار Ed25519 باستثناء ما هو محدد أدناه.

#### Sign/Verify Calculations

يستخدم الجزء الخارجي من leaseset المشفر مفاتيح وتوقيعات Red25519.

Red25519 مطابق تقريباً لـ Ed25519. هناك اختلافان:

مفاتيح Red25519 الخاصة يتم توليدها من أرقام عشوائية ثم يجب تقليلها mod L، حيث L معرّف أعلاه. مفاتيح Ed25519 الخاصة يتم توليدها من أرقام عشوائية ثم يتم "تثبيتها" باستخدام القناع البتي للبايتات 0 و 31. هذا لا يتم فعله لـ Red25519. الدالتان `GENERATE_ALPHA()` و `BLIND_PRIVKEY()` المعرّفتان أعلاه تولّدان مفاتيح Red25519 خاصة صحيحة باستخدام mod L.

في Red25519، حساب r للتوقيع يستخدم بيانات عشوائية إضافية، ويستخدم قيمة المفتاح العام بدلاً من hash المفتاح الخاص. بسبب البيانات العشوائية، كل توقيع Red25519 مختلف، حتى عند توقيع نفس البيانات بنفس المفتاح.

التوقيع:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
التحقق:

```text
// same as in Ed25519
```
### ملاحظات

#### Derivation of subcredentials

كجزء من عملية الإخفاء، نحتاج للتأكد من أن LS2 المشفر يمكن فك تشفيره فقط من قبل شخص يعرف مفتاح التوقيع العام المقابل لـ Destination. لا يتطلب الأمر Destination كاملاً. لتحقيق هذا، نشتق credential من مفتاح التوقيع العام:

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
سلسلة التخصيص تضمن أن الاعتماد لا يتصادم مع أي hash مستخدم كمفتاح بحث DHT، مثل hash الوجهة العادي.

بالنسبة لمفتاح أعمى معين، يمكننا حينها اشتقاق subcredential:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
يتم تضمين الـ subcredential في عمليات اشتقاق المفاتيح أدناه، مما يربط تلك المفاتيح بمعرفة مفتاح التوقيع العام الخاص بالـ Destination.

#### Layer 1 encryption

أولاً، يتم إعداد المدخل لعملية اشتقاق المفتاح:

```text
outerInput = subcredential || publishedTimestamp
```
بعد ذلك، يتم إنشاء salt عشوائي:

```text
outerSalt = CSRNG(32)
```
ثم يتم اشتقاق المفتاح المستخدم لتشفير الطبقة 1:

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
أخيراً، يتم تشفير وتسلسل النص الخام للطبقة 1:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Layer 1 decryption

يتم تحليل الملح (salt) من النص المشفر للطبقة الأولى:

```text
outerSalt = outerCiphertext[0:31]
```
ثم يتم اشتقاق المفتاح المستخدم لتشفير الطبقة 1:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
أخيراً، يتم فك تشفير النص المشفر للطبقة 1:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Layer 2 encryption

عندما يتم تفعيل تفويض العميل، يتم حساب ``authCookie`` كما هو موضح أدناه. عندما يتم تعطيل تفويض العميل، فإن ``authCookie`` هو مصفوفة البايت بطول صفر.

يتم التشفير بطريقة مشابهة للطبقة 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Layer 2 decryption

عندما يتم تمكين تفويض العميل، يتم حساب ``authCookie`` كما هو موضح أدناه. عندما يتم تعطيل تفويض العميل، فإن ``authCookie`` هو مصفوفة البايتات ذات الطول الصفري.

فك التشفير يتم بطريقة مشابهة للطبقة 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### LS2 مشفرة

عندما يتم تمكين تخويل العميل لوجهة معينة، يحتفظ الخادم بقائمة من العملاء المخولين لفك تشفير بيانات LS2 المشفرة. تعتمد البيانات المخزنة لكل عميل على آلية التخويل، وتتضمن شكلاً من أشكال المواد المفتاحية التي ينشئها كل عميل ويرسلها إلى الخادم عبر آلية آمنة خارج النطاق.

هناك بديلان لتنفيذ التصريح لكل عميل:

#### DH client authorization

كل عميل ينشئ زوج مفاتيح DH ``[csk_i, cpk_i]``، ويرسل المفتاح العام ``cpk_i`` إلى الخادم.

معالجة الخادم
^^^^^^^^^^^^^^^^^

ينشئ الخادم ``authCookie`` جديد وزوج مفاتيح DH مؤقت:

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
ثم لكل عميل مُخوَّل، يقوم الخادم بتشفير ``authCookie`` إلى مفتاحه العام:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
يضع الخادم كل مجموعة ``[clientID_i, clientCookie_i]`` في الطبقة 1 من ال LS2 المشفر، بالإضافة إلى ``epk``.

معالجة العميل
^^^^^^^^^^^^^^^^^

يستخدم العميل مفتاحه الخاص لاشتقاق معرف العميل المتوقع ``clientID_i`` ومفتاح التشفير ``clientKey_i`` ومتجه التهيئة للتشفير ``clientIV_i``:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
ثم يبحث العميل في بيانات التفويض للطبقة 1 عن إدخال يحتوي على ``clientID_i``. إذا وُجد إدخال مطابق، يقوم العميل بفك تشفيره للحصول على ``authCookie``:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Pre-shared key client authorization

كل عميل ينشئ مفتاحًا سريًا بحجم 32 بايت ``psk_i``، ويرسله إلى الخادم. بدلاً من ذلك، يمكن للخادم أن ينشئ المفتاح السري، ويرسله إلى عميل واحد أو أكثر.

معالجة الخادم
^^^^^^^^^^^^^^^^^

يولد الخادم ``authCookie`` وملح جديدين:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
ثم لكل عميل مُصرح له، يقوم الخادم بتشفير ``authCookie`` باستخدام مفتاحه المُشارك مسبقاً:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
يضع الخادم كل tuple من ``[clientID_i, clientCookie_i]`` في الطبقة 1 من LS2 المشفر، مع ``authSalt``.

معالجة العميل
^^^^^^^^^^^^^^^^^

يستخدم العميل مفتاحه المشترك مسبقاً لاشتقاق معرف العميل المتوقع ``clientID_i`` ومفتاح التشفير ``clientKey_i`` ومتجه التهيئة للتشفير ``clientIV_i``:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
ثم يبحث العميل في بيانات التفويض للطبقة الأولى عن إدخال يحتوي على ``clientID_i``. إذا كان هناك إدخال مطابق، يقوم العميل بفك تشفيره للحصول على ``authCookie``:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Security considerations

كلا آليتي تفويض العميل المذكورتين أعلاه توفران الخصوصية لعضوية العميل. الكيان الذي يعرف فقط الـ Destination يمكنه رؤية عدد العملاء المشتركين في أي وقت، لكن لا يمكنه تتبع العملاء الذين يتم إضافتهم أو إلغاؤهم.

يجب على الخوادم أن تقوم بعشوائية ترتيب العملاء في كل مرة تقوم فيها بإنشاء LS2 مشفر، لمنع العملاء من معرفة موقعهم في القائمة واستنتاج متى تمت إضافة أو إلغاء عملاء آخرين.

قد يختار الخادم إخفاء عدد العملاء المشتركين من خلال إدراج إدخالات عشوائية في قائمة بيانات التفويض.

مزايا تفويض العميل DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- أمان المخطط لا يعتمد بشكل كامل على التبادل خارج النطاق لمواد مفتاح العميل. المفتاح الخاص للعميل لا يحتاج أبداً لمغادرة جهازه، وبالتالي فإن المهاجم الذي يستطيع اعتراض التبادل خارج النطاق، ولكن لا يستطيع كسر خوارزمية DH، لا يمكنه فك تشفير LS2 المشفر، أو تحديد المدة التي يُمنح فيها العميل الوصول.

عيوب تفويض العميل DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- يتطلب N + 1 من عمليات DH على جانب الخادم لـ N من العملاء.
- يتطلب عملية DH واحدة على جانب العميل.
- يتطلب من العميل توليد المفتاح السري.

مزايا تخويل العميل PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- لا يتطلب عمليات DH.
- يسمح للخادم بتوليد المفتاح السري.
- يسمح للخادم بمشاركة نفس المفتاح مع عدة عملاء، إذا رغب في ذلك.

عيوب تخويل العميل PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- أمان المخطط يعتمد بشكل حرج على التبادل خارج النطاق لمواد مفتاح العميل. خصم يعترض التبادل لعميل معين يمكنه فك تشفير أي LS2 مشفر لاحق مخول لذلك العميل، بالإضافة إلى تحديد متى يتم إلغاء وصول العميل.

### تعريفات

راجع الاقتراح 149.

لا يمكنك استخدام LS2 مشفر للـ bittorrent، بسبب الردود المضغوطة للإعلان التي تبلغ 32 بايت. الـ 32 بايت تحتوي فقط على الـ hash. لا توجد مساحة لإشارة تدل على أن الـ leaseset مشفر، أو أنواع التوقيع.

### تنسيق

بالنسبة لـ leaseSets المشفرة مع المفاتيح غير المتصلة، يجب أيضاً إنشاء المفاتيح الخاصة المُعماة (blinded private keys) في وضع عدم الاتصال، مفتاح واحد لكل يوم.

نظرًا لأن كتلة التوقيع الاختيارية غير المتصلة بالإنترنت موجودة في الجزء النصي الواضح من leaseset المشفر، يمكن لأي شخص يقوم بكشط floodfills استخدام هذا لتتبع leaseset (لكن ليس فك تشفيره) على مدار عدة أيام. لمنع هذا، يجب على مالك المفاتيح أيضًا إنشاء مفاتيح عابرة جديدة لكل يوم. يمكن إنشاء كل من المفاتيح العابرة والمفاتيح المعماة مسبقًا، وتسليمها إلى router في دفعة واحدة.

لا يوجد تنسيق ملف محدد في هذا الاقتراح لتجميع مفاتيح متعددة مؤقتة ومُعمّاة وتوفيرها للعميل أو router. لا يوجد تحسين محدد لبروتوكول I2CP في هذا الاقتراح لدعم leasesets المشفرة مع المفاتيح غير المتصلة.

### Notes

- خدمة تستخدم leasesets مشفرة ستنشر النسخة المشفرة إلى floodfills. ومع ذلك، من أجل الكفاءة، ستقوم بإرسال leasesets غير مشفرة إلى العملاء في رسالة garlic المُغلفة، بمجرد التوثق (عبر القائمة البيضاء، على سبيل المثال).

- قد تقوم عقد Floodfill بتحديد الحد الأقصى للحجم إلى قيمة معقولة لمنع إساءة الاستخدام.

- بعد فك التشفير، يجب إجراء عدة فحوصات، بما في ذلك التأكد من أن
  الطابع الزمني الداخلي وتاريخ انتهاء الصلاحية يتطابقان مع تلك الموجودة في المستوى الأعلى.

- تم اختيار ChaCha20 بدلاً من AES. بينما تكون السرعات متشابهة إذا كان دعم الأجهزة لـ AES متاحاً، فإن ChaCha20 أسرع بـ 2.5-3 مرات عندما لا يكون دعم الأجهزة لـ AES متاحاً، كما هو الحال في أجهزة ARM منخفضة الأداء.

- نحن لا نهتم بالسرعة بما يكفي لاستخدام keyed BLAKE2b. لديه حجم إخراج كبير بما يكفي لاستيعاب أكبر n نحتاجه (أو يمكننا استدعاؤه مرة واحدة لكل مفتاح مرغوب مع معامل عداد). BLAKE2b أسرع بكثير من SHA-256، و keyed-BLAKE2b سيقلل من العدد الإجمالي لاستدعاءات دالة التشفير.
  ومع ذلك، انظر الاقتراح 148، حيث يُقترح أن ننتقل إلى BLAKE2b لأسباب أخرى.
  انظر [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Meta LS2

يُستخدم هذا لاستبدال multihoming. مثل أي leaseset، يتم توقيع هذا من قبل المُنشئ. هذه قائمة مُصادق عليها من hashes الوجهة.

الـ Meta LS2 هو قمة، وربما العقد الوسطية، لهيكل شجري. يحتوي على عدد من الإدخالات، كل منها يشير إلى LS أو LS2 أو Meta LS2 آخر لدعم التعدد الضخم للشبكات المنزلية. قد يحتوي الـ Meta LS2 على مزيج من إدخالات LS وLS2 وMeta LS2. أوراق الشجرة هي دائماً LS أو LS2. الشجرة عبارة عن DAG؛ الحلقات محظورة؛ يجب على العملاء الذين يقومون بعمليات البحث اكتشاف ورفض اتباع الحلقات.

قد يكون لـ Meta LS2 انتهاء صلاحية أطول بكثير من LS أو LS2 العادي. قد يكون للمستوى العلوي انتهاء صلاحية بعد عدة ساعات من تاريخ النشر. سيتم فرض الحد الأقصى لوقت انتهاء الصلاحية بواسطة floodfills والعملاء، وهو قيد التحديد.

حالة الاستخدام لـ Meta LS2 هي التعدد الضخم للاتصال المنزلي (massive multihoming)، ولكن بدون حماية إضافية لربط أجهزة router بـ leasesets (في وقت إعادة تشغيل router) أكثر مما هو متوفر حالياً مع LS أو LS2. هذا مكافئ لحالة استخدام "facebook"، والتي على الأرجح لا تحتاج لحماية الربط. حالة الاستخدام هذه تحتاج على الأرجح لمفاتيح غير متصلة (offline keys)، والتي يتم توفيرها في الرأسية القياسية (standard header) في كل عقدة من عقد الشجرة.

البروتوكول الخلفي للتنسيق بين routers الأوراق، والموقعين الوسطيين وموقعي Meta LS الرئيسيين غير محدد هنا. المتطلبات بسيطة للغاية - فقط التحقق من أن النظير متصل، ونشر LS جديد كل بضع ساعات. التعقيد الوحيد هو في اختيار ناشرين جدد لـ Meta LSes على المستوى الأعلى أو المستوى الوسطي عند الفشل.

مجموعات الإيجار المختلطة حيث يتم دمج الإيجارات من عدة routers وتوقيعها ونشرها في leaseset واحد موثقة في الاقتراح 140، "multihoming غير مرئي". هذا الاقتراح غير قابل للتطبيق كما هو مكتوب، لأن اتصالات streaming لن تكون "ثابتة" على router واحد، انظر http://zzz.i2p/topics/2335 .

البروتوكول الخلفي، والتفاعل مع العناصر الداخلية للـ router والعميل، سيكون معقداً جداً للـ invisible multihoming.

لتجنب إرهاق floodfill للمستوى العلوي Meta LS، يجب أن تكون مدة انتهاء الصلاحية عدة ساعات على الأقل. يجب على العملاء تخزين Meta LS للمستوى العلوي مؤقتاً، والاحتفاظ به عبر عمليات إعادة التشغيل إذا لم تنته صلاحيته.

نحتاج إلى تعريف خوارزمية للعملاء لاجتياز الشجرة، بما في ذلك البدائل الاحتياطية، بحيث يكون الاستخدام موزعًا. دالة تعتمد على مسافة التجمع، والتكلفة، والعشوائية. إذا كان لدى عقدة كل من LS أو LS2 و Meta LS، فنحتاج إلى معرفة متى يُسمح باستخدام تلك الـ leasesets، ومتى نواصل اجتياز الشجرة.

البحث باستخدام

    Standard LS flag (1)
تخزين مع

    Meta LS2 type (7)
احفظ في

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
انتهاء الصلاحية النموذجي

    Hours. Max 18.2 hours (65535 seconds)
نُشر بواسطة

    "master" Destination or coordinator, or intermediate coordinators

### Format

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
الأعلام والخصائص: للاستخدام المستقبلي

### اشتقاق مفتاح الإخفاء

- خدمة موزعة تستخدم هذا النهج ستحتوي على "سيد" واحد أو أكثر يمتلك المفتاح الخاص لوجهة الخدمة. سيقومون (خارج النطاق) بتحديد القائمة الحالية للوجهات النشطة وسينشرون Meta LS2. لضمان التكرار، يمكن لعدة أسياد استخدام multihome (أي النشر المتزامن) لـ Meta LS2.

- يمكن لخدمة موزعة أن تبدأ بوجهة واحدة أو تستخدم multihoming بالطريقة القديمة، ثم تنتقل إلى Meta LS2. يمكن لعملية البحث القياسية LS أن ترجع أي واحد من LS أو LS2 أو Meta LS2.

- عندما تستخدم خدمة Meta LS2، فإنها لا تحتوي على أنفاق (leases).

### Service Record

هذا سجل فردي يشير إلى أن وجهة معينة تشارك في خدمة. يتم إرساله من المشارك إلى الـ floodfill. لا يتم إرساله بشكل منفرد من قبل الـ floodfill أبداً، بل فقط كجزء من قائمة الخدمات. يُستخدم سجل الخدمة أيضاً لإلغاء المشاركة في خدمة، وذلك بتعيين انتهاء الصلاحية إلى الصفر.

هذا ليس LS2 ولكنه يستخدم ترويسة LS2 المعيارية وتنسيق التوقيع.

البحث باستخدام

    n/a, see Service List
تخزين مع

    Service Record type (9)
احفظ في

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
انتهاء الصلاحية النموذجي

    Hours. Max 18.2 hours (65535 seconds)
نُشر بواسطة

    Destination

### Format

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Notes

- إذا كانت قيمة expires تساوي أصفارًا فقط، يجب على الـ floodfill إلغاء السجل وعدم تضمينه في قائمة الخدمات.

- التخزين: قد يقوم الـ floodfill بتقييد تخزين هذه السجلات بصرامة وتحديد عدد السجلات المخزنة لكل hash وانتهاء صلاحيتها. كما يمكن استخدام قائمة بيضاء من الـ hashes.

- أي نوع آخر من netdb في نفس الـ hash له أولوية، لذلك سجل الخدمة لا يمكنه أبداً
  الكتابة فوق LS/RI، لكن LS/RI سوف يكتب فوق جميع سجلات الخدمة في ذلك الـ hash.

### Service List

هذا لا يشبه LS2 على الإطلاق ويستخدم تنسيقاً مختلفاً.

يتم إنشاء قائمة الخدمات وتوقيعها بواسطة floodfill. وهي غير مصادق عليها بمعنى أن أي شخص يمكنه الانضمام إلى خدمة عن طريق نشر Service Record إلى floodfill.

قائمة الخدمات تحتوي على سجلات خدمات مختصرة، وليس سجلات خدمات كاملة. هذه تحتوي على توقيعات ولكن فقط hashes، وليس destinations كاملة، لذلك لا يمكن التحقق منها بدون الـ destination الكامل.

الأمان، إن وُجد، ومرغوبية قوائم الخدمات لا تزال قيد التحديد. يمكن لعقد floodfill أن تحد من النشر، والاستعلامات، إلى قائمة بيضاء من الخدمات، لكن تلك القائمة البيضاء قد تختلف بناءً على التنفيذ، أو تفضيل المشغل. قد لا يكون من الممكن تحقيق إجماع على قائمة بيضاء أساسية مشتركة عبر التنفيذات المختلفة.

إذا كان اسم الخدمة مُدرجاً في سجل الخدمة أعلاه، فقد يعترض مشغلو floodfill؛ وإذا كان الـ hash فقط مُدرجاً، فلا يوجد تحقق، ويمكن لسجل الخدمة أن "يدخل" قبل أي نوع آخر من netDb ويتم تخزينه في floodfill.

البحث باستخدام

    Service List lookup type (11)
تخزين مع

    Service List type (11)
احفظ في

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
انتهاء الصلاحية النموذجي

    Hours, not specified in the list itself, up to local policy
نُشر بواسطة

    Nobody, never sent to floodfill, never flooded.

### Format

لا تستخدم ترويسة LS2 المعيارية المحددة أعلاه.

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
للتحقق من توقيع قائمة الخدمة:

- إضافة هاش اسم الخدمة في المقدمة
- إزالة هاش المنشئ
- التحقق من توقيع المحتويات المعدلة

للتحقق من توقيع كل Short Service Record:

- جلب الوجهة
- التحقق من التوقيع لـ (الطابع الزمني المنشور + انتهاء الصلاحية + العلامات + المنفذ + Hash لاسم الخدمة)

للتحقق من توقيع كل سجل إلغاء (Revocation Record):

- جلب الوجهة
- التحقق من توقيع (الطابع الزمني المنشور + 4 بايتات صفرية + العلامات + المنفذ + Hash
  لاسم الخدمة)

### Notes

- نحن نستخدم طول التوقيع بدلاً من نوع التوقيع حتى نتمكن من دعم أنواع التوقيع غير المعروفة.

- لا يوجد انتهاء صلاحية لقائمة الخدمة، يمكن للمستقبلين اتخاذ قرارهم الخاص بناءً على السياسة أو انتهاء صلاحية السجلات الفردية.

- قوائم الخدمات لا يتم إغراقها، فقط سجلات الخدمة الفردية يتم إغراقها. كل floodfill ينشئ ويوقع ويخزن مؤقتاً قائمة خدمات. يستخدم الـ floodfill سياسته الخاصة لوقت التخزين المؤقت والعدد الأقصى لسجلات الخدمة والإلغاء.

## Common Structures Spec Changes Required

### التشفير والمعالجة

خارج نطاق هذا الاقتراح. أضف إلى مقترحات ECIES 144 و 145.

### New Intermediate Structures

أضف هياكل جديدة لـ Lease2 و MetaLease و LeaseSet2Header و OfflineSignature. فعال اعتباراً من الإصدار 0.9.38.

### New NetDB Types

أضف هياكل لكل نوع جديد من leaseSet، مدمجة من أعلاه. بالنسبة لـ LeaseSet2 وEncryptedLeaseSet وMetaLeaseSet، سارية اعتباراً من الإصدار 0.9.38. بالنسبة لـ Service Record وService List، أولية وغير مجدولة.

### New Signature Type

أضف RedDSA_SHA512_Ed25519 النوع 11. المفتاح العام 32 بايت؛ المفتاح الخاص 32 بايت؛ الهاش 64 بايت؛ التوقيع 64 بايت.

## Encryption Spec Changes Required

خارج نطاق هذا الاقتراح. راجع الاقتراحات 144 و 145.

## I2NP Changes Required

أضف ملاحظة: لا يمكن نشر LS2 إلا إلى floodfills بحد أدنى من الإصدار.

### Database Lookup Message

أضف نوع البحث في قائمة الخدمات.

### Changes

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### ترخيص لكل عميل

أضف جميع أنواع المتاجر الجديدة.

### Changes

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
## I2CP Changes Required

### I2CP Options

الخيارات الجديدة المُفسرة من جانب الـ router، المُرسلة في SessionConfig Mapping:

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
الخيارات الجديدة المُفسَّرة من جانب العميل:

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
### Session Config

لاحظ أنه للتوقيعات غير المتصلة، الخيارات i2cp.leaseSetOfflineExpiration و i2cp.leaseSetTransientPublicKey و i2cp.leaseSetOfflineSignature مطلوبة، والتوقيع يتم بواسطة المفتاح الخاص للتوقيع المؤقت.

### عناوين LS مشفرة مع Base 32

الموجه إلى العميل. لا توجد تغييرات. يتم إرسال الـ leases مع طوابع زمنية بحجم 8 بايت، حتى لو كان الـ leaseset المُرجع سيكون LS2 بطوابع زمنية بحجم 4 بايت. لاحظ أن الاستجابة قد تكون رسالة Create Leaseset أو Create Leaseset2 Message.

### مجموعة الإيجار المشفرة (Encrypted LS) مع المفاتيح غير المتصلة

من الـ router إلى العميل. لا توجد تغييرات. يتم إرسال الـ leases مع طوابع زمنية بحجم 8 بايت، حتى لو كان الـ leaseset المُعاد سيكون LS2 مع طوابع زمنية بحجم 4 بايت. لاحظ أن الاستجابة قد تكون رسالة Create Leaseset أو Create Leaseset2.

### ملاحظات

العميل إلى الموجه. رسالة جديدة، لاستخدامها بدلاً من رسالة Create Leaseset.

### Meta LS2

- لكي يتمكن الـ router من تحليل نوع المتجر، يجب أن يكون النوع موجوداً في الرسالة،
  إلا إذا تم تمريره إلى الـ router مسبقاً في إعدادات الجلسة.
  لتبسيط كود التحليل المشترك، من الأسهل وجوده في الرسالة نفسها.

- لكي يعرف الراوتر نوع وطول المفتاح الخاص،
  يجب أن يكون بعد الـ lease set، إلا إذا كان المحلل يعرف النوع مسبقاً
  في إعداد الجلسة.
  بالنسبة لكود التحليل الشائع، من الأسهل معرفة ذلك من الرسالة نفسها.

- مفتاح التوقيع الخاص، المُعرَّف مسبقاً للإلغاء وغير المستخدم،
  غير موجود في LS2.

### التنسيق

نوع الرسالة لرسالة Create Leaseset2 هو 41.

### ملاحظات

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
### سجل الخدمة

- الحد الأدنى لإصدار router هو 0.9.39.
- الإصدار الأولي مع نوع الرسالة 40 كان في 0.9.38 لكن تم تغيير التنسيق.
  النوع 40 مهجور وغير مدعوم.

### تنسيق

- هناك حاجة لمزيد من التغييرات لدعم LS المشفر والوصفي.

### ملاحظات

من العميل إلى الموجه. رسالة جديدة.

### قائمة الخدمات

- يحتاج الـ router إلى معرفة ما إذا كان الوجهة مُعمى.
  إذا كان مُعمى ويستخدم مصادقة سرية أو لكل عميل،
  فإنه يحتاج إلى الحصول على تلك المعلومات أيضاً.

- البحث عن المضيف (Host Lookup) لعنوان b32 بتنسيق جديد ("b33")
  يخبر الموجه (router) أن العنوان مخفي، لكن لا توجد آلية لتمرير
  المفتاح السري أو المفتاح الخاص إلى الموجه في رسالة البحث عن المضيف.
  بينما يمكننا توسيع رسالة البحث عن المضيف لإضافة تلك المعلومات،
  من الأنظف تعريف رسالة جديدة.

- نحتاج إلى طريقة برمجية للعميل لإخبار الـ router.
  وإلا، سيتوجب على المستخدم تكوين كل وجهة يدوياً.

### تنسيق

قبل أن يرسل العميل رسالة إلى وجهة مُعماة، يجب عليه إما البحث عن "b33" في رسالة البحث عن المضيف (Host Lookup message)، أو إرسال رسالة معلومات التعمية (Blinding Info message). إذا كانت الوجهة المُعماة تتطلب سرًا أو مصادقة خاصة بكل عميل، فيجب على العميل إرسال رسالة معلومات التعمية (Blinding Info message).

الراوتر لا يرسل ردًا على هذه الرسالة.

### ملاحظات

نوع الرسالة لرسالة معلومات الإخفاء (Blinding Info Message) هو 42.

### Format

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
### شهادات المفاتيح

- الحد الأدنى لإصدار الـ router هو 0.9.43

### هياكل وسيطة جديدة

### أنواع NetDB الجديدة

لدعم البحث عن أسماء المضيفين "b33" وإرجاع إشارة في حالة عدم امتلاك الـ router للمعلومات المطلوبة، نحدد رموز نتائج إضافية لرسالة Host Reply Message، كما يلي:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
القيم من 1-255 معرّفة بالفعل كأخطاء، لذلك لا توجد مشكلة في التوافق مع الإصدارات السابقة.

### نوع التوقيع الجديد

جهاز التوجيه إلى العميل. رسالة جديدة.

### Justification

العميل لا يعرف مسبقاً أن Hash معين سيتم حله إلى Meta LS.

إذا أرجع البحث عن leaseset لوجهة معينة Meta LS، فإن الـ router سيقوم بالحل التكراري. بالنسبة للـ datagrams، لا يحتاج الجانب العميل إلى المعرفة؛ ومع ذلك، بالنسبة للـ streaming، حيث يتحقق البروتوكول من الوجهة في SYN ACK، يجب أن يعرف ما هي الوجهة "الحقيقية". لذلك، نحتاج إلى رسالة جديدة.

### Usage

يحتفظ الـ router بذاكرة تخزين مؤقت للوجهة الفعلية المستخدمة من meta LS. عندما يرسل العميل رسالة إلى وجهة تُحل إلى meta LS، يتحقق الـ router من ذاكرة التخزين المؤقت للوجهة الفعلية المستخدمة مؤخراً. إذا كانت ذاكرة التخزين المؤقت فارغة، يختار الـ router وجهة من الـ meta LS، ويبحث عن الـ leaseset. إذا نجح البحث عن الـ leaseset، يضيف الـ router تلك الوجهة إلى ذاكرة التخزين المؤقت، ويرسل للعميل رسالة Meta Redirect Message. هذا يتم مرة واحدة فقط، إلا إذا انتهت صلاحية الوجهة ويجب تغييرها. يجب على العميل أيضاً تخزين المعلومات مؤقتاً إذا لزم الأمر. رسالة Meta Redirect Message لا يتم إرسالها رداً على كل SendMessage.

يرسل الموجه هذه الرسالة فقط للعملاء الذين يستخدمون الإصدار 0.9.47 أو أحدث.

العميل لا يرسل رداً على هذه الرسالة.

### رسالة البحث في قاعدة البيانات

نوع الرسالة لرسالة Meta Redirect Message هو 43.

### التغييرات

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
### رسالة تخزين قاعدة البيانات

كيفية إنشاء ودعم Meta، بما في ذلك التواصل والتنسيق بين أجهزة router، خارج نطاق هذا الاقتراح. راجع الاقتراح ذي الصلة 150.

### التغييرات

التوقيعات غير المتصلة (offline signatures) لا يمكن التحقق منها في streaming أو repliable datagrams. انظر الأقسام أدناه.

## Private Key File Changes Required

ملف المفتاح الخاص (eepPriv.dat) ليس جزءاً رسمياً من مواصفاتنا ولكنه موثق في [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) والتطبيقات الأخرى تدعمه. هذا يُمكّن من نقل المفاتيح الخاصة إلى تطبيقات مختلفة.

يجب إجراء تغييرات لتخزين المفتاح العام المؤقت ومعلومات التوقيع غير المتصل.

### Changes

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
### خيارات I2CP

أضف الدعم للخيارات التالية:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Streaming Changes Required

التوقيعات غير المتصلة لا يمكن التحقق منها حالياً في streaming. التغيير أدناه يضيف كتلة التوقيع غير المتصل إلى الخيارات. هذا يتجنب الحاجة لاسترداد هذه المعلومات عبر I2CP.

### إعداد الجلسة

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
### رسالة طلب Leaseset

- البديل هو إضافة علم فقط، واسترداد المفتاح العام المؤقت عبر I2CP
  (انظر أقسام البحث عن المضيف / رسالة رد المضيف أعلاه)

## عنوان LS2 القياسي

التوقيعات غير المتصلة لا يمكن التحقق منها في معالجة الرسائل القابلة للرد. تحتاج إلى علامة للإشارة إلى التوقيع غير المتصل ولكن لا يوجد مكان لوضع العلامة. سيتطلب رقم بروتوكول وتنسيق جديد تماماً.

### رسالة طلب LeaseSet متغير

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
### إنشاء رسالة Leaseset2

- البديل هو مجرد إضافة علامة، واسترجاع المفتاح العام المؤقت عبر I2CP
  (انظر أقسام رسالة البحث عن المضيف / رد المضيف أعلاه)
- أي خيارات أخرى يجب أن نضيفها الآن بعد أن أصبح لدينا بايتات العلامات؟

## SAM V3 Changes Required

يجب تحسين SAM لدعم التوقيعات غير المتصلة في DESTINATION base 64.

### التبرير

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
لاحظ أن التواقيع غير المتصلة مدعومة فقط لـ STREAM وَ RAW، وليس لـ DATAGRAM (حتى نقوم بتعريف بروتوكول DATAGRAM جديد).

لاحظ أن SESSION STATUS ستُرجع Signing Private Key من جميع الأصفار وبيانات Offline Signature تماماً كما تم توفيرها في SESSION CREATE.

لاحظ أنه لا يمكن استخدام DEST GENERATE و SESSION CREATE DESTINATION=TRANSIENT لإنشاء وجهة موقعة غير متصلة (offline signed destination).

### نوع الرسالة

ارفع الإصدار إلى 3.4، أم اتركه عند 3.1/3.2/3.3 حتى يمكن إضافته دون الحاجة لكل أشياء 3.2/3.3؟

التغييرات الأخرى لم يتم تحديدها بعد. راجع قسم رسالة رد المضيف I2CP أعلاه.

## BOB Changes Required

BOB سيحتاج إلى تحسينات لدعم التوقيعات غير المتصلة و/أو Meta LS. هذا أولوية منخفضة وربما لن يتم تحديده أو تنفيذه أبداً. SAM V3 هي الواجهة المفضلة.

## Publishing, Migration, Compatibility

LS2 (بخلاف LS2 المشفر) يتم نشره في نفس موقع DHT كما هو الحال مع LS1. لا توجد طريقة لنشر كل من LS1 و LS2، إلا إذا كان LS2 في موقع مختلف.

يتم نشر LS2 المشفر في hash المفتاح المقنع (blinded key) ونوعه وبياناته. يُستخدم هذا الـ hash بعد ذلك لتوليد "مفتاح التوجيه" اليومي، كما هو الحال في LS1.

LS2 ستستخدم فقط عندما تكون الميزات الجديدة مطلوبة (التشفير الجديد، LS المشفر، البيانات الوصفية، إلخ). يمكن نشر LS2 فقط إلى floodfills من إصدار محدد أو أعلى.

الخوادم التي تنشر LS2 ستعلم أن أي عملاء متصلين يدعمون LS2. يمكنها إرسال LS2 في garlic encryption.

العملاء سيرسلون LS2 في garlics فقط إذا كانوا يستخدمون التشفير الجديد. العملاء المشتركون سيستخدمون LS1 إلى أجل غير مسمى؟ TODO: كيف يمكن الحصول على عملاء مشتركين يدعمون كلاً من التشفير القديم والجديد؟

## Rollout

0.9.38 يحتوي على دعم floodfill لمعيار LS2، بما في ذلك المفاتيح غير المتصلة.

0.9.39 يحتوي على دعم I2CP لـ LS2 و Encrypted LS2، وتوقيع/التحقق من sig type 11، ودعم floodfill لـ Encrypted LS2 (أنواع التوقيع 7 و 11، بدون مفاتيح غير متصلة)، وتشفير/فك تشفير LS2 (بدون تفويض لكل عميل).

0.9.40 مجدول لأن يحتوي على دعم لتشفير/فك تشفير LS2 مع التخويل لكل عميل، ودعم floodfill و I2CP لـ Meta LS2، ودعم LS2 المشفر بمفاتيح غير متصلة، ودعم b32 لـ LS2 المشفر.

## أنواع DatabaseEntry الجديدة

التصميم المشفر لـ LS2 متأثر بشدة بـ [واصفات الخدمة المخفية v3 الخاصة بـ Tor](https://spec.torproject.org/rend-spec-v3)، والتي كانت لها أهداف تصميم مشابهة.
