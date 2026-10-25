---
title: "Ministreaming लाइब्रेरी"
description: "I2P की पहली TCP-जैसी transport layer पर ऐतिहासिक टिप्पणियां"
slug: "ministreaming"
aliases:
  - "/hi/ministreaming"
  - "/hi/ministreaming/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

## नोट

ministreaming library को "full" [streaming library](/docs/api/streaming) द्वारा बेहतर और विस्तारित किया गया है। Ministreaming अब deprecated है और आज के applications के साथ incompatible है। निम्नलिखित documentation पुराना है। यह भी ध्यान दें कि streaming, ministreaming को समान Java package (net.i2p.client.streaming) में extend करता है, इसलिए वर्तमान API documentation में दोनों शामिल हैं। पुराने ministreaming classes और methods को Javadocs में स्पष्ट रूप से deprecated के रूप में चिह्नित किया गया है।

## Ministreaming Library

ministreaming library कोर [I2CP](/docs/protocol/i2cp) के ऊपर एक परत है जो विश्वसनीय, क्रमानुसार, और प्रमाणित संदेश स्ट्रीम को एक अविश्वसनीय, अव्यवस्थित, और अप्रमाणित संदेश परत पर संचालित करने की अनुमति देती है। ठीक TCP से IP के रिश्ते की तरह, इस streaming कार्यक्षमता में समझौतों और अनुकूलन की एक पूरी श्रृंखला उपलब्ध है, लेकिन इस कार्यक्षमता को बेस I2P कोड में एम्बेड करने के बजाय, इसे अपनी अलग library में विभाजित किया गया है ताकि TCP-जैसी जटिलताओं को अलग रखा जा सके और वैकल्पिक अनुकूलित कार्यान्वयन की अनुमति दी जा सके।

ministreaming library को mihi द्वारा उनकी [I2PTunnel](/docs/api/i2ptunnel) एप्लिकेशन के हिस्से के रूप में लिखा गया था और फिर इसे अलग करके BSD license के तहत जारी किया गया था। इसे "mini"streaming library कहा जाता है क्योंकि यह implementation में कुछ सरलीकरण करती है, जबकि एक अधिक मजबूत streaming library को I2P पर संचालन के लिए और भी अनुकूलित किया जा सकता है। ministreaming library के साथ दो मुख्य समस्याएं हैं: इसका पारंपरिक TCP two phase establishment protocol का उपयोग और वर्तमान में fixed window size का 1 होना। establishment की समस्या लंबे समय तक चलने वाली streams के लिए मामूली है, लेकिन छोटी streams के लिए, जैसे कि quick HTTP requests, इसका प्रभाव महत्वपूर्ण हो सकता है। window size के लिए, ministreaming library भेजे गए messages के भीतर कोई ID या ordering maintain नहीं करती (या कोई application level ACK या SACK शामिल नहीं करती), इसलिए इसे दूसरा message भेजने से पहले औसतन दो गुना समय तक इंतजार करना पड़ता है जितना एक message भेजने में लगता है।

इन समस्याओं के बावजूद भी, ministreaming library कई स्थितियों में काफी अच्छा प्रदर्शन करती है, और इसका API काफी सरल है तथा विभिन्न streaming implementations के आने पर भी अपरिवर्तित रहने में सक्षम है। यह library अपनी स्वयं की ministreaming.jar में deploy की गई है। Java में developers जो इसका उपयोग करना चाहते हैं वे API को सीधे access कर सकते हैं, जबकि अन्य भाषाओं के developers इसे [SAM](/docs/api/samv3) के streaming support के माध्यम से उपयोग कर सकते हैं।
