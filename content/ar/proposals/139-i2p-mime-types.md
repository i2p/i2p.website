---
title: "أنواع MIME في I2P"
number: "139"
author: "zzz"
created: "2017-05-16"
lastupdated: "2017-05-16"
status: "Open"
thread: "http://zzz.i2p/topics/1957"
---

## نظرة عامة

تحديد أنواع MIME لأشكال ملفات I2P الشائعة.
قم بتضمين التعريفات في حزم Debian.
توفير معالج لنوع .su3، وربما الأنواع الأخرى.


## الدافع

لتسهيل عملية إعادة التوزيع وتثبيت الملحقات عند التحميل باستخدام المتصفح،
نحتاج إلى نوع MIME ومعالج لملفات .su3.

بينما نحن في ذلك، بعد تعلم كيفية كتابة ملف تعريف MIME،
وفقًا لمعيار freedesktop.org، يمكننا إضافة تعريفات لأنواع ملفات I2P الشائعة الأخرى.
على الرغم من أنها أقل فائدة للملفات التي لا يتم تحميلها عادةً، مثل
قاعدة البيانات لحظر دفتر العناوين (hostsdb.blockfile)، فإن هذه التعريفات ستسمح
بتحديد أيقونات الملفات بشكل أفضل عند استخدام عارض دليل رسومي مثل "nautilus" على Ubuntu.

من خلال توحيد أنواع MIME، يمكن لكل عملية توجيه كتابة معالجاتها
بما يتناسب، ويمكن مشاركة ملف تعريف MIME من قبل جميع العمليات.


## التصميم

كتابة ملف مصدر XML وفقًا لمعيار freedesktop.org وتضمينه
في حزم Debian. الملف هو "debian/(package).sharedmimeinfo".

ستبدأ جميع أنواع MIME في I2P بـ "application/x-i2p-"، باستثناء jrobin rrd.

المعالجين لهذه الأنواع من MIME يعتمدون على التطبيق ولن يتم
تحديدهم هنا.

سنقوم أيضًا بتضمين التعريفات مع Jetty، وتضمينها مع
برنامج إعادة التوزيع أو التعليمات.

## المواصفات

.blockfile 		application/x-i2p-blockfile

.config 		application/x-i2p-config

.dat	 		application/x-i2p-privkey

.dat	 		application/x-i2p-dht

=.dat	 		application/x-i2p-routerinfo

.ht	 		application/x-i2p-errorpage

.info	 		application/x-i2p-routerinfo

.jrb	 		application/x-jrobin-rrd

.su2			application/x-i2p-update

.su3	(generic)	application/x-i2p-su3

.su3	(router update)	application/x-i2p-su3-update

.su3	(plugin)	application/x-i2p-su3-plugin

.su3	(reseed)	application/x-i2p-su3-reseed

.su3	(news)		application/x-i2p-su3-news

.su3	(blocklist)	application/x-i2p-su3-blocklist

.sud			application/x-i2p-update

.syndie	 		application/x-i2p-syndie

=.txt.gz 		application/x-i2p-peerprofile

.xpi2p	 		application/x-i2p-plugin

## ملاحظات

ليست كل أشكال الملفات المدرجة أعلاه مستخدمة في عمليات التوجيه غير الـ Java؛
قد لا يكون البعض حتى محددًا جيدًا. ومع ذلك، توثيقها هنا
قد يمكّن من توفير الاتساق عبر العمليات في المستقبل.

بعض اللاحقات مثل ".config"، ".dat" و ".info" قد تتداخل مع أنواع
MIME أخرى. يمكن تمييزها باستخدام بيانات إضافية مثل
الاسم الكامل للملف، نمط اسم الملف، أو أرقام سحرية.
انظر مسودة ملف i2p.sharedmimeinfo في موضوع zzz.i2p للمزيد من الأمثلة.

المهمون هم أنواع .su3، وهذه الأنواع لها كلاهما
لاحقة فريدة وتعريفات أرقام سحرية قوية.


## الانتقال

غير قابل للتطبيق.
