---
title: "دليل عمليات Tunnel"
description: "مواصفة موحّدة لبناء وتشفير ونقل حركة المرور عبر I2P tunnels."
slug: "implementation"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

> **النطاق:** يوحّد هذا الدليل تنفيذ tunnel، وتنسيق الرسائل، ومواصفتي إنشاء tunnel (ECIES و ElGamal القديم). تواصل الروابط العميقة الحالية العمل عبر الأسماء المستعارة المذكورة أعلاه.

## نموذج Tunnel {#tunnel-model}

I2P يمرّر الحمولات عبر *tunnels أحادية الاتجاه*: مجموعات مرتّبة من routers تنقل حركة المرور في اتجاه واحد. تتطلّب الرحلة الكاملة ذهاباً وإياباً بين وجهتين أربع tunnels (اثنتان صادرتان، واثنتان واردتان).

ابدأ بقراءة [Tunnel Overview](/docs/overview/tunnel-routing/) للتعرّف على المصطلحات، ثم استخدم هذا الدليل للتفاصيل التشغيلية.

### دورة حياة الرسالة {#message-lifecycle}

1. تقوم **بوابة** tunnel بتجميع رسالة I2NP واحدة أو أكثر على دفعات، وتجزئها، وتكتب تعليمات التسليم.
2. تُغلِّف البوابة الحمولة داخل رسالة tunnel ثابتة الحجم (1024&nbsp;B)، وتضيف حشواً عند الحاجة.
3. يتحقق كل **مشارك** من القفزة السابقة، ويطبق طبقة التشفير الخاصة به، ويمرّر {nextTunnelId, nextIV, encryptedPayload} إلى القفزة التالية.
4. تزيل **نقطة نهاية** tunnel الطبقة النهائية، وتستهلك تعليمات التسليم، وتعيد تجميع الشظايا، وترسل رسائل I2NP المُعاد بناؤها.

يستخدم كشف التكرار Bloom filter (بنية بيانات احتمالية) متناقصاً مفهرساً بمفتاح ناتج عملية XOR بين IV (متجه التهيئة) وأول كتلة من النص المُعَمّى، لمنع هجمات التوسيم المبنية على تبديل IV.

### لمحة سريعة عن الأدوار {#roles}

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Pre-processing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Crypto Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Post-processing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound gateway (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively <em>decrypt</em> using every hop’s keys (so downstream peers encrypt)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to first hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt IV and payload with hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt once more to reveal plaintext payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deliver to target tunnel/destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt with local keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound endpoint (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt using stored hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble and deliver locally</td>
    </tr>
  </tbody>
</table>
### سير عمل التشفير {#encryption-workflow}

- **Inbound tunnels:** تُشفِّر البوابة مرة واحدة باستخدام مفتاح الطبقة الخاص بها؛ ويواصل المشاركون اللاحقون التشفير إلى أن يقوم المُنشئ بفك تشفير الحمولة النهائية.
- **Outbound tunnels:** تُطبِّق البوابة مسبقًا معكوس تشفير كل قفزة بحيث يقوم كل مشارك بالتشفير. وعندما تقوم نقطة النهاية بالتشفير، ينكشف النص الواضح الأصلي للبوابة.

كلا الاتجاهين يمرران `{tunnelId, IV, encryptedPayload}` إلى القفزة التالية.

---

## تنسيق رسالة Tunnel {#tunnel-message-format}

بوابات Tunnel (نفق) تقسّم رسائل I2NP إلى أغلفة ثابتة الحجم لإخفاء طول الحمولة وتبسيط المعالجة عند كل قفزة.

### البنية المشفّرة {#encrypted-layout}

```
+----------------+----------------+-------------------+
| Tunnel ID (4B) | IV (16B)       | Encrypted payload |
+----------------+----------------+-------------------+
```
- **Tunnel ID** – معرّف 32-بت للقفزة التالية (غير صفري، يتغير في كل دورة بناء).
- **IV** (متجه التهيئة) – بطول 16 بايت لـ AES، يُختار لكل رسالة.
- **Encrypted payload** – 1008 بايت من نص مشفّر بـ AES-256-CBC.

إجمالي الحجم: 1028 بايت.

### تخطيط بعد فك التشفير {#decrypted-layout}

بعد أن تُزيل القفزة طبقة التشفير الخاصة بها:

```
[Checksum (4B)][Padding ... 0x00 terminator]
[Delivery Instructions 1][I2NP fragment 1]
[Delivery Instructions 2][I2NP fragment 2]
...
```
- **المجموع الاختباري** يتحقق من صحة الكتلة بعد فك التشفير.
- **الحشو** عبارة عن بايتات عشوائية غير صفرية تنتهي ببايت صفري.
- **تعليمات التسليم** تُخبر نقطة النهاية بكيفية التعامل مع كل جزء (تسليم محلي، إعادة التوجيه إلى tunnel آخر، إلخ).
- **الأجزاء** تحمل رسائل I2NP الأساسية؛ تقوم نقطة النهاية بإعادة تجميعها قبل تمريرها إلى الطبقات العليا.

### خطوات المعالجة {#processing-steps}

1. تقوم البوابات بتجزئة رسائل I2NP ووضعها في قائمة انتظار، مع الاحتفاظ بالقطع الجزئية لفترة وجيزة لإعادة تجميعها.
2. تقوم البوابة بتشفير الحمولة باستخدام مفاتيح الطبقة المناسبة وتُدرج معرّف الـ tunnel بالإضافة إلى متجه التهيئة (IV).
3. يقوم كل مشارك بتشفير متجه التهيئة (AES-256/ECB) ثم الحمولة (AES-256/CBC) قبل إعادة تشفير متجه التهيئة وتمرير الرسالة.
4. يفك الطرف النهائي التشفير بترتيب عكسي، ويتحقق من المجموع الاختباري، وينفّذ تعليمات التسليم، ويعيد تجميع الأجزاء.

---

## إنشاء Tunnel (ECIES-X25519) {#tunnel-creation-ecies}

تبني routers الحديثة tunnels باستخدام مفاتيح ECIES-X25519، ما يقلّص رسائل البناء ويتيح السرية المستقبلية.

- **رسالة البناء:** تحمل رسالة I2NP واحدة من نوع `TunnelBuild` (أو `VariableTunnelBuild`) ما بين 1–8 سجلات بناء مشفّرة، سجل واحد لكل قفزة.
- **مفاتيح الطبقة:** يستمدّ المنشئون مفاتيح الطبقة لكل قفزة، وIV، ومفاتيح الرد عبر HKDF باستخدام هوية X25519 الثابتة لتلك القفزة ومفتاح المنشئ المؤقت.
- **المعالجة:** تفك كل قفزة تشفير سجلها، وتتحقق من أعلام الطلب، وتكتب كتلة الرد (نجاح أو رمز فشل مفصّل)، وتعيد تشفير السجلات المتبقية، ثم تمرّر الرسالة.
- **الردود:** يتلقى المنشئ رسالة رد مغلّفة بطريقة garlic (garlic encryption). السجلات الموسومة كفاشلة تتضمن رمز مستوى الخطورة بحيث يمكن للـrouter إنشاء ملف تعريفي للند.
- **التوافق:** قد تظل routers تقبل أبنية ElGamal القديمة للتوافق مع الإصدارات السابقة، لكن tunnels الجديدة تستخدم ECIES افتراضيًا.

> للاطلاع على ملاحظات حول الثوابت لكل حقل واشتقاق المفاتيح، راجع تاريخ مقترح ECIES وشفرة مصدر router؛ يغطي هذا الدليل التدفق التشغيلي.

---

## إنشاء Tunnel الموروث (ElGamal-2048) {#tunnel-creation-elgamal}

كان تنسيق إنشاء tunnel الأصلي يستخدم مفاتيح ElGamal العامة. تحافظ routers الحديثة على دعم محدود لأغراض التوافق مع الإصدارات السابقة.

> **الحالة:** متقادم. مُحتفَظ به هنا كمرجع تاريخي ولأي شخص يقوم بصيانة أدوات متوافقة مع الإصدارات القديمة.

- **بناء تلسكوبي غير تفاعلي:** تمر رسالة بناء واحدة عبر المسار بأكمله. تفك كل قفزة تشفير سجلها بحجم 528 بايت، تحدّث الرسالة، ثم تعيد توجيهها.
- **طول متغيّر:** سمحت رسالة بناء Tunnel المتغيرة (VTBM) بوجود 1–8 سجلات. أما الرسالة الثابتة الأقدم فكانت تحتوي دائماً على ثمانية سجلات لإخفاء طول tunnel.
- **بنية سجل الطلب:**

```
Bytes 0–3    : Tunnel ID (receiving ID)
Bytes 4–35   : Current hop router hash
Bytes 36–39  : Next tunnel ID
Bytes 40–71  : Next hop router hash
Bytes 72–103 : AES-256 layer key
Bytes 104–135: AES-256 IV key
Bytes 136–167: AES-256 reply key
Bytes 168–183: AES-256 reply IV
Byte 184     : Flags (bit7=IBGW, bit6=OBEP)
Bytes 185–188: Request time (hours since epoch)
Bytes 189–192: Next message ID
Bytes 193–221: Padding
```
- **الأعلام:** تشير البت 7 إلى بوابة واردة (IBGW)؛ وتُميِّز البت 6 نقطةً نهائيةً صادرة (OBEP). وهما متنافيتان.
- **التشفير:** يُشفَّر كل سجل بـ ElGamal-2048 باستخدام المفتاح العام للقفزة. تضمن طبقات التشفير المتماثل AES-256-CBC أن القفزة المقصودة فقط تستطيع قراءة سجلها.
- **حقائق أساسية:** معرّفات tunnel هي قيم 32-بت غير صفرية؛ وقد يُدرج المنشئون سجلات وهمية لإخفاء طول tunnel الفعلي؛ وتعتمد الموثوقية على إعادة محاولة عمليات البناء الفاشلة.

---

## تجمّعات Tunnel ودورة الحياة {#tunnel-pools}

تُحافظ Routers (موجّهات شبكة I2P) على مجمّعات مستقلة لـ tunnel (نفق اتصال في I2P) الواردة والصادرة للمرور الاستكشافي ولكل جلسة I2CP (بروتوكول عميل I2P).

- **اختيار النظائر:** تستخدم tunnels الاستكشافية حاوية النظائر “النشطة، غير المتعطلة” لتعزيز التنوع; بينما تفضّل tunnels الخاصة بالعميل النظائر السريعة وعالية السعة.
- **الترتيب الحتمي:** تُرتَّب النظائر بحسب مسافة XOR بين `SHA256(peerHash || poolKey)` ومفتاح المجموعة العشوائي. يتبدّل المفتاح عند إعادة التشغيل، ما يمنح استقرارًا ضمن التشغيل الواحد ويُربك predecessor attacks (هجمات تحديد العقد السابقة في المسار) عبر تشغيلات متعددة.
- **دورة الحياة:** تقوم routers بتتبّع أزمنة البناء التاريخية لكل رباعية {mode, direction, length, variance}. ومع اقتراب انتهاء صلاحية tunnels، يبدأ الاستبدال مبكرًا; كما يزيد router من عمليات البناء المتوازية عند حدوث إخفاقات، مع وضع حد أقصى للمحاولات القائمة.
- **خيارات الضبط:** أعداد tunnels النشطة/الاحتياطية، طول القفزات والتباين، السماح بلا قفزات، وحدود معدل البناء; جميعها قابلة للضبط لكل مجموعة.

---

## الازدحام والموثوقية {#congestion}

على الرغم من أن tunnels تشبه الدارات، فإن routers تتعامل معها كطوابير رسائل. يُستخدم الإسقاط المبكر العشوائي الموزون (WRED) للإبقاء على الكمون ضمن حدود محددة:

- ترتفع احتمالية الإسقاط مع اقتراب مستوى الاستخدام من الحدود المُكوَّنة.
- يأخذ المشاركون في الاعتبار أجزاء ثابتة الحجم؛ تقوم البوابات/نقاط النهاية بالإسقاط استناداً إلى الحجم المُجمَّع للأجزاء، مع ترجيح إسقاط الحمولات الكبيرة أولاً.
- تقوم نقاط النهاية الصادرة بالإسقاط قبل الأدوار الأخرى لتقليل إهدار جهد الشبكة إلى أدنى حد.

يُترك التسليم المضمون للطبقات العليا مثل [Streaming library](/docs/specs/streaming/). يجب على التطبيقات التي تتطلب الموثوقية أن تتولى بنفسها إعادة الإرسال وإقرارات الاستلام.

---

## قراءات إضافية {#further-reading}

- [Tunnels أحادية الاتجاه (تاريخية)](/docs/legacy/unidirectional-tunnels/)
- [اختيار الأقران](/docs/overview/tunnel-routing#peer-selection/)
- [نظرة عامة على Tunnel](/docs/overview/tunnel-routing/)
- [التنفيذ القديم لـ Tunnel](/docs/legacy/old-implementation/)
