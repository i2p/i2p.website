---
title: "2005-04-19 tarihli I2P Durum Notları"
date: 2005-04-19
author: "jr"
description: "0.5.0.7 için yaklaşan düzeltmeleri, SSU UDP taşıma katmanındaki ilerlemeyi, 0.6’yı Haziran’a taşıyan yol haritası değişikliklerini ve Q geliştirme çalışmalarını kapsayan haftalık güncelleme"
categories: ["status"]
---

Selam herkese, haftanın o zamanı yine geldi,

* Index

1) Ağ durumu 2) SSU durumu 3) Yol haritası güncellemesi 4) Q durumu 5) ???

* 1) Net status

0.5.0.6 yayınlandığından beri geçen neredeyse iki haftalık sürede işler çoğunlukla olumlu gitti, ancak hizmet sağlayıcıları (eepsites(I2P Sites), ircd, vb.) son zamanlarda bazı hatalarla karşılaşıyor. İstemciler iyi durumda olsa da, zamanla bir sunucu, başarısız olan tunnel'ların bazı aşırı throttling (hız kısıtlama) kodlarını tetikleyebildiği bir durumla karşılaşabilir; bu da leaseSet'in düzgün şekilde yeniden oluşturulmasını ve yayınlanmasını engelleyebilir.

CVS'de, başka şeylerin yanı sıra, bazı düzeltmeler yapıldı ve yeni 0.5.0.7 sürümünü bir iki gün içinde yayımlayacağımızı bekliyorum.

* 2) SSU status

Benim (pek heyecanlı!) blogumu takip etmeyenler için, UDP aktarımıyla ilgili epey ilerleme kaydedildi ve şu anda UDP aktarımının aktarım hızı açısından darboğazımız olmayacağını söylemek oldukça güvenli :) Bu kodu hata ayıklarken, üst düzeylerdeki kuyruklamayı da gözden geçirme fırsatını buldum ve gereksiz tıkanma noktalarını kaldırabileceğimiz yerleri belirledim. Yine de, geçen hafta söylediğim gibi, yapılacak daha çok iş var. Daha fazla bilgi mevcut olduğunda daha fazla bilgi mevcut olacak.

* 3) Roadmap update

Artık Nisan ayındayız, bu yüzden yol haritası [1] buna göre güncellendi - 0.5.1’i iptal edip bazı tarihleri kaydırarak. En büyük değişiklik 0.6’yı Nisan’dan Haziran’a taşımak, gerçi bu göründüğü kadar büyük bir değişiklik değil. Geçen hafta belirttiğim gibi, kendi programım biraz kaydı ve Haziran ayında taşınmak yerine Mayıs ayında taşınıyorum; gidilecek yer $somewhere. Bu ay 0.6 için gerekli olanları hazır hâle getirebilsek de, böylesine büyük bir güncellemeyi alelacele yayımlayıp sonra bir ay ortadan kaybolmam mümkün değil; çünkü yazılımın gerçeği, testlerde yakalanmayan hataların mutlaka olacağıdır.

[1] http://www.i2p.net/roadmap

* 4) Q status

Aum bir süredir Q üzerinde harıl harıl çalışıyor, bizim için daha fazla güzellik ekliyor; en son ekran görüntüleri de sitesinde [2] yayında. Ayrıca kodu CVS'e de commit etti (yaşasın), bu yüzden umarız yakında alfa testine başlayabileceğiz. Eminim nasıl yardımcı olunacağına dair ayrıntılarla aum'dan daha çok haber alacağız, ya da CVS'de i2p/apps/q/ dizinindeki güzelliklere dalabilirsiniz

[2] http://aum.i2p/q/

* 5) ???

Ayrıca posta listesinde, forumda ve irc'de canlı tartışmalarla birlikte başka pek çok şey de oluyor. Toplantıya sadece birkaç dakika kaldığı için bunları burada özetlemeye çalışmayacağım; ancak değinilmemiş olup da gündeme getirmek istediğiniz bir şey varsa bir uğrayın!

=jr
