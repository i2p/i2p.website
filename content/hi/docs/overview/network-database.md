---
title: "नेटवर्क डेटाबेस"
description: "I2P के वितरित नेटवर्क डेटाबेस (netDb) को समझना - router संपर्क जानकारी और गंतव्य खोजों के लिए एक विशेषीकृत DHT"
slug: "network-database"
aliases:
  - "/hi/how_networkdatabase"
  - "/hi/how_networkdatabase/"
lastUpdated: "2025-03"
accurateFor: "0.9.65"
---

## अवलोकन

I2P का netDb एक विशेषीकृत वितरित डेटाबेस है, जिसमें केवल दो प्रकार के डेटा होते हैं - router संपर्क जानकारी (**RouterInfos**) और destination संपर्क जानकारी (**LeaseSets**)। प्रत्येक डेटा को उपयुक्त पक्ष द्वारा हस्ताक्षरित किया जाता है और इसे उपयोग या संग्रहीत करने वाले किसी भी व्यक्ति द्वारा सत्यापित किया जाता है। इसके अतिरिक्त, डेटा में जीवंतता की जानकारी होती है, जो अप्रासंगिक प्रविष्टियों को हटाने, नई प्रविष्टियों को पुरानी को बदलने, और हमले के कुछ वर्गों से सुरक्षा प्रदान करने की अनुमति देती है।

netDb को "floodfill" नामक एक सरल तकनीक के साथ वितरित किया जाता है, जहाँ सभी routers के एक उपसमुच्चय को, जिसे "floodfill routers" कहा जाता है, distributed database का रखरखाव करता है।

---

## RouterInfo

जब एक I2P router किसी अन्य router से संपर्क करना चाहता है, तो उन्हें डेटा के कुछ मुख्य भागों को जानना होता है - जिन सभी को router द्वारा एक साथ बांधा जाता है और "RouterInfo" नामक संरचना में हस्ताक्षरित किया जाता है, जो router की पहचान के SHA256 को key के रूप में उपयोग करके वितरित की जाती है। इस संरचना में स्वयं निम्नलिखित शामिल है:

- router की पहचान (एक encryption key, एक signing key, और एक certificate)
- संपर्क पते जिन पर इसे पहुंचा जा सकता है
- यह कब प्रकाशित किया गया था
- मनमाने टेक्स्ट विकल्पों का एक सेट
- उपरोक्त का हस्ताक्षर, जो identity की signing key द्वारा जेनरेट किया गया है

### अपेक्षित विकल्प

निम्नलिखित टेक्स्ट विकल्प, हालांकि सख्ती से आवश्यक नहीं हैं, उपस्थित होने की अपेक्षा की जाती है:

- **caps** (Capabilities flags - floodfill भागीदारी, अनुमानित bandwidth, और कथित पहुंच को इंगित करने के लिए उपयोग किए जाने वाले झंडे)
  - **D**: मध्यम भीड़भाड़ (रिलीज़ 0.9.58 के अनुसार)
  - **E**: उच्च भीड़भाड़ (रिलीज़ 0.9.58 के अनुसार)
  - **f**: Floodfill
  - **G**: सभी tunnel खारिज कर रहा है (रिलीज़ 0.9.58 के अनुसार)
  - **H**: छिपा हुआ
  - **K**: 12 KBps से कम साझा bandwidth
  - **L**: 12 - 48 KBps साझा bandwidth (डिफ़ॉल्ट)
  - **M**: 48 - 64 KBps साझा bandwidth
  - **N**: 64 - 128 KBps साझा bandwidth
  - **O**: 128 - 256 KBps साझा bandwidth
  - **P**: 256 - 2000 KBps साझा bandwidth (रिलीज़ 0.9.20 के अनुसार, नीचे दिया गया नोट देखें)
  - **R**: पहुंच योग्य
  - **U**: पहुंच योग्य नहीं
  - **X**: 2000 KBps से अधिक साझा bandwidth (रिलीज़ 0.9.20 के अनुसार, नीचे दिया गया नोट देखें)

"साझा बैंडविड्थ" == (साझा %) * min(इन bw, आउट bw)

पुराने routers के साथ संगतता के लिए, एक router कई bandwidth अक्षर प्रकाशित कर सकता है, उदाहरण के लिए "PO"।

नोट: P और X बैंडविड्थ क्लासों के बीच सीमा या तो 2000 या 2048 KBps हो सकती है, यह implementor का चुनाव है।

- **netId** = 2 (बुनियादी नेटवर्क संगतता - एक router अलग netId वाले peer के साथ संवाद करने से इंकार कर देगा)
- **router.version** (नई सुविधाओं और संदेशों के साथ संगतता निर्धारित करने के लिए उपयोग किया जाता है)

R/U क्षमताओं पर नोट्स: एक router को आमतौर पर R या U capability प्रकाशित करना चाहिए, जब तक कि पहुंच योग्यता की स्थिति वर्तमान में अज्ञात न हो। R का मतलब है कि router कम से कम एक transport address पर सीधे पहुंच योग्य है (कोई introducers की आवश्यकता नहीं, firewalled नहीं)। U का मतलब है कि router किसी भी transport address पर सीधे पहुंच योग्य नहीं है।

अप्रचलित विकल्प: - ~~coreVersion~~ (कभी उपयोग नहीं किया गया, रिलीज़ 0.9.24 में हटा दिया गया) - ~~stat_uptime~~ = 90m (संस्करण 0.7.9 के बाद से अनुपयोगी, रिलीज़ 0.9.24 में हटा दिया गया)

ये मान अन्य routers द्वारा बुनियादी निर्णयों के लिए उपयोग किए जाते हैं। क्या हमें इस router से जुड़ना चाहिए? क्या हमें इस router के माध्यम से tunnel route करने का प्रयास करना चाहिए? bandwidth क्षमता flag, विशेष रूप से, केवल यह निर्धारित करने के लिए उपयोग किया जाता है कि क्या router tunnel routing के लिए न्यूनतम सीमा को पूरा करता है। न्यूनतम सीमा के ऊपर, विज्ञापित bandwidth का router में कहीं भी उपयोग या भरोसा नहीं किया जाता है, सिवाय user interface में प्रदर्शन और debugging तथा network विश्लेषण के लिए।

वैध NetID संख्याएं:

| उपयोग | NetID संख्या |
|-------|--------------|
| आरक्षित | 0 |
| आरक्षित | 1 |
| वर्तमान नेटवर्क (डिफ़ॉल्ट) | 2 |
| भविष्य के आरक्षित नेटवर्क | 3 - 15 |
| फोर्क और टेस्ट नेटवर्क | 16 - 254 |
| आरक्षित | 255 |
### अतिरिक्त विकल्प

अतिरिक्त टेक्स्ट विकल्पों में router के स्वास्थ्य के बारे में कुछ आंकड़े शामिल हैं, जो [stats.i2p](http://stats.i2p/) जैसी साइटों द्वारा नेटवर्क प्रदर्शन विश्लेषण और डिबगिंग के लिए एकत्रित किए जाते हैं। इन आंकड़ों को डेवलपर्स के लिए महत्वपूर्ण डेटा प्रदान करने के लिए चुना गया था, जैसे कि tunnel निर्माण सफलता दरें, जबकि इस डेटा की आवश्यकता को इस डेटा को प्रकट करने से होने वाले दुष्प्रभावों के साथ संतुलित किया गया है। वर्तमान आंकड़े सीमित हैं:

- खोजी tunnel निर्माण सफलता, अस्वीकार, और timeout दरें
- 1 घंटे की औसत भाग लेने वाले tunnels की संख्या

ये वैकल्पिक हैं, लेकिन यदि शामिल किए जाएं, तो नेटवर्क-व्यापी प्रदर्शन के विश्लेषण में सहायता करते हैं। API 0.9.58 के अनुसार, ये आंकड़े सरलीकृत और मानकीकृत हैं, निम्नलिखित के अनुसार:

- Option keys स्टेट_(statname).(statperiod) होते हैं
- Option values ';' से अलग किए जाते हैं
- Event counts या normalized percentages के लिए stats चौथी value का उपयोग करते हैं; पहली तीन values अनुपयोगी हैं लेकिन उपस्थित होनी चाहिए
- Average values के लिए stats पहली value का उपयोग करते हैं, और ';' separator की आवश्यकता नहीं है
- Stats विश्लेषण में सभी routers के समान भार के लिए, और अतिरिक्त गुमनामी के लिए, routers को ये stats केवल एक घंटे या अधिक uptime के बाद शामिल करने चाहिए, और केवल हर 16 बार में एक बार जब RI प्रकाशित होता है।

उदाहरण:

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Floodfill router अपने network database में entries की संख्या पर अतिरिक्त डेटा प्रकाशित कर सकते हैं। ये वैकल्पिक हैं, लेकिन यदि शामिल किए जाते हैं, तो network-wide प्रदर्शन के विश्लेषण में मदद करते हैं।

निम्नलिखित दो विकल्पों को floodfill routers द्वारा प्रत्येक प्रकाशित RI में शामिल किया जाना चाहिए:

- **netdb.knownLeaseSets**
- **netdb.knownRouters**

उदाहरण:

```
netdb.knownLeaseSets = 158
netdb.knownRouters = 11374
```
प्रकाशित डेटा router के user interface में देखा जा सकता है, लेकिन किसी अन्य router द्वारा इसका उपयोग या भरोसा नहीं किया जाता है।

### पारिवारिक विकल्प

रिलीज़ 0.9.24 के अनुसार, router घोषणा कर सकते हैं कि वे एक "family" का हिस्सा हैं, जो एक ही संस्था द्वारा संचालित होते हैं। एक ही family के कई router को एक single tunnel में उपयोग नहीं किया जाएगा।

परिवार विकल्प हैं:

- **family** (पारिवारिक नाम)
- **family.key** पारिवारिक [Signing Public Key](/docs/specs/common-structures/#type_SigningPublicKey) के signature type code (ASCII अंकों में) को ':' के साथ जोड़कर और फिर Signing Public Key को base 64 में जोड़ा गया
- **family.sig** ((UTF-8 में पारिवारिक नाम) को (32 byte router hash) के साथ जोड़ने का) signature base 64 में

### RouterInfo समाप्ति

RouterInfo की कोई निर्धारित समाप्ति समय नहीं होता। प्रत्येक router अपनी स्थानीय नीति बनाने के लिए स्वतंत्र है ताकि RouterInfo खोजों की आवृत्ति को मेमोरी या डिस्क उपयोग के साथ संतुलित किया जा सके। वर्तमान कार्यान्वयन में, निम्नलिखित सामान्य नीतियां हैं:

- पहले घंटे के uptime के दौरान कोई expiration नहीं होती, क्योंकि persistent stored data पुराना हो सकता है।
- यदि 25 या उससे कम RouterInfos हैं तो कोई expiration नहीं होती।
- जैसे-जैसे local RouterInfos की संख्या बढ़ती है, expiration time कम होता जाता है, ताकि RouterInfos की एक उचित संख्या बनी रहे। 120 से कम routers के साथ expiration time 72 घंटे है, जबकि 300 routers के साथ expiration time लगभग 30 घंटे है।
- [SSU](/docs/legacy/ssu/) introducers वाले RouterInfos लगभग एक घंटे में expire हो जाते हैं, क्योंकि introducer list लगभग उसी समय में expire हो जाती है।
- Floodfills सभी local RouterInfos के लिए कम expiration time (1 घंटा) का उपयोग करते हैं, क्योंकि valid RouterInfos उनमें बार-बार republish होते रहेंगे।

### RouterInfo स्थायी भंडारण

RouterInfos को समय-समय पर डिस्क पर लिखा जाता है ताकि वे restart के बाद उपलब्ध रहें।

लंबी समाप्ति अवधि वाले Meta LeaseSets को स्थायी रूप से संग्रहीत करना वांछनीय हो सकता है। यह implementation पर निर्भर है।

### यह भी देखें

- [RouterInfo specification](/docs/specs/common-structures/#struct_RouterInfo)
- [RouterInfo Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/router/RouterInfo.html)

---

## LeaseSet

netDb में वितरित डेटा का दूसरा हिस्सा "LeaseSet" है - जो किसी विशिष्ट client destination के लिए **tunnel entry points (leases)** के एक समूह का दस्तावेजीकरण करता है। इनमें से प्रत्येक lease निम्नलिखित जानकारी निर्दिष्ट करता है:

- tunnel gateway router (इसकी पहचान निर्दिष्ट करके)
- उस router पर tunnel ID जिसके साथ संदेश भेजना है (एक 4 बाइट संख्या)
- वह tunnel कब समाप्त होगा।

LeaseSet स्वयं netDb में destination के SHA256 से प्राप्त key के तहत संग्रहीत किया जाता है। एक अपवाद Encrypted LeaseSets (LS2) के लिए है, release 0.9.38 के अनुसार। type byte (3) के बाद blinded public key के SHA256 का उपयोग DHT key के लिए किया जाता है, और फिर सामान्य रूप से rotate किया जाता है। नीचे Kademlia Closeness Metric section देखें।

इन leases के अतिरिक्त, LeaseSet में शामिल है:

- गंतव्य स्वयं (एक encryption key, एक signing key और एक certificate)
- अतिरिक्त encryption public key: garlic messages की end-to-end encryption के लिए उपयोग की जाती है
- अतिरिक्त signing public key: LeaseSet निरसन के लिए अभिप्रेत है, लेकिन वर्तमान में अप्रयुक्त है।
- सभी LeaseSet डेटा का signature, यह सुनिश्चित करने के लिए कि Destination ने LeaseSet प्रकाशित किया है।

- [Lease विशिष्टता](/docs/specs/common-structures/#struct_Lease)
- [LeaseSet विशिष्टता](/docs/specs/common-structures/#struct_LeaseSet)
- [Lease Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/Lease.html)
- [LeaseSet Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/LeaseSet.html)

रिलीज़ 0.9.38 के अनुसार, तीन नए प्रकार के LeaseSets परिभाषित हैं; LeaseSet2, MetaLeaseSet, और EncryptedLeaseSet। नीचे देखें।

### अप्रकाशित LeaseSets

केवल आउटगोइंग कनेक्शन के लिए उपयोग किए जाने वाले destination के लिए एक LeaseSet *unpublished* होता है। यह कभी भी floodfill router को प्रकाशन के लिए नहीं भेजा जाता। "Client" tunnel, जैसे कि वेब ब्राउज़िंग और IRC client के लिए, unpublished होते हैं। सर्वर अभी भी उन unpublished destinations को संदेश वापस भेज सकेंगे, [I2NP storage messages](#leaseset-storage-to-peers) की वजह से।

### निरस्त LeaseSet

एक LeaseSet को शून्य leases के साथ एक नया LeaseSet प्रकाशित करके *रद्द* किया जा सकता है। रद्दीकरण को LeaseSet में अतिरिक्त signing key द्वारा हस्ताक्षरित होना चाहिए। रद्दीकरण पूरी तरह से लागू नहीं हैं, और यह अस्पष्ट है कि उनका कोई व्यावहारिक उपयोग है या नहीं। यह उस signing key के लिए एकमात्र नियोजित उपयोग है, इसलिए यह वर्तमान में अप्रयुक्त है।

### LeaseSet2 (LS2)

रिलीज 0.9.38 के बाद से, floodfills एक नई LeaseSet2 संरचना का समर्थन करते हैं। यह संरचना पुरानी LeaseSet संरचना के समान है, और समान उद्देश्य पूरा करती है। नई संरचना नए एन्क्रिप्शन प्रकार, कई एन्क्रिप्शन प्रकार, विकल्प, offline signing keys, और अन्य सुविधाओं का समर्थन करने के लिए आवश्यक लचीलापन प्रदान करती है। विवरण के लिए proposal 123 देखें।

### Meta LeaseSet (LS2)

रिलीज़ 0.9.38 के बाद से, floodfills एक नई Meta LeaseSet संरचना का समर्थन करते हैं। यह संरचना DHT में एक वृक्ष-जैसी संरचना प्रदान करती है, जो अन्य LeaseSets को संदर्भित करने के लिए है। Meta LeaseSets का उपयोग करके, एक साइट बड़ी multihomed सेवाओं को लागू कर सकती है, जहाँ कई अलग-अलग Destinations का उपयोग एक सामान्य सेवा प्रदान करने के लिए किया जाता है। Meta LeaseSet में प्रविष्टियाँ Destinations या अन्य Meta LeaseSets हैं, और इनकी समय-सीमा लंबी हो सकती है, 18.2 घंटों तक। इस सुविधा का उपयोग करके, एक सामान्य सेवा की मेजबानी करने वाले सैकड़ों या हजारों Destinations चलाना संभव होना चाहिए। विवरण के लिए proposal 123 देखें।

### एन्क्रिप्टेड LeaseSets (LS1)

यह अनुभाग एक निश्चित symmetric key का उपयोग करके LeaseSets को encrypt करने की पुराní, असुरक्षित विधि का वर्णन करता है। Encrypted LeaseSets के LS2 संस्करण के लिए नीचे देखें।

एक *encrypted* LeaseSet में, सभी Leases एक अलग key से encrypted होते हैं। leases को केवल उन्हीं के द्वारा decode किया जा सकता है, और इस प्रकार destination से संपर्क केवल उन्हीं के द्वारा किया जा सकता है जिनके पास key है। कोई flag या अन्य प्रत्यक्ष संकेत नहीं है कि LeaseSet encrypted है। Encrypted LeaseSets का व्यापक रूप से उपयोग नहीं किया जाता है, और यह भविष्य के कार्य का विषय है कि encrypted LeaseSets के user interface और implementation को बेहतर बनाया जा सकता है या नहीं।

### एन्क्रिप्टेड LeaseSets (LS2)

रिलीज़ 0.9.38 के रूप में, floodfills एक नई, EncryptedLeaseSet संरचना का समर्थन करते हैं। Destination छुपा हुआ है, और केवल एक blinded public key और एक expiration floodfill को दिखाई देता है। केवल वे जिनके पास पूरा Destination है, संरचना को decrypt कर सकते हैं। संरचना को DHT स्थान पर संग्रहीत किया जाता है जो blinded public key के hash के आधार पर होता है, Destination के hash के आधार पर नहीं। विवरण के लिए प्रस्ताव 123 देखें।

### LeaseSet की समाप्ति

नियमित leaseSets के लिए, समाप्ति का समय उसके leases की नवीनतम समाप्ति का समय होता है। नई leaseSet2 डेटा संरचनाओं के लिए, समाप्ति हेडर में निर्दिष्ट की जाती है। leaseSet2 के लिए, समाप्ति को उसके leases की नवीनतम समाप्ति से मेल खाना चाहिए। EncryptedLeaseSet और MetaLeaseSet के लिए, समाप्ति अलग हो सकती है, और अधिकतम समाप्ति लागू की जा सकती है, जो निर्धारित की जानी है।

### LeaseSet स्थायी भंडारण

LeaseSet डेटा के लिए स्थायी भंडारण की आवश्यकता नहीं है, क्योंकि वे बहुत जल्दी समाप्त हो जाते हैं। हालांकि, लंबी समाप्ति अवधि वाले EncryptedLeaseSet और MetaLeaseSet डेटा का स्थायी भंडारण उचित हो सकता है।

### एन्क्रिप्शन की चयन (LS2)

LeaseSet2 में कई encryption keys हो सकती हैं। keys सर्वर की प्राथमिकता के क्रम में होती हैं, सबसे पसंदीदा पहले। डिफ़ॉल्ट client व्यवहार समर्थित encryption type वाली पहली key का चयन करना है। Clients encryption समर्थन, सापेक्षिक प्रदर्शन, और अन्य कारकों के आधार पर अन्य चयन एल्गोरिदम का उपयोग कर सकते हैं।

---

## बूटस्ट्रैपिंग

netDb विकेंद्रीकृत है, हालांकि आपको कम से कम एक peer का संदर्भ चाहिए ताकि एकीकरण प्रक्रिया आपको जोड़ सके। यह आपके router को एक सक्रिय peer के RouterInfo के साथ "reseeding" करके पूरा किया जाता है - विशेष रूप से, उनकी `routerInfo-$hash.dat` फ़ाइल को प्राप्त करके और इसे अपनी `netDb/` डायरेक्टरी में संग्रहीत करके। कोई भी आपको वे फ़ाइलें प्रदान कर सकता है - आप अपनी netDb डायरेक्टरी को उजागर करके दूसरों को भी प्रदान कर सकते हैं। प्रक्रिया को सरल बनाने के लिए, स्वयंसेवक अपनी netDb डायरेक्टरियों (या एक उपसेट) को नियमित (गैर-i2p) नेटवर्क पर प्रकाशित करते हैं, और इन डायरेक्टरियों के URL I2P में हार्डकोड किए गए हैं। जब router पहली बार शुरू होता है, तो यह स्वचालित रूप से इन URLs में से एक से डेटा प्राप्त करता है, जो यादृच्छिक रूप से चुना जाता है।

---

## Floodfill

floodfill netDb एक सरल वितरित भंडारण तंत्र है। भंडारण एल्गोरिथम सरल है: डेटा को निकटतम peer को भेजें जिसने खुद को floodfill router के रूप में विज्ञापित किया है। जब floodfill netDb में peer को floodfill netDb में नहीं होने वाले peer से netDb store प्राप्त होता है, तो वे इसे floodfill netDb-peers के एक उपसमूह को भेजते हैं। चुने गए peers वे हैं जो किसी विशिष्ट key के निकटतम ([XOR-metric](#kademlia-closeness-metric) के अनुसार) हैं।

यह निर्धारित करना कि कौन floodfill netDb का हिस्सा है बहुत आसान है - यह प्रत्येक router की प्रकाशित routerInfo में एक क्षमता के रूप में उजागर होता है।

Floodfills का कोई केंद्रीय प्राधिकरण नहीं है और वे "सहमति" नहीं बनाते - वे केवल एक सरल DHT overlay लागू करते हैं।

### Floodfill Router ऑप्ट-इन

Tor के विपरीत, जहाँ directory servers हार्डकोडेड और विश्वसनीय होते हैं, और ज्ञात संस्थाओं द्वारा संचालित होते हैं, I2P floodfill peer set के सदस्यों को विश्वसनीय होने की आवश्यकता नहीं है, और ये समय के साथ बदलते रहते हैं।

netDb की विश्वसनीयता बढ़ाने के लिए, और router पर netDb ट्रैफिक के प्रभाव को कम करने के लिए, floodfill केवल उन router पर स्वचालित रूप से सक्षम होता है जो उच्च bandwidth सीमाओं के साथ कॉन्फ़िगर किए गए हैं। उच्च bandwidth सीमाओं वाले router (जिन्हें मैन्युअल रूप से कॉन्फ़िगर करना होता है, क्योंकि डिफ़ॉल्ट बहुत कम होता है) का अनुमान यह है कि वे कम विलंबता वाले कनेक्शन पर हैं, और 24/7 उपलब्ध रहने की संभावना अधिक होती है। एक floodfill router के लिए वर्तमान न्यूनतम share bandwidth 128 KBytes/sec है।

इसके अतिरिक्त, floodfill ऑपरेशन स्वचालित रूप से सक्षम होने से पहले एक router को स्वास्थ्य के लिए कई अतिरिक्त परीक्षणों (आउटबाउंड संदेश queue समय, job lag, आदि) को पास करना होगा।

वर्तमान automatic opt-in नियमों के साथ, नेटवर्क में लगभग 6% routers floodfill routers हैं।

जबकि कुछ peers को मैन्युअल रूप से floodfill के रूप में कॉन्फ़िगर किया जाता है, अन्य केवल उच्च-बैंडविड्थ router होते हैं जो स्वचालित रूप से स्वयंसेवक बन जाते हैं जब floodfill peers की संख्या एक सीमा से नीचे गिर जाती है। यह किसी हमले के कारण अधिकांश या सभी floodfill को खोने से होने वाले दीर्घकालिक नेटवर्क नुकसान को रोकता है। बदले में, ये peers स्वयं को un-floodfill कर लेते हैं जब बहुत सारे floodfill बकाया होते हैं।

### Floodfill Router भूमिकाएं

एक floodfill router की केवल वे सेवाएं जो non-floodfill routers की सेवाओं के अतिरिक्त होती हैं, वे netDb stores को स्वीकार करना और netDb queries का जवाब देना हैं। चूंकि ये आमतौर पर high-bandwidth होते हैं, इसलिए इनके अधिक संख्या में tunnels में भाग लेने (यानी दूसरों के लिए "relay" बनने) की अधिक संभावना होती है, लेकिन यह उनकी distributed database सेवाओं से सीधे संबंधित नहीं है।

---

## Kademlia निकटता मेट्रिक

netDb निकटता निर्धारित करने के लिए एक सरल Kademlia-style XOR metric का उपयोग करता है। Kademlia key बनाने के लिए, RouterIdentity या Destination का SHA256 hash गणना किया जाता है। एक अपवाद Encrypted LeaseSets (LS2) के लिए है, release 0.9.38 के अनुसार। DHT key के लिए type byte (3) के बाद blinded public key का SHA256 उपयोग किया जाता है, और फिर सामान्य रूप से rotate किया जाता है।

[Sybil attacks](#sybil-attack-partial-keyspace) की लागत बढ़ाने के लिए इस एल्गोरिदम में एक संशोधन किया गया है। खोजी जाने वाली या संग्रहीत की जाने वाली key के SHA256 hash के बजाय, 32-byte binary search key को UTC तारीख के साथ जोड़कर SHA256 hash लिया जाता है, जो 8-byte ASCII string yyyyMMdd के रूप में प्रदर्शित होती है, यानी SHA256(key + yyyyMMdd)। इसे "routing key" कहा जाता है, और यह हर दिन रात 12 बजे UTC पर बदलता है। केवल search key को इस तरह से संशोधित किया जाता है, floodfill router hashes को नहीं। DHT के इस दैनिक रूपांतरण को कभी-कभी "keyspace rotation" कहा जाता है, हालांकि यह सख्त अर्थ में rotation नहीं है।

Routing keys कभी भी किसी I2NP संदेश में wire पर नहीं भेजे जाते हैं, वे केवल स्थानीय रूप से दूरी निर्धारण के लिए उपयोग किए जाते हैं।

---

## नेटवर्क डेटाबेस विभाजन - उप-डेटाबेस

पारंपरिक रूप से Kademlia-शैली के DHT इस बात से चिंतित नहीं होते कि DHT में किसी विशेष node पर संग्रहीत जानकारी की unlinkability (असंबद्धता) को संरक्षित करना है या नहीं। उदाहरण के लिए, जानकारी का एक टुकड़ा DHT में एक node पर संग्रहीत हो सकता है, फिर उस node से बिना शर्त वापस मांगा जा सकता है। I2P और netDb का उपयोग करते समय, ऐसा नहीं है, DHT में संग्रहीत जानकारी केवल कुछ ज्ञात परिस्थितियों में साझा की जा सकती है जहाँ ऐसा करना "सुरक्षित" हो। यह attacks के एक वर्ग को रोकने के लिए है जहाँ एक दुर्भावनापूर्ण actor client tunnel को router के साथ जोड़ने की कोशिश कर सकता है - पहले client tunnel में store भेजकर, फिर संदिग्ध client tunnel के "Host" से सीधे इसे वापस मांगकर।

### विभाजन संरचना

I2P router इस attack class के विरुद्ध प्रभावी सुरक्षा लागू कर सकते हैं बशर्ते कुछ शर्तें पूरी हों। एक network database implementation को यह ट्रैक करने में सक्षम होना चाहिए कि कोई database entry client tunnel के माध्यम से प्राप्त हुई थी या सीधे। यदि वह client tunnel के माध्यम से प्राप्त हुई थी, तो उसे यह भी ट्रैक करना चाहिए कि वह किस client tunnel के माध्यम से प्राप्त हुई थी, client के local destination का उपयोग करते हुए। यदि entry कई client tunnel के माध्यम से प्राप्त हुई थी, तो netDb को उन सभी destinations का ट्रैक रखना चाहिए जहाँ entry देखी गई थी। इसे यह भी ट्रैक करना चाहिए कि कोई entry lookup के जवाब के रूप में प्राप्त हुई थी, या store के रूप में।

Java और C++ दोनों implementations में, यह एक single "Main" netDb का उपयोग करके प्राप्त किया जाता है जो direct lookups और floodfill operations के लिए पहले इस्तेमाल होता है। यह main netDb router context में मौजूद होता है। फिर, प्रत्येक client को netDb का अपना version दिया जाता है, जो client tunnels को भेजे गए database entries को capture करने और client tunnels के नीचे भेजे गए lookups का जवाब देने के लिए उपयोग किया जाता है। हम इन्हें "Client Network Databases" या "Sub-Databases" कहते हैं और ये client context में मौजूद होते हैं। Client द्वारा संचालित netDb केवल client के जीवनकाल के लिए मौजूद होता है और केवल उन entries को शामिल करता है जो client के tunnels के साथ संवाद करती हैं। यह client tunnels के नीचे भेजी गई entries को router को सीधे भेजी गई entries के साथ overlap करने से असंभव बनाता है।

इसके अतिरिक्त, प्रत्येक netDb को यह याद रखने की आवश्यकता है कि क्या कोई database entry इसलिए प्राप्त हुई थी क्योंकि यह हमारे destinations में से किसी एक को भेजी गई थी, या इसलिए कि इसे हमारे द्वारा lookup के हिस्से के रूप में अनुरोधित किया गया था। यदि कोई database entry को store के रूप में प्राप्त हुई थी, जैसे कि किसी अन्य router ने इसे हमें भेजा हो, तो netDb को उस entry के लिए अनुरोधों का उत्तर देना चाहिए जब कोई अन्य router key को खोजता है। हालांकि, यदि यह किसी query के उत्तर के रूप में प्राप्त हुई थी, तो netDb को entry के लिए query का उत्तर केवल तभी देना चाहिए जब entry पहले से ही उसी destination पर stored हो चुकी हो। एक client को कभी भी main netDb से entry के साथ queries का उत्तर नहीं देना चाहिए, केवल अपने स्वयं के client network database से।

इन रणनीतियों को लेकर संयुक्त रूप से उपयोग करना चाहिए ताकि दोनों लागू हों। संयोजन में, ये netDb को "विभाजित" करती हैं और इसे हमलों के विरुद्ध सुरक्षित करती हैं।

---

## भंडारण, सत्यापन, और खोज यंत्रविधि

### साथियों को RouterInfo भंडारण

[I2NP](/docs/specs/i2np/) DatabaseStoreMessages जिनमें स्थानीय RouterInfo होता है, peers के साथ [NTCP](/docs/specs/ntcp2/) या [SSU](/docs/specs/ssu2/) transport connection के initialization के भाग के रूप में आदान-प्रदान किया जाता है।

### LeaseSet Storage साथियों के लिए

स्थानीय LeaseSet युक्त [I2NP](/docs/specs/i2np/) DatabaseStoreMessages को संबंधित Destination से सामान्य ट्रैफिक के साथ garlic message में बंडल करके peers के साथ समय-समय पर आदान-प्रदान किया जाता है। यह किसी भी LeaseSet lookups की आवश्यकता के बिना, या संचार करने वाले Destinations को बिल्कुल भी LeaseSets प्रकाशित करने की आवश्यकता के बिना, प्रारंभिक प्रतिक्रिया और बाद की प्रतिक्रियाओं को उपयुक्त Lease पर भेजने की अनुमति देता है।

### Floodfill चयन

DatabaseStoreMessage को उस floodfill को भेजा जाना चाहिए जो संग्रहीत किए जा रहे RouterInfo या LeaseSet के लिए वर्तमान routing key के सबसे निकट है। वर्तमान में, निकटतम floodfill स्थानीय डेटाबेस में खोज द्वारा मिलता है। भले ही वह floodfill वास्तव में निकटतम न हो, यह इसे कई अन्य floodfills को भेजकर "निकट" flood करेगा। यह उच्च स्तर की fault-tolerance प्रदान करता है।

पारंपरिक Kademlia में, एक peer DHT में किसी item को निकटतम target पर insert करने से पहले "find-closest" खोज करता था। चूंकि verify operation मौजूद होने पर निकटतम floodfills को खोजने की प्रवृत्ति रखता है, एक router उन RouterInfo और LeaseSets के लिए DHT "neighborhood" की अपनी जानकारी को जल्दी से बेहतर बना लेगा जिन्हें वह नियमित रूप से प्रकाशित करता है। हालांकि I2NP "find-closest" message को परिभाषित नहीं करता, यदि यह आवश्यक हो जाता है, तो एक router बस एक key के लिए iterative खोज कर सकता है जिसका least significant bit flipped हो (यानी key ^ 0x01) तब तक जब तक DatabaseSearchReplyMessages में कोई निकटतम peers प्राप्त न हों। यह सुनिश्चित करता है कि वास्तविक निकटतम peer मिल जाएगा भले ही किसी अधिक-दूर के peer के पास netDb item हो।

### RouterInfo Storage को Floodfills में

एक router अपना RouterInfo प्रकाशित करता है floodfill router से सीधे कनेक्ट करके और उसे एक nonzero Reply Token के साथ [I2NP](/docs/specs/i2np/) DatabaseStoreMessage भेजकर। यह message end-to-end garlic encrypted नहीं है, क्योंकि यह एक प्रत्यक्ष कनेक्शन है, इसलिए कोई बीच के routers नहीं हैं (और वैसे भी इस डेटा को छुपाने की कोई आवश्यकता नहीं है)। floodfill router [I2NP](/docs/specs/i2np/) DeliveryStatusMessage के साथ उत्तर देता है, जिसमें Message ID को Reply Token के मान पर सेट किया गया होता है।

कुछ परिस्थितियों में, एक router RouterInfo DatabaseStoreMessage को एक exploratory tunnel के माध्यम से भी भेज सकता है; उदाहरण के लिए, connection सीमाओं, connection असंगति, या floodfill से वास्तविक IP छुपाने की इच्छा के कारण। floodfill ऐसे store को overload के समय या अन्य मानदंडों के आधार पर स्वीकार नहीं कर सकता है; RouterInfo के non-direct store को स्पष्ट रूप से अवैध घोषित करना है या नहीं, यह आगे के अध्ययन का विषय है।

### LeaseSet Storage to Floodfills

LeaseSets का भंडारण RouterInfos की तुलना में बहुत अधिक संवेदनशील है, क्योंकि एक router को यह सुनिश्चित करना चाहिए कि LeaseSet को router के साथ जोड़ा न जा सके।

एक router स्थानीय LeaseSet को प्रकाशित करता है उस Destination के लिए एक आउटबाउंड क्लाइंट tunnel के माध्यम से nonzero Reply Token के साथ [I2NP](/docs/specs/i2np/) DatabaseStoreMessage भेजकर। संदेश को Destination के Session Key Manager का उपयोग करके end-to-end garlic encryption से एन्क्रिप्ट किया जाता है, ताकि tunnel के आउटबाउंड endpoint से संदेश छुपाया जा सके। floodfill router [I2NP](/docs/specs/i2np/) DeliveryStatusMessage के साथ उत्तर देता है, जिसमें Message ID को Reply Token के मान पर सेट किया जाता है। यह संदेश क्लाइंट की इनबाउंड tunnels में से एक को वापस भेजा जाता है।

### फ्लडिंग

किसी भी router की तरह, एक floodfill विभिन्न मानदंडों का उपयोग करके LeaseSet या RouterInfo को स्थानीय रूप से संग्रहीत करने से पहले उसे सत्यापित करता है। ये मानदंड अनुकूली हो सकते हैं और वर्तमान परिस्थितियों पर निर्भर हो सकते हैं जिसमें वर्तमान लोड, netdb का आकार, और अन्य कारक शामिल हैं। flooding से पहले सभी सत्यापन अवश्य किया जाना चाहिए।

जब एक floodfill router को एक DatabaseStoreMessage प्राप्त होता है जिसमें एक वैध RouterInfo या LeaseSet होता है जो इसके स्थानीय NetDb में पहले से संग्रहीत की तुलना में नया होता है, तो यह इसे "floods" करता है। NetDb entry को flood करने के लिए, यह NetDb entry की routing key के सबसे निकट कई (वर्तमान में 3) floodfill routers को खोजता है। (Routing key RouterIdentity या Destination का SHA256 Hash होता है जिसमें date (yyyyMMdd) जोड़ा गया होता है।) Key के सबसे निकट flooding करके, खुद के सबसे निकट नहीं, floodfill यह सुनिश्चित करता है कि storage सही स्थान पर पहुंचे, भले ही storing router के पास routing key के लिए DHT "neighborhood" का अच्छा ज्ञान न हो।

फिर floodfill प्रत्येक उन peers से सीधे जुड़ता है और उन्हें शून्य Reply Token के साथ एक [I2NP](/docs/specs/i2np/) DatabaseStoreMessage भेजता है। यह संदेश end-to-end garlic encrypted नहीं है, क्योंकि यह एक सीधा कनेक्शन है, इसलिए कोई बीच के router नहीं हैं (और इस डेटा को छुपाने की कोई आवश्यकता भी नहीं है)। अन्य router जवाब नहीं देते या re-flood नहीं करते, क्योंकि Reply Token शून्य है।

Floodfills को tunnels के माध्यम से flood नहीं करना चाहिए; DatabaseStoreMessage को direct connection के माध्यम से भेजा जाना चाहिए।

Floodfills को कभी भी एक समाप्त हो चुके LeaseSet या एक घंटे से अधिक पुराने प्रकाशित RouterInfo को flood नहीं करना चाहिए।

### RouterInfo और LeaseSet लुकअप

[I2NP](/docs/specs/i2np/) DatabaseLookupMessage का उपयोग floodfill router से netDb entry का अनुरोध करने के लिए किया जाता है। Lookups को router की outbound exploratory tunnels में से एक के माध्यम से भेजा जाता है। Replies को router की inbound exploratory tunnels में से एक के माध्यम से वापस आने के लिए निर्दिष्ट किया जाता है।

Lookups आम तौर पर अनुरोधित key के सबसे निकट के दो "अच्छे" (कनेक्शन विफल नहीं होता) floodfill routers को समानांतर में भेजे जाते हैं।

यदि key स्थानीय रूप से floodfill router द्वारा मिल जाती है, तो यह एक [I2NP](/docs/specs/i2np/) DatabaseStoreMessage के साथ प्रतिक्रिया देता है। यदि key स्थानीय रूप से floodfill router द्वारा नहीं मिलती है, तो यह एक [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage के साथ प्रतिक्रिया देता है जिसमें key के पास के अन्य floodfill routers की सूची होती है।

LeaseSet lookups रिलीज़ 0.9.5 से garlic encrypted end-to-end हैं। RouterInfo lookups एन्क्रिप्टेड नहीं हैं और इसलिए क्लाइंट tunnel के outbound endpoint (OBEP) द्वारा snooping के लिए vulnerable हैं। यह ElGamal encryption की लागत के कारण है। RouterInfo lookup encryption भविष्य की रिलीज़ में सक्षम किया जा सकता है।

रिलीज़ 0.9.7 के अनुसार, LeaseSet lookup (एक DatabaseStoreMessage या DatabaseSearchReplyMessage) के उत्तर lookup में session key और tag शामिल करके एन्क्रिप्ट किए जाएंगे। इससे reply tunnel के inbound gateway (IBGW) से उत्तर छुप जाता है। RouterInfo lookups के responses एन्क्रिप्ट किए जाएंगे यदि हम lookup encryption को सक्षम करते हैं।

(संदर्भ: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) नीचे दिए गए इटैलिक में लिखे शब्दों के लिए धाराएं 2.2-2.3)

नेटवर्क के अपेक्षाकृत छोटे आकार और flooding redundancy के कारण, lookups आमतौर पर O(log n) के बजाय O(1) होते हैं। एक router के पास floodfill router को जानने की अत्यधिक संभावना होती है जो key के काफी करीब हो और पहली कोशिश में ही उत्तर मिल जाए। 0.8.9 से पहले के releases में, routers दो की lookup redundancy का उपयोग करते थे (यानी, दो lookups समानांतर में अलग-अलग peers को किए जाते थे), और lookups के लिए न तो *recursive* और न ही *iterative* routing implemented था। Queries को *एक साथ कई routes के माध्यम से भेजा जाता था* ताकि *query failure की संभावना को कम किया जा सके*।

रिलीज़ 0.8.9 के अनुसार, *iterative lookups* को बिना किसी lookup redundancy के साथ लागू किया गया है। यह एक अधिक कुशल और विश्वसनीय lookup है जो तब बेहतर काम करेगी जब सभी floodfill peers ज्ञात नहीं हैं, और यह network growth की एक गंभीर सीमा को हटाती है। जैसे-जैसे network बढ़ता है और प्रत्येक router केवल floodfill peers के एक छोटे subset को जानता है, lookups O(log n) हो जाएंगी। भले ही peer key के करीब references नहीं लौटाए, lookup अगले सबसे निकट peer के साथ जारी रहती है, अतिरिक्त मजबूती के लिए, और एक दुर्भावनापूर्ण floodfill को key space के एक हिस्से को black-hole करने से रोकने के लिए। Lookups तब तक जारी रहती हैं जब तक कि कुल lookup timeout नहीं पहुंच जाता, या peers की अधिकतम संख्या query नहीं हो जाती।

*Node IDs* *सत्यापनीय* होते हैं क्योंकि हम router hash का प्रत्यक्ष उपयोग node ID और Kademlia key दोनों के रूप में करते हैं। गलत प्रतिक्रियाएं जो search key के करीब नहीं हैं, आमतौर पर अनदेखी की जाती हैं। नेटवर्क के वर्तमान आकार को देखते हुए, एक router के पास *destination ID space के पड़ोस का विस्तृत ज्ञान* होता है।

### RouterInfo भंडारण सत्यापन

नोट: RouterInfo सत्यापन को रिलीज़ 0.9.7.1 से निष्क्रिय कर दिया गया है ताकि पेपर [Practical Attacks Against the I2P Network](http://wwwcip.informatik.uni-erlangen.de/~spjsschl/i2p.pdf) में वर्णित हमले को रोका जा सके। यह स्पष्ट नहीं है कि क्या सत्यापन को सुरक्षित रूप से करने के लिए फिर से डिज़ाइन किया जा सकता है।

यह सत्यापित करने के लिए कि storage सफल रहा है, एक router केवल लगभग 10 सेकंड प्रतीक्षा करता है, फिर key के करीब स्थित किसी अन्य floodfill router को lookup भेजता है (लेकिन उस router को नहीं जिसे store भेजा गया था)। Lookups को router की outbound exploratory tunnels में से किसी एक के माध्यम से भेजा जाता है। Lookups को end-to-end garlic encryption से एन्क्रिप्ट किया जाता है ताकि outbound endpoint (OBEP) द्वारा जासूसी को रोका जा सके।

### LeaseSet भंडारण सत्यापन

यह सत्यापित करने के लिए कि storage सफल रहा है, एक router बस लगभग 10 सेकंड प्रतीक्षा करता है, फिर key के पास के दूसरे floodfill router को एक lookup भेजता है (लेकिन उसे नहीं जिसे store भेजा गया था)। Lookups को उस LeaseSet के destination के लिए outbound client tunnels में से एक के माध्यम से भेजा जाता है जिसका सत्यापन किया जा रहा है। Outbound tunnel के OBEP द्वारा जासूसी को रोकने के लिए, lookups को end-to-end garlic encryption के साथ एन्क्रिप्ट किया जाता है। Replies को client के inbound tunnels में से एक के माध्यम से वापस आने के लिए निर्दिष्ट किया जाता है।

रिलीज़ 0.9.7 के अनुसार, RouterInfo और LeaseSet दोनों लुकअप के लिए उत्तर (एक DatabaseStoreMessage या DatabaseSearchReplyMessage) एन्क्रिप्ट किए जाएंगे, ताकि reply tunnel के inbound gateway (IBGW) से उत्तर को छुपाया जा सके।

### अन्वेषण

*Exploration* netdb lookup का एक विशेष रूप है, जहां एक router नए routers के बारे में जानने का प्रयास करता है। यह एक floodfill router को [I2NP](/docs/specs/i2np/) DatabaseLookup Message भेजकर ऐसा करता है, एक random key की तलाश में। चूंकि यह lookup असफल हो जाएगी, floodfill सामान्यतः [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage के साथ जवाब देगा जिसमें key के नज़दीक के floodfill routers के hashes होंगे। यह सहायक नहीं होगा, क्योंकि अनुरोध करने वाला router शायद पहले से ही उन floodfills को जानता है, और DatabaseLookup Message के "don't include" field में सभी floodfill routers को जोड़ना अव्यावहारिक होगा। एक exploration query के लिए, अनुरोध करने वाला router DatabaseLookup Message में एक विशेष flag सेट करता है। तब floodfill केवल अनुरोधित key के नज़दीक के non-floodfill routers के साथ जवाब देगा।

### लुकअप प्रतिक्रियाओं पर टिप्पणियाँ

lookup अनुरोध का प्रतिक्रिया या तो एक Database Store Message (सफलता पर) या एक Database Search Reply Message (असफलता पर) है। DSRM में प्रतिक्रिया के स्रोत को दर्शाने के लिए एक 'from' router hash फील्ड होता है; DSM में नहीं होता। DSRM 'from' फील्ड असत्यापित है और इसे नकली या अमान्य बनाया जा सकता है। कोई अन्य प्रतिक्रिया टैग नहीं हैं। इसलिए, समानांतर में कई अनुरोध करते समय, विभिन्न floodfill routers के प्रदर्शन की निगरानी करना कठिन है।

---

## MultiHoming

गंतव्य एक साथ कई routers पर hosted हो सकते हैं, समान private और public keys का उपयोग करके (पारंपरिक रूप से eepPriv.dat फ़ाइलों में संग्रहीत)। चूंकि दोनों instances समय-समय पर अपने signed LeaseSets को floodfill peers पर प्रकाशित करेंगे, database lookup का अनुरोध करने वाले peer को सबसे हाल ही में प्रकाशित LeaseSet वापस किया जाएगा। जैसा कि LeaseSets का (अधिकतम) 10 मिनट का जीवनकाल होता है, यदि कोई विशेष instance down हो जाता है, तो outage अधिकतम 10 मिनट का होगा, और आमतौर पर उससे बहुत कम। multihoming function सत्यापित हो चुका है और नेटवर्क पर कई सेवाओं द्वारा उपयोग में है।

रिलीज़ 0.9.38 के अनुसार, floodfills एक नई Meta LeaseSet संरचना का समर्थन करते हैं। यह संरचना DHT में एक ट्री-जैसी संरचना प्रदान करती है, जो अन्य LeaseSets का संदर्भ देने के लिए होती है। Meta LeaseSets का उपयोग करके, एक साइट बड़ी multihomed सेवाएं लागू कर सकती है, जहां एक सामान्य सेवा प्रदान करने के लिए कई अलग-अलग Destinations का उपयोग किया जाता है। Meta LeaseSet में entries Destinations या अन्य Meta LeaseSets होती हैं, और इनकी लंबी expirations हो सकती हैं, 18.2 घंटे तक। इस सुविधा का उपयोग करके, एक सामान्य सेवा की hosting करने वाले सैकड़ों या हज़ारों Destinations चलाना संभव होना चाहिए। विवरण के लिए proposal 123 देखें।

---

## खतरा विश्लेषण

[threat model पेज](/docs/overview/threat-model/#floodfill) पर भी चर्चा की गई है।

एक शत्रुतापूर्ण उपयोगकर्ता नेटवर्क को नुकसान पहुंचाने का प्रयास कर सकता है एक या अधिक floodfill router बनाकर और उन्हें खराब, धीमे, या कोई प्रतिक्रिया न देने के लिए तैयार करके। कुछ परिस्थितियों की चर्चा नीचे की गई है।

### वृद्धि के माध्यम से सामान्य शमन

वर्तमान में नेटवर्क में लगभग 1700 floodfill router हैं। निम्नलिखित में से अधिकांश हमले अधिक कठिन हो जाएंगे, या उनका प्रभाव कम होगा, जैसे-जैसे नेटवर्क का आकार और floodfill router की संख्या बढ़ेगी।

### रिडंडेंसी के माध्यम से सामान्य शमन

फ्लडिंग के माध्यम से, सभी netdb एंट्रियां उस key के सबसे निकटतम 3 floodfill routers पर संग्रहीत होती हैं।

### जालसाजी

सभी netdb entries उनके निर्माताओं द्वारा signed हैं, इसलिए कोई भी router किसी RouterInfo या LeaseSet को forge नहीं कर सकता।

### धीमा या गैर-उत्तरदायी

प्रत्येक router प्रत्येक floodfill router के लिए [peer profile](/docs/overview/peer-selection/) में आँकड़ों का एक विस्तृत सेट बनाए रखता है, जो उस peer के लिए विभिन्न गुणवत्ता मेट्रिक्स को कवर करता है। इस सेट में शामिल है:

- औसत प्रतिक्रिया समय
- अनुरोधित डेटा के साथ उत्तर दी गई क्वेरीज़ का प्रतिशत
- सफलतापूर्वक सत्यापित stores का प्रतिशत
- अंतिम सफल store
- अंतिम सफल lookup
- अंतिम प्रतिक्रिया

जब भी किसी router को यह निर्धारित करना होता है कि कौन सा floodfill router किसी key के सबसे निकट है, तो वह इन मेट्रिक्स का उपयोग करके यह तय करता है कि कौन से floodfill router "अच्छे" हैं। "अच्छाई" निर्धारित करने के लिए उपयोग की जाने वाली विधियां और सीमाएं अपेक्षाकृत नई हैं, और आगे के विश्लेषण और सुधार के अधीन हैं। जबकि पूर्णतः गैर-प्रतिक्रियाशील router को जल्दी पहचान लिया जाएगा और उससे बचा जाएगा, केवल कभी-कभी दुर्भावनापूर्ण व्यवहार करने वाले router से निपटना बहुत कठिन हो सकता है।

### सिबिल अटैक (पूर्ण कीस्पेस)

एक आक्रमणकारी keyspace में फैले हुए बड़ी संख्या में floodfill routers बनाकर [Sybil attack](https://www.freehaven.net/anonbib/cache/sybil.pdf) कर सकता है।

(एक संबंधित उदाहरण में, एक शोधकर्ता ने हाल ही में [बड़ी संख्या में Tor relays](http://blog.torproject.org/blog/june-2010-progress-report) बनाए थे।) यदि सफल हो जाए, तो यह पूरे नेटवर्क पर एक प्रभावी DOS हमला हो सकता है।

यदि floodfills उपरोक्त वर्णित peer profile मेट्रिक्स का उपयोग करके "bad" के रूप में चिह्नित किए जाने के लिए पर्याप्त रूप से दुर्व्यवहार नहीं कर रहे हैं, तो यह एक कठिन स्थिति है जिसे संभालना मुश्किल है। Tor की प्रतिक्रिया relay के मामले में अधिक फुर्तीली हो सकती है, क्योंकि संदिग्ध relays को consensus से मैन्युअल रूप से हटाया जा सकता है। I2P नेटवर्क के लिए कुछ संभावित प्रतिक्रियाएं नीचे सूचीबद्ध हैं, हालांकि उनमें से कोई भी पूर्णतः संतोषजनक नहीं है:

- खराब router hash या IP की एक सूची तैयार करें, और विभिन्न माध्यमों से इस सूची की घोषणा करें (console news, website, forum, आदि); उपयोगकर्ताओं को मैन्युअल रूप से सूची डाउनलोड करनी होगी और इसे अपनी स्थानीय "blacklist" में जोड़ना होगा।
- network में सभी से कहें कि वे मैन्युअल रूप से floodfill को सक्षम करें (अधिक Sybil के साथ Sybil से लड़ें)
- एक नया software version जारी करें जिसमें hardcoded "खराब" सूची शामिल हो
- एक नया software version जारी करें जो peer profile मेट्रिक्स और thresholds में सुधार करता है, "खराब" peers को स्वचालित रूप से पहचानने के प्रयास में।
- ऐसा software जोड़ें जो floodfills को अयोग्य घोषित कर दे यदि उनमें से बहुत सारे एक ही IP block में हैं
- एक स्वचालित subscription-आधारित blacklist लागू करें जो किसी एक व्यक्ति या समूह द्वारा नियंत्रित हो। यह मूल रूप से Tor "consensus" मॉडल का एक हिस्सा लागू करेगा। दुर्भाग्य से यह एक व्यक्ति या समूह को network में किसी भी विशेष router या IP की भागीदारी को block करने की शक्ति देगा, या यहाँ तक कि पूरे network को पूरी तरह से shutdown या नष्ट करने की भी।

जैसे-जैसे नेटवर्क का आकार बढ़ता है, यह हमला अधिक कठिन हो जाता है।

### Sybil Attack (आंशिक कीस्पेस)

एक हमलावर [Sybil attack](https://www.freehaven.net/anonbib/cache/sybil.pdf) कर सकता है keyspace में निकट स्थित कम संख्या (8-15) के floodfill routers बनाकर, और इन routers के RouterInfos को व्यापक रूप से वितरित करके। तब, उस keyspace में किसी key के लिए सभी lookups और stores हमलावर के routers में से किसी एक पर भेज दिए जाएंगे। यदि सफल हो जाए, तो यह उदाहरण के लिए किसी विशेष I2P Site पर एक प्रभावी DOS attack हो सकता है।

चूंकि keyspace को key के cryptographic (SHA256) Hash द्वारा indexed किया जाता है, एक attacker को brute-force method का उपयोग करना होगा और बार-बार router hashes generate करने होंगे जब तक कि उसके पास पर्याप्त hashes न हों जो key के काफी करीब हों। इसके लिए आवश्यक computational power की मात्रा, जो network size पर निर्भर है, अज्ञात है।

इस हमले के विरुद्ध आंशिक सुरक्षा के रूप में, Kademlia "निकटता" निर्धारित करने के लिए उपयोग किया जाने वाला एल्गोरिदम समय के साथ बदलता रहता है। निकटता निर्धारित करने के लिए key के Hash (अर्थात् H(k)) का उपयोग करने के बजाय, हम key को वर्तमान दिनांक स्ट्रिंग के साथ जोड़कर Hash का उपयोग करते हैं, अर्थात् H(k + YYYYMMDD)। "routing key generator" नामक एक फ़ंक्शन यह काम करता है, जो मूल key को "routing key" में रूपांतरित करता है। दूसरे शब्दों में, संपूर्ण netDb keyspace प्रतिदिन UTC मध्यरात्रि में "घूमता" है। किसी भी आंशिक-keyspace हमले को प्रतिदिन पुनर्जनित करना होगा, क्योंकि rotation के बाद, आक्रमणकारी router अब target key के करीब नहीं होंगे, या एक-दूसरे के करीब नहीं होंगे।

यह हमला नेटवर्क के आकार बढ़ने के साथ और कठिन हो जाता है। हालांकि, हाल की रिसर्च दर्शाती है कि keyspace rotation विशेष रूप से प्रभावी नहीं है। एक हमलावर पहले से ही कई router hashes की गणना कर सकता है, और rotation के बाद आधे घंटे के भीतर keyspace के एक हिस्से को "eclipse" करने के लिए केवल कुछ routers ही पर्याप्त हैं।

दैनिक keyspace rotation का एक परिणाम यह है कि distributed network database rotation के बाद कुछ मिनटों के लिए अविश्वसनीय हो सकता है -- lookups विफल हो जाएंगे क्योंकि नए "निकटतम" router को अभी तक store प्राप्त नहीं हुआ है। इस समस्या की सीमा, और शमन के तरीके (उदाहरण के लिए आधी रात को netDb "handoffs") आगे के अध्ययन का विषय हैं।

### Bootstrap हमले

एक आक्रमणकारी reseed वेबसाइट पर नियंत्रण करके, या डेवलपर्स को धोखा देकर अपनी reseed वेबसाइट को router की hardcoded सूची में जोड़वाकर नए routers को एक अलग या बहुमत-नियंत्रित नेटवर्क में boot करने का प्रयास कर सकता है।

कई सुरक्षा उपाय संभव हैं, और इनमें से अधिकांश की योजना बनाई गई है:

- reseeding के लिए HTTPS से HTTP में fallback को अनुमति न दें। एक MITM attacker आसानी से HTTPS को block कर सकता है, फिर HTTP का जवाब दे सकता है।
- installer में reseed data को bundle करना

जो सुरक्षा उपाय लागू किए गए हैं:

- प्रत्येक reseed कार्य को केवल एक ही साइट का उपयोग करने के बजाय कई reseed साइटों से RouterInfos का एक उपसमुच्चय प्राप्त करने के लिए बदलना
- एक आउट-ऑफ-नेटवर्क reseed निगरानी सेवा बनाना जो नियमित रूप से reseed वेबसाइटों को पोल करती है और सत्यापित करती है कि डेटा बासी नहीं है या नेटवर्क के अन्य दृश्यों के साथ असंगत नहीं है
- रिलीज़ 0.9.14 के अनुसार, reseed डेटा को एक हस्ताक्षरित zip फ़ाइल में बंडल किया जाता है और डाउनलोड करते समय हस्ताक्षर की पुष्टि की जाती है। विवरण के लिए [su3 विनिर्देश](/docs/specs/updates/#su3) देखें।

### क्वेरी कैप्चर

यह भी देखें [lookup](#routerinfo-and-leaseset-lookup) (संदर्भ: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) नीचे दिए गए तिर्यक शब्दों के लिए धारा 2.2-2.3)

bootstrap हमले के समान, एक floodfill router का उपयोग करने वाला हमलावर अपने द्वारा नियंत्रित routers के subset की references वापस करके peers को उन तक "steer" करने का प्रयास कर सकता है।

यह exploration के माध्यम से काम करने की संभावना नहीं है, क्योंकि exploration एक कम-आवृत्ति का कार्य है। Router अपने अधिकांश peer references सामान्य tunnel निर्माण गतिविधि के माध्यम से प्राप्त करते हैं। Exploration परिणाम आमतौर पर कुछ router hash तक सीमित होते हैं, और प्रत्येक exploration query एक यादृच्छिक floodfill router को निर्देशित की जाती है।

रिलीज़ 0.8.9 से, *iterative lookups* लागू किए गए हैं। lookup के लिए [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage response में वापस किए गए floodfill router references के लिए, यदि वे lookup key के करीब हैं (या अगले सबसे करीब हैं) तो इन references का पालन किया जाता है। अनुरोधकर्ता router इस पर भरोसा नहीं करता कि references key के करीब हैं (यानी वे *verifiably correct* हैं)। lookup तब भी नहीं रुकता जब कोई करीबी key नहीं मिलती, बल्कि अगले सबसे करीब के node को query करके जारी रहता है, जब तक timeout या अधिकतम queries की संख्या नहीं पहुँच जाती। यह एक malicious floodfill को key space के हिस्से को black-hole करने से रोकता है। साथ ही, दैनिक keyspace rotation के लिए एक attacker को वांछित key space क्षेत्र के भीतर एक router info को पुनः generate करना आवश्यक होता है। यह design सुनिश्चित करता है कि [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) में वर्णित query capture attack बहुत अधिक कठिन है।

### DHT-आधारित रिले चयन

(संदर्भ: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Section 3)

इसका floodfill से बहुत अधिक संबंध नहीं है, लेकिन tunnels के लिए peer selection की कमजोरियों की चर्चा के लिए [peer selection page](/docs/overview/peer-selection/) देखें।

### सूचना रिसाव

(संदर्भ: [In Search of an Anonymous and Secure Lookup](https://www.freehaven.net/anonbib/cache/ccs10-lookup.pdf) Section 3)

यह पेपर Torsk और NISAN द्वारा उपयोग किए जाने वाले "Finger Table" DHT lookups की कमजोरियों को संबोधित करता है। पहली नजर में, ये I2P पर लागू नहीं होते दिखते। पहला, Torsk और NISAN द्वारा DHT का उपयोग I2P में उससे काफी अलग है। दूसरा, I2P के network database lookups का [peer selection](/docs/overview/peer-selection/) और [tunnel building](/docs/overview/tunnel-routing/) प्रक्रियाओं से केवल शिथिल संबंध है; tunnels के लिए केवल पहले से ज्ञात peers का उपयोग किया जाता है। इसके अलावा, peer selection का DHT key-closeness की किसी भी धारणा से कोई संबंध नहीं है।

इसमें से कुछ वास्तव में तब और दिलचस्प हो सकता है जब I2P network बहुत बड़ा हो जाए। अभी, प्रत्येक router network के एक बड़े हिस्से को जानता है, इसलिए network database में किसी विशेष Router Info को देखना भविष्य में उस router को tunnel में उपयोग करने के इरादे का मजबूत संकेत नहीं देता। शायद जब network 100 गुना बड़ा हो जाए, तो lookup अधिक सहसंबंधी हो सकता है। बेशक, एक बड़ा network Sybil attack को बहुत कठिन बना देता है।

हालांकि, I2P में DHT जानकारी लीकेज की सामान्य समस्या पर और अधिक जांच की आवश्यकता है। floodfill router ऐसी स्थिति में हैं कि वे queries को देख सकते हैं और जानकारी एकत्र कर सकते हैं। निश्चित रूप से, *f* = 0.2 के स्तर पर (20% दुर्भावनापूर्ण nodes, जैसा कि पेपर में निर्दिष्ट है) हम उम्मीद करते हैं कि कई Sybil खतरे जिनका हमने वर्णन किया है ([यहाँ](/docs/overview/threat-model/#sybil), [यहाँ](#sybil-attack-full-keyspace) और [यहाँ](#sybil-attack-partial-keyspace)) कई कारणों से समस्याजनक हो जाते हैं।

---

## इतिहास

[netdb चर्चा पृष्ठ पर स्थानांतरित](/docs/legacy/netdb/)।

---

## भविष्य का कार्य

अतिरिक्त netDb lookups और responses का end-to-end एन्क्रिप्शन।

lookup responses को ट्रैक करने के लिए बेहतर तरीके।
