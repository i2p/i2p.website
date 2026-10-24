---
title: "PQ Hybrid SSU2"
description: "ML-KEM का उपयोग करते हुए SSU2 ट्रांसपोर्ट प्रोटोकॉल का पोस्ट-क्वांटम हाइब्रिड वेरिएंट"
slug: "ssu2-hybrid"
lastupdated: "2026-10"
category: "Transports"
accurateFor: "0.9.71"
---

### स्थिति

बीटा Q2 2026, रिलीज़ Q3 2026

## अवलोकन

यह SSU2 ट्रांसपोर्ट प्रोटोकॉल का हाइब्रिड पोस्ट-क्वांटम वेरिएंट है, जैसा कि Proposal 169 में डिज़ाइन किया गया है। अतिरिक्त पृष्ठभूमि जानकारी के लिए उस proposal को देखें।

PQ Hybrid SSU2 केवल उसी address और port पर परिभाषित है जहाँ standard SSU2 चलता है। किसी अलग port पर, या standard SSU2 समर्थन के बिना, इसका संचालन अनुमत नहीं है, और कई वर्षों तक अनुमत नहीं होगा, जब तक कि standard SSU2 को deprecated नहीं कर दिया जाता।

यह विशिष्टता केवल उन परिवर्तनों को दस्तावेज़ीकृत करती है जो PQ Hybrid को सपोर्ट करने के लिए मानक SSU2 में आवश्यक हैं। आधारभूत कार्यान्वयन विवरण के लिए SSU2 विशिष्टता देखें।

## डिज़ाइन

हम NIST FIPS 203 और 204 मानकों [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) का समर्थन करते हैं, जो CRYSTALS-Kyber और CRYSTALS-Dilithium (संस्करण 3.1, 3, और पुराने) पर आधारित हैं, लेकिन उनके साथ संगत (compatible) नहीं हैं।

### Key Exchange

PQ KEM केवल ephemeral keys प्रदान करता है, और Noise XK तथा IK जैसे static-key handshakes को सीधे support नहीं करता। encryption types वही हैं जो PQ Hybrid Ratchet में उपयोग की जाती हैं और इन्हें common structures document [/docs/specs/common-structures/](/docs/specs/common-structures/) में परिभाषित किया गया है, जैसा कि [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) में है, Hybrid types केवल X25519 के संयोजन में परिभाषित की जाती हैं।

एन्क्रिप्शन के प्रकार हैं:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">SSU2 Version</th>
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
</table>
### वैध संयोजन

नए एन्क्रिप्शन प्रकार RouterAddresses में दर्शाए जाते हैं। key certificate में एन्क्रिप्शन प्रकार type 4 ही रहेगा।

## विनिर्देश

### हैंडशेक पैटर्न

हैंडशेक [Noise Protocol](https://noiseprotocol.org/noise.html) हैंडशेक पैटर्न का उपयोग करते हैं।

निम्नलिखित अक्षर मैपिंग का उपयोग किया जाता है:

- e = एक-बार उपयोग होने वाली ephemeral key
- s = static key
- p = message payload
- e1 = एक-बार उपयोग होने वाली ephemeral PQ key, Alice से Bob को भेजी गई
- ekem1 = KEM ciphertext, Bob से Alice को भेजा गया

हाइब्रिड फॉरवर्ड सेक्रेसी (hfs) के लिए XK और IK में निम्नलिखित संशोधन [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) की धारा 5 में निर्दिष्ट अनुसार हैं:

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
e1 पैटर्न को निम्नानुसार परिभाषित किया गया है, जैसा कि [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) के सेक्शन 4 में निर्दिष्ट किया गया है:

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
ekem1 पैटर्न को निम्नानुसार परिभाषित किया गया है, जैसा कि [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) के सेक्शन 4 में निर्दिष्ट किया गया है:

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

हाइब्रिड हैंडशेक [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) में परिभाषित किया गया है। Alice से Bob को भेजा जाने वाला पहला संदेश, message payload से पहले e1, यानी encapsulation key को शामिल करता है। इसे एक अतिरिक्त static key के रूप में माना जाता है; Alice की ओर से इस पर `EncryptAndHash()` या Bob की ओर से `DecryptAndHash()` को कॉल करें। इसके बाद message payload को सामान्य तरीके से प्रोसेस करें।

Bob से Alice को भेजा गया दूसरा संदेश, message payload से पहले ekem1 (ciphertext) को शामिल करता है। इसे एक अतिरिक्त static key के रूप में माना जाता है; इस पर EncryptAndHash() (Bob के रूप में) या DecryptAndHash() (Alice के रूप में) को कॉल करें। इसके बाद, kem_shared_key की गणना करें और MixKey(kem_shared_key) को कॉल करें। फिर message payload को सामान्य तरीके से प्रोसेस करें।

#### परिभाषित ML-KEM संचालन

हम निम्नलिखित फ़ंक्शन परिभाषित करते हैं जो [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) में परिभाषित क्रिप्टोग्राफ़िक बिल्डिंग ब्लॉक्स के अनुरूप हैं।

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

ध्यान दें कि encap_key और ciphertext दोनों को Noise handshake संदेश 1 और 2 में ChaCha/Poly blocks के अंदर encrypt किया गया है। इन्हें handshake प्रक्रिया के भाग के रूप में decrypt किया जाएगा।

kem_shared_key को MixHash() के साथ chaining key में मिलाया जाता है। विवरण के लिए नीचे देखें।

#### संदेश 1 के लिए Alice KDF

'es' मैसेज पैटर्न के बाद और payload से पहले, निम्नलिखित जोड़ें:

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

'es' मैसेज पैटर्न के बाद और payload से पहले, निम्नलिखित जोड़ें:

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

XK के लिए: 'ee' message pattern के बाद और payload से पहले, यह जोड़ें:

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
#### Alice KDF संदेश 2 के लिए

'ee' मैसेज पैटर्न के बाद, जोड़ें:

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
#### संदेश 3 के लिए KDF

अपरिवर्तित

#### split() के लिए KDF

अपरिवर्तित

### हैंडशेक विवरण

#### Noise पहचानकर्ता

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

ध्यान दें कि MLKEM-1024 SSU2 के लिए समर्थित नहीं है, क्योंकि keys एक मानक 1500 बाइट datagram में फिट होने के लिए बहुत बड़ी हैं।

#### Long Header

लंबा हेडर 32 बाइट्स का होता है। इसका उपयोग session बनाए जाने से पहले किया जाता है, जैसे Token Request, SessionRequest, SessionCreated, और Retry के लिए। इसका उपयोग session से बाहर के Peer Test और Hole Punch संदेशों के लिए भी किया जाता है।

निम्नलिखित संदेशों में, MLKEM-512 या MLKEM-768 को इंगित करने के लिए long header में ver (version) फ़ील्ड को 3 या 4 पर सेट करें।

- (0) सत्र अनुरोध
- (1) सत्र बनाया गया
- (9) पुनः प्रयास (नोट: समाप्ति के साथ पुनः प्रयास में कोई भी संस्करण 2-4 हो सकता है)
- (10) टोकन अनुरोध

निम्नलिखित संदेश में, लंबे हेडर में ver (संस्करण) फ़ील्ड को कोई भी संस्करण 2-4 में सेट करें, क्योंकि संस्करण का चयन एलिस का है, चार्ली का नहीं। इसे हमेशा 2 पर सेट करना स्वीकार्य है। लागूकरण कोई भी मान 2-4 स्वीकार करना चाहिए।

- (11) होल पंच

निम्नलिखित संदेश में, MLKEM-512 या MLKEM-768 समर्थित होने पर भी, लंबे हेडर में ver (संस्करण) फ़ील्ड को सामान्य रूप से 2 पर सेट करें। यदि दूसरे छोर पर समर्थन है तो लागूकरण मान को 3 या 4 भी सेट कर सकते हैं, लेकिन यह आवश्यक नहीं है। लागूकरण को कोई भी मान 2-4 स्वीकार करना चाहिए।

- (7) पीयर परीक्षण (सत्र के बाहर के संदेश 5-7)

चर्चा: सभी संदेश प्रकारों के लिए संस्करण क्षेत्र को 3 या 4 पर सेट करना आवश्यक नहीं हो सकता है, लेकिन ऐसा करने से क्वांटम-उपरांत संस्करणों के लिए समर्थित नहीं इस प्रकार के कनेक्शन में जल्दी विफलता का पता लगाने में मदद मिलती है। टोकन अनुरोध और पुनः प्रयास (प्रकार 9 और 10) संगति के लिए संस्करण 3/4 होना चाहिए। साथी परीक्षण संदेश (प्रकार 7) सत्र-बाहर होता है और सत्र शुरू करने के इरादे को इंगित नहीं करता है।

हेडर एन्क्रिप्शन से पहले:

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### शॉर्ट हेडर

अपरिवर्तित

#### SessionRequest (प्रकार 0)

परिवर्तन: वर्तमान SSU2 में ChaCha सेक्शन में केवल block data होता है। ML-KEM के साथ, ChaCha सेक्शन में encrypted PQ public key भी शामिल होगी।

Spoof Protection के लिए KDF परिवर्तन: Proposal 165 [Prop165]_ में उठाए गए मुद्दों को हल करने के लिए, लेकिन एक अलग समाधान के साथ, हम Session Request के लिए KDF को संशोधित करते हैं। यह केवल PQ sessions के लिए है। Non-PQ sessions के लिए KDF अपरिवर्तित रहता है।

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
कच्ची सामग्री:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
अनएन्क्रिप्टेड डेटा (Poly1305 प्रमाणीकरण टैग नहीं दिखाया गया):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
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
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
आकार, IP ओवरहेड को छोड़कर:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
नोट: Type codes केवल आंतरिक उपयोग के लिए हैं। Routers type 4 ही रहेंगे, और समर्थन router addresses में इंगित किया जाएगा।

MLKEM768_X25519 के लिए न्यूनतम MTU: IPv4 के लिए 1318 और IPv6 के लिए 1338। नीचे देखें।

अधिकतम आकार: उसके राउटरइन्फो में प्रकाशित बॉब के एमटीयू का उपयोग करें, या यदि राउटरइन्फो में नहीं है तो डिफ़ॉल्ट 1500 का उपयोग करें। यदि प्रकाशित एमटीयू बहुत कम है तो एमएलकेईएम768_एक्स25519 का उपयोग न करें।

#### SessionCreated (प्रकार 1)

परिवर्तन: वर्तमान SSU2 में केवल एकल ChaCha अनुभाग में पेलोड होता है। ML-KEM के साथ, पेलोड से पहले एक नया ChaCha अनुभाग होगा, जिसमें एन्क्रिप्टेड PQ साइफरटेक्स्ट होगा।

कच्ची सामग्री:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
अनएन्क्रिप्टेड डेटा (Poly1305 auth tag नहीं दिखाया गया):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
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
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
आकार, IP ओवरहेड को छोड़कर:

| प्रकार | प्रकार कोड | Y लंबाई | Msg 2 लंबाई | Msg 2 Enc लंबाई | Msg 2 Dec लंबाई | PQ CT लंबाई | pl लंबाई |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | लागू नहीं | बहुत बड़ा | | | | |
नोट: Type codes केवल आंतरिक उपयोग के लिए हैं। Routers type 4 ही रहेंगे, और समर्थन router addresses में इंगित किया जाएगा।

MLKEM768_X25519 के लिए न्यूनतम MTU: IPv4 के लिए 1318 और IPv6 के लिए 1338। नीचे देखें।

अधिकतम आकार: एलिस के पास अभी तक बॉब का राउटरइन्फो नहीं है और उसे उसका प्रकाशित MTU नहीं पता है। इस संदेश के लिए निम्नलिखित अस्थायी MTU का उपयोग करें। MLKEM512_X25519 के लिए, 1280 या प्राप्त सत्र अनुरोध आकार में से अधिकतम को MTU के रूप में उपयोग करें। MLKEM768_X25519 के लिए, (IPv4 के लिए 1318 या IPv6 के लिए 1338) या प्राप्त सत्र अनुरोध आकार में से अधिकतम को MTU के रूप में उपयोग करें। सत्र अनुरोध की तुलना में सत्र निर्मित का ओवरहेड छोटा होता है, क्योंकि MLKEM साइफरटेक्स्ट MLKEM सार्वजनिक कुंजी से छोटी होती है। इससे सत्र निर्मित में भराव के आकार की एक श्रृंखला की अनुमति मिलती है, भले ही सत्र अनुरोध में थोड़ा या कोई भराव न हो।

#### SessionConfirmed (टाइप 2)

अपरिवर्तित

#### डेटा चरण के लिए KDF

अपरिवर्तित

#### Relay और Peer Test

निम्नलिखित ब्लॉक में version फ़ील्ड हैं। ये version 2 पर ही रहेंगे (non-PQ Bob के साथ compatibility बनाए रखने के लिए), और PQ के लिए version 3/4 में नहीं बदलेंगे।

- रिले अनुरोध
- रिले प्रतिक्रिया
- रिले परिचय
- पीयर परीक्षण

#### प्रकाशित पते

सभी मामलों में, SSU2 transport का नाम सामान्य रूप से उपयोग करें। MLKEM-1024 समर्थित नहीं है।

non-PQ, non-firewalled के समान address/port का उपयोग करें। एक या दोनों PQ variants समर्थित हैं। router address में, v=2 (सामान्य की तरह) और नया parameter pq=[3|4|3,4|4,3] प्रकाशित करें जो MLKEM 512/768/दोनों को इंगित करता है। जिन routers का MTU नीचे निर्दिष्ट न्यूनतम से कम है, उन्हें "4" युक्त "pq" parameter प्रकाशित नहीं करना चाहिए। MLKEM-768 की प्राथमिकता दर्शाने के लिए 4,3 और MLKEM-512 की प्राथमिकता दर्शाने के लिए 3,4 प्रकाशित करें। वास्तविक version initiator (कनेक्शन शुरू करने वाला) पर निर्भर है, और प्राथमिकता का पालन नहीं भी किया जा सकता है। जिन routers का MTU नीचे निर्दिष्ट न्यूनतम से कम है, उन्हें MLKEM768 का उपयोग करके कनेक्ट नहीं करना चाहिए। पुराने routers pq parameter को अनदेखा करेंगे और सामान्य की तरह non-pq के रूप में कनेक्ट होंगे।

अलग address/port का non-PQ की तरह उपयोग, या PQ-only, non-firewalled समर्थित नहीं है। इसे तब तक लागू नहीं किया जाएगा जब तक non-PQ SSU2 को अक्षम नहीं किया जाता, जो अभी से कई वर्ष दूर है। जब non-PQ अक्षम हो जाएगा, तब एक या दोनों PQ variants समर्थित होंगे। Router address में, MLKEM 512/768/दोनों को इंगित करने के लिए v=[3|4|3,4|4,3] प्रकाशित करें। पुराने routers v parameter की जांच करेंगे और इस address को असमर्थित मानकर छोड़ देंगे।

Firewalled पते (कोई IP प्रकाशित नहीं): router address में, v=2 प्रकाशित करें (सामान्य रूप से)। relay को सपोर्ट करने के लिए, firewalled पतों में pq parameter अवश्य प्रकाशित किया जाना चाहिए।

Alice किसी PQ Bob से जुड़ने के लिए उस PQ variant का उपयोग कर सकती है जिसे Bob प्रकाशित करता है, चाहे Alice अपनी router info में pq support का विज्ञापन करे या न करे, या चाहे वह समान variant का विज्ञापन करे या न करे।

#### MTU

MLKEM768 के साथ MTU (Maximum Transmission Unit) से अधिक न होने का ध्यान रखें। IPv4 के लिए MLKEM768_X25519 का न्यूनतम MTU 1318 है और IPv6 के लिए 1338 है (यह मानते हुए कि DateTime और Padding या RelayTagRequest block के साथ न्यूनतम payload 10 bytes है)। SSU2 के लिए सामान्यतः न्यूनतम MTU 1280 है, इसलिए सभी peers MLKEM768 का उपयोग नहीं कर सकते। यदि वास्तविक MTU न्यूनतम से कम है — चाहे स्थानीय रूप से हो या peer द्वारा advertised हो — तो MLKEM768 को publish या उपयोग न करें। इस बात का ध्यान रखें कि padding का आकार इतना न हो कि message 1 या 2 स्थानीय या remote MTU से अधिक हो जाए।

## ओवरहेड विश्लेषण

### Key Exchange

आकार वृद्धि (बाइट्स):

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
</table>
## सुरक्षा विश्लेषण

NIST सुरक्षा श्रेणियों का सारांश [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) के स्लाइड 10 में दिया गया है। प्रारंभिक मानदंड: hybrid protocols के लिए हमारी न्यूनतम NIST सुरक्षा श्रेणी 2 और PQ-only के लिए 3 होनी चाहिए।

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

ये सभी हाइब्रिड प्रोटोकॉल हैं। कार्यान्वयन को MLKEM768 को प्राथमिकता देनी चाहिए; MLKEM512 पर्याप्त रूप से सुरक्षित नहीं है।

NIST सुरक्षा श्रेणियाँ [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

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
</table>
## कार्यान्वयन नोट्स

### लाइब्रेरी समर्थन

Bouncycastle, BoringSSL, और WolfSSL लाइब्रेरी अब MLKEM और MLDSA को सपोर्ट करती हैं। OpenSSL का सपोर्ट उनके 3.5 रिलीज़ में 8 अप्रैल, 2025 को आएगा [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)।

### इनबाउंड ट्रैफ़िक पहचान

हम session request में ephemeral key का MSB (key[31] & 0x80) सेट करते हैं ताकि यह इंगित किया जा सके कि यह एक hybrid connection है। इससे हम एक ही port पर standard NTCP और hybrid NTCP दोनों चला सकते हैं। inbound के लिए केवल एक hybrid variant समर्थित है, और इसे router address में advertise किया जाता है। उदाहरण के लिए, pq=3 या pq=4।

## Router संगतता

### Transport Names

Alice के रूप में, एक PQ कनेक्शन के लिए, obfuscation से पहले, X[31] |= 0x80 सेट करें। इससे X एक अमान्य X25519 public key बन जाती है। Obfuscation के बाद, AES-CBC इसे randomize कर देगा। Obfuscation के बाद X का MSB (Most Significant Bit) random होगा।

## संदर्भ

* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
