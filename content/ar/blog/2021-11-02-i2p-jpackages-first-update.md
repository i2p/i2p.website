---
title: "I2P Jpackages تتلقى أول تحديث لها"
date: 2021-11-02
author: "idk"
description: "تصل الحزم الجديدة الأسهل تثبيتًا إلى مرحلة مهمة جديدة"
categories: ["general"]
---

قبل بضعة أشهر أصدرنا حزمًا جديدة كنا نأمل أن تساعد في تسهيل انضمام أشخاص جدد إلى شبكة I2P من خلال جعل تثبيت وتهيئة I2P أسهل لعدد أكبر من الأشخاص. أزلنا عشرات الخطوات من عملية التثبيت بالانتقال من JVM خارجي إلى Jpackage، وبنينا حزمًا قياسية لأنظمة التشغيل المستهدفة، ووقّعناها بطريقة يتعرّف إليها نظام التشغيل للحفاظ على أمان المستخدم. منذ ذلك الحين، وصلت routers المبنية باستخدام jpackage (الموجّهات في I2P) إلى إنجاز جديد، فهي على وشك تلقي أول تحديثات تدريجية لها. ستستبدل هذه التحديثات jpackage المبني على JDK 16 بـ jpackage محدَّث مبني على JDK 17، وستوفّر إصلاحات لبعض الأخطاء البسيطة التي اكتشفناها بعد الإصدار.

## التحديثات المشتركة بين نظامَي Mac OS وWindows

تتلقى جميع مُثبِّتات I2P jpackaged (مجمّعة باستخدام jpackage) التحديثات التالية:

* Update the jpackaged I2P router to 1.5.1 which is built with JDK 17

يرجى التحديث في أقرب وقت ممكن.

## تحديثات Jpackage الخاصة بـ I2P على Windows

الحزم المخصّصة لـ Windows فقط تتلقى التحديثات التالية:

* Updates I2P in Private Browsing, NoScript browser extensions
* Begins to phase out HTTPS everywhere on new Firefox releases
* Updates launcher script to fix post NSIS launch issue on some architectures

للاطلاع على قائمة كاملة بالتغييرات، راجع changelog.txt في i2p.firefox

## تحديثات Jpackage لنظام Mac OS الخاصة بـ I2P

تتلقى حزم Mac OS فقط التحديثات التالية:

* No Mac-Specific changes. Mac OS is updated to build with JDK 17.

للاطّلاع على ملخص التطوير، راجع الالتزامات في i2p-jpackage-mac
