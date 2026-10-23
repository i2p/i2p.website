---
title: "PQ Hybrid NTCP2"
description: "ML-KEM का उपयोग करते हुए NTCP2 transport protocol का post-quantum hybrid variant"
slug: "ntcp2-hybrid"
lastupdated: "2026-10"
category: "ट्रांसपोर्ट"
accurateFor: "0.9.71"
---

### स्थिति

बीटा Q1 2026, रिलीज़ Q2 2026

## अवलोकन

यह NTCP2 transport protocol का hybrid post-quantum variant है, जैसा कि Proposal 169 में डिज़ाइन किया गया है। अतिरिक्त पृष्ठभूमि के लिए उस proposal को देखें।

PQ Hybrid NTCP2 केवल standard NTCP2 के समान address और port पर ही परिभाषित है। किसी अलग port पर संचालन, या standard NTCP2 समर्थन के बिना, अनुमतित नहीं है, और कई वर्षों तक नहीं होगा, जब तक कि standard NTCP2 deprecated नहीं हो जाता।

यह specification केवल उन परिवर्तनों का दस्तावेजीकरण करती है जो PQ Hybrid को समर्थन देने के लिए standard NTCP2 में आवश्यक हैं। baseline implementation के विवरण के लिए NTCP2 specification देखें।

## डिज़ाइन

हम NIST FIPS 203 और 204 मानकों का समर्थन करते हैं [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) जो CRYSTALS-Kyber और CRYSTALS-Dilithium (संस्करण 3.1, 3, और पुराने) पर आधारित हैं, लेकिन उनके साथ संगत नहीं हैं।

### कुंजी विनिमय

PQ KEM केवल ephemeral keys प्रदान करता है, और Noise XK और IK जैसे static-key handshakes का प्रत्यक्ष समर्थन नहीं करता। encryption types वही हैं जो PQ Hybrid Ratchet में उपयोग किए जाते हैं और common structures document [/docs/specs/common-structures/](/docs/specs/common-structures/) में परिभाषित हैं, जैसा कि [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) में है। Hybrid types केवल X25519 के संयोजन में ही परिभाषित हैं।

एन्क्रिप्शन प्रकार हैं:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 Version</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
### कानूनी संयोजन

नए encryption प्रकार RouterAddresses में दर्शाए गए हैं। key certificate में encryption प्रकार type 4 बना रहेगा।

## विनिर्देश

### हैंडशेक पैटर्न

Handshakes [Noise Protocol](https://noiseprotocol.org/noise.html) handshake patterns का उपयोग करते हैं।

निम्नलिखित अक्षर मैपिंग का उपयोग किया गया है:

- e = एक-बार ephemeral key
- s = static key
- p = संदेश payload
- e1 = एक-बार ephemeral PQ key, Alice से Bob को भेजी गई
- ekem1 = KEM ciphertext, Bob से Alice को भेजा गया

हाइब्रिड फॉरवर्ड सिक्योरिटी (hfs) के लिए XK और IK में निम्नलिखित संशोधन [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) सेक्शन 5 में निर्दिष्ट अनुसार हैं:

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
e1 pattern को निम्नलिखित रूप में परिभाषित किया गया है, जैसा कि [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) section 4 में निर्दिष्ट है:

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
ekem1 पैटर्न को निम्नलिखित रूप में परिभाषित किया गया है, जैसा कि [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) की धारा 4 में निर्दिष्ट है:

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
### Noise Handshake KDF

#### अवलोकन

हाइब्रिड handshake को [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) में परिभाषित किया गया है। पहला संदेश, Alice से Bob तक, message payload से पहले e1, encapsulation key शामिल करता है। इसे एक अतिरिक्त static key के रूप में माना जाता है; इस पर EncryptAndHash() को कॉल करें (Alice के रूप में) या DecryptAndHash() (Bob के रूप में)। फिर message payload को सामान्य रूप से प्रोसेस करें।

दूसरा संदेश, Bob से Alice तक, में ekem1, ciphertext शामिल है, message payload से पहले। इसे एक अतिरिक्त static key के रूप में माना जाता है; इस पर EncryptAndHash() को कॉल करें (Bob के रूप में) या DecryptAndHash() (Alice के रूप में)। फिर, kem_shared_key की गणना करें और MixKey(kem_shared_key) को कॉल करें। फिर message payload को सामान्य रूप से प्रोसेस करें।

#### परिभाषित ML-KEM संचालन

हम निम्नलिखित functions को परिभाषित करते हैं जो [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) में परिभाषित cryptographic building blocks के अनुरूप हैं।

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

ध्यान दें कि encap_key और ciphertext दोनों Noise handshake messages 1 और 2 में ChaCha/Poly blocks के अंदर encrypted हैं। ये handshake process के हिस्से के रूप में decrypt हो जाएंगे।

kem_shared_key को chaining key के साथ MixHash() का उपयोग करके मिलाया जाता है। विवरण के लिए नीचे देखें।

#### संदेश 1 के लिए Alice KDF

'es' संदेश पैटर्न के बाद और payload से पहले, जोड़ें:

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
#### Message 1 के लिए Bob KDF

'es' संदेश पैटर्न के बाद और payload से पहले, जोड़ें:

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
#### संदेश 2 के लिए Bob KDF

XK के लिए: 'ee' संदेश पैटर्न के बाद और payload से पहले, जोड़ें:

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### Message 2 के लिए Alice KDF

'ee' संदेश पैटर्न के बाद, जोड़ें:

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### संदेश 3 के लिए KDF (केवल XK)

अपरिवर्तित

#### split() के लिए KDF

अपरिवर्तित

### हैंडशेक विवरण

#### शोर पहचानकर्ता

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

परिवर्तन: वर्तमान NTCP2 में केवल ChaCha सेक्शन के विकल्प शामिल हैं। ML-KEM के साथ, ChaCha सेक्शन में एन्क्रिप्टेड PQ पब्लिक की भी शामिल होगी।

ताकि PQ और non-PQ NTCP2 दोनों को एक ही router पते और पोर्ट पर समर्थित किया जा सके, हम X मान (X25519 ephemeral public key) के सबसे महत्वपूर्ण bit का उपयोग यह दर्शाने के लिए करते हैं कि यह एक PQ कनेक्शन है। यह bit non-PQ कनेक्शन के लिए हमेशा unset होता है।

Alice के लिए, संदेश को Noise द्वारा एन्क्रिप्ट करने के बाद, लेकिन X के AES obfuscation से पहले, X[31] |= 0x7f सेट करें।

Bob के लिए, X के AES de-obfuscation के बाद, X[31] & 0x80 का परीक्षण करें। यदि बिट सेट है, तो इसे X[31] &= 0x7f के साथ साफ़ करें, और PQ कनेक्शन के रूप में Noise के माध्यम से decrypt करें। यदि बिट साफ़ है, तो सामान्य रूप से non-PQ कनेक्शन के रूप में Noise के माध्यम से decrypt करें।

PQ NTCP2 के लिए जो एक अलग router पते और port पर advertise किया गया है, यह आवश्यक नहीं है।

अतिरिक्त जानकारी के लिए, नीचे दिए गए Published Addresses अनुभाग को देखें।

कच्ची सामग्री:

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
अनएन्क्रिप्टेड डेटा (Poly1305 प्रमाणीकरण टैग दिखाया नहीं गया):

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
नोट: message 1 options block में version field को 2 पर सेट करना होगा, PQ connections के लिए भी।

आकार:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1264+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1232</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
</table>
नोट: Type codes केवल आंतरिक उपयोग के लिए हैं। Router type 4 ही रहेंगे, और समर्थन router addresses में दर्शाया जाएगा।

#### 2) SessionCreated

कच्ची सामग्री:

कच्ची सामग्री:

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  -           16 bytes                    -
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
आकार:

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
आकार:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">784</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1168+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1104</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
</table>
नोट: Type codes केवल आंतरिक उपयोग के लिए हैं। Router type 4 ही रहेंगे, और समर्थन router addresses में दर्शाया जाएगा।

#### 3) SessionConfirmed

अपरिवर्तित

#### Key Derivation Function (KDF) (डेटा चरण के लिए)

अपरिवर्तित

#### प्रकाशित पते

गैर-PQ, गैर-firewalled के समान address/port का उपयोग करें। केवल एक PQ variant समर्थित है। router address में, v=2 प्रकाशित करें (हमेशा की तरह) और नया parameter pq=[3|4|5] MLKEM 512/768/1024 को इंगित करने के लिए। Alice session request में ephemeral key के MSB को सेट करती है (key[31] & 0x80) यह इंगित करने के लिए कि यह एक hybrid connection है। ऊपर देखें। पुराने routers pq parameter को नज़रअंदाज़ करेंगे और सामान्य रूप से गैर-pq connect करेंगे।

गैर-PQ के रूप में अलग address/port, या PQ-only, non-firewalled समर्थित नहीं है। यह तब तक लागू नहीं किया जाएगा जब तक कि गैर-PQ NTCP2 अक्षम नहीं हो जाता, जो अभी से कई साल बाद होगा। जब गैर-PQ अक्षम हो जाएगा, तो कई PQ variants समर्थित हो सकते हैं, लेकिन प्रत्येक address के लिए केवल एक। जब यह समर्थित होगा, router address में, MLKEM 512/768/1024 को इंगित करने के लिए v=[3|4|5] प्रकाशित करें। Alice ephemeral key के MSB को सेट नहीं करता। पुराने routers v parameter की जांच करेंगे और इस address को असमर्थित के रूप में छोड़ देंगे।

Firewalled addresses (कोई IP प्रकाशित नहीं): router address में, v=2 प्रकाशित करें (सामान्य रूप से)। pq parameter प्रकाशित करने की कोई आवश्यकता नहीं है।

Alice, Bob द्वारा प्रकाशित PQ variant का उपयोग करके PQ Bob से जुड़ सकती है, चाहे Alice अपनी router info में pq support का विज्ञापन करे या न करे, या चाहे वह समान variant का विज्ञापन करे।

वर्तमान विनिर्देश में, संदेश 1 और 2 को "उचित" मात्रा में padding के साथ परिभाषित किया गया है, जिसमें 0-31 bytes की सिफारिश की गई है, और कोई अधिकतम सीमा निर्दिष्ट नहीं है।

#### अधिकतम पैडिंग

API 0.9.68 (रिलीज़ 2.11.0) तक, Java I2P ने non-PQ connections के लिए अधिकतम 256 bytes padding को implement किया था, हालांकि यह पहले documented नहीं था। API 0.9.69 (रिलीज़ 2.12.0) से, Java I2P non-PQ connections के लिए वही max padding implement करता है जो MLKEM-512 के लिए करता है। नीचे table देखें।

परिभाषित संदेश आकार को अधिकतम padding के रूप में उपयोग करें, यानी अधिकतम padding PQ कनेक्शन के लिए संदेश आकार को दोगुना कर देगा, निम्नलिखित के अनुसार:

आकार वृद्धि (बाइट्स):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message Max Padding</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">non-PQ (thru 0.9.68)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">non-PQ (as of 0.9.69)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-512</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-768</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-1024</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Session Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1264</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Session Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1168</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648</td>
</tr>
</table>
## ओवरहेड विश्लेषण

### कुंजी विनिमय

NIST सिक्योरिटी श्रेणियों का सारांश [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) slide 10 में दिया गया है। प्रारंभिक मानदंड: हमारी न्यूनतम NIST सिक्योरिटी श्रेणी hybrid प्रोटोकॉल के लिए 2 और PQ-only के लिए 3 होनी चाहिए।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (Msg 1)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (Msg 2)</th>
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
## सुरक्षा विश्लेषण

ये सभी हाइब्रिड प्रोटोकॉल हैं। implementations को MLKEM768 को प्राथमिकता देनी चाहिए; MLKEM512 पर्याप्त सुरक्षित नहीं है।

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

NIST सुरक्षा श्रेणियां [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

Bouncycastle, BoringSSL, और WolfSSL लाइब्रेरी अब MLKEM और MLDSA का समर्थन करती हैं। OpenSSL का समर्थन उनकी 3.5 रिलीज़ में 8 अप्रैल, 2025 को होगा [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)।

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
## कार्यान्वयन टिप्पणियाँ

### लाइब्रेरी सपोर्ट

हम session request में ephemeral key का MSB (key[31] & 0x80) सेट करते हैं यह दर्शाने के लिए कि यह एक hybrid connection है। यह हमें समान port पर standard NTCP और hybrid NTCP दोनों चलाने की अनुमति देता है। inbound के लिए केवल एक hybrid variant समर्थित है, और router address में advertise किया जाता है। उदाहरण के लिए, pq=3 या pq=4।

### इनबाउंड ट्रैफिक की पहचान

Alice के रूप में, एक PQ कनेक्शन के लिए, obfuscation से पहले, X[31] |= 0x80 सेट करें। यह X को एक अवैध X25519 public key बना देता है। Obfuscation के बाद, AES-CBC इसे randomize कर देगा। Obfuscation के बाद X का MSB random होगा।

#### अस्पष्टीकरण

Bob के रूप में, de-obfuscation के बाद जांचें कि क्या (X[31] & 0x80) != 0 है। यदि हां, तो यह एक PQ connection है।

NTCP2-PQ के लिए आवश्यक न्यूनतम router संस्करण TBD है।

नोट: टाइप कोड केवल आंतरिक उपयोग के लिए हैं। Router टाइप 4 ही रहेंगे, और सहायता router addresses में दिखाई जाएगी।

नोट: Type codes केवल आंतरिक उपयोग के लिए हैं। Router type 4 ही रहेंगे, और समर्थन router addresses में दर्शाया जाएगा।

## Router संगतता

### Transport नाम

सभी मामलों में, हमेशा की तरह NTCP2 transport name का उपयोग करें। पुराने routers pq parameter को नज़रअंदाज़ कर देंगे और हमेशा की तरह standard NTCP2 के साथ connect होंगे।

## संदर्भ

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
