---
title: "2004-11-23 tarihli I2P Durum Notları"
date: 2004-11-23
author: "jr"
description: "Ağın toparlanmasını, streaming kütüphanesi testlerindeki ilerlemeyi, yaklaşan 0.4.2 sürüm planlarını ve adres defteri iyileştirmelerini kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Herkese selam, bir durum güncellemesinin vakti geldi

## Dizin:

1. Net status
2. Streaming lib
3. 0.4.2
4. Addressbook.py 0.3.1
5. ???

## 1) Ağ durumu

Geçen haftaki, işlerin oldukça tıkandığı 2-3 günlük dönemden sonra, ağ yeniden rayına oturdu (muhtemelen BitTorrent bağlantı noktasını stres testine tabi tutmayı bıraktığımız için ;). O zamandan beri ağ oldukça güvenilir - gerçekten 30-40+ gündür açık ve çalışır durumda olan birkaç router'ımız var, ancak IRC bağlantıları hâlâ zaman zaman aksıyor. Öte yandan...

## 2) Streaming lib (akış kütüphanesi)

Son yaklaşık bir haftadır, ağ üzerinde streaming kütüphanesinin canlı testlerini çok daha fazla yapıyoruz ve durum oldukça iyi görünüyor. Duck, insanların IRC sunucusuna erişmek için kullanabileceği bir tunnel kurdu ve birkaç gün boyunca yalnızca iki beklenmedik bağlantı kopması yaşadım (bu da bazı hataların izini sürüp bulmamıza yardımcı oldu). Ayrıca insanların denediği, bir squid outproxy (I2P çıkış vekil sunucusu) yönüne yönlendirilen bir i2ptunnel örneğimiz de vardı ve veri aktarım hızı, gecikme ve güvenilirlik, yan yana test ettiğimiz eski kütüphaneyle karşılaştırıldığında çok daha iyiydi.

Genel olarak, streaming kütüphanesi ilk sürüm için yeterince iyi durumda görünüyor. Hâlâ tamamlanmamış birkaç şey var, ancak eski kütüphaneye göre önemli bir iyileştirme ve size daha sonra yükseltmeniz için bir neden de vermemiz gerekiyor, değil mi? ;)

Aslında, sizi biraz kışkırtmak (ya da belki bazı çözümler üretmeniz için ilham vermek) için, streaming lib (akış kitaplığı) için ufukta gördüğüm başlıca şeyler şunlar: - akışlar arasında tıkanıklık ve RTT (gidiş-dönüş süresi) bilgisini paylaşmaya yönelik bazı algoritmalar (her hedef destination (uç kimliği) için mi? her kaynak destination için mi? tüm yerel destination'lar için mi?) - etkileşimli akışlar için daha fazla optimizasyon (mevcut uygulamada odak çoğunlukla bulk (toplu) akışlarda) - I2PTunnel içinde yeni streaming lib özelliklerinin daha açık biçimde kullanılması, tunnel başına ek yükün azaltılması. - istemci düzeyinde bant genişliği sınırlaması (bir akışta tek yönde ya da her iki yönde, veya olası olarak birden fazla akış arasında paylaşımlı). Bu, elbette, router'ın genel bant genişliği sınırlamasına ek olacaktır. - destination'ların kabul ettikleri veya oluşturdukları akış sayısını kısabilmeleri için çeşitli kontroller (bazı temel kodlarımız var, ancak büyük ölçüde devre dışı) - erişim kontrol listeleri (yalnızca belirli ve bilinen diğer destination'lara giden veya onlardan gelen akışlara izin verme) - web kontrolleri ve çeşitli akışların sağlık durumunu izleme, ayrıca bunları açıkça kapatma veya kısma yeteneği

Hepiniz muhtemelen başka öneriler de getirebilirsiniz, ama bu sadece streaming lib (streaming kütüphanesi)’de görmeyi çok istediğim şeylerin kısa bir listesi; bunun için 0.4.2 sürümünü geciktirmeyeceğim. Bunlardan herhangi biriyle ilgilenen olursa, lütfen bana haber verin!

## 3) 0.4.2

Öyleyse, streaming lib (akış kütüphanesi) iyi durumdaysa, sürümü ne zaman çıkaracağız? Mevcut plan, bunu haftanın sonuna kadar yayınlamak; hatta belki yarın bile. Önce halletmek istediğim birkaç başka şey daha var ve elbette onların da test edilmesi gerekiyor, vesaire vesaire.

0.4.2 sürümündeki büyük değişiklik elbette yeni akış kitaplığı (streaming lib) olacak. API açısından, eski kitaplıkla aynıdır - I2PTunnel ve SAM akışları bunu otomatik olarak kullanır, ancak paket açısından geriye dönük uyumlu *değil*. Bu da bizi ilginç bir ikilemle bırakıyor - I2P içinde 0.4.2'yi zorunlu bir yükseltmeye dönüştürmemizi gerektiren hiçbir şey yok, ancak yükseltmeyenler I2PTunnel'ı kullanamayacak - eepsites(I2P Sites) yok, IRC yok, outproxy yok, e-posta yok. Uzun süredir bizimle olan kullanıcılarımızı yükseltmeye zorlayarak yabancılaştırmak istemiyorum, ama işe yarar her şeyin bozulmasına neden olup onları yabancılaştırmak da istemiyorum ;)

Her iki tarafa da ikna edilmeye açığım — 0.4.2 sürümünün daha eski sürümlerle iletişim kurmamasını sağlayacak şekilde tek bir kod satırını değiştirmek yeterince kolay olurdu; ya da olduğu gibi bırakırız ve insanlar her şeyin bozuk olduğundan yakınmaya web sitesine ya da foruma ne zaman gelseler o zaman yükseltirler. Siz ne düşünüyorsunuz?

## 4) AddressBook.py 0.3.1

Ragnarok, adres defteri uygulaması için yeni bir yama sürümü yayımladı - daha fazla bilgi için `http://ragnarok.i2p/` adresine bakın (ya da belki toplantıda bize bir güncelleme verebilir?).

## 5) ???

Biliyorum, BitTorrent bağlantı noktası, susimail, slacker'ın yeni barındırma hizmeti ve daha pek çok şeyle ilgili epey hareketlilik var. Gündeme getirmek istediğiniz başka bir şey var mı? Varsa, yaklaşık 30 dakika sonra her zamanki IRC sunucularındaki #i2p kanalındaki toplantıya uğrayın!

=jr
