---
title: "تشفير ElGamal/AES + SessionTag (وسم الجلسة)"
description: "تشفير طرف-إلى-طرف متقادم يجمع بين ElGamal وAES وSHA-256 ووسوم جلسة أحادية الاستخدام"
slug: "elgamal-aes"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **الحالة:** يصف هذا المستند بروتوكول التشفير ElGamal/AES+SessionTag (مخطط تشفير يجمع بين ElGamal وAES مع SessionTag). لا يزال مدعوماً لأغراض التوافق العكسي فقط، لأن إصدارات I2P الحديثة (2.10.0+) تستخدم [ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/) (مخطط تشفير قائم على ECIES وX25519 مع AEAD وRatchet لتدوير المفاتيح). يُعد بروتوكول ElGamal مُهملًا ويُحتفَظ به حصراً لأغراض تاريخية وللتشغيل البيني.

## نظرة عامة

قدّمت ElGamal/AES+SessionTag الآلية الأصلية للتشفير من الطرف إلى الطرف في I2P لرسائل garlic (نمط رسائل مُجمَّعة في I2P). لقد جمعت بين:

- **ElGamal (2048-بت)** — لتبادل المفاتيح
- **AES-256/CBC** — لتشفير بيانات الحمولة
- **SHA-256** — للتجزئة واشتقاق متجه التهيئة (IV)
- **Session Tags (وسوم الجلسة، 32 بايت)** — لمعرّفات الرسائل لمرة واحدة

أتاح البروتوكول لـ routers والوجهات التواصل بأمان دون الحفاظ على اتصالات مستمرة. كانت كل جلسة تستخدم تبادل ElGamal غير متناظرًا لإنشاء مفتاح AES متناظر، تلاه إرسال رسائل "موسومة" خفيفة تُشير إلى تلك الجلسة.

## آلية عمل البروتوكول

### إنشاء جلسة (جلسة جديدة)

بدأت جلسة جديدة برسالة تتضمن قسمين:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Section</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>ElGamal-encrypted block</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">514 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">222 bytes of plaintext encrypted using the recipient's ElGamal public key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Establishes the AES session key and IV seed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>AES-encrypted block</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable (≥128 bytes typical)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload data, integrity hash, and session tags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Carries the actual message and new tags</td>
    </tr>
  </tbody>
</table>
كان النصّ الصريح داخل كتلة ElGamal (خوارزمية تشفير بالمفتاح العام) يتكوّن من:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 key for the session</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Pre-IV</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Material for deriving the AES initialization vector (<code>IV = first 16 bytes of SHA-256(Pre-IV)</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">158 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Filler to reach required ElGamal plaintext length</td>
    </tr>
  </tbody>
</table>
### رسائل الجلسة القائمة

بمجرد إنشاء جلسة، كان بإمكان المرسل إرسال رسائل **existing-session** (جلسة قائمة) باستخدام علامات جلسة مخزنة مؤقتاً:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Tag</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single-use identifier tied to the existing session key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-Encrypted Block</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted payload and metadata using the established AES key</td>
    </tr>
  </tbody>
</table>
Routers خزّنت مؤقتًا الوسوم التي تم تسليمها لمدة نحو **15 دقيقة**، وبعد ذلك انتهت صلاحية الوسوم غير المستخدمة. كان كل وسم صالحًا لرسالة واحدة بالضبط لمنع هجمات الارتباط.

### تنسيق الكتلة المشفرة بـ AES

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tag Count</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Number (0–200) of new session tags included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Tags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 × N bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Newly generated single-use tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload Size</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Length of the payload in bytes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SHA-256 digest of the payload</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Flag</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 byte</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0x00</code> normal, <code>0x01</code> = new session key follows (unused)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">New Session Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replacement AES key (rarely used)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted message data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable (16-byte aligned)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding to block boundary</td>
    </tr>
  </tbody>
</table>
تقوم Routers بفك التشفير باستخدام مفتاح الجلسة و IV (متجه التهيئة) المشتقين إما من Pre-IV (للجلسات الجديدة) أو من وسم الجلسة (للجلسات الحالية). بعد فك التشفير، تتحقق من السلامة عبر إعادة احتساب تجزئة SHA-256 لحمولة النص الصريح.

## إدارة وسوم الجلسة

- العلامات **أحادية الاتجاه**: لا يمكن إعادة استخدام علامات Alice → Bob في اتجاه Bob → Alice.
- تنتهي صلاحية العلامات بعد حوالي **15 دقيقة**.
- Routers تحتفظ بـ **مديري مفاتيح الجلسة** لكل وجهة لتتبّع العلامات والمفاتيح وأوقات الانتهاء.
- يمكن للتطبيقات التحكم في سلوك العلامات عبر [خيارات I2CP](/docs/specs/i2cp/):
  - **`i2cp.tagThreshold`** — الحد الأدنى من العلامات المخزّنة مؤقتًا قبل إعادة التزويد
  - **`i2cp.tagCount`** — عدد العلامات الجديدة لكل رسالة

قلّلت هذه الآلية المصافحات المكلفة لـ ElGamal إلى الحد الأدنى، مع الحفاظ على عدم قابلية الربط بين الرسائل.

## التكوين والكفاءة

تم تقديم وسوم الجلسة لتحسين الكفاءة عبر النقل عالي التأخير وغير المرتَّب الخاص بـ I2P. كان التكوين المعتاد يقدّم **40 وسمًا لكل رسالة**، مضيفًا نحو 1.2 KB من الحمولة الإضافية. كان بإمكان التطبيقات ضبط سلوك التسليم بناءً على حركة المرور المتوقعة:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Tags</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Short-lived requests (HTTP, datagrams)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0 – 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low overhead, may trigger ElGamal fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent streams or bulk transfer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20 – 50</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Higher bandwidth use, avoids session re-establishment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Long-term services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">50+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures steady tag supply despite loss or delay</td>
    </tr>
  </tbody>
</table>
تقوم Routers بشكل دوري بحذف الوسوم المنتهية الصلاحية وإزالة حالة الجلسة غير المستخدمة لتقليل استخدام الذاكرة والتخفيف من هجمات إغراق الوسوم.

## القيود

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Limitation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Performance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">514-byte ElGamal block adds heavy overhead for new sessions; session tags consume 32 bytes each.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Security</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No forward secrecy – compromise of ElGamal private key exposes past sessions.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Integrity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-CBC requires manual hash verification; no AEAD.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Quantum Resistance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Vulnerable to Shor's algorithm – will not survive quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Complexity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires stateful tag management and careful timeout tuning.</td>
    </tr>
  </tbody>
</table>
دفعت هذه أوجه القصور مباشرة إلى تصميم بروتوكول [ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/)، الذي يوفر سرية أمامية تامة، وتشفيرًا موثقًا بالمصادقة، وتبادلًا فعالًا للمفاتيح.

## حالة الإهمال والترحيل

- **تم تقديمه:** الإصدارات المبكرة من I2P (قبل 0.6)
- **تم إهماله:** مع إدخال ECIES-X25519 (مخطط التشفير ECIES مع X25519) (0.9.46 → 0.9.48)
- **تمت إزالته:** لم يعد الإعداد الافتراضي اعتبارًا من 2.4.0 (ديسمبر 2023)
- **مدعوم:** للتوافق مع الإصدارات القديمة فقط

تعلن routers الحديثة والوجهات الآن عن **نوع التشفير 4 (ECIES-X25519)** بدلاً من **النوع 0 (ElGamal/AES)**. يظل البروتوكول القديم معترفاً به لأغراض قابلية التشغيل البيني مع الأقران غير المُحدَّثين، لكنه لا ينبغي أن يُستخدم في عمليات النشر الجديدة.

## السياق التاريخي

كان ElGamal/AES+SessionTag (SessionTag: وسم جلسة يُستخدم لمرة واحدة) حجر الأساس للبنية التشفيرية المبكرة لـ I2P. قدّم تصميمه الهجين ابتكارات مثل وسوم الجلسات التي تُستخدم لمرة واحدة والجلسات أحادية الاتجاه التي أثّرت في البروتوكولات اللاحقة. وتطوّر كثير من هذه الأفكار إلى بنى حديثة مثل deterministic ratchets (آليات تدوير مفاتيح حتمية) و hybrid post-quantum key exchanges (تبادلات مفاتيح هجينة لما بعد الكم).
