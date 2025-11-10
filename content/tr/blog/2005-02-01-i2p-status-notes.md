---
title: "2005-02-01 tarihli I2P Durum Notları"
date: 2005-02-01
author: "jr"
description: "0.5 tunnel şifrelemesindeki ilerleme, yeni NNTP sunucusu ve teknik önerileri kapsayan haftalık I2P geliştirme durum notları"
categories: ["status"]
---

Herkese merhaba, haftalık durum zamanı

* Index

1) 0.5 durumu 2) nntp 3) teknik öneriler 4) ???

* 1) 0.5 status

0.5 cephesinde çokça ilerleme kaydedildi; dün büyük bir commit serisi girdi.  Router'ın büyük kısmı artık yeni tunnel şifrelemesi ve tunnel pooling (tunnel'ların havuzlanması) [1] kullanıyor ve test ağında iyi çalışıyor.  Entegrasyonu yapılması gereken bazı kilit parçalar hâlâ var ve kodun geriye dönük uyumlu olmadığı da açık, ancak önümüzdeki hafta bir ara daha geniş ölçekli bir dağıtım yapabileceğimizi umuyorum.

Daha önce belirtildiği gibi, ilk 0.5 sürümü, farklı tunnel eş seçimi/sıralaması stratejilerinin çalışmasına olanak tanıyacak temeli sağlayacaktır. Öncelikle keşif ve istemci havuzları için temel bir dizi yapılandırılabilir parametreyle başlayacağız, ancak ilerideki sürümler muhtemelen farklı kullanıcı profilleri için başka seçenekler de içerecektir.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) nntp

LazyGuy'un sitesinde [2] ve blogumda [3] belirtildiği gibi, ağda yeni bir NNTP sunucumuz çalışır durumda ve nntp.fr.i2p adresinden erişilebilir. LazyGuy, gmane'den birkaç listeyi almak için bazı suck [4] betiklerini çalıştırmış olsa da, içerik büyük ölçüde I2P kullanıcılarına ait, onlar için ve onlar tarafından. jdot, LazyGuy ve ben hangi haber okuyucularının güvenle kullanılabileceğine dair biraz araştırma yaptık ve oldukça kolay çözümler olduğu görülüyor. Anonim haber okuma ve gönderme için slrn [5] çalıştırma talimatları için bloguma bakın.

[2] http://fr.i2p/ [3] http://jrandom.dev.i2p/ [4] http://freshmeat.net/projects/suck/ [5] http://freshmeat.net/projects/slrn/

* 3) tech proposals

Orion ve diğerleri, daha zor istemci ve uygulama düzeyi sorunlarını ayrıntılandırmaya yardımcı olmak için çeşitli teknik konulara ilişkin bir dizi RFC’yi ugha’nın wiki’sinde [6] yayınladılar. Lütfen adlandırma konularını, SAM ile ilgili güncellemeleri, swarming fikirlerini (eşzamanlı çoklu eşten veri paylaşımı) ve benzerlerini tartışmak için orayı bir yer olarak kullanın - oraya yazdığınızda, daha iyi bir sonuç elde etmek için hepimiz kendi alanımızda birlikte çalışabiliriz.

[6] http://ugha.i2p/I2pRfc

* 4) ???

Şimdilik anlatacaklarım bu kadar (bu da iyi, çünkü toplantı birazdan başlıyor).  Her zamanki gibi, düşüncelerinizi istediğiniz zaman ve yerde paylaşın :)

=jr
