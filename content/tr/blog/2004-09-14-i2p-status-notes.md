---
title: "2004-09-14 tarihli I2P Durum Notları"
date: 2004-09-14
author: "jr"
description: "0.4.0.1 sürümünü, tehdit modeli güncellemelerini, web sitesi iyileştirmelerini, yol haritası değişikliklerini ve istemci uygulama geliştirme ihtiyaçlarını kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Selam millet, haftanın o vakti yine geldi

## Dizin:

1. 0.4.0.1
2. Threat model updates
3. Website updates
4. Roadmap
5. Client apps
6. ???

## 1) 0.4.0.1

Geçen Çarşamba’daki 0.4.0.1 sürümünden bu yana, ağda işler oldukça iyi gidiyor - ağın üçte ikisinden fazlası güncellendi ve ağda router sayısını 60 ile 80 arasında tutuyoruz. IRC bağlantı süreleri değişken, ancak son zamanlarda 4-12 saatlik bağlantılar normal hale geldi. Yine de OS/X üzerinde başlatma sırasında bazı tuhaflıklara dair raporlar geldi, ancak bu cephede de bazı ilerlemeler kaydedildiğine inanıyorum.

## 2) Tehdit modeli güncellemeleri

Toni’nin gönderisine yanıt olarak belirtildiği gibi, tehdit modelinde oldukça kapsamlı bir revizyon yapıldı. Ana fark, tehditleri eskiden olduğu gibi ad hoc bir şekilde ele almak yerine, literatürde sunulan bazı sınıflandırmaları izlemeye çalışmış olmam. Benim için en büyük sorun, insanların kullanabileceği gerçek teknikleri sunulan kalıplara uydurmanın yollarını bulmaktı — çoğu zaman tek bir saldırı birden fazla farklı kategoriye uyuyordu. Bu nedenle, o sayfadaki bilgilerin nasıl aktarıldığından pek memnun değilim, ama eskisinden daha iyi.

## 3) Web sitesi güncellemeleri

Curiosity’nin yardımı sayesinde, web sitesinde bazı güncellemelere başladık - bunların en görünür olanını doğrudan ana sayfada görebilirsiniz. Bu, I2P’ye rastlayan ve çeşitli sayfaları didik didik etmek zorunda kalmadan, ilk anda şu I2P denen şeyin ne olduğunu öğrenmek isteyen insanlara yardımcı olmalı. Her neyse, ilerleme var; daima ileri :)

## 4) Yol Haritası

İlerleme demişken, sonunda, uygulamamız gerektiğini düşündüğüm unsurlara ve kullanıcının ihtiyaçlarını karşılamak için yapılması gerekenlere dayanarak yenilenmiş bir yol haritasını bir araya getirdim. Eski yol haritasındaki başlıca değişiklikler şunlardır:

- Drop AMOC altogether, replaced with UDP (however, we'll support TCP for those who can't use UDP *cough*mihi*cough*)
- Kept all of the restricted route operation to the 2.0 release, rather than bring in partial restricted routes earlier. I believe we'll be able to meet the needs of many users without restricted routes, though of course with them many more users will be able to join us. Walk before run, as they say.
- Pulled the streaming lib in to the 0.4.3 release, as we don't want to go 1.0 with the ~4KBps per stream limit. The bounty on this is still of course valid, but if no one claims it before 0.4.2 is done, I'll start working on it.
- TCP revamp moved to 0.4.1 to address some of our uglier issues (high CPU usage when connecting to people, the whole mess with "target changed identities", adding autodetection of IP address)

Çeşitli 0.4.* sürümleri için planlanan diğer öğeler zaten uygulandı. Ancak, yol haritasından çıkarılan başka bir öğe daha var...

## 5) İstemci uygulamaları

İstemci uygulamalara ihtiyacımız var. İlgi çekici, güvenli, ölçeklenebilir ve anonim uygulamalar. I2P tek başına çok fazla şey yapmaz; yalnızca iki uç noktanın anonim olarak birbirleriyle iletişim kurmasına olanak tanır. I2PTunnel tam bir İsviçre çakısı sunsa da, bu tür araçlar esasen aramızdaki teknoloji meraklıları için ilgi çekicidir. Bundan fazlasına ihtiyacımız var - insanların gerçekten yapmak istediklerini yapmalarını sağlayan ve bunu daha iyi yapmalarına yardımcı olan bir şeye ihtiyacımız var. İnsanların I2P’yi yalnızca daha güvenli olduğu için kullanmalarının ötesine geçen bir nedene ihtiyacımız var.

Şimdiye kadar o ihtiyacı karşılamak için MyI2P'yi öneriyordum - LiveJournal benzeri bir arayüz sunan dağıtık bir blog sistemi. Kısa süre önce listede MyI2P'nin bazı işlevlerini tartıştım. Ancak, bunu yol haritasından çıkardım; çünkü bu iş benim için yapılması gereğinden fazla ve bunu yaparken temel I2P ağına ihtiyaç duyduğu ilgiyi veremem (zaten son derece sıkışığız).

Çok umut vaat eden birkaç başka uygulama daha var. Stasher, dağıtık veri depolama için önemli bir altyapı sağlayacaktır, ancak bunun nasıl ilerlediğinden emin değilim. Stasher olsa bile, ilgi çekici bir kullanıcı arayüzüne ihtiyaç olacaktır (bazı FCP uygulamaları onunla çalışabilir).

IRC de güçlü bir sistemdir, ancak sunucu tabanlı mimarisi nedeniyle bazı sınırlamaları vardır. Bununla birlikte, oOo şeffaf DCC (Direct Client-to-Client - istemciden istemciye) uygulaması üzerinde bazı çalışmalar yaptı; dolayısıyla, belki de IRC tarafı herkese açık sohbet için ve DCC özel dosya aktarımları ya da sunucusuz sohbet için kullanılabilir.

Genel eepsite(I2P Site) işlevselliği de önemlidir ve şu anda sahip olduklarımız kesinlikle tatmin edici değil. DrWoo’nun belirttiği gibi, mevcut kurulumda ciddi anonimlik riskleri var ve oOo bazı başlıkları filtreleyen yamalar yapmış olsa da, eepsites(I2P Sites) güvenli sayılmadan önce yapılması gereken çok daha fazla iş var. Bunu ele almak için birkaç farklı yaklaşım var; hepsi işe yarayabilir, ancak hepsi de emek gerektiriyor. Bildiğim kadarıyla duck, birinin bir şey üzerinde çalıştığından bahsetmişti; ancak bunun ne aşamada olduğunu ya da herkesin kullanabilmesi için I2P ile birlikte paketlenip paketlenemeyeceğini bilmiyorum. Duck?

Yardımcı olabilecek bir başka istemci uygulama çifti, ya sürü mantığıyla çalışan bir dosya aktarım uygulaması (BitTorrent tarzı) ya da daha geleneksel bir dosya paylaşım uygulaması (DC/Napster/Gnutella vb. tarzı) olabilir. Bunu, çok sayıda insanın istediğini tahmin ediyorum; ancak bu sistemlerin her birinde sorunlar var. Yine de, iyi biliniyorlar ve port etmek çok da zahmetli olmayabilir (belki).

Tamam, yukarıdakiler yeni bir şey değil - peki neden hepsini gündeme getirdim? Şöyle ki, ilgi çekici, güvenli, ölçeklenebilir ve anonim bir istemci uygulamasını hayata geçirmenin bir yolunu bulmamız gerekiyor ve bu, durup dururken kendiliğinden olmayacak. Bunu tek başıma yapamayacağımı kabullendim, bu yüzden proaktif olmalı ve bunu gerçekleştirmek için bir yol bulmalıyız.

Bunu yapmak için, ödül sistemimizin yardımcı olabileceğini düşünüyorum, ancak bu konuda (bir ödülü hayata geçirmek için çalışan kişiler) pek fazla faaliyet görmememizin nedenlerinden birinin de insanların çok dağılmış olması olduğunu düşünüyorum. İhtiyacımız olan sonuçları elde etmek için, ne istediğimizi önceliklendirmemiz ve çabalarımızı en öncelikli maddeye odaklamamız gerektiğini hissediyorum; 'teklifi cazip hale getirerek' birinin öne çıkıp ödül üzerinde çalışmasını teşvik edebilmeyi umarak.

Kişisel kanaatim hâlâ, MyI2P gibi güvenli ve dağıtık bir blog sisteminin en iyisi olacağı yönünde. Verileri yalnızca anonim olarak bir yerden bir yere taşımak yerine, topluluklar inşa etmenin bir yolunu sunar; bu da herhangi bir geliştirme çabasının can damarıdır. Buna ek olarak, nispeten yüksek bir sinyal-gürültü oranı, ortak kaynakların kötüye kullanılma olasılığının düşük olması ve genel olarak hafif bir ağ yükü sunar. Bununla birlikte, normal web sitelerinin sunduğu tüm zenginliği sağlamaz; ancak 1,8 milyon aktif LiveJournal kullanıcısı bunu pek umursamıyor gibi görünüyor.

Bunun ötesinde, tarayıcılara ihtiyaç duydukları güvenliği sağlayan ve insanların eepsites(I2P Sites) 'kullanıma hazır' olarak sunmalarına olanak tanıyan eepsite(I2P Site) mimarisinin güvence altına alınması bir sonraki tercihim olurdu.

Dosya aktarımı ve dağıtık veri depolama da inanılmaz derecede güçlü, ancak ilk tipik son kullanıcı uygulaması için muhtemelen istediğimiz kadar topluluk odaklı görünmüyorlar.

Listedeki tüm uygulamaların dünden uygulanmış olmasını, ayrıca hayal bile edemediğim binlerce başka uygulamayı da istiyorum. Dünya barışını, açlığın sona ermesini, kapitalizmin yıkılmasını, devletçilikten, ırkçılıktan, cinsiyetçilikten, homofobiden kurtuluşu, çevrenin alenen yok edilmesine son verilmesini ve diğer tüm kötülüklerin ortadan kaldırılmasını da istiyorum. Ancak biz de sonuçta sayılı kişiyiz ve ancak bu kadarını başarabiliriz. Bu nedenle, yapmak istediğimiz her şeyin ağırlığı altında oturup kalmak yerine, yapabileceğimiz şeylere öncelik verip çabalarımızı bunları başarmaya odaklamalıyız.

Belki bu akşamki toplantıda ne yapmamız gerektiğine dair bazı fikirleri tartışabiliriz.

## 6) ???

Neyse, şimdilik bende bu kadar; hem de durum notlarını toplantıdan *önce* yazdım! O yüzden bahane yok, GMT’ye göre 21:00’de uğrayın ve hepimizi fikirlerinizle bombardımana tutun.

=jr
