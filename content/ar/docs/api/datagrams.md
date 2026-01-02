---
title: "الرسائل البيانية (Datagrams)"
description: "تنسيقات الرسائل المصادق عليها والقابلة للرد والخام فوق I2CP"
slug: "datagrams"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## نظرة عامة

توفر الـ Datagrams اتصالاً موجهاً للرسائل فوق [I2CP](/docs/specs/i2cp/) وبالتوازي مع مكتبة البث. تتيح إرسال حزم **قابلة للرد**، أو **موثقة**، أو **خام** دون الحاجة إلى تدفقات موجهة بالاتصال. تقوم الـ routers بتغليف الـ datagrams في رسائل I2NP ورسائل tunnel، بغض النظر عما إذا كان NTCP2 أو SSU2 يحمل البيانات.

الدافع الأساسي هو السماح للتطبيقات (مثل المتتبعات، أو محللات DNS، أو الألعاب) بإرسال حزم مستقلة تحدد هوية المرسل.

> **جديد في 2025:** وافق مشروع I2P على **Datagram2 (البروتوكول 19)** و **Datagram3 (البروتوكول 20)**، مما يضيف حماية من إعادة التشغيل ورسائل قابلة للرد بتكلفة أقل لأول مرة منذ عقد من الزمن.

---

## 1. ثوابت البروتوكول

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed (repliable) datagram – “Datagram1”</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM_RAW</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsigned (raw) datagram – no sender info</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed + replay-protected datagram</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable (no signature, hash only)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
  </tbody>
</table>
تم إضفاء الطابع الرسمي على البروتوكولين 19 و20 في **الاقتراح 163 (أبريل 2025)**. وهما يتعايشان مع Datagram1 / RAW للتوافق مع الإصدارات السابقة.

---

## 2. أنواع الرزم البيانية

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Repliable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Authenticated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Replay Protection</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Min Overhead</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Raw</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal size; spoofable.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 427</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Full Destination + signature.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 457</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replay prevention + offline signatures; PQ-ready.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender hash only; low overhead.</td>
    </tr>
  </tbody>
</table>
### أنماط التصميم النموذجية

- **الطلب ← الاستجابة:** إرسال Datagram2 موقّع (طلب + nonce)، واستقبال رد خام أو Datagram3 (صدى nonce).
- **تردد عالي/حمل منخفض:** يُفضل Datagram3 أو RAW.
- **رسائل التحكم الموثّقة:** Datagram2.
- **التوافق مع الإصدارات القديمة:** Datagram1 لا يزال مدعومًا بالكامل.

---

## 3. تفاصيل Datagram2 و Datagram3 (2025)

### Datagram2 (البروتوكول 19)

بديل محسّن لـ Datagram1. الميزات: - **منع إعادة التشغيل:** رمز مضاد لإعادة التشغيل بحجم 4 بايتات. - **دعم التوقيع دون اتصال:** يتيح الاستخدام بواسطة Destinations الموقعة دون اتصال. - **تغطية توقيع موسعة:** تشمل hash الوجهة، الأعلام، الخيارات، كتلة التوقيع دون اتصال، الحمولة. - **جاهز لما بعد الكم:** متوافق مع ML-KEM hybrids المستقبلية. - **الحمل الإضافي:** ≈ 457 بايت (مفاتيح X25519).

### Datagram3 (البروتوكول 20)

يسد الفجوة بين الأنواع الخام والموقعة. المميزات: - **قابل للرد بدون توقيع:** يحتوي على hash بطول 32 بايت للمرسل + علامات بطول 2 بايت. - **حمل إضافي ضئيل:** ≈ 34 بايت. - **لا يوجد دفاع ضد إعادة الإرسال** — يجب على التطبيق تنفيذه.

كلا البروتوكولين من ميزات API 0.9.66 ومُنفذان في router الخاص بـ Java منذ الإصدار 2.9.0؛ لا توجد تطبيقات لـ i2pd أو Go حتى الآن (أكتوبر 2025).

---

## 4. حدود الحجم والتجزئة

- **حجم رسالة Tunnel:** 1 028 بايت (4 بايت Tunnel ID + 16 بايت IV + 1 008 بايت حمولة).  
- **الجزء الأول:** 956 بايت (تسليم TUNNEL النموذجي).  
- **الجزء التالي:** 996 بايت.  
- **الحد الأقصى للأجزاء:** 63–64.  
- **الحد العملي:** ≈ 62 708 بايت (~61 كيلوبايت).  
- **الحد الموصى به:** ≤ 10 كيلوبايت للتسليم الموثوق (تزداد حالات الإسقاط بشكل أُسّي بعد هذا الحد).

**ملخص الحمل الإضافي:** - Datagram1 ≈ 427 بايت (الحد الأدنى).   - Datagram2 ≈ 457 بايت.   - Datagram3 ≈ 34 بايت.   - الطبقات الإضافية (I2CP gzip header، I2NP، Garlic، Tunnel): + ~5.5 كيلوبايت في أسوأ الحالات.

---

## 5. تكامل I2CP / I2NP

مسار الرسالة: 1. ينشئ التطبيق datagram (عبر I2P API أو SAM).   2. يغلف I2CP بترويسة gzip (`0x1F 0x8B 0x08`، RFC 1952) ومجموع تدقيق CRC-32.   3. تُخزن أرقام البروتوكول + المنفذ في حقول ترويسة gzip.   4. يغلف الموجه Router كرسالة I2NP ← Garlic clove ← أجزاء tunnel بحجم 1 كيلوبايت.   5. تمر الأجزاء عبر tunnel صادر ← الشبكة ← tunnel وارد.   6. يُسلَّم datagram المُعاد تجميعه إلى معالج التطبيق بناءً على رقم البروتوكول.

**التكامل:** CRC-32 (من I2CP) + توقيع تشفيري اختياري (Datagram1/2). لا يوجد حقل تدقيق منفصل داخل الـ datagram نفسه.

---

## 6. واجهات البرمجة

### واجهة برمجة التطبيقات Java

الحزمة `net.i2p.client.datagram` تتضمن: - `I2PDatagramMaker` – ينشئ datagrams موقعة.   - `I2PDatagramDissector` – يتحقق ويستخرج معلومات المرسل.   - `I2PInvalidDatagramException` – يُطرح عند فشل التحقق.

`I2PSessionMuxedImpl` (`net.i2p.client.impl.I2PSessionMuxedImpl`) يدير تعدد إرسال البروتوكول والمنافذ للتطبيقات التي تشترك في Destination واحد.

**الوصول إلى Javadoc:** - [idk.i2p Javadoc](http://idk.i2p/javadoc-i2p/) (شبكة I2P فقط) - [Javadoc Mirror](https://eyedeekay.github.io/javadoc-i2p/) (نسخة على الإنترنت العادي) - [Official Javadocs](http://docs.i2p-projekt.de/javadoc/) (الوثائق الرسمية)

### دعم SAMv3

- SAM 3.2 (2016): إضافة معاملات PORT و PROTOCOL.  
- SAM 3.3 (2016): تقديم نموذج PRIMARY/subsession؛ يسمح بالتدفقات + البيانات المجمعة على وجهة واحدة.  
- تمت إضافة دعم أنماط جلسات Datagram2 / 3 في المواصفات 2025 (التنفيذ قيد الانتظار).  
- المواصفات الرسمية: [مواصفات SAM v3](/docs/api/samv3/)

### وحدات i2ptunnel

- **udpTunnel:** قاعدة وظيفية بالكامل لتطبيقات I2P UDP (`net.i2p.i2ptunnel.udpTunnel`).  
- **streamr:** عملي لبث الصوت/الفيديو (`net.i2p.i2ptunnel.streamr`).  
- **SOCKS UDP:** **غير وظيفي** اعتبارًا من الإصدار 2.10.0 (نموذج UDP فقط).

> لأغراض UDP العامة، استخدم Datagram API أو udpTunnel مباشرة—لا تعتمد على SOCKS UDP.

---

## 7. النظام البيئي ودعم اللغات (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library / Package</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td><td style="border:1px solid var(--color-border); padding:0.5rem;">core API (net.i2p.client.datagram)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ full support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2pd / libsam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2 partial</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Limited</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem;">go-i2p / sam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1–3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib, i2p.socket, txi2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs, i2p_client</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">JS/TS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p, i2p-sam</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td><td style="border:1px solid var(--color-border); padding:0.5rem;">network-anonymous-i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td><td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
  </tbody>
</table>
Java I2P هو الموجه الوحيد الذي يدعم subsessions كاملة لـ SAM 3.3 وواجهة برمجة التطبيقات Datagram2 في الوقت الحالي.

---

## 8. مثال على الاستخدام – متتبع UDP (I2PSnark 2.10.0)

أول تطبيق حقيقي لـ Datagram2/3:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Datagram Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Announce Request</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable but low-overhead update</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Response</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Raw Datagram</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal payload return</td></tr>
  </tbody>
</table>
يوضح النمط الاستخدام المختلط لحزم البيانات المصادق عليها والخفيفة لتحقيق التوازن بين الأمان والأداء.

---

## 9. الأمان وأفضل الممارسات

- استخدم Datagram2 لأي تبادل مصادق عليه أو عندما تكون هجمات إعادة التشغيل مهمة.
- فضّل Datagram3 للاستجابات السريعة القابلة للرد مع ثقة معتدلة.
- استخدم RAW للبث العام أو البيانات المجهولة.
- احتفظ بالحمولات ≤ 10 كيلوبايت لضمان التسليم الموثوق.
- كن على علم بأن SOCKS UDP يبقى غير وظيفي.
- تحقق دائماً من CRC لـ gzip والتوقيعات الرقمية عند الاستلام.

---

## 10. المواصفات الفنية

يغطي هذا القسم تنسيقات الحزم (datagram) منخفضة المستوى، والتغليف، وتفاصيل البروتوكول.

### 10.1 تحديد البروتوكول

تنسيقات البيانات المجزأة (Datagram) **لا** تشترك في رأس (header) مشترك. لا يمكن لأجهزة التوجيه (routers) استنتاج النوع من بايتات الحمولة (payload) وحدها.

عند دمج أنواع متعددة من الـ datagram—أو عند الجمع بين الـ datagrams مع البث المستمر—قم بتعيين بشكل صريح: - **رقم البروتوكول** (عبر I2CP أو SAM) - اختيارياً **رقم المنفذ**، إذا كان تطبيقك يتعدد الخدمات

ترك البروتوكول غير محدد (`0` أو `PROTO_ANY`) غير مُستحسن وقد يؤدي إلى أخطاء في التوجيه أو التسليم.

### 10.2 الحزم الخام (Raw Datagrams)

الرسائل البيانية غير القابلة للرد لا تحمل بيانات المرسل أو المصادقة. إنها حمولات معتمة، تُعالج خارج واجهة برمجة التطبيقات للرسائل البيانية عالية المستوى ولكنها مدعومة عبر SAM و I2PTunnel.

**البروتوكول:** `18` (`PROTO_DATAGRAM_RAW`)

**التنسيق:**

```
+----+----+----+----+----//
|     payload...
+----+----+----+----+----//
```
طول البيانات محدود بقيود النقل (≈32 كيلوبايت كحد أقصى عملي، وغالباً أقل بكثير).

### 10.3 Datagram1 (مخططات بيانات قابلة للرد)

يضمّن **Destination** المرسل و**Signature** (التوقيع) للمصادقة وعنوان الرد.

**البروتوكول:** `17` (`PROTO_DATAGRAM`)

**الحمل الإضافي:** ≥427 بايت **الحمولة:** حتى ~31.5 كيلوبايت (محدودة بواسطة النقل)

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
|               from                    |
+                                       +
|                                       |
~             Destination bytes         ~
|                                       |
+----+----+----+----+----+----+----+----+
|             signature                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     payload...
+----+----+----+----//
```
- `from`: وجهة Destination (387+ بايت)
- `signature`: توقيع Signature يطابق نوع المفتاح
  - بالنسبة لـ DSA_SHA1: توقيع لقيمة التجزئة SHA-256 للحمولة
  - بالنسبة لأنواع المفاتيح الأخرى: توقيع مباشر على الحمولة

**ملاحظات:** - تم توحيد التوقيعات لأنواع non-DSA في I2P 0.9.14. - التوقيعات غير المتصلة LS2 (الاقتراح 123) غير مدعومة حالياً في Datagram1.

### 10.4 تنسيق Datagram2

رسالة بيانات قابلة للرد محسّنة تضيف **مقاومة إعادة التشغيل** كما هو محدد في [الاقتراح 163](/proposals/163-datagram2/).

**البروتوكول:** `19` (`PROTO_DATAGRAM2`)

التنفيذ جارٍ حالياً. يجب أن تتضمن التطبيقات فحوصات nonce أو الطابع الزمني للتكرار.

### 10.5 تنسيق Datagram3

يوفر رسائل بيانات **قابلة للرد لكن غير مصادق عليها**. يعتمد على مصادقة الجلسة التي يحتفظ بها الموجه (router) بدلاً من الوجهة والتوقيع المضمنين.

**البروتوكول:** `20` (`PROTO_DATAGRAM3`) **الحالة:** قيد التطوير منذ 0.9.66

مفيد عندما: - تكون الوجهات كبيرة (مثل مفاتيح ما بعد الكم) - تحدث المصادقة في طبقة أخرى - تكون كفاءة النطاق الترددي حرجة

### 10.6 سلامة البيانات

يتم حماية سلامة البيانات (Datagram) من خلال **مجموع التحقق gzip CRC-32** في طبقة I2CP. لا يوجد حقل مجموع تحقق صريح ضمن تنسيق حمولة البيانات (datagram payload) نفسها.

### 10.7 تغليف الحزم

يتم تغليف كل datagram كرسالة I2NP واحدة أو كـ clove فردي في **Garlic Message**. تتولى طبقات I2CP وI2NP والـ tunnel معالجة الطول والتأطير — لا يوجد فاصل داخلي أو حقل طول في بروتوكول الـ datagram.

### 10.8 اعتبارات ما بعد الكم (PQ)

إذا تم تطبيق **Proposal 169** (توقيعات ML-DSA)، فسترتفع أحجام التوقيعات والوجهات بشكل كبير — من ~455 بايت إلى **≥3739 بايت**. سيؤدي هذا التغيير إلى زيادة كبيرة في الحمل الإضافي للبيانات وتقليل سعة الحمولة الفعلية.

**Datagram3**، الذي يعتمد على المصادقة على مستوى الجلسة (وليس التوقيعات المضمنة)، من المرجح أن يصبح التصميم المفضل في بيئات I2P ما بعد الكم.

---

## 11. المراجع

- [اقتراح 163 – Datagram2 و Datagram3](/proposals/163-datagram2/)
- [اقتراح 160 – تكامل UDP Tracker](/proposals/160-udp-trackers/)
- [اقتراح 144 – حسابات MTU للبث المباشر](/proposals/144-ecies-x25519-aead-ratchet/)
- [اقتراح 169 – التوقيعات ما بعد الكم](/proposals/169-pq-crypto/)
- [مواصفات I2CP](/docs/specs/i2cp/)
- [مواصفات I2NP](/docs/specs/i2np/)
- [مواصفات رسائل Tunnel](/docs/specs/implementation/)
- [مواصفات SAM v3](/docs/api/samv3/)
- [توثيق i2ptunnel](/docs/api/i2ptunnel/)

## 12. أبرز تغييرات السجل (2019 – 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Change</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2019</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram API stabilization</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2021</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Protocol port handling reworked</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2022</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.0.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 adoption completed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.6.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy transport removal simplified UDP code</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.9.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2/3 support added (Java API)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.10.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP Tracker implementation released</td></tr>
  </tbody>
</table>
---

## 13. الملخص

يدعم نظام الـ datagram الفرعي الآن أربعة متغيرات من البروتوكول توفر نطاقاً من المصادقة الكاملة إلى النقل الخام خفيف الوزن. يجب على المطورين الانتقال إلى **Datagram2** للحالات الحساسة أمنياً وإلى **Datagram3** لحركة البيانات القابلة للرد بكفاءة. تظل جميع الأنواع القديمة متوافقة لضمان إمكانية التشغيل البيني طويل الأمد.
