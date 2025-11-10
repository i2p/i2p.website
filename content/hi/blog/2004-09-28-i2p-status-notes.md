---
title: "2004-09-28 के लिए I2P स्थिति नोट्स"
date: 2004-09-28
author: "jr"
description: "साप्ताहिक I2P स्थिति अद्यतन, जिसमें नए ट्रांसपोर्ट प्रोटोकॉल का कार्यान्वयन, IP की स्वचालित पहचान, और 0.4.1 रिलीज़ की प्रगति शामिल है"
categories: ["status"]
---

सभी को नमस्ते, साप्ताहिक अपडेट का समय

## अनुक्रमणिका:

1. New transport
2. 0.4.1 status
3. ???

## 1) नया transport (ट्रांसपोर्ट प्रोटोकॉल)

0.4.1 रिलीज़ अपेक्षा से अधिक समय ले रही है, लेकिन नया ट्रांसपोर्ट प्रोटोकॉल और उसका कार्यान्वयन योजना के अनुसार हर चीज़ के साथ तैयार है - IP पहचान, कम-लागत कनेक्शन स्थापना, और एक आसान इंटरफ़ेस जो कनेक्शन विफल होने पर डीबग में मदद करता है। यह पुराने ट्रांसपोर्ट प्रोटोकॉल को पूरी तरह हटाकर और नया लागू करके किया गया है, हालांकि हमारे पास अब भी वही बज़वर्ड्स हैं (2048bit DH + STS, AES256/CBC/PKCS#5)। यदि आप प्रोटोकॉल की समीक्षा करना चाहें, तो यह दस्तावेज़ों में है। नया कार्यान्वयन भी काफ़ी साफ़-सुथरा है, क्योंकि पुराना संस्करण पिछले साल भर में संचित हुए अपडेट्स का बस एक गुच्छा था।

Anyway, there are some things in the new IP detection code that are worth mentioning. Most importantly, it is entirely optional - if you specify an IP address on the config page (or in the router.config itself), it will always use that address, no matter what. However, if you leave that blank, your router will let the first peer it contacts tell it what its IP address is, which it will then start listening on (after adding that to its own RouterInfo and placing that in the network database). Well, thats not quite true - if you haven't explicitly set an IP address, it will trust anyone to tell it what IP address it can be reached at whenever the peer has no connections. So, if your internet connection restarts, perhaps giving you a new DHCP address, your router will trust the first peer it is able to reach.

हाँ, इसका मतलब है कि अब dyndns की ज़रूरत नहीं है। आप चाहें तो इसे इस्तेमाल करना जारी रख सकते हैं, लेकिन यह आवश्यक नहीं है।

फिर भी, यह आपकी सारी ज़रूरतें पूरी नहीं करता - यदि आपके पास NAT या फ़ायरवॉल है, तो अपना बाहरी IP पता जानना लड़ाई का केवल आधा हिस्सा है - आपको NAT या फ़ायरवॉल में inbound port खोलना अभी भी ज़रूरी है। लेकिन, यह एक शुरुआत है।

(एक अतिरिक्त टिप्पणी के रूप में, जो लोग अपने निजी I2P नेटवर्क या सिमुलेटर चला रहे हैं, उनके लिए सेट किए जाने वाले फ्लैग्स की एक नई जोड़ी है i2np.tcp.allowLocal और i2np.tcp.tagFile)

## 2) 0.4.1 स्थिति

0.4.1 के रोडमैप में जो आइटम हैं, उनके अलावा, मैं कुछ और चीज़ें भी शामिल करना चाहता हूँ — बग फिक्स और नेटवर्क मॉनिटरिंग अपडेट्स, दोनों। अभी मैं मेमोरी में अत्यधिक churn संबंधी समस्याओं का पता लगा रहा हूँ, और नेटवर्क पर कभी-कभी दिखने वाली विश्वसनीयता समस्याओं के बारे में कुछ परिकल्पनाओं की पड़ताल करना चाहता हूँ, लेकिन हम जल्द ही रिलीज़ जारी करने के लिए तैयार होंगे, शायद गुरुवार को। दुर्भाग्य से यह backwards compatible (पुराने संस्करणों के साथ संगत) नहीं होगा, इसलिए थोड़ी दिक्कतें रहेंगी, पर नई अपग्रेड प्रक्रिया और अधिक लचीले ट्रांसपोर्ट इम्प्लीमेंटेशन के साथ, यह पिछली backwards incompatible अपडेट्स जितना बुरा नहीं होना चाहिए।

## 3) ???

हाँ, पिछले दो हफ्तों में हमारे अपडेट संक्षिप्त रहे हैं, क्योंकि हम जमीनी स्तर पर कार्यान्वयन पर ध्यान दे रहे हैं, न कि विभिन्न उच्च-स्तरीय डिज़ाइनों पर। मैं आपको प्रोफाइलिंग डेटा के बारे में, या नए ट्रांसपोर्ट के लिए 10,000 कनेक्शन टैग कैश के बारे में बता सकता हूँ, मगर वह इतना दिलचस्प नहीं है। फिर भी आप सबके पास चर्चा करने के लिए कुछ अतिरिक्त बातें हो सकती हैं, तो आज रात की बैठक में आ जाइए और खुलकर बात रखिए।

=jr
