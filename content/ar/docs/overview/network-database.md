---
title: "قاعدة بيانات الشبكة"
description: "فهم قاعدة بيانات الشبكة الموزعة الخاصة بـ I2P (netDb) - DHT متخصص (جدول تجزئة موزع) لمعلومات اتصال router وعمليات البحث عن الوجهات"
slug: "network-database"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. نظرة عامة

تُعدّ **netDb** قاعدة بيانات موزعة متخصصة تحتوي على نوعين فقط من البيانات: - **RouterInfos** – معلومات الاتصال الخاصة بالـ router - **LeaseSets** – معلومات الاتصال الخاصة بالوجهة

جميع البيانات مُوقَّعة تشفيرياً وقابلة للتحقق. يتضمّن كل مُدخل معلومات الحيَوية (liveness) لتمكين إسقاط المُدخلات البالية واستبدال المتقادمة، ما يوفّر حماية ضد فئات معيّنة من الهجمات.

تستخدم عملية التوزيع آلية **floodfill** (آلية الغمر)، حيث تتولى مجموعة فرعية من routers صيانة قاعدة البيانات الموزعة.

---

## 2. RouterInfo

عندما تحتاج routers إلى الاتصال بـ routers أخرى، فإنها تتبادل حِزَم **RouterInfo** التي تحتوي على:

- **هوية router** – مفتاح التشفير، مفتاح التوقيع، الشهادة
- **عناوين الاتصال** – كيفية الوصول إلى router
- **الطابع الزمني للنشر** – متى نُشرت هذه المعلومات
- **خيارات نصية اعتباطية** – أعلام القدرات والإعدادات
- **توقيع تشفيري** – يثبت الأصالة

### 2.1 أعلام القدرات

Routers تعلن عن قدراتها عبر رموز حرفية في RouterInfo الخاص بها:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>f</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill participation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>R</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>U</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unreachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>D</strong>, <strong>E</strong>, <strong>G</strong>, <strong>H</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Various capability indicators</td>
    </tr>
  </tbody>
</table>
### 2.2 تصنيفات عرض النطاق الترددي

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bandwidth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>K</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Under 12 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>L</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12–48 KBps (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>M</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48–64 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>N</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64–128 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>O</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128–256 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256–2000 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>X</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Over 2000 KBps</td>
    </tr>
  </tbody>
</table>
### 2.3 قيم معرّف الشبكة

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current Network (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for Future Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3–15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forks and Test Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16–254</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
  </tbody>
</table>
### 2.4 إحصائيات RouterInfo

Routers تنشر إحصاءات صحية اختيارية لتحليل الشبكة: - معدلات النجاح/الرفض/انتهاء المهلة في إنشاء tunnel استكشافية - متوسط عدد tunnel المشاركة خلال ساعة واحدة

تتبع الإحصاءات الصيغة `stat_(statname).(statperiod)` مع قيم مفصولة بفواصل منقوطة.

**إحصائيات المثال:**

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
قد تنشر Floodfill routers (عُقد floodfill في الشبكة) أيضًا: `netdb.knownLeaseSets` و `netdb.knownRouters`

### 2.5 خيارات العائلة

اعتبارًا من الإصدار 0.9.24، يمكن لـ routers الإعلان عن family membership (نفس المشغل):

- **family**: اسم العائلة
- **family.key**: رمز نوع التوقيع مقترنًا بمفتاح التوقيع العمومي المُرمَّز بترميز base64
- **family.sig**: توقيع لاسم العائلة وتجزئة router بطول 32 بايت

لن يُستَخدَم أكثر من router واحد من العائلة نفسها ضمن أي tunnel واحد.

### 2.6 انتهاء صلاحية RouterInfo (معلومات router في I2P)

- لا يوجد انتهاء صلاحية خلال الساعة الأولى من مدة التشغيل
- لا يوجد انتهاء صلاحية عند وجود 25 أو أقل من RouterInfos المخزنة
- تتناقص مدة الانتهاء مع زيادة العدد المحلي (72 ساعة عند <120 routers; ~30 ساعة عند 300 routers)
- تنقضي صلاحية المعرِّفين في SSU خلال ~1 ساعة
- تستخدم Floodfills مدة انتهاء قدرها ساعة واحدة لجميع RouterInfos المحلية

---

## 3. LeaseSet

**LeaseSets** توثق نقاط دخول tunnel لوجهات معينة، محددة:

- **هوية router عند بوابة tunnel**
- **معرّف tunnel مكوّن من 4 بايت**
- **وقت انتهاء صلاحية tunnel**

تتضمن LeaseSets: - **الوجهة** – مفتاح التشفير، مفتاح التوقيع، شهادة - **مفتاح عام إضافي للتشفير** – من أجل garlic encryption من الطرف إلى الطرف - **مفتاح عام إضافي للتوقيع** – مخصص للإبطال (غير مستخدم حالياً) - **توقيع تشفيري**

### 3.1 أنواع LeaseSet

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unpublished</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Destinations used only for outgoing connections aren't published to floodfill routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Revoked</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Published with zero leases, signed by additional signing key (not fully implemented)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet2 (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, supports new encryption types, multiple encryption types, options, offline signing keys ([Proposal 123](/proposals/123-new-netdb-entries/))</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Meta LeaseSet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tree-like DHT structure for multihomed services, supporting hundreds/thousands of destinations with long expirations (up to 18.2 hours)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS1)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All leases encrypted with separate key; only those with the key can decode and contact the destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, destination hidden with only blinded public key and expiration visible to floodfill</td>
    </tr>
  </tbody>
</table>
### 3.2 انتهاء صلاحية LeaseSet

تنتهي صلاحية LeaseSets العادية عند أحدث تاريخ لانتهاء lease (مدة اتصال) فيها. يُحدَّد تاريخ انتهاء LeaseSet2 في الترويسة. قد تختلف تواريخ انتهاء EncryptedLeaseSet و MetaLeaseSet مع احتمال تطبيق حد أقصى.

---

## 4. التمهيد الأولي

تتطلّب netDb اللامركزية وجود مرجع واحد على الأقل لنظير للاندماج. **Reseeding** تسترجع ملفات RouterInfo (`routerInfo-$hash.dat`) من مجلّدات netDb لدى المتطوعين. عند التشغيل الأول يتم الجلب تلقائيًا من عناوين URLs ثابتة مُضمّنة صراحةً، تُختار عشوائيًا.

---

## 5. آلية Floodfill

تستخدم floodfill netDb (قاعدة بيانات الشبكة بأسلوب floodfill) تخزيناً موزعاً بسيطاً: تُرسَل البيانات إلى أقرب نظير floodfill. عندما يرسل النظراء غير floodfill رسائل التخزين، يعيد نظراء floodfill توجيهها إلى مجموعة فرعية من نظراء floodfill الأقرب إلى المفتاح المحدد.

يُشار إلى المشاركة في floodfill (عُقد لتخزين netDb الموزَّعة في I2P) من خلال علم قدرة (`f`) في RouterInfo.

### 5.1 متطلبات الانضمام الاختياري لـ Floodfill

على خلاف خوادم الدليل الموثوقة المثبتة في الشيفرة (hardcoded) لدى Tor، فإن مجموعة floodfill الخاصة بـ I2P هي **غير موثوقة** وتتغيّر مع مرور الوقت.

يتم تمكين Floodfill تلقائيًا فقط على routers ذات النطاق الترددي العالي التي تستوفي هذه المتطلبات: - حد أدنى 128 KBytes/sec من النطاق الترددي المُشترك (يتم تكوينه يدويًا) - يجب أن تجتاز اختبارات صحة إضافية (زمن قائمة انتظار الرسائل الصادرة، تأخر المهام)

يؤدي الاشتراك التلقائي الحالي إلى نحو **6% من المشاركة في floodfill على مستوى الشبكة**.

توجد floodfills (عُقد خاصة في شبكة I2P لتخزين وتوزيع netDb) المُهيأة يدويًا جنبًا إلى جنب مع المتطوعين تلقائيًا. عندما ينخفض عدد الـ floodfills عن العتبة، تتطوع routers (برامج I2P التي توجّه الحركة) عالية عرض النطاق تلقائيًا. وعندما يكون هناك عدد كبير جدًا من الـ floodfills، فإنها تُلغي عن نفسها وضع الـ floodfill.

### 5.2 أدوار Floodfill (عُقد مسؤولة عن نشر وفهرسة بيانات الشبكة)

إلى جانب قبول عمليات تخزين netDb (قاعدة بيانات الشبكة في I2P) والاستجابة للاستعلامات، تؤدي floodfills (عُقد floodfill في I2P لنشر netDb) وظائف router (الموجّه في I2P) القياسية. إن عرض النطاق الأعلى لديها يعني عادةً مشاركةً أكبر في tunnel (نفق I2P)، لكن ذلك لا يرتبط مباشرةً بخدمات قاعدة البيانات.

---

## 6. مقياس التقارب في Kademlia (بروتوكول جدول تجزئة موزع DHT)

يستخدم netDb قياس المسافة **بأسلوب Kademlia** المعتمد على XOR. تُنشئ تجزئة SHA256 لـ RouterIdentity أو Destination مفتاح Kademlia (باستثناء LS2 Encrypted LeaseSets، التي تستخدم SHA256 لبايت النوع رقم 3 بالإضافة إلى blinded public key (مفتاح عام مُعمّى بالتعمية العمياء)).

### 6.1 تدوير فضاء المفاتيح

لزيادة تكلفة هجمات سيبيل، بدلاً من استخدام `SHA256(key)`، يستخدم النظام:

```
SHA256(key + yyyyMMdd)
```
حيث يكون التاريخ عبارة عن تاريخ UTC بصيغة ASCII بطول 8 بايت. هذا يُنشئ **routing key** (مفتاح التوجيه)، ويتغيّر يوميًا عند منتصف الليل بتوقيت UTC—ويُسمّى ذلك **keyspace rotation** (تدوير فضاء المفاتيح).

لا تُنقَل مفاتيح التوجيه أبدًا في رسائل I2NP؛ فهي تُستخدم فقط لتحديد المسافة محليًا.

---

## 7. تقسيم قاعدة بيانات الشبكة

لا تحافظ Kademlia DHTs (جداول التجزئة الموزعة من نوع كادملِيا) التقليدية على خاصية عدم قابلية ربط المعلومات المخزنة. تمنع I2P الهجمات التي تربط tunnels الخاصة بالعميل بـ routers من خلال تنفيذ **التقسيم**.

### 7.1 استراتيجية التجزئة

Routers تتتبّع: - ما إذا كانت المدخلات قد وصلت عبر client tunnels أم مباشرة - إذا كان عبر tunnel، فأي client tunnel/وجهة - تتم متابعة حالات وصول متعددة عبر tunnel - يُميَّز بين ردود التخزين وردود الاستعلام

كلٌ من تنفيذَي Java و C++ يستخدمان: - قاعدة **"Main" netDb** لعمليات الاستعلام/floodfill المباشرة في سياق router - **"Client Network Databases"** أو **"Sub-Databases"** في سياقات العميل، تلتقط الإدخالات المرسلة إلى client tunnels

توجد netDbs الخاصة بالعميل طوال مدة حياة العميل فقط، وتحتوي فقط على إدخالات tunnel الخاصة بالعميل. لا يمكن أن تتداخل الإدخالات الواردة من client tunnels مع عمليات الوصول المباشرة.

يتعقّب كل netDb ما إذا كانت المدخلات قد وصلت على أنها عمليات تخزين (تستجيب لطلبات الاستعلام) أو على أنها ردود استعلام (لا تستجيب إلا إذا كانت قد خُزِّنت مسبقًا للوجهة نفسها). لا يجيب العملاء مطلقًا عن الاستعلامات باستخدام مدخلات netDb الرئيسية، بل فقط باستخدام مدخلات قاعدة بيانات الشبكة الخاصة بالعميل.

الاستراتيجيات المجمعة **تجزئ** netDb ضد هجمات ربط العميل بالـ router.

---

## 8. التخزين، التحقق، والاستعلام

### 8.1 تخزين RouterInfo لدى النظراء

رسالة I2NP من نوع `DatabaseStoreMessage` تحتوي على تبادل RouterInfo المحلي أثناء تهيئة اتصال النقل عبر NTCP أو SSU.

### 8.2 تخزين LeaseSet لدى الأقران

تُبادَل دوريًا رسائل I2NP `DatabaseStoreMessage` التي تتضمن LeaseSet المحلي عبر رسائل مُشفَّرة باستخدام garlic encryption (أسلوب التشفير بالثوم في I2P) مُضمَّنة مع حركة مرور Destination، مما يتيح الردود من دون عمليات بحث عن LeaseSet.

### 8.3 اختيار Floodfill

`DatabaseStoreMessage` يرسل إلى floodfill الأقرب إلى مفتاح التوجيه الحالي. يُعثر على أقرب floodfill عبر بحث في قاعدة البيانات المحلية. حتى إن لم يكن الأقرب فعلاً، فإن آلية الفيضان (flooding) تنشره ليصبح "أقرب" عبر إرساله إلى عدة floodfills.

يستخدم Kademlia التقليدي بحث "find-closest" (للعثور على أقرب نظير) قبل الإدراج. بينما يفتقر I2NP إلى مثل هذه الرسائل، قد تقوم routers بإجراء بحث تكراري مع قلب البت الأقل أهمية (`key ^ 0x01`) لضمان اكتشاف النظير الأقرب فعلاً.

### 8.4 تخزين RouterInfo لدى Floodfills

Routers تنشر RouterInfo عبر الاتصال مباشرةً بـ floodfill، وذلك بإرسال I2NP `DatabaseStoreMessage` مع رمز رد غير صفري. الرسالة ليست مشفّرة بـ garlic encryption من طرف إلى طرف (اتصال مباشر، بلا وسطاء). يردّ الـ floodfill برسالة `DeliveryStatusMessage` مستخدماً رمز الرد كمعرّف للرسالة.

قد ترسل Routers أيضًا RouterInfo (بيانات تعريف الـ Router في I2P) عبر tunnel استطلاعي (قيود الاتصال، عدم التوافق، إخفاء عنوان IP). قد ترفض Floodfills عمليات التخزين هذه أثناء التحميل الزائد.

### 8.5 تخزين LeaseSet لدى Floodfills

تخزين LeaseSet أكثر حساسية من RouterInfo (بيانات تعريف router في I2P). يجب على Routers منع ارتباط LeaseSet بها.

Routers تنشر LeaseSet عبر tunnel العميل الصادر بإرسال `DatabaseStoreMessage` مع Reply Token (رمز الرد) غير صفري. تكون الرسالة مشفّرة طرفاً إلى طرف باستخدام garlic encryption عبر Session Key Manager (مدير مفاتيح الجلسة) الخاص بـ Destination (الوجهة)، ما يخفيها عن نقطة النهاية الصادرة لـ tunnel. يرد Floodfill بـ `DeliveryStatusMessage` تُعاد عبر tunnel الوارد.

### 8.6 عملية الإغراق

تقوم Floodfills بالتحقق من صحة RouterInfo (بيانات تعريف router)/LeaseSet قبل التخزين محلياً باستخدام معايير تكيُّفية تعتمد على الحمل، وحجم netdb، وعوامل أخرى.

بعد استلام بيانات أحدث وصحيحة، تقوم عُقد floodfill بـ"flood" لها عبر البحث عن أقرب 3 floodfill routers إلى routing key (مفتاح التوجيه). ترسل الاتصالات المباشرة I2NP `DatabaseStoreMessage` مع Reply Token (رمز الرد) يساوي صفراً. لا تقوم الـ routers الأخرى بالرد أو بإعادة الإغراق.

**قيود مهمة:** - يجب ألا تقوم Floodfills بالنشر عبر tunnels; اتصالات مباشرة فقط - لا تقوم Floodfills مطلقاً بنشر LeaseSet منتهي الصلاحية أو RouterInfo نُشر قبل أكثر من ساعة

### 8.7 الاستعلام عن RouterInfo و LeaseSet

تطلب I2NP `DatabaseLookupMessage` إدخالات netdb من floodfill routers (عُقد مُخصّصة لتخزين netdb ونشره).
تُرسَل الاستعلامات عبر tunnel استكشافي صادر؛ وتُحدِّد الردود tunnel استكشافي وارد للعودة.

عادةً ما تُرسَل عمليات الاستعلام إلى اثنين من floodfill routers "جيدين" الأقربَين إلى المفتاح المطلوب، بالتوازي.

- **تطابق محلي**: يتلقى استجابة من نوع I2NP `DatabaseStoreMessage`
- **لا يوجد تطابق محلي**: يتلقى رسالة I2NP `DatabaseSearchReplyMessage` مع مراجع لـ floodfill router أخرى قريبة من المفتاح

عمليات الاستعلام عن LeaseSet تستخدم تشفير garlic من طرف إلى طرف (اعتباراً من 0.9.5). عمليات الاستعلام عن RouterInfo (معلومات الـrouter) غير مُشفّرة بسبب كلفة ElGamal العالية، مما يجعلها عرضة للتجسس من قِبل نقطة النهاية الخارجة.

اعتباراً من 0.9.7، تتضمن ردود الاستعلام مفتاح جلسة ووسماً، مما يخفي الردود عن البوابة الواردة.

### 8.8 عمليات البحث التكرارية

قبل 0.8.9: عمليتا استعلام احتياطيتان متوازيتان من دون توجيه تراجعي أو تكراري.

اعتبارًا من 0.8.9: تم تنفيذ **عمليات البحث التكرارية** بدون تكرار—أكثر كفاءة وموثوقية ومناسبة للمعرفة غير المكتملة بـ floodfill. ومع نمو الشبكات ومع معرفة routers بعدد أقل من floodfills، تقترب عمليات البحث من تعقيد O(log n).

تستمر عمليات البحث التكرارية حتى عند عدم وجود إحالات إلى نظراء أقرب، مما يمنع الحجب الخبيث black-holing (إسقاط الطلبات دون تمريرها أو الرد عليها). يُطبَّق الحد الأقصى الحالي لعدد الاستعلامات والمهلة الزمنية.

### 8.9 التحقق

**RouterInfo Verification**: تم تعطيلها اعتباراً من 0.9.7.1 لمنع الهجمات الموصوفة في الورقة البحثية "Practical Attacks Against the I2P Network".

**التحقق من LeaseSet**: Routers تنتظر ~10 ثوانٍ، ثم تُجري استعلامًا من floodfill (عقدة مخصّصة لنشر netDb) مختلف عبر outbound client tunnel. يُخفي garlic encryption من الطرف إلى الطرف ذلك عن نقطة النهاية الصادرة. تعود الردود عبر inbound tunnels.

اعتباراً من 0.9.7، تُشفَّر الردود مع إخفاء مفتاح الجلسة/الوسم عن بوابة الدخول.

### 8.10 الاستكشاف

**الاستكشاف** يتضمّن استعلام netdb باستخدام مفاتيح عشوائية للتعرّف على routers جديدة. تستجيب Floodfills برسالة `DatabaseSearchReplyMessage` تحتوي على تجزئات routers غير-floodfill القريبة من المفتاح المطلوب. تقوم استعلامات الاستكشاف بتعيين علم خاص في `DatabaseLookupMessage`.

---

## 9. MultiHoming (الاتصال عبر عدة مزودين/واجهات شبكة)

يمكن تشغيل الوجهات التي تستخدم مفاتيح خاصة/عامة متطابقة (الطريقة التقليدية `eepPriv.dat`) على عدة routers في الوقت نفسه. ينشر كل مثيل دوريًا LeaseSets موقعة؛ يُعاد أحدث LeaseSet منشور إلى طالبي الاستعلام. ومع حد أقصى لعمر LeaseSet يبلغ 10 دقائق، فإن فترات الانقطاع لا تستمر لأكثر من ~10 دقائق.

اعتباراً من 0.9.38، تدعم **Meta LeaseSets** الخدمات متعددة الموطن الكبيرة باستخدام Destinations (وجهات) منفصلة توفّر خدمات مشتركة. عناصر Meta LeaseSet هي Destinations أو Meta LeaseSets أخرى بفترات صلاحية تصل إلى 18.2 ساعة، مما يتيح وجود مئات/آلاف Destinations لاستضافة الخدمات المشتركة.

---

## 10. تحليل التهديدات

يعمل حاليًا نحو 1700 floodfill routers. يسهم نمو الشبكة في جعل معظم الهجمات أكثر صعوبة أو أقل تأثيرًا.

### 10.1 تدابير التخفيف العامة

- **النمو**: المزيد من floodfills يجعل الهجمات أصعب أو أقل تأثيرًا
- **التكرار**: تُخزَّن جميع مدخلات netdb على 3 floodfill routers الأقرب إلى المفتاح عبر الإغراق
- **التواقيع**: جميع المدخلات موقعة من المنشئ؛ التزوير مستحيل

### 10.2 Routers البطيئة أو غير المستجيبة

تحتفظ Routers بإحصاءات موسّعة لملف تعريف القرين لـ floodfills: - متوسط زمن الاستجابة - نسبة الإجابة على الاستعلام - نسبة نجاح التحقق من التخزين - آخر عملية تخزين ناجحة - آخر عملية بحث ناجحة - آخر استجابة

Routers تستخدم هذه المقاييس عند تحديد "الجودة" لاختيار أقرب floodfill. يتم بسرعة التعرف على routers غير المستجيبة تمامًا وتجنّبها؛ أما routers الخبيثة جزئيًا فتشكّل تحديًا أكبر.

### 10.3 هجوم سيبيل (فضاء المفاتيح الكامل)

قد يعمد المهاجمون إلى إنشاء أعداد كبيرة من floodfill routers موزعة في جميع أنحاء فضاء المفاتيح، كوسيلة فعّالة لهجوم حجب الخدمة (DOS).

إذا لم يكن سوء السلوك كافياً للحصول على تصنيف "سيئ"، فقد تشمل الاستجابات الممكنة:
- تجميع قوائم تجزئة/عناوين IP للـ router "السيئة" والإعلان عنها عبر أخبار وحدة التحكم، والموقع، والمنتدى
- تمكين floodfill على مستوى الشبكة ("مواجهة Sybil (هجوم سيبيل) بمزيد من Sybil")
- إصدارات برمجية جديدة بقوائم "سيئة" مدمجة بشكل ثابت
- تحسين مقاييس ملفات تعريف الأقران والعتبات الخاصة بالتعرّف التلقائي
- معايير تأهيل كتل IP تستبعد وجود عدة floodfill ضمن كتلة IP واحدة
- قائمة سوداء تلقائية قائمة على الاشتراك (مشابهة لإجماع Tor)

الشبكات الأكبر تجعل الأمر أصعب.

### 10.4 هجوم سيبيل (فضاء مفاتيح جزئي)

قد ينشئ المهاجمون 8–15 routers من نوع floodfill متقاربة ومجمَّعة ضمن فضاء المفاتيح. تُوجَّه جميع عمليات البحث/التخزين لذلك الفضاء نحو routers المهاجم، ممّا يتيح تنفيذ هجوم حجب الخدمة (DoS) على مواقع I2P معيّنة.

نظرًا لأن فضاء المفاتيح مُفهرس باستخدام تجزئات SHA256 التشفيرية، يحتاج المهاجمون إلى استخدام القوة الغاشمة لتوليد routers بقربٍ كافٍ في فضاء المفاتيح.

**الدفاع**: تتغير خوارزمية القرب في Kademlia (بروتوكول DHT) بمرور الوقت باستخدام `SHA256(key + YYYYMMDD)`، وتتبدّل يومياً عند منتصف الليل بتوقيت UTC. هذا **تدوير فضاء المفاتيح** يفرض إعادة توليد الهجوم يومياً.

> **ملاحظة**: تُظهر أبحاث حديثة أن تدوير فضاء المفاتيح ليس فعالًا بشكل خاص—إذ يستطيع المهاجمون حساب تجزئات router مسبقًا، ولا يلزمهم سوى عدة routers لحجب أجزاء من فضاء المفاتيح خلال نصف ساعة بعد التدوير.

نتيجة التدوير اليومي: تصبح netdb الموزعة غير موثوقة لدقائق بعد التدوير—تفشل عمليات البحث قبل أن يتلقى أقرب router جديد عمليات التخزين.

### 10.5 هجمات التمهيد

قد يتمكن المهاجمون من السيطرة على مواقع reseed (إعادة البذر) أو خداع المطورين لإضافة مواقع reseed عدائية، مما يؤدي إلى إقلاع routers الجديدة داخل شبكات معزولة أو خاضعة لسيطرة الأغلبية.

**الدفاعات المُنفَّذة:** - جلب مجموعات فرعية من RouterInfo من عدة مواقع reseed (إعادة البذر: آلية تزويد الـ router بقائمة أولية من نظراء I2P عند البدء) بدلاً من موقع واحد - مراقبة reseed خارج الشبكة عبر استطلاع المواقع دورياً - اعتباراً من 0.9.14، تُحزَّم بيانات reseed كملفات zip موقَّعة مع التحقق من التوقيع المُنزَّل (انظر [مواصفة su3](/docs/specs/updates))

### 10.6 التقاط الاستعلام

قد تقوم Floodfill routers بـ"توجيه" الأقران إلى routers خاضعة لسيطرة المهاجم عبر المراجع المُعادة.

غير محتمل عبر الاستكشاف بسبب انخفاض التواتر؛ تحصل routers على مراجع الأقران أساساً عبر بناء tunnel العادي.

اعتباراً من الإصدار 0.8.9، تم تنفيذ عمليات بحث تكرارية. تُتَّبع مراجع floodfill الواردة في `DatabaseSearchReplyMessage` إذا كانت أقرب إلى مفتاح البحث. الـrouters الطالبة لا تثق في مدى قرب المرجع. تستمر عمليات البحث رغم عدم وجود مفاتيح أقرب، وذلك حتى انقضاء المهلة/بلوغ الحد الأقصى لعدد الاستعلامات، ما يمنع black-holing (حجباً متعمداً لحركة المرور) خبيثاً.

### 10.7 تسريبات المعلومات

تسرُّب المعلومات في DHT (جدول التجزئة الموزع) ضمن I2P يحتاج إلى مزيد من التحقيق. تقوم Floodfill routers برصد الاستعلامات وجمع المعلومات. عند وصول نسبة العقد الخبيثة إلى 20%، تصبح تهديدات Sybil (هجمات سيبيل) المذكورة سابقاً إشكاليةً لأسباب متعددة.

---

## 11. العمل المستقبلي

- تشفير من الطرف إلى الطرف لاستعلامات netDb الإضافية واستجاباتها
- أساليب أفضل لتتبّع استجابات الاستعلام
- أساليب تخفيف لمشكلات الموثوقية المتعلقة بتدوير فضاء المفاتيح

---

## 12. المراجع

- [مواصفة البُنى الشائعة](/docs/specs/common-structures/) – هياكل RouterInfo (بيانات تعريف الـ router) و LeaseSet (مجموعة بيانات مسارات الدخول)
- [مواصفة I2NP (بروتوكول شبكة I2P الداخلي)](/docs/specs/i2np/) – أنواع رسائل قاعدة البيانات
- [الاقتراح 123: إدخالات netDb (قاعدة بيانات الشبكة الموزّعة) الجديدة](/proposals/123-new-netdb-entries) – مواصفة LeaseSet2 (الإصدار الثاني من LeaseSet)
- [مناقشة netDb التاريخية](/docs/netdb/) – تاريخ التطوير والمناقشات المؤرشفة
