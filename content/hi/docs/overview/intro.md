---
title: "I2P: गुमनाम संचार के लिए एक स्केलेबल फ्रेमवर्क"
description: "I2P आर्किटेक्चर और संचालन का परिचय"
slug: "intro"
aliases:
  - "/hi/intro"
  - "/hi/intro/"
  - "/hi/how_intro"
  - "/hi/how_intro/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

नोट: यह दस्तावेज़ मूल रूप से jrandom द्वारा 2003 में लिखा गया था। हालांकि हम इसे अद्यतन रखने का प्रयास करते हैं, कुछ जानकारी अप्रचलित या अधूरी हो सकती है। transport और cryptography अनुभाग 2025-01 तक वर्तमान हैं।

## परिचय

I2P एक स्केलेबल, स्व-संगठित, लचीला packet switched anonymous network layer है, जिसके ऊपर कई अलग-अलग anonymity या सुरक्षा-सचेत applications काम कर सकते हैं। इनमें से प्रत्येक application अपने स्वयं के anonymity, latency, और throughput tradeoffs बना सकते हैं बिना free route mixnet के उचित implementation की चिंता किए, जिससे वे अपनी गतिविधि को I2P के ऊपर पहले से चल रहे users के बड़े anonymity set के साथ मिला सकें।

उपलब्ध एप्लिकेशन पहले से ही सामान्य इंटरनेट गतिविधियों की पूरी श्रृंखला प्रदान करते हैं — **गुमनाम** वेब ब्राउज़िंग, वेब होस्टिंग, चैट, फ़ाइल साझाकरण, ई-मेल, ब्लॉगिंग और कंटेंट सिंडिकेशन, साथ ही विकास के अधीन कई अन्य एप्लिकेशन।

- वेब ब्राउज़िंग: किसी भी मौजूदा browser का उपयोग करके जो proxy का उपयोग करने का समर्थन करता है।
- चैट: IRC और अन्य protocols
- फ़ाइल साझाकरण: [I2PSnark](#i2psnark) और अन्य applications
- ई-मेल: [susimail](#i2pmail--susimail) और अन्य applications
- ब्लॉग: किसी भी local web server का उपयोग करके, या उपलब्ध plugins

[Freenet](#freenet) या [GNUnet](https://www.gnunet.org/en/) जैसे content distribution networks में hosted वेबसाइटों के विपरीत, I2P पर hosted की जाने वाली services पूर्णतः interactive हैं — यहाँ पारंपरिक web-style search engines, bulletin boards, blogs हैं जिन पर आप comment कर सकते हैं, database driven sites हैं, और Freenet जैसे static systems को query करने के लिए bridges हैं जिन्हें locally install करने की आवश्यकता नहीं है।

इन सभी गुमनामी सक्षम एप्लिकेशनों के साथ, I2P message oriented middleware की भूमिका निभाता है — एप्लिकेशन कहते हैं कि वे किसी cryptographic identifier (एक "destination") को कुछ डेटा भेजना चाहते हैं और I2P यह सुनिश्चित करने का ख्याल रखता है कि यह वहाँ सुरक्षित और गुमनाम रूप से पहुँचे। I2P एक सरल [streaming](#streaming-library) library भी बंडल करता है जो I2P के anonymous best-effort संदेशों को reliable, in-order streams के रूप में स्थानांतरित करने की अनुमति देता है, पारदर्शी रूप से नेटवर्क के high bandwidth delay product के लिए tuned एक TCP आधारित congestion control algorithm पेश करता है। जबकि मौजूदा एप्लिकेशनों को नेटवर्क में जोड़ने के लिए कई सरल SOCKS proxies उपलब्ध रहे हैं, उनकी उपयोगिता सीमित रही है क्योंकि लगभग हर एप्लिकेशन नियमित रूप से उस जानकारी को उजागर करता है जो गुमनाम संदर्भ में संवेदनशील जानकारी है। जाने का एकमात्र सुरक्षित तरीका किसी एप्लिकेशन का पूरी तरह audit करना है ताकि उचित संचालन सुनिश्चित हो सके और इसमें सहायता के लिए हम विभिन्न भाषाओं में APIs की एक श्रृंखला प्रदान करते हैं जिनका उपयोग नेटवर्क का अधिकतम लाभ उठाने के लिए किया जा सकता है।

I2P कोई अनुसंधान परियोजना नहीं है — न तो शैक्षणिक, न वाणिज्यिक, और न ही सरकारी — बल्कि यह एक इंजीनियरिंग प्रयास है जिसका उद्देश्य उन लोगों को पर्याप्त स्तर की गुमनामी प्रदान करने के लिए जो कुछ भी आवश्यक है वह करना है जिन्हें इसकी जरूरत है। यह 2003 की शुरुआत से सक्रिय विकास में है एक पूर्णकालिक डेवलपर और दुनिया भर के समर्पित अंशकालिक योगदानकर्ताओं के एक समूह के साथ। I2P पर किया गया सभी काम ओपन सोर्स है और [वेबसाइट](/) पर मुफ्त में उपलब्ध है, अधिकांश कोड सीधे पब्लिक डोमेन में जारी किया गया है, हालांकि BSD-शैली के लाइसेंस के तहत कुछ क्रिप्टोग्राफिक रूटीन का उपयोग किया गया है। I2P पर काम करने वाले लोग इस बात को नियंत्रित नहीं करते कि लोग क्लाइंट एप्लिकेशन किस लाइसेंस के तहत जारी करते हैं, और कई GPL'ed एप्लिकेशन उपलब्ध हैं ([I2PTunnel](#i2ptunnel), [susimail](#i2pmail--susimail), [I2PSnark](#i2psnark), I2P-Bote, I2Phex और अन्य)। I2P के लिए फंडिंग पूरी तरह से दान से आती है, और इस समय किसी भी न्यायाधिकार क्षेत्र में कोई कर छूट नहीं मिलती, क्योंकि कई डेवलपर स्वयं गुमनाम हैं।

---

## संचालन

### अवलोकन

I2P के संचालन को समझने के लिए, कुछ मुख्य अवधारणाओं को समझना आवश्यक है। पहले, I2P नेटवर्क में भाग लेने वाले सॉफ्टवेयर (एक "router") और व्यक्तिगत एप्लिकेशन से जुड़े गुमनाम endpoints ("destinations") के बीच एक सख्त अलगाव बनाता है। यह तथ्य कि कोई I2P चला रहा है, आमतौर पर कोई रहस्य नहीं होता। जो छुपाया जाता है वह इस बारे में जानकारी है कि उपयोगकर्ता क्या कर रहा है, यदि कुछ भी कर रहा है, और साथ ही यह भी कि कोई विशेष destination किस router से जुड़ा है। अंतिम उपयोगकर्ताओं के पास आमतौर पर अपने router पर कई स्थानीय destinations होंगे — उदाहरण के लिए, एक IRC servers में प्रॉक्सी करने के लिए, दूसरा उपयोगकर्ता के गुमनाम वेबसर्वर ("I2P Site") का समर्थन करने के लिए, एक अन्य I2Phex instance के लिए, एक अन्य torrents के लिए, आदि।

समझने के लिए एक और महत्वपूर्ण अवधारणा "tunnel" है। एक tunnel स्पष्ट रूप से चुने गए routers की सूची के माध्यम से एक निर्देशित पथ है। स्तरित एन्क्रिप्शन का उपयोग किया जाता है, इसलिए प्रत्येक router केवल एक ही स्तर को डिक्रिप्ट कर सकता है। डिक्रिप्टेड जानकारी में अगले router का IP और आगे भेजी जाने वाली एन्क्रिप्टेड जानकारी शामिल होती है। प्रत्येक tunnel का एक शुरुआती बिंदु (पहला router, जिसे "gateway" भी कहा जाता है) और एक अंतिम बिंदु होता है। संदेश केवल एक दिशा में भेजे जा सकते हैं। संदेश वापस भेजने के लिए, दूसरी tunnel की आवश्यकता होती है।

![Inbound and outbound tunnel schematic](/images/tunnels.svg) *चित्र 1: दो प्रकार की tunnel मौजूद हैं: inbound और outbound।*

दो प्रकार की tunnels मौजूद हैं: **"outbound" tunnels** संदेशों को tunnel निर्माता से दूर भेजती हैं, जबकि **"inbound" tunnels** संदेशों को tunnel निर्माता के पास लाती हैं। इन दोनों tunnels को मिलाकर उपयोगकर्ता एक-दूसरे को संदेश भेज सकते हैं। भेजने वाला ("Alice" उपरोक्त छवि में) एक outbound tunnel स्थापित करता है, जबकि प्राप्तकर्ता ("Bob" उपरोक्त छवि में) एक inbound tunnel बनाता है। एक inbound tunnel का gateway किसी भी अन्य उपयोगकर्ता से संदेश प्राप्त कर सकता है और उन्हें endpoint ("Bob") तक भेजता रहेगा। Outbound tunnel के endpoint को संदेश को inbound tunnel के gateway तक भेजना होगा। ऐसा करने के लिए, भेजने वाला ("Alice") अपने एन्क्रिप्टेड संदेश में निर्देश जोड़ता है। एक बार जब outbound tunnel का endpoint संदेश को डिक्रिप्ट कर देता है, तो उसके पास संदेश को सही inbound gateway ("Bob" के gateway) तक फॉरवर्ड करने के निर्देश होंगे।

समझने वाली तीसरी महत्वपूर्ण अवधारणा I2P का **"network database"** (या "netDb") है — नेटवर्क metadata साझा करने के लिए उपयोग किए जाने वाले एल्गोरिदम की एक जोड़ी। दो प्रकार के metadata ले जाए जाते हैं **"routerInfo"** और **"leaseSets"** — routerInfo रूटर को किसी विशिष्ट रूटर से संपर्क करने के लिए आवश्यक डेटा देता है (उनकी public keys, transport addresses, आदि), जबकि leaseSet रूटर को किसी विशिष्ट destination से संपर्क करने के लिए आवश्यक जानकारी देता है। एक leaseSet में कई "leases" होते हैं। इन leases में से प्रत्येक एक tunnel gateway निर्दिष्ट करता है, जो एक विशिष्ट destination तक पहुंचने की अनुमति देता है। एक lease में निहित पूरी जानकारी:

- एक tunnel के लिए inbound gateway जो एक विशिष्ट गंतव्य तक पहुंचने की अनुमति देता है।
- समय जब एक tunnel समाप्त हो जाता है।
- संदेशों को encrypt करने के लिए public keys की जोड़ी (tunnel के माध्यम से भेजने और गंतव्य तक पहुंचने के लिए)।

Router स्वयं अपनी routerInfo को netDb में सीधे भेजते हैं, जबकि leaseSet को outbound tunnel के माध्यम से भेजा जाता है (leaseSet को गुमनाम रूप से भेजना आवश्यक होता है, ताकि किसी router को उसके leaseSet से जोड़ा न जा सके)।

हम नेटवर्क में सफल कनेक्शन बनाने के लिए उपरोक्त अवधारणाओं को मिला सकते हैं।

अपनी inbound और outbound tunnels बनाने के लिए, Alice routerInfo एकत्र करने के लिए netDb में lookup करती है। इस तरह, वह peers की सूची एकत्र करती है जिन्हें वह अपनी tunnels में hops के रूप में उपयोग कर सकती है। फिर वह पहले hop को एक build message भेज सकती है, tunnel के निर्माण का अनुरोध करते हुए और उस router से कहते हुए कि वह construction message को आगे भेजे, जब तक कि tunnel का निर्माण पूरा नहीं हो जाता।

![अन्य routers पर जानकारी का अनुरोध करें](/images/netdb_get_routerinfo_1.svg)

![Build tunnel using router information](/images/netdb_get_routerinfo_2.svg) *चित्र 2: Router की जानकारी का उपयोग tunnel बनाने के लिए किया जाता है।*

जब Alice Bob को एक संदेश भेजना चाहती है, तो वह पहले netDb में lookup करती है Bob के leaseSet को खोजने के लिए, जो उसे उसके वर्तमान inbound tunnel gateways देता है। फिर वह अपनी outbound tunnels में से एक को चुनती है और संदेश को उसमें भेजती है, outbound tunnel के endpoint को निर्देशों के साथ कि वह संदेश को Bob के inbound tunnel gateways में से एक को forward करे। जब outbound tunnel endpoint उन निर्देशों को प्राप्त करता है, तो वह संदेश को अनुरोध के अनुसार forward करता है, और जब Bob का inbound tunnel gateway इसे प्राप्त करता है, तो यह tunnel के माध्यम से Bob के router तक forward किया जाता है। यदि Alice चाहती है कि Bob संदेश का उत्तर दे सके, तो उसे अपना destination स्पष्ट रूप से संदेश के हिस्से के रूप में भेजना होगा। यह एक उच्च-स्तरीय layer पेश करके किया जा सकता है, जो [streaming](#streaming-library) library में किया जाता है। Alice response time कम करने के लिए अपना सबसे नवीनतम LeaseSet संदेश के साथ bundle भी कर सकती है ताकि Bob को जवाब देते समय इसके लिए netDb lookup करने की आवश्यकता न हो, लेकिन यह वैकल्पिक है।

![Connect tunnels using LeaseSets](/images/netdb_get_leaseset.svg) *चित्र 3: LeaseSets का उपयोग outbound और inbound tunnels को जोड़ने के लिए किया जाता है।*

जबकि tunnels में स्वयं layered encryption होती है जो नेटवर्क के अंदर के peers को अनधिकृत प्रकटीकरण से रोकती है (जैसे transport layer स्वयं नेटवर्क के बाहर के peers को अनधिकृत प्रकटीकरण से रोकती है), outbound tunnel endpoint और inbound tunnel gateway से संदेश को छुपाने के लिए एक अतिरिक्त end to end encryption layer जोड़ना आवश्यक है। यह "[garlic encryption](#garlic-messages)" Alice के router को कई संदेशों को एक single "garlic message" में wrap करने देती है, किसी विशेष public key के साथ encrypt करके ताकि intermediary peers यह निर्धारित न कर सकें कि garlic में कितने संदेश हैं, वे संदेश क्या कहते हैं, या वे individual cloves कहाँ जाने के लिए हैं। Alice और Bob के बीच सामान्य end to end communication के लिए, garlic को Bob के leaseSet में प्रकाशित public key के साथ encrypt किया जाएगा, जिससे Bob के अपने router को public key दिए बिना संदेश को encrypt करने की अनुमति मिलती है।

एक और महत्वपूर्ण तथ्य जो ध्यान में रखना चाहिए वह यह है कि I2P पूर्णतः message आधारित है और कुछ messages रास्ते में खो सकते हैं। I2P का उपयोग करने वाले applications message oriented interfaces का उपयोग कर सकते हैं और अपनी congestion control और reliability आवश्यकताओं का ध्यान रख सकते हैं, लेकिन अधिकांश के लिए सबसे अच्छा यह होगा कि वे I2P को streams आधारित network के रूप में देखने के लिए प्रदान की गई [streaming](#streaming-library) library का पुनः उपयोग करें।

---

### Tunnels

आवक और जावक दोनों tunnel समान सिद्धांतों पर काम करते हैं। tunnel gateway कई tunnel संदेशों को एकत्र करता है, अंततः उन्हें tunnel वितरण के लिए कुछ में प्रीप्रोसेसिंग करता है। इसके बाद, gateway उस प्रीप्रोसेसिंग डेटा को एन्क्रिप्ट करता है और इसे पहले hop को भेजता है। वह peer और बाद के tunnel प्रतिभागी यह सत्यापित करने के बाद कि यह डुप्लिकेट नहीं है, अगले peer को भेजने से पहले एन्क्रिप्शन की एक परत जोड़ते हैं। अंततः, संदेश endpoint पर पहुंचता है जहां संदेशों को फिर से अलग किया जाता है और अनुरोध के अनुसार आगे भेजा जाता है। अंतर इस बात में आता है कि tunnel का निर्माता क्या करता है — आवक tunnel के लिए, निर्माता endpoint होता है और वे केवल जोड़ी गई सभी परतों को decrypt करते हैं, जबकि जावक tunnel के लिए, निर्माता gateway होता है और वे सभी परतों को पहले से decrypt करते हैं ताकि प्रति-hop एन्क्रिप्शन की सभी परतें जोड़े जाने के बाद, संदेश tunnel endpoint पर स्पष्ट रूप में पहुंचे।

संदेशों को आगे भेजने के लिए विशिष्ट peers का चुनाव तथा उनकी विशेष क्रमबद्धता I2P की गुमनामी और प्रदर्शन विशेषताओं दोनों को समझने के लिए महत्वपूर्ण है। जबकि network database (नीचे) के पास यह तय करने के लिए अपने मापदंड हैं कि कौन से peers से पूछताछ करनी है और कहाँ entries store करनी हैं, tunnel निर्माता एक ही tunnel में नेटवर्क के किसी भी peers का किसी भी क्रम में (और यहाँ तक कि कितनी भी बार) उपयोग कर सकते हैं। यदि पूर्ण latency और capacity डेटा वैश्विक स्तर पर ज्ञात होता, तो चयन और क्रमबद्धता client की विशिष्ट आवश्यकताओं के साथ उनके threat model के अनुसार संचालित होती। दुर्भाग्य से, latency और capacity डेटा को गुमनाम रूप से एकत्र करना तुच्छ नहीं है, और इस जानकारी को प्रदान करने के लिए अविश्वसनीय peers पर निर्भर रहने के अपने गंभीर गुमनामी निहितार्थ हैं।

गुमनामी के दृष्टिकोण से, सबसे सरल तकनीक यह होगी कि पूरे नेटवर्क से peers को यादृच्छिक रूप से चुना जाए, उन्हें यादृच्छिक क्रम में व्यवस्थित किया जाए और उन peers का उसी क्रम में हमेशा के लिए उपयोग किया जाए। प्रदर्शन के दृष्टिकोण से, सबसे सरल तकनीक यह होगी कि आवश्यक अतिरिक्त क्षमता वाले सबसे तेज़ peers को चुना जाए, transparent failover को संभालने के लिए विभिन्न peers में लोड को फैलाया जाए, और जब भी क्षमता की जानकारी बदले तो tunnel को फिर से बनाया जाए। जबकि पहली विधि नाजुक और अकुशल दोनों है, बाद वाली विधि दुर्गम जानकारी की आवश्यकता होती है और अपर्याप्त गुमनामी प्रदान करती है। इसके बजाय I2P कई peer selection रणनीतियों की पेशकश पर काम कर रहा है, जो anonymity aware measurement कोड के साथ मिलकर peers को उनकी profiles के आधार पर व्यवस्थित करता है।

एक आधार के रूप में, I2P लगातार उन peers की प्रोफाइलिंग करता है जिनके साथ यह बातचीत करता है, उनके अप्रत्यक्ष व्यवहार को मापकर — उदाहरण के लिए, जब कोई peer netDb lookup का 1.3 सेकंड में जवाब देता है, तो उस round trip latency को उन सभी routers के profiles में रिकॉर्ड किया जाता है जो दोनों tunnels (inbound और outbound) में शामिल हैं जिनके माध्यम से request और response गुजरे, साथ ही queried peer के profile में भी। प्रत्यक्ष माप, जैसे कि transport layer latency या congestion, profile के हिस्से के रूप में उपयोग नहीं किए जाते, क्योंकि इन्हें manipulate किया जा सकता है और measuring router के साथ जोड़ा जा सकता है, जिससे वे trivial attacks के लिए exposed हो जाते हैं। इन profiles को इकट्ठा करते समय, प्रत्येक पर गणनाओं की एक श्रृंखला चलाई जाती है ताकि इसके प्रदर्शन का सारांश निकाला जा सके — इसकी latency, बहुत सी गतिविधि को संभालने की क्षमता, क्या वे वर्तमान में overloaded हैं, और वे network में कितनी अच्छी तरह integrated लगते हैं। फिर इन गणनाओं की तुलना active peers के लिए की जाती है ताकि routers को चार tiers में व्यवस्थित किया जा सके — fast और high capacity, high capacity, not failing, और failing। इन tiers के लिए thresholds गतिशील रूप से निर्धारित किए जाते हैं, और जबकि वे वर्तमान में काफी सरल algorithms का उपयोग करते हैं, alternatives मौजूद हैं।

इस profile डेटा का उपयोग करते हुए, सबसे सरल उचित peer चयन रणनीति है top tier (तेज़ और उच्च क्षमता) से peers को यादृच्छिक रूप से चुनना, और यह वर्तमान में client tunnels के लिए तैनात है। Exploratory tunnels (जो netDb और tunnel प्रबंधन के लिए उपयोग होती हैं) "not failing" tier से peers को यादृच्छिक रूप से चुनती हैं (जिसमें 'बेहतर' tiers के routers भी शामिल हैं), जो peer को routers का व्यापक नमूना लेने की अनुमति देता है, वास्तव में randomized [hill climbing](https://en.wikipedia.org/wiki/Hill_climbing) के माध्यम से peer चयन को अनुकूलित करता है। हालांकि, ये रणनीतियां अकेली predecessor और netDb harvesting हमलों के माध्यम से router के top tier में peers के बारे में जानकारी का रिसाव करती हैं। इसके बदले में, कई विकल्प मौजूद हैं जो, भले ही लोड को उतने समान रूप से संतुलित न करें, विशेष श्रेणियों के adversaries द्वारा किए जाने वाले हमलों का समाधान करेंगे।

एक यादृच्छिक key चुनकर और peers को उससे उनकी XOR दूरी के अनुसार क्रमबद्ध करके, predecessor और harvesting attacks में leaked जानकारी को peers की failure rate और tier के churn के अनुसार कम किया जा सकता है। netDb harvesting attacks से निपटने की एक और सरल रणनीति है inbound tunnel gateway(s) को fix करना लेकिन tunnels में आगे के peers को randomize करना। उन adversaries के लिए predecessor attacks से निपटने के लिए जिनसे client संपर्क करता है, outbound tunnel endpoints भी fixed रहेंगे। सबसे exposed point पर कौन सा peer fix करना है इसके selection की अवधि की एक सीमा होनी चाहिए, क्योंकि सभी peers अंततः fail हो जाते हैं, इसलिए इसे या तो reactively adjust किया जा सकता है या अन्य routers की measured mean time between failures को mimic करने के लिए proactively avoid किया जा सकता है। इन दोनों strategies को मिलाया जा सकता है, एक fixed exposed peer और tunnels के भीतर XOR based ordering का उपयोग करके। एक और कठोर रणनीति potential tunnel के exact peers और ordering को fix करना होगी, individual peers का उपयोग केवल तभी करना जब वे सभी हर बार समान तरीके से participate करने के लिए सहमत हों। यह XOR based ordering से अलग है क्योंकि हर peer का predecessor और successor हमेशा समान होता है, जबकि XOR केवल यह सुनिश्चित करता है कि उनका order नहीं बदलता।

जैसा कि पहले उल्लेख किया गया है, I2P वर्तमान में (release 0.8) XOR-आधारित क्रम के साथ उपरोक्त tiered random strategy को शामिल करता है। tunnel संचालन, प्रबंधन, और peer चयन में शामिल यांत्रिकी की अधिक विस्तृत चर्चा [tunnel spec](/docs/specs/tunnel-implementation/) में पाई जा सकती है।

---

### Network Database (netDb)

जैसा कि पहले उल्लेख किया गया है, I2P का netDb नेटवर्क के metadata को साझा करने का काम करता है। इसका विस्तृत विवरण [network database](/docs/specs/common-structures/) पेज में उपलब्ध है, लेकिन एक बुनियादी स्पष्टीकरण नीचे दिया गया है।

सभी I2P router में एक स्थानीय netDb होता है, लेकिन सभी router DHT में भाग नहीं लेते या leaseset lookups का जवाब नहीं देते। जो router DHT में भाग लेते हैं और leaseset lookups का जवाब देते हैं, उन्हें 'floodfill' कहा जाता है। Router को मैन्युअल रूप से floodfill के रूप में कॉन्फ़िगर किया जा सकता है, या यदि उनके पास पर्याप्त क्षमता है और वे विश्वसनीय संचालन के लिए अन्य मानदंडों को पूरा करते हैं तो वे स्वचालित रूप से floodfill बन सकते हैं।

अन्य I2P router अपना डेटा संग्रहीत करेंगे और floodfill को सरल 'store' और 'lookup' क्वेरी भेजकर डेटा खोजेंगे। यदि कोई floodfill router को 'store' क्वेरी प्राप्त होती है, तो यह [Kademlia algorithm](http://en.wikipedia.org/wiki/Kademlia) का उपयोग करके जानकारी को अन्य floodfill router में फैलाएगा। 'lookup' क्वेरी वर्तमान में एक महत्वपूर्ण सुरक्षा मुद्दे से बचने के लिए अलग तरीके से काम करती हैं। जब lookup किया जाता है, तो floodfill router lookup को अन्य peers को forward नहीं करेगा, बल्कि हमेशा स्वयं उत्तर देगा (यदि इसके पास अनुरोधित डेटा है)।

नेटवर्क डेटाबेस में दो प्रकार की जानकारी संग्रहीत होती है।

- एक **RouterInfo** एक विशिष्ट I2P router की जानकारी और उससे संपर्क करने का तरीका संग्रहीत करता है
- एक **LeaseSet** एक विशिष्ट destination की जानकारी संग्रहीत करता है (जैसे I2P website, ई-मेल सर्वर...)

यह सभी जानकारी प्रकाशित करने वाली पार्टी द्वारा signed की जाती है और इस जानकारी का उपयोग या storage करने वाले किसी भी I2P router द्वारा verified की जाती है। इसके अतिरिक्त, data में timing की जानकारी होती है, ताकि पुरानी entries के storage और संभावित attacks से बचा जा सके। यही कारण है कि I2P में सही समय बनाए रखने के लिए आवश्यक code bundled होता है, जो कभी-कभार कुछ SNTP servers से query करता है (default रूप से [pool.ntp.org](http://www.pool.ntp.org/) round robin) और transport layer पर routers के बीच skew का पता लगाता है।

कुछ अतिरिक्त टिप्पणियां भी महत्वपूर्ण हैं।

- **अप्रकाशित और एन्क्रिप्टेड leasesets:**
  कोई व्यक्ति चाह सकता है कि केवल विशिष्ट लोग ही किसी destination तक पहुंच सकें। यह netDb में destination को प्रकाशित न करके संभव है। हालांकि आपको destination को अन्य माध्यमों से प्रसारित करना होगा। यह 'encrypted leaseSets' द्वारा समर्थित है। ये leaseSets केवल उन लोगों द्वारा डिकोड किए जा सकते हैं जिनके पास decryption key तक पहुंच है।

- **Bootstrapping:**
  netDb को bootstrap करना काफी सरल है। एक बार जब कोई router किसी पहुंचने योग्य peer की एक routerInfo प्राप्त कर लेता है, तो वह उस router से network में अन्य routers के references के लिए query कर सकता है। वर्तमान में, कई users अपनी routerInfo files को एक website पर post करते हैं ताकि यह जानकारी उपलब्ध हो सके। I2P स्वचालित रूप से इन websites में से किसी एक से जुड़ता है routerInfo files इकट्ठा करने और bootstrap करने के लिए। I2P इस bootstrap process को "reseeding" कहता है।

- **Lookup scalability:**
  I2P नेटवर्क में lookups iterative होते हैं, recursive नहीं। यदि किसी floodfill से lookup असफल हो जाता है, तो lookup को अगले सबसे निकटतम floodfill पर दोहराया जाएगा। floodfill recursively किसी अन्य floodfill से डेटा नहीं मांगता। Iterative lookups बड़े DHT नेटवर्क के लिए scalable होते हैं।

---

### ट्रांसपोर्ट प्रोटोकॉल

Routers के बीच संचार में बाहरी विरोधियों के खिलाफ गोपनीयता और अखंडता प्रदान करने की आवश्यकता होती है जबकि यह प्रमाणित करना होता है कि संपर्क किया गया router वही है जिसे कोई संदेश प्राप्त करना चाहिए। यह कि routers अन्य routers के साथ कैसे संचार करते हैं इसकी विशेषताएं महत्वपूर्ण नहीं हैं — उन बुनियादी आवश्यकताओं को प्रदान करने के लिए अलग-अलग समय पर तीन अलग protocols का उपयोग किया गया है।

I2P वर्तमान में दो transport protocols का समर्थन करता है, TCP पर [NTCP2](/docs/specs/ntcp2/), और UDP पर [SSU2](/docs/specs/ssu2/)। इन्होंने protocols के पिछले versions, [NTCP](/docs/legacy/ssu/) और [SSU](/docs/legacy/ssu/), को बदल दिया है, जो अब deprecated हैं। दोनों protocols IPv4 और IPv6 दोनों का समर्थन करते हैं। TCP और UDP transports दोनों का समर्थन करके, I2P प्रभावी रूप से अधिकांश firewalls को पार कर सकता है, जिसमें प्रतिबंधात्मक censorship regimes में traffic को block करने के लिए बने firewalls भी शामिल हैं। NTCP2 और SSU2 को आधुनिक encryption standards का उपयोग करने, traffic identification resistance में सुधार करने, efficiency और security बढ़ाने, और NAT traversal को अधिक robust बनाने के लिए डिज़ाइन किया गया था। Routers प्रत्येक समर्थित transport और IP address को network database में प्रकाशित करते हैं। Public IPv4 और IPv6 networks तक पहुंच वाले Routers आमतौर पर चार addresses प्रकाशित करते हैं, NTCP2/SSU2 के IPv4/IPv6 के साथ प्रत्येक combination के लिए एक।

[SSU2](/docs/specs/ssu2/) SSU के लक्ष्यों का समर्थन और विस्तार करता है। SSU2 में अन्य आधुनिक UDP-आधारित प्रोटोकॉल जैसे Wireguard और QUIC के साथ कई समानताएं हैं। UDP पर नेटवर्क संदेशों के विश्वसनीय परिवहन के अतिरिक्त, SSU2 peer-to-peer, सहकारी IP address detection, firewall detection, और NAT traversal के लिए विशेष सुविधाएं प्रदान करता है। जैसा कि [SSU spec](/docs/legacy/ssu/) में वर्णित है:

> इस protocol का लक्ष्य सुरक्षित, प्रमाणित, अर्ध-विश्वसनीय और अव्यवस्थित message delivery प्रदान करना है, जो तीसरे पक्षों को केवल न्यूनतम मात्रा में आसानी से पहचाने जाने वाले डेटा को उजागर करे। इसे उच्च डिग्री संचार के साथ-साथ TCP-friendly congestion control का समर्थन करना चाहिए और इसमें PMTU detection शामिल हो सकती है। यह घरेलू उपयोगकर्ताओं के लिए पर्याप्त दरों पर bulk data को कुशलतापूर्वक स्थानांतरित करने में सक्षम होना चाहिए। इसके अतिरिक्त, इसे अधिकांश NATs या firewalls जैसी नेटवर्क बाधाओं को संबोधित करने की तकनीकों का समर्थन करना चाहिए।

[NTCP2](/docs/specs/ntcp2/) NTCP के लक्ष्यों का समर्थन और विस्तार करता है। यह TCP पर नेटवर्क संदेशों का कुशल और पूर्णतः एन्क्रिप्टेड परिवहन प्रदान करता है, और आधुनिक एन्क्रिप्शन मानकों का उपयोग करके ट्रैफिक पहचान के प्रतिरोध को सुनिश्चित करता है।

I2P एक साथ कई transports का समर्थन करता है। आउटबाउंड कनेक्शन के लिए एक विशेष transport का चयन "bids" के साथ किया जाता है। प्रत्येक transport कनेक्शन के लिए bid करता है और इन bids के सापेक्षिक मूल्य से प्राथमिकता निर्धारित होती है। Transports अलग-अलग bids के साथ जवाब दे सकते हैं, यह इस बात पर निर्भर करता है कि peer के साथ पहले से स्थापित कनेक्शन है या नहीं।

बिड (प्राथमिकता) मान implementation-dependent होते हैं और ट्रैफिक स्थितियों, कनेक्शन संख्या, और अन्य कारकों के आधार पर भिन्न हो सकते हैं। Router भी network database में inbound connections के लिए अपनी transport प्राथमिकताओं को प्रत्येक transport और address के लिए transport "लागत" के रूप में प्रकाशित करते हैं।

---

### क्रिप्टोग्राफी

I2P कई protocol layers पर encryption, authentication, और verification के लिए cryptography का उपयोग करता है। मुख्य protocol layers हैं: transports, tunnel build messages, tunnel layer encryption, network database messages, और end-to-end (garlic) messages। I2P के मूल डिज़ाइन में cryptographic primitives का एक छोटा सेट उपयोग किया गया था जो उस समय सुरक्षित माने जाते थे। इनमें ElGamal asymmetric encryption, DSA-SHA1 signatures, AES256/CBC symmetric encryption, और SHA-256 hashes शामिल थे। जैसे-जैसे उपलब्ध computing power बढ़ी और cryptographic research वर्षों में काफी विकसित हुई, I2P को अपने primitives और protocols को upgrade करना पड़ा। इसलिए, हमने "encryption types" और "signature types" की अवधारणा जोड़ी, और अपने protocols को इन identifiers को शामिल करने और support को indicate करने के लिए विस्तारित किया। यह हमें आधुनिक cryptography के लिए network support को समय-समय पर update और extend करने और नए primitives के लिए network को future-proof करने की अनुमति देता है, बिना backward compatibility को तोड़े या network updates के लिए "flag day" की आवश्यकता के। कुछ signature और encryption types experimental उपयोग के लिए भी आरक्षित हैं।

अधिकांश प्रोटोकॉल परतों में उपयोग होने वाले वर्तमान primitives हैं X25519 key exchange, EdDSA signatures, ChaCha20/Poly1305 authenticated symmetric encryption, और SHA-256 hashes। AES256 का उपयोग अभी भी tunnel layer encryption के लिए किया जाता है। इन आधुनिक प्रोटोकॉल का उपयोग नेटवर्क संचार के विशाल बहुमत के लिए किया जाता है। पुराने primitives जिनमें ElGamal, ECDSA, और DSA-SHA1 शामिल हैं, वे पुराने routers के साथ संचार करते समय backward compatibility के लिए अधिकांश implementations द्वारा समर्थित होते रहते हैं। कुछ पुराने प्रोटोकॉल को deprecated कर दिया गया है और/या पूरी तरह से हटा दिया गया है। निकट भविष्य में हम अपने मजबूत सुरक्षा मानकों को बनाए रखने के लिए post-quantum (PQ) या hybrid-PQ encryption और signatures पर migration के लिए अनुसंधान शुरू करेंगे।

ये क्रिप्टोग्राफिक primitives मिलकर I2P की layered defenses प्रदान करते हैं विभिन्न adversaries के विरुद्ध। सबसे निचले स्तर पर, inter-router communication transport layer security द्वारा संरक्षित होता है। transports पर भेजे गए [Tunnel](#tunnels) messages का अपना layered encryption होता है। विभिन्न अन्य messages "garlic messages" के अंदर भेजे जाते हैं, जो भी encrypted होते हैं।

#### Garlic Messages

Garlic messages "onion" स्तरित एन्क्रिप्शन का एक विस्तार हैं, जो एक single message की सामग्री में कई "cloves" — पूर्ण रूप से बने संदेश और उनके delivery के लिए अपने निर्देश शामिल करने की अनुमति देते हैं। Messages को garlic message में तब wrap किया जाता है जब message अन्यथा किसी peer के माध्यम से cleartext में pass होगा जिसके पास जानकारी तक पहुंच नहीं होनी चाहिए — उदाहरण के लिए, जब एक router किसी दूसरे router से tunnel में भाग लेने के लिए कहना चाहता है, तो वे request को garlic के अंदर wrap करते हैं, उस garlic को receiving router की public key के साथ encrypt करते हैं, और इसे tunnel के माध्यम से forward करते हैं। एक और उदाहरण यह है जब कोई client किसी destination को message भेजना चाहता है — sender का router उस data message को (कुछ अन्य messages के साथ) garlic में wrap करेगा, उस garlic को recipient के leaseSet में प्रकाशित public key के साथ encrypt करेगा, और इसे उपयुक्त tunnels के माध्यम से forward करेगा।

encryption layer के अंदर प्रत्येक clove से जुड़े "instructions" में यह क्षमता शामिल है कि clove को स्थानीय रूप से, किसी remote router पर, या किसी remote router पर remote tunnel को forward करने का अनुरोध किया जा सके। इन instructions में ऐसे फ़ील्ड हैं जो एक peer को यह अनुरोध करने की अनुमति देते हैं कि delivery को तब तक देरी से किया जाए जब तक कोई निश्चित समय या शर्त पूरी न हो जाए, हालांकि इन्हें तब तक सम्मानित नहीं किया जाएगा जब तक [nontrivial delays](#variable-latency) deploy नहीं हो जाते। यह संभव है कि garlic messages को बिना tunnels बनाए किसी भी संख्या में hops के माध्यम से स्पष्ट रूप से route किया जा सके, या यहां तक कि tunnel messages को garlic messages में wrap करके और tunnel में अगले hop तक पहुंचाने से पहले उन्हें कई hops के माध्यम से forward करके reroute भी किया जा सके, लेकिन ये तकनीकें वर्तमान में मौजूदा implementation में उपयोग नहीं की जा रही हैं।

#### सत्र टैग

एक अविश्वसनीय, अव्यवस्थित, संदेश आधारित सिस्टम के रूप में, I2P garlic messages को डेटा गोपनीयता और अखंडता प्रदान करने के लिए असममित और सममित एन्क्रिप्शन एल्गोरिदम का एक सरल संयोजन उपयोग करता है। मूल संयोजन को ElGamal/AES+SessionTags कहा जाता था, लेकिन यह 2048bit ElGamal, AES256, SHA256 और 32 byte nonces के सरल उपयोग का वर्णन करने का एक अत्यधिक वर्बोस तरीका है। जबकि यह प्रोटोकॉल अभी भी समर्थित है, अधिकांश नेटवर्क एक नए प्रोटोकॉल, ECIES-X25519-AEAD-Ratchet में माइग्रेट हो गया है। यह प्रोटोकॉल X25519, ChaCha20/Poly1305, और 32 byte nonces उत्पन्न करने के लिए एक synchronized PRNG को जोड़ता है। दोनों प्रोटोकॉल का संक्षिप्त वर्णन नीचे दिया गया है।

#### ElGamal/AES+SessionTags

जब पहली बार कोई router किसी दूसरे router को garlic message encrypt करना चाहता है, तो वे AES256 session key के लिए keying material को ElGamal से encrypt करते हैं और उस encrypted ElGamal block के बाद AES256/CBC encrypted payload जोड़ते हैं। encrypted payload के अलावा, AES encrypted section में payload length, unencrypted payload का SHA256 hash, और कई "session tags" — random 32 byte nonces शामिल होते हैं। अगली बार जब sender किसी दूसरे router को garlic message encrypt करना चाहता है, तो नई session key को ElGamal encrypt करने के बजाय वे simply पहले से delivered session tags में से एक को pick करते हैं और पहले की तरह payload को AES encrypt करते हैं, उस session tag के साथ use की गई session key का उपयोग करके, जिसे session tag से पहले लगाया जाता है। जब कोई router garlic encrypted message प्राप्त करता है, तो वे पहले 32 bytes को check करते हैं कि यह कोई available session tag से match करता है या नहीं — यदि करता है, तो वे simply message को AES decrypt करते हैं, लेकिन यदि नहीं करता, तो वे पहले block को ElGamal decrypt करते हैं।

प्रत्येक session tag का उपयोग केवल एक बार ही किया जा सकता है ताकि आंतरिक विरोधियों को अनावश्यक रूप से विभिन्न संदेशों को समान routers के बीच होने वाले संदेशों से जोड़ने से रोका जा सके। ElGamal/AES+SessionTag एन्क्रिप्टेड संदेश का भेजने वाला तय करता है कि कब और कितने tags देने हैं, प्राप्तकर्ता को संदेशों की एक श्रृंखला को कवर करने के लिए पर्याप्त tags के साथ पहले से स्टॉक करके। Garlic messages एक छोटे अतिरिक्त संदेश को एक clove के रूप में बंडल करके ("delivery status message") सफल tag delivery का पता लगा सकते हैं — जब garlic message अपने इच्छित प्राप्तकर्ता तक पहुंचता है और सफलतापूर्वक decrypt हो जाता है, तो यह छोटा delivery status message उन cloves में से एक होता है जो खुलते हैं और इसमें प्राप्तकर्ता के लिए निर्देश होते हैं कि इस clove को मूल भेजने वाले को वापस भेजे (निश्चित रूप से एक inbound tunnel के माध्यम से)। जब मूल भेजने वाला इस delivery status message को प्राप्त करता है, तो वे जान जाते हैं कि garlic message में बंडल किए गए session tags सफलतापूर्वक पहुंचा दिए गए थे।

Session tags का स्वयं का जीवनकाल बहुत छोटा होता है, जिसके बाद यदि उनका उपयोग नहीं होता तो उन्हें हटा दिया जाता है। इसके अतिरिक्त, प्रत्येक key के लिए संग्रहीत मात्रा सीमित होती है, जैसा कि keys की संख्या भी सीमित होती है — यदि बहुत अधिक आते हैं, तो या तो नए या पुराने messages को हटा दिया जा सकता है। भेजने वाला यह ट्रैक रखता है कि session tags का उपयोग करने वाले messages पहुंच रहे हैं या नहीं, और यदि पर्याप्त संचार नहीं है तो यह उन संदेशों को हटा सकता है जिन्हें पहले ठीक से वितरित माना गया था, और वापस पूर्ण महंगी ElGamal encryption पर लौट सकता है।

#### ECIES-X25519-AEAD-Ratchet

ElGamal/AES+SessionTags में कई तरीकों से काफी अधिक ओवरहेड की आवश्यकता थी। CPU का उपयोग अधिक था क्योंकि ElGamal काफी धीमा है। बैंडविड्थ अत्यधिक था क्योंकि बड़ी संख्या में session tags को पहले से ही डिलीवर करना पड़ता था, और क्योंकि ElGamal public keys बहुत बड़ी होती हैं। मेमोरी का उपयोग अधिक था क्योंकि बड़ी मात्रा में session tags को स्टोर करने की आवश्यकता थी। विश्वसनीयता session tag delivery के खो जाने से बाधित होती थी।

ECIES-X25519-AEAD-Ratchet को इन समस्याओं को हल करने के लिए डिज़ाइन किया गया था। key exchange के लिए X25519 का उपयोग किया जाता है। authenticated symmetric encryption के लिए ChaCha20/Poly1305 का उपयोग किया जाता है। Encryption keys को "double ratcheted" किया जाता है या समय-समय पर rotate किया जाता है। Session tags को 32 bytes से घटाकर 8 bytes किया गया है और इन्हें PRNG के साथ generate किया जाता है। इस protocol की कई समानताएं Signal और WhatsApp में उपयोग किए जाने वाले signal protocol से हैं। यह protocol CPU, RAM, और bandwidth में काफी कम overhead प्रदान करता है।

सेशन टैग्स एक deterministic synchronized PRNG से उत्पन्न होते हैं जो सेशन के दोनों छोरों पर चलकर सेशन टैग्स और सेशन keys बनाता है। PRNG एक HKDF है जो SHA-256 HMAC का उपयोग करता है, और X25519 DH परिणाम से seeded होता है। सेशन टैग्स कभी भी पहले से transmit नहीं किए जाते; वे केवल message के साथ शामिल किए जाते हैं। receiver एक सीमित संख्या में सेशन keys स्टोर करता है, जो सेशन टैग द्वारा indexed होती हैं। sender को कोई सेशन टैग्स या keys स्टोर करने की आवश्यकता नहीं होती क्योंकि वे पहले से नहीं भेजे जाते; वे on-demand उत्पन्न किए जा सकते हैं। sender और recipient के बीच इस PRNG को लगभग synchronized रखकर (recipient अगले उदाहरण के लिए 50 टैग्स की एक window को precompute करता है), समय-समय पर बड़ी संख्या में टैग्स को bundle करने का overhead हटा दिया जाता है।

---

## भविष्य

I2P के protocols अधिकांश platforms पर कुशल हैं, जिनमें cell phones भी शामिल हैं, और अधिकांश threat models के लिए सुरक्षित हैं। हालांकि, कई क्षेत्र हैं जिनमें उन लोगों की आवश्यकताओं को पूरा करने के लिए और सुधार की आवश्यकता है जो शक्तिशाली राज्य-प्रायोजित विरोधियों का सामना कर रहे हैं, और निरंतर cryptographic प्रगति और बढ़ती computing power के खतरों से निपटने के लिए। दो संभावित features, restricted routes और variable latency, को jrandom द्वारा 2003 में प्रस्तावित किया गया था। जबकि हम अब इन features को लागू करने की योजना नहीं रखते हैं, इन्हें नीचे वर्णित किया गया है।

### प्रतिबंधित रूट संचालन

I2P एक overlay network है जो एक कार्यशील packet switched network के ऊपर चलने के लिए डिज़ाइन किया गया है, जो anonymity और security प्रदान करने के लिए end to end principle का उपयोग करता है। जबकि इंटरनेट अब पूरी तरह से end to end principle को अपनाता नहीं है (NAT के उपयोग के कारण), I2P को network के एक बड़े हिस्से के पहुंच योग्य होने की आवश्यकता होती है — किनारों पर कई peers हो सकते हैं जो restricted routes का उपयोग करके चल रहे हों, लेकिन I2P में उस degenerate case के लिए उपयुक्त routing algorithm शामिल नहीं है जहां अधिकांश peers तक पहुंचा नहीं जा सकता। हालांकि, यह ऐसे algorithm का उपयोग करने वाले network के ऊपर काम करेगा।

प्रतिबंधित route संचालन, जहाँ सीधे पहुँच योग्य peers की सीमाएँ होती हैं, के कई अलग कार्यात्मक और गुमनामी प्रभाव होते हैं, जो इस बात पर निर्भर करता है कि प्रतिबंधित routes को कैसे संभाला जाता है। सबसे बुनियादी स्तर पर, प्रतिबंधित routes तब मौजूद होते हैं जब कोई peer NAT या firewall के पीछे होता है जो inbound connections की अनुमति नहीं देता। इसे transport layer में distributed hole punching को एकीकृत करके काफी हद तक हल किया गया था, जिससे अधिकांश NATs और firewalls के पीछे के लोग बिना किसी configuration के unsolicited connections प्राप्त कर सकते हैं। हालांकि, यह network के अंदर के routers के लिए peer के IP address के exposure को सीमित नहीं करता, क्योंकि वे published introducer के माध्यम से peer से परिचय प्राप्त कर सकते हैं।

प्रतिबंधित routes की कार्यात्मक handling के अतिरिक्त, दो स्तरों का प्रतिबंधित संचालन है जिसका उपयोग किसी के IP address के exposure को सीमित करने के लिए किया जा सकता है — संचार के लिए router-specific tunnels का उपयोग करना, और 'client routers' प्रदान करना। पूर्व के लिए, routers या तो tunnels का एक नया pool बना सकते हैं या अपने exploratory pool का पुन: उपयोग कर सकते हैं, उनमें से कुछ के inbound gateways को अपने transport addresses के स्थान पर अपने routerInfo के हिस्से के रूप में प्रकाशित कर सकते हैं। जब कोई peer उनसे संपर्क करना चाहता है, तो वे netDb में उन tunnel gateways को देखते हैं और बस प्रकाशित tunnels में से एक के माध्यम से उन्हें संबंधित संदेश भेजते हैं। यदि प्रतिबंधित route के पीछे का peer जवाब देना चाहता है, तो वह या तो प्रत्यक्ष रूप से (यदि वे peer को अपना IP expose करने को तैयार हैं) या अपने outbound tunnels के माध्यम से अप्रत्यक्ष रूप से ऐसा कर सकते हैं। जब routers जिनसे peer के प्रत्यक्ष कनेक्शन हैं, उस तक पहुंचना चाहते हैं (उदाहरण के लिए, tunnel संदेशों को forward करने के लिए), तो वे बस प्रकाशित tunnel gateway पर अपने प्रत्यक्ष कनेक्शन को प्राथमिकता देते हैं। 'Client routers' की अवधारणा केवल कोई भी router addresses प्रकाशित न करके प्रतिबंधित route को विस्तारित करती है। ऐसे router को netDb में अपना routerInfo प्रकाशित करने की भी आवश्यकता नहीं होगी, केवल उन peers को अपना self signed routerInfo प्रदान करना होगा जिनसे वह संपर्क करता है (router की public keys पास करने के लिए आवश्यक)।

प्रतिबंधित routes के पीछे वाले लोगों के लिए कुछ समझौते हैं, क्योंकि वे अन्य लोगों के tunnels में कम बार भाग लेंगे, और जिन routers से वे जुड़े हैं वे traffic patterns का अनुमान लगा सकेंगे जो अन्यथा उजागर नहीं होते। दूसरी ओर, यदि उस exposure की कीमत IP उपलब्ध कराने की कीमत से कम है, तो यह उपयोगी हो सकता है। यह, निश्चित रूप से, इस बात की मान्यता पर आधारित है कि प्रतिबंधित route के पीछे का router जिन peers से संपर्क करता है वे शत्रुतापूर्ण नहीं हैं — या तो network इतना बड़ा है कि किसी शत्रुतापूर्ण peer का उपयोग करके जुड़ने की संभावना पर्याप्त रूप से कम है, या इसके बजाय विश्वसनीय (और शायद अस्थायी) peers का उपयोग किया जाता है।

Restricted routes जटिल हैं, और समग्र लक्ष्य को काफी हद तक छोड़ दिया गया है। कई संबंधित सुधारों ने उनकी आवश्यकता को काफी कम कर दिया है। हम अब firewall ports को स्वचालित रूप से खोलने के लिए UPnP का समर्थन करते हैं। हम IPv4 और IPv6 दोनों का समर्थन करते हैं। SSU2 ने address detection, firewall state determination, और cooperative NAT hole punching में सुधार किया है। SSU2, NTCP2, और address compatibility checks यह सुनिश्चित करते हैं कि tunnel hops tunnel बनने से पहले connect कर सकें। GeoIP और country identification हमें प्रतिबंधात्मक firewalls वाले देशों के peers से बचने की अनुमति देती है। उन firewalls के पीछे "hidden" routers के लिए समर्थन में सुधार हुआ है। कुछ implementations Yggdrasil जैसे overlay networks पर peers से connections का भी समर्थन करती हैं।

### परिवर्तनीय विलंबता

हालांकि I2P के प्रारंभिक प्रयासों का मुख्य हिस्सा low latency संचार पर रहा है, इसे शुरुआत से ही variable latency सेवाओं को ध्यान में रखकर डिज़ाइन किया गया था। सबसे बुनियादी स्तर पर, I2P के ऊपर चलने वाले applications medium और high latency संचार की गुमनामी प्रदान कर सकते हैं, जबकि अभी भी उनके traffic patterns को low latency traffic के साथ मिला सकते हैं। आंतरिक रूप से, I2P garlic encryption के माध्यम से अपना medium और high latency संचार प्रदान कर सकता है — यह निर्दिष्ट करते हुए कि message को एक निश्चित देरी के बाद, एक निश्चित समय पर, एक निश्चित संख्या के messages के गुजरने के बाद, या किसी अन्य mix strategy के साथ भेजा जाना चाहिए। layered encryption के साथ, केवल वह router जिसने clove ने delay request को उजागर किया हो, जान सकता है कि message को high latency की आवश्यकता है, जिससे traffic को low latency traffic के साथ और भी अधिक मिलाने की अनुमति मिलती है। एक बार transmission precondition पूरी हो जाने पर, clove को पकड़े रखने वाला router (जो खुद संभावित रूप से एक garlic message होगा) बस इसे अनुरोध के अनुसार forward कर देता है — एक router को, एक tunnel को, या सबसे अधिक संभावना है, एक remote client destination को।

चर विलंबता सेवाओं का लक्ष्य इसे समर्थित करने के लिए store-and-forward तंत्र के लिए पर्याप्त संसाधनों की आवश्यकता होती है। ये तंत्र विभिन्न मैसेजिंग एप्लिकेशन में समर्थित हो सकते हैं और समर्थित हैं, जैसे कि i2p-bote। नेटवर्क स्तर पर, Freenet जैसे वैकल्पिक नेटवर्क ये सेवाएं प्रदान करते हैं। हमने I2P router स्तर पर इस लक्ष्य को आगे नहीं बढ़ाने का निर्णय लिया है।

---

## समान प्रणालियां

I2P की आर्किटेक्चर message oriented middleware की अवधारणाओं, DHT की topology, free route mixnets की anonymity और cryptography, तथा packet switched networking की अनुकूलनशीलता पर आधारित है। मूल्य नवीन अवधारणाओं या algorithms से नहीं बल्कि मौजूदा सिस्टम और papers के अनुसंधान परिणामों को सावधानीपूर्वक जोड़ने वाली engineering से आता है। जबकि तकनीकी और कार्यात्मक तुलना के लिए कुछ समान प्रयासों की समीक्षा करना उचित है, इनमें से दो विशेष रूप से यहां निकाले गए हैं — Tor और Freenet।

[नेटवर्क तुलना पृष्ठ](/docs/overview/comparison/) भी देखें। ध्यान दें कि ये विवरण 2003 में jrandom द्वारा लिखे गए थे और वर्तमान में सटीक नहीं हो सकते हैं।

### Tor

*[वेबसाइट](https://www.torproject.org/)*

पहली नज़र में, Tor और I2P में कई कार्यात्मक और गुमनामी संबंधी समानताएं हैं। जबकि I2P का विकास Tor के प्रारंभिक चरण के प्रयासों के बारे में हमारी जानकारी से पहले शुरू हुआ था, मूल onion routing और ZKS प्रयासों के कई सबक I2P के डिज़ाइन में एकीकृत किए गए थे। directory servers के साथ एक अनिवार्य रूप से विश्वसनीय, केंद्रीकृत सिस्टम बनाने के बजाय, I2P में एक स्व-संगठित नेटवर्क डेटाबेस है जहां प्रत्येक peer अन्य routers की प्रोफाइलिंग की जिम्मेदारी लेता है ताकि यह निर्धारित कर सके कि उपलब्ध संसाधनों का सर्वोत्तम उपयोग कैसे किया जाए। एक और मुख्य अंतर यह है कि जबकि I2P और Tor दोनों स्तरित और क्रमबद्ध पथों (tunnels और circuits/streams) का उपयोग करते हैं, I2P मूल रूप से एक packet switched नेटवर्क है, जबकि Tor मूल रूप से एक circuit switched नेटवर्क है, जो I2P को भीड़भाड़ या अन्य नेटवर्क विफलताओं के आसपास पारदर्शी रूप से route करने, अतिरिक्त pathways संचालित करने, और उपलब्ध संसाधनों में डेटा को load balance करने की अनुमति देता है। जबकि Tor एकीकृत outproxy खोज और चयन की पेशकश करके उपयोगी outproxy कार्यक्षमता प्रदान करता है, I2P ऐसे एप्लिकेशन layer के निर्णयों को I2P के ऊपर चलने वाले applications पर छोड़ देता है — वास्तव में, I2P ने TCP-like streaming library को भी एप्लिकेशन layer में बाहरी बना दिया है, जिससे developers को विभिन्न रणनीतियों के साथ प्रयोग करने, अपने domain specific ज्ञान का फायदा उठाकर बेहतर प्रदर्शन प्रदान करने की अनुमति मिलती है।

गुमनामी के दृष्टिकोण से, मुख्य नेटवर्क की तुलना करने पर काफी समानता है। हालांकि, कुछ मुख्य अंतर हैं। जब आंतरिक विरोधी या अधिकांश बाहरी विरोधियों से निपटते समय, I2P के simplex tunnels केवल फ्लो को देखकर ही Tor के duplex circuits की तुलना में आधा ट्रैफिक डेटा उजागर करते हैं — एक HTTP अनुरोध और प्रतिक्रिया Tor में समान पथ का पालन करेंगे, जबकि I2P में अनुरोध बनाने वाले packets एक या अधिक outbound tunnels के माध्यम से बाहर जाएंगे और प्रतिक्रिया बनाने वाले packets एक या अधिक अलग inbound tunnels के माध्यम से वापस आएंगे। जबकि I2P की peer selection और ordering रणनीतियों को predecessor attacks को पर्याप्त रूप से संबोधित करना चाहिए, यदि bidirectional tunnels पर स्विच करना आवश्यक हो, तो हम समान routers के साथ एक inbound और outbound tunnel बना सकते हैं।

Tor के telescopic tunnel creation के उपयोग में एक और anonymity समस्या आती है, क्योंकि जब circuit में cells एक adversary के node से गुजरते हैं तो सरल packet counting और timing measurements के कारण statistical जानकारी उजागर हो जाती है कि adversary circuit के भीतर कहाँ स्थित है। I2P की unidirectional tunnel creation एक single message के साथ होती है ताकि यह data exposed न हो। tunnel में position को protect करना महत्वपूर्ण है, क्योंकि अन्यथा adversary शक्तिशाली predecessor, intersection, और traffic confirmation attacks की एक श्रृंखला mount करने में सक्षम हो जाएगा।

कुल मिलाकर, Tor और I2P अपने फोकस में एक-दूसरे के पूरक हैं — Tor उच्च गति गुमनाम इंटरनेट outproxying प्रदान करने की दिशा में काम करता है, जबकि I2P अपने आप में एक विकेंद्रीकृत लचीला नेटवर्क प्रदान करने की दिशा में काम करता है। सिद्धांत रूप में, दोनों का उपयोग दोनों उद्देश्यों को प्राप्त करने के लिए किया जा सकता है, लेकिन सीमित विकास संसाधनों को देखते हुए, दोनों की अपनी शक्तियां और कमजोरियां हैं। I2P डेवलपर्स ने I2P के डिज़ाइन का लाभ उठाने के लिए Tor को संशोधित करने के लिए आवश्यक चरणों पर विचार किया है, लेकिन संसाधन की कमी के तहत Tor की व्यवहार्यता की चिंताएं सुझाती हैं कि I2P का packet switching आर्किटेक्चर दुर्लभ संसाधनों का अधिक प्रभावी रूप से उपयोग करने में सक्षम होगा।

### Freenet

*[वेबसाइट](http://www.freenetproject.org/)*

Freenet ने I2P के डिज़ाइन के शुरुआती चरणों में एक बड़ी भूमिका निभाई — नेटवर्क के भीतर पूर्णतः निहित एक जीवंत pseudonymous समुदाय की व्यवहार्यता का प्रमाण देकर, यह दिखाते हुए कि outproxies में निहित खतरों से बचा जा सकता है। I2P का पहला बीज Freenet के लिए एक प्रतिस्थापन संचार परत के रूप में शुरू हुआ, एक scalable, anonymous और secure point to point संचार की जटिलताओं को एक censorship resistant distributed डेटा store की जटिलताओं से अलग करने का प्रयास करते हुए। हालांकि, समय के साथ, Freenet के algorithms में निहित कुछ anonymity और scalability मुद्दों ने यह स्पष्ट कर दिया कि I2P का फोकस Freenet के एक component के रूप में रहने के बजाय एक generic anonymous संचार परत प्रदान करने पर सख्ती से बना रहना चाहिए। वर्षों में, Freenet डेवलपर्स ने पुराने डिज़ाइन की कमजोरियों को देखा है, जिससे उन्होंने सुझाव दिया है कि उन्हें substantial anonymity प्रदान करने के लिए एक "premix" परत की आवश्यकता होगी। दूसरे शब्दों में, Freenet को I2P या Tor जैसे mixnet के ऊपर चलना होगा, जहां "client nodes" mixnet के माध्यम से "server nodes" से डेटा request और publish करते हैं, जो फिर Freenet के heuristic distributed डेटा storage algorithms के अनुसार डेटा को fetch और store करते हैं।

Freenet की कार्यक्षमता I2P की कार्यक्षमता के साथ बहुत पूरक है, क्योंकि Freenet मूल रूप से मध्यम और उच्च विलंबता प्रणालियों के संचालन के लिए कई उपकरण प्रदान करता है, जबकि I2P मूल रूप से कम विलंबता mix network प्रदान करता है जो पर्याप्त गुमनामी प्रदान करने के लिए उपयुक्त है। mixnet को सेंसरशिप-प्रतिरोधी वितरित डेटा स्टोर से अलग करने का तर्क इंजीनियरिंग, गुमनामी, सुरक्षा और संसाधन आवंटन के दृष्टिकोण से अभी भी स्व-स्पष्ट लगता है, इसलिए उम्मीद है कि Freenet टीम उस दिशा में प्रयासों को आगे बढ़ाएगी, यदि वे I2P या Tor जैसे मौजूदा mixnets का पुन: उपयोग (या आवश्यकतानुसार सुधार में मदद) नहीं कर रहे हैं।

---

## परिशिष्ट ए: एप्लीकेशन लेयर

I2P स्वयं वास्तव में बहुत कुछ नहीं करता — यह बस रिमोट गंतव्यों को संदेश भेजता है और स्थानीय गंतव्यों को लक्षित संदेश प्राप्त करता है — अधिकांश दिलचस्प काम इसके ऊपर की परतों में होता है। अकेले, I2P को एक अज्ञात और सुरक्षित IP परत के रूप में देखा जा सकता है, और बंडल की गई [streaming library](#streaming-library) को इसके ऊपर एक अज्ञात और सुरक्षित TCP परत के कार्यान्वयन के रूप में देखा जा सकता है। इससे आगे, [I2PTunnel](#i2ptunnel) I2P नेटवर्क में प्रवेश या निकास के लिए एक जेनेरिक TCP प्रॉक्सी सिस्टम को उजागर करता है, साथ ही विभिन्न नेटवर्क एप्लिकेशन अंतिम उपयोगकर्ताओं के लिए और अधिक कार्यक्षमता प्रदान करते हैं।

### स्ट्रीमिंग लाइब्रेरी

I2P streaming library को एक generic streaming interface (TCP sockets को mirror करने वाला) के रूप में देखा जा सकता है, और इसका implementation एक [sliding window protocol](http://en.wikipedia.org/wiki/Sliding_Window_Protocol) को कई optimizations के साथ support करता है, जो I2P पर high delay को ध्यान में रखते हैं। Individual streams अपना maximum packet size और अन्य options को adjust कर सकते हैं, हालांकि 4KB compressed का default खोए गए messages को retransmit करने की bandwidth costs और multiple messages की latency के बीच एक reasonable tradeoff लगता है।

इसके अतिरिक्त, बाद के संदेशों की अपेक्षाकृत उच्च लागत को ध्यान में रखते हुए, streaming library का संदेशों को निर्धारित करने और वितरित करने के लिए protocol को अनुकूलित किया गया है ताकि पारित किए गए व्यक्तिगत संदेशों में जितनी भी जानकारी उपलब्ध हो, उतनी शामिल की जा सके। उदाहरण के लिए, streaming library के माध्यम से proxied एक छोटे HTTP transaction को एक ही round trip में पूरा किया जा सकता है — पहला संदेश एक SYN, FIN और छोटे payload (एक HTTP request आमतौर पर फिट हो जाता है) को bundle करता है और reply एक SYN, FIN, ACK और छोटे payload (कई HTTP responses फिट हो जाते हैं) को bundle करता है। जबकि HTTP server को बताने के लिए कि SYN/FIN/ACK प्राप्त हो गया है, एक अतिरिक्त ACK भेजा जाना चाहिए, local HTTP proxy तुरंत browser को पूरा response दे सकता है।

समग्र रूप से, हालांकि, streaming library TCP के abstraction से काफी समानता रखती है, अपनी sliding windows, congestion control algorithms (दोनों slow start और congestion avoidance), और सामान्य packet behavior (ACK, SYN, FIN, RST, आदि) के साथ।

### नामकरण लाइब्रेरी और पता पुस्तिका

*अधिक जानकारी के लिए [नामकरण और पता पुस्तिका](/docs/overview/naming/) पृष्ठ देखें।*

*द्वारा विकसित: mihi, Ragnarok*

I2P के भीतर नामकरण शुरुआत से ही एक अक्सर बहस का विषय रहा है जिसमें संभावनाओं के पूरे स्पेक्ट्रम में समर्थक हैं। हालांकि, सुरक्षित संचार और विकेंद्रीकृत संचालन की I2P की अंतर्निहित मांग को देखते हुए, पारंपरिक DNS-शैली नामकरण प्रणाली स्पष्ट रूप से बाहर है, जैसे कि "बहुमत नियम" मतदान प्रणाली भी है। इसके बजाय, I2P एक सामान्य नामकरण लाइब्रेरी और एक आधार कार्यान्वयन के साथ आता है जो स्थानीय नाम से destination मैपिंग पर काम करने के लिए डिज़ाइन किया गया है, साथ ही "Address Book" नामक एक वैकल्पिक ऐड-ऑन एप्लिकेशन भी है। address book एक web-of-trust-संचालित सुरक्षित, वितरित, और मानव पठनीय नामकरण प्रणाली है, जो केवल स्थानीय विशिष्टता को अनिवार्य करके सभी मानव पठनीय नामों के वैश्विक रूप से अद्वितीय होने की मांग का त्याग करती है। जबकि I2P में सभी संदेश उनकी destination द्वारा क्रिप्टोग्राफिक रूप से पता लगाए जाते हैं, विभिन्न लोगों के पास "Alice" के लिए स्थानीय address book entries हो सकती हैं जो विभिन्न destinations को संदर्भित करती हैं। लोग अभी भी अपने web of trust में निर्दिष्ट साथियों की प्रकाशित address books को आयात करके, किसी तीसरे पक्ष के माध्यम से प्रदान की गई entries को जोड़कर, या (यदि कुछ लोग पहले आओ पहले पाओ पंजीकरण प्रणाली का उपयोग करके प्रकाशित address books की एक श्रृंखला का आयोजन करते हैं) लोग इन address books को name servers के रूप में मानने का चुनाव कर सकते हैं, पारंपरिक DNS का अनुकरण करते हुए।

I2P DNS-जैसी सेवाओं के उपयोग को बढ़ावा नहीं देता, क्योंकि किसी साइट को हाइजैक करने से होने वाला नुकसान बहुत भारी हो सकता है — और असुरक्षित destinations का कोई मूल्य नहीं है। DNSsec स्वयं अभी भी registrars और certificate authorities पर निर्भर करता है, जबकि I2P के साथ, किसी destination को भेजे गए requests को intercept नहीं किया जा सकता या reply को spoof नहीं किया जा सकता, क्योंकि वे destination की public keys से encrypted होते हैं, और एक destination स्वयं केवल public keys की एक जोड़ी और एक certificate है। दूसरी ओर DNS-style सिस्टम lookup path पर किसी भी name server को सरल denial of service और spoofing attacks करने की अनुमति देते हैं। किसी केंद्रीकृत certificate authority द्वारा signed responses को authenticate करने वाला certificate जोड़ना कई hostile nameserver समस्याओं को हल कर देगा लेकिन replay attacks के साथ-साथ hostile certificate authority attacks के लिए रास्ता खुला रह जाएगा।

वोटिंग स्टाइल नामकरण भी खतरनाक है, विशेष रूप से anonymous systems में Sybil attacks की प्रभावशीलता को देखते हुए — हमलावर बस मनमाने तौर पर बड़ी संख्या में peers बना सकता है और किसी दिए गए नाम पर कब्जा करने के लिए हर एक के साथ "vote" कर सकता है। Proof-of-work methods का उपयोग identity को non-free बनाने के लिए किया जा सकता है, लेकिन जैसे-जैसे network बढ़ता है, online voting करने के लिए सभी से संपर्क करने के लिए आवश्यक load अव्यावहारिक हो जाता है, या यदि पूरे network से query नहीं किया जाता है, तो विभिन्न प्रकार के उत्तरों तक पहुंच हो सकती है।

हालांकि इंटरनेट की तरह, I2P नामकरण सिस्टम के डिज़ाइन और संचालन को (IP-जैसी) संचार परत से अलग रख रहा है। बंडल की गई नामकरण लाइब्रेरी में एक सरल सेवा प्रदाता इंटरफेस शामिल है जिसमें वैकल्पिक नामकरण सिस्टम प्लग इन हो सकते हैं, जिससे अंतिम उपयोगकर्ता यह तय कर सकें कि वे किस प्रकार के नामकरण ट्रेडऑफ को प्राथमिकता देते हैं।

### I2PTunnel

*विकसित किया गया: mihi द्वारा*

I2PTunnel संभवतः I2P का सबसे लोकप्रिय और बहुमुखी client application है, जो I2P network के अंदर और बाहर दोनों तरफ सामान्य proxying की अनुमति देता है। I2PTunnel को चार अलग proxying applications के रूप में देखा जा सकता है — एक "client" जो inbound TCP connections प्राप्त करता है और उन्हें दिए गए I2P destination पर forward करता है, एक "httpclient" (जिसे "eepproxy" भी कहते हैं) जो HTTP proxy की तरह काम करता है और requests को उपयुक्त I2P destination पर forward करता है (यदि आवश्यक हो तो naming service से पूछताछ करने के बाद), एक "server" जो destination पर inbound I2P streaming connections प्राप्त करता है और उन्हें दिए गए TCP host+port पर forward करता है, और एक "httpserver" जो "server" का विस्तार करके HTTP request और responses को parse करता है ताकि सुरक्षित संचालन की अनुमति मिल सके। एक अतिरिक्त "socksclient" application भी है, लेकिन पहले बताए गए कारणों से इसके उपयोग को प्रोत्साहित नहीं किया जाता।

I2P स्वयं एक outproxy network नहीं है — एक mix net में निहित anonymity और security की चिंताएं जो mix में और बाहर डेटा को forward करता है, ने I2P के design को एक anonymous network प्रदान करने पर केंद्रित रखा है जो बाहरी संसाधनों की आवश्यकता के बिना उपयोगकर्ता की जरूरतों को पूरा करने में सक्षम है। हालांकि, I2PTunnel "httpclient" application outproxying के लिए एक hook प्रदान करता है — यदि अनुरोधित hostname ".i2p" में समाप्त नहीं होता है, तो यह उपयोगकर्ता द्वारा प्रदान किए गए outproxies के set से एक random destination चुनता है और अनुरोध को उनके पास forward कर देता है। ये destinations केवल I2PTunnel "server" instances हैं जो स्वयंसेवकों द्वारा चलाए जाते हैं जिन्होंने स्पष्ट रूप से outproxies चलाने का विकल्प चुना है — कोई भी डिफ़ॉल्ट रूप से outproxy नहीं है, और outproxy चलाना स्वचालित रूप से अन्य लोगों को आपके माध्यम से proxy करने के लिए नहीं कहता। जबकि outproxies में अंतर्निहित कमजोरियां हैं, वे I2P का उपयोग करने के लिए एक सरल proof of concept प्रदान करते हैं और एक threat model के तहत कुछ functionality प्रदान करते हैं जो कुछ उपयोगकर्ताओं के लिए पर्याप्त हो सकता है।

I2PTunnel अधिकांश उपयोग में आने वाले एप्लिकेशन को सक्षम बनाता है। एक वेबसर्वर की ओर इशारा करने वाला "httpserver" किसी भी व्यक्ति को अपनी गुमनाम वेबसाइट (या "I2P Site") चलाने की अनुमति देता है — इस उद्देश्य के लिए I2P के साथ एक वेबसर्वर बंडल किया गया है, लेकिन कोई भी वेबसर्वर उपयोग किया जा सकता है। कोई भी व्यक्ति गुमनाम रूप से होस्ट किए गए IRC सर्वर में से किसी एक की ओर इशारा करने वाला "client" चला सकता है, जिनमें से प्रत्येक अपने स्थानीय IRCd की ओर इशारा करने वाला "server" चला रहा है और अपने स्वयं के "client" tunnel के माध्यम से IRCd के बीच संचार कर रहा है। अंतिम उपयोगकर्ताओं के पास [I2Pmail के](#i2pmail--susimail) POP3 और SMTP गंतव्यों की ओर इशारा करने वाले "client" tunnel भी हैं (जो बदले में केवल POP3 और SMTP सर्वर की ओर इशारा करने वाले "server" instances हैं), साथ ही I2P के CVS सर्वर की ओर इशारा करने वाले "client" tunnel भी हैं, जो गुमनाम विकास की अनुमति देते हैं। कई बार लोगों ने NNTP सर्वर की ओर इशारा करने वाले "server" instances तक पहुंचने के लिए "client" प्रॉक्सी भी चलाए हैं।

### I2PSnark

*I2PSnark विकसित: jrandom, et al, [mjw](http://www.klomp.org/mark/) के [Snark](http://www.klomp.org/snark/) client से पोर्ट किया गया*

I2P इंस्टॉल के साथ बंडल किया गया, I2PSnark एक सरल गुमनाम BitTorrent क्लाइंट प्रदान करता है जिसमें मल्टीटोरेंट क्षमताएं हैं, और सभी कार्यक्षमता को एक सादे HTML वेब इंटरफेस के माध्यम से उपलब्ध कराता है।

### I2Pmail / Susimail

*द्वारा विकसित: postman, susi23, mastiejaner*

I2Pmail एक एप्लिकेशन से अधिक एक सेवा है — postman आंतरिक और बाहरी दोनों ईमेल प्रदान करता है जिसमें POP3 और SMTP सेवा शामिल है I2PTunnel instances के माध्यम से mastiejaner के साथ विकसित किए गए घटकों की एक श्रृंखला तक पहुंच बनाकर, जिससे लोग अपने पसंदीदा मेल clients का उपयोग करके छद्म नाम से मेल भेज और प्राप्त कर सकें। हालांकि, चूंकि अधिकांश मेल clients काफी पहचान वाली जानकारी को उजागर करते हैं, I2P में susi23 का web आधारित susimail client bundled है जो विशेष रूप से I2P की गुमनामी आवश्यकताओं को ध्यान में रखकर बनाया गया है। I2Pmail/mail.i2p सेवा पारदर्शी वायरस filtering के साथ-साथ hashcash augmented quotas के साथ denial of service prevention प्रदान करती है। इसके अलावा, प्रत्येक उपयोगकर्ता का mail.i2p outproxies के माध्यम से delivery से पहले अपनी batching strategy पर नियंत्रण है, जो mail.i2p SMTP और POP3 servers से अलग हैं — outproxies और inproxies दोनों mail.i2p SMTP और POP3 servers के साथ I2P के माध्यम से ही संपर्क करते हैं, इसलिए उन गैर-गुमनाम स्थानों से छेड़छाड़ करना उपयोगकर्ता के मेल accounts या गतिविधि patterns तक पहुंच नहीं देता।
