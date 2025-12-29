---
title: "Gizliliğin 20 Yılı: I2P'nin Kısa Tarihi"
date: 2021-08-28
slug: "20-years-of-privacy-a-brief-history-of-i2p"
author: "sadie"
description: "Bildiğimiz Haliyle I2P'nin Tarihi"
categories: ["general"]
---

## Görünmezlik en iyi savunmadır: internet içinde bir internet kurmak

> "I believe most people want this technology so they can express themselves freely. It's a comfortable feeling when you know you can do that. At the same time we can conquer some of the problems seen within the Internet by changing the way security and privacy is viewed, as well as the extent to what it is valued."

Ekim 2001'de, 0x90 (Lance James) bir hayal kurdu. Bu, "diğer Freenet kullanıcılarıyla Freenet konularını konuşmak ve anonimlik, gizlilik ve güvenliği sürdürürken Freenet anahtarlarını değiş tokuş etmek için anlık iletişim kurma isteği" olarak başladı. Buna IIP — the Invisible IRC Project (Görünmez IRC Projesi) adı verildi.

The Invisible IRC Project, The InvisibleNet'in arkasındaki ideal ve çerçeveye dayanıyordu. 2002'de yapılan bir röportajda, 0x90 projeyi "akıllı ağ teknolojisinde yenilikçilik"e odaklanan bir proje olarak tanımladı; hedefi ise "yaygın şekilde kullanılan, ancak güvensizliğiyle tanınan İnternet üzerinde güvenlik ve gizlilikte en yüksek standartları sağlamak"tı.

2003 yılına gelindiğinde, en büyükleri Freenet, GNUNet ve Tor olmak üzere birkaç benzer proje başlatılmıştı. Bu projelerin tümünün, çeşitli türlerdeki trafiği şifrelemek ve anonimleştirmek gibi geniş kapsamlı hedefleri vardı. IIP açısından, yalnızca IRC’nin yeterince büyük bir hedef olmadığı anlaşıldı. Gerekense tüm protokoller için bir anonimleştirme katmanıydı.

2003'ün başlarında, "jrandom" adında yeni bir anonim geliştirici projeye katıldı. Açık hedefi IIP'in kapsamını genişletmekti. jrandom, IIP kod tabanını Java ile yeniden yazmak ve protokolleri, güncel makaleler ile Tor ve Freenet'in o dönemde almakta olduğu erken tasarım kararlarını temel alarak yeniden tasarlamak istiyordu. "onion routing (soğan yönlendirme)" gibi bazı kavramlar "garlic routing (sarımsak yönlendirme)" olacak şekilde değiştirildi.

2003 yazının sonlarına doğru, jrandom projeyi kontrolüne almış ve adını Invisible Internet Project veya "I2P" olarak değiştirmişti. Projenin felsefesini ana hatlarıyla ortaya koyan bir belge yayımladı ve teknik hedefleri ile tasarımını mixnet'ler ve anonimleştirme katmanları bağlamında ele aldı. Ayrıca, bugün I2P'nin kullandığı ağın temelini oluşturan iki protokolün (I2CP ve I2NP) spesifikasyonlarını yayımladı.

2003 sonbaharına gelindiğinde, I2P, Freenet ve Tor hızla gelişiyordu. jrandom, 1 Kasım 2003'te I2P sürüm 0.2'yi yayımladı ve sonraki 3 yıl boyunca sık aralıklarla yeni sürümler yayımlamayı sürdürdü.

Şubat 2005'te, zzz I2P'yi ilk kez kurdu. 2005 yazına gelindiğinde, zzz zzz.i2p ve stats.i2p'yi kurmuştu; bunlar I2P geliştirme için merkezi kaynaklar haline geldi. Temmuz 2005'te, jrandom IP keşfi ve güvenlik duvarı geçişi için yenilikçi SSU (Secure Semi-reliable UDP) taşıma protokolünü de içeren 0.6 sürümünü yayımladı.

2006'nın sonlarından 2007'ye kadar, jrandom odağını Syndie'ye kaydırdığı için I2P çekirdek geliştirme çalışmaları ciddi ölçüde yavaşladı. Kasım 2007'de, jrandom bir yıl veya daha uzun süre ara vermek zorunda kalacağını bildiren gizemli bir mesaj gönderdiğinde felaket yaşandı. Ne yazık ki, jrandom'dan bir daha haber alınamadı.

Felaketin ikinci aşaması, i2p.net sunucularının neredeyse tamamını barındıran şirketin bir elektrik kesintisi yaşaması ve hizmete tam olarak geri dönememesiyle 13 Ocak 2008'de gerçekleşti. Complication, welterde ve zzz, projeyi yeniden ayağa kaldırıp çalışır hâle getirmek için hızla kararlar alarak projeyi i2p2.de adresine taşıdılar ve sürüm kontrolü için CVS'den monotone'a geçtiler.

Proje, merkezî kaynaklara aşırı derecede bağımlı olduğunu fark etti. 2008 boyunca yapılan çalışmalar projeyi merkeziyetsizleştirdi ve rolleri birden fazla kişiye dağıttı. 31 Temmuz 2009 tarihli 0.7.6 sürümünden itibaren, zzz sonraki 49 sürümü imzalayacaktı.

2009'un ortalarına gelindiğinde, zzz kod tabanını çok daha iyi anlamış ve birçok ölçeklenebilirlik sorununu belirlemişti. Ağ, hem anonimleştirme hem de sansürü aşma yetenekleri sayesinde büyüdü. Ağ içi otomatik güncellemeler kullanılabilir hale geldi.

2010 sonbaharında, zzz, web sitesi dokümantasyonu eksiksiz ve doğru olana kadar I2P geliştirmesine moratoryum ilan etti. Bu 3 ay sürdü.

2010'dan itibaren, zzz, ech, hottuna ve diğer katkıcılar, COVID kısıtlamalarına kadar her yıl CCC'ye (Chaos Communications Congress) katıldılar. Proje etrafında bir topluluk oluşturup sürümleri birlikte kutladılar.

2013 yılında, yerleşik I2P desteğine sahip ilk kripto para birimi olan Anoncoin geliştirildi, meeh gibi geliştiriciler I2P ağına altyapı sağlıyordu.

2014 yılında, str4d I2PBote’a katkıda bulunmaya başladı ve Real World Crypto’da, I2P’nin kriptografisinin güncellenmesi üzerine tartışmalar başladı. 2014’ün sonlarına gelindiğinde, yeni imzalama kriptografisinin büyük bölümü, ECDSA ve EdDSA dahil, tamamlanmıştı.

2015 yılında I2PCon, konuşmaların, topluluk desteğinin ve Amerika ile Avrupa’dan katılımcıların yer aldığı Toronto’da gerçekleştirildi. 2016’da Stanford’daki Real World Crypto’da, str4d kriptografi geçişinin ilerleme durumu üzerine bir konuşma yaptı.

NTCP2, 2018'de (sürüm 0.9.36) uygulandı, DPI sansürüne karşı direnç sağlayarak ve daha hızlı, modern kriptografi sayesinde CPU yükünü azaltarak.

2019 yılında ekip, DefCon ve Monero Village'ın da aralarında bulunduğu daha fazla konferansa katılarak geliştiriciler ve araştırmacılarla temas kurdu. Hoàng Nguyên Phong'un I2P sansürü üzerine araştırması USENIX'teki FOCI'ye kabul edildi ve bu da I2P Metrics'in ortaya çıkmasına yol açtı.

CCC 2019'da, Monotone'den GitLab'a geçmeye karar verildi. 10 Aralık 2020'de, proje resmen Monotone'den Git'e geçti ve Git kullanan geliştiricilerin dünyasına katıldı.

0.9.49 (2021), yıllarca süren spesifikasyon çalışmalarını tamamlayarak routers için yeni, daha hızlı ECIES-X25519 şifrelemesine geçişi başlattı. Geçiş birkaç sürüm sürecekti.

## 1.5.0 — Erken yıl dönümü sürümü

0.9.x sürümleriyle geçen 9 yılın ardından, proje anonimlik ve güvenlik sağlamaya yönelik yaklaşık 20 yıllık çalışmayı takdir etmek amacıyla doğrudan 0.9.50'den 1.5.0'a geçti. Bu sürüm, bant genişliğini azaltmak için daha küçük tunnel (tünel) oluşturma mesajlarının uygulanmasını tamamladı ve X25519 şifrelemeye geçişi sürdürdü.

**Tebrikler, ekip. Hadi 20 tane daha yapalım.**
