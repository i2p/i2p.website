---
title: "macOS'ta I2P Kurulumu (Uzun Yol)"
description: "macOS üzerinde I2P ve bağımlılıklarını manuel olarak kurma adım adım kılavuzu"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Neye İhtiyacınız Olacak

- macOS 10.14 (Mojave) veya sonraki sürümleri çalıştıran bir Mac
- Uygulama yüklemek için yönetici erişimi
- Yaklaşık 15-20 dakika süre
- Yükleyicileri indirmek için internet bağlantısı

## Genel Bakış

Bu kurulum süreci dört ana adımdan oluşur:

1. **Java Yükleyin** - Oracle Java Runtime Environment'ı indirin ve kurun
2. **I2P Yükleyin** - I2P yükleyicisini indirin ve çalıştırın
3. **I2P Uygulamasını Yapılandırın** - Başlatıcıyı ayarlayın ve dock'unuza ekleyin
4. **I2P Bant Genişliğini Yapılandırın** - Bağlantınızı optimize etmek için kurulum sihirbazını çalıştırın

## Birinci Bölüm: Java Kurulumu

I2P'nin çalışması için Java gereklidir. Eğer Java 8 veya daha yeni bir sürümü zaten yüklüyseniz, [İkinci Bölüme atlayabilirsiniz](#part-two-download-and-install-i2p).

### Step 1: Download Java

[Oracle Java indirme sayfasını](https://www.oracle.com/java/technologies/downloads/) ziyaret edin ve Java 8 veya sonrası için macOS yükleyicisini indirin.

![macOS için Oracle Java'yı İndirin](/images/guides/macos-install/0-jre.png)

### Step 2: Run the Installer

İndirilen `.dmg` dosyasını İndirilenler klasörünüzde bulun ve açmak için çift tıklayın.

![Java yükleyiciyi açın](/images/guides/macos-install/1-jre.png)

### Step 3: Allow Installation

macOS, yükleyici tanımlanmış bir geliştiriciden olduğu için bir güvenlik uyarısı gösterebilir. Devam etmek için **Aç** düğmesine tıklayın.

![Yükleyiciye devam etmesi için izin verin](/images/guides/macos-install/2-jre.png)

### Adım 1: Java'yı İndirin

Java kurulum işlemini başlatmak için **Yükle** düğmesine tıklayın.

![Java'yı yüklemeye başla](/images/guides/macos-install/3-jre.png)

### Adım 2: Yükleyiciyi Çalıştırın

Yükleyici dosyaları kopyalayacak ve sisteminizde Java'yı yapılandıracaktır. Bu genellikle 1-2 dakika sürer.

![Yükleyicinin tamamlanmasını bekleyin](/images/guides/macos-install/4-jre.png)

### Adım 3: Kuruluma İzin Verin

Başarı mesajını gördüğünüzde, Java kurulmuş demektir! Bitirmek için **Kapat**'a tıklayın.

![Java kurulumu tamamlandı](/images/guides/macos-install/5-jre.png)

## Part Two: Download and Install I2P

Java kurulduktan sonra, I2P router'ını kurabilirsiniz.

### Adım 4: Java'yı Kurun

[İndirmeler sayfasını](/downloads/) ziyaret edin ve **Unix/Linux/BSD/Solaris için I2P** yükleyicisini (`.jar` dosyası) indirin.

![I2P yükleyicisini indir](/images/guides/macos-install/0-i2p.png)

### Adım 5: Kurulumun Tamamlanmasını Bekleyin

İndirilen `i2pinstall_X.X.X.jar` dosyasına çift tıklayın. Yükleyici başlatılacak ve tercih ettiğiniz dili seçmenizi isteyecektir.

![Dilinizi seçin](/images/guides/macos-install/1-i2p.png)

### Adım 6: Kurulum Tamamlandı

Hoş geldiniz mesajını okuyun ve devam etmek için **İleri**'ye tıklayın.

![Yükleyici tanıtımı](/images/guides/macos-install/2-i2p.png)

### Step 4: Important Notice

Yükleyici, güncellemeler hakkında önemli bir bildirim gösterecektir. I2P güncellemeleri, bu yükleyicinin kendisi imzasız olsa bile **uçtan uca imzalanır** ve doğrulanır. **İleri**'ye tıklayın.

![Güncellemeler hakkında önemli uyarı](/images/guides/macos-install/3-i2p.png)

### Adım 1: I2P'yi İndirin

I2P lisans sözleşmesini okuyun (BSD tarzı lisans). Kabul etmek için **İleri**'ye tıklayın.

![Lisans sözleşmesi](/images/guides/macos-install/4-i2p.png)

### Adım 2: Yükleyiciyi Çalıştırın

I2P'nin nereye kurulacağını seçin. Varsayılan konum (`/Applications/i2p`) önerilir. **İleri**'ye tıklayın.

![Kurulum dizinini seçin](/images/guides/macos-install/5-i2p.png)

### Adım 3: Hoş Geldiniz Ekranı

Eksiksiz bir kurulum için tüm bileşenlerin seçili bırakılması. **İleri**'ye tıklayın.

![Yüklenecek bileşenleri seçin](/images/guides/macos-install/6-i2p.png)

### Adım 4: Önemli Uyarı

Seçimlerinizi gözden geçirin ve I2P'yi kurmaya başlamak için **İleri**'ye tıklayın.

![Kurulumu başlat](/images/guides/macos-install/7-i2p.png)

### Adım 5: Lisans Sözleşmesi

Yükleyici I2P dosyalarını sisteminize kopyalayacaktır. Bu işlem yaklaşık 1-2 dakika sürer.

![Kurulum devam ediyor](/images/guides/macos-install/8-i2p.png)

### Adım 6: Kurulum Dizinini Seçin

Yükleyici, I2P'yi başlatmak için başlatma betikleri oluşturur.

![Başlatma betikleri oluşturuluyor](/images/guides/macos-install/9-i2p.png)

### Adım 7: Bileşenleri Seçin

Yükleyici masaüstü kısayolları ve menü girişleri oluşturmayı önerir. Seçimlerinizi yapın ve **İleri**'ye tıklayın.

![Kısayollar oluştur](/images/guides/macos-install/10-i2p.png)

### Adım 8: Kurulumu Başlat

Başarılı! I2P artık yüklendi. Bitirmek için **Bitti**'ye tıklayın.

![Kurulum tamamlandı](/images/guides/macos-install/11-i2p.png)

## Part Three: Configure I2P App

Şimdi I2P'yi Uygulamalar klasörünüze ve Dock'unuza ekleyerek başlatmayı kolaylaştıralım.

### Adım 9: Dosyaların Kurulumu

Finder'ı açın ve **Uygulamalar** klasörünüze gidin.

![Applications klasörünü açın](/images/guides/macos-install/0-conf.png)

### Adım 10: Başlatma Betiklerini Oluştur

`/Applications/i2p/` klasörü içinde **I2P** klasörünü veya **Start I2P Router** uygulamasını arayın.

![I2P başlatıcısını bulun](/images/guides/macos-install/1-conf.png)

### Adım 11: Kurulum Kısayolları

**Start I2P Router** uygulamasını kolay erişim için Dock'unuza sürükleyin. Masaüstünüzde bir takma ad da oluşturabilirsiniz.

![I2P'yi Dock'unuza Ekleyin](/images/guides/macos-install/2-conf.png)

**İpucu**: Dock'taki I2P simgesine sağ tıklayın ve kalıcı hale getirmek için **Seçenekler → Dock'ta Tut** seçeneğini seçin.

## Part Four: Configure I2P Bandwidth

I2P'yi ilk kez başlattığınızda, bant genişliği ayarlarınızı yapılandırmak için bir kurulum sihirbazından geçeceksiniz. Bu, I2P'nin performansını bağlantınıza göre optimize etmeye yardımcı olur.

### Adım 12: Kurulum Tamamlandı

Dock'ınızdaki I2P simgesine tıklayın (veya başlatıcıya çift tıklayın). Varsayılan web tarayıcınız I2P Router Console'a açılacaktır.

![I2P Router Console karşılama ekranı](/images/guides/macos-install/0-wiz.png)

### Step 2: Welcome Wizard

Kurulum sihirbazı sizi karşılayacaktır. I2P'yi yapılandırmaya başlamak için **İleri**'ye tıklayın.

![Kurulum sihirbazı tanıtımı](/images/guides/macos-install/1-wiz.png)

### Adım 1: Uygulamalar Klasörünü Açın

Tercih ettiğiniz **arayüz dilini** seçin ve **açık** veya **koyu** tema arasında tercih yapın. **İleri**'ye tıklayın.

![Dil ve tema seçimi](/images/guides/macos-install/2-wiz.png)

### Adım 2: I2P Başlatıcısını Bulun

Sihirbaz bant genişliği testini açıklayacaktır. Bu test, internet hızınızı ölçmek için **M-Lab** servisine bağlanır. Devam etmek için **İleri**'ye tıklayın.

![Bant genişliği testi açıklaması](/images/guides/macos-install/3-wiz.png)

### Adım 3: Dock'a Ekle

Yükleme ve indirme hızlarınızı ölçmek için **Testi Çalıştır**'a tıklayın. Test yaklaşık 30-60 saniye sürer.

![Bant genişliği testini çalıştırma](/images/guides/macos-install/4-wiz.png)

### Step 6: Test Results

Test sonuçlarınızı gözden geçirin. I2P, bağlantı hızınıza göre bant genişliği ayarları önerecektir.

![Bant genişliği test sonuçları](/images/guides/macos-install/5-wiz.png)

### Adım 1: I2P'yi Başlatın

I2P ağı ile ne kadar bant genişliği paylaşmak istediğinizi seçin:

- **Otomatik** (Önerilen): I2P bant genişliğini kullanımınıza göre yönetir
- **Sınırlı**: Belirli yükleme/indirme limitleri ayarlayın
- **Sınırsız**: Mümkün olduğunca çok paylaşın (hızlı bağlantılar için)

Ayarlarınızı kaydetmek için **İleri**'ye tıklayın.

![Bant genişliği paylaşımını yapılandır](/images/guides/macos-install/6-wiz.png)

### Adım 2: Hoş Geldiniz Sihirbazı

I2P router'ınız artık yapılandırılmış ve çalışıyor! Router konsolu bağlantı durumunuzu gösterecek ve I2P sitelerine göz atmanızı sağlayacak.

## Getting Started with I2P

I2P kurulup yapılandırıldığına göre, artık şunları yapabilirsiniz:

1. **I2P sitelerini gezin**: Popüler I2P hizmetlerine bağlantıları görmek için [I2P ana sayfasını](http://127.0.0.1:7657/home) ziyaret edin
2. **Tarayıcınızı yapılandırın**: `.i2p` sitelerine erişmek için bir [tarayıcı profili](/docs/guides/browser-config) oluşturun
3. **Hizmetleri keşfedin**: I2P e-posta, forum, dosya paylaşımı ve daha fazlasını inceleyin
4. **Router'ınızı izleyin**: [Konsol](http://127.0.0.1:7657/console) ağ durumunuzu ve istatistiklerinizi gösterir

### Adım 3: Dil ve Tema

- **Router Console**: [http://127.0.0.1:7657/](http://127.0.0.1:7657/)
- **Yapılandırma**: [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)
- **Adres Defteri**: [http://127.0.0.1:7657/susidns/addressbook](http://127.0.0.1:7657/susidns/addressbook)
- **Bant Genişliği Ayarları**: [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)

## Re-running the Setup Wizard

Bant genişliği ayarlarınızı değiştirmek veya I2P'yi daha sonra yeniden yapılandırmak isterseniz, hoş geldin sihirbazını Router Console'dan tekrar çalıştırabilirsiniz:

1. [I2P Kurulum Sihirbazı](http://127.0.0.1:7657/welcome)'na gidin
2. Sihirbaz adımlarını tekrar takip edin

## Troubleshooting

### Adım 4: Bant Genişliği Testi Bilgileri

- **Java'yı kontrol edin**: Terminal'de `java -version` komutunu çalıştırarak Java'nın kurulu olduğundan emin olun
- **İzinleri kontrol edin**: I2P klasörünün doğru izinlere sahip olduğundan emin olun
- **Logları kontrol edin**: Hata mesajları için `~/.i2p/wrapper.log` dosyasına bakın

### Adım 5: Bant Genişliği Testi Çalıştırın

- I2P'nin çalıştığından emin olun (Yönlendirici Konsolu'nu kontrol edin)
- Tarayıcınızın proxy ayarlarını HTTP proxy `127.0.0.1:4444` kullanacak şekilde yapılandırın
- Başlattıktan sonra I2P'nin ağa entegre olması için 5-10 dakika bekleyin

### Adım 6: Test Sonuçları

- Bant genişliği testini tekrar çalıştırın ve ayarlarınızı düzenleyin
- Ağ ile bant genişliği paylaştığınızdan emin olun
- Router Console'da bağlantı durumunuzu kontrol edin

## İkinci Bölüm: I2P'yi İndirin ve Kurun

Mac bilgisayarınızdan I2P'yi kaldırmak için:

1. I2P router çalışıyorsa kapatın
2. `/Applications/i2p` klasörünü silin
3. `~/.i2p` klasörünü silin (I2P yapılandırma ve verileriniz)
4. I2P simgesini Dock'tan kaldırın

## Next Steps

- **Topluluğa katılın**: [i2pforum.net](http://i2pforum.net) adresini ziyaret edin veya Reddit'te I2P'yi inceleyin
- **Daha fazla bilgi edinin**: Ağın nasıl çalıştığını anlamak için [I2P belgelerini](/en/docs) okuyun
- **Katkıda bulunun**: I2P [geliştirmeye katkıda bulunmayı](/en/get-involved) veya altyapı çalıştırmayı düşünün

Tebrikler! Artık I2P ağının bir parçasısınız. Görünmez internete hoş geldiniz!

