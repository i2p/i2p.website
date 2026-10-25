---
title: "प्लगइन विनिर्देश"
description: "I2P plugins के लिए .xpi2p / .su3 पैकेजिंग नियम"
slug: "plugin"
aliases:
  - "/hi/plugin_spec"
  - "/hi/plugin_spec/"
lastUpdated: "2022-01"
accurateFor: "0.9.53"
type: docs
---

## अवलोकन

यह दस्तावेज़ .xpi2p फ़ाइल फॉर्मेट को निर्दिष्ट करता है (Firefox .xpi की तरह), लेकिन XML install.rdf फ़ाइल के बजाय एक सरल plugin.config विवरण फ़ाइल के साथ। यह फ़ाइल फॉर्मेट प्रारंभिक plugin इंस्टॉल और plugin अपडेट दोनों के लिए उपयोग किया जाता है।

इसके अतिरिक्त, यह दस्तावेज़ इस बात का संक्षिप्त अवलोकन प्रदान करता है कि router प्लगइन्स को कैसे इंस्टॉल करता है, और प्लगइन डेवलपर्स के लिए नीतियां और दिशानिर्देश।

बेसिक .xpi2p फाइल फॉर्मेट i2pupdate.sud फाइल के समान है (जो router अपडेट के लिए उपयोग किया जाता है), लेकिन इंस्टॉलर उपयोगकर्ता को addon इंस्टॉल करने की अनुमति देगा भले ही उसे अभी तक signer की key ज्ञात न हो।

रिलीज़ 0.9.15 के अनुसार, SU3 फ़ाइल प्रारूप समर्थित है और इसे प्राथमिकता दी जाती है। यह प्रारूप मजबूत signing keys को सक्षम बनाता है।

> **नोट:** हम अब xpi2p फॉर्मेट में plugins वितरित करने की अनुशंसा नहीं करते हैं। su3 फॉर्मेट का उपयोग करें।

मानक निर्देशिका संरचना उपयोगकर्ताओं को निम्नलिखित प्रकार के addons स्थापित करने की अनुमति देगी:

- Console webapps
- cgi-bin, webapps के साथ नई eepsite
- Console themes
- Console अनुवाद
- Java प्रोग्राम
- अलग JVM में Java प्रोग्राम
- कोई भी shell script या प्रोग्राम

एक plugin अपनी सभी फाइलें `~/.i2p/plugins/name/` (`%APPDIR%\I2P\plugins\name\` Windows पर) में install करता है। installer किसी और जगह installation को रोक देगा, हालांकि plugin चलते समय अन्य जगहों पर libraries को access कर सकता है।

इसे केवल स्थापना, अनइंस्टालेशन और अपग्रेडिंग को आसान बनाने और बुनियादी inter-plugin संघर्षों को कम करने के एक तरीके के रूप में देखा जाना चाहिए।

हालांकि, plugin चलने के बाद अनिवार्य रूप से कोई सुरक्षा मॉडल नहीं होता है। plugin उसी JVM में और router के समान अनुमतियों के साथ चलता है, और इसकी फाइल सिस्टम, router, बाहरी प्रोग्राम चलाने आदि तक पूर्ण पहुंच होती है।

## विवरण

foo.xpi2p एक signed update (sud) फ़ाइल है जिसमें निम्नलिखित शामिल है:

zip फ़ाइल के आगे जोड़ा गया मानक .sud हेडर, जिसमें निम्नलिखित शामिल है:

```text
40-byte DSA signature
16-byte plugin version in UTF-8, padded with trailing zeroes if necessary
```
निम्नलिखित को शामिल करने वाली Zip फाइल:

### plugin.config फ़ाइल

यह फ़ाइल आवश्यक है। यह एक मानक I2P कॉन्फ़िगरेशन फ़ाइल है, जिसमें निम्नलिखित गुण हैं:

#### आवश्यक गुण

निम्नलिखित चार आवश्यक गुण हैं। अपडेट प्लगइन के लिए पहले तीन स्थापित प्लगइन के समान होने चाहिए।

-   **name** - इस डायरेक्टरी नाम में इंस्टॉल किया जाएगा। native plugins के लिए, आप अलग-अलग packages में अलग नाम चाह सकते हैं - उदाहरण के लिए foo-windows और foo-linux।
-   **key** - DSA public key 172 B64 chars के रूप में जो '=' के साथ समाप्त होती है। SU3 format के लिए छोड़ दें।
-   **signer** - yourname@mail.i2p की सिफारिश की जाती है
-   **version** - ऐसे format में होना चाहिए जिसे VersionComparator parse कर सके, जैसे 1.2.3-4। अधिकतम 16 bytes (sud version से मेल खाना चाहिए)। मान्य संख्या विभाजक हैं '.', '-', और '_'। यह update plugin के लिए installed plugin में मौजूद version से अधिक होना चाहिए।

#### डिस्प्ले गुण

यदि निम्नलिखित गुणों के मान मौजूद हैं तो वे router console में /configplugins पर प्रदर्शित होते हैं:

-   **date** - Java time - long int
-   **author** - `yourname@mail.i2p` अनुशंसित
-   **websiteURL** - `http://foo.i2p/`
-   **updateURL** - `http://foo.i2p/foo.xpi2p` - अपडेट चेकर इस URL पर bytes 41-56 की जांच करेगा यह निर्धारित करने के लिए कि क्या कोई नया संस्करण उपलब्ध है। 1.7.0 (0.9.53) के रूप में, URL में `$OS` और `$ARCH` variables का उपयोग करना संभव है। अनुशंसित नहीं। तब तक उपयोग न करें जब तक आपने पहले xpi2p प्रारूप में plugins वितरित नहीं किए हों।
-   **updateURL.su3** - `http://foo.i2p/foo.su3` - su3-format अपडेट फाइल का स्थान, 0.9.15 के रूप में। 1.7.0 (0.9.53) के रूप में, URL में `$OS` और `$ARCH` variables का उपयोग करना संभव है।
-   **description** - अंग्रेजी में
-   **description_xx** - भाषा xx के लिए
-   **license** - Plugin लाइसेंस
-   **disableStop=true** - डिफ़ॉल्ट false। यदि true है, तो स्टॉप बटन दिखाया नहीं जाएगा। इसका उपयोग तब करें जब कोई webapps और stopargs वाले कोई clients न हों।

#### कंसोल सारांश बार लिंक गुण

निम्नलिखित properties का उपयोग console summary bar पर एक link जोड़ने के लिए किया जाता है:

-   **consoleLinkName** - summary bar में जोड़ा जाएगा
-   **consoleLinkName_xx** - भाषा xx के लिए
-   **consoleLinkURL** - /appname/index.jsp
-   **consoleLinkTooltip** - 0.7.12-6 से समर्थित
-   **consoleLinkTooltip_xx** - भाषा xx 0.7.12-6 से

#### कंसोल आइकन गुण

कंसोल पर एक कस्टम आइकन जोड़ने के लिए निम्नलिखित वैकल्पिक गुणों का उपयोग किया जा सकता है:

-   **console-icon** - 0.9.20 से समर्थित। केवल webapps के लिए। एक 32x32 image का path, जैसे /icon.png। 1.7.0 (API 0.9.53) से, यदि consoleLinkURL निर्दिष्ट है, तो path उस URL के सापेक्ष है। अन्यथा यह webapp name के सापेक्ष है। plugin में सभी webapps पर लागू होता है।
-   **icon-code** - 0.9.25 से समर्थित। web resources के बिना plugins के लिए console icon प्रदान करता है। एक B64 string जो 32x32 png image file पर `net.i2p.data.Base64 encode FILE` कॉल करने से बनता है।

#### इंस्टॉलर गुण

निम्नलिखित प्रॉपर्टीज़ plugin installer द्वारा उपयोग की जाती हैं:

-   **type** - app/theme/locale/webapp/... (अनुप्रयुक्त नहीं, शायद आवश्यक नहीं)
-   **min-i2p-version** - I2P का न्यूनतम संस्करण जिसकी इस plugin को आवश्यकता है
-   **max-i2p-version** - I2P का अधिकतम संस्करण जिस पर यह plugin चलेगा
-   **min-java-version** - Java का न्यूनतम संस्करण जिसकी इस plugin को आवश्यकता है
-   **min-jetty-version** - 0.8.13 से समर्थित, Jetty 6 webapps के लिए 6 का उपयोग करें
-   **max-jetty-version** - 0.8.13 से समर्थित, Jetty 5 webapps के लिए 5.99999 का उपयोग करें
-   **required-platform-OS** - अनुप्रयुक्त नहीं - संभवतः केवल प्रदर्शित किया जाएगा, सत्यापित नहीं
-   **other-requirements** - अनुप्रयुक्त नहीं, जैसे python x.y - installer द्वारा सत्यापित नहीं, केवल उपयोगकर्ता को प्रदर्शित
-   **dont-start-at-install=true** - डिफ़ॉल्ट false। plugin को install या update करने पर start नहीं करेगा।
-   **router-restart-required=true** - डिफ़ॉल्ट false। यह update पर router या plugin को restart नहीं करता, यह केवल उपयोगकर्ता को सूचित करता है कि restart आवश्यक है।
-   **update-only=true** - डिफ़ॉल्ट false। यदि true है, तो installation मौजूद न होने पर fail हो जाएगा।
-   **install-only=true** - डिफ़ॉल्ट false। यदि true है, तो installation मौजूद होने पर fail हो जाएगा।
-   **min-installed-version** - update के लिए, यदि installation मौजूद है
-   **max-installed-version** - update के लिए, यदि installation मौजूद है
-   **depends=plugin1,plugin2,plugin3** - अनुप्रयुक्त नहीं
-   **depends-version=0.3.4,,5.6.7** - अनुप्रयुक्त नहीं

#### अनुवाद गुण

-   **langs=xx,yy,Klingon,...** - (अनुपलब्ध) (yy देश का झंडा है)

### एप्लिकेशन निर्देशिकाएं और फाइलें

निम्नलिखित में से प्रत्येक निर्देशिका या फाइल वैकल्पिक है, लेकिन कुछ न कुछ वहाँ होना चाहिए अन्यथा यह कुछ भी काम नहीं करेगा:

**console/**

-   **locale/** - केवल वे jars जिनमें base I2P installation में apps के लिए नए resource bundles (अनुवाद) हों। इस plugin के लिए bundles को console/webapp/foo.war या lib/foo.jar के अंदर जाना चाहिए
-   **themes/** - router console के लिए नए themes। प्रत्येक theme को एक subdirectory में रखें।
-   **webapps/** - (webapps के बारे में नीचे दिए गए महत्वपूर्ण नोट्स देखें) .wars - ये install time पर चलाए जाएंगे जब तक webapps.config में disabled न हों। war name का plugin name के समान होना आवश्यक नहीं है। base I2P installation में war names को duplicate न करें।
-   **webapps.config** - router के webapps.config के समान format। webapp classpath के लिए $PLUGIN/lib/ या $I2P/lib में additional jars specify करने के लिए भी उपयोग किया जाता है, `webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar` के साथ

> **नोट:** रिलीज़ 1.7.0 (API 0.9.53) से पहले, classpath लाइन केवल तभी लोड होती थी जब warname प्लगइन के नाम के समान होता था। API 0.9.53 के बाद से, classpath सेटिंग किसी भी warname के लिए काम करेगी।

> **नोट:** router संस्करण 0.7.12-9 से पहले, router `webapps.warname.startOnLoad` के बजाय `plugin.warname.startOnLoad` की तलाश करता था। पुराने router संस्करणों के साथ संगतता के लिए, एक war को निष्क्रिय करने की इच्छा रखने वाले plugin में दोनों लाइनें शामिल होनी चाहिए।

**eepsite/**

(eepsites के बारे में नीचे दिए गए महत्वपूर्ण नोट्स देखें)

-   **cgi-bin/**
-   **docroot/**
-   **logs/**
-   **webapps/**
-   **jetty.xml** - इंस्टॉलर को यहाँ पाथ सेट करने के लिए वेरिएबल प्रतिस्थापन करना होगा। इस फाइल की स्थिति और नाम वास्तव में मायने नहीं रखते, जब तक यह clients.config में सेट है - यह यहाँ से एक स्तर ऊपर होना अधिक सुविधाजनक हो सकता है।

**lib/**

यहाँ कोई भी jars रखें, और उन्हें console/webapps.config और/या clients.config में classpath line में निर्दिष्ट करें

### clients.config फ़ाइल

यह फ़ाइल वैकल्पिक है, और उन clients को निर्दिष्ट करती है जो plugin शुरू होने पर चलाए जाएंगे। यह router की clients.config फ़ाइल के समान format का उपयोग करती है। format के बारे में अधिक जानकारी और clients कैसे शुरू और बंद किए जाते हैं के महत्वपूर्ण विवरणों के लिए clients.config configuration file specification देखें।

-   **clientApp.0.stopargs=foo bar stop baz** - यदि उपस्थित है, तो class को client को रोकने के लिए इन args के साथ कॉल किया जाएगा। सभी stop tasks को शून्य देरी के साथ कॉल किया जाता है। नोट: router यह नहीं बता सकता कि आपके unmanaged clients चल रहे हैं या नहीं।
-   **clientApp.0.uninstallargs=foo bar uninstall baz** - यदि उपस्थित है, तो $PLUGIN को हटाने से ठीक पहले class को इन args के साथ कॉल किया जाएगा। सभी uninstall tasks को शून्य देरी के साथ कॉल किया जाता है।
-   **clientApp.0.classpath=$I2P/lib/foo.bar,$PLUGIN/lib/bar.jar** - plugin runner निम्नलिखित तरीके से args और stopargs लाइनों में variable substitution करेगा:
    -   `$I2P` - I2P बेस इंस्टॉलेशन directory
    -   `$CONFIG` - I2P config directory (आमतौर पर ~/.i2p)
    -   `$PLUGIN` - इस plugin की इंस्टॉलेशन directory (आमतौर पर ~/.i2p/plugins/appname)
    -   `$OS` - host operating system `windows`, `linux`, `mac` के रूप में
    -   `$ARCH` - host architecture `386`, `amd64`, `arm64` के रूप में

(shell scripts या बाहरी programs चलाने के बारे में नीचे दिए गए महत्वपूर्ण नोट्स देखें)

## Plugin Installer कार्य

यह सूची बताती है कि जब I2P द्वारा कोई plugin इंस्टॉल किया जाता है तो क्या होता है।

1.  .xpi2p फ़ाइल डाउनलोड की जाती है।
2.  .sud signature को stored keys के विरुद्ध verify किया जाता है। release 0.9.14.1 के अनुसार, यदि कोई matching key नहीं है, तो installation fail हो जाती है, जब तक कि सभी keys को allow करने के लिए एक advanced router property set न की गई हो।
3.  zip फ़ाइल की integrity को verify करें।
4.  plugin.config फ़ाइल को extract करें।
5.  I2P version को verify करें, यह सुनिश्चित करने के लिए कि plugin काम करेगा।
6.  यह जांचें कि webapps मौजूदा $I2P applications को duplicate न करें।
7.  मौजूदा plugin को stop करें (यदि उपस्थित है)।
8.  Verify करें कि install directory अभी तक exist नहीं करती है यदि update=false है, या overwrite करने के लिए पूछें।
9.  Verify करें कि install directory exist करती है यदि update=true है, या create करने के लिए पूछें।
10. Plugin को appDir/plugins/name/ में unzip करें
11. Plugin को plugins.config में add करें

## प्लगइन स्टार्टर कार्य

यह सूची दिखाता है कि plugins शुरू होने पर क्या होता है। पहले, plugins.config की जांच की जाती है यह देखने के लिए कि कौन से plugins को शुरू करने की आवश्यकता है। प्रत्येक plugin के लिए:

1.  clients.config की जांच करें, और प्रत्येक आइटम को लोड और स्टार्ट करें (कॉन्फ़िगर किए गए jars को classpath में जोड़ें)।
2.  console/webapp और console/webapp.config की जांच करें। आवश्यक आइटमों को लोड और स्टार्ट करें (कॉन्फ़िगर किए गए jars को classpath में जोड़ें)।
3.  console/locale/foo.jar को translation classpath में जोड़ें यदि मौजूद हो।
4.  console/theme को theme search path में जोड़ें यदि मौजूद हो।
5.  summary bar link जोड़ें।

## Console Webapp नोट्स

Console webapps जिनमें background tasks होते हैं, उन्हें ServletContextListener को implement करना चाहिए (उदाहरण के लिए seedless या i2pbote देखें), या servlet में destroy() को override करना चाहिए, ताकि वे बंद हो सकें। Router version 0.7.12-3 के बाद से, console webapps को हमेशा restart से पहले बंद किया जाएगा, इसलिए आपको multiple instances की चिंता करने की जरूरत नहीं है, बशर्ते कि आप यह करें। Router version 0.7.12-3 के बाद से, console webapps को router shutdown के समय भी बंद कर दिया जाएगा।

webapp में library jars को bundle न करें; उन्हें lib/ में रखें और webapps.config में एक classpath डालें। फिर आप अलग install और update plugins बना सकते हैं, जहाँ update plugin में library jars नहीं होंगे।

अपने plugin में कभी भी Jetty, Tomcat, या servlet jars को bundle न करें, क्योंकि ये I2P installation में मौजूद version के साथ conflict कर सकते हैं। किसी भी conflicting libraries को bundle न करने का ध्यान रखें।

.java या .jsp फाइलों को शामिल न करें; अन्यथा Jetty उन्हें इंस्टॉलेशन के समय पुनः compile करेगा, जिससे startup का समय बढ़ जाएगा। जबकि अधिकतर I2P installations में classpath में एक working Java और JSP compiler होगा, इसकी गारंटी नहीं है, और यह सभी cases में काम नहीं कर सकता।

फिलहाल, $PLUGIN में classpath फाइलें जोड़ने वाले webapp का नाम plugin के समान होना चाहिए। उदाहरण के लिए, plugin foo में webapp का नाम foo.war होना चाहिए।

जबकि I2P ने I2P रिलीज़ 0.9.30 से Servlet 3.0 का समर्थन किया है, यह @WebContent के लिए annotation scanning का समर्थन नहीं करता (कोई web.xml फ़ाइल नहीं)। कई अतिरिक्त runtime jars की आवश्यकता होगी, और हम उन्हें मानक इंस्टॉलेशन में प्रदान नहीं करते हैं। यदि आपको @WebContent के समर्थन की आवश्यकता है तो I2P डेवलपर्स से संपर्क करें।

## Eepsite नोट्स

यह स्पष्ट नहीं है कि किसी मौजूदा eepsite में plugin कैसे install करें। router का eepsite से कोई संबंध नहीं है, और यह चल भी रहा हो या न हो, और एक से अधिक भी हो सकते हैं। बेहतर यह है कि एक बिल्कुल नई eepsite के लिए अपना Jetty instance और I2PTunnel instance शुरू करें।

यह एक नया I2PTunnel इंस्टेंशिएट कर सकता है (कुछ हद तक i2ptunnel CLI की तरह), लेकिन यह i2ptunnel gui में दिखाई नहीं देगा क्योंकि वह एक अलग इंस्टेंस है। लेकिन यह ठीक है। फिर आप i2ptunnel और jetty को एक साथ शुरू और बंद कर सकते हैं।

इसलिए router पर भरोसा न करें कि वह इसे किसी मौजूदा eepsite के साथ अपने आप merge कर देगा। शायद ऐसा नहीं होगा। clients.config से एक नया I2PTunnel और Jetty शुरू करें। इसके सबसे अच्छे उदाहरण zzzot और pebble plugins हैं।

jetty.xml में path substitution कैसे करें? उदाहरण के लिए zzzot और pebble plugins देखें।

## क्लाइंट स्टार्ट/स्टॉप नोट्स

रिलीज 0.9.4 के अनुसार, router "managed" plugin clients का समर्थन करता है। Managed plugin clients को `ClientAppManager` द्वारा instantiate और start किया जाता है। ClientAppManager client का reference बनाए रखता है और client की state पर updates प्राप्त करता है। Managed plugin clients को प्राथमिकता दी जाती है, क्योंकि state tracking को implement करना और client को start और stop करना बहुत आसान होता है। यह client code में static references से बचना भी बहुत आसान बनाता है जो client के stop होने के बाद अत्यधिक memory usage का कारण बन सकते हैं। Managed client लिखने के बारे में अधिक जानकारी के लिए clients.config configuration file specification देखें।

"अप्रबंधित" plugin क्लाइंट्स के लिए, router के पास clients.config के माध्यम से शुरू किए गए क्लाइंट्स की स्थिति की निगरानी करने का कोई तरीका नहीं है। Plugin लेखक को यदि संभव हो तो static state table रखकर या PID files का उपयोग करके, कई start या stop कॉल्स को सुचारू रूप से handle करना चाहिए। कई starts या stops पर logging या exceptions से बचें। यह बिना पिछली start के stop कॉल के लिए भी लागू होता है। router version 0.7.12-3 के अनुसार, plugins को router shutdown पर बंद कर दिया जाएगा, जिसका मतलब है कि clients.config में stopargs वाले सभी क्लाइंट्स को कॉल किया जाएगा, चाहे वे पहले start हुए हों या न हों।

## Shell Script और बाहरी प्रोग्राम नोट्स

shell scripts या अन्य external programs चलाने के लिए, एक छोटी Java class लिखें जो OS type को check करे, फिर आपके द्वारा प्रदान की गई .bat या .sh file पर ShellCommand चलाए। इसके लिए एक सामान्यीकृत समाधान I2P 1.7.0/0.9.53 में जोड़ा गया था, "ShellService" जो एक single command के लिए state tracking करता है और ClientAppManager के साथ communicate करता है।

बाहरी प्रोग्राम router के रुकने पर नहीं रुकेंगे, और router के शुरू होने पर दूसरी कॉपी चल जाएगी। आमतौर पर इसे ShellService का उपयोग करके state tracking के लिए कम किया जा सकता है। यदि यह आपके उपयोग के मामले के लिए उपयुक्त नहीं है, तो आप एक wrapper class या shell script लिख सकते हैं जो PID file में PID का सामान्य storage करे, और शुरुआत पर इसकी जांच करे।

## अन्य प्लगइन दिशानिर्देश

-   Key generation, plugin su3 file creation, और verification के अधिकांश कार्यों को automate करने वाली makeplugin.sh shell script के लिए i2p.scripts monotone branch या zzz के page पर किसी भी sample plugin को देखें। आपको इस script को अपनी plugin build process में शामिल करना चाहिए।
-   Plugins के लिए jars और wars का Pack200 दृढ़ता से अनुशंसित है, यह आमतौर पर plugins को 60-65% तक संकुचित करता है। उदाहरण के लिए zzz के page पर किसी भी sample plugin को देखें। Pack200 unpacking, routers 0.7.11-5 या उससे ऊपर के versions पर समर्थित है, जो मूल रूप से सभी routers हैं जो plugins का समर्थन करते हैं।
-   Plugins को $I2P में कहीं भी write करने का प्रयास नहीं करना चाहिए क्योंकि यह readonly हो सकता है, और वैसे भी यह अच्छी नीति नहीं है।
-   Plugins $CONFIG में write कर सकते हैं लेकिन files को केवल $PLUGIN में रखना अनुशंसित है। $PLUGIN में सभी files uninstall के समय delete हो जाएंगी।
-   $CWD कहीं भी हो सकता है; यह मान न लें कि यह किसी विशेष स्थान पर है, $CWD के relative में files को read या write करने का प्रयास न करें। ShellService के लिए, यह हमेशा $PLUGIN के समान होता है।
-   Java programs को I2PAppContext में directory getters के साथ यह पता करना चाहिए कि वे कहाँ हैं।
-   Plugin directory `I2PAppContext.getGlobalContext().getAppDir().getAbsolutePath() + "/plugins/" + appname` है, या clients.config में args line में $PLUGIN argument डालें।
-   सभी config files UTF-8 में होनी चाहिए।
-   Separate JVM में run करने के लिए, `java -cp foo:bar:baz my.main.class arg1 arg2 arg3` के साथ ShellCommand का उपयोग करें।
-   clients.config में stopargs के विकल्प के रूप में, एक Java client `I2PAppContext.addShutdownTask()` के साथ shutdown hook register कर सकता है। लेकिन यह upgrade के समय plugin को shut down नहीं करेगा, इसलिए stopargs अनुशंसित है। साथ ही, सभी created threads को daemon mode पर set करें।
-   Standard installation में मौजूद classes की duplicate करने वाली classes शामिल न करें। यदि आवश्यक हो तो classes को extend करें।
-   Old और new installations के बीच wrapper.config में अलग classpath definitions से सावधान रहें।
-   Clients अलग keynames के साथ duplicate keys, अलग keys के साथ duplicate keynames, और upgrade packages में अलग keys या keynames को reject कर देंगे। अपनी keys की सुरक्षा करें। उन्हें केवल एक बार generate करें।
-   Runtime पर plugin.config file को modify न करें क्योंकि यह upgrade पर overwrite हो जाएगी। Runtime configuration store करने के लिए directory में एक अलग config file का उपयोग करें।
-   सामान्यतः, plugins को $I2P/lib/router.jar तक पहुँच की आवश्यकता नहीं होनी चाहिए। router classes तक पहुँच न बनाएं, जब तक कि आप कुछ विशेष न कर रहे हों।
-   चूंकि प्रत्येक version पहले वाले से अधिक होना चाहिए, आप अपनी build script को enhance कर सकते हैं ताकि version के अंत में build number जोड़ा जा सके।
-   Plugins को कभी भी `System.exit()` call नहीं करना चाहिए।
-   कृपया आपके द्वारा bundle किए जाने वाले किसी भी software के license requirements को पूरा करके licenses का सम्मान करें।
-   Router, JVM time zone को UTC पर set करता है। यदि किसी plugin को user का actual time zone जानने की आवश्यकता है, तो यह router द्वारा I2PAppContext property `i2p.systemTimeZone` में stored होता है।

## Classpaths

$I2P/lib में निम्नलिखित jars को सभी I2P installations के लिए standard classpath में मौजूद माना जा सकता है, चाहे मूल installation कितना भी पुराना या नया हो।

i2p jars में सभी हाल की public APIs में Javadocs में since-release संख्या निर्दिष्ट है। यदि आपके plugin को कुछ विशेषताओं की आवश्यकता है जो केवल हाल के versions में उपलब्ध हैं, तो plugin.config file में min-i2p-version, min-jetty-version, या दोनों properties को सेट करना सुनिश्चित करें।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">addressbook.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription and blockfile support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need; use the NamingService interface</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-logging.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Apache Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since release 0.9.30</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-el.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSP Expressions Language</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with JSPs that use EL. As of release 0.9.30 (Jetty 9), this contains the EL 3.0 API.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with HTTP or other servers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-compiler.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">nothing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since Jetty 6 (release 0.9)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-runtime.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper Compiler and Runtime, and some Tomcat utils</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">javax.servlet.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs. As of release 0.9.30 (Jetty 9), this contains the Servlet 3.1 and JSP 2.3 APIs.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jbigi.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Binaries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jetty-i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Support utilities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Some plugins will need. As of release 0.9.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">mstreaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">org.mortbay.jetty.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty Base</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins starting their own Jetty instance will need. Recommended way of starting Jetty is with <code>net.i2p.jetty.JettyStart</code> in jetty-i2p.jar.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins using router context will need; most will not</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">routerconsole.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need, not a public API</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">sam.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">streaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming Implementation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">URL Launcher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins should not need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray4j.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Systray</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need. As of 0.9.26, no longer present.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">wrapper.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
  </tbody>
</table>
$I2P/lib में निम्नलिखित jars सभी I2P installations के लिए उपस्थित होने मान सकते हैं, चाहे मूल installation कितना भी पुराना या नया हो, लेकिन ये जरूरी नहीं कि classpath में हों:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jstl.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">standard.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
  </tbody>
</table>
ऊपर सूचीबद्ध नहीं की गई कोई भी चीज़ हर किसी के classpath में मौजूद नहीं हो सकती है, भले ही आपके पास यह आपके i2p के संस्करण में classpath में हो। यदि आपको ऊपर सूचीबद्ध नहीं किए गए किसी jar की आवश्यकता है, तो अपने plugin में clients.config या webapps.config में निर्दिष्ट classpath में $I2P/lib/foo.jar जोड़ें।

पहले, clients.config में निर्दिष्ट एक classpath entry पूरे JVM के लिए classpath में जोड़ी जाती थी। हालांकि, 0.7.13-3 के बाद से, इसे class loaders का उपयोग करके ठीक किया गया है, और अब, जैसा कि मूल रूप से इरादा था, clients.config में निर्दिष्ट classpath केवल विशिष्ट thread के लिए है। इसलिए, प्रत्येक client के लिए पूर्ण आवश्यक classpath निर्दिष्ट करें।

## Java संस्करण नोट्स

I2P को रिलीज़ 0.9.24 (जनवरी 2016) से Java 7 की आवश्यकता है। I2P को रिलीज़ 0.9.12 (अप्रैल 2014) से Java 6 की आवश्यकता है। नवीनतम रिलीज़ पर कोई भी I2P उपयोगकर्ता को 1.7 (7.0) JVM चलाना चाहिए।

यदि आपके plugin **के लिए 1.7 की आवश्यकता नहीं है**:

-   सुनिश्चित करें कि सभी java और jsp फाइलें source="1.6" target="1.6" के साथ संकलित हों।
-   सुनिश्चित करें कि सभी bundled library jars भी 1.6 या उससे कम के लिए हों।

यदि आपका plugin **1.7 की आवश्यकता है**:

-   अपने डाउनलोड पेज पर ध्यान दें।
-   अपने plugin.config में min-java-version=1.7 जोड़ें

किसी भी स्थिति में, Java 8 के साथ compile करते समय runtime crashes को रोकने के लिए आपको **अवश्य** एक bootclasspath सेट करना चाहिए।

## अपडेट करते समय JVM क्रैश हो जाता है

नोट - यह सब अब ठीक हो जाना चाहिए।

JVM में यह प्रवृत्ति होती है कि यदि कोई plugin I2P शुरू होने के बाद से चल रहा था (भले ही वह plugin बाद में बंद कर दिया गया हो), तो उस plugin में jars को अपडेट करते समय JVM क्रैश हो जाता है। यह संभावित रूप से 0.7.13-3 में class loader implementation के साथ ठीक हो गया है, लेकिन यह भी हो सकता है कि न हुआ हो।

सबसे सुरक्षित तरीका यह है कि आप अपने plugin को war के अंदर jar के साथ डिज़ाइन करें (एक webapp के लिए), या update के बाद restart की आवश्यकता रखें, या अपने plugin में jars को update न करें।

webapp के अंदर class loader के काम करने के तरीके के कारण, यदि आप webapps.config में classpath specify करते हैं तो external jar होना _संभवतः_ सुरक्षित हो सकता है। इसे verify करने के लिए और अधिक testing की आवश्यकता है। यदि यह केवल webapp के लिए आवश्यक है तो clients.config में 'fake' client के साथ classpath specify न करें - इसके बजाय webapps.config का उपयोग करें।

सबसे कम सुरक्षित, और स्पष्ट रूप से अधिकांश crashes का स्रोत, वे clients हैं जिनके पास clients.config में classpath में निर्दिष्ट plugin jars हैं।

प्रारंभिक इंस्टॉल पर इनमें से कोई भी समस्या नहीं होनी चाहिए - plugin के प्रारंभिक इंस्टॉल के लिए आपको कभी भी restart की आवश्यकता नहीं होनी चाहिए।

## संदर्भ

-   [कॉन्फ़िगरेशन फाइल स्पेसिफिकेशन](/docs/specs/configuration)
-   [DSA क्रिप्टोग्राफी](/docs/specs/cryptography#DSA)
-   [अपडेट्स स्पेसिफिकेशन](/docs/specs/updates)
