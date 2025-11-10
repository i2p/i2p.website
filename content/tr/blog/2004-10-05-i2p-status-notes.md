---
title: "2004-10-05 tarihli I2P Durum Notları"
date: 2004-10-05
author: "jr"
description: "0.4.1.1 sürümü, ağ istatistiklerinin analizi, 0.4.2 streaming library (akış kitaplığı) planları ve birlikte verilen eepserver konularını kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Herkese selam, haftalık güncelleme zamanı

## Dizin:

1. 0.4.1.1 status
2. Pretty pictures
3. 0.4.1.2 and 0.4.2
4. Bundled eepserver
5. ???

## 1) 0.4.1.1 durum

Oldukça sorunlu 0.4.1 sürümünden (ve ardından gelen hızlı 0.4.1.1 güncellemesinden) sonra, ağ yeniden normale dönmüş gibi görünüyor - şu anda 50 küsur eş etkin ve hem irc hem de eepsites(I2P Sites) erişilebilir. Sıkıntıların çoğu, yeni transport (taşıma katmanı) laboratuvar koşulları dışında yetersiz test edilmesinden kaynaklandı (örn. soketlerin tuhaf zamanlarda kopması, aşırı gecikmeler vb.). Bir sonraki sefer o katmanda değişiklik yapmamız gerektiğinde, yayınlamadan önce bunu daha geniş çapta test ettiğimizden emin olacağız.

## 2) Güzel resimler

Son birkaç gündür CVS'de çok sayıda güncelleme yapılıyor ve eklenen yeniliklerden biri, /stats.jsp üzerinde toplanan kaba ortalamalarla uğraşmak yerine, istatistikler üretilirken ham istatistik verisini basitçe çekmemize olanak tanıyan yeni bir istatistik kaydı bileşeniydi. Bununla, birkaç router üzerinde bazı kilit istatistikleri izliyorum ve kalan kararlılık sorunlarını tespit etmeye biraz daha yaklaşıyoruz. Ham istatistikler oldukça hacimli (duck'ın makinesinde 20 saatlik bir çalıştırma neredeyse 60MB veri üretti), ama bu yüzden güzel grafiklerimiz var - `http://dev.i2p.net/~jrandom/stats/`

Bunların çoğunda Y ekseni milisaniye, X ekseni ise saniyedir. Dikkat edilmesi gereken birkaç ilginç nokta var. İlk olarak, client.sendAckTime.png tek bir round trip time (gidiş-dönüş süresi) için oldukça iyi bir yaklaşık değerdir; çünkü ack mesajı (onay) payload (yük) ile birlikte gönderilir ve ardından tunnel’ın tam yolu boyunca geri döner — bu nedenle, gönderilen yaklaşık 33.000 başarılı mesajın çok büyük çoğunluğunun round trip time'ı 10 saniyenin altındaydı. Ardından client.sendsPerFailure.png'yi client.sendAttemptAverage.png ile birlikte incelediğimizde, 563 başarısız gönderimin neredeyse tamamının izin verdiğimiz azami yeniden deneme sayısına kadar gönderildiğini (5; her deneme için 10 sn soft timeout (yumuşak zaman aşımı) ve 60 sn hard timeout (katı zaman aşımı)) görürüz; buna karşılık diğer denemelerin çoğu birinci ya da ikinci denemede başarılı olmuştur.

Bir diğer ilginç görsel ise client.timeout.png; sahip olduğum şu varsayıma ciddi kuşku düşürüyor: ileti gönderim hatalarının bir tür yerel tıkanıklıkla ilişkili olduğu. Grafikteki veriler, hatalar meydana geldiğinde gelen bant genişliği kullanımının geniş ölçüde değiştiğini, yerel gönderim işleme süresinde tutarlı ani sıçramalar olmadığını ve tunnel test gecikmesiyle de görünürde hiçbir örüntü bulunmadığını gösteriyor.

dbResponseTime.png ve dbResponseTime2.png dosyaları, client.sendAckTime.png dosyasına benzerdir; ancak uçtan uca istemci mesajları yerine netDb mesajlarına karşılık gelirler.

transport.sendMessageFailedLifetime.png, bir mesajı yerelde herhangi bir nedenle (örneğin, süresi dolduğu için ya da hedeflediği eş düğüm erişilemez olduğundan) başarısız saymadan önce onu ne kadar süre beklettiğimizi gösteriyor. Bazı başarısızlıklar kaçınılmazdır, ancak bu görsel, yerel gönderim zaman aşımının (10 sn) hemen ardından başarısız olan kayda değer sayıda mesaj olduğunu gösteriyor. Bunu ele almak için yapabileceğimiz birkaç şey var: - birincisi, kara listeyi daha uyarlanabilir hale getirebiliriz- her biri için sabit 4 dakika yerine, bir eş düğümün kara listede kalma süresini üstel olarak artırmak. (bu değişiklik zaten CVS’e işlendi) - ikincisi, nasılsa başarısız olacak gibi göründüğünde mesajları peşinen başarısız sayabiliriz. Bunu yapmak için, her bağlantının kendi gönderim hızını izlemesini sağlıyoruz ve kuyruğuna yeni bir mesaj eklendiğinde, kuyrukta halihazırda biriken bayt sayısının gönderim hızına bölümü, sona ermeye kadar kalan süreyi aşıyorsa, mesajı derhal başarısız sayıyoruz. Ayrıca, bir eş düğüm üzerinden daha fazla tunnel (tünel) isteği kabul edip etmeyeceğimize karar verirken de bu ölçütü kullanabiliriz.

Neyse, sıradaki güzel resme geçelim - transport.sendProcessingTime.png. Burada, bu belirli makinenin nadiren büyük bir gecikmeden sorumlu olduğunu görüyorsunuz - genellikle 10-100ms, ancak bazen 1s veya daha fazlasına kadar çıkan ani sıçramalar oluyor.

tunnel.participatingMessagesProcessed.png dosyasında çizilen her bir nokta, router’ın katıldığı bir tunnel boyunca iletilen mesaj sayısını temsil eder. Bunu ortalama mesaj boyutuyla birleştirmek, eşin (peer) başkaları için üstlendiği tahmini ağ yükünü bize verir.

Son görsel, tunnel.testSuccessTime.png, bir mesajın bir tunnel'den dışarı gönderilip başka bir inbound tunnel üzerinden yeniden geri dönmesinin ne kadar sürdüğünü göstererek tunnel'lerimizin ne kadar iyi olduğuna dair bir tahmin verir.

Tamam, şimdilik bu kadar görsel yeter. 0.4.1.1-6'dan sonraki herhangi bir sürümle, router yapılandırma özelliği "stat.logFilters" değerini istatistik adlarının virgülle ayrılmış bir listesi olarak ayarlayarak verileri kendiniz oluşturabilirsiniz (adları /stats.jsp sayfasından alın). Bu, stats.log dosyasına yazılır ve şununla işleyebilirsiniz

```
java -cp lib/i2p.jar net.i2p.stat.StatLogFilter stat.log
```
her bir istatistik için bunu ayrı dosyalara ayırır, en sevdiğiniz araca (örn. gnuplot) yüklemeye uygundur.

## 3) 0.4.1.2 ve 0.4.2

0.4.1.1 sürümünden bu yana birçok güncelleme yapıldı (tam liste için tarihçeye bakın), ancak henüz kritik düzeltme yok. IP otomatik algılama ile ilgili bazı çözümlenmemiş hatalar giderildikten sonra, bunları bu haftanın ilerleyen günlerinde çıkacak bir sonraki 0.4.1.2 yama sürümünde yayımlayacağız.

O noktada bir sonraki büyük görev 0.4.2 sürümüne ulaşmak olacak; bu da şu anda tunnel işleme üzerinde kapsamlı bir yenileme olarak planlanıyor. Şifrelemeyi ve mesaj işlemeyi, ayrıca tunnel havuzlamasını gözden geçirmek çok iş gerektirecek; ancak bu oldukça kritik, çünkü bir saldırgan şu anda tunnel'lar üzerinde nispeten kolayca bazı istatistiksel saldırılar düzenleyebilir (örn. rastgele tunnel sıralamasıyla predecessor saldırısı veya netDb toplama).

dm ise streaming lib (akış kitaplığı)'i önce yapmanın mantıklı olup olmayacağını gündeme getirdi (şu anda 0.4.3 sürümü için planlanıyor). Bunun yararı, ağın hem daha güvenilir hale gelmesi hem de daha iyi throughput (aktarım hızı) sunması olur; bu da diğer geliştiricileri istemci uygulamalar üzerinde çalışmaya teşvik eder. Bu tamamlandıktan sonra, tunnel yenilemesine geri dönebilir ve (kullanıcıya görünür olmayan) güvenlik sorunlarını ele alabilirim.

Teknik olarak, 0.4.2 ve 0.4.3 için planlanan iki görev birbirinden bağımsız ve nasıl olsa ikisi de yapılacak; dolayısıyla bunların yerlerini değiştirmemizin pek bir dezavantajı yok gibi görünüyor. dm’ye katılma eğilimindeyim ve 0.4.2’nin tunnel güncellemesi, 0.4.3’ün ise streaming kütüphanesi olarak kalması için geçerli nedenler sunulamazsa, yerlerini değiştiririz.

## 4) Birlikte gelen eepserver

0.4.1 sürüm notlarında belirtildiği gibi, kutudan çıkar çıkmaz bir eepsite(I2P Sitesi) çalıştırmak için gerekli yazılım ve yapılandırmayı paketledik - yalnızca ./eepsite/docroot/ dizinine bir dosya bırakıp router konsolunda bulunan I2P hedefini paylaşabilirsiniz.

Yine de birkaç kişi .war dosyalarına olan hevesimi eleştirdi - ne yazık ki çoğu uygulama, bir dosyayı ./eepsite/webapps/ dizinine bırakmaktan biraz daha fazla iş gerektiriyor. blojsom blog motorunu çalıştırmaya dair kısa bir kılavuz hazırladım ve bunun nasıl göründüğünü detonate'in sitesinde görebilirsiniz.

## 5) ???

Şimdilik söyleyeceklerim bu kadar - konuları tartışmak isterseniz 90 dakika sonra toplantıya uğrayın.

=jr
