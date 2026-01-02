---
title: "عملاء I2P البديلون"
description: "تطبيقات عميل I2P التي يحافظ عليها المجتمع (محدثة لعام 2025)"
slug: "alternative-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

التطبيق الرئيسي لعميل I2P يستخدم **Java**. إذا كنت لا تستطيع أو تفضل عدم استخدام Java على نظام معين، فهناك تطبيقات بديلة لعميل I2P تم تطويرها وصيانتها من قبل أعضاء المجتمع. توفر هذه البرامج نفس الوظائف الأساسية باستخدام لغات برمجة أو أساليب مختلفة.

---

## جدول المقارنة

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Client</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Maturity</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Actively Maintained</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Suitable For</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java I2P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes (official)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">General users</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard full router; includes console, plugins, and tools</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-resource systems, servers</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lightweight, fully compatible with Java I2P, includes web console</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Go-I2P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚙️ In development</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Developers, testing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Early-stage Go implementation; not yet production ready</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P+</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable (fork)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Advanced users</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced Java I2P fork with UI and performance improvements</td>
    </tr>
  </tbody>
</table>
---

## i2pd (C++)

**الموقع الإلكتروني:** [https://i2pd.website](https://i2pd.website)

**الوصف:** i2pd (أو *I2P Daemon*) هو عميل I2P كامل الميزات مُطبّق بلغة C++. وهو مستقر للاستخدام الإنتاجي منذ سنوات عديدة (منذ حوالي 2016 تقريباً) ويتم صيانته بنشاط من قبل المجتمع. يُطبّق i2pd بشكل كامل بروتوكولات وواجهات برمجة التطبيقات الخاصة بشبكة I2P، مما يجعله متوافقاً تماماً مع شبكة I2P المبنية على Java. غالباً ما يُستخدم هذا router المكتوب بلغة C++ كبديل خفيف على الأنظمة التي لا تتوفر فيها بيئة تشغيل Java أو غير مرغوب فيها. يتضمن i2pd وحدة تحكم مدمجة قائمة على الويب للتكوين والمراقبة. وهو متعدد المنصات ومتاح بصيغ تغليف متعددة — بل يوجد أيضاً إصدار Android من i2pd متاح (على سبيل المثال، عبر F-Droid).

---

## Go-I2P (Go)

**المستودع:** [https://github.com/go-i2p/go-i2p](https://github.com/go-i2p/go-i2p)

**الوصف:** Go-I2P هو عميل I2P مكتوب بلغة البرمجة Go. وهو تطبيق مستقل لجهاز router الخاص بـ I2P، يهدف إلى الاستفادة من كفاءة وقابلية نقل Go. المشروع قيد التطوير النشط، لكنه لا يزال في مرحلة مبكرة وليس مكتمل الميزات بعد. اعتبارًا من عام 2025، يُعتبر Go-I2P تجريبيًا — حيث يعمل عليه مطورو المجتمع بنشاط، لكن لا يُنصح باستخدامه في بيئات الإنتاج حتى ينضج أكثر. الهدف من Go-I2P هو توفير router حديث وخفيف الوزن لـ I2P مع توافق كامل مع شبكة I2P بمجرد اكتمال التطوير.

---

## I2P+ (نسخة Java)

**الموقع الإلكتروني:** [https://i2pplus.github.io](https://i2pplus.github.io)

**الوصف:** I2P+ هو نسخة مطورة مجتمعياً من عميل Java I2P القياسي. إنه ليس إعادة تطبيق بلغة جديدة، بل هو نسخة محسّنة من router جافا مع ميزات وتحسينات إضافية. يركز I2P+ على تقديم تجربة مستخدم محسّنة وأداء أفضل مع الحفاظ على التوافق الكامل مع شبكة I2P الرسمية. يقدم واجهة web console محدّثة، وخيارات إعداد أكثر سهولة في الاستخدام، وتحسينات متنوعة (على سبيل المثال، أداء torrent محسّن ومعالجة أفضل لنظراء الشبكة، خاصة لأجهزة router خلف الجدران النارية). يتطلب I2P+ بيئة Java تماماً مثل برنامج I2P الرسمي، لذا فهو ليس حلاً للبيئات غير المعتمدة على Java. ومع ذلك، بالنسبة للمستخدمين الذين لديهم Java ويريدون نسخة بديلة بقدرات إضافية، يوفر I2P+ خياراً جذاباً. يتم تحديث هذه النسخة المطورة باستمرار مع إصدارات I2P الأساسية (مع إضافة "+" إلى ترقيم الإصدار) ويمكن الحصول عليها من موقع المشروع.
