---
title: "2005-06-21 tarihli I2P Durum Notları"
date: 2005-06-21
author: "jr"
description: "Geliştiricinin seyahatten dönüşü, SSU transport ilerlemesi, birim testi ödülünün tamamlanması ve hizmet kesintisini kapsayan haftalık güncelleme"
categories: ["status"]
---

Herkese selam, haftalık durum notlarımıza yeniden başlama zamanı.

* Index

1) Geliştir[ici] durumu 2) Geliştir[me] durumu 3) Birim test ödülü 4) Hizmet kesintisi 5) ???

* 1) Dev[eloper] status

Dört ülkede dört şehrin ardından, nihayet yerleşiyorum ve yeniden kod yazmaya hız veriyorum. Geçen hafta bir dizüstü bilgisayarın eksik kalan son parçalarını da bir araya getirdim, artık kanepeden kanepiye dolaşmıyorum ve evde internet erişimim olmasa da, etrafta bolca internet kafe var, bu yüzden erişim güvenilir (sadece aralıklı ve pahalı).

Son söylediğim, en azından sonbahara kadar irc'de eskisi kadar takılmayacağım anlamına geliyor (Ağustos civarına kadar geçici kiralık bir yerim var ve 7/24 internet erişimi sağlayabileceğim bir yer arıyor olacağım). Bu, yine de daha az iş yapacağım anlamına gelmiyor - sadece ağırlıklı olarak kendi test ağımda çalışıp canlı ağda test için yapılar yayımlayacağım (ve, şey, ah evet, sürümler). Ancak bu, #i2p içinde serbest biçimde yürüyen bazı tartışmaları listeye [1] ve/veya foruma [2] taşımak isteyebileceğimiz anlamına geliyor (yine de #i2p geçmişini okumaya devam ediyorum). Geliştirme toplantılarımızı yapmak için gidebileceğim makul bir yer henüz bulamadım, bu yüzden bu hafta orada olmayacağım, ama belki gelecek haftaya kadar bir tane bulmuş olurum.

Neyse, benim hakkımda bu kadar.

[1] http://dev.i2p.net/pipermail/i2p/ [2] http://forum.i2p.net/

* 2) Dev[elopment] status

Taşınırken üzerinde çalıştığım iki ana alan vardı - dokümantasyon ve SSU transport (ikincisi yalnızca dizüstü bilgisayarı aldıktan sonra). Belgeler hâlâ yapım aşamasında; kocaman, göz korkutucu bir genel bakışın yanı sıra, kaynak düzeni, bileşen etkileşimi vb. konuları kapsayan daha küçük uygulama belgelerinden oluşan bir seri de var.

SSU ilerlemesi iyi gidiyor - yeni ACK bit alanları devrede, iletişim (simüle edilmiş) kayıpla etkili biçimde başa çıkıyor, hızlar çeşitli koşullar için uygun ve daha önce karşılaştığım daha kötü hataların bir kısmını giderdim. Yine de bu değişiklikleri test etmeye devam ediyorum ve uygun olduğunda, yardım etmeleri için bazı gönüllülere ihtiyaç duyacağımız bir dizi canlı ağ testi planlayacağız. Bu cephede daha fazla haber mevcut olduğunda gelecek.

* 3) Unit test bounty

Memnuniyetle duyuruyorum ki Comwiz, birim testi ödülünün [3] birinci aşamasını talep etmek üzere bir dizi yama ile öne çıktı! Yamaların bazı küçük ayrıntıları üzerinde hâlâ çalışıyoruz, ancak güncellemeleri aldım ve gerektiği gibi hem junit hem de clover raporlarını oluşturdum. Yamaları kısa süre içinde CVS'ye alacağımızı umuyorum; o noktada Comwiz'in test belgelerini yayınlayacağız.

clover ticari bir ürün olduğundan (açık kaynak geliştiricileri için ücretsizdir [4]), yalnızca clover'ı kurmuş ve clover lisansını almış olanlar clover raporlarını oluşturabilecek. Her hâlükârda, clover raporlarını web üzerinde periyodik olarak yayımlayacağız; böylece clover kurulu olmayanlar da test paketimizin ne kadar iyi çalıştığını görebilecek.

[3] http://www.i2p.net/bounties_unittest [4] http://www.cenqua.com/clover/

* 4) Service outage

Birçoğunun muhtemelen fark ettiği gibi, (en az) outproxies (çıkış vekil sunucuları) arasından biri çevrimdışı (squid.i2p), aynı şekilde www.i2p, dev.i2p, cvs.i2p ve blogum da öyle. Bunlar birbirinden bağımsız olaylar değil - onları barındıran makine arızalandı.

=jr
