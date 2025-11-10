---
title: "Maven Central पर I2P"
date: 2016-06-13
author: "str4d"
description: "I2P क्लाइंट लाइब्रेरीज़ अब Maven Central पर उपलब्ध हैं!"
categories: ["summer-dev"]
---

हम Summer Dev के APIs महीने के लगभग मध्य में हैं, और कई मोर्चों पर बेहतरीन प्रगति कर रहे हैं। मुझे यह घोषणा करते हुए खुशी है कि इनमें से पहला पूरा हो चुका है: I2P क्लाइंट लाइब्रेरीज़ अब Maven Central पर उपलब्ध हैं!

इससे Java डेवलपर्स के लिए अपनी applications में I2P का उपयोग करना काफी आसान हो जाएगा। मौजूदा इंस्टॉलेशन से लाइब्रेरीज़ प्राप्त करने की आवश्यकता के बजाय, वे बस I2P को अपनी dependencies में जोड़ सकते हैं। नए संस्करणों में अपग्रेड करना भी इसी तरह बहुत आसान होगा।

## इनका उपयोग कैसे करें

दो लाइब्रेरी हैं जिनके बारे में आपको जानना चाहिए:

- `net.i2p:i2p` - The core I2P APIs; you can use these to send individual datagrams.
- `net.i2p.client:streaming` - A TCP-like set of sockets for communicating over I2P.

इनमें से एक या दोनों को अपने प्रोजेक्ट की निर्भरताओं में जोड़ें, और आप तैयार हैं!

### Gradle

```
compile 'net.i2p:i2p:0.9.26'
compile 'net.i2p.client:streaming:0.9.26'
```
### Gradle

```xml
<dependency>
    <groupId>net.i2p</groupId>
    <artifactId>i2p</artifactId>
    <version>0.9.26</version>
</dependency>
<dependency>
    <groupId>net.i2p.client</groupId>
    <artifactId>streaming</artifactId>
    <version>0.9.26</version>
</dependency>
```
अन्य बिल्ड प्रणालियों के लिए, कोर और स्ट्रीमिंग लाइब्रेरीज़ से संबंधित Maven Central के पृष्ठ देखें।

Android डेवलपर्स को I2P Android client library का उपयोग करना चाहिए, जिसमें वही लाइब्रेरियाँ और साथ ही Android-विशिष्ट हेल्पर्स शामिल हैं। इसे जल्द ही नई I2P लाइब्रेरियों पर निर्भर बनाने के लिए अपडेट किया जाएगा, ताकि क्रॉस-प्लेटफ़ॉर्म अनुप्रयोग I2P Android या डेस्कटॉप I2P में से किसी के साथ नेटिव रूप से काम कर सकें।

## Get hacking!

इन लाइब्रेरीज़ के साथ शुरुआत करने में मदद के लिए हमारी एप्लिकेशन विकास मार्गदर्शिका देखें। आप IRC (इंटरनेट रिले चैट) पर #i2p-dev में उनके बारे में हमसे चैट भी कर सकते हैं। और यदि आप इन्हें उपयोग करना शुरू करते हैं, तो Twitter पर #I2PSummer हैशटैग के साथ हमें बताइए कि आप किस पर काम कर रहे हैं!
