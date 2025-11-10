---
title: "2005-07-12 için I2P Durum Notları"
date: 2005-07-12
author: "jr"
description: "Hizmetlerin yeniden sağlanması, SSU testlerindeki ilerleme ve olası basitleştirme amacıyla I2CP şifreleme katmanının analizi konularını kapsayan haftalık güncelleme"
categories: ["status"]
---

Selam millet, yine haftanın o zamanı geldi

* Index

1) squid/www/cvs/dev.i2p geri yüklendi 2) SSU testi 3) I2CP kriptografisi 4) ???

* 1) squid/www/cvs/dev.i2p restored

Birkaç colocation sunucusuyla boğuştuktan sonra, eski hizmetlerin bir kısmı geri yüklendi - squid.i2p (iki varsayılan outproxy'den biri), www.i2p (www.i2p.net'e güvenli bir yönlendirme), dev.i2p (e-posta listesi arşivlerinin, cvsweb'in ve varsayılan netDb seed'lerinin bulunduğu dev.i2p.net'e güvenli bir yönlendirme) ve cvs.i2p (CVS sunucumuza güvenli bir yönlendirme - cvs.i2p.net:2401). Blogum hâlâ ortada yok, ama içeriği zaten kayboldu, bu yüzden er ya da geç taptaze bir başlangıç gerekecek. Bu hizmetler artık güvenilir biçimde yeniden çevrimiçi olduğuna göre, şuna geçme zamanı...

* 2) SSU testing

Herkesin router console’undaki küçük sarı kutuda belirtildiği gibi, SSU için canlı ağ testlerinin bir sonraki turuna başladık. Testler herkes için değil, ancak maceraseverseniz ve manuel yapılandırma yapmaktan çekinmiyorsanız, router console’unuzda belirtilen ayrıntılara göz atın (http://localhost:7657/index.jsp). Birden fazla test turu olabilir, ancak 0.6 sürümünden önce SSU’da büyük değişiklikler öngörmüyorum (0.6.1, portlarını yönlendiremeyen veya başka şekilde gelen UDP bağlantılarını alamayanlar için destek ekleyecek).

* 3) I2CP crypto

Yeni giriş belgeleri üzerinde yeniden çalışırken, I2CP SDK içinde yapılan ek şifreleme katmanını gerekçelendirmekte biraz zorlanıyorum. I2CP kripto katmanının ilk amacı, iletilen mesajlara temel düzeyde uçtan uca koruma sağlamak ve ayrıca I2CP istemcilerinin (ör. I2PTunnel, the SAM bridge, I2Phex, azneti2p, vb.) güvenilmeyen router'lar üzerinden iletişim kurmasına olanak tanımaktı. Ancak uygulama ilerledikçe, I2CP katmanının uçtan uca koruması gereksiz hale geldi; çünkü tüm istemci mesajları, router tarafından garlic mesajları içinde uçtan uca şifreleniyor, göndericinin leaseSet'ini ve bazen bir teslim durumu mesajını paketleyerek. Bu garlic katmanı zaten göndericinin router'ından alıcının router'ına kadar uçtan uca şifreleme sağlar - tek fark, bizzat o router'ın kötü niyetli olmasına karşı koruma sağlamamasıdır.

Öngörülebilir kullanım senaryolarına baktığımda ise, yerel router'a güvenilmeyecek geçerli bir senaryo aklıma gelmiyor. En azından, I2CP şifrelemesi yalnızca router'dan iletilen mesajın içeriğini gizler - router yine de hangi hedefe gönderilmesi gerektiğini bilmek zorundadır. Gerekirse, I2CP istemcisi ile router'ın ayrı makinelerde çalışmasına izin vermek için bir SSH/SSL I2CP listener (dinleyici) ekleyebiliriz, ya da bu tür durumlara ihtiyaç duyanlar mevcut tünelleme araçlarını kullanabilir.

Şu anda kullanılan şifreleme katmanlarını kısaca yinelemek gerekirse, şunlar var:  * I2CP'nin uçtan uca ElGamal/AES+SessionTag katmanı,    göndericinin destination (hedef adres)inden alıcının destination'ına kadar şifreler.  * router'ın uçtan uca garlic encryption katmanı    (ElGamal/AES+SessionTag), göndericinin router'ından    alıcının router'ına kadar şifreler.  * Hem inbound hem outbound    tunnels için, her birinin üzerindeki hop (atlama) noktalarında uygulanan tunnel şifreleme katmanı (ancak giden    uç nokta ile gelen ağ geçidi arasında değil).  * router'lar arasındaki taşıma şifreleme katmanı.

Bu katmanlardan birini kaldırma konusunda oldukça temkinli olmak istiyorum, ancak gereksiz işler yaparak kaynaklarımızı boşa harcamak da istemiyorum. Önerdiğim şey, ilk I2CP şifreleme katmanını kaldırmak (ancak elbette I2CP oturum kurulumu sırasında kullanılan kimlik doğrulamasını, leaseSet yetkilendirmesini ve gönderici kimlik doğrulamasını korumaya devam ederek). Bunu neden korumamız gerektiğine dair bir gerekçe sunabilecek olan var mı?

* 4) ???

Şimdilik bu kadar, ama her zamanki gibi pek çok şey olup bitiyor. Bu hafta da toplantı yok; ancak gündeme getirmek istediği bir şey olan varsa, lütfen çekinmeden listeye veya foruma yazsın. Ayrıca, #i2p’deki scrollback’i (sohbet geçmişi) okuyor olsam da, genel sorular veya endişeler tartışmaya daha fazla kişinin katılabilmesi için bunun yerine listeye gönderilmeli.

=jr
