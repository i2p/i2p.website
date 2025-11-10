---
title: "SAM Kütüphanesi Yazmak mı İstiyorsunuz"
date: 2019-06-23
author: "idk"
description: "Yeni başlayanlar için SAM kütüphanesi yazma rehberi!"
---

*Ya da, spesifikasyonları okumaya pek alışık olmayan kişiler için [i2p](https://geti2p.net) ile konuşmak*

Bence I2P'nin en iyi özelliklerinden biri SAM API'sidir; I2P ile seçtiğiniz uygulama veya dil arasında bir köprü kurmak için kullanılabilir. Şu anda çeşitli diller için onlarca SAM kütüphanesi mevcuttur; bunlara şunlar da dahildir:

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

Bu dillerden herhangi birini kullanıyorsanız, mevcut bir kütüphane aracılığıyla uygulamanızı I2P'ye zaten uyarlayabiliyor olabilirsiniz. Ancak bu öğretici bununla ilgili değil. Bu öğretici, yeni bir dilde bir SAM kütüphanesi oluşturmak istiyorsanız ne yapmanız gerektiğini anlatır. Bu öğreticide, Java'da yeni bir SAM kütüphanesi yazacağım. Java'yı seçtim; çünkü sizi SAM'e bağlayan bir Java kütüphanesi henüz yok, Java Android'de kullanılıyor ve neredeyse herkesin en azından *biraz* deneyimi olduğu bir dil; dolayısıyla umarım bunu seçtiğiniz bir programlama diline uyarlayabilirsiniz.

## Kütüphanenizi oluşturma

Kendi kütüphanenizi nasıl yapılandıracağınız, kullanmak istediğiniz dile bağlı olarak değişir. Bu örnek kütüphane için Java kullanacağız; böylece şu şekilde bir kütüphane oluşturabiliriz:

```sh
mkdir jsam
cd jsam
gradle init --type java-library
```
Veya, gradle 5 veya üzerini kullanıyorsanız:

```sh
gradle init --type java-library --project-name jsam
```
## Kütüphanenin Kurulumu

Hemen her SAM kütüphanesinin muhtemelen yönetmesi gereken birkaç veri vardır. En azından, kullanmayı planladığınız SAM Bridge’in adresini ve kullanmak istediğiniz imza türünü saklaması gerekecektir.

### Storing the SAM address

SAM adresini bir String ve bir Integer olarak saklamayı ve çalışma zamanında bir fonksiyonda bunları yeniden birleştirmeyi tercih ediyorum.

```java
public String SAMHost = "127.0.0.1";
public int SAMPort = 7656;
public String SAMAddress(){
    return SAMHost + ":" + SAMPort;
}
```
### Storing the Signature Type

I2P Tunnel için geçerli imza türleri DSA_SHA1, ECDSA_SHA256_P256, ECDSA_SHA384_P384, ECDSA_SHA512_P521, EdDSA_SHA512_Ed25519'dur, ancak en az SAM 3.1'i uygularsanız varsayılan olarak EdDSA_SHA512_Ed25519 kullanmanız şiddetle önerilir. Java'da, 'enum' veri yapısı sabitler grubunu içermek üzere tasarlandığından bu göreve uygundur. Java sınıf tanımınıza enum'u ve enum'un bir örneğini ekleyin.

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
### SAM adresinin saklanması

Bu, SAM bağlantısının kullandığı imza türünün güvenilir biçimde saklanmasını sağlar, ancak bunu köprüye iletebilmek için hâlâ dize olarak elde etmeniz gerekir.

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
Bir şeyleri test etmek önemlidir, öyleyse bazı testler yazalım:

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
Bu işlem tamamlandığında, yapıcınızı oluşturmaya başlayın. Kütüphanemiz için, şu ana kadar mevcut tüm I2P routers üzerinde varsayılan durumlarda işe yarayacak varsayılan ayarlar sunduğumuzu unutmayın.

```java
public Jsam(String host, int port, SIGNATURE_TYPE sig) {
    SAMHost = host;
    SAMPort = port;
    SigType = sig;
}
```
## Establishing a SAM Connection

Nihayet, işin güzel kısmına geldik. SAM bridge (SAM köprüsü) ile etkileşim, SAM bridge'in adresine bir "command" gönderilerek yapılır ve "command" sonucunu, metin (string) tabanlı anahtar-değer çiftlerinden oluşan bir küme olarak ayrıştırabilirsiniz. Bunu göz önünde bulundurarak, daha önce tanımladığımız SAM Address (SAM adresi)'e bir okuma-yazma bağlantısı kuralım, ardından bir "CommandSAM" fonksiyonu ve bir yanıt ayrıştırıcı yazalım.

### İmza Türünün Depolanması

Bir Socket aracılığıyla SAM ile iletişim kuruyoruz, bu nedenle sokete bağlanmak, soketten okumak ve sokete yazmak için Jsam sınıfında aşağıdaki private değişkenleri oluşturmanız gerekecek:

```java
private Socket socket;
private PrintWriter writer;
private BufferedReader reader;
```
Ayrıca, bunu yapmak için bir fonksiyon tanımlayarak bu değişkenleri kurucu metotlarınızda örneklemek isteyeceksiniz.

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
### İmza türünün alınması:

Artık nihayet SAM ile konuşmaya başlamaya hazırsınız. Her şeyi güzelce düzenli tutmak için, SAM'a, satır sonu karakteriyle sonlandırılan tek bir komut gönderen ve bir sonraki adımda oluşturacağımız bir Reply object (Reply nesnesi) döndüren bir fonksiyon oluşturalım:

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
Önceki adımda socket'ten oluşturduğumuz writer ve reader'ı, socket'e yönelik giriş ve çıkışlarımız olarak kullandığımıza dikkat edin. Reader'dan bir yanıt aldığımızda, dizeyi Reply yapıcısına iletiriz; bu da onu ayrıştırır ve Reply nesnesini döndürür.

### Parsing a reply and creating a Reply object.

Yanıtları daha kolay işleyebilmek için, SAM köprüsünden aldığımız sonuçları otomatik olarak ayrıştırmak üzere bir Reply nesnesi kullanacağız. Bir yanıt en az bir konu, bir tür ve bir sonuç içerir; ayrıca keyfi sayıda anahtar-değer çifti barındırabilir.

```java
public class Reply {
    String topic;
    String type;
    REPLY_TYPES result;
    Map<String, String> replyMap = new HashMap<String, String>();
```
Görebileceğiniz gibi, "result" değerini bir enum, REPLY_TYPES olarak saklayacağız. Bu enum, SAM köprüsünün yanıt verebileceği tüm olası yanıt sonuçlarını içerir.

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
Şimdi, soketten parametre olarak alınan yanıt dizesini kabul eden, onu ayrıştıran ve bu bilgileri kullanarak yanıt nesnesini yapılandıran kurucumuzu oluşturalım. Yanıt, boşlukla ayrılmıştır; anahtar-değer çiftleri eşittir (=) işaretiyle birleştirilir ve satır sonu karakteriyle sonlandırılır.

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
Son olarak, kolaylık olması için, Reply nesnesine Reply nesnesinin dize gösterimini döndüren bir toString() işlevi ekleyelim.

```java
public String toString() {
    return topic + " " + type + " " + REPLY_TYPES.get(result) + " " + replyMap.toString();
}
}
```
### SAM Portu'na Bağlanma

Artık SAM ile bir "Hello" mesajı göndererek iletişim kurmaya hazırız. Yeni bir SAM kütüphanesi yazıyorsanız, muhtemelen en az SAM 3.1'i hedeflemelisiniz; çünkü hem I2P hem de i2pd'de kullanılabilir ve SIGNATURE_TYPE parametresine destek getirir.

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
Gördüğünüz gibi, satır sonu karakteriyle sonlandırılmış `HELLO VERSION MIN=3.0 MAX=3.1 \n` komutunu göndermek için daha önce oluşturduğumuz CommandSAM fonksiyonunu kullanıyoruz. Bu, SAM’e API ile iletişim kurmaya başlamak istediğinizi ve SAM’in 3.0 ve 3.1 sürümlerini desteklediğinizi bildirir. Buna karşılık, router da `HELLO REPLY RESULT=OK VERSION=3.1` gibi bir yanıtla dönecektir; bu, geçerli bir Reply nesnesi elde etmek için Reply yapıcısına (constructor) iletebileceğiniz bir dize (string) niteliğindedir. Artık, SAM köprüsü üzerinden yapacağımız tüm iletişimi yönetmek için CommandSAM fonksiyonumuzu ve Reply nesnesini kullanabiliriz.

Son olarak, "HelloSAM" fonksiyonumuz için bir test ekleyelim.

```java
@Test public void testHelloSAM() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
}
```
### SAM'e Komut Göndermek

Artık SAM ile bağlantınızı müzakere edip ikinizin de konuştuğu bir SAM sürümü üzerinde anlaşmış olduğunuza göre, uygulamanızın diğer i2p uygulamalarına bağlanabilmesi için eşler arası bağlantılar kurabilirsiniz. Bunu SAM Bridge'e bir "SESSION CREATE" komutu göndererek yaparsınız. Bunu yapmak için, bir oturum kimliği ve bir hedef türü parametresi kabul eden CreateSession adlı bir işlev kullanacağız.

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
Bu kolaydı, değil mi? Yapmamız gereken tek şey, HelloSAM işlevimizde kullandığımız kalıbı `SESSION CREATE` komutuna uyarlamaktı. Köprüden (bridge) gelen iyi bir yanıt hâlâ OK döndürecektir ve bu durumda yeni oluşturulan SAM bağlantısının kimliğini (ID) geri döndürürüz. Aksi hâlde, zaten geçersiz bir kimlik (ID) olduğu ve işlem başarısız olduğu için boş bir dize döndürürüz; böylece kontrol etmesi kolay olur. Bu işlevin çalışıp çalışmadığını, onun için bir test yazarak görelim:

```java
@Test public void testCreateSession() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("test", classUnderTest.CreateSession("test", ""));
}
```
Dikkat: Bu testte, oturumumuzu başlatmadan önce SAM ile iletişimi kurmak için HelloSAM çağrısını yapmak *zorundayız*. Aksi halde, köprü bir hatayla yanıt verir ve test başarısız olur.

### Bir yanıtı ayrıştırmak ve bir Reply nesnesi oluşturmak.

Artık oturumunuz kuruldu ve yerel destination (I2P hedef kimliği) belirlendi; şimdi bunlarla ne yapmak istediğinize karar vermelisiniz. Oturumunuza, I2P üzerinden uzak bir servise bağlanması ya da gelen bağlantıları bekleyip yanıtlaması komutu verilebilir. Ancak, uzak bir destination’a bağlanmadan önce, API’nin beklediği de bu olduğundan, destination base64 kodlamasını edinmeniz gerekebilir. Bunu yapmak için, base64’ü kullanıma uygun bir biçimde döndürecek bir LookupName fonksiyonu oluşturacağız.

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
Yine, bu, HelloSAM ve CreateSession işlevlerimizle neredeyse aynıdır; tek bir farkla. Özellikle VALUE alanını aradığımız ve NAME alanı `name` argümanıyla aynı olacağı için, yalnızca istenen destination (hedef) için base64 dizesini döndürür.

Artık LookupName fonksiyonumuz olduğuna göre, onu test edelim:

```java
@Test public void testLookupName() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("8ZAW~KzGFMUEj0pdchy6GQOOZbuzbqpWtiApEj8LHy2~O~58XKxRrA43cA23a9oDpNZDqWhRWEtehSnX5NoCwJcXWWdO1ksKEUim6cQLP-VpQyuZTIIqwSADwgoe6ikxZG0NGvy5FijgxF4EW9zg39nhUNKRejYNHhOBZKIX38qYyXoB8XCVJybKg89aMMPsCT884F0CLBKbHeYhpYGmhE4YW~aV21c5pebivvxeJPWuTBAOmYxAIgJE3fFU-fucQn9YyGUFa8F3t-0Vco-9qVNSEWfgrdXOdKT6orr3sfssiKo3ybRWdTpxycZ6wB4qHWgTSU5A-gOA3ACTCMZBsASN3W5cz6GRZCspQ0HNu~R~nJ8V06Mmw~iVYOu5lDvipmG6-dJky6XRxCedczxMM1GWFoieQ8Ysfuxq-j8keEtaYmyUQme6TcviCEvQsxyVirr~dTC-F8aZ~y2AlG5IJz5KD02nO6TRkI2fgjHhv9OZ9nskh-I2jxAzFP6Is1kyAAAA", classUnderTest.LookupName("i2p-projekt.i2p"));
}
```
### SAM'a "HELLO" demek

Sonunda, yeni kütüphanemizle başka bir servise bağlantı kuracağız. Bu kısım başlangıçta beni biraz şaşırttı, ancak en dikkatli Java geliştiricileri muhtemelen Jsam sınıfının içinde bir Socket değişkeni oluşturmak yerine neden Socket sınıfını genişletmediğimizi merak ediyordu. Bunun nedeni, şimdiye kadar "Control Socket" ile iletişim kuruyor olmamız ve asıl iletişimi gerçekleştirmek için yeni bir soket oluşturmamız gerekmesi. Bu yüzden, Jsam sınıfını Socket sınıfından türetmeyi şimdiye kadar erteledik:

```java
public class Jsam extends Socket {
```
Ayrıca, startConnection fonksiyonumuzu, kontrol soketinden uygulamamızda kullanacağımız sokete geçiş yapabilmemiz için değiştirelim. Artık bir Socket argümanı alacak.

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
Bu, iletişim kurmak için hızla ve kolayca yeni bir soket açmamıza, "Hello SAM" el sıkışmasını yeniden gerçekleştirmemize ve akış bağlantısını kurmamıza olanak tanır.

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
Artık SAM üzerinden iletişim kurmak için yeni bir Socket'iniz var! Uzaktan bağlantıları kabul etmek için de aynısını yapalım:

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
İşte böyle. Bir SAM kitaplığını adım adım bu şekilde oluşturursunuz. İleride, bunu kütüphanenin çalışan sürümü olan Jsam ve SAMv3 spesifikasyonu ile çapraz karşılaştıracağım, ama şimdilik başka bazı işleri halletmem gerekiyor.
