---
title: "مناقشة التسمية"
description: "الجدل التاريخي حول نموذج التسمية الخاص بـ I2P ولماذا رُفضت المخططات الشبيهة بـ DNS عالميًا"
slug: "naming"
layout: "single"
lastUpdated: "2025-02"
accurateFor: "historical"
reviewStatus: "needs-review"
---

> **السياق:** تؤرشف هذه الصفحة نقاشات طويلة الأمد من الحقبة المبكرة لتصميم I2P. وهي توضّح لماذا فضّل المشروع دفاتر عناوين موثوقة محليًا على عمليات البحث على غرار DNS أو السجلات القائمة على تصويت الأغلبية. للحصول على إرشادات الاستخدام الحالية، راجع [وثائق التسمية](/docs/overview/naming/).

## بدائل مستبعدة

تستبعد الأهداف الأمنية لـ I2P مخططات التسمية المألوفة:

- **حلّ الأسماء بأسلوب DNS.** يمكن لأي محلّل أسماء على مسار الاستعلام أن يزوّر الإجابات أو يفرض رقابة عليها. حتى مع DNSSEC، يظلّ مسجّلو النطاقات أو سلطات الشهادات المخترَقة نقطة فشل وحيدة. في I2P، الوجهات *هي* مفاتيح عامة—واختطاف عملية الاستعلام سيؤدي إلى اختراق الهوية بالكامل.
- **التسمية المعتمدة على التصويت.** يمكن لخصمٍ أن ينشئ هويات غير محدودة (Sybil attack — هجوم سيبيل) وأن "يفوز" بالأصوات للأسماء الشائعة. تخفيفات إثبات العمل ترفع الكلفة لكنها تفرض عبئاً ثقيلاً على التنسيق.

بدلاً من ذلك، تحافظ I2P عمداً على التسمية فوق طبقة النقل. توفّر مكتبة التسمية المرفقة واجهة مزوّد خدمة تتيح لمخططات تسمية بديلة أن تتعايش—ويقرّر المستخدمون أيّ دفاتر عناوين أو خدمات قفز يثقون بها.

## الأسماء المحلية مقابل الأسماء العالمية (jrandom، 2005)

- الأسماء في I2P فريدة محليًا لكنها مقروءة للبشر. قد لا يتطابق `boss.i2p` الخاص بك مع `boss.i2p` الخاص بشخص آخر، وهذا مقصود في التصميم.
- إذا خدعتك جهة خبيثة لتغيير الوجهة وراء اسم ما، فستتمكن فعليًا من اختطاف خدمة. عدم فرض التفرد العالمي يمنع ذلك النوع من الهجمات.
- تعامل مع الأسماء كأنها إشارات مرجعية أو أسماء مستعارة في التراسل الفوري—أنت من يختار الوجهات التي يثق بها عبر الاشتراك في دفاتر عناوين محددة أو إضافة المفاتيح يدويًا.

## الاعتراضات الشائعة والردود (zzz)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Concern</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Downloading hosts.txt is inefficient.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">At ~400&nbsp;KB for ~800 hosts the bandwidth impact is minor (~10&nbsp;B/s if refreshed twice daily). ETags already avoid unnecessary transfers. Alternate formats (for example <code>recenthosts.cgi</code>) can deliver only new entries.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“It won’t scale.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A hosts.txt entry is ~500&nbsp;bytes; storing thousands locally is practical. Real-time lookups would dramatically slow browsing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Requires trust and manual setup.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">True—and intentional. Users must choose address book providers they trust. Trust is not binary; forcing configuration encourages users to think about it.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Why not just use DNS?”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS depends on short TTLs and can be hijacked mid-path. I2P destinations are immutable public keys, so DNS semantics map poorly.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Subscriptions rely on specific servers.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscriptions are decentralised—you can add multiple providers or run your own. Completely decentralised systems struggle with conflict resolution and hijacking.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Jump services and hosts.txt feel awkward.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">They are pragmatic trade-offs. Jump services provide just-in-time lookups; subscriptions keep a local cache for performance.</td>
    </tr>
  </tbody>
</table>
## مناقشة أفكار تحسين الكفاءة

- قدّم تحديثات تدريجية (فقط الوجهات التي أضيفت منذ آخر جلب).
- وفّر خلاصات إضافية (`recenthosts.cgi`) إلى جانب ملفات hosts الكاملة.
- استكشف أدوات قابلة للبرمجة النصية (على سبيل المثال، `i2host.i2p`) لدمج الخلاصات أو التصفية حسب مستويات الثقة.

## أبرز النقاط

- يتفوّق الأمان على الإجماع العالمي: تقلّل دفاتر العناوين المنسّقة محليًا من مخاطر الاختطاف.
- يمكن لأساليب تسمية متعددة أن تتعايش عبر واجهة برمجة تطبيقات التسمية—والمستخدمون يقررون ما يثقون به.
- لا يزال نظام تسمية عالمي لامركزي بالكامل مسألة بحثية مفتوحة؛ ولا تزال المفاضلات بين الأمان، وسهولة التذكّر البشري، والتفرّد العالمي تعكس [مثلث زوكو](https://zooko.com/distnames.html).

## المراجع

- [وثائق التسمية](/docs/overview/naming/)
- [«الأسماء: لامركزية، آمنة، ذات معنى بشري: اختر اثنين» لزوكو](https://zooko.com/distnames.html)
- عينة خلاصة تزايدية: [stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
