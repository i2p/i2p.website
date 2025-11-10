---
title: "2006-10-10 tarihli I2P Durum Notları"
date: 2006-10-10
author: "jr"
description: "Olumlu geri bildirim alan 0.6.1.26 sürümü, 1.0'a yaklaşan Syndie 0.910a ve Syndie için dağıtık sürüm kontrolünün değerlendirilmesi"
categories: ["status"]
---

Herkese selam, bu hafta kısa durum notları

* Index

1) 0.6.1.26 ve ağ durumu 2) Syndie geliştirme durumu 3) Dağıtık sürüm kontrolünün yeniden ele alınması 4) ???

* 1) 0.6.1.26 and network status

Geçen gün zzz’den birçok i2psnark iyileştirmesi ve Complication’dan bazı yeni NTP güvenlik denetimlerini içeren yeni 0.6.1.26 sürümünü yayımladık ve geri bildirimler olumlu oldu. Ağ, herhangi bir yeni tuhaf davranış olmadan biraz büyüyor gibi görünüyor; yine de bazı kişiler hâlâ tunnel’larını oluşturmakta zorlanıyor (her zaman olduğu gibi).

* 2) Syndie development status

Giderek daha fazla iyileştirme gelmeye devam ediyor; mevcut alfa sürümü 0.910a'da. 1.0 için özellik listesi büyük ölçüde karşılandı, bu yüzden şu anda işin çoğu hata düzeltme ve dokümantasyon. Test etmeye yardımcı olmak isterseniz #i2p'ye uğrayın :)

Ayrıca, kanalda Syndie GUI’nin tasarımları üzerine bazı tartışmalar yapıldı - meerboop bazı güzel fikirler ortaya koydu ve bunların belgelemesi üzerinde çalışıyor. Syndie GUI, Syndie 2.0 sürümünün ana bileşenidir, bu yüzden onu ne kadar çabuk devreye alırsak, o kadar çabuk dünyayı ele geçir^W^W^W^W Syndie’yi habersiz kitlelere sunabiliriz.

Syndie blogumda, bizzat Syndie kullanılarak hata ve özellik isteği takibine ilişkin yeni bir öneri de var. Erişimi kolaylaştırmak için, o gönderinin düz metin dışa aktarımını web'e koydum - 1. sayfa <http://dev.i2p.net/~jrandom/bugsp1.txt> adresinde ve 2. sayfa <http://dev.i2p.net/~jrandom/bugsp2.txt> adresinde.

* 3) Distributed version control revisited

Syndie için hâlâ netleştirilmesi gereken şeylerden biri, kullanılacak herkese açık sürüm kontrol sistemi ve daha önce de belirtildiği gibi, dağıtık ve çevrimdışı işlevsellik gerekli. Dışarıda bulunan yaklaşık yarım düzine açık kaynak seçenek (darcs, mercurial, git/cogito, monotone, arch, bzr, codeville) üzerinde çalışıyor, dokümantasyonlarını inceliyor, onları deniyor ve geliştiricileriyle konuşuyorum. Şu anda, işlevsellik ve güvenlik açısından monotone ve bzr en iyileri gibi görünüyor (güvenilmeyen depolar söz konusu olduğunda, yalnızca kimliği doğrulanmış değişiklikleri çektiğimizden emin olmak için güçlü kriptografiye ihtiyacımız var) ve monotone'un kriptografiyle sıkı entegrasyonu oldukça cazip görünüyor. Yine de yüzlerce sayfalık dokümantasyonu okumaya devam ediyorum; ancak monotone geliştiricileriyle yaptığım görüşmelerden anladığım kadarıyla, her şeyi doğru yapıyorlar gibi görünüyor.

Elbette, hangi dvcs (dağıtık sürüm kontrol sistemi) ile yolumuza devam edersek edelim, tüm sürümler düz tarball biçiminde kullanıma sunulacak ve yamalar inceleme için düz diff -uw biçiminde kabul edilecek. Yine de, geliştirmeye dahil olmayı düşünenler için, düşüncelerinizi ve tercihlerinizi duymayı çok isterim.

* 4) ???

Gördüğünüz gibi, her zamanki gibi pek çok şey oluyor. Forumdaki "solve world hunger" başlığında da daha fazla tartışma oldu, bu yüzden <http://forum.i2p.net/viewtopic.php?t=1910> adresinden göz atın.

Daha konuşmak istediğiniz başka bir şey varsa, lütfen bu akşamki geliştirici toplantımız için #i2p kanalına uğrayın ya da forumda veya posta listesinde yazın!

=jr
