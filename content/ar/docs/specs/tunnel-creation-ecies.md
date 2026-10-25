---
title: "مواصفات إنشاء tunnel (ECIES-X25519)"
description: "تشفير رسائل بناء tunnel باستخدام عمليات التشفير الأساسية ECIES-X25519 لتوفير السرية الأمامية."
slug: "tunnel-creation-ecies"
aliases:
  - "/ar/docs/specs/tunnel-creation-ecies-spec"
  - "/ar/docs/specs/tunnel-creation-ecies-spec/"
category: "البروتوكولات"
lastUpdated: "2025-06"
accurateFor: "0.9.66"
---

## نظرة عامة

تحدد هذه الوثيقة تشفير رسائل Tunnel Build باستخدام العناصر الأساسية للتشفير المقدمة من [ECIES-X25519](/docs/specs/ecies/). وهي جزء من الاقتراح الشامل [Prop156](/proposals/156/) لتحويل أجهزة router من مفاتيح ElGamal إلى مفاتيح ECIES-X25519.

هناك إصداران محددان. الأول يستخدم رسائل البناء الحالية وحجم سجل البناء، للتوافق مع routers ElGamal. تم تنفيذ هذه المواصفة اعتباراً من الإصدار 0.9.48 وهي الآن مهجورة. الثاني يستخدم رسالتي بناء جديدتين وحجم سجل بناء أصغر، ويمكن استخدامه فقط مع routers ECIES. تم تنفيذ هذه المواصفة اعتباراً من الإصدار 0.9.51.

لأغراض نقل الشبكة من ElGamal + AES256 إلى ECIES + ChaCha20، فإن الـ tunnels التي تحتوي على مزيج من routers ElGamal و ECIES ضرورية. يتم توفير مواصفات للتعامل مع hops الـ tunnel المختلطة. لن يتم إجراء أي تغييرات على تنسيق أو معالجة أو تشفير hops ElGamal. هذا التنسيق يحافظ على نفس الحجم لسجلات بناء الـ tunnel، كما هو مطلوب للتوافق.

منشئو أنفاق ElGamal سيولدون أزواج مفاتيح X25519 مؤقتة لكل قفزة، وسيتبعون هذه المواصفة لإنشاء أنفاق تحتوي على قفزات ECIES.

تحدد هذه الوثيقة بناء الأنفاق ECIES-X25519. للحصول على نظرة عامة على جميع التغييرات المطلوبة لأجهزة التوجيه ECIES، راجع الاقتراح 156 [Prop156](/proposals/156/). للحصول على خلفية إضافية حول تطوير مواصفات السجل الطويل، راجع الاقتراح 152 [Prop152](/proposals/152/). للحصول على خلفية إضافية حول تطوير مواصفات السجل القصير، راجع الاقتراح 157 [Prop157](/proposals/157/).

### البدائيات التشفيرية

العناصر الأساسية المطلوبة لتنفيذ هذه المواصفة هي:

- AES-256-CBC كما هو موضح في [التشفير](/docs/specs/cryptography/)
- دوال STREAM ChaCha20: ENCRYPT(k, iv, plaintext) و DECRYPT(k, iv, ciphertext) - كما هو موضح في [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) و [RFC-7539](https://tools.ietf.org/html/rfc7539)
- دوال STREAM ChaCha20/Poly1305: ENCRYPT(k, n, plaintext, ad) و DECRYPT(k, n, ciphertext, ad) - كما هو موضح في [NTCP2](/docs/specs/ntcp2/) و [ECIES-X25519](/docs/specs/ecies/) و [RFC-7539](https://tools.ietf.org/html/rfc7539)
- دوال X25519 DH - كما هو موضح في [NTCP2](/docs/specs/ntcp2/) و [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - كما هو موضح في [NTCP2](/docs/specs/ntcp2/) و [ECIES-X25519](/docs/specs/ecies/)

دوال Noise أخرى معرفة في مكان آخر:

- MixHash(d) - كما في [NTCP2](/docs/specs/ntcp2/) و [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - كما في [NTCP2](/docs/specs/ntcp2/) و [ECIES-X25519](/docs/specs/ecies/)

## التصميم

### إطار عمل بروتوكول Noise

تقدم هذه المواصفة المتطلبات المبنية على إطار عمل Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (المراجعة 34، 2018-07-11). في مصطلحات Noise، Alice هي المبادر، وBob هو المستجيب.

إنه مبني على بروتوكول Noise وهو Noise_N_25519_ChaChaPoly_SHA256. يستخدم بروتوكول Noise هذا العناصر الأساسية التالية:

- نمط المصافحة أحادي الاتجاه: N - أليس لا ترسل مفتاحها الثابت إلى بوب (N)
- دالة DH: X25519 - X25519 DH بطول مفتاح 32 بايت كما هو محدد في [RFC-7748](https://tools.ietf.org/html/rfc7748)
- دالة التشفير: ChaChaPoly - AEAD_CHACHA20_POLY1305 كما هو محدد في [RFC-7539](https://tools.ietf.org/html/rfc7539) القسم 2.8. nonce بحجم 12 بايت، مع تعيين أول 4 بايتات إلى الصفر. مطابق لذلك الموجود في [NTCP2](/docs/specs/ntcp2/)
- دالة الهاش: SHA256 - هاش قياسي بحجم 32 بايت، مستخدم بالفعل على نطاق واسع في I2P

### أنماط المصافحة

تستخدم المصافحات أنماط مصافحة [Noise](https://noiseprotocol.org/noise.html).

يتم استخدام تطابق الأحرف التالي:

- e = مفتاح مؤقت لمرة واحدة
- s = مفتاح ثابت
- p = حمولة الرسالة

طلب البناء مطابق لنمط Noise N. وهذا مطابق أيضاً للرسالة الأولى (طلب الجلسة) في نمط XK المستخدم في [NTCP2](/docs/specs/ntcp2/).

```
<- s
  ...
  e es p ->
```
### تشفير الطلبات

يتم إنشاء سجلات طلب البناء بواسطة منشئ النفق ويتم تشفيرها بشكل غير متماثل لكل hop فردي. هذا التشفير غير المتماثل لسجلات الطلب هو حاليًا ElGamal كما هو محدد في [التشفير](/docs/specs/cryptography/) ويحتوي على checksum SHA-256. هذا التصميم ليس forward-secret.

يستخدم تصميم ECIES نمط Noise أحادي الاتجاه "N" مع ECIES-X25519 ephemeral-static DH، مع HKDF، و ChaCha20/Poly1305 AEAD لتحقيق السرية الأمامية والتكامل والمصادقة. أليس هي طالبة بناء tunnel. كل قفزة في tunnel هي بوب.

### تشفير الرد

يتم إنشاء سجلات الرد للبناء بواسطة منشئ الـ hops وتشفيرها بشكل متماثل للمنشئ. هذا التشفير المتماثل لسجلات الرد ElGamal هو AES مع مجموع تحقق SHA-256 مُسبق. هذا التصميم لا يوفر السرية الأمامية.

ردود ECIES تستخدم ChaCha20/Poly1305 AEAD للتكامل والمصادقة.

## مواصفات السجل الطويل

ملاحظة: منتهي الصلاحية، مهجور. استخدم تنسيق السجل المختصر المحدد أدناه.

### سجلات طلبات البناء

سجلات BuildRequestRecords المشفرة تبلغ 528 بايت لكل من ElGamal و ECIES، من أجل التوافق.

#### سجل الطلب غير المشفر

هذه مواصفات BuildRequestRecord للأنفاق الخاصة بموجهات ECIES-X25519. ملخص التغييرات:

- إزالة router hash غير المستخدم بحجم 32 بايت
- تغيير وقت الطلب من ساعات إلى دقائق
- إضافة حقل انتهاء الصلاحية لوقت tunnel متغير مستقبلي
- إضافة مساحة أكثر للعلامات
- إضافة تعيين لخيارات بناء إضافية
- مفتاح الرد AES-256 و IV لا يتم استخدامهما لسجل الرد الخاص بالقفزة نفسها
- السجل غير المشفر أطول لأن هناك حمولة تشفير أقل

سجل الطلب لا يحتوي على أي مفاتيح رد ChaCha. هذه المفاتيح مُشتقة من KDF. انظر أدناه.

جميع الحقول بتنسيق big-endian.

الحجم غير المشفر: 464 بايت

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40-71</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel layer key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">72-103</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel IV key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">104-135</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">136-151</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply IV</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">152</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">153-155</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">156-159</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">160-163</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">164-167</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">168-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-463</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding</td></tr>
</tbody>
</table>
حقل الأعلام هو نفسه كما هو محدد في [إنشاء الأنفاق](/docs/specs/tunnel-creation/) ويحتوي على ما يلي:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
البت 7 يشير إلى أن القفزة ستكون بوابة داخلية (IBGW). البت 6 يشير إلى أن القفزة ستكون نقطة نهاية خارجية (OBEP). إذا لم يتم تعيين أي من البتين، فستكون القفزة مشاركًا وسيطًا. لا يمكن تعيين كليهما في نفس الوقت.

انتهاء صلاحية الطلب مخصص لمدة tunnel متغيرة مستقبلية. في الوقت الحالي، القيمة الوحيدة المدعومة هي 600 (10 دقائق).

خيارات بناء tunnel هي هيكل Mapping كما هو معرف في [Common](/docs/specs/common-structures/). الخيارات الوحيدة المعرفة حالياً هي لمعاملات النطاق الترددي، اعتباراً من API 0.9.65، انظر أدناه للتفاصيل. إذا كان هيكل Mapping فارغاً، فهذا يعني بايتان 0x00 0x00. الحد الأقصى لحجم Mapping (بما في ذلك حقل الطول) هو 296 بايت، والحد الأقصى لقيمة حقل طول Mapping هو 294.

#### سجل الطلب مشفر

جميع الحقول بترتيب البايت الكبير (big-endian) باستثناء المفتاح العام المؤقت (ephemeral public key) الذي يكون بترتيب البايت الصغير (little-endian).

الحجم المشفر: 528 بايت

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### بناء سجلات الرد

سجلات BuildReplyRecords المُشفرة هي 528 بايت لكل من ElGamal و ECIES، من أجل التوافق.

#### سجل الرد غير المشفر

هذه هي مواصفات BuildReplyRecord الخاصة بـ tunnel لـ routers من نوع ECIES-X25519. ملخص التغييرات:

- إضافة تعيين لخيارات رد البناء
- السجل غير المشفر أطول لأن هناك حمولة تشفير أقل

ردود ECIES مشفرة باستخدام ChaCha20/Poly1305.

جميع الحقول بترتيب البايت الكبير (big-endian).

الحجم غير المشفر: 512 بايت

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-510</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
خيارات رد بناء tunnel هي هيكل Mapping كما هو معرّف في [Common](/docs/specs/common-structures/). الخيارات الوحيدة المعرّفة حالياً هي لمعاملات عرض النطاق الترددي، اعتباراً من API 0.9.65، انظر أدناه للتفاصيل. إذا كان هيكل Mapping فارغاً، فهذا عبارة عن بايتين 0x00 0x00. الحد الأقصى لحجم Mapping (بما في ذلك حقل الطول) هو 511 بايت، والحد الأقصى لقيمة حقل طول Mapping هو 509.

بايت الرد هو إحدى القيم التالية كما هو محدد في [Tunnel-Creation](/docs/specs/tunnel-creation/) لتجنب بصمة الأصابع:

- 0x00 (قبول)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### سجل الرد مُشفّر

الحجم المشفر: 528 بايت

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
بعد الانتقال الكامل إلى سجلات ECIES، تكون قواعد الحشو المدى نفسها كما هو الحال بالنسبة لسجلات الطلب.

### التشفير المتماثل للسجلات

المسارات المختلطة مسموحة وضرورية للانتقال من ElGamal إلى ECIES. خلال الفترة الانتقالية، سيزداد عدد أجهزة router التي تستخدم مفاتيح ECIES.

ستعمل المعالجة المسبقة للتشفير المتماثل بنفس الطريقة:

- "encryption":
  - تشغيل التشفير في وضع فك التشفير
  - سجلات الطلبات مفكوكة التشفير مسبقاً في المعالجة المسبقة (إخفاء سجلات الطلبات المشفرة)
- "decryption":
  - تشغيل التشفير في وضع التشفير
  - سجلات الطلبات مشفرة (كشف سجل الطلب النصي التالي) بواسطة قفزات المشاركين
- ChaCha20 لا يحتوي على "أوضاع"، لذلك يتم تشغيله ببساطة ثلاث مرات:
  - مرة واحدة في المعالجة المسبقة
  - مرة واحدة بواسطة القفزة
  - مرة واحدة في معالجة الرد النهائي

عند استخدام الأنفاق المختلطة، سيحتاج منشئو الأنفاق إلى بناء التشفير المتماثل لـ BuildRequestRecord على أساس نوع التشفير للعقدة الحالية والسابقة.

ستستخدم كل hop نوع التشفير الخاص بها لتشفير BuildReplyRecords، والسجلات الأخرى في VariableTunnelBuildMessage (VTBM).

على مسار الرد، ستحتاج نقطة النهاية (المرسل) إلى إلغاء [التشفير المتعدد](https://en.wikipedia.org/wiki/Multiple_encryption)، باستخدام مفتاح الرد لكل قفزة.

كمثال توضيحي، دعونا ننظر إلى tunnel صادر مع ECIES محاط بـ ElGamal:

- المرسل (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

جميع سجلات BuildRequestRecords تكون في حالتها المشفرة (باستخدام ElGamal أو ECIES).

تشفير AES256/CBC، عند استخدامه، لا يزال يُستخدم لكل سجل، دون ربط عبر سجلات متعددة.

وبالمثل، سيتم استخدام ChaCha20 لتشفير كل سجل، وليس البث عبر VTBM بالكامل.

يتم معالجة سجلات الطلبات مسبقاً من قبل المرسل (OBGW):

- سجل H3 "مشفر" باستخدام:
  - مفتاح الرد الخاص بـ H2 (ChaCha20)
  - مفتاح الرد الخاص بـ H1 (AES256/CBC)
- سجل H2 "مشفر" باستخدام:
  - مفتاح الرد الخاص بـ H1 (AES256/CBC)
- سجل H1 يخرج بدون تشفير متماثل

فقط H2 يفحص علامة تشفير الرد، ويرى أنها متبوعة بـ AES256/CBC.

بعد معالجتها من قبل كل hop، تصبح السجلات في حالة "مفكوكة التشفير":

- يتم "فك تشفير" سجل H3 باستخدام:
  - مفتاح الرد الخاص بـ H3 (AES256/CBC)
- يتم "فك تشفير" سجل H2 باستخدام:
  - مفتاح الرد الخاص بـ H3 (AES256/CBC)
  - مفتاح الرد الخاص بـ H2 (ChaCha20-Poly1305)
- يتم "فك تشفير" سجل H1 باستخدام:
  - مفتاح الرد الخاص بـ H3 (AES256/CBC)
  - مفتاح الرد الخاص بـ H2 (ChaCha20)
  - مفتاح الرد الخاص بـ H1 (AES256/CBC)

منشئ tunnel، والمعروف أيضاً باسم Inbound Endpoint (IBEP)، يعالج الرد لاحقاً:

- سجل H3 "مشفر" باستخدام:
  - مفتاح الرد الخاص بـ H3 (AES256/CBC)
- سجل H2 "مشفر" باستخدام:
  - مفتاح الرد الخاص بـ H3 (AES256/CBC)
  - مفتاح الرد الخاص بـ H2 (ChaCha20-Poly1305)
- سجل H1 "مشفر" باستخدام:
  - مفتاح الرد الخاص بـ H3 (AES256/CBC)
  - مفتاح الرد الخاص بـ H2 (ChaCha20)
  - مفتاح الرد الخاص بـ H1 (AES256/CBC)

### مفاتيح سجل الطلب

هذه المفاتيح مُدرجة بوضوح في ElGamal BuildRequestRecords. بالنسبة لـ ECIES BuildRequestRecords، فإن مفاتيح tunnel ومفاتيح الرد AES مُدرجة، لكن مفاتيح الرد ChaCha مُشتقة من تبادل DH. راجع [Prop156](/proposals/156/) للتفاصيل حول مفاتيح router الثابتة ECIES.

فيما يلي وصف لكيفية اشتقاق المفاتيح المرسلة مسبقاً في سجلات الطلب.

#### KDF للقيم الأولية ck و h

هذا هو معيار [NOISE](https://noiseprotocol.org/noise.html) للنمط "N" مع اسم بروتوكول قياسي.

```
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
#### KDF لسجل الطلب

منشئو tunnel الخاصون بـ ElGamal يولدون زوج مفاتيح X25519 مؤقت لكل قفزة ECIES في tunnel، ويستخدمون المخطط أعلاه لتشفير BuildRequestRecord الخاص بهم. منشئو tunnel الخاصون بـ ElGamal سيستخدمون المخطط السابق لهذه المواصفة للتشفير إلى قفزات ElGamal.

منشئو tunnel الذين يستخدمون ECIES سيحتاجون إلى التشفير لكل مفتاح عام لـ ElGamal hop باستخدام المخطط المحدد في [Tunnel-Creation](/docs/specs/tunnel-creation/). منشئو tunnel الذين يستخدمون ECIES سيستخدمون المخطط المذكور أعلاه للتشفير إلى ECIES hops.

هذا يعني أن tunnel hops ستشاهد فقط السجلات المشفرة من نفس نوع التشفير الخاص بها.

بالنسبة لمنشئي tunnel الذين يستخدمون ElGamal و ECIES، سيقومون بتوليد أزواج مفاتيح X25519 مؤقتة فريدة لكل hop لتشفير hops الخاصة بـ ECIES.

**مهم**: يجب أن تكون المفاتيح المؤقتة فريدة لكل قفزة ECIES، ولكل سجل بناء. عدم استخدام مفاتيح فريدة يفتح ثغرة هجومية للقفزات المتواطئة لتأكيد وجودها في نفس tunnel.

```
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
`replyKey` و `layerKey` و `layerIV` يجب أن تكون مُضمَّنة داخل سجلات ElGamal، ويمكن إنشاؤها بشكل عشوائي.

### تشفير سجل الرد

سجل الرد مشفر بـ ChaCha20/Poly1305.

```
// AEAD parameters
k = chainkey from build request
n = 0
plaintext = 512 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
## مواصفات السجل المختصر

تستخدم هذه المواصفة رسالتي I2NP جديدتين لبناء الأنفاق، رسالة بناء النفق القصير (النوع 25) ورسالة رد بناء النفق الصادر (النوع 26).

يجب أن يكون منشئ tunnel وجميع القفزات في tunnel المنشأ متوافقين مع ECIES-X25519، وعلى الأقل الإصدار 0.9.51. القفزات في tunnel الرد (للبناء الصادر) أو tunnel الصادر (للبناء الوارد) لا تحتاج إلى أي متطلبات.

ستكون سجلات الطلب والرد المشفرة 218 بايت، مقارنة بـ 528 بايت لجميع رسائل البناء الأخرى.

ستكون سجلات الطلبات النصية العادية 154 بايت، مقارنة بـ 222 بايت لسجلات ElGamal، و 464 بايت لسجلات ECIES كما هو محدد أعلاه.

ستكون سجلات الاستجابة النصية العادية 202 بايت، مقارنة بـ 496 بايت لسجلات ElGamal، و 512 بايت لسجلات ECIES كما هو محدد أعلاه.

سيكون تشفير الرد ChaCha20/Poly1305 لسجل الـ hop الخاص به، و ChaCha20 (وليس ChaCha20/Poly1305) للسجلات الأخرى في رسالة البناء.

ستصبح سجلات الطلبات أصغر حجماً من خلال استخدام HKDF لإنشاء مفاتيح الطبقة والرد، لذلك لن يتم تضمينها بشكل صريح في الطلب.

### تدفق الرسائل

```
STBM: Short tunnel build message (type 25)
OTBRM: Outbound tunnel build reply message (type 26)

Outbound Build A-B-C
Reply through existing inbound D-E-F


                New Tunnel
         STBM      STBM      STBM
Creator ------> A ------> B ------> C ---\
                                   OBEP   \
                                          | Garlic wrapped (optional)
                                          | OTBRM
                                          | (TUNNEL delivery)
                                          | from OBEP to
                                          | creator
              Existing Tunnel             /
Creator <-------F---------E-------- D <--/
                                   IBGW



Inbound Build D-E-F
Sent through existing outbound A-B-C


              Existing Tunnel
Creator ------> A ------> B ------> C ---\
                                  OBEP    \
                                          | Garlic wrapped (optional)
                                          | STBM
                                          | (ROUTER delivery)
                                          | from creator
                New Tunnel                | to IBGW
          STBM      STBM      STBM        /
Creator <------ F <------ E <------ D <--/
                                   IBGW
```
#### ملاحظات

تغليف garlic للرسائل يخفيها عن OBEP (للبناء الداخلي) أو IBGW (للبناء الخارجي). هذا موصى به ولكنه ليس مطلوباً. إذا كان OBEP وIBGW نفس router، فإنه ليس ضرورياً.

### سجلات طلبات البناء المختصرة

سجلات BuildRequestRecords المشفرة القصيرة تبلغ 218 بايت.

#### سجل الطلب القصير غير المشفر

ملخص التغييرات من السجلات الطويلة:

- تغيير الطول غير المشفر من 464 إلى 154 بايت
- تغيير الطول المشفر من 528 إلى 218 بايت
- إزالة مفاتيح الطبقة والرد و IVs، سيتم إنتاجها من KDF

سجل الطلب لا يحتوي على أي مفاتيح رد ChaCha. هذه المفاتيح مشتقة من KDF. انظر أدناه.

جميع الحقول بترتيب البايت الكبير (big-endian).

الحجم غير المشفر: 154 بايت.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">41-42</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">43</td><td style="border:1px solid var(--color-border); padding:0.6rem;">layer encryption type</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">44-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-51</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">52-55</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">56-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-153</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding (see below)</td></tr>
</tbody>
</table>
حقل الأعلام هو نفسه المعرّف في [إنشاء الأنفاق](/docs/specs/tunnel-creation/) ويحتوي على ما يلي:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
البت 7 يشير إلى أن القفزة ستكون بوابة داخلة (IBGW). البت 6 يشير إلى أن القفزة ستكون نقطة نهاية خارجة (OBEP). إذا لم يتم تعيين أي من البتين، ستكون القفزة مشاركًا وسيطًا. لا يمكن تعيين كليهما في نفس الوقت.

نوع تشفير الطبقة: 0 للـ AES (كما هو الحال في الأنفاق الحالية)؛ 1 للمستقبل (ChaCha؟)

انتهاء صلاحية الطلب مخصص لمدة tunnel متغيرة في المستقبل. في الوقت الحالي، القيمة الوحيدة المدعومة هي 600 (10 دقائق).

مفتاح المنشئ العام المؤقت هو مفتاح ECIES، بترتيب البايت الكبير. يُستخدم لدالة اشتقاق المفتاح (KDF) لطبقة IBGW ومفاتيح الرد ومتجهات التهيئة. يتم تضمين هذا فقط في السجل النصي الواضح في رسالة Inbound Tunnel Build. وهو مطلوب لأنه لا يوجد DH في هذه الطبقة لسجل البناء.

خيارات بناء tunnel هي هيكل Mapping كما هو محدد في [Common](/docs/specs/common-structures/). الخيارات الوحيدة المعرّفة حاليًا هي لمعاملات النطاق الترددي، اعتبارًا من API 0.9.65، انظر أدناه للتفاصيل. إذا كان هيكل Mapping فارغًا، فهذا يعني بايتان 0x00 0x00. الحد الأقصى لحجم Mapping (بما في ذلك حقل الطول) هو 98 بايت، والحد الأقصى لقيمة حقل طول Mapping هو 96.

#### سجل الطلب المختصر المُشفر

جميع الحقول تستخدم ترتيب البايت الكبير (big-endian) باستثناء المفتاح العام المؤقت الذي يستخدم ترتيب البايت الصغير (little-endian).

الحجم المشفر: 218 بايت

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### سجلات الرد على البناء المختصرة

سجلات BuildReplyRecords المشفرة القصيرة تبلغ 218 بايت.

#### سجل الرد القصير غير المشفر

ملخص التغييرات من السجلات الطويلة:

- تغيير الطول غير المشفر من 512 إلى 202 بايت
- تغيير الطول المشفر من 528 إلى 218 بايت

ردود ECIES مُشفَّرة باستخدام ChaCha20/Poly1305.

جميع الحقول تستخدم ترتيب البايت الكبير (big-endian).

الحجم غير المشفر: 202 بايت.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-200</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding (see below)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
خيارات رد بناء tunnel هي بنية Mapping كما هو محدد في [Common](/docs/specs/common-structures/). الخيارات الوحيدة المحددة حاليًا هي لمعاملات عرض النطاق الترددي، اعتبارًا من API 0.9.65، انظر أدناه للتفاصيل. إذا كانت بنية Mapping فارغة، فهذا عبارة عن بايتين 0x00 0x00. الحد الأقصى لحجم Mapping (بما في ذلك حقل الطول) هو 201 بايت، والحد الأقصى لقيمة حقل طول Mapping هو 199.

بايت الرد هو إحدى القيم التالية كما هو محدد في [إنشاء النفق](/docs/specs/tunnel-creation/) لتجنب بصمة الهوية:

- 0x00 (قبول)
- 30 (TUNNEL_REJECT_BANDWIDTH)

قد يتم تعريف قيمة رد إضافية في المستقبل لتمثيل الرفض للخيارات غير المدعومة.

#### سجل الرد القصير المشفر

الحجم المشفر: 218 بايت

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### KDF

نستخدم chaining key (ck) من حالة Noise بعد تشفير/فك تشفير سجل بناء tunnel لاشتقاق المفاتيح التالية: مفتاح الرد، مفتاح طبقة AES، مفتاح AES IV ومفتاح/علامة رد garlic للـ OBEP.

مفاتيح الرد: لاحظ أن KDF مختلف قليلاً بالنسبة لقفزات OBEP وغير OBEP. على عكس السجلات الطويلة لا يمكننا استخدام الجزء الأيسر من ck لمفتاح الرد، لأنه ليس الأخير وسيتم استخدامه لاحقاً. يُستخدم مفتاح الرد لتشفير رد ذلك السجل باستخدام AEAD/ChaCha20/Poly1305 و ChaCha20 للرد على السجلات الأخرى. كلاهما يستخدم نفس المفتاح. الـ nonce هو موضع السجل في الرسالة بدءاً من 0. انظر أدناه للتفاصيل.

```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
replyKey = keydata[32:63]
ck = keydata[0:31]

AES Layer key:
keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
layerKey = keydata[32:63]

IV key for non-OBEP record:
ivKey = keydata[0:31]
because it's last

IV key for OBEP record:
ck = keydata[0:31]
keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
ivKey = keydata[32:63]
ck = keydata[0:31]

OBEP garlic reply key/tag:
keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
garlicReplyKey = keydata[32:63]
garlicReplyTag = keydata[0:7]
```
ملاحظة: دالة اشتقاق المفتاح (KDF) لمفتاح IV في OBEP مختلفة عن تلك المستخدمة للقفزات الأخرى، حتى لو لم يكن الرد مشفرًا بـ garlic encryption.

#### تشفير السجلات

يتم تشفير سجل الرد الخاص بـ hop باستخدام ChaCha20/Poly1305. هذا مماثل لمواصفات السجل الطويل أعلاه، باستثناء أن 'n' هو رقم السجل 0-7، بدلاً من أن يكون دائماً 0. انظر [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// AEAD parameters
k = replyKey from KDF above
n = record number 0-7
plaintext = 202 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
السجلات الأخرى مشفرة بشكل تكراري ومتماثل في كل قفزة باستخدام ChaCha20 (وليس ChaCha20/Poly1305). هذا يختلف عن مواصفات السجل الطويل أعلاه، التي تستخدم AES ولا تستخدم رقم السجل.

يتم وضع رقم السجل في IV في البايت 4، لأن ChaCha20 يستخدم IV بحجم 12 بايت مع nonce little-endian في البايتات 4-11. راجع [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// Parameters
k = replyKey from KDF above
n = record number 0-7
iv = 12 bytes, all zeros except iv[4] = n
plaintext = 218 byte encrypted record

ciphertext = ENCRYPT(k, iv, plaintext)
```
#### Garlic Encryption

تغليف garlic للرسائل يخفيها عن OBEP (للبناء الداخلي) أو IBGW (للبناء الخارجي). هذا مُوصى به ولكن ليس مطلوباً. إذا كان OBEP و IBGW نفس router، فليس ضرورياً.

تشفير garlic encryption لرسالة Short Tunnel Build Message واردة، بواسطة المنشئ، مشفرة إلى ECIES IBGW، يستخدم تشفير Noise 'N'، كما هو معرف في [ECIES-ROUTERS](/docs/specs/ecies-routers/).

garlic encryption لرسالة Outbound Tunnel Build Reply Message، بواسطة OBEP، المشفرة للمنشئ، تستخدم رسائل Existing Session مع مفتاح الرد garlic reply key بحجم 32 بايت وعلامة الرد garlic reply tag بحجم 8 بايت من KDF أعلاه. التنسيق كما هو محدد للردود على Database Lookups في [I2NP](/docs/specs/i2np/)، و[ECIES-ROUTERS](/docs/specs/ecies-routers/)، و[ECIES-X25519](/docs/specs/ecies/).

#### تشفير الطبقة

تتضمن هذه المواصفة حقل نوع تشفير الطبقة في سجل طلب البناء. نوع تشفير الطبقة الوحيد المدعوم حالياً هو النوع 0، وهو AES. هذا لم يتغير عن المواصفات السابقة، باستثناء أن مفتاح الطبقة ومفتاح IV يتم اشتقاقهما من KDF أعلاه بدلاً من تضمينهما في سجل طلب البناء.

إضافة أنواع تشفير طبقات جديدة، على سبيل المثال ChaCha20، هو موضوع للبحث الإضافي، وليس جزءاً من هذه المواصفة حالياً.

## ملاحظات التنفيذ

- أجهزة router القديمة لا تتحقق من نوع التشفير للقفزة وستقوم بإرسال سجلات مشفرة بـ ElGamal. بعض أجهزة router الحديثة تحتوي على أخطاء وستقوم بإرسال أنواع مختلفة من السجلات المشوهة. يجب على المطورين اكتشاف ورفض هذه السجلات قبل عملية DH إن أمكن، لتقليل استخدام المعالج.

### سجلات البناء

يجب أن يكون ترتيب سجل البناء عشوائياً، بحيث لا تعرف النقاط الوسطية موقعها داخل tunnel.

العدد الأدنى الموصى به من سجلات البناء هو 4. إذا كان هناك سجلات بناء أكثر من القفزات، يجب إضافة سجلات "وهمية"، تحتوي على بيانات عشوائية أو خاصة بالتنفيذ. بالنسبة لبناء الأنفاق الواردة، يجب أن يكون هناك دائماً سجل "وهمي" واحد للـ router المنشئ، مع بادئة hash صحيحة من 16 بايت ومفتاح X25519 ephemeral حقيقي، وإلا فإن القفزة الأقرب ستعرف أن القفزة التالية هي المنشئ.

باقي السجل "المزيف" قد يكون بيانات عشوائية، أو قد يكون مشفراً بأي صيغة ليتمكن المنشئ من إرسال بيانات إلى نفسه حول البناء، ربما لتقليل متطلبات التخزين للبناءات المعلقة.

يجب على منشئي الـ tunnels الواردة استخدام طريقة ما للتحقق من أن "السجل المزيف" الخاص بهم لم يتم تعديله من قبل الـ hop السابق، حيث قد يُستخدم هذا أيضاً لكشف الهوية. يمكن للمنشئ تخزين والتحقق من checksum للسجل، أو تضمين الـ checksum في السجل، أو استخدام دالة تشفير/فك تشفير AEAD، حسب التنفيذ. إذا تم تعديل بادئة الـ hash المكونة من 16 بايت أو محتويات سجل البناء الأخرى، يجب على الـ router التخلص من الـ tunnel.

السجلات المزيفة للأنفاق الصادرة، والسجلات المزيفة الإضافية للأنفاق الواردة، لا تخضع لهذه المتطلبات، وقد تكون بيانات عشوائية تماماً، حيث أنها لن تكون مرئية لأي hop. قد يظل من المرغوب فيه للمنشئ التحقق من أنها لم يتم تعديلها.

## معاملات عرض النطاق الترددي للـ tunnel

### نظرة عامة

مع تحسيننا لأداء الشبكة خلال السنوات القليلة الماضية من خلال بروتوكولات جديدة وأنواع تشفير وتحسينات في التحكم بالازدحام، أصبحت التطبيقات السريعة مثل بث الفيديو ممكنة. تتطلب هذه التطبيقات عرض نطاق ترددي عالي في كل قفزة في أنفاق العميل الخاصة بها.

ومع ذلك، فإن أجهزة router المشاركة لا تملك أي معلومات حول مقدار النطاق الترددي الذي سيستخدمه tunnel عندما تتلقى رسالة بناء tunnel. يمكنها فقط قبول أو رفض tunnel بناءً على إجمالي النطاق الترددي المستخدم حالياً من قبل جميع أنفاق tunnel المشاركة والحد الأقصى للنطاق الترددي الإجمالي لأنفاق tunnel المشاركة.

أيضاً، لا تملك routers الطالبة أي معلومات حول مقدار النطاق الترددي المتوفر عند كل hop.

أيضاً، لا تملك routers حالياً أي طريقة لتحديد حركة البيانات الواردة على tunnel. سيكون هذا مفيداً جداً في أوقات الحمل الزائد أو هجمات DDoS على خدمة ما.

معاملات عرض النطاق الترددي للـ tunnel في رسائل طلب وإجابة بناء الـ tunnel تضيف دعماً لهذه الميزات. راجع [Prop168](/proposals/168/) لمعلومات إضافية عن الخلفية. هذه المعاملات معرّفة اعتباراً من API 0.9.65، لكن الدعم قد يختلف حسب التنفيذ. هي مدعومة لكل من سجلات بناء ECIES الطويلة والقصيرة.

### خيارات طلب البناء

يمكن تعيين الخيارات الثلاثة التالية في حقل تخطيط خيارات بناء النفق للسجل: يمكن لجهاز router الطالب أن يتضمن أي منها أو جميعها أو لا شيء.

- m := الحد الأدنى لعرض النطاق المطلوب لهذا tunnel (KBps عدد صحيح موجب كنص)
- r := عرض النطاق المطلوب لهذا tunnel (KBps عدد صحيح موجب كنص)
- l := حد عرض النطاق لهذا tunnel؛ يُرسل فقط إلى IBGW (KBps عدد صحيح موجب كنص)

القيد: m <= r <= l

يجب على الـ router المشارك رفض الـ tunnel إذا تم تحديد "m" ولا يستطيع توفير عرض النطاق الترددي المطلوب على الأقل.

يتم إرسال خيارات الطلب إلى كل مشارك في سجل طلب البناء المشفر المقابل، وهي غير مرئية للمشاركين الآخرين.

### خيار بناء الرد

يمكن تعيين الخيار التالي في حقل تخطيط خيارات رد بناء tunnel في السجل، عندما تكون الاستجابة ACCEPTED:

- b := عرض النطاق المتاح لهذا الـ tunnel (عدد صحيح موجب بوحدة KBps كسلسلة نصية)

القيد: b >= m

يجب على router المشارك تضمين هذا إذا تم تحديد "m" أو "r" في طلب البناء. يجب أن تكون القيمة على الأقل مساوية لقيمة "m" إذا تم تحديدها، ولكن يمكن أن تكون أقل أو أكثر من قيمة "r" إذا تم تحديدها.

يجب على الـ router المشارك أن يحاول حجز وتوفير هذا المقدار من النطاق الترددي على الأقل للـ tunnel، ولكن هذا غير مضمون. لا يمكن للـ routers التنبؤ بالظروف بعد 10 دقائق في المستقبل، وحركة البيانات المشاركة لها أولوية أقل من حركة البيانات الخاصة بالـ router والـ tunnels الخاصة به.

قد تقوم الـ routers أيضاً بتخصيص عرض نطاق ترددي أكبر من المتاح إذا لزم الأمر، وهذا أمر مرغوب فيه على الأرجح، حيث يمكن لنقاط الاتصال الأخرى في الـ tunnel أن ترفضه.

لهذه الأسباب، يجب التعامل مع رد router المشارك كالتزام يُبذل فيه أفضل جهد ممكن، وليس كضمان.

يتم إرسال خيارات الرد إلى الـ router الطالب في سجل رد البناء المشفر المقابل، وهي غير مرئية للمشاركين الآخرين.

### ملاحظات التنفيذ

معاملات النطاق الترددي كما تُشاهد في routers المشاركة على طبقة tunnel، أي عدد رسائل tunnel ذات الحجم الثابت 1 كيلوبايت في الثانية. النفقات العامة للنقل (NTCP2 أو SSU2) غير مُضمّنة.

قد تكون هذه السعة أكبر أو أصغر بكثير من السعة المرئية عند العميل. رسائل tunnel تحتوي على نفقات إضافية كبيرة، بما في ذلك النفقات من الطبقات العليا بما في ذلك ratchet وstreaming. الرسائل الصغيرة المتقطعة مثل streaming acks سيتم توسيعها إلى 1 كيلوبايت لكل منها. ومع ذلك، ضغط gzip في طبقة I2CP قد يقلل السعة بشكل كبير.

أبسط تنفيذ في router الطالب هو استخدام متوسط وأدنى و/أو أقصى عرض نطاق للأنفاق الحالية في المجموعة لحساب القيم التي توضع في الطلب. خوارزميات أكثر تعقيداً ممكنة وتترك للمطور.

لا توجد حالياً خيارات I2CP أو SAM محددة للعميل لإخبار الـ router بمقدار النطاق الترددي المطلوب، ولا يتم اقتراح خيارات جديدة هنا. قد يتم تعريف الخيارات في تاريخ لاحق إذا لزم الأمر.

قد تستخدم التطبيقات عرض النطاق الترددي المتاح أو أي بيانات أخرى أو خوارزمية أو سياسة محلية أو تكوين محلي لحساب قيمة عرض النطاق الترددي المُعادة في استجابة البناء.

## المراجع

- [الهياكل المشتركة](/docs/specs/common-structures/)
- [التشفير](/docs/specs/cryptography/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ECIES-X25519](/docs/specs/ecies/)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)
- [I2NP](/docs/specs/i2np/)
- [التشفير المتعدد](https://en.wikipedia.org/wiki/Multiple_encryption)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop119](/proposals/119/)
- [Prop143](/proposals/143/)
- [Prop152](/proposals/152/)
- [Prop153](/proposals/153/)
- [Prop156](/proposals/156/)
- [Prop157](/proposals/157/)
- [Prop168](/proposals/168/)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [إنشاء الـ tunnel](/docs/specs/tunnel-creation/)
