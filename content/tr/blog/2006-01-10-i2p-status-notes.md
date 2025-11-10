---
title: "2006-01-10 için I2P Durum Notları"
date: 2006-01-10
author: "jr"
description: "Veri aktarım hızı profilleme algoritmalarını, Syndie blog görünümündeki iyileştirmeleri, HTTP kalıcı bağlantılarındaki ilerlemeyi ve I2Phex gwebcache geliştirmesini kapsayan haftalık güncelleme"
categories: ["status"]
---

Selam millet, görünüşe göre salı yine geldi çattı.

* Index

1) Ağ durumu 2) Aktarım hızı profillemesi 3) Syndie blogları 4) HTTP kalıcı bağlantıları 5) I2Phex gwebcache 6) ???

* 1) Net status

Geçen hafta, CVS’de devam eden çok sayıda hata düzeltmesi ve iyileştirme oldu; mevcut derleme 0.6.1.8-11 sürümünde. Ağ oldukça istikrarlıydı, ancak farklı i2p hizmet sağlayıcılarındaki bazı kesintiler ara sıra aksamaya yol açtı. Nihayet CVS’deki gereksiz derecede yüksek router kimliği değişiminden kurtulduk ve zzz’in dün bulduğu çekirdeğe yönelik yeni bir hata düzeltmesi var; oldukça umut verici görünüyor, ancak bunun etkilerini görmek için beklememiz gerekecek. Geçen hafta olan iki büyük gelişme de yeni throughput (aktarım verimi) tabanlı hız profillemesi ve Syndie’nin blog görünümü üzerinde yapılan önemli çalışmalardı. 0.6.1.9’u ne zaman göreceğimize gelince, bu haftanın ilerleyen günlerinde, en geç hafta sonuna kadar çıkmalı. Gelişmeleri her zamanki kanallardan takip edin.

* 2) Throughput profiling

Veri aktarım hızını izlemek için birkaç yeni eş profilleme algoritmasını test ettik, ancak son bir hafta kadar süredir oldukça iyi görünen bir tanesinde karar kılmış gibiyiz. Temelde, her bir tunnel için 1 dakikalık dönemler boyunca doğrulanmış aktarım hızını izler ve buna göre eşler için aktarım hızı tahminlerini ayarlar. Bir eş için ortalama bir hız hesaplamaya çalışmaz; çünkü bunu yapmak oldukça karmaşıktır; zira tunnels birden fazla eş içerir ve doğrulanmış aktarım hızı ölçümleri de çoğu zaman birden fazla tunnel gerektirir. Bunun yerine, ortalama bir tepe hızı hesaplar - özellikle de eşe ait tunnels ile elde edilebilen en yüksek üç aktarım hızını ölçer ve bunların ortalamasını alır.

Özetle, bu oranlar, tam bir dakika boyunca ölçüldüklerinden, bir eşin (peer) sağlayabildiği sürdürülebilir hızlardır ve her bir eş en azından uçtan uca ölçülen hız kadar hızlı olduğundan, her birini o kadar hızlı olarak işaretlemek güvenlidir. Bunun başka bir varyasyonunu da denemiştik - bir eşin farklı zaman aralıklarında tunnels üzerinden genel throughput’unu (aktarım oranını) ölçmek; bu, tepe hız bilgilerini daha da net sundu, ancak hâlihazırda "fast" olarak işaretlenmemiş eşler aleyhine ciddi biçimde ağırlık koydu; çünkü "fast" olanlar çok daha sık kullanılıyor (istemci tunnels yalnızca fast eşleri kullanır). Bu genel throughput ölçümünün sonucu, yeterince yük altına alınanlar için harika veriler toplamasıydı; ancak yalnızca fast eşler yeterince yük altına alınmıştı ve etkili keşif çok azdı.

Bununla birlikte, 1 dakikalık periyotlar ve tek bir tunnel'ın aktarım hızını kullanmak daha makul değerler sağlıyor gibi görünüyor. Bu algoritmanın bir sonraki sürümde devreye alındığını göreceğiz.

* 3) Syndie blogs

Bazı geri bildirimlere dayanarak, syndie içindeki blog görünümünde daha fazla iyileştirme yapıldı; bu da ona, haber grubu/foruma benzer zincirli (threaded) görünümden belirgin biçimde farklı bir hava kazandırdı. Buna ek olarak, mevcut Syndie mimarisi aracılığıyla genel blog bilgilerini tanımlamak için bütünüyle yeni bir yetenek kazandı. Örnek için, varsayılan "about Syndie" blog yazısına göz atın:  http://syndiemedia.i2p.net/blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1132012800001

Bu, yapabileceklerimizin ancak başlangıcına değiniyor. Bir sonraki sürüm, kendi blogunuzun logosunu, kendi bağlantılarınızı (bloglara, gönderilere, eklere, keyfi harici URL'lere) tanımlamanıza ve umarız daha da fazla özelleştirme yapmanıza olanak tanıyacak. Böyle bir özelleştirme de etiket başına simgeler - standart etiketlerle kullanılmak üzere bir dizi varsayılan simgeyi birlikte sunmak isterim, ancak insanlar, kendi bloglarında kullanmak üzere kendi etiketleri için simgeler tanımlayabilecek ve hatta standart etiketler için varsayılan simgeleri geçersiz kılabilecekler (yine, elbette yalnızca insanlar kendi bloglarını görüntülerken). Belki farklı etiketlere sahip gönderileri farklı şekilde göstermek için bazı stil yapılandırmaları bile olur (elbette yalnızca çok belirli stil özelleştirmelerine izin verilecek - Syndie ile keyfi CSS istismarları yok, çok teşekkürler :)

Blog görünümüyle yapmak istediğim daha çok şey var ve bunlar bir sonraki sürümde yer almayacak, ama yine de insanların bazı özellikleriyle denemeler yapmaya başlaması için iyi bir itici güç olacaktır; umarım bu da hepinizin bana *sizin* neye ihtiyaç duyduğunuzu, benim sizin ne istediğinizi düşündüğüm şey yerine, göstermenize olanak tanır. İyi bir kodlayıcı olabilirim, ama kötü bir kâhinim.

* 4) HTTP persistent connections

zzz tam bir manyak, size söylüyorum. Uzun zamandır istenen bir özellikte biraz ilerleme var - tek bir akış üzerinden birden fazla HTTP isteği göndermenize ve karşılığında birden fazla yanıt almanıza olanak tanıyan kalıcı HTTP bağlantıları desteği. Sanırım biri bunu ilk kez iki yıl kadar önce istemişti ve bazı eepsite(I2P Site) türleri ya da outproxy (I2P çıkış proxy'si) kullanımı için epey yardımcı olabilir. İşin henüz bitmediğini biliyorum, ama ilerliyor. Umarım zzz toplantı sırasında bize bir durum güncellemesi verebilir.

* 5) I2Phex gwebcache

I2Phex'e gwebcache desteğini geri getirme konusunda ilerleme olduğuna dair raporlar duydum, ancak şu anda durumun ne aşamada olduğunu bilmiyorum. Belki Complication bu konuda bu akşam bize bir güncelleme verebilir?

* 6) ???

Gördüğünüz gibi, epey şey oluyor, ama gündeme getirip tartışmak istediğiniz başka konular varsa, birkaç dakika içinde toplantıya uğrayın ve ses verin. Bu arada, son zamanlarda takip ettiğim hoş sitelerden biri http://freedomarchive.i2p/ oldu (I2P kurulu olmayan üşengeçler için, Tino'nun inproxy'sini http://freedomarchive.i2p.tin0.de/ üzerinden kullanabilirsiniz). Her neyse, birkaç dakika içinde görüşürüz.

=jr
