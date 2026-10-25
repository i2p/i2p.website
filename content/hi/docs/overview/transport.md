---
title: "ट्रांसपोर्ट अवलोकन"
description: "बिंदु-से-बिंदु router संचार के लिए I2P की transport layer का अवलोकन"
slug: "transport"
aliases:
  - "/hi/transport"
  - "/hi/transport/"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## I2P में Transports

I2P में एक "transport" दो router के बीच प्रत्यक्ष, point-to-point संचार के लिए एक विधि है। Transport को बाहरी विरोधियों के खिलाफ गोपनीयता और अखंडता प्रदान करनी चाहिए, जबकि यह प्रमाणित करना चाहिए कि संपर्क किया गया router वही है जिसे दिया गया संदेश प्राप्त करना चाहिए।

I2P एक साथ कई transports का समर्थन करता है। वर्तमान में तीन transports लागू किए गए हैं:

1. [NTCP](/docs/legacy/ntcp/), एक Java New I/O (NIO) TCP transport
2. [SSU](/docs/legacy/ssu/), या Secure Semireliable UDP
3. [NTCP2](/docs/specs/ntcp2/), NTCP का एक नया संस्करण

प्रत्येक एक "कनेक्शन" प्रतिमान प्रदान करता है, जिसमें प्रमाणीकरण, फ्लो कंट्रोल, acknowledgments और retransmission शामिल है।

- [I2NP](/docs/specs/i2np/) संदेशों की विश्वसनीय डिलीवरी। Transports केवल I2NP संदेश डिलीवरी का समर्थन करते हैं। ये सामान्य-उद्देश्य डेटा पाइप नहीं हैं।
- सभी transports द्वारा संदेशों की क्रमबद्ध डिलीवरी की गारंटी नहीं है।
- Router addresses का एक सेट बनाए रखना, प्रत्येक transport के लिए एक या अधिक, जिन्हें router अपनी वैश्विक संपर्क जानकारी (RouterInfo) के रूप में प्रकाशित करता है। प्रत्येक transport इन addresses में से किसी एक का उपयोग करके कनेक्ट हो सकता है, जो IPv4 या (version 0.9.8 के अनुसार) IPv6 हो सकते हैं।
- प्रत्येक आउटगोइंग संदेश के लिए सबसे अच्छे transport का चयन
- प्राथमिकता के अनुसार आउटबाउंड संदेशों की queueing
- Router कॉन्फ़िगरेशन के अनुसार आउटबाउंड और इनबाउंड दोनों की bandwidth सीमा
- Transport connections का setup और teardown
- Point-to-point communications की encryption
- प्रत्येक transport के लिए connection limits का रखरखाव, इन limits के लिए विभिन्न thresholds का implementation, और threshold status को router तक पहुंचाना ताकि वह status के आधार पर operational changes कर सके
- UPnP (Universal Plug and Play) का उपयोग करके firewall port opening
- Cooperative NAT/Firewall traversal
- विभिन्न methods द्वारा local IP detection, जिसमें UPnP, incoming connections का inspection, और network devices की enumeration शामिल है
- Transports के बीच firewall status और local IP के coordination, और इनमें से किसी भी में changes
- Firewall status और local IP, और इनमें से किसी भी में changes को router और user interface तक पहुंचाना
- Consensus clock का निर्धारण, जो NTP के backup के रूप में router की clock को आवधिक रूप से अपडेट करने के लिए उपयोग किया जाता है
- प्रत्येक peer के लिए status का रखरखाव, जिसमें यह शामिल है कि वह कनेक्टेड है या नहीं, हाल ही में कनेक्टेड था या नहीं, और अंतिम प्रयास में पहुंच योग्य था या नहीं
- Local rule set के अनुसार valid IP addresses की qualification
- Router द्वारा maintained automated और manual banned peers की सूचियों का सम्मान करना, और उन peers के साथ outbound और inbound connections को मना करना

---

I2P में transport subsystem निम्नलिखित सेवाएं प्रदान करता है:

## ट्रांसपोर्ट सेवाएं

---

- एक router के पास कोई प्रकाशित पते नहीं हैं, इसलिए इसे "छुपा हुआ" माना जाता है और यह आने वाले कनेक्शन प्राप्त नहीं कर सकता
- एक router firewalled है, और इसलिए यह एक SSU पता प्रकाशित करता है जिसमें सहयोगी peers या "introducers" की सूची होती है जो NAT traversal में सहायता करेंगे (विवरण के लिए [SSU spec](/docs/legacy/ssu/) देखें)
- एक router firewalled नहीं है या इसके NAT ports खुले हैं; यह NTCP और SSU दोनों पते प्रकाशित करता है जिनमें सीधे पहुँच योग्य IP और ports होते हैं।

transport subsystem router addresses का एक सेट बनाए रखता है, जिनमें से प्रत्येक में एक transport method, IP, और port की सूची होती है। ये addresses विज्ञापित संपर्क बिंदुओं का निर्माण करते हैं, और router द्वारा network database में प्रकाशित किए जाते हैं। Addresses में अतिरिक्त विकल्पों का एक मनमाना सेट भी हो सकता है।

## Transport Addresses

प्रत्येक transport method कई router addresses प्रकाशित कर सकता है।

सामान्य परिस्थितियां हैं:

---

- transport प्राथमिकताओं का कॉन्फ़िगरेशन
- क्या transport पहले से ही peer से जुड़ा है
- विभिन्न कनेक्शन सीमा थ्रेशोल्ड की तुलना में वर्तमान कनेक्शन्स की संख्या
- क्या peer के साथ हाल की कनेक्शन प्रयास असफल हुए हैं
- संदेश का आकार, क्योंकि अलग-अलग transport की अलग आकार सीमाएं होती हैं
- क्या peer उस transport के लिए आने वाले कनेक्शन स्वीकार कर सकता है, जैसा कि उसके RouterInfo में विज्ञापित है
- क्या कनेक्शन अप्रत्यक्ष होगा (introducers की आवश्यकता) या प्रत्यक्ष
- peer की transport प्राथमिकता, जैसा कि उसके RouterInfo में विज्ञापित है

ट्रांसपोर्ट सिस्टम केवल [I2NP messages](/docs/specs/i2np/) को डिलीवर करता है। किसी भी संदेश के लिए चुना गया ट्रांसपोर्ट ऊपरी-स्तर के प्रोटोकॉल और सामग्री से स्वतंत्र होता है (router या client messages, बाहरी एप्लिकेशन I2P से कनेक्ट करने के लिए TCP या UDP का उपयोग कर रहा था या नहीं, ऊपरी स्तर [the streaming library](/docs/api/streaming/) या [datagrams](/docs/api/datagrams/) का उपयोग कर रहा था या नहीं, आदि)।

## परिवहन चयन

प्रत्येक आउटगोइंग संदेश के लिए, transport system प्रत्येक transport से "बोलियाँ" माँगता है। सबसे कम (सर्वोत्तम) मूल्य की बोली लगाने वाला transport बोली जीत जाता है और डिलीवरी के लिए संदेश प्राप्त करता है। कोई transport बोली लगाने से मना कर सकता है।

कोई transport बिड करता है या नहीं, और किस मूल्य के साथ, यह कई कारकों पर निर्भर करता है:

सामान्यतः, bid values इस प्रकार चुने जाते हैं कि दो routers किसी भी समय केवल एक single transport से जुड़े हों। हालांकि, यह कोई आवश्यकता नहीं है।

- एक TLS/SSH समान transport
- उन routers के लिए एक "अप्रत्यक्ष" transport जो अन्य सभी routers द्वारा पहुंचे जाने योग्य नहीं हैं ("प्रतिबंधित routes" का एक रूप)
- Tor-संगत pluggable transports

---

अतिरिक्त transports विकसित किए जा सकते हैं, जिनमें शामिल हैं:

## नए transports और भविष्य का कार्य

प्रत्येक transport के लिए डिफ़ॉल्ट कनेक्शन सीमा को समायोजित करने का काम जारी है। I2P को एक "mesh network" के रूप में डिज़ाइन किया गया है, जहां यह माना जाता है कि कोई भी router किसी भी अन्य router से जुड़ सकता है। यह अवधारणा उन routers द्वारा टूट सकती है जिन्होंने अपनी कनेक्शन सीमा पार कर ली है, और उन routers द्वारा जो प्रतिबंधात्मक state firewalls के पीछे हैं (restricted routes)।

- एक TLS/SSH जैसा ट्रांसपोर्ट
- उन राउटर्स के लिए एक "अप्रत्यक्ष" ट्रांसपोर्ट जो अन्य सभी राउटर्स द्वारा पहुंच योग्य नहीं हैं (सीमित मार्गों का एक रूप)
- टोर-अनुकूल लगाने योग्य ट्रांसपोर्ट

वर्तमान कनेक्शन सीमाएं SSU के लिए NTCP की तुलना में अधिक हैं, इस धारणा के आधार पर कि NTCP कनेक्शन के लिए मेमोरी आवश्यकताएं SSU की तुलना में अधिक हैं। हालांकि, चूंकि NTCP बफर आंशिक रूप से कर्नेल में हैं और SSU बफर Java heap पर हैं, इस धारणा को सत्यापित करना कठिन है।

[Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf) का विश्लेषण करें और देखें कि transport-layer padding चीजों को कैसे बेहतर बना सकती है।

[ब्रेकिंग एंड इम्प्रूविंग प्रोटोकॉल ऑब्फस्केशन](http://www.iis.se/docs/hjelmvik_breaking.pdf) का विश्लेषण करें और देखें कि ट्रांसपोर्ट-लेयर पैडिंग किस प्रकार चीजों में सुधार कर सकती है।
