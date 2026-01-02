---
title: "Özel Eklentilerin Kurulumu"
description: "Router eklentilerini yükleme, güncelleme ve geliştirme"
slug: "plugins"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

I2P'nin eklenti çerçevesi, çekirdek kuruluma dokunmadan router'ı genişletmenize olanak tanır. Mevcut eklentiler posta, bloglar, IRC, depolama, wiki'ler, izleme araçları ve daha fazlasını kapsar.

> **Güvenlik notu:** Eklentiler, yönlendirici ile aynı izinlerle çalışır. Üçüncü taraf indirmelerine, imzalı herhangi bir yazılım güncellemesine davrandığınız gibi davranın—kurmadan önce kaynağı doğrulayın.

## 1. Bir Eklenti Yükleyin

1. Eklentinin indirme URL'sini proje sayfasından kopyalayın.  
   ![Copy plugin URL](/images/plugins/plugin-step-0.png)
2. Router konsolunun [Eklenti Yapılandırma sayfasını](http://127.0.0.1:7657/configplugins) açın.  
   ![Open plugin configuration](/images/plugins/plugin-step-1.png)
3. URL'yi kurulum alanına yapıştırın ve **Eklentiyi Kur**'a tıklayın.  
   ![Install plugin](/images/plugins/plugin-step-2.png)

Router imzalı arşivi indirir, imzayı doğrular ve eklentiyi anında etkinleştirir. Çoğu eklenti, router'ın yeniden başlatılmasını gerektirmeden konsol bağlantıları veya arka plan hizmetleri ekler.

## 2. Eklentiler Neden Önemlidir

- Son kullanıcılar için tek tıkla dağıtım—`wrapper.config` veya `clients.config` dosyalarında manuel düzenleme gerekmez
- Temel `i2pupdate.su3` paketini küçük tutarken büyük veya niş özellikleri isteğe bağlı olarak sunar
- İsteğe bağlı eklenti başına JVM'ler gerektiğinde süreç izolasyonu sağlar
- Router sürümü, Java çalışma zamanı ve Jetty ile otomatik uyumluluk kontrolleri
- Güncelleme mekanizması router'ı yansıtır: imzalı paketler ve artımlı indirmeler
- Konsol entegrasyonları, dil paketleri, kullanıcı arayüzü temaları ve Java olmayan uygulamalar (betikler aracılığıyla) desteklenir
- `plugins.i2p` gibi düzenlenmiş "uygulama mağazası" dizinlerini etkinleştirir

## 3. Yüklü Eklentileri Yönetme

[I2P Router Eklentisi](http://127.0.0.1:7657/configclients.jsp#plugin) üzerindeki kontrolleri kullanarak:

- Tek bir eklentiyi güncellemeler için kontrol et
- Tüm eklentileri aynı anda kontrol et (router yükseltmelerinden sonra otomatik olarak tetiklenir)
- Mevcut güncellemeleri tek tıkla yükle  
  ![Update plugins](/images/plugins/plugin-update-0.png)
- Servis kaydeden eklentiler için otomatik başlatmayı etkinleştir/devre dışı bırak
- Eklentileri temiz bir şekilde kaldır

## 4. Kendi Eklentinizi Oluşturun

1. Paketleme, imzalama ve metadata gereksinimleri için [eklenti spesifikasyonunu](/docs/specs/plugin/) inceleyin.
2. Mevcut bir binary veya webapp'i kurulabilir bir arşiv haline getirmek için [`makeplugin.sh`](https://github.com/i2p/i2p.scripts/tree/master/plugin/makeplugin.sh) kullanın.
3. Router'ın ilk kurulumları artımlı yükseltmelerden ayırt edebilmesi için hem kurulum hem de güncelleme URL'lerini yayınlayın.
4. Kullanıcıların özgünlüğü doğrulamasına yardımcı olmak için proje sayfanızda checksumları ve imzalama anahtarlarını belirgin şekilde sağlayın.

Örnek mi arıyorsunuz? `plugins.i2p` adresindeki topluluk eklentilerinin kaynak koduna göz atın (örneğin, `snowman` örneği).

## 5. Bilinen Sınırlamalar

- Düz JAR dosyaları içeren bir eklentiyi güncellemek, Java sınıf yükleyicisinin sınıfları önbelleğe aldığı için yönlendirici yeniden başlatması gerektirebilir.
- Konsol, eklentinin aktif bir süreci olmasa bile **Durdur** düğmesini görüntüleyebilir.
- Ayrı bir JVM'de başlatılan eklentiler, geçerli çalışma dizininde bir `logs/` dizini oluşturur.
- Bir imzalayan anahtarı ilk kez göründüğünde otomatik olarak güvenilir; merkezi bir imzalama otoritesi yoktur.
- Windows bazen bir eklenti kaldırıldıktan sonra boş dizinleri geride bırakır.
- Java 5 JVM üzerinde yalnızca Java 6 için olan bir eklentiyi yüklemek, Pack200 sıkıştırması nedeniyle "eklenti bozuk" bildirimi verir.
- Tema ve çeviri eklentileri büyük ölçüde test edilmemiş durumda kalır.
- Otomatik başlatma bayrakları, yönetilmeyen eklentiler için her zaman kalıcı olmaz.

## 6. Gereksinimler ve En İyi Uygulamalar

- Eklenti desteği I2P **0.7.12 ve daha yeni sürümlerde** mevcuttur.
- Güvenlik düzeltmelerini almak için router'ınızı ve eklentilerinizi güncel tutun.
- Kullanıcıların sürümler arasındaki değişiklikleri anlaması için özet sürüm notları ekleyin.
- Mümkün olduğunda, açık-ağ metadata maruziyetini en aza indirmek için eklenti arşivlerini I2P içinde HTTPS üzerinden barındırın.

## 7. İleri Okuma

- [Eklenti belirtimi](/docs/specs/plugin/)
- [İstemci uygulama çerçevesi](/docs/applications/managed-clients/)
- Paketleme araçları için [I2P betikleri deposu](https://github.com/i2p/i2p.scripts/)
