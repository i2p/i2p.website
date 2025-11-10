---
title: "2005-06-28 için I2P Durum Notları"
date: 2005-06-28
author: "jr"
description: "SSU transport dağıtım planlarını, birim testi ödülünün tamamlanması ve lisanslama hususlarını, ayrıca Kaffe Java'nın durumunu kapsayan haftalık güncelleme"
categories: ["status"]
---

Herkese selam, yine haftalık güncelleme zamanı

* Index

1) SSU durumu 2) Birim testi durumu 3) Kaffe durumu 4) ???

* 1) SSU status

SSU taşıma katmanında biraz daha ilerleme kaydedildi ve şu anki düşüncem, biraz daha canlı ağ testi yaptıktan sonra fazla bir gecikme olmadan 0.6 olarak yayımlayabileceğimiz yönünde. İlk SSU sürümü, güvenlik duvarında bir port açamayan ya da NAT ayarlarını düzenleyemeyenler için destek içermeyecek, ancak bu destek 0.6.1’de sunulacak. 0.6.1 yayımlandıktan, test edildikten ve çok iyi çalışır hâle geldikten sonra (diğer adıyla 0.6.1.42), 1.0’a geçeceğiz.

Benim kişisel eğilimim, SSU transport yaygınlaştıkça insanların her ikisini birden etkinleştirmesine (hem TCP hem de UDP portlarını yönlendirmelerine) gerek kalmaması ve geliştiricilerin gereksiz kodun bakımını yapmak zorunda kalmaması için TCP transport’u tamamen bırakmak yönünde. Bu konuda güçlü görüşleri olan var mı?

* 2) Unit test status

Geçen hafta belirtildiği gibi, Comwiz birim testi ödülünün ilk aşamasını talep etmek üzere ortaya çıktı (yaşasın Comwiz! ödülü finanse ettikleri için duck & zab’a da teşekkürler!). Kod CVS'e gönderildi ve yerel kurulumunuza bağlı olarak, i2p/core/java dizinine gidip "ant test junit.report" komutunu çalıştırarak (yaklaşık bir saat bekleyin...) junit ve clover raporlarını üretebilir ve i2p/reports/core/html/junit/index.html dosyasını görüntüleyebilirsiniz. Öte yandan, "ant useclover test junit.report clover.report" komutunu çalıştırıp i2p/reports/core/html/clover/index.html dosyasını görüntüleyebilirsiniz.

Her iki test kümesinin de dezavantajı, yönetici sınıfın “telif hakkı yasası” dediği o aptalca kavramla ilgilidir. Clover ticari bir üründür, ancak cenqua’daki arkadaşlar açık kaynak geliştiricilerinin ücretsiz kullanımına izin veriyor (ve nazikçe bize bir lisans vermeyi de kabul ettiler). Clover raporlarını oluşturmak için, Clover’ın yerel olarak kurulu olması gerekir — benim sistemimde clover.jar ~/.ant/lib/ içinde, lisans dosyamın yanında. Çoğu kişinin Clover’a ihtiyacı olmayacak ve raporları web’de yayımlayacağımız için onu kurmamanız herhangi bir işlev kaybına yol açmayacaktır.

Öte yandan, birim test çerçevesinin kendisini dikkate aldığımızda - junit, IBM Common Public License 1.0 altında yayımlanmıştır ki FSF’ye [1] göre GPL ile uyumlu değildir. Şimdi, bizim tarafımızda GPL lisanslı herhangi bir kod yok (en azından çekirdekte veya router’da yok), ancak lisans politikamıza [2] dönüp baktığımızda, nasıl lisansladığımıza ilişkin ayrıntılardaki amacımız, ortaya konanların mümkün olduğunca çok kişi tarafından kullanılabilmesini sağlamaktır; çünkü anonimlik kalabalıkla güçlenir.

[1] http://www.fsf.org/licensing/licenses/index_html#GPLIncompatibleLicenses [2] http://www.i2p.net/licenses

Bazı insanlar anlaşılmaz biçimde yazılımları GPL altında yayımladıkları için, onların I2P’yi herhangi bir kısıtlama olmadan kullanabilmelerini sağlamaya çalışmamız mantıklı. En azından bu, sunduğumuz asıl işlevselliğin CPL lisanslı koda (ör. junit.framework.*) bağımlı olmasına izin veremeyeceğimiz anlamına geliyor. Bunu birim testlerini de kapsayacak şekilde genişletmek isterdim, ancak junit test çatılarının ortak dili gibi görünüyor (ve sahip olduğumuz kaynaklar düşünüldüğünde, “hey, hadi kendi kamu malı (public domain) birim test çatımızı geliştirelim!” demenin pek de aklı başında olacağını sanmıyorum).

Tüm bunları göz önünde bulundurarak, düşündüğüm şu: junit.jar'ı CVS deposuna dahil edeceğiz ve insanlar birim testlerini çalıştırdıklarında bunu kullanacağız, ancak birim testlerinin kendileri i2p.jar veya router.jar içine derlenmeyecek ve sürümlerde dağıtılmayacak. Gerekirse ek bir jar kümesi (i2p-test.jar ve router-test.jar) sunabiliriz, fakat bunlar junit'e bağımlı olduklarından GPL lisanslı uygulamalar tarafından kullanılamaz.

=jr
