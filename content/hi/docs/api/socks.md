---
title: "SOCKS प्रॉक्सी"
description: "I2P के SOCKS tunnel का सुरक्षित उपयोग"
slug: "socks"
aliases:
  - "/hi/socks"
  - "/hi/socks/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## SOCKS और SOCKS प्रॉक्सी {#overview}

SOCKS proxy रिलीज़ 0.7.1 से काम कर रहा है। SOCKS 4/4a/5 समर्थित हैं। i2ptunnel में एक SOCKS client tunnel बनाकर SOCKS को सक्षम करें। shared-clients और non-shared दोनों समर्थित हैं। कोई SOCKS outproxy नहीं है इसलिए इसका उपयोग सीमित है।

जैसा कि [FAQ](/docs/overview/faq#socks) में कहा गया है:

```
Many applications leak sensitive information that could identify you on the
Internet. I2P only filters connection data, but if the program you intend to
run sends this information as content, I2P has no way to protect your anonymity.
For example, some mail applications will send the IP address of the machine
they are running on to a mail server. There is no way for I2P to filter this,
thus using I2P to 'socksify' existing applications is possible, but extremely
dangerous.
```
और 2005 की एक ईमेल से उद्धरण:

```
... there is a reason why human and others have both built and abandoned the
SOCKS proxies. Forwarding arbitrary traffic is just plain unsafe, and it
behooves us as developers of anonymity and security software to have the safety
of our end users foremost in our minds.
```
यह उम्मीद करना कि हम बिना I2P के ऊपर किसी भी arbitrary client को सुरक्षा और anonymity के लिए उसके व्यवहार और exposed protocols दोनों की auditing किए बिना simply strap कर सकते हैं, naive है। Pretty much *हर* application और protocol anonymity का उल्लंघन करता है, जब तक कि इसे विशेष रूप से इसके लिए designed नहीं किया गया हो, और फिर भी, उनमें से अधिकांश भी ऐसा करते हैं। यही reality है। End users को anonymity और security के लिए designed systems के साथ बेहतर सेवा मिलती है। Existing systems को anonymous environments में काम करने के लिए modify करना कोई छोटा काम नहीं है, existing I2P APIs का simply उपयोग करने की तुलना में orders of magnitude अधिक काम है।

SOCKS proxy मानक address book नामों का समर्थन करता है, लेकिन Base64 destinations का नहीं। Base32 hashes रिलीज़ 0.7 के बाद से काम करने चाहिए। यह केवल outgoing connections का समर्थन करता है, यानी एक I2PTunnel Client। UDP support stubbed out है लेकिन अभी तक काम नहीं कर रहा। Port number द्वारा outproxy selection stubbed out है।

## यह भी देखें {#see-also}

- मीटिंग 81 (16 मार्च, 2004) और मीटिंग 82 (23 मार्च, 2004) के नोट्स।
- [Onioncat](http://www.abenteuerland.at/onioncat/)

## यदि आपको कुछ काम करता मिल जाए {#working}

कृपया हमें बताएं। और socks proxies के जोखिमों के बारे में पर्याप्त चेतावनियां प्रदान करें।
