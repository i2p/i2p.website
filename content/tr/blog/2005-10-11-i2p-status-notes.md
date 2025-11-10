---
title: "2005-10-11 için I2P Durum Notları"
date: 2005-10-11
author: "jr"
description: "0.6.1.2 sürümünün başarıyla yayımlanmasını, güvensiz IRC mesajlarını filtrelemek için yeni I2PTunnelIRCClient vekil sunucusunu, Syndie CLI ve RSS-to-SML dönüşümünü ve I2Phex entegrasyon planlarını kapsayan haftalık güncelleme"
categories: ["status"]
---

Selam millet, yine salı

* Index

1) 0.6.1.2 2) I2PTunnelIRCClient 3) Syndie 4) I2Phex 5) Stego (steganografi) ve karanlık ağlar (flamewar hakkında) 6) ???

* 1) 0.6.1.2

Geçen haftaki 0.6.1.2 sürümü şimdiye kadar oldukça iyi gitti - ağın %75’i güncellendi, HTTP POST gayet iyi çalışıyor ve streaming kitaplığı veriyi makul ölçüde verimli biçimde aktarıyor (bir HTTP isteğine verilen yanıtın tamamı çoğu zaman tek bir uçtan uca gidiş-dönüşte alınıyor). Ağ ayrıca biraz büyüdü - istikrarlı durumda rakamlar yaklaşık 400 civarında eş (peer) gibi görünüyor, ancak hafta sonu digg/gotroot [1] atfının zirvesi sırasında churn (eşlerin katılıp ayrılması) ile 6-700’e kadar sıçradı.

[1] http://gotroot.com/tiki-read_article.php?articleId=195     (evet, çok eski bir makale, biliyorum, ama birisi yeniden bulmuş)

0.6.1.2 yayınlandığından beri, daha da fazla güzel özellik eklendi - son dönemdeki irc2p netsplit'lerinin (ağ bölünmeleri) nedeni bulundu (ve düzeltildi); ayrıca SSU paket iletimine yönelik oldukça ciddi iyileştirmeler yapıldı (paketlerin %5'inden fazlasını kurtarıyor). 0.6.1.3'ün tam olarak ne zaman çıkacağını bilmiyorum, ama belki bu haftanın ilerleyen günlerinde. Göreceğiz.

* 2) I2PTunnelIRCClient

Geçen gün, biraz tartışmanın ardından, dust I2PTunnel için yeni bir uzantı geliştirdi - "ircclient" vekil sunucusu. Bu uzantı, I2P üzerinden istemci ile sunucu arasında gönderilen ve alınan içeriği filtreleyerek çalışır, güvenli olmayan IRC mesajlarını çıkarır ve düzeltilmesi gerekenleri yeniden yazar. Biraz testten sonra oldukça iyi görünüyor ve dust bunu I2PTunnel'e katkı olarak sundu ve artık web arayüzü üzerinden kullanıma sunuluyor. irc2p ekibinin IRC sunucularını güvenli olmayan mesajları reddedecek şekilde yamamış olmaları harikaydı, fakat artık bunu yapmaları için onlara güvenmek zorunda değiliz - yerel kullanıcı kendi filtrelemesi üzerinde kontrole sahip.

Kullanımı oldukça kolay - eskiden olduğu gibi IRC için bir "Client proxy" oluşturmak yerine, sadece bir "IRC proxy" oluşturun. Mevcut "Client proxy"yi bir "IRC proxy"ye dönüştürmek isterseniz, i2ptunnel.config dosyasını (cringe) düzenleyerek, "tunnel.1.type=client" değerini "tunnel.1.ircclient" olarak değiştirebilirsiniz (veya proxy'niz için uygun olan numara her neyse).

If things go well, this will be made the default I2PTunnel proxy type for IRC connections in the next release.

İyi iş çıkardın dust, teşekkürler!

* 3) Syndie

Ragnarok'un zamanlanmış yayın dağıtımı özelliği iyi gidiyor gibi görünüyor ve 0.6.1.2 çıktığından beri iki yeni özellik daha gündeme geldi - Syndie'ye gönderi yapmak için yeni, basitleştirilmiş bir CLI (komut satırı arayüzü) ekledim [2] ve dust (yaşasın dust!) bir RSS/Atom beslemesinden içerik çekmek, içindeki atıfta bulunulan ekleri veya görselleri içeri almak ve RSS içeriğini SML'ye dönüştürmek (!!!) için biraz kod hazırladı [3][4].

Bu ikisinin birlikte doğurduğu sonuçlar açık olmalı. Daha fazla haber olduğunda paylaşacağız.

[2] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000000&expand=true [3] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000001&expand=true [4] http://dust.i2p/Sucker.java     (onu yakında CVS'e entegre edeceğiz)

* 4) I2Phex

Söylentilere göre I2Phex oldukça iyi çalışıyor, ancak zaman içinde sorunlar hâlâ sürüyor. Nasıl ilerlenmesi gerektiği konusunda forumda [5] bazı tartışmalar yapıldı ve Phex'in baş geliştiricisi GregorK da, I2Phex işlevselliğinin yeniden Phex'e entegre edilmesini desteklediğini dile getirmek için tartışmaya bile katıldı (ya da en azından ana sürüm Phex'in taşıma katmanı için basit bir eklenti arayüzü sunması).

Bu gerçekten epey sağlam olurdu; çünkü bakımını yapmamız gereken kod çok daha az olurdu, üstelik kod tabanını iyileştirmeye yönelik Phex ekibinin çalışmalarından da faydalanırdık. Ancak bunun işe yaraması için bazı hackerların öne çıkıp geçişin sorumluluğunu üstlenmesi gerekiyor. I2Phex kodu, sirup'un nerelerde değişiklik yaptığını oldukça açık gösteriyor; bu yüzden çok zor olmamalı, ama muhtemelen pek de çerez değil ;)

Şu an buna hemen atlayacak pek vaktim yok, ama yardım etmek istersen foruma uğrayabilirsin.

[5] http://forum.i2p.net/viewforum.php?f=25

* 5) Stego and darknets (re: flamewar)

Posta listesi [6], son zamanlarda steganografi ve darknets (gizli ağlar) ile ilgili tartışmalarla oldukça aktif. Konu büyük ölçüde "I2P conspiracy theories flamewar" başlığı altında Freenet tech list [7]'e taşındı, ancak hâlâ devam ediyor.

Yazıların kendisinin dışında ekleyebileceğim pek bir şey olduğundan emin değilim, ama bazı kişiler tartışmanın I2P ve Freenet’i anlamalarına yardımcı olduğunu söylediler; bu yüzden bir göz atmaya değer olabilir. Ya da olmayabilir ;)

[6] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html [7] nttp://news.gmane.org/gmane.network.freenet.technical

* 6) ???

Gördüğünüz gibi, pek çok heyecan verici gelişme var ve eminim bazılarını kaçırmışımdır. Birkaç dakika içinde haftalık toplantımız için #i2p kanalına uğrayın ve bir merhaba deyin!

=jr
