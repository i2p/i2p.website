---
title: "ECIES-X25519-AEAD-Ratchet"
description: "I2P end-to-end encryption के लिए Elliptic Curve Integrated Encryption Scheme"
slug: "ecies"
aliases:
  - "/hi/docs/specs/ecies-x25519-aead-ratchet"
  - "/hi/docs/specs/ecies-x25519-aead-ratchet/"
category: "प्रोटोकॉल"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
---

## नोट

नेटवर्क तैनाती पूर्ण। मामूली संशोधनों के अधीन। मूल प्रस्ताव के लिए [Prop144](/proposals/144-ecies-x25519/) देखें, जिसमें पृष्ठभूमि चर्चा और अतिरिक्त जानकारी शामिल है।

निम्नलिखित सुविधाएं 0.9.66 तक लागू नहीं की गई हैं:

- MessageNumbers, Options, और Termination blocks
- Protocol-layer responses
- Zero static key
- Multicast

इस प्रोटोकॉल के MLKEM PQ Hybrid संस्करण के लिए, देखें [ECIES-HYBRID](/docs/specs/ecies-hybrid/)।

## अवलोकन

यह ElGamal/AES+SessionTags [ElG-AES](/docs/specs/elgamal-aes/) को बदलने के लिए नया end-to-end encryption प्रोटोकॉल है।

यह निम्नलिखित पिछले कार्यों पर निर्भर करता है:

- Common structures spec [Common](/docs/specs/common-structures/)
- [I2NP](/docs/specs/i2np/) spec including LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/specs/elgamal-aes/)
- <http://zzz.i2p/topics/1768> नई असममित क्रिप्टो अवलोकन
- निम्न-स्तरीय क्रिप्टो अवलोकन [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- ECIES <http://zzz.i2p/topics/2418>
- [NTCP2](/docs/specs/ntcp2/) [Prop111](/proposals/111-ntcp2/)
- 123 New netDB Entries
- 142 New Crypto Template
- [Noise](https://noiseprotocol.org/noise.html) protocol
- [Signal](https://signal.org/docs/specifications/doubleratchet/) double ratchet algorithm

यह end-to-end, destination-to-destination संचार के लिए नई एन्क्रिप्शन का समर्थन करता है।

यह डिज़ाइन एक Noise handshake और data phase का उपयोग करता है जो Signal के double ratchet को शामिल करता है।

इस विनिर्देश में Signal और Noise के सभी संदर्भ केवल पृष्ठभूमि जानकारी के लिए हैं। इस विनिर्देश को समझने या लागू करने के लिए Signal और Noise प्रोटोकॉल की जानकारी आवश्यक नहीं है।

यह specification संस्करण 0.9.46 से समर्थित है।

## विशिष्टता

डिज़ाइन में Noise handshake और डेटा फेज़ का उपयोग है जिसमें Signal का double ratchet शामिल है।

### क्रिप्टोग्राफिक डिज़ाइन का सारांश

प्रोटोकॉल के पांच हिस्सों को फिर से डिज़ाइन करना है:

- 1\) नए और मौजूदा Session container formats को नए formats से बदल दिया जाता है।
- 2\) ElGamal (256 byte public keys, 128 byte private keys) को ECIES-X25519 (32 byte public और private keys) से बदला जाता है
- 3\) AES को AEAD_ChaCha20_Poly1305 (नीचे ChaChaPoly के रूप में संक्षिप्त) से बदला जाता है
- 4\) SessionTags को ratchets से बदला जाएगा, जो मूलतः एक cryptographic, synchronized PRNG है।
- 5\) AES payload, जैसा कि ElGamal/AES+SessionTags specification में परिभाषित है, को NTCP2 के समान एक block format से बदल दिया जाता है।

पांच बदलावों में से प्रत्येक का अपना अनुभाग नीचे दिया गया है।

### क्रिप्टो प्रकार

crypto type (LS2 में उपयोग किया गया) 4 है। यह एक little-endian 32-byte X25519 public key को दर्शाता है, और यहाँ निर्दिष्ट end-to-end protocol को।

Crypto type 0 ElGamal है। Crypto types 1-3 ECIES-ECDH-AES-SessionTag के लिए आरक्षित हैं, प्रस्ताव 145 [Prop145](/proposals/145-ecies-ecdh-aes/) देखें।

### Noise Protocol Framework

यह प्रोटोकॉल Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (संशोधन 34, 2018-07-11) पर आधारित आवश्यकताएं प्रदान करता है। Noise के गुण Station-To-Station protocol [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) के समान हैं, जो [SSU](/docs/transport/ssu/) प्रोटोकॉल का आधार है। Noise की भाषा में, Alice प्रारंभकर्ता है, और Bob उत्तरदाता है।

यह specification Noise protocol Noise_IK_25519_ChaChaPoly_SHA256 पर आधारित है। (प्रारंभिक key derivation function के लिए वास्तविक identifier "Noise_IKelg2_25519_ChaChaPoly_SHA256" है जो I2P extensions को दर्शाता है - नीचे KDF 1 section देखें) यह Noise protocol निम्नलिखित primitives का उपयोग करता है:

- Interactive Handshake Pattern: IK Alice तुरंत अपनी static key को Bob (I) को भेजती है Alice को पहले से ही Bob की static key पता है (K)
- One-Way Handshake Pattern: N Alice अपनी static key को Bob (N) को नहीं भेजती
- DH Function: X25519 X25519 DH जिसमें 32 bytes की key length है जैसा कि [RFC-7748](https://tools.ietf.org/html/rfc7748) में निर्दिष्ट है।
- Cipher Function: ChaChaPoly AEAD_CHACHA20_POLY1305 जैसा कि [RFC-7539](https://tools.ietf.org/html/rfc7539) section 2.8 में निर्दिष्ट है। 12 byte nonce, जिसमें पहले 4 bytes शून्य पर सेट हैं। यह [NTCP2](/docs/specs/ntcp2/) में उपयोग किए गए के समान है।
- Hash Function: SHA256 मानक 32-byte hash, जो पहले से ही I2P में व्यापक रूप से उपयोग किया जाता है।

#### फ्रेमवर्क में जोड़े गए तत्व

यह विनिर्देश Noise_IK_25519_ChaChaPoly_SHA256 के लिए निम्नलिखित संवर्धनों को परिभाषित करता है। ये आम तौर पर [NOISE](https://noiseprotocol.org/noise.html) अनुभाग 13 में दिए गए दिशानिर्देशों का पालन करते हैं।

1) क्लियरटेक्स्ट ephemeral keys को एन्कोड किया जाता है

    [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf).
2) उत्तर को cleartext tag के साथ prefixed किया जाता है। 3) Payload format को messages 1, 2, और data phase के लिए परिभाषित किया गया है।

    Of course, this is not defined in Noise.

सभी संदेशों में एक [I2NP](/docs/specs/i2np/) Garlic Message header शामिल होता है। डेटा चरण Noise डेटा चरण के समान एन्क्रिप्शन का उपयोग करता है, लेकिन उसके साथ संगत नहीं है।

### हैंडशेक पैटर्न

Handshakes [Noise](https://noiseprotocol.org/noise.html) handshake patterns का उपयोग करते हैं।

निम्नलिखित अक्षर मैपिंग का उपयोग किया जाता है:

- e = एक-बार का ephemeral key
- s = static key
- p = message payload

One-time और Unbound sessions Noise N pattern के समान हैं।

```
<- s
...
e es p ->
```
Bound sessions Noise IK pattern के समान होते हैं।

```
<- s
...
e es s ss p ->
<- tag e ee se
<- p
p ->
```
#### सुरक्षा गुण

Noise शब्दावली का उपयोग करते हुए, स्थापना और डेटा अनुक्रम निम्नलिखित है: ([Noise](https://noiseprotocol.org/noise.html) से Payload Security Properties)

```
IK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es, s, ss           1                2
  <- e, ee, se              2                4
  ->                        2                5
  <-                        2                5
```
#### XK से अंतर

IK हैंडशेक में [NTCP2](/docs/specs/ntcp2/) और [SSU2](/docs/specs/ssu2/) में उपयोग किए जाने वाले XK हैंडशेक से कई अंतर हैं।

- XK के तीन की तुलना में कुल चार DH operations
- पहले संदेश में sender authentication: payload को sender की public key के मालिक से संबंधित के रूप में authenticate किया जाता है, हालांकि key compromise हो सकती है (Authentication 1) XK को Alice के authenticate होने से पहले एक और round trip की आवश्यकता होती है।
- दूसरे संदेश के बाद पूर्ण forward secrecy (Confidentiality 5)। Bob पूर्ण forward secrecy के साथ दूसरे संदेश के तुरंत बाद payload भेज सकता है। XK को पूर्ण forward secrecy के लिए एक और round trip की आवश्यकता होती है।

सारांश में, IK Bob से Alice को response payload की 1-RTT delivery की अनुमति देता है पूर्ण forward secrecy के साथ, हालांकि request payload forward-secret नहीं है।

### सत्र

ElGamal/AES+SessionTag प्रोटोकॉल एकदिशीय है। इस स्तर पर, रिसीवर को पता नहीं होता कि संदेश कहाँ से आया है। आउटबाउंड और इनबाउंड सेशन संबद्ध नहीं होते हैं। पावतियाँ clove में DeliveryStatusMessage (GarlicMessage में wrapped) का उपयोग करके आउट-ऑफ-बैंड होती हैं।

इस specification के लिए, हम एक bidirectional protocol बनाने के लिए दो mechanisms परिभाषित करते हैं - "pairing" और "binding"। ये mechanisms बढ़ी हुई efficiency और security प्रदान करते हैं।

#### सेशन संदर्भ

ElGamal/AES+SessionTags की तरह, सभी inbound और outbound sessions एक निर्दिष्ट context में होने चाहिए, या तो router के context में या किसी विशिष्ट स्थानीय destination के context में। Java I2P में, इस context को Session Key Manager कहा जाता है।

Sessions को contexts के बीच साझा नहीं किया जाना चाहिए, क्योंकि इससे विभिन्न local destinations के बीच, या local destination और router के बीच correlation की अनुमति मिल जाएगी।

जब कोई दिया गया destination ElGamal/AES+SessionTags और इस specification दोनों को support करता है, तो दोनों प्रकार के sessions एक context साझा कर सकते हैं। नीचे section 1c) देखें।

#### इनबाउंड और आउटबाउंड सत्रों को जोड़ना

जब originator (Alice) पर एक outbound session बनाया जाता है, तो एक नया inbound session बनाया जाता है और outbound session के साथ जोड़ा जाता है, जब तक कि कोई reply की अपेक्षा न हो (जैसे raw datagrams)।

एक नया inbound session हमेशा एक नए outbound session के साथ जोड़ा जाता है, जब तक कि कोई जवाब की आवश्यकता न हो (जैसे raw datagrams)।

यदि एक उत्तर का अनुरोध किया जाता है और वह दूर के गंतव्य या router से जुड़ा होता है, तो वह नया आउटबाउंड सेशन उस गंतव्य या router से बाइंड हो जाता है, और उस गंतव्य या router के लिए किसी भी पिछले आउटबाउंड सेशन को बदल देता है।

इनबाउंड और आउटबाउंड सत्रों को जोड़ना एक द्विदिशीय प्रोटोकॉल प्रदान करता है जिसमें DH keys को ratcheting करने की क्षमता होती है।

#### सत्रों और गंतव्यों को बाइंड करना

किसी दिए गए destination या router के लिए केवल एक outbound session होता है। किसी दिए गए destination या router से कई current inbound sessions हो सकते हैं। आम तौर पर, जब एक नया inbound session बनाया जाता है, और उस session पर traffic प्राप्त होता है (जो एक ACK का काम करता है), तो अन्य sessions को अपेक्षाकृत जल्दी expire होने के लिए चिह्नित कर दिया जाता है, लगभग एक मिनट या इतने समय में। पिछले भेजे गए messages (PN) value की जांच की जाती है, और यदि पिछले inbound session में कोई unreceived messages नहीं हैं (window size के भीतर), तो पिछले session को तुरंत delete किया जा सकता है।

जब मूल स्थान (Alice) पर एक outbound session बनाया जाता है, तो वह दूर के छोर के Destination (Bob) से बंधा होता है, और कोई भी युग्मित inbound session भी दूर के छोर के Destination से बंधा होगा। जैसे-जैसे sessions ratchet होते हैं, वे दूर के छोर के Destination से बंधे रहते हैं।

जब रिसीवर (Bob) पर एक inbound session बनाया जाता है, तो यह Alice के विकल्प पर far-end Destination (Alice) से बाइंड हो सकता है। यदि Alice New Session संदेश में binding जानकारी (उसकी static key) शामिल करती है, तो session उस destination से बाइंड हो जाएगा, और एक outbound session बनाया जाएगा और उसी Destination से बाइंड हो जाएगा। जैसे-जैसे sessions ratchet होते हैं, वे far-end Destination से बाइंड रहते हैं।

#### बाइंडिंग और पेयरिंग के फायदे

सामान्य, streaming मामले के लिए, हम उम्मीद करते हैं कि Alice और Bob इस protocol का उपयोग निम्नलिखित तरीके से करेंगे:

- Alice अपने नए outbound session को एक नए inbound session के साथ जोड़ती है, दोनों
  दूर के गंतव्य (Bob) से बंधे होते हैं।
- Alice binding जानकारी और signature, और एक reply
  अनुरोध को Bob को भेजे गए New Session संदेश में शामिल करती है।
- Bob अपने नए inbound session को एक नए outbound session के साथ जोड़ता है, दोनों
  दूर के गंतव्य (Alice) से बंधे होते हैं।
- Bob paired session में Alice को एक reply (ack) भेजता है, एक नई DH key के साथ
  ratchet के साथ।
- Alice Bob की नई key के साथ एक नए outbound session में ratchet करती है, जो
  मौजूदा inbound session के साथ जोड़ा गया है।

एक inbound session को दूर के छोर के Destination से बाइंड करके, और inbound session को उसी Destination से बाइंड किए गए outbound session के साथ जोड़कर, हम दो मुख्य लाभ प्राप्त करते हैं:

1) Bob से Alice को प्रारंभिक उत्तर ephemeral-ephemeral DH का उपयोग करता है

2\) जब Alice को Bob का जवाब मिल जाता है और ratcheting हो जाती है, तो Alice से Bob को भेजे जाने वाले सभी बाद के संदेश ephemeral-ephemeral DH का उपयोग करते हैं।

#### संदेश ACKs

ElGamal/AES+SessionTags में, जब एक LeaseSet को garlic clove के रूप में बंडल किया जाता है, या tags वितरित किए जाते हैं, तो भेजने वाला router एक ACK का अनुरोध करता है। यह एक अलग garlic clove है जिसमें एक DeliveryStatus Message होता है। अतिरिक्त सुरक्षा के लिए, DeliveryStatus Message को एक Garlic Message में wrapped किया जाता है। यह तंत्र प्रोटोकॉल के दृष्टिकोण से out-of-band है।

नए protocol में, चूंकि inbound और outbound sessions जोड़े गए हैं, हमारे पास ACKs in-band हो सकते हैं। कोई अलग clove की आवश्यकता नहीं है।

एक explicit ACK बस एक Existing Session संदेश है जिसमें कोई I2NP ब्लॉक नहीं होता। हालांकि, अधिकतर मामलों में, एक explicit ACK से बचा जा सकता है, क्योंकि रिवर्स ट्रैफिक होता है। implementations के लिए यह वांछनीय हो सकता है कि वे explicit ACK भेजने से पहले थोड़ा समय (शायद सौ ms) इंतजार करें, ताकि streaming या application layer को जवाब देने का समय मिल सके।

Implementations को ACK भेजने को तब तक स्थगित करना होगा जब तक I2NP block process नहीं हो जाता, क्योंकि Garlic Message में lease set के साथ Database Store Message हो सकता है। ACK को route करने के लिए एक हालिया lease set आवश्यक होगा, और binding static key को verify करने के लिए far-end destination (lease set में निहित) आवश्यक होगा।

#### सेशन टाइमआउट

Outbound sessions हमेशा inbound sessions से पहले expire होने चाहिए। जब एक outbound session expire हो जाता है और एक नया बनाया जाता है, तो एक नया paired inbound session भी बनाया जाएगा। यदि कोई पुराना inbound session था, तो उसे expire होने की अनुमति दी जाएगी।

### मल्टिकास्ट

निर्धारित किया जाना है

### परिभाषाएं

हम निम्नलिखित फ़ंक्शन्स को परिभाषित करते हैं जो उपयोग किए गए क्रिप्टोग्राफिक बिल्डिंग ब्लॉक्स के अनुरूप हैं।

ZEROLEN

शून्य-लंबाई बाइट array

CSRNG(n)

क्रिप्टोग्राफिकली-सुरक्षित यादृच्छिक संख्या से n-byte आउटपुट

    generator.

H(p, d)

SHA-256 hash function जो एक personalization string p और data लेता है

    d, and produces an output of length 32 bytes. As defined in
    [NOISE](https://noiseprotocol.org/noise.html). || below means append.

    Use SHA-256 as follows:

        H(p, d) := SHA-256(p || d)

MixHash(d)

SHA-256 hash function जो एक पिछला hash h और नया data d लेता है,

    and produces an output of length 32 bytes. || below means append.

    Use SHA-256 as follows:

        MixHash(d) := h = SHA-256(h || d)

STREAM

ChaCha20/Poly1305 AEAD जैसा कि निर्दिष्ट है

    [RFC-7539](https://tools.ietf.org/html/rfc7539). S_KEY_LEN = 32 and S_IV_LEN =
    12.

    ENCRYPT(k, n, plaintext, ad)

    :   Encrypts plaintext using the cipher key k, and nonce n which
        MUST be unique for the key k. Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16
        bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if
        the key is secret.

    DECRYPT(k, n, ciphertext, ad)

    :   Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional. Returns the plaintext.

DH

X25519 सार्वजनिक कुंजी समझौता प्रणाली। 32 बाइट्स की निजी कुंजियां, सार्वजनिक

    keys of 32 bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()

    :   Generates a new private key.

    DERIVE_PUBLIC(privkey)

    :   Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()

    :   Generates a new private key that maps to a public key suitable
        for Elligator2 encoding. Note that half of the
        randomly-generated private keys will not be suitable and must be
        discarded.

    ENCODE_ELG2(pubkey)

    :   Returns the Elligator2-encoded public key corresponding to the
        given public key (inverse mapping). Encoded keys are little
        endian. Encoded key must be 256 bits indistinguishable from
        random data. See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)

    :   Returns the public key corresponding to the given
        Elligator2-encoded public key. See Elligator2 section below for
        specification.

    DH(privkey, pubkey)

    :   Generates a shared secret from the given private and public
        keys.

HKDF(salt, ikm, info, n)

एक क्रिप्टोग्राफिक key derivation function जो कुछ input key लेता है

    material ikm (which should have good entropy but is not required to
    be a uniformly random string), a salt of length 32 bytes, and a
    context-specific 'info' value, and produces an output of n bytes
    suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using
    the HMAC hash function SHA-256 as specified in
    [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32
    bytes max.

MixKey(d)

पिछली chainKey और नए डेटा d के साथ HKDF() का उपयोग करें, और नई सेट करता है

    chainKey and k. As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows:

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]

### 1) मैसेज फॉर्मेट

#### वर्तमान संदेश प्रारूप की समीक्षा

[I2NP](/docs/specs/i2np/) में निर्दिष्ट Garlic Message निम्नलिखित है। चूंकि एक डिज़ाइन लक्ष्य यह है कि intermediate hops नई और पुरानी crypto में अंतर नहीं कर सकें, इसलिए यह format बदल नहीं सकता, भले ही length field अनावश्यक हो। format को पूर्ण 16-byte header के साथ दिखाया गया है, हालांकि वास्तविक header एक अलग format में हो सकता है, यह इस्तेमाल किए गए transport पर निर्भर करता है।

जब डिक्रिप्ट किया जाता है तो डेटा में Garlic Cloves की एक श्रृंखला और अतिरिक्त डेटा होता है, जिसे Clove Set के रूप में भी जाना जाता है।

विवरण और पूर्ण विनिर्देश के लिए [I2NP](/docs/specs/i2np/) देखें।

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### एन्क्रिप्टेड डेटा फॉर्मेट की समीक्षा

ElGamal/AES+SessionTags में, दो संदेश प्रारूप हैं:

1\) नया session: - 514 byte ElGamal block - AES block (न्यूनतम 128 bytes, 16 का गुणज)

2\) मौजूदा सत्र: - 32 बाइट Session Tag - AES ब्लॉक (न्यूनतम 128 बाइट्स, 16 का गुणज)

ये संदेश एक I2NP garlic message में encapsulated होते हैं, जिसमें एक length field होता है, इसलिए लंबाई पता होती है।

प्राप्तकर्ता पहले Session Tag के रूप में पहले 32 बाइट्स को खोजने का प्रयास करता है। यदि मिल जाता है, तो वह AES block को डिक्रिप्ट करता है। यदि नहीं मिलता, और डेटा कम से कम (514+16) लंबा है, तो वह ElGamal block को डिक्रिप्ट करने का प्रयास करता है, और यदि सफल होता है, तो AES block को डिक्रिप्ट करता है।

#### नए Session Tags और Signal के साथ तुलना

Signal Double Ratchet में, header में निम्नलिखित होता है:

- DH: वर्तमान ratchet सार्वजनिक कुंजी
- PN: पिछली श्रृंखला संदेश लंबाई
- N: संदेश संख्या

Signal की "sending chains" हमारे tag sets के लगभग बराबर हैं। एक session tag का उपयोग करके, हम इसका अधिकांश हिस्सा समाप्त कर सकते हैं।

New Session में, हम अनएन्क्रिप्टेड हेडर में केवल पब्लिक key डालते हैं।

मौजूदा सत्र में, हम हेडर के लिए एक session tag का उपयोग करते हैं। Session tag वर्तमान ratchet public key और संदेश संख्या से जुड़ा होता है।

नए और मौजूदा दोनों Session में, PN और N एन्क्रिप्टेड body में होते हैं।

Signal में, चीजें लगातार ratcheting करती रहती हैं। एक नया DH public key प्राप्तकर्ता को ratchet करने और वापस एक नया public key भेजने की आवश्यकता होती है, जो प्राप्त public key के लिए ack का भी काम करता है। हमारे लिए यह बहुत अधिक DH operations होंगे। इसलिए हम प्राप्त key के ack और नए public key के transmission को अलग करते हैं। नए DH public key से उत्पन्न session tag का उपयोग करके भेजा गया कोई भी message एक ACK का काम करता है। हम केवल तभी नया public key transmit करते हैं जब हम rekey करना चाहते हैं।

DH को ratchet करने से पहले संदेशों की अधिकतम संख्या 65535 है।

जब एक session key वितरित करते हैं, तो हम उससे "Tag Set" निकालते हैं, बजाय session tags को अलग से वितरित करने के। एक Tag Set में 65536 तक tags हो सकते हैं। हालांकि, receivers को "look-ahead" रणनीति लागू करनी चाहिए, बजाय एक साथ सभी संभावित tags generate करने के। अंतिम अच्छे प्राप्त tag के बाद केवल अधिकतम N tags generate करें। N अधिकतम 128 हो सकता है, लेकिन 32 या इससे भी कम एक बेहतर विकल्प हो सकता है।

### 1a) नया सेशन फॉर्मेट

नई सत्र वन टाइम पब्लिक की (32 बाइट्स) एन्क्रिप्टेड डेटा और MAC (शेष बाइट्स)

New Session संदेश में भेजने वाले की static public key हो भी सकती है और नहीं भी। यदि यह शामिल है, तो reverse session उस key से बंधा होता है। Static key को शामिल किया जाना चाहिए यदि replies की अपेक्षा है, यानी streaming और repliable datagrams के लिए। इसे raw datagrams के लिए शामिल नहीं किया जाना चाहिए।

New Session संदेश one-way Noise [NOISE](https://noiseprotocol.org/noise.html) pattern "N" के समान है (यदि static key नहीं भेजी गई है), या two-way pattern "IK" के समान है (यदि static key भेजी गई है)।

### 1b) नया session प्रारूप (binding के साथ)

लंबाई 96 + payload लंबाई है। एन्क्रिप्टेड प्रारूप:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         Static Key                    +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+    (MAC) for Static Key Section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Static Key encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### नया सत्र अस्थायी कुंजी

ephemeral key 32 bytes का है, जो Elligator2 के साथ encoded है। इस key का कभी पुन: उपयोग नहीं किया जाता; प्रत्येक message के साथ एक नई key generate की जाती है, जिसमें retransmissions भी शामिल हैं।

#### स्टेटिक की

जब डिक्रिप्ट किया जाता है, एलिस की X25519 स्टेटिक key, 32 bytes।

#### पेलोड

एन्क्रिप्टेड लेंथ डेटा का शेष भाग है। डिक्रिप्टेड लेंथ एन्क्रिप्टेड लेंथ से 16 कम है। Payload में एक DateTime ब्लॉक होना चाहिए और आमतौर पर एक या अधिक Garlic Clove ब्लॉक होंगे। फॉर्मेट और अतिरिक्त आवश्यकताओं के लिए नीचे payload सेक्शन देखें।

### 1c) नया session फॉर्मेट (binding के बिना)

यदि कोई उत्तर आवश्यक नहीं है, तो कोई static key नहीं भेजी जाती है।

लंबाई 96 + पेलोड लंबाई है। एन्क्रिप्टेड प्रारूप:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### नई सत्र एफिमेरल की

Alice की ephemeral key। यह ephemeral key 32 bytes की है, जो Elligator2 के साथ encoded है, little endian में। यह key कभी भी दोबारा उपयोग नहीं की जाती; हर message के साथ एक नई key generate की जाती है, जिसमें retransmissions भी शामिल हैं।

#### फ्लैग्स सेक्शन डिक्रिप्टेड डेटा

Flags सेक्शन में कुछ भी नहीं होता। यह हमेशा 32 bytes का होता है, क्योंकि इसे binding के साथ New Session messages के लिए static key के समान लंबाई का होना चाहिए। Bob यह निर्धारित करता है कि यह static key है या flags section, यह जांच कर कि क्या 32 bytes सभी शून्य हैं।

TODO यहाँ कोई flags की आवश्यकता है?

#### पेलोड

एन्क्रिप्टेड लेंथ डेटा का बचा हुआ हिस्सा है। डिक्रिप्टेड लेंथ एन्क्रिप्टेड लेंथ से 16 कम होती है। Payload में एक DateTime ब्लॉक होना चाहिए और आमतौर पर एक या अधिक Garlic Clove ब्लॉक होते हैं। फॉर्मेट और अतिरिक्त आवश्यकताओं के लिए नीचे payload सेक्शन देखें।

### 1d) एक-बार प्रारूप (कोई बाइंडिंग या सेशन नहीं)

यदि केवल एक संदेश भेजने की अपेक्षा है, तो कोई सत्र सेटअप या स्थिर कुंजी की आवश्यकता नहीं है।

लंबाई 96 + payload लंबाई है। एन्क्रिप्टेड प्रारूप:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       Ephemeral Public Key            |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### नया सत्र वन टाइम की

वन टाइम key 32 bytes का है, जो Elligator2 के साथ encoded है, little endian में। यह key कभी भी दोबारा उपयोग नहीं की जाती; हर संदेश के साथ एक नई key generate की जाती है, जिसमें retransmissions भी शामिल हैं।

#### फ्लैग्स सेक्शन डिक्रिप्टेड डेटा

Flags सेक्शन में कुछ भी नहीं होता। यह हमेशा 32 bytes का होता है, क्योंकि इसकी लंबाई binding के साथ New Session messages के लिए static key के समान होनी चाहिए। Bob यह निर्धारित करता है कि यह एक static key है या flags सेक्शन है, यह जांचकर कि क्या 32 bytes सभी शून्य हैं।

TODO यहाँ कोई flags की आवश्यकता है?

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+             All zeros                 +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

zeros:: All zeros, 32 bytes.
```
#### पेलोड

एन्क्रिप्टेड लेंथ डेटा का शेष भाग है। डिक्रिप्टेड लेंथ एन्क्रिप्टेड लेंथ से 16 कम है। पेलोड में एक DateTime ब्लॉक होना चाहिए और आमतौर पर एक या अधिक garlic clove ब्लॉक होंगे। फॉर्मेट और अतिरिक्त आवश्यकताओं के लिए नीचे पेलोड सेक्शन देखें।

### 1f) नए सत्र संदेश के लिए KDFs

#### प्रारंभिक ChainKey के लिए KDF

यह IK के लिए मानक [NOISE](https://noiseprotocol.org/noise.html) है जिसमें एक संशोधित प्रोटोकॉल नाम है। ध्यान दें कि हम IK pattern (bound sessions) और N pattern (unbound sessions) दोनों के लिए समान initializer का उपयोग करते हैं।

प्रोटोकॉल नाम दो कारणों से संशोधित किया गया है। पहला, यह इंगित करने के लिए कि ephemeral keys Elligator2 के साथ encoded हैं, और दूसरा, यह इंगित करने के लिए कि दूसरे संदेश से पहले tag value को mix करने के लिए MixHash() को कॉल किया जाता है।

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
 (40 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set chainKey = h

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections
```
#### Flags/Static Key Section Encrypted Contents के लिए KDF

```
This is the "e" message pattern:

// Bob's X25519 static keys
// bpk is published in leaseset
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

// Bob static public key
// MixHash(bpk)
// || below means append
h = SHA256(h || bpk);

// up until here, can all be precalculated by Bob for all incoming connections

// Alice's X25519 ephemeral keys
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

// Alice ephemeral public key
// MixHash(aepk)
// || below means append
h = SHA256(h || aepk);

// h is used as the associated data for the AEAD in the New Session Message
// Retain the Hash h for the New Session Reply KDF
// eapk is sent in cleartext in the
// beginning of the New Session message
elg2_aepk = ENCODE_ELG2(aepk)
// As decoded by Bob
aepk = DECODE_ELG2(elg2_aepk)

End of "e" message pattern.

This is the "es" message pattern:

// Noise es
sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, flags/static key section, ad)

End of "es" message pattern.

This is the "s" message pattern:

// MixHash(ciphertext)
// Save for Payload section KDF
h = SHA256(h || ciphertext)

// Alice's X25519 static keys
ask = GENERATE_PRIVATE()
apk = DERIVE_PUBLIC(ask)

End of "s" message pattern.
```
#### Payload Section के लिए KDF (Alice static key के साथ)

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
#### पेलोड सेक्शन के लिए KDF (Alice स्टेटिक की के बिना)

ध्यान दें कि यह एक Noise "N" पैटर्न है, लेकिन हम bound sessions के लिए उसी "IK" initializer का उपयोग करते हैं।

New Session संदेशों को तब तक Alice की static key युक्त या रहित के रूप में पहचाना नहीं जा सकता जब तक कि static key को decrypt और inspect नहीं किया जाता यह निर्धारित करने के लिए कि इसमें सभी शून्य हैं या नहीं। इसलिए, receiver को सभी New Session संदेशों के लिए "IK" state machine का उपयोग करना चाहिए। यदि static key में सभी शून्य हैं, तो "ss" message pattern को छोड़ना चाहिए।

```
chainKey = from Flags/Static key section
k = from Flags/Static key section
n = 1
ad = h from Flags/Static key section
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1g) नए सत्र उत्तर का प्रारूप

एक New Session संदेश के जवाब में एक या अधिक New Session Replies भेजे जा सकते हैं। प्रत्येक reply के आगे एक tag लगाया जाता है, जो session के लिए TagSet से generate किया जाता है।

New Session Reply दो भागों में है। पहला भाग prepended tag के साथ Noise IK handshake का completion है। पहले भाग की लंबाई 56 bytes है। दूसरा भाग data phase payload है। दूसरे भाग की लंबाई 16 + payload length है।

कुल लंबाई 72 + payload की लंबाई है। एन्क्रिप्टेड प्रारूप:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+        Ephemeral Public Key           +
|                                       |
+            32 bytes                   +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+  (MAC) for Key Section (no data)      +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Tag :: 8 bytes, cleartext

Public Key :: 32 bytes, little endian, Elligator2, cleartext

MAC :: Poly1305 message authentication code, 16 bytes
       Note: The ChaCha20 plaintext data is empty (ZEROLEN)

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### सेशन टैग

यह टैग Session Tags KDF में जनरेट होता है, जैसा कि नीचे DH Initialization KDF में initialize किया गया है। यह reply को session के साथ correlate करता है। DH Initialization से Session Key का उपयोग नहीं किया जाता।

#### नया सत्र उत्तर अस्थायी की

Bob की ephemeral key। Ephemeral key 32 bytes की होती है, जो Elligator2 के साथ encoded होती है, little endian में। यह key कभी दोबारा उपयोग नहीं होती; हर message के साथ एक नई key generate की जाती है, retransmissions सहित।

#### पेलोड

एन्क्रिप्टेड लंबाई डेटा का शेष भाग है। डिक्रिप्टेड लंबाई एन्क्रिप्टेड लंबाई से 16 कम है। Payload में आमतौर पर एक या अधिक Garlic Clove ब्लॉक होते हैं। फॉर्मेट और अतिरिक्त आवश्यकताओं के लिए नीचे payload सेक्शन देखें।

#### Reply TagSet के लिए KDF

TagSet से एक या अधिक tags बनाए जाते हैं, जो नीचे दिए गए KDF का उपयोग करके initialize किया जाता है, New Session message से chainKey का उपयोग करके।

```
// Generate tagset

tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
    tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
#### Reply Key Section Encrypted Contents के लिए KDF

```
// Keys from the New Session message
// Alice's X25519 keys
// apk and aepk are sent in original New Session message
// ask = Alice private static key
// apk = Alice public static key
// aesk = Alice ephemeral private key
// aepk = Alice ephemeral public key
// Bob's X25519 static keys
// bsk = Bob private static key
// bpk = Bob public static key

// Generate the tag
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG

// MixHash(tag)
h = SHA256(h || tag)

This is the "e" message pattern:

// Bob's X25519 ephemeral keys
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

// Bob's ephemeral public key
// MixHash(bepk)
// || below means append
h = SHA256(h || bepk);

// elg2_bepk is sent in cleartext in the
// beginning of the New Session message
elg2_bepk = ENCODE_ELG2(bepk)
// As decoded by Bob
bepk = DECODE_ELG2(elg2_bepk)

End of "e" message pattern.

This is the "ee" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from original New Session Payload Section
sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
keydata = HKDF(chainKey, sharedSecret, "", 32)
chainKey = keydata[0:31]

End of "ee" message pattern.

This is the "se" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
sharedSecret = DH(ask, bepk) = DH(besk, apk)
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

End of "se" message pattern.

// MixHash(ciphertext)
h = SHA256(h || ciphertext)

chainKey is used in the ratchet below.
```
#### Payload Section Encrypted Contents के लिए KDF

यह विभाजन के बाद के पहले Existing Session संदेश की तरह है, लेकिन अलग tag के बिना। इसके अतिरिक्त, हम payload को NSR संदेश से जोड़ने के लिए ऊपर वाले hash का उपयोग करते हैं।

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
### नोट्स

प्रतिक्रिया के आकार के आधार पर, कई NSR संदेश भेजे जा सकते हैं, प्रत्येक अनूठी ephemeral keys के साथ।

Alice और Bob को हर NS और NSR संदेश के लिए नई ephemeral keys का उपयोग करना आवश्यक है।

Alice को Bob के ES messages भेजने से पहले Bob के NSR messages में से एक प्राप्त करना होगा, और Bob को ES messages भेजने से पहले Alice से एक ES message प्राप्त करना होगा।

Bob के NSR Payload Section से `chainKey` और `k` का उपयोग प्रारंभिक ES DH Ratchets (दोनों दिशाओं में, DH Ratchet KDF देखें) के लिए inputs के रूप में किया जाता है।

Bob को केवल Alice से प्राप्त ES संदेशों के लिए Existing Sessions बनाए रखने चाहिए। किसी भी अन्य बनाए गए inbound और outbound sessions (कई NSRs के लिए) को किसी दिए गए session के लिए Alice का पहला ES संदेश प्राप्त करने के तुरंत बाद नष्ट कर देना चाहिए।

### 1h) मौजूदा सत्र प्रारूप

Session tag (8 bytes) एन्क्रिप्टेड डेटा और MAC (नीचे धारा 3 देखें)

#### प्रारूप

एन्क्रिप्टेड:

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### पेलोड

एन्क्रिप्टेड लेंथ डेटा का शेष भाग है। डिक्रिप्टेड लेंथ एन्क्रिप्टेड लेंथ से 16 कम है। फॉर्मेट और आवश्यकताओं के लिए नीचे पेलोड सेक्शन देखें।

#### KDF

```
See AEAD section below.

// AEAD parameters for Existing Session payload
k = The 32-byte session key associated with this session tag
n = The message number N in the current chain, as retrieved from the associated Session Tag.
ad = The session tag, 8 bytes
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 2) ECIES-X25519

प्रारूप: 32-बाइट सार्वजनिक और निजी कुंजियां, little-endian।

### 2a) Elligator2

मानक Noise handshakes में, प्रत्येक दिशा में प्रारंभिक handshake संदेश ephemeral keys के साथ शुरू होते हैं जो cleartext में प्रसारित होती हैं। चूंकि वैध X25519 keys यादृच्छिक से अलग पहचानी जा सकती हैं, एक man-in-the-middle इन संदेशों को मौजूदा Session संदेशों से अलग कर सकता है जो यादृच्छिक session tags के साथ शुरू होते हैं। [NTCP2](/docs/specs/ntcp2/) ([Prop111](/proposals/111-ntcp2/)) में, हमने key को अस्पष्ट करने के लिए out-of-band static key का उपयोग करके एक कम-ओवरहेड XOR function का उपयोग किया था। हालांकि, यहाँ threat model अलग है; हम किसी भी MitM को ट्रैफिक के गंतव्य की पुष्टि करने, या प्रारंभिक handshake संदेशों को मौजूदा Session संदेशों से अलग करने के लिए कोई भी साधन उपयोग करने की अनुमति नहीं देना चाहते।

इसलिए, [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) का उपयोग New Session और New Session Reply संदेशों में ephemeral keys को रूपांतरित करने के लिए किया जाता है ताकि वे uniform random strings से अप्रभेद्य हों।

#### प्रारूप

32-बाइट पब्लिक और प्राइवेट कीज़। एन्कोडेड कीज़ लिटिल एंडियन हैं।

जैसा कि [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) में परिभाषित है, एन्कोडेड keys 254 यादृच्छिक bits से अविभेद्य हैं। हमें 256 यादृच्छिक bits (32 bytes) की आवश्यकता है। इसलिए, encoding और decoding निम्नलिखित रूप में परिभाषित हैं:

एन्कोडिंग:

```
ENCODE_ELG2() Definition

// Encode as defined in Elligator2 specification
encodedKey = encode(pubkey)
// OR in 2 random bits to MSB
randomByte = CSRNG(1)
encodedKey[31] |= (randomByte & 0xc0)
```
डिकोडिंग:

```
DECODE_ELG2() Definition

// Mask out 2 random bits from MSB
encodedKey[31] &= 0x3f
// Decode as defined in Elligator2 specification
pubkey = decode(encodedKey)
```
#### टिप्पणियाँ

Elligator2 औसत key generation समय को दोगुना कर देता है, क्योंकि आधी private keys ऐसी public keys बनाती हैं जो Elligator2 के साथ encoding के लिए अनुपयुक्त हैं। इसके अलावा, key generation का समय exponential distribution के साथ असीमित है, क्योंकि generator को तब तक retry करते रहना पड़ता है जब तक कि एक उपयुक्त key pair नहीं मिल जाता।

इस ओवरहेड को पहले से ही key generation करके प्रबंधित किया जा सकता है, एक अलग thread में, उपयुक्त keys का एक pool बनाए रखने के लिए।

जेनरेटर उपयुक्तता निर्धारित करने के लिए ENCODE_ELG2() फ़ंक्शन करता है। इसलिए, जेनरेटर को ENCODE_ELG2() के परिणाम को संग्रहीत करना चाहिए ताकि इसे फिर से गणना न करनी पड़े।

इसके अतिरिक्त, अनुपयुक्त keys को [NTCP2](/docs/specs/ntcp2/) के लिए उपयोग की जाने वाली keys के pool में जोड़ा जा सकता है, जहाँ Elligator2 का उपयोग नहीं किया जाता। ऐसा करने के security issues का निर्धारण अभी बाकी है।

### 3) AEAD (ChaChaPoly)

ChaCha20 और Poly1305 का उपयोग करते हुए AEAD, वैसा ही जैसा [NTCP2](/docs/specs/ntcp2/) में है। यह [RFC-7539](https://tools.ietf.org/html/rfc7539) से मेल खाता है, जिसका उपयोग TLS [RFC-7905](https://tools.ietf.org/html/rfc7905) में भी समान रूप से किया गया है।

#### नए सत्र और नए सत्र उत्तर इनपुट

New Session message में AEAD block के लिए encryption/decryption functions के inputs:

```
k :: 32 byte cipher key
     See New Session and New Session Reply KDFs above.

n :: Counter-based nonce, 12 bytes.
     n = 0

ad :: Associated data, 32 bytes.
      The SHA256 hash of the preceding data, as output from mixHash()

data :: Plaintext data, 0 or more bytes
```
#### मौजूदा सत्र इनपुट

एक Existing Session संदेश में AEAD ब्लॉक के लिए एन्क्रिप्शन/डिक्रिप्शन फ़ंक्शन्स के इनपुट:

```
k :: 32 byte session key
     As looked up from the accompanying session tag.

n :: Counter-based nonce, 12 bytes.
     Starts at 0 and incremented for each message when transmitting.
     For the receiver, the value
     as looked up from the accompanying session tag.
     First four bytes are always zero.
     Last eight bytes are the message number (n), little-endian encoded.
     Maximum value is 65535.
     Session must be ratcheted when N reaches that value.
     Higher values must never be used.

ad :: Associated data
      The session tag

data :: Plaintext data, 0 or more bytes
```
#### एन्क्रिप्टेड फॉर्मेट

एन्क्रिप्शन फ़ंक्शन का आउटपुट, डिक्रिप्शन फ़ंक्शन का इनपुट:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### नोट्स

- चूंकि ChaCha20 एक stream cipher है, plaintexts को pad करने की आवश्यकता नहीं है।
  अतिरिक्त keystream bytes को discard कर दिया जाता है।
- cipher के लिए key (256 bits) SHA256 KDF के द्वारा agreed upon किया जाता है। प्रत्येक message के लिए KDF के विवरण नीचे अलग
  sections में हैं।
- ChaChaPoly frames known size के होते हैं क्योंकि वे
  I2NP data message में encapsulate होते हैं।
- सभी messages के लिए, padding authenticated data frame के अंदर होता है।

#### AEAD त्रुटि हैंडलिंग

सभी प्राप्त डेटा जो AEAD सत्यापन में असफल होता है, उसे अस्वीकार कर देना चाहिए। कोई प्रतिक्रिया नहीं भेजी जाती।

### 4) Ratchets

हम अभी भी session tags का उपयोग करते हैं, जैसे पहले करते थे, लेकिन हम उन्हें generate करने के लिए ratchets का उपयोग करते हैं। Session tags में एक rekey विकल्प भी था जिसे हमने कभी implement नहीं किया। तो यह double ratchet की तरह है लेकिन हमने कभी दूसरा वाला नहीं किया।

यहाँ हम Signal के Double Ratchet के समान कुछ परिभाषित करते हैं। session tags प्राप्तकर्ता और भेजने वाले दोनों तरफ निर्धारणवादी और समान रूप से उत्पन्न होते हैं।

एक symmetric key/tag ratchet का उपयोग करके, हम sender side पर session tags को store करने के लिए memory usage को समाप्त कर देते हैं। हम tag sets भेजने की bandwidth consumption को भी समाप्त कर देते हैं। Receiver side usage अभी भी महत्वपूर्ण है, लेकिन हम इसे और कम कर सकते हैं क्योंकि हम session tag को 32 bytes से घटाकर 8 bytes कर देंगे।

हम Signal में निर्दिष्ट (और वैकल्पिक) header encryption का उपयोग नहीं करते हैं, बल्कि session tags का उपयोग करते हैं।

DH ratchet का उपयोग करके, हम forward secrecy प्राप्त करते हैं, जो ElGamal/AES+SessionTags में कभी लागू नहीं किया गया था।

नोट: New Session one-time public key ratchet का हिस्सा नहीं है, इसका एकमात्र कार्य Alice की प्रारंभिक DH ratchet key को encrypt करना है।

#### संदेश संख्याएं

Double Ratchet खोए हुए या गलत क्रम में आए संदेशों को संभालता है प्रत्येक संदेश हेडर में एक tag शामिल करके। प्राप्तकर्ता tag के index को देखता है, यह संदेश संख्या N है। यदि संदेश में PN value के साथ एक Message Number block है, तो प्राप्तकर्ता पिछले tag set में उस value से अधिक किसी भी tag को हटा सकता है, जबकि पिछले tag set से छूटे हुए tags को बनाए रख सकता है इस स्थिति में कि छूटे हुए संदेश बाद में आ जाएं।

#### नमूना कार्यान्वयन

हम इन ratchets को implement करने के लिए निम्नलिखित data structures और functions को परिभाषित करते हैं।

TAGSET_ENTRY

TAGSET में एक एकल प्रविष्टि।

    INDEX

    :   An integer index, starting with 0

    SESSION_TAG

    :   An identifier to go out on the wire, 8 bytes

    SESSION_KEY

    :   A symmetric key, never goes on the wire, 32 bytes

TAGSET

TAGSET_ENTRIES का एक संग्रह।

    CREATE(key, n)

    :   Generate a new TAGSET using initial cryptographic key material
        of 32 bytes. The associated session identifier is provided. The
        initial number of of tags to create is specified; this is
        generally 0 or 1 for an outgoing session. LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)

    :   Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()

    :   Generate one more TAGSET_ENTRY, unless the maximum number
        SESSION_TAGS have already been generated. If LAST_INDEX is
        greater than or equal to 65535, return. ++ LAST_INDEX Create a
        new TAGSET_ENTRY with the LAST_INDEX value and the calculated
        SESSION_TAG. Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may be
        deferred and calculated in GET_SESSION_KEY(). Calls EXPIRE()

    EXPIRE()

    :   Remove tags and keys that are too old, or if the TAGSET size
        exceeds some limit.

    RATCHET_TAG()

    :   Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()

    :   Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION

    :   The associated session.

    CREATION_TIME

    :   When the TAGSET was created.

    LAST_INDEX

    :   The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()

    :   Used for outgoing sessions only. EXTEND(1) is called if there
        are no remaining TAGSET_ENTRIES. If EXTEND(1) did nothing, the
        max of 65535 TAGSETS have been used, and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)

    :   Used for incoming sessions only. Returns the TAGSET_ENTRY
        containing the sessionTag. If found, the TAGSET_ENTRY is
        removed. If the SESSION_KEY calculation was deferred, it is
        calculated now. If there are few TAGSET_ENTRIES remaining,
        EXTEND(n) is called.

#### 4a) DH Ratchet

Ratchets लेकिन Signal की तरह तेज़ी से नहीं। हम प्राप्त key की ack को नई key generate करने से अलग करते हैं। सामान्य उपयोग में, Alice और Bob दोनों New Session में तुरंत ratchet करेंगे (दो बार), लेकिन फिर से ratchet नहीं करेंगे।

ध्यान दें कि एक ratchet एकल दिशा के लिए है, और उस दिशा के लिए एक New Session tag / message key ratchet chain उत्पन्न करता है। दोनों दिशाओं के लिए keys उत्पन्न करने हेतु, आपको दो बार ratchet करना होगा।

आप हर बार एक नई key generate और भेजते समय ratchet करते हैं। आप हर बार एक नई key receive करते समय ratchet करते हैं।

Alice एक अनबाउंड आउटबाउंड सेशन बनाते समय एक बार ratchet करती है, वह एक इनबाउंड सेशन नहीं बनाती (अनबाउंड का उत्तर नहीं दिया जा सकता)।

Bob एक unbound inbound session बनाते समय एक बार ratchet करता है, और एक corresponding outbound session नहीं बनाता (unbound non-repliable होता है)।

Alice, Bob से New Session Reply (NSR) संदेशों में से एक प्राप्त करने तक Bob को New Session (NS) संदेश भेजती रहती है। फिर वह NSR के Payload Section KDF परिणामों को session ratchets के लिए इनपुट के रूप में उपयोग करती है (DH Ratchet KDF देखें), और Existing Session (ES) संदेश भेजना शुरू करती है।

प्रत्येक NS संदेश प्राप्त होने पर, Bob एक नया inbound session बनाता है, reply Payload Section के KDF परिणामों का उपयोग करके नए inbound और outbound ES DH Ratchet के लिए inputs के रूप में।

प्रत्येक आवश्यक उत्तर के लिए, Bob, Alice को payload में उत्तर के साथ एक NSR संदेश भेजता है। यह आवश्यक है कि Bob हर NSR के लिए नई ephemeral keys का उपयोग करे।

Bob को Alice से किसी एक inbound session पर ES संदेश प्राप्त करना होगा, संबंधित outbound session पर ES संदेश बनाने और भेजने से पहले।

Alice को Bob से NSR संदेश प्राप्त करने के लिए टाइमर का उपयोग करना चाहिए। यदि टाइमर समाप्त हो जाता है, तो session को हटा देना चाहिए।

KCI और/या resource exhaustion attack से बचने के लिए, जहाँ एक attacker Bob के NSR replies को drop कर देता है ताकि Alice NS messages भेजती रहे, Alice को timer expiration के कारण एक निश्चित संख्या की retries के बाद Bob के साथ New Sessions शुरू करने से बचना चाहिए।

Alice और Bob प्रत्येक NextKey block प्राप्त होने पर एक DH ratchet करते हैं।

Alice और Bob प्रत्येक DH ratchet के बाद नए tag setstchets और दो symmetric keys ratchets generate करते हैं। किसी दी गई दिशा में प्रत्येक नए ES message के लिए, Alice और Bob session tag और symmetric key ratchets को आगे बढ़ाते हैं।

प्रारंभिक handshake के बाद DH ratchets की आवृत्ति implementation-dependent है। जबकि protocol रैचेट आवश्यक होने से पहले 65535 संदेशों की सीमा रखता है, अधिक बार ratcheting (संदेश गिनती, बीता समय, या दोनों के आधार पर) अतिरिक्त सुरक्षा प्रदान कर सकती है।

bound sessions पर अंतिम handshake KDF के बाद, Bob और Alice को inbound और outbound sessions के लिए स्वतंत्र symmetric और tag chain keys बनाने हेतु परिणामी CipherState पर Noise Split() function चलाना चाहिए।

##### KEY और TAG SET IDs

Key और tag set ID नंबरों का उपयोग keys और tag sets की पहचान के लिए किया जाता है। Key IDs का उपयोग NextKey blocks में भेजी गई या उपयोग की गई key की पहचान के लिए किया जाता है। Tag set IDs का उपयोग (message number के साथ) ACK blocks में उस message की पहचान के लिए किया जाता है जिसे ack किया जा रहा है। Key और tag set दोनों IDs एक single direction के लिए tag sets पर लागू होते हैं। Key और tag set ID नंबर sequential होने चाहिए।

प्रत्येक दिशा में एक सेशन के लिए उपयोग किए जाने वाले पहले tag sets में, tag set ID 0 होता है। कोई NextKey blocks नहीं भेजे गए हैं, इसलिए कोई key IDs नहीं हैं।

DH ratchet शुरू करने के लिए, भेजने वाला 0 की key ID के साथ एक नया NextKey block भेजता है। प्राप्तकर्ता 0 की key ID के साथ एक नया NextKey block के साथ जवाब देता है। इसके बाद भेजने वाला 1 की tag set ID के साथ एक नया tag set का उपयोग शुरू करता है।

बाद के tag sets समान रूप से उत्पन्न होते हैं। NextKey exchanges के बाद उपयोग किए जाने वाले सभी tag sets के लिए, tag set number (1 + Alice's key ID + Bob's key ID) होता है।

Key और tag set ID 0 से शुरू होते हैं और क्रमिक रूप से बढ़ते हैं। अधिकतम tag set ID 65535 है। अधिकतम key ID 32767 है। जब कोई tag set लगभग समाप्त हो जाता है, तो tag set भेजने वाले को NextKey एक्सचेंज शुरू करना चाहिए। जब tag set 65535 लगभग समाप्त हो जाता है, तो tag set भेजने वाले को New Session संदेश भेजकर एक नया सत्र शुरू करना चाहिए।

1730 के streaming अधिकतम संदेश आकार के साथ, और यह मानते हुए कि कोई retransmissions नहीं हैं, एकल tag set का उपयोग करके सैद्धांतिक अधिकतम डेटा स्थानांतरण 1730 * 65536 ~= 108 MB है। Retransmissions के कारण वास्तविक अधिकतम इससे कम होगा।

सभी 65536 उपलब्ध tag sets के साथ सैद्धांतिक अधिकतम डेटा स्थानांतरण, सत्र को छोड़कर बदलने से पहले, 64K * 108 MB ~= 6.9 TB है।

##### DH RATCHET MESSAGE FLOW

एक tag set के लिए अगला key exchange उन tags के भेजने वाले (outbound tag set के मालिक) द्वारा शुरू किया जाना चाहिए। प्राप्तकर्ता (inbound tag set का मालिक) जवाब देगा। एप्लिकेशन layer पर एक सामान्य HTTP GET ट्रैफिक के लिए, Bob अधिक संदेश भेजेगा और key exchange शुरू करके पहले ratchet करेगा; नीचे का diagram यह दिखाता है। जब Alice ratchet करती है, तो वही चीज़ उल्टे क्रम में होती है।

NS/NSR handshake के बाद उपयोग किया जाने वाला पहला tag set, tag set 0 है। जब tag set 0 लगभग समाप्त हो जाता है, तो tag set 1 बनाने के लिए दोनों दिशाओं में नई keys का आदान-प्रदान होना चाहिए। इसके बाद, नई key केवल एक दिशा में भेजी जाती है।

टैग सेट 2 बनाने के लिए, टैग भेजने वाला एक नई key भेजता है और टैग प्राप्त करने वाला अपनी पुरानी key का ID पुष्टि के रूप में भेजता है। दोनों पक्ष DH करते हैं।

टैग सेट 3 बनाने के लिए, टैग भेजने वाला अपनी पुरानी key का ID भेजता है और टैग प्राप्त करने वाले से एक नई key का अनुरोध करता है। दोनों पक्ष एक DH करते हैं।

बाद के tag sets को tag sets 2 और 3 के समान उत्पन्न किया जाता है। tag set संख्या (1 + sender key id + receiver key id) होती है।

```
Tag Sender                    Tag Receiver

                 ... use tag set #0 ...


(Tagset #0 almost empty)
(generate new key #0)

Next Key, forward, request reverse, with key #0  -------->
(repeat until next key received)

                            (generate new key #0, do DH, create IB Tagset #1)

        <-------------      Next Key, reverse, with key #0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #1)


                 ... use tag set #1 ...


(Tagset #1 almost empty)
(generate new key #1)

Next Key, forward, with key #1        -------->
(repeat until next key received)

                            (reuse key #0, do DH, create IB Tagset #2)

        <--------------     Next Key, reverse, id 0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #2)


                 ... use tag set #2 ...


(Tagset #2 almost empty)
(reuse key #1)

Next Key, forward, request reverse, id 1  -------->
(repeat until next key received)

                            (generate new key #1, do DH, create IB Tagset #3)

        <--------------     Next Key, reverse, with key #1

(do DH, create OB Tagset #3)
(reuse key #1, do DH, create IB Tagset #3)



                 ... use tag set #3 ...



     After tag set 3, repeat the above
     patterns as shown for tag sets 2 and 3.

     To create a new even-numbered tag set, the sender sends a new key
     to the receiver. The receiver sends his old key ID
     back as an acknowledgement.

     To create a new odd-numbered tag set, the sender sends a reverse request
     to the receiver. The receiver sends a new reverse key to the sender.
```
जब आउटबाउंड टैगसेट के लिए DH ratchet पूरा हो जाता है, और एक नया आउटबाउंड टैगसेट बनाया जाता है, तो इसका तुरंत उपयोग किया जाना चाहिए, और पुराने आउटबाउंड टैगसेट को हटाया जा सकता है।

जब inbound tagset के लिए DH ratchet पूरा हो जाता है, और एक नया inbound tagset बनाया जाता है, तो receiver को दोनों tagsets में tags को सुनना चाहिए, और लगभग 3 मिनट के छोटे समय के बाद पुराने tagset को delete कर देना चाहिए।

टैग सेट और key ID की प्रगति का सारांश नीचे की तालिका में है। * इंगित करता है कि एक नई key उत्पन्न की गई है।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">New Tag Set ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Sender key ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Rcvr key ID</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65534</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32766</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
</tr>
</table>
Key और tag set ID नंबर क्रमिक होने चाहिए।

##### DH INITIALIZATION KDF

यह एक दिशा के लिए DH_INITIALIZE(rootKey, k) की परिभाषा है। यह एक tagset बनाता है, और एक "अगली root key" बनाता है जिसका उपयोग आवश्यकता होने पर बाद की DH ratchet के लिए किया जाता है।

हम DH initialization का उपयोग तीन स्थानों पर करते हैं। पहले, हम इसका उपयोग New Session Replies के लिए एक tag set उत्पन्न करने के लिए करते हैं। दूसरे, हम इसका उपयोग दो tag sets उत्पन्न करने के लिए करते हैं, प्रत्येक दिशा के लिए एक, Existing Session messages में उपयोग के लिए। अंत में, हम इसका उपयोग DH Ratchet के बाद अतिरिक्त Existing Session messages के लिए एक दिशा में नया tag set उत्पन्न करने के लिए करते हैं।

```
Inputs:
1) rootKey = chainKey from Payload Section
2) k from the New Session KDF or split()

// KDF_RK(rk, dh_out)
keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

// Output 1: The next Root Key (KDF input for the next DH ratchet)
nextRootKey = keydata[0:31]
// Output 2: The chain key to initialize the new
// session tag and symmetric key ratchets
// for the tag set
ck = keydata[32:63]

// session tag and symmetric key chain keys
keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
sessTag_ck = keydata[0:31]
symmKey_ck = keydata[32:63]
```
##### DH RATCHET KDF

यह NextKey blocks में नई DH keys के आदान-प्रदान के बाद उपयोग किया जाता है, tagset के समाप्त होने से पहले।

```
// Tag sender generates new X25519 ephemeral keys
// and sends rapk to tag receiver in a NextKey block
rask = GENERATE_PRIVATE()
rapk = DERIVE_PUBLIC(rask)

// Tag receiver generates new X25519 ephemeral keys
// and sends rbpk to Tag sender in a NextKey block
rbsk = GENERATE_PRIVATE()
rbpk = DERIVE_PUBLIC(rbsk)

sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
rootKey = nextRootKey // from previous tagset in this direction
newTagSet = DH_INITIALIZE(rootKey, tagsetKey)
```
#### 4b) Session Tag Ratchet

हर संदेश के लिए Ratchets, जैसा कि Signal में होता है। session tag ratchet symmetric key ratchet के साथ synchronized होता है, लेकिन receiver key ratchet मेमोरी बचाने के लिए "पीछे रह" सकता है।

ट्रांसमीटर प्रत्येक संदेश भेजे जाने पर एक बार ratchet करता है। कोई अतिरिक्त टैग संग्रहीत करने की आवश्यकता नहीं है। ट्रांसमीटर को 'N' के लिए भी एक काउंटर रखना चाहिए, जो वर्तमान chain में संदेश की message number है। 'N' की वैल्यू भेजे गए संदेश में शामिल की जाती है। Message Number block definition देखें।

Receiver को max window size के आधार पर ratchet को आगे बढ़ाना चाहिए और tags को एक "tag set" में store करना चाहिए, जो session के साथ जुड़ा होता है। एक बार प्राप्त होने के बाद, stored tag को discard किया जा सकता है, और यदि कोई पिछले unreceived tags नहीं हैं, तो window को आगे बढ़ाया जा सकता है। Receiver को प्रत्येक session tag के साथ जुड़े 'N' value को रखना चाहिए, और यह जांचना चाहिए कि भेजे गए message में दी गई संख्या इस value से मेल खाती है। Message Number block definition देखें।

##### KDF

यह RATCHET_TAG() की परिभाषा है।

```
Inputs:
1) Session Tag Chain key sessTag_ck
   First time: output from DH ratchet
   Subsequent times: output from previous session tag ratchet

Generated:
2) input_key_material = SESSTAG_CONSTANT
   Must be unique for this tag set (generated from chain key),
   so that the sequence isn't predictable, since session tags
   go out on the wire in plaintext.

Outputs:
1) N (the current session tag number)
2) the session tag (and symmetric key, probably)
3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

Initialization:
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
// Output 1: Next chain key
sessTag_chainKey = keydata[0:31]
// Output 2: The constant
SESSTAG_CONSTANT = keydata[32:63]

// KDF_ST(ck, constant)
keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_0 = keydata_0[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_0 = keydata_0[32:39]

// repeat as necessary to get to tag_n
keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_n = keydata_n[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_n = keydata_n[32:39]
```
#### 4c) Symmetric Key Ratchet

हर संदेश के लिए Ratchets, जैसा कि Signal में होता है। प्रत्येक symmetric key का एक संबंधित संदेश संख्या और session tag होता है। Session key ratchet, symmetric tag ratchet के साथ synchronized होता है, लेकिन receiver key ratchet मेमोरी बचाने के लिए "पीछे रह" सकता है।

ट्रांसमीटर प्रत्येक भेजे गए संदेश के लिए एक बार ratchet करता है। कोई अतिरिक्त keys स्टोर करने की आवश्यकता नहीं है।

जब receiver को session tag मिलता है, यदि उसने पहले से ही symmetric key ratchet को associated key तक आगे नहीं बढ़ाया है, तो उसे associated key तक "catch up" करना होगा। Receiver संभवतः किसी भी पिछले tags के लिए keys को cache करेगा जो अभी तक प्राप्त नहीं हुए हैं। एक बार प्राप्त होने पर, stored key को discard किया जा सकता है, और यदि कोई पिछले unreceived tags नहीं हैं, तो window को आगे बढ़ाया जा सकता है।

दक्षता के लिए, session tag और symmetric key ratchets अलग हैं ताकि session tag ratchet, symmetric key ratchet से आगे चल सके। यह कुछ अतिरिक्त सुरक्षा भी प्रदान करता है, क्योंकि session tags नेटवर्क पर भेजे जाते हैं।

##### KDF

यह RATCHET_KEY() की परिभाषा है।

```
Inputs:
1) Symmetric Key Chain key symmKey_ck
   First time: output from DH ratchet
   Subsequent times: output from previous symmetric key ratchet

Generated:
2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
   No need for uniqueness. Symmetric keys never go out on the wire.
   TODO: Set a constant anyway?

Outputs:
1) N (the current session key number)
2) the session key
3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

// KDF_CK(ck, constant)
SYMMKEY_CONSTANT = ZEROLEN
// Output 1: Next chain key
keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
// Output 2: The symmetric key
k_0 = keydata_0[32:63]

// repeat as necessary to get to k[n]
keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
// Output 1: Next chain key
symmKey_chainKey_n = keydata_n[0:31]
// Output 2: The symmetric key
k_n = keydata_n[32:63]
```
### 5) Payload

यह ElGamal/AES+SessionTags विशिष्टता में परिभाषित AES section प्रारूप को बदल देता है।

यह उसी block format का उपयोग करता है जो [NTCP2](/docs/specs/ntcp2/) specification में परिभाषित है। व्यक्तिगत block types अलग तरीके से परिभाषित हैं।

इस बात की चिंता है कि implementers को कोड साझा करने के लिए प्रोत्साहित करने से parsing की समस्याएं हो सकती हैं। Implementers को कोड साझा करने के फायदे और जोखिमों पर सावधानीपूर्वक विचार करना चाहिए, और यह सुनिश्चित करना चाहिए कि दोनों contexts के लिए ordering और valid block rules अलग हों।

#### Payload Section डिक्रिप्ट किया गया डेटा

एन्क्रिप्टेड लंबाई डेटा का शेष भाग है। डिक्रिप्टेड लंबाई एन्क्रिप्टेड लंबाई से 16 कम है। सभी ब्लॉक प्रकार समर्थित हैं। विशिष्ट सामग्री में निम्नलिखित ब्लॉक शामिल हैं:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Block Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Number</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Block Length</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DateTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Termination (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Options (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21+</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Number (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Next Key</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3 or 35</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic Clove</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Padding</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
</table>
#### असंख्यीकृत डेटा

एन्क्रिप्टेड फ्रेम में शून्य या अधिक ब्लॉक होते हैं। प्रत्येक ब्लॉक में एक बाइट का आइडेंटिफायर, दो बाइट की लंबाई, और शून्य या अधिक बाइट्स का डेटा होता है।

विस्तारशीलता के लिए, प्राप्तकर्ताओं को अज्ञात प्रकार संख्याओं वाले ब्लॉक्स को अनदेखा करना चाहिए, और उन्हें padding के रूप में मानना चाहिए।

एन्क्रिप्टेड डेटा अधिकतम 65535 बाइट्स है, जिसमें 16-बाइट authentication header शामिल है, इसलिए अधिकतम अनएन्क्रिप्टेड डेटा 65519 बाइट्स है।

(Poly1305 auth tag दिखाया नहीं गया):

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
       0 datetime
       1-3 reserved
       4 termination
       5 options
       6 previous message number
       7 next session key
       8 ack
       9 ack request
       10 reserved
       11 Garlic Clove
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
#### ब्लॉक क्रम नियम

New Session संदेश में, DateTime ब्लॉक आवश्यक है, और यह पहला ब्लॉक होना चाहिए।

अन्य अनुमतित ब्लॉक्स:

- Garlic Clove (type 11)
- विकल्प (type 5)
- Padding (type 254)

New Session Reply संदेश में, कोई blocks की आवश्यकता नहीं है।

अन्य अनुमतित ब्लॉक्स:

- Garlic Clove (type 11)
- विकल्प (type 5)
- Padding (type 254)

कोई अन्य blocks की अनुमति नहीं है। Padding, यदि मौजूद है, तो वह अंतिम block होना चाहिए।

Existing Session संदेश में, कोई blocks आवश्यक नहीं हैं, और क्रम निर्दिष्ट नहीं है, निम्नलिखित आवश्यकताओं को छोड़कर:

Termination, यदि मौजूद है, तो Padding को छोड़कर अंतिम block होना चाहिए। Padding, यदि मौजूद है, तो अंतिम block होना चाहिए।

एक ही फ्रेम में कई Garlic Clove ब्लॉक हो सकते हैं। एक ही फ्रेम में अधिकतम दो Next Key ब्लॉक हो सकते हैं। एक ही फ्रेम में कई Padding ब्लॉक की अनुमति नहीं है। अन्य ब्लॉक प्रकारों में शायद एक ही फ्रेम में कई ब्लॉक नहीं होंगे, लेकिन इसे प्रतिबंधित नहीं किया गया है।

#### DateTime

एक समाप्ति। replay prevention में सहायता करता है। Bob को इस timestamp का उपयोग करके यह validate करना होगा कि संदेश हाल ही का है। Bob को replay attacks को रोकने के लिए Bloom filter या अन्य mechanism implement करना होगा, यदि समय वैध है। Bob एक duplicate ephemeral key (Elligator2 decode से पहले या बाद में) के लिए पहले से replay detection check का भी उपयोग कर सकता है ताकि decryption से पहले हाल की duplicate NS messages को detect करके drop कर सके। आम तौर पर केवल New Session messages में शामिल किया जाता है।

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
#### Garlic Clove

[I2NP](/docs/specs/i2np/) में निर्दिष्ट एक single decrypted Garlic Clove, जिसमें उन fields को हटाने के लिए modifications की गई हैं जो unused या redundant हैं। चेतावनी: यह format ElGamal/AES के लिए उपयोग किए जाने वाले format से काफी अलग है। प्रत्येक clove एक अलग payload block है। Garlic Cloves को blocks के across या ChaChaPoly frames के across fragment नहीं किया जा सकता।

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration   
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

size :: size of all data to follow

Delivery Instructions :: As specified in
       the Garlic Clove section of [I2NP]_.
       Length varies but is typically 1, 33, or 37 bytes

type :: I2NP message type

Message_ID :: 4 byte `Integer` I2NP message ID

Expiration :: 4 bytes, seconds since the epoch
```
नोट्स:

- कार्यान्वयनकर्ताओं को यह सुनिश्चित करना चाहिए कि जब एक block पढ़ा जाता है, तो गलत या दुर्भावनापूर्ण data के कारण reads अगले block में overrun न हों।
- [I2NP](/docs/specs/i2np/) में निर्दिष्ट Clove Set format का उपयोग नहीं किया जाता है। प्रत्येक clove अपने स्वयं के block में समाहित है।
- I2NP message header 9 bytes का है, जो [NTCP2](/docs/specs/ntcp2/) में उपयोग किए गए format के समान है।
- [I2NP](/docs/specs/i2np/) में Garlic Message परिभाषा से Certificate, Message ID, और Expiration शामिल नहीं हैं।
- [I2NP](/docs/specs/i2np/) में Garlic Clove परिभाषा से Certificate, Clove ID, और Expiration शामिल नहीं हैं।

#### समाप्ति

कार्यान्वयन वैकल्पिक है। सेशन को बंद करें। यह फ्रेम में अंतिम गैर-पैडिंग ब्लॉक होना चाहिए। इस सेशन में कोई और संदेश नहीं भेजे जाएंगे।

NS या NSR में अनुमतित नहीं है। केवल Existing Session संदेशों में शामिल किया जाता है।

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 1 or more
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       others: optional, impementation-specific
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### विकल्प

UNIMPLEMENTED, आगे के अध्ययन के लिए। अपडेटेड विकल्प पास करें। विकल्पों में सेशन के लिए विभिन्न पैरामीटर शामिल हैं। अधिक जानकारी के लिए नीचे Session Tag Length Analysis अनुभाग देखें।

options ब्लॉक परिवर्तनीय लंबाई का हो सकता है, क्योंकि more_options उपस्थित हो सकते हैं।

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 5
size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
ver :: Protocol version, must be 0
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
STL :: Session tag length (must be 8), other values unimplemented
STimeout :: Session idle timeout (seconds), big endian
SOTW :: Sender Outbound Tag Window, 2 bytes big endian
RITW :: Receiver Inbound Tag Window 2 bytes big endian

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

more_options :: Format undefined, for future use
```
SOTW भेजने वाले की तरफ से प्राप्तकर्ता के लिए प्राप्तकर्ता की inbound tag window (अधिकतम lookahead) के लिए सिफारिश है। RITW भेजने वाले की inbound tag window (अधिकतम lookahead) की घोषणा है जिसका वह उपयोग करने की योजना बना रहा है। इसके बाद प्रत्येक पक्ष कुछ न्यूनतम या अधिकतम या अन्य गणना के आधार पर lookahead को सेट या समायोजित करता है।

नोट्स:

- गैर-डिफ़ॉल्ट session tag length के लिए समर्थन की उम्मीद है कि कभी भी आवश्यक नहीं होगा।
- Tag window Signal दस्तावेज़ में MAX_SKIP है।

समस्याएं:

- विकल्प बातचीत अभी तय होना है (TBD)।
- डिफ़ॉल्ट अभी तय होना है (TBD)।
- पैडिंग और देरी के विकल्प NTCP2 से कॉपी किए गए हैं, लेकिन वे विकल्प
  वहाँ पूरी तरह से लागू या अध्ययन नहीं किए गए हैं।

#### संदेश संख्याएं

Implementation वैकल्पिक है। पिछले tag set (PN) में length (भेजे गए messages की संख्या)। Receiver PN से अधिक tags को पिछले tag set से तुरंत delete कर सकता है। Receiver PN से कम या बराबर tags को पिछले tag set से थोड़े समय बाद (जैसे 2 मिनट) expire कर सकता है।

```
+----+----+----+----+----+
| 6  |  size   |  PN    |
+----+----+----+----+----+

blk :: 6
size :: 2
PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.
```
नोट्स:

- अधिकतम PN 65535 है।
- PN की परिभाषा Signal की परिभाषा के बराबर है, घटाकर एक।
  यह Signal के समान है, लेकिन Signal में, PN और N header में होते हैं। यहाँ, वे encrypted message body में हैं।
- इस block को tag set 0 में न भेजें, क्योंकि कोई पिछला tag
  set नहीं था।

#### अगली DH Ratchet Public Key

अगली DH ratchet key payload में है, और यह वैकल्पिक है। हम हर बार ratchet नहीं करते। (यह signal से अलग है, जहाँ यह header में होती है, और हर बार भेजी जाती है)

पहले ratchet के लिए, Key ID = 0।

NS या NSR में अनुमति नहीं है। केवल Existing Session संदेशों में शामिल किया जाता है।

```
+----+----+----+----+----+----+----+----+
| 7  |  size   |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+                                       +
|     Next DH Ratchet Public Key        |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

blk :: 7
size :: 3 or 35
flag :: 1 byte flags
        bit order: 76543210
        bit 0: 1 for key present, 0 for no key present
        bit 1: 1 for reverse key, 0 for forward key
        bit 2: 1 to request reverse key, 0 for no request
               only set if bit 1 is 0
        bits 7-2: Unused, set to 0 for future compatibility
key ID :: The key ID of this key. 2 bytes, big endian
          0 - 32767
Public Key :: The next X25519 public key, 32 bytes, little endian
              Only if bit 0 is 1
```
नोट्स:

- Key ID उस tag set के लिए उपयोग की जाने वाली local key के लिए एक incrementing counter है, जो 0 से शुरू होता है।
- ID तब तक नहीं बदलना चाहिए जब तक key न बदले।
- यह strictly आवश्यक नहीं हो सकता है, लेकिन debugging के लिए उपयोगी है। Signal key ID का उपयोग नहीं करता।
- अधिकतम Key ID 32767 है।
- दुर्लभ मामले में जब दोनों दिशाओं में tag sets एक ही समय में ratcheting कर रहे हों, तो एक frame में दो Next Key blocks होंगे, एक forward key के लिए और एक reverse key के लिए।
- Key और tag set ID numbers sequential होने चाहिए।
- विवरण के लिए ऊपर DH Ratchet section देखें।

#### स्वीकृति

यह केवल तभी भेजा जाता है जब एक ack request block प्राप्त हुआ हो। कई संदेशों की ack के लिए कई acks मौजूद हो सकते हैं।

NS या NSR में अनुमति नहीं है। केवल Existing Session संदेशों में शामिल किया गया है।

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|             more acks                 |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 8
size :: 4 * number of acks to follow, minimum 1 ack
for each ack:
tagsetid :: 2 bytes, big endian, from the message being acked
N :: 2 bytes, big endian, from the message being acked
```
नोट्स:

- टैग सेट ID और N ack किए जा रहे संदेश की विशिष्ट पहचान करते हैं।
- प्रत्येक दिशा में सत्र के लिए उपयोग किए जाने वाले पहले टैग सेट में, टैग
  सेट ID 0 होता है।
- कोई NextKey ब्लॉक नहीं भेजे गए हैं, इसलिए कोई key ID नहीं हैं।
- NextKey एक्सचेंज के बाद उपयोग किए जाने वाले सभी टैग सेट के लिए, टैग सेट नंबर
  (1 + Alice's key ID + Bob's key ID) होता है।

#### Ack Request

एक in-band ack का अनुरोध करें। Garlic Clove में out-of-band DeliveryStatus Message को बदलने के लिए।

यदि एक स्पष्ट ack का अनुरोध किया गया है, तो वर्तमान tagset ID और message number (N) को एक ack block में वापस किया जाता है।

NS या NSR में अनुमतित नहीं। केवल Existing Session संदेशों में शामिल किया गया।

```
+----+----+----+----+
|  9 |  size   |flg |
+----+----+----+----+

blk :: 9
size :: 1
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
```
#### पैडिंग

सभी padding AEAD frames के अंदर है। TODO AEAD के अंदर padding को मोटे तौर पर negotiated parameters का पालन करना चाहिए। TODO Alice ने NS message में अपने requested tx/rx min/max parameters भेजे। TODO Bob ने NSR message में अपने requested tx/rx min/max parameters भेजे। Data phase के दौरान updated options भेजे जा सकते हैं। ऊपर दी गई options block जानकारी देखें।

यदि उपस्थित है, तो यह frame में अंतिम block होना चाहिए।

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 254
size :: 2 bytes, big endian, 0-65516
padding :: zeros or random data
```
नोट्स:

- ऑल-जीरो पैडिंग ठीक है, क्योंकि यह एन्क्रिप्ट हो जाएगा।
- पैडिंग रणनीतियां TBD।
- केवल-पैडिंग फ्रेम की अनुमति है।
- पैडिंग डिफ़ॉल्ट 0-15 बाइट्स है।
- पैडिंग पैरामीटर नेगोसिएशन के लिए options ब्लॉक देखें
- min/max पैडिंग पैरामीटर के लिए options ब्लॉक देखें
- नेगोसिएट किए गए पैडिंग के उल्लंघन पर router प्रतिक्रिया
  implementation-dependent है।

#### अन्य block प्रकार

भविष्य की संगतता के लिए implementations को अज्ञात block प्रकारों को नजरअंदाज करना चाहिए।

#### भविष्य का काम

- padding की लंबाई या तो प्रत्येक संदेश के आधार पर और लंबाई वितरण के अनुमानों के आधार पर तय की जानी चाहिए, या random delays जोड़े जाने चाहिए। ये प्रतिरोधी उपाय DPI का विरोध करने के लिए शामिल किए जाने हैं, क्योंकि संदेश के आकार अन्यथा यह प्रकट कर देंगे कि I2P traffic को transport protocol द्वारा ले जाया जा रहा है। सटीक padding scheme भविष्य के कार्य का एक क्षेत्र है, Appendix A इस विषय पर अधिक जानकारी प्रदान करता है।

## सामान्य उपयोग पैटर्न

### HTTP GET

यह सबसे सामान्य उपयोग मामला है, और अधिकांश गैर-HTTP streaming उपयोग मामले भी इस उपयोग मामले के समान होंगे। एक छोटा प्रारंभिक संदेश भेजा जाता है, एक उत्तर मिलता है, और दोनों दिशाओं में अतिरिक्त संदेश भेजे जाते हैं।

एक HTTP GET आमतौर पर एक single I2NP message में फिट हो जाता है। Alice एक छोटा request भेजती है एक single new Session message के साथ, एक reply leaseset को bundle करते हुए। Alice तुरंत नई key पर ratchet शामिल करती है। destination के साथ bind करने के लिए sig शामिल करता है। कोई ack requested नहीं।

Bob तुरंत ratchet करता है।

Alice तुरंत ratchet करती है।

उन सत्रों के साथ जारी रहता है।

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5
```
### HTTP POST

Alice के पास तीन विकल्प हैं:

1) केवल पहला संदेश भेजें (window size = 1), जैसे HTTP GET में। नहीं

    recommended.
2) streaming window तक भेजें, लेकिन same Elligator2-encoded का उपयोग करते हुए

    cleartext public key. All messages contain same next public key
    (ratchet). This will be visible to OBGW/IBEP because they all start
    with the same cleartext. Things proceed as in 1). Not recommended.
3) अनुशंसित कार्यान्वयन। streaming window तक भेजें, लेकिन एक

    different Elligator2-encoded cleartext public key (session) for
    each. All messages contain same next public key (ratchet). This will
    not be visible to OBGW/IBEP because they all start with different
    cleartext. Bob must recognize that they all contain the same next
    public key, and respond to all with the same ratchet. Alice uses
    that next public key and continues.

विकल्प 3 संदेश प्रवाह:

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack
```
### उत्तर देने योग्य डेटाग्राम

एक एकल संदेश, जिसकी एक एकल प्रतिक्रिया अपेक्षित है। अतिरिक्त संदेश या प्रतिक्रियाएं भेजी जा सकती हैं।

HTTP GET के समान, लेकिन session tag window size और lifetime के लिए छोटे विकल्पों के साथ। शायद ratchet का अनुरोध न करें।

```
Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message
```
### मल्टिपल रॉ डेटाग्राम

कई गुमनाम संदेश, जिनका कोई जवाब अपेक्षित नहीं है।

इस परिदृश्य में, Alice एक session का अनुरोध करती है, लेकिन binding के बिना। नया session message भेजा जाता है। कोई reply LS bundled नहीं है। एक reply DSM bundled है (यह एकमात्र उपयोग मामला है जिसके लिए bundled DSMs की आवश्यकता होती है)। कोई next key शामिल नहीं है। कोई reply या ratchet का अनुरोध नहीं किया गया है। कोई ratchet नहीं भेजा गया है। Options session tags window को शून्य पर सेट करते हैं।

```
Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->
```
### एकल कच्चा डेटाग्राम

एक एकल गुमनाम संदेश, जिसका कोई उत्तर अपेक्षित नहीं है।

एक-बार संदेश भेजा गया है। कोई reply LS या DSM bundled नहीं हैं। कोई next key शामिल नहीं है। कोई reply या ratchet का अनुरोध नहीं है। कोई ratchet नहीं भेजा गया। Options ने session tags window को शून्य पर सेट किया है।

```
Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message
```
### दीर्घकालिक सत्र

लंबे समय तक चलने वाले सेशन किसी भी समय ratchet कर सकते हैं, या ratchet का अनुरोध कर सकते हैं, ताकि उस समय बिंदु से forward secrecy बनाए रख सकें। सेशन को ratchet करना होगा जब वे प्रति-सेशन भेजे गए संदेशों की सीमा (65535) के पास पहुँच जाते हैं।

## कार्यान्वयन संबंधी विचार

### रक्षा

मौजूदा ElGamal/AES+SessionTag प्रोटोकॉल की तरह, implementations को session tag storage को सीमित करना चाहिए और memory exhaustion attacks से सुरक्षा प्रदान करनी चाहिए।

कुछ अनुशंसित रणनीतियों में शामिल हैं:

- संग्रहीत session tags की संख्या पर कठोर सीमा
- मेमोरी दबाव के दौरान निष्क्रिय inbound sessions की आक्रामक समाप्ति
- एकल दूरस्थ गंतव्य से जुड़े inbound sessions की संख्या पर सीमा
- मेमोरी दबाव के दौरान session tag window का अनुकूली कमी और पुराने अप्रयुक्त 
  tags का हटाना
- मेमोरी दबाव की स्थिति में, अनुरोध करने पर ratchet करने से इनकार

### पैरामीटर

अनुशंसित पैरामीटर और टाइमआउट:

- NSR tagset आकार: 12 tsmin और tsmax
- ES tagset 0 आकार: tsmin 24, tsmax 160
- ES tagset (1+) आकार: 160 tsmin और tsmax
- NSR tagset timeout: receiver के लिए 3 मिनट
- ES tagset timeout: sender के लिए 8 मिनट, receiver के लिए 10 मिनट
- पिछले ES tagset को हटाने के बाद: 3 मिनट
- Tag N की tagset look ahead: min(tsmax, tsmin + N/4)
- Tag N के पीछे tagset trim: min(tsmax, tsmin + N/4) / 2
- अगली key भेजें tag पर: 4096
- Tagset lifetime के बाद अगली key भेजें: TBD
- Session को बदलें अगर NS प्राप्त हुआ इसके बाद: 3 मिनट
- Max clock skew: -5 मिनट से +2 मिनट तक
- NS replay filter अवधि: 5 मिनट
- Padding आकार: 0-15 bytes (अन्य रणनीतियाँ TBD)

### वर्गीकरण

आने वाले संदेशों को वर्गीकृत करने के लिए निम्नलिखित सिफारिशें हैं।

#### केवल X25519

एक tunnel पर जो केवल इस protocol के साथ उपयोग किया जाता है, पहचान वैसे ही करें जैसे वर्तमान में ElGamal/AES+SessionTags के साथ की जाती है:

पहले, प्रारंभिक डेटा को एक session tag के रूप में मानें, और session tag को खोजें। यदि मिल जाए, तो उस session tag से जुड़े संग्रहीत डेटा का उपयोग करके डिक्रिप्ट करें।

यदि नहीं मिला, तो प्रारंभिक डेटा को DH public key और nonce के रूप में मानें। DH ऑपरेशन और निर्दिष्ट KDF करें, और शेष डेटा को decrypt करने का प्रयास करें।

#### X25519 को ElGamal/AES+SessionTags के साथ साझा किया गया

एक tunnel पर जो इस protocol और ElGamal/AES+SessionTags दोनों को support करता है, आने वाले messages को इस प्रकार classify करें:

ElGamal/AES+SessionTags स्पेसिफिकेशन में एक त्रुटि के कारण, AES ब्लॉक को एक यादृच्छिक non-mod-16 लंबाई तक पैड नहीं किया जाता है। इसलिए, मौजूदा सेशन संदेशों की लंबाई mod 16 हमेशा 0 होती है, और नए सेशन संदेशों की लंबाई mod 16 हमेशा 2 होती है (चूंकि ElGamal ब्लॉक 514 बाइट्स लंबा है)।

यदि length mod 16 शून्य या 2 नहीं है, तो प्रारंभिक डेटा को एक session tag के रूप में मानें, और उस session tag को खोजें। यदि मिल जाए, तो उस session tag से जुड़े संग्रहीत डेटा का उपयोग करके decrypt करें।

यदि नहीं मिला, और length mod 16, 0 या 2 नहीं है, तो प्रारंभिक डेटा को DH public key और nonce के रूप में मानें। एक DH ऑपरेशन और निर्दिष्ट KDF करें, और शेष डेटा को डिक्रिप्ट करने का प्रयास करें। (सापेक्षिक ट्रैफिक मिश्रण और X25519 तथा ElGamal DH ऑपरेशन की सापेक्षिक लागतों के आधार पर, यह चरण अंत में भी किया जा सकता है)

अन्यथा, यदि length mod 16 शून्य है, तो प्रारंभिक डेटा को ElGamal/AES session tag के रूप में मानें, और session tag को खोजें। यदि मिल जाता है, तो उस session tag के साथ संग्रहीत डेटा का उपयोग करके decrypt करें।

यदि नहीं मिला, और डेटा कम से कम 642 (514 + 128) बाइट्स लंबा है, और लेंथ mod 16 का परिणाम 2 है, तो प्रारंभिक डेटा को ElGamal block के रूप में मानें। बचे हुए डेटा को decrypt करने का प्रयास करें।

ध्यान दें कि यदि ElGamal/AES+SessionTag spec को non-mod-16 padding की अनुमति देने के लिए अपडेट किया जाता है, तो चीजों को अलग तरीके से करना होगा।

### पुनः प्रसारण और स्थिति परिवर्तन

ratchet layer पुनः प्रेषण नहीं करता है, और दो अपवादों को छोड़कर, प्रेषण के लिए टाइमर का उपयोग नहीं करता है। tagset timeout के लिए भी टाइमर की आवश्यकता होती है।

ट्रांसमिशन टाइमर केवल NSR भेजने के लिए और ES के साथ उत्तर देने के लिए उपयोग किए जाते हैं जब प्राप्त ES में ACK अनुरोध होता है। अनुशंसित टाइमआउट एक सेकंड है। लगभग सभी मामलों में, उच्च स्तर (डेटाग्राम या स्ट्रीमिंग) उत्तर देगा, NSR या ES को मजबूर करेगा, और टाइमर को रद्द किया जा सकता है। यदि टाइमर चलता है, तो NSR या ES के साथ एक खाली पेलोड भेजें।

#### Ratchet-layer प्रतिक्रियाएं

प्रारंभिक implementations उच्च स्तरों पर द्विदिशीय ट्रैफिक पर निर्भर करते हैं। यानी, implementations यह मानते हैं कि विपरीत दिशा में ट्रैफिक जल्द ही प्रसारित होगा, जो ECIES layer पर किसी भी आवश्यक response को मजबूर करेगा।

हालांकि, कुछ ट्रैफिक एकदिशीय या बहुत कम बैंडविड्थ का हो सकता है, जिससे समय पर प्रतिक्रिया उत्पन्न करने के लिए कोई उच्च-स्तरीय ट्रैफिक नहीं होता।

NS और NSR संदेशों की प्राप्ति के लिए एक प्रतिक्रिया की आवश्यकता होती है; ACK Request और Next Key blocks की प्राप्ति के लिए भी एक प्रतिक्रिया की आवश्यकता होती है।

implementations को इनमें से किसी भी संदेश को प्राप्त करने पर एक timer शुरू करना चाहिए जिसके लिए response की आवश्यकता होती है, और यदि कम समय (जैसे 1 सेकंड) में कोई reverse traffic नहीं भेजा जाता है तो ECIES layer पर एक "empty" (कोई Garlic Clove block नहीं) response generate करना चाहिए।

NS और NSR messages के responses के लिए और भी छोटा timeout उपयुक्त हो सकता है, ताकि traffic को जल्द से जल्द कुशल ES messages पर shift किया जा सके।

#### NSR के लिए NS बाइंडिंग

ratchet layer पर, Bob के रूप में, Alice केवल static key द्वारा जानी जाती है। NS message प्रमाणित है ([Noise](https://noiseprotocol.org/noise.html) IK sender authentication 1)। हालांकि, ratchet layer के लिए Alice को कुछ भी भेजने में सक्षम होने के लिए यह पर्याप्त नहीं है, क्योंकि network routing के लिए एक पूर्ण Destination की आवश्यकता होती है।

NSR भेजे जाने से पहले, Alice का पूरा Destination या तो ratchet layer द्वारा या एक उच्च-स्तरीय repliable protocol द्वारा खोजा जाना चाहिए, जो या तो repliable [Datagrams](/docs/specs/datagrams/) या [Streaming](/docs/specs/streaming/) हो। उस Destination के लिए Leaseset खोजने के बाद, उस Leaseset में वही static key होगी जो NS में निहित है।

आमतौर पर, उच्च स्तर प्रतिक्रिया करेगा, जो Alice के Destination Hash द्वारा Alice के Leaseset की network database lookup को मजबूर करता है। वह Leaseset लगभग हमेशा स्थानीय रूप से मिल जाएगा, क्योंकि NS में एक Garlic Clove block था, जिसमें Database Store message था, जिसमें Alice का Leaseset था।

Bob के लिए ratchet-layer NSR भेजने की तैयारी करने और pending session को Alice के Destination से bind करने के लिए, Bob को NS payload को process करते समय Destination को "capture" करना चाहिए। यदि एक Database Store message मिलता है जिसमें एक Leaseset है जिसकी key NS में static key से match करती है, तो pending session अब उस Destination से bind हो जाता है, और Bob जानता है कि response timer की अवधि समाप्त होने पर कोई NSR कहाँ भेजना है। यह recommended implementation है।

एक वैकल्पिक डिज़ाइन यह है कि एक cache या database बनाए रखा जाए जहाँ static key को Destination के साथ mapped किया जाए। इस approach की सुरक्षा और व्यावहारिकता आगे के अध्ययन का विषय है।

न तो यह specification और न ही अन्य specifications सख्ती से यह require करती हैं कि हर NS में Alice का Leaseset हो। हालांकि, व्यावहारिक रूप से, इसमें होना चाहिए। अनुशंसित ES tagset sender timeout (8 मिनट) maximum Leaseset timeout (10 मिनट) से कम है, इसलिए एक छोटी सी अवधि हो सकती है जहां पिछला session समाप्त हो गया हो, Alice को लगता हो कि Bob के पास अभी भी उसका valid Leaseset है, और वह नए NS के साथ नया Leaseset नहीं भेजती। यह आगे के अध्ययन का विषय है।

#### कई NS संदेश

यदि उच्च स्तर (datagram या streaming) द्वारा अधिक डेटा भेजने से पहले कोई NSR response प्राप्त नहीं होता है, संभवतः retransmission के रूप में, Alice को एक नई ephemeral key का उपयोग करके एक नया NS तैयार करना चाहिए। किसी भी पिछले NS से ephemeral key का पुन: उपयोग न करें। Alice को अतिरिक्त handshake state और derived receive tagset बनाए रखना चाहिए, ताकि भेजे गए किसी भी NSR के जवाब में NSR messages प्राप्त कर सके।

कार्यान्वयन भेजे गए NS संदेशों की कुल संख्या को सीमित कर सकते हैं, या NS संदेश भेजने की दर को सीमित कर सकते हैं, या तो उच्च स्तरीय संदेशों को भेजे जाने से पहले कतार में रखकर या छोड़कर।

कुछ स्थितियों में, जब अधिक लोड के तहत हो, या कुछ विशेष हमले के परिदृश्यों में, Bob के लिए यह उपयुक्त हो सकता है कि वह संसाधन समाप्ति हमले से बचने के लिए NS संदेशों को decrypt करने का प्रयास किए बिना ही queue, drop, या सीमित कर दे।

प्रत्येक NS प्राप्त होने पर, Bob एक NSR outbound tagset उत्पन्न करता है, एक NSR भेजता है, split() करता है, और inbound और outbound ES tagsets उत्पन्न करता है। हालांकि, Bob तब तक कोई ES संदेश नहीं भेजता जब तक कि संबंधित inbound tagset पर पहला ES संदेश प्राप्त नहीं हो जाता। उसके बाद, Bob किसी भी अन्य NS प्राप्त या NSR भेजे गए के लिए सभी handshake states और tagsets को त्याग सकता है, या उन्हें जल्दी expire होने दे सकता है। ES संदेशों के लिए NSR tagsets का उपयोग न करें।

यह आगे के अध्ययन का विषय है कि क्या Bob NSR के तुरंत बाद, Alice से पहला ES प्राप्त करने से पहले ही, अनुमानित रूप से ES संदेश भेजना चुन सकता है। कुछ परिस्थितियों और ट्रैफिक पैटर्न में, यह काफी बैंडविड्थ और CPU बचा सकता है। यह रणनीति हेयूरिस्टिक्स पर आधारित हो सकती है जैसे कि ट्रैफिक पैटर्न, पहले session के tagset पर प्राप्त ESs का प्रतिशत, या अन्य डेटा।

#### अनेकों NSR संदेश

प्रत्येक NS संदेश प्राप्त होने पर, जब तक ES संदेश प्राप्त नहीं होता, Bob को एक नया NSR भेजना होगा, या तो उच्च स्तरीय ट्रैफिक भेजे जाने के कारण, या NSR भेजने के टाइमर की समय सीमा समाप्त होने के कारण।

प्रत्येक NSR आने वाले NS के अनुरूप handshake state और tagset का उपयोग करता है। Bob को सभी प्राप्त NS संदेशों के लिए handshake state और tagset को तब तक बनाए रखना चाहिए जब तक ES संदेश प्राप्त नहीं हो जाता।

Implementation कुल भेजे गए NSR संदेशों की संख्या या NSR संदेश भेजने की दर को सीमित कर सकते हैं, या तो उच्च स्तर के संदेशों को भेजने से पहले queue में डालकर या drop करके। ये सीमाएं या तो आने वाले NS संदेशों के कारण या अतिरिक्त उच्च स्तर के outbound traffic के कारण लगाई जा सकती हैं।

कुछ स्थितियों में, जब उच्च लोड के तहत हो, या कुछ आक्रमण परिदृश्यों के तहत हो, तो Alice के लिए यह उपयुक्त हो सकता है कि वह NSR messages को decrypt करने का प्रयास किए बिना queue, drop, या limit करे, ताकि resource exhaustion attack से बचा जा सके। ये सीमाएं सभी sessions में कुल मिलाकर, प्रति session, या दोनों हो सकती हैं।

एक बार Alice को NSR प्राप्त हो जाने के बाद, Alice ES session keys प्राप्त करने के लिए split() करता है। Alice को एक timer सेट करना चाहिए, और यदि higher layer कोई traffic नहीं भेजता है तो एक empty ES message भेजना चाहिए, आमतौर पर एक सेकंड के भीतर।

अन्य inbound NSR tagsets को जल्द ही हटा दिया जा सकता है या उन्हें समाप्त होने दिया जा सकता है, लेकिन Alice को उन्हें थोड़ी देर के लिए रखना चाहिए, ताकि प्राप्त होने वाले किसी भी अन्य NSR संदेशों को decrypt किया जा सके।

### पुनरावृत्ति रोकथाम

Bob को NS replay attacks को रोकने के लिए Bloom filter या अन्य तंत्र लागू करना चाहिए, यदि शामिल DateTime हाल का है, और उन NS संदेशों को अस्वीकार करना चाहिए जहाँ DateTime बहुत पुराना है। Bob decryption से पहले हाल के duplicate NS संदेशों को detect और drop करने के लिए duplicate ephemeral key (Elligator2 decode से पहले या बाद में) के लिए एक पहले से replay detection check का भी उपयोग कर सकता है।

NSR और ES संदेशों में अंतर्निहित रूप से रीप्ले रोकथाम है क्योंकि session tag एक बार के उपयोग का है।

Garlic messages में replay prevention भी होती है यदि router एक router-wide Bloom filter implement करता है जो I2NP message ID पर आधारित है।

## संबंधित परिवर्तन

ECIES Destinations से Database Lookups: देखें [Prop154](/proposals/154-ratchet/), अब [I2NP](/docs/specs/i2np/) में रिलीज़ 0.9.46 के लिए शामिल किया गया है।

यह specification में leaseset के साथ X25519 public key प्रकाशित करने के लिए LS2 समर्थन की आवश्यकता है। [I2NP](/docs/specs/i2np/) में LS2 specifications में कोई परिवर्तन की आवश्यकता नहीं है। सभी समर्थन को [Prop123](/proposals/123-new-netdb-entries/) में डिज़ाइन, निर्दिष्ट और कार्यान्वित किया गया था जो 0.9.38 में implemented है।

इस specification के लिए I2CP options में एक property को enable करने के लिए set करना आवश्यक है। सभी support को [Prop123](/proposals/123-new-netdb-entries/) में design, specify, और implement किया गया था जो 0.9.38 में implement किया गया।

ECIES को सक्षम करने के लिए आवश्यक विकल्प I2CP, BOB, SAM, या i2ptunnel के लिए एक एकल I2CP प्रॉपर्टी है।

सामान्य मान हैं केवल ECIES के लिए i2cp.leaseSetEncType=4, या ECIES और ElGamal दोहरी keys के लिए i2cp.leaseSetEncType=4,0।

## संगतता

LS2 को dual keys के साथ support करने वाला कोई भी router (0.9.38 या उससे ऊपर) dual keys वाले destinations से connection को support करना चाहिए।

ECIES-only destinations को encrypted lookup replies प्राप्त करने के लिए अधिकांश floodfills का 0.9.46 में अपडेट होना आवश्यक है। देखें [Prop154](/proposals/154-ratchet/)।

ECIES-only destinations केवल उन अन्य destinations के साथ connect कर सकते हैं जो या तो ECIES-only हैं, या dual-key हैं।

## संदर्भ

- [Common](/docs/specs/common-structures/)
- [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- [Datagrams](/docs/specs/datagrams/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ElG-AES](/docs/specs/elgamal-aes/)
- [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) - [Elligator लेख](https://www.imperialviolet.org/2013/12/25/elligator.html) और OBFS4 code भी देखें
- [GARLICSPEC](/docs/overview/garlic-routing/)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop111](/proposals/111-ntcp2/)
- [Prop123](/proposals/123-new-netdb-entries/)
- [Prop142](/proposals/142-ecies-template/)
- [Prop144](/proposals/144-ecies-x25519/)
- [Prop145](/proposals/145-ecies-ecdh-aes/)
- [Prop152](/proposals/152-ecies-config/)
- [Prop153](/proposals/153-chacha20-layer/)
- [Prop154](/proposals/154-ratchet/)
- [RFC-2104](https://tools.ietf.org/html/rfc2104)
- [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
- [RFC-5869](https://tools.ietf.org/html/rfc5869)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [Signal](https://signal.org/docs/specifications/doubleratchet/)
- [SSU](/docs/transport/ssu/)
- [SSU2](/docs/specs/ssu2/)
- [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) - Diffie, W.; van Oorschot P. C.; Wiener M. J., Authentication and Authenticated Key Exchanges
- [Streaming](/docs/specs/streaming/)
