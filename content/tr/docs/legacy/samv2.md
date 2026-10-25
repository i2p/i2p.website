---
title: "SAM V2 Spesifikasyonu"
description: "Eski Basit Anonim Mesajlaşma protokolü sürüm 2 (kullanımdan kaldırıldı)"
slug: "samv2"
aliases:
  - "/tr/docs/api/samv2"
  - "/tr/docs/api/samv2/"
  - "/tr/samv2"
  - "/tr/samv2/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## Uyarı - Kullanımdan Kaldırıldı - Desteklenmiyor - [SAMv3](/docs/api/samv3) Kullanın

Aşağıda I2P ile etkileşim için basit bir istemci protokolünün 2. sürümü belirtilmiştir.

SAM V2, I2P sürüm 0.6.1.31'de tanıtıldı. SAM V1'den önemli farklar "\*\*\*" ile işaretlenmiştir. Alternatifler: [SAM V1](/docs/api/sam), [SAM V3](/docs/api/samv3), [BOB](/docs/api/bob).

## Sürüm 2 Değişiklikleri

SAM V2, I2P sürümü 0.6.1.31'de tanıtıldı. Sürüm 1 ile karşılaştırıldığında, SAM v2 aynı I2P hedefi üzerinde birden fazla soketi *paralel olarak* yönetme yolu sağlar, yani istemci bir soketten veri göndermeden önce diğer soketten veri göndermeyi beklemek zorunda değildir. Tüm veriler aynı istemci\<--\>SAM soketi üzerinden geçer. Çoklu soketler için [SAM V3](/docs/api/samv3)'e bakın.

### I2P 0.9.14 Değişiklikleri

Bildirilen sürüm "2.0" olarak kalıyor.

- DEST GENERATE artık bir SIGNATURE_TYPE parametresini destekliyor.
- HELLO VERSION'daki MIN parametresi artık isteğe bağlı.
- HELLO VERSION'daki MIN ve MAX parametreleri artık "3" gibi tek haneli sürümleri destekliyor.

## Versiyon 2 Protokolü

İstemci uygulaması, tüm I2P işlevselliğini yöneten SAMv3 köprüsüyle iletişim kurar (sanal akışlar için streaming kütüphanesini veya eşzamansız mesajlar için doğrudan I2CP kullanarak).

Tüm istemci\<--\>SAM köprüsü iletişimi tek bir TCP soket üzerinden şifrelenmemiş ve kimlik doğrulaması yapılmamış olarak gerçekleşir. SAM köprüsüne erişim güvenlik duvarları veya diğer yöntemlerle korunmalıdır (belki köprü hangi IP'lerden bağlantı kabul ettiği konusunda ACL'lere sahip olabilir).

Tüm bu SAM mesajları düz ASCII formatında tek bir satırda gönderilir ve yeni satır karakteri (\\n) ile sonlandırılır. Aşağıda gösterilen biçimlendirme yalnızca okunabilirlik içindir ve her mesajdaki ilk iki kelimenin belirli sıralarında kalması gerekse de, anahtar=değer çiftlerinin sıralaması değişebilir (örneğin "ONE TWO A=B C=D" veya "ONE TWO C=D A=B" her ikisi de tamamen geçerli yapılardır). Ayrıca protokol büyük/küçük harf duyarlıdır.

SAM mesajları UTF-8 olarak yorumlanır. Key=value çiftleri tek bir boşlukla ayrılmalıdır. Değerler boşluk içeriyorsa çift tırnak içine alınabilir, örneğin key="uzun değer metni". Kaçış mekanizması yoktur.

İletişim üç farklı biçimde gerçekleşebilir:

- [Sanal akışlar](/docs/api/streaming)
- [Yanıtlanabilir datagramlar](/docs/specs/datagrams#repliable) (FROM alanı olan mesajlar)
- [Anonim datagramlar](/docs/specs/datagrams#raw) (ham anonim mesajlar)

## SAM Bağlantı El Sıkışması

İstemci ve köprü bir protokol sürümü üzerinde anlaşana kadar hiçbir SAM iletişimi gerçekleşemez; bu işlem istemcinin bir HELLO göndermesi ve köprünün bir HELLO REPLY göndermesi ile yapılır:

```
HELLO VERSION MIN=$min MAX=$max
```
ve

```
*** HELLO REPLY RESULT=$result VERSION=2.0
```
I2P 0.9.14 sürümünden itibaren MIN parametresi isteğe bağlıdır. MAX parametresi sağlanmalı ve sürüm 2'yi kullanmak için "2"den büyük veya eşit ve "3"ten küçük olmalıdır.

RESULT değeri şunlardan biri olabilir:

- `OK`
- `NOVERSION`

## SAM Oturumları

Bir SAM oturumu, istemcinin SAM köprüsüne bir soket açması, el sıkışma işlemi gerçekleştirmesi ve SESSION CREATE mesajı göndermesiyle oluşturulur ve soket bağlantısı kesildiğinde oturum sonlanır.

Her I2P Destination aynı anda yalnızca bir SAM oturumu için kullanılabilir ve bu formlardan yalnızca birini kullanabilir (diğer formlar aracılığıyla alınan mesajlar bırakılır).

İstemci tarafından köprüye gönderilen SESSION CREATE mesajı aşağıdaki gibidir:

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION, mesaj/akış gönderme ve alma için hangi destination'ın kullanılması gerektiğini belirtir. Eğer bir $name verilirse, SAM bridge kendi yerel depolama alanında (sam.keys dosyası) ilişkili bir destination (ve özel anahtar) arar. Bu isimle eşleşen bir ilişki yoksa, yeni bir tane oluşturur. Destination TRANSIENT olarak belirtilirse, her zaman yeni bir tane oluşturur.

DESTINATION'ın bir tanımlayıcı olduğunu, Base 64 kodlanmış veri *olmadığını* unutmayın. Destination'ı belirtmek için [SAM V3](/docs/api/samv3) kullanmalısınız.

DIRECTION yalnızca STREAM oturumları için belirtilebilir ve köprüye istemcinin stream'ler oluşturacağını veya alacağını ya da her ikisini birden yapacağını bildirir. Bu belirtilmezse, BOTH varsayılacaktır. DIRECTION=RECEIVE olduğunda giden bir stream oluşturmaya çalışmak hatayla sonuçlanmalıdır ve DIRECTION=CREATE olduğunda gelen stream'ler göz ardı edilecektir.

Verilen ek seçenekler, SAM köprüsü tarafından yorumlanmadıysa I2P oturum yapılandırmasına aktarılmalıdır (örneğin "tunnels.depthInbound=0"). Bu seçenekler aşağıda belgelenmiştir.

SAM bridge'in kendisi zaten I2P üzerinden hangi router ile iletişim kurması gerektiği konusunda yapılandırılmış olmalıdır (gerekirse bir geçersiz kılma yolu olabilir, örneğin i2cp.tcp.host=localhost ve i2cp.tcp.port=7654).

Session create mesajını aldıktan sonra, SAM bridge bir session durum mesajı ile yanıt verecektir, şu şekilde:

```
SESSION STATUS
        RESULT=$result
        DESTINATION={$name,TRANSIENT}
        [MESSAGE=...]
```
RESULT değeri aşağıdakilerden biri olabilir:

- `OK`
- `DUPLICATED_DEST`
- `I2P_ERROR`
- `INVALID_KEY`

Eğer uygun değilse, MESSAGE oturumun neden oluşturulamadığına dair insan tarafından okunabilir bilgi içermelidir.

$name bulunamadığında uyarı verilmediğini ve bunun yerine geçici bir hedef oluşturulduğunu unutmayın. Gerçek geçici base 64 hedefinin yanıtta çıktı olarak verilmediğini unutmayın; SESSION CREATE'te sağlanan $name veya TRANSIENT'tir. Bu özelliklere ihtiyacınız varsa, [SAM V3](/docs/api/samv3) kullanmalısınız.

## SAM Sanal Akışları

Sanal akışların güvenilir bir şekilde ve sırayla gönderileceği garanti edilir ve başarısızlık ile başarı bildirimleri mevcut olur olmaz iletilir.

STYLE=STREAM ile oturum kurulduktan sonra, hem istemci hem de SAM bridge, stream'leri yönetmek için aşağıda listelenen çeşitli mesajları eşzamansız olarak karşılıklı gönderebilir:

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
Bu, yerel hedeften belirtilen eşe yeni bir sanal bağlantı kurar ve bunu oturum kapsamlı benzersiz kimlikle işaretler. Benzersiz kimlik, 1'den (2^31-1)'e kadar olan ASCII tabanlı 10'luk bir tamsayıdır.

$destination, [Destination](/docs/specs/common-structures#type_Destination)'ın base 64'üdür ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakteri (binary olarak 387 veya daha fazla bayt) içerir.

SAM bridge buna bir stream durum mesajı ile yanıt verir:

```
STREAM STATUS
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
RESULT değeri şunlardan biri olabilir:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `INVALID_KEY`
- `TIMEOUT`

RESULT OK ise, belirtilen hedef çalışır durumda ve bağlantıyı yetkilendirmiştir; bağlantı mümkün değilse (zaman aşımı, vb.), RESULT uygun hata değerini içerecektir (isteğe bağlı olarak insan tarafından okunabilir bir MESSAGE ile birlikte).

Alıcı tarafında, SAM köprüsü istemciyi aşağıdaki gibi bilgilendirir:

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
Bu, istemciye verilen hedefin kendisiyle sanal bir bağlantı oluşturduğunu bildirir. Takip eden veri akışı, -1'den -(2^31-1)'e kadar olan ASCII taban 10 tam sayısı olan verilen benzersiz ID ile işaretlenecektir.

$destination, [Destination](/docs/specs/common-structures#type_Destination)'ın base 64 kodlamasıdır ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakter (binary olarak 387 veya daha fazla bayt) içerir.

İstemci sanal bağlantı üzerinden veri göndermek istediğinde, bunu şu şekilde yapar:

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Bu, SAM bridge'den sanal bağlantı üzerinden peer'a gönderilen tampona belirtilen veriyi eklemesini ister. Gönderim boyutu $numBytes, yeni satırdan sonra dahil edilen 8bit byte sayısını belirtir ve bu 1 ile 32768 (32KB) arasında olabilir.

**\*\*\* SAM köprüsü hemen şu şekilde yanıtlar:**

```
*** STREAM SEND
***        ID=$id
***        RESULT=$result
***        STATE=$bufferState
```
**\*\*\*** burada $bufferState şunlar olabilir:

- `BUFFER_FULL` - SAM'ın tamponu 32 veya daha fazla KB veri göndermeye hazır ve sonraki SEND istekleri başarısız olacak
- `READY` - SAM'ın tamponu dolu değil ve bir sonraki SEND isteğinin başarılı olması garanti ediliyor

**\*\*\*** ve $result şunlardan biridir:

- `OK` - veri başarıyla arabelleğe alındı
- `FAILED` - arabellek doluydu, hiçbir veri arabelleğe alınmadı

**\*\*\*** SAM bridge BUFFER_FULL ile yanıtladıysa, tamponu tekrar müsait olur olmaz başka bir mesaj gönderecektir:

```
*** STREAM READY_TO_SEND ID=$id
```
**\*\*\*** Sonuç OK olduğunda, SAM bridge mesajı mümkün olduğunca hızlı ve verimli bir şekilde teslim etmek için elinden geleni yapacak, muhtemelen birden fazla SEND mesajını birlikte arabelleğe alacaktır. Veri tesliminde bir hata olursa veya uzak taraf bağlantıyı kapatırsa, SAM bridge istemciye şunu söyleyecektir:

```
STREAM CLOSED
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
RESULT değeri aşağıdakilerden biri olabilir:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `PEER_NOT_FOUND`
- `TIMEOUT`

Bağlantı diğer peer tarafından düzgün bir şekilde kapatılmışsa, $result değeri OK olarak ayarlanır. $result değeri OK değilse, MESSAGE "peer erişilemez" gibi açıklayıcı bir mesaj içerebilir. Bir client bağlantıyı kapatmak istediğinde, SAM bridge'e close mesajını gönderir:

```
STREAM CLOSE
       ID=$id
```
Bridge daha sonra ihtiyaç duyduğu şeyleri temizler ve bu ID'yi atar - artık bu ID üzerinden hiçbir mesaj gönderilemez veya alınamaz.

İletişimin diğer tarafı için, peer veri gönderdiğinde ve bu veri istemci için mevcut olduğunda, SAM köprüsü bunu derhal teslim edecektir:

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
**\*\*\*** SAM sürüm 2.0 ile birlikte, istemci önce SAM köprüsüne tüm oturum için ne kadar gelen veriye izin verildiğini bir mesaj göndererek bildirmek zorundadır:

```
*** STREAM RECEIVE
***        ID=$id
***        LIMIT=$limit\n
```
**\*\*\*** burada $limit şunlar olabilir:

- `NONE` - SAM bridge dinlemeye devam eder ve gelen veriyi iletir (sürüm 1.0'daki davranışla aynı)
- bir tamsayı (2^64'ten küçük) - SAM bridge'in gelen akışı dinlemeyi durduracağı alınan bayt sayısı. İstemci akıştan daha fazla bayt kabul etmeye hazır olduğunda, daha büyük bir $limit ile böyle bir mesajı tekrar göndermesi gerekir.

**\*\*\*** İstemci, eşe bağlantı kurulduktan sonra, yani SAM bridge'den "STREAM CONNECTED" veya "STREAM STATUS RESULT=OK" aldıktan sonra bu tür STREAM RECEIVE mesajlarını göndermek zorundadır.

Tüm akışlar, SAM köprüsü ile istemci arasındaki bağlantının kesilmesi ile örtük olarak kapatılır.

## SAM Yanıtlanabilir Veri Paketleri

I2P doğası gereği bir FROM adresi içermese de, kullanım kolaylığı için ek bir katman olarak yanıtlanabilir datagramlar sağlanır - FROM adresi içeren 31744 bayta kadar olan sırasız ve güvenilmez mesajlar (başlık materyali için 1KB'ye kadar yer bırakır). Bu FROM adresi SAM tarafından dahili olarak doğrulanır (kaynağı doğrulamak için destination'ın imzalama anahtarını kullanır) ve tekrar oynatma koruması içerir.

Minimum boyut 1'dir. En iyi teslimat güvenilirliği için, önerilen maksimum boyut yaklaşık 11 KB'dir.

SAM oturumu STYLE=DATAGRAM ile kurduktan sonra, istemci SAM köprüsüne gönderebilir:

```
DATAGRAM SEND
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
Bir datagram geldiğinde, bridge bunu istemciye şu yolla teslim eder:

```
DATAGRAM RECEIVED
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
$destination, [Destination](/docs/specs/common-structures#type_Destination)'ın base 64 kodlamasıdır ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakter (binary olarak 387 veya daha fazla bayt) içerir.

SAM bridge hiçbir zaman istemciye kimlik doğrulama başlıklarını veya diğer alanları göstermez, yalnızca gönderenin sağladığı verileri iletir. Bu durum oturum kapatılana kadar (istemcinin bağlantıyı kesmesiyle) devam eder.

## SAM Anonim Datagramları

I2P'nin bant genişliğinden en iyi şekilde yararlanmak için SAM, istemcilerin anonim datagramlar göndermesine ve almasına olanak tanır, kimlik doğrulama ve yanıt bilgilerini istemcinin kendisine bırakır. Bu datagramlar güvenilmez ve sırasızdır ve 32768 bayta kadar olabilir.

Minimum boyut 1'dir. En iyi teslim güvenilirliği için önerilen maksimum boyut yaklaşık 11 KB'dir.

STYLE=RAW ile bir SAM oturumu kurduktan sonra, istemci SAM bridge'e şunu gönderebilir:

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
$destination, [Destination](/docs/specs/common-structures#type_Destination)'ın base 64 karşılığıdır ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakter (ikili formatta 387 veya daha fazla bayt) içerir.

Ham bir datagram geldiğinde, köprü bunu istemciye şu yolla iletir:

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## SAM Yardımcı Program İşlevselliği

Aşağıdaki mesaj, istemci tarafından SAM bridge'den ad çözümlemesi sorgulamak için kullanılabilir:

```
NAMING LOOKUP
       NAME=$name
```
şu şekilde yanıtlanır

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE=$message]
```
RESULT değeri şunlardan biri olabilir:

- `OK`
- `INVALID_KEY`
- `KEY_NOT_FOUND`

Eğer NAME=ME ise, yanıt mevcut oturum tarafından kullanılan hedefi içerecektir (TRANSIENT bir oturum kullanıyorsanız kullanışlıdır). $result OK değilse, MESSAGE "bad format" gibi açıklayıcı bir mesaj taşıyabilir.

$destination, [Destination](/docs/specs/common-structures#type_Destination)'ın base 64 karşılığıdır ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakter (binary olarak 387 veya daha fazla bayt) içerir.

Genel ve özel base64 anahtarları aşağıdaki mesaj kullanılarak oluşturulabilir:

```
DEST GENERATE
```
şu şekilde yanıtlanır

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
I2P 0.9.14 sürümünden itibaren, isteğe bağlı bir SIGNATURE_TYPE parametresi desteklenmektedir. SIGNATURE_TYPE değeri, [Key Certificates](/docs/specs/common-structures#type_Certificate) tarafından desteklenen herhangi bir isim (örn. ECDSA_SHA256_P256, büyük/küçük harf duyarsız) veya sayı (örn. 1) olabilir. Varsayılan değer DSA_SHA1'dir.

$destination, [Destination](/docs/specs/common-structures#type_Destination)'ın base 64 kodlamasıdır ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakterinden (binary olarak 387 veya daha fazla bayt) oluşur.

$privkey, [Destination](/docs/specs/common-structures#type_Destination)'ı takip eden [Private Key](/docs/specs/common-structures#type_PrivateKey)'i takip eden [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey)'in birleştirilmesinin base 64 kodlamasıdır ve imza türüne bağlı olarak 884 veya daha fazla base 64 karakter (ikili formatta 663 veya daha fazla bayt) içerir.

## RESULT Değerleri

Bunlar RESULT alanında taşınabilecek değerler ve anlamlarıdır:

| Değer | Anlamı |
|-------|---------|
| `OK` | İşlem başarıyla tamamlandı |
| `CANT_REACH_PEER` | Peer mevcut, ancak ulaşılamıyor |
| `DUPLICATED_DEST` | Belirtilen Destination zaten kullanımda |
| `I2P_ERROR` | Genel bir I2P hatası (örn. I2CP bağlantısının kesilmesi, vb.) |
| `INVALID_KEY` | Belirtilen anahtar geçerli değil (kötü format, vb.) |
| `KEY_NOT_FOUND` | İsimlendirme sistemi verilen ismi çözümleyemiyor |
| `PEER_NOT_FOUND` | Peer ağda bulunamıyor |
| `TIMEOUT` | Bir olay beklerken zaman aşımı (örn. peer yanıtı) |
## Tunnel, I2CP ve Streaming Seçenekleri

Bu seçenekler, bir SAM SESSION CREATE satırının sonunda name=value çiftleri olarak geçirilebilir.

Tüm oturumlar [tunnel uzunlukları gibi I2CP seçenekleri](/docs/protocol/i2cp#options) içerebilir. STREAM oturumları [Streaming lib seçenekleri](/docs/api/streaming#options) içerebilir. Seçenek isimleri ve varsayılan değerler için bu referanslara bakın.

## Base 64 Notları

Base 64 kodlaması I2P standart Base 64 alfabesini "A-Z, a-z, 0-9, -, ~" kullanmalıdır.

## İstemci Kütüphanesi Uygulamaları

C, C++, C#, Perl ve Python için istemci kütüphaneleri mevcuttur. Bunlar I2P Kaynak Paketi'ndeki apps/sam/ dizininde bulunmaktadır. Bazıları eski olabilir ve SAMv2 desteği için güncellenmemiş olabilir.

## Varsayılan SAM Kurulumu

Varsayılan SAM portu 7656'dır. SAM, I2P Router'da varsayılan olarak etkin değildir; router konsolundaki istemcileri yapılandır sayfasında veya clients.config dosyasında manuel olarak başlatılmalı veya otomatik başlayacak şekilde yapılandırılmalıdır.
