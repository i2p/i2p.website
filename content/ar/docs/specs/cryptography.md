---
title: "التشفير منخفض المستوى"
description: "ملخص للبدائيات التماثلية وغير التماثلية وبدائيات التوقيع المستخدمة عبر I2P"
slug: "cryptography"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **الحالة:** تلخّص هذه الصفحة "مواصفة التشفير منخفض المستوى" القديمة. لقد أكملت إصدارات I2P الحديثة (2.10.0، أكتوبر 2025) الانتقال إلى بدائيات تشفير جديدة. استخدم المواصفات المتخصصة مثل [ECIES](/docs/specs/ecies/) (نظام تشفير متكامل قائم على المنحنيات الإهليلجية)، [Encrypted LeaseSets](/docs/specs/encryptedleaseset/)، [NTCP2](/docs/specs/ntcp2/)، [Red25519](/docs/specs/red25519-signature-scheme/)، [SSU2](/docs/specs/ssu2/)، و[Tunnel Creation (ECIES)](/docs/specs/implementation/) للحصول على تفاصيل التنفيذ.

## لقطة للتطور

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Functional Area</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Legacy Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current / Planned Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Migration Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport key exchange</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Diffie–Hellman over 2048-bit prime (NTCP / SSU)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 (NTCP2 / SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (NTCP2 and SSU2 fully deployed)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">End-to-end encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (2.4.0+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Symmetric cipher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256/CBC + HMAC-MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305 (AEAD)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Active (tunnel layer remains AES-256)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA-SHA1 (1024-bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA/RedDSA on Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fully migrated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental / future</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hybrid post-quantum encryption (opt-in)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">In testing (2.10.0)</td>
    </tr>
  </tbody>
  
</table>
## التشفير غير المتماثل

### X25519 (خوارزمية تبادل مفاتيح باستخدام المنحنى البيضي Curve25519)

- تُستخدم لـ NTCP2 و ECIES-X25519-AEAD-Ratchet و SSU2، ولإنشاء tunnel معتمد على X25519.  
- يوفّر مفاتيح صغيرة الحجم، وعمليات بزمن ثابت، وسرية أمامية عبر Noise protocol framework (إطار عمل بروتوكول Noise).  
- يوفّر أمانًا بمستوى 128-بت مع مفاتيح بحجم 32 بايت وتبادل مفاتيح فعّال.

### ElGamal (قديم)

- تم الإبقاء عليه للتوافق مع الإصدارات الأقدم من routers.  
- يعمل على العدد الأوّلي لمجموعة Oakley رقم 14 بطول 2048 بت (RFC 3526) مع المولِّد 2.  
- يشفّر مفاتيح جلسة AES إضافةً إلى IVs (متجهات التهيئة) ضمن نصوص مشفّرة بحجم 514 بايت.  
- يفتقر إلى التشفير الموثّق والسرية الأمامية؛ وقد انتقلت جميع نقاط النهاية الحديثة إلى ECIES.

## التشفير المتماثل

### ChaCha20/Poly1305 (خوارزمية AEAD للتشفير المصادق تجمع بين تشفير التدفق ChaCha20 ودالة مصادقة الرسائل Poly1305)

- البدائية الافتراضية للتشفير الموثَّق عبر NTCP2 وSSU2 وECIES.  
- توفّر أمان AEAD وأداءً عاليًا من دون دعم عتادي لـ AES.  
- مُنفّذة وفق RFC 7539 (مفتاح 256‑بت، nonce (رقم وحيد الاستخدام) بطول 96‑بت، ووسم 128‑بت).

### AES‑256/CBC (قديم)

- لا يزال مستخدماً لتشفير طبقة tunnel، حيث إن بنيته كخوارزمية تشفير كتليّة تلائم نموذج التشفير الطبقي الخاص بـ I2P.  
- يستخدم حشو PKCS#5 وتحويلات IV (متجه التهيئة) لكل قفزة.  
- مُجدول لمراجعة طويلة الأمد لكنه لا يزال متيناً من الناحية التشفيرية.

## التواقيع

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signature Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage Notes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA‑SHA1 (1024‑bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Original default; still accepted for legacy Destinations.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA‑SHA256/384/512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used during 2014–2015 transition.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for Router and Destination identities (since 0.9.15).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used for encrypted LeaseSet signatures (0.9.39+).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Specialized</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA‑SHA512‑4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For out‑of‑band signing (su3 updates, reseeds, plugins).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Application‑layer</td>
    </tr>
  </tbody>
</table>
## التجزئة واشتقاق المفاتيح

- **SHA‑256:** تُستخدم لمفاتيح DHT (جدول التجزئة الموزّع)، وHKDF (دالة اشتقاق المفاتيح المعتمدة على HMAC)، والتواقيع القديمة.  
- **SHA‑512:** تُستخدم من قِبل EdDSA (خوارزمية التوقيع الرقمي للمنحنيات الإهليلجية)/RedDSA، وفي اشتقاقات HKDF ضمن Noise (إطار عمل بروتوكولات Noise).  
- **HKDF‑SHA256:** تشتق مفاتيح الجلسة في ECIES (مخطط التشفير المتكامل بالمنحنيات الإهليلجية)، وNTCP2، وSSU2.  
- اشتقاقات SHA‑256 ذات التدوير اليومي تؤمّن مواقع تخزين RouterInfo وLeaseSet في netDb.

## ملخص طبقة النقل

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Exchange</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Authentication</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU (Legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DH‑2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES‑256/CBC + HMAC‑MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed (2.4.0)</td>
    </tr>
  </tbody>
</table>
كلا الناقلين يوفّران سرية أمامية على مستوى الوصلة وحماية من إعادة التشغيل، باستخدام نمط المصافحة Noise_XK (نمط ضمن إطار عمل Noise).

## تشفير طبقة Tunnel

- يواصل استخدام AES‑256/CBC للتشفير متعدد الطبقات على مستوى كل قفزة.  
- تقوم البوابات الصادرة بإجراء فك تشفير AES بشكل تكراري؛ وتعيد كل قفزة التشفير باستخدام مفتاح الطبقة ومفتاح IV (المتجه الابتدائي) الخاصين بها.  
- يخفف التشفير بـ IV مزدوج من هجمات الترابط والتأكيد.  
- الانتقال إلى AEAD (تشفير مصادق مع بيانات مرتبطة) قيد الدراسة، لكنه غير مخطط له حالياً.

## التشفير ما بعد الكمّي

- I2P 2.10.0 يقدم **تشفيراً هجيناً تجريبياً لما بعد الكم**.  
- يتم تمكينه يدوياً عبر Hidden Service Manager (مدير الخدمات المخفية) لأغراض الاختبار.  
- يجمع بين X25519 وKEM المقاوم للكم (آلية تغليف المفاتيح) (الوضع الهجين).
- غير مُفعل افتراضياً؛ مُخصص للبحث وتقييم الأداء.

## إطار قابلية التوسعة

- تُتيح *مُعرِّفات الأنواع* للتشفير والتوقيع دعماً متوازياً لعدة بدائيات تشفيرية.  
- تشمل التعيينات الحالية:  
  - **أنواع التشفير:** 0 = ElGamal/AES+SessionTags, 4 = ECIES‑X25519‑AEAD‑Ratchet.  
  - **أنواع التوقيع:** 0 = DSA‑SHA1, 7 = EdDSA‑SHA512‑Ed25519, 11 = RedDSA‑SHA512‑Ed25519.  
- يتيح هذا الإطار ترقيات مستقبلية، بما في ذلك مخططات ما بعد الكم، دون انقسامات في الشبكة.

## التركيب التشفيري

- **طبقة النقل:** X25519 + ChaCha20/Poly1305 (إطار Noise).  
- **طبقة Tunnel:** تشفير متعدد الطبقات AES‑256/CBC لإخفاء الهوية.  
- **من طرف إلى طرف:** ECIES‑X25519‑AEAD‑Ratchet للحفاظ على السرية ولتحقيق السرية المستقبلية (forward secrecy).  
- **طبقة قاعدة البيانات:** تواقيع EdDSA/RedDSA لضمان الأصالة.

تتضافر هذه الطبقات لتوفير الدفاع في العمق: حتى إذا اختُرقت طبقة واحدة، فإن الطبقات الأخرى تحافظ على السرية وعدم إمكانية الربط.

## ملخص

يتمحور المكدس التشفيري الخاص بـ I2P 2.10.0 حول:

- **Curve25519 (X25519)** لتبادل المفاتيح  
- **ChaCha20/Poly1305** للتشفير المتماثل  
- **EdDSA / RedDSA** للتواقيع  
- **SHA‑256 / SHA‑512** للتجزئة والاشتقاق  
- **أوضاع هجينة تجريبية لما بعد الكمّ** للتوافقية المستقبلية

لا تزال ElGamal وAES‑CBC وDSA القديمة موجودة لأغراض التوافق مع الإصدارات السابقة، لكنها لم تعد تُستخدم في وسائط النقل النشطة أو مسارات التشفير.
