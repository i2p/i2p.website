---
title: "निम्न-स्तरीय क्रिप्टोग्राफी"
description: "I2P में प्रयुक्त सममित, असममित, और हस्ताक्षर primitives (मूलभूत क्रिप्टोग्राफिक विधियाँ) का सारांश"
slug: "cryptography"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **स्थिति:** यह पृष्ठ पुराने "लो-लेवल क्रिप्टोग्राफी विनिर्देश" का संक्षेप प्रस्तुत करता है। आधुनिक I2P रिलीज़ (2.10.0, अक्टूबर 2025) ने नए क्रिप्टोग्राफ़िक प्रिमिटिव्स पर माइग्रेशन पूरा कर लिया है। कार्यान्वयन विवरण के लिए [ECIES](/docs/specs/ecies/), [Encrypted LeaseSets](/docs/specs/encryptedleaseset/), [NTCP2](/docs/specs/ntcp2/), [Red25519](/docs/specs/red25519-signature-scheme/), [SSU2](/docs/specs/ssu2/), तथा [Tunnel Creation (ECIES)](/docs/specs/implementation/) जैसी विशेषीकृत विनिर्देशों का उपयोग करें।

## विकास का स्नैपशॉट

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
## असममित एन्क्रिप्शन

### X25519 (Curve25519 पर आधारित एलिप्टिक-वक्र Diffie–Hellman (ECDH) कुंजी-विनिमय योजना)

- NTCP2, ECIES-X25519-AEAD-Ratchet, SSU2, और X25519-आधारित tunnel निर्माण के लिए उपयोग किया जाता है.  
- कॉम्पैक्ट कुंजियाँ, स्थिर-समय संचालन, और Noise प्रोटोकॉल फ़्रेमवर्क के माध्यम से फॉरवर्ड सीक्रेसी (पूर्व सत्रों की गोपनीयता बरकरार रहती है) प्रदान करता है.  
- 32-बाइट कुंजियों और कुशल कुंजी आदान-प्रदान के साथ 128-बिट सुरक्षा प्रदान करता है.

### ElGamal (पुराना)

- पुराने routers के साथ बैकवर्ड संगतता के लिए बनाए रखा गया है।  
- 2048-बिट Oakley Group 14 prime (RFC 3526) पर generator 2 के साथ संचालित होता है।  
- AES सेशन कीज़ तथा IVs (Initialization Vectors) को 514-बाइट साइफ़रटेक्स्ट्स में एन्क्रिप्ट करता है।  
- प्रमाणीकृत एन्क्रिप्शन और forward secrecy (भविष्य-गोपनीयता) का अभाव है; सभी आधुनिक एंडपॉइंट्स ECIES पर स्थानांतरित हो चुके हैं।

## सममित कूटलेखन

### ChaCha20/Poly1305 (एन्क्रिप्शन और प्रमाणीकरण के लिए AEAD एल्गोरिद्म संयोजन)

- NTCP2, SSU2, और ECIES में प्रयुक्त डिफ़ॉल्ट प्रमाणित एन्क्रिप्शन प्रिमिटिव।  
- AES हार्डवेयर समर्थन के बिना AEAD (संबद्ध डेटा सहित प्रमाणित एन्क्रिप्शन) सुरक्षा और उच्च प्रदर्शन प्रदान करता है।  
- RFC 7539 के अनुरूप लागू किया गया है (256‑बिट कुंजी, 96‑बिट नॉन्स, 128‑बिट टैग).

### AES‑256/CBC (पुराना)

- अब भी tunnel परत एन्क्रिप्शन में उपयोग होता है, जहाँ इसकी block‑cipher (ब्लॉक‑आधारित कूटलेखन) संरचना I2P के स्तरीय एन्क्रिप्शन मॉडल में फिट बैठती है.  
- PKCS#5 पैडिंग और प्रत्येक‑हॉप IV (Initialization Vector, आरंभिक वेक्टर) रूपांतरणों का उपयोग करता है.  
- दीर्घकालिक समीक्षा के लिए निर्धारित है, परंतु क्रिप्टोग्राफ़िक रूप से सुदृढ़ बनी हुई है.

## हस्ताक्षर

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
## हैश और कुंजी व्युत्पत्ति

- **SHA‑256:** DHT (वितरित हैश तालिका) कुंजियों, HKDF, और पुराने प्रकार के हस्ताक्षरों के लिए उपयोग किया जाता है.  
- **SHA‑512:** EdDSA/RedDSA द्वारा, तथा Noise HKDF व्युत्पत्तियों में उपयोग किया जाता है.  
- **HKDF‑SHA256:** ECIES, NTCP2, और SSU2 में सत्र कुंजियाँ व्युत्पन्न करता है.  
- प्रतिदिन बदलती SHA‑256 व्युत्पत्तियाँ netDb में RouterInfo और LeaseSet के भंडारण स्थानों को सुरक्षित करती हैं.

## ट्रांसपोर्ट लेयर सारांश

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
दोनों ट्रांसपोर्ट प्रोटोकॉल, Noise_XK हैंडशेक पैटर्न का उपयोग करते हुए, लिंक‑स्तरीय forward secrecy (जिसमें दीर्घकालीन कुंजी के उजागर होने पर भी सेशन कुंजियाँ सुरक्षित रहती हैं) और रीप्ले सुरक्षा प्रदान करते हैं।

## Tunnel परत कूटलेखन

- प्रति‑हॉप स्तरीकृत एन्क्रिप्शन के लिए AES‑256/CBC का उपयोग जारी है.  
- आउटबाउंड गेटवे क्रमिक AES डिक्रिप्शन करते हैं; प्रत्येक हॉप अपनी लेयर कुंजी और IV (initialization vector, आरंभन सदिश) कुंजी का उपयोग करके पुनः एन्क्रिप्ट करता है.  
- डबल‑IV एन्क्रिप्शन सहसंबंध और पुष्टि हमलों को कम करता है.  
- AEAD (Authenticated Encryption with Associated Data, संबद्ध डेटा सहित प्रमाणित एन्क्रिप्शन) में स्थानांतरण अध्ययनाधीन है, परंतु फिलहाल इसकी योजना नहीं है.

## पोस्ट‑क्वांटम क्रिप्टोग्राफी

- I2P 2.10.0 में **प्रायोगिक हाइब्रिड पोस्ट‑क्वांटम एन्क्रिप्शन** पेश किया गया है।  
- परीक्षण के लिए Hidden Service Manager (हिडन सर्विस मैनेजर) के माध्यम से मैन्युअल रूप से सक्षम किया जा सकता है।  
- X25519 को एक क्वांटम‑प्रतिरोधी KEM (कुंजी एनकैप्सुलेशन मेकैनिज़्म) के साथ जोड़ता है (हाइब्रिड मोड)।
- डिफ़ॉल्ट नहीं; शोध और प्रदर्शन मूल्यांकन के लिए अभिप्रेत।

## विस्तारयोग्यता फ्रेमवर्क

- एन्क्रिप्शन और सिग्नेचर *प्रकार पहचानकर्ता* अनेक क्रिप्टोग्राफ़िक प्रिमिटिव्स (आधारभूत तत्त्व) के समानांतर समर्थन की अनुमति देते हैं.  
- वर्तमान मैपिंग में शामिल हैं:  
  - **एन्क्रिप्शन प्रकार:** 0 = ElGamal/AES+SessionTags, 4 = ECIES‑X25519‑AEAD‑Ratchet.  
  - **सिग्नेचर प्रकार:** 0 = DSA‑SHA1, 7 = EdDSA‑SHA512‑Ed25519, 11 = RedDSA‑SHA512‑Ed25519.  
- यह फ़्रेमवर्क भविष्य के उन्नयन सक्षम करता है, जिनमें post‑quantum (क्वांटम‑प्रतिरोधी) योजनाएँ शामिल हैं, बिना नेटवर्क विभाजनों के.

## क्रिप्टोग्राफिक संयोजन

- **ट्रांसपोर्ट लेयर:** X25519 + ChaCha20/Poly1305 (Noise फ्रेमवर्क).  
- **Tunnel लेयर:** अनामिकता के लिए AES‑256/CBC परतदार एन्क्रिप्शन।  
- **एंड‑टू‑एंड:** गोपनीयता और फॉरवर्ड सीक्रेसी (आगे की गोपनीयता) के लिए ECIES‑X25519‑AEAD‑Ratchet।  
- **डेटाबेस लेयर:** प्रामाणिकता के लिए EdDSA/RedDSA हस्ताक्षर।

ये परतें मिलकर बहु‑स्तरीय सुरक्षा प्रदान करती हैं: यदि किसी एक परत से समझौता हो भी जाए, तब भी अन्य परतें गोपनीयता और unlinkability (विभिन्न गतिविधियों/संदेशों/पहचानकर्ताओं को आपस में जोड़कर पहचान न किया जा सकना) बनाए रखती हैं।

## सारांश

I2P 2.10.0 का क्रिप्टोग्राफिक स्टैक मुख्य रूप से इन पर केंद्रित है:

- **Curve25519 (X25519)** कुंजी विनिमय के लिए  
- **ChaCha20/Poly1305** सममित एन्क्रिप्शन के लिए  
- **EdDSA / RedDSA** हस्ताक्षरों के लिए  
- **SHA‑256 / SHA‑512** हैशिंग और व्युत्पत्ति के लिए  
- **प्रायोगिक क्वांटम‑पश्चात हाइब्रिड मोड** आगे की अनुकूलता के लिए

पुराने ElGamal, AES‑CBC, और DSA backward compatibility के लिए बने हुए हैं, लेकिन अब सक्रिय ट्रांसपोर्ट्स या एन्क्रिप्शन पथों में उपयोग नहीं होते।
