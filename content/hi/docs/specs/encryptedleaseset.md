---
title: "एन्क्रिप्टेड LeaseSet"
description: "निजी Destinations (गंतव्य) के लिए अभिगम-नियंत्रित LeaseSet प्रारूप"
slug: "encryptedleaseset"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## अवलोकन

यह दस्तावेज़ एन्क्रिप्टेड LeaseSet2 (LS2) के लिए blinding (पहचान/कुंजी छिपाने हेतु यादृच्छिक ढंकना), एन्क्रिप्शन और डीक्रिप्शन को निर्दिष्ट करता है। एन्क्रिप्टेड LeaseSets, I2P नेटवर्क डेटाबेस में छिपी सेवा की जानकारी के पहुँच-नियंत्रित प्रकाशन की सुविधा प्रदान करते हैं।

**मुख्य विशेषताएँ:** - forward secrecy (पुराने सत्रों की गोपनीयता सुरक्षित रखने हेतु) के लिए दैनिक कुंजी परिवर्तन - दो-स्तरीय क्लाइंट प्राधिकरण (DH-based और PSK-based; क्रमशः Diffie–Hellman और pre-shared key पर आधारित) - AES हार्डवेयर के बिना उपकरणों पर बेहतर प्रदर्शन के लिए ChaCha20 एन्क्रिप्शन - key blinding (कुंजी-ब्लाइंडिंग) के साथ Red25519 हस्ताक्षर - गोपनीयता-संरक्षित क्लाइंट सदस्यता

**संबंधित प्रलेखन:** - [सामान्य संरचनाओं की विशिष्टता](/docs/specs/common-structures/) - एन्क्रिप्टेड LeaseSet संरचना - [प्रस्ताव 123: नई netDB प्रविष्टियाँ](/proposals/123-new-netdb-entries/) - एन्क्रिप्टेड LeaseSets पर पृष्ठभूमि - [नेटवर्क डेटाबेस प्रलेखन](/docs/specs/common-structures/) - NetDB उपयोग

---

## संस्करण इतिहास और कार्यान्वयन स्थिति

### प्रोटोकॉल विकास समयरेखा

**संस्करण क्रमांकन पर महत्वपूर्ण नोट:**   I2P दो अलग-अलग संस्करण क्रमांकन प्रणालियों का उपयोग करता है: - **API/Router संस्करण:** 0.9.x श्रृंखला (तकनीकी विनिर्देशों में प्रयुक्त) - **उत्पाद रिलीज़ संस्करण:** 2.x.x श्रृंखला (सार्वजनिक रिलीज़ के लिए प्रयुक्त)

तकनीकी विनिर्देश API संस्करणों का उल्लेख करते हैं (उदा., 0.9.41), जबकि अंतिम उपयोगकर्ता उत्पाद संस्करण देखते हैं (उदा., 2.10.0)।

### कार्यान्वयन मील के पत्थर

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill support for standard LS2, offline keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full encrypted LS2 support, Red25519 (sig type&nbsp;11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.40</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Per-client authorization, encrypted LS2 with offline keys, B32 support</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Protocol finalized as stable</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2.10.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest Java implementation (API version 0.9.61)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>i2pd 2.58.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full C++ implementation compatibility</td></tr>
  </tbody>
</table>
### वर्तमान स्थिति

- ✅ **प्रोटोकॉल स्थिति:** जून 2019 से स्थिर और अपरिवर्तित
- ✅ **Java I2P:** संस्करण 0.9.40+ में पूर्णतः कार्यान्वित
- ✅ **i2pd (C++):** संस्करण 2.58.0+ में पूर्णतः कार्यान्वित
- ✅ **अंतरसंचालनीयता:** कार्यान्वयनों के बीच पूर्ण
- ✅ **नेटवर्क परिनियोजन:** 6+ वर्षों के परिचालन अनुभव के साथ उत्पादन-तैयार

---

## क्रिप्टोग्राफिक परिभाषाएँ

### संकेतन और परंपराएँ

- `||` संयोजन को दर्शाता है
- `mod L` Ed25519 के order के अनुसार मॉड्यूलर अपचयन को दर्शाता है
- अन्यथा निर्दिष्ट न होने पर सभी बाइट ऐरे नेटवर्क बाइट क्रम (big-endian — उच्च-क्रम बाइट पहले) में होते हैं
- Little-endian (निम्न-क्रम बाइट पहले) मान स्पष्ट रूप से दर्शाए जाते हैं

### CSRNG(n)

**क्रिप्टोग्राफिक रूप से सुरक्षित यादृच्छिक संख्या जनरेटर**

कुंजी सामग्री के निर्माण के लिए उपयुक्त, क्रिप्टोग्राफ़िक रूप से सुरक्षित यादृच्छिक डेटा के `n` बाइट्स उत्पन्न करता है।

**सुरक्षा आवश्यकताएँ:** - क्रिप्टोग्राफिक रूप से सुरक्षित होना चाहिए (कुंजी उत्पन्न करने के लिए उपयुक्त) - जब सन्निहित बाइट अनुक्रम नेटवर्क पर उजागर हों, तब सुरक्षित होना चाहिए - कार्यान्वयन को संभावित रूप से अविश्वसनीय स्रोतों से प्राप्त आउटपुट को हैश करना चाहिए

**संदर्भ:** - [PRNG सुरक्षा संबंधी विचार](http://projectbullrun.org/dual-ec/ext-rand.html) - [Tor डेवलपर चर्चा](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)

### H(p, d)

**व्यक्तिकरण के साथ SHA-256 हैश**

डोमेन-पृथक्करण वाला हैश फ़ंक्शन, जो लेता है: - `p`: पर्सनलाइज़ेशन स्ट्रिंग (डोमेन पृथक्करण प्रदान करती है) - `d`: हैश करने हेतु डेटा

**कार्यान्वयन:**

```
H(p, d) := SHA-256(p || d)
```
**उपयोग:** विभिन्न प्रोटोकॉल में SHA-256 के उपयोगों के बीच टकराव हमलों को रोकने के लिए क्रिप्टोग्राफिक डोमेन पृथक्करण प्रदान करता है।

### स्ट्रीम: ChaCha20

**स्ट्रीम सिफर: ChaCha20 जैसा कि RFC 7539 के अनुभाग 2.4 में निर्दिष्ट है**

**पैरामीटर:** - `S_KEY_LEN = 32` (256-बिट कुंजी) - `S_IV_LEN = 12` (96-बिट nonce, एक-बार-प्रयुक्त संख्या) - प्रारंभिक काउंटर: `1` (RFC 7539 0 या 1 की अनुमति देता है; AEAD संदर्भों के लिए 1 अनुशंसित है)

**ENCRYPT(k, iv, plaintext)**

निम्न का उपयोग करके plaintext (साधारण पाठ) को एन्क्रिप्ट करता है: - `k`: 32-बाइट cipher key (कूट-कुंजी) - `iv`: 12-बाइट nonce (एक बार उपयोग होने वाला यादृच्छिक मान; प्रत्येक कुंजी के लिए अद्वितीय होना अनिवार्य है) - plaintext के समान आकार का ciphertext (एन्क्रिप्टेड आउटपुट/सांकेतिक पाठ) लौटाता है

**सुरक्षा गुणधर्म:** यदि कुंजी गोपनीय है, तो पूरा ciphertext (एन्क्रिप्टेड डेटा) यादृच्छिक डेटा से अलग से पहचाना न जा सके।

**DECRYPT(k, iv, ciphertext)**

सिफरटेक्स्ट को डिक्रिप्ट करता है, उपयोग करते हुए: - `k`: 32-बाइट साइफ़र कुंजी - `iv`: 12-बाइट नॉनस (एक बार प्रयुक्त मान) - प्लेनटेक्स्ट (साधारण पाठ) लौटाता है

**डिज़ाइन तर्क:** AES की तुलना में ChaCha20 को चुना गया क्योंकि: - हार्डवेयर-त्वरण के बिना उपकरणों पर AES की तुलना में 2.5-3x तेज - स्थिर-समय (constant-time) कार्यान्वयन हासिल करना आसान - AES-NI उपलब्ध होने पर सुरक्षा और गति तुलनीय

**संदर्भ:** - [RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539) - IETF प्रोटोकॉल्स के लिए ChaCha20 (स्ट्रीम साइफर) और Poly1305 (संदेश प्रमाणीकरण कोड (MAC) एल्गोरिथ्म)

### हस्ताक्षर: Red25519

**हस्ताक्षर योजना: Red25519 (SigType 11) के साथ Key Blinding (कुंजी को छिपाने की तकनीक)**

Red25519, Ed25519 वक्र पर किए गए Ed25519 हस्ताक्षरों पर आधारित है, हैशिंग के लिए SHA-512 का उपयोग करता है, और ZCash RedDSA में निर्दिष्ट key blinding (कुंजी-ब्लाइंडिंग—कुंजी को छिपाने/मास्क करने की तकनीक) का समर्थन करता है।

**फ़ंक्शन्स:**

#### DERIVE_PUBLIC(privkey)

दी गई निजी कुंजी के अनुरूप सार्वजनिक कुंजी लौटाता है। - मानक Ed25519 (एक एलिप्टिक-कर्व हस्ताक्षर योजना) आधार बिंदु पर स्केलर गुणन का उपयोग करता है

#### SIGN(privkey, m)

निजी कुंजी `privkey` से संदेश `m` पर किया गया हस्ताक्षर लौटाता है।

**Red25519 में Ed25519 की तुलना में हस्ताक्षर संबंधी अंतर:** 1. **Random Nonce (एक-बार-प्रयुक्त यादृच्छिक संख्या):** अतिरिक्त 80 बाइट यादृच्छिक डेटा का उपयोग करता है

   ```
   T = CSRNG(80)  // 80 random bytes
   r = H*(T || publickey || message)
   ```
यह Red25519 (एक क्रिप्टोग्राफ़िक हस्ताक्षर योजना) के प्रत्येक हस्ताक्षर को अद्वितीय बनाता है, भले ही संदेश और कुंजी वही हों।

2. **निजी कुंजी निर्माण:** Red25519 की निजी कुंजियाँ यादृच्छिक संख्याओं से उत्पन्न की जाती हैं और `mod L` में घटाई जाती हैं, Ed25519 की bit-clamping (बिटों को निश्चित पैटर्न में बाध्य करना) पद्धति के उपयोग के बजाय।

#### VERIFY(pubkey, m, sig)

हस्ताक्षर `sig` को सार्वजनिक कुंजी `pubkey` और संदेश `m` के विरुद्ध सत्यापित करता है। - अगर हस्ताक्षर वैध है तो `true` लौटाता है, अन्यथा `false` - सत्यापन Ed25519 के समान है

**कुंजी ब्लाइंडिंग क्रियाएँ:**

#### GENERATE_ALPHA(data, secret)

key blinding (कुंजी-अंधीकरण) के लिए alpha उत्पन्न करता है. - `data`: सामान्यतः इसमें signing public key (हस्ताक्षर सार्वजनिक कुंजी) और signature types (हस्ताक्षर प्रकार) होते हैं - `secret`: वैकल्पिक अतिरिक्त secret (रहस्य; यदि उपयोग न हो तो शून्य लंबाई) - परिणाम Ed25519 निजी कुंजियों के समान वितरण का होता है (mod L reduction के बाद)

#### BLIND_PRIVKEY(privkey, alpha)

गुप्त `alpha` का उपयोग करके निजी कुंजी को ब्लाइंड (blinding, छिपाने की तकनीक) करता है। - कार्यान्वयन: `blinded_privkey = (privkey + alpha) mod L` - फील्ड (बीजीय क्षेत्र) में स्केलर अंकगणित का उपयोग करता है

#### BLIND_PUBKEY(pubkey, alpha)

Secret `alpha` का उपयोग करके एक सार्वजनिक कुंजी को blind (क्रिप्टोग्राफ़िक छुपाव) करता है. - कार्यान्वयन: `blinded_pubkey = pubkey + DERIVE_PUBLIC(alpha)` - वक्र पर group element (point) addition का उपयोग करता है

**महत्वपूर्ण विशेषता:**

```
BLIND_PUBKEY(pubkey, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))
```
**सुरक्षा संबंधी विचार:**

ZCash प्रोटोकॉल स्पेसिफिकेशन अनुभाग 5.4.6.1 से: सुरक्षा के लिए, alpha का वितरण ठीक वैसा ही होना चाहिए जैसा ब्लाइंडिंग हटाई गईं निजी कुंजियों का होता है। यह सुनिश्चित करता है कि "पुनः यादृच्छीकृत सार्वजनिक कुंजी और उस कुंजी के अंतर्गत हस्ताक्षर(ों) का संयोजन उस कुंजी को प्रकट नहीं करता जिससे इसे पुनः यादृच्छीकृत किया गया था।"

**समर्थित हस्ताक्षर प्रकार:** - **Type 7 (Ed25519):** मौजूदा destinations (डेस्टिनेशन) के लिए समर्थित (पिछली संगतता) - **Type 11 (Red25519):** एन्क्रिप्शन का उपयोग करने वाले नए destinations के लिए अनुशंसित - **Blinded keys (ब्लाइंडेड कुंजियाँ):** हमेशा Type 11 (Red25519) का उपयोग करें

**संदर्भ:** - [ZCash प्रोटोकॉल विनिर्देश](https://zips.z.cash/protocol/protocol.pdf) - अनुभाग 5.4.6 RedDSA - [I2P Red25519 विनिर्देश](/docs/specs/red25519-signature-scheme/)

### DH (Diffie-Hellman कुंजी विनिमय): X25519

**Elliptic Curve Diffie-Hellman (अण्डाकार वक्र आधारित Diffie-Hellman कुंजी सहमति): X25519**

Curve25519 पर आधारित सार्वजनिक-कुंजी सहमति प्रणाली।

**पैरामीटर्स:** - निजी कुंजियाँ: 32 बाइट्स - सार्वजनिक कुंजियाँ: 32 बाइट्स - साझा रहस्य आउटपुट: 32 बाइट्स

**फ़ंक्शंस:**

#### GENERATE_PRIVATE()

CSRNG (Cryptographically Secure Random Number Generator—क्रिप्टोग्राफ़िक रूप से सुरक्षित रैंडम नंबर जनरेटर) का उपयोग करके एक नई 32-बाइट निजी कुंजी उत्पन्न करता है।

#### DERIVE_PUBLIC(privkey)

दी गई निजी कुंजी से 32-बाइट सार्वजनिक कुंजी व्युत्पन्न करता है. - Curve25519 पर स्केलर गुणन (scalar multiplication) का उपयोग करता है

#### DH(privkey, pubkey)

Diffie-Hellman कुंजी समझौता निष्पादित करता है। - `privkey`: स्थानीय 32-बाइट निजी कुंजी - `pubkey`: दूरस्थ 32-बाइट सार्वजनिक कुंजी - रिटर्न: 32-बाइट साझा रहस्य

**सुरक्षा विशेषताएँ:** - Curve25519 पर गणनात्मक Diffie-Hellman मान्यता - जब क्षणिक कुंजियाँ उपयोग की जाती हैं तो Forward secrecy (पिछला संचार सुरक्षित रहता है) - टाइमिंग हमलों को रोकने के लिए समय-स्थिर कार्यान्वयन आवश्यक है

**संदर्भ:** - [RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748) - सुरक्षा के लिए दीर्घवृत्तीय वक्र

### HKDF (HMAC-आधारित कुंजी व्युत्पत्ति फ़ंक्शन)

**HMAC-आधारित कुंजी व्युत्पत्ति फ़ंक्शन**

इनपुट कुंजी सामग्री से कुंजी सामग्री का निष्कर्षण और विस्तार करता है।

**पैरामीटर्स:** - `salt`: अधिकतम 32 बाइट्स (आम तौर पर SHA-256 के लिए 32 बाइट्स) - `ikm`: इनपुट कुंजी-सामग्री (किसी भी लंबाई की, अच्छी एंट्रॉपी होनी चाहिए) - `info`: संदर्भ-विशिष्ट जानकारी (डोमेन पृथक्करण) - `n`: आउटपुट की लंबाई बाइट्स में

**कार्यान्वयन:**

RFC 5869 में निर्दिष्ट अनुसार HKDF का उपयोग किया जाता है, निम्न के साथ: - **हैश फ़ंक्शन:** SHA-256 - **HMAC:** RFC 2104 में निर्दिष्ट अनुसार - **सॉल्ट की लंबाई:** अधिकतम 32 बाइट (SHA-256 के लिए HashLen (हैश लंबाई))

**उपयोग पैटर्न:**

```
keys = HKDF(salt, ikm, info, n)
```
**डोमेन पृथक्करण:** `info` पैरामीटर प्रोटोकॉल में HKDF (HMAC-आधारित कुंजी व्युत्पन्न फ़ंक्शन) के विभिन्न उपयोगों के बीच क्रिप्टोग्राफिक डोमेन पृथक्करण प्रदान करता है।

**सत्यापित जानकारी मान:** - `"ELS2_L1K"` - लेयर 1 (बाहरी) एन्क्रिप्शन - `"ELS2_L2K"` - लेयर 2 (आंतरिक) एन्क्रिप्शन - `"ELS2_XCA"` - DH क्लाइंट प्राधिकरण - `"ELS2PSKA"` - PSK क्लाइंट प्राधिकरण - `"i2pblinding1"` - अल्फ़ा निर्माण

**संदर्भ:** - [RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869) - HKDF विनिर्देश - [RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104) - HMAC विनिर्देश

---

## प्रारूप विनिर्देश

कूटबद्ध LS2 तीन घोंसलेदार परतों से बना होता है:

1. **लेयर 0 (बाहरी):** भंडारण और पुनर्प्राप्ति के लिए सादा पाठ जानकारी
2. **लेयर 1 (मध्य):** क्लाइंट प्रमाणीकरण डेटा (कूटबद्ध)
3. **लेयर 2 (आंतरिक):** वास्तविक LeaseSet2 डेटा (कूटबद्ध)

**समग्र संरचना:**

```
Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature
```
**महत्वपूर्ण:** एन्क्रिप्टेड LS2 blinded keys (गोपनीयता हेतु छिपाई गई कुंजियाँ) का उपयोग करता है. Destination (गंतव्य पहचान) हैडर में शामिल नहीं होता. DHT का भंडारण स्थान `SHA-256(sig type || blinded public key)` है, जिसे प्रतिदिन बदला जाता है.

### स्तर 0 (बाहरी) - सादा पाठ

Layer 0 मानक LS2 header का उपयोग नहीं करता है। इसमें blinded keys (ब्लाइंडिंग तकनीक से छिपाई गई कुंजियाँ) के लिए अनुकूलित एक कस्टम प्रारूप है।

**संरचना:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Not in header, from DatabaseStore message field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, always <code>0x000b</code> (Red25519 type 11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 blinded public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch (rolls over in 2106)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, offset from published in seconds (max 65,535 &asymp; 18.2 hours)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Bit flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Transient Key Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present if flag bit&nbsp;0 is set</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, length of outer ciphertext</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">outerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;1 data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 signature over all preceding data</td></tr>
  </tbody>
</table>
**फ्लैग्स फ़ील्ड (2 बाइट, बिट 15-0):** - **बिट 0:** ऑफ़लाइन कुंजियों का संकेतक   - `0` = कोई ऑफ़लाइन कुंजियाँ नहीं   - `1` = ऑफ़लाइन कुंजियाँ मौजूद हैं (अस्थायी कुंजी डेटा आगे आता है) - **बिट्स 1-15:** आरक्षित, भविष्य की संगतता के लिए 0 होना चाहिए

**अस्थायी कुंजी डेटा (यदि फ़्लैग बिट 0 = 1 हो तो):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Signing Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length implied by signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signed by blinded public key; covers expires timestamp, transient sig type, and transient public key</td></tr>
  </tbody>
</table>
**हस्ताक्षर सत्यापन:** - **ऑफ़लाइन कुंजियों के बिना:** ब्लाइंडेड सार्वजनिक कुंजी के साथ सत्यापित करें - **ऑफ़लाइन कुंजियों के साथ:** अस्थायी सार्वजनिक कुंजी के साथ सत्यापित करें

हस्ताक्षर Type से लेकर outerCiphertext तक (दोनों सहित) सभी डेटा को शामिल करता है।

### परत 1 (मध्य) - क्लाइंट प्राधिकरण

**डिक्रिप्शन:** [लेयर 1 एन्क्रिप्शन](#layer-1-encryption) अनुभाग देखें।

**संरचना:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Authorization flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Auth Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present based on flags</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">innerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;2 data (remainder)</td></tr>
  </tbody>
</table>
**फ्लैग्स फ़ील्ड (1 बाइट, बिट्स 7-0):** - **बिट 0:** प्राधिकरण मोड   - `0` = प्रति-क्लाइंट प्राधिकरण नहीं (सभी)   - `1` = प्रति-क्लाइंट प्राधिकरण (प्रमाणीकरण अनुभाग आगे आता है) - **बिट्स 3-1:** प्रमाणीकरण स्कीम (केवल तब जब बिट 0 = 1)   - `000` = DH क्लाइंट प्रमाणीकरण   - `001` = PSK क्लाइंट प्रमाणीकरण   - अन्य आरक्षित - **बिट्स 7-4:** अप्रयुक्त, 0 होना आवश्यक है

**DH क्लाइंट प्राधिकरण डेटा (फ्लैग्स = 0x01, बिट्स 3-1 = 000):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ephemeralPublicKey</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Server's ephemeral X25519 public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**authClient प्रविष्टि (40 बाइट):** - `clientID_i`: 8 बाइट - `clientCookie_i`: 32 बाइट (कूटबद्ध authCookie)

**PSK क्लाइंट प्राधिकरण डेटा (flags = 0x03, bits 3-1 = 001):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authSalt</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Salt for PSK key derivation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**authClient एंट्री (40 बाइट्स):** - `clientID_i`: 8 बाइट्स - `clientCookie_i`: 32 बाइट्स (एन्क्रिप्टेड authCookie)

### परत 2 (आंतरिक) - LeaseSet डेटा

**डिक्रिप्शन:** [लेयर 2 एन्क्रिप्शन](#layer-2-encryption) अनुभाग देखें।

**संरचना:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>3</code> (LS2) or <code>7</code> (Meta LS2)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Complete LeaseSet2 or MetaLeaseSet2</td></tr>
  </tbody>
</table>
आंतरिक परत में LeaseSet2 की पूर्ण संरचना शामिल है, जिसमें: - LS2 header - Lease संबंधी जानकारी - LS2 signature

**सत्यापन आवश्यकताएँ:** डिक्रिप्शन के बाद, इम्प्लीमेंटेशन को निम्नलिखित का सत्यापन करना चाहिए: 1. आंतरिक टाइमस्टैम्प बाहरी प्रकाशित टाइमस्टैम्प से मेल खाता हो 2. आंतरिक समाप्ति बाहरी समाप्ति से मेल खाती हो 3. LS2 का डिजिटल हस्ताक्षर मान्य हो 4. Lease (I2P में LeaseSet का एक प्रविष्टि) डेटा सुव्यवस्थित हो

**संदर्भ:** - [सामान्य संरचनाओं का विनिर्देश](/docs/specs/common-structures/) - LeaseSet2 स्वरूप विवरण

---

## Blinding (छिपाने की तकनीक) कुंजी व्युत्पत्ति

### अवलोकन

I2P, Ed25519 और ZCash RedDSA पर आधारित एक additive key blinding scheme (जोड़-आधारित कुंजी ब्लाइंडिंग योजना) का उपयोग करता है। forward secrecy (आगे की गोपनीयता) के लिए ब्लाइंडेड कुंजियाँ प्रतिदिन (UTC मध्यरात्रि) बदली जाती हैं।

**डिज़ाइन का औचित्य:**

I2P ने स्पष्ट रूप से Tor के rend-spec-v3.txt के परिशिष्ट A.2 में वर्णित दृष्टिकोण का उपयोग न करने का निर्णय लिया। विनिर्देशन के अनुसार:

> "हम Tor के rend-spec-v3.txt के परिशिष्ट A.2 का उपयोग नहीं करते, जिसके डिज़ाइन लक्ष्य समान हैं, क्योंकि उसकी ब्लाइंडेड सार्वजनिक कुंजियाँ prime-order subgroup (अभाज्य-आदेश उपसमूह) से बाहर हो सकती हैं, और इसके सुरक्षा निहितार्थ अज्ञात हैं."

I2P की additive blinding (योगात्मक ब्लाइंडिंग) यह गारंटी देती है कि ब्लाइंडेड कुंजियाँ Ed25519 curve के अभाज्य-क्रम उपसमूह में बनी रहें।

### गणितीय परिभाषाएँ

**Ed25519 पैरामीटर्स:** - `B`: Ed25519 आधार बिंदु (generator, जनक) = `2^255 - 19` - `L`: Ed25519 order (क्रम) = `2^252 + 27742317777372353535851937790883648493`

**मुख्य चर:** - `A`: Unblinded (ब्लाइंडिंग रहित) 32-बाइट हस्ताक्षर हेतु सार्वजनिक कुंजी (in Destination) - `a`: Unblinded 32-बाइट हस्ताक्षर हेतु निजी कुंजी - `A'`: Blinded (ब्लाइंडिंग लागू) 32-बाइट हस्ताक्षर हेतु सार्वजनिक कुंजी (एन्क्रिप्टेड LeaseSet में प्रयुक्त) - `a'`: Blinded 32-बाइट हस्ताक्षर हेतु निजी कुंजी - `alpha`: 32-बाइट blinding factor (ब्लाइंडिंग गुणांक) (गोपनीय)

**सहायक फ़ंक्शंस:**

#### LEOS2IP(x)

"Little-Endian (सबसे कम महत्त्वपूर्ण बाइट पहले) Octet String (8-बिट की स्ट्रिंग) का पूर्णांक में रूपांतरण"

किसी बाइट ऐरे को little-endian (जहाँ सबसे कम महत्त्वपूर्ण बाइट पहले आती है) क्रम से पूर्णांक निरूपण में परिवर्तित करता है।

#### H*(x)

"हैश और रिड्यूस"

```
H*(x) = (LEOS2IP(SHA512(x))) mod L
```
Ed25519 (एक एलिप्टिक-कर्व हस्ताक्षर एल्गोरिथ्म) की कुंजी निर्माण में जैसा ऑपरेशन होता है, वैसा ही।

### अल्फ़ा पीढ़ी

**दैनिक रोटेशन:** प्रत्येक दिन UTC मध्यरात्रि (00:00:00 UTC) पर नई alpha (एक आंतरिक क्रिप्टोग्राफ़िक पैरामीटर) और blinded keys (ब्लाइंडिंग की गई कुंजियाँ) अनिवार्य रूप से उत्पन्न की जानी चाहिए।

**GENERATE_ALPHA(destination, date, secret) एल्गोरिद्म:**

```python
# Input parameters
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes, big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes, big endian) 
     # Always 0x000b (Red25519)
datestring = "YYYYMMDD" (8 bytes ASCII from current UTC date)
secret = optional UTF-8 encoded string (zero-length if not used)

# Computation
keydata = A || stA || stA'  # 36 bytes total
seed = HKDF(
    salt=H("I2PGenerateAlpha", keydata),
    ikm=datestring || secret,
    info="i2pblinding1",
    n=64
)

# Treat seed as 64-byte little-endian integer and reduce
alpha = seed mod L
```
**सत्यापित पैरामीटर:** - Salt personalization (व्यक्तिकरण): `"I2PGenerateAlpha"` - HKDF info (जानकारी): `"i2pblinding1"` - आउटपुट: रिडक्शन से पहले 64 बाइट्स - अल्फ़ा वितरण: `mod L` के बाद Ed25519 निजी कुंजियों की तरह समान वितरण

### निजी कुंजी ब्लाइंडिंग

**BLIND_PRIVKEY(a, alpha) एल्गोरिथ्म:**

एन्क्रिप्टेड LeaseSet प्रकाशित करने वाले destination (I2P गंतव्य/पहचान) के मालिक के लिए:

```python
# For Ed25519 private key (type 7)
if sigtype == 7:
    seed = destination's signing private key (32 bytes)
    a = left_half(SHA512(seed))  # 32 bytes
    a = clamp(a)  # Ed25519 clamping
    
# For Red25519 private key (type 11)
elif sigtype == 11:
    a = destination's signing private key (32 bytes)
    # No clamping for Red25519

# Additive blinding using scalar arithmetic
blinded_privkey = a' = (a + alpha) mod L

# Derive blinded public key
blinded_pubkey = A' = DERIVE_PUBLIC(a')
```
**महत्वपूर्ण:** `mod L` रिडक्शन निजी और सार्वजनिक कुंजियों के बीच सही बीजगणितीय संबंध बनाए रखने के लिए अत्यावश्यक है।

### Public Key Blinding (क्रिप्टोग्राफी में वह तकनीक जिसमें सार्वजनिक कुंजी का प्रयोग कर इनपुट/हस्ताक्षर को पहले से छिपा दिया जाता है)

**BLIND_PUBKEY(A, alpha) एल्गोरिथ्म:**

एन्क्रिप्टेड LeaseSet को प्राप्त करने और सत्यापित करने वाले क्लाइंट्स के लिए:

```python
alpha = GENERATE_ALPHA(destination, date, secret)
A = destination's signing public key (32 bytes)

# Additive blinding using group elements (curve points)
blinded_pubkey = A' = A + DERIVE_PUBLIC(alpha)
```
**गणितीय समकक्षता:**

दोनों विधियाँ समान परिणाम देती हैं:

```
BLIND_PUBKEY(A, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(a, alpha))
```
ऐसा इसलिए है:

```
A' = A + [alpha]B
   = [a]B + [alpha]B
   = [a + alpha]B  (group operation)
   = DERIVE_PUBLIC(a + alpha mod L)
```
### Blinded Keys (ब्लाइंड की गई कुंजियाँ) के साथ हस्ताक्षर

**बिना ब्लाइंडिंग के LeaseSet हस्ताक्षर:**

unblinded (ब्लाइंडिंग हटाया हुआ) LeaseSet (जो सीधे प्रमाणीकृत क्लाइंट्स को भेजा जाता है) पर हस्ताक्षर इनका उपयोग करके किया जाता है: - मानक Ed25519 (type 7) या Red25519 (type 11) हस्ताक्षर - Unblinded हस्ताक्षर करने की निजी कुंजी - unblinded सार्वजनिक कुंजी से सत्यापित

**ऑफलाइन कुंजियों के साथ:** - unblinded transient (जिसमें blinding नहीं होता, अस्थायी) निजी कुंजी से हस्ताक्षरित - unblinded transient सार्वजनिक कुंजी से सत्यापित - दोनों का प्रकार 7 या 11 होना चाहिए

**एन्क्रिप्टेड LeaseSet हस्ताक्षर:**

एन्क्रिप्टेड LeaseSet का बाहरी भाग blinded keys (ब्लाइंडेड कुंजियाँ) के साथ Red25519 हस्ताक्षरों का उपयोग करता है।

**Red25519 हस्ताक्षर एल्गोरिदम:**

```python
# Generate per-signature random nonce
T = CSRNG(80)  # 80 random bytes

# Calculate r (differs from Ed25519)
r = H*(T || blinded_pubkey || message)

# Rest is same as Ed25519
R = [r]B
S = (r + H(R || A' || message) * a') mod L
signature = R || S  # 64 bytes total
```
**Ed25519 से मुख्य अंतर:** 1. 80 बाइट के यादृच्छिक डेटा `T` का उपयोग करता है (न कि निजी कुंजी का हैश) 2. सार्वजनिक कुंजी के मान का सीधे उपयोग करता है (न कि निजी कुंजी का हैश) 3. हर हस्ताक्षर अद्वितीय होता है, भले ही संदेश और कुंजी वही हों

**सत्यापन:**

Ed25519 के समान:

```python
# Parse signature
R = signature[0:32]
S = signature[32:64]

# Verify equation: [S]B = R + [H(R || A' || message)]A'
return [S]B == R + [H(R || A' || message)]A'
```
### सुरक्षा संबंधी विचार

**अल्फा वितरण:**

सुरक्षा के लिए, alpha का वितरण unblinded (ब्लाइंडिंग हटाए गए) निजी कुंजियों के समान होना चाहिए। जब Ed25519 (type 7) को Red25519 (type 11) में ब्लाइंडिंग किया जाता है, तो वितरणों में थोड़ा अंतर रहता है।

**सिफारिश:** ZCash की आवश्यकताओं को पूरा करने के लिए अनब्लाइंडेड और ब्लाइंडेड दोनों प्रकार की कुंजियों के लिए Red25519 (type 11) का उपयोग करें: "पुनः-यादृच्छीकृत सार्वजनिक कुंजी और उसी कुंजी के अंतर्गत हस्ताक्षर(ों) का संयोजन उस मूल कुंजी का खुलासा नहीं करता जिससे उसे पुनः-यादृच्छीकृत किया गया था।"

**प्रकार 7 समर्थन:** Ed25519 (एक एलिप्टिक-कर्व डिजिटल हस्ताक्षर एल्गोरिथ्म) मौजूदा गंतव्यों के साथ बैकवर्ड संगतता के लिए समर्थित है, लेकिन नए एन्क्रिप्टेड गंतव्यों के लिए प्रकार 11 की अनुशंसा की जाती है।

**दैनिक रोटेशन के लाभ:** - Forward secrecy: आज की blinded key से समझौता हो जाए तो भी बीते दिन की कुंजी उजागर नहीं होती - Unlinkability (संबंध न जोड़ा जा सकना): दैनिक रोटेशन DHT (वितरित हैश तालिका) के माध्यम से दीर्घकालिक ट्रैकिंग को रोकता है - कुंजी पृथक्करण: विभिन्न समय अवधियों के लिए अलग-अलग कुंजियाँ

**संदर्भ:** - [ZCash प्रोटोकॉल विनिर्देश](https://zips.z.cash/protocol/protocol.pdf) - अनुभाग 5.4.6.1 - [Tor Key Blinding (कुंजी-ब्लाइंडिंग) पर चर्चा](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html) - [Tor टिकट #8106](https://trac.torproject.org/projects/tor/ticket/8106)

---

## कूटलेखन और प्रसंस्करण

### Subcredential (उप-प्रमाण-पत्र) की व्युत्पत्ति

एन्क्रिप्शन से पहले, हम एक क्रेडेंशियल और एक उप-क्रेडेंशियल व्युत्पन्न करते हैं, ताकि एन्क्रिप्टेड परतों को Destination (I2P में एंडपॉइंट/गंतव्य पहचान) की हस्ताक्षर सार्वजनिक कुंजी के ज्ञान से संबद्ध किया जा सके।

**लक्ष्य:** यह सुनिश्चित करना कि केवल वे लोग जो Destination की हस्ताक्षर करने वाली सार्वजनिक कुंजी जानते हों, एन्क्रिप्टेड LeaseSet को डिक्रिप्ट कर सकें। पूरा Destination आवश्यक नहीं है।

#### प्रमाण-पत्र की गणना

```python
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes big endian)
     # Always 0x000b (Red25519)

keydata = A || stA || stA'  # 36 bytes

credential = H("credential", keydata)  # 32 bytes
```
**डोमेन पृथक्करण:** पर्सनलाइज़ेशन स्ट्रिंग `"credential"` सुनिश्चित करती है कि यह हैश किसी भी DHT (वितरित हैश तालिका) लुकअप कुंजियों या प्रोटोकॉल में अन्य उपयोगों से टकराव न हो।

#### Subcredential (उप-प्रमाण-पत्र) की गणना

```python
blindedPublicKey = A' (32 bytes, from blinding process)

subcredential = H("subcredential", credential || blindedPublicKey)  # 32 bytes
```
**उद्देश्य:** subcredential (उप-क्रेडेंशियल) एन्क्रिप्टेड LeaseSet को इनसे जोड़ता है: 1. विशिष्ट Destination (गंतव्य) (credential के माध्यम से) 2. विशिष्ट blinded key (ब्लाइंडेड कुंजी) (blindedPublicKey के माध्यम से) 3. विशिष्ट दिन (blindedPublicKey के दैनिक रोटेशन के माध्यम से)

यह रीप्ले हमलों और cross-day linking (अलग-अलग दिनों में गतिविधियों को जोड़कर संबंध निकालना) को रोकता है।

### लेयर 1 एन्क्रिप्शन

**संदर्भ:** लेयर 1 में क्लाइंट प्राधिकरण डेटा शामिल होता है और इसे subcredential (उप-प्रमाणपत्र) से व्युत्पन्न कुंजी से एन्क्रिप्ट किया गया है।

#### एन्क्रिप्शन एल्गोरिदम

```python
# Prepare input
outerInput = subcredential || publishedTimestamp
# publishedTimestamp: 4 bytes from Layer 0

# Generate random salt
outerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

outerKey = keys[0:31]    # 32 bytes (indices 0-31 inclusive)
outerIV = keys[32:43]    # 12 bytes (indices 32-43 inclusive)

# Encrypt and prepend salt
outerPlaintext = [Layer 1 data]
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
**आउटपुट:** `outerCiphertext` की लंबाई `32 + len(outerPlaintext)` बाइट्स है।

**सुरक्षा गुण:** - सॉल्ट समान subcredential (उप-प्रमाण-पत्र) होने पर भी अद्वितीय कुंजी/IV जोड़े सुनिश्चित करता है - संदर्भ स्ट्रिंग `"ELS2_L1K"` डोमेन पृथक्करण प्रदान करती है - ChaCha20 semantic security (सिफरटेक्स्ट यादृच्छिक से अविभेद्य) प्रदान करता है

#### डिक्रिप्शन एल्गोरिदम

```python
# Parse salt from ciphertext
outerSalt = outerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV (same process as encryption)
outerInput = subcredential || publishedTimestamp
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",
    n=44
)

outerKey = keys[0:31]    # 32 bytes
outerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
**सत्यापन:** डिक्रिप्शन के बाद, लेयर 2 पर आगे बढ़ने से पहले यह जांचें कि लेयर 1 की संरचना सही ढंग से निर्मित है।

### लेयर 2 एन्क्रिप्शन

**संदर्भ:** लेयर 2 में वास्तविक LeaseSet2 डेटा होता है और इसे ऐसी कुंजी से एन्क्रिप्ट किया जाता है जो authCookie से (यदि प्रति-क्लाइंट प्रमाणीकरण सक्षम है) या रिक्त स्ट्रिंग से (यदि नहीं) व्युत्पन्न होती है।

#### एन्क्रिप्शन एल्गोरिथ्म

```python
# Determine authCookie based on authorization mode
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Prepare input
innerInput = authCookie || subcredential || publishedTimestamp

# Generate random salt
innerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Encrypt and prepend salt
innerPlaintext = [Layer 2 data: LS2 type byte + LeaseSet2 data]
innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
**आउटपुट:** `innerCiphertext` की लंबाई `32 + len(innerPlaintext)` बाइट्स है।

**Key Binding (कुंजी-संबंधन):** - यदि क्लाइंट प्रमाणीकरण नहीं है: केवल subcredential (उप-क्रेडेंशियल) और टाइमस्टैम्प से बंधा होता है - यदि क्लाइंट प्रमाणीकरण सक्षम है: अतिरिक्त रूप से authCookie से भी बंधा होता है (प्रत्येक अधिकृत क्लाइंट के लिए अलग)

#### डिक्रिप्शन एल्गोरिथ्म

```python
# Determine authCookie (same as encryption)
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Parse salt from ciphertext
innerSalt = innerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV
innerInput = authCookie || subcredential || publishedTimestamp
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",
    n=44
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
**सत्यापन:** डिक्रिप्शन के बाद: 1. सत्यापित करें कि LS2 का टाइप बाइट मान्य है (3 या 7) 2. LeaseSet2 संरचना को पार्स करें 3. सत्यापित करें कि आंतरिक टाइमस्टैम्प बाहरी प्रकाशित टाइमस्टैम्प से मेल खाता है 4. सत्यापित करें कि आंतरिक समाप्ति बाहरी समाप्ति से मेल खाती है 5. LeaseSet2 के हस्ताक्षर का सत्यापन करें

### एन्क्रिप्शन परत का सारांश

```
┌─────────────────────────────────────────────────┐
│ Layer 0 (Plaintext)                             │
│ - Blinded public key                            │
│ - Timestamps                                    │
│ - Signature                                     │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Layer 1 (Encrypted with subcredential)  │   │
│  │ - Authorization flags                   │   │
│  │ - Client auth data (if enabled)         │   │
│  │                                          │   │
│  │  ┌────────────────────────────────┐     │   │
│  │  │ Layer 2 (Encrypted with        │     │   │
│  │  │          authCookie + subcred) │     │   │
│  │  │ - LeaseSet2 type               │     │   │
│  │  │ - LeaseSet2 data               │     │   │
│  │  │ - Leases                       │     │   │
│  │  │ - LS2 signature                │     │   │
│  │  └────────────────────────────────┘     │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```
**डिक्रिप्शन प्रक्रिया:** 1. लेयर 0 के हस्ताक्षर को blinded public key (ब्लाइंडेड पब्लिक की) से सत्यापित करें 2. subcredential (उप-क्रेडेंशियल) का उपयोग करके लेयर 1 को डिक्रिप्ट करें 3. authCookie प्राप्त करने के लिए प्राधिकरण डेटा (यदि उपस्थित हो) को प्रोसेस करें 4. authCookie और subcredential का उपयोग करके लेयर 2 को डिक्रिप्ट करें 5. LeaseSet2 को सत्यापित करें और पार्स करें

---

## प्रति-क्लाइंट अधिकार-प्रदान

### अवलोकन

जब प्रति-क्लाइंट प्राधिकरण सक्षम होता है, तो सर्वर अधिकृत क्लाइंटों की सूची बनाए रखता है। प्रत्येक क्लाइंट के पास key material (कुंजी-सामग्री) होता है, जिसे सुरक्षित रूप से out-of-band (मुख्य चैनल से अलग माध्यम) प्रेषित किया जाना चाहिए।

**दो प्राधिकरण तंत्र:** 1. **DH (Diffie-Hellman) क्लाइंट प्राधिकरण:** अधिक सुरक्षित, X25519 key agreement का उपयोग करता है 2. **PSK (Pre-Shared Key — पूर्व-साझा कुंजी) प्राधिकरण:** सरल, सममित कुंजियों का उपयोग करता है

**सामान्य सुरक्षा गुणधर्म:** - क्लाइंट सदस्यता गोपनीयता: पर्यवेक्षक क्लाइंटों की संख्या देख सकते हैं लेकिन विशिष्ट क्लाइंटों की पहचान नहीं कर सकते - गुमनाम क्लाइंट जोड़/निरसन: यह ट्रैक नहीं किया जा सकता कि विशिष्ट क्लाइंट कब जोड़े या हटाए गए हैं - 8-बाइट क्लाइंट पहचानकर्ता टकराव की संभावना: ~18 क्विंटिलियन में 1 (नगण्य)

### DH (डिफ़ी-हेलमैन) क्लाइंट प्राधिकरण

**सारांश:** प्रत्येक क्लाइंट एक X25519 कुंजी-युग्म उत्पन्न करता है और अपनी सार्वजनिक कुंजी को एक सुरक्षित आउट-ऑफ-बैंड चैनल के माध्यम से सर्वर को भेजता है। सर्वर अस्थायी DH का उपयोग करके प्रत्येक क्लाइंट के लिए एक अद्वितीय authCookie को कूटबद्ध करता है।

#### क्लाइंट कुंजी सृजन

```python
# Client generates keypair
csk_i = GENERATE_PRIVATE()  # 32-byte X25519 private key
cpk_i = DERIVE_PUBLIC(csk_i)  # 32-byte X25519 public key

# Client sends cpk_i to server via secure out-of-band channel
# Client KEEPS csk_i secret (never transmitted)
```
**सुरक्षा लाभ:** क्लाइंट की निजी कुंजी कभी उनके डिवाइस से बाहर नहीं जाती। out-of-band transmission (मुख्य संचार चैनल से अलग माध्यम द्वारा प्रेषण) को अवरोधित करने वाला विरोधी X25519 DH को तोड़े बिना भविष्य के एन्क्रिप्टेड LeaseSets को डिक्रिप्ट नहीं कर सकता।

#### सर्वर प्रसंस्करण

```python
# Server generates new auth cookie and ephemeral keypair
authCookie = CSRNG(32)  # 32-byte cookie

esk = GENERATE_PRIVATE()  # 32-byte ephemeral private key
epk = DERIVE_PUBLIC(esk)  # 32-byte ephemeral public key

# For each authorized client i
for cpk_i in authorized_clients:
    # Perform DH key agreement
    sharedSecret = DH(esk, cpk_i)  # 32 bytes
    
    # Derive client-specific encryption key
    authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
    okm = HKDF(
        salt=epk,  # Ephemeral public key as salt
        ikm=authInput,
        info="ELS2_XCA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**लेयर 1 डेटा संरचना:**

```
ephemeralPublicKey (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
**सर्वर अनुशंसाएँ:** - प्रत्येक प्रकाशित एन्क्रिप्टेड LeaseSet के लिए नया अस्थायी कुंजी-युग्म उत्पन्न करें - स्थिति-आधारित ट्रैकिंग रोकने के लिए क्लाइंट क्रम को यादृच्छिक करें - वास्तविक क्लाइंट संख्या छिपाने के लिए डमी प्रविष्टियाँ जोड़ने पर विचार करें

#### क्लाइंट प्रसंस्करण

```python
# Client has: csk_i (their private key), destination, date, secret
# Client receives: encrypted LeaseSet with epk in Layer 1

# Perform DH key agreement with server's ephemeral public key
sharedSecret = DH(csk_i, epk)  # 32 bytes

# Derive expected client identifier and decryption key
cpk_i = DERIVE_PUBLIC(csk_i)  # Client's own public key
authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=epk,
    ikm=authInput,
    info="ELS2_XCA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
**क्लाइंट त्रुटि प्रबंधन:** - यदि `clientID_i` नहीं मिला: क्लाइंट रद्द कर दिया गया है या कभी अधिकृत नहीं किया गया - यदि डिक्रिप्शन विफल हो: डेटा भ्रष्ट है या कुंजियाँ गलत हैं (अत्यंत दुर्लभ) - रद्दीकरण का पता लगाने के लिए क्लाइंट्स को नियमित रूप से पुनः फ़ेच करना चाहिए

### PSK (पूर्व-साझा कुंजी) क्लाइंट प्राधिकरण

**अवलोकन:** प्रत्येक क्लाइंट के पास एक पूर्व-साझा 32-बाइट सममित कुंजी होती है। सर्वर प्रत्येक क्लाइंट की PSK (पूर्व-साझा कुंजी) का उपयोग करके उसी authCookie को एन्क्रिप्ट करता है।

#### कुंजी निर्माण

```python
# Option 1: Client generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Client sends psk_i to server via secure out-of-band channel

# Option 2: Server generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Server sends psk_i to one or more clients via secure out-of-band channel
```
**सुरक्षा नोट:** आवश्यकता होने पर एक ही PSK (pre-shared key, पूर्व-साझा कुंजी) को कई क्लाइंट्स के बीच साझा किया जा सकता है (जिससे "समूह" प्राधिकरण बनता है)।

#### सर्वर प्रसंस्करण

```python
# Server generates new auth cookie and salt
authCookie = CSRNG(32)  # 32-byte cookie
authSalt = CSRNG(32)     # 32-byte salt

# For each authorized client i
for psk_i in authorized_clients:
    # Derive client-specific encryption key
    authInput = psk_i || subcredential || publishedTimestamp
    
    okm = HKDF(
        salt=authSalt,
        ikm=authInput,
        info="ELS2PSKA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**लेयर 1 डेटा संरचना:**

```
authSalt (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
#### क्लाइंट प्रसंस्करण

```python
# Client has: psk_i (their pre-shared key), destination, date, secret
# Client receives: encrypted LeaseSet with authSalt in Layer 1

# Derive expected client identifier and decryption key
authInput = psk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=authSalt,
    ikm=authInput,
    info="ELS2PSKA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
### तुलना और अनुशंसाएँ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">DH Authorization</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">PSK Authorization</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Exchange</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Asymmetric (X25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric (shared secret)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Security</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Higher (forward secrecy)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Lower (depends on PSK secrecy)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Client Privacy</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Private key never transmitted</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK must be transmitted securely</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Performance</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 DH operations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">No DH operations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Sharing</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">One key per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Can share key among multiple clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Revocation Detection</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary cannot tell when revoked</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary can track revocation if PSK intercepted</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">High security requirements</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Performance-critical or group access</td></tr>
  </tbody>
</table>
**अनुशंसा:** - **DH प्राधिकरण का उपयोग करें** उच्च-सुरक्षा अनुप्रयोगों के लिए, जहाँ forward secrecy (आगे की गोपनीयता) महत्वपूर्ण हो - **PSK (pre-shared key, पहले से साझा कुंजी) प्राधिकरण का उपयोग करें** जब प्रदर्शन अत्यंत महत्वपूर्ण हो या क्लाइंट समूहों का प्रबंधन करना हो - **PSK को कभी भी पुनः उपयोग न करें** अलग-अलग सेवाओं या समयावधियों में - **हमेशा सुरक्षित चैनलों का उपयोग करें** कुंजी वितरण के लिए (उदा., Signal, OTR, PGP)

### सुरक्षा संबंधी विचार

**क्लाइंट सदस्यता गोपनीयता:**

दोनों तंत्र क्लाइंट सदस्यता की गोपनीयता इन माध्यमों से प्रदान करते हैं: 1. **एन्क्रिप्टेड क्लाइंट पहचानकर्ता:** HKDF आउटपुट से व्युत्पन्न 8-बाइट clientID 2. **अविभेद्य कुकीज़:** सभी 32-बाइट clientCookie मान यादृच्छिक प्रतीत होते हैं 3. **क्लाइंट-विशिष्ट मेटाडेटा नहीं:** किस प्रविष्टि का संबंध किस क्लाइंट से है, यह पहचानने का कोई तरीका नहीं

एक पर्यवेक्षक देख सकता है: - अधिकृत क्लाइंट्स की संख्या (`clients` फ़ील्ड से) - समय के साथ क्लाइंट संख्या में परिवर्तन

एक पर्यवेक्षक यह नहीं देख सकता: - कौन से विशिष्ट क्लाइंट अधिकृत हैं - कब विशिष्ट क्लाइंट जोड़े या हटाए जाते हैं (यदि गिनती समान रहती है) - क्लाइंट की पहचान बताने वाली कोई भी जानकारी

**यादृच्छिकरण संबंधी सिफारिशें:**

सर्वरों को हर बार जब वे एक एन्क्रिप्टेड LeaseSet उत्पन्न करते हैं, क्लाइंट क्रम को यादृच्छिक करना चाहिए:

```python
import random

# Before serializing
auth_entries = [(clientID_i, clientCookie_i) for each client]
random.shuffle(auth_entries)
# Now serialize in randomized order
```
**लाभ:** - क्लाइंट्स को सूची में अपनी स्थिति जानने से रोकता है - स्थिति परिवर्तन के आधार पर होने वाले inference attacks (अनुमान-आधारित हमले) को रोकता है - क्लाइंट जोड़/निरस्तीकरण को अप्रभेद्य बनाता है

**क्लाइंट की संख्या छिपाना:**

सर्वर यादृच्छिक डमी प्रविष्टियाँ जोड़ सकते हैं:

```python
# Add dummy entries
num_dummies = random.randint(0, max_dummies)
for _ in range(num_dummies):
    dummy_id = CSRNG(8)
    dummy_cookie = CSRNG(32)
    auth_entries.append((dummy_id, dummy_cookie))

# Randomize all entries (real + dummy)
random.shuffle(auth_entries)
```
**लागत:** डमी प्रविष्टियाँ एन्क्रिप्टेड LeaseSet का आकार बढ़ाती हैं (प्रत्येक 40 बाइट).

**AuthCookie (प्रमाणीकरण कुकी) का रोटेशन:**

सर्वरों को एक नया authCookie उत्पन्न करना चाहिए: - जब भी एक एन्क्रिप्टेड LeaseSet प्रकाशित किया जाए (आम तौर पर हर कुछ घंटों में) - किसी क्लाइंट को रद्द करने के तुरंत बाद - नियमित अनुसूची पर (उदा., प्रतिदिन), भले ही किसी क्लाइंट में कोई बदलाव न हो

**लाभ:** - यदि authCookie से समझौता हो जाए, तो उजागर होने को सीमित करता है - रद्द किए गए क्लाइंट्स की पहुँच जल्दी समाप्त हो जाए, यह सुनिश्चित करता है - Layer 2 के लिए forward secrecy (आगे की गोपनीयता) प्रदान करता है

---

## एन्क्रिप्टेड LeaseSets के लिए Base32 एड्रेसिंग

### अवलोकन

पारंपरिक I2P base32 पते में केवल Destination (I2P में सेवा/एंडपॉइंट की क्रिप्टोग्राफिक पहचान) का हैश शामिल होता है (32 बाइट → 52 अक्षर)। यह एन्क्रिप्टेड LeaseSets के लिए अपर्याप्त है क्योंकि:

1. क्लाइंट को ब्लाइंडेड सार्वजनिक कुंजी व्युत्पन्न करने के लिए **अनब्लाइंडेड सार्वजनिक कुंजी** की आवश्यकता होती है
2. क्लाइंट को उचित कुंजी व्युत्पत्ति के लिए **हस्ताक्षर प्रकार** (अनब्लाइंडेड और ब्लाइंडेड) की आवश्यकता होती है
3. सिर्फ हैश से यह जानकारी उपलब्ध नहीं होती

**समाधान:** एक नया base32 (32-आधारित एन्कोडिंग) प्रारूप जिसमें सार्वजनिक कुंजी और हस्ताक्षर प्रकार शामिल हैं।

### पता प्रारूप विनिर्देश

**डिकोड की गई संरचना (35 बाइट्स):**

```
┌─────────────────────────────────────────────────────┐
│ Byte 0   │ Byte 1  │ Byte 2  │ Bytes 3-34          │
│ Flags    │ Unblind │ Blinded │ Public Key          │
│ (XOR)    │ SigType │ SigType │ (32 bytes)          │
│          │ (XOR)   │ (XOR)   │                     │
└─────────────────────────────────────────────────────┘
```
**पहले 3 बाइट्स (Checksum के साथ XOR):**

पहले 3 बाइट्स में ऐसा मेटाडाटा होता है जिसे CRC-32 चेकसम के कुछ हिस्सों के साथ XOR किया गया है:

```python
# Data structure before XOR
flags = 0x00           # 1 byte (reserved for future use)
unblinded_sigtype = 0x07 or 0x0b  # 1 byte (7 or 11)
blinded_sigtype = 0x0b  # 1 byte (always 11)

# Compute CRC-32 checksum of public key
checksum = crc32(pubkey)  # 4-byte CRC-32 of bytes 3-34

# XOR first 3 bytes with parts of checksum
data[0] = flags XOR (checksum >> 24) & 0xFF
data[1] = unblinded_sigtype XOR (checksum >> 16) & 0xFF  
data[2] = blinded_sigtype XOR (checksum >> 8) & 0xFF

# Bytes 3-34 contain the unmodified 32-byte public key
data[3:34] = pubkey
```
**चेकसम के गुण:** - मानक CRC-32 बहुपद का उपयोग करता है - गलत-नकारात्मक दर: ~16 मिलियन में 1 - पते में टाइपिंग गलतियों के लिए त्रुटि पहचान प्रदान करता है - प्रमाणीकरण के लिए उपयोग नहीं किया जा सकता (क्रिप्टोग्राफ़िक रूप से सुरक्षित नहीं)

**कूटबद्ध प्रारूप:**

```
Base32Encode(35 bytes) || ".b32.i2p"
```
**विशेषताएँ:** - कुल अक्षर: 56 (35 बाइट्स × 8 बिट्स ÷ 5 बिट्स प्रति अक्षर) - प्रत्यय: ".b32.i2p" (पारंपरिक base32 के समान) - कुल लंबाई: 56 + 8 = 64 अक्षर (null terminator (स्ट्रिंग के अंत का NULL वर्ण) को छोड़कर)

**Base32 एन्कोडिंग:** - वर्णमाला: `abcdefghijklmnopqrstuvwxyz234567` (मानक RFC 4648) - अंत में 5 अप्रयुक्त बिट 0 होने ही चाहिए - केस-असंवेदनशील (प्रचलनानुसार छोटे अक्षरों में)

### पता निर्माण

```python
import struct
from zlib import crc32
import base64

def generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype):
    """
    Generate base32 address for encrypted LeaseSet.
    
    Args:
        pubkey: 32-byte public key (bytes)
        unblinded_sigtype: Unblinded signature type (7 or 11)
        blinded_sigtype: Blinded signature type (always 11)
    
    Returns:
        String address ending in .b32.i2p
    """
    # Verify inputs
    assert len(pubkey) == 32, "Public key must be 32 bytes"
    assert unblinded_sigtype in [7, 11], "Unblinded sigtype must be 7 or 11"
    assert blinded_sigtype == 11, "Blinded sigtype must be 11"
    
    # Compute CRC-32 of public key
    checksum = crc32(pubkey) & 0xFFFFFFFF  # Ensure 32-bit unsigned
    
    # Prepare metadata bytes
    flags = 0x00
    
    # XOR metadata with checksum parts
    byte0 = flags ^ ((checksum >> 24) & 0xFF)
    byte1 = unblinded_sigtype ^ ((checksum >> 16) & 0xFF)
    byte2 = blinded_sigtype ^ ((checksum >> 8) & 0xFF)
    
    # Construct 35-byte data
    data = bytes([byte0, byte1, byte2]) + pubkey
    
    # Base32 encode (standard alphabet)
    # Python's base64 module uses uppercase by default
    b32 = base64.b32encode(data).decode('ascii').lower().rstrip('=')
    
    # Construct full address
    address = b32 + ".b32.i2p"
    
    return address
```
### पते का विश्लेषण

```python
import struct
from zlib import crc32
import base64

def parse_encrypted_b32_address(address):
    """
    Parse base32 address for encrypted LeaseSet.
    
    Args:
        address: String address ending in .b32.i2p
    
    Returns:
        Tuple of (pubkey, unblinded_sigtype, blinded_sigtype)
    
    Raises:
        ValueError: If address is invalid or checksum fails
    """
    # Remove suffix
    if not address.endswith('.b32.i2p'):
        raise ValueError("Invalid address suffix")
    
    b32 = address[:-8]  # Remove ".b32.i2p"
    
    # Verify length (56 characters for 35 bytes)
    if len(b32) != 56:
        raise ValueError(f"Invalid length: {len(b32)} (expected 56)")
    
    # Base32 decode
    # Add padding if needed
    padding_needed = (8 - (len(b32) % 8)) % 8
    b32_padded = b32.upper() + '=' * padding_needed
    
    try:
        data = base64.b32decode(b32_padded)
    except Exception as e:
        raise ValueError(f"Invalid base32 encoding: {e}")
    
    # Verify decoded length
    if len(data) != 35:
        raise ValueError(f"Invalid decoded length: {len(data)} (expected 35)")
    
    # Extract public key
    pubkey = data[3:35]
    
    # Compute CRC-32 for verification
    checksum = crc32(pubkey) & 0xFFFFFFFF
    
    # Un-XOR metadata bytes
    flags = data[0] ^ ((checksum >> 24) & 0xFF)
    unblinded_sigtype = data[1] ^ ((checksum >> 16) & 0xFF)
    blinded_sigtype = data[2] ^ ((checksum >> 8) & 0xFF)
    
    # Verify expected values
    if flags != 0x00:
        raise ValueError(f"Invalid flags: {flags:#x} (expected 0x00)")
    
    if unblinded_sigtype not in [7, 11]:
        raise ValueError(f"Invalid unblinded sigtype: {unblinded_sigtype} (expected 7 or 11)")
    
    if blinded_sigtype != 11:
        raise ValueError(f"Invalid blinded sigtype: {blinded_sigtype} (expected 11)")
    
    return pubkey, unblinded_sigtype, blinded_sigtype
```
### पारंपरिक Base32 (बेस 32 एन्कोडिंग) से तुलना

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Traditional B32</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Encrypted LS2 B32</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Content</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256 hash of Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Public key + signature types</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Decoded Size</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">35 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Encoded Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">52 characters</td><td style="border:1px solid var(--color-border); padding:0.5rem;">56 characters</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Suffix</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Total Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">60 chars</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 chars</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">None</td><td style="border:1px solid var(--color-border); padding:0.5rem;">CRC-32 (XOR'd into first 3 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Regular destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted LeaseSet destinations</td></tr>
  </tbody>
</table>
### उपयोग संबंधी प्रतिबंध

**BitTorrent असंगतता:**

एन्क्रिप्टेड LS2 (leaseSet का नया संस्करण) पते BitTorrent के compact announce replies (ट्रैकर के उत्तर का संक्षिप्त प्रारूप) के साथ उपयोग नहीं किए जा सकते:

```
Compact announce reply format:
┌────────────────────────────┐
│ 32-byte destination hash   │  ← Only hash, no signature types
│ 2-byte port                │
└────────────────────────────┘
```
**समस्या:** संक्षिप्त फ़ॉर्मैट में केवल हैश (32 bytes) शामिल होता है, जिसमें हस्ताक्षर प्रकारों या सार्वजनिक कुंजी की जानकारी के लिए कोई स्थान नहीं है।

**समाधान:** पूर्ण announce replies (ट्रैकर के 'announce' अनुरोध के उत्तर) का उपयोग करें या ऐसे HTTP-आधारित ट्रैकर उपयोग करें जो पूर्ण पतों का समर्थन करते हों।

### एड्रेस बुक एकीकरण

यदि किसी क्लाइंट की पता पुस्तिका में पूर्ण Destination (गंतव्य पहचान) हो:

1. पूर्ण Destination (I2P की गंतव्य पहचान) संग्रहीत करें (इसमें सार्वजनिक कुंजी शामिल है)
2. हैश के आधार पर रिवर्स लुकअप का समर्थन करें
3. जब एन्क्रिप्टेड LS2 मिले, तो पता पुस्तिका से सार्वजनिक कुंजी प्राप्त करें
4. यदि पूर्ण Destination पहले से ज्ञात है तो नए base32 प्रारूप की आवश्यकता नहीं

**एड्रेस बुक के वे प्रारूप जो एन्क्रिप्टेड LS2 (LeaseSet का संस्करण 2) का समर्थन करते हैं:** - hosts.txt जिसमें पूर्ण destination strings हों - SQLite डेटाबेस जिनमें destination कॉलम हो - JSON/XML प्रारूप जिनमें पूर्ण destination डेटा हो

### कार्यान्वयन के उदाहरण

**उदाहरण 1: पता उत्पन्न करें**

```python
# Ed25519 destination example
pubkey = bytes.fromhex('a' * 64)  # 32-byte public key
unblinded_type = 7   # Ed25519
blinded_type = 11    # Red25519 (always)

address = generate_encrypted_b32_address(pubkey, unblinded_type, blinded_type)
print(f"Address: {address}")
# Output: 56 base32 characters + .b32.i2p
```
**उदाहरण 2: पार्स करें और सत्यापित करें**

```python
address = "abc...xyz.b32.i2p"  # 56 chars + suffix

try:
    pubkey, unblinded, blinded = parse_encrypted_b32_address(address)
    print(f"Public Key: {pubkey.hex()}")
    print(f"Unblinded SigType: {unblinded}")
    print(f"Blinded SigType: {blinded}")
except ValueError as e:
    print(f"Invalid address: {e}")
```
**उदाहरण 3: Destination से रूपांतरण**

```python
def destination_to_encrypted_b32(destination):
    """
    Convert full Destination to encrypted LS2 base32 address.
    
    Args:
        destination: I2P Destination object
    
    Returns:
        Base32 address string
    """
    # Extract public key and signature type from destination
    pubkey = destination.signing_public_key  # 32 bytes
    sigtype = destination.sig_type  # 7 or 11
    
    # Blinded type is always 11 (Red25519)
    blinded_type = 11
    
    # Generate address
    return generate_encrypted_b32_address(pubkey, sigtype, blinded_type)
```
### सुरक्षा संबंधी विचार

**गोपनीयता:** - Base32 पता सार्वजनिक कुंजी को प्रकट करता है - यह जानबूझकर किया गया है और प्रोटोकॉल के लिए आवश्यक है - न तो निजी कुंजी का खुलासा करता है और न ही सुरक्षा से समझौता करता है - सार्वजनिक कुंजियाँ डिज़ाइन के अनुसार सार्वजनिक जानकारी होती हैं

**टकराव प्रतिरोध:** - CRC-32 केवल 32 बिट का टकराव प्रतिरोध प्रदान करता है - क्रिप्टोग्राफ़िक रूप से सुरक्षित नहीं है (केवल त्रुटि पहचान के लिए उपयोग करें) - प्रमाणीकरण के लिए चेकसम पर निर्भर न रहें - पूर्ण गंतव्य सत्यापन अभी भी आवश्यक है

**पता सत्यापन:** - उपयोग से पहले हमेशा checksum (चेकसम) का सत्यापन करें - अमान्य signature types (हस्ताक्षर प्रकार) वाले पतों को अस्वीकार करें - यह सत्यापित करें कि public key (सार्वजनिक कुंजी) on the curve (elliptic curve पर वैध बिंदु) है (कार्यान्वयन-विशिष्ट)

**संदर्भ:** - [प्रस्ताव 149: एन्क्रिप्टेड LS2 के लिए B32](/proposals/149-b32-encrypted-ls2/) - [B32 एड्रेसिंग विनिर्देश](/docs/specs/b32-for-encrypted-leasesets/) - [I2P नामकरण विनिर्देश](/docs/overview/naming/)

---

## ऑफ़लाइन कुंजियों का समर्थन

### अवलोकन

ऑफ़लाइन कुंजियाँ मुख्य हस्ताक्षर कुंजी को ऑफ़लाइन (कोल्ड स्टोरेज) रखने की अनुमति देती हैं, जबकि दैनिक संचालन के लिए एक अस्थायी हस्ताक्षर कुंजी का उपयोग किया जाता है। यह उच्च-सुरक्षा सेवाओं के लिए अत्यंत महत्वपूर्ण है।

**एन्क्रिप्टेड LS2 की विशिष्ट आवश्यकताएँ:** - अस्थायी कुंजियाँ ऑफलाइन उत्पन्न की जानी चाहिएँ - Blinded private keys (ब्लाइंडिंग: निजी कुंजी को ऐसा रूप देना कि उसे मूल से जोड़ा न जा सके) पूर्व-उत्पन्न होनी चाहिएँ (प्रति दिन एक) - अस्थायी और Blinded कुंजियाँ दोनों बैचों में प्रदान की जानी चाहिएँ - मानकीकृत फ़ाइल प्रारूप अभी परिभाषित नहीं किया गया है (विशिष्टता में TODO)

### ऑफ़लाइन कुंजी संरचना

**लेयर 0 अस्थायी कुंजी डेटा (जब फ्लैग बिट 0 = 1 हो):**

```
┌───────────────────────────────────────────────────┐
│ Expires Timestamp       │ 4 bytes (seconds)       │
│ Transient Sig Type      │ 2 bytes (big endian)    │
│ Transient Signing Pubkey│ Variable (sigtype len)  │
│ Signature (by blinded)  │ 64 bytes (Red25519)     │
└───────────────────────────────────────────────────┘
```
**हस्ताक्षर कवरेज:** ऑफ़लाइन कुंजी ब्लॉक में मौजूद हस्ताक्षर निम्नलिखित को आवृत करता है: - समाप्ति टाइमस्टैम्प (4 बाइट्स) - अस्थायी हस्ताक्षर प्रकार (2 बाइट्स)   - अस्थायी हस्ताक्षर हेतु सार्वजनिक कुंजी (परिवर्ती)

इस हस्ताक्षर का सत्यापन **blinded public key** (blinded यानी मास्क/छिपाई गई public key) का उपयोग करके किया जाता है, जिससे सिद्ध होता है कि blinded private key (blinded यानी मास्क/छिपाई गई private key) रखने वाली इकाई ने इस अस्थायी कुंजी को अधिकृत किया है।

### कुंजी उत्पन्न करने की प्रक्रिया

**Offline Keys के साथ कूटबद्ध LeaseSet के लिए:**

1. **अस्थायी कुंजी-युग्म उत्पन्न करें** (ऑफ़लाइन, कोल्ड स्टोरेज में):
   ```python
   # For each day in future
   for date in future_dates:
       # Generate daily transient keypair
       transient_privkey = generate_red25519_privkey()  # Type 11
       transient_pubkey = derive_public(transient_privkey)

       # Store for later delivery
       keys[date] = (transient_privkey, transient_pubkey)
   ```

2. **Generate daily blinded keypairs** (offline, in cold storage):
   ```python
# प्रत्येक दिन के लिए    for date in future_dates:

       # Derive alpha for this date
       datestring = date.strftime("%Y%m%d")  # "YYYYMMDD"
       alpha = GENERATE_ALPHA(destination, datestring, secret)
       
       # Blind the signing private key
       a = destination_signing_privkey  # Type 7 or 11
       blinded_privkey = BLIND_PRIVKEY(a, alpha)  # Result is type 11
       blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
       
       # Store for later delivery
       blinded_keys[date] = (blinded_privkey, blinded_pubkey)
   ```

3. **Sign transient keys with blinded keys** (offline):
   ```python
for date in future_dates:

       transient_pubkey = keys[date][1]
       blinded_privkey = blinded_keys[date][0]
       
       # Create signature data
       expires = int((date + timedelta(days=1)).timestamp())
       sig_data = struct.pack('>I', expires)  # 4 bytes
       sig_data += struct.pack('>H', 11)     # Transient type (Red25519)
       sig_data += transient_pubkey          # 32 bytes
       
       # Sign with blinded private key
       signature = RED25519_SIGN(blinded_privkey, sig_data)
       
       # Package for delivery
       offline_sig_blocks[date] = {
           'expires': expires,
           'transient_type': 11,
           'transient_pubkey': transient_pubkey,
           'signature': signature
       }
   ```

4. **Package for delivery to router:**
   ```python
# प्रत्येक तिथि के लिए    delivery_package[date] = {

       'transient_privkey': keys[date][0],
       'transient_pubkey': keys[date][1],
       'blinded_privkey': blinded_keys[date][0],
       'blinded_pubkey': blinded_keys[date][1],
       'offline_sig_block': offline_sig_blocks[date]
}

   ```

### Router Usage

**Daily Key Loading:**

```python
# UTC के अनुसार मध्यरात्रि पर (या प्रकाशन से पहले)

date = datetime.utcnow().date()

# आज के लिए कुंजियाँ लोड करें

today_keys = load_delivery_package(date)

transient_privkey = today_keys['transient_privkey'] transient_pubkey = today_keys['transient_pubkey'] blinded_privkey = today_keys['blinded_privkey'] blinded_pubkey = today_keys['blinded_pubkey'] offline_sig_block = today_keys['offline_sig_block']

# आज के एन्क्रिप्टेड LeaseSet के लिए इन कुंजियों का उपयोग करें

```

**Publishing Process:**

```python
# 1. आंतरिक LeaseSet2 बनाएँ

inner_ls2 = create_leaseset2(

    destinations, leases, expires, 
    signing_key=transient_privkey  # Use transient key
)

# 2. लेयर 2 को एन्क्रिप्ट करें

layer2_ciphertext = encrypt_layer2(inner_ls2, authCookie, subcredential, timestamp)

# 3. प्राधिकरण डेटा के साथ लेयर 1 बनाएँ

layer1_plaintext = create_layer1(authorization_data, layer2_ciphertext)

# 4. लेयर 1 को एन्क्रिप्ट करें

layer1_ciphertext = encrypt_layer1(layer1_plaintext, subcredential, timestamp)

# 5. ऑफ़लाइन हस्ताक्षर ब्लॉक के साथ Layer 0 (परत 0) बनाएँ

layer0 = create_layer0(

    blinded_pubkey,
    timestamp,
    expires,
    flags=0x0001,  # Bit 0 set (offline keys present)
    offline_sig_block=offline_sig_block,
    layer1_ciphertext=layer1_ciphertext
)

# 6. लेयर 0 पर अस्थायी निजी कुंजी से हस्ताक्षर करें

signature = RED25519_SIGN(transient_privkey, layer0)

# 7. हस्ताक्षर संलग्न करें और प्रकाशित करें

encrypted_leaseset = layer0 + signature publish_to_netdb(encrypted_leaseset)

```

### Security Considerations

**Tracking via Offline Signature Block:**

The offline signature block is in plaintext (Layer 0). An adversary scraping floodfills could:
- Track the same encrypted LeaseSet across multiple days
- Correlate encrypted LeaseSets even though blinded keys change daily

**Mitigation:** Generate new transient keys daily (in addition to blinded keys):

```python
# हर दिन नई अस्थायी और नई blinded keys (ब्लाइंडेड कुंजियाँ) दोनों उत्पन्न करें

for date in future_dates:

    # New transient keypair for this day
    transient_privkey = generate_red25519_privkey()
    transient_pubkey = derive_public(transient_privkey)
    
    # New blinded keypair for this day
    alpha = GENERATE_ALPHA(destination, datestring, secret)
    blinded_privkey = BLIND_PRIVKEY(signing_privkey, alpha)
    blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
    
    # Sign new transient key with new blinded key
    sig = RED25519_SIGN(blinded_privkey, transient_pubkey || metadata)
    
    # Now offline sig block changes daily
```

**Benefits:**
- Prevents tracking across days via offline signature block
- Provides same security as encrypted LS2 without offline keys
- Each day appears completely independent

**Cost:**
- More keys to generate and store
- More complex key management

### File Format (TODO)

**Current Status:** No standardized file format defined for batch key delivery.

**Requirements for Future Format:**

1. **Must support multiple dates:**
   - Batch delivery of 30+ days worth of keys
   - Clear date association for each key set

2. **Must include all necessary data:**
   - Transient private key
   - Transient public key
   - Blinded private key
   - Blinded public key
   - Pre-computed offline signature block
   - Expiration timestamps

3. **Should be tamper-evident:**
   - Checksums or signatures over entire file
   - Integrity verification before loading

4. **Should be encrypted:**
   - Keys are sensitive material
   - Encrypt file with router's key or passphrase

**Proposed Format Example (JSON, encrypted):**

```json
{   "version": 1,   "destination_hash": "base64...",   "keys": [

    {
      "date": "2025-10-15",
      "transient": {
        "type": 11,
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "blinded": {
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "offline_sig_block": {
        "expires": 1729123200,
        "signature": "base64..."
      }
    }
],   "signature": "base64..."  // Signature over entire structure }

```

### I2CP Protocol Enhancement (TODO)

**Current Status:** No I2CP protocol enhancement defined for offline keys with encrypted LeaseSet.

**Requirements:**

1. **Key delivery mechanism:**
   - Upload batch of keys from client to router
   - Acknowledgment of successful key loading

2. **Key expiration notification:**
   - Router notifies client when keys running low
   - Client can generate and upload new batch

3. **Key revocation:**
   - Emergency revocation of future keys if compromise suspected

**Proposed I2CP Messages:**

```
UPLOAD_OFFLINE_KEYS   - एन्क्रिप्टेड कुंजी सामग्री का बैच   - कवर की गई तिथि सीमा

OFFLINE_KEY_STATUS   - शेष दिनों की संख्या   - अगली कुंजी की समाप्ति तिथि

REVOKE_OFFLINE_KEYS     - रद्द करने हेतु तिथि सीमा   - प्रतिस्थापन के लिए नई कुंजियाँ (वैकल्पिक)

```

### Implementation Status

**Java I2P:**
- ✅ Offline keys for standard LS2: Fully supported (since 0.9.38)
- ⚠️ Offline keys for encrypted LS2: Implemented (since 0.9.40)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**i2pd (C++):**
- ✅ Offline keys for standard LS2: Fully supported
- ✅ Offline keys for encrypted LS2: Fully supported (since 2.58.0)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**References:**
- [Offline Signatures Proposal](/proposals/123-new-netdb-entries/)
- [I2CP Specification](/docs/specs/i2cp/)

---

## Security Considerations

### Cryptographic Security

**Algorithm Selection:**

All cryptographic primitives are based on well-studied algorithms:
- **ChaCha20:** Modern stream cipher, constant-time, no timing attacks
- **SHA-256:** NIST-approved hash, 128-bit security level
- **HKDF:** RFC 5869 standard, proven security bounds
- **Ed25519/Red25519:** Curve25519-based, ~128-bit security level
- **X25519:** Diffie-Hellman over Curve25519, ~128-bit security level

**Key Sizes:**
- All symmetric keys: 256 bits (32 bytes)
- All public/private keys: 256 bits (32 bytes)
- All nonces/IVs: 96 bits (12 bytes)
- All signatures: 512 bits (64 bytes)

These sizes provide adequate security margins against current and near-future attacks.

### Forward Secrecy

**Daily Key Rotation:**

Encrypted LeaseSets rotate keys daily (UTC midnight):
- New blinded public/private key pair
- New storage location in DHT
- New encryption keys for both layers

**Benefits:**
- Compromising today's blinded key doesn't reveal yesterday's
- Limits exposure window to 24 hours
- Prevents long-term tracking via DHT

**Enhanced with Ephemeral Keys:**

DH client authorization uses ephemeral keys:
- Server generates new ephemeral DH keypair for each publication
- Compromising ephemeral key only affects that publication
- True forward secrecy even if long-term keys compromised

### Privacy Properties

**Destination Blinding:**

The blinded public key:
- Is unlinkable to the original destination (without knowing the secret)
- Changes daily, preventing long-term correlation
- Cannot be reversed to find the original public key

**Client Membership Privacy:**

Per-client authorization provides:
- **Anonymity:** No way to identify which clients are authorized
- **Untraceability:** Cannot track when specific clients added/revoked
- **Size obfuscation:** Can add dummy entries to hide true count

**DHT Privacy:**

Storage location rotates daily:
```
location = SHA-256(sig_type || blinded_public_key)

```

This prevents:
- Correlation across days via DHT lookups
- Long-term monitoring of service availability
- Traffic analysis of DHT queries

### Threat Model

**Adversary Capabilities:**

1. **Network Adversary:**
   - Can monitor all DHT traffic
   - Can observe encrypted LeaseSet publications
   - Cannot decrypt without proper keys

2. **Floodfill Adversary:**
   - Can store and analyze all encrypted LeaseSets
   - Can track publication patterns over time
   - Cannot decrypt Layer 1 or Layer 2
   - Can see client count (but not identities)

3. **Authorized Client Adversary:**
   - Can decrypt specific encrypted LeaseSets
   - Can access inner LeaseSet2 data
   - Cannot determine other clients' identities
   - Cannot decrypt past LeaseSets (with ephemeral keys)

**Out of Scope:**

- Malicious router implementations
- Compromised router host systems
- Side-channel attacks (timing, power analysis)
- Physical access to keys
- Social engineering attacks

### Attack Scenarios

**1. Offline Keys Tracking Attack:**

**Attack:** Adversary tracks encrypted LeaseSets via unchanging offline signature block.

**Mitigation:** Generate new transient keys daily (in addition to blinded keys).

**Status:** Documented recommendation, implementation-specific.

**2. Client Position Inference Attack:**

**Attack:** If client order is static, clients can infer their position and detect when other clients added/removed.

**Mitigation:** Randomize client order in authorization list for each publication.

**Status:** Documented recommendation in specification.

**3. Client Count Analysis Attack:**

**Attack:** Adversary monitors client count changes over time to infer service popularity or client churn.

**Mitigation:** Add random dummy entries to authorization list.

**Status:** Optional feature, deployment-specific trade-off (size vs. privacy).

**4. PSK Interception Attack:**

**Attack:** Adversary intercepts PSK during out-of-band exchange and can decrypt all future encrypted LeaseSets.

**Mitigation:** Use DH client authorization instead, or ensure secure key exchange (Signal, OTR, PGP).

**Status:** Known limitation of PSK approach, documented in specification.

**5. Timing Correlation Attack:**

**Attack:** Adversary correlates publication times across days to link encrypted LeaseSets.

**Mitigation:** Randomize publication times, use delayed publishing.

**Status:** Implementation-specific, not addressed in core specification.

**6. Long-term Secret Compromise:**

**Attack:** Adversary compromises the blinding secret and can compute all past and future blinded keys.

**Mitigation:** 
- Use optional secret parameter (not empty)
- Rotate secret periodically
- Use different secrets for different services

**Status:** Secret parameter is optional; using it is highly recommended.

### Operational Security

**Key Management:**

1. **Signing Private Key:**
   - Store offline in cold storage
   - Use only for generating blinded keys (batch process)
   - Never expose to online router

2. **Blinded Private Keys:**
   - Generate offline, deliver in batches
   - Rotate daily automatically
   - Delete after use (forward secrecy)

3. **Transient Private Keys (with offline keys):**
   - Generate offline, deliver in batches
   - Can be longer-lived (days/weeks)
   - Rotate regularly for enhanced privacy

4. **Client Authorization Keys:**
   - DH: Client private keys never leave client device
   - PSK: Use unique keys per client, secure exchange
   - Revoke immediately upon client removal

**Secret Management:**

The optional secret parameter in `GENERATE_ALPHA`:
- SHOULD be used for high-security services
- MUST be transmitted securely to authorized clients
- SHOULD be rotated periodically (e.g., monthly)
- CAN be different for different client groups

**Monitoring and Auditing:**

1. **Publication Monitoring:**
   - Verify encrypted LeaseSets published successfully
   - Monitor floodfill acceptance rates
   - Alert on publication failures

2. **Client Access Monitoring:**
   - Log client authorization attempts (without identifying clients)
   - Monitor for unusual patterns
   - Detect potential attacks early

3. **Key Rotation Auditing:**
   - Verify daily key rotation occurs
   - Check blinded key changes daily
   - Ensure old keys are deleted

### Implementation Security

**Constant-Time Operations:**

Implementations MUST use constant-time operations for:
- All scalar arithmetic (mod L operations)
- Private key comparisons
- Signature verification
- DH key agreement

**Memory Security:**

- Zero sensitive key material after use
- Use secure memory allocation for keys
- Prevent keys from being paged to disk
- Clear stack variables containing key material

**Random Number Generation:**

- Use cryptographically secure RNG (CSRNG)
- Properly seed RNG from OS entropy source
- Do not use predictable RNGs for key material
- Verify RNG output quality periodically

**Input Validation:**

- Validate all public keys are on the curve
- Check all signature types are supported
- Verify all lengths before parsing
- Reject malformed encrypted LeaseSets early

**Error Handling:**

- Do not leak information via error messages
- Use constant-time comparison for authentication
- Do not expose timing differences in decryption
- Log security-relevant events properly

### Recommendations

**For Service Operators:**

1. ✅ **Use Red25519 (type 11)** for new destinations
2. ✅ **Use DH client authorization** for high-security services
3. ✅ **Generate new transient keys daily** when using offline keys
4. ✅ **Use the optional secret parameter** in GENERATE_ALPHA
5. ✅ **Randomize client order** in authorization lists
6. ✅ **Monitor publication success** and investigate failures
7. ⚠️ **Consider dummy entries** to hide client count (size trade-off)

**For Client Implementers:**

1. ✅ **Validate blinded public keys** are on prime-order subgroup
2. ✅ **Verify all signatures** before trusting data
3. ✅ **Use constant-time operations** for cryptographic primitives
4. ✅ **Zero key material** immediately after use
5. ✅ **Implement proper error handling** without information leaks
6. ✅ **Support both Ed25519 and Red25519** destination types

**For Network Operators:**

1. ✅ **Accept encrypted LeaseSets** in floodfill routers
2. ✅ **Enforce reasonable size limits** to prevent abuse
3. ✅ **Monitor for anomalous patterns** (extremely large, frequent updates)
4. ⚠️ **Consider rate limiting** encrypted LeaseSet publications

---

## Implementation Notes

### Java I2P Implementation

**Repository:** https://github.com/i2p/i2p.i2p

**Key Classes:**
- `net.i2p.data.LeaseSet2` - LeaseSet2 structure
- `net.i2p.data.EncryptedLeaseSet` - Encrypted LS2 implementation
- `net.i2p.crypto.eddsa.EdDSAEngine` - Ed25519/Red25519 signatures
- `net.i2p.crypto.HKDF` - HKDF implementation
- `net.i2p.crypto.ChaCha20` - ChaCha20 cipher

**Configuration:**

Enable encrypted LeaseSet in `clients.config`:
```properties
# एन्क्रिप्टेड LeaseSet सक्षम करें

i2cp.encryptLeaseSet=true

# वैकल्पिक: क्लाइंट प्राधिकरण सक्षम करें

i2cp.enableAccessList=true

# वैकल्पिक: DH authorization (Diffie-Hellman आधारित प्राधिकरण) का उपयोग करें (डिफ़ॉल्ट PSK (pre-shared key/पूर्व-साझा कुंजी) है)

i2cp.accessListType=0

# वैकल्पिक: Blinding secret (ब्लाइंडिंग हेतु गुप्त कुंजी) (अत्यधिक अनुशंसित)

i2cp.blindingSecret=अपना-सीक्रेट-यहाँ

```

**API Usage Example:**

```java
// एन्क्रिप्टेड LeaseSet बनाएँ EncryptedLeaseSet els = new EncryptedLeaseSet();

// गंतव्य सेट करें
els.setDestination(destination);

// प्रत्येक क्लाइंट के लिए प्राधिकरण सक्षम करें els.setAuthorizationEnabled(true); els.setAuthType(EncryptedLeaseSet.AUTH_DH);

// अधिकृत क्लाइंट जोड़ें (DH सार्वजनिक कुंजियाँ) for (byte[] clientPubKey : authorizedClients) {

    els.addClient(clientPubKey);
}

// ब्लाइंडिंग पैरामीटर सेट करें els.setBlindingSecret("your-secret");

// हस्ताक्षर करें और प्रकाशित करें els.sign(signingPrivateKey); netDb.publish(els);

```

### i2pd (C++) Implementation

**Repository:** https://github.com/PurpleI2P/i2pd

**Key Files:**
- `libi2pd/LeaseSet.h/cpp` - LeaseSet implementations
- `libi2pd/Crypto.h/cpp` - Cryptographic primitives
- `libi2pd/Ed25519.h/cpp` - Ed25519/Red25519 signatures
- `libi2pd/ChaCha20.h/cpp` - ChaCha20 cipher

**Configuration:**

Enable in tunnel configuration (`tunnels.conf`):
```ini
[my-hidden-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# एन्क्रिप्टेड LeaseSet सक्षम करें

encryptleaseset = true

# वैकल्पिक: क्लाइंट प्राधिकरण प्रकार (0=DH (डिफी-हेल्मन), 1=PSK (पूर्व-साझा कुंजी))

authtype = 0

# वैकल्पिक: Blinding secret (ब्लाइंडिंग हेतु गोपनीय मान)

secret = अपना-सीक्रेट-यहाँ

# वैकल्पिक: अधिकृत क्लाइंट्स (प्रत्येक पंक्ति में एक, base64 में एन्कोड की गई सार्वजनिक कुंजियाँ)

client.1 = base64-encoded-client-pubkey-1 client.2 = base64-encoded-client-pubkey-2

```

**API Usage Example:**

```cpp
// एन्क्रिप्टेड LeaseSet बनाएँ auto encryptedLS = std::make_shared<i2p::data::EncryptedLeaseSet>(

    destination,
    blindingSecret
);

// प्रति-क्लाइंट प्राधिकरण सक्षम करें encryptedLS->SetAuthType(i2p::data::AUTH_TYPE_DH);

// अधिकृत क्लाइंट जोड़ें for (const auto& clientPubKey : authorizedClients) {

    encryptedLS->AddClient(clientPubKey);
}

// हस्ताक्षर करें और प्रकाशित करें encryptedLS->Sign(signingPrivKey); netdb.Publish(encryptedLS);

```

### Testing and Debugging

**Test Vectors:**

Generate test vectors for implementation verification:

```python
# टेस्ट वेक्टर 1: Key blinding (कुंजी को गोपनीय बनाने की तकनीक)

destination_pubkey = bytes.fromhex('a' * 64) sigtype = 7 blinded_sigtype = 11 date = "20251015" secret = ""

alpha = generate_alpha(destination_pubkey, sigtype, blinded_sigtype, date, secret) print(f"Alpha: {alpha.hex()}")

# अपेक्षित: (संदर्भ कार्यान्वयन से मिलान कर सत्यापित करें)

```

**Unit Tests:**

Key areas to test:
1. HKDF derivation with various inputs
2. ChaCha20 encryption/decryption
3. Red25519 signature generation and verification
4. Key blinding (private and public)
5. Layer 1/2 encryption/decryption
6. Client authorization (DH and PSK)
7. Base32 address generation and parsing

**Integration Tests:**

1. Publish encrypted LeaseSet to test network
2. Retrieve and decrypt from client
3. Verify daily key rotation
4. Test client authorization (add/remove clients)
5. Test offline keys (if supported)

**Common Implementation Errors:**

1. **Incorrect mod L reduction:** Must use proper modular arithmetic
2. **Endianness errors:** Most fields are big-endian, but some crypto uses little-endian
3. **Off-by-one in array slicing:** Verify indices are inclusive/exclusive as needed
4. **Missing constant-time comparisons:** Use constant-time for all sensitive comparisons
5. **Not zeroing key material:** Always zero keys after use

### Performance Considerations

**Computational Costs:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Cost</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per publication</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 point add + 1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 X25519 ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N = number of clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 X25519 op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 DH ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Only HKDF + ChaCha20</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature (Red25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 signature op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Similar cost to Ed25519</td></tr>
  </tbody>
</table>

**Size Overhead:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded public key</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH ephemeral pubkey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if DH auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK salt</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if PSK auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline sig block</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈100 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if offline keys)</td></tr>
  </tbody>
</table>

**Typical Sizes:**

- **No client auth:** ~200 bytes overhead
- **With 10 DH clients:** ~600 bytes overhead
- **With 100 DH clients:** ~4200 bytes overhead

**Optimization Tips:**

1. **Batch key generation:** Generate blinded keys for multiple days in advance
2. **Cache subcredentials:** Compute once per day, reuse for all publications
3. **Reuse ephemeral keys:** Can reuse ephemeral DH key for short period (minutes)
4. **Parallel client encryption:** Encrypt client cookies in parallel
5. **Fast path for no auth:** Skip authorization layer entirely when disabled

### Compatibility

**Backward Compatibility:**

- Ed25519 (type 7) destinations supported for unblinded keys
- Red25519 (type 11) required for blinded keys
- Traditional LeaseSets still fully supported
- Encrypted LeaseSets do not break existing network

**Forward Compatibility:**

- Reserved flag bits for future features
- Extensible authorization scheme (3 bits allow 8 types)
- Version field in various structures

**Interoperability:**

- Java I2P and i2pd fully interoperable since:
  - Java I2P 0.9.40 (May 2019)
  - i2pd 2.58.0 (September 2025)
- Encrypted LeaseSets work across implementations
- Client authorization works across implementations

---

## References

### IETF RFCs

- **[RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104)** - HMAC: Keyed-Hashing for Message Authentication (February 1997)
- **[RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869)** - HMAC-based Extract-and-Expand Key Derivation Function (HKDF) (May 2010)
- **[RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539)** - ChaCha20 and Poly1305 for IETF Protocols (May 2015)
- **[RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748)** - Elliptic Curves for Security (January 2016)

### I2P Specifications

- **[Common Structures Specification](/docs/specs/common-structures/)** - LeaseSet2 and EncryptedLeaseSet structures
- **[Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/)** - Background and design of LeaseSet2
- **[Proposal 146: Red25519](/proposals/146-red25519/)** - Red25519 signature scheme specification
- **[Proposal 149: B32 for Encrypted LS2](/proposals/149-b32-encrypted-ls2/)** - Base32 addressing for encrypted LeaseSets
- **[Red25519 Specification](/docs/specs/red25519-signature-scheme/)** - Detailed Red25519 implementation
- **[B32 Addressing Specification](/docs/specs/b32-for-encrypted-leasesets/)** - Base32 address format
- **[Network Database Documentation](/docs/specs/common-structures/)** - NetDB usage and operations
- **[I2CP Specification](/docs/specs/i2cp/)** - I2P Client Protocol

### Cryptographic References

- **[Ed25519 Paper](http://cr.yp.to/papers.html#ed25519)** - "High-speed high-security signatures" by Bernstein et al.
- **[ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf)** - Section 5.4.6: RedDSA signature scheme
- **[Tor Rendezvous Specification v3](https://spec.torproject.org/rend-spec)** - Tor's onion service specification (for comparison)

### Security References

- **[Key Blinding Security Discussion](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)** - Tor Project mailing list discussion
- **[Tor Ticket #8106](https://trac.torproject.org/projects/tor/ticket/8106)** - Key blinding implementation discussion
- **[PRNG Security](http://projectbullrun.org/dual-ec/ext-rand.html)** - Random number generator security considerations
- **[Tor PRNG Discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)** - Discussion of PRNG usage in Tor

### Implementation References

- **[Java I2P Repository](https://github.com/i2p/i2p.i2p)** - Official Java implementation
- **[i2pd Repository](https://github.com/PurpleI2P/i2pd)** - C++ implementation
- **[I2P Website](/)** - Official I2P project website
- **[I2P Specifications](/docs/specs/)** - Complete specification index

### Version History

- **[I2P Release Notes](/en/blog)** - Official release announcements
- **[Java I2P Releases](https://github.com/i2p/i2p.i2p/releases)** - GitHub release history
- **[i2pd Releases](https://github.com/PurpleI2P/i2pd/releases)** - GitHub release history

---

## Appendix A: Cryptographic Constants

### Ed25519 / Red25519 Constants

```python
# Ed25519 आधार बिंदु (जनित्र)

B = 2**255 - 19

# Ed25519 का क्रम (स्केलर क्षेत्र का आकार)

L = 2**252 + 27742317777372353535851937790883648493

# हस्ताक्षर प्रकार के मान

SIGTYPE_ED25519 = 7    # 0x0007 SIGTYPE_RED25519 = 11  # 0x000b

# कुंजी आकार

PRIVKEY_SIZE = 32  # bytes PUBKEY_SIZE = 32   # bytes SIGNATURE_SIZE = 64  # bytes

```

### ChaCha20 Constants

```python
# ChaCha20 (एक स्ट्रीम सिफर एल्गोरिदम) पैरामीटर

CHACHA20_KEY_SIZE = 32   # बाइट्स (256 बिट्स) CHACHA20_NONCE_SIZE = 12  # बाइट्स (96 बिट्स) CHACHA20_INITIAL_COUNTER = 1  # RFC 7539 0 या 1 की अनुमति देता है

```

### HKDF Constants

```python
# HKDF (HMAC-आधारित कुंजी व्युत्पत्ति फ़ंक्शन) के पैरामीटर

HKDF_HASH = "SHA-256" HKDF_SALT_MAX = 32  # बाइट (HashLen)

# HKDF (HMAC-आधारित कुंजी व्युत्पत्ति फ़ंक्शन) सूचना स्ट्रिंग्स (डोमेन पृथक्करण)

HKDF_INFO_ALPHA = b"i2pblinding1" HKDF_INFO_LAYER1 = b"ELS2_L1K" HKDF_INFO_LAYER2 = b"ELS2_L2K" HKDF_INFO_DH_AUTH = b"ELS2_XCA" HKDF_INFO_PSK_AUTH = b"ELS2PSKA"

```

### Hash Personalization Strings

```python
# SHA-256 personalization strings (व्यक्तिकरण स्ट्रिंग्स)

HASH_PERS_ALPHA = b"I2PGenerateAlpha" HASH_PERS_RED25519 = b"I2P_Red25519H(x)" HASH_PERS_CREDENTIAL = b"credential" HASH_PERS_SUBCREDENTIAL = b"subcredential"

```

### Structure Sizes

```python
# लेयर 0 (बाहरी) के आकार

BLINDED_SIGTYPE_SIZE = 2   # बाइट्स BLINDED_PUBKEY_SIZE = 32   # बाइट्स (Red25519 के लिए) PUBLISHED_TS_SIZE = 4      # बाइट्स EXPIRES_SIZE = 2           # बाइट्स FLAGS_SIZE = 2             # बाइट्स LEN_OUTER_CIPHER_SIZE = 2  # बाइट्स SIGNATURE_SIZE = 64        # बाइट्स (Red25519)

# ऑफलाइन कुंजी ब्लॉक आकार

OFFLINE_EXPIRES_SIZE = 4   # बाइट्स OFFLINE_SIGTYPE_SIZE = 2   # बाइट्स OFFLINE_SIGNATURE_SIZE = 64  # बाइट्स

# परत 1 (मध्य) के आकार

AUTH_FLAGS_SIZE = 1        # बाइट EPHEMERAL_PUBKEY_SIZE = 32  # बाइट्स (DH auth) AUTH_SALT_SIZE = 32        # बाइट्स (PSK auth) NUM_CLIENTS_SIZE = 2       # बाइट्स CLIENT_ID_SIZE = 8         # बाइट्स CLIENT_COOKIE_SIZE = 32    # बाइट्स AUTH_CLIENT_ENTRY_SIZE = 40  # बाइट्स (CLIENT_ID + CLIENT_COOKIE)

# एन्क्रिप्शन का अतिरिक्त भार

SALT_SIZE = 32  # बाइट (प्रत्येक एन्क्रिप्टेड लेयर की शुरुआत में जोड़ा जाता है)

# Base32 पता

B32_ENCRYPTED_DECODED_SIZE = 35  # बाइट्स B32_ENCRYPTED_ENCODED_LEN = 56   # अक्षर B32_SUFFIX = ".b32.i2p"

```

---

## Appendix B: Test Vectors

### Test Vector 1: Alpha Generation

**Input:**
```python
# गंतव्य सार्वजनिक कुंजी (Ed25519)

A = bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') stA = 0x0007  # Ed25519 stA_prime = 0x000b  # Red25519 date = "20251015" secret = ""  # खाली गोपनीय मान

```

**Computation:**
```python
keydata = A || bytes([0x00, 0x07]) || bytes([0x00, 0x0b])

# keydata = 36 बाइट्स

salt = SHA256(b"I2PGenerateAlpha" + keydata) ikm = b"20251015" info = b"i2pblinding1"

seed = HKDF(salt, ikm, info, 64) alpha = LEOS2IP(seed) mod L

```

**Expected Output:**
```
(संदर्भ कार्यान्वयन के साथ मिलान कर सत्यापित करें) alpha = [64-बाइट हेक्साडेसिमल मान]

```

### Test Vector 2: ChaCha20 Encryption

**Input:**
```python
key = bytes([i for i in range(32)])  # 0x00..0x1f nonce = bytes([i for i in range(12)])  # 0x00..0x0b plaintext = b"Hello, I2P!"

```

**Computation:**
```python
ciphertext = ChaCha20_Encrypt(key, nonce, plaintext, counter=1)

```

**Expected Output:**
```
ciphertext = [RFC 7539 परीक्षण वेक्टरों के साथ सत्यापित करें]

```

### Test Vector 3: HKDF

**Input:**
```python
salt = bytes(32)  # सभी शून्य ikm = b"test input keying material" info = b"ELS2_L1K" n = 44

```

**Computation:**
```python
keys = HKDF(salt, ikm, info, n)

```

**Expected Output:**
```
keys = [44-बाइट हेक्स मान]

```

### Test Vector 4: Base32 Address

**Input:**
```python
pubkey = bytes.fromhex('bbbb' + 'bb' * 30)  # 32 बाइट unblinded_sigtype = 11  # Red25519 blinded_sigtype = 11    # Red25519

```

**Computation:**
```python
address = generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype)

```

**Expected Output:**
```
address = [56 base32 अक्षर].b32.i2p

# पुष्टि करें कि checksum (डेटा अखंडता जाँच मान) का सत्यापन सही ढंग से होता है

```

---

## Appendix C: Glossary

**Alpha (α):** The secret blinding factor used to blind public and private keys. Generated from the destination, date, and optional secret.

**AuthCookie:** A 32-byte random value encrypted for each authorized client, used as input to Layer 2 encryption.

**B (Base Point):** The generator point for the Ed25519 elliptic curve.

**Blinded Key:** A public or private key that has been transformed using the alpha blinding factor. Blinded keys cannot be linked to the original keys without knowing alpha.

**ChaCha20:** A stream cipher providing fast, secure encryption without requiring AES hardware support.

**ClientID:** An 8-byte identifier derived from HKDF output, used to identify authorization entries for clients.

**ClientCookie:** A 32-byte encrypted value containing the authCookie for a specific client.

**Credential:** A 32-byte value derived from the destination's public key and signature types, binding encryption to knowledge of the destination.

**CSRNG:** Cryptographically Secure Random Number Generator. Must provide unpredictable output suitable for key generation.

**DH (Diffie-Hellman):** A cryptographic protocol for securely establishing shared secrets. I2P uses X25519.

**Ed25519:** An elliptic curve signature scheme providing fast signatures with 128-bit security level.

**Ephemeral Key:** A short-lived cryptographic key, typically used once and then discarded.

**Floodfill:** I2P routers that store and serve network database entries, including encrypted LeaseSets.

**HKDF:** HMAC-based Key Derivation Function, used to derive multiple cryptographic keys from a single source.

**L (Order):** The order of the Ed25519 scalar field (approximately 2^252).

**Layer 0 (Outer):** The plaintext portion of an encrypted LeaseSet, containing blinded key and metadata.

**Layer 1 (Middle):** The first encrypted layer, containing client authorization data.

**Layer 2 (Inner):** The innermost encrypted layer, containing the actual LeaseSet2 data.

**LeaseSet2 (LS2):** Second version of I2P's network database entry format, introducing encrypted variants.

**NetDB:** The I2P network database, a distributed hash table storing router and destination information.

**Offline Keys:** A feature allowing the main signing key to remain in cold storage while a transient key handles daily operations.

**PSK (Pre-Shared Key):** A symmetric key shared in advance between two parties, used for PSK client authorization.

**Red25519:** An Ed25519-based signature scheme with key blinding support, based on ZCash RedDSA.

**Salt:** Random data used as input to key derivation functions to ensure unique outputs.

**SigType:** A numeric identifier for signature algorithms (e.g., 7 = Ed25519, 11 = Red25519).

**Subcredential:** A 32-byte value derived from the credential and blinded public key, binding encryption to a specific encrypted LeaseSet.

**Transient Key:** A temporary signing key used with offline keys, with a limited validity period.

**X25519:** An elliptic curve Diffie-Hellman protocol over Curve25519, providing key agreement.

---

## Document Information

**Status:** This document represents the current stable encrypted LeaseSet specification as implemented in I2P since June 2019. The protocol is mature and widely deployed.

**Contributing:** For corrections or improvements to this documentation, please submit issues or pull requests to the I2P specifications repository.

**Support:** For questions about implementing encrypted LeaseSets:
- I2P Forum: https://i2pforum.net/
- IRC: #i2p-dev on OFTC
- Matrix: #i2p-dev:matrix.org

**Acknowledgments:** This specification builds on work by the I2P development team, ZCash cryptography research, and Tor Project's key blinding research.