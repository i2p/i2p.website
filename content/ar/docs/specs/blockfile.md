---
title: "مواصفات Blockfile وقاعدة بيانات المضيفين"
description: "مواصفات تنسيق ملف I2P blockfile والجداول في hostsdb.blockfile المستخدمة من قبل خدمة التسمية Blockfile Naming Service"
slug: "blockfile"
aliases:
  - "/ar/blockfile"
  - "/ar/blockfile/"
category: "التنسيقات"
lastUpdated: "2023-11"
accurateFor: "0.9.59"
---

## نظرة عامة

تحدد هذه الوثيقة تنسيق ملف I2P blockfile والجداول الموجودة في hostsdb.blockfile المستخدمة من قِبل خدمة Blockfile Naming Service [NAMING](/docs/overview/naming/).

يوفر blockfile بحثاً سريعاً عن الوجهة (Destination) بتنسيق مضغوط. بينما تكون النفقات العامة لصفحة blockfile كبيرة، يتم تخزين الوجهات في تنسيق ثنائي بدلاً من Base 64 كما في تنسيق hosts.txt. بالإضافة إلى ذلك، يوفر blockfile إمكانية تخزين البيانات الوصفية التعسفية (مثل تاريخ الإضافة والمصدر والتعليقات) لكل إدخال. قد يتم استخدام البيانات الوصفية في المستقبل لتوفير ميزات متقدمة لدفتر العناوين. متطلبات تخزين blockfile تمثل زيادة متواضعة مقارنة بتنسيق hosts.txt، ويوفر blockfile انخفاضاً يبلغ حوالي 10 أضعاف في أوقات البحث.

blockfile هو ببساطة تخزين على القرص لخرائط مرتبة متعددة (أزواج key-value)، مُطبق كـ skiplists. تم تبني تنسيق blockfile من قاعدة بيانات Metanotion Blockfile Database [METANOTION](http://www.metanotion.net/software/sandbox/block.html). أولاً سنحدد تنسيق الملف، ثم استخدام هذا التنسيق بواسطة BlockfileNamingService.

## تنسيق ملف الكتل (Blockfile Format)

تم تعديل مواصفات blockfile الأصلية لإضافة أرقام سحرية لكل صفحة. الملف منظم في صفحات بحجم 1024 بايت. الصفحات مرقمة بدءاً من 1. الـ "superblock" دائماً في الصفحة 1، أي بدءاً من البايت 0 في الملف. قائمة metaindex skiplist دائماً في الصفحة 2، أي بدءاً من البايت 1024 في الملف.

جميع قيم الأعداد الصحيحة من 2 بايت غير موقعة. جميع قيم الأعداد الصحيحة من 4 بايت (أرقام الصفحات) موقعة والقيم السالبة غير مسموحة. جميع قيم الأعداد الصحيحة مخزنة بترتيب بايتات الشبكة (big endian).

قاعدة البيانات مصممة ليتم فتحها والوصول إليها بواسطة خيط واحد فقط. يوفر BlockfileNamingService المزامنة.

### تنسيق الكتلة الفائقة

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x3141de493250 ("1A" 0xde "I2P")</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Major version</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x01</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Minor version</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x02</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">File length</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total length in bytes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First free list page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">20-21</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Mounted flag</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x01 = yes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">22-23</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Span size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Max number of key/value pairs per span (16 for hostsdb). Used for new skip lists.</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Page size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">As of version 1.2. Prior to 1.2, 1024 is assumed.</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">28-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### تنسيق صفحة كتلة قائمة التخطي

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x536b69704c697374 "SkipList"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First level page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total number of keys - may only be valid at startup</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">20-23</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Spans</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total number of spans - may only be valid at startup</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Levels</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total number of levels - may only be valid at startup</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">28-29</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Span size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">As of version 1.2. Max number of key/value pairs per span. Prior to that, specified for all skiplists in the superblock. Used for new spans in this skip list.</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">30-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### تنسيق صفحة كتلة تخطي المستوى

جميع المستويات لها مدى. ليس جميع المديات لها مستويات.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x42534c6576656c73 "BSLevels"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Max height</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Current height</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next level pages</td><td style="border:1px solid var(--color-border); padding:0.6rem;">'current height' entries, 4 bytes each, lowest first</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">remaining</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### تخطي تنسيق صفحة كتلة النطاق

هياكل المفتاح/القيمة مرتبة حسب المفتاح داخل كل نطاق وعبر جميع النطاقات. هياكل المفتاح/القيمة مرتبة حسب المفتاح داخل كل نطاق. النطاقات غير النطاق الأول قد لا تكون فارغة.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x5370616e "Span"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First continuation page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Previous span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-17</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Max keys</td><td style="border:1px solid var(--color-border); padding:0.6rem;">16 for hostsdb</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">18-19</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Current number of keys</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">20-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key/value structures</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### تنسيق صفحة كتلة استمرار المدى

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x434f4e54 "CONT"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next continuation page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key/value structures</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### تنسيق هيكل المفتاح/القيمة

يجب ألا تتوزع أطوال المفاتيح والقيم عبر الصفحات، أي أن جميع البايتات الأربعة يجب أن تكون في نفس الصفحة. إذا لم يكن هناك مساحة كافية، فإن آخر 1-3 بايتات من الصفحة تبقى غير مستخدمة وستكون الأطوال عند الإزاحة 8 في صفحة المتابعة. يمكن تقسيم بيانات المفاتيح والقيم عبر الصفحات. الحد الأقصى لأطوال المفاتيح والقيم هو 65535 بايت.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key length in bytes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">2-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">value length in bytes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key data</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;"></td><td style="border:1px solid var(--color-border); padding:0.6rem;">value data</td></tr>
</tbody>
</table>
### تنسيق صفحة كتلة القائمة الحرة

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x2366724c69737423 "#frList#"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next free list block</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0 if none</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Number of valid free pages</td><td style="border:1px solid var(--color-border); padding:0.6rem;">in this block (0 - 252)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Free pages</td><td style="border:1px solid var(--color-border); padding:0.6rem;">4 bytes each, only the first (valid number) are valid</td></tr>
</tbody>
</table>
### تنسيق كتلة الصفحة الحرة

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x7e2146524545217e "~!FREE!~"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
الفهرس الفوقي (الموجود في الصفحة 2) هو تخطيط لسلاسل US-ASCII إلى أعداد صحيحة من 4 بايت. المفتاح هو اسم قائمة التخطي والقيمة هي فهرس الصفحة لقائمة التخطي.

## جداول خدمة تسمية ملفات الكتل

الجداول التي تم إنشاؤها واستخدامها بواسطة BlockfileNamingService هي كما يلي. العدد الأقصى للإدخالات لكل span هو 16.

### قائمة تخطي الخصائص

`%%__INFO__%%` هو skiplist قاعدة البيانات الرئيسية مع إدخالات مفتاح/قيمة String/Properties التي تحتوي على إدخال واحد فقط:

**info** - خصائص (خريطة نص UTF-8/نص)، مُسلسلة كـ [Mapping](/docs/specs/common-structures/#type-mapping):

- **version** - "4"
- **created** - Java long time (ms)
- **upgraded** - Java long time (ms) (اعتباراً من إصدار قاعدة البيانات 2)
- **lists** - قائمة مفصولة بفواصل من قواعد بيانات المضيف، يتم البحث فيها بالترتيب للاستعلامات. دائماً تقريباً "privatehosts.txt,userhosts.txt,hosts.txt".
- **listversion_*** - إصدار كل قاعدة بيانات في القوائم، على سبيل المثال: listversion_hosts.txt=4. يُستخدم لتحديد الترقية الجزئية أو المجهضة للقوائم الفردية. (اعتباراً من إصدار قاعدة البيانات 4)

### قائمة التخطي للبحث العكسي

`%%__REVERSE__%%` هو skiplist البحث العكسي مع مدخلات مفتاح/قيمة من نوع Integer/Properties (اعتباراً من إصدار قاعدة البيانات 2):

- مفاتيح skiplist هي أعداد صحيحة من 4 بايت، وهي البايتات الأربعة الأولى من hash الخاص بـ [Destination](/docs/specs/common-structures/#struct-destination).
- قيم skiplist هي كل واحدة منها Properties (خريطة String/String بتشفير UTF-8) مسلسلة كـ [Mapping](/docs/specs/common-structures/#type-mapping)
  - قد توجد إدخالات متعددة في الخصائص، كل واحدة هي تخطيط عكسي، حيث أنه قد يكون هناك أكثر من اسم مضيف واحد لـ destination معين، أو قد تحدث تضاربات مع نفس البايتات الأربعة الأولى من الـ hash.
  - كل مفتاح خاصية هو اسم مضيف.
  - كل قيمة خاصية هي سلسلة نصية فارغة.

### قوائم التخطي لملفات hosts.txt و userhosts.txt و privatehosts.txt

لكل قاعدة بيانات مضيف، هناك skiplist تحتوي على المضيفين لتلك قاعدة البيانات. لاحظ أن تنسيق الإصدار 4 يدعم عدة Destinations لكل اسم مضيف. تم تقديم هذا التنسيق في إصدار I2P 0.9.26. يتم ترحيل قواعد بيانات الإصدار 3 تلقائياً إلى الإصدار 4.

المفاتيح/القيم في هذه القوائم المتخطية هي كما يلي:

**key** - نص UTF-8 (اسم المضيف)

**value** - - إصدار قاعدة البيانات 4: DestEntry، وهو رقم من بايت واحد لأزواج Properties/Destination التي تتبع. ذلك العدد من الأزواج من: Properties (خريطة UTF-8 String/String) متسلسلة كـ [Mapping](/docs/specs/common-structures/#type-mapping) متبوعة بـ [Destination](/docs/specs/common-structures/#struct-destination) ثنائي (متسلسل كالمعتاد). - إصدار قاعدة البيانات 3: DestEntry، وهو Properties (خريطة UTF-8 String/String) متسلسلة كـ [Mapping](/docs/specs/common-structures/#type-mapping) متبوعة بـ [Destination](/docs/specs/common-structures/#struct-destination) ثنائي (متسلسل كالمعتاد).

خصائص DestEntry تحتوي عادة على:

- **"a"** - الوقت المُضاف (Java long time in ms)
- **"m"** - الوقت المُعدّل آخر مرة (Java long time in ms)
- **"notes"** - تعليقات يوفرها المستخدم
- **"s"** - المصدر الأصلي للإدخال (عادة اسم ملف أو رابط اشتراك)
- **"v"** - إذا تم التحقق من توقيع الإدخال، "true" أو "false"

يتم تخزين مفاتيح أسماء المضيفين بأحرف صغيرة وتنتهي دائماً بـ ".i2p".

## المراجع

- [الوجهة](/docs/specs/common-structures/#struct-destination)
- [التخطيط](/docs/specs/common-structures/#type-mapping)
- [METANOTION](http://www.metanotion.net/software/sandbox/block.html)
- [التسمية](/docs/overview/naming/)
