---
title: "بروتوكول البث المباشر"
description: "بروتوكول نقل شبيه بـ TCP يستخدم من قبل معظم تطبيقات I2P"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## نظرة عامة

توفر **مكتبة I2P Streaming** نقلاً موثوقاً ومرتباً ومصادقاً عليه عبر طبقة الرسائل في I2P، مشابهة لـ **TCP over IP**. تقع فوق [بروتوكول I2CP](/docs/specs/i2cp/) وتُستخدم من قبل جميع تطبيقات I2P التفاعلية تقريباً، بما في ذلك بروكسيات HTTP وIRC وBitTorrent والبريد الإلكتروني.

### الخصائص الأساسية

- إعداد اتصال من مرحلة واحدة باستخدام علامات **SYN** و **ACK** و **FIN** التي يمكن دمجها مع بيانات الحمولة لتقليل عدد الرحلات ذهاباً وإياباً.
- **التحكم في الازدحام بنافذة منزلقة**، مع بداية بطيئة وتجنب للازدحام مُعدّل لبيئة I2P ذات الكمون العالي.
- ضغط الحزم (الافتراضي 4KB شرائح مضغوطة) يوازن بين تكلفة إعادة الإرسال وكمون التجزئة.
- قناة **مصادق عليها، مشفرة**، و**موثوقة** بالكامل بين وجهات I2P.

يتيح هذا التصميم إكمال طلبات واستجابات HTTP الصغيرة في رحلة ذهاب وإياب واحدة. قد تحمل حزمة SYN حمولة الطلب، بينما قد تحتوي حزمة SYN/ACK/FIN الخاصة بالمستجيب على نص الاستجابة الكامل.

---

## أساسيات واجهة برمجة التطبيقات (API)

واجهة برمجة التطبيقات للبث في Java تحاكي برمجة المقابس القياسية في Java:

```java
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(host, port, options);
I2PSocket socket       = mgr.connect(destination);
I2PServerSocket server = mgr.getServerSocket();
```
- `I2PSocketManagerFactory` يتفاوض أو يعيد استخدام جلسة router عبر I2CP.
- إذا لم يتم توفير مفتاح، يتم إنشاء وجهة جديدة تلقائياً.
- يمكن للمطورين تمرير خيارات I2CP (مثل أطوال tunnel، أنواع التشفير، أو إعدادات الاتصال) من خلال خريطة `options`.
- `I2PSocket` و `I2PServerSocket` يعكسان واجهات Java القياسية `Socket`، مما يجعل الترحيل سهلاً ومباشراً.

وثائق Javadocs الكاملة متاحة من وحدة تحكم موجه I2P أو [هنا](/docs/specs/streaming/).

---

## التكوين والضبط

يمكنك تمرير خصائص الإعدادات عند إنشاء مدير المقبس (socket manager) عبر:

```java
I2PSocketManagerFactory.createManager(host, port, properties);
```
### الخيارات الرئيسية

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum send window (bytes)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128 KB</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Timeout before connection close</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.enforceProtocol</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enforce protocol ID (prevents confusion)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.congestionAlgorithm</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion control method</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default (AIMD TCP-like)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.disableRejectLogging</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Disable logging rejected packets</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
    </tr>
  </tbody>
</table>
### السلوك حسب حمل العمل

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Workload</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Settings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>HTTP-like</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default parameters are ideal.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Bulk Transfer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Increase window size to 256 KB or 512 KB; lengthen timeouts.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Real-time Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length to 1-2 hops; adjust RTO downwards.</td>
    </tr>
  </tbody>
</table>
تشمل الميزات الأحدث منذ الإصدار 0.9.4 منع سجلات الرفض، ودعم قوائم DSA (0.9.21)، وفرض البروتوكول الإلزامي (0.9.36). تتضمن أجهزة الـ router منذ الإصدار 2.10.0 التشفير الهجين ما بعد الكمي (ML-KEM + X25519) على طبقة النقل.

---

## تفاصيل البروتوكول

يتم تعريف كل تدفق بواسطة **معرف التدفق** (Stream ID). تحمل الحزم أعلام تحكم مشابهة لـ TCP: `SYNCHRONIZE`، `ACK`، `FIN`، و `RESET`. يمكن أن تحتوي الحزم على كل من البيانات وأعلام التحكم في وقت واحد، مما يحسن الكفاءة للاتصالات قصيرة الأمد.

### دورة حياة الاتصال

1. **إرسال SYN** — يتضمن المُبادِر بيانات اختيارية.
2. **استجابة SYN/ACK** — يتضمن المُستجيب بيانات اختيارية.
3. **إنهاء ACK** — يُنشئ الموثوقية وحالة الجلسة.
4. **FIN/RESET** — يُستخدم للإغلاق المنظم أو الإنهاء المفاجئ.

### التجزئة وإعادة الترتيب

نظرًا لأن أنفاق I2P تُدخل تأخيرًا وإعادة ترتيب للرسائل، تقوم المكتبة بتخزين الحزم مؤقتًا من التدفقات غير المعروفة أو التي تصل مبكرًا. يتم تخزين الرسائل المخزنة مؤقتًا حتى تكتمل المزامنة، مما يضمن تسليمًا كاملاً ومرتبًا.

### تطبيق البروتوكول

الخيار `i2p.streaming.enforceProtocol=true` (افتراضي منذ الإصدار 0.9.36) يضمن أن الاتصالات تستخدم رقم بروتوكول I2CP الصحيح، مما يمنع التعارضات بين الأنظمة الفرعية المتعددة التي تشترك في وجهة واحدة.

---

## التوافقية وأفضل الممارسات

يتعايش بروتوكول البث مع **Datagram API**، مما يمنح المطورين الاختيار بين النقل الموجه بالاتصال والنقل غير الموجه بالاتصال.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reliable, ordered data (HTTP, IRC, FTP)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connectionless or lossy data (DNS, telemetry)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
    </tr>
  </tbody>
</table>
### العملاء المشتركون

يمكن للتطبيقات إعادة استخدام الأنفاق الموجودة عن طريق العمل كـ **عملاء مشتركين**، مما يسمح لخدمات متعددة بمشاركة نفس الوجهة. بينما يقلل هذا من العبء، إلا أنه يزيد من مخاطر الربط بين الخدمات—استخدمه بحذر.

### التحكم في الازدحام

- تتكيف طبقة البث المباشر بشكل مستمر مع زمن الاستجابة وسرعة النقل عبر الملاحظات المبنية على RTT.
- تعمل التطبيقات بشكل أفضل عندما تكون أجهزة router مساهمة كنظراء (مع تمكين المشاركة في tunnels).
- آليات التحكم في الازدحام الشبيهة بـ TCP تمنع إرهاق النظراء البطيئين وتساعد في موازنة استخدام النطاق الترددي عبر tunnels.

### اعتبارات زمن الاستجابة

نظرًا لأن I2P يضيف عدة مئات من الميلي ثانية من التأخير الأساسي، يجب على التطبيقات تقليل عدد الرحلات ذهابًا وإيابًا. قم بتجميع البيانات مع إعداد الاتصال حيثما أمكن (على سبيل المثال، طلبات HTTP في SYN). تجنب التصميمات التي تعتمد على العديد من التبادلات المتسلسلة الصغيرة.

---

## الاختبار والتوافق

- قم دائماً بالاختبار على كل من **Java I2P** و **i2pd** لضمان التوافق الكامل.
- على الرغم من توحيد البروتوكول، قد توجد اختلافات طفيفة في التنفيذ.
- تعامل مع routers الأقدم بمرونة—فالعديد من النظراء لا يزالون يستخدمون إصدارات ما قبل 2.0.
- راقب إحصائيات الاتصال باستخدام `I2PSocket.getOptions()` و `getSession()` لقراءة مقاييس RTT وإعادة الإرسال.

يعتمد الأداء بشكل كبير على إعداد tunnel:   - **أنفاق قصيرة (1-2 hops)** → زمن استجابة أقل، عدم إخفاء هوية مخفض.   - **أنفاق طويلة (3+ hops)** → عدم إخفاء هوية أعلى، زيادة في RTT.

---

## التحسينات الرئيسية (2.0.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent ACK Bundling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized round-trip reduction for HTTP workloads.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Adaptive Window Scaling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved large file transfer stability.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling and Socket Reuse</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced per-connection overhead.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Protocol Enforcement Default</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures correct stream usage.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hybrid ML-KEM Ratchet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adds post-quantum hybrid encryption layer.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd Streaming API Compatibility Fixes</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full parity with Java I2P library behavior.</td>
    </tr>
  </tbody>
</table>
---

## ملخص

**مكتبة I2P Streaming Library** هي العمود الفقري لجميع الاتصالات الموثوقة داخل I2P. فهي تضمن تسليم الرسائل بالترتيب الصحيح، مع المصادقة والتشفير، وتوفر بديلاً شبه جاهز لبروتوكول TCP في البيئات المجهولة.

لتحقيق الأداء الأمثل: - قلل من الرحلات ذهابًا وإيابًا من خلال تجميع SYN+payload.   - اضبط معاملات النافذة والمهلة الزمنية وفقًا لحمل العمل الخاص بك.   - فضل الأنفاق الأقصر للتطبيقات الحساسة لزمن الاستجابة.   - استخدم تصاميم متوافقة مع الازدحام لتجنب إرهاق الأقران.
