---
title: "2005-02-22 için I2P Durum Notları"
date: 2005-02-22
author: "jr"
description: "0.5 sürümünün başarısı, yakında çıkacak 0.5.0.1 hata düzeltmesi, tunnel eş düğümlerinin sıralama stratejileri ve azneti2p güncellemelerini kapsayan haftalık I2P geliştirme durum notları"
categories: ["status"]
---

Selam millet, haftalık güncelleme zamanı

* Index

1) 0.5 2) Sonraki adımlar 3) azneti2p 4) ???

* 1) 0.5

Hepinizin duyduğu gibi, sonunda 0.5'i yayımladık ve genel olarak gayet iyi gidiyor. Güncellemelerin ne kadar hızlı gerçekleştiğini gerçekten takdir ediyorum - ilk gün içinde ağın %50-75'i 0.5'e geçmişti! Bu hızlı benimseme sayesinde, çeşitli değişikliklerin etkisini daha çabuk görebildik ve bunun sonucunda da bir sürü hata bulduk. Hâlâ bazı bekleyen sorunlar olsa da, en önemlilerini ele almak için bu akşamın ilerleyen saatlerinde yeni bir 0.5.0.1 sürümü yayımlayacağız.

Hataların bir yan faydası olarak, router'ların binlerce tunnel kaldırabildiğini görmek hoştu ;)

* 2) Next steps

0.5.0.1 sürümünden sonra, keşif amaçlı tunnel oluşturmadaki bazı değişiklikleri denemek için başka bir derleme olabilir (tüm eşlerin başarısız olmayan olarak seçilmesi yerine, yalnızca bir veya iki başarısız olmayan eş kullanıp geri kalanını yüksek kapasiteli seçmek gibi). Bunun ardından 0.5.1'e doğru ilerleyeceğiz; bu sürüm, tunnel aktarım verimini artıracak (birden fazla küçük mesajı tek bir tunnel mesajında gruplayarak) ve kullanıcının predecessor attack (öncül saldırı) karşısındaki maruziyeti üzerinde daha fazla denetim sahibi olmasına olanak tanıyacak.

Bu kontroller, istemci başına eş sıralama ve seçim stratejileri biçimini alacak; biri gelen ağ geçidi ve giden uç nokta için ve biri de tunnel’in geri kalanı için.  Öngördüğüm stratejilerin kabaca taslağı:  
  = rastgele (şu an elimizde olan)  
  = dengeli (her bir eşi kullanma sıklığını açıkça azaltmaya çalışmak)  
  = katı (A-->B-->C’yi bir kez kullanırsak, aynı sırada kalırlar
            sonraki tunnel’lar sırasında [zamanla sınırlı])  
  = gevşek (istemci için rastgele bir anahtar üret, o anahtarla her eş arasındaki XOR
           değerini hesapla ve eşleri her zaman
           o anahtara olan uzaklığa göre sırala [zamanla sınırlı])  
  = sabit (MBTF başına her zaman aynı eşleri kullanmak)

Neyse, plan bu, yine de hangi stratejilerin önce devreye alınacağından emin değilim. Önerilere fazlasıyla açığım :)

* 3) azneti2p

azureus'taki ekip bir dizi güncellemeyle yoğun şekilde çalışıyor ve en son b34 anlık görüntüsü [1] I2P ile ilgili bazı hata düzeltmeleri içeriyor gibi görünüyor.  Son olarak gündeme getirdiğim anonimliğe ilişkin sorundan beri kaynak kodu denetlemeye zaman bulamamış olsam da, o belirli hatayı düzeltmişler; bu yüzden kendinizi maceraperest hissediyorsanız, güncellemelerini edinin ve bir deneyin!

[1] http://azureus.sourceforge.net/index_CVS.php

* 4) ???

Bir sürü şey oluyor, eminim ki hepsine değinemedim.  Birkaç dakika içinde toplantıya uğra ve neler olup bittiğine bir bak!

=jr
