---
title: "بروتوكول العميل لـ I2P (I2CP)"
description: "كيف تتفاوض التطبيقات بشأن الجلسات وtunnels وLeaseSets مع I2P router."
slug: "i2cp"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## نظرة عامة

I2CP هو بروتوكول تحكم منخفض المستوى بين I2P router وأي عملية عميل. يحدّد فصلاً صارماً للمسؤوليات:

- **Router**: يدير التوجيه، والتشفير، ودورات حياة الـ tunnel، وعمليات قاعدة بيانات الشبكة
- **العميل**: يختار خصائص إخفاء الهوية، ويُكوّن tunnels، ويرسل/يتلقى الرسائل

تمرّ جميع الاتصالات عبر مقبس TCP واحد (اختياريًا مُغلّف بـ TLS)، مما يتيح عمليات غير متزامنة وبازدواج كامل.

**إصدار البروتوكول**: تستخدم I2CP بايت إصدار البروتوكول `0x2A` (42 بالنظام العشري) يُرسَل أثناء إقامة الاتصال الأولي. لقد ظل هذا البايت الخاص بالإصدار مستقراً منذ نشأة البروتوكول.

**الحالة الحالية**: هذه المواصفة تنطبق على إصدار router 0.9.67 (إصدار API 0.9.67)، الصادر في 2025-09.

## سياق التنفيذ

### تنفيذ جافا

التنفيذ المرجعي موجود في Java I2P: - SDK للعميل: حزمة `i2p.jar` - تنفيذ الـ router (برنامج التوجيه في I2P): حزمة `router.jar` - [Javadocs](http://docs.i2p-projekt.de/javadoc/)

عندما يعمل العميل وrouter ضمن نفس بيئة JVM (آلة جافا الافتراضية)، تُنقَل رسائل I2CP على شكل كائنات Java من دون إجراء تسلسل. يستخدم العملاء الخارجيون البروتوكول المُسَلسَل عبر TCP.

### تنفيذ C++

يطبّق i2pd (الـ I2P router المكتوب بـ C++) بروتوكول I2CP خارجيًا لاتصالات العملاء.

### العملاء غير المكتوبين بلغة Java

لا توجد **تنفيذات غير مكتوبة بـ Java معروفة** لمكتبة عميل I2CP كاملة. ينبغي للتطبيقات غير المكتوبة بـ Java استخدام بروتوكولات على مستوى أعلى بدلاً من ذلك:

- **SAM (المراسلة المجهولة البسيطة) v3**: واجهة قائمة على المقابس مع مكتبات بلغات متعددة
- **BOB (الجسر المفتوح الأساسي)**: بديل أبسط لـ SAM

تعالج هذه البروتوكولات عالية المستوى تعقيدات I2CP داخليًا، كما توفر أيضًا مكتبة التدفق (للاتصالات المشابهة لـ TCP) ومكتبة الداتاغرام (للاتصالات المشابهة لـ UDP).

## إقامة الاتصال

### 1. اتصال TCP

اتصل بمنفذ I2CP الخاص بـ router: - القيمة الافتراضية: `127.0.0.1:7654` - قابلة للتهيئة عبر إعدادات router - غلاف TLS اختياري (يوصى به بشدة للاتصالات عن بُعد)

### 2. مصافحة البروتوكول

**الخطوة 1**: أرسل بايت إصدار البروتوكول `0x2A`

**الخطوة 2**: مزامنة الساعة

```
Client → Router: GetDateMessage
Router → Client: SetDateMessage
```
يُرجِع الـ router الطابع الزمني الحالي وسلسلة إصدار واجهة برمجة تطبيقات I2CP (بروتوكول التحكّم في I2P) (منذ الإصدار 0.8.7).

**الخطوة 3**: المصادقة (إذا كانت مفعّلة)

اعتبارًا من 0.9.11، يمكن تضمين المصادقة في GetDateMessage عبر Mapping (خريطة مفاتيح/قيم) تتضمن: - `i2cp.username` - `i2cp.password`

اعتبارًا من الإصدار 0.9.16، عندما تكون المصادقة مُفعَّلة، **يجب** إتمامها عبر GetDateMessage قبل إرسال أي رسائل أخرى.

**الخطوة 4**: إنشاء الجلسة

```
Client → Router: CreateSessionMessage (contains SessionConfig)
Router → Client: SessionStatusMessage (status=Created)
```
**الخطوة 5**: إشارة جاهزية Tunnel

```
Router → Client: RequestVariableLeaseSetMessage
```
تشير هذه الرسالة إلى أنه تم بناء الـ tunnels الواردة. لن يقوم الـ router بإرسالها إلا بعد توفر tunnel وارد واحد على الأقل وtunnel صادر واحد.

**الخطوة 6**: نشر LeaseSet

```
Client → Router: CreateLeaseSet2Message
```
في هذه المرحلة، تكون الجلسة جاهزة للعمل بالكامل لإرسال الرسائل واستقبالها.

## أنماط تدفق الرسائل

### رسالة صادرة (يرسلها العميل إلى وجهة بعيدة)

**مع i2cp.messageReliability=none**:

```
Client → Router: SendMessageMessage (nonce=0)
[No acknowledgments]
```
**مع i2cp.messageReliability=BestEffort**:

```
Client → Router: SendMessageMessage (nonce>0)
Router → Client: MessageStatusMessage (status=Accepted)
Router → Client: MessageStatusMessage (status=Success or Failure)
```
### رسالة واردة (Router يسلّمها إلى العميل)

**مع i2cp.fastReceive=true** (الإعداد الافتراضي منذ 0.9.4):

```
Router → Client: MessagePayloadMessage
[No acknowledgment required]
```
**مع i2cp.fastReceive=false** (مهمل):

```
Router → Client: MessageStatusMessage (status=Available)
Client → Router: ReceiveMessageBeginMessage
Router → Client: MessagePayloadMessage
Client → Router: ReceiveMessageEndMessage
```
ينبغي على العملاء الحديثين دائمًا استخدام وضع الاستقبال السريع.

## هياكل البيانات الشائعة

### ترويسة رسالة I2CP

تستخدم جميع رسائل I2CP هذه الترويسة المشتركة:

```
+----+----+----+----+----+----+----+----+
| Body Length (4 bytes)                 |
+----+----+----+----+----+----+----+----+
|Type|  Message Body (variable)        |
+----+----+----+----+----+----+----+----+
```
- **طول جسم الرسالة**: عدد صحيح بطول 4 بايت، طول جسم الرسالة فقط (لا يشمل الترويسة)
- **النوع**: عدد صحيح بطول 1 بايت، معرّف نوع الرسالة
- **جسم الرسالة**: 0 بايت فأكثر، يختلف التنسيق بحسب نوع الرسالة

**حد حجم الرسالة**: تقريبًا 64 كيلوبايت كحد أقصى.

### معرّف الجلسة

عدد صحيح بطول 2 بايت يعرّف جلسة بشكل فريد على router.

**قيمة خاصة**: `0xFFFF` تشير إلى "بدون جلسة" (تُستخدم لاستعلامات اسم المضيف من دون جلسة قائمة).

### معرّف الرسالة

عدد صحيح بطول 4 بايت يتم توليده بواسطة router لتحديد رسالة بشكل فريد ضمن جلسة.

**مهم**: معرّفات الرسائل **ليست** فريدة عالميًا، بل فريدة ضمن الجلسة فقط. كما أنها تختلف أيضًا عن الـ nonce (عدد يُستخدم مرة واحدة) الذي يولّده العميل.

### تنسيق الحمولة

يتم ضغط حمولات الرسائل باستخدام gzip مع ترويسة gzip قياسية بطول 10 بايت: - تبدأ بـ: `0x1F 0x8B 0x08` (RFC 1952) - منذ 0.7.1: تحتوي الأجزاء غير المستخدمة من ترويسة gzip على معلومات البروتوكول، ومنفذ المصدر، ومنفذ الوجهة - يتيح هذا استخدام streaming (اتصالات متدفقة) و datagrams (رسائل عديمة الاتصال) على الوجهة نفسها

**التحكم في الضغط**: اضبط `i2cp.gzip=false` لتعطيل الضغط (يضبط مستوى جهد gzip إلى 0). تظل ترويسة gzip مُضمّنة، ولكن مع حد أدنى من العبء الإضافي للضغط.

### بنية SessionConfig

يحدد إعدادات جلسة عميل:

```
+----------------------------------+
| Destination                      |
+----------------------------------+
| Mapping (configuration options)  |
+----------------------------------+
| Creation Date                    |
+----------------------------------+
| Signature                        |
+----------------------------------+
```
**المتطلبات الحرجة**: 1. **يجب أن يكون التعيين مرتبًا حسب المفتاح** لأغراض التحقق من التوقيع 2. **تاريخ الإنشاء** يجب أن يكون ضمن ±30 ثانية من الوقت الحالي للـ router 3. **التوقيع** يتم إنشاؤه بواسطة SigningPrivateKey (مفتاح التوقيع الخاص) الخاص بالـ Destination (الوجهة)

**التواقيع غير المتصلة** (اعتبارًا من 0.9.38):

عند استخدام التوقيع دون اتصال، يجب أن يحتوي التعيين على:
- `i2cp.leaseSetOfflineExpiration`
- `i2cp.leaseSetTransientPublicKey`
- `i2cp.leaseSetOfflineSignature`

بعد ذلك يتم إنشاء Signature بواسطة SigningPrivateKey المؤقت.

## خيارات تكوين النواة

### إعدادات Tunnel

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby inbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby outbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
  </tbody>
</table>
**ملاحظات**: - القيم لـ `quantity` > 6 تتطلب أقرانًا يشغّلون الإصدار 0.9.0+ وتزيد بشكل ملحوظ من استهلاك الموارد - اضبط `backupQuantity` على 1-2 للخدمات عالية التوفّر - Zero-hop tunnels تُضحّي بإخفاء الهوية لتقليل الكمون لكنها مفيدة للاختبار

### معالجة الرسائل

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>clientMessageTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">60000&nbsp;ms</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy timeout for message delivery</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.messageReliability</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">BestEffort</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>None</code>, <code>BestEffort</code>, or <code>Guaranteed</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.fastReceive</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Skip ReceiveMessageBegin/End handshake (default since 0.9.4)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.gzip</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Enable gzip compression of message payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.priority</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Priority for outbound scheduling (-25 to +25)</td>
    </tr>
  </tbody>
</table>
**موثوقية الرسائل**: - `None`: لا توجد إقرارات من router (الموجّه في I2P) (الافتراضي في مكتبة البث منذ 0.8.1) - `BestEffort`: يرسل router إشعار قبول + إشعارات نجاح/فشل - `Guaranteed`: غير مُنفّذ (حاليًا يتصرّف مثل BestEffort)

**تجاوز لكل رسالة** (منذ 0.9.14): - في جلسة تكون فيها `messageReliability=none`، فإن تعيين قيمة nonce غير صفرية يطلب إشعار تسليم لتلك الرسالة المحددة - تعيين nonce=0 في جلسة `BestEffort` يعطّل الإشعارات لتلك الرسالة

### تكوين LeaseSet (بنية بيانات تحدد كيفية الوصول إلى وجهة داخل I2P)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.dontPublishLeaseSet</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disable automatic LeaseSet publication (for client-only destinations)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet variant: 1 = standard, 3 = LS2, 5 = encrypted, 7 = meta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated encryption type codes (see below)</td>
    </tr>
  </tbody>
</table>
### وسوم الجلسة القديمة لـ ElGamal/AES

تنطبق هذه الخيارات فقط على تشفير ElGamal القديم (خوارزمية تشفير بالمفتاح العام):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.lowTagThreshold</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum session tags before replenishing</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.tagsToSend</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of tags to send in a batch</td>
    </tr>
  </tbody>
</table>
**ملاحظة**: يستخدمون عملاء ECIES-X25519 آلية ratchet (آلية تحديث مفاتيح تدريجية) مختلفة ويتجاهلون هذه الخيارات.

## أنواع التشفير

يدعم I2CP عدة مخططات لتشفير من طرف إلى طرف عبر الخيار `i2cp.leaseSetEncType`. يمكن تحديد أنواع متعددة (مفصولة بفواصل) لدعم كل من النظراء الحديثين والقدامى.

### أنواع التشفير المدعومة

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32-byte X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current Standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-768 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-1024 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (likely ML-KEM-512 hybrid)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Future</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Planned</td>
    </tr>
  </tbody>
</table>
**التكوين الموصى به**:

```
i2cp.leaseSetEncType=4,0
```
يوفّر هذا دعمًا لـ X25519 (المفضّل) مع ElGamal كخيار بديل لأغراض التوافق.

### تفاصيل نوع التشفير

**النوع 0 - ElGamal/AES+وسوم الجلسة**: - مفاتيح ElGamal العامة بطول 2048-بت (256 بايت) - تشفير متماثل AES-256 - وسوم الجلسة بطول 32 بايت تُرسل على دفعات - عبء عالٍ على المعالج والنطاق الترددي والذاكرة - يتم التخلص منه تدريجياً على مستوى الشبكة

**النوع 4 - ECIES-X25519-AEAD-Ratchet**: - تبادل مفاتيح X25519 (مفاتيح بحجم 32 بايت) - ChaCha20/Poly1305 AEAD - Double Ratchet بأسلوب Signal (المسنّن المزدوج) - وسوم جلسة بحجم 8 بايت (مقارنةً بـ 32 بايت في ElGamal) - تُولَّد الوسوم عبر PRNG متزامن (مولّد أعداد عشوائية زائف) (لا تُرسَل مسبقاً) - خفض الحمل الإضافي بنحو ~92% مقارنةً بـ ElGamal - المعيار في I2P الحديثة (تستخدمه معظم routers)

**النوعان 5-6 - هجين ما بعد الكم**: - يجمع بين X25519 و ML-KEM (NIST FIPS 203) - يوفر أمانًا مقاومًا للكم - ML-KEM-768 لتحقيق توازن بين الأمان والأداء - ML-KEM-1024 لأقصى درجات الأمان - أحجام رسائل أكبر بسبب بيانات مفاتيح PQ (ما بعد الكم) - لا يزال دعم الشبكة قيد النشر

### استراتيجية الترحيل

شبكة I2P تنتقل بنشاط من ElGamal (النوع 0) إلى X25519 (النوع 4): - NTCP → NTCP2 (مكتمل) - SSU → SSU2 (مكتمل) - ElGamal tunnels → X25519 tunnels (مكتمل) - ElGamal من طرف إلى طرف → ECIES-X25519 (مكتمل في معظمه)

## LeaseSet2 (الجيل الثاني من تنسيق leaseSet في I2P) والميزات المتقدمة

### خيارات LeaseSet2 (منذ 0.9.38)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies LeaseSet variant (1, 3, 5, 7)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encryption types supported (comma-separated)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetAuthType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-client authentication: 0 = none, 1 = DH, 2 = PSK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 private key for decrypting LS2 with auth</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetSecret</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Base64 secret for blinded addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetTransientPublicKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transient signing key for offline signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivateKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Persistent LeaseSet encryption keys (type:key pairs)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetOption.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Service records (proposal 167)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.dh.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth material (indexed from 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.psk.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth material (indexed from 0)</td>
    </tr>
  </tbody>
</table>
### العناوين المعماة

اعتبارًا من 0.9.39، يمكن للوجهات استخدام عناوين "blinded" (مطموسة الهوية) (b33 format) التي تتغير دوريًا: - يتطلب `i2cp.leaseSetSecret` للحماية بكلمة مرور - مصادقة لكل عميل اختيارية - راجع المقترحين 123 و149 للتفاصيل

### سجلات الخدمة (منذ 0.9.66)

يدعم LeaseSet2 خيارات سجل الخدمة (المقترح 167):

```
i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 mail.example.b32.i2p
```
يتبع التنسيق أسلوب سجل SRV في DNS، ولكن مع تكييفه لـ I2P.

## جلسات متعددة (منذ 0.9.21)

يمكن لاتصال I2CP واحد إدارة جلسات متعددة:

**الجلسة الأساسية**: أول جلسة يتم إنشاؤها ضمن اتصال **الجلسات الفرعية**: جلسات إضافية تشترك في مجموعة الـ tunnel الخاصة بالجلسة الأساسية

### خصائص الجلسة الفرعية

1. **Tunnels مشتركة**: استخدم مجمّعات tunnel الواردة/الصادرة نفسها كما في الجلسة الأساسية
2. **مفاتيح تشفير مشتركة**: يجب استخدام مفاتيح تشفير LeaseSet متطابقة
3. **مفاتيح توقيع مختلفة**: يجب استخدام مفاتيح توقيع Destination (الوجهة في I2P) مختلفة
4. **لا ضمان لإخفاء الهوية**: مرتبطة بوضوح بالجلسة الأساسية (نفس router، نفس tunnels)

### حالة استخدام Subsession (جلسة فرعية)

تمكين التواصل مع الوجهات باستخدام أنواع توقيع مختلفة: - الأساسي: توقيع EdDSA (حديث) - Subsession (جلسة فرعية): توقيع DSA (التوافق مع الإصدارات القديمة)

### دورة حياة الجلسة الفرعية

**الإنشاء**:

```
Client → Router: CreateSessionMessage
Router → Client: SessionStatusMessage (unique Session ID)
Router → Client: RequestVariableLeaseSetMessage (separate for each destination)
Client → Router: CreateLeaseSet2Message (separate for each destination)
```
**التدمير**: - تدمير جلسة فرعية: يبقي الجلسة الأساسية سليمة - تدمير الجلسة الأساسية: يدمر جميع الجلسات الفرعية ويغلق الاتصال - DisconnectMessage: يدمر جميع الجلسات

### التعامل مع معرّف الجلسة

تحتوي معظم رسائل I2CP على حقل معرّف الجلسة. الاستثناءات: - DestLookup / DestReply (مهملة، استخدم HostLookup / HostReply) - GetBandwidthLimits / BandwidthLimits (الاستجابة ليست خاصة بجلسة معينة)

**مهم**: ينبغي ألا يكون لدى العملاء عدة رسائل CreateSession (رسالة إنشاء جلسة) معلّقة في آن واحد، إذ لا يمكن ربط الاستجابات بالطلبات بشكل لا لبس فيه.

## فهرس الرسائل

### ملخص أنواع الرسائل

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Direction</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReconfigureSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestroySession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessage</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageBegin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageEnd</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SessionStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">29</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReportAbuse</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disconnect</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">31</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessagePayload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">33</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">35</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">36</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">37</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">42</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>
**المفتاح**: C = عميل، R = Router

### تفاصيل الرسالة الرئيسية

#### CreateSessionMessage (رسالة إنشاء جلسة) (النوع 1)

**الغرض**: بدء جلسة I2CP جديدة

**المحتوى**: بنية SessionConfig

**الاستجابة**: SessionStatusMessage (status=Created أو Invalid)

**المتطلبات**: - يجب أن يكون التاريخ في SessionConfig ضمن ±30 ثانية من وقت router - يجب أن يكون التعيين مرتبًا حسب المفتاح للـتحقق من صحة التوقيع - يجب ألا تكون لدى الوجهة جلسة نشطة مسبقًا

#### RequestVariableLeaseSetMessage (النوع 37)

**الغرض**: يطلب Router إذن العميل من أجل tunnels الواردة

**المحتوى**: - معرّف الجلسة - عدد إدخالات Lease (مصطلح في I2P يشير إلى إدخال مرتبط بـ tunnel وفترة صلاحيته) - مصفوفة من هياكل Lease (لكلٍ منها انتهاء صلاحية مستقل)

**الاستجابة**: CreateLeaseSet2Message

**الأهمية**: هذه هي الإشارة على أن الجلسة قيد التشغيل. لا يرسل router هذا إلا بعد: 1. تم إنشاء inbound tunnel واحد على الأقل 2. تم إنشاء outbound tunnel واحد على الأقل

**توصية بشأن المهلة**: ينبغي للعملاء إنهاء الجلسة إذا لم يتم استلام هذه الرسالة بعد مرور 5 دقائق أو أكثر على إنشاء الجلسة.

#### CreateLeaseSet2Message (النوع 41)

**الغرض**: العميل ينشر LeaseSet إلى قاعدة بيانات الشبكة

**المحتوى**: - معرّف الجلسة - بايت نوع الـ LeaseSet (1، 3، 5، أو 7) - LeaseSet أو LeaseSet2 أو EncryptedLeaseSet أو MetaLeaseSet - عدد المفاتيح الخاصة - قائمة المفاتيح الخاصة (واحد لكل مفتاح عام في LeaseSet، بنفس الترتيب)

**المفاتيح الخاصة**: مطلوبة لفك تشفير رسائل garlic (تقنية تغليف في I2P) الواردة. التنسيق:

```
Encryption type (2 bytes)
Key length (2 bytes)
Private key data (variable)
```
**ملاحظة**: يحل محل CreateLeaseSetMessage (رسالة إنشاء LeaseSet) (النوع 4) المهملة، والتي لا يمكنها التعامل مع: - متغيرات LeaseSet2 - التشفير غير القائم على ElGamal - أنواع تشفير متعددة - LeaseSets مشفرة - مفاتيح توقيع غير متصلة

#### SendMessageExpiresMessage (النوع 36)

**الغرض**: إرسال رسالة إلى الوجهة مع وقت انتهاء الصلاحية وخيارات متقدمة

**المحتوى**: - معرّف الجلسة - الوجهة - الحمولة (gzipped، مضغوط باستخدام gzip) - Nonce (عدد يُستعمل مرة واحدة، 4 بايت) - الأعلام (2 بايت) - انظر أدناه - تاريخ الانتهاء (6 بايت، مقتطع من 8)

**حقل الأعلام** (2 بايت، ترتيب البتات 15...0):

**البتات 15-11**: غير مستخدمة، يجب أن تكون 0

**البتّات 10-9**: تجاوز اعتمادية الرسالة (غير مستخدم، استخدم nonce (عدد يُستخدم مرة واحدة) بدلاً من ذلك)

**البت 8**: لا تقم بتضمين LeaseSet - 0: قد يقوم Router بتضمين LeaseSet ضمن garlic (رسالة garlic في I2P) - 1: لا تقم بتضمين LeaseSet

**البتات 7-4**: عتبة الوسوم الدنيا (ElGamal فقط، يتم تجاهلها في ECIES)

```
0000 = Use session settings
0001 = 2 tags
0010 = 3 tags
...
1111 = 192 tags
```
**البتات 3-0**: وسوم تُرسل عند الحاجة (لـ ElGamal (نظام تشفير بالمفتاح العام) فقط، ويتم تجاهلها مع ECIES (مخطط تشفير متكامل بالمنحنيات البيضوية))

```
0000 = Use session settings
0001 = 2 tags
0010 = 4 tags
...
1111 = 160 tags
```
#### MessageStatusMessage (رسالة حالة الرسالة، النوع 22)

**الغرض**: إخطار العميل بحالة تسليم الرسالة

**المحتوى**: - معرّف الجلسة - معرّف الرسالة (مولَّد بواسطة router) - رمز الحالة (1 بايت) - الحجم (4 بايت، ذو صلة فقط عندما يكون status=0) - Nonce (رقم يُستخدم مرة واحدة؛ 4 بايت، يطابق nonce الخاص بعملية SendMessage لدى العميل)

**رموز الحالة** (الرسائل الصادرة):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Accepted</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router accepted message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Delivered to local client</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local delivery failed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown/error</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No network connectivity</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid/closed session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid options/expiration</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Overflow Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queue/buffer full</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message Expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired before send</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Local LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local LeaseSet problem</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Local Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No tunnels available</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsupported Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet not found</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Meta Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot send to meta LS</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Loopback Denied</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Same source and destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
  </tbody>
</table>
**رموز النجاح**: 1, 2, 4, 6 **رموز الفشل**: جميع الرموز الأخرى

**رمز الحالة 0** (مهمل): رسالة متاحة (واردة، الاستقبال السريع معطل)

#### HostLookupMessage (النوع 38)

**الغرض**: الاستعلام عن الوجهة باستخدام اسم المضيف أو التجزئة (يحل محل DestLookup)

**المحتوى**: - معرّف الجلسة (أو 0xFFFF لعدم وجود جلسة) - معرّف الطلب (4 بايت) - المهلة بالميلي ثانية (4 بايت، الحد الأدنى الموصى به: 10000) - نوع الطلب (1 بايت) - مفتاح الاستعلام (Hash، اسم مضيف من النوع String، أو Destination (الوجهة))

**أنواع الطلبات**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lookup Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Returns</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
  </tbody>
</table>
تعيد الأنواع 2-4 خيارات LeaseSet (المقترح 167) إن توفرت.

**الاستجابة**: HostReplyMessage

#### HostReplyMessage (رسالة رد المضيف) (النوع 39)

**الغرض**: استجابة لـ HostLookupMessage (رسالة البحث عن المضيف)

**المحتوى**: - معرّف الجلسة - معرّف الطلب - رمز النتيجة (1 بايت) - الوجهة (موجودة عند النجاح، وأحياناً عند بعض حالات الفشل المحددة) - التعيين (فقط لأنواع البحث 2-4، وقد يكون فارغاً)

**رموز النتائج**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup succeeded</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Password Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires password</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Private Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires private key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Password and Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires both</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Decryption Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot decrypt LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Lookup Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet not found in netdb</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Type Unsupported</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router doesn't support this type</td>
    </tr>
  </tbody>
</table>
#### BlindingInfoMessage (رسالة معلومات الإعماء) (النوع 42)

**الغرض**: إعلام router بمتطلبات المصادقة الخاصة بـ blinded destination (وجهة مُعمّاة) (اعتبارًا من 0.9.43)

**المحتوى**: - معرّف الجلسة - الأعلام (1 بايت) - نوع نقطة النهاية (1 بايت): 0=تجزئة, 1=اسم المضيف, 2=الوجهة, 3=SigType+Key - نوع التوقيع الأعمى (2 بايت) - انتهاء الصلاحية (4 بايت, ثوانٍ منذ Epoch (بداية زمن يونكس)) - بيانات نقطة النهاية (تختلف حسب النوع) - المفتاح الخاص (32 بايت, فقط إذا كان بت العلم 0 مُعيّنًا) - كلمة مرور الاستعلام (سلسلة نصية, فقط إذا كان بت العلم 4 مُعيّنًا)

**الأعلام** (ترتيب البتات 76543210):

- **البت 0**: 0=الجميع، 1=لكل عميل
- **البتات 3-1**: آلية المصادقة (إذا كانت البت 0=1): 000=DH (ديفي-هيلمان)، 001=PSK (مفتاح مشترك مسبقًا)
- **البت 4**: 1=يتطلب سرًا
- **البتات 7-5**: غير مستخدمة، تُضبط إلى 0

**لا استجابة**: يعالج Router بصمت

**حالة استخدام**: قبل الإرسال إلى وجهة مُعمّاة (عنوان b33)، يجب على العميل إما أن: 1. إجراء استعلام عن b33 عبر HostLookup (استعلام المضيف)، أو 2. إرسال رسالة BlindingInfo (معلومات التعمية)

إذا كانت الوجهة تتطلب المصادقة، فإن BlindingInfo (معلومات التعمية العمياء) مطلوبة.

#### ReconfigureSessionMessage (رسالة إعادة تهيئة الجلسة) (النوع 2)

**الغرض**: تحديث تكوين الجلسة بعد إنشائها

**المحتوى**: - معرّف الجلسة - SessionConfig (فقط الخيارات التي تم تغييرها مطلوبة)

**الاستجابة**: SessionStatusMessage (رسالة حالة الجلسة) (status=Updated أو Invalid)

**ملاحظات**: - Router يدمج الإعدادات الجديدة مع الإعدادات الحالية - خيارات Tunnel (`inbound.*`, `outbound.*`) تُطبَّق دائمًا - قد تكون بعض الخيارات غير قابلة للتغيير بعد إنشاء الجلسة - يجب أن يكون التاريخ ضمن ±30 ثانية من وقت Router - يجب ترتيب التعيين حسب المفتاح

#### DestroySessionMessage (رسالة تدمير الجلسة) (النوع 3)

**الغرض**: إنهاء جلسة

**المحتوى**: معرّف الجلسة

**الاستجابة المتوقعة**: SessionStatusMessage (status=Destroyed)

**السلوك الفعلي** (Java I2P حتى الإصدار 0.9.66): - Router لا يرسل مطلقًا SessionStatus(Destroyed) - إذا لم تبقَ أي جلسات: يرسل DisconnectMessage - إذا بقيت جلسات فرعية: لا رد

**مهم**: يحيد سلوك Java I2P عن المواصفة. ينبغي على عمليات التنفيذ توخي الحذر عند تدمير الجلسات الفرعية الفردية.

#### DisconnectMessage (رسالة قطع الاتصال) (النوع 30)

**الغرض**: إشعار بأن الاتصال على وشك أن يتم إنهاؤه

**المحتوى**: سلسلة السبب

**التأثير**: تُدمَّر جميع الجلسات ضمن الاتصال، ويُغلَق المقبس

**التنفيذ**: بشكل أساسي router → العميل في Java I2P

## سجل إصدارات البروتوكول

### اكتشاف الإصدار

يتم تبادل إصدار بروتوكول I2CP ضمن رسائل Get/SetDate (منذ 0.8.7). بالنسبة إلى routers الأقدم، لا تتوفر معلومات الإصدار.

**سلسلة الإصدار**: تشير إلى إصدار واجهة برمجة التطبيقات (API) "core"، وليس بالضرورة إصدار router.

### الجدول الزمني للميزات

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.67</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PQ Hybrid ML-KEM (enc types 5-7) in LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.66</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Host lookup/reply extensions (proposal 167), service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.62</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus loopback error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.46</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 (enc type 4) in LeaseSet, ECIES end-to-end</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.43</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo message, extended HostReply failure codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet options, Meta LS error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2 message, RedDSA Ed25519 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Preliminary LS2 support (format changed in 0.9.39)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.21</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Multiple sessions on single connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.20</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional SetDate messages for clock shifts</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.16</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Authentication required before other messages (when enabled)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.15</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA Ed25519 signature type</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.14</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-message reliability override with nonzero nonce</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.12</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA P-256/384/521 signature types, RSA support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.11</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup/HostReply messages, auth in GetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.5</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional MessageStatus codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Fast receive mode default, nonce=0 allowed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag tag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">16 leases per LeaseSet (up from 6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Version strings in Get/SetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup in standard session, concurrent lookups</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>messageReliability=none</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits, BandwidthLimits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires, ReconfigureSession, ports in gzip header</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup, DestReply</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.6.5-</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original protocol features</td>
    </tr>
  </tbody>
</table>
## اعتبارات الأمان

### المصادقة

**الافتراضي**: لا يلزم إجراء مصادقة **اختياري**: مصادقة باسم مستخدم/كلمة مرور (منذ 0.9.11) **مطلوب**: عند التمكين، يجب إتمام المصادقة قبل الرسائل الأخرى (منذ 0.9.16)

**الاتصالات عن بُعد**: استخدم دائمًا TLS (`i2cp.SSL=true`) لحماية بيانات الاعتماد والمفاتيح الخاصة.

### انحراف الساعة

يجب أن يكون SessionConfig Date ضمن ±30 ثانية من وقت الـrouter، وإلا فسيتم رفض الجلسة. استخدم Get/SetDate للمزامنة.

### التعامل مع المفتاح الخاص

CreateLeaseSet2Message (رسالة إنشاء LeaseSet2) تحتوي على مفاتيح خاصة لفك تشفير الرسائل الواردة. يجب أن تكون هذه المفاتيح: - تُنقَل بأمان (TLS للاتصالات عن بُعد) - تُخزَّن بأمان بواسطة router - تُستبدل عند تعرّضها للاختراق

### انتهاء صلاحية الرسالة

استخدم دائمًا SendMessageExpires (وليس SendMessage) لتعيين وقت انتهاء صريح. هذا:
- يمنع وضع الرسائل في قائمة الانتظار إلى أجل غير مسمى
- يقلّل استهلاك الموارد
- يحسّن الموثوقية

### إدارة وسوم الجلسة

**ElGamal** (خوارزمية تشفير بالمفتاح العام) (مُهمَل): - يجب إرسال الوسوم على دفعات - فقدان الوسوم يؤدي إلى فشل فك التشفير - استهلاك مرتفع للذاكرة

**ECIES-X25519** (الحالي): - تُولَّد الوسوم عبر PRNG متزامن (مولّد أعداد شبه عشوائية) - لا حاجة إلى إرسال مسبق - مقاوم لفقدان الرسائل - حمل إضافي أقل بكثير

## أفضل الممارسات

### لمطوري العملاء

1. **استخدم وضع الاستلام السريع**: اضبط دائماً `i2cp.fastReceive=true` (أو اعتمد على القيمة الافتراضية)

2. **يفضل استخدام ECIES-X25519 (مخطط ECIES للتشفير بالمنحنيات الإهليلجية مع X25519)**: قم بتهيئة `i2cp.leaseSetEncType=4,0` لأفضل أداء مع الحفاظ على التوافق

3. **حدّد انتهاء الصلاحية صراحةً**: استخدم SendMessageExpires، وليس SendMessage

4. **تعامل مع subsessions (جلسات فرعية) بعناية**: كن على دراية بأن subsessions لا توفر أي إخفاء للهوية بين destinations (وجهات)

5. **مهلة إنشاء الجلسة**: أنهِ الجلسة إذا لم يتم استلام RequestVariableLeaseSet (اسم رسالة تطلب leaseSet متغيراً) خلال 5 دقائق

6. **فرز تعيينات التكوين**: احرص دائمًا على فرز مفاتيح Mapping قبل توقيع SessionConfig

7. **استخدم أعداد Tunnel المناسبة**: لا تضبط `quantity` > 6 إلا عند الضرورة

8. **ضع في الاعتبار SAM/BOB لغير Java**: نفّذ SAM بدلًا من I2CP مباشرةً

### لمطوري Router

1. **التحقق من التواريخ**: فرض نافذة زمنية قدرها ±30 ثانية على تواريخ SessionConfig

2. **تقييد حجم الرسالة**: فرض حد أقصى لحجم الرسالة قدره ~64 KB

3. **دعم الجلسات المتعددة**: تنفيذ دعم الجلسات الفرعية حسب مواصفة 0.9.21

4. **أرسل RequestVariableLeaseSet فورًا**: فقط بعد وجود كل من الـ inbound و الـ outbound tunnels

5. **التعامل مع الرسائل المهملة**: قبولها ولكن عدم التشجيع على استخدام ReceiveMessageBegin/End

6. **دعم ECIES-X25519 (مخطط تشفير بالمفتاح العام يعتمد X25519 وفق ECIES)**: أعطِ الأولوية لتشفير النوع 4 في عمليات النشر الجديدة

## تنقيح واستكشاف الأخطاء وإصلاحها

### المشكلات الشائعة

**تم رفض الجلسة (غير صالحة)**: - تحقّق من انحراف الساعة (يجب أن يكون ضمن ±30 ثانية) - تحقّق من أن Mapping (خريطة الخيارات) مرتّبة حسب المفتاح - تأكّد من أن Destination (هوية الوجهة في I2P) غير مستخدمة مسبقًا

**لا يوجد RequestVariableLeaseSet (مصطلح في I2P)**: - قد يكون Router يبني tunnels (انتظر حتى 5 دقائق) - تحقق من مشكلات اتصال الشبكة - تحقق من وجود عدد كافٍ من اتصالات الأقران

**إخفاقات تسليم الرسائل**: - تحقّق من رموز MessageStatus لمعرفة سبب الفشل المحدّد - تأكّد من أن LeaseSet البعيد منشور ومحدّث - تأكّد من توافق أنواع التشفير

**مشكلات الجلسات الفرعية**: - تحقّق من إنشاء الجلسة الأساسية أولاً - أكّد استخدام مفاتيح التشفير نفسها - تحقّق من اختلاف مفاتيح التوقيع

### رسائل التشخيص

**GetBandwidthLimits**: استعلم عن سعة router **HostLookup**: اختبر حلّ الأسماء وتوفّر LeaseSet (مجموعة بيانات المسارات في I2P) **MessageStatus**: تتبّع تسليم الرسائل من طرف إلى طرف

## المواصفات ذات الصلة

- **الهياكل الشائعة**: /docs/specs/common-structures/
- **I2NP (بروتوكول الشبكة)**: /docs/specs/i2np/
- **ECIES-X25519 (مخطط تشفير بيضوي ECIES باستخدام منحنى X25519)**: /docs/specs/ecies/
- **إنشاء tunnel**: /docs/specs/implementation/
- **مكتبة التدفق**: /docs/specs/streaming/
- **مكتبة الداتاغرام**: /docs/api/datagrams/
- **SAM v3**: /docs/api/samv3/

## المقترحات المشار إليها

- [المقترح 123](/proposals/123-new-netdb-entries/): LeaseSets مشفّرة والمصادقة
- [المقترح 144](/proposals/144-ecies-x25519-aead-ratchet/): ECIES-X25519-AEAD-Ratchet
- [المقترح 149](/proposals/149-b32-encrypted-ls2/): صيغة العنوان المحجّب (b33)
- [المقترح 152](/proposals/152-ecies-tunnels/): إنشاء tunnel باستخدام X25519
- [المقترح 154](/proposals/154-ecies-lookups/): استعلامات قاعدة البيانات من وجهات ECIES
- [المقترح 156](/proposals/156-ecies-routers/): ترحيل Router إلى ECIES-X25519
- [المقترح 161](/ar/proposals/161-ri-dest-padding/): ضغط حشو الوجهة
- [المقترح 167](/proposals/167-service-records/): سجلات خدمة LeaseSet
- [المقترح 169](/proposals/169-pq-crypto/): التشفير الهجين ما بعد الكمّي (ML-KEM)

## مرجع Javadocs (توثيق Java المُولّد تلقائيًا)

- [حزمة I2CP](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/package-summary.html)
- [MessageStatusMessage](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/MessageStatusMessage.html)
- [واجهة برمجة تطبيقات العميل](http://docs.i2p-projekt.de/javadoc/net/i2p/client/package-summary.html)

## ملخص العناصر المُهملة

### رسائل مهملة (لا تستخدم)

- **CreateLeaseSetMessage** (النوع 4): استخدم CreateLeaseSet2Message
- **RequestLeaseSetMessage** (النوع 21): استخدم RequestVariableLeaseSetMessage
- **ReceiveMessageBeginMessage** (النوع 6): استخدم وضع الاستلام السريع
- **ReceiveMessageEndMessage** (النوع 7): استخدم وضع الاستلام السريع
- **DestLookupMessage** (النوع 34): استخدم HostLookupMessage
- **DestReplyMessage** (النوع 35): استخدم HostReplyMessage
- **ReportAbuseMessage** (النوع 29): لم تُنفّذ مطلقًا

### خيارات مهملة

- تشفير ElGamal (النوع 0): الترحيل إلى ECIES-X25519 (النوع 4)
- تواقيع DSA: الترحيل إلى EdDSA أو ECDSA
- `i2cp.fastReceive=false`: استخدم دائمًا وضع الاستلام السريع
