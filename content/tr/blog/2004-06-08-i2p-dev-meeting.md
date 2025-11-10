---
title: "I2P Geliştirici Toplantısı - 08 Haziran 2004"
date: 2004-06-08
author: "duck"
description: "08 Haziran 2004 tarihli I2P geliştirme toplantısı tutanağı."
categories: ["meeting"]
---

## Kısa bir özet

<p class="attendees-inline"><strong>Katılanlar:</strong> cervantes, deer, duck, fvw, hypercubus, mihi, Nightblade, Sonium, ugha_node</p>

## Toplantı Günlüğü

<div class="irc-log"> 21:02:08 &lt;duck&gt; Tue Jun  8 21:02:08 UTC 2004 21:02:21 &lt;duck&gt; toplantı zamanı 21:02:33 &lt;duck&gt; yazı şu adreste: http://dev.i2p.net/pipermail/i2p/2004-June/000268.html 21:02:39 &lt;duck&gt; ama numaralandırmada bir hata yaptım 21:02:45 &lt;duck&gt; dolayısıyla ilk 5 numaralı madde atlanacak 21:02:53 &lt;hypercubus&gt; yaşasın! 21:03:03  * duck birasına biraz buz koyar 21:03:14  * mihi ilk #5'i #4 olarak yeniden adlandırırdım ;) 21:03:27 &lt;hypercubus&gt; yok, haftaya iki tane 4. madde yapalım ;-) 21:03:37  * duck 'hypercubus' adını 'mihi' olarak değiştirir 21:03:48 &lt;hypercubus&gt; yaşasın! 21:03:49 &lt;duck&gt; tamam 21:03:53 &lt;duck&gt; * 1) libsam 21:04:02 &lt;duck&gt; kanalda Nightblade var mı? 21:04:39 &lt;duck&gt; (idle     : 0 days 0 hours 0 mins 58 secs) 21:05:03 &lt;hypercubus&gt; ;-) 21:05:53  * duck mikrofonu geri alır 21:06:15 &lt;duck&gt; Nightblade C / C++ için bir SAM kütüphanesi yazdı 21:06:23 &lt;duck&gt; bende derleniyor.. ama söyleyebileceğim tek şey bu :) 21:06:37 &lt;mihi&gt; test örnekleri yok mu? ;) 21:07:06 &lt;duck&gt; eğer rFfreebsd kullananlar varsa Nightblade sizinle ilgilenebilir 21:07:08 &lt;ugha_node&gt; Koddaki strstr çağrıları beni gerçekten sinirlendirdi. ;) 21:07:27 &lt;ugha_node&gt; duck: rFfreebsd nedir? 21:07:42 &lt;duck&gt; freebsd'i öyle yazmışım 21:08:00 &lt;mihi&gt; rm -rF freebsd? 21:08:29 &lt;ugha_node&gt; Ne yazık ki -F rm ile çalışmıyor. 21:08:30 &lt;duck&gt; ugha_node: BSD lisanslı; öyleyse düzelt 21:08:41 &lt;fvw&gt; kulağa mantıklı geliyor :). Ne yazık ki son freebsd makinemdeki kurulumu bir süre önce kaldırdım. Yine de başkalarının makinelerinde hesaplarım var ve test örneklerini çalıştırmaya hazırım. 21:08:43 &lt;ugha_node&gt; duck: yapabilirim. :) 21:08:50 &lt;duck&gt; (lanet BSD hippileri) 21:09:09 &lt;duck&gt; ah, güzel ve kısa, frank 21:09:17 &lt;duck&gt; libsam hakkında yorum var mı? 21:09:49 &lt;duck&gt; fvw: sanırım ihtiyacı olursa Nightblade seninle iletişime geçer 21:09:50  * fvw irc istemcisini öldüren tamamen mantıklı unix davranışına homurdanır. 21:10:02 &lt;duck&gt; ama e-postası bir haftalıktı, bir şey bulmuş olabilir 21:10:17 &lt;mihi&gt; fvw: ? 21:10:24 &lt;fvw&gt; evet, teklifimi değerlendirmek isteyen biri olduysa onu biraz kaçırmışım.                  e-posta falan göndermekten çekinmeyin. 21:10:42  * duck #2'ye geçer 21:10:46 &lt;hypercubus&gt; ıı, nereye? ;-) 21:10:54 &lt;duck&gt; 2) tek bir tarayıcıyla i2p ve normal web'i gezmek 21:10:57 &lt;fvw&gt; taze kurulum, zsh'ı arka plandaki işlere HUP göndermemesini henüz söylemedim.                  &lt;/offtopic&gt;

21:11:09 <fvw> hypercubus: Sanırım genel posta listesi kullanıcı listesinde yer alıyorum. fvw.i2p@var.cx
21:12:11 <duck> tarayıcının proxy yok sayma listesine tüm TLD'leri eklemekle ilgili bazı şeyler vardı
21:12:23 <fvw> bunun tartışılması gerekiyor mu? Bence büyük ölçüde                  posta listesinde halledildi.
21:12:24 <duck> Bence bu çirkin bir hack
21:12:36 <fvw> evet, ondan bahsedildi. Tekrar hoş geldin.
21:12:47 <duck> fvw: Konuyu okumadım :)
21:13:12 <duck> peki, bunu tartışmak istemiyorsan, #3'e geçelim
21:13:19 <duck> * 3) sohbet kanalı
21:13:23 <hypercubus> cervantes'in betiği Konqueror 3.2.2, Firefox 0.8 ve                         Opera 7.51'de mükemmel çalışıyor; hepsi Gentoo w/KDE 3.2.2 için
21:13:39  * mihi #4 üzerine bir bayrak diker
21:13:55 <duck> #i2p-chat burada konu dışı sohbet ve hafif destek için alternatif bir kanal
21:14:08 <duck> Bunu kimin kaydettiğini bilmiyorum
21:14:12 <hypercubus> ben yaptım
21:14:17 <duck> o zaman dikkatli olsan iyi olur :)
21:14:22 <fvw> ıı, #4 yok, sadece iki tane #5 var :)
21:14:33 <hypercubus> ihtiyacım olduğunda parolayı hatırlayabilirsem şanslıyım ;-)
21:14:33 <mihi> [22:27] -ChanServ-      Kanal: #i2p-chat
21:14:33 <mihi> [22:27] -ChanServ-      İrtibat: hypercubus <<ONLINE>>

21:14:33 &lt;mihi&gt; [22:27] -ChanServ-    Alternatif: cervantes &lt;&lt;ONLINE&gt;&gt; 21:14:37 &lt;mihi&gt; [22:27] -ChanServ-   Kayıtlı: 4 gün (0sa 2dk 41sn) önce 21:15:12 &lt;hypercubus&gt; etrafta olmadığımda ve sorun çıktığında kullanılmak üzere güvendiğim birkaç kişiye op yetkisi verdim 21:15:24 &lt;duck&gt; kulağa hoş geliyor 21:15:39 &lt;duck&gt; biraz aşırı olabilir 21:15:51 &lt;hypercubus&gt; IRC'de asla bilemezsin ;-) 21:15:55 &lt;duck&gt; ama protogirl buraya katıldıktan sonra bu kanalı biraz toparlamanın iyi olacağını düşündüm 21:16:03 &lt;hypercubus&gt; heh 21:16:27 &lt;hypercubus&gt; önümüzdeki birkaç ay içinde bir ara buna kesinlikle ihtiyaç duyacağız 21:16:34 &lt;duck&gt; jups 21:16:48 &lt;duck&gt; sonra freenode tayfası bizi kapı dışarı eder  21:16:55 &lt;hypercubus&gt; ;-) 21:17:13 &lt;duck&gt; onların kampf'ında yazılı olmayan hiçbir şeyi sevmezler 21:17:16 &lt;duck&gt; err 21:17:44  * duck $nextitem'a geçer ve mihi'nin breakpoint'ini tetikler 21:17:47 &lt;hypercubus&gt; yeni kanalı destekle ilişkilendirmenin freenode açısından meşrulaştıracağını düşündüm 21:18:47 &lt;duck&gt; hypercubus: şaşırabilirsin 21:19:04 &lt;hypercubus&gt; *öksürür* itiraf edeyim tüm kuralları okumadım... 21:19:24 &lt;duck&gt; bu Rus ruleti 21:19:39 &lt;hypercubus&gt; hmm, bu kadar vahim olacağını düşünmemiştim 21:19:52  * duck negatif davranıyor 21:19:54 &lt;hypercubus&gt; peki, neler yapabileceğimize bakarım 21:20:09 &lt;fvw&gt; üzgünüm, bir şeyi kaçırmış olmalıyım. freenode bizi neden atar ki? 21:20:21  * duck mihi'nin breakpoint'i için zaman aşımı sayacına bakar 21:20:32 &lt;duck&gt; fvw: geliştirme kanallarına odaklanıyorlar 21:20:35 &lt;mihi&gt; ? 21:20:53 &lt;mihi&gt; duck: breakpoint /^4).*/ üzerinde tetiklenir 21:21:01 &lt;duck&gt; mihi: ama #4 yok 21:21:06 &lt;fvw&gt; e ne olmuş? i2p o kadar alfa ki şu anda destek bile geliştirme sayılır. 21:21:11 &lt;fvw&gt; (ve hayır, bunu benden alıntılayamazsın) 21:21:36 &lt;duck&gt; fvw: IIP'te gerçekleşen tartışma türlerine aşina olmayabilirsin 21:21:38 &lt;hypercubus&gt; evet ama bunun için *2* kanalımız var 21:21:45 &lt;duck&gt; ve muhtemelen #i2p kanallarında da olacak 21:22:04 &lt;duck&gt; freenode'un bunu hoş karşılamadığından oldukça eminim. 21:22:10 &lt;Nightblade&gt; şimdi buradayım 21:22:49 &lt;hypercubus&gt; onlara bir margarita makinesi falan bağışlarız 21:22:49 &lt;mihi&gt; duck: neyden bahsediyorsun? flood'lardan mı? yoksa #cl? nedir? 21:23:08 &lt;fvw&gt; IIP üzerindeki tartışmalar mı yoksa #iip üzerindekiler mi? #iip'te geliştirme ve destek dışında bir şey görmedim. Ve IIP üzerindeki tartışmalar #i2p@freenode'a değil, I2P'ye taşınır. 21:23:09 &lt;duck&gt; her türden politik doğruculuğa uygun olmayan muhabbet 21:23:36 &lt;fvw&gt; margarita makineleri mi var? Ooh, ben de isterim. 21:23:54 &lt;duck&gt; neyse 21:24:38 &lt;hypercubus&gt; 2)'yi yeniden ele alalım mı? 21:24:58 &lt;duck&gt; hypercubus: tarayıcı vekil sunucusu (proxy) hakkında ekleyeceğin ne var? 21:25:18 &lt;hypercubus&gt; oops, numara 1... çünkü nightblade az önce varlığıyla bizi şereflendirdi ;-) 21:25:33 &lt;duck&gt; Nightblade: libsam'i 'tartışma' özgürlüğünü kendimizde gördük 21:25:42 &lt;Nightblade&gt; Tamam, birkaç şey söyleyeceğim 21:25:48 &lt;hypercubus&gt; ama evet, şimdi düşününce, tarayıcı işiyle ilgili listede gündeme gelmeyen bir şeyim de vardı 21:25:56 &lt;duck&gt; Nightblade: fvw bize biraz FreeBSD testi konusunda yardımcı olabileceğini söyledi 21:26:20 &lt;fvw&gt; Artık FreeBSD makinem yok ama FreeBSD makinelerinde hesaplarım var, bana test vakaları verin, memnuniyetle çalıştırırım. 21:27:02 &lt;Nightblade&gt; Libsam (C) kullanan bir C++ DHT (dağıtık karma tablo) üzerinde çalışmaya başladım.  Bu noktada üzerinde çok çalışmama rağmen özellikle ileri gidebilmiş değilim.  Şu anda DHT'deki düğümler SAM veri mesajı aracılığıyla birbirlerine "ping" atabiliyor 21:27:09 &lt;Nightblade&gt; bu süreçte libsam'de birkaç küçük hata buldum 21:27:18 &lt;Nightblade&gt; bunun yeni bir sürümünü ileride bir zamanda yayımlayacağım 21:27:51 &lt;ugha_node&gt; Nightblade: lütfen libsam'deki 'strstr' çağrılarını kaldırabilir misin? :) 21:27:52 &lt;Nightblade&gt; test vakası şu: derlemeyi deneyin ve hataları bana bildirin 21:28:01 &lt;Nightblade&gt; strstr ile ne sorun var 21:28:21 &lt;ugha_node&gt; strcmp yerine kullanılmak için tasarlanmamıştır. 21:28:38 &lt;Nightblade&gt; ayrıca libsam'i Windows'a port etmeyi de düşünüyorum, ama bu yakın zamanda değil 21:29:07 &lt;Nightblade&gt; estetik dışında, onu kullanma biçimimde bir sorun var mı? 21:29:15 &lt;Nightblade&gt; bana değişiklikleri gönderebilir veya neyi tercih edeceğini söyleyebilirsin 21:29:19 &lt;Nightblade&gt; bu en kolay yol gibi görünmüştü 21:29:21 &lt;ugha_node&gt; Nightblade: herhangi birine rastlamadım. 21:29:32 &lt;fvw&gt; strcmp elbette strstr'den daha verimlidir. 21:29:36 &lt;ugha_node&gt; Ama sadece hızlıca göz attım. 21:30:20 &lt;ugha_node&gt; fvw: bazı durumlarda strcmp yerine strstr kullanan şeyleri istismar edebilirsin, ama burada öyle değil. 21:31:22 &lt;Nightblade&gt; evet, şimdi değiştirebileceğim bazı yerleri görüyorum 21:31:28 &lt;fvw&gt; o da var, ama onu fark etmiş olacağını varsayıyorum. Aslında, bu açıkları önlemek için strncmp kullanman gerekir. Ama bu konunun dışında. 21:31:31 &lt;Nightblade&gt; neden öyle yaptığımı hatırlamıyorum 21:31:57 &lt;ugha_node&gt; fvw: katılıyorum. 21:32:27 &lt;Nightblade&gt; ah, şimdi nedenini hatırladım 21:32:40 &lt;Nightblade&gt; strncmp için uzunluğu hesaplamak zorunda kalmamanın tembelce bir yolu 21:32:49 &lt;duck&gt; heh 21:32:52 &lt;ugha_node&gt; Nightblade: heheh. 21:33:01 &lt;fvw&gt; min(strlen(foo), sizeof(*foo)) kullan 21:33:04 &lt;hypercubus&gt; şaplaklamaya başlayalım mı? 21:33:15 &lt;fvw&gt; oral seksin önce geldiğini sanıyordum? *eğilir* 21:33:32 &lt;fvw&gt; peki, sıradaki madde sanırım. Hypercube'ün proxy'leme hakkında bir yorumu vardı? 21:33:38 &lt;hypercubus&gt; heh 21:33:54 &lt;duck&gt; gelsin bakalım! 21:34:03 &lt;Nightblade&gt; bir sonraki sürüm için değişiklikleri yapacağım - en azından bazılarında 21:34:25 &lt;hypercubus&gt; tamam, bu birkaç hafta önce kanalda kısaca konuşulmuştu, ama bence yeniden ele alınmayı hak ediyor 21:34:48 &lt;deer&gt; * Sugadude oral seksi gerçekleştirmek için gönüllü olur. 21:34:59 &lt;hypercubus&gt; tarayıcının engelleme listesine TLD'ler eklemek veya proxy betiğini kullanmak yerine, üçüncü bir yol var 21:35:29 &lt;hypercubus&gt; anonimlik açısından diğer iki yaklaşımla aynı sakıncalara sahip olmamalı 21:36:17 &lt;fvw&gt; bunu size yalnızca 29,99$ gibi ucuz mu ucuz bir fiyata mı anlatacağım? Hadi dökül artık! 21:36:27 &lt;hypercubus&gt; ve bu da eeproxy'nin gelen HTML sayfalarını yeniden yazarak sayfayı bir frameset içine gömmesi olurdu...  21:36:58 &lt;hypercubus&gt; ana frame istenen HTTP içeriğini içerir, diğer frame ise bir kontrol çubuğu görevi görür 21:37:13 &lt;hypercubus&gt; ve proxy'lemeyi istediğin gibi açıp kapatmana izin verir 21:37:40 &lt;hypercubus&gt; ve ayrıca renkli kenarlıklar ya da başka bir tür uyarı ile anonim olmayan şekilde gezinmekte olduğunu sana bildirir 21:37:54 &lt;fvw&gt; bir i2p sitesinin (JavaScript vb. ile) anonimliği kapatmasını nasıl engelleyeceksin? 21:37:59  * duck jrandom-skill-level-of toleransını uygulamaya çalışır 21:37:59 &lt;hypercubus&gt; ya da bir eepsite sayfasındaki bir bağlantının RealWeb(tm)'e götürdüğünü 21:38:04 &lt;duck&gt; harika! yap bunu! 21:38:16 &lt;fvw&gt; yine de fproxy benzeri bir şey yapman ya da geçiş için tarayıcı tarafından kontrol edilmeyen bir şey yapman gerekecek. 21:38:29 &lt;ugha_node&gt; fvw: Doğru. 21:39:10 &lt;hypercubus&gt; bu yüzden bunu tekrar buraya ortaya atıyorum, belki biri bunu nasıl güvenceye alabileceğimize dair bazı fikirler sunar 21:39:31 &lt;hypercubus&gt; ama bence bu, çoğu i2p son kullanıcılr için şiddetle ihtiyaç duyulacak bir şey 21:39:33 &lt;hypercubus&gt; *kullanıcılar 21:40:04 &lt;hypercubus&gt; çünkü TLD/proxy betiği/ayrı bir tarayıcı yaklaşımları sıradan bir internet kullanıcısından beklemek için fazla 21:40:29 &lt;fvw&gt; Uzun vadede, fproxy benzeri çalışan bir şeyin en iyi fikir olduğunu düşünüyorum. Ama bu bence kesinlikle bir öncelik değil ve aslında sitelerde gezinmenin i2p'nin killer app'i olacağını da sanmıyorum. 21:40:42 &lt;Sonium&gt; netDb nedir ki? 21:40:59 &lt;duck&gt; Sonium: bilinen router'ların veritabanı 21:41:10 &lt;hypercubus&gt; fproxy çoğu kullanıcı için fazla hantal 21:41:32 &lt;Sonium&gt; böyle bir veritabanı anonimliği zedelemez mi? 21:41:39 &lt;hypercubus&gt; bence bu, freenet'in geliştirici olmayan toplulukta hiçbir zaman tutmamasının nedenlerinden biri 21:41:41 &lt;fvw&gt; hypercube: şart değil. proxy otomatik yapılandırma ("pac") tarayıcı yapılandırmana tek bir değer girmeye indirgeme kadar basit hale getirebilir. Bence ön görülebilir gelecekte, tüm i2p kullanıcılarının bilgisayar konusunda en azından az biraz bilinçli olacağını küçümsememeliyiz. (freenet-support'taki tüm kanıtlara rağmen) 21:42:00 &lt;ugha_node&gt; Sonium: Hayır, 'kötü adamlar' o bilgiyi zaten elle toplayabilirler. 21:42:21 &lt;Sonium&gt; ama NetDb çökerse i2p de çöker, değil mi? 21:42:29 &lt;fvw&gt; hypercubus: Pek değil, bence bunun başlıca nedeni 0.5'in başlarından beri hiç çalışmamış olmasıdır. &lt;/offtopic time="once again"&gt;

21:42:44 &lt;fvw&gt; Sonium: birden fazla netdb'in olabilir (herkes bir tane çalıştırabilir)
21:42:58 &lt;hypercubus&gt; zaten pac'imiz var ve teknik açıdan müthiş çalışmasına rağmen, gerçekçi                         olarak avg. jog'un anonimliğini korumayacak
21:43:03 &lt;hypercubus&gt; *avg. joe
21:43:22 &lt;ugha_node&gt; fvw: Şey.. Her router'ın kendi netDb'si vardır.
21:43:42 &lt;duck&gt; tamam. bayılmak üzereyim. işiniz bitince toplantıyı *baff* ederek kapattığınızdan                   emin olun
21:43:52 &lt;ugha_node&gt; I2P'nin artık merkezi bağımlılıkları yok.
21:44:07 &lt;hypercubus&gt; tamam, ben sadece bu fikri resmen kayıtlara geçirmek istedim ;-)
21:44:30 &lt;fvw&gt; ugha_node: tamam, o zaman yayımlanmış bir netdb. Aslında bir düğüm çalıştırmıyorum (henüz), terminolojiye                  tamamen hâkim değilim.
21:44:34 &lt;ugha_node&gt; Hmm. mihi bir şey söylemek istemiyor muydu?
21:45:05  * fvw duck'ı biraz daha ayakta ve çalışır halde tutmak için kahve aromalı çikolata            yedirir.
21:45:07 &lt;mihi&gt; hayır :)
21:45:21 &lt;mihi&gt; duck bir ağ cihazı mı? ;)
21:45:25 &lt;ugha_node&gt; mihi: Bu arada, pencere boyutunu artırma ödülünü alacak mısın?
21:45:28  * fvw duck'a onu süresiz kapatmak için alkol aromalı çikolata yedirir.
21:45:30 &lt;hypercubus&gt; İsveççe
21:45:52 &lt;mihi&gt; ugha_node: hangi ödül?
21:46:00 &lt;hypercubus&gt; tamam, o zaman 5)'e geçelim, söylenme seansı? ;-)
21:46:13 &lt;ugha_node&gt; mihi: http://www.i2p.net/node/view/224
21:46:27  * duck fvw'nun çikolatasından biraz yer
21:47:16 &lt;mihi&gt; ugha_node: kesinlikle hayır; üzgünüm
21:47:36 &lt;ugha_node&gt; mihi: Ah, tamam. :(
21:48:33  * mihi bir süre önce "eski" akış API'sini hack'lemeye çalıştı, ama o çok            hatalıydı...
21:48:53 &lt;mihi&gt; ama bence benimkini düzeltmek yerine onu düzeltmek daha kolay olur...
21:49:21 &lt;ugha_node&gt; Heh.
21:49:42 &lt;hypercubus&gt; ne kadar mütevazı
21:49:46 &lt;mihi&gt; çünkü zaten içinde bazı (bozuk) "yeniden sıralama" desteği var
21:50:49 &lt;Sonium&gt; i2p-#i2p kanalında kaç kişi olduğunu deer'e sormanın bir yolu var mı?
21:51:01 &lt;duck&gt; hayır
21:51:08 &lt;hypercubus&gt; hayır, ama bunu bogobot'a ekleyebilirim
21:51:08 &lt;Sonium&gt; :/
21:51:11 &lt;Nightblade&gt; !list
21:51:13 &lt;deer&gt; &lt;duck&gt; 10 kişi
21:51:13 &lt;hypercubus&gt; yükleyiciyi bitirdikten sonra ;-)
21:51:24 &lt;Sonium&gt; !list
21:51:32 &lt;Sonium&gt; o_O
21:51:35 &lt;mihi&gt; Sonium ;)
21:51:38 &lt;ugha_node&gt; Burası bir fserv kanalı değil!
21:51:39 &lt;Sonium&gt; bu bir hileydi!
21:51:40 &lt;ugha_node&gt; :)
21:51:41 &lt;hypercubus&gt; !who olmalı
21:51:44 &lt;deer&gt; &lt;duck&gt; ant duck identiguy Pseudonym ugha2p bogobot hirvox jrandom Sugadude                   unknown
21:51:48 &lt;cervantes&gt; ops, toplantıyı kaçırdım
21:51:57 &lt;ugha_node&gt; !list
21:52:01 &lt;Nightblade&gt; !who
21:52:11 &lt;deer&gt; &lt;duck&gt; !who-your-mom
21:52:17 &lt;mihi&gt; !who !has !the !list ?
21:52:21 &lt;fvw&gt; !yesletsallspamthechannelwithinoperativecommands
21:52:33 &lt;Nightblade&gt; !ban fvw!*@*
21:52:42 &lt;mihi&gt; !ban *!*@*
21:52:50 &lt;hypercubus&gt; bir tokmağın ineceğini hissediyorum
21:52:51 &lt;duck&gt; kapatmak için iyi bir zamana benziyor
21:52:55 &lt;Sonium&gt; bu arada, chanserv'de olduğu gibi bir !8 komutunu da uygulamalısın
21:52:59 &lt;fvw&gt; peki, bunu hallettiğimize göre, haydi kap.. evet. o.
21:53:00  * hypercubus medyum
21:53:05 &lt;duck&gt; *BAFF*
21:53:11 &lt;Nightblade&gt; !baff
21:53:12 &lt;hypercubus&gt; saçım, saçım
21:53:24  * fvw hypercube'ü işaret eder ve güler. Saçın! Saçın! </div>
