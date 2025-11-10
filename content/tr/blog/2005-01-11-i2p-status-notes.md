---
title: "2005-01-11 tarihli I2P Durum Notları"
date: 2005-01-11
author: "jr"
description: "Weekly I2P development status notes covering network status, 0.5 progress, 0.6 status, azneti2p, FreeBSD port, and hosts.txt as Web of Trust"
categories: ["status"]
---

Selam millet, haftalık güncelleme zamanı

* Index

1) Ağ durumu 2) 0.5 ilerlemesi 3) 0.6 durumu 4) azneti2p 5) fbsd 6) hosts.txt WoT olarak 7) ???

* 1) Net status

Genel olarak ağ iyi gidiyor, yine de irc sunucularından birinin çevrimdışı olması ve outproxy'min aksaması nedeniyle bazı sorunlar yaşadık. Ancak diğer irc sunucusu erişilebilir durumdaydı (ve hâlâ öyle) (gerçi şu anda CTCP devre dışı değil - bkz. [1]), bu yüzden irc ihtiyacımızı giderebildik :)

[1] http://ugha.i2p/HowTo/IrcAnonymityGuide

* 2) 0.5 progress

İlerleme var, durmadan ileri!  Tamam, sanırım bundan biraz daha ayrıntıya girmeliyim.  Yeni tunnel yönlendirme şifrelemesini sonunda uyguladım ve test ettim (yaşasın!), ancak bazı tartışmalar sırasında bir düzeyde anonimlik sızıntısı olabilecek bir yer bulduk, bu yüzden gözden geçiriliyor (ilk atlama düğümü ilk atlama olduğunu bilecekti, bu da Kötü.  ama düzeltmesi gerçekten çok çok kolay).  Her neyse, bununla ilgili belgeleri ve kodu yakında güncelleyip yayımlamayı umuyorum ve 0.5 tunnel işleyişi / havuzlama / vb. ile ilgili diğer belgeleri de daha sonra yayımlayacağım.  Daha fazla haber oldukça duyuracağım.

* 3) 0.6 status

(ne!?)

Mule, UDP aktarımı üzerine araştırmalara başladı ve zab’ın LimeWire’ın UDP koduyla ilgili deneyimlerinden faydalanıyoruz. Her şey çok umut verici, ancak yapılacak çok iş var (ve yol haritasında [2] hâlâ birkaç ay ileride). İlhamınız veya önerileriniz mi var? Dahil olun ve çabayı yapılması gerekenlere odaklamaya yardımcı olun!

[2] http://www.i2p.net/roadmap#0.6

* 4) azneti2p

Haberi aldığımda heyecandan neredeyse altıma kaçırıyordum, ama görünen o ki Azureus ekibindeki arkadaşlar hem anonim tracker (izleyici) kullanımı hem de anonim veri iletişimine izin veren bir I2P eklentisi yazmış! Birden fazla torrent, tek bir I2P destination (I2P hedefi) içinde de çalışıyor ve doğrudan I2PSocket kullanıyor; bu da streaming lib (akış kütüphanesi) ile sıkı entegrasyona olanak tanıyor. azneti2p eklentisi bu 0.1 sürümüyle hâlâ erken aşamada ve yolda bir sürü optimizasyon ile kullanım kolaylığı iyileştirmesi var, ama ellerinizi kirletmeye hazırsanız i2p IRC ağlarında i2p-bt kanalına uğrayın ve eğlenceye katılın :)

Macera meraklıları için, en son azureus [3] sürümünü edinin, onların i2p howto (nasıl yapılır kılavuzu) [4]'ya göz atın ve eklenti [5]'yi kapın.

[3] http://azureus.sourceforge.net/index_CVS.php [4] http://azureus.sourceforge.net/doc/AnonBT/i2p/I2P_howto.htm [5] http://azureus.sourceforge.net/plugin_details.php?plugin=azneti2p

duck, i2p-bt ile uyumluluğu korumak için olağanüstü çabalar gösteriyor ve ben bunu yazarken #i2p-bt’de hummalı biçimde kod yazılıyor; bu yüzden çok yakında yeni bir i2p-bt sürümü için gözünüzü açık tutun.

* 5) fbsd

lioux’un çalışması sayesinde artık i2p için bir FreeBSD ports kaydı var [6]. Aslında ortalıkta çok sayıda dağıtıma özgü kurulum olmasını pek istemesek de, yeni sürüm için yeterli bildirim yaptığımızda bunu güncel tutacağına söz veriyor. Bu, fbsd-current kullanıcıları için yararlı olmalı - teşekkürler lioux!

[6] http://www.freshports.org/net/i2p/

* 6) hosts.txt as WoT

Artık 0.4.2.6 sürümü Ragnarok'un adres defterini paketle birlikte sunduğuna göre, hosts.txt dosyanızı yeni girdilerle doldurmayı sürdürme süreci her kullanıcının kendi kontrolündedir. Üstelik, adres defteri aboneliklerini basit bir güven ağı olarak görebilirsiniz; sizi yeni destinations (I2P'de hizmet/uç nokta kimlikleri) ile tanıştırması için güvendiğiniz bir siteden yeni girdileri içe aktarırsınız (varsayılanlar dev.i2p ve duck.i2p'dir).

Bu olanakla birlikte tamamen yeni bir boyut geliyor - insanların kendi hosts.txt dosyalarında hangi sitelere fiilen bağlantı vereceklerini ve hangilerine vermeyeceklerini seçebilme yeteneği. Geçmişte yaşanan herkese açık serbest ortama hâlâ bir yer olsa da, artık adlandırma sistemi sadece teoride değil pratikte de tamamen dağıtık olduğuna göre, insanlar başkalarına ait destinations (hedefler) yayımlama konusunda kendi politikalarını belirlemek zorunda kalacaklar.

Burada perde arkasındaki önemli nokta, bunun I2P topluluğu için bir öğrenme fırsatı olmasıdır. Önceden, hem gott hem de ben, gott'un sitesini jrandom.i2p olarak yayımlayarak adlandırma meselesini ileriye taşımaya çalışıyorduk (o bu siteyi önce kendisi talep etti - ben istemedim ve o URL'nin içeriği üzerinde hiçbir şekilde kontrolüm yok). Şimdi, http://dev.i2p.net/i2p/hosts.txt veya forum.i2p üzerinde listelenmeyen sitelerle nasıl başa çıkacağımızı araştırmaya başlayabiliriz. Bu konumlarda yer almaması bir sitenin çalışmasını hiçbir şekilde engellemez - hosts.txt dosyanız sadece yerel adres defterinizdir.

Neyse, yeter bu gevezelik, sadece herkesi haberdar etmek istedim ki hepimiz ne yapılması gerektiğini görebilelim.

* 7) ???

Vay canına, ne kadar çok şey var. Yoğun bir haftaydı ve yakın zamanda işlerin yavaşlayacağını öngörmüyorum. O halde, birkaç dakika içinde toplantıya uğra, konuları konuşabiliriz.

=jr
