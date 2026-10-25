---
title: "I2PTunnel"
description: "I2P के साथ इंटरफेस करने और सेवाएं प्रदान करने के लिए उपकरण"
slug: "i2ptunnel"
aliases:
  - "/hi/i2ptunnel"
  - "/hi/i2ptunnel/"
  - "/hi/i2ptunnel_migration"
  - "/hi/i2ptunnel_migration/"
  - "/hi/i2ptunnel_services"
  - "/hi/i2ptunnel_services/"
lastUpdated: "2023-10"
accurateFor: "0.9.59"
---

## अवलोकन {#overview}

I2PTunnel एक उपकरण है जो I2P पर सेवाओं के साथ इंटरफेसिंग और प्रदान करने के लिए उपयोग होता है। I2PTunnel के destination को [hostname](/docs/overview/naming), [Base32](/docs/overview/naming#base32), या पूरी 516-byte destination key का उपयोग करके परिभाषित किया जा सकता है। एक स्थापित I2PTunnel आपकी client machine पर localhost:port के रूप में उपलब्ध होगा। यदि आप I2P network पर एक सेवा प्रदान करना चाहते हैं, तो आप बस उपयुक्त ip_address:port के लिए I2PTunnel बनाएं। सेवा के लिए एक संबंधित 516-byte destination key उत्पन्न होगी और यह पूरे I2P में उपलब्ध हो जाएगी। I2PTunnel प्रबंधन के लिए एक web interface [localhost:7657/i2ptunnel/](http://localhost:7657/i2ptunnel/) पर उपलब्ध है।

## डिफ़ॉल्ट सेवाएं {#default-services}

### Server Tunnels {#default-server-tunnels}

- **I2P Webserver** - एक tunnel जो Jetty webserver की ओर इंगित करता है जो
  [localhost:7658](http://localhost:7658) पर चलता है I2P पर सुविधाजनक और त्वरित hosting के लिए।
  document root है:
  - **Unix** - `$HOME/.i2p/eepsite/docroot`
  - **Windows** - `%LOCALAPPDATA%\I2P\I2P Site\docroot`, जो विस्तृत होता है: `C:\Users\**username**\AppData\Local\I2P\I2P Site\docroot`

### Client Tunnels {#default-client-tunnels}

- **I2P HTTP Proxy** - *localhost:4444* - एक HTTP proxy जो I2P और नियमित इंटरनेट को I2P के माध्यम से गुमनाम रूप से ब्राउज़ करने के लिए उपयोग किया जाता है। I2P के माध्यम से इंटरनेट ब्राउज़िंग "Outproxies:" विकल्प द्वारा निर्दिष्ट एक यादृच्छिक proxy का उपयोग करती है।
- **Irc2P** - *localhost:6668* - डिफ़ॉल्ट गुमनाम IRC नेटवर्क, Irc2P के लिए एक IRC tunnel।
- **gitssh.idk.i2p** - *localhost:7670* - प्रोजेक्ट Git रिपॉजिटरी के लिए SSH पहुंच
- **smtp.postman.i2p** - *localhost:7659* - hq.postman.i2p पर postman द्वारा प्रदान की गई एक SMTP सेवा
- **pop3.postman.i2p** - *localhost:7660* - hq.postman.i2p पर postman की संगत POP सेवा

## कॉन्फ़िगरेशन {#configuration}

[I2PTunnel कॉन्फ़िगरेशन](/docs/specs/configuration)

## क्लाइंट मोड {#client-modes}

### मानक {#client-modes-standard}

एक स्थानीय TCP पोर्ट खोलता है जो I2P के अंदर किसी गंतव्य पर सेवा (जैसे HTTP, FTP या SMTP) से जुड़ता है। tunnel कॉमा द्वारा अलग किए गए (", ") गंतव्यों की सूची से एक यादृच्छिक होस्ट पर निर्देशित होता है।

### HTTP {#client-mode-http}

एक HTTP-client tunnel। यह tunnel HTTP अनुरोध में URL द्वारा निर्दिष्ट गंतव्य से जुड़ता है। यदि कोई outproxy प्रदान किया गया है तो इंटरनेट पर proxying का समर्थन करता है। HTTP कनेक्शन से निम्नलिखित headers को हटा देता है:

- **Accept\*:** (not including "Accept" and "Accept-Encoding") क्योंकि ये ब्राउज़र के बीच बहुत भिन्न होते हैं और पहचानकर्ता के रूप में उपयोग हो सकते हैं।
- **Referer:**
- **Via:**
- **From:**

HTTP क्लाइंट proxy उपयोगकर्ता की सुरक्षा करने और बेहतर उपयोगकर्ता अनुभव प्रदान करने के लिए कई सेवाएं प्रदान करता है।

**Request header प्रसंस्करण:** - गोपनीयता-समस्याग्रस्त headers को हटाना - स्थानीय या दूरस्थ outproxy के लिए routing - Outproxy चयन, caching, और पहुंच ट्रैकिंग - Hostname से destination lookups - Host header को b32 में बदलना - पारदर्शी decompression के समर्थन को इंगित करने के लिए header जोड़ना - Force connection: close - RFC-अनुपालित proxy समर्थन - RFC-अनुपालित hop-by-hop header प्रसंस्करण और stripping - वैकल्पिक digest और बुनियादी username/password प्रमाणीकरण - वैकल्पिक outproxy digest और बुनियादी username/password प्रमाणीकरण - दक्षता के लिए सभी headers को पारित करने से पहले buffering - Jump server लिंक - Jump response प्रसंस्करण और forms (address helper) - Blinded b32 प्रसंस्करण और credential forms - मानक HTTP और HTTPS (CONNECT) requests का समर्थन

**Response header processing:** - Response को decompress करना है या नहीं इसकी जांच - Force connection: close - RFC-compliant hop-by-hop header processing और stripping - दक्षता के लिए सभी headers को pass करने से पहले buffering

**HTTP error responses:** - कई सामान्य और असामान्य errors के लिए, ताकि उपयोगकर्ता को पता चल सके कि क्या हुआ - विभिन्न errors के लिए 20 से अधिक unique translated, styled, और formatted error pages - forms, CSS, images, और errors को serve करने के लिए internal web server

#### पारदर्शी प्रतिक्रिया संपीड़न {#transparent-response-compression}

i2ptunnel response compression का अनुरोध HTTP header के साथ किया जाता है:

- **X-Accept-Encoding:** x-i2p-gzip;q=1.0, identity;q=0.5, deflate;q=0, gzip;q=0, *;q=0

सर्वर साइड वेब सर्वर को अनुरोध भेजने से पहले इस hop-by-hop header को हटा देता है। सभी q values के साथ विस्तृत header आवश्यक नहीं है; सर्वर को केवल header में कहीं भी "x-i2p-gzip" की तलाश करनी चाहिए।

सर्वर साइड यह निर्धारित करता है कि webserver से प्राप्त headers के आधार पर response को compress करना है या नहीं, जिसमें Content-Type, Content-Length, और Content-Encoding शामिल हैं, यह आकलन करने के लिए कि response compressible है और अतिरिक्त CPU की आवश्यकता के लायक है। यदि सर्वर साइड response को compress करता है, तो यह निम्नलिखित HTTP header जोड़ता है:

- **Content-Encoding:** x-i2p-gzip

यदि यह header response में मौजूद है, तो HTTP client proxy इसे transparently decompress कर देता है। Client side इस header को हटा देता है और browser को response भेजने से पहले gunzip करता है। ध्यान दें कि हमारे पास अभी भी I2CP layer पर underlying gzip compression है, जो तब भी प्रभावी है जब response HTTP layer पर compressed नहीं है।

यह डिज़ाइन और वर्तमान कार्यान्वयन RFC 2616 का कई तरीकों से उल्लंघन करता है:

- X-Accept-Encoding एक मानक header नहीं है
- प्रति-hop dechunk/chunk नहीं करता; यह chunking को end-to-end पास करता है
- Transfer-Encoding header को end-to-end पास करता है
- प्रति-hop encoding निर्दिष्ट करने के लिए Transfer-Encoding नहीं, बल्कि Content-Encoding का उपयोग करता है
- जब Content-Encoding सेट हो तो x-i2p gzipping को प्रतिबंधित करता है (लेकिन हम शायद वैसे भी ऐसा नहीं करना चाहते)
- Server side server-sent chunking को gzip करता है, dechunk-gzip-rechunk और dechunk-gunzip-rechunk करने के बजाय
- Gzipped content को बाद में chunk नहीं किया जाता। RFC 2616 के अनुसार "identity" के अलावा सभी Transfer-Encoding को chunk किया जाना चाहिए।
- क्योंकि gzip के बाहर (के बाद) कोई chunking नहीं है, डेटा के अंत को खोजना अधिक कठिन है, जिससे keepalive का कोई भी implementation कठिन हो जाता है।
- RFC 2616 कहता है कि यदि Transfer-Encoding मौजूद है तो Content-Length नहीं भेजा जाना चाहिए, लेकिन हम भेजते हैं। Spec कहता है कि यदि Transfer-Encoding मौजूद है तो Content-Length को ignore करें, जो browsers करते हैं, इसलिए यह हमारे लिए काम करता है।

पिछड़े-संगत तरीके से मानक-अनुपालित hop-by-hop compression को लागू करने के लिए बदलाव आगे के अध्ययन का विषय है। dechunk-gzip-rechunk में किसी भी बदलाव के लिए एक नए encoding प्रकार की आवश्यकता होगी, शायद x-i2p-gzchunked। यह Transfer-Encoding: gzip के समान होगा, लेकिन संगतता कारणों से इसे अलग तरीके से संकेत देना होगा। किसी भी बदलाव के लिए एक औपचारिक प्रस्ताव की आवश्यकता होगी।

#### पारदर्शी अनुरोध संपीड़न {#transparent-request-compression}

समर्थित नहीं है, हालांकि POST को फायदा होगा। ध्यान दें कि हमारे पास अभी भी I2CP layer पर अंतर्निहित gzip compression है।

#### स्थायित्व {#persistence}

क्लाइंट और सर्वर proxies वर्तमान में तीनों hops (ब्राउज़र socket, I2P socket, सर्वर socket) पर RFC 2616 HTTP persistent sockets का समर्थन नहीं करते हैं। Connection: close headers हर hop पर inject किए जाते हैं। persistence को implement करने के लिए बदलावों की जांच की जा रही है। ये बदलाव standards-compliant और backwards-compatible होने चाहिए, और इसके लिए किसी औपचारिक प्रस्ताव की आवश्यकता नहीं होगी।

#### पाइपलाइनिंग {#pipelining}

क्लाइंट और सर्वर proxies वर्तमान में RFC 2616 HTTP pipelining का समर्थन नहीं करते हैं और ऐसा करने की कोई योजना नहीं है। आधुनिक ब्राउज़र proxies के माध्यम से pipelining का समर्थन नहीं करते हैं क्योंकि अधिकांश proxies इसे सही तरीके से implement नहीं कर सकते।

#### संगतता {#compatibility}

Proxy implementations अन्य implementations के साथ दूसरी तरफ सही तरीके से काम करने चाहिए। Client proxies को server side पर HTTP-aware server proxy (यानी एक standard tunnel) के बिना काम करना चाहिए। सभी implementations x-i2p-gzip को support नहीं करते हैं।

#### User Agent {#user-agent}

यह इस पर निर्भर करता है कि tunnel एक outproxy का उपयोग कर रहा है या नहीं, यह निम्नलिखित User-Agent को जोड़ेगा:

- *Outproxy:* **User-Agent:** Windows पर हाल की Firefox रिलीज़ से user agent का उपयोग करता है
- *Internal I2P use:* **User-Agent:** MYOB/6.66 (AN/ON)

### IRC क्लाइंट {#client-mode-irc}

कॉमा से अलग की गई (", ") गंतव्य सूची द्वारा निर्दिष्ट एक यादृच्छिक IRC सर्वर से कनेक्शन बनाता है। गुमनामी की चिंताओं के कारण केवल IRC कमांड के एक श्वेतसूची उपसमुच्चय की अनुमति है।

निम्नलिखित अनुमति सूची IRC सर्वर से IRC क्लाइंट तक आने वाले commands के लिए है।

**अनुमति सूची:** - AUTHENTICATE - CAP - ERROR - H - JOIN - KICK - MODE - NICK - PART - PING - PROTOCTL - QUIT - TOPIC - WALLOPS

IRC client से IRC server तक जाने वाले commands के लिए भी एक allow list है। IRC administrative commands की संख्या के कारण यह काफी बड़ी है। विवरण के लिए IRCFilter.java source देखें।

आउटबाउंड फ़िल्टर पहचान की जानकारी को हटाने के लिए निम्नलिखित commands को भी संशोधित करता है: - NOTICE - PART - PING - PRIVMSG - QUIT - USER

### SOCKS 4/4a/5 {#client-mode-socks}

I2P router को SOCKS proxy के रूप में उपयोग करने में सक्षम बनाता है।

### SOCKS IRC {#client-mode-socks-irc}

I2P router को SOCKS proxy के रूप में उपयोग करने की सुविधा देता है जिसमें [IRC](#client-mode-irc) client mode द्वारा निर्दिष्ट command whitelist होती है।

### CONNECT {#client-mode-connect}

एक HTTP tunnel बनाता है और HTTP request method "CONNECT" का उपयोग करके एक TCP tunnel निर्माण करता है जो आमतौर पर SSL और HTTPS के लिए उपयोग किया जाता है।

### Streamr {#client-mode-streamr}

एक UDP-server बनाता है जो Streamr client I2PTunnel से जुड़ा होता है। streamr client tunnel एक streamr server tunnel की सदस्यता लेगा।

![Streamr diagram](/images/I2PTunnel-streamr.png)

## Server Modes {#server-modes}

### मानक {#server-mode-standard}

एक स्थानीय ip:port के लिए एक गंतव्य बनाता है जिसमें एक खुला TCP पोर्ट होता है।

### HTTP {#server-mode-http}

स्थानीय HTTP सर्वर ip:port के लिए एक destination बनाता है। Accept-encoding: x-i2p-gzip के साथ requests के लिए gzip का समर्थन करता है, ऐसी request में Content-encoding: x-i2p-gzip के साथ उत्तर देता है।

HTTP server proxy वेबसाइट होस्टिंग को आसान और अधिक सुरक्षित बनाने के लिए कई सेवाएं प्रदान करता है, और क्लाइंट साइड पर बेहतर उपयोगकर्ता अनुभव प्रदान करता है।

**Request header प्रसंस्करण:** - Header सत्यापन - Header spoof सुरक्षा - Header आकार जांच - वैकल्पिक inproxy और user-agent अस्वीकृति - X-I2P headers जोड़ना ताकि webserver को पता चल सके कि request कहाँ से आई - Host header प्रतिस्थापन ताकि webserver vhosts आसान हो जाएं - Force connection: close - RFC-अनुपालित hop-by-hop header प्रसंस्करण और stripping - दक्षता के लिए सभी headers को पास करने से पहले buffering

**DDoS सुरक्षा:** - POST थ्रॉटलिंग - टाइमआउट्स और slowloris सुरक्षा - सभी tunnel प्रकारों के लिए streaming में अतिरिक्त थ्रॉटलिंग होती है

**Response header processing:** - कुछ गोपनीयता-समस्याग्रस्त headers को हटाना - Mime type और अन्य headers की जांच करना कि response को compress करना है या नहीं - Force connection: close - RFC-अनुपालित hop-by-hop header processing और stripping - दक्षता के लिए सभी headers को पारित करने से पहले buffering करना

**HTTP error responses:** - कई सामान्य और असामान्य errors तथा throttling के लिए, ताकि client-side user को पता चल सके कि क्या हुआ

**पारदर्शी response compression:** - वेब सर्वर और/या I2CP layer compress कर सकते हैं, लेकिन वेब सर्वर अक्सर नहीं करता, और यह उच्च layer पर compress करना सबसे कुशल है, भले ही I2CP भी compress करे। HTTP server proxy client-side proxy के साथ सहयोग करके responses को पारदर्शी रूप से compress करने का काम करता है।

### HTTP द्विदिशीय {#server-mode-http-bidir}

*निष्प्रभावित*

एक I2PTunnel HTTP Server और एक I2PTunnel HTTP client दोनों के रूप में कार्य करता है जिसमें कोई outproxying क्षमताएं नहीं हैं। एक उदाहरण एप्लिकेशन एक वेब एप्लिकेशन होगा जो client-type अनुरोध करता है, या निदान उपकरण के रूप में I2P Site का loopback-testing करता है।

### IRC सर्वर {#server-mode-irc}

एक destination बनाता है जो क्लाइंट के registration sequence को फिल्टर करता है और क्लाइंट के destination key को hostname के रूप में IRC-server को पास करता है।

### Streamr {#server-mode-streamr}

एक UDP-client बनाया जाता है जो मीडिया सर्वर से जुड़ता है। UDP-Client को Streamr सर्वर I2PTunnel के साथ जोड़ा जाता है।
