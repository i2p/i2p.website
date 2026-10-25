---
title: "नेटवर्क डेटाबेस चर्चा"
description: "netDb के लिए floodfill, Kademlia प्रयोगों और भविष्य की tuning पर ऐतिहासिक नोट्स"
slug: "netdb"
aliases:
  - "/hi/docs/legacy/netdb"
  - "/hi/docs/legacy/netdb/"
  - "/hi/netdb_discussion"
  - "/hi/netdb_discussion/"
lastUpdated: "2008-03"
accurateFor: "0.7"
---

नोट: निम्नलिखित netdb implementation के इतिहास की चर्चा है और यह वर्तमान जानकारी नहीं है। वर्तमान प्रलेखन के लिए [मुख्य netdb पेज](/docs/overview/network-database) देखें।

## इतिहास {#status}

netDb को "floodfill" नामक एक सरल तकनीक के साथ वितरित किया जाता है। बहुत समय पहले, netDb भी Kademlia DHT को एक fallback algorithm के रूप में उपयोग करता था। हालांकि, यह हमारे application में अच्छी तरह से काम नहीं करता था, और इसे release 0.6.1.20 में पूरी तरह से disable कर दिया गया था।

*(पुराने Syndie में jrandom की एक पोस्ट से रूपांतरित, 26 नवंबर, 2005)*

floodfill netDb वास्तव में केवल एक सरल और शायद अस्थायी उपाय है, जो सबसे सरल संभावित एल्गोरिदम का उपयोग करता है - floodfill netDb में किसी peer को डेटा भेजना, 10 सेकंड इंतजार करना, netDb में किसी यादृच्छिक peer को चुनना और उनसे भेजी जाने वाली entry के लिए पूछना, इसके उचित insertion / distribution को सत्यापित करना। यदि सत्यापन peer उत्तर नहीं देता, या उनके पास entry नहीं है, तो sender प्रक्रिया को दोहराता है। जब floodfill netDb में कोई peer को floodfill netDb में न होने वाले किसी peer से netDb store प्राप्त होता है, तो वे इसे floodfill netDb के सभी peers को भेज देते हैं।

एक समय पर, Kademlia search/store कार्यक्षमता अभी भी मौजूद थी। peers ने floodfill peers को हमेशा हर key के लिए netDb में भाग न लेने वाले किसी भी peer की तुलना में 'closer' माना। यदि floodfill peers किसी कारण से विफल हो जाते हैं तो हम Kademlia netDb पर वापस लौट जाते हैं। हालांकि, Kademlia को फिर पूरी तरह से disable कर दिया गया (नीचे देखें)।

हाल ही में, Kademlia को 2009 के अंत में आंशिक रूप से फिर से शामिल किया गया था, ताकि प्रत्येक floodfill router द्वारा संग्रहीत किए जाने वाले netdb के आकार को सीमित किया जा सके।

### Floodfill Algorithm का परिचय

Floodfill को रिलीज़ 0.6.0.4 में पेश किया गया था, जिसमें Kademlia को बैकअप एल्गोरिदम के रूप में रखा गया।

*(पुराने Syndie में jrandom की पोस्ट से रूपांतरित, 26 नवंबर, 2005)*

जैसा कि मैंने अक्सर कहा है, मैं किसी विशिष्ट तकनीक से विशेष रूप से बंधा नहीं हूं - मेरे लिए जो मायने रखता है वह यह है कि क्या परिणाम मिलेगा। जबकि मैं पिछले कुछ वर्षों में विभिन्न netDb विचारों पर काम कर रहा हूं, पिछले कुछ हफ्तों में हमने जिन समस्याओं का सामना किया है, उन्होंने इनमें से कुछ को चरम पर पहुंचा दिया है। लाइव नेट पर, netDb redundancy factor को 4 peers पर सेट करके (मतलब हम एक entry को तब तक नए peers को भेजते रहते हैं जब तक कि उनमें से 4 confirm नहीं कर देते कि उन्हें मिल गया है) और per-peer timeout को उस peer के औसत reply time के 4 गुना पर सेट करके, हमें **अभी भी** 4 के ACK करने से पहले औसतन 40-60 peers को भेजना पड़ता है। इसका मतलब है कि जितने messages भेजे जाने चाहिए उससे 36-56 गुना ज्यादा messages भेजना, जिसमें से हर एक tunnels का उपयोग करता है और इससे 2-4 links पार करता है। इससे भी आगे, यह value काफी skewed है, क्योंकि एक 'failed' store में peers की औसत संख्या (मतलब 60 सेकंड तक messages भेजने के बाद 4 से कम लोगों ने message को ACK किया) 130-160 peers की range में थी।

यह पागलपन है, खासकर एक ऐसे network के लिए जिसमें शायद केवल 250 peers हैं।

सबसे सरल उत्तर यह कहना है "अरे jrandom, यह टूटा हुआ है। इसे ठीक करो", लेकिन यह मुद्दे के मूल तक नहीं पहुंचता। एक अन्य वर्तमान प्रयास के अनुरूप, संभावना है कि हमारे पास प्रतिबंधित routes के कारण काफी संख्या में network समस्याएं हैं - ऐसे peers जो कुछ अन्य peers के साथ बात नहीं कर सकते, अक्सर NAT या firewall मुद्दों के कारण। यदि, मान लें, किसी विशेष netDb entry के सबसे नजदीकी K peers एक 'प्रतिबंधित route' के पीछे हैं जैसे कि netDb store message उन तक पहुंच सकता है लेकिन किसी अन्य peer का netDb lookup message नहीं पहुंच सकता, तो वह entry अनिवार्य रूप से पहुंच से बाहर हो जाएगी। इन बातों को थोड़ा और आगे बढ़ाते हुए और इस तथ्य को ध्यान में रखते हुए कि कुछ प्रतिबंधित routes शत्रुतापूर्ण इरादे से बनाए जाएंगे, यह स्पष्ट है कि हमें दीर्घकालिक netDb समाधान पर अधिक गौर से देखना होगा।

कुछ विकल्प हैं, लेकिन विशेष रूप से दो का उल्लेख करना उचित है। पहला यह है कि netDb को बस एक Kademlia DHT के रूप में पूरे नेटवर्क के एक उपसमुच्चय का उपयोग करके चलाना, जहां वे सभी peers बाहरी रूप से पहुंच योग्य हों। जो peers netDb में भाग नहीं ले रहे हैं, वे अभी भी उन peers से query करते हैं लेकिन उन्हें अवांछित netDb store या lookup संदेश प्राप्त नहीं होते। netDb में भागीदारी स्व-चयन और उपयोगकर्ता-निष्कासन दोनों होगी - routers चुनेंगे कि वे अपने routerInfo में एक flag प्रकाशित करना चाहते हैं या नहीं जो बताता है कि वे भाग लेना चाहते हैं, जबकि प्रत्येक router चुनता है कि वह किन peers को netDb का हिस्सा मानना चाहता है (जो peers उस flag को प्रकाशित करते हैं लेकिन कभी कोई उपयोगी डेटा नहीं देते, उन्हें नज़रअंदाज़ कर दिया जाएगा, वास्तव में उन्हें netDb से हटा दिया जाएगा)।

एक और विकल्प अतीत की एक झलक है, DTSTTCPW (Do The Simplest Thing That Could Possibly Work) मानसिकता पर वापस जाना - एक floodfill netDb, लेकिन उपरोक्त विकल्प की तरह, केवल पूर्ण नेटवर्क के एक हिस्से का उपयोग करना। जब कोई उपयोगकर्ता floodfill netDb में कोई entry प्रकाशित करना चाहता है, तो वे बस इसे भाग लेने वाले routers में से किसी एक को भेजते हैं, ACK की प्रतीक्षा करते हैं, और फिर 30 सेकंड बाद, floodfill netDb में किसी अन्य यादृच्छिक प्रतिभागी से पूछताछ करके यह सत्यापित करते हैं कि यह उचित रूप से वितरित हुई थी। यदि हुई थी, तो बहुत अच्छा, और यदि नहीं, तो बस प्रक्रिया को दोहराएं। जब एक floodfill router को netDb store प्राप्त होता है, तो वे तुरंत ACK करते हैं और netDb store को अपने सभी ज्ञात netDb peers को queue off करते हैं। जब एक floodfill router को netDb lookup प्राप्त होता है, यदि उनके पास डेटा है, तो वे इसके साथ उत्तर देते हैं, लेकिन यदि उनके पास नहीं है, तो वे floodfill netDb में, मान लेते हैं, 20 अन्य peers के लिए hashes के साथ उत्तर देते हैं।

इसे नेटवर्क अर्थशास्त्र के दृष्टिकोण से देखते हुए, floodfill netDb मूल broadcast netDb के काफी समान है, सिवाय इसके कि एक entry को publish करने की लागत मुख्यतः netDb के peers द्वारा वहन की जाती है, publisher द्वारा नहीं। इसे थोड़ा और विस्तार से समझाते हुए और netDb को एक blackbox की तरह मानते हुए, हम देख सकते हैं कि netDb द्वारा आवश्यक कुल bandwidth है:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
जहाँ:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
कुछ मान भरने पर:

```
recvKBps = 1000 * (5 + 1) * (1 + 0.05) * (1 + 0.2) * 2KB / 10m
         = 25.2KBps
```
यह, बदले में, N के साथ रैखिक रूप से बढ़ता है (100,000 peers पर, netDb को कुल 2.5MBps के netDb store messages को संभालने में सक्षम होना चाहिए, या, 300 peers पर, 7.6KBps)।

जबकि floodfill netDb में प्रत्येक netDb प्रतिभागी को क्लाइंट द्वारा उत्पन्न netDb stores का केवल एक छोटा सा हिस्सा सीधे प्राप्त होगा, उन सभी को अंततः सभी entries प्राप्त हो जाएंगी, इसलिए उनके सभी links में पूरी recvKBps को संभालने की क्षमता होनी चाहिए। बदले में, अन्य peers को sync में रखने के लिए उन सभी को `(recvKBps/sizeof(netDb)) * (sizeof(netDb)-1)` भेजना होगा।

एक floodfill netDb को netDb ऑपरेशन के लिए tunnel routing या किसी विशेष selection की आवश्यकता नहीं होगी कि वह कौन से entries का 'safely' उत्तर दे सकता है, क्योंकि मूल धारणा यह है कि वे सभी सब कुछ store कर रहे हैं। ओह, और netDb disk usage की आवश्यकता के संबंध में, यह अभी भी किसी भी आधुनिक machine के लिए काफी तुच्छ है, प्रत्येक 1000 peers के लिए लगभग 11MB की आवश्यकता होती है `(N * (L + 1) * S)`।

Kademlia netDb इन संख्याओं को कम कर देगा, आदर्श रूप से उन्हें K गुना M से विभाजित करके लाएगा, जहाँ K = redundancy factor है और M netDb में routers की संख्या है (जैसे 5/100, जो 100,000 routers पर 126KBps का recvKBps और 536MB देता है)। हालांकि Kademlia netDb का नकारात्मक पहलू प्रतिकूल वातावरण में सुरक्षित संचालन की बढ़ी हुई जटिलता है।

अब मैं जिसके बारे में सोच रहा हूं वह यह है कि हमारे मौजूदा live network में एक floodfill netDb को सरल रूप से implement और deploy करना है, उन peers को जो इसका उपयोग करना चाहते हैं, अन्य peers को चुनने देना है जो members के रूप में flagged हैं और पारंपरिक Kademlia netDb peers को query करने के बजाय उनसे query करना है। इस स्तर पर bandwidth और disk की आवश्यकताएं काफी तुच्छ हैं (7.6KBps और 3MB disk space) और यह debugging plan से netDb को पूरी तरह हटा देगा - जो समस्याएं अभी भी संबोधित की जानी हैं वे netDb से असंबंधित किसी चीज़ के कारण होंगी।

peers को यह flag publish करने के लिए कैसे चुना जाएगा कि वे floodfill netDb का हिस्सा हैं? शुरुआत में, इसे एक advanced config option के रूप में manually किया जा सकता है (अगर router अपनी external reachability verify नहीं कर सकता तो ignore कर दिया जाएगा)। अगर बहुत सारे peers यह flag set करते हैं, तो netDb participants कैसे चुनते हैं कि किन्हें eject करना है? फिर से, शुरुआत में इसे एक advanced config option के रूप में manually किया जा सकता है (उन peers को drop करने के बाद जो unreachable हैं)। हम netDb partitioning से कैसे बचते हैं? routers को यह verify करवाकर कि netDb flood fill ठीक से कर रहा है, K random netDb peers को query करके। वे routers जो netDb में participate नहीं कर रहे, tunnel के लिए नए routers कैसे discover करते हैं? शायद यह एक particular netDb lookup भेजकर किया जा सकता है ताकि netDb router netDb में peers के साथ respond न करे, बल्कि netDb के बाहर के random peers के साथ respond करे।

I2P का netDb पारंपरिक लोड बेयरिंग DHTs से बहुत अलग है - यह केवल नेटवर्क metadata को ले जाता है, कोई वास्तविक payload नहीं, यही कारण है कि floodfill algorithm का उपयोग करने वाला netDb भी I2P Site/IRC/bt/mail/syndie/आदि डेटा की मनमानी मात्रा को बनाए रख सकता है। जैसे-जैसे I2P बढ़ता है, हम उस लोड को थोड़ा और वितरित करने के लिए कुछ अनुकूलन भी कर सकते हैं (संभवतः netDb प्रतिभागियों के बीच bloom filters पास करके यह देखने के लिए कि उन्हें क्या साझा करने की आवश्यकता है), लेकिन लगता है कि हम अभी के लिए एक बहुत सरल समाधान के साथ काम चला सकते हैं।

एक तथ्य पर गौर करना उपयोगी हो सकता है - सभी leaseSets को netDb में प्रकाशित करने की आवश्यकता नहीं है! वास्तव में, अधिकांश को इसकी आवश्यकता नहीं होती - केवल उन destinations के लिए जो अवांछित संदेश प्राप्त करेंगे (यानी servers)। ऐसा इसलिए है क्योंकि एक destination से दूसरे में भेजे जाने वाले garlic wrapped संदेशों में पहले से ही भेजने वाले का leaseSet शामिल होता है ताकि उन दो destinations के बीच कोई भी बाद की send/recv (कम समय अवधि के भीतर) बिना किसी netDb गतिविधि के काम कर सके।

तो, उन समीकरणों पर वापस जाते हुए, हम L को 5 से बदलकर 0.1 जैसा कुछ कर सकते हैं (यह मानते हुए कि हर 50 गंतव्यों में से केवल 1 एक server है)। पिछली समीकरणों ने clients के queries का उत्तर देने के लिए आवश्यक network load को भी नज़रअंदाज़ किया था, लेकिन जबकि यह अत्यधिक परिवर्तनशील है (user गतिविधि के आधार पर), यह publishing frequency की तुलना में काफी नगण्य होने की भी संभावना है।

वैसे भी, अभी भी कोई जादू नहीं है, लेकिन आवश्यक bandwidth/disk space में लगभग 1/5वें की अच्छी कमी है (शायद बाद में और भी अधिक, इस बात पर निर्भर करते हुए कि routerInfo distribution peer establishment के हिस्से के रूप में सीधे जाता है या केवल netDb के माध्यम से)।

### Kademlia Algorithm का निष्क्रियकरण

Kademlia को रिलीज़ 0.6.1.20 में पूर्णतः निष्क्रिय कर दिया गया था।

*(jrandom के साथ 11/07 की IRC बातचीत से रूपांतरित)*

Kademlia को सेवा के एक न्यूनतम स्तर की आवश्यकता होती है जो baseline प्रदान नहीं कर सकता था (bandwidth, cpu), यहाँ तक कि tiers जोड़ने के बाद भी (शुद्ध kad उस बिंदु पर बेतुका है)। Kademlia बस काम नहीं करता। यह एक अच्छा विचार था, लेकिन एक शत्रुतापूर्ण और तरल वातावरण के लिए नहीं।

### वर्तमान स्थिति

netDb I2P नेटवर्क में एक बहुत विशिष्ट भूमिका निभाता है, और algorithms को हमारी आवश्यकताओं के अनुसार tuned किया गया है। इसका मतलब यह भी है कि इसे उन जरूरतों के लिए tuned नहीं किया गया है जिनका हमें अभी तक सामना नहीं करना पड़ा है। I2P वर्तमान में काफी छोटा है (कुछ सौ routers)। कुछ गणनाओं के अनुसार 3-5 floodfill routers नेटवर्क में 10,000 nodes को handle करने में सक्षम होने चाहिए। netDb implementation वर्तमान में हमारी जरूरतों को पूर्ण रूप से पूरा करता है, लेकिन जैसे-जैसे नेटवर्क बढ़ेगा, संभवतः और tuning और bugfixing की आवश्यकता होगी।

### गणनाओं का अपडेट 03-2008

वर्तमान संख्याएं:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
जहाँ:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
मान्यताओं में परिवर्तन:

- L अब लगभग .5 है, ऊपर दिए गए .1 की तुलना में, i2psnark और अन्य ऐप्स की लोकप्रियता के कारण।
- F लगभग .33 है, लेकिन tunnel testing में bugs 0.6.1.33 में ठीक किए गए हैं, इसलिए यह बहुत बेहतर हो जाएगा।
- चूंकि netDb लगभग 2/3 5K routerInfos और 1/3 2K leaseSets है, इसलिए S = 4K है।
  RouterInfo का साइज़ 0.6.1.32 और 0.6.1.33 में घट रहा है क्योंकि हम अनावश्यक stats को हटा रहे हैं।
- R = tunnel build period: 0.2 बहुत कम था - यह शायद 0.7 था -
  लेकिन 0.6.1.32 में build algorithm सुधार इसे लगभग 0.2 तक लाना चाहिए
  जैसे-जैसे network अपग्रेड होता है। इसे अभी 0.5 कहते हैं जब आधा network .30 या उससे पहले के version पर है।

```
recvKBps = 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4KB / 10m
         ~= 28KBps
```
यह केवल stores के लिए हिसाब रखता है - queries के बारे में क्या?

### Kademlia एल्गोरिदम की वापसी?

*(I2P मीटिंग 2 जनवरी, 2007 से रूपांतरित)*

Kademlia netDb बस ठीक से काम नहीं कर रहा था। क्या यह हमेशा के लिए मर गया है या यह वापस आएगा? यदि यह वापस आता है, तो Kademlia netDb में peers नेटवर्क में routers का एक बहुत ही सीमित उपसमूह होंगे (मूल रूप से floodfill peers की एक विस्तृत संख्या, यदि/जब floodfill peers लोड को संभाल नहीं सकते)। लेकिन जब तक floodfill peers लोड को संभाल नहीं सकते (और अन्य peers जो संभाल सकते हों वे जोड़े नहीं जा सकते), तब तक यह अनावश्यक है।

### Floodfill का भविष्य

*(jrandom के साथ 11/07 की IRC बातचीत से रूपांतरित)*

यहाँ एक प्रस्ताव है: Capacity class O स्वचालित रूप से floodfill है। हम्म। जब तक हमें यकीन न हो, हम सभी O class routers को DDoS करने का एक फैंसी तरीका बना सकते हैं। यह काफी मामला है: हम यह सुनिश्चित करना चाहते हैं कि floodfill की संख्या यथासंभव कम हो जबकि पर्याप्त पहुंच प्रदान करे। यदि/जब netDb अनुरोध विफल होते हैं, तो हमें floodfill peers की संख्या बढ़ाने की आवश्यकता है, लेकिन अभी, मैं netDb fetch समस्या के बारे में जानकारी में नहीं हूँ। मेरे रिकॉर्ड के अनुसार 33 "O" class peers हैं। 33 floodfill के लिए /बहुत/ है।

तो floodfill तब सबसे अच्छा काम करता है जब उस pool में peers की संख्या कड़ाई से सीमित हो? और floodfill pool का आकार ज्यादा नहीं बढ़ना चाहिए, भले ही network खुद धीरे-धीरे बढ़े? 3-5 floodfill peers 10K routers को handle कर सकते हैं iirc (मैंने पुराने syndie में विवरण समझाने वाले कई नंबर पोस्ट किए थे)। automatic opt-in के साथ यह एक कठिन requirement लगती है, खासकर यदि opt-in करने वाले nodes दूसरों के data पर भरोसा नहीं कर सकते। जैसे "देखते हैं कि क्या मैं top 5 में हूँ", और केवल अपने बारे में data पर भरोसा कर सकते हैं (जैसे "मैं निश्चित रूप से O class हूँ, और 150 KB/s move कर रहा हूँ, और 123 दिनों से up हूँ")। और top 5 भी hostile है। मूल रूप से, यह tor directory servers के समान है - trusted लोगों (यानी devs) द्वारा चुने गए। हाँ, अभी यह opt-in द्वारा exploit हो सकता है, लेकिन इसे detect और deal करना trivial होगा। लगता है कि अंत में, हमें Kademlia से कुछ अधिक उपयोगी चाहिए, और केवल reasonably capable peers को उस scheme में join करना चाहिए। N class और उससे ऊपर denial of service का जोखिम दबाने के लिए काफी बड़ी मात्रा होनी चाहिए, मुझे उम्मीद है। लेकिन यह floodfill से अलग होना चाहिए, इस अर्थ में कि यह humongous traffic नहीं बनाएगा। Large quantity? DHT based netDb के लिए? जरूरी नहीं कि DHT-based हो।

### Floodfill TODO सूची {#todo}

नोट: निम्नलिखित वर्तमान जानकारी नहीं है। वर्तमान स्थिति और भविष्य के कार्यों की सूची के लिए [मुख्य netDb पृष्ठ](/docs/overview/network-database) देखें।

13 मार्च, 2008 को नेटवर्क कुछ घंटों के लिए केवल एक floodfill तक सीमित हो गया था (लगभग 18:00 - 20:00 UTC), और इसने बहुत परेशानी का कारण बना।

0.6.1.33 में लागू किए गए दो बदलाव floodfill peer हटाने या churn के कारण होने वाली बाधा को कम करना चाहिए:

1. हर बार खोज के लिए उपयोग किए जाने वाले floodfill peers को randomize करें।
   यह आपको अंततः असफल होने वाले peers से आगे निकलने में मदद करेगा।
   इस बदलाव ने एक गंभीर bug को भी ठीक किया है जो कभी-कभी ff search code को पागल कर देता था।
2. उन floodfill peers को प्राथमिकता दें जो चालू हैं।
   अब code उन peers से बचता है जो shitlisted हैं, असफल हो रहे हैं, या आधे घंटे से नहीं सुने गए हैं, यदि संभव हो।

एक लाभ यह है कि I2P Site के साथ पहला संपर्क तेज़ होता है (यानी जब आपको पहले leaseset प्राप्त करना पड़ता है)। lookup timeout 10s है, इसलिए यदि आप किसी ऐसे peer से पूछना शुरू नहीं करते जो down है, तो आप 10s बचा सकते हैं।

इन बदलावों में गुमनामी के निहितार्थ *हो सकते हैं*। उदाहरण के लिए, floodfill **store** कोड में, टिप्पणियां हैं कि shitlisted peers से बचा नहीं जाता, क्योंकि एक peer "shitty" हो सकता है और फिर देख सकता है कि क्या होता है। Searches, stores की तुलना में बहुत कम संवेदनशील होती हैं - वे बहुत कम बार होती हैं, और कम जानकारी देती हैं। तो शायद हमें लगता है कि हमें इसकी चिंता करने की जरूरत नहीं है? लेकिन यदि हम बदलावों को समायोजित करना चाहते हैं, तो "down" या shitlisted के रूप में सूचीबद्ध peer को भेजना आसान होगा, बस उसे उन 2 के हिस्से के रूप में नहीं गिनना जिन्हें हम भेज रहे हैं (क्योंकि हम वास्तव में जवाब की उम्मीद नहीं करते)।

कई स्थान हैं जहाँ एक floodfill peer का चयन किया जाता है - यह फिक्स केवल एक को संबोधित करती है - एक नियमित peer कहाँ से खोज करता है [एक समय में 2]। अन्य स्थान जहाँ बेहतर floodfill चयन को लागू किया जाना चाहिए:

1. एक नियमित peer किसे store करता है [एक समय में 1]
   (random - योग्यता जोड़ने की आवश्यकता है, क्योंकि timeouts लंबे हैं)
2. एक नियमित peer store को verify करने के लिए किसे search करता है [एक समय में 1]
   (random - योग्यता जोड़ने की आवश्यकता है, क्योंकि timeouts लंबे हैं)
3. एक floodfill peer असफल search के जवाब में किसे भेजता है (search के सबसे करीब के 3)
4. एक floodfill peer किसे flood करता है (अन्य सभी floodfill peers को)
5. NTCP हर-6-घंटे "whisper" में भेजी जाने वाली floodfill peers की सूची
   (हालांकि अन्य floodfill सुधारों के कारण यह अब आवश्यक नहीं हो सकता है)

बहुत कुछ और भी हो सकता है और होना चाहिए:

- floodfill peer के integration को बेहतर तरीके से rate करने के लिए "dbHistory" stats का उपयोग करें
- floodfill peers जो respond नहीं करते हैं उनके लिए तुरंत react करने के लिए "dbHistory" stats का उपयोग करें
- retries पर smarter बनें - retries को upper layer द्वारा handle किया जाता है, FloodOnlySearchJob में नहीं, इसलिए यह एक और random sort करता है और फिर से try करता है, बजाय purposefully उन ff peers को skip करने के जिन्हें हमने अभी try किया था।
- integration stats को और बेहतर बनाएं
- netDb में सिर्फ floodfill indication के बजाय वास्तव में integration stats का उपयोग करें
- latency stats का भी उपयोग करें?
- failing floodfill peers को पहचानने में और सुधार

हाल ही में पूरा किया गया:

- [Release 0.6.3 में]
  नेटवर्क के विश्लेषण के आधार पर class O peers के कुछ प्रतिशत के लिए floodfill में automatic opt-in को लागू करना।
- [Release 0.6.3 में]
  floodfill ट्रैफिक को कम करने के लिए netDb entry size को कम करना जारी रखना -
  हम अब नेटवर्क की निगरानी के लिए आवश्यक stats की न्यूनतम संख्या पर हैं।
- [Release 0.6.3 में]
  बाहर करने के लिए floodfill peers की मैन्युअल सूची
  (router ident द्वारा [blocklists](/docs/overview/threat-model#blocklist))
- [Release 0.6.3 में]
  stores के लिए बेहतर floodfill peer selection:
  उन peers से बचना जिनका netDb पुराना है, या हाल में failed store है,
  या forever-shitlisted हैं।
- [Release 0.6.4 में]
  RouterInfo stores के लिए पहले से जुड़े हुए floodfill peers को प्राथमिकता देना, ताकि
  floodfill peers के साथ direct connections की संख्या कम हो सके।
- [Release 0.6.5 में]
  जो Peers अब floodfill नहीं हैं, वे query के जवाब में अपना routerInfo भेजते हैं,
  ताकि query करने वाले router को पता चल जाए कि वह
  अब floodfill नहीं है।
- [Release 0.6.5 में]
  स्वचालित रूप से floodfill बनने की आवश्यकताओं की और ट्यूनिंग
- [Release 0.6.5 में]
  तेज़ floodfills को प्राथमिकता देने की तैयारी में response time profiling को ठीक करना
- [Release 0.6.5 में]
  blocklisting में सुधार
- [Release 0.7 में]
  netDb exploration को ठीक करना
- [Release 0.7 में]
  blocklisting को डिफ़ॉल्ट रूप से चालू करना, ज्ञात समस्या पैदा करने वालों को block करना
- [हाल की releases में कई सुधार, एक निरंतर प्रयास]
  high-bandwidth और floodfill routers पर संसाधन की मांग को कम करना

यह एक लंबी सूची है लेकिन एक ऐसा नेटवर्क बनाने के लिए इतना काम करना होगा जो बहुत सारे peers के floodfill स्विच को बार-बार ऑन और ऑफ करने से होने वाले DOS से प्रतिरोधी हो। या floodfill router होने का नाटक करने से। जब हमारे पास केवल दो ff routers थे, और वे दोनों 24/7 चालू रहते थे, तब यह कोई समस्या नहीं थी। फिर से, jrandom की अनुपस्थिति ने हमें उन जगहों की ओर इशारा किया है जिनमें सुधार की आवश्यकता है।

इस प्रयास में सहायता के लिए, floodfill peers के लिए अतिरिक्त profile डेटा अब (रिलीज़ 0.6.1.33 के अनुसार) router console के "Profiles" पृष्ठ पर प्रदर्शित किया जाता है। हम इसका उपयोग यह विश्लेषित करने के लिए करेंगे कि floodfill peers की रेटिंग के लिए कौन सा डेटा उपयुक्त है।

नेटवर्क वर्तमान में काफी लचीला है, हालांकि हम floodfill peers के प्रदर्शन और विश्वसनीयता को मापने और उस पर प्रतिक्रिया करने के लिए अपने algorithms को बेहतर बनाना जारी रखेंगे। जबकि हम इस समय दुर्भावनापूर्ण floodfills या floodfill DDOS के संभावित खतरों के खिलाफ पूर्णतः सुरक्षित नहीं हैं, अधिकांश infrastructure मौजूद है, और जरूरत पड़ने पर हम तुरंत प्रतिक्रिया करने की अच्छी स्थिति में हैं।
