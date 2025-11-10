---
title: "I2P Geliştirici Toplantısı - 01 Haziran 2004"
date: 2004-06-01
author: "duck"
description: "01 Haziran 2004 tarihli I2P geliştirme toplantısı tutanağı."
categories: ["meeting"]
---

## Kısa özet

<p class="attendees-inline"><strong>Hazır bulunanlar:</strong> deer, duck, hypercubus, Masterboy, mihi, Nightblade, tessier, wilde</p>

## Toplantı Günlüğü

<div class="irc-log"> [22:59] &lt;duck&gt; Sal Haz  1 21:00:00 UTC 2004 [23:00] &lt;duck&gt; selam millet! [23:00] &lt;mihi&gt; merhaba duck [23:00] &lt;duck&gt; http://dev.i2p.net/pipermail/i2p/2004-June/000250.html [23:00] &lt;duck&gt; önerim: [23:00] * Masterboy #i2p kanalına katıldı

[23:00] &lt;duck&gt; 1) kod ilerlemesi
[23:00] &lt;duck&gt; 2) öne çıkan içerik
[23:00] &lt;duck&gt; 3) testnet durumu
[23:00] &lt;duck&gt; 4) ödül programları
[23:00] &lt;duck&gt; 5) ???
[23:00] &lt;Masterboy&gt; merhaba:)
[23:00] &lt;duck&gt; .
[23:01] &lt;duck&gt; jrandom yok olduğuna göre bunu kendimiz yapmak zorundayız
[23:01] &lt;duck&gt; (Günlük tuttuğunu ve bağımsızlığımızı doğruladığını biliyorum)
[23:01] &lt;Masterboy&gt; sorun değil:P
[23:02] &lt;duck&gt; gündemle ilgili bir sorun yoksa, ona bağlı kalmayı öneriyorum
[23:02] &lt;duck&gt; yine de uymayacaksanız yapabileceğim pek bir şey yok :)
[23:02] &lt;duck&gt; .
[23:02] &lt;mihi&gt; ;)
[23:02] &lt;duck&gt; 1) kod ilerlemesi
[23:02] &lt;duck&gt; cvs'ye pek fazla kod gönderilmedi
[23:02] &lt;duck&gt; Bu hafta kupayı ben kazandım: http://duck.i2p/duck_trophy.jpg
[23:03] * hypercubus'un henüz cvs hesabı yok
[23:03] &lt;Masterboy&gt; peki kim bir şey gönderdi?
[23:03] &lt;duck&gt; gizlice kod yazan var mı?
[23:03] * Nightblade #I2P kanalına katıldı

[23:03] &lt;hypercubus&gt; BrianR bazı şeyler üzerinde çalışıyordu
[23:04] &lt;hypercubus&gt; 0.4 yükleyicinin belki %20'sini kaba taslak hallettim
[23:04] &lt;duck&gt; hypercubus: eğer elinde bir şeyler varsa diff'leri sağla, $dev senin adına commit eder
[23:04] &lt;duck&gt; tabii ki katı lisans sözleşmeleri geçerli
[23:05] &lt;duck&gt; hypercubus: harika, herhangi bir sorun / bahsetmeye değer bir şey var mı?
[23:06] &lt;hypercubus&gt; henüz değil, ama muhtemelen preinstaller (ön yükleyici) kabuk betiklerini test etmek için birkaç BSD kullanan kişiye ihtiyacım olacak
[23:06] * duck birkaç taşı ters çevirir
[23:06] &lt;Nightblade&gt; yalnızca metin mi
[23:07] &lt;mihi&gt; duck: duck_trophy.jpg üzerinde hangisi sensin?
[23:07] &lt;mihi&gt; ;)
[23:07] &lt;Nightblade&gt; luckypunk'ta freebsd var, ayrıca ISS'imde de freebsd var ama yapılandırmaları biraz bozuk
[23:07] &lt;Nightblade&gt; yani web barındırıcım olan ISS, comcast değil
[23:08] &lt;duck&gt; mihi: gözlüklü soldaki. wilde, sağdaki bana kupayı uzatan kişi
[23:08] * wilde el sallar
[23:08] &lt;hypercubus&gt; seçeneklerin var... Java yüklüyse preinstaller'ı tamamen atlayabilirsin...    Java yüklü değilse linux ikili (binary) veya win32 ikili (binary) preinstaller'ı (konsol modu) çalıştırabilir ya da    genel bir *nix betik preinstaller'ı (konsol modu) çalıştırabilirsin
[23:08] &lt;hypercubus&gt; ana yükleyici sana konsol modunu veya havalı GUI modunu kullanma seçeneği sunuyor
[23:08] &lt;Masterboy&gt; yakında freebsd kuracağım, bu yüzden ileride yükleyiciyi de denerim
[23:09] &lt;hypercubus&gt; tamam, güzel... jrandom dışında onu kullanan başka biri var mı bilmiyordum
[23:09] &lt;Nightblade&gt; freebsd'de Java, "java" yerine "javavm" olarak çağrılır
[23:09] &lt;hypercubus&gt; sun kaynaklarından derlenen sürüm mü?
[23:09] &lt;mihi&gt; freebsd symlink'leri (sembolik bağlar) destekler ;)
[23:10] &lt;hypercubus&gt; neyse, ikili (binary) preinstaller %100 tamam
[23:10] &lt;hypercubus&gt; gcj ile yerel (native) olarak derleniyor
[23:11] &lt;hypercubus&gt; sadece sizden kurulum dizinini istiyor ve sizin için bir JRE alıyor
[23:11] &lt;duck&gt; w00t
[23:11] &lt;Nightblade&gt; güzel
[23:11] &lt;hypercubus&gt; jrandom, i2p için özel bir JRE paketliyor

[23:12] &lt;deer&gt; &lt;j&gt; .
[23:12] &lt;Nightblade&gt; freebsd ports koleksiyonundan java'yı yüklerseniz, javavm adlı    bir sarmalayıcı betik kullanırsınız
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;hypercubus&gt; her neyse, bu iş neredeyse tamamen otomatik olacak
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;deer&gt; &lt;duck&gt; r: kes
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;deer&gt; &lt;m&gt; .
[23:13] &lt;deer&gt; &lt;m&gt; aptal irc sunucusu, pipelining'i (istekleri ardışık iletme) desteklemiyor :(
[23:13] &lt;duck&gt; hypercubus: bizim için bir tahmini zaman var mı?
[23:14] &lt;deer&gt; &lt;m&gt; oops, sorun şu: "Nick change too fast" :(
[23:14] &lt;hypercubus&gt; yine de bir aydan kısa sürede bitirmeyi bekliyorum, 0.4 sürüme hazır hale gelmeden önce
[23:14] &lt;hypercubus&gt; ama şu anda geliştirme sistemim için yeni bir işletim sistemi derliyorum, bu yüzden yükleyiciye geri dönmem    birkaç günü bulacak ;-)
[23:14] &lt;hypercubus&gt; yine de sorun yok
[23:15] &lt;duck&gt; tamam. o hâlde haftaya daha fazla haber var :)
[23:15] &lt;duck&gt; başka kodlama yapıldı mı?
[23:15] &lt;hypercubus&gt; umarım... tabii elektrik şirketi beni yine yarı yolda bırakmazsa
[23:16] * duck #2'ye geçer
[23:16] &lt;duck&gt; * 2) öne çıkan içerik
[23:16] &lt;duck&gt; bu hafta çok sayıda akışlı ses (ogg/vorbis) işi yapıldı
[23:16] &lt;duck&gt; baffled kendi egoplay akışını çalıştırıyor ve ben de bir akış çalıştırıyorum
[23:16] &lt;Masterboy&gt; ve oldukça iyi çalışıyor
[23:17] &lt;duck&gt; sitemizde nasıl kullanılacağına dair bilgi bulabilirsiniz
[23:17] &lt;hypercubus&gt; bizim için kabaca istatistik var mı?
[23:17] &lt;duck&gt; orada listelenmeyen bir oynatıcı kullanıyorsanız ve nasıl kullanılacağını çözdüyseniz, lütfen bana gönderin, ben de    eklerim
[23:17] &lt;Masterboy&gt; duck, sitende baffled'ın akışının bağlantısı nerede?
[23:17] &lt;Masterboy&gt; :P
[23:17] &lt;duck&gt; hypercubus: 4kB/s gayet iyi gidiyor
[23:18] &lt;duck&gt; ve ogg ile o kadar da kötü değil
[23:18] &lt;hypercubus&gt; ama bu hâlâ ortalama hız gibi mi görünüyor?
[23:18] &lt;duck&gt; benim gözlemim bunun maksimum olduğu
[23:18] &lt;duck&gt; ama hepsi konfigürasyon ince ayarı
[23:19] &lt;hypercubus&gt; neden bunun maksimum gibi göründüğüne dair bir fikrin var mı?
[23:19] &lt;hypercubus&gt; ve burada sadece akıştan bahsetmiyorum
[23:19] &lt;hypercubus&gt; indirmeler de
[23:20] &lt;Nightblade&gt; dün duck'ın barındırma    hizmetinden birkaç megabaytlık bazı büyük dosyalar indiriyordum ve yaklaşık 4kb-5kb hız alıyordum
[23:20] &lt;duck&gt; bence bu rtt (gidiş-dönüş süresi)
[23:20] &lt;Nightblade&gt; şu Chips filmleri
[23:20] &lt;hypercubus&gt; i2p kullanmaya başladığımdan beri sürekli aldığım ~3'e göre 4-5 bir iyileşme gibi görünüyor

[23:20] &lt;Masterboy&gt; 4-5kb fena değil..
[23:20] &lt;duck&gt; windowsize 1 ile pek hızlanamazsın..
[23:20] &lt;duck&gt; windowsize&gt;1 ödülü: http://www.i2p.net/node/view/224
[23:21] &lt;duck&gt; mihi: belki yorum yapabilirsin?
[23:21] &lt;hypercubus&gt; ama dikkat çekici şekilde tutarlı 3 kbps
[23:21] &lt;mihi&gt; ne hakkında? ministreaming ile windowsize&gt;1: bunu başarırsan büyücüsün ;)
[23:21] &lt;hypercubus&gt; bant genişliği ölçerinde hiç aksama yok... oldukça düzgün bir çizgi
[23:21] &lt;duck&gt; mihi: neden 4kb/s'te bu kadar stabil olduğu hakkında
[23:21] &lt;mihi&gt; fikrim yok. hiç ses duymuyorum :(
[23:22] &lt;duck&gt; mihi: tüm i2ptunnel aktarımları için
[23:22] &lt;Masterboy&gt; mihi ogg streaming eklentisini yapılandırman gerekiyor..
[23:22] &lt;mihi&gt; Masterboy:?
[23:23] &lt;mihi&gt; hayır, hız konusunda i2ptunnel içinde bir sınır yok. router'da olmalı...
[23:23] &lt;duck&gt; benim düşüncem: maksimum paket boyutu: 32kB, 5 saniyelik RTT: 32kB/5s =~ 6.5kb/s
[23:24] &lt;hypercubus&gt; kulağa makul geliyor
[23:25] &lt;duck&gt; tamam..
[23:25] &lt;duck&gt; diğer içerik:
[23:25] * hirvox #i2p kanalına katıldı

[23:25] <duck> Naughtious'tan yeni bir eepsite var
[23:25] <duck> anonynanny.i2p
[23:25] <duck> anahtar CVS'ye commit edildi ve ugha'nın wiki'sine koydu
[23:25] * mihi "sitting in the ..." duyuyor - duck++
[23:25] <Nightblade> 4 kb hızda iki ya da üç akış açabiliyor musun bir bak; o zaman bunun router'da mı yoksa streaming kütüphanesinde mi olduğunu anlayabilirsin
[23:26] <duck> Naughtious: orada mısın? planın hakkında biraz anlat :)
[23:26] <Masterboy> barındırma sağladığını okudum
[23:26] <duck> Nightblade: baffled'dan 3 paralel indirme denedim ve her biri 3-4 kB verdi
[23:26] <Nightblade> anladım
[23:27] <mihi> Nightblade: peki bunu nasıl anlayabiliyorsun?
[23:27] * mihi 'stop&go' modunda dinlemeyi seviyor ;)
[23:27] <Nightblade> şey, router'da aynı anda yalnızca 4 kb işlemeye izin veren bir tür sınırlama varsa
[23:27] <Nightblade> ya da başka bir şeyse
[23:28] <hypercubus> bu anonynanny sitesini biri açıklayabilir mi? şu anda çalışan bir I2P router'ım yok
[23:28] <mihi> hypercubus: sadece bir wiki ya da ona benzer bir şey
[23:28] <duck> Plone CMS kurulumu, açık hesap oluşturma
[23:28] <duck> dosya yüklemeye ve web sitesi işlerine izin veriyor
[23:28] <duck> web arayüzü üzerinden
[23:28] <Nightblade> başka yapılacak şey, "repliable datagram"ın (yanıtlanabilir datagram) verimini test etmek olur; bildiğim kadarıyla akışlarla aynı ama onay (ack) yok
[23:28] <duck> muhtemelen Drupal'a çok benziyor
[23:28] <hypercubus> evet, daha önce Plone çalıştırdım
[23:29] <duck> Nightblade: bunları yönetmek için airhook kullanmayı düşünüyordum
[23:29] <duck> ama şimdilik sadece bazı temel düşünceler
[23:29] <hypercubus> wiki içeriği için her şey serbest mi, yoksa özellikle odaklandığı bir şey var mı?
[23:29] <Nightblade> airhook'un GPL lisanslı olduğunu düşünüyorum
[23:29] <duck> protokolü
[23:29] <duck> kodu değil
[23:29] <Nightblade> ah :)
[23:30] <duck> hypercubus: kaliteli içerik istiyor ve bunu sağlamana izin veriyor :)
[23:30] <Masterboy> kendine ait en iyi pr0n'u yükle hyper ;P
[23:30] <duck> tamam
[23:30] * Masterboy bunu yapmayı da deneyecek
[23:30] <hypercubus> evet, açık bir wiki çalıştıran herkes resmen kaliteli içerik istiyor demektir ;-)
[23:31] <duck> tamam
[23:31] * duck #3'e geçiyor
[23:31] <duck> * 3) testnet durumu
[23:31] <Nightblade> Airhook kesintili, güvenilmez veya gecikmeli ağları zarifçe idare eder  <-- hehe I2P için pek iyimser bir tanım değil!
[23:31] <duck> nasıl gidiyor?
[23:32] <duck> datagram over i2p tartışmasını sona bırakalım
[23:32] <tessier> Açık wikilerde dolaşıp şuna link vermeyi seviyorum: http://www.fissure.org/humour/pics/squirre   l.jpg
[23:32] <tessier> airhook harika
[23:32] <tessier> onu bir p2p ağ kurmak için de inceliyordum.
[23:32] <Nightblade> bana güvenilir görünüyor (#3)
[23:32] <Nightblade> şimdiye kadar gördüğüm en iyisi
[23:33] <duck> evet
[23:33] <mihi> iyi çalışıyor - en azından stop&go ses akışı için
[23:33] <duck> irc'de oldukça etkileyici çalışma süreleri görüyorum
[23:33] <hypercubus> katılıyorum... router konsolumda çok daha fazla mavi adam görüyorum
[23:33] <Nightblade> mihi: techno mu dinliyorsun? :)
[23:33] <duck> ama söylemesi zor, çünkü bogobot 00:00'ı geçen bağlantıları idare edemiyor gibi görünüyor
[23:33] <tessier> bende ses akışı harika çalışıyor ama web sitelerini yüklemek çoğu zaman birkaç deneme gerektiriyor
[23:33] <Masterboy> bence i2p 6 saatlik kullanımdan sonra çok iyi çalışıyor; 6. saatte irc'yi 7 saat kullandım ve böylece router'ım 13 saat çalışmış oldu
[23:33] <duck> (*ipucu*)
[23:34] <hypercubus> duck: ıı... heheh
[23:34] <hypercubus> sanırım onu düzeltebilirim
[23:34] <hypercubus> günlüklemeyi günlük (daily) olarak mı ayarladın?
[23:34] <duck> hypercubus++
[23:34] <hypercubus> yani log döndürme
[23:34] <duck> ah evet
[23:34] <duck> duck--
[23:34] <hypercubus> bu yüzden
[23:34] <Nightblade> bütün gün işteydim, bilgisayarımı açtım, i2p'yi başlattım ve sadece birkaç dakika içinde duck'ın irc sunucusundaydım
[23:35] <duck> bazı garip DNF'ler görüyorum
[23:35] <duck> kendi eepsite'lerime bağlanırken bile
[23:35] <duck> (http://dev.i2p.net/bugzilla/show_bug.cgi?id=74)
[23:35] <duck> sanırım şu anda sorunların çoğuna bunun sebep olduğu
[23:35] <hypercubus> bogoparser yalnızca tamamen tek bir log dosyası içinde gerçekleşen çalışma sürelerini analiz edecek... yani log dosyası yalnızca 24 saati kapsıyorsa, hiç kimse 24 saatten uzun bağlı görünmeyecek
[23:35] <duck> Masterboy ve ughabugha'da da vardı sanırım...
[23:36] <Masterboy> evet
[23:36] <duck> (onu düzelt ve gelecek haftanın kupasını kesin kazanırsın!)
[23:37] <deer> <mihi> bogobot heyecanlı mı? ;)
[23:37] <Masterboy> web sitemi denedim ve bazen yenile'ye bastığımda başka rotayı mı alıyor? yüklemesini beklemem gerekiyor ama asla beklemiyorum ;P tekrar basıyorum ve anında geliyor
[23:37] <deer> <mihi> ups, üzg. bunun geçitli olduğunu unuttum...
[23:38] <duck> Masterboy: zaman aşımı 61 saniye mi sürüyor?
[23:39] <duck> mihi: bogobot şimdi haftalık döndürmeye ayarlandı
[23:39] * mihi IRC'den çıktı ("görüşürüz, iyi toplantılar")
[23:40] <Masterboy> üzgünüm, web sitemde kontrol etmedim; anında ulaşamazsam sadece yenile'ye basıyorum ve anında yükleniyor..
[23:40] <duck> hm
[23:40] <duck> neyse, bunun düzeltilmesi gerekiyor
[23:41] <duck> .... #4
[23:41] <Masterboy> bence rota her seferinde aynı verilmiyor
[23:41] <duck> * 4) ödüller
[23:41] <duck> Masterboy: yerel bağlantılar kısa kesilmeli
[23:42] <duck> wilde'ın bazı ödül fikirleri vardı... orada mısın?
[23:42] <Masterboy> belki bu bir peer (eş) seçimi hatasıdır
[23:42] <wilde> bunun gerçekten gündem için olduğundan emin değilim
[23:42] <duck> oh
[23:42] <wilde> tamam ama düşünceler şöyleydi:
[23:42] <Masterboy> bence halka açıldığımızda ödül sistemi daha iyi işleyecek
[23:43] <Nightblade> masterboy: evet, her bağlantı için iki tunnel var; en azından router.config'i okuduğumdan anladığım bu
[23:43] <wilde> bu ayı i2p'nin küçük tanıtımını yapmak ve ödül havuzunu biraz artırmak için kullanabiliriz
[23:43] <Masterboy> Mute projesinin iyi gittiğini görüyorum - 600$ aldılar ve daha çok da kod yazmadılar ;P
[23:44] <wilde> özgürlük topluluklarını, kripto insanlarını vb. hedefleyelim
[23:44] <Nightblade> jrandom'ın tanıtım istediğini sanmıyorum
[23:44] <wilde> genel Slashdot ilgisi değil, hayır
[23:44] <hypercubus> benim de gözlemlediğim bu
[23:44] <Masterboy> bunu yine de öne çıkarmak istiyorum - halka açıldığımızda sistem çok daha iyi çalışacak ;P
[23:45] <wilde> Masterboy: ödüller örneğin myi2p geliştirmesini hızlandırabilir
[23:45] <Masterboy> ve jr'ın dediği gibi 1.0'a kadar halka açık yok ve yalnızca 0.4'ten sonra biraz ilgi
[23:45] <Masterboy> *yazdı
[23:45] <wilde> bir ödül için 500$+ gibi bir rakamımız olduğunda, insanlar gerçekten birkaç hafta idare edebilir
[23:46] <hypercubus> zor olan şu ki, küçük bir geliştirici topluluğunu hedeflesek bile, hani öhöm Mute geliştiricileri gibi, bu adamlar i2p hakkında bizim istediğimizden daha fazla yayabilir
[23:46] <Nightblade> birisi i2p hatalarını düzelterek kariyer yapabilir
[23:46] <hypercubus> hem de çok erken
[23:46] <wilde> i2p bağlantıları zaten birçok kamusal yerde var
[23:46] <Masterboy> Google'da ararsın ve i2p'yi bulursun

[23:47] <hypercubus> gözden ırak halka açık yerler ;-) (bir freesite (Freenet üzerindeki site) üzerinde i2p bağlantısını gördüm... şu lanet freesite'ın    yüklenmesi bile şans!)
[23:47] <wilde> http://en.wikipedia.org/wiki/I2p
[23:47] <Masterboy> ama 0.4 bitene kadar reklam yok konusunda hemfikirim
[23:47] <Masterboy> neee???????
[23:47] <wilde> http://www.ovmj.org/GNUnet/links.php3?xlang=English
[23:48] <Masterboy> protol0l harika iş çıkarıyor ;P
[23:48] <Masterboy> ;))))))
[23:48] <hypercubus> güzel yazım hatası ;-)
[23:48] <wilde> tamam neyse, I2P'yi hâlâ özel tutmamız gerektiğine katılıyorum (jr bu günlüğü okusun ;)
[23:49] <Masterboy> bunu kim yaptı?
[23:49] <Masterboy> bence Freenet ekibinin tartışması daha fazla dikkat çekti..
[23:50] <Masterboy> ve jr'nin toad ile tartışması geniş kitleye çok bilgi verdi..
[23:50] <Masterboy> yani ughas wiki'sinde olduğu gibi - bunun için hepimiz jr'yi suçlayabiliriz ;P
[23:50] <wilde> tamam neyse, /. getirmeden biraz $ getirebilir miyiz, göreceğiz.
[23:50] <Masterboy> katılıyorum
[23:50] <hypercubus> freenet geliştirici listesi benim "geniş kitle" dediğim şey pek değil ;-)
[23:50] <wilde> .
[23:51] <hypercubus> wilde: düşündüğünden daha yakında çok $'ın olacak ;-)
[23:51] <wilde> aman hadi ama, annem bile freenet-devl'e abone
[23:51] <duck> annem gmame üzerinden okuyor
[23:51] <deer> <clayboy> burada okullarda freenet-devl öğretiliyor
[23:52] <wilde> .
[23:52] <Masterboy> yani 0.4 stabil olduktan sonra daha fazla ödül göreceğiz..
[23:53] <Masterboy> yani 2 ay sonra ;P
[23:53] <wilde> o duck nereye gitti?
[23:53] <duck> teşekkürler wilde  
[23:53] <hypercubus> şu ana kadar tek ödül talep eden olarak, şunu söylemeliyim ki ödül parası bu meydan okumayı üstlenme kararım üzerinde    hiçbir etkisi olmadı
[23:54] <wilde> hehe, 100 katı olsaydı olurdu
[23:54] <duck> wsen bu dünya için fazla iyisin
[23:54] <Nightblade> haha
[23:54] * duck #5'e taşınır
[23:54] <hypercubus> wilde, $100 benim için hiçbir şey ifade etmiyor ;-)
[23:54] <duck> 100 * 10 = 1000
[23:55] * duck pops("5 airhook")
[23:55] <duck> tessier: bununla ilgili gerçek dünya deneyimin var mı
[23:55] <duck> (http://www.airhook.org/)
[23:55] * Masterboy bunu deneyecek :P
[23:56] <duck> java implementasyonu (çalışıp çalışmadığını bilmiyorum) http://cvs.ofb.net/airhook-j/
[23:56] <duck> python implementasyonu (dağınık, geçmişte çalışıyordu) http://cvs.sourceforge.net/viewcvs.py/khashmir   /khashmir/airhook.py
[23:58] * duck söylenme-vanasını açar
[23:58] <Nightblade> j olanı da gpl
[23:58] <duck> public domain'e (kamu malı) port et
[23:58] <hypercubus> amin
[23:58] <Nightblade> protokol dokümanının tamamı yaklaşık 3 sayfa - o kadar zor olamaz
[23:59] <Masterboy> hiçbir şey zor değildir
[23:59] <Masterboy> sadece kolay değil
[23:59] <duck> yine de tam olarak tanımlandığını sanmıyorum
[23:59] * hypercubus masterboy'un şans kurabiyelerini alır
[23:59] <duck> başvuru uygulaması için C koduna dalman gerekebilir
[00:00] <Nightblade> ben kendim yapardım ama şu anda diğer i2p işleriyle meşgulüm
[00:00] <Nightblade> (ve ayrıca tam zamanlı işim)
[00:00] <hypercubus> duck: belki bunun için bir ödül?
[00:00] <Nightblade> zaten var
[00:00] <Masterboy> ?
[00:00] <Masterboy> ahh Pseudonyms
[00:00] <duck> 2 düzeyde kullanılabilir
[00:00] <duck> 1) TCP dışında bir transport (taşıma) olarak
[00:01] <duck> 2) i2cp/sam içinde datagramları işlemek için bir protokol olarak
[00:01] <hypercubus> o zaman bu ciddi biçimde düşünmeye değer
[00:01] <hypercubus> </obvious>

[00:02] &lt;Nightblade&gt; duck: SAM içindeki repliable datagram (yanıtlanabilir datagram) için azami boyutun 31kb olduğunu fark ettim,    stream için ise azami boyut 32kb - bu da bana, repliable datagram kipinde her pakette gönderenin destination'ının (hedef adresi) gönderildiğini,    stream kipinde ise yalnızca başlangıçta gönderildiğini düşündürüyor -
[00:02] &lt;Masterboy&gt; şey, airhook cvs pek güncel değil..
[00:03] &lt;Nightblade&gt; bu da sam üzerinden repliable    datagrams’ın üzerine bir protokol koymanın verimsiz olacağını düşündürüyor
[00:03] &lt;duck&gt; airhook’un mesaj boyutu 256 bayt, i2cp’ninki 32kb, yani en azından biraz değiştirmen gerekir
[00:04] &lt;Nightblade&gt; aslında protokolü SAM içinde yapmak isteseydin,    anoymous datagram’ı kullanıp ilk paketin gönderenin destination’ını içermesini sağlayabilirdin.... falan filan - bir sürü fikrim var ama    onları kodlamak için yeterince zamanım yok
[00:06] &lt;duck&gt; öte yandan imzaları doğrulamakta da sorunların olur
[00:06] &lt;duck&gt; yani biri sana sahte paketler gönderebilir
[00:06] &lt;Masterboy&gt; konu:::: SAM
[00:06] &lt;Masterboy&gt; ;P
[00:07] &lt;Nightblade&gt; doğru
[00:08] &lt;Nightblade&gt; ama o destination’a geri gönderir ve bir alındı gelmezse, bunun    sahteci olduğunu anlarsın
[00:08] &lt;Nightblade&gt; bir el sıkışma (handshake) olması gerekir
[00:08] &lt;duck&gt; ama bunun için uygulama seviyesinde el sıkışmalarına ihtiyacın olacak
[00:08] &lt;Nightblade&gt; hayır, pek değil
[00:09] &lt;Nightblade&gt; sadece SAM’e erişmek için bir kütüphaneye koy
[00:09] &lt;Nightblade&gt; ama bu işi yapmanın kötü bir yolu
[00:09] &lt;Nightblade&gt; yani öyle yapmak
[00:09] &lt;duck&gt; ayrıca ayrı tunnel’lar da kullanabilirsin
[00:09] &lt;Nightblade&gt; bu, streaming lib içinde olmalı
[00:11] &lt;duck&gt; evet. mantıklı
[00:12] &lt;duck&gt; tamam
[00:12] &lt;duck&gt; kendimi *baff*-lı hissediyorum
[00:13] &lt;Nightblade&gt; ja
[00:13] * duck *baffs* </div>
