---
title: "Resimlerle Temel I2P Tunnels Kılavuzu"
date: 2019-06-02
author: "idk"
description: "Temel i2ptunnel Kurulumu"
categories: ["tutorial"]
---

Java I2P router, kullanıcıya ilk eepSite (I2P içindeki web sitesi) sağlamak için önceden yapılandırılmış bir statik web sunucusu, jetty, ile gelse de, pek çok kişi web sunucusundan daha gelişmiş işlevsellik ister ve farklı bir sunucuyla bir eepSite oluşturmayı tercih eder. Bu elbette mümkündür ve aslında bir kez yaptıktan sonra gerçekten çok kolaydır.

Bunu yapmak kolay olsa da, yapmadan önce göz önünde bulundurmanız gereken birkaç şey var. Web sunucunuzdan, kimlik tespitine yol açabilecek üstbilgiler ve sunucu/dağıtım türünü bildiren varsayılan hata sayfaları gibi, kimlik belirleyici özellikleri kaldırmak isteyeceksiniz. Yanlış yapılandırılmış uygulamaların anonimliğe yönelik tehditleri hakkında daha fazla bilgi için bkz.: [Riseup burada](https://riseup.net/en/security/network-security/tor/onionservices-best-practices), [Whonix burada](https://www.whonix.org/wiki/Onion_Services), [Bazı OPSEC hatalarına dair bu blog yazısı](https://blog.0day.rocks/securing-a-web-hidden-service-89d935ba1c1d), [ve I2P uygulamaları sayfası burada](https://geti2p.net/docs/applications/supported). Bu bilgilerin çoğu Tor Onion Services için ifade edilmiş olsa da, aynı süreçler ve ilkeler I2P üzerinden uygulama barındırma için de geçerlidir.

### Birinci Adım: Tunnel Sihirbazını Açın

127.0.0.1:7657 adresindeki I2P web arayüzüne gidin ve [Gizli Servisler Yöneticisi](http://127.0.0.1:7657/i2ptunnelmgr) (localhost'a bağlantı) sayfasını açın. Başlamak için "Tunnel Wizard" adlı düğmeye tıklayın.

### Adım İki: Sunucu Tunnel seçin

Tunnel sihirbazı çok basit. Bir http *sunucusu* kurduğumuz için, yapmamız gereken tek şey bir *sunucu* tunnel seçmektir.

### Üçüncü Adım: Bir HTTP Tunnel seçin

Bir HTTP tunnel, HTTP hizmetlerini barındırmak için optimize edilmiş tunnel türüdür. Bu amaca özel olarak uyarlanmış filtreleme ve hız sınırlama özellikleri etkin durumdadır. Bir standart tunnel da işe yarayabilir; ancak bir standart tunnel seçerseniz, bu güvenlik özelliklerini kendiniz uygulamanız gerekir. HTTP Tunnel yapılandırmasına daha derinlemesine bir bakış bir sonraki öğreticide mevcuttur.

### Dördüncü Adım: Ona bir ad ve açıklama verin

Kendi yararınıza ve hangi amaçla tunnel (tünel) kullandığınızı hatırlayıp ayırt edebilmek için ona iyi bir takma ad ve açıklama verin. Daha sonra geri dönüp ek yönetim işlemleri yapmanız gerekirse, tunnel'i Gizli Servisler Yöneticisi'nde bu şekilde ayırt edeceksiniz.

### Beşinci Adım: Ana makine ve bağlantı noktasını yapılandırın

Bu adımda, web sunucunuzun dinlediği TCP bağlantı noktasını belirtirsiniz. Çoğu web sunucusu 80 veya 8080 numaralı bağlantı noktasında dinlediği için, örnek bunu göstermektedir. Web hizmetlerinizi yalıtmak için alternatif bağlantı noktaları veya sanal makineler ya da konteynerler kullanıyorsanız, ana makineyi (host), bağlantı noktasını (port) veya her ikisini de ayarlamanız gerekebilir.

### Altıncı Adım: Otomatik olarak başlatılıp başlatılmayacağına karar verin

Bu adımı daha ayrıntılı açıklamanın bir yolunu düşünemiyorum.

### Yedinci Adım: Ayarlarınızı gözden geçirin

Son olarak, seçtiğiniz ayarlara bir göz atın. Onaylıyorsanız bunları kaydedin. Eğer tunnel'i otomatik olarak başlatmayı seçmediyseniz, Hidden Services Manager (Gizli Servisler Yöneticisi)'a gidin ve hizmetinizi erişilebilir kılmak istediğinizde onu manuel olarak başlatın.

### Ek: HTTP Sunucusu Özelleştirme Seçenekleri

I2P, http sunucu tunnel'ini özel yollarla yapılandırmaya yönelik ayrıntılı bir panel sunar. Hepsinin üzerinden adım adım geçerek bu eğitimi tamamlayacağım. Er ya da geç.
