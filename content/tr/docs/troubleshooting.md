---
title: "I2P Router Sorun Giderme Kılavuzu"
description: "Bağlantı, performans ve yapılandırma problemleri de dahil olmak üzere yaygın I2P router sorunları için kapsamlı bir sorun giderme kılavuzu"
slug: "troubleshooting"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

I2P router'ları en yaygın olarak **port yönlendirme sorunları**, **yetersiz bant genişliği tahsisi** ve **yetersiz bootstrap (ağa ilk katılım/önyükleme) süresi** nedeniyle başarısız olur. Bu üç etmen, bildirilen sorunların %70'inden fazlasını oluşturur. Router'ın ağa tam olarak entegre olabilmesi için başlatıldıktan sonra en az **10-15 dakika**, **en az 128 KB/sn bant genişliği** (önerilen 256 KB/sn) ve güvenlik duvarı arkasında olmama durumuna ulaşmak için uygun **UDP/TCP port yönlendirmesi** gerekir. Yeni kullanıcılar çoğu zaman anında bağlantı bekler ve router'ı erken yeniden başlatır; bu, entegrasyon ilerlemesini sıfırlar ve can sıkıcı bir kısır döngü yaratır. Bu kılavuz, 2.10.0 ve sonraki sürümleri etkileyen başlıca I2P sorunlarının tümü için ayrıntılı çözümler sunar.

I2P'nin anonimlik mimarisi, doğası gereği, çok atlamalı şifreli tunnel kullanımı aracılığıyla gizlilik için hızdan ödün verir. Bu temel tasarımı anlamak, kullanıcıların normal davranışları sorun sanmak yerine gerçekçi beklentiler belirlemelerine ve etkili biçimde sorun gidermelerine yardımcı olur.

## Router başlamıyor veya hemen çöküyor

En yaygın başlatma başarısızlıkları, **port çakışmalarından**, **Java sürüm uyumsuzluğundan** veya **bozulmuş yapılandırma dosyalarından** kaynaklanır. Daha derin sorunları araştırmaya başlamadan önce başka bir I2P örneğinin zaten çalışıp çalışmadığını kontrol edin.

**Çakışan süreçlerin olmadığını doğrulayın:**

Linux: `ps aux | grep i2p` veya `netstat -tulpn | grep 7657`

Windows: Görev Yöneticisi → Ayrıntılar → komut satırında i2p geçen java.exe'yi arayın

macOS: Etkinlik Monitörü → "i2p" ifadesini arayın

Bir zombie process (zombi süreç) varsa, onu sonlandırın: `pkill -9 -f i2p` (Linux/Mac) veya `taskkill /F /IM javaw.exe` (Windows)

**Java sürüm uyumluluğunu kontrol edin:**

I2P 2.10.0+ **en az Java 8** gerektirir; Java 11 veya daha yenisi önerilir. Kurulumunuzda "mixed mode" ("interpreted mode" değil) ibaresinin göründüğünü doğrulayın:

```bash
java -version
```
Şunu göstermelidir: OpenJDK veya Oracle Java, sürüm 8+, "mixed mode"

**Kaçının:** GNU GCJ, güncel olmayan Java gerçeklemeleri, yalnızca yorumlayıcı modlar

**Yaygın port çakışmaları**, birden çok servis I2P'nin varsayılan portları için yarıştığında ortaya çıkar. router konsolu (7657), I2CP (7654), SAM (7656) ve HTTP proxy (4444) portlarının boşta olması gerekir. Çakışmaları kontrol edin: `netstat -ano | findstr "7657 4444 7654"` (Windows) veya `lsof -i :7657,4444,7654` (Linux/Mac).

**Yapılandırma dosyası bozulması**, günlüklerdeki ayrıştırma hatalarıyla birlikte anında çökmeler olarak kendini gösterir. Router.config, **BOM (Bayt Sırası İmi) olmadan UTF-8 kodlaması** gerektirir, `=` işaretini ayırıcı olarak kullanır (`:` değil) ve bazı özel karakterlere izin vermez. Önce yedekleyin, sonra inceleyin: `~/.i2p/router.config` (Linux), `%LOCALAPPDATA%\I2P\router.config` (Windows), `~/Library/Application Support/i2p/router.config` (macOS).

Kimliği koruyarak yapılandırmayı sıfırlamak için: I2P'yi durdurun, router.keys ve keyData dizinini yedekleyin, router.config dosyasını silin, yeniden başlatın. router varsayılan yapılandırmayı yeniden oluşturur.

**Java yığın tahsisi çok düşük** OutOfMemoryError çökmelerine neden olur. wrapper.config dosyasını düzenleyin ve `wrapper.java.maxmemory` değerini varsayılan 128 veya 256'dan **en az 512**'ye yükseltin (yüksek bant genişlikli router'lar için 1024). Bu, tamamen kapatmayı, 11 dakika beklemeyi ve ardından yeniden başlatmayı gerektirir - konsolda "Restart" düğmesine tıklamak değişikliği uygulamaz.

## "Network: Firewalled" durumunu gidermek

Firewalled durumu, router'ın doğrudan gelen bağlantıları kabul edemediği ve introducers (aracı düğümler) üzerine bağımlı kalmak zorunda olduğu anlamına gelir. Router bu durumda çalışsa da, **performans önemli ölçüde düşer** ve ağa katkısı asgari düzeyde kalır. Firewalled olmayan duruma ulaşmak için doğru port yönlendirmesi gereklidir.

**router rastgele bir bağlantı noktası seçer**; iletişim için 9000-31000 aralığında. Bağlantı noktanızı http://127.0.0.1:7657/confignet adresinde bulun - "UDP Port" ve "TCP Port" ifadelerini arayın (genellikle aynı numara). En iyi performans için **hem UDP hem de TCP**'yi yönlendirmeniz gerekir; ancak yalnızca UDP temel işlevselliği sağlar.

**UPnP otomatik port yönlendirmeyi etkinleştirin** (en basit yöntem):

1. http://127.0.0.1:7657/confignet adresine gidin
2. "Enable UPnP" seçeneğini işaretleyin
3. Değişiklikleri kaydedin ve router'ı yeniden başlatın
4. 5-10 dakika bekleyin ve durumun "Network: Firewalled"dan "Network: OK"ye değiştiğini doğrulayın

UPnP, router desteği (2010'dan sonra üretilen tüketici router'larının çoğunda varsayılan olarak etkin) ve uygun ağ yapılandırması gerektirir.

**Manuel port yönlendirme** (UPnP başarısız olduğunda gereklidir):

1. http://127.0.0.1:7657/confignet adresinden I2P bağlantı noktanızı not alın (örn. 22648)
2. Yerel IP adresinizi bulun: `ipconfig` (Windows), `ip addr` (Linux), Sistem Tercihleri → Ağ (macOS)
3. router'ın yönetim arayüzüne erişin (genellikle 192.168.1.1 veya 192.168.0.1)
4. Port Yönlendirme'ye gidin (Gelişmiş, NAT veya Sanal Sunucular altında olabilir)
5. İki kural oluşturun:
   - Dış Bağlantı Noktası: [I2P bağlantı noktanız] → Dahili IP: [bilgisayarınız] → Dahili Bağlantı Noktası: [aynısı] → Protokol: **UDP**
   - Dış Bağlantı Noktası: [I2P bağlantı noktanız] → Dahili IP: [bilgisayarınız] → Dahili Bağlantı Noktası: [aynısı] → Protokol: **TCP**
6. Yapılandırmayı kaydedin ve gerekirse router'ınızı yeniden başlatın

**Port yönlendirmesini doğrulayın** yapılandırmadan sonra çevrimiçi kontrol araçlarını kullanarak. Algılama başarısız olursa, güvenlik duvarı ayarlarını kontrol edin - hem sistem güvenlik duvarı hem de varsa antivirüsün güvenlik duvarı I2P bağlantı noktasına izin vermelidir.

**Hidden mode alternatifi** port yönlendirme yapılamayan kısıtlayıcı ağlar için: http://127.0.0.1:7657/confignet adresinden etkinleştirin → "Hidden mode" seçeneğini işaretleyin. router güvenlik duvarı arkasında kalır, ancak bu duruma göre optimize olmak için yalnızca SSU tanıtıcılarını kullanır. Performans daha yavaş olur, ancak işlevsel kalır.

## Router "Starting" veya "Testing" durumlarında takılı kalıyor

İlk önyükleme sırasında görülen bu geçici durumlar genellikle **yeni kurulumlar için 10-15 dakika** veya **halihazırda çalışan router'lar için 3-5 dakika** içinde çözülür. Erken müdahale çoğu zaman sorunları daha da kötüleştirir.

**"Network: Testing"**, router'ın çeşitli bağlantı türleri (doğrudan, introducers (aracılar), birden çok protokol sürümü) üzerinden erişilebilirliği sınadığını gösterir. Bu, başlatıldıktan sonra **ilk 5-10 dakika boyunca normaldir**. Router, en iyi yapılandırmayı belirlemek için birden çok senaryoyu test eder.

**"Rejecting tunnels: starting up"** bootstrap (önyükleme) sırasında, router yeterli eş bilgisine sahip değilken görünür. Router, ağa yeterince entegre olana kadar aktarma trafiğine katılmaz. netDb 50+ router ile dolduğunda bu mesaj 10-20 dakika içinde kaybolmalıdır.

**Saat sapması erişilebilirlik testini öldürür.** I2P, sistem saatinin ağ saatine göre **±60 saniye** içinde olmasını gerektirir. 90 saniyeyi aşan bir fark, bağlantının otomatik olarak reddedilmesine neden olur. Sistem saatinizi senkronize edin:

Linux: `sudo timedatectl set-ntp true && sudo systemctl restart systemd-timesyncd`

Windows: Denetim Masası → Tarih ve Saat → İnternet Saati → Şimdi güncelle → Otomatik eşitlemeyi etkinleştir

macOS: Sistem Tercihleri → Tarih ve Saat → "Tarihi ve saati otomatik olarak ayarla" seçeneğini etkinleştir

Saat kaymasını düzelttikten sonra, düzgün bir entegrasyon için I2P’yi tamamen yeniden başlatın.

**Yetersiz bant genişliği tahsisi** başarılı test yapılmasını engeller. router'ın test tunnels oluşturabilmesi için yeterli kapasiteye ihtiyacı vardır. Şurada yapılandırın: http://127.0.0.1:7657/config:

- **Asgari yeterli:** Gelen 96 KB/sn, Giden 64 KB/sn
- **Önerilen standart:** Gelen 256 KB/sn, Giden 128 KB/sn  
- **En uygun performans:** Gelen 512+ KB/sn, Giden 256+ KB/sn
- **Paylaşım yüzdesi:** 80% (router'ın ağa bant genişliği katkısında bulunmasına olanak tanır)

Daha düşük bant genişliği işe yarayabilir, ancak entegrasyon süresini dakikalardan saatlere uzatır.

**Bozulmuş netDb**, düzgün olmayan kapatma veya disk hatalarından dolayı sonsuz test döngülerine neden olur. router, geçerli eş verileri olmadan testleri tamamlayamaz:

```bash
# Stop I2P completely
i2prouter stop    # or systemctl stop i2p

# Delete corrupted database (safe - will reseed automatically)
rm -rf ~/.i2p/netDb/*

# Restart and allow 10-15 minutes for reseed
i2prouter start
```
Windows: `%APPDATA%\I2P\netDb\` veya `%LOCALAPPDATA%\I2P\netDb\` klasörünün içeriğini silin

**Güvenlik duvarının reseed (ilk eş temini) işlemini engellemesi**, ilk eşleri edinmeyi önler. Başlangıç sürecinde, I2P HTTPS reseed sunucularından router bilgilerini alır. Kurumsal/İSS güvenlik duvarları bu bağlantıları engelleyebilir. Kısıtlayıcı ağların arkasında çalışıyorsanız, http://127.0.0.1:7657/configreseed adresinde reseed proxy'yi yapılandırın.

## Yavaş hızlar, zaman aşımları ve tunnel oluşturma başarısızlıkları

I2P'nin tasarımı, çok sıçramalı şifreleme, paket ek yükü ve rota öngörülemezliği nedeniyle doğası gereği **açık internete kıyasla 3-10 kat daha yavaş hızlar** üretir. Bir tunnel kurulumu birden çok router üzerinden geçer; her biri gecikme ekler. Bunu anlamak, normal davranışı sorun sanarak yanlış teşhis etmeyi önler.

**Tipik performans beklentileri:**

- .i2p sitelerinde web'de gezinme: Başlangıçta sayfalar 10-30 saniyede yüklenir, tunnel (I2P'de kullanılan şifreli bağlantı yolu) kurulumu sonrası daha hızlı
- I2PSnark ile torrent kullanımı: seed sayısına ve ağ koşullarına bağlı olarak torrent başına 10-100 KB/sn  
- Büyük dosya indirmeleri: Sabır gerekir - megabaytlık dosyalar dakikalar, gigabaytlar saatler sürebilir
- İlk bağlantı en yavaştır: Tunnel oluşturma 30-90 saniye sürer; sonraki bağlantılar mevcut tunnel'leri kullanır

**Tunnel oluşturma başarı oranı** ağ sağlığını gösterir. http://127.0.0.1:7657/tunnels adresinden kontrol edin:

- **60%'ın üzerinde:** Normal, sağlıklı çalışma
- **40-60%:** Sınırda, bant genişliğini artırmayı veya yükü azaltmayı düşünün
- **40%'ın altında:** Sorunlu - yetersiz bant genişliğine, ağ sorunlarına veya kötü peer (eş) seçimine işaret eder

**Bant genişliği tahsisini artırın** ilk optimizasyon olarak. Yavaşlamaların çoğu bant genişliği yetersizliğinden kaynaklanır. http://127.0.0.1:7657/config adresinde limitleri kademeli olarak artırın ve http://127.0.0.1:7657/graphs adresindeki grafikleri izleyin.

**DSL/Kablo (1-10 Mbps bağlantı hızları) için:** - Gelen: 400 KB/sn - Giden: 200 KB/sn - Paylaşım: %80 - Bellek: 384 MB (wrapper.config'i düzenleyin)

**Yüksek hızlı (10-100+ Mbps) bağlantılar için:** - Gelen: 1500 KB/sec   - Giden: 1000 KB/sec - Paylaşım: 80-100% - Bellek: 512-1024 MB - Göz önünde bulundurun: http://127.0.0.1:7657/configadvanced adresinde katılımcı tunnels (tüneller) sayısını 2000-5000'e artırmayı

**Tunnel yapılandırmasını optimize edin** daha iyi performans için. Belirli tunnel ayarlarına http://127.0.0.1:7657/i2ptunnel adresinden erişin ve her bir tunnel'ı düzenleyin:

- **Tunnel sayısı:** 2'den 3-4'e çıkarın (daha fazla rota mevcut)
- **Yedek sayısı:** 1-2 olarak ayarlayın (tunnel başarısız olursa hızlı yedek geçiş)
- **Tunnel uzunluğu:** Varsayılan 3 atlama iyi bir denge sağlar; 2'ye düşürmek hızı artırır ancak anonimliği azaltır

**Yerel kripto kütüphanesi (jbigi)** salt Java şifrelemeye kıyasla 5-10 kat daha iyi performans sağlar. Yüklendiğini http://127.0.0.1:7657/logs adresinde doğrulayın - "jbigi loaded successfully" veya "Using native CPUID implementation" ifadelerini arayın. Yoksa:

Linux: Genellikle otomatik olarak algılanır ve ~/.i2p/jbigi-*.so konumundan yüklenir Windows: I2P kurulum dizininde jbigi.dll dosyasını kontrol edin Eksikse: Derleme araçlarını kurup kaynaktan derleyin veya resmi depolardan önceden derlenmiş ikili dosyaları indirin

**Router'ı kesintisiz çalışır halde tutun.** Her yeniden başlatma entegrasyonu sıfırlar ve tunnel ağını ve eş ilişkilerini yeniden oluşturmak 30-60 dakika gerektirir. Yüksek çalışma süresine sahip kararlı routers, tunnel kurulumunda öncelikli olarak seçilir; bu da performans için olumlu bir geri besleme yaratır.

## Yüksek CPU ve bellek kullanımı

Aşırı kaynak kullanımı genellikle **yetersiz bellek tahsisi**, **eksik yerel kriptografi kitaplıkları** veya **ağ katılımına aşırı taahhüt** olduğunu gösterir. İyi yapılandırılmış routers, aktif kullanım sırasında CPU'nun %10-%30'unu kullanmalı ve ayrılan heap'in (yığın) %80'inin altında kararlı bellek kullanımını sürdürmelidir.

**Bellek sorunları şu şekilde kendini gösterir:** - Düz tepeli bellek grafikleri (maksimumda çakılı) - Sık çöp toplama (garbage collection; dik düşüşlü testere dişi deseni) - Günlüklerde OutOfMemoryError - Router'ın yük altında yanıtsız hale gelmesi - Kaynak tükenmesi nedeniyle otomatik kapanma

**Java heap (yığın bellek) için ayrılan belleği artırın** wrapper.config dosyasında (tam kapatma gerektirir):

```bash
# Linux: ~/.i2p/wrapper.config
# Windows: %APPDATA%\I2P\wrapper.config  
# Find and modify:
wrapper.java.maxmemory=512

# Recommendations by usage:
# Light browsing only: 256
# Standard use (browsing + light torrenting): 512
# Heavy use (multiple applications, active torrenting): 768-1024
# Floodfill or very high bandwidth: 1024-2048
```
**Kritik:** wrapper.config dosyasını düzenledikten sonra, **tamamen kapatmalısınız** (yeniden başlatmayın), düzgün bir sonlanma için 11 dakika bekleyin ve ardından yeniden çalıştırın. Router konsolundaki "Restart" düğmesi wrapper ayarlarını yeniden yüklemez.

**CPU optimizasyonu yerel kripto kütüphanesi gerektirir.** Saf Java BigInteger işlemleri, yerel gerçekleştirmelere kıyasla 10–20 kat daha fazla CPU tüketir. Başlatma sırasında http://127.0.0.1:7657/logs adresinde jbigi durumunu doğrulayın. jbigi olmadan, tunnel oluşturma ve şifreleme işlemleri sırasında CPU kullanımı %50–100 seviyesine sıçrar.

**Katılımcı tunnel yükünü azaltın** router aşırı yük altındaysa:

1. http://127.0.0.1:7657/configadvanced adresine erişin
2. `router.maxParticipatingTunnels=1000` olarak ayarlayın (varsayılan 8000)
3. http://127.0.0.1:7657/config adresindeki paylaşım yüzdesini %80'den %50'ye düşürün
4. Etkinse floodfill modunu devre dışı bırakın: `router.floodfillParticipant=false`

**I2PSnark'ın bant genişliğini ve eşzamanlı torrent sayısını sınırlandırın.** Torrent kullanımı önemli ölçüde kaynak tüketir. http://127.0.0.1:7657/i2psnark adresinde:

- Aktif torrent sayısını en fazla 3-5 olacak şekilde sınırlandırın
- "Up BW Limit" ve "Down BW Limit" ayarlarını makul değerlere ayarlayın (her biri için 50-100 KB/sn)
- Aktif olarak gerekmediğinde torrentleri durdurun
- Aynı anda düzinelerce torrent için seeding (kaynak olarak paylaşma) yapmaktan kaçının

**Kaynak kullanımını izleyin** http://127.0.0.1:7657/graphs adresindeki yerleşik grafikler aracılığıyla. Bellek, flat-top (tepede düzleşme) değil, bir boşluk payı göstermelidir. tunnel oluşturma sırasında CPU sıçramaları normaldir; kalıcı yüksek CPU, yapılandırma sorunlarına işaret eder.

**Ağır kaynak kısıtlamalı sistemler** (Raspberry Pi, eski donanım) için alternatif olarak **i2pd**'yi (C++ gerçeklemesi) değerlendirin. i2pd, Java I2P için 350+ MB'a kıyasla ~130 MB RAM gerektirir ve benzer yükler altında %70'e kıyasla ~%7 CPU (işlemci) kullanır. i2pd'nin yerleşik uygulamalarının olmadığını ve harici araçlar gerektirdiğini unutmayın.

## I2PSnark torrent sorunları

I2PSnark'ın I2P router mimarisiyle entegrasyonu, **torrent işlemlerinin tamamen router tunnel sağlığına bağlı olduğunu** anlamayı gerektirir. Router, 10+ aktif eş ve işlevsel tunnels ile yeterli entegrasyonu sağlayana kadar torrentler başlamaz.

**Torrentlerin %0'da takılı kalması genellikle şunlara işaret eder:**

1. **Router tam olarak entegre değil:** I2P'yi başlattıktan sonra torrent etkinliği beklemeye başlamadan önce 10-15 dakika bekleyin
2. **DHT devre dışı:** http://127.0.0.1:7657/i2psnark → Configuration → "Enable DHT"i işaretleyin (0.9.2 sürümünden beri varsayılan olarak etkin)
3. **Geçersiz veya ölü tracker'lar:** I2P torrentleri I2P'ye özgü tracker'lar gerektirir - clearnet (açık internet) tracker'ları çalışmaz
4. **Yetersiz tunnel yapılandırması:** I2PSnark Configuration → Tunnels bölümünden tunnel sayısını artırın

**Daha iyi performans için I2PSnark tunnels'ı yapılandırın:**

- Gelen tunnel sayısı: 3-5 (Java I2P için varsayılan 2, i2pd için 5)
- Giden tunnel sayısı: 3-5  
- Tunnel uzunluğu: 3 atlama (hız için 2'ye düşürün, daha az anonimlik)
- Tunnel sayısı: 3 (tutarlı performans sağlar)

**Temel I2P torrent tracker'ları** eklemeniz gerekenler: - tracker2.postman.i2p (birincil, en güvenilir) - w7tpbzncbcocrqtwwm3nezhnnsw4ozadvi2hmvzdhrqzfxfum7wa.b32.i2p/a

Herhangi bir clearnet (.i2p olmayan; anonim olmayan açık internet) tracker'larını kaldırın - hiçbir değer sağlamazlar ve zaman aşımına uğrayan bağlantı denemeleri oluştururlar.

**"Torrent not registered" hataları**, izleyici (tracker) ile iletişim başarısız olduğunda oluşur. torrent'e sağ tıklayıp → "Start" seçeneğini kullanmak yeniden duyuruyu zorlar. Sorun sürüyorsa, I2P için yapılandırılmış bir tarayıcıda http://tracker2.postman.i2p adresine giderek izleyicinin erişilebilirliğini doğrulayın. Çalışmayan izleyiciler, çalışan alternatiflerle değiştirilmelidir.

**Eşler bağlanmıyor**; tracker başarılı olsa da şunları düşündürür: - Router güvenlik duvarı arkasında (port yönlendirme ile iyileşir ama zorunlu değildir) - Yetersiz bant genişliği (256+ KB/sec'e artırın)   - Sürü çok küçük (bazı torrentlerde 1-2 seed (gönderici) bulunur; sabır gerekir) - DHT kapalı (izleyicisiz eş keşfi için etkinleştirin)

**DHT ve PEX (Peer Exchange)'i etkinleştirin** I2PSnark Configuration bölümünde. DHT, izleyiciye bağımlı olmadan eşlerin bulunmasını sağlar. PEX, bağlı eşlerden yeni eşler keşfederek sürü keşfini hızlandırır.

**İndirilen dosyaların bozulması** I2PSnark'ın yerleşik bütünlük denetimi sayesinde nadiren meydana gelir. Tespit edilirse:

1. Torrent'e sağ tıklayın → "Check" tüm parçaların rehash'ini (yeniden hash hesaplama) zorlar
2. Bozulmuş torrent verilerini silin (.torrent dosyası saklanır)  
3. Parça doğrulamasıyla yeniden indirmek için sağ tıklayın → "Start"
4. Bozulma devam ederse diski hatalar için kontrol edin: `chkdsk` (Windows), `fsck` (Linux)

**İzleme dizini çalışmıyor** uygun yapılandırma gerektirir:

1. I2PSnark Yapılandırması → "Watch directory": Mutlak yolu ayarlayın (örn., `/home/user/torrents/watch`)
2. I2P sürecinin okuma izinlerine sahip olduğundan emin olun: `chmod 755 /path/to/watch`
3. .torrent dosyalarını izleme dizinine yerleştirin - I2PSnark bunları otomatik olarak ekler
4. "Auto start" ayarını yapılandırın: torrentlerin eklendiklerinde hemen başlayıp başlamayacağını belirleyin

**Torrent kullanımı için performans optimizasyonu:**

- Eşzamanlı etkin torrentleri sınırlandırın: standart bağlantılar için en fazla 3–5
- Önemli indirmelere öncelik verin: düşük öncelikli torrentleri geçici olarak durdurun
- router için ayrılan bant genişliğini artırın: Daha fazla bant genişliği = daha iyi torrent performansı
- Sabırlı olun: I2P torrent kullanımı, clearnet (açık internet) BitTorrent'e kıyasla doğası gereği daha yavaştır
- İndirdikten sonra paylaşımda kalın: Ağ karşılıklılıkla gelişir

## I2P üzerinden Git (dağıtık sürüm kontrol sistemi) yapılandırması ve sorun giderme

I2P üzerinden Git işlemleri, SSH/HTTP erişimi için ya **SOCKS proxy yapılandırması** ya da **özel I2P tunnels** gerektirir. Git'in tasarımı düşük gecikmeli bağlantıları varsayar, bu da I2P'nin yüksek gecikmeli mimarisini zorlayıcı hâle getirir.

**Git'i I2P SOCKS proxy'sini kullanacak şekilde yapılandırın:**

~/.ssh/config dosyasını düzenleyin (mevcut değilse oluşturun):

```
Host *.i2p
    ProxyCommand nc -X 5 -x 127.0.0.1:4447 %h %p
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
```
Bu, .i2p ana bilgisayarlarına yapılan tüm SSH bağlantılarını I2P'nin SOCKS proxy'si (4447 numaralı port) üzerinden yönlendirir. ServerAlive ayarları, I2P gecikmesi sırasında bağlantıyı sürdürür.

HTTP/HTTPS git işlemleri için git'i global olarak yapılandırın:

```bash
git config --global http.proxy socks5h://127.0.0.1:4447
git config --global https.proxy socks5h://127.0.0.1:4447
```
Not: `socks5h` DNS çözümlemesini proxy üzerinden gerçekleştirir - .i2p alan adları için kritiktir.

**Git SSH için özel bir I2P tunnel oluşturun** (SOCKS'tan daha güvenilir):

1. http://127.0.0.1:7657/i2ptunnel adresine erişin
2. "New client tunnel" → "Standard"
3. Yapılandırın:
   - Ad: Git-SSH  
   - Tür: Client
   - Port: 2222 (Git erişimi için yerel port)
   - Hedef: [your-git-server].i2p:22
   - Otomatik başlatma: Etkin
   - Tunnel sayısı: 3-4 (güvenilirlik için daha yüksek)
4. Kaydedin ve tunnel'ı başlatın
5. SSH'yi tunnel kullanacak şekilde yapılandırın: `ssh -p 2222 git@127.0.0.1`

**SSH kimlik doğrulama hataları** I2P üzerinden genellikle şunlardan kaynaklanır:

- Anahtar ssh-agent'e eklenmedi: `ssh-add ~/.ssh/id_rsa`
- Anahtar dosya izinleri hatalı: `chmod 600 ~/.ssh/id_rsa`
- Tunnel çalışmıyor: http://127.0.0.1:7657/i2ptunnel adresinde yeşil durumda göründüğünü doğrulayın
- Git sunucusu belirli bir anahtar türü gerektiriyor: RSA başarısız olursa ed25519 anahtarı oluşturun

**Git işlemlerinin zaman aşımına uğraması** I2P'nin gecikme özellikleriyle ilişkilidir:

- Git zaman aşımı süresini artırın: `git config --global http.postBuffer 524288000` (500MB arabellek)
- Düşük hız sınırını artırın: `git config --global http.lowSpeedLimit 1000` ve `git config --global http.lowSpeedTime 600` (10 dakika bekler)
- İlk checkout için sığ klon kullanın: `git clone --depth 1 [url]` (yalnızca en son commit'i getirir, daha hızlı)
- Düşük etkinlik dönemlerinde klonlayın: Ağ tıkanıklığı I2P performansını etkiler

**Yavaş git clone/fetch işlemleri** I2P’nin mimarisine özgüdür. 100MB’lık bir depo I2P üzerinden 30-60 dakika sürebilir; clearnet (açık internet) üzerinde ise saniyeler içinde tamamlanır. Stratejiler:

- Sığ klonlar kullanın: `--depth 1` başlangıçtaki veri aktarımını önemli ölçüde azaltır
- Artımlı olarak alın: Tam bir klon yerine, belirli dalları alın: `git fetch origin branch:branch`
- I2P üzerinden rsync kullanmayı düşünün: Çok büyük depolar için rsync daha iyi performans gösterebilir
- Tunnel sayısını artırın: Daha fazla tunnel, uzun süreli büyük aktarımlar için daha iyi aktarım hızı sağlar

**"Bağlantı reddedildi" hataları** tunnel yanlış yapılandırmasına işaret eder:

1. I2P router çalıştığını doğrulayın: http://127.0.0.1:7657 adresini kontrol edin
2. http://127.0.0.1:7657/i2ptunnel adresinde tunnel’in aktif ve yeşil olduğunu doğrulayın
3. Tunnel’i test edin: `nc -zv 127.0.0.1 2222` (tunnel çalışıyorsa bağlanmalıdır)
4. Hedefin erişilebilir olduğunu kontrol edin: Mümkünse hedefin HTTP arayüzünü tarayıcıda açın
5. Belirli hatalar için http://127.0.0.1:7657/logs adresindeki tunnel günlüklerini inceleyin

**I2P üzerinden Git için en iyi uygulamalar:**

- Kararlı Git erişimi için I2P router'ı sürekli çalışır durumda tutun
- Parola ile kimlik doğrulama yerine SSH anahtarları kullanın (daha az etkileşimli istem)
- Geçici SOCKS bağlantıları yerine kalıcı tunnel'ları yapılandırın
- Daha iyi kontrol için kendi I2P git sunucunuzu barındırmayı düşünün
- İşbirlikçileriniz için .i2p git uç noktalarınızı belgeleyin

## eepsites'e erişim ve .i2p alan adlarını çözümleme

Kullanıcıların .i2p sitelerine erişememesinin en yaygın nedeni **yanlış tarayıcı proxy yapılandırmasıdır**. I2P siteleri yalnızca I2P ağı içinde bulunur ve I2P'nin HTTP proxy'si üzerinden yönlendirme gerektirir.

**Tarayıcı proxy ayarlarını tam olarak şu şekilde yapılandırın:**

**Firefox (I2P için önerilir):**

1. Menü → Ayarlar → Ağ Ayarları → Ayarlar düğmesi
2. "Manuel proxy yapılandırması"nı seçin
3. HTTP Proxy: **127.0.0.1** Port: **4444**
4. SSL Proxy: **127.0.0.1** Port: **4444**  
5. SOCKS Proxy: **127.0.0.1** Port: **4447** (isteğe bağlı, SOCKS uygulamaları için)
6. "SOCKS v5 kullanırken DNS'i proxy üzerinden çöz" seçeneğini işaretleyin
7. Kaydetmek için Tamam

**Kritik Firefox about:config ayarları:**

`about:config` sayfasına gidin ve şunları değiştirin:

- `media.peerconnection.ice.proxy_only` = **true** (WebRTC IP sızıntılarını önler)
- `keyword.enabled` = **false** (.i2p adreslerinin arama motorlarına yönlendirilmesini önler)
- `network.proxy.socks_remote_dns` = **true** (DNS çözümlemesini proxy üzerinden yapar)

**Chrome/Chromium kısıtlamaları:**

Chrome, uygulamaya özel olanlar yerine sistem genelindeki proxy ayarlarını kullanır. Windows'da: Ayarlar → "proxy" ara → "Bilgisayarınızın proxy ayarlarını açın" → HTTP'yi 127.0.0.1:4444 ve HTTPS'i 127.0.0.1:4445 olarak yapılandırın.

Daha iyi bir yaklaşım: Seçici .i2p yönlendirmesi için FoxyProxy veya Proxy SwitchyOmega uzantılarını kullanın.

**"Website Not Found In Address Book" hataları**, router'da .i2p alan adının kriptografik adresi bulunmadığı anlamına gelir. I2P, merkezi DNS yerine yerel adres defterleri kullanır. Çözümler:

**Yöntem 1: Atlama hizmetlerini kullanın** (yeni siteler için en kolay yöntem):

http://stats.i2p adresine gidin ve siteyi arayın. addresshelper (adres yardımcısı) bağlantısına tıklayın: `http://example.i2p/?i2paddresshelper=base64destination`. Tarayıcınız "Adres defterine kaydet?" mesajını gösterir - eklemek için onaylayın.

**Yöntem 2: Adres defteri aboneliklerini güncelleyin:**

1. http://127.0.0.1:7657/dns adresine gidin (SusiDNS)
2. "Subscriptions" sekmesine tıklayın  
3. Etkin abonelikleri doğrulayın (varsayılan: http://i2p-projekt.i2p/hosts.txt)
4. Önerilen abonelikleri ekleyin:
   - http://stats.i2p/cgi-bin/newhosts.txt
   - http://notbob.i2p/hosts.txt
   - http://reg.i2p/export/hosts.txt
5. Abonelikleri hemen güncellemeye zorlamak için "Update Now" düğmesine tıklayın
6. İşlenmesi için 5-10 dakika bekleyin

**Yöntem 3: base32 adresleri kullanın** (site çevrimiçiyse her zaman çalışır):

Her .i2p sitesinin bir base32 adresi vardır: .b32.i2p ile biten 52 rastgele karakter (örn., `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`). Base32 adresleri adres defterini atlar - router doğrudan kriptografik bir sorgulama gerçekleştirir.

**Yaygın tarayıcı yapılandırma hataları:**

- Yalnızca HTTP kullanan sitelerde HTTPS denemek: Çoğu .i2p site yalnızca HTTP kullanır - `https://example.i2p` çalışmaz
- `http://` önekini unutmak: Tarayıcı bağlanmak yerine arama yapabilir - her zaman `http://example.i2p` kullanın
- WebRTC (gerçek zamanlı web iletişimi) etkin: Gerçek IP adresinizi sızdırabilir - Firefox ayarları veya eklentileri üzerinden devre dışı bırakın
- DNS proxy’lenmiyor: Clearnet (açık internet) DNS, .i2p’yi çözümleyemez - DNS sorgularını proxy üzerinden geçirmek gerekir
- Yanlış proxy bağlantı noktası: HTTP için 4444 (clearnet’e HTTPS outproxy (dış proxy) olan 4445 değil)

**Router tam olarak entegre edilmemiş** herhangi bir siteye erişimi engeller. Yeterli entegrasyonu doğrulayın:

1. http://127.0.0.1:7657 sayfasının "Network: OK" veya "Network: Firewalled" gösterdiğini kontrol edin ("Network: Testing" değil)
2. Aktif eşler en az 10+ (tercihen 50+) göstermeli  
3. "Rejecting tunnels: starting up" mesajı olmamalı
4. .i2p erişimini beklemeden önce router başlatıldıktan sonra tam 10-15 dakika bekleyin

**IRC ve e-posta istemcisi yapılandırması** benzer proxy kalıplarını izler:

**IRC:** İstemciler **127.0.0.1:6668** adresine bağlanır (I2P'nin IRC proxy tunnel'ı). IRC istemcisinin vekil sunucu ayarlarını devre dışı bırakın - localhost:6668 bağlantısı zaten I2P üzerinden iletilmektedir.

**E-posta (Postman):**  - SMTP: **127.0.0.1:7659** - POP3: **127.0.0.1:7660**   - SSL/TLS yok (şifreleme I2P tunnel tarafından sağlanır) - Kimlik bilgileri postman.i2p hesap kaydından

Tüm bu tunnel'ların http://127.0.0.1:7657/i2ptunnel adresinde "running" (yeşil) durumunda olması gerekir.

## Kurulum hataları ve paket sorunları

Paket tabanlı kurulumlar (Debian, Ubuntu, Arch) bazen **depo değişiklikleri**, **GPG anahtarının süresinin dolması** veya **bağımlılık çakışmaları** nedeniyle başarısız olabilir. Son sürümlerde resmi depolar deb.i2p2.de/deb.i2p2.no (destek sonu [EOL]) adreslerinden **deb.i2p.net** adresine taşındı.

**Debian/Ubuntu deposunu en güncel hâle getirin:**

```bash
# Remove old repository entries
sudo rm /etc/apt/sources.list.d/i2p.list

# Add current repository
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/i2p.list

# Download and install current signing key
curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings/

# Update and install
sudo apt update
sudo apt install i2p i2p-keyring
```
**GPG imza doğrulama hataları** depo anahtarlarının süresi dolduğunda veya değiştiğinde oluşur:

```bash
# Error: "The following signatures were invalid"
# Solution: Install current keyring package
sudo apt install i2p-keyring

# Manual key import if package unavailable
wget https://geti2p.net/_static/i2p-debian-repo.key.asc
sudo apt-key add i2p-debian-repo.key.asc
```
**Paket kurulumu sonrasında servis başlamıyor** çoğunlukla Debian/Ubuntu'daki AppArmor profil sorunlarından kaynaklanır:

```bash
# Check service status
sudo systemctl status i2p.service

# Common error: "Failed at step APPARMOR spawning"
# Solution: Reconfigure without AppArmor
sudo dpkg-reconfigure -plow i2p
# Select "No" for AppArmor when prompted

# Alternative: Set profile to complain mode
sudo aa-complain /usr/sbin/wrapper

# Check logs for specific errors  
sudo journalctl -xe -u i2p.service
```
**İzin sorunları** paketle kurulan I2P'de:

```bash
# Fix ownership (package install uses 'i2psvc' user)
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p

# Set file descriptor limits (add to /etc/security/limits.conf)
i2psvc soft nofile 4096  
i2psvc hard nofile 8192
```
**Java uyumluluk sorunları:**

I2P 2.10.0 **en az Java 8** gerektirir. Daha eski sistemlerde Java 7 veya daha öncesi bulunabilir:

```bash
# Check Java version
java -version

# Install appropriate Java (Debian/Ubuntu)
sudo apt install openjdk-11-jre-headless

# Set default Java if multiple versions installed
sudo update-alternatives --config java
```
**Wrapper yapılandırma hataları** servisin başlatılmasını engeller:

Wrapper.config konumu kurulum yöntemine göre değişir: - Kullanıcı kurulumu: `~/.i2p/wrapper.config` - Paket kurulumu: `/etc/i2p/wrapper.config` veya `/var/lib/i2p/wrapper.config`

Yaygın wrapper.config sorunları:

- Yanlış yollar: `wrapper.java.command` geçerli bir Java kurulumuna işaret etmelidir
- Yetersiz bellek: `wrapper.java.maxmemory` çok düşük ayarlanmış (512+ olacak şekilde artırın)
- Yanlış pid dosyası konumu: `wrapper.pidfile` yazılabilir bir konum olmalıdır
- Eksik wrapper (sarmalayıcı) ikilisi: Bazı platformlarda önceden derlenmiş wrapper bulunmaz (yedek olarak runplain.sh kullanın)

**Güncelleme başarısızlıkları ve bozuk güncellemeler:**

Router konsolu güncellemeleri, ağ kesintileri nedeniyle indirme ortasında ara sıra başarısız olabilir. Elle güncelleme prosedürü:

1. https://geti2p.net/en/download adresinden i2pupdate_X.X.X.zip dosyasını indirin
2. SHA256 sağlama toplamının yayımlanan karmayla eşleştiğini doğrulayın
3. I2P kurulum dizinine `i2pupdate.zip` adıyla kopyalayın
4. Router'ı yeniden başlatın - güncellemeyi otomatik olarak algılar ve çıkarır
5. Güncellemenin kurulması için 5-10 dakika bekleyin
6. Yeni sürümü http://127.0.0.1:7657 adresinde doğrulayın

**Çok eski sürümlerden geçiş** (0.9.47 öncesi) güncel sürümlere, uyumsuz imza anahtarları veya kaldırılmış özellikler nedeniyle başarısız olabilir. Kademeli güncellemeler gereklidir:

- 0.9.9'dan eski sürümler: Mevcut imzalar doğrulanamaz - manuel güncelleme yapın
- Java 6/7 kullanan sürümler: I2P'yi 2.x'e güncellemeden önce Java'yı yükseltin
- Büyük sürüm atlamaları: Önce ara bir sürüme güncelleyin (önerilen ara durak 0.9.47)

**Yükleyici ne zaman, paket ne zaman kullanılmalı:**

- **Paketler (apt/yum):** Sunucular için en uygunu, otomatik güvenlik güncellemeleri, sistem entegrasyonu, systemd yönetimi
- **Yükleyici (.jar):** Kullanıcı düzeyi kurulumlar için en uygunu, Windows, macOS, özel kurulumlar, en son sürüme erişim

## Yapılandırma dosyası bozulması ve kurtarma

I2P'deki yapılandırma kalıcılığı, birkaç kritik dosyaya dayanır. Bozulma genellikle **düzgün kapatılmama**, **disk hataları** veya **elle düzenleme hataları** nedeniyle ortaya çıkar. Dosyaların amaçlarını anlamak, tam yeniden kurulum yerine cerrahi hassasiyette onarım yapmayı sağlar.

**Kritik dosyalar ve amaçları:**

- **router.keys** (516+ bayt): Router'ın kriptografik kimliği - bunun kaybedilmesi yeni bir kimlik oluşturur
- **router.info** (otomatik oluşturulur): Yayınlanan router bilgisi - silmek güvenlidir, yeniden oluşturulur  
- **router.config** (metin): Ana yapılandırma - bant genişliği, ağ ayarları, tercihler
- **i2ptunnel.config** (metin): Tunnel tanımları - istemci/sunucu tunnel'ları, anahtarlar, hedefler
- **netDb/** (dizin): Eş veritabanı - ağ katılımcıları için router bilgileri
- **peerProfiles/** (dizin): Eşlere ilişkin performans istatistikleri - tunnel seçimini etkiler
- **keyData/** (dizin): eepsite'lar ve servisler için hedef anahtarlar - kaybedilmesi adresleri değiştirir
- **addressbook/** (dizin): Yerel .i2p ana bilgisayar adı eşlemeleri

**Tam yedekleme prosedürü** değişikliklerden önce:

```bash
# Stop I2P first
i2prouter stop  # or: systemctl stop i2p

# Backup directory
BACKUP_DIR=~/i2p-backup-$(date +%Y%m%d-%H%M)
mkdir -p $BACKUP_DIR

# Copy critical files
cp -r ~/.i2p/router.keys $BACKUP_DIR/
cp -r ~/.i2p/*.config $BACKUP_DIR/
cp -r ~/.i2p/keyData $BACKUP_DIR/
cp -r ~/.i2p/addressbook $BACKUP_DIR/
cp -r ~/.i2p/eepsite $BACKUP_DIR/  # if hosting sites

# Optional but recommended
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
```
**Router.config bozulma belirtileri:**

- Router, günlüklerdeki ayrıştırma hataları nedeniyle başlamıyor
- Ayarlar yeniden başlatmanın ardından korunmuyor
- Beklenmedik varsayılan değerler görünüyor  
- Dosyayı görüntülerken bozuk karakterler

**Bozulmuş router.config dosyasını onarın:**

1. Mevcut olanın yedeğini alın: `cp router.config router.config.broken`
2. Dosya kodlamasını kontrol edin: BOM olmadan UTF-8 olmalı
3. Sözdizimini doğrulayın: Anahtarlar `=` ayırıcısını kullanır (`:` değil), anahtarların sonunda boşluk olmamalıdır, `#` yalnızca yorumlar içindir
4. Yaygın bozulmalar: Değerlerde ASCII dışı karakterler, satır sonu sorunları (CRLF vs LF)
5. Düzeltilemiyorsa: router.config dosyasını silin - router varsayılanı oluşturur ve kimliği korur

**Korunması gereken temel router.config ayarları:**

```properties
i2np.bandwidth.inboundKBytesPerSecond=512
i2np.bandwidth.outboundKBytesPerSecond=256
router.updatePolicy=notify
routerconsole.lang=en
router.hiddenMode=false
```
**Kayıp veya geçersiz router.keys** yeni bir router kimliği oluşturur. Bu, şu durumlar dışında kabul edilebilir:

- floodfill (I2P ağ veritabanını (netDb) dağıtan düğüm) çalıştırmak (floodfill statüsünü kaybeder)
- Yayınlanmış bir adresle eepsites (I2P içi web siteleri) barındırmak (sürekliliği kaybeder)  
- Ağda yerleşmiş itibar

Yedek olmadan kurtarma mümkün değil - yenisini oluşturun: router.keys dosyasını silin, I2P'yi yeniden başlatın, yeni bir kimlik oluşturulur.

**Kritik ayrım:** router.keys (kimlik) ile keyData/* (hizmetler). router.keys kaybedilirse router kimliği değişir. keyData/mysite-keys.dat kaybedilirse eepsite'inizin .i2p adresi değişir - adres yayımlandıysa bu felaket olur.

**eepsite/hizmet anahtarlarını ayrı ayrı yedekleyin:**

```bash
# Identify your service keys
ls -la ~/.i2p/keyData/

# Backup with descriptive names  
cp ~/.i2p/keyData/myservice-keys.dat ~/backups/myservice-keys-$(date +%Y%m%d).dat

# Store securely (encrypted if sensitive)
gpg -c ~/backups/myservice-keys-*.dat
```
**NetDb ve peerProfiles bozulması:**

Belirtiler: Etkin eş yok, tunnels oluşturulamıyor, günlüklerde "Database corruption detected"

Güvenli düzeltme (hepsi otomatik olarak reseed (başlangıç verilerini yeniden alma)/yeniden oluşturma yapacaktır):

```bash
i2prouter stop
rm -rf ~/.i2p/netDb/*
rm -rf ~/.i2p/peerProfiles/*
i2prouter start
# Wait 10-15 minutes for reseed and integration
```
Bu dizinler yalnızca önbelleğe alınmış ağ bilgileri içerir - silmek yeni bir bootstrap (önyükleme) zorunlu kılar ancak kritik veri kaybına yol açmaz.

**Önleme stratejileri:**

1. **Her zaman temiz kapatma:** `i2prouter stop` kullanın veya router konsolundaki "Shutdown" düğmesini kullanın - asla zorla sonlandırmayın
2. **Otomatik yedeklemeler:** Ayrı bir diske ~/.i2p'nin haftalık yedeği için cron görevi
3. **Disk sağlığı izleme:** SMART durumunu periyodik olarak kontrol edin - arızalanan diskler veriyi bozar
4. **Yeterli disk alanı:** 1+ GB boş alan bulundurun - dolu diskler bozulmaya neden olur
5. **UPS önerilir:** UPS (kesintisiz güç kaynağı) yazma sırasında yaşanan elektrik kesintilerinde dosyaları korur
6. **Kritik yapılandırmaları sürüm kontrolüne alın:** router.config ve i2ptunnel.config için bir Git deposu geri almayı mümkün kılar

**Dosya izinleri önemlidir:**

```bash
# Correct permissions (user install)
chmod 600 ~/.i2p/router.keys
chmod 600 ~/.i2p/*.config  
chmod 700 ~/.i2p/keyData
chmod 755 ~/.i2p

# Never run as root - creates permission problems
```
## Yaygın hata mesajlarının çözümlenmesi

I2P'nin günlükleme sistemi, sorunları tam olarak saptayan belirli hata mesajları sağlar. Bu mesajları anlamak, sorun gidermeyi hızlandırır.

**"No tunnels available"** ifadesi, router'ın çalışabilmesi için yeterli sayıda tunnel oluşturmadığında görünür. Bu, başlatıldıktan sonra **ilk 5-10 dakika boyunca normaldir**. 15 dakikadan uzun süre devam ederse:

1. http://127.0.0.1:7657 adresinde Aktif Eşler > 10 olduğunu doğrulayın
2. Bant genişliği tahsisinin yeterli olduğunu kontrol edin (en az 128+ KB/sn)
3. http://127.0.0.1:7657/tunnels adresinde tunnel başarı oranını inceleyin (>%40 olmalı)
4. Günlükleri, tunnel oluşturmanın reddedilme nedenleri için gözden geçirin

**"Clock skew detected"** veya **"NTCP2 disconnect code 7"**, sistem saatinin ağ konsensüsünden 90 saniyeden fazla saptığını gösterir. I2P **±60 saniyelik doğruluk** gerektirir. Saatinde sapma olan routers ile bağlantılar otomatik olarak reddedilir.

Hemen düzeltin:

```bash
# Linux  
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
date  # Verify correct time

# Windows
# Control Panel → Date and Time → Internet Time → Update now

# Verify after sync
http://127.0.0.1:7657/logs  # Should no longer show clock skew warnings
```
**"Build timeout"** veya **"Tunnel build timeout exceeded"**, eş zinciri boyunca tunnel inşasının zaman aşımı penceresi (genellikle 60 saniye) içinde tamamlanmadığı anlamına gelir. Nedenleri:

- **Yavaş peers (eşler):** Router, tunnel için yanıt vermeyen katılımcıları seçti
- **Ağ tıkanıklığı:** I2P ağı yüksek yük altında
- **Yetersiz bant genişliği:** Bant genişliği sınırlarınız, tunnel kurulumunun zamanında yapılmasını engelliyor
- **Aşırı yüklenmiş router:** Çok fazla katılımcı tunnel, kaynakları tüketiyor

Çözümler: Bant genişliğini artırın, katılımcı tunnel sayısını azaltın (`router.maxParticipatingTunnels` http://127.0.0.1:7657/configadvanced adresinde), daha iyi eş (peer) seçimi için port yönlendirmeyi etkinleştirin.

**"Router is shutting down"** veya **"Graceful shutdown in progress"** normal kapatma veya çökme sonrası kurtarma sırasında görünür. Düzgün kapatma (graceful shutdown), router tunnel'leri kapatıp eşleri bilgilendirirken ve durum bilgisini kalıcılaştırırken **10 dakikaya kadar** sürebilir.

Kapatma durumunda 11 dakikadan uzun süre takılı kalırsa, zorla sonlandırın:

```bash
# Linux  
kill -9 $(pgrep -f i2p)

# Windows
taskkill /F /IM javaw.exe
```
**"java.lang.OutOfMemoryError: Java heap space"** heap belleğinin tükendiğini gösterir. Hızlı çözümler:

1. wrapper.config dosyasını düzenleyin: `wrapper.java.maxmemory=512` (veya daha yüksek)
2. **Tam kapanma gerekli** - yeniden başlatma değişikliği uygulamaz
3. Tam kapanma için 11 dakika bekleyin  
4. router'ı temiz başlatın
5. http://127.0.0.1:7657/graphs adresinde ayrılan belleği doğrulayın - boş alan göstermeli

**İlgili bellek hataları:**

- **"GC overhead limit exceeded":** Çöp toplamada çok fazla zaman harcanıyor - yığın boyutunu artırın
- **"Metaspace" (Java sınıf meta verisi alanı):** Java sınıf meta verisi alanı tükendi - `wrapper.java.additional.X=-XX:MaxMetaspaceSize=256M` ekleyin

**Windows'a özgü:** Kaspersky Antivirus, wrapper.config ayarlarından bağımsız olarak Java yığınını 512MB ile sınırlar - kaldırın veya I2P'yi istisnalara ekleyin.

**"Connection timeout"** veya **"I2CP Error - port 7654"** uygulamalar router'a bağlanmaya çalıştıklarında:

1. router'ın çalıştığını doğrulayın: http://127.0.0.1:7657 yanıt vermeli
2. I2CP bağlantı noktasını kontrol edin: `netstat -an | grep 7654` LISTENING göstermeli
3. localhost güvenlik duvarının izin verdiğinden emin olun: `sudo ufw allow from 127.0.0.1`  
4. Uygulamanın doğru bağlantı noktasını kullandığını doğrulayın (I2CP=7654, SAM=7656)

**"Certificate validation failed"** veya **"RouterInfo corrupt"** reseed (başlangıç verilerinin yeniden alınması) sırasında:

Temel nedenler: saat sapması (önce düzeltin), bozulmuş netDb, geçersiz reseed (yeniden tohumlama) sertifikaları

```bash
# After fixing clock:
i2prouter stop
rm -rf ~/.i2p/netDb/*  # Delete corrupted database
i2prouter start  # Auto-reseeds with fresh data
```
**"Database corruption detected"** netDb veya peerProfiles içinde disk düzeyinde veri bozulmasına işaret eder:

```bash
# Safe fix - all will rebuild
i2prouter stop  
rm -rf ~/.i2p/netDb/* ~/.i2p/peerProfiles/*
i2prouter start
```
Disk sağlığını SMART araçlarıyla kontrol edin - tekrarlayan veri bozulmaları depolama biriminin arızalanmakta olduğuna işaret eder.

## Platforma özgü zorluklar

Farklı işletim sistemleri, izinler, güvenlik politikaları ve sistem entegrasyonuna bağlı olarak I2P'nin dağıtımında kendine özgü zorluklar ortaya çıkarır.

### Linux izin ve servis sorunları

Paket ile kurulan I2P, belirli izinler gerektiren sistem kullanıcısı **i2psvc** (Debian/Ubuntu) veya **i2p** (diğer dağıtımlar) olarak çalışır:

```bash
# Fix package install permissions  
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p
sudo chmod 644 /var/lib/i2p/*.config

# User install permissions (should be your user)
chown -R $USER:$USER ~/.i2p
chmod 700 ~/.i2p
chmod 600 ~/.i2p/router.keys ~/.i2p/*.config
```
**Dosya tanımlayıcı sınırları** router'ın bağlantı kapasitesini etkiler. Varsayılan sınırlar (1024), yüksek bant genişliğine sahip router'lar için yetersizdir:

```bash
# Check current limits
ulimit -n

# Temporary increase  
ulimit -n 4096

# Permanent fix: Edit /etc/security/limits.conf
i2psvc soft nofile 4096
i2psvc hard nofile 8192

# Systemd override
sudo mkdir -p /etc/systemd/system/i2p.service.d/
sudo nano /etc/systemd/system/i2p.service.d/override.conf

# Add:
[Service]
LimitNOFILE=8192

sudo systemctl daemon-reload
sudo systemctl restart i2p
```
**AppArmor çakışmaları** Debian/Ubuntu'da yaygındır ve servisin başlatılmasını engeller:

```bash
# Error: "Failed at step APPARMOR spawning /usr/sbin/wrapper"
# Cause: AppArmor profile missing or misconfigured

# Solution 1: Disable AppArmor for I2P
sudo aa-complain /usr/sbin/wrapper

# Solution 2: Reconfigure package without AppArmor
sudo dpkg-reconfigure -plow i2p  
# Select "No" when asked about AppArmor

# Solution 3: LXC/Proxmox containers - disable AppArmor in container config
lxc.apparmor.profile: unconfined
```
**SELinux sorunları** RHEL/CentOS/Fedora üzerinde:

```bash
# Temporary: Set permissive mode
sudo setenforce 0

# Permanent: Generate custom policy
sudo ausearch -c 'java' --raw | audit2allow -M i2p_policy
sudo semodule -i i2p_policy.pp

# Or disable SELinux for I2P process (less secure)
sudo semanage permissive -a i2p_t
```
**SystemD servis sorun giderme:**

```bash
# Detailed service status
sudo systemctl status i2p.service -l

# Full logs  
sudo journalctl -xe -u i2p.service

# Follow logs live
sudo journalctl -f -u i2p.service

# Restart with logging
sudo systemctl restart i2p.service && sudo journalctl -f -u i2p.service
```
### Windows güvenlik duvarı ve antivirüs müdahalesi

Windows Defender ve üçüncü taraf antivirüs ürünleri, ağ davranış kalıpları nedeniyle I2P’yi sık sık potansiyel tehdit olarak işaretler. Doğru yapılandırma, güvenliği korurken gereksiz engellemeleri önler.

**Windows Defender Güvenlik Duvarını Yapılandırın:**

```powershell
# Run PowerShell as Administrator

# Find Java path (adjust for your Java installation)
$javaPath = "C:\Program Files\Eclipse Adoptium\jdk-11.0.16.101-hotspot\bin\javaw.exe"

# Create inbound rules
New-NetFirewallRule -DisplayName "I2P Java" -Direction Inbound -Program $javaPath -Action Allow
New-NetFirewallRule -DisplayName "I2P UDP" -Direction Inbound -Protocol UDP -LocalPort 22648 -Action Allow  
New-NetFirewallRule -DisplayName "I2P TCP" -Direction Inbound -Protocol TCP -LocalPort 22648 -Action Allow

# Add exclusions to Windows Defender
Add-MpPreference -ExclusionPath "C:\Program Files\i2p"
Add-MpPreference -ExclusionPath "$env:APPDATA\I2P"
Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\I2P"
Add-MpPreference -ExclusionProcess "javaw.exe"
```
Port 22648'i http://127.0.0.1:7657/confignet adresindeki gerçek I2P bağlantı noktanızla değiştirin.

**Kaspersky Antivirus'a özgü sorun:** Kaspersky'nin "Application Control" özelliği, wrapper.config ayarlarından bağımsız olarak Java heap (Java yığını) değerini 512MB ile sınırlar. Bu, yüksek bant genişliğine sahip router'larda OutOfMemoryError oluşmasına neden olur.

Çözümler: 1. I2P'yi Kaspersky dışlamalarına ekleyin: Ayarlar → Ek → Tehditler ve Dışlamalar → Dışlamaları Yönet 2. Veya Kaspersky'yi kaldırın (I2P'nin çalışması için önerilir)

**Üçüncü taraf antivirüsler için genel yönergeler:**

- I2P kurulum dizinini hariç tutma listesine ekleyin  
- %APPDATA%\I2P ve %LOCALAPPDATA%\I2P dizinlerini hariç tutma listesine ekleyin
- javaw.exe'yi davranışsal analizden hariç tutun
- I2P protokollerine müdahale edebilecek "Network Attack Protection" özelliklerini devre dışı bırakın

### macOS Gatekeeper kurulumu engelliyor

macOS Gatekeeper (Apple’ın macOS’teki uygulama güvenliği özelliği), imzalanmamış uygulamaların çalıştırılmasını engeller. I2P yükleyicileri Apple Developer ID (Apple’ın geliştirici kimlik sertifikası) ile imzalanmamıştır, bu da güvenlik uyarılarını tetikler.

**I2P yükleyicisi için Gatekeeper (macOS güvenlik özelliği) engelini atlatma:**

```bash
# Method 1: Remove quarantine attribute
xattr -d com.apple.quarantine ~/Downloads/i2pinstall_*.jar
java -jar ~/Downloads/i2pinstall_*.jar

# Method 2: Use System Settings (macOS 13+)
# Try to open installer → macOS blocks it
# System Settings → Privacy & Security → scroll down
# Click "Open Anyway" next to I2P warning
# Confirm in dialog

# Method 3: Control-click installer
# Control-click (right-click) i2pinstall_*.jar
# Select "Open" from menu → "Open" again in dialog
# Bypasses Gatekeeper for this specific file
```
**Kurulumdan sonra çalıştırmak** yine de uyarıları tetikleyebilir:

```bash
# If I2P won't start due to Gatekeeper:
xattr -dr com.apple.quarantine ~/i2p/
```
**Gatekeeper'ı asla kalıcı olarak devre dışı bırakmayın** - diğer uygulamalar için güvenlik riski oluşturur. Yalnızca dosyaya özel istisnalar kullanın.

**macOS güvenlik duvarı yapılandırması:**

1. Sistem Tercihleri → Güvenlik ve Gizlilik → Güvenlik Duvarı → Güvenlik Duvarı Seçenekleri
2. Uygulama eklemek için "+" düğmesine tıklayın  
3. Java kurulumuna gidin (ör. `/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home/bin/java`)
4. Ekleyin ve "Gelen bağlantılara izin ver" olarak ayarlayın

### Android I2P uygulamasıyla ilgili sorunlar

Android sürüm kısıtlamaları ve kaynak sınırlamaları benzersiz zorluklar doğurur.

**Minimum gereksinimler:** - Güncel sürümler için Android 5.0+ (API düzeyi 21+) gereklidir - En az 512MB RAM, 1GB+ önerilir   - Uygulama + router verileri için 100MB depolama alanı - I2P için arka planda çalışma kısıtlamaları devre dışı

**Uygulama anında çöküyor:**

1. **Android sürümünü kontrol edin:** Ayarlar → Telefon hakkında → Android sürümü (5.0+ olmalı)
2. **Tüm I2P sürümlerini kaldırın:** Yalnızca tek bir varyantı yükleyin:
   - net.i2p.android (Google Play)
   - net.i2p.android.router (F-Droid)  
   Birden fazla kurulum çakışır
3. **Uygulama verilerini temizleyin:** Ayarlar → Uygulamalar → I2P → Depolama → Verileri temizle
4. **Sıfırdan yeniden yükleyin**

**Pil optimizasyonu router'ı sonlandırıyor:**

Android, pil tasarrufu için arka plan uygulamalarını agresif biçimde sonlandırır. I2P için bir istisna tanınması gerekir:

1. Ayarlar → Pil → Pil optimizasyonu (veya Uygulama pil kullanımı)
2. I2P'yi bulun → Optimize etme (veya Arka plan etkinliğine izin ver)
3. Ayarlar → Uygulamalar → I2P → Pil → Arka plan etkinliğine izin ver + Kısıtlamaları kaldır

**Mobil cihazlarda bağlantı sorunları:**

- **Bootstrap (başlatma) WiFi gerektirir:** İlk reseed (başlangıç ağ eşlerini indirme) ciddi miktarda veri indirir - WiFi kullanın, hücresel veri kullanmayın
- **Ağ değişiklikleri:** I2P ağ geçişlerini sorunsuz yönetemez - WiFi/hücresel geçişinden sonra uygulamayı yeniden başlatın
- **Mobil için bant genişliği:** Hücresel verinin tükenmesini önlemek için 64-128 KB/sec düzeyinde ihtiyatlı biçimde yapılandırın

**Mobil için performans optimizasyonu:**

1. I2P uygulaması → Menü → Ayarlar → Bant genişliği
2. Uygun sınırları ayarlayın: 64 KB/sec gelen, 32 KB/sec giden (hücresel için)
3. Katılımcı tunnels sayısını azaltın: Ayarlar → Gelişmiş → Maksimum katılımcı tunnels: 100-200
4. Pil tasarrufu için "Stop I2P when screen off" seçeneğini etkinleştirin

**Android'de torrent kullanımı:**

- En fazla 2-3 eşzamanlı torrent ile sınırlandırın
- DHT'nin (Dağıtılmış Hash Tablosu) agresiflik düzeyini azaltın  
- Torrent için yalnızca WiFi kullanın
- Mobil donanımda daha yavaş hızları kabul edin

## Reseed (netDb için başlangıç eş bilgilerini alma) ve önyükleme sorunları

Yeni I2P kurulumları, ağa katılmak için genel HTTPS sunucularından başlangıç eş bilgilerini alma işlemi olan **reseeding** (başlangıç eş bilgilerini alma) gerektirir. Reseeding sorunları, kullanıcıları sıfır eş ve herhangi bir ağ erişimi olmadan mahsur bırakır.

**"No active peers" temiz kurulumdan sonra** genellikle reseed (başlangıç eş listesini indirme işlemi) başarısızlığını gösterir. Belirtiler:

- Bilinen eşler: 0 ya da 5'in altında kalıyor
- "Network: Testing" 15 dakikadan uzun sürüyor
- Günlüklerde "Reseed failed" ya da reseed (ağa ilk kez katılmak için başlangıç düğümlerini alma işlemi) sunucularına bağlantı hataları görülüyor

**Reseed (başlangıç yönlendirici bilgilerini indirme işlemi) neden başarısız olur:**

1. **HTTPS’i engelleyen güvenlik duvarı:** Kurumsal/İSS güvenlik duvarları reseed sunucularına (ağa ilk katılmayı/önyüklemeyi sağlayan sunucular) bağlantıları engeller (443 numaralı port)
2. **SSL sertifikası hataları:** Sistemde güncel kök sertifikalar bulunmuyor
3. **Proxy gereksinimi:** Ağ, dış bağlantılar için HTTP/SOCKS proxy gerektirir
4. **Saat sapması:** Sistem saati yanlış olduğunda SSL sertifikası doğrulaması başarısız olur
5. **Coğrafi sansür:** Bazı ülkeler/İSS’ler bilinen reseed sunucularını engeller

**Elle reseed (yeniden tohumlama) işlemini zorla:**

1. http://127.0.0.1:7657/configreseed adresine gidin
2. "Save changes and reseed now" düğmesine tıklayın  
3. "Reseed got XX router infos" iletisini görmek için http://127.0.0.1:7657/logs sayfasını izleyin
4. İşleme için 5-10 dakika bekleyin
5. http://127.0.0.1:7657 adresini kontrol edin - Known peers 50+'ya yükselmiş olmalı

**reseed proxy'yi yapılandırın** (ilk başlatmada gerekli başlangıç verilerini almak için kullanılan vekil sunucu) kısıtlayıcı ağlar için:

http://127.0.0.1:7657/configreseed → Proxy Yapılandırması:

- HTTP Proxy: [proxy-server]:[port]
- Veya SOCKS5: [socks-server]:[port]  
- "Yalnızca reseed için proxy kullan" seçeneğini etkinleştir (reseed: netDb'yi başlatmak için başlangıç girdilerini yeniden indirme işlemi)
- Gerekirse kimlik bilgileri
- Kaydet ve reseed'i zorla

**Alternatif: reseed (ilk ağ verilerini indirme) için Tor proxy'si:**

Tor Browser veya Tor daemon (arka plan süreci) çalışıyorsa:

- Proxy türü: SOCKS5
- Ana bilgisayar: 127.0.0.1
- Bağlantı noktası: 9050 (varsayılan Tor SOCKS bağlantı noktası)
- Etkinleştir ve yeniden tohumla

**su3 dosyası aracılığıyla manuel reseed** (son çare):

Tüm otomatik reseed (başlangıç düğümü bilgilerinin yeniden alınması) başarısız olduğunda, reseed dosyasını bant dışı olarak edinin:

1. Kısıtlamasız bir bağlantı üzerinden güvenilir bir kaynaktan i2pseeds.su3 dosyasını indirin (https://reseed.i2p.rocks/i2pseeds.su3, https://reseed-fr.i2pd.xyz/i2pseeds.su3)
2. I2P'yi tamamen durdurun
3. i2pseeds.su3 dosyasını ~/.i2p/ dizinine kopyalayın  
4. I2P'yi başlatın - dosyayı otomatik olarak çıkarır ve işler
5. İşleme tamamlandıktan sonra i2pseeds.su3 dosyasını silin
6. http://127.0.0.1:7657 adresinde eş sayısının arttığını doğrulayın

**reseed (yeniden tohumlama) sırasında SSL sertifika hataları:**

```
Error: "Reseed: Certificate verification failed"  
Cause: System root certificates outdated or missing
```
Çözümler:

```bash
# Linux - update certificates
sudo apt install ca-certificates
sudo update-ca-certificates

# Windows - install KB updates for root certificate trust
# Or install .NET Framework (includes certificate updates)

# macOS - update system
# Software Update includes certificate trust updates
```
**30 dakikayı aştığı halde 0 bilinen eşte takılı kaldı:**

Tam bir reseed (yeniden tohumlama işlemi) başarısızlığını belirtir. Sorun giderme sırası:

1. **Sistem saatinin doğru olduğunu doğrulayın** (en yaygın sorun - İLK ÖNCE düzeltin)
2. **HTTPS bağlantısını test edin:** Tarayıcıda https://reseed.i2p.rocks adresine erişmeyi deneyin - başarısız olursa ağ sorunudur
3. **I2P günlüklerini** http://127.0.0.1:7657/logs adresinde belirli reseed (ağı başlatmak için başlangıç verilerini alma işlemi) hataları için kontrol edin
4. **Farklı bir reseed URL'si deneyin:** http://127.0.0.1:7657/configreseed → özel reseed URL'si ekleyin: https://reseed-fr.i2pd.xyz/
5. **Manuel su3 dosyası yöntemini kullanın** otomatik denemeler tükendiyse

**Reseed (yeniden tohumlama) sunucuları zaman zaman çevrimdışı:** I2P, birden fazla sabit kodlanmış reseed sunucusu içerir. Biri başarısız olursa, router otomatik olarak diğerlerini dener. Tüm reseed sunucularının tamamen devre dışı kalması son derece nadirdir, ancak mümkündür.

**Şu anda aktif reseed sunucuları (ağ başlangıç sunucuları)** (Ekim 2025 itibarıyla):

- https://reseed.i2p.rocks/
- https://reseed-fr.i2pd.xyz/
- https://i2p.novg.net/
- https://i2p-projekt.de/

Varsayılanlarla ilgili sorun yaşıyorsanız özel URL'ler olarak ekleyin.

**Yoğun sansür uygulanan bölgelerdeki kullanıcılar için:**

İlk reseed (ağ başlangıç tohumlaması) için Tor üzerinden Snowflake/Meek köprülerini kullanmayı düşünün; entegrasyon tamamlandığında doğrudan I2P’ye geçin. Ya da sansür bölgesinin dışından steganografi, e-posta veya USB yoluyla i2pseeds.su3 edinin.

## Ek yardıma ne zaman başvurmalı

Bu kılavuz, I2P ile ilgili sorunların çok büyük çoğunluğunu kapsar, ancak bazıları geliştiricilerin dikkatini veya topluluğun uzmanlığını gerektirir.

**Şu durumlarda I2P topluluğundan yardım isteyin:**

- Tüm sorun giderme adımlarını uyguladıktan sonra router sürekli çöküyor
- Ayrılan heap'i aşan sürekli büyümeye neden olan bellek sızıntıları
- Yeterli yapılandırmaya rağmen tunnel başarı oranı %20'nin altında kalıyor  
- Günlüklerde bu kılavuzda ele alınmayan yeni hatalar
- Güvenlik açıkları keşfedildi
- Özellik talepleri veya iyileştirme önerileri

**Yardım istemeden önce, tanılama bilgilerini toplayın:**

1. I2P sürümü: http://127.0.0.1:7657 (örn., "2.10.0")
2. Java sürümü: `java -version` çıktısı
3. İşletim sistemi ve sürümü
4. Router durumu: Ağ durumu, Aktif eş sayısı, Katılınan tunnels
5. Bant genişliği yapılandırması: Gelen/Giden sınırları
6. Port yönlendirme durumu: Firewalled (güvenlik duvarı arkasında) veya OK
7. İlgili günlük alıntıları: http://127.0.0.1:7657/logs adresinden hataları gösteren son 50 satır

**Resmi destek kanalları:**

- **Forum:** https://i2pforum.net (açık internet) veya http://i2pforum.i2p (I2P içinde)
- **IRC:** #i2p Irc2P üzerinde (irc.postman.i2p I2P üzerinden) veya irc.freenode.net (açık internet)
- **Reddit:** https://reddit.com/r/i2p topluluk tartışmaları için
- **Bug tracker:** https://i2pgit.org/i2p-hackers/i2p.i2p/-/issues doğrulanmış hatalar için
- **Mailing list:** i2p-dev@lists.i2p-projekt.de geliştirme soruları için

**Gerçekçi beklentiler önemlidir.** I2P, temel tasarımı gereği clearnet (açık internet)'ten daha yavaştır - çok atlamalı şifreli tunnel kullanımı içkin bir gecikme yaratır. Sayfaların 30 saniyede yüklenmesi ve 50 KB/sn torrent hızlarıyla çalışan bir I2P router **doğru şekilde çalışıyor**, bozuk değildir. Yapılandırma optimizasyonundan bağımsız olarak clearnet hızlarını bekleyen kullanıcılar hayal kırıklığına uğrayacaktır.

## Sonuç

Çoğu I2P sorunu üç kategoriden kaynaklanır: bootstrap (ağla ilk bağlantı) sırasında yetersiz sabır (10-15 dakika gerekir), yetersiz kaynak tahsisi (en az 512 MB RAM, 256 KB/sn bant genişliği) veya yanlış yapılandırılmış port yönlendirme. I2P'nin dağıtık mimarisini ve anonimliğe odaklı tasarımını anlamak, kullanıcıların beklenen davranışı gerçek sorunlardan ayırt etmelerine yardımcı olur.

router'ın "Firewalled" durumu, ideal olmasa da, I2P kullanımını engellemez - yalnızca ağa katkıyı sınırlar ve performansı biraz düşürür. Yeni kullanıcılar **optimizasyon yerine kararlılığa** öncelik vermelidir: entegrasyon çalışma süresiyle kendiliğinden iyileştiğinden, gelişmiş ayarları değiştirmeden önce router'ı birkaç gün boyunca kesintisiz çalıştırın.

Sorun giderirken, önce her zaman temel unsurları doğrulayın: doğru sistem saati, yeterli bant genişliği, router'ın kesintisiz çalışması ve 10'dan fazla aktif eş. Sorunların çoğu, anlaşılması güç yapılandırma parametrelerini ayarlamaya çalışmaktansa bu temel konuları ele alarak çözülür. I2P, router günler ve haftalar süren çalışma süresi boyunca itibar kazanıp eş seçimini optimize ettikçe, sabır ve kesintisiz çalışmayı daha iyi performansla ödüllendirir.
