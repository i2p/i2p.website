---
title: "UDP Trackers"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "बंद"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
toc: true
---

## स्थिति

2025-06-24 की समीक्षा में अनुमोदित। विशिष्टता [UDP specification](/docs/specs/udp-bittorrent-announces/) पर है। zzzot 0.20.0-beta2 में कार्यान्वित। API 0.9.67 के रूप में i2psnark में कार्यान्वित। स्थिति के लिए अन्य कार्यान्वयनों के दस्तावेजीकरण की जांच करें।

## अवलोकन

यह प्रस्ताव I2P में UDP tracker के implementation के लिए है।

### Change History

I2P में UDP trackers के लिए एक प्रारंभिक प्रस्ताव हमारे [bittorrent spec page](/docs/applications/bittorrent/) पर मई 2014 में पोस्ट किया गया था; यह हमारी औपचारिक प्रस्ताव प्रक्रिया से पहले था, और इसे कभी लागू नहीं किया गया। यह प्रस्ताव 2022 की शुरुआत में बनाया गया था और 2014 संस्करण को सरल बनाता है।

चूंकि यह प्रस्ताव repliable datagrams पर निर्भर करता है, इसे तब रोक दिया गया था जब हमने 2023 की शुरुआत में [Datagram2 proposal](/proposals/163-datagram2/) पर काम करना शुरू किया था। वह प्रस्ताव अप्रैल 2025 में स्वीकृत हुआ था।

इस प्रस्ताव के 2023 संस्करण में दो मोड निर्दिष्ट थे, "compatibility" और "fast"। आगे के विश्लेषण से पता चला कि fast मोड असुरक्षित होगा, और बड़ी संख्या में torrents वाले clients के लिए भी अक्षम होगा। इसके अलावा, BiglyBT ने compatibility मोड के लिए प्राथमिकता दर्शाई। यह मोड मानक [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) का समर्थन करने वाले किसी भी tracker या client के लिए implement करना आसान होगा।

जबकि compatibility mode को client साइड पर शुरू से implement करना अधिक जटिल है, हमारे पास इसके लिए प्रारंभिक कोड है जो 2023 में शुरू किया गया था।

इसलिए, यहाँ मौजूदा संस्करण को fast mode को हटाने के लिए और भी सरल बनाया गया है, और "compatibility" शब्द को हटा दिया गया है। मौजूदा संस्करण नए Datagram2 format पर स्विच करता है, और UDP announce extension protocol [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) के संदर्भ जोड़ता है।

इसके अलावा, connect response में एक connection ID lifetime field जोड़ा गया है, ताकि इस protocol की efficiency gains को बढ़ाया जा सके।

## Motivation

जैसे-जैसे सामान्य उपयोगकर्ता आधार और विशेष रूप से bittorrent उपयोगकर्ताओं की संख्या बढ़ती जा रही है, हमें trackers और announces को अधिक कुशल बनाना होगा ताकि trackers अभिभूत न हो जाएं।

Bittorrent ने 2008 में BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) में UDP tracker का प्रस्ताव दिया था, और अब clearnet पर अधिकांश tracker केवल UDP-आधारित हैं।

डेटाग्राम बनाम स्ट्रीमिंग प्रोटोकॉल की बैंडविड्थ बचत की गणना करना कठिन है। एक repliable request लगभग स्ट्रीमिंग SYN के समान आकार का होता है, लेकिन payload लगभग 500 bytes छोटा होता है क्योंकि HTTP GET में एक विशाल 600 byte URL parameter string होती है। Raw reply स्ट्रीमिंग SYN ACK की तुलना में बहुत छोटा होता है, जो tracker के outbound traffic के लिए महत्वपूर्ण कमी प्रदान करता है।

इसके अतिरिक्त, implementation-specific मेमोरी में कमी होनी चाहिए, क्योंकि datagrams को streaming connection की तुलना में बहुत कम in-memory state की आवश्यकता होती है।

Post-Quantum encryption और signatures जैसा कि [/proposals/169-pq-crypto/](/proposals/169-pq-crypto/) में परिकल्पित है, encrypted और signed structures का overhead काफी बढ़ाएंगे, जिसमें destinations, leasesets, streaming SYN और SYN ACK शामिल हैं। I2P में PQ crypto को अपनाने से पहले जहाँ संभव हो वहाँ इस overhead को कम करना महत्वपूर्ण है।

## प्रेरणा

यह प्रस्ताव repliable datagram2, repliable datagram3, और raw datagrams का उपयोग करता है, जैसा कि [/docs/api/datagrams/](/docs/api/datagrams/) में परिभाषित है। Datagram2 और Datagram3 repliable datagrams के नए रूप हैं, जो Proposal 163 [/proposals/163-datagram2/](/proposals/163-datagram2/) में परिभाषित हैं। Datagram2 replay प्रतिरोध और offline signature समर्थन जोड़ता है। Datagram3 पुराने datagram format से छोटा है, लेकिन authentication के बिना।

### BEP 15

संदर्भ के लिए, [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) में परिभाषित message flow निम्नलिखित है:

```
Client                        Tracker
    Connect Req. ------------->
      <-------------- Connect Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
```
कनेक्ट फेज IP address spoofing को रोकने के लिए आवश्यक है। tracker एक connection ID रिटर्न करता है जिसका उपयोग client बाद की announces में करता है। यह connection ID client में डिफॉल्ट रूप से एक मिनट में expire हो जाता है, और tracker में दो मिनट में।

I2P मौजूदा UDP-सक्षम client code bases में अपनाने में आसानी के लिए BEP 15 के समान message flow का उपयोग करेगा: दक्षता के लिए, और नीचे चर्चित सुरक्षा कारणों से:

```
Client                        Tracker
    Connect Req. ------------->       (Repliable Datagram2)
      <-------------- Connect Resp.   (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
             ...
```
यह streaming (TCP) announces की तुलना में संभावित रूप से एक बड़ी bandwidth बचत प्रदान करता है। जबकि Datagram2 का आकार streaming SYN के लगभग बराबर है, raw response streaming SYN ACK की तुलना में काफी छोटा है। बाद के requests में Datagram3 का उपयोग होता है, और बाद के responses raw होते हैं।

announce अनुरोध Datagram3 होते हैं ताकि tracker को connection ID से announce destination या hash के बड़े mapping table को maintain करने की आवश्यकता न हो। इसके बजाय, tracker sender hash, वर्तमान timestamp (किसी interval के आधार पर), और एक secret value से cryptographically connection ID generate कर सकता है। जब कोई announce अनुरोध प्राप्त होता है, तो tracker connection ID को validate करता है, और फिर Datagram3 sender hash को send target के रूप में उपयोग करता है।

### परिवर्तन इतिहास

एक integrated application (router और client एक process में, उदाहरण के लिए i2psnark, और ZzzOT Java plugin) के लिए, या एक I2CP-based application (उदाहरण के लिए BiglyBT) के लिए, streaming और datagram traffic को अलग-अलग implement और route करना सीधा होना चाहिए। ZzzOT और i2psnark से अपेक्षा की जाती है कि वे इस proposal को implement करने वाले पहले tracker और client होंगे।

गैर-एकीकृत tracker और client पर नीचे चर्चा की गई है।

#### Trackers

चार ज्ञात I2P tracker implementations हैं:

- zzzot, एक integrated Java router plugin, जो opentracker.dg2.i2p और कई अन्य स्थानों पर चल रहा है
- tracker2.postman.i2p, जो संभवतः Java router और HTTP Server tunnel के पीछे चल रहा है
- पुराना C opentracker, जिसे zzz द्वारा port किया गया, UDP support को comment out करके
- नया C opentracker, जिसे r4sas द्वारा port किया गया, opentracker.r4sas.i2p और संभवतः अन्य स्थानों पर चल रहा है,
  जो संभवतः i2pd router और HTTP Server tunnel के पीछे चल रहा है

एक external tracker application के लिए जो वर्तमान में announce requests प्राप्त करने के लिए HTTP server tunnel का उपयोग करती है, implementation काफी कठिन हो सकती है। एक विशेषीकृत tunnel विकसित की जा सकती है जो datagrams को local HTTP requests/responses में translate करे। या, एक विशेषीकृत tunnel डिज़ाइन की जा सकती है जो HTTP requests और datagrams दोनों को handle करे और datagrams को external process को forward करे। ये design decisions विशिष्ट router और tracker implementations पर बहुत अधिक निर्भर करेंगे, और इस proposal के scope के बाहर हैं।

#### Clients

बाहरी SAM-आधारित torrent clients जैसे qbittorrent और अन्य libtorrent-आधारित clients को [SAM v3.3](/docs/api/samv3/) की आवश्यकता होगी जो i2pd द्वारा समर्थित नहीं है। यह DHT support के लिए भी आवश्यक है, और इतना जटिल है कि किसी भी ज्ञात SAM torrent client ने इसे implement नहीं किया है। इस proposal का कोई SAM-आधारित implementation जल्द ही अपेक्षित नहीं है।

### Connection Lifetime

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) निर्दिष्ट करता है कि connection ID client में एक मिनट में expire हो जाता है, और tracker में दो मिनट में। यह configurable नहीं है। यह संभावित दक्षता लाभों को सीमित करता है, जब तक कि clients batched announces नहीं करते कि वे सभी को एक मिनट की window के भीतर कर सकें। i2psnark वर्तमान में announces को batch नहीं करता; यह उन्हें फैलाता है, traffic के bursts से बचने के लिए। Power users की रिपोर्ट है कि वे एक साथ हजारों torrents चला रहे हैं, और उतनी सारी announces को एक मिनट में burst करना realistic नहीं है।

यहाँ, हम connect response को extend करने का प्रस्ताव रखते हैं ताकि एक optional connection lifetime field जोड़ा जा सके। default, यदि मौजूद नहीं है, तो एक मिनट है। अन्यथा, seconds में निर्दिष्ट lifetime का उपयोग client द्वारा किया जाएगा, और tracker connection ID को एक मिनट और बनाए रखेगा।

### Compatibility with BEP 15

यह डिज़ाइन [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) के साथ यथासंभव संगतता बनाए रखता है ताकि मौजूदा clients और trackers में आवश्यक परिवर्तनों को सीमित किया जा सके।

एकमात्र आवश्यक परिवर्तन announce response में peer info का format है। Connect response में lifetime field का जोड़ना आवश्यक नहीं है लेकिन दक्षता के लिए इसकी दृढ़ता से सिफारिश की जाती है, जैसा कि ऊपर समझाया गया है।

### BEP 15

एक UDP announce प्रोटोकॉल का एक महत्वपूर्ण लक्ष्य address spoofing को रोकना है। क्लाइंट को वास्तव में मौजूद होना चाहिए और एक वास्तविक leaseset को bundle करना चाहिए। Connect Response प्राप्त करने के लिए इसके पास inbound tunnels होने चाहिए। ये tunnels zero-hop हो सकते हैं और तुरंत बनाए जा सकते हैं, लेकिन इससे creator का पता चल जाएगा। यह प्रोटोकॉल उस लक्ष्य को पूरा करता है।

### Tracker/Client समर्थन

- यह प्रस्ताव blinded destinations का समर्थन नहीं करता,
  लेकिन इसे ऐसा करने के लिए विस्तारित किया जा सकता है। नीचे देखें।

## डिज़ाइन

### Protocols and Ports

Repliable Datagram2 I2CP protocol 19 का उपयोग करता है; repliable Datagram3 I2CP protocol 20 का उपयोग करता है; raw datagrams I2CP protocol 18 का उपयोग करते हैं। Requests Datagram2 या Datagram3 हो सकती हैं। Responses हमेशा raw होती हैं। I2CP protocol 17 का उपयोग करने वाला पुराना repliable datagram ("Datagram1") format requests या replies के लिए उपयोग नहीं किया जाना चाहिए; यदि ये request/reply ports पर प्राप्त हों तो इन्हें drop करना चाहिए। ध्यान दें कि Datagram1 protocol 17 अभी भी DHT protocol के लिए उपयोग किया जाता है।

अनुरोध announce URL से I2CP "to port" का उपयोग करते हैं; नीचे देखें। अनुरोध "from port" क्लाइंट द्वारा चुना जाता है, लेकिन यह शून्य नहीं होना चाहिए, और DHT द्वारा उपयोग किए जाने वाले पोर्ट से अलग पोर्ट होना चाहिए, ताकि responses को आसानी से वर्गीकृत किया जा सके। Trackers को गलत पोर्ट पर प्राप्त अनुरोधों को अस्वीकार करना चाहिए।

Responses अनुरोध से I2CP "to port" का उपयोग करते हैं। अनुरोध का "from port" अनुरोध के "to port" से आता है।

### Announce URL

announce URL प्रारूप [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) में निर्दिष्ट नहीं है, लेकिन clearnet की तरह, UDP announce URL "udp://host:port/path" के रूप में होते हैं। path को नजरअंदाज किया जाता है और यह खाली हो सकता है, लेकिन clearnet पर यह आमतौर पर "/announce" होता है। :port हिस्सा हमेशा मौजूद होना चाहिए, हालांकि, यदि ":port" हिस्सा छोड़ा गया है, तो 6969 के default I2CP port का उपयोग करें, क्योंकि clearnet पर यह सामान्य port है। cgi parameters &a=b&c=d भी जोड़े जा सकते हैं, उन्हें प्रोसेस किया जा सकता है और announce request में प्रदान किया जा सकता है, [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) देखें। यदि कोई parameters या path नहीं हैं, तो trailing / को भी छोड़ा जा सकता है, जैसा कि [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) में निहित है।

### कनेक्शन जीवनकाल

सभी values network byte order (big endian) में भेजे जाते हैं। packets के किसी निश्चित size के होने की उम्मीद न करें। भविष्य के extensions packets के size को बढ़ा सकते हैं।

#### Connect Request

Client से tracker तक। 16 bytes। Must be repliable Datagram2। [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) के समान। कोई बदलाव नहीं।

```
Offset  Size            Name            Value
  0       64-bit integer  protocol_id     0x41727101980 // magic constant
  8       32-bit integer  action          0 // connect
  12      32-bit integer  transaction_id
```
#### Connect Response

Tracker से client तक। 16 या 18 bytes। Raw होना चाहिए। [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) के समान है सिवाय नीचे दिए गए नोट्स के।

```
Offset  Size            Name            Value
  0       32-bit integer  action          0 // connect
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  lifetime        optional  // Change from BEP 15
```
प्रतिक्रिया को I2CP "to port" पर भेजा जाना चाहिए जो अनुरोध "from port" के रूप में प्राप्त हुआ था।

lifetime फ़ील्ड वैकल्पिक है और connection_id client lifetime को सेकंड में दर्शाता है। डिफ़ॉल्ट 60 है, और यदि निर्दिष्ट किया गया है तो न्यूनतम 60 है। अधिकतम 65535 या लगभग 18 घंटे है। tracker को client lifetime से 60 सेकंड अधिक के लिए connection_id को बनाए रखना चाहिए।

#### Announce Request

Client से tracker तक। न्यूनतम 98 bytes। Repliable Datagram3 होना चाहिए। [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) के समान सिवाय नीचे दिए गए नोट्स के।

connection_id वही है जो connect response में प्राप्त हुआ था।

```
Offset  Size            Name            Value
  0       64-bit integer  connection_id
  8       32-bit integer  action          1     // announce
  12      32-bit integer  transaction_id
  16      20-byte string  info_hash
  36      20-byte string  peer_id
  56      64-bit integer  downloaded
  64      64-bit integer  left
  72      64-bit integer  uploaded
  80      32-bit integer  event           0     // 0: none; 1: completed; 2: started; 3: stopped
  84      32-bit integer  IP address      0     // default
  88      32-bit integer  key
  92      32-bit integer  num_want        -1    // default
  96      16-bit integer  port
  98      varies          options     optional  // As specified in BEP 41
```
[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) से परिवर्तन:

- key को नजरअंदाज किया जाता है
- port को संभवतः नजरअंदाज किया जाता है
- options अनुभाग, यदि मौजूद है, तो [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) में परिभाषित के अनुसार है

प्रतिक्रिया को I2CP "to port" पर भेजा जाना चाहिए जो अनुरोध "from port" के रूप में प्राप्त हुआ था। announce अनुरोध के port का उपयोग न करें।

#### Announce Response

Tracker से client तक। न्यूनतम 20 bytes। Raw होना चाहिए। [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) के समान सिवाय नीचे दिए गए अपवादों के।

```
Offset  Size            Name            Value
  0           32-bit integer  action          1 // announce
  4           32-bit integer  transaction_id
  8           32-bit integer  interval
  12          32-bit integer  leechers
  16          32-bit integer  seeders
  20   32 * n 32-byte hash    binary hashes     // Change from BEP 15
  ...                                           // Change from BEP 15
```
[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) से बदलाव:

- IPv4+port के 6-byte या IPv6+port के 18-byte के बजाय, हम SHA-256 binary peer hashes के साथ 32-byte "compact responses" का एक गुणज वापस करते हैं। TCP compact responses की तरह, हम port शामिल नहीं करते हैं।

प्रतिक्रिया को उस I2CP "to port" पर भेजा जाना चाहिए जो अनुरोध के "from port" के रूप में प्राप्त हुआ था। announce अनुरोध के port का उपयोग न करें।

I2P datagrams का अधिकतम आकार लगभग 64 KB का बहुत बड़ा होता है; हालांकि, विश्वसनीय डिलीवरी के लिए, 4 KB से बड़े datagrams से बचना चाहिए। bandwidth की दक्षता के लिए, trackers को संभवतः अधिकतम peers को लगभग 50 तक सीमित करना चाहिए, जो विभिन्न layers पर overhead से पहले लगभग 1600 byte packet के अनुरूप होता है, और fragmentation के बाद two-tunnel-message payload सीमा के भीतर होना चाहिए।

BEP 15 की तरह, यहाँ भी peer addresses (BEP 15 के लिए IP/port, यहाँ hashes) की संख्या का कोई count शामिल नहीं है जो आगे आने वाले हैं। जबकि BEP 15 में इसका विचार नहीं किया गया था, सभी zeros का एक end-of-peers marker परिभाषित किया जा सकता है जो यह संकेत दे कि peer info पूरा है और कुछ extension data आगे आता है।

ताकि भविष्य में विस्तार संभव हो, clients को 32-byte all-zeros hash और उसके बाद आने वाले किसी भी data को ignore करना चाहिए। Trackers को all-zeros hash से announces को reject करना चाहिए, हालांकि वह hash पहले से ही Java routers द्वारा banned है।

#### Scrape

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) से scrape request/response इस प्रस्ताव द्वारा आवश्यक नहीं है, लेकिन यदि चाहें तो इसे लागू किया जा सकता है, कोई बदलाव की आवश्यकता नहीं है। क्लाइंट को पहले एक connection ID प्राप्त करना होगा। Scrape request हमेशा repliable Datagram3 होता है। Scrape response हमेशा raw होता है।

#### ट्रैकर्स

Tracker से client तक। न्यूनतम 8 bytes (यदि message खाली है)। Raw होना चाहिए। [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) के समान। कोई बदलाव नहीं।

```
Offset  Size            Name            Value
  0       32-bit integer  action          3 // error
  4       32-bit integer  transaction_id
  8       string          message
```
## Extensions

Extension bits या version field शामिल नहीं हैं। Clients और trackers को packets का एक निश्चित size होने की अपेक्षा नहीं करनी चाहिए। इस तरह से, compatibility को तोड़े बिना अतिरिक्त fields जोड़े जा सकते हैं। यदि आवश्यक हो तो [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) में परिभाषित extensions format की सिफारिश की जाती है।

connect response को एक वैकल्पिक connection ID lifetime जोड़ने के लिए संशोधित किया गया है।

यदि blinded destination समर्थन की आवश्यकता है, तो हम या तो announce request के अंत में blinded 35-byte address जोड़ सकते हैं, या responses में blinded hashes का अनुरोध कर सकते हैं, [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) format का उपयोग करके (paramters TBD)। blinded 35-byte peer addresses का सेट announce reply के अंत में जोड़ा जा सकता है, एक all-zeros 32-byte hash के बाद।

## Implementation guidelines

गैर-एकीकृत, गैर-I2CP clients और trackers के लिए चुनौतियों की चर्चा के लिए ऊपर design section देखें।

### BEP 15 के साथ संगतता

दिए गए tracker hostname के लिए, एक client को HTTP URLs की तुलना में UDP को प्राथमिकता देनी चाहिए, और दोनों को announce नहीं करना चाहिए।

मौजूदा BEP 15 समर्थन वाले क्लाइंट्स को केवल छोटे संशोधनों की आवश्यकता होनी चाहिए।

यदि कोई client DHT या अन्य datagram protocols का समर्थन करता है, तो उसे शायद request "from port" के रूप में एक अलग port चुनना चाहिए ताकि replies उस port पर वापस आएं और DHT messages के साथ मिश्रित न हों। Client केवल raw datagrams को replies के रूप में प्राप्त करता है। Trackers कभी भी client को repliable datagram2 नहीं भेजेंगे।

Default opentrackers की सूची वाले clients को UDP URLs जोड़ने के लिए सूची को update करना चाहिए जब ज्ञात opentrackers के UDP support करने की पुष्टि हो जाए।

क्लाइंट अनुरोधों के retransmission को implement कर सकते हैं या नहीं भी कर सकते हैं। Retransmissions, यदि implement किए गए हैं, तो कम से कम 15 सेकंड का प्रारंभिक timeout उपयोग करना चाहिए, और प्रत्येक retransmission के लिए timeout को दोगुना करना चाहिए (exponential backoff)।

क्लाइंट को error response प्राप्त होने के बाद back off करना चाहिए।

### सुरक्षा विश्लेषण

मौजूदा BEP 15 समर्थन वाले tracker में केवल छोटे संशोधनों की आवश्यकता होनी चाहिए। यह प्रस्ताव 2014 के प्रस्ताव से इस बात में भिन्न है कि tracker को समान port पर repliable datagram2 और datagram3 के reception का समर्थन करना चाहिए।

tracker संसाधन आवश्यकताओं को कम करने के लिए, इस protocol को इस तरह डिज़ाइन किया गया है कि tracker को बाद की validation के लिए client hashes से connection IDs की mappings store करने की कोई आवश्यकता न हो। यह संभव है क्योंकि announce request packet एक repliable Datagram3 packet है, इसलिए इसमें sender का hash होता है।

एक अनुशंसित implementation है:

- वर्तमान epoch को connection lifetime के resolution के साथ वर्तमान समय के रूप में परिभाषित करें,
  ``epoch = now / lifetime``।
- एक cryptographic hash function ``H(secret, clienthash, epoch)`` परिभाषित करें जो
  8 byte का output generate करता है।
- सभी connections के लिए उपयोग किए जाने वाले random constant secret को generate करें।
- Connect responses के लिए, ``connection_id = H(secret,  clienthash, epoch)`` generate करें
- Announce requests के लिए, वर्तमान epoch में received connection ID को validate करें यह verify करके
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``

## Migration

मौजूदा clients UDP announce URLs का समर्थन नहीं करते हैं और उन्हें ignore करते हैं।

मौजूदा tracker repliable या raw datagram के reception को support नहीं करते हैं, वे drop हो जाएंगे।

यह प्रस्ताव पूर्णतः वैकल्पिक है। न तो clients और न ही trackers को इसे किसी भी समय implement करना आवश्यक है।

## Rollout

पहले implementations ZzzOT और i2psnark में होने की उम्मीद है। इनका उपयोग इस प्रस्ताव के परीक्षण और सत्यापन के लिए किया जाएगा।

परीक्षण और सत्यापन पूरा होने के बाद अन्य implementations वांछित रूप में अनुसरण करेंगे।
