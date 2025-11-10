---
title: "2005-08-30 için I2P Durum Notları"
date: 2005-08-30
author: "jr"
description: "NAT sorunları, floodfill netDb dağıtımı ve Syndie uluslararasılaştırma ilerlemesiyle birlikte 0.6.0.3 ağ durumunu ele alan haftalık güncelleme"
categories: ["status"]
---

Selam millet, yine haftanın o vakti geldi.

* Index

1) Ağ durumu 2) floodfill netDb 3) Syndie 4) ???

* 1) Net status

0.6.0.3 bir haftadır yayında; raporlar oldukça iyi, ancak günlükleme ve görüntüleme bazıları için epey kafa karıştırıcı oldu. Birkaç dakika önce itibarıyla I2P, hatırı sayılır sayıda kişinin NAT’lerini veya güvenlik duvarlarını yanlış yapılandırdığını bildiriyor — 241 eşten 41’i durumun ERR-Reject’e geçtiğini görürken, 200’ü ise doğrudan OK oldu (açık bir durum alabilecekleri zaman). Bu iyi değil, ancak ne yapılması gerektiğine biraz daha odaklanmaya yardımcı oldu.

Since the release, there have been a few bugfixes for long standing error conditions, bringing the current CVS HEAD up to 0.6.0.3-4, which will likely be pushed out as 0.6.0.4 later this week.

* 2) floodfill netDb

Blogumda [2] tartışıldığı [1] gibi, hem gördüğümüz kısıtlı rota durumunu (router'ların %20'si) ele alacak hem de işleri biraz basitletecek, geriye dönük uyumlu yeni bir netDb deniyoruz. floodfill netDb, 0.6.0.3-4'ün bir parçası olarak ek bir yapılandırma gerektirmeden devreye alındı ve temel olarak, mevcut kademlia db'ye geri dönmeden önce floodfill db içinde sorgulama yaparak çalışıyor. Birkaç kişi denemeye yardımcı olmak isterse, 0.6.0.3-4'e geçip bir deneyin!

[1] http://syndiemedia.i2p.net/index.jsp?selector=entry://ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1125100800001 [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 3) Syndie

Syndie'nin geliştirilmesi oldukça iyi ilerliyor; tam remote syndication (uzaktan dağıtım) kullanımda ve I2P'nin gereksinimlerine göre optimize edilmiş durumda (HTTP isteklerinin sayısını en aza indirip, sonuçları ve yüklemeleri multipart HTTP POST isteklerinde paketleyerek). Yeni remote syndication ile kendi yerel Syndie örneğinizi çalıştırabilir, çevrimdışı olarak okuyup gönderi yayımlayabilir ve daha sonra Syndie'nizi bir başkasınınkiyle senkronize edebilirsiniz - yeni gönderileri indirip yerelde oluşturduklarınızı karşıya yükleyerek (ister toplu halde, ister blog bazında, ister gönderi bazında).

Genel bir Syndie sitesi syndiemedia.i2p'dir (web üzerinden http://syndiemedia.i2p.net/ adresinden de erişilebilir) ve kamuya açık arşivlerine http://syndiemedia.i2p/archive/archive.txt adresinden erişilebilir (senkronize etmek için Syndie düğümünüzü oraya yönlendirin). O syndiemedia'daki 'ön sayfa' varsayılan olarak yalnızca benim blogumu içerecek şekilde filtrelenmiştir, ancak açılır menü üzerinden diğer bloglara hâlâ erişebilir ve varsayılanınızı buna göre ayarlayabilirsiniz. (zamanla, syndiemedia.i2p'nin varsayılanı, syndie'ye iyi bir giriş noktası sağlayacak bir dizi tanıtıcı gönderi ve blogdan oluşacak şekilde değişecektir).

Hâlâ devam eden çalışmalardan biri, Syndie kod tabanının uluslararasılaştırılması. Yerel kopyamı, herhangi bir içerikle (herhangi bir karakter kümesi / locale (bölgesel ayarlar) / vb.) herhangi bir makinede (muhtemelen farklı karakter kümeleri / locale / vb. ile) düzgün çalışacak şekilde değiştirdim ve veriyi temiz biçimde sunarak kullanıcının tarayıcısının onu doğru şekilde yorumlayabilmesini sağladım. Yine de, Syndie'nin kullandığı bir Jetty bileşeninde sorunlarla karşılaştım; çünkü uluslararasılaştırılmış multipart isteklerle ilgilenen sınıfı karakter kümesini gözetmiyor. Henüz ;)

Neyse, bu, uluslararasılaştırma kısmı halledildiğinde, içerik ve blogların tüm dillerde (ama elbette, henüz çevrilmiş olmayacak) görüntülenebilir ve düzenlenebilir olacağı anlamına geliyor. O zamana kadar ise, imzalı içerik alanlarının içinde UTF-8 karakter dizileri bulunduğundan, oluşturulan içerik uluslararasılaştırma tamamlandığında bozulabilir. Yine de, dilediğiniz gibi kurcalamaktan çekinmeyin ve umarım işleri bu gece ya da yarın bir ara bitireceğim.

Ayrıca, SML [3] için hâlâ ufukta olan bazı fikirler arasında, insanların ekli torrent'i en sevdikleri BT istemcisinde (susibt, i2p-bt, azneti2p ya da hatta I2P olmayan bir BT istemcisi) tek tıklamayla başlatmasına olanak tanıyacak bir [torrent attachment="1"]my file[/torrent] etiketi de var. Başka tür kancalara (ör. bir [ed2k] etiketi?) talep var mı, yoksa insanlar Syndie’de içeriği yaymak için tamamen farklı çılgın fikirler mi düşünüyor?

[3] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1124496000000

* 4) ???

Neyse, bir sürü şey oluyor; bu yüzden 10 dakika sonra irc://irc.{postman,arcturus,freshcoffee}.i2p/#i2p veya freenode.net üzerinden toplantıya uğrayın!

=jr
