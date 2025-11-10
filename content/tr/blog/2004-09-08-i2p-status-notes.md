---
title: "2004-09-08 tarihli I2P Durum Notları"
date: 2004-09-08
author: "jr"
description: "0.4 sürümünü, ağ kapasitesi sorunlarını, web sitesi güncellemelerini ve I2PTunnel arayüz iyileştirmelerini kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Herkese merhaba, geç kaldığım için özür dilerim...

## Dizin:

1. 0.4
2. Capacity and overload
3. Website updates
4. I2PTunnel web interface
5. Roadmap and todo
6. ???

## 1) 0.4

Eminim hepinizin de gördüğü gibi, 0.4 sürümü geçen gün yayınlandı ve genel olarak her şey gayet iyi gidiyor. 0.3'ün yayınlanmasından bu yana 6 ay (ve 1.0 SDK'nin yayınlanmasından bu yana bir yıl) geçtiğine inanmak zor, ama çok yol katettik ve hepinizin sıkı çalışması, coşkusu ve sabrı harikalar yarattı. Tebrikler ve teşekkürler!

Her iyi sürümde olduğu gibi, yayımlanır yayımlanmaz bazı sorunlar bulduk ve son birkaç gündür hata raporları birikiyor, biz de çılgınlar gibi yamalar uyguluyoruz (düzeltildikçe değişiklikleri izleyebilirsiniz). Bir sonraki revizyonu yayımlamadan önce ezmemiz gereken birkaç hata daha var, ancak bunun önümüzdeki bir gün kadar içinde tamamlanmış olmalı.

## 2) Kapasite ve aşırı yüklenme

Son birkaç sürümde tunnels tahsislerinin epey dengesiz olduğunu gördük ve bunların bazıları hata kaynaklı olsa da (0.4 sürümü çıktığından beri bunlardan ikisi düzeltildi), hâlâ ortada genel bir algoritma sorusu var - bir router daha fazla tunnels kabul etmeyi ne zaman bırakmalı?

Birkaç sürüm önce, router aşırı yüklendiğinde (yerel mesaj işleme süresi 1s'yi aştığında) bir tunnel'e katılma taleplerini reddetmek için hız sınırlama kodu ekledik ve bu kayda değer ölçüde yardımcı oldu. Ancak, o basit algoritmanın ele alınmayan iki yönü var: - bant genişliğimiz doygunluğa ulaştığında, yerel işleme süremiz yine de hızlı olabilir, bu yüzden daha fazla tunnel isteğini kabul etmeye devam ederiz - tek bir peer (eş düğüm) "çok fazla" tunnel'e katıldığında, bunlar başarısız olduğunda, bu ağ için daha zararlı olur.

İlk sorun, basitçe bant genişliği sınırlayıcısını etkinleştirerek oldukça kolay şekilde ele alınır (çünkü bant genişliği sınırlaması, bant genişliği gecikmesine uygun olarak mesaj işleme süresini yavaşlatır). İkincisi daha karmaşıktır ve hem daha fazla araştırma hem de daha fazla simülasyon gerektirir. Aklımdaki şey, ağda içinde yer aldığımız tunnel (tünel) sayısı ile ağdan istenen tunnel sayısının oranına dayanarak, bazı temel bir "kindness factor" da dahil edilmek suretiyle, tunnel isteklerini olasılıksal olarak reddetmek; eğer içinde yer aldığımız sayı bundan azsa P(reject) = 0 olarak ayarlamak.

Ama dediğim gibi, daha fazla çalışma ve simülasyon gerekli.

## 3) Web sitesi güncellemeleri

Artık yeni I2P web arayüzüne sahip olduğumuza göre, eski son kullanıcı belgelerimizin neredeyse tamamı geçersiz hale geldi. Bu sayfaları gözden geçirmek ve artık her şeyin nasıl olduğunu anlatacak şekilde güncellemek için yardıma ihtiyacımız var. duck ve diğerlerinin önerdiği gibi, `http://localhost:7657/` readme belgesinin ötesinde yeni bir 'kickstart' (hızlı başlangıç) kılavuzuna ihtiyacımız var - insanların hemen kullanmaya başlayıp sisteme girebilmelerini sağlayacak bir şeye.

Ayrıca, yeni web arayüzümüz bağlam duyarlı yardımı entegre etmek için bolca alan sunuyor. Pakete dahil edilen help.jsp'de görebileceğiniz gibi, "hmm. muhtemelen burada biraz yardım metni olmalı."

Farklı sayfalara, terimlerin ne anlama geldiğini ve nasıl kullanılacağını açıklayan 'hakkında' ve/veya 'sorun giderme' bağlantıları ekleyebilsek muhtemelen harika olur.

## 4) I2PTunnel web arayüzü

Yeni `http://localhost:7657/i2ptunnel/` arayüzünü 'aşırı sade' olarak nitelendirmek az bile olur. Bunu kullanılabilir bir duruma yaklaştırmak için çok iş yapmamız gerekiyor - şu anda işlevsellik teknik olarak mevcut, ancak onu anlamlandırabilmek için perde arkasında neler olup bittiğini gerçekten bilmeniz gerekiyor. duck'ın bu konuda, toplantı sırasında gündeme getirebileceği bazı ek fikirleri olduğunu düşünüyorum.

## 5) Yol haritası ve yapılacaklar

Yol haritasını güncel tutma konusunda geri kaldım, ancak işin aslı şu ki önümüzde bazı ek revizyonlar var. Benim "büyük sorunlar" olarak gördüklerimi açıklamaya yardımcı olmak için, her biri hakkında biraz ayrıntıya giren yeni bir görev listesi hazırladım. Bence bu noktada seçeneklerimizi gözden geçirmeye ve belki de yol haritasını yeniden düzenlemeye oldukça açık olmalıyız.

O yapılacaklar listesinde bahsetmeyi unuttuğum bir şey de şu: hafif bağlantı protokolünü eklerken IP adresinin (isteğe bağlı) otomatik algılanmasını da dahil edebiliriz. Bu 'tehlikeli' olabilir (bu yüzden isteğe bağlı olacak), ancak aldığımız destek taleplerinin sayısını dramatik biçimde azaltacaktır :)

Neyse, yapılacaklar listesine eklenen görevler çeşitli sürümler için planladıklarımızdır ve kesinlikle hepsinin 1.0'a, hatta 2.0'a bile girmesi söz konusu değil. Birkaç farklı olası önceliklendirme/sürüm taslağı çıkardım, ama bunları henüz kesinleştirmiş değilim. Ancak insanlar ileride başka büyük konuları belirleyebilirse çok takdir edilir; çünkü planlanmamış bir iş her zaman baş belasıdır.

## 6) ???

Tamam, şimdilik bende bu kadar (iyi ki de öyle, çünkü toplantı birkaç dakika içinde başlıyor). Daha fazla sohbet etmek için GMT'ye göre saat 21:00'de irc.freenode.net üzerindeki #i2p kanalına, www.invisiblechat.com veya irc.duck.i2p adreslerine uğrayın.
