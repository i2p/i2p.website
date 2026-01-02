---
title: "अक्सर पूछे जाने वाले प्रश्न"
description: "व्यापक I2P FAQ: router सहायता, कॉन्फ़िगरेशन, reseeds, गोपनीयता/सुरक्षा, प्रदर्शन, और समस्या निवारण"
slug: "faq"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## I2P Router सहायता

### I2P किन सिस्टम पर चलेगा? {#systems}

I2P को Java प्रोग्रामिंग भाषा में लिखा गया है। इसका परीक्षण Windows, Linux, FreeBSD और OSX पर किया गया है। एक Android पोर्ट भी उपलब्ध है।

मेमोरी उपयोग के संदर्भ में, I2P डिफ़ॉल्ट रूप से 128 MB RAM उपयोग करने के लिए कॉन्फ़िगर किया गया है। यह ब्राउज़िंग और IRC उपयोग के लिए पर्याप्त है। हालांकि, अन्य गतिविधियों के लिए अधिक मेमोरी आवंटन की आवश्यकता हो सकती है। उदाहरण के लिए, यदि कोई high-bandwidth router चलाना चाहता है, I2P torrents में भाग लेना चाहता है या high-traffic hidden services प्रदान करना चाहता है, तो अधिक मात्रा में मेमोरी की आवश्यकता होती है।

CPU उपयोग के संदर्भ में, I2P को Raspberry Pi श्रृंखला के single-board computers जैसे मामूली सिस्टम पर चलाने के लिए परीक्षण किया गया है। चूंकि I2P क्रिप्टोग्राफिक तकनीकों का भारी उपयोग करता है, एक मजबूत CPU, I2P द्वारा उत्पन्न workload के साथ-साथ सिस्टम के अन्य कार्यों (जैसे Operating System, GUI, अन्य प्रक्रियाएं जैसे Web Browsing) को संभालने के लिए बेहतर रूप से उपयुक्त होगा।

Sun/Oracle Java या OpenJDK का उपयोग करने की सिफारिश की जाती है।

### क्या I2P का उपयोग करने के लिए Java इंस्टॉल करना आवश्यक है? {#java}

हाँ, I2P Core का उपयोग करने के लिए Java आवश्यक है। हम Windows, Mac OSX, और Linux के लिए अपने easy-installers में Java शामिल करते हैं। यदि आप I2P Android app चला रहे हैं तो अधिकांश मामलों में आपको Dalvik या ART जैसे Java runtime की भी आवश्यकता होगी।

### "I2P Site" क्या है और मैं अपने ब्राउज़र को कैसे कॉन्फ़िगर करूं ताकि मैं उन्हें उपयोग कर सकूं? {#I2P-Site}

एक I2P Site एक सामान्य वेबसाइट है सिवाय इसके कि यह I2P के अंदर होस्ट की जाती है। I2P sites के पते सामान्य इंटरनेट पतों की तरह दिखते हैं, जो लोगों की सुविधा के लिए मानव-पठनीय, गैर-क्रिप्टोग्राफिक तरीके से ".i2p" में समाप्त होते हैं। वास्तव में एक I2P Site से कनेक्ट होने के लिए क्रिप्टोग्राफी की आवश्यकता होती है, जिसका अर्थ है कि I2P Site के पते लंबे "Base64" Destinations और छोटे "B32" पते भी होते हैं। सही तरीके से ब्राउज़ करने के लिए आपको अतिरिक्त कॉन्फ़िगरेशन करने की आवश्यकता हो सकती है। I2P Sites को ब्राउज़ करने के लिए आपकी I2P इंस्टॉलेशन में HTTP Proxy को सक्रिय करना और फिर इसका उपयोग करने के लिए अपने ब्राउज़र को कॉन्फ़िगर करना आवश्यक होगा। अधिक जानकारी के लिए, नीचे "Browsers" अनुभाग या "Browser Configuration" गाइड देखें।

### राउटर कंसोल में Active x/y संख्याओं का क्या अर्थ है? {#active}

आपके router console के Peers पेज पर, आपको दो संख्याएं दिखाई दे सकती हैं - Active x/y। पहली संख्या उन peers की संख्या है जिन्हें आपने पिछले कुछ मिनटों में संदेश भेजा है या जिनसे संदेश प्राप्त किया है। दूसरी संख्या हाल ही में देखे गए peers की संख्या है, यह हमेशा पहली संख्या से बड़ी या बराबर होगी।

### मेरे router में बहुत कम सक्रिय peers हैं, क्या यह ठीक है? {#peers}

हां, यह सामान्य हो सकता है, खासकर जब router अभी-अभी शुरू किया गया हो। नए routers को शुरू होने और नेटवर्क के बाकी हिस्सों से जुड़ने में समय लगेगा। नेटवर्क एकीकरण, अपटाइम और प्रदर्शन में सुधार करने में मदद के लिए, इन सेटिंग्स की समीक्षा करें:

- **बैंडविड्थ साझा करें** - यदि कोई router बैंडविड्थ साझा करने के लिए कॉन्फ़िगर किया गया है, तो यह अन्य routers के लिए अधिक ट्रैफ़िक रूट करेगा जो इसे नेटवर्क के बाकी हिस्सों के साथ एकीकृत करने में मदद करता है, साथ ही किसी के स्थानीय कनेक्शन के प्रदर्शन में सुधार करता है। इसे [http://localhost:7657/config](http://localhost:7657/config) पेज पर कॉन्फ़िगर किया जा सकता है।
- **नेटवर्क इंटरफ़ेस** - सुनिश्चित करें कि [http://localhost:7657/confignet](http://localhost:7657/confignet) पेज पर कोई इंटरफ़ेस निर्दिष्ट नहीं है। यह प्रदर्शन को कम कर सकता है जब तक कि आपका कंप्यूटर कई बाहरी IP पतों के साथ मल्टी-होम्ड न हो।
- **I2NP protocol** - सुनिश्चित करें कि router होस्ट के ऑपरेटिंग सिस्टम और खाली नेटवर्क(एडवांस्ड) सेटिंग्स के लिए एक मान्य प्रोटोकॉल पर कनेक्शन की अपेक्षा करने के लिए कॉन्फ़िगर किया गया है। नेटवर्क कॉन्फ़िगरेशन पेज में 'Hostname' फ़ील्ड में कोई IP पता दर्ज न करें। यहाँ आप जो I2NP Protocol चुनते हैं वह केवल तभी उपयोग किया जाएगा जब आपके पास पहले से पहुंचने योग्य पता न हो। उदाहरण के लिए, संयुक्त राज्य अमेरिका में अधिकांश Verizon 4G और 5G वायरलेस कनेक्शन, UDP को ब्लॉक करते हैं और उस पर पहुंचा नहीं जा सकता। अन्य UDP का उपयोग बलपूर्वक करेंगे भले ही यह उनके लिए उपलब्ध हो। सूचीबद्ध I2NP Protocols से एक उचित सेटिंग चुनें।

### मैं कुछ प्रकार की सामग्री का विरोधी हूँ। मैं उन्हें वितरित करने, संग्रहीत करने या एक्सेस करने से कैसे बचूँ? {#badcontent}

डिफ़ॉल्ट रूप से इनमें से कोई भी सामग्री इंस्टॉल नहीं की गई है। हालांकि, चूंकि I2P एक peer-to-peer नेटवर्क है, इसलिए संभव है कि आप गलती से प्रतिबंधित सामग्री का सामना कर सकें। यहां एक सारांश है कि I2P कैसे आपको आपकी मान्यताओं के उल्लंघन में अनावश्यक रूप से शामिल होने से रोकता है।

- **वितरण** - ट्रैफ़िक I2P नेटवर्क के भीतर आंतरिक है, आप एक [exit node](#exit) नहीं हैं (हमारे दस्तावेज़ीकरण में इसे outproxy कहा जाता है)।
- **संग्रहण** - I2P नेटवर्क सामग्री का वितरित संग्रहण नहीं करता है, इसे उपयोगकर्ता द्वारा विशेष रूप से इंस्टॉल और कॉन्फ़िगर करना होता है (उदाहरण के लिए, Tahoe-LAFS के साथ)। यह एक अलग अनाम नेटवर्क, [Freenet](http://freenetproject.org/) की विशेषता है। I2P router चलाने से, आप किसी के लिए सामग्री संग्रहीत नहीं कर रहे हैं।
- **पहुंच** - आपका router आपके विशिष्ट निर्देश के बिना कोई सामग्री अनुरोध नहीं करेगा।

### क्या I2P को ब्लॉक करना संभव है? {#blocking}

हां, अब तक सबसे आसान और सबसे आम तरीका bootstrap, या "Reseed" सर्वर को ब्लॉक करना है। सभी obfuscated ट्रैफ़िक को पूरी तरह से ब्लॉक करना भी काम करेगा (हालांकि यह कई अन्य चीजों को तोड़ देगा जो I2P नहीं हैं और अधिकांश लोग इतनी दूर तक जाने को तैयार नहीं हैं)। reseed ब्लॉकिंग के मामले में, Github पर एक reseed bundle है, इसे ब्लॉक करने से Github भी ब्लॉक हो जाएगा। आप प्रॉक्सी के माध्यम से reseed कर सकते हैं (यदि आप Tor का उपयोग नहीं करना चाहते हैं तो इंटरनेट पर कई मिल सकते हैं) या ऑफ़लाइन friend-to-friend आधार पर reseed bundles साझा कर सकते हैं।

### `wrapper.log` में मुझे एक त्रुटि दिखाई देती है जो Router Console लोड करते समय "`Protocol family unavailable`" बताती है {#protocolfamily}

अक्सर यह त्रुटि कुछ सिस्टम पर किसी भी नेटवर्क सक्षम java सॉफ़्टवेयर के साथ होती है जो डिफ़ॉल्ट रूप से IPv6 का उपयोग करने के लिए कॉन्फ़िगर किए गए हैं। इसे हल करने के कुछ तरीके हैं:

- Linux आधारित सिस्टम पर, आप `echo 0 > /proc/sys/net/ipv6/bindv6only` चला सकते हैं
- `wrapper.config` में निम्नलिखित पंक्तियों को खोजें:
  ```
  #wrapper.java.additional.5=-Djava.net.preferIPv4Stack=true
  #wrapper.java.additional.6=-Djava.net.preferIPv6Addresses=false
  ```
  यदि ये पंक्तियाँ मौजूद हैं, तो "#" हटाकर उन्हें अनकमेंट करें। यदि ये पंक्तियाँ मौजूद नहीं हैं, तो उन्हें "#" के बिना जोड़ें।

एक अन्य विकल्प `~/.i2p/clients.config` से `::1` को हटाना होगा

**चेतावनी**: `wrapper.config` में किए गए किसी भी बदलाव को लागू करने के लिए, आपको router और wrapper को पूरी तरह से बंद करना होगा। अपने router console पर *Restart* क्लिक करने से यह फ़ाइल दोबारा नहीं पढ़ी जाएगी! आपको *Shutdown* क्लिक करना होगा, 11 मिनट प्रतीक्षा करनी होगी, फिर I2P को शुरू करना होगा।

### I2P के भीतर अधिकांश I2P Sites बंद हैं? {#down}

यदि आप हर I2P Site को देखें जो कभी बनाई गई है, तो हां, उनमें से अधिकांश बंद हैं। लोग और I2P Sites आते-जाते रहते हैं। I2P में शुरुआत करने का एक अच्छा तरीका यह है कि उन I2P Sites की सूची देखें जो वर्तमान में चालू हैं। [identiguy.i2p](http://identiguy.i2p) सक्रिय I2P Sites को ट्रैक करता है।

### I2P पोर्ट 32000 पर क्यों सुन रहा है? {#port32000}

हम जो Tanuki java service wrapper उपयोग करते हैं वह इस पोर्ट को खोलता है — localhost से बाइंड — ताकि JVM के अंदर चल रहे सॉफ़्टवेयर के साथ संचार कर सके। जब JVM लॉन्च होता है तो उसे एक key दी जाती है ताकि वह wrapper से कनेक्ट हो सके। JVM द्वारा wrapper से अपना कनेक्शन स्थापित करने के बाद, wrapper किसी भी अतिरिक्त कनेक्शन को अस्वीकार कर देता है।

अधिक जानकारी [wrapper दस्तावेज़ीकरण](http://wrapper.tanukisoftware.com/doc/english/prop-port.html) में पाई जा सकती है।

### मैं अपने ब्राउज़र को कैसे कॉन्फ़िगर करूं? {#browserproxy}

विभिन्न ब्राउज़रों के लिए proxy कॉन्फ़िगरेशन स्क्रीनशॉट के साथ एक अलग पेज पर है। बाहरी टूल्स के साथ अधिक उन्नत कॉन्फ़िगरेशन, जैसे कि ब्राउज़र प्लग-इन FoxyProxy या proxy सर्वर Privoxy, संभव हैं लेकिन आपके सेटअप में लीक पैदा कर सकते हैं।

### I2P के भीतर IRC से कैसे कनेक्ट करें? {#irc}

I2P के भीतर मुख्य IRC सर्वर, Irc2P, के लिए एक tunnel तब बनाया जाता है जब I2P इंस्टॉल किया जाता है ([I2PTunnel कॉन्फ़िगरेशन पेज](http://localhost:7657/i2ptunnel/index.jsp) देखें), और I2P router के शुरू होने पर यह स्वचालित रूप से शुरू हो जाता है। इससे कनेक्ट करने के लिए, अपने IRC क्लाइंट को `localhost 6668` से कनेक्ट करने के लिए कहें। HexChat-जैसे क्लाइंट उपयोगकर्ता सर्वर `localhost/6668` के साथ एक नया नेटवर्क बना सकते हैं (यदि आपके पास प्रॉक्सी सर्वर कॉन्फ़िगर है तो "Bypass proxy server" को टिक करना याद रखें)। Weechat उपयोगकर्ता एक नया नेटवर्क जोड़ने के लिए निम्नलिखित कमांड का उपयोग कर सकते हैं:

```
/server add irc2p localhost/6668
```
### मैं अपनी खुद की I2P Site कैसे सेटअप करूं? {#myI2P-Site}

सबसे आसान तरीका है router console में [i2ptunnel](http://127.0.0.1:7657/i2ptunnel/) लिंक पर क्लिक करना और एक नया 'Server Tunnel' बनाना। आप tunnel destination को किसी मौजूदा webserver के port पर सेट करके dynamic content परोस सकते हैं, जैसे Tomcat या Jetty। आप static content भी परोस सकते हैं। इसके लिए, tunnel destination को इस पर सेट करें: `0.0.0.0 port 7659` और content को `~/.i2p/eepsite/docroot/` directory में रखें। (गैर-Linux सिस्टम पर, यह किसी अलग स्थान पर हो सकता है। router console जांचें।) 'eepsite' सॉफ्टवेयर I2P इंस्टॉलेशन पैकेज के हिस्से के रूप में आता है और I2P शुरू होने पर स्वचालित रूप से शुरू होने के लिए सेट है। इसके द्वारा बनाई गई डिफ़ॉल्ट साइट को http://127.0.0.1:7658 पर एक्सेस किया जा सकता है। हालांकि, आपकी 'eepsite' दूसरों के लिए भी आपकी eepsite key file के माध्यम से सुलभ है, जो यहाँ स्थित है: `~/.i2p/eepsite/i2p/eepsite.keys`। अधिक जानने के लिए, readme file पढ़ें: `~/.i2p/eepsite/README.txt`।

### यदि मैं घर पर I2P पर एक वेबसाइट होस्ट करूं, जिसमें केवल HTML और CSS हो, तो क्या यह खतरनाक है? {#hosting}

यह आपके विरोधी और आपके खतरे के मॉडल पर निर्भर करता है। यदि आप केवल कॉर्पोरेट "गोपनीयता" उल्लंघनों, सामान्य अपराधियों और सेंसरशिप के बारे में चिंतित हैं, तो यह वास्तव में खतरनाक नहीं है। कानून प्रवर्तन संभवतः आपको वैसे भी ढूंढ लेगा यदि वे वास्तव में चाहते हैं। केवल तभी होस्टिंग करना जब आपके पास एक सामान्य (इंटरनेट) होम यूज़र ब्राउज़र चल रहा हो, यह जानना वास्तव में कठिन बना देगा कि उस हिस्से को कौन होस्ट कर रहा है। कृपया अपनी I2P साइट की होस्टिंग को किसी अन्य सेवा की होस्टिंग की तरह ही समझें - यह उतना ही खतरनाक - या सुरक्षित - है जितना आप इसे स्वयं कॉन्फ़िगर और प्रबंधित करते हैं।

नोट: i2p सेवा (destination) को i2p router से अलग होस्ट करने का पहले से ही एक तरीका है। यदि आप [समझते हैं कि यह कैसे](/docs/overview/tech-intro#i2pservices) काम करता है, तो आप वेबसाइट (या सेवा) के लिए एक अलग मशीन को सर्वर के रूप में सेटअप कर सकते हैं जो सार्वजनिक रूप से उपलब्ध होगी और उसे एक [बहुत] सुरक्षित SSH tunnel के माध्यम से webserver पर forward कर सकते हैं या एक सुरक्षित, साझा, filesystem का उपयोग कर सकते हैं।

### I2P ".i2p" वेबसाइटों को कैसे खोजता है? {#addresses}

I2P Address Book एप्लिकेशन मानव-पठनीय नामों को दीर्घकालिक destinations से मैप करता है, जो सेवाओं से जुड़े होते हैं, जिससे यह नेटवर्क डेटाबेस या DNS सेवा की तुलना में hosts फ़ाइल या संपर्क सूची की तरह अधिक काम करता है। यह स्थानीय-प्रथम (local-first) भी है - कोई मान्यता प्राप्त वैश्विक namespace नहीं है, आप तय करते हैं कि कोई भी .i2p डोमेन अंततः किससे मैप होगा। बीच का रास्ता कुछ ऐसा है जिसे "Jump Service" कहा जाता है जो एक मानव-पठनीय नाम प्रदान करता है और आपको एक पृष्ठ पर पुनर्निर्देशित करता है जहाँ आपसे पूछा जाएगा "क्या आप I2P router को $SITE_CRYPTO_KEY को $SITE_NAME.i2p नाम देने की अनुमति देते हैं" या कुछ इस प्रकार की बात। एक बार जब यह आपकी address book में हो जाता है, तो आप साइट को दूसरों के साथ साझा करने में मदद के लिए अपने स्वयं के jump URL उत्पन्न कर सकते हैं।

### Address Book में पते कैसे जोड़ें? {#addressbook}

आप किसी साइट का बेस32 या बेस64 जाने बिना पता नहीं जोड़ सकते जिसे आप देखना चाहते हैं। "होस्टनेम" जो मानव-पठनीय है, केवल क्रिप्टोग्राफिक पते के लिए एक उपनाम है, जो बेस32 या बेस64 से मेल खाता है। क्रिप्टोग्राफिक पते के बिना, I2P Site तक पहुंचने का कोई तरीका नहीं है, यह डिज़ाइन द्वारा है। उन लोगों को पता वितरित करना जो इसे अभी तक नहीं जानते हैं आमतौर पर Jump सेवा प्रदाता की जिम्मेदारी है। किसी अज्ञात I2P Site पर जाने से Jump सेवा का उपयोग ट्रिगर होगा। stats.i2p सबसे विश्वसनीय Jump सेवा है।

यदि आप i2ptunnel के माध्यम से एक साइट होस्ट कर रहे हैं, तो अभी तक इसका jump service के साथ पंजीकरण नहीं होगा। इसे स्थानीय रूप से एक URL देने के लिए, कॉन्फ़िगरेशन पेज पर जाएं और "Add to Local Address Book" वाले बटन पर क्लिक करें। फिर addresshelper URL को देखने और साझा करने के लिए http://127.0.0.1:7657/dns पर जाएं।

### I2P कौन से पोर्ट उपयोग करता है? {#ports}

I2P द्वारा उपयोग किए जाने वाले ports को 2 भागों में विभाजित किया जा सकता है:

1. इंटरनेट-फेसिंग पोर्ट, जो अन्य I2P routers के साथ संचार के लिए उपयोग किए जाते हैं
2. लोकल पोर्ट, स्थानीय कनेक्शन के लिए

इनका विस्तृत विवरण नीचे दिया गया है।

#### 1. इंटरनेट-फेसिंग पोर्ट

नोट: रिलीज़ 0.7.8 के बाद से, नए इंस्टॉल पोर्ट 8887 का उपयोग नहीं करते हैं; जब प्रोग्राम पहली बार चलाया जाता है तो 9000 और 31000 के बीच एक रैंडम पोर्ट चुना जाता है। चुने गए पोर्ट को router [configuration page](http://127.0.0.1:7657/confignet) पर दिखाया जाता है।

**आउटबाउंड**

- [कॉन्फ़िगरेशन पेज](http://127.0.0.1:7657/confignet) पर सूचीबद्ध रैंडम पोर्ट से मनमाने रिमोट UDP पोर्ट्स तक UDP, जवाबों की अनुमति देता है
- रैंडम हाई पोर्ट्स से मनमाने रिमोट TCP पोर्ट्स तक TCP
- पोर्ट 123 पर आउटबाउंड UDP, जवाबों की अनुमति देता है। यह I2P के आंतरिक समय सिंक के लिए आवश्यक है (SNTP के माध्यम से - pool.ntp.org में एक रैंडम SNTP होस्ट या आपके द्वारा निर्दिष्ट किसी अन्य सर्वर से क्वेरी करना)

**INBOUND**

- (वैकल्पिक, अनुशंसित) [configuration page](http://127.0.0.1:7657/confignet) पर उल्लिखित पोर्ट पर किसी भी स्थान से UDP
- (वैकल्पिक, अनुशंसित) [configuration page](http://127.0.0.1:7657/confignet) पर उल्लिखित पोर्ट पर किसी भी स्थान से TCP
- Inbound TCP को [configuration page](http://127.0.0.1:7657/confignet) पर अक्षम किया जा सकता है

#### 2. स्थानीय I2P पोर्ट

स्थानीय I2P पोर्ट डिफ़ॉल्ट रूप से केवल स्थानीय कनेक्शनों को सुनते हैं, सिवाय जहाँ उल्लेख किया गया हो:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PORT</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PURPOSE</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">DESCRIPTION</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1900</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UPnP SSDP UDP multicast listener</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cannot be changed. Binds to all interfaces. May be disabled on <a href="http://127.0.0.1:7657/confignet">confignet</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2827</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A higher level socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a>. May be changed in the bob.config file.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4444</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/0">I2P HTTP Proxy</a> to configure it. Include in your browser's proxy configuration for HTTP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4445</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/1">I2P HTTPS Proxy</a> to configure it. Include in your browser's proxy configuration for HTTPS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6668</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IRC proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A tunnel to the inside-the-I2P IRC network. Disabled by default. Configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/2">irc.postman.i2p (IRC proxy)</a> and may be enabled/disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7654</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2CP (client protocol) port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For advanced client usage. Do not expose to an external network.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7656</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a> and configured on <a href="http://127.0.0.1:7657/sam">sam</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7657 (or 7658 via SSL)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router console</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The router console provides valuable information about your router and the network, in addition to giving you access to configure your router and its associated applications.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7659</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">'eepsite' - an example webserver (Jetty)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Included in the <code>i2pinstall</code> and <code>i2pupdate</code> packages - may be disabled if another webserver is available. May be configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/3">eepsite</a> and disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7660</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel UDP port for SSH</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Required for Grizzled's/novg's UDP support. Instances disabled by default. May be enabled/disabled and configured to use a different port on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">123</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTP Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used by <a href="http://127.0.0.1:7657/confignet">NTP Time Sync</a>. May be disabled/changed.</td>
    </tr>
  </tbody>
</table>
### मेरी एड्रेस बुक में बहुत सारे होस्ट मिसिंग हैं। कुछ अच्छे सब्सक्रिप्शन लिंक कौन से हैं? {#subscriptions}

एड्रेस बुक [http://localhost:7657/dns](http://localhost:7657/dns) पर स्थित है जहाँ अधिक जानकारी मिल सकती है।

**कुछ अच्छे address book subscription लिंक कौन से हैं?**

आप निम्नलिखित प्रयास कर सकते हैं:

- [http://stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
- [http://identiguy.i2p/hosts.txt](http://identiguy.i2p/hosts.txt)

### मैं अपनी अन्य मशीनों से वेब कंसोल को कैसे एक्सेस कर सकता हूं या इसे पासवर्ड प्रोटेक्ट कैसे कर सकता हूं? {#remote_webconsole}

सुरक्षा उद्देश्यों के लिए, router का admin console डिफ़ॉल्ट रूप से केवल स्थानीय इंटरफ़ेस पर कनेक्शन के लिए सुनता है।

कंसोल को दूर से एक्सेस करने के दो तरीके हैं:

1. SSH Tunnel
2. अपने console को एक Public IP address पर उपलब्ध कराने के लिए username और password के साथ configure करना

इन्हें नीचे विस्तार से बताया गया है:

**विधि 1: SSH Tunnel**

यदि आप यूनिक्स-जैसा ऑपरेटिंग सिस्टम चला रहे हैं, तो यह आपके I2P console को दूर से एक्सेस करने का सबसे आसान तरीका है। (नोट: SSH सर्वर सॉफ़्टवेयर Windows चलाने वाले सिस्टम के लिए भी उपलब्ध है, उदाहरण के लिए [https://github.com/PowerShell/Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH))

एक बार जब आप अपने सिस्टम पर SSH एक्सेस कॉन्फ़िगर कर लेते हैं, तो '-L' फ्लैग को उचित आर्गुमेंट्स के साथ SSH को पास किया जाता है - उदाहरण के लिए:

```
ssh -L 7657:localhost:7657 (System_IP)
```
जहाँ '(System_IP)' को आपके सिस्टम के IP address से बदला जाता है। यह command port 7657 (पहले colon से पहले वाली संख्या) को remote system के (जो पहले और दूसरे colon के बीच 'localhost' string द्वारा निर्दिष्ट है) port 7657 (दूसरे colon के बाद वाली संख्या) पर forward करता है। आपका remote I2P console अब आपके local system पर 'http://localhost:7657' के रूप में उपलब्ध होगा और जब तक आपका SSH session सक्रिय रहेगा तब तक उपलब्ध रहेगा।

यदि आप रिमोट सिस्टम पर शेल शुरू किए बिना एक SSH सत्र शुरू करना चाहते हैं, तो आप '-N' फ्लैग जोड़ सकते हैं:

```
ssh -NL 7657:localhost:7657 (System_IP)
```
**विधि 2: अपने console को उपयोगकर्ता नाम और पासवर्ड के साथ सार्वजनिक IP पते पर उपलब्ध कराने के लिए कॉन्फ़िगर करना**

1. `~/.i2p/clients.config` खोलें और बदलें:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
   ```
   इसके साथ:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1,(System_IP) ./webapps/
   ```
   जहाँ आप (System_IP) को अपने सिस्टम के public IP address से बदलें

2. [http://localhost:7657/configui](http://localhost:7657/configui) पर जाएं और यदि चाहें तो console के लिए username और password जोड़ें - अपने I2P console को छेड़छाड़ से सुरक्षित रखने के लिए username और password जोड़ना अत्यधिक अनुशंसित है, जिससे de-anonymization हो सकता है।

3. [http://localhost:7657/index](http://localhost:7657/index) पर जाएं और "Graceful restart" पर क्लिक करें, जो JVM को पुनः आरंभ करता है और client applications को फिर से लोड करता है

उसके शुरू होने के बाद, अब आप अपने console को दूर से एक्सेस कर सकेंगे। router console को `http://(System_IP):7657` पर लोड करें और यदि आपका ब्राउज़र authentication popup को सपोर्ट करता है तो आपसे ऊपर चरण 2 में निर्दिष्ट username और password मांगा जाएगा।

नोट: आप उपरोक्त कॉन्फ़िगरेशन में 0.0.0.0 निर्दिष्ट कर सकते हैं। यह एक इंटरफ़ेस को निर्दिष्ट करता है, न कि नेटवर्क या netmask को। 0.0.0.0 का अर्थ है "सभी इंटरफ़ेस से bind करें", इसलिए यह 127.0.0.1:7657 के साथ-साथ किसी भी LAN/WAN IP पर भी पहुँच योग्य हो सकता है। इस विकल्प का उपयोग करते समय सावधान रहें क्योंकि console आपके सिस्टम पर कॉन्फ़िगर किए गए सभी addresses पर उपलब्ध होगा।

### मैं अपनी अन्य मशीनों से एप्लिकेशन कैसे उपयोग कर सकता हूँ? {#remote_i2cp}

SSH Port Forwarding का उपयोग करने के निर्देशों के लिए कृपया पिछला उत्तर देखें, और अपने console में यह पेज भी देखें: [http://localhost:7657/configi2cp](http://localhost:7657/configi2cp)

### क्या I2P को SOCKS proxy के रूप में उपयोग करना संभव है? {#socks}

SOCKS proxy रिलीज़ 0.7.1 से कार्यशील है। SOCKS 4/4a/5 समर्थित हैं। I2P के पास SOCKS outproxy नहीं है इसलिए यह केवल I2P के भीतर उपयोग तक सीमित है।

कई एप्लिकेशन संवेदनशील जानकारी लीक करते हैं जो इंटरनेट पर आपकी पहचान कर सकती है और यह एक जोखिम है जिसके बारे में I2P SOCKS proxy का उपयोग करते समय आपको जागरूक होना चाहिए। I2P केवल कनेक्शन डेटा को फ़िल्टर करता है, लेकिन यदि आप जिस प्रोग्राम को चलाना चाहते हैं वह इस जानकारी को सामग्री के रूप में भेजता है, तो I2P के पास आपकी गुमनामी की रक्षा करने का कोई तरीका नहीं है। उदाहरण के लिए, कुछ मेल एप्लिकेशन मेल सर्वर को उस मशीन का IP पता भेज देंगे जिस पर वे चल रहे हैं। हम I2P-विशिष्ट टूल या एप्लिकेशन (जैसे torrents के लिए [I2PSnark](http://localhost:7657/i2psnark/)) की सिफारिश करते हैं, या ऐसे एप्लिकेशन जो I2P के साथ उपयोग करने के लिए सुरक्षित माने जाते हैं जिनमें [Firefox](https://www.mozilla.org/) पर पाए जाने वाले लोकप्रिय प्लगइन शामिल हैं।

### मैं नियमित इंटरनेट पर IRC, BitTorrent, या अन्य सेवाओं को कैसे एक्सेस करूं? {#proxy_other}

Outproxies नामक सेवाएं हैं जो I2P और इंटरनेट के बीच पुल का काम करती हैं, जैसे Tor Exit Nodes। HTTP और HTTPS के लिए डिफ़ॉल्ट outproxy कार्यक्षमता `exit.stormycloud.i2p` द्वारा प्रदान की जाती है और इसे StormyCloud Inc द्वारा चलाया जाता है। यह HTTP Proxy में कॉन्फ़िगर किया गया है। इसके अतिरिक्त, गुमनामी की सुरक्षा में मदद के लिए, I2P आपको डिफ़ॉल्ट रूप से नियमित इंटरनेट से अनाम कनेक्शन बनाने की अनुमति नहीं देता है। अधिक जानकारी के लिए कृपया [Socks Outproxy](/docs/api/socks#outproxy) पृष्ठ देखें।

---

## रीसीड्स

### मेरा router कई मिनटों से चालू है और इसमें शून्य या बहुत कम कनेक्शन हैं {#reseed}

सबसे पहले Router Console में [http://127.0.0.1:7657/netdb](http://127.0.0.1:7657/netdb) पेज देखें – आपका network database। यदि आप I2P के भीतर से एक भी router सूचीबद्ध नहीं देखते हैं लेकिन console कहता है कि आप firewalled होना चाहिए, तो संभवतः आप reseed servers से कनेक्ट नहीं हो सकते। यदि आप अन्य I2P routers सूचीबद्ध देखते हैं तो [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config) में अधिकतम connections की संख्या कम करने का प्रयास करें, हो सकता है कि आपका router कई connections को संभाल नहीं सकता।

### मैं मैन्युअल रूप से रीसीड कैसे करूं? {#manual_reseed}

सामान्य परिस्थितियों में, I2P आपको हमारे bootstrap लिंक का उपयोग करके स्वचालित रूप से नेटवर्क से कनेक्ट कर देगा। यदि बाधित इंटरनेट reseed सर्वर से bootstrapping विफल कर देता है, तो bootstrap करने का एक आसान तरीका Tor ब्राउज़र का उपयोग करना है (डिफ़ॉल्ट रूप से यह localhost खोलता है), जो [http://127.0.0.1:7657/configreseed](http://127.0.0.1:7657/configreseed) के साथ बहुत अच्छी तरह से काम करता है। I2P router को मैन्युअल रूप से reseed करना भी संभव है।

Tor ब्राउज़र का उपयोग करके reseed करते समय आप एक साथ कई URLs चुन सकते हैं और आगे बढ़ सकते हैं। हालांकि डिफ़ॉल्ट मान जो 2 है (कई urls में से) वह भी काम करेगा लेकिन यह धीमा होगा।

---

## गोपनीयता-सुरक्षा

### क्या मेरा router एक "exit node"(outproxy) है जो नियमित इंटरनेट से जुड़ता है? मैं नहीं चाहता कि यह हो। {#exit}

नहीं, आपका router i2p network के माध्यम से encrypted e2e ट्रैफ़िक को एक यादृच्छिक tunnel endpoint तक पहुंचाने में भाग लेता है, जो आमतौर पर outproxy नहीं होता, लेकिन transport layer पर आपके router और इंटरनेट के बीच कोई ट्रैफ़िक पास नहीं होता है। एक अंतिम उपयोगकर्ता के रूप में, यदि आप सिस्टम और नेटवर्क प्रशासन में कुशल नहीं हैं तो आपको outproxy नहीं चलाना चाहिए।

### क्या नेटवर्क ट्रैफ़िक का विश्लेषण करके I2P के उपयोग का पता लगाना आसान है? {#detection}

I2P ट्रैफ़िक आमतौर पर UDP ट्रैफ़िक जैसा दिखता है, और इससे ज़्यादा कुछ नहीं - और इसे उससे ज़्यादा कुछ न दिखाना एक लक्ष्य है। यह TCP का भी समर्थन करता है। कुछ प्रयास के साथ, निष्क्रिय ट्रैफ़िक विश्लेषण (passive traffic analysis) इस ट्रैफ़िक को "I2P" के रूप में वर्गीकृत करने में सक्षम हो सकता है, लेकिन हमें उम्मीद है कि traffic obfuscation के निरंतर विकास से यह और कम हो जाएगा। यहां तक कि obfs4 जैसी एक काफी सरल protocol obfuscation परत भी सेंसर को I2P को ब्लॉक करने से रोकेगी (यह एक लक्ष्य है जिसे I2P तैनात करता है)।

### क्या I2P का उपयोग सुरक्षित है? {#safe}

यह आपके व्यक्तिगत खतरे के मॉडल पर निर्भर करता है। अधिकांश लोगों के लिए, I2P बिना किसी सुरक्षा के उपयोग की तुलना में बहुत सुरक्षित है। कुछ अन्य नेटवर्क (जैसे Tor, mixminion/mixmaster), संभवतः कुछ विशेष विरोधियों के खिलाफ अधिक सुरक्षित हैं। उदाहरण के लिए, I2P ट्रैफ़िक TLS/SSL का उपयोग नहीं करता है, इसलिए इसमें "सबसे कमजोर कड़ी" की समस्याएं नहीं हैं जो Tor में होती हैं। "अरब स्प्रिंग" के दौरान सीरिया में बहुत से लोगों ने I2P का उपयोग किया था, और हाल ही में परियोजना ने निकट और मध्य पूर्व में I2P की छोटी भाषाई स्थापनाओं में बड़ी वृद्धि देखी है। यहां ध्यान देने वाली सबसे महत्वपूर्ण बात यह है कि I2P एक तकनीक है और इंटरनेट पर आपकी गोपनीयता/गुमनामी बढ़ाने के लिए आपको एक how-to/गाइड की आवश्यकता है। साथ ही अपने ब्राउज़र की जांच करें या fingerprint हमलों को ब्लॉक करने के लिए fingerprint-search-engine को इम्पोर्ट करें जिसमें बहुत बड़े (अर्थात: विशिष्ट लंबी पूंछ / बहुत सटीक विविध डेटा संरचना) वातावरण संबंधी चीजों के बारे में डेटासेट हो और VPN का उपयोग न करें ताकि इससे आने वाले सभी जोखिमों को कम किया जा सके जैसे स्वयं का TLS cache व्यवहार और प्रदाता व्यवसाय की तकनीकी संरचना जिसे अपने डेस्कटॉप सिस्टम की तुलना में आसानी से हैक किया जा सकता है। सार्वजनिक नेटवर्क और शीर्ष व्यक्तिगत जोखिम मॉडल में एक isolated tor V-Browser का उपयोग इसके बेहतरीन anti-fingerprint सुरक्षा के साथ और केवल आवश्यक सिस्टम संचार की अनुमति के साथ एक समग्र appguard-livetime-protection और anti-spy disable scripts और live-cd के साथ अंतिम स्थायी vm-use का उपयोग किसी भी "लगभग स्थायी संभावित जोखिम" को हटाने और घटती संभावना द्वारा सभी जोखिमों को कम करने के लिए एक अच्छा विकल्प हो सकता है और i2p उपयोग के लिए इस लक्ष्य के साथ आप जो सबसे अच्छा कर सकते हैं वह यह हो सकता है।

### मैं router console में अन्य सभी I2P nodes के IP addresses देख सकता हूं। क्या इसका मतलब है कि मेरा IP address दूसरों को दिखाई दे रहा है? {#netdb_ip}

हां, अन्य I2P nodes के लिए जो आपके router के बारे में जानते हैं। हम इसका उपयोग शेष I2P नेटवर्क से कनेक्ट करने के लिए करते हैं। पते भौतिक रूप से "routerInfos (key,value) objects" में स्थित होते हैं, जो या तो दूरस्थ रूप से प्राप्त किए जाते हैं या peer से प्राप्त होते हैं। "routerInfos" में router के बारे में कुछ जानकारी (कुछ वैकल्पिक अवसरवादी जोड़ी गई) होती है, जो "peer द्वारा प्रकाशित" होती है, bootstrapping के लिए। इस object में clients के बारे में कोई डेटा नहीं है। हुड के नीचे करीब से देखने पर आपको पता चलेगा कि हर किसी की गिनती ids बनाने के नवीनतम प्रकार से की गई है जिसे "SHA-256 Hashes (low=Positive hash(-key), high=Negative hash(+key))" कहा जाता है। I2P नेटवर्क के पास upload और indexing के दौरान बनाए गए routerInfos का अपना database डेटा है, लेकिन यह key/value tables और नेटवर्क topology और state-of-load / state-of-bandwidth और DB components में storages के लिए routing संभावनाओं की प्राप्ति में गहराई से निर्भर करता है।

### क्या outproxy का उपयोग करना सुरक्षित है? {#proxy_safe}

यह इस बात पर निर्भर करता है कि "सुरक्षित" की आपकी परिभाषा क्या है। Outproxies बहुत अच्छे होते हैं जब वे काम करते हैं, लेकिन दुर्भाग्य से वे स्वेच्छा से उन लोगों द्वारा चलाए जाते हैं जो रुचि खो सकते हैं या जिनके पास उन्हें 24/7 बनाए रखने के लिए संसाधन नहीं हो सकते हैं – कृपया जागरूक रहें कि आप ऐसे समय का अनुभव कर सकते हैं जिसके दौरान सेवाएं अनुपलब्ध, बाधित या अविश्वसनीय हो सकती हैं, और हम इस सेवा से संबद्ध नहीं हैं और इस पर हमारा कोई प्रभाव नहीं है।

outproxy स्वयं आपके ट्रैफ़िक को आते-जाते देख सकते हैं, end-to-end एन्क्रिप्टेड HTTPS/SSL डेटा के अपवाद के साथ, ठीक उसी तरह जैसे आपका ISP आपके कंप्यूटर से आने-जाने वाले ट्रैफ़िक को देख सकता है। यदि आप अपने ISP के साथ सहज हैं, तो outproxy के साथ यह इससे बुरा नहीं होगा।

### "डी-एनोनिमाइज़िंग" हमलों के बारे में क्या? {#deanon}

बहुत विस्तृत व्याख्या के लिए, हमारे [Threat Model](/docs/overview/threat-model) के बारे में लेख पढ़ें। सामान्यतः, de-anonymizing तुच्छ नहीं है, लेकिन यदि आप पर्याप्त सावधान नहीं हैं तो संभव है।

---

## इंटरनेट एक्सेस/प्रदर्शन

### मैं I2P के माध्यम से सामान्य इंटरनेट साइटों तक नहीं पहुँच सकता। {#outproxy}

इंटरनेट साइटों के लिए प्रॉक्सी करना (eepsites जो इंटरनेट से बाहर हैं) गैर-ब्लॉक प्रदाताओं द्वारा I2P उपयोगकर्ताओं को एक सेवा के रूप में प्रदान की जाती है। यह सेवा I2P विकास का मुख्य फोकस नहीं है, और स्वैच्छिक आधार पर प्रदान की जाती है। I2P पर होस्ट की गई Eepsites को हमेशा बिना outproxy के काम करना चाहिए। Outproxies एक सुविधा हैं लेकिन वे डिज़ाइन के अनुसार न तो पूर्ण हैं और न ही परियोजना का एक बड़ा हिस्सा। जागरूक रहें कि वे I2P की अन्य सेवाओं द्वारा प्रदान की जाने वाली उच्च-गुणवत्ता सेवा प्रदान करने में सक्षम नहीं हो सकती हैं।

### मैं I2P के माध्यम से https:// या ftp:// साइटों तक नहीं पहुँच सकता। {#https}

डिफ़ॉल्ट HTTP प्रॉक्सी केवल HTTP और HTTPS outproxying का समर्थन करता है।

### मेरा router बहुत अधिक CPU का उपयोग क्यों कर रहा है? {#cpu}

सबसे पहले, सुनिश्चित करें कि आपके पास I2P से संबंधित हर भाग का नवीनतम संस्करण है – पुराने संस्करणों में कोड में अनावश्यक CPU-खपत करने वाले खंड थे। एक [performance Log](/docs/overview/performance) भी है जो समय के साथ I2P प्रदर्शन में हुए कुछ सुधारों को दस्तावेज़ित करता है।

### मेरे सक्रिय peers / ज्ञात peers / भाग लेने वाली tunnels / कनेक्शन / बैंडविड्थ समय के साथ नाटकीय रूप से बदलते रहते हैं! क्या कुछ गलत है? {#vary}

I2P नेटवर्क की सामान्य स्थिरता अनुसंधान का एक सतत क्षेत्र है। उस अनुसंधान का एक विशेष भाग इस बात पर केंद्रित है कि कॉन्फ़िगरेशन सेटिंग्स में छोटे बदलाव router के व्यवहार को कैसे बदलते हैं। चूंकि I2P एक peer-to-peer नेटवर्क है, अन्य peers द्वारा की गई कार्रवाइयों का आपके router के प्रदर्शन पर प्रभाव पड़ेगा।

### I2P पर डाउनलोड, torrents, वेब ब्राउज़िंग और अन्य सभी चीजें नियमित इंटरनेट की तुलना में धीमी क्यों होती हैं? {#slow}

I2P में विभिन्न सुरक्षा उपाय हैं जो अतिरिक्त routing और encryption की अतिरिक्त परतें जोड़ते हैं। यह अन्य peers (Tunnels) के माध्यम से ट्रैफ़िक को भी bounce करता है जिनकी अपनी गति और गुणवत्ता होती है, कुछ धीमे होते हैं, कुछ तेज़। इससे विभिन्न दिशाओं में अलग-अलग गति पर बहुत अधिक overhead और ट्रैफ़िक जुड़ जाता है। डिज़ाइन के अनुसार ये सभी चीजें इसे इंटरनेट पर सीधे कनेक्शन की तुलना में धीमा बना देंगी, लेकिन बहुत अधिक गुमनाम और फिर भी अधिकांश चीजों के लिए पर्याप्त तेज़।

नीचे एक उदाहरण दिया गया है जिसमें I2P का उपयोग करते समय विलंबता (latency) और बैंडविड्थ संबंधी विचारों को समझने में मदद के लिए स्पष्टीकरण प्रस्तुत किया गया है।

नीचे दिए गए चित्र पर विचार करें। यह I2P के माध्यम से अनुरोध करने वाले एक client, I2P के माध्यम से अनुरोध प्राप्त करने वाले एक server और फिर I2P के माध्यम से वापस प्रतिक्रिया देने के बीच संबंध को दर्शाता है। जिस circuit पर अनुरोध यात्रा करता है, उसे भी दर्शाया गया है।

आरेख से, मान लीजिए कि 'P', 'Q' और 'R' लेबल वाले बॉक्स 'A' के लिए एक outbound tunnel को दर्शाते हैं और 'X', 'Y' और 'Z' लेबल वाले बॉक्स 'B' के लिए एक outbound tunnel को दर्शाते हैं। इसी तरह, 'X', 'Y' और 'Z' लेबल वाले बॉक्स 'B' के लिए एक inbound tunnel को दर्शाते हैं जबकि 'P_1', 'Q_1' और 'R_1' लेबल वाले बॉक्स 'A' के लिए एक inbound tunnel को दर्शाते हैं। बॉक्स के बीच के तीर ट्रैफ़िक की दिशा दिखाते हैं। तीरों के ऊपर और नीचे का टेक्स्ट हॉप की एक जोड़ी के बीच कुछ उदाहरण बैंडविड्थ के साथ-साथ उदाहरण लेटेंसी का विवरण देता है।

जब client और server दोनों पूरे समय 3-hop tunnels का उपयोग कर रहे हों, तो कुल 12 अन्य I2P routers ट्रैफ़िक को relay करने में शामिल होते हैं। 6 peers, client से server तक ट्रैफ़िक को relay करते हैं जो 'A' से एक 3-hop outbound tunnel ('P', 'Q', 'R') और 'B' तक एक 3-hop inbound tunnel ('X', 'Y', 'Z') में विभाजित होता है। इसी तरह, 6 peers server से वापस client तक ट्रैफ़िक को relay करते हैं।

सबसे पहले, हम latency पर विचार कर सकते हैं - वह समय जो एक client के अनुरोध को I2P network को पार करने, server तक पहुंचने और वापस client तक आने में लगता है। सभी latencies को जोड़ने पर हम देखते हैं कि:

```
    40 + 100 + 20 + 60 + 80 + 10 + 30 ms        (client to server)
  + 60 + 40 + 80 + 60 + 100 + 20 + 40 ms        (server to client)
  -----------------------------------
  TOTAL:                          740 ms
```
हमारे उदाहरण में कुल round-trip time 740 ms तक जोड़ता है - निश्चित रूप से नियमित इंटरनेट वेबसाइटों को ब्राउज़ करते समय सामान्य रूप से देखे जाने वाले समय से बहुत अधिक।

दूसरा, हम उपलब्ध bandwidth पर विचार कर सकते हैं। यह client और server के बीच hops के बीच सबसे धीमी link के साथ-साथ जब server द्वारा client को traffic भेजा जा रहा हो, के माध्यम से निर्धारित होता है। client से server की ओर जाने वाले traffic के लिए, हम देखते हैं कि हमारे उदाहरण में hops 'R' और 'X' के साथ-साथ hops 'X' और 'Y' के बीच उपलब्ध bandwidth 32 KB/s है। अन्य hops के बीच अधिक उपलब्ध bandwidth के बावजूद, ये hops एक bottleneck के रूप में कार्य करेंगे और 'A' से 'B' तक traffic के लिए अधिकतम उपलब्ध bandwidth को 32 KB/s पर सीमित कर देंगे। इसी तरह, server से client तक के path को trace करने पर पता चलता है कि 64 KB/s की अधिकतम bandwidth है - hops 'Z_1' और 'Y_1', 'Y_1' और 'X_1' तथा 'Q_1' और 'P_1' के बीच।

हम आपकी bandwidth सीमाओं को बढ़ाने की अनुशंसा करते हैं। यह उपलब्ध bandwidth की मात्रा बढ़ाकर नेटवर्क में मदद करता है जो बदले में आपके I2P अनुभव को बेहतर बनाएगा। Bandwidth सेटिंग्स [http://localhost:7657/config](http://localhost:7657/config) पृष्ठ पर स्थित हैं। कृपया अपने ISP द्वारा निर्धारित अपने इंटरनेट कनेक्शन की सीमाओं के बारे में जागरूक रहें, और अपनी सेटिंग्स को तदनुसार समायोजित करें।

हम पर्याप्त मात्रा में shared bandwidth सेट करने की भी सिफारिश करते हैं - यह participating tunnels को आपके I2P router के माध्यम से route किए जाने की अनुमति देता है। participating traffic की अनुमति देने से आपका router नेटवर्क में अच्छी तरह से एकीकृत रहता है और आपकी transfer speeds में सुधार होता है।

I2P एक चल रहा काम है। बहुत सारे सुधार और फिक्सेस लागू किए जा रहे हैं, और सामान्य तौर पर, नवीनतम रिलीज़ चलाने से आपके प्रदर्शन में मदद मिलेगी। यदि आपने नहीं किया है, तो नवीनतम रिलीज़ इंस्टॉल करें।

### मुझे लगता है कि मुझे एक बग मिला है, मैं इसे कहाँ रिपोर्ट कर सकता हूँ? {#bug}

आप हमारे bugtracker पर किसी भी bug/issue की रिपोर्ट कर सकते हैं, जो non-private internet और I2P दोनों पर उपलब्ध है। हमारे पास एक discussion forum भी है, जो I2P और non-private internet दोनों पर उपलब्ध है। आप हमारे IRC channel से भी जुड़ सकते हैं: या तो हमारे IRC network, IRC2P के माध्यम से, या Freenode पर।

- **हमारा Bugtracker:**
  - Non-private internet: [https://i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)
  - I2P पर: [http://git.idk.i2p/I2P_Developers/i2p.i2p/issues](http://git.idk.i2p/I2P_Developers/i2p.i2p/issues)
- **हमारे फोरम:** [i2pforum.i2p](http://i2pforum.i2p/)
- **लॉग पेस्ट करें:** आप किसी भी महत्वपूर्ण लॉग को किसी पेस्ट सेवा में पेस्ट कर सकते हैं जैसे कि [PrivateBin Wiki](https://github.com/PrivateBin/PrivateBin/wiki/PrivateBin-Directory) पर सूचीबद्ध non-private internet सेवाएं, या I2P पेस्ट सेवा जैसे कि यह [PrivateBin instance](http://paste.crypthost.i2p) या यह [Javascript-free पेस्ट सेवा](http://pasta-nojs.i2p) और #i2p में IRC पर फॉलो अप करें
- **IRC:** #i2p-dev में शामिल हों - IRC पर डेवलपर्स के साथ चर्चा करें

कृपया router logs पेज से प्रासंगिक जानकारी शामिल करें जो यहाँ उपलब्ध है: [http://127.0.0.1:7657/logs](http://127.0.0.1:7657/logs)। हम अनुरोध करते हैं कि आप 'I2P Version and Running Environment' सेक्शन के अंतर्गत सभी टेक्स्ट के साथ-साथ पेज पर प्रदर्शित विभिन्न logs में दिखाई देने वाली किसी भी त्रुटि या चेतावनी को साझा करें।

---

### मेरा एक सवाल है! {#question}

बढ़िया! हमें IRC पर खोजें:

- `irc.freenode.net` पर चैनल `#i2p`
- `IRC2P` पर चैनल `#i2p`

या [फोरम](http://i2pforum.i2p/) पर पोस्ट करें और हम इसे यहाँ पोस्ट करेंगे (उम्मीद है कि उत्तर के साथ)।
