---
title: "2005-08-02 tarihli I2P Durum Notları"
date: 2005-08-02
author: "jr"
description: "0.6 sürüm durumunu, PeerTest sistemini, SSU tanıştırmalarını, I2PTunnel web arayüzü düzeltmelerini ve I2P üzerinden mnet'i kapsayan gecikmiş bir güncelleme"
categories: ["status"]
---

Merhaba herkese, bugün notlar gecikmeli,

* Index:

1) 0.6 durumu 2) PeerTest (eşler arası test) 3) SSU tanıştırmaları 4) I2PTunnel web arayüzü 5) i2p üzerinden mnet 6) ???

* 1) 0.6 status

Hepinizin de gördüğü gibi, birkaç gün önce 0.6 sürümünü yayımladık ve genel olarak işler oldukça iyi gidiyor. 0.5.*’ten bu yana yapılan bazı transport (aktarım) iyileştirmeleri netDb gerçeklemesinde sorunları ortaya çıkardı, ancak bunların büyük bir kısmına yönelik düzeltmeler şu anda (0.6-1 build olarak) test ediliyor ve kısa süre içinde 0.6.0.1 olarak dağıtılacak. Ayrıca farklı NAT ve güvenlik duvarı yapılandırmalarıyla ilgili bazı sorunlara ve bazı kullanıcıların yaşadığı MTU sorunlarına rastladık - daha az test eden olduğu için daha küçük test ağında bulunmayan sorunlar. En fazla sorun çıkaran durumlar için geçici çözümler eklendi, ancak yakında uzun vadeli bir çözümümüz geliyor - peer tests (eş testleri).

* 2) PeerTest

0.6.1 ile, genel IP'leri ve portları işbirliği içinde test edip yapılandırmak için yeni bir sistemi devreye alacağız. Bu, çekirdek SSU protokolüne entegre edilmiştir ve geriye dönük uyumlu olacaktır. Özünde yaptığı şey, Alice'in Bob'a genel IP'sinin ve port numarasının ne olduğunu sormasına izin vermek ve ardından Bob'un da sırayla, Alice'in doğru yapılandırmasını doğrulaması ya da düzgün çalışmasını engelleyen kısıtlamanın ne olduğunu öğrenmesi için Charlie'yi devreye sokmasını sağlamaktır. Bu teknik İnternet'te yeni bir şey değil, ancak i2p kod tabanına yeni bir ek ve en yaygın yapılandırma hatasını ortadan kaldırmalıdır.

* 3) SSU introductions

SSU protokol spesifikasyonunda açıklandığı üzere, güvenlik duvarlarının ve NAT'lerin arkasındaki insanların, aksi halde istek dışı UDP mesajlarını alamıyor olsalar bile, ağa tam olarak katılmalarını sağlayacak bir işlevsellik olacak. Tüm olası durumlarda çalışmayacak, ancak çoğunu ele alacak. SSU spesifikasyonunda tanımlanan mesajlarla PeerTest için gerekli mesajlar arasında benzerlikler var; bu nedenle, spesifikasyon söz konusu mesajlarla güncellendiğinde, tanıştırmaları PeerTest mesajlarının yanında taşıyabileceğiz. Her hâlükârda, bu tanıştırmaları 0.6.2'de devreye alacağız ve o da geriye dönük uyumlu olacak.

* 4) I2PTunnel web interface

Bazı kişiler I2PTunnel web arayüzündeki çeşitli pürüzleri fark edip bununla ilgili raporlar ilettiler ve smeghead gerekli düzeltmeleri bir araya getirmeye başladı - belki bu güncellemeleri daha ayrıntılı olarak, ayrıca bunlar için bir ETA (tahmini zaman) da açıklayabilir?

* 5) mnet over i2p

Kanalda tartışmalar sürerken orada değildim ama logları okuyunca, icepick’in mnet’i i2p üzerinde çalıştırmak için biraz kurcalama yaptığı ve bunun da mnet dağıtık veri deposunun anonim olarak çalışırken dayanıklı içerik yayınlama sunmasına olanak tanıdığı anlaşılıyor. Bu cephedeki ilerleme hakkında çok fazla bilgim yok, ancak icepick’in SAM ve twisted aracılığıyla I2P ile entegrasyonda iyi ilerleme kaydettiği anlaşılıyor; belki icepick bizi daha fazla bilgilendirebilir?

* 6) ???

Tamam, yukarıdakilerden çok daha fazlası oluyor, ama zaten gecikiyorum, bu yüzden sanırım yazmayı bırakıp bu mesajı göndermeliyim. Bu akşam kısa bir süreliğine çevrimiçi olabileceğim, bu yüzden etrafta olan varsa saat 9:30p civarı (bunu ne zaman alırsanız alın ;) her zamanki irc sunucularındaki #i2p kanalında {irc.duck.i2p, irc.postman.i2p, irc.freenode.net, irc.metropipe.net} bir toplantı yapabiliriz.

Sabır gösterdiğiniz ve işleri ileriye taşımamıza yardımcı olduğunuz için teşekkürler!

=jr
