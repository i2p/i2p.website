---
title: "SAM v2"
description: "البروتوكول القديم للمراسلة المجهولة البسيطة"
slug: "samv2"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **مهمل:** تم تضمين SAM v2 مع I2P 0.6.1.31 ولم يعد يُصان. استخدم [SAM v3](/docs/api/samv3/) للتطوير الجديد. كان التحسين الوحيد في v2 مقارنةً بـ v1 هو دعم عدة مقابس مُتعددة الإرسال عبر اتصال SAM واحد.

## ملاحظات الإصدار

- تظل سلسلة الإصدار المُبلّغ عنها "2.0".
- اعتبارًا من 0.9.14 تقبل رسالة `HELLO VERSION` قيَم `MIN`/`MAX` المؤلفة من رقم واحد، ومعلمة `MIN` اختيارية.
- يدعم `DEST GENERATE` `SIGNATURE_TYPE`، لذا يمكن إنشاء وجهات Ed25519.

## أساسيات الجلسة

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]
```
- قد يكون لكل وجهة جلسة SAM نشطة واحدة فقط (تدفقات، datagrams (حزم بيانات غير متصلة)، أو خام).
- `STYLE` يختار التدفقات الافتراضية، datagrams الموقعة، أو datagrams الخام.
- تُمرَّر الخيارات الإضافية إلى I2CP (على سبيل المثال، `tunnels.quantityInbound=3`).
- الاستجابات مماثلة لـ v1: `SESSION STATUS RESULT=OK|DUPLICATED_DEST|I2P_ERROR|INVALID_KEY`.

## ترميز الرسائل

ASCII القائم على الأسطر مع أزواج `key=value` مفصولة بمسافات (قد تُوضَع القيم بين علامات اقتباس). أنواع الاتصال هي نفسها كما في v1:

- تدفقات عبر مكتبة التدفق الخاصة بـ I2P
- داتاغرامات قابلة للرد (`PROTO_DATAGRAM`)
- داتاغرامات خام (`PROTO_DATAGRAM_RAW`)

## متى يجب استخدامه

مخصص فقط للعملاء القديمة التي لا يمكنها الترحيل. يوفر SAM v3:

- تمرير الوجهة الثنائية (`DEST GENERATE BASE64`)
- دعم الجلسات الفرعية وDHT (جدول تجزئة موزع) (v3.3)
- تحسين الإبلاغ عن الأخطاء وتفاوض الخيارات

راجع:

- [SAM v1](/docs/legacy/sam/)
- [SAM v3](/docs/api/samv3/)
- [واجهة برمجة تطبيقات الداتاغرام](/docs/api/datagrams/)
- [بروتوكول البث](/docs/specs/streaming/)
