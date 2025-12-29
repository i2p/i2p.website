---
title: "Uygulama Geliştirme"
description: "Neden I2P'ye özgü uygulamalar yazmalı, temel kavramlar, geliştirme seçenekleri ve basit bir başlangıç kılavuzu"
slug: "applications"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Neden I2P'ye Özel Kod Yazılır?

I2P'de uygulamaları kullanmanın birden fazla yolu vardır. [I2PTunnel](/docs/api/i2ptunnel/) kullanarak, açık I2P desteği programlamaya gerek kalmadan normal uygulamaları kullanabilirsiniz. Bu, tek bir web sitesine bağlanmanız gereken istemci-sunucu senaryoları için çok etkilidir. Şekil 1'de gösterildiği gibi, o web sitesine bağlanmak için I2PTunnel kullanarak basitçe bir tunnel oluşturabilirsiniz.

Uygulamanız dağıtık ise, çok sayıda eşle bağlantı kurulması gerekecektir. I2PTunnel kullanırken, Şekil 2'de gösterildiği gibi, iletişim kurmak istediğiniz her eş için yeni bir tunnel oluşturmanız gerekir. Bu işlem elbette otomatikleştirilebilir, ancak çok sayıda I2PTunnel örneği çalıştırmak büyük miktarda ek yük oluşturur. Ayrıca, birçok protokolde tüm eşlerin aynı port setini kullanmasını zorlamanız gerekecektir — örneğin DCC sohbetini güvenilir şekilde çalıştırmak istiyorsanız, protokol TCP/IP'ye özgü bilgileri (host ve port) içerdiğinden, herkesin port 10001'in Alice, port 10002'nin Bob, port 10003'ün Charlie olduğu konusunda anlaşması gerekir.

Genel ağ uygulamaları genellikle kullanıcıları tanımlamak için kullanılabilecek çok sayıda ek veri gönderir. Ana bilgisayar adları, port numaraları, saat dilimleri, karakter setleri vb. sıklıkla kullanıcıya bilgi verilmeden gönderilir. Bu nedenle, ağ protokolünü özellikle anonimlik göz önünde bulundurularak tasarlamak, kullanıcı kimliklerinin tehlikeye girmesini önleyebilir.

I2P üzerinde nasıl etkileşim kurulacağını belirlerken gözden geçirilmesi gereken verimlilik hususları da vardır. Streaming kütüphanesi ve onun üzerine inşa edilen şeyler TCP'ye benzer el sıkışmalarla çalışırken, çekirdek I2P protokolleri (I2NP ve I2CP) kesinlikle mesaj tabanlıdır (UDP gibi veya bazı durumlarda ham IP gibi). Önemli ayrım şudur: I2P ile iletişim, uzun ve geniş bir ağ üzerinden gerçekleşir — her uçtan uca mesaj önemsiz olmayan gecikmelere sahip olacaktır, ancak birkaç KB'a kadar yük içerebilir. Basit bir istek ve yanıta ihtiyaç duyan bir uygulama, herhangi bir durumu ortadan kaldırabilir ve MTU algılama veya mesaj parçalama konusunda endişelenmeden (en iyi çaba) datagramları kullanarak başlatma ve sonlandırma el sıkışmaları tarafından oluşturulan gecikmeyi düşürebilir.

<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_serverclient.png" alt="Creating a server-client connection using I2PTunnel only requires creating a single tunnel." />
  <figcaption>Figure 1: Creating a server-client connection using I2PTunnel only requires creating a single tunnel.</figcaption>
</figure>
<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_peertopeer.png" alt="Setting up connections for a peer-to-peer applications requires a very large amount of tunnels." />
  <figcaption>Figure 2: Setting up connections for a peer-to-peer applications requires a very large amount of tunnels.</figcaption>
</figure>
Özetle, I2P'ye özgü kod yazmanın birkaç nedeni:

- Çok sayıda I2PTunnel örneği oluşturmak önemsiz olmayan miktarda kaynak tüketir, bu da dağıtık uygulamalar için sorunludur (her eş için yeni bir tunnel gereklidir).
- Genel ağ protokolleri genellikle kullanıcıları tanımlamak için kullanılabilecek çok miktarda ek veri gönderir. I2P için özel olarak programlama yapmak, bu tür bilgileri sızdırmayan bir ağ protokolü oluşturulmasına olanak tanır ve kullanıcıları anonim ve güvenli tutar.
- Normal internet üzerinde kullanılmak üzere tasarlanmış ağ protokolleri, çok daha yüksek gecikme süresine sahip bir ağ olan I2P'de verimsiz olabilir.

I2P, geliştiriciler için standart bir [eklenti arayüzünü](/docs/specs/plugin/) destekler, böylece uygulamalar kolayca entegre edilip dağıtılabilir.

Java ile yazılmış ve standart webapps/app.war üzerinden bir HTML arayüzü kullanılarak erişilebilen/çalıştırılabilen uygulamalar, I2P dağıtımına dahil edilmek üzere değerlendirilebilir.

## Önemli Kavramlar

I2P kullanırken uyum sağlanması gereken birkaç değişiklik vardır:

### Hedefler

I2P üzerinde çalışan bir uygulama, benzersiz bir kriptografik olarak güvenli uç nokta olan bir "destination" (hedef) üzerinden mesaj gönderir ve alır. TCP veya UDP terimleriyle, bir destination büyük ölçüde bir hostname ve port numarası çiftinin eşdeğeri olarak düşünülebilir, ancak birkaç fark vardır.

- I2P destination'ın kendisi kriptografik bir yapıdır — bir hedefe gönderilen tüm veriler, sanki IPsec evrensel olarak dağıtılmış gibi şifrelenir ve son noktanın (anonimleştirilmiş) konumu, sanki DNSSEC evrensel olarak dağıtılmış gibi imzalanır.
- I2P destination'lar hareketli tanımlayıcılardır — bir I2P router'dan diğerine taşınabilirler (hatta "multihome" yapabilirler — aynı anda birden fazla router üzerinde çalışabilirler). Bu, tek bir son noktanın (port) tek bir host üzerinde kalması gereken TCP veya UDP dünyasından oldukça farklıdır.
- I2P destination'lar çirkin ve büyüktür — perde arkasında, şifreleme için 2048 bitlik bir ElGamal public key, imzalama için 1024 bitlik bir DSA public key ve iş kanıtı (proof of work) veya gizlenmiş veri içerebilen değişken boyutlu bir sertifika bulunur.

Bu büyük ve çirkin hedeflere kısa ve hoş isimlerle (örn. "irc.duck.i2p") atıfta bulunmanın mevcut yolları vardır, ancak bu teknikler global benzersizliği garanti etmez (çünkü her kişinin makinesinde yerel bir veritabanında saklanırlar) ve mevcut mekanizma özellikle ölçeklenebilir veya güvenli değildir (host listesine yapılan güncellemeler, isimlendirme servislerine "abonelikler" kullanılarak yönetilir). Belki bir gün güvenli, insan tarafından okunabilir, ölçeklenebilir ve global olarak benzersiz bir isimlendirme sistemi olabilir, ancak uygulamalar bunun mevcut olmasına bağımlı olmamalıdır. [İsimlendirme sistemi hakkında daha fazla bilgi](/docs/overview/naming/) mevcuttur.

Çoğu uygulama protokolleri ve portları ayırt etmeye ihtiyaç duymasa da, I2P bunları *destekler*. Karmaşık uygulamalar, tek bir hedef üzerinde trafiği çoğullamak için mesaj bazında bir protokol, kaynak port ve hedef port belirtebilir. Ayrıntılar için [datagram sayfasına](/docs/api/datagrams/) bakın. Basit uygulamalar, bir hedefin "tüm portlarında" "tüm protokolleri" dinleyerek çalışır.

### Anonimlik ve Gizlilik

I2P, ağ üzerinden geçirilen tüm veriler için şeffaf uçtan uca şifreleme ve kimlik doğrulama sağlar — Bob, Alice'in hedefine gönderiyorsa, yalnızca Alice'in hedefi bunu alabilir ve Bob datagram veya streaming kütüphanesini kullanıyorsa, Alice, verileri gönderenin kesinlikle Bob'un hedefi olduğunu bilir.

Elbette I2P, Alice ve Bob arasında gönderilen verileri şeffaf bir şekilde anonimleştirir, ancak gönderdikleri içeriği anonimleştirmek için hiçbir şey yapmaz. Örneğin, Alice Bob'a tam adını, devlet kimlik bilgilerini ve kredi kartı numaralarını içeren bir form gönderirse, I2P'nin yapabileceği hiçbir şey yoktur. Bu nedenle, protokoller ve uygulamalar hangi bilgileri korumaya çalıştıklarını ve hangi bilgileri açığa çıkarmaya istekli olduklarını akılda tutmalıdır.

### I2P Datagramları Birkaç KB'a Kadar Olabilir

I2P datagramları kullanan uygulamalar (ham veya yanıtlanabilir olanlar) esasen UDP açısından düşünülebilir — datagramlar sırasız, en iyi çaba ile gönderilir ve bağlantısızdır — ancak UDP'nin aksine, uygulamaların MTU tespiti konusunda endişelenmesine gerek yoktur ve basitçe büyük datagramlar gönderebilirler. Üst sınır nominal olarak 32 KB olsa da, mesaj aktarım için parçalandığından, bütünün güvenilirliği düşer. Şu anda yaklaşık 10 KB'ın üzerindeki datagramlar önerilmemektedir. Ayrıntılar için [datagram sayfasına](/docs/api/datagrams/) bakın. Birçok uygulama için 10 KB veri, tüm bir istek veya yanıt için yeterlidir ve bu, uygulamaların parçalama, yeniden gönderme vb. yazmak zorunda kalmadan I2P'de UDP benzeri bir uygulama olarak şeffaf bir şekilde çalışmasına olanak tanır.

## Geliştirme Seçenekleri

I2P üzerinden veri göndermek için her birinin kendine özgü avantaj ve dezavantajları olan çeşitli yöntemler bulunmaktadır. Streaming kütüphanesi, I2P uygulamalarının çoğunluğu tarafından kullanılan önerilen arayüzdür.

### Streaming Kütüphanesi

[Tam streaming kütüphanesi](/docs/specs/streaming/) artık standart arayüzdür. [Streaming geliştirme kılavuzunda](#developing-with-the-streaming-library) açıklandığı gibi, TCP benzeri soketler kullanarak programlama yapılmasına olanak tanır.

### BOB

BOB, herhangi bir dildeki uygulamanın I2P'ye ve I2P'den akış bağlantıları kurmasını sağlayan [Basic Open Bridge](/docs/legacy/bob/) (Temel Açık Köprü)'dür. Şu anda UDP desteği bulunmamaktadır, ancak UDP desteği yakın gelecekte planlanmaktadır. BOB ayrıca destination key oluşturma ve bir adresin I2P spesifikasyonlarına uygun olup olmadığını doğrulama gibi çeşitli araçlar içerir. Güncel bilgiler ve BOB kullanan uygulamalar bu [I2P Sitesi](http://bob.i2p/)'nde bulunabilir.

### SAM, SAM V2, SAM V3

*SAM önerilmez. SAM V2 uygun, SAM V3 önerilir.*

SAM, herhangi bir dilde yazılmış bir uygulamanın düz bir TCP soketi üzerinden bir SAM köprüsüyle iletişim kurmasına ve bu köprünün tüm I2P trafiğini çoğullamasına, şifreleme/şifre çözme ve olay tabanlı işlemeyi şeffaf bir şekilde koordine etmesine olanak tanıyan [Simple Anonymous Messaging](/docs/legacy/sam/) protokolüdür. SAM üç işletim stilini destekler:

- stream'ler, Alice ve Bob birbirlerine güvenilir bir şekilde ve sırayla veri göndermek istediklerinde
- yanıtlanabilir datagram'lar, Alice'in Bob'a Bob'un yanıtlayabileceği bir mesaj göndermek istediğinde
- ham datagram'lar, Alice mümkün olduğunca fazla bant genişliği ve performans elde etmek istediğinde ve Bob verinin göndereninin kimliği doğrulanmış olup olmadığını umursamadığında (örn. aktarılan veri kendi kendini doğrulayan türde)

SAM V3, SAM ve SAM V2 ile aynı hedefe yönelir, ancak çoğullama/tekilleme (multiplexing/demultiplexing) gerektirmez. Her I2P akışı, uygulama ile SAM köprüsü arasında kendi soketi tarafından işlenir. Ayrıca, datagramlar SAM köprüsü ile datagram iletişimleri aracılığıyla uygulama tarafından gönderilebilir ve alınabilir.

[SAM V2](/docs/legacy/samv2/), [SAM](/docs/legacy/sam/)'deki bazı sorunları düzelten ve imule tarafından kullanılan yeni bir sürümdür.

[SAM V3](/docs/api/samv3/), imule tarafından 1.4.0 sürümünden itibaren kullanılmaktadır.

### I2PTunnel

I2PTunnel uygulaması, uygulamaların eşlere yönelik belirli TCP benzeri tüneller oluşturmasına olanak tanır. Bu, ya I2PTunnel 'istemci' uygulamaları (belirli bir portu dinleyen ve o porta bir soket açıldığında belirli bir I2P hedefine bağlanan) ya da I2PTunnel 'sunucu' uygulamaları (belirli bir I2P hedefini dinleyen ve yeni bir I2P bağlantısı aldığında belirli bir TCP host/port'a outproxy yapan) oluşturarak gerçekleştirilir. Bu akışlar 8-bit temizdir ve SAM'in kullandığı aynı streaming kütüphanesi aracılığıyla kimlik doğrulaması yapılır ve güvenli hale getirilir, ancak birden fazla benzersiz I2PTunnel örneği oluşturmanın önemsiz olmayan bir maliyeti vardır, çünkü her birinin kendi benzersiz I2P hedefi ve kendi tunnel, anahtar vb. seti bulunur.

### SOCKS

I2P, SOCKS V4 ve V5 proxy'sini destekler. Giden bağlantılar iyi çalışır. Gelen (sunucu) ve UDP işlevselliği eksik ve test edilmemiş olabilir.

### Ministreaming

*Kaldırıldı*

Eskiden basit bir "ministreaming" kütüphanesi vardı, ancak şimdi ministreaming.jar yalnızca tam streaming kütüphanesi için arayüzleri içeriyor.

### Datagramlar

*UDP benzeri uygulamalar için önerilir*

[Datagram kütüphanesi](/docs/api/datagrams/), UDP benzeri paketler göndermeyi sağlar. Kullanmak mümkündür:

- Yanıtlanabilir datagramlar
- Ham datagramlar

### I2CP

*Önerilmez*

[I2CP](/docs/specs/i2cp/) kendisi dilden bağımsız bir protokoldür, ancak Java dışında bir dilde I2CP kütüphanesi uygulamak için önemli miktarda kod yazılması gerekir (şifreleme rutinleri, nesne serileştirme, asenkron mesaj işleme, vb.). Birisi C veya başka bir dilde I2CP kütüphanesi yazabilse de, bunun yerine C SAM kütüphanesini kullanmak muhtemelen daha faydalı olacaktır.

### Web Uygulamaları

I2P, Jetty web sunucusu ile birlikte gelir ve bunun yerine Apache sunucusunu kullanacak şekilde yapılandırma oldukça basittir. Herhangi bir standart web uygulaması teknolojisi çalışmalıdır.

## Geliştirmeye Başlayın — Basit Bir Kılavuz

I2P kullanarak geliştirme yapmak, çalışan bir I2P kurulumu ve kendi seçtiğiniz bir geliştirme ortamı gerektirir. Java kullanıyorsanız, [streaming library](#developing-with-the-streaming-library) veya datagram library ile geliştirmeye başlayabilirsiniz. Başka bir programlama dili kullanıyorsanız, SAM veya BOB kullanılabilir.

### Streaming Kütüphanesi ile Geliştirme

Aşağıda, orijinal sayfadaki örneğin kısaltılmış ve güncellenmiş bir versiyonu bulunmaktadır. Tam örnek için eski sayfaya veya kod tabanımızdaki Java örneklerine bakın.

```java
// Server example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
I2PServerSocket server = manager.getServerSocket();
I2PSocket socket = server.accept();
BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
String s;
while ((s = br.readLine()) != null) {
    System.out.println("Received: " + s);
}
```
*Kod örneği: veri alan temel sunucu.*

```java
// Client example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
Destination dest = new Destination(serverDestBase64);
I2PSocket socket = manager.connect(dest);
BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
bw.write("Hello I2P!\n");
bw.flush();
```
*Kod örneği: istemci bağlanıyor ve bir satır gönderiyor.*
