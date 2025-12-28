---
title: "SAM v2"
description: "लीगेसी Simple Anonymous Messaging प्रोटोकॉल"
slug: "samv2"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **अप्रचलित:** SAM v2 I2P 0.6.1.31 के साथ जारी किया गया था और अब इसका रखरखाव नहीं किया जाता। नए विकास के लिए [SAM v3](/docs/api/samv3/) का उपयोग करें। v2 में v1 की तुलना में केवल एक सुधार था: एकल SAM कनेक्शन पर मल्टीप्लेक्स किए गए कई सॉकेट्स के लिए समर्थन।

## संस्करण नोट्स

- रिपोर्ट की गई संस्करण स्ट्रिंग `"2.0"` ही बनी रहती है.
- 0.9.14 से `HELLO VERSION` संदेश एक-अंकीय `MIN`/`MAX` मानों को स्वीकार करता है और `MIN` पैरामीटर वैकल्पिक है.
- `DEST GENERATE` `SIGNATURE_TYPE` का समर्थन करता है, इसलिए Ed25519 डेस्टिनेशन बनाए जा सकते हैं.

## सत्र की मूल बातें

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]
```
- प्रत्येक डेस्टिनेशन के पास केवल एक सक्रिय SAM सत्र हो सकता है (स्ट्रीम्स, डेटाग्राम, या रॉ)।
- `STYLE` वर्चुअल स्ट्रीम्स, हस्ताक्षरित डेटाग्राम, या रॉ डेटाग्राम का चयन करता है।
- अतिरिक्त विकल्प I2CP को पास किए जाते हैं (उदाहरण के लिए, `tunnels.quantityInbound=3`)।
- प्रतिक्रियाएँ v1 के अनुरूप हैं: `SESSION STATUS RESULT=OK|DUPLICATED_DEST|I2P_ERROR|INVALID_KEY`।

## संदेश एन्कोडिंग

लाइन-उन्मुख ASCII जिसमें `key=value` युग्म स्पेस द्वारा अलग किए गए हों (मान उद्धरण चिह्नों में हो सकते हैं)। संचार प्रकार v1 के समान हैं:

- I2P streaming library के माध्यम से स्ट्रीम्स
- प्रतिक्रिया-योग्य डेटाग्राम (`PROTO_DATAGRAM`)
- रॉ डेटाग्राम (`PROTO_DATAGRAM_RAW`)

## कब उपयोग करें

केवल उन पुराने क्लाइंट्स के लिए जो माइग्रेट नहीं कर सकते। SAM v3 प्रदान करता है:

- बाइनरी डेस्टिनेशन हस्तांतरण (`DEST GENERATE BASE64`)
- Subsessions (उप-सत्र) और DHT (वितरित हैश तालिका) समर्थन (v3.3)
- बेहतर त्रुटि रिपोर्टिंग और विकल्प नेगोशिएशन

देखें:

- [SAM v1](/docs/legacy/sam/)
- [SAM v3](/docs/api/samv3/)
- [डेटाग्राम API](/docs/api/datagrams/)
- [स्ट्रीमिंग प्रोटोकॉल](/docs/specs/streaming/)
