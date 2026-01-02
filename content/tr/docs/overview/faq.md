---
title: "Sıkça Sorulan Sorular"
description: "Kapsamlı I2P SSS: router yardımı, yapılandırma, reseed'ler, gizlilik/güvenlik, performans ve sorun giderme"
slug: "faq"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## I2P Router Yardım

### I2P hangi sistemlerde çalışır? {#systems}

I2P, Java programlama dilinde yazılmıştır. Windows, Linux, FreeBSD ve OSX üzerinde test edilmiştir. Ayrıca bir Android portu da mevcuttur.

Bellek kullanımı açısından, I2P varsayılan olarak 128 MB RAM kullanacak şekilde yapılandırılmıştır. Bu miktar web gezintisi ve IRC kullanımı için yeterlidir. Ancak diğer aktiviteler daha fazla bellek tahsisi gerektirebilir. Örneğin, yüksek bant genişlikli bir router çalıştırmak, I2P torrentlerine katılmak veya yüksek trafikli gizli servisleri barındırmak istiyorsanız, daha yüksek miktarda bellek gereklidir.

CPU kullanımı açısından, I2P'nin Raspberry Pi gibi tek kartlı bilgisayar serilerinde çalışabildiği test edilmiştir. I2P kriptografik teknikleri yoğun bir şekilde kullandığından, daha güçlü bir CPU hem I2P tarafından oluşturulan iş yükünü hem de sistemin geri kalanıyla ilgili görevleri (yani İşletim Sistemi, GUI, Web Tarayıcısı gibi Diğer süreçler) daha iyi yönetebilir.

Sun/Oracle Java veya OpenJDK kullanılması önerilir.

### I2P kullanmak için Java yüklemek gerekli mi? {#java}

Evet, I2P Core kullanmak için Java gereklidir. Windows, Mac OSX ve Linux için kolay kurulum paketlerimizin içinde Java bulunmaktadır. I2P Android uygulamasını çalıştırıyorsanız, çoğu durumda Dalvik veya ART gibi bir Java çalışma ortamının kurulu olması gerekir.

### "I2P Site" nedir ve tarayıcımı bunları kullanabilmek için nasıl yapılandırırım? {#I2P-Site}

I2P Sitesi, I2P içinde barındırılması dışında normal bir web sitesidir. I2P siteleri, insanların yararı için insan tarafından okunabilir, kriptografik olmayan bir şekilde ".i2p" ile biten normal internet adresleri gibi görünen adreslere sahiptir. Aslında bir I2P Sitesine bağlanmak kriptografi gerektirir, bu da I2P Site adreslerinin aynı zamanda uzun "Base64" Destinations ve daha kısa "B32" adresleri olduğu anlamına gelir. Doğru şekilde göz atmak için ek yapılandırma yapmanız gerekebilir. I2P Sitelerine göz atmak, I2P kurulumunuzda HTTP Proxy'yi etkinleştirmenizi ve ardından tarayıcınızı bunu kullanacak şekilde yapılandırmanızı gerektirecektir. Daha fazla bilgi için aşağıdaki "Tarayıcılar" bölümüne veya "Tarayıcı Yapılandırması" Kılavuzuna göz atın.

### Router konsolundaki Aktif x/y sayıları ne anlama gelir? {#active}

Router konsolunuzdaki Eşler (Peers) sayfasında iki sayı görebilirsiniz - Aktif x/y. İlk sayı, son birkaç dakikada mesaj gönderdiğiniz veya mesaj aldığınız eş sayısıdır. İkinci sayı ise yakın zamanda görülen eş sayısıdır, bu her zaman ilk sayıdan büyük veya ona eşit olacaktır.

### Router'ımda çok az aktif eş var, bu normal mi? {#peers}

Evet, bu normal olabilir, özellikle router yeni başlatıldığında. Yeni routerların başlatılması ve ağın geri kalanına bağlanması için zamana ihtiyacı vardır. Ağ entegrasyonunu, çalışma süresini ve performansı iyileştirmeye yardımcı olmak için şu ayarları gözden geçirin:

- **Bant genişliği paylaşımı** - Bir router bant genişliği paylaşacak şekilde yapılandırılırsa, diğer router'lar için daha fazla trafik yönlendirir, bu da hem ağın geri kalanıyla entegrasyonunu sağlar hem de yerel bağlantının performansını iyileştirir. Bu, [http://localhost:7657/config](http://localhost:7657/config) sayfasında yapılandırılabilir.
- **Ağ arayüzü** - [http://localhost:7657/confignet](http://localhost:7657/confignet) sayfasında belirtilmiş bir arayüz olmadığından emin olun. Bilgisayarınız birden fazla harici IP adresine sahip çok yollu (multi-homed) bir sistem değilse, bu performansı düşürebilir.
- **I2NP protokolü** - Router'ın, ana bilgisayarın işletim sistemi ve boş ağ (Gelişmiş) ayarları için geçerli bir protokol üzerinden bağlantı bekleyecek şekilde yapılandırıldığından emin olun. Ağ yapılandırma sayfasındaki 'Hostname' alanına bir IP adresi girmeyin. Burada seçtiğiniz I2NP Protokolü yalnızca henüz ulaşılabilir bir adresiniz yoksa kullanılacaktır. Örneğin, Amerika Birleşik Devletleri'ndeki çoğu Verizon 4G ve 5G kablosuz bağlantısı UDP'yi engeller ve bu protokol üzerinden erişilemez. Diğerleri ise UDP'yi kendilerine uygun olsa bile zorla kullanır. Listelenen I2NP Protokollerinden makul bir ayar seçin.

### Belirli içerik türlerine karşıyım. Bunları dağıtmaktan, depolamaktan veya erişmekten nasıl kaçınırım? {#badcontent}

Bu materyallerin hiçbiri varsayılan olarak yüklenmez. Ancak I2P eşler arası bir ağ olduğundan, kazara yasaklanmış içerikle karşılaşmanız mümkündür. I2P'nin sizi inançlarınızın ihlali konusunda gereksiz yere dahil olmaktan nasıl koruduğuna dair bir özet:

- **Dağıtım** - Trafik I2P ağının içinde kalır, siz bir [çıkış düğümü](#exit) değilsiniz (belgelerimizde outproxy olarak adlandırılır).
- **Depolama** - I2P ağı dağıtılmış içerik depolaması yapmaz, bu özelliğin kullanıcı tarafından özel olarak kurulması ve yapılandırılması gerekir (örneğin Tahoe-LAFS ile). Bu, farklı bir anonim ağ olan [Freenet](http://freenetproject.org/)'in bir özelliğidir. Bir I2P router çalıştırarak kimse için içerik depolamış olmuyorsunuz.
- **Erişim** - Router'ınız sizin özel talimatınız olmadan herhangi bir içerik talep etmeyecektir.

### I2P'yi engellemek mümkün mü? {#blocking}

Evet, açık ara en kolay ve en yaygın yol bootstrap veya "Reseed" sunucularını engellemektir. Tüm gizlenmiş trafiği tamamen engellemek de işe yarar (ancak bu I2P olmayan pek çok şeyi bozar ve çoğu kişi bu kadar ileri gitmeye istekli değildir). Reseed engellemesi durumunda, Github'da bir reseed paketi bulunmaktadır, bunu engellemek Github'ı da engelleyecektir. Bir proxy üzerinden reseed yapabilirsiniz (Tor kullanmak istemiyorsanız İnternet'te birçok proxy bulunabilir) veya reseed paketlerini çevrimdışı olarak arkadaştan arkadaşa paylaşabilirsiniz.

### Router Console yüklenirken `wrapper.log` dosyasında "`Protocol family unavailable`" hatası görüyorum {#protocolfamily}

Bu hata, varsayılan olarak IPv6 kullanacak şekilde yapılandırılmış bazı sistemlerde, ağ etkinleştirilmiş herhangi bir java yazılımında ortaya çıkabilir. Bunu çözmenin birkaç yolu vardır:

- Linux tabanlı sistemlerde, `echo 0 > /proc/sys/net/ipv6/bindv6only` komutunu çalıştırabilirsiniz
- `wrapper.config` dosyasında aşağıdaki satırları arayın:
  ```
  #wrapper.java.additional.5=-Djava.net.preferIPv4Stack=true
  #wrapper.java.additional.6=-Djava.net.preferIPv6Addresses=false
  ```
  Bu satırlar mevcutsa, "#" işaretlerini kaldırarak yorum satırından çıkarın. Satırlar mevcut değilse, "#" işaretleri olmadan ekleyin.

Başka bir seçenek, `~/.i2p/clients.config` dosyasından `::1` ifadesini kaldırmak olabilir

**UYARI**: `wrapper.config` dosyasındaki herhangi bir değişikliğin etkili olması için router'ı ve wrapper'ı tamamen durdurmanız gerekir. Router konsolunuzda *Yeniden Başlat* seçeneğine tıklamak bu dosyayı TEKRAR OKUMAYACAKTIR! *Kapat* seçeneğine tıklamanız, 11 dakika beklemeniz ve ardından I2P'yi başlatmanız gerekir.

### I2P içindeki I2P Sitelerinin çoğu kapalı mı? {#down}

Şimdiye kadar oluşturulmuş tüm I2P Sitelerini düşünürseniz, evet, çoğu çevrimdışı. İnsanlar ve I2P Siteleri gelir gider. I2P'ye başlamak için iyi bir yol, şu anda aktif olan I2P Sitelerinin bir listesine göz atmaktır. [identiguy.i2p](http://identiguy.i2p) aktif I2P Sitelerini takip eder.

### I2P neden 32000 portunu dinliyor? {#port32000}

Kullandığımız Tanuki java servis sarmalayıcısı, JVM içinde çalışan yazılımla iletişim kurmak için bu portu — localhost'a bağlı olarak — açar. JVM başlatıldığında, sarmalayıcıya bağlanabilmesi için bir anahtar verilir. JVM, sarmalayıcıya bağlantısını kurduktan sonra, sarmalayıcı herhangi bir ek bağlantıyı reddeder.

Daha fazla bilgi [wrapper belgelerinde](http://wrapper.tanukisoftware.com/doc/english/prop-port.html) bulunabilir.

### Tarayıcımı nasıl yapılandırırım? {#browserproxy}

Farklı tarayıcılar için proxy yapılandırması, ekran görüntüleriyle birlikte ayrı bir sayfadadır. FoxyProxy tarayıcı eklentisi veya Privoxy proxy sunucusu gibi harici araçlarla daha gelişmiş yapılandırmalar mümkündür ancak kurulumunuzda sızıntılara neden olabilir.

### I2P içinde IRC'ye nasıl bağlanırım? {#irc}

I2P içindeki ana IRC sunucusuna, Irc2P'ye bir tunnel, I2P kurulduğunda oluşturulur ([I2PTunnel yapılandırma sayfasına](http://localhost:7657/i2ptunnel/index.jsp) bakın) ve I2P router başladığında otomatik olarak başlatılır. Bağlanmak için IRC istemcinize `localhost 6668`'e bağlanmasını söyleyin. HexChat benzeri istemci kullanıcıları `localhost/6668` sunucusuyla yeni bir ağ oluşturabilir (bir proxy sunucu yapılandırdıysanız "Bypass proxy server" seçeneğini işaretlemeyi unutmayın). Weechat kullanıcıları yeni bir ağ eklemek için aşağıdaki komutu kullanabilir:

```
/server add irc2p localhost/6668
```
### Kendi I2P Sitemi nasıl kurarım? {#myI2P-Site}

En kolay yöntem, router konsolundaki [i2ptunnel](http://127.0.0.1:7657/i2ptunnel/) bağlantısına tıklayıp yeni bir 'Sunucu Tüneli' oluşturmaktır. Tünel hedefini Tomcat veya Jetty gibi mevcut bir web sunucusunun portuna ayarlayarak dinamik içerik sunabilirsiniz. Statik içerik de sunabilirsiniz. Bunun için tünel hedefini: `0.0.0.0 port 7659` olarak ayarlayın ve içeriği `~/.i2p/eepsite/docroot/` dizinine yerleştirin. (Linux dışı sistemlerde bu farklı bir yerde olabilir. Router konsolunu kontrol edin.) 'eepsite' yazılımı I2P kurulum paketinin bir parçası olarak gelir ve I2P başlatıldığında otomatik olarak başlayacak şekilde ayarlanmıştır. Oluşturulan varsayılan siteye http://127.0.0.1:7658 adresinden erişilebilir. Ancak, 'eepsite'ınıza başkaları da eepsite anahtar dosyanız üzerinden erişebilir, dosya konumu: `~/.i2p/eepsite/i2p/eepsite.keys`. Daha fazla bilgi için şu konumdaki readme dosyasını okuyun: `~/.i2p/eepsite/README.txt`.

### Evde I2P üzerinde yalnızca HTML ve CSS içeren bir web sitesi barındırırsam, tehlikeli midir? {#hosting}

Rakibinize ve tehdit modelinize bağlıdır. Yalnızca kurumsal "gizlilik" ihlalleri, tipik suçlular ve sansür konusunda endişeleniyorsanız, gerçekten tehlikeli değildir. Kolluk kuvvetleri gerçekten isterlerse muhtemelen sizi zaten bulacaktır. Yalnızca normal bir (internet) ev kullanıcı tarayıcısı çalışırken barındırma yapmak, o bölümü kimin barındırdığını bilmeyi gerçekten zorlaştıracaktır. Lütfen I2P sitenizi barındırmayı, diğer herhangi bir hizmeti barındırmak gibi düşünün - ne kadar tehlikeli - veya güvenli - olduğu, onu nasıl yapılandırıp yönettiğinize bağlıdır.

Not: Bir i2p hizmetini (destination) i2p router'dan ayırmanın zaten bir yolu var. Eğer bunun [nasıl çalıştığını](/docs/overview/tech-intro#i2pservices) anlıyorsanız, o zaman web sitesi (veya hizmet) için ayrı bir makineyi sunucu olarak kurabilir, bu sunucuyu halka açık hale getirebilir ve [son derece] güvenli bir SSH tüneli üzerinden web sunucusuna yönlendirebilir veya güvenli, paylaşımlı bir dosya sistemi kullanabilirsiniz.

### I2P ".i2p" web sitelerini nasıl bulur? {#addresses}

I2P Adres Defteri uygulaması, insan tarafından okunabilir isimleri hizmetlerle ilişkilendirilmiş uzun vadeli hedeflerle eşleştirir, bu da onu bir ağ veritabanı veya DNS hizmetinden ziyade bir hosts dosyasına veya kişi listesine benzer hale getirir. Ayrıca yerel önceliklidir (local-first) - tanınmış bir küresel ad alanı yoktur, herhangi bir .i2p alan adının sonuçta neye eşleşeceğine siz karar verirsiniz. Orta yol ise "Jump Service" (atlama hizmeti) olarak adlandırılan bir şeydir; bu hizmet, sizi "I2P router'ına $SITE_CRYPTO_KEY'i $SITE_NAME.i2p adıyla çağırma izni veriyor musunuz?" veya bu yönde bir soru sorulacak bir sayfaya yönlendirerek insan tarafından okunabilir bir isim sağlar. Adres defterinize eklendikten sonra, siteyi başkalarıyla paylaşmaya yardımcı olmak için kendi jump URL'lerinizi oluşturabilirsiniz.

### Adres Defterine nasıl adres eklerim? {#addressbook}

Ziyaret etmek istediğiniz sitenin en azından base32 veya base64 adresini bilmeden bir adres ekleyemezsiniz. İnsan tarafından okunabilen "hostname" (ana makine adı), base32 veya base64'e karşılık gelen kriptografik adresin yalnızca bir takma adıdır. Kriptografik adres olmadan bir I2P Sitesine erişmenin hiçbir yolu yoktur, bu tasarım gereğidir. Adresi henüz bilmeyen kişilere dağıtmak genellikle Jump servis sağlayıcısının sorumluluğundadır. Bilinmeyen bir I2P Sitesini ziyaret etmek, bir Jump servisinin kullanımını tetikler. stats.i2p en güvenilir Jump servisidir.

Eğer i2ptunnel üzerinden bir site barındırıyorsanız, henüz bir jump servisi kaydı olmayacaktır. Yerel olarak bir URL vermek için yapılandırma sayfasını ziyaret edin ve "Yerel Adres Defterine Ekle" yazan düğmeye tıklayın. Ardından addresshelper URL'sini aramak için http://127.0.0.1:7657/dns adresine gidin ve paylaşın.

### I2P hangi portları kullanır? {#ports}

I2P tarafından kullanılan portlar 2 bölüme ayrılabilir:

1. Diğer I2P yönlendiricileriyle iletişim için kullanılan, İnternet'e açık portlar
2. Yerel bağlantılar için yerel portlar

Bunlar aşağıda detaylı olarak açıklanmıştır.

#### 1. İnternet'e açık portlar

Not: 0.7.8 sürümünden itibaren, yeni kurulumlar 8887 portunu kullanmaz; program ilk kez çalıştırıldığında 9000 ile 31000 arasında rastgele bir port seçilir. Seçilen port, router [yapılandırma sayfasında](http://127.0.0.1:7657/confignet) gösterilir.

**GİDEN**

- [yapılandırma sayfasında](http://127.0.0.1:7657/confignet) listelenen rastgele porttan rastgele uzak UDP portlarına UDP, yanıtlara izin verir
- Rastgele yüksek portlardan rastgele uzak TCP portlarına TCP
- 123 numaralı portta giden UDP, yanıtlara izin verir. Bu, I2P'nin dahili zaman senkronizasyonu için gereklidir (SNTP aracılığıyla - pool.ntp.org içinde rastgele bir SNTP sunucusuna veya belirttiğiniz başka bir sunucuya sorgu gönderme)

**GELEN**

- (İsteğe bağlı, önerilir) Rastgele konumlardan [yapılandırma sayfasında](http://127.0.0.1:7657/confignet) belirtilen porta UDP
- (İsteğe bağlı, önerilir) Rastgele konumlardan [yapılandırma sayfasında](http://127.0.0.1:7657/confignet) belirtilen porta TCP
- Gelen TCP [yapılandırma sayfasında](http://127.0.0.1:7657/confignet) devre dışı bırakılabilir

#### 2. Yerel I2P portları

Yerel I2P portları, aksi belirtilmedikçe varsayılan olarak yalnızca yerel bağlantıları dinler:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PORT</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PURPOSE</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">DESCRIPTION</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1900</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UPnP SSDP UDP multicast listener</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cannot be changed. Binds to all interfaces. May be disabled on <a href="http://127.0.0.1:7657/confignet">confignet</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2827</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A higher level socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a>. May be changed in the bob.config file.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4444</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/0">I2P HTTP Proxy</a> to configure it. Include in your browser's proxy configuration for HTTP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4445</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/1">I2P HTTPS Proxy</a> to configure it. Include in your browser's proxy configuration for HTTPS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6668</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IRC proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A tunnel to the inside-the-I2P IRC network. Disabled by default. Configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/2">irc.postman.i2p (IRC proxy)</a> and may be enabled/disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7654</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2CP (client protocol) port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For advanced client usage. Do not expose to an external network.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7656</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a> and configured on <a href="http://127.0.0.1:7657/sam">sam</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7657 (or 7658 via SSL)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router console</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The router console provides valuable information about your router and the network, in addition to giving you access to configure your router and its associated applications.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7659</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">'eepsite' - an example webserver (Jetty)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Included in the <code>i2pinstall</code> and <code>i2pupdate</code> packages - may be disabled if another webserver is available. May be configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/3">eepsite</a> and disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7660</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel UDP port for SSH</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Required for Grizzled's/novg's UDP support. Instances disabled by default. May be enabled/disabled and configured to use a different port on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">123</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTP Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used by <a href="http://127.0.0.1:7657/confignet">NTP Time Sync</a>. May be disabled/changed.</td>
    </tr>
  </tbody>
</table>
### Adres defterimdeki birçok sunucu eksik. İyi abonelik bağlantıları nelerdir? {#subscriptions}

Adres defteri [http://localhost:7657/dns](http://localhost:7657/dns) adresinde bulunur ve daha fazla bilgi burada edinilabilir.

**İyi adres defteri abonelik bağlantıları nelerdir?**

Aşağıdakileri deneyebilirsiniz:

- [http://stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
- [http://identiguy.i2p/hosts.txt](http://identiguy.i2p/hosts.txt)

### Web konsoluna diğer makinelerimden nasıl erişebilirim veya şifre koruması nasıl eklerim? {#remote_webconsole}

Güvenlik amaçları doğrultusunda, router'ın yönetim konsolu varsayılan olarak yalnızca yerel arayüzden gelen bağlantıları dinler.

Konsola uzaktan erişim için iki yöntem bulunmaktadır:

1. SSH Tüneli
2. Konsolunuzu genel bir IP adresinde kullanıcı adı ve şifre ile erişilebilir hale getirme

Bunlar aşağıda ayrıntılı olarak açıklanmıştır:

**Yöntem 1: SSH Tüneli**

Unix benzeri bir İşletim Sistemi çalıştırıyorsanız, bu I2P konsolunuza uzaktan erişim için en kolay yöntemdir. (Not: SSH sunucu yazılımı Windows çalıştıran sistemler için de mevcuttur, örneğin [https://github.com/PowerShell/Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH))

Sisteminize SSH erişimini yapılandırdıktan sonra, '-L' bayrağı uygun argümanlarla SSH'ye iletilir - örneğin:

```
ssh -L 7657:localhost:7657 (System_IP)
```
burada '(System_IP)' yerine Sisteminizin IP adresi yazılır. Bu komut 7657 portunu (ilk iki noktadan önceki sayı) uzak sistemin (ilk ve ikinci iki nokta arasındaki 'localhost' dizesi tarafından belirtilen) 7657 portuna (ikinci iki noktadan sonraki sayı) yönlendirir. Uzak I2P konsolunuz artık yerel sisteminizde 'http://localhost:7657' olarak erişilebilir olacak ve SSH oturumunuz aktif olduğu sürece kullanılabilir kalacaktır.

Uzak sistemde bir kabuk başlatmadan bir SSH oturumu başlatmak istiyorsanız, '-N' bayrağını ekleyebilirsiniz:

```
ssh -NL 7657:localhost:7657 (System_IP)
```
**Yöntem 2: Konsolunuzu bir Genel IP adresinde kullanıcı adı ve şifre ile erişilebilir olacak şekilde yapılandırma**

1. `~/.i2p/clients.config` dosyasını açın ve şunu:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
   ```
   bununla değiştirin:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1,(System_IP) ./webapps/
   ```
   burada (System_IP) yerine sisteminizin genel IP adresini yazın

2. [http://localhost:7657/configui](http://localhost:7657/configui) adresine gidin ve isterseniz bir konsol kullanıcı adı ve şifresi ekleyin - I2P konsolunuzu kurcalamaya karşı güvence altına almak için bir kullanıcı adı ve şifre eklemeniz şiddetle tavsiye edilir, aksi takdirde anonimliğinizin bozulmasına yol açabilir.

3. [http://localhost:7657/index](http://localhost:7657/index) adresine gidin ve JVM'i yeniden başlatıp istemci uygulamalarını yeniden yükleyen "Graceful restart" seçeneğine tıklayın

Bundan sonra başlatıldığında, artık konsolunuza uzaktan erişebilmeniz gerekir. Router konsolunu `http://(Sistem_IP):7657` adresinden yükleyin ve tarayıcınız kimlik doğrulama açılır penceresini destekliyorsa, yukarıdaki 2. adımda belirttiğiniz kullanıcı adı ve şifre istenecektir.

NOT: Yukarıdaki yapılandırmada 0.0.0.0 belirtebilirsiniz. Bu bir ağ veya netmask değil, bir arayüz belirtir. 0.0.0.0 "tüm arayüzlere bağlan" anlamına gelir, böylece 127.0.0.1:7657 üzerinden ve herhangi bir LAN/WAN IP'si üzerinden erişilebilir olur. Bu seçeneği kullanırken dikkatli olun çünkü konsol sisteminizde yapılandırılmış TÜM adreslerde erişilebilir olacaktır.

### Diğer makinelerden uygulamaları nasıl kullanabilirim? {#remote_i2cp}

SSH Port Forwarding kullanımı için lütfen önceki cevaba bakın ve ayrıca konsolunuzdaki şu sayfaya da göz atın: [http://localhost:7657/configi2cp](http://localhost:7657/configi2cp)

### I2P'yi bir SOCKS proxy olarak kullanmak mümkün mü? {#socks}

SOCKS proxy, 0.7.1 sürümünden beri çalışmaktadır. SOCKS 4/4a/5 desteklenmektedir. I2P'nin bir SOCKS outproxy'si olmadığı için kullanımı yalnızca I2P içindedir.

Birçok uygulama, sizi İnternet üzerinde tanımlayabilecek hassas bilgileri sızdırır ve bu, I2P SOCKS proxy kullanırken farkında olunması gereken bir risktir. I2P yalnızca bağlantı verilerini filtreler, ancak çalıştırmayı düşündüğünüz program bu bilgileri içerik olarak gönderirse, I2P anonimliğinizi koruyamaz. Örneğin, bazı e-posta uygulamaları üzerinde çalıştıkları makinenin IP adresini bir posta sunucusuna gönderir. I2P'ye özel araçlar veya uygulamalar ([I2PSnark](http://localhost:7657/i2psnark/) gibi torrent uygulamaları için) veya [Firefox](https://www.mozilla.org/) üzerinde bulunan popüler eklentiler dahil olmak üzere I2P ile güvenli olduğu bilinen uygulamalar öneriyoruz.

### Normal İnternet'te IRC, BitTorrent veya diğer hizmetlere nasıl erişebilirim? {#proxy_other}

I2P ile İnternet arasında köprü görevi gören, Tor Çıkış Düğümleri (Exit Nodes) gibi Outproxy adı verilen hizmetler bulunmaktadır. HTTP ve HTTPS için varsayılan outproxy işlevselliği `exit.stormycloud.i2p` tarafından sağlanır ve StormyCloud Inc. tarafından işletilir. Bu, HTTP Proxy'de yapılandırılır. Ek olarak, anonimliği korumaya yardımcı olmak için I2P, varsayılan olarak normal İnternet'e anonim bağlantılar kurmanıza izin vermez. Daha fazla bilgi için lütfen [Socks Outproxy](/docs/api/socks#outproxy) sayfasına bakın.

---

## Reseed'ler

### Router'ım birkaç dakikadır çalışıyor ancak hiç ya da çok az bağlantım var {#reseed}

Öncelikle Router Console'daki [http://127.0.0.1:7657/netdb](http://127.0.0.1:7657/netdb) sayfasını kontrol edin – ağ veritabanınız. I2P içinden listelenmiş tek bir router görmüyorsanız ancak konsol güvenlik duvarının arkasında olduğunuzu söylüyorsa, muhtemelen reseed sunucularına bağlanamıyorsunuzdur. Diğer I2P router'ları listelenmiş olarak görüyorsanız, [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config) adresinden maksimum bağlantı sayısını düşürmeyi deneyin, router'ınız çok fazla bağlantıyı kaldıramıyor olabilir.

### Manuel olarak nasıl reseed yapabilirim? {#manual_reseed}

Normal koşullar altında, I2P sizi bootstrap bağlantılarımızı kullanarak ağa otomatik olarak bağlar. Kesintili internet reseed sunucularından bootstrap yapılmasını başarısız kılıyorsa, bootstrap yapmanın kolay bir yolu Tor tarayıcısını kullanmaktır (Varsayılan olarak localhost'u açar), [http://127.0.0.1:7657/configreseed](http://127.0.0.1:7657/configreseed) ile çok iyi çalışır. Bir I2P router'ını manuel olarak reseed etmek de mümkündür.

Yeniden tohum ekleme (reseed) için Tor tarayıcısını kullanırken, aynı anda birden fazla URL seçebilir ve devam edebilirsiniz. Varsayılan değer olan 2 (birden fazla url'den) de çalışacaktır ancak yavaş olacaktır.

---

## Gizlilik-Güvenlik

### Router'ım normal İnternet'e bir "çıkış düğümü" (outproxy) mü? Olmasını istemiyorum. {#exit}

Hayır, router'ınız şifrelenmiş uçtan uca trafiğin i2p ağı üzerinden rastgele bir tunnel uç noktasına taşınmasına katılır, genellikle bir outproxy değildir, ancak router'ınız ile İnternet arasında transport katmanı üzerinden trafik geçişi olmaz. Son kullanıcı olarak, sistem ve ağ yönetiminde yetenekli değilseniz outproxy çalıştırmamalısınız.

### Ağ trafiğini analiz ederek I2P kullanımını tespit etmek kolay mıdır? {#detection}

I2P trafiği genellikle UDP trafiği gibi görünür ve bundan fazlası değil – ve bundan fazlası gibi görünmemesi bir hedeftir. Ayrıca TCP'yi de destekler. Biraz çabayla, pasif trafik analizi trafiği "I2P" olarak sınıflandırabilir, ancak trafik gizlemenin sürekli geliştirilmesinin bunu daha da azaltacağını umuyoruz. Obfs4 gibi oldukça basit bir protokol gizleme katmanı bile sansürcülerin I2P'yi engellemesini önleyecektir (I2P'nin dağıtacağı bir hedeftir).

### I2P Kullanmak Güvenli mi? {#safe}

Kişisel tehdit modelinize bağlıdır. Çoğu insan için I2P, hiçbir koruma kullanmamaktan çok daha güvenlidir. Bazı diğer ağlar (Tor, mixminion/mixmaster gibi), belirli düşmanlara karşı muhtemelen daha güvenlidir. Örneğin, I2P trafiği TLS/SSL kullanmaz, bu nedenle Tor'un sahip olduğu "en zayıf halka" sorunlarına sahip değildir. I2P, "Arap Baharı" sırasında Suriye'de birçok kişi tarafından kullanıldı ve son zamanlarda proje, Yakın ve Orta Doğu'daki daha küçük dil dilimlerinde I2P kurulumlarında daha büyük bir büyüme gördü. Burada belirtilmesi gereken en önemli şey, I2P'nin bir teknoloji olduğu ve İnternet'te gizliliğinizi/anonimliğinizi artırmak için bir nasıl yapılır/kılavuza ihtiyacınız olmasıdır. Ayrıca tarayıcınızı kontrol edin veya parmak izi saldırılarını çok büyük (yani: tipik uzun kuyruklar / çok doğru çeşitli veri yapısı) bir veri setiyle engellemek için parmak izi-arama-motorunu içe aktarın, bu veri seti birçok ortam öğesi hakkındadır ve kendi TLS önbellek davranışı ve sağlayıcı işletmesinin kendi masaüstü sisteminden daha kolay hacklenebilen teknik yapısı gibi kendisinden kaynaklanan tüm riskleri azaltmak için VPN kullanmayın. İzole bir Tor V-Browser'ı harika parmak izi önleme korumaları ile kullanmak ve yalnızca gerekli sistem iletişimlerine izin veren genel bir uygulama koruma-yaşam süresi-koruması ve "neredeyse kalıcı olası risk"i ortadan kaldırmak için casus karşıtı devre dışı bırakma betikleri ve canlı-cd ile son bir sanal makine kullanımı ve azalan olasılıkla tüm riskleri düşürmek, kamusal ağlarda ve en yüksek bireysel risk modelinde iyi bir seçenek olabilir ve i2p kullanımı için bu hedefe ulaşmak için yapabileceğiniz en iyi şey olabilir.

### Router konsolunda diğer tüm I2P node'larının IP adreslerini görüyorum. Bu benim IP adresimin de başkaları tarafından görülebildiği anlamına mı geliyor? {#netdb_ip}

Evet, router'ınız hakkında bilgi sahibi olan diğer I2P düğümleri için. Bunu I2P ağının geri kalanıyla bağlantı kurmak için kullanırız. Adresler fiziksel olarak "routerInfo'larda (anahtar,değer) nesnelerinde" bulunur; bunlar uzaktan alınır veya eşlerden (peer) alınır. "routerInfo'lar", router'ın kendisi hakkında önyükleme (bootstrapping) için "eş tarafından yayınlanan" bazı bilgileri (bazıları isteğe bağlı fırsatçı olarak eklenmiş) içerir. Bu nesnede istemciler hakkında hiçbir veri bulunmaz. Kaputun altına daha yakından bakıldığında, herkesin "SHA-256 Hash'ler (düşük=Pozitif hash(-anahtar), yüksek=Negatif hash(+anahtar))" adı verilen en yeni kimlik oluşturma türüyle sayıldığını göreceksiniz. I2P ağı, yükleme ve indeksleme sırasında oluşturulan routerInfo'ların kendi veritabanı verilerine sahiptir, ancak bu durum anahtar/değer tablolarının ve ağ topolojisinin gerçekleştirilmesine ve yük durumuna / bant genişliği durumuna ve DB bileşenlerindeki depolama için yönlendirme olasılıklarına derinlemesine bağlıdır.

### Outproxy kullanmak güvenli midir? {#proxy_safe}

"Güvenli" tanımınızın ne olduğuna bağlı. Outproxy'ler çalıştıklarında harikadır, ancak ne yazık ki gönüllü olarak, ilgisini kaybedebilecek veya bunları 7/24 sürdürecek kaynaklara sahip olmayabilecek kişiler tarafından yürütülürler – lütfen hizmetlerin kullanılamaz, kesintiye uğramış veya güvenilmez olduğu dönemler yaşayabileceğinizi unutmayın ve bu hizmetle ilişkili değiliz ve üzerinde hiçbir etkimiz yoktur.

Outproxy'lerin kendileri, uçtan uca şifrelenmiş HTTPS/SSL verileri hariç olmak üzere, trafiğinizin gelip gittiğini görebilir; tıpkı ISS'nizin (İnternet Servis Sağlayıcınızın) bilgisayarınızdan gelen ve giden trafiği görebildiği gibi. ISS'niz konusunda rahat hissediyorsanız, outproxy ile de durumun daha kötü olması söz konusu değildir.

### "Anonimliği Kaldırma" saldırıları ne olacak? {#deanon}

Çok uzun bir açıklama için [Tehdit Modeli](/docs/overview/threat-model) hakkındaki makalelerimizi okuyun. Genel olarak, kimlik tespiti önemsiz değildir, ancak yeterince dikkatli olmazsanız mümkündür.

---

## İnternet Erişimi/Performans

### I2P üzerinden normal İnternet sitelerine erişemiyorum. {#outproxy}

İnternet sitelerine proxy'leme (İnternet'e açık eepsite'lar) I2P kullanıcılarına engelleme yapmayan sağlayıcılar tarafından bir hizmet olarak sunulmaktadır. Bu hizmet I2P geliştirmesinin ana odak noktası değildir ve gönüllülük esasına göre sağlanmaktadır. I2P üzerinde barındırılan eepsite'lar her zaman outproxy olmadan çalışmalıdır. Outproxy'ler bir kolaylıktır ancak tasarım gereği ne mükemmeldir ne de projenin büyük bir parçasıdır. I2P'nin diğer hizmetlerinin sağlayabileceği yüksek kaliteli hizmeti sunamayabileceklerinin farkında olun.

### I2P üzerinden https:// veya ftp:// sitelerine erişemiyorum. {#https}

Varsayılan HTTP proxy yalnızca HTTP ve HTTPS outproxy'i destekler.

### Router'ım neden çok fazla CPU kullanıyor? {#cpu}

Öncelikle, I2P ile ilgili tüm bileşenlerin en son sürüme sahip olduğunuzdan emin olun – eski sürümlerde kodda gereksiz CPU tüketen bölümler bulunuyordu. Ayrıca, I2P performansındaki iyileştirmelerin zaman içindeki gelişimini belgeleyen bir [performans Günlüğü](/docs/overview/performance) de mevcuttur.

### Aktif eşlerim / bilinen eşlerim / katıldığım tüneller / bağlantılar / bant genişliği zaman içinde büyük ölçüde değişiyor! Bir sorun mu var? {#vary}

I2P ağının genel kararlılığı devam eden bir araştırma alanıdır. Bu araştırmanın önemli bir bölümü, yapılandırma ayarlarındaki küçük değişikliklerin router davranışını nasıl değiştirdiğine odaklanmıştır. I2P bir eşler arası ağ olduğundan, diğer eşlerin eylemleri router'ınızın performansı üzerinde etkili olacaktır.

### I2P'de indirmeler, torrent'ler, web gezintisi ve diğer her şeyi normal internete kıyasla yavaşlatan nedir? {#slow}

I2P, ekstra yönlendirme ve ek şifreleme katmanları ekleyen farklı koruma mekanizmalarına sahiptir. Ayrıca trafiği, kendi hız ve kalitesine sahip diğer eşler (Tunnels) üzerinden yönlendirir; bazıları yavaş, bazıları hızlıdır. Bu durum, farklı yönlerde farklı hızlarda çok fazla ek yük ve trafiğe neden olur. Tasarım gereği tüm bunlar, internet üzerindeki doğrudan bağlantıya kıyasla daha yavaş olmasına sebep olacaktır, ancak çok daha anonimdir ve çoğu şey için hala yeterince hızlıdır.

Aşağıda, I2P kullanırken gecikme ve bant genişliği konularına bağlam sağlamaya yardımcı olmak için açıklamalı bir örnek sunulmuştur.

Aşağıdaki diyagramı inceleyin. I2P üzerinden istek yapan bir istemci, I2P üzerinden isteği alan bir sunucu ve ardından yine I2P üzerinden geri yanıt veren bir sunucu arasındaki bağlantıyı göstermektedir. İsteğin üzerinden geçtiği devre de gösterilmiştir.

Diyagramdan, 'P', 'Q' ve 'R' etiketli kutuların 'A' için bir giden tüneli temsil ettiğini ve 'X', 'Y' ve 'Z' etiketli kutuların 'B' için bir giden tüneli temsil ettiğini düşünün. Benzer şekilde, 'X', 'Y' ve 'Z' etiketli kutular 'B' için bir gelen tüneli temsil ederken 'P_1', 'Q_1' ve 'R_1' etiketli kutular 'A' için bir gelen tüneli temsil eder. Kutular arasındaki oklar trafik yönünü gösterir. Okların üstündeki ve altındaki metinler, bir çift atlama arasındaki örnek bant genişliğinin yanı sıra örnek gecikme sürelerini detaylandırır.

Hem istemci hem de sunucu baştan sona 3 atlamalı tunnel'lar kullandığında, trafiği aktarmada toplam 12 başka I2P router'ı görev alır. 6 eş, istemciden sunucuya olan trafiği aktarır; bu trafik 'A'dan ('P', 'Q', 'R') 3 atlamalı bir giden tunnel'a ve 'B'ye ('X', 'Y', 'Z') 3 atlamalı bir gelen tunnel'a bölünür. Benzer şekilde, 6 eş sunucudan istemciye geri dönen trafiği aktarır.

İlk olarak, gecikmeyi düşünebiliriz - bir istemciden gelen isteğin I2P ağını geçmesi, sunucuya ulaşması ve istemciye geri dönmesi için geçen süre. Tüm gecikmeleri toplarsak şunu görürüz:

```
    40 + 100 + 20 + 60 + 80 + 10 + 30 ms        (client to server)
  + 60 + 40 + 80 + 60 + 100 + 20 + 40 ms        (server to client)
  -----------------------------------
  TOTAL:                          740 ms
```
Örneğimizdeki toplam gidiş-dönüş süresi 740 ms'ye ulaşıyor - bu, normal internet sitelerine göz atarken normalde görülenin kesinlikle çok üzerinde.

İkinci olarak, mevcut bant genişliğini düşünebiliriz. Bu, istemci ve sunucu arasındaki hop'lar (atlama noktaları) arasındaki en yavaş bağlantı ile ve ayrıca sunucu tarafından istemciye trafik iletilirken belirlenir. İstemciden sunucuya giden trafik için, örneğimizde 'R' & 'X' hop'ları ile 'X' & 'Y' hop'ları arasındaki mevcut bant genişliğinin 32 KB/s olduğunu görüyoruz. Diğer hop'lar arasında daha yüksek mevcut bant genişliği olmasına rağmen, bu hop'lar bir darboğaz görevi görecek ve 'A'dan 'B'ye olan trafik için maksimum mevcut bant genişliğini 32 KB/s ile sınırlayacaktır. Benzer şekilde, sunucudan istemciye olan yolu izlediğimizde maksimum 64 KB/s bant genişliği olduğunu görüyoruz - 'Z_1' & 'Y_1', 'Y_1' & 'X_1' ve 'Q_1' & 'P_1' hop'ları arasında.

Bant genişliği limitlerini artırmanızı öneririz. Bu, mevcut bant genişliği miktarını artırarak ağa yardımcı olur ve bunun sonucunda I2P deneyiminizi iyileştirir. Bant genişliği ayarları [http://localhost:7657/config](http://localhost:7657/config) sayfasında bulunmaktadır. Lütfen İnternet Servis Sağlayıcınız (ISP) tarafından belirlenen internet bağlantınızın limitlerinin farkında olun ve ayarlarınızı buna göre düzenleyin.

Ayrıca yeterli miktarda paylaşımlı bant genişliği ayarlamanızı öneririz - bu, katılımcı tünellerin I2P router'ınız üzerinden yönlendirilmesine olanak tanır. Katılımcı trafiğe izin vermek, router'ınızı ağa iyi entegre tutar ve aktarım hızlarınızı artırır.

I2P devam eden bir çalışmadır. Birçok iyileştirme ve düzeltme uygulanmaktadır ve genel olarak, en son sürümü çalıştırmak performansınıza yardımcı olacaktır. Henüz yapmadıysanız, en son sürümü yükleyin.

### Sanırım bir hata buldum, nerede bildirebilirim? {#bug}

Karşılaştığınız hataları/sorunları, hem normal internet hem de I2P üzerinden erişilebilen hata takip sistemimizde bildirebilirsiniz. Ayrıca hem I2P hem de normal internet üzerinden erişilebilen bir tartışma forumumuz bulunmaktadır. IRC kanalımıza da katılabilirsiniz: IRC ağımız IRC2P üzerinden veya Freenode'da.

- **Hata İzleyicimiz:**
  - Genel internet: [https://i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)
  - I2P üzerinde: [http://git.idk.i2p/I2P_Developers/i2p.i2p/issues](http://git.idk.i2p/I2P_Developers/i2p.i2p/issues)
- **Forumlarımız:** [i2pforum.i2p](http://i2pforum.i2p/)
- **Günlük kayıtlarını yapıştırın:** İlginç günlük kayıtlarını [PrivateBin Wiki](https://github.com/PrivateBin/PrivateBin/wiki/PrivateBin-Directory) sayfasında listelenen genel internet servisleri veya bu [PrivateBin örneği](http://paste.crypthost.i2p) ya da bu [Javascript-siz yapıştırma servisi](http://pasta-nojs.i2p) gibi I2P yapıştırma servislerine yapıştırabilir ve IRC'de #i2p kanalında takip edebilirsiniz
- **IRC:** #i2p-dev kanalına katılın ve geliştiricilerle IRC üzerinden görüşün

Lütfen [http://127.0.0.1:7657/logs](http://127.0.0.1:7657/logs) adresinde bulunan router günlükleri sayfasından ilgili bilgileri ekleyin. 'I2P Sürümü ve Çalışma Ortamı' bölümünün altındaki tüm metni ve sayfada gösterilen çeşitli günlüklerde görüntülenen hataları veya uyarıları paylaşmanızı rica ederiz.

---

### Bir sorum var! {#question}

Harika! Bizi IRC'de bulun:

- `irc.freenode.net` üzerinde `#i2p` kanalı
- `IRC2P` üzerinde `#i2p` kanalı

veya [foruma](http://i2pforum.i2p/) gönderin, biz de burada yayınlayalım (umarız cevabıyla birlikte).
