---
title: "كيفية التبديل إلى خدمة StormyCloud Outproxy"
date: 2022-08-04
author: "idk"
description: "كيفية التبديل إلى خدمة StormyCloud Outproxy (الوكيل الخارجي)"
categories: ["general"]
---

## كيفية التبديل إلى خدمة StormyCloud Outproxy (وكيل الخروج)

**وكيل خروج جديد واحترافي**

لسنوات، كانت I2P تعتمد على outproxy (خادم وسيط للخروج إلى الإنترنت المفتوح) افتراضي واحد، `false.i2p`، التي تراجعت موثوقيتها. وعلى الرغم من ظهور عدة منافسين لتغطية جزء من النقص، فإنهم في الغالب غير قادرين على التطوع لخدمة مستخدمي تنفيذ I2P كامل بشكل افتراضي. ومع ذلك، فقد أطلقت StormyCloud، وهي منظمة احترافية غير ربحية تدير عقد خروج Tor، خدمة outproxy احترافية جديدة، جرى اختبارها من قبل أعضاء مجتمع I2P، وستصبح outproxy الافتراضي الجديد في الإصدار القادم.

**من هم StormyCloud**

بكلماتهم الخاصة، فإن StormyCloud هي:

> Mission of StormyCloud Inc: To defend Internet access as a universal human right. By doing so, the group protects users' electronic privacy and builds community by fostering unrestricted access to information and thus the free exchange of ideas across borders. This is essential because the Internet is the most powerful tool available for making a positive difference in the world.

> الأجهزة: نملك جميع أجهزتنا ونقوم حالياً بالاستضافة المشتركة في مركز بيانات من فئة Tier 4. لدينا في الوقت الحالي ارتباط صاعد بسرعة 10GBps مع خيار الترقية إلى 40GBps من دون الحاجة إلى تغييرات كبيرة. لدينا ASN (رقم النظام المستقل) خاص بنا وحيّز عناوين IP (IPv4 وIPv6).

لمعرفة المزيد عن StormyCloud، زر [موقعهم الإلكتروني](https://www.stormycloud.org/).

أو زرهم على [I2P](http://stormycloud.i2p/).

**التبديل إلى StormyCloud Outproxy (وكيل الخروج) على I2P**

للتبديل إلى outproxy (وكيل خارجي) StormyCloud *اليوم* يمكنك زيارة [مدير الخدمات المخفية](http://127.0.0.1:7657/i2ptunnel/edit?tunnel=0). بمجرد وصولك إلى هناك، ينبغي عليك تغيير قيمة **Outproxies** و **SSL Outproxies** إلى `exit.stormycloud.i2p`. بعد أن تقوم بذلك، مرّر إلى أسفل الصفحة وانقر على زر "Save".

**شكرًا لـ StormyCloud**

نود أن نشكر StormyCloud على تطوعها لتقديم خدمات outproxy (الوكيل الخارجي) عالية الجودة لشبكة I2P.
