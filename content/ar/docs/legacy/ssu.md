---
title: "SSU (بروتوكول UDP آمن وشبه موثوق)"
description: "مواصفات بروتوكول النقل UDP الأصلي (مهجور، تم استبداله بـ SSU2)"
slug: "ssu"
aliases:
  - "/ar/docs/transport/ssu"
  - "/ar/docs/transport/ssu/"
  - "/ar/docs/transports/ssu"
  - "/ar/docs/transports/ssu/"
  - "/ar/docs/specs/ssu-spec"
  - "/ar/docs/specs/ssu-spec/"
  - "/ar/udp_spec"
  - "/ar/udp_spec/"
category: "طرق النقل"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
---

## نظرة عامة

مهجور - تم استبدال SSU بـ SSU2. تم إزالة دعم SSU من i2pd في الإصدار 2.44.0 (API 0.9.56) 2022-11. تم إزالة دعم SSU من Java I2P في الإصدار 2.4.0 (API 0.9.61) 2023-12.

راجع [نظرة عامة على SSU](/docs/transport/ssu/) للمزيد من المعلومات.

## تبادل مفاتيح DH {#dh}

يتم وصف تبادل المفاتيح الأولي DH بطول 2048 بت في [صفحة مفاتيح SSU](/docs/transport/ssu/#keys). يستخدم هذا التبادل نفس العدد الأولي المشترك المستخدم لـ [تشفير ElGamal](/docs/specs/cryptography/#elgamal) في I2P.

## رأس الرسالة {#header}

تبدأ جميع حزم UDP بـ MAC بحجم 16 بايت (كود مصادقة الرسالة) و IV بحجم 16 بايت (متجه التهيئة) متبوعة بحمولة متغيرة الحجم مشفرة بالمفتاح المناسب. الـ MAC المستخدم هو HMAC-MD5، مقطوع إلى 16 بايت، بينما المفتاح هو مفتاح AES256 كامل بحجم 32 بايت. البنية المحددة لـ MAC هي أول 16 بايت من:

```
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)
```
حيث '+' يعني الإلحاق و '^' يعني العملية المنطقية الحصرية (exclusive-or).

يتم إنشاء الـ IV بشكل عشوائي لكل حزمة. الـ encryptedPayload هو النسخة المشفرة من الرسالة التي تبدأ ببايت العلامة (التشفير ثم الـ MAC). الـ payloadLength المستخدم في الـ MAC هو عدد صحيح غير موقع من 2 بايت، big endian. لاحظ أن الـ protocolVersion هو 0، لذا فإن العملية exclusive-or لا تؤثر. الـ macKey إما أن يكون مفتاح المقدمة أو يتم بناؤه من مفتاح الـ DH المتبادل (انظر التفاصيل أدناه)، كما هو محدد لكل رسالة أدناه.

**تحذير** - إن HMAC-MD5-128 المستخدم هنا غير معياري، راجع [تفاصيل HMAC](/docs/specs/cryptography/#udp) للمزيد من المعلومات.

الحمولة نفسها (أي الرسالة التي تبدأ ببايت العلم) مُشفرة بـ AES256/CBC باستخدام الـ IV والـ sessionKey، مع معالجة منع الإعادة ضمن محتواها، كما هو موضح أدناه.

إن protocolVersion هو عدد صحيح غير موقع من 2 بايت، big endian، وهو مضبوط حالياً على 0. النظراء الذين يستخدمون إصدار بروتوكول مختلف لن يتمكنوا من التواصل مع هذا النظير، رغم أن الإصدارات السابقة التي لا تستخدم هذا العلم يمكنها ذلك.

يتم استخدام العملية الحصرية OR لـ ((netid - 2) << 8) لتحديد الاتصالات عبر الشبكات بسرعة. إن netid هو عدد صحيح بدون إشارة من 2 بايت، big endian، وهو مضبوط حالياً على 2. اعتباراً من الإصدار 0.9.42. راجع المقترح 147 لمزيد من المعلومات. نظراً لأن معرف الشبكة الحالي هو 2، فهذه عملية لا تأثير لها على الشبكة الحالية وهي متوافقة مع الإصدارات السابقة. أي اتصالات من شبكات الاختبار يجب أن يكون لها معرف مختلف وستفشل في HMAC.

### مواصفات HMAC

- الحشو الداخلي: 0x36...
- الحشو الخارجي: 0x5C...
- المفتاح: 32 بايت
- دالة هاش الملخص: MD5، 16 بايت
- حجم الكتلة: 64 بايت
- حجم MAC: 16 بايت
- أمثلة تنفيذ C:
  - hmac.h في [i2pd](https://github.com/PurpleI2P/i2pd)
  - I2PHMAC.cpp في [i2pcpp](http://git.repo.i2p/w/i2pcpp.git)
- مثال تنفيذ Java:
  - I2PHMac.java في [I2P](https://github.com/i2p/i2p.i2p)

### تفاصيل مفتاح الجلسة

يتم إنشاء مفتاح الجلسة المكون من 32 بايت كما يلي:

1. خذ مفتاح DH المتبادل، ممثلاً كمصفوفة بايت BigInteger موجبة بأقل طول
   (مكمل الاثنين big-endian)
2. إذا كان البت الأكثر أهمية هو 1 (أي array[0] & 0x80 != 0)،
   أضف بايت 0x00 في المقدمة، كما في تمثيل Java's BigInteger.toByteArray()
3. إذا كانت مصفوفة البايت أكبر من أو تساوي 32 بايت، استخدم
   أول (الأكثر أهمية) 32 بايت
4. إذا كانت مصفوفة البايت أقل من 32 بايت، أضف بايتات 0x00 لتمديدها
   إلى 32 بايت. *من غير المحتمل جداً - انظر الملاحظة أدناه.*

### تفاصيل مفتاح MAC

يتم إنشاء مفتاح MAC المكون من 32 بايت كما يلي:

1. خذ مصفوفة بايتات مفتاح DH المتبادل، مع إضافة بايت 0x00 في المقدمة إذا لزم الأمر، من الخطوة 2 في تفاصيل مفتاح الجلسة أعلاه.
2. إذا كانت مصفوفة البايتات تلك أكبر من أو تساوي 64 بايت، فإن مفتاح MAC هو البايتات 33-64 من تلك المصفوفة.
3. إذا كانت مصفوفة البايتات تلك أقل من 64 بايت، فإن مفتاح MAC هو hash SHA-256 لتلك المصفوفة. *اعتباراً من الإصدار 0.9.8. انظر الملاحظة أدناه.*

#### ملاحظة مهمة

الكود قبل الإصدار 0.9.8 كان معطلاً ولم يتعامل بشكل صحيح مع مصفوفات بايت مفاتيح DH بين 32 و 63 بايت (الخطوتان 3 و 4 أعلاه) وسيفشل الاتصال. نظراً لأن هذه الحالات لم تعمل مطلقاً، تم إعادة تعريفها كما هو موضح أعلاه للإصدار 0.9.8، وتم إعادة تعريف حالة 0-32 بايت أيضاً. نظراً لأن مفتاح DH المتبادل الاسمي هو 256 بايت، فإن احتمالات أن يكون التمثيل الأدنى أقل من 64 بايت ضئيلة جداً.

### تنسيق الترويسة

داخل الحمولة المُشفرة بـ AES، هناك بنية مشتركة أساسية للرسائل المختلفة - علامة بايت واحد وطابع زمني للإرسال من أربعة بايتات (ثوان منذ unix epoch).

تنسيق الرأس (header) هو:

```
Header: 37+ bytes
  Encryption starts with the flag byte.
  +----+----+----+----+----+----+----+----+
  |                  MAC                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                   IV                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |flag|        time       |              |
  +----+----+----+----+----+              +
  | keying material (optional)            |
  +                                       +
  |                                       |
  ~                                       ~
  |                                       |
  +                        +----+----+----+
  |                        |#opt|         |
  +----+----+----+----+----+----+         +
  | #opt extended option bytes (optional) |
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
```
يحتوي بايت العلامة على حقول البت التالية:

```
Bit order: 76543210 (bit 7 is MSB)

  bits 7-4: payload type
     bit 3: If 1, rekey data is included. Always 0, unimplemented
     bit 2: If 1, extended options are included. Always 0 before release
            0.9.24.
  bits 1-0: reserved, set to 0 for compatibility with future uses
```
بدون إعادة تكوين المفاتيح والخيارات الموسعة، يبلغ حجم الرأس 37 بايت.

### إعادة إنشاء المفاتيح {#rekey}

إذا تم تعيين علامة إعادة المفتاح، فإن 64 بايت من مواد المفاتيح تتبع الطابع الزمني.

عند إعادة إنشاء المفاتيح، يتم تمرير أول 32 بايت من مادة المفاتيح إلى SHA256 لإنتاج مفتاح MAC الجديد، والـ 32 بايت التالية يتم تمريرها إلى SHA256 لإنتاج مفتاح الجلسة الجديد، رغم أن المفاتيح لا تُستخدم فوراً. يجب على الطرف الآخر أيضاً أن يرد بتعيين علامة إعادة المفاتيح ونفس مادة المفاتيح تلك. بمجرد أن يقوم كلا الطرفين بإرسال واستقبال تلك القيم، يجب استخدام المفاتيح الجديدة والتخلص من المفاتيح السابقة. قد يكون من المفيد الاحتفاظ بالمفاتيح القديمة لفترة وجيزة، للتعامل مع فقدان الحزم وإعادة ترتيبها.

ملاحظة: إعادة إنشاء المفاتيح غير مُنفذة حالياً.

### الخيارات الموسعة {#extend}

إذا تم تعيين علامة الخيارات الممتدة، يتم إلحاق قيمة حجم الخيار بايت واحد، متبوعة بعدد البايتات المقابل لخيارات ممتدة. لطالما كانت الخيارات الممتدة جزءًا من المواصفات، لكنها لم تُطبق حتى الإصدار 0.9.24. عند وجودها، يكون تنسيق الخيار خاصًا بنوع الرسالة. راجع وثائق الرسائل أدناه لمعرفة ما إذا كانت الخيارات الممتدة متوقعة للرسالة المعطاة، والتنسيق المحدد. بينما كانت router الـ Java تتعرف دائمًا على العلامة وطول الخيارات، فإن التطبيقات الأخرى لم تفعل ذلك. لذلك، لا ترسل خيارات ممتدة إلى router أقدم من الإصدار 0.9.24.

## الحشو

جميع الرسائل تحتوي على 0 أو أكثر من بايتات الحشو. يجب أن تكون كل رسالة محشوة لحدود 16 بايت، كما هو مطلوب بواسطة [طبقة تشفير AES256](/docs/specs/cryptography/#AES).

حتى الإصدار 0.9.7، كانت الرسائل تُحشى فقط إلى حدود الـ 16 بايت التالية، والرسائل التي ليست من مضاعفات 16 بايت يمكن أن تكون غير صالحة.

اعتباراً من الإصدار 0.9.7، يمكن حشو الرسائل إلى أي طول طالما تم احترام MTU الحالي. أي بايتات حشو إضافية من 1-15 بايت خارج الكتلة الأخيرة من 16 بايت لا يمكن تشفيرها أو فك تشفيرها وسيتم تجاهلها. ومع ذلك، يتم تضمين الطول الكامل وكل الحشو في حساب MAC.

اعتباراً من الإصدار 0.9.8، الرسائل المُرسلة ليست بالضرورة مضاعفات لـ 16 بايت. رسالة SessionConfirmed هي استثناء، انظر أدناه.

## المفاتيح

التوقيعات في رسائل SessionCreated و SessionConfirmed يتم توليدها باستخدام [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) من [RouterIdentity](/docs/specs/common-structures/#routeridentity) والذي يتم توزيعه خارج النطاق من خلال النشر في قاعدة بيانات الشبكة، و [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) المرتبط به.

حتى الإصدار 0.9.15، كانت خوارزمية التوقيع دائماً DSA، مع توقيع بحجم 40 بايت.

اعتباراً من الإصدار 0.9.16، يمكن تحديد خوارزمية التوقيع بواسطة [KeyCertificate](/docs/specs/common-structures/#key-certificates) في [RouterIdentity](/docs/specs/common-structures/#routeridentity) الخاص بـ Bob.

كل من مفاتيح التقديم ومفاتيح الجلسة هي 32 بايت، وهي معرّفة بواسطة مواصفات الهياكل المشتركة [SessionKey](/docs/specs/common-structures/#sessionkey). المفتاح المستخدم لـ MAC والتشفير محدد لكل رسالة أدناه.

يتم تسليم مفاتيح المقدمة من خلال قناة خارجية (قاعدة بيانات الشبكة)، حيث كانت تقليدياً مطابقة لـ router Hash حتى الإصدار 0.9.47، ولكن قد تكون عشوائية اعتباراً من الإصدار 0.9.48.

## ملاحظات

### IPv6

تسمح مواصفات البروتوكول بعناوين IPv4 بحجم 4 بايت وعناوين IPv6 بحجم 16 بايت. SSU-over-IPv6 مدعوم اعتبارًا من الإصدار 0.9.8. راجع وثائق الرسائل الفردية أدناه للحصول على تفاصيل حول دعم IPv6.

### الطوابع الزمنية {#time}

بينما تستخدم معظم أجزاء I2P طوابع زمنية [Date](/docs/specs/common-structures/#date) بحجم 8 بايت مع دقة بالميلي ثانية، يستخدم SSU طوابع زمنية من عدد صحيح غير موقع بحجم 4 بايت مع دقة ثانية واحدة. نظراً لأن هذه القيم غير موقعة، فإنها لن تعود للصفر حتى فبراير 2106.

## الرسائل

يوجد 10 رسائل (أنواع البيانات المفيدة) معرّفة:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Notes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionrequest">SessionRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessioncreated">SessionCreated</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionconfirmed">SessionConfirmed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayrequest">RelayRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayresponse">RelayResponse</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayintro">RelayIntro</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#peertest">PeerTest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessiondestroyed">SessionDestroyed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Implemented as of 0.8.9</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#holepunch">HolePunch</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### SessionRequest (النوع 0) {#sessionrequest}

هذه هي الرسالة الأولى المرسلة لإنشاء جلسة.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte X, to begin the DH agreement; 1 byte IP address size; that many bytes representation of Bob's IP address; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
</table>
تنسيق الرسالة:

```
+----+----+----+----+----+----+----+----+
|         X, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
الحجم النموذجي بما في ذلك الرأس، في التنفيذ الحالي: 304 (IPv4) أو 320 (IPv6) بايت (قبل حشو non-mod-16)

#### الخيارات المتقدمة

ملاحظة: تم تنفيذه في الإصدار 0.9.24.

- الحد الأدنى للطول: 3 (بايت طول الخيار + 2 بايت)
- طول الخيار: 2 كحد أدنى
- 2 بايت للأعلام:

```
Bit order: 15...76543210 (bit 15 is MSB)

      bit 0: 1 for Alice to request a relay tag from Bob in the
             SessionCreated response, 0 if Alice does not need a relay tag.
             Note that "1" is the default if no extended options are present
  bits 15-1: unused, set to 0 for compatibility with future uses
```
#### ملاحظات

- عناوين IPv4 و IPv6 مدعومة.
- البيانات غير المفسرة يمكن أن تُستخدم في المستقبل للتحديات.

### SessionCreated (النوع 1) {#sessioncreated}

هذا هو الرد على [SessionRequest](#sessionrequest).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte Y, to complete the DH agreement; 1 byte IP address size; that many bytes representation of Alice's IP address; 2 byte Alice's port number; 4 byte relay (introduction) tag which Alice can publish (else 0x00000000); 4 byte timestamp (seconds from the epoch) for use in the DSA signature; Bob's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Bob's signed on time), encrypted with another layer of encryption using the negotiated sessionKey. The IV is reused here. See notes for length information.; 0-15 bytes of padding of the signature, using random data, to a multiple of 16 bytes, so that the signature + padding may be encrypted with an additional layer of encryption using the negotiated session key as part of the DSA block.; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, with an additional layer of encryption over the 40 byte signature and the following 8 bytes padding.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey</td>
</tr>
</table>
تنسيق الرسالة:

```
+----+----+----+----+----+----+----+----+
|         Y, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| Port (A)| public relay tag  |  signed
+----+----+----+----+----+----+----+----+
  on time |                             |
+----+----+                             +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+         +----+----+----+----+----+----+
|         |   (0-15 bytes of padding) 
+----+----+----+----+----+----+----+----+
          |                             |
+----+----+                             +
|           arbitrary amount            |
~        of uninterpreted data          ~
~                .  .  .                ~
```
الحجم النموذجي بما يشمل الرأس، في التطبيق الحالي: 368 بايت (IPv4 أو IPv6) (قبل الحشو غير المضاعف للعدد 16)

#### ملاحظات

- عناوين IPv4 و IPv6 مدعومة.
- إذا كان relay tag غير صفر، فإن Bob يعرض أن يعمل كـ introducer لـ
  Alice. يمكن لـ Alice لاحقاً نشر عنوان Bob و relay tag في
  قاعدة بيانات الشبكة.
- للتوقيع، يجب على Bob استخدام منفذه الخارجي، حيث أن هذا ما ستستخدمه Alice للتحقق. إذا كان NAT/firewall الخاص بـ Bob قد ربط منفذه الداخلي بمنفذ خارجي مختلف، وكان Bob غير مدرك لذلك، فإن التحقق من قبل Alice سيفشل.
- راجع قسم [المفاتيح](#keys) أعلاه للحصول على تفاصيل حول التواقيع. Alice لديها بالفعل مفتاح التوقيع العام الخاص بـ Bob، من قاعدة بيانات الشبكة.
- حتى الإصدار 0.9.15، كان التوقيع دائماً توقيع DSA بحجم 40 بايت وكانت الحشوة دائماً 8 بايت. اعتباراً من الإصدار 0.9.16، نوع التوقيع وطوله مستنبطان من نوع [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) في [RouterIdentity](/docs/specs/common-structures/#routeridentity) الخاص بـ Bob. الحشوة حسب الحاجة لتكون مضاعف للعدد 16 بايت.
- هذه هي الرسالة الوحيدة التي تستخدم مفتاح intro الخاص بالمرسل. جميع الرسائل الأخرى تستخدم مفتاح intro الخاص بالمستقبل أو مفتاح الجلسة المؤسس.
- وقت التوقيع يبدو غير مستخدم أو غير محقق منه في التنفيذ الحالي.
- البيانات غير المفسرة يمكن أن تُستخدم في المستقبل للتحديات.
- الخيارات الموسعة في الرأس: غير متوقعة، غير محددة.

### SessionConfirmed (النوع 2) {#sessionconfirmed}

هذا هو الرد على رسالة [SessionCreated](#sessioncreated) والخطوة الأخيرة في إنشاء جلسة. قد تكون هناك حاجة لعدة رسائل SessionConfirmed إذا كان يجب تقسيم هوية الـ router إلى أجزاء.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte identity fragment info (bits 7-4: current identity fragment # 0-14; bits 3-0: total identity fragments (F) 1-15); 2 byte size of the current identity fragment; that many byte fragment of Alice's <a href="/docs/specs/common-structures/#routeridentity">RouterIdentity</a>; After the last identity fragment only: 4 byte signed-on time; N bytes padding, currently uninterpreted; After the last identity fragment only: The remaining bytes contain Alice's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Alice's signed on time). See notes for length information.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey, as generated from the DH exchange</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key, as generated from the DH exchange</td>
</tr>
</table>
**Fragment 0 خلال F-2** (فقط إذا كان F > 1؛ غير مستخدم حالياً، انظر الملاحظات أدناه):

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|      fragment of Alice's full         |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
**الجزء F-1 (الجزء الأخير أو الوحيد):**

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|     last fragment of Alice's full     |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|  signed on time   |                   |
+----+----+----+----+                   +
|  arbitrary amount of uninterpreted    |
~      data, until the signature at     ~
~       end of the current packet       ~
|  Packet length must be mult. of 16    |
+----+----+----+----+----+----+----+----+
+                                       +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
الحجم النموذجي متضمناً الرأس، في التنفيذ الحالي: 512 بايت (مع توقيع Ed25519) أو 480 بايت (مع توقيع DSA-SHA1) (قبل الحشو غير mod-16)

#### ملاحظات

- في التطبيق الحالي، الحد الأقصى لحجم الجزء هو 512 بايت. يجب توسيع هذا ليتمكن من التعامل مع التوقيعات الأطول بدون تجزئة. التطبيق الحالي لا يعالج بشكل صحيح التوقيعات المقسمة عبر جزأين.
- [RouterIdentity](/docs/specs/common-structures/#routeridentity) النموذجي يبلغ 387 بايت، لذا لا تكون التجزئة ضرورية أبداً. إذا قام التشفير الجديد بتوسيع حجم RouterIdentity، فيجب اختبار نظام التجزئة بعناية.
- لا توجد آلية لطلب أو إعادة توصيل الأجزاء المفقودة.
- يجب تعيين حقل إجمالي الأجزاء F بشكل متطابق في جميع الأجزاء.
- راجع قسم [المفاتيح](#keys) أعلاه للحصول على تفاصيل حول توقيعات DSA.
- يبدو أن وقت التوقيع غير مستخدم أو غير مُتحقق منه في التطبيق الحالي.
- بما أن التوقيع في النهاية، فإن الحشو في الحزمة الأخيرة أو الوحيدة يجب أن يملأ إجمالي الحزمة إلى مضاعف من 16 بايت، وإلا فلن يتم فك تشفير التوقيع بشكل صحيح. هذا يختلف عن جميع أنواع الرسائل الأخرى، حيث يكون الحشو في النهاية.
- حتى الإصدار 0.9.15، كان التوقيع دائماً توقيع DSA بحجم 40 بايت. اعتباراً من الإصدار 0.9.16، نوع التوقيع وطوله مُضمنان في نوع [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) في [RouterIdentity](/docs/specs/common-structures/#routeridentity) الخاص بـ Alice. الحشو كما هو ضروري إلى مضاعف من 16 بايت.
- الخيارات الموسعة في الترويسة: غير متوقعة، غير محددة.

### SessionDestroyed (النوع 8) {#sessiondestroyed}

تم تنفيذ رسالة SessionDestroyed (الاستقبال فقط) في الإصدار 0.8.1، ويتم إرسالها اعتباراً من الإصدار 0.8.9.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob or Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">none</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
هذه الرسالة لا تحتوي على أي بيانات. الحجم النموذجي بما في ذلك الرأس، في التنفيذ الحالي: 48 بايت (قبل الحشو غير المضاعف لـ 16)

#### ملاحظات

- رسائل التدمير المستلمة مع مفتاح التعريف الخاص بالمرسل أو المستقبل سيتم تجاهلها.
- الخيارات الموسعة في الرأس: غير متوقعة، غير محددة.

### RelayRequest (النوع 3) {#relayrequest}

هذه هي الرسالة الأولى المرسلة من Alice إلى Bob لطلب التعريف بـ Charlie.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte relay (introduction) tag, nonzero, as received by Alice in the SessionCreated message from Bob; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes to be relayed to Charlie in the intro; Alice's 32-byte introduction key (so Bob can reply with Charlie's info); 4 byte nonce of Alice's relay request; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
تنسيق الرسالة:

```
+----+----+----+----+----+----+----+----+
|      relay tag    |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|size| challenge bytes   |
+----+----+----+----+                   +
|      to be delivered to Charlie       |
+----+----+----+----+----+----+----+----+
| Alice's intro key                     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|       nonce       |                   |
+----+----+----+----+                   +
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
الحجم النموذجي شاملاً الرأس، في التنفيذ الحالي: 96 بايت (لا يتضمن عنوان IP الخاص بـ Alice) أو 112 بايت (يتضمن عنوان IP الخاص بـ Alice المكون من 4 بايت) (قبل الحشو غير المتوافق مع مضاعفات الـ 16)

#### ملاحظات

- عنوان IP يُدرج فقط إذا كان مختلفاً عن عنوان المصدر والمنفذ في الحزمة.
- يمكن إرسال هذه الرسالة عبر IPv4 أو IPv6.
  إذا كانت الرسالة عبر IPv6 لتقديم IPv4،
  أو (اعتباراً من الإصدار 0.9.50) عبر IPv4 لتقديم IPv6،
  يجب على Alice أن تتضمن عنوان وميناء التقديم الخاص بها.
  هذا مدعوم اعتباراً من الإصدار 0.9.50.
- إذا قامت Alice بتضمين عنوانها/منفذها، قد يقوم Bob بإجراء تحقق إضافي
  قبل المتابعة.
  - قبل الإصدار 0.9.24، رفض Java I2P أي عنوان أو منفذ كان
    مختلفاً عن الاتصال.
- التحدي غير مُنفّذ، حجم التحدي دائماً صفر
- الترحيل لـ IPv6 مدعوم اعتباراً من الإصدار 0.9.50.
- قبل الإصدار 0.9.12، كان مفتاح التقديم الخاص بـ Bob يُستخدم دائماً. اعتباراً من الإصدار
  0.9.12، يُستخدم مفتاح الجلسة إذا كانت هناك جلسة مُثبتة بين
  Alice و Bob. في الممارسة، يجب أن تكون هناك جلسة مُثبتة، حيث أن Alice
  ستحصل فقط على المعرّف الفريد (علامة التقديم) من رسالة إنشاء الجلسة،
  و Bob سيضع علامة التقديم كغير صالحة بمجرد تدمير الجلسة.
- الخيارات المُوسّعة في الرأس: غير متوقعة، غير مُعرّفة.

### RelayResponse (النوع 4) {#relayresponse}

هذه هي الاستجابة لـ [RelayRequest](#relayrequest) ويتم إرسالها من Bob إلى Alice.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Charlie's IP address; 2 byte Charlie's port number; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte Alice's port number; 4 byte nonce sent by Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
تنسيق الرسالة:

```
+----+----+----+----+----+----+----+----+
|size|    Charlie IP     | Port (C)|size|
+----+----+----+----+----+----+----+----+
|    Alice IP       | Port (A)|  nonce
+----+----+----+----+----+----+----+----+
          |   arbitrary amount of       |
+----+----+                             +
|          uninterpreted data           |
~                .  .  .                ~
```
الحجم النموذجي بما في ذلك الرأس، في التطبيق الحالي: 64 (Alice IPv4) أو 80 (Alice IPv6) بايت (قبل حشو non-mod-16)

#### ملاحظات

- يمكن إرسال هذه الرسالة عبر IPv4 أو IPv6.
- عنوان IP/المنفذ الخاص بـ Alice هما العنوان/المنفذ الظاهريان اللذان استقبل Bob عليهما الـ RelayRequest (وليس بالضرورة العنوان الذي ضمّنته Alice في الـ RelayRequest)، وقد يكونان IPv4 أو IPv6. تتجاهل Alice حاليًا هذين القيمتين عند الاستقبال.
- عنوان IP الخاص بـ Charlie قد يكون IPv4، أو كما هو الحال اعتبارًا من الإصدار 0.9.50، IPv6، حيث أن هذا هو العنوان الذي ستُرسل Alice إليه الـ SessionRequest بعد الـ Hole Punch.
- يُدعم التتابع (Relaying) لـ IPv6 اعتبارًا من الإصدار 0.9.50.
- قبل الإصدار 0.9.12، كان يُستخدم دائمًا مفتاح التعريف الخاص بـ Alice. اعتبارًا من الإصدار 0.9.12، يُستخدم مفتاح الجلسة إذا كانت هناك جلسة مُنشأة بين Alice و Bob.
- الخيارات الموسّعة في الرأس: غير متوقعة، غير محددة.

### RelayIntro (النوع 5) {#relayintro}

هذه هي المقدمة لأليس، والتي تم إرسالها من بوب إلى تشارلي.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Charlie</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes relayed from Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie MAC Key</td>
</tr>
</table>
تنسيق الرسالة:

```
+----+----+----+----+----+----+----+----+
|size|     Alice IP      | Port (A)|size|
+----+----+----+----+----+----+----+----+
|      that many bytes of challenge     |
+                                       +
|        data relayed from Alice        |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
الحجم النموذجي بما في ذلك الرأس، في التنفيذ الحالي: 48 بايت (قبل الحشو غير المضاعف لـ 16)

#### ملاحظات

- بالنسبة لـ IPv4، عنوان IP الخاص بـ Alice يكون دائماً 4 بايت، لأن Alice تحاول الاتصال بـ Charlie عبر IPv4.
  اعتباراً من الإصدار 0.9.50، أصبح IPv6 مدعوماً، وقد يكون عنوان IP الخاص بـ Alice 16 بايت.
- بالنسبة لـ IPv4، يجب إرسال هذه الرسالة عبر اتصال IPv4 مُنشأ،
  حيث أن هذه هي الطريقة الوحيدة التي يعرف بها Bob عنوان IPv4 الخاص بـ Charlie ليعيده إلى Alice في RelayResponse.
  اعتباراً من الإصدار 0.9.50، أصبح IPv6 مدعوماً، وقد يتم إرسال هذه الرسالة عبر اتصال IPv6 مُنشأ.
- اعتباراً من الإصدار 0.9.50، أي عنوان SSU منشور مع introducers يجب أن يحتوي على "4" أو "6" في خيار "caps".
- Challenge غير مُطبق، حجم التحدي دائماً صفر
- الخيارات الممتدة في الرأس: غير متوقعة، غير معرّفة.

### البيانات (النوع 6) {#data}

تُستخدم هذه الرسالة لنقل البيانات والإقرار بالاستلام.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
**البيانات:** 1 بايت flags (انظر أدناه)؛ إذا تم تضمين ACKs صريحة: 1 بايت لعدد ACKs، وذلك العدد من MessageIds بحجم 4 بايت يتم الـ ACK لها بالكامل؛ إذا تم تضمين ACK bitfields: 1 بايت لعدد ACK bitfields، وذلك العدد من MessageIds بحجم 4 بايت + 1 بايت أو أكثر لـ ACK bitfield (انظر الملاحظات)؛ إذا تم تضمين بيانات موسعة: 1 بايت لحجم البيانات، وذلك العدد من البايتات للبيانات الموسعة (غير مفسرة حالياً)؛ 1 بايت لعدد الشظايا (يمكن أن يكون صفر)؛ إذا كان غير صفر، فذلك العدد من شظايا الرسائل.

```
Flags byte:
  Bit order: 76543210 (bit 7 is MSB)
  bit 7: explicit ACKs included
  bit 6: ACK bitfields included
  bit 5: reserved
  bit 4: explicit congestion notification (ECN)
  bit 3: request previous ACKs
  bit 2: want reply
  bit 1: extended data included (unused, never set)
  bit 0: reserved
```
تحتوي كل جزء على: - 4 بايت messageId - 3 بايت معلومات الجزء:   - البتات 23-17: رقم الجزء 0 - 127   - البت 16: isLast (1 = صحيح)   - البتات 15-14: غير مستخدمة، تُعيّن إلى 0 للتوافق مع الاستخدامات المستقبلية   - البتات 13-0: حجم الجزء 0 - 16383 - عدد البايتات المطابق من بيانات الجزء

تنسيق الرسالة:

```
+----+----+----+----+----+----+----+----+
|flag| (additional headers, determined  |
+----+                                  +
~ by the flags, such as ACKs or         ~
| bitfields                             |
+----+----+----+----+----+----+----+----+
|#frg|     messageId     |   frag info  |
+----+----+----+----+----+----+----+----+
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
#### ملاحظات حقل البت للإقرار ACK

يستخدم الـ bitfield البتات السبع المنخفضة من كل بايت، مع البت العالي يحدد ما إذا كان هناك بايت bitfield إضافي يتبعه (1 = صحيح، 0 = بايت الـ bitfield الحالي هو الأخير). هذا التسلسل من مصفوفات البت السبع يمثل ما إذا كان قد تم استلام fragment - إذا كان البت 1، فقد تم استلام الـ fragment. للتوضيح، بافتراض أنه تم استلام الـ fragments 0، 2، 5، و 9، ستكون بايتات الـ bitfield كما يلي:

```
byte 0:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 1 (further bitfield bytes follow)
   bit 6: 0 (fragment 6 not received)
   bit 5: 1 (fragment 5 received)
   bit 4: 0 (fragment 4 not received)
   bit 3: 0 (fragment 3 not received)
   bit 2: 1 (fragment 2 received)
   bit 1: 0 (fragment 1 not received)
   bit 0: 1 (fragment 0 received)
byte 1:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 0 (no further bitfield bytes)
   bit 6: 0 (fragment 13 not received)
   bit 5: 0 (fragment 12 not received)
   bit 4: 0 (fragment 11 not received)
   bit 3: 0 (fragment 10 not received)
   bit 2: 1 (fragment 9 received)
   bit 1: 0 (fragment 8 not received)
   bit 0: 0 (fragment 7 not received)
```
#### ملاحظات

- التنفيذ الحالي يضيف عددًا محدودًا من الإقرارات المكررة للرسائل المُقرة سابقًا، في حالة توفر المساحة.
- إذا كان عدد الأجزاء صفر، فهذه رسالة إقرار فقط أو رسالة الحفاظ على الاتصال.
- خاصية ECN غير مُنفذة، ولا يتم تعيين البت مطلقًا.
- في التنفيذ الحالي، يتم تعيين بت طلب الرد عندما يكون عدد الأجزاء أكبر من صفر، ولا يتم تعيينه عندما لا توجد أجزاء.
- البيانات الموسعة غير مُنفذة ولا تكون موجودة أبدًا.
- استقبال أجزاء متعددة مدعوم في جميع الإصدارات. إرسال أجزاء متعددة مُنفذ في الإصدار 0.9.16.
- كما هو مُنفذ حاليًا، الحد الأقصى للأجزاء هو 64 (أقصى رقم جزء = 63).
- كما هو مُنفذ حاليًا، الحد الأقصى لحجم الجزء بالطبع أقل من الـ MTU.
- احرص على عدم تجاوز الحد الأقصى للـ MTU حتى لو كان هناك عدد كبير من الإقرارات للإرسال.
- البروتوكول يسمح بأجزاء بطول صفر لكن لا يوجد سبب لإرسالها.
- في SSU، تستخدم البيانات رأس I2NP قصير مكون من 5 بايتات متبوعًا بحمولة رسالة I2NP بدلاً من رأس I2NP القياسي المكون من 16 بايت. رأس I2NP القصير يتكون فقط من نوع I2NP ذو البايت الواحد وانتهاء الصلاحية 4-بايت بالثواني. معرف رسالة I2NP يُستخدم كمعرف رسالة للجزء. حجم I2NP يتم تجميعه من أحجام الأجزاء. مجموع التحقق I2NP غير مطلوب حيث أن سلامة رسالة UDP مضمونة بواسطة فك التشفير.
- معرفات الرسائل ليست أرقام تسلسلية وليست متتالية. SSU لا يضمن التسليم بالترتيب. بينما نستخدم معرف رسالة I2NP كمعرف رسالة SSU، من منظور بروتوكول SSU، هي أرقام عشوائية. في الواقع، بما أن router يستخدم مرشح Bloom واحد لجميع النظراء، يجب أن يكون معرف الرسالة رقمًا عشوائيًا فعليًا.
- لأنه لا توجد أرقام تسلسلية، لا توجد طريقة للتأكد من استلام الإقرار. التنفيذ الحالي يرسل بانتظام كمية كبيرة من الإقرارات المكررة. الإقرارات المكررة يجب ألا تُؤخذ كمؤشر على الازدحام.
- ملاحظات حقل بت الإقرار: مُستقبِل حزمة البيانات لا يعرف كم جزء في الرسالة إلا إذا استلم الجزء الأخير. لذلك، عدد بايتات حقل البت المُرسلة في الرد قد يكون أقل أو أكثر من عدد الأجزاء مقسومًا على 7. على سبيل المثال، إذا كان أعلى جزء رآه المُستقبِل هو رقم 4، فمطلوب بايت واحد فقط للإرسال، حتى لو كان هناك 13 جزء في المجموع. يمكن تضمين ما يصل إلى 10 بايتات (أي (64 / 7) + 1) لكل معرف رسالة مُقر.
- خيارات موسعة في الرأس: غير متوقعة، غير محددة.

### PeerTest (النوع 7) {#peertest}

راجع [SSU Peer Testing](/docs/transport/ssu/#peerTesting) للتفاصيل. ملاحظة: يتم دعم اختبار الأقران IPv6 اعتباراً من الإصدار 0.9.27.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte nonce; 1 byte IP address size (may be zero); that many byte representation of Alice's IP address, if size > 0; 2 byte Alice's port number; Alice's or Charlie's 32-byte introduction key; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
</table>
المفتاح التشفيري المستخدم (مدرج بترتيب الحدوث): 1. عند الإرسال من Alice إلى Bob: Alice/Bob sessionKey 2. عند الإرسال من Bob إلى Charlie: Bob/Charlie sessionKey 3. عند الإرسال من Charlie إلى Bob: Bob/Charlie sessionKey 4. عند الإرسال من Bob إلى Alice: Alice/Bob sessionKey (أو بالنسبة لـ Bob قبل الإصدار 0.9.52، Alice's introKey) 5. عند الإرسال من Charlie إلى Alice: Alice's introKey، كما تم استلامه في رسالة PeerTest من Bob 6. عند الإرسال من Alice إلى Charlie: Charlie's introKey، كما تم استلامه في رسالة PeerTest من Charlie

مفتاح MAC المستخدم (مدرج بترتيب الحدوث): 1. عند الإرسال من Alice إلى Bob: مفتاح MAC الخاص بـ Alice/Bob 2. عند الإرسال من Bob إلى Charlie: مفتاح MAC الخاص بـ Bob/Charlie 3. عند الإرسال من Charlie إلى Bob: مفتاح MAC الخاص بـ Bob/Charlie 4. عند الإرسال من Bob إلى Alice: introKey الخاص بـ Alice، كما تم استلامه في رسالة PeerTest من Alice 5. عند الإرسال من Charlie إلى Alice: introKey الخاص بـ Alice، كما تم استلامه في رسالة PeerTest من Bob 6. عند الإرسال من Alice إلى Charlie: introKey الخاص بـ Charlie، كما تم استلامه في رسالة PeerTest من Charlie

تنسيق الرسالة:

```
+----+----+----+----+----+----+----+----+
|    test nonce     |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|                        |
+----+----+----+                        +
| Alice or Charlie's                    |
+ introduction key (Alice's is sent to  +
| Bob and Charlie, while Charlie's is   |
+ sent to Alice)                        +
|                                       |
+              +----+----+----+----+----+
|              | arbitrary amount of    |
+----+----+----+                        |
| uninterpreted data                    |
~                .  .  .                ~
```
الحجم النموذجي بما في ذلك الرأس، في التنفيذ الحالي: 80 بايت (قبل الحشو غير المضاعف للرقم 16)

#### ملاحظات

- عندما ترسل من قبل Alice، يكون حجم عنوان IP هو 0، وعنوان IP غير موجود، والمنفذ هو 0، حيث أن Bob و Charlie لا يستخدمان البيانات؛ الهدف هو تحديد عنوان IP/المنفذ الحقيقي لـ Alice وإخبار Alice؛ Bob و Charlie لا يهتمان بما تعتقد Alice أن عنوانها هو.
- عندما ترسل من قبل Bob أو Charlie، يكون IP والمنفذ موجودين، ويكون عنوان IP بحجم 4 أو 16 بايت. اختبار IPv6 مدعوم اعتباراً من الإصدار 0.9.27.
- عندما ترسل من قبل Charlie إلى Alice، يكون IP والمنفذ كما يلي:
  المرة الأولى (الرسالة 5): IP والمنفذ المطلوب من Alice كما تم استلامه في الرسالة 2.
  المرة الثانية (الرسالة 7): IP والمنفذ الفعلي لـ Alice الذي تم استلام الرسالة 6 منه.
- ملاحظات IPv6: حتى الإصدار 0.9.26، فقط اختبار عناوين IPv4 مدعوم. لذلك، يجب أن تكون جميع الاتصالات بين Alice-Bob و Alice-Charlie عبر IPv4. ومع ذلك، قد يكون الاتصال بين Bob-Charlie عبر IPv4 أو IPv6. عنوان Alice، عندما يُحدد في رسالة PeerTest، يجب أن يكون 4 بايت.
  اعتباراً من الإصدار 0.9.27، اختبار عناوين IPv6 مدعوم، وقد يكون الاتصال بين Alice-Bob و Alice-Charlie عبر IPv6، إذا أشار Bob و Charlie إلى الدعم بقدرة 'B' في عنوان IPv6 المنشور الخاص بهما.
  انظر الاقتراح 126 للتفاصيل.
- Alice ترسل الطلب إلى Bob باستخدام جلسة موجودة عبر النقل (IPv4 أو IPv6) التي تريد اختبارها.
  عندما يستلم Bob طلباً من Alice عبر IPv4، يجب على Bob اختيار Charlie يعلن عن عنوان IPv4.
  عندما يستلم Bob طلباً من Alice عبر IPv6، يجب على Bob اختيار Charlie يعلن عن عنوان IPv6.
  الاتصال الفعلي بين Bob-Charlie قد يكون عبر IPv4 أو IPv6 (أي، مستقل عن نوع عنوان Alice).
- يجب على النظير الاحتفاظ بجدول لحالات الاختبار النشطة (nonces). عند استلام رسالة PeerTest، ابحث عن nonce في الجدول. إذا وُجد، فهو اختبار موجود وأنت تعرف دورك (Alice أو Bob أو Charlie). خلاف ذلك، إذا لم يكن IP موجوداً والمنفذ هو 0، فهذا اختبار جديد وأنت Bob.
  خلاف ذلك، هذا اختبار جديد وأنت Charlie.
- اعتباراً من الإصدار 0.9.15، يجب أن يكون لدى Alice جلسة مؤسسة مع Bob وتستخدم مفتاح الجلسة.
- قبل إصدار API 0.9.52، في بعض التنفيذات، رد Bob على Alice باستخدام مفتاح التعريف الخاص بـ Alice بدلاً من مفتاح جلسة Alice/Bob، على الرغم من أن Alice و Bob لديهما جلسة مؤسسة (منذ 0.9.15).
  اعتباراً من إصدار API 0.9.52، سيستخدم Bob بشكل صحيح مفتاح الجلسة في جميع التنفيذات، ويجب على Alice رفض رسالة مستلمة من Bob بمفتاح التعريف الخاص بـ Alice إذا كان Bob إصدار API 0.9.52 أو أعلى.
- الخيارات الممتدة في الرأس: غير متوقعة، غير محددة.

### HolePunch {#holepunch}

HolePunch هو ببساطة حزمة UDP بدون بيانات. إنه غير مصادق عليه وغير مشفر. لا يحتوي على رأس SSU، لذلك لا يحتوي على رقم نوع رسالة. يتم إرساله من Charlie إلى Alice كجزء من تسلسل Introduction.

## رسائل البيانات النموذجية {#sampledatagrams}

### رسالة البيانات الدنيا

- لا توجد أجزاء، لا توجد ACKs، لا توجد NACKs، إلخ
- الحجم: 39 بايت

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|    |
+----+----+----+----+----+----+----+    +
|  padding to fit a full AES256 block   |
+----+----+----+----+----+----+----+----+
```
### رسالة بيانات أساسية مع الحمولة

- الحجم: 46+fragmentSize بايت

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|
+----+----+----+----+----+----+----+----+
  messageId    |   frag info  |         |
----+----+----+----+----+----+         +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
```
## المراجع

- [تشفير AES](/docs/specs/cryptography/#AES)
- [مواصفات الهياكل المشتركة](/docs/specs/common-structures/)
- [التاريخ](/docs/specs/common-structures/#date)
- [تشفير ElGamal](/docs/specs/cryptography/#elgamal)
- [تفاصيل HMAC](/docs/specs/cryptography/#udp)
- [مصدر I2P](https://github.com/i2p/i2p.i2p)
- [مصدر i2pd](https://github.com/PurpleI2P/i2pd)
- [KeyCertificate](/docs/specs/common-structures/#key-certificates)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SessionKey](/docs/specs/common-structures/#sessionkey)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [نظرة عامة على SSU](/docs/transport/ssu/)
- [مفاتيح SSU](/docs/transport/ssu/#keys)
- [اختبار النظراء في SSU](/docs/transport/ssu/#peerTesting)
