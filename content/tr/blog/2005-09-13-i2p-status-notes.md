---
title: "2005-09-13 için I2P Durum Notları"
date: 2005-09-13
author: "jr"
description: "NAT delik açma (NAT hole punching) için SSU tanıştırmaları, birim testi ödül programındaki ilerleme, istemci uygulaması yol haritası tartışması ve kullanımdan kaldırılmış garantili teslim modunun kaldırılmasını kapsayan haftalık güncelleme"
categories: ["status"]
---

Herkese selam, haftalık durum notlarının zamanı geldi

* Index

1) Ağ durumu 2) SSU introductions / NAT delik açma 3) Ödüller 4) İstemci uygulaması yönergeleri 5) ???

* 1) Net status

Ağda 0.6.0.5 sürümüyle yol almaya hâlâ devam ediyoruz ve neredeyse herkes güncelledi; birçoğu da o zamandan beri derlemelerden birini çalıştırıyor (CVS HEAD şu anda 0.6.0.5-9). Genel olarak her şey hâlâ iyi çalışıyor, ancak gözlemlediğim kadarıyla ağ trafiğinde ciddi bir artış var; muhtemelen daha fazla i2p-bt veya i2phex kullanımından dolayı. IRC sunucularından biri dün gece küçük bir aksama yaşadı, fakat diğeri gayet iyi dayandı ve işler iyi şekilde toparlanmış görünüyor. Bununla birlikte, CVS derlemelerinde hata işleme ve diğer özelliklerde önemli iyileştirmeler yapıldı, bu yüzden bu hafta içinde yeni bir sürüm çıkaracağımızı bekliyorum.

* 2) SSU introductions / NAT hole punching

CVS'teki en son derlemeler, uzun süredir tartışılan SSU introductions [1] desteğini içeriyor; bu da, kullanıcıların kontrol etmedikleri bir NAT veya güvenlik duvarının arkasında bulunduğu durumlarda merkeziyetsiz NAT hole punching (NAT delme) gerçekleştirmemize olanak tanıyor. Simetrik NAT'ı desteklemese de, sahadaki durumların çoğunu kapsıyor. Sahadan gelen raporlar iyi; ancak yalnızca en son derlemelere sahip kullanıcılar NAT arkasındaki kullanıcılarla iletişim kurabiliyor - eski derlemelerin, önce kullanıcının onlara ulaşmasını beklemesi gerekiyor. Bu nedenle, bu kısıtlı rotaların kullanımda olduğu süreyi azaltmak için kodu normalden daha erken bir sürümde yayımlayacağız.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#introduction

* 3) Bounties

Az önce i2p-cvs posta listesini kontrol ediyordum ve Comwiz'den, birim test ödülünün [2] görünüşe göre 3. aşamasıyla ilgili bir dizi commit fark ettim. Belki Comwiz bu konularla ilgili bir durum güncellemesi bu geceki toplantıda verebilir.

[2] http://www.i2p.net/bounty_unittests

Bu arada, anonim bir kişinin önerisi sayesinde, hall of fame [3]'i biraz güncelledim; buna katkı tarihlerini eklemek, aynı kişiden gelen birden fazla bağışı birleştirmek ve tek bir para birimine dönüştürmek de dahil. Katkıda bulunan herkese tekrar teşekkür ederim; eğer yayınlanan yanlış bilgi varsa ya da bir şey eksikse, lütfen iletişime geçin, güncellenecektir.

[3] http://www.i2p.net/halloffame

* 4) Client app directions

Mevcut CVS derlemelerindeki daha yeni düzenlemelerden biri, eski mode=guaranteed teslim biçiminin kaldırılmasıdır. Bunu hâlâ kullananların olduğunu fark etmemiştim (ve bu tamamen gereksiz, çünkü bir yıldır tam özellikli streaming lib (akış kitaplığı) var), ancak i2phex’i kurcalarken o bayrağın ayarlı olduğunu fark ettim. Mevcut derlemeyle (ve sonraki tüm sürümlerle) i2phex sadece mode=best_effort kullanacak; bu da umarız performansını iyileştirir.

Bunu gündeme getirmemin amacı (i2phex kullanıcılarından söz etmenin ötesinde), I2P’nin istemci tarafında sizin nelere ihtiyaç duyduğunuzu ve zamanımın bir kısmını bunlardan bazılarını karşılamaya yardımcı olmak için ayırmam gerekip gerekmediğini sormak. Aklıma ilk gelenlerle, farklı açılarda yapılabilecek çok iş görüyorum:  = Syndie: basitleştirilmiş gönderim, otomatik eşzamanlama, veri
    içe aktarma, uygulama entegrasyonu (i2p-bt, susimail, i2phex vb. ile),
    forum benzeri davranışı sağlamak için threading (konu dizisi) desteği ve daha fazlası.
  = eepproxy: geliştirilmiş throughput (aktarım kapasitesi), pipelining desteği
  = i2phex: genel bakım (sıkıntı noktalarını anlayacak kadar yeterince
    kullanmadım)
  = irc: geliştirilmiş dayanıklılık, tekrarlayan irc sunucusu kesintilerini tespit
    edip kapalı olan sunuculardan kaçınmak, CTCP eylemlerini sunucuda değil yerelde
    filtrelemek, DCC proxy
  = jbigi, jcpuid ve service wrapper (servis sarmalayıcısı) ile geliştirilmiş x64 desteği
  = systray (sistem tepsisi) entegrasyonu ve o DOS kutusunu kaldırmak
  = ani artışlar (bursting) için geliştirilmiş bant genişliği kontrolleri
  = ağ ve CPU aşırı yüklenmesi için geliştirilmiş tıkanıklık kontrolü ve
    kurtarma.
  = üçüncü taraf uygulamalar için router console'un mevcut özelliklerini
    daha fazla ortaya çıkarmak ve belgelendirmek
  = İstemci geliştirici dokümantasyonu
  = I2P giriş dokümantasyonu

Ayrıca, tüm bunların ötesinde, yol haritasındaki [4] ve yapılacaklar listesindeki [5] diğer işler de var. Teknik olarak neye ihtiyacımız olduğunu biliyorum, ama kullanıcı açısından *sizin* neye ihtiyaç duyduğunuzu bilmiyorum. Benimle konuşun, ne istiyorsunuz?

[4] http://www.i2p.net/roadmap [5] http://www.i2p.net/todo

* 5) ???

Yukarıda bahsedilenlerin ötesinde, router çekirdeğinde ve uygulama geliştirme tarafında başka çalışmalar da sürüyor, ancak şu anda her şey kullanıma hazır değil. Gündeme getirmek istediği bir şey olan varsa, bu gece 20:00 UTC'de #i2p'deki toplantıya uğrayın!

=jr
