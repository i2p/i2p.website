---
title: "I2P पर Bittorrent"
description: "I2P पर BitTorrent clients और trackers के लिए प्रोटोकॉल विनिर्देश"
slug: "bittorrent"
lastUpdated: "2026-08"
accurateFor: "0.9.70"
---

I2P पर कई bittorrent clients और trackers उपलब्ध हैं। चूंकि I2P addressing IP और port के बजाय Destination का उपयोग करती है, I2P पर संचालन के लिए tracker और client software में मामूली बदलाव आवश्यक हैं। ये बदलाव नीचे निर्दिष्ट हैं। पुराने I2P clients और trackers के साथ संगतता के लिए दिशानिर्देशों को ध्यान से नोट करें।

यह पृष्ठ सभी clients और trackers के लिए सामान्य protocol विवरण निर्दिष्ट करता है। विशिष्ट clients और trackers अन्य अनूठी सुविधाओं या protocols को लागू कर सकते हैं।

हम I2P में client और tracker software के अतिरिक्त ports का स्वागत करते हैं।

---

## डेवलपर्स के लिए सामान्य मार्गदर्शन

अधिकांश गैर-Java bittorrent क्लाइंट I2P से [SAMv3](/docs/api/samv3/) के माध्यम से कनेक्ट होंगे। SAM sessions (या I2P के अंदर, tunnel pools या tunnels के समूह) लंबे समय तक चलने के लिए डिज़ाइन किए गए हैं। अधिकांश bittorrent क्लाइंट्स को केवल एक session की आवश्यकता होगी, जो स्टार्टअप पर बनाया जाता है और बाहर निकलने पर बंद हो जाता है। I2P, Tor से अलग है, जहां circuits तेज़ी से बनाए और त्यागे जा सकते हैं। यदि आप अपनी application को एक या दो से अधिक समानांतर sessions का उपयोग करने या उन्हें तेज़ी से बनाने और त्यागने के लिए डिज़ाइन करने से पहले सावधानी से सोचें और I2P developers से सलाह लें। Bittorrent क्लाइंट्स को हर कनेक्शन के लिए एक अनूठा session नहीं बनाना चाहिए। अपने क्लाइंट को announces और क्लाइंट कनेक्शन के लिए समान session का उपयोग करने के लिए डिज़ाइन करें।

साथ ही, कृपया सुनिश्चित करें कि आपकी client सेटिंग्स (और router सेटिंग्स के बारे में उपयोगकर्ताओं को दिशा-निर्देश, या router डिफ़ॉल्ट्स यदि आप एक router bundle करते हैं) का परिणाम यह होगा कि आपके उपयोगकर्ता नेटवर्क में जितने संसाधन उपभोग करते हैं उससे अधिक योगदान दें। I2P एक peer-to-peer नेटवर्क है, और यदि कोई लोकप्रिय एप्लिकेशन नेटवर्क को स्थायी congestion में धकेल देती है तो नेटवर्क जीवित नहीं रह सकता।

I2P outproxy के माध्यम से clearnet पर bittorrent के लिए सहायता प्रदान न करें क्योंकि यह संभवतः ब्लॉक हो जाएगा। मार्गदर्शन के लिए outproxy ऑपरेटरों से सलाह लें।

Java I2P और i2pd router implementations स्वतंत्र हैं और इनके व्यवहार, फीचर समर्थन, और डिफ़ॉल्ट सेटिंग्स में मामूली अंतर हैं। कृपया अपनी application को दोनों routers के नवीनतम संस्करण के साथ परीक्षण करें।

i2pd SAM डिफ़ॉल्ट रूप से सक्षम होता है; Java I2P SAM नहीं होता। अपने उपयोगकर्ताओं को निर्देश दें कि Java I2P में SAM कैसे सक्षम करें (router console में /configclients के माध्यम से), और/या यदि प्रारंभिक कनेक्शन विफल हो जाता है तो उपयोगकर्ता को एक अच्छा त्रुटि संदेश प्रदान करें, जैसे "सुनिश्चित करें कि I2P चल रहा है और SAM interface सक्षम है"।

Java I2P और i2pd router के पास tunnel quantities के लिए अलग-अलग defaults हैं। Java default 2 है और i2pd default 5 है। अधिकतर low- से medium-bandwidth और low- से medium-connection counts के लिए, 3 पर्याप्त है। Java I2P और i2pd router के साथ consistent performance पाने के लिए कृपया SESSION CREATE message में tunnel quantity specify करें।

I2P कई signature और encryption प्रकारों का समर्थन करता है। संगतता के लिए, I2P पुराने और अक्षम प्रकारों को डिफ़ॉल्ट के रूप में उपयोग करता है, इसलिए सभी clients को नए प्रकार निर्दिष्ट करने चाहिए।

यदि SAM का उपयोग कर रहे हैं, तो signature type को DEST GENERATE और SESSION CREATE (transient के लिए) commands में निर्दिष्ट किया जाता है। सभी clients को SIGNATURE_TYPE=7 (Ed25519) सेट करना चाहिए।

encryption type SAM SESSION CREATE command या i2cp options में निर्दिष्ट किया जाता है। कई encryption types की अनुमति है। कुछ trackers ECIES-X25519 को support करते हैं, कुछ ElGamal को support करते हैं, और कुछ दोनों को support करते हैं। Clients को i2cp.leaseSetEncType=4,0 (ECIES-X25519 और ElGamal के लिए) set करना चाहिए ताकि वे दोनों से connect कर सकें।

DHT समर्थन के लिए SAMv3.3 PRIMARY और SUBSESSIONS की आवश्यकता होती है TCP और UDP के लिए समान session पर। इसके लिए client side पर काफी विकास कार्य की आवश्यकता होगी, जब तक कि client Java में नहीं लिखा गया हो। i2pd वर्तमान में SAMv3.3 का समर्थन नहीं करता है। libtorrent वर्तमान में SAMv3.3 का समर्थन नहीं करता है।

DHT समर्थन के बिना, आप चाहेंगे कि magnet links काम करें इसलिए ज्ञात open trackers की एक कॉन्फ़िगरेबल सूची में स्वचालित रूप से घोषणा करें। वर्तमान में उपलब्ध open trackers की जानकारी के लिए I2P उपयोगकर्ताओं से सलाह लें और अपनी defaults को अप-टू-डेट रखें। i2p_pex extension का समर्थन करना भी DHT समर्थन की कमी को कम करने में मदद करेगा।

डेवलपर्स के लिए यह सुनिश्चित करने के अधिक मार्गदर्शन के लिए कि आपका एप्लिकेशन केवल उन संसाधनों का उपयोग करता है जिनकी इसे आवश्यकता है, कृपया [SAMv3 specification](/docs/api/samv3/) और [I2P को अपने एप्लिकेशन के साथ bundle करने के लिए हमारी गाइड](/docs/applications/embedding/) देखें। अधिक सहायता के लिए I2P या i2pd डेवलपर्स से संपर्क करें।

---

## घोषणाएं

क्लाइंट्स आमतौर पर पुराने trackers के साथ संगतता के लिए announce में एक फेक port=6881 parameter शामिल करते हैं। Trackers port parameter को नजरअंदाज कर सकते हैं, और इसकी आवश्यकता नहीं होनी चाहिए।

ip parameter क्लाइंट के [Destination](/docs/specs/common-structures/#struct_Destination) का base 64 है, जो I2P Base 64 alphabet [A-Z][a-z][0-9]-~ का उपयोग करता है। [Destinations](/docs/specs/common-structures/#struct_Destination) 387+ bytes के होते हैं, इसलिए Base 64 516+ bytes का होता है। क्लाइंट आमतौर पर पुराने trackers के साथ compatibility के लिए Base 64 Destination में ".i2p" जोड़ते हैं। Trackers को ".i2p" जोड़ना अनिवार्य नहीं करना चाहिए।

अन्य पैरामीटर मानक bittorrent के समान हैं।

क्लाइंट्स के लिए वर्तमान Destinations 387 या अधिक बाइट्स के हैं (Base 64 encoding में 516 या अधिक)। अभी के लिए मानने योग्य उचित अधिकतम 475 बाइट्स है। चूंकि tracker को compact responses देने के लिए Base64 को decode करना होता है (नीचे देखें), इसलिए tracker को शायद announce के समय Base64 को decode करना चाहिए और गलत Base64 को reject करना चाहिए।

डिफ़ॉल्ट response type non-compact है। Clients compact=1 parameter के साथ compact response का अनुरोध कर सकते हैं। एक tracker अनुरोध किए जाने पर compact response वापस कर सकता है, लेकिन यह आवश्यक नहीं है। नोट: सभी लोकप्रिय trackers अब compact responses का समर्थन करते हैं और कम से कम एक को announce में compact=1 की आवश्यकता होती है। सभी clients को compact responses का अनुरोध करना चाहिए और उनका समर्थन करना चाहिए।

नए I2P clients के डेवलपर्स को दृढ़ता से प्रोत्साहित किया जाता है कि वे port 4444 पर HTTP client proxy के बजाय अपने स्वयं के tunnel पर announces को implement करें। ऐसा करना न केवल अधिक कुशल है बल्कि यह tracker द्वारा destination enforcement की अनुमति भी देता है (नीचे देखें)।

UDP announces के लिए specification को 2025-06 में अंतिम रूप दिया गया था। विभिन्न I2P clients और trackers में support 2025 के बाद में धीरे-धीरे आएगा। अतिरिक्त जानकारी के लिए नीचे देखें।

---

## गैर-कॉम्पैक्ट ट्रैकर प्रतिक्रियाएं

नोट: अप्रचलित। सभी लोकप्रिय tracker अब compact responses का समर्थन करते हैं और कम से कम एक को announce में compact=1 की आवश्यकता होती है। सभी clients को compact responses का अनुरोध करना और समर्थन करना चाहिए।

Non-compact response बिल्कुल standard bittorrent की तरह है, एक I2P "ip" के साथ। यह एक लंबी base64-encoded "DNS string" है, संभवतः ".i2p" suffix के साथ।

Tracker आमतौर पर पुराने client के साथ compatibility के लिए एक नकली port key शामिल करते हैं, या announce से port का उपयोग करते हैं। Client को port parameter को ignore करना चाहिए, और इसकी आवश्यकता नहीं होनी चाहिए।

ip key का मान client के [Destination](/docs/specs/common-structures/#struct_Destination) का base 64 है, जैसा कि ऊपर वर्णित है। Trackers आमतौर पर Base 64 Destination के साथ ".i2p" जोड़ते हैं यदि यह announce ip में नहीं था, पुराने clients के साथ संगतता के लिए। Clients को responses में जोड़े गए ".i2p" की आवश्यकता नहीं होनी चाहिए।

अन्य response keys और values मानक bittorrent के समान हैं।

---

## कॉम्पैक्ट ट्रैकर प्रतिक्रियाएं

कॉम्पैक्ट response में, "peers" dictionary key का value एक single byte string है, जिसकी लंबाई 32 bytes का गुणांक है। इस string में peers के binary [Destinations](/docs/specs/common-structures/#struct_Destination) के concatenated [32-byte SHA-256 Hashes](/docs/specs/common-structures/#type_Hash) होते हैं। यह hash tracker द्वारा compute किया जाना चाहिए, जब तक कि destination enforcement (नीचे देखें) का उपयोग न किया जा रहा हो, जिस स्थिति में X-I2P-DestHash या X-I2P-DestB32 HTTP headers में दिया गया hash को binary में convert करके store किया जा सकता है। peers key अनुपस्थित हो सकती है, या peers value zero-length हो सकता है।

जबकि compact response समर्थन clients और trackers दोनों के लिए वैकल्पिक है, इसकी अत्यधिक अनुशंसा की जाती है क्योंकि यह सामान्य response size को 90% से अधिक कम कर देता है।

---

## गंतव्य प्रवर्तन

कुछ I2P bittorrent clients अपनी tunnels के माध्यम से announce करते हैं, लेकिन सभी नहीं। Trackers spoofing को रोकने के लिए इसकी आवश्यकता रख सकते हैं, और I2PTunnel HTTP Server tunnel द्वारा जोड़े गए HTTP headers का उपयोग करके client के [Destination](/docs/specs/common-structures/#struct_Destination) को verify कर सकते हैं। Headers हैं X-I2P-DestHash, X-I2P-DestB64, और X-I2P-DestB32, जो समान जानकारी के लिए अलग-अलग formats हैं। इन headers को client द्वारा spoof नहीं किया जा सकता। Destinations को enforce करने वाले tracker को ip announce parameter की बिल्कुल आवश्यकता नहीं है।

जैसे कि कई clients अपनी tunnel के बजाय HTTP proxy का उपयोग announces के लिए करते हैं, destination enforcement उन clients के उपयोग को तब तक रोकेगा जब तक कि वे clients अपनी tunnel के माध्यम से announce करने के लिए convert नहीं हो जाते।

दुर्भाग्यवश, जैसे-जैसे नेटवर्क बढ़ता है, वैसे-वैसे दुर्भावना की मात्रा भी बढ़ेगी, इसलिए हम उम्मीद करते हैं कि सभी tracker अंततः destinations को लागू करेंगे। tracker और client दोनों डेवलपर्स को इसकी अपेक्षा करनी चाहिए।

---

## होस्ट नाम घोषित करें

टॉरेंट फाइलों में announce URL host names आमतौर पर [I2P naming standards](/docs/overview/naming/) का पालन करते हैं। address books से host names और ".b32.i2p" Base 32 hostnames के अलावा, पूर्ण Base 64 Destination (".i2p" के साथ या बिना) को भी समर्थित होना चाहिए। Non-open trackers को इनमें से किसी भी प्रारूप में अपने host name को पहचानना चाहिए।

गुमनामी बनाए रखने के लिए, clients को आम तौर पर torrent files में non-I2P announce URLs को नजरअंदाज करना चाहिए।

---

## क्लाइंट कनेक्शन

Client-to-client कनेक्शन TCP पर standard protocol का उपयोग करते हैं। वर्तमान में कोई ज्ञात I2P clients नहीं हैं जो uTP communication का समर्थन करते हों।

I2P पतों के लिए 387+ बाइट [Destinations](/docs/specs/common-structures/#struct_Destination) का उपयोग करता है, जैसा कि ऊपर समझाया गया है।

यदि client के पास केवल destination का hash है (जैसे कि compact response या PEX से), तो उसे Base 32 के साथ encode करके, ".b32.i2p" जोड़कर, और Naming Service से query करके lookup करना होगा, जो उपलब्ध होने पर पूरा Destination वापस करेगी।

यदि client के पास किसी peer का पूरा Destination है जो उसे एक non-compact response में मिला है, तो उसे connection setup में इसे सीधे उपयोग करना चाहिए। Destination को वापस Base 32 hash में convert करके lookup के लिए उपयोग न करें, यह काफी अक्षम है।

---

## क्रॉस-नेटवर्क रोकथाम

गुमनामी बनाए रखने के लिए, I2P bittorrent क्लाइंट आमतौर पर गैर-I2P announces या peer connections का समर्थन नहीं करते हैं। I2P HTTP outproxies अक्सर announces को ब्लॉक कर देते हैं। bittorrent ट्रैफिक का समर्थन करने वाले कोई ज्ञात SOCKS outproxies नहीं हैं।

HTTP inproxy के माध्यम से गैर-I2P clients के उपयोग को रोकने के लिए, I2P trackers अक्सर उन accesses या announces को block कर देते हैं जिनमें X-Forwarded-For HTTP header होता है। Trackers को IPv4 या IPv6 IPs के साथ standard network announces को reject करना चाहिए, और उन्हें responses में deliver नहीं करना चाहिए।

---

## PEX

I2P PEX ut_pex पर आधारित है। चूंकि ut_pex का कोई औपचारिक विनिर्देश उपलब्ध नहीं दिखता, इसलिए सहायता के लिए libtorrent स्रोत की समीक्षा करना आवश्यक हो सकता है। यह एक extension message है, जो [extension handshake](http://www.bittorrent.org/beps/bep_0010.html) में "i2p_pex" के रूप में पहचाना जाता है। इसमें 3 keys तक के साथ एक bencoded dictionary होती है, "added", "added.f", और "dropped"। added और dropped values प्रत्येक एक single byte string हैं, जिनकी लंबाई 32 bytes का गुणज है। ये byte strings peers के binary [Destinations](/docs/specs/common-structures/#struct_Destination) के SHA-256 Hashes को जोड़कर बनाई गई हैं। यह वही प्रारूप है जो ऊपर निर्दिष्ट i2p compact response format में peers dictionary value का है। added.f value, यदि मौजूद है, तो ut_pex में समान है।

---

## DHT

DHT समर्थन i2psnark क्लाइंट में संस्करण 0.9.2 से शामिल है। [BEP 5](http://www.bittorrent.org/beps/bep_0005.html) से प्रारंभिक अंतर नीचे वर्णित हैं, और ये परिवर्तन के अधीन हैं। यदि आप DHT समर्थन के साथ एक क्लाइंट विकसित करना चाहते हैं तो I2P डेवलपर्स से संपर्क करें।

मानक DHT के विपरीत, I2P DHT options handshake में एक bit का उपयोग नहीं करता, या PORT message का। यह एक extension message के साथ विज्ञापित किया जाता है, जो [extension handshake](http://www.bittorrent.org/beps/bep_0010.html) में "i2p_dht" के रूप में पहचाना जाता है। इसमें दो keys के साथ एक bencoded dictionary होती है, "port" और "rport", दोनों integers हैं।

कॉम्पैक्ट नोड जानकारी में सूचीबद्ध UDP (datagram) पोर्ट का उपयोग repliable (signed) datagrams प्राप्त करने के लिए किया जाता है। इसका उपयोग queries के लिए किया जाता है, announces को छोड़कर। हम इसे "query port" कहते हैं। यह extension message से "port" value है। Queries [I2CP](/docs/specs/i2cp/) प्रोटोकॉल नंबर 17 का उपयोग करती हैं।

उस UDP port के अतिरिक्त, हम एक दूसरा datagram port उपयोग करते हैं जो query port + 1 के बराबर होता है। इसका उपयोग replies, errors, और announces के लिए unsigned (raw) datagrams प्राप्त करने के लिए किया जाता है। यह port बढ़ी हुई efficiency प्रदान करता है क्योंकि replies में query में भेजे गए tokens होते हैं, और उन्हें signed होने की आवश्यकता नहीं होती। हम इसे "response port" कहते हैं। यह extension message से "rport" value है। यह query port + 1 होना चाहिए। Responses और announces [I2CP](/docs/specs/i2cp/) protocol number 18 का उपयोग करते हैं।

Compact peer info 32 bytes (32 byte SHA256 Hash) का है 4 byte IP + 2 byte port के बजाय। कोई peer port नहीं है। एक response में, "values" key strings की एक list है, जिसमें प्रत्येक में एक single compact peer info होता है।

Compact node info 54 बाइट्स का है (20 बाइट Node ID + 32 बाइट SHA256 Hash + 2 बाइट port) बजाय 20 बाइट Node ID + 4 बाइट IP + 2 बाइट port के। एक response में, "nodes" key एक single byte string है जिसमें concatenated compact node info होती है।

सुरक्षित node ID आवश्यकता: विभिन्न DHT हमलों को और कठिन बनाने के लिए, Node ID के पहले 4 bytes को destination Hash के पहले 4 bytes से मेल खाना चाहिए, और Node ID के अगले दो bytes को destination hash के अगले दो bytes के साथ port के exclusive-OR किए गए परिणाम से मेल खाना चाहिए।

एक torrent फ़ाइल में, trackerless torrent dictionary "nodes" key TBD है। यह host string और port integer वाली lists की list के बजाय 32 byte binary strings (SHA256 Hashes) की एक list हो सकती है। विकल्प: concatenated hashes के साथ एक single byte string, या केवल strings की एक list।

---

## डेटाग्राम (UDP) ट्रैकर्स

I2P में UDP announces के लिए स्पेसिफिकेशन 2025-06 में अंतिम रूप दिया गया था। विभिन्न I2P clients और trackers में समर्थन 2025 में बाद में उपलब्ध होगा। [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) से अंतर [UDP announce specification](/docs/specs/udp-announces/) में प्रलेखित है। स्पेसिफिकेशन में [नए Datagram 2/3 formats](/docs/specs/datagrams/) के लिए समर्थन की भी आवश्यकता है।

---

## अतिरिक्त जानकारी

अनुमत फास्ट सेट की गणना के लिए एक प्रारंभिक विनिर्देश [प्रस्ताव 172](/proposals/172-bep6-allowed-fast) में दिया गया है।

---

## अतिरिक्त जानकारी

- I2P bittorrent मानकों पर आमतौर पर [zzz.i2p](http://zzz.i2p/) पर चर्चा की जाती है।
- वर्तमान tracker सॉफ्टवेयर क्षमताओं का चार्ट [वहाँ भी उपलब्ध है](http://zzz.i2p/files/trackers.html)।
- [I2P bittorrent FAQ](http://forum.i2p/viewtopic.php?t=2068)
- [I2P पर DHT चर्चा](http://zzz.i2p/topics/812)
