---
title: "ملاحظات حالة I2P بتاريخ 2004-08-31"
date: 2004-08-31
author: "jr"
description: "التحديث الأسبوعي لحالة I2P الذي يغطي تدهور أداء الشبكة، التخطيط لإصدار 0.3.5، متطلبات التوثيق، وتقدم Stasher DHT"
categories: ["status"]
---

حسنًا يا أولاد وبنات، إنه يوم الثلاثاء مرة أخرى!

## الفهرس:

1. 0.3.4.3
2. 0.3.5 and 0.4
3. docs
4. stasher update
5. ???

## 1) 0.3.4.3

حسناً، كما لاحظتم جميعاً، رغم أن عدد المستخدمين على الشبكة ظلّ مستقراً إلى حدّ كبير، فإن الأداء قد تدهور بشكل ملحوظ خلال الأيام القليلة الماضية. كان مصدر ذلك سلسلةً من الأخطاء البرمجية في اختيار النظراء والكود الخاص بتسليم الرسائل، وقد انكشفت عندما حدث هجوم حجب خدمة (DoS) بسيط الأسبوع الماضي. وكانت النتيجة أن tunnels (الأنفاق في I2P) لدى الجميع تقريباً تتعطّل باستمرار، مما أحدث تأثيراً يشبه كرة الثلج إلى حدّ ما. لذا، لا، لست وحدك — فالشبكة كانت سيئة للغاية بالنسبة لنا جميعاً أيضاً ;)

لكن الخبر السار هو أننا أصلحنا المشكلات بسرعة كبيرة، وقد أُدرجت الإصلاحات في CVS منذ الأسبوع الماضي، ولكن ستظل الشبكة تقدّم أداءً سيئًا للمستخدمين حتى يصدر الإصدار التالي. وبهذه المناسبة...

## 2) 0.3.5 و 0.4

مع أن الإصدار التالي سيضم كل التحسينات والمزايا التي خططنا لها لإصدار 0.4 (مثبّت جديد، معيار جديد لواجهة الويب، واجهة i2ptunnel جديدة، systray (علبة النظام) & خدمة Windows، تحسينات في threading (إدارة مؤشرات التنفيذ)، إصلاحات للأخطاء، إلخ)، كانت الطريقة التي تدهور بها الإصدار الأخير مع مرور الوقت دالّة. أريد لنا أن نتحرك بوتيرة أبطأ في هذه الإصدارات، بمنحها وقتاً لتنتشر على نحو أوسع ولتتكشّف العيوب. ومع أن المُحاكي يستطيع استكشاف الأساسيات، فلا توجد لديه وسيلة لمحاكاة مشكلات الشبكة الطبيعية التي نراها على الشبكة الحية (على الأقل، ليس بعد).

وعليه، سيكون الإصدار التالي 0.3.5 - ونأمل أن يكون آخر إصدار ضمن سلسلة 0.3.*، لكن قد لا يكون كذلك إذا ظهرت مشكلات أخرى. بالنظر إلى كيفية عمل الشبكة حين كنت غير متصل في يونيو/حزيران، بدأ الأداء بالتدهور بعد نحو أسبوعين. لذلك أفكّر في تأجيل ترقيتنا إلى مستوى الإصدار 0.4 التالي إلى أن نستطيع الحفاظ على درجة عالية من الاعتمادية لمدة لا تقل عن أسبوعين. هذا لا يعني أننا لن نواصل العمل خلال تلك الفترة، بالطبع.

على أي حال، كما ذُكر الأسبوع الماضي، hypercubus يواصل العمل بجد على نظام التثبيت الجديد، متعاملًا مع تغييراتي المستمرة ومطالبي بدعم أنظمة عجيبة الأطوار. ينبغي أن ننتهي من تسوية الأمور خلال الأيام القليلة المقبلة لطرح إصدار 0.3.5 خلال الأيام القليلة المقبلة.

## 3) الوثائق

أحد الأمور المهمة التي نحتاج إلى القيام بها خلال "نافذة الاختبار" التي تمتد لأسبوعين قبل 0.4 هو أن نقوم بالتوثيق بشكل مكثف للغاية. ما أتساءل عنه هو ما الأشياء التي تشعرون أن توثيقنا يفتقر إليها — ما الأسئلة التي لديكم والتي نحتاج إلى الإجابة عنها؟ رغم أنني أود أن أقول "حسنًا، الآن اذهبوا واكتبوا تلك الوثائق"، إلا أنني واقعي، لذا فكل ما أطلبه هو أن تحددوا ما الذي ينبغي أن تتناوله تلك الوثائق.

على سبيل المثال، إحدى الوثائق التي أعمل عليها الآن هي مراجعة لنموذج التهديد، والذي أصفه الآن كسلسلة من حالات الاستخدام تشرح كيف يمكن لـ I2P تلبية احتياجات أفراد مختلفين، بما في ذلك الوظائف المتاحة، والخصوم الذين يخشاهم ذلك الشخص، وكيف يدافع عن نفسه.

إذا كنت لا تظن أن سؤالك يتطلب وثيقة كاملة لمعالجته، فببساطة صِغه كسؤال وسنضيفه إلى قسم الأسئلة الشائعة.

## 4) stasher update

مرّ أوم على القناة في وقت سابق اليوم ومعه تحديث (بينما كنت أمطره بالأسئلة):

```
<aum> quick stasher update, with apologies for tomorrow's meeting:
<aum> infinite-level splitfiles working, have successfully
      inserted and retrieved large files
<jrandom> w00t
<aum> splitfile fragmentation/reassembly transparently occuring
      within stasher
<aum> freenet interface working
<jrandom> wow
<jrandom> so FUQID/FIW works?
<aum> use of fcp splitfile commands in freenet clients strictly
      forbidden (at this stage)
<aum> most clients such as fuqid/fiw should allow setting
      extremely large splitfile sizes, which should prevent them
      trying to talk splitfiles
<aum> if not, then i can dummy up something
<jrandom> r0x0r aum, that kicks ass!
<aum> hooks are in for detailed freenet key support
<jrandom> detailed freenet key support?
<aum> yes, specific chk@, ssk@, ksk@
<jrandom> ok great, so they're all verified @ each node, etc?
<aum> no - only verifiable by the requestor
<aum> my thinking is, given KSK@fred = 'mary',
<aum> to store as SHA1(SHA1("KSK@fred")) = E(mary), where key
      for E is SHA1("KSK@fred")
<aum> ie, crypto key is SHA1(uri), and kademlia key is
      SHA1(SHA1(uri))
<jrandom> hm
<aum> so a possessor of the URI can decyrpt, but owner of a
      datastore cannot decrypt (and therefore has plausible
      deniability)
<jrandom> well, ksks are inherently insecure, so thats no big
      loss, but what about ssk?
<deer> <detonate> those keys aren't very large
<aum> SSK as for freenet
<jrandom> so the SSKs are verified at each node?
<aum> except i'm looking to use same encryption over the top
<aum> not feasible to verify SSK at the target node
<jrandom> why not?  freenet does
<aum> well maybe it is feasible,
<aum> i guess i shouldn't be so lazy
<aum> i was trying to keep the kademlia and freenet layers
      separate
<jrandom> heh, you're not being lazy, there's a truckload of
      work here, and you're doing a great job
<aum> verifying on target node will cause some pathological
      couplings between the two layers, and force deviation
      from pure kademlia
<jrandom> i dont think its possible to do SSKs or CHKs
      securely without having the node validate the key
      properties
<aum> not correct
<aum> fred asks mary, 'gimme SSK@madonna'
<aum> mary sends back what she thinks is 'SSK@madonna'
<aum> fred tests it, barfs, then goes on to ask the next node
<aum> anyway, i MUST go - but am open to continuing discussion
      over email, or tomorrow
<aum> bbl guys
<jrandom> mallory floods the net with 'SSK@madonna' ==
      'sexDrugsRockNRoll'
<jrandom> l8r aum
```
إذن، كما ترون، هناك الكثير والكثير من التقدّم. حتى لو جرى التحقق من المفاتيح فوق طبقة DHT (جدول التجزئة الموزّع)، فهذا في غاية الروعة (برأيي المتواضع). هيا يا aum!

## 5) ???

Ok, thats all I've got to say (which is good, since the meeting starts in a few moments)... swing on by and say whatcha want!

=jr
