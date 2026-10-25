---
title: "PQ Hybrid ECIES-X25519-AEAD-Ratchet"
description: "ML-KEM का उपयोग करते हुए ECIES एन्क्रिप्शन प्रोटोकॉल का पोस्ट-क्वांटम हाइब्रिड वेरिएंट"
slug: "ecies-hybrid"
category: "प्रोटोकॉल"
lastUpdated: "2026-04"
accurateFor: "0.9.69"
---

## नोट

विभिन्न router कार्यान्वयनों में implementation, testing, और rollout प्रगति पर है। स्थिति के लिए उन implementations के documentation की जांच करें।

## अवलोकन

यह ECIES-X25519-AEAD-Ratchet protocol [ECIES](/docs/specs/ecies/) का PQ Hybrid variant है। यह समग्र PQ प्रस्ताव [Prop169](/proposals/169-pq-crypto/) का पहला चरण है जिसे अनुमोदित किया गया है। समग्र लक्ष्यों, threat models, विश्लेषण, विकल्पों और अतिरिक्त जानकारी के लिए उस प्रस्ताव को देखें।

यह विनिर्देश केवल मानक [ECIES](/docs/specs/ecies/) से अंतर शामिल करता है और इसे उस विनिर्देश के साथ मिलकर पढ़ा जाना चाहिए।

## डिज़ाइन

हम NIST FIPS 203 मानक [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) का समर्थन करते हैं जो CRYSTALS-Kyber पर आधारित है, लेकिन उसके साथ संगत नहीं है।

Hybrid handshakes [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) में निर्दिष्ट के अनुसार हैं।

### key एक्सचेंज

हम Ratchet के लिए एक हाइब्रिड key exchange को परिभाषित करते हैं। PQ KEM केवल ephemeral keys प्रदान करता है, और static-key handshakes जैसे कि Noise IK का प्रत्यक्ष समर्थन नहीं करता है।

हम तीन ML-KEM वेरिएंट्स को [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) के अनुसार परिभाषित करते हैं, कुल मिलाकर 3 नए एन्क्रिप्शन प्रकारों के लिए। Hybrid प्रकार केवल X25519 के साथ संयोजन में परिभाषित हैं।

नए एन्क्रिप्शन प्रकार हैं:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
</table>
Overhead काफी अधिक होगा। वर्तमान में IK के लिए सामान्य message 1 और 2 के आकार लगभग 100 bytes (किसी भी अतिरिक्त payload से पहले) हैं। यह algorithm के आधार पर 8x से 15x तक बढ़ जाएगा।

### नई क्रिप्टो आवश्यक

- ML-KEM (पूर्व में CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- SHA3-128 (पूर्व में Keccak-256) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) केवल SHAKE128 के लिए उपयोग किया जाता है
- SHA3-256 (पूर्व में Keccak-512) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 और SHAKE256 (SHA3-128 और SHA3-256 के लिए XOF एक्सटेंशन)
  [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

SHA3-256, SHAKE128, और SHAKE256 के लिए टेस्ट वेक्टर [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values) पर उपलब्ध हैं।

ध्यान दें कि Java bouncycastle library उपरोक्त सभी का समर्थन करती है। C++ library का समर्थन OpenSSL 3.5 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/) में है।

## विनिर्देश

### सामान्य संरचनाएं

key की लंबाई और identifiers के लिए common structures specification [COMMON](/docs/specs/common-structures/) देखें।

### हैंडशेक पैटर्न

Handshakes [Noise](https://noiseprotocol.org/noise.html) handshake patterns का उपयोग करते हैं।

निम्नलिखित अक्षर मैपिंग का उपयोग किया जाता है:

- e = एक-बार का ephemeral key
- s = static key
- p = message payload
- e1 = एक-बार का ephemeral PQ key, Alice से Bob को भेजा गया
- ekem1 = KEM ciphertext, Bob से Alice को भेजा गया

hybrid forward secrecy (hfs) के लिए XK और IK में निम्नलिखित संशोधन [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) सेक्शन 5 में निर्दिष्ट हैं:

```
IK:                         IKhfs:
<- s                        <- s
...                         ...
-> e, es, s, ss, p          -> e, es, e1, s, ss, p
<- tag, e, ee, se, p        <- tag, e, ee, ekem1, se, p
<- p                        <- p
p ->                        p ->

e1 and ekem1 are encrypted. See pattern definitions below.
NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
e1 पैटर्न को निम्नलिखित रूप में परिभाषित किया गया है, जैसा कि [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) सेक्शन 4 में निर्दिष्ट है:

```
For Alice:
    (encap_key, decap_key) = PQ_KEYGEN()

    // EncryptAndHash(encap_key)
    ciphertext = ENCRYPT(k, n, encap_key, ad)
    n++
    MixHash(ciphertext)

For Bob:
    // DecryptAndHash(ciphertext)
    encap_key = DECRYPT(k, n, ciphertext, ad)
    n++
    MixHash(ciphertext)
```
ekem1 पैटर्न निम्नलिखित रूप में परिभाषित है, जैसा कि [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) खंड 4 में निर्दिष्ट है:

```
For Bob:
    (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

    // EncryptAndHash(kem_ciphertext)
    ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
    MixHash(ciphertext)

    // MixKey
    MixKey(kem_shared_key)

For Alice:
    // DecryptAndHash(ciphertext)
    kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
    MixHash(ciphertext)

    // MixKey
    kem_shared_key = DECAPS(kem_ciphertext, decap_key)
    MixKey(kem_shared_key)
```
### परिभाषित ML-KEM ऑपरेशन्स

हम निम्नलिखित functions को परिभाषित करते हैं जो cryptographic building blocks के अनुरूप हैं जैसा कि [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) में परिभाषित किया गया है।

**(encap_key, decap_key) = PQ_KEYGEN()**

Alice encapsulation और decapsulation keys बनाती है। Encapsulation key को NS message में भेजा जाता है। encap_key और decap_key के sizes ML-KEM variant के आधार पर अलग-अलग होते हैं।

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)**

Bob प्राप्त NS संदेश में मिले ciphertext का उपयोग करके ciphertext और shared key की गणना करता है। ciphertext को NSR संदेश में भेजा जाता है। ciphertext का आकार ML-KEM variant के आधार पर अलग होता है। kem_shared_key हमेशा 32 bytes का होता है।

**kem_shared_key = DECAPS(ciphertext, decap_key)**

Alice को NSR संदेश में प्राप्त ciphertext का उपयोग करके shared key की गणना करती है। kem_shared_key हमेशा 32 bytes का होता है।

ध्यान दें कि encap_key और ciphertext दोनों Noise handshake messages 1 और 2 में ChaCha/Poly blocks के अंदर एन्क्रिप्टेड हैं। ये handshake प्रक्रिया के भाग के रूप में डिक्रिप्ट किए जाएंगे।

kem_shared_key को chaining key के साथ MixHash() का उपयोग करके मिलाया जाता है। विवरण के लिए नीचे देखें।

### Noise Handshake KDF

#### अवलोकन

Hybrid handshake को [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) में परिभाषित किया गया है। पहला संदेश, Alice से Bob तक, message payload से पहले e1, encapsulation key, को शामिल करता है। इसे एक अतिरिक्त static key के रूप में माना जाता है; इस पर EncryptAndHash() को (Alice के रूप में) या DecryptAndHash() को (Bob के रूप में) call करें। फिर message payload को सामान्य रूप से process करें।

दूसरा संदेश, Bob से Alice को, message payload से पहले ekem1, ciphertext को शामिल करता है। इसे एक अतिरिक्त static key के रूप में माना जाता है; इस पर EncryptAndHash() को (Bob के रूप में) या DecryptAndHash() को (Alice के रूप में) कॉल करें। फिर, kem_shared_key की गणना करें और MixKey(kem_shared_key) को कॉल करें। फिर message payload को सामान्य रूप से प्रोसेस करें।

#### नॉइज़ पहचानकर्ता

ये Noise initialization strings हैं:

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### NS संदेश के लिए Alice KDF

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### NS संदेश के लिए Bob KDF

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### NSR संदेश के लिए Bob KDF

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
#### NSR संदेश के लिए Alice KDF

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
#### split() के लिए KDF

अपरिवर्तित

### संदेश प्रारूप

#### NS फॉर्मेट

परिवर्तन: वर्तमान ratchet में पहले ChaCha खंड में static key और दूसरे खंड में payload शामिल था। ML-KEM के साथ, अब तीन खंड हैं। पहले खंड में encrypted PQ public key है। दूसरे खंड में static key है। तीसरे खंड में payload है।

एन्क्रिप्टेड प्रारूप:

```
+----+----+----+----+----+----+----+----+
|                                       |
+         New Session Ephemeral         +
|            Public Key                 |
+            32 bytes                   +
|      Encoded with Elligator2          |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for encap_key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for Static Key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
डिक्रिप्टेड फॉर्मेट:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|            (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
आकार:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">pl len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">96+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">912+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1296+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1360+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1680+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
ध्यान दें कि payload में एक DateTime block होना आवश्यक है, इसलिए न्यूनतम payload का आकार 7 है। न्यूनतम NS आकार की गणना तदनुसार की जा सकती है।

#### NSR प्रारूप

परिवर्तन: वर्तमान ratchet में पहले ChaCha सेक्शन के लिए खाली payload है, और दूसरे सेक्शन में payload है। ML-KEM के साथ, अब तीन सेक्शन हैं। पहले सेक्शन में एन्क्रिप्टेड PQ ciphertext है। दूसरे सेक्शन में खाली payload है। तीसरे सेक्शन में payload है।

एन्क्रिप्टेड फॉर्मेट:

```
+----+----+----+----+----+----+----+----+
|       Session Tag 8 bytes             |
+----+----+----+----+----+----+----+----+
|                                       |
+       Ephemeral Public Key            +
|            32 bytes                   |
+      Encoded with Elligator2          +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for ciphertext Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+   (MAC) for key Section (no data)     +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
डिक्रिप्टेड प्रारूप:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

empty

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
आकार:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">72+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">856+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1176+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1656+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
ध्यान दें कि जबकि NSR में आमतौर पर एक गैर-शून्य payload होता है, ratchet specification [ECIES](/docs/specs/ecies/) इसे आवश्यक नहीं मानता, इसलिए न्यूनतम payload का आकार 0 है। न्यूनतम NSR आकार की गणना तदनुसार की जा सकती है।

## ओवरहेड विश्लेषण

### की एक्सचेंज

आकार वृद्धि (बाइट्स):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (NS)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (NSR)</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+784</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1104</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
</tr>
</table>
गति:

[CLOUDFLARE](https://blog.cloudflare.com/pq-2024/) द्वारा रिपोर्ट की गई गति:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Relative speed</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 DH/keygen</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">baseline</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2.25x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1.5x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1x (same)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">XK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH (keygen + 3 DH)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower</td>
</tr>
</table>
## सुरक्षा विश्लेषण

NIST सुरक्षा श्रेणियों का सारांश [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) स्लाइड 10 में दिया गया है। प्रारंभिक मानदंड: hybrid protocols के लिए हमारी न्यूनतम NIST सुरक्षा श्रेणी 2 होनी चाहिए और PQ-only के लिए 3 होनी चाहिए।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Category</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Secure As</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES128</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA256</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES192</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA384</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES256</td>
</tr>
</table>
### हैंडशेक

ये सभी हाइब्रिड प्रोटोकॉल हैं। संभवतः MLKEM768 को प्राथमिकता देने की आवश्यकता है; MLKEM512 पर्याप्त सुरक्षित नहीं है।

NIST सुरक्षा श्रेणियां [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Algorithm</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Security Category</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
## प्रकार प्राथमिकताएं

सुरक्षा श्रेणी और की लंबाई के आधार पर प्रारंभिक समर्थन के लिए अनुशंसित प्रकार है:

MLKEM768_X25519 (प्रकार 6)

## कार्यान्वयन टिप्पणियां

### लाइब्रेरी सहायता

Bouncycastle, BoringSSL, और WolfSSL लाइब्रेरीज अब MLKEM का समर्थन करती हैं। OpenSSL समर्थन उनकी 3.5 रिलीज़ 8 अप्रैल, 2025 में होगा [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)।

### साझा Tunnels

संदेश 1 (New Session Message) की लंबाई जांच के आधार पर समान tunnels पर कई protocols का स्वचालित वर्गीकरण/पहचान संभव होनी चाहिए। MLKEM512_X25519 को उदाहरण के रूप में लेते हुए, संदेश 1 की लंबाई वर्तमान ratchet protocol से 816 bytes अधिक है, और न्यूनतम संदेश 1 का आकार (केवल DateTime payload के साथ) 919 bytes है। वर्तमान ratchet के साथ अधिकतर संदेश 1 के आकार में 816 bytes से कम payload होता है, इसलिए उन्हें non-hybrid ratchet के रूप में वर्गीकृत किया जा सकता है। बड़े संदेश संभवतः POSTs हैं जो दुर्लभ हैं।

तो अनुशंसित रणनीति यह है:

- यदि message 1 919 bytes से कम है, तो यह वर्तमान ratchet protocol है।
- यदि message 1 919 bytes से अधिक या बराबर है, तो यह संभवतः MLKEM512_X25519 है। पहले MLKEM512_X25519 की कोशिश करें, और यदि यह विफल हो जाता है, तो वर्तमान ratchet protocol की कोशिश करें।

यह हमें समान destination पर standard ratchet और hybrid ratchet को कुशलता से समर्थन करने की अनुमति देना चाहिए, जैसे हमने पहले समान destination पर ElGamal और ratchet को समर्थन किया था। इसलिए, हम MLKEM hybrid protocol में बहुत तेज़ी से माइग्रेट कर सकते हैं, जितना कि तब हो सकता यदि हम समान destination के लिए dual-protocols का समर्थन नहीं कर सकते, क्योंकि हम मौजूदा destinations में MLKEM समर्थन जोड़ सकते हैं।

आवश्यक समर्थित संयोजन हैं:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

निम्नलिखित संयोजन जटिल हो सकते हैं, और इनका समर्थन करना आवश्यक नहीं है, लेकिन ये implementation-dependent हो सकते हैं:

- एक से अधिक MLKEM
- ElG + एक या अधिक MLKEM
- X25519 + एक या अधिक MLKEM
- ElG + X25519 + एक या अधिक MLKEM

एक ही destination पर कई MLKEM algorithms (उदाहरण के लिए, MLKEM512_X25519 और MLKEM_768_X25519) का समर्थन करना आवश्यक नहीं है। केवल एक चुनें। Implementation-dependent है।

एक ही destination पर तीन algorithms (उदाहरण के लिए X25519, MLKEM512_X25519, और MLKEM769_X25519) का समर्थन करना आवश्यक नहीं है। वर्गीकरण और retry strategy बहुत जटिल हो सकती है। कॉन्फ़िगरेशन और कॉन्फ़िगरेशन UI बहुत जटिल हो सकता है। Implementation-dependent।

एक ही destination पर ElGamal और hybrid algorithms दोनों को support करना आवश्यक नहीं है। ElGamal अप्रचलित है, और ElGamal + hybrid केवल (बिना X25519 के) का कोई विशेष अर्थ नहीं है। साथ ही, ElGamal और Hybrid New Session Messages दोनों बड़े होते हैं, इसलिए classification strategies को अक्सर दोनों decryptions को आज़माना पड़ता है, जो अकुशल होगा। Implementation-dependent।

क्लाइंट समान tunnels पर X25519 और hybrid प्रोटोकॉल के लिए समान या अलग X25519 static keys का उपयोग कर सकते हैं, यह implementation पर निर्भर करता है।

### फॉरवर्ड सिक्योरिटी

ECIES स्पेसिफिकेशन New Session Message payload में Garlic Messages की अनुमति देता है, जो प्रारंभिक स्ट्रीमिंग पैकेट, आमतौर पर एक HTTP GET, के 0-RTT डिलीवरी की अनुमति देता है, client के leaseset के साथ। हालांकि, New Session Message payload में forward secrecy नहीं है। चूंकि यह प्रस्ताव ratchet के लिए enhanced forward secrecy पर जोर दे रहा है, implementations स्ट्रीमिंग payload, या पूर्ण स्ट्रीमिंग संदेश को शामिल करना पहले Existing Session Message तक स्थगित कर सकते या करना चाहिए। यह 0-RTT डिलीवरी की कीमत पर होगा। रणनीतियां traffic type या tunnel type, या उदाहरण के लिए GET vs. POST पर भी निर्भर हो सकती हैं। Implementation-dependent।

### नया सेशन आकार

MLKEM New Session Message का आकार नाटकीय रूप से बढ़ा देगा, जैसा कि ऊपर वर्णित है। यह tunnel के माध्यम से New Session Message की डिलीवरी की विश्वसनीयता को काफी कम कर सकता है, जहां उन्हें कई 1024 बाइट tunnel संदेशों में खंडित करना पड़ता है। डिलीवरी की सफलता खंडों की घातांकीय संख्या के अनुपातिक होती है। Implementation विभिन्न रणनीतियों का उपयोग करके संदेश के आकार को सीमित कर सकते हैं, 0-RTT डिलीवरी की कीमत पर। Implementation-dependent है।

## संदर्भ

- [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
- [COMMON](/docs/specs/common-structures/)
- [ECIES](/docs/specs/ecies/)
- [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [FORUM](http://zzz.i2p/topics/3294)
- [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
- [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
- [Noise](https://noiseprotocol.org/noise.html)
- [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
- [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
- [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
- [Prop169](/proposals/169-pq-crypto/)
