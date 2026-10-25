---
title: "डेटाग्राम"
description: "I2CP के ऊपर प्रमाणित, उत्तर देने योग्य, और कच्चे संदेश प्रारूप"
slug: "datagrams"
aliases:
  - "/hi/datagrams"
  - "/hi/datagrams/"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## डेटाग्राम अवलोकन {#overview}

Datagrams आधार [I2CP](/docs/specs/i2cp) पर निर्मित होते हैं ताकि मानक प्रारूप में प्रमाणित और जवाबी संदेश प्रदान कर सकें। इससे एप्लिकेशन्स विश्वसनीय रूप से datagram से "from" पता पढ़ सकते हैं और जान सकते हैं कि वह पता वास्तव में संदेश भेजा है। यह कुछ एप्लिकेशन्स के लिए आवश्यक है क्योंकि आधार I2P संदेश पूरी तरह से कच्चा होता है - इसमें कोई "from" पता नहीं होता (IP packets के विपरीत)। इसके अतिरिक्त, payload पर हस्ताक्षर करके संदेश और भेजने वाले को प्रमाणित किया जाता है।

Datagrams, [streaming library packets](/docs/api/streaming) की तरह, एक application-level construct हैं। ये protocols निम्न-स्तरीय [transports](/docs/overview/transport) से स्वतंत्र हैं; protocols को router द्वारा I2NP messages में परिवर्तित किया जाता है, और कोई भी protocol किसी भी transport द्वारा carry किया जा सकता है।

## एप्लिकेशन गाइड {#application}

Java में लिखे गए एप्लिकेशन datagram API का उपयोग कर सकते हैं, जबकि अन्य भाषाओं में एप्लिकेशन [SAM](/docs/api/samv3) के datagram समर्थन का उपयोग कर सकते हैं। [SOCKS proxy](/docs/api/socks), 'streamr' tunnel प्रकार, और udpTunnel classes में i2ptunnel में सीमित समर्थन भी उपलब्ध है।

### Datagram Length {#length}

एप्लिकेशन डिज़ाइनर को repliable बनाम non-repliable डेटाग्राम के ट्रेडऑफ पर सावधानीपूर्वक विचार करना चाहिए। साथ ही, डेटाग्राम का आकार विश्वसनीयता को प्रभावित करेगा, क्योंकि tunnel का विभाजन 1KB tunnel संदेशों में होता है। जितने अधिक संदेश खंड होंगे, उतनी ही अधिक संभावना है कि उनमें से कोई एक मध्यवर्ती hop द्वारा छोड़ दिया जाएगा। कुछ KB से बड़े संदेशों की अनुशंसा नहीं की जाती। लगभग 10 KB से अधिक पर, डिलिवरी की संभावना नाटकीय रूप से कम हो जाती है।

[Datagrams Specification पेज देखें।](/docs/specs/datagrams)

यह भी ध्यान दें कि निचली परतों द्वारा जोड़े गए विभिन्न ओवरहेड, विशेष रूप से garlic messages, Kademlia-over-UDP एप्लिकेशन द्वारा उपयोग किए जाने वाले रुक-रुक कर आने वाले संदेशों पर बड़ा बोझ डालते हैं। वर्तमान में implementations को streaming library का उपयोग करके लगातार ट्रैफिक के लिए ट्यून किया गया है।

### I2CP प्रोटोकॉल संख्या और पोर्ट्स {#protocol}

signed (repliable) datagrams के लिए मानक I2CP protocol संख्या PROTO_DATAGRAM (17) है। Applications I2CP header में protocol सेट करना चुन सकती हैं या नहीं भी। default implementation-dependent है। यह समान Destination पर प्राप्त datagram और streaming traffic को demultiplex करने के लिए सेट होना आवश्यक है।

चूंकि datagrams connection-oriented नहीं होते हैं, application को datagrams को विशिष्ट peers या communications sessions के साथ संबद्ध करने के लिए port numbers की आवश्यकता हो सकती है, जैसा कि IP पर UDP के साथ पारंपरिक रूप से होता है। Applications I2CP (gzip) header में 'from' और 'to' ports जोड़ सकती हैं जैसा कि [I2CP page](/docs/specs/i2cp#format) में वर्णित है।

datagram API में यह निर्दिष्ट करने के लिए कोई method नहीं है कि यह non-repliable (raw) है या repliable है। application को उपयुक्त प्रकार की अपेक्षा करने के लिए डिज़ाइन किया जाना चाहिए। I2CP protocol number या port का उपयोग application द्वारा datagram type को इंगित करने के लिए किया जाना चाहिए। I2CP protocol numbers PROTO_DATAGRAM (signed, जिसे Datagram1 भी कहा जाता है), PROTO_DATAGRAM_RAW, PROTO_DATAGRAM2, और PROTO_DATAGRAM3 इस उद्देश्य के लिए I2PSession API में परिभाषित हैं। client/server datagram applications में एक सामान्य design pattern यह है कि एक request के लिए signed datagrams का उपयोग करें जिसमें एक nonce शामिल हो, और reply के लिए raw datagram का उपयोग करें, जो request से nonce वापस करे।

**डिफ़ॉल्ट:**

- PROTO_DATAGRAM = 17
- PROTO_DATAGRAM_RAW = 18
- PROTO_DATAGRAM2 = 19
- PROTO_DATAGRAM3 = 20

### डेटा अखंडता {#integrity}

डेटा अखंडता [I2CP layer](/docs/specs/i2cp#format) में लागू gzip CRC-32 checksum द्वारा सुनिश्चित की जाती है। प्रमाणित डेटाग्राम (Datagram1 और Datagram2) भी अखंडता सुनिश्चित करते हैं। datagram protocol में कोई checksum field नहीं है।

### पैकेट एनकैप्सुलेशन {#encapsulation}

प्रत्येक datagram को I2P के माध्यम से एक single message के रूप में भेजा जाता है (या एक [Garlic Message](/docs/overview/garlic-routing) में एक individual clove के रूप में)। Message encapsulation अंतर्निहित [I2CP](/docs/specs/i2cp), [I2NP](/docs/specs/i2np), और [tunnel message](/docs/specs/tunnel-message) layers में implemented है। datagram protocol में कोई packet delimiter mechanism या length field नहीं है।

## विनिर्देश {#spec}

[Datagrams Specification पेज देखें।](/docs/specs/datagrams)
