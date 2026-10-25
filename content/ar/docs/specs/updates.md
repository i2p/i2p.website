---
title: "مواصفات تحديث البرمجيات"
description: "مواصفات آلية تحديث برنامج I2P وتنسيق ملف SU3 وخلاصة الأخبار"
slug: "updates"
aliases:
  - "/ar/updates"
  - "/ar/updates/"
category: "التصميم"
lastUpdated: "2025-04"
accurateFor: "0.9.65"
---

## نظرة عامة

يستخدم I2P نظاماً بسيطاً وآمناً للتحديث التلقائي للبرامج. تقوم وحدة تحكم router بسحب ملف الأخبار بشكل دوري من عنوان URL خاص بـ I2P قابل للتكوين. يوجد عنوان URL احتياطي مُبرمج مسبقاً يشير إلى موقع المشروع الإلكتروني، في حالة تعطل مضيف أخبار المشروع الافتراضي.

يتم عرض محتويات ملف الأخبار في الصفحة الرئيسية لوحة تحكم router. بالإضافة إلى ذلك، يحتوي ملف الأخبار على رقم الإصدار الأحدث من البرنامج. إذا كان الإصدار أعلى من رقم إصدار router، فسيعرض إشارة للمستخدم بأن هناك تحديث متاح.

يمكن للـ router اختيارياً تحميل الإصدار الجديد، أو تحميله وتثبيته، إذا تم تكوينه للقيام بذلك.

## مواصفات ملف الأخبار القديم

تم استبدال هذا التنسيق بتنسيق أخبار su3 اعتباراً من الإصدار 0.9.17.

قد يحتوي ملف news.xml على العناصر التالية:

```
<i2p.news date="$Date: 2010-01-22 00:00:00 $" />
<i2p.release version="0.7.14" date="2010/01/22" minVersion="0.6" />
```
المعاملات في إدخال i2p.release كما يلي. جميع المفاتيح غير حساسة لحالة الأحرف. يجب وضع جميع القيم بين علامتي اقتباس مزدوجتين.

**date** : تاريخ إصدار إصدار الـ router. غير مستخدم. التنسيق غير محدد.

**minJavaVersion** : الحد الأدنى من إصدار Java المطلوب لتشغيل الإصدار الحالي. اعتباراً من الإصدار 0.9.9.

**minVersion** : الحد الأدنى لإصدار الـ router المطلوب للتحديث إلى الإصدار الحالي. إذا كان الـ router أقدم من هذا، يجب على المستخدم (يدوياً؟) التحديث إلى إصدار وسيط أولاً. اعتباراً من الإصدار 0.9.9.

**su3Clearnet** : واحد أو أكثر من عناوين URL لـ HTTP حيث يمكن العثور على ملف التحديث .su3 على الشبكة العادية (غير I2P). يجب فصل عناوين URL المتعددة بمسافة أو فاصلة. اعتباراً من الإصدار 0.9.9.

**su3SSL** : واحد أو أكثر من عناوين HTTPS URLs حيث يمكن العثور على ملف التحديث .su3 على الشبكة العادية (غير I2P). يجب فصل عدة URLs بمسافة أو فاصلة. اعتباراً من الإصدار 0.9.9.

**sudTorrent** : رابط المغناطيس للتورنت .sud (غير pack200) للتحديث. اعتباراً من الإصدار 0.9.4.

**su2Torrent** : رابط magnet لملف التورنت .su2 (pack200) الخاص بالتحديث. اعتباراً من الإصدار 0.9.4.

**su3Torrent** : رابط المغناطيس لتورنت .su3 (التنسيق الجديد) للتحديث. اعتباراً من الإصدار 0.9.9.

**version** : مطلوب. أحدث إصدار router متاح حالياً.

يمكن تضمين العناصر داخل تعليقات XML لمنع تفسيرها من قبل المتصفحات. عنصر i2p.release والإصدار مطلوبان. جميع العناصر الأخرى اختيارية. ملاحظة: بسبب قيود المحلل يجب أن يكون العنصر بأكمله على سطر واحد.

## مواصفات ملف التحديث

اعتباراً من الإصدار 0.9.9، سيستخدم ملف التحديث الموقع، المسمى i2pupdate.su3، تنسيق الملف "su3" المحدد أدناه. سيستخدم الموقعون المعتمدون للإصدارات مفاتيح RSA بحجم 4096 بت. يتم توزيع شهادات المفاتيح العامة X.509 لهؤلاء الموقعين في حزم تثبيت router. قد تحتوي التحديثات على شهادات لموقعين جدد معتمدين، و/أو تحتوي على قائمة بالشهادات المراد حذفها للإلغاء.

## مواصفات ملف التحديث القديم

هذا التنسيق قديم منذ الإصدار 0.9.9.

ملف التحديث الموقع، والذي يُسمى تقليدياً i2pupdate.sud، هو ببساطة ملف مضغوط بتنسيق zip مع رأس (header) مكون من 56 بايت مُضاف في المقدمة. يحتوي الرأس على:

- توقيع DSA بحجم 40 بايت [Signature](/docs/specs/common-structures#signature)
- إصدار I2P بحجم 16 بايت بترميز UTF-8، مبطن بأصفار في النهاية إذا لزم الأمر

التوقيع يغطي أرشيف zip فقط - وليس الإصدار المُضاف في المقدمة. يجب أن يطابق التوقيع أحد مفاتيح DSA [SigningPublicKey](/docs/specs/common-structures#signingpublickey) المُكوَّنة في router، والذي يحتوي على قائمة افتراضية مُدمجة من مفاتيح مديري إصدارات المشروع الحاليين.

لأغراض مقارنة الإصدارات، تحتوي حقول الإصدار على [0-9]*، وفواصل الحقول هي '-' و '_' و '.'، ويتم تجاهل جميع الأحرف الأخرى.

اعتباراً من الإصدار 0.8.8، يجب أيضاً تحديد الإصدار كتعليق في ملف zip بترميز UTF-8، بدون الأصفار اللاحقة. يتحقق router المُحدِّث من أن الإصدار في الرأس (غير المشمول بالتوقيع) يتطابق مع الإصدار في تعليق ملف zip، والذي يكون مشمولاً بالتوقيع. هذا يمنع انتحال رقم الإصدار في الرأس.

## التحميل والتثبيت

يقوم الـ router أولاً بتنزيل رأس ملف التحديث من واحد من قائمة قابلة للتكوين من عناوين I2P URLs، باستخدام عميل HTTP المدمج والـ proxy، ويتحقق من أن الإصدار أحدث. هذا يمنع مشكلة خوادم التحديث التي لا تحتوي على أحدث ملف. ثم يقوم الـ router بتنزيل ملف التحديث الكامل. يتحقق الـ router من أن إصدار ملف التحديث أحدث قبل التثبيت. كما يتحقق بالطبع من التوقيع، ويتحقق من أن تعليق ملف الـ zip يطابق إصدار الرأس، كما هو موضح أعلاه.

يتم استخراج ملف zip ونسخه إلى "i2pupdate.zip" في دليل تكوين I2P (~/.i2p على Linux).

اعتباراً من الإصدار 0.7.12، يدعم الـ router ضغط Pack200. الملفات داخل أرشيف الzip التي تحمل لاحقة .jar.pack أو .war.pack يتم إلغاء ضغطها بشكل شفاف إلى ملف .jar أو .war. ملفات التحديث التي تحتوي على ملفات .pack تُسمى تقليدياً بلاحقة '.su2'. Pack200 يقلل حجم ملفات التحديث بحوالي 60%.

اعتباراً من الإصدار 0.8.7، سيقوم الـ router بحذف ملفات libjbigi.so و libjcpuid.so إذا كان أرشيف الـ zip يحتوي على ملف lib/jbigi.jar، بحيث يتم استخراج الملفات الجديدة من jbigi.jar.

اعتباراً من الإصدار 0.8.12، إذا كان أرشيف zip يحتوي على ملف deletelist.txt، فسيقوم الموجه بحذف الملفات المدرجة فيه. التنسيق هو:

- اسم ملف واحد في كل سطر
- جميع أسماء الملفات نسبية لدليل التثبيت؛ لا يُسمح بأسماء الملفات المطلقة، ولا ملفات تبدأ بـ ".."
- التعليقات تبدأ بـ '#'

سيقوم الـ router بعد ذلك بحذف ملف deletelist.txt.

## مواصفات ملف SU3

يتم استخدام هذه المواصفة لتحديثات router اعتباراً من الإصدار 0.9.9، وبيانات reseed اعتباراً من الإصدار 0.9.14، والإضافات اعتباراً من الإصدار 0.9.15، وملف الأخبار اعتباراً من الإصدار 0.9.17.

### المشاكل مع تنسيق .sud/.su2 السابق

- لا يوجد رقم سحري أو علامات
- لا توجد طريقة لتحديد الضغط، pack200 أم لا، أو خوارزمية التوقيع
- الإصدار غير مغطى بالتوقيع، لذا يتم فرضه من خلال طلب وجوده في تعليق ملف zip (لملفات الموجه) أو في ملف plugin.config (للإضافات)
- الموقع غير محدد لذا يجب على المُتحقق تجربة جميع المفاتيح المعروفة
- تنسيق التوقيع قبل البيانات يتطلب مرورين لتوليد الملف

### الأهداف

- إصلاح المشاكل المذكورة أعلاه
- الانتقال إلى خوارزمية توقيع أكثر أماناً
- الاحتفاظ بمعلومات الإصدار في نفس التنسيق والإزاحة للتوافق مع أدوات فحص الإصدار الحالية
- التحقق من التوقيع واستخراج الملف في مرة واحدة

### المواصفة

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number "I2Psu3"</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">su3 file format version = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature type: 0x0000 = DSA-SHA1, 0x0001 = ECDSA-SHA256-P256, 0x0002 = ECDSA-SHA384-P384, 0x0003 = ECDSA-SHA512-P521, 0x0004 = RSA-SHA256-2048, 0x0005 = RSA-SHA384-3072, 0x0006 = RSA-SHA512-4096, 0x0008 = EdDSA-SHA512-Ed25519ph</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature length, e.g. 40 (0x0028) for DSA-SHA1. Must match that specified for the <a href="/docs/specs/common-structures#signature">Signature</a> type.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version length (in bytes not chars, including padding), must be at least 16 (0x10) for compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID length (in bytes not chars)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content length (not including header or sig)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File type: 0x00 = zip file, 0x01 = xml file (0.9.15), 0x02 = html file (0.9.17), 0x03 = xml.gz file (0.9.17), 0x04 = txt.gz file (0.9.28), 0x05 = dmg file (0.9.51), 0x06 = exe file (0.9.51)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content type: 0x00 = unknown, 0x01 = router update, 0x02 = plugin or plugin update, 0x03 = reseed data, 0x04 = news feed (0.9.15), 0x05 = blocklist feed (0.9.28)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40-55+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version, UTF-8 padded with trailing 0x00, 16 bytes minimum, length specified at byte 13. Do not append 0x00 bytes if the length is 16 or more.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ID of signer, (e.g. "zzz@mail.i2p") UTF-8, not padded, length specified at byte 15</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content: Length specified in header at bytes 16-23, Format specified in header at byte 25, Content specified in header at byte 27</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature: Length is specified in header at bytes 10-11, covers everything starting at byte 0</td>
    </tr>
  </tbody>
</table>
يجب تعيين جميع الحقول غير المستخدمة إلى 0 للتوافق مع الإصدارات المستقبلية.

### تفاصيل التوقيع

يغطي التوقيع الرأس بالكامل بدءاً من البايت 0، وحتى نهاية المحتوى. نستخدم التواقيع الخام. نأخذ hash للبيانات (باستخدام نوع hash المضمن في نوع التوقيع في البايتات 8-9) ونمررها إلى دالة توقيع أو تحقق "خام" (مثل "NONEwithRSA" في Java).

بينما يمكن تنفيذ التحقق من التوقيع واستخراج المحتوى في مرحلة واحدة، يجب على التطبيق قراءة وتخزين أول 10 بايت مؤقتاً لتحديد نوع الـ hash قبل البدء في التحقق.

أطوال التوقيعات لأنواع التوقيعات المختلفة مُعطاة في مواصفات [التوقيع](/docs/specs/common-structures#signature). قم بحشو التوقيع بأصفار رائدة إذا لزم الأمر. راجع [صفحة تفاصيل التشفير](/docs/specs/cryptography#sig) لمعرفة معايير أنواع التوقيعات المختلفة.

### ملاحظات

يحدد نوع المحتوى نطاق الثقة. لكل نوع محتوى، يحتفظ العملاء بمجموعة من شهادات المفاتيح العامة X.509 للأطراف الموثوقة لتوقيع ذلك المحتوى. يمكن استخدام الشهادات المخصصة لنوع المحتوى المحدد فقط. يتم البحث عن الشهادة بواسطة معرف الموقع. يجب على العملاء التحقق من أن نوع المحتوى هو المتوقع للتطبيق.

جميع القيم بترتيب بايت الشبكة (big endian).

للحصول على تنفيذ python لتوقيعات Raw RSA المتوافقة مع Java "NONEwithRSA"، راجع [هذا المقال في Stack Overflow](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530).

## مواصفات ملف تحديث Router SU3

### تفاصيل SU3

- نوع محتوى SU3: 1 (تحديث ROUTER)
- نوع ملف SU3: 0 (ZIP)
- إصدار SU3: إصدار الـ router

ملفات Jar و war في الأرشيف المضغوط لم تعد مضغوطة باستخدام pack200 كما هو موثق أعلاه لملفات "su2"، لأن بيئات تشغيل Java الحديثة لم تعد تدعمها.

### ملاحظات

- بالنسبة للإصدارات، إصدار SU3 هو إصدار router "الأساسي"، مثل "0.9.20".
- بالنسبة لإصدارات التطوير، المدعومة اعتباراً من الإصدار 0.9.20، إصدار SU3 هو إصدار router "الكامل"، مثل "0.9.20-5" أو "0.9.20-5-rc". راجع RouterVersion.java في [مصدر I2P](https://github.com/i2p/i2p.i2p).

## مواصفات ملف SU3 لإعادة البذر

اعتباراً من الإصدار 0.9.14، يتم تسليم بيانات إعادة البذر بصيغة ملف "su3".

### الأهداف

- ملفات موقعة بتوقيعات قوية وشهادات موثوقة لمنع هجمات man-in-the-middle التي يمكن أن تقوم بتشغيل الضحايا في شبكة منفصلة وغير موثوقة.
- استخدام تنسيق ملف su3 المستخدم بالفعل للتحديثات والإضافات
- ملف مضغوط واحد لتسريع عملية reseeding، والتي كانت بطيئة عند جلب 200 ملف

### المواصفات

1. يجب أن يكون اسم الملف "i2pseeds.su3". اعتباراً من الإصدار 0.9.42، يجب على المطلوب إلحاق سلسلة استعلام "?netid=2" بعنوان URL للطلب، بافتراض معرف الشبكة الحالي 2. يمكن استخدام هذا لمنع الاتصالات عبر الشبكات المختلفة. يجب أن تضع شبكات الاختبار معرف شبكة مختلف. راجع الاقتراح 147 للتفاصيل.
2. يجب أن يكون الملف في نفس الدليل مع معلومات router على خادم الويب.
3. سيحاول router أولاً جلب (عنوان URL للفهرس)/i2pseeds.su3؛ إذا فشل ذلك سيجلب عنوان URL للفهرس ثم يجلب ملفات معلومات router الفردية الموجودة في الروابط.

### تفاصيل SU3

- نوع محتوى SU3: 3 (RESEED)
- نوع ملف SU3: 0 (ZIP)
- إصدار SU3: ثوانٍ منذ العصر، بصيغة ASCII (date +%s). لا يعود للصفر في 2038 أو 2106.
- ملفات معلومات router في ملف zip يجب أن تكون في "المستوى الأعلى". لا توجد مجلدات في ملف zip.
- ملفات معلومات router يجب أن تُسمى "routerInfo-(44 حرف base 64 router hash).dat"، كما في آلية reseed القديمة. يجب استخدام أبجدية I2P base 64.

### ملاحظات

- تحذير: من المعروف أن عدة reseeds غير مستجيبة عبر IPv6. يُنصح بإجبار أو تفضيل IPv4.
- تحذير: بعض reseeds تستخدم شهادات CA موقعة ذاتياً. يجب على التطبيقات إما استيراد والوثوق بهذه الـ CAs عند الـ reseeding، أو حذف الـ reseeds الموقعة ذاتياً من قائمة reseed.
- مفاتيح reseed signer يتم توزيعها على التطبيقات كشهادات X.509 موقعة ذاتياً مع مفاتيح RSA-4096 (نوع التوقيع 6). يجب على التطبيقات فرض التواريخ الصالحة في الشهادات.

## مواصفات ملف المكون الإضافي SU3

اعتباراً من الإصدار 0.9.15، يمكن تعبئة الإضافات في تنسيق ملف "su3".

### تفاصيل SU3

- نوع محتوى SU3: 2 (PLUGIN)
- نوع ملف SU3: 0 (ZIP) - راجع [مواصفات المكون الإضافي](/docs/specs/plugin) للتفاصيل.
- إصدار SU3: إصدار المكون الإضافي، يجب أن يطابق ذلك الموجود في plugin.config.

ملفات Jar و war في الملف المضغوط يجب ألا تُضغط باستخدام pack200 كما هو موثق أعلاه لملفات "su2"، حيث أن إصدارات Java الحديثة لم تعد تدعمها.

## مواصفات ملف أخبار SU3

اعتباراً من الإصدار 0.9.17، يتم توصيل الأخبار بتنسيق ملف "su3".

### الأهداف

- أخبار موقعة بتوقيعات قوية وشهادات موثوقة
- استخدام تنسيق ملف su3 المستخدم بالفعل للتحديثات وإعادة البذر والإضافات
- تنسيق XML قياسي للاستخدام مع المحللات القياسية
- تنسيق Atom قياسي للاستخدام مع قارئات ومولدات التدفقات القياسية
- تطهير والتحقق من HTML قبل عرضه على وحدة التحكم
- مناسب للتنفيذ السهل على Android والمنصات الأخرى بدون وحدة تحكم HTML

### تفاصيل SU3

- نوع محتوى SU3: 4 (NEWS)
- نوع ملف SU3: 1 (XML) أو 3 (XML.GZ)
- إصدار SU3: ثواني منذ العهد، في ASCII (date +%s). لا يتجاوز في 2038 أو 2106.
- تنسيق الملف: XML أو XML مضغوط، يحتوي على تغذية XML [RFC 4287](https://tools.ietf.org/html/rfc4287) (Atom). يجب أن تكون مجموعة الأحرف UTF-8.

### تفاصيل تغذية Atom

يتم استخدام عناصر `<feed>` التالية:

**`<entry>`** : عنصر إخباري. انظر أدناه.

**`<i2p:release>`** : بيانات تحديث I2P الوصفية. انظر أدناه.

**`<i2p:revocations>`** : إبطالات الشهادات. انظر أدناه.

**`<i2p:blocklist>`** : بيانات قائمة الحظر. انظر أدناه.

**`<updated>`** : مطلوب. الطابع الزمني للتغذية (متوافق مع [RFC 4287](https://tools.ietf.org/html/rfc4287) القسم 3.3 و [RFC 3339](https://tools.ietf.org/html/rfc3339)).

### تفاصيل مدخل Atom

يمكن تحليل وعرض كل `<entry>` من Atom في تغذية الأخبار في وحدة تحكم الـ router. يتم استخدام العناصر التالية:

**`<author>`** : اختياري. يحتوي على `<name>` - اسم مؤلف الإدخال.

**`<content>`** : مطلوب. المحتوى، يجب أن يكون type="xhtml". سيتم تنظيف XHTML بقائمة بيضاء من العناصر المسموحة وقائمة سوداء من السمات غير المسموحة. قد يتجاهل العملاء عنصراً، أو الإدخال المحيط، أو الخلاصة بأكملها عند مواجهة عنصر غير موجود في القائمة البيضاء.

**`<link>`** : اختياري. رابط للمزيد من المعلومات.

**`<summary>`** : اختياري. ملخص قصير، مناسب لتلميح الأدوات.

**`<title>`** : مطلوب. عنوان الخبر.

**`<updated>`** : مطلوب. الطابع الزمني لهذا الإدخال (يجب أن يتوافق مع [RFC 4287](https://tools.ietf.org/html/rfc4287) القسم 3.3 و [RFC 3339](https://tools.ietf.org/html/rfc3339)).

### تفاصيل إصدار Atom i2p:release

يجب أن يكون هناك كيان `<i2p:release>` واحد على الأقل في التغذية. كل منها يحتوي على الخصائص والكيانات التالية:

**date (خاصية)** : مطلوب. الطابع الزمني لهذا الإدخال (متوافق مع [RFC 4287](https://tools.ietf.org/html/rfc4287) القسم 3.3 و [RFC 3339](https://tools.ietf.org/html/rfc3339)). قد يكون التاريخ أيضاً بصيغة مقتطعة yyyy-mm-dd (بدون 'T')؛ هذه هي صيغة "التاريخ الكامل" في RFC 3339. في هذه الصيغة يُفترض أن الوقت هو 00:00:00 UTC لأي معالجة.

**minJavaVersion (خاصية)** : إذا كانت موجودة، فهي الحد الأدنى من إصدار Java المطلوب لتشغيل الإصدار الحالي.

**minVersion (خاصية)** : إذا كانت موجودة، فهي الإصدار الأدنى من الـ router المطلوب للتحديث إلى الإصدار الحالي. إذا كان الـ router أقدم من هذا، يجب على المستخدم التحديث (يدوياً؟) إلى إصدار وسطي أولاً.

**`<i2p:version>`** : مطلوب. أحدث إصدار متاح حالياً من الـ router.

**`<i2p:update>`** : ملف تحديث (واحد أو أكثر). يجب أن يحتوي على عنصر فرعي واحد على الأقل.   - type (خاصية): "sud"، "su2"، أو "su3". يجب أن تكون فريدة عبر جميع عناصر `<i2p:update>`.   - `<i2p:clearnet>`: روابط التحميل المباشر خارج الشبكة (صفر أو أكثر). href (خاصية): رابط http عادي للإنترنت العادي.   - `<i2p:clearnetssl>`: روابط التحميل المباشر خارج الشبكة (صفر أو أكثر). href (خاصية): رابط https عادي للإنترنت العادي.   - `<i2p:torrent>`: رابط magnet داخل الشبكة. href (خاصية): رابط magnet.   - `<i2p:url>`: روابط التحميل المباشر داخل الشبكة (صفر أو أكثر). href (خاصية): رابط http .i2p داخل الشبكة.

- آلية تحديث الـ router هي جزء من وحدة تحكم الـ router عبر الويب. لا يوجد حاليًا أي توفير لتحديثات الـ router المدمج الذي يفتقر إلى وحدة تحكم الـ router.

### تفاصيل إلغاءات i2p للـ Atom

هذا العنصر اختياري ولا يوجد أكثر من عنصر `<i2p:revocations>` واحد في الخلاصة. هذه الميزة مدعومة اعتباراً من الإصدار 0.9.26.

يحتوي الكيان `<i2p:revocations>` على كيان واحد أو أكثر من `<i2p:crl>`. يحتوي الكيان `<i2p:crl>` على الخصائص التالية:

**updated (السمة)** : مطلوبة. الطابع الزمني لهذا الإدخال (وفقاً لـ [RFC 4287](https://tools.ietf.org/html/rfc4287) القسم 3.3 و [RFC 3339](https://tools.ietf.org/html/rfc3339)). قد يكون التاريخ أيضاً بالتنسيق المقتطع yyyy-mm-dd (بدون 'T')؛ هذا هو تنسيق "التاريخ الكامل" في RFC 3339. في هذا التنسيق يُفترض أن الوقت هو 00:00:00 UTC لأي معالجة.

**id (attribute)** : مطلوب. معرف فريد لمنشئ قائمة الشهادات المُلغاة هذه.

**(محتوى الكيان)** : مطلوب. قائمة إبطال الشهادات (CRL) مشفرة بترميز base 64 قياسي مع أسطر جديدة، تبدأ بالسطر '-----BEGIN X509 CRL-----' وتنتهي بالسطر '-----END X509 CRL-----'. راجع [RFC 5280](https://tools.ietf.org/html/rfc5280) لمزيد من المعلومات حول قوائم CRL.

### تفاصيل Atom i2p:blocklist

هذا العنصر اختياري ولا يوجد أكثر من عنصر واحد `<i2p:blocklist>` في الخلاصة. هذه الميزة مجدولة للتنفيذ في الإصدار 0.9.28.

يحتوي عنصر `<i2p:blocklist>` على عنصر واحد أو أكثر من عناصر `<i2p:block>` أو `<i2p:unblock>`، وعنصر "updated"، وخصائص "signer" و "sig":

**signer (attribute)** : مطلوب. معرف فريد (UTF-8) للمفتاح العام المستخدم لتوقيع قائمة الحظر هذه.

**sig (خاصية)** : مطلوب. توقيع بالتنسيق code:b64sig، حيث code هو رقم نوع التوقيع ASCII، و b64sig هو التوقيع المشفر بـ base 64 (أبجدية I2P). انظر أدناه لمواصفات البيانات المراد توقيعها.

**`<updated>`** : مطلوب. طابع زمني لقائمة الحظر (متوافق مع [RFC 4287](https://tools.ietf.org/html/rfc4287) القسم 3.3 و [RFC 3339](https://tools.ietf.org/html/rfc3339)). يمكن أن يكون التاريخ أيضاً بصيغة مقطوعة yyyy-mm-dd (بدون 'T')؛ هذه هي صيغة "التاريخ الكامل" في RFC 3339. في هذه الصيغة يُفترض أن يكون الوقت 00:00:00 UTC لأي معالجة.

**`<i2p:block>`** : اختياري، يُسمح بعدة كيانات. إدخال واحد، إما عنوان IPv4 أو IPv6 حرفي، أو router hash مكون من 44 حرف base 64 (أبجدية I2P). عناوين IPv6 قد تكون في صيغة مختصرة (تحتوي على "::"). الدعم للإدخالات مع netmask، مثل x.y.0.0/16، اختياري. الدعم لأسماء المضيفين اختياري.

**`<i2p:unblock>`** : اختياري، يُسمح بعدة كيانات. نفس تنسيق `<i2p:block>`.

**مواصفات التوقيع:** لإنشاء البيانات المراد توقيعها أو التحقق منها، قم بربط البيانات التالية بترميز ASCII: النص المحدث متبوعاً بسطر جديد (ASCII 0x0a)، ثم كل إدخال حظر بالترتيب المستلم مع سطر جديد بعد كل منها، ثم كل إدخال إلغاء حظر بالترتيب المستلم مع سطر جديد بعد كل منها.

## مواصفات ملف قائمة الحظر

TBD، غير مُنفذ، راجع الاقتراح 130. يتم تسليم تحديثات القائمة السوداء في ملف الأخبار، انظر أعلاه.

## العمل المستقبلي

- **[CRYPTO-SIG]** [التشفير - التوقيعات](/docs/specs/cryptography#sig)
- **[I2P-SRC]** [كود مصدر I2P](https://github.com/i2p/i2p.i2p)
- **[PLUGIN]** [مواصفة الإضافة](/docs/specs/plugin)
- **[Python]** [توقيعات Python RSA الخام](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530)
- **[RFC-3339]** [RFC 3339 - التاريخ والوقت](https://tools.ietf.org/html/rfc3339)
- **[RFC-4287]** [RFC 4287 - تنسيق Atom Syndication](https://tools.ietf.org/html/rfc4287)
- **[RFC-5280]** [RFC 5280 - قوائم إلغاء الشهادات](https://tools.ietf.org/html/rfc5280)
- **[Signature]** [نوع التوقيع](/docs/specs/common-structures#signature)
- **[SigningPublicKey]** [نوع SigningPublicKey](/docs/specs/common-structures#signingpublickey)

## المراجع

- **[CRYPTO-SIG]** [التشفير - التوقيعات](/docs/specs/cryptography#sig)
- **[I2P-SRC]** [الشيفرة المصدرية لـ I2P](https://github.com/i2p/i2p.i2p)
- **[PLUGIN]** [مواصفات Plugin](/docs/specs/plugin)
- **[Python]** [توقيعات RSA الخام في Python](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530)
- **[RFC-3339]** [RFC 3339 - التاريخ والوقت](https://tools.ietf.org/html/rfc3339)
- **[RFC-4287]** [RFC 4287 - صيغة Atom للتغذية](https://tools.ietf.org/html/rfc4287)
- **[RFC-5280]** [RFC 5280 - قوائم إلغاء الشهادات](https://tools.ietf.org/html/rfc5280)
- **[Signature]** [نوع Signature](/docs/specs/common-structures#signature)
- **[SigningPublicKey]** [نوع SigningPublicKey](/docs/specs/common-structures#signingpublickey)
