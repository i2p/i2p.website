---
title: "I2PTunnel"
description: "I2P üzerinde arayüz sağlama ve hizmet sunma aracı"
slug: "i2ptunnel"
aliases:
  - "/tr/i2ptunnel"
  - "/tr/i2ptunnel/"
  - "/tr/i2ptunnel_migration"
  - "/tr/i2ptunnel_migration/"
  - "/tr/i2ptunnel_services"
  - "/tr/i2ptunnel_services/"
lastUpdated: "2023-10"
accurateFor: "0.9.59"
---

## Genel Bakış {#overview}

I2PTunnel, I2P üzerinde arayüz oluşturmak ve hizmet sağlamak için kullanılan bir araçtır. Bir I2PTunnel'ın hedefi [hostname](/docs/overview/naming), [Base32](/docs/overview/naming#base32) veya tam 516-bayt destination anahtarı kullanılarak tanımlanabilir. Kurulmuş bir I2PTunnel, istemci makinenizde localhost:port olarak erişilebilir olacaktır. I2P ağında bir hizmet sağlamak istiyorsanız, uygun ip_address:port adresine bir I2PTunnel oluşturmanız yeterlidir. Hizmet için karşılık gelen 516-bayt destination anahtarı oluşturulacak ve I2P genelinde erişilebilir hale gelecektir. I2PTunnel yönetimi için web arayüzü [localhost:7657/i2ptunnel/](http://localhost:7657/i2ptunnel/) adresinde mevcuttur.

## Varsayılan Hizmetler {#default-services}

### Sunucu Tunnel'ları {#default-server-tunnels}

- **I2P Webserver** - I2P üzerinde kolay ve hızlı hosting için [localhost:7658](http://localhost:7658) adresinde çalışan bir Jetty webserver'a yönlendirilen tunnel.
  Belge kök dizini:
  - **Unix** - `$HOME/.i2p/eepsite/docroot`
  - **Windows** - `%LOCALAPPDATA%\I2P\I2P Site\docroot`, şu şekilde genişler: `C:\Users\**username**\AppData\Local\I2P\I2P Site\docroot`

### İstemci Tünelleri {#default-client-tunnels}

- **I2P HTTP Proxy** - *localhost:4444* - I2P ve normal interneti I2P üzerinden anonim olarak gezinmek için kullanılan bir HTTP proxy'si. I2P üzerinden internet gezinmek, "Outproxies:" seçeneği tarafından belirtilen rastgele bir proxy kullanır.
- **Irc2P** - *localhost:6668* - Varsayılan anonim IRC ağı olan Irc2P'ye yönelik bir IRC tunnel'ı.
- **gitssh.idk.i2p** - *localhost:7670* - Proje Git deposuna SSH erişimi
- **smtp.postman.i2p** - *localhost:7659* - hq.postman.i2p adresindeki postman tarafından sağlanan bir SMTP hizmeti
- **pop3.postman.i2p** - *localhost:7660* - hq.postman.i2p adresindeki postman'ın eşlik eden POP hizmeti

## Yapılandırma {#configuration}

[I2PTunnel Konfigürasyonu](/docs/specs/configuration)

## İstemci Modları {#client-modes}

### Standart {#client-modes-standard}

I2P içindeki bir hedefte bulunan bir servise (HTTP, FTP veya SMTP gibi) bağlanan yerel bir TCP portu açar. Tunnel, virgülle ayrılmış (", ") hedef listesinden rastgele bir host'a yönlendirilir.

### HTTP {#client-mode-http}

Bir HTTP-istemci tüneli. Tünel, HTTP isteğindeki URL ile belirtilen hedefe bağlanır. Bir outproxy sağlanmışsa internet'e proxy yapılmasını destekler. HTTP bağlantılarından aşağıdaki başlıkları çıkarır:

- **Accept\*:** ("Accept" ve "Accept-Encoding" hariç) çünkü bu başlıklar tarayıcılar arasında büyük farklılık gösterir ve tanımlayıcı olarak kullanılabilir.
- **Referer:**
- **Via:**
- **From:**

HTTP istemci proxy'si, kullanıcıyı korumak ve daha iyi bir kullanıcı deneyimi sağlamak için bir dizi hizmet sunar.

**İstek başlığı işleme:** - Gizlilik sorunlu başlıkları kaldırma - Yerel veya uzak outproxy'ye yönlendirme - Outproxy seçimi, önbellekleme ve erişilebilirlik takibi - Hostname'den hedef arama - Host başlığını b32'ye değiştirme - Şeffaf açma desteğini belirten başlık ekleme - Bağlantı kapatmaya zorlama - RFC uyumlu proxy desteği - RFC uyumlu hop-by-hop başlık işleme ve kaldırma - İsteğe bağlı digest ve temel kullanıcı adı/şifre kimlik doğrulaması - İsteğe bağlı outproxy digest ve temel kullanıcı adı/şifre kimlik doğrulaması - Verimlilik için geçiş öncesi tüm başlıkları arabelleğe alma - Jump server bağlantıları - Jump yanıt işleme ve formları (adres yardımcısı) - Gizlenmiş b32 işleme ve kimlik bilgisi formları - Standart HTTP ve HTTPS (CONNECT) isteklerini destekler

**Yanıt başlığı işleme:** - Yanıtın açılıp açılmayacağının kontrol edilmesi - Bağlantının zorla kapatılması - RFC uyumlu hop-by-hop başlık işleme ve çıkarma - Verimlilik için tüm başlıkların geçirilmeden önce tamponlanması

**HTTP hata yanıtları:** - Birçok yaygın ve yaygın olmayan hata için, böylece kullanıcı ne olduğunu bilir - Çeşitli hatalar için 20'den fazla benzersiz çevrilmiş, stillendirilmiş ve biçimlendirilmiş hata sayfası - Formları, CSS'i, görselleri ve hataları sunmak için dahili web sunucusu

#### Şeffaf Yanıt Sıkıştırması {#transparent-response-compression}

i2ptunnel yanıt sıkıştırması HTTP başlığı ile istenir:

- **X-Accept-Encoding:** x-i2p-gzip;q=1.0, identity;q=0.5, deflate;q=0, gzip;q=0, *;q=0

Sunucu tarafı, isteği web sunucusuna göndermeden önce bu hop-by-hop başlığını kaldırır. Tüm q değerlerini içeren ayrıntılı başlık gerekli değildir; sunucular sadece başlıkta herhangi bir yerde "x-i2p-gzip" aramalıdır.

Sunucu tarafı, yanıtın sıkıştırılabilir olup olmadığını ve gereken ek CPU'nun değip değmeyeceğini değerlendirmek için web sunucusundan alınan Content-Type, Content-Length ve Content-Encoding dahil olmak üzere başlıklara dayanarak yanıtı sıkıştırıp sıkıştırmayacağını belirler. Sunucu tarafı yanıtı sıkıştırırsa, aşağıdaki HTTP başlığını ekler:

- **Content-Encoding:** x-i2p-gzip

Bu başlık yanıtta mevcut ise, HTTP istemci proxy'si bunu şeffaf bir şekilde açar. İstemci tarafı bu başlığı kaldırır ve yanıtı tarayıcıya göndermeden önce gunzip ile açar. HTTP katmanında yanıt sıkıştırılmamış olsa bile, I2CP katmanındaki temel gzip sıkıştırmasının hala mevcut olduğunu ve etkili olduğunu unutmayın.

Bu tasarım ve mevcut uygulama RFC 2616'yı çeşitli şekillerde ihlal ediyor:

- X-Accept-Encoding standart bir header değildir
- Her hop için dechunk/chunk yapmaz; chunking'i uçtan uca aktarır
- Transfer-Encoding header'ını uçtan uca aktarır
- Per-hop encoding belirtmek için Transfer-Encoding değil, Content-Encoding kullanır
- Content-Encoding ayarlandığında x-i2p gzipping'i yasaklar (ama muhtemelen bunu yapmak istemeyiz)
- Sunucu tarafı, dechunk-gzip-rechunk ve dechunk-gunzip-rechunk yapmak yerine sunucu tarafından gönderilen chunking'i gziplar
- Gziplenmiş içerik sonrasında chunk'lanmaz. RFC 2616, "identity" dışındaki tüm Transfer-Encoding'lerin chunk'lanmasını gerektirir.
- Gzip'in dışında (sonrasında) chunking olmadığı için, verinin sonunu bulmak daha zordur ve keepalive'ın herhangi bir uygulamasını zorlaştırır.
- RFC 2616, Transfer-Encoding mevcut olduğunda Content-Length'in gönderilmemesi gerektiğini söyler, ama biz gönderiyoruz. Spesifikasyon, Transfer-Encoding mevcut olduğunda Content-Length'i yok sayılmasını söyler, tarayıcılar da bunu yapar, bu yüzden bizim için çalışır.

Standartlara uyumlu hop-by-hop sıkıştırmanın geriye dönük uyumlu bir şekilde uygulanması için yapılacak değişiklikler, daha fazla araştırma gerektiren bir konudur. dechunk-gzip-rechunk'a yapılacak herhangi bir değişiklik, belki x-i2p-gzchunked gibi yeni bir kodlama türü gerektirecektir. Bu, Transfer-Encoding: gzip ile aynı olacaktır, ancak uyumluluk nedenleriyle farklı şekilde sinyallenmelidir. Herhangi bir değişiklik resmi bir teklif gerektirecektir.

#### Şeffaf İstek Sıkıştırması {#transparent-request-compression}

Desteklenmiyor, ancak POST işleminden fayda görebilir. I2CP katmanında hala temel gzip sıkıştırmasının mevcut olduğunu unutmayın.

#### Kalıcılık {#persistence}

İstemci ve sunucu proxy'leri şu anda üç hop'tan hiçbirinde (tarayıcı soketi, I2P soketi, sunucu soketi) RFC 2616 HTTP kalıcı soketlerini desteklememektedir. Her hop'ta Connection: close başlıkları enjekte edilir. Kalıcılığı uygulama değişiklikleri araştırılmaktadır. Bu değişiklikler standartlara uyumlu ve geriye dönük uyumlu olmalı ve resmi bir öneri gerektirmemelidir.

#### Pipelining {#pipelining}

İstemci ve sunucu proxy'leri şu anda RFC 2616 HTTP pipelining'i desteklememektedir ve bunu destekleme planı da bulunmamaktadır. Modern tarayıcılar proxy'ler üzerinden pipelining'i desteklemez çünkü çoğu proxy bunu doğru şekilde uygulayamaz.

#### Uyumluluk {#compatibility}

Proxy uygulamaları diğer taraftaki diğer uygulamalarla doğru şekilde çalışmalıdır. İstemci proxy'leri, sunucu tarafında HTTP-aware sunucu proxy'si olmaksızın (yani standart bir tunnel ile) çalışabilmelidir. Tüm uygulamalar x-i2p-gzip desteklemez.

#### Kullanıcı Ajanı {#user-agent}

Tunnel'ın bir outproxy kullanıp kullanmadığına bağlı olarak aşağıdaki User-Agent'ı ekleyecektir:

- *Outproxy:* **User-Agent:** Windows üzerinde güncel bir Firefox sürümünden user agent kullanır
- *Dahili I2P kullanımı:* **User-Agent:** MYOB/6.66 (AN/ON)

### IRC İstemcisi {#client-mode-irc}

Virgülle ayrılmış (", ") hedef listesinde belirtilen rastgele bir IRC sunucusuna bağlantı oluşturur. Anonimlik kaygıları nedeniyle yalnızca beyaz listeye alınmış bir IRC komut alt kümesine izin verilir.

Aşağıdaki izin listesi, IRC sunucusundan IRC istemcisine gelen komutlar içindir.

**İzin verilen liste:** - AUTHENTICATE - CAP - ERROR - H - JOIN - KICK - MODE - NICK - PART - PING - PROTOCTL - QUIT - TOPIC - WALLOPS

IRC istemcisinden IRC sunucusuna giden komutlar için de bir izin listesi bulunmaktadır. IRC yönetim komutlarının sayısının fazla olması nedeniyle oldukça büyüktür. Detaylar için IRCFilter.java kaynak koduna bakınız.

Giden filtre ayrıca tanımlayıcı bilgileri çıkarmak için aşağıdaki komutları da değiştirir: - NOTICE - PART - PING - PRIVMSG - QUIT - USER

### SOCKS 4/4a/5 {#client-mode-socks}

I2P router'ın SOCKS proxy olarak kullanılmasını sağlar.

### SOCKS IRC {#client-mode-socks-irc}

I2P router'ının [IRC](#client-mode-irc) istemci modu tarafından belirtilen komut beyaz listesi ile SOCKS proxy olarak kullanılmasını sağlar.

### CONNECT {#client-mode-connect}

Bir HTTP tunnel oluşturur ve genellikle SSL ve HTTPS için kullanılan bir TCP tunnel'ı kurmak için "CONNECT" HTTP istek yöntemini kullanır.

### Streamr {#client-mode-streamr}

Streamr istemci I2PTunnel'ına bağlı bir UDP sunucusu oluşturur. Streamr istemci tunnel'ı bir streamr sunucu tunnel'ına abone olacaktır.

![Streamr diyagramı](/images/I2PTunnel-streamr.png)

## Sunucu Modları {#server-modes}

### Standart {#server-mode-standard}

Açık bir TCP portu ile yerel ip:port adresine bir hedef oluşturur.

### HTTP {#server-mode-http}

Yerel bir HTTP sunucusu ip:port'una bir hedef oluşturur. Accept-encoding: x-i2p-gzip içeren istekler için gzip desteği sağlar, bu tür isteklerde Content-encoding: x-i2p-gzip ile yanıt verir.

HTTP sunucu proxy'si, bir web sitesi barındırmayı daha kolay ve güvenli hale getirmek ve istemci tarafında daha iyi bir kullanıcı deneyimi sağlamak için bir dizi hizmet sunar.

**İstek başlığı işleme:** - Başlık doğrulaması - Başlık sahtekarlığı koruması - Başlık boyutu kontrolleri - İsteğe bağlı inproxy ve kullanıcı-aracısı reddi - Web sunucusunun isteğin nereden geldiğini bilmesi için X-I2P başlıkları ekleme - Web sunucusu vhost'larını kolaylaştırmak için Host başlığı değiştirme - Bağlantıyı zorunlu kapatma: close - RFC uyumlu hop-by-hop başlık işleme ve çıkarma - Verimlilik için tüm başlıkları geçirmeden önce tamponlama

**DDoS koruması:** - POST kısıtlama - Zaman aşımı ve slowloris koruması - Tüm tunnel türleri için streaming'de ek kısıtlama uygulanır

**Response header işleme:** - Bazı gizlilik sorunlu başlıkların çıkarılması - Yanıtın sıkıştırılıp sıkıştırılmayacağına dair mime tipi ve diğer başlık kontrolü - Bağlantı kapatmayı zorla - RFC uyumlu hop-by-hop header işleme ve çıkarma - Verimlilik için tüm başlıkları geçirmeden önce tamponlama

**HTTP hata yanıtları:** - Birçok yaygın ve pek yaygın olmayan hata ile kısıtlama durumları için, böylece istemci tarafındaki kullanıcı ne olduğunu bilir

**Şeffaf yanıt sıkıştırması:** - Web sunucusu ve/veya I2CP katmanı sıkıştırabilir, ancak web sunucusu genellikle sıkıştırmaz ve I2CP de sıkıştırsa bile yüksek bir katmanda sıkıştırmak en verimlidir. HTTP sunucu proxy'si, yanıtları şeffaf bir şekilde sıkıştırmak için istemci tarafı proxy ile işbirliği içinde çalışır.

### HTTP Çift Yönlü {#server-mode-http-bidir}

*Kullanımdan Kaldırıldı*

Hem I2PTunnel HTTP Sunucusu hem de outproxy yetenekleri olmayan I2PTunnel HTTP istemcisi olarak çalışır. Örnek bir uygulama, istemci türü isteklerde bulunan bir web uygulaması veya tanı aracı olarak bir I2P Sitesini geri döngü testine tabi tutmak olabilir.

### IRC Sunucusu {#server-mode-irc}

Bir istemcinin kayıt sırasını filtreleyen ve istemcinin destination anahtarını IRC sunucusuna hostname olarak ileten bir destination oluşturur.

### Streamr {#server-mode-streamr}

Bir medya sunucusuna bağlanan UDP istemcisi oluşturulur. UDP İstemcisi bir Streamr server I2PTunnel ile eşleştirilir.
