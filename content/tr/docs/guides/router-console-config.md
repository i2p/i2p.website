---
title: "Router Konsolu Yapılandırma Kılavuzu"
description: "I2P Yönlendirici Konsolu'nu anlamak ve yapılandırmak için kapsamlı bir kılavuz"
slug: "router-console-config"
lastUpdated: "2025-11"
accurateFor: "2.10.0"
type: dokümanlar
---

Bu kılavuz, I2P Router Console'una ve yapılandırma sayfalarına genel bir bakış sunar. Her bölüm, sayfanın ne yaptığını ve ne için tasarlandığını açıklayarak I2P router'ınızı nasıl izleyip yapılandıracağınızı anlamanıza yardımcı olur.

## Yönlendirici Konsolu'na Erişim

I2P Router Console, I2P router'ınızı yönetmek ve izlemek için merkezi merkezdir. Varsayılan olarak, I2P router'ınız çalışırken [I2P Router Console](http://127.0.0.1:7657/home) adresinden erişilebilir.

![Router Console Ana Sayfa](/images/router-console-home.png)

Ana sayfa birkaç önemli bölüm görüntüler:

- **Uygulamalar** - E-posta, Torrent, Gizli Servisler Yöneticisi ve Web Sunucusu gibi yerleşik I2P uygulamalarına hızlı erişim
- **I2P Topluluk Siteleri** - Forum, dokümantasyon ve proje web siteleri dahil olmak üzere önemli topluluk kaynaklarına bağlantılar
- **Yapılandırma ve Yardım** - Bant genişliği ayarlarını yapılandırma, eklentileri yönetme ve yardım kaynaklarına erişim araçları
- **Ağ ve Geliştirici Bilgileri** - Grafiklere, günlüklere, teknik dokümantasyona ve ağ istatistiklerine erişim

## Adres Defteri

**URL:** [Adres Defteri](http://127.0.0.1:7657/dns)

![Router Console Address Book](/images/router-console-address-book.png)

I2P Adres Defteri, clearnet'teki DNS'e benzer şekilde çalışır ve I2P hedefleri (eepsite'lar) için insanlar tarafından okunabilir isimleri yönetmenize olanak tanır. Burası, kişisel adres defterinize I2P adreslerini görüntüleyip ekleyebileceğiniz yerdir.

Adres defteri sistemi birden fazla katman üzerinden çalışır:

- **Yerel Kayıtlar** - Yalnızca yönlendiricinizde saklanan kişisel adres defterleriniz
  - **Yerel Adres Defteri** - Manuel olarak eklediğiniz veya kendi kullanımınız için kaydettiğiniz hostlar
  - **Özel Adres Defteri** - Başkalarıyla paylaşmak istemediğiniz adresler; hiçbir zaman halka açık olarak dağıtılmaz

- **Abonelikler** - Router'ınızın adres defterini bilinen I2P siteleriyle otomatik olarak güncelleyen uzak adres defteri kaynakları (`http://i2p-projekt.i2p/hosts.txt` gibi)

- **Router Addressbook** - Yerel kayıtlarınız ve aboneliklerinizin birleştirilmiş sonucu, router'ınızdaki tüm I2P uygulamaları tarafından aranabilir

- **Yayınlanmış Adres Defteri** - Adres defterinizi başkalarının abonelik kaynağı olarak kullanması için isteğe bağlı olarak halka açık şekilde paylaşma (bir I2P sitesi çalıştırıyorsanız kullanışlıdır)

Adres defteri, aboneliklerinizi düzenli olarak kontrol eder ve içeriği yönlendirici adres defterinizle birleştirerek hosts.txt dosyanızı I2P ağıyla güncel tutar.

## Yapılandırma

**URL:** [Gelişmiş Yapılandırma](http://127.0.0.1:7657/configadvanced)

Yapılandırma bölümü, birden fazla özelleşmiş sekme aracılığıyla tüm router ayarlarına erişim sağlar.

### Advanced

![Router Console Gelişmiş Yapılandırma](/images/router-console-config-advanced.png)

Gelişmiş yapılandırma sayfası, normal çalışma için genellikle gerekli olmayan düşük seviyeli router ayarlarına erişim sağlar. **Çoğu kullanıcı, belirli bir yapılandırma seçeneğini ve bunun router davranışı üzerindeki etkisini anlamadıkça bu ayarları değiştirmemelidir.**

Temel özellikler:

- **Floodfill Yapılandırması** - Router'ınızın floodfill eşi olarak katılıp katılmayacağını kontrol eder. Bu, ağ veritabanı bilgilerini depolayıp dağıtarak ağa yardımcı olur. Daha fazla sistem kaynağı kullanabilir ancak I2P ağını güçlendirir.

- **Gelişmiş I2P Yapılandırması** - `router.config` dosyasına doğrudan erişim, şunlar dahil tüm gelişmiş yapılandırma parametrelerini gösterir:
  - Bant genişliği limitleri ve burst ayarları
  - Transport ayarları (NTCP2, SSU2, UDP portları ve anahtarlar)
  - Router tanımlama ve sürüm bilgisi
  - Konsol tercihleri ve güncelleme ayarları

En gelişmiş yapılandırma seçenekleri kullanıcı arayüzünde gösterilmez çünkü nadiren ihtiyaç duyulur. Bu ayarları düzenleyebilmek için `router.config` dosyanıza manuel olarak `routerconsole.advanced=true` eklemeniz gerekir.

**Uyarı:** Gelişmiş ayarları yanlış şekilde değiştirmek, router'ınızın performansını veya bağlantısını olumsuz etkileyebilir. Bu ayarları yalnızca ne yaptığınızı biliyorsanız değiştirin.

### Bandwidth

**URL:** [Bant Genişliği Yapılandırması](http://127.0.0.1:7657/config)

![Router Console Bant Genişliği Yapılandırması](/images/router-console-config-bandwidth.png)

Bant genişliği yapılandırma sayfası, yönlendiricinizin I2P ağına ne kadar bant genişliği katkıda bulunacağını kontrol etmenizi sağlar. I2P, hızlarınızı internet bağlantınızın hızıyla eşleşecek şekilde yapılandırdığınızda en iyi şekilde çalışır.

**Temel Ayarlar:**

- **KBps In** - Yönlendiricinizin kabul edeceği maksimum gelen bant genişliği (indirme hızı)
- **KBps Out** - Yönlendiricinizin kullanacağı maksimum giden bant genişliği (yükleme hızı)
- **Share** - Giden bant genişliğinizin katılımcı trafiğe ayrılan yüzdesi (başkalarının trafiğini yönlendirmeye yardımcı olma)

**Önemli Notlar:**

- Tüm değerler saniyede **bit** değil, saniyede **bayt** (KBps) cinsindendir
- Ne kadar çok bant genişliği sağlarsanız, ağa o kadar çok yardımcı olur ve kendi anonimliğinizi o kadar iyileştirirsiniz
- Yukarı akış paylaşım miktarınız (KBps Out), ağa genel katkınızı belirler
- Ağınızın hızından emin değilseniz, ölçmek için **Bandwidth Test** kullanın
- Daha yüksek paylaşım bant genişliği hem anonimliğinizi iyileştirir hem de I2P ağını güçlendirmeye yardımcı olur

Yapılandırma sayfası, ayarlarınıza göre tahmini aylık veri aktarımını gösterir ve internet planı limitelerinize göre bant genişliği tahsisini planlamanıza yardımcı olur.

### Client Configuration

**URL:** [İstemci Yapılandırması](http://127.0.0.1:7657/configclients)

![Router Console Client Yapılandırması](/images/router-console-config-clients.png)

İstemci Yapılandırması sayfası, başlangıçta hangi I2P uygulamalarının ve hizmetlerinin çalışacağını kontrol etmenize olanak tanır. Burası, yerleşik I2P istemcilerini kaldırmadan etkinleştirebileceğiniz veya devre dışı bırakabileceğiniz yerdir.

**Önemli Uyarı:** Buradaki ayarları değiştirirken dikkatli olun. Router konsolu ve uygulama tunnel'ları I2P'nin çoğu kullanımı için gereklidir. Yalnızca ileri düzey kullanıcılar bu ayarları değiştirmelidir.

**Mevcut İstemciler:**

- **Uygulama tünelleri** - İstemci ve sunucu tünellerini yöneten I2PTunnel sistemi (HTTP proxy, IRC, vb.)
- **I2P Router Konsolu** - Şu anda kullanmakta olduğunuz web tabanlı yönetim arayüzü
- **I2P web sunucusu (eepsite)** - Kendi I2P web sitenizi barındırmak için yerleşik Jetty web sunucusu
- **Başlangıçta Router Konsolu'nu web tarayıcısında aç** - Konsol ana sayfasını tarayıcınızda otomatik olarak başlatır
- **SAM uygulama köprüsü** - Üçüncü taraf uygulamaların I2P'ye bağlanması için API köprüsü

Her istemci şunları gösterir: - **Başlangıçta Çalıştır?** - Otomatik başlatmayı etkinleştirme/devre dışı bırakma onay kutusu - **Kontrol** - Anlık kontrol için Başlat/Durdur düğmeleri - **Sınıf ve argümanlar** - İstemcinin nasıl başlatıldığına dair teknik detaylar

"Başlangıçta Çalıştır?" ayarındaki değişikliklerin geçerli olması için router'ın yeniden başlatılması gerekir. Tüm değişiklikler `/var/lib/i2p/i2p-config/clients.config.d/` dizinine kaydedilir.

### İleri Düzey

**URL:** [I2CP Yapılandırması](http://127.0.0.1:7657/configi2cp)

![Router Console I2CP Yapılandırması](/images/router-console-config-i2cp.png)

I2CP (I2P Client Protocol) yapılandırma sayfası, harici uygulamaların I2P router'ınıza nasıl bağlanacağını yapılandırmanıza olanak tanır. I2CP, uygulamaların tunnel oluşturmak ve I2P üzerinden veri göndermek/almak için router ile iletişim kurmak için kullandığı protokoldür.

**Önemli:** Varsayılan ayarlar çoğu kullanıcı için yeterlidir. Burada yapılan değişikliklerin harici istemci uygulamasında da yapılandırılması gerekir. Birçok istemci SSL veya yetkilendirmeyi desteklemez. **Tüm değişikliklerin etkili olması için yeniden başlatma gerekir.**

**Yapılandırma Seçenekleri:**

- **Harici I2CP Arayüz Yapılandırması**
  - **SSL olmadan Etkin** - Standart I2CP erişimi (varsayılan ve en uyumlu)
  - **SSL zorunlu olarak Etkin** - Yalnızca şifrelenmiş I2CP bağlantıları
  - **Devre Dışı** - Harici istemcilerin I2CP üzerinden bağlanmasını engeller

- **I2CP Arayüzü** - Dinlenecek ağ arayüzü (varsayılan: yalnızca localhost için 127.0.0.1)
- **I2CP Portu** - I2CP bağlantıları için port numarası (varsayılan: 7654)

- **Yetkilendirme**
  - **Kullanıcı adı ve parola gerektir** - I2CP bağlantıları için kimlik doğrulamayı etkinleştir
  - **Kullanıcı adı** - I2CP erişimi için gerekli kullanıcı adını ayarla
  - **Parola** - I2CP erişimi için gerekli parolayı ayarla

**Güvenlik Notu:** I2P router'ınızla aynı makinede yalnızca uygulamalar çalıştırıyorsanız, uzaktan erişimi önlemek için arayüzü `127.0.0.1` olarak ayarlı tutun. Bu ayarları yalnızca diğer cihazlardan I2P uygulamalarının router'ınıza bağlanmasına izin vermeniz gerekiyorsa değiştirin.

### Bant Genişliği

**URL:** [Ağ Yapılandırması](http://127.0.0.1:7657/confignet)

![Router Console Network Yapılandırması](/images/router-console-config-network.png)

Ağ Yapılandırması sayfası, I2P router'ınızın internete nasıl bağlanacağını yapılandırmanıza olanak tanır; bu ayarlar IP adresi algılama, IPv4/IPv6 tercihleri ve hem UDP hem de TCP transport'ları için port ayarlarını içerir.

**Harici Olarak Erişilebilir IP Adresi:**

- **Tüm otomatik algılama yöntemlerini kullan** - Genel IP adresinizi birden fazla yöntem kullanarak otomatik olarak algılar (önerilir)
- **UPnP IP adresi algılamasını devre dışı bırak** - IP adresinizi keşfetmek için UPnP kullanımını engeller
- **Yerel arayüz IP adresini yoksay** - Yerel ağ IP adresinizi kullanmaz
- **Yalnızca SSU IP adresi algılamasını kullan** - IP algılama için yalnızca SSU2 aktarımını kullanır
- **Gizli mod - IP yayınlama** - Ağ trafiğine katılımı engeller (anonimliği azaltır)
- **Ana bilgisayar adı veya IP belirt** - Genel IP adresinizi veya ana bilgisayar adınızı manuel olarak ayarlar

**IPv4 Yapılandırması:**

- **Gelen bağlantıları devre dışı bırak (Güvenlik duvarı arkasında)** - Gelen bağlantıları engelleyen bir güvenlik duvarı, ev ağı, ISS, DS-Lite veya operatör sınıfı NAT arkasındaysanız bunu işaretleyin

**IPv6 Yapılandırması:**

- **IPv4'ü IPv6'ya Tercih Et** - IPv4 bağlantılarına öncelik verir
- **IPv6'yı IPv4'e Tercih Et** - IPv6 bağlantılarına öncelik verir (çift yığın ağları için varsayılan)
- **IPv6'yı Etkinleştir** - IPv6 bağlantılarına izin verir
- **IPv6'yı Devre Dışı Bırak** - Tüm IPv6 bağlantısını devre dışı bırakır
- **Yalnızca IPv6 Kullan (IPv4'ü devre dışı bırak)** - Deneysel yalnızca IPv6 modu
- **Gelen Bağlantıları Devre Dışı Bırak (Güvenlik Duvarı Arkasında)** - IPv6'nızın güvenlik duvarı arkasında olup olmadığını kontrol edin

**IP Değiştiğinde Yapılacak İşlem:**

- **Laptop modu** - IP adresiniz değiştiğinde gelişmiş anonimlik için router kimliğini ve UDP portunu değiştiren deneysel özellik

**UDP Yapılandırması:**

- **Port Belirtin** - SSU2 aktarımı için belirli bir UDP portu ayarlayın (güvenlik duvarınızda açılmalıdır)
- **Tamamen devre dışı bırak** - Yalnızca tüm giden UDP trafiğini engelleyen bir güvenlik duvarının arkasındaysanız seçin

**TCP Yapılandırması:**

- **Port Belirle** - NTCP2 taşıması için belirli bir TCP portu ayarla (güvenlik duvarınızda açılmalıdır)
- **UDP için yapılandırılan aynı portu kullan** - Her iki taşıma için tek bir port kullanarak yapılandırmayı basitleştirir
- **Otomatik algılanan IP adresini kullan** - Genel IP adresinizi otomatik olarak algılar (henüz algılanmadıysa veya güvenlik duvarı varsa "şu anda bilinmiyor" gösterir)
- **Her zaman otomatik algılanan IP adresini kullan (Güvenlik duvarı yok)** - Doğrudan internet erişimi olan router'lar için en iyisi
- **Gelen bağlantıları devre dışı bırak (Güvenlik duvarlı)** - TCP bağlantılarının güvenlik duvarınız tarafından engellenip engellenmediğini kontrol edin
- **Tamamen devre dışı bırak** - Yalnızca giden TCP'yi kısıtlayan veya engelleyen bir güvenlik duvarının arkasındaysanız seçin
- **Hostname veya IP belirle** - Dışarıdan erişilebilir adresinizi manuel olarak yapılandırın

**Önemli:** Ağ ayarlarındaki değişikliklerin tam olarak etkili olması için router'ın yeniden başlatılması gerekebilir. Doğru port yönlendirme yapılandırması, router'ınızın performansını önemli ölçüde artırır ve I2P ağına yardımcı olur.

### İstemci Yapılandırması

**URL:** [Eş Yapılandırması](http://127.0.0.1:7657/configpeer)

![Router Console Peer Configuration](/images/router-console-config-peer.png)

Peer Yapılandırma sayfası, I2P ağındaki bireysel peer'ları yönetmek için manuel kontroller sağlar. Bu, genellikle yalnızca sorunlu peer'lar için sorun giderme amacıyla kullanılan gelişmiş bir özelliktir.

**Manuel Eş Kontrolleri:**

- **Router Hash** - Yönetmek istediğiniz eşin 44 karakterlik base64 router hash değerini girin

**Bir Eş Sunucuyu Manuel Olarak Yasaklama / Yasağı Kaldırma:**

Bir peer'ı yasaklamak, oluşturduğunuz tünellere katılmalarını engeller. Bu işlem: - Peer'ın istemci veya keşif tünellerinizde kullanılmasını engeller - Yeniden başlatma gerektirmeden hemen etkili olur - Peer'ı manuel olarak yasaktan kaldırana veya router'ınızı yeniden başlatana kadar devam eder - **Yeniden başlatana kadar peer'ı yasakla** - Peer'ı geçici olarak engeller - **Peer yasakını kaldır** - Daha önce engellenmiş bir peer üzerindeki yasaklamayı kaldırır

**Profil Bonuslarını Ayarlama:**

Profil bonusları, tünele katılım için eşlerin nasıl seçildiğini etkiler. Bonuslar pozitif veya negatif olabilir: - **Hızlı eşler** - Yüksek hız gerektiren istemci tünelleri için kullanılır - **Yüksek Kapasite eşleri** - Güvenilir yönlendirme gerektiren bazı keşif tünelleri için kullanılır - Mevcut bonuslar profiller sayfasında görüntülenir

**Yapılandırma:** - **Hız** - Bu eş için hız bonusunu ayarlayın (0 = nötr) - **Kapasite** - Bu eş için kapasite bonusunu ayarlayın (0 = nötr) - **Eş bonuslarını ayarla** - Bonus ayarlarını uygula

**Kullanım Senaryoları:** - Sürekli bağlantı sorunlarına neden olan bir peer'ı yasaklayın - Kötü niyetli olduğundan şüphelendiğiniz bir peer'ı geçici olarak hariç tutun - Düşük performanslı peer'ları öncelikten düşürmek için bonusları ayarlayın - Belirli peer'ları hariç tutarak tünel oluşturma sorunlarını giderin

**Not:** Çoğu kullanıcının bu özelliği kullanmasına hiç gerek kalmayacaktır. I2P router, performans metriklerine dayalı olarak peer seçimini ve profillemeyi otomatik olarak yönetir.

### I2CP Yapılandırması

**URL:** [Reseed Yapılandırması](http://127.0.0.1:7657/configreseed)

![Router Console Reseed Yapılandırması](/images/router-console-config-reseed.png)

Reseed Yapılandırma sayfası, otomatik reseed işlemi başarısız olursa router'ınızı manuel olarak reseed etmenize olanak tanır. Reseed, I2P'yi ilk kurduğunuzda veya router'ınızda çok az router referansı kaldığında diğer router'ları bulmak için kullanılan başlatma sürecidir.

**Manuel Reseed Ne Zaman Kullanılır:**

1. Yeniden tohumlama başarısız olduysa, öncelikle ağ bağlantınızı kontrol etmelisiniz
2. Bir güvenlik duvarı yeniden tohumlama sunucularına bağlantılarınızı engelliyorsa, bir proxy'ye erişiminiz olabilir:
   - Proxy uzak bir genel proxy olabilir veya bilgisayarınızda (localhost) çalışıyor olabilir
   - Bir proxy kullanmak için Yeniden Tohumlama Yapılandırması bölümünde türü, sunucuyu ve bağlantı noktasını yapılandırın
   - Tor Browser çalıştırıyorsanız, SOCKS 5, localhost, port 9150 yapılandırarak onun üzerinden yeniden tohumlama yapın
   - Komut satırı Tor çalıştırıyorsanız, SOCKS 5, localhost, port 9050 yapılandırarak onun üzerinden yeniden tohumlama yapın
   - Bazı eşleriniz varsa ancak daha fazlasına ihtiyacınız varsa, I2P Outproxy seçeneğini deneyebilirsiniz. Sunucu ve port alanlarını boş bırakın. Bu, hiç eşiniz olmadığında ilk yeniden tohumlama için çalışmayacaktır
   - Ardından, "Değişiklikleri kaydet ve şimdi yeniden tohumla" düğmesine tıklayın
   - Varsayılan ayarlar çoğu kişi için çalışacaktır. Bunları yalnızca HTTPS kısıtlayıcı bir güvenlik duvarı tarafından engelleniyorsa ve yeniden tohumlama başarısız olduysa değiştirin

3. I2P çalıştıran ve güvendiğiniz birini tanıyorsanız, router konsolundaki bu sayfayı kullanarak oluşturulmuş bir reseed dosyası göndermelerini isteyin. Ardından, aldığınız dosyayla reseed yapmak için bu sayfayı kullanın. İlk olarak, aşağıdan dosyayı seçin. Sonra, "Reseed from file" üzerine tıklayın

4. Reseed dosyalarını yayınlayan güvendiğiniz birini tanıyorsanız, onlara URL'yi sorun. Ardından, aldığınız URL ile reseed yapmak için bu sayfayı kullanın. İlk olarak, aşağıya URL'yi girin. Sonra, "Reseed from URL" düğmesine tıklayın

5. Manuel olarak yeniden seed işlemi için [SSS](/docs/overview/faq/) bölümüne bakın

**Manuel Reseed Seçenekleri:**

- **URL'den Yeniden Tohum** - Güvenilir bir kaynaktan zip veya su3 URL'si girin ve "URL'den Yeniden Tohum"a tıklayın
  - su3 formatı tercih edilir, çünkü güvenilir bir kaynak tarafından imzalandığı doğrulanacaktır
  - zip formatı imzasızdır; zip dosyasını yalnızca güvendiğiniz bir kaynaktan kullanın

- **Dosyadan Yeniden Tohum** - Yerel bir zip veya su3 dosyasına göz atın ve seçin, ardından "Dosyadan yeniden tohum" düğmesine tıklayın
  - Yeniden tohum dosyalarını [checki2p.com/reseed](https://checki2p.com/reseed) adresinde bulabilirsiniz

- **Reseed Dosyası Oluştur** - Başkalarının manuel olarak reseed yapması için paylaşabileceğiniz yeni bir reseed zip dosyası oluşturun
  - Bu dosya asla kendi router'ınızın kimliğini veya IP'sini içermeyecektir

**Reseeding Yapılandırması:**

Varsayılan ayarlar çoğu kullanıcı için çalışacaktır. Bunları yalnızca HTTPS kısıtlayıcı bir güvenlik duvarı tarafından engelleniyorsa ve reseed başarısız olmuşsa değiştirin.

- **Reseed URL'leri** - Reseed sunucularına ait HTTPS URL listesi (varsayılan liste yerleşik olarak gelir ve düzenli olarak güncellenir)
- **Proxy Yapılandırması** - Reseed sunucularına bir proxy üzerinden erişmeniz gerekiyorsa HTTP/HTTPS/SOCKS proxy yapılandırın
- **URL listesini sıfırla** - Varsayılan reseed sunucu listesini geri yükle

**Önemli:** Manuel yeniden tohum ekleme yalnızca otomatik yeniden tohum eklemenin tekrar tekrar başarısız olduğu nadir durumlarda gerekli olmalıdır. Çoğu kullanıcının bu sayfayı kullanmasına hiç gerek olmayacaktır.

### Ağ Yapılandırması

**URL:** [Router Family Yapılandırması](http://127.0.0.1:7657/configfamily)

![Router Console Router Family Configuration](/images/router-console-config-family.png)

Router Family Configuration sayfası, router ailelerini yönetmenize olanak tanır. Aynı ailedeki routerlar bir family key (aile anahtarı) paylaşır ve bu onları aynı kişi veya kuruluş tarafından işletildiğini belirtir. Bu, kontrol ettiğiniz birden fazla routerın aynı tunnel için seçilmesini önler, aksi takdirde anonimlik azalır.

**Router Family Nedir?**

Birden fazla I2P router işlettiğinizde, bunları aynı ailenin parçası olacak şekilde yapılandırmalısınız. Bu şunları sağlar: - Router'larınız aynı tunnel yolunda birlikte kullanılmaz - Diğer kullanıcılar, tunnel'ları sizin router'larınızı kullandığında uygun anonimliği korur - Ağ, tunnel katılımını düzgün bir şekilde dağıtabilir

**Mevcut Aile:**

Bu sayfa mevcut router ailenizin adını gösterir. Bir ailenin parçası değilseniz, bu alan boş olacaktır.

**Aile Anahtarını Dışa Aktar:**

- **Kontrol ettiğiniz diğer yönlendiricilere aktarılmak üzere gizli aile anahtarını dışa aktarın**
- Aile anahtarı dosyanızı indirmek için "Export Family Key" düğmesine tıklayın
- Aynı aileye eklemek için bu anahtarı diğer yönlendiricilerinize aktarın

**Router Ailesinden Ayrıl:**

- **Artık ailenin bir üyesi olmayın**
- Bu yönlendiriciyi mevcut ailesinden çıkarmak için "Aileden Ayrıl"a tıklayın
- Bu işlem, aile anahtarı yeniden içe aktarılmadan geri alınamaz

**Önemli Hususlar:**

- **Genel Kayıt Gereklidir:** Ailenizin ağ genelinde tanınması için, aile anahtarınızın I2P geliştirme ekibi tarafından I2P kod tabanına eklenmesi gerekir. Bu, ağdaki tüm router'ların aileniz hakkında bilgi sahibi olmasını sağlar.
- Birden fazla genel router işletiyorsanız, aile anahtarınızı kaydetmek için **I2P ekibiyle iletişime geçin**
- Yalnızca bir router çalıştıran kullanıcıların çoğunun bu özelliği kullanmasına hiç gerek olmayacaktır
- Aile yapılandırması öncelikli olarak birden fazla genel router işleten operatörler veya altyapı sağlayıcıları tarafından kullanılır

**Kullanım Senaryoları:**

- Yedeklilik için birden fazla I2P router çalıştırma
- Birden fazla makinede reseed sunucuları veya outproxy'ler gibi altyapı çalıştırma
- Bir organizasyon için I2P router ağı yönetimi

### Eş Yapılandırması

**URL:** [Tünel Yapılandırması](http://127.0.0.1:7657/configtunnels)

![Router Console Tunnel Yapılandırması](/images/router-console-config-tunnels.png)

Tünel Yapılandırması sayfası, hem keşif tünelleri (router iletişimi için kullanılır) hem de istemci tünelleri (uygulamalar tarafından kullanılır) için varsayılan tünel ayarlarını düzenlemenize olanak tanır. **Varsayılan ayarlar çoğu kişi için çalışır ve yalnızca ödünleşimleri anlıyorsanız değiştirilmelidir.**

**Önemli Uyarılar:**

⚠️ **Anonimlik ile Performans Dengesi:** Anonimlik ve performans arasında temel bir denge vardır. 3 hop'tan uzun tüneller (örneğin 2 hop + 0-2 hop, 3 hop + 0-1 hop, 3 hop + 0-2 hop) veya yüksek miktar + yedek miktar, performansı veya güvenilirliği ciddi şekilde azaltabilir. Yüksek CPU ve/veya yüksek giden bant genişliği kullanımı ortaya çıkabilir. Bu ayarları dikkatle değiştirin ve sorun yaşarsanız ayarlayın.

⚠️ **Kalıcılık:** Keşif tüneli ayar değişiklikleri router.config dosyasında saklanır. İstemci tüneli değişiklikleri geçicidir ve kaydedilmez. Kalıcı istemci tüneli değişiklikleri yapmak için [I2PTunnel sayfasına](/docs/api/i2ptunnel) bakın.

**Keşif Tünelleri:**

Keşif tünelleri, yönlendiriciniz tarafından ağ veritabanıyla iletişim kurmak ve I2P ağına katılmak için kullanılır.

Hem Inbound hem de Outbound için yapılandırma seçenekleri: - **Length** - Tüneldeki hop sayısı (varsayılan: 2-3 hop) - **Randomization** - Tünel uzunluğundaki rastgele varyans (varsayılan: 0-1 hop) - **Quantity** - Aktif tünel sayısı (varsayılan: 2 tünel) - **Backup quantity** - Etkinleştirilmeye hazır yedek tünel sayısı (varsayılan: 0 tünel)

**I2P Web Sunucusu için İstemci Tünelleri:**

Bu ayarlar, yerleşik I2P web sunucusu (eepsite) için tünelleri kontrol eder.

⚠️ **ANONİMLİK UYARISI** - Ayarlar 1-hop tunnel'ları içeriyor. ⚠️ **PERFORMANS UYARISI** - Ayarlar yüksek tunnel miktarları içeriyor.

Hem Gelen hem de Giden için yapılandırma seçenekleri: - **Uzunluk** - Tunnel uzunluğu (varsayılan: web sunucusu için 1 hop) - **Rastgeleleştirme** - Tunnel uzunluğunda rastgele değişkenlik - **Miktar** - Aktif tunnel sayısı - **Yedek miktar** - Yedek tunnel sayısı

**Paylaşımlı İstemciler için İstemci Tünelleri:**

Bu ayarlar paylaşımlı istemci uygulamaları için geçerlidir (HTTP proxy, IRC, vb.).

Hem Gelen hem de Giden bağlantılar için yapılandırma seçenekleri: - **Uzunluk** - Tünel uzunluğu (varsayılan: 3 atlama) - **Rastgeleleştirme** - Tünel uzunluğunda rastgele değişkenlik - **Miktar** - Aktif tünel sayısı - **Yedek miktar** - Yedek tünel sayısı

**Tünel Parametrelerini Anlamak:**

- **Uzunluk:** Daha uzun tüneller daha fazla anonimlik sağlar ancak performansı ve güvenilirliği azaltır
- **Rastgeleleştirme:** Tünel yollarına öngörülemezlik ekleyerek güvenliği artırır
- **Miktar:** Daha fazla tünel güvenilirliği ve yük dağılımını iyileştirir ancak kaynak kullanımını artırır
- **Yedek miktarı:** Başarısız tünelleri değiştirmeye hazır önceden oluşturulmuş tüneller, dayanıklılığı artırır

**En İyi Uygulamalar:**

- Özel ihtiyaçlarınız yoksa varsayılan ayarları koruyun
- Tunnel uzunluğunu yalnızca anonimlik kritik önemdeyse ve daha yavaş performansı kabul edebiliyorsanız artırın
- Sık tunnel arızaları yaşıyorsanız miktar/yedeklemeyi artırın
- Değişiklik yaptıktan sonra router performansını izleyin
- Değişiklikleri uygulamak için "Değişiklikleri kaydet"e tıklayın

### Reseed Yapılandırması

**URL:** [Arayüz Yapılandırması](http://127.0.0.1:7657/configui)

![Router Console UI Yapılandırması](/images/router-console-config-ui.png)

UI Yapılandırma sayfası, tema seçimi, dil tercihleri ve parola koruması dahil olmak üzere router konsolunuzun görünümünü ve erişilebilirliğini özelleştirmenize olanak tanır.

**Router Konsolu Teması:**

Router konsolu arayüzü için karanlık ve aydınlık temalar arasından seçim yapın: - **Dark** - Karanlık mod teması (düşük ışıklı ortamlarda gözler için daha rahat) - **Light** - Aydınlık mod teması (geleneksel görünüm)

Ek tema seçenekleri: - **Temayı tüm uygulamalarda evrensel olarak ayarla** - Seçilen temayı sadece router konsolu için değil, tüm I2P uygulamaları için uygula - **Mobil konsolun kullanılmasını zorla** - Masaüstü tarayıcılarda bile mobil için optimize edilmiş arayüzü kullan - **E-posta ve Torrent uygulamalarını konsola göm** - Susimail ve I2PSnark'ı ayrı sekmelerde açmak yerine doğrudan konsol arayüzüne entegre et

**Router Konsolu Dili:**

Router konsolu arayüzü için tercih ettiğiniz dili açılır menüden seçin. I2P, İngilizce, Almanca, Fransızca, İspanyolca, Rusça, Çince, Japonca ve daha fazlası dahil olmak üzere birçok dili destekler.

**Çeviri katkıları bekliyoruz:** Eksik veya hatalı çeviriler fark ederseniz, çeviri projesine katkıda bulunarak I2P'yi geliştirmeye yardımcı olabilirsiniz. IRC'de #i2p-dev kanalındaki geliştiricilerle iletişime geçin veya çeviri durum raporunu kontrol edin (sayfada bağlantısı bulunmaktadır).

**Router Konsolu Parolası:**

Router konsolunuza erişimi korumak için kullanıcı adı ve parola kimlik doğrulaması ekleyin:

- **Kullanıcı Adı** - Konsol erişimi için kullanıcı adını girin
- **Parola** - Konsol erişimi için parolayı girin
- **Kullanıcı ekle** - Belirtilen kimlik bilgileriyle yeni bir kullanıcı oluşturun
- **Seçileni sil** - Mevcut kullanıcı hesaplarını kaldırın

**Neden Şifre Eklemeliyim?**

- Yönlendirici konsolunuza yetkisiz yerel erişimi önler
- Bilgisayarınızı birden fazla kişi kullanıyorsa gereklidir
- Yönlendirici konsolunuz yerel ağınızda erişilebilir durumdaysa önerilir
- I2P yapılandırmanızı ve gizlilik ayarlarınızı değiştirilmeye karşı korur

**Güvenlik Notu:** Şifre koruması yalnızca [I2P Router Console](http://127.0.0.1:7657) adresindeki router console web arayüzüne erişimi etkiler. I2P trafiğini şifrelemez veya uygulamaların I2P kullanmasını engellemez. Bilgisayarınızın tek kullanıcısıysanız ve router console yalnızca localhost'ta dinliyorsa (varsayılan), bir şifre gerekli olmayabilir.

### Yönlendirici Ailesi Yapılandırması

**URL:** [WebApp Yapılandırması](http://127.0.0.1:7657/configwebapps)

![Router Console WebApp Yapılandırması](/images/router-console-config-webapps.png)

WebApp Yapılandırma sayfası, I2P router'ınız içinde çalışan Java web uygulamalarını yönetmenize olanak tanır. Bu uygulamalar webConsole istemcisi tarafından başlatılır ve router ile aynı JVM'de çalışarak router konsolu üzerinden erişilebilen entegre işlevsellik sağlar.

**WebApps Nedir?**

WebApp'ler, aşağıdakilerden biri olabilen Java tabanlı uygulamalardır: - **Tam uygulamalar** (örn. torrent'ler için I2PSnark) - **Ayrıca etkinleştirilmesi gereken diğer istemcilerin ön yüzleri** (örn. Susidns, I2PTunnel) - **Web arayüzü olmayan web uygulamaları** (örn. adres defteri)

**Önemli Notlar:**

- Bir webapp tamamen devre dışı bırakılabilir veya yalnızca başlangıçta çalışması engellenebilir
- webapps dizininden bir war dosyasının kaldırılması webapp'i tamamen devre dışı bırakır
- Ancak .war dosyası ve webapp dizini, router'ınızı daha yeni bir sürüme güncellediğinizde yeniden görünecektir
- **Bir webapp'i kalıcı olarak devre dışı bırakmak için:** Tercih edilen yöntem olan burada devre dışı bırakın

**Mevcut Web Uygulamaları:**

| WebApp | Description |
|--------|-------------|
| **i2psnark** | Torrents - Built-in BitTorrent client for I2P |
| **i2ptunnel** | Hidden Services Manager - Configure client and server tunnels |
| **imagegen** | Identification Image Generator - Creates unique identicons |
| **jsonrpc** | jsonrpc.war - JSON-RPC API interface (disabled by default) |
| **routerconsole** | I2P Router Console - The main administrative interface |
| **susidns** | Address Book - Manage I2P addresses and subscriptions |
| **susimail** | Email - Web-based email client for I2P |
**Kontroller:**

Her bir webapp için: - **Başlangıçta Çalıştır?** - Otomatik başlatmayı etkinleştirmek/devre dışı bırakmak için onay kutusu - **Kontrol** - Anlık kontrol için Başlat/Durdur düğmeleri   - **Durdur** - Çalışmakta olan webapp'i durdurur   - **Başlat** - Durdurulmuş bir webapp'i başlatır

**Yapılandırma Düğmeleri:**

- **İptal** - Değişiklikleri iptal et ve önceki sayfaya dön
- **WebApp Yapılandırmasını Kaydet** - Değişikliklerinizi kaydedin ve uygulayın

**Kullanım Senaryoları:**

- Torrent kullanmıyorsanız kaynak tasarrufu için I2PSnark'ı durdurun
- API erişimine ihtiyacınız yoksa jsonrpc'yi devre dışı bırakın
- Harici bir e-posta istemcisi kullanıyorsanız Susimail'i durdurun
- Belleği boşaltmak veya sorunları gidermek için webapps'i geçici olarak durdurun

**Performans İpucu:** Kullanılmayan web uygulamalarını devre dışı bırakmak, özellikle düşük kaynaklı sistemlerde bellek kullanımını azaltabilir ve router performansını iyileştirebilir.

## Help

**URL:** [Yardım](http://127.0.0.1:7657/help)

Yardım sayfası, I2P'yi etkili bir şekilde anlamanıza ve kullanmanıza yardımcı olacak kapsamlı dokümantasyon ve kaynaklar sağlar. Sorun giderme, öğrenme ve destek alma için merkezi bir merkez görevi görür.

**Bulacaklarınız:**

- **Hızlı Başlangıç Kılavuzu** - I2P'ye yeni başlayan kullanıcılar için temel bilgiler
- **Sıkça Sorulan Sorular (SSS)** - I2P kurulumu, yapılandırması ve kullanımı hakkında yaygın soruların cevapları
- **Sorun Giderme** - Yaygın sorunlara ve bağlantı hatalarına yönelik çözümler
- **Teknik Dokümantasyon** - I2P protokolleri, mimarisi ve teknik özellikleri hakkında detaylı bilgiler
- **Uygulama Kılavuzları** - Torrent, e-posta ve gizli servisler gibi I2P uygulamalarının kullanım talimatları
- **Ağ Bilgileri** - I2P'nin nasıl çalıştığını ve onu güvenli kılan özellikleri anlama
- **Destek Kaynakları** - Forum, IRC kanalları ve topluluk desteği bağlantıları

**Yardım Alma:**

I2P ile ilgili sorun yaşıyorsanız: 1. Sık sorulan sorular ve cevaplar için SSS'ye bakın 2. Özel probleminiz için sorun giderme bölümünü inceleyin 3. [i2pforum.i2p](http://i2pforum.i2p) veya [i2pforum.net](https://i2pforum.net) adresindeki I2P forumunu ziyaret edin 4. Gerçek zamanlı topluluk desteği için #i2p IRC kanalına katılın 5. Detaylı teknik bilgi için dokümantasyonda arama yapın

**İpucu:** Yardım sayfasına router konsolunun kenar çubuğundan her zaman erişilebilir, bu sayede ihtiyacınız olduğunda yardım bulmak kolaydır.

## Performance Graphs

**URL:** [Performans Grafikleri](http://127.0.0.1:7657/graphs)

![Router Console Performans Grafikleri](/images/router-console-graphs.png)

Performans Grafikleri sayfası, I2P router'ınızın performansının ve ağ etkinliğinin gerçek zamanlı görsel izlemesini sağlar. Bu grafikler bant genişliği kullanımını, eş bağlantılarını, bellek tüketimini ve genel router sağlığını anlamanıza yardımcı olur.

**Mevcut Grafikler:**

- **Bant Genişliği Kullanımı**
  - **Düşük seviye gönderme hızı (bayt/saniye)** - Giden trafik hızı
  - **Düşük seviye alma hızı (bayt/saniye)** - Gelen trafik hızı
  - Mevcut, ortalama ve maksimum bant genişliği kullanımını gösterir
  - Yapılandırılmış bant genişliği limitinize yaklaşıp yaklaşmadığınızı izlemenize yardımcı olur

- **Aktif Eşler**
  - **router.activePeers 60 saniyelik ortalama** - Aktif olarak iletişim kurduğunuz eş sayısı
  - Ağ bağlantınızın sağlığını gösterir
  - Daha fazla aktif eş genellikle daha iyi tunnel oluşturma ve ağ katılımı anlamına gelir

- **Router Bellek Kullanımı**
  - **router.memoryUsed averaged for 60 sec** - JVM bellek tüketimi
  - Mevcut, ortalama ve maksimum bellek kullanımını MB cinsinden gösterir
  - Bellek sızıntılarını tespit etmek veya Java heap boyutunu artırmanız gerekip gerekmediğini belirlemek için kullanışlıdır

**Grafik Görünümünü Yapılandır:**

Grafiklerin nasıl görüntüleneceğini ve yenileneceğini özelleştirin:

- **Grafik boyutu** - Genişlik (varsayılan: 400 piksel) ve yükseklik (varsayılan: 100 piksel) ayarlayın
- **Görüntüleme dönemi** - Görüntülenecek zaman aralığı (varsayılan: 60 dakika)
- **Yenileme gecikmesi** - Grafiklerin ne sıklıkla güncelleneceği (varsayılan: 5 dakika)
- **Grafik türü** - Ortalamalar veya Olaylar görünümü arasından seçim yapın
- **Göstergeyi gizle** - Yer kazanmak için göstergeyi grafiklerden kaldırın
- **UTC** - Grafiklerde yerel saat yerine UTC saatini kullanın
- **Kalıcılık** - Geçmiş analizi için grafik verilerini diskte saklayın

**Gelişmiş Seçenekler:**

Hangi istatistiklerin grafikleneceğini seçmek için **[Select Stats]** düğmesine tıklayın: - Tunnel metrikleri (oluşturma başarı oranı, tunnel sayısı, vb.) - Network database istatistikleri - Transport istatistikleri (NTCP2, SSU2) - Client tunnel performansı - Ve çok daha fazla detaylı metrik

**Kullanım Alanları:**

- Yapılandırılmış limitlerini aşmadığınızdan emin olmak için bant genişliğini izleyin
- Ağ sorunlarını giderirken eş bağlantısını doğrulayın
- Java heap ayarlarını optimize etmek için bellek kullanımını takip edin
- Zaman içindeki performans kalıplarını belirleyin
- Grafikleri ilişkilendirerek tunnel oluşturma sorunlarını teşhis edin

**İpucu:** Değişikliklerinizi uygulamak için yapılandırmanızı yaptıktan sonra "Ayarları kaydet ve grafikleri yeniden çiz" düğmesine tıklayın. Grafikler, yenileme gecikmesi ayarınıza göre otomatik olarak güncellenecektir.
