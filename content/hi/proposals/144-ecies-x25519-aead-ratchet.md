---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "बंद"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## नोट

नेटवर्क deployment और testing प्रगति में है। मामूली संशोधनों के अधीन। आधिकारिक specification के लिए [SPEC](/docs/specs/ecies/) देखें।

निम्नलिखित features 0.9.46 तक implement नहीं किए गए हैं:

- MessageNumbers, Options, और Termination blocks
- Protocol-layer responses
- Zero static key
- Multicast

## अवलोकन

यह I2P की शुरुआत से पहले नए end-to-end encryption प्रकार का एक प्रस्ताव है, जो ElGamal/AES+SessionTags [Elg-AES](/docs/legacy/elgamal-aes/) को बदलने के लिए है।

यह निम्नलिखित पूर्व कार्य पर आधारित है:

- Common structures spec [Common Structures](/docs/specs/common-structures/)
- [I2NP](/docs/specs/i2np/) spec जिसमें LS2 शामिल है
- ElGamal/AES+Session Tags [Elg-AES](/docs/legacy/elgamal-aes/)
- [http://zzz.i2p/topics/1768](http://zzz.i2p/topics/1768) नया asymmetric crypto अवलोकन
- निम्न-स्तरीय crypto अवलोकन [CRYPTO-ELG](/docs/specs/cryptography/)
- ECIES [http://zzz.i2p/topics/2418](http://zzz.i2p/topics/2418)
- [NTCP2](/docs/specs/ntcp2/) [Proposal 111](/proposals/111-ntcp-2/)
- 123 New netDB Entries
- 142 New Crypto Template
- [Noise](https://noiseprotocol.org/noise.html) protocol
- [Signal](https://signal.org/docs/) double ratchet algorithm

लक्ष्य end-to-end, destination-to-destination संचार के लिए नई एन्क्रिप्शन का समर्थन करना है।

यह डिज़ाइन एक Noise handshake और data phase का उपयोग करेगा जिसमें Signal का double ratchet शामिल होगा।

इस प्रस्ताव में Signal और Noise के सभी संदर्भ केवल पृष्ठभूमि जानकारी के लिए हैं। इस प्रस्ताव को समझने या लागू करने के लिए Signal और Noise प्रोटोकॉल का ज्ञान आवश्यक नहीं है।

### Current ElGamal Uses

समीक्षा के रूप में, ElGamal 256-byte public keys निम्नलिखित डेटा संरचनाओं में पाई जा सकती हैं। सामान्य संरचना विनिर्देश का संदर्भ लें।

- एक Router Identity में
  यह router की encryption key है।

- एक Destination में
  Destination की public key का उपयोग पुराने i2cp-to-i2cp encryption के लिए किया जाता था
  जो संस्करण 0.6 में निष्क्रिय कर दिया गया था, यह वर्तमान में LeaseSet encryption के लिए
  IV के अलावा अप्रयुक्त है, जो deprecated है।
  इसके बजाय LeaseSet में public key का उपयोग किया जाता है।

- एक LeaseSet में
  यह destination की एन्क्रिप्शन key है।

- LS2 में
  यह destination की encryption key है।

### EncTypes in Key Certs

समीक्षा के रूप में, जब हमने signature types के लिए समर्थन जोड़ा था तब हमने encryption types के लिए समर्थन भी जोड़ा था। encryption type फ़ील्ड हमेशा शून्य होता है, Destinations और RouterIdentities दोनों में। क्या कभी इसे बदलना है यह TBD है। common structures specification [Common Structures](/docs/specs/common-structures/) का संदर्भ लें।

### वर्तमान ElGamal उपयोग

समीक्षा के रूप में, हम ElGamal का उपयोग इसके लिए करते हैं:

1) Tunnel Build संदेश (key RouterIdentity में है)    प्रतिस्थापन इस प्रस्ताव में शामिल नहीं है।    प्रस्ताव 152 [Proposal 152](/proposals/152-ecies-tunnels) देखें।

2) netdb और अन्य I2NP msgs का Router-to-router encryption (Key RouterIdentity में है)    इस proposal पर निर्भर करता है।    1) के लिए भी एक proposal की आवश्यकता है, या RI options में key डालना।

3) Client End-to-end ElGamal+AES/SessionTag (key LeaseSet में है, Destination key का उपयोग नहीं किया जाता)    प्रतिस्थापन इस प्रस्ताव में शामिल है।

4) NTCP1 और SSU के लिए Ephemeral DH    प्रतिस्थापन इस प्रस्ताव में शामिल नहीं है।    NTCP2 के लिए प्रस्ताव 111 देखें।    SSU2 के लिए कोई वर्तमान प्रस्ताव नहीं है।

### Key Certs में EncTypes

- पीछे की ओर संगत
- LS2 (प्रस्ताव 123) की आवश्यकता और उस पर निर्माण
- NTCP2 (प्रस्ताव 111) के लिए जोड़े गए नए crypto या primitives का लाभ उठाना
- समर्थन के लिए कोई नए crypto या primitives की आवश्यकता नहीं
- crypto और signing के decoupling को बनाए रखना; सभी वर्तमान और भविष्य के संस्करणों का समर्थन
- destinations के लिए नए crypto को सक्षम करना
- routers के लिए नए crypto को सक्षम करना, लेकिन केवल garlic messages के लिए - tunnel building
  एक अलग प्रस्ताव होगा
- 32-byte binary destination hashes पर निर्भर किसी भी चीज़ को नुकसान न पहुँचाना, जैसे bittorrent
- ephemeral-static DH का उपयोग करके 0-RTT message delivery बनाए रखना
- इस protocol layer पर messages की buffering / queueing की आवश्यकता नहीं;
  response की प्रतीक्षा के बिना दोनों दिशाओं में असीमित message delivery का समर्थन जारी रखना
- 1 RTT के बाद ephemeral-ephemeral DH में अपग्रेड
- out-of-order messages की handling बनाए रखना
- 256-bit security बनाए रखना
- forward secrecy जोड़ना
- authentication (AEAD) जोड़ना
- ElGamal की तुलना में बहुत अधिक CPU-कुशल
- DH को कुशल बनाने के लिए Java jbigi पर निर्भर न रहना
- DH operations को कम से कम करना
- ElGamal (514 byte ElGamal block) की तुलना में बहुत अधिक bandwidth-कुशल
- यदि वांछित हो तो एक ही tunnel पर नए और पुराने crypto का समर्थन
- प्राप्तकर्ता एक ही tunnel से आने वाले नए और पुराने crypto को कुशलता से अलग कर सकता है
- अन्य लोग नए और पुराने या भविष्य के crypto में अंतर नहीं कर सकते
- नए बनाम मौजूदा Session length classification को समाप्त करना (padding का समर्थन)
- कोई नए I2NP messages की आवश्यकता नहीं
- AES payload में SHA-256 checksum को AEAD से बदलना
- transmit और receive sessions की binding का समर्थन ताकि
  acknowledgements protocol के भीतर हो सकें, न कि केवल out-of-band।
  यह replies को तुरंत forward secrecy प्राप्त करने की अनुमति भी देगा।
- कुछ messages (RouterInfo stores) की end-to-end encryption को सक्षम करना
  जो हम वर्तमान में CPU overhead के कारण नहीं करते।
- I2NP Garlic Message
  या Garlic Message Delivery Instructions format को न बदलना।
- Garlic Clove Set और Clove formats में अप्रयुक्त या अनावश्यक fields को समाप्त करना।

session tags के साथ कई समस्याओं को समाप्त करें, जिनमें शामिल हैं:

- पहले उत्तर तक AES का उपयोग न कर पाना
- यदि टैग डिलीवरी को मान लिया जाए तो अविश्वसनीयता और रुकावटें
- बैंडविड्थ अक्षम, विशेष रूप से पहली डिलीवरी पर
- टैग स्टोर करने के लिए भारी स्थान अक्षमता
- टैग डिलीवर करने के लिए भारी बैंडविड्थ ओवरहेड
- अत्यधिक जटिल, कार्यान्वयन करना कठिन
- विभिन्न उपयोग मामलों के लिए ट्यूनिंग करना कठिन
  (streaming बनाम datagrams, server बनाम client, उच्च बनाम कम बैंडविड्थ)
- टैग डिलीवरी के कारण मेमोरी समाप्ति की कमजोरियां

### असममित क्रिप्टो उपयोग

- LS2 format परिवर्तन (proposal 123 पूरा हो गया है)
- नया DHT rotation algorithm या shared random generation
- Tunnel building के लिए नई encryption।
  देखें proposal 152 [Proposal 152](/proposals/152-ecies-tunnels)।
- Tunnel layer encryption के लिए नई encryption।
  देखें proposal 153 [Proposal 153](/proposals/153-chacha20-layer-encryption)।
- I2NP DLM / DSM / DSRM messages की encryption, transmission, और reception की विधियाँ।
  कोई बदलाव नहीं।
- कोई LS1-to-LS2 या ElGamal/AES-to-this-proposal संचार समर्थित नहीं है।
  यह proposal एक bidirectional protocol है।
  Destinations समान tunnels का उपयोग करके दो leasesets प्रकाशित करके backward compatibility को संभाल सकते हैं,
  या LS2 में दोनों encryption types डाल सकते हैं।
- Threat model परिवर्तन
- Implementation विवरण यहाँ चर्चित नहीं हैं और प्रत्येक project पर छोड़े गए हैं।
- (आशावादी) Multicast को समर्थन देने के लिए extensions या hooks जोड़ना

### लक्ष्य

ElGamal/AES+SessionTag लगभग 15 वर्षों से हमारा एकमात्र end-to-end प्रोटोकॉल रहा है, मूल रूप से प्रोटोकॉल में बिना किसी संशोधन के। अब ऐसे cryptographic primitives हैं जो तेज़ हैं। हमें प्रोटोकॉल की सुरक्षा को बढ़ाने की आवश्यकता है। हमने प्रोटोकॉल के memory और bandwidth overhead को कम करने के लिए heuristic रणनीतियां और workarounds भी विकसित किए हैं, लेकिन वे रणनीतियां नाज़ुक हैं, tune करना कठिन है, और प्रोटोकॉल को और भी अधिक टूटने का खतरा बनाती हैं, जिससे session drop हो जाता है।

लगभग इसी समयावधि के लिए, ElGamal/AES+SessionTag विनिर्देश और संबंधित दस्तावेज़ीकरण ने वर्णन किया है कि session tags प्रदान करना कितना bandwidth-महंगा है, और session tag delivery को एक "synchronized PRNG" से बदलने का प्रस्ताव किया है। एक synchronized PRNG निर्धारणवादी रूप से दोनों छोरों पर एक सामान्य seed से व्युत्पन्न समान tags उत्पन्न करता है। एक synchronized PRNG को "ratchet" भी कहा जा सकता है। यह प्रस्ताव (अंततः) उस ratchet तंत्र को निर्दिष्ट करता है, और tag delivery को समाप्त करता है।

ratchet (एक synchronized PRNG) का उपयोग करके session tags उत्पन्न करने से, हम New Session message और बाद के messages में आवश्यकता पड़ने पर session tags भेजने की overhead को समाप्त कर देते हैं। 32 tags के एक विशिष्ट tag set के लिए, यह 1KB होता है। इससे भेजने वाले पक्ष पर session tags का storage भी समाप्त हो जाता है, जिससे storage आवश्यकताएं आधी हो जाती हैं।

एक पूर्ण two-way handshake, Noise IK pattern के समान, Key Compromise Impersonation (KCI) attacks से बचने के लिए आवश्यक है। [NOISE](https://noiseprotocol.org/noise.html) में Noise "Payload Security Properties" table देखें। KCI पर अधिक जानकारी के लिए, यह paper देखें https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf

### गैर-लक्ष्य / दायरे से बाहर

खतरा मॉडल NTCP2 (प्रस्ताव 111) की तुलना में कुछ अलग है। MitM नोड्स OBEP और IBGW हैं और माना जाता है कि उनके पास वर्तमान या ऐतिहासिक global NetDB का पूरा दृश्य है, floodfills के साथ मिलीभगत करके।

लक्ष्य इन MitMs को ट्रैफ़िक को नए और मौजूदा सेशन संदेशों के रूप में, या नए crypto बनाम पुराने crypto के रूप में वर्गीकृत करने से रोकना है।

## Detailed Proposal

यह प्रस्ताव ElGamal/AES+SessionTags को बदलने के लिए एक नया end-to-end प्रोटोकॉल परिभाषित करता है। डिजाइन में Signal के double ratchet को शामिल करते हुए Noise handshake और data phase का उपयोग होगा।

### औचित्य

प्रोटोकॉल के पांच भाग हैं जिन्हें फिर से डिज़ाइन किया जाना है:

- 1) नए और मौजूदा Session container formats को नए formats के साथ बदल दिया जाता है।
- 2) ElGamal (256 byte public keys, 128 byte private keys) को ECIES-X25519 (32 byte public और private keys) के साथ बदल दिया जाता है।
- 3) AES को AEAD_ChaCha20_Poly1305 (नीचे ChaChaPoly के रूप में संक्षिप्त) के साथ बदल दिया जाता है।
- 4) SessionTags को ratchets के साथ बदल दिया जाएगा, जो मूल रूप से एक cryptographic, synchronized PRNG है।
- 5) AES payload, जैसा कि ElGamal/AES+SessionTags specification में परिभाषित है, को NTCP2 के समान block format के साथ बदल दिया जाता है।

पांच परिवर्तनों में से प्रत्येक का अपना अनुभाग नीचे दिया गया है।

### खतरा मॉडल

मौजूदा I2P router implementations में निम्नलिखित मानक क्रिप्टोग्राफिक primitives के लिए implementations की आवश्यकता होगी, जो वर्तमान I2P protocols के लिए आवश्यक नहीं हैं:

- ECIES (लेकिन यह मूल रूप से X25519 है)
- Elligator2

मौजूदा I2P router कार्यान्वयन जिन्होंने अभी तक [NTCP2](/docs/specs/ntcp2/) ([Proposal 111](/proposals/111-ntcp-2/)) को लागू नहीं किया है, उन्हें इसके लिए भी कार्यान्वयन की आवश्यकता होगी:

- X25519 key generation और DH
- AEAD_ChaCha20_Poly1305 (नीचे ChaChaPoly के रूप में संक्षिप्त)
- HKDF

### Crypto Type

crypto type (LS2 में उपयोग किया गया) 4 है। यह एक little-endian 32-byte X25519 public key को दर्शाता है, और यहाँ निर्दिष्ट end-to-end protocol को।

Crypto type 0 ElGamal है। Crypto types 1-3 ECIES-ECDH-AES-SessionTag के लिए आरक्षित हैं, proposal 145 [Proposal 145](/proposals/145-ecies) देखें।

### क्रिप्टोग्राफिक डिज़ाइन का सारांश

यह प्रस्ताव Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11) पर आधारित आवश्यकताएं प्रदान करता है। Noise में Station-To-Station protocol [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) के समान गुण हैं, जो [SSU](/docs/legacy/ssu/) protocol का आधार है। Noise की भाषा में, Alice initiator है, और Bob responder है।

यह प्रस्ताव Noise protocol Noise_IK_25519_ChaChaPoly_SHA256 पर आधारित है। (प्रारंभिक key derivation function के लिए वास्तविक identifier "Noise_IKelg2_25519_ChaChaPoly_SHA256" है जो I2P extensions को दर्शाता है - नीचे KDF 1 section देखें) यह Noise protocol निम्नलिखित primitives का उपयोग करता है:

- Interactive Handshake Pattern: IK
  Alice तुरंत Bob को अपनी static key भेजती है (I)
  Alice को Bob की static key पहले से पता है (K)

- One-Way Handshake Pattern: N
  Alice अपनी static key को Bob को transmit नहीं करती है (N)

- DH Function: X25519
  X25519 DH जिसमें 32 बाइट्स की key length है जैसा कि [RFC-7748](https://tools.ietf.org/html/rfc7748) में निर्दिष्ट है।

- Cipher Function: ChaChaPoly
  AEAD_CHACHA20_POLY1305 जैसा कि [RFC-7539](https://tools.ietf.org/html/rfc7539) section 2.8 में निर्दिष्ट है।
  12 byte nonce, जिसके पहले 4 bytes शून्य पर सेट हैं।
  [NTCP2](/docs/specs/ntcp2/) के समान।

- Hash Function: SHA256
  मानक 32-बाइट hash, पहले से ही I2P में व्यापक रूप से उपयोग किया जाता है।

### I2P के लिए नए क्रिप्टोग्राफिक प्रिमिटिव्स

यह प्रस्ताव Noise_IK_25519_ChaChaPoly_SHA256 में निम्नलिखित सुधारों को परिभाषित करता है। ये आमतौर पर [NOISE](https://noiseprotocol.org/noise.html) section 13 में दिशानिर्देशों का पालन करते हैं।

1) Cleartext ephemeral keys को [Elligator2](https://elligator.cr.yp.to/) के साथ encode किया जाता है।

2) उत्तर cleartext tag के साथ prefixed होता है।

3) पेलोड प्रारूप संदेश 1, 2, और डेटा चरण के लिए परिभाषित किया गया है। निश्चित रूप से, यह Noise में परिभाषित नहीं है।

सभी संदेशों में एक [I2NP](/docs/specs/i2np/) Garlic Message header शामिल होता है। डेटा फेज़ Noise डेटा फेज़ के समान, लेकिन उसके साथ compatible नहीं, encryption का उपयोग करता है।

### क्रिप्टो प्रकार

Handshakes [Noise](https://noiseprotocol.org/noise.html) handshake patterns का उपयोग करते हैं।

निम्नलिखित अक्षर मैपिंग का उपयोग किया गया है:

- e = एक-बार का ephemeral key
- s = static key
- p = संदेश payload

एक-बार और Unbound सेशन Noise N pattern के समान हैं।

```

<- s
  ...
  e es p ->

```
Bound sessions Noise IK pattern के समान होते हैं।

```

<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->

```
### Noise Protocol Framework

वर्तमान ElGamal/AES+SessionTag प्रोटोकॉल एकदिशीय है। इस स्तर पर, प्राप्तकर्ता को पता नहीं होता कि संदेश कहाँ से आया है। आउटबाउंड और इनबाउंड सत्र संबद्ध नहीं हैं। पावती clove में DeliveryStatusMessage (GarlicMessage में wrapped) का उपयोग करके आउट-ऑफ-बैंड होती है।

एक unidirectional protocol में पर्याप्त अकुशलता होती है। किसी भी उत्तर को भी महंगे 'New Session' संदेश का उपयोग करना पड़ता है। इससे अधिक bandwidth, CPU, और memory का उपयोग होता है।

एकदिशीय protocol में भी security कमजोरियां हैं। सभी sessions ephemeral-static DH पर आधारित हैं। return path के बिना, Bob के लिए अपनी static key को ephemeral key में "ratchet" करने का कोई तरीका नहीं है। यह जाने बिना कि message कहाँ से आया है, outbound messages के लिए प्राप्त ephemeral key का उपयोग करने का कोई तरीका नहीं है, इसलिए प्रारंभिक reply भी ephemeral-static DH का उपयोग करती है।

इस प्रस्ताव के लिए, हम द्विदिशीय प्रोटोकॉल बनाने के लिए दो तंत्र परिभाषित करते हैं - "pairing" और "binding"। ये तंत्र बढ़ी हुई दक्षता और सुरक्षा प्रदान करते हैं।

### फ्रेमवर्क में जोड़े गए हिस्से

ElGamal/AES+SessionTags की तरह, सभी inbound और outbound sessions एक दिए गए context में होने चाहिए, या तो router के context में या किसी विशेष local destination के context में। Java I2P में, इस context को Session Key Manager कहा जाता है।

Sessions को contexts के बीच साझा नहीं किया जाना चाहिए, क्योंकि इससे विभिन्न local destinations के बीच, या local destination और router के बीच correlation की अनुमति मिल जाएगी।

जब कोई दिया गया destination ElGamal/AES+SessionTags और इस प्रस्ताव दोनों का समर्थन करता है, तो दोनों प्रकार के sessions एक context साझा कर सकते हैं। नीचे धारा 1c) देखें।

### Handshake Patterns

जब originator (Alice) पर एक outbound session बनाया जाता है, तो एक नया inbound session बनाया जाता है और outbound session के साथ जोड़ा जाता है, जब तक कि कोई reply की अपेक्षा न हो (जैसे raw datagrams)।

एक नया inbound session हमेशा एक नए outbound session के साथ जोड़ा जाता है, जब तक कि कोई reply का अनुरोध नहीं किया गया हो (जैसे raw datagrams)।

यदि एक उत्तर का अनुरोध किया जाता है और वह दूर-छोर गंतव्य या router से बंधा होता है, तो वह नया आउटबाउंड सत्र उस गंतव्य या router से बंधा होता है, और उस गंतव्य या router के किसी भी पिछले आउटबाउंड सत्र को प्रतिस्थापित कर देता है।

इनबाउंड और आउटबाउंड sessions को जोड़ना एक द्विदिशीय प्रोटोकॉल प्रदान करता है जिसमें DH keys को ratchet करने की क्षमता होती है।

### सत्र

किसी दिए गए destination या router के लिए केवल एक outbound session होता है। किसी दिए गए destination या router से कई current inbound sessions हो सकते हैं। आम तौर पर, जब एक नया inbound session बनाया जाता है, और उस session पर traffic प्राप्त होता है (जो एक ACK का काम करता है), तो अन्य सभी को अपेक्षाकृत जल्दी expire होने के लिए mark कर दिया जाएगा, लगभग एक मिनट या उसके आसपास में। पिछले भेजे गए messages (PN) value की जांच की जाती है, और यदि पिछले inbound session में कोई unreceived messages नहीं हैं (window size के भीतर), तो पिछला session तुरंत delete हो सकता है।

जब originator (Alice) पर एक outbound session बनाया जाता है, तो यह far-end Destination (Bob) से bound होता है, और कोई भी paired inbound session भी far-end Destination से bound होगा। जैसे-जैसे sessions ratchet करते हैं, वे far-end Destination से bound रहते हैं।

जब receiver (Bob) पर एक inbound session बनाया जाता है, तो यह Alice के विकल्प पर far-end Destination (Alice) से bind हो सकता है। यदि Alice New Session message में binding information (उसकी static key) शामिल करती है, तो session उस destination से bind हो जाएगा, और एक outbound session बनाया जाएगा और समान Destination से bind होगा। जैसे-जैसे sessions ratchet होते हैं, वे far-end Destination से bind रहते हैं।

### सेशन संदर्भ

सामान्य, streaming मामले के लिए, हम उम्मीद करते हैं कि Alice और Bob प्रोटोकॉल का उपयोग निम्नलिखित तरीके से करेंगे:

- Alice अपने नए outbound session को एक नए inbound session के साथ जोड़ती है, दोनों far-end destination (Bob) से bound होते हैं।
- Alice binding information और signature, और एक reply request को Bob को भेजे गए New Session message में शामिल करती है।
- Bob अपने नए inbound session को एक नए outbound session के साथ जोड़ता है, दोनों far-end destination (Alice) से bound होते हैं।
- Bob paired session में Alice को एक reply (ack) भेजता है, नई DH key के लिए ratchet के साथ।
- Alice Bob की नई key के साथ नए outbound session के लिए ratchet करती है, जो मौजूदा inbound session से paired होता है।

दूर-छोर के Destination के साथ एक inbound session को bind करके, और उसी Destination से bound एक outbound session के साथ inbound session को pair करके, हमें दो प्रमुख लाभ प्राप्त होते हैं:

1) Bob से Alice को प्रारंभिक उत्तर ephemeral-ephemeral DH का उपयोग करता है

2) Alice द्वारा Bob का reply प्राप्त करने और ratchet करने के बाद, Alice से Bob को भेजे जाने वाले सभी बाद के messages ephemeral-ephemeral DH का उपयोग करते हैं।

### Inbound और Outbound Sessions को जोड़ना

ElGamal/AES+SessionTags में, जब एक LeaseSet को garlic clove के रूप में बंडल किया जाता है, या tags वितरित किए जाते हैं, तो भेजने वाला router एक ACK का अनुरोध करता है। यह एक अलग garlic clove है जिसमें DeliveryStatus Message होता है। अतिरिक्त सुरक्षा के लिए, DeliveryStatus Message को Garlic Message में लपेटा जाता है। यह तंत्र प्रोटोकॉल के दृष्टिकोण से out-of-band है।

नए protocol में, चूंकि inbound और outbound sessions paired हैं, हमारे पास ACKs in-band हो सकते हैं। अलग clove की आवश्यकता नहीं है।

एक स्पष्ट ACK केवल एक Existing Session संदेश है जिसमें कोई I2NP block नहीं है। हालांकि, अधिकांश मामलों में, एक स्पष्ट ACK से बचा जा सकता है, क्योंकि reverse traffic होता है। implementations के लिए यह वांछनीय हो सकता है कि वे स्पष्ट ACK भेजने से पहले थोड़ा समय (शायद सौ ms) प्रतीक्षा करें, ताकि streaming या application layer को जवाब देने का समय मिल सके।

Implementation को I2NP ब्लॉक प्रोसेस होने तक किसी भी ACK भेजने को स्थगित करना होगा, क्योंकि Garlic Message में lease set के साथ एक Database Store Message हो सकता है। ACK को route करने के लिए एक हालिया lease set आवश्यक होगा, और binding static key को सत्यापित करने के लिए far-end destination (lease set में निहित) आवश्यक होगा।

### Binding Sessions और Destinations

Outbound sessions हमेशा inbound sessions से पहले समाप्त होने चाहिए। जब एक outbound session समाप्त हो जाता है, और एक नया बनाया जाता है, तो एक नया युग्मित inbound session भी बनाया जाएगा। यदि कोई पुराना inbound session था, तो उसे समाप्त होने दिया जाएगा।

### बाइंडिंग और पेयरिंग के फायदे

निर्धारित किया जाना है

### Message ACKs

हम निम्नलिखित functions को परिभाषित करते हैं जो उपयोग किए जाने वाले cryptographic building blocks के अनुरूप हैं।

ZEROLEN

    zero-length byte array

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).
    || below means append.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

MixHash(d)

    SHA-256 hash function that takes a previous hash h and new data d,
    and produces an output of length 32 bytes.
    || below means append.

    Use SHA-256 as follows::

        MixHash(d) := h = SHA-256(h || d)

STREAM

    The ChaCha20/Poly1305 AEAD as specified in [RFC-7539](https://tools.ietf.org/html/rfc7539).
    S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Encrypts plaintext using the cipher key k, and nonce n which MUST be unique for
        the key k.
        Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16 bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, n, ciphertext, ad)
        Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional.
        Returns the plaintext.

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()
        Generates a new private key that maps to a public key suitable for Elligator2 encoding.
        Note that half of the randomly-generated private keys will not be suitable and must be discarded.

    ENCODE_ELG2(pubkey)
        Returns the Elligator2-encoded public key corresponding to the given public key (inverse mapping).
        Encoded keys are little endian.
        Encoded key must be 256 bits indistinguishable from random data.
        See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)
        Returns the public key corresponding to the given Elligator2-encoded public key.
        See Elligator2 section below for specification.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.

MixKey(d)

    Use HKDF() with a previous chainKey and new data d, and
    sets the new chainKey and k.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]


### सेशन टाइमआउट्स

### मल्टिकास्ट

[I2NP](/docs/specs/i2np/) में निर्दिष्ट Garlic Message निम्नलिखित है। चूंकि एक डिज़ाइन लक्ष्य यह है कि intermediate hops नई crypto को पुराने से अलग नहीं कर सकते, यह format नहीं बदल सकता, भले ही length field redundant हो। format को पूरे 16-byte header के साथ दिखाया गया है, हालांकि वास्तविक header अलग format में हो सकता है, जो उपयोग किए गए transport पर निर्भर करता है।

जब डिक्रिप्ट किया जाता है तो डेटा में Garlic Cloves की एक श्रृंखला और अतिरिक्त डेटा होता है, जिसे Clove Set भी कहा जाता है।

विवरण और पूर्ण विनिर्देश के लिए [I2NP](/docs/specs/i2np/) देखें।

```

+----+----+----+----+----+----+----+----+
  |type|      msg_id       |  expiration
  +----+----+----+----+----+----+----+----+
                           |  size   |chks|
  +----+----+----+----+----+----+----+----+
  |      length       |                   |
  +----+----+----+----+                   +
  |          encrypted data               |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

```
### परिभाषाएं

वर्तमान संदेश प्रारूप, जो 15 वर्षों से अधिक समय से उपयोग में है, ElGamal/AES+SessionTags है। ElGamal/AES+SessionTags में, दो संदेश प्रारूप हैं:

1) नया session: - 514 byte ElGamal block - AES block (128 bytes न्यूनतम, 16 का गुणांक)

2) मौजूदा session: - 32 byte Session Tag - AES block (128 bytes न्यूनतम, 16 का गुणज)

128 तक का न्यूनतम padding Java I2P में implemented के रूप में है लेकिन reception पर इसे enforce नहीं किया जाता है।

ये संदेश एक I2NP garlic message में encapsulated होते हैं, जिसमें एक length field होता है, इसलिए length ज्ञात होती है।

ध्यान दें कि non-mod-16 length के लिए कोई padding परिभाषित नहीं है, इसलिए New Session हमेशा (mod 16 == 2) होता है, और एक Existing Session हमेशा (mod 16 == 0) होता है। हमें इसे ठीक करने की आवश्यकता है।

receiver पहले पहले 32 bytes को Session Tag के रूप में lookup करने का प्रयास करता है। यदि मिल जाता है, तो वह AES block को decrypt करता है। यदि नहीं मिलता, और data कम से कम (514+16) लंबा है, तो वह ElGamal block को decrypt करने का प्रयास करता है, और यदि सफल होता है, तो AES block को decrypt करता है।

### 1) संदेश प्रारूप

Signal Double Ratchet में, header में निम्नलिखित होता है:

- DH: वर्तमान ratchet सार्वजनिक कुंजी
- PN: पिछली श्रृंखला संदेश लंबाई
- N: संदेश संख्या

Signal की "sending chains" लगभग हमारे tag sets के समकक्ष हैं। एक session tag का उपयोग करके, हम इसका अधिकांश भाग समाप्त कर सकते हैं।

New Session में, हम केवल public key को unencrytped header में डालते हैं।

मौजूदा Session में, हम header के लिए एक session tag का उपयोग करते हैं। Session tag वर्तमान ratchet public key और message number के साथ जुड़ा होता है।

नए और मौजूदा दोनों Session में, PN और N encrypted body में होते हैं।

Signal में, चीजें लगातार ratcheting होती रहती हैं। एक नया DH public key प्राप्तकर्ता को ratchet करने और वापस एक नया public key भेजने की आवश्यकता होती है, जो प्राप्त public key के लिए ack का भी काम करता है। यह हमारे लिए बहुत अधिक DH operations होगा। इसलिए हम प्राप्त key की ack और नए public key के transmission को अलग करते हैं। नए DH public key से generated session tag का उपयोग करने वाला कोई भी message एक ACK का काम करता है। हम केवल तभी नया public key transmit करते हैं जब हम rekey करना चाहते हैं।

DH को ratchet करने से पहले संदेशों की अधिकतम संख्या 65535 है।

जब session key deliver करते हैं, तो हम इससे "Tag Set" derive करते हैं, बजाय session tags को अलग से deliver करने के। एक Tag Set में 65536 tags तक हो सकते हैं। हालांकि, receivers को "look-ahead" strategy implement करनी चाहिए, बजाय सभी संभावित tags को एक साथ generate करने के। केवल अंतिम अच्छे tag received के बाद अधिकतम N tags generate करें। N अधिकतम 128 हो सकता है, लेकिन 32 या इससे भी कम बेहतर विकल्प हो सकता है।

### वर्तमान मैसेज फॉर्मेट की समीक्षा

नया सेशन वन टाइम पब्लिक key (32 bytes) एन्क्रिप्टेड डेटा और MAC (शेष bytes)

New Session संदेश में भेजने वाले की static public key हो भी सकती है या नहीं भी। यदि यह शामिल है, तो reverse session उस key के साथ bound है। Static key को शामिल किया जाना चाहिए यदि replies की अपेक्षा है, यानी streaming और repliable datagrams के लिए। इसे raw datagrams के लिए शामिल नहीं किया जाना चाहिए।

New Session message एक-तरफा Noise [NOISE](https://noiseprotocol.org/noise.html) pattern "N" (यदि static key नहीं भेजी गई है), या दो-तरफा pattern "IK" (यदि static key भेजी गई है) के समान है।

### एन्क्रिप्टेड डेटा फॉर्मेट की समीक्षा

लंबाई 96 + payload लंबाई है। एन्क्रिप्टेड प्रारूप:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +         Static Key                    +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for Static Key Section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Static Key encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### नए Session Tags और Signal से तुलना

ephemeral key 32 bytes का होता है, जो Elligator2 के साथ encoded होता है। यह key कभी भी दोबारा उपयोग नहीं होती; हर संदेश के साथ एक नई key generate की जाती है, जिसमें retransmissions भी शामिल हैं।

### 1a) नया session प्रारूप

जब decrypt किया जाता है, Alice की X25519 static key, 32 bytes।

### 1b) नया session format (binding के साथ)

एन्क्रिप्टेड लेंथ डेटा का शेष हिस्सा है। डिक्रिप्टेड लेंथ एन्क्रिप्टेड लेंथ से 16 कम है। Payload में एक DateTime ब्लॉक होना आवश्यक है और आमतौर पर एक या अधिक Garlic Clove ब्लॉक्स होंगे। फॉर्मेट और अतिरिक्त आवश्यकताओं के लिए नीचे payload सेक्शन देखें।

### नया सत्र एफेमेरल की

यदि कोई उत्तर आवश्यक नहीं है, तो कोई static key नहीं भेजी जाती।

लंबाई 96 + payload length है। एन्क्रिप्टेड प्रारूप:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flags Section               +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for above section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Flags Section encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### स्थिर कुंजी

Alice की ephemeral key। Ephemeral key 32 bytes की है, जो Elligator2 के साथ encoded है, little endian में। यह key कभी दोबारा उपयोग नहीं की जाती; हर message के साथ एक नई key generate की जाती है, जिसमें retransmissions भी शामिल हैं।

### पेलोड

Flags सेक्शन में कुछ भी नहीं होता है। यह हमेशा 32 bytes का होता है, क्योंकि binding के साथ New Session messages के लिए static key के समान लंबाई होनी चाहिए। Bob यह निर्धारित करता है कि यह static key है या flags सेक्शन है, यह टेस्ट करके कि क्या 32 bytes सभी zeros हैं।

TODO यहाँ कोई flags की आवश्यकता है?

### 1c) नया session प्रारूप (binding के बिना)

एन्क्रिप्टेड लेंथ डेटा का बचा हुआ भाग है। डिक्रिप्टेड लेंथ एन्क्रिप्टेड लेंथ से 16 कम होती है। पेलोड में एक DateTime ब्लॉक होना आवश्यक है और आमतौर पर एक या अधिक Garlic Clove ब्लॉक्स होंगे। फॉर्मेट और अतिरिक्त आवश्यकताओं के लिए नीचे पेलोड सेक्शन देखें।

### नया सत्र अस्थायी कुंजी

यदि केवल एक single message भेजे जाने की अपेक्षा है, तो कोई session setup या static key की आवश्यकता नहीं है।

लंबाई 96 + payload लंबाई है। Encrypted प्रारूप:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       Ephemeral Public Key            |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flags Section               +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for above section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Flags Section encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### फ्लैग्स सेक्शन डिक्रिप्टेड डेटा

एक बार का key 32 bytes का होता है, जो Elligator2 के साथ encode किया जाता है, little endian में। यह key कभी भी दोबारा उपयोग नहीं किया जाता; प्रत्येक message के साथ एक नया key generate किया जाता है, retransmissions सहित।

### पेलोड

Flags सेक्शन में कुछ भी नहीं होता। यह हमेशा 32 bytes का होता है, क्योंकि इसका binding के साथ New Session messages के लिए static key के समान length होना आवश्यक है। Bob यह निर्धारित करता है कि यह static key है या flags section है, यह जांचकर कि क्या सभी 32 bytes शून्य हैं।

TODO यहाँ कोई flags की आवश्यकता है?

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                                       |
  +             All zeros                 +
  |              32 bytes                 |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  zeros:: All zeros, 32 bytes.

```
### 1d) एक-बारीय प्रारूप (कोई binding या session नहीं)

Encrypted length डेटा का शेष भाग है। Decrypted length, encrypted length से 16 कम है। Payload में एक DateTime block होना आवश्यक है और आमतौर पर एक या अधिक Garlic Clove blocks होते हैं। प्रारूप और अतिरिक्त आवश्यकताओं के लिए नीचे payload अनुभाग देखें।

### नया सेशन वन टाइम Key

### फ्लैग्स सेक्शन डिक्रिप्टेड डेटा

यह IK के लिए एक संशोधित protocol नाम के साथ मानक [NOISE](https://noiseprotocol.org/noise.html) है। ध्यान दें कि हम IK pattern (bound sessions) और N pattern (unbound sessions) दोनों के लिए समान initializer का उपयोग करते हैं।

प्रोटोकॉल नाम दो कारणों से संशोधित किया गया है। पहला, यह दर्शाने के लिए कि ephemeral keys Elligator2 के साथ encoded हैं, और दूसरा, यह दर्शाने के लिए कि tag value को mix करने के लिए दूसरे message से पहले MixHash() को call किया जाता है।

```

This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  h = SHA256(protocol_name);

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by Alice for all outgoing connections

```
### पेलोड

```

This is the "e" message pattern:

  // Bob's X25519 static keys
  // bpk is published in leaseset
  bsk = GENERATE_PRIVATE()
  bpk = DERIVE_PUBLIC(bsk)

  // Bob static public key
  // MixHash(bpk)
  // || below means append
  h = SHA256(h || bpk);

  // up until here, can all be precalculated by Bob for all incoming connections

  // Alice's X25519 ephemeral keys
  aesk = GENERATE_PRIVATE_ELG2()
  aepk = DERIVE_PUBLIC(aesk)

  // Alice ephemeral public key
  // MixHash(aepk)
  // || below means append
  h = SHA256(h || aepk);

  // h is used as the associated data for the AEAD in the New Session Message
  // Retain the Hash h for the New Session Reply KDF
  // eapk is sent in cleartext in the
  // beginning of the New Session message
  elg2_aepk = ENCODE_ELG2(aepk)
  // As decoded by Bob
  aepk = DECODE_ELG2(elg2_aepk)

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, flags/static key section, ad)

  End of "es" message pattern.

  This is the "s" message pattern:

  // MixHash(ciphertext)
  // Save for Payload section KDF
  h = SHA256(h || ciphertext)

  // Alice's X25519 static keys
  ask = GENERATE_PRIVATE()
  apk = DERIVE_PUBLIC(ask)

  End of "s" message pattern.


```
### 1f) नए Session Message के लिए KDFs

```

This is the "ss" message pattern:

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  // chainKey from Static Key Section
  Set sharedSecret = X25519 DH result
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)

  End of "ss" message pattern.

  // MixHash(ciphertext)
  // Save for New Session Reply KDF
  h = SHA256(h || ciphertext)

```
### प्रारंभिक ChainKey के लिए KDF

ध्यान दें कि यह एक Noise "N" pattern है, लेकिन हम bound sessions के लिए उसी "IK" initializer का उपयोग करते हैं।

New Session messages को तब तक Alice की static key युक्त या न युक्त के रूप में पहचाना नहीं जा सकता जब तक static key को decrypt और inspect नहीं किया जाता यह निर्धारित करने के लिए कि इसमें सभी zeros हैं या नहीं। इसलिए, receiver को सभी New Session messages के लिए "IK" state machine का उपयोग करना चाहिए। यदि static key में सभी zeros हैं, तो "ss" message pattern को skip करना चाहिए।

```

chainKey = from Flags/Static key section
  k = from Flags/Static key section
  n = 1
  ad = h from Flags/Static key section
  ciphertext = ENCRYPT(k, n, payload, ad)

```
### Flags/Static Key Section Encrypted Contents के लिए KDF

एक या अधिक New Session Replies एकल New Session संदेश के जवाब में भेजे जा सकते हैं। प्रत्येक उत्तर के पहले एक tag लगाया जाता है, जो session के लिए TagSet से generated होता है।

New Session Reply दो भागों में है। पहला भाग एक prepended tag के साथ Noise IK handshake की पूर्णता है। पहले भाग की लंबाई 56 bytes है। दूसरा भाग data phase payload है। दूसरे भाग की लंबाई 16 + payload length है।

कुल लंबाई 72 + payload लंबाई है। Encrypted format:

```

+----+----+----+----+----+----+----+----+
  |       Session Tag   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Ephemeral Public Key           +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for Key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Tag :: 8 bytes, cleartext

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  MAC :: Poly1305 message authentication code, 16 bytes
         Note: The ChaCha20 plaintext data is empty (ZEROLEN)

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### KDF for Payload Section (Alice static key के साथ)

Tag Session Tags KDF में generate किया जाता है, जैसा कि नीचे DH Initialization KDF में initialize किया गया है। यह reply को session के साथ correlate करता है। DH Initialization से Session Key का उपयोग नहीं किया जाता।

### KDF पेलोड सेक्शन के लिए (Alice static key के बिना)

Bob की ephemeral key। Ephemeral key 32 bytes की है, जो Elligator2 के साथ encoded है, little endian में। यह key कभी भी दोबारा उपयोग नहीं की जाती; हर message के साथ एक नई key generate की जाती है, जिसमें retransmissions भी शामिल हैं।

### 1g) नया Session Reply प्रारूप

एन्क्रिप्टेड लेंथ डेटा का शेष भाग है। डिक्रिप्टेड लेंथ एन्क्रिप्टेड लेंथ से 16 कम है। Payload में आमतौर पर एक या अधिक Garlic Clove blocks होते हैं। फॉर्मेट और अतिरिक्त आवश्यकताओं के लिए नीचे payload सेक्शन देखें।

### Session Tag

TagSet से एक या अधिक tags बनाए जाते हैं, जो नीचे दिए गए KDF का उपयोग करके initialize किया जाता है, New Session message से chainKey का उपयोग करते हुए।

```

// Generate tagset
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
### नया सत्र उत्तर अस्थायी कुंजी

```

// Keys from the New Session message
  // Alice's X25519 keys
  // apk and aepk are sent in original New Session message
  // ask = Alice private static key
  // apk = Alice public static key
  // aesk = Alice ephemeral private key
  // aepk = Alice ephemeral public key
  // Bob's X25519 static keys
  // bsk = Bob private static key
  // bpk = Bob public static key

  // Generate the tag
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  tag = tagsetEntry.SESSION_TAG

  // MixHash(tag)
  h = SHA256(h || tag)

  This is the "e" message pattern:

  // Bob's X25519 ephemeral keys
  besk = GENERATE_PRIVATE_ELG2()
  bepk = DERIVE_PUBLIC(besk)

  // Bob's ephemeral public key
  // MixHash(bepk)
  // || below means append
  h = SHA256(h || bepk);

  // elg2_bepk is sent in cleartext in the
  // beginning of the New Session message
  elg2_bepk = ENCODE_ELG2(bepk)
  // As decoded by Bob
  bepk = DECODE_ELG2(elg2_bepk)

  End of "e" message pattern.

  This is the "ee" message pattern:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  // chainKey from original New Session Payload Section
  sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "", 32)
  chainKey = keydata[0:31]

  End of "ee" message pattern.

  This is the "se" message pattern:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  sharedSecret = DH(ask, bepk) = DH(besk, apk)
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

  End of "se" message pattern.

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  chainKey is used in the ratchet below.

```
### पेलोड

यह पहले Existing Session मैसेज की तरह है, post-split के बाद, लेकिन अलग tag के बिना। इसके अतिरिक्त, हम payload को NSR मैसेज से bind करने के लिए ऊपर से hash का उपयोग करते हैं।

```

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // AEAD parameters for New Session Reply payload
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### Reply TagSet के लिए KDF

प्रतिक्रिया के आकार के आधार पर, कई NSR संदेश भेजे जा सकते हैं, प्रत्येक अद्वितीय ephemeral keys के साथ।

Alice और Bob को हर NS और NSR संदेश के लिए नई ephemeral keys का उपयोग करना आवश्यक है।

Alice को Bob के ES संदेश भेजने से पहले Bob के NSR संदेशों में से एक प्राप्त करना चाहिए, और Bob को ES संदेश भेजने से पहले Alice से एक ES संदेश प्राप्त करना चाहिए।

Bob के NSR Payload Section से ``chainKey`` और ``k`` का उपयोग प्रारंभिक ES DH Ratchets (दोनों दिशाओं में, DH Ratchet KDF देखें) के लिए inputs के रूप में किया जाता है।

Bob को केवल Alice से प्राप्त ES संदेशों के लिए Existing Sessions को बनाए रखना चाहिए। किसी भी अन्य बनाए गए inbound और outbound sessions (कई NSRs के लिए) को किसी दिए गए session के लिए Alice का पहला ES संदेश प्राप्त करने के तुरंत बाद नष्ट कर देना चाहिए।

### Reply Key Section Encrypted Contents के लिए KDF

Session tag (8 bytes) एन्क्रिप्टेड डेटा और MAC (नीचे धारा 3 देखें)

### पेलोड सेक्शन एन्क्रिप्टेड कंटेंट्स के लिए KDF

एन्क्रिप्टेड:

```

+----+----+----+----+----+----+----+----+
  |       Session Tag                     |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Session Tag :: 8 bytes, cleartext

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### नोट्स

एन्क्रिप्टेड length डेटा का शेष भाग है। डिक्रिप्टेड length एन्क्रिप्टेड length से 16 कम है। फॉर्मेट और आवश्यकताओं के लिए नीचे payload सेक्शन देखें।

KDF

```
See AEAD section below.

  // AEAD parameters for Existing Session payload
  k = The 32-byte session key associated with this session tag
  n = The message number N in the current chain, as retrieved from the associated Session Tag.
  ad = The session tag, 8 bytes
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1h) मौजूदा session प्रारूप

प्रारूप: 32-बाइट सार्वजनिक और निजी keys, little-endian।

औचित्य: [NTCP2](/docs/specs/ntcp2/) में उपयोग किया जाता है।

### प्रारूप

मानक Noise handshakes में, प्रत्येक दिशा में प्रारंभिक handshake संदेश ephemeral keys के साथ शुरू होते हैं जो cleartext में प्रसारित किए जाते हैं। चूंकि वैध X25519 keys को random से अलग किया जा सकता है, एक man-in-the-middle इन संदेशों को Existing Session संदेशों से अलग कर सकता है जो random session tags के साथ शुरू होते हैं। [NTCP2](/docs/specs/ntcp2/) ([Proposal 111](/proposals/111-ntcp-2/)) में, हमने key को obfuscate करने के लिए out-of-band static key का उपयोग करके एक low-overhead XOR function का उपयोग किया था। हालांकि, यहाँ threat model अलग है; हम नहीं चाहते कि कोई भी MitM किसी भी साधन का उपयोग करके traffic के destination की पुष्टि करे, या प्रारंभिक handshake संदेशों को Existing Session संदेशों से अलग करे।

इसलिए, New Session और New Session Reply संदेशों में ephemeral keys को transform करने के लिए [Elligator2](https://elligator.cr.yp.to/) का उपयोग किया जाता है ताकि वे uniform random strings से अप्रभेद्य हों।

### पेलोड

32-बाइट public और private keys। Encoded keys little endian हैं।

[Elligator2](https://elligator.cr.yp.to/) में परिभाषित अनुसार, एन्कोडेड keys 254 random bits से अप्रभेद्य हैं। हमें 256 random bits (32 bytes) की आवश्यकता है। इसलिए, encoding और decoding को निम्नलिखित रूप में परिभाषित किया गया है:

एन्कोडिंग:

```

ENCODE_ELG2() Definition

  // Encode as defined in Elligator2 specification
  encodedKey = encode(pubkey)
  // OR in 2 random bits to MSB
  randomByte = CSRNG(1)
  encodedKey[31] |= (randomByte & 0xc0)
```
डिकोडिंग:

```

DECODE_ELG2() Definition

  // Mask out 2 random bits from MSB
  encodedKey[31] &= 0x3f
  // Decode as defined in Elligator2 specification
  pubkey = decode(encodedKey)
```
### 2) ECIES-X25519

OBEP और IBGW को ट्रैफिक को वर्गीकृत करने से रोकने के लिए आवश्यक।

### 2a) Elligator2

Elligator2 औसत key generation time को दोगुना कर देता है, क्योंकि आधी private keys के परिणामस्वरूप ऐसी public keys बनती हैं जो Elligator2 के साथ encoding के लिए अनुपयुक्त होती हैं। साथ ही, key generation time exponential distribution के साथ असीमित होता है, क्योंकि generator को तब तक retry करते रहना पड़ता है जब तक कि उपयुक्त key pair नहीं मिल जाता।

इस overhead को अलग thread में पहले से key generation करके प्रबंधित किया जा सकता है, ताकि उपयुक्त keys का एक pool बनाए रखा जा सके।

generator ENCODE_ELG2() फ़ंक्शन को उपयुक्तता निर्धारित करने के लिए करता है। इसलिए, generator को ENCODE_ELG2() का परिणाम संग्रहीत करना चाहिए ताकि इसे दोबारा गणना न करनी पड़े।

इसके अतिरिक्त, अनुपयुक्त keys को [NTCP2](/docs/specs/ntcp2/) के लिए उपयोग की जाने वाली keys के pool में जोड़ा जा सकता है, जहाँ Elligator2 का उपयोग नहीं किया जाता। ऐसा करने की security issues अभी भी TBD हैं।

### प्रारूप

AEAD का उपयोग ChaCha20 और Poly1305 के साथ, [NTCP2](/docs/specs/ntcp2/) में समान। यह [RFC-7539](https://tools.ietf.org/html/rfc7539) से मेल खाता है, जो TLS [RFC-7905](https://tools.ietf.org/html/rfc7905) में भी समान रूप से उपयोग किया जाता है।

### औचित्य

New Session संदेश में एक AEAD ब्लॉक के लिए encryption/decryption फ़ंक्शन के लिए इनपुट:

```

k :: 32 byte cipher key
       See New Session and New Session Reply KDFs above.

  n :: Counter-based nonce, 12 bytes.
       n = 0

  ad :: Associated data, 32 bytes.
        The SHA256 hash of the preceding data, as output from mixHash()

  data :: Plaintext data, 0 or more bytes

```
### नोट्स

एक Existing Session message में AEAD block के लिए encryption/decryption functions के लिए इनपुट:

```

k :: 32 byte session key
       As looked up from the accompanying session tag.

  n :: Counter-based nonce, 12 bytes.
       Starts at 0 and incremented for each message when transmitting.
       For the receiver, the value
       as looked up from the accompanying session tag.
       First four bytes are always zero.
       Last eight bytes are the message number (n), little-endian encoded.
       Maximum value is 65535.
       Session must be ratcheted when N reaches that value.
       Higher values must never be used.

  ad :: Associated data
        The session tag

  data :: Plaintext data, 0 or more bytes

```
### 3) AEAD (ChaChaPoly)

encryption फंक्शन का आउटपुट, decryption फंक्शन का इनपुट:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       ChaCha20 encrypted data         |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  encrypted data :: Same size as plaintext data, 0 - 65519 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### नया Session और नया Session Reply Inputs

- चूंकि ChaCha20 एक stream cipher है, plaintexts को padded करने की आवश्यकता नहीं है।
  अतिरिक्त keystream bytes को discard कर दिया जाता है।

- cipher के लिए key (256 bits) SHA256 KDF के माध्यम से सहमत की जाती है।
  प्रत्येक message के लिए KDF के विवरण नीचे अलग sections में हैं।

- ChaChaPoly फ्रेम ज्ञात आकार के होते हैं क्योंकि वे I2NP डेटा संदेश में encapsulated होते हैं।

- सभी संदेशों के लिए,
  padding प्रमाणित
  डेटा फ्रेम के अंदर है।

### मौजूदा Session Inputs

सभी प्राप्त डेटा जो AEAD verification में असफल होता है, उसे त्याग दिया जाना चाहिए। कोई response वापस नहीं की जाती।

### एन्क्रिप्टेड प्रारूप

[NTCP2](/docs/specs/ntcp2/) में उपयोग किया जाता है।

### नोट्स

हम अभी भी session tags का उपयोग करते हैं, जैसा कि पहले करते थे, लेकिन हम उन्हें generate करने के लिए ratchets का उपयोग करते हैं। Session tags में एक rekey विकल्प भी था जिसे हमने कभी implement नहीं किया। तो यह double ratchet की तरह है लेकिन हमने कभी दूसरा वाला नहीं किया।

यहाँ हम Signal के Double Ratchet के समान कुछ परिभाषित करते हैं। session tags receiver और sender दोनों तरफ निर्धारक और समान रूप से उत्पन्न होते हैं।

symmetric key/tag ratchet का उपयोग करके, हम sender side पर session tags को store करने के लिए memory usage को समाप्त करते हैं। हम tag sets भेजने की bandwidth consumption को भी समाप्त करते हैं। Receiver side usage अभी भी महत्वपूर्ण है, लेकिन हम इसे और कम कर सकते हैं क्योंकि हम session tag को 32 bytes से 8 bytes तक छोटा करेंगे।

हम Signal में निर्दिष्ट (और वैकल्पिक) header encryption का उपयोग नहीं करते हैं, इसके बजाय हम session tags का उपयोग करते हैं।

DH ratchet का उपयोग करके, हम forward secrecy प्राप्त करते हैं, जो कभी भी ElGamal/AES+SessionTags में implement नहीं किया गया था।

नोट: New Session वन-टाइम public key रैचेट का हिस्सा नहीं है, इसका एकमात्र कार्य Alice की प्रारंभिक DH रैचेट key को एन्क्रिप्ट करना है।

### AEAD Error Handling

Double Ratchet प्रत्येक संदेश हेडर में एक tag शामिल करके खोए हुए या गलत क्रम में आने वाले संदेशों को संभालता है। प्राप्तकर्ता tag के index को देखता है, यह संदेश संख्या N है। यदि संदेश में PN वैल्यू के साथ एक Message Number block है, तो प्राप्तकर्ता पिछले tag set में उस वैल्यू से अधिक किसी भी tag को हटा सकता है, जबकि पिछले tag set के छूटे हुए tags को बनाए रख सकता है इस मामले में कि छूटे हुए संदेश बाद में पहुंचें।

### औचित्य

हम इन ratchets को implement करने के लिए निम्नलिखित data structures और functions को परिभाषित करते हैं।

TAGSET_ENTRY

    A single entry in a TAGSET.

    INDEX
        An integer index, starting with 0

    SESSION_TAG
        An identifier to go out on the wire, 8 bytes

    SESSION_KEY
        A symmetric key, never goes on the wire, 32 bytes

TAGSET

    A collection of TAGSET_ENTRIES.

    CREATE(key, n)
        Generate a new TAGSET using initial cryptographic key material of 32 bytes.
        The associated session identifier is provided.
        The initial number of of tags to create is specified; this is generally 0 or 1
        for an outgoing session.
        LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)
        Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()
        Generate one more TAGSET_ENTRY, unless the maximum number SESSION_TAGS have
        already been generated.
        If LAST_INDEX is greater than or equal to 65535, return.
        ++ LAST_INDEX
        Create a new TAGSET_ENTRY with the LAST_INDEX value and the calculated SESSION_TAG.
        Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may
        be deferred and calculated in GET_SESSION_KEY().
        Calls EXPIRE()

    EXPIRE()
        Remove tags and keys that are too old, or if the TAGSET size exceeds some limit.

    RATCHET_TAG()
        Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()
        Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION
        The associated session.

    CREATION_TIME
        When the TAGSET was created.

    LAST_INDEX
        The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()
        Used for outgoing sessions only.
        EXTEND(1) is called if there are no remaining TAGSET_ENTRIES.
        If EXTEND(1) did nothing, the max of 65535 TAGSETS have been used,
        and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)
        Used for incoming sessions only.
        Returns the TAGSET_ENTRY containing the sessionTag.
        If found, the TAGSET_ENTRY is removed.
        If the SESSION_KEY calculation was deferred, it is calculated now.
        If there are few TAGSET_ENTRIES remaining, EXTEND(n) is called.


### 4) Ratchets

Ratchets करते हैं लेकिन Signal की तरह उतनी तेज़ी से नहीं। हम प्राप्त की का ack को नई key generate करने से अलग करते हैं। सामान्य उपयोग में, Alice और Bob दोनों New Session में तुरंत ratchet करेंगे (दो बार), लेकिन दोबारा ratchet नहीं करेंगे।

ध्यान दें कि एक ratchet एक ही दिशा के लिए होता है, और उस दिशा के लिए एक New Session tag / message key ratchet chain उत्पन्न करता है। दोनों दिशाओं के लिए keys उत्पन्न करने के लिए, आपको दो बार ratchet करना होगा।

आप हर बार जब एक नई key generate और send करते हैं तो आप ratchet करते हैं। आप हर बार जब एक नई key receive करते हैं तो आप ratchet करते हैं।

Alice एक बार ratchet करती है जब वह एक unbound outbound session बनाती है, वह inbound session नहीं बनाती (unbound non-repliable होता है)।

Bob एक बार ratchet करता है जब एक unbound inbound session बनाता है, और कोई संबंधित outbound session नहीं बनाता है (unbound गैर-जवाब देने योग्य होता है)।

Alice तब तक Bob को New Session (NS) संदेश भेजती रहती है जब तक उसे Bob के New Session Reply (NSR) संदेशों में से कोई एक प्राप्त नहीं हो जाता। फिर वह NSR के Payload Section KDF परिणामों को session ratchets के लिए इनपुट के रूप में उपयोग करती है (DH Ratchet KDF देखें), और Existing Session (ES) संदेश भेजना शुरू कर देती है।

प्रत्येक प्राप्त NS संदेश के लिए, Bob एक नया inbound session बनाता है, reply Payload Section के KDF परिणामों का उपयोग करके नए inbound और outbound ES DH Ratchet के लिए inputs के रूप में।

प्रत्येक आवश्यक reply के लिए, Bob Alice को payload में reply के साथ एक NSR message भेजता है। यह आवश्यक है कि Bob हर NSR के लिए नई ephemeral keys का उपयोग करे।

Bob को Alice से किसी एक inbound session पर ES message प्राप्त करना होगा, इससे पहले कि वह संबंधित outbound session पर ES messages बनाए और भेजे।

Alice को Bob से NSR message प्राप्त करने के लिए एक timer का उपयोग करना चाहिए। यदि timer समाप्त हो जाता है, तो session को हटा देना चाहिए।

KCI और/या resource exhaustion attack से बचने के लिए, जहाँ एक आक्रमणकारी Bob के NSR replies को drop करके Alice को NS messages भेजते रहने पर मजबूर करता है, Alice को timer expiration के कारण एक निश्चित संख्या की retries के बाद Bob के साथ New Sessions शुरू करने से बचना चाहिए।

Alice और Bob दोनों प्रत्येक प्राप्त NextKey ब्लॉक के लिए एक DH ratchet करते हैं।

Alice और Bob प्रत्येक DH ratchet के बाद नए tag setstchets और दो symmetric keys ratchets generate करते हैं। किसी दिए गए direction में प्रत्येक नए ES message के लिए, Alice और Bob session tag और symmtric key ratchets को advance करते हैं।

प्रारंभिक handshake के बाद DH ratchets की आवृत्ति implementation-dependent होती है। जबकि protocol एक ratchet की आवश्यकता से पहले 65535 संदेशों की सीमा रखता है, अधिक बार-बार ratcheting (संदेश की संख्या, बीते समय, या दोनों के आधार पर) अतिरिक्त सुरक्षा प्रदान कर सकती है।

bound sessions पर final handshake KDF के बाद, Bob और Alice को inbound और outbound sessions के लिए independent symmetric और tag chain keys बनाने हेतु resulting CipherState पर Noise Split() function चलाना आवश्यक है।

#### KEY AND TAG SET IDS

Key और tag set ID संख्याओं का उपयोग keys और tag sets की पहचान करने के लिए किया जाता है। Key IDs का उपयोग NextKey blocks में भेजी गई या उपयोग की गई key की पहचान करने के लिए किया जाता है। Tag set IDs का उपयोग (message संख्या के साथ) ACK blocks में उस message की पहचान करने के लिए किया जाता है जिसे ack किया जा रहा है। Key और tag set IDs दोनों एक ही दिशा के tag sets पर लागू होते हैं। Key और tag set ID संख्याएं क्रमिक होनी चाहिए।

प्रत्येक दिशा में एक session के लिए उपयोग किए जाने वाले पहले tag sets में, tag set ID 0 होती है। कोई NextKey blocks नहीं भेजे गए हैं, इसलिए कोई key IDs नहीं हैं।

DH ratchet शुरू करने के लिए, भेजने वाला एक नया NextKey ब्लॉक 0 की key ID के साथ भेजता है। प्राप्तकर्ता 0 की key ID के साथ एक नया NextKey ब्लॉक के साथ जवाब देता है। भेजने वाला फिर 1 की tag set ID के साथ एक नया tag set का उपयोग शुरू करता है।

बाद के tag set भी इसी तरह generate किए जाते हैं। NextKey exchanges के बाद उपयोग किए जाने वाले सभी tag set के लिए, tag set number (1 + Alice's key ID + Bob's key ID) होता है।

Key और tag set ID 0 से शुरू होती हैं और क्रमानुसार बढ़ती हैं। अधिकतम tag set ID 65535 है। अधिकतम key ID 32767 है। जब कोई tag set लगभग समाप्त हो जाता है, तो tag set sender को NextKey exchange शुरू करना चाहिए। जब tag set 65535 लगभग समाप्त हो जाता है, तो tag set sender को New Session message भेजकर एक नया session शुरू करना चाहिए।

1730 के streaming maximum message size के साथ, और कोई retransmissions नहीं मानते हुए, single tag set का उपयोग करके theoretical maximum data transfer 1730 * 65536 ~= 108 MB है। Retransmissions के कारण actual maximum इससे कम होगा।

सभी 65536 उपलब्ध tag sets के साथ सैद्धांतिक अधिकतम डेटा ट्रांसफर, session को त्यागना और बदलना पड़ने से पहले, 64K * 108 MB ~= 6.9 TB है।

#### DH RATCHET MESSAGE FLOW

एक tag set के लिए अगला key exchange उन tags के भेजने वाले (outbound tag set के मालिक) द्वारा शुरू किया जाना चाहिए। प्राप्तकर्ता (inbound tag set का मालिक) जवाब देगा। application layer पर एक सामान्य HTTP GET traffic के लिए, Bob अधिक messages भेजेगा और key exchange शुरू करके पहले ratchet करेगा; नीचे का diagram यह दिखाता है। जब Alice ratchet करती है, तो वही चीज़ विपरीत क्रम में होती है।

NS/NSR handshake के बाद उपयोग किया जाने वाला पहला tag set, tag set 0 है। जब tag set 0 लगभग समाप्त हो जाता है, तो tag set 1 बनाने के लिए दोनों दिशाओं में नई keys का आदान-प्रदान करना आवश्यक होता है। उसके बाद, एक नई key केवल एक दिशा में भेजी जाती है।

टैग सेट 2 बनाने के लिए, टैग भेजने वाला एक नई key भेजता है और टैग प्राप्त करने वाला अपनी पुरानी key का ID acknowledgement के रूप में भेजता है। दोनों पक्ष एक DH करते हैं।

tag set 3 बनाने के लिए, tag sender अपनी पुरानी key का ID भेजता है और tag receiver से एक नई key का अनुरोध करता है। दोनों पक्ष एक DH करते हैं।

बाद के tag sets को tag sets 2 और 3 की तरह generate किया जाता है। tag set नंबर (1 + sender key id + receiver key id) होता है।

```

Tag Sender                    Tag Receiver

                   ... use tag set #0 ...


  (Tagset #0 almost empty)
  (generate new key #0)

  Next Key, forward, request reverse, with key #0  -------->
  (repeat until next key received)

                              (generate new key #0, do DH, create IB Tagset #1)

          <-------------      Next Key, reverse, with key #0
                              (repeat until tag received on new tagset)

  (do DH, create OB Tagset #1)


                   ... use tag set #1 ...


  (Tagset #1 almost empty)
  (generate new key #1)

  Next Key, forward, with key #1        -------->
  (repeat until next key received)

                              (reuse key #0, do DH, create IB Tagset #2)

          <--------------     Next Key, reverse, id 0
                              (repeat until tag received on new tagset)

  (do DH, create OB Tagset #2)


                   ... use tag set #2 ...


  (Tagset #2 almost empty)
  (reuse key #1)

  Next Key, forward, request reverse, id 1  -------->
  (repeat until next key received)

                              (generate new key #1, do DH, create IB Tagset #3)

          <--------------     Next Key, reverse, with key #1

  (do DH, create OB Tagset #3)
  (reuse key #1, do DH, create IB Tagset #3)


                   ... use tag set #3 ...


       After tag set 3, repeat the above
       patterns as shown for tag sets 2 and 3.

       To create a new even-numbered tag set, the sender sends a new key
       to the receiver. The receiver sends his old key ID
       back as an acknowledgement.

       To create a new odd-numbered tag set, the sender sends a reverse request
       to the receiver. The receiver sends a new reverse key to the sender.

```
जब outbound tagset के लिए DH ratchet पूरा हो जाता है, और एक नया outbound tagset बनाया जाता है, तो इसका तुरंत उपयोग किया जाना चाहिए, और पुराने outbound tagset को हटाया जा सकता है।

DH ratchet के inbound tagset के लिए पूरा होने के बाद, और एक नया inbound tagset बनने के बाद, receiver को दोनों tagsets में tags को सुनना चाहिए, और पुराने tagset को कुछ समय बाद, लगभग 3 मिनट बाद delete कर देना चाहिए।

नीचे दी गई तालिका में tag set और key ID progression का सारांश है। * यह दर्शाता है कि एक नई key generate की गई है।

| New Tag Set ID | Sender key ID | Rcvr key ID |
|----------------|---------------|-------------|
| 0              | n/a           | n/a         |
| 1              | 0 *           | 0 *         |
| 2              | 1 *           | 0           |
| 3              | 1             | 1 *         |
| 4              | 2 *           | 1           |
| 5              | 2             | 2 *         |
| ...            | ...           | ...         |
| 65534          | 32767 *       | 32766       |
| 65535          | 32767         | 32767 *     |
Key और tag set ID संख्याएं अनुक्रमिक होनी चाहिए।

#### DH INITIALIZATION KDF

यह एक दिशा के लिए DH_INITIALIZE(rootKey, k) की परिभाषा है। यह एक tagset बनाता है, और एक "next root key" बनाता है जो आवश्यकता पड़ने पर बाद के DH ratchet के लिए उपयोग किया जाता है।

हम तीन स्थानों पर DH initialization का उपयोग करते हैं। पहले, हम इसका उपयोग New Session Replies के लिए एक tag set उत्पन्न करने के लिए करते हैं। दूसरे, हम दो tag sets उत्पन्न करने के लिए इसका उपयोग करते हैं, प्रत्येक दिशा के लिए एक, Existing Session messages में उपयोग के लिए। अंत में, हम DH Ratchet के बाद इसका उपयोग करते हैं ताकि अतिरिक्त Existing Session messages के लिए एक दिशा में एक नया tag set उत्पन्न कर सकें।

```

Inputs:
  1) rootKey = chainKey from Payload Section
  2) k from the New Session KDF or split()

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // Output 1: The next Root Key (KDF input for the next DH ratchet)
  nextRootKey = keydata[0:31]
  // Output 2: The chain key to initialize the new
  // session tag and symmetric key ratchets
  // for the tag set
  ck = keydata[32:63]

  // session tag and symmetric key chain keys
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

```
#### DH RATCHET KDF

यह नई DH keys के NextKey blocks में exchange होने के बाद उपयोग किया जाता है, tagset के समाप्त होने से पहले।

```


// Tag sender generates new X25519 ephemeral keys
  // and sends rapk to tag receiver in a NextKey block
  rask = GENERATE_PRIVATE()
  rapk = DERIVE_PUBLIC(rask)
  
  // Tag receiver generates new X25519 ephemeral keys
  // and sends rbpk to Tag sender in a NextKey block
  rbsk = GENERATE_PRIVATE()
  rbpk = DERIVE_PUBLIC(rbsk)

  sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
  tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
  rootKey = nextRootKey // from previous tagset in this direction
  newTagSet = DH_INITIALIZE(rootKey, tagsetKey)

```
### संदेश संख्याएं

हर संदेश के लिए Ratchets, जैसा कि Signal में होता है। Session tag ratchet, symmetric key ratchet के साथ synchronized होता है, लेकिन receiver key ratchet मेमोरी बचाने के लिए "पीछे रह" सकता है।

Transmitter प्रत्येक भेजे गए संदेश के लिए एक बार ratchet करता है। कोई अतिरिक्त tags संग्रहीत करने की आवश्यकता नहीं है। Transmitter को वर्तमान chain में संदेश की संदेश संख्या 'N' के लिए एक counter भी रखना चाहिए। 'N' मान भेजे गए संदेश में शामिल किया जाता है। Message Number block की परिभाषा देखें।

रिसीवर को अधिकतम window साइज़ से आगे ratchet करना होगा और tags को एक "tag set" में स्टोर करना होगा, जो session के साथ जुड़ा होता है। एक बार प्राप्त होने पर, स्टोर किए गए tag को हटाया जा सकता है, और यदि कोई पिछले अप्राप्त tags नहीं हैं, तो window को आगे बढ़ाया जा सकता है। रिसीवर को प्रत्येक session tag के साथ जुड़े 'N' value को रखना चाहिए, और जांचना चाहिए कि भेजे गए संदेश में number इस value से मेल खाता है या नहीं। Message Number block definition देखें।

#### KDF

यह RATCHET_TAG() की परिभाषा है।

```

Inputs:
  1) Session Tag Chain key sessTag_ck
     First time: output from DH ratchet
     Subsequent times: output from previous session tag ratchet

  Generated:
  2) input_key_material = SESSTAG_CONSTANT
     Must be unique for this tag set (generated from chain key),
     so that the sequence isn't predictable, since session tags
     go out on the wire in plaintext.

  Outputs:
  1) N (the current session tag number)
  2) the session tag (and symmetric key, probably)
  3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

  Initialization:
  keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
  // Output 1: Next chain key
  sessTag_chainKey = keydata[0:31]
  // Output 2: The constant
  SESSTAG_CONSTANT = keydata[32:63]

  // KDF_ST(ck, constant)
  keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
  // Output 1: Next chain key
  sessTag_chainKey_0 = keydata_0[0:31]
  // Output 2: The session tag
  // or more if tag is longer than 8 bytes
  tag_0 = keydata_0[32:39]

  // repeat as necessary to get to tag_n
  keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
  // Output 1: Next chain key
  sessTag_chainKey_n = keydata_n[0:31]
  // Output 2: The session tag
  // or more if tag is longer than 8 bytes
  tag_n = keydata_n[32:39]

```
### नमूना कार्यान्वयन

हर संदेश के लिए Ratchets, जैसा कि Signal में होता है। प्रत्येक symmetric key का एक संबंधित message number और session tag होता है। Session key ratchet, symmetric tag ratchet के साथ synchronized होता है, लेकिन receiver key ratchet memory बचाने के लिए "पीछे रह" सकता है।

Transmitter प्रत्येक संदेश प्रसारण के लिए एक बार ratchet करता है। कोई अतिरिक्त keys संग्रहीत करनी आवश्यक नहीं है।

जब receiver को एक session tag मिलता है, यदि उसने पहले से ही symmetric key ratchet को associated key तक आगे नहीं बढ़ाया है, तो उसे associated key तक "catch up" करना होगा। Receiver संभवतः किसी भी पिछले tags के लिए keys को cache करेगा जो अभी तक प्राप्त नहीं हुए हैं। एक बार प्राप्त होने पर, stored key को discard किया जा सकता है, और यदि कोई पिछले unreceived tags नहीं हैं, तो window को आगे बढ़ाया जा सकता है।

दक्षता के लिए, session tag और symmetric key ratchets अलग होते हैं ताकि session tag ratchet, symmetric key ratchet से आगे चल सके। यह कुछ अतिरिक्त सुरक्षा भी प्रदान करता है, क्योंकि session tags wire पर जाते हैं।

#### KDF

यह RATCHET_KEY() की परिभाषा है।

```

Inputs:
  1) Symmetric Key Chain key symmKey_ck
     First time: output from DH ratchet
     Subsequent times: output from previous symmetric key ratchet

  Generated:
  2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
     No need for uniqueness. Symmetric keys never go out on the wire.
     TODO: Set a constant anyway?

  Outputs:
  1) N (the current session key number)
  2) the session key
  3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

  // KDF_CK(ck, constant)
  SYMMKEY_CONSTANT = ZEROLEN
  // Output 1: Next chain key
  keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
  symmKey_chainKey_0 = keydata_0[0:31]
  // Output 2: The symmetric key
  k_0 = keydata_0[32:63]

  // repeat as necessary to get to k[n]
  keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
  // Output 1: Next chain key
  symmKey_chainKey_n = keydata_n[0:31]
  // Output 2: The symmetric key
  k_n = keydata_n[32:63]


```
### 4a) DH Ratchet

यह ElGamal/AES+SessionTags विनिर्देश में परिभाषित AES अनुभाग प्रारूप को प्रतिस्थापित करता है।

यह [NTCP2](/docs/specs/ntcp2/) specification में परिभाषित समान block format का उपयोग करता है। व्यक्तिगत block types को अलग तरीके से परिभाषित किया गया है।

चिंताएं हैं कि implementers को कोड साझा करने के लिए प्रोत्साहित करना parsing संबंधी समस्याओं का कारण बन सकता है। Implementers को कोड साझा करने के फायदे और जोखिमों पर सावधानीपूर्वक विचार करना चाहिए, और यह सुनिश्चित करना चाहिए कि दोनों contexts के लिए ordering और valid block के नियम अलग हों।

### Payload Section Decrypted data

एन्क्रिप्टेड length डेटा का शेष भाग है। डिक्रिप्टेड length एन्क्रिप्टेड length से 16 कम है। सभी block types समर्थित हैं। सामान्य contents में निम्नलिखित blocks शामिल हैं:

| Payload Block Type | Type Number | Block Length |
|--------------------|-------------|--------------|
| DateTime           | 0           | 7            |
| Termination (TBD)  | 4           | 9 typ.       |
| Options (TBD)      | 5           | 21+          |
| Message Number (TBD) | 6           | TBD          |
| Next Key           | 7           | 3 or 35      |
| ACK                | 8           | 4 typ.       |
| ACK Request        | 9           | 3            |
| Garlic Clove       | 11          | varies       |
| Padding            | 254         | varies       |
### Unencrypted data

encrypted frame में शून्य या अधिक blocks होते हैं। प्रत्येक block में एक one-byte identifier, एक two-byte length, और शून्य या अधिक bytes का data होता है।

extensibility के लिए, receivers को अज्ञात type numbers वाले blocks को ignore करना चाहिए, और उन्हें padding की तरह treat करना चाहिए।

एन्क्रिप्टेड डेटा अधिकतम 65535 बाइट्स का है, जिसमें 16-बाइट प्रमाणीकरण हेडर शामिल है, इसलिए अधिकतम अनएन्क्रिप्टेड डेटा 65519 बाइट्स का है।

(Poly1305 auth tag दिखाया नहीं गया):

```

+----+----+----+----+----+----+----+----+
  |blk |  size   |       data             |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |blk |  size   |       data             |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  ~               .   .   .               ~

  blk :: 1 byte
         0 datetime
         1-3 reserved
         4 termination
         5 options
         6 previous message number
         7 next session key
         8 ack
         9 ack request
         10 reserved
         11 Garlic Clove
         224-253 reserved for experimental features
         254 for padding
         255 reserved for future extension
  size :: 2 bytes, big endian, size of data to follow, 0 - 65516
  data :: the data

  Maximum ChaChaPoly frame is 65535 bytes.
  Poly1305 tag is 16 bytes
  Maximum total block size is 65519 bytes
  Maximum single block size is 65519 bytes
  Block type is 1 byte
  Block length is 2 bytes
  Maximum single block data size is 65516 bytes.

```
### Block Ordering Rules

New Session मैसेज में, DateTime ब्लॉक आवश्यक है, और यह पहला ब्लॉक होना चाहिए।

अन्य अनुमतित ब्लॉक्स:

- Garlic Clove (type 11)
- विकल्प (type 5)
- Padding (type 254)

New Session Reply संदेश में, कोई blocks की आवश्यकता नहीं है।

अन्य अनुमतित ब्लॉक्स:

- Garlic Clove (टाइप 11)
- Options (टाइप 5)
- Padding (टाइप 254)

कोई अन्य blocks की अनुमति नहीं है। Padding, यदि उपस्थित है, तो अंतिम block होना चाहिए।

Existing Session संदेश में, कोई blocks आवश्यक नहीं हैं, और क्रम अनिर्दिष्ट है, निम्नलिखित आवश्यकताओं को छोड़कर:

Termination, यदि मौजूद है, तो Padding को छोड़कर अंतिम block होना चाहिए। Padding, यदि मौजूद है, तो अंतिम block होना चाहिए।

एक single frame में कई Garlic Clove blocks हो सकते हैं। एक single frame में अधिकतम दो Next Key blocks हो सकते हैं। एक single frame में कई Padding blocks की अनुमति नहीं है। अन्य block types में शायद एक single frame में कई blocks नहीं होंगे, लेकिन यह प्रतिबंधित नहीं है।

### DateTime

एक समाप्ति। रिप्लाई रोकथाम में सहायता करती है। Bob को इस timestamp का उपयोग करके यह validate करना होगा कि संदेश हाल का है। यदि समय वैध है, तो Bob को replay attacks को रोकने के लिए Bloom filter या अन्य तंत्र implement करना होगा। आमतौर पर केवल New Session संदेशों में शामिल किया जाता है।

```

+----+----+----+----+----+----+----+
  | 0  |    4    |     timestamp     |
  +----+----+----+----+----+----+----+

  blk :: 0
  size :: 2 bytes, big endian, value = 4
  timestamp :: Unix timestamp, unsigned seconds.
               Wraps around in 2106

```
### 4b) Session Tag Ratchet

एक single decrypted Garlic Clove जैसा कि [I2NP](/docs/specs/i2np/) में निर्दिष्ट है, उन fields को हटाने के लिए modifications के साथ जो unused या redundant हैं। चेतावनी: यह format ElGamal/AES के लिए वाले से काफी अलग है। प्रत्येक clove एक अलग payload block है। Garlic Cloves को blocks के बीच या ChaChaPoly frames के बीच fragment नहीं किया जा सकता।

```

+----+----+----+----+----+----+----+----+
  | 11 |  size   |                        |
  +----+----+----+                        +
  |      Delivery Instructions            |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |type|  Message_ID       | Expiration   
  +----+----+----+----+----+----+----+----+
       |      I2NP Message body           |
  +----+                                  +
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  size :: size of all data to follow

  Delivery Instructions :: As specified in
         the Garlic Clove section of [I2NP](/docs/specs/i2np/).
         Length varies but is typically 1, 33, or 37 bytes

  type :: I2NP message type

  Message_ID :: 4 byte `Integer` I2NP message ID

  Expiration :: 4 bytes, seconds since the epoch

```
नोट्स:

- कार्यान्वयनकर्ताओं को यह सुनिश्चित करना चाहिए कि एक block को पढ़ते समय,
  विकृत या दुर्भावनापूर्ण डेटा के कारण अगले block में overrun न हो।

- [I2NP](/docs/specs/i2np/) में निर्दिष्ट Clove Set प्रारूप का उपयोग नहीं किया जाता है।
  प्रत्येक clove अपने स्वयं के ब्लॉक में समाहित होता है।

- I2NP संदेश हेडर 9 बाइट्स का है, जो [NTCP2](/docs/specs/ntcp2/) में उपयोग किए गए फॉर्मेट के समान है।

- [I2NP](/docs/specs/i2np/) में Garlic Message परिभाषा से Certificate, Message ID, और Expiration शामिल नहीं हैं।

- Certificate, Clove ID, और Expiration को [I2NP](/docs/specs/i2np/) में Garlic Clove definition से शामिल नहीं किया गया है।

औचित्य:

- certificates का कभी उपयोग नहीं किया गया था।
- अलग message ID और clove IDs का कभी उपयोग नहीं किया गया था।
- अलग expirations का कभी उपयोग नहीं किया गया था।
- पुराने Clove Set और Clove formats की तुलना में कुल मिलाकर बचत
  1 clove के लिए लगभग 35 bytes, 2 cloves के लिए 54 bytes,
  और 3 cloves के लिए 73 bytes है।
- Block format extensible है और कोई भी नए fields को
  नए block types के रूप में जोड़ा जा सकता है।

### Termination

कार्यान्वयन वैकल्पिक है। session को drop करें। यह frame में अंतिम non-padding block होना चाहिए। इस session में कोई और messages नहीं भेजे जाएंगे।

NS या NSR में अनुमति नहीं है। केवल Existing Session messages में शामिल किया जाता है।

```

+----+----+----+----+----+----+----+----+
  | 4  |  size   | rsn|     addl data     |
  +----+----+----+----+                   +
  ~               .   .   .               ~
  +----+----+----+----+----+----+----+----+

  blk :: 4
  size :: 2 bytes, big endian, value = 1 or more
  rsn :: reason, 1 byte:
         0: normal close or unspecified
         1: termination received
         others: optional, impementation-specific
  addl data :: optional, 0 or more bytes, for future expansion, debugging,
               or reason text.
               Format unspecified and may vary based on reason code.

```
### 4c) Symmetric Key Ratchet (सममित कुंजी रैचेट)

अभी तक UNIMPLEMENTED, आगे के अध्ययन के लिए। अपडेट किए गए options पास करें। Options में session के लिए विभिन्न parameters शामिल होते हैं। अधिक जानकारी के लिए नीचे Session Tag Length Analysis अनुभाग देखें।

options block परिवर्तनीय लंबाई का हो सकता है, क्योंकि more_options उपस्थित हो सकते हैं।

```

+----+----+----+----+----+----+----+----+
  | 5  |  size   |ver |flg |STL |STimeout |
  +----+----+----+----+----+----+----+----+
  |  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
  +----+----+----+----+----+----+----+----+
  |  tdmy   |  rdmy   |  tdelay |  rdelay |
  +----+----+----+----+----+----+----+----+
  |              more_options             |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 5
  size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
  ver :: Protocol version, must be 0
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility
  STL :: Session tag length (must be 8), other values unimplemented
  STimeout :: Session idle timeout (seconds), big endian
  SOTW :: Sender Outbound Tag Window, 2 bytes big endian
  RITW :: Receiver Inbound Tag Window 2 bytes big endian

  tmin, tmax, rmin, rmax :: requested padding limits
      tmin and rmin are for desired resistance to traffic analysis.
      tmax and rmax are for bandwidth limits.
      tmin and tmax are the transmit limits for the router sending this options block.
      rmin and rmax are the receive limits for the router sending this options block.
      Each is a 4.4 fixed-point float representing 0 to 15.9375
      (or think of it as an unsigned 8-bit integer divided by 16.0).
      This is the ratio of padding to data. Examples:
      Value of 0x00 means no padding
      Value of 0x01 means add 6 percent padding
      Value of 0x10 means add 100 percent padding
      Value of 0x80 means add 800 percent (8x) padding
      Alice and Bob will negotiate the minimum and maximum in each direction.
      These are guidelines, there is no enforcement.
      Sender should honor receiver's maximum.
      Sender may or may not honor receiver's minimum, within bandwidth constraints.

  tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
  rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
  tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
  rdelay: Requested intra-message delay, 2 bytes big endian, msec average

  more_options :: Format undefined, for future use

```
SOTW प्रेषक की ओर से प्राप्तकर्ता को प्राप्तकर्ता की inbound tag window (अधिकतम lookahead) के लिए सिफारिश है। RITW प्रेषक की inbound tag window (अधिकतम lookahead) की घोषणा है जिसका उपयोग करने की वह योजना बनाता है। प्रत्येक पक्ष फिर किसी न्यूनतम या अधिकतम या अन्य गणना के आधार पर lookahead को सेट या समायोजित करता है।

नोट्स:

- गैर-डिफ़ॉल्ट session tag length के लिए समर्थन की उम्मीद है कि
  कभी भी आवश्यक नहीं होगी।
- Tag window Signal दस्तावेज़ में MAX_SKIP है।

समस्याएं:

- विकल्प परामर्श (Options negotiation) अभी तय होना है।
- डिफ़ॉल्ट अभी तय होने हैं।
- पैडिंग और देरी के विकल्प NTCP2 से कॉपी किए गए हैं,
  लेकिन वे विकल्प वहाँ पूरी तरह से लागू या अध्ययन नहीं किए गए हैं।

### Message Numbers

कार्यान्वयन वैकल्पिक है। पिछले tag set (PN) में लंबाई (भेजे गए संदेशों की संख्या)। Receiver तुरंत पिछले tag set से PN से अधिक tags को हटा सकता है। Receiver थोड़े समय बाद (जैसे 2 मिनट) पिछले tag set से PN के बराबर या उससे कम tags को expire कर सकता है।

```

+----+----+----+----+----+
  | 6  |  size   |  PN    |
 +----+----+----+----+----+

  blk :: 6
  size :: 2
  PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.

```
नोट्स:

- अधिकतम PN 65535 है।
- PN की परिभाषा Signal की परिभाषा के बराबर है, माइनस वन।
  यह Signal के समान है, लेकिन Signal में, PN और N हेडर में होते हैं।
  यहाँ, वे एन्क्रिप्टेड मैसेज बॉडी में हैं।
- इस ब्लॉक को tag set 0 में न भेजें, क्योंकि कोई पिछला tag set नहीं था।

### 5) पेलोड

अगली DH ratchet key payload में है, और यह वैकल्पिक है। हम हर बार ratchet नहीं करते। (यह signal से अलग है, जहाँ यह header में होती है, और हर बार भेजी जाती है)

पहले ratchet के लिए, Key ID = 0.

NS या NSR में अनुमति नहीं है। केवल Existing Session संदेशों में शामिल किया जाता है।

```

+----+----+----+----+----+----+----+----+
  | 7  |  size   |flag|  key ID |         |
  +----+----+----+----+----+----+         +
  |                                       |
  +                                       +
  |     Next DH Ratchet Public Key        |
  +                                       +
  |                                       |
  +                             +----+----+
  |                             |
  +----+----+----+----+----+----+

  blk :: 7
  size :: 3 or 35
  flag :: 1 byte flags
          bit order: 76543210
          bit 0: 1 for key present, 0 for no key present
          bit 1: 1 for reverse key, 0 for forward key
          bit 2: 1 to request reverse key, 0 for no request
                 only set if bit 1 is 0
          bits 7-2: Unused, set to 0 for future compatibility
  key ID :: The key ID of this key. 2 bytes, big endian
            0 - 32767
  Public Key :: The next X25519 public key, 32 bytes, little endian
                Only if bit 0 is 1


```
नोट्स:

- Key ID उस tag set के लिए उपयोग की जाने वाली local key के लिए एक बढ़ता हुआ counter है, जो 0 से शुरू होता है।
- ID तब तक नहीं बदलना चाहिए जब तक key नहीं बदलती।
- यह strictly आवश्यक नहीं हो सकता, लेकिन debugging के लिए उपयोगी है।
  Signal key ID का उपयोग नहीं करता।
- अधिकतम Key ID 32767 है।
- दुर्लभ स्थिति में जब दोनों दिशाओं में tag sets एक साथ ratcheting कर रहे हों,
  एक frame में दो Next Key blocks होंगे, एक forward key के लिए और एक reverse key के लिए।
- Key और tag set ID numbers sequential होने चाहिए।
- विवरण के लिए ऊपर DH Ratchet section देखें।

### Payload Section डिक्रिप्टेड डेटा

यह केवल तभी भेजा जाता है जब एक ack request block प्राप्त हुआ हो। कई messages को ack करने के लिए कई acks उपस्थित हो सकते हैं।

NS या NSR में अनुमति नहीं है। केवल Existing Session संदेशों में शामिल किया जाता है।

```
+----+----+----+----+----+----+----+----+
  | 8  |  size   |tagsetid |   N     |    |
  +----+----+----+----+----+----+----+    +
  |             more acks                 |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 8
  size :: 4 * number of acks to follow, minimum 1 ack
  for each ack:
  tagsetid :: 2 bytes, big endian, from the message being acked
  N :: 2 bytes, big endian, from the message being acked


```
नोट्स:

- टैग सेट ID और N उस संदेश की विशिष्ट पहचान करते हैं जिसे ack किया जा रहा है।
- प्रत्येक दिशा में session के लिए उपयोग किए जाने वाले पहले tag sets में, tag set ID 0 होता है।
- कोई NextKey blocks नहीं भेजे गए हैं, इसलिए कोई key IDs नहीं हैं।
- NextKey exchanges के बाद उपयोग किए जाने वाले सभी tag sets के लिए, tag set number (1 + Alice's key ID + Bob's key ID) होता है।

### अनएन्क्रिप्टेड डेटा

एक in-band ack का अनुरोध करें। Garlic Clove में out-of-band DeliveryStatus Message को बदलने के लिए।

यदि एक स्पष्ट ack का अनुरोध किया जाता है, तो वर्तमान tagset ID और message number (N) को एक ack block में वापस किया जाता है।

NS या NSR में अनुमतित नहीं है। केवल Existing Session संदेशों में शामिल किया गया है।

```

+----+----+----+----+
  |  9 |  size   |flg |
  +----+----+----+----+

  blk :: 9
  size :: 1
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility

```
### ब्लॉक क्रमबद्धता नियम

सभी padding AEAD frames के अंदर है। TODO AEAD के अंदर padding को मोटे तौर पर negotiated parameters का पालन करना चाहिए। TODO Alice ने अपने अनुरोधित tx/rx min/max parameters को NS message में भेजा। TODO Bob ने अपने अनुरोधित tx/rx min/max parameters को NSR message में भेजा। अपडेटेड options को data phase के दौरान भेजा जा सकता है। ऊपर दी गई options block जानकारी देखें।

यदि मौजूद है, तो यह frame में अंतिम block होना चाहिए।

```

+----+----+----+----+----+----+----+----+
  |254 |  size   |      padding           |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 254
  size :: 2 bytes, big endian, 0-65516
  padding :: zeros or random data

```
नोट्स:

- सभी-शून्य padding ठीक है, क्योंकि यह encrypted हो जाएगा।
- Padding रणनीतियाँ TBD।
- केवल-padding frames की अनुमति है।
- Padding डिफ़ॉल्ट 0-15 bytes है।
- Padding parameter negotiation के लिए options block देखें
- Min/max padding parameters के लिए options block देखें
- Negotiated padding के उल्लंघन पर router response implementation-dependent है।

### DateTime

Implementation को forward compatibility के लिए अज्ञात block types को ignore करना चाहिए।

### Garlic Clove

- पैडिंग लेंथ या तो प्रति-मैसेज के आधार पर तय की जानी चाहिए और 
  लेंथ डिस्ट्रिब्यूशन के अनुमान लगाने चाहिए, या रैंडम देरी जोड़ी जानी चाहिए।
  ये प्रतिरोधी उपाय DPI का प्रतिरोध करने के लिए शामिल किए जाने चाहिए, क्योंकि 
  मैसेज साइज़ अन्यथा यह प्रकट कर देते हैं कि I2P ट्रैफिक ट्रांसपोर्ट 
  प्रोटोकॉल द्वारा वहन किया जा रहा है। सटीक पैडिंग योजना भविष्य के काम का 
  क्षेत्र है, परिशिष्ट A इस विषय पर अधिक जानकारी प्रदान करता है।

## Typical Usage Patterns

### समाप्ति

यह सबसे विशिष्ट उपयोग मामला है, और अधिकांश गैर-HTTP स्ट्रीमिंग उपयोग मामले भी इस उपयोग मामले के समान होंगे। एक छोटा प्रारंभिक संदेश भेजा जाता है, एक उत्तर आता है, और अतिरिक्त संदेश दोनों दिशाओं में भेजे जाते हैं।

एक HTTP GET आमतौर पर एक ही I2NP message में फिट हो जाता है। Alice एक single new Session message के साथ एक छोटा request भेजती है, एक reply leaseset को bundle करते हुए। Alice में immediate ratchet से new key तक शामिल है। destination के साथ bind करने के लिए sig शामिल है। कोई ack का अनुरोध नहीं है।

Bob तुरंत ratchet करता है।

Alice तुरंत ratchet करती है।

उन sessions के साथ जारी रखता है।

```

Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5

```
### विकल्प

Alice के पास तीन विकल्प हैं:

1) केवल पहला संदेश भेजें (window size = 1), जैसे कि HTTP GET में। अनुशंसित नहीं।

2) streaming window तक भेजें, लेकिन समान Elligator2-encoded cleartext public key का उपयोग करते हुए। सभी संदेशों में समान next public key (ratchet) होता है। यह OBGW/IBEP के लिए दिखाई देगा क्योंकि वे सभी समान cleartext से शुरू होते हैं। चीजें 1) की तरह आगे बढ़ती हैं। अनुशंसित नहीं।

3) अनुशंसित implementation।    streaming window तक भेजें, लेकिन प्रत्येक के लिए अलग Elligator2-encoded cleartext public key (session) का उपयोग करते हुए।    सभी messages में समान next public key (ratchet) होता है।    यह OBGW/IBEP को दिखाई नहीं देगा क्योंकि वे सभी अलग cleartext से शुरू होते हैं।    Bob को पहचानना चाहिए कि उन सभी में समान next public key है,    और सभी को समान ratchet के साथ जवाब देना चाहिए।    Alice उस next public key का उपयोग करती है और आगे बढ़ती है।

विकल्प 3 संदेश प्रवाह:

```

Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack

```
### संदेश संख्याएं

एक एकल संदेश, जिसके लिए एक एकल उत्तर अपेक्षित है। अतिरिक्त संदेश या उत्तर भेजे जा सकते हैं।

HTTP GET के समान, लेकिन session tag window size और lifetime के लिए छोटे विकल्पों के साथ। शायद ratchet का अनुरोध न करें।

```

Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message

```
### अगली DH Ratchet Public Key

कई गुमनाम संदेश, जिनके लिए कोई उत्तर अपेक्षित नहीं है।

इस परिस्थिति में, Alice एक session का अनुरोध करती है, लेकिन binding के बिना। नया session message भेजा जाता है। कोई reply LS bundled नहीं है। एक reply DSM bundled है (यह एकमात्र use case है जिसमें bundled DSMs की आवश्यकता होती है)। कोई next key शामिल नहीं है। कोई reply या ratchet का अनुरोध नहीं किया गया है। कोई ratchet नहीं भेजा गया है। Options session tags window को शून्य पर सेट करते हैं।

```

Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->

```
### पावती

एक एकल गुमनाम संदेश, जिसका कोई उत्तर अपेक्षित नहीं है।

एक बार का संदेश भेजा जाता है। कोई reply LS या DSM bundled नहीं होते। कोई next key शामिल नहीं होती। कोई reply या ratchet का अनुरोध नहीं किया जाता। कोई ratchet नहीं भेजा जाता। Options, session tags window को शून्य पर सेट करते हैं।

```

Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message

```
### Ack अनुरोध

लंबे समय तक चलने वाले sessions किसी भी समय ratchet कर सकते हैं, या ratchet का अनुरोध कर सकते हैं, उस समय बिंदु से forward secrecy बनाए रखने के लिए। Sessions को ratchet करना होगा जब वे प्रति-session भेजे गए संदेशों की सीमा (65535) के पास पहुंचते हैं।

## Implementation Considerations

### पैडिंग

मौजूदा ElGamal/AES+SessionTag प्रोटोकॉल की तरह, implementations को session tag storage को सीमित करना चाहिए और memory exhaustion attacks से सुरक्षा करनी चाहिए।

कुछ अनुशंसित रणनीतियों में शामिल हैं:

- संग्रहीत session tags की संख्या पर कठोर सीमा
- memory pressure के दौरान निष्क्रिय inbound sessions की आक्रामक समाप्ति
- एक ही far-end destination से बंधे inbound sessions की संख्या पर सीमा
- memory pressure के दौरान session tag window का अनुकूली कमी और पुराने अप्रयुक्त tags का हटाना
- memory pressure के दौरान अनुरोध पर ratchet करने से इनकार

### अन्य block प्रकार

अनुशंसित parameters और timeouts:

- NSR tagset साइज़: 12 tsmin और tsmax
- ES tagset 0 साइज़: tsmin 24, tsmax 160
- ES tagset (1+) साइज़: 160 tsmin और tsmax
- NSR tagset timeout: receiver के लिए 3 मिनट
- ES tagset timeout: sender के लिए 8 मिनट, receiver के लिए 10 मिनट
- पिछले ES tagset को हटाने का समय: 3 मिनट बाद
- Tag N का tagset look ahead: min(tsmax, tsmin + N/4)
- Tag N के पीछे tagset trim: min(tsmax, tsmin + N/4) / 2
- अगली key भेजने का tag: TBD
- Tagset lifetime के बाद अगली key भेजें: TBD
- Session को बदलें यदि NS प्राप्त हो: 3 मिनट बाद
- अधिकतम clock skew: -5 मिनट से +2 मिनट तक
- NS replay filter अवधि: 5 मिनट
- Padding साइज़: 0-15 bytes (अन्य रणनीतियां TBD)

### भविष्य का काम

आने वाले संदेशों को वर्गीकृत करने के लिए निम्नलिखित सिफारिशें हैं।

### X25519 Only

एक tunnel पर जो केवल इस protocol के साथ उपयोग होता है, identification को वैसे ही करें जैसे वर्तमान में ElGamal/AES+SessionTags के साथ किया जाता है:

पहले, प्रारंभिक डेटा को session tag के रूप में मानें, और session tag को lookup करें। यदि मिल जाए, तो उस session tag के साथ संग्रहीत डेटा का उपयोग करके decrypt करें।

यदि नहीं मिला, तो प्रारंभिक डेटा को DH public key और nonce के रूप में मानें। DH ऑपरेशन और निर्दिष्ट KDF को निष्पादित करें, और शेष डेटा को decrypt करने का प्रयास करें।

### HTTP GET

एक tunnel पर जो इस protocol और ElGamal/AES+SessionTags दोनों को support करता है, incoming messages को निम्नलिखित प्रकार से classify करें:

ElGamal/AES+SessionTags विनिर्देश में एक दोष के कारण, AES ब्लॉक को एक यादृच्छिक गैर-mod-16 लंबाई तक padded नहीं किया जाता है। इसलिए, Existing Session संदेशों की लंबाई mod 16 हमेशा 0 होती है, और New Session संदेशों की लंबाई mod 16 हमेशा 2 होती है (क्योंकि ElGamal ब्लॉक 514 bytes लंबा होता है)।

यदि length mod 16, 0 या 2 नहीं है, तो प्रारंभिक डेटा को session tag के रूप में treat करें, और session tag को look up करें। यदि मिल जाता है, तो उस session tag से जुड़े stored डेटा का उपयोग करके decrypt करें।

यदि नहीं मिला, और length mod 16, 0 या 2 नहीं है, तो प्रारंभिक डेटा को एक DH public key और nonce के रूप में मानें। एक DH operation करें और निर्दिष्ट KDF, और शेष डेटा को decrypt करने का प्रयास करें। (relative traffic mix के आधार पर, और X25519 और ElGamal DH operations की relative costs के आधार पर, यह step अंत में भी किया जा सकता है)

अन्यथा, यदि length mod 16 शून्य है, तो प्रारंभिक डेटा को ElGamal/AES session tag के रूप में मानें, और session tag को देखें। यदि मिल जाता है, तो उस session tag से जुड़े संग्रहीत डेटा का उपयोग करके decrypt करें।

यदि नहीं मिला, और डेटा कम से कम 642 (514 + 128) bytes लंबा है, और length mod 16 का परिणाम 2 है, तो प्रारंभिक डेटा को ElGamal block के रूप में मानें। शेष डेटा को decrypt करने का प्रयास करें।

ध्यान दें कि यदि ElGamal/AES+SessionTag spec को non-mod-16 padding की अनुमति देने के लिए अपडेट किया जाता है, तो चीजों को अलग तरीके से करना होगा।

### HTTP POST

प्रारंभिक implementations द्विदिशीय traffic पर निर्भर करते हैं उच्च layers पर। यानी, implementations यह मान लेते हैं कि विपरीत दिशा में traffic जल्द ही transmit होगा, जो ECIES layer पर किसी भी आवश्यक response को मजबूर करेगा।

हालांकि, कुछ ट्रैफिक एकदिशीय या बहुत कम bandwidth का हो सकता है, जिससे समय पर प्रतिक्रिया उत्पन्न करने के लिए कोई उच्च-स्तरीय ट्रैफिक नहीं होता।

NS और NSR संदेशों की प्राप्ति के लिए प्रतिक्रिया आवश्यक है; ACK Request और Next Key blocks की प्राप्ति के लिए भी प्रतिक्रिया आवश्यक है।

एक परिष्कृत implementation एक timer शुरू कर सकता है जब इन messages में से कोई एक प्राप्त होता है जिसके लिए response की आवश्यकता होती है, और ECIES layer पर एक "empty" (कोई Garlic Clove block नहीं) response generate कर सकता है यदि कम समय (जैसे 1 second) में कोई reverse traffic नहीं भेजा जाता है।

NS और NSR संदेशों के responses के लिए और भी कम timeout उपयुक्त हो सकता है, ताकि यातायात को जितनी जल्दी हो सके कुशल ES संदेशों पर स्थानांतरित किया जा सके।

## Analysis

### Repliable Datagram

प्रत्येक दिशा में पहले दो messages के लिए Message overhead निम्नलिखित है। यह मानता है कि ACK से पहले प्रत्येक दिशा में केवल एक message है, या कोई भी अतिरिक्त messages को Existing Session messages के रूप में speculatively भेजा गया है। यदि delivered session tags का कोई speculative acks नहीं है, तो पुराने protocol का overhead बहुत अधिक है।

नए protocol के विश्लेषण के लिए कोई padding नहीं मानी गई है। कोई bundled leaseSet नहीं माना गया है।

### मल्टिपल Raw Datagrams

नया सेशन मैसेज, हर दिशा में समान:

```

ElGamal block:
  514 bytes

  AES block:
  - 2 byte tag count
  - 1024 bytes of tags (32 typical)
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte clove cert, id, exp.
  - 15 byte msg cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  1143 total

  Total:
  1657 bytes
```
मौजूदा session संदेश, प्रत्येक दिशा में समान:

```

AES block:
  - 32 byte session tag
  - 2 byte tag count
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte msg cert, id, exp.
  - 15 byte clove cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  151 total
```
```
Four message total (two each direction)
  3616 bytes overhead
```
### सिंगल Raw डेटाग्राम

Alice-to-Bob नया Session संदेश:

```

- 32 byte ephemeral public key
  - 32 byte static public key
  - 16 byte Poly1305 MAC
  - 7 byte DateTime block
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  148 bytes overhead
```
Bob-to-Alice नया सत्र उत्तर संदेश:

```

- 8 byte session tag
  - 32 byte ephemeral public key
  - 16 byte Poly1305 MAC
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  117 bytes overhead
```
मौजूदा session संदेश, प्रत्येक दिशा में समान:

```

- 8 byte session tag
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  69 bytes
```
### लंबे समय तक चलने वाले Sessions

कुल चार संदेश (प्रत्येक दिशा में दो):

```

372 bytes
  90% (approx. 10x) reduction compared to ElGamal/AES+SessionTags
```
केवल Handshake:

```

ElGamal: 1657 + 1657 = 3314 bytes
  Ratchet: 148 _ 117 = 265 bytes
  92% (approx. 12x) reduction compared to ElGamal/AES+SessionTags
```
दीर्घकालिक कुल (handshakes को नजरअंदाज करते हुए):

```
ElGamal: 151 + 32 byte tag sent previously = 183 bytes
  Ratchet: 69 bytes
  64% (approx. 3x) reduction compared to ElGamal/AES+SessionTags
```
### CPU

TODO इस अनुभाग को प्रस्ताव के स्थिर होने के बाद अपडेट करें।

निम्नलिखित cryptographic operations प्रत्येक पार्टी द्वारा New Session और New Session Reply संदेशों का आदान-प्रदान करने के लिए आवश्यक हैं:

- HMAC-SHA256: 3 प्रति HKDF, कुल TBD
- ChaChaPoly: 2 प्रत्येक
- X25519 key generation: 2 Alice, 1 Bob
- X25519 DH: 3 प्रत्येक
- Signature verification: 1 (Bob)

Alice प्रति-bound-session न्यूनतम 5 ECDHs की गणना करती है, Bob को प्रत्येक NS message के लिए 2, और Bob के प्रत्येक NSR message के लिए 3।

Bob भी प्रति-bound-session 6 ECDHs की गणना करता है, Alice के प्रत्येक NS message के लिए 3, और अपने प्रत्येक NSR message के लिए 3।

प्रत्येक Existing Session संदेश के लिए प्रत्येक पक्ष द्वारा निम्नलिखित क्रिप्टोग्राफिक operations आवश्यक हैं:

- HKDF: 2
- ChaChaPoly: 1

### रक्षा

वर्तमान session tag की लंबाई 32 bytes है। हमें अभी तक उस लंबाई के लिए कोई औचित्य नहीं मिला है, लेकिन हम archives की खोज जारी रखे हुए हैं। ऊपर दिया गया प्रस्ताव नई tag लंबाई को 8 bytes के रूप में परिभाषित करता है। 8 byte tag को उचित ठहराने वाला विश्लेषण निम्नलिखित है:

session tag ratchet को यादृच्छिक, समान रूप से वितरित tags उत्पन्न करने वाला माना जाता है। किसी विशेष session tag की लंबाई के लिए कोई क्रिप्टोग्राफिक कारण नहीं है। session tag ratchet symmetric key ratchet के साथ समकालिक है, लेकिन उससे स्वतंत्र आउटपुट उत्पन्न करता है। दोनों ratchets के आउटपुट अलग लंबाई के हो सकते हैं।

इसलिए, एकमात्र चिंता session tag collision की है। यह माना जाता है कि implementations दोनों sessions के साथ decrypt करने की कोशिश करके collisions को handle करने का प्रयास नहीं करेंगे; implementations केवल tag को या तो पिछले या नए session के साथ associate करेंगे, और उस tag के साथ दूसरे session पर प्राप्त कोई भी message decryption fail होने के बाद drop कर दिया जाएगा।

लक्ष्य एक session tag लंबाई का चयन करना है जो टकराव के जोखिम को कम करने के लिए पर्याप्त बड़ी हो, जबकि मेमोरी उपयोग को कम करने के लिए पर्याप्त छोटी हो।

यह मानता है कि implementations memory exhaustion attacks को रोकने के लिए session tag storage को सीमित करते हैं। यह इस संभावना को भी काफी कम कर देगा कि एक attacker collisions बना सके। नीचे Implementation Considerations section देखें।

सबसे खराब स्थिति के लिए, 64 नए inbound sessions प्रति सेकंड वाले व्यस्त server का मान लें। 15 मिनट के inbound session tag lifetime का मान लें (वर्तमान के समान, शायद इसे कम किया जाना चाहिए)। 32 के inbound session tag window का मान लें। 64 * 15 * 60 * 32 = 1,843,200 tags वर्तमान Java I2P max inbound tags 750,000 है और जहाँ तक हम जानते हैं यह कभी hit नहीं हुआ है।

दस लाख में से एक (1e-6) session tag collisions का लक्ष्य शायद पर्याप्त है। भीड़भाड़ के कारण रास्ते में एक संदेश छूटने की संभावना इससे कहीं अधिक है।

संदर्भ: https://en.wikipedia.org/wiki/Birthday_paradox संभावना तालिका अनुभाग।

32 बाइट session tags (256 bits) के साथ session tag space 1.2e77 है। 1e-18 probability के साथ collision की probability के लिए 4.8e29 entries की आवश्यकता होती है। 1e-6 probability के साथ collision की probability के लिए 4.8e35 entries की आवश्यकता होती है। 32 बाइट के 1.8 मिलियन tags कुल मिलाकर लगभग 59 MB होते हैं।

16 byte session tags (128 bits) के साथ session tag space 3.4e38 है। 1e-18 probability के साथ collision की संभावना के लिए 2.6e10 entries की आवश्यकता होती है। 1e-6 probability के साथ collision की संभावना के लिए 2.6e16 entries की आवश्यकता होती है। 16 bytes के 1.8 million tags कुल मिलाकर लगभग 30 MB होते हैं।

8 byte session tags (64 bits) के साथ session tag space 1.8e19 है। 1e-18 probability के साथ collision की संभावना के लिए 6.1 entries की आवश्यकता होती है। 1e-6 probability के साथ collision की संभावना के लिए 6.1e6 (6,100,000) entries की आवश्यकता होती है। 8 bytes के 1.8 million tags कुल मिलाकर लगभग 15 MB होते हैं।

6.1 मिलियन सक्रिय tags हमारे worst-case अनुमान के 1.8 मिलियन tags से 3 गुना से अधिक है। इसलिए collision की संभावना दस लाख में से एक से कम होगी। अतः हम निष्कर्ष निकालते हैं कि 8 byte session tags पर्याप्त हैं। इसके परिणामस्वरूप storage space में 4x की कमी होती है, इसके अतिरिक्त 2x की कमी इसलिए होती है क्योंकि transmit tags store नहीं किए जाते। इसलिए हमारे पास ElGamal/AES+SessionTags की तुलना में session tag memory usage में 8x की कमी होगी।

इन मान्यताओं के गलत होने की स्थिति में लचीलेपन को बनाए रखने के लिए, हम options में एक session tag length field शामिल करेंगे, ताकि default length को प्रति-session के आधार पर override किया जा सके। हम dynamic tag length negotiation को implement करने की अपेक्षा नहीं करते हैं जब तक कि यह बिल्कुल आवश्यक न हो।

implementations को कम से कम session tag collisions को पहचानना चाहिए, उन्हें gracefully handle करना चाहिए, और collisions की संख्या को log या count करना चाहिए। यद्यपि अभी भी अत्यंत असंभावित है, ये ElGamal/AES+SessionTags की तुलना में बहुत अधिक संभावित होंगे, और वास्तव में हो सकते हैं।

### पैरामीटर

प्रति सेकंड दोगुने sessions (128) और दोगुने tag window (64) का उपयोग करके, हमारे पास 4 गुना tags (7.4 मिलियन) हैं। एक मिलियन में से एक collision की संभावना के लिए अधिकतम 6.1 मिलियन tags है। 12 byte (या यहां तक कि 10 byte) tags एक बहुत बड़ा margin जोड़ देंगे।

हालांकि, क्या दस लाख में से एक की टक्कर की संभावना एक अच्छा लक्ष्य है? रास्ते में छूटने की संभावना से बहुत बड़ा होना ज्यादा उपयोगी नहीं है। Java के DecayingBloomFilter के लिए false-positive लक्ष्य लगभग 10,000 में से 1 है, लेकिन 1000 में से 1 भी गंभीर चिंता का विषय नहीं है। लक्ष्य को 10,000 में से 1 तक कम करने से, 8 byte tags के साथ काफी मार्जिन मिल जाता है।

### वर्गीकरण

भेजने वाला तुरंत tags और keys बनाता है, इसलिए कोई storage की आवश्यकता नहीं है। यह ElGamal/AES की तुलना में कुल storage आवश्यकताओं को आधे में काट देता है। ECIES tags 8 bytes के हैं जबकि ElGamal/AES के लिए 32 bytes हैं। यह कुल storage आवश्यकताओं को एक और factor of 4 से काट देता है। Per-tag session keys को receiver पर "gaps" को छोड़कर store नहीं किया जाता है, जो उचित loss rates के लिए न्यूनतम होते हैं।

tag expiration time में 33% की कमी से एक और 33% की बचत होती है, छोटे session समय को मानते हुए।

इसलिए, ElGamal/AES की तुलना में कुल स्थान की बचत 10.7 के कारक या 92% है।

## Related Changes

### केवल X25519

ECIES Destinations से Database Lookups: देखें [Proposal 154](/proposals/154-ecies-lookups), जो अब release 0.9.46 के लिए [I2NP](/docs/specs/i2np/) में शामिल कर दिया गया है।

इस प्रस्ताव के लिए leaseset के साथ X25519 public key प्रकाशित करने हेतु LS2 समर्थन की आवश्यकता है। [I2NP](/docs/specs/i2np/) में LS2 विनिर्देशों में कोई परिवर्तन आवश्यक नहीं है। सभी समर्थन को [Proposal 123](/proposals/123-new-netdb-entries) में डिज़ाइन, विनिर्दिष्ट, और कार्यान्वित किया गया था जो 0.9.38 में लागू किया गया।

### X25519 Shared ElGamal/AES+SessionTags के साथ

कोई नहीं। इस proposal के लिए LS2 support की आवश्यकता है, और I2CP options में एक property set करनी होगी जो enabled हो। [I2CP](/docs/specs/i2cp/) specifications में कोई बदलाव की आवश्यकता नहीं है। सभी support को [Proposal 123](/proposals/123-new-netdb-entries) में design, specify, और implement किया गया था जो 0.9.38 में implement हुआ।

ECIES को सक्षम करने के लिए आवश्यक विकल्प I2CP, BOB, SAM, या i2ptunnel के लिए एक एकल I2CP प्रॉपर्टी है।

सामान्य मान हैं i2cp.leaseSetEncType=4 केवल ECIES के लिए, या i2cp.leaseSetEncType=4,0 ECIES और ElGamal dual keys के लिए।

### Protocol-layer Responses

यह सेक्शन [Proposal 123](/proposals/123-new-netdb-entries) से कॉपी किया गया है।

SessionConfig Mapping में विकल्प:

```
  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  0: ElGamal
                                  1-3: See proposal 145
                                  4: This proposal.
```
### Create Leaseset2 Message

यह प्रपोज़ल LS2 की आवश्यकता है जो रिलीज़ 0.9.38 से समर्थित है। [I2CP](/docs/specs/i2cp/) स्पेसिफिकेशन में कोई बदलाव की आवश्यकता नहीं है। सभी समर्थन को [Proposal 123](/proposals/123-new-netdb-entries) में डिज़ाइन, निर्दिष्ट, और implement किया गया था जो 0.9.38 में implement हुआ।

### ओवरहेड

दोहरी keys के साथ LS2 का समर्थन करने वाला कोई भी router (0.9.38 या उच्चतर) को दोहरी keys वाले destinations के साथ connection का समर्थन करना चाहिए।

ECIES-only destinations को encrypted lookup replies प्राप्त करने के लिए अधिकांश floodfills को 0.9.46 में अपडेट करने की आवश्यकता होगी। [Proposal 154](/proposals/154-ecies-lookups) देखें।

ECIES-only destinations केवल उन अन्य destinations से कनेक्ट हो सकते हैं जो या तो ECIES-only हैं, या dual-key हैं।
