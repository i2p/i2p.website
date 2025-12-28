---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "مغلق"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## ملاحظة

نشر الشبكة والاختبار قيد التقدم. قابل لمراجعات طفيفة. انظر [المواصفات](/docs/specs/ecies/) للمواصفة الرسمية.

الميزات التالية غير مطبقة اعتبارًا من الإصدار 0.9.46:

- كتل MessageNumbers وOptions وTermination
- استجابات طبقة البروتوكول
- مفتاح ثابت صفري
- Multicast

## نظرة عامة

هذا اقتراح لأول نوع تشفير جديد من طرف إلى طرف منذ بداية I2P، لاستبدال ElGamal/AES+SessionTags [Elg-AES](/docs/legacy/elgamal-aes/).

يعتمد على العمل السابق كما يلي:

- مواصفات الهياكل المشتركة [Common Structures](/docs/specs/common-structures/)
- مواصفات [I2NP](/docs/specs/i2np/) بما في ذلك LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/legacy/elgamal-aes/)
- [http://zzz.i2p/topics/1768](http://zzz.i2p/topics/1768) نظرة عامة على التشفير غير المتماثل الجديد
- نظرة عامة على التشفير منخفض المستوى [CRYPTO-ELG](/docs/specs/cryptography/)
- ECIES [http://zzz.i2p/topics/2418](http://zzz.i2p/topics/2418)
- [NTCP2](/docs/specs/ntcp2/) [Proposal 111](/proposals/111-ntcp-2/)
- 123 إدخالات netDB جديدة
- 142 قالب التشفير الجديد
- بروتوكول [Noise](https://noiseprotocol.org/noise.html)
- خوارزمية double ratchet الخاصة بـ [Signal](https://signal.org/docs/)

الهدف هو دعم التشفير الجديد للتواصل من طرف إلى طرف، من destination إلى destination.

سيستخدم التصميم مصافحة Noise ومرحلة بيانات تتضمن double ratchet الخاص بـ Signal.

جميع المراجع إلى Signal و Noise في هذا الاقتراح هي لمعلومات أساسية فقط. المعرفة ببروتوكولات Signal و Noise غير مطلوبة لفهم أو تنفيذ هذا الاقتراح.

### Current ElGamal Uses

كمراجعة، يمكن العثور على مفاتيح ElGamal العامة بحجم 256 بايت في هياكل البيانات التالية. راجع مواصفات الهياكل المشتركة.

- في هوية الـ Router
  هذا هو مفتاح التشفير الخاص بالـ router.

- في Destination
  تم استخدام المفتاح العام للوجهة للتشفير القديم من i2cp إلى i2cp
  والذي تم تعطيله في الإصدار 0.6، وهو غير مستخدم حالياً باستثناء
  IV لتشفير LeaseSet، والذي أصبح مهجوراً.
  يتم استخدام المفتاح العام في LeaseSet بدلاً من ذلك.

- في LeaseSet
  هذا هو مفتاح التشفير الخاص بالوجهة.

- في LS2
  هذا هو مفتاح التشفير الخاص بالوجهة.

### EncTypes in Key Certs

كمراجعة، أضفنا دعم أنواع التشفير عندما أضفنا دعم أنواع التوقيع. حقل نوع التشفير يكون دائماً صفر، سواء في Destinations أو RouterIdentities. ما إذا كان سيتم تغيير ذلك في أي وقت لا يزال قيد التحديد (TBD). راجع مواصفات البنى المشتركة [Common Structures](/docs/specs/common-structures/).

### الاستخدامات الحالية لـ ElGamal

كمراجعة، نحن نستخدم ElGamal لـ:

1) رسائل بناء الـ Tunnel (المفتاح موجود في RouterIdentity)    الاستبدال غير مشمول في هذا الاقتراح.    انظر الاقتراح 152 [Proposal 152](/proposals/152-ecies-tunnels).

2) تشفير router-to-router لـ netdb ورسائل I2NP الأخرى (المفتاح في RouterIdentity)    يعتمد على هذا الاقتراح.    يتطلب اقتراحاً للنقطة 1) أيضاً، أو وضع المفتاح في خيارات RI.

3) Client End-to-end ElGamal+AES/SessionTag (المفتاح موجود في LeaseSet، مفتاح الوجهة غير مستخدم) الاستبدال مُغطى في هذا الاقتراح.

4) Ephemeral DH لـ NTCP1 و SSU    الاستبدال غير مغطى في هذا الاقتراح.    راجع الاقتراح 111 لـ NTCP2.    لا يوجد اقتراح حالي لـ SSU2.

### أنواع التشفير في شهادات المفاتيح

- متوافق مع الإصدارات السابقة
- يتطلب ويعتمد على LS2 (الاقتراح 123)
- الاستفادة من التشفير الجديد أو العناصر الأساسية المضافة لـ NTCP2 (الاقتراح 111)
- لا يتطلب تشفير جديد أو عناصر أساسية جديدة للدعم
- المحافظة على فصل التشفير والتوقيع؛ دعم جميع الإصدارات الحالية والمستقبلية
- تمكين التشفير الجديد للوجهات
- تمكين التشفير الجديد للـ routers، ولكن فقط لرسائل garlic - بناء النفق سيكون اقتراحاً منفصلاً
- عدم كسر أي شيء يعتمد على hashes الوجهة الثنائية 32-بايت، مثل bittorrent
- المحافظة على تسليم الرسائل 0-RTT باستخدام ephemeral-static DH
- عدم تطلب تخزين مؤقت / طابور للرسائل في طبقة البروتوكول هذه؛
  مواصلة دعم تسليم الرسائل غير المحدود في كلا الاتجاهين دون انتظار استجابة
- الترقية إلى ephemeral-ephemeral DH بعد 1 RTT
- المحافظة على معالجة الرسائل خارج التسلسل
- المحافظة على أمان 256-بت
- إضافة السرية الأمامية
- إضافة المصادقة (AEAD)
- أكثر كفاءة في المعالج بكثير من ElGamal
- عدم الاعتماد على Java jbigi لجعل DH فعال
- تقليل عمليات DH
- أكثر كفاءة في استخدام النطاق الترددي بكثير من ElGamal (كتلة ElGamal 514 بايت)
- دعم التشفير الجديد والقديم على نفس النفق إذا رغب في ذلك
- المتلقي قادر على التمييز بكفاءة بين التشفير الجديد والقديم القادم عبر
  نفس النفق
- الآخرون لا يستطيعون التمييز بين التشفير الجديد أو القديم أو المستقبلي
- إلغاء تصنيف طول الجلسة الجديد مقابل الموجود (دعم الحشو)
- لا تتطلب رسائل I2NP جديدة
- استبدال checksum SHA-256 في حمولة AES بـ AEAD
- دعم ربط جلسات الإرسال والاستقبال بحيث
  يمكن أن تحدث الإقرارات ضمن البروتوكول، بدلاً من خارج النطاق فقط.
  هذا سيسمح أيضاً للردود بالحصول على السرية الأمامية فوراً.
- تمكين التشفير من النهاية إلى النهاية لرسائل معينة (مخازن RouterInfo)
  التي لا نفعلها حالياً بسبب العبء على المعالج.
- عدم تغيير رسالة I2NP Garlic Message
  أو تنسيق تعليمات Garlic Message Delivery Instructions.
- إلغاء الحقول غير المستخدمة أو المتكررة في تنسيقات Garlic Clove Set و Clove.

القضاء على عدة مشاكل متعلقة بعلامات الجلسة، بما في ذلك:

- عدم القدرة على استخدام AES حتى الرد الأول
- عدم الموثوقية والتوقفات إذا افترض تسليم العلامات
- عدم كفاءة في استخدام النطاق الترددي، خاصة عند التسليم الأول
- عدم كفاءة كبيرة في المساحة لتخزين العلامات
- حمولة إضافية كبيرة في النطاق الترددي لتسليم العلامات
- معقد للغاية، صعب التنفيذ
- صعب الضبط لحالات الاستخدام المختلفة
  (التدفق مقابل datagrams، الخادم مقابل العميل، النطاق الترددي العالي مقابل المنخفض)
- نقاط ضعف استنزاف الذاكرة بسبب تسليم العلامات

### استخدامات التشفير غير المتماثل

- تغييرات تنسيق LS2 (اكتمل المقترح 123)
- خوارزمية تناوب DHT جديدة أو توليد عشوائي مشترك
- تشفير جديد لبناء tunnel.
  انظر المقترح 152 [Proposal 152](/proposals/152-ecies-tunnels).
- تشفير جديد لتشفير طبقة tunnel.
  انظر المقترح 153 [Proposal 153](/proposals/153-chacha20-layer-encryption).
- طرق التشفير والإرسال والاستقبال لرسائل I2NP DLM / DSM / DSRM.
  لا تتغير.
- لا يتم دعم الاتصال من LS1-إلى-LS2 أو ElGamal/AES-إلى-هذا-المقترح.
  هذا المقترح هو بروتوكول ثنائي الاتجاه.
  قد تتعامل الوجهات مع التوافق العكسي من خلال نشر leasesets اثنين
  باستخدام نفس tunnels، أو وضع كلا نوعي التشفير في LS2.
- تغييرات نموذج التهديد
- تفاصيل التنفيذ لا تُناقش هنا وتُترك لكل مشروع.
- (متفائل) إضافة امتدادات أو خطافات لدعم multicast

### الأهداف

لقد كان ElGamal/AES+SessionTag بروتوكولنا الوحيد من طرف إلى طرف لحوالي 15 عامًا، بشكل أساسي دون تعديلات على البروتوكول. توجد الآن بدائل تشفيرية أسرع. نحتاج إلى تعزيز أمان البروتوكول. لقد طورنا أيضًا استراتيجيات إرشادية وحلول بديلة لتقليل النفقات العامة للذاكرة وعرض النطاق الترددي للبروتوكول، لكن هذه الاستراتيجيات هشة وصعبة الضبط، وتجعل البروتوكول أكثر عرضة للكسر، مما يؤدي إلى انقطاع الجلسة.

خلال نفس الفترة الزمنية تقريباً، وصفت مواصفات ElGamal/AES+SessionTag والوثائق ذات الصلة مدى استهلاك session tags للعرض الترددي أثناء التسليم، واقترحت استبدال تسليم session tag بـ "synchronized PRNG". يولد synchronized PRNG بشكل حتمي نفس العلامات في كلا الطرفين، مشتقة من بذرة مشتركة. يمكن أيضاً تسمية synchronized PRNG بـ "ratchet". يحدد هذا الاقتراح (أخيراً) آلية ratchet تلك، ويلغي تسليم العلامات.

من خلال استخدام ratchet (مولد أرقام عشوائية كاذبة متزامن) لتوليد session tags، نتخلص من العبء الإضافي لإرسال session tags في رسالة New Session والرسائل اللاحقة عند الحاجة. بالنسبة لمجموعة tags نموذجية تحتوي على 32 tag، هذا يوفر 1KB. كما يلغي هذا تخزين session tags في الجانب المرسل، مما يقلل متطلبات التخزين إلى النصف.

مطلوب مصافحة كاملة ثنائية الاتجاه، مشابهة لنمط Noise IK، لتجنب هجمات انتحال هوية اختراق المفتاح (KCI). راجع جدول "خصائص أمان الحمولة" في Noise في [NOISE](https://noiseprotocol.org/noise.html). لمزيد من المعلومات حول KCI، راجع البحث https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf

### غير الأهداف / خارج النطاق

نموذج التهديد مختلف إلى حد ما عن NTCP2 (اقتراح 111). عقد MitM هي OBEP و IBGW ويُفترض أن لديها رؤية كاملة للـ NetDB العالمي الحالي أو التاريخي، من خلال التواطؤ مع floodfills.

الهدف هو منع هذه الهجمات من نوع MitM من تصنيف حركة البيانات كرسائل جلسة جديدة وموجودة، أو كتشفير جديد مقابل تشفير قديم.

## Detailed Proposal

يحدد هذا الاقتراح بروتوكولاً جديداً من طرف إلى طرف لاستبدال ElGamal/AES+SessionTags. سيستخدم التصميم مصافحة Noise ومرحلة البيانات التي تدمج الآلية المزدوجة لـ Signal.

### المبرر

هناك خمسة أجزاء من البروتوكول تحتاج إلى إعادة تصميم:

- 1) يتم استبدال تنسيقات حاوي الجلسة الجديدة والموجودة
  بتنسيقات جديدة.
- 2) يتم استبدال ElGamal (مفاتيح عامة 256 بايت، مفاتيح خاصة 128 بايت)
  بـ ECIES-X25519 (مفاتيح عامة وخاصة 32 بايت)
- 3) يتم استبدال AES بـ
  AEAD_ChaCha20_Poly1305 (مختصر كـ ChaChaPoly أدناه)
- 4) سيتم استبدال SessionTags بـ ratchets،
  والتي هي في الأساس مولد أرقام عشوائية متزامن ومشفر.
- 5) يتم استبدال حمولة AES، كما هو محدد في مواصفة ElGamal/AES+SessionTags،
  بتنسيق كتلة مشابه لذلك في NTCP2.

كل واحد من التغييرات الخمسة له قسم منفصل أدناه.

### نموذج التهديد

تطبيقات router الحالية في I2P ستتطلب تطبيقات للعناصر الأساسية التشفيرية المعيارية التالية، والتي غير مطلوبة لبروتوكولات I2P الحالية:

- ECIES (ولكن هذا في الأساس X25519)
- Elligator2

تتطلب تطبيقات router الموجودة في I2P التي لم تقم بعد بتطبيق [NTCP2](/docs/specs/ntcp2/) ([Proposal 111](/proposals/111-ntcp-2/)) أيضاً تطبيقات لـ:

- توليد مفاتيح X25519 و DH
- AEAD_ChaCha20_Poly1305 (مختصرة كـ ChaChaPoly أدناه)
- HKDF

### Crypto Type

نوع التشفير (المستخدم في LS2) هو 4. هذا يشير إلى مفتاح عام X25519 بحجم 32 بايت little-endian، والبروتوكول من طرف إلى طرف المحدد هنا.

نوع التشفير 0 هو ElGamal. أنواع التشفير 1-3 محجوزة لـ ECIES-ECDH-AES-SessionTag، انظر الاقتراح 145 [Proposal 145](/proposals/145-ecies).

### ملخص التصميم التشفيري

يقدم هذا الاقتراح المتطلبات المبنية على Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (المراجعة 34، 2018-07-11). يتمتع Noise بخصائص مشابهة لبروتوكول Station-To-Station [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol)، والذي يشكل الأساس لبروتوكول [SSU](/docs/legacy/ssu/). في مصطلحات Noise، Alice هي المبادِرة، وBob هو المستجيب.

هذا الاقتراح مبني على بروتوكول Noise وهو Noise_IK_25519_ChaChaPoly_SHA256. (المعرف الفعلي لدالة اشتقاق المفتاح الأولية هو "Noise_IKelg2_25519_ChaChaPoly_SHA256" للإشارة إلى امتدادات I2P - انظر قسم KDF 1 أدناه) يستخدم بروتوكول Noise هذا العناصر الأساسية التالية:

- نمط المصافحة التفاعلية: IK
  أليس ترسل مفتاحها الثابت إلى بوب فوراً (I)
  أليس تعرف مفتاح بوب الثابت مسبقاً (K)

- نمط المصافحة أحادية الاتجاه: N
  أليس لا ترسل مفتاحها الثابت إلى بوب (N)

- DH Function: X25519
  X25519 DH مع طول مفتاح 32 بايت كما هو محدد في [RFC-7748](https://tools.ietf.org/html/rfc7748).

- وظيفة التشفير: ChaChaPoly
  AEAD_CHACHA20_POLY1305 كما هو محدد في [RFC-7539](https://tools.ietf.org/html/rfc7539) القسم 2.8.
  nonce بطول 12 بايت، مع تعيين أول 4 بايتات إلى الصفر.
  مطابق لذلك الموجود في [NTCP2](/docs/specs/ntcp2/).

- Hash Function: SHA256
  هاش قياسي بحجم 32 بايت، مستخدم بالفعل على نطاق واسع في I2P.

### البدائل التشفيرية الجديدة لـ I2P

تحدد هذه المقترحة التحسينات التالية لـ Noise_IK_25519_ChaChaPoly_SHA256. وهذه تتبع عموماً الإرشادات الواردة في [NOISE](https://noiseprotocol.org/noise.html) القسم 13.

1) المفاتيح المؤقتة غير المشفرة مُرمزة باستخدام [Elligator2](https://elligator.cr.yp.to/).

2) الرد مسبوق بعلامة نص واضح.

3) تنسيق الحمولة محدد للرسائل 1، 2، ومرحلة البيانات. بالطبع، هذا غير محدد في Noise.

جميع الرسائل تتضمن رأس رسالة [I2NP](/docs/specs/i2np/) Garlic Message. مرحلة البيانات تستخدم تشفيرًا مشابهًا لمرحلة بيانات Noise، ولكنها غير متوافقة معها.

### نوع التشفير

المصافحات تستخدم أنماط مصافحة [Noise](https://noiseprotocol.org/noise.html).

يتم استخدام التطابق التالي للحروف:

- e = مفتاح مؤقت لمرة واحدة
- s = مفتاح ثابت
- p = حمولة الرسالة

جلسات الاستخدام الواحد وغير المقيدة مشابهة لنمط Noise N.

```

<- s
  ...
  e es p ->

```
الجلسات المربوطة مشابهة لنمط Noise IK.

```

<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->

```
### إطار عمل بروتوكول Noise

البروتوكول الحالي ElGamal/AES+SessionTag أحادي الاتجاه. في هذه الطبقة، لا يعرف المتلقي مصدر الرسالة. جلسات الإرسال والاستقبال غير مترابطة. الإقرارات تتم خارج النطاق باستخدام DeliveryStatusMessage (مغلفة في GarlicMessage) في clove.

هناك عدم كفاءة كبيرة في البروتوكول أحادي الاتجاه. أي رد يجب أن يستخدم أيضاً رسالة 'New Session' مكلفة. هذا يسبب استخدام أعلى لعرض النطاق الترددي ووحدة المعالجة المركزية والذاكرة.

هناك أيضاً نقاط ضعف أمنية في البروتوكول أحادي الاتجاه. جميع الجلسات تعتمد على DH مؤقت-ثابت. بدون مسار إرجاع، لا توجد طريقة لـ Bob لـ "ratchet" مفتاحه الثابت إلى مفتاح مؤقت. بدون معرفة مصدر الرسالة، لا توجد طريقة لاستخدام المفتاح المؤقت المستلم للرسائل الصادرة، لذلك الرد الأولي يستخدم أيضاً DH مؤقت-ثابت.

لهذا الاقتراح، نحدد آليتين لإنشاء بروتوكول ثنائي الاتجاه - "الإقران" و"الربط". توفر هذه الآليات كفاءة وأمان متزايدين.

### إضافات إلى الإطار العام

كما هو الحال مع ElGamal/AES+SessionTags، يجب أن تكون جميع الجلسات الواردة والصادرة في سياق معين، إما سياق الموجه أو السياق لوجهة محلية معينة. في Java I2P، يُسمى هذا السياق بـ Session Key Manager.

يجب عدم مشاركة الجلسات بين السياقات، حيث أن ذلك من شأنه أن يسمح بالربط بين الوجهات المحلية المختلفة، أو بين وجهة محلية وrouter.

عندما يدعم وجهة معينة كلاً من ElGamal/AES+SessionTags وهذا الاقتراح، يمكن لكلا النوعين من الجلسات مشاركة السياق. انظر القسم 1c) أدناه.

### أنماط المصافحة

عندما يتم إنشاء جلسة صادرة في المُرسِل (Alice)، يتم إنشاء جلسة واردة جديدة وإقرانها مع الجلسة الصادرة، إلا إذا لم يكن هناك رد متوقع (مثل raw datagrams).

جلسة واردة جديدة مقترنة دائماً بجلسة صادرة جديدة، إلا إذا لم يكن هناك رد مطلوب (مثل البيانات الخام).

إذا تم طلب رد وربطه بوجهة أو router بعيدة، فإن جلسة الإرسال الجديدة تلك تُربط بتلك الوجهة أو router، وتحل محل أي جلسة إرسال سابقة إلى تلك الوجهة أو router.

إقران الجلسات الواردة والصادرة يوفر بروتوكولاً ثنائي الاتجاه مع القدرة على تدوير مفاتيح DH.

### الجلسات

توجد جلسة صادرة واحدة فقط إلى وجهة أو router معين. قد توجد عدة جلسات واردة حالية من وجهة أو router معين. بشكل عام، عند إنشاء جلسة واردة جديدة، وتلقي حركة البيانات على تلك الجلسة (والتي تعمل كـ ACK)، ستتم علامة أي جلسات أخرى للانتهاء بسرعة نسبية، خلال دقيقة تقريباً. يتم فحص قيمة الرسائل المرسلة السابقة (PN)، وإذا لم توجد رسائل غير مستلمة (ضمن حجم النافذة) في الجلسة الواردة السابقة، فقد يتم حذف الجلسة السابقة فوراً.

عندما يتم إنشاء جلسة صادرة في المنشئ (Alice)، فإنها ترتبط بوجهة الطرف البعيد (Bob)، وأي جلسة واردة مقترنة ستكون أيضاً مرتبطة بوجهة الطرف البعيد. عندما تتقدم الجلسات، فإنها تستمر في الارتباط بوجهة الطرف البعيد.

عندما يتم إنشاء جلسة واردة في المستقبل (Bob)، يمكن ربطها بـ Destination البعيد (Alice)، حسب خيار Alice. إذا قامت Alice بتضمين معلومات الربط (مفتاحها الثابت) في رسالة New Session، فسيتم ربط الجلسة بذلك الـ destination، وسيتم إنشاء جلسة صادرة وربطها بنفس الـ Destination. عندما تتطور الجلسات، تستمر في البقاء مربوطة بـ Destination البعيد.

### سياق الجلسة

بالنسبة للحالة الشائعة، حالة التدفق (streaming)، نتوقع من Alice و Bob استخدام البروتوكول كما يلي:

- تقوم Alice بربط جلسة الصادرة الجديدة الخاصة بها بجلسة واردة جديدة، وكلاهما مرتبط بالوجهة البعيدة (Bob).
- تتضمن Alice معلومات الربط والتوقيع، وطلب رد، في رسالة New Session المُرسلة إلى Bob.
- يقوم Bob بربط جلسته الواردة الجديدة بجلسة صادرة جديدة، وكلاهما مرتبط بالوجهة البعيدة (Alice).
- يرسل Bob ردًا (ack) إلى Alice في الجلسة المقترنة، مع ratchet إلى مفتاح DH جديد.
- تقوم Alice بعمل ratchet إلى جلسة صادرة جديدة بمفتاح Bob الجديد، مقترنة بالجلسة الواردة الموجودة.

من خلال ربط جلسة واردة بـ Destination بعيدة المدى، وإقران الجلسة الواردة بجلسة صادرة مرتبطة بنفس الـ Destination، نحقق فائدتين رئيسيتين:

1) الرد الأولي من Bob إلى Alice يستخدم DH ephemeral-ephemeral

٢) بعد أن تتلقى Alice رد Bob وتقوم بعملية ratchet، جميع الرسائل اللاحقة من Alice إلى Bob تستخدم ephemeral-ephemeral DH.

### إقران جلسات الوارد والصادر

في ElGamal/AES+SessionTags، عندما يتم تجميع LeaseSet كـ garlic clove، أو يتم تسليم العلامات، يطلب router المرسل ACK. هذا عبارة عن garlic clove منفصل يحتوي على رسالة DeliveryStatus. لأمان إضافي، يتم تغليف رسالة DeliveryStatus في رسالة Garlic. هذه الآلية خارج النطاق من منظور البروتوكول.

في البروتوكول الجديد، نظراً لأن الجلسات الواردة والصادرة مقترنة، يمكننا الحصول على ACKs داخلياً. لا حاجة لـ clove منفصل.

إقرار الاستلام الصريح هو ببساطة رسالة جلسة موجودة بدون كتلة I2NP. ومع ذلك، في معظم الحالات، يمكن تجنب إقرار الاستلام الصريح، حيث يوجد حركة مرور عكسية. قد يكون من المرغوب فيه للتطبيقات أن تنتظر فترة قصيرة (ربما مائة ميلي ثانية) قبل إرسال إقرار استلام صريح، لإعطاء طبقة البث المباشر أو طبقة التطبيق وقتاً للاستجابة.

ستحتاج التطبيقات أيضًا إلى تأجيل أي إرسال للـ ACK حتى بعد معالجة كتلة I2NP، حيث قد تحتوي رسالة Garlic على Database Store Message مع lease set. سيكون من الضروري وجود lease set حديث لتوجيه الـ ACK، وستكون الوجهة البعيدة (الموجودة في الـ lease set) ضرورية للتحقق من المفتاح الثابت المربوط.

### ربط الجلسات والوجهات

يجب أن تنتهي صلاحية الجلسات الصادرة دائماً قبل الجلسات الواردة. عند انتهاء صلاحية جلسة صادرة وإنشاء جلسة جديدة، سيتم إنشاء جلسة واردة مقترنة جديدة أيضاً. إذا كانت هناك جلسة واردة قديمة، فسيُسمح لها بانتهاء الصلاحية.

### فوائد الربط والإقران

سيتم تحديده لاحقاً

### إقرارات الرسائل

نحدد الدوال التالية المقابلة للوحدات البنائية التشفيرية المستخدمة.

ZEROLEN

    zero-length byte array

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).
    || below means append.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

MixHash(d)

    SHA-256 hash function that takes a previous hash h and new data d,
    and produces an output of length 32 bytes.
    || below means append.

    Use SHA-256 as follows::

        MixHash(d) := h = SHA-256(h || d)

STREAM

    The ChaCha20/Poly1305 AEAD as specified in [RFC-7539](https://tools.ietf.org/html/rfc7539).
    S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Encrypts plaintext using the cipher key k, and nonce n which MUST be unique for
        the key k.
        Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16 bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, n, ciphertext, ad)
        Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional.
        Returns the plaintext.

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()
        Generates a new private key that maps to a public key suitable for Elligator2 encoding.
        Note that half of the randomly-generated private keys will not be suitable and must be discarded.

    ENCODE_ELG2(pubkey)
        Returns the Elligator2-encoded public key corresponding to the given public key (inverse mapping).
        Encoded keys are little endian.
        Encoded key must be 256 bits indistinguishable from random data.
        See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)
        Returns the public key corresponding to the given Elligator2-encoded public key.
        See Elligator2 section below for specification.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.

MixKey(d)

    Use HKDF() with a previous chainKey and new data d, and
    sets the new chainKey and k.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]


### مهلات انتهاء الجلسة

### البث المتعدد

رسالة garlic كما هو محدد في [I2NP](/docs/specs/i2np/) كما يلي. نظراً لأن هدف التصميم هو أن القفزات الوسطية لا تستطيع التمييز بين التشفير الجديد والقديم، فإن هذا التنسيق لا يمكن تغييره، حتى لو كان حقل الطول زائداً عن الحاجة. يُظهر التنسيق مع العنوان الكامل 16-byte، رغم أن العنوان الفعلي قد يكون في تنسيق مختلف، اعتماداً على وسيلة النقل المستخدمة.

عند فك التشفير، تحتوي البيانات على سلسلة من Garlic Cloves وبيانات إضافية، والمعروفة أيضاً باسم Clove Set.

راجع [I2NP](/docs/specs/i2np/) للحصول على التفاصيل والمواصفات الكاملة.

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
### التعريفات

تنسيق الرسالة الحالي، المستخدم لأكثر من 15 عاماً، هو ElGamal/AES+SessionTags. في ElGamal/AES+SessionTags، هناك تنسيقان للرسالة:

١) جلسة جديدة: - كتلة ElGamal بحجم ٥١٤ بايت - كتلة AES (١٢٨ بايت كحد أدنى، مضاعف الرقم ١٦)

2) الجلسة الموجودة: - 32 بايت Session Tag - كتلة AES (128 بايت كحد أدنى، مضاعف للرقم 16)

الحد الأدنى للحشو إلى 128 كما هو مطبق في Java I2P ولكن لا يتم فرضه عند الاستقبال.

هذه الرسائل محاطة بـ I2NP garlic message، والتي تحتوي على حقل طول، لذلك الطول معروف.

لاحظ أنه لا توجد حشوة محددة للطول غير مضاعف الـ 16، لذا فإن الجلسة الجديدة دائماً (mod 16 == 2)، والجلسة الموجودة دائماً (mod 16 == 0). نحتاج لإصلاح هذا.

يحاول المستقبل أولاً البحث عن أول 32 بايت كـ Session Tag. إذا وُجدت، فإنه يفك تشفير كتلة AES. إذا لم توجد، وكانت البيانات بطول (514+16) على الأقل، فإنه يحاول فك تشفير كتلة ElGamal، وإذا نجح، يفك تشفير كتلة AES.

### ١) تنسيق الرسالة

في Signal Double Ratchet، يحتوي الرأس على:

- DH: المفتاح العام الحالي للـ ratchet
- PN: طول رسالة السلسلة السابقة
- N: رقم الرسالة

"سلاسل الإرسال" الخاصة بـ Signal تعادل تقريباً مجموعات العلامات (tag sets) الخاصة بنا. باستخدام علامة الجلسة (session tag)، يمكننا إزالة معظم ذلك.

في الجلسة الجديدة، نضع المفتاح العام فقط في العنوان غير المشفر.

في الجلسة الموجودة، نستخدم علامة الجلسة للرأس. علامة الجلسة مرتبطة بالمفتاح العام الحالي لـ ratchet، ورقم الرسالة.

في كل من الجلسة الجديدة والموجودة، يكون PN و N في النص المشفر.

في Signal، الأمور تتطور باستمرار. مفتاح DH العام الجديد يتطلب من المستقبل أن يتطور ويرسل مفتاحاً عاماً جديداً مرة أخرى، والذي يعمل أيضاً كإقرار استلام للمفتاح العام المستلم. هذا سيكون عدداً كبيراً جداً من عمليات DH بالنسبة لنا. لذلك نفصل بين إقرار استلام المفتاح المستلم وإرسال مفتاح عام جديد. أي رسالة تستخدم session tag مُولد من مفتاح DH العام الجديد تشكل إقرار استلام (ACK). نحن نرسل مفتاحاً عاماً جديداً فقط عندما نرغب في إعادة تشفير المفاتيح.

الحد الأقصى لعدد الرسائل قبل أن يجب على DH القيام بـ ratchet هو 65535.

عند تسليم مفتاح الجلسة، نشتق "مجموعة العلامات" (Tag Set) منه، بدلاً من الحاجة إلى تسليم علامات الجلسة أيضاً. يمكن أن تحتوي مجموعة العلامات على ما يصل إلى 65536 علامة. ومع ذلك، يجب على المستقبلين تنفيذ استراتيجية "النظر إلى الأمام" (look-ahead)، بدلاً من توليد جميع العلامات المحتملة دفعة واحدة. قم بتوليد N علامة على الأكثر بعد آخر علامة صحيحة تم استقبالها. قد يكون N في أفضل الأحوال 128، ولكن 32 أو حتى أقل قد يكون خياراً أفضل.

### مراجعة تنسيق الرسائل الحالي

مفتاح عام لمرة واحدة لجلسة جديدة (32 بايت) البيانات المشفرة وMAC (البايتات المتبقية)

قد تحتوي أو لا تحتوي رسالة الجلسة الجديدة على المفتاح العام الثابت للمرسل. إذا تم تضمينه، فإن الجلسة العكسية ترتبط بذلك المفتاح. يجب تضمين المفتاح الثابت إذا كانت الردود متوقعة، أي للبث المتدفق والرسائل القابلة للرد. لا يجب تضمينه للرسائل الخام.

رسالة الجلسة الجديدة مشابهة لنمط Noise [NOISE](https://noiseprotocol.org/noise.html) أحادي الاتجاه "N" (إذا لم يتم إرسال المفتاح الثابت)، أو النمط ثنائي الاتجاه "IK" (إذا تم إرسال المفتاح الثابت).

### مراجعة تنسيق البيانات المشفرة

الطول هو 96 + طول البيانات المفيدة. التنسيق المشفر:

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
### علامات الجلسة الجديدة ومقارنة بـ Signal

المفتاح المؤقت يتكون من 32 بايت، مُرمز باستخدام Elligator2. هذا المفتاح لا يُعاد استخدامه أبداً؛ يتم توليد مفتاح جديد مع كل رسالة، بما في ذلك إعادة الإرسال.

### 1أ) تنسيق الجلسة الجديد

عند فك التشفير، مفتاح X25519 الثابت الخاص بأليس، 32 بايت.

### 1b) تنسيق الجلسة الجديد (مع الربط)

الطول المشفر هو باقي البيانات. الطول المفكوك هو أقل من الطول المشفر بـ 16. يجب أن تحتوي الحمولة على كتلة DateTime وعادة ما تحتوي على كتلة واحدة أو أكثر من كتل Garlic Clove. انظر قسم الحمولة أدناه للتنسيق والمتطلبات الإضافية.

### مفتاح الجلسة الجديد المؤقت

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
### المفتاح الثابت

مفتاح Alice المؤقت. المفتاح المؤقت يتكون من 32 بايت، مُرمز باستخدام Elligator2، little endian. هذا المفتاح لا يُعاد استخدامه أبداً؛ يتم إنشاء مفتاح جديد مع كل رسالة، بما في ذلك إعادة الإرسال.

### الحمولة

قسم الأعلام (Flags) لا يحتوي على شيء. يكون دائماً 32 بايت، لأنه يجب أن يكون بنفس طول المفتاح الثابت لرسائل الجلسة الجديدة مع الربط. يحدد Bob ما إذا كان مفتاحاً ثابتاً أم قسم أعلام عن طريق اختبار ما إذا كانت الـ 32 بايت كلها أصفار.

TODO هل هناك حاجة لأي flags هنا؟

### 1c) تنسيق الجلسة الجديد (بدون ربط)

الطول المشفر هو ما تبقى من البيانات. الطول المفكوك التشفير أقل بـ 16 من الطول المشفر. يجب أن تحتوي الحمولة على كتلة DateTime وعادة ما تحتوي على كتلة أو أكثر من كتل Garlic Clove. راجع قسم الحمولة أدناه للتنسيق والمتطلبات الإضافية.

### مفتاح الجلسة الجديد المؤقت

إذا كان من المتوقع إرسال رسالة واحدة فقط، فلا حاجة لإعداد جلسة أو مفتاح ثابت.

الطول هو 96 + طول الحمولة. التنسيق المشفر:

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
### قسم العلامات البيانات المفكوكة التشفير

المفتاح المستخدم مرة واحدة يبلغ 32 بايت، مُرمز باستخدام Elligator2، little endian. هذا المفتاح لا يُعاد استخدامه أبداً؛ يتم إنشاء مفتاح جديد مع كل رسالة، بما في ذلك إعادات الإرسال.

### الحمولة

يحتوي قسم Flags على لا شيء. يبلغ طوله دائماً 32 بايت، لأنه يجب أن يكون بنفس طول المفتاح الثابت لرسائل New Session مع الربط. يحدد Bob ما إذا كان مفتاحاً ثابتاً أم قسم flags عن طريق اختبار ما إذا كانت الـ 32 بايت كلها أصفار.

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
### 1د) تنسيق لمرة واحدة (بدون ربط أو جلسة)

الطول المشفر هو باقي البيانات. الطول المفكوك للتشفير أقل بـ 16 من الطول المشفر. يجب أن تحتوي الحمولة على كتلة DateTime وعادة ما تحتوي على كتلة واحدة أو أكثر من كتل Garlic Clove. راجع قسم الحمولة أدناه للتنسيق والمتطلبات الإضافية.

### مفتاح الجلسة الجديد لمرة واحدة

### قسم الأعلام البيانات المفكوكة التشفير

هذا هو [NOISE](https://noiseprotocol.org/noise.html) القياسي لـ IK مع اسم بروتوكول معدّل. لاحظ أننا نستخدم نفس المُهيِّئ لكل من نمط IK (الجلسات المربوطة) ونمط N (الجلسات غير المربوطة).

يتم تعديل اسم البروتوكول لسببين. أولاً، للإشارة إلى أن المفاتيح المؤقتة مُرمزة باستخدام Elligator2، وثانياً، للإشارة إلى أن MixHash() يتم استدعاؤها قبل الرسالة الثانية لخلط قيمة العلامة.

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
### الحمولة

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
### 1و) KDFs لرسالة الجلسة الجديدة

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
### KDF لـ ChainKey الأولي

لاحظ أن هذا هو نمط Noise "N"، لكننا نستخدم نفس مُهيئ "IK" كما هو الحال في الجلسات المرتبطة.

رسائل الجلسة الجديدة لا يمكن تحديدها كما لو كانت تحتوي على المفتاح الثابت لأليس أم لا حتى يتم فك تشفير المفتاح الثابت وفحصه لتحديد ما إذا كان يحتوي على أصفار فقط. لذلك، يجب على المستقبل استخدام آلة الحالة "IK" لجميع رسائل الجلسة الجديدة. إذا كان المفتاح الثابت يحتوي على أصفار فقط، فيجب تخطي نمط الرسالة "ss".

```

chainKey = from Flags/Static key section
  k = from Flags/Static key section
  n = 1
  ad = h from Flags/Static key section
  ciphertext = ENCRYPT(k, n, payload, ad)

```
### KDF لمحتويات قسم العلامات/المفتاح الثابت المشفرة

يمكن إرسال رد أو أكثر من ردود New Session Reply استجابة لرسالة New Session واحدة. كل رد يسبق بعلامة (tag)، والتي يتم إنشاؤها من TagSet للجلسة.

الـ New Session Reply يتكون من جزأين. الجزء الأول هو إكمال مصافحة Noise IK مع tag مُلحق في المقدمة. طول الجزء الأول هو 56 بايت. الجزء الثاني هو حمولة مرحلة البيانات. طول الجزء الثاني هو 16 + طول الحمولة.

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
### KDF لقسم الحمولة (مع مفتاح Alice الثابت)

يتم إنشاء العلامة في Session Tags KDF، كما تم تهيئتها في DH Initialization KDF أدناه. هذا يربط الرد بالجلسة. لا يتم استخدام Session Key من DH Initialization.

### KDF لقسم الحمولة (بدون مفتاح Alice الثابت)

مفتاح Bob المؤقت. المفتاح المؤقت هو 32 بايت، مُرمز بـ Elligator2، little endian. هذا المفتاح لا يُعاد استخدامه أبداً؛ يتم إنشاء مفتاح جديد مع كل رسالة، بما في ذلك إعادة الإرسال.

### 1g) تنسيق رد الجلسة الجديدة

الطول المشفر هو ما تبقى من البيانات. الطول المفكوك التشفير أقل بـ 16 من الطول المشفر. ستحتوي الحمولة عادة على كتلة أو أكثر من كتل Garlic Clove. انظر قسم الحمولة أدناه للتنسيق والمتطلبات الإضافية.

### علامة الجلسة

يتم إنشاء علامة واحدة أو أكثر من TagSet، والتي يتم تهيئتها باستخدام KDF أدناه، باستخدام chainKey من رسالة New Session.

```

// Generate tagset
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
### مفتاح جلسة الرد المؤقت الجديد

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
### الحمولة

هذا يشبه رسالة الجلسة الموجودة الأولى، بعد التقسيم، ولكن بدون علامة منفصلة. بالإضافة إلى ذلك، نستخدم الـ hash من الأعلى لربط الحمولة برسالة NSR.

```

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // AEAD parameters for New Session Reply payload
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### KDF لمجموعة علامات الرد

يمكن إرسال عدة رسائل NSR كرد، كل منها بمفاتيح مؤقتة فريدة، اعتماداً على حجم الاستجابة.

أليس وبوب مطلوبان لاستخدام مفاتيح عابرة جديدة لكل رسالة NS وNSR.

يجب على Alice أن تستقبل إحدى رسائل NSR من Bob قبل إرسال رسائل الجلسة الموجودة (ES)، ويجب على Bob أن يستقبل رسالة ES من Alice قبل إرسال رسائل ES.

تُستخدم ``chainKey`` و ``k`` من NSR Payload Section الخاصة بـ Bob كمدخلات لـ ES DH Ratchets الأولية (كلا الاتجاهين، انظر DH Ratchet KDF).

يجب على Bob الاحتفاظ بالجلسات الموجودة فقط لرسائل ES المستلمة من Alice. أي جلسات واردة أو صادرة أخرى تم إنشاؤها (لـ NSR متعددة) يجب تدميرها فوراً بعد استلام أول رسالة ES من Alice لجلسة معيّنة.

### دالة اشتقاق المفتاح لمحتويات مشفرة لقسم مفتاح الرد

علامة الجلسة (8 بايت) البيانات المشفرة و MAC (انظر القسم 3 أدناه)

### KDF للمحتويات المشفرة في قسم الحمولة

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
### ملاحظات

الطول المشفر هو باقي البيانات. الطول المفكوك التشفير أقل من الطول المشفر بـ 16. انظر قسم الحمولة أدناه للتنسيق والمتطلبات.

دالة اشتقاق المفتاح (KDF)

```
See AEAD section below.

  // AEAD parameters for Existing Session payload
  k = The 32-byte session key associated with this session tag
  n = The message number N in the current chain, as retrieved from the associated Session Tag.
  ad = The session tag, 8 bytes
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1ح) تنسيق الجلسة الموجودة

التنسيق: مفاتيح عامة وخاصة بحجم 32 بايت، little-endian.

المبرر: يُستخدم في [NTCP2](/docs/specs/ntcp2/).

### التنسيق

في عمليات المصافحة القياسية لـ Noise، تبدأ رسائل المصافحة الأولى في كل اتجاه بمفاتيح مؤقتة يتم إرسالها كنص واضح. نظراً لأن مفاتيح X25519 الصحيحة قابلة للتمييز عن البيانات العشوائية، قد يتمكن الوسيط المتطفل من تمييز هذه الرسائل عن رسائل الجلسة الحالية التي تبدأ بعلامات جلسة عشوائية. في [NTCP2](/docs/specs/ntcp2/) ([Proposal 111](/proposals/111-ntcp-2/))، استخدمنا دالة XOR منخفضة التكلفة باستخدام المفتاح الثابت خارج النطاق لتشويش المفتاح. ومع ذلك، نموذج التهديد هنا مختلف؛ نحن لا نريد السماح لأي MitM باستخدام أي وسيلة لتأكيد وجهة حركة البيانات، أو لتمييز رسائل المصافحة الأولى عن رسائل الجلسة الحالية.

لذلك، يتم استخدام [Elligator2](https://elligator.cr.yp.to/) لتحويل المفاتيح المؤقتة في رسائل New Session و New Session Reply بحيث تكون غير قابلة للتمييز عن السلاسل العشوائية المنتظمة.

### الحمولة

مفاتيح عامة وخاصة بحجم 32 بايت. المفاتيح المُرمزة تستخدم ترتيب little endian.

كما هو محدد في [Elligator2](https://elligator.cr.yp.to/)، فإن المفاتيح المشفرة غير قابلة للتمييز عن 254 بت عشوائية. نحن نتطلب 256 بت عشوائية (32 بايت). لذلك، يتم تعريف التشفير وفك التشفير كما يلي:

الترميز:

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
### 2) ECIES-X25519

مطلوب لمنع OBEP و IBGW من تصنيف حركة البيانات.

### 2أ) Elligator2

يضاعف Elligator2 متوسط وقت توليد المفاتيح، حيث أن نصف المفاتيح الخاصة ينتج عنها مفاتيح عامة غير مناسبة للترميز باستخدام Elligator2. كما أن وقت توليد المفاتيح غير محدود مع توزيع أسي، حيث يجب على المولد الاستمرار في إعادة المحاولة حتى يتم العثور على زوج مفاتيح مناسب.

يمكن إدارة هذا العبء الإضافي من خلال إجراء توليد المفاتيح مسبقاً، في thread منفصل، للاحتفاظ بمجموعة من المفاتيح المناسبة.

يقوم المولد بتنفيذ دالة ENCODE_ELG2() لتحديد الملاءمة. لذلك، ينبغي للمولد تخزين نتيجة ENCODE_ELG2() حتى لا يضطر لحسابها مرة أخرى.

بالإضافة إلى ذلك، قد تُضاف المفاتيح غير المناسبة إلى مجموعة المفاتيح المستخدمة لـ [NTCP2](/docs/specs/ntcp2/)، حيث لا يُستخدم Elligator2. المسائل الأمنية المتعلقة بذلك لم تُحدد بعد.

### التنسيق

AEAD باستخدام ChaCha20 و Poly1305، نفس الطريقة المستخدمة في [NTCP2](/docs/specs/ntcp2/). هذا يتوافق مع [RFC-7539](https://tools.ietf.org/html/rfc7539)، والذي يُستخدم أيضاً بطريقة مشابهة في TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

### التبرير

المدخلات لدوال التشفير/فك التشفير لكتلة AEAD في رسالة New Session:

```

k :: 32 byte cipher key
       See New Session and New Session Reply KDFs above.

  n :: Counter-based nonce, 12 bytes.
       n = 0

  ad :: Associated data, 32 bytes.
        The SHA256 hash of the preceding data, as output from mixHash()

  data :: Plaintext data, 0 or more bytes

```
### ملاحظات

المدخلات لوظائف التشفير/فك التشفير لكتلة AEAD في رسالة Existing Session:

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
### 3) AEAD (ChaChaPoly)

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
### مدخلات الجلسة الجديدة ورد الجلسة الجديدة

- نظراً لأن ChaCha20 هو مشفر تدفق، فلا حاجة لحشو النصوص الواضحة.
  يتم تجاهل بايتات التدفق المفتاحي الإضافية.

- يتم الاتفاق على مفتاح التشفير (256 بت) بواسطة SHA256 KDF.
  تفاصيل KDF لكل رسالة موجودة في أقسام منفصلة أدناه.

- إطارات ChaChaPoly ذات حجم معروف حيث أنها مُغلفة في رسالة بيانات I2NP.

- لجميع الرسائل،
  الحشو موجود داخل إطار
  البيانات المصدق عليها.

### مدخلات الجلسة الموجودة

يجب تجاهل جميع البيانات المستلمة التي تفشل في التحقق من AEAD. لا يتم إرجاع أي استجابة.

### التنسيق المشفر

يُستخدم في [NTCP2](/docs/specs/ntcp2/).

### ملاحظات

ما زلنا نستخدم session tags، كما كان من قبل، لكننا نستخدم ratchets لتوليدها. كان لدى session tags أيضاً خيار إعادة تشفير المفاتيح (rekey) الذي لم ننفذه أبداً. لذا الأمر يشبه double ratchet لكننا لم نقم بالثاني أبداً.

هنا نحدد شيئًا مشابهًا لـ Double Ratchet الخاص بـ Signal. يتم إنشاء علامات الجلسة بشكل حتمي ومتطابق على جانبي المستقبل والمرسل.

من خلال استخدام آلية التشفير المتماثل للمفتاح/العلامة، نتخلص من استهلاك الذاكرة لتخزين علامات الجلسة في جانب المرسل. كما نتخلص من استهلاك عرض النطاق الترددي لإرسال مجموعات العلامات. استهلاك الجانب المستقبل لا يزال كبيراً، لكن يمكننا تقليله أكثر حيث سنقلص علامة الجلسة من 32 بايت إلى 8 بايت.

نحن لا نستخدم تشفير العناوين كما هو محدد (واختياري) في Signal، بل نستخدم علامات الجلسة بدلاً من ذلك.

من خلال استخدام DH ratchet، نحقق forward secrecy، والتي لم يتم تنفيذها مطلقاً في ElGamal/AES+SessionTags.

ملاحظة: المفتاح العام لمرة واحدة للجلسة الجديدة (New Session one-time public key) ليس جزءاً من الـ ratchet، وظيفته الوحيدة هي تشفير مفتاح الـ DH ratchet الأولي لأليس.

### معالجة أخطاء AEAD

يتعامل Double Ratchet مع الرسائل المفقودة أو غير المرتبة من خلال تضمين علامة في كل رأس رسالة. يبحث المستقبل عن فهرس العلامة، وهذا هو رقم الرسالة N. إذا كانت الرسالة تحتوي على كتلة رقم الرسالة مع قيمة PN، يمكن للمستقبل حذف أي علامات أعلى من تلك القيمة في مجموعة العلامات السابقة، مع الاحتفاظ بالعلامات المتجاوزة من مجموعة العلامات السابقة في حالة وصول الرسائل المتجاوزة لاحقاً.

### المبرر

نحدد هياكل البيانات والدوال التالية لتنفيذ هذه الـ ratchets.

TAGSET_ENTRY

    A single entry in a TAGSET.

    INDEX
        An integer index, starting with 0

    SESSION_TAG
        An identifier to go out on the wire, 8 bytes

    SESSION_KEY
        A symmetric key, never goes on the wire, 32 bytes

مجموعة العلامات

    A collection of TAGSET_ENTRIES.

    CREATE(key, n)
        Generate a new TAGSET using initial cryptographic key material of 32 bytes.
        The associated session identifier is provided.
        The initial number of of tags to create is specified; this is generally 0 or 1
        for an outgoing session.
        LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)
        Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()
        Generate one more TAGSET_ENTRY, unless the maximum number SESSION_TAGS have
        already been generated.
        If LAST_INDEX is greater than or equal to 65535, return.
        ++ LAST_INDEX
        Create a new TAGSET_ENTRY with the LAST_INDEX value and the calculated SESSION_TAG.
        Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may
        be deferred and calculated in GET_SESSION_KEY().
        Calls EXPIRE()

    EXPIRE()
        Remove tags and keys that are too old, or if the TAGSET size exceeds some limit.

    RATCHET_TAG()
        Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()
        Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION
        The associated session.

    CREATION_TIME
        When the TAGSET was created.

    LAST_INDEX
        The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()
        Used for outgoing sessions only.
        EXTEND(1) is called if there are no remaining TAGSET_ENTRIES.
        If EXTEND(1) did nothing, the max of 65535 TAGSETS have been used,
        and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)
        Used for incoming sessions only.
        Returns the TAGSET_ENTRY containing the sessionTag.
        If found, the TAGSET_ENTRY is removed.
        If the SESSION_KEY calculation was deferred, it is calculated now.
        If there are few TAGSET_ENTRIES remaining, EXTEND(n) is called.


### 4) Ratchets

Ratchets ولكن ليس بنفس سرعة Signal. نحن نفصل إقرار المفتاح المستلم عن توليد المفتاح الجديد. في الاستخدام النموذجي، ستقوم Alice وBob كلاهما بعمل ratchet (مرتين) فوراً في جلسة جديدة، ولكن لن يقوما بعمل ratchet مرة أخرى.

لاحظ أن ratchet مخصص لاتجاه واحد، وينتج سلسلة ratchet جديدة لعلامة الجلسة / مفتاح الرسالة لذلك الاتجاه. لتوليد مفاتيح لكلا الاتجاهين، عليك تشغيل ratchet مرتين.

تقوم بالتطوير في كل مرة تولد فيها وترسل مفتاحاً جديداً. تقوم بالتطوير في كل مرة تتلقى فيها مفتاحاً جديداً.

تقوم Alice بعملية ratchet واحدة عند إنشاء جلسة صادرة غير مرتبطة، وهي لا تنشئ جلسة واردة (غير مرتبطة تعني غير قابلة للرد عليها).

يقوم Bob بعمل ratchet مرة واحدة عند إنشاء جلسة واردة غير مربوطة، ولا ينشئ جلسة صادرة مقابلة (غير المربوط لا يمكن الرد عليه).

تواصل Alice إرسال رسائل الجلسة الجديدة (NS) إلى Bob حتى تستقبل إحدى رسائل رد الجلسة الجديدة (NSR) الخاصة به. ثم تستخدم نتائج KDF من قسم الحمولة الخاص بـ NSR كمدخلات لآليات ratchet الخاصة بالجلسة (انظر DH Ratchet KDF)، وتبدأ في إرسال رسائل الجلسة الموجودة (ES).

لكل رسالة NS مستلمة، ينشئ Bob جلسة واردة جديدة، باستخدام نتائج KDF لقسم الحمولة الخاص بالرد كمدخلات لـ ES DH Ratchet الوارد والصادر الجديد.

لكل رد مطلوب، يرسل Bob إلى Alice رسالة NSR مع الرد في البيانات الحمولة. من المطلوب أن يستخدم Bob مفاتيح مؤقتة جديدة لكل NSR.

يجب على Bob أن يتلقى رسالة ES من Alice على إحدى الجلسات الواردة، قبل إنشاء وإرسال رسائل ES على الجلسة الصادرة المقابلة.

يجب على Alice استخدام مؤقت لاستقبال رسالة NSR من Bob. إذا انتهت صلاحية المؤقت، يجب إزالة الجلسة.

لتجنب هجوم KCI و/أو استنزاف الموارد، حيث يقوم المهاجم بإسقاط ردود NSR الخاصة بـ Bob لإبقاء Alice ترسل رسائل NS، يجب على Alice تجنب بدء جلسات جديدة مع Bob بعد عدد معين من المحاولات بسبب انتهاء صلاحية المؤقت.

أليس وبوب يقوم كل منهما بعملية DH ratchet لكل كتلة NextKey يتم استلامها.

Alice و Bob كل منهما ينشئ مجموعات علامات جديدة ومفتاحين متماثلين ratchets بعد كل DH ratchet. لكل رسالة ES جديدة في اتجاه معين، Alice و Bob يقدمان علامة الجلسة والمفتاح المتماثل ratchets.

تكرار DH ratchets بعد المصافحة الأولية يعتمد على التنفيذ. بينما يضع البروتوكول حداً أقصى قدره 65535 رسالة قبل أن يصبح ratchet مطلوباً، فإن استخدام ratcheting أكثر تكراراً (بناءً على عدد الرسائل أو الوقت المنقضي أو كليهما) قد يوفر أماناً إضافياً.

بعد المصافحة النهائية KDF على الجلسات المربوطة، يجب على Bob و Alice تشغيل دالة Noise Split() على CipherState الناتج لإنشاء مفاتيح متماثلة مستقلة ومفاتيح سلسلة العلامات للجلسات الواردة والصادرة.

#### KEY AND TAG SET IDS

تُستخدم أرقام معرّفات مجموعات المفاتيح والعلامات لتحديد المفاتيح ومجموعات العلامات. تُستخدم معرّفات المفاتيح في كتل NextKey لتحديد المفتاح المُرسل أو المُستخدم. تُستخدم معرّفات مجموعات العلامات (مع رقم الرسالة) في كتل ACK لتحديد الرسالة التي يتم إقرارها. تنطبق معرّفات المفاتيح ومجموعات العلامات على مجموعات العلامات لاتجاه واحد. يجب أن تكون أرقام معرّفات المفاتيح ومجموعات العلامات متسلسلة.

في مجموعات العلامات الأولى المستخدمة لجلسة في كل اتجاه، يكون معرف مجموعة العلامات 0. لم يتم إرسال كتل NextKey، لذلك لا توجد معرفات مفاتيح.

لبدء عملية DH ratchet، يرسل المُرسِل كتلة NextKey جديدة بمعرف مفتاح 0. يرد المُستقبِل بكتلة NextKey جديدة بمعرف مفتاح 0. يبدأ المُرسِل بعد ذلك في استخدام مجموعة علامات جديدة بمعرف مجموعة علامات 1.

يتم إنشاء مجموعات العلامات اللاحقة بطريقة مماثلة. لجميع مجموعات العلامات المستخدمة بعد تبادلات NextKey، يكون رقم مجموعة العلامات هو (1 + معرف مفتاح Alice + معرف مفتاح Bob).

معرفات المفاتيح ومجموعات العلامات تبدأ من 0 وتزداد بشكل تسلسلي. الحد الأقصى لمعرف مجموعة العلامات هو 65535. الحد الأقصى لمعرف المفتاح هو 32767. عندما تكون مجموعة العلامات على وشك النفاد، يجب على مرسل مجموعة العلامات بدء تبادل NextKey. عندما تكون مجموعة العلامات 65535 على وشك النفاد، يجب على مرسل مجموعة العلامات بدء جلسة جديدة عن طريق إرسال رسالة New Session.

مع حد أقصى لحجم الرسالة المتدفقة يبلغ 1730، وبافتراض عدم وجود إعادة إرسال، فإن الحد الأقصى النظري لنقل البيانات باستخدام مجموعة tag واحدة هو 1730 * 65536 ~= 108 ميجابايت. سيكون الحد الأقصى الفعلي أقل بسبب إعادة الإرسال.

الحد الأقصى النظري لنقل البيانات مع جميع مجموعات العلامات الـ 65536 المتاحة، قبل أن تضطر الجلسة للتخلص منها واستبدالها، هو 64K * 108 MB ~= 6.9 TB.

#### DH RATCHET MESSAGE FLOW

تبادل المفاتيح التالي لمجموعة العلامات يجب أن يبدأه مرسل تلك العلامات (مالك مجموعة العلامات الصادرة). المستقبل (مالك مجموعة العلامات الواردة) سوف يستجيب. بالنسبة لحركة مرور HTTP GET النموذجية في طبقة التطبيق، سيرسل Bob رسائل أكثر وسيقوم بعملية ratchet أولاً من خلال بدء تبادل المفاتيح؛ الرسم البياني أدناه يوضح ذلك. عندما تقوم Alice بعملية ratchet، يحدث نفس الشيء بالعكس.

مجموعة العلامات الأولى المستخدمة بعد مصافحة NS/NSR هي مجموعة العلامات 0. عندما تكون مجموعة العلامات 0 على وشك النفاد، يجب تبادل مفاتيح جديدة في كلا الاتجاهين لإنشاء مجموعة العلامات 1. بعد ذلك، يتم إرسال مفتاح جديد في اتجاه واحد فقط.

لإنشاء مجموعة العلامات 2، يرسل مُرسِل العلامة مفتاحاً جديداً ويرسل مُستقبِل العلامة معرف مفتاحه القديم كإقرار. يقوم كلا الطرفين بـ DH.

لإنشاء مجموعة العلامات 3، يرسل مرسل العلامة معرف مفتاحه القديم ويطلب مفتاحًا جديدًا من مستقبل العلامة. يقوم كلا الطرفين بتنفيذ DH.

يتم إنشاء مجموعات العلامات اللاحقة كما هو الحال مع مجموعات العلامات 2 و 3. رقم مجموعة العلامات هو (1 + معرف مفتاح المرسل + معرف مفتاح المستقبل).

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
بعد اكتمال آلية DH ratchet للـ tagset الصادر، وإنشاء tagset صادر جديد، يجب استخدامه فورًا، ويمكن حذف الـ tagset الصادر القديم.

بعد اكتمال DH ratchet للـ tagset الواردة، وإنشاء tagset واردة جديدة، يجب على المستقبل الاستماع للعلامات في كلا الـ tagsets، وحذف الـ tagset القديمة بعد فترة قصيرة، حوالي 3 دقائق.

ملخص تقدم مجموعة العلامات ومعرف المفتاح موضح في الجدول أدناه. * تشير إلى أنه يتم إنشاء مفتاح جديد.

| New Tag Set ID | Sender key ID | Rcvr key ID |
|----------------|---------------|-------------|
| 0              | n/a           | n/a         |
| 1              | 0 *           | 0 *         |
| 2              | 1 *           | 0           |
| 3              | 1             | 1 *         |
| 4              | 2 *           | 1           |
| 5              | 2             | 2 *         |
| ...            | ...           | ...         |
| 65534          | 32767 *       | 32766       |
| 65535          | 32767         | 32767 *     |
يجب أن تكون أرقام معرفات المفاتيح ومجموعات العلامات متتالية.

#### DH INITIALIZATION KDF

هذا هو تعريف DH_INITIALIZE(rootKey, k) لاتجاه واحد. ينشئ tagset، و "next root key" لاستخدامها في DH ratchet لاحق إذا لزم الأمر.

نستخدم تهيئة DH في ثلاثة أماكن. أولاً، نستخدمها لتوليد مجموعة علامات لـ New Session Replies. ثانياً، نستخدمها لتوليد مجموعتي علامات، واحدة لكل اتجاه، للاستخدام في رسائل Existing Session. أخيراً، نستخدمها بعد DH Ratchet لتوليد مجموعة علامات جديدة في اتجاه واحد لرسائل Existing Session إضافية.

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
#### DH RATCHET KDF

يتم استخدام هذا بعد تبادل مفاتيح DH الجديدة في كتل NextKey، قبل نفاد tagset.

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
### أرقام الرسائل

آليات Ratchet لكل رسالة، كما هو الحال في Signal. آلية ratchet لعلامة الجلسة متزامنة مع آلية ratchet للمفتاح المتماثل، لكن آلية ratchet لمفتاح المستقبل قد "تتأخر" لتوفير الذاكرة.

يقوم المرسل بعملية ratchet واحدة لكل رسالة مرسلة. لا يجب تخزين علامات إضافية. يجب على المرسل أيضاً الاحتفاظ بعداد لـ 'N'، رقم الرسالة للرسالة في السلسلة الحالية. يتم تضمين قيمة 'N' في الرسالة المرسلة. راجع تعريف كتلة رقم الرسالة.

يجب على المستقبل أن يتقدم بحجم النافذة الأقصى ويخزن العلامات في "مجموعة علامات"، والتي ترتبط بالجلسة. بمجرد الاستقبال، يمكن التخلص من العلامة المخزنة، وإذا لم تكن هناك علامات سابقة غير مستقبلة، يمكن تقديم النافذة. يجب على المستقبل الاحتفاظ بقيمة 'N' المرتبطة بكل علامة جلسة، والتحقق من أن الرقم في الرسالة المرسلة يطابق هذه القيمة. انظر تعريف كتلة Message Number.

#### KDF

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
### تنفيذ نموذجي

Ratchets لكل رسالة، كما في Signal. كل مفتاح متماثل له رقم رسالة وعلامة جلسة مرتبطة به. ratchet مفتاح الجلسة متزامن مع ratchet العلامة المتماثلة، لكن ratchet مفتاح المستقبِل قد "يتأخر" لتوفير الذاكرة.

المرسل يقوم بالتنقل (ratchet) مرة واحدة لكل رسالة يتم إرسالها. لا يجب تخزين مفاتيح إضافية.

عندما يحصل المستقبل على session tag، إذا لم يكن قد قام بالفعل بتقديم symmetric key ratchet للوصول إلى المفتاح المرتبط، فيجب عليه "اللحاق" بالمفتاح المرتبط. من المحتمل أن يقوم المستقبل بتخزين المفاتيح مؤقتاً لأي tags سابقة لم يتم استلامها بعد. بمجرد الاستلام، يمكن التخلص من المفتاح المخزن، وإذا لم تكن هناك tags سابقة غير مستلمة، فيمكن تقديم النافذة.

لتحقيق الكفاءة، يكون ratchet علامة الجلسة و ratchet المفتاح المتماثل منفصلين بحيث يمكن لـ ratchet علامة الجلسة أن يتقدم على ratchet المفتاح المتماثل. وهذا يوفر أيضاً بعض الأمان الإضافي، حيث أن علامات الجلسة تخرج عبر الشبكة.

#### KDF

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
### 4أ) DH Ratchet

هذا يحل محل تنسيق قسم AES المحدد في مواصفات ElGamal/AES+SessionTags.

هذا يستخدم نفس تنسيق الكتلة كما هو محدد في مواصفات [NTCP2](/docs/specs/ntcp2/). يتم تعريف أنواع الكتل الفردية بشكل مختلف.

هناك مخاوف من أن تشجيع المطورين على مشاركة الكود قد يؤدي إلى مشاكل في التحليل. يجب على المطورين النظر بعناية في فوائد ومخاطر مشاركة الكود، والتأكد من أن قواعد الترتيب والكتل الصالحة مختلفة للسياقين.

### Payload Section Decrypted data

الطول المشفر هو الجزء المتبقي من البيانات. الطول المفكوك التشفير يقل بـ 16 عن الطول المشفر. جميع أنواع الكتل مدعومة. المحتويات النموذجية تتضمن الكتل التالية:

| Payload Block Type | Type Number | Block Length |
|--------------------|-------------|--------------|
| DateTime           | 0           | 7            |
| Termination (TBD)  | 4           | 9 typ.       |
| Options (TBD)      | 5           | 21+          |
| Message Number (TBD) | 6           | TBD          |
| Next Key           | 7           | 3 or 35      |
| ACK                | 8           | 4 typ.       |
| ACK Request        | 9           | 3            |
| Garlic Clove       | 11          | varies       |
| Padding            | 254         | varies       |
### Unencrypted data

يحتوي الإطار المشفر على صفر أو أكثر من الكتل. تحتوي كل كتلة على معرف بحجم بايت واحد، وطول بحجم بايتين، وصفر أو أكثر من بايتات البيانات.

للقابلية للتوسعة، يجب على المستقبلات تجاهل الكتل ذات أرقام الأنواع غير المعروفة، والتعامل معها كحشو.

البيانات المشفرة يبلغ حدها الأقصى 65535 بايت، بما في ذلك رأسية المصادقة البالغة 16 بايت، لذا فإن الحد الأقصى للبيانات غير المشفرة هو 65519 بايت.

(علامة المصادقة Poly1305 غير معروضة):

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
### Block Ordering Rules

في رسالة الجلسة الجديدة، كتلة DateTime مطلوبة، ويجب أن تكون الكتلة الأولى.

الكتل المسموحة الأخرى:

- Garlic Clove (النوع 11)
- خيارات (النوع 5)
- حشو (النوع 254)

في رسالة New Session Reply، لا توجد حاجة إلى أي blocks.

الكتل الأخرى المسموحة:

- Garlic Clove (النوع 11)
- Options (النوع 5)
- Padding (النوع 254)

لا يُسمح بأي blocks أخرى. الحشو (Padding)، إذا كان موجوداً، يجب أن يكون آخر block.

في رسالة الجلسة الموجودة، لا تُطلب أي كتل، والترتيب غير محدد، باستثناء المتطلبات التالية:

الإنهاء، إذا كان موجوداً، يجب أن يكون الكتلة الأخيرة باستثناء الحشو. الحشو، إذا كان موجوداً، يجب أن يكون الكتلة الأخيرة.

قد تحتوي الإطار الواحد على عدة كتل Garlic Clove. قد يحتوي الإطار الواحد على كتلتين Next Key كحد أقصى. لا يُسمح بوجود عدة كتل Padding في الإطار الواحد. أنواع الكتل الأخرى على الأرجح لن تحتوي على كتل متعددة في الإطار الواحد، لكن ذلك غير محظور.

### DateTime

انتهاء صلاحية. يساعد في منع الردود. يجب على Bob التحقق من أن الرسالة حديثة، باستخدام هذا الطابع الزمني. يجب على Bob تطبيق Bloom filter أو آلية أخرى لمنع هجمات replay، إذا كان الوقت صالحاً. يتم تضمينه عادةً في رسائل New Session فقط.

```

+----+----+----+----+----+----+----+
  | 0  |    4    |     timestamp     |
  +----+----+----+----+----+----+----+

  blk :: 0
  size :: 2 bytes, big endian, value = 4
  timestamp :: Unix timestamp, unsigned seconds.
               Wraps around in 2106

```
### 4ب) Session Tag Ratchet

كتلة Garlic Clove واحدة مفكوكة التشفير كما هو محدد في [I2NP](/docs/specs/i2np/)، مع تعديلات لإزالة الحقول غير المستخدمة أو المكررة. تحذير: هذا التنسيق مختلف بشكل كبير عن التنسيق الخاص بـ ElGamal/AES. كل clove هو كتلة حمولة منفصلة. لا يجوز تقسيم Garlic Cloves عبر الكتل أو عبر إطارات ChaChaPoly.

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
         the Garlic Clove section of [I2NP](/docs/specs/i2np/).
         Length varies but is typically 1, 33, or 37 bytes

  type :: I2NP message type

  Message_ID :: 4 byte `Integer` I2NP message ID

  Expiration :: 4 bytes, seconds since the epoch

```
ملاحظات:

- يجب على المطورين التأكد من أنه عند قراءة كتلة،
  فإن البيانات المشوهة أو الضارة لن تسبب تجاوز القراءة
  إلى الكتلة التالية.

- تنسيق Clove Set المحدد في [I2NP](/docs/specs/i2np/) غير مستخدم.
  كل clove موجود في كتلته الخاصة.

- رأس رسالة I2NP يبلغ 9 بايت، بتنسيق مطابق
  للمستخدم في [NTCP2](/docs/specs/ntcp2/).

- الشهادة ومعرف الرسالة وانتهاء الصلاحية من
  تعريف Garlic Message في [I2NP](/docs/specs/i2np/) غير مضمنة.

- الشهادة، معرف Clove، وتاريخ انتهاء الصلاحية من
  تعريف Garlic Clove في [I2NP](/docs/specs/i2np/) غير مُضمَّنة.

التبرير:

- لم يتم استخدام الشهادات مطلقاً.
- لم يتم استخدام معرف الرسالة المنفصل ومعرفات clove المنفصلة مطلقاً.
- لم يتم استخدام انتهاءات الصلاحية المنفصلة مطلقاً.
- إجمالي التوفير مقارنة بتنسيقات Clove Set وClove القديمة
  يبلغ تقريباً 35 بايت لـ clove واحد، و54 بايت لـ clove اثنين،
  و73 بايت لـ 3 cloves.
- تنسيق الكتلة قابل للتوسيع ويمكن إضافة أي حقول جديدة
  كأنواع كتل جديدة.

### Termination

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
### 4c) Symmetric Key Ratchet

الخرخيشة المتماثلة للمفاتيح

غير مُطبَّق، للدراسة الإضافية. تمرير الخيارات المحدَّثة. تتضمن الخيارات معاملات مختلفة للجلسة. راجع قسم Session Tag Length Analysis أدناه للحصول على مزيد من المعلومات.

كتلة الخيارات قد تكون ذات طول متغير، حيث قد تكون more_options موجودة.

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
SOTW هو توصية المرسل للمستقبل لنافذة العلامات الواردة للمستقبل (أقصى نظرة مسبقة). RITW هو إعلان المرسل لنافذة العلامات الواردة (أقصى نظرة مسبقة) التي يخطط لاستخدامها. يقوم كل طرف بعد ذلك بتعيين أو تعديل النظرة المسبقة بناءً على حد أدنى أو أقصى أو حساب آخر.

ملاحظات:

- الدعم لطول علامة الجلسة غير الافتراضي نأمل ألا
  يكون مطلوباً أبداً.
- نافذة العلامة هي MAX_SKIP في وثائق Signal.

المشاكل:

- التفاوض على الخيارات قيد التحديد.
- الافتراضيات قيد التحديد.
- خيارات الحشو والتأخير منسوخة من NTCP2،
  ولكن هذه الخيارات لم يتم تنفيذها أو دراستها بالكامل هناك.

### Message Numbers

التنفيذ اختياري. الطول (عدد الرسائل المرسلة) في مجموعة العلامات السابقة (PN). يمكن للمستقبل حذف العلامات الأعلى من PN من مجموعة العلامات السابقة فورًا. يمكن للمستقبل انتهاء صلاحية العلامات الأقل من أو تساوي PN من مجموعة العلامات السابقة بعد فترة قصيرة (مثل دقيقتين).

```

+----+----+----+----+----+
  | 6  |  size   |  PN    |
 +----+----+----+----+----+

  blk :: 6
  size :: 2
  PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.

```
ملاحظات:

- الحد الأقصى لـ PN هو 65535.
- تعريفات PN تساوي تعريف Signal، ناقص واحد.
  هذا مشابه لما يفعله Signal، ولكن في Signal، PN و N موجودان في الرأس.
  هنا، هما في نص الرسالة المشفرة.
- لا ترسل هذا البلوك في tag set 0، لأنه لم يكن هناك tag set سابق.

### 5) الحمولة

مفتاح DH ratchet التالي موجود في الـ payload، وهو اختياري. نحن لا نقوم بعملية ratchet في كل مرة. (هذا مختلف عن signal، حيث يكون في الـ header، ويُرسل في كل مرة)

بالنسبة للـ ratchet الأول، Key ID = 0.

غير مسموح في NS أو NSR. يُضمّن فقط في رسائل الجلسة الموجودة.

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

- Key ID هو عداد متزايد للمفتاح المحلي المستخدم لمجموعة العلامات تلك، بدءًا من 0.
- يجب ألا يتغير الـ ID إلا إذا تغير المفتاح.
- قد لا يكون ضروريًا بشكل صارم، لكنه مفيد للتصحيح.
  Signal لا يستخدم key ID.
- الحد الأقصى لـ Key ID هو 32767.
- في الحالة النادرة التي تكون فيها مجموعات العلامات في كلا الاتجاهين تعمل بآلية ratcheting في
  نفس الوقت، سيحتوي الإطار على كتلتين Next Key، واحدة للمفتاح الأمامي
  وواحدة للمفتاح العكسي.
- أرقام المفتاح ومعرف مجموعة العلامات يجب أن تكون متسلسلة.
- راجع قسم DH Ratchet أعلاه للتفاصيل.

### قسم الحمولة البيانات المفكوكة التشفير

يتم إرسال هذا فقط في حالة استلام كتلة طلب إقرار (ack request block). قد تكون عدة إقرارات موجودة لتأكيد استلام رسائل متعددة.

غير مسموح في NS أو NSR. يتم تضمينه فقط في رسائل الجلسة الموجودة.

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

- معرف مجموعة العلامات و N يحددان بشكل فريد الرسالة التي يتم تأكيد استلامها.
- في مجموعات العلامات الأولى المستخدمة للجلسة في كل اتجاه، يكون معرف مجموعة العلامات 0.
- لم يتم إرسال أي كتل NextKey، لذا لا توجد معرفات مفاتيح.
- لجميع مجموعات العلامات المستخدمة بعد تبادلات NextKey، يكون رقم مجموعة العلامات هو (1 + معرف مفتاح Alice + معرف مفتاح Bob).

### البيانات غير المشفرة

طلب إقرار استلام داخل النطاق. لاستبدال رسالة DeliveryStatus خارج النطاق في Garlic Clove.

إذا تم طلب إقرار صريح، يتم إرجاع معرف tagset الحالي ورقم الرسالة (N) في كتلة إقرار.

غير مسموح في NS أو NSR. يتم تضمينه فقط في رسائل الجلسة الموجودة.

```

+----+----+----+----+
  |  9 |  size   |flg |
  +----+----+----+----+

  blk :: 9
  size :: 1
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility

```
### قواعد ترتيب الكتل

جميع الحشو موجود داخل إطارات AEAD. TODO الحشو داخل AEAD يجب أن يلتزم تقريباً بالمعاملات المتفاوض عليها. TODO Alice أرسلت معاملات tx/rx الدنيا/العليا المطلوبة في رسالة NS. TODO Bob أرسل معاملات tx/rx الدنيا/العليا المطلوبة في رسالة NSR. يمكن إرسال خيارات محدثة أثناء مرحلة البيانات. انظر معلومات كتلة الخيارات أعلاه.

إذا كان موجوداً، يجب أن يكون هذا آخر block في الإطار.

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

- الحشو بالأصفار فقط مقبول، حيث سيتم تشفيره.
- استراتيجيات الحشو لم تُحدد بعد.
- الإطارات التي تحتوي على حشو فقط مسموحة.
- الحشو الافتراضي هو 0-15 بايت.
- راجع كتلة الخيارات لتفاوض معامل الحشو
- راجع كتلة الخيارات لمعاملات الحشو الدنيا/العليا
- استجابة الـ router عند انتهاك الحشو المتفاوض عليه تعتمد على التنفيذ.

### التاريخ والوقت

يجب على التنفيذات تجاهل أنواع الكتل المجهولة من أجل التوافق المستقبلي.

### فص Garlic

- يجب تحديد طول الحشو إما على أساس كل رسالة على حدة وتقديرات توزيع الطول، أو إضافة تأخيرات عشوائية. هذه التدابير المضادة يجب تضمينها لمقاومة الفحص العميق للحزم (DPI)، حيث أن أحجام الرسائل قد تكشف أن حركة مرور I2P يتم نقلها بواسطة بروتوكول النقل. نظام الحشو الدقيق هو مجال للعمل المستقبلي، الملحق A يوفر معلومات أكثر حول هذا الموضوع.

## Typical Usage Patterns

### الإنهاء

هذه هي حالة الاستخدام الأكثر شيوعاً، ومعظم حالات الاستخدام للبث غير HTTP ستكون مطابقة لهذه الحالة أيضاً. يتم إرسال رسالة أولية صغيرة، يتبعها رد، ثم يتم إرسال رسائل إضافية في كلا الاتجاهين.

طلب HTTP GET عادة ما يتناسب مع رسالة I2NP واحدة. ترسل Alice طلباً صغيراً مع رسالة Session جديدة واحدة، مع تجميع reply leaseset. تتضمن Alice تبديل فوري للمفتاح الجديد. يتضمن توقيع لربط الوجهة. لا يُطلب إقرار استلام.

يقوم Bob بعملية ratchet فوراً.

أليس تقوم بالتدوير فوراً.

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
### الخيارات

أليس لديها ثلاثة خيارات:

1) إرسال الرسالة الأولى فقط (window size = 1)، كما في HTTP GET. غير مُوصى به.

2) إرسال حتى نافذة التدفق، ولكن باستخدام نفس المفتاح العام للنص الواضح المشفر بـ Elligator2. جميع الرسائل تحتوي على نفس المفتاح العام التالي (ratchet). سيكون هذا مرئياً لـ OBGW/IBEP لأنها جميعاً تبدأ بنفس النص الواضح. تستمر الأمور كما في 1). غير موصى به.

3) التنفيذ الموصى به. إرسال حتى نافذة التدفق، ولكن باستخدام مفتاح عام مختلف مُرمز بـ Elligator2 (جلسة) لكل واحدة. جميع الرسائل تحتوي على نفس المفتاح العام التالي (ratchet). لن يكون هذا مرئياً لـ OBGW/IBEP لأنها جميعاً تبدأ بنص واضح مختلف. يجب على Bob أن يتعرف على أنها جميعاً تحتوي على نفس المفتاح العام التالي، ويستجيب للجميع بنفس الـ ratchet. Alice تستخدم ذلك المفتاح العام التالي وتتابع.

تدفق الرسائل للخيار 3:

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
### أرقام الرسائل

رسالة واحدة، مع توقع رد واحد. قد يتم إرسال رسائل أو ردود إضافية.

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
### مفتاح DH Ratchet العام التالي

رسائل مجهولة متعددة، دون توقع ردود.

في هذا السيناريو، تطلب Alice جلسة، ولكن بدون ربط. يتم إرسال رسالة جلسة جديدة. لا يتم تجميع reply LS. يتم تجميع reply DSM (هذه هي حالة الاستخدام الوحيدة التي تتطلب DSMs مجمعة). لا يتم تضمين مفتاح تالي. لا يتم طلب رد أو ratchet. لا يتم إرسال ratchet. تقوم الخيارات بتعيين نافذة علامات الجلسة إلى صفر.

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
### إقرار

رسالة مجهولة واحدة، بدون توقع رد.

يتم إرسال رسالة لمرة واحدة. لا يتم تجميع LS أو DSM للرد. لا يتم تضمين مفتاح تالي. لا يُطلب رد أو ratchet. لا يتم إرسال ratchet. تقوم الخيارات بتعيين نافذة علامات الجلسة إلى صفر.

```

Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message

```
### طلب إقرار الاستلام

الجلسات طويلة المدى قد تقوم بـ ratchet، أو تطلب ratchet، في أي وقت، للحفاظ على السرية التامة من تلك النقطة الزمنية. يجب على الجلسات أن تقوم بـ ratchet عندما تقترب من حد الرسائل المرسلة لكل جلسة (65535).

## Implementation Considerations

### الحشو

كما هو الحال مع بروتوكول ElGamal/AES+SessionTag الموجود، يجب على التنفيذات تحديد تخزين session tag والحماية ضد هجمات استنزاف الذاكرة.

تشمل بعض الاستراتيجيات الموصى بها:

- حد أقصى صارم على عدد علامات الجلسة المخزنة
- انتهاء صلاحية قاسي للجلسات الواردة الخاملة عند الضغط على الذاكرة
- حد أقصى على عدد الجلسات الواردة المرتبطة بوجهة واحدة بعيدة المدى
- تقليل تكيفي لنافذة علامات الجلسة وحذف العلامات القديمة غير المستخدمة
  عند الضغط على الذاكرة
- رفض تنفيذ ratchet عند الطلب، إذا كان هناك ضغط على الذاكرة

### أنواع الكتل الأخرى

المعاملات والمهلات الزمنية الموصى بها:

- حجم مجموعة علامات NSR: 12 tsmin و tsmax
- حجم مجموعة علامات ES 0: tsmin 24، tsmax 160
- حجم مجموعة علامات ES (1+): 160 tsmin و tsmax
- مهلة زمنية لمجموعة علامات NSR: 3 دقائق للمستقبل
- مهلة زمنية لمجموعة علامات ES: 8 دقائق للمرسل، 10 دقائق للمستقبل
- إزالة مجموعة علامات ES السابقة بعد: 3 دقائق
- نظرة مسبقة لمجموعة العلامات للعلامة N: min(tsmax, tsmin + N/4)
- تقليم مجموعة العلامات خلف العلامة N: min(tsmax, tsmin + N/4) / 2
- إرسال المفتاح التالي عند العلامة: TBD
- إرسال المفتاح التالي بعد عمر مجموعة العلامات: TBD
- استبدال الجلسة إذا تم استلام NS بعد: 3 دقائق
- أقصى انحراف للساعة: -5 دقائق إلى +2 دقيقة
- مدة مرشح إعادة التشغيل NS: 5 دقائق
- حجم الحشو: 0-15 بايت (استراتيجيات أخرى TBD)

### العمل المستقبلي

فيما يلي توصيات لتصنيف الرسائل الواردة.

### X25519 Only

على tunnel يُستخدم حصرياً مع هذا البروتوكول، قم بالتعريف كما يتم حالياً مع ElGamal/AES+SessionTags:

أولاً، تعامل مع البيانات الأولية كعلامة جلسة (session tag)، وابحث عن علامة الجلسة. إذا تم العثور عليها، فك التشفير باستخدام البيانات المخزنة المرتبطة بتلك علامة الجلسة.

إذا لم يتم العثور عليه، تعامل مع البيانات الأولية كمفتاح DH عام و nonce. قم بتنفيذ عملية DH و KDF المحدد، وحاول فك تشفير البيانات المتبقية.

### HTTP GET

في tunnel يدعم كلاً من هذا البروتوكول و ElGamal/AES+SessionTags، قم بتصنيف الرسائل الواردة كما يلي:

بسبب خلل في مواصفات ElGamal/AES+SessionTags، لا يتم حشو كتلة AES إلى طول عشوائي غير مضاعف للعدد 16. لذلك، فإن طول رسائل الجلسة الموجودة mod 16 يكون دائماً 0، وطول رسائل الجلسة الجديدة mod 16 يكون دائماً 2 (حيث أن كتلة ElGamal يبلغ طولها 514 بايت).

إذا كان باقي القسمة للطول على 16 ليس 0 أو 2، تعامل مع البيانات الأولية كـ session tag، وابحث عن session tag. إذا وُجد، قم بفك التشفير باستخدام البيانات المخزنة المرتبطة بذلك session tag.

إذا لم يتم العثور عليها، وكان طول البيانات mod 16 ليس 0 أو 2، تعامل مع البيانات الأولية كمفتاح عام DH و nonce. قم بتنفيذ عملية DH و KDF المحدد، وحاول فك تشفير البيانات المتبقية. (بناءً على مزيج حركة المرور النسبية، والتكاليف النسبية لعمليات X25519 و ElGamal DH، قد يتم تنفيذ هذه الخطوة أخيراً بدلاً من ذلك)

وإلا، إذا كان باقي القسمة على 16 يساوي 0، فتعامل مع البيانات الأولية كـ ElGamal/AES session tag، وابحث عن session tag. إذا وُجد، فك التشفير باستخدام البيانات المحفوظة المرتبطة بذلك الـ session tag.

إذا لم يتم العثور عليها، وكانت البيانات طولها على الأقل 642 (514 + 128) بايت، وكان الطول mod 16 يساوي 2، فتعامل مع البيانات الأولية كـ ElGamal block. حاول فك تشفير البيانات المتبقية.

لاحظ أنه إذا تم تحديث مواصفات ElGamal/AES+SessionTag للسماح بـ padding غير mod-16، فسيتوجب القيام بالأمور بشكل مختلف.

### HTTP POST

التطبيقات الأولية تعتمد على حركة البيانات ثنائية الاتجاه في الطبقات العليا. أي أن التطبيقات تفترض أن حركة البيانات في الاتجاه المعاكس سيتم إرسالها قريباً، مما سيفرض أي استجابة مطلوبة في طبقة ECIES.

ومع ذلك، قد تكون حركة البيانات معينة أحادية الاتجاه أو ذات عرض نطاق منخفض جداً، بحيث لا توجد حركة بيانات على طبقة أعلى لتوليد استجابة في الوقت المناسب.

استقبال رسائل NS و NSR يتطلب استجابة؛ استقبال كتل ACK Request و Next Key يتطلب أيضاً استجابة.

قد يبدأ التطبيق المتطور مؤقتًا عند استلام إحدى هذه الرسائل التي تتطلب استجابة، وينشئ استجابة "فارغة" (بدون كتلة Garlic Clove) في طبقة ECIES إذا لم يتم إرسال حركة مرور عكسية في فترة زمنية قصيرة (مثل ثانية واحدة).

قد يكون من المناسب أيضًا استخدام مهلة زمنية أقصر للاستجابات لرسائل NS و NSR، لتحويل حركة البيانات إلى رسائل ES الفعالة في أسرع وقت ممكن.

## Analysis

### مخطط البيانات القابل للرد

الحمولة الإضافية للرسالة للرسالتين الأوليين في كل اتجاه كما يلي. هذا يفترض رسالة واحدة فقط في كل اتجاه قبل الـ ACK، أو أن أي رسائل إضافية يتم إرسالها بشكل تكهني كرسائل Existing Session. إذا لم تكن هناك تأكيدات تكهنية لعلامات الجلسة المُسلمة، فإن الحمولة الإضافية أو البروتوكول القديم أعلى بكثير.

لا يُفترض وجود حشو (padding) لتحليل البروتوكول الجديد. لا يُفترض وجود leaseset مُجمَّع.

### البيانات الخام المتعددة

رسالة جلسة جديدة، نفس الشيء في كل اتجاه:

```

ElGamal block:
  514 bytes

  AES block:
  - 2 byte tag count
  - 1024 bytes of tags (32 typical)
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte clove cert, id, exp.
  - 15 byte msg cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  1143 total

  Total:
  1657 bytes
```
رسائل الجلسة الموجودة، نفس الرسائل في كل اتجاه:

```

AES block:
  - 32 byte session tag
  - 2 byte tag count
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte msg cert, id, exp.
  - 15 byte clove cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  151 total
```
```
Four message total (two each direction)
  3616 bytes overhead
```
### رسالة بيانات خام واحدة

رسالة جلسة جديدة من Alice إلى Bob:

```

- 32 byte ephemeral public key
  - 32 byte static public key
  - 16 byte Poly1305 MAC
  - 7 byte DateTime block
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  148 bytes overhead
```
رسالة رد جلسة جديدة من Bob إلى Alice:

```

- 8 byte session tag
  - 32 byte ephemeral public key
  - 16 byte Poly1305 MAC
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  117 bytes overhead
```
رسائل الجلسة الموجودة، نفسها في كل اتجاه:

```

- 8 byte session tag
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  69 bytes
```
### جلسات طويلة المدى

أربع رسائل إجمالاً (اثنتان في كل اتجاه):

```

372 bytes
  90% (approx. 10x) reduction compared to ElGamal/AES+SessionTags
```
مصافحة فقط:

```

ElGamal: 1657 + 1657 = 3314 bytes
  Ratchet: 148 _ 117 = 265 bytes
  92% (approx. 12x) reduction compared to ElGamal/AES+SessionTags
```
الإجمالي طويل المدى (تجاهل المصافحات):

```
ElGamal: 151 + 32 byte tag sent previously = 183 bytes
  Ratchet: 69 bytes
  64% (approx. 3x) reduction compared to ElGamal/AES+SessionTags
```
### CPU

TODO تحديث هذا القسم بعد استقرار الاقتراح.

العمليات التشفيرية التالية مطلوبة من كل طرف لتبادل رسائل الجلسة الجديدة والرد على الجلسة الجديدة:

- HMAC-SHA256: 3 لكل HKDF، المجموع لم يُحدد بعد
- ChaChaPoly: 2 لكل واحد
- توليد مفتاح X25519: 2 Alice، 1 Bob
- X25519 DH: 3 لكل واحد
- التحقق من التوقيع: 1 (Bob)

تحسب Alice 5 ECDHs لكل جلسة مربوطة (كحد أدنى)، 2 لكل رسالة NS إلى Bob، و3 لكل رسالة NSR من Bob.

يحسب Bob أيضًا 6 ECDHs لكل جلسة مرتبطة، 3 لكل من رسائل NS الخاصة بـ Alice، و3 لكل من رسائل NSR الخاصة به.

العمليات التشفيرية التالية مطلوبة من كل طرف لكل رسالة Existing Session:

- HKDF: 2
- ChaChaPoly: 1

### الدفاع

طول علامة الجلسة الحالي هو 32 بايت. لم نجد بعد أي مبرر لهذا الطول، ولكننا نواصل البحث في الأرشيف. الاقتراح أعلاه يحدد طول العلامة الجديد بـ 8 بايت. التحليل الذي يبرر علامة 8 بايت هو كما يلي:

يُفترض أن مولد session tag ratchet ينتج علامات عشوائية موزعة بانتظام. لا يوجد سبب تشفيري لطول معين لعلامة الجلسة. مولد session tag ratchet متزامن مع مولد symmetric key ratchet، لكنه ينتج مخرجات مستقلة عنه. قد تكون مخرجات المولدين بأطوال مختلفة.

لذلك، الاهتمام الوحيد هو تضارب علامات الجلسة (session tag collision). يُفترض أن التطبيقات لن تحاول التعامل مع التضاربات عن طريق محاولة فك التشفير مع كلا الجلستين؛ التطبيقات ستربط العلامة ببساطة إما بالجلسة السابقة أو الجديدة، وأي رسالة يتم استقبالها بتلك العلامة في الجلسة الأخرى ستُسقط بعد فشل فك التشفير.

الهدف هو اختيار طول session tag كبير بما يكفي لتقليل خطر التصادمات، بينما يكون صغيراً بما يكفي لتقليل استخدام الذاكرة.

هذا يفترض أن التطبيقات تحد من تخزين علامات الجلسة لمنع هجمات استنزاف الذاكرة. وهذا سيقلل أيضاً بشكل كبير من فرص قدرة المهاجم على إحداث تصادمات. راجع قسم اعتبارات التطبيق أدناه.

في أسوأ الحالات، افترض خادماً مشغولاً مع 64 جلسة واردة جديدة في الثانية. افترض مدة حياة session tag واردة لمدة 15 دقيقة (مثل الآن، ربما يجب تقليلها). افترض نافذة session tag واردة بحجم 32. 64 * 15 * 60 * 32 = 1,843,200 tags الحد الأقصى الحالي لـ tags الواردة في Java I2P هو 750,000 ولم يتم الوصول إليه قط حسب علمنا.

هدف حدوث تصادم واحد من كل مليون (1e-6) في علامات الجلسة يُعتبر كافياً على الأرجح. احتمالية فقدان رسالة في الطريق بسبب الازدحام أعلى بكثير من ذلك.

مرجع: https://en.wikipedia.org/wiki/Birthday_paradox قسم جدول الاحتمالات.

مع session tags بحجم 32 بايت (256 بت) فإن مساحة session tag تساوي 1.2e77. احتمالية التصادم بحتمالية 1e-18 تتطلب 4.8e29 إدخال. احتمالية التصادم بحتمالية 1e-6 تتطلب 4.8e35 إدخال. 1.8 مليون tag بحجم 32 بايت لكل منها يساوي حوالي 59 ميجابايت إجمالي.

مع session tags بحجم 16 بايت (128 بت) فإن مساحة session tag هي 3.4e38. احتمال حدوث تصادم بمعدل احتمال 1e-18 يتطلب 2.6e10 إدخالات. احتمال حدوث تصادم بمعدل احتمال 1e-6 يتطلب 2.6e16 إدخالات. 1.8 مليون tag بحجم 16 بايت لكل منها يبلغ حوالي 30 ميجابايت إجمالي.

مع session tags بحجم 8 بايت (64 بت)، مساحة session tag هي 1.8e19. احتمالية التصادم مع احتمالية 1e-18 تتطلب 6.1 إدخال. احتمالية التصادم مع احتمالية 1e-6 تتطلب 6.1e6 (6,100,000) إدخال. 1.8 مليون tag بحجم 8 بايت لكل منها يبلغ حوالي 15 ميجابايت إجمالي.

6.1 مليون علامة نشطة هو أكثر من 3 أضعاف تقديرنا للحالة الأسوأ البالغ 1.8 مليون علامة. لذا فإن احتمالية التصادم ستكون أقل من واحد في المليون. لذلك نستنتج أن علامات الجلسة بحجم 8 بايت كافية. وهذا يؤدي إلى تقليل مساحة التخزين بمقدار 4 أضعاف، بالإضافة إلى التقليل بمقدار الضعف لأن علامات الإرسال لا يتم تخزينها. لذا سيكون لدينا تقليل بمقدار 8 أضعاف في استخدام ذاكرة علامات الجلسة مقارنة بـ ElGamal/AES+SessionTags.

للحفاظ على المرونة في حال كانت هذه الافتراضات خاطئة، سنقوم بتضمين حقل طول علامة الجلسة في الخيارات، بحيث يمكن تجاوز الطول الافتراضي على أساس كل جلسة. لا نتوقع تنفيذ التفاوض الديناميكي لطول العلامة إلا إذا كان ذلك ضروريًا للغاية.

يجب على التطبيقات، كحد أدنى، أن تتعرف على تضارب علامات الجلسة (session tag collisions)، وأن تتعامل معها بطريقة مناسبة، وأن تسجل أو تحسب عدد التضاربات. رغم أنها لا تزال نادرة الحدوث للغاية، إلا أنها ستكون أكثر احتمالاً مما كانت عليه مع ElGamal/AES+SessionTags، ويمكن أن تحدث فعلياً.

### المعاملات

باستخدام ضعف الجلسات في الثانية (128) وضعف نافذة العلامة (64)، لدينا 4 أضعاف العلامات (7.4 مليون). الحد الأقصى لفرصة واحد من المليون للتصادم هو 6.1 مليون علامة. علامات 12 بايت (أو حتى 10 بايت) ستضيف هامش أمان ضخم.

ومع ذلك، هل احتمالية التصادم الواحد من المليون هدف جيد؟ كونها أكبر بكثير من احتمالية الإسقاط في الطريق لا يُعتبر مفيداً كثيراً. الهدف الإيجابي الخاطئ لـ Java's DecayingBloomFilter هو تقريباً 1 من كل 10,000، ولكن حتى 1 من كل 1000 ليس مصدر قلق كبير. من خلال تقليل الهدف إلى 1 من كل 10,000، هناك هامش كافٍ مع العلامات ذات 8 بايت.

### التصنيف

يُنشئ المرسل العلامات والمفاتيح أثناء التشغيل، لذا لا توجد حاجة للتخزين. هذا يقلل متطلبات التخزين الإجمالية إلى النصف مقارنة بـ ElGamal/AES. علامات ECIES تبلغ 8 بايت بدلاً من 32 لـ ElGamal/AES. هذا يقلل متطلبات التخزين الإجمالية بعامل 4 إضافي. مفاتيح الجلسة لكل علامة لا يتم تخزينها في المستقبِل باستثناء "الفجوات"، والتي تكون قليلة عند معدلات الفقد المعقولة.

انخفاض 33% في وقت انتهاء صلاحية العلامة يخلق توفيراً إضافياً بنسبة 33%، بافتراض أوقات جلسات قصيرة.

لذلك، إجمالي توفير المساحة مقارنة بـ ElGamal/AES هو عامل 10.7، أو 92%.

## Related Changes

### X25519 فقط

عمليات البحث في قاعدة البيانات من وجهات ECIES: راجع [الاقتراح 154](/proposals/154-ecies-lookups)، والذي تم دمجه الآن في [I2NP](/docs/specs/i2np/) للإصدار 0.9.46.

يتطلب هذا الاقتراح دعم LS2 لنشر المفتاح العام X25519 مع الـ leaseset. لا تحتاج مواصفات LS2 في [I2NP](/docs/specs/i2np/) لأي تغييرات. تم تصميم وتحديد وتنفيذ كامل الدعم في [الاقتراح 123](/proposals/123-new-netdb-entries) المنفذ في الإصدار 0.9.38.

### X25519 مشترك مع ElGamal/AES+SessionTags

لا شيء. يتطلب هذا الاقتراح دعم LS2، وخاصية يتم تعيينها في خيارات I2CP ليتم تفعيلها. لا توجد تغييرات مطلوبة على مواصفات [I2CP](/docs/specs/i2cp/). تم تصميم وتحديد وتنفيذ كل الدعم في [الاقتراح 123](/proposals/123-new-netdb-entries) المنفذ في الإصدار 0.9.38.

الخيار المطلوب لتمكين ECIES هو خاصية I2CP واحدة لـ I2CP أو BOB أو SAM أو i2ptunnel.

القيم النموذجية هي i2cp.leaseSetEncType=4 لـ ECIES فقط، أو i2cp.leaseSetEncType=4,0 لمفاتيح مزدوجة من ECIES و ElGamal.

### استجابات طبقة البروتوكول

هذا القسم منسوخ من [الاقتراح 123](/proposals/123-new-netdb-entries).

الخيار في تطابق SessionConfig:

```
  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  0: ElGamal
                                  1-3: See proposal 145
                                  4: This proposal.
```
### Create Leaseset2 Message

يتطلب هذا الاقتراح LS2 والذي مدعوم اعتبارًا من الإصدار 0.9.38. لا توجد تغييرات مطلوبة في مواصفات [I2CP](/docs/specs/i2cp/). تم تصميم وتحديد وتنفيذ جميع الدعم في [الاقتراح 123](/proposals/123-new-netdb-entries) المُنفذ في 0.9.38.

### النفقات الإضافية

أي router يدعم LS2 مع المفاتيح المزدوجة (0.9.38 أو أعلى) يجب أن يدعم الاتصال بالوجهات التي تحتوي على مفاتيح مزدوجة.

وجهات ECIES فقط ستتطلب تحديث أغلبية الـ floodfills إلى الإصدار 0.9.46 للحصول على ردود بحث مشفرة. راجع [الاقتراح 154](/proposals/154-ecies-lookups).

وجهات ECIES فقط يمكنها الاتصال فقط بالوجهات الأخرى التي تكون إما ECIES فقط، أو ذات مفتاح مزدوج.
