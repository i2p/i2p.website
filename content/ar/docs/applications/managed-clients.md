---
title: "العملاء المُدارون"
description: "كيفية تكامل التطبيقات المُدارة من قِبل الراوتر مع ClientAppManager ومُخطط المنافذ"
slug: "managed-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. نظرة عامة

الإدخالات في [`clients.config`](/docs/specs/configuration/#clients-config) تخبر الـ router أي التطبيقات يتم تشغيلها عند بدء التشغيل. كل إدخال قد يعمل كـ **managed** client (مفضل) أو كـ **unmanaged** client. الـ managed clients تتعاون مع `ClientAppManager`، والذي:

- يقوم بإنشاء التطبيق وتتبع حالة دورة الحياة لوحدة تحكم الموجه (router console)
- يوفر عناصر التحكم في البدء/الإيقاف للمستخدم ويفرض عمليات إيقاف نظيفة عند خروج الموجه
- يستضيف **سجل عملاء** خفيف و**مُخطط منافذ** حتى تتمكن التطبيقات من اكتشاف خدمات بعضها البعض

العملاء غير المُدارين (Unmanaged clients) يستدعون ببساطة دالة `main()`؛ استخدمها فقط للكود القديم الذي لا يمكن تحديثه.

## 2. تنفيذ عميل مُدار

يجب على العملاء المُدارة تنفيذ إما `net.i2p.app.ClientApp` (للتطبيقات الموجهة للمستخدم) أو `net.i2p.router.app.RouterApp` (لامتدادات الـ router). قم بتوفير أحد الـ constructors أدناه حتى يتمكن المدير من توفير context ومعاملات التكوين:

```java
public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)
```
```java
public MyRouterApp(RouterContext context, ClientAppManager manager, String[] args)
```
يحتوي مصفوفة `args` على القيم المُكوَّنة في `clients.config` أو الملفات الفردية في `clients.config.d/`. قم بتوسيع الفئات المساعدة `ClientApp` / `RouterApp` عندما يكون ذلك ممكناً لوراثة الربط الافتراضي لدورة الحياة.

### 2.1 Lifecycle Methods

من المتوقع أن ينفذ العملاء المُدارون (Managed clients):

- `startup()` - تنفيذ التهيئة والعودة بسرعة. يجب استدعاء `manager.notify()` مرة واحدة على الأقل للانتقال من حالة INITIALIZED.
- `shutdown(String[] args)` - تحرير الموارد وإيقاف خيوط العمل في الخلفية. يجب استدعاء `manager.notify()` مرة واحدة على الأقل لتغيير الحالة إلى STOPPING أو STOPPED.
- `getState()` - إبلاغ لوحة التحكم بما إذا كان التطبيق قيد التشغيل أو البدء أو الإيقاف أو فشل

يستدعي المدير هذه الوظائف (methods) عندما يتفاعل المستخدمون مع وحدة التحكم.

### 2.2 Advantages

- تقارير حالة دقيقة في وحدة تحكم الراوتر
- عمليات إعادة تشغيل نظيفة دون تسريب threads أو مراجع ثابتة
- استهلاك ذاكرة أقل بمجرد توقف التطبيق
- تسجيل مركزي والإبلاغ عن الأخطاء عبر السياق المُدرج

## 3. Unmanaged Clients (Fallback Mode)

إذا لم يقم الصف المُكوَّن بتنفيذ واجهة مُدارة، يقوم الموجه بتشغيله عن طريق استدعاء `main(String[] args)` ولا يمكنه تتبع العملية الناتجة. تعرض وحدة التحكم معلومات محدودة وقد لا يتم تشغيل خطافات الإيقاف. احتفظ بهذا الوضع للسكريبتات أو الأدوات المساعدة ذات الاستخدام الواحد التي لا يمكنها اعتماد واجهات برمجة التطبيقات المُدارة.

## 4. Client Registry

يمكن للعملاء المُدارة وغير المُدارة تسجيل أنفسها لدى المدير بحيث يمكن للمكونات الأخرى استرجاع مرجع بالاسم:

```java
manager.register(this);
```
يستخدم التسجيل القيمة المُرجعة من `getName()` الخاصة بالعميل كمفتاح للسجل. تتضمن التسجيلات المعروفة `console` و `i2ptunnel` و `Jetty` و `outproxy` و `update`. استرجع عميلاً باستخدام `ClientAppManager.getRegisteredApp(String name)` لتنسيق الميزات (على سبيل المثال، استعلام console عن Jetty للحصول على تفاصيل الحالة).

لاحظ أن سجل العملاء (client registry) ومُخطط المنافذ (port mapper) هما نظامان منفصلان. يُمكّن سجل العملاء التواصل بين التطبيقات عن طريق البحث بالاسم، بينما يقوم مُخطط المنافذ بربط أسماء الخدمات بتركيبات host:port لاكتشاف الخدمات.

## 3. العملاء غير المُدارة (وضع الاحتياطي)

يوفر port mapper دليلاً بسيطاً لخدمات TCP الداخلية. قم بتسجيل منافذ loopback حتى يتجنب المتعاونون العناوين المشفرة بشكل ثابت:

```java
context.portMapper().register(PortMapper.SVC_HTTPS_PROXY, 4445);
```
أو مع تحديد صريح للمضيف:

```java
context.portMapper().register(PortMapper.SVC_HTTP_PROXY, "127.0.0.1", 4444);
```
ابحث عن الخدمات باستخدام `PortMapper.getPort(String name)` (يُرجع -1 إذا لم يتم العثور عليها) أو `getPort(String name, int defaultPort)` (يُرجع القيمة الافتراضية إذا لم يتم العثور عليها). تحقق من حالة التسجيل باستخدام `isRegistered(String name)` واسترجع المضيف المسجل باستخدام `getActualHost(String name)`.

ثوابت خدمة تعيين المنافذ الشائعة من `net.i2p.util.PortMapper`:

- `SVC_CONSOLE` - وحدة تحكم الموجه Router (المنفذ الافتراضي 7657)
- `SVC_HTTP_PROXY` - وكيل HTTP (المنفذ الافتراضي 4444)
- `SVC_HTTPS_PROXY` - وكيل HTTPS (المنفذ الافتراضي 4445)
- `SVC_I2PTUNNEL` - مدير I2PTunnel
- `SVC_SAM` - جسر SAM (المنفذ الافتراضي 7656)
- `SVC_SAM_SSL` - جسر SAM بـ SSL
- `SVC_SAM_UDP` - SAM بـ UDP
- `SVC_BOB` - جسر BOB (المنفذ الافتراضي 2827)
- `SVC_EEPSITE` - موقع eepsite قياسي (المنفذ الافتراضي 7658)
- `SVC_HTTPS_EEPSITE` - موقع eepsite بـ HTTPS
- `SVC_IRC` - نفق IRC (المنفذ الافتراضي 6668)
- `SVC_SUSIDNS` - SusiDNS

ملاحظة: `httpclient` و `httpsclient` و `httpbidirclient` هي أنواع أنفاق i2ptunnel (تُستخدم في إعدادات `tunnel.N.type`)، وليست ثوابت خدمة port mapper.

## 4. سجل العملاء

### 2.1 أساليب دورة الحياة

اعتبارًا من الإصدار 0.9.42، يدعم الموجه (router) تقسيم التكوين إلى ملفات فردية ضمن دليل `clients.config.d/`. يحتوي كل ملف على خصائص لعميل واحد مع جميع الخصائص مسبوقة بـ `clientApp.0.`:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
```
هذا هو النهج الموصى به للتثبيتات والإضافات الجديدة.

### 2.2 المزايا

للتوافق مع الإصدارات السابقة، يستخدم التنسيق التقليدي الترقيم المتسلسل:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.1.main=net.i2p.apps.systray.UrlLauncher
clientApp.1.name=URL Launcher
clientApp.1.delay=5
```
### 6.3 Configuration Properties

**مطلوب:** - `main` - اسم الفئة الكامل الذي ينفذ ClientApp أو RouterApp، أو يحتوي على `main(String[] args)` ثابت

**اختياري:** - `name` - اسم العرض لوحدة تحكم الموجه (router console) (افتراضيًا اسم الفئة) - `args` - معاملات مفصولة بمسافة أو علامة تبويب (تدعم النصوص المقتبسة) - `delay` - الثواني قبل البدء (افتراضيًا 120) - `onBoot` - يفرض `delay=0` إذا كان true - `startOnLoad` - يمكّن/يعطل العميل (افتراضيًا true)

**خاص بالإضافة:** - `stopargs` - المعاملات الممررة أثناء الإيقاف - `uninstallargs` - المعاملات الممررة أثناء إلغاء تثبيت الإضافة - `classpath` - إدخالات مسار الفئة الإضافية مفصولة بفواصل

**استبدال المتغيرات للإضافات:** - `$I2P` - دليل I2P الأساسي - `$CONFIG` - دليل إعدادات المستخدم (مثال: ~/.i2p) - `$PLUGIN` - دليل الإضافات - `$OS` - اسم نظام التشغيل - `$ARCH` - اسم البنية المعمارية

## 5. Port Mapper

- فضّل العملاء المُدارين؛ واستخدم العملاء غير المُدارين فقط عند الضرورة القصوى.
- اجعل عمليات التهيئة والإيقاف خفيفة الوزن حتى تظل عمليات console سريعة الاستجابة.
- استخدم أسماء واضحة للسجل والمنافذ حتى تتمكن أدوات التشخيص (والمستخدمون النهائيون) من فهم وظيفة الخدمة.
- تجنّب استخدام الـ static singletons - اعتمد على السياق والمدير المُحقَنين لمشاركة الموارد.
- استدعِ `manager.notify()` عند كل انتقال بين الحالات للحفاظ على دقة حالة console.
- إذا كان يجب عليك العمل في JVM منفصل، وثّق كيفية إظهار السجلات والتشخيصات في console الرئيسي.
- بالنسبة للبرامج الخارجية، فكّر في استخدام ShellService (المُضاف في الإصدار 1.7.0) للحصول على مزايا العملاء المُدارين.

## 6. تنسيق الإعداد

تم تقديم العملاء المُدارة في **الإصدار 0.9.4** (17 ديسمبر 2012) وتظل البنية الموصى بها حتى **الإصدار 2.10.0** (9 سبتمبر 2025). ظلت واجهات برمجة التطبيقات الأساسية مستقرة دون أي تغييرات جذرية خلال هذه الفترة:

- توقيعات المُنشئ (Constructor) دون تغيير
- دوال دورة الحياة (startup، shutdown، getState) دون تغيير
- دوال تسجيل ClientAppManager دون تغيير
- دوال تسجيل والبحث في PortMapper دون تغيير

التحسينات البارزة: - **0.9.42 (2019)** - هيكل دليل clients.config.d/ لملفات التكوين الفردية - **1.7.0 (2021)** - إضافة ShellService لتتبع حالة البرامج الخارجية - **2.10.0 (2025)** - الإصدار الحالي بدون تغييرات في واجهة برمجة التطبيقات للعملاء المُدارين

الإصدار الرئيسي التالي سيتطلب Java 17+ كحد أدنى (متطلب بنية تحتية، وليس تغييراً في الـ API).

## References

- [مواصفات clients.config](/docs/specs/configuration/#clients-config)
- [مواصفات ملف التكوين](/docs/specs/configuration/)
- [فهرس الوثائق التقنية لـ I2P](/docs/)
- [ClientAppManager Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientAppManager.html) (API 0.9.66)
- [PortMapper Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/util/PortMapper.html) (API 0.9.66)
- [واجهة ClientApp](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html) (API 0.9.66)
- [واجهة RouterApp](https://i2p.github.io/i2p.i2p/net/i2p/router/app/RouterApp.html) (API 0.9.66)
- [Javadoc بديل (مستقر)](https://docs.i2p-projekt.de/javadoc/)
- [Javadoc بديل (نسخة مرآة على الشبكة العادية)](https://eyedeekay.github.io/javadoc-i2p/)

> **ملاحظة:** تستضيف شبكة I2P وثائق شاملة على http://idk.i2p/javadoc-i2p/ والتي تتطلب router من I2P للوصول إليها. للوصول عبر الإنترنت العادي، استخدم نسخة GitHub Pages المذكورة أعلاه.
