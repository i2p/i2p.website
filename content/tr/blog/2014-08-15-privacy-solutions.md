---
title: "Gizlilik Çözümleri'nin doğuşu"
date: 2014-08-15
author: "Meeh"
description: "Kuruluşun başlatılması"
categories: ["press"]
---

Herkese merhaba!

Bugün, I2P yazılımını geliştiren ve sürdüren yeni bir kuruluş olan Privacy Solutions projesini duyuruyoruz. Privacy Solutions, I2P protokolleri ve teknolojisine dayalı, kullanıcıların gizliliğini, güvenliğini ve anonimliğini artırmak üzere tasarlanmış birkaç yeni geliştirme çalışmasını içerir.

Bu çabalar şunları içerir:

1. The Abscond browser bundle.
2. The i2pd C++ router project.
3. The "BigBrother" I2P network monitoring project.
4. The Anoncoin crypto-coin project.
5. The Monero crypto-coin project.

Privacy Solutions'un başlangıç finansmanı Anoncoin ve Monero projelerinin destekçileri tarafından sağlandı. Privacy Solutions, Norveç merkezli, Norveç devletinin resmi sicillerine kayıtlı, kâr amacı gütmeyen türde bir kuruluştur. (ABD'deki 501(c)3'e benzer.)

Privacy Solutions, BigBrother (bunun ne olduğunu sonra ele alacağız) ve düşük gecikmeli ağları birincil taşıma katmanı olarak kullanması planlanan kripto paralar nedeniyle ağ araştırmaları için Norveç hükümetinden finansman başvurusunda bulunmayı planlıyor. Araştırmamız, anonimlik, güvenlik ve gizlilik alanlarındaki yazılım teknolojisi ilerlemelerini destekleyecek.

Önce Abscond Browser Bundle hakkında biraz. Bu, ilk başta Meeh’in tek kişilik bir projesiydi, ancak daha sonra arkadaşlar yamalar göndermeye başladı; proje artık, Tor’un tarayıcı paketiyle (browser bundle) sağladığı gibi I2P’ye aynı kolay erişimi sunmayı hedefliyor. İlk sürümümüz uzak değil; Apple derleme araç zincirinin kurulumu da dahil olmak üzere yalnızca birkaç gitian betik görevi kaldı. Yine de, kararlı ilan etmeden önce I2P’nin durumunu kontrol etmek için Java örneğinden PROCESS_INFORMATION (bir süreç hakkında kritik bilgileri tutan bir C yapısı) ile izleme ekleyeceğiz. I2pd hazır olduğunda Java sürümünün yerine de geçecek; böylece pakete artık bir JRE (Java Çalışma Ortamı) dahil etmenin anlamı kalmayacak. Abscond Browser Bundle hakkında daha fazlasını https://hideme.today/dev adresinde okuyabilirsiniz.

Ayrıca i2pd'nin mevcut durumu hakkında bilgi vermek istiyoruz. i2pd artık iki yönlü akışı destekliyor; bu da yalnızca HTTP'yi değil, aynı zamanda uzun ömürlü iletişim kanallarını da kullanmayı mümkün kılıyor. Anında IRC desteği eklendi. i2pd kullanıcıları, I2P IRC ağına erişmek için bunu Java I2P'de olduğu gibi kullanabiliyor. I2PTunnel, I2P ağının temel özelliklerinden biridir ve I2P olmayan uygulamaların şeffaf biçimde iletişim kurmasına olanak tanır. Bu nedenle, i2pd için hayati bir özellik ve başlıca kilometre taşlarından biridir.

Son olarak, I2P'ye aşinaysanız muhtemelen Bigbrother.i2p'yi biliyorsunuzdur; bu, Meeh'in bir yıldan biraz daha önce yaptığı bir metrik sistemidir. Yakın zamanda, Meeh'in aslında ilk başlatmadan bu yana rapor gönderen düğümlerden 100Gb tekrarsız veriye sahip olduğunu fark ettik. Bu da Privacy Solutions'a taşınacak ve NSPOF (tek hata noktası olmayan) arka uç ile yeniden yazılacak. Bununla birlikte Graphite'ı (http://graphite.wikidot.com/screen-shots) kullanmaya da başlayacağız. Bu, son kullanıcılarımız için gizlilik sorunları yaratmadan ağ hakkında harika bir genel bakış sağlayacak. İstemciler ülke, router hash ve tunnel oluşturmadaki başarı oranı dışında tüm verileri filtreler. Bu hizmetin adı, her zamanki gibi, Meeh'in küçük bir şakasıdır.

Buradaki haberleri biraz kısalttık; daha fazla bilgiyle ilgileniyorsanız lütfen https://blog.privacysolutions.no/ adresini ziyaret edin. Hâlâ yapım aşamasındayız ve daha fazla içerik gelecek!

Daha fazla bilgi için şu adresten iletişime geçin: press@privacysolutions.no

Saygılarımla,

Mikal "Meeh" Villa
