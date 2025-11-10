---
title: "2005-03-01 tarihli I2P Durum Notları"
date: 2005-03-01
author: "jr"
description: "0.5.0.1 hatalarını ve yakında çıkacak 0.5.0.2'yi, yol haritası güncellemelerini, adres defteri düzenleyicisini ve i2p-bt güncellemelerini kapsayan haftalık I2P geliştirme durum notları"
categories: ["status"]
---

Herkese selam, durum güncellememizin zamanı geldi.

* Index

1) 0.5.0.1 2) yol haritası 3) adres defteri düzenleyicisi ve yapılandırma 4) i2p-bt 5) ???

* 1) 0.5.0.1

Geçen hafta tartıştığımız gibi, toplantıdan birkaç saat sonra, (başka şeylerin yanı sıra) 0.5’te çok sayıda tunnel oluşturulmasına yol açan hataları düzelten yeni 0.5.0.1 sürümünü yayınladık. Genel olarak, bu sürüm işleri iyileştirdi, ancak daha geniş testlerde bazı kişileri etkileyen ek hatalara rastladık. Özellikle, 0.5.0.1 sürümü, yavaş bir makineniz varsa veya router’ınızdaki tunnel’lar toplu halde başarısız olursa çok fazla CPU tüketebilir ve uzun süre çalışan bazı I2PTunnel sunucuları, sistem OOM’a (Out Of Memory - bellek tükenmesi) düşene kadar RAM’i tüketebilir. Ayrıca streaming lib (akış kütüphanesi) içinde de uzun süredir devam eden bir hata var; bazı hatalar belirli bir şekilde meydana gelirse bağlantı kuramayabiliriz.

Bunların çoğu (diğerlerinin yanı sıra) cvs'de düzeltildi, ancak bazıları hâlâ çözülmemiş durumda. Hepsi düzeltildiğinde, paketleyip 0.5.0.2 sürümü olarak yayınlayacağız. Bunun ne zaman olacağından tam emin değilim; umarım bu hafta, ama göreceğiz.

* 2) roadmap

Büyük sürümlerden sonra, yol haritası [1] sanki ... revize ediliyor.  0.5 sürümü de farklı değildi.  Bu sayfa, ileriye dönük olarak makul ve uygun olduğunu düşündüklerimi yansıtıyor, ama elbette, daha fazla insan işlere yardımcı olmak için katılırsa, buna göre revize edilebilir.  0.6 ile 0.6.1 arasında kayda değer bir ara olduğunu fark edeceksiniz ve bu, çok fazla çalışma yapıldığını yansıtmakla birlikte, aynı zamanda taşınacak olmam gerçeğini de yansıtıyor (yine yılın o zamanı).

[1] http://www.i2p.net/roadmap

* 3) addressbook editor and config

Detonate, adres defteri girdilerini (hosts.txt) yönetmek için web tabanlı bir arayüz üzerinde çalışmaya başladı ve bu oldukça umut verici görünüyor. Belki toplantı sırasında detonate'den bir güncelleme alabiliriz?

Ayrıca, smeghead adres defteri yapılandırmasını (subscriptions.txt, config.txt) yönetmek için web tabanlı bir arayüz üzerinde bir süredir çalışıyor. Belki toplantı sırasında smeghead'den bir güncelleme alabiliriz?

* 4) i2p-bt

i2p-bt cephesinde bazı ilerlemeler kaydedildi; geçen haftaki toplantıda tartışıldığı üzere azneti2p uyumluluk sorunlarını ele alan yeni 0.1.8 sürümü yayımlandı. Belki toplantı sırasında duck veya smeghead'den bir güncelleme alabiliriz?

Legion ayrıca i2p-bt rev'den bir fork (çatallanma) oluşturdu, başka bazı kodları birleştirdi, bazı şeyleri yamaladı ve kendi eepsite(I2P Site) üzerinde bir Windows binary (ikili dosya) mevcut. Duyuru [2], kaynak kodun erişime açılabileceğini ima ediyor gibi görünüyor, ancak şu anda eepsite(I2P Site) üzerinde yer almıyor. I2P geliştiricileri o istemcinin kodunu denetlemedi (hatta görmedi) bile, bu nedenle anonimliğe ihtiyaç duyanlar önce kodun bir kopyasını edinip gözden geçirmek isteyebilir.

[2] http://forum.i2p.net/viewtopic.php?t=382

Ayrıca Legion'un BitTorrent istemcisinin 2. sürümü üzerinde de çalışmalar var, ancak bunun durumu hakkında bilgim yok. Belki toplantı sırasında Legion'dan bir güncelleme alabiliriz?

* 5) ???

Şimdilik söyleyeceklerim bu kadar, bir sürü şey oluyor.  Toplantı sırasında belki güncellemesini alabileceğimiz işler üzerinde çalışan başka kimse var mı?

=jr
