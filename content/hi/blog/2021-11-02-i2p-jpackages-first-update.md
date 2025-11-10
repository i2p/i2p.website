---
title: "I2P Jpackages को उनका पहला अपडेट मिला"
date: 2021-11-02
author: "idk"
description: "नए, स्थापित करने में आसान पैकेज एक नए मील के पत्थर तक पहुँच गए हैं"
categories: ["general"]
---

कुछ महीने पहले हमने नए पैकेज जारी किए थे, जिनसे हमारी उम्मीद थी कि वे I2P नेटवर्क में नए लोगों को जोड़ने में मदद करेंगे, क्योंकि इससे अधिक लोगों के लिए I2P की स्थापना और विन्यास आसान हो जाएगा। एक बाहरी JVM से Jpackage पर स्विच करके हमने स्थापना प्रक्रिया से दर्जनों चरण हटा दिए, लक्षित ऑपरेटिंग सिस्टमों के लिए मानक पैकेज बनाए, और उन्हें इस तरह साइन किया कि ऑपरेटिंग सिस्टम उन्हें पहचान सके ताकि उपयोगकर्ता सुरक्षित रहें। तब से, jpackage routers ने एक नया मील का पत्थर हासिल किया है—वे अपने पहले क्रमिक अपडेट प्राप्त करने वाले हैं। ये अपडेट JDK 16 jpackage को अद्यतन JDK 17 jpackage से प्रतिस्थापित करेंगे और कुछ छोटे बगों के लिए सुधार प्रदान करेंगे जिन्हें हमने रिलीज़ के बाद पहचाना।

## Mac OS और Windows दोनों के लिए सामान्य अपडेट

सभी jpackaged I2P इंस्टॉलर्स को निम्नलिखित अपडेट प्राप्त होते हैं:

* Update the jpackaged I2P router to 1.5.1 which is built with JDK 17

कृपया यथाशीघ्र अद्यतन करें।

## I2P Windows Jpackage अद्यतन

केवल Windows के लिए पैकेज निम्नलिखित अपडेट प्राप्त करते हैं:

* Updates I2P in Private Browsing, NoScript browser extensions
* Begins to phase out HTTPS everywhere on new Firefox releases
* Updates launcher script to fix post NSIS launch issue on some architectures

परिवर्तनों की पूर्ण सूची के लिए i2p.firefox में changelog.txt देखें

## I2P Mac OS Jpackage अद्यतन

केवल Mac OS के लिए पैकेजों को निम्नलिखित अपडेट प्राप्त होते हैं:

* No Mac-Specific changes. Mac OS is updated to build with JDK 17.

विकास का सारांश हेतु i2p-jpackage-mac में कमिट्स देखें
