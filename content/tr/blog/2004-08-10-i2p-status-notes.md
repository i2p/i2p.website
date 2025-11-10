---
title: "2004-08-10 tarihli I2P Durum Notları"
date: 2004-08-10
author: "jr"
description: "0.3.4.1 sürümünün performansını, outproxy yük dengelemesini ve dokümantasyon güncellemelerini kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Herkese selam, haftalık güncelleme zamanı

## Dizin:

1. 0.3.4.1 status
2. Updated docs
3. 0.4 progress
4. ???

## 1) 0.3.4.1 durumu

Pekala, geçen gün 0.3.4.1 sürümünü yayınladık ve gayet iyi gidiyor. irc üzerindeki bağlantı süreleri sürekli olarak birkaç saat boyunca devam ediyor ve aktarım hızları da oldukça iyi (geçen gün 3 paralel akış kullanarak bir eepsite(I2P Site) üzerinden 25KBps indirdim).

0.3.4.1 sürümüyle eklenen (sürüm duyurusuna eklemeyi unuttuğum) gerçekten harika bir özellik, eepproxy'nin I2P dışı istekleri bir dizi outproxy (I2P dış ağ vekil sunucusu) üzerinden round-robin yöntemiyle sırayla yönlendirmesine olanak tanıyan, mule tarafından yapılan yamaydı. Varsayılan hâlâ yalnızca squid.i2p adlı outproxy kullanmaktır, ancak router.config dosyanıza girip clientApp satırını şu şekilde değiştirirseniz:

```
-e 'httpclient 4444 squid.i2p,www1.squid.i2p'
```
Bu, her HTTP isteğini listelenen iki outproxy'den (squid.i2p ve www1.squid.i2p) birinin üzerinden rastgele yönlendirecek. Bu sayede, birkaç kişi daha outproxy (I2P içinden clearnet'e erişim sağlayan çıkış proxy'si) çalıştırırsa, squid.i2p'ye bu kadar bağımlı olmazsınız. Elbette, outproxy'lerle ilgili kaygılarımı hepiniz duydunuz, ancak bu özelliğe sahip olmak insanlara daha fazla seçenek sunuyor.

Son birkaç saattir bir miktar istikrarsızlık yaşıyoruz, ancak duck ve cervantes'in yardımıyla iki ciddi hatayı belirledim ve şu anda düzeltmeleri test ediyorum. Düzeltmeler oldukça kapsamlı, bu yüzden sonuçları doğruladıktan sonra önümüzdeki bir iki gün içinde 0.3.4.2 sürümünü yayımlamayı bekliyorum.

## 2) Güncellenmiş belgeler

Sitedeki dokümantasyonu güncel hale getirme işini biraz aksattık ve hâlâ birkaç büyük boşluk olsa da (örneğin netDb ve i2ptunnel belgeleri), yakın zamanda bunlardan birkaçını güncelledik (ağ karşılaştırmaları ve SSS). 0.4 ve 1.0 sürümlerine yaklaştıkça, insanların siteyi gözden geçirip nelerin iyileştirilebileceğine bakmalarını takdir ederim.

Özellikle dikkat çeken şey güncellenmiş Onur Listesi - hepinizin yaptığı cömert bağışları yansıtacak şekilde onu nihayet senkronize ettik (teşekkürler!). İlerlerken, bu kaynakları geliştiricilere ve diğer katkıda bulunanlara karşılık ödemek ve ayrıca oluşan maliyetleri (örn. barındırma sağlayıcıları vb) karşılamak için kullanacağız.

## 3) 0.4 ilerleme

Geçen haftanın notlarına dönüp baktığımızda, 0.4 için hâlâ yapılacak birkaç şeyimiz var, ama simülasyonlar oldukça iyi gidiyor ve kaffe ile ilgili sorunların çoğu bulundu. Yine de harika olurdu, insanlar router veya istemci uygulamaların farklı yönlerini olabildiğince zorlayıp karşılaştıkları hatalar için kayıt açabilseler.

## 4) ???

Şimdilik gündeme getirebileceğim bu kadar - bizi ileri taşımaya yardımcı olmak için ayırdığınız zamana minnettarım ve bence harika ilerleme kaydediyoruz. Elbette, konuşmak istediği başka bir şey olan varsa, #i2p'deki toplantıya... şey... şimdi uğrayın :)

=jr
