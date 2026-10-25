---
title: "NTCP (NIO-based TCP)"
description: "I2P के लिए लेगेसी Java NIO-आधारित TCP ट्रांसपोर्ट, जिसे NTCP2 द्वारा प्रतिस्थापित किया गया"
slug: "ntcp"
aliases:
  - "/hi/docs/transport/ntcp"
  - "/hi/docs/transport/ntcp/"
  - "/hi/docs/ntcp"
  - "/hi/docs/ntcp/"
  - "/hi/ntcp"
  - "/hi/ntcp/"
lastUpdated: "2021-10"
accurateFor: "0.9.52"
---

अप्रचलित, अब समर्थित नहीं। 0.9.40 2019-05 से डिफ़ॉल्ट रूप से अक्षम। 0.9.50 2021-05 से समर्थन हटा दिया गया। [NTCP2](/docs/specs/ntcp2) द्वारा प्रतिस्थापित। NTCP एक Java NIO-आधारित ट्रांसपोर्ट है जो I2P रिलीज़ 0.6.1.22 में पेश किया गया था। Java NIO (new I/O) पुराने TCP ट्रांसपोर्ट की प्रति कनेक्शन 1 thread की समस्याओं से पीड़ित नहीं है। NTCP-over-IPv6 संस्करण 0.9.8 से समर्थित है।

डिफ़ॉल्ट रूप से, NTCP उस IP/Port का उपयोग करता है जो SSU द्वारा स्वचालित रूप से पहचाना जाता है। config.jsp पर सक्षम होने पर, SSU बाहरी पता बदलने या firewall स्थिति बदलने पर NTCP को सूचित/पुनः आरंभ करेगा। अब आप स्थिर IP या dyndns सेवा के बिना inbound TCP को सक्षम कर सकते हैं।

I2P के भीतर NTCP कोड अपेक्षाकृत हल्का है (SSU कोड के आकार का 1/4) क्योंकि यह विश्वसनीय डिलीवरी के लिए अंतर्निहित Java TCP transport का उपयोग करता है।

## Router Address विशिष्टता {#ra}

निम्नलिखित properties network database में संग्रहीत हैं।

- **Transport name:** NTCP
- **host:** IP (IPv4 या IPv6)।
  संक्षिप्त IPv6 पता ("::" के साथ) की अनुमति है।
  Host names पहले अनुमतित थे, लेकिन release 0.9.32 के बाद से deprecated हैं। proposal 141 देखें।
- **port:** 1024 - 65535

## NTCP प्रोटोकॉल विनिर्देश

### मानक संदेश प्रारूप

स्थापना के बाद, NTCP transport व्यक्तिगत I2NP messages भेजता है, एक सरल checksum के साथ। अनएन्क्रिप्टेड message को निम्नलिखित तरीके से encode किया जाता है:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
| sizeof(data)  |                                               |
+-------+-------+                                               +
|                            data                               |
~                                                               ~
|                                                               |
+                                       +-------+-------+-------+
|                                       |        padding
+-------+-------+-------+-------+-------+-------+-------+-------+
                                | Adler checksum of sz+data+pad |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
डेटा को फिर AES/256/CBC एन्क्रिप्शन से एन्क्रिप्ट किया जाता है। एन्क्रिप्शन के लिए सेशन की (session key) स्थापना के दौरान बातचीत की जाती है (Diffie-Hellman 2048 bit का उपयोग करके)। दो routers के बीच स्थापना EstablishState class में लागू की गई है और नीचे विस्तार से बताई गई है। AES/256/CBC एन्क्रिप्शन के लिए IV पिछले एन्क्रिप्टेड संदेश के अंतिम 16 bytes हैं।

कुल संदेश लंबाई (छह साइज और चेकसम बाइट्स सहित) को 16 के गुणज तक लाने के लिए 0-15 बाइट्स की पैडिंग आवश्यक होती है। वर्तमान में अधिकतम संदेश साइज 16 KB है। इसलिए वर्तमान में अधिकतम डेटा साइज 16 KB - 6, या 16378 बाइट्स है। न्यूनतम डेटा साइज 1 है।

### Time Sync Message Format

एक विशेष मामला metadata संदेश है जहां sizeof(data) 0 है। उस स्थिति में, unencrypted संदेश को इस प्रकार encode किया जाता है:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
|       0       |      timestamp in seconds     | uninterpreted
+-------+-------+-------+-------+-------+-------+-------+-------+
        uninterpreted           | Adler checksum of bytes 0-11  |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
कुल लंबाई: 16 बाइट्स। समय सिंक संदेश लगभग 15 मिनट के अंतराल पर भेजा जाता है। यह संदेश उसी तरह एन्क्रिप्ट किया जाता है जैसे मानक संदेश होते हैं।

### चेकसम

मानक और समय सिंक संदेश Adler-32 checksum का उपयोग करते हैं जैसा कि [ZLIB Specification](http://tools.ietf.org/html/rfc1950) में परिभाषित है।

### निष्क्रिय समयसीमा

Idle timeout और connection close प्रत्येक endpoint के विवेक पर निर्भर करता है और भिन्न हो सकता है। वर्तमान implementation में timeout को कम किया जाता है जब connections की संख्या configured maximum के करीब पहुंचती है, और timeout को बढ़ाया जाता है जब connection count कम होता है। अनुशंसित minimum timeout दो मिनट या अधिक है, और अनुशंसित maximum timeout दस मिनट या अधिक है।

### RouterInfo एक्सचेंज

स्थापना के बाद, और उसके बाद हर 30-60 मिनट में, दोनों router को आम तौर पर DatabaseStoreMessage का उपयोग करके RouterInfos का आदान-प्रदान करना चाहिए। हालांकि, Alice को यह जांचना चाहिए कि पहला queued message एक DatabaseStoreMessage है या नहीं ताकि duplicate message न भेजा जाए; यह अक्सर floodfill router से कनेक्ट करते समय होता है।

### स्थापना अनुक्रम

establish state में, DH keys और signatures का आदान-प्रदान करने के लिए एक 4-चरणीय संदेश अनुक्रम होता है। पहले दो संदेशों में 2048-bit Diffie Hellman exchange होता है। फिर, कनेक्शन की पुष्टि के लिए महत्वपूर्ण डेटा के signatures का आदान-प्रदान किया जाता है।

```
Alice                   contacts                      Bob
=========================================================
 X+(H(X) xor Bob.identHash)----------------------------->
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)
```
```
  Legend:
    X, Y: 256 byte DH public keys
    H(): 32 byte SHA256 Hash
    E(data, session key, IV): AES256 Encrypt
    S(): Signature
    tsA, tsB: timestamps (4 bytes, seconds since epoch)
    sk: 32 byte Session key
    sz: 2 byte size of Alice identity to follow
```
#### DH Key Exchange {#DH}

प्रारंभिक 2048-bit DH key exchange वही साझा prime (p) और generator (g) का उपयोग करता है जो I2P के [ElGamal encryption](/docs/specs/cryptography#elgamal) के लिए उपयोग किया जाता है।

DH key exchange में कई चरण होते हैं, जो नीचे दिखाए गए हैं। इन चरणों और I2P routers के बीच भेजे गए messages के बीच mapping को bold में चिह्नित किया गया है।

1. Alice एक गुप्त पूर्णांक x उत्पन्न करती है। फिर वह `X = g^x mod p` की गणना करती है।
2. Alice, X को Bob को भेजती है **(संदेश 1)**।
3. Bob एक गुप्त पूर्णांक y उत्पन्न करता है। फिर वह `Y = g^y mod p` की गणना करता है।
4. Bob, Y को Alice को भेजता है। **(संदेश 2)**
5. Alice अब `sessionKey = Y^x mod p` की गणना कर सकती है।
6. Bob अब `sessionKey = X^y mod p` की गणना कर सकता है।
7. अब Alice और Bob दोनों के पास एक साझा key `sessionKey = g^(x*y) mod p` है।

sessionKey का उपयोग फिर **Message 3** और **Message 4** में identities के आदान-प्रदान के लिए किया जाता है। DH exchange के लिए exponent (x और y) की लंबाई [cryptography page](/docs/specs/cryptography#exponent) पर दस्तावेजीकृत है।

#### सेशन की विवरण

32-बाइट सत्र कुंजी निम्नलिखित प्रकार से बनाई जाती है:

1. एक्सचेंज किए गए DH key को लें, जो एक positive minimal-length BigInteger byte array (two's complement big-endian) के रूप में प्रस्तुत है
2. यदि सबसे महत्वपूर्ण bit 1 है (यानी array[0] & 0x80 != 0), तो एक 0x00 byte को प्रीपेंड करें, जैसा कि Java के BigInteger.toByteArray() representation में होता है
3. यदि वह byte array 32 bytes से अधिक या बराबर है, तो पहले (सबसे महत्वपूर्ण) 32 bytes का उपयोग करें
4. यदि वह byte array 32 bytes से कम है, तो 32 bytes तक विस्तार करने के लिए 0x00 bytes को append करें। *(अत्यंत असंभावित)*

#### संदेश 1 (सत्र अनुरोध)

यह DH request है। Alice के पास पहले से ही Bob की [Router Identity](/docs/specs/common-structures#struct_RouterIdentity), IP address, और port है, जो उसके [Router Info](/docs/specs/common-structures#struct_RouterInfo) में शामिल है, जो [network database](/docs/overview/network-database) में प्रकाशित किया गया था। Alice, Bob को भेजती है:

```
 X+(H(X) xor Bob.identHash)----------------------------->

    Size: 288 bytes
```
सामग्री:

```
 +----+----+----+----+----+----+----+----+
 |         X, as calculated from DH      |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXxorHI                  |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  X :: 256 byte X from Diffie Hellman

  HXxorHI :: SHA256 Hash(X) xored with SHA256 Hash(Bob's RouterIdentity)
             (32 bytes)
```
**नोट्स:**

- Bob अपने स्वयं के router hash का उपयोग करके HXxorHI को सत्यापित करता है। यदि यह सत्यापित नहीं होता है, तो Alice ने गलत router से संपर्क किया है, और Bob कनेक्शन को drop कर देता है।

#### संदेश 2 (सत्र बनाया गया)

यह DH reply है। Bob, Alice को भेजता है:

```
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])

    Size: 304 bytes
```
अनएन्क्रिप्टेड सामग्री:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXY                      |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |        tsB        |     padding       |
 +----+----+----+----+                   +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y :: 256 byte Y from Diffie Hellman

  HXY :: SHA256 Hash(X concatenated with Y)
         (32 bytes)

  tsB :: 4 byte timestamp (seconds since the epoch)

  padding :: 12 bytes random data
```
एन्क्रिप्टेड सामग्री:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y: 256 byte Y from Diffie Hellman

  encrypted data: 48 bytes AES encrypted using the DH session key and
                  the last 16 bytes of Y as the IV
```
**नोट्स:**

- Alice कनेक्शन को drop कर सकती है यदि Bob के साथ clock skew बहुत अधिक है जैसा कि tsB का उपयोग करके गणना की गई है।

#### संदेश 3 (सत्र पुष्टि A)

इसमें Alice के router identity और महत्वपूर्ण डेटा का signature शामिल है। Alice, Bob को भेजती है:

```
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->

    Size: 448 bytes (typ. for 387 byte identity and DSA signature), see notes below
```
अनएन्क्रिप्टेड सामग्री:

```
 +----+----+----+----+----+----+----+----+
 |   sz    | Alice's Router Identity     |
 +----+----+                             +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +                        +----+----+----+
 |                        |     tsA
 +----+----+----+----+----+----+----+----+
      |             padding              |
 +----+                                  +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  sz :: 2 byte size of Alice's router identity to follow (387+)

  ident :: Alice's 387+ byte RouterIdentity

  tsA :: 4 byte timestamp (seconds since the epoch)

  padding :: 0-15 bytes random data

  signature :: the Signature of the following concatenated data:
               X, Y, Bob's RouterIdentity, tsA, tsB.
               Alice signs it with the SigningPrivateKey associated with
               the SigningPublicKey in her RouterIdentity
```
एन्क्रिप्टेड सामग्री:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: 448 bytes AES encrypted using the DH session key and
                  the last 16 bytes of HXxorHI (i.e., the last 16 bytes
                  of message #1) as the IV
                  448 is the typical length, but it could be longer, see below.
```
**नोट्स:**

- Bob signature को verify करता है, और असफल होने पर, connection को drop कर देता है।
- Bob connection को drop कर सकता है यदि Alice के साथ clock skew बहुत अधिक है जैसा कि tsA का उपयोग करके गणना की गई है।
- Alice इस message के encrypted contents के अंतिम 16 bytes को अगले message के लिए IV के रूप में उपयोग करेगा।
- Release 0.9.15 तक, router identity हमेशा 387 bytes की थी, signature हमेशा 40 byte DSA signature थी, और padding हमेशा 15 bytes थी। Release 0.9.16 से, router identity 387 bytes से अधिक लंबी हो सकती है, और signature type और length Alice की [Router Identity](/docs/specs/common-structures#struct_RouterIdentity) में [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) के type से implied होते हैं। Padding पूरी unencrypted contents के लिए 16 bytes के multiple के लिए आवश्यकतानुसार होती है।
- Message की कुल length Router Identity को पढ़ने के लिए इसे आंशिक रूप से decrypt किए बिना निर्धारित नहीं की जा सकती। चूंकि Router Identity की न्यूनतम length 387 bytes है, और न्यूनतम Signature length 40 है (DSA के लिए), न्यूनतम कुल message size 2 + 387 + 4 + (signature length) + (16 bytes तक padding) है, या DSA के लिए 2 + 387 + 4 + 40 + 15 = 448। Receiver वास्तविक Router Identity length निर्धारित करने के लिए decrypt करने से पहले उस न्यूनतम मात्रा को पढ़ सकता है। Router Identity में छोटे Certificates के लिए, यह संभवतः पूरा message होगा, और message में कोई अतिरिक्त bytes नहीं होंगे जिनके लिए अतिरिक्त decryption operation की आवश्यकता हो।

#### संदेश 4 (सत्र पुष्टि B)

यह महत्वपूर्ण डेटा का हस्ताक्षर है। Bob, Alice को भेजता है:

```
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)

    Size: 48 bytes (typ. for DSA signature), see notes below
```
अनएन्क्रिप्टेड सामग्री:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |               padding                 |
 +----+----+----+----+----+----+----+----+

  signature :: the Signature of the following concatenated data:
               X, Y, Alice's RouterIdentity, tsA, tsB.
               Bob signs it with the SigningPrivateKey associated with
               the SigningPublicKey in his RouterIdentity

  padding :: 0-15 bytes random data
```
एन्क्रिप्टेड सामग्री:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: Data AES encrypted using the DH session key and
                  the last 16 bytes of the encrypted contents of message #2 as the IV
                  48 bytes for a DSA signature, may vary for other signature types
```
**नोट्स:**

- Alice signature को verify करता है, और failure पर, connection को drop कर देता है।
- Bob इस message के encrypted contents के अंतिम 16 bytes को अगले message के लिए IV के रूप में उपयोग करेगा।
- Release 0.9.15 तक, signature हमेशा 40 byte का DSA signature था और padding हमेशा 8 bytes था। Release 0.9.16 से, signature type और length Bob के [Router Identity](/docs/specs/common-structures#struct_RouterIdentity) में [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) के type से implied होते हैं। Padding पूरे unencrypted contents के लिए 16 bytes के multiple तक आवश्यक होता है।

#### स्थापना के बाद

कनेक्शन स्थापित हो जाता है, और मानक या समय सिंक संदेश आदान-प्रदान किए जा सकते हैं। सभी बाद के संदेश बातचीत की गई DH session key का उपयोग करके AES एन्क्रिप्टेड होते हैं। Alice संदेश #3 की एन्क्रिप्टेड सामग्री के अंतिम 16 bytes को अगले IV के रूप में उपयोग करेगी। Bob संदेश #4 की एन्क्रिप्टेड सामग्री के अंतिम 16 bytes को अगले IV के रूप में उपयोग करेगा।

### कनेक्शन संदेश जांचें

वैकल्पिक रूप से, जब Bob को एक कनेक्शन प्राप्त होता है, तो यह एक check connection हो सकता है (शायद Bob द्वारा किसी से अपने listener को verify करने के लिए कहने से प्रेरित)। Check Connection वर्तमान में उपयोग में नहीं है। हालांकि, रिकॉर्ड के लिए, check connections को निम्नलिखित तरीके से formatted किया जाता है। एक check info connection को 256 bytes प्राप्त होंगे जिसमें शामिल है:

- 32 bytes की अव्याख्यायित, अनदेखी की गई डेटा
- 1 byte आकार
- उतने bytes जो स्थानीय router का IP address बनाते हैं (जैसा कि remote side द्वारा पहुंचा गया)
- 2 byte port number जिस पर स्थानीय router तक पहुंचा गया था
- 4 byte i2p network समय जैसा कि remote side को पता है (epoch के बाद से सेकंड)
- अव्याख्यायित padding डेटा, byte 223 तक
- स्थानीय router की identity hash और byte 32 से byte 223 तक के SHA256 का xor

रिलीज़ 0.9.12 के बाद से चेक कनेक्शन पूरी तरह से निष्क्रिय कर दिया गया है।

## चर्चा

अब [NTCP चर्चा पृष्ठ](/docs/discussions/ntcp) पर।

## भविष्य का कार्य {#future}

- अधिकतम संदेश आकार को लगभग 32 KB तक बढ़ाया जाना चाहिए।

- निश्चित packet आकारों का एक सेट बाहरी विरोधियों से डेटा विखंडन को और छुपाने के लिए उपयुक्त हो सकता है, लेकिन tunnel, garlic, और end to end padding तब तक अधिकांश आवश्यकताओं के लिए पर्याप्त होना चाहिए।
  हालांकि, वर्तमान में सीमित संख्या में संदेश आकार बनाने के लिए अगली 16-byte सीमा से आगे padding का कोई प्रावधान नहीं है।

- NTCP के लिए मेमोरी उपयोग (कर्नेल के सहित) की तुलना SSU के लिए मेमोरी उपयोग से की जानी चाहिए।

- क्या establishment messages को किसी तरह से randomly padded किया जा सकता है, ताकि initial packet sizes के आधार पर I2P traffic की पहचान को रोका जा सके?
