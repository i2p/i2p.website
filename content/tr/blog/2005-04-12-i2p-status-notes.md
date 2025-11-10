---
title: "2005-04-12 tarihli I2P Durum Notları"
date: 2005-04-12
author: "jr"
description: "0.5.0.6 netDb düzeltmeleri, SSU UDP taşımasındaki ilerleme, Bayesçi eş (peer) profilleme sonuçları ve Q geliştirmesini kapsayan haftalık güncelleme"
categories: ["status"]
---

Selam millet, yine güncelleme zamanı

* Index

1) Ağ durumu 2) SSU durumu 3) Bayesyen eş profillemesi 4) Q durumu 5) ???

* 1) Net status

Geçen haftaki 0.5.0.6 sürümü, gördüğümüz netDb sorunlarını düzeltmiş gibi görünüyor (yaşasın). Siteler ve hizmetler 0.5.0.5’e kıyasla çok daha güvenilir, ancak birkaç günlük çalışma süresinin ardından bir site veya hizmetin erişilemez hale gelmesiyle ilgili bazı sorun bildirimleri de oldu.

* 2) SSU status

0.6 UDP kodunda çok fazla ilerleme kaydedildi; ilk grup commit zaten CVS'ye yapıldı. Henüz pratikte kullanabileceğiniz bir şey değil, ancak temel unsurlar yerinde. Oturum müzakeresi iyi çalışıyor ve yarı güvenilir mesaj iletimi beklendiği gibi çalışıyor. Yine de yapılacak çok iş var; yazılacak test senaryoları ve hata ayıklanacak alışılmadık durumlar bulunuyor, ama bu da ilerleme.

İşler yolunda giderse, gelecek hafta yalnızca güvenlik duvarlarını/NAT’lerini elle yapılandırabilen kişiler için bazı alfa testleri yapabiliriz. Aktarıcı işleyicisini eklemek, netDb’yi routerInfo (yönlendirici bilgisi kaydı) ömrünün daha hızlı sona ermesi için ayarlamak ve yayınlanacak aktarıcıları seçmekten önce genel işleyişi iyice oturtmak istiyorum. Ayrıca, ele aldığımız birkaç kritik kuyruklama etkeni olduğu için bu fırsatı bir dizi kapsamlı test yapmak için de kullanacağım.

* 3) Bayesian peer profiling

bla, tunnel'ları hangi eşler (peer'lar) üzerinden geçireceğimize nasıl karar verdiğimizle ilgili bazı revizyonlar üzerinde bir süredir yoğun biçimde çalışıyor; bla toplantıya katılamamış olsa da, paylaşılacak bazı ilginç veriler var:

<+bla> Doğrudan düğüm hız ölçümleri yaptım: OB tunnels uzunluğu 0, IB tunnels uzunluğu 1 kullanarak yaklaşık 150 düğümün profilini çıkardım, batching-interval = 0ms
<+bla> Buna ek olarak, naif Bayesçi sınıflandırma kullanarak _çok_ temel ve _ilk_ hız tahmini yaptım
<+bla> İkincisi varsayılan expl. tunnel uzunlukları kullanılarak yapıldı
<+bla> "ground truth" (doğrulanmış gerçek ölçüm verisi) sahibi olduğum düğümler kümesi ile mevcut ölçümlerdeki düğümler kümesinin kesişimi 117 düğüm
<+bla> Sonuçlar _o kadar_ kötü değil, ama çok da etkileyici sayılmaz
<+bla> Bkz. http://theland.i2p/estspeed.png
<+bla> Temel düzeyde çok yavaş/hızlı ayrımı fena değil, ancak daha hızlı eşler arasındaki ince ayrım çok daha iyi olabilir
<+jrandom2p> hmm, gerçek değerler nasıl hesaplandı - bu tam RTT mi yoksa RTT/uzunluk mu?
<+bla> Normal expl. tunnels kullanıldığında, yığınlama gecikmelerini önlemek neredeyse imkânsız.
<+bla> Gerçek değerler ground truth değerleri: OB=0 ve IB=1 kullanılarak elde edilenler
<+bla> (ve variance=0, ve batching gecikmesi yok)
<+jrandom2p> yine de buradan bakınca sonuçlar oldukça iyi görünüyor
<+bla> Tahmin edilen zamanlamalar, uzunluğu 2 +/- 1 olan _gerçek_ expl. tunnels üzerinden Bayesçi çıkarım kullanılarak elde edilenlerdir.
<+bla> Bu, yaklaşık 3 saatlik bir süre boyunca kaydedilmiş 3000 RTT'den elde edildi (bu uzun).
<+bla> Şimdilik eş hızının sabit olduğunu varsayıyor. Ağırlıklandırmayı henüz uygulamadım
<+jrandom2p> müthiş görünüyor. güzel iş bla
<+jrandom2p> hmm, o hâlde tahmin gerçek değerin 1/4'üne eşit olmalı
<+bla> jrandom: Hayır: Ölçülen tüm RTT'ler (normal expl. tunnels kullanılarak) gidiş-dönüşteki atlama sayısına göre düzeltiliyor
<+jrandom2p> ah tamam
<+bla> Ancak ondan sonra Bayesçi sınıflandırıcı eğitiliyor
<+bla> Şimdilik, ölçülen atlama başına süreleri 10 sınıfa ayırıyorum: 50, 100, ..., 450 ms ve ayrıca >500 ms için bir sınıf.
<+bla> Örneğin, küçük atlama başına gecikmeler daha büyük bir faktörle ağırlıklandırılabilir; tam başarısızlıklar (>60000 ms) için de aynı şekilde.
<+bla> Yine de... tahmin edilen zamanlamaların %65'i, gerçek düğüm süresinden 0.5 standart sapma içinde kalıyor.
<+bla> Ancak bu yeniden yapılmalı, çünkü standart sapma >60000 ms başarısızlıklardan ciddi biçimde etkileniyor.

Daha fazla tartışmanın ardından, bla mevcut hız hesaplayıcısıyla bir karşılaştırma sundu, @ http://theland.i2p/oldspeed.png adresinde yayınlandı Bu PNG'lerin aynaları şuralarda: http://dev.i2p.net/~jrandom/estspeed.png ve http://dev.i2p.net/~jrandom/oldspeed.png

(terminoloji açısından, IB=gelen tunnel hop sayısı, OB=giden tunnel hop sayısı, ve bazı netleştirmelerin ardından, "ground truth" (doğru kabul edilen referans) ölçümleri 1 hop giden ve 0 hop gelen kullanılarak elde edildi, tam tersi değil)

* 4) Q status

Aum, Q üzerinde de büyük ilerlemeler kaydediyor; son olarak web tabanlı bir istemci arayüzü üzerinde çalışıyor. Bir sonraki Q derlemesi, çok sayıda yeni özellik içerdiği için geriye dönük uyumlu olmayacak; ama eminim, duyurulacak daha fazla bilgi olduğunda Aum'dan daha fazlasını duyacağız :)

* 5) ???

Şimdilik bu kadar (toplantı zamanı gelmeden bunu toparlamam lazım). Bu arada, görünüşe göre planlanandan daha erken taşınacağım, dolayısıyla taşınma sürecindeyken yol haritasındaki bazı tarihler kayabilir. Neyse, birkaç dakika içinde kanala uğrayıp bizi yeni fikirlerle sıkıştırın!

=jr
