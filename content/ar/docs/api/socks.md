---
title: "بروكسي SOCKS"
description: "استخدام نفق SOCKS الخاص بـ I2P بأمان"
slug: "socks"
aliases:
  - "/ar/socks"
  - "/ar/socks/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## SOCKS وخوادم SOCKS الوكيلة {#overview}

يعمل بروكسي SOCKS اعتباراً من الإصدار 0.7.1. تدعم SOCKS 4/4a/5. قم بتفعيل SOCKS عن طريق إنشاء tunnel عميل SOCKS في i2ptunnel. يدعم كل من العملاء المشتركين وغير المشتركين. لا يوجد SOCKS outproxy لذلك فائدته محدودة.

كما هو مذكور في [الأسئلة الشائعة](/docs/overview/faq#socks):

```
Many applications leak sensitive information that could identify you on the
Internet. I2P only filters connection data, but if the program you intend to
run sends this information as content, I2P has no way to protect your anonymity.
For example, some mail applications will send the IP address of the machine
they are running on to a mail server. There is no way for I2P to filter this,
thus using I2P to 'socksify' existing applications is possible, but extremely
dangerous.
```
وبالاقتباس من رسالة إلكترونية لعام 2005:

```
... there is a reason why human and others have both built and abandoned the
SOCKS proxies. Forwarding arbitrary traffic is just plain unsafe, and it
behooves us as developers of anonymity and security software to have the safety
of our end users foremost in our minds.
```
الأمل في أن نتمكن ببساطة من ربط عميل عشوائي فوق I2P دون مراجعة سلوكه والبروتوكولات المكشوفة منه من ناحية الأمان وإخفاء الهوية أمر ساذج. تقريباً *كل* تطبيق وبروتوكول ينتهك إخفاء الهوية، إلا إذا تم تصميمه خصيصاً لهذا الغرض، وحتى في هذه الحالة، معظمها ينتهكه أيضاً. هذا هو الواقع. المستخدمون النهائيون يُخدمون بشكل أفضل بأنظمة مصممة لإخفاء الهوية والأمان. تعديل الأنظمة الموجودة للعمل في بيئات مجهولة الهوية ليس بالأمر الهين، بل يتطلب عملاً أكثر بمراتب عديدة من مجرد استخدام APIs الموجودة في I2P.

يدعم SOCKS proxy أسماء دفتر العناوين القياسية، لكن ليس وجهات Base64. يجب أن تعمل hashes Base32 اعتباراً من الإصدار 0.7. يدعم الاتصالات الصادرة فقط، أي I2PTunnel Client. دعم UDP محدد في الكود لكنه لا يعمل بعد. اختيار outproxy حسب رقم المنفذ محدد في الكود.

## انظر أيضاً {#see-also}

- ملاحظات الاجتماع 81 (16 مارس، 2004) والاجتماع 82 (23 مارس، 2004).
- [Onioncat](http://www.abenteuerland.at/onioncat/)

## إذا تمكنت من تشغيل شيء ما {#working}

يرجى إعلامنا. ويرجى تقديم تحذيرات واضحة حول مخاطر وكلاء SOCKS.
