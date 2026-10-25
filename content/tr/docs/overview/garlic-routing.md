---
title: "Garlic Routing"
description: "I2P'de garlic routing terminolojisi, mimarisi ve uygulamasını anlama"
slug: "garlic-routing"
aliases:
  - "/tr/how_garlicrouting"
  - "/tr/how_garlicrouting/"
lastUpdated: "2025-10"
accurateFor: "0.9.12"
---

## Garlic Routing ve "Garlic" Terminolojisi

"Garlic routing" ve "garlic encryption" terimleri I2P teknolojisine atıfta bulunurken genellikle oldukça gevşek bir şekilde kullanılır. Burada, terimlerin tarihçesini, çeşitli anlamlarını ve I2P'de "garlic" yöntemlerinin kullanımını açıklıyoruz.

"Garlic routing" terimi ilk olarak [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) tarafından Roger Dingledine'in Free Haven [Yüksek Lisans tezi](https://www.freehaven.net/papers.html) Bölüm 8.1.1'de (Haziran 2000) [Onion Routing](https://www.onion-router.net/)'den türetilerek ortaya atılmıştır.

"Garlic" terimi muhtemelen ilk olarak I2P geliştiricileri tarafından kullanılmıştır çünkü I2P, Freedman'ın tarif ettiği şekilde bir paketleme biçimi uygular veya sadece Tor'dan genel farklılıkları vurgulamak için kullanılmıştır. Spesifik gerekçe tarihin derinliklerinde kaybolmuş olabilir. Genel olarak, I2P'ye atıfta bulunurken, "garlic" terimi üç şeyden birini ifade edebilir:

1. Katmanlı Şifreleme
2. Birden fazla mesajı bir araya paketleme
3. ElGamal/AES Şifrelemesi

Ne yazık ki, I2P'nin son yıllarda "garlic" terminolojisini kullanımı her zaman kesin olmamıştır; bu nedenle okuyucunun bu terimle karşılaştığında dikkatli olması önerilir. Umarız aşağıdaki açıklama durumu netleştirecektir.

### Katmanlı Şifreleme

Onion routing, bir dizi eş üzerinden yollar veya tunnel'lar oluşturma ve ardından bu tunnel'ı kullanma tekniğidir. Mesajlar gönderen tarafından tekrar tekrar şifrelenir ve ardından her hop tarafından şifresi çözülür. Oluşturma aşamasında, her eşe yalnızca bir sonraki hop için yönlendirme talimatları açıklanır. İşletme aşamasında ise mesajlar tunnel üzerinden geçirilir ve mesaj ile yönlendirme talimatları yalnızca tunnel'ın uç noktasına açıklanır.

Bu, Mixmaster'ın (bkz. [ağ karşılaştırmaları](/docs/overview/comparison/)) mesaj gönderme yöntemine benzer - bir mesajı alır, alıcının açık anahtarıyla şifreler, ardından bu şifrelenmiş mesajı alır ve onu (bir sonraki atlamayı belirten talimatlarla birlikte) şifreler, ardından bu ortaya çıkan şifrelenmiş mesajı alır ve bu böyle devam eder, yol boyunca her atlama için bir şifreleme katmanı olana kadar.

Bu anlamda, genel bir kavram olarak "garlic routing", "onion routing" ile aynıdır. I2P'de uygulandığı şekliyle, tabii ki Tor'daki uygulamadan birkaç fark vardır; aşağıya bakın. Buna rağmen, I2P'nin [onion routing üzerine yapılan geniş akademik araştırmalardan](https://www.onion-router.net/Publications.html), [Tor ve benzer mixnet'lerden](https://freehaven.net/anonbib/topic.html) faydalanacağı kadar önemli benzerlikler vardır.

### Birden Fazla Mesajı Paketleme

Michael Freedman, "garlic routing"'i onion routing'in bir uzantısı olarak tanımladı; bu yöntemde birden fazla mesaj birlikte paketlenir. Her mesajı bir "bulb" (ampul) olarak adlandırdı. Her birinin kendi teslimat talimatları olan tüm mesajlar, uç noktada açığa çıkar. Bu, onion routing "reply block"'unun orijinal mesajla verimli bir şekilde paketlenmesine olanak tanır.

Bu konsept I2P'de aşağıda açıklandığı gibi uygulanmaktadır. Garlic "bulbs" (soğanlar) için kullandığımız terim "cloves" (dişler)dir. Tek bir mesaj yerine herhangi bir sayıda mesaj içerilebilir. Bu, Tor'da uygulanan onion routing'den önemli bir farklılıktır. Ancak bu, I2P ve Tor arasındaki birçok büyük mimari farklılıktan yalnızca biridir; belki de terminolojide bir değişikliği tek başına haklı çıkaracak kadar yeterli değildir.

Freedman tarafından açıklanan yöntemden bir diğer fark, yolun tek yönlü olmasıdır - onion routing veya mixmaster yanıt bloklarında görülen "dönüş noktası" yoktur, bu da algoritmayı büyük ölçüde basitleştirir ve daha esnek ve güvenilir teslimat sağlar.

### ElGamal/AES Şifreleme

Bazı durumlarda, "garlic encryption" sadece [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) şifrelemesini (çoklu katmanlar olmaksızın) ifade edebilir.

---

## I2P'de "Garlic" Yöntemleri

Artık çeşitli "garlic" terimlerini tanımladığımıza göre, I2P'nin üç yerde garlic routing, paketleme ve şifreleme kullandığını söyleyebiliriz:

1. Tunnel oluşturma ve tunnel üzerinden yönlendirme için (katmanlı şifreleme)
2. Uçtan uca mesaj tesliminin başarısını veya başarısızlığını belirlemek için (paketleme)
3. Bazı ağ veritabanı girişlerini yayınlamak için (başarılı trafik analizi saldırısı olasılığını azaltma) (ElGamal/AES)

Bu tekniğin ağın performansını iyileştirmek, taşıma gecikmesi/verim dengesini kullanmak ve güvenilirliği artırmak için verileri yedekli yollar aracılığıyla dallara ayırmak için kullanılabileceği önemli yollar da vardır.

### Tunnel Oluşturma ve Yönlendirme

I2P'de, tunnel'lar tek yönlüdür. Her taraf iki tunnel inşa eder, biri giden ve biri gelen trafik için. Bu nedenle, tek bir gidiş-dönüş mesaj ve yanıt için dört tunnel gereklidir.

Tunnel'lar katmanlı şifreleme ile inşa edilir ve kullanılır. Bu, [tunnel uygulama sayfasında](/docs/specs/tunnel-implementation/) açıklanmıştır. Şifreleme için [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) kullanıyoruz.

Tunnel'lar tüm [I2NP mesajlarını](/docs/specs/i2np/) taşımak için genel amaçlı bir mekanizmadır ve Garlic Messages tunnel'ları oluşturmak için kullanılmaz. Outbound tunnel uç noktasında açılmak üzere birden fazla I2NP mesajını tek bir Garlic Message içinde paketlemeyiz; tunnel şifrelemesi yeterlidir.

### Uçtan Uca Mesaj Paketleme

Tunnel'ların üzerindeki katmanda, I2P [Destination'lar](/docs/specs/common-structures/) arasında uçtan uca mesajlar iletir. Tek bir tunnel içinde olduğu gibi, şifreleme için [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) kullanırız. [I2CP arayüzü](/docs/api/i2cp/) aracılığıyla router'a iletilen her istemci mesajı, bir Garlic Message içinde kendi Delivery Instructions'ına sahip tek bir Garlic Clove haline gelir. Delivery Instructions bir Destination, Router veya Tunnel belirtebilir.

Genel olarak, bir Garlic Message yalnızca bir clove içerir. Ancak, router periyodik olarak Garlic Message içinde iki ek clove paketler:

![Garlic Message Cloves](/images/garliccloves.svg)

1. **Bir Teslimat Durumu Mesajı**, kaynak router'a onay olarak geri gönderilmesini belirten Teslimat Talimatları ile birlikte. Bu, referanslarda açıklanan "yanıt bloğu" veya "yanıt onion"a benzerdir. Uçtan uca mesaj teslimatının başarısını veya başarısızlığını belirlemek için kullanılır. Kaynak router, Teslimat Durumu Mesajını beklenen süre içinde alamama durumunda, uzak uç Destination'a olan yönlendirmeyi değiştirebilir veya başka eylemler gerçekleştirebilir.

2. **Bir Database Store Message**, kaynak Destination için bir LeaseSet içeren ve uzak uç destination'ın router'ını belirten Delivery Instructions ile birlikte. Router periyodik olarak bir LeaseSet paketleyerek, uzak ucun iletişimi sürdürebilmesini sağlar. Aksi takdirde uzak uç, network database girişi için bir floodfill router'a sorgu yapmak zorunda kalır ve [network database sayfasında](/docs/specs/common-structures/) açıklandığı gibi tüm LeaseSet'lerin network database'e yayınlanması gerekir.

Varsayılan olarak, Delivery Status ve Database Store Mesajları yerel LeaseSet değiştiğinde, ek Session Tag'leri teslim edildiğinde veya mesajlar önceki dakika içinde paketlenmemişse paketlenir.

Açıkçası, ek mesajlar şu anda belirli amaçlar için paketlenmekte olup genel amaçlı bir yönlendirme şemasının parçası değildir.

0.9.12 sürümünden itibaren, Teslimat Durumu Mesajı, gönderen tarafından başka bir Garlic Mesajı içerisine sarılır, böylece içerikler şifrelenir ve dönüş yolundaki router'lara görünmez olur.

### Floodfill Ağ Veritabanına Depolama

[Ağ veritabanı sayfasında](/docs/specs/common-structures/) açıklandığı gibi, yerel leaseSet'ler floodfill router'lara, tunnel'ın giden gateway'ine görünmez olması için Garlic Message içinde sarılmış bir Database Store Message ile gönderilir.

---

## Gelecekteki Çalışmalar

Garlic Message mekanizması çok esnektir ve birçok mixnet teslimat yöntemi türünü uygulamak için bir yapı sağlar. Tunnel message Delivery Instructions'taki kullanılmayan gecikme seçeneği ile birlikte, geniş bir yelpazede toplu işleme, gecikme, karıştırma ve yönlendirme stratejileri mümkündür.

Özellikle, giden tunnel uç noktasında çok daha fazla esneklik potansiyeli vardır. Mesajlar oradan birkaç tunnel'dan birine yönlendirilebilir (böylece noktadan noktaya bağlantılar minimize edilir), ya da yedeklilik için birkaç tunnel'a multicast yapılabilir, veya streaming ses ve video için kullanılabilir.

Bu tür deneyler, belirli yönlendirme yollarını sınırlama, çeşitli yollar boyunca iletilen I2NP mesaj türlerini kısıtlama ve belirli mesaj süre sonu zamanlarını uygulama gibi güvenlik ve anonimliği sağlama ihtiyacıyla çelişebilir.

ElGamal/AES şifrelemesinin bir parçası olarak, garlic message gönderici tarafından belirtilen miktarda dolgu verisi içerir ve böylece gönderenin trafik analizi karşısında aktif karşı önlemler almasına olanak tanır. Bu özellik şu anda 16 baytın katlarına doldurma gereksinimine ek olarak kullanılmamaktadır.

[Floodfill router'lara](/docs/specs/common-structures/) giden ve gelen ek mesajların şifrelenmesi.

---

## Kaynaklar

- Garlic routing terimi ilk olarak Roger Dingledine'ın Free Haven [Yüksek Lisans tezi](https://www.freehaven.net/papers.html)'nde (Haziran 2000) kullanılmıştır, [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) tarafından yazılan Bölüm 8.1.1'e bakınız.
- [Onion Router Yayınları](https://www.onion-router.net/Publications.html)
- [Onion Routing (Wikipedia)](https://en.wikipedia.org/wiki/Onion_routing)
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)
- [Tor Projesi](https://www.torproject.org/)
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)
- Onion routing ilk olarak 1996'da David M. Goldschlag, Michael G. Reed ve Paul F. Syverson tarafından [Hiding Routing Information](https://www.onion-router.net/Publications/IH-1996.pdf) çalışmasında tanımlanmıştır.
