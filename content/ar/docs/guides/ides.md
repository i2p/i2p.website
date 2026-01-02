---
title: "استخدام بيئة تطوير متكاملة (IDE) مع I2P"
description: "إعداد Eclipse وNetBeans لتطوير I2P باستخدام Gradle وملفات المشروع المرفقة"
slug: "ides"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

<p> تم إعداد فرع التطوير الرئيسي لـ I2P (<code>i2p.i2p</code>) لتمكين المطورين من إعداد اثنتين من بيئات التطوير المتكاملة الشائعة الاستخدام لتطوير Java بسهولة: Eclipse و NetBeans. </p>

<h2>Eclipse</h2>

<p> تحتوي فروع التطوير الرئيسية لـ I2P (<code>i2p.i2p</code> والفروع المتفرعة منها) على <code>build.gradle</code> لتمكين إعداد الفرع بسهولة في Eclipse. </p>

<ol> <li> تأكد من أن لديك إصدار حديث من Eclipse. أي إصدار أحدث من 2017 سيفي بالغرض. </li> <li> قم بسحب فرع I2P إلى دليل ما (مثل <code>$HOME/dev/i2p.i2p</code>). </li> <li> اختر "File → Import..." ثم تحت "Gradle" اختر "Existing Gradle Project". </li> <li> في خانة "Project root directory:" اختر الدليل الذي تم سحب فرع I2P إليه. </li> <li> في مربع حوار "Import Options"، اختر "Gradle Wrapper" واضغط Continue. </li> <li> في مربع حوار "Import Preview" يمكنك مراجعة هيكل المشروع. يجب أن تظهر مشاريع متعددة تحت "i2p.i2p". اضغط "Finish". </li> <li> تم! يجب أن تحتوي مساحة العمل الخاصة بك الآن على جميع المشاريع داخل فرع I2P، ويجب أن تكون تبعيات البناء الخاصة بها معدة بشكل صحيح. </li> </ol>

<h2>NetBeans</h2>

<p> تحتوي فروع التطوير الرئيسية لـ I2P (<code>i2p.i2p</code> والفروع المشتقة منها) على ملفات مشروع NetBeans. </p>

```markdown
<!-- احتفظ بالمحتوى بسيطاً وقريباً من النص الأصلي؛ سيتم التحديث لاحقاً. -->
```
