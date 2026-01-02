---
title: "إرشادات كتابة وثائق I2P"
description: "الحفاظ على الاتساق والدقة وإمكانية الوصول في جميع الوثائق التقنية الخاصة بـ I2P"
slug: "writing-guidelines"
lastUpdated: "2025-10"
---

**الهدف:** الحفاظ على الاتساق والدقة وقابلية الوصول عبر وثائق I2P التقنية

---

## المبادئ الأساسية

### 1. تحقق من كل شيء

**لا تفترض أو تخمّن أبدًا.** يجب التحقق من جميع التصريحات التقنية مقابل: - الشيفرة المصدرية الحالية لـ I2P (https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master) - التوثيق الرسمي لـ API (https://i2p.github.io/i2p.i2p/  - مواصفات التهيئة [/docs/specs/](/docs/) - ملاحظات الإصدارات الأخيرة [/releases/](/categories/release/)

**مثال على التحقق السليم:**

```markdown
❌ BAD: "The ClientApp interface probably requires three constructor parameters."
✅ GOOD: "The ClientApp interface requires this constructor signature: 
         public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)"
```
### 2. الأولوية للوضوح على الإيجاز

اكتب للمطورين الذين قد يتعرّفون على I2P (مشروع الإنترنت غير المرئي) للمرة الأولى. اشرح المفاهيم بصورة وافية بدلاً من افتراض وجود معرفة مسبقة.

**مثال:**

```markdown
❌ BAD: "Use the port mapper for service discovery."
✅ GOOD: "The port mapper offers a simple directory for internal TCP services. 
         Register loopback ports so other applications can discover your service 
         without hardcoded addresses."
```
### 3. إمكانية الوصول أولاً

يجب أن تكون الوثائق متاحة للمطورين على clearnet (الإنترنت العام) رغم أن I2P عبارة عن شبكة تراكبية. وفّر دائمًا بدائل قابلة للوصول عبر clearnet لموارد I2P الداخلية.

---

## الدقة التقنية

### توثيق واجهات برمجة التطبيقات والواجهات

**قم دائمًا بتضمين:** 1. أسماء الحزم كاملة عند أول ذكر: `net.i2p.app.ClientApp` 2. تواقيع الأساليب كاملة مع أنواع الإرجاع 3. أسماء المعاملات وأنواعها 4. المعاملات المطلوبة مقابل الاختيارية

**مثال:**

```markdown
The `startup()` method has signature `void startup() throws IOException` and must 
execute without blocking. The method must call `ClientAppManager.notify()` at least 
once to transition from INITIALIZED state.
```
### خصائص الإعداد

عند توثيق ملفات التهيئة: 1. اعرض أسماء الخصائص بدقة 2. حدّد ترميز الملف (UTF-8 لملفات تهيئة I2P) 3. قدّم أمثلة كاملة 4. وثّق القيم الافتراضية 5. اذكر الإصدار الذي أُدخلت/تغيّرت فيه الخصائص

**مثال:**

```markdown
### clients.config Properties

**Required:**
- `clientApp.N.main` - Full class name (no default)

**Optional:**
- `clientApp.N.delay` - Seconds before starting (default: 120)
- `clientApp.N.onBoot` - Forces delay=0 if true (default: false, added in 0.9.4)
```
### الثوابت والتعدادات

عند توثيق الثوابت، استخدم أسماء الشيفرة الفعلية:

```markdown
❌ BAD: "Common registrations include console, i2ptunnel, Jetty, sam, and bob"

✅ GOOD: "Common port mapper service constants from `net.i2p.util.PortMapper`:
- `SVC_CONSOLE` - Router console (default port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (default port 4444)
- `SVC_SAM` - SAM bridge (default port 7656)"
```
### التمييز بين المفاهيم المتشابهة

يحتوي I2P على عدة أنظمة متداخلة. احرص دائماً على توضيح أي نظام تقوم بتوثيقه:

**مثال:**

```markdown
Note that client registry and port mapper are separate systems:
- **ClientAppManager registry** enables inter-application communication by name lookup
- **PortMapper** maps service names to host:port combinations for service discovery
- **i2ptunnel tunnel types** are configuration values (tunnel.N.type), not service registrations
```
---

## روابط التوثيق والمراجع

### قواعد إمكانية الوصول لعناوين URL

1. **المراجع الأساسية** ينبغي أن تستخدم عناوين URL قابلة للوصول عبر clearnet (الإنترنت العام خارج I2P)
2. **عناوين I2P الداخلية** (نطاقات .i2p) يجب أن تتضمّن ملاحظات حول إمكانية الوصول
3. **احرص دائماً على توفير بدائل** عند وضع روابط إلى موارد I2P الداخلية

**قالب لعناوين URL الداخلية الخاصة بـ I2P:**

```markdown
> **Note:** The I2P network hosts comprehensive documentation at http://idk.i2p/javadoc-i2p/ 
> which requires an I2P router for access. For clearnet access, use the GitHub Pages 
> mirror at https://eyedeekay.github.io/javadoc-i2p/
```
### عناوين URL مرجعية موصى بها لـ I2P

**المواصفات الرسمية:** - [التهيئة](/docs/specs/configuration/) - [الإضافة](/docs/specs/plugin/) - [فهرس الوثائق](/docs/)

**توثيق واجهة برمجة التطبيقات (API) (اختر الأحدث):** - الأحدث: https://i2p.github.io/i2p.i2p/ (API 0.9.66 اعتباراً من I2P 2.10.0) - مرآة Clearnet (الإنترنت العام): https://eyedeekay.github.io/javadoc-i2p/

**الشيفرة المصدرية:** - GitLab (الرسمي): https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master - مرآة GitHub: https://github.com/i2p/i2p.i2p

### معايير تنسيق الروابط

```markdown
✅ GOOD: [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
✅ GOOD: [Configuration Specification](https://geti2p.net/spec/configuration)

❌ BAD: See the ClientApp docs at http://idk.i2p/...
❌ BAD: [link](url) with no descriptive text
```
---

## تتبع الإصدارات

### البيانات الوصفية للمستند

يجب أن يتضمن كل مستند تقني البيانات الوصفية للإصدار في frontmatter (قسم البيانات التمهيدية في أعلى الملف):

```markdown
---
title: "Document Title"
description: "Brief description"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
**تعريفات الحقول:** - `lastUpdated`: السنة-الشهر لتاريخ آخر مراجعة/تحديث للمستند - `accurateFor`: إصدار I2P الذي تم التحقق من المستند مقابله - `reviewStatus`: إحدى القيم "draft"، "needs-review"، "verified"، "outdated"

### مراجع الإصدارات في المحتوى

عند الإشارة إلى الإصدارات: 1. استخدم **عريض** للإصدار الحالي: "**الإصدار 2.10.0** (سبتمبر 2025)" 2. اذكر رقم الإصدار وتاريخه في المراجع التاريخية 3. دوّن إصدار واجهة برمجة التطبيقات (API) بشكل منفصل عن إصدار I2P عند الاقتضاء

**مثال:**

```markdown
Managed clients were introduced in **version 0.9.4** (December 17, 2012) and 
remain the recommended architecture as of **version 2.10.0** (September 9, 2025). 
The current API version is **0.9.66**.
```
### توثيق التغييرات مع مرور الوقت

بالنسبة للميزات التي تطورت:

```markdown
**Version history:**
- **0.9.4 (December 2012)** - Managed clients introduced
- **0.9.42 (2019)** - clients.config.d/ directory structure added
- **1.7.0 (2021)** - ShellService added for external program tracking
- **2.10.0 (September 2025)** - Current release, no API changes to managed clients
```
### إشعارات إيقاف الدعم

عند توثيق الميزات المهملة:

```markdown
> **Deprecated:** This feature was deprecated in version X.Y.Z and will be removed 
> in version A.B.C. Use [alternative feature](link) instead.
```
---

## معايير المصطلحات

### مصطلحات I2P الرسمية

استخدم هذه المصطلحات بالضبط على نحو متسق:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct Term</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Avoid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P node, I2P client (ambiguous)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">eepsite</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P website, hidden service (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">connection, circuit (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">netDb</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">network database, DHT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lease set</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination info</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">address, endpoint</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">base64 destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P address, .i2p address</td>
    </tr>
  </tbody>
</table>
### مصطلحات العميل المُدار

عند توثيق العملاء المُدارين:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use This</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Not This</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed application</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unmanaged client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">legacy client, static client</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ClientAppManager</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application manager, client manager</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lifecycle methods</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">state methods, control methods</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">client registry</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application registry, name service</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port mapper</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port registry, service directory</td>
    </tr>
  </tbody>
</table>
### مصطلحات التهيئة

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Incorrect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.cfg, client.config</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config.d/</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.d/, config.d/</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.cfg</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel.config</td>
    </tr>
  </tbody>
</table>
### أسماء الحزم والأصناف

احرص على استخدام الأسماء المؤهَّلة بالكامل عند أول ذكر، ثم استخدم الأسماء القصيرة بعد ذلك:

```markdown
The `net.i2p.app.ClientApp` interface requires implementation of three lifecycle 
methods. When a ClientApp starts, the manager calls `startup()`...
```
---

## أمثلة على التعليمات البرمجية والتنسيق

### أمثلة على التعليمات البرمجية لـ Java

استخدم تمييز بناء الجملة بشكل صحيح وأمثلة كاملة:

```markdown
### Example: Registering with Port Mapper

\`\`\`java
// Register HTTP proxy service
context.portMapper().register(
    PortMapper.SVC_HTTP_PROXY, 
    "127.0.0.1", 
    4444
);

// Later, retrieve the port
int port = context.portMapper().getPort(PortMapper.SVC_HTTP_PROXY);
if (port == -1) {
    // Service not registered
}
\`\`\`
```
**متطلبات مثال الشيفرة:** 1. تضمين تعليقات تشرح الأسطر الأساسية 2. إظهار معالجة الأخطاء حيثما كان ذلك مناسبا 3. استخدام أسماء متغيرات واقعية 4. مطابقة اصطلاحات ترميز I2P (مسافة بادئة من 4 مسافات) 5. إظهار جمل الاستيراد إن لم تكن واضحة من السياق

### أمثلة التكوين

اعرض أمثلة تكوين كاملة وصحيحة:

```markdown
### Example: clients.config.d/ Entry

File: `clients.config.d/00-console.config`

\`\`\`properties
# Router console configuration
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
\`\`\`
```
### أمثلة سطر الأوامر

استخدم `$` لأوامر المستخدم، و`#` للمستخدم الجذر:

```markdown
\`\`\`bash
# Install I2P on Debian/Ubuntu
$ sudo apt-get install i2p

# Start the router
$ i2prouter start
\`\`\`
```
### كود ضمن السطر

استخدم backticks (العلامات المعكوسة) لـ: - أسماء الأساليب: `startup()` - أسماء الأصناف: `ClientApp` - أسماء الخصائص: `clientApp.0.main` - أسماء الملفات: `clients.config` - الثوابت: `SVC_HTTP_PROXY` - أسماء الحِزم: `net.i2p.app`

---

## النبرة والصوت

### احترافي لكنه سهل الفهم

اكتب لجمهور تقني من دون نبرة استعلاء:

```markdown
❌ BAD: "Obviously, you should implement the startup() method."
✅ GOOD: "Managed clients must implement the startup() method to initialize resources."

❌ BAD: "Even a junior dev knows you need to call notify()."
✅ GOOD: "The manager requires at least one notify() call during startup to track state transitions."
```
### المبني للمعلوم

استخدموا صيغة المبني للمعلوم لتحقيق الوضوح:

```markdown
❌ PASSIVE: "The ClientAppManager is notified by the client when state changes."
✅ ACTIVE: "The client notifies ClientAppManager when state changes."
```
### الصيغة الأمرية في التعليمات

استخدم صيغ الأمر المباشرة في المحتوى الإجرائي:

```markdown
✅ "Implement these three lifecycle methods:"
✅ "Call manager.notify() after changing state."
✅ "Register services using context.portMapper().register()"
```
### تجنّب المصطلحات غير الضرورية

اشرح المصطلحات عند أول استخدام:

```markdown
✅ GOOD: "The netDb (network database) stores information about I2P routers and destinations."
❌ BAD: "Query the netDb for peer info." (no explanation)
```
### إرشادات علامات الترقيم

1. **لا تستخدم em-dashes (الشرطات الطويلة)** - استخدم شرطات عادية، أو فواصل، أو فواصل منقوطة بدلاً منها
2. استخدم **Oxford comma (فاصلة أوكسفورد)** في القوائم: "console, i2ptunnel, and Jetty"
3. **النقاط داخل كتل الشيفرة** فقط عند الضرورة النحوية
4. **القوائم التسلسلية** تستخدم الفواصل المنقوطة عندما تحتوي العناصر على فواصل

---

## بنية المستند

### ترتيب الأقسام القياسي

لوثائق واجهة برمجة التطبيقات:

1. **نظرة عامة** - ما الذي تفعله الميزة، ولماذا توجد
2. **التنفيذ** - كيفية تنفيذها/استخدامها
3. **التهيئة** - كيفية تهيئتها
4. **مرجع واجهة برمجة التطبيقات (API)** - أوصاف تفصيلية للأساليب/الخصائص
5. **أمثلة** - أمثلة كاملة تعمل
6. **أفضل الممارسات** - نصائح وتوصيات
7. **سجل الإصدارات** - متى قُدمت، والتغييرات مع مرور الوقت
8. **المراجع** - روابط إلى وثائق ذات صلة

### هرمية العناوين

استخدم مستويات العناوين الدلالية:

```markdown
# Document Title (h1 - only one per document)

## Major Section (h2)

### Subsection (h3)

#### Detail Section (h4)

**Bold text for emphasis within sections**
```
### مربعات المعلومات

استخدم كتل الاقتباس للتنبيهات الخاصة:

```markdown
> **Note:** Additional information that clarifies the main content.

> **Warning:** Important information about potential issues or breaking changes.

> **Deprecated:** This feature is deprecated and will be removed in version X.Y.Z.

> **Status:** Current implementation status or version information.
```
### القوائم والتنظيم

**القوائم غير المرتبة** للعناصر غير المتسلسلة:

```markdown
- First item
- Second item
- Third item
```
**القوائم المرتبة** للخطوات المتسلسلة:

```markdown
1. First step
2. Second step
3. Third step
```
**قوائم التعاريف** لشرح المصطلحات:

```markdown
**Term One**
: Explanation of term one

**Term Two**  
: Explanation of term two
```
---

## الأخطاء الشائعة التي يجب تجنبها

### 1. الخلط بين الأنظمة المتشابهة

**لا تخلط بين:** - سجل ClientAppManager مقابل PortMapper - أنواع tunnel الخاصة بـ i2ptunnel مقابل ثوابت خدمة port mapper - ClientApp مقابل RouterApp (سياقات مختلفة) - العملاء المُدارون مقابل العملاء غير المُدارين

**وضّح دائمًا أي نظام** تتحدث عنه:

```markdown
✅ "Register with ClientAppManager using manager.register(this) for name-based lookup."
✅ "Register with PortMapper using context.portMapper().register() for port discovery."
```
### 2. مراجع إلى إصدارات قديمة

**لا تفعل:** - الإشارة إلى الإصدارات القديمة على أنها "الحالية" - وضع روابط إلى وثائق واجهة برمجة التطبيقات (API) المتقادّمة - استخدام تواقيع أساليب مهملة في الأمثلة

**قم بما يلي:** - تحقّق من ملاحظات الإصدار قبل النشر - تحقّق من أن توثيق واجهة برمجة التطبيقات (API) يطابق الإصدار الحالي - حدّث الأمثلة لاستخدام أفضل الممارسات الحالية

### 3. عناوين URL يتعذر الوصول إليها

**لا تفعل:** - لا تضع روابط فقط إلى نطاقات .i2p من دون بدائل على الإنترنت العام (clearnet) - لا تستخدم روابط التوثيق المعطّلة أو القديمة - لا تضع روابط إلى مسارات file:// محلية

**افعل:** - وفّر بدائل clearnet (الإنترنت العام) لجميع روابط I2P الداخلية - تحقّق من إمكانية الوصول إلى عناوين URL قبل النشر - استخدم عناوين URL دائمة (geti2p.net، وليس استضافة مؤقتة)

### 4. أمثلة على الشيفرة غير المكتملة

**لا تفعل:** - عرض مقتطفات بدون سياق - إهمال معالجة الأخطاء - استخدام متغيرات غير معرّفة - تجاوز عبارات الاستيراد عندما لا يكون ذلك واضحًا

**افعل:** - اعرض أمثلة كاملة قابلة للترجمة - أدرج معالجة الأخطاء اللازمة - اشرح ما يفعله كل سطر مهم - اختبر الأمثلة قبل النشر

### 5. عبارات ملتبسة

```markdown
❌ "Some applications register services."
✅ "Applications implementing ClientApp may register with ClientAppManager 
   using manager.register(this) to enable name-based lookup."

❌ "Configuration files go in the config directory."
✅ "Modern I2P installations store client configurations in 
   $I2P/clients.config.d/ as individual files."
```
---

## اتفاقيات Markdown (لغة ترميز مبسطة)

### تسمية الملفات

استخدم صيغة kebab-case (تنسيق تسمية يفصل الكلمات بشرطات وصل (-)) لأسماء الملفات:
- `managed-clients.md`
- `port-mapper-guide.md`
- `configuration-reference.md`

### تنسيق Frontmatter (البيانات التعريفية التمهيدية)

احرص دائماً على تضمين مقدمة YAML:

```yaml
---
title: "Document Title"
description: "Brief description under 160 characters"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
### تنسيق الروابط

**الروابط الداخلية** (ضمن الوثائق):

```markdown
See [clients.config specification](https://geti2p.net/spec/configuration#clients-config)
```
**روابط خارجية** (إلى موارد أخرى):

```markdown
For more details, see [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
```
**روابط مستودعات الشيفرة**:

```markdown
View source: [ClientApp.java](https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master/core/java/src/net/i2p/app/ClientApp.java)
```
### تنسيق الجداول

استخدم جداول Markdown بنكهة GitHub:

```markdown
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `main` | String | (required) | Full class name |
| `delay` | Integer | 120 | Seconds before start |
| `onBoot` | Boolean | false | Force immediate start |
```
### وسوم لغة كتل الشيفرة

حدد دائمًا اللغة لتمييز بناء الجملة:

```markdown
\`\`\`java
// Java code
\`\`\`

\`\`\`bash
# Shell commands
\`\`\`

\`\`\`properties
# Configuration files
\`\`\`

\`\`\`xml
<!-- XML files -->
\`\`\`
```
---

## قائمة التحقق للمراجعة

قبل نشر التوثيق، تحقّق مما يلي:

- [ ] تم التحقق من جميع الادعاءات التقنية مقابل الشيفرة المصدرية أو التوثيق الرسمي
- [ ] أرقام الإصدارات والتواريخ محدّثة
- [ ] جميع عناوين URL قابلة للوصول من clearnet (الإنترنت العام/المكشوف) (أو تم توفير بدائل)
- [ ] أمثلة الشيفرة مكتملة ومختبرة
- [ ] المصطلحات تتبع اصطلاحات I2P
- [ ] بدون em-dashes (استخدم الشرطات العادية أو علامات ترقيم أخرى)
- [ ] الـ Frontmatter (بيانات تمهيدية في رأس الملف) مكتملة ودقيقة
- [ ] التسلسل الهرمي للعناوين دلالي (h1 → h2 → h3)
- [ ] القوائم والجداول منسّقة بشكل صحيح
- [ ] قسم المراجع يتضمن جميع المصادر المذكورة
- [ ] المستند يتبع إرشادات البنية
- [ ] النبرة مهنية ولكن يسهل فهمها
- [ ] يتم التمييز بوضوح بين المفاهيم المتشابهة
- [ ] لا توجد روابط أو مراجع معطلة
- [ ] أمثلة الضبط صالحة ومحدّثة

---

**الملاحظات:** إذا وجدت مشكلات أو كانت لديك اقتراحات بشأن هذه الإرشادات، يُرجى تقديمها عبر قنوات تطوير I2P الرسمية.
