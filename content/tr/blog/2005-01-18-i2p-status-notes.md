---
title: "2005-01-18 tarihli I2P Durum Notları"
date: 2005-01-18
author: "jr"
description: "Ağ durumu, 0.5 tunnel yönlendirme tasarımı, i2pmail.v2 ve azneti2p_0.2 güvenlik düzeltmesini kapsayan haftalık I2P geliştirme durum notları"
categories: ["status"]
---

Herkese selam, haftalık güncelleme zamanı

* Index

1) Ağ durumu 2) 0.5 3) i2pmail.v2 4) azneti2p_0.2 5) ???

* 1) Net status

Hmm, burada rapor edilecek pek bir şey yok - işler geçen hafta olduğu gibi çalışıyor, ağın boyutu hâlâ oldukça benzer, belki biraz daha büyük. Bazı güzel yeni siteler ortaya çıkıyor - ayrıntılar için forum [1] ve orion [2]'a bakın.

[1] http://forum.i2p.net/viewforum.php?f=16 [2] http://orion.i2p/

* 2) 0.5

postman, dox, frosk ve cervantes'in yardımı sayesinde (ve veriyi router'ları üzerinden tunnel eden herkes ;), bir tam günlük mesaj boyutu istatistikleri [3] topladık. Orada iki istatistik seti var - yakınlaştırmanın yüksekliği ve genişliği. Bu, farklı mesaj dolgulama stratejilerinin ağ yükü üzerindeki etkisini inceleme isteğiyle yapıldı; 0.5 tunnel yönlendirmesine yönelik taslaklardan birinde açıklandığı üzere [4]. (ooOOoo güzel resimler).

O verileri didik didik ederken bulduklarımın ürkütücü yanı şuydu: oldukça basit, elle ayarlanmış padding breakpoints (doldurma için eşik noktaları) kullanıldığında, o sabit boyutlara padding uygulamak bile bant genişliğinin %25’inden fazlasının israf olmasına yol açıyordu. Evet, biliyorum, bunu yapmayacağız. Belki siz o ham veriyi didik didik ederek daha iyi bir şey bulabilirsiniz.

[3] http://dev.i2p.net/~jrandom/messageSizes/ [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                  tunnel.html?rev=HEAD#tunnel.padding

Aslında, o [4] bağlantısı bizi tunnel yönlendirmesi için 0.5 planlarının durumuna götürüyor. Connelly’nin [5] yazdığı gibi, son zamanlarda bazı taslaklar hakkında IRC’de çokça tartışma oldu; polecat, bla, duck, nickster, detonate ve diğerleri öneriler ve sorgulayıcı sorularla katkıda bulundu (tamam, bir de iğnelemeler ;). Bir haftadan biraz fazla bir sürenin ardından, [4] ile ilgili, bir şekilde gelen tunnel geçidini ele geçirebilen ve ayrıca o tunnelin ilerleyen kısmındaki diğer eşlerden birini de kontrol eden bir saldırganı konu alan olası bir güvenlik açığına rastladık. Her ne kadar çoğu durumda bu tek başına uç noktayı açığa çıkarmasa ve ağ büyüdükçe olasılıksal olarak gerçekleştirilmesi zorlaşsa da, yine de Berbat (tm).

İşte [6] devreye giriyor. Bu, o sorunu ortadan kaldırır, her uzunlukta tunnel kullanmamıza olanak tanır ve dünya açlığını da çözer [7]. Ancak bir saldırganın tunnel içinde döngüler oluşturabileceği başka bir sorunu da ortaya çıkarır; Taral'ın geçen yıl ElGamal/AES üzerinde kullanılan session tags (oturum etiketleri) ile ilgili yaptığı bir öneriye [8] dayanarak, senkronize sözde rastgele sayı üreteçleri [9] serisi kullanarak verilen zararı en aza indirebiliriz.

[5] http://dev.i2p.net/pipermail/i2p/2005-January/000557.html [6] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                             tunnel-alt.html?rev=HEAD [7] Hangi ifadenin yanlış olduğunu tahmin edin? [8] http://www.i2p.net/todo#sessionTag [9] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                 tunnel-alt.html?rev=HEAD#tunnel.prng

Yukarıdakiler kulağa kafa karıştırıcı geliyorsa endişelenmeyin - burada bazı çetrefilli tasarım sorunlarının iç yüzünün açıkça masaya yatırıldığını görüyorsunuz. Eğer yukarıdakiler *kafa karıştırıcı gelmiyorsa*, lütfen bizimle iletişime geçin, çünkü bu konuları birlikte masaya yatırmak için her zaman daha fazla kafa arıyoruz :)

Her neyse, listede [10] belirttiğim gibi, sırada kalan ayrıntıları netleştirmek için ikinci stratejiyi [6] hayata geçirmek istiyorum.  0.5 için plan şu anda geriye dönük uyumlu olmayan tüm değişiklikleri - yeni tunnel şifrelemesi vb. - bir araya getirip bunu 0.5.0 olarak yayınlamak; ardından bu ağda oturdukça, önerilerde anlatıldığı gibi havuzlama stratejisini ayarlamak gibi 0.5'in [11] diğer bölümlerine geçip bunu da 0.5.1 olarak yayınlamak.  Ay sonuna kadar 0.5.0'ı yetiştirebileceğimizi umuyorum, ama göreceğiz.

[10] http://dev.i2p.net/pipermail/i2p/2005-January/000558.html [11] http://www.i2p.net/roadmap#0.5

* 3) i2pmail.v2

Geçen gün postman, gelecek nesil e-posta altyapısı için bir taslak eylem planı yayınladı [12] ve bu cidden harika görünüyor.  Elbette hayal edebileceğimiz daha nice süsler püsler vardır, ama pek çok açıdan oldukça iyi bir mimariye sahip.  Şu ana kadar belgelenenlere göz atın [13] ve görüşlerinizle postman ile iletişime geçin!

[12] http://forum.i2p.net/viewtopic.php?t=259 [13] http://www.postman.i2p/mailv2.html

* 4) azneti2p_0.2

Listeye yazdığım gibi [14], azureus için orijinal azneti2p eklentisinde ciddi bir anonimlik hatası vardı.  Sorun şuydu: bazı kullanıcıların anonim, bazılarının anonim olmadığı karma torrentlerde, anonim kullanıcılar I2P üzerinden değil, anonim olmayan kullanıcılarla /doğrudan/ bağlantı kuruyorlardı.  Paul Gardner ve diğer azureus geliştiricileri oldukça hızlı davrandı ve hemen bir yama yayınladılar.  Gördüğüm sorun artık azureus v. 2203-b12 + azneti2p_0.2 sürümünde mevcut değil.

Yine de, olası anonimlik sorunlarını gözden geçirmek için kodu baştan sona inceleyip denetlemedik, bu yüzden "kendi riskinizde kullanın" (Öte yandan, 1.0 sürümü çıkana kadar I2P için de aynısını söylüyoruz). Eğer buna hazırsanız, Azureus geliştiricilerinin eklentiyle ilgili daha fazla geri bildirim ve hata raporunu memnuniyetle karşılayacaklarını biliyorum. Elbette, başka sorunlar hakkında bir şey öğrenirsek insanları bilgilendirmeye devam edeceğiz.

[14] http://dev.i2p.net/pipermail/i2p/2005-January/000553.html

* 5) ???

Gördüğünüz gibi, epey şey oluyor. Sanırım gündeme getirebileceklerim aşağı yukarı bu kadar, ama konuşmak istediğiniz başka bir şey varsa (ya da yukarıdaki konular hakkında sadece biraz dert yanmak istiyorsanız) lütfen 40 dakika sonra yapılacak toplantıya uğrayın.

=jr
