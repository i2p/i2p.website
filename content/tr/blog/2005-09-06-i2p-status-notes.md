---
title: "2005-09-06 tarihli I2P Durum Notları"
date: 2005-09-06
author: "jr"
description: "0.6.0.5 sürümünün başarıyla yayımlanmasını, floodfill netDb performansını, Syndie'nin RSS ve takma adlarla ilgili ilerlemesini ve yeni susidns adres defteri yönetim uygulamasını kapsayan haftalık güncelleme"
categories: ["status"]
---

Herkese merhaba,


* Index

1) Ağ durumu 2) Syndie durumu 3) susidns 4) ???

* 1) Net status

Birçoğunun gördüğü üzere, kısa bir 0.6.0.4 revizyonunun ardından 0.6.0.5 sürümü geçen hafta yayımlandı ve şu ana kadar güvenilirlik büyük ölçüde iyileşti; ağ da her zamankinden daha büyük hale geldi. Hala biraz iyileştirme payı var, ancak yeni netDb'nin tasarlandığı gibi çalıştığı görülüyor. Hatta yedek yol (fallback) da test edildi - floodfill eşlerine ulaşılamadığında, router'lar kademlia netDb'ye geri dönüyor ve geçen gün bu senaryo gerçekleştiğinde, irc ve eepsite(I2P sitesi) güvenilirliği kayda değer ölçüde azalmadı.

Yeni netDb'nin nasıl çalıştığıyla ilgili bir soru aldım ve yanıtı [1] blogumda [2] yayımladım. Her zamanki gibi, bu tür konularda herhangi bir sorusu olan varsa, lütfen bana iletmekten çekinmeyin; ister listede ister liste dışında, forumda ya da hatta blogunuzda ;)

[1] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1125792000000&expand=true [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 2) Syndie status

syndiemedia.i2p (ve http://syndiemedia.i2p.net/) üzerinden de görebileceğiniz gibi, son zamanlarda epey ilerleme kaydedildi; RSS, pet names (özel adlar yaklaşımı), yönetimsel kontroller ve makul css kullanımına yönelik ilk adımlar dahil. Isamoor'un önerilerinin çoğu uygulamaya kondu, Adam'ınkiler de öyle; bu yüzden, orada görmek istediğiniz bir şey varsa, lütfen bana bir mesaj atın!

Syndie artık beta’ya oldukça yakın; o aşamada hem varsayılan I2P uygulamalarından biri olarak dağıtıma dahil edilecek hem de bağımsız paket olarak sunulacak, bu nedenle her türlü yardım büyük memnuniyetle karşılanacaktır. Bugünkü en son eklemelerle (cvs içinde), Syndie için skinning (tema uygulama) da artık çok kolay - i2p/docs/ dizininizde yeni bir syndie_standard.css dosyası oluşturmanız yeterli; belirtilen stiller Syndie’nin varsayılanlarını geçersiz kılacaktır. Bununla ilgili daha fazla bilgiye blogumda [2] ulaşabilirsiniz.

* 3) susidns

Susi bizim için bir web uygulaması daha hızlıca geliştirdi - susidns [3]. Bu, addressbook uygulamasını yönetmek için basit bir arayüz sağlıyor - kayıtları, abonelikleri vb. Oldukça iyi görünüyor; umarız yakında bunu varsayılan uygulamalardan biri olarak sunabileceğiz, ama şimdilik çocuk oyuncağı: onu eepsite(I2P Site)'inden indirip webapps dizininize kaydedin, router'ınızı yeniden başlatın ve hazırsınız.

[3] http://susi.i2p/?page_id=13

* 4) ???

İstemci uygulaması tarafına kesinlikle odaklandık (ve bunu yapmaya da devam edeceğiz), ancak zamanımın büyük bir kısmı hâlâ ağın çekirdek işleyişine odaklanıyor ve yolda heyecan verici gelişmeler var - introductions (aracılar üzerinden tanıştırma) ile güvenlik duvarı ve NAT aşma, geliştirilmiş SSU otomatik yapılandırması, gelişmiş eş sıralaması ve seçimi ve hatta bazı basit kısıtlı rota işleme. Web sitesi cephesinde ise HalfEmpty stil sayfalarımızda bazı iyileştirmeler yaptı (yaşasın!).

Her neyse, bir sürü şey oluyor; şu anda bahsetmeye zaman bulabildiklerim şimdilik bu kadar, ama UTC 20:00'deki toplantıya uğrayıp bir merhaba deyin :)

=jr
