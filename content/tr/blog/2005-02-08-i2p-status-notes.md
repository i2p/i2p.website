---
title: "2005-02-08 tarihli I2P Durum Notları"
date: 2005-02-08
author: "jr"
description: "0.4.2.6 güncellemelerini, Bloom filtreleriyle 0.5 tunnel ilerlemesini, i2p-bt 0.1.6’yı ve Fortuna PRNG’yi kapsayan haftalık I2P geliştirme durum notları"
categories: ["status"]
---

Selam millet, yine güncelleme zamanı

* Index

1) 0.4.2.6-* 2) 0.5 3) i2p-bt 0.1.6 4) fortuna 5) ???

* 1) 0.4.2.6-*

Öyle görünmese de, 0.4.2.6 sürümü çıktığından beri bir aydan fazla oldu ve işler hâlâ oldukça iyi durumda.  O zamandan beri bir dizi epey faydalı güncelleme [1] geldi, ancak yeni bir sürümün yayımlanmasını gerektirecek gerçek bir show stopper (kritik engelleyici sorun) olmadı.  Bununla birlikte, son bir iki gün içinde bize gerçekten iyi hata düzeltmeleri gönderildi (teşekkürler anon ve Sugadude!) ve 0.5 sürümünün eşiğinde olmasaydık muhtemelen paketleyip yayımlardım.  anon'un güncellemesi, streaming lib (akış kitaplığı) içinde BT ve diğer büyük aktarımlarda görülen zaman aşımı sorunlarının çoğuna neden olan bir sınır koşulunu düzeltiyor, bu yüzden kendinizi biraz maceracı hissediyorsanız CVS HEAD'i alın ve deneyin.  Ya da elbette bir sonraki sürümü bekleyin.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) 0.5

0.5 cephesinde çok ama çok ilerleme var (buna i2p-cvs listesindeki [2] herkes tanıklık edebilir). Tüm tunnel güncellemeleri ve çeşitli performans ayarları test edildi ve çeşitli [3] zorunlu sıralama algoritmaları açısından pek bir şey içermese de, temelleri kapsıyor. Ayrıca, XLattice [5]'ten (BSD lisanslı) Bloom filtreleri [4] entegre ettik; bu sayede mesaj başına herhangi bir bellek kullanımı gerektirmeden ve neredeyse 0ms ek yükle yeniden oynatma saldırılarını tespit edebiliyoruz. İhtiyaçlarımızı karşılamak için, filtreler basitçe zamanla sönümlenecek şekilde genişletildi; böylece bir tunnel'in süresi dolduktan sonra, filtre artık o tunnel'da gördüğümüz IV'leri (Initialization Vector - başlatma vektörü) barındırmıyor.

0.5 sürümüne olabildiğince çok şeyi dahil etmeye çalışırken, aynı zamanda beklenmeyeni de beklememiz gerektiğinin farkındayım - yani bunu iyileştirmenin en iyi yolu, onu sizin ellerinize ulaştırıp sizin için nasıl çalıştığını (ve nasıl çalışmadığını) görerek öğrenmektir. Bunu desteklemek için, daha önce de belirttiğim gibi, 0.5 sürümünü yayımlayacağız (umarım gelecek hafta çıkar), geriye dönük uyumluluğu bozarak, ardından buradan yola çıkarak iyileştirmeler üzerinde çalışacak ve hazır olduğunda 0.5.1 sürümünü yayımlayacağız.

Yol haritasına [6] geri baktığımızda, 0.5.1’e ertelenen tek şey katı sıralama. Zamanla hız sınırlama ve yük dengelemede de iyileştirmeler olacak, eminim, ama bunun üzerinde muhtemelen sonsuza dek ince ayar yapmayı sürdüreceğimizi tahmin ediyorum. 0.5’e dahil etmeyi umduğum, indirme aracı ve tek tıkla güncelleme kodu gibi başka konular da konuşulmuştu, ancak bunların da erteleneceği anlaşılıyor.

[2] http://dev.i2p.net/pipermail/i2p-cvs/2005-February/thread.html [3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                     tunnel-alt.html?rev=HEAD#tunnel.selection.client [4] http://en.wikipedia.org/wiki/Bloom_filter [5] http://xlattice.sourceforge.net/index.html [6] http://www.i2p.net/roadmap

* 3) i2p-bt 0.1.6

duck yeni bir i2p-bt sürümünü yamalayıp yayınladı (yaşasın!); her zamanki yerlerde mevcut, sıcakken kapın [7]. Bu güncelleme ve anon'un streaming lib yaması sayesinde, birkaç dosyayı seed ederken uplink (yükleme bağlantısı) kapasitemi neredeyse tamamen doldurdum, o yüzden bir deneyin.

[7] http://forum.i2p.net/viewtopic.php?t=300

* 4) fortuna

Geçen haftaki toplantıda da belirtildiği gibi, smeghead son zamanlarda bir dizi farklı güncelleme üzerinde aralıksız çalışıyor ve I2P’yi gcj ile çalışır hâle getirmek için uğraşırken bazı JVM’lerde gerçekten çok kötü PRNG (psödo-rastgele sayı üreteci) sorunları ortaya çıktı; bu da güvenebileceğimiz bir PRNG’ye sahip olma konusunu adeta dayattı. GNU-Crypto ekibinden yanıt aldıktan sonra, onların fortuna uygulaması henüz gerçekten devreye alınmamış olsa da, ihtiyaçlarımıza en iyi uyum sağlayacak seçenek gibi görünüyor. Bunu 0.5 sürümüne dahil edebiliriz, ancak büyük olasılıkla 0.5.1’e ertelenecek; çünkü gerekli miktarda rastgele veri sağlayabilmesi için üzerinde biraz ince ayar yapmak isteyeceğiz.

* 5) ???

Bir sürü şey oluyor ve son zamanlarda forum [8] de epey hareketlendi, bu yüzden eminim bazı şeyleri gözden kaçırmışımdır. Her neyse, birkaç dakika içinde toplantıya uğrayın ve aklınızdakileri söyleyin (ya da sadece sessizce takılıp arada bir alaycı yorum atın).

=jr [8] http://forum.i2p.net/
