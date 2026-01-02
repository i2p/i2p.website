---
title: "دمج I2P في تطبيقك"
description: "إرشادات عملية محدّثة لتضمين router الخاص بـ I2P مع تطبيقك بشكل مسؤول"
slug: "embedding"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

دمج I2P مع تطبيقك هو طريقة قوية لإضافة المستخدمين—ولكن فقط إذا تم تكوين الـ router بشكل مسؤول.

## 1. التنسيق مع فرق الموجه (Router)

- اتصل بمسؤولي صيانة **Java I2P** و**i2pd** قبل التضمين. يمكنهم مراجعة إعداداتك الافتراضية وتسليط الضوء على مخاوف التوافق.
- اختر تطبيق router الذي يناسب مجموعتك التقنية:
  - **Java/Scala** → Java I2P
  - **C/C++** → i2pd
  - **لغات أخرى** → قم بتضمين router والتكامل باستخدام [SAM v3](/docs/api/samv3/) أو [I2CP](/docs/specs/i2cp/)
- تحقق من شروط إعادة التوزيع للملفات التنفيذية لـ router والتبعيات (Java runtime، ICU، إلخ).

## 2. الإعدادات الافتراضية الموصى بها

اهدف إلى "المساهمة أكثر مما تستهلك". الإعدادات الافتراضية الحديثة تعطي الأولوية لصحة الشبكة واستقرارها.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Setting</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Default (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth share</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">80% for participating tunnels </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel quantities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd: 3 inbound / 3 outbound; Java I2P: 2 inbound / 2 outbound. </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature &amp; encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use Ed25519 (<code>SIGNATURE_TYPE=7</code>) and advertise ECIES-X25519 + ElGamal (<code>i2cp.leaseSetEncType=4,0</code>).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Client protocols</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use SAM v3 or I2CP.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">API listeners</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bind SAM/I2CP to <code>127.0.0.1</code> only. Disable if not needed.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UI toggles</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Expose bandwidth controls, logs, and an opt-in checkbox for participating tunnels.</td>
    </tr>
  </tbody>
</table>
### الأنفاق المشاركة تبقى أساسية

**لا** تقم بتعطيل الأنفاق المشاركة (participating tunnels).

1. أجهزة Router التي لا تقوم بالترحيل تعمل بشكل أسوأ بنفسها.
2. تعتمد الشبكة على المشاركة الطوعية للسعة.
3. حركة المرور التغطية (حركة المرور المُرحّلة) تحسن إخفاء الهوية.

**الحد الأدنى الرسمي:** - عرض النطاق المشترك: ≥ 12 كيلوبايت/ثانية   - الانضمام التلقائي لـ Floodfill: ≥ 128 كيلوبايت/ثانية   - الموصى به: 2 tunnel وارد / 2 tunnel صادر (الإعداد الافتراضي لـ Java I2P)

## 3. الاستمرارية وإعادة البذر

يجب الحفاظ على أدلة الحالة الدائمة (`netDb/`، profiles، certificates) بين عمليات التشغيل.

بدون الاستمرارية، سيقوم المستخدمون بتشغيل عمليات إعادة البذر عند كل بدء تشغيل—مما يؤدي إلى تدهور الأداء وزيادة الحمل على خوادم إعادة البذر.

إذا كانت الاستمرارية غير ممكنة (مثل الحاويات أو التثبيتات المؤقتة):

1. قم بتضمين **1,000–2,000 router infos** في برنامج التثبيت.
2. قم بتشغيل واحد أو أكثر من خوادم reseed مخصصة لتخفيف الحمل عن الخوادم العامة.

متغيرات التكوين: - الدليل الأساسي: `i2p.dir.base` - دليل التكوين: `i2p.dir.config` - يتضمن `certificates/` لإعادة البذر.

## 4. الأمان والتعرض للخطر

- احتفظ بوحدة تحكم router (`127.0.0.1:7657`) محلية فقط.
- استخدم HTTPS في حالة عرض واجهة المستخدم خارجيًا.
- عطّل SAM/I2CP الخارجي ما لم يكن مطلوبًا.
- راجع الإضافات المُضمّنة—قم بتضمين ما يدعمه تطبيقك فقط.
- قم دائمًا بتضمين المصادقة للوصول عن بُعد إلى وحدة التحكم.

**ميزات الأمان المقدمة منذ الإصدار 2.5.0:** - عزل NetDB بين التطبيقات (2.4.0+)   - التخفيف من هجمات حجب الخدمة وقوائم حظر Tor (2.5.1)   - مقاومة فحص NTCP2 (2.9.0)   - تحسينات اختيار router من نوع Floodfill (2.6.0+)

## 5. واجهات برمجة التطبيقات المدعومة (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recommended bridge for non-Java apps.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable protocol core, used internally by Java I2P.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PControl</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSON-RPC API; plugin maintained.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚠️ Deprecated</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed from Java I2P since 1.7.0; use SAM v3 instead.</td>
    </tr>
  </tbody>
</table>
جميع المستندات الرسمية موجودة تحت `/docs/api/` — المسار القديم `/spec/samv3/` **غير موجود**.

## 6. الشبكات والمنافذ

المنافذ الافتراضية النموذجية: - 4444 – بروكسي HTTP   - 4445 – بروكسي HTTPS   - 7654 – I2CP   - 7656 – جسر SAM Bridge   - 7657 – لوحة تحكم Router Console   - 7658 – موقع I2P محلي   - 6668 – بروكسي IRC   - 9000–31000 – منفذ router عشوائي (UDP/TCP وارد)

تختار أجهزة التوجيه منفذًا عشوائيًا للاتصالات الواردة عند التشغيل الأول. يؤدي إعادة التوجيه إلى تحسين الأداء، ولكن قد يتعامل UPnP مع ذلك تلقائيًا.

## 7. التغييرات الحديثة (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2 is now the exclusive UDP transport.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blocked</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 2.6.0 (July 2024).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram2/3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated, repliable datagram formats (2.9.0).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet service records</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enables service discovery (Proposal 167).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tunnel build parameters</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adaptive congestion handling (2.9.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-quantum crypto</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced (beta)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM hybrid ratchet, opt-in from 2.10.0.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 requirement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Announced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Becomes mandatory in 2.11.0 (early 2026).</td>
    </tr>
  </tbody>
</table>
## 8. تجربة المستخدم والاختبار

- توضيح ما يقوم به I2P ولماذا يتم مشاركة النطاق الترددي.
- توفير تشخيصات الموجه (النطاق الترددي، الأنفاق، حالة إعادة البذر).
- اختبار الحزم على Windows وmacOS وLinux (بما في ذلك الأجهزة ذات الذاكرة المنخفضة).
- التحقق من التوافق مع كل من أقران **Java I2P** و**i2pd**.
- اختبار الاستعادة من انقطاع الشبكة والخروج غير السليم.

## 9. موارد المجتمع

- المنتدى: [i2pforum.net](https://i2pforum.net) أو `http://i2pforum.i2p` داخل I2P.  
- الكود: [i2pgit.org/I2P_Developers/i2p.i2p](https://i2pgit.org/I2P_Developers/i2p.i2p).  
- IRC (شبكة Irc2P): `#i2p-dev`، `#i2pd`.  
  - `#i2papps` غير موثق؛ قد لا يكون موجوداً.  
  - وضح أي شبكة (Irc2P مقابل ilita.i2p) تستضيف قناتك.

التضمين المسؤول يعني الموازنة بين تجربة المستخدم، الأداء، والمساهمة في الشبكة. استخدم هذه الإعدادات الافتراضية، ابقَ متزامناً مع مشرفي الـ router، واختبر تحت حمل واقعي قبل الإصدار.
