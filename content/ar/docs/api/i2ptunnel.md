---
title: "I2PTunnel"
description: "أداة للتفاعل مع I2P وتوفير الخدمات عليها"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## نظرة عامة

I2PTunnel هو مكون أساسي في I2P للتفاعل مع شبكة I2P وتوفير الخدمات عليها. يمكّن تطبيقات البث الإعلامي والتطبيقات القائمة على TCP من العمل بشكل مجهول من خلال تجريد الأنفاق (tunnel abstraction). يمكن تحديد وجهة النفق عن طريق [اسم المضيف](/docs/overview/naming)، أو [Base32](/docs/overview/naming#base32)، أو مفتاح الوجهة الكامل.

كل tunnel مُنشأ يستمع محلياً (مثل `localhost:port`) ويتصل داخلياً بوجهات I2P. لاستضافة خدمة، أنشئ tunnel يشير إلى عنوان IP والمنفذ المطلوبين. يتم توليد مفتاح وجهة I2P مقابل، مما يسمح للخدمة بأن تصبح قابلة للوصول عالمياً ضمن شبكة I2P. واجهة الويب الخاصة بـ I2PTunnel متاحة على [I2P Router Tunnel Manager](http://localhost:7657/i2ptunnel/).

---

## الخدمات الافتراضية

### نفق الخادم

- **I2P Webserver** – tunnel إلى خادم ويب Jetty على [localhost:7658](http://localhost:7658) لاستضافة سهلة على I2P.  
  - **Unix:** `$HOME/.i2p/eepsite/docroot`  
  - **Windows:** `%LOCALAPPDATA%\I2P\I2P Site\docroot` → `C:\Users\<username>\AppData\Local\I2P\I2P Site\docroot`

### أنفاق العميل

- **I2P HTTP Proxy** – `localhost:4444` – يُستخدم لتصفح I2P والإنترنت من خلال الوكلاء الخارجيين (outproxies).  
- **I2P HTTPS Proxy** – `localhost:4445` – النسخة الآمنة من وكيل HTTP.  
- **Irc2P** – `localhost:6668` – نفق شبكة IRC المجهول الافتراضي.  
- **Git SSH (gitssh.idk.i2p)** – `localhost:7670` – نفق العميل للوصول إلى المستودعات عبر SSH.  
- **Postman SMTP** – `localhost:7659` – نفق العميل للبريد الصادر.  
- **Postman POP3** – `localhost:7660` – نفق العميل للبريد الوارد.

> ملاحظة: فقط خادم الويب I2P هو **نفق خادم** افتراضي؛ جميع الأنفاق الأخرى هي أنفاق عميل تتصل بخدمات I2P خارجية.

---

## الإعدادات

يتم توثيق مواصفات إعداد I2PTunnel في [/spec/configuration](/docs/specs/configuration/).

---

## أوضاع العميل

### قياسي

يفتح منفذ TCP محلي يتصل بخدمة على وجهة I2P. يدعم إدخالات وجهات متعددة مفصولة بفواصل لتحقيق التكرار والموثوقية.

### HTTP

نفق بروكسي لطلبات HTTP/HTTPS. يدعم الـ outproxies المحلية والبعيدة، إزالة الرؤوس، التخزين المؤقت، المصادقة، والضغط الشفاف.

**حماية الخصوصية:**   - يزيل الترويسات: `Accept-*`, `Referer`, `Via`, `From`   - يستبدل ترويسات المضيف بوجهات Base32   - يفرض إزالة hop-by-hop المتوافقة مع RFC   - يضيف دعمًا لفك الضغط الشفاف   - يوفر صفحات أخطاء داخلية واستجابات محلية

**سلوك الضغط:**   - يمكن للطلبات استخدام رأس مخصص `X-Accept-Encoding: x-i2p-gzip`   - الاستجابات مع `Content-Encoding: x-i2p-gzip` يتم فك ضغطها تلقائياً   - يتم تقييم الضغط حسب نوع MIME وطول الاستجابة لتحقيق الكفاءة

**الاستمرارية (جديد منذ الإصدار 2.5.0):**   يتم الآن دعم HTTP Keepalive والاتصالات المستمرة للخدمات المستضافة على I2P من خلال مدير الخدمات المخفية. هذا يقلل من زمن الاستجابة والحمل الزائد للاتصال ولكنه لا يتيح بعد المقابس (sockets) المستمرة المتوافقة تمامًا مع RFC 2616 عبر جميع القفزات.

**Pipelining:**   يبقى غير مدعوم وغير ضروري؛ المتصفحات الحديثة قامت بإيقافه.

**سلوك User-Agent:**   - **Outproxy:** يستخدم User-Agent حالي من Firefox ESR.   - **داخلي:** `MYOB/6.66 (AN/ON)` للحفاظ على اتساق عدم الكشف عن الهوية.

### عميل IRC

يتصل بخوادم IRC المبنية على I2P. يسمح بمجموعة فرعية آمنة من الأوامر مع تصفية المعرفات للحفاظ على الخصوصية.

### SOCKS 4/4a/5

يوفر إمكانية بروكسي SOCKS لاتصالات TCP. يبقى UDP غير مُطبَّق في Java I2P (فقط في i2pd).

### اتصال

ينفذ نفق HTTP `CONNECT` لاتصالات SSL/TLS.

### Streamr

يُمكّن البث بنمط UDP عبر التغليف القائم على TCP. يدعم بث الوسائط عند إقرانه مع نفق خادم Streamr المقابل.

![مخطط I2PTunnel Streamr](/images/I2PTunnel-streamr.png)

---

## أوضاع الخادم

### خادم قياسي

ينشئ وجهة TCP مرتبطة بعنوان IP محلي:منفذ.

### خادم HTTP

ينشئ وجهة تتفاعل مع خادم ويب محلي. يدعم الضغط (`x-i2p-gzip`)، وإزالة الرؤوس، والحماية من هجمات DDoS. يستفيد الآن من **دعم الاتصال المستمر** (v2.5.0+) و**تحسين تجميع الخيوط** (v2.7.0–2.9.0).

### HTTP ثنائي الاتجاه

**مُهمَل** – لا يزال يعمل ولكن لا يُنصح باستخدامه. يعمل كخادم وعميل HTTP في نفس الوقت دون استخدام outproxying. يُستخدم بشكل أساسي لاختبارات الحلقة المرجعية التشخيصية.

### خادم IRC

ينشئ وجهة مُصفاة لخدمات IRC، حيث يمرر مفاتيح وجهة العميل كأسماء مضيفين.

### خادم Streamr

يتزاوج مع نفق عميل Streamr للتعامل مع تدفقات البيانات بنمط UDP عبر I2P.

---

## الميزات الجديدة (2.4.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Keepalive/Persistent Connections</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP tunnels now support persistent sockets for I2P-hosted services, improving performance.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling Optimization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0-2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced CPU overhead and latency by improving thread management.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-Quantum Encryption (ML-KEM)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional hybrid X25519+ML-KEM encryption to resist future quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Segmentation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Isolates I2PTunnel contexts for improved security and privacy.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Removal / SSU2 Adoption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0-2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Upgraded transport layer; transparent to users.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor Blocking</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents inefficient and unstable I2P-over-Tor routing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Browser Proxy (Proposal 166)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced identity-aware proxy mode; details pending confirmation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 Requirement (upcoming)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.11.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Future release will require Java 17+.</td>
    </tr>
  </tbody>
</table>
---

## ميزات الأمان

- **إزالة الترويسات** للحفاظ على عدم الكشف عن الهوية (Accept, Referer, From, Via)
- **عشوائية User-Agent** حسب in/outproxy
- **تقييد معدل POST** و **الحماية من Slowloris**
- **تقييد الاتصالات** في أنظمة البث الفرعية
- **معالجة ازدحام الشبكة** على مستوى tunnel
- **عزل NetDB** لمنع التسريبات بين التطبيقات

---

## التفاصيل التقنية

- حجم مفتاح الوجهة الافتراضي: 516 بايت (قد يتجاوز ذلك لشهادات LS2 الموسعة)
- عناوين Base32: `{52–56+ chars}.b32.i2p`
- أنفاق الخادم تظل متوافقة مع كل من Java I2P و i2pd
- ميزة متوقفة: `httpbidirserver` فقط؛ لا توجد إزالات منذ 0.9.59
- تم التحقق من صحة المنافذ الافتراضية وجذور المستندات لجميع المنصات

---

## ملخص

يظل I2PTunnel العمود الفقري لدمج التطبيقات مع I2P. بين الإصدارين 0.9.59 و2.10.0، اكتسب دعم الاتصالات المستمرة، والتشفير المقاوم للحوسبة الكمومية، وتحسينات كبيرة في معالجة الخيوط. معظم الإعدادات تبقى متوافقة، لكن يجب على المطورين التحقق من إعداداتهم لضمان الامتثال للإعدادات الافتراضية الحديثة للنقل والأمان.
