---
title: "ElGamal/AES + SessionTag Encryption"
description: "ElGamal, AES, SHA-256, और one-time session tags को मिलाकर बनाई गई पुरानी end-to-end encryption"
slug: "elgamal-aes"
aliases:
  - "/hi/how_elgamalaes"
  - "/hi/how_elgamalaes/"
lastUpdated: "2020-04"
accurateFor: "0.9.46"
---

## अवलोकन

ElGamal/AES+SessionTags का उपयोग end-to-end encryption के लिए किया जाता है।

एक अविश्वसनीय, अव्यवस्थित, संदेश आधारित सिस्टम के रूप में, I2P garlic messages को डेटा गोपनीयता और अखंडता प्रदान करने के लिए असममित और सममित एन्क्रिप्शन एल्गोरिदम का एक सरल संयोजन उपयोग करता है। संपूर्ण रूप से, इस संयोजन को ElGamal/AES+SessionTags के रूप में संदर्भित किया जाता है, लेकिन यह 2048bit ElGamal, AES256, SHA256, और 32 byte nonces के उपयोग का वर्णन करने का एक अत्यधिक विस्तृत तरीका है।

जब पहली बार कोई router किसी दूसरे router को garlic message encrypt करना चाहता है, तो वे AES256 session key के लिए keying material को ElGamal के साथ encrypt करते हैं और उस encrypted ElGamal block के बाद AES256/CBC encrypted payload को जोड़ते हैं। encrypted payload के अतिरिक्त, AES encrypted section में payload length, unencrypted payload का SHA256 hash, और कई "session tags" - random 32 byte nonces शामिल होते हैं। अगली बार जब sender किसी दूसरे router को garlic message encrypt करना चाहता है, तो नई session key को ElGamal encrypt करने के बजाय वे बस पहले से delivered session tags में से एक को चुनते हैं और payload को पहले की तरह AES encrypt करते हैं, उस session tag के साथ उपयोग की गई session key का उपयोग करके, जिसके आगे session tag itself को prepend किया जाता है। जब कोई router garlic encrypted message प्राप्त करता है, तो वे पहले 32 bytes की जांच करते हैं कि यह किसी available session tag से match करता है या नहीं - यदि करता है, तो वे बस message को AES decrypt करते हैं, लेकिन यदि नहीं करता, तो वे पहले block को ElGamal decrypt करते हैं।

प्रत्येक session tag केवल एक बार उपयोग किया जा सकता है ताकि internal adversaries को अलग-अलग संदेशों को समान routers के बीच होने वाले संदेशों के रूप में अनावश्यक रूप से correlate करने से रोका जा सके। ElGamal/AES+SessionTag encrypted संदेश का भेजने वाला यह चुनता है कि कब और कितने tags देने हैं, प्राप्तकर्ता को संदेशों की एक श्रृंखला को कवर करने के लिए पर्याप्त tags के साथ पूर्व-संग्रहित करता है। Garlic messages एक छोटे अतिरिक्त संदेश को clove के रूप में bundling करके ("delivery status message") सफल tag delivery का पता लगा सकते हैं - जब garlic message इच्छित प्राप्तकर्ता तक पहुंचता है और सफलतापूर्वक decrypt हो जाता है, तो यह छोटा delivery status message उजागर होने वाले cloves में से एक होता है और इसमें प्राप्तकर्ता के लिए निर्देश होते हैं कि clove को वापस मूल भेजने वाले को भेजा जाए (निश्चित रूप से एक inbound tunnel के माध्यम से)। जब मूल भेजने वाला इस delivery status message को प्राप्त करता है, तो उन्हें पता चल जाता है कि garlic message में bundled session tags सफलतापूर्वक पहुंचा दिए गए थे।

Session tags के स्वयं का जीवनकाल छोटा होता है, जिसके बाद यदि उपयोग नहीं किया जाता तो उन्हें हटा दिया जाता है। इसके अतिरिक्त, प्रत्येक key के लिए संग्रहीत मात्रा सीमित होती है, जैसे कि keys की संख्या भी - यदि बहुत अधिक आते हैं, तो नए या पुराने messages छोड़े जा सकते हैं। भेजने वाला ट्रैक रखता है कि session tags का उपयोग करने वाले messages पहुंच रहे हैं या नहीं, और यदि पर्याप्त संचार नहीं है तो वह उन्हें छोड़ सकता है जिन्हें पहले से ठीक से वितरित माना जाता था, और पूर्ण महंगे ElGamal encryption पर वापस जा सकता है। Session तब तक मौजूद रहेगा जब तक उसके सभी tags समाप्त या expire नहीं हो जाते।

सत्र एकदिशीय होते हैं। टैग Alice से Bob को दिए जाते हैं, और फिर Alice उन टैग्स का उपयोग करती है, एक के बाद एक, Bob को भेजे जाने वाले बाद के संदेशों में।

Sessions Destinations के बीच, Routers के बीच, या एक Router और Destination के बीच स्थापित किए जा सकते हैं। प्रत्येक Router और Destination अपना स्वयं का Session Key Manager बनाए रखता है जो Session Keys और Session Tags का ट्रैक रखता है। अलग Session Key Managers विरोधियों द्वारा कई Destinations को एक दूसरे से या Router से जोड़ने से रोकता है।

## संदेश प्राप्ति

प्रत्येक प्राप्त संदेश में निम्नलिखित दो संभावित स्थितियों में से एक होती है:

1. यह एक मौजूदा session का हिस्सा है और इसमें एक Session Tag और एक AES encrypted block होता है
2. यह एक नए session के लिए है और इसमें ElGamal और AES दोनों encrypted blocks होते हैं

जब एक router को कोई संदेश प्राप्त होता है, तो वह पहले यह मान लेता है कि यह किसी मौजूदा सत्र से है और Session Tag को देखने का प्रयास करता है और AES का उपयोग करके निम्नलिखित डेटा को डिक्रिप्ट करता है। यदि वह असफल हो जाता है, तो वह मान लेता है कि यह एक नए सत्र के लिए है और ElGamal का उपयोग करके इसे डिक्रिप्ट करने का प्रयास करता है।

## नए सेशन संदेश विनिर्देश {#new}

एक नया Session ElGamal Message में दो भाग होते हैं, एक एन्क्रिप्टेड ElGamal ब्लॉक और एक एन्क्रिप्टेड AES ब्लॉक।

एन्क्रिप्टेड संदेश में निम्नलिखित शामिल है:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |       ElGamal Encrypted Block         |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         |                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         +
   +----+----+
```
### ElGamal Block

एन्क्रिप्टेड ElGamal Block हमेशा 514 बाइट लंबा होता है।

अनएन्क्रिप्टेड ElGamal डेटा 222 बाइट्स लंबा है, जिसमें निम्नलिखित शामिल है:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |           Session Key                 |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |              Pre-IV                   |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   +                                       +
   |                                       |
   +                                       +
   |       158 bytes random padding        |
   ~                                       ~
   |                                       |
   +                             +----+----+
   |                             |
   +----+----+----+----+----+----+
```
32-बाइट [Session Key](/docs/specs/common-structures#type_SessionKey) सत्र का पहचानकर्ता है। 32-बाइट Pre-IV का उपयोग AES ब्लॉक के लिए IV जनरेट करने में किया जाएगा जो इसके बाद आता है; IV, Pre-IV के SHA-256 Hash के पहले 16 बाइट्स होते हैं।

222 बाइट का payload [ElGamal का उपयोग करके](/docs/specs/cryptography#elgamal) एन्क्रिप्ट किया जाता है और एन्क्रिप्टेड ब्लॉक 514 बाइट लंबा होता है।

### AES Block {#aes}

AES ब्लॉक में unencrypted डेटा निम्नलिखित शामिल करता है:

```
   +----+----+----+----+----+----+----+----+
   |tag count|                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |          Session Tags                 |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +         +----+----+----+----+----+----+
   |         |    payload size   |         |
   +----+----+----+----+----+----+         +
   |                                       |
   +                                       +
   |          Payload Hash                 |
   +                                       +
   |                                       |
   +                             +----+----+
   |                             |flag|    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |          New Session Key (opt.)       |
   +                                       +
   |                                       |
   +                                  +----+
   |                                  |    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |           Payload                     |
   ~                                       ~
   |                                       |
   +                        +----//---+----+
   |                        |              |
   +----+----+----//---+----+              +
   |          Padding to 16 bytes          |
   +----+----+----+----+----+----+----+----+
```
#### परिभाषा

```
tag count:
    2-byte Integer, 0-200

Session Tags:
    That many 32-byte SessionTags

payload size:
    4-byte Integer

Payload Hash:
    The 32-byte SHA256 Hash of the payload

flag:
    A one-byte value. Normally == 0. If == 0x01, a Session Key follows

New Session Key:
    A 32-byte SessionKey,
    to replace the old key, and is only present if preceding flag is 0x01

Payload:
    the data

Padding:
    Random data to a multiple of 16 bytes for the total length.
    May contain more than the minimum required padding.
```
न्यूनतम लंबाई: 48 bytes

डेटा को फिर [AES Encrypted](/docs/specs/cryptography) किया जाता है, ElGamal सेक्शन से session key और IV (pre-IV से गणना किया गया) का उपयोग करके। encrypted AES Block की लंबाई परिवर्तनशील होती है लेकिन हमेशा 16 bytes का गुणज होती है।

#### नोट्स

- वास्तविक अधिकतम payload लंबाई, और अधिकतम ब्लॉक लंबाई, 64 KB से कम है; [I2NP Overview](/docs/protocol/i2np) देखें।
- New Session Key वर्तमान में अप्रयुक्त है और कभी उपस्थित नहीं है।

## मौजूदा सेशन संदेश विनिर्देश {#existing}

सफलतापूर्वक वितरित session tags को एक संक्षिप्त अवधि (वर्तमान में 15 मिनट) तक याद रखा जाता है जब तक कि वे उपयोग या त्याग नहीं हो जाते। एक tag का उपयोग इसे एक Existing Session Message में पैकेज करके किया जाता है जिसमें केवल एक AES encrypted block होता है, और इससे पहले कोई ElGamal block नहीं होता।

मौजूदा सत्र संदेश निम्नलिखित है:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |            Session Tag                |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
```
#### परिभाषा

```
Session Tag:
    A 32-byte SessionTag
    previously delivered in an AES block

AES Encrypted Block:
    As specified above.
```
session tag भी pre-IV के रूप में कार्य करता है। IV, sessionTag के SHA-256 Hash के पहले 16 bytes होते हैं।

मौजूदा सत्र से एक संदेश को decode करने के लिए, एक router Session Tag को खोजता है ताकि संबंधित Session Key मिल सके। यदि Session Tag मिल जाता है, तो AES block को संबंधित Session Key का उपयोग करके decrypt किया जाता है। यदि tag नहीं मिलता है, तो संदेश को एक [New Session Message](#new) माना जाता है।

## Session Tag कॉन्फ़िगरेशन विकल्प {#config}

रिलीज़ 0.9.2 के अनुसार, क्लाइंट वर्तमान session के लिए भेजे जाने वाले Session Tags की डिफ़ॉल्ट संख्या और low tag threshold को कॉन्फ़िगर कर सकता है। संक्षिप्त streaming connections या datagrams के लिए, इन विकल्पों का उपयोग bandwidth को काफी कम करने के लिए किया जा सकता है। विवरण के लिए [I2CP options specification](/docs/protocol/i2cp#options) देखें। session सेटिंग्स को प्रति-संदेश आधार पर भी override किया जा सकता है। विवरण के लिए [I2CP Send Message Expires specification](/docs/specs/i2cp#msg_SendMessageExpires) देखें।

## भविष्य का कार्य {#future}

**नोट:** ElGamal/AES+SessionTags को ECIES-X25519-AEAD-Ratchet (Proposal 144) से बदला जा रहा है। नीचे संदर्भित मुद्दे और विचारों को नए प्रोटोकॉल के डिज़ाइन में शामिल किया गया है। निम्नलिखित बिंदुओं को ElGamal/AES+SessionTags में संबोधित नहीं किया जाएगा।

Session Key Manager के algorithms को tune करने के लिए कई संभावित क्षेत्र हैं; कुछ streaming library के व्यवहार के साथ interact कर सकते हैं, या समग्र प्रदर्शन पर महत्वपूर्ण प्रभाव डाल सकते हैं।

- प्रदान किए गए tags की संख्या संदेश के आकार पर निर्भर हो सकती है, tunnel message layer पर अंततः 1KB तक padding को ध्यान में रखते हुए।

- Clients router को session lifetime का एक अनुमान भेज सकते हैं, जो आवश्यक tags की संख्या के लिए एक सलाह के रूप में काम करे।

- बहुत कम tags की डिलीवरी के कारण router को महंगे ElGamal encryption पर वापस जाना पड़ता है।

- Router Session Tags की डिलीवरी मान सकता है, या उनका उपयोग करने से पहले पुष्टि का इंतजार कर सकता है; प्रत्येक रणनीति के लिए ट्रेडऑफ हैं।

- बहुत छोटे संदेशों के लिए, session स्थापित करने के बजाय, ElGamal block में pre-IV और padding fields के लगभग पूरे 222 bytes का उपयोग पूरे संदेश के लिए किया जा सकता है।

- Padding रणनीति का मूल्यांकन करें; वर्तमान में हम न्यूनतम 128 bytes तक pad करते हैं।
  छोटे संदेशों को pad करने के बजाय कुछ tags जोड़ना बेहतर होगा।

- शायद चीजें अधिक कुशल हो सकती हैं यदि Session Tag सिस्टम द्विदिशीय होता,
  तो 'forward' पथ में वितरित tags को 'reverse' पथ में उपयोग किया जा सकता,
  इस प्रकार प्रारंभिक response में ElGamal से बचा जा सकता।
  router वर्तमान में कुछ ऐसी तरकीबें करता है जब वह
  खुद को tunnel test messages भेजता है।

- Session Tags से बदलकर
  [एक synchronized PRNG](/docs/overview/performance#future#prng) में।

- इनमें से कई विचारों के लिए एक नया I2NP message type की आवश्यकता हो सकती है, या
  [Delivery Instructions](/docs/specs/tunnel-message#struct_TunnelMessageDeliveryInstructions) में
  एक flag सेट करना होगा,
  या Session Key field के पहले कुछ bytes में एक magic number सेट करना होगा
  और random Session Key के magic number से मैच होने के छोटे जोखिम को स्वीकार करना होगा।
