---
title: "2006-04-18 tarihli I2P Durum Notları"
date: 2006-04-18
author: "jr"
description: "0.6.1.16 ağ iyileştirmeleri, tunnel oluşturma kaynaklı tıkanıklık çökmesi analizi ve Feedspace geliştirme güncellemeleri"
categories: ["status"]
---

Herkese selam, haftalık durum notlarımız için salı yine geldi.

* Index

1) Ağ durumu ve 0.6.1.16 2) Tunnel oluşturma ve tıkanıklık 3) Feedspace 4) ???

* 1) Net status and 0.6.1.16

Ağın %70'inin 0.6.1.16'ya yükseltilmesiyle, önceki sürümlere göre bir iyileşme gördüğümüz anlaşılıyor ve bu sürümdeki sorunlar giderildiğinden bir sonraki darboğazımızı daha net görebiliyoruz.  Henüz 0.6.1.16'ya geçmemiş olanlar lütfen en kısa sürede yükseltin; çünkü önceki sürümler, tunnel oluşturma isteklerini keyfi olarak reddedecektir (router'ın daha fazla tunnel'e katılmak için yeterli kaynaklara sahip olması durumunda bile).

* 2) Tunnel creation and congestion

Şu anda, muhtemelen en iyi congestion collapse (tıkanıklık çökmesi) olarak tanımlanabilecek bir durum yaşıyor gibiyiz - router'lar bant genişliği açısından kısıtlı olduğundan tunnel oluşturma istekleri reddediliyor, bu yüzden yedek kaynakları olan başka router'lar bulma umuduyla daha fazla tunnel oluşturma isteği gönderiliyor, bu da yalnızca kullanılan bant genişliğini artırıyor.  Bu sorun, 0.6.1.10 sürümünde yeni tunnel oluşturma kriptografisine geçtiğimizden beri mevcut ve büyük ölçüde şu gerçeğe bağlanabilir: istek ve yanıt iki tunnel uzunluğunu kat edene kadar (daha doğrusu, *etmedikçe*) atlama başına katılma/reddetme geri bildirimi alamıyoruz.  Bu peer'lar (eşler) arasından herhangi biri mesajı iletmeyi başaramazsa, hangi peer'ın başarısız olduğunu, hangi peer'lerin kabul ettiğini ve hangilerinin bunu açıkça reddettiğini bilmiyoruz.

Zaten işlemde olan eşzamanlı tunnel oluşturma isteklerinin sayısını sınırlandırıyoruz (ve testler zaman aşımını artırmanın yardımcı olmadığını gösteriyor), dolayısıyla Nagle'ın geleneksel çözümü yeterli değil. Şu anda istek işleme kodumuzda, (açık reddetmelere karşıt olarak) isteğin sessizce düşürülmesi sıklığını azaltmak ve yük altındayken eşzamanlılığı düşürmek için istek üretim kodumuzda birkaç ince ayar deniyorum. Ayrıca, tunnel oluşturma başarı oranlarını kayda değer ölçüde artıran bazı başka iyileştirmeleri de deniyorum; ancak bunlar henüz güvenli kullanım için hazır değil.

tunnel'ın ucunda ışık var ve ilerlemeye devam ederken bizimle kalıp gösterdiğiniz sabır için minnettarım. Bu hafta içinde bazı iyileştirmeleri yayınlamak için bir başka sürüm daha çıkarmayı bekliyorum; ardından, congestion collapse (ağ tıkanıklığı çökmesi) giderilmiş mi diye görmek için ağın durumunu yeniden değerlendireceğiz.

* 3) Feedspace

Frosk, Feedspace üzerinde var gücüyle çalışıyor ve Trac sitesinde birkaç sayfayı güncelledi; yeni bir genel bakış belgesi, açık görevlerin bir listesi, bazı veritabanı ayrıntıları ve daha fazlası dahil. En son değişiklikleri yakalamak için http://feedspace.i2p/ adresine uğrayın ve fırsatınız olur olmaz Frosk’u soru yağmuruna tutun :)

* 4) ???

Şimdilik konuşmaya hazır olduğum konular kabaca bu kadar, ama bu akşam ilerleyen saatlerde (20:00 UTC) yapılacak toplantımız için lütfen #i2p'ye uğrayın; biraz daha sohbet edelim!

=jr
