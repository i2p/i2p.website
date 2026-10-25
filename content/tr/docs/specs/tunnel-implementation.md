---
title: "Tunnel Uygulaması"
description: "I2P tunnel işleyişi, oluşturulması ve mesaj işleme spesifikasyonu"
slug: "tunnel-implementation"
aliases:
  - "/tr/docs/specs/implementation"
  - "/tr/docs/specs/implementation/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Bu sayfa mevcut tunnel uygulamasını belgelemektedir.

## Tunnel Genel Bakış {#tunnel.overview}

I2P içerisinde, mesajlar bir yönde sanal bir peer tüneli boyunca iletilir ve mesajı bir sonraki hop'a aktarmak için mevcut olan her türlü yöntem kullanılır. Mesajlar tünelin *gateway*'ine ulaşır, sabit boyutlu tünel mesajlarına paketlenir ve/veya parçalanır, ardından tüneldeki bir sonraki hop'a iletilir. Bu hop mesajı işler, geçerliliğini doğrular ve bir sonraki hop'a gönderir, bu şekilde tünel endpoint'ine ulaşana kadar devam eder. Bu *endpoint* gateway tarafından paketlenen mesajları alır ve talimat verildiği gibi iletir - ya başka bir router'a, ya başka bir router'daki başka bir tünele ya da yerel olarak.

Tunnel'ların hepsi aynı şekilde çalışır, ancak iki farklı gruba ayrılabilir - gelen tunnel'lar ve giden tunnel'lar. Gelen tunnel'ların güvenilmeyen bir gateway'i vardır ve bu gateway mesajları tunnel yaratıcısına doğru iletir, tunnel yaratıcısı ise tunnel endpoint'i olarak görev yapar. Giden tunnel'lar için ise tunnel yaratıcısı gateway olarak görev yapar ve mesajları uzak endpoint'e iletir.

Tunnel'ın yaratıcısı, tunnel'a hangi eşlerin katılacağını tam olarak seçer ve her birine gerekli yapılandırma verilerini sağlar. Herhangi bir sayıda atlama noktasına sahip olabilirler. Amaç, hem katılımcıların hem de üçüncü tarafların bir tunnel'ın uzunluğunu belirlemesini zorlaştırmak, hatta işbirliği yapan katılımcıların bile aynı tunnel'ın bir parçası olup olmadıklarını belirlemelerini zorlaştırmaktır (işbirliği yapan eşlerin tunnel'da birbirinin yanında bulunduğu durum hariç).

Pratikte, farklı amaçlar için bir dizi tunnel havuzu kullanılır - her yerel istemci hedefinin, anonimlik ve performans ihtiyaçlarını karşılayacak şekilde yapılandırılmış kendi gelen tunnel'ları ve giden tunnel'ları vardır. Ayrıca, router'ın kendisi netDb'ye katılmak ve tunnel'ların kendilerini yönetmek için bir dizi havuz bulundurur.

I2P, bu tunnel'lar ile bile doğası gereği paket anahtarlı bir ağdır ve paralel çalışan birden fazla tunnel'dan yararlanarak dayanıklılığı artırır ve yükü dengeler. Temel I2P katmanının dışında, istemci uygulamaları için isteğe bağlı uçtan uca akış kütüphanesi mevcuttur ve bu kütüphane mesaj yeniden sıralama, yeniden iletim, tıkanıklık kontrolü vb. dahil olmak üzere TCP benzeri işlevsellik sunar.

I2P tunnel terminolojisine genel bir bakış [tunnel genel bakış sayfasında](/docs/overview/tunnel-routing) bulunmaktadır.

## Tunnel İşlemi (Mesaj İşleme) {#tunnel.operation}

### Genel Bakış

Bir tunnel oluşturulduktan sonra, [I2NP mesajları](/docs/specs/i2np) işlenir ve tunnel üzerinden geçirilir. Tunnel işletimi, tunnel içindeki çeşitli eşler tarafından üstlenilen dört farklı sürece sahiptir.

1. İlk olarak, tunnel gateway bir dizi
   I2NP mesajını toplar ve bunları teslim için tunnel mesajlarına ön işler.
2. Sonra, bu gateway ön işlenmiş veriyi şifreler ve
   ilk hop'a iletir.
3. Bu peer ve sonraki tunnel
   katılımcıları, şifrelemenin bir katmanını açar, bunun
   tekrar olmadığını doğrular ve sonraki peer'a iletir.
4. Sonunda, tunnel mesajları gateway tarafından başlangıçta paketlenen I2NP mesajlarının
   yeniden birleştirildiği ve talep edildiği gibi iletildiği uç noktaya ulaşır.

Ara tunnel katılımcıları, gelen veya giden bir tunnel'da olup olmadıklarını bilmezler; her zaman bir sonraki atlama için "şifreleme" yaparlar. Bu nedenle, düz metin giden uç noktada ortaya çıkacak şekilde, giden tunnel ağ geçidinde "şifre çözmek" için simetrik AES şifrelemesinden yararlanırız.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Preprocessing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Postprocessing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Gateway (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively encrypt (using decryption operations)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation) to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Forward as instructed to Inbound Gateway or Router</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="4"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Endpoint (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Receive data</td>
    </tr>
  </tbody>
</table>
### Gateway İşleme {#tunnel.gateway}

#### Mesaj Ön İşleme {#tunnel.preprocessing}

Bir tunnel gateway'in işlevi, [I2NP mesajlarını](/docs/specs/i2np) parçalara ayırıp sabit boyutlu [tunnel mesajlarına](/docs/specs/tunnel-message) paketlemek ve tunnel mesajlarını şifrelemektir. Tunnel mesajları aşağıdakileri içerir:

- 4 baytlık bir Tunnel ID
- 16 baytlık bir IV (başlatma vektörü)
- Bir sağlama toplamı
- Gerekirse dolgu
- Bir veya daha fazla { teslim talimatı, I2NP mesaj parçası } çifti

Tunnel ID'leri her atlamada kullanılan 4 baytlık sayılardır - katılımcılar hangi tunnel ID ile gelen mesajları dinleyeceklerini ve bir sonraki atlamaya hangi tunnel ID ile iletmeleri gerektiğini bilirler, ve her atlama aldıkları mesajlar için tunnel ID'yi seçer. Tunnel'ların kendileri kısa ömürlüdür (10 dakika). Sonraki tunnel'lar aynı eş dizisi kullanılarak inşa edilse bile, her atlamanın tunnel ID'si değişecektir.

Düşmanların yol boyunca mesaj boyutunu ayarlayarak mesajları etiketlemesini önlemek için, tüm tunnel mesajları sabit 1024 bayt boyutundadır. Daha büyük I2NP mesajlarını barındırmak ve aynı zamanda daha küçük olanları daha verimli bir şekilde desteklemek için, gateway daha büyük I2NP mesajlarını her tunnel mesajı içinde yer alan parçalara böler. Uç nokta, I2NP mesajını parçalardan kısa bir süre boyunca yeniden oluşturmaya çalışır, ancak gerektiğinde onları atar.

Ayrıntılar [tunnel mesaj spesifikasyonunda](/docs/specs/tunnel-message) bulunmaktadır.

### Gateway Şifreleme

Mesajların dolgulu yük haline ön işlemden geçirilmesinden sonra, gateway rastgele 16 baytlık bir IV değeri oluşturur, bunu ve tunnel mesajını gerektiği kadar yinelemeli olarak şifreler ve {tunnelID, IV, şifrelenmiş tunnel mesajı} üçlüsünü bir sonraki hop'a iletir.

Gateway'de şifrelemenin nasıl yapıldığı tunnel'ın inbound veya outbound olmasına bağlıdır. Inbound tunnel'lar için, rastgele bir IV seçerler, bunu işleyerek ve güncelleyerek gateway için IV oluştururlar ve bu IV'yi kendi katman anahtarlarıyla birlikte kullanarak önceden işlenmiş veriyi şifrelerler. Outbound tunnel'lar için ise (şifrelenmemiş) IV ve önceden işlenmiş veriyi, tunnel'daki tüm hop'lar için IV ve katman anahtarlarıyla yinelemeli olarak deşifre etmeleri gerekir. Outbound tunnel şifrelemenin sonucu, her peer bunu şifrelediğinde endpoint'in başlangıçtaki önceden işlenmiş veriyi geri alacak olmasıdır.

### Katılımcı İşleme {#tunnel.participant}

Bir eş (peer) bir tunnel mesajı aldığında, mesajın daha önce olduğu gibi aynı önceki hoptan geldiğini kontrol eder (ilk mesaj tunnel'dan geçtiğinde başlatılır). Önceki eş farklı bir router ise veya mesaj daha önce görüldüyse, mesaj düşürülür. Katılımcı daha sonra alınan IV'yi mevcut IV'yi belirlemek için kendi IV anahtarını kullanarak AES256/ECB ile şifreler, o IV'yi katılımcının katman anahtarı ile veriyi şifrelemek için kullanır, mevcut IV'yi tekrar kendi IV anahtarını kullanarak AES256/ECB ile şifreler, ardından {nextTunnelId, nextIV, encryptedData} tuple'ını bir sonraki hopa iletir. IV'nin bu çift şifrelemesi (hem kullanım öncesi hem sonrası) belirli bir sınıf doğrulama saldırısını ele almaya yardımcı olur.

Yinelenen mesaj algılama, mesaj IV'leri üzerinde azalan Bloom filtresi ile gerçekleştirilir. Her router, katıldığı tüm tunnel'lar için alınan mesajın IV'si ile ilk bloğunun XOR'unu içeren tek bir Bloom filtresi tutar ve görülen girdileri 10-20 dakika sonra (tunnel'ların süresi dolacağı zaman) düşürecek şekilde değiştirilir. Bloom filtresinin boyutu ve kullanılan parametreler, ihmal edilebilir bir yanlış pozitif şansı ile router'ın ağ bağlantısını fazlasıyla doyurabilecek düzeydedir. Bloom filtresine beslenen benzersiz değer, IV ile ilk bloğun XOR'udur; bu, tunnel'daki sıralı olmayan işbirlikçi eşlerin IV ve ilk blok değiştirilerek mesajı yeniden göndererek etiketlemesini önlemek içindir.

### Uç Nokta İşleme {#tunnel.endpoint}

Tunnel'daki son hop'ta bir tunnel mesajını aldıktan ve doğruladıktan sonra, endpoint'in gateway tarafından kodlanan veriyi nasıl kurtaracağı tunnel'ın gelen (inbound) mi yoksa giden (outbound) tunnel mi olduğuna bağlıdır. Giden tunnel'lar için endpoint, mesajı diğer katılımcılar gibi kendi katman anahtarıyla şifreler ve önceden işlenmiş veriyi ortaya çıkarır. Gelen tunnel'lar için endpoint aynı zamanda tunnel yaratıcısıdır, bu nedenle her adımın katman ve IV anahtarlarını ters sırada kullanarak IV ve mesajı yinelemeli olarak şifresini çözebilir.

Bu noktada, tunnel uç noktası gateway tarafından gönderilen önceden işlenmiş veriyi alır, ardından bu veriyi içerdiği I2NP mesajlarına ayırarak teslimat talimatlarında belirtildiği şekilde iletebilir.

## Tunnel Oluşturma {#tunnel.building}

Bir tunnel oluştururken, yaratıcı gerekli yapılandırma verilerini içeren bir isteği her hop'a göndermeli ve tunnel'ı etkinleştirmeden önce hepsinin kabul etmesini beklemelidir. İstekler, yalnızca bir bilgi parçasını (tunnel katmanı veya IV anahtarı gibi) bilmesi gereken eşlerin o veriye erişebilmesi için şifrelenir. Ayrıca, yalnızca tunnel yaratıcısı eşin yanıtına erişim sahibi olacaktır. Tunnel'ları üretirken akılda tutulması gereken üç önemli boyut vardır: hangi eşlerin kullanıldığı (ve nerede), isteklerin nasıl gönderildiği (ve yanıtların nasıl alındığı), ve bunların nasıl korunduğu.

### Eş Seçimi {#tunnel.peerselection}

İki tunnel türünün - gelen ve giden - ötesinde, farklı tunnellar için kullanılan iki peer seçim tarzı vardır - exploratory ve client. Exploratory tunnellar hem network database bakımı hem de tunnel bakımı için kullanılırken, client tunnellar uçtan uca client mesajları için kullanılır.

#### Keşif Tunnel Eş Seçimi {#tunnel.selection.exploratory}

Keşif tunnel'ları, ağın bir alt kümesinden rastgele seçilen eşler kullanılarak oluşturulur. Belirli alt küme, yerel router'a ve onların tunnel yönlendirme ihtiyaçlarına göre değişir. Genel olarak, keşif tunnel'ları eşin "başarısız olmayan ama aktif" profil kategorisindeki rastgele seçilmiş eşlerden oluşturulur. Tunnel'ların ikincil amacı, sadece tunnel yönlendirmesinin ötesinde, az kullanılan yüksek kapasiteli eşleri bulmak ve bunları istemci tunnel'larında kullanmak üzere yükseltmektir.

Keşifsel peer seçimi [Peer Profilleme ve Seçim sayfasında](/docs/overview/peer-selection) daha ayrıntılı olarak ele alınmaktadır.

#### Client Tunnel Eş Seçimi {#tunnel.selection.client}

Client tunnel'ları daha katı gereksinimler seti ile inşa edilir - yerel router, performans ve güvenilirliğin client uygulamasının ihtiyaçlarını karşılayacak şekilde "hızlı ve yüksek kapasiteli" profil kategorisinden eşler seçecektir. Ancak, client'ın anonimlik ihtiyaçlarına bağlı olarak, bu temel seçimin ötesinde uyulması gereken birkaç önemli detay bulunmaktadır.

İstemci eş seçimi [Eş Profilleme ve Seçim sayfasında](/docs/overview/peer-selection) daha ayrıntılı olarak ele alınmaktadır.

#### Tunnel İçinde Eş Sıralaması {#ordering}

Eşler, [predecessor saldırısı](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([2008 güncellemesi](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)) ile başa çıkmak için tunnel'lar içinde sıralanır.

Predecessor saldırısını engellemek için tunnel seçimi, eşleri (peers) katı bir sırada tutar - eğer A, B ve C belirli bir tunnel havuzu için bir tunnel'da bulunuyorsa, A'dan sonraki hop her zaman B'dir ve B'den sonraki hop her zaman C'dir.

Sıralama, başlangıçta her tunnel havuzu için rastgele 32 baytlık bir anahtar oluşturarak gerçekleştirilir. Peer'lar sıralamayı tahmin edebilmemeli, aksi takdirde bir saldırgan tunnel'ın her iki ucunda olma şansını maksimize etmek için birbirinden uzak iki router hash'i oluşturabilir. Peer'lar, (peer'ın hash'i ile rastgele anahtar birleştirilmiş) SHA256 Hash'inin rastgele anahtardan XOR mesafesine göre sıralanır:

```
      p = peer hash
      k = random key
      d = XOR(H(p+k), k)
```
Her tunnel havuzu farklı bir rastgele anahtar kullandığından, sıralama tek bir havuz içinde tutarlıdır ancak farklı havuzlar arasında tutarlı değildir. Router her yeniden başlatıldığında yeni anahtarlar üretilir.

### İstek Teslimi {#tunnel.request}

Çok atlamalı bir tunnel, tekrar tekrar şifresi çözülen ve iletilen tek bir yapı mesajı kullanılarak oluşturulur. [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) terminolojisinde bu "etkileşimsiz" teleskopik tunnel oluşturma olarak adlandırılır.

Bu tunnel isteği hazırlama, iletim ve yanıt yöntemi, [açığa çıkan öncüllerin sayısını azaltmak](/docs/specs/tunnel-creation), iletilen mesaj sayısını kesmek, uygun bağlantıyı doğrulamak ve geleneksel teleskopik tunnel oluşturmanın mesaj sayma saldırısından kaçınmak için tasarlanmıştır. (Bir tunnel'ı zaten kurulmuş olan kısmı üzerinden genişletmek için mesaj gönderen bu yöntem, "Hashing it out" makalesinde "etkileşimli" teleskopik tunnel oluşturma olarak adlandırılmaktadır.)

Tunnel isteği ve yanıt mesajlarının detayları ve şifrelenmesi [burada belirtilmiştir](/docs/specs/tunnel-creation).

Eşler, çeşitli nedenlerle tunnel oluşturma isteklerini reddedebilir, ancak giderek artan şiddette dört tür reddetme türü bilinmektedir: olasılıksal reddetme (router'ın kapasitesine yaklaştığı için veya istek seline yanıt olarak), geçici aşırı yüklenme, bant genişliği aşırı yüklenme ve kritik arıza. Bu dört tür reddetme alındığında, tunnel oluşturucu tarafından söz konusu router'ın profilini ayarlamaya yardımcı olmak için yorumlanır.

Peer profiling hakkında daha fazla bilgi için [Peer Profiling ve Seçimi sayfasına](/docs/overview/peer-selection) bakın.

### Tunnel Havuzları {#tunnel.pooling}

Verimli çalışmaya izin vermek için, router bir dizi tunnel havuzu tutar ve her biri belirli bir amaç için kullanılan bir tunnel grubunu kendi yapılandırmasıyla yönetir. O amaç için bir tunnel gerektiğinde, router uygun havuzdan rastgele bir tane seçer. Genel olarak, iki keşif tunnel havuzu vardır - biri gelen ve biri giden - her ikisi de router'ın varsayılan yapılandırmasını kullanır. Ayrıca, her yerel hedef için bir çift havuz vardır - bir gelen ve bir giden tunnel havuzu. Bu havuzlar, yerel hedef [I2CP](/docs/specs/i2cp) aracılığıyla router'a bağlandığında belirtilen yapılandırmayı kullanır veya belirtilmemişse router'ın varsayılanlarını kullanır.

Her pool konfigürasyonunda, kaç tunnel'ın aktif tutulacağını, arıza durumunda kaç yedek tunnel'ın sürdürüleceğini, tunnel'ların ne kadar uzun olması gerektiğini, bu uzunlukların rastgele hale getirilip getirilmeyeceğini ve ayrı tunnel'lar yapılandırılırken izin verilen diğer ayarları tanımlayan birkaç temel ayar bulunur. Konfigürasyon seçenekleri [I2CP sayfasında](/docs/specs/i2cp) belirtilmiştir.

### Tunnel Uzunlukları ve Varsayılanlar {#length}

[Tunnel genel bakış sayfasında](/docs/overview/tunnel-routing#length).

### Önceden Hazırlık Yapma Stratejisi ve Öncelik {#strategy}

Tunnel oluşturma maliyetlidir ve tunnel'lar oluşturulduktan sonra sabit bir süre sonra sona erer. Ancak, tunnel'ları tükenen bir havuz olduğunda, Destination esasen ölür. Ayrıca, tunnel oluşturma başarı oranı hem yerel hem de küresel ağ koşullarıyla büyük ölçüde değişebilir. Bu nedenle, gereksiz tunnel oluşturmadan, çok erken oluşturmadan veya şifrelenmiş oluşturma mesajlarını oluşturup göndermek için çok fazla CPU veya bant genişliği tüketmeden, yeni tunnel'ların ihtiyaç duyulmadan önce başarıyla oluşturulmasını sağlamak için öngörülü, uyarlanabilir bir oluşturma stratejisi sürdürmek önemlidir.

Her bir {keşifsel/istemci, gelen/giden, uzunluk, uzunluk varyansı} tuple'ı için router, başarılı bir tunnel yapısı için gereken süre hakkında istatistikleri tutar. Bu istatistikleri kullanarak, bir tunnel'ın sona ermesinden ne kadar önce bir yedek oluşturmaya başlaması gerektiğini hesaplar. Başarılı bir yedek olmadan son kullanma süresi yaklaştıkça, paralel olarak birden fazla yapım denemesi başlatır ve gerekirse paralel deneme sayısını artıracaktır.

Bant genişliği ve CPU kullanımını sınırlamak için router ayrıca tüm havuzlarda bekleyen maksimum yapım denemesi sayısını da sınırlar. Kritik yapımlar (keşif tunnel'ları için olanlar ve tunnel'ları tükenen havuzlar için olanlar) öncelik alır.

## Tunnel Mesaj Sınırlama {#tunnel.throttling}

I2P içindeki tunnel'lar devre anahtarlamalı bir ağa benzese de, I2P içindeki her şey kesinlikle mesaj tabanlıdır - tunnel'lar sadece mesajların teslimini organize etmeye yardımcı olan muhasebe hileleridir. Mesajların güvenilirliği veya sıralaması hakkında hiçbir varsayım yapılmaz ve yeniden iletimler üst seviyeler (örneğin I2P'nin istemci katmanı akış kütüphanesi) tarafından gerçekleştirilir. Bu, I2P'nin hem paket anahtarlamalı hem de devre anahtarlamalı ağlar için mevcut olan kısıtlama tekniklerinden yararlanmasına olanak tanır. Örneğin, her router her tunnel'ın ne kadar veri kullandığının hareketli ortalamasını takip edebilir, bunu router'ın katıldığı diğer tüm tunnel'ların kullandığı ortalamalarla birleştirebilir ve kapasitesi ile kullanımına dayanarak ek tunnel katılım isteklerini kabul edebilir veya reddedebilir. Öte yandan, her router kapasitesini aşan mesajları basitçe bırakabilir ve normal Internet üzerinde kullanılan araştırmalardan yararlanabilir.

Mevcut uygulamada, router'lar ağırlıklı rastgele erken atma (WRED) stratejisi uygular. Tüm katılımcı router'lar (dahili katılımcı, gelen gateway ve giden endpoint) için, router, bant genişliği limitlerineapproached yaklaşıldıkça mesajların bir kısmını rastgele atmaya başlar. Trafik limitlere yaklaştıkça veya limitleri aştıkça, daha fazla mesaj atılır. Dahili katılımcı için, tüm mesajlar parçalanır ve doldurulur ve bu nedenle aynı boyuttadır. Ancak gelen gateway ve giden endpoint'te, atma kararı tam (birleştirilmiş) mesaj üzerinde verilir ve mesaj boyutu dikkate alınır. Büyük mesajların atılma olasılığı daha yüksektir. Ayrıca, mesajların giden endpoint'te atılma olasılığı gelen gateway'e göre daha yüksektir, çünkü bu mesajlar yolculuklarında o kadar "ileri" değildir ve bu nedenle bu mesajları atmanın ağ maliyeti daha düşüktür.

## Gelecek Çalışmalar {#future}

### Karıştırma/Toplu İşleme {#tunnel.mixing}

Gateway'de ve her hop'ta mesajları geciktirmek, yeniden sıralamak, yeniden yönlendirmek veya padding eklemek için hangi stratejiler kullanılabilir? Bu işlemler ne ölçüde otomatik olarak yapılmalı, ne kadarı tunnel başına veya hop başına ayar olarak yapılandırılmalı ve tunnel'ın yaratıcısı (ve dolayısıyla kullanıcı) bu işlemi nasıl kontrol etmeli? Tüm bunlar bilinmeyen olarak bırakılmıştır ve uzak bir gelecek sürümü için çözülecektir.

### Doldurma

Doldurma stratejileri çeşitli seviyelerde kullanılabilir ve mesaj boyutu bilgisinin farklı saldırganlara maruz kalmasını ele alır. Mevcut sabit tunnel mesaj boyutu 1024 bayttır. Ancak bunun içinde, parçalanmış mesajların kendileri tunnel tarafından hiç doldurulmaz, fakat uçtan uca mesajlar için garlic wrapping'in bir parçası olarak doldurulabilirler.

### WRED

WRED stratejileri uçtan uca performans ve ağ tıkanıklığı çöküşünün önlenmesi üzerinde önemli bir etkiye sahiptir. Mevcut WRED stratejisi dikkatli bir şekilde değerlendirilmeli ve iyileştirilmelidir.
