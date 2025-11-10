---
title: "2005-11-08 için I2P Durum Notları"
date: 2005-11-08
author: "jr"
description: "0.6.1.4 kararlılığı, performans optimizasyonu yol haritası, I2Phex 0.1.1.35 sürümü, I2P-Rufus BitTorrent istemcisi geliştirilmesi, I2PSnarkGUI ilerlemesi ve Syndie kullanıcı arayüzü yenilemelerini kapsayan haftalık güncelleme"
categories: ["status"]
---

Selam millet, yine salı

* Index

1) Ağ durumu / kısa vadeli yol haritası 2) I2Phex 3) I2P-Rufus 4) I2PSnarkGUI 5) Syndie 6) ???

* 1) Net status / short term roadmap

0.6.1.4 hâlâ oldukça sağlam görünüyor, gerçi o zamandan beri CVS'de bazı hata düzeltmeleri yapıldı. Ayrıca verileri daha verimli aktarması için SSU için bazı optimizasyonlar da ekledim; bunun yaygın olarak kullanıma sunulduğunda ağ üzerinde fark edilir bir etkisi olacağını umuyorum. Yine de şimdilik 0.6.1.5'i bekletiyorum, çünkü bir sonraki sürüme dahil etmek istediğim birkaç başka şey daha var. Mevcut plan bunu bu hafta sonu yayımlamak, o yüzden son gelişmeler için takipte kalın.

0.6.2 sürümü, daha da güçlü saldırganlara karşı koymak için pek çok harika yenilik içerecek, ancak etkilemeyeceği tek şey performans. Her ne kadar anonimlik I2P’nin tüm amacı olsa da, aktarım hızı ve gecikme kötüyse hiç kullanıcımız olmaz. Bu nedenle, planım 0.6.2 eş sıralama stratejilerini ve yeni tunnel oluşturma tekniklerini uygulamaya geçmeden önce performansı olması gereken düzeye getirmek.

* 2) I2Phex

Son zamanlarda I2Phex cephesinde de epey hareketlilik var; yeni bir 0.1.1.35 sürümü yayınlandı [1]. Ayrıca CVS'de de ek değişiklikler yapıldı (teşekkürler Legion!), bu yüzden bu hafta ilerleyen günlerde 0.1.1.36 görürsem şaşırmam.

gwebcache cephesinde de bazı iyi gelişmeler oldu (bkz. http://awup.i2p/), ancak bildiğim kadarıyla I2P özellikli bir gwebcache kullanacak şekilde I2Phex'in değiştirilmesi üzerinde çalışmaya başlayan kimse yok (ilgileniyor musunuz? bana haber verin!).

[1] http://forum.i2p.net/viewtopic.php?t=1157

* 3) I2P-Rufus

Söylentilere göre defnax ve Rawn, Rufus BT istemcisi üzerinde çalışıyor ve I2P-BT'den bazı I2P ile ilgili kodları birleştiriyorlar. Portun mevcut durumunu bilmiyorum, ama güzel özelliklere sahip olacak gibi görünüyor. Eminim paylaşılacak daha fazla şey olduğunda daha fazlasını duyacağız.

* 4) I2PSnarkGUI

Dolaşan bir başka söylenti de Markus'un yeni bir C# grafik kullanıcı arayüzü (GUI) üzerinde bazı çalışmalar yaptığı... PlanetPeer'deki ekran görüntüleri oldukça güzel görünüyor [2]. Platformdan bağımsız bir web arayüzü için hâlâ planlar var, ama bu da oldukça güzel görünüyor. GUI ilerledikçe Markus'tan daha fazla haber alacağımızdan eminim.

[2] http://board.planetpeer.de/index.php?topic=1338

* 5) Syndie

Ayrıca Syndie kullanıcı arayüzü yenilemeleri [3] ile ilgili de bazı tartışmalar sürüyor ve bu alanda oldukça yakında bazı ilerlemeler göreceğimizi bekliyorum. dust ayrıca Sucker üzerinde yoğun şekilde çalışıyor; Syndie'ye daha fazla RSS/Atom beslemeyi çekmek için daha iyi destek ekliyor ve SML'in bizzat kendisine yönelik bazı iyileştirmeler yapıyor.

[3] http://syndiemedia.i2p.net:8000/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1131235200000&expand=true

* 6) ???

Her zamanki gibi, bir sürü şey oluyor. Haftalık geliştirici toplantımız için birkaç dakika içinde #i2p kanalına uğrayın.

=jr
