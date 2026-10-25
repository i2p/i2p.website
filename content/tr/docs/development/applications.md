---
title: "Uygulama Geliştirme"
description: "Neden I2P'ye özgü uygulamalar yazılır, temel kavramlar, geliştirme seçenekleri ve başlangıç rehberi"
slug: "applications"
aliases:
  - "/tr/docs/develop/applications"
  - "/tr/docs/develop/applications/"
  - "/tr/applications"
  - "/tr/applications/"
lastUpdated: "2013-05"
accurateFor: "0.9.6"
---

## Neden I2P'ye Özgü Kod Yazmalı?

I2P'de uygulamaları kullanmanın birden fazla yolu vardır. [I2PTunnel](/docs/api/i2ptunnel/) kullanarak, açık I2P desteği programlama gerekmeden düzenli uygulamaları kullanabilirsiniz. Bu, tek bir web sitesine bağlanmanız gereken istemci-sunucu senaryoları için çok etkilidir. Şekil 1'de gösterildiği gibi, o web sitesine bağlanmak için I2PTunnel kullanarak basitçe bir tunnel oluşturabilirsiniz.

Uygulamanız dağıtık ise, çok sayıda eş ile bağlantı kurması gerekecektir. I2PTunnel kullanarak, iletişim kurmak istediğiniz her eş için yeni bir tunnel oluşturmanız gerekecektir, bu Şekil 2'de gösterildiği gibidir. Bu süreç elbette otomatikleştirilebilir, ancak çok sayıda I2PTunnel örneği çalıştırmak büyük miktarda ek yük yaratır. Ayrıca, birçok protokolde herkesi tüm eşler için aynı port setini kullanmaya zorlamanız gerekecektir — örneğin DCC sohbetini güvenilir şekilde çalıştırmak istiyorsanız, herkesin port 10001'in Alice, port 10002'nin Bob, port 10003'ün Charlie olduğu konusunda anlaşması gerekir ve böyle devam eder, çünkü protokol TCP/IP'ye özgü bilgileri (host ve port) içerir.

Genel ağ uygulamaları genellikle kullanıcıları tanımlamak için kullanılabilecek çok miktarda ek veri gönderir. Ana bilgisayar adları, port numaraları, saat dilimleri, karakter setleri vb. genellikle kullanıcı bilgilendirilmeden gönderilir. Bu nedenle, ağ protokolünü özellikle anonimlik düşünülerek tasarlamak, kullanıcı kimliklerinin tehlikeye girmesini önleyebilir.

I2P üzerinde nasıl etkileşim kurulacağını belirlerken gözden geçirilmesi gereken verimlilik hususları da vardır. Streaming kütüphanesi ve bunun üzerine inşa edilen şeyler TCP'ye benzer handshake'lerle çalışırken, çekirdek I2P protokolleri (I2NP ve I2CP) tamamen mesaj tabanlıdır (UDP veya bazı durumlarda ham IP gibi). Önemli ayrım şudur ki I2P ile iletişim uzun yağlı ağ üzerinden çalışır — her uçtan uca mesaj önemsiz olmayan gecikmelere sahip olacaktır, ancak birkaç KB'ye kadar yükler içerebilir. Basit istek ve yanıta ihtiyaç duyan bir uygulama, MTU tespiti veya mesaj parçalanması konularında endişelenmek zorunda kalmadan (en iyi çaba) datagramları kullanarak herhangi bir durumu kaldırabilir ve başlangıç ile kapanış handshake'lerinin neden olduğu gecikmeyi düşürebilir.

![I2PTunnel kullanarak sunucu-istemci bağlantısı oluşturmak yalnızca tek bir tunnel oluşturmayı gerektirir.](/images/i2ptunnel_serverclient.png)

*Şekil 1: I2PTunnel kullanarak sunucu-istemci bağlantısı oluşturmak yalnızca tek bir tunnel oluşturmayı gerektirir.*

![Eşler arası uygulamalar için bağlantı kurmak çok büyük miktarda tunnel gerektirir.](/images/i2ptunnel_peertopeer.png)

*Şekil 2: Eşler arası uygulamalar için bağlantı kurma çok büyük miktarda tunnel gerektirir.*

Özetle, I2P'ye özgü kod yazmanın bir dizi nedeni:

- Çok sayıda I2PTunnel örneği oluşturmak önemsiz olmayan miktarda kaynak tüketir, bu da dağıtık uygulamalar için sorunludur (her eş için yeni bir tunnel gereklidir).
- Genel ağ protokolleri genellikle kullanıcıları tanımlamak için kullanılabilecek çok miktarda ek veri gönderir. I2P için özel programlama, bu tür bilgileri sızdırmayan bir ağ protokolü oluşturulmasına olanak tanır ve kullanıcıları anonim ve güvenli tutar.
- Normal internet üzerinde kullanım için tasarlanmış ağ protokolleri, çok daha yüksek gecikme süresi olan bir ağ olan I2P üzerinde verimsiz olabilir.

I2P, geliştiriciler için standart bir [plugins arayüzünü](/docs/specs/plugin/) destekler böylece uygulamalar kolayca entegre edilip dağıtılabilir.

Java ile yazılmış ve standart webapps/app.war üzerinden HTML arayüzü kullanılarak erişilebilir/çalıştırılabilir uygulamalar, I2P dağıtımına dahil edilmek üzere değerlendirilebilir.

---

## Önemli Kavramlar

I2P kullanırken uyum sağlanması gereken birkaç değişiklik bulunmaktadır:

### Destination ~= host+port

I2P üzerinde çalışan bir uygulama, benzersiz kriptografik olarak güvenli bir uç nokta olan "destination"'dan mesajlar gönderir ve alır. TCP veya UDP terimleriyle, bir destination büyük ölçüde hostname ve port numarası çiftinin eşdeğeri olarak kabul edilebilir, ancak birkaç fark vardır.

- Bir I2P destination'ı kendisi kriptografik bir yapıdır — ona gönderilen tüm veriler, uç noktanın (anonimleştirilmiş) konumu DNSSEC'in evrensel dağıtımı varmış gibi imzalanmış şekilde, IPsec'in evrensel dağıtımı varmış gibi şifrelenir.
- I2P destination'ları mobil tanımlayıcılardır — bir I2P router'dan diğerine taşınabilirler (hatta "multihome" yapabilirler — aynı anda birden fazla router üzerinde çalışabilirler). Bu, tek bir uç noktanın (port) tek bir host üzerinde kalması gereken TCP veya UDP dünyasından oldukça farklıdır.
- I2P destination'ları çirkin ve büyüktür — perde arkasında, şifreleme için 2048 bit ElGamal public key, imzalama için 1024 bit DSA public key ve proof of work veya blinded data içerebilen değişken boyutlu bir sertifika barındırırlar.

Bu büyük ve çirkin hedeflere kısa ve güzel isimlerle (örneğin "irc.duck.i2p") başvurmanın mevcut yolları vardır, ancak bu teknikler küresel benzersizliği garanti etmez (çünkü her kişinin makinesindeki bir veritabanında yerel olarak saklanırlar) ve mevcut mekanizma özellikle ölçeklenebilir veya güvenli değildir (host listesindeki güncellemeler isimlendirme hizmetlerine "abonelikler" kullanılarak yönetilir). Bir gün güvenli, insan tarafından okunabilir, ölçeklenebilir ve küresel olarak benzersiz bir isimlendirme sistemi olabilir, ancak uygulamalar bunun yerinde olmasına bağlı olmamalıdır, çünkü böyle bir canavarın mümkün olmadığını düşünenler vardır. [İsimlendirme sistemi hakkında daha fazla bilgi](/docs/overview/naming/) mevcuttur.

Çoğu uygulama protokolleri ve portları ayırt etmek zorunda olmasa da, I2P bunları *destekler*. Karmaşık uygulamalar, tek bir hedef üzerinde trafiği çoklayabilmek için mesaj bazında protokol, kaynak port ve hedef port belirtebilir. Detaylar için [datagram sayfasına](/docs/api/datagrams/) bakın. Basit uygulamalar, bir hedefin "tüm portlarında" "tüm protokolleri" dinleyerek çalışır.

### Anonimlik ve Gizlilik

I2P, ağ üzerinden geçirilen tüm veriler için şeffaf uçtan uca şifreleme ve kimlik doğrulama sağlar — Bob, Alice'in hedefine gönderirse, yalnızca Alice'in hedefi bunu alabilir ve Bob datagram veya streaming kütüphanesini kullanıyorsa, Alice Bob'un hedefinin veriyi gönderen olduğunu kesin olarak bilir.

Tabii ki, I2P Alice ve Bob arasında gönderilen veriyi şeffaf bir şekilde anonimleştirir, ancak gönderdikleri içeriği anonimleştirmek için hiçbir şey yapmaz. Örneğin, Alice Bob'a tam adını, devlet kimlik numaralarını ve kredi kartı numaralarını içeren bir form gönderirse, I2P'nin yapabileceği hiçbir şey yoktur. Bu nedenle, protokoller ve uygulamalar hangi bilgiyi korumaya çalıştıklarını ve hangi bilgiyi ifşa etmeye istekli olduklarını göz önünde bulundurmalıdır.

### I2P Datagramları Birkaç KB'ye Kadar Olabilir

I2P datagramları (ham veya yanıtlanabilir olanlar) kullanan uygulamalar esasen UDP açısından düşünülebilir — datagramlar sırasız, en iyi çaba esası ve bağlantısızdır — ancak UDP'den farklı olarak, uygulamaların MTU tespiti konusunda endişelenmelerine gerek yoktur ve büyük datagramları kolayca gönderebilirler. Üst sınır nominal olarak 32 KB olsa da, mesaj taşıma için parçalara bölünür, bu da bütünün güvenilirliğini düşürür. Yaklaşık 10 KB'ın üzerindeki datagramlar şu anda önerilmemektedir. Ayrıntılar için [datagram sayfasına](/docs/api/datagrams/) bakın. Birçok uygulama için, 10 KB veri tam bir istek veya yanıt için yeterlidir ve parçalama, yeniden gönderme vb. yazmak zorunda kalmadan I2P'de UDP benzeri bir uygulama olarak şeffaf bir şekilde çalışmalarına olanak tanır.

---

## Geliştirme Seçenekleri

I2P üzerinden veri göndermek için her birinin kendine özgü avantaj ve dezavantajları olan çeşitli yöntemler bulunmaktadır. Streaming lib, I2P uygulamalarının çoğunluğu tarafından kullanılan önerilen arayüzdür.

### Streaming Lib

[Tam streaming kütüphanesi](/docs/api/streaming/) artık standart arayüzdür. [Streaming geliştirme kılavuzu](#developing-with-the-streaming-library)'nda açıklandığı gibi, TCP benzeri soketler kullanarak programlama yapılmasına olanak tanır.

### BOB

BOB, herhangi bir dildeki uygulamanın I2P'ye ve I2P'den akış bağlantıları kurmasını sağlayan [Basic Open Bridge](/docs/legacy/bob/) (Temel Açık Köprü)'dür. Şu anda UDP desteği bulunmamakla birlikte, yakın gelecekte UDP desteği planlanmaktadır. BOB ayrıca hedef anahtar üretimi ve bir adresin I2P spesifikasyonlarına uygun olduğunun doğrulanması gibi çeşitli araçlar içerir. Güncel bilgiler ve BOB kullanan uygulamalar bu [I2P Site](http://bob.i2p/)'da bulunabilir.

### SAM, SAM V2, SAM V3

*SAM önerilmez. SAM V2 kabul edilebilir, SAM V3 önerilir.*

SAM, herhangi bir dilde yazılmış bir uygulamanın düz bir TCP soket aracılığıyla bir SAM köprüsüyle iletişim kurmasına ve bu köprünün tüm I2P trafiğini çoklayarak şifreleme/şifre çözme ve olay tabanlı işlemeyi şeffaf bir şekilde koordine etmesine olanak tanıyan [Simple Anonymous Messaging](/docs/legacy/sam/) protokolüdür. SAM üç farklı işlem stilini destekler:

- akışlar, Alice ve Bob'un birbirlerine güvenilir bir şekilde ve sırayla veri göndermek istedikleri durumlar için
- yanıtlanabilir datagramlar, Alice'in Bob'a yanıtlayabileceği bir mesaj göndermek istediği durumlar için
- ham datagramlar, Alice'in mümkün olan en yüksek bant genişliği ve performansı sıkıştırmak istediği ve Bob'un verinin göndereninin doğrulanıp doğrulanmadığını umursamadığı durumlar için (örneğin aktarılan veri kendi kendini doğrulayan türde)

SAM V3, SAM ve SAM V2 ile aynı amacı hedefler, ancak multiplexing/demultiplexing gerektirmez. Her I2P akışı, uygulama ile SAM köprüsü arasında kendi soketi tarafından işlenir. Bunun yanında, datagramlar uygulama tarafından SAM köprüsü ile datagram iletişimi yoluyla gönderilebilir ve alınabilir.

[SAM V2](/docs/legacy/samv2/), [SAM](/docs/legacy/sam/)'deki bazı sorunları düzelten ve imule tarafından kullanılan yeni bir sürümdür.

[SAM V3](/docs/api/samv3/) sürüm 1.4.0'dan beri imule tarafından kullanılmaktadır.

### I2PTunnel

I2PTunnel uygulaması, uygulamaların I2PTunnel 'client' uygulamaları (belirli bir portu dinleyen ve o porta bir soket açıldığında belirli bir I2P hedefine bağlanan) ya da I2PTunnel 'server' uygulamaları (belirli bir I2P hedefini dinleyen ve yeni bir I2P bağlantısı aldığında belirli bir TCP host/portuna outproxy yapan) oluşturarak eşler arası özel TCP benzeri tunnel'lar kurmasına olanak tanır. Bu akışlar 8-bit temizdir ve SAM'in kullandığı streaming kütüphanesi aracılığıyla doğrulanır ve güvenli hale getirilir, ancak her birinin kendi benzersiz I2P hedefi ve kendi tunnel'lar, anahtarlar vb. seti olduğundan, birden fazla benzersiz I2PTunnel örneği oluşturmanın önemsiz olmayan bir maliyeti vardır.

### SOCKS

I2P, SOCKS V4 ve V5 proxy destekler. Giden bağlantılar iyi çalışır. Gelen (sunucu) ve UDP işlevselliği eksik ve test edilmemiş olabilir.

### Ministreaming

*Kaldırıldı*

Eskiden basit bir "ministreaming" kütüphanesi vardı, ancak şimdi ministreaming.jar yalnızca tam streaming kütüphanesi için arayüzleri içeriyor.

### Datagramlar

*UDP benzeri uygulamalar için önerilir*

[Datagram kütüphanesi](/docs/api/datagrams/) UDP benzeri paketler göndermeye olanak tanır. Kullanmak mümkündür:

- Yanıtlanabilir datagramlar
- Ham datagramlar

### I2CP

*Önerilmez*

[I2CP](/docs/specs/i2cp/) kendisi dil bağımsız bir protokoldür, ancak Java dışında bir dilde I2CP kütüphanesi geliştirmek için önemli miktarda kod yazılması gerekir (şifreleme rutinleri, nesne marshalling'i, asenkron mesaj işleme, vb.). Birisi C veya başka bir dilde I2CP kütüphanesi yazabilse de, büyük olasılıkla bunun yerine C SAM kütüphanesini kullanmak daha faydalı olacaktır.

### Web Uygulamaları

I2P, Jetty web sunucusu ile birlikte gelir ve bunun yerine Apache sunucusunu kullanmak üzere yapılandırma oldukça basittir. Herhangi bir standart web uygulaması teknolojisi çalışmalıdır.

---

## Geliştirmeye Başlayın — Basit Bir Kılavuz

I2P kullanarak geliştirme yapmak için çalışan bir I2P kurulumu ve kendi seçiminizde bir geliştirme ortamına ihtiyacınız vardır. Java kullanıyorsanız, [streaming library](#developing-with-the-streaming-library) veya datagram library ile geliştirmeye başlayabilirsiniz. Başka bir programlama dili kullanıyorsanız, SAM veya BOB kullanılabilir.

### Streaming Library ile Geliştirme

Aşağıdaki örnek, streaming kütüphanesini kullanarak TCP benzeri istemci ve sunucu uygulamalarının nasıl oluşturulacağını gösterir.

Bu, classpath'inizde aşağıdaki kütüphaneleri gerektirecektir:

- `$I2P/lib/streaming.jar`: Streaming kütüphanesinin kendisi
- `$I2P/lib/mstreaming.jar`: Streaming kütüphanesi için fabrika ve arayüzler
- `$I2P/lib/i2p.jar`: Standart I2P sınıfları, veri yapıları, API ve yardımcı araçlar

Bunları bir I2P kurulumundan alabilir veya Maven Central'dan aşağıdaki bağımlılıkları ekleyebilirsiniz:

- `net.i2p:i2p`
- `net.i2p.client:streaming`

Ağ iletişimi I2P ağ soketlerinin kullanımını gerektirir. Bunu göstermek için, bir istemcinin sunucuya metin mesajları gönderebileceği ve sunucunun bu mesajları yazdırıp istemciye geri göndereceği bir uygulama oluşturacağız. Başka bir deyişle, sunucu bir yankı işlevi görecek.

Sunucu uygulamasını başlatarak başlayacağız. Bu, bir I2PSocketManager almayı ve bir I2PServerSocket oluşturmayı gerektirir. I2PSocketManagerFactory'ye mevcut bir Destination için kaydedilmiş anahtarları sağlamayacağız, böylece bizim için yeni bir Destination oluşturacak. Bu yüzden I2PSocketManager'dan bir I2PSession isteyeceğiz, böylece oluşturulan Destination'ı öğrenebiliriz, çünkü istemcinin bize bağlanabilmesi için bu bilgiyi daha sonra kopyalayıp yapıştırmamız gerekecek.

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
*Kod örneği 1: sunucu uygulamasını başlatma.*

I2PServerSocket elde ettiğimizde, istemcilerden gelen bağlantıları kabul etmek için I2PSocket örnekleri oluşturabiliriz. Bu örnekte, aynı anda yalnızca bir istemciyi işleyebilen tek bir I2PSocket örneği oluşturacağız. Gerçek bir sunucu birden fazla istemciyi işleyebilmelidir. Bunu yapmak için, her biri ayrı thread'lerde olmak üzere birden fazla I2PSocket örneği oluşturulmalıdır. I2PSocket örneğini oluşturduktan sonra, veriyi okur, yazdırır ve istemciye geri göndeririz.

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
*Kod örneği 2: istemcilerden bağlantıları kabul etme ve mesajları işleme.*

Yukarıdaki sunucu kodunu çalıştırdığınızda, şuna benzer bir çıktı yazdırması gerekir (ancak satır sonları olmadan, sadece büyük bir karakter bloğu olarak):

```
y17s~L3H9q5xuIyyynyWahAuj6Jeg5VC~Klu9YPquQvD4vlgzmxn4yy~5Z0zVvKJiS2Lk
poPIcB3r9EbFYkz1mzzE3RYY~XFyPTaFQY8omDv49nltI2VCQ5cx7gAt~y4LdWqkyk3au
...
```
Bu, sunucu Destination'ının base64 temsilidir. İstemci sunucuya ulaşmak için bu dizgeye ihtiyaç duyacaktır.

Şimdi, istemci uygulamasını oluşturacağız. Yine, başlatma için bir dizi adım gereklidir. Yine, bir I2PSocketManager alarak başlamamız gerekecek. Bu sefer bir I2PSession ve I2PServerSocket kullanmayacağız. Bunun yerine, bağlantımızı başlatmak için sunucu Destination dizesini kullanacağız. Kullanıcıdan Destination dizesini isteyeceğiz ve bu dizeyi kullanarak bir I2PSocket oluşturacağız. Bir I2PSocket'e sahip olduğumuzda, sunucuya veri göndermeye ve sunucudan veri almaya başlayabiliriz.

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
*Kod örneği 3: istemciyi başlatmak ve sunucu uygulamasına bağlamak.*

Son olarak, hem sunucu hem de istemci uygulamasını çalıştırabilirsiniz. İlk olarak sunucu uygulamasını başlatın. Bu, bir Destination dizesi yazdıracaktır (yukarıda gösterildiği gibi). Ardından, istemci uygulamasını başlatın. Bir Destination dizesi istediğinde, sunucu tarafından yazdırılan dizeyi girebilirsiniz. İstemci daha sonra sunucuya 'Hello I2P!' (bir satır sonu ile birlikte) gönderecek, sunucu da mesajı yazdırıp istemciye geri gönderecektir.

Tebrikler, I2P üzerinden başarıyla iletişim kurdunuz!

---

## Mevcut Uygulamalar

Katkıda bulunmak istiyorsanız bizimle iletişime geçin.

- [I2P-Bote](http://i2pbote.i2p/) - HungryHobo ile iletişime geçin
- [Syndie](http://syndie.i2p2.de/)
- [IMule](http://www.imule.i2p/)
- [I2Phex](http://forum.i2p/viewforum.php?f=25)

Ayrıca [plugins.i2p](http://plugins.i2p/) üzerindeki tüm eklentileri, [echelon.i2p](http://echelon.i2p/) üzerinde listelenen uygulamaları ve kaynak kodları ile [git.repo.i2p](http://git.repo.i2p/) üzerinde barındırılan uygulama kodlarını da inceleyin.

I2P dağıtımında bulunan paketli uygulamaları da görün - SusiMail ve I2PSnark.

---

## Uygulama Fikirleri

- NNTP sunucusu - geçmişte bazıları vardı, şu anda hiçbiri yok
- Jabber sunucusu - geçmişte bazıları vardı ve şu anda genel internete erişimi olan bir tane var
- PGP Anahtar sunucusu ve/veya proxy
- İçerik Dağıtımı / DHT uygulamaları - feedspace'i yeniden canlandır, dijjer'ı port et, alternatifleri ara
- [Syndie](http://syndie.i2p2.de/) geliştirmesine yardım et
- Web tabanlı uygulamalar - Bloglar, pastebinler, depolama, takip, beslemeler vb. gibi web sunucusu tabanlı uygulamaları barındırmak için sınır tanımaz. Perl, PHP, Python veya Ruby gibi herhangi bir web veya CGI teknolojisi çalışacaktır.
- Eski uygulamaları yeniden canlandır, daha önce i2p kaynak paketindeki birçoğu - bogobot, pants, proxyscript, q, stasher, socks proxy, i2ping, feedspace
