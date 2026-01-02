---
title: "التعدد الخفي للشبكات"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "مفتوح"
thread: "http://zzz.i2p/topics/2335"
toc: true
---

## نظرة عامة

يحدد هذا الاقتراح تصميماً لبروتوكول يمكّن عميل I2P أو خدمة أو عملية موازن خارجي من إدارة عدة routers بشفافية تستضيف [Destination](http://localhost:63465/docs/specs/common-structures/#destination) واحد.

الاقتراح حالياً لا يحدد تنفيذاً محدداً. يمكن تنفيذه كإضافة لـ [I2CP](/docs/specs/i2cp/)، أو كبروتوكول جديد.

## الدافع

التعدد المضيفي هو عندما يتم استخدام عدة routers لاستضافة نفس الوجهة. الطريقة الحالية لتطبيق التعدد المضيفي مع I2P هي تشغيل نفس الوجهة على كل router بشكل مستقل؛ router الذي يتم استخدامه من قبل العملاء في أي وقت معين هو آخر من ينشر LeaseSet.

هذا حل مؤقت وعلى الأرجح لن يعمل للمواقع الكبيرة على نطاق واسع. لنفترض أن لدينا 100 router متعدد المسارات كل منها يحتوي على 16 tunnel. هذا يعني 1600 نشر LeaseSet كل 10 دقائق، أو ما يقارب 3 في الثانية الواحدة. سوف تصبح عقد floodfill مثقلة وستبدأ آليات التحكم في المعدل بالعمل. وهذا قبل أن نذكر حتى حركة البحث.

الاقتراح 123 يحل هذه المشكلة باستخدام meta-LeaseSet، والذي يسرد الـ 100 hash الحقيقية لـ LeaseSet. يصبح البحث عملية من مرحلتين: أولاً البحث عن meta-LeaseSet، ثم البحث عن أحد LeaseSets المسماة. هذا حل جيد لمشكلة حركة مرور البحث، ولكنه بحد ذاته ينشئ تسريباً كبيراً للخصوصية: من الممكن تحديد أي routers متعددة الاستضافة متصلة عن طريق مراقبة meta-LeaseSet المنشورة، لأن كل LeaseSet حقيقي يتطابق مع router واحد.

نحتاج إلى طريقة لعميل I2P أو خدمة لنشر Destination واحد عبر عدة routers، بطريقة لا يمكن تمييزها عن استخدام router واحد (من منظور LeaseSet نفسه).

## التصميم

### Definitions

    User
        The person or organisation wanting to multihome their Destination(s). A
        single Destination is considered here without loss of generality (WLOG).

    Client
        The application or service running behind the Destination. It may be a
        client-side, server-side, or peer-to-peer application; we refer to it as
        a client in the sense that it connects to the I2P routers.

        The client consists of three parts, which may all be in the same process
        or may be split across processes or machines (in a multi-client setup):

        Balancer
            The part of the client that manages peer selection and tunnel
            building. There is a single balancer at any one time, and it
            communicates with all I2P routers. There may be failover balancers.

        Frontend
            The part of the client that can be operated in parallel. Each
            frontend communicates with a single I2P router.

        Backend
            The part of the client that is shared between all frontends. It has
            no direct communication with any I2P router.

    Router
        An I2P router run by the user that sits at the boundary between the I2P
        network and the user's network (akin to an edge device in corporate
        networks). It builds tunnels under the command of a balancer, and routes
        packets for a client or frontend.

### High-level overview

تخيل التكوين المطلوب التالي:

- تطبيق عميل مع Destination واحد.
- أربعة routers، كل منها يدير ثلاثة أنفاق واردة.
- جميع الأنفاق الاثني عشر يجب أن تُنشر في LeaseSet واحد.

### Single-client

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]-----
                 |-{ [Tunnel 3]===/               \
                 |                                 \
                 |-{ [Tunnel 4]===\                 \
  [Destination]  |-{ [Tunnel 5]====[Router 2]-----   \
    \            |-{ [Tunnel 6]===/               \   \
     [LeaseSet]--|                               [Client]
                 |-{ [Tunnel 7]===\               /   /
                 |-{ [Tunnel 8]====[Router 3]-----   /
                 |-{ [Tunnel 9]===/                 /
                 |                                 /
                 |-{ [Tunnel 10]==\               /
                 |-{ [Tunnel 11]===[Router 4]-----
                  -{ [Tunnel 12]==/
```
### التعريفات

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]---------[Frontend 1]
                 |-{ [Tunnel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Tunnel 4]===\            \                    \
  [Destination]  |-{ [Tunnel 5]====[Router 2]---\-----[Frontend 2]   \
    \            |-{ [Tunnel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Balancer]            [Backend]
                 |-{ [Tunnel 7]===\          /   /                /   /
                 |-{ [Tunnel 8]====[Router 3]---/-----[Frontend 3]   /
                 |-{ [Tunnel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Tunnel 10]==\          /                    /
                 |-{ [Tunnel 11]===[Router 4]---------[Frontend 4]
                  -{ [Tunnel 12]==/
```
### نظرة عامة على المستوى العالي

- تحميل أو إنشاء وجهة (Destination).

- افتح جلسة مع كل router، مربوطة بـ Destination.

- بشكل دوري (حوالي كل عشر دقائق، ولكن أكثر أو أقل بناءً على حالة tunnel):

- احصل على المستوى السريع من كل router.

- استخدم المجموعة الفائقة من الأقران لبناء الأنفاق من/إلى كل router.

    - By default, tunnels to/from a particular router will use peers from
      that router's fast tier, but this is not enforced by the protocol.

- جمع مجموعة الأنفاق الواردة النشطة من جميع أجهزة التوجيه النشطة، وإنشاء LeaseSet.

- نشر LeaseSet من خلال واحد أو أكثر من أجهزة التوجيه.

### عميل واحد

لإنشاء وإدارة هذا التكوين، يحتاج العميل إلى الوظائف الجديدة التالية بالإضافة إلى ما يوفره حالياً [I2CP](/docs/specs/i2cp/):

- أخبر router ببناء tunnels، بدون إنشاء LeaseSet لها.
- احصل على قائمة بـ tunnels الحالية في مجموعة الوارد.

بالإضافة إلى ذلك، ستمكن الوظائف التالية من مرونة كبيرة في كيفية إدارة العميل لأنفاق tunnel الخاصة به:

- احصل على محتويات الطبقة السريعة للـ router.
- اطلب من الـ router بناء نفق داخلي أو خارجي باستخدام قائمة معطاة من
  النظراء.

### متعدد العملاء

```
         Client                           Router

                    --------------------->  Create Session
   Session Status  <---------------------
                    --------------------->  Get Fast Tier
        Peer List  <---------------------
                    --------------------->  Create Tunnel
    Tunnel Status  <---------------------
                    --------------------->  Get Tunnel Pool
      Tunnel List  <---------------------
                    --------------------->  Publish LeaseSet
                    --------------------->  Send Packet
      Send Status  <---------------------
  Packet Received  <---------------------
```
### عملية العميل العامة

**إنشاء جلسة** - إنشاء جلسة للوجهة المحددة.

**حالة الجلسة** - تأكيد أن الجلسة قد تم إعدادها، ويمكن للعميل الآن البدء في بناء tunnels.

**الحصول على الطبقة السريعة** - طلب قائمة بالعقد (peers) التي يعتبرها الـ router حالياً لبناء الأنفاق من خلالها.

**قائمة النظراء** - قائمة بالنظراء المعروفين لدى الـ router.

**إنشاء نفق** - طلب من الـ router بناء نفق جديد عبر النظراء المحددين.

**حالة النفق** - نتيجة بناء نفق معين، بمجرد أن يصبح متاحاً.

**الحصول على مجموعة الأنفاق** - طلب قائمة بالأنفاق الحالية في مجموعة الأنفاق الواردة أو الصادرة للوجهة.

**قائمة الأنفاق** - قائمة بالأنفاق للمجموعة المطلوبة.

**نشر LeaseSet** - طلب من الموجه نشر الـ LeaseSet المقدم من خلال أحد الأنفاق الصادرة للوجهة. لا حاجة لحالة رد؛ يجب على الموجه الاستمرار في إعادة المحاولة حتى يقتنع بأن الـ LeaseSet قد تم نشره.

**إرسال الحزمة** - حزمة صادرة من العميل. تحدد اختياريًا نفقًا صادرًا يجب (يُفترض؟) إرسال الحزمة من خلاله.

**إرسال الحالة** - يُعلم العميل بنجاح أو فشل إرسال الحزمة.

**تم استلام الحزمة** - حزمة واردة للعميل. اختيارياً تحدد tunnel الوارد الذي تم استلام الحزمة من خلاله(؟)

## Security implications

من منظور أجهزة router، هذا التصميم مكافئ وظيفياً للوضع الراهن. لا يزال router يبني جميع الأنفاق، ويحتفظ بملفات تعريف الأقران الخاصة به، ويفرض الفصل بين عمليات router والعميل. في التكوين الافتراضي يكون مطابقاً تماماً، لأن الأنفاق لذلك router يتم بناؤها من طبقته السريعة الخاصة.

من منظور netDB، فإن LeaseSet واحد تم إنشاؤه عبر هذا البروتوكول مطابق للوضع الراهن، لأنه يستفيد من الوظائف الموجودة مسبقاً. ومع ذلك، بالنسبة لـ LeaseSets الأكبر التي تقترب من 16 Lease، قد يكون من الممكن للمراقب أن يحدد أن LeaseSet متعدد المضيفين:

- الحد الأقصى الحالي لحجم الطبقة السريعة هو 75 peer. يتم اختيار البوابة الواردة
  (IBGW، العقدة المنشورة في Lease) من جزء من الطبقة
  (مقسمة عشوائياً لكل tunnel pool بواسطة hash، وليس العد):

      1 hop
          The whole fast tier

      2 hops
          Half of the fast tier
          (the default until mid-2014)

      3+ hops
          A quarter of the fast tier
          (3 being the current default)

هذا يعني أنه في المتوسط ستكون IBGWs من مجموعة من 20-30 نظير.

- في إعداد single-homed، سيحتوي LeaseSet كامل بـ 16 tunnel على 16 IBGW مختارة عشوائياً من مجموعة تصل إلى (لنقل) 20 peer.

- في إعداد متعدد المسارات مكون من 4 أجهزة router باستخدام التكوين الافتراضي، سيكون لدى LeaseSet كامل مكون من 16 tunnel ما مجموعه 16 IBGW مختارة عشوائياً من مجموعة تضم 80 peer كحد أقصى، رغم أنه من المحتمل وجود جزء من الـ peers المشتركة بين أجهزة الـ router.

وبالتالي مع الإعداد الافتراضي، قد يكون من الممكن من خلال التحليل الإحصائي معرفة أن LeaseSet يتم إنتاجه بواسطة هذا البروتوكول. قد يكون من الممكن أيضاً معرفة عدد الـ routers الموجودة، رغم أن تأثير التغيير على الطبقات السريعة سيقلل من فعالية هذا التحليل.

نظرًا لأن العميل لديه سيطرة كاملة على الأقران التي يختارها، يمكن تقليل أو إزالة تسريب المعلومات هذا من خلال اختيار IBGWs من مجموعة مُقلصة من الأقران.

## Compatibility

هذا التصميم متوافق تماماً مع الشبكة إلى الوراء، لأنه لا توجد تغييرات على تنسيق LeaseSet. جميع الـ routers ستحتاج إلى معرفة البروتوكول الجديد، لكن هذا ليس مصدر قلق لأنها ستكون جميعاً تحت سيطرة نفس الكيان.

## Performance and scalability notes

الحد الأعلى البالغ 16 Lease لكل LeaseSet لا يتغير بهذا الاقتراح. بالنسبة للوجهات التي تتطلب أنفاق أكثر من ذلك، هناك تعديلان محتملان للشبكة:

- زيادة الحد الأقصى لحجم LeaseSets. هذا سيكون الأبسط في التطبيق (رغم أنه سيتطلب دعماً شاملاً من الشبكة قبل أن يمكن استخدامه على نطاق واسع)، لكن قد يؤدي إلى عمليات بحث أبطأ بسبب أحجام الحزم الأكبر. يتم تحديد الحد الأقصى المجدي لحجم LeaseSet بواسطة MTU للبروتوكولات الأساسية، وبالتالي يكون حوالي 16kB.

- تنفيذ الاقتراح 123 لـ LeaseSets متدرجة. بالتزامن مع هذا الاقتراح،
  يمكن توزيع الـ Destinations الخاصة بـ sub-LeaseSets عبر عدة
  routers، مما يجعلها تعمل بشكل فعال مثل عناوين IP متعددة لخدمة clearnet.

## Acknowledgements

شكرًا لـ psi على النقاش الذي أدى إلى هذا الاقتراح.
