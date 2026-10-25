---
title: "بروتوكول عميل I2P (I2CP)"
description: "كيف تتفاوض التطبيقات على الجلسات والأنفاق وmجموعات الإيجار (LeaseSets) مع router الشبكة I2P."
slug: "i2cp"
aliases:
  - "/ar/docs/api/i2cp"
  - "/ar/docs/api/i2cp/"
  - "/ar/docs/specs/i2cp-spec"
  - "/ar/docs/specs/i2cp-spec/"
category: "البروتوكولات"
lastUpdated: "2025-07"
accurateFor: "0.9.67"
---

## نظرة عامة

هذه هي مواصفات بروتوكول I2P Control Protocol (I2CP)، وهو الواجهة منخفضة المستوى بين العملاء والـ router. عملاء Java سيستخدمون واجهة برمجة تطبيقات عميل I2CP، والتي تنفذ هذا البروتوكول.

لا توجد تطبيقات معروفة غير مكتوبة بـ Java لمكتبة من جانب العميل تنفذ I2CP. بالإضافة إلى ذلك، التطبيقات الموجهة للمقابس (streaming) ستحتاج إلى تنفيذ بروتوكول streaming، لكن لا توجد مكتبات غير مكتوبة بـ Java لذلك أيضاً. لذلك، يجب على العملاء غير المكتوبين بـ Java استخدام البروتوكول عالي المستوى SAM [SAMv3](/docs/api/samv3/) بدلاً من ذلك، والذي تتوفر له مكتبات بعدة لغات.

هذا بروتوكول منخفض المستوى مدعوم داخليًا وخارجيًا من قبل Java I2P router. يتم تسلسل البروتوكول فقط إذا لم يكن العميل وال router في نفس JVM؛ وإلا فإن رسائل I2CP Java objects يتم تمريرها عبر واجهة JVM داخلية. I2CP مدعوم أيضًا خارجيًا من قبل C++ router i2pd.

معلومات أكثر متاحة في صفحة نظرة عامة على I2CP [I2CP](/docs/specs/i2cp/).

## الجلسات

تم تصميم البروتوكول للتعامل مع عدة "جلسات"، كل منها بمعرف جلسة من 2 بايت، عبر اتصال TCP واحد، ومع ذلك، لم يتم تنفيذ الجلسات المتعددة حتى الإصدار 0.9.21. راجع [قسم الجلسات المتعددة أدناه](#multisession). لا تحاول استخدام جلسات متعددة على اتصال I2CP واحد مع routers أقدم من الإصدار 0.9.21.

يبدو أيضًا أن هناك بعض الأحكام لعميل واحد للتحدث مع عدة routers عبر اتصالات منفصلة. هذا أيضًا غير مختبر، وربما غير مفيد.

لا توجد طريقة للحفاظ على الجلسة بعد قطع الاتصال، أو لاستعادتها على اتصال I2CP مختلف. عند إغلاق المقبس، يتم تدمير الجلسة.

## أمثلة على تسلسل الرسائل

ملاحظة: الأمثلة أدناه لا تُظهر بايت البروتوكول (0x2a) الذي يجب إرساله من العميل إلى الـ router عند الاتصال لأول مرة. يمكن العثور على مزيد من المعلومات حول تهيئة الاتصال في صفحة نظرة عامة على I2CP [I2CP](/docs/specs/i2cp/).

### إنشاء جلسة قياسية

```
  Client                                           Router

                           --------------------->  Get Date Message
        Set Date Message  <---------------------
                           --------------------->  Create Session Message
  Session Status Message  <---------------------
Request LeaseSet Message  <---------------------
                           --------------------->  Create LeaseSet Message

```
### الحصول على حدود عرض النطاق (جلسة بسيطة)

```
  Client                                           Router

                           --------------------->  Get Bandwidth Limits Message
Bandwidth Limits Message  <---------------------

```
### البحث عن الوجهة (جلسة بسيطة)

```
  Client                                           Router

                           --------------------->  Dest Lookup Message
      Dest Reply Message  <---------------------

```
### الرسالة الصادرة

جلسة موجودة، مع i2cp.messageReliability=none

```
  Client                                           Router

                           --------------------->  Send Message Message

```
جلسة موجودة، مع i2cp.messageReliability=none و nonce غير صفري

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (succeeded)

```
جلسة موجودة، مع i2cp.messageReliability=BestEffort

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (accepted)
  Message Status Message  <---------------------
  (succeeded)

```
### الرسالة الواردة

جلسة موجودة، مع i2cp.fastReceive=true (اعتباراً من الإصدار 0.9.4)

```
  Client                                           Router

 Message Payload Message  <---------------------

```
جلسة موجودة، مع i2cp.fastReceive=false (مهجور)

```
  Client                                           Router

  Message Status Message  <---------------------
  (available)
                           --------------------->  Receive Message Begin Message
 Message Payload Message  <---------------------
                           --------------------->  Receive Message End Message

```
### ملاحظات الجلسات المتعددة {#multisession}

الجلسات المتعددة على اتصال I2CP واحد مدعومة اعتباراً من إصدار router 0.9.21. الجلسة الأولى التي يتم إنشاؤها هي "الجلسة الأساسية". الجلسات الإضافية هي "جلسات فرعية". تُستخدم الجلسات الفرعية لدعم وجهات متعددة تتشارك مجموعة مشتركة من tunnels. التطبيق الأولي هو أن تستخدم الجلسة الأساسية مفاتيح توقيع ECDSA، بينما تستخدم الجلسة الفرعية مفاتيح توقيع DSA للتواصل مع eepsites القديمة.

تتشارك الجلسات الفرعية نفس مجمعات الأنفاق الواردة والصادرة مع الجلسة الأساسية. يجب أن تستخدم الجلسات الفرعية نفس مفاتيح التشفير الخاصة بالجلسة الأساسية. وهذا ينطبق على كل من مفاتيح تشفير leaseSet ومفاتيح تشفير الوجهة (غير المستخدمة). يجب أن تستخدم الجلسات الفرعية مفاتيح توقيع مختلفة في الوجهة، لذا فإن hash الوجهة يختلف عن الجلسة الأساسية. وحيث أن الجلسات الفرعية تستخدم نفس مفاتيح التشفير والأنفاق الخاصة بالجلسة الأساسية، فمن الواضح للجميع أن الوجهات تعمل على نفس router، وبالتالي فإن ضمانات إخفاء الهوية المضادة للارتباط المعتادة لا تنطبق.

يتم إنشاء الجلسات الفرعية عن طريق إرسال رسالة CreateSession وتلقي رسالة SessionStatus كرد، كالمعتاد. يجب إنشاء الجلسات الفرعية بعد إنشاء الجلسة الأساسية. ستحتوي استجابة SessionStatus، عند النجاح، على معرف جلسة فريد، مختلف عن المعرف الخاص بالجلسة الأساسية. بينما يجب معالجة رسائل CreateSession بالترتيب، لا توجد طريقة مؤكدة لربط رسالة CreateSession بالاستجابة، لذلك يجب ألا يكون لدى العميل عدة رسائل CreateSession معلقة في نفس الوقت. قد لا يتم احترام خيارات SessionConfig للجلسة الفرعية عندما تختلف عن الجلسة الأساسية. على وجه الخصوص، نظراً لأن الجلسات الفرعية تستخدم نفس مجموعة tunnel كالجلسة الأساسية، فقد يتم تجاهل خيارات tunnel.

سيقوم الـ router بإرسال رسائل RequestVariableLeaseSet منفصلة لكل Destination إلى العميل، ويجب على العميل الرد برسالة CreateLeaseSet لكل منها. لن تكون الـ leases للـ Destinations الاثنين متطابقة بالضرورة، حتى لو تم اختيارها من نفس مجموعة الـ tunnel.

يمكن تدمير الجلسة الفرعية باستخدام رسالة DestroySession كالمعتاد. هذا لن يدمر الجلسة الأساسية أو يوقف اتصال I2CP. تدمير الجلسة الأساسية سيؤدي، مع ذلك، إلى تدمير جميع الجلسات الفرعية وإيقاف اتصال I2CP. رسالة Disconnect تدمر جميع الجلسات.

لاحظ أن معظم رسائل I2CP، وليس جميعها، تحتوي على معرف جلسة. بالنسبة للرسائل التي لا تحتوي على معرف جلسة، قد يحتاج العملاء إلى منطق إضافي للتعامل بشكل صحيح مع ردود router. DestLookup و DestReply لا تحتويان على معرفات الجلسة؛ استخدم بدلاً من ذلك HostLookup و HostReply الأحدث. GetBandwidthLimts و BandwidthLimits لا تحتويان على معرفات جلسة، ومع ذلك فإن الاستجابة ليست خاصة بجلسة معينة.

### ملاحظات الإصدار {#notes}

لا يُتوقع أن يتغير بايت إصدار البروتوكول الأولي (0x2a) المُرسل من العميل. قبل الإصدار 0.8.7، لم تكن معلومات إصدار الـ router متاحة للعميل، مما منع العملاء الجدد من العمل مع الـ routers القديمة. اعتباراً من الإصدار 0.8.7، يتم تبادل سلاسل إصدار البروتوكول للطرفين في رسائل Get/Set Date. مستقبلاً، يمكن للعملاء استخدام هذه المعلومات للتواصل بشكل صحيح مع الـ routers القديمة. يجب على العملاء والـ routers عدم إرسال رسائل غير مدعومة من الطرف الآخر، حيث أنها عادة ما تقطع الجلسة عند استلام رسالة غير مدعومة.

معلومات الإصدار المتبادلة هي إصدار واجهة برمجة التطبيقات "الأساسية" أو إصدار بروتوكول I2CP، وليست بالضرورة إصدار router.

ملخص أساسي لإصدارات بروتوكول I2CP كما يلي. للتفاصيل، انظر أدناه.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Required I2CP Features</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.67</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">PQ Hybrid ML-KEM (enc types 5-7) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host lookup/reply extensions (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MessageStatus message Loopback error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 (enc type 4) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BlindingInfo message supported; Additional HostReply message failure codes</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet options; MessageStatus message Meta LS error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">CreateLeaseSet2 message and options supported; Dest/LS key certs w/ RedDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Preliminary CreateLeaseSet2 message supported (abandoned)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Multiple sessions on a single I2CP connection supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional SetDate messages may be sent to the client at any time</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Authentication, if enabled, is required via GetDate before all other messages</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Per-message override of messageReliability=none with nonzero nonce</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types supported; RSA sig types also supported but currently unused</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host Lookup and Host Reply messages supported; Authentication mapping in Get Date message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Request Variable Lease Set message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional Message Status codes defined</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message nonce=0 allowed; Fast receive mode is the default</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag tag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a lease set (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Date and Set Date version strings included. If not present, the client or router is version 0.8.6 or older.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Get Bandwidth messages supported in standard session; Concurrent Dest Lookup messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability=none supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Bandwidth Limits and Bandwidth Limits messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires message supported; Reconfigure Session message supported; Ports and protocol numbers in gzip header</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Dest Reply messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
</table>
## الهياكل الشائعة {#structures}

### رأس رسالة I2CP {#struct-I2CPMessageHeader}

#### الوصف

رأس مشترك لجميع رسائل I2CP، يحتوي على طول الرسالة ونوع الرسالة.

#### المحتويات

1.  4 بايت [Integer](/docs/specs/common-structures/#integer) تحدد طول
    جسم الرسالة
2.  1 بايت [Integer](/docs/specs/common-structures/#integer) تحدد نوع الرسالة.
3.  جسم رسالة I2CP، 0 أو أكثر من البايتات

#### ملاحظات

الحد الأقصى الفعلي لطول الرسالة هو حوالي 64 كيلوبايت.

### معرف الرسالة {#struct-MessageId}

#### الوصف

يحدد بشكل فريد رسالة في انتظار على router معين في نقطة زمنية محددة. يتم إنشاء هذا دائماً بواسطة الـ router وليس نفس الـ nonce الذي ينشئه العميل.

#### المحتويات

1.  4 بايت [Integer](/docs/specs/common-structures/#integer)

#### ملاحظات

معرفات الرسائل فريدة داخل الجلسة فقط؛ وهي ليست فريدة على مستوى النظام بالكامل.

### الحمولة {#struct-Payload}

#### الوصف

هذا الهيكل هو محتوى رسالة يتم تسليمها من وجهة إلى أخرى.

#### المحتويات

1.  4 بايت طول [Integer](/docs/specs/common-structures/#integer)
2.  عدد البايتات المقابل

#### ملاحظات

الحمولة في تنسيق gzip كما هو محدد في صفحة نظرة عامة على I2CP [I2CP-FORMAT](/docs/specs/i2cp/#format).

الحد الفعلي لطول الرسالة هو حوالي 64 كيلوبايت.

### إعدادات الجلسة {#struct-SessionConfig}

#### الوصف

يحدد خيارات التكوين لجلسة عميل معينة.

#### المحتويات

1.  [Destination](/docs/specs/common-structures/#destination)
2.  [Mapping](/docs/specs/common-structures/#mapping) للخيارات
3.  [Date](/docs/specs/common-structures/#date) الإنشاء
4.  [Signature](/docs/specs/common-structures/#signature) للحقول الثلاثة السابقة،
    موقعة بواسطة [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)

#### ملاحظات

- يتم تحديد الخيارات في صفحة نظرة عامة على I2CP
  [I2CP-OPTIONS](/docs/specs/i2cp/#options).
- يجب ترتيب [Mapping](/docs/specs/common-structures/#mapping) حسب المفتاح حتى
  يتم التحقق من صحة التوقيع بشكل صحيح في router.
- يجب أن يكون تاريخ الإنشاء ضمن +/- 30 ثانية من الوقت الحالي
  عند معالجته بواسطة router، وإلا سيتم رفض الإعداد.

#### التوقيعات غير المتصلة

- إذا كان [Destination](/docs/specs/common-structures/#destination) موقعاً بشكل غير متصل،
  فيجب أن يحتوي [Mapping](/docs/specs/common-structures/#mapping) على الخيارات الثلاثة
  i2cp.leaseSetOfflineExpiration و i2cp.leaseSetTransientPublicKey و
  i2cp.leaseSetOfflineSignature. يتم بعد ذلك إنشاء
  [Signature](/docs/specs/common-structures/#signature) بواسطة
  [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) المؤقت ويتم
  التحقق منه باستخدام [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
  المحدد في i2cp.leaseSetTransientPublicKey. راجع
  [I2CP-OPTIONS](/docs/specs/i2cp/#options) للتفاصيل.

### معرف الجلسة {#struct-SessionId}

#### الوصف

يحدد بشكل فريد جلسة على router معين في نقطة زمنية محددة.

#### المحتويات

1.  2 بايت [Integer](/docs/specs/common-structures/#integer)

#### ملاحظات

يتم استخدام معرف الجلسة 0xffff للإشارة إلى "عدم وجود جلسة"، على سبيل المثال لعمليات البحث عن أسماء المضيفين.

## الرسائل

انظر أيضاً [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html).

### أنواع الرسائل {#types}

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Direction</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BandwidthLimitsMessage">BandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BlindingInfoMessage">BlindingInfoMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">42</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSetMessage">CreateLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSet2Message">CreateLeaseSet2Message</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateSessionMessage">CreateSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestLookupMessage">DestLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">34</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestReplyMessage">DestReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">35</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestroySessionMessage">DestroySessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DisconnectMessage">DisconnectMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetBandwidthLimitsMessage">GetBandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetDateMessage">GetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostLookupMessage">HostLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostReplyMessage">HostReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessagePayloadMessage">MessagePayloadMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">31</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessageStatusMessage">MessageStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageBeginMessage">ReceiveMessageBeginMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageEndMessage">ReceiveMessageEndMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReportAbuseMessage">ReportAbuseMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">29</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestLeaseSetMessage">RequestLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestVariableLeaseSetMessage">RequestVariableLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">37</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageMessage">SendMessageMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageExpiresMessage">SendMessageExpiresMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SessionStatusMessage">SessionStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SetDateMessage">SetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">33</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### BandwidthLimitsMessage {#BandwidthLimitsMessage}

#### الوصف

أخبر العميل عن حدود عرض النطاق الترددي.

يُرسل من router إلى العميل كاستجابة لـ [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage).

#### المحتويات

1.  4 بايت [Integer](/docs/specs/common-structures/#integer) حد العميل الوارد
    (KBps)
2.  4 بايت [Integer](/docs/specs/common-structures/#integer) حد العميل الصادر
    (KBps)
3.  4 بايت [Integer](/docs/specs/common-structures/#integer) حد router الوارد
    (KBps)
4.  4 بايت [Integer](/docs/specs/common-structures/#integer) حد انفجار router الوارد
    (KBps)
5.  4 بايت [Integer](/docs/specs/common-structures/#integer) حد router الصادر
    (KBps)
6.  4 بايت [Integer](/docs/specs/common-structures/#integer) حد انفجار router الصادر
    (KBps)
7.  4 بايت [Integer](/docs/specs/common-structures/#integer) وقت انفجار router
    (ثواني)
8.  تسعة 4-بايت [Integer](/docs/specs/common-structures/#integer) (غير محدد)

#### ملاحظات

قد تكون حدود العميل القيم الوحيدة المحددة، وقد تكون الحدود الفعلية للـ router، أو نسبة مئوية من حدود الـ router، أو خاصة بعميل معين، حسب التنفيذ. جميع القيم المصنفة كحدود router قد تكون 0، حسب التنفيذ. اعتباراً من الإصدار 0.7.2.

### BlindingInfoMessage {#BlindingInfoMessage}

#### الوصف

أخبر الـ router أن الوجهة مخفية، مع كلمة مرور البحث الاختيارية والمفتاح الخاص الاختياري لفك التشفير. راجع المقترحات 123 و 149 للتفاصيل.

يحتاج الـ router إلى معرفة ما إذا كان الوجهة مخفية. إذا كانت مخفية وتستخدم مصادقة سرية أو لكل عميل، فإنه يحتاج إلى الحصول على تلك المعلومات أيضاً.

البحث عن المضيف لعنوان b32 بصيغة جديدة ("b33") يخبر الموجه أن العنوان مخفي، ولكن لا توجد آلية لتمرير المفتاح السري أو المفتاح الخاص إلى الموجه في رسالة البحث عن المضيف. بينما يمكننا توسيع رسالة البحث عن المضيف لإضافة تلك المعلومات، فإن تعريف رسالة جديدة أكثر وضوحاً.

تُوفر هذه الرسالة طريقة برمجية للعميل لإخبار الـ router. وإلا، فسيتوجب على المستخدم تكوين كل وجهة يدوياً.

#### الاستخدام

قبل أن يرسل العميل رسالة إلى وجهة مخفية، يجب عليه إما البحث عن "b33" في رسالة Host Lookup، أو إرسال رسالة Blinding Info. إذا كانت الوجهة المخفية تتطلب سراً أو مصادقة لكل عميل، فيجب على العميل إرسال رسالة Blinding Info.

لا يرسل الـ router ردًا على هذه الرسالة. يتم الإرسال من العميل إلى الـ router.

#### المحتويات

1.  [معرف الجلسة](#struct-sessionid)
2.  1 بايت [عدد صحيح](/docs/specs/common-structures/#integer) أعلام

> - ترتيب البتات: 76543210 > - البت 0: 0 للجميع، 1 لكل عميل > - البتات 3-1: مخطط المصادقة، إذا تم تعيين البت 0 إلى 1 لكل >   عميل، وإلا 000 >   - 000: مصادقة العميل DH (أو عدم وجود مصادقة لكل عميل) >   - 001: مصادقة العميل PSK > - البت 4: 1 إذا كان السر مطلوباً، 0 إذا لم يكن السر مطلوباً > - البتات 7-5: غير مستخدمة، تعيين إلى 0 للتوافق المستقبلي

3. 1 بايت [Integer](/docs/specs/common-structures/#integer) نوع نقطة النهاية

> - النوع 0 هو [Hash](/docs/specs/common-structures/#hash) > - النوع 1 هو اسم المضيف [String](/docs/specs/common-structures/#string) > - النوع 2 هو [Destination](/docs/specs/common-structures/#destination) > - النوع 3 هو نوع التوقيع و >   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)

4.  2 بايت [Integer](/docs/specs/common-structures/#integer) نوع التوقيع المعمى
5.  4 بايت [Integer](/docs/specs/common-structures/#integer) ثواني انتهاء الصلاحية منذ
    العصر
6.  نقطة النهاية: البيانات كما هو محدد، واحدة من

> - النوع 0: 32 بايت [Hash](/docs/specs/common-structures/#hash) > > - النوع 1: اسم المضيف [String](/docs/specs/common-structures/#string) > > - النوع 2: ثنائي [Destination](/docs/specs/common-structures/#destination) > >  > >  - النوع 3: 2 بايت [Integer](/docs/specs/common-structures/#integer) نوع التوقيع، متبوعاً بـ > >  -   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) (الطول كما >       يقترحه نوع التوقيع)

7.  [PrivateKey](/docs/specs/common-structures/#privatekey) مفتاح فك التشفير موجود فقط
    إذا تم تعيين بت العلم 0 إلى 1. مفتاح خاص ECIES_X25519 بحجم 32 بايت،
    little-endian
8.  [String](/docs/specs/common-structures/#string) كلمة مرور البحث موجودة فقط إذا
    تم تعيين بت العلم 4 إلى 1.

#### ملاحظات

- اعتباراً من الإصدار 0.9.43.
- نوع نقطة النهاية Hash غالباً لا يكون مفيداً ما لم يتمكن الـ router من إجراء بحث عكسي في دفتر العناوين للحصول على الـ Destination.
- نوع نقطة النهاية hostname غالباً لا يكون مفيداً ما لم يتمكن الـ router من إجراء بحث في دفتر العناوين للحصول على الـ Destination.

### CreateLeaseSetMessage {#CreateLeaseSetMessage}

مُهمل. لا يمكن استخدامه مع LeaseSet2، أو المفاتيح غير المتصلة، أو أنواع التشفير غير ElGamal، أو أنواع التشفير المتعددة، أو LeaseSets المشفرة. استخدم CreateLeaseSet2Message مع جميع routers الإصدار 0.9.39 أو أعلى.

#### الوصف

يتم إرسال هذه الرسالة استجابة لـ [RequestLeaseSetMessage](#RequestLeaseSetMessage) أو [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) وتحتوي على جميع هياكل [Lease](/docs/specs/common-structures/#lease) التي يجب نشرها إلى قاعدة بيانات شبكة I2NP.

مُرسل من العميل إلى الموجه.

#### المحتويات

1.  [Session ID](#struct-sessionid)
2.  DSA [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) أو 20
    بايت يتم تجاهلها
3.  [PrivateKey](/docs/specs/common-structures/#privatekey)
4.  [LeaseSet](/docs/specs/common-structures/#leaseset)

#### ملاحظات

يتطابق SigningPrivateKey مع [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) من داخل LeaseSet، فقط إذا كان نوع مفتاح التوقيع هو DSA. هذا مخصص لإبطال LeaseSet، والذي لم يتم تنفيذه ومن غير المحتمل أن يتم تنفيذه أبداً. إذا لم يكن نوع مفتاح التوقيع DSA، فإن هذا الحقل يحتوي على 20 بايت من البيانات العشوائية. طول هذا الحقل هو دائماً 20 بايت، ولا يساوي أبداً طول مفتاح التوقيع الخاص غير DSA.

يطابق PrivateKey الـ [PublicKey](/docs/specs/common-structures/#publickey) من LeaseSet. PrivateKey ضروري لفك تشفير الرسائل المرسلة عبر garlic routing.

الإلغاء غير مُنفّذ. الاتصال بعدة routers غير مُنفّذ في أي مكتبة عميل.

### CreateLeaseSet2Message {#CreateLeaseSet2Message}

#### الوصف

يتم إرسال هذه الرسالة كاستجابة لـ [RequestLeaseSetMessage](#RequestLeaseSetMessage) أو [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) وتحتوي على جميع هياكل [Lease](/docs/specs/common-structures/#lease) التي يجب نشرها في قاعدة بيانات شبكة I2NP.

مُرسل من العميل إلى الـ router. منذ الإصدار 0.9.39. المصادقة لكل عميل لـ EncryptedLeaseSet مدعومة اعتباراً من الإصدار 0.9.41. MetaLeaseSet غير مدعوم بعد عبر I2CP. انظر الاقتراح 123 لمزيد من المعلومات.

#### المحتويات

1.  [معرف الجلسة](#struct-sessionid)
2.  بايت واحد لنوع leaseSet المتبع.

> - النوع 1 هو [LeaseSet](/docs/specs/common-structures/#leaseset) (مهجور) > - النوع 3 هو [LeaseSet2](/docs/specs/common-structures/#leaseset2) > - النوع 5 هو [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) > - النوع 7 هو [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)

3.  [LeaseSet](/docs/specs/common-structures/#leaseset) أو
    [LeaseSet2](/docs/specs/common-structures/#leaseset2) أو
    [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) أو
    [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
4.  بايت واحد يحدد عدد المفاتيح الخاصة التي ستتبع.
5.  قائمة [PrivateKey](/docs/specs/common-structures/#privatekey). واحد لكل مفتاح عام في lease set، بنفس الترتيب. (غير موجود لـ Meta LS2)

> - نوع التشفير (2 بايت [Integer](/docs/specs/common-structures/#integer)) > - طول مفتاح التشفير (2 بايت [Integer](/docs/specs/common-structures/#integer)) > - [PrivateKey](/docs/specs/common-structures/#privatekey) التشفير (عدد البايتات >   المحددة)

#### ملاحظات

تتطابق PrivateKeys مع كل من [PublicKey](/docs/specs/common-structures/#publickey) من LeaseSet. إن PrivateKeys ضرورية لفك تشفير الرسائل المُوجهة عبر garlic encryption.

راجع المقترح 123 للمزيد من المعلومات حول leaseSet المشفرة.

محتويات وتنسيق MetaLeaseSet أولية وقابلة للتغيير. لا يوجد بروتوكول محدد لإدارة عدة routers. راجع الاقتراح 123 للمزيد من المعلومات.

مفتاح التوقيع الخاص، الذي كان محدداً مسبقاً للإلغاء وغير مستخدم، غير موجود في LS2.

الإصدار الأولي مع نوع الرسالة 40 كان في 0.9.38 ولكن تم تغيير التنسيق. النوع 40 مهجور وغير مدعوم. النوع 41 غير صالح حتى 0.9.39.

### CreateSessionMessage {#CreateSessionMessage}

#### الوصف

يتم إرسال هذه الرسالة من عميل لبدء جلسة، حيث يتم تعريف الجلسة كاتصال Destination واحد بالشبكة، والتي سيتم تسليم جميع الرسائل لذلك Destination إليها ومن خلالها سيتم إرسال جميع الرسائل التي يرسلها ذلك Destination إلى أي Destination آخر.

يتم إرساله من العميل إلى الـ router. يستجيب الـ router برسالة [SessionStatusMessage](#SessionStatusMessage).

#### المحتويات

1.  [إعدادات الجلسة](#struct-sessionconfig)

#### ملاحظات

- هذه هي الرسالة الثانية المرسلة من العميل. سابقاً أرسل العميل
  [GetDateMessage](#GetDateMessage) وتلقى استجابة
  [SetDateMessage](#SetDateMessage).
- إذا كان التاريخ في إعداد الجلسة بعيداً جداً (أكثر من +/- 30
  ثانية) عن الوقت الحالي للـ router، سيتم رفض الجلسة.
- إذا كانت هناك جلسة موجودة بالفعل على الـ router لهذا الـ Destination، فسيتم
  رفض الجلسة.
- يجب ترتيب [Mapping](/docs/specs/common-structures/#mapping) في إعداد الجلسة
  حسب المفتاح حتى يتم التحقق من صحة التوقيع بشكل صحيح في الـ
  router.

### رسالة البحث عن الوجهة {#DestLookupMessage}

#### الوصف

يُرسل من العميل إلى الـ router. يرد الـ router برسالة [DestReplyMessage](#DestReplyMessage).

#### المحتويات

1.  SHA-256 [Hash](/docs/specs/common-structures/#hash)

#### ملاحظات

اعتبارًا من الإصدار 0.7.

اعتبارًا من الإصدار 0.8.3، يتم دعم عمليات البحث المتعددة المعلقة، كما يتم دعم عمليات البحث في كل من I2PSimpleSession والجلسات العادية.

[HostLookupMessage](#HostLookupMessage) مُفضل اعتباراً من الإصدار 0.9.11.

### DestReplyMessage {#DestReplyMessage}

#### الوصف

يُرسل من Router إلى العميل كاستجابة لـ [DestLookupMessage](#DestLookupMessage).

#### المحتويات

1.  [Destination](/docs/specs/common-structures/#destination) عند النجاح، أو
    [Hash](/docs/specs/common-structures/#hash) عند الفشل

#### ملاحظات

اعتباراً من الإصدار 0.7.

اعتباراً من الإصدار 0.8.3، يتم إرجاع Hash المطلوب في حالة فشل البحث، بحيث يمكن للعميل أن يكون لديه عدة عمليات بحث معلقة وربط الردود بعمليات البحث. لربط استجابة Destination بطلب، خذ Hash الخاص بـ Destination. قبل الإصدار 0.8.3، كانت الاستجابة فارغة عند الفشل.

### DestroySessionMessage {#DestroySessionMessage}

#### الوصف

يتم إرسال هذه الرسالة من العميل لتدمير جلسة.

يُرسل من العميل إلى الموجه (Router). يجب على الموجه أن يستجيب برسالة [SessionStatusMessage](#SessionStatusMessage) (محذوفة). ومع ذلك، راجع الملاحظات المهمة أدناه.

#### المحتويات

1.  [معرف الجلسة](#struct-sessionid)

#### ملاحظات

يجب على الـ router في هذه النقطة تحرير جميع الموارد المرتبطة بالجلسة.

من خلال API 0.9.66، فإن router Java I2P ومكتبات العميل تنحرف بشكل كبير عن هذه المواصفات. لا يرسل router أبداً استجابة SessionStatus(Destroyed). إذا لم تعد هناك جلسات متبقية، فإنه يرسل [DisconnectMessage](#DisconnectMessage). إذا كانت هناك جلسات فرعية أو الجلسة الأساسية متبقية، فإنه لا يرد.

تستجيب مكتبة عميل Java لرسالة SessionStatus عن طريق تدمير جميع الجلسات وإعادة الاتصال.

قد لا يكون تدمير الجلسات الفرعية الفردية على اتصال يحتوي على جلسات متعددة مختبرًا بالكامل أو يعمل بشكل صحيح على تطبيقات router والعميل المختلفة. استخدم الحذر.

يجب على التطبيقات التعامل مع إشارة destroy للجلسة الأساسية كإشارة destroy لجميع الجلسات الفرعية، ولكن السماح بإشارة destroy لجلسة فرعية واحدة والحفاظ على الاتصال مفتوحاً، ولكن Java I2P لا تقوم بذلك حالياً. إذا تم تغيير سلوك Java I2P في الإصدارات اللاحقة، فسيتم توثيق ذلك هنا.

### رسالة قطع الاتصال {#DisconnectMessage}

#### الوصف

أخبر الطرف الآخر أن هناك مشاكل وأن الاتصال الحالي على وشك أن يتم إنهاؤه. هذا ينهي جميع الجلسات على ذلك الاتصال. سيتم إغلاق المقبس قريباً. يُرسل إما من router إلى العميل أو من العميل إلى router.

#### المحتويات

1.  السبب [String](/docs/specs/common-structures/#string)

#### ملاحظات

مُنفَّذ فقط في اتجاه router إلى العميل، على الأقل في Java I2P.

### GetBandwidthLimitsMessage {#GetBandwidthLimitsMessage}

#### الوصف

اطلب من الـ router أن يوضح ما هي حدود النطاق الترددي الحالية له.

يتم إرسالها من العميل إلى الـ router. يستجيب الـ router برسالة [BandwidthLimitsMessage](#BandwidthLimitsMessage).

#### المحتويات

*لا يوجد*

#### ملاحظات

اعتباراً من الإصدار 0.7.2.

اعتباراً من الإصدار 0.8.3، مدعوم في كل من I2PSimpleSession وفي الجلسات القياسية.

### GetDateMessage {#GetDateMessage}

#### الوصف

يُرسل من العميل إلى الموجه. يستجيب الموجه برسالة [SetDateMessage](#SetDateMessage).

#### المحتويات

1.  إصدار I2CP API [String](/docs/specs/common-structures/#string)
2.  المصادقة [Mapping](/docs/specs/common-structures/#mapping) (اختياري، اعتباراً من
    الإصدار 0.9.11)

#### ملاحظات

- بشكل عام هي أول رسالة يرسلها العميل بعد إرسال بايت إصدار البروتوكول.
- يتم تضمين سلسلة الإصدار اعتباراً من الإصدار 0.8.7. هذا مفيد فقط إذا لم يكن العميل و router في نفس JVM. إذا لم تكن موجودة، فإن العميل هو إصدار 0.8.6 أو أقدم.
- اعتباراً من الإصدار 0.9.11، قد يتم تضمين المصادقة [Mapping](/docs/specs/common-structures/#mapping)، مع المفاتيح i2cp.username و i2cp.password. لا يحتاج Mapping إلى أن يكون مرتباً حيث أن هذه الرسالة غير موقعة. قبل وبما في ذلك 0.9.10، يتم تضمين المصادقة في [Session Config](#struct-sessionconfig) Mapping، ولا يتم فرض مصادقة لـ [GetDateMessage](#GetDateMessage)، [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage)، أو [DestLookupMessage](#DestLookupMessage). عند التمكين، تكون المصادقة عبر [GetDateMessage](#GetDateMessage) مطلوبة قبل أي رسائل أخرى اعتباراً من الإصدار 0.9.16. هذا مفيد فقط خارج سياق router. هذا تغيير غير متوافق، لكنه سيؤثر فقط على الجلسات خارج سياق router مع المصادقة، والتي يجب أن تكون نادرة.

### رسالة البحث عن المضيف {#HostLookupMessage}

#### الوصف

يُرسل من العميل إلى الموجه. يستجيب الموجه برسالة [HostReplyMessage](#HostReplyMessage).

هذا يحل محل [DestLookupMessage](#DestLookupMessage) ويضيف معرف طلب ومهلة زمنية ودعم البحث عن أسماء المضيفين. وبما أنه يدعم أيضاً عمليات البحث بالـ Hash، فيمكن استخدامه لجميع عمليات البحث إذا كان الـ router يدعمه. بالنسبة لعمليات البحث عن أسماء المضيفين، سيستعلم الـ router خدمة التسمية في سياقه. هذا مفيد فقط إذا كان العميل خارج سياق الـ router. داخل سياق الـ router، يجب على العميل الاستعلام من خدمة التسمية بنفسه، وهو أكثر كفاءة بكثير.

#### المحتويات

1.  [Session ID](#struct-sessionid)
2.  4 بايت [Integer](/docs/specs/common-structures/#integer) معرف الطلب
3.  4 بايت [Integer](/docs/specs/common-structures/#integer) المهلة الزمنية (ملي ثانية)
4.  1 بايت [Integer](/docs/specs/common-structures/#integer) نوع الطلب
5.  SHA-256 [Hash](/docs/specs/common-structures/#hash) أو اسم المضيف
    [String](/docs/specs/common-structures/#string) أو
    [Destination](/docs/specs/common-structures/#destination)

أنواع الطلبات:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Lookup key (item 5)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As of</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
</table>
الأنواع 2-4 تطلب إرجاع تخطيط الخيارات من LeaseSet في رسالة HostReply. انظر الاقتراح 167.

#### ملاحظات

- اعتباراً من الإصدار 0.9.11. استخدم [DestLookupMessage](#DestLookupMessage) للـ routers الأقدم.
- سيتم إرجاع معرف الجلسة ومعرف الطلب في [HostReplyMessage](#HostReplyMessage). استخدم 0xFFFF لمعرف الجلسة إذا لم تكن هناك جلسة.
- المهلة الزمنية مفيدة لعمليات البحث عن Hash. الحد الأدنى الموصى به 10,000 (10 ثوانٍ). في المستقبل قد تكون مفيدة أيضاً لعمليات البحث في خدمة الأسماء البعيدة. قد لا يتم احترام هذه القيمة لعمليات البحث عن أسماء المضيفين المحلية، والتي يجب أن تكون سريعة.
- البحث عن أسماء المضيفين بصيغة Base 32 مدعوم لكن من الأفضل تحويلها إلى Hash أولاً.

### HostReplyMessage {#HostReplyMessage}

#### الوصف

يُرسل من الـ Router إلى العميل كرد على [HostLookupMessage](#HostLookupMessage).

#### المحتويات

1.  [Session ID](#struct-sessionid)
2.  4 بايت [Integer](/docs/specs/common-structures/#integer) معرف الطلب
3.  1 بايت [Integer](/docs/specs/common-structures/#integer) رمز النتيجة

> - 0: نجح > - 1: فشل > - 2: كلمة مرور البحث مطلوبة (اعتباراً من 0.9.43) > - 3: المفتاح الخاص مطلوب (اعتباراً من 0.9.43) > - 4: كلمة مرور البحث والمفتاح الخاص مطلوبان (اعتباراً من 0.9.43) > - 5: فشل فك تشفير leaseSet (اعتباراً من 0.9.43) > - 6: فشل البحث عن leaseSet (اعتباراً من 0.9.66) > - 7: نوع البحث غير مدعوم (اعتباراً من 0.9.66)

4.  [Destination](/docs/specs/common-structures/#destination)، موجود فقط إذا كان رمز النتيجة صفراً، باستثناء أنه قد يُرجع أيضاً لأنواع البحث 2-4. انظر أدناه.
5.  [Mapping](/docs/specs/common-structures/#mapping)، موجود فقط إذا كان رمز النتيجة صفراً، يُرجع فقط لأنواع البحث 2-4. اعتباراً من 0.9.66. انظر أدناه.

#### الاستجابات لأنواع البحث 2-4

يُعرّف الاقتراح 167 أنواعاً إضافية من البحث التي ترجع جميع الخيارات من الـ leaseset، إذا كانت موجودة. لأنواع البحث 2-4، يجب على الـ router جلب الـ leaseset، حتى لو كان مفتاح البحث موجوداً في دفتر العناوين.

في حالة النجاح، ستحتوي HostReply على خيارات Mapping من leaseset، وتتضمنها كعنصر رقم 5 بعد الوجهة. إذا لم تكن هناك خيارات في Mapping، أو كان leaseset إصدار 1، فسيتم تضمينها مع ذلك كـ Mapping فارغ (بايتان: 0 0). سيتم تضمين جميع الخيارات من leaseset، وليس فقط خيارات سجل الخدمة. على سبيل المثال، قد تكون خيارات للمعاملات المحددة في المستقبل موجودة. قد يكون Mapping المُرجع مرتبًا أو غير مرتب، حسب التنفيذ.

في حالة فشل البحث عن leaseSet، سيحتوي الرد على رمز خطأ جديد 6 (فشل البحث عن leaseSet) ولن يتضمن تطابقاً. عندما يتم إرجاع رمز الخطأ 6، قد يكون حقل الوجهة موجوداً أو غير موجود. سيكون موجوداً إذا نجح البحث عن اسم المضيف في دفتر العناوين، أو إذا نجح بحث سابق وتم تخزين النتيجة مؤقتاً، أو إذا كانت الوجهة موجودة في رسالة البحث (نوع البحث 4).

إذا لم يكن نوع البحث مدعوماً، فإن الرد سيحتوي على رمز خطأ جديد 7 (نوع البحث غير مدعوم).

#### ملاحظات

- اعتباراً من الإصدار 0.9.11. انظر ملاحظات [HostLookupMessage](#HostLookupMessage).
- معرف الجلسة ومعرف الطلب هما نفسهما من [HostLookupMessage](#HostLookupMessage).
- رمز النتيجة هو 0 للنجاح، 1-255 للفشل. 1 يشير إلى فشل عام. اعتباراً من 0.9.43، تم تعريف رموز الفشل الإضافية 2-5 لدعم الأخطاء الموسعة لعمليات البحث "b33". انظر المقترحات 123 و 149 للحصول على معلومات إضافية. اعتباراً من 0.9.66، تم تعريف رموز الفشل الإضافية 6-7 لدعم الأخطاء الموسعة لعمليات البحث من النوع 2-4. انظر المقترح 167 للحصول على معلومات إضافية.

### MessagePayloadMessage {#MessagePayloadMessage}

#### الوصف

تسليم محتوى الرسالة إلى العميل.

يُرسل من الـ Router إلى العميل. إذا كان i2cp.fastReceive=true، وهو ليس الإعداد الافتراضي، يستجيب العميل برسالة [ReceiveMessageEndMessage](#ReceiveMessageEndMessage).

#### المحتويات

1.  [معرف الجلسة](#struct-sessionid)
2.  [معرف الرسالة](#struct-messageid)
3.  [الحمولة](#struct-payload)

#### ملاحظات

### MessageStatusMessage {#MessageStatusMessage}

#### الوصف

إشعار العميل بحالة التسليم لرسالة واردة أو صادرة. يُرسل من router إلى العميل. إذا كانت هذه الرسالة تشير إلى وجود رسالة واردة متاحة، يستجيب العميل برسالة [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage). بالنسبة للرسالة الصادرة، هذا رد على رسالة [SendMessageMessage](#SendMessageMessage) أو [SendMessageExpiresMessage](#SendMessageExpiresMessage).

#### المحتويات

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid) يتم إنشاؤه بواسطة router
3.  1 بايت [Integer](/docs/specs/common-structures/#integer) الحالة
4.  4 بايت [Integer](/docs/specs/common-structures/#integer) الحجم
5.  4 بايت [Integer](/docs/specs/common-structures/#integer) nonce تم إنشاؤه مسبقاً
    بواسطة العميل

#### ملاحظات

حتى الإصدار 0.9.4، قيم الحالة المعروفة هي 0 للرسالة متاحة، 1 للمقبولة، 2 لنجح بأفضل جهد، 3 لفشل بأفضل جهد، 4 لنجح مضمون، 5 لفشل مضمون. الرقم الصحيح للحجم يحدد حجم الرسالة المتاحة وهو ذو صلة فقط عندما الحالة = 0. على الرغم من أن المضمون غير مُطبق، (أفضل جهد هو الخدمة الوحيدة)، فإن تنفيذ router الحالي يستخدم رموز حالة المضمون، وليس رموز أفضل جهد.

اعتباراً من إصدار router 0.9.5، تم تعريف رموز حالة إضافية، ولكنها ليست بالضرورة مُطبقة. انظر [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html) للتفاصيل. بالنسبة للرسائل الصادرة، تشير الرموز 1، 2، 4، و 6 إلى النجاح؛ جميع الرموز الأخرى تشير إلى فشل. قد تختلف رموز الفشل المُرجعة وهي خاصة بالتطبيق.

جميع رموز الحالة:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Available</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DEPRECATED. For incoming messages only. All other status codes below are for outgoing messages. The included size is the size in bytes of the available message. This is unused in "fast receive" mode, which is the default as of release 0.9.4.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Accepted</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outgoing message accepted by the local router for delivery. The included nonce matches the nonce in the <a href="#SendMessageMessage">SendMessageMessage</a>, and the included Message ID will be used for subsequent success or failure notification.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success (unused)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable failure</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generic failure, specific cause unknown. May not really be a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery successful. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery failure. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local router is not ready, has shut down, or has major problems. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Network Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local computer apparently has no network connectivity at all. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Session</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The I2CP session is invalid or closed. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Message</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message payload is invalid or zero-length or too big. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Options</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is invalid in the message options, or the expiration is in the past or too far in the future. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">13</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Overflow Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Some queue or buffer in the router is full and the message was dropped. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Expired</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message expired before it could be sent. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Local Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The client has not yet signed a <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>, or the local keys are invalid, or it has expired, or it does not have any tunnels in it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Local Tunnels</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local problems. No outbound tunnel to send through, or no inbound tunnel if a reply is required. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unsupported Encryption</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The certs or options in the <a href="/docs/specs/common-structures/#destination">Destination</a> or its <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> indicate that it uses an encryption format that we don't support, so we can't talk to it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is wrong with the far-end <a href="/docs/specs/common-structures/#destination">Destination</a>. Bad format, unsupported options, certificates, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but something strange is wrong with it. Unsupported options or certificates, no tunnels, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expired Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but it's expired and we can't get a new one. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Could not find the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>. This is a common failure, equivalent to a DNS lookup failure. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Meta Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The far-end destination's lease set was a meta lease set, and cannot be sent to. The client should request the meta lease set's contents with a HostLookupMessage, and select one of the hashes contained within to look up and send to. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Loopback Denied</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message was attempted to be sent from and to the same destination or session. This is a guaranteed failure.</td>
</tr>
</table>
عندما يكون status = 1 (مقبول)، فإن nonce يطابق nonce في [SendMessageMessage](#SendMessageMessage)، وسيتم استخدام Message ID المرفق للإشعار اللاحق بالنجاح أو الفشل. وإلا، يمكن تجاهل nonce.

### ReceiveMessageBeginMessage {#ReceiveMessageBeginMessage}

مُهمَل. غير مدعوم من قبل i2pd.

#### الوصف

اطلب من الـ router تسليم رسالة تم إشعاره بها مسبقاً. يُرسل من العميل إلى الـ Router. يستجيب الـ router برسالة [MessagePayloadMessage](#MessagePayloadMessage).

#### المحتويات

1.  [معرف الجلسة](#struct-sessionid)
2.  [معرف الرسالة](#struct-messageid)

#### ملاحظات

يتم إرسال [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) كاستجابة لـ [MessageStatusMessage](#MessageStatusMessage) التي تفيد بأن رسالة جديدة متاحة للاستلام. إذا كان معرف الرسالة المحدد في [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) غير صالح أو غير صحيح، فقد لا يرد الـ router ببساطة، أو قد يرسل [DisconnectMessage](#DisconnectMessage).

هذا غير مستخدم في وضع "الاستقبال السريع"، والذي يُعد الافتراضي اعتباراً من الإصدار 0.9.4.

### ReceiveMessageEndMessage {#ReceiveMessageEndMessage}

مُهمل. غير مدعوم من قبل i2pd.

#### الوصف

أخبر الـ router أن تسليم الرسالة قد تم بنجاح وأن الـ router يمكنه التخلص من الرسالة.

مُرسل من العميل إلى الـ router.

#### المحتويات

1.  [معرف الجلسة](#struct-sessionid)
2.  [معرف الرسالة](#struct-messageid)

#### ملاحظات

يتم إرسال [ReceiveMessageEndMessage](#ReceiveMessageEndMessage) بعد أن تقوم [MessagePayloadMessage](#MessagePayloadMessage) بتسليم حمولة الرسالة بالكامل.

هذا غير مستخدم في وضع "الاستقبال السريع"، والذي يُعتبر الوضع الافتراضي اعتباراً من الإصدار 0.9.4.

### ReconfigureSessionMessage {#ReconfigureSessionMessage}

#### الوصف

يُرسل من العميل إلى الـ router لتحديث إعدادات الجلسة. يستجيب الـ router برسالة [SessionStatusMessage](#SessionStatusMessage).

#### المحتويات

1.  [معرف الجلسة](#struct-sessionid)
2.  [إعدادات الجلسة](#struct-sessionconfig)

#### ملاحظات

- اعتباراً من الإصدار 0.7.1.
- إذا كان التاريخ في Session Config بعيداً جداً (أكثر من +/- 30
  ثانية) عن الوقت الحالي للـ router، سيتم رفض الجلسة.
- يجب ترتيب [Mapping](/docs/specs/common-structures/#mapping) في Session Config حسب المفتاح بحيث يتم التحقق من التوقيع بشكل صحيح في
  الـ router.
- قد يتم تعيين بعض خيارات التكوين فقط في
  [CreateSessionMessage](#CreateSessionMessage)، والتغييرات هنا لن
  يتعرف عليها الـ router. التغييرات في خيارات tunnel inbound.\*
  و outbound.\* يتم التعرف عليها دائماً.
- بشكل عام، يجب على الـ router دمج التكوين المحدث مع
  التكوين الحالي، لذا فإن التكوين المحدث يحتاج فقط إلى احتواء الخيارات الجديدة أو
  المتغيرة. ومع ذلك، بسبب الدمج، لا يمكن إزالة الخيارات بهذه الطريقة؛ يجب تعيينها صراحة إلى القيمة الافتراضية المرغوبة.

### ReportAbuseMessage {#ReportAbuseMessage}

مُهمل، غير مُستخدم، غير مدعوم

#### الوصف

أخبر الطرف الآخر (client أو router) أنه تحت الهجوم، مع إشارة محتملة إلى MessageId معين. إذا كان الـ router تحت الهجوم، قد يقرر الـ client الانتقال إلى router آخر، وإذا كان client تحت الهجوم، قد يعيد الـ router بناء routers الخاصة به أو يضع في القائمة السوداء بعض العقد التي أرسلت له رسائل تحمل الهجوم.

يُرسل إما من router إلى العميل أو من العميل إلى router.

#### المحتويات

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) شدة الإساءة (0 هو الحد الأدنى من الإساءة، 255 هو الحد الأقصى من الإساءة)
3.  السبب [String](/docs/specs/common-structures/#string)
4.  [Message ID](#struct-messageid)

#### ملاحظات

غير مستخدم. غير مُنفذ بالكامل. يمكن لكل من router والعميل إنتاج [ReportAbuseMessage](#ReportAbuseMessage)، لكن لا يملك أي منهما معالج للرسالة عند استلامها.

### RequestLeaseSetMessage {#RequestLeaseSetMessage}

مُهْمَل. غير مدعوم من قِبل i2pd. لا يتم إرساله من Java I2P إلى عملاء الإصدار 0.9.7 أو أعلى (2013-07). استخدم RequestVariableLeaseSetMessage.

#### الوصف

طلب من العميل للموافقة على تضمين مجموعة معينة من tunnels الواردة. يُرسل من الـ router إلى العميل. يستجيب العميل برسالة [CreateLeaseSetMessage](#CreateLeaseSetMessage).

أول هذه الرسائل المُرسلة في جلسة هي إشارة للعميل بأن الأنفاق قد تم بناؤها وهي جاهزة لحركة البيانات. يجب على الـ router عدم إرسال أول هذه الرسائل حتى يتم بناء نفق واحد على الأقل للبيانات الواردة ونفق واحد للبيانات الصادرة. يجب على العملاء إنهاء الجلسة وتدميرها إذا لم يتم استلام أول هذه الرسائل بعد فترة زمنية معينة (مُوصى به: 5 دقائق أو أكثر).

#### المحتويات

1.  [Session ID](#struct-sessionid)
2.  1 بايت عدد [Integer](/docs/specs/common-structures/#integer) من الأنفاق
3.  هذا العدد من أزواج:
    1.  [Hash](/docs/specs/common-structures/#hash)
    2.  [TunnelId](/docs/specs/common-structures/#tunnelid)
4.  تاريخ الانتهاء [Date](/docs/specs/common-structures/#date)

#### ملاحظات

هذا يطلب [LeaseSet](/docs/specs/common-structures/#leaseset) مع جميع إدخالات [Lease](/docs/specs/common-structures/#lease) مُعيّنة لتنتهي صلاحيتها في نفس الوقت. لإصدارات العميل 0.9.7 أو أحدث، يتم استخدام [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage).

### RequestVariableLeaseSetMessage {#RequestVariableLeaseSetMessage}

#### الوصف

طلب من العميل الترخيص بإدراج مجموعة معينة من الأنفاق الواردة.

يُرسل من الـ router إلى العميل. يستجيب العميل برسالة [CreateLeaseSetMessage](#CreateLeaseSetMessage) أو [CreateLeaseSet2Message](#CreateLeaseSet2Message).

أول هذه الرسائل المُرسلة في جلسة معينة هي إشارة للعميل بأن الـ tunnels قد تم بناؤها وهي جاهزة لحركة البيانات. يجب على الـ router عدم إرسال أول هذه الرسائل حتى يتم بناء tunnel واحد على الأقل للبيانات الواردة وآخر للبيانات الصادرة. يجب على العملاء إنهاء الجلسة وتدميرها إذا لم يتم استقبال أول هذه الرسائل خلال فترة زمنية معينة (الموصى به: 5 دقائق أو أكثر).

#### المحتويات

1.  [Session ID](#struct-sessionid)
2.  1 بايت [Integer](/docs/specs/common-structures/#integer) عدد tunnels
3.  بهذا العدد من إدخالات [Lease](/docs/specs/common-structures/#lease)

#### ملاحظات

هذا يطلب [LeaseSet](/docs/specs/common-structures/#leaseset) مع وقت انتهاء صلاحية فردي لكل [Lease](/docs/specs/common-structures/#lease).

اعتباراً من الإصدار 0.9.7. بالنسبة للعملاء قبل ذلك الإصدار، استخدم [RequestLeaseSetMessage](#RequestLeaseSetMessage).

### SendMessageMessage {#SendMessageMessage}

#### الوصف

هذه هي الطريقة التي يرسل بها العميل رسالة (الحمولة) إلى [Destination](/docs/specs/common-structures/#destination). سيستخدم الـ router انتهاء صلاحية افتراضي.

يُرسل من العميل إلى router. يستجيب router برسالة [MessageStatusMessage](#MessageStatusMessage).

#### المحتويات

1.  [معرف الجلسة](#struct-sessionid)
2.  [الوجهة](/docs/specs/common-structures/#destination)
3.  [الحمولة](#struct-payload)
4.  4 بايت [عدد صحيح](/docs/specs/common-structures/#integer) nonce

#### ملاحظات

بمجرد وصول [SendMessageMessage](#SendMessageMessage) بشكل كامل وسليم، يجب على الـ router أن يُرجع [MessageStatusMessage](#MessageStatusMessage) يُفيد بأنه تم قبولها للتسليم. ستحتوي تلك الرسالة على نفس الـ nonce المُرسل هنا. لاحقاً، بناءً على ضمانات التسليم لإعدادات الجلسة، قد يرسل الـ router إضافياً [MessageStatusMessage](#MessageStatusMessage) آخر لتحديث الحالة.

اعتباراً من الإصدار 0.8.1، لا يرسل الـ router أي [MessageStatusMessage](#MessageStatusMessage) إذا كان i2cp.messageReliability=none.

قبل الإصدار 0.9.4، لم تكن قيمة nonce البالغة 0 مسموحة. اعتباراً من الإصدار 0.9.4، أصبحت قيمة nonce البالغة 0 مسموحة، وتخبر router أنه يجب ألا يرسل [MessageStatusMessage](#MessageStatusMessage)، أي أنه يتصرف كما لو أن i2cp.messageReliability=none لهذه الرسالة فقط.

قبل الإصدار 0.9.14، لم يكن بإمكان تجاوز جلسة بها i2cp.messageReliability=none على أساس كل رسالة على حدة. اعتباراً من الإصدار 0.9.14، في جلسة بها i2cp.messageReliability=none، يمكن للعميل طلب تسليم [MessageStatusMessage](#MessageStatusMessage) مع نجاح أو فشل التسليم عن طريق تعيين nonce لقيمة غير صفرية. لن يرسل router رسالة [MessageStatusMessage](#MessageStatusMessage) الخاصة بـ "accepted" ولكنه سيرسل لاحقاً للعميل [MessageStatusMessage](#MessageStatusMessage) بنفس nonce، وقيمة نجاح أو فشل.

### SendMessageExpiresMessage {#SendMessageExpiresMessage}

#### الوصف

يُرسل من العميل إلى الـ router. مماثل لـ [SendMessageMessage](#SendMessageMessage)، باستثناء أنه يتضمن انتهاء صلاحية وخيارات.

#### المحتويات

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 بايت [Integer](/docs/specs/common-structures/#integer) nonce
5.  2 بايت من الخيارات (flags)
6.  تاريخ انتهاء الصلاحية [Date](/docs/specs/common-structures/#date) مقطوع من 8 بايت إلى 6 بايت

#### ملاحظات

اعتباراً من الإصدار 0.7.1.

في وضع "أفضل جهد"، بمجرد وصول SendMessageExpiresMessage كاملة وسليمة، يجب على الـ router أن يُرجع MessageStatusMessage تُفيد بأنه تم قبولها للتسليم. ستحتوي تلك الرسالة على نفس الـ nonce المُرسل هنا. لاحقاً، بناءً على ضمانات التسليم لتكوين الجلسة، قد يُرسل الـ router أيضاً MessageStatusMessage أخرى لتحديث الحالة.

اعتباراً من الإصدار 0.8.1، لا يرسل الـ router أي Message Status Message إذا كان i2cp.messageReliability=none.

قبل الإصدار 0.9.4، لم تكن قيمة nonce بـ 0 مسموحة. اعتباراً من الإصدار 0.9.4، أصبحت قيمة nonce بـ 0 مسموحة، وتخبر الـ router أنه يجب ألا يرسل أي Message Status Message، أي أنها تعمل كما لو أن i2cp.messageReliability=none لهذه الرسالة فقط.

قبل الإصدار 0.9.14، لم يكن بالإمكان تجاوز جلسة بإعداد i2cp.messageReliability=none على أساس كل رسالة على حدة. اعتباراً من الإصدار 0.9.14، في جلسة بإعداد i2cp.messageReliability=none، يمكن للعميل طلب تسليم Message Status Message مع نجاح أو فشل التسليم عن طريق تعيين nonce إلى قيمة غير صفرية. لن يرسل الموجه Message Status Message "مقبولة" ولكنه سيرسل لاحقاً للعميل Message Status Message بنفس nonce، وقيمة نجاح أو فشل.

#### حقل الأعلام

اعتباراً من الإصدار 0.8.4، تم إعادة تعريف البايتين العلويين من التاريخ لاحتواء الأعلام. يجب أن تكون الأعلام افتراضياً جميعها أصفار للتوافق مع الإصدارات السابقة. لن يتداخل التاريخ مع حقل الأعلام حتى عام 10889. قد يستخدم التطبيق الأعلام لتوفير تلميحات للموجه حول ما إذا كان يجب تسليم LeaseSet و/أو ElGamal/AES Session Tags مع الرسالة. ستؤثر الإعدادات بشكل كبير على كمية الحمولة الإضافية للبروتوكول وموثوقية تسليم الرسائل. يتم تعريف بتات الأعلام الفردية كما يلي، اعتباراً من الإصدار 0.9.2. التعريفات عرضة للتغيير. استخدم فئة SendMessageOptions لبناء الأعلام.

ترتيب البت: 15...0

البتات 15-11

:   غير مستخدم، يجب أن يكون صفراً

البتات 10-9

:   تجاوز موثوقية الرسالة (غير مُنفذ، سيتم إزالته).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">00</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use session setting i2cp.messageReliability (default)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">01</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "best effort" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "guaranteed" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unused. Use a nonce value of 0 to force "none" and override a session setting of "best effort" or "guaranteed".</td>
</tr>
</table>
البت 8

:   إذا كان 1، لا تضمن lease set في garlic encryption مع هذه الرسالة. إذا

    0, the router may bundle a lease set at its discretion.

البتات 7-4

:   الحد الأدنى للعلامات. إذا كان عدد العلامات المتاحة أقل من هذا الرقم،

    send more. This is advisory and does not force tags to be delivered.
    For ElGamal only. Ignored for ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tag threshold</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">3</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">9</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">14</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">20</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">27</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">35</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">45</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">57</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">72</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">92</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">117</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">147</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">192</td></tr>
</table>
البتات 3-0

:   عدد العلامات المراد إرسالها عند الحاجة. هذا استشاري ولا

    force tags to be delivered. For ElGamal only. Ignored for
    ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tags to send</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">4</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">8</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">12</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">16</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">24</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">32</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">40</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">51</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">64</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">80</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">100</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">125</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">160</td></tr>
</table>
### رسالة حالة الجلسة {#SessionStatusMessage}

#### الوصف

توجيه العميل بخصوص حالة جلسته.

يُرسل من الـ Router إلى العميل، كاستجابة لـ [CreateSessionMessage](#CreateSessionMessage) أو [ReconfigureSessionMessage](#ReconfigureSessionMessage) أو [DestroySessionMessage](#DestroySessionMessage). في جميع الحالات، بما في ذلك الاستجابة لـ [CreateSessionMessage](#CreateSessionMessage)، يجب على الـ router أن يستجيب فوراً (لا تنتظر بناء الـ tunnels).

#### المحتويات

1.  [معرف الجلسة](#struct-sessionid)
2.  1 بايت [عدد صحيح](/docs/specs/common-structures/#integer) الحالة

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Definition</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destroyed</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The session with the given ID is terminated. May be a response to a <a href="#DestroySessionMessage">DestroySessionMessage</a>.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, a new session with the given ID is now active.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Updated</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, an existing session with the given ID has been reconfigured.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Invalid</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the configuration is invalid. The included session ID should be ignored. In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, the new configuration is invalid for the session with the given ID.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Refused</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the router was unable to create the session, perhaps due to limits being exceeded. The included session ID should be ignored.</td>
</tr>
</table>
#### ملاحظات

قيم الحالة محددة أعلاه. إذا كانت الحالة Created، فإن معرف الجلسة هو المعرف الذي سيتم استخدامه لبقية الجلسة.

### SetDateMessage {#SetDateMessage}

#### الوصف

التاريخ والوقت الحالي. يتم إرساله من الـ Router إلى العميل كجزء من المصافحة الأولية. اعتباراً من الإصدار 0.9.20، يمكن أيضاً إرساله في أي وقت بعد المصافحة لإشعار العميل بتغيير في الساعة.

#### المحتويات

1.  [التاريخ](/docs/specs/common-structures/#date)
2.  إصدار I2CP API [String](/docs/specs/common-structures/#string)

#### ملاحظات

هذه عموماً أول رسالة يرسلها الـ router. يتم تضمين نص الإصدار اعتباراً من الإصدار 0.8.7. هذا مفيد فقط إذا لم يكن العميل والـ router في نفس JVM. إذا لم تكن موجودة، فإن الـ router هو إصدار 0.8.6 أو أقدم.

لن يتم إرسال رسائل SetDate إضافية إلى العملاء في نفس JVM.

## المراجع

- [التاريخ](/docs/specs/common-structures/#date)
- [الوجهة](/docs/specs/common-structures/#destination)
- [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)
- [الهاش](/docs/specs/common-structures/#hash)
- [نظرة عامة على I2CP](/docs/specs/i2cp/)
- [وثائق I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)
- [العدد الصحيح](/docs/specs/common-structures/#integer)
- [Lease](/docs/specs/common-structures/#lease)
- [LeaseSet](/docs/specs/common-structures/#leaseset)
- [LeaseSet2](/docs/specs/common-structures/#leaseset2)
- [التخطيط](/docs/specs/common-structures/#mapping)
- [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
- [وثائق MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)
- [المفتاح الخاص](/docs/specs/common-structures/#privatekey)
- [المفتاح العام](/docs/specs/common-structures/#publickey)
- [هوية router](/docs/specs/common-structures/#routeridentity)
- [SAMv3](/docs/api/samv3/)
- [التوقيع](/docs/specs/common-structures/#signature)
- [مفتاح التوقيع الخاص](/docs/specs/common-structures/#signingprivatekey)
- [مفتاح التوقيع العام](/docs/specs/common-structures/#signingpublickey)
- [النص](/docs/specs/common-structures/#string)
- [معرف tunnel](/docs/specs/common-structures/#tunnelid)
