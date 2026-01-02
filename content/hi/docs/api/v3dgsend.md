---
title: "v3dgsend"
description: "SAM v3 के माध्यम से I2P डेटाग्राम भेजने के लिए CLI उपयोगिता"
slug: "v3dgsend"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> स्थिति: यह `v3dgsend` उपयोगिता के लिए एक संक्षिप्त संदर्भ है। यह [Datagram API](/docs/api/datagrams/) और [SAM v3](/docs/api/samv3/) दस्तावेज़ों का पूरक है।

## अवलोकन

`v3dgsend` SAM v3 इंटरफ़ेस का उपयोग करके I2P datagrams भेजने के लिए एक command-line सहायक उपकरण है। यह datagram वितरण का परीक्षण करने, सेवाओं के प्रोटोटाइप बनाने और पूर्ण client लिखे बिना end-to-end व्यवहार की पुष्टि करने के लिए उपयोगी है।

सामान्य उपयोग में शामिल हैं:

- किसी गंतव्य (Destination) तक डेटाग्राम पहुंच की स्मोक-टेस्टिंग
- फ़ायरवॉल और एड्रेस बुक कॉन्फ़िगरेशन की पुष्टि करना
- रॉ बनाम साइन्ड (जवाब देने योग्य) डेटाग्राम के साथ प्रयोग करना

## उपयोग

बेसिक इनवोकेशन प्लेटफॉर्म और पैकेजिंग के अनुसार भिन्न होता है। सामान्य विकल्पों में शामिल हैं:

- Destination: base64 Destination या `.i2p` नाम
- Protocol: raw (PROTOCOL 18) या signed (PROTOCOL 17)
- Payload: inline स्ट्रिंग या फ़ाइल इनपुट

सटीक flags के लिए अपने distribution की packaging या `--help` output देखें।

## यह भी देखें

- [Datagram API](/docs/api/datagrams/)
- [SAM v3](/docs/api/samv3/)
- [Streaming Library](/docs/api/streaming/) (datagrams का विकल्प)
