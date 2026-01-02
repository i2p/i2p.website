---
title: "نموذج التهديدات في I2P"
description: "كتالوج الهجمات المأخوذة بالاعتبار في تصميم I2P والتدابير الوقائية المطبقة"
slug: "threat-model"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## 1. ما معنى "مجهول الهوية"

يوفر I2P *عدم الكشف عن الهوية العملي*—وليس الخفاء التام. يُعرّف عدم الكشف عن الهوية بأنه صعوبة قيام خصم بمعرفة المعلومات التي ترغب في الحفاظ على خصوصيتها: من أنت، وأين أنت، أو مع من تتحدث. عدم الكشف عن الهوية المطلق مستحيل؛ بدلاً من ذلك، يهدف I2P إلى تحقيق **عدم كشف كافٍ عن الهوية** في مواجهة الخصوم السلبيين والنشطين على المستوى العالمي.

تعتمد خصوصيتك على كيفية تكوين I2P، وكيفية اختيار الأقران والاشتراكات، وما هي التطبيقات التي تعرضها.

---

## 2. التطور التشفيري وتطور النقل (2003 ← 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Era</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Algorithms</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.3 – 0.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES-256 + DSA-SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy stack (2003–2015)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced DSA</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36 (2018)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong> introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise <em>XK_25519_ChaChaPoly_SHA256</em></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56 (2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong> enabled by default</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0 (2023)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Sub-DB isolation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents router↔client linkage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.8.0+ (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing / observability reductions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DoS hardening</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0 (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid ML-KEM support (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
    </tr>
  </tbody>
</table>
**المجموعة التشفيرية الحالية (Noise XK):** - **X25519** لتبادل المفاتيح   - **ChaCha20/Poly1305 AEAD** للتشفير   - **Ed25519 (EdDSA-SHA512)** للتوقيعات   - **SHA-256** للتجزئة و HKDF   - اختياري **ML-KEM hybrids** للاختبار ما بعد الكمي

تم إيقاف جميع استخدامات ElGamal و AES-CBC. النقل بالكامل عبر NTCP2 (TCP) و SSU2 (UDP)؛ كلاهما يدعم IPv4/IPv6، السرية الأمامية (forward secrecy)، وإخفاء فحص الحزم العميق (DPI obfuscation).

---

## 3. ملخص بنية الشبكة

- **شبكة مزج حرة التوجيه:** يحدد المرسلون والمستقبلون أنفاقهم الخاصة.  
- **لا توجد سلطة مركزية:** التوجيه والتسمية لا مركزيان؛ كل router يحتفظ بالثقة المحلية.  
- **أنفاق أحادية الاتجاه:** الوارد والصادر منفصلان (مدة حياة 10 دقائق).  
- **أنفاق استكشافية:** قفزتان بشكل افتراضي؛ أنفاق العملاء 2-3 قفزات.  
- **موجهات Floodfill:** حوالي 1,700 من أصل 55,000 عقدة (~6%) تحتفظ بـ NetDB الموزعة.  
- **تدوير NetDB:** تدور مساحة المفاتيح يوميًا عند منتصف الليل بتوقيت UTC.  
- **عزل قواعد البيانات الفرعية:** منذ الإصدار 2.4.0، يستخدم كل عميل وrouter قواعد بيانات منفصلة لمنع الربط.

---

## 4. فئات الهجمات والدفاعات الحالية

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current Status (2025)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Defenses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Brute Force / Cryptanalysis</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Impractical with modern primitives (X25519, ChaCha20).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Strong crypto, key rotation, Noise handshakes.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Timing Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Still unsolved for low-latency systems.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unidirectional tunnels, 1024&nbsp;B cells, profile recalc (45&nbsp;s). Research continues for non-trivial delays (3.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Intersection Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inherent weakness of low latency mixnets.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel rotation (10&nbsp;min), leaseset expirations, multihoming.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Predecessor Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partially mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tiered peer selection, strict XOR ordering, variable length tunnels.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Sybil Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No comprehensive defense.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IP /16 limits, profiling, diversity rules; HashCash infra exists but not required.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Floodfill / NetDB Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved but still a concern.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">One /16 per lookup, limit 500 active, daily rotation, randomized verification delay, Sub-DB isolation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS / Flooding</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Frequent (esp. 2023 incidents).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing (2.4+), aggressive leaseset removal (2.8+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Traffic ID / Fingerprinting</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Greatly reduced.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise obfuscation, random padding, no plaintext headers.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Censorship / Partitioning</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Possible with state-level blocking.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden mode, IPv6, multiple reseeds, mirrors.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Development / Supply Chain</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source, signed SU3 releases (RSA-4096), multi-signer trust model.</td>
    </tr>
  </tbody>
</table>
---

## 5. قاعدة بيانات الشبكة الحديثة (NetDB)

**الحقائق الأساسية (لا تزال دقيقة):** - قاعدة بيانات Kademlia المعدلة تخزن RouterInfo و LeaseSets.   - تجزئة المفاتيح باستخدام SHA-256؛ استعلامات متوازية إلى أقرب 2 floodfills مع مهلة 10 ثواني.   - عمر LeaseSet ≈ 10 دقائق (LeaseSet2) أو 18 ساعة (MetaLeaseSet).

**أنواع جديدة (منذ 0.9.38):** - **LeaseSet2 (النوع 3)** – أنواع تشفير متعددة، مع طابع زمني.   - **EncryptedLeaseSet2 (النوع 5)** – وجهة مخفية (blinded destination) للخدمات الخاصة (مصادقة DH أو PSK).   - **MetaLeaseSet (النوع 7)** – استضافة متعددة (multihoming) وفترات انتهاء صلاحية ممتدة.

**ترقية أمنية رئيسية – عزل قاعدة البيانات الفرعية (2.4.0):** - يمنع الربط بين router↔العميل.   - كل عميل وrouter يستخدمان أجزاء netDb منفصلة.   - تم التحقق والمراجعة (2.5.0).

---

## 6. الوضع المخفي والمسارات المقيدة

- **الوضع المخفي:** مُنفّذ (تلقائي في الدول المقيدة وفقاً لتقييمات Freedom House).  
    أجهزة الـ router لا تنشر RouterInfo ولا توجّه حركة المرور.  
- **المسارات المقيدة:** منفّذ جزئياً (أنفاق موثوقة أساسية فقط).  
    التوجيه الشامل عبر نظراء موثوقين لا يزال مخططاً له (3.0+).

المقايضة: خصوصية أفضل ↔ مساهمة أقل في سعة الشبكة.

---

## 7. هجمات حجب الخدمة وFloodfill

**تاريخياً:** أظهرت أبحاث UCSB لعام 2013 إمكانية السيطرة على Eclipse وFloodfill. **تشمل الدفاعات الحديثة:** - تدوير يومي لمساحة المفاتيح. - حد Floodfill ≈ 500، واحد لكل /16. - تأخيرات عشوائية للتحقق من التخزين. - تفضيل أجهزة التوجيه الأحدث (2.6.0). - إصلاح التسجيل التلقائي (2.9.0). - توجيه مدرك للازدحام وتقييد الإيجار (2.4.0+).

هجمات floodfill تبقى ممكنة نظريًا ولكن أصعب عمليًا.

---

## 8. تحليل حركة المرور والرقابة

من الصعب تحديد حركة مرور I2P: لا يوجد منفذ ثابت، ولا مصافحة بنص واضح، وحشو عشوائي. حزم NTCP2 وSSU2 تحاكي البروتوكولات الشائعة وتستخدم إخفاء رأس ChaCha20. استراتيجيات الحشو أساسية (أحجام عشوائية)، حركة المرور الوهمية غير مطبقة (مكلفة). الاتصالات من عقد خروج Tor محظورة منذ الإصدار 2.6.0 (لحماية الموارد).

---

## 9. القيود المستمرة (المعترف بها)

- ارتباط التوقيت للتطبيقات منخفضة الكمون يبقى خطرًا أساسيًا.
- هجمات التقاطع لا تزال قوية ضد الوجهات العامة المعروفة.
- هجمات Sybil تفتقر إلى دفاع كامل (HashCash غير مفعّل).
- حركة المرور ذات المعدل الثابت والتأخيرات غير التافهة تبقى غير منفذة (مخطط لها في 3.0).

الشفافية حول هذه القيود متعمدة — فهي تمنع المستخدمين من المبالغة في تقدير إخفاء الهوية.

---

## 10. إحصائيات الشبكة (2025)

- ~55,000 router نشط حول العالم (↑ من 7,000 في 2013)
- ~1,700 floodfill router (~6%)
- 95% يشاركون في توجيه tunnel افتراضياً
- مستويات عرض النطاق الترددي: K (<12 كيلوبايت/ثانية) → X (>2 ميجابايت/ثانية)
- الحد الأدنى لمعدل floodfill: 128 كيلوبايت/ثانية
- وحدة تحكم router تتطلب Java 8+، مخطط Java 17+ في الدورة القادمة

---

## 11. التطوير والموارد المركزية

- الموقع الرسمي: [geti2p.net](/)
- الوثائق: [Documentation](/docs/)  
- مستودع Debian: <https://deb.i2pgit.org> ( استبدل deb.i2p2.de في أكتوبر 2023 )  
- الكود المصدري: <https://i2pgit.org/I2P_Developers/i2p.i2p> (Gitea) + نسخة مرآة على GitHub  
- جميع الإصدارات موقعة بحاويات SU3 (RSA-4096، مفاتيح zzz/str4d)  
- لا توجد قوائم بريدية نشطة؛ المجتمع عبر <https://i2pforum.net> و IRC2P.  
- دورة التحديث: إصدارات مستقرة كل 6–8 أسابيع.

---

## 12. ملخص تحسينات الأمان منذ الإصدار 0.8.x

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Effect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed SHA1/DSA weakness</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2018</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2019</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2 / EncryptedLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden services privacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sub-DB Isolation + Congestion-Aware Routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stopped NetDB linkage / improved resilience</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill selection improvements</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced long-term node influence</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Observability reductions + PQ hybrid crypto</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Harder timing analysis / future-proofing</td>
    </tr>
  </tbody>
</table>
---

## 13. العمل المعروف غير المحلول أو المخطط له

- مسارات مقيدة شاملة (trusted-peer routing) ← مخطط لها في 3.0.
- تأخير/تجميع غير تافه لمقاومة التوقيت ← مخطط له في 3.0.
- حشو متقدم وحركة مرور وهمية ← غير مُنفذ.
- التحقق من الهوية باستخدام HashCash ← البنية التحتية موجودة لكنها غير نشطة.
- استبدال R5N DHT ← اقتراح فقط.

---

## 14. المراجع الرئيسية

- *Practical Attacks Against the I2P Network* (Egger et al., RAID 2013)  
- *Privacy Implications of Performance-Based Peer Selection* (Herrmann & Grothoff, PETS 2011)  
- *Resilience of the Invisible Internet Project* (Muntaka et al., Wiley 2025)  
- [وثائق I2P الرسمية](/docs/)

---

## 15. الخاتمة

نموذج إخفاء الهوية الأساسي في I2P صمد لعقدين من الزمن: التضحية بالتفرد العالمي مقابل الثقة المحلية والأمان. من ElGamal إلى X25519، ومن NTCP إلى NTCP2، ومن إعادة التهيئة اليدوية إلى عزل Sub-DB، تطور المشروع مع الحفاظ على فلسفته في الدفاع المتعمق والشفافية.

تبقى العديد من الهجمات ممكنة نظريًا ضد أي mixnet منخفض التأخير، لكن التحصين المستمر لـ I2P يجعلها غير عملية بشكل متزايد. الشبكة أكبر وأسرع وأكثر أمانًا من أي وقت مضى — ومع ذلك لا تزال صادقة بشأن حدودها.
