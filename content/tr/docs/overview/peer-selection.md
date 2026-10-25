---
title: "Eş Profilleme ve Seçimi"
description: "I2P router'larının tunnel oluşturmak için eş profilleme ve seçme yöntemi"
slug: "peer-selection"
aliases:
  - "/tr/how_peerselection"
  - "/tr/how_peerselection/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## Not

Bu sayfa, 2010 itibariyle Java I2P peer profilleme ve seçim uygulamasını açıklamaktadır. Hala genel olarak doğru olsa da, bazı ayrıntılar artık doğru olmayabilir. Yeni tehditler, saldırılar ve ağ koşullarını ele almak için yasaklama, engelleme ve seçim stratejilerini geliştirmeye devam ediyoruz. Mevcut ağda çeşitli sürümlere sahip birden fazla router uygulaması bulunmaktadır. Diğer I2P uygulamaları tamamen farklı profilleme ve seçim stratejilerine sahip olabilir veya hiç profilleme kullanmayabilir.

## Genel Bakış {#overview}

### Eş Profilleme {#profiling}

**Eş profilleme**, diğer router'ların veya eşlerin **gözlemlenen** performansına dayalı veri toplama ve bu eşleri gruplara ayırma işlemidir. Profilleme, eşin kendisi tarafından [ağ veritabanında](/docs/overview/network-database) yayınlanan herhangi bir iddia edilen performans verisini **kullanmaz**.

Profiller iki amaç için kullanılır:

1. Trafiğimizi aktarmak için eş seçimi, aşağıda tartışılan konu
2. Ağ veritabanı depolama ve sorguları için floodfill router'larından eş seçimi,
   bu konu [network database](/docs/overview/network-database) sayfasında tartışılmaktadır

### Eş Seçimi {#selection}

**Peer seçimi**, ağdaki hangi router'ların mesajlarımızı iletmesini istediğimizi seçme sürecidir (hangi peer'ları tunnel'larımıza katılmaya davet edeceğiz). Bunu başarmak için her peer'ın nasıl performans gösterdiğini takip ederiz (peer'ın "profili") ve bu verileri ne kadar hızlı olduklarını, isteklerimizi ne sıklıkta kabul edebileceklerini ve aşırı yüklenmiş görünüp görünmediklerini veya kabul ettiklerini güvenilir şekilde gerçekleştirip gerçekleştiremediklerini tahmin etmek için kullanırız.

Diğer bazı anonim ağların aksine, I2P'de iddia edilen bant genişliği güvenilmez kabul edilir ve **yalnızca** tunnel yönlendirmesi için yetersiz olan çok düşük bant genişliği reklamı yapan eş düğümlerden kaçınmak için kullanılır. Tüm eş seçimi profil oluşturma yoluyla yapılır. Bu, çok sayıda tunnel yakalamak amacıyla yüksek bant genişliği iddia eden eş düğümlere dayalı basit saldırıları önler. Ayrıca [zamanlama saldırılarını](/docs/overview/threat-model#timing) da daha zor hale getirir.

Peer seçimi oldukça sık yapılır, çünkü bir router çok sayıda istemci ve keşif tunnel'ı tutabilir ve bir tunnel'ın yaşam süresi sadece 10 dakikadır.

### Daha Fazla Bilgi {#further-info}

Daha fazla bilgi için [PET-CON 2009.1](http://web.archive.org/web/20100413184504/http://www.pet-con.org/index.php/PET_Convention_2009.1)'de sunulan [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf) makalesine bakın. Makalenin yayınlanmasından sonra yapılan küçük değişikliklerle ilgili notlar için [aşağıya](#notes) bakın.

## Profiller {#profiles}

Her peer hakkında toplanan bir dizi veri noktası bulunur; bunlar arasında bir network database sorgusuna yanıt verme süreleri hakkındaki istatistikler, tunnel'larının ne sıklıkla başarısız olduğu, bize kaç yeni peer tanıtabildikleri gibi bilgiler ile onlardan en son ne zaman haber aldığımız veya son iletişim hatasının ne zaman oluştuğu gibi basit veri noktaları yer alır.

Profiller oldukça küçüktür, birkaç KB'tır. Bellek kullanımını kontrol etmek için, profil sayısı arttıkça profil sona erme süresi azalır. Profiller router kapatılana kadar bellekte tutulur ve kapatma sırasında diske yazılır. Başlangıçta profiller okunur, böylece router tüm profilleri yeniden başlatmak zorunda kalmaz ve bu sayede router başlangıç sonrasında ağa hızlıca yeniden entegre olabilir.

## Peer Özetleri {#summaries}

Profillerin kendileri bir peer'ın performansının özeti olarak değerlendirilebilirken, etkili peer seçimine olanak sağlamak için her özeti dört basit değere ayırıyoruz: peer'ın hızını, kapasitesini, ağa ne kadar iyi entegre olduğunu ve başarısız olup olmadığını temsil eden değerler.

### Hız {#speed}

Hız hesaplaması basitçe profili gözden geçirir ve bir dakika içinde peer üzerinden tek bir tunnel'da ne kadar veri gönderebileceğimizi veya alabileceğimizi tahmin eder. Bu tahmin için sadece önceki dakikadaki performansa bakar.

### Kapasite {#capacity}

Kapasite hesaplaması basitçe profili inceleyerek eş düğümün belirli bir zaman dilimi boyunca kaç tunnel'a katılmayı kabul edeceğini tahmin eder. Bu tahmin için eş düğümün kaç tunnel oluşturma isteğini kabul ettiğine, reddettiğine ve bıraktığına, ayrıca kabul edilen tunnel'lardan kaçının sonradan başarısız olduğuna bakar. Hesaplama zaman ağırlıklı olduğu için yakın zamandaki aktivite daha eski aktiviteden daha fazla sayılsa da, 48 saate kadar eski istatistikler de dahil edilebilir.

Güvenilmez ve ulaşılamaz eşleri tanımak ve bunlardan kaçınmak kritik derecede önemlidir. Ne yazık ki, tunnel oluşturma ve test etme birkaç eşin katılımını gerektirdiğinden, bırakılan bir oluşturma isteğinin veya test başarısızlığının nedenini kesin olarak belirlemek zordur. Router her bir eşe bir başarısızlık olasılığı atar ve bu olasılığı kapasite hesaplamasında kullanır. Bırakılmalar ve test başarısızlıkları, reddedilmelerden çok daha yüksek ağırlıkta değerlendirilir.

## Eş Organizasyonu {#organization}

Yukarıda belirtildiği gibi, her peer'ın profilini detaylı olarak inceleyerek birkaç temel hesaplama yapıyoruz ve bunlara dayanarak her peer'ı üç gruba ayırıyoruz - hızlı, yüksek kapasiteli ve standart.

Gruplandırmalar birbirini dışlamaz ve birbirleriyle ilgisiz de değildir:

- Bir eş (peer), kapasite hesaplaması tüm eşlerin medyanını karşılıyor veya aşıyorsa "yüksek kapasiteli" olarak kabul edilir.
- Bir eş, zaten "yüksek kapasiteli" ise ve hız hesaplaması tüm eşlerin medyanını karşılıyor veya aşıyorsa "hızlı" olarak kabul edilir.
- Bir eş, "yüksek kapasiteli" değilse "standart" olarak kabul edilir

### Grup Boyut Sınırları {#group-limits}

Grupların boyutu sınırlı olabilir.

- Hızlı grup 30 peer ile sınırlıdır.
  Daha fazla olması durumunda, yalnızca en yüksek hız derecesine sahip olanlar gruba yerleştirilir.
- Yüksek kapasite grubu 75 peer ile sınırlıdır (hızlı grup dahil).
  Daha fazla olması durumunda, yalnızca en yüksek kapasite derecesine sahip olanlar gruba yerleştirilir.
- Standart grubun sabit bir sınırı yoktur, ancak yerel ağ veritabanında saklanan RouterInfo sayısından biraz daha küçüktür.
  Günümüzün ağında aktif bir router'da yaklaşık 1000 RouterInfo ve 500 peer profili olabilir
  (hızlı ve yüksek kapasite gruplarındakiler dahil).

## Yeniden Hesaplama ve Kararlılık {#recalculation}

Özetler yeniden hesaplanır ve eşler gruplara yeniden sıralanır, her 45 saniyede bir.

Gruplar oldukça kararlı olma eğilimindedir, yani her yeniden hesaplamada sıralamalarda fazla "karışıklık" yoktur. Hızlı ve yüksek kapasiteli gruplardaki eşler, kendilerinden daha fazla tunnel inşa edilmesini sağlar, bu da hız ve kapasite derecelendirmelerini artırır ve grubta bulunmalarını pekiştirir.

## Eş Seçimi {#peer-selection}

Router, tunnel'lar oluşturmak için yukarıdaki gruplardan eş düğümler seçer.

### İstemci Tunnelları için Eş Seçimi {#client-tunnels}

İstemci tunnel'ları HTTP proxy'leri ve web sunucuları gibi uygulama trafiği için kullanılır.

[Bazı saldırılara](http://blog.torproject.org/blog/one-cell-enough) karşı hassasiyeti azaltmak ve performansı artırmak için, istemci tunnel'ları oluşturmak üzere eşler en küçük gruptan, yani "hızlı" gruptan rastgele seçilir. Aynı istemci için daha önce bir tunnel'da katılımcı olan eşlerin seçilmesine yönelik herhangi bir yanlılık yoktur.

### Keşif Tunnel'ları için Eş Seçimi {#exploratory-tunnels}

Exploratory tunneller, network veritabanı trafiği ve istemci tunnellerini test etme gibi router yönetim amaçları için kullanılır. Exploratory tunneller ayrıca daha önce bağlantı kurulmamış routerlara ulaşmak için de kullanılır, bu nedenle "exploratory" (keşif amaçlı) olarak adlandırılırlar. Bu tunneller genellikle düşük bant genişliğine sahiptir.

Keşif tunnel'larını oluşturmak için peer'lar genellikle standart gruptan rastgele seçilir. Bu oluşturma girişimlerinin başarı oranı, client tunnel oluşturma başarı oranına kıyasla düşükse, router bunun yerine yüksek kapasiteli gruptan peer'ları rastgele ağırlıklı ortalama ile seçecektir. Bu, ağ performansı zayıf olduğunda bile tatmin edici bir oluşturma başarı oranını korumaya yardımcı olur. Daha önce bir keşif tunnel'ında katılımcı olan peer'ları seçmeye yönelik herhangi bir önyargı yoktur.

Standart grup, router'ın bildiği tüm eşlerin çok büyük bir alt kümesini içerdiğinden, keşif tünelleri esasen tüm eşlerden rastgele seçim yapılarak inşa edilir, ta ki inşa başarı oranı çok düşük hale gelene kadar.

### Kısıtlamalar {#restrictions}

Bazı basit saldırıları önlemek ve performans için aşağıdaki kısıtlamalar bulunmaktadır:

- Aynı /16 IP alanından iki peer aynı tunnel'da bulunamaz.
- Bir peer, router tarafından oluşturulan tüm tunnel'ların maksimum %33'ünde yer alabilir.
- Son derece düşük bant genişliğine sahip peer'ler kullanılmaz.
- Yakın zamanda bağlantı girişimi başarısız olan peer'ler kullanılmaz.

### Tunnel'larda Peer Sıralaması {#ordering}

Eşler, [öncül saldırısı](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([2008 güncellemesi](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)) ile başa çıkmak için tunnel'lar içinde sıralanır. Daha fazla bilgi [tunnel sayfasında](/docs/specs/tunnel-implementation#ordering) mevcuttur.

## Gelecek Çalışmalar {#future}

- Gerektiğinde hız ve kapasite hesaplamalarını analiz etmeye ve ayarlamaya devam et
- Ağ büyüdükçe bellek kullanımını kontrol etmek için gerekirse daha agresif bir çıkarma stratejisi uygula
- Grup boyutu sınırlarını değerlendir
- Yapılandırılmışsa, belirli eşleri dahil etmek veya hariç tutmak için GeoIP verilerini kullan

## Notlar {#notes}

[Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf) makalesini okuyanlar için, makalenin yayınlanmasından bu yana I2P'de yapılan aşağıdaki küçük değişiklikleri göz önünde bulundurun:

- Entegrasyon hesaplaması hala kullanılmıyor
- Makalede "gruplar" "katmanlar" olarak adlandırılıyor
- "Başarısız" katmanı artık kullanılmıyor
- "Başarısız Olmayan" katmanı artık "Standart" olarak adlandırılıyor

## Kaynaklar {#references}

- [I2P Anonim Ağında Peer Profiling ve Seçimi](/pdf/I2P-PET-CON-2009.1.pdf)
- [Bir Hücre Yeterli](http://blog.torproject.org/blog/one-cell-enough)
- [Tor Giriş Korumaları](https://wiki.torproject.org/noreply/TheOnionRouter/TorFAQ#EntryGuards)
- [Murdoch 2007 Makalesi](http://freehaven.net/anonbib/#murdoch-pet2007)
- [Tor için Ayarlama](http://www.crhc.uiuc.edu/~nikita/papers/tuneup-cr.pdf)
- [Tor'a Karşı Düşük Kaynaklı Yönlendirme Saldırıları](http://cs.gmu.edu/~mccoy/papers/wpes25-bauer.pdf)
