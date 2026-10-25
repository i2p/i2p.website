---
title: "Tunnel निर्माण विनिर्देश (ECIES-X25519)"
description: "फॉरवर्ड सिक्योरिटी के लिए ECIES-X25519 crypto primitives का उपयोग करके tunnel Build संदेश एन्क्रिप्शन।"
slug: "tunnel-creation-ecies"
aliases:
  - "/hi/docs/specs/tunnel-creation-ecies-spec"
  - "/hi/docs/specs/tunnel-creation-ecies-spec/"
category: "प्रोटोकॉल"
lastUpdated: "2025-06"
accurateFor: "0.9.66"
---

## अवलोकन

यह दस्तावेज़ [ECIES-X25519](/docs/specs/ecies/) द्वारा शुरू की गई crypto primitives का उपयोग करके Tunnel Build message encryption को निर्दिष्ट करता है। यह routers को ElGamal से ECIES-X25519 keys में बदलने के लिए समग्र प्रस्ताव [Prop156](/proposals/156/) का एक भाग है।

दो संस्करण निर्दिष्ट हैं। पहला मौजूदा build messages और build record size का उपयोग करता है, ElGamal routers के साथ संगतता के लिए। यह specification रिलीज़ 0.9.48 के रूप में कार्यान्वित की गई थी और अब deprecated है। दूसरा दो नए build messages और एक छोटे build record size का उपयोग करता है, और केवल ECIES routers के साथ उपयोग किया जा सकता है। यह specification रिलीज़ 0.9.51 के रूप में कार्यान्वित है।

नेटवर्क को ElGamal + AES256 से ECIES + ChaCha20 में स्थानांतरित करने के उद्देश्य से, मिश्रित ElGamal और ECIES routers वाली tunnels आवश्यक हैं। मिश्रित tunnel hops को संभालने के लिए विनिर्देश प्रदान किए गए हैं। ElGamal hops के format, processing, या encryption में कोई बदलाव नहीं किया जाएगा। यह format tunnel build records के लिए समान आकार बनाए रखता है, जैसा कि compatibility के लिए आवश्यक है।

ElGamal tunnel creators प्रति-hop ephemeral X25519 keypairs उत्पन्न करेंगे, और ECIES hops वाले tunnels बनाने के लिए इस spec का पालन करेंगे।

यह दस्तावेज़ ECIES-X25519 tunnel निर्माण को निर्दिष्ट करता है। ECIES router के लिए आवश्यक सभी परिवर्तनों के अवलोकन के लिए, प्रस्ताव 156 [Prop156](/proposals/156/) देखें। लंबे रिकॉर्ड विनिर्देश के विकास की अतिरिक्त पृष्ठभूमि के लिए, प्रस्ताव 152 [Prop152](/proposals/152/) देखें। छोटे रिकॉर्ड विनिर्देश के विकास की अतिरिक्त पृष्ठभूमि के लिए, प्रस्ताव 157 [Prop157](/proposals/157/) देखें।

### क्रिप्टोग्राफिक प्राइमिटिव्स

इस विनिर्देश को लागू करने के लिए आवश्यक मूलभूत तत्व हैं:

- AES-256-CBC जैसा कि [Cryptography](/docs/specs/cryptography/) में है
- STREAM ChaCha20 functions: ENCRYPT(k, iv, plaintext) और DECRYPT(k, iv, ciphertext) - जैसा कि [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) और [RFC-7539](https://tools.ietf.org/html/rfc7539) में है
- STREAM ChaCha20/Poly1305 functions: ENCRYPT(k, n, plaintext, ad) और DECRYPT(k, n, ciphertext, ad) - जैसा कि [NTCP2](/docs/specs/ntcp2/), [ECIES-X25519](/docs/specs/ecies/), और [RFC-7539](https://tools.ietf.org/html/rfc7539) में है
- X25519 DH functions - जैसा कि [NTCP2](/docs/specs/ntcp2/) और [ECIES-X25519](/docs/specs/ecies/) में है
- HKDF(salt, ikm, info, n) - जैसा कि [NTCP2](/docs/specs/ntcp2/) और [ECIES-X25519](/docs/specs/ecies/) में है

अन्यत्र परिभाषित अन्य Noise फ़ंक्शन:

- MixHash(d) - जैसा कि [NTCP2](/docs/specs/ntcp2/) और [ECIES-X25519](/docs/specs/ecies/) में है
- MixKey(d) - जैसा कि [NTCP2](/docs/specs/ntcp2/) और [ECIES-X25519](/docs/specs/ecies/) में है

## डिज़ाइन

### Noise Protocol Framework

यह specification Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11) पर आधारित आवश्यकताओं को प्रदान करती है। Noise की भाषा में, Alice initiator है, और Bob responder है।

यह Noise protocol Noise_N_25519_ChaChaPoly_SHA256 पर आधारित है। यह Noise protocol निम्नलिखित primitives का उपयोग करता है:

- One-Way Handshake Pattern: N - Alice अपनी static key को Bob को transmit नहीं करती (N)
- DH Function: X25519 - X25519 DH जिसकी key length 32 bytes है जैसा कि [RFC-7748](https://tools.ietf.org/html/rfc7748) में निर्दिष्ट है
- Cipher Function: ChaChaPoly - AEAD_CHACHA20_POLY1305 जैसा कि [RFC-7539](https://tools.ietf.org/html/rfc7539) section 2.8 में निर्दिष्ट है। 12 byte nonce, जिसके पहले 4 bytes शून्य पर सेट हैं। यह [NTCP2](/docs/specs/ntcp2/) के समान है
- Hash Function: SHA256 - मानक 32-byte hash, जो पहले से ही I2P में व्यापक रूप से उपयोग होता है

### हैंडशेक पैटर्न

Handshakes [Noise](https://noiseprotocol.org/noise.html) handshake patterns का उपयोग करते हैं।

निम्नलिखित अक्षर मैपिंग का उपयोग किया जाता है:

- e = one-time ephemeral key (एक बार उपयोग होने वाली अस्थायी कुंजी)
- s = static key (स्थिर कुंजी)
- p = message payload (संदेश पेलोड)

बिल्ड अनुरोध Noise N पैटर्न के समान है। यह [NTCP2](/docs/specs/ntcp2/) में उपयोग किए गए XK पैटर्न के पहले (Session Request) संदेश के भी समान है।

```
<- s
  ...
  e es p ->
```
### अनुरोध एन्क्रिप्शन

Build request records tunnel creator द्वारा बनाए जाते हैं और व्यक्तिगत hop के लिए asymmetrically encrypted होते हैं। Request records का यह asymmetric encryption वर्तमान में ElGamal है जैसा कि [Cryptography](/docs/specs/cryptography/) में परिभाषित है और इसमें SHA-256 checksum शामिल है। यह design forward-secret नहीं है।

ECIES डिज़ाइन एक-तरफा Noise पैटर्न "N" का उपयोग करता है जो ECIES-X25519 ephemeral-static DH के साथ, एक HKDF के साथ, और ChaCha20/Poly1305 AEAD के साथ forward secrecy, integrity, और authentication के लिए है। Alice tunnel build requestor है। tunnel में हर hop एक Bob है।

### उत्तर एन्क्रिप्शन

Build reply records hops creator द्वारा बनाए जाते हैं और creator के लिए symmetrically encrypted होते हैं। ElGamal reply records की यह symmetric encryption AES के साथ होती है जिसमें पहले से जोड़ा गया SHA-256 checksum होता है। यह design forward-secret नहीं है।

ECIES replies अखंडता और प्रमाणीकरण के लिए ChaCha20/Poly1305 AEAD का उपयोग करते हैं।

## लॉन्ग रिकॉर्ड विनिर्देश

नोट: अप्रचलित, पुराना। नीचे निर्दिष्ट Short Record प्रारूप का उपयोग करें।

### बिल्ड रिक्वेस्ट रिकॉर्ड

एन्क्रिप्टेड BuildRequestRecords ElGamal और ECIES दोनों के लिए संगतता के लिए 528 बाइट्स होते हैं।

#### अनुरोध रिकॉर्ड अनएन्क्रिप्टेड

यह ECIES-X25519 routers के लिए tunnel BuildRequestRecord का specification है। परिवर्तनों का सारांश:

- अप्रयुक्त 32-बाइट router hash हटाएं
- अनुरोध समय को घंटों से मिनटों में बदलें
- भविष्य के परिवर्तनीय tunnel समय के लिए समाप्ति फील्ड जोड़ें
- flags के लिए अधिक स्थान जोड़ें
- अतिरिक्त build विकल्पों के लिए Mapping जोड़ें
- AES-256 reply key और IV का उपयोग hop के अपने reply रिकॉर्ड के लिए नहीं किया जाता
- अनएन्क्रिप्टेड रिकॉर्ड लंबा है क्योंकि कम encryption ओवरहेड है

अनुरोध रिकॉर्ड में कोई ChaCha reply keys नहीं हैं। ये keys एक KDF से व्युत्पन्न होती हैं। नीचे देखें।

सभी फील्ड big-endian हैं।

अनएन्क्रिप्टेड आकार: 464 बाइट्स

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40-71</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel layer key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">72-103</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel IV key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">104-135</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">136-151</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply IV</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">152</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">153-155</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">156-159</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">160-163</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">164-167</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">168-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-463</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding</td></tr>
</tbody>
</table>
flags फ़ील्ड वही है जो [Tunnel-Creation](/docs/specs/tunnel-creation/) में परिभाषित है और इसमें निम्नलिखित शामिल है:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
बिट 7 इंगित करता है कि hop एक inbound gateway (IBGW) होगा। बिट 6 इंगित करता है कि hop एक outbound endpoint (OBEP) होगा। यदि कोई भी बिट सेट नहीं है, तो hop एक intermediate participant होगा। दोनों एक साथ सेट नहीं हो सकते।

अनुरोध की समाप्ति भविष्य में परिवर्तनशील tunnel अवधि के लिए है। फिलहाल, केवल समर्थित मान 600 (10 मिनट) है।

tunnel build विकल्प एक Mapping संरचना है जो [Common](/docs/specs/common-structures/) में परिभाषित है। वर्तमान में केवल bandwidth पैरामीटर के लिए विकल्प परिभाषित हैं, API 0.9.65 के अनुसार, विवरण के लिए नीचे देखें। यदि Mapping संरचना खाली है, तो यह दो bytes 0x00 0x00 होता है। Mapping का अधिकतम आकार (length field सहित) 296 bytes है, और Mapping length field का अधिकतम मान 294 है।

#### अनुरोध रिकॉर्ड एन्क्रिप्टेड

सभी फील्ड big-endian हैं सिवाय ephemeral public key के जो little-endian है।

एन्क्रिप्टेड आकार: 528 बाइट्स

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Reply Records बनाएं

एन्क्रिप्टेड BuildReplyRecords ElGamal और ECIES दोनों के लिए संगतता के लिए 528 बाइट्स हैं।

#### Reply Record अनएन्क्रिप्टेड

यह ECIES-X25519 router के लिए tunnel BuildReplyRecord का विशिष्टीकरण है। परिवर्तनों का सारांश:

- बिल्ड रिप्लाई विकल्पों के लिए मैपिंग जोड़ें
- अनएन्क्रिप्टेड रिकॉर्ड लंबा होता है क्योंकि कम एन्क्रिप्शन ओवरहेड होता है

ECIES उत्तर ChaCha20/Poly1305 के साथ एन्क्रिप्ट किए गए हैं।

सभी फ़ील्ड big-endian हैं।

अनएन्क्रिप्टेड आकार: 512 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-510</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
tunnel build reply options एक Mapping structure है जैसा कि [Common](/docs/specs/common-structures/) में परिभाषित है। वर्तमान में केवल bandwidth parameters के लिए options परिभाषित हैं, API 0.9.65 के अनुसार, विवरण के लिए नीचे देखें। यदि Mapping structure खाली है, तो यह दो bytes 0x00 0x00 है। Mapping का अधिकतम आकार (length field सहित) 511 bytes है, और Mapping length field का अधिकतम मान 509 है।

Reply byte निम्नलिखित values में से एक है जैसा कि [Tunnel-Creation](/docs/specs/tunnel-creation/) में परिभाषित है fingerprinting से बचने के लिए:

- 0x00 (स्वीकार करें)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Reply Record एन्क्रिप्टेड

एन्क्रिप्टेड साइज़: 528 बाइट्स

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
ECIES रिकॉर्ड्स में पूर्ण संक्रमण के बाद, ranged padding नियम अनुरोध रिकॉर्ड्स के समान हैं।

### रिकॉर्ड्स का सिमेट्रिक एन्क्रिप्शन

मिश्रित tunnel की अनुमति है, और ElGamal से ECIES में संक्रमण के लिए आवश्यक हैं। संक्रमणकालीन अवधि के दौरान, बढ़ती संख्या में router ECIES keys के तहत keyed होंगे।

सिमेट्रिक क्रिप्टोग्राफी प्रीप्रोसेसिंग उसी तरह से चलेगी:

- "encryption":
  - cipher को decryption mode में चलाया जाता है
  - request records को preprocessing में पहले से ही decrypt किया जाता है (encrypted request records को छुपाते हुए)
- "decryption":
  - cipher को encryption mode में चलाया जाता है
  - request records को participant hops द्वारा encrypt किया जाता है (अगले plaintext request record को प्रकट करते हुए)
- ChaCha20 में "modes" नहीं होते, इसलिए इसे बस तीन बार चलाया जाता है:
  - एक बार preprocessing में
  - एक बार hop द्वारा
  - एक बार final reply processing पर

जब mixed tunnel का उपयोग किया जाता है, तो tunnel निर्माताओं को BuildRequestRecord के symmetric encryption को वर्तमान और पिछले hop के encryption प्रकार के आधार पर करना होगा।

प्रत्येक hop BuildReplyRecords को encrypt करने के लिए अपने स्वयं के encryption type का उपयोग करेगा, और VariableTunnelBuildMessage (VTBM) में अन्य records के लिए भी।

reply path पर, endpoint (sender) को प्रत्येक hop की reply key का उपयोग करके [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption) को पूर्ववत करना होगा।

स्पष्टीकरण के उदाहरण के रूप में, आइए एक outbound tunnel को देखते हैं जिसमें ECIES है जो ElGamal से घिरा हुआ है:

- भेजने वाला (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

सभी BuildRequestRecords अपनी एन्क्रिप्टेड स्थिति में हैं (ElGamal या ECIES का उपयोग करके)।

AES256/CBC cipher, जब उपयोग किया जाता है, तब भी प्रत्येक रिकॉर्ड के लिए उपयोग किया जाता है, कई रिकॉर्ड में chaining के बिना।

इसी प्रकार, ChaCha20 का उपयोग प्रत्येक record को encrypt करने के लिए किया जाएगा, न कि पूरे VTBM में streaming के लिए।

अनुरोध रिकॉर्ड्स को Sender (OBGW) द्वारा प्रीप्रोसेस किया जाता है:

- H3 का रिकॉर्ड निम्नलिखित का उपयोग करके "encrypted" किया जाता है:
  - H2 की reply key (ChaCha20)
  - H1 की reply key (AES256/CBC)
- H2 का रिकॉर्ड निम्नलिखित का उपयोग करके "encrypted" किया जाता है:
  - H1 की reply key (AES256/CBC)
- H1 का रिकॉर्ड symmetric encryption के बिना भेजा जाता है

केवल H2 reply encryption flag की जांच करता है, और देखता है कि इसके बाद AES256/CBC आता है।

प्रत्येक hop द्वारा प्रसंस्करण के बाद, रिकॉर्ड "decrypted" स्थिति में होते हैं:

- H3 का record निम्नलिखित का उपयोग करके "decrypt" किया जाता है:
  - H3 की reply key (AES256/CBC)
- H2 का record निम्नलिखित का उपयोग करके "decrypt" किया जाता है:
  - H3 की reply key (AES256/CBC)
  - H2 की reply key (ChaCha20-Poly1305)
- H1 का record निम्नलिखित का उपयोग करके "decrypt" किया जाता है:
  - H3 की reply key (AES256/CBC)
  - H2 की reply key (ChaCha20)
  - H1 की reply key (AES256/CBC)

Tunnel निर्माता, जिसे Inbound Endpoint (IBEP) भी कहा जाता है, उत्तर को postprocess करता है:

- H3 का record "encrypted" होता है इसका उपयोग करके:
  - H3 की reply key (AES256/CBC)
- H2 का record "encrypted" होता है इसका उपयोग करके:
  - H3 की reply key (AES256/CBC)
  - H2 की reply key (ChaCha20-Poly1305)
- H1 का record "encrypted" होता है इसका उपयोग करके:
  - H3 की reply key (AES256/CBC)
  - H2 की reply key (ChaCha20)
  - H1 की reply key (AES256/CBC)

### रिक्वेस्ट रिकॉर्ड कीज़

ये keys स्पष्ट रूप से ElGamal BuildRequestRecords में शामिल की जाती हैं। ECIES BuildRequestRecords के लिए, tunnel keys और AES reply keys शामिल की जाती हैं, लेकिन ChaCha reply keys DH exchange से derive की जाती हैं। router static ECIES keys के विवरण के लिए [Prop156](/proposals/156/) देखें।

नीचे इस बात का विवरण है कि request records में पहले भेजी गई keys को कैसे derive करें।

#### प्रारंभिक ck और h के लिए KDF

यह pattern "N" के लिए मानक [NOISE](https://noiseprotocol.org/noise.html) है जो एक मानक protocol नाम के साथ है।

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
(31 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
// Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
h = protocol_name || 0

Define ck = 32 byte chaining key. Copy the h data to ck.
Set chainKey = h

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by all routers.
```
#### Request Record के लिए KDF

ElGamal tunnel creators प्रत्येक ECIES hop के लिए tunnel में एक ephemeral X25519 keypair उत्पन्न करते हैं, और अपने BuildRequestRecord को encrypt करने के लिए उपरोक्त scheme का उपयोग करते हैं। ElGamal tunnel creators ElGamal hops को encrypt करने के लिए इस spec से पहले वाली scheme का उपयोग करेंगे।

ECIES tunnel creators को प्रत्येक ElGamal hop की public key के लिए [Tunnel-Creation](/docs/specs/tunnel-creation/) में परिभाषित scheme का उपयोग करके encrypt करना होगा। ECIES tunnel creators ECIES hops के लिए encrypt करने हेतु उपरोक्त scheme का उपयोग करेंगे।

इसका मतलब यह है कि tunnel hops केवल अपने समान एन्क्रिप्शन प्रकार के एन्क्रिप्टेड रिकॉर्ड ही देख सकेंगे।

ElGamal और ECIES tunnel creators के लिए, वे ECIES hops में एन्क्रिप्ट करने के लिए प्रति-hop अद्वितीय ephemeral X25519 keypairs उत्पन्न करेंगे।

**महत्वपूर्ण**: Ephemeral keys प्रत्येक ECIES hop के लिए और प्रत्येक build record के लिए अद्वितीय होनी चाहिए। अद्वितीय keys का उपयोग न करने से colluding hops के लिए यह पुष्टि करने का आक्रमण मार्ग खुल जाता है कि वे एक ही tunnel में हैं।

```
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
hesk = GENERATE_PRIVATE()
hepk = DERIVE_PUBLIC(hesk)

// MixHash(hepk)
// || below means append
h = SHA256(h || hepk);

// up until here, can all be precalculated by each router
// for all incoming build requests

// Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
sesk = GENERATE_PRIVATE()
sepk = DERIVE_PUBLIC(sesk)

// MixHash(sepk)
h = SHA256(h || sepk);

End of "e" message pattern.

This is the "es" message pattern:

// Noise es
// Sender performs an X25519 DH with Hop's static public key.
// Each Hop, finds the record w/ their truncated identity hash,
// and extracts the Sender's ephemeral key preceding the encrypted record.
sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
keydata = HKDF(chainKey, sharedSecret, "", 64)
// Save for Reply Record KDF
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
plaintext = 464 byte build request record
ad = h
ciphertext = ENCRYPT(k, n, plaintext, ad)

End of "es" message pattern.

// MixHash(ciphertext)
// Save for Reply Record KDF
h = SHA256(h || ciphertext)
```
`replyKey`, `layerKey` और `layerIV` को अभी भी ElGamal records के अंदर शामिल करना होगा, और इन्हें यादृच्छिक रूप से उत्पन्न किया जा सकता है।

### Reply Record एन्क्रिप्शन

Reply record ChaCha20/Poly1305 एन्क्रिप्टेड है।

```
// AEAD parameters
k = chainkey from build request
n = 0
plaintext = 512 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
## संक्षिप्त रिकॉर्ड विशिष्टता

यह विनिर्देश दो नए I2NP tunnel build संदेशों का उपयोग करता है, Short Tunnel Build Message (प्रकार 25) और Outbound Tunnel Build Reply Message (प्रकार 26)।

tunnel बनाने वाला और बनाए गए tunnel के सभी hops में ECIES-X25519 होना चाहिए, और कम से कम version 0.9.51 होना चाहिए। reply tunnel के hops (एक outbound build के लिए) या outbound tunnel (एक inbound build के लिए) की कोई आवश्यकताएं नहीं हैं।

एन्क्रिप्टेड request और reply records 218 bytes के होंगे, जबकि अन्य सभी build messages 528 bytes के होते हैं।

plaintext request records 154 बाइट्स होंगे, जबकि ElGamal records के लिए 222 बाइट्स और ऊपर परिभाषित ECIES records के लिए 464 बाइट्स होंगे।

plaintext response records 202 bytes के होंगे, जबकि ElGamal records के लिए 496 bytes और ऊपर परिभाषित ECIES records के लिए 512 bytes होंगे।

Reply encryption hop के अपने record के लिए ChaCha20/Poly1305 होगी, और build message में अन्य records के लिए ChaCha20 (ChaCha20/Poly1305 नहीं) होगी।

Request records को HKDF का उपयोग करके layer और reply keys बनाने के लिए छोटा बनाया जाएगा, इसलिए वे request में स्पष्ट रूप से शामिल नहीं होंगे।

### संदेश प्रवाह

```
STBM: Short tunnel build message (type 25)
OTBRM: Outbound tunnel build reply message (type 26)

Outbound Build A-B-C
Reply through existing inbound D-E-F


                New Tunnel
         STBM      STBM      STBM
Creator ------> A ------> B ------> C ---\
                                   OBEP   \
                                          | Garlic wrapped (optional)
                                          | OTBRM
                                          | (TUNNEL delivery)
                                          | from OBEP to
                                          | creator
              Existing Tunnel             /
Creator <-------F---------E-------- D <--/
                                   IBGW



Inbound Build D-E-F
Sent through existing outbound A-B-C


              Existing Tunnel
Creator ------> A ------> B ------> C ---\
                                  OBEP    \
                                          | Garlic wrapped (optional)
                                          | STBM
                                          | (ROUTER delivery)
                                          | from creator
                New Tunnel                | to IBGW
          STBM      STBM      STBM        /
Creator <------ F <------ E <------ D <--/
                                   IBGW
```
#### टिप्पणियां

संदेशों की garlic wrapping उन्हें OBEP (inbound build के लिए) या IBGW (outbound build के लिए) से छुपाती है। यह अनुशंसित है लेकिन आवश्यक नहीं है। यदि OBEP और IBGW एक ही router हैं, तो यह आवश्यक नहीं है।

### छोटे बिल्ड अनुरोध रिकॉर्ड

छोटे एन्क्रिप्टेड BuildRequestRecords 218 बाइट्स के होते हैं।

#### छोटा अनुरोध रिकॉर्ड अनएन्क्रिप्टेड

लंबे रिकॉर्ड्स से परिवर्तनों का सारांश:

- अनएन्क्रिप्टेड लेंथ को 464 से 154 bytes में बदलें
- एन्क्रिप्टेड लेंथ को 528 से 218 bytes में बदलें
- layer और reply keys और IVs को हटाएं, वे KDF से generate होंगे

अनुरोध रिकॉर्ड में कोई ChaCha उत्तर कुंजियां नहीं हैं। ये कुंजियां एक KDF से प्राप्त की जाती हैं। नीचे देखें।

सभी फील्ड big-endian हैं।

अनएन्क्रिप्टेड आकार: 154 बाइट्स।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">41-42</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">43</td><td style="border:1px solid var(--color-border); padding:0.6rem;">layer encryption type</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">44-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-51</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">52-55</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">56-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-153</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding (see below)</td></tr>
</tbody>
</table>
flags फ़ील्ड वही है जो [Tunnel-Creation](/docs/specs/tunnel-creation/) में परिभाषित है और इसमें निम्नलिखित शामिल है:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
बिट 7 यह दर्शाता है कि hop एक inbound gateway (IBGW) होगा। बिट 6 यह दर्शाता है कि hop एक outbound endpoint (OBEP) होगा। यदि कोई भी बिट सेट नहीं है, तो hop एक intermediate participant होगा। दोनों एक साथ सेट नहीं हो सकते।

Layer encryption प्रकार: 0 AES के लिए (जैसा कि वर्तमान tunnels में है); 1 भविष्य के लिए (ChaCha?)

अनुरोध की समाप्ति भविष्य की परिवर्तनीय tunnel अवधि के लिए है। अभी के लिए, केवल समर्थित मान 600 (10 मिनट) है।

creator ephemeral public key एक ECIES key है, big-endian। यह IBGW layer और reply keys और IVs के लिए KDF के लिए उपयोग की जाती है। यह केवल Inbound Tunnel Build message में plaintext record में शामिल की जाती है। यह आवश्यक है क्योंकि build record के लिए इस layer पर कोई DH नहीं है।

tunnel build options एक Mapping structure है जैसा कि [Common](/docs/specs/common-structures/) में परिभाषित है। वर्तमान में केवल bandwidth parameters के लिए विकल्प परिभाषित हैं, API 0.9.65 के अनुसार, विवरण के लिए नीचे देखें। यदि Mapping structure खाली है, तो यह दो bytes 0x00 0x00 है। Mapping का अधिकतम आकार (length field सहित) 98 bytes है, और Mapping length field का अधिकतम मान 96 है।

#### छोटा अनुरोध रिकॉर्ड एन्क्रिप्टेड

सभी फ़ील्ड big-endian हैं सिवाय ephemeral public key के जो little-endian है।

एन्क्रिप्टेड आकार: 218 बाइट्स

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### शॉर्ट बिल्ड रिप्लाई रिकॉर्ड्स

छोटे encrypted BuildReplyRecords 218 बाइट्स के होते हैं।

#### संक्षिप्त उत्तर रिकॉर्ड अनएन्क्रिप्टेड

लंबे रिकॉर्ड्स से परिवर्तनों का सारांश:

- अनएन्क्रिप्टेड लंबाई को 512 से 202 बाइट्स में बदलें
- एन्क्रिप्टेड लंबाई को 528 से 218 बाइट्स में बदलें

ECIES replies ChaCha20/Poly1305 के साथ encrypted हैं।

सभी फ़ील्ड big-endian हैं।

अनएन्क्रिप्टेड आकार: 202 बाइट्स।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-200</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding (see below)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
tunnel build reply options एक Mapping structure है जैसा कि [Common](/docs/specs/common-structures/) में परिभाषित है। वर्तमान में केवल bandwidth parameters के लिए विकल्प परिभाषित हैं, API 0.9.65 के अनुसार, विवरण के लिए नीचे देखें। यदि Mapping structure खाली है, तो यह दो bytes 0x00 0x00 है। Mapping का अधिकतम size (length field सहित) 201 bytes है, और Mapping length field का अधिकतम मान 199 है।

Reply byte निम्नलिखित values में से एक है जो [Tunnel-Creation](/docs/specs/tunnel-creation/) में परिभाषित है fingerprinting से बचने के लिए:

- 0x00 (स्वीकार करें)
- 30 (TUNNEL_REJECT_BANDWIDTH)

भविष्य में असमर्थित विकल्पों के लिए अस्वीकृति को दर्शाने हेतु एक अतिरिक्त उत्तर मान परिभाषित किया जा सकता है।

#### छोटा उत्तर रिकॉर्ड एन्क्रिप्टेड

एन्क्रिप्टेड साइज़: 218 बाइट्स

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### KDF

हम tunnel build record encryption/decryption के बाद Noise state से chaining key (ck) का उपयोग करके निम्नलिखित keys derive करते हैं: reply key, AES layer key, AES IV key और OBEP के लिए garlic reply key/tag।

Reply keys: ध्यान दें कि KDF OBEP और non-OBEP hops के लिए थोड़ा अलग है। लंबे records के विपरीत हम reply key के लिए ck के बाएं भाग का उपयोग नहीं कर सकते, क्योंकि यह अंतिम नहीं है और बाद में उपयोग किया जाएगा। Reply key का उपयोग AEAD/ChaCha20/Poly1305 का उपयोग करके उस record को encrypt करने के लिए और ChaCha20 का उपयोग करके अन्य records को reply करने के लिए किया जाता है। दोनों समान key का उपयोग करते हैं। Nonce, message में record की स्थिति है जो 0 से शुरू होती है। विवरण के लिए नीचे देखें।

```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
replyKey = keydata[32:63]
ck = keydata[0:31]

AES Layer key:
keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
layerKey = keydata[32:63]

IV key for non-OBEP record:
ivKey = keydata[0:31]
because it's last

IV key for OBEP record:
ck = keydata[0:31]
keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
ivKey = keydata[32:63]
ck = keydata[0:31]

OBEP garlic reply key/tag:
keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
garlicReplyKey = keydata[32:63]
garlicReplyTag = keydata[0:7]
```
नोट: OBEP पर IV key के लिए KDF अन्य hops से अलग है, भले ही reply garlic encrypted न हो।

#### रिकॉर्ड एन्क्रिप्शन

hop का अपना reply record ChaCha20/Poly1305 के साथ encrypted होता है। यह ऊपर दिए गए long record specification के समान है, सिवाय इसके कि 'n' record number 0-7 है, हमेशा 0 होने के बजाय। देखें [RFC-7539](https://tools.ietf.org/html/rfc7539)।

```
// AEAD parameters
k = replyKey from KDF above
n = record number 0-7
plaintext = 202 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
अन्य रिकॉर्ड्स को प्रत्येक hop पर ChaCha20 (ChaCha20/Poly1305 नहीं) के साथ iteratively और symmetrically encrypt किया जाता है। यह ऊपर दी गई long record specification से अलग है, जो AES का उपयोग करती है और record number का उपयोग नहीं करती।

रिकॉर्ड संख्या को IV में बाइट 4 पर रखा जाता है, क्योंकि ChaCha20 एक 12-बाइट IV का उपयोग करता है जिसमें बाइट 4-11 पर little-endian nonce होता है। देखें [RFC-7539](https://tools.ietf.org/html/rfc7539)।

```
// Parameters
k = replyKey from KDF above
n = record number 0-7
iv = 12 bytes, all zeros except iv[4] = n
plaintext = 218 byte encrypted record

ciphertext = ENCRYPT(k, iv, plaintext)
```
#### Garlic Encryption

संदेशों की garlic wrapping उन्हें OBEP (inbound build के लिए) या IBGW (outbound build के लिए) से छुपाती है। यह अनुशंसित है लेकिन आवश्यक नहीं है। यदि OBEP और IBGW एक ही router हैं, तो यह आवश्यक नहीं है।

एक inbound Short Tunnel Build Message का garlic encryption, creator द्वारा, ECIES IBGW के लिए encrypted, Noise 'N' encryption का उपयोग करता है, जैसा कि [ECIES-ROUTERS](/docs/specs/ecies-routers/) में परिभाषित है।

एक Outbound Tunnel Build Reply Message का garlic encryption, OBEP द्वारा, creator के लिए encrypted, उपरोक्त KDF से 32-byte garlic reply key और 8-byte garlic reply tag के साथ Existing Session messages का उपयोग करता है। प्रारूप [I2NP](/docs/specs/i2np/), [ECIES-ROUTERS](/docs/specs/ecies-routers/), और [ECIES-X25519](/docs/specs/ecies/) में Database Lookups के replies के लिए निर्दिष्ट के अनुसार है।

#### लेयर एन्क्रिप्शन

यह specification build request record में एक layer encryption type field शामिल करती है। वर्तमान में केवल layer encryption type 0 समर्थित है, जो AES है। यह पिछली specifications से अपरिवर्तित है, सिवाय इसके कि layer key और IV key ऊपर दिए गए KDF से derived होती हैं बजाय build request record में शामिल होने के।

नए layer encryption types जोड़ना, उदाहरण के लिए ChaCha20, अतिरिक्त अनुसंधान का विषय है, और वर्तमान में इस specification का हिस्सा नहीं है।

## कार्यान्वयन टिप्पणियाँ

- पुराने router encryption type की जांच नहीं करते और ElGamal-encrypted records भेजते हैं। कुछ हाल के router में बग हैं और वे विभिन्न प्रकार के malformed records भेजते हैं। Implementers को यदि संभव हो तो DH operation से पहले इन records का पता लगाना और उन्हें reject करना चाहिए, ताकि CPU usage कम हो सके।

### बिल्ड रिकॉर्ड्स

Build record क्रम को randomized होना चाहिए, ताकि बीच के hops को tunnel के भीतर अपनी स्थिति का पता न चले।

build records की अनुशंसित न्यूनतम संख्या 4 है। यदि hops से अधिक build records हैं, तो "fake" records जोड़े जाने चाहिए, जिनमें random या implementation-specific data हो। Inbound tunnel builds के लिए, originating router के लिए हमेशा एक "fake" record होना चाहिए, जिसमें सही 16-byte hash prefix और एक वास्तविक X25519 ephemeral key हो, अन्यथा closest hop को पता चल जाएगा कि next hop originator है।

"नकली" रिकॉर्ड का शेष भाग यादृच्छिक डेटा हो सकता है, या किसी भी प्रारूप में एन्क्रिप्टेड हो सकता है ताकि प्रवर्तक स्वयं को बिल्ड के बारे में डेटा भेज सके, संभवतः लंबित बिल्ड्स के लिए स्टोरेज आवश्यकताओं को कम करने के लिए।

इनबाउंड tunnel के मूल प्रवर्तकों को यह सत्यापित करने के लिए कोई न कोई तरीका इस्तेमाल करना चाहिए कि उनका "नकली" रिकॉर्ड पिछले hop द्वारा संशोधित नहीं किया गया है, क्योंकि इसका उपयोग deanonymization के लिए भी किया जा सकता है। मूल प्रवर्तक रिकॉर्ड का checksum संग्रहीत कर सकता है और उसे सत्यापित कर सकता है, या checksum को रिकॉर्ड में शामिल कर सकता है, या AEAD encryption/decryption function का उपयोग कर सकता है, जो implementation पर निर्भर है। यदि 16-byte hash prefix या अन्य build record सामग्री को संशोधित किया गया था, तो router को tunnel को discard कर देना चाहिए।

आउटबाउंड tunnels के लिए नकली रिकॉर्ड, और इनबाउंड tunnels के लिए अतिरिक्त नकली रिकॉर्ड, इन आवश्यकताओं के अधीन नहीं हैं, और ये पूर्णतः यादृच्छिक डेटा हो सकते हैं, क्योंकि ये कभी भी किसी hop को दिखाई नहीं देंगे। फिर भी प्रवर्तक के लिए यह सत्यापित करना वांछनीय हो सकता है कि वे संशोधित नहीं किए गए हैं।

## Tunnel बैंडविड्थ पैरामीटर

### अवलोकन

जैसे-जैसे हमने पिछले कई वर्षों में नए प्रोटोकॉल, एन्क्रिप्शन प्रकार और कंजेशन कंट्रोल में सुधार के साथ नेटवर्क की प्रदर्शन क्षमता बढ़ाई है, वीडियो स्ट्रीमिंग जैसे तेज़ एप्लिकेशन संभव होते जा रहे हैं। इन एप्लिकेशन्स को अपने client tunnel के प्रत्येक hop पर उच्च bandwidth की आवश्यकता होती है।

हालांकि, भाग लेने वाले router के पास इस बारे में कोई जानकारी नहीं होती कि जब उन्हें tunnel build message मिलता है तो कोई tunnel कितनी bandwidth का उपयोग करेगा। वे केवल सभी भाग लेने वाले tunnel द्वारा उपयोग की जा रही वर्तमान कुल bandwidth और भाग लेने वाले tunnel के लिए कुल bandwidth सीमा के आधार पर tunnel को स्वीकार या अस्वीकार कर सकते हैं।

अनुरोध करने वाले router के पास भी इस बात की कोई जानकारी नहीं होती कि प्रत्येक hop पर कितनी bandwidth उपलब्ध है।

इसके अलावा, router के पास वर्तमान में tunnel पर inbound traffic को सीमित करने का कोई तरीका नहीं है। यह overload या किसी service के DDoS के समय बहुत उपयोगी होगा।

tunnel बिल्ड रिक्वेस्ट और रिप्लाई मैसेज में tunnel बैंडविड्थ पैरामीटर इन सुविधाओं के लिए समर्थन जोड़ते हैं। अतिरिक्त पृष्ठभूमि के लिए [Prop168](/proposals/168/) देखें। ये पैरामीटर API 0.9.65 से परिभाषित हैं, लेकिन समर्थन implementation के अनुसार भिन्न हो सकता है। ये लंबे और छोटे दोनों ECIES बिल्ड रिकॉर्ड के लिए समर्थित हैं।

### बिल्ड रिक्वेस्ट विकल्प

निम्नलिखित तीन विकल्प रिकॉर्ड के tunnel build options mapping field में सेट किए जा सकते हैं: एक अनुरोधकर्ता router कोई भी, सभी, या कोई भी शामिल नहीं कर सकता है।

- m := इस tunnel के लिए आवश्यक न्यूनतम bandwidth (KBps positive integer as a string)
- r := इस tunnel के लिए अनुरोधित bandwidth (KBps positive integer as a string)
- l := इस tunnel के लिए सीमित bandwidth; केवल IBGW को भेजा जाता है (KBps positive integer as a string)

बाधा: m <= r <= l

भाग लेने वाले router को tunnel को अस्वीकार कर देना चाहिए यदि "m" निर्दिष्ट है और वह कम से कम उतनी bandwidth प्रदान नहीं कर सकता।

अनुरोध विकल्प प्रत्येक प्रतिभागी को संबंधित एन्क्रिप्टेड बिल्ड अनुरोध रिकॉर्ड में भेजे जाते हैं, और अन्य प्रतिभागियों को दिखाई नहीं देते हैं।

### बिल्ड रिप्लाई विकल्प

जब response ACCEPTED हो तो निम्नलिखित विकल्प record के tunnel build reply options mapping field में सेट किया जा सकता है:

- b := इस tunnel के लिए उपलब्ध bandwidth (KBps पॉजिटिव इंटीजर string के रूप में)

बाधा: b >= m

भाग लेने वाले router को यह शामिल करना चाहिए यदि build request में "m" या "r" में से कोई भी निर्दिष्ट किया गया था। यदि निर्दिष्ट किया गया है तो मान कम से कम "m" मान के बराबर होना चाहिए, लेकिन यदि निर्दिष्ट किया गया है तो यह "r" मान से कम या अधिक हो सकता है।

भाग लेने वाले router को tunnel के लिए कम से कम इतनी bandwidth आरक्षित करने और प्रदान करने का प्रयास करना चाहिए, हालांकि इसकी गारंटी नहीं है। Router 10 मिनट बाद की स्थितियों की भविष्यवाणी नहीं कर सकते, और भाग लेने वाला traffic एक router के अपने traffic और tunnels की तुलना में कम प्राथमिकता वाला होता है।

Router आवश्यकता पड़ने पर उपलब्ध bandwidth को over-allocate भी कर सकते हैं, और यह संभवतः वांछनीय है, क्योंकि tunnel में अन्य hops इसे अस्वीकार कर सकते हैं।

इन कारणों से, भाग लेने वाले router का उत्तर एक सर्वोत्तम प्रयास प्रतिबद्धता के रूप में माना जाना चाहिए, लेकिन गारंटी के रूप में नहीं।

Reply विकल्प अनुरोधकर्ता router को संबंधित encrypted build reply record में भेजे जाते हैं, और अन्य प्रतिभागियों को दिखाई नहीं देते।

### कार्यान्वयन टिप्पणियां

बैंडविड्थ पैरामीटर tunnel layer पर भाग लेने वाले routers पर दिखाई देते हैं, यानी प्रति सेकंड निश्चित आकार के 1 KB tunnel संदेशों की संख्या। Transport (NTCP2 या SSU2) ओवरहेड इसमें शामिल नहीं है।

यह bandwidth क्लाइंट पर दिखाई देने वाली bandwidth से काफी अधिक या कम हो सकती है। Tunnel messages में काफी overhead होता है, जिसमें ratchet और streaming सहित उच्च layers का overhead शामिल है। छोटे intermittent messages जैसे streaming acks को 1 KB तक बढ़ाया जाएगा। हालांकि, I2CP layer पर gzip compression bandwidth को काफी कम कर सकता है।

अनुरोधकर्ता router पर सबसे सरल कार्यान्वयन यह है कि अनुरोध में डालने वाली वैल्यूज की गणना करने के लिए pool में मौजूदा tunnels की औसत, न्यूनतम, और/या अधिकतम बैंडविड्थ का उपयोग करें। अधिक जटिल एल्गोरिदम संभव हैं और यह कार्यान्वयनकर्ता पर निर्भर है।

वर्तमान में कोई I2CP या SAM विकल्प परिभाषित नहीं हैं जो क्लाइंट को router को बताने के लिए उपलब्ध हों कि कितनी bandwidth की आवश्यकता है, और यहाँ कोई नए विकल्प प्रस्तावित नहीं हैं। यदि आवश्यक हो तो विकल्पों को बाद की तारीख में परिभाषित किया जा सकता है।

कार्यान्वयन उपलब्ध bandwidth या किसी अन्य डेटा, एल्गोरिदम, स्थानीय नीति, या स्थानीय कॉन्फ़िगरेशन का उपयोग करके build response में वापस की जाने वाली bandwidth value की गणना कर सकते हैं।

## संदर्भ

- [Common](/docs/specs/common-structures/)
- [Cryptography](/docs/specs/cryptography/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ECIES-X25519](/docs/specs/ecies/)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)
- [I2NP](/docs/specs/i2np/)
- [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop119](/proposals/119/)
- [Prop143](/proposals/143/)
- [Prop152](/proposals/152/)
- [Prop153](/proposals/153/)
- [Prop156](/proposals/156/)
- [Prop157](/proposals/157/)
- [Prop168](/proposals/168/)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [Tunnel-Creation](/docs/specs/tunnel-creation/)
