---
title: "مواصفات التشفير منخفض المستوى"
description: "التفاصيل المنخفضة المستوى للخوارزميات التشفيرية المستخدمة في I2P"
slug: "cryptography"
aliases:
  - "/ar/how_cryptography"
  - "/ar/how_cryptography/"
category: "التصميم"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## نظرة عامة

> **ملاحظة:** هذا المستند عفا عليه الزمن إلى حد كبير. راجع المستندات التالية للمواصفات الحالية: > - [ECIES](/docs/specs/ecies) > - [Encrypted LeaseSet](/docs/specs/encryptedleaseset) > - [NTCP2](/docs/specs/ntcp2) > - [Red25519](/docs/specs/red25519) > - [SSU2](/docs/specs/ssu2) > - [Tunnel Creation (ECIES)](/docs/specs/tunnel-creation-ecies)

تحدد هذه الصفحة التفاصيل التقنية المنخفضة المستوى للتشفير في I2P.

هناك عدة خوارزميات تشفير مستخدمة في I2P. في التصميم الأصلي لـ I2P، كان هناك نوع واحد فقط من كل نوع - خوارزمية متناظرة واحدة، وخوارزمية غير متناظرة واحدة، وخوارزمية توقيع واحدة، وخوارزمية تشويش واحدة. لم يكن هناك أي إجراء لإضافة المزيد من الخوارزميات أو الانتقال إلى أخرى ذات أمان أكبر.

في السنوات الأخيرة أضفنا إطار عمل لدعم عدة خوارزميات أساسية ومجموعاتها بطريقة متوافقة مع الإصدارات السابقة. تم تعريف العديد من خوارزميات التوقيع، مع أطوال مفاتيح وتوقيعات متنوعة، من خلال "أنواع التوقيع". كما تم تعريف مخططات التشفير من طرف إلى طرف، باستخدام مجموعة من التشفير غير المتماثل والمتماثل، ومع أطوال مفاتيح متنوعة، من خلال "أنواع التشفير".

تتضمن البروتوكولات وهياكل البيانات المختلفة في I2P حقولاً لتحديد نوع التوقيع و/أو نوع التشفير. هذه الحقول، بالإضافة إلى تعريفات الأنواع، تحدد أطوال المفاتيح والتوقيعات والعناصر الأساسية للتشفير المطلوبة لاستخدامها. تعريفات أنواع التوقيع والتشفير موجودة في [مواصفات الهياكل المشتركة](/docs/specs/common-structures).

تستخدم بروتوكولات I2P الأصلية NTCP وSSU وElGamal/AES+SessionTags مزيجاً من تشفير ElGamal غير المتماثل وتشفير AES المتماثل. تستخدم البروتوكولات الأحدث NTCP2 وECIES-X25519-AEAD-Ratchet مزيجاً من تبادل مفاتيح X25519 وتشفير ChaCha20/Poly1305 المتماثل.

- ECIES-X25519-AEAD-Ratchet قد حل محل ElGamal/AES+SessionTags.
- NTCP2 قد حل محل NTCP.
- SSU2 قد حل محل SSU.
- إنشاء tunnel بـ X25519 قد حل محل إنشاء tunnel بـ ElGamal.

## التشفير غير المتماثل

خوارزمية التشفير غير المتماثل الأصلية في I2P هي ElGamal. الخوارزمية الأحدث، المستخدمة في عدة أماكن، هي ECIES X25519 DH key exchange.

نحن في عملية نقل جميع استخدامات ElGamal إلى X25519.

تم ترحيل NTCP (مع ElGamal) إلى NTCP2 (مع X25519). يتم حالياً ترحيل ElGamal/AES+SessionTag إلى ECIES-X25519-AEAD-Ratchet.

### X25519

لتفاصيل استخدام X25519 انظر [NTCP2](/docs/specs/ntcp2) و [ECIES](/docs/specs/ecies).

### ElGamal

يُستخدم ElGamal في عدة أماكن في I2P:

- لتشفير رسائل TunnelBuild من router إلى router
- للتشفير من طرف إلى طرف (من وجهة إلى وجهة) كجزء من ElGamal/AES+SessionTag باستخدام مفتاح التشفير في LeaseSet
- لتشفير بعض مخازن واستعلامات netDb المرسلة إلى floodfill routers كجزء من ElGamal/AES+SessionTag (من وجهة إلى router أو من router إلى router).

نستخدم الأعداد الأولية الشائعة لتشفير وفك تشفير 2048 ElGamal، كما هو محدد في IETF [RFC-3526](http://tools.ietf.org/html/rfc3526). نحن نستخدم حاليًا ElGamal فقط لتشفير IV ومفتاح الجلسة في كتلة واحدة، متبوعة بالحمولة المشفرة بـ AES باستخدام ذلك المفتاح وIV.

يحتوي ElGamal غير المشفر على:

```
+----+----+----+----+----+----+----+----+
|nonz|           H(data)                |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |  data...
+----+----+----+-//
```
إن H(data) هو SHA256 للبيانات المشفرة في كتلة ElGamal، ويسبقها بايت عشوائي غير صفري. هذا البايت عشوائي فعلياً اعتباراً من الإصدار 0.9.28؛ وقبل ذلك كان دائماً 0xFF. يمكن أن يُستخدم للعلامات في المستقبل. البيانات المشفرة في الكتلة قد تصل إلى 222 بايت في الطول. نظراً لأن البيانات المشفرة قد تحتوي على عدد كبير من الأصفار إذا كان النص الواضح أصغر من 222 بايت، يُنصح بأن تقوم الطبقات العليا بحشو النص الواضح إلى 222 بايت ببيانات عشوائية. الطول الإجمالي: عادة 255 بايت.

يحتوي ElGamal المشفر على:

```
+----+----+----+----+----+----+----+----+
|  zero padding...       |              |
+----+----+----+-//-+----+              +
|                                       |
+                                       +
|       ElG encrypted part 1            |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    |   zero padding...      |         |
+----+----+----+----+-//-+----+         +
|                                       |
+                                       +
|       ElG encrypted part 2            |
~                                       ~
|                                       |
+         +----+----+----+----+----+----+
|         +
+----+----+
```
يتم إضافة أصفار في بداية كل جزء مشفر ليصبح حجمه بالضبط 257 بايت. الطول الإجمالي: 514 بايت. في الاستخدام النموذجي، تقوم الطبقات العليا بحشو البيانات الواضحة إلى 222 بايت، مما ينتج عنه كتلة غير مشفرة من 255 بايت. يتم ترميز هذا كجزأين مشفرين بحجم 256 بايت لكل منهما، وهناك بايت واحد من الحشو الصفري قبل كل جزء في هذه الطبقة.

راجع كود ElGamal [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java).

العدد الأولي المشترك هو العدد الأولي Oakley للمفاتيح 2048 بت [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3):

```
2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
```
أو كقيمة سادس عشرية:

```
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
```
استخدام 2 كمولد.

#### الأس القصير {#exponent}

في حين أن حجم الأس القياسي هو 2048 بت (256 بايت) و I2P PrivateKey هو 256 بايت كاملة، في بعض الحالات نستخدم حجم الأس القصير وهو 226 بت (28.25 بايت). هذا يجب أن يكون آمناً للاستخدام مع Oakley primes [vanOorschot1996] [BENCHMARKS].

كما أن [Koshiba2004] يدعم هذا على ما يبدو، وفقاً لهذا الموضوع في sci.crypt [SCI.CRYPT]. يتم حشو باقي PrivateKey بالأصفار.

قبل الإصدار 0.9.8، كانت جميع routers تستخدم الأس القصير. اعتباراً من الإصدار 0.9.8، تستخدم routers 64-bit x86 أساً كاملاً بحجم 2048-بت. جميع routers تستخدم الآن الأس الكامل باستثناء عدد قليل من routers على أجهزة بطيئة جداً، والتي تواصل استخدام الأس القصير بسبب المخاوف المتعلقة بحمولة المعالج. إن الانتقال إلى أس أطول لهذه المنصات يُعتبر موضوعاً للدراسة المستقبلية.

#### التقادم

يجب دراسة قابلية تعرض الشبكة لهجوم ElGamal وتأثير الانتقال إلى طول بت أطول. قد يكون من الصعب جداً جعل أي تغيير متوافقاً مع الإصدارات السابقة.

## التشفير المتماثل

خوارزمية التشفير المتماثل الأصلية في I2P هي AES. الخوارزمية الأحدث، المستخدمة في عدة أماكن، هي Authenticated Encryption with Associated Data (AEAD) ChaCha20/Poly1305.

نحن في عملية ترحيل جميع استخدامات AES إلى ChaCha20/Poly1305.

تم ترحيل NTCP (مع AES) إلى NTCP2 (مع ChaCha20/Poly1305). يتم ترحيل ElGamal/AES+SessionTag إلى ECIES-X25519-AEAD-Ratchet.

### ChaCha20/Poly1305

لتفاصيل استخدام ChaCha20/Poly1305 انظر [NTCP2](/docs/specs/ntcp2) و [ECIES](/docs/specs/ecies).

### AES

يُستخدم AES للتشفير المتماثل، في عدة حالات:

- لتشفير نقل SSU (انظر قسم "وسائل النقل") بعد تبادل مفاتيح DH
- للتشفير من طرف إلى طرف (من وجهة إلى وجهة) كجزء من ElGamal/AES+SessionTag
- لتشفير بعض مخازن netDb والاستعلامات المرسلة إلى router floodfill كجزء من ElGamal/AES+SessionTag (من الوجهة إلى router أو من router إلى router).
- لتشفير رسائل اختبار tunnel الدورية المرسلة من router إلى نفسه، عبر tunnel الخاصة به.

نستخدم AES مع مفاتيح 256 بت وكتل 128 بت في وضع CBC. الحشو المستخدم محدد في IETF [RFC-2313](http://tools.ietf.org/html/rfc2313) (PKCS#5 1.5، القسم 8.1 (لنوع الكتلة 02)). في هذه الحالة، يتكون الحشو من ثمانيات بايت مُولدة عشوائياً كاذباً لتطابق كتل 16 بايت. على وجه التحديد، راجع كود CBC [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java) وتنفيذ Cryptix AES [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java)، بالإضافة إلى الحشو الموجود في دالة ElGamalAESEngine.getPadding [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java).

#### البِلى والتقادم

سيتم دراسة قابلية تأثر الشبكة بهجمات AES وتأثير الانتقال إلى طول بت أطول. قد يكون من الصعب جداً جعل أي تغيير متوافقاً مع الإصدارات السابقة.

## التوقيعات {#sig}

يتم تعريف العديد من خوارزميات التوقيع، بأطوال مفاتيح وتوقيعات متفاوتة، بواسطة أنواع التوقيع. من السهل نسبياً إضافة المزيد من أنواع التوقيع.

EdDSA-SHA512-Ed25519 هو خوارزمية التوقيع الافتراضية الحالية. DSA، التي كانت الخوارزمية الأصلية قبل أن نضيف دعم أنواع التوقيع، لا تزال قيد الاستخدام في الشبكة.

### DSA

يتم إنشاء التوقيعات والتحقق منها باستخدام [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm) بحجم 1024 بت (L=1024, N=160)، كما هو مُطبق في [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java). تم اختيار DSA لأنه أسرع بكثير للتوقيعات من ElGamal.

#### SEED

160 بت:

```
86108236b8526e296e923a4015b4282845b572cc
```
#### عداد

```
33
```
#### العدد الأولي DSA (p)

1024 بت:

```
9C05B2AA 960D9B97 B8931963 C9CC9E8C 3026E9B8 ED92FAD0
A69CC886 D5BF8015 FCADAE31 A0AD18FA B3F01B00 A358DE23
7655C496 4AFAA2B3 37E96AD3 16B9FB1C C564B5AE C5B69A9F
F6C3E454 8707FEF8 503D91DD 8602E867 E6D35D22 35C1869C
E2479C3B 9D5401DE 04E0727F B33D6511 285D4CF2 9538D9E3
B6051F5B 22CC1C93
```
#### خارج قسمة DSA (q)

```
A5DFC28F EF4CA1E2 86744CD8 EED9D29D 684046B7
```
#### مولد DSA (g)

1024 بت:

```
0C1F4D27 D40093B4 29E962D7 223824E0 BBC47E7C 832A3923
6FC683AF 84889581 075FF908 2ED32353 D4374D73 01CDA1D2
3C431F46 98599DDA 02451824 FF369752 593647CC 3DDC197D
E985E43D 136CDCFC 6BD5409C D2F45082 1142A5E6 F8EB1C3A
B5D0484B 8129FCF1 7BCE4F7F 33321C3C B3DBB14A 905E7B2B
3E93BE47 08CBCC82
```
SigningPublicKey هو 1024 بت. SigningPrivateKey هو 160 بت.

#### الإهمال

[NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf) يوصي بحد أدنى قدره (L=2048, N=224) للاستخدام بعد عام 2010. قد يتم التخفيف من هذا إلى حد ما بواسطة "فترة التشفير"، أو العمر الافتراضي لمفتاح معين.

تم اختيار العدد الأولي في عام 2003، والشخص الذي اختار العدد (TheCrypto) لم يعد حالياً مطور I2P. وبالتالي، لا نعلم ما إذا كان العدد الأولي المُختار هو "عدد أولي قوي". إذا تم اختيار عدد أولي أكبر لأغراض مستقبلية، فيجب أن يكون هذا عدداً أولياً قوياً، وسنقوم بتوثيق عملية البناء.

## خوارزميات التوقيع الجديدة

اعتباراً من الإصدار 0.9.12، يدعم router خوارزميات توقيع إضافية أكثر أماناً من DSA بطول 1024 بت. كان الاستخدام الأول للوجهات؛ وتمت إضافة الدعم لهويات router في الإصدار 0.9.16. لا يمكن ترحيل الوجهات الموجودة من التوقيعات القديمة إلى الجديدة؛ ومع ذلك، هناك دعم لـ tunnel واحد مع وجهات متعددة، وهذا يوفر طريقة للتبديل إلى أنواع توقيع أحدث. يتم ترميز نوع التوقيع في الوجهة وهوية router، بحيث يمكن إضافة خوارزميات توقيع أو منحنيات جديدة في أي وقت.

أنواع التوقيع المدعومة حالياً هي كما يلي:

- DSA-SHA1
- ECDSA-SHA256-P256
- ECDSA-SHA384-P384 (غير مستخدم على نطاق واسع)
- ECDSA-SHA512-P521 (غير مستخدم على نطاق واسع)
- EdDSA-SHA512-Ed25519 (افتراضي اعتباراً من الإصدار 0.9.15)
- RedDSA-SHA512-Ed25519 (اعتباراً من الإصدار 0.9.39)

يتم استخدام أنواع التوقيع الإضافية في طبقة التطبيق فقط، بشكل أساسي لتوقيع والتحقق من ملفات su3. أنواع التوقيع هذه كما يلي:

- RSA-SHA256-2048 (غير مستخدم على نطاق واسع)
- RSA-SHA384-3072 (غير مستخدم على نطاق واسع)
- RSA-SHA512-4096
- EdDSA-SHA512-Ed25519ph (اعتباراً من الإصدار 0.9.25؛ غير مستخدم على نطاق واسع)

### ECDSA

يستخدم ECDSA المنحنيات المعيارية من NIST وخوارزميات التشفير المعيارية SHA-2.

قمنا بترحيل الوجهات الجديدة إلى ECDSA-SHA256-P256 في الإطار الزمني للإصدارات 0.9.16 - 0.9.19. الاستخدام لهويات الـ Router مدعوم اعتباراً من الإصدار 0.9.16 وحدث ترحيل الـ routers الموجودة في عام 2015.

### RSA

RSA PKCS#1 v1.5 القياسي (RFC 2313) مع الأس العام F4 = 65537.

يُستخدم RSA الآن لتوقيع جميع المحتوى الموثوق خارج الشبكة، بما في ذلك تحديثات router والـ reseeding والإضافات والأخبار. التوقيعات مضمنة في تنسيق "su3" [UPDATES]. يُوصى بمفاتيح 4096 بت وتستخدمها جميع الموقعين المعروفين. RSA غير مستخدم، أو مخطط لاستخدامه، في أي Destinations داخل الشبكة أو Router Identities.

### EdDSA 25519

EdDSA قياسي باستخدام منحنى 25519 وهاشات SHA-2 قياسية بحجم 512 بت.

مدعوم اعتباراً من الإصدار 0.9.15.

تم ترحيل الوجهات وهويات الـ router في أواخر عام 2015.

### RedDSA 25519

EdDSA قياسي يستخدم منحنى 25519 وهاش SHA-2 قياسي بحجم 512 بت، ولكن مع مفاتيح خاصة مختلفة، وتعديلات طفيفة على التوقيع. لـ leaseSet المشفرة. راجع [EncryptedLeaseSet](/docs/specs/encryptedleaseset) و [Red25519](/docs/specs/red25519) للتفاصيل.

مدعوم اعتباراً من الإصدار 0.9.39.

## الهاشات

تُستخدم الـ hashes في خوارزميات التوقيع وكمفاتيح في شبكة DHT الخاصة بالشبكة.

خوارزميات التوقيع الأقدم تستخدم SHA1 و SHA256. خوارزميات التوقيع الأحدث تستخدم SHA512. جدول التجمية الموزع (DHT) يستخدم SHA256.

### SHA256

هاشات DHT داخل I2P هي SHA256 القياسية.

#### التقادم

يجب دراسة قابلية تأثر الشبكة لهجوم SHA-256 وتأثير الانتقال إلى hash أطول. قد يكون من الصعب جداً جعل أي تغيير متوافقاً مع الإصدارات السابقة.

## وسائل النقل

في أدنى طبقة من طبقات البروتوكول، يتم حماية الاتصال بين router إلى router من خلال أمان طبقة النقل.

تستخدم اتصالات NTCP2 خوارزمية X25519 Diffie-Hellman والتشفير المُصادق عليه ChaCha20/Poly1305.

تستخدم SSU وبروتوكولات النقل المهجورة NTCP تبادل مفاتيح Diffie-Hellman بحجم 256 بايت (2048 بت) باستخدام نفس العدد الأولي المشترك والمولد المحدد أعلاه لـ ElGamal، متبوعًا بتشفير AES متماثل كما هو موضح أعلاه.

من المخطط أن يتم ترحيل SSU إلى SSU2 (مع X25519 و ChaCha20/Poly1305).

جميع وسائل النقل توفر السرية التامة للأمام [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy) على روابط النقل.

### اتصالات NTCP2 {#tcp}

تستخدم اتصالات NTCP2 تبادل المفاتيح X25519 Diffie-Hellman والتشفير المصادق عليه ChaCha20/Poly1305، وإطار عمل بروتوكول Noise [Noise](https://noiseprotocol.org/noise.html).

راجع مواصفات NTCP2 [NTCP2](/docs/specs/ntcp2) للتفاصيل والمراجع.

### اتصالات UDP {#udp}

SSU (نقل UDP) يقوم بتشفير كل حزمة باستخدام AES256/CBC مع IV صريح و MAC (HMAC-MD5-128) بعد الاتفاق على مفتاح جلسة مؤقت من خلال تبادل Diffie-Hellman بحجم 2048 بت، ومصادقة محطة إلى محطة باستخدام مفتاح DSA الخاص بـ router الآخر، بالإضافة إلى أن كل رسالة شبكة لها hash خاص بها للتحقق من السلامة المحلية.

راجع مواصفات SSU للتفاصيل.

تحذير - يبدو أن HMAC-MD5-128 المستخدم في SSU الخاص بـ I2P غير معياري. على ما يبدو، استخدمت نسخة مبكرة من SSU الخوارزمية HMAC-SHA256، ثم تم التبديل إلى MD5-128 لأسباب تتعلق بالأداء، لكن تم ترك حجم المخزن المؤقت 32-byte كما هو. راجع HMACGenerator.java وملاحظات الحالة بتاريخ 2005-07-05 للتفاصيل.

### اتصالات NTCP

لم يعد NTCP مستخدماً، تم استبداله بـ NTCP2.

تم التفاوض على اتصالات NTCP باستخدام تطبيق Diffie-Hellman بحجم 2048 بت، مع استخدام هوية الـ router للمضي قدماً في اتفاقية محطة إلى محطة، متبوعة ببعض الحقول المشفرة الخاصة بالبروتوكول، مع تشفير جميع البيانات اللاحقة باستخدام AES (كما هو موضح أعلاه). السبب الأساسي لإجراء تفاوض DH بدلاً من استخدام ElGamalAES+SessionTag هو أنه يوفر "السرية التامة للأمام" [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)، بينما ElGamalAES+SessionTag لا يوفر ذلك.

## المراجع

- [BENCHMARKS](https://web.archive.org/web/20080423000000*/http://www.eskimo.com/~weidai/benchmarks.html) - معايير أداء Crypto++، متاحة أصلاً في http://www.eskimo.com/~weidai/benchmarks.html (لم تعد تعمل الآن)، محفوظة من http://www.archive.org/، بتاريخ 23 أبريل 2008.
- [Common](/docs/specs/common-structures) - مواصفات البنى المشتركة
- [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java)
- [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java)
- [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm)
- [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java)
- [ECIES](/docs/specs/ecies)
- [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java)
- [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset)
- [Koshiba2004](http://www.springerlink.com/content/2jry7cftp5bpdghm/) - Koshiba & Kurosawa. Short Exponent Diffie-Hellman Problems. PKC 2004, LNCS 2947, pp. 173-186
- [NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf)
- [Noise](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2)
- [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)
- [Red25519](/docs/specs/red25519)
- [RFC-2313](http://tools.ietf.org/html/rfc2313)
- [RFC-3526](http://tools.ietf.org/html/rfc3526)
- [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3)
- [SCI.CRYPT](https://groups.google.com/forum/#!topic/sci.crypt/GFWl76dBZnc)
- [SHA-2](https://en.wikipedia.org/wiki/SHA-2)
- [SSU2](/docs/specs/ssu2)
- [UPDATES](/docs/specs/updates)
- [vanOorschot1996](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.14.5952&rep=rep1&type=pdf) - van Oorschot, Weiner. On Diffie-Hellman Key Agreement with Short Exponents. EuroCrypt '96
