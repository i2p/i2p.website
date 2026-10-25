---
title: "नामकरण और पता पुस्तिका"
description: "I2P कैसे मानव-पठनीय hostnames को destinations में मैप करता है"
slug: "naming"
aliases:
  - "/hi/docs/specs/naming"
  - "/hi/docs/specs/naming/"
  - "/hi/docs/naming"
  - "/hi/docs/naming/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## अवलोकन

I2P एक सामान्य naming library और एक base implementation के साथ आता है जो स्थानीय नाम से destination mapping के लिए डिज़ाइन किया गया है, साथ ही एक add-on application भी है जिसे [address book](#address-book) कहते हैं। I2P [Base32 hostnames](#base32-names) का भी समर्थन करता है जो Tor के .onion addresses के समान हैं।

Address book एक web-of-trust संचालित सुरक्षित, वितरित, और मानव-पठनीय नामकरण प्रणाली है, जो केवल स्थानीय विशिष्टता को अनिवार्य बनाकर सभी मानव-पठनीय नामों के वैश्विक रूप से अद्वितीय होने की आवश्यकता का त्याग करती है। जबकि I2P में सभी संदेश उनके destination द्वारा क्रिप्टोग्राफिक रूप से पता किए जाते हैं, अलग-अलग लोगों के पास "Alice" के लिए स्थानीय address book entries हो सकती हैं जो अलग-अलग destinations को संदर्भित करती हैं। लोग अभी भी अपने web of trust में निर्दिष्ट peers की प्रकाशित address books को import करके, किसी तृतीय पक्ष द्वारा प्रदान की गई entries को जोड़कर, या (यदि कुछ लोग first come first serve registration system का उपयोग करके प्रकाशित address books की एक श्रृंखला व्यवस्थित करते हैं) लोग इन address books को name servers के रूप में मानना चुन सकते हैं, पारंपरिक DNS का अनुकरण करते हुए, नए नामों की खोज कर सकते हैं।

नोट: I2P नामकरण प्रणाली के पीछे के तर्क, इसके विरुद्ध सामान्य तर्क और संभावित विकल्पों के लिए [naming discussion](/docs/legacy/naming/) पृष्ठ देखें।

---

## नेमिंग सिस्टम घटक

I2P में कोई केंद्रीय naming authority नहीं है। सभी hostnames स्थानीय हैं।

नेमिंग सिस्टम काफी सरल है और इसका अधिकांश भाग router के बाहरी एप्लिकेशन में लागू किया गया है, लेकिन I2P डिस्ट्रिब्यूशन के साथ बंडल किया गया है। घटक हैं:

1. स्थानीय [naming service](#naming-services) जो lookups करती है और [Base32 hostnames](#base32-names) को भी handle करती है।
2. [HTTP proxy](#http-proxy) जो router से lookups के लिए पूछती है और असफल lookups में सहायता के लिए उपयोगकर्ता को remote jump services की ओर इशारा करती है।
3. HTTP [host-add forms](#host-add-services) जो उपयोगकर्ताओं को अपनी स्थानीय hosts.txt में hosts जोड़ने की अनुमति देते हैं।
4. HTTP [jump services](#jump-services) जो अपनी lookups और redirection प्रदान करती हैं।
5. [Address book](#address-book) एप्लिकेशन जो HTTP के माध्यम से प्राप्त बाहरी host lists को स्थानीय list के साथ merge करती है।
6. [SusiDNS](#susidns) एप्लिकेशन जो address book कॉन्फ़िगरेशन और स्थानीय host lists को देखने के लिए एक सरल web front-end है।

---

## नेमिंग सर्विसेज

I2P में सभी destinations 516-byte (या अधिक लंबी) keys होती हैं। (अधिक सटीक रूप से कहें तो, यह एक 256-byte public key प्लस एक 128-byte signing key प्लस एक 3-या-अधिक byte certificate है, जो Base64 representation में 516 या अधिक bytes की होती है। Non-null [Certificates](/docs/legacy/naming/#certificates) अब signature type indication के लिए उपयोग में हैं। इसलिए, हाल ही में generated destinations में certificates 3 bytes से अधिक होते हैं।

यदि कोई application (i2ptunnel या HTTP proxy) किसी destination को नाम से access करना चाहती है, तो router उस नाम को resolve करने के लिए एक बहुत ही सरल local lookup करता है।

### Hosts.txt नामकरण सेवा

hosts.txt Naming Service टेक्स्ट फाइलों के माध्यम से एक सरल रैखिक खोज करता है। यह naming service 0.8.8 रिलीज़ तक डिफ़ॉल्ट था जब इसे Blockfile Naming Service से बदल दिया गया। hosts.txt प्रारूप हजारों entries तक फाइल बढ़ने के बाद बहुत धीमा हो गया था।

यह तीन स्थानीय फाइलों में क्रमानुसार एक रैखिक खोज करता है, होस्ट नामों को देखने और उन्हें 516-बाइट गंतव्य कुंजी में परिवर्तित करने के लिए। प्रत्येक फाइल एक सरल [कॉन्फ़िगरेशन फाइल प्रारूप](/docs/specs/configuration/) में है, जिसमें hostname=base64 होता है, प्रति पंक्ति एक। फाइलें हैं:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile नामकरण सेवा

Blockfile Naming Service एक डेटाबेस फाइल hostsdb.blockfile में कई "address books" स्टोर करता है। यह Naming Service रिलीज 0.8.8 के बाद से डिफ़ॉल्ट है।

एक blockfile केवल मल्टिपल sorted maps (key-value pairs) का on-disk storage है, जो skiplists के रूप में implemented है। blockfile format को [Blockfile page](/docs/specs/blockfile/) पर निर्दिष्ट किया गया है। यह compact format में fast Destination lookup प्रदान करता है। जबकि blockfile overhead काफी होता है, destinations को hosts.txt format में Base 64 के बजाय binary में store किया जाता है। इसके अतिरिक्त, blockfile प्रत्येक entry के लिए arbitrary metadata storage (जैसे added date, source, और comments) की सुविधा प्रदान करता है ताकि advanced address book features को implement किया जा सके। blockfile storage requirement hosts.txt format की तुलना में मामूली वृद्धि है, और blockfile lookup times में लगभग 10x की कमी प्रदान करता है।

निर्माण पर, naming service उन तीन फाइलों से entries import करती है जो hosts.txt Naming Service द्वारा उपयोग की जाती हैं। blockfile पिछले implementation की नकल करते हुए तीन maps को maintain करती है जिन्हें क्रम में खोजा जाता है, जिनका नाम privatehosts.txt, userhosts.txt, और hosts.txt है। यह तेज़ reverse lookups को implement करने के लिए एक reverse-lookup map भी maintain करती है।

### अन्य नामकरण सेवा सुविधाएं

lookup केस-इंसेंसिटिव है। पहला मैच उपयोग किया जाता है, और conflicts का पता नहीं लगाया जाता। lookups में नामकरण नियमों की कोई enforcement नहीं है। Lookups कुछ मिनटों के लिए cached रहते हैं। Base 32 resolution [नीचे वर्णित है](#base32-names)। Naming Service API का पूरा विवरण [Naming Service Javadocs](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html) में देखें। यह API रिलीज़ 0.8.7 में काफी विस्तृत किया गया था ताकि adds और removes, hostname के साथ मनमाने properties का storage, और अन्य सुविधाएं प्रदान की जा सकें।

### वैकल्पिक और प्रयोगात्मक नामकरण सेवाएं

नामकरण सेवा को कॉन्फ़िगरेशन प्रॉपर्टी `i2p.naming.impl=class` के साथ निर्दिष्ट किया जाता है। अन्य implementations भी संभव हैं। उदाहरण के लिए, router के भीतर नेटवर्क पर real-time lookups (DNS की तरह) के लिए एक प्रायोगिक सुविधा है। अधिक जानकारी के लिए [चर्चा पृष्ठ पर विकल्प](/docs/legacy/naming/#alternatives) देखें।

HTTP proxy सभी hostnames के लिए router के माध्यम से lookup करता है जो '.i2p' पर समाप्त होते हैं। अन्यथा, यह request को एक configured HTTP outproxy पर forward कर देता है। इसलिए, व्यावहारिक रूप से, सभी HTTP (I2P Site) hostnames का pseudo-Top Level Domain '.i2p' पर समाप्त होना आवश्यक है।

यदि router hostname को resolve करने में असफल हो जाता है, तो HTTP proxy उपयोगकर्ता को कई "jump" सेवाओं के links के साथ एक error page वापस करता है। विवरण के लिए नीचे देखें।

---

## .i2p.alt डोमेन

हमने पहले [.i2p TLD को आरक्षित करने के लिए आवेदन दिया था](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/) [RFC 6761](https://www.rfc-editor.org/rfc/rfc6761.html) में निर्दिष्ट प्रक्रियाओं का पालन करते हुए। हालांकि, यह आवेदन और अन्य सभी आवेदन खारिज कर दिए गए, और RFC 6761 को एक "गलती" घोषित किया गया।

GNUnet टीम और अन्य द्वारा कई वर्षों के काम के बाद, .alt डोमेन को 2023 के अंत तक [RFC 9476](https://www.rfc-editor.org/rfc/rfc9476.html) में एक विशेष-उपयोग TLD के रूप में आरक्षित किया गया था। जबकि IANA द्वारा स्वीकृत कोई आधिकारिक रजिस्ट्रार नहीं हैं, हमने प्राथमिक अनौपचारिक रजिस्ट्रार [GANA](https://gana.gnunet.org/dot-alt/dot_alt.html) के साथ .i2p.alt डोमेन पंजीकृत किया है। यह दूसरों को डोमेन उपयोग करने से नहीं रोकता है, लेकिन इससे इसे हतोत्साहित करने में मदद मिलनी चाहिए।

.alt domain का एक फायदा यह है कि, सिद्धांत रूप में, DNS resolvers RFC 9476 का अनुपालन करने के लिए अपडेट होने के बाद .alt requests को forward नहीं करेंगे, और इससे DNS leaks की रोकथाम होगी। .i2p.alt hostnames के साथ compatibility के लिए, I2P software और services को इन hostnames को handle करने के लिए अपडेट किया जाना चाहिए ताकि .alt TLD को हटा दिया जा सके। ये अपडेट 2024 की पहली छमाही में निर्धारित हैं।

इस समय, .i2p.alt को I2P hostnames के प्रदर्शन और आदान-प्रदान के लिए पसंदीदा रूप बनाने की कोई योजना नहीं है। यह आगे की अनुसंधान और चर्चा का विषय है।

---

## पता पुस्तिका

### आने वाली सब्स्क्रिप्शन और मर्जिंग

पता पुस्तिका एप्लिकेशन समय-समय पर अन्य उपयोगकर्ताओं की hosts.txt फाइलों को प्राप्त करती है और कई जांचों के बाद उन्हें स्थानीय hosts.txt के साथ मिला देती है। नामकरण संघर्षों का समाधान पहले आने पहले पाने के आधार पर किया जाता है।

किसी अन्य उपयोगकर्ता की hosts.txt फाइल को subscribe करने में उन्हें एक निश्चित मात्रा में विश्वास देना शामिल है। आप नहीं चाहते कि वे, उदाहरण के लिए, किसी नई साइट को 'hijack' करें जैसे कि नई साइट के लिए अपनी खुद की key तेज़ी से डालकर नए host/key entry को आपको भेजने से पहले।

इस कारण से, केवल एक subscription डिफ़ॉल्ट रूप से कॉन्फ़िगर की गई है `http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`, जिसमें I2P रिलीज़ में शामिल hosts.txt की एक प्रति होती है। उपयोगकर्ताओं को अपनी स्थानीय एड्रेस बुक एप्लिकेशन में अतिरिक्त subscriptions कॉन्फ़िगर करनी होंगी (subscriptions.txt या [SusiDNS](#susidns) के माध्यम से)।

कुछ अन्य सार्वजनिक address book सब्स्क्रिप्शन लिंक:

- http://i2host.i2p/cgi-bin/i2hostetag
- http://stats.i2p/cgi-bin/newhosts.txt

इन सेवाओं के संचालकों के पास होस्ट्स को सूचीबद्ध करने के लिए विभिन्न नीतियां हो सकती हैं। इस सूची में उपस्थिति का मतलब समर्थन नहीं है।

### नामकरण नियम

जबकि I2P के भीतर host names पर कोई तकनीकी सीमाएं नहीं होनी चाहिए, address book subscriptions से आयात किए गए host names पर कई प्रतिबंध लगाता है। यह बुनियादी टाइपोग्राफिकल स्वच्छता और browsers के साथ संगतता के लिए, और सुरक्षा के लिए करता है। नियम मूलतः RFC2396 Section 3.2.2 के समान हैं। इन नियमों का उल्लंघन करने वाले किसी भी hostnames को अन्य routers तक प्रसारित नहीं किया जा सकता।

नामकरण नियम:

- Names को import करते समय lower case में convert कर दिया जाता है।
- Names को lower case में convert करने के बाद existing userhosts.txt और hosts.txt (लेकिन privatehosts.txt में नहीं) में existing names के साथ conflict के लिए check किया जाता है।
- Lower case में convert करने के बाद केवल [a-z] [0-9] '.' और '-' contain करना चाहिए।
- '.' या '-' से start नहीं होना चाहिए।
- '.i2p' से end होना चाहिए।
- '.i2p' सहित अधिकतम 67 characters।
- '..' contain नहीं करना चाहिए।
- '.-' या '-.' contain नहीं करना चाहिए (0.6.1.33 के बाद से)।
- IDN के लिए 'xn--' को छोड़कर '--' contain नहीं करना चाहिए।
- Base32 hostnames (*.b32.i2p) base 32 use के लिए reserved हैं इसलिए import करने की अनुमति नहीं है।
- Project use के लिए reserved कुछ hostnames की अनुमति नहीं है (proxy.i2p, router.i2p, console.i2p, mail.i2p, *.proxy.i2p, *.router.i2p, *.console.i2p, *.mail.i2p, और अन्य)
- 'www.' से शुरू होने वाले hostnames discouraged हैं और कुछ registration services द्वारा reject कर दिए जाते हैं। कुछ addressbook implementations automatically lookups से 'www.' prefixes को strip कर देते हैं। इसलिए 'www.example.i2p' register करना unnecessary है, और 'www.example.i2p' और 'example.i2p' के लिए अलग destination register करने से कुछ users के लिए 'www.example.i2p' unreachable हो जाएगा।
- Keys को base64 validity के लिए check किया जाता है।
- Keys को hosts.txt (लेकिन privatehosts.txt में नहीं) में existing keys के साथ conflict के लिए check किया जाता है।
- Minimum key length 516 bytes।
- Maximum key length 616 bytes (100 bytes तक के certs के लिए account करने के लिए)।

सब्स्क्रिप्शन के माध्यम से प्राप्त कोई भी नाम जो सभी जांच पास करता है, उसे स्थानीय नामकरण सेवा के माध्यम से जोड़ा जाता है।

ध्यान दें कि होस्ट नाम में '.' प्रतीकों का कोई महत्व नहीं है, और ये किसी वास्तविक नामकरण या ट्रस्ट पदानुक्रम को दर्शाते नहीं हैं। यदि 'host.i2p' नाम पहले से मौजूद है, तो किसी को भी अपनी hosts.txt में 'a.host.i2p' नाम जोड़ने से रोकने के लिए कुछ भी नहीं है, और यह नाम दूसरों की address book द्वारा आयात किया जा सकता है। गैर-डोमेन 'मालिकों' को subdomain से इनकार करने की विधियां (certificates?), और इन विधियों की वांछनीयता और व्यवहार्यता, भविष्य की चर्चा के विषय हैं।

International Domain Names (IDN) भी i2p में काम करते हैं (punycode 'xn--' रूप का उपयोग करके)। Firefox के location bar में IDN .i2p domain names को सही तरीके से प्रदर्शित देखने के लिए, about:config में 'network.IDN.whitelist.i2p (boolean) = true' जोड़ें।

चूंकि address book एप्लिकेशन privatehosts.txt का बिल्कुल उपयोग नहीं करता है, व्यावहारिक रूप से यह फ़ाइल एकमात्र स्थान है जहाँ उन साइटों के लिए निजी aliases या "pet names" रखना उपयुक्त है जो पहले से ही hosts.txt में मौजूद हैं।

### उन्नत सब्स्क्रिप्शन फीड प्रारूप

रिलीज़ 0.9.26 से, subscription साइटें और clients एक उन्नत hosts.txt feed protocol का समर्थन कर सकते हैं जिसमें signatures सहित metadata शामिल है। यह format मानक hosts.txt hostname=base64destination format के साथ backwards-compatible है। विवरण के लिए [specification](/docs/specs/subscription/) देखें।

### आउटगोइंग सब्सक्रिप्शन

Address Book मर्ज किए गए hosts.txt को एक स्थान पर प्रकाशित करेगा (परंपरागत रूप से स्थानीय I2P Site की होम डायरेक्टरी में hosts.txt) ताकि अन्य लोग अपनी सब्सक्रिप्शन के लिए इसे एक्सेस कर सकें। यह चरण वैकल्पिक है और डिफ़ॉल्ट रूप से अक्षम है।

### होस्टिंग और HTTP ट्रांसपोर्ट समस्याएं

address book एप्लिकेशन, eepget के साथ मिलकर, subscription के web server द्वारा वापस की गई Etag और/या Last-Modified जानकारी को save करता है। यह आवश्यक bandwidth को काफी कम कर देता है, क्योंकि अगली fetch पर यदि कुछ भी नहीं बदला है तो web server '304 Not Modified' return करेगा।

हालांकि यदि hosts.txt में कोई बदलाव हुआ है तो पूरी hosts.txt फ़ाइल डाउनलोड हो जाती है। इस मुद्दे पर चर्चा के लिए नीचे देखें।

Static hosts.txt या समकक्ष CGI application सर्व करने वाले hosts को दृढ़ता से प्रोत्साहित किया जाता है कि वे Content-Length header, और या तो Etag या Last-Modified header प्रदान करें। यह भी सुनिश्चित करें कि server उपयुक्त होने पर '304 Not Modified' प्रदान करे। यह network bandwidth को नाटकीय रूप से कम करेगा, और corruption की संभावनाओं को कम करेगा।

---

## होस्ट सेवाएं जोड़ें

एक host add service एक सरल CGI एप्लिकेशन है जो hostname और Base64 key को parameters के रूप में लेती है और उसे अपनी local hosts.txt में जोड़ देती है। यदि अन्य routers उस hosts.txt को subscribe करते हैं, तो नया hostname/key network के माध्यम से propagate हो जाएगा।

यह अनुशंसा की जाती है कि host add services कम से कम वे प्रतिबंध लगाएं जो ऊपर सूचीबद्ध address book application द्वारा लगाए गए हैं। Host add services hostnames और keys पर अतिरिक्त प्रतिबंध भी लगा सकती हैं, उदाहरण के लिए:

- 'subdomains' की संख्या पर सीमा।
- विभिन्न तरीकों के माध्यम से 'subdomains' के लिए प्राधिकरण।
- Hashcash या signed certificates।
- host names और/या content की संपादकीय समीक्षा।
- content के आधार पर hosts का वर्गीकरण।
- कुछ host names का आरक्षण या अस्वीकार।
- किसी निश्चित समयावधि में पंजीकृत names की संख्या पर प्रतिबंध।
- पंजीकरण और प्रकाशन के बीच देरी।
- सत्यापन के लिए host के चालू होने की आवश्यकता।
- समाप्ति और/या निरसन।
- IDN spoof rejection।

---

## जंप सेवाएं

एक jump service एक सरल CGI एप्लिकेशन है जो hostname को parameter के रूप में लेती है और उचित URL पर 301 redirect वापस करती है जिसके साथ `?i2paddresshelper=key` स्ट्रिंग जोड़ी जाती है। HTTP proxy इस जोड़ी गई स्ट्रिंग की व्याख्या करेगा और उस key को वास्तविक गंतव्य के रूप में उपयोग करेगा। इसके अतिरिक्त, proxy उस key को cache करेगा ताकि restart तक address helper की आवश्यकता न हो।

ध्यान दें कि subscriptions की तरह ही, jump service का उपयोग करना एक निश्चित मात्रा में भरोसे को दर्शाता है, क्योंकि एक jump service दुर्भावनापूर्ण तरीके से उपयोगकर्ता को गलत गंतव्य पर redirect कर सकता है।

सर्वोत्तम सेवा प्रदान करने के लिए, एक jump service को कई hosts.txt प्रदाताओं की सदस्यता लेनी चाहिए ताकि इसकी स्थानीय host सूची अद्यतन रहे।

---

## SusiDNS

SusiDNS केवल address book subscriptions को configure करने और चार address book files तक पहुंचने के लिए एक web interface front-end है। सभी वास्तविक कार्य 'address book' application द्वारा किया जाता है।

वर्तमान में, SusiDNS के भीतर address book नामकरण नियमों का बहुत कम प्रवर्तन है, इसलिए एक उपयोगकर्ता स्थानीय रूप से ऐसे hostnames दर्ज कर सकता है जो address book subscription नियमों द्वारा अस्वीकार कर दिए जाएंगे।

---

## Base32 नाम

I2P, Tor के .onion addresses के समान Base32 hostnames का समर्थन करता है। Base32 addresses पूर्ण 516-character Base64 Destinations या addresshelpers की तुलना में बहुत छोटे और संभालने में आसान होते हैं। उदाहरण: `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

Tor में, पता 16 वर्णों (80 बिट्स) का होता है, या SHA-1 hash का आधा भाग। I2P पूर्ण SHA-256 hash को दर्शाने के लिए 52 वर्णों (256 बिट्स) का उपयोग करता है। इसका रूप {52 chars}.b32.i2p है। Tor का एक [proposal](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013) है अपनी hidden services के लिए {52 chars}.onion के समान प्रारूप में बदलने का। Base32 naming service में लागू किया गया है, जो पूर्ण Destination प्राप्त करने के लिए LeaseSet lookup करने हेतु I2CP पर router से क्वेरी करता है। Base32 lookups तभी सफल होंगे जब Destination उपलब्ध हो और LeaseSet प्रकाशित कर रहा हो। क्योंकि resolution के लिए network database lookup की आवश्यकता हो सकती है, यह local address book lookup की तुलना में काफी अधिक समय ले सकता है।

Base32 पते अधिकांश स्थानों पर उपयोग किए जा सकते हैं जहाँ hostnames या पूर्ण destinations का उपयोग होता है, हालांकि कुछ अपवाद हैं जहाँ वे विफल हो सकते हैं यदि नाम तुरंत resolve नहीं होता। I2PTunnel विफल हो जाएगा, उदाहरण के लिए, यदि नाम किसी destination में resolve नहीं होता।

---

## विस्तारित Base32 नाम

Extended base 32 नाम release 0.9.40 में encrypted lease sets के समर्थन के लिए पेश किए गए थे। Encrypted leasesets के addresses की पहचान 56 या अधिक encoded characters से होती है, ".b32.i2p" को छोड़कर (35 या अधिक decoded bytes), जबकि traditional base 32 addresses के लिए 52 characters (32 bytes) होते हैं। अतिरिक्त जानकारी के लिए proposals 123 और 149 देखें।

मानक Base 32 ("b32") पते में destination का hash होता है। यह encrypted ls2 (proposal 123) के लिए काम नहीं करेगा।

आप एक encrypted LS2 (proposal 123) के लिए पारंपरिक base 32 address का उपयोग नहीं कर सकते, क्योंकि इसमें केवल destination का hash होता है। यह non-blinded public key प्रदान नहीं करता। Clients को destination की public key, sig type, blinded sig type, और leaseset को fetch और decrypt करने के लिए एक वैकल्पिक secret या private key जानना आवश्यक है। इसलिए, केवल base 32 address अपर्याप्त है। Client को या तो पूरा destination (जिसमें public key है), या अकेली public key की आवश्यकता होती है। यदि client के पास address book में पूरा destination है, और address book hash द्वारा reverse lookup का समर्थन करता है, तो public key प्राप्त की जा सकती है।

इसलिए हमें एक नए फॉर्मेट की आवश्यकता है जो hash के बजाय public key को base32 address में डाले। इस फॉर्मेट में public key के signature type और blinding scheme के signature type भी होने चाहिए।

यह खंड इन पतों के लिए एक नए b32 फॉर्मेट का दस्तावेजीकरण करता है। जबकि हमने चर्चाओं के दौरान इस नए फॉर्मेट को "b33" पता कहा है, वास्तविक नया फॉर्मेट सामान्य ".b32.i2p" प्रत्यय को बरकरार रखता है।

### निर्माण और एन्कोडिंग

{56+ chars}.b32.i2p (बाइनरी में 35+ chars) का hostname निम्नलिखित तरीके से बनाएं। पहले, base 32 encoded होने वाले बाइनरी डेटा को बनाएं:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
पोस्ट-प्रोसेसिंग और चेकसम:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
b32 के अंत में कोई भी अप्रयुक्त bits 0 होने चाहिए। एक मानक 56 character (35 byte) address के लिए कोई अप्रयुक्त bits नहीं हैं।

### डिकोडिंग और सत्यापन

```
Strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes) :
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### गुप्त और निजी की बिट्स

secret और private key bits का उपयोग clients, proxies, या अन्य client-side code को यह संकेत देने के लिए किया जाता है कि leaseset को decrypt करने के लिए secret और/या private key की आवश्यकता होगी। विशिष्ट implementations उपयोगकर्ता से आवश्यक डेटा प्रदान करने के लिए संकेत कर सकते हैं, या यदि आवश्यक डेटा गुम है तो connection attempts को अस्वीकार कर सकते हैं।

### नोट्स

- पहले 3 bytes को hash के साथ XORing करना सीमित checksum क्षमता प्रदान करता है, और सुनिश्चित करता है कि शुरुआत में सभी base32 chars randomized हों। केवल कुछ flag और sigtype combinations वैध हैं, इसलिए कोई भी typo एक अवैध combination बनाने की संभावना है और इसे reject कर दिया जाएगा।
- सामान्य स्थिति में (1 byte sigtypes, कोई secret नहीं, कोई per-client auth नहीं), hostname {56 chars}.b32.i2p होगा, जो 35 bytes में decode होगा, Tor के समान।
- Tor 2-byte checksum की 1/64K false negative rate है। 3 bytes के साथ, कुछ ignored bytes को घटाकर, हमारी दर एक मिलियन में से एक के करीब है, क्योंकि अधिकांश flag/sigtype combinations अवैध हैं।
- छोटे inputs के लिए और छोटे बदलावों का पता लगाने के लिए Adler-32 एक खराब विकल्प है। हम इसके बजाय CRC-32 का उपयोग करते हैं। CRC-32 तेज़ है और व्यापक रूप से उपलब्ध है।
- जबकि यह इस specification के दायरे से बाहर है, routers और/या clients को public key से destination की mapping को याद रखना और cache करना चाहिए (शायद persistently), और इसके विपरीत।
- length के आधार पर पुराने और नए flavors को अलग करें। पुराने b32 addresses हमेशा {52 chars}.b32.i2p होते हैं। नए {56+ chars}.b32.i2p हैं
- Tor discussion thread [यहाँ है](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- 2-byte sigtypes के कभी होने की उम्मीद न करें, हम केवल 13 तक हैं। अभी implement करने की आवश्यकता नहीं।
- नया format jump links में उपयोग किया जा सकता है (और jump servers द्वारा serve किया जा सकता है) यदि वांछित हो, बिल्कुल b32 की तरह।
- 32 bytes से लंबी कोई भी secret, private key, या public key DNS max label length 63 chars से अधिक हो जाएगी। Browsers शायद परवाह नहीं करते।
- कोई backward compatibility समस्याएं नहीं। लंबे b32 addresses पुराने software में 32-byte hashes में convert होने में असफल हो जाएंगे।
