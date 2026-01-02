---
title: "مواصفة تحديث البرمجيات"
description: "آلية تحديث آمنة وموقّعة وهيكلية الخلاصة لـ I2P routers"
slug: "updates"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## نظرة عامة

Routers تتحقق تلقائيًا من وجود تحديثات عبر الاستعلام الدوري لموجز أخبار موقّع والموزَّع عبر شبكة I2P. عند الإعلان عن إصدار أحدث، يقوم router بتنزيل أرشيف تحديث موقّع تشفيريًا (`.su3`) ويجهّزه للتثبيت.   يضمن هذا النظام توزيعًا **مصادقًا عليه ومقاومًا للعبث**، و**متعدد القنوات** للإصدارات الرسمية.

اعتبارًا من I2P 2.10.0، يستخدم نظام التحديث: - تواقيع **RSA-4096 / SHA-512** - **تنسيق حاوية SU3** (بديلاً عن SUD/SU2 القديمة) - **مرايا احتياطية:** HTTP داخل الشبكة، HTTPS على clearnet (الإنترنت العام)، وBitTorrent

---

## 1. موجز الأخبار

Routers تتحقق من موجز Atom الموقّع كل بضع ساعات لاكتشاف الإصدارات الجديدة والتنبيهات الأمنية.   يتم توقيع الموجز وتوزيعه كملف `.su3`، والذي قد يتضمن:

- `<i2p:version>` — رقم الإصدار الجديد  
- `<i2p:minVersion>` — أدنى إصدار مدعوم من router  
- `<i2p:minJavaVersion>` — الحد الأدنى لبيئة تشغيل Java المطلوبة  
- `<i2p:update>` — يسرد عدة مرايا تنزيل (I2P، HTTPS، تورنت)  
- `<i2p:revocations>` — بيانات إبطال الشهادات  
- `<i2p:blocklist>` — قوائم حظر على مستوى الشبكة للأقران المخترقين

### توزيع الخلاصة

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Channel</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P HTTP (eepsite)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Primary update source</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Private, resilient</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet HTTPS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback mirror</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Public fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BitTorrent magnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed channel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduces mirror load</td>
    </tr>
  </tbody>
</table>
تفضّل Routers خلاصة I2P، لكنها يمكن أن تعود إلى clearnet (الإنترنت العام غير المجهول) أو التوزيع عبر التورنت إذا لزم الأمر.

---

## 2. تنسيقات الملفات

### SU3 (المعيار الحالي)

قُدِّم في الإصدار 0.9.9، وقد حلّ SU3 محلّ تنسيقي SUD وSU2 القديمين. يحتوي كل ملف على رأس، وحمولة، وتوقيع في النهاية.

**بنية الرأس** <table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">   <thead>

    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
</thead>   <tbody>

    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"I2Psu3"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Format Version</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">e.g., <code>0x000B</code> (RSA-SHA512-4096)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>512 bytes</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version String</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Certificate name</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 = router update, 3 = reseed, 4 = news feed</td>
    </tr>
</tbody> </table>

**خطوات التحقق من التوقيع** 1. حلّل الترويسة وحدّد خوارزمية التوقيع.   2. تحقّق من قيمة التجزئة والتوقيع باستخدام شهادة الموقّع المخزَّنة.   3. أكِّد أن شهادة الموقّع غير مُلغاة.   4. قارِن سلسلة الإصدار المضمّنة ببيانات التعريف الخاصة بالحمولة.

تأتي routers مع شهادات مُوقّعين موثوقين (حاليًا **zzz** و**str4d**) وترفض أي مصادر غير موقّعة أو مُلغاة.

### SU2 (عفا عليه الزمن)

- استُخدم الامتداد `.su2` مع ملفات JAR المضغوطة باستخدام Pack200 (تنسيق ضغط لحزم Java).  
- أُزيل بعد أن أعلنت Java 14 تقادم Pack200 (JEP 367).  
- عُطِّل في I2P 0.9.48+; وقد استُبدل الآن بالكامل بضغط ZIP.

### SUD (قديم)

- صيغة ZIP موقَّعة بـ DSA‑SHA1 (خوارزمية توقيع رقمية تعتمد SHA‑1) في الإصدارات المبكرة (قبل 0.9.9).  
- لا يوجد معرّف للموقّع أو رأس، مع سلامة بيانات محدودة.  
- تم استبدالها بسبب تشفير ضعيف وعدم فرض الالتزام بالإصدار.

---

## 3. سير عمل التحديث

### 3.1 التحقق من الترويسة

تقوم routers بجلب **SU3 header** فقط للتحقق من سلسلة الإصدار قبل تنزيل الملفات الكاملة. هذا يمنع إهدار عرض النطاق الترددي على المرايا المتقادمة أو الإصدارات القديمة.

### 3.2 تنزيل كامل

بعد التحقق من الترويسة، يقوم الـ router بتنزيل ملف `.su3` الكامل من: - مرايا eepsite داخل الشبكة (مفضلة)   - مرايا HTTPS على الإنترنت التقليدي (clearnet) (كخيار احتياطي)   - BitTorrent (توزيع اختياري بمساعدة الأقران)

تستخدم التنزيلات عملاء HTTP القياسيين لـ I2PTunnel، مع إعادة المحاولة، ومعالجة انتهاء المهلة، والرجوع إلى مرايا بديلة.

### 3.3 التحقق من التوقيع

يخضع كل ملف مُنزَّل لـ: - **التحقق من التوقيع:** التحقق باستخدام RSA-4096/SHA512   - **مطابقة الإصدار:** التحقق من توافق إصدار الرأس مع إصدار الحمولة   - **منع الرجوع إلى إصدار أقدم:** يضمن أن التحديث أحدث من الإصدار المثبّت

تُستبعد الملفات غير الصالحة أو غير المتطابقة على الفور.

### 3.4 التحضير للتثبيت

بعد التحقق: 1. استخرج محتويات ملف ZIP إلى دليل مؤقت   2. أزل الملفات المدرجة في `deletelist.txt`   3. استبدل المكتبات الأصلية إذا كان `lib/jbigi.jar` مضمنًا   4. انسخ شهادات الموقّع إلى `~/.i2p/certificates/`   5. انقل التحديث إلى `i2pupdate.zip` ليتم تطبيقه عند إعادة التشغيل التالية

يتم تثبيت التحديث تلقائيًا عند التشغيل التالي أو عند تفعيل خيار “تثبيت التحديث الآن” يدويًا.

---

## 4. إدارة الملفات

### deletelist.txt

قائمة نصية بالملفات المتقادمة التي يجب حذفها قبل فك حزم المحتويات الجديدة.

**القواعد:** - مسار واحد في كل سطر (مسارات نسبية فقط) - تُتجاهل الأسطر التي تبدأ بـ `#` - يُرفض استخدام `..` والمسارات المطلقة

### المكتبات الأصلية

لمنع الثنائيات الأصلية القديمة أو غير المتطابقة: - إذا كان `lib/jbigi.jar` موجود، يتم حذف ملفات `.so` أو `.dll` القديمة   - يضمن استخراج المكتبات الخاصة بالمنصة حديثا

---

## 5. إدارة الشهادات

يمكن لـ Routers تلقي **شهادات توقيع جديدة** من خلال التحديثات أو عبر عمليات الإلغاء في موجز الأخبار.

- يتم نسخ ملفات `.crt` الجديدة إلى دليل الشهادات.  
- تُحذف الشهادات الملغاة قبل عمليات التحقق المستقبلية.  
- يدعم تدوير المفاتيح دون الحاجة إلى تدخل يدوي من المستخدم.

يتم توقيع جميع التحديثات دون اتصال باستخدام **air-gapped signing systems (أنظمة توقيع معزولة هوائيًا)**.   لا يتم مطلقًا تخزين المفاتيح الخاصة على خوادم البناء.

---

## 6. إرشادات المطورين

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Topic</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Signing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use RSA-4096 (SHA-512) via <code>apps/jetty/news</code> SU3 tooling.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Policy</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P eepsite preferred, clearnet HTTPS fallback, torrent optional.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Testing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Validate updates from prior releases, across all OS platforms.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Version Enforcement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>minVersion</code> prevents incompatible upgrades.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Certificate Rotation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distribute new certs in updates and revocation lists.</td>
    </tr>
  </tbody>
</table>
ستستكشف الإصدارات القادمة دمج التواقيع ما بعد الكم (انظر Proposal 169) والبناءات القابلة لإعادة الإنتاج.

---

## 7. نظرة عامة على الأمان

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Threat</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tampering</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cryptographic signature (RSA-4096/SHA512)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Key Compromise</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Feed-based certificate revocation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Downgrade Attack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version comparison enforcement</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Hijack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verification, multiple mirrors</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback to alternate mirrors/torrents</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>MITM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS transport + signature-level integrity</td>
    </tr>
  </tbody>
</table>
---

## 8. إدارة الإصدارات

- Router: **2.10.0 (API 0.9.67)**  
- اتباع الترقيم الدلالي للإصدارات بصيغة `Major.Minor.Patch`.  
- فرض الحد الأدنى للإصدار يمنع الترقيات غير الآمنة.  
- الإصدارات المدعومة من Java: **Java 8–17**. ابتداءً من 2.11.0+ سيتطلب Java 17+.

---
