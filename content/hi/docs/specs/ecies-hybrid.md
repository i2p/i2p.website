---
title: "ECIES-X25519-AEAD-Ratchet हाइब्रिड एन्क्रिप्शन"
description: "ECIES एन्क्रिप्शन प्रोटोकॉल का पोस्ट‑क्वांटम हाइब्रिड वैरिएंट, जो ML‑KEM का उपयोग करता है"
slug: "ecies-hybrid"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## कार्यान्वयन स्थिति

**वर्तमान परिनियोजन:** - **i2pd (C++ कार्यान्वयन)**: संस्करण 2.58.0 (सितंबर 2025) में ML-KEM-512, ML-KEM-768, और ML-KEM-1024 समर्थन के साथ पूर्ण रूप से कार्यान्वित। जब OpenSSL 3.5.0 या उससे नया उपलब्ध हो, तो पोस्ट-क्वांटम एंड-टू-एंड एन्क्रिप्शन डिफ़ॉल्ट रूप से सक्षम होता है। - **Java I2P**: संस्करण 0.9.67 / 2.10.0 (सितंबर 2025) तक अभी तक कार्यान्वित नहीं किया गया है। विशिष्टता अनुमोदित है और भविष्य के रिलीज़ के लिए कार्यान्वयन नियोजित है।

यह विनिर्देश स्वीकृत कार्यक्षमता का वर्णन करता है जो वर्तमान में i2pd में परिनियोजित है और Java I2P कार्यान्वयनों के लिए योजनाबद्ध है।

## सारांश

यह ECIES-X25519-AEAD-Ratchet प्रोटोकॉल [ECIES](/docs/specs/ecies/) का पोस्ट-क्वांटम हाइब्रिड वैरिएंट है। यह प्रस्ताव 169 [Prop169](/proposals/169-pq-crypto/) के अनुमोदन हेतु पहले चरण का प्रतिनिधित्व करता है। समग्र उद्देश्यों, थ्रेट मॉडल (खतरा मॉडल), विश्लेषण, विकल्पों और अतिरिक्त जानकारी के लिए उस प्रस्ताव को देखें।

प्रस्ताव 169 की स्थिति: **Open** (हाइब्रिड ECIES कार्यान्वयन के लिए पहला चरण स्वीकृत)।

यह विनिर्देश मानक [ECIES](/docs/specs/ecies/) से केवल अंतर सम्मिलित करता है और उसे उस विनिर्देश के साथ मिलकर पढ़ा जाना चाहिए।

## डिज़ाइन

हम NIST FIPS 203 मानक [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) का उपयोग करते हैं, जो CRYSTALS-Kyber (संस्करण 3.1, 3, और उससे पुराने) पर आधारित है, लेकिन उसके साथ संगत नहीं है।

Hybrid handshakes (मिश्रित हैंडशेक) परंपरागत X25519 Diffie-Hellman को post-quantum (क्वांटमोत्तर) ML-KEM key encapsulation mechanisms (कुंजी एन्कैप्सुलेशन तंत्र) के साथ संयोजित करते हैं। यह दृष्टिकोण PQNoise शोध में प्रलेखित hybrid forward secrecy (अग्र-गोपनीयता) अवधारणाओं और TLS 1.3, IKEv2 तथा WireGuard में समान कार्यान्वयनों पर आधारित है।

### कुंजी विनिमय

हम Ratchet (संदेश एन्क्रिप्शन में प्रयुक्त कुंजी-अद्यतन तंत्र) के लिए एक हाइब्रिड कुंजी-विनिमय परिभाषित करते हैं। Post-quantum KEM (क्वांटम-प्रतिरोधी Key Encapsulation Mechanism) केवल अल्पकालिक कुंजियाँ प्रदान करता है और Noise IK (Noise प्रोटोकॉल का एक स्थिर-कुंजी हैंडशेक पैटर्न) जैसे स्थिर-कुंजी हैंडशेक का प्रत्यक्ष समर्थन नहीं करता।

हम [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) में निर्दिष्ट तीन ML-KEM (कुंजी संलग्नन तंत्र) रूपांतर परिभाषित करते हैं, जिससे कुल 3 नए एन्क्रिप्शन प्रकार मिलते हैं। हाइब्रिड प्रकार केवल X25519 (एलिप्टिक कर्व डिफी–हेलमैन आधारित कुंजी-विनिमय) के साथ संयोजन में ही परिभाषित हैं।

नए एन्क्रिप्शन प्रकार हैं:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Security Level</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Variant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 1 (AES-128 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-512</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 3 (AES-192 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-768 (Recommended)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 5 (AES-256 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-1024</td>
    </tr>
  </tbody>
</table>
**नोट:** MLKEM768_X25519 (Type 6) अनुशंसित डिफ़ॉल्ट वैरिएंट है, जो उचित ओवरहेड के साथ मजबूत post-quantum security (क्वांटम कंप्यूटिंग के बाद भी सुरक्षित) प्रदान करता है।

Overhead (अतिरिक्त बोझ) केवल X25519 एन्क्रिप्शन की तुलना में काफी अधिक है। IK pattern के लिए सामान्यत: संदेश 1 और 2 के आकार वर्तमान में लगभग 96–103 bytes (अतिरिक्त payload (डेटा सामग्री) से पहले) होते हैं। यह संदेश के प्रकार पर निर्भर करते हुए MLKEM512 के लिए लगभग 9–12 गुना, MLKEM768 के लिए 13–16 गुना, और MLKEM1024 के लिए 17–23 गुना बढ़ जाएगा।

### नए क्रिप्टो की आवश्यकता

- **ML-KEM** (पूर्व में CRYSTALS-Kyber) [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) - मॉड्यूल-लैटिस-आधारित Key-Encapsulation Mechanism (कुंजी संकुलन तंत्र) मानक
- **SHA3-256** (पूर्व में Keccak-512) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - SHA-3 मानक का भाग
- **SHAKE128 और SHAKE256** (SHA3 के लिए XOF विस्तार) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Extendable-Output Functions (विस्तारयोग्य आउटपुट फंक्शंस)

SHA3-256, SHAKE128, और SHAKE256 के लिए परीक्षण वेक्टर [NIST Cryptographic Algorithm Validation Program](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program) में उपलब्ध हैं।

**लाइब्रेरी समर्थन:** - Java: Bouncycastle लाइब्रेरी संस्करण 1.79 और उसके बाद के संस्करण सभी ML-KEM (पोस्ट-क्वांटम कुंजी एन्कैप्सुलेशन विधि) वैरिएंट्स और SHA3/SHAKE फंक्शंस का समर्थन करते हैं - C++: OpenSSL 3.5 और इसके बाद के संस्करणों में पूर्ण ML-KEM समर्थन शामिल है (अप्रैल 2025 में जारी) - Go: ML-KEM और SHA3 के कार्यान्वयन के लिए कई लाइब्रेरी उपलब्ध हैं

## विनिर्देश

### सामान्य संरचनाएँ

कुंजी लंबाइयों और पहचानकर्ताओं के लिए [सामान्य संरचना विनिर्देश](/docs/specs/common-structures/) देखें।

### हैंडशेक पैटर्न

हैंडशेक, हाइब्रिड पोस्ट-क्वांटम सुरक्षा के लिए I2P-विशिष्ट अनुकूलनों के साथ [Noise Protocol Framework](https://noiseprotocol.org/noise.html) के हैंडशेक पैटर्न का उपयोग करते हैं।

निम्नलिखित अक्षर मैपिंग का उपयोग किया जाता है:

- **e** = एक-बार प्रयुक्त अस्थायी कुंजी (X25519)
- **s** = स्थिर कुंजी
- **p** = संदेश पेलोड
- **e1** = एक-बार प्रयुक्त अस्थायी PQ (post-quantum/क्वांटम-पश्चात) कुंजी, Alice से Bob को भेजी गई (I2P-विशिष्ट टोकन)
- **ekem1** = KEM (Key Encapsulation Mechanism/कुंजी एन्कैप्सुलेशन तंत्र) का कूट-पाठ, Bob से Alice को भेजा गया (I2P-विशिष्ट टोकन)

**महत्वपूर्ण नोट:** पैटर्न नाम "IKhfs" और "IKhfselg2" तथा टोकन "e1" और "ekem1" आधिकारिक Noise Protocol Framework (Noise प्रोटोकॉल ढांचा) विनिर्देश में प्रलेखित नहीं हैं; ये I2P-विशिष्ट अनुकूलन हैं। ये Noise IK pattern में ML-KEM (पोस्ट-क्वांटम कुंजी संलग्नीकरण तंत्र) को एकीकृत करने के लिए कस्टम परिभाषाएँ दर्शाते हैं। जबकि हाइब्रिड X25519 + ML-KEM दृष्टिकोण पोस्ट-क्वांटम क्रिप्टोग्राफी अनुसंधान और अन्य प्रोटोकॉल में व्यापक रूप से मान्यता प्राप्त है, यहाँ उपयोग किया गया विशिष्ट नामकरण I2P-विशिष्ट है।

hybrid forward secrecy (संकर अग्र-गोपनीयता) के लिए IK में निम्नलिखित संशोधन लागू किए जाते हैं:

```
Standard IK:              I2P IKhfs (Hybrid):
<- s                      <- s
...                       ...
-> e, es, s, ss, p        -> e, es, e1, s, ss, p
<- e, ee, se, p           <- e, ee, ekem1, se, p
<- p                      <- p
p ->                      p ->

Note: e1 and ekem1 are encrypted within ChaCha20-Poly1305 AEAD blocks.
Note: e1 (ML-KEM public key) and ekem1 (ML-KEM ciphertext) have different sizes.
```
**e1** पैटर्न को निम्नानुसार परिभाषित किया गया है:

```
For Alice (sender):
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++
MixHash(ciphertext)

For Bob (receiver):
// DecryptAndHash(ciphertext)
encap_key = DECRYPT(k, n, ciphertext, ad)
n++
MixHash(ciphertext)
```
**ekem1** पैटर्न इस प्रकार परिभाषित है:

```
For Bob (receiver of encap_key):
(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
MixHash(ciphertext)

// MixKey
MixKey(kem_shared_key)

For Alice (sender of encap_key):
// DecryptAndHash(ciphertext)
kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
MixHash(ciphertext)

// MixKey
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
MixKey(kem_shared_key)
```
### परिभाषित ML-KEM प्रचालन

हम [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) में निर्दिष्ट क्रिप्टोग्राफिक निर्माण घटकों के अनुरूप निम्नलिखित फ़ंक्शनों को परिभाषित करते हैं।

**(encap_key, decap_key) = PQ_KEYGEN()** : Alice encapsulation (एन्कैप्सुलेशन) और decapsulation (डीकैप्सुलेशन) कुंजियाँ बनाती है। encapsulation कुंजी NS संदेश में भेजी जाती है। कुंजी आकार:   - ML-KEM-512: encap_key = 800 बाइट्स, decap_key = 1632 बाइट्स   - ML-KEM-768: encap_key = 1184 बाइट्स, decap_key = 2400 बाइट्स   - ML-KEM-1024: encap_key = 1568 बाइट्स, decap_key = 3168 बाइट्स

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)** : Bob NS संदेश में प्राप्त एन्कैप्सुलेशन कुंजी का उपयोग करके साइफरटेक्स्ट और साझा कुंजी की गणना करता है। साइफरटेक्स्ट NSR संदेश में भेजा जाता है। साइफरटेक्स्ट के आकार:   - ML-KEM-512: 768 बाइट्स   - ML-KEM-768: 1088 बाइट्स   - ML-KEM-1024: 1568 बाइट्स

kem_shared_key की लंबाई सभी तीनों रूपांतरों में हमेशा **32 bytes** होती है।

**kem_shared_key = DECAPS(ciphertext, decap_key)** : Alice NSR संदेश में प्राप्त ciphertext (कूट-पाठ) का उपयोग करके साझा कुंजी की गणना करती है। kem_shared_key हमेशा **32 bytes** होती है।

**Important:** encap_key और ciphertext दोनों Noise हैंडशेक संदेश 1 और 2 में ChaCha20-Poly1305 ब्लॉकों के भीतर एन्क्रिप्ट किए गए होते हैं। इन्हें हैंडशेक प्रक्रिया के हिस्से के रूप में डिक्रिप्ट किया जाएगा।

kem_shared_key को MixKey() के साथ चेनिंग कुंजी में मिश्रित किया जाता है। विवरण के लिए नीचे देखें।

### Noise हैंडशेक KDF (Key Derivation Function - कुंजी व्युत्पत्ति फ़ंक्शन)

#### अवलोकन

हाइब्रिड हैंडशेक पारंपरिक X25519 ECDH को पोस्ट-क्वांटम ML-KEM (कुंजी संकुलन तंत्र) के साथ संयोजित करता है। पहला संदेश, जो Alice से Bob को जाता है, संदेश पेलोड से पहले e1 (ML-KEM संकुलन कुंजी) शामिल करता है। इसे अतिरिक्त कुंजी सामग्री के रूप में माना जाता है; इस पर EncryptAndHash() कॉल करें (Alice के रूप में) या DecryptAndHash() (Bob के रूप में)। फिर संदेश पेलोड को सामान्य रूप से प्रोसेस करें।

दूसरा संदेश, जो Bob से Alice को है, में संदेश पेलोड से पहले ekem1 (ML-KEM ciphertext, यानी ML-KEM से उत्पन्न एन्क्रिप्टेड डेटा) शामिल होता है। इसे अतिरिक्त कुंजी सामग्री के रूप में माना जाता है; इस पर EncryptAndHash() को कॉल करें (Bob के रूप में) या DecryptAndHash() (Alice के रूप में)। फिर kem_shared_key की गणना करें और MixKey(kem_shared_key) को कॉल करें। उसके बाद संदेश पेलोड को सामान्य रूप से प्रसंस्करित करें।

#### Noise (Noise प्रोटोकॉल फ्रेमवर्क) पहचानकर्ता

ये Noise (एक क्रिप्टोग्राफ़िक हैंडशेक प्रोटोकॉल) की इनिशियलाइज़ेशन स्ट्रिंग्स हैं (I2P-विशिष्ट):

- `Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256`

#### NS संदेश के लिए Alice का KDF

'es' संदेश पैटर्न के बाद और 's' संदेश पैटर्न से पहले, जोड़ें:

```
This is the "e1" message pattern:
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++

// MixHash(ciphertext)
h = SHA256(h || ciphertext)

End of "e1" message pattern.

NOTE: For the next section (payload for XK or static key for IK),
the keydata and chain key remain the same,
and n now equals 1 (instead of 0 for non-hybrid).
```
#### NS संदेश के लिए Bob KDF (कुंजी व्युत्पन्न फ़ंक्शन)

'es' संदेश पैटर्न के बाद और 's' संदेश पैटर्न से पहले, जोड़ें:

```
This is the "e1" message pattern:

// DecryptAndHash(encap_key_section)
// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
encap_key = DECRYPT(k, n, encap_key_section, ad)
n++

// MixHash(encap_key_section)
h = SHA256(h || encap_key_section)

End of "e1" message pattern.

NOTE: For the next section (payload for XK or static key for IK),
the keydata and chain key remain the same,
and n now equals 1 (instead of 0 for non-hybrid).
```
#### NSR संदेश के लिए Bob का KDF (कुंजी व्युत्पत्ति फ़ंक्शन)

'ee' संदेश पैटर्न के बाद और 'se' संदेश पैटर्न से पहले, जोड़ें:

```
This is the "ekem1" message pattern:

(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

// MixHash(ciphertext)
h = SHA256(h || ciphertext)

// MixKey(kem_shared_key)
keydata = HKDF(chainKey, kem_shared_key, "", 64)
chainKey = keydata[0:31]

End of "ekem1" message pattern.
```
#### NSR Message के लिए Alice का KDF (कुंजी व्युत्पन्न फ़ंक्शन)

'ee' संदेश पैटर्न के बाद और 'ss' संदेश पैटर्न से पहले, जोड़ें:

```
This is the "ekem1" message pattern:

// DecryptAndHash(kem_ciphertext_section)
// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

// MixHash(kem_ciphertext_section)
h = SHA256(h || kem_ciphertext_section)

// MixKey(kem_shared_key)
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
keydata = HKDF(chainKey, kem_shared_key, "", 64)
chainKey = keydata[0:31]

End of "ekem1" message pattern.
```
#### split() के लिए KDF (कुंजी व्युत्पत्ति फ़ंक्शन)

split() फ़ंक्शन मानक ECIES विनिर्देश से अपरिवर्तित रहता है। हैंडशेक पूर्ण होने के बाद:

```
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]
k_ba = keydata[32:63]
```
ये चल रहे संचार के लिए द्विदिश सत्र कुंजियाँ हैं।

### संदेश प्रारूप

#### NS (नया सत्र) प्रारूप

**परिवर्तन:** वर्तमान ratchet (कुंजी-अपडेट तंत्र) में पहले ChaCha20-Poly1305 खंड में स्थिर कुंजी और दूसरे खंड में पेलोड होता है। ML-KEM (मॉड्यूल-लैटिस आधारित कुंजी एनकैप्सुलेशन तंत्र) के साथ, अब तीन खंड हैं। पहला खंड कूटबद्ध ML-KEM सार्वजनिक कुंजी (encap_key) को समाहित करता है। दूसरा खंड स्थिर कुंजी को समाहित करता है। तीसरा खंड पेलोड को समाहित करता है।

**संदेश आकार:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ key len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">912+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">880+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1296+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1264+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1680+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1648+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
**नोट:** पेलोड में एक DateTime block (तिथि-समय ब्लॉक) होना अनिवार्य है (न्यूनतम 7 बाइट: 1-बाइट प्रकार, 2-बाइट आकार, 4-बाइट टाइमस्टैम्प)। न्यूनतम NS आकार इसी अनुसार गणना किए जा सकते हैं। अतः न्यूनतम व्यावहारिक NS आकार X25519 के लिए 103 बाइट है, और हाइब्रिड वेरिएंट के लिए 919 से 1687 बाइट तक होता है।

तीन ML-KEM (Module Lattice Key Encapsulation Mechanism—मॉड्यूल-लैटिस कुंजी कैप्सुलेशन मैकेनिज़्म) वेरिएंट्स के लिए 816, 1200, और 1584 बाइट्स की आकार-वृद्धि, ML-KEM सार्वजनिक कुंजी के साथ-साथ प्रमाणित एन्क्रिप्शन के लिए 16-बाइट Poly1305 MAC (Message Authentication Code—संदेश प्रमाणीकरण कोड) के कारण होती है।

#### NSR (New Session Reply, नए सत्र का उत्तर) प्रारूप

**परिवर्तन:** वर्तमान ratchet (कुंजी अद्यतन तंत्र) में पहले ChaCha20-Poly1305 (एक AEAD सिफर) खंड का पेलोड खाली होता है और पेलोड दूसरे खंड में होता है. ML-KEM (एक उत्तर-क्वांटम कुंजी एन्कैप्सुलेशन तंत्र) के साथ, अब तीन खंड हैं. पहला खंड एन्क्रिप्टेड ML-KEM साइफरटेक्स्ट समाहित करता है. दूसरे खंड में पेलोड खाली है. तीसरे खंड में पेलोड समाहित है.

**संदेश आकार:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ ct len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">72+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">856+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">824+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">784+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1176+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1144+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1104+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1656+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1624+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1584+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
तीनों ML-KEM (एक post-quantum कुंजी एनकैप्सुलेशन विधि) वेरिएंट्स के लिए आकार में 784, 1104, और 1584 बाइट की बढ़ोतरी, ML-KEM ciphertext (गोपनीयकृत पाठ) के साथ-साथ authenticated encryption (प्रमाणित एन्क्रिप्शन) हेतु 16-बाइट के Poly1305 MAC (संदेश प्रमाणीकरण कोड) को जोड़ने से होती है।

## ओवरहेड विश्लेषण

### कुंजी विनिमय

केवल X25519 की तुलना में hybrid encryption (जिसमें असिमेट्रिक और सिमेट्रिक एन्क्रिप्शन का संयुक्त उपयोग होता है) का ओवरहेड उल्लेखनीय रूप से अधिक है:

- **MLKEM512_X25519**: हैंडशेक संदेश के आकार में लगभग 9-12x वृद्धि (NS: 9.5x, NSR: 11.9x)
- **MLKEM768_X25519**: हैंडशेक संदेश के आकार में लगभग 13-16x वृद्धि (NS: 13.5x, NSR: 16.3x)
- **MLKEM1024_X25519**: हैंडशेक संदेश के आकार में लगभग 17-23x वृद्धि (NS: 17.5x, NSR: 23x)

अतिरिक्त post-quantum सुरक्षा (क्वांटम कंप्यूटर-प्रतिरोधी) लाभों के लिए यह ओवरहेड स्वीकार्य है। संदेश के प्रकार के अनुसार गुणांक बदलते हैं क्योंकि आधार संदेश आकार भिन्न होते हैं (NS न्यूनतम 96 बाइट, NSR न्यूनतम 72 बाइट)।

### बैंडविड्थ संबंधी विचार

न्यूनतम पेलोड के साथ एक सामान्य सत्र स्थापना के लिए: - केवल X25519: ~200 बाइट कुल (NS + NSR) - MLKEM512_X25519: ~1,800 बाइट कुल (9x वृद्धि) - MLKEM768_X25519: ~2,500 बाइट कुल (12.5x वृद्धि) - MLKEM1024_X25519: ~3,400 बाइट कुल (17x वृद्धि)

सत्र स्थापना के बाद, सतत संदेश एन्क्रिप्शन X25519-केवल सत्रों के समान डेटा परिवहन प्रारूप का ही उपयोग करता है, इसलिए बाद के संदेशों के लिए कोई ओवरहेड (अतिरिक्त प्रसंस्करण लागत) नहीं होता।

## सुरक्षा विश्लेषण

### हैंडशेक्स

हाइब्रिड हैंडशेक परंपरागत (X25519) और पोस्ट-क्वांटम (ML-KEM) सुरक्षा दोनों प्रदान करता है। सत्र कुंजियों से समझौता करने के लिए हमलावर को परंपरागत ECDH (Elliptic Curve Diffie-Hellman — एलिप्टिक कर्व डिफ्फी-हेल्मन, कुंजी विनिमय) और पोस्ट-क्वांटम KEM (Key Encapsulation Mechanism — कुंजी एनकैप्सुलेशन तंत्र) **दोनों** को तोड़ना होगा।

यह प्रदान करता है: - **वर्तमान सुरक्षा**: X25519 ECDH (अण्डाकार वक्र डिफी‑हेल्मन कुंजी सहमति) पारंपरिक हमलावरों के विरुद्ध सुरक्षा प्रदान करता है (128-बिट सुरक्षा स्तर) - **भविष्य सुरक्षा**: ML-KEM (पोस्ट-क्वांटम कुंजी संकुलन तंत्र) क्वांटम हमलावरों के विरुद्ध सुरक्षा प्रदान करता है (पैरामीटर सेट के अनुसार बदलता है) - **संकर सुरक्षा**: सत्र से समझौता करने के लिए दोनों को तोड़ा जाना चाहिए (सुरक्षा स्तर = दोनों घटकों का अधिकतम)

### सुरक्षा स्तर

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variant</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NIST Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Classical Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Hybrid Security</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-128 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-192 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
  </tbody>
</table>
**नोट:** हाइब्रिड सुरक्षा स्तर दोनों घटकों में से कमजोर वाले द्वारा सीमित होता है। सभी मामलों में, X25519 128-बिट पारंपरिक सुरक्षा प्रदान करता है। यदि क्रिप्टोग्राफ़िक रूप से प्रासंगिक कोई क्वांटम कंप्यूटर उपलब्ध हो जाता है, तो सुरक्षा स्तर चुने गए ML-KEM (कुंजी एनकैप्सुलेशन तंत्र) पैरामीटर सेट पर निर्भर करेगा।

### Forward Secrecy (ऐसी क्रिप्टोग्राफिक विशेषता जिसमें दीर्घकालिक कुंजी के लीक होने पर भी पिछले सत्रों का डेटा सुरक्षित रहता है)

यह हाइब्रिड दृष्टिकोण forward secrecy (आगे की गोपनीयता) के गुणधर्म बनाए रखता है। सत्र कुंजियाँ अस्थायी X25519 तथा अस्थायी ML-KEM कुंजी-विनिमयों, दोनों से व्युत्पन्न होती हैं। यदि हैंडशेक के बाद X25519 या ML-KEM की अस्थायी निजी कुंजियों में से किसी एक को भी नष्ट कर दिया जाए, तो भले ही दीर्घकालीन स्थिर कुंजियाँ समझौता हो जाएँ, पिछले सत्रों को डिक्रिप्ट नहीं किया जा सकता।

दूसरा संदेश (NSR) भेजे जाने के बाद IK पैटर्न पूर्ण फॉरवर्ड सीक्रेसी (Noise Confidentiality level 5) प्रदान करता है।

## प्रकार प्राथमिकताएँ

इम्प्लीमेंटेशन को कई हाइब्रिड प्रकारों का समर्थन करना चाहिए और सबसे मज़बूत, परस्पर-समर्थित वैरिएंट पर नेगोशिएट करना चाहिए। प्राथमिकता का क्रम इस प्रकार होना चाहिए:

1. **MLKEM768_X25519** (प्रकार 6) - अनुशंसित डिफ़ॉल्ट, सुरक्षा और प्रदर्शन का सर्वोत्तम संतुलन
2. **MLKEM1024_X25519** (प्रकार 7) - संवेदनशील अनुप्रयोगों के लिए सर्वोच्च सुरक्षा
3. **MLKEM512_X25519** (प्रकार 5) - संसाधन-सीमित परिदृश्यों के लिए बेसलाइन पोस्ट-क्वांटम (क्वांटम-प्रतिरोधी) सुरक्षा
4. **X25519** (प्रकार 4) - केवल पारंपरिक (क्लासिकल), संगतता हेतु फॉलबैक

**तर्क:** MLKEM768_X25519 (एक हाइब्रिड कुंजी विनिमय सूट) को डिफ़ॉल्ट के रूप में अनुशंसित किया जाता है क्योंकि यह NIST Category 3 सुरक्षा (AES-192 समकक्ष) प्रदान करता है, जिसे क्वांटम कंप्यूटरों के विरुद्ध पर्याप्त संरक्षण माना जाता है, साथ ही संदेश आकारों को यथोचित बनाए रखते हुए। MLKEM1024_X25519 अधिक सुरक्षा प्रदान करता है, परंतु ओवरहेड में उल्लेखनीय वृद्धि के साथ।

## कार्यान्वयन संबंधी टिप्पणियाँ

### लाइब्रेरी समर्थन

- **Java**: Bouncycastle लाइब्रेरी संस्करण 1.79 (अगस्त 2024) और बाद के संस्करण सभी आवश्यक ML-KEM (NIST का Module Lattice‑based Key Encapsulation Mechanism मानक) वैरिएंट्स और SHA3/SHAKE फ़ंक्शनों का समर्थन करते हैं. FIPS 203 अनुपालन के लिए `org.bouncycastle.pqc.crypto.mlkem.MLKEMEngine` का उपयोग करें.
- **C++**: OpenSSL 3.5 (अप्रैल 2025) और बाद के संस्करणों में EVP_KEM इंटरफ़ेस के माध्यम से ML-KEM समर्थन शामिल है. यह एक दीर्घकालिक समर्थन रिलीज़ है, जिसका रखरखाव अप्रैल 2030 तक किया जाएगा.
- **Go**: ML-KEM और SHA3 के लिए कई तृतीय-पक्ष लाइब्रेरी उपलब्ध हैं, जिनमें Cloudflare की CIRCL लाइब्रेरी शामिल है.

### स्थानांतरण रणनीति

इम्प्लीमेंटेशन को चाहिए: 1. संक्रमण अवधि के दौरान X25519-only और hybrid (मिश्रित) ML-KEM वेरिएंट दोनों का समर्थन करें 2. जब दोनों peers (समकक्ष) उन्हें समर्थन करते हों, तो hybrid वेरिएंट को प्राथमिकता दें 3. backward compatibility (पुराने संस्करणों के साथ अनुकूलता) हेतु X25519-only पर fallback (विकल्प पर वापसी) बनाए रखें 4. डिफ़ॉल्ट वेरिएंट चुनते समय नेटवर्क बैंडविड्थ की सीमाओं पर विचार करें

### साझा Tunnels

बढ़े हुए संदेश आकार साझा tunnel उपयोग को प्रभावित कर सकते हैं। कार्यान्वयन को निम्नलिखित पर विचार करना चाहिए: - जहाँ संभव हो, ओवरहेड को कम करने के लिए हैंडशेक्स को बैच में करना - संग्रहीत स्थिति को कम करने के लिए hybrid sessions (हाइब्रिड सत्र) के लिए कम समाप्ति समय का उपयोग करना - बैंडविड्थ उपयोग की निगरानी करना और उसी के अनुसार पैरामीटर समायोजित करना - सत्र स्थापना ट्रैफ़िक के लिए congestion control (भीड़-नियंत्रण) लागू करना

### नए सेशन आकार से संबंधित विचार

बड़े हैंडशेक संदेशों के कारण, कार्यान्वयन को निम्न करने की आवश्यकता हो सकती है: - सत्र नेगोशिएशन के लिए बफ़र आकार बढ़ाएँ (न्यूनतम 4KB अनुशंसित) - धीमे कनेक्शनों के लिए टाइमआउट मान समायोजित करें (लगभग ~3-17x बड़े संदेशों का ध्यान रखें) - NS/NSR संदेशों में पेलोड डेटा के लिए कंप्रेशन पर विचार करें - यदि ट्रांसपोर्ट लेयर द्वारा आवश्यक हो तो फ्रैगमेंटेशन हैंडलिंग लागू करें

### परीक्षण और मान्यकरण

कार्यान्वयन को यह सत्यापित करना चाहिए: - सही ML-KEM कुंजी निर्माण, encapsulation (लपेटना), और decapsulation (खोलना) - kem_shared_key का Noise KDF (Key Derivation Function—कुंजी व्युत्पन्न फ़ंक्शन) में सही एकीकरण - संदेश आकार की गणनाएँ विनिर्देश से मेल खाती हों - अन्य I2P router कार्यान्वयनों के साथ अंतरसंचालनीयता - जब ML-KEM उपलब्ध न हो तो फॉलबैक (वैकल्पिक) व्यवहार

ML-KEM कार्यों के लिए परीक्षण वेक्टर NIST के [Cryptographic Algorithm Validation Program](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program) में उपलब्ध हैं।

## संस्करण संगतता

**I2P संस्करण क्रमांकन:** I2P दो समानांतर संस्करण संख्याएँ बनाए रखता है: - **Router रिलीज़ संस्करण**: 2.x.x प्रारूप (उदा., 2.10.0 सितंबर 2025 में जारी) - **API/प्रोटोकॉल संस्करण**: 0.9.x प्रारूप (उदा., 0.9.67 router 2.10.0 के अनुरूप है)

यह विशिष्टता प्रोटोकॉल संस्करण 0.9.67 का संदर्भ देती है, जो router रिलीज़ 2.10.0 और उसके बाद के संस्करणों के अनुरूप है।

**संगतता मैट्रिक्स:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.58.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (512/768/1024)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deployed September 2025</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67 / 2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not yet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Planned for future release</td>
    </tr>
  </tbody>
</table>
## संदर्भ

- **[ECIES]**: [ECIES-X25519-AEAD-Ratchet विनिर्देश](/docs/specs/ecies/)
- **[Prop169]**: [प्रस्ताव 169: पोस्ट-क्वांटम क्रिप्टोग्राफी](/proposals/169-pq-crypto/)
- **[FIPS203]**: [NIST FIPS 203 - ML-KEM मानक](https://csrc.nist.gov/pubs/fips/203/final)
- **[FIPS202]**: [NIST FIPS 202 - SHA-3 मानक](https://csrc.nist.gov/pubs/fips/202/final)
- **[Noise]**: [Noise प्रोटोकॉल फ्रेमवर्क](https://noiseprotocol.org/noise.html)
- **[COMMON]**: [सामान्य संरचनाएँ विनिर्देश](/docs/specs/common-structures/)
- **[RFC7539]**: [RFC 7539 - ChaCha20 और Poly1305](https://www.rfc-editor.org/rfc/rfc7539)
- **[RFC5869]**: [RFC 5869 - HKDF](https://www.rfc-editor.org/rfc/rfc5869)
- **[OpenSSL]**: [OpenSSL 3.5 ML-KEM दस्तावेज़ीकरण](https://docs.openssl.org/3.5/man7/EVP_KEM-ML-KEM/)
- **[Bouncycastle]**: [Bouncycastle जावा क्रिप्टोग्राफी लाइब्रेरी](https://www.bouncycastle.org/)

---
