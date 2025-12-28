---
title: "إعدادات Router"
description: "خيارات الإعداد والتنسيقات الخاصة بـ I2P routers والعملاء"
slug: "configuration"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## نظرة عامة

يوفّر هذا المستند مواصفة تقنية شاملة لملفات تهيئة I2P المستخدمة بواسطة router وتطبيقات متعددة. ويغطي مواصفات تنسيق الملفات، وتعريفات الخصائص، وتفاصيل التنفيذ التي جرى التحقق منها بمقارنتها مع الشفرة المصدرية لـ I2P والوثائق الرسمية.

### النطاق

- ملفات إعداد Router وتنسيقاتها
- إعدادات تطبيقات العميل
- إعدادات I2PTunnel tunnel
- مواصفات تنسيقات الملفات والتنفيذ
- ميزات خاصة بالإصدار والميزات المهملة

### ملاحظات التنفيذ

تُقرأ وتُكتب ملفات التهيئة باستخدام أسلوبي `DataHelper.loadProps()` و`storeProps()` في مكتبة I2P الأساسية. يختلف تنسيق الملف اختلافًا كبيرًا عن التنسيق المسلسل المستخدم في بروتوكولات I2P (انظر [مواصفة البنى العامة - تعيين الأنواع](/docs/specs/common-structures/#type-mapping)).

---

## التنسيق العام لملف الإعدادات

تتبع ملفات تهيئة I2P صيغة خصائص Java المعدّلة، مع استثناءات وقيود محددة.

### مواصفات التنسيق

استنادًا إلى [Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) (خصائص Java) مع الفروق الجوهرية التالية:

#### الترميز

- **يجب** استخدام ترميز UTF-8 (وليس ISO-8859-1 كما في خصائص Java القياسية)
- التنفيذ: يستخدم دوال `DataHelper.getUTF8()` المساعدة لجميع عمليات الملفات

#### تسلسلات الهروب

- **لا** يتم التعرف على أي تسلسلات هروب (بما في ذلك الشرطة المائلة العكسية `\`)
- استمرار السطر **غير** مدعوم
- تُعامل أحرف الشرطة المائلة العكسية كأحرف حرفية

#### محارف التعليق

- يبدأ `#` تعليقًا في أي موضع على السطر
- يبدأ `;` تعليقًا **فقط** عندما يكون في العمود 1 (أي في بداية السطر)
- `!` **لا** يبدأ تعليقًا (يختلف عن Java Properties)

#### فواصل المفتاح والقيمة

- `=` هو الفاصل **الوحيد** المعتمد بين المفتاح والقيمة
- `:` **غير** معترف به كفاصل
- المسافات البيضاء **غير** معترف بها كفاصل

#### التعامل مع المسافات البيضاء

- المسافات البيضاء في البداية والنهاية **لا** تُزال من المفاتيح
- المسافات البيضاء في البداية والنهاية **تُزال** من القيم

#### معالجة الأسطر

- يتم تجاهل الأسطر التي لا تحتوي على `=` (تُعامل كتعليقات أو أسطر فارغة)
- القيم الفارغة (`key=`) مدعومة ابتداءً من الإصدار 0.9.10
- تُخزَّن المفاتيح ذات القيم الفارغة وتُسترجع بشكل طبيعي

#### قيود الأحرف

**يجب ألّا تحتوي المفاتيح على**: - `#` (علامة الشباك/علامة الباوند) - `=` (علامة يساوي) - `\n` (محرف سطر جديد) - لا يمكن أن تبدأ بـ `;` (فاصلة منقوطة)

**لا يجوز أن تحتوي القيم على**: - `#` (علامة الهاش/الشباك) - `\n` (محرف سطر جديد) - لا يمكن أن تبدأ أو تنتهي بـ `\r` (محرف إرجاع العربة) - لا يمكن أن تبدأ أو تنتهي بمحارف بيضاء (تُزال تلقائيًا)

### فرز الملفات

لا يشترط ترتيب ملفات الإعداد حسب المفتاح. ومع ذلك، تقوم معظم تطبيقات I2P بترتيب المفاتيح أبجديًا عند كتابة ملفات الإعداد لتسهيل: - التحرير اليدوي - عمليات diff (المقارنة) في أنظمة التحكم في الإصدارات - قابلية القراءة البشرية

### تفاصيل التنفيذ

#### قراءة ملفات الإعداد

```java
// Method signature from net.i2p.data.DataHelper
public static Properties loadProps(File file)
```
**السلوك**: - يقرأ ملفات مُرمَّزة بترميز UTF-8 - يفرض جميع قواعد التنسيق الموضَّحة أعلاه - يتحقق من قيود الأحرف - يُرجِع كائن Properties فارغًا إذا كان الملف غير موجودًا - يرمي `IOException` عند أخطاء القراءة

#### كتابة ملفات الإعداد

```java
// Method signature from net.i2p.data.DataHelper
public static void storeProps(Properties props, File file)
```
**السلوك**: - يكتب ملفات مُرمّزة بترميز UTF-8 - يرتّب المفاتيح أبجديًا (ما لم تُستخدم OrderedProperties (فئة تُحافظ على ترتيب الخصائص)) - يضبط أذونات الملف إلى الوضع 600 (قراءة/كتابة للمستخدم فقط) اعتبارًا من الإصدار 0.8.1 - يرمي `IllegalArgumentException` عند وجود أحرف غير صالحة في المفاتيح أو القيم - يرمي `IOException` عند أخطاء الكتابة

#### التحقق من صحة التنسيق

يُجري التنفيذ تحققًا صارمًا: - يتم فحص المفاتيح والقيم بحثًا عن أحرف محظورة - تؤدي الإدخالات غير الصالحة إلى طرح استثناءات أثناء عمليات الكتابة - تتجاهل القراءة بصمت الأسطر غير السليمة (الأسطر التي لا تحتوي على `=`)

### أمثلة التنسيق

#### ملف ضبط صالح

```properties
# This is a comment
; This is also a comment (column 1 only)
key.with.dots=value with spaces
another_key=value=with=equals
empty.value=
numeric.value=12345
unicode.value=こんにちは
```
#### أمثلة على تكوينات غير صالحة

```properties
# INVALID: Key contains equals sign
invalid=key=value

# INVALID: Key contains hash
invalid#key=value

# INVALID: Value contains newline (implicit)
key=value
continues here

# INVALID: Semicolon comment not in column 1 (treated as key)
 ; not.a.comment=value
```
---

## المكتبة الأساسية وإعدادات Router

### إعدادات العملاء (clients.config)

**الموقع**: `$I2P_CONFIG_DIR/clients.config` (قديمة) أو `$I2P_CONFIG_DIR/clients.config.d/` (حديثة)   **واجهة الإعداد**: وحدة تحكم Router في `/configclients`   **تغيير التنسيق**: الإصدار 0.9.42 (أغسطس 2019)

#### بنية المجلدات (الإصدار 0.9.42+)

اعتباراً من الإصدار 0.9.42، يُقسَّم ملف clients.config الافتراضي تلقائياً إلى ملفات تهيئة مستقلة:

```
$I2P_CONFIG_DIR/
├── clients.config.d/
│   ├── 00-webConsole.config
│   ├── 01-i2ptunnel.config
│   ├── 02-i2psnark.config
│   ├── 03-susidns.config
│   └── ...
└── clients.config (legacy, auto-migrated)
```
**سلوك الترحيل**: - عند التشغيل لأول مرة بعد الترقية إلى 0.9.42+، يتم تقسيم الملف الأحادي تلقائيًا - الخصائص في الملفات المُقسَّمة تُسبَق بـ `clientApp.0.` - لا يزال التنسيق القديم مدعومًا للتوافق العكسي - يُمكّن التنسيق المُقسَّم التغليف المعياري وإدارة الإضافات

#### تنسيق الخاصية

تكون الأسطر بالشكل `clientApp.x.prop=val`، حيث إن `x` هو رقم التطبيق.

**متطلبات ترقيم التطبيق**: - يجب أن يبدأ بـ 0 - يجب أن يكون متسلسلاً (من دون فجوات) - الترتيب يحدد تسلسل بدء التشغيل

#### الخصائص المطلوبة

##### رئيسي

- **النوع**: String (اسم فئة مؤهَّل بالكامل)
- **مطلوب**: نعم
- **الوصف**: سيتم استدعاء المنشئ أو الطريقة `main()` في هذه الفئة اعتمادًا على نوع العميل (مُدار مقابل غير مُدار)
- **مثال**: `clientApp.0.main=net.i2p.router.web.RouterConsoleRunner`

#### خصائص اختيارية

##### الاسم

- **النوع**: سلسلة نصية
- **إلزامي**: لا
- **الوصف**: الاسم المعروض في لوحة تحكم router
- **مثال**: `clientApp.0.name=Router Console`

##### args

- **النوع**: سلسلة نصية (مفصولة بمسافة أو محرف جدولة)
- **مطلوب**: لا
- **الوصف**: الوسيطات المُمرَّرة إلى باني الفئة الرئيسية أو إلى الدالة main()
- **الاقتباس**: يمكن وضع الوسيطات التي تحتوي على مسافات أو محارف جدولة بين علامتي اقتباس ' أو "
- **مثال**: `clientApp.0.args=-d $CONFIG/eepsite`

##### تأخير

- **النوع**: عدد صحيح (ثوانٍ)
- **مطلوب**: لا
- **الافتراضي**: 120
- **الوصف**: عدد الثواني المراد انتظارها قبل بدء تشغيل العميل
- **التجاوزات**: يتم تجاوزه بواسطة `onBoot=true` (يضبط التأخير على 0)
- **القيم الخاصة**:
  - `< 0`: انتظر حتى يصل الـ router إلى حالة RUNNING، ثم ابدأ فورًا في خيط (thread) جديد
  - `= 0`: شغّل فورًا في الخيط نفسه (تنتقل الاستثناءات إلى وحدة التحكم)
  - `> 0`: ابدأ بعد تأخير في خيط جديد (تُسجَّل الاستثناءات ولا تُمرَّر)

##### onBoot

- **النوع**: Boolean
- **مطلوب**: لا
- **الافتراضي**: false
- **الوصف**: يفرض تأخيرًا مقداره 0، ويتجاوز إعداد التأخير المحدّد صراحةً
- **حالة الاستخدام**: بدء الخدمات الحرجة على الفور عند إقلاع router

##### startOnLoad

- **النوع**: قيمة منطقية
- **مطلوب**: لا
- **القيمة الافتراضية**: true
- **الوصف**: ما إذا كان يجب بدء تشغيل العميل على الإطلاق
- **حالة الاستخدام**: تعطيل العملاء دون إزالة التكوين

#### خصائص خاصة بالمكوّن الإضافي

هذه الخصائص تُستخدم فقط بواسطة الإضافات (وليس العملاء الأساسيين):

##### stopargs

- **النوع**: سلسلة نصية (مفصولة بمسافة أو علامة تبويب)
- **الوصف**: الوسائط الممررة لإيقاف العميل
- **استبدال المتغيرات**: نعم (انظر أدناه)

##### uninstallargs

- **النوع**: سلسلة نصية (مفصولة بمسافة أو محرف جدولة)
- **الوصف**: المعاملات المُمرَّرة لإلغاء تثبيت العميل
- **استبدال المتغيرات**: نعم (انظر أدناه)

##### مسار الأصناف

- **النوع**: سلسلة نصية (مسارات مفصولة بفواصل)
- **الوصف**: عناصر مسار الأصناف (classpath) الإضافية للعميل
- **استبدال المتغيرات**: نعم (انظر أدناه)

#### استبدال المتغيرات (للمكونات الإضافية فقط)

يتم استبدال المتغيّرات التالية في `args` و`stopargs` و`uninstallargs` و`classpath` للملحقات:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P installation directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>/usr/share/i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User configuration directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p/plugins/foo</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$OS</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Operating system name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>linux</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$ARCH</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Architecture name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>amd64</code></td>
    </tr>
  </tbody>
</table>
**ملاحظة**: يُجرى استبدال المتغيرات فقط للإضافات، وليس للعملاء الأساسيين.

#### أنواع العملاء

##### العملاء المُدارون

- يتم استدعاء المُنشئ مع معاملي `RouterContext` و`ClientAppManager`
- يجب على العميل تنفيذ واجهة `ClientApp`
- يتم التحكم في دورة الحياة بواسطة router
- يمكن بدء تشغيله وإيقافه وإعادة تشغيله بشكل ديناميكي

##### عملاء غير مُدارين

- يتم استدعاء الطريقة `main(String[] args)`
- يتم تشغيله في خيط منفصل
- دورة الحياة لا تُدار بواسطة router
- نوع عميل قديم

#### مثال على التكوين

```properties
# Router Console (core client)
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=-d $CONFIG/eepsite
clientApp.0.delay=0
clientApp.0.onBoot=true
clientApp.0.startOnLoad=true

# I2PTunnel (core client)
clientApp.1.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.1.name=I2PTunnel
clientApp.1.args=
clientApp.1.delay=120
clientApp.1.startOnLoad=true

# Plugin Example
clientApp.2.main=org.example.plugin.PluginMain
clientApp.2.name=Example Plugin
clientApp.2.args=-config $PLUGIN/config.properties
clientApp.2.stopargs=-shutdown
clientApp.2.uninstallargs=-remove $PLUGIN
clientApp.2.classpath=$PLUGIN/lib/plugin.jar,$PLUGIN/lib/dep.jar
clientApp.2.delay=240
clientApp.2.startOnLoad=true
```
---

### تكوين المسجل (logger.config)

**الموقع**: `$I2P_CONFIG_DIR/logger.config`   **واجهة التهيئة**: وحدة تحكم Router عند `/configlogging`

#### مرجع الخصائص

##### إعدادات المخزن المؤقت لوحدة التحكم

###### logger.consoleBufferSize

- **النوع**: عدد صحيح
- **القيمة الافتراضية**: 20
- **الوصف**: العدد الأقصى لرسائل السجل المراد تخزينها مؤقتًا في وحدة التحكم
- **النطاق**: 1-1000 مُوصى به

##### تنسيق التاريخ والوقت

###### logger.dateFormat

- **النوع**: String (نمط SimpleDateFormat)
- **القيمة الافتراضية**: من الإعدادات المحلية للنظام
- **مثال**: `HH:mm:ss.SSS`
- **التوثيق**: [Java SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)

##### مستويات السجل

###### logger.defaultLevel

- **النوع**: تعداد
- **القيمة الافتراضية**: ERROR
- **القيم**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **الوصف**: مستوى التسجيل الافتراضي لجميع الأصناف

###### logger.minimumOnScreenLevel

- **النوع**: Enum
- **القيمة الافتراضية**: CRIT
- **القيم**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **الوصف**: أدنى مستوى للرسائل المعروضة على الشاشة

###### logger.record.{class}

- **النوع**: تعداد
- **القيم**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **الوصف**: تجاوز مستوى التسجيل لكل فئة
- **مثال**: `logger.record.net.i2p.router.transport.udp=DEBUG`

##### خيارات العرض

###### logger.displayOnScreen

- **النوع**: منطقي
- **القيمة الافتراضية**: true
- **الوصف**: ما إذا كان يجب عرض رسائل السجل في إخراج وحدة التحكم

###### logger.dropDuplicates

- **النوع**: منطقي
- **القيمة الافتراضية**: true
- **الوصف**: تجاهل رسائل السجل المتكررة المتتالية

###### logger.dropOnOverflow

- **النوع**: منطقي
- **الافتراضي**: false
- **الوصف**: إسقاط الرسائل عند امتلاء المخزن المؤقت (بدلاً من الحظر (blocking))

##### سلوك التفريغ

###### logger.flushInterval

- **النوع**: عدد صحيح (ثوانٍ)
- **القيمة الافتراضية**: 29
- **منذ**: الإصدار 0.9.18
- **الوصف**: مدى تكرار تفريغ المخزن المؤقت للسجل إلى القرص

##### إعدادات التنسيق

###### logger.format

- **النوع**: سلسلة (تسلسل محارف)
- **الوصف**: قالب تنسيق رسالة السجل
- **أحرف التنسيق**:
  - `d` = التاريخ/الوقت
  - `c` = اسم الصنف
  - `t` = اسم الخيط
  - `p` = الأولوية (مستوى السجل)
  - `m` = الرسالة
- **مثال**: `dctpm` ينتج `[الطابع الزمني] [الصنف] [الخيط] [المستوى] الرسالة`

##### الضغط (الإصدار 0.9.56+)

###### logger.gzip

- **النوع**: منطقي
- **القيمة الافتراضية**: false
- **منذ**: الإصدار 0.9.56
- **الوصف**: تمكين ضغط gzip لملفات السجل المدوّرة

###### logger.minGzipSize

- **النوع**: عدد صحيح (بايت)
- **القيمة الافتراضية**: 65536
- **منذ**: الإصدار 0.9.56
- **الوصف**: الحد الأدنى لحجم الملف لتفعيل الضغط (افتراضيًا 64 كيلوبايت)

##### إدارة الملفات

###### logger.logBufferSize

- **النوع**: عدد صحيح (بايتات)
- **القيمة الافتراضية**: 1024
- **الوصف**: أقصى عدد من الرسائل لتخزينها مؤقتًا قبل التفريغ

###### logger.logFileName

- **النوع**: سلسلة نصية (مسار ملف)
- **القيمة الافتراضية**: `logs/log-@.txt`
- **الوصف**: نمط تسمية ملف السجل (`@` يتم استبداله برقم التدوير)

###### logger.logFilenameOverride

- **النوع**: سلسلة (مسار ملف)
- **الوصف**: تجاوز لاسم ملف السجل (يعطل نمط تدوير السجلات)

###### logger.logFileSize

- **النوع**: سلسلة نصية (حجم بوحدة قياس)
- **القيمة الافتراضية**: 10M
- **الوحدات**: K (كيلوبايت)، M (ميجابايت)، G (جيجابايت)
- **مثال**: `50M`، `1G`

###### logger.logRotationLimit

- **النوع**: عدد صحيح
- **القيمة الافتراضية**: 2
- **الوصف**: أعلى رقم لملف تدوير السجل (log-0.txt إلى log-N.txt)

#### تكوين نموذجي

```properties
# Basic logging configuration
logger.consoleBufferSize=50
logger.dateFormat=yyyy-MM-dd HH:mm:ss.SSS
logger.defaultLevel=WARN
logger.displayOnScreen=true
logger.dropDuplicates=true
logger.dropOnOverflow=false

# Flushing and format
logger.flushInterval=30
logger.format=dctpm

# File management
logger.logBufferSize=2048
logger.logFileName=logs/log-@.txt
logger.logFileSize=25M
logger.logRotationLimit=5

# Compression (0.9.56+)
logger.gzip=true
logger.minGzipSize=131072

# On-screen filtering
logger.minimumOnScreenLevel=ERROR

# Per-class overrides
logger.record.net.i2p.router.transport=INFO
logger.record.net.i2p.router.tunnel=DEBUG
logger.record.net.i2p.crypto=WARN
```
---

### تكوين الملحق

#### إعدادات كل مكوّن إضافي على حدة (plugins/*/plugin.config)

**الموقع**: `$I2P_CONFIG_DIR/plugins/{plugin-name}/plugin.config`   **التنسيق**: تنسيق ملف تهيئة I2P القياسي   **التوثيق**: [مواصفات الإضافة](/docs/specs/plugin/)

##### الخصائص المطلوبة

###### الاسم

- **النوع**: سلسلة نصية
- **مطلوب**: نعم
- **الوصف**: اسم العرض للمكوّن الإضافي
- **مثال**: `name=I2P Plugin Example`

###### مفتاح

- **النوع**: String (مفتاح عام)
- **إلزامي**: نعم (يُحذف للمكونات الإضافية الموقعة بـ SU3)
- **الوصف**: المفتاح العام لتوقيع المكون الإضافي لأغراض التحقق
- **الصيغة**: مفتاح توقيع مرمز بصيغة Base64

###### الموقّع

- **النوع**: سلسلة نصية
- **مطلوب**: نعم
- **الوصف**: هوية موقّع الملحق
- **مثال**: `signer=user@example.i2p`

###### الإصدار

- **النوع**: سلسلة نصية (صيغة VersionComparator «مقارنة الإصدارات»)
- **مطلوب**: نعم
- **الوصف**: إصدار المكوّن الإضافي للتحقق من التحديثات
- **الصيغة**: نظام الإصدار الدلالي (Semantic Versioning) أو صيغة قابلة للمقارنة مخصّصة
- **مثال**: `version=1.2.3`

##### خصائص العرض

###### تاريخ

- **النوع**: Long (طابع زمني Unix بالميلي ثانية)
- **الوصف**: تاريخ إصدار المكوّن الإضافي

###### المؤلف

- **النوع**: سلسلة نصية
- **الوصف**: اسم مؤلف المكوّن الإضافي

###### websiteURL

- **النوع**: سلسلة نصية (URL)
- **الوصف**: عنوان URL لموقع الإضافة

###### updateURL

- **النوع**: سلسلة نصية (URL)
- **الوصف**: عنوان URL للتحقق من التحديث للمكوّن الإضافي

###### updateURL.su3

- **النوع**: سلسلة نصية (URL)
- **منذ**: الإصدار 0.9.15
- **الوصف**: عنوان URL لتحديث بتنسيق SU3 (مفضل)

###### الوصف

- **النوع**: سلسلة نصية
- **الوصف**: وصف المكوّن الإضافي باللغة الإنجليزية

###### الوصف_{language}

- **النوع**: سلسلة نصية
- **الوصف**: وصف المكوّن الإضافي المُوطَّن
- **مثال**: `description_de=Deutsche Beschreibung`

###### الترخيص

- **النوع**: سلسلة نصية
- **الوصف**: معرّف ترخيص الإضافة
- **مثال**: `license=Apache 2.0`

##### خصائص التثبيت

###### dont-start-at-install

- **النوع**: Boolean
- **القيمة الافتراضية**: false
- **الوصف**: منع التشغيل التلقائي بعد التثبيت

###### يلزم إعادة تشغيل الـ router

- **النوع**: منطقي
- **الافتراضي**: false
- **الوصف**: يتطلب إعادة تشغيل router بعد التثبيت

###### للتثبيت فقط

- **النوع**: Boolean (قيمة منطقية)
- **القيمة الافتراضية**: false
- **الوصف**: تثبيت مرة واحدة فقط (لا تحديثات)

###### update-only (تحديث فقط)

- **Type**: Boolean (قيمة منطقية)
- **Default**: false
- **Description**: تحديث التثبيت الحالي فقط (بدون تثبيت جديد)

##### مثال على تهيئة الملحق

```properties
# Required properties
name=Example I2P Plugin
signer=developer@mail.i2p
version=1.5.0

# Display properties
author=Plugin Developer
websiteURL=http://plugin.example.i2p
updateURL=http://plugin.example.i2p/update.xpi2p
updateURL.su3=http://plugin.example.i2p/update.su3
description=Example plugin demonstrating configuration
description_de=Beispiel-Plugin zur Demonstration der Konfiguration
license=MIT

# Installation behavior
dont-start-at-install=false
router-restart-required=false
```
#### إعدادات الملحقات العامة (plugins.config)

**الموقع**: `$I2P_CONFIG_DIR/plugins.config`   **الغرض**: تمكين/تعطيل الإضافات المثبتة بشكل شامل

##### تنسيق الخاصية

```properties
plugin.{name}.startOnLoad=true|false
```
- `{name}`: اسم الإضافة من plugin.config
- `startOnLoad`: ما إذا كان يجب تشغيل الإضافة عند بدء تشغيل router

##### مثال

```properties
plugin.i2psnark.startOnLoad=true
plugin.susimail.startOnLoad=true
plugin.susidns.startOnLoad=true
plugin.i2pbote.startOnLoad=false
```
---

### إعدادات تطبيقات الويب (webapps.config)

**الموقع**: `$I2P_CONFIG_DIR/webapps.config`   **الغرض**: تمكين/تعطيل وتهيئة تطبيقات الويب

#### تنسيق الخاصية

##### webapps.{name}.startOnLoad

- **النوع**: قيمة منطقية
- **الوصف**: ما إذا كان سيتم تشغيل تطبيق ويب عند بدء تشغيل router
- **الصيغة**: `webapps.{name}.startOnLoad=true|false`

##### webapps.{name}.classpath

- **النوع**: سلسلة نصية (مسارات مفصولة بمسافة أو فاصلة)
- **الوصف**: عناصر classpath (مسار فئات جافا) إضافية لتطبيق الويب
- **التنسيق**: `webapps.{name}.classpath=[paths]`

#### استبدال المتغيرات

تدعم المسارات عمليات استبدال المتغيرات التالية:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User config directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin webapps</td>
    </tr>
  </tbody>
</table>
#### حلّ Classpath (مسار الأصناف)

- **تطبيقات الويب الأساسية**: مسارات نسبية بالنسبة إلى `$I2P/lib`
- **تطبيقات الويب الإضافية**: مسارات نسبية بالنسبة إلى `$CONFIG/plugins/{appname}/lib`

#### مثال على التهيئة

```properties
# Router console
webapps.routerconsole.startOnLoad=true
webapps.routerconsole.classpath=routerconsole.jar

# I2PSnark
webapps.i2psnark.startOnLoad=true
webapps.i2psnark.classpath=i2psnark.jar

# SusiDNS
webapps.susidns.startOnLoad=true
webapps.susidns.classpath=susidns.jar

# Plugin webapp example
webapps.exampleplugin.startOnLoad=false
webapps.exampleplugin.classpath=$PLUGIN/lib/webapp.jar,$PLUGIN/lib/deps.jar
```
---

### تكوين Router (router.config)

**الموقع**: `$I2P_CONFIG_DIR/router.config`   **واجهة الإعداد**: وحدة تحكم Router على `/configadvanced`   **الغرض**: إعدادات Router الأساسية ومعلمات الشبكة

#### فئات الإعدادات

##### تكوين الشبكة

إعدادات عرض النطاق الترددي:

```properties
i2np.bandwidth.inboundKBytesPerSecond=100
i2np.bandwidth.outboundKBytesPerSecond=50
i2np.bandwidth.share.percentage=80
```
إعدادات النقل:

```properties
# NTCP (TCP-based transport)
i2np.ntcp.port=8887
i2np.ntcp.enable=true
i2np.ntcp.autoip=true

# SSU (UDP-based transport)
i2np.udp.port=8887
i2np.udp.enable=true

# UPnP/NAT-PMP
i2np.upnp.enable=true
```
##### سلوك Router

```properties
# Tunnel participation
router.maxParticipatingTunnels=200
router.sharePercentage=80

# Updates
router.updatePolicy=notify
router.updateURL=http://update.i2p2.i2p/

# Network integration
router.hiddenMode=false
router.clockSkewOffset=0
```
##### إعدادات وحدة التحكم

```properties
# Language and display
routerconsole.lang=en
routerconsole.country=US
routerconsole.summaryRefresh=60

# Browser
routerconsole.browser=default

# Security
routerconsole.enableCompression=true
```
##### إعداد الوقت

```properties
# NTP
time.disabled=false
time.sntpServerList=0.pool.ntp.org,1.pool.ntp.org
```
**ملاحظة**: إعدادات router شاملة. راجع وحدة تحكم router في `/configadvanced` للحصول على مرجع كامل للخصائص.

---

## ملفات تهيئة التطبيق

### إعدادات دفتر العناوين (addressbook/config.txt)

**الموقع**: `$I2P_CONFIG_DIR/addressbook/config.txt`   **التطبيق**: SusiDNS   **الغرض**: حل أسماء المضيفين وإدارة دفتر العناوين

#### مواقع الملفات

##### router_addressbook

- **القيمة الافتراضية**: `../hosts.txt`
- **الوصف**: دفتر العناوين الرئيسي (أسماء المضيفين على مستوى النظام)
- **التنسيق**: تنسيق ملف hosts القياسي

##### privatehosts.txt

- **الموقع**: `$I2P_CONFIG_DIR/addressbook/privatehosts.txt`
- **الوصف**: تعيينات أسماء المضيفين الخاصة
- **الأولوية**: الأعلى (يتجاوز جميع المصادر الأخرى)

##### userhosts.txt

- **الموقع**: `$I2P_CONFIG_DIR/addressbook/userhosts.txt`
- **الوصف**: تعيينات أسماء المضيفين التي أضافها المستخدم
- **الإدارة**: عبر واجهة SusiDNS

##### hosts.txt

- **الموقع**: `$I2P_CONFIG_DIR/addressbook/hosts.txt`
- **الوصف**: دفتر عناوين عام تم تنزيله
- **المصدر**: خلاصات الاشتراك

#### خدمة التسمية

##### BlockfileNamingService (خدمة تسمية ملفات الكتل) (الإعداد الافتراضي منذ 0.8.8)

تنسيق التخزين: - **الملف**: `hostsdb.blockfile` - **الموقع**: `$I2P_CONFIG_DIR/addressbook/` - **الأداء**: ~10x أسرع في عمليات البحث من hosts.txt - **التنسيق**: تنسيق قاعدة بيانات ثنائي

خدمة التسمية القديمة: - **التنسيق**: ملف hosts.txt بنص عادي - **الحالة**: مُهمل ولكن ما يزال مدعوماً - **حالة الاستخدام**: تحرير يدوي، التحكم بالإصدارات

#### قواعد اسم المضيف

يجب أن تتوافق أسماء المضيفين في I2P مع:

1. **متطلب TLD (النطاق ذو المستوى الأعلى)**: يجب أن ينتهي بـ `.i2p`
2. **الحد الأقصى للطول**: 67 حرفًا إجمالًا
3. **مجموعة الأحرف**: `[a-z]`, `[0-9]`, `.` (نقطة), `-` (واصلة)
4. **حالة الأحرف**: أحرف صغيرة فقط
5. **قيود البداية**: لا يمكن أن يبدأ بـ `.` أو `-`
6. **أنماط محظورة**: لا يمكن أن يحتوي على `..` أو `.-` أو `-.` (منذ 0.6.1.33)
7. **محجوز**: أسماء مضيفين Base32 `*.b32.i2p` (52 حرفًا من base32.b32.i2p)

##### أمثلة صحيحة

```
example.i2p
my-site.i2p
test.example.i2p
site123.i2p
```
##### أمثلة غير صالحة

```
example.com          # Wrong TLD
-invalid.i2p         # Starts with hyphen
invalid..i2p         # Contains double dot
invalid.-.i2p        # Contains dot-hyphen
UPPERCASE.I2P        # Must be lowercase
verylonghostnameover67charactersthatexceedsthemaximumlength.i2p  # Too long
```
#### إدارة الاشتراكات

##### subscriptions.txt

- **الموقع**: `$I2P_CONFIG_DIR/addressbook/subscriptions.txt`
- **التنسيق**: عنوان URL واحد في كل سطر
- **القيمة الافتراضية**: `http://i2p-projekt.i2p/hosts.txt`

##### تنسيق خلاصة الاشتراك (منذ الإصدار 0.9.26)

تنسيق موجز متقدم مع بيانات وصفية:

```
#
# I2P Address Book Subscription Feed
# Format: hostname=destination [#property=value ...]
#

example.i2p=base64destination #added=20250101 #src=manual
another.i2p=base64destination #added=20250102 #src=feed1
```
خصائص البيانات الوصفية: - `added`: تاريخ إضافة اسم المضيف (تنسيق YYYYMMDD) - `src`: معرّف المصدر - `sig`: توقيع اختياري

**التوافق مع الإصدارات السابقة**: لا يزال تنسيق hostname=destination البسيط مدعومًا.

#### مثال على التهيئة

```properties
# Address book locations
router_addressbook=../hosts.txt
privatehosts.txt=$CONFIG/addressbook/privatehosts.txt
userhosts.txt=$CONFIG/addressbook/userhosts.txt
hosts.txt=$CONFIG/addressbook/hosts.txt

# Naming service
naming.service=BlockfileNamingService
naming.service.blockfile.location=$CONFIG/addressbook/hostsdb.blockfile

# Subscriptions
subscriptions.txt=$CONFIG/addressbook/subscriptions.txt
subscriptions.schedule=daily
subscriptions.proxy=false
```
---

### إعدادات I2PSnark (i2psnark.config.d/i2psnark.config)

**الموقع**: `$I2P_CONFIG_DIR/i2psnark.config.d/i2psnark.config`   **التطبيق**: عميل BitTorrent I2PSnark   **واجهة الإعدادات**: واجهة ويب رسومية على http://127.0.0.1:7657/i2psnark

#### هيكلية المجلدات

```
$I2P_CONFIG_DIR/i2psnark.config.d/
├── i2psnark.config
├── [torrent-hash-1]/
│   └── *.config
├── [torrent-hash-2]/
│   └── *.config
└── ...
```
#### الإعدادات الرئيسية (i2psnark.config)

التهيئة الافتراضية الدنيا:

```properties
i2psnark.dir=i2psnark
```
خصائص إضافية تُدار عبر واجهة الويب:

```properties
# Basic settings
i2psnark.dir=i2psnark
i2psnark.autoStart=false
i2psnark.openTrackers=true

# Network settings
i2psnark.uploaders=8
i2psnark.upBW=40
i2psnark.seedPct=100

# I2CP settings
i2psnark.i2cpHost=127.0.0.1
i2psnark.i2cpPort=7654
```
#### إعدادات التورنت الفردية

**الموقع**: `$I2P_CONFIG_DIR/i2psnark.config.d/[torrent-hash]/*.config`   **التنسيق**: إعدادات لكل تورنت   **الإدارة**: تلقائي (عبر واجهة الويب الرسومية)

تتضمن الخصائص: - إعدادات الرفع/التنزيل الخاصة بكل تورنت - أولويات الملفات - معلومات المتتبع - حدود النظراء

**ملاحظة**: تتم إدارة إعدادات التورنت في المقام الأول عبر واجهة الويب. لا يُنصح بالتحرير اليدوي.

#### تنظيم بيانات التورنت

تخزين البيانات منفصل عن التهيئة:

```
$I2P_CONFIG_DIR/i2psnark/          # Data directory
├── *.torrent                       # Torrent metadata files
├── *.torrent.downloaded/           # Downloaded file directories
├── file1.dat                       # Direct file downloads
└── ...

$I2P_CONFIG_DIR/i2psnark.config.d/ # Configuration directory
├── i2psnark.config                 # Main config
└── [hashes]/                       # Per-torrent configs
```
---

### إعدادات I2PTunnel (i2ptunnel.config)

**الموقع**: `$I2P_CONFIG_DIR/i2ptunnel.config` (قديم) أو `$I2P_CONFIG_DIR/i2ptunnel.config.d/` (حديث)   **واجهة الإعداد**: لوحة تحكم Router على `/i2ptunnel`   **تغيير التنسيق**: الإصدار 0.9.42 (أغسطس 2019)

#### بنية المجلدات (الإصدار 0.9.42+)

اعتبارًا من الإصدار 0.9.42، يتم تقسيم ملف i2ptunnel.config الافتراضي تلقائيًا:

```
$I2P_CONFIG_DIR/
├── i2ptunnel.config.d/
│   ├── http-proxy/
│   │   └── tunnel.config
│   ├── irc-proxy/
│   │   └── tunnel.config
│   ├── ssh-service/
│   │   └── tunnel.config
│   └── ...
└── i2ptunnel.config (legacy, auto-migrated)
```
**اختلاف جوهري في التنسيق**: - **تنسيق أحادي**: الخصائص مُسبوقة بـ `tunnel.N.` - **تنسيق مُجزّأ**: الخصائص **غير** مُسبوقة (مثلًا، `description=`، وليس `tunnel.0.description=`)

#### سلوك الترحيل

عند التشغيل لأول مرة بعد الترقية إلى 0.9.42: 1. يتم قراءة i2ptunnel.config الموجود 2. يتم إنشاء إعدادات tunnel الفردية في i2ptunnel.config.d/ 3. تُزال البادئة من الخصائص في الملفات المقسمة 4. يتم نسخ الملف الأصلي احتياطيًا 5. لا يزال التنسيق القديم مدعومًا للتوافق مع الإصدارات السابقة

#### أقسام التهيئة

تم توثيق تهيئة I2PTunnel بالتفصيل في قسم [مرجع تهيئة I2PTunnel](#i2ptunnel-configuration-reference) أدناه. تنطبق أوصاف الخصائص على كلٍ من الصيغ الأحادية (`tunnel.N.property`) والمجزأة (`property`).

---

## مرجع إعدادات I2PTunnel

يوفّر هذا القسم مرجعاً تقنياً شاملاً لجميع خصائص تهيئة I2PTunnel. تُعرَض الخصائص بصيغة split format (صيغة مُجزّأة) (من دون البادئة `tunnel.N.`). ولصيغة monolithic format (صيغة موحّدة)، أضِف البادئة `tunnel.N.` إلى جميع الخصائص، حيث N هو رقم الـ tunnel.

**هام**: الخصائص الموصوفة بصيغة `tunnel.N.option.i2cp.*` مُنفَّذة في I2PTunnel وهي **غير** مدعومة عبر واجهات أخرى مثل بروتوكول I2CP أو SAM API.

### الخصائص الأساسية

#### tunnel.N.description (الوصف)

- **النوع**: سلسلة نصية
- **السياق**: جميع tunnels
- **الوصف**: وصف tunnel قابل للقراءة من قبل البشر لعرضه في واجهة المستخدم
- **مثال**: `description=HTTP Proxy for outproxy access`

#### tunnel.N.name (الاسم)

- **النوع**: سلسلة نصية
- **السياق**: جميع الـ tunnel
- **مطلوب**: نعم
- **الوصف**: معرّف tunnel فريد واسم العرض
- **مثال**: `name=I2P HTTP Proxy`

#### tunnel.N.type (النوع)

- **النوع**: تعداد (Enum)
- **السياق**: جميع tunnels
- **مطلوب**: نعم
- **القيم**:
  - `client` - tunnel عميل عام
  - `httpclient` - عميل وكيل HTTP
  - `ircclient` - tunnel عميل IRC
  - `socksirctunnel` - وكيل SOCKS لـ IRC
  - `sockstunnel` - وكيل SOCKS (الإصدار 4 و4a و5)
  - `connectclient` - عميل وكيل CONNECT
  - `streamrclient` - عميل Streamr
  - `server` - tunnel خادم عام
  - `httpserver` - tunnel خادم HTTP
  - `ircserver` - tunnel خادم IRC
  - `httpbidirserver` - خادم HTTP ثنائي الاتجاه
  - `streamrserver` - خادم Streamr

#### tunnel.N.interface (واجهة)

- **النوع**: سلسلة نصية (عنوان IP أو اسم مضيف)
- **السياق**: مقتصر على tunnels الخاصة بالعميل
- **القيمة الافتراضية**: 127.0.0.1
- **الوصف**: الواجهة المحلية التي سيتم الربط بها للاتصالات الواردة
- **ملاحظة أمنية**: الربط على 0.0.0.0 يسمح باتصالات عن بُعد
- **مثال**: `interface=127.0.0.1`

#### tunnel.N.listenPort (listenPort)

- **النوع**: عدد صحيح
- **السياق**: Client tunnels فقط
- **النطاق**: 1-65535
- **الوصف**: منفذ محلي للاستماع إلى اتصالات العملاء
- **مثال**: `listenPort=4444`

#### tunnel.N.targetHost (targetHost)

- **النوع**: سلسلة نصية (عنوان IP أو اسم مضيف)
- **السياق**: فقط لـ tunnels الخاصة بالخادم
- **الوصف**: خادم محلي لإعادة توجيه الاتصالات إليه
- **مثال**: `targetHost=127.0.0.1`

#### tunnel.N.targetPort (targetPort)

- **النوع**: عدد صحيح
- **السياق**: خاص بـ Server tunnels فقط
- **النطاق**: 1-65535
- **الوصف**: المنفذ على targetHost المراد الاتصال به
- **مثال**: `targetPort=80`

#### tunnel.N.targetDestination (targetDestination)

- **النوع**: سلسلة نصية (وجهات مفصولة بفواصل أو مسافات)
- **السياق**: tunnels الخاصة بالعميل فقط
- **الصيغة**: `destination[:port][,destination[:port]]`
- **الوصف**: وجهة/وجهات I2P للاتصال بها
- **أمثلة**:
  - `targetDestination=example.i2p`
  - `targetDestination=example.i2p:8080`
  - `targetDestination=site1.i2p,site2.i2p:8080`

#### tunnel.N.i2cpHost (i2cpHost)

- **النوع**: سلسلة نصية (عنوان IP أو اسم المضيف)
- **القيمة الافتراضية**: 127.0.0.1
- **الوصف**: عنوان واجهة I2CP لـ I2P router
- **ملاحظة**: يُتجاهَل عند التشغيل في سياق router
- **مثال**: `i2cpHost=127.0.0.1`

#### tunnel.N.i2cpPort (i2cpPort)

- **النوع**: عدد صحيح
- **القيمة الافتراضية**: 7654
- **النطاق**: 1-65535
- **الوصف**: منفذ I2CP الخاص بـ I2P router
- **ملاحظة**: يُتجاهَل عند التشغيل في سياق router
- **مثال**: `i2cpPort=7654`

#### tunnel.N.startOnLoad (startOnLoad)

- **النوع**: منطقي
- **القيمة الافتراضية**: true
- **الوصف**: ما إذا كان سيتم بدء tunnel عند تحميل I2PTunnel
- **مثال**: `startOnLoad=true`

### إعدادات الوكيل

#### tunnel.N.proxyList (proxyList)

- **النوع**: سلسلة نصية (أسماء المضيفين المفصولة بفواصل أو مسافات)
- **السياق**: وكلاء HTTP وSOCKS فقط
- **الوصف**: قائمة بمضيفي outproxy (وكيل الخروج إلى الإنترنت العام)
- **مثال**: `proxyList=outproxy.example.i2p,backup.example.i2p`

### إعدادات الخادم

#### tunnel.N.privKeyFile (privKeyFile)

- **النوع**: سلسلة نصية (مسار ملف)
- **السياق**: الخوادم وtunnels (قنوات اتصال داخل I2P) الخاصة بالعميل والمستمرة
- **الوصف**: ملف يحتوي على المفاتيح الخاصة لوجهة دائمة
- **المسار**: مطلق أو نسبي بالنسبة إلى دليل إعدادات I2P
- **مثال**: `privKeyFile=eepsite/eepPriv.dat`

#### tunnel.N.spoofedHost (spoofedHost)

- **النوع**: String (اسم المضيف)
- **السياق**: خوادم HTTP فقط
- **القيمة الافتراضية**: اسم مضيف Base32 للوجهة
- **الوصف**: قيمة ترويسة Host المُمرَّرة إلى الخادم المحلي
- **مثال**: `spoofedHost=example.i2p`

#### tunnel.N.spoofedHost.NNNN (spoofedHost.NNNN)

- **النوع**: سلسلة نصية (اسم المضيف)
- **السياق**: خوادم HTTP فقط
- **الوصف**: تجاوز المضيف الظاهري لمنفذ وارد محدد
- **حالة الاستخدام**: استضافة مواقع متعددة على منافذ مختلفة
- **مثال**: `spoofedHost.8080=site1.example.i2p`

### خيارات خاصة بالعميل

#### tunnel.N.sharedClient (sharedClient)

- **النوع**: منطقي
- **السياق**: Client tunnels فقط
- **القيمة الافتراضية**: false
- **الوصف**: ما إذا كان بإمكان عدة عملاء مشاركة هذا الـ tunnel
- **مثال**: `sharedClient=false`

#### tunnel.N.option.persistentClientKey (persistentClientKey)

- **النوع**: قيمة منطقية
- **السياق**: خاصّ بـ Client tunnels فقط
- **الافتراضي**: false
- **الوصف**: تخزين وإعادة استخدام مفاتيح الوجهة عبر عمليات إعادة التشغيل
- **التعارض**: يتنافى مع `i2cp.newDestOnResume=true`
- **مثال**: `option.persistentClientKey=true`

### خيارات I2CP (تنفيذ I2PTunnel)

**مهم**: تبدأ هذه الخصائص بالبادئة `option.i2cp.` ولكن يتم **تنفيذها في I2PTunnel**، وليس في طبقة بروتوكول I2CP. وهي غير متاحة عبر واجهات برمجة تطبيقات I2CP أو SAM.

#### tunnel.N.option.i2cp.delayOpen (option.i2cp.delayOpen)

- **النوع**: منطقي
- **السياق**: خاص بـ Client tunnels فقط
- **القيمة الافتراضية**: false
- **الوصف**: تأخير إنشاء tunnel حتى أول اتصال
- **حالة الاستخدام**: توفير الموارد لـ tunnels نادرة الاستخدام
- **مثال**: `option.i2cp.delayOpen=false`

#### tunnel.N.option.i2cp.newDestOnResume (option.i2cp.newDestOnResume)

- **النوع**: منطقي
- **السياق**: Client tunnels فقط
- **الافتراضي**: false
- **المتطلبات**: `i2cp.closeOnIdle=true`
- **التعارض**: غير قابل للجمع (تعارض متبادل) مع `persistentClientKey=true`
- **الوصف**: إنشاء وجهة جديدة بعد انتهاء مهلة الخمول
- **مثال**: `option.i2cp.newDestOnResume=false`

#### tunnel.N.option.i2cp.leaseSetPrivateKey (option.i2cp.leaseSetPrivateKey)

- **النوع**: سلسلة نصية (مفتاح مُرمَّز بـ base64)
- **السياق**: tunnels (مسارات اتصال في I2P) الخاصة بالخادم فقط
- **الوصف**: مفتاح تشفير leaseset (مجموعة معلومات الوصول في I2P) خاص دائم
- **حالة الاستخدام**: الحفاظ على leaseset مُشفّرة ومتّسقة عبر عمليات إعادة التشغيل
- **مثال**: `option.i2cp.leaseSetPrivateKey=AAAA...base64...`

#### tunnel.N.option.i2cp.leaseSetSigningPrivateKey (option.i2cp.leaseSetSigningPrivateKey)

- **النوع**: String (sigtype:base64)
- **السياق**: tunnels الخاصة بالخادم فقط
- **التنسيق**: `sigtype:base64key`
- **الوصف**: المفتاح الخاص الدائم لتوقيع leaseset
- **مثال**: `option.i2cp.leaseSetSigningPrivateKey=7:AAAA...base64...`

### خيارات خاصة بالخادم

#### tunnel.N.option.enableUniqueLocal (option.enableUniqueLocal)

- **النوع**: منطقي
- **السياق**: tunnels الخاصة بالخادم فقط
- **القيمة الافتراضية**: false
- **الوصف**: استخدام عنوان IP محلي فريد لكل وجهة I2P بعيدة
- **حالة الاستخدام**: تتبّع عناوين IP للعملاء في سجلات الخادم
- **ملاحظة أمنية**: قد يقلل من مستوى عدم الكشف عن الهوية
- **مثال**: `option.enableUniqueLocal=false`

#### tunnel.N.option.targetForPort.NNNN (option.targetForPort.NNNN)

- **النوع**: سلسلة نصية (hostname:port)
- **السياق**: Server tunnels فقط
- **الوصف**: تجاوز targetHost/targetPort للمنفذ الوارد NNNN
- **حالة الاستخدام**: توجيه قائم على المنفذ إلى خدمات محلية مختلفة
- **مثال**: `option.targetForPort.8080=localhost:8080`

### تكوين تجمع الخيوط

#### tunnel.N.option.i2ptunnel.usePool (option.i2ptunnel.usePool)

- **النوع**: منطقي
- **السياق**: ينطبق على tunnels الخوادم فقط
- **القيمة الافتراضية**: true
- **الوصف**: استخدام مجمّع مؤشرات الترابط (thread pool) لمعالجة الاتصالات
- **ملاحظة**: تكون القيمة دائمًا false في الخوادم القياسية (يتم تجاهله)
- **مثال**: `option.i2ptunnel.usePool=true`

#### tunnel.N.option.i2ptunnel.blockingHandlerCount (option.i2ptunnel.blockingHandlerCount)

- **النوع**: عدد صحيح
- **السياق**: فقط لـ Server tunnels
- **القيمة الافتراضية**: 65
- **الوصف**: الحد الأقصى لحجم thread pool (تجمّع الخيوط)
- **ملاحظة**: يتم تجاهله للخوادم القياسية
- **مثال**: `option.i2ptunnel.blockingHandlerCount=100`

### خيارات عميل HTTP

#### tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL (option.i2ptunnel.httpclient.allowInternalSSL)

- **النوع**: منطقي
- **السياق**: عملاء HTTP فقط
- **القيمة الافتراضية**: false
- **الوصف**: السماح باتصالات SSL إلى عناوين .i2p
- **مثال**: `option.i2ptunnel.httpclient.allowInternalSSL=false`

#### tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper (option.i2ptunnel.httpclient.disableAddressHelper)

- **النوع**: منطقي
- **السياق**: عملاء HTTP فقط
- **الافتراضي**: false
- **الوصف**: تعطيل روابط مساعد العنوان في استجابات الوكيل
- **مثال**: `option.i2ptunnel.httpclient.disableAddressHelper=false`

#### tunnel.N.option.i2ptunnel.httpclient.jumpServers (option.i2ptunnel.httpclient.jumpServers)

- **النوع**: سلسلة نصية (عناوين URL مفصولة بفواصل أو بمسافات)
- **السياق**: عملاء HTTP فقط
- **الوصف**: عناوين URL لخوادم Jump (خوادم القفز) لحل أسماء المضيفين
- **مثال**: `option.i2ptunnel.httpclient.jumpServers=http://jump.i2p/jump,http://stats.i2p/jump`

#### tunnel.N.option.i2ptunnel.httpclient.sendAccept (option.i2ptunnel.httpclient.sendAccept)

- **النوع**: منطقي
- **السياق**: عملاء HTTP فقط
- **الافتراضي**: false
- **الوصف**: تمرير رؤوس Accept-* (باستثناء Accept و Accept-Encoding)
- **مثال**: `option.i2ptunnel.httpclient.sendAccept=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendReferer (option.i2ptunnel.httpclient.sendReferer)

- **النوع**: منطقي (Boolean)
- **السياق**: عملاء HTTP فقط
- **القيمة الافتراضية**: false
- **الوصف**: تمرير رؤوس Referer عبر الوكيل
- **ملاحظة الخصوصية**: قد تسرّب معلومات
- **مثال**: `option.i2ptunnel.httpclient.sendReferer=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendUserAgent (option.i2ptunnel.httpclient.sendUserAgent)

- **النوع**: Boolean (قيمة منطقية)
- **السياق**: عملاء HTTP فقط
- **القيمة الافتراضية**: false
- **الوصف**: تمرير رؤوس User-Agent عبر الوكيل
- **ملاحظة الخصوصية**: قد تُسرّب معلومات المتصفح
- **مثال**: `option.i2ptunnel.httpclient.sendUserAgent=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendVia (option.i2ptunnel.httpclient.sendVia)

- **النوع**: قيمة منطقية
- **السياق**: عملاء HTTP فقط
- **القيمة الافتراضية**: false
- **الوصف**: تمرير ترويسات Via عبر الوكيل
- **مثال**: `option.i2ptunnel.httpclient.sendVia=false`

#### tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies (option.i2ptunnel.httpclient.SSLOutproxies)

- **النوع**: سلسلة نصية (وجهات مفصولة بفواصل أو مسافات)
- **السياق**: عملاء HTTP فقط
- **الوصف**: وكلاء خروج SSL داخل الشبكة لطلبات HTTPS
- **مثال**: `option.i2ptunnel.httpclient.SSLOutproxies=ssl-outproxy.i2p`

#### tunnel.N.option.i2ptunnel.useLocalOutproxy (option.i2ptunnel.useLocalOutproxy)

- **النوع**: قيمة منطقية
- **السياق**: لعملاء HTTP فقط
- **القيمة الافتراضية**: true
- **الوصف**: استخدام ملحقات outproxy (وكيل خروج) المحلية المسجّلة
- **مثال**: `option.i2ptunnel.useLocalOutproxy=true`

### مصادقة عميل HTTP

#### tunnel.N.option.proxyAuth (option.proxyAuth)

- **النوع**: تعداد
- **السياق**: عملاء HTTP فقط
- **القيمة الافتراضية**: false
- **القيم**: `true`, `false`, `basic`, `digest`
- **الوصف**: يتطلب مصادقة محلية للوصول إلى الوكيل
- **ملاحظة**: `true` تعادل `basic`
- **مثال**: `option.proxyAuth=basic`

#### tunnel.N.option.proxy.auth.USER.md5 (option.proxy.auth.USER.md5)

- **النوع**: سلسلة ست عشرية مؤلفة من 32 محرفاً بأحرف صغيرة
- **السياق**: لعملاء HTTP فقط
- **يتطلب**: `proxyAuth=basic` أو `proxyAuth=digest`
- **الوصف**: تجزئة MD5 لكلمة مرور المستخدم USER
- **مهمل**: استخدم SHA-256 بدلاً من ذلك (0.9.56+)
- **مثال**: `option.proxy.auth.alice.md5=5f4dcc3b5aa765d61d8327deb882cf99`

#### tunnel.N.option.proxy.auth.USER.sha256 (option.proxy.auth.USER.sha256)

- **النوع**: سلسلة (سداسي عشري بأحرف صغيرة مكوّنة من 64 حرفًا)
- **السياق**: عملاء HTTP فقط
- **يتطلب**: `proxyAuth=digest`
- **منذ**: الإصدار 0.9.56
- **المعيار**: RFC 7616
- **الوصف**: تجزئة SHA-256 لكلمة مرور المستخدم USER
- **مثال**: `option.proxy.auth.alice.sha256=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

### مصادقة الوكيل الخارجي

#### tunnel.N.option.outproxyAuth (option.outproxyAuth)

- **النوع**: قيمة منطقية
- **السياق**: خاص بعملاء HTTP فقط
- **القيمة الافتراضية**: false
- **الوصف**: إرسال بيانات المصادقة إلى outproxy (الوكيل الخارجي)
- **مثال**: `option.outproxyAuth=false`

#### tunnel.N.option.outproxyUsername (option.outproxyUsername)

- **النوع**: سلسلة نصية
- **السياق**: عملاء HTTP فقط
- **يتطلّب**: `outproxyAuth=true`
- **الوصف**: اسم المستخدم لمصادقة outproxy (وكيل خروجي)
- **مثال**: `option.outproxyUsername=user`

#### tunnel.N.option.outproxyPassword (option.outproxyPassword)

- **النوع**: سلسلة نصية
- **السياق**: عملاء HTTP فقط
- **يتطلب**: `outproxyAuth=true`
- **الوصف**: كلمة مرور لمصادقة outproxy (وكيل خارجي للوصول إلى الإنترنت العام)
- **الأمان**: مخزّنة كنص عادي
- **مثال**: `option.outproxyPassword=secret`

### خيارات عميل SOCKS

#### tunnel.N.option.i2ptunnel.socks.proxy.default (option.i2ptunnel.socks.proxy.default)

- **النوع**: سلسلة نصية (وجهات مفصولة بفواصل أو مسافات)
- **السياق**: عملاء SOCKS فقط
- **الوصف**: وكلاء خروج داخل الشبكة للمنافذ غير المحددة
- **مثال**: `option.i2ptunnel.socks.proxy.default=outproxy.i2p`

#### tunnel.N.option.i2ptunnel.socks.proxy.NNNN (option.i2ptunnel.socks.proxy.NNNN)

- **النوع**: سلسلة نصية (وجهات مفصولة بفواصل أو مسافات)
- **السياق**: عملاء SOCKS فقط
- **الوصف**: وكلاء خروج داخل الشبكة لمنفذ NNNN تحديداً
- **مثال**: `option.i2ptunnel.socks.proxy.443=ssl-outproxy.i2p`

#### tunnel.N.option.outproxyType (option.outproxyType)

- **النوع**: تعداد
- **السياق**: عملاء SOCKS فقط
- **القيمة الافتراضية**: socks
- **منذ**: الإصدار 0.9.57
- **القيم**: `socks`, `connect` (HTTPS)
- **الوصف**: نوع الـ outproxy (وكيل خارجي) المُكوَّن
- **مثال**: `option.outproxyType=connect`

### خيارات خادم HTTP

#### tunnel.N.option.maxPosts (option.maxPosts)

- **النوع**: عدد صحيح
- **السياق**: خوادم HTTP فقط
- **القيمة الافتراضية**: 0 (غير محدود)
- **الوصف**: الحد الأقصى لطلبات POST من وجهة واحدة لكل postCheckTime
- **مثال**: `option.maxPosts=10`

#### tunnel.N.option.maxTotalPosts (option.maxTotalPosts)

- **النوع**: عدد صحيح
- **السياق**: خوادم HTTP فقط
- **القيمة الافتراضية**: 0 (غير محدود)
- **الوصف**: الحد الأقصى لعدد عمليات POST من جميع الوجهات لكل postCheckTime
- **مثال**: `option.maxTotalPosts=50`

#### tunnel.N.option.postCheckTime (option.postCheckTime)

- **النوع**: عدد صحيح (ثوانٍ)
- **السياق**: خوادم HTTP فقط
- **القيمة الافتراضية**: 300
- **الوصف**: إطار زمني للتحقق من حدود طلبات POST
- **مثال**: `option.postCheckTime=600`

#### tunnel.N.option.postBanTime (option.postBanTime)

- **النوع**: عدد صحيح (ثوانٍ)
- **السياق**: خوادم HTTP فقط
- **القيمة الافتراضية**: 1800
- **الوصف**: مدة الحظر بعد تجاوز maxPosts لوجهة واحدة
- **مثال**: `option.postBanTime=3600`

#### tunnel.N.option.postTotalBanTime (option.postTotalBanTime)

- **النوع**: عدد صحيح (بالثواني)
- **السياق**: خوادم HTTP فقط
- **القيمة الافتراضية**: 600
- **الوصف**: مدة الحظر بعد تجاوز maxTotalPosts
- **مثال**: `option.postTotalBanTime=1200`

### خيارات أمان خادم HTTP

#### tunnel.N.option.rejectInproxy (option.rejectInproxy)

- **النوع**: منطقي
- **السياق**: خوادم HTTP فقط
- **القيمة الافتراضية**: false
- **الوصف**: رفض الاتصالات التي تبدو قادمة عبر inproxy (وكيل دخول)
- **مثال**: `option.rejectInproxy=false`

#### tunnel.N.option.rejectReferer (option.rejectReferer)

- **النوع**: منطقي (Boolean)
- **السياق**: خوادم HTTP فقط
- **القيمة الافتراضية**: false
- **منذ**: الإصدار 0.9.25
- **الوصف**: رفض الاتصالات التي تحتوي على ترويسة Referer (ترويسة HTTP الخاصة بالإحالة)
- **مثال**: `option.rejectReferer=false`

#### tunnel.N.option.rejectUserAgents (option.rejectUserAgents)

- **النوع**: منطقي (Boolean)
- **السياق**: خوادم HTTP فقط
- **القيمة الافتراضية**: false
- **منذ**: الإصدار 0.9.25
- **يتطلب**: الخاصية `userAgentRejectList`
- **الوصف**: رفض الاتصالات ذات User-Agent المطابق
- **مثال**: `option.rejectUserAgents=false`

#### tunnel.N.option.userAgentRejectList (option.userAgentRejectList)

- **النوع**: سلسلة نصية (سلاسل مطابقة مفصولة بفواصل)
- **السياق**: خوادم HTTP فقط
- **منذ**: الإصدار 0.9.25
- **حالة الأحرف**: مطابقة حساسة لحالة الأحرف
- **خاص**: "none" (منذ 0.9.33) يطابق User-Agent فارغ
- **الوصف**: قائمة بأنماط User-Agent المطلوب رفضها
- **مثال**: `option.userAgentRejectList=Mozilla,Opera,none`

### خيارات خادم IRC

#### tunnel.N.option.ircserver.fakeHostname (option.ircserver.fakeHostname)

- **النوع**: سلسلة نصية (نمط اسم المضيف)
- **السياق**: خوادم IRC فقط
- **القيمة الافتراضية**: `%f.b32.i2p`
- **الرموز**:
  - `%f` = التجزئة الكاملة لوجهة بترميز base32
  - `%c` = تجزئة وجهة مُقنَّعة (انظر cloakKey)
- **الوصف**: تنسيق اسم المضيف المُرسل إلى خادم IRC
- **مثال**: `option.ircserver.fakeHostname=%c.irc.i2p`

#### tunnel.N.option.ircserver.cloakKey (option.ircserver.cloakKey)

- **النوع**: سلسلة نصية (عبارة مرور)
- **السياق**: خوادم IRC فقط
- **القيمة الافتراضية**: عشوائي في كل جلسة
- **القيود**: من دون علامات اقتباس أو مسافات
- **الوصف**: عبارة مرور لتمويه اسم المضيف بشكل متسق (hostname cloaking)
- **حالة الاستخدام**: تتبّع المستخدم بشكل مستمر عبر عمليات إعادة التشغيل/الخوادم
- **مثال**: `option.ircserver.cloakKey=mysecretkey`

#### tunnel.N.option.ircserver.method (option.ircserver.method)

- **النوع**: تعداد
- **السياق**: خوادم IRC فقط
- **القيمة الافتراضية**: user
- **القيم**: `user`, `webirc`
- **الوصف**: طريقة المصادقة لخادم IRC
- **مثال**: `option.ircserver.method=webirc`

#### tunnel.N.option.ircserver.webircPassword (option.ircserver.webircPassword)

- **النوع**: سلسلة نصية (كلمة مرور)
- **السياق**: خوادم IRC فقط
- **يتطلب**: `method=webirc`
- **القيود**: بدون علامات اقتباس أو مسافات
- **الوصف**: كلمة مرور لمصادقة بروتوكول WEBIRC
- **مثال**: `option.ircserver.webircPassword=webircpass`

#### tunnel.N.option.ircserver.webircSpoofIP (option.ircserver.webircSpoofIP)

- **النوع**: سلسلة نصية (عنوان IP)
- **السياق**: خوادم IRC فقط
- **يتطلب**: `method=webirc`
- **الوصف**: عنوان IP مُنتَحل لبروتوكول WEBIRC
- **مثال**: `option.ircserver.webircSpoofIP=10.0.0.1`

### تهيئة SSL/TLS

#### tunnel.N.option.useSSL (option.useSSL)

- **النوع**: منطقي
- **القيمة الافتراضية**: false
- **السياق**: جميع tunnels
- **السلوك**:
  - **الخوادم**: استخدام SSL للاتصالات بالخادم المحلي
  - **العملاء**: يتطلب SSL من العملاء المحليين
- **مثال**: `option.useSSL=false`

#### tunnel.N.option.keystoreFile (option.keystoreFile)

- **النوع**: سلسلة نصية (مسار ملف)
- **السياق**: لِـ client tunnels فقط
- **القيمة الافتراضية**: `i2ptunnel-(random).ks`
- **المسار**: نسبي إلى `$(I2P_CONFIG_DIR)/keystore/` إذا لم يكن مطلقًا
- **مُولَّد تلقائيًا**: يُنشأ إذا لم يكن موجودًا
- **الوصف**: ملف مخزن المفاتيح الذي يحتوي على المفتاح الخاص لـ SSL
- **مثال**: `option.keystoreFile=my-tunnel.ks`

#### tunnel.N.option.keystorePassword (option.keystorePassword)

- **النوع**: سلسلة نصية (كلمة مرور)
- **السياق**: Client tunnels فقط
- **القيمة الافتراضية**: changeit
- **يُنشأ تلقائيًا**: كلمة مرور عشوائية إذا تم إنشاء مخزن مفاتيح جديد
- **الوصف**: كلمة المرور لمخزن مفاتيح SSL
- **مثال**: `option.keystorePassword=secretpassword`

#### tunnel.N.option.keyAlias (option.keyAlias)

- **النوع**: سلسلة نصية (اسم مستعار)
- **السياق**: خاص بـ Client tunnels فقط
- **يُنشأ تلقائيًا**: يُنشأ عند إنشاء مفتاح جديد
- **الوصف**: اسم مستعار للمفتاح الخاص في مخزن المفاتيح
- **مثال**: `option.keyAlias=mytunnel-key`

#### tunnel.N.option.keyPassword (option.keyPassword)

- **النوع**: سلسلة نصية (كلمة مرور)
- **السياق**: tunnels الخاصة بالعميل فقط
- **يتم توليده تلقائياً**: كلمة مرور عشوائية إذا تم إنشاء مفتاح جديد
- **الوصف**: كلمة مرور للمفتاح الخاص في مخزن المفاتيح (keystore)
- **مثال**: `option.keyPassword=keypass123`

### خيارات I2CP العامة وخيارات التدفق

تُمرَّر جميع خصائص `tunnel.N.option.*` (غير الموثَّقة تحديدًا أعلاه) إلى واجهة I2CP ومكتبة البث بعد إزالة البادئة `tunnel.N.option.`.

**مهم**: هذه منفصلة عن الخيارات الخاصة بـ I2PTunnel. راجع: - [مواصفة I2CP](/docs/specs/i2cp/) - [مواصفة مكتبة البث](/docs/specs/streaming/)

أمثلة لخيارات البث التدفقي:

```properties
option.i2cp.messageReliability=BestEffort
option.i2p.streaming.connectDelay=1000
option.i2p.streaming.maxWindowSize=128
```
### مثال كامل على Tunnel

```properties
# HTTP Proxy (split format without tunnel.N. prefix)
name=I2P HTTP Proxy
description=HTTP proxy for accessing I2P sites and outproxy
type=httpclient
interface=127.0.0.1
listenPort=4444
targetDestination=
sharedClient=true
startOnLoad=true

# I2CP configuration
i2cpHost=127.0.0.1
i2cpPort=7654

# HTTP client options
option.i2ptunnel.httpclient.allowInternalSSL=false
option.i2ptunnel.httpclient.disableAddressHelper=false
option.i2ptunnel.httpclient.jumpServers=http://stats.i2p/cgi-bin/jump.cgi
option.i2ptunnel.httpclient.sendAccept=false
option.i2ptunnel.httpclient.sendReferer=false
option.i2ptunnel.httpclient.sendUserAgent=false

# Proxy authentication
option.proxyAuth=false

# Outproxy configuration
option.i2ptunnel.httpclient.SSLOutproxies=false.i2p
proxyList=false.i2p

# Client behavior
option.persistentClientKey=false
option.i2cp.delayOpen=false

# I2CP tunnel options
option.inbound.length=3
option.outbound.length=3
option.inbound.quantity=2
option.outbound.quantity=2
```
---

## سجل الإصدارات والجدول الزمني للميزات

### الإصدار 0.9.10 (2013)

**الميزة**: دعم القيم الفارغة في ملفات الإعداد - المفاتيح ذات القيم الفارغة (`key=`) أصبحت مدعومة الآن - كانت تُتجاهَل سابقًا أو تتسبب في أخطاء في التحليل

### الإصدار 0.9.18 (2015)

**الميزة**: تكوين فترة تفريغ المسجّل - الخاصية: `logger.flushInterval` (الافتراضي 29 ثانية) - يقلّل I/O للقرص (الإدخال/الإخراج للقرص) مع الحفاظ على كمون سجل مقبول

### الإصدار 0.9.23 (نوفمبر 2015)

**تغيير رئيسي**: الحد الأدنى المطلوب هو Java 7 - انتهى دعم Java 6 - مطلوب للاستمرار في تلقي تحديثات الأمان

### الإصدار 0.9.25 (2015)

**الميزات**: خيارات أمان خادم HTTP - `tunnel.N.option.rejectReferer` - رفض الاتصالات التي تحتوي على ترويسة Referer - `tunnel.N.option.rejectUserAgents` - رفض ترويسات User-Agent محددة - `tunnel.N.option.userAgentRejectList` - أنماط User-Agent المطلوب رفضها - **حالة الاستخدام**: الحد من برامج الزحف والعملاء غير المرغوب فيهم

### الإصدار 0.9.33 (يناير 2018)

**الميزة**: تصفية محسّنة لـ User-Agent (وكيل المستخدم) - `userAgentRejectList` القيمة النصية "none" تطابق User-Agent الفارغ - إصلاحات أخطاء إضافية لـ i2psnark و i2ptunnel و streaming و SusiMail

### الإصدار 0.9.41 (2019)

**إيقاف الدعم**: تمت إزالة BOB Protocol (بروتوكول BOB الخاص بـ I2P) من Android - يجب على مستخدمي Android الانتقال إلى SAM أو I2CP

### الإصدار 0.9.42 (أغسطس 2019)

**تغيير كبير**: تقسيم ملفات الإعداد - تقسيم `clients.config` إلى بنية دليل `clients.config.d/` - تقسيم `i2ptunnel.config` إلى بنية دليل `i2ptunnel.config.d/` - ترحيل تلقائي عند أول تشغيل بعد الترقية - يُتيح الحزم المعيارية وإدارة الملحقات - لا يزال التنسيق الأحادي القديم مدعوماً

**ميزات إضافية**: - تحسينات أداء SSU - منع العبور بين الشبكات (Proposal 147) - دعم أولي لأنواع التشفير

### الإصدار 0.9.56 (2021)

**الميزات**: تحسينات الأمان والتسجيل - `logger.gzip` - ضغط Gzip للسجلات المُدوَّرة (الإعداد الافتراضي: false) - `logger.minGzipSize` - الحد الأدنى للحجم للضغط (الإعداد الافتراضي: 65536 بايت) - `tunnel.N.option.proxy.auth.USER.sha256` - مصادقة الملخص باستخدام SHA-256 (RFC 7616) - **الأمان**: يحل SHA-256 محل MD5 في مصادقة الملخص

### الإصدار 0.9.57 (يناير 2023)

**ميزة**: تهيئة نوع outproxy (وكيل خروج إلى الإنترنت العام) الخاص بـ SOCKS - `tunnel.N.option.outproxyType` - اختر نوع outproxy (socks|connect) - القيمة الافتراضية: socks - دعم HTTPS CONNECT لـ outproxies الخاصة بـ HTTPS

### الإصدار 2.6.0 (يوليو 2024)

**تغيير كاسر للتوافق**: تم حظر I2P-over-Tor (تشغيل I2P عبر Tor) - يتم الآن رفض الاتصالات الواردة من عناوين IP لعقد خروج Tor - **السبب**: يضعف أداء I2P، ويهدر موارد عقد الخروج في Tor - **التأثير**: سيُحظر المستخدمون الذين يصلون إلى I2P عبر عقد خروج Tor - عقد الترحيل غير الخروجية وعملاء Tor غير متأثرين

### الإصدار 2.10.0 (سبتمبر 2025 - الحالي)

**الميزات الرئيسية**: - **التشفير ما بعد الكم** متاح (اختياري عبر Hidden Service Manager (مدير الخدمات المخفية)) - **دعم مُتعقّب UDP** لـ I2PSnark لتقليل حمل المُتعقّب - **ثبات Hidden Mode (الوضع المخفي)** تحسينات لتقليل استنزاف RouterInfo - تحسينات في الشبكة لـ routers المزدحمة - تعزيز اجتياز UPnP/NAT - تحسينات NetDB مع إزالة leaseset بشكل عدواني - تقليل قابليّة الرصد لأحداث router

**التهيئة**: لم تتم إضافة أي خصائص تهيئة جديدة

**تغيير بالغ الأهمية مرتقب**: الإصدار القادم (على الأرجح 2.11.0 أو 3.0.0) سيتطلب جافا 17 أو أحدث

---

## الميزات المُهمَلة والتغييرات الكاسرة للتوافق

### إهمالات حرجة

#### الوصول عبر I2P-over-Tor (الإصدار 2.6.0+)

- **الحالة**: محظور منذ يوليو 2024
- **التأثير**: رفض الاتصالات القادمة من عناوين IP لعُقد الخروج في Tor
- **السبب**: يُضعِف أداء شبكة I2P دون تقديم فوائد لإخفاء الهوية
- **يؤثر على**: عُقد الخروج في Tor فقط، وليس المرحلات أو عملاء Tor العاديين
- **البديل**: استخدم I2P أو Tor بشكل منفصل، وليس معًا

#### مصادقة الملخص باستخدام MD5

- **الحالة**: مُهمل (استخدم SHA-256)
- **الخاصية**: `tunnel.N.option.proxy.auth.USER.md5`
- **السبب**: MD5 مكسور تشفيرياً
- **البديل**: `tunnel.N.option.proxy.auth.USER.sha256` (اعتباراً من 0.9.56)
- **الجدول الزمني**: لا يزال MD5 مدعوماً ولكن غير مستحسن

### تغييرات معمارية في التهيئة

#### ملفات التكوين الأحادية (الإصدار 0.9.42+)

- **المتأثر**: `clients.config`, `i2ptunnel.config`
- **الحالة**: مُهمل لصالح بنية أدلة منفصلة
- **الترحيل**: تلقائي عند أول تشغيل بعد الترقية إلى 0.9.42
- **التوافق**: التنسيق القديم ما زال يعمل (متوافق مع الإصدارات السابقة)
- **التوصية**: استخدم التنسيق المُقسّم للتكوينات الجديدة

### متطلبات إصدار جافا

#### دعم Java 6

- **انتهى**: الإصدار 0.9.23 (نوفمبر 2015)
- **الحد الأدنى**: Java 7 مطلوب منذ 0.9.23

#### متطلب Java 17 (قادم)

- **الحالة**: تغيير حرج مرتقب
- **الهدف**: الإصدار الرئيسي التالي بعد 2.10.0 (على الأرجح 2.11.0 أو 3.0.0)
- **الحد الأدنى الحالي**: Java 8
- **الإجراء المطلوب**: الاستعداد للترحيل إلى Java 17
- **الجدول الزمني**: سيتم الإعلان عنه مع ملاحظات الإصدار

### الميزات التي تمت إزالتها

#### بروتوكول BOB (أندرويد)

- **تمت الإزالة**: الإصدار 0.9.41
- **المنصة**: Android فقط
- **البديل**: بروتوكول SAM أو I2CP
- **سطح المكتب**: لا يزال BOB متاحًا على منصات سطح المكتب

### عمليات الترحيل الموصى بها

1. **المصادقة**: الانتقال من MD5 إلى SHA-256 لمصادقة الملخص
2. **تنسيق التكوين**: الانتقال إلى بنية مجلدات منفصلة للعملاء وtunnels
3. **وقت تشغيل Java**: التخطيط للترقية إلى Java 17 قبل الإصدار الرئيسي التالي
4. **تكامل Tor**: لا تقم بتوجيه I2P عبر عقد الخروج في Tor

---

## المراجع

### التوثيق الرسمي

- [مواصفة تهيئة I2P](/docs/specs/configuration/) - المواصفة الرسمية لصيغة ملف التهيئة
- [مواصفة ملحق I2P](/docs/specs/plugin/) - تهيئة الملحق وحزمه
- [البنى المشتركة في I2P - تعيين الأنواع](/docs/specs/common-structures/#type-mapping) - صيغة تسلسل بيانات البروتوكول
- [صيغة خصائص Java](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) - مواصفة الصيغة الأساسية

### الشيفرة المصدرية

- [مستودع I2P Java Router](https://github.com/i2p/i2p.i2p) - مرآة GitHub
- [Gitea الخاص بمطوري I2P](https://i2pgit.org/I2P_Developers/i2p.i2p) - المستودع الرسمي للشيفرة المصدرية لـ I2P
- [DataHelper.java](https://github.com/i2p/i2p.i2p/blob/master/core/java/src/net/i2p/data/DataHelper.java) - تنفيذ عمليات I/O (إدخال/إخراج) لملفات التهيئة

### موارد المجتمع

- [منتدى I2P](https://i2pforum.net/) - نقاشات المجتمع النشطة ودعم
- [موقع I2P](/) - الموقع الرسمي للمشروع

### توثيق واجهة برمجة التطبيقات

- [DataHelper JavaDoc](https://i2pplus.github.io/javadoc/net/i2p/data/DataHelper.html) - توثيق واجهة برمجة التطبيقات (API) لأساليب ملف التهيئة

### حالة المواصفة

- **آخر تحديث للمواصفة**: يناير 2023 (الإصدار 0.9.57)
- **الإصدار الحالي لـ I2P**: 2.10.0 (سبتمبر 2025)
- **الدقة التقنية**: لا تزال المواصفة دقيقة حتى الإصدار 2.10.0 (لا تغييرات كاسرة للتوافق)
- **الصيانة**: مستند حي يُحدّث عند تعديل تنسيق الإعدادات
