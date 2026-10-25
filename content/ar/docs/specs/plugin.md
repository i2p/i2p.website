---
title: "مواصفات الإضافة"
description: "قواعد تغليف .xpi2p / .su3 لإضافات I2P"
slug: "plugin"
aliases:
  - "/ar/plugin_spec"
  - "/ar/plugin_spec/"
lastUpdated: "2022-01"
accurateFor: "0.9.53"
type: docs
---

## نظرة عامة

تحدد هذه الوثيقة تنسيق ملف .xpi2p (مثل .xpi في Firefox)، ولكن مع ملف وصف plugin.config بسيط بدلاً من ملف XML install.rdf. يُستخدم تنسيق الملف هذا لكل من عمليات تثبيت الإضافات الأولية وتحديثات الإضافات.

بالإضافة إلى ذلك، توفر هذه الوثيقة نظرة عامة مختصرة حول كيفية تثبيت router للإضافات، والسياسات والإرشادات لمطوري الإضافات.

تنسيق ملف .xpi2p الأساسي هو نفس تنسيق ملف i2pupdate.sud (التنسيق المستخدم لتحديثات router)، لكن المثبت سيسمح للمستخدم بتثبيت الإضافة حتى لو لم يكن يعرف مفتاح الموقع بعد.

اعتباراً من الإصدار 0.9.15، يتم دعم تنسيق ملف SU3 وهو المفضل. يمكّن هذا التنسيق من استخدام مفاتيح توقيع أقوى.

> **ملاحظة:** لا نوصي بتوزيع الإضافات بتنسيق xpi2p بعد الآن. استخدم تنسيق su3.

هيكل المجلدات المعياري سيسمح للمستخدمين بتثبيت الأنواع التالية من الإضافات:

- تطبيقات الويب للوحة التحكم
- موقع eepsite جديد مع cgi-bin وتطبيقات الويب
- قوالب وحة التحكم
- ترجمات وحة التحكم
- برامج Java
- برامج Java في JVM منفصلة
- أي سكريبت shell أو برنامج

يقوم الـ plugin بتثبيت جميع ملفاته في `~/.i2p/plugins/name/` (`%APPDIR%\I2P\plugins\name\` على Windows). سيمنع المثبت التثبيت في أي مكان آخر، رغم أن الـ plugin يمكنه الوصول إلى المكتبات في أماكن أخرى أثناء التشغيل.

يجب اعتبار هذا فقط كطريقة لتسهيل التثبيت وإلغاء التثبيت والترقية، وتقليل التعارضات الأساسية بين الإضافات.

لا يوجد نموذج أمان فعلياً بمجرد تشغيل البرنامج المساعد. يعمل البرنامج المساعد في نفس JVM وبنفس الأذونات مثل router، ولديه وصول كامل إلى نظام الملفات والـ router وتنفيذ البرامج الخارجية وغيرها.

## التفاصيل

foo.xpi2p هو ملف تحديث موقع (sud) يحتوي على ما يلي:

رأس .sud قياسي مُلحق بداية ملف zip، يحتوي على ما يلي:

```text
40-byte DSA signature
16-byte plugin version in UTF-8, padded with trailing zeroes if necessary
```
ملف Zip يحتوي على التالي:

### ملف plugin.config

هذا الملف مطلوب. إنه ملف تكوين I2P معياري، يحتوي على الخصائص التالية:

#### الخصائص المطلوبة

الخصائص الأربع التالية مطلوبة. يجب أن تكون الثلاث الأولى مطابقة لتلك الموجودة في المكون الإضافي المثبت لمكون إضافي محديث.

-   **name** - سيتم تثبيته في اسم المجلد هذا. بالنسبة للإضافات الأصلية، قد ترغب في أسماء منفصلة في حزم مختلفة - foo-windows و foo-linux، على سبيل المثال.
-   **key** - مفتاح DSA العام كـ 172 حرف B64 منتهي بـ '='. احذف هذا لتنسيق SU3.
-   **signer** - yourname@mail.i2p مُوصى به
-   **version** - يجب أن يكون في تنسيق يمكن لـ VersionComparator تحليله، مثل 1.2.3-4. 16 بايت كحد أقصى (يجب أن يطابق إصدار sud). فواصل الأرقام الصحيحة هي '.', '-', و '_'. يجب أن يكون هذا أكبر من الموجود في الإضافة المُثبتة لإضافة التحديث.

#### خصائص العرض

قيم الخصائص التالية تظهر في /configplugins في وحدة تحكم الموجه إذا كانت موجودة:

-   **date** - Java time - long int
-   **author** - `yourname@mail.i2p` مُوصى به
-   **websiteURL** - `http://foo.i2p/`
-   **updateURL** - `http://foo.i2p/foo.xpi2p` - سيفحص مدقق التحديثات البايتات 41-56 في هذا الرابط لتحديد ما إذا كان إصدار أحدث متاحاً. اعتباراً من 1.7.0 (0.9.53)، من الممكن استخدام المتغيرات `$OS` و `$ARCH` في الرابط. غير مُوصى به. لا تستخدم هذا إلا إذا كنت قد وزعت plugins بصيغة xpi2p مسبقاً.
-   **updateURL.su3** - `http://foo.i2p/foo.su3` - موقع ملف التحديث بصيغة su3، اعتباراً من 0.9.15. اعتباراً من 1.7.0 (0.9.53)، من الممكن استخدام المتغيرات `$OS` و `$ARCH` في الرابط.
-   **description** - باللغة الإنجليزية
-   **description_xx** - للغة xx
-   **license** - رخصة الـ plugin
-   **disableStop=true** - القيمة الافتراضية false. إذا كانت true، فلن يتم إظهار زر الإيقاف. استخدم هذا إذا لم تكن هناك تطبيقات ويب ولا عملاء مع stopargs.

#### خصائص رابط شريط ملخص وحدة التحكم

الخصائص التالية تُستخدم لإضافة رابط على شريط ملخص وحدة التحكم:

-   **consoleLinkName** - سيتم إضافته إلى شريط الملخص
-   **consoleLinkName_xx** - للغة xx
-   **consoleLinkURL** - /appname/index.jsp
-   **consoleLinkTooltip** - مدعوم اعتباراً من 0.7.12-6
-   **consoleLinkTooltip_xx** - اللغة xx اعتباراً من 0.7.12-6

#### خصائص أيقونة وحدة التحكم

يمكن استخدام الخصائص الاختيارية التالية لإضافة أيقونة مخصصة في وحدة التحكم:

-   **console-icon** - مدعوم اعتباراً من 0.9.20. فقط لتطبيقات الويب. مسار لصورة 32x32، مثل /icon.png. اعتباراً من 1.7.0 (API 0.9.53)، إذا تم تحديد consoleLinkURL، فإن المسار يكون نسبة إلى ذلك الرابط. وإلا فهو نسبة إلى اسم تطبيق الويب. ينطبق على جميع تطبيقات الويب في الإضافة.
-   **icon-code** - مدعوم اعتباراً من 0.9.25. يوفر أيقونة وحدة التحكم للإضافات بدون موارد ويب. سلسلة B64 تُنتج عن طريق استدعاء `net.i2p.data.Base64 encode FILE` على ملف صورة png بحجم 32x32.

#### خصائص المثبت

الخصائص التالية مستخدمة من قبل مثبت الإضافة:

-   **type** - app/theme/locale/webapp/... (غير مُنفذ، ربما غير ضروري)
-   **min-i2p-version** - الحد الأدنى لإصدار I2P المطلوب لهذا المكون الإضافي
-   **max-i2p-version** - الحد الأقصى لإصدار I2P الذي سيعمل عليه هذا المكون الإضافي
-   **min-java-version** - الحد الأدنى لإصدار Java المطلوب لهذا المكون الإضافي
-   **min-jetty-version** - مدعوم اعتباراً من 0.8.13، استخدم 6 لتطبيقات Jetty 6
-   **max-jetty-version** - مدعوم اعتباراً من 0.8.13، استخدم 5.99999 لتطبيقات Jetty 5
-   **required-platform-OS** - غير مُنفذ - ربما سيتم عرضه فقط، وليس التحقق منه
-   **other-requirements** - غير مُنفذ، مثل python x.y - لا يتم التحقق منه بواسطة أداة التثبيت، يتم عرضه للمستخدم فقط
-   **dont-start-at-install=true** - الافتراضي false. لن يبدأ المكون الإضافي عند تثبيته أو تحديثه.
-   **router-restart-required=true** - الافتراضي false. هذا لا يعيد تشغيل router أو المكون الإضافي عند التحديث، بل يُعلم المستخدم فقط بأن إعادة التشغيل مطلوبة.
-   **update-only=true** - الافتراضي false. إذا كان true، سيفشل إذا لم يكن هناك تثبيت موجود.
-   **install-only=true** - الافتراضي false. إذا كان true، سيفشل إذا كان هناك تثبيت موجود.
-   **min-installed-version** - للتحديث، إذا كان هناك تثبيت موجود
-   **max-installed-version** - للتحديث، إذا كان هناك تثبيت موجود
-   **depends=plugin1,plugin2,plugin3** - غير مُنفذ
-   **depends-version=0.3.4,,5.6.7** - غير مُنفذ

#### خصائص الترجمة

-   **langs=xx,yy,Klingon,...** - (غير مُنفذ) (yy هو علم الدولة)

### دلائل وملفات التطبيق

كل واحد من الأدلة أو الملفات التالية اختياري، ولكن يجب أن يكون هناك شيء ما وإلا فلن يقوم بأي عمل:

**console/**

-   **locale/** - فقط ملفات jar التي تحتوي على حزم موارد جديدة (ترجمات) للتطبيقات في تثبيت I2P الأساسي. يجب وضع الحزم الخاصة بهذا المكون الإضافي داخل console/webapp/foo.war أو lib/foo.jar
-   **themes/** - سمات جديدة لوحة تحكم الـ router. ضع كل سمة في دليل فرعي.
-   **webapps/** - (انظر الملاحظات المهمة أدناه حول webapps) ملفات .wars - سيتم تشغيلها وقت التثبيت إلا إذا تم تعطيلها في webapps.config. لا يجب أن يكون اسم war مطابقًا لاسم المكون الإضافي. لا تكرر أسماء war في تثبيت I2P الأساسي.
-   **webapps.config** - نفس تنسيق webapps.config الخاص بالـ router. يُستخدم أيضًا لتحديد ملفات jar إضافية في $PLUGIN/lib/ أو $I2P/lib لمسار فئة webapp، مع `webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar`

> **ملاحظة:** قبل الإصدار 1.7.0 (API 0.9.53)، كان يتم تحميل سطر classpath فقط إذا كان warname مطابقاً لاسم الإضافة. اعتباراً من API 0.9.53، ستعمل إعدادات classpath لأي warname.

> **ملاحظة:** قبل إصدار router 0.7.12-9، كان الـ router يبحث عن `plugin.warname.startOnLoad` بدلاً من `webapps.warname.startOnLoad`. للتوافق مع إصدارات الـ router الأقدم، يجب على البرنامج المساعد الذي يرغب في تعطيل ملف war أن يتضمن كلا السطرين.

**eepsite/**

(راجع الملاحظات المهمة أدناه حول مواقع eepsite)

-   **cgi-bin/**
-   **docroot/**
-   **logs/**
-   **webapps/**
-   **jetty.xml** - سيتعين على المثبت القيام بتبديل المتغيرات هنا لتعيين المسار. موقع واسم هذا الملف لا يهم حقاً، طالما تم تعيينه في clients.config - قد يكون من الأنسب أن يكون في مستوى أعلى من هنا.

**lib/**

ضع أي ملفات jar هنا، وحددها في سطر classpath في console/webapps.config و/أو clients.config

### ملف clients.config

هذا الملف اختياري، ويحدد العملاء الذين سيتم تشغيلهم عند بدء تشغيل الإضافة. يستخدم نفس تنسيق ملف clients.config الخاص بالموجه. راجع مواصفات ملف تكوين clients.config للحصول على مزيد من المعلومات حول التنسيق والتفاصيل المهمة حول كيفية بدء وإيقاف العملاء.

-   **clientApp.0.stopargs=foo bar stop baz** - إذا كان موجوداً، سيتم استدعاء الفئة بهذه المعاملات لإيقاف العميل. يتم استدعاء جميع مهام الإيقاف بدون تأخير. ملاحظة: لا يمكن للـ router معرفة ما إذا كانت عملاؤك غير المُدارين يعملون أم لا.
-   **clientApp.0.uninstallargs=foo bar uninstall baz** - إذا كان موجوداً، سيتم استدعاء الفئة بهذه المعاملات قبل حذف $PLUGIN مباشرة. يتم استدعاء جميع مهام إلغاء التثبيت بدون تأخير.
-   **clientApp.0.classpath=$I2P/lib/foo.bar,$PLUGIN/lib/bar.jar** - سيقوم مشغل البرنامج المساعد بإجراء استبدال المتغيرات في سطور args و stopargs كما يلي:
    -   `$I2P` - دليل تثبيت I2P الأساسي
    -   `$CONFIG` - دليل إعداد I2P (عادة ~/.i2p)
    -   `$PLUGIN` - دليل تثبيت هذا البرنامج المساعد (عادة ~/.i2p/plugins/appname)
    -   `$OS` - نظام التشغيل المضيف في الشكل `windows`، `linux`، `mac`
    -   `$ARCH` - معمارية المضيف في الشكل `386`، `amd64`، `arm64`

(انظر الملاحظات المهمة أدناه حول تشغيل shell scripts أو البرامج الخارجية)

## مهام مثبت الإضافات

هذا يسرد ما يحدث عند تثبيت إضافة بواسطة I2P.

1.  يتم تحميل ملف .xpi2p.
2.  يتم التحقق من توقيع .sud مقابل المفاتيح المخزنة. اعتباراً من الإصدار 0.9.14.1، إذا لم يكن هناك مفتاح مطابق، فشل التثبيت، ما لم يتم تعيين خاصية router متقدمة للسماح بجميع المفاتيح.
3.  التحقق من سلامة ملف zip.
4.  استخراج ملف plugin.config.
5.  التحقق من إصدار I2P، للتأكد من أن المكون الإضافي سيعمل.
6.  التحقق من أن تطبيقات الويب لا تكرر تطبيقات $I2P الموجودة.
7.  إيقاف المكون الإضافي الموجود (إن وجد).
8.  التحقق من أن دليل التثبيت غير موجود بعد إذا كان update=false، أو السؤال للكتابة فوقه.
9.  التحقق من أن دليل التثبيت موجود إذا كان update=true، أو السؤال لإنشائه.
10. إلغاء ضغط المكون الإضافي إلى appDir/plugins/name/
11. إضافة المكون الإضافي إلى plugins.config

## مهام بدء البرنامج المساعد

هذا يسرد ما يحدث عند بدء تشغيل الإضافات. أولاً، يتم فحص plugins.config لمعرفة الإضافات التي تحتاج إلى بدء التشغيل. لكل إضافة:

1.  فحص clients.config، وتحميل وبدء كل عنصر (إضافة ملفات jar المكونة إلى classpath).
2.  فحص console/webapp و console/webapp.config. تحميل وبدء العناصر المطلوبة (إضافة ملفات jar المكونة إلى classpath).
3.  إضافة console/locale/foo.jar إلى مسار الترجمة classpath إذا كان موجوداً.
4.  إضافة console/theme إلى مسار البحث عن الثيمات إذا كان موجوداً.
5.  إضافة رابط شريط الملخص.

## ملاحظات تطبيق الويب للوحة التحكم

يجب على تطبيقات الويب الخاصة بوحدة التحكم والتي تحتوي على مهام تعمل في الخلفية أن تنفذ ServletContextListener (راجع seedless أو i2pbote كأمثلة)، أو تعيد تعريف destroy() في servlet، حتى يمكن إيقافها. اعتباراً من إصدار router 0.7.12-3، سيتم دائماً إيقاف تطبيقات ويب وحدة التحكم قبل إعادة تشغيلها، لذا لا تحتاج للقلق بشأن تشغيل عدة نسخ، طالما أنك تفعل ذلك. أيضاً اعتباراً من إصدار router 0.7.12-3، سيتم إيقاف تطبيقات ويب وحدة التحكم عند إغلاق router.

لا تحزم ملفات jar الخاصة بالمكتبة في تطبيق الويب؛ ضعها في lib/ وضع classpath في webapps.config. عندها يمكنك إنشاء إضافات تثبيت وتحديث منفصلة، حيث لا تحتوي إضافة التحديث على ملفات jar الخاصة بالمكتبة.

لا تقم أبداً بتجميع ملفات Jetty أو Tomcat أو servlet jars في الإضافة الخاصة بك، حيث قد تتعارض مع الإصدار الموجود في تثبيت I2P. احرص على عدم تجميع أي مكتبات متعارضة.

لا تشمل ملفات .java أو .jsp؛ وإلا فإن Jetty سيعيد تجميعها عند التثبيت، مما سيزيد من وقت بدء التشغيل. وبينما معظم تثبيتات I2P ستحتوي على مترجم Java وJSP يعمل في classpath، إلا أن هذا غير مضمون، وقد لا يعمل في جميع الحالات.

في الوقت الحالي، تطبيق الويب الذي يحتاج إلى إضافة ملفات classpath في $PLUGIN يجب أن يكون له نفس اسم المكون الإضافي. على سبيل المثال، تطبيق ويب في المكون الإضافي foo يجب أن يُسمى foo.war.

بينما يدعم I2P إصدار Servlet 3.0 منذ إصدار I2P 0.9.30، فإنه لا يدعم مسح التعليقات التوضيحية لـ @WebContent (لا يوجد ملف web.xml). ستكون هناك حاجة إلى عدة ملفات jar إضافية لوقت التشغيل، ولا نوفر تلك في التثبيت القياسي. اتصل بمطوري I2P إذا كنت بحاجة إلى دعم لـ @WebContent.

## ملاحظات Eepsite

ليس من الواضح كيفية تثبيت مكون إضافي على eepsite موجود. ال router ليس لديه اتصال مع ال eepsite، وقد يكون يعمل أو لا يعمل، وقد يكون هناك أكثر من واحد. الأفضل هو بدء مثيل Jetty الخاص بك ومثيل I2PTunnel، لإنشاء eepsite جديد تماماً.

يمكنه إنشاء I2PTunnel جديد (إلى حد ما مثل ما يفعله i2ptunnel CLI)، ولكنه لن يظهر في واجهة i2ptunnel الرسومية بالطبع، فهذا مثيل مختلف. لكن هذا لا بأس به. عندها يمكنك بدء وإيقاف i2ptunnel و jetty معًا.

لذا لا تعتمد على أن الـ router سيدمج هذا تلقائياً مع eepsite موجود. من المحتمل ألا يحدث ذلك. ابدأ I2PTunnel و Jetty جديدين من clients.config. أفضل الأمثلة على ذلك هي إضافات zzzot و pebble.

كيفية الحصول على استبدال المسار في jetty.xml؟ راجع إضافات zzzot و pebble للأمثلة.

## ملاحظات بدء/إيقاف العميل

اعتباراً من الإصدار 0.9.4، يدعم الـ router عملاء الإضافات "المُدارة". يتم إنشاء وتشغيل عملاء الإضافات المُدارة بواسطة `ClientAppManager`. يحتفظ ClientAppManager بمرجع للعميل ويتلقى تحديثات حول حالة العميل. عملاء الإضافات المُدارة مُفضلة، حيث أنه من الأسهل بكثير تطبيق تتبع الحالة وبدء تشغيل العميل وإيقافه. كما أنه من الأسهل بكثير تجنب المراجع الثابتة في كود العميل والتي يمكن أن تؤدي إلى استخدام مفرط للذاكرة بعد إيقاف العميل. انظر مواصفات ملف التكوين clients.config للحصول على مزيد من المعلومات حول كتابة عميل مُدار.

بالنسبة لعملاء البرنامج المساعد "غير المُدارين"، لا يملك الـ router أي طريقة لمراقبة حالة العملاء الذين يتم تشغيلهم عبر clients.config. يجب على مؤلف البرنامج المساعد التعامل مع استدعاءات التشغيل أو الإيقاف المتعددة بسلاسة، إن أمكن ذلك، من خلال الاحتفاظ بجدول حالة ثابت، أو استخدام ملفات PID، إلخ. تجنب التسجيل أو الاستثناءات عند التشغيل أو الإيقاف المتعدد. هذا ينطبق أيضاً على استدعاء الإيقاف دون تشغيل مسبق. اعتباراً من إصدار الـ router 0.7.12-3، سيتم إيقاف البرامج المساعدة عند إغلاق الـ router، مما يعني أن جميع العملاء الذين لديهم stopargs في clients.config سيتم استدعاؤهم، سواء تم تشغيلهم مسبقاً أم لا.

## ملاحظات حول Shell Script والبرامج الخارجية

لتشغيل shell scripts أو البرامج الخارجية الأخرى، اكتب فئة Java صغيرة تتحقق من نوع نظام التشغيل، ثم تشغل ShellCommand على ملف .bat أو .sh الذي تقدمه. تم إضافة حل عام لهذا في I2P 1.7.0/0.9.53، وهو "ShellService" الذي يقوم بتتبع حالة أمر واحد ويتواصل مع ClientAppManager.

البرامج الخارجية لن تتوقف عند توقف الـ router، وستبدأ نسخة ثانية عند تشغيل الـ router. يمكن عادة التخفيف من هذه المشكلة باستخدام ShellService لتتبع الحالة. إذا كان ذلك غير مناسب لحالة الاستخدام الخاصة بك، يمكنك كتابة فئة wrapper أو نص shell script يقوم بالتخزين المعتاد للـ PID في ملف PID، والتحقق منه عند البدء.

## إرشادات البرمجيات الإضافية الأخرى

-   راجع فرع monotone الخاص بـ i2p.scripts أو أي من الإضافات النموذجية في صفحة zzz للحصول على shell script للـ makeplugin.sh. هذا يؤتمت معظم المهام لإنتاج المفاتيح، وإنشاء ملف su3 للإضافة، والتحقق. يجب عليك دمج هذا الـ script في عملية بناء الإضافة الخاصة بك.
-   Pack200 للـ jars والـ wars مُوصى به بشدة للإضافات، فهو يقلل حجم الإضافات عمومًا بنسبة 60-65%. راجع أي من الإضافات النموذجية في صفحة zzz كمثال. إلغاء حزم Pack200 مدعوم على routers الإصدار 0.7.11-5 أو أعلى، وهو في الأساس جميع routers التي تدعم الإضافات.
-   يجب ألا تحاول الإضافات الكتابة في أي مكان في $I2P لأنه قد يكون للقراءة فقط، وهذا ليس سياسة جيدة على أي حال.
-   يمكن للإضافات الكتابة في $CONFIG لكن الاحتفاظ بالملفات في $PLUGIN فقط مُوصى به. جميع الملفات في $PLUGIN ستُحذف عند إلغاء التثبيت.
-   $CWD قد يكون في أي مكان؛ لا تفترض أنه في مكان معين، لا تحاول قراءة أو كتابة ملفات نسبية إلى $CWD. بالنسبة لـ ShellService، فهو دائمًا نفس $PLUGIN.
-   يجب على برامج Java معرفة مكانها باستخدام directory getters في I2PAppContext.
-   دليل الإضافة هو `I2PAppContext.getGlobalContext().getAppDir().getAbsolutePath() + "/plugins/" + appname`، أو ضع معامل $PLUGIN في سطر args في clients.config.
-   جميع ملفات الإعدادات يجب أن تكون UTF-8.
-   للتشغيل في JVM منفصل، استخدم ShellCommand مع `java -cp foo:bar:baz my.main.class arg1 arg2 arg3`.
-   كبديل لـ stopargs في clients.config، قد يُسجل عميل Java خطاف إيقاف التشغيل باستخدام `I2PAppContext.addShutdownTask()`. لكن هذا لن يوقف إضافة عند الترقية، لذا stopargs مُوصى به. أيضًا، اضبط جميع threads المُنشأة على وضع daemon.
-   لا تشمل classes مكررة لتلك الموجودة في التثبيت المعياري. مدد الـ classes إذا لزم الأمر.
-   احذر من تعريفات classpath المختلفة في wrapper.config بين التثبيتات القديمة والجديدة.
-   سترفض العملاء المفاتيح المكررة بأسماء مفاتيح مختلفة، وأسماء المفاتيح المكررة بمفاتيح مختلفة، ومفاتيح أو أسماء مفاتيح مختلفة في حزم الترقية. احم مفاتيحك. أنتجها مرة واحدة فقط.
-   لا تعدل ملف plugin.config في وقت التشغيل لأنه سيُستبدل عند الترقية. استخدم ملف إعدادات مختلف في الدليل لحفظ إعدادات وقت التشغيل.
-   عمومًا، يجب ألا تتطلب الإضافات الوصول إلى $I2P/lib/router.jar. لا تصل إلى router classes، إلا إذا كنت تفعل شيئًا خاصًا.
-   نظرًا لأن كل إصدار يجب أن يكون أعلى من الذي قبله، يمكنك تحسين script البناء الخاص بك لإضافة رقم بناء إلى نهاية الإصدار.
-   يجب ألا تستدعي الإضافات أبدًا `System.exit()`.
-   يرجى احترام التراخيص من خلال تلبية متطلبات الترخيص لأي برنامج تُرفقه.
-   يضبط router المنطقة الزمنية للـ JVM على UTC. إذا احتاجت إضافة لمعرفة المنطقة الزمنية الفعلية للمستخدم، فهي مُخزنة بواسطة router في خاصية I2PAppContext `i2p.systemTimeZone`.

## مسارات الفئات

يمكن افتراض أن ملفات jar التالية في $I2P/lib موجودة في classpath الأساسي لجميع تثبيتات I2P، بغض النظر عن عمر التثبيت الأصلي أو حداثته.

جميع واجهات برمجة التطبيقات العامة الحديثة في ملفات i2p jar تحتوي على رقم الإصدار المحدد في Javadocs. إذا كان المكون الإضافي الخاص بك يتطلب ميزات معينة متوفرة فقط في الإصدارات الحديثة، تأكد من تعيين الخصائص min-i2p-version أو min-jetty-version أو كلاهما في ملف plugin.config.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">addressbook.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription and blockfile support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need; use the NamingService interface</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-logging.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Apache Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since release 0.9.30</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-el.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSP Expressions Language</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with JSPs that use EL. As of release 0.9.30 (Jetty 9), this contains the EL 3.0 API.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with HTTP or other servers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-compiler.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">nothing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since Jetty 6 (release 0.9)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-runtime.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper Compiler and Runtime, and some Tomcat utils</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">javax.servlet.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs. As of release 0.9.30 (Jetty 9), this contains the Servlet 3.1 and JSP 2.3 APIs.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jbigi.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Binaries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jetty-i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Support utilities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Some plugins will need. As of release 0.9.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">mstreaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">org.mortbay.jetty.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty Base</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins starting their own Jetty instance will need. Recommended way of starting Jetty is with <code>net.i2p.jetty.JettyStart</code> in jetty-i2p.jar.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins using router context will need; most will not</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">routerconsole.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need, not a public API</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">sam.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">streaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming Implementation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">URL Launcher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins should not need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray4j.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Systray</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need. As of 0.9.26, no longer present.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">wrapper.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
  </tbody>
</table>
يمكن افتراض وجود ملفات jar التالية في `$I2P/lib` لجميع تثبيتات I2P، بغض النظر عن قدم أو حداثة التثبيت الأصلي، ولكنها ليست بالضرورة في classpath:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jstl.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">standard.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
  </tbody>
</table>
أي شيء غير مدرج أعلاه قد لا يكون موجودًا في classpath الخاص بالجميع، حتى لو كان لديك في classpath في إصدارك من i2p. إذا كنت تحتاج إلى أي jar غير مدرج أعلاه، أضف `$I2P/lib/foo.jar` إلى classpath المحدد في `clients.config` أو `webapps.config` في الإضافة الخاصة بك.

سابقاً، كان إدخال classpath المحدد في clients.config يُضاف إلى classpath لكامل JVM. ومع ذلك، اعتباراً من الإصدار 0.7.13-3، تم إصلاح هذا باستخدام class loaders، والآن، كما كان مقصوداً أصلاً، فإن classpath المحدد في clients.config هو فقط للخيط المحدد. لذلك، حدد classpath الكامل المطلوب لكل عميل.

## ملاحظات إصدار Java

يتطلب I2P إصدار Java 7 منذ الإصدار 0.9.24 (يناير 2016). كان I2P يتطلب Java 6 منذ الإصدار 0.9.12 (أبريل 2014). أي مستخدمين لـ I2P على الإصدار الأحدث يجب أن يشغلوا JVM إصدار 1.7 (7.0).

إذا كان المكون الإضافي الخاص بك **لا يتطلب الإصدار 1.7**:

-   تأكد من أن جميع ملفات java و jsp مُجمعة باستخدام source="1.6" target="1.6".
-   تأكد من أن جميع ملفات jar للمكتبات المدمجة مخصصة أيضاً للإصدار 1.6 أو أقل.

إذا كان البرنامج المساعد الخاص بك **يتطلب 1.7**:

-   لاحظ ذلك في صفحة التحميل الخاصة بك.
-   أضف min-java-version=1.7 إلى plugin.config الخاص بك

في جميع الأحوال، يجب عليك **حتماً** تعيين bootclasspath عند الترجمة باستخدام Java 8 لمنع تعطل وقت التشغيل.

## تعطل JVM عند التحديث

ملاحظة - يجب أن يكون كل هذا مُصحح الآن.

لدى JVM ميل للتعطل عند تحديث ملفات jar في إضافة إذا كانت تلك الإضافة قيد التشغيل منذ بدء تشغيل I2P (حتى لو تم إيقاف الإضافة لاحقاً). ربما تم إصلاح هذا مع تطبيق class loader في الإصدار 0.7.13-3، لكن قد يكون لم يتم إصلاحه.

الأكثر أماناً هو تصميم plugin الخاص بك مع ملف jar داخل ملف war (لتطبيق ويب)، أو طلب إعادة تشغيل بعد التحديث، أو عدم تحديث ملفات jar في plugin الخاص بك.

نظراً لطريقة عمل محملات الفئات داخل تطبيق الويب، قد يكون من الآمن وجود ملفات jar خارجية إذا قمت بتحديد مسار الفئات في webapps.config. مطلوب المزيد من الاختبار للتحقق من ذلك. لا تحدد مسار الفئات باستخدام عميل "وهمي" في clients.config إذا كان مطلوباً فقط لتطبيق ويب - استخدم webapps.config بدلاً من ذلك.

الأقل أماناً، والذي يبدو أنه مصدر معظم الأعطال، هو العملاء الذين لديهم plugin jars محددة في classpath في clients.config.

لا يجب أن يكون أي من هذا مشكلة عند التثبيت الأولي - لا يجب أبداً أن تحتاج إلى إعادة تشغيل للتثبيت الأولي للإضافة.

## المراجع

-   [مواصفات ملف التكوين](/docs/specs/configuration)
-   [تشفير DSA](/docs/specs/cryptography#DSA)
-   [مواصفات التحديثات](/docs/specs/updates)
