---
title: "Tunnel निर्माण विनिर्देश (ElGamal)"
description: "विरासत ElGamal-आधारित tunnel निर्माण विनिर्देश, X25519 द्वारा प्रतिस्थापित"
slug: "elgamal-tunnel-creation"
aliases:
  - "/hi/tunnel-alt-creation"
  - "/hi/tunnel-alt-creation/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## अवलोकन {#tunnelcreate-overview}

नोट: अप्रचलित - यह ElGamal tunnel build specification है। वर्तमान विधि के लिए [X25519 tunnel build specification](/docs/specs/tunnel-creation-ecies) देखें।

यह दस्तावेज़ "नॉन-इंटरैक्टिव टेलिस्कोपिंग" विधि का उपयोग करके tunnel बनाने के लिए उपयोग किए जाने वाले एन्क्रिप्टेड tunnel build संदेशों का विवरण निर्दिष्ट करता है। प्रक्रिया का अवलोकन, peer selection और ordering methods सहित, tunnel build दस्तावेज़ [TUNNEL-IMPL](/docs/specs/tunnel-implementation) देखें।

टनल निर्माण एक एकल संदेश द्वारा पूरा किया जाता है जो टनल में पीयर के पथ के साथ पारित किया जाता है, स्थान पर पुनर्लिखित किया जाता है, और टनल निर्माता को वापस भेजा जाता है। यह एकल टनल संदेश परिवर्तनीय संख्या के रिकॉर्ड्स (8 तक) से बना होता है - टनल में प्रत्येक संभावित पीयर के लिए एक। व्यक्तिगत रिकॉर्ड्स असममित रूप से (ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal)) एन्क्रिप्ट किए जाते हैं ताकि केवल पथ के साथ एक विशिष्ट पीयर द्वारा पढ़े जा सकें, जबकि प्रत्येक हॉप पर सममित एन्क्रिप्शन (AES [CRYPTO-AES](/docs/specs/cryptography#AES)) की एक अतिरिक्त परत जोड़ी जाती है ताकि असममित रूप से एन्क्रिप्ट किए गए रिकॉर्ड को केवल उपयुक्त समय पर ही उजागर किया जा सके।

### रिकॉर्ड्स की संख्या {#number}

सभी रिकॉर्ड्स में वैध डेटा होना आवश्यक नहीं है। 3-hop tunnel के लिए build message में, उदाहरण के लिए, tunnel की वास्तविक लंबाई को प्रतिभागियों से छुपाने के लिए अधिक रिकॉर्ड्स हो सकते हैं। दो प्रकार के build message हैं। मूल Tunnel Build Message ([TBM](/docs/specs/i2np#msg-tunnelbuild)) में 8 रिकॉर्ड्स होते हैं, जो किसी भी व्यावहारिक tunnel लंबाई के लिए पर्याप्त से अधिक है। नवीन Variable Tunnel Build Message ([VTBM](/docs/specs/i2np#msg-variabletunnelbuild)) में 1 से 8 रिकॉर्ड्स होते हैं। प्रवर्तक message के आकार को वांछित tunnel लंबाई अस्पष्टता की मात्रा के साथ संतुलित कर सकता है।

वर्तमान नेटवर्क में, अधिकांश tunnel 2 या 3 hops लंबे होते हैं। वर्तमान implementation 4 hops या कम के tunnel बनाने के लिए 5-record VTBM का उपयोग करता है, और लंबे tunnel के लिए 8-record TBM का उपयोग करता है। 5-record VTBM (जो fragmented होने पर तीन 1KB tunnel messages में फिट हो जाता है) नेटवर्क ट्रैफिक को कम करता है और build success rate बढ़ाता है, क्योंकि छोटे messages के drop होने की संभावना कम होती है।

उत्तर संदेश का प्रकार और लंबाई build संदेश के समान होनी चाहिए।

### Request Record विनिर्देश {#tunnelcreate-requestrecord}

I2NP Specification [BRR](/docs/specs/i2np#struct-buildrequestrecord) में भी निर्दिष्ट है।

रिकॉर्ड का क्लियरटेक्स्ट, केवल पूछे जा रहे हॉप को दिखाई देता है:

```
bytes     0-3: tunnel ID to receive messages as, nonzero
bytes    4-35: local router identity hash
bytes   36-39: next tunnel ID, nonzero
bytes   40-71: next router identity hash
bytes  72-103: AES-256 tunnel layer key
bytes 104-135: AES-256 tunnel IV key
bytes 136-167: AES-256 reply key
bytes 168-183: AES-256 reply IV
byte      184: flags
bytes 185-188: request time (in hours since the epoch, rounded down)
bytes 189-192: next message ID
bytes 193-221: uninterpreted / random padding
```
अगली tunnel ID और अगली router identity hash फील्ड का उपयोग tunnel में अगले hop को निर्दिष्ट करने के लिए किया जाता है, हालांकि एक outbound tunnel endpoint के लिए, वे निर्दिष्ट करते हैं कि पुनर्लिखित tunnel creation reply संदेश कहाँ भेजा जाना चाहिए। इसके अलावा, अगली संदेश ID निर्दिष्ट करती है कि संदेश (या उत्तर) को कौन सी संदेश ID का उपयोग करना चाहिए।

tunnel layer key, tunnel IV key, reply key, और reply IV प्रत्येक 32-बाइट के यादृच्छिक मान हैं जो creator द्वारा उत्पन्न किए जाते हैं, केवल इस build request record में उपयोग के लिए।

flags फ़ील्ड में निम्नलिखित शामिल है:

```
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
Bit 7 इंगित करता है कि hop एक inbound gateway (IBGW) होगा। Bit 6 इंगित करता है कि hop एक outbound endpoint (OBEP) होगा। यदि कोई भी bit सेट नहीं है, तो hop एक intermediate participant होगा। दोनों एक साथ सेट नहीं हो सकते।

#### अनुरोध रिकॉर्ड निर्माण

हर hop को एक यादृच्छिक Tunnel ID मिलता है, जो शून्य नहीं होता। वर्तमान और अगले-hop के Tunnel ID भरे जाते हैं। हर record को एक यादृच्छिक tunnel IV key, reply IV, layer key, और reply key मिलती है।

#### Request Record Encryption {#encryption}

वह cleartext record ElGamal 2048 encrypted [CRYPTO-ELG](/docs/specs/cryptography#elgamal) है hop की public encryption key के साथ और 528 byte record में formatted है:

```
bytes   0-15: First 16 bytes of the SHA-256 of the current hop's router identity
bytes 16-527: ElGamal-2048 encrypted request record
```
512-byte एन्क्रिप्टेड रिकॉर्ड में, ElGamal डेटा में 514-byte ElGamal एन्क्रिप्टेड ब्लॉक [CRYPTO-ELG](/docs/specs/cryptography#elgamal) के bytes 1-256 और 258-513 शामिल हैं। ब्लॉक से दो padding bytes (स्थान 0 और 257 पर शून्य bytes) हटा दिए जाते हैं।

चूंकि cleartext पूरे field का उपयोग करता है, इसलिए `SHA256(cleartext) + cleartext` के अतिरिक्त किसी अतिरिक्त padding की आवश्यकता नहीं है।

प्रत्येक 528-byte रिकॉर्ड को फिर पुनरावृत्ति के साथ एन्क्रिप्ट किया जाता है (AES डिक्रिप्शन का उपयोग करते हुए, प्रत्येक hop के लिए reply key और reply IV के साथ) ताकि router identity केवल संबंधित hop के लिए ही cleartext में हो।

### हॉप प्रसंस्करण और एन्क्रिप्शन {#tunnelcreate-hopprocessing}

जब एक hop को TunnelBuildMessage मिलता है, तो वह उसमें निहित records को देखता है और अपने identity hash (16 bytes तक trimmed) से शुरू होने वाले record को खोजता है। फिर वह उस record से ElGamal block को decrypt करता है और protected cleartext को retrieve करता है। उस समय, वे AES-256 reply key को Bloom filter में डालकर सुनिश्चित करते हैं कि tunnel request duplicate नहीं है। Duplicate या invalid requests को drop कर दिया जाता है। जो records वर्तमान घंटे या पिछले घंटे (यदि घंटे की शुरुआत के तुरंत बाद हो) के stamp के साथ नहीं हैं, उन्हें drop करना होगा। उदाहरण के लिए, timestamp में घंटे को लें, इसे full time में convert करें, फिर यदि यह वर्तमान समय से 65 मिनट से अधिक पीछे या 5 मिनट से अधिक आगे है, तो यह invalid है। Bloom filter की duration कम से कम एक घंटा (plus कुछ मिनट, clock skew के लिए allow करने हेतु) होनी चाहिए, ताकि वर्तमान घंटे में duplicate records जो record में hour timestamp की जांच करके reject नहीं हुए हैं, वे filter द्वारा reject हो जाएं।

यह निर्णय लेने के बाद कि वे tunnel में भाग लेने के लिए सहमत होंगे या नहीं, वे उस record को बदल देते हैं जिसमें अनुरोध था, एक encrypted reply block के साथ। अन्य सभी records को शामिल reply key और IV के साथ AES-256 encrypted [CRYPTO-AES](/docs/specs/cryptography#AES) किया जाता है। प्रत्येक को समान reply key और reply IV के साथ अलग से AES/CBC encrypted किया जाता है। CBC mode को records में आगे जारी (chained) नहीं रखा जाता।

प्रत्येक hop केवल अपना response जानता है। यदि यह सहमत है, तो यह tunnel की अवधि समाप्त होने तक इसे बनाए रखेगा, भले ही इसका उपयोग न हो, क्योंकि यह नहीं जान सकता कि अन्य सभी hops सहमत हुए हैं या नहीं।

#### Reply Record Specification {#tunnelcreate-replyrecord}

वर्तमान hop अपना record पढ़ने के बाद, वे इसे एक reply record से बदल देते हैं जिसमें यह बताया जाता है कि वे tunnel में भाग लेने के लिए सहमत हैं या नहीं, और यदि वे सहमत नहीं हैं, तो वे अपनी अस्वीकृति का कारण वर्गीकृत करते हैं। यह केवल एक 1 byte मान है, जिसमें 0x0 का मतलब है कि वे tunnel में भाग लेने के लिए सहमत हैं, और उच्च मान का मतलब है अस्वीकृति के उच्च स्तर।

निम्नलिखित अस्वीकरण कोड परिभाषित हैं:

- TUNNEL_REJECT_PROBABALISTIC_REJECT = 10
- TUNNEL_REJECT_TRANSIENT_OVERLOAD = 20
- TUNNEL_REJECT_BANDWIDTH = 30
- TUNNEL_REJECT_CRIT = 50

अन्य कारणों को छुपाने के लिए, जैसे कि router shutdown, peers से, वर्तमान implementation लगभग सभी rejections के लिए TUNNEL_REJECT_BANDWIDTH का उपयोग करता है।

उत्तर को AES session key के साथ एन्क्रिप्ट किया जाता है जो इसे encrypted block में दिया गया है, और पूरे record size तक पहुंचने के लिए 495 bytes के random data के साथ padded किया जाता है। Padding को status byte से पहले रखा जाता है:

```
AES-256-CBC(SHA-256(padding+status) + padding + status, key, IV)

bytes   0-31 : SHA-256 of bytes 32-527
bytes 32-526 : Random padding
byte 527     : Reply value
```
यह I2NP spec [BRR](/docs/specs/i2np#struct-buildrequestrecord) में भी वर्णित है।

### Tunnel Build Message की तैयारी {#tunnelcreate-requestpreparation}

एक नया Tunnel Build Message बनाते समय, सभी Build Request Records को पहले बनाया जाना चाहिए और ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal) का उपयोग करके asymmetrically encrypted (असममित रूप से एन्क्रिप्ट) किया जाना चाहिए। फिर प्रत्येक record को AES [CRYPTO-AES](/docs/specs/cryptography#AES) का उपयोग करके path में पहले के hops की reply keys और IVs के साथ preemptively decrypt (पूर्वानुमानित रूप से डिक्रिप्ट) किया जाता है। यह decryption reverse order में चलाया जाना चाहिए ताकि asymmetrically encrypted data सही hop पर clear में दिखाई दे जब उनका predecessor इसे encrypt करता है।

व्यक्तिगत अनुरोधों के लिए आवश्यक नहीं होने वाले अतिरिक्त रिकॉर्ड्स को बनाने वाले द्वारा केवल यादृच्छिक डेटा से भरा जाता है।

### Tunnel Build Message Delivery {#tunnelcreate-requestdelivery}

आउटबाउंड tunnel के लिए, डिलीवरी tunnel creator से सीधे पहले hop तक की जाती है, TunnelBuildMessage को इस तरह पैकेज करके जैसे कि creator tunnel में सिर्फ एक और hop हो। इनबाउंड tunnel के लिए, डिलीवरी मौजूदा आउटबाउंड tunnel के माध्यम से की जाती है। आउटबाउंड tunnel आमतौर पर उसी pool से होता है जिसमें नई tunnel बनाई जा रही है। यदि उस pool में कोई आउटबाउंड tunnel उपलब्ध नहीं है, तो एक आउटबाउंड exploratory tunnel का उपयोग किया जाता है। स्टार्टअप के समय, जब कोई आउटबाउंड exploratory tunnel अभी तक मौजूद नहीं है, तो एक नकली 0-hop आउटबाउंड tunnel का उपयोग किया जाता है।

### Tunnel Build Message Endpoint Handling {#tunnelcreate-endpointhandling}

एक outbound tunnel बनाने के लिए, जब अनुरोध एक outbound endpoint तक पहुंचता है ('allow messages to anyone' flag द्वारा निर्धारित), hop को सामान्य रूप से संसाधित किया जाता है, record के स्थान पर एक reply को encrypt करके और अन्य सभी records को encrypt करके, लेकिन चूंकि TunnelBuildMessage को आगे भेजने के लिए कोई 'next hop' नहीं है, इसलिए यह encrypted reply records को TunnelBuildReplyMessage ([TBRM](/docs/specs/i2np#msg-tunnelbuildreply)) या VariableTunnelBuildReplyMessage ([VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply)) में रखता है (message का प्रकार और records की संख्या request के साथ मेल खानी चाहिए) और इसे request record में निर्दिष्ट reply tunnel को deliver करता है। वह reply tunnel किसी भी अन्य message की तरह ही Tunnel Build Reply Message को tunnel creator को वापस forward करता है [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation)। tunnel creator तब इसे संसाधित करता है, जैसा कि नीचे वर्णित है।

Reply tunnel का चयन creator द्वारा निम्नलिखित तरीके से किया गया था: आमतौर पर यह उसी pool का एक inbound tunnel होता है जिसमें नई outbound tunnel बनाई जा रही है। यदि उस pool में कोई inbound tunnel उपलब्ध नहीं है, तो एक inbound exploratory tunnel का उपयोग किया जाता है। Startup के समय, जब अभी तक कोई inbound exploratory tunnel मौजूद नहीं है, तो एक नकली 0-hop inbound tunnel का उपयोग किया जाता है।

एक inbound tunnel के निर्माण के लिए, जब अनुरोध inbound endpoint (जिसे tunnel creator भी कहा जाता है) तक पहुंचता है, तो एक स्पष्ट Tunnel Build Reply Message उत्पन्न करने की आवश्यकता नहीं होती, और router प्रत्येक उत्तर को निम्नलिखित तरीके से संसाधित करता है।

### Tunnel Build Reply Message Processing {#tunnelcreate-replyprocessing}

Reply records को process करने के लिए, creator को बस प्रत्येक record को व्यक्तिगत रूप से AES decrypt करना होता है, peer के बाद tunnel में प्रत्येक hop की reply key और IV का उपयोग करके (reverse order में)। यह फिर reply को expose करता है जो specify करता है कि वे tunnel में भाग लेने के लिए सहमत हैं या वे क्यों मना करते हैं। यदि वे सभी सहमत हैं, तो tunnel को created माना जाता है और तुरंत उपयोग किया जा सकता है, लेकिन यदि कोई भी मना करता है, तो tunnel को discard कर दिया जाता है।

समझौते और अस्वीकृतियों को प्रत्येक peer के profile [PEER-SELECTION](/docs/overview/peer-selection) में दर्ज किया जाता है, जो भविष्य में peer tunnel क्षमता के मूल्यांकन में उपयोग के लिए होता है।

## इतिहास और नोट्स {#tunnelcreate-notes}

यह रणनीति I2P mailing list पर Michael Rogers, Matthew Toseland (toad), और jrandom के बीच predecessor attack के संबंध में हुई चर्चा के दौरान सामने आई। देखें [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html), [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html)। इसे release 0.6.1.10 में 2006-02-16 को पेश किया गया था, जो I2P में अंतिम बार कोई non-backward-compatible बदलाव था।

नोट्स:

- यह डिज़ाइन tunnel के भीतर दो शत्रुतापूर्ण peers को एक या अधिक request या reply records को tag करने से नहीं रोकता ताकि वे यह पता लगा सकें कि वे समान tunnel के भीतर हैं, लेकिन ऐसा करना tunnel creator द्वारा reply पढ़ते समय पता लगाया जा सकता है, जिससे tunnel को अवैध के रूप में चिह्नित किया जा सकता है।

- इस डिज़ाइन में asymmetrically encrypted section पर proof of work शामिल नहीं है, हालांकि 16 byte identity hash को आधे में काटा जा सकता है और बाद वाले को 2^64 तक की cost वाले hashcash function से बदला जा सकता है।

- यह डिज़ाइन अकेले tunnel के भीतर दो शत्रुतापूर्ण peers को timing जानकारी का उपयोग करके यह निर्धारित करने से नहीं रोकता कि वे एक ही tunnel में हैं या नहीं। batched और synchronized request delivery का उपयोग मदद कर सकता है (requests को batch करना और उन्हें (ntp-synchronized) मिनट पर भेजना)। हालांकि, ऐसा करने से peers को requests को delay करके और बाद में tunnel में delay का पता लगाकर उन्हें 'tag' करने की सुविधा मिलती है, हालांकि शायद छोटी window में deliver नहीं होने वाले requests को drop करना काम कर सकता है (हालांकि ऐसा करने के लिए clock synchronization की उच्च डिग्री की आवश्यकता होगी)। वैकल्पिक रूप से, शायद individual hops request को आगे forward करने से पहले random delay inject कर सकते हैं?

- क्या अनुरोध को टैग करने के कोई गैर-घातक तरीके हैं?

- एक घंटे के रिज़ॉल्यूशन के साथ timestamp का उपयोग replay prevention के लिए किया जाता है। यह constraint release 0.9.16 तक लागू नहीं किया गया था।

## भविष्य का कार्य {#future}

- वर्तमान implementation में, originator अपने लिए एक record खाली छोड़ देता है। इस प्रकार n records का एक message केवल n-1 hops का tunnel बना सकता है। यह inbound tunnels के लिए आवश्यक प्रतीत होता है (जहाँ next-to-last hop अगले hop के लिए hash prefix देख सकता है), लेकिन outbound tunnels के लिए नहीं। इस पर अनुसंधान और सत्यापन किया जाना है। यदि anonymity से समझौता किए बिना शेष record का उपयोग करना संभव है, तो हमें ऐसा करना चाहिए।

- उपरोक्त टिप्पणियों में वर्णित संभावित टैगिंग और timing attacks का और विश्लेषण।

- केवल VTBM का उपयोग करें; उन पुराने peers का चयन न करें जो इसका समर्थन नहीं करते।

- Build Request Record tunnel lifetime या expiration निर्दिष्ट नहीं करता; प्रत्येक hop 10 मिनट बाद tunnel को expire कर देता है, जो एक network-wide hardcoded constant है। हम flag field में एक bit का उपयोग कर सकते हैं और padding से 4 (या 8) bytes लेकर lifetime या expiration निर्दिष्ट कर सकते हैं। Requestor केवल तभी इस विकल्प को निर्दिष्ट करेगा जब सभी participants इसे support करते हों।

## संदर्भ {#ref}

- [BRR](/docs/specs/i2np#struct-buildrequestrecord) - Build Request Record
- [CRYPTO-AES](/docs/specs/cryptography#AES) - AES Encryption
- [CRYPTO-ELG](/docs/specs/cryptography#elgamal) - ElGamal Encryption
- [HASHING-IT-OUT](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) - Hashing It Out Paper
- [PEER-SELECTION](/docs/overview/peer-selection) - Peer Selection
- [PREDECESSOR](http://forensics.umass.edu/pubs/wright-tissec.pdf) - Predecessor Attack Paper
- [PREDECESSOR-2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf) - Predecessor Attack Paper (2008)
- [TBM](/docs/specs/i2np#msg-tunnelbuild) - Tunnel Build Message
- [TBRM](/docs/specs/i2np#msg-tunnelbuildreply) - Tunnel Build Reply Message
- [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html) - Tunnel Build Reasoning
- [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html) - Tunnel Build Summary
- [TUNNEL-IMPL](/docs/specs/tunnel-implementation) - Tunnel Implementation
- [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation) - Tunnel Operation
- [VTBM](/docs/specs/i2np#msg-variabletunnelbuild) - Variable Tunnel Build Message
- [VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply) - Variable Tunnel Build Reply Message
