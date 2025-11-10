---
title: "I2P geliştirici toplantısı"
date: 2003-07-15
author: "nop"
description: "Proje güncellemeleri ve teknik tartışmaların ele alındığı I2P geliştirme toplantısı"
categories: ["meeting"]
---

(Wayback Machine'in katkılarıyla http://www.archive.org/)

## Kısa özet

<p class="attendees-inline"><strong>Katılanlar:</strong> gott, hezekiah, jeremiah, jrand0m, mihi, Neo, nop, WinBear</p>

## Toplantı Günlüğü

<div class="irc-log"> --- Günlük açıldı Tue Jul 15 17:46:47 2003 17:46 < gott> selam. 17:46 <@nop> sessizliğimle ilgili ufak bir not 17:46 <@hezekiah> Tue Jul 15 21:46:49 UTC 2003 17:47 <@hezekiah> Tamam. iip-dev toplantısı başladı. 17:47 <@hezekiah> 48.si mi 49.su mu? 17:47 < jrand0m> nop> bu yüzden router 	mimarisini en kısa sürede netleştirmemiz kritik. Farklı insanların farklı 	hızlarda ilerlediğini anlıyorum ve farklı bileşenler buna göre ilerleyebilsin 	diye bölümlere ayırmalıyız 17:47 < mihi> 49. 17:47 <@hezekiah> Tamam! 49. iip-dev toplantısına hoş geldiniz! 17:47 < jrand0m> İşimde üç günüm daha var, bundan sonra haftada 90+ saatimi 	bunu hayata geçirmeye ayıracağım 17:48 < jrand0m> Herkesin bunu yapabilmesini beklemiyorum, işte bu yüzden 	bölmemiz gerekiyor 17:48 < jrand0m> selam hezekiah :) 17:48 <@hezekiah> lol 17:48 <@nop> buna itiraz olarak 17:48 <@hezekiah> Bir dakika bekleyeceğim. Sonra gündemi yapabiliriz. :) 17:48 <@nop> router mimarisinin güvenliği aynı zamanda acele etmemenize 	da bağlı 17:49 <@nop> acele edersek 17:49 <@nop> gözden kaçırırız 17:49 <@nop> bu da bizi ileride büyük bir dağınıklığı toparlamak zorunda 	bırakabilir 17:49 -!- Rain [Rain@anon.iip] çıkış yaptı [I Quit] 17:49 < jrand0m> nop> katılmıyorum. router'ı uygulamadan (hatta ağın nasıl 	çalışacağını bilmeden bile) uygulama katmanını ve API'leri yine de 	oluşturabiliriz 17:49 <@nop> Buna katılıyorum 17:50 <@nop> Özellikle alttaki ağdan bahsediyorum 17:50 < jrand0m> gönderdiğim API üzerinde anlaşabilirsek, ihtiyacımız 	olan bölümlendirme budur 17:50 < jrand0m> doğru, router implementasyonu ve ağ tasarımı hâlâ bitmedi 17:50 <@nop> tamam 17:50 <@nop> oh, şimdiye kadar API'ne kesinlikle katılıyorum 17:51 <@hezekiah> jrand0m: Bir sorun. 17:51 < jrand0m> söyle hezekiah 17:51 <@hezekiah> Bunu C'de uygularsan farklı görünecek. 17:51 < jrand0m> çok da farklı değil 17:51 < gott> eyvah 17:51 < jrand0m> daha az büyük harf ve nesneleri struct'larla değiştir 17:51 < gott> insanlar bunu hangi dillerde uygulamayı düşünüyor? 17:51 < jrand0m> (API için) 17:51 <@hezekiah> Şey, jrand0m? C'de 'byte[]' diye bir şey yok. 17:51 < jrand0m> gott> bununla ilgili örnek cevaplar için posta arşivlerini 	oku 17:52 <@hezekiah> Büyük olasılıkla uzunluğu belirtmek için bir tamsayıyla 	birlikte void* kullanacaksın. 17:52 < jrand0m> hezekiah> o zaman unsigned int[] 17:52 < gott> jrand0m: bir kez olsun, tarafı olmadığım bir din savaşı 17:52 <@hezekiah> Doğru hatırlıyorsam (burada bana yardım et nop), bir 	fonksiyondan öylece unsigned int[] döndüremezsin. 17:53 <@hezekiah> gott: neye karşılık? sözde kod mu? 17:53 < jrand0m> doğru, sözdizimsel değişiklikler. ama evet, gerçek 	farklılıklar varsa, onları en kısa sürede çözmemiz gerekiyor. (mesela bugün) 	Belki şimdi "high level router architecture and API" başlıklı gönderdiğim 	e-postaya bakıp gözden geçirmek için iyi bir zaman olur? 17:54 <@hezekiah> nop? UserX? Buna var mısınız? 17:54 < jrand0m> çok farklı değil ama yine de farklı, evet. bu yüzden 	bugünkü e-postada Java API dedim :) 17:54 -!- WinBear [WinBear@anon.iip] #iip-dev kanalına katıldı 17:55 <@nop> bekle 17:55 <@nop> yukarıyı okuyorum 17:55 -!- mihi_2 [~none@anon.iip] #iip-dev kanalına katıldı 17:55 -!- mihi şimdi olarak biliniyor nickthief60234 17:55 -!- mihi_2 şimdi olarak biliniyor mihi 17:55 < jrand0m> tekrar hoş geldin mihi 17:55 < gott> bu arada, bu canlı olarak mı kaydediliyor? 17:55 -!- nickthief60234 [~none@anon.iip] çıkış yaptı [EOF From client] 17:55 <@hezekiah> gott: Evet. 17:55 < mihi> yedeklilik kuraldır ;) 17:55 < gott> O zaman sonra okurum. 17:55 -!- gott [~gott@anon.iip] #iip-dev kanalından ayrıldı [gott] 17:56 <@nop> tamam 17:56 <@nop> evet 17:56 < WinBear> jrand0m: selam 17:56 <@nop> kesinlikle farklılıklar var 17:56 <@nop> ihtiyacımız olan 17:56 < jrand0m> selam WinBear 17:56 <@nop> bu diller için ana API düzeyi denetimleri yazacak belirli 	geliştiricilerden bir ekip 17:56 <@nop> jrand0m'un Java'yı halledebildiğini biliyoruz 17:56 <@nop> ve muhtemelen thecrypto ile de ekip olabilir 17:56 <@nop> ve hezekiah ve ekip C yapabilir 17:56 <@nop> ve isterse jeremiah 17:56 <@nop> Python yapabilir 17:56 <@hezekiah> C++ da yapabilirim! ;-) 17:56 <@nop> tamam 17:56 <@nop> C++ da 17:57 <@hezekiah> lol 17:57 <@nop> C++ muhtemelen çalışır 17:57 <@nop> C ile 17:57 <@nop> yeter ki olayı şablonlarla mahvetmeyin 17:57 < jrand0m> heh 17:57 <@hezekiah> lol 17:57 <@hezekiah> Aslında, MSVC C ve C++ nesne dosyalarını bağlayabiliyor 	ama gcc bundan pek hoşlanmıyor gibi. 17:57 <@nop> yani, C ile uyumlu struct'lara bağlı kalın, yoksa bu mümkün 	değil mi 17:57 < jrand0m> ilk soru, ondan önce, bu API'leri hangi uygulamalar 	kullanacak? Java kullanmak isteyecek uygulamalar biliyorum, iproxy C'de 	mi olacak? 17:58 <@hezekiah> nop: C ve C++ nesne düzeyinde uyumlu değil diye düşünüyorum. 17:58 <@nop> tamam 17:58 <@hezekiah> nop: C++'ın C ile anlaşması, Java'dan çok daha iyi 	olmayacak. 17:58 <@nop> belki USerX C yapar 17:58 <@nop> ve sen C++'ı üstlenebilirsin 17:58 <@hezekiah> We don 17:58 <@nop> ? 17:58 <@hezekiah> don't even need to _do_ C++ if you don't want to. It's 	just that I prefer it. 17:59 <@nop> şey, mesele şu 17:59 <@nop> C++ geliştiricisi çok var 17:59 <@nop> özellikle Microsoft dünyasında 17:59 <@hezekiah> Linux dünyasında bile. (bkz: KDE ve Qt.) 17:59 < jrand0m> Sadece .so veya .a yaparsan C ve C++ ikili düzeyde 	uyumludur 17:59 < jrand0m> (bu arada) 18:00 <@nop> C, C++ için iyi bir yedek olur mu, yani C++ geliştiricileri 	bir C API'sini C geliştiricisinin C++ API'sine göre daha kolay idare 	edebilir mi? 18:00 <@hezekiah> jrand0m: Evet. Muhtemelen kütüphaneler olabilir ... ama eğer 	you can 18:00 <@hezekiah> sınıfları bile kullanamıyorsan, amacını biraz boşa çıkarır. 18:00 <@nop> doğru 18:00 <@nop> C'de kalalım 18:01 <@nop> çünkü C++ kodlayıcıları yine de bir C kütüphanesini oldukça 	kolay çağırabilir 18:01 <@hezekiah> Bir modül diğerinin fonksiyonlarını çağırması gerekiyorsa, 	o zaman ikisi de aynı dilde olmalı. 18:01 <@hezekiah> nop: C++ kodlayıcıları C'yi yeterince bilir ... C'yi 	hiç /öğrenmedilerse/ biraz uğraş gerektirebilir. 18:02 <@hezekiah> Ancak, C kodlayıcıları C++'ı bilemeyebilir çünkü C, 	C++'ın yalnızca bir alt kümesidir. 18:02 -!- logger_ [~logger@anon.iip] #iip-dev kanalına katıldı 18:02 -!- #iip-dev için konu: toplantıdan sonra günlük dosyaları çevrimiçi olacak: 	http://wiki.invisiblenet.net/?Meetings 18:02 [Kullanıcılar #iip-dev] 18:02 [@hezekiah] [+Ehud    ] [ leenookx] [ moltar] [ tek    ] 18:02 [@nop     ] [ jeremiah] [ logger_ ] [ Neo   ] [ WinBear] 18:02 [@UserX   ] [ jrand0m ] [ mihi    ] [ ptsc  ] 18:02 -!- Irssi: #iip-dev: Toplam 14 rumuz [3 op, 0 halfop, 1 voice, 10 normal] 18:02 < jrand0m> doğru 18:02 -!- Irssi: #iip-dev'e katılım 9 sn içinde eşitlendi 18:02 < jrand0m> (JMS ile :) 18:02 <@nop> evet 18:03 -!- Artık adın logger 18:03 < jrand0m> tamam, önce API'lerin gerçekten ilgili olup olmadığını 	görmek için genel mimariyi gözden geçirebilir miyiz? 18:03 <@nop> olur  18:04 < jrand0m> :) 18:04 < jrand0m> tamam, routerArchitecture.png ile gönderdiğim e-postaya 	bakın. o ayrım hakkında bir düşünce var mı? 18:04 -!- tek [~tek@anon.iip] çıkış yaptı [] 18:05 < WinBear> jrand0m: bu wiki'de mi? 18:05 < jrand0m> WinBear> hayır, posta listesinde, gerçi arşivler kapalı. 	dur onu wikki'ye ekleyeyim 18:06 <@hezekiah> Yanılıyorsam düzeltin ... 18:07 <@hezekiah> ... ama mümkün olduğunca benzer 3 ayrı API'imiz olacak 	gibi görünüyor. 18:07 <@hezekiah> Doğru mu? 18:07 < jrand0m> evet hezekiah 18:07 <@hezekiah> Her API farklı dilde olduğuna göre, her birinin ayrı ayrı 	implementasyonları mı olacak? 18:07 < jrand0m> evet 18:07 <@hezekiah> Yoksa Java veya Python'un bir C kütüphanesine erişmesinin 	bir yolu var mı? 18:08 < jrand0m> evet, ama o yola gitmek istemiyoruz 18:08 < mihi> Java için: JNI 18:08 <@hezekiah> O hâlde Java, C, C++, Python vb.'nin birlikte çalışması 	hakkındaki konuşma boşuna çünkü asla birlikte çalışmayacaklar mı? 18:08 < jrand0m> wiki'ye nasıl resim eklerim? 18:08 <@hezekiah> Her API'nin, o dilde yazılmış kendi arka ucu var. 18:08 < jrand0m> hayır hezekiah, diyagrama bak 18:09 <@hezekiah> Ah, tabii! 18:09 <@hezekiah> API'ler bir arka uca bağlanmıyor. 18:10 <@hezekiah> Soketler üzerinden konuşuyorlar. 18:10 < jrand0m> evet efendim 18:10 <@hezekiah> Yine de bu biraz kafa karıştırıcı. 18:10 <@hezekiah> Bana bir saniye ver. :) 18:11 <@hezekiah> Tamam. 'transport' (taşıma) diye etiketlenen şey nedir? 18:11 < jrand0m> örneğin, çift yönlü HTTP transport, SMTP transport, düz 	soket transport, yoklayan HTTP soketi, vb. 18:11 < jrand0m> router'lar arasında baytları hareket ettiren şey 18:12 <@hezekiah> Tamam. 18:12 <@hezekiah> Yani baktığım diyagram bir kişinin bilgisayarını gösteriyor. 18:12 <@hezekiah> Transport'lar aracılığıyla diğer insanların bilgisayarlarıyla 	konuşan bir router'ı var. 18:12 < jrand0m> doğru 18:12 <@hezekiah> 1. kişi (Alice) 2 uygulama çalıştırıyor. 18:12 <@hezekiah> Biri C'de, diğeri Java'da. 18:13 <@hezekiah> İkisi de bir kütüphaneye bağlı (o da API). 18:13 < jrand0m> ikisi de ayrı kütüphanelere "bağlı" (API'ler) 18:13 <@nop> basit kavram 18:13 <@nop> evet 18:13 <@hezekiah> Bu kütüphaneler, programdan girdiyi alır, şifreler 	ve soketler (UNIX veya TCP) üzerinden router'a gönderir ... ki bu da 	Alice'in çalıştırdığı başka bir programdır. 18:13 < jrand0m> doğru 18:14 <@hezekiah> Tamam. Yani isproxy'nin ikiye bölünmesi gibi. 18:14 < jrand0m> bingo :) 18:14 <@hezekiah> Bir parça alt seviyedir ve C ile yazılmıştır, diğeri 	üst seviyedir ve her neyle yazılmışsa. 18:14 < jrand0m> aynen 18:14 <@hezekiah> Tamam. Anladım. :) 18:14 < jrand0m> w00t 18:14 <@hezekiah> Yani hiçbir dilin diğer dillerle iyi geçinmesine gerek 	yok. 18:14 < jrand0m> WinBear> üzgünüm, wiki'ye atamam çünkü sadece metin 	kabul ediyor :/ 18:15 <@hezekiah> Hepsi router ile soketler üzerinden iletişim kurduğuna 	göre, tasarım açısından istersen PASCAL'da bile bir API yazabilirsin. 18:15 <@nop> evet 18:15 <@nop> keyfi 18:15 < jrand0m> doğru 18:15 <@nop> keyfi soketleri işler 18:15 < jrand0m> yine de standartlaştırılması gereken bazı şeyler var 	(Destination, Lease vb. için veri yapıları gibi) 18:15 < WinBear> jrand0m: hezekiah'ın söylediklerine dayanarak belirsiz bir 	fikrim var 18:15 < jrand0m> aynen 18:16 <@hezekiah> jrand0m: Doğru. O soketten geçen baytların yapısı ve 	sırası bir yerde tasarımda 18:16 <@hezekiah> tanımlanır. 18:17 <@hezekiah> Ama yine de bu baytların gönderilip alınma şeklini canın 	nasıl isterse öyle uygulayabilirsin. 18:17 <@nop> WinBear: bu, IRC istemcisinin isproxy ile çalışma biçimiyle 	tamamen aynı 18:17 < jrand0m> aynen 18:17 <@hezekiah> Güzel. 18:17 <@hezekiah> Şimdi anlıyorum. :) 18:17 -!- moltar [~me@anon.iip] #iip-dev kanalından ayrıldı [moltar] 18:17 <@nop> pek 18:17 <@nop> tam olarak değil 18:17 <@hezekiah> Hoppala. 18:17 <@nop> ama onun nasıl çalıştığını düşün 18:17 <@nop> ve keyfi soketleri anlayabilirsin 18:17 <@nop> isproxy sadece yönlendirir 18:17 <@nop> ve teslim eder 18:18 <@nop> şimdi jrand0m 18:18 <@nop> hızlı soru 18:18 < jrand0m> evet efendim? 18:18 <@nop> bu API sadece bu ağda çalışmak üzere tasarlanmış yeni 	uygulamalar için mi tasarlandı 18:18 -!- mode/#iip-dev [+v logger] by hezekiah 18:18 < WinBear> nop: yüksek seviyenin IRC istemcisinin yerini almasıyla mı? 18:18 < jrand0m> nop> evet. gerçi bir SOCKS5 vekil sunucu da bu API'yi 	kullanabilir 18:18 <@nop> yoksa hâlihazırdaki standart istemcileri 	çalıştıracak bir ara katman olabilir mi 18:18 <@nop> örneğin 18:19 <@nop> yani yapmamız gereken tek şey aracı -> API yazmak olur 18:19 < jrand0m> (ama bir 'lookup' hizmeti olmadığını unutmayın - bu ağ 	için DNS yok) 18:19 < jrand0m> doğru 18:19 <@nop> böylece mesela Mozilla vb.'yi destekleyebiliriz 18:19 <@nop> böylece sadece eklenti yazabilirler 18:19 < jrand0m> nop> evet 18:19 <@nop> tamam 18:19 <@nop> ya da transport'lar :) 18:20 < jrand0m> (ör. SOCKS5, HTTP outproxy'leri destination1, destination2 	ve destination3'e sabit kodlar) 18:20 <@nop> tamam 18:20 < WinBear> sanırım anladım 18:21 < jrand0m> w00t 18:21 < jrand0m> tamam, bu tasarımda düşünmek zorunda kaldığım şeylerden 	biri, özel anahtarları uygulamanın bellek alanında tutmaktı - router asla 	destination özel anahtarlarını ele geçirmiyor. 18:21 <@hezekiah> Yani uygulama, veriyi API'ye göndererek I2P ağı üzerinden 	ham veri yollayabilir ve gerisini dert etmesine gerek yok. 18:22 <@hezekiah> Doğru mu? 18:22 < jrand0m> bu, API'lerin kriptonun uçtan uca kısmını uygulaması 	gerekliği anlamına gelir 18:22 < jrand0m> aynen hezekiah 18:22 <@hezekiah> Tamam. 18:22 <@nop> evet 18:22 <@nop> fikir bu 18:22 <@nop> senin için yapar 18:22 <@nop> sen sadece kancayı çağırırsın 18:23 <@hezekiah> Hızlı bir soru: 18:23 <@hezekiah> Bu 'router' belli bir protokolü transport'ları üzerinden 	konuşmak zorunda. 18:23 < jrand0m> doğru 18:23 <@hezekiah> O hâlde router'ın birden fazla implementasyonunu sağlamak 	mümkün ... 18:23 < jrand0m> evet 18:24 <@hezekiah> ... yeter ki aynı protokolü konuşsunlar. 18:24 < jrand0m> (bu yüzden özellikte bitbucket'lar için yer tutucular var) 18:24 < jrand0m> doğru 18:24 <@hezekiah> Yani biri Java, biri C, biri PASCAL olan router'larınız var. 18:24  * jrand0m irkilir 18:24 < jrand0m> ama evet 18:24 <@hezekiah> Ve hepsi aynı protokolü kullanarak TCP/IP üzerinden 	konuştukları için birbiriyle konuşabilir. 18:24  * WinBear zıplar 18:24 <@hezekiah> jrand0m: Evet. Ben de PASCAL günlerimi pek hoş 	hatırlamıyorum. 18:25 < jrand0m> şey, örneğin Pascal, TCP transport üzerinden C olanla 	konuşabilir ve C olan da HTTP transport üzerinden Java olanla konuşabilir 18:25 <@hezekiah> Doğru. 18:25 < jrand0m> (transport'lar kendi türleriyle konuşur, router'lar 	aralarındaki iletileri yönetir ama nasıl iletildikleriyle uğraşmazlar) 18:26 <@hezekiah> Vurgulamak istediğim nokta, protokolün aynı olduğu, bu 	yüzden birinin router'ının hangi dilde implement edildiğinin önemsiz 	olmasıydı. 18:26 < jrand0m> doğru 18:26 <@hezekiah> Güzel. 18:26 < jrand0m> şimdi C vs Java vs vb. tartışmalarına neden "kimin 	umrunda" dediğimi anlıyor musun? :) 18:26 <@hezekiah> Evet. 18:26 <@hezekiah> lol 18:27 <@hezekiah> Sana hakkını vermeliyim jrand0m. Bu, geliştiricilerin 	bu ağ için program yazmasını çok kolaylaştıracak. 18:27 < jrand0m> heh, şey, API pek de orijinal değil. Bu, Message Oriented 	Middleware (MOM)'ın çalışma şekli 18:27 <@hezekiah> Hatta belirli platforma özgü özelliklerde uzmanlaşan 	router'lar bile yapabilirsin (64-bit CPU'lar gibi). 18:28 < jrand0m> kesinlikle 18:28 <@hezekiah> jrand0m: Alçakgönüllü de! ;-) 18:28 <@hezekiah> Pekâlâ, bana iyi görünüyor. 18:28 < jrand0m> tamam, UserX, nop, bu ayrım mantıklı mı? 18:28 <@nop> elbette 18:28 <@nop> userx hâlâ burada mı 18:29 <@hezekiah> 1:26'dır boşta. 18:29 < jrand0m> 'k. o zaman iki görevimiz var: ağı tasarlamak ve API'nin 	nasıl çalıştığını tasarlamak. 18:29 <@nop> doğru 18:29 <@hezekiah> Hızlı basit soru: API'ler uçtan uca kripto yapıyor. 	Router'lar da düğümler arası kripto yapıyor mu? 18:29 <@nop> evet 18:30 < jrand0m> evet 18:30 < jrand0m> (transport düzeyi) 18:30 <@hezekiah> Güzel. :) 18:30 <@nop> hezekiah: bu açıdan 	şimdiye kadar sahip olduklarımıza çok benziyor 18:30 <@nop> 18:31 < jrand0m> tamam.. şey, kahretsin, performans modeli üzerine 	yorum yapması için thecrypto buralarda değil. 18:31 < Neo> ve paranoyak olanlar için, uygulamalar API'ye gelmeden önce 	PGP şifrelemesini yapabilir ;) 18:31 < jrand0m> kesinlikle neo 18:31 < jrand0m> Hatta uçtan uca kriptografiyi API'nin dışında bırakıp 	uygulamalara bırakmayı bile düşündüm... 18:31 <@hezekiah> jrand0m: Bu zalimce olurdu. 18:31 < jrand0m> heheh 18:32 <@hezekiah> Bu arada, API'ler ve router soketler üzerinden iletişim 	kurar. 18:32 <@hezekiah> UNIX'te UNIX soketleri mi yoksa yerel TCP/IP soketleri 	mi kullanacaklar? 18:32 < jrand0m> muhtemelen sadelik için sadece yerel TCP/IP 18:32 <@nop> bekle 18:32 <@hezekiah> (Muhtemelen ikisini de kabul eden bir router yapılabilir.) 18:33  * hezekiah bu değiştirilebilir parçalar kurulumunu gerçekten seviyor 18:33 <@nop> eğer bir saniye beklersen 18:34 <@hezekiah> Bekliyorum ... :) 18:34 <@nop> thecrypto'yu evinden arayacağım 18:34 <@nop> bağlanıp bağlanamayacağına bakayım 18:34 < jrand0m> hehe tamam 18:34 <@hezekiah> lol 18:34  * hezekiah kalın bir İtalyan aksanı takınır 18:34 <@hezekiah> Nop'un ... BAĞLANTILARI var! 18:34 < jeremiah> merhaba 18:34 <@nop> hey jeremiah 18:35 < jrand0m> selam jeremiah 18:35 <@nop> API seviyesinde bir Python API'sine yardımcı olmaya istekli 	olur musun 18:35 < jeremiah> tabii 18:35  * jeremiah gecikmiş mesajları okur 18:35 < jrand0m> heh tamam 18:35  * nop arıyor 18:36 <@nop> evde değil 18:36 <@nop> bir saat içinde dönecek 18:36 < jrand0m> 'k, .xls'i okuyan ya da model hakkında yorumu olan 	başkası var mı? 18:37 <@hezekiah> .xls'i okudum ... ama P2P hakkında çok şey bilmiyorum, 	bu yüzden çoğu kafamın üstünden geçti. 18:37 <@hezekiah> UserX bu işlerde iyidir. 18:37 <@nop> Hâlâ okumam lazım 18:37 < jrand0m> (bu arada, morphmix çılgın sayılar veriyordu... 	ağdaki rastgele konakların ortalama 20-150 ms ping sürelerine sahip 	olabileceğini söylüyorlardı, benim beklediğim 3-500 yerine) 18:37 < jrand0m> güzel 18:37 <@nop> bu staroffice mi openoffice mi? 18:37 < jrand0m> openoffice, ama .xls'e dışa aktardım 18:37 <@nop> hangisi excell? 18:37 < jrand0m> doğru 18:38 <@hezekiah> Bu arada, API ile ilgili ... 18:38 < jrand0m> evet efendim? 18:38 <@hezekiah> ... C'de boolean int olur. 18:38 <@nop> hangi e-posta 18:38 <@nop> hezekiah: evet 18:38 <@hezekiah> Sınıflar yapı işaretçileri (structure pointer) olarak 	gönderilir. 18:38 <@nop> boolean'ı typedef etmedikçe 18:39 <@hezekiah> ve byte[] kullanan fonksiyonlar, tamponun uzunluğunu 	belirten ek bir parametreyle birlikte void* kullanır. 18:39 <@nop> hezekiah: titizleniyorsun :) 18:39 < jrand0m> nop> arşivlere erişemiyorum, bu yüzden konu satırının 	ne olduğundan emin değilim ama geçen haftaydı... 18:39 <@nop> onu daha sonraya saklayalım 18:39 <@hezekiah> nop: Titizlik mi? 18:39 < jrand0m> heh, evet, C API üzerinde çalışan sizler o detayı 	arada çözebilirsiniz 18:39  * jeremiah gecikmiş mesajları okumayı bitirdi 18:39 <@nop> dosyanın adı ne 18:39 <@hezekiah> nop: Sadece farklı olan her şeyi bulmaya çalışıyorum 	ki jrand0m'un istediği gibi halledelim. 18:40 <@hezekiah> Yardımcı olmaya çalışıyorum. :) 18:40 <@nop> hezekiah: evet, muhtemelen toplantı zamanı dışında 18:40 < jrand0m> nop> simple_latency.xls 18:40 <@hezekiah> boolean sendMessage(Destination dest, byte[] payload); 18:40 <@hezekiah>  şu olurdu 18:40 <@hezekiah> int sendMessage(Destination dest, void* payload, int length); 18:40 <@hezekiah> . 18:40 <@hezekiah> byte[]  recieveMessage(int msgId); 18:40 <@hezekiah>  bu ya şöyle olabilir: 18:41 <@hezekiah> void*  recieveMessage(int msgId, int* length); 18:41 <@hezekiah>  ya da 18:41 <@nop> jrand0m: aldım 18:41 <@hezekiah> void recieveMessage(int msgId, void* buf, int* length); 18:41 <@hezekiah>  ya da 18:41 < jrand0m> hezekia: neden typedef struct { int length; void* data; 	} Payload; olmasın 18:41 <@hezekiah> DataBlock* recieveMessage(int msgId)l 18:41 <@hezekiah> DataBlock* recieveMessage(int msgId); 18:41 < jeremiah> bu xls nerede? 18:41 <@nop> oh iip-dev 18:41 <@hezekiah> jrand0m: Az önce bahsettiğin struct temelde DataBlock'un 	kendisi. 18:42 < jrand0m> aynen hezekiah 18:42 <@nop> konu more models 18:42 <@hezekiah> Büyük olasılıkla C sürümünde DataBlock'lar olur. 18:43 <@hezekiah> Bunun ötesinde, not edilmesi gereken tek şey her 'interface'in 	sadece bir fonksiyon kümesi olacağıdır. 18:43 <@hezekiah> nop: C API'de olacak tüm farkları bulabildim mi? 18:43 < jrand0m> doğru. 	belki #include "i2psession.h" ya da buna benzer bir şey 18:43 < jeremiah> bir taslak Python API'si var mı? 18:44 < jrand0m> hayır jeremiah, Python'u pek bilmiyorum :/ 18:44 <@nop> Java API'yi yeniden gözden geçirmem gerekir ama tam isabet 	ettiğini söyleyebilirim 18:44 < jrand0m> ama muhtemelen Java'ya benzer olur, çünkü Python OO'dur 18:44 < jeremiah> güzel, C olanından bir tane türetebilirim 18:44  * nop bir Java'cı değil 18:44 < jrand0m> güzel jeremiah 18:44 < jeremiah> birkaç gün önce gönderdiğinde C API var mıydı? 18:44 <@hezekiah> Evet. Python Java API'sini halledebilmelidir. 18:44 < jrand0m> jeremiah> o Java olanıydı 18:45 < jrand0m> oh, Java olan bugün 18:45 < jrand0m> eskisi dil bağımsızdı 18:45 <@hezekiah> Hmm 18:45 <@nop> UserX, C API'ye yardımcı olabileceğini söylüyor 18:45 < jrand0m> güzel 18:45 <@nop> şu an işte meşgul 18:46 < jrand0m> iyi 18:46 <@hezekiah> Son bir not: C API'sinde, her fonksiyon muhtemelen Java'da 	'interface'i olduğu yapıya bir structure* alır. 18:46 <@nop> hezekiah: iyi görünüyor 18:46 <@nop> iyi görünüyor 18:46 <@hezekiah> I2PSession       createSession(String keyFileToLoadFrom, 	Properties options); 18:46 <@hezekiah>  şöyle olurdu: 18:46 <@nop> Java ve onların yerel olmayan veri tipleri ;) 18:46 <@hezekiah> I2PSession* createSession(I2PClient* client, char* 	keyFileToLoadFrom, Properties* options); 18:46 <@nop> ;) 18:46 < jrand0m> hehe 18:46 < jrand0m> doğru hezekiah 18:47 < jeremiah> Unicode'u ele alıyor muyuz? 18:47 <@hezekiah> Neyse, bu farklarla yaşayabiliyorsanız, C ve Java API'leri 	bunun ötesinde aynı olmalı. 18:47 <@hezekiah> nop? Unicode? :) 18:47 < jrand0m> UTF8, değilse UTF16 18:48 <@hezekiah> Belki Unicode uygulama seviyesinde ele alınmalı. 18:48 < jrand0m> doğru, karakter seti tamamen mesaj içeriğidir 18:48 <@hezekiah> Oh. 18:48 < jeremiah> tamam 18:48 <@hezekiah> Java String'ler Unicode değil mi jrand0m? 18:48 < jrand0m> bitbucket'ların hepsi bit düzeyinde tanımlı olacak 18:48 < jrand0m> evet hezekiah 18:48 < jrand0m> (onlara açıkça karakter kümesini değiştirmelerini 	söylemedikçe) 18:49 <@hezekiah> Dolayısıyla C API'si Unicode kullanarak stringleri 	implemente etmediği sürece Java API'sine gönderilen string C API'sine 	gönderilenden farklı olur. 18:49 < jrand0m> ilgili değil 18:49 <@hezekiah> Tamam. 18:49 < jrand0m> (app->API != API->router. biz yalnızca API->router'ı 	tanımlarız) 18:49 <@hezekiah> Demek istediğim şu, jrand0m: 18:50 <@hezekiah> Parolamı Java API ile ayarlarsam, router'a gider ve 	başka bir yere çıkar. 18:50 < jrand0m> parola? bir Destination mı oluşturuyorsun? 18:50 <@hezekiah> Sonra başka bir router bulur, bu da onu C ile implement 	edilmiş başka bir API'ye gönderir (?) 18:50 <@hezekiah>   void            setPassphrase(String old, String new); 18:50 <@hezekiah> O fonksiyon. 18:51 < jrand0m> hezekiah> bu, router'ın yönetimsel yöntemlerine erişmek için 	yönetimsel paroladır 18:51 <@hezekiah> Ah 18:51 <@hezekiah> Java String kullanan API fonksiyonlarından herhangi 	biri, o String'in başka bir API'ye gönderilmesiyle sonuçlanıyor mu? 18:51 < jrand0m> Uygulamaların %99,9'u yalnızca I2PSession kullanacak, 	I2PAdminSession değil 18:51 <@nop> ayrıca, router ile taşınan her şey ağda taşınmak üzere 	dönüştürülüyor, doğru mu? 18:51 <@hezekiah> Öyleyse Unicode kullanmalıyız. 18:51 <@nop> Unicode ilgili olmaz 18:52 < jrand0m> hayır. tüm routerlar arası bilgi bitbucket'larla 	tanımlanacak 18:52 <@hezekiah> Tamam. 18:52 < jrand0m> doğru nop, transport düzeyinde 18:52 <@hezekiah> (bitbucket'in sadece bir ikili tampon olduğunu 	varsayıyorum, doğru mu?) 18:53 < jrand0m> bir bitbucket (bit kovası), birinci bitin X, ikinci bitin 	Y, 3-42. bitlerin Z anlamına geldiğini vb. belirten bir ifadedir 18:53 < jrand0m> (ör. sertifikalar bitbucket'i için X.509 kullanmak 	isteyebiliriz)

18:53 <@hezekiah> Bununla daha önce hiç uğraşmadım.
18:54 <@hezekiah> Oraya geldiğimde endişelenirim. :)
18:54 < jrand0m> heh aynen
18:55 < jrand0m> tamam, bugün değinmek istediğim dört şey: *router 	'mimarisi, *performans modeli, *saldırı analizi, *psyc.  İlkini hallettik, thecrypto çevrimdışı, bu yüzden belki bunu erteleriz (nop, model hakkında düşüncelerin yoksa?)
18:57 <@hezekiah> Hım ... jrand0m. Bir sorum daha var.
18:57 < jeremiah> jrand0m: ağ spesifikasyonunun en son sürümü nerede? 	13'ünde gönderdiğin şey mi?
18:57 < jrand0m> evet efendim?
18:57 <@hezekiah> Şey, router mimarisi, API'lerin Uygulama tarafından 	/kendilerine gönderilen/ anahtarları işlemesini öngörüyor.
18:57 < jrand0m> jeremiah> evet
18:57 <@nop> Şimdilik yok
18:58 <@hezekiah> Şimdi ... API'nin anahtarı almasının tek yolu 	createSession gibi görünüyor.
18:58 < jrand0m> hezekiah> router  açık anahtarlar ve imzalar alır, 	özel anahtarlar değil
18:58 < jrand0m> doğru
18:58 <@hezekiah> Ama bu bir dosya gerektiriyor.
18:58 < jrand0m> anahtarlar bir dosyada veya API'nin belleğinde saklanır
18:58 < jrand0m> evet
18:58 <@hezekiah> Peki uygulama bir anahtar üretiyorsa, neden bunu bir 	arabellek üzerinden API'ye doğrudan gönderemesin?
18:59 <@hezekiah> Gerçekten bir dosyada saklayıp sonra dosya adını mı 	vermek zorunda?
18:59 < jrand0m> hayır, istersen bellekte olabilir
18:59 <@hezekiah> Yine de API'de bunların hepsini yapacak bir işlev yok.
18:59 <@hezekiah> Sadece bir düşünce.
19:00 <@hezekiah> Anahtar yalnızca bir kez üretilip defalarca 	kullanılacaksa (GPG anahtarları gibi) bir dosya mantıklı.
19:00 -!- mihi [none@anon.iip] çıktı [hoşça kalın, geç oluyor...]
19:00 <@hezekiah> Ama daha sık üretilecekse, o zaman bir yapı ya da 	türünden bir arabellek üzerinden API'ye doğrudan göndermenin bir yolu hoş 	olabilir
19:00 <@hezekiah> .
19:01 < jrand0m> evet, bir kez ve sadece bir kez üretilir (tabii bir 	alüminyum folyo şapka takmıyorsan)
19:02 < jrand0m> yine de createDestination(keyFileToSaveTo) o anahtarı 	oluşturmanı sağlar
19:02 <@hezekiah> Tamam.
19:02 <@hezekiah> O halde Uygulama'dan API'ye doğrudan aktarım 	gerekmiyor. Bir dosya yeter.
19:03 <@hezekiah> Peki, ben kaba bir şekilde böldüğümden önce 	neredeydik? :)
19:06 < jeremiah> yani şu anda sadece router API'si üzerinde çalışıyoruz, 	istemci olan üzerinde değil, doğru mu?
19:06 < jrand0m> şey, şimdilik performans analizini atlıyoruz (umarım 	gelecek haftadan önce e-posta listesinde bunun hakkında biraz sohbet 	olur?).  Muhtemelen saldırı analizi için de aynı şekilde (yeni 	spesifikasyonu okuyan ve yorumları olan var mı?)
19:07 <@hezekiah> Madem onu atlıyoruz, şimdi ne hakkında konuşmamız 	gerekiyor?
19:07 <@hezekiah> Psyc?
19:07 < jrand0m> başka dile getirmek isteyen bir yorumunuz yoksa...?
19:08 <@hezekiah> Şey, bir kez olsun, yorum deliğim (nam-ı diğer ağzım) 	boş.
19:08 < jrand0m> hehe
19:09 < jrand0m> tamam, işin IRC tarafının nasıl işleyeceğine dair 	fikir olan var mı ve psyc ilgili veya yararlı olabilir mi?
19:09 < jeremiah> ara not (sinirimi bozdu): Wired'ın "Wired, Tired, 	Expired" listesinde Waste 'wired' olarak yer almıştı
19:09 < jrand0m> heh
19:09 < jrand0m> herkesi ne kadar etkileyeceğimizi farkında mısın?
19:09 < jeremiah> evet
19:09 <@hezekiah> jrand0m: Bu, bunu çalıştırdığımızı varsayıyor.
19:10 < jrand0m> Çalışacağına garanti veriyorum.
19:10 <@hezekiah> Dışarıda başarısız olmuş bir sürü başka girişim var.
19:10 < jrand0m> Bunun için işimden ayrıldım.
19:10 <@hezekiah> O zaman herkesi hayran bırakacağız. :)
19:10 <@hezekiah> Evet. Peki bunu yapınca ekmek masaya nasıl gelecek?
19:10 <@hezekiah> GPL kodu pek para kazandırmaz. ;-)
19:10 < jrand0m> heh
19:11 <@hezekiah> psyc konusunda ... şöyle söyleyeyim:
19:11 <@hezekiah> İlk kez ondan haberdar oluşum, bize onunla ilgili 	e-posta attığın zamandı.
19:11 < jrand0m> hay aksi, onu bulan ben değildim :)
19:11 <@hezekiah> Ancak IRC muhtemelen en yaygın (hatta /en/ yaygın 	değilse) sohbet protokollerinden biridir.
19:11 <@hezekiah> İnsanlar, psyc'ın ne olduğunu /bilmelerinden/ ÇOK önce 	IRC uygulamaları isteyecek.
19:11 <@hezekiah> jrand0m: Amanın. Özür. O detayı unutmuşum. :)
19:12 < jrand0m> psyc'a göre değil.  Tarihleri sanırım 86'ya kadar gidiyor
19:12 <@hezekiah> Mesele şu ki, protokolün üstünlüğü, onu kimin 	kullandığı kadar önemli değil.
19:12 <@hezekiah> _Tarihleri_ o kadar eskiye gidiyor olabilir.
19:12 <@hezekiah> Ama kaç kişi Psyc'ı _kullanıyor_?
19:12 < jeremiah> evet, ben doğduktan bir yıl sonra (öhöm) 	ortalardalarsa ve hâlâ o kadar büyük değillerse
19:12 <@hezekiah> Demek istediğim, daha iyi bir protokol olsa bile, çoğu 	insan IRC'yi _kullanıyor_.
19:13 <@hezekiah> Dünyadaki en iyi I2P ağı yapabiliriz ...
19:13 -!- Ehud [logger@anon.iip] çıktı [Ping zaman aşımı]
19:14 < jeremiah> neden umursadığımızı kısaca açıklayabilir mi biri? 	IRC'nin sadece olası uygulamalardan biri olacağını, ağın isterse psyc'ı da 	destekleyecek kadar esnek olduğunu sanıyordum
19:14 <@hezekiah> Doğru.
19:14 <@hezekiah> Psyc yapılabilir ...
19:14 <@hezekiah> ... ama önce IRC yapmamız gerektiğini söylüyorum çünkü 	daha çok kişi onu kullanıyor.

19:14 <@hezekiah> jrand0m, harika bir I2P ağı oluşturabiliriz, ama insanlar istedikleri bir şey olmadıkça 	onu kullanmazlar. 19:14 < jrand0m> jeremiah> psyc'nin ilginç olmasının nedeni, psyc'nin çalıştığıyla aynı tarzda IRC'yi 	uygulamak isteyebilecek olmamız
19:15 <@hezekiah> Bu yüzden onlara bir 'killer-app' (vazgeçilmez bir uygulama) sağlamalıyız.
19:15 < jeremiah> ok
19:15 < jrand0m> doğru, IIP görünmez bir IRC projesi ve insanların IRC'yi 	çalıştırmasına izin verecek
19:16 < jrand0m> merkezi bir sunucu olmadan (hatta aslında hiçbir sunucu olmadan), 	IRC'nin nasıl çalışacağını çözmek için yapılması gereken çok fazla düşünme var. 	psyc bunun için olası bir yanıt sunuyor
19:16 < jrand0m> gerçi başkaları da var
19:17 <@hezekiah> Dediğim gibi, psyc daha iyi olabilir, ama insanlar IRC kullanmak istiyor, 	psyc değil.
19:17 < jrand0m> ve kullanacaklar
19:17 < jrand0m> irc kullanacaklar
19:17 <@hezekiah> Her şey pazarlama ile ilgili, bebeğim! ;-)
19:17 < jeremiah> Bu gece spesifikasyonu ve psyc ile ilgili bazı şeyleri okumaya çalışacağım
19:17 < jrand0m> aynen
19:17 <@hezekiah> lol
19:17 < jeremiah> yarın 5:00 UTC'de buluşmayı mı planlıyoruz?
19:17 <@hezekiah> Hayır?
19:18 < jeremiah> ya da ne zaman olursa
19:18 < jrand0m> iip'te 24x7'yim :)
19:18 < jeremiah> evet ama ben yemek yiyorum
19:18 <@hezekiah> jrand0m: Fark ettim.
19:18 < jrand0m> 05:00 utc mi yoksa 17:00 utc mi?
19:18 <@hezekiah> jeremiah: LOL!
19:18 <@hezekiah> Şey, iip-dev toplantısı resmi olarak 21:00 UTC'de başlıyor.
19:18 -!- Ehud [~logger@anon.iip] #iip-dev kanalına katıldı
19:19 < jeremiah> ok, 05:00 UTC dedim çünkü aslında sallıyordum
19:19 < jeremiah> mids nerede?
19:19 <@hezekiah> mids, projeden bir süreliğine ayrıldı.
19:19 <@hezekiah> Birkaç toplantı önce orada değil miydin?
19:19 < jeremiah> ok
19:19 < jeremiah> sanırım değilmişim
19:19 <@hezekiah> Gündemin bir parçası olarak bir tür veda partisi yaptık.
19:19 < jeremiah> oh
19:20 <@hezekiah> Tamam ...
19:20 <@hezekiah> Gündemde hâlâ bir şey var mı?
19:20  * jrand0m benimkinde hiçbir şey kalmadı
19:20 < jeremiah> psyc hakkında:
19:20 < jeremiah> bu bir psyc özelliğiyse, bundan 	bir süre önce bahsettiğini biliyorum
19:20  * hezekiah en başta hiç gündemi yoktu
19:21 <@hezekiah> pace
19:21 <@hezekiah> place
19:21 < jeremiah> Odadaki her kullanıcının diğer 	her kullanıcıya mesaj göndermesinin akıllıca olduğunu düşünmüyorum
19:21 <@hezekiah> İşte!
19:21 < jrand0m> jeremiah> yani yedekli atanmış pseudoserver'lar 	iletileri yeniden dağıtır mıydı?
19:21 < jrand0m> (pseudoservers = kanalda kullanıcı listesini tutan 	eşler)
19:21 < jeremiah> 'broadcasting'in de o kadar akıllıca olduğunu düşünmüyorum, ama bu

seems like it'll require a _çok_ bant genişliği gerektirecek gibi görünüyor; bir modemde olabilecek belirli bir kullanıcı için, ve diyelim ki... 20 mesajı ayrı ayrı göndermenin gecikmesi 	sohbeti mahvederdi
19:21 < jeremiah> En iyi çözümü bilmiyorum, belki de o bir çözüm olurdu
19:22 < jeremiah> Bence istersen doğrudan mesajlaşma iyi olurdu, 	ama muhtemelen o kadar önemli olmadığı durumlar da var
19:22 <@hezekiah> Mesajın, özgünlüğü garanti etmek için yazarın özel 	anahtarıyla imzalanması gerekir.
19:22 <@hezekiah> Bu mesele yine de uzun süre önem arz etmeyecek olsa da, 	bence jeremiah haklı bir noktaya değiniyor
19:22 < jrand0m> hezekiah> bu, kullanıcıların kanıtlanabilir iletişim istemelerini gerektirir :)
19:23 < jrand0m> kesinlikle.
19:23 <@hezekiah> Bir kanaldaki 100 kullanıcıya mesaj göndermek zorunda olsaydım ...
19:23 < jeremiah> ortalama mesajım sadece birkaç yüz bayt olmasına rağmen, 	bunu yüzlerce kullanıcıya göndermek o kadar da zor olmayabilir
19:23 <@hezekiah> ... şey, sohbetim /çok/ yavaş olurdu.
19:23 < jeremiah> özellikle de bir yanıt beklemesen
19:23 <@hezekiah> Tek bir mesaj göndermek için 20K.
19:23 <@hezekiah> Sanmıyorum. :)
19:23 < jrand0m> şey, bir kanalda 100 kullanıcı varsa, *birinin* 	100 mesaj göndermesi gerekir
19:23 < jeremiah> 20K mı?
19:23 < jeremiah> ah, doğru
19:23 <@hezekiah> 200 kullanıcı
19:24 < jeremiah> hımm
19:24 < jeremiah> routers bu işte iyi olmaz mıydı?
19:24 < jeremiah> bir dereceye kadar güvenle, onların düzgün bir bant genişliğine sahip olduğunu varsayabiliriz, 	değil mi?
19:24 <@hezekiah> Her kişinin bir 'router implementation'ı olduğunu sanıyordum
19:24 < jrand0m> pek sayılmaz.  eğer aktarıcılar (relay'ler) varsa, aday gösterme mekanizmasının 	bunu hesaba katması gerekir
19:24 < jrand0m> evet hezekiah
19:24 < jeremiah> spesifikasyonu okumadım
19:25 < jrand0m> bir router, senin yerel router'ındır
19:25 <@hezekiah> Ugh!
19:25 <@hezekiah> Hâlâ nick'lerinizi karıştırıyorum!
19:25 <@hezekiah> lol
19:25 < jrand0m> hehe
19:25 <@hezekiah> Um ... nop nereye gitti?
19:25 <@hezekiah> Oh.
19:26 <@hezekiah> Hâlâ burada.
19:26 <@hezekiah> Bir an gitti sandım,
19:26 < jrand0m> ama jeremiah haklı, psyc 	göz önünde bulundurmak isteyebileceğimiz bazı fikirler ortaya koyuyor, bunları reddetmek de isteyebiliriz gerçi
19:26 <@hezekiah> Önce ağı çalışır hâle getirelim.
19:26  * jrand0m buna kadeh kaldırır
19:26 <@hezekiah> Gözünü bitiş çizgisine dikersen, 	önündeki 3 inçlik taşa takılırsın.
19:27  * jeremiah ilham geldiğini hisseder
19:27 <@hezekiah> lol
19:27 < jrand0m> Bence gerçekten harika olur, 	gelecek haftaya kadar ağ spesifikasyonunu gözden geçirmeyi hedefleyebilir, 	herhangi birinin düşüncesi veya yorumu olduğunda iip-dev'e e-postalar gönderebilirsek. 	deli miyim?
19:27 <@hezekiah> nop? Gündeme ekleyecek başka bir şeyin var mı, 	yoksa oturumu kapatalım mı?
19:27 <@hezekiah> jrand0m: Şey, 	gelecek haftaya kadar bunların hepsini okuyabilir miyim bilmiyorum, ama deneyeceğim. :)
19:27 < jrand0m> heh
19:28 < jrand0m> yorucu 15 sayfa ;)
19:28 <@hezekiah> 15 sayfa?
19:28 <@hezekiah> 120 gibi görünüyordu!
19:29 < jrand0m> heh, şey, sanırım çözünürlüğüne bağlı ;)
19:29 < jeremiah> orada bir sürü anchors (çapa bağlantıları) var, 	bu da onu kocaman gösteriyor
19:29 < jrand0m> hehe
19:29 <@hezekiah> Sol tarafta 15 bağlantıdan ÇOK daha fazlası var, dostum!
19:29 <@hezekiah> İtiraf et!
19:29 <@hezekiah> 15'ten fazla. :)
19:29 <@hezekiah> Oh!
19:29 <@hezekiah> Onlar sayfa değil! Onlar sadece anchors!
19:29 <@hezekiah> Kurtuldum!
19:30  * hezekiah boğulmaktan yeni kurtarılmış bir denizci gibi hissediyor
19:30 < jeremiah> sınıf, cilt 4 bölüm 2 Mesaj Bayt Yapısı'na dön
19:30 < jrand0m> lol
19:30 <@hezekiah> lol
19:30 <@nop> kapanış
19:30 <@hezekiah> *baf*!
19:30 <@hezekiah> Gelecek hafta, 21:00 UTC, aynı yer.
19:30 <@hezekiah> Orada görüşürüz. :)
19:30 < jeremiah> görüşürüz
--- Günlük kapatıldı Tue Jul 15 19:30:51 2003 </div>
