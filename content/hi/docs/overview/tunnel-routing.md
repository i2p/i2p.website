---
title: "Tunnel राउटिंग"
description: "I2P tunnel शब्दावली, निर्माण और संचालन का अवलोकन"
slug: "tunnel-routing"
lastUpdated: "2026-03"
accurateFor: "0.9.68"
---

## सिंहावलोकन

इस पृष्ठ में I2P tunnel शब्दावली और संचालन का अवलोकन है, जिसमें अधिक तकनीकी पृष्ठों, विवरणों और विनिर्देशों के लिंक शामिल हैं।

जैसा कि [परिचय](/docs/overview/intro/) में संक्षेप में बताया गया है, I2P वर्चुअल "tunnels" बनाता है - routers के एक क्रम के माध्यम से अस्थायी और एकदिशीय पथ। इन tunnels को या तो inbound tunnels (जहां इसे दी गई हर चीज tunnel के निर्माता की ओर जाती है) या outbound tunnels (जहां tunnel निर्माता संदेशों को अपने से दूर धकेलता है) के रूप में वर्गीकृत किया जाता है। जब Alice, Bob को एक संदेश भेजना चाहती है, तो वह (आमतौर पर) इसे अपने मौजूदा outbound tunnels में से किसी एक के माध्यम से भेजेगी और उस tunnel के endpoint को निर्देश देगी कि वह इसे Bob के वर्तमान inbound tunnels में से किसी एक के gateway router को forward करे, जो बदले में इसे Bob को पास करता है।

![Alice अपनी outbound tunnel के माध्यम से Bob की inbound tunnel के द्वारा उससे जुड़ रही है](/images/tunnelSending.svg)

```
A: Outbound Gateway (Alice)
B: Outbound Participant
C: Outbound Endpoint
D: Inbound Gateway
E: Inbound Participant
F: Inbound Endpoint (Bob)
```
---

## Tunnel शब्दावली

- **Tunnel gateway** - tunnel में पहला router। Inbound tunnels के लिए, यह वह है जिसका उल्लेख [network database](/docs/overview/network-database/) में प्रकाशित LeaseSet में किया गया है। Outbound tunnels के लिए, gateway मूल router है। (जैसे ऊपर A और D दोनों)

- **Tunnel endpoint** - tunnel का अंतिम router। (जैसे ऊपर C और F दोनों)

- **Tunnel participant** - gateway या endpoint को छोड़कर tunnel में सभी router (जैसे ऊपर B और E दोनों)

- **n-Hop tunnel** - एक tunnel जिसमें inter-router jumps की एक विशिष्ट संख्या होती है, जैसे:
  - **0-hop tunnel** - एक tunnel जहाँ gateway भी endpoint है
  - **1-hop tunnel** - एक tunnel जहाँ gateway सीधे endpoint से बात करता है
  - **2-(या अधिक)-hop tunnel** - एक tunnel जहाँ कम से कम एक intermediate tunnel participant होता है। (ऊपर का diagram दो 2-hop tunnels शामिल करता है - एक Alice से outbound, एक Bob को inbound)

- **Tunnel ID** - एक [4 byte integer](/docs/specs/common-structures/#type_TunnelId) जो tunnel के हर hop के लिए अलग होता है, और router पर सभी tunnels में unique होता है। tunnel creator द्वारा randomly चुना जाता है।

---

## Tunnel निर्माण जानकारी

तीन भूमिकाएं (gateway, participant, endpoint) निभाने वाले routers को अपने कार्यों को पूरा करने के लिए प्रारंभिक [Tunnel Build Message](/docs/specs/tunnel-creation/) में डेटा के अलग-अलग हिस्से दिए जाते हैं:

**tunnel gateway को मिलता है:**

- **tunnel encryption key** - अगली hop तक संदेशों और निर्देशों को encrypt करने के लिए एक [AES private key](/docs/specs/common-structures/#type_SessionKey)
- **tunnel IV key** - अगली hop तक IV को double-encrypt करने के लिए एक [AES private key](/docs/specs/common-structures/#type_SessionKey)
- **reply key** - tunnel build request के reply को encrypt करने के लिए एक [AES public key](/docs/specs/common-structures/#type_SessionKey)
- **reply IV** - tunnel build request के reply को encrypt करने के लिए IV
- **tunnel id** - 4 byte integer (केवल inbound gateways के लिए)
- **next hop** - path में अगला router कौन सा है (जब तक यह 0-hop tunnel नहीं है, और gateway भी endpoint है)
- **next tunnel id** - अगली hop पर tunnel ID

**सभी मध्यवर्ती tunnel प्रतिभागियों को मिलता है:**

- **tunnel encryption key** - अगले hop को संदेश और निर्देश एन्क्रिप्ट करने के लिए एक [AES private key](/docs/specs/common-structures/#type_SessionKey)
- **tunnel IV key** - अगले hop को IV को double-encrypt करने के लिए एक [AES private key](/docs/specs/common-structures/#type_SessionKey)
- **reply key** - tunnel build request के reply को एन्क्रिप्ट करने के लिए एक [AES public key](/docs/specs/common-structures/#type_SessionKey)
- **reply IV** - tunnel build request के reply को एन्क्रिप्ट करने के लिए IV
- **tunnel id** - 4 byte integer
- **next hop** - path में अगला router कौन सा है
- **next tunnel id** - अगले hop पर tunnel ID

**tunnel endpoint को मिलता है:**

- **tunnel encryption key** - endpoint (स्वयं) को संदेश और निर्देश एन्क्रिप्ट करने के लिए एक [AES private key](/docs/specs/common-structures/#type_SessionKey)
- **tunnel IV key** - endpoint (स्वयं) को IV को डबल-एन्क्रिप्ट करने के लिए एक [AES private key](/docs/specs/common-structures/#type_SessionKey)
- **reply key** - tunnel build request के उत्तर को एन्क्रिप्ट करने के लिए एक [AES public key](/docs/specs/common-structures/#type_SessionKey) (केवल outbound endpoints)
- **reply IV** - tunnel build request के उत्तर को एन्क्रिप्ट करने के लिए IV (केवल outbound endpoints)
- **tunnel id** - 4 बाइट integer (केवल outbound endpoints)
- **reply router** - उत्तर भेजने के लिए tunnel का inbound gateway (केवल outbound endpoints)
- **reply tunnel id** - reply router का tunnel ID (केवल outbound endpoints)

विवरण [tunnel creation specification](/docs/specs/tunnel-creation/) में हैं।

---

## Tunnel पूलिंग

किसी विशेष उद्देश्य के लिए कई tunnels को एक "tunnel pool" में समूहीकृत किया जा सकता है, जैसा कि [tunnel specification](/docs/specs/tunnel-implementation/#tunnel.pooling) में वर्णित है। यह redundancy और अतिरिक्त bandwidth प्रदान करता है। router द्वारा स्वयं उपयोग किए जाने वाले pools को "exploratory tunnels" कहा जाता है। applications द्वारा उपयोग किए जाने वाले pools को "client tunnels" कहा जाता है।

---

## Tunnel की लंबाई

जैसा कि ऊपर उल्लेख किया गया है, प्रत्येक क्लाइंट अपने router से अनुरोध करता है कि वे कम से कम एक निश्चित संख्या में hops शामिल करने वाले tunnels प्रदान करें। किसी के outbound और inbound tunnels में कितने routers रखे जाएं, इस निर्णय का I2P द्वारा प्रदान की जाने वाली latency, throughput, reliability और anonymity पर महत्वपूर्ण प्रभाव पड़ता है - जितने अधिक peers से संदेश गुजरना पड़ता है, उतनी ही अधिक देर लगती है वहां पहुंचने में और उतनी ही अधिक संभावना होती है कि उन routers में से कोई एक समय से पहले fail हो जाए। tunnel में जितने कम routers होते हैं, किसी adversary के लिए traffic analysis attacks करना और किसी की anonymity को भेदना उतना ही आसान हो जाता है। Tunnel lengths को clients [I2CP options](/docs/specs/i2cp/#options) के माध्यम से निर्दिष्ट करते हैं। एक tunnel में hops की अधिकतम संख्या 7 है।

### 0-hop tunnels

tunnel में कोई remote router न होने पर, उपयोगकर्ता के पास बहुत बुनियादी plausible deniability है (क्योंकि कोई भी निश्चित रूप से नहीं जानता कि जिस peer ने उन्हें संदेश भेजा था वह केवल tunnel के हिस्से के रूप में इसे आगे forward कर रहा था)। हालांकि, statistical analysis attack करना काफी आसान होगा और यह देखना कि किसी विशिष्ट गंतव्य को लक्षित संदेश हमेशा एक ही gateway के माध्यम से भेजे जाते हैं। outbound 0-hop tunnels के विरुद्ध statistical analysis अधिक जटिल हैं, लेकिन समान जानकारी दिखा सकते हैं (हालांकि इन्हें mount करना थोड़ा कठिन होगा)।

### 1-hop tunnel

tunnel में केवल एक remote router के साथ, उपयोगकर्ता के पास plausible deniability और बुनियादी anonymity दोनों होती है, जब तक कि वे किसी internal adversary का सामना नहीं कर रहे हैं ([threat model](/docs/overview/threat-model/) में वर्णित के अनुसार)। हालांकि, यदि adversary पर्याप्त संख्या में router चलाता है जैसे कि tunnel में single remote router अक्सर उन compromised routers में से एक हो, तो वे उपरोक्त statistical traffic analysis attack को mount कर सकते हैं।

### 2-hop tunnels

tunnel में दो या अधिक दूरस्थ router के साथ, traffic analysis attack को अंजाम देने की लागत बढ़ जाती है, क्योंकि इसे माउंट करने के लिए कई दूरस्थ router से समझौता करना होगा।

### 3-hop (या अधिक) tunnel

कुछ हमलों के प्रति संवेदनशीलता को कम करने के लिए, उच्चतम स्तर की सुरक्षा के लिए 3 या अधिक हॉप्स की अनुशंसा की जाती है। [हाल के अध्ययनों](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/) में यह भी निष्कर्ष निकाला गया है कि 3 से अधिक हॉप्स अतिरिक्त सुरक्षा प्रदान नहीं करते हैं।

### Tunnel डिफ़ॉल्ट लंबाई

Router अपनी exploratory tunnels के लिए डिफ़ॉल्ट रूप से 2-hop tunnels का उपयोग करता है। Client tunnel डिफ़ॉल्ट एप्लिकेशन द्वारा [I2CP options](/docs/specs/i2cp/#options) का उपयोग करके सेट किए जाते हैं। अधिकांश एप्लिकेशन अपने डिफ़ॉल्ट के रूप में 2 या 3 hops का उपयोग करते हैं।

---

## Tunnel परीक्षण

सभी tunnels का उनके निर्माता द्वारा नियमित रूप से परीक्षण किया जाता है, एक DeliveryStatusMessage को outbound tunnel के माध्यम से भेजकर और दूसरे inbound tunnel के लिए निर्देशित करके (दोनों tunnels का एक साथ परीक्षण)। यदि कोई भी लगातार कई परीक्षणों में असफल हो जाता है, तो उसे अब कार्यशील नहीं माना जाता है। यदि यह किसी client के inbound tunnel के लिए उपयोग में था, तो एक नया leaseSet बनाया जाता है। Tunnel परीक्षण की असफलताएं [peer profile में capacity rating](/docs/overview/peer-selection/#capacity) में भी प्रतिबिंबित होती हैं।

---

Tunnel creation को [garlic routing](/docs/overview/garlic-routing/) द्वारा संभाला जाता है जो एक router को Tunnel Build Message भेजता है, उनसे अनुरोध करता है कि वे tunnel में भाग लें (उन्हें उपरोक्त सभी उपयुक्त जानकारी प्रदान करते हुए, एक certificate के साथ, जो अभी एक 'null' cert है, लेकिन आवश्यकता पड़ने पर hashcash या अन्य non-free certificates का समर्थन करेगा)। वह router संदेश को tunnel की अगली hop को आगे भेजता है। विवरण [tunnel creation specification](/docs/specs/tunnel-creation/) में है।

## Tunnel निर्माण

---

बहु-स्तरीय एन्क्रिप्शन को tunnel संदेशों की [garlic encryption](/docs/overview/garlic-routing/) द्वारा संभाला जाता है। विवरण [tunnel specification](/docs/specs/tunnel-implementation/) में हैं। प्रत्येक hop का IV एक अलग key के साथ एन्क्रिप्ट किया जाता है जैसा कि वहाँ समझाया गया है।

## Tunnel एन्क्रिप्शन

---

---

## भविष्य का काम

- अन्य tunnel परीक्षण तकनीकों का उपयोग किया जा सकता है, जैसे कि कई परीक्षणों को cloves में garlic wrapping करना, व्यक्तिगत tunnel प्रतिभागियों का अलग से परीक्षण करना, आदि।

- 3-hop exploratory tunnels डिफॉल्ट्स पर जाएं।

- भविष्य के किसी दूर के release में, pooling, mixing, और chaff generation सेटिंग्स को निर्दिष्ट करने वाले विकल्प लागू किए जा सकते हैं।

- भविष्य की किसी दूर की रिलीज़ में, tunnel के जीवनकाल के दौरान अनुमतित संदेशों की मात्रा और आकार पर सीमाएं लागू की जा सकती हैं (जैसे प्रति मिनट 300 से अधिक संदेश या 1MB नहीं)।

---

## यह भी देखें

- [Tunnel specification](/docs/specs/tunnel-implementation/)
- [Tunnel creation specification](/docs/specs/tunnel-creation/)
- [एकदिशीय tunnels](/docs/legacy/unidirectional/)
- [Tunnel message specification](/docs/specs/tunnel-message/)
- [Garlic routing](/docs/overview/garlic-routing/)
- [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/)
- [I2CP विकल्प](/docs/specs/i2cp/#options)
