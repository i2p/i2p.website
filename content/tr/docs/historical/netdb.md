---
title: "Ağ Veritabanı Tartışması"
description: "floodfill, Kademlia deneyleri ve netDb için gelecekte yapılacak ayarlamalar hakkında tarihsel notlar"
slug: "netdb"
reviewStatus: "needs-review"
---

> **Not:** Bu arşiv niteliğindeki tartışma, ağ veritabanına (netDb) yönelik tarihsel yaklaşımların ana hatlarını çizer. Güncel davranış ve yönlendirme için [ana netDb belgelerine](/docs/specs/common-structures/) başvurun.

## Tarihçe

I2P'nin netDb'si basit bir floodfill algoritması kullanılarak dağıtılır. Erken sürümler ayrıca yedek olarak bir Kademlia DHT (dağıtık hash tablosu) uygulamasını da barındırıyordu, ancak bunun güvenilmez olduğu kanıtlandı ve 0.6.1.20 sürümünde tamamen devre dışı bırakıldı. Floodfill tasarımı, yayınlanan bir kaydı katılımcı bir router'a iletir, onay bekler ve gerekirse diğer floodfill eşleriyle yeniden dener. Floodfill eşleri, floodfill olmayan router'lardan gelen depolama (store) iletilerini diğer tüm floodfill katılımcılarına yayınlar.

2009'un sonlarında, bireysel floodfill router'lar üzerindeki depolama yükünü azaltmak için Kademlia (bir DHT protokolü) sorguları kısmen yeniden devreye sokuldu.

### Floodfill'e Giriş (I2P'de netDb verilerini depolayıp dağıtan özel router rolü)

Floodfill ilk olarak 0.6.0.4 sürümünde ortaya çıktı; bu sırada Kademlia (bir DHT protokolü) yedek olarak kullanılabilir olmaya devam etti. O dönemde, yüksek paket kaybı ve kısıtlı rotalar, en yakın dört eşten onay almayı zorlaştırıyor, çoğu zaman onlarca tekrarlı depolama girişimini gerektiriyordu. Dışarıdan erişilebilen routers'tan oluşan bir floodfill altkümesine geçiş, pragmatik bir kısa vadeli çözüm sağladı.

### Kademlia’yı (bir dağıtık hash tablosu [DHT] protokolü) yeniden ele almak

Göz önünde bulundurulan bazı alternatifler şunlardı:

- Katılıma isteğe bağlı olarak dahil olmayı seçen erişilebilir router'larla sınırlı bir Kademlia DHT (Kademlia tabanlı dağıtık karma tablosu) olarak netDb'yi çalıştırmak
- floodfill modelini (netDb verisini barındırıp dağıtan yüksek kapasiteli düğüm modeli) korumak ancak katılımı yeterli kapasiteye sahip router'larla sınırlamak ve dağıtımı rastgele denetimlerle doğrulamak

floodfill yaklaşımı, dağıtması daha kolay olduğu ve netDb'nin kullanıcı yüklerini değil, yalnızca meta veriyi taşıdığı için tercih edildi. Çoğu hedef bir LeaseSet yayımlamaz; çünkü gönderici genellikle kendi LeaseSet'ini garlic mesajları içinde paketler.

## Güncel Durum (Tarihsel Bakış Açısı)

netDb algoritmaları ağın ihtiyaçlarına göre uyarlanmıştır ve geçmişte rahatlıkla birkaç yüz router'ı kaldırabilmiştir. Erken tahminler, 3–5 floodfill router'ın yaklaşık 10.000 düğümü destekleyebileceğini öne sürüyordu.

### Güncellenmiş Hesaplamalar (Mart 2008)

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
Burada:

- `N`: Ağdaki router sayısı
- `L`: Her router başına ortalama istemci hedef sayısı (`RouterInfo` için +1)
- `F`: Tunnel başarısızlık yüzdesi
- `R`: Tunnel ömrünün bir kesri olarak Tunnel yeniden oluşturma süresi
- `S`: Ortalama netDb girdi boyutu
- `T`: Tunnel ömrü

2008 dönemine ait değerleri (`N = 700`, `L = 0.5`, `F = 0.33`, `R = 0.5`, `S = 4 KB`, `T = 10 minutes`) kullanmak şu sonucu verir:

```
recvKBps ≈ 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4 KB / 10m ≈ 28 KBps
```
### Kademlia Geri Dönecek mi?

Geliştiriciler 2007'nin başları civarında Kademlia'nın (bir dağıtık hash tablosu algoritması) yeniden devreye alınmasını tartıştılar. Uzlaşı, floodfill kapasitesinin ihtiyaç duyuldukça kademeli olarak genişletilebileceği; buna karşılık Kademlia'nın standart router kitlesi için kayda değer ölçüde karmaşıklık ve kaynak gereksinimleri eklediği yönündeydi. Yedek çözüm, floodfill kapasitesi yetersiz kalmadıkça pasif kalır.

### Floodfill Kapasite Planlaması

Bant genişliği sınıfı `O` router'ların floodfill'e otomatik kabulü, cazip olsa da, düşman düğümlerin katılmayı seçmesi halinde denial-of-service (hizmet reddi) senaryoları riski taşır. Tarihsel analiz, floodfill havuzunun sınırlandırılmasının (örneğin, ~10K router'ı 3–5 eşin işlemesi) daha güvenli olduğunu öne sürmüştü. Yeterli ama kontrollü bir floodfill kümesini sürdürmek için güvenilir operatörler veya otomatik heuristics (sezgisel yöntemler) kullanılagelmiştir.

## Floodfill Yapılacaklar (Tarihsel)

> Bu bölüm arşiv amaçlı olarak tutulmaktadır. Ana netDb sayfası güncel yol haritasını ve tasarımla ilgili değerlendirmeleri takip eder.

13 Mart 2008'de yalnızca bir kullanılabilir floodfill router'ın bulunduğu bir süre gibi operasyonel olaylar, 0.6.1.33 ile 0.7.x arasındaki sürümlerde sunulan çeşitli iyileştirmelere yol açtı; bunlar arasında şunlar vardı:

- Aramalarda floodfill seçimini rastgeleleştirme ve yanıt veren eşlere öncelik verme
- router konsolu "Profiles" sayfasında ek floodfill metriklerinin görüntülenmesi
- floodfill bant genişliği kullanımını azaltmak için netDb giriş boyutunda kademeli azaltımlar
- profil verileri aracılığıyla toplanan performansa dayalı olarak sınıf `O` router'larının bir alt kümesi için otomatik opt-in (isteğe bağlı katılım)
- Geliştirilmiş engelleme listesi yönetimi, floodfill eş seçimi ve keşif sezgisel yöntemleri

O dönemden kalan fikirler arasında şunlar vardı:

- floodfill eşlerini daha iyi derecelendirmek ve seçmek için `dbHistory` istatistiklerini kullanma
- Başarısız olan eşlerle tekrar tekrar iletişime geçmekten kaçınmak için yeniden deneme davranışını iyileştirme
- Seçimde gecikme ölçümleri ve entegrasyon puanlarından yararlanma
- Başarısız olan floodfill router'ları daha hızlı tespit etme ve tepki verme
- Yüksek bant genişlikli ve floodfill düğümlerindeki kaynak gereksinimlerini azaltmaya devam etme

Bu notların yazıldığı sırada bile, ağ dayanıklı kabul ediliyordu ve düşmanca floodfill'lere veya floodfill hedefli hizmet reddi saldırılarına hızla karşılık vermek için gerekli altyapı mevcuttu.

## Ek Notlar

- router konsolu, floodfill güvenilirliğinin analiz edilmesine yardımcı olmak için geliştirilmiş profil verilerini uzun süredir sunmaktadır.
- Tarihsel yorumlar Kademlia (bir DHT algoritması) veya alternatif DHT şemeleri üzerine spekülasyon yapmış olsa da, floodfill üretim ağları için birincil algoritma olarak kalmıştır.
- Geleceğe dönük araştırmalar, kötüye kullanma fırsatlarını sınırlarken floodfill'e kabulü uyarlanabilir hâle getirmeye odaklandı.
