---
title: "أنفاق ECIES"
aliases:
  - "/ar/proposals/152-ecies-config"
  - "/ar/proposals/152-ecies-config/"
  - "/ar/proposals/152"
  - "/ar/proposals/152/"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "مغلق"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
toc: true
---

## ملاحظة

نشر الشبكة والاختبار قيد التقدم. قابل للمراجعات الطفيفة. راجع [SPEC](/docs/specs/tunnel-implementation/) للمواصفات الرسمية.

## نظرة عامة

تقترح هذه الوثيقة تغييرات على تشفير رسائل Tunnel Build باستخدام العناصر التشفيرية الأساسية المقدمة بواسطة [ECIES-X25519](/docs/specs/ecies/). إنها جزء من الاقتراح الشامل [Proposal 156](/proposals/156-ecies-routers) لتحويل أجهزة router من مفاتيح ElGamal إلى مفاتيح ECIES-X25519.

لأغراض نقل الشبكة من ElGamal + AES256 إلى ECIES + ChaCha20، تُعتبر الأنفاق التي تحتوي على مزيج من موجهات ElGamal و ECIES ضرورية. يتم توفير مواصفات للتعامل مع القفزات المختلطة للأنفاق. لن يتم إجراء أي تغييرات على تنسيق أو معالجة أو تشفير قفزات ElGamal.

منشئو أنفاق ElGamal سيحتاجون إلى إنشاء أزواج مفاتيح X25519 مؤقتة لكل قفزة، واتباع هذه المواصفات لإنشاء الأنفاق التي تحتوي على قفزات ECIES.

يحدد هذا الاقتراح التغييرات المطلوبة لبناء الأنفاق ECIES-X25519. للاطلاع على نظرة عامة على جميع التغييرات المطلوبة لأجهزة router الخاصة بـ ECIES، راجع الاقتراح 156 [Proposal 156](/proposals/156-ecies-routers).

يحافظ هذا الاقتراح على نفس الحجم لسجلات بناء الأنفاق، كما هو مطلوب للتوافق. ستتم تنفيذ سجلات البناء والرسائل الأصغر لاحقاً - انظر [الاقتراح 157](/proposals/157-new-tbm).

### Cryptographic Primitives

لا يتم تقديم أي عناصر تشفيرية جديدة. العناصر التشفيرية المطلوبة لتنفيذ هذا الاقتراح هي:

- AES-256-CBC كما هو موضح في [التشفير](/docs/specs/cryptography/)
- دوال STREAM ChaCha20/Poly1305:
  ENCRYPT(k, n, plaintext, ad) و DECRYPT(k, n, ciphertext, ad) - كما هو موضح في [NTCP2](/docs/specs/ntcp2/) [ECIES-X25519](/docs/specs/ecies/) و [RFC-7539](https://tools.ietf.org/html/rfc7539)
- دوال X25519 DH - كما هو موضح في [NTCP2](/docs/specs/ntcp2/) و [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - كما هو موضح في [NTCP2](/docs/specs/ntcp2/) و [ECIES-X25519](/docs/specs/ecies/)

وظائف Noise الأخرى المُعرَّفة في مكان آخر:

- MixHash(d) - كما في [NTCP2](/docs/specs/ntcp2/) و [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - كما في [NTCP2](/docs/specs/ntcp2/) و [ECIES-X25519](/docs/specs/ecies/)

### Goals

- زيادة سرعة العمليات التشفيرية
- استبدال ElGamal + AES256/CBC بـ ECIES primitives لـ tunnel BuildRequestRecords و BuildReplyRecords
- عدم تغيير حجم BuildRequestRecords و BuildReplyRecords المشفرة (528 بايت) للتوافق
- لا توجد رسائل I2NP جديدة
- الحفاظ على حجم سجل البناء المشفر للتوافق
- إضافة السرية الأمامية لـ Tunnel Build Messages
- إضافة التشفير المصادق عليه
- كشف إعادة ترتيب hops لـ BuildRequestRecords
- زيادة دقة الطوابع الزمنية بحيث يمكن تقليل حجم مرشح Bloom
- إضافة حقل لانتهاء صلاحية النفق بحيث تصبح أعمار الأنفاق المتغيرة ممكنة (أنفاق ECIES الكاملة فقط)
- إضافة حقل خيارات قابل للتوسع للميزات المستقبلية
- إعادة استخدام العناصر التشفيرية الموجودة
- تحسين أمان رسائل بناء النفق حيثما أمكن مع الحفاظ على التوافق
- دعم الأنفاق مع peers مختلطة ElGamal/ECIES
- تحسين الدفاعات ضد هجمات "التوسيم" على رسائل البناء
- لا تحتاج hops لمعرفة نوع التشفير للـ hop التالي قبل معالجة رسالة البناء،
  حيث قد لا تملك RI الخاص بالـ hop التالي في ذلك الوقت
- زيادة التوافق مع الشبكة الحالية إلى أقصى حد
- عدم تغيير تشفير AES للطلب/الرد لبناء النفق لـ routers ElGamal
- عدم تغيير تشفير "الطبقة" AES للنفق، لذلك راجع [الاقتراح 153](/proposals/153-chacha20-layer-encryption)
- الاستمرار في دعم كل من TBM/TBRM بـ 8 سجلات و VTBM/VTBRM متغيرة الحجم
- عدم طلب ترقية "يوم العلم" للشبكة بالكامل

### البدائيات التشفيرية

- إعادة تصميم كاملة لرسائل بناء tunnel تتطلب "يوم علم".
- تقليص رسائل بناء tunnel (يتطلب جميع القفزات ECIES واقتراح جديد)
- استخدام خيارات بناء tunnel كما هو محدد في [الاقتراح 143](/proposals/143-build-message-options)، مطلوب فقط للرسائل الصغيرة
- Tunnels ثنائية الاتجاه - لذلك انظر [الاقتراح 119](/proposals/119-bidirectional-tunnels)
- رسائل بناء tunnel أصغر - لذلك انظر [الاقتراح 157](/proposals/157-new-tbm)

## Threat Model

### الأهداف

- لا يمكن لأي من القفزات تحديد منشئ النفق.

- العقد الوسطى يجب ألا تكون قادرة على تحديد اتجاه النفق أو موقعها في النفق.

- لا يمكن لأي من النقاط الوسطية قراءة محتويات سجلات الطلبات أو الردود الأخرى، باستثناء router hash المقطوع والمفتاح المؤقت للنقطة التالية

- لا يمكن لأي عضو في tunnel الرد للبناء الصادر قراءة أي سجلات رد.

- لا يمكن لأي عضو في النفق الصادر للبناء الداخل قراءة أي سجلات طلب،
  باستثناء أن OBEP يمكنه رؤية router hash المقطوع والمفتاح المؤقت لـ IBGW

### الأهداف غير المطلوبة

هدف رئيسي من تصميم بناء الأنفاق هو جعل الأمر أكثر صعوبة على الـ routers المتواطئة X و Y لمعرفة أنها في نفق واحد. إذا كان الـ router X في القفزة m والـ router Y في القفزة m+1، فسيعرفان ذلك بوضوح. لكن إذا كان الـ router X في القفزة m والـ router Y في القفزة m+n حيث n>1، فيجب أن يكون هذا أصعب بكثير.

هجمات الوسم هي حيث يقوم router الوسيط X بتعديل رسالة بناء tunnel بطريقة تجعل router Y قادراً على اكتشاف التعديل عندما تصل إليه رسالة البناء. الهدف هو أن أي رسالة معدلة يتم إسقاطها بواسطة router بين X و Y قبل أن تصل إلى router Y. بالنسبة للتعديلات التي لا يتم إسقاطها قبل router Y، يجب على منشئ tunnel اكتشاف التلف في الرد وتجاهل tunnel.

الهجمات المحتملة:

- تعديل سجل البناء
- استبدال سجل البناء
- إضافة أو إزالة سجل البناء
- إعادة ترتيب سجلات البناء

TODO: هل يمنع التصميم الحالي جميع هذه الهجمات؟

## Design

### Noise Protocol Framework

هذا الاقتراح يوفر المتطلبات المبنية على إطار عمل بروتوكول Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (المراجعة 34، 2018-07-11). في مصطلحات Noise، Alice هي المُبادِرة، وBob هو المُستجيب.

يعتمد هذا الاقتراح على بروتوكول Noise وهو Noise_N_25519_ChaChaPoly_SHA256. يستخدم بروتوكول Noise هذا العناصر الأولية التالية:

- One-Way Handshake Pattern: N
  أليس لا ترسل مفتاحها الثابت إلى بوب (N)

- DH Function: X25519
  X25519 DH بطول مفتاح 32 بايت كما هو محدد في [RFC-7748](https://tools.ietf.org/html/rfc7748).

- دالة التشفير: ChaChaPoly
  AEAD_CHACHA20_POLY1305 كما هو محدد في [RFC-7539](https://tools.ietf.org/html/rfc7539) القسم 2.8.
  nonce بحجم 12 بايت، مع تعيين أول 4 بايتات إلى الصفر.
  مطابق لذلك الموجود في [NTCP2](/docs/specs/ntcp2/).

- Hash Function: SHA256
  دالة تجزئة قياسية بحجم 32 بايت، مستخدمة بالفعل على نطاق واسع في I2P.

#### Additions to the Framework

لا شيء.

### أهداف التصميم

تستخدم عمليات المصافحة أنماط مصافحة [Noise](https://noiseprotocol.org/noise.html).

يتم استخدام تطابق الأحرف التالي:

- e = مفتاح مؤقت لاستخدام واحد
- s = مفتاح ثابت
- p = حمولة الرسالة

طلب البناء مطابق لنمط Noise N. وهذا مطابق أيضاً لأول رسالة (طلب الجلسة) في نمط XK المستخدم في [NTCP2](/docs/specs/ntcp2/).

```text
<- s
  ...
  e es p ->
```
### هجمات وضع العلامات

سجلات طلبات البناء يتم إنشاؤها بواسطة منشئ النفق ويتم تشفيرها بشكل غير متماثل للقفزة الفردية. هذا التشفير غير المتماثل لسجلات الطلبات هو حاليًا ElGamal كما هو محدد في [التشفير](/docs/specs/cryptography/) ويحتوي على مجموع اختبار SHA-256. هذا التصميم ليس سريًا للأمام.

التصميم الجديد سيستخدم نمط Noise أحادي الاتجاه "N" مع ECIES-X25519 ephemeral-static DH، مع HKDF، و ChaCha20/Poly1305 AEAD للسرية المستقبلية والتكامل والمصادقة. Alice هي طالبة بناء النفق. كل hop في النفق هو Bob.

(خصائص أمان الحمولة)

```text
N:                      Authentication   Confidentiality
    -> e, es                  0                2

    Authentication: None (0).
    This payload may have been sent by any party, including an active attacker.

    Confidentiality: 2.
    Encryption to a known recipient, forward secrecy for sender compromise
    only, vulnerable to replay.  This payload is encrypted based only on DHs
    involving the recipient's static key pair.  If the recipient's static
    private key is compromised, even at a later date, this payload can be
    decrypted.  This message can also be replayed, since there's no ephemeral
    contribution from the recipient.

    "e": Alice generates a new ephemeral key pair and stores it in the e
         variable, writes the ephemeral public key as cleartext into the
         message buffer, and hashes the public key along with the old h to
         derive a new h.

    "es": A DH is performed between the Alice's ephemeral key pair and the
          Bob's static key pair.  The result is hashed along with the old ck to
          derive a new ck and k, and n is set to zero.
```
### Reply encryption

سجلات الرد يتم إنشاؤها بواسطة منشئ hops ويتم تشفيرها بشكل متماثل للمنشئ. هذا التشفير المتماثل لسجلات الرد يستخدم حالياً AES مع checksum SHA-256 مُقدم مسبقاً. ويحتوي على checksum SHA-256. هذا التصميم لا يوفر السرية المستقبلية (forward-secret).

سيستخدم التصميم الجديد ChaCha20/Poly1305 AEAD للحفاظ على التكامل والمصادقة.

### إطار عمل بروتوكول Noise

المفتاح العام المؤقت في الطلب لا يحتاج إلى إخفاء بـ AES أو Elligator2. القفزة السابقة هي الوحيدة التي يمكنها رؤيته، وتلك القفزة تعلم أن القفزة التالية هي ECIES.

سجلات الرد لا تحتاج إلى تشفير غير متماثل كامل مع DH آخر.

## Specification

### Build Request Records

سجلات BuildRequestRecords المشفرة هي 528 بايت لكل من ElGamal و ECIES، من أجل التوافق.

#### Request Record Unencrypted (ElGamal)

للمرجعية، هذه هي المواصفة الحالية لـ tunnel BuildRequestRecord لـ routers ElGamal، مأخوذة من [I2NP](/docs/specs/i2np/). البيانات غير المشفرة مُقدمة ببايت غير صفري و SHA-256 hash للبيانات قبل التشفير، كما هو محدد في [Cryptography](/docs/specs/cryptography/).

جميع الحقول تستخدم الترتيب big-endian.

الحجم غير المشفر: 222 بايت

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes    4-35: local router identity hash
  bytes   36-39: next tunnel ID, nonzero
  bytes   40-71: next router identity hash
  bytes  72-103: AES-256 tunnel layer key
  bytes 104-135: AES-256 tunnel IV key
  bytes 136-167: AES-256 reply key
  bytes 168-183: AES-256 reply IV
  byte      184: flags
  bytes 185-188: request time (in hours since the epoch, rounded down)
  bytes 189-192: next message ID
  bytes 193-221: uninterpreted / random padding
```
#### Request Record Encrypted (ElGamal)

للمرجع، هذه هي المواصفة الحالية لـ tunnel BuildRequestRecord لأجهزة التوجيه ElGamal، مأخوذة من [I2NP](/docs/specs/i2np/).

الحجم المشفر: 528 بايت

```text
bytes    0-15: Hop's truncated identity hash
  bytes  16-528: ElGamal encrypted BuildRequestRecord
```
#### Request Record Unencrypted (ECIES)

هذه هي المواصفات المقترحة لـ tunnel BuildRequestRecord لأجهزة router من نوع ECIES-X25519. ملخص التغييرات:

- إزالة hash الموجه غير المستخدم بحجم 32 بايت
- تغيير وقت الطلب من ساعات إلى دقائق
- إضافة حقل انتهاء الصلاحية لوقت tunnel متغير مستقبلي
- إضافة مساحة أكبر للـ flags
- إضافة Mapping لخيارات بناء إضافية
- مفتاح الرد AES-256 والـ IV غير مستخدمين لسجل الرد الخاص بالـ hop نفسه
- السجل غير المشفر أطول لأن هناك عبء تشفير أقل

سجل الطلب لا يحتوي على أي مفاتيح رد ChaCha. هذه المفاتيح مشتقة من KDF. انظر أدناه.

جميع الحقول بترتيب البايت الكبير (big-endian).

الحجم غير المشفر: 464 بايت

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes     4-7: next tunnel ID, nonzero
  bytes    8-39: next router identity hash
  bytes   40-71: AES-256 tunnel layer key
  bytes  72-103: AES-256 tunnel IV key
  bytes 104-135: AES-256 reply key
  bytes 136-151: AES-256 reply IV
  byte      152: flags
  bytes 153-155: more flags, unused, set to 0 for compatibility
  bytes 156-159: request time (in minutes since the epoch, rounded down)
  bytes 160-163: request expiration (in seconds since creation)
  bytes 164-167: next message ID
  bytes   168-x: tunnel build options (Mapping)
  bytes     x-x: other data as implied by flags or options
  bytes   x-463: random padding
```
حقل الأعلام هو نفسه كما هو معرّف في [إنشاء الأنفاق](/docs/specs/tunnel-implementation/) ويحتوي على ما يلي::

```text
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
ترتيب البت: 76543210 (البت 7 هو MSB)  البت 7: إذا تم تعيينه، السماح بالرسائل من أي شخص  البت 6: إذا تم تعيينه، السماح بالرسائل إلى أي شخص، وإرسال الرد إلى

البتات 5-0: غير محددة، يجب تعيينها إلى 0 للتوافق مع الخيارات المستقبلية

البت 7 يشير إلى أن القفزة ستكون بوابة دخول (IBGW). البت 6 يشير إلى أن القفزة ستكون نقطة نهاية خروج (OBEP). إذا لم يتم تعيين أي من البتين، فإن القفزة ستكون مشاركًا وسيطًا. لا يمكن تعيين كليهما في نفس الوقت.

#### Request Record Encrypted (ECIES)

انتهاء صلاحية الطلب مخصص لمدة tunnel متغيرة مستقبلية. في الوقت الحالي، القيمة الوحيدة المدعومة هي 600 (10 دقائق).

خيارات بناء tunnel هي هيكل Mapping كما هو محدد في [الهياكل المشتركة](/docs/specs/common-structures/). هذا للاستخدام المستقبلي. لا توجد خيارات محددة حاليًا. إذا كان هيكل Mapping فارغًا، فهذا يعني بايتين 0x00 0x00. الحد الأقصى لحجم Mapping (بما في ذلك حقل الطول) هو 296 بايت، والقيمة القصوى لحقل طول Mapping هي 294.

```text
bytes    0-15: Hop's truncated identity hash
  bytes   16-47: Sender's ephemeral X25519 public key
  bytes  48-511: ChaCha20 encrypted BuildRequestRecord
  bytes 512-527: Poly1305 MAC
```
### أنماط المصافحة

جميع الحقول بترتيب البايت الكبير (big-endian) باستثناء المفتاح العام المؤقت (ephemeral public key) الذي يكون بترتيب البايت الصغير (little-endian).

#### Reply Record Unencrypted (ElGamal)

الحجم المشفر: 528 بايت

سجلات BuildReplyRecords المشفرة هي 528 بايت لكل من ElGamal و ECIES، من أجل التوافق.

ردود ElGamal مشفرة باستخدام AES.

```text
bytes   0-31: SHA-256 Hash of bytes 32-527
  bytes 32-526: random data
  byte     527: reply

  total length: 528
```
#### Reply Record Unencrypted (ECIES)

جميع الحقول بصيغة big-endian.

- إضافة تعيين لخيارات رد البناء
- السجل غير المشفر أطول لأن هناك عبء تشفير أقل

الحجم غير المُشفّر: 528 بايت

هذه هي المواصفة المقترحة لـ tunnel BuildReplyRecord لـ routers ECIES-X25519. ملخص التغييرات:

ردود ECIES مشفرة بـ ChaCha20/Poly1305.

```text
bytes    0-x: Tunnel Build Reply Options (Mapping)
  bytes    x-x: other data as implied by options
  bytes  x-510: Random padding
  byte     511: Reply byte
```
جميع الحقول بصيغة big-endian.

الحجم غير المشفر: 512 بايت

- 0x00 (قبول)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Reply Record Encrypted (ECIES)

خيارات رد بناء tunnel هي هيكل Mapping كما هو محدد في [الهياكل المشتركة](/docs/specs/common-structures/). هذا للاستخدام المستقبلي. لا توجد خيارات محددة حالياً. إذا كان هيكل Mapping فارغاً، فهذا يكون بايتين 0x00 0x00. الحد الأقصى لحجم Mapping (بما في ذلك حقل الطول) هو 511 بايت، والقيمة القصوى لحقل طول Mapping هي 509.

```text
bytes   0-511: ChaCha20 encrypted BuildReplyRecord
  bytes 512-527: Poly1305 MAC
```
بايت الرد هو إحدى القيم التالية كما هو محدد في [إنشاء الأنفاق](/docs/specs/tunnel-implementation/) لتجنب بصمة الهوية:

### تشفير الطلبات

الحجم المشفر: 528 بايت

بعد الانتقال الكامل إلى سجلات ECIES، تكون قواعد الحشو المحدود النطاق هي نفسها المستخدمة لسجلات الطلبات.

- "التشفير":

- cipher يعمل في وضع فك التشفير
- سجلات الطلبات يتم فك تشفيرها بشكل استباقي في المعالجة المسبقة (إخفاء سجلات الطلبات المشفرة)

- "decryption":

- تشغيل التشفير في وضع التشفير
- سجلات الطلبات مشفرة (تكشف سجل طلب النص العادي التالي) بواسطة قفزات المشاركين

- ChaCha20 ليس لديه "أوضاع"، لذلك يتم تشغيله ببساطة ثلاث مرات:

- مرة واحدة في المعالجة المسبقة
- مرة واحدة بواسطة الـ hop
- مرة واحدة في معالجة الرد النهائي

الأنفاق المختلطة مسموحة وضرورية للانتقال من ElGamal إلى ECIES. خلال الفترة الانتقالية، سيزداد عدد أجهزة router التي تستخدم مفاتيح ECIES.

المعالجة المسبقة للتشفير المتماثل ستعمل بنفس الطريقة:

عند استخدام الأنفاق المختلطة، سيحتاج منشئو الأنفاق إلى تأسيس التشفير المتماثل لـ BuildRequestRecord على نوع التشفير للقفزة الحالية والسابقة.

كل hop سيستخدم نوع التشفير الخاص به لتشفير BuildReplyRecords، والسجلات الأخرى في VariableTunnelBuildMessage (VTBM).

- المرسل (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

في مسار الرد، ستحتاج نقطة النهاية (المرسل) إلى إلغاء [التشفير المتعدد](https://en.wikipedia.org/wiki/Multiple_encryption)، باستخدام مفتاح الرد الخاص بكل قفزة.

كمثال توضيحي، دعونا ننظر إلى tunnel صادر مع ECIES محاط بـ ElGamal:

جميع سجلات BuildRequestRecords في حالتها المشفرة (باستخدام ElGamal أو ECIES).

يتم استخدام تشفير AES256/CBC، عند استخدامه، لكل سجل على حدة، دون ربط عبر سجلات متعددة.

- سجل H3 "مُشفر" باستخدام:

- مفتاح الرد الخاص بـ H2 (ChaCha20)
- مفتاح الرد الخاص بـ H1 (AES256/CBC)

- سجل H2 "مُشفر" باستخدام:

- مفتاح الرد للـ H1 (AES256/CBC)

- يتم إرسال سجل H1 بدون تشفير متماثل

وبالمثل، سيتم استخدام ChaCha20 لتشفير كل سجل، وليس بث مستمر عبر VTBM بأكمله.

يتم معالجة سجلات الطلبات مسبقاً بواسطة المرسل (OBGW):

- يتم "فك تشفير" سجل H3 باستخدام:

- مفتاح الرد الخاص بـ H3 (AES256/CBC)

- يتم "فك تشفير" سجل H2 باستخدام:

- مفتاح الرد الخاص بـ H3 (AES256/CBC)
- مفتاح الرد الخاص بـ H2 (ChaCha20-Poly1305)

- يتم "فك تشفير" سجل H1 باستخدام:

- مفتاح الرد الخاص بـ H3 (AES256/CBC)
- مفتاح الرد الخاص بـ H2 (ChaCha20)
- مفتاح الرد الخاص بـ H1 (AES256/CBC)

فقط H2 يفحص علامة تشفير الرد، ويرى أنها متبوعة بـ AES256/CBC.

- سجل H3 "مشفر" باستخدام:

- مفتاح الرد الخاص بـ H3 (AES256/CBC)

- سجل H2 "مشفر" باستخدام:

- مفتاح الرد الخاص بـ H3 (AES256/CBC)
- مفتاح الرد الخاص بـ H2 (ChaCha20-Poly1305)

- سجل H1 "مُشفر" باستخدام:

- مفتاح الرد الخاص بـ H3 (AES256/CBC)
- مفتاح الرد الخاص بـ H2 (ChaCha20)
- مفتاح الرد الخاص بـ H1 (AES256/CBC)

### تشفير الرد

بعد معالجتها من قبل كل hop، تكون السجلات في حالة "مفكوكة التشفير":

منشئ tunnel، المعروف أيضاً باسم Inbound Endpoint (IBEP)، يقوم بمعالجة الرد لاحقاً:

#### KDF for Initial ck and h

هذه المفاتيح مُضمنة صراحة في ElGamal BuildRequestRecords. بالنسبة لـ ECIES BuildRequestRecords، يتم تضمين مفاتيح tunnel ومفاتيح AES reply، لكن مفاتيح ChaCha reply مُشتقة من تبادل DH. راجع [الاقتراح 156](/proposals/156-ecies-routers) لتفاصيل مفاتيح router الثابتة ECIES.

```text
This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  // Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
  h = protocol_name || 0

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by all routers.
```
#### KDF for Request Record

فيما يلي وصف لكيفية اشتقاق المفاتيح المرسلة مسبقاً في سجلات الطلبات.

هذا هو [NOISE](https://noiseprotocol.org/noise.html) قياسي للنمط "N" مع اسم بروتوكول قياسي.

منشئو أنفاق ElGamal يولدون زوج مفاتيح X25519 مؤقت لكل قفزة ECIES في النفق، ويستخدمون المخطط أعلاه لتشفير BuildRequestRecord الخاص بهم. سيستخدم منشئو أنفاق ElGamal المخطط السابق لهذه المواصفة للتشفير إلى قفزات ElGamal.

منشئو أنفاق ECIES سيحتاجون إلى التشفير لكل مفتاح عام لقفزة ElGamal باستخدام المخطط المحدد في [إنشاء الأنفاق](/docs/specs/tunnel-implementation/). سيستخدم منشئو أنفاق ECIES المخطط أعلاه للتشفير إلى قفزات ECIES.

هذا يعني أن قفزات tunnel ستشاهد فقط السجلات المشفرة من نفس نوع التشفير الخاص بها.

```text
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || below means append
  h = SHA256(h || hepk);

  // up until here, can all be precalculated by each router
  // for all incoming build requests

  // Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  // Sender performs an X25519 DH with Hop's static public key.
  // Each Hop, finds the record w/ their truncated identity hash,
  // and extracts the Sender's ephemeral key preceding the encrypted record.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Save for Reply Record KDF
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  plaintext = 464 byte build request record
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  End of "es" message pattern.

  // MixHash(ciphertext)
  // Save for Reply Record KDF
  h = SHA256(h || ciphertext)
```
بالنسبة لمُنشِئي tunnel من نوع ElGamal و ECIES، فسيقومون بإنتاج أزواج مفاتيح X25519 مؤقتة فريدة لكل hop لتشفير hops من نوع ECIES.

### المبرر

**مهم**: يجب أن تكون المفاتيح المؤقتة فريدة لكل hop في ECIES، ولكل سجل بناء. عدم استخدام مفاتيح فريدة يفتح ثغرة أمنية للـ hops المتواطئة لتأكيد أنها في نفس الـ tunnel.

### Reply Record Encryption (ECIES)

``replyKey`` و ``layerKey`` و ``layerIV`` يجب أن تُضمَّن أيضاً داخل سجلات ElGamal، ويمكن توليدها عشوائياً.

```text
// AEAD parameters
  k = chainkey from build request
  n = 0
  plaintext = 512 byte build reply record
  ad = h from build request

  ciphertext = ENCRYPT(k, n, plaintext, ad)
```
### سجلات طلب البناء

كما هو محدد في [إنشاء الأنفاق](/docs/specs/tunnel-implementation/). لا توجد تغييرات على التشفير لقفزات ElGamal.

### Security Analysis

سجل الرد مُشفر بـ ChaCha20/Poly1305.

كما هو محدد في [Tunnel Creation](/docs/specs/tunnel-implementation/). لا توجد تغييرات على التشفير لقفزات ElGamal.

ElGamal لا يوفر السرية الأمامية لرسائل بناء الأنفاق.

AES256/CBC في وضع أفضل قليلاً، حيث أنه معرض فقط لضعف نظري من هجوم `biclique` معروف النص الأصلي.

الهجوم العملي الوحيد المعروف ضد AES256/CBC هو هجوم padding oracle، عندما يكون الـ IV معروفاً للمهاجم.

المهاجم سيحتاج إلى كسر تشفير ElGamal للقفزة التالية للحصول على معلومات مفتاح AES256/CBC (مفتاح الرد و IV).

ElGamal يستهلك موارد المعالج بشكل أكبر بكثير من ECIES، مما يؤدي إلى استنزاف محتمل للموارد.

## نموذج التهديد

ECIES، المستخدم مع مفاتيح ephemeral جديدة لكل BuildRequestRecord أو VariableTunnelBuildMessage، يوفر forward-secrecy.

## Implementation Notes

* أجهزة التوجيه الأقدم لا تتحقق من نوع التشفير للقفزة وسترسل سجلات مشفرة بـ ElGamal. بعض أجهزة التوجيه الحديثة تحتوي على أخطاء وسترسل أنواع مختلفة من السجلات المشوهة. يجب على المطورين اكتشاف ورفض هذه السجلات قبل عملية DH إن أمكن، لتقليل استخدام المعالج.

## Issues

## التصميم

يوفر ChaCha20Poly1305 تشفير AEAD، مما يسمح للمستقبل بالتحقق من سلامة الرسالة قبل محاولة فك التشفير.

## المراجع

* [العام](/docs/specs/common-structures/)
* [التشفير](/docs/specs/cryptography/)
* [ECIES-X25519](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [NTCP2](/docs/specs/ntcp2/)
* [Prop119](/proposals/119-bidirectional-tunnels/)
* [Prop143](/proposals/143-build-message-options/)
* [Prop153](/proposals/153-chacha20-layer-encryption/)
* [Prop156](/proposals/156-ecies-routers/)
* [Prop157](/proposals/157-new-tbm/)
* [SPEC](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [إنشاء tunnel](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [التشفير المتعدد](https://en.wikipedia.org/wiki/Multiple_encryption)
* [RFC-7539](https://tools.ietf.org/html/rfc7539)
* [RFC-7748](https://tools.ietf.org/html/rfc7748)
