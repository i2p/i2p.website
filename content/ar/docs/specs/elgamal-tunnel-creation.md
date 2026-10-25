---
title: "مواصفات إنشاء الـ tunnel (ElGamal)"
description: "مواصفات بناء الأنفاق القديمة المبنية على ElGamal، تم استبدالها بـ X25519"
slug: "elgamal-tunnel-creation"
aliases:
  - "/ar/tunnel-alt-creation"
  - "/ar/tunnel-alt-creation/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## نظرة عامة {#tunnelcreate-overview}

ملاحظة: مهجور - هذه هي مواصفات بناء tunnel الخاصة بـ ElGamal. راجع [مواصفات بناء tunnel X25519](/docs/specs/tunnel-creation-ecies) للطريقة الحالية.

تحدد هذه الوثيقة تفاصيل رسائل بناء tunnel المشفرة المستخدمة لإنشاء tunnels باستخدام طريقة "التلسكوب غير التفاعلي". راجع وثيقة بناء tunnel [TUNNEL-IMPL](/docs/specs/tunnel-implementation) للحصول على نظرة عامة على العملية، بما في ذلك طرق اختيار وترتيب الأقران.

يتم إنجاز إنشاء tunnel من خلال رسالة واحدة يتم تمريرها عبر مسار النظراء في tunnel، تُعاد كتابتها في المكان نفسه، وتُرسل مرة أخرى إلى منشئ tunnel. تتكون رسالة tunnel الواحدة هذه من عدد متغير من السجلات (حتى 8) - سجل واحد لكل نظير محتمل في tunnel. يتم تشفير السجلات الفردية بشكل غير متماثل (ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal)) لتكون قابلة للقراءة فقط من قِبل نظير محدد على طول المسار، بينما يُضاف طبقة إضافية من التشفير المتماثل (AES [CRYPTO-AES](/docs/specs/cryptography#AES)) في كل نقطة انتقال لكشف السجل المُشفر بشكل غير متماثل فقط في الوقت المناسب.

### عدد السجلات {#number}

ليس من الضروري أن تحتوي جميع السجلات على بيانات صالحة. رسالة البناء لـ tunnel من 3 قفزات، على سبيل المثال، قد تحتوي على سجلات أكثر لإخفاء الطول الفعلي للـ tunnel عن المشاركين. هناك نوعان من رسائل البناء. رسالة Tunnel Build Message الأصلية ([TBM](/docs/specs/i2np#msg-tunnelbuild)) تحتوي على 8 سجلات، وهو أكثر من كافٍ لأي طول عملي للـ tunnel. رسالة Variable Tunnel Build Message الأحدث ([VTBM](/docs/specs/i2np#msg-variabletunnelbuild)) تحتوي على 1 إلى 8 سجلات. يمكن للمنشئ الموازنة بين حجم الرسالة والمقدار المرغوب من إخفاء طول الـ tunnel.

في الشبكة الحالية، معظم الأنفاق يبلغ طولها 2 أو 3 قفزات. التنفيذ الحالي يستخدم VTBM من 5 سجلات لبناء أنفاق بطول 4 قفزات أو أقل، و TBM من 8 سجلات للأنفاق الأطول. إن VTBM من 5 سجلات (والذي، عند تجزئته، يتسع في ثلاث رسائل tunnel بحجم 1KB) يقلل من حركة المرور في الشبكة ويزيد من معدل نجاح البناء، لأن الرسائل الأصغر أقل عرضة للإسقاط.

يجب أن تكون رسالة الرد من نفس النوع والطول مثل رسالة البناء.

### مواصفات سجل الطلب {#tunnelcreate-requestrecord}

محدد أيضًا في مواصفات I2NP [BRR](/docs/specs/i2np#struct-buildrequestrecord).

النص الواضح للسجل، مرئي فقط للقفزة المطلوبة:

```
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
تُستخدم حقول معرف tunnel التالي وهاش هوية router التالي لتحديد القفزة التالية في tunnel، على الرغم من أنه بالنسبة لنقطة نهاية tunnel الصادر، فإنها تحدد المكان الذي يجب إرسال رسالة رد إنشاء tunnel المعاد كتابتها إليه. بالإضافة إلى ذلك، يحدد معرف الرسالة التالي معرف الرسالة الذي يجب أن تستخدمه الرسالة (أو الرد).

مفتاح طبقة النفق، ومفتاح IV للنفق، ومفتاح الرد، و IV الرد هي قيم عشوائية مكونة من 32 بايت لكل منها يتم إنشاؤها بواسطة المنشئ، للاستخدام في سجل طلب البناء هذا فقط.

يحتوي حقل الإشارات على ما يلي:

```
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
البت 7 يشير إلى أن القفزة ستكون بوابة داخلية (IBGW). البت 6 يشير إلى أن القفزة ستكون نقطة نهاية خارجية (OBEP). إذا لم يتم تعيين أي من البتين، ستكون القفزة مشاركًا وسطيًا. لا يمكن تعيين كليهما في نفس الوقت.

#### إنشاء سجل الطلب

كل قفزة تحصل على معرف tunnel عشوائي، غير صفري. يتم ملء معرفات الـ tunnel للقفزة الحالية والتالية. كل سجل يحصل على مفتاح IV عشوائي للـ tunnel، وIV للرد، ومفتاح الطبقة، ومفتاح الرد.

#### تشفير سجل الطلب {#encryption}

يتم تشفير هذا السجل النصي الواضح باستخدام ElGamal 2048 [CRYPTO-ELG](/docs/specs/cryptography#elgamal) بمفتاح التشفير العام الخاص بالقفزة وتنسيقه في سجل بحجم 528 بايت:

```
bytes   0-15: First 16 bytes of the SHA-256 of the current hop's router identity
bytes 16-527: ElGamal-2048 encrypted request record
```
في السجل المشفر بحجم 512 بايت، تحتوي بيانات ElGamal على البايتات 1-256 و 258-513 من كتلة ElGamal المشفرة بحجم 514 بايت [CRYPTO-ELG](/docs/specs/cryptography#elgamal). يتم إزالة بايتَي الحشو من الكتلة (البايتات الصفرية في المواقع 0 و 257).

نظراً لأن النص الواضح يستخدم الحقل كاملاً، فلا حاجة لحشو إضافي بعد `SHA256(cleartext) + cleartext`.

يتم بعد ذلك تشفير كل سجل بحجم 528 بايت بشكل تكراري (باستخدام فك تشفير AES، مع مفتاح الرد و IV الرد لكل hop) بحيث تكون هوية الـ router في النص الواضح فقط للـ hop المعني.

### معالجة القفزات والتشفير {#tunnelcreate-hopprocessing}

عندما يتلقى hop رسالة TunnelBuildMessage، يبحث خلال السجلات الموجودة بداخلها عن واحد يبدأ بـ identity hash الخاص به (مقطوع إلى 16 بايت). ثم يقوم بفك تشفير كتلة ElGamal من ذلك السجل ويسترد النص الواضح المحمي. في تلك النقطة، يتأكدون من أن طلب tunnel ليس مكررًا عن طريق إدخال مفتاح الرد AES-256 في مرشح Bloom. الطلبات المكررة أو غير الصالحة يتم إسقاطها. السجلات التي لا تحمل طابع الساعة الحالية، أو الساعة السابقة إذا كان بعد بداية الساعة بقليل، يجب إسقاطها. على سبيل المثال، خذ الساعة في الطابع الزمني، حوّلها إلى وقت كامل، ثم إذا كانت متأخرة أكثر من 65 دقيقة أو متقدمة 5 دقائق عن الوقت الحالي، فهي غير صالحة. مرشح Bloom يجب أن يكون له مدة لا تقل عن ساعة واحدة (بالإضافة إلى بضع دقائق، للسماح بانحراف الساعة)، بحيث أن السجلات المكررة في الساعة الحالية التي لا يتم رفضها بفحص الطابع الزمني للساعة في السجل، سيتم رفضها بواسطة المرشح.

بعد أن يقرروا ما إذا كانوا سيوافقون على المشاركة في tunnel أم لا، يقومون باستبدال السجل الذي احتوى على الطلب بكتلة رد مشفرة. جميع السجلات الأخرى مشفرة بـ AES-256 [CRYPTO-AES](/docs/specs/cryptography#AES) باستخدام مفتاح الرد و IV المرفقين. كل منها مشفر بشكل منفصل بـ AES/CBC باستخدام نفس مفتاح الرد و reply IV. وضع CBC لا يستمر (مترابط) عبر السجلات.

كل hop يعرف فقط استجابته الخاصة. إذا وافق، سيحافظ على النفق حتى انتهاء صلاحيته، حتى لو لم يتم استخدامه، لأنه لا يستطيع معرفة ما إذا كانت جميع الـ hops الأخرى قد وافقت.

#### مواصفات سجل الرد {#tunnelcreate-replyrecord}

بعد أن يقرأ الـ hop الحالي سجله، يستبدله بسجل رد يوضح ما إذا كان يوافق على المشاركة في الـ tunnel أم لا، وإذا كان لا يوافق، فإنه يصنف سبب رفضه. هذا مجرد قيمة من 1 بايت، حيث 0x0 تعني أنهم يوافقون على المشاركة في الـ tunnel، والقيم الأعلى تعني مستويات رفض أعلى.

أكواد الرفض التالية معرفة:

- TUNNEL_REJECT_PROBABALISTIC_REJECT = 10
- TUNNEL_REJECT_TRANSIENT_OVERLOAD = 20
- TUNNEL_REJECT_BANDWIDTH = 30
- TUNNEL_REJECT_CRIT = 50

لإخفاء الأسباب الأخرى، مثل إيقاف تشغيل الـ router، عن النظراء، يستخدم التطبيق الحالي TUNNEL_REJECT_BANDWIDTH لتقريباً جميع حالات الرفض.

يتم تشفير الرد باستخدام مفتاح جلسة AES المُرسل إليه في الكتلة المشفرة، مع إضافة حشو من 495 بايت من البيانات العشوائية للوصول إلى حجم السجل الكامل. يتم وضع الحشو قبل بايت الحالة:

```
AES-256-CBC(SHA-256(padding+status) + padding + status, key, IV)

bytes   0-31 : SHA-256 of bytes 32-527
bytes 32-526 : Random padding
byte 527     : Reply value
```
هذا موضح أيضاً في مواصفات I2NP [BRR](/docs/specs/i2np#struct-buildrequestrecord).

### إعداد رسالة بناء Tunnel {#tunnelcreate-requestpreparation}

عند بناء رسالة Tunnel Build Message جديدة، يجب أولاً بناء جميع سجلات Build Request Records وتشفيرها بشكل غير متماثل باستخدام ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal). ثم يتم فك تشفير كل سجل مسبقاً باستخدام مفاتيح الرد وقيم IV الخاصة بالقفزات السابقة في المسار، باستخدام AES [CRYPTO-AES](/docs/specs/cryptography#AES). يجب تشغيل فك التشفير هذا بترتيب عكسي بحيث تظهر البيانات المشفرة بشكل غير متماثل بوضوح في القفزة الصحيحة بعد أن يقوم سلفها بتشفيرها.

السجلات الزائدة غير المطلوبة للطلبات الفردية يتم ملؤها ببساطة ببيانات عشوائية من قبل المنشئ.

### تسليم رسالة بناء النفق {#tunnelcreate-requestdelivery}

بالنسبة للأنفاق الصادرة، يتم التسليم مباشرة من منشئ النفق إلى القفزة الأولى، مع تغليف TunnelBuildMessage كما لو أن المنشئ كان مجرد قفزة أخرى في النفق. بالنسبة للأنفاق الواردة، يتم التسليم من خلال نفق صادر موجود. النفق الصادر يكون عموماً من نفس المجموعة التي ينتمي إليها النفق الجديد قيد البناء. إذا لم يكن هناك نفق صادر متاح في تلك المجموعة، يتم استخدام نفق استكشافي صادر. عند بدء التشغيل، عندما لا يوجد نفق استكشافي صادر بعد، يتم استخدام نفق صادر وهمي بصفر قفزات.

### معالجة نقطة النهاية لرسالة بناء Tunnel {#tunnelcreate-endpointhandling}

لإنشاء tunnel صادر، عندما يصل الطلب إلى نقطة نهاية صادرة (كما هو محدد بواسطة علم 'السماح بالرسائل لأي شخص')، يتم معالجة الوصلة كالمعتاد، تشفير رد مكان السجل وتشفير جميع السجلات الأخرى، ولكن نظراً لعدم وجود 'وصلة تالية' لإعادة توجيه TunnelBuildMessage إليها، فإنها بدلاً من ذلك تضع سجلات الرد المشفرة في TunnelBuildReplyMessage ([TBRM](/docs/specs/i2np#msg-tunnelbuildreply)) أو VariableTunnelBuildReplyMessage ([VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply)) (يجب أن يتطابق نوع الرسالة وعدد السجلات مع تلك الموجودة في الطلب) وتسلمها إلى tunnel الرد المحدد ضمن سجل الطلب. ذلك tunnel الرد يعيد توجيه Tunnel Build Reply Message إلى منشئ tunnel، تماماً كما هو الحال مع أي رسالة أخرى [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation). ثم يقوم منشئ tunnel بمعالجتها، كما هو موضح أدناه.

يتم اختيار tunnel الرد من قبل المنشئ كما يلي: عادة ما يكون tunnel واردًا من نفس المجموعة التي ينتمي إليها tunnel الصادر الجديد الذي يتم إنشاؤه. إذا لم يكن هناك tunnel وارد متاح في تلك المجموعة، يتم استخدام tunnel استكشافي وارد. عند بدء التشغيل، عندما لا يوجد بعد tunnel استكشافي وارد، يتم استخدام tunnel وارد وهمي بـ 0 قفزة.

لإنشاء tunnel وارد، عندما يصل الطلب إلى النقطة النهائية الواردة (المعروفة أيضاً باسم منشئ tunnel)، لا توجد حاجة لإنشاء رسالة رد بناء tunnel صريحة، ويقوم router بمعالجة كل رد من الردود، كما هو موضح أدناه.

### معالجة رسالة رد بناء Tunnel {#tunnelcreate-replyprocessing}

لمعالجة سجلات الرد، يحتاج المنشئ ببساطة إلى فك تشفير AES لكل سجل بشكل فردي، باستخدام مفتاح الرد و IV لكل قفزة في tunnel بعد النظير (بترتيب عكسي). هذا يكشف عن الرد الذي يحدد ما إذا كانوا يوافقون على المشاركة في tunnel أو سبب رفضهم. إذا وافقوا جميعاً، يُعتبر tunnel مُنشأ ويمكن استخدامه فوراً، ولكن إذا رفض أي شخص، يتم التخلص من tunnel.

يتم تسجيل الموافقات والرفض في ملف تعريف كل peer [PEER-SELECTION](/docs/overview/peer-selection)، لاستخدامها في التقييمات المستقبلية لسعة tunnel الخاصة بالـ peer.

## التاريخ والملاحظات {#tunnelcreate-notes}

نشأت هذه الاستراتيجية خلال نقاش في القائمة البريدية لـ I2P بين مايكل روجرز وماثيو توسلاند (toad) وjrandom بخصوص هجوم predecessor. انظر [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html)، [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html). تم تقديمها في الإصدار 0.6.1.10 في 2006-02-16، والذي كان آخر مرة تم فيها إجراء تغيير غير متوافق مع الإصدارات السابقة في I2P.

ملاحظات:

- هذا التصميم لا يمنع اثنين من الأقران المعاديين داخل tunnel من وضع علامات على سجل أو أكثر من سجلات الطلب أو الرد لاكتشاف أنهم داخل نفس tunnel، ولكن القيام بذلك يمكن اكتشافه من قبل منشئ tunnel عند قراءة الرد، مما يؤدي إلى وسم tunnel كغير صالح.

- هذا التصميم لا يتضمن إثبات عمل على القسم المشفر بشكل غير متماثل، على الرغم من أن هوية hash البالغة 16 بايت يمكن تقليلها إلى النصف مع استبدال الجزء الأخير بدالة hashcash بتكلفة تصل إلى 2^64.

- هذا التصميم وحده لا يمنع نظيرين عدائيين داخل tunnel من استخدام معلومات التوقيت لتحديد ما إذا كانا في نفس tunnel. استخدام التسليم المجمع والمتزامن للطلبات يمكن أن يساعد (تجميع الطلبات وإرسالها في الدقيقة المتزامنة مع ntp). ومع ذلك، فإن القيام بذلك يتيح للنظراء 'وسم' الطلبات عن طريق تأخيرها واكتشاف التأخير لاحقاً في tunnel، على الرغم من أن ربما إسقاط الطلبات غير المسلمة في نافذة زمنية صغيرة قد يعمل (على الرغم من أن القيام بذلك سيتطلب درجة عالية من تزامن الساعة). بدلاً من ذلك، ربما يمكن للقفزات الفردية حقن تأخير عشوائي قبل إعادة توجيه الطلب؟

- هل توجد أي طرق غير مميتة لوسم الطلب؟

- يتم استخدام الطابع الزمني بدقة ساعة واحدة لمنع إعادة التشغيل. لم يتم فرض هذا القيد حتى الإصدار 0.9.16.

## العمل المستقبلي {#future}

- في التنفيذ الحالي، يترك المنشئ سجلاً واحداً فارغاً لنفسه. وبالتالي فإن رسالة تحتوي على n سجلات يمكنها فقط بناء tunnel من n-1 hops. يبدو أن هذا ضروري للـ inbound tunnels (حيث يمكن للقفزة قبل الأخيرة رؤية بادئة التجزئة للقفزة التالية)، ولكن ليس للـ outbound tunnels. هذا يحتاج إلى بحث والتحقق منه. إذا كان من الممكن استخدام السجل المتبقي دون المساس بإخفاء الهوية، فيجب علينا القيام بذلك.

- مزيد من التحليل للهجمات المحتملة للوسم والتوقيت المذكورة في الملاحظات أعلاه.

- استخدم VTBM فقط؛ لا تختر العقد القديمة التي لا تدعمه.

- سجل طلب البناء لا يحدد مدة حياة tunnel أو انتهاء صلاحيته؛
  كل hop ينهي صلاحية tunnel بعد 10 دقائق، وهو ثابت مبرمج
  على مستوى الشبكة. يمكننا استخدام bit في حقل العلامة وأخذ 4 (أو 8)
  بايتات من الحشو لتحديد مدة الحياة أو انتهاء الصلاحية. الطالب
  سيحدد هذا الخيار فقط إذا كان جميع المشاركين يدعمونه.

## المراجع {#ref}

- [BRR](/docs/specs/i2np#struct-buildrequestrecord) - Build Request Record
- [CRYPTO-AES](/docs/specs/cryptography#AES) - AES Encryption
- [CRYPTO-ELG](/docs/specs/cryptography#elgamal) - ElGamal Encryption
- [HASHING-IT-OUT](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) - Hashing It Out Paper
- [PEER-SELECTION](/docs/overview/peer-selection) - Peer Selection
- [PREDECESSOR](http://forensics.umass.edu/pubs/wright-tissec.pdf) - Predecessor Attack Paper
- [PREDECESSOR-2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf) - Predecessor Attack Paper (2008)
- [TBM](/docs/specs/i2np#msg-tunnelbuild) - Tunnel Build Message
- [TBRM](/docs/specs/i2np#msg-tunnelbuildreply) - Tunnel Build Reply Message
- [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html) - Tunnel Build Reasoning
- [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html) - Tunnel Build Summary
- [TUNNEL-IMPL](/docs/specs/tunnel-implementation) - Tunnel Implementation
- [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation) - Tunnel Operation
- [VTBM](/docs/specs/i2np#msg-variabletunnelbuild) - Variable Tunnel Build Message
- [VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply) - Variable Tunnel Build Reply Message
