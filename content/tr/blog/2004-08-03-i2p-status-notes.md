---
title: "2004-08-03 tarihli I2P Durum Notları"
date: 2004-08-03
author: "jr"
description: "0.3.4 sürümünün performansını, yeni web konsolu geliştirmesini ve çeşitli uygulama projelerini kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

selam millet, hadi bu durum güncellemesini aradan çıkaralım

## Dizin:

1. 0.3.4 status
2. On deck for 0.3.4.1
3. New web console / I2PTunnel controller
4. 0.4 stuff
5. Other development activities
6. ???

## 1) 0.3.4 durumu

Geçen haftaki 0.3.4 sürümüyle birlikte, yeni ağ oldukça iyi performans gösteriyor - IRC bağlantıları tek seferde birkaç saat sürüyor ve eepsite(I2P Site) erişimi oldukça güvenilir görünüyor. Aktarım hızı genel olarak hâlâ düşük, ancak biraz iyileşti (eskiden tutarlı biçimde 4-5KBps görürdüm, şimdi tutarlı biçimde 5-8KBps görüyorum). oOo, IRC etkinliğini özetleyen, mesajların gidiş-dönüş süresi ve bağlantı ömrünü içeren bir çift betik yayımladı (yakın zamanda CVS'e gönderilen hypercubus'un bogobot'una dayanıyor).

## 2) 0.3.4.1 için sırada

0.3.4 kullanan herkesin fark ettiği gibi, günlükleme konusunda *öhm* biraz fazla ayrıntıya kaçmıştım, bu durum cvs'de giderildi. Buna ek olarak, ministreaming kütüphanesini stres testine sokmak için bazı araçlar yazdıktan sonra, yığınla belleği tüketmemesi için bir 'choke' (kısıtlama) ekledim (bir akışın arabelleğine 128KB'den fazla veri eklemeye çalışıldığında bloklayacak, böylece büyük bir dosya gönderirken router'ınız o dosyanın tamamını belleğe yüklemez). Bunun insanların karşılaştığı OutOfMemory sorunlarına yardımcı olacağını düşünüyorum, ancak bunu doğrulamak için bazı ek izleme / hata ayıklama kodu ekleyeceğim.

## 3) Yeni web konsolu / I2PTunnel denetleyicisi

0.3.4.1 için yukarıdaki değişikliklere ek olarak, yeni router konsolunun ilk aşamasını bazı testler için hazır hâle getirdik. Birkaç nedenden dolayı, onu henüz varsayılan kuruluma dahil etmeyeceğiz, bu yüzden birkaç gün içinde 0.3.4.1 revizyonu çıktığında nasıl çalıştırılacağına dair talimatlar olacak. Gördüğünüz gibi, web tasarımı konusunda gerçekten kötüyüm ve çoğunuzun söylediği gibi, uygulama katmanıyla oyalanmayı bırakıp çekirdek ile router'ı sapasağlam hâle getirmeliyim. Dolayısıyla, yeni konsol istediğimiz iyi işlevlerin çoğuna sahip olsa da (router'ı tamamen birkaç basit web sayfası üzerinden yapılandırmak, router'ın sağlık durumuna ilişkin hızlı ve okunabilir bir özet sunmak, farklı I2PTunnel örnekleri oluşturma / düzenleme / durdurma / başlatma olanağı sağlamak), web tarafında iyi olan kişilerden gerçekten yardıma ihtiyacım var.

Yeni web konsolunda kullanılan teknolojiler, router / I2PTunnels’a veri için sorgu gönderen ve istekleri işleyen standart JSP, CSS ve basit Java bean’lerdir. Bunların tümü bir çift .war dosyası halinde paketlenir ve entegre bir Jetty webserver’a dağıtılır (ki bunun router’ın clientApp.* satırları üzerinden başlatılması gerekir). Ana router konsolu JSP’leri ve bean’leri teknik açıdan oldukça sağlamdır; ancak I2PTunnel örneklerini yönetmek için oluşturduğum yeni JSP ve bean’ler biraz derme çatmadır.

## 4) 0.4 ile ilgili konular

Yeni web arayüzüne ek olarak, 0.4 sürümü henüz tam olarak entegre etmediğimiz hypercubus'un yeni yükleyicisini de içerecek. Ayrıca birkaç büyük ölçekli simülasyon daha yapmamız gerekiyor (özellikle IRC ve outproxies (dışa çıkış vekil sunucuları) gibi asimetrik uygulamaların ele alınması konusunda). Buna ek olarak, açık kaynak JVM'lerde yeni web altyapısını çalıştırabilmemiz için kaffe/classpath'e iletmem gereken bazı güncellemeler var. Ayrıca birkaç belge daha hazırlamam gerekiyor (biri ölçeklenebilirlik üzerine, diğeri de birkaç yaygın senaryoda güvenlik/anonimliği analiz eden). Geliştirdiğiniz tüm iyileştirmelerin yeni web konsoluna entegre edilmiş olmasını da istiyoruz.

Ayrıca, bulunmasına yardımcı olduğun tüm hataları da düzelt :)

## 5) Diğer geliştirme faaliyetleri

Temel I2P sisteminde çok fazla ilerleme kaydedilmiş olsa da, bu işin yalnızca yarısı - I2P'yi kullanışlı hale getirmek için uygulamalar ve kütüphaneler üzerinde harika çalışmalar yapan birçoğunuz var. Kimlerin ne üzerinde çalıştığına dair sohbet geçmişinde bazı sorular gördüm, bu bilgiyi ortaya çıkarmaya yardımcı olmak için de işte bu konuda bildiğim her şey (listede yer almayan bir şey üzerinde çalışıyor ve paylaşmak istiyorsanız, ben yanılıyorsam ya da ilerlemenizi tartışmak istiyorsanız, lütfen ses verin!)

### Active development:

- python SAM/I2P lib (devs: sunshine, aum)
- C SAM lib (devs: nightblade)
- python kademlia/I2P DHT (devs: aum)
- v2v - Voice over I2P (devs: aum)
- outproxy load balancing (devs: mule)

### Development I've heard about but don't know the status of:

- swarming file transfer / BT (devs: nickster)

### Paused development:

- Enclave DHT (devs: nightblade)
- perl SAM lib (devs: BrianR)
- I2PSnark / BT (devs: eco)
- i2pIM (devs: thecrypto)
- httptunnel (devs: mihi)
- MyI2P address book (devs: jrandom)
- MyI2P blogging (devs: jrandom)

## 6) ???

Şimdilik aklıma gelenler bu kadar - bu gece ilerleyen saatlerdeki toplantıya uğrayıp biraz sohbet edelim. Her zamanki gibi, GMT 21:00'de, alışıldık sunuculardaki #i2p kanalında.

=jr
