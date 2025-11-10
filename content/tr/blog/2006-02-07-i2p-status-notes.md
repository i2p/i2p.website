---
title: "2006-02-07 için I2P Durum Notları"
date: 2006-02-07
author: "jr"
description: "PRE ağındaki testlerin ilerlemesi, ElGamal şifreleme için kısa üs optimizasyonu ve gwebcache desteğine sahip I2Phex 0.1.1.37"
categories: ["status"]
---

Selam millet, salı yine geldi

* Index

1) Ağ durumu 2) _PRE ağ ilerlemesi 3) I2Phex 0.1.1.37 4) ???

* 1) Net status

Son bir hafta içinde canlı ağda kayda değer bir değişiklik olmadı, dolayısıyla canlı ağın durumu çok değişmedi. Öte yandan...

* 2) _PRE net progress

Geçen hafta, 0.6.1.10 sürümü için geriye dönük uyumsuz kodları CVS’de ayrı bir dala (i2p_0_6_1_10_PRE) commit etmeye başladım ve bir grup gönüllü de bunu test etmemize yardımcı oldu. Bu yeni _PRE ağı canlı ağ ile iletişim kuramıyor ve anlamlı bir anonimliğe sahip değil (çünkü 10’dan az eş var). Bu router’lardan alınan pen register günlükleriyle, hem yeni hem de eski koddaki birkaç ciddi hata tespit edilip giderildi, ancak daha fazla test ve iyileştirme çalışmaları devam ediyor.

Yeni tunnel oluşturma kriptografisinin bir yönü, oluşturucunun her atlama (hop) için baştan yoğun işlem gerektiren asimetrik şifrelemeyi yapmak zorunda olmasıdır; oysa eski tunnel oluşturma, yalnızca önceki atlama tunnel’e katılmayı kabul ederse şifreleme yapıyordu. Bu şifreleme, hem yerel CPU performansına hem de tunnel uzunluğuna bağlı olarak 400-1000 ms veya daha fazla sürebilir (her atlama için tam bir ElGamal şifrelemesi yapar). _PRE net üzerinde hâlihazırda kullanılan bir optimizasyon, kısa üs [1] kullanımıdır - ElGamal anahtarı olarak 2048 bitlik 'x' kullanmak yerine, 228 bitlik 'x' kullanıyoruz; bu, ayrık logaritma probleminin iş yüküyle eşleşmesi için önerilen uzunluktur. Bu, atlama başına şifreleme süresini yaklaşık bir büyüklük mertebesi düşürmüştür, ancak şifre çözme süresini etkilemez.

Kısa üslerin kullanımına ilişkin pek çok çelişen görüş var ve genel durumda güvenli değil, ancak anladığım kadarıyla, sabit bir güvenli asal kullandığımız için (Oakley group 14 [2]), q'nun mertebesi sorun teşkil etmemeli.  Bununla birlikte, bu doğrultuda ek düşünceleri olan varsa, daha fazlasını duymayı çok isterim.

Tek büyük alternatif, 1024 bitlik şifrelemeye geçmek (bu sayede belki 160 bitlik kısa bir üs kullanabiliriz). Bu, her hâlükârda uygun olabilir ve eğer _PRE net üzerinde 2048 bitlik şifreleme ile işler çok zahmetli olursa, geçişi _PRE net içinde gerçekleştirebiliriz. Aksi takdirde, yeni şifrelemenin daha geniş ölçekte yaygınlaştırılmasının olacağı 0.6.1.10 sürümü çıkana kadar bekleyebiliriz; böylece gerekli olup olmadığını görebiliriz. Böyle bir geçiş muhtemel görünürse çok daha fazla bilgi paylaşılacaktır.

[1] "Kısa Üslerle Diffie-Hellman Anahtar Uzlaşması Üzerine" -     van Oorschot, Weiner EuroCrypt 96'da.  yansısı şurada     http://dev.i2p.net/~jrandom/Euro96-DH.ps [2] http://www.ietf.org/rfc/rfc3526.txt

Her durumda, _PRE net üzerinde epey ilerleme var; bununla ilgili iletişimin çoğu irc2p üzerindeki #i2p_pre kanalında yürütülüyor.

* 3) I2Phex 0.1.1.37

Complication, Rawn'un pycache portu ile uyumlu gwebcache'leri (Gnutella web önbelleği) desteklemesi için en güncel I2Phex kodunu birleştirip yamaladı. Bu, kullanıcıların I2Phex'i indirip kurabileceği, "Connect to the network"e tıklayabileceği ve bir iki dakika sonra mevcut I2Phex eşlerine dair bazı referansları çekip ağa katılacağı anlamına geliyor. Artık i2phex.hosts dosyalarını elle yönetme ya da anahtarları elle paylaşma derdi yok (w00t)! Varsayılan olarak iki gwebcache var, ancak i2phex.cfg içindeki i2pGWebCache0, i2pGWebCache1 veya i2pGWebCache2 özelliklerini değiştirerek bunlar değiştirilebilir ya da üçüncü bir tane eklenebilir.

Harika iş, Complication ve Rawn!

* 4) ???

Şimdilik bu kadar; bu da iyi aslında, çünkü toplantıya zaten geç kaldım :) Birazdan #i2p'de görüşürüz

=jr
