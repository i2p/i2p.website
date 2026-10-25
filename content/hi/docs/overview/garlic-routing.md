---
title: "Garlic Routing"
description: "I2P में garlic routing शब्दावली, आर्किटेक्चर और कार्यान्वयन को समझना"
slug: "garlic-routing"
aliases:
  - "/hi/how_garlicrouting"
  - "/hi/how_garlicrouting/"
lastUpdated: "2025-10"
accurateFor: "0.9.12"
---

## Garlic Routing और "Garlic" शब्दावली

"गार्लिक रूटिंग" और "garlic encryption" शब्दों का उपयोग अक्सर I2P की तकनीक का उल्लेख करते समय काफी शिथिलता से किया जाता है। यहाँ, हम इन शब्दों का इतिहास, विभिन्न अर्थ, और I2P में "गार्लिक" विधियों के उपयोग को समझाते हैं।

"Garlic routing" शब्द पहली बार [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) द्वारा Roger Dingledine के Free Haven [Master's thesis](https://www.freehaven.net/papers.html) के Section 8.1.1 (जून 2000) में गढ़ा गया था, जो [Onion Routing](https://www.onion-router.net/) से व्युत्पन्न है।

"Garlic" का इस्तेमाल मूल रूप से I2P डेवलपर्स द्वारा इसलिए किया गया हो सकता है क्योंकि I2P एक प्रकार की bundling को implement करता है जैसा कि Freedman ने वर्णन किया है, या फिर बस Tor से सामान्य अंतर को emphasize करने के लिए। विशिष्ट तर्क इतिहास में खो गया हो सकता है। आम तौर पर, जब I2P की बात करते हैं, तो "garlic" शब्द का मतलब तीन चीजों में से एक हो सकता है:

1. स्तरित एन्क्रिप्शन
2. कई संदेशों को एक साथ बंडल करना
3. ElGamal/AES एन्क्रिप्शन

दुर्भाग्यवश, पिछले वर्षों में I2P द्वारा "garlic" शब्दावली का उपयोग हमेशा सटीक नहीं रहा है; इसलिए पाठकों को इस शब्द के सामने आने पर सावधान रहने की सलाह दी जाती है। उम्मीद है कि नीचे दी गई व्याख्या से बात स्पष्ट हो जाएगी।

### स्तरित एन्क्रिप्शन

Onion routing एक तकनीक है जो peers (साथियों) की श्रृंखला के माध्यम से paths (पथ) या tunnels (सुरंगें) बनाने के लिए उपयोग की जाती है, और फिर उस tunnel का उपयोग करने के लिए। संदेशों को मूल भेजने वाले द्वारा बार-बार encrypted (एन्क्रिप्ट) किया जाता है, और फिर हर hop (छलांग) पर decrypted (डिक्रिप्ट) किया जाता है। निर्माण चरण के दौरान, केवल अगली hop के लिए routing निर्देश प्रत्येक peer के सामने प्रकट होते हैं। संचालन चरण के दौरान, संदेश tunnel के माध्यम से पारित होते हैं, और संदेश तथा इसके routing निर्देश केवल tunnel के endpoint (अंतिम बिंदु) पर ही प्रकट होते हैं।

यह Mixmaster के संदेश भेजने के तरीके के समान है (देखें [नेटवर्क तुलनाएं](/docs/overview/comparison/)) - एक संदेश लेना, उसे प्राप्तकर्ता की public key से एन्क्रिप्ट करना, फिर उस एन्क्रिप्टेड संदेश को लेकर उसे (अगला hop निर्दिष्ट करने वाले निर्देशों के साथ) एन्क्रिप्ट करना, और फिर उस परिणामी एन्क्रिप्टेड संदेश को लेकर इसी तरह आगे करते रहना, जब तक कि path के प्रत्येक hop के लिए एन्क्रिप्शन की एक परत न हो जाए।

इस अर्थ में, एक सामान्य अवधारणा के रूप में "garlic routing" "onion routing" के समान है। जैसा कि I2P में लागू किया गया है, निश्चित रूप से, Tor में implementation से कई अंतर हैं; नीचे देखें। फिर भी, काफी समानताएं हैं जैसे कि I2P को [onion routing पर बड़ी मात्रा में अकादमिक अनुसंधान](https://www.onion-router.net/Publications.html), [Tor, और समान mixnets](https://freehaven.net/anonbib/topic.html) से लाभ मिलता है।

### कई संदेशों को एक साथ बंडल करना

Michael Freedman ने "garlic routing" को onion routing के विस्तार के रूप में परिभाषित किया, जिसमें कई संदेशों को एक साथ बंडल किया जाता है। उन्होंने प्रत्येक संदेश को एक "bulb" कहा। सभी संदेश, जिनमें से प्रत्येक के अपने डिलीवरी निर्देश होते हैं, endpoint पर उजागर होते हैं। यह onion routing "reply block" को मूल संदेश के साथ कुशलता से बंडल करने की अनुमति देता है।

यह अवधारणा I2P में लागू की गई है, जैसा कि नीचे वर्णित है। garlic "bulbs" के लिए हमारा शब्द "cloves" है। केवल एक single message के बजाय कोई भी संख्या में messages समाहित हो सकते हैं। यह Tor में लागू onion routing से एक महत्वपूर्ण अंतर है। हालांकि, यह I2P और Tor के बीच कई प्रमुख architectural अंतरों में से केवल एक है; शायद यह अकेले ही terminology में बदलाव को उचित ठहराने के लिए पर्याप्त नहीं है।

Freedman द्वारा वर्णित विधि से एक और अंतर यह है कि path एकदिशीय है - यहाँ कोई "turning point" नहीं है जैसा कि onion routing या mixmaster reply blocks में देखा जाता है, जो algorithm को बहुत सरल बनाता है और अधिक लचीली और विश्वसनीय delivery की अनुमति देता है।

### ElGamal/AES एन्क्रिप्शन

कुछ मामलों में, "garlic encryption" का मतलब केवल [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) एन्क्रिप्शन हो सकता है (कई परतों के बिना)।

---

## I2P में "Garlic" विधियाँ

अब जबकि हमने विभिन्न "garlic" शब्दों को परिभाषित किया है, हम कह सकते हैं कि I2P तीन स्थानों पर garlic routing, bundling और encryption का उपयोग करता है:

1. tunnels के निर्माण और उनके माध्यम से routing के लिए (layered encryption)
2. end to end message delivery की सफलता या असफलता निर्धारित करने के लिए (bundling)
3. कुछ network database entries को publish करने के लिए (सफल traffic analysis attack की संभावना को कम करना) (ElGamal/AES)

ऐसे भी महत्वपूर्ण तरीके हैं जिनसे इस तकनीक का उपयोग नेटवर्क के प्रदर्शन को बेहतर बनाने के लिए किया जा सकता है, transport latency/throughput tradeoffs का फायदा उठाकर, और विश्वसनीयता बढ़ाने के लिए redundant paths के माध्यम से डेटा को शाखाओं में बांटकर।

### Tunnel निर्माण और Routing

I2P में, tunnel एकदिशीय होते हैं। प्रत्येक पार्टी दो tunnel बनाती है, एक आउटबाउंड के लिए और एक इनबाउंड ट्रैफिक के लिए। इसलिए, एक single round-trip message और reply के लिए चार tunnel की आवश्यकता होती है।

Tunnels का निर्माण और उपयोग layered encryption के साथ किया जाता है। इसका वर्णन [tunnel implementation page](/docs/specs/tunnel-implementation/) पर दिया गया है। हम encryption के लिए [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) का उपयोग करते हैं।

Tunnels सभी [I2NP messages](/docs/specs/i2np/) को ट्रांसपोर्ट करने के लिए एक सामान्य-उद्देश्य तंत्र हैं, और Garlic Messages का उपयोग tunnels बनाने के लिए नहीं किया जाता है। हम outbound tunnel endpoint पर unwrapping के लिए कई I2NP messages को एक single Garlic Message में bundle नहीं करते हैं; tunnel encryption पर्याप्त है।

### एंड-टू-एंड मैसेज बंडलिंग

tunnel की ऊपरी परत पर, I2P [Destinations](/docs/specs/common-structures/) के बीच end-to-end messages पहुंचाता है। जैसे एक single tunnel के भीतर होता है, हम encryption के लिए [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) का उपयोग करते हैं। प्रत्येक client message जो [I2CP interface](/docs/api/i2cp/) के माध्यम से router को पहुंचाया जाता है, एक Garlic Message के अंदर अपने Delivery Instructions के साथ एक single Garlic Clove बन जाता है। Delivery Instructions एक Destination, Router, या Tunnel निर्दिष्ट कर सकते हैं।

आमतौर पर, एक Garlic Message में केवल एक clove होगा। हालांकि, router समय-समय पर Garlic Message में दो अतिरिक्त cloves को bundle करेगा:

![Garlic Message Cloves](/images/garliccloves.svg)

1. **एक डिलिवरी स्टेटस मैसेज**, जिसमें डिलिवरी निर्देश होते हैं जो निर्दिष्ट करते हैं कि इसे पुष्टिकरण के रूप में मूल router को वापस भेजा जाए। यह संदर्भों में वर्णित "reply block" या "reply onion" के समान है। इसका उपयोग end to end मैसेज डिलिवरी की सफलता या विफलता निर्धारित करने के लिए किया जाता है। मूल router, अपेक्षित समयावधि के भीतर डिलिवरी स्टेटस मैसेज प्राप्त न करने पर, दूर के Destination के लिए routing में संशोधन कर सकता है, या अन्य कार्रवाई कर सकता है।

2. **एक Database Store Message**, जिसमें मूल Destination के लिए एक LeaseSet होता है, जिसमें दूर के छोर के destination के router को निर्दिष्ट करने वाले Delivery Instructions होते हैं। LeaseSet को समय-समय पर बंडल करके, router यह सुनिश्चित करता है कि दूर का छोर संचार बनाए रख सकेगा। अन्यथा दूर के छोर को network database entry के लिए floodfill router से पूछताछ करनी होगी, और सभी LeaseSets को network database में प्रकाशित करना होगा, जैसा कि [network database page](/docs/specs/common-structures/) पर समझाया गया है।

डिफ़ॉल्ट रूप से, Delivery Status और Database Store Messages को bundle किया जाता है जब स्थानीय LeaseSet में बदलाव होता है, जब अतिरिक्त Session Tags वितरित किए जाते हैं, या यदि पिछले मिनट में messages को bundle नहीं किया गया हो।

स्पष्ट रूप से, अतिरिक्त संदेश वर्तमान में विशिष्ट उद्देश्यों के लिए बंडल किए गए हैं, और सामान्य-उद्देश्य routing योजना का हिस्सा नहीं हैं।

रिलीज 0.9.12 से, Delivery Status Message को मूल भेजने वाले द्वारा दूसरे Garlic Message में लपेटा जाता है ताकि सामग्री एन्क्रिप्टेड हो और वापसी के रास्ते पर routers को दिखाई न दे।

### Floodfill Network Database में भंडारण

जैसा कि [network database पृष्ठ](/docs/specs/common-structures/) पर समझाया गया है, स्थानीय LeaseSets को floodfill routers में एक Database Store Message में भेजा जाता है जो Garlic Message में wrapped होता है ताकि यह tunnel के outbound gateway के लिए दिखाई न दे।

---

## भविष्य का कार्य

Garlic Message तंत्र बहुत लचीला है और कई प्रकार के mixnet डिलीवरी तरीकों को लागू करने के लिए एक संरचना प्रदान करता है। tunnel message Delivery Instructions में अप्रयुक्त देरी विकल्प के साथ मिलकर, batching, देरी, मिश्रण और रूटिंग रणनीतियों का एक व्यापक स्पेक्ट्रम संभव है।

विशेष रूप से, outbound tunnel endpoint पर बहुत अधिक लचीलेपन की संभावना है। संदेशों को वहां से कई tunnels में से किसी एक में रूट किया जा सकता है (इस प्रकार point-to-point कनेक्शन्स को कम करना), या redundancy के लिए कई tunnels में multicast किया जा सकता है, या streaming audio और video के लिए।

ऐसे प्रयोग सुरक्षा और गुमनामी सुनिश्चित करने की आवश्यकता के साथ टकराव हो सकते हैं, जैसे कि निश्चित routing paths को सीमित करना, विभिन्न paths पर forward किए जा सकने वाले I2NP messages के प्रकारों को प्रतिबंधित करना, और निश्चित message expiration times को लागू करना।

ElGamal/AES encryption के हिस्से के रूप में, एक garlic message में भेजने वाले द्वारा निर्दिष्ट मात्रा में padding डेटा होता है, जो भेजने वाले को traffic analysis के खिलाफ सक्रिय प्रतिकारी उपाय अपनाने की अनुमति देता है। वर्तमान में इसका उपयोग नहीं किया जा रहा है, 16 bytes के गुणज तक pad करने की आवश्यकता के अतिरिक्त।

[floodfill routers](/docs/specs/common-structures/) से और उनतक अतिरिक्त संदेशों का एन्क्रिप्शन।

---

## संदर्भ

- garlic routing शब्द पहली बार Roger Dingledine के Free Haven [Master's thesis](https://www.freehaven.net/papers.html) (जून 2000) में गढ़ा गया था, [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) द्वारा लिखा गया धारा 8.1.1 देखें।
- [Onion Router Publications](https://www.onion-router.net/Publications.html)
- [Onion Routing (Wikipedia)](https://en.wikipedia.org/wiki/Onion_routing)
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)
- [Tor Project](https://www.torproject.org/)
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)
- Onion routing का पहली बार वर्णन 1996 में David M. Goldschlag, Michael G. Reed, और Paul F. Syverson द्वारा [Hiding Routing Information](https://www.onion-router.net/Publications/IH-1996.pdf) में किया गया था।
