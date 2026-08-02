---
title: "NTCP2 Transport"
description: "router-to-router लिंक्स के लिए Noise-आधारित TCP परिवहन"
slug: "ntcp2"
category: "ट्रांसपोर्ट्स"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

## अवलोकन

NTCP2 एक प्रमाणित key agreement protocol है जो [NTCP](/docs/transport/ntcp) के विभिन्न प्रकार की स्वचालित पहचान और हमलों के प्रतिरोध को बेहतर बनाता है।

NTCP2 को लचीलेपन और NTCP के साथ सह-अस्तित्व के लिए डिज़ाइन किया गया है। इसे NTCP के समान पोर्ट पर, या अलग पोर्ट पर, या बिना एक साथ NTCP समर्थन के समर्थित किया जा सकता है। विवरण के लिए नीचे Published Router Info अनुभाग देखें।

अन्य I2P transports की तरह, NTCP2 केवल I2NP संदेशों के point-to-point (router-to-router) transport के लिए परिभाषित है। यह एक सामान्य उद्देश्य डेटा पाइप नहीं है।

NTCP2 संस्करण 0.9.36 से समर्थित है। मूल प्रस्ताव के लिए [Prop111](/proposals/111-ntcp-2) देखें, जिसमें पृष्ठभूमि चर्चा और अतिरिक्त जानकारी शामिल है।

## Noise Protocol Framework

NTCP2 Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revision 33, 2017-10-04) का उपयोग करता है। Noise के गुण Station-To-Station protocol [STS](#references) के समान हैं, जो [SSU](/docs/transport/ssu) protocol का आधार है। Noise की भाषा में, Alice initiator है, और Bob responder है।

NTCP2, Noise प्रोटोकॉल Noise_XK_25519_ChaChaPoly_SHA256 पर आधारित है। (प्रारंभिक key derivation function के लिए वास्तविक पहचानकर्ता "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256" है जो I2P एक्सटेंशन को दर्शाता है - नीचे KDF 1 सेक्शन देखें) यह Noise प्रोटोकॉल निम्नलिखित primitives का उपयोग करता है:

- Handshake Pattern: XK Alice अपनी key Bob को भेजती है (X) Alice को Bob की static key पहले से ही पता है (K)
- DH Function: X25519 X25519 DH जिसमें 32 bytes की key length है जैसा कि [RFC-7748](https://tools.ietf.org/html/rfc7748) में निर्दिष्ट है।
- Cipher Function: ChaChaPoly AEAD_CHACHA20_POLY1305 जैसा कि [RFC-7539](https://tools.ietf.org/html/rfc7539) section 2.8 में निर्दिष्ट है। 12 byte nonce, जिसके पहले 4 bytes zero पर सेट हैं।
- Hash Function: SHA256 मानक 32-byte hash, जो I2P में पहले से ही व्यापक रूप से उपयोग में है।

## फ्रेमवर्क में अतिरिक्त सुविधाएं

NTCP2 निम्नलिखित सुधारों को Noise_XK_25519_ChaChaPoly_SHA256 के लिए परिभाषित करता है। ये आम तौर पर [NOISE](https://noiseprotocol.org/noise.html) अनुभाग 13 में दिए गए दिशा-निर्देशों का पालन करते हैं।

1) Cleartext ephemeral keys को एक ज्ञात key और IV का उपयोग करके AES encryption के साथ obfuscate किया जाता है। 2) संदेश 1 और 2 में random cleartext padding जोड़ा जाता है। Cleartext padding को handshake hash (MixHash) गणना में शामिल किया जाता है। संदेश 2 और संदेश 3 भाग 1 के लिए नीचे KDF sections देखें। संदेश 3 और data phase संदेशों में random AEAD padding जोड़ा जाता है। 3) दो-byte frame length field जोड़ा जाता है, जैसा कि TCP पर Noise के लिए आवश्यक है, और obfs4 की तरह। इसका उपयोग केवल data phase संदेशों में किया जाता है। संदेश 1 और 2 AEAD frames fixed length के हैं। संदेश 3 भाग 1 AEAD frame fixed length का है। संदेश 3 भाग 2 AEAD frame length संदेश 1 में निर्दिष्ट किया गया है। 4) दो-byte frame length field को SipHash-2-4 के साथ obfuscate किया जाता है, obfs4 की तरह। 5) संदेश 1,2,3, और data phase के लिए payload format परिभाषित किया गया है। निश्चित रूप से, ये framework में परिभाषित नहीं हैं।

## संदेश

सभी NTCP2 संदेश 65537 बाइट्स या उससे कम लंबाई के होते हैं। संदेश प्रारूप Noise संदेशों पर आधारित है, जिसमें फ्रेमिंग और अविभेद्यता के लिए संशोधन किए गए हैं। मानक Noise लाइब्रेरी का उपयोग करने वाले implementation को प्राप्त संदेशों को Noise संदेश प्रारूप से/में पूर्व-प्रसंस्कृत करने की आवश्यकता हो सकती है। सभी एन्क्रिप्टेड फ़ील्ड AEAD ciphertexts हैं।

स्थापना अनुक्रम निम्नलिखित है:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Noise terminology का उपयोग करते हुए, establishment और data sequence निम्नलिखित है: (Payload Security Properties [Noise](https://noiseprotocol.org/noise.html) से)

```
XK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
एक बार session स्थापित हो जाने के बाद, Alice और Bob Data messages का आदान-प्रदान कर सकते हैं।

सभी संदेश प्रकार (SessionRequest, SessionCreated, SessionConfirmed, Data और TimeSync) इस अनुभाग में निर्दिष्ट हैं।

कुछ संकेतन:

    - RH_A = Router Hash for Alice (32 bytes)
    - RH_B = Router Hash for Bob (32 bytes)

### प्रमाणित एन्क्रिप्शन

तीन अलग प्रमाणित एन्क्रिप्शन इंस्टेंसेज (CipherStates) हैं। एक handshake चरण के दौरान, और दो (transmit और receive) डेटा चरण के लिए। प्रत्येक का KDF से अपना key है।

एन्क्रिप्टेड/प्रमाणीकृत डेटा को इस रूप में दर्शाया जाएगा

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Encrypted and authenticated data    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### ChaCha20/Poly1305

एन्क्रिप्टेड और प्रमाणीकृत डेटा प्रारूप।

एन्क्रिप्शन/डिक्रिप्शन फ़ंक्शन्स के लिए इनपुट्स:

```
k :: 32 byte cipher key, as generated from KDF

nonce :: Counter-based nonce, 12 bytes.
         Starts at 0 and incremented for each message.
         First four bytes are always zero.
         Last eight bytes are the counter, little-endian encoded.
         Maximum value is 2**64 - 2.
         Connection must be dropped and restarted after
         it reaches that value.
         The value 2**64 - 1 must never be sent.

ad :: In handshake phase:
      Associated data, 32 bytes.
      The SHA256 hash of all preceding data.
      In data phase:
      Zero bytes

data :: Plaintext data, 0 or more bytes
```
एन्क्रिप्शन फ़ंक्शन का आउटपुट, डिक्रिप्शन फ़ंक्शन का इनपुट:

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+                             +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Obfs Len :: Length of (encrypted data + MAC) to follow, 16 - 65535
            Obfuscation using SipHash (see below)
            Not used in message 1 or 2, or message 3 part 1, where the length is fixed
            Not used in message 3 part 1, as the length is specified in message 1

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
ChaCha20 के लिए, यहाँ जो वर्णित है वह [RFC-7539](https://tools.ietf.org/html/rfc7539) के अनुरूप है, जो TLS [RFC-7905](https://tools.ietf.org/html/rfc7905) में भी समान रूप से उपयोग किया जाता है।

#### नोट्स

- चूंकि ChaCha20 एक stream cipher है, plaintexts को padded करने की आवश्यकता नहीं है। अतिरिक्त keystream bytes को छोड़ दिया जाता है।
- cipher के लिए key (256 bits) SHA256 KDF के माध्यम से सहमत की जाती है। प्रत्येक message के लिए KDF का विवरण नीचे अलग sections में है।
- messages 1, 2, और message 3 के पहले भाग के लिए ChaChaPoly frames ज्ञात आकार के हैं। message 3 के दूसरे भाग से शुरू करके, frames परिवर्तनीय आकार के हैं। message 3 part 1 का आकार message 1 में निर्दिष्ट किया गया है। data phase से शुरू करके, frames को obfs4 की तरह SipHash के साथ obfuscated दो-byte length के साथ prepended किया जाता है।
- Padding, messages 1 और 2 के लिए authenticated data frame के बाहर है। Padding को अगले message के लिए KDF में उपयोग किया जाता है ताकि tampering का पता चल जाए। message 3 से शुरू करके, padding authenticated data frame के अंदर है।

#### AEAD त्रुटि हैंडलिंग

- संदेश 1, 2, और संदेश 3 के भाग 1 और 2 में, AEAD संदेश का आकार पहले से ज्ञात होता है। AEAD प्रमाणीकरण विफलता पर, प्राप्तकर्ता को आगे की संदेश प्रसंस्करण रोकनी चाहिए और बिना प्रतिक्रिया दिए कनेक्शन बंद कर देना चाहिए। यह एक असामान्य बंद होना चाहिए (TCP RST)।
- probing प्रतिरोध के लिए, संदेश 1 में, AEAD विफलता के बाद, Bob को एक यादृच्छिक timeout (सीमा TBD) सेट करना चाहिए और फिर socket बंद करने से पहले यादृच्छिक संख्या में bytes (सीमा TBD) पढ़ना चाहिए। Bob को बार-बार विफलताओं वाले IPs की blacklist बनाए रखनी चाहिए।
- डेटा चरण में, AEAD संदेश का आकार SipHash के साथ "encrypted" (अस्पष्ट) होता है। decryption oracle बनाने से बचने के लिए सावधानी बरतनी चाहिए। डेटा चरण AEAD प्रमाणीकरण विफलता पर, प्राप्तकर्ता को एक यादृच्छिक timeout (सीमा TBD) सेट करना चाहिए और फिर यादृच्छिक संख्या में bytes (सीमा TBD) पढ़ना चाहिए। पढ़ने के बाद, या read timeout पर, प्राप्तकर्ता को "AEAD failure" reason code युक्त termination block के साथ payload भेजना चाहिए, और कनेक्शन बंद कर देना चाहिए।
- डेटा चरण में invalid length field value के लिए भी समान error action लें।

### Key Derivation Function (KDF) (हैंडशेक संदेश 1 के लिए)

KDF handshake phase cipher key k को DH result से generate करता है, HMAC-SHA256(key, data) का उपयोग करके जैसा कि [RFC-2104](https://tools.ietf.org/html/rfc2104) में परिभाषित है। ये InitializeSymmetric(), MixHash(), और MixKey() functions हैं, बिल्कुल वैसे ही जैसे Noise spec में परिभाषित है।

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
 (48 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set ck = h

Define rs = Bob's 32-byte static key as published in the RouterInfo

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections

// Alice must validate that Bob's static key is a valid point on the curve here.

// Bob static key
// MixHash(rs)
// || below means append
h = SHA256(h || rs);

// up until here, can all be precalculated by Bob for all incoming connections

This is the "e" message pattern:

Alice generates her ephemeral DH key pair e.

// Alice ephemeral key X
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 1
// Retain the Hash h for the message 2 KDF


End of "e" message pattern.

This is the "es" message pattern:

// DH(e, rs) == DH(s, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's static key
Set input_key_material = X25519 DH result

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, defined above
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 2 KDF


End of "es" message pattern.
```
### 1) SessionRequest

Alice Bob को भेजती है।

Noise सामग्री: Alice की ephemeral key X Noise payload: 16 byte विकल्प ब्लॉक Non-noise payload: यादृच्छिक padding

(पेलोड सिक्योरिटी प्रॉपर्टीज [Noise](https://noiseprotocol.org/noise.html) से)

```
XK(s, rs):           Authentication   Confidentiality
  -> e, es                  0                2

  Authentication: None (0).
  This payload may have been sent by any party, including an active attacker.

  Confidentiality: 2.
  Encryption to a known recipient, forward secrecy for sender compromise
  only, vulnerable to replay.  This payload is encrypted based only on DHs
  involving the recipient's static key pair.  If the recipient's static
  private key is compromised, even at a later date, this payload can be
  decrypted.  This message can also be replayed, since there's no ephemeral
  contribution from the recipient.

  "e": Alice generates a new ephemeral key pair and stores it in the e
       variable, writes the ephemeral public key as cleartext into the
       message buffer, and hashes the public key along with the old h to
       derive a new h.

  "es": A DH is performed between the Alice's ephemeral key pair and the
        Bob's static key pair.  The result is hashed along with the old ck to
        derive a new ck and k, and n is set to zero.
```
X मान को एन्क्रिप्ट किया जाता है ताकि payload की अविभेद्यता और विशिष्टता सुनिश्चित हो सके, जो आवश्यक DPI प्रतिरोधी उपाय हैं। हम इसे प्राप्त करने के लिए AES एन्क्रिप्शन का उपयोग करते हैं, elligator2 जैसे अधिक जटिल और धीमे विकल्पों के बजाय। Bob के router public key के साथ asymmetric एन्क्रिप्शन बहुत धीमा होगा। AES एन्क्रिप्शन Bob के router hash को key के रूप में और Bob के IV को network database में प्रकाशित के अनुसार उपयोग करता है।

AES एन्क्रिप्शन केवल DPI प्रतिरोध के लिए है। कोई भी पक्ष जो Bob के router hash और IV को जानता है, जो network database में प्रकाशित होते हैं, इस संदेश में X मान को decrypt कर सकता है।

पैडिंग Alice द्वारा एन्क्रिप्ट नहीं की जाती है। Bob के लिए पैडिंग को डिक्रिप्ट करना आवश्यक हो सकता है, timing attacks को रोकने के लिए।

कच्ची सामग्री:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted X         |
+             (32 bytes)                +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data           |
+             (16 bytes)                +
|   k defined in KDF for message 1      |
+   n = 0                               +
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

X :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: As published in Bobs network database entry

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as NTCP
           (see Version Detection section below).
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
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

X :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as "NTCP"
           (see Version Detection section below)
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Options block: नोट: सभी फ़ील्ड big-endian हैं।

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id :: 1 byte, the network ID (currently 2, except for test networks)
      As of 0.9.42. See proposal 147.

ver :: 1 byte, protocol version (currently 2)

padLen :: 2 bytes, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

m3p2Len :: 2 bytes, length of the the second AEAD frame in SessionConfirmed
           (message 3 part 2) See notes below

Rsvd :: 2 bytes, set to 0 for compatibility with future options

tsA :: 4 bytes, Unix timestamp, unsigned seconds.
       Wraps around in 2106

Reserved :: 4 bytes, set to 0 for compatibility with future options
```
#### टिप्पणियां

- जब प्रकाशित पता "NTCP" है, तो Bob एक ही port पर NTCP और NTCP2 दोनों का समर्थन करता है। संगतता के लिए, "NTCP" के रूप में प्रकाशित पते पर कनेक्शन शुरू करते समय, Alice को padding सहित इस संदेश का अधिकतम आकार 287 bytes या उससे कम तक सीमित करना चाहिए। यह Bob द्वारा स्वचालित प्रोटोकॉल पहचान की सुविधा प्रदान करता है। "NTCP2" के रूप में प्रकाशित होने पर, कोई आकार प्रतिबंध नहीं है। नीचे Published Addresses और Version Detection अनुभागों को देखें।

- प्रारंभिक AES block में अद्वितीय X मान यह सुनिश्चित करता है कि ciphertext हर session के लिए अलग हो।

- Bob को उन connections को reject करना चाहिए जहाँ timestamp value वर्तमान समय से बहुत अधिक अलग है। अधिकतम delta time को "D" कहते हैं। Bob को पहले इस्तेमाल हुए handshake values का एक local cache बनाए रखना चाहिए और replay attacks को रोकने के लिए duplicates को reject करना चाहिए। Cache में values का lifetime कम से कम 2*D होना चाहिए। Cache values implementation-dependent हैं, हालांकि 32-byte X value (या इसका encrypted equivalent) का उपयोग किया जा सकता है।

- Diffie-Hellman ephemeral keys का कभी भी पुन: उपयोग नहीं किया जा सकता, क्रिप्टोग्राफिक हमलों को रोकने के लिए, और पुन: उपयोग को replay attack के रूप में खारिज कर दिया जाएगा।

- "KE" और "auth" विकल्प संगत होने चाहिए, अर्थात् साझा गुप्त K उपयुक्त आकार का होना चाहिए। यदि अधिक "auth" विकल्प जोड़े जाते हैं, तो यह "KE" फ्लैग के अर्थ को अंतर्निहित रूप से बदल सकता है ताकि एक अलग KDF या एक अलग truncation आकार का उपयोग किया जा सके।

- Bob को यहाँ यह validate करना होगा कि Alice की ephemeral key curve पर एक valid point है।

- Padding को एक उचित मात्रा तक सीमित होना चाहिए। Bob अत्यधिक padding वाले connections को अस्वीकार कर सकता है। Bob अपने padding options को message 2 में निर्दिष्ट करेगा। Min/max दिशानिर्देश TBD। न्यूनतम 0 से 31 bytes तक का random size? (Distribution implementation-dependent है) Java implementations वर्तमान में padding को अधिकतम 256 bytes तक सीमित करते हैं।

- किसी भी त्रुटि पर, जिसमें AEAD, DH, timestamp, स्पष्ट replay, या key validation विफलता शामिल है, Bob को आगे की message processing रोकनी चाहिए और बिना जवाब दिए connection बंद कर देना चाहिए। यह एक असामान्य बंद होना चाहिए (TCP RST)। probing प्रतिरोध के लिए, AEAD विफलता के बाद, Bob को एक random timeout (सीमा TBD) सेट करना चाहिए और फिर socket बंद करने से पहले random संख्या में bytes (सीमा TBD) पढ़ना चाहिए।

- Bob decryption का प्रयास करने से पहले valid key के लिए एक fast MSB check कर सकता है (X[31] & 0x80 == 0)। यदि high bit set है, तो AEAD failures की तरह probing resistance implement करें।

- DoS शमन: DH एक अपेक्षाकृत महंगा ऑपरेशन है। पिछले NTCP प्रोटोकॉल की तरह, router को CPU या कनेक्शन थकावट को रोकने के लिए सभी आवश्यक उपाय करने चाहिए। अधिकतम सक्रिय कनेक्शन और प्रगति में अधिकतम कनेक्शन सेटअप पर सीमा लगाएं। रीड टाइमआउट लागू करें (प्रति-रीड और "slowloris" के लिए कुल दोनों)। समान स्रोत से बार-बार या एक साथ कनेक्शन को सीमित करें। बार-बार असफल होने वाले स्रोतों के लिए ब्लैकलिस्ट बनाए रखें। AEAD विफलता का जवाब न दें।

- तेज़ version detection और handshaking को सुविधाजनक बनाने के लिए, implementations को यह सुनिश्चित करना चाहिए कि Alice पहले message की पूरी contents को buffer करे और फिर padding सहित एक साथ flush करे। इससे इस बात की संभावना बढ़ जाती है कि data एक single TCP packet में contained होगा (जब तक कि OS या middleboxes द्वारा segmented न हो), और Bob द्वारा एक साथ receive किया जाएगा। इसके अतिरिक्त, implementations को यह सुनिश्चित करना चाहिए कि Bob दूसरे message की पूरी contents को buffer करे और फिर padding सहित एक साथ flush करे। और यह कि Bob तीसरे message की पूरी contents को buffer करे और फिर एक साथ flush करे। यह भी efficiency के लिए है और random padding की effectiveness को सुनिश्चित करने के लिए है।

- "ver" फ़ील्ड: संपूर्ण Noise protocol, extensions, और NTCP protocol जिसमें payload specifications शामिल हैं, जो NTCP2 को दर्शाता है। इस फ़ील्ड का उपयोग भविष्य के परिवर्तनों के लिए समर्थन दर्शाने हेतु किया जा सकता है।

- Message 3 part 2 length: यह दूसरे AEAD frame का आकार है (16-byte MAC सहित) जिसमें Alice की Router Info और वैकल्पिक padding होती है जो SessionConfirmed message में भेजी जाएगी। चूंकि router समय-समय पर अपनी Router Info को पुनः जेनरेट और पुनः प्रकाशित करते हैं, इसलिए वर्तमान Router Info का आकार message 3 भेजे जाने से पहले बदल सकता है। इम्प्लीमेंटेशन को दो रणनीतियों में से एक चुनना होगा:

a\) संदेश 3 में भेजे जाने वाले वर्तमान Router Info को सेव करें, ताकि साइज़ पता हो, और वैकल्पिक रूप से padding के लिए जगह जोड़ें;

b\) निर्दिष्ट आकार को पर्याप्त रूप से बढ़ाएं ताकि Router Info आकार में संभावित वृद्धि की अनुमति हो सके, और जब message 3 वास्तव में भेजा जाता है तो हमेशा padding जोड़ें। दोनों में से किसी भी स्थिति में, message 1 में शामिल "m3p2len" लंबाई उस frame के आकार के बिल्कुल बराबर होनी चाहिए जब वह message 3 में भेजा जाता है।

- यदि message 1 को validate करने और padding को पढ़ने के बाद कोई incoming data शेष रहता है तो Bob को connection को fail करना चाहिए। Alice से कोई extra data नहीं होना चाहिए, क्योंकि Bob ने अभी तक message 2 के साथ respond नहीं किया है।

- नेटवर्क ID फील्ड का उपयोग क्रॉस-नेटवर्क कनेक्शन को तुरंत पहचानने के लिए किया जाता है। यदि यह फील्ड शून्य नहीं है, और Bob के नेटवर्क ID से मेल नहीं खाता, तो Bob को कनेक्शन बंद करना चाहिए और भविष्य के कनेक्शन को ब्लॉक करना चाहिए। टेस्ट नेटवर्क से कोई भी कनेक्शन में एक अलग ID होना चाहिए और टेस्ट में असफल हो जाएगा। 0.9.42 के अनुसार। अधिक जानकारी के लिए प्रस्ताव 147 देखें।

- API 0.9.68 (रिलीज 2.11.0) तक, Java I2P ने non-PQ कनेक्शन के लिए अधिकतम 256 बाइट्स पैडिंग को लागू किया था, हालांकि यह पहले दस्तावेजित नहीं था।
  API 0.9.69 (रिलीज 2.12.0) से, Java I2P non-PQ कनेक्शन के लिए वही अधिकतम पैडिंग लागू करता है जो MLKEM-512 के लिए है। अधिकतम पैडिंग 880 बाइट्स है।

### Key Derivation Function (KDF) (handshake message 2 और message 3 part 1 के लिए)

```
// take h saved from message 1 KDF
// MixHash(ciphertext)
h = SHA256(h || 32 byte encrypted payload from message 1)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 1)

This is the "e" message pattern:

Bob generates his ephemeral DH key pair e.

// h is from KDF for handshake message 1
// Bob ephemeral key Y
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 2
// Retain the Hash h for the message 3 KDF

End of "e" message pattern.

This is the "ee" message pattern:

// DH(e, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Alice's ephemeral key in memory, no longer needed
// Alice:
e(public and private) = (all zeros)
// Bob:
re = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 3 KDF

End of "ee" message pattern.
```
### 2) SessionCreated

Bob, Alice को भेजता है।

Noise सामग्री: Bob की ephemeral key Y Noise payload: 16 byte विकल्प ब्लॉक Non-noise payload: यादृच्छिक padding

(Payload Security Properties [Noise](https://noiseprotocol.org/noise.html) से)

```
XK(s, rs):           Authentication   Confidentiality
  <- e, ee                  2                1

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 1.
  Encryption to an ephemeral recipient.
  This payload has forward secrecy, since encryption involves an ephemeral-ephemeral DH ("ee").
  However, the sender has not authenticated the recipient,
  so this payload might be sent to any party, including an active attacker.


  "e": Bob generates a new ephemeral key pair and stores it in the e variable,
  writes the ephemeral public key as cleartext into the message buffer,
  and hashes the public key along with the old h to derive a new h.

  "ee": A DH is performed between the Bob's ephemeral key pair and the Alice's ephemeral key pair.
  The result is hashed along with the old ck to derive a new ck and k, and n is set to zero.
```
Y मान को पेलोड की अपरिचयता और विशिष्टता सुनिश्चित करने के लिए एन्क्रिप्ट किया जाता है, जो आवश्यक DPI प्रतिकारी उपाय हैं। हम इसे प्राप्त करने के लिए AES एन्क्रिप्शन का उपयोग करते हैं, न कि अधिक जटिल और धीमे विकल्पों जैसे elligator2 का। Alice के router पब्लिक की के लिए असमान्य एन्क्रिप्शन बहुत धीमा होगा। AES एन्क्रिप्शन Bob के router hash को की के रूप में उपयोग करता है और संदेश 1 से AES स्थिति का (जो Bob के IV के साथ प्रारंभ की गई थी जैसा कि netDb में प्रकाशित है)।

AES एन्क्रिप्शन केवल DPI प्रतिरोध के लिए है। कोई भी पक्ष जो Bob के router hash और IV को जानता है, जो network database में प्रकाशित हैं, और message 1 के पहले 32 बाइट्स को कैप्चर करता है, वह इस message में Y मान को डिक्रिप्ट कर सकता है।

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
|   ChaChaPoly encrypted data (options) |
+   16 bytes                            +
|   k defined in KDF for message 2      |
+   n = 0; see KDF for associated data  +
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

Y :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: Using AES state from message 1
```
अनएन्क्रिप्टेड डेटा (Poly1305 auth tag नहीं दिखाया गया):

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

Y :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Alice and Bob will use the padding data in the KDF for message 3 part 1.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
#### नोट्स

- Alice को यह सत्यापित करना चाहिए कि Bob की ephemeral key curve पर एक वैध बिंदु है।
- Padding को उचित मात्रा तक सीमित होना चाहिए। Alice अत्यधिक padding वाले कनेक्शन को अस्वीकार कर सकती है। Alice अपने padding विकल्पों को message 3 में निर्दिष्ट करेगी। न्यूनतम/अधिकतम दिशानिर्देश अभी तय किए जाने हैं। न्यूनतम 0 से 31 bytes तक का random size? (वितरण implementation-dependent है)
- किसी भी त्रुटि पर, जिसमें AEAD, DH, timestamp, स्पष्ट replay, या key validation failure शामिल है, Alice को आगे की message processing रोकनी चाहिए और बिना जवाब दिए कनेक्शन बंद करना चाहिए। यह असामान्य बंदी (TCP RST) होनी चाहिए।
- तीव्र handshaking को सुविधाजनक बनाने के लिए, implementations को यह सुनिश्चित करना चाहिए कि Bob पहले message की संपूर्ण सामग्री को padding सहित buffer करे और फिर एक साथ flush करे। इससे इस बात की संभावना बढ़ जाती है कि डेटा एक single TCP packet में समाया जाए (जब तक कि OS या middleboxes द्वारा विभाजित न किया जाए), और Alice द्वारा एक साथ प्राप्त किया जाए। यह दक्षता के लिए भी है और random padding की प्रभावशीलता सुनिश्चित करने के लिए भी है।
- Alice को कनेक्शन fail करना चाहिए यदि message 2 को सत्यापित करने और padding को पढ़ने के बाद कोई incoming data शेष रह जाता है। Bob से कोई अतिरिक्त डेटा नहीं होना चाहिए, क्योंकि Alice ने अभी तक message 3 के साथ जवाब नहीं दिया है।

विकल्प ब्लॉक: नोट: सभी फ़ील्ड big-endian हैं।

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Reserved :: 10 bytes total, set to 0 for compatibility with future options

padLen :: 2 bytes, big endian, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

tsB :: 4 bytes, big endian, Unix timestamp, unsigned seconds.
       Wraps around in 2106
```
#### टिप्पणियाँ

- Alice को उन connections को reject करना चाहिए जहाँ timestamp value वर्तमान समय से बहुत अधिक भिन्न है। अधिकतम delta time को "D" कहते हैं। Alice को पहले से उपयोग किए गए handshake values का एक local cache बनाए रखना चाहिए और duplicates को reject करना चाहिए, replay attacks को रोकने के लिए। Cache में values का lifetime कम से कम 2*D होना चाहिए। Cache values implementation-dependent हैं, हालांकि 32-byte Y value (या इसका encrypted equivalent) का उपयोग किया जा सकता है।

- API 0.9.68 (रिलीज 2.11.0) तक, Java I2P ने non-PQ connections के लिए अधिकतम 256 bytes padding को लागू किया था, हालांकि यह पहले से documented नहीं था।
  API 0.9.69 (रिलीज 2.12.0) से, Java I2P non-PQ connections के लिए वही अधिकतम padding लागू करता है जो MLKEM-512 के लिए है। अधिकतम padding 848 bytes है।

#### समस्याएं

- यहाँ min/max padding विकल्प शामिल करें?

### handshake संदेश 3 भाग 1 के लिए एन्क्रिप्शन, संदेश 2 KDF का उपयोग करके)

```
// take h saved from message 2 KDF
// MixHash(ciphertext)
h = SHA256(h || 24 byte encrypted payload from message 2)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 2)
// h is used as the associated data for the AEAD in message 3 part 1, below

This is the "s" message pattern:

Define s = Alice's static public key, 32 bytes

// EncryptAndHash(s.publickey)
// EncryptWithAd(h, s.publickey)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// k is from handshake message 1
// n is 1
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, s.publickey)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// h is used as the associated data for the AEAD in message 3 part 2

End of "s" message pattern.
```
### Key Derivation Function (KDF) (handshake message 3 part 2 के लिए)

```
This is the "se" message pattern:

// DH(s, re) == DH(e, rs)
Define input_key_material = 32 byte DH result of Alice's static key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Bob's ephemeral key in memory, no longer needed
// Alice:
re = (all zeros)
// Bob:
e(public and private) = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).

// h from message 3 part 1 is used as the associated data for the AEAD in message 3 part 2

// EncryptAndHash(payload)
// EncryptWithAd(h, payload)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// n is 0
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, payload)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// retain the chaining key ck for the data phase KDF
// retain the hash h for the data phase Additional Symmetric Key (SipHash) KDF

End of "se" message pattern.

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 3) SessionConfirmed

Alice, Bob को भेजती है।

Noise content: Alice की static key Noise payload: Alice का RouterInfo और random padding Non-noise payload: कोई नहीं

(Payload Security Properties [Noise](https://noiseprotocol.org/noise.html) से)

```
XK(s, rs):           Authentication   Confidentiality
  -> s, se                  2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).  The
  sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key
  pair.  Assuming the corresponding private keys are secure, this
  authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.  This payload is
  encrypted based on an ephemeral-ephemeral DH as well as an ephemeral-static
  DH with the recipient's static key pair.  Assuming the ephemeral private
  keys are secure, and the recipient is not being actively impersonated by an
  attacker that has stolen its static private key, this payload cannot be
  decrypted.

  "s": Alice writes her static public key from the s variable into the
  message buffer, encrypting it, and hashes the output along with the old h
  to derive a new h.

  "se": A DH is performed between the Alice's static key pair and the Bob's
  ephemeral key pair.  The result is hashed along with the old ck to derive a
  new ck and k, and n is set to zero.
```
इसमें दो ChaChaPoly frames हैं। पहला Alice की encrypted static public key है। दूसरा Noise payload है: Alice का encrypted RouterInfo, वैकल्पिक options, और वैकल्पिक padding। ये अलग keys का उपयोग करते हैं, क्योंकि इनके बीच में MixKey() function को call किया जाता है।

कच्ची सामग्री:

```
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data (32 bytes)  +
|   Alice static key S                  |
+     k defined in KDF for message 2    +
|   n = 1 see KDF for associated data   |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data             +
|     Length specified in message 1     |
+     (including 16 byte MAC to follow) +
|                                       |
+       Alice RouterInfo                +
|       using block format 2            |
+       Alice Options (optional)        +
|       using block format 1            |
+       Arbitrary padding               +
|       using block format 254          |
+                                       +
| k defined in KDF for message 3 part 2 |
+     n = 0                             +
|     see KDF for associated data       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, ChaChaPoly encrypted Alice's X25519 static key, little endian
     inside 48 byte ChaChaPoly frame
```
अशिफ्रित डेटा (Poly1305 auth tags दिखाए नहीं गए हैं):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|              S                        |
+       Alice static key                +
|          (32 bytes)                   |
+                                       +
|                                       |
+                                       +
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+                                       +
|       Alice RouterInfo block          |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Options block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Padding block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, Alice's X25519 static key, little endian
```
#### नोट्स

- Bob को सामान्य Router Info सत्यापन करना चाहिए। सुनिश्चित करें कि signature प्रकार समर्थित है, signature को सत्यापित करें, timestamp सीमा के भीतर है यह सत्यापित करें, और कोई भी अन्य आवश्यक जांच करें।

- Bob को सत्यापित करना होगा कि पहले frame में प्राप्त Alice की static key, Router Info में दी गई static key से मेल खाती है। Bob को पहले Router Info में एक NTCP या NTCP2 Router Address खोजना होगा जिसमें मेल खाता version (v) option हो। नीचे Published Router Info और Unpublished Router Info sections देखें।

- यदि Bob के netdb में Alice की RouterInfo का पुराना version है, तो verify करें कि router info में static key दोनों में समान है, यदि present है, और यदि पुराना version XXX से कम पुराना है (नीचे key rotate time देखें)

- Bob को यहाँ यह सत्यापित करना चाहिए कि Alice की static key curve पर एक वैध बिंदु है।

- विकल्प शामिल होने चाहिए, padding parameters निर्दिष्ट करने के लिए।

- किसी भी त्रुटि पर, जिसमें AEAD, RI, DH, timestamp, या key validation failure शामिल है, Bob को आगे की message processing रोकनी चाहिए और बिना जवाब दिए कनेक्शन बंद कर देना चाहिए। यह एक असामान्य बंद होना (TCP RST) होना चाहिए।

- तेज़ handshaking को सुविधाजनक बनाने के लिए, implementations को यह सुनिश्चित करना होगा कि Alice तीसरे संदेश की संपूर्ण सामग्री को buffer करे और फिर एक साथ flush करे, दोनों AEAD frames सहित। यह इस संभावना को बढ़ाता है कि डेटा एक ही TCP packet में समाहित होगा (जब तक कि OS या middleboxes द्वारा विभाजित न हो), और Bob द्वारा एक साथ प्राप्त होगा। यह दक्षता के लिए भी है और random padding की प्रभावशीलता सुनिश्चित करने के लिए भी है।

- Message 3 part 2 frame length: इस frame की length (MAC सहित) Alice द्वारा message 1 में भेजी जाती है। padding के लिए पर्याप्त स्थान रखने के महत्वपूर्ण नोट्स के लिए उस message को देखें।

- संदेश 3 भाग 2 फ्रेम सामग्री: इस फ्रेम का प्रारूप डेटा चरण फ्रेम के प्रारूप के समान है, सिवाय इसके कि फ्रेम की लंबाई Alice द्वारा संदेश 1 में भेजी गई है। डेटा चरण फ्रेम प्रारूप के लिए नीचे देखें। फ्रेम में निम्नलिखित क्रम में 1 से 3 ब्लॉक होने चाहिए:

1)  Alice का Router Info block (आवश्यक)   2)  Options block (वैकल्पिक)

3\) पैडिंग ब्लॉक (वैकल्पिक) इस फ्रेम में कभी भी कोई अन्य ब्लॉक प्रकार नहीं होना चाहिए।

- Message 3 part 2 padding की आवश्यकता नहीं है यदि Alice message 3 के अंत में एक data phase frame (जिसमें वैकल्पिक रूप से padding हो सकती है) जोड़ती है और दोनों को एक साथ भेजती है, क्योंकि यह एक पर्यवेक्षक को bytes की एक बड़ी stream के रूप में दिखाई देगा। चूंकि Alice के पास आम तौर पर, लेकिन हमेशा नहीं, Bob को भेजने के लिए एक I2NP message होगा (इसीलिए वह उससे जुड़ी है), यह recommended implementation है, efficiency के लिए और random padding की प्रभावशीलता सुनिश्चित करने के लिए।

- संदेश 3 AEAD फ्रेम (भाग 1 और 2) दोनों की कुल अधिकतम सैद्धांतिक लंबाई 65535 बाइट्स है; भाग 1 की लंबाई 48 बाइट्स है, इसलिए भाग 2 की अधिकतम फ्रेम लंबाई 65487 है; MAC को छोड़कर भाग 2 की अधिकतम प्लेनटेक्स्ट लंबाई 65471 है।
  चेतावनी: कुछ लागू करने वाले कार्यान्वयन बहुत छोटी लंबाई लागू करते हैं। जावा I2P वर्तमान में कुल लंबाई को 4096 बाइट्स तक सीमित करता है। अत्यधिक पैडिंग न जोड़ें।

### Key Derivation Function (KDF) (डेटा चरण के लिए)

डेटा चरण शून्य-लंबाई संबद्ध डेटा इनपुट का उपयोग करता है।

KDF chaining key ck से दो cipher keys k_ab और k_ba उत्पन्न करता है, HMAC-SHA256(key, data) का उपयोग करके जैसा कि [RFC-2104](https://tools.ietf.org/html/rfc2104) में परिभाषित है। यह Split() function है, जो Noise spec में परिभाषित के अनुसार बिल्कुल वैसा ही है।

```
ck = from handshake phase

// k_ab, k_ba = HKDF(ck, zerolen)
// ask_master = HKDF(ck, zerolen, info="ask")

// zerolen is a zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)
// overwrite the chaining key in memory, no longer needed
ck = (all zeros)

// Output 1
// cipher key, for Alice transmits to Bob (Noise doesn't make clear which is which, but Java code does)
k_ab =   HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// cipher key, for Bob transmits to Alice (Noise doesn't make clear which is which, but Java code does)
k_ba =   HMAC-SHA256(temp_key, k_ab || byte(0x02)).


KDF for SipHash for length field:
Generate an Additional Symmetric Key (ask) for SipHash
SipHash uses two 8-byte keys (big endian) and 8 byte IV for first data.

// "ask" is 3 bytes, US-ASCII, no null termination
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
// sip_master = HKDF(ask_master, h || "siphash")
// "siphash" is 7 bytes, US-ASCII, no null termination
// overwrite previous temp_key in memory
// h is from KDF for message 3 part 2
temp_key = HMAC-SHA256(ask_master, h || "siphash")
// overwrite ask_master in memory, no longer needed
ask_master = (all zeros)
sip_master = HMAC-SHA256(temp_key, byte(0x01))

Alice to Bob SipHash k1, k2, IV:
// sipkeys_ab, sipkeys_ba = HKDF(sip_master, zerolen)
// overwrite previous temp_key in memory
temp_key = HMAC-SHA256(sip_master, zerolen)
// overwrite sip_master in memory, no longer needed
sip_master = (all zeros)

sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
sipk1_ab = sipkeys_ab[0:7], little endian
sipk2_ab = sipkeys_ab[8:15], little endian
sipiv_ab = sipkeys_ab[16:23]

Bob to Alice SipHash k1, k2, IV:

sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02)).
sipk1_ba = sipkeys_ba[0:7], little endian
sipk2_ba = sipkeys_ba[8:15], little endian
sipiv_ba = sipkeys_ba[16:23]

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 4) डेटा चरण

Noise payload: जैसा कि नीचे परिभाषित है, random padding सहित Non-noise payload: कोई नहीं

संदेश 3 के दूसरे भाग से शुरू करके, सभी संदेश एक प्रमाणित और एन्क्रिप्टेड ChaChaPoly "frame" के अंदर होते हैं जिसमें एक prepended two-byte obfuscated length होती है। सभी padding frame के अंदर होती है। Frame के अंदर एक मानक प्रारूप होता है जिसमें शून्य या अधिक "blocks" होते हैं। प्रत्येक block में एक one-byte type और एक two-byte length होती है। Types में date/time, I2NP message, options, termination, और padding शामिल हैं।

नोट: Bob अपना RouterInfo Alice को डेटा चरण में अपने पहले संदेश के रूप में भेज सकता है, लेकिन यह आवश्यक नहीं है।

(Payload Security Properties [Noise](https://noiseprotocol.org/noise.html) से)

```
XK(s, rs):           Authentication   Confidentiality
  <-                        2                5
  ->                        2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.
  This payload is encrypted based on an ephemeral-ephemeral DH as well as
  an ephemeral-static DH with the recipient's static key pair.
  Assuming the ephemeral private keys are secure, and the recipient is not being actively impersonated
  by an attacker that has stolen its static private key, this payload cannot be decrypted.
```
#### नोट्स

- दक्षता के लिए और length field की पहचान को न्यूनतम करने के लिए, implementations को सुनिश्चित करना चाहिए कि sender पूरे data messages की सामग्री को एक साथ buffer करे और फिर flush करे, जिसमें length field और AEAD frame शामिल हैं। इससे इस बात की संभावना बढ़ जाती है कि data एक single TCP packet में समाहित हो जाएगा (जब तक कि OS या middleboxes द्वारा segmented न हो), और दूसरी पार्टी द्वारा एक साथ receive हो जाए। यह भी दक्षता के लिए है और random padding की प्रभावशीलता सुनिश्चित करने के लिए है।
- Router AEAD error पर session को terminate करने का विकल्प चुन सकता है, या communications को जारी रखने का प्रयास कर सकता है। यदि जारी रखता है, तो router को बार-बार errors के बाद terminate कर देना चाहिए।

#### SipHash अस्पष्ट लंबाई

संदर्भ: [SipHash](https://www.131002.net/siphash/)

एक बार जब दोनों पक्ष handshake पूरा कर लेते हैं, तो वे payloads स्थानांतरित करते हैं जो फिर ChaChaPoly "frames" में एन्क्रिप्ट और प्रमाणित किए जाते हैं।

प्रत्येक frame से पहले दो-byte length होती है, big endian में। यह length बताती है कि आगे कितने encrypted frame bytes आने हैं, MAC सहित। stream में पहचाने जाने योग्य length fields को transmit करने से बचने के लिए, frame length को SipHash से derived mask के साथ XOR करके obfuscate किया जाता है, जैसा कि data phase KDF से initialize किया गया है। ध्यान दें कि दोनों directions में KDF से unique SipHash keys और IVs होते हैं।

```
    sipk1, sipk2 = The SipHash keys from the KDF.  (two 8-byte long integers)
    IV[0] = sipiv = The SipHash IV from the KDF. (8 bytes)
    length is big endian.
    For each frame:
      IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
      Mask[n] = First 2 bytes of IV[n]
      obfuscatedLength = length ^ Mask[n]

    The first length output will be XORed with with IV[1].
```
प्राप्तकर्ता के पास समान SipHash keys और IV होती है। लंबाई को decode करना length को छुपाने के लिए उपयोग किए गए mask को derive करके और frame की लंबाई प्राप्त करने के लिए truncated digest को XOR करके किया जाता है। Frame length, MAC सहित encrypted frame की कुल लंबाई है।

#### नोट्स

- यदि आप एक SipHash library function का उपयोग करते हैं जो unsigned long integer return करता है, तो Mask के रूप में least significant two bytes का उपयोग करें। Long integer को little endian के रूप में next IV में convert करें।

#### कच्ची सामग्री

```
+----+----+----+----+----+----+----+----+
|obf size |                             |
+----+----+                             +
|                                       |
+   ChaChaPoly frame                    +
|   Encrypted and authenticated         |
+   key is k_ab for Alice to Bob        +
|   key is k_ba for Bob to Alice        |
+   as defined in KDF for data phase    +
|   n starts at 0 and increments        |
+   for each frame in that direction    +
|   no associated data                  |
+   16 bytes minimum                    +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

obf size :: 2 bytes length obfuscated with SipHash
            when de-obfuscated: 16 - 65535

Minimum size including length field is 18 bytes.
Maximum size including length field is 65537 bytes.
Obfuscated length is 2 bytes.
Maximum ChaChaPoly frame is 65535 bytes.
```
#### नोट्स

- चूंकि receiver को MAC की जांच करने के लिए पूरा frame प्राप्त करना होता है, इसलिए यह अनुशंसा की जाती है कि sender frame के आकार को अधिकतम करने के बजाय कुछ KB तक सीमित रखे। इससे receiver पर विलंबता कम से कम होगी।

#### अशिफ्रित डेटा

एन्क्रिप्टेड फ्रेम में शून्य या अधिक ब्लॉक होते हैं। प्रत्येक ब्लॉक में एक एक-बाइट आइडेंटिफायर, एक दो-बाइट लंबाई, और शून्य या अधिक बाइट का डेटा होता है।

विस्तारणीयता के लिए, प्राप्तकर्ताओं को अज्ञात पहचानकर्ताओं वाले ब्लॉक्स को अनदेखा करना चाहिए, और उन्हें padding के रूप में मानना चाहिए।

एन्क्रिप्टेड डेटा अधिकतम 65535 बाइट्स है, जिसमें 16-बाइट प्रमाणीकरण हेडर शामिल है, इसलिए अधिकतम अनएन्क्रिप्टेड डेटा 65519 बाइट्स है।

(Poly1305 प्रमाणीकरण टैग दिखाया नहीं गया):

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
~               .   .   .               ~

blk :: 1 byte
       0 for datetime
       1 for options
       2 for RouterInfo
       3 for I2NP message
       4 for termination
       224-253 reserved for experimental features
       254 for padding
       255 reserved for future extension
size :: 2 bytes, big endian, size of data to follow, 0 - 65516
data :: the data

Maximum ChaChaPoly frame is 65535 bytes.
Poly1305 tag is 16 bytes
Maximum total block size is 65519 bytes
Maximum single block size is 65519 bytes
Block type is 1 byte
Block length is 2 bytes
Maximum single block data size is 65516 bytes.
```
#### ब्लॉक क्रमबद्धता नियम

handshake message 3 part 2 में, क्रम यह होना चाहिए: RouterInfo, उसके बाद Options यदि मौजूद है, उसके बाद Padding यदि मौजूद है। कोई अन्य blocks की अनुमति नहीं है।

डेटा चरण में, क्रम अनिर्दिष्ट है, निम्नलिखित आवश्यकताओं को छोड़कर: Padding, यदि मौजूद है, तो अंतिम ब्लॉक होना चाहिए। Termination, यदि मौजूद है, तो Padding को छोड़कर अंतिम ब्लॉक होना चाहिए।

एक single frame में कई I2NP blocks हो सकते हैं। एक single frame में कई Padding blocks की अनुमति नहीं है। अन्य block types में शायद एक single frame में कई blocks नहीं होंगे, लेकिन यह निषिद्ध नहीं है।

#### दिनांक समय

समय सिंक्रोनाइज़ेशन के लिए विशेष स्थिति:

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
नोट: implementations को nearest second तक round करना चाहिए ताकि network में clock bias को रोका जा सके।

#### विकल्प

अपडेटेड विकल्प पास करें। विकल्पों में शामिल हैं: न्यूनतम और अधिकतम पैडिंग।

Options ब्लॉक परिवर्तनीय लंबाई का होगा।

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
~----+----+----+----+----+----+----+    ~
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 1
size :: 2 bytes, big endian, size of options to follow, 12 bytes minimum

tmin, tmax, rmin, rmax :: requested padding limits
    tmin and rmin are for desired resistance to traffic analysis.
    tmax and rmax are for bandwidth limits.
    tmin and tmax are the transmit limits for the router sending this options block.
    rmin and rmax are the receive limits for the router sending this options block.
    Each is a 4.4 fixed-point float representing 0 to 15.9375
    (or think of it as an unsigned 8-bit integer divided by 16.0).
    This is the ratio of padding to data. Examples:
    Value of 0x00 means no padding
    Value of 0x01 means add 6 percent padding
    Value of 0x10 means add 100 percent padding
    Value of 0x80 means add 800 percent (8x) padding
    Alice and Bob will negotiate the minimum and maximum in each direction.
    These are guidelines, there is no enforcement.
    Sender should honor receiver's maximum.
    Sender may or may not honor receiver's minimum, within bandwidth constraints.

tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
rdelay: Requested intra-message delay, 2 bytes big endian, msec average

Padding distribution specified as additional parameters?
Random delay specified as additional parameters?

more_options :: Format TBD
```
#### विकल्प समस्याएं

- विकल्प प्रारूप TBD है।
- विकल्प बातचीत TBD है।

#### RouterInfo

Alice की RouterInfo को Bob को पास करें। handshake message 3 part 2 में उपयोग किया जाता है। Alice की RouterInfo को Bob को, या Bob की को Alice को पास करें। data phase में वैकल्पिक रूप से उपयोग किया जाता है।

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
| (Alice RI in handshake msg 3 part 2)  |
~ (Alice, Bob, or third-party           ~
|  RI in data phase)                    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 2
size :: 2 bytes, big endian, size of flag + router info to follow
flg :: 1 byte flags
       bit order: 76543210
       bit 0: 0 for local store, 1 for flood request
       bits 7-1: Unused, set to 0 for future compatibility
routerinfo :: Alice's or Bob's RouterInfo
```
#### नोट्स

- जब data phase में उपयोग किया जाता है, तो receiver (Alice या Bob) को validate करना होगा कि यह वही Router Hash है जो मूल रूप से भेजा गया था (Alice के लिए) या भेजा गया था (Bob के लिए)। फिर, इसे एक local I2NP DatabaseStore Message के रूप में treat करें। signature को validate करें, अधिक recent timestamp को validate करें, और local netdb में store करें। यदि flag bit 0 है 1, और receiving party floodfill है, तो इसे एक nonzero reply token के साथ DatabaseStore Message के रूप में treat करें, और इसे nearest floodfills को flood करें।
- Router Info gzip के साथ compressed नहीं है (DatabaseStore Message के विपरीत, जहाँ यह है)
- Flooding का अनुरोध तब तक नहीं किया जाना चाहिए जब तक RouterInfo में published RouterAddresses न हों। Receiving router को RouterInfo को flood नहीं करना चाहिए जब तक उसमें published RouterAddresses न हों।
- Implementers को यह सुनिश्चित करना होगा कि जब एक block को read करते हैं, तो malformed या malicious data के कारण reads अगले block में overrun न हों।
- यह protocol इस बात की acknowledgement प्रदान नहीं करता कि RouterInfo प्राप्त हुआ, store हुआ, या flood हुआ (handshake या data phase दोनों में)। यदि acknowledgement वांछित है, और receiver floodfill है, तो sender को बजाय एक standard I2NP DatabaseStoreMessage को reply token के साथ भेजना चाहिए।

#### समस्याएं

- डेटा फेज़ में भी इस्तेमाल हो सकता है, I2NP DatabaseStoreMessage के बजाय। उदाहरण के लिए, Bob इसे डेटा फेज़ शुरू करने के लिए उपयोग कर सकता है।
- क्या इसमें originator के अलावा अन्य routers के लिए RI शामिल करने की अनुमति है, DatabaseStoreMessages के सामान्य प्रतिस्थापन के रूप में, जैसे कि floodfills द्वारा flooding के लिए?

#### I2NP Message

एक संशोधित हेडर के साथ एक एकल I2NP संदेश। I2NP संदेशों को ब्लॉक्स में या ChaChaPoly फ्रेम्स में विभाजित नहीं किया जा सकता।

यह मानक NTCP I2NP header के पहले 9 bytes का उपयोग करता है, और header के अंतिम 7 bytes को हटा देता है, जैसा कि निम्नलिखित है: expiration को 8 से 4 bytes तक छोटा करें (milliseconds के बजाय seconds, SSU के समान), 2 byte length को हटाएं (block size - 9 का उपयोग करें), और one-byte SHA256 checksum को हटाएं।

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg id         |
+----+----+----+----+----+----+----+----+
|   short exp       |     message       |
+----+----+----+----+                   +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 3
size :: 2 bytes, big endian, size of type + msg id + exp + message to follow
        I2NP message body size is (size - 9).
type :: 1 byte, I2NP msg type, see I2NP spec
msg id :: 4 bytes, big endian, I2NP message ID
short exp :: 4 bytes, big endian, I2NP message expiration, Unix timestamp, unsigned seconds.
             Wraps around in 2106
message :: I2NP message body
```
#### नोट्स

- कार्यान्वयनकर्ताओं को सुनिश्चित करना चाहिए कि ब्लॉक पढ़ते समय, गलत तरीके से बना हुआ या दुर्भावनापूर्ण डेटा अगले ब्लॉक में रीडिंग के overrun का कारण न बने।

#### समाप्ति

Noise एक स्पष्ट समाप्ति संदेश की सिफारिश करता है। मूल NTCP में यह नहीं है। कनेक्शन को बंद कर दें। यह frame में अंतिम non-padding block होना चाहिए।

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |    valid data frames   |
+----+----+----+----+----+----+----+----+
    received   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 9 or more
valid data frames received :: The number of valid AEAD data phase frames received
                              (current receive nonce value)
                              0 if error occurs in handshake phase
                              8 bytes, big endian
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       2: idle timeout
       3: router shutdown
       4: data phase AEAD failure
       5: incompatible options
       6: incompatible signature type
       7: clock skew
       8: padding violation
       9: AEAD framing error
       10: payload format error
       11: message 1 error
       12: message 2 error
       13: message 3 error
       14: intra-frame read timeout
       15: RI signature verification fail
       16: s parameter missing, invalid, or mismatched in RouterInfo
       17: banned
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### नोट्स

सभी कारण वास्तव में उपयोग नहीं हो सकते हैं, यह implementation पर निर्भर है। Handshake failures आम तौर पर TCP RST के साथ close का परिणाम होंगे। ऊपर handshake message sections में दिए गए notes देखें। सूचीबद्ध अतिरिक्त कारण consistency, logging, debugging, या यदि policy बदलाव के लिए हैं।

#### पैडिंग

यह AEAD frames के अंदर padding के लिए है। संदेश 1 और 2 के लिए padding AEAD frames के बाहर हैं। संदेश 3 और data phase के लिए सभी padding AEAD frames के अंदर हैं।

AEAD के अंदर padding को negotiated parameters का मोटे तौर पर पालन करना चाहिए। Bob ने message 2 में अपने requested tx/rx min/max parameters भेजे थे। Alice ने message 3 में अपने requested tx/rx min/max parameters भेजे थे। Data phase के दौरान updated options भेजे जा सकते हैं। ऊपर दी गई options block जानकारी देखें।

यदि मौजूद है, तो यह frame में अंतिम block होना चाहिए।

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 254
size :: 2 bytes, big endian, size of padding to follow
padding :: random data
```
#### नोट्स

- Size = 0 की अनुमति है।
- Padding रणनीतियाँ TBD।
- न्यूनतम padding TBD।
- केवल-padding frames की अनुमति है।
- Padding डिफ़ॉल्ट TBD।
- Padding parameter बातचीत के लिए options block देखें
- न्यूनतम/अधिकतम padding parameters के लिए options block देखें
- Noise संदेशों को 64KB तक सीमित करता है। यदि अधिक padding आवश्यक है, तो कई frames भेजें।
- बातचीत की गई padding के उल्लंघन पर router की प्रतिक्रिया implementation-dependent है।

#### अन्य ब्लॉक प्रकार

Implementation को forward compatibility के लिए अज्ञात block types को ignore करना चाहिए, सिवाय message 3 part 2 में, जहाँ अज्ञात blocks की अनुमति नहीं है।

#### भविष्य का कार्य

- पैडिंग की लंबाई या तो प्रति-संदेश के आधार पर तय की जानी है और लंबाई वितरण के अनुमान लगाए जाने हैं, या रैंडम देरी जोड़ी जानी चाहिए। ये प्रतिरोधी उपाय DPI का विरोध करने के लिए शामिल किए जाने हैं, क्योंकि संदेश के आकार अन्यथा यह प्रकट कर देंगे कि transport protocol द्वारा I2P traffic ले जाया जा रहा है। सटीक पैडिंग योजना भविष्य के काम का एक क्षेत्र है।

### 5) समाप्ति

कनेक्शन को सामान्य या असामान्य TCP socket बंद करने के माध्यम से समाप्त किया जा सकता है, या जैसा कि Noise सुझाता है, एक स्पष्ट समाप्ति संदेश के द्वारा। स्पष्ट समाप्ति संदेश को ऊपर डेटा फेज में परिभाषित किया गया है।

किसी भी सामान्य या असामान्य समाप्ति पर, router को किसी भी in-memory ephemeral डेटा को शून्य कर देना चाहिए, जिसमें handshake ephemeral keys, symmetric crypto keys, और संबंधित जानकारी शामिल है।

## प्रकाशित Router जानकारी

### क्षमताएं

रिलीज़ 0.9.50 के अनुसार, NTCP2 पतों में "caps" विकल्प समर्थित है, SSU के समान। "caps" विकल्प में एक या अधिक क्षमताएं प्रकाशित की जा सकती हैं। क्षमताएं किसी भी क्रम में हो सकती हैं, लेकिन कार्यान्वयन में स्थिरता के लिए "46" अनुशंसित क्रम है। दो क्षमताएं परिभाषित हैं:

4: आउटबाउंड IPv4 क्षमता को दर्शाता है। यदि host फील्ड में कोई IP प्रकाशित है, तो यह क्षमता आवश्यक नहीं है। यदि router छुपा हुआ है, या NTCP2 केवल आउटबाउंड है, तो '4' और '6' को एक ही पते में संयुक्त किया जा सकता है।

6: आउटबाउंड IPv6 क्षमता को दर्शाता है। यदि host फील्ड में कोई IP प्रकाशित है, तो यह capability आवश्यक नहीं है। यदि router छुपा हुआ है, या NTCP2 केवल आउटबाउंड है, तो '4' और '6' को एक ही address में संयुक्त किया जा सकता है।

### प्रकाशित पते

प्रकाशित RouterAddress (RouterInfo का हिस्सा) में "NTCP" या "NTCP2" का प्रोटोकॉल आइडेंटिफायर होगा।

RouterAddress में वर्तमान NTCP प्रोटोकॉल की तरह "host" और "port" विकल्प होने चाहिए।

RouterAddress में NTCP2 समर्थन को दर्शाने के लिए तीन विकल्प होने चाहिए:

- s=(Base64 key) इस RouterAddress के लिए वर्तमान Noise static public key (s)। मानक I2P Base 64 वर्णमाला का उपयोग करके Base 64 encoded। binary में 32 bytes, Base 64 encoded के रूप में 44 bytes, little-endian X25519 public key।
- i=(Base64 IV) इस RouterAddress के लिए message 1 में X value को encrypt करने के लिए वर्तमान IV। मानक I2P Base 64 वर्णमाला का उपयोग करके Base 64 encoded। binary में 16 bytes, Base 64 encoded के रूप में 24 bytes, big-endian।
- v=2 वर्तमान version (2)। जब "NTCP" के रूप में प्रकाशित किया जाता है, तो version 1 के लिए अतिरिक्त समर्थन निहित है। भविष्य के versions के लिए समर्थन comma-separated values के साथ होगा, जैसे v=2,3 Implementation को compatibility की जांच करनी चाहिए, यदि comma मौजूद है तो कई versions सहित। Comma-separated versions संख्यात्मक क्रम में होने चाहिए।

Alice को NTCP2 protocol का उपयोग करके कनेक्ट करने से पहले यह सत्यापित करना होगा कि सभी तीन विकल्प मौजूद हैं और वैध हैं।

जब "s", "i", और "v" विकल्पों के साथ "NTCP" के रूप में प्रकाशित किया जाता है, तो router को उस host और port पर NTCP और NTCP2 दोनों प्रोटोकॉल के लिए आने वाले कनेक्शन स्वीकार करने चाहिए, और प्रोटोकॉल संस्करण का स्वचालित रूप से पता लगाना चाहिए।

जब "s", "i", और "v" विकल्पों के साथ "NTCP2" के रूप में प्रकाशित किया जाता है, तो router केवल NTCP2 प्रोटोकॉल के लिए उस होस्ट और पोर्ट पर आने वाले कनेक्शन स्वीकार करता है।

यदि कोई router NTCP1 और NTCP2 दोनों connections को support करता है लेकिन incoming connections के लिए automatic version detection implement नहीं करता है, तो उसे "NTCP" और "NTCP2" दोनों addresses advertise करना चाहिए, और NTCP2 options को केवल "NTCP2" address में include करना चाहिए। Router को "NTCP2" address में "NTCP" address की तुलना में कम cost value (उच्च priority) set करनी चाहिए, ताकि NTCP2 को प्राथमिकता दी जाए।

यदि एक ही RouterInfo में कई NTCP2 RouterAddresses ("NTCP" या "NTCP2" के रूप में) प्रकाशित किए गए हैं (अतिरिक्त IP पतों या ports के लिए), तो समान port निर्दिष्ट करने वाले सभी addresses में समान NTCP2 options और values होने चाहिए। विशेष रूप से, सभी में समान static key और iv होना चाहिए।

### अप्रकाशित NTCP2 पता

यदि Alice आने वाले कनेक्शन्स के लिए अपना NTCP2 पता ("NTCP" या "NTCP2" के रूप में) प्रकाशित नहीं करती है, तो उसे एक "NTCP2" router पता प्रकाशित करना होगा जिसमें केवल उसकी static key और NTCP2 version हो, ताकि Bob message 3 part 2 में Alice का RouterInfo प्राप्त करने के बाद key को validate कर सके।

- s=(Base64 key) प्रकाशित पतों के लिए ऊपर परिभाषित के अनुसार।
- v=2 प्रकाशित पतों के लिए ऊपर परिभाषित के अनुसार।

इस router address में "i", "host" या "port" विकल्प नहीं होंगे, क्योंकि ये outbound NTCP2 connections के लिए आवश्यक नहीं हैं। इस address के लिए प्रकाशित cost का सख्त महत्व नहीं है, क्योंकि यह केवल inbound है; हालांकि, अगर cost को अन्य addresses की तुलना में अधिक (कम प्राथमिकता) सेट किया जाए तो यह अन्य routers के लिए सहायक हो सकता है। सुझाया गया मान 14 है।

Alice मौजूदा प्रकाशित "NTCP" पते में केवल "s" और "v" विकल्प भी जोड़ सकती है।

### Public Key और IV रोटेशन

RouterInfos की caching के कारण, router चालू रहने के दौरान static public key या IV को rotate नहीं करना चाहिए, चाहे वे published address में हों या न हों। Routers को इस key और IV को persistently store करना चाहिए ताकि तुरंत restart के बाद पुनः उपयोग हो सके, जिससे incoming connections काम करते रहें, और restart times expose न हों। Routers को last-shutdown time को persistently store करना चाहिए, या अन्यथा निर्धारित करना चाहिए, ताकि startup पर पिछले downtime की गणना की जा सके।

restart के समय को उजागर करने की चिंताओं के अधीन, router इस key या IV को startup पर rotate कर सकते हैं यदि router पहले कुछ समय के लिए down था (कम से कम कुछ घंटे)।

यदि router के पास कोई भी प्रकाशित NTCP2 RouterAddresses (NTCP या NTCP2 के रूप में) हैं, तो rotation से पहले न्यूनतम downtime बहुत अधिक होना चाहिए, उदाहरण के लिए एक महीना, जब तक कि स्थानीय IP address नहीं बदला हो या router "rekeys" न करे।

यदि router के पास कोई प्रकाशित SSU RouterAddresses हैं, लेकिन NTCP2 (NTCP या NTCP2 के रूप में) नहीं है, तो रोटेशन से पहले न्यूनतम डाउनटाइम अधिक होना चाहिए, उदाहरण के लिए एक दिन, जब तक कि स्थानीय IP पता नहीं बदला हो या router "rekeys" न हो। यह तब भी लागू होता है जब प्रकाशित SSU पता में introducers हों।

यदि router के पास कोई प्रकाशित RouterAddresses (NTCP, NTCP2, या SSU) नहीं हैं, तो rotation से पहले न्यूनतम downtime केवल दो घंटे तक का हो सकता है, भले ही IP address बदल जाए, जब तक कि router "rekeys" न करे।

यदि router एक अलग Router Hash में "rekeys" करता है, तो उसे एक नया noise key और IV भी generate करना चाहिए।

कार्यान्वयन को इस बात से अवगत होना चाहिए कि static public key या IV को बदलने से उन router से आने वाले NTCP2 कनेक्शन प्रतिबंधित हो जाएंगे जिन्होंने पुराने RouterInfo को cache किया है। RouterInfo प्रकाशन, tunnel peer selection (OBGW और IB closest hop दोनों सहित), zero-hop tunnel selection, transport selection, और अन्य कार्यान्वयन रणनीतियों को इस बात का ध्यान रखना चाहिए।

IV rotation key rotation के समान नियमों के अधीन है, सिवाय इसके कि IVs केवल प्रकाशित RouterAddresses में मौजूद होते हैं, इसलिए छुपे हुए या firewalled routers के लिए कोई IV नहीं होता। यदि कुछ भी बदलता है (version, key, options?) तो यह सुझाया जाता है कि IV भी बदल जाए।

नोट: rekeying से पहले न्यूनतम डाउनटाइम को नेटवर्क स्वास्थ्य सुनिश्चित करने के लिए संशोधित किया जा सकता है, और मध्यम समय के लिए डाउन रहने वाले router द्वारा reseeding को रोकने के लिए।

## संस्करण का पता लगाना

जब "NTCP" के रूप में प्रकाशित किया जाता है, तो router को आने वाले कनेक्शन के लिए protocol version का स्वचालित रूप से पता लगाना चाहिए।

यह डिटेक्शन implementation-dependent है, लेकिन यहाँ कुछ सामान्य मार्गदर्शन है।

आने वाले NTCP connection के version का पता लगाने के लिए, Bob निम्नलिखित तरीके से आगे बढ़ता है:

- कम से कम 64 बाइट्स का इंतज़ार करें (न्यूनतम NTCP2 संदेश 1 का आकार)

- यदि प्रारंभिक प्राप्त डेटा 288 या अधिक बाइट्स है, तो आने वाला कनेक्शन version 1 है।

- यदि 288 बाइट्स से कम है, तो या तो

> - अधिक डेटा के लिए थोड़ा समय प्रतीक्षा करें (व्यापक NTCP2 अपनाने से पहले अच्छी रणनीति) यदि कम से कम 288 कुल प्राप्त हुआ है, तो यह NTCP 1 है।   >   > - संस्करण 2 के रूप में डिकोडिंग के पहले चरणों को आजमाएं, यदि यह असफल हो जाता है, तो अधिक डेटा के लिए थोड़ा समय प्रतीक्षा करें (व्यापक NTCP2 अपनाने के बाद अच्छी रणनीति)   >   >   > - SessionRequest पैकेट के पहले 32 बाइट्स (X key) को key RH_B के साथ AES-256 का उपयोग करके decrypt करें।   >   > - curve पर एक वैध point को verify करें। यदि यह असफल हो जाता है, तो NTCP 1 के लिए अधिक डेटा के लिए थोड़ा समय प्रतीक्षा करें   >   > - AEAD frame को verify करें। यदि यह असफल हो जाता है, तो NTCP 1 के लिए अधिक डेटा के लिए थोड़ा समय प्रतीक्षा करें

ध्यान दें कि यदि हमें NTCP 1 पर सक्रिय TCP विभाजन हमलों का पता चलता है तो अतिरिक्त रणनीतियों या परिवर्तनों की सिफारिश की जा सकती है।

तेज़ version detection और handshaking को सुविधाजनक बनाने के लिए, implementations को यह सुनिश्चित करना चाहिए कि Alice पहले message की संपूर्ण सामग्री को buffer करे और फिर एक साथ flush करे, padding सहित। इससे इस बात की संभावना बढ़ जाती है कि डेटा एक ही TCP packet में समाहित होगा (जब तक कि OS या middleboxes द्वारा segment न किया जाए), और Bob द्वारा एक साथ प्राप्त किया जाएगा। यह efficiency के लिए भी है और random padding की प्रभावशीलता सुनिश्चित करने के लिए भी। यह NTCP और NTCP2 दोनों handshakes पर लागू होता है।

## वेरिएंट्स, फॉलबैक्स, और सामान्य समस्याएं

- यदि Alice और Bob दोनों NTCP2 का समर्थन करते हैं, तो Alice को NTCP2 के साथ कनेक्ट करना चाहिए।
- यदि Alice किसी भी कारण से NTCP2 का उपयोग करके Bob से कनेक्ट करने में विफल रहता है, तो कनेक्शन विफल हो जाता है। Alice NTCP 1 का उपयोग करके पुनः प्रयास नहीं कर सकता।

## घड़ी विचलन दिशानिर्देश

Peer timestamps पहले दो handshake संदेशों में शामिल होते हैं, Session Request और Session Created। दो peers के बीच +/- 60 सेकंड से अधिक का clock skew आमतौर पर घातक होता है। यदि Bob को लगता है कि उसकी local clock खराब है, तो वह calculated skew या किसी external source का उपयोग करके अपनी clock को adjust कर सकता है। अन्यथा, Bob को Session Created के साथ reply करना चाहिए, भले ही maximum skew exceed हो गया हो, connection को बस बंद करने के बजाय। यह Alice को Bob का timestamp प्राप्त करने और skew calculate करने की अनुमति देता है, और यदि आवश्यक हो तो कार्रवाई करने की। Bob के पास इस समय Alice की router identity नहीं है, लेकिन resources को संरक्षित करने के लिए, Bob के लिए Alice के IP से आने वाले connections को कुछ समय के लिए ban करना वांछनीय हो सकता है, या excessive skew के साथ repeated connection attempts के बाद।

Alice को RTT का आधा घटाकर गणना की गई clock skew को समायोजित करना चाहिए। यदि Alice को लगता है कि उसकी स्थानीय clock खराब है, तो वह गणना की गई skew या किसी बाहरी स्रोत का उपयोग करके अपनी clock को समायोजित कर सकती है। यदि Alice को लगता है कि Bob की clock खराब है, तो वह Bob को कुछ समय के लिए ban कर सकती है। दोनों ही स्थितियों में, Alice को कनेक्शन बंद कर देना चाहिए।

यदि Alice Session Confirmed के साथ जवाब देती है (संभवतः इसलिए कि skew 60s की सीमा के बहुत करीब है, और Alice और Bob की गणनाएं RTT के कारण बिल्कुल समान नहीं हैं), तो Bob को आधे RTT को घटाकर गणना की गई clock skew को समायोजित करना चाहिए। यदि समायोजित clock skew अधिकतम सीमा से अधिक हो जाती है, तो Bob को clock skew reason code के साथ Disconnect message भेजकर जवाब देना चाहिए, और connection को बंद कर देना चाहिए। इस बिंदु पर, Bob के पास Alice की router identity है, और वह Alice को कुछ समय के लिए ban कर सकता है।

## संदर्भ

- [सामान्य संरचनाएं](/docs/specs/common-structures)
- [I2NP](/docs/specs/i2np)
- [Network Database](/docs/overview/network-database)
- [NOISE - Noise Protocol Framework](https://noiseprotocol.org/noise.html)
- [NTCP](/docs/transport/ntcp)
- [Prop104](/proposals/104-tls-transport)
- [Prop109](/proposals/109-pt-transport)
- [Prop111](/proposals/111-ntcp-2)
- [RFC-2104 - HMAC](https://tools.ietf.org/html/rfc2104)
- [RFC-3526 - DH Groups](https://tools.ietf.org/html/rfc3526)
- [RFC-6151](https://tools.ietf.org/html/rfc6151)
- [RFC-7539 - ChaCha20-Poly1305](https://tools.ietf.org/html/rfc7539)
- [RFC-7748 - X25519](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [SipHash](https://www.131002.net/siphash/)
- [SSU](/docs/transport/ssu)
- **[STS]** Diffie, W.; van Oorschot P. C.; Wiener M. J., प्रमाणीकरण और प्रमाणित की एक्सचेंज
