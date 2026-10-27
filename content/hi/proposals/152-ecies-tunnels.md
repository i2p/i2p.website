---
title: "ECIES टनल"
aliases:
  - "/hi/proposals/152-ecies-config"
  - "/hi/proposals/152-ecies-config/"
  - "/hi/proposals/152"
  - "/hi/proposals/152/"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "बंद"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
toc: true
---

## नोट

नेटवर्क deployment और testing प्रगति में है। मामूली संशोधनों के अधीन। आधिकारिक specification के लिए [SPEC](/docs/specs/tunnel-implementation/) देखें।

## अवलोकन

यह दस्तावेज़ [ECIES-X25519](/docs/specs/ecies/) द्वारा प्रस्तुत crypto primitives का उपयोग करके Tunnel Build message encryption में परिवर्तनों का प्रस्ताव करता है। यह router को ElGamal से ECIES-X25519 keys में परिवर्तित करने के लिए समग्र प्रस्ताव [Proposal 156](/proposals/156-ecies-routers) का एक भाग है।

नेटवर्क को ElGamal + AES256 से ECIES + ChaCha20 में संक्रमित करने के उद्देश्य से, मिश्रित ElGamal और ECIES router वाली tunnel आवश्यक हैं। मिश्रित tunnel hop को संभालने के लिए विशिष्टताएं प्रदान की गई हैं। ElGamal hop के प्रारूप, प्रसंस्करण, या एन्क्रिप्शन में कोई परिवर्तन नहीं किया जाएगा।

ElGamal tunnel creators को प्रति-hop अस्थायी X25519 keypairs बनाने होंगे, और ECIES hops वाले tunnels बनाने के लिए इस spec का पालन करना होगा।

यह proposal ECIES-X25519 tunnel building के लिए आवश्यक परिवर्तनों को निर्दिष्ट करता है। ECIES routers के लिए आवश्यक सभी परिवर्तनों के अवलोकन के लिए, proposal 156 [Proposal 156](/proposals/156-ecies-routers) देखें।

यह प्रस्ताव tunnel build records के लिए समान आकार बनाए रखता है, जैसा कि compatibility के लिए आवश्यक है। छोटे build records और messages बाद में लागू किए जाएंगे - देखें [Proposal 157](/proposals/157-new-tbm)।

### Cryptographic Primitives

कोई नया cryptographic primitives नहीं शामिल किया गया है। इस प्रस्ताव को लागू करने के लिए आवश्यक primitives हैं:

- AES-256-CBC जैसा कि [Cryptography](/docs/specs/cryptography/) में है
- STREAM ChaCha20/Poly1305 functions:
  ENCRYPT(k, n, plaintext, ad) और DECRYPT(k, n, ciphertext, ad) - जैसा कि [NTCP2](/docs/specs/ntcp2/) [ECIES-X25519](/docs/specs/ecies/) और [RFC-7539](https://tools.ietf.org/html/rfc7539) में है
- X25519 DH functions - जैसा कि [NTCP2](/docs/specs/ntcp2/) और [ECIES-X25519](/docs/specs/ecies/) में है
- HKDF(salt, ikm, info, n) - जैसा कि [NTCP2](/docs/specs/ntcp2/) और [ECIES-X25519](/docs/specs/ecies/) में है

अन्य Noise functions जो कहीं और परिभाषित हैं:

- MixHash(d) - जैसा कि [NTCP2](/docs/specs/ntcp2/) और [ECIES-X25519](/docs/specs/ecies/) में है
- MixKey(d) - जैसा कि [NTCP2](/docs/specs/ntcp2/) और [ECIES-X25519](/docs/specs/ecies/) में है

### Goals

- crypto operations की गति बढ़ाना
- tunnel BuildRequestRecords और BuildReplyRecords के लिए ElGamal + AES256/CBC को ECIES primitives से बदलना
- संगतता के लिए encrypted BuildRequestRecords और BuildReplyRecords का size (528 bytes) में कोई परिवर्तन नहीं
- कोई नया I2NP messages नहीं
- संगतता के लिए encrypted build record size बनाए रखना
- Tunnel Build Messages के लिए forward secrecy जोड़ना
- authenticated encryption जोड़ना
- hops को BuildRequestRecords को reorder करने का पता लगाना
- timestamp की resolution बढ़ाना ताकि Bloom filter का size कम किया जा सके
- tunnel expiration के लिए field जोड़ना ताकि विभिन्न tunnel lifetimes संभव हो सकें (केवल all-ECIES tunnels)
- भविष्य की features के लिए extensible options field जोड़ना
- मौजूदा cryptographic primitives का पुन: उपयोग
- संगतता बनाए रखते हुए जहाँ संभव हो tunnel build message security में सुधार
- mixed ElGamal/ECIES peers के साथ tunnels का समर्थन
- build messages पर "tagging" attacks के विरुद्ध सुरक्षा में सुधार
- Hops को build message को process करने से पहले अगली hop के encryption type को जानने की आवश्यकता नहीं है,
  क्योंकि उस समय उनके पास अगली hop का RI नहीं हो सकता
- वर्तमान network के साथ अधिकतम संगतता
- ElGamal routers के लिए tunnel build AES request/reply encryption में कोई परिवर्तन नहीं
- tunnel AES "layer" encryption में कोई परिवर्तन नहीं, इसके लिए देखें [Proposal 153](/proposals/153-chacha20-layer-encryption)
- दोनों 8-record TBM/TBRM और variable-size VTBM/VTBRM का समर्थन जारी रखना
- पूरे network के लिए "flag day" upgrade की आवश्यकता नहीं

### क्रिप्टोग्राफिक प्रिमिटिव्स

- tunnel build संदेशों का पूर्ण पुनर्डिज़ाइन जिसके लिए एक "flag day" की आवश्यकता है।
- tunnel build संदेशों को छोटा करना (सभी ECIES hops और एक नए proposal की आवश्यकता)
- tunnel build विकल्पों का उपयोग जैसा कि [Proposal 143](/proposals/143-build-message-options) में परिभाषित है, केवल छोटे संदेशों के लिए आवश्यक
- Bidirectional tunnels - इसके लिए देखें [Proposal 119](/proposals/119-bidirectional-tunnels)
- छोटे tunnel build संदेश - इसके लिए देखें [Proposal 157](/proposals/157-new-tbm)

## Threat Model

### लक्ष्य

- कोई भी hop tunnel के originator को निर्धारित नहीं कर सकता।

- Middle hops को tunnel की दिशा या tunnel में उनकी स्थिति निर्धारित करने में सक्षम नहीं होना चाहिए।

- कोई भी hop अन्य request या reply records की कोई भी contents को पढ़ नहीं सकता, सिवाय अगले hop के लिए truncated router hash और ephemeral key के

- आउटबाउंड बिल्ड के लिए reply tunnel का कोई भी सदस्य किसी भी reply records को नहीं पढ़ सकता।

- आउटबाउंड tunnel का कोई भी सदस्य inbound build के लिए किसी भी request records को नहीं पढ़ सकता,
  इस अपवाद के साथ कि OBEP truncated router hash और IBGW के लिए ephemeral key देख सकता है

### गैर-लक्ष्य

tunnel निर्माण डिज़ाइन का एक मुख्य लक्ष्य सहयोगी routers X और Y के लिए यह जानना कठिन बनाना है कि वे एक ही tunnel में हैं। यदि router X hop m पर है और router Y hop m+1 पर है, तो वे स्पष्ट रूप से जान जाएंगे। लेकिन यदि router X hop m पर है और router Y hop m+n पर है जहाँ n>1 है, तो यह काफी कठिन होना चाहिए।

Tagging attacks वे हैं जहाँ middle-hop router X tunnel build message को इस तरह बदल देता है कि router Y उस alteration को detect कर सके जब build message वहाँ पहुँचता है। लक्ष्य यह है कि कोई भी altered message को X और Y के बीच किसी router द्वारा drop कर दिया जाए इससे पहले कि वह router Y तक पहुँचे। उन modifications के लिए जो router Y से पहले drop नहीं होतीं, tunnel creator को reply में corruption को detect करना चाहिए और tunnel को discard करना चाहिए।

संभावित हमले:

- एक बिल्ड रिकॉर्ड को बदलें
- एक बिल्ड रिकॉर्ड को बदलें
- एक बिल्ड रिकॉर्ड जोड़ें या हटाएं
- बिल्ड रिकॉर्ड्स को पुनः क्रमित करें

TODO: क्या वर्तमान डिज़ाइन इन सभी हमलों को रोकता है?

## Design

### Noise Protocol Framework

यह प्रस्ताव Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (संशोधन 34, 2018-07-11) पर आधारित आवश्यकताएं प्रदान करता है। Noise की भाषा में, Alice प्रारंभकर्ता है, और Bob उत्तरदाता है।

यह प्रस्ताव Noise protocol Noise_N_25519_ChaChaPoly_SHA256 पर आधारित है। यह Noise protocol निम्नलिखित primitives का उपयोग करता है:

- One-Way Handshake Pattern: N
  Alice अपनी static key को Bob को transmit नहीं करती है (N)

- DH Function: X25519
  X25519 DH जिसमें 32 बाइट्स की key length है जैसा कि [RFC-7748](https://tools.ietf.org/html/rfc7748) में निर्दिष्ट है।

- Cipher Function: ChaChaPoly
  AEAD_CHACHA20_POLY1305 जैसा कि [RFC-7539](https://tools.ietf.org/html/rfc7539) section 2.8 में निर्दिष्ट है।
  12 byte nonce, जिसके पहले 4 bytes शून्य पर सेट हैं।
  [NTCP2](/docs/specs/ntcp2/) के समान।

- Hash Function: SHA256
  मानक 32-बाइट hash, जो पहले से ही I2P में व्यापक रूप से उपयोग किया जाता है।

#### Additions to the Framework

कोई नहीं।

### डिज़ाइन लक्ष्य

हैंडशेक [Noise](https://noiseprotocol.org/noise.html) हैंडशेक पैटर्न का उपयोग करते हैं।

निम्नलिखित अक्षर मैपिंग का उपयोग किया जाता है:

- e = एक-बार उपयोग की इफेमेरल key
- s = static key
- p = संदेश payload

बिल्ड रिक्वेस्ट Noise N pattern के समान है। यह [NTCP2](/docs/specs/ntcp2/) में उपयोग किए गए XK pattern के पहले (Session Request) संदेश के भी समान है।

```text
<- s
  ...
  e es p ->
```
### टैगिंग अटैक

Build request records tunnel creator द्वारा बनाए जाते हैं और व्यक्तिगत hop के लिए asymmetrically encrypted होते हैं। Request records की यह asymmetric encryption वर्तमान में ElGamal है जैसा कि [Cryptography](/docs/specs/cryptography/) में परिभाषित है और इसमें SHA-256 checksum शामिल है। यह design forward-secret नहीं है।

नया डिज़ाइन one-way Noise pattern "N" का उपयोग करेगा जो ECIES-X25519 ephemeral-static DH के साथ है, एक HKDF के साथ, और forward secrecy, integrity, और authentication के लिए ChaCha20/Poly1305 AEAD के साथ। Alice tunnel build requestor है। tunnel में प्रत्येक hop एक Bob है।

(Payload Security Properties)

```text
N:                      Authentication   Confidentiality
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
### Reply encryption

Build reply records को hops creator द्वारा बनाया जाता है और creator के लिए symmetrically encrypted किया जाता है। Reply records का यह symmetric encryption वर्तमान में AES है जिसमें एक prepended SHA-256 checksum होता है। और इसमें एक SHA-256 checksum शामिल होता है। यह design forward-secret नहीं है।

नया डिज़ाइन integrity और authentication के लिए ChaCha20/Poly1305 AEAD का उपयोग करेगा।

### Noise Protocol Framework

अनुरोध में ephemeral public key को AES या Elligator2 के साथ obfuscate करने की आवश्यकता नहीं है। पिछला hop ही एकमात्र है जो इसे देख सकता है, और वह hop जानता है कि अगला hop ECIES है।

Reply records को किसी अन्य DH के साथ पूर्ण asymmetric encryption की आवश्यकता नहीं होती है।

## Specification

### Build Request Records

एन्क्रिप्टेड BuildRequestRecords संगतता के लिए ElGamal और ECIES दोनों के लिए 528 बाइट्स हैं।

#### Request Record Unencrypted (ElGamal)

संदर्भ के लिए, यह ElGamal routers के लिए tunnel BuildRequestRecord की वर्तमान specification है, जो [I2NP](/docs/specs/i2np/) से ली गई है। अनएन्क्रिप्टेड डेटा को एक nonzero byte और encryption से पहले डेटा के SHA-256 hash के साथ prepend किया जाता है, जैसा कि [Cryptography](/docs/specs/cryptography/) में परिभाषित है।

सभी फ़ील्ड big-endian हैं।

अनएन्क्रिप्टेड आकार: 222 bytes

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes    4-35: local router identity hash
  bytes   36-39: next tunnel ID, nonzero
  bytes   40-71: next router identity hash
  bytes  72-103: AES-256 tunnel layer key
  bytes 104-135: AES-256 tunnel IV key
  bytes 136-167: AES-256 reply key
  bytes 168-183: AES-256 reply IV
  byte      184: flags
  bytes 185-188: request time (in hours since the epoch, rounded down)
  bytes 189-192: next message ID
  bytes 193-221: uninterpreted / random padding
```
#### Request Record Encrypted (ElGamal)

संदर्भ के लिए, यह ElGamal routers के लिए tunnel BuildRequestRecord की वर्तमान specification है, जो [I2NP](/docs/specs/i2np/) से ली गई है।

एन्क्रिप्टेड साइज़: 528 bytes

```text
bytes    0-15: Hop's truncated identity hash
  bytes  16-528: ElGamal encrypted BuildRequestRecord
```
#### Request Record Unencrypted (ECIES)

यह ECIES-X25519 routers के लिए tunnel BuildRequestRecord की प्रस्तावित specification है। बदलावों का सारांश:

- अप्रयुक्त 32-byte router hash को हटाएं
- अनुरोध समय को घंटों से मिनटों में बदलें
- भविष्य के variable tunnel time के लिए expiration field जोड़ें
- flags के लिए अधिक स्थान जोड़ें
- अतिरिक्त build options के लिए Mapping जोड़ें
- AES-256 reply key और IV का उपयोग hop के अपने reply record के लिए नहीं किया जाता
- Unencrypted record लंबा है क्योंकि कम encryption overhead है

अनुरोध रिकॉर्ड में कोई ChaCha reply keys नहीं हैं। वे keys एक KDF से व्युत्पन्न होती हैं। नीचे देखें।

सभी फील्ड big-endian हैं।

अनएन्क्रिप्टेड आकार: 464 bytes

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes     4-7: next tunnel ID, nonzero
  bytes    8-39: next router identity hash
  bytes   40-71: AES-256 tunnel layer key
  bytes  72-103: AES-256 tunnel IV key
  bytes 104-135: AES-256 reply key
  bytes 136-151: AES-256 reply IV
  byte      152: flags
  bytes 153-155: more flags, unused, set to 0 for compatibility
  bytes 156-159: request time (in minutes since the epoch, rounded down)
  bytes 160-163: request expiration (in seconds since creation)
  bytes 164-167: next message ID
  bytes   168-x: tunnel build options (Mapping)
  bytes     x-x: other data as implied by flags or options
  bytes   x-463: random padding
```
flags फील्ड वही है जो [Tunnel Creation](/docs/specs/tunnel-implementation/) में परिभाषित है और इसमें निम्नलिखित शामिल है::

```text
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
Bit order: 76543210 (bit 7 MSB है)  bit 7: यदि सेट है, तो किसी से भी संदेश की अनुमति दें  bit 6: यदि सेट है, तो किसी को भी संदेश की अनुमति दें, और उत्तर को भेजें

bits 5-0: अपरिभाषित, भविष्य के विकल्पों के साथ संगतता के लिए 0 पर सेट करना आवश्यक है

बिट 7 इंगित करता है कि hop एक inbound gateway (IBGW) होगा। बिट 6 इंगित करता है कि hop एक outbound endpoint (OBEP) होगा। यदि कोई भी बिट सेट नहीं है, तो hop एक intermediate participant होगा। दोनों एक साथ सेट नहीं हो सकते।

#### Request Record Encrypted (ECIES)

अनुरोध की समाप्ति भविष्य के परिवर्तनीय tunnel अवधि के लिए है। अभी के लिए, केवल समर्थित मान 600 (10 मिनट) है।

tunnel build विकल्प एक Mapping संरचना है जैसा कि [Common Structures](/docs/specs/common-structures/) में परिभाषित है। यह भविष्य के उपयोग के लिए है। वर्तमान में कोई विकल्प परिभाषित नहीं हैं। यदि Mapping संरचना खाली है, तो यह दो bytes 0x00 0x00 है। Mapping का अधिकतम आकार (length field सहित) 296 bytes है, और Mapping length field का अधिकतम मान 294 है।

```text
bytes    0-15: Hop's truncated identity hash
  bytes   16-47: Sender's ephemeral X25519 public key
  bytes  48-511: ChaCha20 encrypted BuildRequestRecord
  bytes 512-527: Poly1305 MAC
```
### हैंडशेक पैटर्न

सभी फ़ील्ड big-endian हैं सिवाय ephemeral public key के जो little-endian है।

#### Reply Record Unencrypted (ElGamal)

एन्क्रिप्टेड साइज़: 528 bytes

एन्क्रिप्टेड BuildReplyRecords ElGamal और ECIES दोनों के लिए संगतता हेतु 528 बाइट्स के होते हैं।

ElGamal उत्तर AES के साथ एन्क्रिप्ट किए जाते हैं।

```text
bytes   0-31: SHA-256 Hash of bytes 32-527
  bytes 32-526: random data
  byte     527: reply

  total length: 528
```
#### Reply Record Unencrypted (ECIES)

सभी फील्ड big-endian हैं।

- बिल्ड रिप्लाई विकल्पों के लिए मैपिंग जोड़ें
- अनएन्क्रिप्टेड रिकॉर्ड लंबा है क्योंकि कम एन्क्रिप्शन ओवरहेड होता है

अनएन्क्रिप्टेड साइज़: 528 bytes

यह ECIES-X25519 routers के लिए tunnel BuildReplyRecord का प्रस्तावित विनिर्देश है। परिवर्तनों का सारांश:

ECIES replies ChaCha20/Poly1305 के साथ encrypt किए जाते हैं।

```text
bytes    0-x: Tunnel Build Reply Options (Mapping)
  bytes    x-x: other data as implied by options
  bytes  x-510: Random padding
  byte     511: Reply byte
```
सभी फ़ील्ड big-endian हैं।

अनएन्क्रिप्टेड आकार: 512 bytes

- 0x00 (स्वीकार करें)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Reply Record Encrypted (ECIES)

tunnel build reply options एक Mapping structure है जैसा कि [Common Structures](/docs/specs/common-structures/) में परिभाषित है। यह भविष्य के उपयोग के लिए है। वर्तमान में कोई options परिभाषित नहीं हैं। यदि Mapping structure खाली है, तो यह दो bytes 0x00 0x00 है। Mapping का अधिकतम आकार (length field सहित) 511 bytes है, और Mapping length field का अधिकतम मान 509 है।

```text
bytes   0-511: ChaCha20 encrypted BuildReplyRecord
  bytes 512-527: Poly1305 MAC
```
Reply byte निम्नलिखित values में से एक है जो [Tunnel Creation](/docs/specs/tunnel-implementation/) में defined है fingerprinting से बचने के लिए:

### अनुरोध एन्क्रिप्शन

एन्क्रिप्टेड साइज़: 528 bytes

ECIES records में पूर्ण संक्रमण के बाद, ranged padding नियम request records के समान ही हैं।

- "encryption":

- cipher डिक्रिप्शन मोड में चलाया जाता है
- request records को preprocessing में पूर्व-निर्धारित रूप से decrypt किया जाता है (encrypted request records को छुपाते हुए)

- "decryption":

- cipher एन्क्रिप्शन मोड में चलाया जाता है
- प्रतिभागी hops द्वारा एन्क्रिप्ट किए गए request records (अगले plaintext request record को प्रकट करते हुए)

- ChaCha20 में "modes" नहीं होते हैं, इसलिए इसे केवल तीन बार चलाया जाता है:

- एक बार preprocessing में
- एक बार hop द्वारा
- एक बार final reply processing पर

मिश्रित tunnels की अनुमति है, और ElGamal से ECIES में संक्रमण के लिए आवश्यक हैं। संक्रमणकालीन अवधि के दौरान, बढ़ती संख्या में routers को ECIES keys के तहत keyed किया जाएगा।

सममित क्रिप्टोग्राफी preprocessing उसी तरीके से चलेगी:

जब mixed tunnels का उपयोग किया जाता है, तो tunnel creators को BuildRequestRecord के symmetric encryption को current और previous hop के encryption type के आधार पर करना होगा।

प्रत्येक hop BuildReplyRecords को encrypt करने के लिए अपना स्वयं का encryption type उपयोग करेगा, और VariableTunnelBuildMessage (VTBM) में अन्य records के लिए भी।

- भेजने वाला (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

जवाबी पथ पर, endpoint (प्रेषक) को [Multiple Encryption](https://en.wikipedia.org/wiki/Multiple_encryption) को पूर्ववत करना होगा, प्रत्येक hop की reply key का उपयोग करते हुए।

एक स्पष्टीकरण उदाहरण के रूप में, आइए एक outbound tunnel को देखते हैं जो ECIES के साथ ElGamal से घिरा हुआ है:

सभी BuildRequestRecords अपनी एन्क्रिप्टेड स्थिति में हैं (ElGamal या ECIES का उपयोग करके)।

AES256/CBC cipher, जब उपयोग किया जाता है, अभी भी प्रत्येक record के लिए उपयोग किया जाता है, बिना कई records में chaining के।

- H3 का record "encrypted" है इसका उपयोग करके:

- H2 की reply key (ChaCha20)
- H1 की reply key (AES256/CBC)

- H2 का record "encrypted" है इसका उपयोग करके:

- H1 की reply key (AES256/CBC)

- H1 का रिकॉर्ड symmetric encryption के बिना बाहर जाता है

इसी तरह, ChaCha20 का उपयोग प्रत्येक record को encrypt करने के लिए किया जाएगा, पूरे VTBM में streaming के लिए नहीं।

अनुरोध रिकॉर्ड्स को Sender (OBGW) द्वारा प्रीप्रोसेस किया जाता है:

- H3 का रिकॉर्ड इसका उपयोग करके "decrypted" किया जाता है:

- H3 का reply key (AES256/CBC)

- H2 का record निम्नलिखित का उपयोग करके "decrypted" किया जाता है:

- H3 का reply key (AES256/CBC)
- H2 का reply key (ChaCha20-Poly1305)

- H1 का record "decrypt" किया जाता है इसका उपयोग करके:

- H3 की reply key (AES256/CBC)
- H2 की reply key (ChaCha20)
- H1 की reply key (AES256/CBC)

केवल H2 reply encryption flag की जांच करता है, और देखता है कि इसके बाद AES256/CBC है।

- H3 का record "encrypted" किया जाता है इसका उपयोग करके:

- H3 की reply key (AES256/CBC)

- H2 का रिकॉर्ड "encrypted" है इसका उपयोग करके:

- H3 की reply key (AES256/CBC)
- H2 की reply key (ChaCha20-Poly1305)

- H1 का रिकॉर्ड निम्नलिखित का उपयोग करके "encrypted" है:

- H3 की reply key (AES256/CBC)
- H2 की reply key (ChaCha20)
- H1 की reply key (AES256/CBC)

### उत्तर एन्क्रिप्शन

प्रत्येक hop द्वारा प्रोसेस किए जाने के बाद, records "decrypted" स्थिति में होते हैं:

tunnel creator, जिसे Inbound Endpoint (IBEP) भी कहा जाता है, reply को postprocess करता है:

#### KDF for Initial ck and h

ये keys स्पष्ट रूप से ElGamal BuildRequestRecords में शामिल की जाती हैं। ECIES BuildRequestRecords के लिए, tunnel keys और AES reply keys शामिल की जाती हैं, लेकिन ChaCha reply keys DH exchange से derive की जाती हैं। router static ECIES keys के विवरण के लिए [Proposal 156](/proposals/156-ecies-routers) देखें।

```text
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
#### KDF for Request Record

नीचे इस बात का विवरण है कि request records में पहले से भेजी गई keys को कैसे derive किया जाए।

यह pattern "N" के लिए मानक प्रोटोकॉल नाम के साथ मानक [NOISE](https://noiseprotocol.org/noise.html) है।

ElGamal tunnel creators प्रत्येक ECIES hop के लिए tunnel में एक ephemeral X25519 keypair generate करते हैं, और अपने BuildRequestRecord को encrypt करने के लिए उपरोक्त scheme का उपयोग करते हैं। ElGamal tunnel creators ElGamal hops को encrypt करने के लिए इस spec से पूर्व की scheme का उपयोग करेंगे।

ECIES tunnel creators को प्रत्येक ElGamal hop की public key के लिए [Tunnel Creation](/docs/specs/tunnel-implementation/) में परिभाषित scheme का उपयोग करके encrypt करना होगा। ECIES tunnel creators ECIES hops के लिए encrypt करने हेतु उपरोक्त scheme का उपयोग करेंगे।

इसका मतलब यह है कि tunnel hops केवल अपने समान encryption प्रकार के encrypted records को ही देख पाएंगे।

```text
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
ElGamal और ECIES tunnel creators के लिए, वे ECIES hops को encrypt करने के लिए प्रति-hop अद्वितीय ephemeral X25519 keypairs generate करेंगे।

### औचित्य

**महत्वपूर्ण**: Ephemeral keys प्रत्येक ECIES hop के लिए और प्रत्येक build record के लिए अद्वितीय होनी चाहिए। अद्वितीय keys का उपयोग न करना colluding hops के लिए एक attack vector खोलता है ताकि वे पुष्टि कर सकें कि वे एक ही tunnel में हैं।

### Reply Record Encryption (ECIES)

``replyKey``, ``layerKey`` और ``layerIV`` को अभी भी ElGamal records के अंदर शामिल किया जाना चाहिए, और इन्हें randomly generate किया जा सकता है।

```text
// AEAD parameters
  k = chainkey from build request
  n = 0
  plaintext = 512 byte build reply record
  ad = h from build request

  ciphertext = ENCRYPT(k, n, plaintext, ad)
```
### Build Request Records का निर्माण

जैसा कि [Tunnel Creation](/docs/specs/tunnel-implementation/) में परिभाषित है। ElGamal hops के लिए encryption में कोई बदलाव नहीं है।

### Security Analysis

reply record ChaCha20/Poly1305 encrypted है।

जैसा कि [Tunnel Creation](/docs/specs/tunnel-implementation/) में परिभाषित किया गया है। ElGamal hops के लिए एन्क्रिप्शन में कोई बदलाव नहीं हैं।

ElGamal, Tunnel Build Messages के लिए forward secrecy प्रदान नहीं करता है।

AES256/CBC की स्थिति थोड़ी बेहतर है, यह केवल एक ज्ञात plaintext `biclique` attack से सैद्धांतिक कमजोरी के लिए संवेदनशील है।

AES256/CBC के विरुद्ध एकमात्र ज्ञात व्यावहारिक हमला padding oracle attack है, जब IV आक्रमणकारी को ज्ञात हो।

एक आक्रमणकारी को AES256/CBC key की जानकारी (reply key और IV) प्राप्त करने के लिए अगले hop के ElGamal encryption को तोड़ना होगा।

ElGamal, ECIES की तुलना में काफी अधिक CPU-intensive है, जिससे संभावित resource exhaustion हो सकता है।

## खतरा मॉडल

ECIES, जो प्रति-BuildRequestRecord या VariableTunnelBuildMessage के लिए नई ephemeral keys के साथ उपयोग किया जाता है, forward-secrecy प्रदान करता है।

## Implementation Notes

* पुराने router encryption type की जांच नहीं करते और ElGamal-encrypted
  records भेजते हैं। कुछ हाल के router में bugs हैं और वे विभिन्न प्रकार के malformed records भेजते हैं।
  Implementers को इन records को DH operation से पहले detect और reject करना चाहिए
  यदि संभव हो, ताकि CPU usage कम हो सके।

## Issues

## डिज़ाइन

ChaCha20Poly1305 AEAD एन्क्रिप्शन प्रदान करता है, जो प्राप्तकर्ता को डिक्रिप्शन का प्रयास करने से पहले संदेश की अखंडता को सत्यापित करने की अनुमति देता है।

## संदर्भ

* [सामान्य](/docs/specs/common-structures/)
* [क्रिप्टोग्राफी](/docs/specs/cryptography/)
* [ECIES-X25519](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [NTCP2](/docs/specs/ntcp2/)
* [Prop119](/proposals/119-bidirectional-tunnels/)
* [Prop143](/proposals/143-build-message-options/)
* [Prop153](/proposals/153-chacha20-layer-encryption/)
* [Prop156](/proposals/156-ecies-routers/)
* [Prop157](/proposals/157-new-tbm/)
* [SPEC](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [Tunnel-Creation](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption)
* [RFC-7539](https://tools.ietf.org/html/rfc7539)
* [RFC-7748](https://tools.ietf.org/html/rfc7748)
