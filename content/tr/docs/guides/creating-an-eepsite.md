---
title: "I2P Eepsite Oluşturma"
description: "Yerleşik Jetty web sunucusunu kullanarak I2P ağında kendi web sitenizi nasıl oluşturup barındıracağınızı öğrenin"
lastUpdated: "2025-11"
toc: true
---

## Eepsite nedir?

Bir **eepsite**, yalnızca I2P ağında bulunan bir web sitesidir. Clearnet üzerinden erişilebilen geleneksel web sitelerinin aksine, eepsite'lere yalnızca I2P üzerinden erişilebilir; bu da hem site işletmecisi hem de ziyaretçiler için anonimlik ve gizlilik sağlar. Eepsite'ler `.i2p` sözde üst düzey alan adını kullanır ve özel `.b32.i2p` adresleri ya da I2P adres defterine kayıtlı, insan tarafından okunabilir adlar üzerinden erişilir.

Tüm Java I2P kurulumları, hafif, Java tabanlı bir web sunucusu olan [Jetty](https://jetty.org/index.html) ile önceden kurulmuş ve önceden yapılandırılmış şekilde gelir. Bu, birkaç dakika içinde kendi eepsite'inizi (I2P üzerinde barındırılan web sitesi) barındırmaya başlamanızı kolaylaştırır - ek bir yazılım kurulumu gerekmez.

Bu kılavuz, I2P'nin yerleşik araçlarını kullanarak ilk eepsite'inizi oluşturma ve yapılandırma sürecinde size adım adım rehberlik edecek.

---

## Adım 1: Gizli Hizmetler Yöneticisine Erişin

Gizli Servisler Yöneticisi (I2P Tunnel Manager olarak da adlandırılır), HTTP sunucuları (eepsites) dahil olmak üzere tüm I2P sunucu ve istemci tunnel yapılandırmalarını yaptığınız yerdir.

1. [I2P Router Console](http://127.0.0.1:7657)'unuzu açın
2. [Hidden Services Manager](http://127.0.0.1:7657/i2ptunnelmgr)'e gidin

Gizli Servisler Yöneticisi arayüzünde şunları görmelisiniz: - **Durum Mesajları** - Geçerli tunnel ve istemci durumu - **Genel Tunnel Kontrolü** - Tüm tunnel'ları aynı anda yönetmek için düğmeler - **I2P Gizli Servisler** - Yapılandırılmış sunucu tunnel'lerinin listesi

![Gizli Servisler Yöneticisi](/images/guides/eepsite/hidden-services-manager.png)

Varsayılan olarak, yapılandırılmış ancak başlatılmamış mevcut bir **I2P web sunucusu** kaydı göreceksiniz. Bu, kullanmanız için hazır, önceden yapılandırılmış Jetty web sunucusudur.

---

## Adım 2: Eepsite sunucunuzun ayarlarını yapılandırın

Sunucu yapılandırma sayfasını açmak için Gizli Servisler listesindeki **I2P webserver** öğesine tıklayın. Burada eepsite ayarlarınızı özelleştirebilirsiniz.

![Eepsite Sunucu Ayarları](/images/guides/eepsite/webserver-settings.png)

### Yapılandırma Seçeneklerinin Açıklaması

**Name** - Bu, tunnel'iniz için dahili bir tanımlayıcıdır - Birden fazla eepsites çalıştırıyorsanız hangisinin hangisi olduğunu takip etmek için kullanışlıdır - Varsayılan: "I2P webserver"

**Açıklama** - Kendi referansınız için eepsite'inizin kısa bir açıklaması - Yalnızca Hidden Services Manager (Gizli Servisler Yöneticisi) içinde size görünür - Örnek: "My eepsite" veya "Kişisel blog"

**Auto Start Tunnel** - **Önemli**: I2P router'ınız başladığında eepsite'ınızı otomatik olarak başlatmak için bu kutuyu işaretleyin - router yeniden başlatmalarından sonra sitenizin manuel müdahale olmadan erişilebilir kalmasını sağlar - Önerilen: **Etkin**

**Hedef (Ana makine ve bağlantı noktası)** - **Ana makine**: Web sunucunuzun çalıştığı yerel adres (varsayılan: `127.0.0.1`) - **Bağlantı noktası**: Web sunucunuzun dinlediği bağlantı noktası (Jetty için varsayılan: `7658`) - Önceden kurulu Jetty web sunucusunu kullanıyorsanız, **bunları varsayılan değerlerde bırakın** - Yalnızca farklı bir bağlantı noktasında özel bir web sunucusu çalıştırıyorsanız değiştirin

**Web Sitesi Ana Makine Adı** - Bu, eepsite'inizin insan tarafından okunabilir `.i2p` alan adıdır - Varsayılan: `mysite.i2p` (yer tutucu) - `stormycloud.i2p` veya `myblog.i2p` gibi özel bir alan adı kaydedebilirsiniz - Yalnızca otomatik olarak oluşturulan `.b32.i2p` adresini kullanmak istiyorsanız boş bırakın (outproxies (I2P dışa çıkış proxy'leri) için) - Özel bir ana makine adını nasıl talep edeceğinizi öğrenmek için aşağıdaki [I2P Alan Adınızı Kaydetme](#registering-your-i2p-domain) bölümüne bakın

**Yerel Hedef** - Bu, eepsite'inizin benzersiz kriptografik tanımlayıcısıdır (hedef adresi) - tunnel ilk oluşturulduğunda otomatik olarak üretilir - Bunu I2P üzerindeki sitenizin kalıcı "IP adresi" olarak düşünebilirsiniz - Uzun alfasayısal dizi, sitenizin kodlanmış biçimdeki `.b32.i2p` adresidir

**Özel Anahtar Dosyası** - eepsite'inizin özel anahtarlarının saklandığı konum - Varsayılan: `eepsite/eepPriv.dat` - **Bu dosyayı güvenli tutun** - Bu dosyaya erişimi olan herkes eepsite'inizin kimliğine bürünebilir - Bu dosyayı asla paylaşmayın veya silmeyin

### Önemli Not

Sarı uyarı kutusu, QR kodu oluşturma veya kayıt kimlik doğrulama özelliklerini etkinleştirmek için, `.i2p` sonekine sahip bir web sitesi ana bilgisayar adı yapılandırmanız gerektiğini hatırlatır (örneğin, `mynewsite.i2p`).

---

## Adım 3: Gelişmiş Ağ Seçenekleri (İsteğe bağlı)

Yapılandırma sayfasında aşağı kaydırırsanız, gelişmiş ağ seçeneklerini bulabilirsiniz. **Bu ayarlar isteğe bağlıdır** - varsayılanlar çoğu kullanıcı için gayet iyi çalışır. Ancak, güvenlik gereksinimlerinize ve performans ihtiyaçlarınıza göre bunları ayarlayabilirsiniz.

### Tunnel Uzunluk Seçenekleri

![Tunnel Uzunluğu ve Sayı Seçenekleri](/images/guides/eepsite/tunnel-options.png)

**Tunnel Length** - **Varsayılan**: 3 atlamalı tunnel (yüksek anonimlik) - İsteğin eepsite'inize ulaşmadan önce kaç adet router atlamasından geçtiğini kontrol eder - **Daha fazla atlama = Daha yüksek anonimlik, ancak daha yavaş performans** - **Daha az atlama = Daha hızlı performans, ancak daha düşük anonimlik** - Seçenekler, varyans ayarlarıyla 0-3 atlama arasında değişir - **Öneri**: Belirli performans gereksinimleriniz yoksa 3 atlamada tutun

**Tunnel Varyansı** - **Varsayılan**: 0 hop varyansı (rastgeleleştirme yok, tutarlı performans) - Ek güvenlik için tunnel uzunluğuna rastgeleleştirme ekler - Örnek: "0-1 hop varyansı" tunnel'ların rastgele olarak 3 veya 4 hop olacağı anlamına gelir - Öngörülemezliği artırır ancak tutarsız yükleme sürelerine yol açabilir

### Tunnel Miktar Seçenekleri

**Sayı (Gelen/Giden Tunnels)** - **Varsayılan**: 2 gelen, 2 giden tunnels (standart bant genişliği ve güvenilirlik) - eepsite'inize ayrılan paralel tunnels sayısını belirler - **Daha fazla tunnels = Daha iyi kullanılabilirlik ve yük yönetimi, ancak daha yüksek kaynak kullanımı** - **Daha az tunnels = Daha düşük kaynak kullanımı, ancak daha düşük yedeklilik** - Çoğu kullanıcı için önerilen: 2/2 (varsayılan) - Yüksek trafikli siteler 3/3 veya daha üzeri değerlerden fayda görebilir

**Yedek Sayısı** - **Varsayılan**: 0 yedek tunnels (yedeklilik yok, ek kaynak kullanımı yok) - Birincil tunnels başarısız olursa etkinleşen bekleme durumundaki tunnels - Güvenilirliği artırır ancak daha fazla bant genişliği ve CPU tüketir - Çoğu kişisel eepsite yedek tunnels gerektirmez

### POST Sınırları

![POST Limitleri Yapılandırması](/images/guides/eepsite/post-limits.png)

eepsite'iniz (I2P ağı içindeki web sitesi) formlar (iletişim formları, yorum bölümleri, dosya yüklemeleri vb.) içeriyorsa, kötüye kullanımı önlemek için POST isteği limitlerini yapılandırabilirsiniz:

**İstemci Başına Sınırlar** - **Dönem Başına**: Tek bir istemciden gelen azami istek sayısı (varsayılan: 5 dakikada 6) - **Engelleme Süresi**: Kötüye kullanım yapan istemcilerin ne kadar süreyle engelleneceği (varsayılan: 20 dakika)

**Toplam Limitler** - **Toplam**: Tüm istemcilerden toplam en fazla POST isteği sayısı (varsayılan: 5 dakikada 20) - **Engelleme Süresi**: Limit aşıldığında tüm POST isteklerinin reddedileceği süre (varsayılan: 10 dakika)

**POST Limit Süresi** - İstek hızlarını ölçmek için zaman penceresi (varsayılan: 5 dakika)

Bu kısıtlamalar, spam'a, hizmet reddi saldırılarına ve otomatik form gönderiminin kötüye kullanılmasına karşı korumaya yardımcı olur.

### Gelişmiş Ayarlar Ne Zaman Düzenlenmeli

- **Yüksek trafikli topluluk sitesi**: tunnel sayısını artırın (3-4 gelen/giden)
- **Performans-kritik uygulama**: tunnel uzunluğunu 2 atlamaya düşürün (gizlilikten ödün)
- **Maksimum anonimlik gerekli**: 3 atlamayı koruyun, 0-1 varyans ekleyin
- **Meşru olarak yüksek kullanıma sahip formlar**: POST limitlerini buna göre artırın
- **Kişisel blog/portföy**: Tüm varsayılanları kullanın

---

## Adım 4: Eepsite'inize İçerik Ekleme

Artık eepsite'iniz yapılandırıldığına göre, web sunucusunun belge kök dizinine web sitenizin dosyalarını (HTML, CSS, görseller vb.) eklemeniz gerekir. Konum, işletim sisteminize, kurulum türünüze ve I2P uygulamasına bağlı olarak değişir.

### Belge kök dizininizi bulma

**belge kök dizini** (çoğunlukla `docroot` olarak adlandırılır), tüm web sitesi dosyalarınızı koyduğunuz klasördür. `index.html` dosyanız doğrudan bu klasöre yerleştirilmelidir.

#### Java I2P (Standart Dağıtım)

**Linux** - **Standart kurulum**: `~/.i2p/eepsite/docroot/` - **Paket kurulumu (servis olarak çalışıyor)**: `/var/lib/i2p/i2p-config/eepsite/docroot/`

**Windows** - **Standart kurulum**: `%LOCALAPPDATA%\I2P\eepsite\docroot\`   - Örnek yol: `C:\Users\YourUsername\AppData\Local\I2P\eepsite\docroot\` - **Windows Hizmeti kurulumu**: `%PROGRAMDATA%\I2P\eepsite\docroot\`   - Örnek yol: `C:\ProgramData\I2P\eepsite\docroot\`

**macOS** - **Standart kurulum**: `/Users/YourUsername/Library/Application Support/i2p/eepsite/docroot/`

#### I2P+ (Geliştirilmiş I2P Dağıtımı)

I2P+, Java I2P ile aynı dizin yapısını kullanır. İşletim sisteminize göre yukarıdaki yolları izleyin.

#### i2pd (C++ Uygulaması)

**Linux/Unix** - **Varsayılan**: `/var/lib/i2pd/eepsite/` veya `~/.i2pd/eepsite/` - HTTP sunucusu tunnel'ınız altındaki geçerli `root` ayarı için `i2pd.conf` yapılandırma dosyanızı kontrol edin

**Windows** - i2pd kurulum dizininizdeki `i2pd.conf` dosyasını kontrol edin

**macOS** - Genellikle: `~/Library/Application Support/i2pd/eepsite/`

### Web Sitenizin Dosyalarını Ekleme

1. **Belge kök dizininize gidin** dosya yöneticinizi veya terminalinizi kullanarak
2. **Web sitesi dosyalarınızı oluşturun veya kopyalayın** `docroot` klasörüne
   - En azından bir `index.html` dosyası oluşturun (bu ana sayfanızdır)
   - Gerektikçe CSS, JavaScript, görseller ve diğer varlıkları ekleyin
3. **Alt dizinleri düzenleyin** herhangi bir web sitesinde yapacağınız gibi:
   ```
   docroot/
   ├── index.html
   ├── about.html
   ├── css/
   │   └── style.css
   ├── images/
   │   └── logo.png
   └── js/
       └── script.js
   ```

### Hızlı Başlangıç: Basit HTML Örneği

Yeni başlıyorsanız, `docroot` klasörünüzde temel bir `index.html` dosyası oluşturun:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My I2P Eepsite</title>
</head>
<body>
    <h1>Welcome to My Eepsite!</h1>
    <p>This is my first website on the I2P network.</p>
    <p>Privacy-focused and decentralized!</p>
</body>
</html>
```
### İzinler (Linux/Unix/macOS)

I2P'yi bir servis olarak ya da farklı bir kullanıcı olarak çalıştırıyorsanız, I2P işleminin dosyalarınızı okuma izni olduğundan emin olun:

```bash
# Set appropriate ownership (if running as i2p user)
sudo chown -R i2p:i2p /var/lib/i2p/i2p-config/eepsite/docroot/

# Or set readable permissions for all users
chmod -R 755 ~/.i2p/eepsite/docroot/
```
### İpuçları

- **Varsayılan içerik**: I2P'yi ilk kez kurduğunuzda, `docroot` klasöründe zaten örnek içerik bulunur - dilediğiniz gibi değiştirebilirsiniz
- **Statik siteler en iyi çalışır**: Jetty servlet'leri ve JSP'yi desteklese de, basit HTML/CSS/JavaScript sitelerinin bakımı en kolaydır
- **Harici web sunucuları**: İleri düzey kullanıcılar, farklı portlarda özel web sunucuları (Apache, Nginx, Node.js, vb.) çalıştırıp I2P tunnel'ını (tünel) onlara yönlendirebilir

---

## Adım 5: Eepsite'inizi Başlatma

Artık eepsite’iniz (I2P üzerinde barındırılan web sitesi) yapılandırıldı ve içeriği hazır; onu başlatıp I2P ağında erişilebilir hale getirmenin zamanı geldi.

### Tunnel'i Başlat

1. **[Gizli Servisler Yöneticisi](http://127.0.0.1:7657/i2ptunnelmgr)** sayfasına geri dönün
2. Listede **I2P web sunucusu** girdinizi bulun
3. Control sütunundaki **Start** düğmesine tıklayın

![Eepsite Çalıştırma](/images/guides/eepsite/eepsite-running.png)

### Tunnel kurulana kadar bekleyin

Start'a tıkladıktan sonra, eepsite tunnel'iniz oluşturulmaya başlayacaktır. Bu işlem genellikle **30-60 saniye** sürer. Durum göstergesini izleyin:

- **Kırmızı ışık** = Tunnel başlatılıyor/kuruluyor
- **Sarı ışık** = Tunnel kısmen kurulmuş
- **Yeşil ışık** = Tunnel tam olarak çalışır durumda ve hazır

Bir kez **yeşil ışığı** gördüğünüzde, eepsite'iniz I2P ağında yayında!

### Eepsite'inize Erişin

Çalışan eepsite'inizin yanındaki **Preview** düğmesine tıklayın. Bu, eepsite'inizin adresini içeren yeni bir tarayıcı sekmesi açar.

Eepsite'inizin iki tür adresi vardır:

1. **Base32 adresi (.b32.i2p)**: Şuna benzeyen uzun bir kriptografik adres:
   ```
   http://fcyianvr325tdgiiueyg4rsq4r5iuibzovl26msox5ryoselykpq.b32.i2p
   ```
   - Bu, eepsite'inizin kalıcı, kriptografik olarak türetilmiş adresidir
   - Değiştirilemez ve özel anahtarınıza bağlıdır
   - Alan adı kaydı olmadan bile her zaman çalışır

2. **İnsan tarafından okunabilir alan adı (.i2p)**: Bir Web sitesi ana bilgisayar adı ayarlarsanız (örn. `testwebsite.i2p`)
   - Yalnızca alan adı kaydından sonra çalışır (bkz. bir sonraki bölüm)
   - Hatırlaması ve paylaşması daha kolay
   - .b32.i2p adresinize eşlenir

**Copy Hostname** düğmesi, paylaşım için tam `.b32.i2p` adresinizi hızlıca kopyalamanıza olanak tanır.

---

## ⚠️ Kritik: Özel Anahtarınızı Yedekleyin

Devam etmeden önce, eepsite için özel anahtar dosyanızı **yedeklemek zorundasınız**. Bu, birkaç nedenle kritik derecede önemlidir:

### Anahtarınızı Neden Yedeklemelisiniz?

**Özel anahtarınız (`eepPriv.dat`) eepsite'inizin kimliğidir.** Bu, `.b32.i2p` adresinizi belirler ve eepsite'inizin sahipliğini kanıtlar.

- **Anahtar = .b32 adresi**: Özel anahtarınız, benzersiz .b32.i2p adresinizi matematiksel olarak üretir
- **Kurtarılamaz**: Anahtarınızı kaybederseniz, eepsite adresinizi kalıcı olarak kaybedersiniz
- **Değiştirilemez**: Bir .b32 adresine yönlendiren bir alan adını kaydettiyseniz, **bunu güncellemenin bir yolu yoktur** - kayıt kalıcıdır
- **Taşıma için gereklidir**: Yeni bir bilgisayara geçmek veya I2P'yi yeniden kurmak, aynı adresi korumak için bu anahtarı gerektirir
- **Multihoming (çoklu barındırma) desteği**: eepsite'inizi birden fazla konumdan çalıştırmak, her sunucuda aynı anahtarı gerektirir

### Özel anahtar nerede?

Varsayılan olarak, özel anahtarınız şu konumda saklanır: - **Linux**: `~/.i2p/eepsite/eepPriv.dat` (veya hizmet kurulumları için `/var/lib/i2p/i2p-config/eepsite/eepPriv.dat`) - **Windows**: `%LOCALAPPDATA%\I2P\eepsite\eepPriv.dat` veya `%PROGRAMDATA%\I2P\eepsite\eepPriv.dat` - **macOS**: `/Users/YourUsername/Library/Application Support/i2p/eepsite/eepPriv.dat`

Bu yolu ayrıca tunnel yapılandırmanızda "Private Key File" altında kontrol edip/değiştirebilirsiniz.

### Yedekleme Nasıl Yapılır

1. **tunnel'inizi durdurun** (isteğe bağlı, ancak daha güvenli)
2. **`eepPriv.dat`'i kopyalayın** güvenli bir konuma:
   - Harici USB sürücü
   - Şifrelenmiş yedekleme sürücüsü
   - Parola korumalı arşiv
   - Güvenli bulut depolama (şifrelenmiş)
3. **Birden fazla yedek saklayın** farklı fiziksel konumlarda
4. **Bu dosyayı asla paylaşmayın** - buna sahip olan herkes eepsite'inizin kimliğine bürünebilir

### Yedekten Geri Yükle

Yeni bir sistemde veya yeniden yükledikten sonra eepsite'inizi geri yüklemek için:

1. I2P'yi yükleyin ve tunnel ayarlarınızı oluşturun/yapılandırın
2. Anahtarı kopyalamadan önce **tunnel'ı durdurun**
3. Yedeklediğiniz `eepPriv.dat` dosyasını doğru konuma kopyalayın
4. Tunnel'ı başlatın - orijinal .b32 adresinizi kullanacaktır

---

## Bir alan adı kaydetmiyorsanız

**Tebrikler!** Özel bir `.i2p` alan adı kayıt ettirmeyi planlamıyorsanız, eepsite'iniz artık tamamlandı ve çalışır durumda.

Şunları yapabilirsiniz: - `.b32.i2p` adresinizi başkalarıyla paylaşın - Herhangi bir I2P destekli tarayıcıyla I2P ağı üzerinden sitenize erişin - Web sitenizin dosyalarını istediğiniz zaman `docroot` klasöründe güncelleyin - Hidden Services Manager'da tunnel durumunu izleyin

**İnsan tarafından okunabilir bir alan adı istiyorsanız** (uzun bir .b32 adresi yerine `mysite.i2p` gibi), bir sonraki bölüme devam edin.

---

## I2P Alan Adınızı Kaydetme

İnsanların okuyup anlayabileceği bir `.i2p` alan adı (örneğin `testwebsite.i2p`), uzun bir `.b32.i2p` adresine kıyasla hatırlaması ve paylaşması çok daha kolaydır. Alan adı kaydı ücretsizdir ve seçtiğiniz adı eepsite’inizin (I2P içindeki web sitenizin) kriptografik adresine bağlar.

### Önkoşullar

- eepsite'iniz yeşil ışık göstermeli
- tunnel yapılandırmanızda (Adım 2) bir **Website Hostname** ayarlamış olmalısınız
- Örnek: `testwebsite.i2p` veya `myblog.i2p`

### Adım 1: Kimlik doğrulama dizesi oluşturun

1. **tunnel yapılandırmanıza geri dönün** Gizli Hizmetler Yöneticisi'nde
2. Ayarları açmak için **I2P webserver** girişinize tıklayın
3. **Kayıt Kimlik Doğrulaması** düğmesini bulmak için aşağı kaydırın

![Kayıt Kimlik Doğrulaması](/images/guides/eepsite/registration-authentication.png)

4. **Registration Authentication**'a tıklayın
5. **Kimlik doğrulama dizesinin tamamını kopyalayın** "Ana bilgisayar [yourdomainhere] eklemek için kimlik doğrulaması" için gösterilen

Kimlik doğrulama dizesi şu şekilde görünecektir:

```
testwebsite.i2p=I8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1uNxFZ0HN7tQbbVj1pmbahepQZNxEW0ufwnMYAoFo8opBQAEAAcAAA==#!date=1762104890#sig=9DjEfrcNRxsoSxiE0Mp0-7rH~ktYWtgwU8c4J0eSo0VHbGxDxdiO9D1Cvwcx8hkherMO07UWOC9BWf-1wRyUAw==
```
Bu dize şunları içerir: - Alan adınız (`testwebsite.i2p`) - Hedef adresiniz (uzun kriptografik tanımlayıcı) - Bir zaman damgası - Özel anahtara sahip olduğunuzu kanıtlayan bir kriptografik imza

**Bu kimlik doğrulama dizesini saklayın** - her iki kayıt hizmeti için de buna ihtiyacınız olacak.

### Adım 2: stats.i2p'ye kaydolun

1. **Şuraya gidin** [stats.i2p Anahtar Ekle](http://stats.i2p/i2p/addkey.html) (I2P içinde)

![stats.i2p Alan Adı Kaydı](/images/guides/eepsite/stats-i2p-add.png)

2. **Kimlik doğrulama dizgesini** "Authentication String" alanına yapıştırın
3. **Adınızı ekleyin** (isteğe bağlı) - varsayılan olarak "Anonymous"
4. **Bir açıklama ekleyin** (önerilir) - eepsite'inizin (I2P üzerinde barındırılan web sitesi) ne hakkında olduğunu kısaca açıklayın
   - Örnek: "Yeni I2P Eepsite", "Kişisel blog", "Dosya paylaşım hizmeti"
5. **"HTTP Service?" seçeneğini işaretleyin** bu bir web sitesi ise (çoğu eepsite için işaretli bırakın)
   - IRC, NNTP, proxy'ler, XMPP, git, vb. için işaretini kaldırın
6. **Submit**'e tıklayın

İşlem başarılı olursa, alan adınızın stats.i2p adres defterine eklendiğine dair bir onay göreceksiniz.

### Adım 3: reg.i2p'e kaydolun

Maksimum kullanılabilirliği sağlamak için, reg.i2p hizmetine de kaydolmalısınız:

1. **Şuraya gidin** [reg.i2p Add Domain](http://reg.i2p/add) (I2P içinde)

![reg.i2p Alan Adı Kaydı](/images/guides/eepsite/reg-i2p-add.png)

2. **Aynı kimlik doğrulama metnini yapıştırın** "Auth string" alanına
3. **Bir açıklama ekleyin** (isteğe bağlı ancak önerilir)
   - Bu, diğer I2P kullanıcılarının sitenizin ne sunduğunu anlamasına yardımcı olur
4. **Submit**'e tıklayın

Alan adınızın kaydedildiğine dair bir onay almalısınız.

### Adım 4: Yayılmayı Bekleyin

Her iki hizmete de gönderdikten sonra, alan adı kaydınız I2P ağının adres defteri sistemi aracılığıyla yayılacaktır.

**Yayılma zaman çizelgesi**: - **İlk kayıt**: Kayıt hizmetlerinde anında - **Ağ genelinde yayılma**: Birkaç saat ile 24+ saat arası - **Tam kullanılabilirlik**: Tüm routers güncellenene kadar 48 saate kadar sürebilir

**Bu normal!** I2P adres defteri sistemi anında değil, belirli aralıklarla güncellenir. eepsite'iniz çalışıyor - diğer kullanıcıların yalnızca güncellenmiş adres defterini almaları gerekiyor.

### Alan adınızı doğrulayın

Birkaç saat sonra alan adınızı test edebilirsiniz:

1. **Yeni bir tarayıcı sekmesi açın** I2P tarayıcınızda
2. Alan adınıza doğrudan erişmeyi deneyin: `http://yourdomainname.i2p`
3. Yüklenirse, alan adınız kayıtlı ve yayılıyor!

Eğer hâlâ çalışmıyorsa: - Daha uzun süre bekleyin (adres defterleri kendi zamanlamalarına göre güncellenir) - Router'ınızın adres defterinin eşitlenmesi için zamana ihtiyaç duyabilir - Bir adres defteri güncellemesini zorlamak için I2P router'ınızı yeniden başlatmayı deneyin

### Önemli Notlar

- **Kayıt kalıcıdır**: Kayıt tamamlanıp ağa yayıldıktan sonra alan adınız kalıcı olarak `.b32.i2p` adresinizi işaret eder
- **Hedef değiştirilemez**: Alan adınızın işaret ettiği `.b32.i2p` adresini güncelleyemezsiniz - bu yüzden `eepPriv.dat` dosyasının yedeğini almak kritik önemdedir
- **Alan adı sahipliği**: Yalnızca özel anahtarın sahibi alan adı kaydını yapabilir veya güncelleyebilir
- **Ücretsiz hizmet**: I2P üzerindeki alan adı kaydı ücretsizdir, topluluk tarafından işletilir ve merkeziyetsizdir
- **Birden fazla kayıt kuruluşu**: Hem stats.i2p hem de reg.i2p ile kayıt olmak güvenilirliği ve yayılım hızını artırır

---

## Tebrikler!

I2P eepsite'iniz artık kayıtlı bir alan adıyla tamamen çalışır durumda!

**Sonraki adımlar**: - `docroot` klasörünüze daha fazla içerik ekleyin - Alan adınızı I2P topluluğuyla paylaşın - `eepPriv.dat` yedeğinizi güvende tutun - tunnel durumunuzu düzenli olarak izleyin - Sitenizi tanıtmak için I2P forumlarına veya IRC'ye katılmayı düşünün

I2P ağına hoş geldiniz! 🎉
