---
title: "I2P'nin 2005-08-23 tarihli Durum Notları"
date: 2005-08-23
author: "jr"
description: "0.6.0.3 sürüm iyileştirmelerini, Irc2P ağ durumunu, i2p-bt için susibt web arayüzünü ve Syndie ile güvenli bloglamayı kapsayan haftalık güncelleme"
categories: ["status"]
---

Herkese selam, yine haftalık durum notlarının zamanı geldi

* Index

1) 0.6.0.3 durumu 2) IRC durumu 3) susibt 4) Syndie 5) ???

* 1) 0.6.0.3 status

Geçen gün [1] belirtildiği gibi, kullanımınıza hazır yeni bir 0.6.0.3 sürümümüz yayımlandı. 0.6.0.2 sürümüne göre büyük bir iyileştirme (irc'de günlerce bağlantı kopmadan kalmak pek de nadir değil - bir yükseltme ile bölünen 5 günlük kesintisiz çalışma sürelerim oldu), ancak değinmeye değer birkaç nokta var. Yine de her zaman böyle olmuyor - yavaş internet bağlantısına sahip kişiler sorunlarla karşılaşabiliyor, ama bu yine de bir ilerleme.

Eş testi koduyla ilgili (çok) yaygın bir soru ortaya çıktı-"Neden Status: Unknown yazıyor?" Unknown *tamamen normaldir* - bu KESİNLİKLE bir sorunun göstergesi değildir. Ayrıca, bazen "OK" ile "ERR-Reject" arasında gidip geldiğini görürseniz, bu her şeyin yolunda olduğu ANLAMINA GELMEZ - bir kez bile ERR-Reject görürseniz, bu büyük olasılıkla NAT (Ağ Adresi Çevirisi) veya güvenlik duvarı sorunu yaşadığınız anlamına gelir. Biliyorum, kafa karıştırıcı ve daha sonra daha anlaşılır bir durum gösterimi (ve mümkün olduğunda otomatik çözüm) içeren bir sürüm çıkacak, ancak şimdilik, "omg bozulmuş!!!11 durum Unknown!" dediğinizde sizi görmezden gelirsem şaşırmayın ;)

(Aşırı sayıdaki 'Unknown' durum değerlerinin nedeni, "Charlie" [2]'nin halihazırda SSU oturumuna sahip olduğumuz biri olduğu peer tests (eş testleri) durumlarını yok saymamızdır; çünkü bu, NAT'ımız bozuk olsa bile NAT'ımızı aşabileceklerini ima eder)

[1] http://dev.i2p.net/pipermail/i2p/2005-August/000844.html [2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#peerTesting

* 2) IRC status

Yukarıda belirtildiği gibi, Irc2P operatörleri ağlarıyla harika bir iş çıkardılar; gecikme belirgin biçimde azaldı ve güvenilirlik belirgin biçimde arttı - günlerdir netsplit (ağ bölünmesi) görmedim. Orada yeni bir irc sunucusu da var; böylece sayımız 3 oldu - irc.postman.i2p, irc.arcturus.i2p ve irc.freshcoffee.i2p. Belki Irc2P ekibinden biri toplantı sırasında ilerlemeleri hakkında bize bir güncelleme verebilir?

* 3) susibt

susimail ile ünlenen susi23, BT (BitTorrent) ile ilgili iki araçla geri döndü - susibt [3] ve yeni bir tracker (izleyici) botu [4]. susibt, i2p-bt'nin işleyişini yönetmek için bir web uygulamasıdır (i2p jetty örneğinizde zahmetsizce kurulabilir). Sitesinde söylediği gibi:

SusiBT, i2p-bt için bir web arayüzüdür. i2p router’ınıza (yönlendirici) entegre olur ve otomatik yükleme ve indirmelere, yeniden başlatmanın ardından kaldığı yerden devam etmeye ve dosya yükleme ile indirme gibi bazı yönetim işlevlerine olanak tanır. Uygulamanın daha sonraki sürümleri torrent dosyalarının otomatik olarak oluşturulmasını ve yüklenmesini destekleyecektir.

[3] http://susi.i2p/?page_id=31 [4] http://susi.i2p/?p=33

Bir "w00t" alabilir miyim?

* 4) Syndie

Listede ve kanalda belirtildiği gibi, güvenli ve kimlik doğrulamalı bloglama / içerik dağıtımı için yeni bir istemci uygulamamız var. Syndie ile, "eepsite(I2P Site)'ınız açık mı" sorusu ortadan kalkıyor, çünkü site kapalıyken bile içeriği okuyabiliyorsunuz; ayrıca Syndie, ön yüze odaklanarak içerik dağıtım ağlarının doğasında bulunan tüm çirkin sorunlardan kaçınıyor. Neyse, hâlâ üzerinde çalışılan bir proje, ama insanlar girip denemek isterse, http://syndiemedia.i2p/ adresinde herkese açık bir Syndie düğümü var (web üzerinden http://66.111.51.110:8000/ adresinden de erişilebilir). Oraya girip bir blog oluşturmakta özgürsünüz; ya da kendinizi maceraperest hissediyorsanız, birkaç yorum/öneri/endişe hakkında bloglayın! Elbette yamalar memnuniyetle karşılanır; özellik önerileri de öyle, o yüzden çekinmeden gönderin.

* 5) ???

Bir sürü şey oluyor demek biraz hafif kalır... yukarıdakilere ek olarak, SSU'nun tıkanıklık kontrolünde (-1 zaten cvs'de), bant genişliği sınırlayıcımızda ve netDb üzerinde (ara sıra görülen site erişilemezliği için) bazı iyileştirmeler üzerinde çalışıyorum; ayrıca forumda bildirilen CPU sorununda da hata ayıklıyorum. Eminim başkaları da rapor edilecek bazı havalı şeyler üzerinde çalışıyordur, bu yüzden umarım bu akşamki toplantıya uğrayıp uzun uzun anlatırlar :)

Neyse, bu akşam 20:00 GMT'de her zamanki sunuculardaki #i2p kanalında görüşürüz!

=jr
