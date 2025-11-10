---
title: "I2P geliştirici toplantısı, 4 Eylül 2002"
date: 2002-09-04
author: "nop"
description: "Proje güncellemeleri ve teknik tartışmaları içeren I2P geliştirme toplantısı"
categories: ["meeting"]
---

(Wayback Machine'in katkılarıyla http://www.archive.org/)

## Kısa bir özet

<p class="attendees-inline"><strong>Hazır bulunanlar:</strong> ArdVark, athena, gabierOQP, legabier, mids, nop, Sheige</p>

## Toplantı Günlüğü

<div class="irc-log"> --- Günlük açıldı Tue Sep 03 23:55:46 2002
 23:56 <@mids> test
 --- Gün değişti Wed Sep 04 2002
 00:34 < athena> merhaba :)
 00:34 < athena> bugün özel bir gündem yok mu?
 00:36 -!- mode/#iip-dev [+o nop] by mids
 00:36 -!- mode/#iip-dev [+v logger] by mids
 00:36 <@mids> henüz değil en azından
 00:55 < athena> OQP... sevimli :)
 00:56 <@mids> OQP nedir?
 00:56 < athena> sanırım 'occupé'
 00:56 <@mids> anladım
 00:58 < gabierOQP> OQP=Fransızcada occupé
 00:58 < gabierOQP> meşgul
 00:58 -!- gabierOQP artık legabier olarak biliniyor
 00:59 <@mids> anlaşıldı
 01:00 <@mids> Tue Sep  3 23:00:00 UTC 2002
 01:00 <@mids> 10. IIP toplantısına hoş geldiniz
 01:00 <@mids> Gündem:
 01:00 <@mids> 1) Hoş geldiniz
 01:00 <@mids> 2) Web sitesi durum güncellemesi
 01:00 <@mids> 3) ...
 01:00 <@mids> a) Sorular
 01:00 <@mids> .
 01:00 <@mids> 1. maddeye geçelim
 01:00 <@mids> hepiniz hoş geldiniz
 01:00 < legabier> freenet neden bu kadar yavaş ve iip neden bu kadar hızlı?
 01:01 <@mids> legabier: bunu a kısmına kadar erteleyebilir miyiz?
 01:01 < legabier> ok
 01:01 <@mids> bölüm 2
 01:01 <@mids> nop: durum güncellemesi?
 01:02 <@mids> hımm
 01:02 <@mids> web sitesi CVS'de
 01:02 <@mids> nop dosyaları gözden geçirdi
 01:03 <@mids> ama iyi metni olmayan bazı kısımlar var
 01:03 <@mids> ve destek alanının daha iyi bir düzenine ihtiyaç var
 01:03 <@mids> onun dışında bitti
 01:03 <@mids> site ne zaman yayında olacak söylemeyeceğim
 01:03 <@mids> ama çevrimiçi olma zamanı üzerine özel bahisler yapmada özgürsünüz :)
 01:04 <@mids> .
 01:04 <@mids> nop'un muhtemelen ekleyeceği bir şey vardır
 01:04 <@mids> 3 dakika falan bekleyelim
 01:06 < athena> lol
 01:06 <@mids> sanırım nop yanıt veremeyecek kadar web sitesini düzenlemekle meşgul
 01:06 <@mids> peki tamam...
 01:06 <@mids> soru turuna geçmeden önce.. konuşmamız gereken başka maddeler var mı?
 01:08 <@mids> sanırım yok :-)
 01:08 <@mids> Herkes aynı fikirde olduğunda hoşuma gidiyor :)
 01:08 <@mids> .
 01:08 <@mids> legabier'den soru: "freenet neden bu kadar yavaş ve iip neden bu kadar hızlı?"
 01:08 <@mids> freenet farklı bir programdır, IIP ile Freenet arasında teknik bir ilişki yoktur
 01:08 <@mids> Freenet tamamen merkezsizdir.. IIP değil (henüz)
 01:08 <@nop> haha
 01:09 <@mids> Freenet dosya transferi için tasarlanmıştır, oysa IIP üzerinden IRC kısa satırlar kullanır
 01:09 <@nop> freenet merkezsiz diye
 01:09 <@nop> IIP'nin hızlı olmasının nedeni bu değil
 01:09 <@mids> peki, bizi aydınlat, ey usta yoda :)
 01:10 <@nop> farklar
 01:10 <@nop> freenet == yüksek hacim, düşük hız, statik (arşivlenmiş) içerik
 01:10 <@nop> iip == düşük hacim, yüksek hız, dinamik içerik
 01:10 <@nop> tamamen farklı kavramlar, merkezî ya da merkezsiz fark etmez, IIP hızlı kalacaktır
 01:11  * mids bunun da böyle olmasını umar
 01:11  * nop bunu bilir
 01:11 <@mids> tamam
 01:11 <@mids> bu sorunu yanıtlıyor mu legabier?
 01:12 < legabier> evet, merci :)
 01:13  * mids seyircilerin üzerine spotu çevirir.. bir sonraki soru ve/veya yorumu arar
 01:13 < athena> nop'un çalıştırdıkları ve mids'inki dışında neden bu kadar az public relay (genel aktarıcı düğüm) var? genelde yalnızca 2 ya da 3 tane daha görüyorum. gönüllümüz yok mu yoksa uptime denetleyicisi bunların çoğunu reddediyor mu?
 01:13 < Sheige> Bende onlardan 8 tane var.... sanırım
 01:14 < Sheige> (yine de az)
 01:14 < athena> mids ve nop'unkileri saymazsan bu kaç eder?
 01:14 <@mids> 5
 01:14 <@mids> kaynak: http://invisiblenet.net/iip/crypto/node.ref
 01:15 < athena> hmmm, tamam... sanırım yenisini indirmem gerekiyor... yine de, 20 kadar public node (genel düğüm) güzel olurdu :)
 01:15 <@mids> Ben _sanıyorum_ ki uptime denetleyicisi biraz fazla katı
 01:16 <@mids> ağ kapalıyken bir süre önce codeshark onu duraklatmak zorunda kaldı
 01:16 <@mids> yoksa tüm relay'leri dışarı atardı
 01:17 <@nop> katı denetim iyi bir şey
 01:17 <@nop> çalışmayan çok sayıda relay'in olsaydı daha fazla sorun yaşardın
 01:17 <@nop> sağlam relay bağlantısına sahip daha az sayıda olması daha iyidir
 01:17 <@mids> nop: şey.. ama yeniden duyurular çalışıyor gibi görünmüyor
 01:17 <@nop> bir sürü berbat olan yerine
 01:17 <@nop> evet, çalışıyorlar
 01:17 <@mids> hımm
 01:17 <@nop> sadece zaman alıyor
 01:17 <@nop> ayrıca bir relay isen rotanı görmezsin
 01:17 <@mids> o zaman neden sadece 7 tane var :)
 01:17 <@nop> relay'lerin istikrarı yüzünden
 01:18 <@nop> görünmeleri birkaç gün daha sürebilir
 01:20 <@nop> bu konuda codeshark ile konuş
 01:20 <@nop> onun daha fazla detayı olur
 01:20 <@nop> bunu onunla test edeceğim
 01:20 <@mids> tamam
 01:21 <@mids> sanırım relay'ime bağlanan düğüm sayısı bir şekilde fazla
 01:21 <@mids> ama belki de bildiğimizden çok daha fazla kullanıcı var :)
 01:21 < athena> kaç bağlantın var?
 01:22 <@mids> bunu söylemeli miyim bilmiyorum
 01:22  * mids arka kanaldan biraz konuşur
 01:22 < athena> en iyi erişilebilen relay sen olabilirsin
 01:22 <@mids> heh, son zamanlardaki istikrarsızlıkla bunu söyleyemem
 01:22 < athena> node.ref içindeki hostların yarısı üzerinden bağlanamadığımı sık sık görüyorum
 01:22 < athena> ve 7 ile başladığında bu pek fazla güvenilir relay demek değil
 01:23 <@nop> şey, açık olanların çoğu genelde öyledir
 01:23 < athena> sadece kendi deneyimimi aktarıyorum...
 01:24 <@nop> belki bu daha yeni
 01:25 <@mids> çalışma süresini (uptime) ölçmek ilginç olurdu...
 01:25 <@mids> ama...
 01:25 < athena> bunu topolojik olarak çeşitli konumlardan ölçmeniz gerekir
 01:27 <@mids> nop: buna karşı olur musun?
 01:27 <@mids> bu iş tamamen anonimlikle ilgili olmasaydı, bir sürü istatistik görmeyi çok isterdim :)
 01:27 <@nop> ıı, saldırı bilgisi ortaya çıkarıyorsa, evet
 01:28 <@nop> belki sonra anonim olmayan bir weary sistem kurar ve istatistik toplarız
 01:28 < athena> kamuya açık olan tüm istatistiklerin yayımlanması GEREKTİĞİNİ söylerdim
 01:28 <@nop> özellikle büyüdükçe
 01:28 < athena> bilgiyi gizli tutmaya değil, IIP'nin güvenliğine güvenin
 01:28 <@nop> şey athena, biri istatistik topluyorsa, yayımlanmalı
 01:28 <@nop> ama şu ana kadar kimse toplamıyor
 01:28 <@nop> toplayan varsa lütfen bulgularınızı yayımlayın
 01:28 <@nop> ;)
 01:29 < athena> belki ben yaparım :p
 01:29 <@mids> peki.. istatistikleri "adil" bir şekilde toplamaya çalışacağım
 01:29 <@mids> public node yetkilerimi kötüye kullanmadan
 01:29 <@mids> bu şekilde toplayabildiğim her şeyi herkes toplayabilir
 01:29 < athena> tam olarak kastettiğim buydu, harika
 01:30 < ArdVark> neden public node gücünü kötüye kullanmıyor ve bunun neleri içerdiğini de bize göstermiyorsun, mids?
 01:30 <@mids> şimdi eğer IIP sohbet sisteminden kaybolursam... bunun sebebi birinin benim istatistikleri toplamamdan hoşlanmaması ;)
 01:30 <@mids> ArdVark: belki bu bir sonraki adımdır...
 01:30 < athena> ArdVark: lol, müthiş nokta! zaten herkes bir public node olabilir...
 01:30 < athena> s/anyway/anyone/
 01:31 <@mids> athena: bir public relay kur ve sen yap :)
 01:31 < ArdVark> bu canavarın başarısızlıklarının da başarıları gibi raporlanmasını istiyorum
 01:32 <@mids> bağlantıları kaydetmek için public relay çalıştıran 100 "ajans"ımız olsa harika olurdu, ama bu arada anonimliği artırmaya da yardımcı olurlar
 01:33 < ArdVark> farklı bir konu, mevcut olanı bitirmemek adına: invisiblnet'e wiki eklemeyi hiç düşündünüz mü? yoksa çok mu zahmetli?
 01:33 <@mids> wiki derken wikiwiki mi?
 01:33 < ArdVark> evet
 01:33 <@mids> şu $#@&%@ infobot'lar zaten bir çeşit wiki
 01:33 < athena> mids: zaten bir public relay çalıştırmadığımı nereden biliyorsun ;)
 01:34 < ArdVark> o infobot'ları seviyorum mids   ;)
 01:34 <@mids> ArdVark: biliyorum, seviyorsun
 01:34 <@mids> ArdVark: IIP'in 'arkasına' bir web sunucusu koyarsan... üzerine bir wiki kurabilirsin
 01:35 < ArdVark> tamam, sanırım bu makul
 01:35 <@mids> ama IRC üzerinden web sunucusu çalıştırmak pek harika değil
 01:35 < ArdVark> hayır, web sitesini kastettim
 01:35 <@mids> oh
 01:35 <@mids> normal web sitesinde demek istiyorsun
 01:35 < ArdVark> evet
 01:36 <@mids> sanırım yapabilirsin
 01:36 <@mids> öte yandan.. herkese açık bir wiki de kullanabilirsin....
 01:36 < ArdVark> peki
 01:37 <@mids> bence wiki'yi gerçekten sourceforge'a kurmamalıyız.... şimdi değil
 01:37 <@mids> çünkü kurmak/ince ayar yapmak vs. biraz iş
 01:38 <@mids> ama birisi bir wiki çalıştırabilir ve IIP de ona işaret edebilir
 01:38 < ArdVark> tamam
 01:39 <@mids> ArdVark: ama belki IIP için (freenet'in şu an sahip olduğu gibi) herkese açık bir wiki en doğrusu
 01:39 <@mids> .
 01:39 < ArdVark> evet tamam
 01:41 <@mids> Ben yatıyorum. burada sohbet etmeye devam etmekten çekinmeyin :)
 01:41 < athena> iyi geceler mids
 01:49 <@mids> wiki ile oynamak isteyenler için: http://mids.student.utwente.nl/~mids/phpwiki/
 01:49 <@mids> onunla ne yaparsanız umurumda değil :)
 02:00 -!- mode/#iip-dev [+o codeshark] by Trent
 --- Günlük kapatıldı Wed Sep 04 07:03:17 2002 </div>
