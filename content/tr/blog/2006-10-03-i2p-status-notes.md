---
title: "2006-10-03 tarihli I2P Durum Notları"
date: 2006-10-03
author: "jr"
description: "Ağ performansı analizi, CPU darboğazı araştırması, Syndie 1.0 sürüm planlaması ve dağıtık sürüm kontrolü değerlendirmesi"
categories: ["status"]
---

Herkese selam, bu hafta gecikmiş durum notları

* Index

1) Ağ durumu 2) Router geliştirme durumu 3) Syndie gerekçesinin devamı 4) Syndie geliştirme durumu 5) Dağıtık sürüm kontrolü 6) ???

* 1) Net status

Son bir iki hafta irc ve diğer hizmetlerde oldukça istikrarlı geçti, ancak dev.i2p/squid.i2p/www.i2p/cvs.i2p birkaç aksaklık yaşadı (geçici olarak işletim sistemiyle ilgili sorunlar nedeniyle). Şu anda durum istikrarlı görünüyor.

* 2) Router dev status

Syndie tartışmasının diğer yüzü "peki, bu router için ne anlama geliyor?" sorusu; ve bunu yanıtlamak için, router geliştirmesinin şu anda hangi noktada olduğunu kısaca açıklayayım.

Genel olarak, router’ı 1.0’a ulaşmaktan alıkoyan şey bana göre anonimlik özellikleri değil, performansıdır. Elbette, iyileştirilecek anonimlik sorunları var, ancak anonim bir ağ için oldukça iyi performans elde etsek de, performansımız daha geniş kullanım için yeterli değil. Ayrıca, ağın anonimliğini artırmaya yönelik iyileştirmeler performansını artırmaz (aklıma gelen çoğu durumda, anonimlik iyileştirmeleri verimi düşürür ve gecikmeyi artırır). Önce performans sorunlarını çözmemiz gerekiyor; çünkü performans yetersizse, anonimlik teknikleri ne kadar güçlü olursa olsun tüm sistem yetersizdir.

Öyleyse, performansımızı geriye çeken ne? İlginçtir ki, bu CPU kullanımımız gibi görünüyor. Nedenine tam olarak geçmeden önce, biraz daha arka plan bilgisi.

 - to prevent partitioning attacks, we all need to plausibly build
   our tunnels from the same pool of routers.
 - to allow the tunnels to be of manageable length (and source
   routed), the routers in that pool must be directly reachable by
   anyone.
 - the bandwidth costs of receiving and rejecting tunnel join
   requests exceeds the capacity of dialup users on burst.

Bu nedenle, router katmanlarına ihtiyacımız var - bazıları küresel olarak erişilebilir ve yüksek bant genişliği limitlerine sahip (tier A), bazıları ise değil (tier B). Bu, netDb içindeki kapasite bilgileri aracılığıyla fiilen halihazırda uygulanmış durumda ve bir-iki gün önce itibarıyla, tier B'nin tier A'ya oranı yaklaşık 3'e 1 idi (cap L, M, N veya O olan 93 router ve cap K olan 278 router).

Şimdi, A katmanında yönetilmesi gereken temelde iki kıt kaynak vardır - bant genişliği ve CPU. Bant genişliği olağan yollarla yönetilebilir (yükü geniş bir havuza yaymak, bazı eşlerin çok yüksek miktarları üstlenmesini sağlamak [örn. T3 bağlantısı olanlar], ve bireysel tunnels ve bağlantıları reddetmek veya sınırlamak).

CPU kullanımını yönetmek daha zordur. A katmanı router'larda görülen birincil CPU darboğazı, tunnel build isteklerinin şifresinin çözülmesidir. Büyük router'lar bu etkinlik tarafından tamamen tüketilebilir (ve ediliyor) - örneğin, router'larımdan birinde yaşam boyu ortalama tunnel şifre çözme süresi 225ms ve bir tunnel isteğinin şifresinin çözülmesinin yaşam boyu *ortalama* sıklığı 60 saniyede 254 olay, yani saniyede 4.2’dir. Bu ikisini basitçe çarpmak, CPU’nun %95’inin yalnızca tunnel isteği şifre çözme tarafından tüketildiğini gösteriyor (ve bu, olay sayılarındaki ani artışları hesaba katmıyor). Yine de o router, aynı anda 4-6000 tunnel’a katılmayı bir şekilde başarıyor ve şifresi çözülen isteklerin yaklaşık %80’ini kabul ediyor.

Ne yazık ki, o router üzerindeki CPU çok ağır yüklendiği için, daha şifreleri çözülebilmeden önemli sayıda tunnel oluşturma isteğini düşürmek zorunda kalıyor (aksi halde istekler kuyrukta o kadar uzun süre bekleyecekti ki, kabul edilseler bile asıl istekte bulunan onları zaten kaybolmuş ya da herhangi bir şey yapılamayacak kadar yük altında sayacaktı). Bu açıdan bakıldığında, router'ın %80 kabul oranı çok daha kötü görünüyor - çalışma ömrü boyunca yaklaşık 250k isteğin şifresini çözdü (yani yaklaşık 200k kabul edildi), ancak CPU aşırı yüklenmesi nedeniyle şifre çözme kuyruğunda yaklaşık 430k isteği düşürmek zorunda kaldı (o %80 kabul oranını %30'a indirerek).

Çözümler, tunnel isteği şifresinin çözülmesine ilişkin ilgili CPU maliyetini azaltma doğrultusunda gibi görünüyor. CPU süresini bir büyüklük mertebesinde azaltırsak, bu A düzeyi router'ın kapasitesini önemli ölçüde artırır, böylece retleri (hem açık hem de örtük, atılan istekler nedeniyle) azaltır. Bu da sırayla tunnel oluşturma başarı oranını artırarak lease sürelerinin dolma sıklığını azaltır; bu da ardından, tunnel'lerin yeniden oluşturulması nedeniyle ağ üzerindeki bant genişliği yükünü azaltır.

Bunu yapmanın yöntemlerinden biri, tunnel oluşturma isteklerini 2048bit Elgamal kullanmaktan, mesela 1024bit ya da 768bit kullanmaya çevirmek olurdu. Ancak burada şu sorun var: Bir tunnel oluşturma isteği mesajının şifrelemesini kırarsanız, tunnel'in tam yolunu öğrenirsiniz. Bu yola gitsek bile, bize ne kadar kazandırırdı? Şifre çözme süresinde bir büyüklük mertebesinde iyileşme, B katmanının A katmanına oranında bir büyüklük mertebesinde artışla (diğer adıyla freeriders (bedavacılar) sorunu) silinip gidebilir ve sonra çıkmaza girerdik; çünkü 512 veya 256bit Elgamal'e geçmemizin (ve hâlâ kendimize aynada bakabilmemizin) bir yolu yok ;)

Bir alternatif, daha zayıf kriptografi kullanmak fakat yeni tunnel oluşturma süreciyle eklediğimiz paket sayımı saldırılarına karşı korumayı kaldırmak olurdu. Bu, Tor-benzeri teleskopik bir tunnel içinde tamamen geçici, müzakere edilmiş anahtarlar kullanmamıza izin verirdi (ancak, yine de, bir hizmeti tanımlayan çok basit pasif paket sayımı saldırılarına tunnel oluşturucusunu maruz bırakırdı).

Başka bir fikir, netDb içinde daha da açık yük bilgilerini yayımlamak ve kullanmaktır; bu da istemcilerin, yukarıdakine benzer, yüksek bant genişliğine sahip bir router'ın tunnel istek iletilerinin %60'ını hiç incelemeden düşürdüğü durumları daha doğru şekilde saptamasına olanak tanır. Bu doğrultuda yapılmaya değer birkaç deney var ve bunlar tam geriye dönük uyumlulukla gerçekleştirilebilir; dolayısıyla yakında bunları görmeye başlamalıyız.

Yani, bugün gördüğüm kadarıyla darboğaz router/ağda. Bununla nasıl başa çıkabileceğimize dair her türlü öneri büyük memnuniyetle karşılanacaktır.

* 3) Syndie rationale continued

Forumda Syndie ve onun nereye oturduğuna dair ayrıntılı bir gönderi var - şuradan göz atın <http://forum.i2p.net/viewtopic.php?t=1910>

Ayrıca, üzerinde çalışılan Syndie dokümantasyonundan iki alıntıyı vurgulamak istiyorum. İlk olarak, irc'den (ve henüz yayımlanmamış SSS'den):

<bar> Üzerinde düşündüğüm bir soru şu: ileride kim        syndie üretim sunucularını/arşivlerini barındıracak kadar cesarete sahip olacak?  <bar> bunlar, bugün eepsites(I2P Sites)        kadar kolay izlenebilir olmayacak mı?  <jrandom> herkese açık syndie arşivlerinin, forumlara gönderilen içeriği        *okumak* gibi bir yeteneği yoktur; bunu yapabilmek için gerekli anahtarlar forumlar        tarafından yayımlanmadığı sürece.  <jrandom> ve usecases.html'in ikinci paragrafına bak  <jrandom> elbette, arşivleri barındıranlar bir forumu kaldırmaları yönünde        yasal talimat alırlarsa muhtemelen bunu yaparlar  <jrandom> (ama o zaman insanlar başka bir        arşive taşınabilir, forumun işleyişini aksatmadan)  <void> evet, farklı bir        ortama geçişin sorunsuz olacağı gerçeğinden bahsetmelisin  <bar> arşivim kapanırsa, tüm forumumu yeni bir        arşive yükleyebilirim, değil mi?  <jrandom> aynen bar  <void> geçiş sırasında aynı anda iki yöntemi kullanabilirler  <void> ve herkes ortamları senkronize edebilir  <jrandom> doğru void

Henüz yayımlanmamış Syndie usecases.html dosyasının ilgili bölümü şöyledir:

Pek çok farklı grup tartışmaları bir çevrimiçi forumda düzenlemek istese de, geleneksel forumların (web siteleri, BBS'ler vb.) merkezî yapısı sorun yaratabilir. Örneğin, forumu barındıran site hizmet reddi (DoS) saldırıları veya idari işlemler yoluyla çevrimdışı hâle getirilebilir. Ayrıca, tek bir sunucu grubun etkinliğini izlemek için kolay bir nokta sunar; böylece, bir forumda takma adlar kullanılıyor olsa bile, bu takma adlar tek tek iletileri gönderen veya okuyan IP adreslerine bağlanabilir.

Ayrıca, forumlar yalnızca merkeziyetsiz değildir; aynı zamanda ad-hoc (geçici ve amaca özel) bir şekilde düzenlenmiş olup diğer örgütleme teknikleriyle tamamen uyumludur. Bu, küçük bir grup insanın forumlarını bir teknik kullanarak (iletileri bir wiki sitesine yapıştırarak dağıtmak) yürütebileceği, başka bir grubun ise forumunu başka bir teknikle (iletilerini OpenDHT gibi dağıtık bir hash tablosuna yayımlayarak) yürütebileceği; ve eğer bir kişi her iki teknikten de haberdarsa, iki forumu birbirleriyle senkronize edebileceği anlamına gelir. Bu, yalnızca wiki sitesinden haberdar olanların, yalnızca OpenDHT hizmetinden haberdar olanlarla birbirleri hakkında hiçbir şey bilmeden konuşabilmesini sağlar. Daha da ileri götürüldüğünde, Syndie, tüm organizasyon genelinde iletişim kurarken bireysel hücrelerin kendi görünürlüklerini kontrol etmelerine olanak tanır.

* 4) Syndie dev status

Son zamanlarda Syndie üzerinde çok ilerleme kaydedildi; IRC kanalındaki kullanıcılara 7 alfa sürümü dağıtıldı. scriptable interface (betiklenebilir arayüz) içindeki başlıca sorunların çoğu giderildi ve umuyorum ki bu ayın ilerleyen günlerinde Syndie 1.0 sürümünü yayımlayabileceğiz.

Az önce "1.0" mı dedim? Kesinlikle! Syndie 1.0 bir metin tabanlı uygulama olacak ve mutt veya tin gibi benzer metin tabanlı uygulamaların kullanılabilirliğiyle karşılaştırılabilir bile olmayacak olsa da, yine de tam bir işlev yelpazesi sunacak, HTTP ve dosya tabanlı syndication (içerik dağıtımı) stratejilerine izin verecek ve umarız potansiyel geliştiricilere Syndie'nin yeteneklerini gösterecek.

Şu anda, insanların arşivlerini ve okuma alışkanlıklarını daha iyi düzenlemelerini sağlayacak bir Syndie 1.1 sürümünü kabaca planlıyorum ve belki de bazı arama işlevlerini entegre eden bir 1.2 sürümünü (hem basit aramalar hem de belki lucene'in tam metin aramaları). Syndie 2.0 muhtemelen ilk GUI sürümü olacak, tarayıcı eklentisi ise 3.0 ile gelecek. Elbette, ek arşivler ve mesaj dağıtım ağları için destek, uygulanır uygulanmaz gelecek (freenet, mixminion/mixmaster/smtp, opendht, gnutella vb.).

Yine de şunun farkındayım: metin tabanlı uygulamalar esasen teknik meraklılara yönelik olduğundan, Syndie 1.0 bazılarının istediği kadar dünyayı sarsıcı olmayacak; ancak "1.0" sürümünü nihai bir sürüm olarak görme alışkanlığımızı kırmayı ve onu bunun yerine bir başlangıç olarak değerlendirmeyi denemek istiyorum.

* 5) Distributed version control

Şimdiye kadar, Syndie için sürüm kontrol sistemi (VCS) olarak subversion ile kurcalıyordum; gerçi gerçekten sadece CVS ve clearcase'e hâkimim. Bunun nedeni, zamanın çoğunda çevrimdışı olmam ve çevrimiçi olduğumda bile çevirmeli bağlantının yavaş olması; bu yüzden subversion'ın yerel diff/revert/etc işlevleri oldukça kullanışlı oldu. Ancak dün void, bunun yerine dağıtık sistemlerden birine bakmamızı önererek beni dürttü.

Birkaç yıl önce I2P için bir VCS (sürüm kontrol sistemi) değerlendirirken onlara bakmıştım, ancak çevrimdışı işlevlerine ihtiyacım olmadığı için (o zamanlar internet erişimim iyiydi) onları eledim; bu yüzden öğrenmeye değmezdi. Artık durum böyle değil, bu yüzden şimdi onlara biraz daha yakından bakıyorum.

- From what I can see, darcs, monotone, and codeville are the top

Alternatifler var ve darcs'in yama tabanlı VCS (sürüm kontrol sistemi) yaklaşımı özellikle cazip görünüyor. Örneğin, tüm işlerimi yerelde yapabilir ve gzip'lenmiş & gpg'lenmiş diff'leri sadece scp ile dev.i2p.net üzerindeki bir Apache dizinine yükleyebilirim; insanlar da kendi değişikliklerini, kendi seçtikleri konumlara gzip'lenmiş ve gpg'lenmiş diff'lerini yayımlayarak katkıda bulunabilir. Bir sürümü etiketleme zamanı geldiğinde, sürümün içerdiği yama kümesini belirten bir darcs diff oluşturur ve o .gz'lenmiş/.gpg'lenmiş diff'i de diğerleri gibi yüklerdim (elbette gerçek tar.bz2, .exe ve .zip dosyalarını da dağıtmanın yanı sıra ;)).

Ve, özellikle ilginç bir nokta olarak, bu gzip'lenmiş/gpg'lenmiş diff'ler Syndie iletilerine ek olarak gönderilebilir, bu da Syndie'nin kendi kendini barındırabilmesini sağlar.

Yine de şu zımbırtılarla ilgili deneyimi olan var mı? Bir tavsiyeniz var mı?

* 6) ???

Bu sefer yalnızca 24 ekran dolusu metin (forum gönderisi dahil) ;) Ne yazık ki toplantıya katılamadım, ama her zamanki gibi, herhangi bir fikir ya da öneriniz varsa sizden duymayı çok isterim - sadece listeye, foruma yazın ya da IRC'ye uğrayın.

=jr
