---
title: "SSU (Secure Semireliable UDP)"
description: "मूल UDP परिवहन प्रोटोकॉल विनिर्देश (पुराना, SSU2 द्वारा प्रतिस्थापित)"
slug: "ssu"
aliases:
  - "/hi/docs/transport/ssu"
  - "/hi/docs/transport/ssu/"
  - "/hi/docs/transports/ssu"
  - "/hi/docs/transports/ssu/"
  - "/hi/docs/specs/ssu-spec"
  - "/hi/docs/specs/ssu-spec/"
category: "ट्रांसपोर्ट"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
---

## अवलोकन

पुराना हो गया - SSU को SSU2 से बदल दिया गया है। SSU समर्थन को i2pd से रिलीज 2.44.0 (API 0.9.56) 2022-11 में हटा दिया गया था। SSU समर्थन को Java I2P से रिलीज 2.4.0 (API 0.9.61) 2023-12 में हटा दिया गया था।

अधिक जानकारी के लिए [SSU अवलोकन](/docs/transport/ssu/) देखें।

## DH Key Exchange {#dh}

प्रारंभिक 2048-bit DH key exchange का वर्णन [SSU Keys page](/docs/transport/ssu/#keys) पर किया गया है। यह exchange वही shared prime का उपयोग करता है जो I2P के [ElGamal encryption](/docs/specs/cryptography/#elgamal) के लिए उपयोग किया जाता है।

## संदेश हेडर {#header}

सभी UDP datagrams एक 16 byte MAC (Message Authentication Code) और एक 16 byte IV (Initialization Vector) से शुरू होते हैं, जिसके बाद उपयुक्त key के साथ encrypted variable-size payload होता है। उपयोग किया गया MAC HMAC-MD5 है, जो 16 bytes तक truncated है, जबकि key एक पूर्ण 32 byte AES256 key है। MAC का specific construct निम्नलिखित से पहले 16 bytes है:

```
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)
```
जहाँ '+' का मतलब append (जोड़ना) है और '^' का मतलब exclusive-or (विशिष्ट-या) है।

IV प्रत्येक packet के लिए randomly generate किया जाता है। encryptedPayload, flag byte से शुरू होने वाले message का encrypted version है (encrypt-then-MAC)। MAC में उपयोग किया जाने वाला payloadLength एक 2 byte unsigned integer है, big endian। ध्यान दें कि protocolVersion 0 है, इसलिए exclusive-or एक no-op है। macKey या तो introduction key है या exchanged DH key से construct किया जाता है (नीचे विवरण देखें), जैसा कि नीचे प्रत्येक message के लिए specified है।

**चेतावनी** - यहाँ उपयोग किया गया HMAC-MD5-128 गैर-मानक है, अधिक जानकारी के लिए [HMAC विवरण](/docs/specs/cryptography/#udp) देखें।

पेलोड स्वयं (यानी, flag byte से शुरू होने वाला संदेश) IV और sessionKey के साथ AES256/CBC एन्क्रिप्ट किया गया है, जिसमें replay prevention इसके body के भीतर संबोधित किया गया है, जो नीचे समझाया गया है।

protocolVersion एक 2 बाइट का unsigned integer है, big endian में, और वर्तमान में यह 0 पर सेट है। अलग protocol version का उपयोग करने वाले peers इस peer के साथ संवाद नहीं कर पाएंगे, हालांकि इस flag का उपयोग नहीं करने वाले पुराने versions कर सकते हैं।

((netid - 2) << 8) का exclusive OR cross-network connections को तुरंत पहचानने के लिए उपयोग किया जाता है। netid एक 2 बाइट unsigned integer है, big endian में, और वर्तमान में इसे 2 पर सेट किया गया है। 0.9.42 के अनुसार। अधिक जानकारी के लिए proposal 147 देखें। चूंकि वर्तमान network ID 2 है, यह वर्तमान network के लिए no-op है और backward compatible है। test networks से कोई भी connections में अलग ID होगी और HMAC fail हो जाएगा।

### HMAC विनिर्देश

- Inner padding: 0x36...
- Outer padding: 0x5C...
- Key: 32 बाइट्स
- Hash digest function: MD5, 16 बाइट्स
- Block size: 64 बाइट्स
- MAC size: 16 बाइट्स
- Example C implementations:
  - hmac.h in [i2pd](https://github.com/PurpleI2P/i2pd)
  - I2PHMAC.cpp in [i2pcpp](http://git.repo.i2p/w/i2pcpp.git)
- Example Java implementation:
  - I2PHMac.java in [I2P](https://github.com/i2p/i2p.i2p)

### सेशन की विवरण

32-बाइट session key निम्नलिखित तरीके से बनाई जाती है:

1. एक्सचेंज की गई DH key को लें, जो एक पॉजिटिव minimal-length
   BigInteger byte array (two's complement big-endian) के रूप में प्रस्तुत है
2. यदि सबसे महत्वपूर्ण बिट 1 है (यानी array[0] & 0x80 != 0),
   तो एक 0x00 byte को prepend करें, जैसे Java के BigInteger.toByteArray()
   representation में होता है
3. यदि byte array 32 bytes से अधिक या बराबर है, तो
   पहले (सबसे महत्वपूर्ण) 32 bytes का उपयोग करें
4. यदि byte array 32 bytes से कम है, तो 0x00 bytes को append करके इसे
   32 bytes तक बढ़ाएं। *बहुत कम संभावना - नीचे दी गई टिप्पणी देखें।*

### MAC Key विवरण

32-बाइट MAC key इस प्रकार बनाई जाती है:

1. ऊपर दिए गए Session Key Details में चरण 2 से एक्सचेंज की गई DH key byte array को लें, जिसमें यदि आवश्यक हो तो 0x00 byte को प्रीपेंड किया गया हो।
2. यदि वह byte array 64 bytes से बड़ी या बराबर है, तो MAC key उस byte array के bytes 33-64 होंगी।
3. यदि वह byte array 64 bytes से कम है, तो MAC key उस byte array का SHA-256 Hash होगी। *रिलीज़ 0.9.8 के बाद से। नीचे दिया गया नोट देखें।*

#### महत्वपूर्ण नोट

रिलीज 0.9.8 से पहले का कोड टूटा हुआ था और 32 से 63 बाइट्स के बीच DH key byte arrays को सही तरीके से handle नहीं करता था (ऊपर step 3 और 4) और कनेक्शन fail हो जाता था। चूंकि ये cases कभी भी काम नहीं करते थे, इन्हें रिलीज 0.9.8 के लिए ऊपर वर्णित तरीके से फिर से परिभाषित किया गया, और 0-32 byte case को भी फिर से परिभाषित किया गया। चूंकि nominal exchanged DH key 256 bytes का होता है, minimal representation के 64 bytes से कम होने की संभावना बेहद कम है।

### हेडर प्रारूप

AES एन्क्रिप्टेड payload के भीतर, विभिन्न संदेशों के लिए एक न्यूनतम सामान्य संरचना है - एक बाइट का flag और एक चार बाइट का भेजने का timestamp (unix epoch के बाद से सेकंड में)।

हेडर फॉर्मेट है:

```
Header: 37+ bytes
  Encryption starts with the flag byte.
  +----+----+----+----+----+----+----+----+
  |                  MAC                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                   IV                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |flag|        time       |              |
  +----+----+----+----+----+              +
  | keying material (optional)            |
  +                                       +
  |                                       |
  ~                                       ~
  |                                       |
  +                        +----+----+----+
  |                        |#opt|         |
  +----+----+----+----+----+----+         +
  | #opt extended option bytes (optional) |
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
```
फ्लैग बाइट में निम्नलिखित बिटफ़ील्ड होते हैं:

```
Bit order: 76543210 (bit 7 is MSB)

  bits 7-4: payload type
     bit 3: If 1, rekey data is included. Always 0, unimplemented
     bit 2: If 1, extended options are included. Always 0 before release
            0.9.24.
  bits 1-0: reserved, set to 0 for compatibility with future uses
```
रीकीइंग और विस्तारित विकल्पों के बिना, हेडर का आकार 37 बाइट्स है।

### पुनः कुंजीकरण {#rekey}

यदि rekey flag सेट है, तो timestamp के बाद 64 bytes की keying material आती है।

जब rekeying करते हैं, तो keying material के पहले 32 bytes को SHA256 में डाला जाता है नई MAC key बनाने के लिए, और अगले 32 bytes को SHA256 में डाला जाता है नई session key बनाने के लिए, हालांकि keys तुरंत इस्तेमाल नहीं की जातीं। दूसरी तरफ को भी rekey flag सेट करके और वही keying material के साथ जवाब देना चाहिए। एक बार जब दोनों तरफ से ये values भेजी और प्राप्त की गई हों, तो नई keys का इस्तेमाल करना चाहिए और पुरानी keys को हटा देना चाहिए। packet loss और reordering को संभालने के लिए पुरानी keys को थोड़ी देर तक रखना उपयोगी हो सकता है।

नोट: रीकीइंग वर्तमान में अनुपलब्ध है।

### विस्तृत विकल्प {#extend}

यदि extended options flag सेट है, तो एक बाइट का option size value जोड़ा जाता है, जिसके बाद उतने extended option bytes होते हैं। Extended options हमेशा से specification का हिस्सा रहे हैं, लेकिन release 0.9.24 तक implement नहीं किए गए थे। जब मौजूद हों, तो option format message type के लिए विशिष्ट होता है। दिए गए message के लिए extended options की अपेक्षा है या नहीं और निर्दिष्ट format के लिए नीचे message documentation देखें। जबकि Java routers ने हमेशा flag और options length को पहचाना है, अन्य implementations ने नहीं। इसलिए, release 0.9.24 से पुराने routers को extended options न भेजें।

## पैडिंग

सभी संदेशों में 0 या अधिक bytes की padding होती है। प्रत्येक संदेश को 16 byte boundary तक padded होना चाहिए, जैसा कि [AES256 encryption layer](/docs/specs/cryptography/#AES) द्वारा आवश्यक है।

रिलीज़ 0.9.7 तक, संदेशों को केवल अगली 16 बाइट सीमा तक padded किया जाता था, और जो संदेश 16 बाइट के गुणज नहीं थे वे संभावित रूप से अवैध हो सकते थे।

रिलीज़ 0.9.7 के अनुसार, संदेशों को किसी भी लंबाई तक padded किया जा सकता है जब तक कि वर्तमान MTU का सम्मान किया जाए। 16 बाइट्स के अंतिम ब्लॉक के बाद कोई भी अतिरिक्त 1-15 padding बाइट्स को encrypt या decrypt नहीं किया जा सकता और उन्हें अनदेखा कर दिया जाएगा। हालांकि, पूरी लंबाई और सभी padding को MAC गणना में शामिल किया जाता है।

रिलीज 0.9.8 के अनुसार, प्रसारित संदेश आवश्यक रूप से 16 बाइट्स के गुणज नहीं हैं। SessionConfirmed संदेश एक अपवाद है, नीचे देखें।

## कुंजियाँ

SessionCreated और SessionConfirmed संदेशों में हस्ताक्षर [RouterIdentity](/docs/specs/common-structures/#routeridentity) से [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) का उपयोग करके बनाए जाते हैं जो network database में प्रकाशित करके out-of-band वितरित किया जाता है, और संबंधित [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) के साथ।

रिलीज़ 0.9.15 तक, signature algorithm हमेशा DSA था, जिसमें 40 byte का signature होता था।

रिलीज़ 0.9.16 के अनुसार, signature algorithm को Bob के [RouterIdentity](/docs/specs/common-structures/#routeridentity) में एक [KeyCertificate](/docs/specs/common-structures/#key-certificates) द्वारा निर्दिष्ट किया जा सकता है।

परिचय कीज़ और सेशन कीज़ दोनों 32 बाइट्स की होती हैं, और Common structures specification [SessionKey](/docs/specs/common-structures/#sessionkey) द्वारा परिभाषित की जाती हैं। MAC और encryption के लिए उपयोग की जाने वाली key नीचे प्रत्येक संदेश के लिए निर्दिष्ट है।

Introduction keys बाहरी चैनल (network database) के माध्यम से वितरित की जाती हैं, जहाँ ये पारंपरिक रूप से release 0.9.47 तक router Hash के समान रही हैं, लेकिन release 0.9.48 से ये random हो सकती हैं।

## नोट्स

### IPv6

प्रोटोकॉल स्पेसिफिकेशन 4-बाइट IPv4 और 16-बाइट IPv6 दोनों पतों की अनुमति देता है। SSU-over-IPv6 को वर्जन 0.9.8 से समर्थित किया गया है। IPv6 समर्थन के विवरण के लिए नीचे दिए गए व्यक्तिगत संदेशों के दस्तावेज़ीकरण को देखें।

### टाइमस्टैम्प {#time}

जबकि I2P का अधिकांश भाग मिलीसेकंड रिज़ॉल्यूशन के साथ 8-byte [Date](/docs/specs/common-structures/#date) timestamps का उपयोग करता है, SSU एक-सेकंड रिज़ॉल्यूशन के साथ 4-byte unsigned integer timestamps का उपयोग करता है। चूंकि ये values unsigned हैं, ये फरवरी 2106 तक roll over नहीं होंगे।

## संदेश

10 संदेश (payload types) परिभाषित हैं:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Notes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionrequest">SessionRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessioncreated">SessionCreated</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionconfirmed">SessionConfirmed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayrequest">RelayRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayresponse">RelayResponse</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayintro">RelayIntro</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#peertest">PeerTest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessiondestroyed">SessionDestroyed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Implemented as of 0.8.9</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#holepunch">HolePunch</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### SessionRequest (type 0) {#sessionrequest}

यह session स्थापित करने के लिए भेजा गया पहला संदेश है।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte X, to begin the DH agreement; 1 byte IP address size; that many bytes representation of Bob's IP address; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
</table>
संदेश प्रारूप:

```
+----+----+----+----+----+----+----+----+
|         X, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
वर्तमान implementation में header सहित सामान्य आकार: 304 (IPv4) या 320 (IPv6) bytes (non-mod-16 padding से पहले)

#### विस्तृत विकल्प

नोट: 0.9.24 में लागू किया गया।

- न्यूनतम लंबाई: 3 (विकल्प लंबाई बाइट + 2 बाइट्स)
- विकल्प लंबाई: न्यूनतम 2
- 2 बाइट्स flags:

```
Bit order: 15...76543210 (bit 15 is MSB)

      bit 0: 1 for Alice to request a relay tag from Bob in the
             SessionCreated response, 0 if Alice does not need a relay tag.
             Note that "1" is the default if no extended options are present
  bits 15-1: unused, set to 0 for compatibility with future uses
```
#### नोट्स

- IPv4 और IPv6 पते समर्थित हैं।
- असंसाधित डेटा का संभावित रूप से भविष्य में चुनौतियों के लिए उपयोग किया जा सकता है।

### SessionCreated (type 1) {#sessioncreated}

यह एक [SessionRequest](#sessionrequest) का प्रतिक्रिया है।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte Y, to complete the DH agreement; 1 byte IP address size; that many bytes representation of Alice's IP address; 2 byte Alice's port number; 4 byte relay (introduction) tag which Alice can publish (else 0x00000000); 4 byte timestamp (seconds from the epoch) for use in the DSA signature; Bob's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Bob's signed on time), encrypted with another layer of encryption using the negotiated sessionKey. The IV is reused here. See notes for length information.; 0-15 bytes of padding of the signature, using random data, to a multiple of 16 bytes, so that the signature + padding may be encrypted with an additional layer of encryption using the negotiated session key as part of the DSA block.; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, with an additional layer of encryption over the 40 byte signature and the following 8 bytes padding.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey</td>
</tr>
</table>
संदेश प्रारूप:

```
+----+----+----+----+----+----+----+----+
|         Y, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| Port (A)| public relay tag  |  signed
+----+----+----+----+----+----+----+----+
  on time |                             |
+----+----+                             +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+         +----+----+----+----+----+----+
|         |   (0-15 bytes of padding) 
+----+----+----+----+----+----+----+----+
          |                             |
+----+----+                             +
|           arbitrary amount            |
~        of uninterpreted data          ~
~                .  .  .                ~
```
वर्तमान implementation में header सहित सामान्य आकार: 368 bytes (IPv4 या IPv6) (non-mod-16 padding से पहले)

#### नोट्स

- IPv4 और IPv6 addresses समर्थित हैं।
- यदि relay tag शून्य नहीं है, तो Bob Alice के लिए introducer का काम करने की पेशकश कर रहा है। Alice बाद में network database में Bob का address और relay tag प्रकाशित कर सकती है।
- signature के लिए, Bob को अपने external port का उपयोग करना चाहिए, क्योंकि Alice इसी का उपयोग verify करने के लिए करेगी। यदि Bob के NAT/firewall ने उसके internal port को एक अलग external port में map किया है, और Bob को इसकी जानकारी नहीं है, तो Alice द्वारा verification fail हो जाएगी।
- Signatures के विवरण के लिए ऊपर [Keys](#keys) section देखें। Alice के पास पहले से ही Bob की public signing key है, network database से।
- Release 0.9.15 तक, signature हमेशा 40 byte DSA signature थी और padding हमेशा 8 bytes थी। Release 0.9.16 से, signature type और length Bob के [RouterIdentity](/docs/specs/common-structures/#routeridentity) में [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) के type से implied हैं। Padding 16 bytes के multiple के लिए आवश्यकतानुसार है।
- यह एकमात्र message है जो sender की intro key का उपयोग करता है। अन्य सभी receiver की intro key या established session key का उपयोग करते हैं।
- Signed-on time वर्तमान implementation में unused या unverified लगता है।
- Uninterpreted data भविष्य में challenges के लिए संभावित रूप से उपयोग किया जा सकता है।
- Header में extended options: अपेक्षित नहीं, अपरिभाषित।

### SessionConfirmed (प्रकार 2) {#sessionconfirmed}

यह [SessionCreated](#sessioncreated) संदेश का उत्तर है और एक session स्थापित करने का अंतिम चरण है। यदि Router Identity को खंडित करना पड़े तो कई SessionConfirmed संदेशों की आवश्यकता हो सकती है।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte identity fragment info (bits 7-4: current identity fragment # 0-14; bits 3-0: total identity fragments (F) 1-15); 2 byte size of the current identity fragment; that many byte fragment of Alice's <a href="/docs/specs/common-structures/#routeridentity">RouterIdentity</a>; After the last identity fragment only: 4 byte signed-on time; N bytes padding, currently uninterpreted; After the last identity fragment only: The remaining bytes contain Alice's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Alice's signed on time). See notes for length information.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey, as generated from the DH exchange</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key, as generated from the DH exchange</td>
</tr>
</table>
**Fragment 0 से F-2 तक** (केवल यदि F > 1; वर्तमान में अप्रयुक्त, नीचे नोट्स देखें):

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|      fragment of Alice's full         |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
**Fragment F-1 (अंतिम या एकमात्र fragment):**

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|     last fragment of Alice's full     |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|  signed on time   |                   |
+----+----+----+----+                   +
|  arbitrary amount of uninterpreted    |
~      data, until the signature at     ~
~       end of the current packet       ~
|  Packet length must be mult. of 16    |
+----+----+----+----+----+----+----+----+
+                                       +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
वर्तमान implementation में header सहित सामान्य आकार: 512 bytes (Ed25519 signature के साथ) या 480 bytes (DSA-SHA1 signature के साथ) (non-mod-16 padding से पहले)

#### नोट्स

- वर्तमान कार्यान्वयन में, अधिकतम fragment आकार 512 बाइट्स है। इसे विस्तारित करना चाहिए ताकि लंबे signatures fragmentation के बिना काम कर सकें।
  वर्तमान कार्यान्वयन दो fragments में विभाजित signatures को सही तरीके से प्रोसेस नहीं करता।
- सामान्य [RouterIdentity](/docs/specs/common-structures/#routeridentity) 387 बाइट्स का है, इसलिए fragmentation की कभी आवश्यकता नहीं होती। यदि नई crypto RouterIdentity का आकार बढ़ाती है, तो
  fragmentation scheme का सावधानीपूर्वक परीक्षण किया जाना चाहिए।
- अनुपस्थित fragments का अनुरोध करने या पुनः वितरित करने के लिए कोई तंत्र नहीं है।
- कुल fragments फील्ड F को सभी fragments में समान रूप से सेट किया जाना चाहिए।
- DSA signatures पर विस्तार के लिए ऊपर [Keys](#keys) अनुभाग देखें।
- Signed-on time वर्तमान कार्यान्वयन में अप्रयुक्त या असत्यापित प्रतीत होता है।
- चूंकि signature अंत में है, अंतिम या केवल packet में padding को कुल packet को 16 बाइट्स के गुणज तक pad करना चाहिए, या signature
  सही तरीके से decrypt नहीं होगा। यह अन्य सभी message प्रकारों से अलग है, जहां padding अंत में होती है।
- रिलीज़ 0.9.15 तक, signature हमेशा 40 बाइट DSA signature था। रिलीज़ 0.9.16 से,
  signature प्रकार और लंबाई Alice के [RouterIdentity](/docs/specs/common-structures/#routeridentity) में [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) के प्रकार से निहित हैं। Padding
  16 बाइट्स के गुणज के लिए आवश्यक है।
- Header में विस्तारित विकल्प: अपेक्षित नहीं, अपरिभाषित।

### SessionDestroyed (प्रकार 8) {#sessiondestroyed}

SessionDestroyed संदेश को रिलीज़ 0.8.1 में लागू किया गया था (केवल रिसेप्शन के लिए), और रिलीज़ 0.8.9 से इसे भेजा जाता है।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob or Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">none</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
इस संदेश में कोई डेटा नहीं है। वर्तमान कार्यान्वयन में हेडर सहित सामान्य आकार: 48 बाइट्स (non-mod-16 padding से पहले)

#### नोट्स

- भेजने वाले या प्राप्त करने वाले की intro key के साथ प्राप्त Destroy संदेशों को नजरअंदाज कर दिया जाएगा।
- हेडर में Extended विकल्प: अपेक्षित नहीं, अपरिभाषित।

### RelayRequest (type 3) {#relayrequest}

यह Alice से Bob को भेजा गया पहला संदेश है जो Charlie से परिचय का अनुरोध करता है।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte relay (introduction) tag, nonzero, as received by Alice in the SessionCreated message from Bob; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes to be relayed to Charlie in the intro; Alice's 32-byte introduction key (so Bob can reply with Charlie's info); 4 byte nonce of Alice's relay request; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
संदेश प्रारूप:

```
+----+----+----+----+----+----+----+----+
|      relay tag    |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|size| challenge bytes   |
+----+----+----+----+                   +
|      to be delivered to Charlie       |
+----+----+----+----+----+----+----+----+
| Alice's intro key                     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|       nonce       |                   |
+----+----+----+----+                   +
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
वर्तमान implementation में header सहित सामान्य आकार: 96 bytes (Alice IP शामिल नहीं) या 112 bytes (4-byte Alice IP शामिल) (non-mod-16 padding से पहले)

#### नोट्स

- IP address केवल तभी शामिल किया जाता है जब यह packet के
  source address और port से अलग हो।
- यह message IPv4 या IPv6 के माध्यम से भेजा जा सकता है।
  यदि message IPv4 introduction के लिए IPv6 के माध्यम से है,
  या (release 0.9.50 के बाद से) IPv6 introduction के लिए IPv4 के माध्यम से है,
  तो Alice को अपना introduction address और port शामिल करना चाहिए।
  यह release 0.9.50 के बाद से समर्थित है।
- यदि Alice अपना address/port शामिल करती है, तो Bob जारी रखने से पहले
  अतिरिक्त validation कर सकता है।
  - Release 0.9.24 से पहले, Java I2P ने किसी भी address या port को अस्वीकार कर दिया
    जो connection से अलग था।
- Challenge अभी तक implement नहीं है, challenge size हमेशा zero होता है
- IPv6 के लिए relaying release 0.9.50 के बाद से समर्थित है।
- Release 0.9.12 से पहले, Bob की intro key हमेशा उपयोग की जाती थी। Release
  0.9.12 के बाद से, session key का उपयोग किया जाता है यदि Alice और
  Bob के बीच एक established session है। व्यावहारिक रूप से, एक established session होना चाहिए, क्योंकि Alice
  केवल session created message से nonce (introduction tag) प्राप्त करेगी,
  और Bob session destroy होने पर introduction tag को invalid मार्क कर देगा।
- Header में extended options: अपेक्षित नहीं, undefined।

### RelayResponse (type 4) {#relayresponse}

यह एक [RelayRequest](#relayrequest) का जवाब है और Bob से Alice को भेजा जाता है।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Charlie's IP address; 2 byte Charlie's port number; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte Alice's port number; 4 byte nonce sent by Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
संदेश प्रारूप:

```
+----+----+----+----+----+----+----+----+
|size|    Charlie IP     | Port (C)|size|
+----+----+----+----+----+----+----+----+
|    Alice IP       | Port (A)|  nonce
+----+----+----+----+----+----+----+----+
          |   arbitrary amount of       |
+----+----+                             +
|          uninterpreted data           |
~                .  .  .                ~
```
वर्तमान कार्यान्वयन में header सहित सामान्य आकार: 64 (Alice IPv4) या 80 (Alice IPv6) बाइट्स (non-mod-16 padding से पहले)

#### टिप्पणियाँ

- यह संदेश IPv4 या IPv6 के माध्यम से भेजा जा सकता है।
- Alice का IP address/port वह स्पष्ट IP/port है जो Bob को RelayRequest पर प्राप्त हुआ (जरूरी नहीं कि वह IP हो जो Alice ने RelayRequest में शामिल की हो), और यह IPv4 या IPv6 हो सकता है। Alice वर्तमान में प्राप्त होने पर इन्हें अनदेखा करती है।
- Charlie का IP address IPv4 हो सकता है, या, release 0.9.50 के अनुसार, IPv6, क्योंकि यह वह address है जिस पर Alice Hole Punch के बाद SessionRequest भेजेगी।
- IPv6 के लिए Relaying को release 0.9.50 के अनुसार समर्थित किया गया है।
- Release 0.9.12 से पहले, Alice की intro key हमेशा उपयोग की जाती थी। Release 0.9.12 के अनुसार, session key का उपयोग किया जाता है यदि Alice और Bob के बीच एक स्थापित session है।
- Header में Extended options: अपेक्षित नहीं, अपरिभाषित।

### RelayIntro (प्रकार 5) {#relayintro}

यह Alice का परिचय है, जो Bob से Charlie को भेजा गया है।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Charlie</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes relayed from Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie MAC Key</td>
</tr>
</table>
संदेश प्रारूप:

```
+----+----+----+----+----+----+----+----+
|size|     Alice IP      | Port (A)|size|
+----+----+----+----+----+----+----+----+
|      that many bytes of challenge     |
+                                       +
|        data relayed from Alice        |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
वर्तमान कार्यान्वयन में header सहित सामान्य आकार: 48 bytes (non-mod-16 padding से पहले)

#### नोट्स

- IPv4 के लिए, Alice का IP address हमेशा 4 bytes का होता है, क्योंकि Alice IPv4 के माध्यम से Charlie से कनेक्ट करने की कोशिश कर रही है।
  Release 0.9.50 के रूप में, IPv6 समर्थित है, और Alice का IP address 16 bytes का हो सकता है।
- IPv4 के लिए, यह message एक स्थापित IPv4 connection के माध्यम से भेजा जाना चाहिए,
  क्योंकि यही एकमात्र तरीका है जिससे Bob को Charlie का IPv4 address पता चलता है ताकि वह RelayResponse में Alice को वापस कर सके।
  Release 0.9.50 के रूप में, IPv6 समर्थित है, और यह message एक स्थापित IPv6 connection के माध्यम से भेजा जा सकता है।
- Release 0.9.50 के रूप में, introducers के साथ प्रकाशित किसी भी SSU address में "caps" विकल्प में "4" या "6" होना चाहिए।
- Challenge अनुपलब्ध है, challenge का आकार हमेशा शून्य होता है
- Header में विस्तृत विकल्प: अपेक्षित नहीं, अपरिभाषित।

### डेटा (प्रकार 6) {#data}

यह संदेश डेटा परिवहन और पुष्टिकरण के लिए उपयोग किया जाता है।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
**डेटा:** 1 बाइट flags (नीचे देखें); यदि explicit ACKs शामिल हैं: 1 बाइट ACKs की संख्या, उतने 4 बाइट MessageIds जो पूर्ण रूप से ACK हैं; यदि ACK bitfields शामिल हैं: 1 बाइट ACK bitfields की संख्या, उतने 4 बाइट MessageIds + 1 या अधिक बाइट ACK bitfield (नोट्स देखें); यदि extended data शामिल है: 1 बाइट डेटा साइज़, उतने बाइट्स का extended data (वर्तमान में अनुवादित नहीं); 1 बाइट fragments की संख्या (शून्य हो सकती है); यदि शून्य नहीं, तो उतने message fragments।

```
Flags byte:
  Bit order: 76543210 (bit 7 is MSB)
  bit 7: explicit ACKs included
  bit 6: ACK bitfields included
  bit 5: reserved
  bit 4: explicit congestion notification (ECN)
  bit 3: request previous ACKs
  bit 2: want reply
  bit 1: extended data included (unused, never set)
  bit 0: reserved
```
प्रत्येक fragment में शामिल है: - 4 byte messageId - 3 byte fragment info:   - bits 23-17: fragment # 0 - 127   - bit 16: isLast (1 = true)   - bits 15-14: अप्रयुक्त, भविष्य के उपयोग के साथ संगतता के लिए 0 पर सेट करें   - bits 13-0: fragment size 0 - 16383 - fragment data के उतने bytes

संदेश प्रारूप:

```
+----+----+----+----+----+----+----+----+
|flag| (additional headers, determined  |
+----+                                  +
~ by the flags, such as ACKs or         ~
| bitfields                             |
+----+----+----+----+----+----+----+----+
|#frg|     messageId     |   frag info  |
+----+----+----+----+----+----+----+----+
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
#### ACK Bitfield टिप्पणियां

bitfield प्रत्येक byte के 7 निम्न bits का उपयोग करता है, जिसमें उच्च bit यह निर्दिष्ट करता है कि कोई अतिरिक्त bitfield byte इसके बाद आता है या नहीं (1 = true, 0 = वर्तमान bitfield byte अंतिम है)। 7 bit arrays का यह sequence दर्शाता है कि कोई fragment प्राप्त हुआ है या नहीं - यदि कोई bit 1 है, तो fragment प्राप्त हो गया है। स्पष्ट करने के लिए, मान लेते हैं कि fragments 0, 2, 5, और 9 प्राप्त हो गए हैं, तो bitfield bytes इस प्रकार होंगे:

```
byte 0:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 1 (further bitfield bytes follow)
   bit 6: 0 (fragment 6 not received)
   bit 5: 1 (fragment 5 received)
   bit 4: 0 (fragment 4 not received)
   bit 3: 0 (fragment 3 not received)
   bit 2: 1 (fragment 2 received)
   bit 1: 0 (fragment 1 not received)
   bit 0: 1 (fragment 0 received)
byte 1:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 0 (no further bitfield bytes)
   bit 6: 0 (fragment 13 not received)
   bit 5: 0 (fragment 12 not received)
   bit 4: 0 (fragment 11 not received)
   bit 3: 0 (fragment 10 not received)
   bit 2: 1 (fragment 9 received)
   bit 1: 0 (fragment 8 not received)
   bit 0: 0 (fragment 7 not received)
```
#### नोट्स

- वर्तमान implementation पहले से ack किए गए messages के लिए सीमित संख्या में duplicate acks जोड़ती है, यदि स्थान उपलब्ध है।
- यदि fragments की संख्या शून्य है, तो यह एक ack-only या keepalive message है।
- ECN feature unimplemented है, और bit कभी set नहीं होता।
- वर्तमान implementation में, want reply bit तब set होता है जब fragments की संख्या शून्य से अधिक होती है, और जब कोई fragments नहीं होते तो set नहीं होता।
- Extended data unimplemented है और कभी उपस्थित नहीं होता।
- Multiple fragments का reception सभी releases में supported है। Multiple fragments का transmission release 0.9.16 में implemented है।
- जैसा कि वर्तमान में implemented है, maximum fragments 64 है (maximum fragment number = 63)।
- जैसा कि वर्तमान में implemented है, maximum fragment size निश्चित रूप से MTU से कम है।
- सावधान रहें कि maximum MTU को exceed न करें भले ही भेजने के लिए बड़ी संख्या में ACKs हों।
- Protocol zero-length fragments की अनुमति देता है लेकिन उन्हें भेजने का कोई कारण नहीं है।
- SSU में, data एक छोटा 5-byte I2NP header उपयोग करता है जिसके बाद I2NP message का payload होता है, standard 16-byte I2NP header के बजाय। छोटे I2NP header में केवल one-byte I2NP type और seconds में 4-byte expiration होता है। I2NP message ID को fragment के लिए message ID के रूप में उपयोग किया जाता है। I2NP size को fragment sizes से assemble किया जाता है। I2NP checksum आवश्यक नहीं है क्योंकि UDP message integrity decryption द्वारा सुनिश्चित की जाती है।
- Message IDs sequence numbers नहीं हैं और consecutive नहीं हैं। SSU in-order delivery की गारंटी नहीं देता। जबकि हम I2NP message ID को SSU message ID के रूप में उपयोग करते हैं, SSU protocol के नजरिए से, ये random numbers हैं। वास्तव में, चूंकि router सभी peers के लिए एक single Bloom filter उपयोग करता है, message ID एक वास्तविक random number होना चाहिए।
- क्योंकि कोई sequence numbers नहीं हैं, इसलिए यह सुनिश्चित करने का कोई तरीका नहीं है कि ACK प्राप्त हुआ था। वर्तमान implementation नियमित रूप से बड़ी मात्रा में duplicate ACKs भेजती है। Duplicate ACKs को congestion का संकेत नहीं माना जाना चाहिए।
- ACK Bitfield नोट्स: Data packet का receiver नहीं जानता कि message में कितने fragments हैं जब तक कि उसे last fragment प्राप्त न हो। इसलिए, response में भेजे गए bitfield bytes की संख्या fragments की संख्या को 7 से विभाजित करने से कम या अधिक हो सकती है। उदाहरण के लिए, यदि receiver द्वारा देखा गया सबसे ऊंचा fragment number 4 है, तो केवल एक byte भेजना आवश्यक है, भले ही कुल 13 fragments हो सकते हों। प्रत्येक message ID acked के लिए 10 bytes तक (यानी (64 / 7) + 1) शामिल किए जा सकते हैं।
- Header में extended options: अपेक्षित नहीं, undefined।

### PeerTest (प्रकार 7) {#peertest}

विवरण के लिए [SSU Peer Testing](/docs/transport/ssu/#peerTesting) देखें। नोट: IPv6 peer testing रिलीज़ 0.9.27 से समर्थित है।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte nonce; 1 byte IP address size (may be zero); that many byte representation of Alice's IP address, if size > 0; 2 byte Alice's port number; Alice's or Charlie's 32-byte introduction key; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
</table>
उपयोग की गई Crypto Key (घटित होने के क्रम में सूचीबद्ध): 1. जब Alice से Bob को भेजा जाता है: Alice/Bob sessionKey 2. जब Bob से Charlie को भेजा जाता है: Bob/Charlie sessionKey 3. जब Charlie से Bob को भेजा जाता है: Bob/Charlie sessionKey 4. जब Bob से Alice को भेजा जाता है: Alice/Bob sessionKey (या 0.9.52 से पहले के Bob के लिए, Alice का introKey) 5. जब Charlie से Alice को भेजा जाता है: Alice का introKey, जैसा कि Bob से PeerTest संदेश में प्राप्त हुआ था 6. जब Alice से Charlie को भेजा जाता है: Charlie का introKey, जैसा कि Charlie से PeerTest संदेश में प्राप्त हुआ था

MAC Key का उपयोग (घटना के क्रम में सूचीबद्ध): 1. जब Alice से Bob को भेजा गया: Alice/Bob MAC Key 2. जब Bob से Charlie को भेजा गया: Bob/Charlie MAC Key 3. जब Charlie से Bob को भेजा गया: Bob/Charlie MAC Key 4. जब Bob से Alice को भेजा गया: Alice का introKey, जैसा कि Alice से PeerTest message में प्राप्त हुआ 5. जब Charlie से Alice को भेजा गया: Alice का introKey, जैसा कि Bob से PeerTest message में प्राप्त हुआ 6. जब Alice से Charlie को भेजा गया: Charlie का introKey, जैसा कि Charlie से PeerTest message में प्राप्त हुआ

संदेश प्रारूप:

```
+----+----+----+----+----+----+----+----+
|    test nonce     |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|                        |
+----+----+----+                        +
| Alice or Charlie's                    |
+ introduction key (Alice's is sent to  +
| Bob and Charlie, while Charlie's is   |
+ sent to Alice)                        +
|                                       |
+              +----+----+----+----+----+
|              | arbitrary amount of    |
+----+----+----+                        |
| uninterpreted data                    |
~                .  .  .                ~
```
वर्तमान implementation में header सहित सामान्य आकार: 80 bytes (non-mod-16 padding से पहले)

#### नोट्स

- जब Alice द्वारा भेजा जाता है, IP address का आकार 0 होता है, IP address मौजूद नहीं होता, और port
  0 होता है, क्योंकि Bob और Charlie डेटा का उपयोग नहीं करते; बात यह है कि Alice का
  वास्तविक IP address/port निर्धारित करना और Alice को बताना; Bob और Charlie को परवाह नहीं है कि
  Alice अपना address क्या समझती है।
- जब Bob या Charlie द्वारा भेजा जाता है, IP और port मौजूद होते हैं, और IP address
  4 या 16 bytes का होता है। Release 0.9.27 के अनुसार IPv6 testing समर्थित है।
- जब Charlie द्वारा Alice को भेजा जाता है, IP और port निम्नलिखित हैं:
  पहली बार (message 5): Alice का अनुरोधित IP और port जैसा message 2 में प्राप्त हुआ।
  दूसरी बार (message 7): Alice का वास्तविक IP और port जिससे message 6 प्राप्त हुआ था।
- IPv6 नोट्स: Release 0.9.26 तक, केवल IPv4 addresses की testing समर्थित है। इसलिए, सभी
  Alice-Bob और Alice-Charlie संचार IPv4 के माध्यम से होना चाहिए। Bob-Charlie
  संचार, हालांकि, IPv4 या IPv6 के माध्यम से हो सकता है। Alice का address, जब
  PeerTest message में निर्दिष्ट हो, 4 bytes का होना चाहिए।
  Release 0.9.27 के अनुसार, IPv6 addresses की testing समर्थित है,
  और Alice-Bob और Alice-Charlie संचार IPv6 के माध्यम से हो सकता है,
  यदि Bob और Charlie अपने प्रकाशित IPv6 address में 'B' capability के साथ समर्थन दिखाते हैं।
  विवरण के लिए Proposal 126 देखें।
- Alice उस transport (IPv4 या IPv6) पर मौजूदा session का उपयोग करके Bob को अनुरोध भेजती है जिसे वह test करना चाहती है।
  जब Bob को Alice से IPv4 के माध्यम से अनुरोध प्राप्त होता है, Bob को ऐसा Charlie चुनना चाहिए जो IPv4 address advertise करता हो।
  जब Bob को Alice से IPv6 के माध्यम से अनुरोध प्राप्त होता है, Bob को ऐसा Charlie चुनना चाहिए जो IPv6 address advertise करता हो।
  वास्तविक Bob-Charlie संचार IPv4 या IPv6 के माध्यम से हो सकता है (यानी, Alice के address type से स्वतंत्र)।
- एक peer को सक्रिय test states (nonces) की तालिका बनाए रखनी चाहिए। PeerTest message के
  प्राप्त होने पर, तालिका में nonce को देखें। यदि मिल जाता है, तो यह मौजूदा
  test है और आप अपनी भूमिका जानते हैं (Alice, Bob, या Charlie)। अन्यथा, यदि
  IP मौजूद नहीं है और port 0 है, तो यह नया test है और आप Bob हैं।
  अन्यथा, यह नया test है और आप Charlie हैं।
- Release 0.9.15 के अनुसार, Alice का Bob के साथ established session होना चाहिए और उसे session key का
  उपयोग करना चाहिए।
- API version 0.9.52 से पहले, कुछ implementations में, Bob ने Alice को
  Alice/Bob session key के बजाय Alice की intro key का उपयोग करके जवाब दिया, भले ही
  Alice और Bob का established session हो (0.9.15 से)।
  API version 0.9.52 के अनुसार, Bob सभी implementations में session key का सही
  उपयोग करेगा, और Alice को Bob से प्राप्त message को Alice की intro key के साथ
  अस्वीकार करना चाहिए यदि Bob API version 0.9.52 या उससे ऊपर है।
- Header में extended options: अपेक्षित नहीं, अपरिभाषित।

### HolePunch {#holepunch}

HolePunch केवल एक UDP पैकेट है जिसमें कोई डेटा नहीं होता। यह अप्रमाणित और अनएन्क्रिप्टेड होता है। इसमें SSU हेडर नहीं होता, इसलिए इसमें कोई मैसेज टाइप नंबर नहीं होता। यह Introduction अनुक्रम के भाग के रूप में Charlie से Alice को भेजा जाता है।

## नमूना डेटाग्राम {#sampledatagrams}

### न्यूनतम डेटा संदेश

- कोई fragments नहीं, कोई ACKs नहीं, कोई NACKs नहीं, आदि
- Size: 39 bytes

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|    |
+----+----+----+----+----+----+----+    +
|  padding to fit a full AES256 block   |
+----+----+----+----+----+----+----+----+
```
### payload के साथ न्यूनतम डेटा संदेश

- आकार: 46+fragmentSize bytes

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|
+----+----+----+----+----+----+----+----+
  messageId    |   frag info  |         |
----+----+----+----+----+----+         +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
```
## संदर्भ

- [AES Encryption](/docs/specs/cryptography/#AES)
- [Common Structures Specification](/docs/specs/common-structures/)
- [Date](/docs/specs/common-structures/#date)
- [ElGamal Encryption](/docs/specs/cryptography/#elgamal)
- [HMAC Details](/docs/specs/cryptography/#udp)
- [I2P Source](https://github.com/i2p/i2p.i2p)
- [i2pd Source](https://github.com/PurpleI2P/i2pd)
- [KeyCertificate](/docs/specs/common-structures/#key-certificates)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SessionKey](/docs/specs/common-structures/#sessionkey)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [SSU Overview](/docs/transport/ssu/)
- [SSU Keys](/docs/transport/ssu/#keys)
- [SSU Peer Testing](/docs/transport/ssu/#peerTesting)
