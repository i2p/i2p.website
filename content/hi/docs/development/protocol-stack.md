---
title: "प्रोटोकॉल स्टैक"
description: "I2P प्रोटोकॉल स्टैक परतों का अवलोकन"
slug: "protocol-stack"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
aliases:
  - "/hi/docs/develop/protocol-stack"
  - "/hi/docs/develop/protocol-stack/"
  - "/hi/protocols"
  - "/hi/protocols/"
---

I2P stack एक स्तरित डिज़ाइन है जो गुमनाम संचार को सक्षम बनाता है। प्रत्येक स्तर अपने नीचे के स्तरों की क्षमताओं के ऊपर विशिष्ट सुविधाएं जोड़ता है। प्रत्येक घटक पर अतिरिक्त विवरण के लिए [Technical Documentation Index](/docs/develop/overview) देखें।

## इंटरनेट परत {#internet}

**IP** - Internet Protocol नियमित इंटरनेट पर hosts को address करने और best-effort delivery का उपयोग करते हुए इंटरनेट भर में packets को route करने की अनुमति देता है।

## Transport Layer {#transport}

- **TCP** - Transmission Control Protocol पैकेट्स की विश्वसनीय, क्रमबद्ध डिलीवरी की अनुमति देता है
- **UDP** - User Datagram Protocol पैकेट्स की अविश्वसनीय, बेक्रम डिलीवरी की अनुमति देता है

## I2P Transport Layer {#i2p-transport}

एन्क्रिप्टेड router-to-router कनेक्शन (अभी तक गुमनाम नहीं):

- **[NTCP2](/docs/specs/ntcp2)** - NIO-आधारित TCP transport
- **[SSU2](/docs/specs/ssu2)** - Secure Semi-reliable UDP transport

## I2P Tunnel Layer {#tunnels}

पूर्ण गुमनाम एन्क्रिप्टेड tunnel कनेक्शन प्रदान करता है:

- **[Tunnel messages](/docs/legacy/tunnel-message)** - एन्क्रिप्टेड I2NP संदेश और उनकी डिलीवरी के लिए एन्क्रिप्टेड निर्देश
- **[I2NP messages](/docs/specs/i2np)** - मल्टी-हॉप अज्ञात routing के लिए layered encryption वाले प्रोटोकॉल संदेश

## I2P Garlic Layer {#garlic}

एन्क्रिप्टेड और गुमनाम end-to-end I2P संदेश वितरण प्रदान करता है:

- **[Garlic messages](/docs/overview/garlic-routing)** - गुमनाम डिलीवरी के लिए wrapped I2NP संदेश

## I2P Client Layer {#client}

- **[I2CP](/docs/specs/i2cp)** - I2P Control Protocol एप्लिकेशन्स को I2P नेटवर्क तक पहुंचने की अनुमति देता है बिना router API का प्रत्यक्ष उपयोग किए

## I2P End-to-End Transport Layer {#e2e-transport}

- **[Streaming Library](/docs/api/streaming)** - TCP के समान विश्वसनीय, क्रमबद्ध डिलीवरी प्रदान करती है
- **[Datagram Library](/docs/api/datagrams)** - UDP के समान अविश्वसनीय डिलीवरी प्रदान करती है

## I2P एप्लिकेशन इंटरफेस लेयर {#app-interface}

एप्लिकेशन डेवलपर्स के लिए वैकल्पिक इंटरफेसेस:

- **[I2PTunnel](/docs/api/i2ptunnel)** - TCP कनेक्शन को I2P के अंदर और बाहर tunnel करता है
- **[SAMv3](/docs/api/samv3)** - गैर-Java एप्लिकेशन के लिए Simple Anonymous Messaging प्रोटोकॉल

## I2P एप्लिकेशन प्रॉक्सी परत {#app-proxy}

मानक इंटरनेट प्रोटोकॉल के लिए प्रॉक्सी:

- **HTTP** - वेब ब्राउज़िंग प्रॉक्सी
- **IRC** - Internet Relay Chat प्रॉक्सी
- **[SOCKS](/docs/api/socks)** - SOCKS4/4a/5 प्रॉक्सी
- **Streamr** - UDP स्ट्रीमिंग प्रॉक्सी

## एप्लिकेशन {#applications}

एप्लिकेशन I2P के साथ विभिन्न स्तरों पर इंटरफेस कर सकते हैं:

**Streaming/Datagram Applications:** - streaming या datagram libraries का सीधे उपयोग करने वाले I2P-native applications

**SAM Applications:** - SAM प्रोटोकॉल का उपयोग करके किसी भी भाषा में एप्लिकेशन

**I2P-विशिष्ट एप्लिकेशन:** - I2P के लिए विशेष रूप से डिज़ाइन की गई एप्लिकेशन (I2PSnark, SusiMail, आदि)

**मानक इंटरनेट एप्लिकेशन:** - I2P प्रॉक्सी का उपयोग करने वाले नियमित एप्लिकेशन (वेब ब्राउज़र, IRC क्लाइंट, आदि)

## स्टैक आरेख {#diagram}

![I2P Protocol Stack](/images/protocol_stack.png)

नोट: SAM स्ट्रीमिंग लाइब्रेरी और डेटाग्राम दोनों का उपयोग कर सकता है।
