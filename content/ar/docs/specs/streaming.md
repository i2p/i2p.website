---
title: "بروتوكول التدفق"
description: "آلية نقل موثوقة شبيهة بـ TCP تستخدمها معظم تطبيقات I2P"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## نظرة عامة

توفر I2P Streaming Library إيصال بيانات موثوقًا، وفق الترتيب، ومصادقًا عليه فوق طبقة الرسائل غير الموثوقة الخاصة بـ I2P — على غرار TCP فوق IP. تُستخدم من قبل تكاد جميع تطبيقات I2P التفاعلية مثل تصفح الويب، وIRC، والبريد الإلكتروني، ومشاركة الملفات.

إنه يضمن النقل الموثوق، والتحكم في الازدحام، وإعادة الإرسال، والتحكم في التدفق عبر tunnels المجهولة عالية الكمون الخاصة بـ I2P. يُشفَّر كل تدفق بالكامل من طرف إلى طرف بين الوجهات.

---

## مبادئ التصميم الأساسية

تنفّذ مكتبة البثّ **تهيئة اتصال أحادية المرحلة**، حيث يمكن لأعلام SYN وACK وFIN حمل حمولة بيانات في الرسالة نفسها. وهذا يقلّل عدد رحلات الذهاب والإياب في البيئات عالية الكمون — إذ يمكن لعملية HTTP صغيرة أن تكتمل في رحلة ذهاب وإياب واحدة.

يُستوحى التحكم في الازدحام وإعادة الإرسال من TCP ولكنه مُكيَّف لبيئة I2P. أحجام النوافذ مستندة إلى الرسائل، وليست مستندة إلى البايتات، وهي مُضبوطة وفق زمن تأخير الـ tunnel والعبء الإضافي. يدعم البروتوكول البدء البطيء، وتجنّب الازدحام، والتراجع الأُسّي بطريقة مشابهة لخوارزمية AIMD في TCP (الزيادة الإضافية/النقصان الضربي).

---

## المعمارية

تعمل مكتبة التدفق بين التطبيقات وواجهة I2CP.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Application</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard I2PSocket and I2PServerSocket usage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection setup, sequencing, retransmission, and flow control</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel creation, routing, and message handling</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2NP / Router Layer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport through tunnels</td>
    </tr>
  </tbody>
</table>
يصل معظم المستخدمين إليه عبر I2PSocketManager أو I2PTunnel أو SAMv3. تتعامل المكتبة بشفافية مع إدارة الوجهات، واستخدام tunnel، وعمليات إعادة الإرسال.

---

## تنسيق الحزمة

```
+-----------------------------------------------+
| Send Stream ID (4B) | Receive Stream ID (4B) |
+-----------------------------------------------+
| Sequence Number (4B) | Ack Through (4B)      |
+-----------------------------------------------+
| NACK Count (1B) | optional NACK list (4B each)
+-----------------------------------------------+
| Flags (1B) | Option Size (1B) | Options ...   |
+-----------------------------------------------+
| Payload ...                                  |
```
### تفاصيل الترويسة

- **معرّفات التدفق**: قيم بطول 32 بت تُعرّف بشكل فريد التدفقات المحلية والبعيدة.
- **رقم التسلسل**: يبدأ من 0 مع SYN (علم بدء الاتصال)، ويزداد مع كل رسالة.
- **Ack Through**: يُقِرّ بجميع الرسائل حتى N، باستثناء تلك الموجودة في قائمة NACK (عدم الإقرار).
- **Flags**: قناع بتّي يتحكم في الحالة والسلوك.
- **Options**: قائمة بطول متغيّر لـ RTT (زمن الرحلة ذهاباً وإياباً)، وMTU (أقصى حجم لوحدة النقل)، والتفاوض على البروتوكول.

### أعلام المفتاح

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SYN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection initiation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Acknowledge received packets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FIN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Graceful close</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RST</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reset connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sender’s destination included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SIGNATURE_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Message signed by sender</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECHO / ECHO_REPLY</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong keepalive</td>
    </tr>
  </tbody>
</table>
---

## التحكم في التدفق والموثوقية

تستخدم Streaming (طبقة تدفق الاتصالات في I2P) **آلية نافذة معتمدة على الرسائل**، بخلاف نهج TCP (بروتوكول التحكم بالنقل) المعتمد على البايتات. يساوي عدد الحزم غير المؤكدة المسموح بكونها قيد العبور حجم النافذة الحالي (القيمة الافتراضية 128).

### الآليات

- **التحكم في الازدحام:** البداية البطيئة وتجنّب قائم على AIMD (الزيادة الجمعيّة/النقصان الضربي).  
- **الخنق/فكّ الخنق:** إشارات التحكم في التدفق استنادًا إلى إشغال المخزن المؤقت.  
- **إعادة الإرسال:** حساب RTO وفق RFC 6298 مع تراجع أسّي.  
- **ترشيح التكرارات:** يضمن الموثوقية رغم احتمال إعادة ترتيب الرسائل.

قيم الإعداد النموذجية:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max unacknowledged messages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxMessageSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1730</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum payload bytes per message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Idle connection timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connectTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">300000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection establishment timeout</td>
    </tr>
  </tbody>
</table>
---

## إنشاء الاتصال

1. **المُبادر** يرسل SYN (اختياريًا مع حمولة و FROM_INCLUDED).  
2. **المستجيب** يرد بـ SYN+ACK (قد يتضمن حمولة).  
3. **المُبادر** يرسل ACK النهائي مؤكدًا إتمام التأسيس.

تتيح الحمولات الأولية الاختيارية نقل البيانات قبل اكتمال المصافحة بالكامل.

---

## تفاصيل التنفيذ

### إعادة الإرسال والمهلة

تتبع خوارزمية إعادة الإرسال **RFC 6298**.   - **RTO (مهلة إعادة الإرسال) الأولي:** 9s   - **الحد الأدنى لـ RTO:** 100ms   - **الحد الأقصى لـ RTO:** 45s   - **ألفا:** 0.125   - **بيتا:** 0.25

### مشاركة كتلة التحكم

تعيد الاتصالات الأخيرة إلى القرين نفسه استخدام بيانات RTT (زمن الذهاب والإياب) وبيانات النافذة السابقة للتدرّج بشكل أسرع، ما يتفادى كمون “cold start” (بدء بارد). تنتهي صلاحية كتل التحكم بعد عدة دقائق.

### MTU (الحد الأقصى لحجم وحدة الإرسال) والتجزئة

- MTU الافتراضي: **1730 بايت** (يتسع لرسالتين من I2NP).  
- وجهات ECIES (نظام تشفير قائم على المنحنيات الإهليلجية): **1812 بايت** (حمولة إضافية أقل).  
- الحد الأدنى للـ MTU المدعوم: 512 بايت.

حجم الحمولة لا يشمل ترويسة البث الدنيا البالغة 22 بايت.

---

## سجل الإصدارات

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol numbers defined in I2CP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable-length signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED not required in RESET</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol enforcement enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">OFFLINE_SIGNATURE support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bob’s hash added to NACK field in SYN</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-Quantum hybrid encryption (experimental)</td>
    </tr>
  </tbody>
</table>
---

## الاستخدام على مستوى التطبيق

### مثال بلغة جافا

```java
Properties props = new Properties();
props.setProperty("i2p.streaming.maxWindowSize", "512");
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(props);

I2PSocket socket = mgr.connect(destination);
InputStream in = socket.getInputStream();
OutputStream out = socket.getOutputStream();
```
### دعم SAMv3 و i2pd

- **SAMv3**: يوفّر وضعي STREAM و DATAGRAM للعملاء غير المكتوبين بـ Java.  
- **i2pd**: يوفّر معلمات بث متطابقة عبر خيارات ملف الإعدادات (مثل `i2p.streaming.maxWindowSize`، `profile`، إلخ).

---

## الاختيار بين Streaming (التدفق شبيه TCP) و Datagrams (رسائل عديمة الاتصال)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP, IRC, Email</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires reliability</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Repliable Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single request/response</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Telemetry, Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Raw Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Best-effort acceptable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P2P DHT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">High connection churn</td>
    </tr>
  </tbody>
</table>
---

## الأمن والمستقبل ما بعد الكم

جلسات التدفق مشفرة من طرف إلى طرف على طبقة I2CP.   التشفير الهجين لما بعد الكم (ML-KEM + X25519) مدعوم تجريبياً في 2.10.0 لكنه معطّل افتراضياً.

---

## المراجع

- [نظرة عامة على واجهة برمجة تطبيقات البث](/docs/specs/streaming/)  
- [مواصفة بروتوكول البث](/docs/specs/streaming/)  
- [مواصفة I2CP](/docs/specs/i2cp/)  
- [الاقتراح 144: حسابات MTU (أقصى وحدة نقل) للبث](/proposals/144-ecies-x25519-aead-ratchet/)  
- [ملاحظات إصدار I2P 2.10.0](/ar/blog/2025/09/08/i2p-2.10.0-release/)
