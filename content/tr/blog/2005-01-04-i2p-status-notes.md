---
title: "I2P 2005-01-04 Tarihli Durum Notları"
date: 2005-01-04
author: "jr"
description: "2005'in ilk haftalık durum notları: ağın 160 router'a kadar büyümesi, 0.4.2.6 özellikleri ve 0.5 geliştirmesi"
categories: ["status"]
---

Herkese selam, 2005 yılındaki ilk haftalık durum notlarımızın vakti geldi

* Index

1) Ağ durumu 2) 0.4.2.6 3) 0.5 4) jabber @ chat.i2p 5) ???

* 1) Net status

Son bir haftadır ağda işler oldukça ilginçti - yılbaşı gecesinde, i2p-bt hakkında konuşan popüler bir web sitesine bazı yorumlar gönderildi ve küçük bir yeni kullanıcı akını yaşadık. Şu anda ağda 120-150 arasında routers var, ancak bu birkaç gün önce 160 ile zirve yapmıştı. Yine de ağ ayakta kaldı; yüksek kapasiteli eşler fazla yükü üstlenerek diğer eşleri pek etkilemeden bunu karşıladı. Gerçekten hızlı bağlantılarda bant genişliği sınırı olmadan çalışan bazı kullanıcılar 2-300KBps veri aktarım hızları bildirdiler; daha az kapasiteye sahip olanlar ise genelde düşük 1-5KBps hızları görüyor.

Sanırım Connelly’nin, yılbaşından sonraki birkaç gün içinde 300+ farklı router gördüğünü söylediğini hatırlıyorum; yani kayda değer bir oynaklık olmuş. Öte yandan, artık önceki 80-90’ın aksine istikrarlı olarak çevrimiçi 120-150 kullanıcı var; bu makul bir artış. Yine de şimdilik bunun çok fazla büyümesini *istemiyoruz*, çünkü hâlâ çözülmesi gereken bilinen implementasyon sorunları var. Özellikle, 0.6 sürümü [1] çıkana kadar, iş parçacığı sayısını makul bir düzeyde tutmak için 2-300 peer (eş düğüm) seviyesinin altında kalmak isteyeceğiz. Ancak biri UDP transport (UDP taşıma katmanı) gerçekleştirilmesine yardım etmek isterse, oraya çok daha hızlı ulaşabiliriz.

Son bir haftada i2p-bt trackerlarının yayınladığı istatistikleri izledim ve gigabaytlarca büyük dosya aktarıldı; bazı raporlarda 80-120KBps bildirildi. IRC, o yorumlar o web sitesine yayınlandığından beri normalden daha fazla aksama yaşadı, ancak bağlantı kopmaları arasındaki süre hâlâ saat mertebesinde. (Gördüğüm kadarıyla, irc.duck.i2p'nin üzerinde bulunduğu router bant genişliği sınırına oldukça yakın çalışıyor, bu da durumu açıklayabilir)

[1] http://www.i2p.net/roadmap#0.6

* 2) 0.4.2.6

0.4.2.5 sürümünden bu yana CVS'e, yakında kullanıma sunmak isteyeceğimiz bazı düzeltmeler ve yeni özellikler eklendi; bunlar arasında streaming lib (akış kütüphanesi) için güvenilirlik düzeltmeleri, IP adresi değişikliklerine karşı geliştirilmiş dayanıklılık ve ragnarok'un addressbook (adres defteri) uygulamasının paketlenmesi bulunuyor.

addressbook (adres defteri) hakkında hiç duymadıysanız veya onu kullanmadıysanız, kısacası, bazı anonim olarak barındırılan konumlardan (varsayılan olarak http://dev.i2p/i2p/hosts.txt ve http://duck.i2p/hosts.txt) belirli aralıklarla değişiklikleri alıp birleştirerek hosts.txt dosyanızı otomatik olarak güncelleyecektir. Herhangi bir dosyayı değiştirmeniz, herhangi bir yapılandırmaya dokunmanız veya ek bir uygulama çalıştırmanız gerekmeyecek - standart bir .war dosyası olarak I2P router içinde dağıtılacaktır.

Elbette, addressbook (adres defteri) ile *gerçekten* derinlemesine uğraşmak istiyorsanız bunu kesinlikle yapabilirsiniz - ayrıntılar için Ragnarok'un sitesine [2] bakın. Eğer router'ınızda addressbook zaten kuruluysa, 0.4.2.6 yükseltmesi sırasında biraz uğraşmanız gerekecek, ama tüm eski yapılandırma ayarlarınızla çalışacaktır.

[2] http://ragnarok.i2p/

* 3) 0.5

Sayılar, sayılar, sayılar! Neyse, daha önce de söylediğim gibi, 0.5 sürümü tunnel yönlendirmesinin nasıl çalıştığını baştan aşağı yenileyecek ve bu konuda ilerleme kaydediliyor. Son birkaç gündür yeni şifreleme kodunun (ve birim testlerinin) uygulamasını yapıyorum ve onlar çalışır hale gelir gelmez, yeni tunnel yönlendirmesinin nasıl işleyeceği, ne olduğu ve neden böyle işleyeceğine ilişkin mevcut düşüncelerimi anlatan bir belge yayımlayacağım. İnsanlar bunun somut olarak ne anlama geldiğini inceleyebilsin, ayrıca sorunlu alanları ve iyileştirme önerilerini bulabilsin diye şifrelemeyi daha sonra değil, şimdi onun için hayata geçiriyorum. Haftanın sonuna kadar kodu çalışır duruma getirmeyi umuyorum, bu yüzden belki bu hafta sonu daha fazla belge yayımlanır. Yine de söz vermiyorum.

* 4) jabber @ chat.i2p

jdot yeni bir jabber sunucusu kurdu ve hem bire bir sohbetler hem de grup sohbetleri için oldukça iyi çalışıyor gibi görünüyor. forum [3] üzerinde yer alan bilgilere göz atın. i2p geliştirici tartışma kanalı yine de irc #i2p olacak, ama alternatiflerin olması her zaman güzeldir.

[3] http://forum.i2p.net/viewtopic.php?t=229

* 5) ???

Tamam, şimdilik değinmem gerekenler aşağı yukarı bu kadar - ama eminim başkalarının da gündeme getirmek istediği başka birçok şey daha vardır, o yüzden 15 dk sonra @ her zamanki yerde [4] yapılacak toplantıya uğrayın ve bize neler olup bittiğini söyleyin!

=jr
