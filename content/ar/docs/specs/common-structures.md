---
title: "مواصفات الهياكل الشائعة"
description: "أنواع البيانات المشتركة لجميع بروتوكولات I2P"
slug: "common-structures"
aliases:
  - "/docs/specs/common-structures"
  - "/docs/specs/common-structures/"
category: "التصميم"
lastUpdated: "2026-10"
accurateFor: "0.9.71"
---

تصف هذه الوثيقة بعض أنواع البيانات الشائعة لجميع بروتوكولات I2P، مثل [I2NP](/docs/specs/i2np/)، و[I2CP](/docs/specs/i2cp/)، و[SSU](/docs/legacy/ssu/)، إلخ.

## مواصفة النوع العام

### عدد صحيح

#### الوصف

يمثل عدد صحيح غير سالب.

#### المحتويات

من 1 إلى 8 بايت بترتيب بايت الشبكة (big endian) تمثل عدد صحيح غير مُوقع.

### التاريخ

#### الوصف

عدد المللي ثانية منذ منتصف الليل في 1 يناير 1970 بتوقيت GMT. إذا كان الرقم 0، فإن التاريخ غير محدد أو فارغ.

#### المحتويات

8 بايت [Integer](#integer)

### نص

#### الوصف

يمثل سلسلة نصية مُرمزة بتشفير UTF-8.

#### المحتويات

بايت واحد أو أكثر حيث البايت الأول هو عدد البايتات (وليس الأحرف!) في السلسلة النصية والبايتات المتبقية من 0-255 هي مصفوفة الأحرف المُرمزة بـ UTF-8 غير المنتهية بقيمة فارغة. الحد الأقصى للطول هو 255 بايت (وليس أحرف). قد يكون الطول 0.

### PublicKey

#### الوصف

تُستخدم هذه البنية في التشفير غير المتماثل ElGamal أو غيره، وتمثل الأس فقط وليس الأعداد الأولية، والتي هي ثابتة ومُعرَّفة في مواصفات التشفير [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy). خطط التشفير الأخرى في طور التعريف، انظر الجدول أدناه.

#### المحتويات

يتم استنتاج نوع المفتاح وطوله من السياق أو يتم تحديدهما في شهادة المفتاح الخاصة بوجهة أو RouterInfo، أو الحقول في [LeaseSet2](#leaseset2) أو هيكل بيانات آخر. النوع الافتراضي هو ElGamal. اعتباراً من الإصدار 0.9.38، قد يتم دعم أنواع أخرى، حسب السياق. المفاتيح هي big-endian ما لم يُذكر خلاف ذلك.

مفاتيح X25519 مدعومة في Destinations و LeaseSet2 اعتباراً من الإصدار 0.9.44. مفاتيح X25519 مدعومة في RouterIdentities اعتباراً من الإصدار 0.9.48.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there; discouraged for leasesets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Little-endian. See <a href="/docs/specs/ecies/">ECIES</a> and <a href="/docs/specs/ecies-routers/">ECIES-ROUTERS</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.PublicKey](http://docs.i2p-projekt.de/net/i2p/data/PublicKey.html)

### المفتاح الخاص

#### الوصف

يتم استخدام هذه البنية في ElGamal أو طرق فك التشفير غير المتماثلة الأخرى، حيث تمثل الأس فقط وليس الأعداد الأولية التي تكون ثابتة ومحددة في مواصفات التشفير [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy). مخططات التشفير الأخرى في طور التعريف، انظر الجدول أدناه.

#### المحتويات

يتم استنتاج نوع المفتاح وطوله من السياق أو يتم تخزينهما بشكل منفصل في هيكل بيانات أو ملف مفتاح خاص. النوع الافتراضي هو ElGamal. اعتباراً من الإصدار 0.9.38، قد يتم دعم أنواع أخرى، حسب السياق. المفاتيح تكون big-endian ما لم يُذكر خلاف ذلك.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there; discouraged for leasesets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">66</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Little-endian. See <a href="/docs/specs/ecies/">ECIES</a> and <a href="/docs/specs/ecies-routers/">ECIES-ROUTERS</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1632</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2400</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3168</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.PrivateKey](http://docs.i2p-projekt.de/net/i2p/data/PrivateKey.html)

### SessionKey

#### الوصف

يتم استخدام هذا الهيكل للتشفير وفك التشفير المتماثل باستخدام AES256.

#### المحتويات

32 بايت

JavaDoc: [net.i2p.data.SessionKey](http://docs.i2p-projekt.de/net/i2p/data/SessionKey.html)

### SigningPublicKey

#### الوصف

تُستخدم هذه البنية للتحقق من التوقيعات.

#### المحتويات

يتم استنتاج نوع المفتاح وطوله من السياق أو يتم تحديدهما في شهادة المفتاح الخاصة بوجهة معينة. النوع الافتراضي هو DSA_SHA1. اعتباراً من الإصدار 0.9.12، قد يتم دعم أنواع أخرى، اعتماداً على السياق.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### ملاحظات

* عندما يتكون مفتاح من عنصرين (على سبيل المثال النقاط X,Y)، يتم تسلسله عبر حشو كل عنصر إلى length/2 بأصفار بادئة إذا لزم الأمر.

* جميع الأنواع تستخدم ترتيب Big Endian، باستثناء EdDSA و RedDSA، والتي يتم تخزينها ونقلها بتنسيق Little Endian.

JavaDoc: [net.i2p.data.SigningPublicKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPublicKey.html)

### SigningPrivateKey

#### الوصف

تُستخدم هذه البنية لإنشاء التوقيعات.

#### المحتويات

يتم تحديد نوع المفتاح وطوله عند إنشائه. النوع الافتراضي هو DSA_SHA1. اعتباراً من الإصدار 0.9.12، قد يتم دعم أنواع أخرى، حسب السياق.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">66</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### ملاحظات

* عندما يتكون مفتاح من عنصرين (على سبيل المثال النقاط X,Y)، يتم تسلسله عبر حشو كل عنصر إلى length/2 مع أصفار بادئة إذا لزم الأمر.

* جميع الأنواع تستخدم ترتيب البايت الكبير (Big Endian)، باستثناء EdDSA و RedDSA، والتي يتم تخزينها ونقلها بتنسيق ترتيب البايت الصغير (Little Endian).

JavaDoc: [net.i2p.data.SigningPrivateKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPrivateKey.html)

### التوقيع

#### الوصف

تمثل هذه البنية توقيع بعض البيانات.

#### المحتويات

يتم استنتاج نوع التوقيع وطوله من نوع المفتاح المستخدم. النوع الافتراضي هو DSA_SHA1. اعتبارًا من الإصدار 0.9.12، قد يتم دعم أنواع أخرى، اعتمادًا على السياق.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### ملاحظات

* عندما يتكون التوقيع من عنصرين (على سبيل المثال القيم R,S)، يتم تسلسله عبر حشو كل عنصر إلى length/2 بأصفار بادئة إذا لزم الأمر.

* جميع الأنواع تستخدم ترتيب البايت الكبير (Big Endian)، باستثناء EdDSA و RedDSA، والتي يتم تخزينها ونقلها بتنسيق ترتيب البايت الصغير (Little Endian).

JavaDoc: [net.i2p.data.Signature](http://docs.i2p-projekt.de/net/i2p/data/Signature.html)

### التجميع

#### الوصف

يمثل SHA256 لبعض البيانات.

#### المحتويات

32 بايت

JavaDoc: [net.i2p.data.Hash](http://docs.i2p-projekt.de/net/i2p/data/Hash.html)

### علامة الجلسة

ملاحظة: Session Tags لوجهات ECIES-X25519 (ratchet) وrouters ECIES-X25519 هي 8 بايت. راجع [ECIES](/docs/specs/ecies/) و [ECIES-ROUTERS](/docs/specs/ecies-routers/).

#### الوصف

رقم عشوائي

#### المحتويات

32 بايت

JavaDoc: [net.i2p.data.SessionTag](http://docs.i2p-projekt.de/net/i2p/data/SessionTag.html)

### TunnelId

#### الوصف

يحدد معرفاً فريداً لكل router في tunnel. معرف Tunnel ID عادة ما يكون أكبر من الصفر؛ لا تستخدم قيمة الصفر إلا في حالات خاصة.

#### المحتويات

4 بايت [Integer](#integer)

JavaDoc: [net.i2p.data.TunnelId](http://docs.i2p-projekt.de/net/i2p/data/TunnelId.html)

### الشهادة

#### الوصف

الشهادة هي حاوية لمختلف الإيصالات أو إثباتات العمل المستخدمة عبر شبكة I2P.

#### المحتويات

1 بايت [عدد صحيح](#integer) يحدد نوع الشهادة، متبوعًا بـ 2 بايت [عدد صحيح](#integer) يحدد حجم حمولة الشهادة، ثم ذلك العدد من البايتات.

```
+----+----+----+----+----+-/
|type| length  | payload
+----+----+----+----+----+-/

type :: Integer
        length -> 1 byte

length :: Integer
          length -> 2 bytes

payload :: data
           length -> $length bytes
```
#### ملاحظات

* بالنسبة لـ [Router Identities](#routeridentity)، تكون الشهادة دائماً NULL حتى الإصدار 0.9.15. اعتباراً من 0.9.16، يتم استخدام Key Certificate لتحديد أنواع المفاتيح. اعتباراً من 0.9.48، يُسمح بأنواع المفاتيح العامة للتشفير X25519. انظر أدناه.

* بالنسبة لـ [Garlic Cloves](/docs/specs/i2np/#struct-garlicclove)، تكون الشهادة دائماً NULL، ولا توجد أنواع أخرى مُنفذة حالياً.

* بالنسبة لـ [Garlic Messages](/docs/specs/i2np/#msg-garlic)، تكون الشهادة دائماً NULL، ولا يوجد أي تطبيقات أخرى حالياً.

* بالنسبة لـ [Destinations](#destination)، قد تكون الشهادة غير فارغة (non-NULL). اعتباراً من الإصدار 0.9.12، يمكن استخدام شهادة مفتاح لتحديد نوع المفتاح العام للتوقيع. انظر أدناه.

* يُحذر المطورون من السماح بوجود بيانات زائدة في الشهادات.
  يجب فرض الطول المناسب لكل نوع من أنواع الشهادات.

#### أنواع الشهادات

أنواع الشهادات التالية معرّفة:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Null</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HashCash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains an ASCII colon-separated hashcash string.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Hidden routers generally do not announce that they are hidden.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40 or 72</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">43 or 75</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains a 40-byte DSA signature, optionally followed by the 32-byte Hash of the signing Destination.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains multiple certificates.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 0.9.12. See below for details.</td>
    </tr>
  </tbody>
</table>
#### شهادات المفاتيح

تم تقديم شهادات المفاتيح في الإصدار 0.9.12. قبل ذلك الإصدار، كانت جميع PublicKeys هي مفاتيح ElGamal بحجم 256 بايت، وجميع SigningPublicKeys كانت مفاتيح DSA-SHA1 بحجم 128 بايت. توفر شهادة المفتاح آلية للإشارة إلى نوع PublicKey و SigningPublicKey في Destination أو RouterIdentity، ولتعبئة أي بيانات مفتاح تتجاوز الأطوال المعيارية.

من خلال الحفاظ على 384 بايت بالضبط قبل الشهادة، ووضع أي بيانات مفاتيح إضافية داخل الشهادة، نحافظ على التوافق مع أي برامج تقوم بتحليل الوجهات وهويات الـ router.

حمولة شهادة المفتاح تحتوي على:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Data</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signing Public Key Type (<a href="#integer">Integer</a>)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Crypto Public Key Type (<a href="#integer">Integer</a>)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Excess Signing Public Key Data</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0+</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Excess Crypto Public Key Data</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0+</td>
    </tr>
  </tbody>
</table>
تحذير: ترتيب أنواع المفاتيح عكس ما قد تتوقعه؛ نوع المفتاح العام للتوقيع يأتي أولاً.

أنواع مفاتيح التوقيع العامة المُعرّفة هي:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Public Key Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely if ever used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely if ever used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (GOST)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/134-gost/">Prop134</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (GOST)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/134-gost/">Prop134</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only; never used for Router Identities</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65280-65534</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for experimental use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for future expansion</td>
    </tr>
  </tbody>
</table>
أنواع مفاتيح التشفير العامة المحددة هي:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Public Key Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies/">ECIES</a> and proposal 156</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (NONE)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65280-65534</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for experimental use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for future expansion</td>
    </tr>
  </tbody>
</table>
عندما لا تكون شهادة المفتاح (Key Certificate) موجودة، يتم تعريف الـ 384 بايت السابقة في الوجهة (Destination) أو هوية الموجه (RouterIdentity) كمفتاح عام ElGamal بحجم 256 بايت يتبعه مفتاح التوقيع العام DSA-SHA1 بحجم 128 بايت. عندما تكون شهادة المفتاح موجودة، يتم إعادة تعريف الـ 384 بايت السابقة كما يلي:

* كامل أو الجزء الأول من المفتاح العام المشفر

* حشو عشوائي إذا كان إجمالي أطوال المفتاحين أقل من 384 بايت

* الجزء الكامل أو الأول من مفتاح التوقيع العام

يتم محاذاة المفتاح العام للتشفير في البداية ويتم محاذاة المفتاح العام للتوقيع في النهاية. الحشو (إن وُجد) يكون في المنتصف. أطوال وحدود بيانات المفتاح الأولية، والحشو، وأجزاء بيانات المفتاح الزائدة في الشهادات غير محددة بشكل صريح، ولكنها مُشتقة من أطوال أنواع المفاتيح المحددة. إذا تجاوز إجمالي أطوال المفاتيح العامة للتشفير والتوقيع 384 بايت، فسيتم احتواء الباقي في شهادة المفتاح. إذا لم يكن طول المفتاح العام للتشفير 256 بايت، فإن الطريقة لتحديد الحد الفاصل بين المفتاحين ستكون محددة في مراجعة مستقبلية لهذا المستند.

أمثلة على التخطيطات باستخدام مفتاح ElGamal العام للتشفير ونوع مفتاح التوقيع العام المحدد:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Padding Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Excess Signing Key Data in Cert</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.Certificate](http://docs.i2p-projekt.de/net/i2p/data/Certificate.html)

#### ملاحظات

* يُحذر المطورون من السماح بوجود بيانات زائدة في شهادات المفاتيح (Key Certificates).
  يجب فرض الطول المناسب لكل نوع من أنواع الشهادات.

* شهادة KEY مع الأنواع 0,0 (ElGamal,DSA_SHA1) مسموحة ولكن غير مستحبة.
  لم يتم اختبارها جيداً وقد تسبب مشاكل في بعض التطبيقات.
  استخدم شهادة NULL في التمثيل القانوني لـ
  Destination أو RouterIdentity من نوع (ElGamal,DSA_SHA1)، والذي سيكون أقصر بـ 4 بايتات
  من استخدام شهادة KEY.

### الربط

#### الوصف

مجموعة من تعيينات المفتاح/القيمة أو الخصائص

#### المحتويات

عدد صحيح بحجم 2 بايت متبوع بسلسلة من أزواج String=String;

تحذير: معظم استخدامات Mapping تكون في هياكل موقعة، حيث يجب ترتيب إدخالات Mapping حسب المفتاح، بحيث يكون التوقيع غير قابل للتغيير. عدم الترتيب حسب المفتاح سيؤدي إلى فشل التوقيع!

```bytefield
size       | 4 | red    | Integer, 2 bytes
key_string | 4 | blue   | String (len + data)
val_string | 8 | green  | String (len + data)
;          | 8 | yellow | :: A single byte containing ';'
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+
```
</details>
#### ملاحظات

* التشفير ليس الأمثل - نحتاج إما إلى أحرف '=' و ';'، أو إلى أطوال السلاسل النصية، ولكن ليس كلاهما

#### الوصف

* تشير بعض الوثائق إلى أن السلاسل النصية قد لا تتضمن '=' أو ';' ولكن هذا التشفير يدعمها

* السلاسل النصية معرّفة لتكون UTF-8 ولكن في التطبيق الحالي، I2CP يستخدم UTF-8 بينما I2NP لا يفعل ذلك. على سبيل المثال، سلاسل UTF-8 النصية في تخطيط خيارات RouterInfo في رسالة I2NP Database Store ستتعرض للتلف.

* يسمح الترميز بالمفاتيح المكررة، ومع ذلك في أي استخدام يكون فيه التعيين موقعاً، قد تتسبب المكررات في فشل التوقيع.

* التخطيطات المتضمنة في رسائل I2NP (مثل في RouterAddress أو RouterInfo)
  يجب أن تكون مرتبة حسب المفتاح بحيث يكون التوقيع ثابتاً. المفاتيح المكررة
  غير مسموحة.

* التطابقات الموجودة في [I2CP SessionConfig](/docs/specs/i2cp/#struct-sessionconfig) يجب أن تُرتب حسب المفتاح بحيث يكون التوقيع ثابتاً. المفاتيح المكررة غير مسموحة.

* يتم تعريف طريقة الترتيب كما في Java String.compareTo()، باستخدام قيمة Unicode للأحرف.

* رغم أن الأمر يعتمد على التطبيق، إلا أن المفاتيح والقيم حساسة للأحرف الكبيرة والصغيرة بشكل عام.

* حدود أطوال سلاسل المفتاح والقيمة هي 255 بايت (وليس حرف) لكل منهما، بالإضافة إلى بايت الطول. قد يكون بايت الطول 0.

* حد الطول الإجمالي هو 65535 بايت، بالإضافة إلى حقل الحجم المكون من 2 بايت، أو 65537 إجمالي.

* هوية Router مع نوع تشفير X25519 ونوع توقيع Ed25519
  ستحتوي على 10 نسخ (320 بايت) من البيانات العشوائية، لتوفير حوالي 288 بايت عند الضغط.

JavaDoc: [net.i2p.data.DataHelper](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)

## مواصفات الهيكل المشترك

### KeysAndCert

#### المحتويات

مفتاح تشفير عام، ومفتاح توقيع عام، وشهادة، تُستخدم إما كـ RouterIdentity أو Destination.

#### إرشادات توليد الحشو

[PublicKey](#publickey) متبوع بـ [SigningPublicKey](#signingpublickey) ثم [Certificate](#certificate).

```bytefield
public_key          | 8 | blue   | PublicKey (partial or full), 256 bytes or as specified in key cert

padding (optional)  | 8 | yellow | random data, pub + pad + sig == 384 bytes

signing_key         | 8 | green  | SigningPublicKey (partial or full), 128 bytes or as specified

certificate         | 3 | purple | Certificate, >= 3 bytes
= total length: 387+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-/

public_key :: `PublicKey` (partial or full)
              length -> 256 bytes or as specified in key certificate

padding :: random data
           length -> 0 bytes or as specified in key certificate
           public_key length + padding length + signing_key length == 384 bytes

signing__key :: `SigningPublicKey` (partial or full)
                length -> 128 bytes or as specified in key certificate

certificate :: `Certificate`
               length -> >= 3 bytes

total length: 387+ bytes
```

</details>
#### ملاحظات

تم اقتراح هذه الإرشادات في الاقتراح 161 وتم تنفيذها في إصدار API 0.9.57. هذه الإرشادات متوافقة مع الإصدارات السابقة مع جميع الإصدارات منذ 0.6 (2005). راجع الاقتراح 161 للحصول على معلومات أساسية وتفاصيل إضافية.

لأي مجموعة مستخدمة حالياً من أنواع المفاتيح غير ElGamal + DSA-SHA1، ستكون هناك حشوة. بالإضافة إلى ذلك، بالنسبة للوجهات، فإن حقل المفتاح العام بحجم 256 بايت لم يعد مستخدماً منذ الإصدار 0.6 (2005).

يجب على المطورين توليد البيانات العشوائية لمفاتيح Destination العامة، وحشو Destination و Router Identity، بحيث تكون قابلة للضغط في بروتوكولات I2P المختلفة مع الحفاظ على الأمان، ودون أن تبدو تمثيلات Base 64 تالفة أو غير آمنة. هذا يوفر معظم فوائد إزالة حقول الحشو دون أي تغييرات مدمرة في البروتوكول.

بشكل دقيق، فإن مفتاح التوقيع العام المكون من 32 بايت وحده (في كل من Destinations و Router Identities) ومفتاح التشفير العام المكون من 32 بايت (في Router Identities فقط) هو رقم عشوائي يوفر كل الإنتروبيا اللازمة لجعل hashes SHA-256 لهذه الهياكل قوية تشفيرياً وموزعة عشوائياً في DHT قاعدة بيانات الشبكة.

ومع ذلك، من باب الحذر الشديد، نوصي باستخدام حد أدنى 32 بايت من البيانات العشوائية في حقل المفتاح العام ElG والحشو. بالإضافة إلى ذلك، إذا كانت جميع الحقول تحتوي على أصفار، فإن وجهات Base 64 ستحتوي على تسلسلات طويلة من أحرف AAAA، مما قد يسبب القلق أو الالتباس للمستخدمين.

كرر الـ 32 بايت من البيانات العشوائية حسب الحاجة بحيث يكون هيكل KeysAndCert الكامل قابلاً للضغط بدرجة عالية في بروتوكولات I2P مثل I2NP Database Store Message و Streaming SYN و SSU2 handshake و repliable Datagrams.

أمثلة:

* وجهة بنوع توقيع Ed25519
  ستحتوي على 11 نسخة (352 بايت) من البيانات العشوائية، مما يوفر حوالي 320 بايت عند الضغط.

* لا تفترض أن هذه دائماً 387 بايت! إنها 387 بايت بالإضافة إلى طول الشهادة المحدد في البايتات 385-386، والذي قد يكون غير صفر.

يجب على التطبيقات، بطبيعة الحال، تخزين الهيكل الكامل المكون من 387+ بايت لأن hash SHA-256 للهيكل يغطي المحتويات الكاملة.

#### الوصف

* اعتباراً من الإصدار 0.9.12، إذا كانت الشهادة هي Key Certificate، فقد تختلف حدود حقول المفاتيح. راجع قسم Key Certificate أعلاه للتفاصيل.

* يتم محاذاة المفتاح العام للتشفير في البداية ويتم محاذاة المفتاح العام للتوقيع في النهاية. الحشو (إن وجد) يكون في المنتصف.

* كان الشهادة لـ RouterIdentity دائماً NULL حتى الإصدار 0.9.12.

JavaDoc: [net.i2p.data.KeysAndCert](http://docs.i2p-projekt.de/net/i2p/data/KeysAndCert.html)

### RouterIdentity

#### المحتويات

يحدد الطريقة لتعريف router معين بشكل فريد

#### ملاحظات

مطابق لـ KeysAndCert.

انظر [KeysAndCert](#keysandcert) للحصول على إرشادات حول إنتاج البيانات العشوائية لحقل الحشو.

#### الوصف

* لا تفترض أن هذه دائماً 387 بايت! إنها 387 بايت بالإضافة إلى طول الشهادة المحدد في البايتات 385-386، والذي قد يكون غير صفري.

* اعتباراً من الإصدار 0.9.12، إذا كانت الشهادة هي Key Certificate، فقد تختلف حدود حقول المفاتيح. راجع قسم Key Certificate أعلاه للحصول على التفاصيل.

* المفتاح العام للتشفير محاذي في البداية والمفتاح العام للتوقيع محاذي في النهاية. الحشو (إن وجد) يكون في المنتصف.

* RouterIdentities مع شهادة مفتاح ومفتاح عام ECIES_X25519
  مدعومة اعتباراً من الإصدار 0.9.48.
  قبل ذلك، كانت جميع RouterIdentities من نوع ElGamal.

* تم استخدام المفتاح العام للوجهة في التشفير القديم من i2cp إلى i2cp والذي تم تعطيله في الإصدار 0.6 (2005)، وهو حالياً غير مستخدم باستثناء IV لتشفير LeaseSet، والذي أصبح مهجوراً. يتم استخدام المفتاح العام في LeaseSet بدلاً من ذلك.

JavaDoc: [net.i2p.data.router.RouterIdentity](http://docs.i2p-projekt.de/net/i2p/data/router/RouterIdentity.html)

### الوجهة

#### المحتويات

يُعرّف الـ Destination نقطة نهاية معينة يمكن توجيه الرسائل إليها للتسليم الآمن.

#### ملاحظات

مطابق لـ [KeysAndCert](#keysandcert)، باستثناء أن المفتاح العام لا يُستخدم أبداً، وقد يحتوي على بيانات عشوائية بدلاً من مفتاح ElGamal عام صحيح.

انظر [KeysAndCert](#keysandcert) للحصول على إرشادات حول توليد البيانات العشوائية لحقول المفتاح العام والحشو.

#### الوصف

* لا تفترض أن هذه دائماً 387 بايت! إنها 387 بايت بالإضافة إلى طول الشهادة المحدد في البايتات 385-386، والذي قد يكون غير صفر.

* اعتباراً من الإصدار 0.9.12، إذا كانت الشهادة هي Key Certificate، فقد تختلف حدود حقول المفتاح. راجع قسم Key Certificate أعلاه للحصول على التفاصيل.

* المفتاح العام للتشفير محاذٍ في البداية والمفتاح العام للتوقيع محاذٍ في النهاية. الحشو (إن وُجد) يكون في المنتصف.

* تم استخدام المفتاح العام للوجهة في التشفير القديم من I2CP إلى I2CP والذي تم تعطيله في الإصدار 0.6، وهو حالياً غير مستخدم.

JavaDoc: [net.i2p.data.Destination](http://docs.i2p-projekt.de/net/i2p/data/Destination.html)

### عقد الإيجار

#### المحتويات

مُهمل. استخدم LeaseSet2 و Lease2.

يُعرِّف الصلاحية الخاصة بقناة معينة لتلقي الرسائل المستهدفة إلى [وجهة](#destination).

#### الوصف

دالة التجزئة SHA256 [Hash](#hash) الخاصة بهوية الموجه [RouterIdentity](#routeridentity) للموجه البوابة، ثم المعرف الخاص بالأنبوب [TunnelId](#tunnelid)، وأخيرًا التاريخ النهائي [Date](#date).

```bytefield
tunnel_gw   | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes

tunnel_id   | 4 | green  | TunnelId, 4 bytes
end_date    | 4 | yellow | Date, 8 bytes

= Total size 44 bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway
             length -> 32 bytes

tunnel_id :: `TunnelId`
             length -> 4 bytes

end_date :: `Date`
            length -> 8 bytes
```

</details>
JavaDoc: [net.i2p.data.Lease](http://docs.i2p-projekt.de/net/i2p/data/Lease.html)

### LeaseSet

#### المحتويات

مُهمل. استخدم LeaseSet2 و Lease2.

يحتوي على جميع [الإيجارات](#lease) المصرح بها حاليًا لـ [وجهة](#destination) معينة، و[مفتاح العمومي](#publickey) الذي يمكن تشفير رسائل الثوم (garlic) إليه، ثم [مفتاح التوقيع العمومي](#signingpublickey) الذي يمكن استخدامه لإلغاء هذا الإصدار المحدد من الهيكل. يُعدّ "LeaseSet" أحد الهيكلَين المخزَّنين في قاعدة بيانات الشبكة (والهيكل الآخر هو [RouterInfo](#routerinfo))، ويُفتَّح باستخدام دالة التجزئة SHA256 للـ[وجهة](#destination) المحتواة فيه.

#### ملاحظات

[Destination](#destination)، متبوعًا بـ [PublicKey](#publickey) للتشفير، ثم [SigningPublicKey](#signingpublickey) والذي يمكن استخدامه لإلغاء هذا الإصدار من LeaseSet، ثم 1 بايت [Integer](#integer) يحدد كم عدد هياكل [Lease](#lease) الموجودة في المجموعة، متبوعة بهياكل [Lease](#lease) الفعلية وأخيرًا [Signature](#signature) للبايتات السابقة موقعة بواسطة [SigningPrivateKey](#signingprivatekey) الخاص بـ [Destination](#destination).

```bytefield
destination     | 8 | blue   | Destination, >= 387+ bytes
encryption_key  | 8 | green  | PublicKey, 256 bytes
signing_key     | 8 | cyan   | SigningPublicKey, 128 bytes or as specified in destination's key cert
num             | 1 | red    | Integer, 1 byte, number of leases (0-16)
Lease 0         | 7 | yellow | Lease, 44 bytes
Lease 1         | 8 | yellow | Lease, 44 bytes
Lease ($num-1)  | 8 | yellow | Lease, 44 bytes
signature       | 8 | purple | Signature, 40 bytes or as specified in destination's key cert

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: `Destination`
               length -> >= 387+ bytes

encryption_key :: `PublicKey`
                  length -> 256 bytes

signing_key :: `SigningPublicKey`
               length -> 128 bytes or as specified in destination's key
                         certificate

num :: `Integer`
       length -> 1 byte
       Number of leases to follow
       value: 0 <= num <= 16

leases :: [`Lease`]
          length -> $num*44 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate
```

</details>
#### الوصف

* يتم استخدام مفتاح التشفير للتشفير الشامل من طرف إلى طرف ElGamal/AES+SessionTag
  [ELGAMAL-AES](/docs/specs/elgamal-aes/). يتم حالياً إنشاؤه من جديد عند كل بدء تشغيل للموجه، وهو غير مستمر.

* يمكن التحقق من التوقيع باستخدام المفتاح العام للتوقيع الخاص بالوجهة.

* يُسمح بـ LeaseSet بدون أي Leases ولكنه غير مستخدم.
  كان مخصصاً لإلغاء LeaseSet، والذي لم يتم تنفيذه.
  جميع متغيرات LeaseSet2 تتطلب Lease واحد على الأقل.

* إن signing_key غير مستخدم حالياً. كان مخصصاً لإلغاء LeaseSet، والذي لم يتم تنفيذه. يتم حالياً إنشاؤه من جديد عند كل بدء تشغيل للـ router، وهو غير دائم. نوع signing key هو دائماً نفس نوع signing key الخاص بالوجهة.

* يتم التعامل مع أقرب انتهاء صلاحية لجميع الـ Leases كطابع زمني أو إصدار للـ LeaseSet. عموماً لن تقبل الـ routers تخزين LeaseSet ما لم يكن "أحدث" من النسخة الحالية. توخ الحذر عند نشر LeaseSet جديد حيث يكون أقدم Lease هو نفسه أقدم Lease في الـ LeaseSet السابق. يجب على الـ router الناشر عموماً زيادة انتهاء صلاحية أقدم Lease بما لا يقل عن 1 ميللي ثانية في تلك الحالة.

* قبل الإصدار 0.9.7، عندما يتم تضمينه في رسالة DatabaseStore المرسلة من router المصدر، كان router يعيّن جميع انتهاء صلاحيات leases المنشورة لنفس القيمة، وهي قيمة أقدم lease. اعتباراً من الإصدار 0.9.7، ينشر router انتهاء الصلاحية الفعلي لكل lease. هذا تفصيل تنفيذي وليس جزءاً من مواصفات الهياكل.

* الحجم الإجمالي: 40 بايت

مستندات جافا: [net.i2p.data.LeaseSet](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet.html)

### Lease2

#### المحتويات

يحدد التفويض لنفق معين لاستقبال الرسائل المستهدفة لـ [Destination](#destination). مماثل لـ [Lease](#lease) ولكن مع end_date من 4 بايت. يُستخدم بواسطة [LeaseSet2](#leaseset2). مدعوم اعتباراً من الإصدار 0.9.38؛ راجع المقترح 123 للمزيد من المعلومات.

#### ملاحظات

SHA256 [هاش](#hash) لـ [RouterIdentity](#routeridentity) الراوتر البوابة، ثم [TunnelId](#tunnelid)، وأخيراً تاريخ انتهاء مكوّن من 4 بايتات.

```bytefield
tunnel_gw   | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes

tunnel_id   | 4 | green  | TunnelId, 4 bytes
end_date    | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway
             length -> 32 bytes

tunnel_id :: `TunnelId`
             length -> 4 bytes

end_date :: 4 byte date
            length -> 4 bytes
            Seconds since the epoch, rolls over in 2106.
```

</details>
#### الوصف

* يمكن، بل ويجب، إنشاء هذا القسم في وضع عدم الاتصال.

JavaDoc: [net.i2p.data.Lease2](http://docs.i2p-projekt.de/net/i2p/data/Lease2.html)

### التوقيع دون اتصال

#### المحتويات

هذا جزء اختياري من [LeaseSet2Header](#leaseset2header). ويُستخدم أيضًا في البث وفي I2CP. مدعوم بدءًا من الإصدار 0.9.38؛ انظر الاقتراح 123 لمزيد من المعلومات.

#### ملاحظات

يحتوي على انتهاء صلاحية، ونوع توقيع و[SigningPublicKey](#signingpublickey) مؤقت، و[Signature](#signature).

```bytefield
expires              | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
sigtype              | 2 | cyan   | 2 byte type of the transient_public_key
_ | 2
transient_public_key | 8 | green  | SigningPublicKey, as inferred from sigtype

signature            | 8 | purple | Signature, as inferred from sigtype of the Destination's key

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4 byte date
           length -> 4 bytes
           Seconds since the epoch, rolls over in 2106.

sigtype :: 2 byte type of the transient_public_key
           length -> 2 bytes

transient_public_key :: `SigningPublicKey`
                        length -> As inferred from the sigtype

signature :: `Signature`
             length -> As inferred from the sigtype of the signing public key
                       in the `Destination` that preceded this offline signature.
             Signature of expires timestamp, transient sig type, and public key,
             by the destination public key.
```

</details>
#### الوصف

* **الأعلام** (2 بايت):
  * البت 0: إذا تم تعيينه، فإن المفاتيح غير المتصلة موجودة (انظر [OfflineSignature](#offlinesignature))
  * البت 1: إذا تم تعيينه، فهذا leaseSet غير منشور
  * البت 2: إذا تم تعيينه، فهذا leaseSet مُعمى
  * البتات 15-3: محجوزة، يتم تعيينها إلى 0

### LeaseSet2Header

#### المحتويات

هذا هو الجزء المشترك بين [LeaseSet2](#leaseset2) و [MetaLeaseSet](#metaleaseset). مدعوم بدءًا من الإصدار 0.9.38؛ انظر الاقتراح 123 لمزيد من المعلومات.

#### ملاحظات

يحتوي على [Destination](#destination)، وطابعين زمنيين، و[OfflineSignature](#offlinesignature) اختياري.

```bytefield
destination          | 8 | blue   | Destination, >= 387+ bytes

published            | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
expires              | 2 | cyan   | 2 byte time, offset from published in seconds, 18.2 hours max
flags                | 2 | red
offline_signature    | 8 | purple | OfflineSignature, varies, optional (present if flags bit 0 set

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: `Destination`
               length -> >= 387+ bytes

published :: 4 byte date
             length -> 4 bytes
             Seconds since the epoch, rolls over in 2106.

expires :: 2 byte time
           length -> 2 bytes
           Offset from published timestamp in seconds, 18.2 hours max

flags :: 2 bytes
  Bit order: 15 14 ... 3 2 1 0
  Bit 0: If 0, no offline keys; if 1, offline keys
  Bit 1: If 0, a standard published leaseset.
         If 1, an unpublished leaseset.
  Bit 2: If 0, a standard published leaseset.
         If 1, this unencrypted leaseset will be blinded and encrypted when published.
  Bits 15-3: set to 0 for compatibility with future uses

offline_signature :: `OfflineSignature`
                     length -> varies
                     Optional, only present if bit 0 is set in the flags.
```

</details>
#### الوصف

* الحجم الإجمالي: 395 بايت كحد أدنى

* الحد الأقصى الفعلي لوقت انتهاء الصلاحية هو حوالي 660 (11 دقيقة) لـ
  [LeaseSet2](#leaseset2) و 65535 (18.2 ساعة كاملة) لـ [MetaLeaseSet](#metaleaseset).

* [LeaseSet](#leaseset) (1) لم يكن لديه حقل 'published'، لذلك تطلب إصدار النسخ
  البحث عن أقدم lease. يضيف LeaseSet2 حقل 'published'
  بدقة ثانية واحدة. يجب على الـ routers تحديد معدل إرسال
  leasesets جديدة إلى floodfills بمعدل أبطأ بكثير من مرة واحدة في الثانية (لكل وجهة).
  إذا لم يتم تطبيق هذا، فيجب على الكود التأكد من أن كل leaseset جديد
  لديه وقت 'published' متأخر ثانية واحدة على الأقل عن السابق، وإلا
  فإن floodfills لن تقوم بتخزين أو إغراق الـ leaseset الجديد.

- serviceoption := optionkey optionvalue
- optionkey := _service._proto
- service := الاسم الرمزي للخدمة المطلوبة. يجب أن يكون بأحرف صغيرة. مثال: "smtp".
  الأحرف المسموحة هي [a-z0-9-] ويجب ألا تبدأ أو تنتهي بـ '-'.
  يجب استخدام المعرفات القياسية من [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) أو Linux /etc/services إذا كانت معرفة هناك.
- proto := بروتوكول النقل للخدمة المطلوبة. يجب أن يكون بأحرف صغيرة، إما "tcp" أو "udp".
  "tcp" يعني التدفق و "udp" يعني البيانات القابلة للرد.
  قد يتم تعريف مؤشرات البروتوكول للبيانات الخام و datagram2 لاحقاً.
  الأحرف المسموحة هي [a-z0-9-] ويجب ألا تبدأ أو تنتهي بـ '-'.
- optionvalue := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priority weight port target [appoptions]
- ttl := وقت البقاء، ثواني صحيحة. عدد صحيح موجب. مثال: "86400".
  يُوصى بحد أدنى 86400 (يوم واحد)، راجع قسم التوصيات أدناه للتفاصيل.
- priority := أولوية المضيف المستهدف، القيمة الأقل تعني الأفضلية الأكبر. عدد صحيح غير سالب. مثال: "0"
  مفيد فقط إذا كان هناك أكثر من سجل واحد، لكنه مطلوب حتى لو كان سجل واحد فقط.
- weight := وزن نسبي للسجلات ذات الأولوية نفسها. القيمة الأعلى تعني فرصة أكبر للاختيار. عدد صحيح غير سالب. مثال: "0"
  مفيد فقط إذا كان هناك أكثر من سجل واحد، لكنه مطلوب حتى لو كان سجل واحد فقط.
- port := منفذ I2CP الذي يمكن العثور على الخدمة عليه. عدد صحيح غير سالب. مثال: "25"
  المنفذ 0 مدعوم لكن غير مُوصى به.
- target := اسم المضيف أو b32 للوجهة التي توفر الخدمة. اسم مضيف صالح كما في [NAMING](/docs/overview/naming/). يجب أن يكون بأحرف صغيرة.
  مثال: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" أو "example.i2p".
  يُوصى بـ b32 ما لم يكن اسم المضيف "معروفاً جيداً"، أي في كتب العناوين الرسمية أو الافتراضية.
- appoptions := نص تعسفي خاص بالتطبيق، يجب ألا يحتوي على " " أو ",". الترميز هو UTF-8.

### LeaseSet2

#### المحتويات

موجود في رسالة I2NP من النوع DatabaseStore رقم 3. مدعوم بدءًا من الإصدار 0.9.38؛ راجع الاقتراح 123 لمزيد من المعلومات.

يحتوي على جميع [Lease2](#lease2) المعتمدة حالياً لـ [Destination](#destination) معين، و[PublicKey](#publickey) التي يمكن تشفير رسائل garlic إليها. LeaseSet هو أحد الهيكلين المخزنين في قاعدة بيانات الشبكة (والآخر هو [RouterInfo](#routerinfo))، ويتم فهرسته تحت SHA256 للـ [Destination](#destination) المحتوى.

#### تفضيل مفتاح التشفير

[LeaseSet2Header](#leaseset2header)، يليه خيارات، ثم واحد أو أكثر من [PublicKey](#publickey) للتشفير، و[Integer](#integer) يحدد عدد هياكل [Lease2](#lease2) الموجودة في المجموعة، تليها هياكل [Lease2](#lease2) الفعلية، وأخيرًا [Signature](#signature) للبايتات السابقة موقعة بواسطة [SigningPrivateKey](#signingprivatekey) الخاص بـ [Destination](#destination) أو بالمفتاح العابر.

```bytefield
ls2_header       | 8 | blue   | LeaseSet2Header, varies
options          | 8 | gray   | Mapping, varies, 2 bytes minimum
numk             | 2 | red    | Integer, 1 byte, number of encryption keys (1 <= numk <= max TBD)
keytype0         | 3 | cyan   | Encryption type of PublicKey, 2 bytes
keylen0          | 3 | cyan   | Length of PublicKey, 2 bytes
encryption_key_0 | 8 | green  | PublicKey, keylen bytes
keytypen         | 4 | cyan   | Encryption type of PublicKey, 2 bytes
keylenn          | 4 | cyan   | Length of PublicKey, 2 bytes
encryption_key_n | 8 | green  | PublicKey, keylen bytes
num              | 1 | red    | Integer, 1 byte, number of Lease2s (0-16)
Lease2 0         | 7 | yellow | Lease2, 40 bytes
Lease2 ($num-1)  | 8 | yellow | Lease2, 40 bytes
signature        | 8 | purple | Signature, 40 bytes or as specified in destination's key cert
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: `LeaseSet2Header`
             length -> varies

options :: `Mapping`
           length -> varies, 2 bytes minimum

numk :: `Integer`
        length -> 1 byte
        Number of key types, key lengths, and `PublicKey`s to follow
        value: 1 <= numk <= max TBD

keytype :: The encryption type of the `PublicKey` to follow.
           length -> 2 bytes

keylen :: The length of the `PublicKey` to follow.
          Must match the specified length of the encryption type.
          length -> 2 bytes

encryption_key :: `PublicKey`
                  length -> keylen bytes

num :: `Integer`
       length -> 1 byte
       Number of `Lease2`s to follow
       value: 0 <= num <= 16

leases :: [`Lease2`]
          length -> $num*40 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate, or by the sigtype of the transient public key,
                       if present in the header
```

</details>
#### الخيارات

بالنسبة لـ leasesets المنشورة (الخادم)، مفاتيح التشفير مرتبة حسب تفضيل الخادم، الأكثر تفضيلاً أولاً. إذا كان العملاء يدعمون أكثر من نوع تشفير واحد، يُنصح بأن يحترموا تفضيل الخادم ويختاروا النوع المدعوم الأول كطريقة التشفير المستخدمة للاتصال بالخادم. بشكل عام، أنواع المفاتيح الأحدث (ذات الأرقام الأعلى) أكثر أماناً أو كفاءة ومفضلة، لذا يجب أن تُدرج المفاتيح بترتيب عكسي لنوع المفتاح.

ومع ذلك، قد تختار العميلات، حسب التنفيذ، بناءً على تفضيلاتها بدلًا من ذلك، أو استخدام طريقة ما لتحديد التفضيل "المدمج". قد يكون هذا مفيدًا كخيار تهيئة، أو لأغراض التصحيح.

ترتيب المفاتيح في leasesets غير المنشورة (العميل) لا يهم فعليًا، لأن الاتصالات عادة لن تُحاول مع العملاء غير المنشورين. ما لم يُستخدم هذا الترتيب لتحديد تفضيل مدمج، كما هو موضح أعلاه.

#### ملاحظات

اعتبارًا من واجهة برمجة التطبيقات (API) 0.9.66، تم تعريف تنسيق قياسي لخيارات سجل الخدمة. راجع الاقتراح 167 للحصول على التفاصيل. قد تُعرَّف في المستقبل خيارات أخرى غير سجلات الخدمة، وتستخدم تنسيقًا مختلفًا.

يجب ترتيب خيارات LS2 حسب المفتاح، بحيث يكون التوقيع ثابتاً.

تُعرّف خيارات سجل الخدمة كما يلي:

* تم استخدام المفتاح العام للوجهة في التشفير القديم من I2CP إلى I2CP والذي تم تعطيله في الإصدار 0.6، وهو حالياً غير مستخدم.

أمثلة:

في LS2 للعنوان aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p، والذي يشير إلى خادم SMTP واحد:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

في LS2 لـ aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p، يشير إلى خادمي SMTP اثنين:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

في LS2 لعنوان bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p، يشير إلى نفسه كخادم SMTP:

"_smtp._tcp" "0 999999 25"

#### الوصف

* تُستخدم مفاتيح التشفير للتشفير من طرف إلى طرف ElGamal/AES+SessionTag
  [ELGAMAL-AES](/docs/specs/elgamal-aes/) (النوع 0) أو مخططات التشفير الأخرى من طرف إلى طرف.
  انظر [ECIES](/docs/specs/ecies/) والاقتراحين 145 و156.
  يمكن إنشاؤها من جديد عند كل بدء تشغيل للrouter
  أو يمكن أن تكون دائمة.
  X25519 (النوع 4، انظر [ECIES](/docs/specs/ecies/)) مدعوم اعتباراً من الإصدار 0.9.44.

* التوقيع يغطي البيانات أعلاه، مُسبوقة بالبايت الواحد الذي يحتوي على نوع DatabaseStore (3).

* يمكن التحقق من التوقيع باستخدام المفتاح العام للتوقيع الخاص بالوجهة، أو المفتاح العام المؤقت للتوقيع، إذا تم تضمين توقيع غير متصل في رأس leaseset2.

* يتم توفير طول المفتاح لكل مفتاح، بحيث يمكن لـ floodfills والعملاء تحليل البنية حتى لو لم تكن جميع أنواع التشفير معروفة أو مدعومة.

* انظر الملاحظة حول حقل 'published' في [LeaseSet2Header](#leaseset2header)

* تطبيق الخيارات، إذا كان الحجم أكبر من واحد، يجب أن يكون مرتباً حسب المفتاح، بحيث يكون التوقيع ثابتاً.

* الحجم الإجمالي: 40 بايت

توثيق جافا: [net.i2p.data.LeaseSet2](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet2.html)

### MetaLease

#### المحتويات

مبدئي. غير مدعوم بالكامل.

يحدد التفويض لـ tunnel معين لتلقي الرسائل المستهدفة لـ [Destination](#destination). نفس [Lease2](#lease2) ولكن مع العلامات والتكلفة بدلاً من معرف الـ tunnel. يُستخدم بواسطة [MetaLeaseSet](#metaleaseset). محتوى في رسالة I2NP DatabaseStore من النوع 7. مدعوم اعتباراً من الإصدار 0.9.38؛ انظر المقترح 123 لمزيد من المعلومات.

#### ملاحظات

دالة التجزئة SHA256 [Hash](#hash) الخاصة بهوية الموجه [RouterIdentity](#routeridentity) للموجه البوابة، ثم العلمات والتكلفة، وأخيرًا تاريخ الانتهاء المؤلف من 4 بايت.

```bytefield
tunnel_gw | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes
flags     | 3 | red    | 3 bytes
cost      | 1 | green  | 1 byte
end_date  | 4 | yellow | 4 bytes, seconds since epoch
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway,
             or the hash of another `MetaLeaseSet`.
             length -> 32 bytes

flags :: 3 bytes of flags
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Type of the entry.
         If 0, unknown.
         If 1, a `LeaseSet`.
         If 3, a `LeaseSet2`.
         If 5, a `MetaLeaseSet`.
         Bits 23-4: set to 0 for compatibility with future uses
         length -> 3 bytes

cost :: 1 byte, 0-255. Lower value is higher priority.
        length -> 1 byte

end_date :: 4 byte date
            length -> 4 bytes
            Seconds since the epoch, rolls over in 2106.

```
</details>
#### الوصف

* تم استخدام المفتاح العام للوجهة للتشفير القديم من I2CP إلى I2CP الذي تم تعطيله في الإصدار 0.6، وهو حالياً غير مستخدم.

مستندات جافا: [net.i2p.data.MetaLease](http://docs.i2p-projekt.de/net/i2p/data/MetaLease.html)

### MetaLeaseSet

#### المحتويات

مبدئي. غير مدعوم بالكامل.

موجود في رسالة I2NP من النوع DatabaseStore رقم 7. تم تعريفه بدءًا من الإصدار 0.9.38؛ انظر الاقتراح 123 للحصول على مزيد من المعلومات.

يحتوي على جميع عقود [MetaLease](#metalease) المصرح بها حاليًا لموقع [Destination](#destination) معين، وكذلك على [PublicKey](#publickey) الذي يمكن تشفير رسائل الثوم (garlic) إليه. يُعدّ LeaseSet إحدى الهيكلين المخزَّنين في قاعدة البيانات الشبكية (والهيكل الآخر هو [RouterInfo](#routerinfo))، ويتم فهرسته باستخدام تجزئة SHA256 الخاصة بـ [Destination](#destination) المضمنة فيه.

#### ملاحظات

[LeaseSet2Header](#leaseset2header)، متبوعًا بخيارات، و[Integer](#integer) يحدد عدد هياكل [Lease2](#lease2) الموجودة في المجموعة، ثم تتبعها هياكل [Lease2](#lease2) الفعلية، وأخيرًا [Signature](#signature) للبايتات السابقة موقعة بواسطة [SigningPrivateKey](#signingprivatekey) الخاصة بـ [Destination](#destination) أو بالمفتاح العابر.

```bytefield
ls2_header       | 8 | blue   | LeaseSet2Header, varies
options          | 8 | green  | Mapping, varies, 2 bytes minimum
num              | 1 | red    | Integer, 1 byte
MetaLease 0      | 7 | yellow | 40 bytes
MetaLease ($num-1) | 8 | yellow | 40 bytes
numr             | 1 | red    | Integer, 1 byte
revocation_0     | 8 | cyan   | Hash, 32 bytes
revocation_n     | 8 | cyan   | Hash, 32 bytes
signature        | 8 | purple | Signature, 40+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: `LeaseSet2Header`
             length -> varies

options :: `Mapping`
           length -> varies, 2 bytes minimum

num :: `Integer`
        length -> 1 byte
        Number of `MetaLease`s to follow
        value: 1 <= num <= max TBD

leases :: `MetaLease`s
          length -> $numr*40 bytes

numr :: `Integer`
        length -> 1 byte
        Number of `Hash`es to follow
        value: 0 <= numr <= max TBD

revocations :: [`Hash`]
               length -> $numr*32 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate, or by the sigtype of the transient public key,
                       if present in the header

```
</details>
#### الوصف

* التوقيع يكون على البيانات أعلاه، مع إضافة البايت الواحد الذي يحتوي على نوع DatabaseStore (7) في المقدمة.

* يمكن التحقق من التوقيع باستخدام المفتاح العام للتوقيع الخاص بالوجهة، أو المفتاح العام المؤقت للتوقيع، إذا كان التوقيع غير المتصل مضمناً في رأس leaseset2.

* انظر الملاحظة حول حقل 'published' في [LeaseSet2Header](#leaseset2header)

* المفتاح العام للوجهة كان يُستخدم لتشفير I2CP-to-I2CP القديم الذي تم تعطيله في الإصدار 0.6، وهو غير مستخدم حالياً.

JavaDoc: [net.i2p.data.MetaLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/MetaLeaseSet.html)

### EncryptedLeaseSet

#### المحتويات

محتوى في رسالة I2NP من النوع DatabaseStore رقم 5. تم تعريفه بدءًا من الإصدار 0.9.38؛ وبدأ العمل به بدءًا من الإصدار 0.9.39؛ انظر الاقتراح 123 لمزيد من المعلومات.

لا يكون المفتاح المخفي ووقت انتهاء الصلاحية فقط مرئيين بشكل نصي واضح. يتم تشفير مجموعة الإيجار الفعلية.

#### ملاحظات

نوع توقيع مكوّن من بايتين، و[مفتاح التوقيع الخاص المموّه](#signingprivatekey)، ووقت النشر، وانتهاء الصلاحية، والعلم. ثم طول مكوّن من بايتين يتبعه البيانات المشفرة. وأخيرًا، [توقيع](#signature) للبايتات السابقة تم توقيعه بواسطة المفتاح المموّه [SigningPrivateKey](#signingprivatekey) أو المفتاح العابر.

```bytefield
sigtype            | 2 | red    | 2 bytes
blinded_public_key | 8 | blue   | SigningPublicKey, varies
published          | 4 | green  | 4 bytes, seconds since epoch
expires            | 2 | yellow | 2 bytes
flags              | 2 | red    | 2 bytes
offline_signature  | 8 | orange | OfflineSignature, optional, varies
len                | 2 | gray   | Integer, 2 bytes
encrypted_data     | 8 | cyan   | Encrypted data, len bytes
signature          | 8 | purple | Signature, varies
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### الوصف

* التوقيع يكون على البيانات أعلاه، مُسبوقة بالبايت الواحد الذي يحتوي على نوع DatabaseStore (5).

* يمكن التحقق من التوقيع باستخدام المفتاح العام للتوقيع الخاص بالوجهة، أو المفتاح العام المؤقت للتوقيع، إذا كان التوقيع غير المتصل مضمنًا في رأس leaseset2.

* التعمية والتشفير محددان في [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)

* هذا الهيكل لا يستخدم [LeaseSet2Header](#leaseset2header).

* الحد الأقصى للوقت الفعلي للانتهاء هو حوالي 660 (11 دقيقة)، إلا إذا كان [MetaLeaseSet](#metaleaseset) مشفراً.

* انظر الاقتراح 123 للحصول على ملاحظات حول استخدام التوقيعات غير المتصلة مع leasesets المشفرة.

* انظر الملاحظة حول حقل 'published' في [LeaseSet2Header](#leaseset2header)
  (نفس المشكلة، حتى لو أننا لا نستخدم تنسيق LeaseSet2Header هنا)

* التكلفة عادة ما تكون 5 أو 6 لـ SSU، و 10 أو 11 لـ NTCP.

* انتهاء الصلاحية غير مستخدم حالياً، دائماً null (جميع الأصفار). اعتباراً من الإصدار 0.9.3، يُفترض أن انتهاء الصلاحية صفر ولا يتم تخزينه، لذا أي انتهاء صلاحية غير صفري سيفشل في التحقق من توقيع RouterInfo. تنفيذ انتهاء الصلاحية (أو استخدام آخر لهذه البايتات) سيكون تغييراً غير متوافق مع الإصدارات السابقة. يجب على الـ routers تعيين هذا الحقل إلى جميع الأصفار. اعتباراً من الإصدار 0.9.12، يتم التعرف على حقل انتهاء الصلاحية غير الصفري مرة أخرى، ومع ذلك يجب أن ننتظر عدة إصدارات لاستخدام هذا الحقل، حتى تتعرف عليه الغالبية العظمى من الشبكة.

JavaDoc: [net.i2p.data.EncryptedLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/EncryptedLeaseSet.html)

### RouterAddress

#### المحتويات

يُعرّف هذا الهيكل الوسيلة للتواصل مع جهاز توجيه من خلال بروتوكول نقل.

#### ملاحظات

بايت واحد [Integer](#integer) يعرّف التكلفة النسبية لاستخدام العنوان، حيث إن القيمة `1` تعني مجانًا والقيمة `255` تعني باهظة التكلفة، متبوعًا بـ [Date](#date) انتهاء الصلاحية الذي بعدم لا ينبغي استخدام العنوان بعده، أو إذا كانت القيمة null، فإن العنوان لا ينتهي صلاحيته أبدًا. بعد ذلك يأتي [String](#string) يحدد بروتوكول النقل الذي يستخدمه عنوان الموجه هذا. وأخيرًا، يوجد [Mapping](#mapping) يحتوي على جميع الخيارات الخاصة بالنقل اللازمة لإنشاء الاتصال، مثل عنوان IP، ورقم المنفذ، وعنوان البريد الإلكتروني، وURL، إلخ.

```bytefield
cost            | 1 | green  | Integer, 1 byte
expiration      | 7 | yellow | Date, 8 bytes
transport_style | 8 | blue   | String, 1-256 bytes
options         | 8 | purple | Mapping
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-/-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### الوصف

* الخيارات التالية، رغم أنها غير مطلوبة، إلا أنها معيارية ومتوقع وجودها في معظم عناوين الـ router: "host" (عنوان IPv4 أو IPv6 أو اسم المضيف) و "port".

* قد يتبع peer_size [Integer](#integer) قائمة تحتوي على عدد مماثل من hash قيم router.
  هذا غير مستخدم حاليًا. كان مخصصًا لشكل من أشكال المسارات المقيدة،
  والذي لم يتم تنفيذه.
  قد تتطلب تنفيذات معينة أن تكون القائمة مرتبة بحيث يكون التوقيع ثابتًا.
  يجب البحث في هذا قبل تمكين هذه الميزة.

* يمكن التحقق من التوقيع باستخدام المفتاح العام للتوقيع الخاص بـ router_ident.

* انظر صفحة قاعدة بيانات الشبكة [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo) للاطلاع على الخيارات القياسية المتوقع وجودها في جميع معلومات router.

مستندات جافا: [net.i2p.data.router.RouterAddress](http://docs.i2p-projekt.de/net/i2p/data/router/RouterAddress.html)

### RouterInfo

#### المحتويات

يحدد جميع البيانات التي يريد router نشرها ليراها الشبكة. [RouterInfo](#routerinfo) هو أحد البنيتين المخزنتين في قاعدة بيانات الشبكة (والأخرى هي [LeaseSet](#leaseset))، ويتم فهرسته تحت SHA256 للـ [RouterIdentity](#routeridentity) المحتوى.

#### ملاحظات

[RouterIdentity](#routeridentity) يليها [Date](#date)، عند نشر المدخل

```bytefield
router_ident           | 8 | blue   | RouterIdentity, >= 387+ bytes
published              | 8 | green  | Date, 8 bytes
size                   | 1 | red    | Integer, 1 byte
RouterAddress 0        | 7 | yellow | varies
RouterAddress 1        | 8 | yellow | varies
RouterAddress ($size-1)| 8 | yellow | varies
psiz                   | 1 | red    | Integer, 1 byte
options                | 7 | purple | Mapping
signature              | 8 | cyan   | Signature, 40+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-/-+----+----+----+
|psiz| options                          |
+----+----+----+----+-/-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### ملاحظات

* أجهزة router القديمة جداً كانت تتطلب ترتيب العناوين حسب SHA256 الخاص ببياناتها
  بحيث يكون التوقيع ثابتاً.
  هذا لم يعد مطلوباً، ولا يستحق التنفيذ من أجل التوافق مع الإصدارات السابقة.

- [ECIES](/docs/specs/ecies/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy)
- [ELGAMAL-AES](/docs/specs/elgamal-aes/)
- [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NAMING](/docs/overview/naming/)
- [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo)
- [Prop134](/proposals/134-gost/)
- [Prop169](/proposals/169-pq-crypto/)
- [REGISTRY](http://www.dns-sd.org/ServiceTypes.html)
- [SSU](/docs/legacy/ssu/)
- [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions)

* يمكن التحقق من التوقيع باستخدام المفتاح العمومي للتوقيع الخاص بـ router_ident.

* راجع صفحة قاعدة بيانات الشبكة [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo) للخيارات القياسية التي من المتوقع أن تكون موجودة في جميع معلومات الموجهات.

* كانت تتطلب الموجهات القديمة جدًا فرز العناوين حسب قيمة الهاش SHA256 للبيانات الخاصة بها
  حتى تكون التوقيعات ثابتة (لا تتغير).
  لم يعد هذا الشرط مطلوبًا، ولا يستحق التنفيذ من أجل التوافق مع الإصدارات السابقة.

توثيق جافا: [net.i2p.data.router.RouterInfo](http://docs.i2p-projekt.de/net/i2p/data/router/RouterInfo.html)

### تعليمات التسليم

يتم تعريف تعليمات تسليم رسالة النفق في وثيقة مواصفات النفق [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions).

يتم تعريف تعليمات تسليم رسائل Garlic في مواصفات رسائل I2NP [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions).

## المراجع

- [ECIES](/docs/specs/ecies/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy)
- [ELGAMAL-AES](/docs/specs/elgamal-aes/)
- [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NAMING](/docs/overview/naming/)
- [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo)
- [Prop134](/proposals/134-gost/)
- [Prop169](/proposals/169-pq-crypto/)
- [REGISTRY](http://www.dns-sd.org/ServiceTypes.html)
- [SSU](/docs/legacy/ssu/)
- [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions)
