---
title: "2005-03-22 tarihli I2P Durum Notları"
date: 2005-03-22
author: "jr"
description: "0.5.0.3 sürümü, tunnel mesaj toplulaştırma uygulaması ve otomatik güncelleme araçlarını kapsayan haftalık I2P geliştirme durum notları"
categories: ["status"]
---

Selam millet, kısa bir durum güncellemesi

* Index

1) 0.5.0.3 2) toplu işleme 3) güncelleme 4) ???

* 0.5.0.3

Yeni sürüm yayımlandı ve çoğunuz oldukça hızlı bir şekilde yükselttiniz — teşekkürler! Çeşitli sorunlara yönelik bazı hata düzeltmeleri vardı, ancak devrim niteliğinde bir şey yoktu — en büyük kısım 0.5 ve 0.5.0.1 kullanıcılarını ağın dışına bırakmaktı. O zamandan beri ağın davranışını izliyor, neler olup bittiğini inceliyorum ve bir miktar iyileşme olmuş olsa da hâlâ yoluna konması gereken bazı şeyler var.

Bir ya da iki gün içinde, henüz kimsenin karşılaşmadığı ancak yeni toplu işleme kodunu bozan bir sorun için bir hata düzeltmesi içeren yeni bir sürüm yayınlanacak. Ayrıca, kullanıcının tercihlerine göre güncelleme sürecini otomatikleştirmeye yönelik bazı araçlar ve diğer küçük şeyler de olacak.

* batching

Blogumda belirttiğim gibi, tunnel (tünel) mesajlarını çok basit bir şekilde toplu paketleyerek ağ üzerinde gereken bant genişliğini ve mesaj sayısını önemli ölçüde azaltma imkanı var - her I2NP mesajını, boyutundan bağımsız olarak, kendine ait bir tunnel mesajına koymak yerine, kısa bir gecikme ekleyerek tek bir tunnel mesajı içinde 15 veya daha fazlasını bir araya getirebiliriz. En büyük kazanımlar, küçük mesajlar kullanan hizmetlerde (örneğin IRC) görülecek, buna karşılık büyük dosya aktarımları bundan pek etkilenmeyecek. Toplu paketlemeyi gerçekleştiren kod uygulanıp test edildi, ancak ne yazık ki canlı ağda, bir tunnel mesajı içindeki ilk I2NP mesajı dışındakilerin tümünün kaybolmasına yol açan bir hata var. Bu yüzden, ilgili düzeltmeyi içeren bir ara sürüm yayınlayacağız; bunu da yaklaşık bir hafta sonra toplu paketleme sürümü izleyecek.

* updating

Bu ara sürümde, sıkça tartışılan 'autoupdate' (otomatik güncelleme) kodunun bir kısmını sunacağız. Gerçek güncelleme duyurularını periyodik olarak kontrol etmek, güncellemeyi anonim olarak ya da anonim olmadan indirmek ve ardından onu ya yüklemek ya da yalnızca yüklemeye hazır olduğunu belirten bir bildirimi router konsolunda göstermek için araçlara sahibiz. Güncellemenin kendisi artık smeghead'in yeni imzalı güncelleme biçimini kullanacak; bu, özünde güncelleme artı bir DSA imzasıdır. Bu imzayı doğrulamak için kullanılan anahtarlar I2P ile birlikte paketlenecek ve ayrıca router konsolundan yapılandırılabilir olacaktır.

Varsayılan davranış, sadece periyodik olarak güncelleme duyurularını kontrol etmek olacak, ancak bunlara göre işlem yapmayacak - sadece router konsolunda tek tıklamayla "Şimdi güncelle" özelliğini gösterecek.  Farklı kullanıcı ihtiyaçları için başka birçok senaryo da olacak, ancak umarız bunların hepsi yeni bir yapılandırma sayfası aracılığıyla karşılanacak.

* ???

Kendimi pek iyi hissetmiyorum, bu yüzden yukarıda yazılanlar neler olup bittiğine dair tüm ayrıntılara pek girmiyor. Toplantıya uğrayın da eksikleri tamamlayın :)

Bu arada, bir iki gün içinde kendim için yeni bir PGP anahtarı da yayımlayacağım (çünkü mevcut olanın süresi yakında doluyor...), o yüzden takipte kalın.

=jr
