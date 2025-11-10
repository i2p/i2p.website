---
title: "2006-02-28 tarihli I2P Durum Notları"
date: 2006-02-28
author: "jr"
description: "0.6.1.12 ile birlikte ağ iyileştirmeleri, yeni eş seçim stratejileri içeren 0.6.2 için yol haritası ve mini proje fırsatları"
categories: ["status"]
---

Hey millet, yine salı söylenme seansı zamanı

* Index

1) Ağ durumu ve 0.6.1.12 2) 0.6.2'ye giden yol 3) Mini projeler 4) ???

* 1) Net status and 0.6.1.12

Geçen hafta ağda kayda değer iyileşmeler görüldü; önce geçen salı 0.6.1.11’in yaygın dağıtımıyla, ardından da geçtiğimiz pazartesi yayımlanan 0.6.1.12 sürümüyle (şu ana kadar ağın %70’ine dağıtıldı - teşekkürler!). Genel olarak, 0.6.1.10 ve daha önceki sürümlere kıyasla durum çok daha iyi - tunnel oluşturma başarı oranları, o yedek tunnel’lara gerek kalmadan, tam bir büyüklük mertebesi daha yüksek; gecikme azaldı, CPU kullanımı düştü ve aktarım hızı arttı. Ayrıca, TCP tamamen devre dışı bırakılmışken, paket yeniden iletim oranı kontrol altında kalıyor.

* 2) Road to 0.6.2

There is still some improvement to be made in the peer selection code, as we are still seeing 10-20% client tunnel rejection rates, and high throughput (10+KBps) tunnels aren't as common as they should be.  On the other hand, now that CPU load is down so much, I can run an additional router on dev.i2p.net without causing problems for my primary router (which serves up squid.i2p, www.i2p, cvs.i2p, syndiemedia.i2p, and others, pushing 2-300+KBps).

Ayrıca, aşırı yoğun ağlarda bulunan insanlar için (ne yani, öyle olmayanlar da mı var?) bazı iyileştirmeleri deniyorum. Bu konuda bir miktar ilerleme var gibi görünüyor, ancak daha fazla test gerekli olacak. Bu, umarım, irc2p’de güvenilir bağlantıları sürdürmekte zorlanan 4 ya da 5 kişiye yardımcı olur (ve elbette, aynı belirtilerden sessizce mustarip olanlara da).

Bu düzgün çalıştıktan sonra, buna 0.6.2 diyebilmeden önce hâlâ yapacak işlerimiz var - bu geliştirilmiş eş (peer) seçme stratejilerine ek olarak yeni eş sıralama stratejilerine ihtiyacımız var.  Temel olarak, üç yeni strateji eklemek istiyorum - = katı sıralama (her bir eşin öncülünü ve ardılını sınırlama,   MTBF rotasyonu ile) = sabit uçlar (gelen ağ geçidi ve   giden uç nokta olarak sabit bir eş kullanma) = sınırlı komşu (ilk uzak   atlama için sınırlı bir eş kümesi kullanma)

Üzerinde çalışılacak başka ilginç stratejiler de var, ama en önemlileri bu üçü.  Bunlar hayata geçirildiğinde, 0.6.2 için işlevsel olarak tamamlanmış olacağız.  Belirsiz bir tahmini tarih: mart/nisan.

* 3) Miniprojects

Yapılacak sayısız faydalı iş var, ama yalnızca blogumda yayınladığım, bir geliştiricinin çok fazla zaman harcamadan hızlıca ortaya koyabileceği beş küçük projeyi anlattığım bir gönderiye dikkatinizi çekmek istiyorum [1]. Bunlara atılmak isteyen olursa, eminim bir teşekkür olarak genel fondan bazı kaynaklar [2] ayırırız; yine de çoğunuzun nakitten ziyade hack hevesiyle motive olduğunun farkındayım ;)

[1] http://syndiemedia.i2p.net:8000/blog.jsp?     blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&     entry=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1140652800002 [2] http://www.i2p.net/halloffame

* 4) ???

Neyse, bildiğim kadarıyla olup bitenlerin hızlı bir özeti bu. Bu arada, cervantes’e de 500. forum kullanıcısına ulaşılması vesilesiyle tebrikler :) Her zamanki gibi, birkaç dakika içinde yapılacak toplantı için #i2p’ye uğrayın!

=jr
