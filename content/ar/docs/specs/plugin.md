---
title: "تنسيق حزمة المكوّن الإضافي"
description: ".xpi2p / .su3 قواعد التحزيم لإضافات I2P"
slug: "plugin"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## نظرة عامة

ملحقات I2P هي أرشيفات موقّعة توسّع وظائف الـ router (الموجّه الخاص بـ I2P). تُوزَّع كملفات `.xpi2p` أو `.su3`، وتُثبَّت في `~/.i2p/plugins/<name>/` (أو `%APPDIR%\I2P\plugins\<name>\` على Windows)، وتعمل بكامل صلاحيات الـ router من دون عزل (sandboxing).

### أنواع الإضافات المدعومة

- تطبيقات ويب للوحة التحكم
- eepsites جديدة مع cgi-bin وتطبيقات ويب
- سمات لوحة التحكم
- ترجمات لوحة التحكم
- برامج Java (ضمن العملية أو على JVM منفصل (آلة جافا الافتراضية))
- سكربتات shell والملفات الثنائية الأصلية

### نموذج الأمان

**حرِج:** تعمل الإضافات في نفس JVM (آلة جافا الافتراضية) وبأذونات متطابقة مع الـ I2P router. لديها وصول غير مقيّد إلى: - نظام الملفات (قراءة وكتابة) - واجهات برمجة تطبيقات الـ router والحالة الداخلية - اتصالات الشبكة - تنفيذ البرامج الخارجية

يجب التعامل مع المكوّنات الإضافية على أنها برمجيات موثوقة بالكامل. يجب على المستخدمين التحقق من مصادر المكوّنات الإضافية وتواقيعها قبل التثبيت.

---

## تنسيقات الملفات

### صيغة SU3 (موصى بها بشدة)

**الحالة:** نشط، التنسيق المفضّل منذ I2P 0.9.15 (سبتمبر 2014)

يوفّر تنسيق `.su3` ما يلي: - **مفاتيح توقيع RSA-4096** (مقابل DSA-1024 في xpi2p) - التوقيع مُخزَّن في رأس الملف - الرقم السحري: `I2Psu3` - توافقية مستقبلية أفضل

**البنية:**

```
[SU3 Header with RSA-4096 signature]
[ZIP Archive]
  ├── plugin.config (required)
  ├── console/
  ├── lib/
  ├── webapps/
  └── [other plugin files]
```
### تنسيق XPI2P (متقادم، مهمل)

**الحالة:** مدعوم لأغراض التوافق مع الإصدارات السابقة، غير موصى به للمكوّنات الإضافية الجديدة

يستخدم تنسيق `.xpi2p` تواقيع تشفيرية أقدم: - **تواقيع DSA-1024** (مهملة وفقًا لـ NIST-800-57) - توقيع DSA بطول 40 بايت يُضاف في مقدمة ملف ZIP - يتطلب الحقل `key` في plugin.config

**البنية:**

```
[40-byte DSA signature]
[16-byte version string (UTF-8, zero-padded)]
[ZIP Archive]
```
**مسار الترحيل:** عند الانتقال من xpi2p إلى su3، وفّر كلًا من `updateURL` و`updateURL.su3` خلال فترة الانتقال. تُعطي routers الحديثة (0.9.15+) الأولوية تلقائيًا لـ SU3.

---

## هيكل الأرشيف و plugin.config

### الملفات المطلوبة

**plugin.config** - ملف تهيئة قياسي لـ I2P يحتوي على أزواج المفتاح-القيمة

### الخصائص المطلوبة

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Installation directory name, must match for updates</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Alphanumeric, no spaces</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>signer</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Developer contact information</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>user@mail.i2p</code> format recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>version</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Plugin version for update comparison</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Max 16 bytes, parsed by VersionComparator</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>key</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA public key (172 B64 chars ending with '=')</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Omit for SU3 format</strong></td></tr>
  </tbody>
</table>
**أمثلة على صيغ الإصدار:** - `1.2.3` - `1.2.3-4` - `2.0.0-beta.1`

الفواصل المسموح بها: `.` (نقطة)، `-` (شرطة)، `_` (شرطة سفلية)

### خصائص البيانات الوصفية الاختيارية

#### عرض المعلومات

- `date` - تاريخ الإصدار (طابع زمني طويل في Java)
- `author` - اسم المطوّر (يُوصى بـ `user@mail.i2p`)
- `description` - وصف باللغة الإنجليزية
- `description_xx` - وصف محلي (xx = رمز اللغة)
- `websiteURL` - الصفحة الرئيسية للملحق (`http://foo.i2p/`)
- `license` - معرّف الترخيص (مثل "Apache-2.0", "GPL-3.0")

#### تحديث الإعدادات

- `updateURL` - موقع تحديث XPI2P (قديم)
- `updateURL.su3` - موقع تحديث SU3 (مُفضَّل)
- `min-i2p-version` - أدنى إصدار مطلوب من I2P
- `max-i2p-version` - أقصى إصدار متوافق من I2P
- `min-java-version` - أدنى إصدار من Java (مثلًا، `1.7`، `17`)
- `min-jetty-version` - أدنى إصدار من Jetty (استخدم `6` لـ Jetty 6+)
- `max-jetty-version` - أقصى إصدار من Jetty (استخدم `5.99999` لـ Jetty 5)

#### سلوك التثبيت

- `dont-start-at-install` - القيمة الافتراضية `false`. إذا كانت `true`، يتطلب بدءاً يدوياً
- `router-restart-required` - القيمة الافتراضية `false`. يبلغ المستخدم بأن إعادة التشغيل مطلوبة بعد التحديث
- `update-only` - القيمة الافتراضية `false`. يفشل إذا لم يكن المُلحق مثبت مسبقاً
- `install-only` - القيمة الافتراضية `false`. يفشل إذا كان المُلحق موجود بالفعل
- `min-installed-version` - أدنى إصدار مطلوب للتحديث
- `max-installed-version` - أقصى إصدار يمكن تحديثه
- `disableStop` - القيمة الافتراضية `false`. يخفي زر الإيقاف إذا كانت `true`

#### تكامل وحدة التحكم

- `consoleLinkName` - نص رابط شريط ملخّص وحدة التحكم
- `consoleLinkName_xx` - نص رابط مترجم حسب اللغة (xx = رمز اللغة)
- `consoleLinkURL` - وجهة الرابط (على سبيل المثال، `/appname/index.jsp`)
- `consoleLinkTooltip` - نص التلميح عند تمرير المؤشر (مدعوم منذ 0.7.12-6)
- `consoleLinkTooltip_xx` - التلميح المترجم
- `console-icon` - مسار أيقونة 32×32 (مدعوم منذ 0.9.20)
- `icon-code` - صورة PNG مقاس 32×32 مُرمَّزة بصيغة Base64 للإضافات التي لا تحتوي على موارد ويب (منذ 0.9.25)

#### متطلبات المنصّة (للعرض فقط)

- `required-platform-OS` - متطلب نظام التشغيل (غير ملزم)
- `other-requirements` - متطلبات إضافية (مثلًا، "Python 3.8+")

#### إدارة التبعيات (غير منفذة)

- `depends` - قائمة تبعيات الإضافة مفصولة بفواصل
- `depends-version` - متطلبات الإصدارات للتبعيات
- `langs` - محتويات حزمة اللغة
- `type` - نوع الإضافة (app/theme/locale/webapp)

### استبدال المتغيرات في عنوان URL للتحديث

**حالة الميزة:** متاحة منذ I2P 1.7.0 (0.9.53)

كلٌّ من `updateURL` و`updateURL.su3` يدعمان متغيّرات خاصّة بالمنصّة:

**المتغيّرات:** - `$OS` - نظام التشغيل: `windows`, `linux`, `mac` - `$ARCH` - المعمارية: `386`, `amd64`, `arm64`

**مثال:**

```properties
updateURL.su3=http://foo.i2p/downloads/foo-$OS-$ARCH.su3
```
**النتيجة على Windows AMD64:**

```
http://foo.i2p/downloads/foo-windows-amd64.su3
```
هذا يتيح استخدام ملف plugin.config واحد لكل بناء مخصص لمنصة محددة.

---

## بنية الدليل

### التخطيط القياسي

```
plugins/
└── pluginname/
    ├── plugin.config (required)
    ├── console/
    │   ├── locale/          # Translation JARs
    │   ├── themes/          # Console themes
    │   ├── webapps/         # Web applications
    │   └── webapps.config   # Webapp configuration
    ├── eepsite/
    │   ├── cgi-bin/
    │   ├── docroot/
    │   ├── logs/
    │   ├── webapps/
    │   └── jetty.xml
    ├── lib/
    │   └── *.jar            # Plugin libraries
    └── clients.config       # Client startup configuration
```
### أغراض الدليل

**console/locale/** - ملفات JAR تحتوي على حزم موارد لترجمات I2P الأساسية - يجب أن تكون الترجمات الخاصة بالمكونات الإضافية في `console/webapps/*.war` أو `lib/*.jar`

**console/themes/** - يحتوي كل دليل فرعي على سمة كاملة للوحة التحكم - تُضاف تلقائيًا إلى مسار البحث عن السمات

**console/webapps/** - ملفات `.war` للتكامل مع وحدة التحكم - تُشغَّل تلقائياً ما لم تُعطَّل في `webapps.config` - لا يلزم أن يطابق اسم ملف WAR اسم المكوّن الإضافي

**eepsite/** - eepsite كامل مع مثيل Jetty الخاص به - يتطلب تهيئة `jetty.xml` مع استبدال المتغيرات - راجع أمثلة zzzot وملحق pebble

**lib/** - مكتبات JAR الخاصة بالملحقات - حدّد ضمن classpath (مسار الأصناف) عبر `clients.config` أو `webapps.config`

---

## تهيئة تطبيق الويب

### تنسيق webapps.config

ملف إعدادات I2P قياسي يتحكم في سلوك تطبيق الويب.

**الصياغة:**

```properties
# Disable autostart
webapps.warname.startOnLoad=false

# Add classpath JARs (as of API 0.9.53, works for any warname)
webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar
```
**ملاحظات مهمة:** - قبل router 0.7.12-9، استخدم `plugin.warname.startOnLoad` للتوافق - قبل API 0.9.53، كان classpath (مسار الأصناف) يعمل فقط إذا كان warname يطابق اسم الملحق - اعتبارًا من 0.9.53+، يعمل classpath مع أي اسم لتطبيق ويب

### أفضل الممارسات لتطبيقات الويب

1. **تنفيذ ServletContextListener**
   - نفّذ `javax.servlet.ServletContextListener` لأغراض التنظيف
   - أو أعد تعريف `destroy()` في servlet (مكوّن خادم في Java)
   - يضمن الإيقاف السليم أثناء التحديثات وعند إيقاف router

2. **إدارة المكتبات**
   - ضع ملفات JAR المشتركة في `lib/`، وليس داخل WAR
   - ارجع عبر classpath (مسار الأصناف) الخاص بـ `webapps.config`
   - يتيح تثبيت/تحديث الملحقات بشكل منفصل

3. **تجنّب تعارض المكتبات**
   - لا تُضمِّن أبداً ملفات JAR الخاصة بـ Jetty أو Tomcat أو servlet
   - لا تُضمِّن أبداً ملفات JAR من تثبيت I2P القياسي
   - راجع قسم classpath الخاص بالمكتبات القياسية

4. **متطلبات التصريف**
   - لا تُضمِّن ملفات المصدر `.java` أو `.jsp`
   - قم بتصريف جميع ملفات JSP مسبقًا لتجنّب تأخيرات بدء التشغيل
   - لا يمكن افتراض توفّر مصرّف Java/JSP

5. **التوافق مع واجهة برمجة تطبيقات Servlet**
   - I2P يدعم Servlet 3.0 (منذ 0.9.30)
   - **مسح التعليقات التوضيحية غير مدعوم** (@WebContent)
   - يجب توفير واصف النشر التقليدي `web.xml`

6. **إصدار Jetty**
   - الحالي: Jetty 9 (I2P 0.9.30+)
   - استخدم `net.i2p.jetty.JettyStart` للتجريد
   - يحمي من تغييرات واجهة برمجة تطبيقات Jetty

---

## إعدادات العميل

### تنسيق clients.config

يحدد العملاء (الخدمات) التي يبدأ تشغيلها بواسطة المكوّن الإضافي.

**العميل الأساسي:**

```properties
clientApp.0.main=com.example.PluginMain
clientApp.0.name=Example Plugin Service
clientApp.0.delay=30
clientApp.0.args=arg1 arg2 $PLUGIN/config.properties
```
**عميل مع إيقاف/إلغاء التثبيت:**

```properties
clientApp.0.stopargs=stop
clientApp.0.uninstallargs=uninstall
clientApp.0.classpath=$PLUGIN/lib/plugin.jar,$I2P/lib/i2p.jar
```
### مرجع الخصائص

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>main</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fully qualified class name implementing ClientApp interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Display name for user interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>delay</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Startup delay in seconds (default: 0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>args</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Space-separated arguments passed to constructor</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>stopargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments for shutdown (must handle gracefully)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>uninstallargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments called before plugin deletion</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>classpath</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated JAR paths</td></tr>
  </tbody>
</table>
### استبدال المتغيرات

يتم استبدال المتغيرات التالية في `args` و`stopargs` و`uninstallargs` و`classpath`:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Replacement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$I2P</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P base installation directory</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$CONFIG</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P configuration directory (typically <code>~/.i2p</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$PLUGIN</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">This plugin's directory (<code>$CONFIG/plugins/name</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$OS</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Operating system: <code>windows</code>, <code>linux</code>, <code>mac</code></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$ARCH</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Architecture: <code>386</code>, <code>amd64</code>, <code>arm64</code></td></tr>
  </tbody>
</table>
### العملاء المُدارون مقابل العملاء غير المُدارين

**العملاء المُدارون (موصى به منذ 0.9.4):** - يتم إنشاء مثيلاتهم بواسطة ClientAppManager (مدير تطبيقات العميل) - يحافظ على المراجع وتتبع الحالة - إدارة دورة الحياة أسهل - إدارة ذاكرة أفضل

**العملاء غير المُدارين:** - يبدأها الـrouter، دون تتبّع للحالة - يجب التعامل بسلاسة مع استدعاءات البدء/الإيقاف المتعددة - استخدم حالة ثابتة أو ملفات PID (معرّف العملية) للتنسيق - يُستدعى عند إيقاف تشغيل الـrouter (اعتباراً من 0.7.12-3)

### ShellService (خدمة سطر الأوامر) (منذ 0.9.53 / 1.7.0)

حل عام لتشغيل البرامج الخارجية مع تتبع الحالة تلقائيًا.

**الميزات:** - يعالج دورة حياة العملية - يتواصل مع ClientAppManager - إدارة تلقائية لمعرّف العملية (PID) - دعم متعدد المنصات

**الاستخدام:**

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myservice.sh
```
بالنسبة إلى البرامج النصية الخاصة بكل منصة:

```properties
clientApp.0.args=$PLUGIN/bin/myservice-$OS.$ARCH
```
**بديل (قديم):** اكتب غلاف Java يتحقق من نوع نظام التشغيل، واستدعِ `ShellCommand` بالملف المناسب `.bat` أو `.sh`.

---

## عملية التثبيت

### سير تثبيت المستخدم

1. يقوم المستخدم بلصق عنوان URL للملحق في صفحة تهيئة ملحقات وحدة تحكم Router (`/configplugins`)
2. يقوم Router بتنزيل ملف الملحق
3. التحقق من التوقيع (يفشل إذا كان المفتاح غير معروف وتم تمكين الوضع الصارم)
4. التحقق من سلامة ملف ZIP
5. استخراج وتحليل `plugin.config`
6. التحقق من توافق الإصدارات (`min-i2p-version`, `min-java-version`, إلخ.)
7. اكتشاف تعارض اسم تطبيق الويب
8. إيقاف الملحق الحالي إذا كان تحديثًا
9. التحقق من صحة الدليل (يجب أن يكون ضمن `plugins/`)
10. استخراج جميع الملفات إلى دليل الملحق
11. تحديث `plugins.config`
12. بدء تشغيل الملحق (ما لم يكن `dont-start-at-install=true`)

### الأمان والثقة

**إدارة المفاتيح:** - نموذج الثقة First-key-seen (القائم على أول مفتاح يتم رؤيته) للموقّعين الجدد - فقط مفاتيح jrandom و zzz مضمّنة مسبقًا - اعتبارًا من 0.9.14.1، يتم رفض المفاتيح غير المعروفة افتراضيًا - يمكن لخاصية متقدمة تجاوز هذا الإعداد لأغراض التطوير

**قيود التثبيت:** - يجب أن تُفك الأرشيفات إلى مجلد الإضافات فقط - يرفض المثبّت المسارات خارج `plugins/` - يمكن للإضافات الوصول إلى ملفات في أماكن أخرى بعد التثبيت - لا يوجد تشغيل ضمن بيئة معزولة (sandboxing) أو عزل للامتيازات

---

## آلية التحديث

### عملية التحقق من التحديث

1. Router يقرأ `updateURL.su3` (المفضّل) أو `updateURL` من plugin.config
2. طلب HTTP HEAD أو GET جزئي لجلب البايتات 41-56
3. استخراج سلسلة الإصدار من الملف البعيد
4. مقارنة مع الإصدار المثبّت باستخدام VersionComparator
5. إذا كان أحدث، فقم بمطالبة المستخدم أو بالتنزيل تلقائيًا (وفقًا للإعدادات)
6. إيقاف الملحق
7. تثبيت التحديث
8. بدء تشغيل الملحق (إلا إذا تغير تفضيل المستخدم)

### مقارنة الإصدارات

تُقسَّم الإصدارات إلى مكوّنات مفصولة بالنقطة/الشرطة/الشرطة السفلية: - `1.2.3` < `1.2.4` - `1.2.3` < `1.2.3-1` - `2.0.0` > `1.9.9`

**أقصى طول:** 16 بايت (يجب أن يتطابق مع رأس SUD/SU3)

### أفضل ممارسات التحديث

1. قم دائماً بزيادة رقم الإصدار عند طرح الإصدارات
2. اختبر مسار التحديث بدءاً من الإصدار السابق
3. ضع في الاعتبار `router-restart-required` للتغييرات الكبرى
4. وفّر كلاً من `updateURL` و`updateURL.su3` أثناء الترحيل
5. استخدم لاحقة رقم البناء للاختبار (`1.2.3-456`)

---

## مسار الأصناف والمكتبات القياسية

### متاح دائمًا في Classpath (مسار تحميل الأصناف في جافا)

ملفات JAR التالية من `$I2P/lib` تكون دائماً ضمن classpath (مسار الفئات) لـ I2P 0.9.30+:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Plugin Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Required for all plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>mstreaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>streaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming implementation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2ptunnel.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP/server plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>router.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Router internals</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed, avoid if possible</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>javax.servlet.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet 3.1, JSP 2.3 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with servlets/JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jasper-runtime.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper compiler/runtime</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>commons-el.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">EL 3.0 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSPs using expression language</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jetty-i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty utilities</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins starting Jetty</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>org.mortbay.jetty.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty 9 base</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Custom Jetty instances</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>sam.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>addressbook.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription/blockfile</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Use NamingService instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>routerconsole.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Not public API, avoid</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jbigi.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Native crypto</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>systray.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">URL launcher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>wrapper.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Service wrapper</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
  </tbody>
</table>
### ملاحظات خاصة

**commons-logging.jar:** - فارغ منذ 0.9.30 - قبل 0.9.30: Apache Tomcat JULI - قبل 0.9.24: Commons Logging + JULI - قبل 0.9: Commons Logging فقط

**jasper-compiler.jar:** - فارغ منذ Jetty 6 (0.9)

**systray4j.jar:** - أزيل في 0.9.26

### غير موجود في Classpath (مسار الأصناف) (يجب تحديده)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jstl.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>standard.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
  </tbody>
</table>
### مواصفة مسار الأصناف

**في clients.config:**

```properties
clientApp.0.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/i2p.jar
```
**في webapps.config:**

```properties
webapps.mywebapp.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/jstl.jar
```
**مهم:** اعتبارًا من الإصدار 0.7.13-3، أصبحت إعدادات classpath (مسار الصفوف في جافا) خاصة بكل thread (خيط تنفيذ)، وليست على مستوى JVM (آلة جافا الافتراضية). حدّد classpath كاملة لكل عميل.

---

## متطلبات إصدار Java

### المتطلبات الحالية (أكتوبر 2025)

**I2P 2.10.0 وما قبله:** - الحد الأدنى: Java 7 (مطلوب منذ 0.9.24، يناير 2016) - الموصى به: Java 8 أو أحدث

**I2P 2.11.0 وما بعده (قادم):** - **الحد الأدنى: Java 17+** (أُعلن عنه في ملاحظات إصدار 2.9.0) - تم تقديم تحذير قبل إصدارين (2.9.0 → 2.10.0 → 2.11.0)

### استراتيجية توافق الإضافات

**لأقصى قدر من التوافق (حتى I2P 2.10.x):**

```xml
<javac source="1.7" target="1.7" />
```
```properties
min-java-version=1.7
```
**بالنسبة إلى ميزات Java 8+:**

```xml
<javac source="1.8" target="1.8" />
```
```properties
min-java-version=1.8
```
**لميزات Java 11+:**

```xml
<javac source="11" target="11" />
```
```properties
min-java-version=11
```
**التحضير لـ 2.11.0+:**

```xml
<javac source="17" target="17" />
```
```properties
min-java-version=17
min-i2p-version=2.11.0
```
### أفضل ممارسات الترجمة البرمجية

**عند الترجمة باستخدام JDK أحدث لاستهداف إصدار أقدم:**

```xml
<javac source="1.7" target="1.7" 
       bootclasspath="${java7.home}/jre/lib/rt.jar"
       includeantruntime="false" />
```
هذا يمنع استخدام واجهات برمجة التطبيقات (APIs) غير المتاحة في إصدار Java المستهدف.

---

## ضغط Pack200 - ملغى

### تحديث هام: لا تستخدم Pack200 (تنسيق ضغط خاص بجافا)

**الحالة:** مُهمَل ومحذوف

أوصت المواصفة الأصلية بشدة باستخدام ضغط Pack200 لتقليل الحجم بنسبة 60-65%. **لم يعد ذلك صالحًا.**

**الجدول الزمني:** - **JEP 336:** تم وسم Pack200 كمهمل في Java 11 (سبتمبر 2018) - **JEP 367:** تمت إزالة Pack200 في Java 14 (مارس 2020)

**تنص مواصفة تحديثات I2P الرسمية:** > "لم تعد ملفات Jar وwar داخل ملف zip تُضغط باستخدام pack200 (آلية ضغط قديمة في Java) كما هو موثّق أعلاه لملفات 'su2'، لأن بيئات تشغيل Java الحديثة لم تعد تدعمه."

**ما الذي يجب فعله:**

1. **أزل pack200 (آلية ضغط JAR قديمة في Java) من عمليات البناء فورًا**
2. **استخدم ضغط ZIP القياسي**
3. **فكّر في بدائل:**
   - ProGuard/R8 (أدوات لتصغير الشيفرة)
   - UPX (أداة لضغط الثنائيات الأصلية)
   - خوارزميات ضغط حديثة (zstd (خوارزمية ضغط عالية الأداء)، brotli (خوارزمية ضغط للويب)) إذا توفّرت أداة فك ضغط مخصصة

**بالنسبة إلى الملحقات الحالية:** - الـ routers القديمة (0.7.11-5 حتى Java 10) لا تزال قادرة على فك ضغط pack200 - الـ routers الجديدة (Java 11+) غير قادرة على فك ضغط pack200 - أعد إصدار الملحقات بدون ضغط pack200

---

## مفاتيح التوقيع والأمان

### توليد المفاتيح (صيغة SU3)

استخدم البرنامج النصي `makeplugin.sh` من مستودع i2p.scripts:

```bash
# Generate new signing key
./makeplugin.sh keygen

# Keys stored in ~/.i2p-plugin-keys/
```
**تفاصيل أساسية:** - الخوارزمية: RSA_SHA512_4096 - التنسيق: شهادة X.509 - التخزين: تنسيق مخزن مفاتيح Java

### توقيع الإضافات

```bash
# Create signed su3 file
./makeplugin.sh sign myplugin.zip myplugin.su3 keyname

# Verify signature
./makeplugin.sh verify myplugin.su3
```
### أفضل ممارسات إدارة المفاتيح

1. **أنشئ مرة واحدة، واحفظها إلى الأبد**
   - Routers ترفض أسماء مفاتيح مكررة مع مفاتيح مختلفة
   - Routers ترفض مفاتيح مكررة مع أسماء مفاتيح مختلفة
   - يتم رفض التحديثات عند عدم تطابق المفتاح/الاسم

2. **التخزين الآمن**
   - أنشئ نسخة احتياطية من مخزن المفاتيح بأمان
   - استخدم عبارة مرور قوية
   - لا تُدرجها مطلقًا في نظام التحكم بالإصدارات

3. **تدوير المفاتيح**
   - غير مدعوم من قبل البنية المعمارية الحالية
   - خطط لاستخدام المفاتيح على المدى الطويل
   - ضع في الاعتبار مخططات التوقيع المتعدد لتطوير الفرق

### توقيع DSA القديم (XPI2P)

**الحالة:** يعمل ولكنه متقادم

تواقيع DSA-1024 المستخدمة في صيغة xpi2p:
- توقيع بطول 40 بايت
- مفتاح عام بطول 172 حرفًا بترميز base64
- توصي NIST-800-57 بحد أدنى (L=2048, N=224)
- تستخدم I2P معلمات أضعف (L=1024, N=160)

**التوصية:** استخدم SU3 (تنسيق تحديث موقّع في I2P) مع RSA-4096 بدلًا من ذلك.

---

## إرشادات تطوير الملحقات

### أفضل الممارسات الأساسية

1. **التوثيق**
   - وفّر ملف README (ملف التعليمات) واضحاً مع تعليمات التثبيت
   - وثّق خيارات التهيئة والقيم الافتراضية
   - أدرج سجل التغييرات مع كل إصدار
   - حدّد إصدارات I2P/Java المطلوبة

2. **تحسين الحجم**
   - ضمّن الملفات الضرورية فقط
   - لا تقم مطلقًا بتجميع ملفات JAR الخاصة بالـ router
   - افصل حزم التثبيت عن حزم التحديث (المكتبات في lib/)
   - ~~استخدم ضغط Pack200~~ **مهمل - استخدم ZIP القياسي**

3. **التهيئة**
   - لا تقم أبدًا بتعديل `plugin.config` أثناء وقت التشغيل
   - استخدم ملف إعدادات منفصلًا لإعدادات وقت التشغيل
   - وثّق إعدادات router المطلوبة (منافذ SAM، tunnels، إلخ)
   - احترم إعدادات المستخدم القائمة

4. **استخدام الموارد**
   - تجنّب الاستهلاك الافتراضي المفرط لعرض النطاق الترددي
   - طبّق حدوداً معقولة لاستخدام وحدة المعالجة المركزية (CPU)
   - نظّف الموارد عند إيقاف التشغيل
   - استخدم daemon threads (خيوط تعمل في الخلفية وتنتهي تلقائياً عند انتهاء التطبيق) حيثما كان ذلك مناسباً

5. **الاختبار**
   - اختبر التثبيت/الترقية/إلغاء التثبيت على جميع المنصات
   - اختبر التحديثات من الإصدار السابق
   - تحقق من توقف/إعادة تشغيل تطبيق الويب أثناء التحديثات
   - اختبر باستخدام الحد الأدنى للإصدار المدعوم من I2P

6. **نظام الملفات**
   - لا تكتب مطلقًا إلى `$I2P` (قد يكون للقراءة فقط)
   - اكتب بيانات وقت التشغيل إلى `$PLUGIN` أو `$CONFIG`
   - استخدم `I2PAppContext` لاكتشاف الدلائل
   - لا تفترض موقع `$CWD`

7. **التوافق**
   - لا تكرر فئات I2P القياسية
   - قم بتمديد الفئات إذا لزم الأمر، لا تستبدلها
   - تحقّق من `min-i2p-version`، `min-jetty-version` في plugin.config
   - اختبر مع إصدارات I2P الأقدم إذا كنت تدعمها

8. **التعامل مع إيقاف التشغيل**
   - اضبط `stopargs` بشكل صحيح في clients.config
   - سجّل خطافات إيقاف التشغيل: `I2PAppContext.addShutdownTask()`
   - تعامل بسلاسة مع استدعاءات البدء/الإيقاف المتعددة
   - اضبط جميع سلاسل التنفيذ على وضع daemon (خدمة تعمل في الخلفية)

9. **الأمان**
   - تحقق من صحة كل المدخلات الخارجية
   - لا تستدعِ `System.exit()`
   - احترم خصوصية المستخدم
   - اتبع ممارسات البرمجة الآمنة

10. **الترخيص**
    - حدّد رخصة الملحق بوضوح
    - احترم تراخيص المكتبات المضمّنة
    - ضمّن الإسناد المطلوب
    - وفّر الوصول إلى الشيفرة المصدرية إذا كان ذلك مطلوبًا

### اعتبارات متقدمة

**التعامل مع المنطقة الزمنية:** - يقوم Router بضبط المنطقة الزمنية لـ JVM إلى UTC - المنطقة الزمنية الفعلية للمستخدم: `I2PAppContext` خاصية `i2p.systemTimeZone`

**اكتشاف الدليل:**

```java
// Plugin directory
String pluginDir = I2PAppContext.getGlobalContext()
    .getAppDir().getAbsolutePath() + "/plugins/" + pluginName;

// Or use $PLUGIN variable in clients.config args
```
**ترقيم الإصدارات:** - استخدم الترقيم الدلالي (major.minor.patch) - أضف رقم البناء لأغراض الاختبار (1.2.3-456) - تأكد من أن الأرقام تزداد دائمًا ولا تتراجع بين التحديثات

**الوصول إلى صنف Router:** - يُفضَّل عموماً تجنّب التبعيات على `router.jar` - استخدم واجهات برمجة التطبيقات العامة في `i2p.jar` بدلاً من ذلك - قد يقيّد I2P مستقبلاً الوصول إلى صنف Router

**منع تعطل JVM (تاريخيًا):** - تم الإصلاح في 0.7.13-3 - استخدم محمِّلات الأصناف بشكل صحيح - تجنّب تحديث JARs (ملفات أرشيف جافا) في مُلحق قيد التشغيل - صمِّم بحيث تتم إعادة التشغيل عند التحديث إذا لزم الأمر

---

## ملحقات Eepsite

### نظرة عامة

يمكن للملحقات توفير eepsites كاملة مع مثيلات Jetty و I2PTunnel الخاصة بها.

### المعمارية

**لا تحاول القيام بما يلي:** - تثبيت في eepsite موجود مسبقًا - دمج مع eepsite الافتراضي الخاص بـ router - افتراض توفر eepsite واحد فقط

**بدلاً من ذلك:** - ابدأ مثيلاً جديداً لـ I2PTunnel (عبر أسلوب CLI (سطر الأوامر)) - ابدأ مثيلاً جديداً لـ Jetty - قم بتهيئة كليهما في `clients.config`

### هيكلية المثال

```
plugins/myeepsite/
├── plugin.config
├── clients.config          # Starts Jetty + I2PTunnel
├── eepsite/
│   ├── jetty.xml          # Requires variable substitution
│   ├── docroot/
│   ├── webapps/
│   └── logs/
└── lib/
    └── [dependencies]
```
### استبدال المتغيرات في jetty.xml

استخدم المتغير `$PLUGIN` للمسارات:

```xml
<Set name="resourceBase">$PLUGIN/eepsite/docroot</Set>
```
يقوم Router بالاستبدال أثناء بدء تشغيل المكوّن الإضافي.

### أمثلة

التنفيذات المرجعية: - **إضافة zzzot** - متعقّب تورنت - **إضافة pebble** - منصّة تدوين

كلاهما متاحان في صفحة الملحقات الخاصة بـ zzz (I2P-internal).

---

## تكامل وحدة التحكم

### روابط شريط الملخص

إضافة رابط قابل للنقر إلى شريط الملخص في لوحة تحكم router:

```properties
consoleLinkName=My Plugin
consoleLinkURL=/myplugin/
consoleLinkTooltip=Open My Plugin Interface
```
الإصدارات المحلية:

```properties
consoleLinkName_de=Mein Plugin
consoleLinkTooltip_de=Öffne Mein Plugin Schnittstelle
```
### أيقونات وحدة التحكم

**ملف صورة (منذ 0.9.20):**

```properties
console-icon=/myicon.png
```
مسار نسبي إلى `consoleLinkURL` إذا تم تحديده (اعتباراً من 0.9.53)، وإلا فنسبي إلى اسم تطبيق الويب.

**أيقونة مضمّنة (منذ 0.9.25):**

```properties
icon-code=iVBORw0KGgoAAAANSUhEUgAAA...Base64EncodedPNG...
```
ولّد باستخدام:

```bash
base64 -w 0 icon-32x32.png
```
أو Java:

```bash
java -cp i2p.jar net.i2p.data.Base64 encode icon.png
```
المتطلبات: - 32x32 بكسل - بصيغة PNG - بترميز Base64 (من دون فواصل أسطر)

---

## التدويل

### حزم الترجمة

**بالنسبة إلى ترجمات I2P الأساسية:** - ضع ملفات JAR في `console/locale/` - تحتوي على حزم الموارد لتطبيقات I2P الحالية - التسمية: `messages_xx.properties` (xx = رمز اللغة)

**لترجمات خاصة بالمكوّنات الإضافية:** - ضمّن في `console/webapps/*.war` - أو ضمّن في `lib/*.jar` - استخدم نهج Java ResourceBundle (حزمة الموارد في جافا) القياسي

### السلاسل النصية المترجمة في plugin.config

```properties
description=My awesome plugin
description_de=Mein tolles Plugin
description_fr=Mon plugin génial
description_es=Mi plugin increíble
```
الحقول المدعومة: - `description_xx` - `consoleLinkName_xx` - `consoleLinkTooltip_xx`

### ترجمة سمة وحدة التحكم

السمات الموجودة في `console/themes/` تُضاف تلقائيًا إلى مسار بحث السمات.

---

## ملحقات خاصة بالمنصة

### نهج الحزم المنفصلة

استخدم أسماء ملحقات مختلفة لكل منصة:

```properties
# Windows package
name=myplugin-windows

# Linux package  
name=myplugin-linux

# macOS package
name=myplugin-mac
```
### نهج استبدال المتغيرات

ملف plugin.config واحد مع متغيرات المنصة:

```properties
name=myplugin
updateURL.su3=http://myplugin.i2p/downloads/myplugin-$OS-$ARCH.su3
```
في clients.config:

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myapp-$OS-$ARCH
```
### اكتشاف نظام التشغيل وقت التشغيل

مقاربة Java للتنفيذ الشرطي:

```java
String os = System.getProperty("os.name").toLowerCase();
if (os.contains("win")) {
    // Windows-specific code
} else if (os.contains("nix") || os.contains("nux")) {
    // Linux-specific code
} else if (os.contains("mac")) {
    // macOS-specific code
}
```
---

## استكشاف الأخطاء وإصلاحها

### المشكلات الشائعة

**الإضافة لا تبدأ:** 1. تحقق من توافق إصدار I2P (`min-i2p-version`) 2. تحقق من إصدار Java (`min-java-version`) 3. تحقق من سجلات router بحثًا عن الأخطاء 4. تحقق من توفّر جميع ملفات JAR المطلوبة في مسار الأصناف (classpath)

**تطبيق الويب غير قابل للوصول:** 1. أكّد أن `webapps.config` لا يعطّله 2. تحقّق من توافق إصدار Jetty (`min-jetty-version`) 3. تحقّق من أن `web.xml` موجود (لا يُدعَم فحص التعليقات التوضيحية) 4. تحقّق من وجود تعارض في أسماء تطبيقات الويب

**فشل التحديث:** 1. تحقّق من أن سلسلة الإصدار قد زادت 2. تحقّق من أن التوقيع يطابق مفتاح التوقيع 3. تأكّد من أن اسم المكوّن الإضافي يطابق الإصدار المثبّت 4. راجع إعدادات `update-only`/`install-only`

**البرنامج الخارجي لا يتوقف:** 1. استخدم ShellService لإدارة دورة الحياة تلقائيًا 2. نفذ معالجة صحيحة لـ`stopargs` 3. تحقق من تنظيف ملف PID 4. تأكد من إنهاء العملية

### تسجيل التصحيح

تمكين تسجيل التصحيح في router:

```
logger.record.net.i2p.router.web.ConfigPluginsHandler=DEBUG
```
تحقق من السجلات:

```
~/.i2p/logs/log-router-0.txt
```
---

## معلومات مرجعية

### المواصفات الرسمية

- [مواصفات الإضافة](/docs/specs/plugin/)
- [تنسيق التهيئة](/docs/specs/configuration/)
- [مواصفات التحديث](/docs/specs/updates/)
- [التشفير](/docs/specs/cryptography/)

### سجل إصدارات I2P

**الإصدار الحالي:** - **I2P 2.10.0** (8 سبتمبر 2025)

**الإصدارات الرئيسية منذ 0.9.53:** - 2.10.0 (سبتمبر 2025) - إعلان بشأن Java 17+ - 2.9.0 (يونيو 2025) - تحذير بشأن Java 17+ - 2.8.0 (أكتوبر 2024) - اختبار التشفير ما بعد الكمّ - 2.6.0 (مايو 2024) - حظر I2P-over-Tor - 2.4.0 (ديسمبر 2023) - تحسينات أمنية في NetDB - 2.2.0 (مارس 2023) - التحكم في الازدحام - 2.1.0 (يناير 2023) - تحسينات الشبكة - 2.0.0 (نوفمبر 2022) - بروتوكول نقل SSU2 - 1.7.0/0.9.53 (فبراير 2022) - ShellService, استبدال المتغيرات - 0.9.15 (سبتمبر 2014) - تم تقديم تنسيق SU3

**ترقيم الإصدارات:** - سلسلة 0.9.x: حتى الإصدار 0.9.53 - سلسلة 2.x: بدءًا من 2.0.0 (تقديم SSU2)

### موارد المطورين

**الشيفرة المصدرية:** - المستودع الرئيسي: https://i2pgit.org/I2P_Developers/i2p.i2p - مرآة GitHub: https://github.com/i2p/i2p.i2p

**أمثلة على الإضافات:** - zzzot (متعقب BitTorrent) - pebble (منصة تدوين) - i2p-bote (بريد إلكتروني دون خوادم) - orchid (عميل Tor) - seedless (تبادل الأقران)

**أدوات البناء:** - makeplugin.sh - توليد المفاتيح والتوقيع - موجود في مستودع i2p.scripts - يؤتمت إنشاء su3 (صيغة حزمة موقعة خاصة بـ I2P) والتحقق منها

### دعم المجتمع

**المنتديات:** - [منتدى I2P](https://i2pforum.net/) - [zzz.i2p](http://zzz.i2p/) (متاح داخل I2P فقط)

**IRC/الدردشة:** - #i2p-dev على OFTC - I2P IRC داخل الشبكة

---

## الملحق أ: مثال كامل لملف plugin.config

```properties
# Required fields
name=example-plugin
signer=developer@mail.i2p
version=1.2.3

# Update configuration
updateURL.su3=http://example.i2p/plugins/example-$OS-$ARCH.su3
min-i2p-version=2.0.0
min-java-version=17

# Display information
date=1698796800000
author=Example Developer <developer@mail.i2p>
websiteURL=http://example.i2p/
license=Apache-2.0

description=An example I2P plugin demonstrating best practices
description_de=Ein Beispiel-I2P-Plugin zur Demonstration bewährter Praktiken
description_es=Un plugin I2P de ejemplo que demuestra las mejores prácticas

# Console integration
consoleLinkName=Example Plugin
consoleLinkName_de=Beispiel-Plugin
consoleLinkURL=/example/
consoleLinkTooltip=Open the Example Plugin control panel
consoleLinkTooltip_de=Öffne das Beispiel-Plugin-Kontrollfeld
console-icon=/icon.png

# Installation behavior
dont-start-at-install=false
router-restart-required=false

# Platform requirements (informational)
required-platform-OS=All platforms supported
other-requirements=Requires 512MB free disk space
```
---

## الملحق ب: مثال كامل لملف clients.config

```properties
# Main service client (managed)
clientApp.0.main=com.example.plugin.MainService
clientApp.0.name=Example Plugin Main Service
clientApp.0.delay=30
clientApp.0.args=$PLUGIN/config.properties --port=7656
clientApp.0.stopargs=shutdown
clientApp.0.uninstallargs=cleanup
clientApp.0.classpath=$PLUGIN/lib/example.jar,$I2P/lib/i2p.jar,$I2P/lib/mstreaming.jar

# External program via ShellService
clientApp.1.main=net.i2p.apps.ShellService
clientApp.1.name=Example Native Helper
clientApp.1.delay=35
clientApp.1.args=$PLUGIN/bin/helper-$OS-$ARCH --config $PLUGIN/helper.conf
clientApp.1.classpath=$I2P/lib/i2p.jar

# Jetty eepsite
clientApp.2.main=net.i2p.jetty.JettyStart
clientApp.2.name=Example Eepsite
clientApp.2.delay=40
clientApp.2.args=$PLUGIN/eepsite/jetty.xml
clientApp.2.stopargs=$PLUGIN/eepsite/jetty.xml stop
clientApp.2.classpath=$PLUGIN/lib/example-web.jar,$I2P/lib/i2p.jar

# I2PTunnel for eepsite
clientApp.3.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.3.name=Example Eepsite Tunnel
clientApp.3.delay=45
clientApp.3.args=$PLUGIN/eepsite/i2ptunnel.config
```
---

## الملحق C: مثال كامل لملف webapps.config

```properties
# Disable autostart for admin webapp
webapps.example-admin.startOnLoad=false

# Main webapp with classpath
webapps.example.startOnLoad=true
webapps.example.classpath=$PLUGIN/lib/example-core.jar,$PLUGIN/lib/commons-utils.jar,$I2P/lib/jstl.jar,$I2P/lib/standard.jar

# Legacy support (pre-0.7.12-9)
plugin.example.startOnLoad=true
```
---

## الملحق د: قائمة التحقق من الترحيل (0.9.53 إلى 2.10.0)

### التغييرات المطلوبة

- [ ] **إزالة ضغط Pack200 (تنسيق ضغط لملفات JAR في Java) من عملية البناء**
  - إزالة مهام pack200 من البرامج النصية لـ Ant/Maven/Gradle
  - إعادة إصدار المكونات الإضافية الحالية بدون pack200

- [ ] **مراجعة متطلبات إصدار جافا**
  - النظر في اشتراط جافا 11+ للميزات الجديدة
  - التخطيط لاشتراط جافا 17+ في I2P 2.11.0
  - تحديث `min-java-version` في plugin.config

- [ ] **تحديث الوثائق**
  - إزالة مراجع Pack200
  - تحديث متطلبات إصدار Java
  - تحديث مراجع إصدارات I2P (0.9.x → 2.x)

### التغييرات الموصى بها

- [ ] **عزّز التواقيع الرقمية**
  - انقل من XPI2P (صيغة إضافات قديمة في I2P) إلى SU3 (تنسيق تحديثات موقّع في I2P) إذا لم يتم ذلك بالفعل
  - استخدم مفاتيح RSA-4096 للإضافات الجديدة

- [ ] **الاستفادة من الميزات الجديدة (إذا كنت تستخدم 0.9.53+)**
  - استخدم متغيرات `$OS` / `$ARCH` للتحديثات المخصّصة للمنصة
  - استخدم ShellService (خدمة سطر الأوامر) للبرامج الخارجية
  - استخدم مسار classpath المحسّن لتطبيقات الويب (يعمل مع أي اسم WAR)

- [ ] **اختبار التوافق**
  - اختبر على I2P 2.10.0
  - تحقق باستخدام Java 8، 11، 17
  - تحقق على Windows وLinux وmacOS

### تحسينات اختيارية

- [ ] تنفيذ ServletContextListener بالشكل الصحيح (مستمع سياق Servlets في Java)
- [ ] إضافة أوصاف مُحلية
- [ ] توفير أيقونة لوحدة التحكم
- [ ] تحسين معالجة إيقاف التشغيل
- [ ] إضافة تسجيل شامل
- [ ] كتابة اختبارات مؤتمتة
