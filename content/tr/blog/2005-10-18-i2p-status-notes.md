---
title: "2005-10-18 için I2P Durum Notları"
date: 2005-10-18
author: "jr"
description: "0.6.1.3 sürümünün başarısı, Freenet ile iş birliği tartışması, tunnel bootstrap saldırılarının analizi, I2Phex yükleme hatasındaki ilerleme ve simetrik NAT ödülü hakkında haftalık güncelleme"
categories: ["status"]
---

Herkese selam, yine Salı oldu

* Index

1) 0.6.1.3 2) Freenet, I2P ve karanlık ağlar (aman tanrım) 3) Tunnel önyükleme saldırıları 4) I2Phex 5) Syndie/Sucker 6) ??? [500+ simetrik NAT ödülü]

* 1) 0.6.1.3

Geçen Cuma yeni 0.6.1.3 sürümünü yayınladık ve ağın %70’i yükseltilmiş durumdayken geri bildirimler çok olumlu. Yeni SSU iyileştirmelerinin gereksiz yeniden iletimleri azalttığı anlaşılıyor; bu da daha yüksek hızlarda daha verimli veri aktarımına olanak tanıyor ve bildiğim kadarıyla IRC proxy'si ya da Syndie iyileştirmeleriyle ilgili büyük bir sorun yaşanmadı.

Kayda değer bir nokta, Eol’un rentacoder[1]’da simetrik NAT desteği için bir ödül ilan etmiş olması; dolayısıyla umarız bu cephede biraz ilerleme kaydederiz!

[1] http://rentacoder.com/RentACoder/misc/BidRequests/ShowBidRequest.asp?lngBidRequestId=349320

* 2) Freenet, I2P, and darknets (oh my)

Nihayet 100+ mesajlık o başlığı, iki ağın nereye oturduğuna, hangi kullanım alanlarına uygun olduklarına ve hangi alanlarda daha fazla işbirliği yapabileceğimize dair daha net bir bakışla sonlandırdık. Burada hangi topolojilere veya tehdit modellerine en uygun olduklarına girmeyeceğim, ama daha fazla bilgi isterseniz posta listelerini inceleyebilirsiniz. İşbirliği cephesinde, SSU transport'u yeniden kullanmaya yönelik bazı örnek kodları toad'a gönderdim; bu kısa vadede Freenet topluluğu için faydalı olabilir ve ileride I2P'nin uygun olduğu ortamlarda Freenet kullanıcılarına premix routing (ön-karıştırma yönlendirme tekniği) sunmak için birlikte çalışabiliriz. Freenet ilerledikçe, Freenet'i bir istemci uygulaması olarak I2P üzerinde çalışır hâle de getirebiliriz; bu, onu çalıştıran kullanıcılar arasında otomatik içerik dağıtımına olanak tanır (ör. Syndie arşivleri ve gönderilerinin aktarılması), ancak önce Freenet'in planlanan yük ve içerik dağıtım sistemlerinin nasıl çalıştığını göreceğiz.

* 3) Tunnel bootstrap attacks

Michael Rogers, I2P'nin tunnel oluşturma sürecine [2][3][4] yönelik bazı ilginç yeni saldırılar hakkında iletişime geçti. Birincil saldırı (tüm önyükleme süreci boyunca başarıyla bir öncül saldırısı yürütmek) ilginç, ancak pek pratik değil - başarı olasılığı, saldırgan sayısının c, ağdaki eş sayısının n ve hedefin (ömür boyunca) inşa ettiği t adet tunnel için (c/n)^t; router h tunnel inşa ettikten sonra bir saldırganın bir tunnel içindeki tüm h sıçramayı ele geçirme olasılığından (P(success) = (c/n)^h) daha düşüktür.

Michael listeye başka bir saldırı daha gönderdi; şu anda üzerinde çalışıyoruz, dolayısıyla onu da oradan takip edebileceksiniz.

[2] http://dev.i2p.net/pipermail/i2p/2005-October/001005.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001008.html [4] http://dev.i2p.net/pipermail/i2p/2005-October/001006.html

* 4) I2Phex

Striker yükleme hatası üzerinde daha fazla ilerleme kaydediyor ve raporlara göre hatayı tam olarak tespit etmiş durumda. Umarız bu gece CVS'e girer ve kısa bir süre sonra 0.1.1.33 olarak yayımlanır. Daha fazla bilgi için forumu [5] takip edin.

[5] http://forum.i2p.net/viewforum.i2p?f=25

Söylentilere göre redzara, Phex ana dalıyla yeniden birleştirme konusunda da oldukça iyi ilerleme kaydediyor; umarız Gregor'un yardımıyla yakında her şeyi güncel hale getireceğiz!

* 5) Syndie/Sucker

dust, Sucker ile de durmaksızın çalışıyor; kod daha fazla RSS/Atom verisini Syndie'ye aktarıyor. Belki Sucker ve post CLI'yi Syndie'ye daha ileri düzeyde entegre edebiliriz; hatta farklı RSS/Atom akışlarının çeşitli bloglara içe aktarımını zamanlamak için web tabanlı bir kontrol paneli bile ekleyebiliriz. Göreceğiz...

* 6) ???

Yukarıdakilerin ötesinde daha pek çok şey var, ama bildiğim kadarıyla özeti bu. Herhangi birinin sorusu ya da endişesi varsa ya da başka konuları gündeme getirmek isterse, bu akşam saat 20:00 UTC'de #i2p kanalındaki toplantıya uğrayın!

=jr
