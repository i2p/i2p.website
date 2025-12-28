---
title: "ECIES Tunnels"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Kapalı"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
toc: true
---

## Not

Ağ dağıtımı ve testler sürüyor. Küçük düzeltmeler yapılabilir. Resmî belirtim için [SPEC](/docs/specs/implementation/)'e bakın.

## Genel Bakış

Bu belge, [ECIES-X25519](/docs/specs/ecies/) tarafından tanıtılan kriptografik ilkelleri kullanarak Tunnel Build (tunnel kurulumu) mesajı şifrelemesinde değişiklikler önerir. Bu, router'ların ElGamal'dan ECIES-X25519 anahtarlarına dönüştürülmesine yönelik genel öneri [Proposal 156](/proposals/156-ecies-routers) kapsamında yer alan bir bölümdür.

Ağın ElGamal + AES256'tan ECIES + ChaCha20'ye geçişi amacıyla, ElGamal ve ECIES router'larının karışık olduğu tunnel'lar gereklidir. Karışık tunnel atlamalarının işlenmesine ilişkin spesifikasyonlar sağlanmıştır. ElGamal atlamalarının biçimi, işlenmesi veya şifrelemesinde herhangi bir değişiklik yapılmayacaktır.

ElGamal tunnel oluşturucularının, her atlama için geçici X25519 anahtar çiftleri oluşturmaları ve ECIES atlamaları içeren tunnel'lar oluşturmak için bu belirtimi izlemeleri gerekir.

Bu öneri, ECIES-X25519 Tunnel Oluşturma için gerekli değişiklikleri belirtir. ECIES routers için gerekli tüm değişikliklerin genel bir özeti için bkz. Öneri 156 [Öneri 156](/proposals/156-ecies-routers).

Bu öneri, uyumluluk gereği, tunnel oluşturma kayıtlarının boyutunu aynı tutar. Daha küçük oluşturma kayıtları ve mesajlar daha sonra uygulanacaktır - bkz. [Öneri 157](/proposals/157-new-tbm).

### Kriptografik İlkeller

Yeni bir kriptografik ilkel tanıtılmamaktadır. Bu öneriyi uygulamak için gerekli ilkeller şunlardır:

- AES-256-CBC, [Cryptography](/docs/specs/cryptography/) belgesindeki gibi
- STREAM ChaCha20/Poly1305 fonksiyonları:
  ENCRYPT(k, n, plaintext, ad) ve DECRYPT(k, n, ciphertext, ad) - [NTCP2](/docs/specs/ntcp2/) [ECIES-X25519](/docs/specs/ecies/) ve [RFC-7539](https://tools.ietf.org/html/rfc7539) belgelerindeki gibi
- X25519 DH fonksiyonları - [NTCP2](/docs/specs/ntcp2/) ve [ECIES-X25519](/docs/specs/ecies/) belgelerindeki gibi
- HKDF(salt, ikm, info, n) - [NTCP2](/docs/specs/ntcp2/) ve [ECIES-X25519](/docs/specs/ecies/) belgelerindeki gibi

Başka yerlerde tanımlanan diğer Noise (kriptografik el sıkışma protokolü) işlevleri:

- MixHash(d) - [NTCP2](/docs/specs/ntcp2/) ve [ECIES-X25519](/docs/specs/ecies/)'de olduğu gibi
- MixKey(d) - [NTCP2](/docs/specs/ntcp2/) ve [ECIES-X25519](/docs/specs/ecies/)'de olduğu gibi

### Hedefler


### Amaçlanmayanlar

- Bir "flag day" (eşgüdümlü, aynı anda yapılan zorunlu geçiş) gerektiren tunnel kurulum mesajlarının tamamen yeniden tasarlanması.
- tunnel kurulum mesajlarının küçültülmesi (tüm atlamaların ECIES olması ve yeni bir öneri gerektirir)
- [Proposal 143](/proposals/143-build-message-options)'te tanımlandığı üzere tunnel kurulum seçeneklerinin kullanımı, yalnızca küçük mesajlar için gereklidir
- Çift yönlü tunnel'lar - bunun için bkz. [Proposal 119](/proposals/119-bidirectional-tunnels)
- Daha küçük tunnel kurulum mesajları - bunun için bkz. [Proposal 157](/proposals/157-new-tbm)

## Tehdit Modeli

### Tasarım Hedefleri

- Hiçbir atlama, tunnel'in başlatıcısını tespit edemez.

- Ara atlamalar, tunnel'in yönünü
  ya da tunnel içindeki konumlarını belirleyememelidir.

- Hiçbir atlama, diğer istek veya yanıt kayıtlarının herhangi bir içeriğini okuyamaz, hariç
  bir sonraki atlama için kısaltılmış router hash ve geçici anahtar

- Giden tunnel oluşturma için kullanılan reply tunnel'in hiçbir üyesi herhangi bir yanıt kaydını okuyamaz.

- Gelen oluşturma (inbound build) için kullanılan outbound tunnel'ın hiçbir üyesi,
  OBEP (Outbound Endpoint)'in IBGW (Inbound Gateway) için kısaltılmış router karma değerini ve geçici anahtarı görebilmesi istisnası dışında, herhangi bir istek kaydını okuyamaz

### Etiketleme Saldırıları

Tunnel oluşturma tasarımının başlıca hedeflerinden biri, işbirliği yapan router X ve Y'nin tek bir tunnel içinde olduklarını bilmelerini zorlaştırmaktır. Eğer router X m. atlamada ve router Y m+1. atlamadaysa, bunu elbette bileceklerdir. Ancak router X m. atlamada ve router Y m+n. atlamadaysa (n>1), bunu bilmeleri çok daha zor olmalıdır.

Etiketleme saldırıları, orta atlama router X'in, tunnel oluşturma mesajını, bu mesaj router Y'ye ulaştığında router Y'nin değişikliği saptayabileceği biçimde değiştirmesine dayanır. Amaç, değiştirilen her mesajın, router Y'ye ulaşmadan önce X ile Y arasındaki bir router tarafından düşürülmesidir. Router Y'den önce düşürülmeyen değişiklikler için, tunnel oluşturucusu yanıttaki bozulmayı algılamalı ve tunnel'ı atmalıdır.

Olası saldırılar:

- Bir derleme kaydını düzenle
- Bir derleme kaydını değiştir
- Bir derleme kaydı ekle veya kaldır
- Derleme kayıtlarını yeniden sırala

TODO: Mevcut tasarım tüm bu saldırıları önlüyor mu?

## Tasarım

### Noise Protokol Çerçevesi

Bu öneri, Noise Protocol Framework (Noise Protokol Çatısı) [NOISE](https://noiseprotocol.org/noise.html) (Revizyon 34, 2018-07-11) temel alınarak gereksinimleri tanımlar. Noise terminolojisinde, Alice başlatan, Bob ise yanıtlayandır.

Bu öneri, Noise protokolü Noise_N_25519_ChaChaPoly_SHA256 üzerine dayanmaktadır. Bu Noise protokolü aşağıdaki kriptografik ilkeleri kullanır:

- Tek Yönlü El Sıkışma Deseni: N
  Alice, statik anahtarını Bob'a iletmez (N)

- DH Fonksiyonu (Diffie-Hellman): X25519
  X25519 DH, [RFC-7748](https://tools.ietf.org/html/rfc7748) belgesinde belirtildiği gibi 32 bayt anahtar uzunluğuna sahiptir.

- Şifreleme İşlevi: ChaChaPoly
  AEAD_CHACHA20_POLY1305, [RFC-7539](https://tools.ietf.org/html/rfc7539) bölüm 2.8'de belirtildiği gibi.
  12 baytlık nonce (tek kullanımlık sayı), ilk 4 baytı sıfıra ayarlanmış.
  [NTCP2](/docs/specs/ntcp2/) içindekiyle aynıdır.

- Özet Fonksiyonu: SHA256
  Standart 32 baytlık özet, I2P'de halihazırda yaygın olarak kullanılıyor.

#### Çerçeveye eklemeler

Hiçbiri.

### El Sıkışma Kalıpları

El sıkışma işlemleri [Noise](https://noiseprotocol.org/noise.html) el sıkışma desenlerini kullanır.

Aşağıdaki harf eşlemesi kullanılır:

- e = tek kullanımlık geçici anahtar
- s = statik anahtar
- p = mesaj yükü

Oluşturma isteği, Noise N pattern (Noise N deseni) ile özdeştir. Bu ayrıca [NTCP2](/docs/specs/ntcp2/) içinde kullanılan XK pattern (XK deseni) içindeki ilk (Session Request - Oturum İsteği) iletiyle de özdeştir.

```text
<- s
  ...
  e es p ->
```
### İstek şifrelemesi

Build request kayıtları, tunnel oluşturucusu tarafından oluşturulur ve her bir atlama için asimetrik olarak şifrelenir. Bu istek kayıtlarının asimetrik şifrelemesi, şu anda [Cryptography](/docs/specs/cryptography/) bölümünde tanımlandığı üzere ElGamal'dır ve bir SHA-256 sağlama toplamı içerir. Bu tasarım ileri gizlilik sağlamaz.

Yeni tasarım, ileri gizlilik, bütünlük ve kimlik doğrulama için ECIES-X25519 ephemeral-static DH ile tek yönlü Noise deseni "N", bir HKDF ve ChaCha20/Poly1305 AEAD kullanacaktır. Alice, tunnel oluşturma isteğinde bulunan taraftır. tunnel içindeki her atlama noktası bir Bob'dur.

(Yük Güvenlik Özellikleri)

```text
N:                      Authentication   Confidentiality
    -> e, es                  0                2

    Authentication: None (0).
    This payload may have been sent by any party, including an active attacker.

    Confidentiality: 2.
    Encryption to a known recipient, forward secrecy for sender compromise
    only, vulnerable to replay.  This payload is encrypted based only on DHs
    involving the recipient's static key pair.  If the recipient's static
    private key is compromised, even at a later date, this payload can be
    decrypted.  This message can also be replayed, since there's no ephemeral
    contribution from the recipient.

    "e": Alice generates a new ephemeral key pair and stores it in the e
         variable, writes the ephemeral public key as cleartext into the
         message buffer, and hashes the public key along with the old h to
         derive a new h.

    "es": A DH is performed between the Alice's ephemeral key pair and the
          Bob's static key pair.  The result is hashed along with the old ck to
          derive a new ck and k, and n is set to zero.
```
### Yanıt şifreleme

Oluşturma yanıt kayıtları, atlamanın (hop) oluşturucusu tarafından oluşturulur ve oluşturucuya simetrik olarak şifrelenir. Bu yanıt kayıtlarının simetrik şifrelemesi, şu anda başına eklenmiş bir SHA-256 sağlama toplamıyla birlikte AES kullanır. Bu tasarım ileri gizlilik (forward secrecy) sağlamaz.

Yeni tasarım, bütünlük ve kimlik doğrulama için ChaCha20/Poly1305 AEAD (Authenticated Encryption with Associated Data — ilişkili verili kimlik doğrulamalı şifreleme) kullanacak.

### Gerekçe

İstekteki geçici açık anahtarın AES veya Elligator2 ile gizlenmesine gerek yoktur. Bunu yalnızca bir önceki atlama görebilir ve o atlama bir sonraki atlamanın ECIES kullandığını bilir.

Yanıt kayıtları, başka bir DH (Diffie-Hellman anahtar değişimi) ile tam kapsamlı asimetrik şifreleme gerektirmez.

## Spesifikasyon

### Oluşturma İsteği Kayıtları

Uyumluluk amacıyla, Encrypted BuildRequestRecords (şifrelenmiş oluşturma isteği kayıtları) hem ElGamal hem de ECIES için 528 bayttır.

#### Şifrelenmemiş İstek Kaydı (ElGamal)

Referans olması açısından, bu, ElGamal router'lar için tunnel BuildRequestRecord'un [I2NP](/docs/specs/i2np/)'ten alınmış güncel belirtimidir. Şifrelenmeden önce, [Kriptografi](/docs/specs/cryptography/)'de tanımlandığı gibi, şifrelenmemiş verinin başına sıfır olmayan bir bayt ve verinin SHA-256 özeti eklenir.

Tüm alanlar big-endian (yüksek anlamlı bayt önce) düzenindedir.

Şifrelenmemiş boyut: 222 bayt

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes    4-35: local router identity hash
  bytes   36-39: next tunnel ID, nonzero
  bytes   40-71: next router identity hash
  bytes  72-103: AES-256 tunnel layer key
  bytes 104-135: AES-256 tunnel IV key
  bytes 136-167: AES-256 reply key
  bytes 168-183: AES-256 reply IV
  byte      184: flags
  bytes 185-188: request time (in hours since the epoch, rounded down)
  bytes 189-192: next message ID
  bytes 193-221: uninterpreted / random padding
```
#### Şifrelenmiş İstek Kaydı (ElGamal)

Referans olması için, bu metin [I2NP](/docs/specs/i2np/) belgesinden alınmış ElGamal routers için tunnel BuildRequestRecord'un güncel belirtimidir.

Şifrelenmiş boyut: 528 bayt

```text
bytes    0-15: Hop's truncated identity hash
  bytes  16-528: ElGamal encrypted BuildRequestRecord
```
#### İstek Kaydı Şifrelenmemiş (ECIES - Eliptik Eğri Entegre Şifreleme Şeması)

Bu, ECIES-X25519 routers için tunnel BuildRequestRecord (tunnel oluşturma isteği kaydı) için önerilen spesifikasyondur. Değişikliklerin özeti:

- Kullanılmayan 32 baytlık router hash'ini kaldır
- İstek zamanını saatlerden dakikalara değiştir
- İleride değişken tunnel süresi için bir sona erme alanı ekle
- Bayraklar için daha fazla alan ekle
- Ek derleme seçenekleri için Eşleme ekle
- Atlamanın kendi yanıt kaydı için AES-256 yanıt anahtarı ve IV (başlatma vektörü) kullanılmaz
- Şifrelenmemiş kayıt, şifreleme ek yükü daha az olduğu için daha uzundur

İstek kaydı hiçbir ChaCha yanıt anahtarı içermez. Bu anahtarlar bir KDF'den (anahtar türetme fonksiyonu) türetilir. Aşağıya bakın.

Tüm alanlar big-endian bayt sıralamasındadır (en anlamlı bayt önce).

Şifrelenmemiş boyut: 464 bayt

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes     4-7: next tunnel ID, nonzero
  bytes    8-39: next router identity hash
  bytes   40-71: AES-256 tunnel layer key
  bytes  72-103: AES-256 tunnel IV key
  bytes 104-135: AES-256 reply key
  bytes 136-151: AES-256 reply IV
  byte      152: flags
  bytes 153-155: more flags, unused, set to 0 for compatibility
  bytes 156-159: request time (in minutes since the epoch, rounded down)
  bytes 160-163: request expiration (in seconds since creation)
  bytes 164-167: next message ID
  bytes   168-x: tunnel build options (Mapping)
  bytes     x-x: other data as implied by flags or options
  bytes   x-463: random padding
```
Bayraklar alanı, [Tunnel Creation](/docs/specs/implementation/) bölümünde tanımlananla aynıdır ve aşağıdakileri içerir::

Bit sırası: 76543210 (bit 7 MSB'dir (en anlamlı bit))  bit 7: ayarlıysa, herhangi birinden gelen mesajlara izin ver  bit 6: ayarlıysa, herkese mesaj gönderimine izin ver ve yanıtı şuna gönder

        specified next hop in a Tunnel Build Reply Message
bitler 5-0: Tanımsız, gelecekteki seçeneklerle uyumluluk için 0 olarak ayarlanmalıdır

7. bit, atlamanın bir gelen ağ geçidi (IBGW) olacağını belirtir. 6. bit, atlamanın bir giden uç nokta (OBEP) olacağını belirtir. Her iki bit de ayarlanmadıysa, atlama ara katılımcı olacaktır. İkisi birden aynı anda ayarlanamaz.

İstek zaman aşımı, ileride değişken tunnel sürelerini desteklemek içindir. Şimdilik desteklenen tek değer 600'dür (10 dakika).

tunnel oluşturma seçenekleri, [Common Structures](/docs/specs/common-structures/) bölümünde tanımlandığı gibi bir Mapping yapısıdır (eşleme yapısı). Bu, gelecekte kullanım içindir. Şu anda tanımlı herhangi bir seçenek yoktur. Mapping yapısı boşsa, bu iki bayttır: 0x00 0x00. Mapping'in azami boyutu (uzunluk alanı dahil) 296 bayttır ve Mapping uzunluk alanının alabileceği en yüksek değer 294'tür.

#### Şifrelenmiş İstek Kaydı (ECIES)

Tüm alanlar big-endian (büyük uçlu bayt sıralaması) olup, bunun istisnası little-endian (küçük uçlu bayt sıralaması) olan geçici açık anahtardır.

Şifrelenmiş boyut: 528 bayt

```text
bytes    0-15: Hop's truncated identity hash
  bytes   16-47: Sender's ephemeral X25519 public key
  bytes  48-511: ChaCha20 encrypted BuildRequestRecord
  bytes 512-527: Poly1305 MAC
```
### Oluşturma Yanıt Kayıtları

Uyumluluk amacıyla, şifrelenmiş BuildReplyRecords (tünel oluşturma yanıt kayıtları) hem ElGamal hem de ECIES için 528 bayttır.

#### Şifrelenmemiş Yanıt Kaydı (ElGamal)

ElGamal (açık anahtarlı şifreleme algoritması) yanıtları AES (simetrik şifreleme standardı) ile şifrelenir.

Tüm alanlar big-endian biçimindedir (en anlamlı baytın önce geldiği bayt sıralaması).

Şifrelenmemiş boyut: 528 bayt

```text
bytes   0-31: SHA-256 Hash of bytes 32-527
  bytes 32-526: random data
  byte     527: reply

  total length: 528
```
#### Şifrelenmemiş Yanıt Kaydı (ECIES - Eliptik Eğri Bütünleşik Şifreleme Şeması)

Bu, ECIES-X25519 router'lar için tunnel BuildReplyRecord'un önerilen belirtimidir. Değişikliklerin özeti:

- build reply options (build yanıt seçenekleri) için Mapping ekle
- Şifrelenmemiş kayıt, daha az şifreleme ek yükü olduğu için daha uzundur

ECIES (Eliptik Eğri Entegre Şifreleme Şeması) yanıtları ChaCha20/Poly1305 ile şifrelenir.

Tüm alanlar big-endian'dır (en anlamlı bayt önce).

Şifrelenmemiş boyut: 512 bayt

```text
bytes    0-x: Tunnel Build Reply Options (Mapping)
  bytes    x-x: other data as implied by options
  bytes  x-510: Random padding
  byte     511: Reply byte
```
tunnel oluşturma yanıtı seçenekleri, [Ortak Yapılar](/docs/specs/common-structures/) bölümünde tanımlandığı gibi bir Mapping (eşleme) yapısıdır. Bu, gelecekte kullanım içindir. Şu anda herhangi bir seçenek tanımlı değildir. Mapping yapısı boşsa, bu iki bayttır: 0x00 0x00. Mapping'in (uzunluk alanı dahil) azami boyutu 511 bayttır ve Mapping uzunluk alanının alabileceği azami değer 509'dur.

Yanıt baytı, parmak izi çıkarımını önlemek için [Tunnel Creation](/docs/specs/implementation/)'da tanımlandığı üzere aşağıdaki değerlerden biridir:

- 0x00 (kabul)
- 30 (TUNNEL_REJECT_BANDWIDTH - bant genişliği nedeniyle reddedildi)

#### Yanıt Kaydı Şifreli (ECIES - Eliptik Eğri Tabanlı Entegre Şifreleme Şeması)

Şifrelenmiş boyut: 528 bayt

```text
bytes   0-511: ChaCha20 encrypted BuildReplyRecord
  bytes 512-527: Poly1305 MAC
```
ECIES (Eliptik Eğri Entegre Şifreleme Şeması) kayıtlarına tam geçişten sonra, aralıklandırılmış dolgu kuralları, istek kayıtları için olanlarla aynıdır.

### Kayıtların simetrik olarak şifrelenmesi

Karma tunnels kullanımı, ElGamal'dan ECIES'e geçiş için hem izinli hem de gereklidir. Geçiş dönemi boyunca, giderek daha fazla router ECIES anahtarlarıyla yapılandırılacaktır.

Simetrik şifreleme için ön işleme aynı şekilde çalışacaktır:

- "encryption":

- şifreleme algoritması şifre çözme modunda çalıştırılır
  - istek kayıtlarının şifresi ön işleme aşamasında önceden çözülür (şifreli istek kayıtlarını gizleyerek)

- "şifre çözme":

- şifreleme modunda çalışan şifreleme algoritması
  - istek kayıtları, katılımcı atlamalar tarafından şifrelenir (bir sonraki açık metin istek kaydını ortaya çıkararak)

- ChaCha20'nun "çalışma kipleri" yoktur, bu nedenle yalnızca üç kez çalıştırılır:

- ön işleme sırasında bir kez
  - her atlamada bir kez
  - nihai yanıtın işlenmesi sırasında bir kez

Karma tunnel'lar kullanıldığında, tunnel oluşturucularının BuildRequestRecord için kullanılan simetrik şifrelemeyi mevcut ve önceki atlamanın şifreleme türüne dayandırmaları gerekecektir.

Her atlama, BuildReplyRecords (inşa yanıt kayıtları) ile VariableTunnelBuildMessage (VTBM) (değişken tünel inşa mesajı) içindeki diğer kayıtları şifrelemek için kendi şifreleme türünü kullanacaktır.

Yanıt yolunda, uç nokta (gönderici), her atlamanın yanıt anahtarını kullanarak [Multiple Encryption](https://en.wikipedia.org/wiki/Multiple_encryption) katmanlarını çözmek zorundadır.

Açıklayıcı bir örnek olarak, ElGamal (genel anahtarlı şifreleme algoritması) ile sarmalanmış ECIES (Eliptik Eğri Tümleşik Şifreleme Şeması) kullanan bir giden tunnel örneğine bakalım:

- Gönderici (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Tüm BuildRequestRecords (oluşturma isteği kayıtları) şifrelenmiş durumdadır (ElGamal veya ECIES kullanılarak).

AES256/CBC şifrelemesi, kullanıldığında, yine her kayıt için ayrı ayrı kullanılır; birden fazla kayıt arasında zincirleme yapılmaz.

Benzer şekilde, ChaCha20 her bir kaydı şifrelemek için kullanılacak, tüm VTBM boyunca akış halinde değil.

İstek kayıtları Gönderici (OBGW) tarafından ön işlemden geçirilir:

- H3'nin kaydı, aşağıdakiler kullanılarak "şifrelenir":

- H2'nin yanıt anahtarı (ChaCha20)
  - H1'in yanıt anahtarı (AES256/CBC)

- H2'nin kaydı şu kullanılarak "şifrelenir":

- H1'in yanıt anahtarı (AES256/CBC)

- H1'in kaydı simetrik şifreleme olmadan gönderilir

Yalnızca H2 yanıt şifreleme bayrağını kontrol eder ve devamında AES256/CBC olduğunu görür.

Her bir atlama tarafından işlemden geçirildikten sonra, kayıtlar "şifresi çözülmüş" durumdadır:

- H3'ün kaydı, şu kullanılarak "şifresi çözülür":

- H3 için yanıt anahtarı (AES256/CBC)

- H2'nin kaydı şu kullanılarak "deşifre edilir":

- H3'ün yanıt anahtarı (AES256/CBC)
  - H2'nin yanıt anahtarı (ChaCha20-Poly1305)

- H1'in kaydı, şunlar kullanılarak "şifresi çözülür":

- H3'ün yanıt anahtarı (AES256/CBC)
  - H2'nin yanıt anahtarı (ChaCha20)
  - H1'in yanıt anahtarı (AES256/CBC)

Tunnel oluşturucusu, diğer adıyla Inbound Endpoint (IBEP) (gelen uç noktası), yanıtı son işlemden geçirir:

- H3'nin kaydı, şunlar kullanılarak "şifrelenmiş"tir:

- H3'nin yanıt anahtarı (AES256/CBC)

- H2'nin kaydı aşağıdakiler kullanılarak "şifrelenir":

- H3'ün yanıt anahtarı (AES256/CBC)
  - H2'nin yanıt anahtarı (ChaCha20-Poly1305)

- H1'in kaydı şu kullanılarak "şifrelenir":

- H3'ün yanıt anahtarı (AES256/CBC)
  - H2'nin yanıt anahtarı (ChaCha20)
  - H1'in yanıt anahtarı (AES256/CBC)

### İstek Kaydı Anahtarları (ECIES)

Bu anahtarlar, ElGamal BuildRequestRecords (tunnel oluşturma isteği kayıtları) içinde açıkça yer alır. ECIES BuildRequestRecords için, tunnel anahtarları ve AES yanıt anahtarları dahil edilir, ancak ChaCha yanıt anahtarları DH değişiminden türetilir. router’ın statik ECIES anahtarlarına ilişkin ayrıntılar için [Proposal 156](/proposals/156-ecies-routers) belgesine bakın.

Aşağıda, istek kayıtlarında daha önce iletilen anahtarların nasıl türetileceğine dair bir açıklama yer almaktadır.

#### Başlangıç ck ve h için KDF (anahtar türetme fonksiyonu)

Bu, desen "N" için, standart bir protokol adıyla kullanılan standart [NOISE](https://noiseprotocol.org/noise.html) uygulamasıdır.

```text
This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  // Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
  h = protocol_name || 0

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by all routers.
```
#### İstek Kaydı için KDF

ElGamal tunnel oluşturucuları, tunnel içindeki her ECIES hop (geçiş noktası) için geçici bir X25519 anahtar çifti oluşturur ve BuildRequestRecord verilerini şifrelemek için yukarıdaki yöntemi kullanır. ElGamal tunnel oluşturucuları, ElGamal hoplara şifreleme yaparken bu spesifikasyondan önceki yöntemi kullanacaktır.

ECIES tunnel oluşturucularının, [Tunnel Creation](/docs/specs/implementation/) bölümünde tanımlanan şemayı kullanarak her bir ElGamal hop (atlama) genel anahtarına şifreleme yapmaları gerekecektir. ECIES tunnel oluşturucuları, ECIES hop'lara şifreleme yapmak için yukarıdaki şemayı kullanacaktır.

Bu, tunnel üzerindeki ara düğümlerin yalnızca kendi şifreleme türleriyle şifrelenmiş kayıtları göreceği anlamına gelir.

ElGamal ve ECIES tunnel oluşturucuları, ECIES atlamalarına şifreli olarak iletmek için her atlama başına benzersiz ve geçici X25519 anahtar çiftleri oluşturacaklardır.

**ÖNEMLİ**: Geçici anahtarlar, her ECIES atlaması ve her oluşturma kaydı için benzersiz olmalıdır. Benzersiz anahtarlar kullanmamak, işbirliği yapan atlamaların aynı tunnel içinde olduklarını doğrulamalarına olanak tanıyan bir saldırı vektörü açar.

```text
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || below means append
  h = SHA256(h || hepk);

  // up until here, can all be precalculated by each router
  // for all incoming build requests

  // Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  // Sender performs an X25519 DH with Hop's static public key.
  // Each Hop, finds the record w/ their truncated identity hash,
  // and extracts the Sender's ephemeral key preceding the encrypted record.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Save for Reply Record KDF
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  plaintext = 464 byte build request record
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  End of "es" message pattern.

  // MixHash(ciphertext)
  // Save for Reply Record KDF
  h = SHA256(h || ciphertext)
```
``replyKey``, ``layerKey`` ve ``layerIV`` hâlâ ElGamal kayıtlarının içine dahil edilmelidir ve rastgele oluşturulabilir.

### İstek Kaydı Şifrelemesi (ElGamal; açık anahtarlı şifreleme algoritması)

[Tunnel Oluşturma](/docs/specs/implementation/) içinde tanımlandığı gibi. ElGamal atlamaları için şifrelemede herhangi bir değişiklik yoktur.

### Yanıt Kaydı Şifrelemesi (ECIES - Eliptik Eğri Entegre Şifreleme Şeması)

Yanıt kaydı ChaCha20/Poly1305 ile şifrelenir.

```text
// AEAD parameters
  k = chainkey from build request
  n = 0
  plaintext = 512 byte build reply record
  ad = h from build request

  ciphertext = ENCRYPT(k, n, plaintext, ad)
```
### Yanıt Kaydı Şifrelemesi (ElGamal, açık anahtarlı şifreleme yöntemi)

[Tunnel Oluşturma](/docs/specs/implementation/) bölümünde tanımlandığı gibi. ElGamal atlamaları için şifrelemede herhangi bir değişiklik yoktur.

### Güvenlik Analizi

ElGamal, Tunnel Build Messages için ileriye dönük gizlilik sağlamaz.

AES256/CBC biraz daha iyi bir konumda, yalnızca bilinen açık metin `biclique` saldırısından (biclique: çift klik yaklaşımı) kaynaklanan teorik bir zayıflamaya karşı savunmasızdır.

AES256/CBC’ye karşı bilinen tek pratik saldırı, saldırganın IV’yi (başlatma vektörü) bildiği durumda gerçekleştirilebilen bir padding oracle attack (dolgu kehaneti saldırısı)dır.

Bir saldırganın, AES256/CBC anahtar bilgisine (yanıt anahtarı ve IV) erişebilmesi için bir sonraki atlamanın ElGamal şifrelemesini kırması gerekir.

ElGamal (açık anahtar şifreleme şeması), ECIES’e (Eliptik Eğri Entegre Şifreleme Şeması) kıyasla işlemci açısından önemli ölçüde daha yoğundur ve bu da olası kaynak tükenmesine yol açabilir.

ECIES (Eliptik Eğri Tümleşik Şifreleme Şeması), her BuildRequestRecord veya VariableTunnelBuildMessage için yeni geçici anahtarlarla kullanıldığında, ileri gizlilik sağlar.

ChaCha20Poly1305, alıcının şifre çözmeyi denemeden önce mesaj bütünlüğünü doğrulamasına olanak sağlayan AEAD şifrelemesi (İlişkili Verilerle Kimliği Doğrulanmış Şifreleme) sağlar.

## Gerekçe

Bu tasarım, mevcut kriptografik yapıtaşlarının, protokollerin ve kodun yeniden kullanımını en üst düzeye çıkarır. Bu tasarım riski en aza indirir.

## Uygulama Notları

* Eski router'lar, atlamanın şifreleme türünü kontrol etmez ve ElGamal ile şifrelenmiş
  kayıtlar gönderir. Bazı yeni router'lar hatalıdır ve çeşitli türlerde hatalı biçimlendirilmiş kayıtlar gönderir.
  Uygulayıcılar, mümkünse CPU kullanımını azaltmak için DH (Diffie-Hellman) işlemi öncesinde
  bu kayıtları tespit edip reddetmelidir.

## Sorunlar

## Geçiş

Bkz. [Öneri 156](/proposals/156-ecies-routers).

## Kaynaklar

* [Genel](/docs/specs/common-structures/)
* [Kriptografi](/docs/specs/cryptography/)
* [ECIES-X25519](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [NTCP2](/docs/specs/ntcp2/)
* [Prop119](/proposals/119-bidirectional-tunnels/)
* [Prop143](/proposals/143-build-message-options/)
* [Prop153](/proposals/153-chacha20-layer-encryption/)
* [Prop156](/proposals/156-ecies-routers/)
* [Prop157](/proposals/157-new-tbm/)
* [SPEC](/docs/specs/implementation/#tunnel-creation-ecies)
* [Tunnel-Creation](/docs/specs/tunnel-creation/)
* [Çoklu Şifreleme](https://en.wikipedia.org/wiki/Multiple_encryption)
* [RFC-7539](https://tools.ietf.org/html/rfc7539)
* [RFC-7748](https://tools.ietf.org/html/rfc7748)
