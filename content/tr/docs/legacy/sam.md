---
title: "SAM V1 Belirtimi"
description: "Eski Basit Anonim Mesajlaşma protokolü sürüm 1 (kullanımdan kaldırıldı)"
slug: "sam"
aliases:
  - "/tr/docs/api/sam"
  - "/tr/docs/api/sam/"
  - "/tr/sam"
  - "/tr/sam/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## Uyarı - Kullanımdan Kaldırıldı - Desteklenmiyor - [SAMv3](/docs/api/samv3) Kullanın

Aşağıda I2P ile etkileşim kurmak için basit bir istemci protokolünün 1. sürümü belirtilmiştir. Daha yeni alternatifler: [SAM V2](/docs/api/samv2), [SAM V3](/docs/api/samv3), [BOB](/docs/api/bob).

## SAMv1 API'si için dil kütüphaneleri

- C
- C#
- Perl
- Python

Kütüphaneler I2P kaynak kod deposunda bulunmaktadır.

### I2P 0.9.14 Değişiklikleri

Bildirilen sürüm "1.0" olarak kalır.

- DEST GENERATE artık bir SIGNATURE_TYPE parametresini destekliyor.
- HELLO VERSION'daki MIN parametresi artık isteğe bağlı.
- HELLO VERSION'daki MIN ve MAX parametreleri artık "3" gibi tek haneli sürümleri destekliyor.

## Sürüm 1 Protokolü

İstemci uygulaması, tüm I2P işlevselliğini yöneten SAMv3 köprüsü ile iletişim kurar (sanal akışlar için streaming kütüphanesini veya asenkron mesajlar için doğrudan I2CP kullanarak).

Tüm istemci\<--\>SAM bridge iletişimi tek bir TCP soketi üzerinden şifrelenmemiş ve kimlik doğrulaması yapılmamış şekilde gerçekleşir. SAM bridge erişimi güvenlik duvarları veya diğer yöntemlerle korunmalıdır (bridge hangi IP'lerden bağlantı kabul edeceği konusunda ACL'lere sahip olabilir).

Tüm bu SAM mesajları düz ASCII formatında tek bir satırda gönderilir ve yeni satır karakteri (\\n) ile sonlandırılır. Aşağıda gösterilen biçimlendirme yalnızca okunabilirlik içindir ve her mesajdaki ilk iki kelimenin belirli sıralarını koruması gerekirken, anahtar=değer çiftlerinin sırası değişebilir (örneğin "ONE TWO A=B C=D" veya "ONE TWO C=D A=B" yapıları tamamen geçerlidir). Ayrıca protokol büyük-küçük harf duyarlıdır.

SAM mesajları UTF-8 olarak yorumlanır. Anahtar=değer çiftleri tek bir boşlukla ayrılmalıdır. Değerler boşluk içeriyorsa çift tırnak içine alınabilir, örneğin key="uzun değer metni". Kaçış mekanizması yoktur.

İletişim üç farklı biçim alabilir:

- [Sanal akışlar](/docs/api/streaming)
- [Yanıtlanabilir datagramlar](/docs/specs/datagrams#repliable) (FROM alanı olan mesajlar)
- [Anonim datagramlar](/docs/specs/datagrams#raw) (ham anonim mesajlar)

## SAM Bağlantı El Sıkışması

İstemci ve köprü bir protokol sürümü üzerinde anlaşana kadar hiçbir SAM iletişimi gerçekleşemez, bu da istemcinin bir HELLO göndermesi ve köprünün bir HELLO REPLY göndermesi ile yapılır:

```
HELLO VERSION MIN=$min MAX=$max
```
ve

```
HELLO REPLY RESULT=$result VERSION=1.0
```
I2P 0.9.14 sürümünden itibaren, MIN parametresi isteğe bağlıdır. MAX parametresi sağlanmalı ve sürüm 1'i kullanmak için "1"den büyük veya eşit ve "2"den küçük olmalıdır.

RESULT değeri şunlardan biri olabilir:

- `OK`
- `NOVERSION`

## SAM Oturumları

Bir SAM oturumu, bir istemcinin SAM köprüsüne bir soket açması, bir el sıkışma işlemi gerçekleştirmesi ve bir SESSION CREATE mesajı göndermesi ile oluşturulur ve soket bağlantısı kesildiğinde oturum sonlanır.

Her I2P Destination aynı anda yalnızca bir SAM oturumu için kullanılabilir ve bu formlardan yalnızca birini kullanabilir (diğer formlar aracılığıyla alınan mesajlar düşürülür).

İstemci tarafından köprüye gönderilen SESSION CREATE mesajı aşağıdaki gibidir:

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION, mesaj/stream gönderme ve alma için hangi destination'ın kullanılacağını belirtir. Eğer bir $name verilirse, SAM bridge kendi yerel depolama alanında (sam.keys dosyası) ilişkili bir destination (ve private key) aramak için kontrol eder. Bu isimle eşleşen bir ilişki yoksa, yeni bir tane oluşturur. Destination TRANSIENT olarak belirtilirse, her zaman yeni bir tane oluşturur.

DESTINATION'ın bir tanımlayıcı olduğunu, Base 64 kodlanmış veri *olmadığını* unutmayın. Destination'ı belirtmek için [SAM V3](/docs/api/samv3) kullanmalısınız.

DIRECTION yalnızca STREAM oturumları için belirtilebilir ve köprüye istemcinin stream'leri oluşturacağını, alacağını veya her ikisini birden yapacağını bildirir. Bu belirtilmezse, BOTH varsayılır. DIRECTION=RECEIVE olduğunda giden bir stream oluşturmaya çalışmak bir hataya neden olmalı ve DIRECTION=CREATE olduğunda gelen stream'ler göz ardı edilmelidir.

Verilen ek seçenekler, SAM köprüsü tarafından yorumlanmadığı takdirde I2P oturum yapılandırmasına aktarılmalıdır (örneğin "tunnels.depthInbound=0"). Bu seçenekler aşağıda belgelenmiştir.

SAM bridge'in kendisi zaten I2P üzerinden hangi router ile iletişim kurması gerektiği konusunda yapılandırılmış olmalıdır (gerekirse bir geçersiz kılma yolu olabilir, örneğin i2cp.tcp.host=localhost ve i2cp.tcp.port=7654).

Session oluşturma mesajını aldıktan sonra, SAM köprüsü aşağıdaki gibi bir session durumu mesajı ile yanıt verecektir:

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

Eğer uygun değilse, MESSAGE oturum neden oluşturulamadığına dair insan tarafından okunabilir bilgi içermelidir.

$name bulunamadığında ve bunun yerine geçici bir hedef oluşturulduğunda herhangi bir uyarı verilmediğini unutmayın. Gerçek geçici base 64 hedefinin yanıtta çıktı olarak verilmediğini unutmayın; SESSION CREATE'de sağlanan $name veya TRANSIENT'tir. Bu özelliklere ihtiyacınız varsa, [SAM V3](/docs/api/samv3) kullanmalısınız.

## SAM Sanal Akışları

Sanal akışların güvenilir bir şekilde ve sırayla gönderileceği garanti edilir, başarısızlık ve başarı bildirimleri mevcut olur olmaz sunulur.

STYLE=STREAM ile oturum kurduktan sonra, hem istemci hem de SAM köprüsü, aşağıda listelenen akışları yönetmek için çeşitli mesajları eşzamansız olarak ileri geri gönderebilir:

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
Bu, yerel hedeften belirtilen eşe yeni bir sanal bağlantı kurar ve onu oturum kapsamlı benzersiz ID ile işaretler. Benzersiz ID, 1'den (2^31-1)'e kadar olan ASCII tabanlı 10'luk tam sayıdır.

$destination, [Destination](/docs/specs/common-structures#type_Destination)'ın base 64 halidir ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakter (binary olarak 387 veya daha fazla bayt) içerir.

SAM bridge buna bir stream durum mesajı ile yanıt vermelidir:

```
STREAM STATUS
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
RESULT değeri aşağıdakilerden biri olabilir:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `INVALID_KEY`
- `TIMEOUT`

RESULT OK ise, belirtilen hedef aktiftir ve bağlantıyı yetkilendirmiştir; bağlantı mümkün değilse (zaman aşımı, vb.), RESULT uygun hata değerini içerecektir (isteğe bağlı insan tarafından okunabilir bir MESSAGE ile birlikte).

Alıcı tarafta, SAM köprüsü istemciyi şu şekilde basitçe bilgilendirir:

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
Bu, istemciye verilen hedefin kendileriyle sanal bir bağlantı oluşturduğunu bildirir. Takip eden veri akışı, -1'den -(2^31-1)'e kadar ASCII base 10 tamsayısı olan verilen benzersiz ID ile işaretlenecektir.

$destination, [Destination](/docs/specs/common-structures#type_Destination)'ın base 64 kodlamasıdır ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakter (binary olarak 387 veya daha fazla bayt) içerir.

İstemci sanal bağlantı üzerinden veri göndermek istediğinde, bunu şu şekilde yapar:

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Bu, sanal bağlantı üzerinden eş düğüme gönderilen tampon belleğe belirtilen veriyi ekler. Gönderme boyutu $numBytes, yeni satır karakterinden sonra dahil edilen 8 bit bayt sayısıdır ve 1 ile 32768 (32KB) arasında olabilir.

SAM bridge daha sonra mesajı mümkün olduğunca hızlı ve verimli bir şekilde iletmek için elinden geleni yapacak, belki de birden fazla SEND mesajını birlikte tamponlayacaktır. Verileri iletmede bir hata olursa veya uzak taraf bağlantıyı kapatırsa, SAM bridge istemciye şunu söyleyecektir:

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

Bağlantı diğer peer tarafından temiz bir şekilde kapatıldıysa, $result OK olarak ayarlanır. Eğer $result OK değilse, MESSAGE "peer ulaşılamıyor" gibi açıklayıcı bir mesaj taşıyabilir. Bir istemci bağlantıyı kapatmak istediğinde, SAM bridge'e kapatma mesajını gönderir:

```
STREAM CLOSE
       ID=$id
```
Bridge daha sonra gerekli temizlik işlemlerini yapar ve bu ID'yi siler - artık bu ID üzerinden herhangi bir mesaj gönderilemez veya alınamaz.

İletişimin diğer tarafı için, peer veri gönderdiğinde ve bu veri istemci için kullanılabilir hale geldiğinde, SAM köprüsü bunu derhal teslim edecektir:

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Tüm akışlar, SAM bridge ile istemci arasındaki bağlantının kesilmesiyle örtük olarak kapatılır.

## SAM Yanıtlanabilir Veri Paketleri

I2P doğal olarak bir FROM adresi içermese de, kullanım kolaylığı için yanıtlanabilir datagramlar olarak ek bir katman sağlanır - FROM adresini içeren (başlık materyali için 1KB'ye kadar yer bırakan) 31744 bayta kadar sırasız ve güvenilmez mesajlar. Bu FROM adresi SAM tarafından dahili olarak doğrulanır (kaynağı doğrulamak için destination'ın imzalama anahtarını kullanarak) ve tekrar oynatma koruması içerir.

Minimum boyut 1'dir. En iyi teslimat güvenilirliği için önerilen maksimum boyut yaklaşık 11 KB'dır.

STYLE=DATAGRAM ile bir SAM oturumu kurduktan sonra, istemci SAM köprüsüne gönderebilir:

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
$destination, signature türüne bağlı olarak 516 veya daha fazla base 64 karakter (binary olarak 387 veya daha fazla bayt) olan [Destination](/docs/specs/common-structures#type_Destination)'ın base 64 halidir.

SAM köprüsü, istemciye asla kimlik doğrulama başlıklarını veya diğer alanları sunmaz, yalnızca gönderenin sağladığı verileri iletir. Bu, oturum kapanana kadar (istemci bağlantıyı düşürene kadar) devam eder.

## SAM Anonim Datagramları

I2P'nin bant genişliğinden maksimum verim elde etmek için SAM, istemcilerin anonim datagram'lar göndermesine ve almasına izin verir, kimlik doğrulama ve yanıt bilgilerini istemcinin kendisine bırakır. Bu datagram'lar güvenilmez ve sırasızdır ve 32768 bayta kadar olabilir.

Minimum boyut 1'dir. En iyi teslimat güvenilirliği için, önerilen maksimum boyut yaklaşık 11 KB'dir.

STYLE=RAW ile bir SAM oturumu kurduktan sonra, istemci SAM bridge'ine şunları gönderebilir:

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
$destination, [Destination](/docs/specs/common-structures#type_Destination)'ın base 64 kodlamasıdır ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakter (binary olarak 387 veya daha fazla bayt) içerir.

Ham bir datagram geldiğinde, köprü bunu istemciye şu yolla teslim eder:

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## SAM Yardımcı Program İşlevselliği

Aşağıdaki mesaj, istemci tarafından SAM bridge'den ad çözümlemesi sorgusu yapmak için kullanılabilir:

```
NAMING LOOKUP
       NAME=$name
```
yanıtı ise şu şekildedir

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

Eğer NAME=ME ise, yanıt mevcut oturum tarafından kullanılan hedefi içerecektir (TRANSIENT bir oturum kullanıyorsanız yararlıdır). Eğer $result OK değilse, MESSAGE "kötü format" gibi açıklayıcı bir mesaj iletebilir.

$destination, [Destination](/docs/specs/common-structures#type_Destination)'ın base 64 kodlamasıdır ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakter (binary olarak 387 veya daha fazla byte) içerir.

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
I2P 0.9.14 sürümünden itibaren, isteğe bağlı bir SIGNATURE_TYPE parametresi desteklenmektedir. SIGNATURE_TYPE değeri, [Key Certificates](/docs/specs/common-structures#type_Certificate) tarafından desteklenen herhangi bir isim (örn. ECDSA_SHA256_P256, büyük/küçük harf duyarsız) veya numara (örn. 1) olabilir. Varsayılan değer DSA_SHA1'dir.

$destination, signature türüne bağlı olarak 516 veya daha fazla base 64 karakter (binary formatında 387 veya daha fazla byte) olan [Destination](/docs/specs/common-structures#type_Destination)'ın base 64 halidir.

$privkey, [Destination](/docs/specs/common-structures#type_Destination)'ın ardından [Private Key](/docs/specs/common-structures#type_PrivateKey)'in ardından [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey)'in birleştirilmesinin base 64'üdür ve imza türüne bağlı olarak 884 veya daha fazla base 64 karakter (ikili formatta 663 veya daha fazla bayt) içerir.

## RESULT Değerleri

Bunlar RESULT alanının taşıyabileceği değerler ve anlamları:

| Değer | Anlamı |
|-------|---------|
| `OK` | İşlem başarıyla tamamlandı |
| `CANT_REACH_PEER` | Peer mevcut, ancak ulaşılamıyor |
| `DUPLICATED_DEST` | Belirtilen Destination zaten kullanımda |
| `I2P_ERROR` | Genel bir I2P hatası (ör. I2CP bağlantı kesintisi, vb.) |
| `INVALID_KEY` | Belirtilen anahtar geçerli değil (hatalı format, vb.) |
| `KEY_NOT_FOUND` | İsimlendirme sistemi verilen ismi çözümleyemiyor |
| `PEER_NOT_FOUND` | Peer ağda bulunamıyor |
| `TIMEOUT` | Bir olayı beklerken zaman aşımı (ör. peer yanıtı) |
## Tunnel, I2CP ve Streaming Seçenekleri

Bu seçenekler, SAM SESSION CREATE satırının sonunda name=value çiftleri olarak geçirilebilir.

Tüm oturumlar [tunnel uzunlukları gibi I2CP seçenekleri](/docs/protocol/i2cp#options) içerebilir. STREAM oturumları [Streaming lib seçenekleri](/docs/api/streaming#options) içerebilir. Seçenek adları ve varsayılan değerler için bu referanslara bakın.

## Base 64 Notları

Base 64 kodlaması I2P standart Base 64 alfabesini "A-Z, a-z, 0-9, -, ~" kullanmalıdır.

## İstemci Kütüphanesi Uygulamaları

C, C++, C#, Perl ve Python için istemci kütüphaneleri mevcuttur. Bunlar I2P Kaynak Paketindeki apps/sam/ dizininde bulunmaktadır.

## Varsayılan SAM Kurulumu

Varsayılan SAM portu 7656'dır. SAM, I2P Router'da varsayılan olarak etkin değildir; router konsolundaki istemcileri yapılandır sayfasında veya clients.config dosyasında manuel olarak başlatılmalı veya otomatik başlaması için yapılandırılmalıdır.
