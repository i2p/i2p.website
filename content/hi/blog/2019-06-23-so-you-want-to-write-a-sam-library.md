---
title: "तो आप एक SAM लाइब्रेरी लिखना चाहते हैं"
date: 2019-06-23
author: "idk"
description: "शुरुआती के लिए SAM लाइब्रेरी लिखने की मार्गदर्शिका!"
---

*या, [i2p](https://geti2p.net) से बात करना उन लोगों के लिए जो स्पेसिफिकेशन पढ़ने के ज्यादा आदी नहीं हैं*

मेरी राय में, I2P की सबसे बेहतरीन विशेषताओं में से एक इसका SAM API है, जिसका उपयोग I2P और आपकी पसंद के अनुप्रयोग या भाषा के बीच एक सेतु बनाने के लिए किया जा सकता है। वर्तमान में, विभिन्न भाषाओं के लिए दर्जनों SAM लाइब्रेरी मौजूद हैं, जिनमें शामिल हैं:

- [i2psam, for c++](https://github.com/i2p/i2psam)
- [libsam3, for C](https://github.com/i2p/libsam3)
- [txi2p for Python](https://github.com/str4d/txi2p)
- [i2plib for Python](https://github.com/l-n-s/i2plib)
- [i2p.socket for Python](https://github.com/majestrate/i2p.socket)
- [leaflet for Python](https://github.com/MuxZeroNet/leaflet)
- [gosam, for Go](https://github.com/eyedeekay/gosam)
- [sam3 for Go](https://github.com/eyedeekay/sam3)
- [node-i2p for nodejs](https://github.com/redhog/node-i2p)
- [haskell-network-anonymous-i2p](https://github.com/solatis/haskell-network-anonymous-i2p)
- [i2pdotnet for .Net languages](https://github.com/SamuelFisher/i2pdotnet)
- [rust-i2p](https://github.com/stallmanifold/rust-i2p)
- [and i2p.rb for ruby](https://github.com/dryruby/i2p.rb)

यदि आप इनमें से किसी भाषा का उपयोग कर रहे हैं, तो आप किसी मौजूदा लाइब्रेरी का उपयोग करके अपने एप्लिकेशन को I2P पर पोर्ट कर सकते हैं। लेकिन यह ट्यूटोरियल उस बारे में नहीं है। यह ट्यूटोरियल इस बारे में है कि यदि आप किसी नई भाषा में SAM लाइब्रेरी बनाना चाहते हैं तो क्या करना चाहिए। इस ट्यूटोरियल में, मैं Java में एक नई SAM लाइब्रेरी कार्यान्वित करूंगा। मैंने Java चुना क्योंकि अभी तक ऐसी कोई Java लाइब्रेरी नहीं है जो आपको SAM से जोड़ती हो, Android में Java के उपयोग के कारण, और क्योंकि यह ऐसी भाषा है जिसके साथ लगभग हर किसी का कम से कम *थोड़ा* अनुभव है, इसलिए उम्मीद है कि आप इसे अपनी पसंद की भाषा में अनुवाद कर सकेंगे।

## अपनी लाइब्रेरी बनाना

आप अपनी खुद की लाइब्रेरी कैसे सेटअप करते हैं, यह उस भाषा पर निर्भर करेगा जिसे आप उपयोग करना चाहते हैं। इस उदाहरण लाइब्रेरी के लिए, हम java का उपयोग करेंगे ताकि हम इस तरह की लाइब्रेरी बना सकें:

```sh
mkdir jsam
cd jsam
gradle init --type java-library
```
या, यदि आप gradle 5 या उससे अधिक का उपयोग कर रहे हैं:

```sh
gradle init --type java-library --project-name jsam
```
## लाइब्रेरी की स्थापना

ऐसे कुछ डेटा आइटम होते हैं जिनका प्रबंधन लगभग हर SAM library को करना चाहिए। कम से कम, उसे उस SAM Bridge का पता सहेजना होगा जिसका आप उपयोग करना चाहते हैं, और वह हस्ताक्षर प्रकार जिसे आप उपयोग करना चाहते हैं।

### Storing the SAM address

मैं SAM पता को एक String (स्ट्रिंग) और एक Integer (इन्टीजर) के रूप में संग्रहीत करना पसंद करता हूँ, और runtime (रनटाइम) के दौरान एक function (फ़ंक्शन) में उन्हें फिर से संयोजित करता हूँ।

```java
public String SAMHost = "127.0.0.1";
public int SAMPort = 7656;
public String SAMAddress(){
    return SAMHost + ":" + SAMPort;
}
```
### Storing the Signature Type

I2P Tunnel के लिए मान्य हस्ताक्षर प्रकार DSA_SHA1, ECDSA_SHA256_P256, ECDSA_SHA384_P384, ECDSA_SHA512_P521, EdDSA_SHA512_Ed25519 हैं, लेकिन अगर आप कम-से-कम SAM 3.1 लागू करते हैं तो डिफ़ॉल्ट रूप में EdDSA_SHA512_Ed25519 का उपयोग करना दृढ़ता से अनुशंसित है। Java में, 'enum' डेटा स्ट्रक्चर इस कार्य के लिए उपयुक्त है, क्योंकि इसका उद्देश्य constants (स्थिर मान) के एक समूह को समाहित करना है। अपने Java class definition में enum, और उस enum का एक instance, जोड़ें।

```java
enum SIGNATURE_TYPE {
    DSA_SHA1,
    ECDSA_SHA256_P256,
    ECDSA_SHA384_P384,
    ECDSA_SHA512_P521,
    EdDSA_SHA512_Ed25519;
}
public SIGNATURE_TYPE SigType = SIGNATURE_TYPE.EdDSA_SHA512_Ed25519;
```
### SAM पता सहेजना

इससे SAM connection द्वारा उपयोग किए जा रहे हस्ताक्षर प्रकार का भरोसेमंद भंडारण सुनिश्चित होता है, लेकिन उसे bridge तक संप्रेषित करने के लिए आपको उसे अभी भी एक string के रूप में प्राप्त करना होगा।

```java
public String SignatureType() {
    switch (SigType) {
        case DSA_SHA1:
            return "SIGNATURE_TYPE=DSA_SHA1";
        case ECDSA_SHA256_P256:
            return "SIGNATURE_TYPE=ECDSA_SHA256_P256";
        case ECDSA_SHA384_P384:
            return "SIGNATURE_TYPE=ECDSA_SHA384_P384";
        case ECDSA_SHA512_P521:
            return "SIGNATURE_TYPE=ECDSA_SHA512_P521";
        case EdDSA_SHA512_Ed25519:
            return "SIGNATURE_TYPE=EdDSA_SHA512_Ed25519";
    }
    return "";
}
```
चीज़ों का परीक्षण करना महत्वपूर्ण है, तो चलिए कुछ परीक्षण लिखते हैं:

```java
@Test public void testValidDefaultSAMAddress() {
    Jsam classUnderTest = new Jsam();
    assertEquals("127.0.0.1:7656", classUnderTest.SAMAddress());
}
@Test public void testValidDefaultSignatureType() {
    Jsam classUnderTest = new Jsam();
    assertEquals("EdDSA_SHA512_Ed25519", classUnderTest.SignatureType());
}
```
यह हो जाने के बाद, अपना constructor (कन्स्ट्रक्टर) बनाना शुरू करें। ध्यान दें कि हमने अपनी लाइब्रेरी के लिए ऐसे डिफ़ॉल्ट निर्धारित किए हैं, जो अब तक मौजूद सभी I2P routers पर डिफ़ॉल्ट स्थितियों में उपयोगी रहेंगे।

```java
public Jsam(String host, int port, SIGNATURE_TYPE sig) {
    SAMHost = host;
    SAMPort = port;
    SigType = sig;
}
```
## Establishing a SAM Connection

आख़िरकार, अब रोचक भाग। SAM bridge के साथ अंतःक्रिया SAM bridge के पते पर एक "command" भेजकर की जाती है, और आप उस command के परिणाम को स्ट्रिंग-आधारित key-value pairs के एक सेट के रूप में पार्स कर सकते हैं। तो इसे ध्यान में रखते हुए, आइए पहले परिभाषित किए गए SAM Address के साथ एक read-write कनेक्शन स्थापित करें, फिर एक "CommandSAM" Function और एक reply parser लिखें।

### हस्ताक्षर प्रकार का संग्रहण

हम SAM के साथ Socket (सॉकेट) के जरिए संचार कर रहे हैं, इसलिए Socket से कनेक्ट करने, उससे पढ़ने, और उस पर लिखने के लिए, आपको Jsam क्लास में निम्नलिखित private वेरिएबल्स बनाने होंगे:

```java
private Socket socket;
private PrintWriter writer;
private BufferedReader reader;
```
आप उन वैरिएबल्स को अपने Constructors में इंस्टैंशिएट करने के लिए एक फ़ंक्शन भी बनाना चाहेंगे।

```java
public Jsam(String host, int port, SIGNATURE_TYPE sig) {
    SAMHost = host;
    SAMPort = port;
    SigType = sig;
    startConnection();
}
public void startConnection() {
    try {
        socket = new Socket(SAMHost, SAMPort);
        writer = new PrintWriter(socket.getOutputStream(), true);
        reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
    } catch (Exception e) {
        //omitted for brevity
    }
}
```
### हस्ताक्षर प्रकार प्राप्त करना:

अब आप अंततः SAM से बात करना शुरू करने के लिए पूरी तरह तैयार हैं। चीज़ों को सुव्यवस्थित रखने के लिए, आइए एक फ़ंक्शन बनाते हैं जो SAM को एक एकल कमांड भेजता है, जिसे एक नई पंक्ति (newline) से समाप्त किया जाता है, और जो एक Reply ऑब्जेक्ट लौटाता है, जिसे हम अगले चरण में बनाएँगे:

```java
public Reply CommandSAM(String args) {
    writer.println(args + "\n");
    try {
        String repl = reader.readLine();
        return new Reply(repl);
    } catch (Exception e) {
        //omitted for brevity
    }
}
```
ध्यान दें कि हम पिछले चरण में socket से बनाए गए writer और reader को उसी socket के लिए अपने इनपुट और आउटपुट के रूप में उपयोग कर रहे हैं। जब हमें reader से कोई reply मिलता है, तो हम उस string को Reply constructor को पास करते हैं, जो उसे पार्स करके एक Reply object वापस करता है।

### Parsing a reply and creating a Reply object.

जवाबों को अधिक आसानी से संभालने के लिए, हम SAM bridge से प्राप्त परिणामों को अपने-आप पार्स करने के लिए एक Reply ऑब्जेक्ट का उपयोग करेंगे। एक Reply में कम-से-कम एक विषय, एक प्रकार, और एक परिणाम होता है, साथ ही कुंजी-मूल्य युग्मों की मनमानी संख्या भी।

```java
public class Reply {
    String topic;
    String type;
    REPLY_TYPES result;
    Map<String, String> replyMap = new HashMap<String, String>();
```
जैसा कि आप देख सकते हैं, हम "result" को एक enum, REPLY_TYPES के रूप में संग्रहीत करेंगे। यह enum SAM bridge द्वारा दिए जाने वाले सभी संभावित प्रतिक्रिया परिणामों को शामिल करता है।

```java
enum REPLY_TYPES {
    OK,
    CANT_REACH_PEER,
    DUPLICATED_ID,
    DUPLICATED_DEST,
    I2P_ERROR,
    INVALID_KEY,
    KEY_NOT_FOUND,
    PEER_NOT_FOUND,
    TIMEOUT;
    public static REPLY_TYPES set(String type) {
        String temp = type.trim();
        switch (temp) {
        case "RESULT=OK":
            return OK;
        case "RESULT=CANT_REACH_PEER":
            return CANT_REACH_PEER;
        case "RESULT=DUPLICATED_ID":
            return DUPLICATED_ID;
        case "RESULT=DUPLICATED_DEST":
            return DUPLICATED_DEST;
        case "RESULT=I2P_ERROR":
            return I2P_ERROR;
        case "RESULT=INVALID_KEY":
            return INVALID_KEY;
        case "RESULT=KEY_NOT_FOUND":
            return KEY_NOT_FOUND;
        case "RESULT=PEER_NOT_FOUND":
            return PEER_NOT_FOUND;
        case "RESULT=TIMEOUT":
            return TIMEOUT;
        }
        return I2P_ERROR;
    }
    public static String get(REPLY_TYPES type) {
        switch (type) {
        case OK:
            return "RESULT=OK";
        case CANT_REACH_PEER:
            return "RESULT=CANT_REACH_PEER";
        case DUPLICATED_ID:
            return "RESULT=DUPLICATED_ID";
        case DUPLICATED_DEST:
            return "RESULT=DUPLICATED_DEST";
        case I2P_ERROR:
            return "RESULT=I2P_ERROR";
        case INVALID_KEY:
            return "RESULT=INVALID_KEY";
        case KEY_NOT_FOUND:
            return "RESULT=KEY_NOT_FOUND";
        case PEER_NOT_FOUND:
            return "RESULT=PEER_NOT_FOUND";
        case TIMEOUT:
            return "RESULT=TIMEOUT";
        }
        return "RESULT=I2P_ERROR";
    }
};
```
अब हम अपना कंस्ट्रक्टर बनाते हैं, जो सॉकेट से प्राप्त रिप्लाई स्ट्रिंग को एक पैरामीटर के रूप में लेता है, उसे पार्स करता है, और उसी जानकारी का उपयोग करके रिप्लाई ऑब्जेक्ट तैयार करता है। रिप्लाई स्पेस द्वारा विभाजित होती है, जिसमें कुंजी‑मान युग्म बराबर (=) चिह्न से जुड़े होते हैं और अंत में न्यूलाइन (नई पंक्ति) से समाप्त होती है।

```java
public Reply(String reply) {
    String trimmed = reply.trim();
    String[] replyvalues = reply.split(" ");
    if (replyvalues.length < 2) {
        //omitted for brevity
    }
    topic = replyvalues[0];
    type = replyvalues[1];
    result = REPLY_TYPES.set(replyvalues[2]);

    String[] replyLast = Arrays.copyOfRange(replyvalues, 2, replyvalues.length);
    for (int x = 0; x < replyLast.length; x++) {
        String[] kv = replyLast[x].split("=", 2);
        if (kv.length != 2) {

        }
        replyMap.put(kv[0], kv[1]);
    }
}
```
अंत में, सुविधा के लिए, आइए Reply ऑब्जेक्ट को एक toString() फ़ंक्शन दें जो Reply ऑब्जेक्ट का स्ट्रिंग प्रतिनिधित्व लौटाता है।

```java
public String toString() {
    return topic + " " + type + " " + REPLY_TYPES.get(result) + " " + replyMap.toString();
}
}
```
### SAM पोर्ट से कनेक्ट करना

अब हम "Hello" संदेश भेजकर SAM के साथ संचार स्थापित करने के लिए तैयार हैं। यदि आप एक नई SAM लाइब्रेरी लिख रहे हैं, तो आपको कम से कम SAM 3.1 को लक्षित करना चाहिए, क्योंकि यह I2P और i2pd दोनों में उपलब्ध है और SIGNATURE_TYPE पैरामीटर के लिए समर्थन पेश करता है।

```java
public boolean HelloSAM() {
    Reply repl = CommandSAM("HELLO VERSION MIN=3.0 MAX=3.1 \n");
    if (repl.result == Reply.REPLY_TYPES.OK) {
        return true;
    }
    System.out.println(repl.String());
    return false;
}
```
जैसा कि आप देख सकते हैं, हम पहले बनाई हुई CommandSAM फ़ंक्शन का उपयोग newline से समाप्त होने वाली कमांड `HELLO VERSION MIN=3.0 MAX=3.1 \n` भेजने के लिए करते हैं। यह SAM को बताता है कि आप API के साथ संचार शुरू करना चाहते हैं, और कि आप SAM संस्करण 3.0 और 3.1 के साथ संवाद करना जानते हैं। उसी के जवाब में, router `HELLO REPLY RESULT=OK VERSION=3.1` जैसा उत्तर देगा, जो एक string है जिसे आप Reply constructor को देकर एक वैध Reply object प्राप्त कर सकते हैं। अब से, हम अपनी CommandSAM फ़ंक्शन और Reply object का उपयोग SAM bridge के माध्यम से होने वाले सभी संचार को संभालने के लिए कर सकते हैं।

अंत में, आइए अपनी "HelloSAM" फ़ंक्शन के लिए एक परीक्षण जोड़ें।

```java
@Test public void testHelloSAM() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
}
```
### SAM को कमांड भेजना

अब जब आपने SAM के साथ अपना कनेक्शन नेगोशिएट कर लिया है और ऐसा SAM संस्करण तय कर लिया है जिसे आप दोनों समर्थन करते हैं, तो आप अपनी एप्लिकेशन के लिए peer-to-peer (सहकर्मी-से-सहकर्मी) कनेक्शन सेट कर सकते हैं ताकि वह अन्य i2p एप्लिकेशनों से जुड़ सके। आप यह SAM Bridge को "SESSION CREATE" कमांड भेजकर करते हैं। ऐसा करने के लिए, हम CreateSession फ़ंक्शन का उपयोग करेंगे, जो एक सेशन ID और एक डेस्टिनेशन प्रकार पैरामीटर स्वीकार करता है।

```java
public String CreateSession(String id, String destination ) {
    if (destination == "") {
        destination = "TRANSIENT";
    }
    Reply repl = CommandSAM("SESSION CREATE STYLE=STREAM ID=" + ID + " DESTINATION=" + destination);
    if (repl.result == Reply.REPLY_TYPES.OK) {
        return id;
    }
    return "";
}
```
यह आसान था, है ना? हमें बस इतना ही करना था कि अपनी HelloSAM फ़ंक्शन में उपयोग किए गए पैटर्न को `SESSION CREATE` कमांड पर लागू कर दें। ब्रिज से अच्छा उत्तर अब भी OK लौटाएगा, और उस स्थिति में हम नई बनाई गई SAM कनेक्शन का ID वापस करते हैं। अन्यथा, हम एक खाली स्ट्रिंग लौटाते हैं, क्योंकि वह वैसे भी एक अमान्य ID है और यह विफल हो गया, इसलिए जाँचना आसान हो जाता है। आइए इसके लिए एक परीक्षण लिखकर देखें कि यह फ़ंक्शन काम करता है या नहीं:

```java
@Test public void testCreateSession() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("test", classUnderTest.CreateSession("test", ""));
}
```
ध्यान दें कि इस परीक्षण में, हमारे सत्र शुरू करने से पहले SAM के साथ संचार स्थापित करने के लिए हमें पहले HelloSAM को कॉल करना *ज़रूरी* है। यदि ऐसा नहीं किया गया, तो ब्रिज एक त्रुटि के साथ उत्तर देगा और परीक्षण विफल हो जाएगा।

### उत्तर को पार्स करना और एक Reply ऑब्जेक्ट बनाना.

अब आपका सेशन स्थापित हो चुका है और आपका स्थानीय destination (गंतव्य) भी है, और आपको तय करना है कि आप इनके साथ क्या करना चाहते हैं। अब आप अपने सेशन को I2P के जरिए किसी दूरस्थ सेवा से कनेक्ट होने का निर्देश दे सकते हैं, या आने वाले कनेक्शनों की प्रतीक्षा करने के लिए कह सकते हैं जिनका उत्तर देना है। हालाँकि, किसी दूरस्थ destination से कनेक्ट करने से पहले, आपको उस destination का base64 प्राप्त करना पड़ सकता है, जिसकी API अपेक्षा करती है। यह करने के लिए, हम एक LookupName फ़ंक्शन बनाएँगे, जो base64 को उपयोगी रूप में लौटाएगा।

```java
public String LookupName(String name) {
    String cmd = "NAMING LOOKUP NAME=" + name + "\n";
    Reply repl = CommandSAM(cmd);
    if (repl.result == Reply.REPLY_TYPES.OK) {
        System.out.println(repl.replyMap.get("VALUE"));
        return repl.replyMap.get("VALUE");
    }
    return "";
}
```
फिर से, यह हमारे HelloSAM और CreateSession फ़ंक्शनों के लगभग समान है, बस एक अंतर के साथ। चूँकि हम विशेष रूप से VALUE खोज रहे हैं और NAME फ़ील्ड `name` आर्गुमेंट के समान होगी, यह केवल अनुरोधित destination (I2P सेवा का पहचानकर्ता) की base64 स्ट्रिंग लौटाता है।

अब जब हमारे पास हमारा LookupName फ़ंक्शन है, आइए इसका परीक्षण करें:

```java
@Test public void testLookupName() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("8ZAW~KzGFMUEj0pdchy6GQOOZbuzbqpWtiApEj8LHy2~O~58XKxRrA43cA23a9oDpNZDqWhRWEtehSnX5NoCwJcXWWdO1ksKEUim6cQLP-VpQyuZTIIqwSADwgoe6ikxZG0NGvy5FijgxF4EW9zg39nhUNKRejYNHhOBZKIX38qYyXoB8XCVJybKg89aMMPsCT884F0CLBKbHeYhpYGmhE4YW~aV21c5pebivvxeJPWuTBAOmYxAIgJE3fFU-fucQn9YyGUFa8F3t-0Vco-9qVNSEWfgrdXOdKT6orr3sfssiKo3ybRWdTpxycZ6wB4qHWgTSU5A-gOA3ACTCMZBsASN3W5cz6GRZCspQ0HNu~R~nJ8V06Mmw~iVYOu5lDvipmG6-dJky6XRxCedczxMM1GWFoieQ8Ysfuxq-j8keEtaYmyUQme6TcviCEvQsxyVirr~dTC-F8aZ~y2AlG5IJz5KD02nO6TRkI2fgjHhv9OZ9nskh-I2jxAzFP6Is1kyAAAA", classUnderTest.LookupName("i2p-projekt.i2p"));
}
```
### SAM को "HELLO" कहना

आखिरकार, हम अपनी नई लाइब्रेरी के साथ किसी दूसरी सेवा से कनेक्शन स्थापित करने जा रहे हैं। शुरुआत में यह हिस्सा मुझे थोड़ा उलझनभरा लगा, लेकिन सबसे सतर्क Java डेवलपर्स शायद सोच रहे होंगे कि हमने Jsam class के अंदर एक Socket वेरिएबल बनाने के बजाय socket class को extend क्यों नहीं किया। ऐसा इसलिए है क्योंकि अभी तक हम "Control Socket" से ही संवाद कर रहे थे, और वास्तविक संचार के लिए हमें एक नया socket बनाना होगा। इसीलिए हमने अब तक Jsam class में Socket class को extend करने का इंतज़ार किया है:

```java
public class Jsam extends Socket {
```
साथ ही, आइए अपनी startConnection फ़ंक्शन को इस तरह संशोधित करें कि हम इसे नियंत्रण सॉकेट से उस सॉकेट पर स्विच करने के लिए इस्तेमाल कर सकें जिसका हम अपने एप्लिकेशन में उपयोग करेंगे। अब यह एक Socket आर्गुमेंट लेगा।

```java
public void startConnection(Socket socket) {
    try {
        socket.connect(new InetSocketAddress(SAMHost, SAMPort), 600 );
    } catch (Exception e) {
        System.out.println(e);
    }
    try {
        writer = new PrintWriter(socket.getOutputStream(), true);
    } catch (Exception e) {
        System.out.println(e);
    }
    try {
        reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
    } catch (Exception e) {
        System.out.println(e);
    }
}
```
इससे हम जल्दी और आसानी से संचार के लिए एक नया सॉकेट खोल सकते हैं, "Hello SAM" हैंडशेक फिर से कर सकते हैं, और स्ट्रीम को कनेक्ट कर सकते हैं।

```java
public String ConnectSession(String id, String destination) {
    startConnection(this);
    HelloSAM();
    if (destination.endsWith(".i2p")) {
        destination = LookupName(destination);
    }
    String cmd = "STREAM CONNECT ID=" + id + " DESTINATION=" + destination + " SILENT=false";
    Reply repl = CommandSAM(cmd);
    if (repl.result == Reply.REPLY_TYPES.OK) {
        System.out.println(repl.String());
        return id;
    }
    System.out.println(repl.String());
    return "";
}
```
और अब आपके पास SAM के माध्यम से संचार करने के लिए एक नया सॉकेट है! आइए दूरस्थ कनेक्शनों को स्वीकार करने के लिए भी वही करें:

```java
public String AcceptSession(String id) {
    startConnection(this);
    HelloSAM();
    String cmd = "STREAM ACCEPT ID=" + id  + " SILENT=false";
    Reply repl = CommandSAM(cmd);
    if (repl.result == Reply.REPLY_TYPES.OK) {
        System.out.println(repl.String());
        return id;
    }
    System.out.println(repl.String());
    return "";
}
```
लीजिए, हो गया। इसी तरह आप चरण-दर-चरण SAM लाइब्रेरी बनाते हैं। भविष्य में, मैं इसे लाइब्रेरी के कार्यरत संस्करण Jsam और SAM v3 specification के साथ क्रॉस-रेफरेंस करूँगा, लेकिन अभी के लिए मुझे कुछ और काम निपटाने हैं।
