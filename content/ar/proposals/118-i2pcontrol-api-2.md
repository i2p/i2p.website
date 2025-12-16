---
title: "I2PControl API 2"
number: "118"
author: "hottuna"
created: "2016-01-23"
lastupdated: "2018-03-22"
status: "مرفوض"
thread: "http://zzz.i2p/topics/2030"
toc: true
---

## نظرة عامة

تقدم هذه الاقتراح API2 لـ I2PControl.

تم رفض هذا الاقتراح ولن يتم تنفيذه لأنه يكسر التوافق مع الإصدارات السابقة.
انظر رابط موضوع النقاش للحصول على التفاصيل.

### تنبيه للمطورين!

جميع معلمات RPC ستصبح الآن أحرف صغيرة. هذا *سيكسر* التوافق
مع تنفيذات API1. السبب في ذلك هو توفير
للمستخدمين من API2 فأعلى بأبسط وأكثر واجهة برمجة تطبيقات تماسكًا ممكنة.


## مواصفات API 2

```json
{
    "id": "id",
    "method": "method_name",
    "params": {
      "token": "auth_token",
      "method_param": "method_parameter_value",
    },
    "jsonrpc": "2.0"
  }

  {
    "id": "id",
    "result": "result_value",
    "jsonrpc": "2.0"
  }
```

### المعلمات

**`"id"`**

رقم الهوية أو الطلب. يُستخدم لتحديد أي رد تم توليده بواسطة أي طلب.

**`"method_name"`**

اسم RPC الجاري استدعاؤها.

**`"auth_token"`**

رمز المصادقة للجلسة. يلزم تقديمه مع كل RPC باستثناء استدعاء 'authenticate'.

**`"method_parameter_value"`**

معلمة الطريقة. يُستخدم لتقديم نكهات مختلفة لطريقة. مثل 'get'، 'set' والأنواع المشابهة لذلك.

**`"result_value"`**

القيمة التي تعيدها RPC. نوعها ومحتوياتها تعتمد على الطريقة وأي طريقة.


### البادئات

نظام تسمية RPC يشبه كيف يتم القيام به في CSS، مع بادئات البائع
للتنفيذات المختلفة لـ API (i2p، kovri، i2pd):

```text
XXX.YYY.ZZZ
    i2p.XXX.YYY.ZZZ
    i2pd.XXX.YYY.ZZZ
    kovri.XXX.YYY.ZZZ
```

الفكرة العامة من البادئات الخاصة بالبائع هي إتاحة بعض الحرية
ودع التنفيذات تبتكر دون الحاجة إلى انتظار كل تنفيذ
آخر للحاق بالركب. إذا تم تنفيذ RPC بواسطة جميع التنفيذات،
يمكن إزالة بادئتها المتعددة ويمكن تضمينها كـ RPC أساسية في
الإصدار التالي من API.


### دليل قراءة الطريقة

 * **rpc.method**

   * *parameter* [نوع المعلمة]:  [null]، [number]، [string]، [boolean]،
     [array] أو [object]. [object] هو خريطة {key:value}.
  * يعيد:

```text

  "return_value" [string] // هذه هي القيمة التي تعيدها استدعاء RPC
```


### الطرق

* **authenticate** - بالنظر إلى توفير كلمة مرور صحيحة، توفر هذه الطريقة لك رمزًا للوصول الإضافي وقائمة بمستويات API المدعومة.

  * *password* [string]:  كلمة المرور لهذه التنفيذ لـ i2pcontrol

    يعيد:
```text
    [object]
    {
      "token" : [string], // الرمز الذي سيتم تقديمه مع جميع الطرق الأخرى لـ RPC
      "api" : [[int],[int], ...]  // قائمة بمستويات API المدعومة.
    }
```

* **control.** - التحكم في i2p

  * **control.reseed** - بدء التبذير

    * [nil]: لا حاجة لمعلمة

    يعيد:
```text
      [nil]
```

  * **control.restart** - إعادة تشغيل مثيل i2p

    * [nil]: لا حاجة لمعلمة

    يعيد:
```text
      [nil]
```

  * **control.restart.graceful** - إعادة تشغيل مثيل i2p بشكل سلس

    * [nil]: لا حاجة لمعلمة

    يعيد:
```text
      [nil]
```

  * **control.shutdown** - إيقاف تشغيل مثيل i2p

    * [nil]: لا حاجة لمعلمة

    يعيد:
```text
      [nil]
```

  * **control.shutdown.graceful** - إيقاف تشغيل مثيل i2p بشكل سلس

    * [nil]: لا حاجة لمعلمة

    يعيد:
```text
      [nil]
```

  * **control.update.find** - **حظر** البحث عن تحديثات موقعة

    * [nil]: لا حاجة لمعلمة

    يعيد:
```text
      true [boolean] // True إذا كانت التحديثات الموقعة متوفرة
```

  * **control.update.start** - بدء عملية التحديث

    * [nil]: لا حاجة لمعلمة

    يعيد:
```text
      [nil]
```

* **i2pcontrol.** - قم بتكوين i2pcontrol

  * **i2pcontrol.address** - احصل على/غير عنوان IP الذي يستمع إليه i2pcontrol.

    * *get* [null]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: سيكون هذا عنوان IP مثل "0.0.0.0" أو "192.168.0.1"

    يعيد:
```text
      [nil]
```

  * **i2pcontrol.password** - تغيير كلمة مرور i2pcontrol.

    * *set* [string]: تعيين كلمة المرور الجديدة إلى هذه السلسلة

    يعيد:
```text
      [nil]
```

  * **i2pcontrol.port** - احصل على/غير المنفذ الذي يستمع إليه i2pcontrol.

    * *get* [null]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      7650 [number]
```

    * *set* [number]: غير المنفذ الذي يستمع إليه i2pcontrol إلى هذا المنفذ

    يعيد:
```text
      [nil]
```

* **settings.** - احصل على/غير إعدادات مثيل i2p

  * **settings.advanced** - إعدادات متقدمة

    * *get*  [string]: احصل على قيمة هذا الإعداد

    يعيد:
```text
      "setting-value" [string]
```

    * *getAll* [null]:

    يعيد:
```text
      [object]
      {
        "setting-name" : "setting-value", [string]
        ".." : ".."
      }
```

    * *set* [string]: غير قيمة هذا الإعداد
    * *setAll* [object] {"setting-name" : "setting-value", ".." : ".." }

    يعيد:
```text
      [nil]
```

  * **settings.bandwidth.in** - إعدادات عرض النطاق الترددي الوارد
  * **settings.bandwidth.out** - إعدادات عرض النطاق الترددي الصادر

    * *get* [nil]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      0 [number]
```

    * *set* [number]: حدد حدود عرض النطاق الترددي

    يعيد:
```text
     [nil]
```

  * **settings.ntcp.autoip** - احصل على إعداد الكشف التلقائي عن IP لـ NTCP

    * *get* [null]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      true [boolean]
```

  * **settings.ntcp.hostname** - احصل على اسم مضيف NTCP

    * *get* [null]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: تعيين اسم مضيف جديد

    يعيد:
```text
      [nil]
```

  * **settings.ntcp.port** - منفذ NTCP

    * *get* [null]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      0 [number]
```

    * *set* [number]: تعيين منفذ NTCP جديد.

    يعيد:
```text
      [nil]
```

    * *set* [boolean]: تعيين الكشف التلقائي عن IP لـ NTCP

    يعيد:
```text
      [nil]
```

  * **settings.ssu.autoip** - تكوين إعداد الكشف التلقائي عن IP لـ SSU

    * *get* [nil]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      true [boolean]
```

  * **settings.ssu.hostname** - تكوين اسم المضيف

    * *get* [null]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: تعيين اسم مضيف SSU جديد

    يعيد:
```text
      [nil]
```

  * **settings.ssu.port** - منفذ SSU

    * *get* [null]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      0 [number]
```

    * *set* [number]: تعيين منفذ SSU جديد.

    يعيد:
```text
      [nil]
```

    * *set* [boolean]: تعيين الكشف التلقائي عن IP لـ SSU

    يعيد:
```text
      [nil]
```

  * **settings.share** - احصل على نسبة مشاركة عرض النطاق الترددي

    * *get* [null]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      0 [number] // نسبة مشاركة عرض النطاق الترددي (0-100)
```

    * *set* [number]: تعيين نسبة مشاركة عرض النطاق الترددي (0-100)

    يعيد:
```text
      [nil]
```

  * **settings.upnp** - تفعيل أو تعطيل UPNP

    * *get* [nil]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      true [boolean]
```

    * *set* [boolean]: تعيين الكشف التلقائي عن IP لـ SSU

    يعيد:
```text
      [nil]
```

* **stats.** - احصل على إحصائيات من مثيل i2p

  * **stats.advanced** - توفر هذه الطريقة الوصول إلى جميع الإحصائيات المحفوظة داخل المثيل.

    * *get* [string]:  اسم الإحصائية المتقدمة المطلوب توفيرها
    * *Optional:* *period* [number]:  الفترة للإحصائية المطلوبة

  * **stats.knownpeers** - يعيد عدد الأقران المعروفين
  * **stats.uptime** - يعيد الوقت بالمللي ثانية منذ بدء تشغيل الموجه
  * **stats.bandwidth.in** - يعيد عرض النطاق الترددي الوارد (يفضل للثانية الأخيرة)
  * **stats.bandwidth.in.total** - يعيد عدد البايتات المستلمة منذ آخر إعادة تشغيل
  * **stats.bandwidth.out** - يعيد عرض النطاق الترددي الصادر (يفضل للثانية الأخيرة)'
  * **stats.bandwidth.out.total** - يعيد عدد البايتات المرسلة منذ آخر إعادة تشغيل'
  * **stats.tunnels.participating** - يعيد عدد الأنفاق التي يشارك فيها حاليًا
  * **stats.netdb.peers.active** - يعيد عدد الأقران الذين قمنا مؤخرًا بالتواصل معهم
  * **stats.netdb.peers.fast** - يعيد عدد الأقران "السريع"
  * **stats.netdb.peers.highcapacity** - يعيد عدد الأقران "عالي السعة"
  * **stats.netdb.peers.known** - يعيد عدد الأقران المعروفين

    * *get* [null]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      0.0 [number]
```

* **status.** - احصل على حالة مثيل i2p

  * **status.router** - احصل على حالة الموجه

    * *get* [null]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      "status" [string]
```

  * **status.net** - احصل على حالة شبكة الموجه

    * *get* [null]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      0 [number]
      /**
       *    0 – OK
       *    1 – TESTING
       *    2 – FIREWALLED
       *    3 – HIDDEN
       *    4 – WARN_FIREWALLED_AND_FAST
       *    5 – WARN_FIREWALLED_AND_FLOODFILL
       *    6 – WARN_FIREWALLED_WITH_INBOUND_TCP
       *    7 – WARN_FIREWALLED_WITH_UDP_DISABLED
       *    8 – ERROR_I2CP
       *    9 – ERROR_CLOCK_SKEW
       *   10 – ERROR_PRIVATE_TCP_ADDRESS
       *   11 – ERROR_SYMMETRIC_NAT
       *   12 – ERROR_UDP_PORT_IN_USE
       *   13 – ERROR_NO_ACTIVE_PEERS_CHECK_CONNECTION_AND_FIREWALL
       *   14 – ERROR_UDP_DISABLED_AND_TCP_UNSET
       */
```

  * **status.isfloodfill** - هل مثيل i2p حاليًا يملأ الفيض

    * *get* [null]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      true [boolean]
```

  * **status.isreseeding** - هل مثيل i2p حاليًا يعيد البذور

    * *get* [null]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      true [boolean]
```

  * **status.ip** - عنوان IP العام المكتشف لهذا المثيل من i2p

    * *get* [null]: لا حاجة لتعيين هذه المعلمة.

    يعيد:
```text
      "0.0.0.0" [string]
```
