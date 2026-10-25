---
title: "एप्लिकेशन डेवलपमेंट"
description: "I2P-विशिष्ट ऐप्स क्यों लिखें, मुख्य अवधारणाएं, विकास विकल्प, और शुरुआती गाइड"
slug: "applications"
aliases:
  - "/hi/docs/develop/applications"
  - "/hi/docs/develop/applications/"
  - "/hi/applications"
  - "/hi/applications/"
lastUpdated: "2013-05"
accurateFor: "0.9.6"
---

## I2P-विशिष्ट कोड क्यों लिखें?

I2P में applications का उपयोग करने के कई तरीके हैं। [I2PTunnel](/docs/api/i2ptunnel/) का उपयोग करके, आप बिना स्पष्ट I2P support को program किए नियमित applications का उपयोग कर सकते हैं। यह client-server scenarios के लिए बहुत प्रभावी है, जहाँ आपको किसी एकल website से connect करना हो। आप बस I2PTunnel का उपयोग करके उस website से connect करने के लिए एक tunnel बना सकते हैं, जैसा कि Figure 1 में दिखाया गया है।

यदि आपका एप्लिकेशन वितरित है, तो इसे बड़ी संख्या में peers से कनेक्शन की आवश्यकता होगी। I2PTunnel का उपयोग करते हुए, आपको प्रत्येक peer के लिए जिससे आप संपर्क करना चाहते हैं एक नई tunnel बनानी होगी, जैसा कि चित्र 2 में दिखाया गया है। यह प्रक्रिया निश्चित रूप से स्वचालित हो सकती है, लेकिन बहुत सारे I2PTunnel instances चलाना बड़ी मात्रा में ओवरहेड बनाता है। इसके अतिरिक्त, कई प्रोटोकॉल के साथ आपको सभी को सभी peers के लिए ports का एक ही सेट उपयोग करने के लिए मजबूर करना होगा — जैसे यदि आप विश्वसनीय रूप से DCC chat चलाना चाहते हैं, तो सभी को इस बात पर सहमत होना होगा कि port 10001 Alice का है, port 10002 Bob का है, port 10003 Charlie का है, और इसी तरह, क्योंकि प्रोटोकॉल में TCP/IP विशिष्ट जानकारी (host और port) शामिल होती है।

सामान्य नेटवर्क एप्लिकेशन अक्सर बहुत सारा अतिरिक्त डेटा भेजते हैं जिसका उपयोग उपयोगकर्ताओं की पहचान करने के लिए किया जा सकता है। होस्टनेम, पोर्ट नंबर, टाइम ज़ोन, कैरेक्टर सेट आदि अक्सर उपयोगकर्ता को सूचित किए बिना भेजे जाते हैं। इसलिए, नेटवर्क प्रोटोकॉल को विशेष रूप से गुमनामी को ध्यान में रखकर डिज़ाइन करना उपयोगकर्ता की पहचान से समझौता करने से बच सकता है।

I2P के साथ बातचीत करने के तरीके का निर्धारण करते समय दक्षता की बातों पर भी विचार करना होता है। streaming library और उस पर बनी चीजें TCP के समान handshakes के साथ काम करती हैं, जबकि मुख्य I2P protocols (I2NP और I2CP) सख्ती से message आधारित हैं (UDP या कुछ मामलों में raw IP की तरह)। महत्वपूर्ण अंतर यह है कि I2P के साथ, संचार एक long fat network पर हो रहा है — प्रत्येक end to end message में महत्वपूर्ण latencies होंगी, लेकिन इसमें कई KB तक के payloads हो सकते हैं। एक application जिसे एक सरल request और response की आवश्यकता है, वह MTU detection या messages के fragmentation की चिंता किए बिना (best effort) datagrams का उपयोग करके किसी भी state से छुटकारा पा सकती है और startup और teardown handshakes से होने वाली latency को कम कर सकती है।

![I2PTunnel का उपयोग करके सर्वर-क्लाइंट कनेक्शन बनाने के लिए केवल एक ही tunnel बनाना आवश्यक है।](/images/i2ptunnel_serverclient.png)

*चित्र 1: I2PTunnel का उपयोग करके सर्वर-क्लाइंट कनेक्शन बनाने के लिए केवल एक tunnel बनाना आवश्यक है।*

![एक peer-to-peer एप्लिकेशन के लिए कनेक्शन स्थापित करने के लिए बहुत बड़ी मात्रा में tunnel की आवश्यकता होती है।](/images/i2ptunnel_peertopeer.png)

*चित्र 2: peer-to-peer अनुप्रयोगों के लिए कनेक्शन स्थापित करने के लिए बहुत बड़ी मात्रा में tunnels की आवश्यकता होती है।*

संक्षेप में, I2P-विशिष्ट कोड लिखने के कई कारण:

- बड़ी मात्रा में I2PTunnel instances बनाना काफी संसाधनों की खपत करता है, जो वितरित अनुप्रयोगों के लिए समस्याजनक है (प्रत्येक peer के लिए एक नई tunnel की आवश्यकता होती है)।
- सामान्य नेटवर्क प्रोटोकॉल अक्सर बहुत सारा अतिरिक्त डेटा भेजते हैं जिसका उपयोग उपयोगकर्ताओं की पहचान के लिए किया जा सकता है। I2P के लिए विशेष रूप से प्रोग्रामिंग करने से एक नेटवर्क प्रोटोकॉल का निर्माण संभव होता है जो ऐसी जानकारी leak नहीं करता, उपयोगकर्ताओं को गुमनाम और सुरक्षित रखता है।
- नियमित इंटरनेट पर उपयोग के लिए डिज़ाइन किए गए नेटवर्क प्रोटोकॉल I2P पर अकुशल हो सकते हैं, जो बहुत अधिक latency वाला नेटवर्क है।

I2P डेवलपर्स के लिए एक मानक [plugins interface](/docs/specs/plugin/) का समर्थन करता है ताकि एप्लिकेशन्स को आसानी से एकीकृत और वितरित किया जा सके।

Java में लिखे गए और standard webapps/app.war के माध्यम से HTML interface का उपयोग करके accessible/runnable एप्लिकेशन को I2P distribution में शामिल करने के लिए विचार किया जा सकता है।

---

## महत्वपूर्ण अवधारणाएं

I2P का उपयोग करते समय कुछ बदलाव हैं जिनके साथ तालमेल बिठाना आवश्यक है:

### Destination ~= host+port

I2P पर चलने वाला एक एप्लिकेशन एक अद्वितीय क्रिप्टोग्राफिकली सुरक्षित अंत बिंदु — एक "destination" से संदेश भेजता है और प्राप्त करता है। TCP या UDP के संदर्भ में, एक destination को (मुख्यतः) hostname और port number की जोड़ी के बराबर माना जा सकता है, हालांकि कुछ अंतर हैं।

- एक I2P destination स्वयं में एक क्रिप्टोग्राफिक कंस्ट्रक्ट है — इसे भेजे जाने वाले सभी डेटा को इस प्रकार एन्क्रिप्ट किया जाता है जैसे कि IPsec की यूनिवर्सल डिप्लॉयमेंट हो और end point के (गुमनाम) स्थान पर इस प्रकार हस्ताक्षर किए गए हों जैसे कि DNSSEC की यूनिवर्सल डिप्लॉयमेंट हो।
- I2P destinations मोबाइल आइडेंटिफायर हैं — इन्हें एक I2P router से दूसरे में मूव किया जा सकता है (या यह "multihome" भी कर सकते हैं — एक साथ कई routers पर ऑपरेट कर सकते हैं)। यह TCP या UDP दुनिया से काफी अलग है जहां एक single end point (port) को एक single host पर ही रहना होता है।
- I2P destinations बदसूरत और बड़े होते हैं — पर्दे के पीछे, इनमें एन्क्रिप्शन के लिए एक 2048 bit ElGamal public key, साइनिंग के लिए एक 1024 bit DSA public key, और एक variable size certificate होता है, जिसमें proof of work या blinded data हो सकता है।

इन बड़े और जटिल destinations को छोटे और सुंदर नामों से संदर्भित करने के मौजूदा तरीके हैं (जैसे "irc.duck.i2p"), लेकिन ये तकनीकें वैश्विक स्तर पर विशिष्टता की गारंटी नहीं देतीं (क्योंकि ये प्रत्येक व्यक्ति की मशीन पर स्थानीय रूप से एक database में संग्रहीत होते हैं) और वर्तमान mechanism विशेष रूप से scalable या secure नहीं है (host list के updates को naming services की "subscriptions" का उपयोग करके प्रबंधित किया जाता है)। भविष्य में कोई secure, human readable, scalable, और globally unique naming system हो सकता है, लेकिन applications को इसके उपलब्ध होने पर निर्भर नहीं रहना चाहिए, क्योंकि कुछ लोगों का मानना है कि ऐसी चीज़ संभव नहीं है। [Naming system पर अधिक जानकारी](/docs/overview/naming/) उपलब्ध है।

जबकि अधिकांश applications को protocols और ports में अंतर करने की आवश्यकता नहीं होती, I2P *इन्हें* support करता है। जटिल applications एक single destination पर traffic को multiplex करने के लिए, प्रति-message के आधार पर, एक protocol, from port, और to port specify कर सकते हैं। विवरण के लिए [datagram page](/docs/api/datagrams/) देखें। सरल applications एक destination के "all protocols" पर "all ports" को listen करके operate करते हैं।

### गुमनामी और गोपनीयता

I2P में नेटवर्क पर भेजे गए सभी डेटा के लिए पारदर्शी end-to-end encryption और प्रमाणीकरण है — यदि Bob, Alice के destination पर भेजता है, तो केवल Alice का destination ही इसे प्राप्त कर सकता है, और यदि Bob datagrams या streaming library का उपयोग कर रहा है, तो Alice को निश्चित रूप से पता होता है कि Bob का destination ही वह है जिसने डेटा भेजा है।

बेशक, I2P Alice और Bob के बीच भेजे गए डेटा को पारदर्शी रूप से गुमनाम बनाता है, लेकिन यह उनके द्वारा भेजी जाने वाली सामग्री को गुमनाम बनाने के लिए कुछ नहीं करता। उदाहरण के लिए, यदि Alice Bob को अपने पूरे नाम, सरकारी ID, और क्रेडिट कार्ड नंबरों के साथ एक फॉर्म भेजती है, तो I2P कुछ नहीं कर सकता। इसलिए, protocols और applications को यह ध्यान रखना चाहिए कि वे किस जानकारी को सुरक्षित करने की कोशिश कर रहे हैं और किस जानकारी को उजागर करने के लिए तैयार हैं।

### I2P डेटाग्राम कई KB तक के हो सकते हैं

I2P datagrams का उपयोग करने वाले applications (चाहे raw हों या repliable) को मूल रूप से UDP के संदर्भ में समझा जा सकता है — datagrams unordered, best effort, और connectionless होते हैं — लेकिन UDP के विपरीत, applications को MTU detection की चिंता करने की आवश्यकता नहीं है और वे बस बड़े datagrams भेज सकते हैं। जबकि upper limit नाममात्र रूप से 32 KB है, message transport के लिए fragmented हो जाता है, इस प्रकार पूरे की reliability कम हो जाती है। लगभग 10 KB से अधिक के datagrams वर्तमान में recommended नहीं हैं। विवरण के लिए [datagram page](/docs/api/datagrams/) देखें। कई applications के लिए, 10 KB data एक पूरे request या response के लिए पर्याप्त है, जिससे वे I2P में UDP-like application के रूप में transparently operate कर सकते हैं बिना fragmentation, resends, आदि लिखे।

---

## विकास विकल्प

I2P पर डेटा भेजने के कई तरीके हैं, जिनमें से प्रत्येक के अपने फायदे और नुकसान हैं। streaming lib अनुशंसित इंटरफेस है, जिसका उपयोग अधिकांश I2P एप्लिकेशन करते हैं।

### स्ट्रीमिंग लाइब्रेरी

[पूरी streaming library](/docs/api/streaming/) अब मानक इंटरफेस है। यह TCP जैसे sockets का उपयोग करके प्रोग्रामिंग की अनुमति देती है, जैसा कि [Streaming development guide](#developing-with-the-streaming-library) में समझाया गया है।

### BOB

BOB एक [Basic Open Bridge](/docs/legacy/bob/) है, जो किसी भी भाषा में एप्लिकेशन को I2P से और I2P तक streaming connections बनाने की अनुमति देता है। इस समय इसमें UDP समर्थन नहीं है, लेकिन निकट भविष्य में UDP समर्थन की योजना है। BOB में कई उपकरण भी शामिल हैं, जैसे destination key generation, और यह सत्यापन कि कोई पता I2P specifications के अनुसार है। अद्यतन जानकारी और BOB का उपयोग करने वाले एप्लिकेशन इस [I2P Site](http://bob.i2p/) पर मिल सकते हैं।

### SAM, SAM V2, SAM V3

*SAM की सिफारिश नहीं की जाती। SAM V2 ठीक है, SAM V3 की सिफारिश की जाती है।*

SAM एक [Simple Anonymous Messaging](/docs/legacy/sam/) प्रोटोकॉल है, जो किसी भी भाषा में लिखे गए एप्लिकेशन को एक सामान्य TCP socket के माध्यम से SAM bridge से बात करने की अनुमति देता है और उस bridge को अपने सभी I2P ट्रैफिक को multiplex करने, पारदर्शी रूप से encryption/decryption और event आधारित handling को समन्वयित करने की सुविधा देता है। SAM तीन प्रकार के संचालन शैलियों का समर्थन करता है:

- streams, जब Alice और Bob एक दूसरे को डेटा विश्वसनीय रूप से और क्रम में भेजना चाहते हैं
- repliable datagrams, जब Alice Bob को एक संदेश भेजना चाहती है जिसका Bob उत्तर दे सके
- raw datagrams, जब Alice अधिकतम बैंडविड्थ और प्रदर्शन प्राप्त करना चाहती है, और Bob को इस बात की परवाह नहीं है कि डेटा का भेजने वाला प्रमाणित है या नहीं (जैसे स्थानांतरित डेटा स्वयं प्रमाणित है)

SAM V3 का लक्ष्य SAM और SAM V2 के समान ही है, लेकिन इसमें multiplexing/demultiplexing की आवश्यकता नहीं है। प्रत्येक I2P stream को एप्लिकेशन और SAM bridge के बीच अपने स्वयं के socket द्वारा संभाला जाता है। इसके अलावा, SAM bridge के साथ datagram संचार के माध्यम से एप्लिकेशन द्वारा datagrams भेजे और प्राप्त किए जा सकते हैं।

[SAM V2](/docs/legacy/samv2/) एक नया संस्करण है जो imule द्वारा उपयोग किया जाता है और यह [SAM](/docs/legacy/sam/) की कुछ समस्याओं को ठीक करता है।

[SAM V3](/docs/api/samv3/) का उपयोग imule द्वारा संस्करण 1.4.0 से किया जा रहा है।

### I2PTunnel

I2PTunnel एप्लिकेशन अनुप्रयोगों को peers के साथ विशिष्ट TCP-जैसी tunnels बनाने की अनुमति देता है, या तो I2PTunnel 'client' अनुप्रयोग बनाकर (जो एक विशिष्ट port पर सुनते हैं और जब भी उस port पर एक socket खोला जाता है तो एक विशिष्ट I2P destination से कनेक्ट होते हैं) या I2PTunnel 'server' अनुप्रयोग बनाकर (जो एक विशिष्ट I2P destination को सुनते हैं और जब भी उन्हें एक नया I2P कनेक्शन मिलता है तो वे एक विशिष्ट TCP host/port पर outproxy करते हैं)। ये streams 8-bit clean हैं, और उसी streaming library के माध्यम से प्रमाणित और सुरक्षित हैं जिसका SAM उपयोग करता है, लेकिन कई अद्वितीय I2PTunnel instances बनाने में एक महत्वपूर्ण overhead शामिल है, क्योंकि प्रत्येक का अपना अद्वितीय I2P destination और tunnels, keys आदि का अपना सेट होता है।

### SOCKS

I2P एक SOCKS V4 और V5 proxy का समर्थन करता है। आउटबाउंड कनेक्शन अच्छी तरह से काम करते हैं। इनबाउंड (सर्वर) और UDP कार्यक्षमता अधूरी और अपरीक्षित हो सकती है।

### मिनीस्ट्रीमिंग

*हटा दिया गया*

पहले एक सरल "ministreaming" library होती थी, लेकिन अब ministreaming.jar में केवल पूर्ण streaming library के लिए interfaces हैं।

### डेटाग्राम

*UDP-जैसे applications के लिए अनुशंसित*

[Datagram library](/docs/api/datagrams/) UDP जैसे packets भेजने की अनुमति देती है। इसका उपयोग करना संभव है:

- Repliable datagrams
- Raw datagrams

### I2CP

*अनुशंसित नहीं*

[I2CP](/docs/specs/i2cp/) स्वयं एक भाषा स्वतंत्र प्रोटोकॉल है, लेकिन Java के अलावा किसी अन्य भाषा में I2CP लाइब्रेरी को implement करने के लिए काफी मात्रा में कोड लिखना पड़ता है (encryption routines, object marshalling, asynchronous message handling, आदि)। जबकि कोई व्यक्ति C या किसी और भाषा में I2CP लाइब्रेरी लिख सकता है, इसके बजाय C SAM लाइब्रेरी का उपयोग करना अधिक उपयोगी होगा।

### वेब एप्लिकेशन

I2P Jetty webserver के साथ आता है, और इसके बजाय Apache server का उपयोग करने के लिए कॉन्फ़िगर करना सीधा है। कोई भी मानक web app technology काम करनी चाहिए।

---

## विकास शुरू करें — एक सरल गाइड

I2P का उपयोग करके विकास के लिए एक कार्यशील I2P स्थापना और आपकी पसंद के विकास वातावरण की आवश्यकता होती है। यदि आप Java का उपयोग कर रहे हैं, तो आप [streaming library](#developing-with-the-streaming-library) या datagram library के साथ विकास शुरू कर सकते हैं। अन्य प्रोग्रामिंग भाषा का उपयोग करते समय, SAM या BOB का उपयोग किया जा सकता है।

### Streaming Library के साथ विकास करना

निम्नलिखित उदाहरण दिखाता है कि streaming library का उपयोग करके TCP-जैसे client और server applications कैसे बनाएं।

इसके लिए आपके classpath में निम्नलिखित libraries की आवश्यकता होगी:

- `$I2P/lib/streaming.jar`: streaming लाइब्रेरी स्वयं
- `$I2P/lib/mstreaming.jar`: streaming लाइब्रेरी के लिए Factory और interfaces
- `$I2P/lib/i2p.jar`: मानक I2P classes, data structures, API, और utilities

आप इन्हें I2P installation से प्राप्त कर सकते हैं, या Maven Central से निम्नलिखित dependencies जोड़ सकते हैं:

- `net.i2p:i2p`
- `net.i2p.client:streaming`

नेटवर्क संचार के लिए I2P नेटवर्क sockets का उपयोग आवश्यक है। इसे प्रदर्शित करने के लिए, हम एक एप्लिकेशन बनाएंगे जहाँ एक क्लाइंट सर्वर को टेक्स्ट संदेश भेज सकता है, जो संदेशों को प्रिंट करेगा और उन्हें वापस क्लाइंट को भेज देगा। दूसरे शब्दों में, सर्वर एक echo की तरह काम करेगा।

हम server application को initialize करने से शुरुआत करेंगे। इसके लिए एक I2PSocketManager प्राप्त करना और एक I2PServerSocket बनाना आवश्यक है। हम I2PSocketManagerFactory को किसी मौजूदा Destination के लिए saved keys प्रदान नहीं करेंगे, इसलिए यह हमारे लिए एक नया Destination बना देगा। इसलिए हम I2PSocketManager से एक I2PSession मांगेंगे, ताकि हम उस Destination का पता लगा सकें जो बनाया गया था, क्योंकि हमें बाद में उस जानकारी को copy और paste करना होगा ताकि client हमसे connect हो सके।

```java
package i2p.echoserver;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        //Initialize application
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());
        //The additional main method code comes here...
    }

}
```
*कोड उदाहरण 1: सर्वर एप्लिकेशन को प्रारंभ करना।*

एक बार जब हमारे पास I2PServerSocket है, तो हम clients से connections स्वीकार करने के लिए I2PSocket instances बना सकते हैं। इस उदाहरण में, हम एक single I2PSocket instance बनाएंगे, जो एक समय में केवल एक client को handle कर सकता है। एक वास्तविक server को multiple clients को handle करने में सक्षम होना चाहिए। इसके लिए, multiple I2PSocket instances बनाने होंगे, प्रत्येक को अलग threads में। एक बार जब हमने I2PSocket instance बना लिया है, तो हम data पढ़ते हैं, इसे print करते हैं और इसे वापस client को भेजते हैं।

```java
package i2p.echoserver;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ConnectException;
import java.net.SocketTimeoutException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.util.I2PThread;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());

        //Create socket to handle clients
        I2PThread t = new I2PThread(new ClientHandler(serverSocket));
        t.setName("clienthandler1");
        t.setDaemon(false);
        t.start();
    }

    private static class ClientHandler implements Runnable {

        public ClientHandler(I2PServerSocket socket) {
            this.socket = socket;
        }

        public void run() {
            while(true) {
                try {
                    I2PSocket sock = this.socket.accept();
                    if(sock != null) {
                        //Receive from clients
                        BufferedReader br = new BufferedReader(new InputStreamReader(sock.getInputStream()));
                        //Send to clients
                        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(sock.getOutputStream()));
                        String line = br.readLine();
                        if(line != null) {
                            System.out.println("Received from client: " + line);
                            bw.write(line);
                            bw.flush(); //Flush to make sure everything got sent
                        }
                        sock.close();
                    }
                } catch (I2PException ex) {
                    System.out.println("General I2P exception!");
                } catch (ConnectException ex) {
                    System.out.println("Error connecting!");
                } catch (SocketTimeoutException ex) {
                    System.out.println("Timeout!");
                } catch (IOException ex) {
                    System.out.println("General read/write-exception!");
                }
            }
        }

        private I2PServerSocket socket;

    }

}
```
*कोड उदाहरण 2: क्लाइंट्स से कनेक्शन स्वीकार करना और संदेशों को संभालना।*

जब आप उपरोक्त server code चलाते हैं, तो यह कुछ इस प्रकार print करना चाहिए (लेकिन line endings के बिना, यह सिर्फ characters का एक विशाल block होना चाहिए):

```
y17s~L3H9q5xuIyyynyWahAuj6Jeg5VC~Klu9YPquQvD4vlgzmxn4yy~5Z0zVvKJiS2Lk
poPIcB3r9EbFYkz1mzzE3RYY~XFyPTaFQY8omDv49nltI2VCQ5cx7gAt~y4LdWqkyk3au
...
```
यह सर्वर Destination का base64-representation है। क्लाइंट को सर्वर तक पहुंचने के लिए इस स्ट्रिंग की आवश्यकता होगी।

अब, हम क्लाइंट एप्लिकेशन बनाएंगे। फिर से, प्रारंभीकरण के लिए कई चरणों की आवश्यकता है। फिर से, हमें I2PSocketManager प्राप्त करके शुरुआत करनी होगी। इस बार हम I2PSession और I2PServerSocket का उपयोग नहीं करेंगे। इसके बजाय, हम अपना कनेक्शन शुरू करने के लिए सर्वर Destination स्ट्रिंग का उपयोग करेंगे। हम उपयोगकर्ता से Destination स्ट्रिंग मांगेंगे, और इस स्ट्रिंग का उपयोग करके I2PSocket बनाएंगे। एक बार हमारे पास I2PSocket हो जाए, तो हम सर्वर से डेटा भेजना और प्राप्त करना शुरू कर सकते हैं।

```java
package i2p.echoclient;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.InterruptedIOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.ConnectException;
import java.net.NoRouteToHostException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;
import net.i2p.data.DataFormatException;
import net.i2p.data.Destination;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        System.out.println("Please enter a Destination:");
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String destinationString;
        try {
            destinationString = br.readLine();
        } catch (IOException ex) {
            System.out.println("Failed to get a Destination string.");
            return;
        }
        Destination destination;
        try {
            destination = new Destination(destinationString);
        } catch (DataFormatException ex) {
            System.out.println("Destination string incorrectly formatted.");
            return;
        }
        I2PSocket socket;
        try {
            socket = manager.connect(destination);
        } catch (I2PException ex) {
            System.out.println("General I2P exception occurred!");
            return;
        } catch (ConnectException ex) {
            System.out.println("Failed to connect!");
            return;
        } catch (NoRouteToHostException ex) {
            System.out.println("Couldn't find host!");
            return;
        } catch (InterruptedIOException ex) {
            System.out.println("Sending/receiving was interrupted!");
            return;
        }
        try {
            //Write to server
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            bw.write("Hello I2P!\n");
            //Flush to make sure everything got sent
            bw.flush();
            //Read from server
            BufferedReader br2 = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String s = null;
            while ((s = br2.readLine()) != null) {
                System.out.println("Received from server: " + s);
            }
            socket.close();
        } catch (IOException ex) {
            System.out.println("Error occurred while sending/receiving!");
        }
    }

}
```
*कोड उदाहरण 3: client को शुरू करना और इसे server एप्लिकेशन से जोड़ना।*

अंत में, आप server और client दोनों applications चला सकते हैं। पहले, server application शुरू करें। यह एक Destination string प्रिंट करेगा (जैसा कि ऊपर दिखाया गया है)। इसके बाद, client application शुरू करें। जब यह Destination string की मांग करे, तो आप server द्वारा प्रिंट की गई string दर्ज कर सकते हैं। फिर client 'Hello I2P!' (एक newline के साथ) server को भेजेगा, जो message को प्रिंट करेगा और इसे वापस client को भेज देगा।

बधाई हो, आपने I2P पर सफलतापूर्वक संचार कर लिया है!

---

## मौजूदा एप्लिकेशन

यदि आप योगदान देना चाहते हैं तो हमसे संपर्क करें।

- [I2P-Bote](http://i2pbote.i2p/) - HungryHobo से संपर्क करें
- [Syndie](http://syndie.i2p2.de/)
- [IMule](http://www.imule.i2p/)
- [I2Phex](http://forum.i2p/viewforum.php?f=25)

[plugins.i2p](http://plugins.i2p/) पर सभी plugins, [echelon.i2p](http://echelon.i2p/) पर सूचीबद्ध applications और source code, और [git.repo.i2p](http://git.repo.i2p/) पर होस्ट किए गए application code भी देखें।

I2P वितरण में बंडल किए गए एप्लिकेशन भी देखें - SusiMail और I2PSnark।

---

## एप्लीकेशन आइडियाज़

- NNTP server - अतीत में कुछ थे, इस समय कोई नहीं
- Jabber server - अतीत में कुछ थे, और इस समय एक है, जिसकी सार्वजनिक इंटरनेट तक पहुंच है
- PGP Key server और/या proxy
- Content Distribution / DHT applications - feedspace को पुनर्जीवित करें, dijjer को port करें, विकल्प खोजें
- [Syndie](http://syndie.i2p2.de/) development में मदद करें
- Web-based applications - blogs, pastebins, storage, tracking, feeds, आदि जैसे web-server-based applications होस्ट करने के लिए आकाश की कोई सीमा नहीं है। Perl, PHP, Python, या Ruby जैसी कोई भी web या CGI तकनीक काम करेगी।
- कुछ पुराने apps को पुनर्जीवित करें, जो पहले i2p source package में थे - bogobot, pants, proxyscript, q, stasher, socks proxy, i2ping, feedspace
