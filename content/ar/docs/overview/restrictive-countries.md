---
title: "البلدان الصارمة/المقيدة"
description: "كيف يتصرف I2P في الولايات القضائية التي تفرض قيودًا على أدوات التوجيه أو إخفاء الهوية (الوضع المخفي والقائمة الصارمة)"
slug: "restrictive-countries"
lastUpdated: "2024-07"
accurateFor: "2.10.0"
type: الوثائق
reviewStatus: "needs-review"
---

يتضمن هذا التطبيق من I2P (تطبيق Java الموزع على هذا الموقع) "قائمة البلدان الصارمة" المستخدمة لتعديل سلوك router في المناطق التي قد يكون فيها المشاركة في routing للآخرين مقيدًا بموجب القانون. على الرغم من أننا لسنا على علم بولايات قضائية تحظر استخدام I2P، إلا أن العديد منها لديه حظر واسع على نقل حركة المرور (relaying traffic). يتم وضع routers التي يبدو أنها في البلدان "الصارمة" تلقائيًا في وضع Hidden (المخفي).

يشير المشروع إلى الأبحاث الصادرة عن منظمات الحقوق المدنية والرقمية عند اتخاذ هذه القرارات. وعلى وجه الخصوص، تُوجّه الأبحاث المستمرة التي تُجريها منظمة فريدم هاوس (Freedom House) خياراتنا. التوجيه العام هو تضمين الدول التي لديها درجة حريات مدنية (CL) تبلغ 16 أو أقل، أو درجة حرية الإنترنت تبلغ 39 أو أقل (غير حرة).

## ملخص الوضع المخفي

عندما يتم وضع router في وضع الإخفاء (Hidden mode)، تتغير ثلاثة أشياء رئيسية في سلوكه:

- لا ينشر معلومات الموجه (RouterInfo) إلى قاعدة بيانات الشبكة (netDb).
- لا يقبل أنفاق المشاركة (participating tunnels).
- يرفض الاتصالات المباشرة بالموجهات في نفس البلد.

هذه الدفاعات تجعل أجهزة التوجيه (routers) أكثر صعوبة في الإحصاء بشكل موثوق، وتقلل من خطر انتهاك الحظر المحلي على نقل حركة المرور للآخرين.

## قائمة البلدان ذات الرقابة الصارمة (اعتبارًا من 2024)

```
/* Afghanistan */ "AF",
/* Azerbaijan */ "AZ",
/* Bahrain */ "BH",
/* Belarus */ "BY",
/* Brunei */ "BN",
/* Burundi */ "BI",
/* Cameroon */ "CM",
/* Central African Republic */ "CF",
/* Chad */ "TD",
/* China */ "CN",
/* Cuba */ "CU",
/* Democratic Republic of the Congo */ "CD",
/* Egypt */ "EG",
/* Equatorial Guinea */ "GQ",
/* Eritrea */ "ER",
/* Ethiopia */ "ET",
/* Iran */ "IR",
/* Iraq */ "IQ",
/* Kazakhstan */ "KZ",
/* Laos */ "LA",
/* Libya */ "LY",
/* Myanmar */ "MM",
/* North Korea */ "KP",
/* Palestinian Territories */ "PS",
/* Pakistan */ "PK",
/* Rwanda */ "RW",
/* Saudi Arabia */ "SA",
/* Somalia */ "SO",
/* South Sudan */ "SS",
/* Sudan */ "SD",
/* Eswatini (Swaziland) */ "SZ",
/* Syria */ "SY",
/* Tajikistan */ "TJ",
/* Thailand */ "TH",
/* Turkey */ "TR",
/* Turkmenistan */ "TM",
/* Venezuela */ "VE",
/* United Arab Emirates */ "AE",
/* Uzbekistan */ "UZ",
/* Vietnam */ "VN",
/* Western Sahara */ "EH",
/* Yemen */ "YE"
```
إذا كنت تعتقد أن دولة ما يجب إضافتها أو إزالتها من القائمة الصارمة، يرجى فتح تذكرة على: https://i2pgit.org/i2p/i2p.i2p/

المرجع: Freedom House – https://freedomhouse.org/
