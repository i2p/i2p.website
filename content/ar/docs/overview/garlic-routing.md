---
title: "التوجيه بطريقة Garlic"
description: "فهم مصطلحات garlic routing، البنية المعمارية، والتنفيذ الحديث في I2P"
slug: "garlic-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

---

## 1. نظرة عامة

يظل **garlic routing** أحد الابتكارات الأساسية في I2P، حيث يجمع بين التشفير متعدد الطبقات وتجميع الرسائل والأنفاق أحادية الاتجاه. وعلى الرغم من تشابهه المفاهيمي مع **onion routing**، إلا أنه يوسع النموذج ليجمع رسائل مشفرة متعددة ("cloves") في مغلف واحد ("garlic")، مما يحسن الكفاءة وعدم الكشف عن الهوية.

تم صياغة مصطلح *garlic routing* من قبل [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) في [رسالة الماجستير الخاصة بـ Roger Dingledine في Free Haven](https://www.freehaven.net/papers.html) (يونيو 2000، §8.1.1). اعتمد مطورو I2P المصطلح في أوائل العقد الأول من القرن الحادي والعشرين ليعكس تحسينات التجميع ونموذج النقل أحادي الاتجاه، مما يميزه عن تصميم Tor القائم على تبديل الدوائر.

> **ملخص:** garlic routing = تشفير متعدد الطبقات + تجميع الرسائل + توصيل مجهول عبر أنفاق أحادية الاتجاه.

---

## 2. مصطلح "Garlic"

تاريخياً، تم استخدام مصطلح *garlic* في ثلاثة سياقات مختلفة داخل I2P:

1. **التشفير متعدد الطبقات** – حماية على مستوى tunnel بأسلوب onion  
2. **تجميع رسائل متعددة** – عدة "cloves" داخل "garlic message"  
3. **التشفير من طرف إلى طرف** – كان سابقاً *ElGamal/AES+SessionTags*، الآن *ECIES‑X25519‑AEAD‑Ratchet*

بينما تظل البنية المعمارية سليمة، فقد تم تحديث نظام التشفير بالكامل.

---

## 3. التشفير الطبقي

يشترك توجيه Garlic مع توجيه Onion في مبدأه الأساسي: يقوم كل router بفك تشفير طبقة واحدة فقط من التشفير، ويتعرف فقط على القفزة التالية وليس المسار الكامل.

ومع ذلك، يقوم I2P بتنفيذ **tunnels أحادية الاتجاه**، وليست دوائر ثنائية الاتجاه:

- **Outbound tunnel**: يرسل الرسائل بعيداً عن المُنشئ
- **Inbound tunnel**: ينقل الرسائل عائدة إلى المُنشئ

رحلة كاملة ذهاباً وإياباً (Alice ↔ Bob) تستخدم أربعة tunnels: outbound الخاص بـ Alice → inbound الخاص بـ Bob، ثم outbound الخاص بـ Bob → inbound الخاص بـ Alice. هذا التصميم **يقلل تعرض بيانات الارتباط إلى النصف** مقارنة بالدوائر ثنائية الاتجاه.

لمزيد من التفاصيل حول تنفيذ الأنفاق، راجع [مواصفات النفق](/docs/specs/implementation) ومواصفات [إنشاء النفق (ECIES)](/docs/specs/implementation).

---

## 4. تجميع رسائل متعددة ("القرنفل")

تصور Freedman الأصلي لـ garlic routing تضمين عدة "بصيلات" مشفرة داخل رسالة واحدة. يطبق I2P هذا على شكل **cloves** (فصوص) داخل **garlic message** (رسالة الثوم) — كل clove له تعليمات التسليم والوجهة المشفرة الخاصة به (router أو destination أو tunnel).

يتيح تجميع garlic لـ I2P:

- دمج الإقرارات والبيانات الوصفية مع رسائل البيانات
- تقليل أنماط حركة البيانات القابلة للملاحظة
- دعم هياكل الرسائل المعقدة دون اتصالات إضافية

![Garlic Message Cloves](/images/garliccloves.png)   *الشكل 1: رسالة Garlic تحتوي على عدة cloves، كل منها له تعليمات التسليم الخاصة به.*

تشمل فصوص الثوم النموذجية:

1. **رسالة حالة التسليم** — إقرارات تؤكد نجاح أو فشل التسليم.  
   يتم تغليفها في طبقة garlic خاصة بها للحفاظ على السرية.
2. **رسالة تخزين قاعدة البيانات** — LeaseSets مجمعة تلقائياً حتى يتمكن الأقران من الرد دون الاستعلام مرة أخرى من netDb.

يتم تجميع القرنفل عندما:

- يجب نشر LeaseSet جديد
- يتم تسليم علامات جلسة جديدة
- لم يحدث تجميع مؤخراً (حوالي دقيقة واحدة افتراضياً)

تحقق رسائل garlic توصيلاً فعالاً من طرف إلى طرف لمكونات مشفرة متعددة في حزمة واحدة.

---

## 5. تطور التشفير

### 5.1 Historical Context

الوثائق المبكرة (الإصدار 0.9.12 أو أقدم) وصفت تشفير *ElGamal/AES+SessionTags*:   - **ElGamal 2048‑bit** لتغليف مفاتيح جلسة AES   - **AES‑256/CBC** لتشفير الحمولة   - علامات جلسة بحجم 32 بايت تُستخدم مرة واحدة لكل رسالة

هذا النظام التشفيري **مُهمل**.

### 5.2 ECIES‑X25519‑AEAD‑Ratchet (Current Standard)

بين عامي 2019 و2023، انتقلت I2P بالكامل إلى ECIES‑X25519‑AEAD‑Ratchet. يقوم المكدس الحديث بتوحيد المكونات التالية:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ECIES Primitive or Concept</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport Layer (NTCP2, SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise_NX → X25519, ChaCha20/Poly1305, BLAKE2s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2NP Delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES‑X25519‑AEAD (ChaCha20/Poly1305)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Management</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ratchet with rekey records, per-clove key material</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline Authentication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA (Ed25519) with LeaseSet2/MetaLeaseSet chains</td>
    </tr>
  </tbody>
</table>
فوائد الانتقال إلى ECIES:

- **السرية الأمامية** عبر مفاتيح ratcheting لكل رسالة  
- **حجم حمولة مُخفّض** مقارنة بـ ElGamal  
- **المرونة** ضد التقدمات في التحليل التشفيري  
- **التوافق** مع الهجينات المستقبلية لما بعد الكم (انظر الاقتراح 169)

تفاصيل إضافية: راجع [مواصفات ECIES](/docs/specs/ecies) و[مواصفات EncryptedLeaseSet](/docs/specs/encryptedleaseset).

---

## 6. LeaseSets and Garlic Bundling

تتضمن مغلفات garlic في كثير من الأحيان LeaseSets لنشر أو تحديث إمكانية الوصول إلى الوجهة.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Capabilities</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Distribution Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet (legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single encryption/signature pair</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Accepted for backward compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple crypto suites, offline signing keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for modern routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EncryptedLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Access-controlled, destination hidden from floodfill</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires shared decryption key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MetaLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Aggregates multiple destinations or multi-homed services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Extends LeaseSet2 fields recursively</td>
    </tr>
  </tbody>
</table>
يتم توزيع جميع مجموعات الإيجار (LeaseSets) عبر *floodfill DHT* الذي تحتفظ به أجهزة التوجيه المتخصصة. يتم التحقق من المنشورات وختمها بطابع زمني وتحديد معدلها لتقليل الربط بين البيانات الوصفية.

راجع [وثائق قاعدة بيانات الشبكة](/docs/specs/common-structures) للحصول على التفاصيل.

---

## 7. Modern “Garlic” Applications within I2P

يتم استخدام التشفير القائم على garlic وتجميع الرسائل في جميع أنحاء مكدس بروتوكول I2P:

1. **إنشاء واستخدام الأنفاق (Tunnel)** — تشفير متعدد الطبقات لكل قفزة  
2. **توصيل الرسائل من طرف إلى طرف** — رسائل garlic مجمعة مع cloves التأكيد المستنسخ وLeaseSet  
3. **نشر قاعدة بيانات الشبكة (Network Database)** — LeaseSets ملفوفة في مظاريف garlic للخصوصية  
4. **بروتوكولات النقل SSU2 وNTCP2** — تشفير الطبقة الأساسية باستخدام إطار عمل Noise وعمليات X25519/ChaCha20 الأولية

التوجيه garlic هو بالتالي كل من *طريقة لطبقات التشفير* و *نموذج لمراسلة الشبكة*.

---

## 6. LeaseSets وتجميع Garlic

مركز توثيق I2P [متاح هنا](/docs/)، ويتم صيانته بشكل مستمر. المواصفات الحية ذات الصلة تشمل:

- [مواصفات ECIES](/docs/specs/ecies) — ECIES‑X25519‑AEAD‑Ratchet
- [إنشاء Tunnel (ECIES)](/docs/specs/implementation) — بروتوكول بناء tunnel الحديث
- [مواصفات I2NP](/docs/specs/i2np) — تنسيقات رسائل I2NP
- [مواصفات SSU2](/docs/specs/ssu2) — بروتوكول نقل SSU2 UDP
- [البنى المشتركة](/docs/specs/common-structures) — سلوك netDb و floodfill

التحقق الأكاديمي: أكد Hoang وآخرون (IMC 2018، USENIX FOCI 2019) و Muntaka وآخرون (2025) الاستقرار المعماري والمرونة التشغيلية لتصميم I2P.

---

## 7. تطبيقات "Garlic" الحديثة ضمن I2P

المقترحات الجارية:

- **المقترح 169:** هجين ما بعد الكم (ML-KEM 512/768/1024 + X25519)  
- **المقترح 168:** تحسين عرض النطاق الترددي للنقل  
- **تحديثات Datagram والبث المباشر:** إدارة محسّنة للازدحام

قد تشمل التعديلات المستقبلية استراتيجيات إضافية لتأخير الرسائل أو التكرار متعدد الأنفاق على مستوى رسائل garlic، بالاستناد إلى خيارات التسليم غير المستخدمة التي وصفها فريدمان أصلاً.

---

## 8. الوثائق والمراجع الحالية

- Freedman, M. J. & Dingledine, R. (2000). *Free Haven Master's Thesis,* § 8.1.1. [Free Haven Papers](https://www.freehaven.net/papers.html)  
- [Onion Router Publications](https://www.onion-router.net/Publications.html)  
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)  
- [Tor Project](https://www.torproject.org/)  
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)  
- Goldschlag, D. M., Reed, M. G., Syverson, P. F. (1996). *Hiding Routing Information.* NRL Publication.

---
