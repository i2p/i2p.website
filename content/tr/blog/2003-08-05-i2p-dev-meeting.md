---
title: "I2P geliştirici toplantısı, 5 Ağustos 2003"
date: 2003-08-05
author: "nop"
description: "Java geliştirme durumu, kriptografi güncellemeleri ve SDK ilerlemesini kapsayan 52. I2P geliştirici toplantısı"
categories: ["meeting"]
---

<h2 id="quick-recap">Quick recap</h2>

<p class="attendees-inline"><strong>Katılanlar:</strong> hezekiah, jeremiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">Toplantı Günlüğü</h2>

<div class="irc-log"> <nop>	ok, meeting started <nop>	what's on the agenda -->	logger (logger@anon.iip) has joined #iip-dev -->	Anon02 (~anon@anon.iip) has joined #iip-dev <hezekiah>	Tue Aug  5 21:03:10 UTC 2003 <hezekiah>	Welcome to the Nth iip-dev meeting. <hezekiah>	What's on the agenda? <thecrypto>	Tue Aug  5 21:02:44 UTC 2003 <thecrypto>	synced to a NTP stratum 2 :) <hezekiah>	Tue Aug  5 21:03:13 UTC 2003 -->	ptm (~ptm@anon.iip) has joined #iip-dev <hezekiah>	Just synced to NIST. :) <mihi>	this sync does not help w/ iip delays ;) <jrand0m>	nop: things I want to see covered: java dev status, java crypto 	  status, python dev status, sdk status, naming service <hezekiah>	(We're going into the naming service _already_?) <jrand0m>	not design you wanker, thats co's schpeel.  just talk about stuff 	  if there's stuff to talk about. <hezekiah>	Ah *	jrand0m puts LART away <jrand0m>	anything else on the agenda? <jrand0m>	or shall we dig in? <hezekiah>	Well, I can't think of anything else to add. <hezekiah>	Ah! <hezekiah>	Oh! <jrand0m>	ok.  java dev status: <hezekiah>	Good. <--	mrflibble has quit (Ping timeout) <nop>	ok <nop>	agenda <nop>	1) Welcome <jrand0m>	as of today, there is a java client API with a stub java router 	  that can talk to each other.  in addition, there is an application called ATalk 	  allowing anonymous IM + file transfer. <nop>	2) IIP 1.1 blackouts <nop>	3) I2P <nop>	4) The End with comments and stuff *	jrand0m goes back to corner <nop>	sorry 	  joeyo jrand0m Aug 05 17:08:24 * hezekiah gives jrand0m a dunce hat to wear in 	  the corner. ;-) <nop>	sorry about that <nop>	didn't see you started there <nop>	maybe I should go in corner <hezekiah>	lol <jrand0m>	no worry.  item 1) *	hezekiah hands nop a dunce hat too. :) <nop>	ok welcome everybuddy <nop>	blah blah <nop>	2) IIP 1.1 blackouts -->	mrflibble (mrflibble@anon.iip) has joined #iip-dev <hezekiah>	52nd iip-dev meeting and all that good rot! <nop>	the server recently had some issues with the hard drive sectors and has 	  been replaced <nop>	I plan to be moving the darn server into a more stable environment with 	  redundancy <nop>	and possibly lend out control of multiple ircd servers <nop>	dunno <nop>	that's something to be discussed <--	Anon02 has quit (EOF From client) <nop>	hopefully our servers should stay up now since the harddrive was replaced <nop>	sorry about the inconvenience folks <nop>	3) I2P - Jrand0m take it away <nop>	come out of the corner jrand0m *	hezekiah goes over to the corner, pulls jrand0m off his chair, drags him 	  to the podium, takes away his dunce hat, and hands him the mic. *	nop goes into that corner to fill his place <hezekiah>	lol! <jrand0m>	sorry, back *	nop grabs dunce hat from hezekiah *	nop puts it on his head *	nop applauds for jrand0m *	jrand0m just watches the show <jrand0m>	er... um ok <hezekiah>	jrand0m: i2p, java status, etc. Talk man! <jrand0m>	so, as of today, there is a java client API with a stub java 	  router that can talk to each other.  in addition, there is an application called 	  ATalk allowing anonymous IM + file transfer. <hezekiah>	File transfer already!? <jrand0m>	si sr <hezekiah>	Wow. <hezekiah>	I'm sure behind the times. <jrand0m>	but not the most graceful <hezekiah>	lol <jrand0m>	it takes a file and tosses it in a message <hezekiah>	Ouch. <nop>	how long did 1.8 mb local transfer take? <jrand0m>	I've tested with a 4K file and a 1.8Mb file <jrand0m>	a few seconds <nop>	nice <nop>	:) <hezekiah>	Does the java stuff do real encryption yet, or does it still 	  fake that? <nop>	fake <nop>	even I know that <nop>	:) <jrand0m>	I warmed it up by talking to myself first [e.g. one window to 	  another, saying hi] so it didn't deal with the overhead of the first elg <jrand0m>	right, its faked largely <thecrypto>	most of the encryption is fake <thecrypto>	that's being worked on though <hezekiah>	Of course. :) <jrand0m>	definitely. <jrand0m>	on that front, wanna give us an update thecrypto? <thecrypto>	well, right now i'm done with ElGamal and SHA256 <thecrypto>	right now I'm working on generating primes for DSA <thecrypto>	I'll send out 5 and then we can just pick one <hezekiah>	nop: Didn't you have prime(s) coming for use with DSA? <thecrypto>	We also have some benchmarks on ElGamal and SHA256 <thecrypto>	And they are all fast <jrand0m>	latest benchmarks w/ elg: <jrand0m>	Key Generation Time Average: 4437	total: 443759	min: 	  872	   max: 21110	   Keygen/second: 0 <jrand0m>	Encryption Time Average    : 356	total: 35657	min: 	  431	   max: 611	   Encryption Bps: 179 <jrand0m>	Decryption Time Average    : 983	total: 98347	min: 	  881	   max: 2143	   Decryption Bps: 65

<hezekiah>	min ve max: saniye cinsinden mi?
<jrand0m>	Bps'in pek kullanışlı olmadığını unutmayın, çünkü yalnızca 	  64 bayt şifreleyip/şifre çözüyoruz
<thecrypto>	ms
<jrand0m>	hayır, üzgünüm, bunların hepsi milisaniye
<hezekiah>	Harika. :)
<hezekiah>	Ve bu java'da mı yapılıyor?
<thecrypto>	evet
<thecrypto>	tamamen java
<hezekiah>	OK. Resmen etkilendim. :)
<jrand0m>	100%.  P4 1.8
<thecrypto>	benim 800 Mhz makinemde de aşağı yukarı aynı
<hezekiah>	Aynı testleri nasıl yapabilirim?
<jrand0m>	sha256 kıyaslaması:
<jrand0m>	Kısa Mesaj Zaman Ortalaması  : 0 toplam: 0	min: 0	max: 	  0  Bps: NaN
<jrand0m>	Orta Mesaj Zaman Ortalaması : 1 toplam: 130	min: 0	max: 	  10 Bps: 7876923
<jrand0m>	Uzun Mesaj Zaman Ortalaması   : 146	toplam: 14641	min: 	  130	   max: 270	   Bps: 83037
<thecrypto>	ElGamalBench programını çalıştır
<hezekiah>	OK.
<hezekiah>	Gidip bulacağım.
<jrand0m>	(kısa boyut: ~10 bayt, orta ~10KB, uzun ~ 1MB)
<jrand0m>	java -cp i2p.jar ElGamalBench
<jrand0m>	("ant all" çalıştırdıktan sonra)
<hezekiah>	jrand0m: Teşekkürler. :)
<jrand0m>	sorun değil
<thecrypto>	NaN olayı o kadar hızlı olduğunu, sonunda 0'a bölme durumuna düştüğümüz anlamına geliyor 	  o kadar hızlı :)
<hezekiah>	sha kıyaslaması nedir?
<jrand0m>	java -cp i2p.jar SHA256Bench -->	Neo (anon@anon.iip) #iip-dev'e katıldı
<hezekiah>	OK.
<jrand0m>	muhtemelen bunları ilgili motorların main() metotları olacak şekilde 	  taşımak isteyeceğiz, ama şimdilik bulundukları yerde iyiler
<hezekiah>	Tüm bunların bir AMD K6-2 333MHz üzerinde ne kadar hızlı olduğuna bakalım ( 	  tam sayı matematiğiyle pek tanınmayan bir çip.)
<jrand0m>	heh
<jrand0m>	tamam, o halde geriye DSA ve AES kaldı, değil mi?
<jrand0m>	bunların hepsi müthiş thecrypto.  güzel iş.
<thecrypto>	evet
<jrand0m>	diğer ikisi için bir tahmini zaman alabilir miyim?  ;)
<hezekiah>	Eğer bu benim makinemde de seninki kadar hızlıysa, 	  bunu nasıl yaptığını bana göstermen gerekiyor. ;-)
<thecrypto>	asal sayılar hazır olur olmaz DSA neredeyse bitmiş olacak
<nop>	hezekiah python için sslcrypto'yu denedin mi
<thecrypto>	asal sayı üretecinden ve bunun gibi şeylerden biraz kod kopyalayıp 	  düzenleyince bitiyor
<nop>	o bağlantıdaki olanı
<hezekiah>	nop: sslcrypto bize bir fayda sağlamaz.
<hezekiah>	nop: ElGamal _ya da_ AES _ya da_ sha256'i uygulamıyor.
<thecrypto>	AES büyük ölçüde hazır; sadece bir yerlerde hâlâ bulup yok etmeye 	  çalıştığım bir hata var, onu halleder halletmez tamamlanacak
<jrand0m>	thecrypto> yani cuma gününe kadar, DSA anahtar üretimi, imzalama, doğrulama ve AES şifreleme, 	  keyfi boyutlu girdiler için şifre çözme?
<nop>	McNab'ın sitesindeki olan yapmıyor mu?
<thecrypto>	evet
<nop>	tüh
<thecrypto>	cuma olmalı
<thecrypto>	büyük olasılıkla perşembe
<jrand0m>	thecrypto> buna UnsignedBigInteger işleri de dahil mi?
<thecrypto>	yaz kampı nedeniyle gelecek haftaki toplantıyı kaçıracağım ve 	  ondan sonra geri döneceğim
<thecrypto>	jrand0m: muhtemelen hayır
<jrand0m>	tamam.
<jrand0m>	şimdilik, java ve python arasında birlikte çalışabilirlik 	  bozuk.
<jrand0m>	yani kripto için. ---	Bildirim: jeremiah çevrimiçi (anon.iip). -->	jeremiah (~chatzilla@anon.iip) #iip-dev'e katıldı
<jrand0m>	(yani imzalar, anahtarlar, şifreleme ve şifre çözme için)

<nop>	hmm belki C/C++'a daha çok odaklanmalıyız
<thecrypto>	şey, tamamen çalışır hale getirdiğimizde hem java hem de python'un birbirleriyle konuşabildiğinden
	  emin olabiliriz
<jrand0m>	sen yokken imzasız kısımlara bakarım.
<jeremiah>	biri bana sohbet geçmişini e-postayla atabilir mi? jeremiah@kingprimate.com
<hezekiah>	jeremiah: Bana bir dakika ver. :)
<jrand0m>	nop> C/C++ için geliştiricilerimiz var mı?
<nop>	Bir kişi var, evet
<nop>	ve Hezekiah'ın da yapabileceğini biliyoruz
<jrand0m>	ya da belki hezekiah + jeremiah'tan bir python geliştirici durum güncellemesi alıp
	  C/C++ geliştirme için daha fazla kişiyi ne zaman bulacağımızı görebiliriz
<jrand0m>	doğru, tabii. ama hez+jeremiah şu anda python üzerinde çalışıyor (değil mi?)
<hezekiah>	Evet.
<--	mrflibble ayrıldı (Ping zaman aşımı)
<hezekiah>	Zavallı jeremiah'a epey sıkıntı çıkarıyorum gibi.
<nop>	Ben sadece şunu diyordum, python hızlı hızlara ulaşamayacaksa
<hezekiah>	Python esasen bu ağı anlamam için.
<nop>	ahh
<hezekiah>	Temel olarak tüm spesifikasyonu takip eder hale getirdiğimde, onu jeremiah'a devretmeyi
	  ve uygun gördüğü gibi yapmasını düşünüyorum.
<hezekiah>	Bu, spesin mükemmel bir uygulaması olması amaçlanmıyor.
<hezekiah>	(Eğer onu isteseydim C++ kullanırdım.)
<jeremiah>	şey, iirc, uygulamanın gerçekten işlemci yoğun kısımları yok; crypto (kriptografi) dışında,
	  ve ideal olarak o da zaten C ile halledilecek, değil mi?
<jrand0m>	tabii jeremiah. hepsi uygulamaya bağlı
-->	mrflibble (mrflibble@anon.iip) #iip-dev kanalına katıldı
<hezekiah>	jeremiah: Teoride.
<jrand0m>	peki python tarafında neredeyiz? istemci API'si, yalnızca yerel router, vb.?
<jeremiah>	python uygulaması ayrıca en baştan hangi optimizasyonları yapabileceğimizi de görmemizi sağlayacak...
	  onu güncel tutmak ya da mümkünse C uygulamasının ilerisinde tutmak isterim
<hezekiah>	jrand0m: Tamam. Bende olanlar şöyle.
<hezekiah>	 _teoride_ router, bir istemciden gelen yönetim dışındaki tüm mesajları işleyebilmelidir.
<hezekiah>	Ancak, henüz bir istemcim yok, bu yüzden hata ayıklayamadım (yani hâlâ hatalar var.)
<hezekiah>	Şu anda istemci üzerinde çalışıyorum.
<jrand0m>	tamam. imza doğrulamayı devre dışı bırakabilirsen, şu an java istemcisini ona karşı çalıştırabilmeliyiz
<hezekiah>	Bir iki gün içinde yönetim mesajları hariç onu bitirmeyi umuyorum.
<jrand0m>	bunu toplantıdan sonra test edebiliriz
<hezekiah>	jrand0m: Tamam.
<jeremiah>	son toplantıdan beri çoğunlukla gerçek dünya işleriyle uğraşıyordum, istemci API'si üzerinde
	  çalışabilirim, sadece düşüncemi hezekiah'inkiyle senkronize etmeye çalışıyordum
<jrand0m>	güzel
<hezekiah>	jeremiah: Biliyor musun, sadece bekle.
<hezekiah>	jeremiah: Muhtemelen şu anda uğraşman için fazla fazla yeni şey ekliyorum.
<jeremiah>	hezekiah: doğru, söyleyeceğim şey şuydu: muhtemelen sen temel kısımları uygulamaya koyup ilerlemelisin
<hezekiah>	jeremiah: Biraz sonra stabil hale gelecek ve sen de onu iyileştirmeye başlayabileceksin.
	  (Yardım gerektiren pek çok TODO yorum var.)
<jeremiah>	ve sonra resmi kavradığımda onu daha sonra genişletebilirim
<hezekiah>	Aynen.
<hezekiah>	Tüm bu kodun bakımını sen yapacaksın. :)
<jrand0m>	güzel. yani çalışan bir python router + istemci API'si için tahmini süre 1-2 hafta mı?
<hezekiah>	Haftaya tatile gidiyorum, o yüzden muhtemelen.
<hezekiah>	yakında router'dan router'a ilişkin daha fazla detaya sahip olacak mıyız?
<jrand0m>	hayır.
<jrand0m>	şey, evet.
<jrand0m>	ama hayır.
<hezekiah>	lol
<jeremiah>	hezekiah: tatil ne kadar sürecek?
<hezekiah>	1 hafta.
<jeremiah>	tamam
<jrand0m>	(yani SDK çıkar çıkmaz zamanımın %100'ü I2NP'ye gidecek)
<hezekiah>	tatile gitmeden önce yönetim dışı tüm işlevleri yazmış olmayı umuyorum
<hezekiah>	.
<jrand0m>	ama sonra döndükten kısa süre sonra üniversiteye gidiyorsun, değil mi?
<hezekiah>	I2NP?
<hezekiah>	Doğru.
<jrand0m>	ağ protokolü
<hezekiah>	tatilden sonra yaklaşık 1 haftam var.
<hezekiah>	sonra gidiyorum.
<hezekiah>	ve boş zamanım bir anda dibe vuracak.
<jrand0m>	yani o 1 hafta sadece hata ayıklama olmalı
<jeremiah>	hez yokken kod üzerinde çalışabilirim yine de
<jrand0m>	aynen
<jrand0m>	yaz planların nasıl, jeremiah?
<hezekiah>	jeremiah: Belki o yönetim işlevlerini çalışır hale getirebilirsin?

<thecrypto>	tatilden döndükten sonra üzerinde çalışmak için hâlâ bir ayım olacak
<jrand0m>	bir hayatın mı olacak, yoksa bizim geri kalanımız gibi l00sers mı?  :)
<jeremiah>	belki
<hezekiah>	100sers?
<hezekiah>	100ser nedir?
<jeremiah>	22'sinde üniversiteye gidiyorum, onun dışında geliştirme yapabilirim
<mihi>	hezekiah: bir kaybeden
<jeremiah>	ve gitmeden önceki son hafta tüm arkadaşlarım şehirde olmayacak... bu yüzden hiper-geliştirme moduna geçebilirim
<hezekiah>	mihi: Ah!
<jrand0m>	hehe
<hezekiah>	Tamam. Gündemde neredeydik?
<hezekiah>	Yani, sırada ne var?
<jrand0m>	sdk durumu
<jrand0m>	sdk == bir istemci impl, yalnızca yerel bir router impl, bir uygulama ve dokümantasyon.
<jrand0m>	Bunu gelecek salıya kadar çıkarmak istiyorum.
<hezekiah>	jeremiah: O bekleyen işler yolda. Orada seni unuttuğum için üzgünüm. :)
<jeremiah>	teşekkürler
<jrand0m>	tamam, co ortalıkta değil, bu yüzden adlandırma servisi işleri muhtemelen biraz gündem dışı
<jrand0m>	spesifikasyonları yayınladıktan sonra ya da o buralardayken adlandırma servisini tartışabiliriz
<jrand0m>	tamam, I2P işleri için bu kadar
<jrand0m>	başka I2P işi olan var mı, yoksa şuna geçiyor muyuz:
<nop>	4) Son, yorumlar ve falan filan
<hezekiah>	Aklıma bir şey gelmiyor.
<jrand0m>	Herkesin şunu gördüğünü varsayıyorum http://www.cnn.com/2003/TECH/internet/08/05/anarchist.prison.ap/index.html ?
<thecrypto>	burada değil
<jrand0m>	(nop onu daha önce burada paylaştı)
<hezekiah>	Bomba yapımı sitesine link verdiği için tutuklanan adamla ilgili olan mı?
<jrand0m>	evet
<jrand0m>	I2P'yi ASAP ayağa kaldırma ihtiyacıyla ilgili bağlantı bariz olmalı ;)
<hezekiah>	Tamam! jeremiah, o günlükler şimdi gönderildi.
<jeremiah>	teşekkürler
<jrand0m>	soru / yorum / düşünce / frizbi atan var mı, yoksa rekor kıracak kadar kısa bir toplantı mı yapıyoruz?
*	thecrypto bir frizbi fırlatır
<--	logger ayrıldı (Ping zaman aşımı)
<jrand0m>	kahretsin bugün hepiniz pek sessizsiniz ;)
<mihi>	soru:
<mihi>	geliştirici olmayanlar java kodunu nereden alabilir?
<jrand0m>	efendim?
<thecrypto>	henüz değil
<mihi>	404
<jrand0m>	yayına hazır olduğumuzda o erişilebilir olacak. yani kaynak kod SDK ile birlikte çıkacak
<jrand0m>	heh
<jrand0m>	evet, SF kullanmıyoruz
<hezekiah>	nop: anonim CVS'i bir ara çalışır hâle getirmemiz mümkün mü?
<hezekiah>	zaman?
<--	mrflibble ayrıldı (Ping zaman aşımı)
<nop>	şey, standart olmayan bir port açardım
<jrand0m>	hezekiah> kodun üzerinde GPL lisansı olduğunda onu sağlayacağız
<nop>	ama viewcvs üzerinde çalışıyorum
<jrand0m>	yani şu an değil, çünkü GPL dokümanı henüz koda eklenmedi
<hezekiah>	jrand0m: Tüm python kod dizinlerinde var ve tüm python kaynak dosyaları GPL-2 altında lisanslamayı belirtiyor.
<jrand0m>	hezekiah> bu cathedral üzerinde mi?
<hezekiah>	Evet.
<jrand0m>	ah tamam.  i2p/core/code/python ?  yoksa farklı bir modül mü? * jrand0m onu orada görmemiş
<hezekiah>	Her python kod dizininde içinde GPL-2 bulunan bir COPYING dosyası var ve her kaynak dosyada lisans GPL-2 olarak ayarlı
<hezekiah>	O i2p/router/python ve i2p/api/python
<jrand0m>	'k
<jrand0m>	yani, evet, gelecek salıya kadar SDK + halka açık kaynak erişimine sahip olacağız.
<hezekiah>	Süper.
<hezekiah>	Ya da senin söylemeyi sevdiğin gibi, wikked. ;-)
<jrand0m>	heh
<jrand0m>	nada mas?
<hezekiah>	nada mas? Bu ne demek!?
<jeremiah>	daha fazlası yok
*	jrand0m üniversitede biraz espanol öğrenmeni önerir
-->	mrflibble (mrflibble@anon.iip) #iip-dev kanalına katıldı
<hezekiah>	Sorusu olan?
<hezekiah>	İlk çağrı!
<--	ptm (~ptm@anon.iip) #iip-dev kanalından ayrıldı (ptm)
<hezekiah>	İkinci çağrı!
<--	mrflibble ayrıldı (Bay Flibble diyor ki: "game over boys")
<hezekiah>	Şimdi konuşun... veya daha sonra konuşasınız gelene kadar bekleyin!
<thecrypto>	tamam, ElGamal'ı daha da optimize edeceğim, bu yüzden gelecekte daha da hızlı ElGamal benchmark'larını bekleyin
<jrand0m>	lütfen ayar çekmeden önce DSA ve AES'e odaklan... ne olurrrr :)
<thecrypto>	odaklanacağım
<hezekiah>	Bunu yapmasının nedeni, yine insanlara sorun çıkarıyor olmam. ;-)
<thecrypto>	DSA asalları üretiyorum
-->	mrflibble (mrflibble@anon.iip) #iip-dev kanalına katıldı
<thecrypto>	şey, en azından şu anda DSA asalları üreten programı yazıyorum
<hezekiah>	Java'daki ElGamal bir AMD K-6 II 333MHz'i sevmiyor.
<hezekiah>	Tamam.
<hezekiah>	Soru turu bitti!
<jrand0m>	tamam hez, işimiz bitti. java istemcisini ve python router'ını çalıştırma konusunda küçük bir powwow yapmak ister misin?
<hezekiah>	Hepinizle gelecek hafta görüşürüz yurttaşlar!
*	hezekiah *baf*er'i masaya indirir
</div>
