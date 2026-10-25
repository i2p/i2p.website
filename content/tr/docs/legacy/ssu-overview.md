---
title: "Güvenli Yarı-Güvenilir UDP (SSU)"
description: "SSU2'den önce kullanılan orijinal UDP taşıma protokolü (kullanımdan kaldırıldı)"
slug: "ssu-overview"
aliases:
  - "/tr/udp"
  - "/tr/udp/"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
---

**KULLANIM DIŞI** - SSU, SSU2 ile değiştirilmiştir. SSU desteği i2pd'den 2.44.0 sürümünde (API 0.9.56) 2022-11'de kaldırılmıştır. SSU desteği Java I2P'den 2.4.0 sürümünde (API 0.9.61) 2023-12'de kaldırılmıştır.

SSU (I2P belgelerinin ve kullanıcı arayüzlerinin çoğunda "UDP" olarak da adlandırılır) I2P'de uygulanan iki [transport](/docs/transport)'tan biriydi. Diğeri [NTCP2](/docs/specs/ntcp2)'dir. [NTCP](/docs/legacy/ntcp) desteği kaldırılmıştır.

SSU, I2P 0.6 sürümünde tanıtıldı. Standart bir I2P kurulumunda, router giden bağlantılar için hem NTCP hem de SSU kullanır. SSU-over-IPv6, 0.9.8 sürümünden itibaren desteklenmektedir.

SSU "yarı güvenilir" olarak adlandırılır çünkü onaylanmamış mesajları tekrar tekrar iletir, ancak yalnızca maksimum sayıda deneme yapar. Bundan sonra mesaj düşürülür.

## SSU Servisleri

NTCP aktarım protokolü gibi, SSU da güvenilir, şifreli, bağlantı odaklı, noktadan noktaya veri aktarımı sağlar. SSU'ya özgü olarak, aşağıdakiler dahil olmak üzere IP tespiti ve NAT geçiş hizmetleri de sunar:

- [Introducers](#introduction) kullanarak işbirlikçi NAT/Güvenlik duvarı geçişi
- Gelen paketlerin incelenmesi ve [peer testing](#peerTesting) ile yerel IP tespiti
- Güvenlik duvarı durumu ve yerel IP ile bunlardaki değişikliklerin NTCP'ye iletilmesi
- Güvenlik duvarı durumu ve yerel IP ile bunlardaki değişikliklerin router ve kullanıcı arayüzüne iletilmesi

## Router Adres Spesifikasyonu {#ra}

Aşağıdaki özellikler ağ veritabanında saklanır.

- **Transport name:** SSU
- **caps:** [B,C,4,6] [Aşağıya bakın](#capabilities).
- **host:** IP (IPv4 veya IPv6).
  Kısaltılmış IPv6 adresi ("::" ile) izin verilir.
  Güvenlik duvarı arkasındaysa mevcut olabilir veya olmayabilir.
  Host adları daha önce izin veriliyordu, ancak 0.9.32 sürümünden itibaren kullanımdan kaldırıldı. Öneri 141'e bakın.
- **iexp[0-2]:** Bu introducer'ın son kullanma tarihi.
  ASCII rakamları, epoch'tan bu yana saniye cinsinden.
  Yalnızca güvenlik duvarı arkasındaysa ve introducer'lar gerekiyorsa mevcut.
  İsteğe bağlı (bu introducer için diğer özellikler mevcut olsa bile).
  0.9.30 sürümünden itibaren, öneri 133.
- **ihost[0-2]:** Introducer'ın IP'si (IPv4 veya IPv6).
  Host adları daha önce izin veriliyordu, ancak 0.9.32 sürümünden itibaren kullanımdan kaldırıldı. Öneri 141'e bakın.
  Kısaltılmış IPv6 adresi ("::" ile) izin verilir.
  Yalnızca güvenlik duvarı arkasındaysa ve introducer'lar gerekiyorsa mevcut.
  [Aşağıya bakın](#introduction).
- **ikey[0-2]:** Introducer'ın Base 64 introduction anahtarı. [Aşağıya bakın](#key).
  Yalnızca güvenlik duvarı arkasındaysa ve introducer'lar gerekiyorsa mevcut.
  [Aşağıya bakın](#introduction).
- **iport[0-2]:** Introducer'ın portu 1024 - 65535.
  Yalnızca güvenlik duvarı arkasındaysa ve introducer'lar gerekiyorsa mevcut.
  [Aşağıya bakın](#introduction).
- **itag[0-2]:** Introducer'ın etiketi 1 - (2^32 - 1)
  ASCII rakamları.
  Yalnızca güvenlik duvarı arkasındaysa ve introducer'lar gerekiyorsa mevcut.
  [Aşağıya bakın](#introduction).
- **key:** Base 64 introduction anahtarı. [Aşağıya bakın](#key).
- **mtu:** İsteğe bağlı. Varsayılan ve maksimum 1484. Minimum 620.
  IPv6 için mevcut olmalıdır, burada minimum 1280 ve maksimum 1488'dir
  (maksimum, 0.9.28 sürümünden önce 1472 idi).
  IPv6 MTU, 16'nın katı olmalıdır.
  (IPv4 MTU + 4), 16'nın katı olmalıdır.
  [Aşağıya bakın](#mtu).
- **port:** 1024 - 65535
  Güvenlik duvarı arkasındaysa mevcut olabilir veya olmayabilir.

# Protokol Detayları

## Tıkanıklık Kontrolü {#congestioncontrol}

SSU'nun yalnızca yarı güvenilir teslimat, TCP uyumlu çalışma ve yüksek verim kapasitesi ihtiyacı, tıkanıklık kontrolünde büyük bir esneklik sağlar. Aşağıda özetlenen tıkanıklık kontrol algoritması hem bant genişliğinde verimli hem de uygulaması basit olacak şekilde tasarlanmıştır.

Paketler, router'ın giden kapasitesini aşmamaya ve uzak eşin ölçülen kapasitesini geçmemeye dikkat ederek router'ın politikasına göre planlanır. Ölçülen kapasite, TCP'nin yavaş başlangıç ve tıkanıklık önleme mekanizmaları doğrultusunda çalışır; gönderim kapasitesinde toplamsal artışlar ve tıkanıklık durumunda çarpımsal azalmalar gerçekleştirir. TCP'den farklı olarak, router'lar belirli bir süre veya yeniden iletim sayısından sonra bazı mesajları bırakırken diğer mesajları iletmeye devam edebilir.

Tıkanıklık tespit teknikleri de TCP'den farklıdır, çünkü her mesajın kendine özgü ve sıralı olmayan bir tanımlayıcısı vardır ve her mesajın sınırlı bir boyutu vardır - en fazla 32KB. Bu geri bildirimi gönderene verimli bir şekilde iletmek için, alıcı periyodik olarak tamamen ACK'lenmiş mesaj tanımlayıcılarının bir listesini içerir ve kısmen alınmış mesajlar için bit alanları da içerebilir; burada her bit bir fragmanın alınmasını temsil eder. Eğer yinelenen fragmanlar gelirse, mesaj tekrar ACK'lenmelidir veya mesaj hala tamamen alınmamışsa, bit alanı yeni güncellemelerle birlikte yeniden iletilmelidir.

Mevcut uygulama paketleri belirli bir boyuta doldurmaz, bunun yerine sadece tek bir mesaj parçasını pakete yerleştirir ve gönderir (MTU'yu aşmamaya dikkat ederek).

### MTU {#mtu}

Router sürüm 0.8.12 itibariyle, IPv4 için iki MTU değeri kullanılmaktadır: 620 ve 1484. MTU değeri, yeniden iletilen paketlerin yüzdesine göre ayarlanır.

Her iki MTU değeri için de (MTU % 16) == 12 olması arzu edilir, böylece 28 baytlık IP/UDP başlığından sonraki yük kısmı şifreleme amaçları için 16 baytın katı olur.

Küçük MTU değeri için, 2646 baytlık Variable Tunnel Build Message'ı birden fazla pakete verimli bir şekilde paketlemek arzu edilir; 620 baytlık MTU ile 5 pakete güzel bir şekilde sığar.

Ölçümlere dayanarak, 1492 neredeyse tüm makul boyuttaki küçük I2NP mesajlarına uyar (daha büyük I2NP mesajları 1900 ila 4500 bayt arasında olabilir ki bu zaten canlı ağ MTU'suna sığmayacaktır).

MTU değerleri 0.8.9 - 0.8.11 sürümleri için 608 ve 1492 idi. Büyük MTU değeri 0.8.9 sürümünden önce 1350 idi.

Maksimum alım paketi boyutu 0.8.12 sürümünden itibaren 1571 bayttır. 0.8.9 - 0.8.11 sürümlerinde 1535 bayttı. 0.8.9 sürümünden önce 2048 bayttı.

0.9.2 sürümünden itibaren, bir router'ın ağ arayüzü MTU değeri 1484'ten az ise, bunu network database'de yayınlayacak ve diğer router'lar bir bağlantı kurulduğunda buna saygı göstermelidir.

IPv6 için minimum MTU 1280'dir. IPv6 IP/UDP başlığı 48 bayttır, bu nedenle (MTU % 16 == 0) koşulunu sağlayan bir MTU kullanırız ve bu durum 1280 için geçerlidir. Maksimum IPv6 MTU 1488'dir. (0.9.28 sürümünden önce maksimum 1472 idi).

### Mesaj Boyutu Sınırları {#max}

Maksimum mesaj boyutu nominal olarak 32KB olmasına rağmen, pratik limit farklıdır. Protokol, fragment sayısını 7 bit veya 128 ile sınırlar. Ancak mevcut uygulama, her mesajı maksimum 64 fragment ile sınırlar, bu da 608 MTU kullanılırken 64 * 534 = 33.3 KB için yeterlidir. Paketlenmiş leaseSet'ler ve oturum anahtarları için ek yük nedeniyle, uygulama seviyesindeki pratik limit yaklaşık 6KB daha düşüktür, yani yaklaşık 26KB'dir. UDP taşıma limitini 32KB'ın üzerine çıkarmak için daha fazla çalışma gereklidir. Daha büyük MTU kullanan bağlantılar için daha büyük mesajlar mümkündür.

## Boşta Kalma Zaman Aşımı

Boşta kalma zaman aşımı ve bağlantı kapatma her uç noktanın takdirindedir ve değişiklik gösterebilir. Mevcut uygulama, bağlantı sayısı yapılandırılan maksimuma yaklaştıkça zaman aşımını düşürür ve bağlantı sayısı az olduğunda zaman aşımını artırır. Önerilen minimum zaman aşımı iki dakika veya daha fazla, önerilen maksimum zaman aşımı ise on dakika veya daha fazladır.

## Anahtarlar {#keys}

Kullanılan tüm şifreleme, 32 bayt anahtar ve 16 bayt IV'lere sahip AES256/CBC'dir. Alice, Bob ile bir oturum başlattığında, MAC ve oturum anahtarları DH değişiminin bir parçası olarak müzakere edilir ve daha sonra sırasıyla HMAC ve şifreleme için kullanılır. DH değişimi sırasında, Bob'un herkesçe bilinebilir introKey'i MAC ve şifreleme için kullanılır.

Hem başlangıç mesajı hem de sonraki yanıt, yanıtlayanın (Bob) introKey'ini kullanır - yanıtlayanın istekte bulunanın (Alice) introKey'ini bilmesi gerekmez. Bob tarafından kullanılan DSA imzalama anahtarı, Alice'in onunla iletişime geçtiğinde zaten Alice tarafından bilinmelidir, ancak Alice'in DSA anahtarı Bob tarafından henüz bilinmiyor olabilir.

Bir mesaj aldığında, alıcı "from" IP adresini ve portunu tüm kurulmuş oturumlarla kontrol eder - eşleşme varsa, o oturumdaki MAC anahtarları HMAC'te test edilir. Bunların hiçbiri doğrulanmazsa veya eşleşen IP adresi yoksa, alıcı MAC'te kendi introKey'ini dener. Bu da doğrulanmazsa, paket düşürülür. Doğrulanırsa, mesaj türüne göre yorumlanır, ancak alıcı aşırı yüklenmiş durumdaysa yine de düşürülebilir.

Alice ve Bob arasında kurulmuş bir oturum varsa, ancak Alice herhangi bir nedenle anahtarları kaybederse ve Bob ile iletişim kurmak isterse, SessionRequest ve ilgili mesajlar aracılığıyla istediği zaman yeni bir oturum kurabilir. Bob anahtarı kaybettiyse ancak Alice bunu bilmiyorsa, önce wantReply bayrağı ayarlanmış bir DataMessage göndererek Bob'u yanıt vermeye teşvik etmeye çalışacaktır ve Bob sürekli olarak yanıt veremezse, Alice anahtarın kaybolduğunu varsayarak yeni bir tane kuracaktır.

DH anahtar anlaşması için, [RFC3526](http://www.faqs.org/rfcs/rfc3526.html) 2048bit MODP grubu (#14) kullanılır:

```
  p = 2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
  g = 2
```
Bunlar I2P'nin [ElGamal şifrelemesi](/docs/specs/cryptography#elgamal) için kullanılan aynı p ve g değerleridir.

## Tekrar Saldırı Önleme {#replay}

SSU katmanında yeniden oynatma önleme, aşırı eski zaman damgalı paketleri veya bir IV'yi yeniden kullananları reddederek gerçekleşir. Yinelenen IV'leri tespit etmek için, yalnızca yakın zamanda eklenen IV'lerin tespit edilmesi amacıyla periyodik olarak "bozunan" bir dizi Bloom filtresi kullanılır.

DataMessage'larda kullanılan messageId'ler SSU transport katmanının üzerindeki katmanlarda tanımlanır ve şeffaf bir şekilde aktarılır. Bu ID'ler belirli bir sırada değildir - aslında tamamen rastgele olmaları muhtemeldir. SSU katmanı messageId tekrar oynatma önleme girişiminde bulunmaz - üst katmanlar bunu hesaba katmalıdır.

## Adresleme {#addressing}

Bir SSU peer ile iletişim kurmak için iki bilgi setinden biri gereklidir: peer'ın herkese açık olarak erişilebilir olduğu durumlarda doğrudan adres, veya peer'ı tanıtmak için üçüncü bir taraf kullanılması durumunda dolaylı adres. Bir peer'ın sahip olabileceği adres sayısında herhangi bir kısıtlama yoktur.

```
    Direct: host, port, introKey, options
  Indirect: tag, relayhost, port, relayIntroKey, targetIntroKey, options
```
Her adres ayrıca bir dizi seçeneği de ortaya çıkarabilir - o belirli peer'ın özel yetenekleri. Mevcut yeteneklerin listesi için [aşağıya](#capabilities) bakın.

Adresler, seçenekler ve yetenekler [ağ veritabanında](/docs/overview/network-database) yayınlanır.

## Doğrudan Oturum Kurulumu {#direct}

Doğrudan oturum kurulumu, NAT geçişi için üçüncü bir tarafa ihtiyaç duyulmadığında kullanılır. Mesaj dizisi şu şekildedir:

### Bağlantı Kurulumu (Doğrudan) {#establishDirect}

Alice doğrudan Bob'a bağlanır. IPv6, 0.9.8 sürümünden itibaren desteklenir.

```
        Alice                         Bob
    SessionRequest --------------------->
          <--------------------- SessionCreated
    SessionConfirmed ------------------->
          <--------------------- DeliveryStatusMessage
          <--------------------- DatabaseStoreMessage
    DatabaseStoreMessage --------------->
    Data <--------------------------> Data
```
SessionConfirmed mesajı alındıktan sonra, Bob onay olarak küçük bir [DeliveryStatus mesajı](/docs/specs/i2np#msg_DeliveryStatus) gönderir. Bu mesajda, 4 baytlık mesaj ID'si rastgele bir sayıya ayarlanır ve 8 baytlık "varış zamanı" mevcut ağ genelindeki ID'ye ayarlanır ki bu 2'dir (yani 0x0000000000000002).

Durum mesajı gönderildikten sonra, eşler genellikle [RouterInfo](/docs/specs/common-structures#struct_RouterInfo)'larını içeren [DatabaseStore mesajları](/docs/specs/i2np#msg_DatabaseStore) alışverişi yaparlar, ancak bu zorunlu değildir.

Durum mesajının türü veya içeriğinin önemli olduğu görülmemektedir. Başlangıçta DatabaseStore mesajı birkaç saniye geciktiği için eklenmişti; artık store anında gönderildiğinden, belki de durum mesajı kaldırılabilir.

## Giriş {#introduction}

Introduction anahtarları harici bir kanal (network database) aracılığıyla iletilir, burada geleneksel olarak 0.9.47 sürümüne kadar router Hash ile aynı olmuştur, ancak 0.9.48 sürümünden itibaren rastgele olabilir. Bir session anahtarı oluştururken kullanılmaları gerekir. Dolaylı adres için, peer önce relayhost ile iletişime geçmeli ve onlardan verilen tag altında o relayhost'ta bilinen peer'a bir introduction istemelidir. Mümkünse, relayhost adreslenmiş peer'a istekte bulunan peer ile iletişim kurmasını söyleyen bir mesaj gönderir ve aynı zamanda istekte bulunan peer'a adreslenmiş peer'ın bulunduğu IP ve portu verir. Ayrıca, bağlantı kuran peer, bağlandığı peer'ın public anahtarlarını önceden bilmelidir (ancak herhangi bir aracı relay peer için bu gerekli değildir).

Üçüncü taraf tanıtımı yoluyla dolaylı oturum kurulumu, verimli NAT geçişi için gereklidir. Charlie, gelen talep edilmemiş UDP paketlerine izin vermeyen bir NAT veya güvenlik duvarının arkasında bulunan bir router, önce birkaç eşe bağlanır ve bunlardan bazılarını tanıtıcı olarak görev yapmaları için seçer. Bu eşlerin her biri (Bob, Bill, Betty, vb.) Charlie'ye bir tanıtım etiketi - 4 baytlık rastgele bir sayı - sağlar ve Charlie bunu kendisiyle iletişim kurma yöntemi olarak herkese açık hale getirir. Charlie'nin yayınlanmış iletişim yöntemlerine sahip olan Alice adlı bir router, önce tanıtıcılardan bir veya daha fazlasına RelayRequest paketi gönderir ve her birinden kendisini Charlie ile tanıştırmasını ister (Charlie'yi tanımlamak için tanıtım etiketini sunar). Bob daha sonra Alice'in genel IP ve port numarasını içeren bir RelayIntro paketini Charlie'ye iletir, ardından Alice'e Charlie'nin genel IP ve port numarasını içeren bir RelayResponse paketi gönderir. Charlie RelayIntro paketini aldığında, Alice'in IP ve portuna küçük rastgele bir paket gönderir (NAT/güvenlik duvarında delik açar) ve Alice Bob'un RelayResponse paketini aldığında, belirtilen IP ve port ile yeni bir tam yönlü oturum kurulumuna başlar.

### Bağlantı Kurulumu (Tanıtıcı Kullanarak Dolaylı) {#establishIndirect}

Alice önce tanıtıcı Bob'a bağlanır, Bob da isteği Charlie'ye iletir.

```
        Alice                         Bob                  Charlie
    RelayRequest ---------------------->
         <-------------- RelayResponse    RelayIntro ----------->
         <-------------------------------------------- HolePunch (data ignored)
    SessionRequest -------------------------------------------->
         <-------------------------------------------- SessionCreated
    SessionConfirmed ------------------------------------------>
         <-------------------------------------------- DeliveryStatusMessage
         <-------------------------------------------- DatabaseStoreMessage
    DatabaseStoreMessage -------------------------------------->
    Data <--------------------------------------------------> Data
```
Hole punch işleminden sonra, oturum Alice ve Charlie arasında doğrudan kurulumdaki gibi kurulur.

### IPv6 Notları

IPv6, 0.9.8 sürümünden itibaren desteklenmektedir. Yayınlanan relay adresleri IPv4 veya IPv6 olabilir ve Alice-Bob iletişimi IPv4 veya IPv6 üzerinden gerçekleştirilebilir. 0.9.49 sürümüne kadar Bob-Charlie ve Alice-Charlie iletişimi yalnızca IPv4 üzerinden yapılmaktadır. IPv6 için relay desteği 0.9.50 sürümünden itibaren sağlanmaktadır. Ayrıntılar için spesifikasyona bakınız.

Spesifikasyon 0.9.8 sürümünden itibaren değiştirilmiş olsa da, IPv6 üzerinden Alice-Bob iletişimi aslında 0.9.50 sürümüne kadar desteklenmiyordu. Java router'ların önceki sürümleri, IPv6 üzerinden introducer olarak çalışmadıkları halde, IPv6 adresleri için 'C' yeteneğini hatalı bir şekilde yayınlıyorlardı. Bu nedenle, router'lar IPv6 adresindeki 'C' yeteneğine yalnızca router sürümü 0.9.50 veya daha yüksekse güvenmelidir.

## Eş Testi {#peerTesting}

Eş düğümler için işbirlikçi erişilebilirlik testinin otomasyonu, bir dizi PeerTest mesajı ile sağlanır. Doğru şekilde yürütüldüğünde, bir eş düğüm kendi erişilebilirliğini belirleyebilir ve davranışını buna göre güncelleyebilir. Test süreci oldukça basittir:

```
        Alice                  Bob                  Charlie
    PeerTest ------------------->
                             PeerTest-------------------->
                                <-------------------PeerTest
         <-------------------PeerTest
         <------------------------------------------PeerTest
    PeerTest------------------------------------------>
         <------------------------------------------PeerTest
```
PeerTest mesajlarının her biri, Alice tarafından başlatılan test serisini tanımlayan bir nonce taşır. Alice beklediği belirli bir mesajı almazsa, buna göre yeniden iletim yapacak ve aldığı verilere veya eksik mesajlara dayanarak erişilebilirliğini öğrenecektir. Ulaşılabilecek çeşitli son durumlar şu şekildedir:

- Eğer Bob'dan bir yanıt almazsa, belirli bir sayıya kadar yeniden iletim yapacaktır, ancak hiçbir zaman yanıt gelmezse, güvenlik duvarının veya NAT'ının bir şekilde yanlış yapılandırıldığını, giden bir pakete doğrudan yanıt olarak bile gelen tüm UDP paketlerini reddettiğini anlayacaktır. Alternatif olarak, Bob çalışmıyor olabilir veya Charlie'nin yanıt vermesini sağlayamıyor olabilir.

- Alice, üçüncü bir taraftan (Charlie) beklenen nonce ile bir PeerTest mesajı almazsa, Bob'un cevabını almış olsa bile Bob'a gönderdiği ilk isteği belirli sayıda yeniden gönderir. Charlie'nin ilk mesajı hala ulaşmıyorsa ancak Bob'unki ulaşıyorsa, Alice bir NAT veya firewall arkasında olduğunu ve istenmeyen bağlantı girişimlerinin reddedildiğini ve port forwarding'in düzgün çalışmadığını anlar (Bob'un sunduğu IP ve port yönlendirilmiş olmalıdır).

- Eğer Alice, Bob'un PeerTest mesajını ve Charlie'nin her iki PeerTest mesajını alır ancak Bob'un ve Charlie'nin ikinci mesajlarındaki kapsanan IP ve port numaraları eşleşmezse, simetrik bir NAT'ın arkasında olduğunu bilir; bu NAT, tüm giden paketlerini her bağlantı kurulan peer için farklı 'from' portları ile yeniden yazar. Bu durumda açıkça bir port yönlendirmesi yapması ve uzaktan bağlantı için bu portu her zaman açık tutması gerekir, bundan sonraki port keşfini yok sayar.

- Eğer Alice, Charlie'nin ilk mesajını alır ama ikincisini almazsa,
  PeerTest mesajını Charlie'ye belirli bir sayıda yeniden iletir,
  ancak yanıt alınmazsa Charlie'nin kafasının karıştığını veya
  artık çevrimiçi olmadığını bilir.

Alice, peer testlerine katılma yeteneği olan bilinen eşler arasından Bob'u rastgele seçmelidir. Bob da benzer şekilde, peer testlerine katılabilecek yetenekte olan ve hem Bob'tan hem de Alice'ten farklı bir IP'de bulunan tanıdığı eşler arasından Charlie'yi rastgele seçmelidir. İlk hata koşulu oluşursa (Alice, Bob'tan PeerTest mesajları alamazsa), Alice yeni bir eşi Bob olarak belirlemeye karar verebilir ve farklı bir nonce ile yeniden deneyebilir.

Alice'in tanıtım anahtarı, Charlie'nin ek bilgi gerektirmeden onunla iletişim kurabilmesi için tüm PeerTest mesajlarında yer alır. 0.9.15 sürümünden itibaren Alice'in sahtecilik saldırılarını önlemek için Bob ile kurulmuş bir oturumu olmalıdır. Peer testinin geçerli olabilmesi için Alice'in Charlie ile kurulmuş bir oturumu olmamalıdır. Alice daha sonra Charlie ile bir oturum kurabilir, ancak bu zorunlu değildir.

### IPv6 Notları

0.9.26 sürümü dahil olmak üzere, yalnızca IPv4 adreslerinin test edilmesi desteklenmektedir. Yalnızca IPv4 adreslerinin test edilmesi desteklenmektedir. Bu nedenle, tüm Alice-Bob ve Alice-Charlie iletişimi IPv4 üzerinden olmalıdır. Ancak Bob-Charlie iletişimi IPv4 veya IPv6 üzerinden olabilir. Alice'in adresi, PeerTest mesajında belirtildiğinde, 4 bayt olmalıdır. 0.9.27 sürümünden itibaren, IPv6 adreslerinin test edilmesi desteklenmektedir ve Bob ve Charlie yayınlanmış IPv6 adreslerinde bir 'B' özelliği ile desteği belirtirse, Alice-Bob ve Alice-Charlie iletişimi IPv6 üzerinden olabilir. Ayrıntılar için [Öneri 126](/spec/proposals/126-ipv6-peer-testing)'ya bakın.

0.9.50 sürümünden önce, Alice isteği Bob'a test etmek istediği transport (IPv4 veya IPv6) üzerinden mevcut bir oturum kullanarak gönderir. Bob, Alice'den IPv4 üzerinden bir istek aldığında, IPv4 adresi yayınlayan bir Charlie seçmelidir. Bob, Alice'den IPv6 üzerinden bir istek aldığında, IPv6 adresi yayınlayan bir Charlie seçmelidir. Gerçek Bob-Charlie iletişimi IPv4 veya IPv6 üzerinden olabilir (yani Alice'in adres türünden bağımsızdır).

0.9.50 sürümünden itibaren, eğer mesaj bir IPv4 peer testi için IPv6 üzerinden gönderiliyorsa veya (0.9.50 sürümünden itibaren) bir IPv6 peer testi için IPv4 üzerinden gönderiliyorsa, Alice kendi tanıtım adresini ve portunu dahil etmelidir.

Ayrıntılar için [Önerge 158](/spec/proposals/158)'e bakın.

## İletim Penceresi, ACK'ler ve Yeniden İletimler {#acks}

DATA mesajı, tam mesajların ACK'lerini ve bir mesajın bireysel parçalarının kısmi ACK'lerini içerebilir. Ayrıntılar için [protokol spesifikasyonu sayfasının](/docs/legacy/ssu) data mesajı bölümüne bakın.

Pencere yönetimi, ACK ve yeniden iletim stratejilerinin ayrıntıları burada belirtilmemiştir. Mevcut uygulama için Java koduna bakın. Kurulum aşamasında ve peer testi için, router'lar yeniden iletim için üstel geri çekilme (exponential backoff) uygulamalıdır. Kurulu bir bağlantı için, router'lar TCP veya [streaming](/docs/api/streaming)'e benzer şekilde ayarlanabilir iletim penceresi, RTT tahmini ve zaman aşımı uygulamalıdır. Başlangıç, minimum ve maksimum parametreler için koda bakın.

## Güvenlik {#security}

UDP kaynak adresleri tabii ki sahte olabilir. Ayrıca, belirli SSU mesajları içindeki IP'ler ve portlar (RelayRequest, RelayResponse, RelayIntro, PeerTest) meşru olmayabilir. Ayrıca, belirli eylemler ve yanıtlar hız sınırlaması gerektirebilir.

Doğrulama detayları burada belirtilmemiştir. Uygulayıcılar uygun yerlerde savunma mekanizmaları eklemelidir.

## Eş Yetenekleri {#capabilities}

Bir veya daha fazla yetenek "caps" seçeneğinde yayınlanabilir. Yetenekler herhangi bir sırada olabilir, ancak implementasyonlar arası tutarlılık için "BC46" önerilen sıralamadır.

**B** : Peer adresinde 'B' kabiliyeti bulunuyorsa, bu onların peer testlerine 'Bob' veya 'Charlie' olarak katılmaya istekli ve yetenekli olduklarını ifade eder. 0.9.26 sürümüne kadar peer testing IPv6 adresleri için desteklenmiyordu ve IPv6 adresi için mevcut olan 'B' kabiliyeti göz ardı edilmeliydi. 0.9.27 sürümünden itibaren peer testing IPv6 adresleri için desteklenmekte olup, IPv6 adresinde 'B' kabiliyetinin varlığı veya yokluğu gerçek desteği (veya destek eksikliğini) gösterir.

**C** : Eğer peer adresi 'C' yeteneğini içeriyorsa, bu onların o adres üzerinden introducer (tanıtıcı) olarak hizmet vermeye istekli ve yetenekli olduğu anlamına gelir - başka türlü erişilemeyen Charlie için introducer Bob rolünü üstlenirler. 0.9.50 sürümünden önce, Java router'lar IPv6 introducer'ları tam olarak uygulanmamış olmasına rağmen, IPv6 adresleri için 'C' yeteneğini yanlış bir şekilde yayınlıyordu. Bu nedenle, router'lar 0.9.50'den önceki sürümlerin 'C' yeteneği ilan edilse bile IPv6 üzerinden introducer rolü üstlenemeyeceğini varsaymalıdır.

**4** : 0.9.50 sürümünden itibaren, giden IPv4 yeteneğini belirtir. Host alanında bir IP yayınlanmışsa, bu yetenek gerekli değildir. Bu, IPv4 tanıtımları için introducer'ları olan bir adresse, '4' dahil edilmelidir. Router gizliyse, '4' ve '6' tek bir adreste birleştirilebilir.

**6** : 0.9.50 sürümünden itibaren, giden IPv6 yeteneğini belirtir. Host alanında bir IP yayınlanmışsa, bu yetenek gerekli değildir. Bu, IPv6 tanıtımları için introducer'ları olan bir adres ise, '6' dahil edilmelidir (şu anda desteklenmemektedir). Router gizli ise, '4' ve '6' tek bir adreste birleştirilebilir.

# Gelecek Çalışmalar {#future}

Not: Bu sorunlar SSU2 geliştirme sürecinde ele alınacaktır.

- Mevcut SSU performansının analizi, pencere boyutu ayarlaması ve diğer parametrelerin değerlendirilmesi dahil olmak üzere, ve performansı iyileştirmek için protokol uygulamasının ayarlanması gelecekteki çalışmalar için bir konudur.

- Mevcut uygulama aynı paketler için tekrar tekrar onaylar gönderiyor,
  bu da gereksiz yere ek yük artışına neden oluyor.

- 620'lik varsayılan küçük MTU değeri analiz edilmeli ve muhtemelen artırılmalıdır.
  Mevcut MTU ayarlama stratejisi değerlendirilmelidir.
  Streaming lib 1730-byte paketi 3 küçük SSU paketine sığar mı? Muhtemelen hayır.

- Protokol, kurulum sırasında MTU'ları değiş tokuş etmek için genişletilmelidir.

- Rekeying şu anda uygulanmamıştır ve hiçbir zaman uygulanmayacaktır.

- RelayIntro ve RelayResponse'daki 'challenge' alanlarının potansiyel kullanımı ve SessionRequest ile SessionCreated'daki padding alanının kullanımı belgelenmemiştir.

- Sabit paket boyutları kümesi, veri parçalanmasını dış düşmanlara karşı daha da gizlemek için uygun olabilir, ancak o zamana kadar çoğu ihtiyaç için tunnel, garlic ve uçtan uca padding yeterli olmalıdır.

- SessionCreated ve SessionConfirmed içindeki oturum açma zamanları kullanılmıyor veya doğrulanmıyor gibi görünüyor.

# Spesifikasyon {#spec}

[Artık SSU spesifikasyon sayfasında](/docs/legacy/ssu).
