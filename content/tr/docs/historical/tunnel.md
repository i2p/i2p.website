---
title: "Tunnel Tartışması"
description: "Tunnel dolgusu, parçalama ve oluşturma stratejilerinin tarihsel incelemesi"
slug: "tunnel"
aliases:
  - "/tr/docs/discussions/tunnel"
  - "/tr/docs/discussions/tunnel/"
  - "/tr/tunnel_discussion"
  - "/tr/tunnel_discussion/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Not: Bu belge, I2P'deki mevcut tunnel uygulamasına alternatifler hakkında eski bilgiler ve gelecekteki olasılıklar üzerine spekülasyonlar içermektedir. Güncel bilgiler için [tunnel sayfasına](/docs/specs/tunnel-implementation) bakınız.

Bu sayfa, 0.6.1.10 sürümü itibariyle mevcut tunnel oluşturma uygulamasını belgelemektedir. 0.6.1.10 sürümünden önce kullanılan eski tunnel oluşturma yöntemi [eski tunnel sayfasında](/docs/historical/tunnel-alt) belgelenmiştir.

### Yapılandırma Alternatifleri {#config}

Uzunluklarının ötesinde, her tunnel için kullanılabilecek ek yapılandırılabilir parametreler olabilir; örneğin teslim edilen mesajların sıklığına yönelik kısıtlama, dolgunun nasıl kullanılacağı, bir tunnel'ın ne kadar süre çalışır durumda kalacağı, sahte mesajların enjekte edilip edilmeyeceği ve hangi toplu işleme stratejilerinin kullanılacağı gibi. Bunların hiçbiri şu anda uygulanmamıştır.

### Dolgu Alternatifleri {#tunnel.padding}

Her birinin kendi avantajları olan çeşitli tunnel dolgu stratejileri mümkündür:

- Doldurma yok
- Rastgele boyuta doldurma
- Sabit boyuta doldurma
- En yakın KB'a doldurma
- En yakın üstel boyuta doldurma (2^n bayt)

Bu dolgu stratejileri çeşitli seviyelerde kullanılabilir ve mesaj boyutu bilgilerinin farklı saldırganlara maruz kalmasını ele alır. 0.4 ağından bazı istatistikleri topladıktan ve gözden geçirdikten, aynı zamanda anonimlik değiş tokuşlarını araştırdıktan sonra, 1024 baytlık sabit tunnel mesaj boyutu ile başlıyoruz. Ancak bunun içinde, parçalanmış mesajların kendileri tunnel tarafından hiç doldurulmaz (uçtan uca mesajlar için ise garlic encryption sarmalama sürecinin bir parçası olarak doldurulabilirler).

### Parçalama Alternatifleri {#tunnel.fragmentation}

Düşmanların yol boyunca mesaj boyutunu ayarlayarak mesajları etiketlemesini önlemek için, tüm tunnel mesajları sabit 1024 bayt boyutundadır. Daha büyük I2NP mesajlarını barındırmak ve aynı zamanda daha küçük olanları daha verimli bir şekilde desteklemek için, gateway daha büyük I2NP mesajlarını her tunnel mesajı içinde bulunan parçalara böler. Uç nokta, I2NP mesajını parçalardan kısa bir süre boyunca yeniden oluşturmaya çalışacak, ancak gerektiğinde bunları atacaktır.

Router'lar fragmentların nasıl düzenleneceği konusunda büyük serbestiye sahiptir; bunları ayrı birimler halinde verimsiz bir şekilde yerleştirebilir, 1024 baytlık tunnel mesajlarına daha fazla veri sığdırmak için kısa bir süre toplu halde işleyebilir veya gateway'in göndermek istediği diğer mesajlarla fırsatçı bir şekilde doldurabilir.

### Daha Fazla Alternatif {#tunnel.alternatives}

#### Tunnel İşlemini Yolun Ortasında Ayarlama {#tunnel.reroute}

Basit tunnel yönlendirme algoritması çoğu durum için yeterli olsa da, keşfedilebilecek üç alternatif vardır:

- Bir tünelde uç nokta dışındaki bir eş'in geçici olarak sonlandırma
  noktası olarak hareket etmesini sağlamak için gateway'de kullanılan şifrelemeyi ayarlayarak
  onlara işlenmiş I2NP mesajlarının düz metnini vermek. Her eş düz
  metne sahip olup olmadığını kontrol edebilir ve aldığında mesajı sahip
  oldukları gibi işleyebilir.
- Bir tünele katılan router'ların mesajı iletmeden önce yeniden
  karıştırmasına izin vermek - onu o eş'in kendi giden tünellerinden biri
  üzerinden geçirerek, bir sonraki hop'a teslim talimatları ile birlikte.
- Tünel yaratıcısının bir eş'in tüneldeki "sonraki hop"unu yeniden
  tanımlaması için kod uygulamak, böylece daha fazla dinamik yönlendirmeye
  izin vermek.

#### Çift Yönlü Tunnel'ları Kullan {#tunnel.bidirectional}

Gelen ve giden iletişim için iki ayrı tunnel kullanma mevcut stratejisi mevcut olan tek teknik değildir ve anonimlik üzerinde etkileri vardır. Olumlu tarafta, ayrı tunnel'lar kullanarak bir tunnel'daki katılımcılara analiz için maruz kalan trafik verilerini azaltır - örneğin, bir web tarayıcısından gelen outbound tunnel'daki eşler yalnızca HTTP GET trafiğini görürken, inbound tunnel'daki eşler tunnel boyunca iletilen yükü görür. Çift yönlü tunnel'larla, tüm katılımcılar örneğin bir yönde 1KB gönderildiği, sonra diğer yönde 100KB gönderildiği gerçeğine erişebilir. Olumsuz tarafta, tek yönlü tunnel'lar kullanmak, profillenmesi ve hesaba katılması gereken iki set eş olduğu ve predecessor saldırılarının artan hızını ele almak için ek özen gösterilmesi gerektiği anlamına gelir. Aşağıda özetlenen tunnel havuzlama ve oluşturma süreci predecessor saldırısı endişelerini en aza indirmelidir, ancak istenirse hem inbound hem de outbound tunnel'ları aynı eşler boyunca oluşturmak çok sorun olmayacaktır.

#### Geri Kanal İletişimi {#tunnel.backchannel}

Şu anda kullanılan IV değerleri rastgele değerlerdir. Ancak, bu 16 baytlık değerin gateway'den endpoint'e, ya da outbound tunnel'larda gateway'den herhangi bir peer'a kontrol mesajları göndermek için kullanılması mümkündür. Inbound gateway belirli değerleri IV'ye bir kez kodlayabilir ve endpoint bunu kurtarabilir (endpoint'in aynı zamanda creator olduğunu bildiği için). Outbound tunnel'lar için, creator tunnel oluşturma sırasında katılımcılara belirli değerleri iletebilir (örneğin "IV olarak 0x0 görürseniz, bu X anlamına gelir", "0x1 Y anlamına gelir", vb.). Outbound tunnel'daki gateway aynı zamanda creator olduğu için, peer'lardan herhangi birinin doğru değeri alacağı şekilde bir IV oluşturabilirler. Tunnel creator hatta inbound tunnel gateway'ine, o gateway'in bireysel katılımcılarla tam olarak bir kez iletişim kurmak için kullanabileceği bir dizi IV değeri verebilir (ancak bunun gizli anlaşma tespiti konusunda sorunları olacaktır).

Bu teknik daha sonra akış ortasında mesaj iletmek için veya gelen gateway'in endpoint'e DoS saldırısı altında olduğunu ya da başka şekilde yakında başarısız olacağını bildirmesine izin vermek için kullanılabilir. Şu anda bu ters kanalı kullanma planı bulunmamaktadır.

#### Değişken Boyutlu Tunnel Mesajları {#tunnel.variablesize}

Transport katmanının kendi sabit veya değişken mesaj boyutuna sahip olması ve kendi fragmantasyonunu kullanması mümkün olsa da, tunnel katmanı bunun yerine değişken boyutlu tunnel mesajları kullanabilir. Aradaki fark tehdit modellerinin bir meselesidir - transport katmanında sabit boyut, harici saldırganlara maruz kalan bilgiyi azaltmaya yardımcı olur (genel akış analizi hala çalışsa da), ancak dahili saldırganlar (yani tunnel katılımcıları) için mesaj boyutu açığa çıkar. Sabit boyutlu tunnel mesajları, tunnel katılımcılarına maruz kalan bilgiyi azaltmaya yardımcı olur, ancak tunnel uç noktalarına ve gateway'lere maruz kalan bilgiyi gizlemez. Sabit boyutlu uçtan uca mesajlar, ağdaki tüm eşlere maruz kalan bilgiyi gizler.

Her zaman olduğu gibi, bu I2P'nin kime karşı koruma sağlamaya çalıştığı sorunudur. Değişken boyutlu tunnel mesajları tehlikelidir, çünkü katılımcıların mesaj boyutunu diğer katılımcılara yönelik bir arka kanal olarak kullanmalarına izin verir - örneğin, 1337 byte'lık bir mesaj görürseniz, işbirliği yapan başka bir eş ile aynı tunnel'dasınız demektir. Sabit boyut setine sahip olsak bile (1024, 2048, 4096, vb.), bu arka kanal yine de mevcuttur çünkü eşler her boyutun frekansını taşıyıcı olarak kullanabilir (örneğin, iki 1024 byte'lık mesajın ardından bir 8192). Daha küçük mesajlar başlık yükünü (IV, tunnel ID, hash bölümü, vb.) getirir, ancak daha büyük sabit boyutlu mesajlar ya gecikmeyi artırır (toplulaştırma nedeniyle) ya da yükü dramatik şekilde artırır (dolgu nedeniyle). Fragmantasyon, kayıp fragmanlar nedeniyle potansiyel mesaj kaybı pahasına yükü amorti etmeye yardımcı olur.

Zamanlama saldırıları, sabit boyutlu mesajların etkinliğini değerlendirirken de önemlidir, ancak etkili olabilmeleri için ağ aktivite desenlerinin önemli bir görünümünü gerektirirler. Tunnel'daki aşırı yapay gecikmeler, periyodik testler nedeniyle tunnel'ın yaratıcısı tarafından tespit edilecek ve bu da tüm tunnel'ın atılmasına ve içindeki eşlerin profillerinin ayarlanmasına neden olacaktır.

### Alternatif Oluşturma {#tunnel.building.alternatives}

Referans: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

#### Eski Tunnel Oluşturma Yöntemi {#tunnel.building.old}

0.6.1.10 sürümünden önce kullanılan eski tunnel oluşturma yöntemi [eski tunnel sayfasında](/docs/historical/tunnel-alt) belgelenmiştir. Bu, mesajların tüm katılımcılara paralel olarak gönderildiği "hep birden" veya "paralel" bir yöntemdi.

#### Tek Seferlik Teleskopik İnşa {#tunnel.building.oneshot}

NOT: Bu mevcut yöntemdir.

Keşif tunnellarının tunnel oluşturma mesajlarını gönderme ve alma için kullanımıyla ilgili ortaya çıkan bir soru, bunun tunnel'ın öncül saldırılarına karşı savunmasızlığını nasıl etkilediğidir. Bu tunnelların uç noktaları ve geçitleri ağ boyunca rastgele dağıtılacak olsa da (bu kümede tunnel yaratıcısı bile bulunabilir), başka bir alternatif ise [Tor](https://www.torproject.org/)'da yapıldığı gibi, istek ve yanıtı iletmek için tunnel yollarının kendisini kullanmaktır. Ancak bu, tunnel oluşturma sırasında sızıntılara yol açabilir ve eş düğümlerin tunnel inşa edilirken zamanlama veya paket sayısını izleyerek tunnel'da daha sonra kaç hop olduğunu keşfetmelerine olanak tanıyabilir.

#### "Etkileşimli" Teleskopik İnşa {#tunnel.building.telescoping}

Her hop'ı tunnel'ın mevcut kısmından geçen bir mesajla tek tek oluştur. Eşlerin tunnel içindeki konumlarını belirlemek için mesajları sayabilmesi nedeniyle büyük sorunları vardır.

#### Yönetim İçin Keşif Dışı Tunnel'lar {#tunnel.building.nonexploratory}

Tunnel oluşturma sürecine ikinci bir alternatif, router'a keşif yapmayan ek bir gelen ve giden havuz seti vermek ve bunları tunnel isteği ve yanıtı için kullanmaktır. Router'ın ağa iyi entegre olmuş bir görüşe sahip olduğu varsayılırsa, bu gerekli olmamalıdır, ancak router bir şekilde bölünmüş durumdaysa, tunnel yönetimi için keşif yapmayan havuzlar kullanmak, router'ın bölümünde hangi eşlerin bulunduğuna dair bilgi sızıntısını azaltacaktır.

#### Keşif İsteği Teslimi {#tunnel.building.exploratory}

I2P 0.6.1.10 sürümüne kadar kullanılan üçüncü bir alternatif, bireysel tunnel istek mesajlarını garlic encryption ile şifreler ve bunları hoplara ayrı ayrı teslim eder, exploratory tunnel'lar aracılığıyla iletir ve yanıtlarının ayrı bir exploratory tunnel'dan geri gelmesini sağlar. Bu strateji, yukarıda özetlenen stratejinin lehine terk edilmiştir.

#### Daha Fazla Tarihçe ve Tartışma {#history}

Variable Tunnel Build Message'ın tanıtılmasından önce, en az iki sorun vardı:

1. Mesajların boyutu (maksimum 8-hop nedeniyle, tipik tunnel uzunluğu 2 veya 3 hop iken...
   ve mevcut araştırmalar 3'ten fazla hop'un anonimliği artırmadığını göstermektedir);
2. Yüksek yapım başarısızlık oranı, özellikle uzun (ve keşif amaçlı) tunnel'lar için, çünkü tüm hop'ların kabul etmesi gerekir yoksa tunnel atılır.

VTBM #1'i düzeltti ve #2'yi geliştirdi.

Welterde, yeniden yapılandırmaya izin vermek için paralel yönteme değişiklikler önerdi. Sponge, bir tür 'token' kullanmayı önerdi.

Tunnel oluşturma konusunu öğrenen herkesin, mevcut yönteme giden tarihsel süreci, özellikle çeşitli yöntemlerde var olabilecek anonimlik açıklarını incelemesi gerekir. Ekim 2005 tarihli mail arşivleri özellikle faydalıdır. [Tunnel oluşturma spesifikasyonu](/docs/specs/tunnel-creation) belirtildiği gibi, mevcut strateji Michael Rogers, Matthew Toseland (toad) ve jrandom arasında I2P mail listesinde predecessor saldırısı hakkında yapılan tartışma sırasında ortaya çıkmıştır.

#### Eş Sıralama Alternatifleri {#ordering}

Daha az katı bir sıralama da mümkündür, bu A'dan sonraki hop'un B olabileceğini garanti ederken, B'nin asla A'dan önce olamayacağını sağlar. Diğer yapılandırma seçenekleri arasında sadece gelen tunnel gateway'lerinin ve giden tunnel uç noktalarının sabitlenmesi veya MTBF oranında döndürülmesi yeteneği bulunur.

## Karıştırma/Toplu İşleme {#tunnel.mixing}

Gateway'de ve her hop'ta mesajları geciktirmek, yeniden sıralamak, yeniden yönlendirmek veya padding yapmak için hangi stratejiler kullanılmalı? Bu işlemler ne ölçüde otomatik yapılmalı, ne kadarı tunnel başına veya hop başına ayar olarak yapılandırılmalı ve tunnel'ın yaratıcısı (ve dolayısıyla kullanıcı) bu işlemi nasıl kontrol etmeli? Bunların hepsi bilinmeyen olarak bırakılmış durumda ve gelecekteki bir sürümde çözülecek.
