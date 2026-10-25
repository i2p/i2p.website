---
title: "Tunnel चर्चा"
description: "tunnel padding, fragmentation, और build strategies की ऐतिहासिक खोज"
slug: "tunnel"
aliases:
  - "/hi/docs/discussions/tunnel"
  - "/hi/docs/discussions/tunnel/"
  - "/hi/tunnel_discussion"
  - "/hi/tunnel_discussion/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

नोट: इस दस्तावेज़ में I2P में वर्तमान tunnel implementation के विकल्पों के बारे में पुराणी जानकारी है, और भविष्य की संभावनाओं पर अनुमान है। वर्तमान जानकारी के लिए [tunnel पेज](/docs/specs/tunnel-implementation) देखें।

यह पेज रिलीज़ 0.6.1.10 के अनुसार वर्तमान tunnel बिल्ड implementation को document करता है। पुराना tunnel बिल्ड method, जो रिलीज़ 0.6.1.10 से पहले उपयोग किया जाता था, [पुराने tunnel page](/docs/historical/tunnel-alt) पर documented है।

### कॉन्फ़िगरेशन विकल्प {#config}

उनकी लंबाई के अलावा, प्रत्येक tunnel के लिए अतिरिक्त कॉन्फ़िगरेशन योग्य पैरामीटर हो सकते हैं जिनका उपयोग किया जा सकता है, जैसे कि वितरित संदेशों की आवृत्ति पर throttle, padding का उपयोग कैसे करना चाहिए, tunnel कितने समय तक चालू रहना चाहिए, chaff संदेश inject करना है या नहीं, और यदि कोई है तो कौन सी batching रणनीतियों को अपनाना चाहिए। इनमें से कोई भी वर्तमान में implemented नहीं है।

### पैडिंग विकल्प {#tunnel.padding}

कई tunnel padding रणनीतियाँ संभव हैं, प्रत्येक के अपने फायदे हैं:

- कोई padding नहीं
- यादृच्छिक आकार तक padding
- निश्चित आकार तक padding
- निकटतम KB तक padding
- निकटतम घातांकीय आकार तक padding (2^n bytes)

ये padding रणनीतियों का उपयोग विभिन्न स्तरों पर किया जा सकता है, जो विभिन्न विरोधियों के लिए संदेश आकार की जानकारी के exposure को संबोधित करती हैं। 0.4 network से कुछ आंकड़े एकत्रित करने और समीक्षा करने के बाद, साथ ही anonymity tradeoffs की खोज करने के बाद, हम 1024 bytes के एक निर्धारित tunnel संदेश आकार से शुरुआत कर रहे हैं। हालांकि इसके भीतर, fragmented संदेश स्वयं tunnel द्वारा बिल्कुल भी pad नहीं किए जाते (हालांकि end to end संदेशों के लिए, वे garlic wrapping के हिस्से के रूप में pad हो सकते हैं)।

### विखंडन विकल्प {#tunnel.fragmentation}

पथ के साथ संदेश के आकार को समायोजित करके विरोधियों को संदेशों को टैग करने से रोकने के लिए, सभी tunnel संदेश 1024 बाइट्स के निश्चित आकार में होते हैं। बड़े I2NP संदेशों को समायोजित करने के साथ-साथ छोटे संदेशों को अधिक कुशलता से समर्थन करने के लिए, gateway बड़े I2NP संदेशों को छोटे टुकड़ों में विभाजित करता है जो प्रत्येक tunnel संदेश में समाहित होते हैं। endpoint एक छोटी अवधि के लिए टुकड़ों से I2NP संदेश को पुनर्निर्मित करने का प्रयास करेगा, लेकिन आवश्यकतानुसार उन्हें छोड़ देगा।

Router के पास इस बात की काफी छूट है कि fragments को कैसे व्यवस्थित किया जाए, चाहे उन्हें असक्षम रूप से अलग इकाइयों के रूप में भरा जाए, 1024 byte tunnel messages में अधिक payload फिट करने के लिए संक्षिप्त अवधि के लिए बैच किया जाए, या अवसरवादी रूप से अन्य संदेशों के साथ पैड किया जाए जिन्हें gateway भेजना चाहता था।

### अधिक विकल्प {#tunnel.alternatives}

#### Tunnel प्रसंस्करण को मध्यधारा में समायोजित करें {#tunnel.reroute}

जबकि सरल tunnel रूटिंग एल्गोरिदम अधिकांश मामलों के लिए पर्याप्त होना चाहिए, तीन विकल्प हैं जिन्हें खोजा जा सकता है:

- एक peer को endpoint के अलावा अस्थायी रूप से tunnel के लिए termination point के रूप में कार्य करने के लिए gateway पर उपयोग की जाने वाली encryption को समायोजित करके उन्हें preprocessed I2NP messages का plaintext दें। प्रत्येक peer यह जांच सकता है कि क्या उनके पास plaintext है, प्राप्त होने पर message को संसाधित करता है जैसे कि उनके पास था।
- tunnel में भाग लेने वाले routers को message को आगे भेजने से पहले remix करने की अनुमति दें - इसे उस peer के अपने outbound tunnels में से एक के माध्यम से bounce करके, अगले hop तक पहुंचाने के निर्देशों के साथ।
- tunnel creator के लिए code implement करें ताकि वे tunnel में किसी peer के "next hop" को फिर से परिभाषित कर सकें, जिससे आगे dynamic redirection की अनुमति मिले।

#### द्विदिशीय Tunnels का उपयोग करें {#tunnel.bidirectional}

inbound और outbound संचार के लिए दो अलग tunnels का उपयोग करने की वर्तमान रणनीति एकमात्र उपलब्ध तकनीक नहीं है, और इसके गुमनामी संबंधी प्रभाव हैं। सकारात्मक पहलू पर, अलग tunnels का उपयोग करके यह tunnel के प्रतिभागियों के विश्लेषण के लिए उजागर होने वाले ट्रैफिक डेटा को कम कर देता है - उदाहरण के लिए, web browser से outbound tunnel में peers केवल HTTP GET के ट्रैफिक को देखेंगे, जबकि inbound tunnel में peers tunnel के साथ वितरित पेलोड को देखेंगे। bidirectional tunnels के साथ, सभी प्रतिभागियों के पास इस तथ्य तक पहुंच होगी कि जैसे 1KB एक दिशा में भेजा गया, फिर दूसरी में 100KB। नकारात्मक पहलू पर, unidirectional tunnels का उपयोग करने का मतलब है कि peers के दो सेट हैं जिन्हें प्रोफाइल और हिसाब में रखा जाना चाहिए, और predecessor attacks की बढ़ी हुई गति को संबोधित करने के लिए अतिरिक्त सावधानी बरतनी चाहिए। नीचे बताई गई tunnel pooling और building प्रक्रिया को predecessor attack की चिंताओं को कम करना चाहिए, हालांकि यदि वांछित हो, तो inbound और outbound दोनों tunnels को समान peers के साथ build करना बहुत कठिन नहीं होगा।

#### बैकचैनल संचार {#tunnel.backchannel}

इस समय, उपयोग किए जाने वाले IV values यादृच्छिक values हैं। हालांकि, उस 16 byte value का उपयोग gateway से endpoint तक control messages भेजने के लिए किया जा सकता है, या outbound tunnels पर, gateway से किसी भी peer तक। Inbound gateway एक बार IV में कुछ निश्चित values को encode कर सकता है, जिन्हें endpoint recover कर सकेगा (क्योंकि यह जानता है कि endpoint भी creator है)। Outbound tunnels के लिए, creator tunnel creation के दौरान participants को कुछ निश्चित values दे सकता है (जैसे "यदि आप IV के रूप में 0x0 देखते हैं, तो इसका मतलब X है", "0x1 का मतलब Y है", आदि)। चूंकि outbound tunnel पर gateway भी creator है, वे एक IV बना सकते हैं ताकि किसी भी peer को सही value मिले। Tunnel creator inbound tunnel gateway को IV values की एक series भी दे सकता है जिसका उपयोग वह gateway व्यक्तिगत participants के साथ बिल्कुल एक बार संवाद करने के लिए कर सकता है (हालांकि इसमें collusion detection के संबंध में समस्याएं होंगी)।

यह तकनीक बाद में stream के बीच में message पहुंचाने के लिए इस्तेमाल की जा सकती है, या inbound gateway को endpoint को बताने की अनुमति देने के लिए कि उस पर DoS हमला हो रहा है या वह जल्द ही fail होने वाला है। इस समय, इस backchannel का उपयोग करने की कोई योजना नहीं है।

#### परिवर्तनीय आकार tunnel संदेश {#tunnel.variablesize}

जबकि transport layer का अपना निश्चित या परिवर्तनीय message size हो सकता है, अपने fragmentation का उपयोग करते हुए, tunnel layer इसके बजाय परिवर्तनीय आकार के tunnel messages का उपयोग कर सकती है। यह अंतर threat models का मुद्दा है - transport layer पर निश्चित आकार बाहरी adversaries को उजागर होने वाली जानकारी को कम करने में मदद करता है (हालांकि समग्र flow analysis अभी भी काम करती है), लेकिन आंतरिक adversaries (अर्थात tunnel participants) के लिए message size उजागर हो जाता है। निश्चित आकार के tunnel messages tunnel participants को उजागर होने वाली जानकारी को कम करने में मदद करते हैं, लेकिन tunnel endpoints और gateways को उजागर होने वाली जानकारी को छुपाते नहीं हैं। निश्चित आकार के end to end messages नेटवर्क में सभी peers को उजागर होने वाली जानकारी को छुपाते हैं।

हमेशा की तरह, यह इस बात का सवाल है कि I2P किससे सुरक्षा प्रदान करने की कोशिश कर रहा है। परिवर्तनशील आकार के tunnel संदेश खतरनाक हैं, क्योंकि वे प्रतिभागियों को संदेश के आकार को ही अन्य प्रतिभागियों के साथ backchannel के रूप में उपयोग करने की अनुमति देते हैं - उदाहरण के लिए यदि आप 1337 बाइट का संदेश देखते हैं, तो आप किसी अन्य मिलीभगत करने वाले peer के साथ एक ही tunnel पर हैं। अनुमतित आकारों के एक निश्चित सेट (1024, 2048, 4096, आदि) के साथ भी, वह backchannel अभी भी मौजूद है क्योंकि peers प्रत्येक आकार की आवृत्ति को carrier के रूप में उपयोग कर सकते हैं (उदाहरण के लिए दो 1024 बाइट संदेशों के बाद एक 8192)। छोटे संदेशों में headers (IV, tunnel ID, hash portion, आदि) का overhead लगता है, लेकिन बड़े निश्चित आकार के संदेश या तो latency बढ़ाते हैं (batching के कारण) या dramatically overhead बढ़ाते हैं (padding के कारण)। Fragmentation overhead को amortize करने में मदद करता है, खोए हुए fragments के कारण संभावित संदेश हानि की कीमत पर।

Timing attacks भी fixed size messages की प्रभावशीलता की समीक्षा करते समय प्रासंगिक हैं, हालांकि इन्हें प्रभावी होने के लिए नेटवर्क गतिविधि पैटर्न का व्यापक दृश्य चाहिए होता है। tunnel में अत्यधिक कृत्रिम देरी का पता tunnel के निर्माता द्वारा आवधिक परीक्षण के कारण लगा लिया जाता है, जिससे वह पूरा tunnel खराब हो जाता है और उसके भीतर के peers के profiles को समायोजित किया जाता है।

### वैकल्पिक निर्माण {#tunnel.building.alternatives}

संदर्भ: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

#### पुराना Tunnel निर्माण विधि {#tunnel.building.old}

पुराना tunnel निर्माण विधि, जो रिलीज़ 0.6.1.10 से पहले उपयोग की जाती थी, [पुराने tunnel पृष्ठ](/docs/historical/tunnel-alt) पर प्रलेखित है। यह एक "सभी एक साथ" या "समानांतर" विधि थी, जहाँ संदेश सभी प्रतिभागियों को समानांतर में भेजे जाते थे।

#### वन-शॉट टेलीस्कोपिक बिल्डिंग {#tunnel.building.oneshot}

नोट: यह वर्तमान विधि है।

exploratory tunnels के उपयोग को लेकर एक प्रश्न उठा है कि tunnel creation messages भेजने और प्राप्त करने के लिए इसका उपयोग कैसे tunnel की predecessor attacks के प्रति संवेदनशीलता को प्रभावित करता है। जबकि उन tunnels के endpoints और gateways network में यादृच्छिक रूप से वितरित होंगे (संभवतः उस सेट में tunnel creator भी शामिल हो), एक अन्य विकल्प यह है कि tunnel pathways का उपयोग करके request और response को आगे भेजा जाए, जैसा कि [Tor](https://www.torproject.org/) में किया जाता है। हालांकि, इससे tunnel creation के दौरान जानकारी का रिसाव हो सकता है, जिससे peers यह पता लगा सकते हैं कि tunnel में आगे कितने hops हैं, tunnel के निर्माण के दौरान timing या packet count की निगरानी करके।

#### "इंटरैक्टिव" टेलीस्कोपिक बिल्डिंग {#tunnel.building.telescoping}

मौजूदा tunnel के हिस्से के माध्यम से एक संदेश के साथ एक समय में एक hop बनाएं। इसमें बड़ी समस्याएं हैं क्योंकि peers संदेशों की गिनती करके tunnel में अपनी स्थिति निर्धारित कर सकते हैं।

#### प्रबंधन के लिए गैर-अन्वेषणकारी Tunnels {#tunnel.building.nonexploratory}

tunnel निर्माण प्रक्रिया का दूसरा विकल्प यह है कि router को अतिरिक्त non-exploratory inbound और outbound pools का सेट दिया जाए, जिनका उपयोग tunnel request और response के लिए किया जा सके। यह मानते हुए कि router के पास network का अच्छी तरह से एकीकृत दृश्य है, यह आवश्यक नहीं होना चाहिए, लेकिन यदि router किसी तरह से विभाजित था, तो tunnel प्रबंधन के लिए non-exploratory pools का उपयोग करने से इस बारे में जानकारी के रिसाव को कम किया जा सकेगा कि router के partition में कौन से peers हैं।

#### खोजपूर्ण अनुरोध वितरण {#tunnel.building.exploratory}

तीसरा विकल्प, जो I2P 0.6.1.10 तक उपयोग किया गया था, व्यक्तिगत tunnel request संदेशों को garlic encrypt करता है और उन्हें hops तक व्यक्तिगत रूप से पहुंचाता है, उन्हें exploratory tunnels के माध्यम से प्रसारित करता है और उनका उत्तर एक अलग exploratory tunnel में वापस आता है। इस रणनीति को ऊपर बताई गई रणनीति के पक्ष में छोड़ दिया गया है।

#### अधिक इतिहास और चर्चा {#history}

Variable Tunnel Build Message के आने से पहले, कम से कम दो समस्याएं थीं:

1. संदेशों का आकार (8-hop अधिकतम के कारण, जबकि सामान्य tunnel लंबाई 2 या 3 hops होती है...
   और वर्तमान अनुसंधान दर्शाता है कि 3 से अधिक hops anonymity को बढ़ाते नहीं हैं);
2. उच्च निर्माण विफलता दर, विशेष रूप से लंबी (और exploratory) tunnels के लिए, क्योंकि सभी hops को सहमत होना चाहिए या tunnel को त्याग दिया जाता है।

VTBM ने #1 को ठीक किया है और #2 में सुधार किया है।

Welterde ने parallel method में संशोधन का प्रस्ताव दिया है जो reconfiguration की अनुमति देगा। Sponge ने किसी प्रकार के 'tokens' का उपयोग करने का प्रस्ताव दिया है।

tunnel निर्माण के किसी भी छात्र को वर्तमान विधि तक पहुंचने वाले ऐतिहासिक रिकॉर्ड का अध्ययन करना चाहिए, विशेष रूप से विभिन्न विधियों में मौजूद विभिन्न गुमनामी कमजोरियों का। अक्टूबर 2005 के मेल अभिलेखागार विशेष रूप से सहायक हैं। जैसा कि [tunnel creation specification](/docs/specs/tunnel-creation) पर बताया गया है, वर्तमान रणनीति predecessor attack के संबंध में Michael Rogers, Matthew Toseland (toad), और jrandom के बीच I2P mailing list पर हुई चर्चा के दौरान आई।

#### Peer Ordering Alternatives {#ordering}

एक कम सख्त क्रम भी संभव है, जो यह सुनिश्चित करता है कि जबकि A के बाद का hop B हो सकता है, B कभी भी A से पहले नहीं हो सकता। अन्य कॉन्फ़िगरेशन विकल्पों में केवल inbound tunnel gateways और outbound tunnel endpoints को fixed रखने, या MTBF दर पर rotate करने की क्षमता शामिल है।

## मिक्सिंग/बैचिंग {#tunnel.mixing}

gateway और प्रत्येक hop पर messages को delay करने, reorder करने, reroute करने, या padding करने के लिए कौन सी रणनीतियों का उपयोग किया जाना चाहिए? यह कितनी हद तक automatically किया जाना चाहिए, कितना per tunnel या per hop setting के रूप में configure किया जाना चाहिए, और tunnel का creator (और बदले में, user) इस operation को कैसे control करना चाहिए? यह सब अज्ञात है, भविष्य की release के लिए काम किया जाना बाकी है।
