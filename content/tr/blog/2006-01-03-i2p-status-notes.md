---
title: "I2P için 2006-01-03 tarihli Durum Notları"
date: 2006-01-03
author: "jr"
description: "0.6.1.8 sürüm kararlılığı, yük testi sonuçları ve aktarım hızı optimizasyonu için eş profillemesi ile kapsamlı 2005 değerlendirmesi ve 2006 yol haritası önizlemesini kapsayan yeni yıl güncellemesi"
categories: ["status"]
---

Herkese selam, mutlu yıllar! Onlarsız geçen bir haftanın ardından haftalık durum notlarımıza geri dönelim -

* Index

1) Ağ durumu ve 0.6.1.8 2) Yük testi sonuçları ve eş profilleme 3) 2005 değerlendirmesi / 2006 önizlemesi / ???

* 1) Net status and 0.6.1.8

Geçen hafta 0.6.1.8'i yayımladık ve sahadan gelen raporlar, zzz'nin yaptığı değişikliklerin epey yardımcı olduğunu ve son zamanlarda ağ trafiği önemli ölçüde artmış olmasına rağmen ağda işlerin oldukça kararlı göründüğünü gösteriyor (stats.i2p'ye göre ortalama son bir ayda ikiye katlanmış görünüyor). I2PSnark da oldukça iyi çalışıyor gibi görünüyor - birkaç pürüzle karşılaşmış olsak da, bunların çoğunu sonraki sürümlerde tespit edip düzelttik. Syndie'nin yeni blog arayüzü hakkında fazla geri bildirim gelmedi, ancak Syndie trafiğinde az da olsa bir artış oldu (kısmen protocol'un dust'un rss/atom içe aktarıcısını keşfetmesi sayesinde :)

* 2) Load testing results and peer profiling

Son birkaç haftadır throughput darboğazımızı belirlemeye çalışıyorum. Farklı yazılım bileşenlerinin her biri, I2P üzerinden uçtan uca iletişimde tipik olarak gördüğümüzden çok daha yüksek hızlarda veri iletebilecek kapasitede, bu yüzden canlı ağda onları stres testine tabi tutmak için özel yazılmış kodla kıyaslamalar yapıyorum. İlk test seti, ağdaki tüm router'lar üzerinden tek atlamalı gelen tunnel'ler kurup veriyi bu tunnel üzerinden olabildiğince çabuk iletmeye dayanıyordu ve oldukça umut verici sonuçlar gösterdi; router'lar, beklenebilecek kapasitelerine yakın hızları karşılayabildi (ör. çoğu yalnızca ömür boyu ortalama 4-16KBps işleyebilirken, bazıları tek bir tunnel üzerinden 20-120KBps'ye kadar çıkarabiliyordu). Bu test, daha fazla araştırma için iyi bir temel oluşturdu ve tunnel işlemesinin tek başına, genellikle gördüğümüzden çok daha fazlasını aktarabildiğini gösterdi.

Bu sonuçları canlı tunnels (tüneller) üzerinden yeniden üretme girişimleri o kadar başarılı olmadı. Ya da, belki de daha başarılı olduklarını söyleyebilirsiniz; çünkü şu anda gördüğümüze benzer bir aktarım hızı gösterdiler, bu da doğru yolda olduğumuz anlamına geliyordu. 1hop test sonuçlarına geri dönersek, kodu elle hızlı olarak belirlediğim eşleri seçecek şekilde değiştirdim ve bu "hileli" eş seçimiyle canlı tunnels üzerinden yük testlerini yeniden çalıştırdım; 120KBps seviyesine çıkmasa da makul bir iyileşme gösterdi.

Ne yazık ki, insanlardan eşlerini elle seçmelerini istemek hem anonimlik hem de doğrusu kullanılabilirlik açısından ciddi sorunlar doğuruyor, ancak yük testi verileriyle donanmış olarak bir çıkış yolu var gibi görünüyor. Son birkaç gündür, eşleri hızlarına göre profillemek için yeni bir yöntem deniyorum - esasen, son gecikmelerini değil de tepe sürdürülebilir aktarım hızlarını izlemek. Naif uygulamalar epey başarılı oldu ve elle seçeceğim eşleri birebir seçmemiş olsa da oldukça iyi iş çıkardı. Yine de üzerinde çözmemiz gereken bazı pürüzler var; örneğin exploratory tunnels'ı hızlı katmana terfi ettirebildiğimizden emin olmak gibi, ancak şu anda bu konuda bazı deneyler yapıyorum.

Genel olarak, en dar darboğazı zorluyor ve onu genişletirken bu aktarım hızı dalgalanmasının sonuna yaklaştığımızı düşünüyorum. Eminim yakında bir sonrakine de takılacağız ve bu bize kesinlikle normal internet hızları sağlamayacak, ama yine de yardımcı olacaktır.

* 3) 2005 review / 2006 preview / ???

2005'in pek çok alanda çığır açtığını söylemek biraz hafif kalır - geçen yıl yayımlanan 25 sürümde I2P'yi sayısız şekilde geliştirdik, ağı 5 kat büyüttük, birkaç yeni istemci uygulamasını devreye aldık (Syndie, I2Phex, I2PSnark, I2PRufus), postman ve cervantes'in yeni irc2p IRC ağına geçtik ve bazı faydalı eepsites(I2P Sites) filizlendi (örneğin zzz'nin stats.i2p sitesi, orion'un orion.i2p sitesi ve tino'nun proxy ve izleme hizmetleri, sadece birkaçını anmak gerekirse). Topluluk da biraz daha olgunlaştı; bunda forumda ve kanallarda Complication'ın ve diğerlerinin destek çabalarının payı büyük, ve tüm kesimlerden gelen hata raporlarının kalitesi ve çeşitliliği önemli ölçüde arttı. Topluluk içindekilerin süregelen mali desteği etkileyici oldu ve her ne kadar bütünüyle sürdürülebilir geliştirme için gerekli düzeyde olmasa da, kış boyunca beni geçindirebilecek bir mali tamponumuz var.

Geçtiğimiz yıl boyunca teknik, sosyal veya finansal olarak katkıda bulunan herkese, desteğiniz için teşekkürler!

2006 bizim için büyük bir yıl olacak; bu kış 0.6.2 geliyor, 1.0 sürümümüzü ilkbahar ya da yaza planlıyoruz, 2.0 ise sonbaharda, hatta daha da erken olabilir. Bu, neler yapabileceğimizi göreceğimiz yıl olacak ve uygulama katmanındaki çalışmalar her zamankinden daha kritik olacak. Öyleyse aklında bazı fikirler varsa, şimdi kolları sıvama zamanı :)

Her neyse, haftalık durum toplantımız birkaç dakika içinde başlayacak, bu yüzden daha fazla konuşmak istediğiniz bir şey varsa, her zamanki yerlerde [1] #i2p'ye uğrayın ve merhaba deyin!

=jr [1] http://forum.i2p.net/viewtopic.php?t=952
