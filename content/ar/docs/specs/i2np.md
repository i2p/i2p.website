---
title: "بروتوكول شبكة I2P (I2NP)"
description: "تنسيقات الرسائل وأولوياتها وحدود أحجامها بين Router وRouter داخل I2P."
slug: "i2np"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## نظرة عامة

يحدد بروتوكول شبكة I2P (I2NP) كيف تقوم routers بتبادل الرسائل، واختيار بروتوكولات النقل، ومزج حركة المرور مع الحفاظ على إخفاء الهوية. يعمل بين **I2CP** (واجهة برمجة تطبيقات العميل) وبروتوكولات النقل (**NTCP2** و**SSU2**).

I2NP (بروتوكول شبكة I2P) هو الطبقة الواقعة فوق بروتوكولات النقل الخاصة بـ I2P. إنه بروتوكول من router (الموجّه) إلى router يُستخدم من أجل: - عمليات البحث في قاعدة بيانات الشبكة والردود - إنشاء tunnels (أنفاق) - رسائل بيانات router والعميل المشفّرة

قد تُرسَل رسائل I2NP من نقطة إلى نقطة إلى router آخر، أو تُرسَل بشكلٍ مجهول عبر tunnels إلى ذلك router.

Routers تضع الأعمال الصادرة في طابور باستخدام أولويات محلية. تُعالَج الأرقام ذات الأولوية الأعلى أولاً. يُعامَل أي شيء أعلى من أولوية بيانات tunnel القياسية (400) على أنه عاجل.

### بروتوكولات النقل الحالية

يستخدم I2P الآن **NTCP2** (TCP) و**SSU2** (UDP) لكل من IPv4 وIPv6. يستخدم كلا بروتوكولي النقل: - **X25519** لتبادل المفاتيح (Noise protocol framework، إطار عمل بروتوكول Noise) - **ChaCha20/Poly1305** للتشفير المصادق عليه (AEAD) - **SHA-256** للتجزئة

**تمت إزالة بروتوكولات النقل القديمة:** - تمت إزالة NTCP (TCP الأصلي) من Java router في الإصدار 0.9.50 (مايو 2021) - تمت إزالة SSU v1 (UDP الأصلي) من Java router في الإصدار 2.4.0 (ديسمبر 2023) - تمت إزالة SSU v1 من i2pd في الإصدار 2.44.0 (نوفمبر 2022)

اعتبارًا من عام 2025، تكون الشبكة قد أتمّت الانتقال بالكامل إلى نواقل مبنية على Noise (إطار عمل للمصافحات التشفيرية)، من دون أي دعم للنواقل القديمة.

---

## نظام ترقيم الإصدارات

**مهم:** يستخدم I2P نظام ترقيم الإصدارات مزدوجًا يجب فهمه بوضوح:

### الإصدارات (الموجّهة للمستخدم)

هذه هي الإصدارات التي يراها المستخدمون ويقومون بتنزيلها: - 0.9.50 (مايو 2021) - آخر إصدار من سلسلة 0.9.x - **1.5.0** (أغسطس 2021) - أول إصدار من سلسلة 1.x - 1.6.0, 1.7.0, 1.8.0, 1.9.0 (خلال 2021-2022) - **2.0.0** (نوفمبر 2022) - أول إصدار من سلسلة 2.x - من 2.1.0 حتى 2.9.0 (خلال 2023-2025) - **2.10.0** (8 سبتمبر 2025) - الإصدار الحالي

### إصدارات واجهة برمجة التطبيقات (توافق البروتوكول)

هذه أرقام الإصدارات الداخلية التي تُنشر في الحقل "router.version" ضمن خصائص RouterInfo: - 0.9.50 (مايو 2021) - **0.9.51** (أغسطس 2021) - نسخة واجهة برمجة التطبيقات (API) للإصدار 1.5.0 - من 0.9.52 حتى 0.9.66 (مستمرة عبر إصدارات 2.x) - **0.9.67** (سبتمبر 2025) - نسخة API للإصدار 2.10.0

**نقطة أساسية:** لم تكن هناك أي إصدارات مرقّمة من 0.9.51 وحتى 0.9.67. هذه الأرقام موجودة فقط كمُعرِّفات لإصدارات API (واجهة برمجة التطبيقات). قفز I2P من الإصدار 0.9.50 مباشرةً إلى 1.5.0.

### جدول تعيين الإصدارات

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Release Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Last 0.9.x release, removed NTCP1</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages (218 bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.52</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.53</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance enhancements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.54</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 introduced</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.56</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.1.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.57</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Stability improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.2.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ElGamal routers deprecated</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.61</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">December 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Removed SSU1 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.62</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.63</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network optimizations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.64</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">October 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum preparation work</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel bandwidth parameters</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (beta)</td>
    </tr>
  </tbody>
</table>
**قريبًا:** إصدار 2.11.0 (مخطط له في ديسمبر 2025) سيتطلب Java 17+ ويفعّل التشفير ما بعد الكم افتراضيًا.

---

## إصدارات البروتوكول

يجب على جميع routers نشر إصدار بروتوكول I2NP الخاص بهم في الحقل "router.version" ضمن خصائص RouterInfo (معلومات الـ router). يمثّل هذا الحقل إصدار واجهة برمجة التطبيقات (API)، إذ يبيّن مستوى الدعم لمختلف مزايا بروتوكول I2NP، وليس بالضرورة الإصدار الفعلي للـ router.

إذا رغبت routers بديلة (غير Java) في نشر أي معلومات عن إصدار التنفيذ الفعلي للـ router، فيجب أن يتم ذلك ضمن خاصية أخرى. يُسمح بإصدارات غير تلك المدرجة أدناه. سيتم تحديد الدعم عبر مقارنة رقمية؛ على سبيل المثال، 0.9.13 يعني دعم ميزات 0.9.12.

**ملاحظة:** لم تعد الخاصية "coreVersion" تُنشر في معلومات الـ router، ولم تُستخدم مطلقًا لتحديد إصدار بروتوكول I2NP.

### ملخص ميزات إصدار واجهة برمجة التطبيقات

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Required I2NP Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (MLKEM ratchet) support (beta), UDP tracker support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 service record options (see proposal 167)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel build bandwidth parameters (see proposal 168)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.63), minimum floodfill peers will send DSM to (as of 0.9.63)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.62), <strong>ElGamal routers deprecated</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 transport support (if published in router info)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers, minimum peers will build tunnels through (as of 0.9.58), minimum floodfill peers will send DSM to (as of 0.9.58)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.49</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic messages to ECIES-X25519 routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 routers, ECIES-X25519 build request/response records</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup flag bit 4 for AEAD reply</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.44</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 keys in LeaseSet2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.40</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet may be sent in a DSM, RedDSA_SHA512_Ed25519 signature type supported</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 transport support (if published in router info), minimum peers will build tunnels through (as of 0.9.46)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.28</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signature types disallowed, minimum floodfill peers will send DSM to (as of 0.9.34)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 7-1 ignored</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RI key certs / ECDSA and EdDSA signature types, DLM lookup types (flag bits 3-2), minimum version compatible with the current network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with EdDSA Ed25519 signature type (if floodfill)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with ECDSA P-256, P-384, and P-521 signature types (if floodfill); non-zero expiration allowed in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) for floodfill routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Non-zero DLM flag bits 7-1 allowed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Requires zero expiration in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Supports up to 16 leases in a DSM LeaseSet store (previously 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">VTBM and VTBRM message support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill supports encrypted DSM stores</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBM and TBRM messages introduced; minimum version compatible with the current network</td></tr>
  </tbody>
</table>
**ملاحظة:** هناك أيضًا ميزات متعلقة بالنقل ومشكلات في التوافق. راجع وثائق النقل الخاصة بـ NTCP2 وSSU2 للاطّلاع على التفاصيل.

---

## رأس الرسالة

يستخدم I2NP بنية ترويسة منطقية بطول 16 بايت، بينما تستخدم وسائط النقل الحديثة (NTCP2 وSSU2) ترويسة مختصرة بطول 9 بايت مع حذف حقول الحجم والمجموع الاختباري الزائدة عن الحاجة. تظل الحقول متماثلة من الناحية المفاهيمية.

### مقارنة تنسيق الترويسة

**التنسيق القياسي (16 بايت):**

يُستخدم في نقل NTCP القديم وعندما تُضمَّن رسائل I2NP داخل رسائل أخرى (TunnelData، TunnelGateway، GarlicClove).

```
Bytes 0-15:
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

type :: Integer (1 byte)
        Identifies the message type (see message type table)

msg_id :: Integer (4 bytes)
          Uniquely identifies this message (for some time at least)
          Usually a locally-generated random number, but for outgoing
          tunnel build messages may be derived from the incoming message

expiration :: Date (8 bytes)
              Unix timestamp in milliseconds when this message expires

size :: Integer (2 bytes)
        Length of the payload (0 to ~61.2 KB for tunnel messages)

chks :: Integer (1 byte)
        SHA256 hash of payload truncated to first byte
        Deprecated - NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity
```
**الصيغة القصيرة لـ SSU (مهجورة، 5 بايتات):**

```
+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

type :: Integer (1 byte)
short_expiration :: Integer (4 bytes, seconds since epoch)
```
**الصيغة القصيرة لـ NTCP2 و SSU2، وفصوص الثوم الخاصة بـ ECIES-Ratchet (آلية السقاطة الخاصة بـ ECIES) (9 بايت):**

يُستخدم في وسائط النقل الحديثة وفي رسائل garlic (أسلوب تجميع رسائل متعددة في I2P) المشفّرة بـ ECIES.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer (1 byte)
msg_id :: Integer (4 bytes)
short_expiration :: Integer (4 bytes, seconds since epoch, unsigned)
```
### تفاصيل حقل الرأس

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Type</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Identifies the message class (0&ndash;255, see message types below)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Unique ID</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Locally unique identifier for matching replies</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Expiration</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 (standard) / 4 (short)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Timestamp when the message expires. Routers discard expired messages. Short format uses seconds since epoch (unsigned, wraps February 7, 2106)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Payload Length</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Size in bytes (0 to ~61.2 KB for tunnel messages). NTCP2 and SSU2 encode this in their frame headers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated. First byte of SHA-256 hash of the payload. NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity</td>
    </tr>
  </tbody>
</table>
### ملاحظات التنفيذ

- عند الإرسال عبر SSU (متقادم)، كان يتم تضمين النوع ووقت الانقضاء المكوَّن من 4 بايت فقط
- عند الإرسال عبر NTCP2 أو SSU2 (الإصدار 2 من SSU)، يُستخدم التنسيق القصير بحجم 9 بايت
- يلزم وجود الترويسة القياسية بحجم 16 بايت لرسائل I2NP المُضمَّنة داخل رسائل أخرى (Data, TunnelData, TunnelGateway, GarlicClove)
- اعتباراً من الإصدار 0.8.12، تم تعطيل التحقق من المجموع الاختباري في بعض المواضع ضمن مكدس البروتوكولات من أجل الكفاءة، لكن ما يزال توليد المجموع الاختباري مطلوباً للتوافق
- إن وقت الانقضاء القصير غير موقَّع وسيلتفّ في 7 فبراير 2106. بعد ذلك التاريخ، يجب إضافة إزاحة للحصول على الوقت الصحيح
- للتوافق مع الإصدارات الأقدم، قم دائماً بتوليد المجاميع الاختبارية حتى وإن لم تُتحقق منها

---

## قيود الحجم

رسائل Tunnel تقسّم حمولات I2NP إلى قطع ثابتة الحجم: - **القطعة الأولى:** حوالي 956 بايت - **القطع اللاحقة:** كل منها حوالي 996 بايت - **الحد الأقصى للقطع:** 64 (مرقمة من 0 إلى 63) - **الحد الأقصى للحمولة:** حوالي 61,200 بايت (61.2 KB)

**الحساب:** 956 + (63 × 996) = 63,704 بايت كحد أقصى نظري، مع حد عملي يقارب 61,200 بايت بسبب الكلفة الإضافية.

### السياق التاريخي

كانت وسائط النقل القديمة تفرض حدوداً أكثر صرامة لحجم الإطارات: - NTCP: إطارات بحجم 16 KB - SSU: إطارات بحجم يقارب 32 KB

يدعم NTCP2 إطارات بحجم يقارب 65 KB، لكن حدّ التجزئة الخاص بـ tunnel ما زال سارياً.

### اعتبارات بيانات التطبيق

قد تقوم رسائل Garlic (رسائل مركبة في I2P) بتجميع LeaseSets أو وسوم الجلسة أو متغيرات LeaseSet2 المشفّرة، مما يقلل المساحة المتاحة لبيانات الحمولة.

**التوصية:** ينبغي أن تبقى Datagrams (رزم بيانات عديمة الاتصال) ≤ 10 KB لضمان تسليم موثوق. قد تواجه الرسائل التي تقترب من حد 61 KB: - ازدياد زمن الاستجابة بسبب إعادة تجميع الأجزاء بعد التجزئة - ارتفاع احتمال فشل التسليم - تعرّض أكبر لتحليل حركة المرور

### التفاصيل التقنية للتجزئة

كل رسالة tunnel يبلغ حجمها بالضبط 1,024 بايت (1 كيلوبايت) وتحتوي على: - tunnel ID بطول 4 بايت - متجه التهيئة (IV) بطول 16 بايت - 1,004 بايت من البيانات المشفّرة

ضمن البيانات المُشفّرة، تحمل رسائل tunnel رسائل I2NP مُجزأة مع رؤوس أجزاء تشير إلى: - رقم الجزء (0-63) - ما إذا كان هذا هو الجزء الأول أم جزء لاحق - معرّف الرسالة الكلي لإعادة التجميع

يتضمن الجزء الأول كامل ترويسة رسالة I2NP (16 بايت)، مما يترك حوالي 956 بايتاً للحمولة. الأجزاء اللاحقة لا تتضمن ترويسة الرسالة، ما يتيح نحو 996 بايتاً من الحمولة لكل جزء.

---

## أنواع الرسائل الشائعة

تستخدم Routers نوع الرسالة والأولوية لجدولة المهام الصادرة. تُعالج القيم ذات الأولوية الأعلى أولاً. تطابق القيم أدناه الإعدادات الافتراضية الحالية في Java I2P (اعتباراً من إصدار واجهة برمجة التطبيقات 0.9.67).

**ملاحظة:** تعتمد قيم الأولوية على التنفيذ. للحصول على قيم الأولوية المرجعية، راجع توثيق الصنف `OutNetMessage` في الشيفرة المصدرية لـ Java I2P.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Priority</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseStore</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">460</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies (LeaseSet ≈ 898&nbsp;B, RouterInfo ≈ 2&ndash;4&nbsp;KB compressed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishes RouterInfo or LeaseSet objects. Supports LeaseSet2, EncryptedLeaseSet, and MetaLeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseLookup</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queries the network database for RouterInfo or LeaseSet entries</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseSearchReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">≈161&nbsp;B (5 hashes)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Returns candidate floodfill router hashes (typically 3&ndash;16 hashes, recommended maximum 16)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DeliveryStatus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">12&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receipts for tunnel tests or acknowledgements inside GarlicMessages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>GarlicMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">100 (local)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bundles multiple message cloves (e.g., DataMessage, LeaseSets). Supports ElGamal/AES (deprecated) and ECIES-X25519-AEAD-Ratchet encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelData</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,028&nbsp;B (fixed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted tunnel message exchanged between hops. Contains a 4-byte tunnel ID, 16-byte IV, and 1,004 bytes of encrypted data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelGateway</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300&ndash;400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encapsulates messages at the tunnel gateway before fragmentation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DataMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">425</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4&ndash;62&nbsp;KB</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Carries end-to-end garlic payloads (application traffic)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuild</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requests tunnel participation from routers (8 × 528-byte records). Replaced by VariableTunnelBuild for ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuildReply</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to TunnelBuild with accept/reject status per hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable-length tunnel build for ElGamal or ECIES-X25519 routers (1&ndash;8 records, API 0.9.12+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to VariableTunnelBuild</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ShortTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers only (1&ndash;8 × 218-byte records, API 0.9.51+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>OutboundTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sent from outbound endpoint to originator for ECIES-X25519 routers (API 0.9.51+)</td>
    </tr>
  </tbody>
</table>
**أنواع الرسائل المحجوزة:** - النوع 0: محجوز - الأنواع 4-9: محجوزة للاستخدام المستقبلي - الأنواع 12-17: محجوزة للاستخدام المستقبلي - الأنواع 224-254: محجوزة للرسائل التجريبية - النوع 255: محجوز للتوسّع المستقبلي

### ملاحظات حول نوع الرسالة

- رسائل مستوى التحكم (DatabaseLookup, TunnelBuild, إلخ.) عادةً تنتقل عبر **exploratory tunnels**، وليس عبر client tunnels، مما يتيح تحديد الأولوية بشكل مستقل
- قيم الأولوية تقريبية وقد تختلف حسب التنفيذ
- TunnelBuild (21) و TunnelBuildReply (22) مُهملة لكنها ما تزال مُنفّذة لأغراض التوافق مع tunnels طويلة جداً (>8 قفزات)
- أولوية بيانات tunnel القياسية هي 400؛ وكل ما هو أعلى من ذلك يُعامل كعاجل
- الطول المعتاد لـ tunnel في شبكة اليوم هو 3-4 قفزات، لذا فإن معظم عمليات إنشاء tunnel تستخدم ShortTunnelBuild (سجلات بحجم 218 بايت) أو VariableTunnelBuild (سجلات بحجم 528 بايت)

---

## التشفير وتغليف الرسائل

غالبًا ما تقوم routers بتغليف رسائل I2NP قبل الإرسال، مما يخلق طبقات متعددة من التشفير. قد تكون رسالة DeliveryStatus: 1. ملفوفة داخل GarlicMessage (مشفّرة) 2. داخل DataMessage 3. ضمن رسالة TunnelData (مشفّرة مرة أخرى)

كل hop (قفزة) يفك تشفير طبقته فقط؛ تكشف الوجهة النهائية عن الحمولة الأعمق في الداخل.

### خوارزميات التشفير

**قديمة (يجري التخلص منها تدريجياً):** - ElGamal/AES + SessionTags (وسوم الجلسة) - ElGamal-2048 للتشفير غير المتماثل - AES-256 للتشفير المتماثل - وسوم الجلسة بطول 32 بايت

**الوضع الحالي (المعيار ابتداءً من API 0.9.48):** - ECIES-X25519 + ChaCha20/Poly1305 AEAD (تشفير موثق مع بيانات إضافية) مع سرية أمامية متدرجة - إطار عمل بروتوكول Noise (Noise_IK_25519_ChaChaPoly_SHA256 للوجهات) - وسوم جلسة بحجم 8 بايت (مخفضة من 32 بايت) - Signal Double Ratchet (خوارزمية السقاطة المزدوجة الخاصة ببروتوكول سيغنال) للسرية الأمامية - تم تقديمه في إصدار API 0.9.46 (2020) - إلزامي لجميع routers اعتباراً من إصدار API 0.9.58 (2023)

**المستقبل (بيتا اعتباراً من 2.10.0):** - تشفير هجين مقاوم لما بعد الكم باستخدام MLKEM (خوارزمية تبادل مفاتيح مقاومة للكم، ML-KEM-768) مقترناً بـ X25519 - آلية سقاطة هجينة تجمع بين اتفاق المفاتيح الكلاسيكي واتفاق المفاتيح لما بعد الكم - متوافق رجعياً مع ECIES-X25519 - سيصبح الإعداد الافتراضي في الإصدار 2.11.0 (ديسمبر 2025)

### إلغاء الاعتماد التدريجي لـ ElGamal Router

**هام للغاية:** تم إهمال ElGamal routers بدءًا من إصدار API 0.9.58 (الإصدار 2.2.0، مارس 2023). وبما أن الحد الأدنى الموصى به لإصدار floodfill المراد الاستعلام عنه أصبح الآن 0.9.58، فلا حاجة لأن تقوم عمليات التنفيذ بتنفيذ التشفير لـ ElGamal floodfill routers.

**مع ذلك:** لا تزال وجهات ElGamal مدعومة للتوافق مع الإصدارات السابقة. لا يزال بإمكان العملاء الذين يستخدمون تشفير ElGamal التواصل عبر ECIES routers.

### تفاصيل ECIES-X25519-AEAD-Ratchet

هذا هو نوع التشفير 4 في مواصفة التشفير الخاصة بـ I2P. يوفّر:

**أهم الميزات:** - سرّية أمامية عبر ratcheting (آلية تدوير مفاتيح تدريجية؛ مفاتيح جديدة لكل رسالة) - تقليل مساحة تخزين وسم الجلسة (8 بايت مقابل 32 بايت) - أنواع جلسات متعددة (جلسة جديدة، جلسة قائمة، لمرة واحدة) - قائم على بروتوكول Noise Noise_IK_25519_ChaChaPoly_SHA256 - متكامل مع خوارزمية Double Ratchet الخاصة بـ Signal

**البدائيات التشفيرية:** - X25519 لاتفاق تبادل المفاتيح Diffie-Hellman - ChaCha20 لتشفير الدفق - Poly1305 لمصادقة الرسائل (AEAD) - SHA-256 للتجزئة - HKDF لاشتقاق المفاتيح

**إدارة الجلسات:** - جلسة جديدة: اتصال أولي باستخدام مفتاح وجهة ثابت - جلسة قائمة: رسائل لاحقة باستخدام علامات الجلسة - جلسة لمرة واحدة: جلسات برسالة واحدة بعبء بروتوكولي أقل

راجع [مواصفة ECIES](/docs/specs/ecies/) و[الاقتراح 144](/proposals/144-ecies-x25519-aead-ratchet/) للحصول على التفاصيل التقنية الكاملة.

---

## البنى الشائعة

البُنى التالية هي عناصر في عدة رسائل I2NP. وهي ليست رسائل كاملة.

### BuildRequestRecord (ElGamal)

**مهمل.** يُستخدَم فقط في الشبكة الحالية عندما يحتوي tunnel على router من نوع ElGamal. راجع [ECIES Tunnel Creation](/docs/specs/implementation/) للتنسيق الحديث.

**الغرض:** سجل واحد ضمن مجموعة تضم عدة سجلات لطلب إنشاء قفزة واحدة داخل الـ tunnel.

**التنسيق:**

مشفّر بـ ElGamal وAES (إجمالي 528 بايت):

```
+----+----+----+----+----+----+----+----+
| encrypted data (528 bytes)            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
بنية مشفّرة بـ ElGamal (خوارزمية تشفير بالمفتاح العام) (528 بايت):

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ElGamal encrypted data (512 bytes)    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity

encrypted_data :: ElGamal-2048 encrypted (bytes 1-256 and 258-513
                  of the 514-byte ElGamal block, with padding bytes
                  at positions 0 and 257 removed)
```
بنية النص الواضح (222 بايت قبل التشفير):

```
+----+----+----+----+----+----+----+----+
| receive_tunnel (4) | our_ident (32)   |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel (4)   |
+----+----+----+----+----+----+----+----+
| next_ident (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key (32 bytes)                     |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv (16 bytes)                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time (4) | send_msg_id  |
+----+----+----+----+----+----+----+----+
     (4)                | padding (29)  |
+----+----+----+----+----+              +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId (4 bytes, nonzero)
our_ident :: Hash (32 bytes)
next_tunnel :: TunnelId (4 bytes, nonzero)
next_ident :: Hash (32 bytes)
layer_key :: SessionKey (32 bytes)
iv_key :: SessionKey (32 bytes)
reply_key :: SessionKey (32 bytes)
reply_iv :: 16 bytes
flag :: Integer (1 byte)
request_time :: Integer (4 bytes, hours since epoch = time / 3600)
send_message_id :: Integer (4 bytes)
padding :: 29 bytes random data
```
**ملاحظات:** - ينتج عن تشفير ElGamal-2048 (خوارزمية تشفير بالمفتاح العام) كتلة بحجم 514 بايت، لكن يتم إزالة بايتي الحشو (في الموضعين 0 و257)، لينتج 512 بايت - راجع [مواصفة إنشاء Tunnel](/docs/specs/implementation/) لمعرفة تفاصيل الحقول - الشيفرة المصدرية: `net.i2p.data.i2np.BuildRequestRecord` - ثابت: `EncryptedBuildRecord.RECORD_SIZE = 528`

### BuildRequestRecord (سجل طلب البناء) (ECIES-X25519 المطوّل)

بالنسبة إلى ECIES-X25519 (مخطط ECIES فوق X25519) routers، التي تم تقديمها في إصدار API 0.9.48. تستخدم 528 بايتًا للحفاظ على التوافق مع الإصدارات الأقدم في tunnels المختلطة.

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (464 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (464 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**إجمالي الحجم:** 528 بايت (مماثل لـElGamal للتوافق)

راجع [ECIES Tunnel Creation](/docs/specs/implementation/) للاطلاع على بنية النص غير المشفّر وتفاصيل التشفير.

### BuildRequestRecord (ECIES-X25519 قصير)

خاص بـ ECIES-X25519 routers فقط، اعتباراً من إصدار API 0.9.51 (الإصدار 1.5.0). هذا هو التنسيق القياسي الحالي.

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (154 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (154 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**الحجم الإجمالي:** 218 بايت (انخفاض بنسبة 59% مقارنةً بـ 528 بايت)

**الاختلاف الرئيسي:** تستمد السجلات القصيرة جميع المفاتيح عبر HKDF (وظيفة اشتقاق المفاتيح) بدلاً من تضمينها بشكل صريح في السجل. يشمل ذلك: - مفاتيح الطبقة (لتشفير tunnel) - مفاتيح IV (لتشفير tunnel) - مفاتيح الرد (لبناء الرد) - قيم IV الخاصة بالرد (لبناء الرد)

يتم اشتقاق جميع المفاتيح باستخدام آلية HKDF الخاصة ببروتوكول Noise، استنادًا إلى السرّ المشترك الناتج عن تبادل المفاتيح X25519.

**الفوائد:** - تتسع 4 سجلات قصيرة في رسالة tunnel واحدة (873 بايت) - عمليات بناء tunnel بثلاث رسائل بدلاً من رسائل منفصلة لكل سجل - انخفاض استهلاك النطاق الترددي والكمون - نفس خصائص الأمان كما في التنسيق الطويل

انظر [المقترح 157](/proposals/157-new-tbm/) للمبررات و[إنشاء Tunnel باستخدام ECIES](/docs/specs/implementation/) للمواصفة الكاملة.

**شفرة المصدر:** - `net.i2p.data.i2np.ShortEncryptedBuildRecord` - ثابت: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

### BuildResponseRecord (ElGamal)

**مهمل.** يُستخدم فقط عندما يحتوي الـ tunnel على router من نوع ElGamal.

**الغرض:** سجل واحد ضمن مجموعة من سجلات متعددة تتضمن استجابات لطلب إنشاء.

**التنسيق:**

مشفّر (528 بايت، نفس حجم BuildRequestRecord (سجلّ طلب البناء)):

```
bytes 0-527 :: AES-encrypted record
```
البنية غير المشفرة:

```
+----+----+----+----+----+----+----+----+
| SHA-256 hash (32 bytes)               |
+                                       +
|        (hash of bytes 32-527)         |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data (495 bytes)               |
~                                       ~
|                                  |ret |
+----+----+----+----+----+----+----+----+

bytes 0-31 :: SHA-256 hash of bytes 32-527
bytes 32-526 :: Random data (could be used for congestion info)
byte 527 :: Reply code (0 = accept, 30 = reject)
```
**رموز الرد:** - `0` - قبول - `30` - رفض (تجاوز حد عرض النطاق)

انظر [مواصفة إنشاء Tunnel](/docs/specs/implementation/) للتفاصيل حول حقل الرد.

### سجل استجابة البناء (ECIES-X25519)

بالنسبة إلى routers التي تستخدم ECIES-X25519 (مخطط تشفير بالمنحنى الإهليلجي باستخدام X25519)، إصدار واجهة برمجة التطبيقات 0.9.48+. بنفس حجم الطلب المقابل (528 للطويل، 218 للقصير).

**التنسيق:**

الصيغة الطويلة (528 بايت):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (512 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
التنسيق المختصر (218 بايت):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (202 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**بنية النص الصريح (كلا التنسيقين):**

يحتوي على بنية Mapping (بنية تعيين) بصيغة key-value الخاصة بـ I2P مع: - رمز حالة الرد (إلزامي) - معامل عرض النطاق المتاح ("b") (اختياري، أضيف في API 0.9.65) - معلمات اختيارية أخرى للتوسعات المستقبلية

**رموز حالة الرد:** - `0` - نجاح - `30` - رفض: تم تجاوز عرض النطاق الترددي

انظر [إنشاء Tunnel باستخدام ECIES](/docs/specs/implementation/) للاطلاع على المواصفة الكاملة.

### GarlicClove (مكوّن رسالة ضمن garlic encryption) (ElGamal/AES)

**تحذير:** هذا هو التنسيق المستخدم لفصوص الثوم داخل رسائل الثوم المُشفَّرة باستخدام ElGamal (خوارزمية تشفير بالمفتاح العام). يختلف تنسيق رسائل الثوم وفصوص الثوم الخاصة بـ ECIES-AEAD-X25519-Ratchet اختلافًا كبيرًا. راجع [مواصفة ECIES](/docs/specs/ecies/) (مخطط التشفير المتكامل بالمنحنيات البيضوية) للاطلاع على التنسيق الحديث.

**أُعلن إهماله بالنسبة إلى routers (API 0.9.58+)، ولا يزال مدعومًا للوجهات.**

**التنسيق:**

غير مشفّر:

```
+----+----+----+----+----+----+----+----+
| Delivery Instructions (variable)      |
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message (variable)               |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (8)   |Cert|
+----+----+----+----+----+----+----+----+
                                    (3) |
+----+----+----+----+----+----+----+----+

Delivery Instructions :: Variable length (typically 1, 33, or 37 bytes)
I2NP Message :: Any I2NP message
Clove ID :: 4-byte Integer (random, checked for duplicates)
Expiration :: Date (8 bytes)
Certificate :: Always NULL (3 bytes total, all zeroes)
```
**ملاحظات:** - لا تُجزَّأ الـ clove (رسالة فرعية ضمن GarlicMessage) إطلاقًا - عندما يكون البِتّ الأول من بايت العَلَم لـ Delivery Instructions (تعليمات التسليم) يساوي 0، لا يُشفَّر الـ clove - عندما يكون البِتّ الأول 1، يكون الـ clove مُشفَّرًا (ميزة غير منفذة) - الطول الأقصى دالة لمجموع أطوال الـ cloves وللطول الأقصى لـ GarlicMessage (رسالة حاوية لعدة cloves) - قد يُستخدم حقل الشهادة (Certificate) مع HashCash لـ "الدفع" مقابل التوجيه (احتمال مستقبلي) - الرسائل المستخدمة عمليًا: DataMessage, DeliveryStatusMessage, DatabaseStoreMessage - يمكن أن تحتوي GarlicMessage على GarlicMessage (nested garlic)، لكن هذا لا يُستخدم عمليًا

انظر [Garlic Routing (توجيه «الثوم»)](/docs/overview/garlic-routing/) للحصول على نظرة عامة مفاهيمية.

### GarlicClove (ECIES-X25519-AEAD-Ratchet) (عنصر رسالة ضمن garlic encryption في I2P)

بالنسبة إلى routers والوجهات من نوع ECIES-X25519، إصدار API 0.9.46+. هذا هو التنسيق القياسي الحالي.

**اختلاف جوهري:** تستخدم ECIES garlic (أسلوب تجميع رسائل في I2P) بنية مختلفة تماماً تعتمد على كتل Noise protocol (بروتوكول Noise) بدلاً من البُنى الصريحة لـ clove (عنصر رسالة في I2P).

**التنسيق:**

تحتوي رسائل ECIES بأسلوب garlic (تقنية "garlic" في I2P) على سلسلة من الكتل:

```
Block structure:
+----+----+----+----+----+----+----+----+
|type| length    | data ...
+----+----+----+----+----+-//-

type :: 1 byte block type
length :: 2 bytes block length
data :: variable length data
```
**أنواع الكتل:** - `0` - Garlic Clove Block (كتلة فصّ الثوم؛ تحتوي على رسالة I2NP) - `1` - كتلة التاريخ والوقت (طابع زمني) - `2` - كتلة الخيارات (خيارات التسليم) - `3` - كتلة الحشو - `254` - كتلة الإنهاء (غير مُنفذة)

**Garlic Clove Block (كتلة فصّ الثوم) (النوع 0):**

```
+----+----+----+----+----+----+----+----+
|  0 | length    | Delivery Instructions |
+----+----+----+----+                    +
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (4)        |
+----+----+----+----+----+----+----+----+
```
**الفروقات الأساسية عن صيغة ElGamal:** - يستخدم انتهاء صلاحية بطول 4 بايت (ثوانٍ منذ Epoch، بداية حقبة يونكس) بدلاً من تاريخ بطول 8 بايت - لا يوجد حقل شهادة - مُغلّف ضمن بنية كتل تحتوي على النوع والطول - تُشفَّر الرسالة كاملة باستخدام ChaCha20/Poly1305 AEAD (تشفير مصادق مع بيانات مرتبطة) - إدارة الجلسة عبر ratcheting (آلية السقاطة الأمنية)

انظر [مواصفة ECIES](/docs/specs/ecies/) للتفاصيل الكاملة حول إطار عمل بروتوكول Noise (إطار لبناء بروتوكولات تبادل المفاتيح المشفّرة) وهياكل الكتل.

### تعليمات تسليم Garlic Clove (رسالة فرعية ضمن garlic encryption)

يُستخدم هذا التنسيق لفصوص الثوم الخاصة بكلٍ من ElGamal وECIES. وهو يحدد كيفية إيصال الرسالة المضمّنة.

**تحذير بالغ الأهمية:** هذه المواصفة مخصصة لـ Delivery Instructions (تعليمات التسليم) داخل Garlic Cloves (فصوص الثوم) فقط. تُستخدم "Delivery Instructions" أيضًا داخل رسائل tunnel، حيث يختلف التنسيق اختلافًا كبيرًا. راجع [مواصفة رسالة tunnel](/docs/specs/implementation/) بخصوص Delivery Instructions الخاصة بـ tunnel. لا تخلط بين هذين التنسيقين.

**التنسيق:**

مفتاح الجلسة والتأخير غير مستخدمين ولا يظهران مطلقًا، لذا فالأطوال الثلاثة الممكنة هي: - 1 بايت (LOCAL) - 33 بايت (ROUTER and DESTINATION) - 37 بايت (TUNNEL)

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|       Session Key (optional, 32)     |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|       To Hash (optional, 32)         |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    | Tunnel ID (4, opt)| Delay (4, opt)|
+----+----+----+----+----+----+----+----+

flag :: 1 byte
        Bit order: 76543210
        bit 7: encrypted? (Unimplemented, always 0)
               If 1, a 32-byte encryption session key follows
        bits 6-5: delivery type
               0x0 = LOCAL (0)
               0x1 = DESTINATION (1)
               0x2 = ROUTER (2)
               0x3 = TUNNEL (3)
        bit 4: delay included? (Not fully implemented, always 0)
               If 1, four delay bytes are included
        bits 3-0: reserved, set to 0 for compatibility

Session Key :: 32 bytes (Optional, unimplemented)
               Present if encrypt flag bit is set

To Hash :: 32 bytes (Optional)
           Present if delivery type is DESTINATION, ROUTER, or TUNNEL
           - DESTINATION: SHA256 hash of the destination
           - ROUTER: SHA256 hash of the router identity
           - TUNNEL: SHA256 hash of the gateway router identity

Tunnel ID :: 4 bytes (Optional)
             Present if delivery type is TUNNEL
             The destination tunnel ID (nonzero)

Delay :: 4 bytes (Optional, unimplemented)
         Present if delay included flag is set
         Specifies delay in seconds
```
**الأطوال النموذجية:** - تسليم محلي: 1 بايت (العلم فقط) - تسليم ROUTER / الوجهة: 33 بايت (العلم + التجزئة) - تسليم TUNNEL: 37 بايت (العلم + التجزئة + tunnel ID)

**أوصاف نوع التسليم:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LOCAL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to the local router (this router)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DESTINATION</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a destination (client) identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ROUTER</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to another router identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TUNNEL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a tunnel gateway router</td>
    </tr>
  </tbody>
</table>

---

## رسائل I2NP

المواصفات الكاملة للرسائل لجميع أنواع رسائل I2NP.

### ملخص أنواع الرسائل

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseSearchReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelData</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelGateway</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ShortTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">OutboundTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
  </tbody>
</table>
**محجوز:** - النوع 0: محجوز - الأنواع 4-9: محجوز للاستخدام المستقبلي - الأنواع 12-17: محجوز للاستخدام المستقبلي - الأنواع 224-254: محجوز للرسائل التجريبية - النوع 255: محجوز للتوسعة المستقبلية

---

### DatabaseStore (رسالة تخزين قاعدة البيانات) (النوع 1)

**الغرض:** عملية تخزين في قاعدة البيانات غير مطلوبة مسبقاً، أو استجابة لرسالة DatabaseLookup (رسالة البحث في قاعدة البيانات) ناجحة.

**المحتويات:** أيٌّ من LeaseSet (بنية بيانات في I2P) أو LeaseSet2 أو MetaLeaseSet أو EncryptedLeaseSet غير مضغوط، أو RouterInfo مضغوط.

**تنسيق باستخدام رمز الرد:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token (4)   | reply_tunnelId
+----+----+----+----+----+----+----+----+
     (4)               | reply gateway  |
+----+----+----+----+----+              +
|       SHA256 hash (32 bytes)          |
+                                       +
|                                       |
+                                  +----+
|                                  |
+----+----+----+----+----+----+----+
| data ...
+----+-//

key :: 32 bytes
       SHA256 hash (the "real" hash, not routing key)

type :: 1 byte
        Type identifier
        bit 0:
            0 = RouterInfo
            1 = LeaseSet or variants
        bits 3-1: (as of 0.9.38)
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
        bits 7-4:
            Reserved, set to 0

reply token :: 4 bytes
               If greater than zero, a DeliveryStatusMessage is
               requested with the Message ID set to the reply token
               A floodfill router is also expected to flood the data
               to the closest floodfill peers

reply_tunnelId :: 4 bytes (only if reply token > 0)
                  TunnelId of the inbound gateway of the tunnel
                  for the response
                  If 0, reply is sent directly to reply gateway

reply gateway :: 32 bytes (only if reply token > 0)
                 SHA256 hash of the RouterInfo
                 If reply_tunnelId is nonzero: inbound gateway router
                 If reply_tunnelId is zero: router to send reply to

data :: Variable length
        If type == 0: 2-byte Integer length + gzip-compressed RouterInfo
        If type == 1: Uncompressed LeaseSet
        If type == 3: Uncompressed LeaseSet2
        If type == 5: Uncompressed EncryptedLeaseSet
        If type == 7: Uncompressed MetaLeaseSet
```
**التنسيق باستخدام رمز الرد == 0:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//
```

**الشيفرة المصدرية:** - `net.i2p.data.i2np.DatabaseStoreMessage` - `net.i2p.data.RouterInfo` (لبنية RouterInfo) - `net.i2p.data.LeaseSet` (لبنية LeaseSet)

---

### DatabaseLookup (استعلام قاعدة البيانات) (النوع 2)

**الغرض:** طلب للاستعلام عن عنصر في قاعدة بيانات الشبكة. تكون الاستجابة إما DatabaseStore (رسالة تخزين قاعدة البيانات) أو DatabaseSearchReply (رسالة ردّ البحث في قاعدة البيانات).

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key (32 bytes)    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the from router (32)  |
+    or reply tunnel gateway            +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId (4)| size (2)|   |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude (32 bytes) |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude (32)       |
+                                       +
~                                       ~
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|   Session key if reply encryption     |
+       requested (32 bytes)             +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|   Session tags if reply encryption    |
+       requested (variable)             +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

key :: 32 bytes
       SHA256 hash of the object to lookup

from :: 32 bytes
        If deliveryFlag == 0: SHA256 hash of RouterInfo (sender)
        If deliveryFlag == 1: SHA256 hash of reply tunnel gateway

flags :: 1 byte
         Bit order: 76543210
         bit 0: deliveryFlag
             0 = send reply directly
             1 = send reply to some tunnel
         bit 1: encryptionFlag
             Through 0.9.5: must be 0
             As of 0.9.6: ignored
             As of 0.9.7:
                 0 = send unencrypted reply
                 1 = send AES encrypted reply using key and tag
         bits 3-2: lookup type flags
             Through 0.9.5: must be 00
             As of 0.9.6: ignored
             As of 0.9.16:
                 00 = ANY (deprecated, use LS or RI as of 0.9.16)
                 01 = LS lookup (LeaseSet or variants)
                 10 = RI lookup (RouterInfo)
                 11 = exploration lookup (RouterInfo, non-floodfill)
         bit 4: ECIESFlag
             Before 0.9.46: ignored
             As of 0.9.46:
                 0 = send unencrypted or ElGamal reply
                 1 = send ChaCha/Poly encrypted reply using key
         bits 7-5:
             Reserved, set to 0

reply_tunnelId :: 4 bytes (only if deliveryFlag == 1)
                  TunnelId of the tunnel to send reply to (nonzero)

size :: 2 bytes
        Integer (valid range: 0-512)
        Number of peers to exclude from DatabaseSearchReply

excludedPeers :: $size SHA256 hashes of 32 bytes each
                 If lookup fails, exclude these peers from the reply
                 If includes a hash of all zeroes, the request is
                 exploratory (return non-floodfill routers only)

reply_key :: 32 bytes (conditional, see encryption modes below)
reply_tags :: 1 byte count + variable length tags (conditional)
```
**أنماط تشفير الرد:**

**ملاحظة:** أصبحت ElGamal routers متقادمة اعتبارًا من API 0.9.58. وبما أن الإصدار الأدنى الموصى به من floodfill للاستعلام هو الآن 0.9.58، فلا يلزم على عمليات التنفيذ تطبيق التشفير لـ ElGamal floodfill routers. لا تزال وجهات ElGamal مدعومة.

يُستخدم البت رقم 4 (ECIESFlag) بالاقتران مع البت رقم 1 (encryptionFlag) لتحديد وضع تشفير الرد:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Flag bits 4,1</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">From</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">To Router</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reply</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DH?</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.7, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.46, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.49, current standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
  </tbody>
</table>
**بدون تشفير (الأعلام 0,0):**

لا وجود لـ reply_key أو tags أو reply_tags.

**ElG إلى ElG (أعلام 0,1) - مهمل:**

مدعوم اعتباراً من 0.9.7، وأُعلن إهماله اعتباراً من 0.9.58.

```
reply_key :: 32 byte SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (1-32, typically 1)
        Number of reply tags that follow

reply_tags :: One or more 32-byte SessionTags
              Each is CSRNG(32) random data
```
**ECIES (مخطط تشفير مدمج بالمنحنيات الإهليلجية) إلى ElG (إل-غامال) (أعلام 1,0) - مهمل:**

مدعوم اعتبارًا من 0.9.46، ومهمل اعتبارًا من 0.9.58.

```
reply_key :: 32 byte ECIES SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (required value: 1)
        Number of reply tags that follow

reply_tags :: One 8-byte ECIES SessionTag
              CSRNG(8) random data
```
الرد هو رسالة ECIES Existing Session (ECIES: مخطط التشفير المتكامل للمنحنيات الإهليلجية) كما هو محدد في [مواصفة ECIES](/docs/specs/ecies/):

```
+----+----+----+----+----+----+----+----+
| Session Tag (8 bytes)                 |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted payload            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

tag :: 8 byte reply_tag
k :: 32 byte session key (the reply_key)
n :: 0 (nonce)
ad :: The 8 byte reply_tag
payload :: Plaintext data (DSM or DSRM)
ciphertext = ENCRYPT(k, n, payload, ad)
```
**ECIES (نظام تشفير متكامل قائم على المنحنيات الإهليلجية) إلى ECIES (flags 1,0) - المعيار الحالي:**

تقوم وجهة ECIES (مخطط التشفير المتكامل بالمنحنى البيضوي) أو router بإرسال استعلام إلى router يعتمد ECIES. مدعوم ابتداءً من الإصدار 0.9.49.

نفس التنسيق كما في "ECIES to ElG" أعلاه. يتم تحديد تشفير رسالة الاستعلام في [ECIES (تشفير متكامل قائم على المنحنى الإهليلجي) Routers](/docs/specs/ecies/#routers). الجهة الطالبة مجهولة الهوية.

**ECIES (مخطط التشفير المتكامل بالمنحنيات الإهليلجية) إلى ECIES مع DH (تبادل مفاتيح ديفي-هيلمان) (أعلام 1,1) - مستقبلاً:**

لم يتم تحديده بالكامل بعد. انظر [المقترح 156](/proposals/156-ecies-routers/).

**ملاحظات:** - قبل 0.9.16، قد يكون المفتاح لـ RouterInfo أو LeaseSet (نفس فضاء المفاتيح، دون علم للتمييز) - تكون الردود المشفّرة مفيدة فقط عندما يكون الرد عبر tunnel - قد يكون عدد الوسوم المتضمّنة أكبر من واحد إذا نُفِّذت استراتيجيات استعلام DHT بديلة - مفتاح الاستعلام ومفاتيح الاستبعاد هي التجزئات "الحقيقية"، وليست مفاتيح التوجيه - قد تُعاد الأنواع 3 و5 و7 (متغيرات LeaseSet2) اعتبارًا من 0.9.38. انظر [Proposal 123](/proposals/123-new-netdb-entries/) - **ملاحظات الاستعلام الاستكشافي:** يُعرَّف الاستعلام الاستكشافي بأنه يُرجع قائمة بتجزئات غير floodfill قريبة من المفتاح. ومع ذلك، تختلف التطبيقات: تقوم Java فعلًا بالاستعلام عن مفتاح البحث لـ RI وتُعيد DatabaseStore إن وُجد؛ أما i2pd فلا يفعل ذلك. لذلك لا يُنصح باستخدام استعلام استكشافي للتجزئات المُستلمة سابقًا

**الشيفرة المصدرية:** - `net.i2p.data.i2np.DatabaseLookupMessage` - التشفير: `net.i2p.crypto.SessionKeyManager`

---

### DatabaseSearchReply (ردّ بحث قاعدة البيانات) (النوع 3)

**الغرض:** الاستجابة لرسالة DatabaseLookup (بحث في قاعدة البيانات) التي فشلت.

**المحتويات:** قائمة بتجزئات router الأقرب إلى المفتاح المطلوب.

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key (32 bytes)  |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes (variable)           |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    | from (32 bytes)                  |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key :: 32 bytes
       SHA256 of the object being searched

num :: 1 byte Integer
       Number of peer hashes that follow (0-255)

peer_hashes :: $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
               SHA256 of the RouterIdentity that the sender thinks is
               close to the key

from :: 32 bytes
        SHA256 of the RouterInfo of the router this reply was sent from
```

**الشيفرة المصدرية:** - `net.i2p.data.i2np.DatabaseSearchReplyMessage`

---

### حالة التسليم (النوع 10)

**الغرض:** إقرار بسيط باستلام الرسالة. عادةً ما يُنشئه مُرسِل الرسالة ويُغلَّف ضمن Garlic Message (رسالة Garlic، نوع رسالة في I2P) مع الرسالة نفسها، ليُعاد من قِبل الوجهة.

**المحتويات:** مُعرِّف الرسالة المُسلَّمة ووقت الإنشاء أو الوصول.

**التنسيق:**

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id (4)            | time_stamp (8)                    |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer (4 bytes)
          Unique ID of the message we deliver the DeliveryStatus for
          (see I2NP Message Header for details)

time_stamp :: Date (8 bytes)
              Time the message was successfully created or delivered
```
**ملاحظات:** - يُضبط الطابع الزمني دائمًا من قبل المُنشئ على الوقت الحالي. ومع ذلك، هناك عدة استخدامات لهذا في الشيفرة، وقد يُضاف المزيد في المستقبل - تُستخدم هذه الرسالة أيضًا كتأكيد على إنشاء الجلسة في SSU. في هذه الحالة، يُضبط معرّف الرسالة على رقم عشوائي، ويُضبط "وقت الوصول" على المعرّف الحالي على مستوى الشبكة، وهو 2 (أي `0x0000000000000002`) - عادةً ما يتم تغليف DeliveryStatus (رسالة حالة التسليم) داخل GarlicMessage (رسالة Garlic) وإرساله عبر tunnel لتقديم إقرار بالاستلام من دون كشف المُرسِل - تُستخدم لاختبار tunnel لقياس زمن الوصول والموثوقية

**الشيفرة المصدرية:** - `net.i2p.data.i2np.DeliveryStatusMessage` - يُستخدم في: `net.i2p.router.tunnel.InboundEndpointProcessor` لاختبار tunnel (نفق اتصال في I2P)

---

### GarlicMessage (النوع 11)

**تحذير:** هذا هو التنسيق المستخدم لرسائل garlic المشفّرة بـ ElGamal (أسلوب I2P لتجميع عدة رسائل في رسالة واحدة). يختلف تنسيق رسائل ECIES-AEAD-X25519-Ratchet garlic اختلافًا كبيرًا. راجع [مواصفة ECIES](/docs/specs/ecies/) للاطلاع على التنسيق الحديث.

**الغرض:** يُستخدم لتغليف عدة رسائل I2NP مُشفّرة.

**المحتويات:** عند فك التشفير، توجد سلسلة من Garlic Cloves (وحدات رسائل ضمن garlic encryption) وبيانات إضافية، تُعرف أيضًا باسم Clove Set (مجموعة الفصوص).

**تنسيق مشفّر:**

```
+----+----+----+----+----+----+----+----+
| length (4)            | data          |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length :: 4 byte Integer
          Number of bytes that follow (0 to 64 KB)

data :: $length bytes
        ElGamal encrypted data
```
**البيانات المفكوك تشفيرها (Clove Set، مجموعة «الفصوص»):**

```
+----+----+----+----+----+----+----+----+
| num| clove 1 (variable)               |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| clove 2 (variable)                    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate (3) | Message_ID (4)  |
+----+----+----+----+----+----+----+----+
    Expiration (8)                  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Number of GarlicCloves to follow

clove :: GarlicClove (see GarlicClove structure above)

Certificate :: Always NULL (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```

**بالنسبة لتنسيق ECIES-X25519-AEAD-Ratchet (المعيار الحالي لـ routers):**

راجع [مواصفة ECIES](/docs/specs/ecies/) و[المقترح 144](/proposals/144-ecies-x25519-aead-ratchet/).

**الشفرة المصدرية:** - `net.i2p.data.i2np.GarlicMessage` - التشفير: `net.i2p.crypto.elgamal.ElGamalAESEngine` (مهمل) - التشفير الحديث: `net.i2p.crypto.ECIES` حزم

---

### TunnelData (النوع 18)

**الغرض:** رسالة تُرسَل من بوابة الـtunnel أو أحد المشاركين فيه إلى المشارك التالي أو نقطة النهاية. البيانات ذات طول ثابت، وتحتوي على رسائل I2NP تكون مجزأة، ومجموعة على دفعات، ومضافًا إليها الحشو، ومشفَّرة.

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
| tunnelID (4)          | data (1024)   |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

data :: 1024 bytes
        Payload data, fixed to 1024 bytes
```
**بنية الحمولة (1024 بايت):**

```
Bytes 0-15: Initialization Vector (IV) for AES encryption
Bytes 16-1023: Encrypted tunnel message data (1008 bytes)
```
**ملاحظات:** - يتم تعيين معرّف رسالة I2NP لِـ TunnelData (رسالة بيانات النفق) إلى رقم عشوائي جديد عند كل قفزة - يتم تحديد تنسيق رسالة tunnel (ضمن البيانات المُشفَّرة) في [Tunnel Message Specification (مواصفات رسائل النفق)](/docs/specs/implementation/) - تفك كل قفزة طبقة واحدة باستخدام AES-256 في وضع CBC - يُحدَّث IV (مُتّجه التهيئة) عند كل قفزة باستخدام البيانات بعد فك التشفير - الحجم الإجمالي هو 1,028 بايت بالضبط (4 tunnelId + 1024 بيانات) - هذه هي الوحدة الأساسية لحركة مرور tunnel - تحمل رسائل TunnelData رسائل I2NP المُجزّأة (مثل GarlicMessage (رسالة Garlic) وDatabaseStore (تخزين قاعدة البيانات)، إلخ.)

**الشيفرة المصدرية:** - `net.i2p.data.i2np.TunnelDataMessage` - ثابت: `TunnelDataMessage.DATA_LENGTH = 1024` - المعالجة: `net.i2p.router.tunnel.InboundGatewayProcessor`

---

### TunnelGateway (بوابة الـ tunnel) (النوع 19)

**الغرض:** يغلف رسالة I2NP أخرى لإرسالها إلى tunnel عبر بوابة الدخول الخاصة به.

**التنسيق:**

```
+----+----+----+----+----+----+----+-//
| tunnelId (4)          | length (2)| data...
+----+----+----+----+----+----+----+-//

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

length :: 2 byte Integer
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**ملاحظات:** - الحمولة عبارة عن رسالة I2NP ذات ترويسة قياسية بطول 16 بايت - تُستخدم لحقن الرسائل في tunnels من الـ router المحلي - تقوم البوابة بتجزئة الرسالة المضمّنة عند الحاجة - بعد التجزئة، تُغلَّف الأجزاء داخل رسائل TunnelData - TunnelGateway لا يُرسَل مطلقًا عبر الشبكة؛ إنه نوع رسالة داخلي يُستخدَم قبل معالجة tunnel

**الشيفرة المصدرية:** - `net.i2p.data.i2np.TunnelGatewayMessage` - المعالجة: `net.i2p.router.tunnel.OutboundGatewayProcessor`

---

### DataMessage (رسالة بيانات) (النوع 20)

**الغرض:** تُستخدم من قِبَل Garlic Messages (رسائل Garlic) وGarlic Cloves (فصوص Garlic) لتغليف بيانات اعتباطية (عادةً بيانات تطبيق مُشفّرة من طرف إلى طرف).

**التنسيق:**

```
+----+----+----+----+----+----+-//-+
| length (4)            | data...    |
+----+----+----+----+----+----+-//-+

length :: 4 bytes
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**ملاحظات:** - لا تحتوي هذه الرسالة على أي معلومات التوجيه ولن يتم إرسالها مطلقاً "بدون تغليف" - لا يُستخدم إلا داخل Garlic messages (رسائل غارليك) - يحتوي عادةً على بيانات تطبيق مُشفّرة من طرف إلى طرف (HTTP وIRC والبريد الإلكتروني، إلخ) - تكون البيانات عادةً حمولة مُشفّرة بـ ElGamal/AES أو ECIES - أقصى طول عملي يبلغ نحو 61.2 KB بسبب قيود تجزئة رسائل tunnel

**الشيفرة المصدرية:** - `net.i2p.data.i2np.DataMessage`

---

### TunnelBuild (النوع 21)

**تم إهماله.** استخدم VariableTunnelBuild (النوع 23) أو ShortTunnelBuild (النوع 25).

**الغرض:** طلب إنشاء tunnel بطول ثابت لـ 8 قفزات.

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
| Record 0 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
Record size: 528 bytes
Total size: 8 × 528 = 4,224 bytes
```
**ملاحظات:** - اعتبارًا من 0.9.48، قد يحتوي على ECIES-X25519 BuildRequestRecords (سجلات طلب إنشاء باستخدام ECIES-X25519). راجع [ECIES Tunnel Creation](/docs/specs/implementation/) (إنشاء tunnel باستخدام ECIES) - راجع [Tunnel Creation Specification](/docs/specs/implementation/) (مواصفات إنشاء tunnel) للتفاصيل - يجب ضبط معرّف الرسالة I2NP لهذه الرسالة وفقًا لمواصفات إنشاء tunnel - على الرغم من ندرته في شبكة اليوم (تم استبداله بـ VariableTunnelBuild، بناء tunnel متغيّر)، لا يزال من الممكن استخدامه لـtunnels طويلة جدًا ولم يُعلن تقادمه رسميًا - Routers يجب أن تستمر في تنفيذ ذلك للتوافق - التنسيق الثابت المكوّن من 8 سجلات غير مرن ويهدر عرض النطاق الترددي لـtunnels الأقصر

**الشيفرة المصدرية:** - `net.i2p.data.i2np.TunnelBuildMessage` - ثابت: `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8`

---

### TunnelBuildReply (النوع 22)

**مهمل.** استخدم VariableTunnelBuildReply (رد بناء tunnel متغير) (النوع 24) أو OutboundTunnelBuildReply (رد بناء tunnel صادر) (النوع 26).

**الغرض:** ردّ إنشاء tunnel بطول ثابت لـ 8 قفزات.

**التنسيق:**

نفس التنسيق مثل TunnelBuildMessage (رسالة بناء tunnel)، مع BuildResponseRecords (سجلات استجابة البناء) بدلاً من BuildRequestRecords (سجلات طلب البناء).

```
Total size: 8 × 528 = 4,224 bytes
```
**ملاحظات:** - اعتبارًا من 0.9.48، قد يحتوي على ECIES-X25519 BuildResponseRecords (سجلات استجابة البناء). راجع [إنشاء Tunnel باستخدام ECIES](/docs/specs/implementation/) - راجع [مواصفات إنشاء Tunnel](/docs/specs/implementation/) للتفاصيل - يجب ضبط معرّف رسالة I2NP لهذه الرسالة وفقًا لمواصفات إنشاء Tunnel - على الرغم من أنه نادرًا ما يُرى في شبكة اليوم (استُبدل بـ VariableTunnelBuildReply (ردّ بناء Tunnel متغيّر))، لا يزال من الممكن استخدامه لـ tunnels طويلة جدًا ولم يُعلن تقادمه رسميًا - يجب على Routers الاستمرار في تنفيذ ذلك لضمان التوافق

**الشفرة المصدرية:** - `net.i2p.data.i2np.TunnelBuildReplyMessage`

---

### VariableTunnelBuild (النوع 23)

**الغرض:** إنشاء tunnel متغيّر الطول لعدد يتراوح بين 1 و8 قفزات. يدعم كِلا نوعَي routers: ElGamal وECIES-X25519.

**التنسيق:**

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords (variable)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildRequestRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**ملاحظات:** - اعتبارًا من 0.9.48، قد يحتوي على ECIES-X25519 BuildRequestRecords (سجلات طلب البناء). راجع [ECIES Tunnel Creation](/docs/specs/implementation/) - تم تقديمه في إصدار router 0.7.12 (2009) - قد لا يُرسَل إلى مشاركي الـ tunnel الأقدم من الإصدار 0.7.12 - راجع [Tunnel Creation Specification](/docs/specs/implementation/) للتفاصيل - يجب ضبط معرّف رسالة I2NP وفقًا لمواصفة إنشاء الـ tunnel - **العدد النموذجي للسجلات:** 4 (لـ tunnel من 4 قفزات) - **الحجم الإجمالي النموذجي:** 1 + (4 × 528) = 2,113 بايت - هذه هي رسالة بناء الـ tunnel القياسية لـ ElGamal routers - عادةً ما تستخدم ECIES routers ShortTunnelBuild (رسالة بناء Tunnel مختصرة، النوع 25) بدلًا من ذلك

**شفرة المصدر:** - `net.i2p.data.i2np.VariableTunnelBuildMessage`

---

### VariableTunnelBuildReply (النوع 24)

**الغرض:** رد بناء tunnel بطول متغير لـ 1-8 قفزات. يدعم كلا نوعي routers: ElGamal وECIES-X25519.

**التنسيق:**

نفس التنسيق مثل VariableTunnelBuildMessage، مع BuildResponseRecords بدلاً من BuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords (variable)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildResponseRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**ملاحظات:** - اعتبارًا من 0.9.48، قد يحتوي على ECIES-X25519 (مخطط تشفير قائم على المنحنى الإهليلجي X25519) BuildResponseRecords (سجلات استجابة البناء). انظر [إنشاء ECIES Tunnel](/docs/specs/implementation/) - تم تقديمه في إصدار router 0.7.12 (2009) - قد لا يتم إرساله إلى مشاركي tunnel قبل الإصدار 0.7.12 - انظر [مواصفة إنشاء Tunnel](/docs/specs/implementation/) للتفاصيل - يجب تعيين معرف رسالة I2NP وفقًا لمواصفة إنشاء tunnel - **العدد النموذجي للسجلات:** 4 - **الحجم الإجمالي النموذجي:** 2,113 بايت

**شفرة المصدر:** - `net.i2p.data.i2np.VariableTunnelBuildReplyMessage`

---

### ShortTunnelBuild (النوع 25)

**Purpose:** رسائل بناء tunnel قصيرة لـ ECIES-X25519 routers فقط. تم تقديمها في إصدار API 0.9.51 (الإصدار 1.5.0، أغسطس 2021). هذا هو المعيار الحالي لعمليات بناء ECIES tunnel.

**الصيغة:**

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords (var)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildRequestRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**ملاحظات:** - تم تقديمه في إصدار router 0.9.51 (الإصدار 1.5.0، أغسطس 2021) - قد لا يُرسَل إلى مشاركي tunnel قبل إصدار API (واجهة برمجة التطبيقات) 0.9.51 - انظر [ECIES Tunnel Creation](/docs/specs/implementation/) للمواصفة الكاملة (ECIES: نظام تشفير منحنى بيضاوي متكامل) - انظر [Proposal 157](/proposals/157-new-tbm/) للتبرير - **العدد المعتاد من السجلات:** 4 - **الحجم الإجمالي المعتاد:** 1 + (4 × 218) = 873 بايت - **توفير في عرض النطاق:** أصغر بنسبة 59% من VariableTunnelBuild (تنسيق بناء Tunnel متغيّر) (873 مقابل 2,113 بايت) - **فائدة في الأداء:** تتسع 4 سجلات قصيرة في رسالة tunnel واحدة؛ بينما يتطلب VariableTunnelBuild ثلاث رسائل tunnel - هذا هو الآن تنسيق بناء tunnel القياسي لـ ECIES-X25519 tunnels - تشتق السجلات المفاتيح عبر HKDF (وظيفة اشتقاق مفتاح مبنية على الهاش) بدلاً من تضمينها صراحةً

**الشيفرة المصدرية:** - `net.i2p.data.i2np.ShortTunnelBuildMessage` - الثابت: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

---

### OutboundTunnelBuildReply (النوع 26)

**الغرض:** مرسلة من نقطة النهاية الصادرة لـ tunnel جديد إلى المُنشئ. خاصة بـ ECIES-X25519 routers فقط. قُدِّمت في إصدار واجهة برمجة التطبيقات 0.9.51 (الإصدار 1.5.0، أغسطس 2021).

**التنسيق:**

نفس التنسيق مثل ShortTunnelBuildMessage, مع ShortBuildResponseRecords بدلاً من ShortBuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords (var)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildResponseRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**ملاحظات:** - تم تقديمه في إصدار router 0.9.51 (الإصدار 1.5.0، أغسطس 2021) - راجع [إنشاء Tunnel ECIES](/docs/specs/implementation/) للمواصفة الكاملة - **العدد النموذجي للسجلات:** 4 - **الحجم الإجمالي النموذجي:** 873 بايت - يُرسل هذا الرد من نقطة النهاية الصادرة (OBEP) إلى مُنشئ tunnel عبر tunnel صادر تم إنشاؤه حديثًا - يوفر تأكيدًا على أن جميع القفزات قبلت بناء tunnel

**الشيفرة المصدرية:** - `net.i2p.data.i2np.OutboundTunnelBuildReplyMessage`

---

## المراجع

### المواصفات الرسمية

- **[مواصفة I2NP](/docs/specs/i2np/)** - المواصفة الكاملة لتنسيق رسائل I2NP
- **[البُنى الشائعة](/docs/specs/common-structures/)** - أنواع البيانات والبُنى المستخدمة في جميع أنحاء I2P
- **[إنشاء Tunnel](/docs/specs/implementation/)** - إنشاء Tunnel باستخدام ElGamal (مهمل)
- **[إنشاء Tunnel بـ ECIES](/docs/specs/implementation/)** - إنشاء Tunnel باستخدام ECIES-X25519 (الحالي)
- **[رسالة Tunnel](/docs/specs/implementation/)** - تنسيق رسالة Tunnel وتعليمات التسليم
- **[مواصفة NTCP2](/docs/specs/ntcp2/)** - بروتوكول النقل عبر TCP
- **[مواصفة SSU2](/docs/specs/ssu2/)** - بروتوكول النقل عبر UDP
- **[مواصفة ECIES](/docs/specs/ecies/)** - تشفير ECIES-X25519-AEAD-Ratchet
- **[مواصفة التشفير](/docs/specs/cryptography/)** - بدائيات تشفير منخفضة المستوى
- **[مواصفة I2CP](/docs/specs/i2cp/)** - مواصفة بروتوكول العميل
- **[مواصفة Datagram](/docs/api/datagrams/)** - تنسيقات Datagram2 وDatagram3

### المقترحات

- **[الاقتراح 123](/proposals/123-new-netdb-entries/)** - مدخلات netDB جديدة (LeaseSet2, EncryptedLeaseSet, MetaLeaseSet)
- **[الاقتراح 144](/proposals/144-ecies-x25519-aead-ratchet/)** - تشفير ECIES-X25519-AEAD-Ratchet
- **[الاقتراح 154](/proposals/154-ecies-lookups/)** - استعلام قاعدة بيانات مُشفّر
- **[الاقتراح 156](/proposals/156-ecies-routers/)** - ECIES routers
- **[الاقتراح 157](/proposals/157-new-tbm/)** - رسائل إنشاء tunnel أصغر (تنسيق قصير)
- **[الاقتراح 159](/proposals/159-ssu2/)** - نقل SSU2
- **[الاقتراح 161](/ar/proposals/161-ri-dest-padding/)** - حشو قابل للضغط
- **[الاقتراح 163](/proposals/163-datagram2/)** - Datagram2 وDatagram3
- **[الاقتراح 167](/proposals/167-service-records/)** - معلمات سجل خدمة LeaseSet
- **[الاقتراح 168](/proposals/168-tunnel-bandwidth/)** - معلمات عرض النطاق لبناء tunnel
- **[الاقتراح 169](/proposals/169-pq-crypto/)** - تشفير هجين ما بعد الكم

### التوثيق

- **[التوجيه بالثوم](/docs/overview/garlic-routing/)** - تجميع الرسائل بطبقات
- **[ElGamal/AES](/docs/legacy/elgamal-aes/)** - مخطط تشفير مُهمل
- **[تنفيذ Tunnel](/docs/specs/implementation/)** - التجزئة والمعالجة
- **[قاعدة بيانات الشبكة](/docs/specs/common-structures/)** - جدول تجزئة موزع
- **[نقل NTCP2](/docs/specs/ntcp2/)** - مواصفة نقل TCP
- **[نقل SSU2](/docs/specs/ssu2/)** - مواصفة نقل UDP
- **[مقدمة تقنية](/docs/overview/tech-intro/)** - نظرة عامة على معمارية I2P

### الشفرة المصدرية

- **[مستودع Java I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)** - التنفيذ الرسمي بلغة Java
- **[مرآة GitHub](https://github.com/i2p/i2p.i2p)** - مرآة GitHub لـ Java I2P
- **[مستودع i2pd](https://github.com/PurpleI2P/i2pd)** - تنفيذ بلغة C++

### المواقع الرئيسية للشيفرة المصدرية

**Java I2P (i2pgit.org/I2P_Developers/i2p.i2p):** - `core/java/src/net/i2p/data/i2np/` - تنفيذات رسائل I2NP - `core/java/src/net/i2p/crypto/` - تنفيذات التشفير - `router/java/src/net/i2p/router/tunnel/` - معالجة tunnel - `router/java/src/net/i2p/router/transport/` - تنفيذات النقل

**الثوابت والقيم:** - `I2NPMessage.MAX_SIZE = 65536` - أقصى حجم لرسالة I2NP - `I2NPMessageImpl.HEADER_LENGTH = 16` - حجم الترويسة القياسي - `TunnelDataMessage.DATA_LENGTH = 1024` - حمولة رسالة Tunnel - `EncryptedBuildRecord.RECORD_SIZE = 528` - سجل بناء طويل - `ShortEncryptedBuildRecord.RECORD_SIZE = 218` - سجل بناء قصير - `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8` - الحد الأقصى للسجلات لكل عملية بناء

---

## الملحق أ: إحصاءات الشبكة والحالة الراهنة

### تركيبة الشبكة (اعتبارًا من أكتوبر 2025)


### الحد الأدنى لمتطلبات Router (الموجّه)

- **إصدار API:** 0.9.16+ (لتوافق EdDSA مع الشبكة)
- **الحد الأدنى الموصى به:** API 0.9.51+ (بُنى tunnel القصيرة بتقنية ECIES)
- **الحد الأدنى الحالي لـ floodfills:** API 0.9.58+ (إيقاف دعم router المعتمد على ElGamal)
- **متطلب قادم:** Java 17+ (اعتبارًا من الإصدار 2.11.0، ديسمبر 2025)

### متطلبات عرض النطاق الترددي

- **الحد الأدنى:** 128 KBytes/sec (علم N أو أعلى) لـ floodfill
- **الموصى به:** 256 KBytes/sec (علم O) أو أعلى
- **متطلبات floodfill:**
  - حد أدنى لعرض النطاق الترددي 128 KB/sec
  - مدة تشغيل مستقرة (>95% مُوصى بها)
  - زمن وصول منخفض (<500ms إلى الأقران)
  - اجتياز اختبارات الصحة (زمن قائمة الانتظار، تأخر المهام)

### إحصائيات Tunnel

- **الطول النموذجي لـ tunnel:** 3-4 قفزات
- **الحد الأقصى لطول الـ tunnel:** 8 قفزات (نظري، نادر الاستخدام)
- **العمر النموذجي لـ tunnel:** 10 دقائق
- **معدل نجاح بناء الـ tunnel:** أكثر من 85% لدى routers ذات اتصال جيد
- **صيغة رسالة بناء الـ tunnel:**
  - ECIES (نظام تشفير متكامل بالمنحنيات البيضوية) routers: ShortTunnelBuild (سجلات بحجم 218 بايت)
  - tunnels المختلطة: VariableTunnelBuild (سجلات بحجم 528 بايت)

### مقاييس الأداء

- **وقت بناء tunnel:** 1-3 ثانية (نموذجي)
- **الكمون من طرف إلى طرف:** 0.5-2 ثانية (نموذجي، 6-8 قفزات إجمالًا)
- **معدل النقل:** محدود بعرض نطاق tunnel (عادةً 10-50 KB/sec لكل tunnel)
- **أقصى حجم مخطط بيانات (datagram):** 10 KB موصى به (61.2 KB حد أقصى نظري)

---

## الملحق ب: الميزات المهملة والمحذوفة

### تمت إزالته بالكامل (لم يعد مدعومًا)

- **نقل NTCP** - أزيل في الإصدار 0.9.50 (مايو 2021)
- **نقل SSU v1** - أزيل من Java I2P في الإصدار 2.4.0 (ديسمبر 2023)
- **نقل SSU v1** - أزيل من i2pd في الإصدار 2.44.0 (نوفمبر 2022)
- **أنواع تواقيع RSA** - غير مسموح بها اعتبارا من API 0.9.28

### مهمل (مدعوم ولكن غير موصى به)

- **ElGamal (خوارزمية تشفير/توقيع) routers** - أُعلن تقادمها اعتباراً من API 0.9.58 (مارس 2023)
  - لا تزال وجهات ElGamal مدعومة لأغراض التوافق العكسي
  - يجب على routers الجديدة استخدام ECIES-X25519 (مخطط تشفير منحنيات إهليلجية باستخدام X25519) حصرياً
- **TunnelBuild (type 21)** - أُعلن تقادمه لصالح VariableTunnelBuild وShortTunnelBuild
  - ما زال مُنفّذاً من أجل tunnels الطويلة جداً (>8 قفزات)
- **TunnelBuildReply (type 22)** - أُعلن تقادمه لصالح VariableTunnelBuildReply وOutboundTunnelBuildReply
- **تشفير ElGamal/AES** - أُعلن تقادمه لصالح ECIES-X25519-AEAD-Ratchet
  - لا يزال مستخدماً للوجهات القديمة
- **سجلات طلب البناء ECIES الطويلة (528 بايت)** - أُعلن تقادمها لصالح التنسيق القصير (218 بايت)
  - لا تزال قيد الاستخدام في tunnels المختلطة ذات قفزات ElGamal

### الجدول الزمني لدعم الإصدارات القديمة

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Deprecated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2018 (0.9.36)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2021 (0.9.50)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by NTCP2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU v1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2022 (0.9.54)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (Java) / 2022 (i2pd)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by SSU2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal routers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (0.9.58)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations still supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017 (0.9.28)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Never widely used</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2009 (0.7.12)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Not removed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Still supported for long tunnels</td>
    </tr>
  </tbody>
</table>
---

## الملحق ج: التطورات المستقبلية

### التشفير ما بعد الكمّي

**الحالة:** نسخة تجريبية اعتبارًا من الإصدار 2.10.0 (سبتمبر 2025)، وستصبح الإعداد الافتراضي في 2.11.0 (ديسمبر 2025)

**التنفيذ:** - نهج هجين يجمع بين X25519 الكلاسيكي وخوارزمية ما بعد الكم MLKEM (ML-KEM-768) - متوافق رجعياً مع البنية التحتية الحالية ECIES-X25519 - يستخدم Signal Double Ratchet (خوارزمية «التدرّج المزدوج» من Signal) مع مادة المفتاح الكلاسيكية وPQ (ما بعد الكم) - راجع [Proposal 169](/proposals/169-pq-crypto/) للتفاصيل

**مسار الترحيل:** 1. الإصدار 2.10.0 (سبتمبر 2025): متاح كخيار تجريبي 2. الإصدار 2.11.0 (ديسمبر 2025): مفعل افتراضيًا 3. الإصدارات المستقبلية: سيصبح إلزاميًا لاحقًا

### الميزات المخطط لها

- **تحسينات IPv6** - دعم أفضل لـ IPv6 وآليات الانتقال
- **تقييد السرعة لكل tunnel** - تحكم دقيق في عرض النطاق الترددي لكل tunnel
- **مقاييس محسّنة** - مراقبة الأداء والتشخيص بشكل أفضل
- **تحسينات البروتوكول** - تقليل الحمولة الإضافية وتحسين الكفاءة
- **تحسين اختيار floodfill** - توزيع أفضل لقاعدة بيانات الشبكة

### مجالات البحث

- **تحسين طول Tunnel** - طول tunnel ديناميكي يعتمد على نموذج التهديد
- **حشو متقدم** - تحسينات في مقاومة تحليل حركة المرور
- **مخططات تشفير جديدة** - استعداد لتهديدات الحوسبة الكمّية
- **التحكم في الازدحام** - تعامل أفضل مع حمل الشبكة
- **دعم الأجهزة المحمولة** - تحسينات للأجهزة والشبكات المحمولة

---

## الملحق د: إرشادات التنفيذ

### للتنفيذات الجديدة

**الحد الأدنى من المتطلبات:** 1. دعم ميزات API الخاصة بالإصدار 0.9.51+ 2. تنفيذ تشفير ECIES-X25519-AEAD-Ratchet (مخطط تشفير مع آلية ratchet يعتمد X25519 وAEAD) 3. دعم بروتوكولات النقل NTCP2 وSSU2 4. تنفيذ رسائل ShortTunnelBuild (رسائل بناء tunnel مختصرة) (سجلات بحجم 218 بايت) 5. دعم متغيرات LeaseSet2 (الأنواع 3 و5 و7) 6. استخدام تواقيع EdDSA (Ed25519؛ خوارزمية توقيع بمنحنيات بيضوية)

**موصى به:** 1. دعم التشفير الهجين بعد الكم (اعتباراً من 2.11.0) 2. تنفيذ معلمات عرض النطاق الترددي لكل tunnel 3. دعم تنسيقات Datagram2 وDatagram3 4. تنفيذ خيارات سجل الخدمة في LeaseSets 5. اتّباع المواصفات الرسمية على /docs/specs/

**غير مطلوب:** 1. دعم ElGamal router (مُهمل) 2. دعم النقل القديم (SSU1, NTCP) 3. BuildRequestRecords (سجلات طلب البناء) طويلة لـ ECIES (528 بايت لـ ECIES tunnels الخالصة) 4. رسائل TunnelBuild/TunnelBuildReply (استخدم المتغيرات Variable أو Short)

### الاختبار والتحقق من الصحة

**الامتثال للبروتوكول:** 1. اختبار قابلية التشغيل البيني مع I2P router الرسمي المكتوب بلغة Java 2. اختبار قابلية التشغيل البيني مع i2pd C++ router 3. التحقق من صحة تنسيقات الرسائل وفقًا للمواصفات 4. اختبار دورات إنشاء/تفكيك tunnel 5. التحقق من التشفير/فك التشفير باستخدام متجهات الاختبار

**اختبار الأداء:** 1. قياس معدلات نجاح بناء tunnel (يجب أن تكون >85%) 2. الاختبار بأطوال tunnel مختلفة (2-8 قفزات) 3. التحقق من صحة التجزئة وإعادة التجميع 4. الاختبار تحت الحمل (tunnels متعددة ومتزامنة) 5. قياس زمن الوصول من طرف إلى طرف

**اختبارات الأمان:** 1. التحقق من تنفيذ التشفير (استخدم متجهات الاختبار) 2. اختبار منع هجمات إعادة الإرسال 3. التحقق من صحة معالجة انتهاء صلاحية الرسائل 4. الاختبار ضد الرسائل سيئة التشكيل 5. التحقق من سلامة توليد الأرقام العشوائية

### مزالق التنفيذ الشائعة

1. **تنسيقات تعليمات التسليم المربكة** - Garlic clove (رسالة فرعية ضمن garlic encryption) مقابل رسالة tunnel
2. **اشتقاق المفاتيح غير الصحيح** - استخدام HKDF لسجلات البناء القصيرة
3. **معالجة معرّف الرسالة** - عدم ضبطه بشكل صحيح لعمليات بناء tunnel
4. **مشكلات التجزئة** - عدم احترام الحد العملي البالغ 61.2 KB
5. **أخطاء ترتيب البايتات (Endianness)** - Java تستخدم big-endian (الأكثر أهمية أولاً) لجميع الأعداد الصحيحة
6. **التعامل مع تاريخ الانتهاء** - التنسيق القصير يلتف في 7 فبراير 2106
7. **توليد المجموع الاختباري (Checksum)** - لا يزال مطلوبًا حتى إن لم يُتحقَّق منه
