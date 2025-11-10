---
title: "2005-02-15 için I2P Durum Notları"
date: 2005-02-15
author: "jr"
description: "Ağın 211 routers düzeyine ulaşması, 0.5 sürüm hazırlıkları ve i2p-bt 0.1.7'yi kapsayan haftalık I2P geliştirme durum notları"
categories: ["status"]
---

Merhaba, yine haftanın o zamanı,

* Index

1) Ağ durumu 2) 0.5 durumu 3) i2p-bt 0.1.7 4) ???

* 1) Net status

Ağda yeni hatalar ortaya çıkmamış olsa da, geçen hafta popüler bir Fransız p2p web sitesinde biraz görünürlük kazandık; bu da hem kullanıcı sayısında hem de bittorrent etkinliğinde artışa yol açtı. Zirvede ağ üzerindeki router sayısı 211’e ulaştı, ancak son zamanlarda 150 ile 180 arasında seyrediyor. Bildirilen bant genişliği kullanımı da arttı, ne var ki maalesef irc güvenilirliği azaldı; yük nedeniyle sunuculardan biri bant genişliği limitlerini düşürdü. Bunu iyileştirmek için streaming kitaplığına bir dizi iyileştirme yapıldı, ancak bunlar 0.5-pre branch üzerinde, dolayısıyla henüz canlı ağa sunulmadı.

Bir diğer geçici sorun, HTTP outproxy’lerinden (dış proxy) birinin (www1.squid.i2p) hizmet dışı kalması oldu; bu da outproxy isteklerinin %50’sinin başarısız olmasına yol açtı. I2PTunnel yapılandırmanızı [1] açıp eepProxy’yi düzenleyerek ve "Outproxies:" satırını yalnızca "squid.i2p" içerecek şekilde değiştirerek bu outproxy’yi geçici olarak kaldırabilirsiniz. Umarız yedekliliği artırmak için diğerini de yakında yeniden çevrimiçi hale getirebiliriz.

[1] http://localhost:7657/i2ptunnel/index.jsp

* 2) 0.5 status

Geçtiğimiz hafta 0.5 üzerinde çok ilerleme kaydettik (bunu duymaktan bıkmışsınızdır, değil mi?). postman, cervantes, duck, spaetz ve adı açıklanmayan bir kişinin yardımı sayesinde, yeni kodla neredeyse bir haftadır bir test ağı çalıştırıyoruz ve yerel test ağımda görmediğim epey sayıda hatayı çözdük.

Yaklaşık son bir gündür yapılan değişiklikler küçük çaplı ve 0.5 sürümü yayımlanmadan önce tamamlanmamış kayda değer bir kod işi kalacağını öngörmüyorum. Biraz ek temizlik, dokümantasyon ve paketleme kaldı; ayrıca, zaman içinde ek hatalar ortaya çıkarsa diye 0.5 test ağının bir süre daha çalışmasına izin vermekte de zarar yok. Bu GERİYE DÖNÜK UYUMLU OLMAYAN BİR SÜRÜM olacağından, güncelleme planlamanız için size zaman tanımak adına, 0.5’in yayımlanması için SON TARİHİ BU CUMA olarak belirleyeceğim.

bla'nın irc'de belirttiği gibi, eepsite(I2P Site) barındıranlar sitelerini Perşembe veya Cuma günü yayından kaldırmak ve birçok kullanıcı yükseltmiş olacağından Cumartesi'ye kadar kapalı tutmak isteyebilirler. Bu, bir kesişim saldırısının etkisini azaltmaya yardımcı olacaktır (örneğin, ağın %90'ı 0.5'e geçmişse ve siz hâlâ 0.4'teyseniz, birisi eepsite(I2P Site) adresinize ulaşırsa, ağda kalan router'ların %10'u arasında olduğunuzu bilir).

0.5’te nelerin güncellendiğine girmeye başlayabilirim, ama iş sayfalarca uzar gider, o yüzden belki de şimdilik bekleyip bunu yazmam gereken dokümantasyona koymalıyım :)

* 3) i2p-bt 0.1.7

duck, geçen haftaki 0.1.6 güncellemesi için bir hata düzeltme sürümü hazırladı ve söylentilere göre epey sağlam (artan ağ kullanımı göz önüne alındığında belki /fazla/ sağlam ;)  Daha fazla bilgi @ i2p-bt forumunda [2]

[2] http://forum.i2p.net/viewtopic.php?t=300

* 4) ???

IRC tartışmalarında ve forumda [3] pek çok başka şey de oluyor; kısaca özetlemek mümkün değil. Belki ilgilenenler toplantıya uğrayıp bizimle güncellemelerini ve düşüncelerini paylaşabilir? Her neyse, hepinizle birazdan görüşürüz

=jr
