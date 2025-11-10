---
title: "2005-08-16 tarihli I2P Durum Notları"
date: 2005-08-16
author: "jr"
description: "PeerTest durumu, Irc2P ağındaki geçiş, Feedspace GUI'deki ilerleme ve toplantı saatinin GMT 20:00'ye alınması konularını kapsayan kısa bir güncelleme"
categories: ["status"]
---

Herkese selam, bugün kısa notlar

* Index:

1) PeerTest durumu 2) Irc2P 3) Feedspace 4) meta 5) ???

* 1) PeerTest status

Daha önce belirtildiği gibi, yaklaşan 0.6.1 sürümü, router'ı daha dikkatli yapılandırmak ve erişilebilirliği doğrulamak (ya da ne yapılması gerektiğini belirtmek) için bir dizi test içerecek ve son iki derlemeden beri CVS'de bazı kodlarımız olsa da, gereken düzeyde sorunsuz çalışması için hâlâ bazı ince ayarlar gerekiyor. Şu anda, [1]'de belgelenen test akışında, Charlie'nin erişilebilirliğini doğrulamak için ek bir paket ekleyerek ve Charlie yanıt verene kadar Bob'un Alice'e yanıtını geciktirerek bazı küçük değişiklikler yapıyorum. Bu, Bob test için hazır bir Charlie bulana kadar Alice'e yanıt vermeyeceğinden, insanların gördüğü gereksiz "ERR-Reject" durum değerlerinin sayısını azaltmalıdır (ve Bob yanıt vermediğinde, Alice durum olarak "Unknown" görür).

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html#peerTesting

Her neyse, evet, bu kadar - yarın 0.6.0.2-3 çıkmış olmalı, iyice test edildiğinde sürüm olarak yayınlanacak.

* 2) Irc2P

Forumda belirtildiği gibi [2], IRC kullanan I2P kullanıcılarının yeni IRC ağına geçmek için yapılandırmalarını güncellemeleri gerekiyor. Duck, [redacted] için geçici olarak çevrimdışı olacak ve o süre zarfında sunucunun sorun yaşamamasını ummak yerine, postman ve smeghead devreye girip sizin kullanımınız için yeni bir IRC ağı kurdular. Postman ayrıca duck’ın tracker’ını (izleyici) ve i2p-bt sitesini [3]'te yansıladı ve sanırım susi’nin yeni bir IdleRPG örneği başlattığına dair yeni IRC ağında bir şeyler gördüm (daha fazla bilgi için kanal listesine bakın).

Eski i2pirc ağından (duck, baffled, the metropipe crew, postman) sorumlu olanlara ve yeni irc2p ağından (postman, arcturus) sorumlu olanlara teşekkürlerimi sunarım! İlginç hizmetler ve içerik I2P'yi değerli kılıyor ve onları oluşturmak sizlere düşüyor!

[2] http://forum.i2p.net/viewtopic.php?t=898 [3] http://hq.postman.i2p/

* 3) Feedspace

Hazır konusu açılmışken, geçen gün frosk'un blogunu okuyordum ve Feedspace üzerinde biraz daha ilerleme olduğunu gördüm - özellikle de hoş, minik bir GUI (grafiksel kullanıcı arayüzü) konusunda. Test etmeye henüz hazır olmayabileceğini biliyorum, ama zamanı gelince frosk'un bize biraz kod yollayacağından eminim. Bu arada, hazır olduğunda Feedspace'e entegre olabilecek başka bir anonimlik odaklı web tabanlı blog aracının da yolda olduğuna dair bir söylenti duydum; ama yine, hazır olduğunda bununla ilgili daha fazla bilgi alacağımızdan eminim.

* 4) meta

Ben de açgözlü bir herif olduğumdan, toplantıları biraz öne çekmek istiyorum - GMT 21:00 yerine GMT 20:00'yi deneyelim. Neden? Çünkü programıma daha iyi uyuyor ;) (en yakın internet kafeler çok geç saatlere kadar açık değiller).

* 5) ???

Şimdilik bu kadar - Bu akşamki toplantı için bir net kafenin yakınlarında olmaya çalışacağım, bu yüzden GMT *8*P'de /new/ irc sunucularındaki {irc.postman.i2p, irc.arcturus.i2p} #i2p kanalına uğramaktan çekinmeyin. irc.freenode.net'e bir changate botumuz olabilir - birini çalıştırmak isteyen var mı?

selam, =jr
