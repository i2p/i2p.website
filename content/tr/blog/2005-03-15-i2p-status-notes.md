---
title: "2005-03-15 tarihli I2P Durum Notları"
date: 2005-03-15
author: "jr"
description: "Ağ performansı analizi, hız hesaplama iyileştirmeleri ve Feedspace geliştirme çalışmalarını kapsayan haftalık I2P geliştirme durum notları"
categories: ["status"]
---

Herkese selam, haftalık güncelleme zamanı

* Index

1) Ağ durumu 2) Feedspace 3) ???

* 1) Net status

Geçen hafta boyunca zamanımın büyük kısmını ağın davranışını analiz etmeye, istatistikleri izlemeye ve simülatörde çeşitli olayları yeniden üretmeye çalışmaya harcadım. Tuhaf ağ davranışının bir kısmı, hâlâ eski sürümleri kullanan yaklaşık iki düzine router ile açıklanabilse de, asıl etken hız hesaplamalarımızın bize iyi veri sağlamaması - veriyi hızla aktarabilen eşleri doğru şekilde belirleyemiyoruz. Geçmişte bu pek sorun değildi, çünkü bir hata nedeniyle, kapasiteye dayalı katmanları doğru şekilde oluşturmak yerine en yüksek kapasiteli 8 eşi 'fast' havuzu olarak kullanıyorduk. Mevcut hız hesaplamamız periyodik bir gecikme testinden türetilmiştir (özellikle bir tunnel testinin RTT'si), ancak bu, değere güven duymak için yetersiz veri sağlıyor. İhtiyacımız olan, gerekli olduğunda 'yüksek kapasite' eşlerin 'fast' katmanına terfi etmesine izin verirken daha fazla veri noktası toplamamızı sağlayacak daha iyi bir yöntem.

Karşı karşıya olduğumuz temel sorunun bu olduğunu doğrulamak için, biraz hileye başvurdum ve belirli bir tunnel pool'un (tünel havuzu) seçiminde hangi eşlerin kullanılacağını elle belirlemeye olanak tanıyan bir işlev ekledim. Elle seçtiğim bu eşlerle, irc üzerinde iki günden fazla süre bağlantı kopmadan kaldım ve kontrol ettiğim başka bir hizmette de oldukça makul bir performans aldım. Yaklaşık son iki gündür, bazı yeni istatistikleri kullanan yeni bir hız hesaplayıcısını deniyorum ve seçimde iyileşme sağlamış olsa da hâlâ bazı sorunları var. Bu öğleden sonra birkaç alternatif üzerinde çalıştım, ancak bunları ağda denemek için yapılacak işler hâlâ var.

* 2) Feedspace

Frosk, i2pcontent/fusenet dokümantasyonunun bir başka revizyonunu yayınladı; ancak bu kez yeni bir adla ve yeni bir yerde: http://feedspace.i2p/ - Destination (I2P adresi) için orion [1] ya da bloguma [2] bakın. Bu iş gerçekten umut verici görünüyor; hem "vay canına, müthiş işlevsellik" açısından hem de "bu, I2P'nin anonimliğine yardımcı olacak" açısından. Frosk ve ekip harıl harıl çalışıyor, ama kesinlikle geri bildirim (ve yardım) arıyorlar. Belki toplantıda Frosk'tan bir güncelleme alabiliriz?

[1] http://orion.i2p/#feedspace.i2p [2] http://jrandom.dev.i2p/

* 3) ???

Tamam, pek bir şeye benzemeyebilir, ama aslında çok şey oluyor, gerçekten :) Eminim bazı şeyleri de kaçırmışımdır, o yüzden toplantıya uğrayın ve neler olup bittiğine bakın.

=jr
