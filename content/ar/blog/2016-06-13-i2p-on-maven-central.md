---
title: "I2P على Maven Central"
date: 2016-06-13
author: "str4d"
description: "أصبحت مكتبات عميل I2P متاحة الآن على Maven Central!"
categories: ["summer-dev"]
---

لقد شارفنا على منتصف شهر واجهات برمجة التطبيقات ضمن Summer Dev، ونحرز تقدماً كبيراً على عدة جبهات. ويسعدني أن أعلن أن أول هذه الإنجازات قد اكتمل: أصبحت مكتبات العميل الخاصة بـ I2P متاحة الآن على Maven Central!

سيجعل ذلك الأمر أبسط بكثير لمطوري جافا لاستخدام I2P في تطبيقاتهم. بدلًا من الحاجة إلى الحصول على المكتبات من التثبيت الحالي، يمكنهم ببساطة إضافة I2P إلى تبعياتهم. وبالمثل، ستكون الترقية إلى إصدارات جديدة أسهل بكثير.

## كيفية استخدامها

هناك مكتبتان يجب أن تعرفهما:

- `net.i2p:i2p` - The core I2P APIs; you can use these to send individual datagrams.
- `net.i2p.client:streaming` - A TCP-like set of sockets for communicating over I2P.

أضف واحدًا من هذين أو كليهما إلى تبعيات مشروعك، وستكون جاهزًا للانطلاق!

### Gradle

```
compile 'net.i2p:i2p:0.9.26'
compile 'net.i2p.client:streaming:0.9.26'
```
### Gradle

```xml
<dependency>
    <groupId>net.i2p</groupId>
    <artifactId>i2p</artifactId>
    <version>0.9.26</version>
</dependency>
<dependency>
    <groupId>net.i2p.client</groupId>
    <artifactId>streaming</artifactId>
    <version>0.9.26</version>
</dependency>
```
بالنسبة إلى أنظمة البناء الأخرى، راجع صفحات Maven Central الخاصة بمكتبتي core و streaming.

ينبغي لمطوري Android استخدام مكتبة عميل I2P الخاصة بـ Android، التي تتضمن المكتبات نفسها إضافةً إلى أدوات مساعدة خاصة بـ Android. سأقوم بتحديثها قريبًا لتعتمد على مكتبات I2P الجديدة، بحيث تتمكّن التطبيقات متعددة المنصات من العمل بشكل أصلي مع I2P على Android أو مع I2P على سطح المكتب.

## Get hacking!

اطّلع على دليل تطوير التطبيقات لدينا للحصول على مساعدة للبدء باستخدام هذه المكتبات. يمكنك أيضًا الدردشة معنا حولها في #i2p-dev على IRC. وإن بدأت باستخدامها، فأخبرنا بما تعمل عليه عبر الوسم #I2PSummer على Twitter!
