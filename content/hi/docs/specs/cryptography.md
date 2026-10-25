---
title: "निम्न-स्तरीय क्रिप्टोग्राफी विनिर्देश"
description: "I2P में उपयोग किए जाने वाले क्रिप्टोग्राफिक एल्गोरिदम की निम्न-स्तरीय जानकारी"
slug: "cryptography"
aliases:
  - "/hi/how_cryptography"
  - "/hi/how_cryptography/"
category: "डिज़ाइन"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## अवलोकन

> **नोट:** यह दस्तावेज़ अधिकतर अप्रचलित है। वर्तमान विनिर्देशों के लिए निम्नलिखित दस्तावेज़ देखें: > - [ECIES](/docs/specs/ecies) > - [Encrypted LeaseSet](/docs/specs/encryptedleaseset) > - [NTCP2](/docs/specs/ntcp2) > - [Red25519](/docs/specs/red25519) > - [SSU2](/docs/specs/ssu2) > - [Tunnel Creation (ECIES)](/docs/specs/tunnel-creation-ecies)

यह पृष्ठ I2P में क्रिप्टोग्राफी के निम्न-स्तरीय विवरणों को निर्दिष्ट करता है।

I2P के भीतर कई cryptographic algorithms का उपयोग होता है। I2P के मूल डिज़ाइन में, हर प्रकार का केवल एक ही algorithm था - एक symmetric algorithm, एक asymmetric algorithm, एक signing algorithm, और एक hashing algorithm। अधिक algorithms जोड़ने या अधिक सुरक्षा वाले algorithms में migrate करने का कोई प्रावधान नहीं था।

हाल के वर्षों में हमने एक framework जोड़ा है जो backward-compatible तरीके से कई primitives और combinations को support करता है। विभिन्न key और signature lengths के साथ कई signature algorithms को "signature types" द्वारा परिभाषित किया गया है। End-to-end encryption schemes, जो asymmetric और symmetric encryption के संयोजन का उपयोग करती हैं और विभिन्न key lengths के साथ आती हैं, को "encryption types" द्वारा परिभाषित किया गया है।

I2P में विभिन्न protocols और data structures में signature type और/या encryption type को निर्दिष्ट करने के लिए fields शामिल हैं। ये fields, type definitions के साथ मिलकर, key और signature lengths और उन्हें उपयोग करने के लिए आवश्यक cryptographic primitives को परिभाषित करती हैं। Signature और encryption types की परिभाषाएं [Common Structures specification](/docs/specs/common-structures) में हैं।

मूल I2P protocols NTCP, SSU, और ElGamal/AES+SessionTags ElGamal asymmetric encryption और AES symmetric encryption के संयोजन का उपयोग करते हैं। नए protocols NTCP2 और ECIES-X25519-AEAD-Ratchet X25519 key exchange और ChaCha20/Poly1305 symmetric encryption के संयोजन का उपयोग करते हैं।

- ECIES-X25519-AEAD-Ratchet ने ElGamal/AES+SessionTags को बदल दिया है।
- NTCP2 ने NTCP को बदल दिया है।
- SSU2 ने SSU को बदल दिया है।
- X25519 tunnel creation ने ElGamal tunnel creation को बदल दिया है।

## असममित एन्क्रिप्शन

I2P में मूल असममित एन्क्रिप्शन एल्गोरिदम ElGamal है। नया एल्गोरिदम, जो कई स्थानों पर उपयोग किया जाता है, ECIES X25519 DH key exchange है।

हम सभी ElGamal उपयोग को X25519 में माइग्रेट करने की प्रक्रिया में हैं।

NTCP (ElGamal के साथ) को NTCP2 (X25519 के साथ) में माइग्रेट किया गया था। ElGamal/AES+SessionTag को ECIES-X25519-AEAD-Ratchet में माइग्रेट किया जा रहा है।

### X25519

X25519 उपयोग के विवरण के लिए [NTCP2](/docs/specs/ntcp2) और [ECIES](/docs/specs/ecies) देखें।

### ElGamal

ElGamal का उपयोग I2P में कई स्थानों पर किया जाता है:

- router-to-router TunnelBuild संदेशों को एन्क्रिप्ट करने के लिए
- LeaseSet में एन्क्रिप्शन key का उपयोग करके ElGamal/AES+SessionTag के भाग के रूप में end-to-end (destination-to-destination) एन्क्रिप्शन के लिए
- ElGamal/AES+SessionTag के भाग के रूप में floodfill routers को भेजे गए कुछ netDb stores और queries के एन्क्रिप्शन के लिए (destination-to-router या router-to-router)।

हम 2048 ElGamal एन्क्रिप्शन और डिक्रिप्शन के लिए सामान्य प्राइम्स का उपयोग करते हैं, जैसा कि IETF [RFC-3526](http://tools.ietf.org/html/rfc3526) द्वारा दिया गया है। हम वर्तमान में केवल ElGamal का उपयोग एक सिंगल ब्लॉक में IV और सेशन की को एन्क्रिप्ट करने के लिए करते हैं, जिसके बाद उस की और IV का उपयोग करके AES एन्क्रिप्टेड पेलोड आता है।

अनएन्क्रिप्टेड ElGamal में निम्नलिखित शामिल है:

```
+----+----+----+----+----+----+----+----+
|nonz|           H(data)                |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |  data...
+----+----+----+-//
```
H(data) उस data का SHA256 है जो ElGamal block में encrypted है, और इसके पहले एक random nonzero byte आता है। यह byte वास्तव में 0.9.28 से random है; उससे पहले यह हमेशा 0xFF था। भविष्य में यह संभवतः flags के लिए उपयोग हो सकता है। Block में encrypted data 222 bytes तक लंबा हो सकता है। चूंकि encrypted data में काफी संख्या में zeros हो सकते हैं यदि cleartext 222 bytes से छोटा है, इसलिए यह सुझाव दिया जाता है कि higher layers cleartext को random data के साथ 222 bytes तक pad करें। कुल लंबाई: आम तौर पर 255 bytes।

एन्क्रिप्टेड ElGamal में निम्नलिखित शामिल है:

```
+----+----+----+----+----+----+----+----+
|  zero padding...       |              |
+----+----+----+-//-+----+              +
|                                       |
+                                       +
|       ElG encrypted part 1            |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    |   zero padding...      |         |
+----+----+----+----+-//-+----+         +
|                                       |
+                                       +
|       ElG encrypted part 2            |
~                                       ~
|                                       |
+         +----+----+----+----+----+----+
|         +
+----+----+
```
प्रत्येक एन्क्रिप्टेड हिस्से को शून्यों के साथ आगे बढ़ाकर ठीक 257 बाइट्स का आकार बनाया जाता है। कुल लंबाई: 514 बाइट्स। सामान्य उपयोग में, उच्च स्तरों पर cleartext डेटा को 222 बाइट्स तक पैड किया जाता है, जिसके परिणामस्वरूप 255 बाइट्स का अनएन्क्रिप्टेड ब्लॉक बनता है। इसे दो 256-बाइट एन्क्रिप्टेड हिस्सों के रूप में एन्कोड किया जाता है, और इस स्तर पर प्रत्येक हिस्से से पहले एक बाइट का शून्य पैडिंग होता है।

ElGamal कोड [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java) देखें।

साझा किया गया प्राइम 2048 बिट कीज के लिए Oakley प्राइम है [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3):

```
2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
```
या एक hexadecimal मान के रूप में:

```
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
```
2 को generator के रूप में उपयोग करना।

#### शॉर्ट एक्सपोनेंट {#exponent}

जबकि मानक घातांक आकार 2048 बिट्स (256 बाइट्स) है और I2P PrivateKey पूरे 256 बाइट्स का है, कुछ मामलों में हम 226 बिट्स (28.25 बाइट्स) के छोटे घातांक आकार का उपयोग करते हैं। यह Oakley primes के साथ उपयोग के लिए सुरक्षित होना चाहिए [vanOorschot1996] [BENCHMARKS]।

इसके अलावा, [Koshiba2004] स्पष्ट रूप से इस sci.crypt thread [SCI.CRYPT] के अनुसार इसका समर्थन करता है। PrivateKey का शेष भाग zeroes से भरा जाता है।

रिलीज़ 0.9.8 से पहले, सभी router छोटे exponent का उपयोग करते थे। रिलीज़ 0.9.8 के बाद से, 64-bit x86 router पूरे 2048-bit exponent का उपयोग करते हैं। अब सभी router पूरे exponent का उपयोग करते हैं, सिवाय बहुत धीमे hardware वाले कुछ router के, जो processor load की चिंता के कारण छोटे exponent का उपयोग करना जारी रखते हैं। इन platforms के लिए लंबे exponent में संक्रमण आगे के अध्ययन का विषय है।

#### अप्रचलन

नेटवर्क की ElGamal हमले के प्रति संवेदनशीलता और लंबी bit length पर संक्रमण के प्रभाव का अध्ययन किया जाना है। किसी भी परिवर्तन को backward-compatible बनाना काफी कठिन हो सकता है।

## सममित एन्क्रिप्शन

I2P में मूल symmetric encryption algorithm AES है। नया algorithm, जो कई स्थानों पर उपयोग किया जाता है, Authenticated Encryption with Associated Data (AEAD) ChaCha20/Poly1305 है।

हम सभी AES उपयोग को ChaCha20/Poly1305 में स्थानांतरित करने की प्रक्रिया में हैं।

NTCP (AES के साथ) को NTCP2 (ChaCha20/Poly1305 के साथ) में माइग्रेट किया गया था। ElGamal/AES+SessionTag को ECIES-X25519-AEAD-Ratchet में माइग्रेट किया जा रहा है।

### ChaCha20/Poly1305

ChaCha20/Poly1305 उपयोग के विवरण के लिए [NTCP2](/docs/specs/ntcp2) और [ECIES](/docs/specs/ecies) देखें।

### AES

AES का उपयोग symmetric encryption के लिए किया जाता है, कई मामलों में:

- SSU transport एन्क्रिप्शन के लिए (देखें अनुभाग "Transports") DH key exchange के बाद
- End-to-end (destination-to-destination) एन्क्रिप्शन के लिए ElGamal/AES+SessionTag के एक भाग के रूप में
- कुछ netDb stores और queries के एन्क्रिप्शन के लिए जो floodfill routers को भेजे जाते हैं ElGamal/AES+SessionTag के एक भाग के रूप में (destination-to-router या router-to-router)।
- Periodic tunnel test messages के एन्क्रिप्शन के लिए जो router अपने आप को भेजता है, अपनी ही tunnels के माध्यम से।

हम CBC mode में 256 bit keys और 128 bit blocks के साथ AES का उपयोग करते हैं। उपयोग की जाने वाली padding IETF [RFC-2313](http://tools.ietf.org/html/rfc2313) (PKCS#5 1.5, section 8.1 (block type 02 के लिए)) में निर्दिष्ट है। इस मामले में, padding में 16 byte blocks से मैच करने के लिए pseudorandomly generated octets होते हैं। विशेष रूप से, CBC code [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java) और Cryptix AES implementation [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java) देखें, साथ ही padding भी, जो ElGamalAESEngine.getPadding function [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java) में पाई जाती है।

#### अप्रचलन

नेटवर्क की AES हमले के प्रति संवेदनशीलता और लंबी बिट लेंथ में बदलाव के प्रभाव का अध्ययन किया जाना है। किसी भी बदलाव को backward-compatible बनाना काफी कठिन हो सकता है।

## हस्ताक्षर {#sig}

signature types द्वारा विभिन्न key और signature lengths के साथ अनेक signature algorithms परिभाषित किए गए हैं। अधिक signature types जोड़ना अपेक्षाकृत आसान है।

EdDSA-SHA512-Ed25519 वर्तमान डिफ़ॉल्ट signature algorithm है। DSA, जो signature types के लिए समर्थन जोड़ने से पहले मूल algorithm था, अभी भी नेटवर्क में उपयोग में है।

### DSA

Signatures को 1024 bit [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm) (L=1024, N=160) के साथ generate और verify किया जाता है, जैसा कि [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java) में implemented है। DSA को इसलिए चुना गया है क्योंकि यह signatures के लिए ElGamal से बहुत तेज़ है।

#### SEED

160 bit:

```
86108236b8526e296e923a4015b4282845b572cc
```
#### काउंटर

```
33
```
#### DSA अभाज्य (p)

1024 bit:

```
9C05B2AA 960D9B97 B8931963 C9CC9E8C 3026E9B8 ED92FAD0
A69CC886 D5BF8015 FCADAE31 A0AD18FA B3F01B00 A358DE23
7655C496 4AFAA2B3 37E96AD3 16B9FB1C C564B5AE C5B69A9F
F6C3E454 8707FEF8 503D91DD 8602E867 E6D35D22 35C1869C
E2479C3B 9D5401DE 04E0727F B33D6511 285D4CF2 9538D9E3
B6051F5B 22CC1C93
```
#### DSA भागफल (q)

```
A5DFC28F EF4CA1E2 86744CD8 EED9D29D 684046B7
```
#### DSA जेनरेटर (g)

1024 बिट:

```
0C1F4D27 D40093B4 29E962D7 223824E0 BBC47E7C 832A3923
6FC683AF 84889581 075FF908 2ED32353 D4374D73 01CDA1D2
3C431F46 98599DDA 02451824 FF369752 593647CC 3DDC197D
E985E43D 136CDCFC 6BD5409C D2F45082 1142A5E6 F8EB1C3A
B5D0484B 8129FCF1 7BCE4F7F 33321C3C B3DBB14A 905E7B2B
3E93BE47 08CBCC82
```
SigningPublicKey 1024 bits का है। SigningPrivateKey 160 bits का है।

#### अप्रचलन

[NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf) 2010 के बाद उपयोग के लिए न्यूनतम (L=2048, N=224) की सिफारिश करता है। यह "cryptoperiod", या किसी दिए गए key की जीवनकाल द्वारा कुछ हद तक कम हो सकता है।

यह अभाज्य संख्या 2003 में चुनी गई थी, और जिस व्यक्ति (TheCrypto) ने इस संख्या को चुना था, वह वर्तमान में I2P developer नहीं है। इसलिए, हमें नहीं पता कि चुनी गई अभाज्य संख्या एक 'strong prime' है या नहीं। यदि भविष्य के उद्देश्यों के लिए एक बड़ी अभाज्य संख्या चुनी जाती है, तो वह strong prime होनी चाहिए, और हम निर्माण प्रक्रिया का दस्तावेजीकरण करेंगे।

## नए हस्ताक्षर एल्गोरिदम

रिलीज़ 0.9.12 के अनुसार, router अतिरिक्त signature algorithms का समर्थन करता है जो 1024-bit DSA से अधिक सुरक्षित हैं। पहला उपयोग Destinations के लिए था; Router Identities के लिए समर्थन रिलीज़ 0.9.16 में जोड़ा गया था। मौजूदा Destinations को पुराने से नए signatures में माइग्रेट नहीं किया जा सकता है; हालांकि, एकल tunnel के साथ कई Destinations के लिए समर्थन है, और यह नए signature प्रकारों पर स्विच करने का एक तरीका प्रदान करता है। Signature प्रकार Destination और Router Identity में एन्कोड किया जाता है, ताकि नए signature algorithms या curves किसी भी समय जोड़े जा सकें।

वर्तमान में समर्थित हस्ताक्षर प्रकार निम्नलिखित हैं:

- DSA-SHA1
- ECDSA-SHA256-P256
- ECDSA-SHA384-P384 (व्यापक रूप से उपयोग नहीं किया जाता)
- ECDSA-SHA512-P521 (व्यापक रूप से उपयोग नहीं किया जाता)
- EdDSA-SHA512-Ed25519 (रिलीज 0.9.15 के बाद से डिफ़ॉल्ट)
- RedDSA-SHA512-Ed25519 (रिलीज 0.9.39 के बाद से)

अतिरिक्त signature प्रकार केवल application layer पर उपयोग किए जाते हैं, मुख्यतः su3 फाइलों को sign और verify करने के लिए। ये signature प्रकार निम्नलिखित हैं:

- RSA-SHA256-2048 (व्यापक रूप से उपयोग नहीं किया गया)
- RSA-SHA384-3072 (व्यापक रूप से उपयोग नहीं किया गया)
- RSA-SHA512-4096
- EdDSA-SHA512-Ed25519ph (रिलीज 0.9.25 के रूप में; व्यापक रूप से उपयोग नहीं किया गया)

### ECDSA

ECDSA मानक NIST curves और मानक SHA-2 hashes का उपयोग करता है।

हमने 0.9.16 - 0.9.19 रिलीज़ समय सीमा में नए destinations को ECDSA-SHA256-P256 में माइग्रेट किया। Router Identities के लिए उपयोग रिलीज़ 0.9.16 से समर्थित है और मौजूदा routers का माइग्रेशन 2015 में हुआ।

### RSA

मानक RSA PKCS#1 v1.5 (RFC 2313) सार्वजनिक घातांक F4 = 65537 के साथ।

RSA का उपयोग अब सभी out-of-band विश्वसनीय सामग्री पर हस्ताक्षर करने के लिए किया जाता है, जिसमें router अपडेट, reseeding, प्लगइन्स, और समाचार शामिल हैं। हस्ताक्षर "su3" प्रारूप [UPDATES] में एम्बेडेड होते हैं। 4096-बिट keys की सिफारिश की जाती है और सभी ज्ञात हस्ताक्षरकर्ताओं द्वारा उपयोग की जाती हैं। RSA का उपयोग किसी भी in-network Destinations या Router Identities में नहीं किया जाता है, और न ही इसकी योजना है।

### EdDSA 25519

मानक EdDSA जो curve 25519 और मानक 512-bit SHA-2 hashes का उपयोग करता है।

रिलीज़ 0.9.15 से समर्थित।

Destinations और Router Identities को 2015 के अंत में स्थानांतरित किया गया था।

### RedDSA 25519

curve 25519 और मानक 512-bit SHA-2 hashes का उपयोग करते हुए मानक EdDSA, लेकिन अलग private keys के साथ, और signing में मामूली संशोधन। encrypted leasesets के लिए। विवरण के लिए [EncryptedLeaseSet](/docs/specs/encryptedleaseset) और [Red25519](/docs/specs/red25519) देखें।

रिलीज़ 0.9.39 से समर्थित है।

## हैशेस

हैश का उपयोग signature एल्गोरिदम में और नेटवर्क के DHT में keys के रूप में किया जाता है।

पुराने signature algorithms SHA1 और SHA256 का उपयोग करते हैं। नए signature algorithms SHA512 का उपयोग करते हैं। DHT SHA256 का उपयोग करता है।

### SHA256

I2P के भीतर DHT hashes मानक SHA256 हैं।

#### अप्रचलन

SHA-256 हमले के लिए नेटवर्क की संवेदनशीलता और लंबे hash में संक्रमण के प्रभाव का अध्ययन किया जाना है। किसी भी बदलाव को backward-compatible बनाना काफी कठिन हो सकता है।

## ट्रांसपोर्ट

सबसे निचली प्रोटोकॉल परत पर, point-to-point inter-router संचार को transport layer security द्वारा सुरक्षित किया जाता है।

NTCP2 कनेक्शन X25519 Diffie-Hellman और ChaCha20/Poly1305 प्रमाणित एन्क्रिप्शन का उपयोग करते हैं।

SSU और अप्रचलित NTCP transports 256 बाइट (2048 बिट) Diffie-Hellman key exchange का उपयोग करते हैं जो ElGamal के लिए ऊपर निर्दिष्ट समान shared prime और generator का उपयोग करके, इसके बाद ऊपर वर्णित symmetric AES encryption का पालन करते हैं।

SSU को SSU2 में माइग्रेट करने की योजना है (X25519 और ChaCha20/Poly1305 के साथ)।

सभी transports transport links पर perfect forward secrecy [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy) प्रदान करते हैं।

### NTCP2 कनेक्शन {#tcp}

NTCP2 कनेक्शन X25519 Diffie-Hellman और ChaCha20/Poly1305 प्रमाणित एन्क्रिप्शन, और Noise प्रोटोकॉल फ्रेमवर्क [Noise](https://noiseprotocol.org/noise.html) का उपयोग करते हैं।

विवरण और संदर्भों के लिए NTCP2 विनिर्देश [NTCP2](/docs/specs/ntcp2) देखें।

### UDP कनेक्शन {#udp}

SSU (UDP transport) प्रत्येक पैकेट को AES256/CBC के साथ एक स्पष्ट IV और MAC (HMAC-MD5-128) के साथ एन्क्रिप्ट करता है, जो 2048 bit Diffie-Hellman एक्सचेंज के माध्यम से एक अस्थायी सत्र कुंजी पर सहमति के बाद, दूसरे router की DSA key के साथ station-to-station प्रमाणीकरण के साथ, और प्रत्येक नेटवर्क संदेश का स्थानीय अखंडता जाँच के लिए अपना hash होता है।

विवरण के लिए SSU specification देखें।

चेतावनी - SSU में उपयोग किया जाने वाला I2P का HMAC-MD5-128 स्पष्ट रूप से गैर-मानक है। स्पष्ट रूप से, SSU के एक प्रारंभिक संस्करण में HMAC-SHA256 का उपयोग किया गया था, और फिर प्रदर्शन कारणों से इसे MD5-128 में बदल दिया गया था, लेकिन 32-बाइट buffer size को बरकरार रखा गया। विवरण के लिए HMACGenerator.java और 2005-07-05 status notes देखें।

### NTCP कनेक्शन

NTCP का अब उपयोग नहीं होता, इसे NTCP2 से बदल दिया गया है।

NTCP कनेक्शन 2048 Diffie-Hellman implementation के साथ negotiate किए गए थे, router की identity का उपयोग करते हुए station to station agreement के साथ आगे बढ़ने के लिए, जिसके बाद कुछ encrypted protocol specific fields आते थे, और सभी बाद के data को AES (जैसा कि ऊपर बताया गया) के साथ encrypt किया जाता था। ElGamalAES+SessionTag का उपयोग करने के बजाय DH negotiation करने का मुख्य कारण यह है कि यह '(perfect) forward secrecy' [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy) प्रदान करता है, जबकि ElGamalAES+SessionTag नहीं करता।

## संदर्भ

- [BENCHMARKS](https://web.archive.org/web/20080423000000*/http://www.eskimo.com/~weidai/benchmarks.html) - Crypto++ benchmarks, मूल रूप से http://www.eskimo.com/~weidai/benchmarks.html पर (अब बंद), http://www.archive.org/ से बचाया गया, 23 अप्रैल, 2008 की तारीख।
- [Common](/docs/specs/common-structures) - Common Structures Specification
- [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java)
- [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java)
- [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm)
- [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java)
- [ECIES](/docs/specs/ecies)
- [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java)
- [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset)
- [Koshiba2004](http://www.springerlink.com/content/2jry7cftp5bpdghm/) - Koshiba & Kurosawa. Short Exponent Diffie-Hellman Problems. PKC 2004, LNCS 2947, pp. 173-186
- [NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf)
- [Noise](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2)
- [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)
- [Red25519](/docs/specs/red25519)
- [RFC-2313](http://tools.ietf.org/html/rfc2313)
- [RFC-3526](http://tools.ietf.org/html/rfc3526)
- [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3)
- [SCI.CRYPT](https://groups.google.com/forum/#!topic/sci.crypt/GFWl76dBZnc)
- [SHA-2](https://en.wikipedia.org/wiki/SHA-2)
- [SSU2](/docs/specs/ssu2)
- [UPDATES](/docs/specs/updates)
- [vanOorschot1996](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.14.5952&rep=rep1&type=pdf) - van Oorschot, Weiner. On Diffie-Hellman Key Agreement with Short Exponents. EuroCrypt '96
