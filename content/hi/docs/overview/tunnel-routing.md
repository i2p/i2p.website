---
title: "टनल रूटिंग"
description: "I2P टनल शब्दावली, निर्माण और जीवनचक्र का अवलोकन"
slug: "tunnel-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## अवलोकन

I2P अस्थायी, एकदिशात्मक tunnels बनाता है — routers का क्रमबद्ध अनुक्रम जो एन्क्रिप्टेड ट्रैफ़िक को अग्रेषित करते हैं। Tunnels को **inbound** (संदेश निर्माता की ओर प्रवाहित होते हैं) या **outbound** (संदेश निर्माता से दूर प्रवाहित होते हैं) के रूप में वर्गीकृत किया जाता है।

एक सामान्य आदान-प्रदान में Alice का संदेश उसकी किसी एक outbound tunnel के माध्यम से बाहर भेजा जाता है, outbound endpoint को निर्देश दिया जाता है कि वह इसे Bob की किसी एक inbound tunnel के gateway को अग्रेषित करे, और फिर Bob इसे अपने inbound endpoint पर प्राप्त करता है।

![एलिस अपनी आउटबाउंड tunnel के माध्यम से बॉब की इनबाउंड tunnel से जुड़ रही है](/images/tunnelSending.png)

- **A**: Outbound Gateway (Alice)
- **B**: Outbound Participant
- **C**: Outbound Endpoint
- **D**: Inbound Gateway
- **E**: Inbound Participant
- **F**: Inbound Endpoint (Bob)

टनल का निश्चित जीवनकाल 10 मिनट होता है और ये 1024 बाइट्स के निश्चित आकार के संदेश वहन करती हैं (tunnel header सहित 1028 बाइट्स), ताकि संदेश के आकार या समय पैटर्न के आधार पर ट्रैफिक विश्लेषण को रोका जा सके।

## टनल शब्दावली

- **Tunnel gateway:** tunnel में पहला router। Inbound tunnels के लिए, इस router की पहचान प्रकाशित [LeaseSet](/docs/specs/common-structures/) में दिखाई देती है। Outbound tunnels के लिए, gateway मूल router है (ऊपर A और D)।
- **Tunnel endpoint:** tunnel में अंतिम router (ऊपर C और F)।
- **Tunnel participant:** tunnel में मध्यवर्ती router (ऊपर B और E)। Participants अपनी स्थिति या tunnel की दिशा निर्धारित नहीं कर सकते।
- **n-hop tunnel:** inter-router hops की संख्या।
  - **0-hop:** Gateway और endpoint एक ही router हैं – न्यूनतम गुमनामी।
  - **1-hop:** Gateway सीधे endpoint से जुड़ता है – कम विलंबता, कम गुमनामी।
  - **2-hop:** Exploratory tunnels के लिए डिफ़ॉल्ट; संतुलित सुरक्षा/प्रदर्शन।
  - **3-hop:** मजबूत गुमनामी की आवश्यकता वाले अनुप्रयोगों के लिए अनुशंसित।
- **Tunnel ID:** 4-byte integer जो प्रत्येक router और प्रत्येक hop के लिए अद्वितीय है, निर्माता द्वारा यादृच्छिक रूप से चुना गया। प्रत्येक hop विभिन्न IDs पर प्राप्त और forward करता है।

## टनल निर्माण जानकारी

gateway, participant, और endpoint भूमिकाओं को भरने वाले Routers, Tunnel Build Message के भीतर विभिन्न रिकॉर्ड प्राप्त करते हैं। आधुनिक I2P दो तरीकों का समर्थन करता है:

- **ElGamal** (लीगेसी, 528-बाइट रिकॉर्ड)
- **ECIES-X25519** (वर्तमान, 218-बाइट रिकॉर्ड Short Tunnel Build Message – STBM के माध्यम से)

### Information Distributed to Participants

**Gateway प्राप्त करता है:** - Tunnel layer key (AES-256 या ChaCha20 key, tunnel प्रकार के आधार पर) - Tunnel IV key (initialization vectors को encrypt करने के लिए) - Reply key और reply IV (build reply encryption के लिए) - Tunnel ID (केवल inbound gateways) - Next hop identity hash और tunnel ID (यदि non-terminal हो)

**मध्यवर्ती प्रतिभागी प्राप्त करते हैं:** - अपने hop के लिए Tunnel layer key और IV key - Tunnel ID और अगले hop की जानकारी - build response एन्क्रिप्शन के लिए Reply key और IV

**Endpoints प्राप्त करते हैं:** - Tunnel layer और IV keys - Reply router और tunnel ID (केवल outbound endpoints) - Reply key और IV (केवल outbound endpoints)

पूरी जानकारी के लिए देखें [Tunnel Creation Specification](/docs/specs/implementation/) और [ECIES Tunnel Creation Specification](/docs/specs/implementation/)।

## Tunnel Pooling

राउटर अतिरेक (redundancy) और लोड वितरण के लिए टनल को **tunnel pools** में समूहित करते हैं। प्रत्येक पूल कई समानांतर टनल बनाए रखता है, जो एक के विफल होने पर failover की अनुमति देता है। आंतरिक रूप से उपयोग किए जाने वाले पूल **exploratory tunnels** हैं, जबकि एप्लिकेशन-विशिष्ट पूल **client tunnels** हैं।

प्रत्येक destination अलग-अलग inbound और outbound pools को बनाए रखता है जो I2CP विकल्पों द्वारा कॉन्फ़िगर किए जाते हैं (tunnel संख्या, backup संख्या, लंबाई, और QoS पैरामीटर)। Routers tunnel स्वास्थ्य की निगरानी करते हैं, आवधिक परीक्षण चलाते हैं, और pool का आकार बनाए रखने के लिए विफल tunnels को स्वचालित रूप से पुनर्निर्माण करते हैं।

## टनल पूलिंग

**0-hop Tunnels**: केवल संभावित इनकार (plausible deniability) प्रदान करती हैं। ट्रैफ़िक हमेशा एक ही router से उत्पन्न होता है और समाप्त होता है — किसी भी अनाम उपयोग के लिए हतोत्साहित।

**1-hop Tunnels**: निष्क्रिय पर्यवेक्षकों के विरुद्ध बुनियादी गुमनामी प्रदान करते हैं लेकिन यदि कोई विरोधी उस एकल hop को नियंत्रित करता है तो असुरक्षित हैं।

**2-hop Tunnels** : दो दूरस्थ राउटर शामिल करती हैं और हमले की लागत को काफी बढ़ाती हैं। खोजपूर्ण पूल के लिए डिफ़ॉल्ट।

**3-hop Tunnels**: मजबूत गुमनामी सुरक्षा की आवश्यकता वाले अनुप्रयोगों के लिए अनुशंसित। अतिरिक्त hops बिना किसी सार्थक सुरक्षा लाभ के विलंबता बढ़ाते हैं।

**डिफ़ॉल्ट** : Router **2-hop** exploratory tunnel और एप्लिकेशन-विशिष्ट **2 या 3 hop** client tunnel का उपयोग करते हैं, जो प्रदर्शन और गुमनामी को संतुलित करते हैं।

## टनल की लंबाई

राउटर समय-समय पर एक आउटबाउंड टनल के माध्यम से एक इनबाउंड टनल में `DeliveryStatusMessage` भेजकर टनल का परीक्षण करते हैं। यदि परीक्षण विफल होता है, तो दोनों टनल को नकारात्मक प्रोफ़ाइल भार मिलता है। लगातार विफलताएं एक टनल को अनुपयोगी चिह्नित करती हैं; फिर राउटर एक प्रतिस्थापन का पुनर्निर्माण करता है और एक नया LeaseSet प्रकाशित करता है। परिणाम पीयर क्षमता मेट्रिक्स में शामिल होते हैं जो [peer selection system](/docs/overview/tunnel-routing/) द्वारा उपयोग किए जाते हैं।

## टनल परीक्षण

Router एक गैर-इंटरैक्टिव **telescoping** विधि का उपयोग करके tunnel निर्माण करते हैं: एक एकल Tunnel Build Message hop-by-hop प्रसारित होता है। प्रत्येक hop अपने रिकॉर्ड को डिक्रिप्ट करता है, अपना उत्तर जोड़ता है, और संदेश को आगे भेजता है। अंतिम hop एक अलग पथ के माध्यम से समग्र बिल्ड उत्तर लौटाता है, जो सहसंबंध को रोकता है। आधुनिक कार्यान्वयन ECIES के लिए **Short Tunnel Build Messages (STBM)** और पुराने पथों के लिए **Variable Tunnel Build Messages (VTBM)** का उपयोग करते हैं। प्रत्येक रिकॉर्ड को ElGamal या ECIES-X25519 का उपयोग करके per-hop एन्क्रिप्ट किया जाता है।

## टनल निर्माण

टनल ट्रैफ़िक बहु-स्तरीय एन्क्रिप्शन का उपयोग करता है। जब संदेश tunnel से गुजरते हैं तो प्रत्येक hop एन्क्रिप्शन की एक परत जोड़ता या हटाता है।

- **ElGamal tunnels:** PKCS#5 padding के साथ payloads के लिए AES-256/CBC।
- **ECIES tunnels:** authenticated encryption के लिए ChaCha20 या ChaCha20-Poly1305।

प्रत्येक hop में दो keys होती हैं: एक **layer key** और एक **IV key**। Routers IV को decrypt करते हैं, इसका उपयोग payload को process करने के लिए करते हैं, फिर forward करने से पहले IV को फिर से encrypt करते हैं। यह double IV scheme message tagging को रोकती है।

आउटबाउंड गेटवे सभी परतों को पहले से डिक्रिप्ट करते हैं ताकि सभी प्रतिभागियों द्वारा एन्क्रिप्शन जोड़े जाने के बाद एंडपॉइंट को प्लेनटेक्स्ट प्राप्त हो। इनबाउंड tunnel विपरीत दिशा में एन्क्रिप्ट करते हैं। प्रतिभागी tunnel की दिशा या लंबाई निर्धारित नहीं कर सकते।

## टनल एन्क्रिप्शन

- नेटवर्क लोड संतुलन के लिए डायनामिक tunnel जीवनकाल और अनुकूली पूल आकार
- वैकल्पिक tunnel परीक्षण रणनीतियाँ और व्यक्तिगत हॉप निदान
- वैकल्पिक proof-of-work या bandwidth प्रमाणपत्र सत्यापन (API 0.9.65+ में लागू)
- endpoint मिश्रण के लिए ट्रैफ़िक शेपिंग और chaff सम्मिलन अनुसंधान
- ElGamal की निरंतर सेवानिवृत्ति और ECIES-X25519 में माइग्रेशन

## चल रहा विकास

- [Tunnel Implementation Specification](/docs/specs/implementation/)
- [Tunnel Creation Specification (ElGamal)](/docs/specs/implementation/)
- [Tunnel Creation Specification (ECIES-X25519)](/docs/specs/implementation/)
- [Tunnel Message Specification](/docs/specs/implementation/)
- [Garlic Routing](/docs/overview/garlic-routing/)
- [I2P Network Database](/docs/specs/common-structures/)
- [Peer Profiling and Selection](/docs/overview/tunnel-routing/)
- [I2P Threat Model](/docs/overview/threat-model/)
- [ElGamal/AES + SessionTag Encryption](/docs/legacy/elgamal-aes/)
- [I2CP Options](/docs/specs/i2cp/)
