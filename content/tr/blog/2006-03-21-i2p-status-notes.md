---
title: "2006-03-21 için I2P Durum Notları"
date: 2006-03-21
author: "jr"
description: "Ağ istatistikleri için JRobin entegrasyonu, biff ve toopie IRC botları ve yeni GPG anahtarı duyurusu"
categories: ["status"]
---

Selam millet, yine salı oldu.

* Index

1) Ağ durumu 2) jrobin 3) biff ve toopie 4) yeni anahtar 5) ???

* 1) Net status

Geçtiğimiz hafta oldukça istikrarlı geçti, henüz yeni bir sürüm yok. Bir süredir tunnel hız sınırlaması ve düşük bant genişliğinde çalışma üzerinde yoğun şekilde çalışıyorum, ancak bu testlere yardımcı olmak için JRobin'i web konsoluyla ve istatistik yönetim sistemimizle entegre ettim.

* 2) JRobin

JRobin [1], RRDtool [2]'un tamamen Java ile gerçekleştirilen bir portudur; bu da zzz'nin çok az bellek ek yüküyle durmaksızın ürettiği türden güzel grafikler oluşturmamıza olanak tanır.  Bunu tamamen bellek içi çalışacak şekilde yapılandırdık, bu yüzden dosya kilidi çekişmesi yok ve veritabanını güncelleme süresi algılanamayacak kadar kısadır.  JRobin'in yapabildiği ama henüz yararlanmadığımız bir sürü güzel özellik var, ancak bir sonraki sürüm temel işlevselliği ve verileri RRDtool'un anlayabileceği bir biçimde dışa aktarma olanağını içerecek.

[1] http://www.jrobin.org/ [2] http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/

* 3) biff and toopie

Postman bazı kullanışlı botlar üzerinde yoğun biçimde çalışıyor ve memnuniyetle bildirebilirim ki sevimli biff geri döndü [3], irc2p'de takılırken (anonim) e-posta aldığında sana haber veriyor.  Buna ek olarak, postman bizim için yepyeni bir bot geliştirdi - toopie - I2P/irc2p için bir bilgi botu olarak hizmet etmesi için.  toopie'yi hâlâ SSS'lerle besliyoruz, ancak kısa süre içinde olağan kanallara katılacak.  Teşekkürler postman!

[3] http://hq.postman.i2p/?page_id=15

* 4) new key

Dikkat edenler fark etmişsinizdir, GPG anahtarımın süresi birkaç gün içinde doluyor.  http://dev.i2p.net/~jrandom adresindeki yeni anahtarımın parmak izi 0209 9706 442E C4A9 91FA  B765 CE08 BC25 33DC 8D49 ve anahtar kimliği 33DC8D49.  Bu gönderi eski anahtarımla imzalanmıştır, ancak önümüzdeki yıl boyunca sonraki gönderilerim (ve sürümlerim) yeni anahtarla imzalanacak.

* 5) ???

Şimdilik bu kadar - birkaç dakika içinde haftalık toplantımıza bir selam vermek için #i2p’ye uğrayın!

=jr
