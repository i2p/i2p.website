---
title: "Yeni netDB Girişleri"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Aç"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
toc: true
---

## Durum

Bu önerinin bölümleri tamamlanmış ve 0.9.38 ve 0.9.39 sürümlerinde uygulanmıştır. Common Structures, I2CP, I2NP ve diğer spesifikasyonlar artık şu anda desteklenen değişiklikleri yansıtacak şekilde güncellenmiştir.

Tamamlanan bölümler hala küçük revizyonlara tabi olabilir. Bu teklifin diğer bölümleri hala geliştirme aşamasındadır ve önemli revizyonlara tabi olabilir.

Hizmet Arama (9 ve 11 türleri) düşük önceliklidir ve zamanlanmamıştır, ayrı bir öneriye ayrılabilir.

## Genel Bakış

Bu, aşağıdaki 4 teklifin güncellenmiş ve birleştirilmiş halidir:

- 110 LS2
- 120 Büyük çoklu barındırma için Meta LS2
- 121 Şifrelenmiş LS2
- 122 Kimlik doğrulamasız hizmet arama (anycasting)

Bu öneriler çoğunlukla bağımsızdır, ancak mantıklı olması için bunların birkaçı için ortak bir format tanımlıyor ve kullanıyoruz.

Aşağıdaki öneriler bir dereceye kadar ilişkilidir:

- 140 Invisible Multihoming (bu öneriye uyumlu değil)
- 142 New Crypto Template (yeni simetrik kripto için)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 for Encrypted LS2
- 150 Garlic Farm Protocol
- 151 ECDSA Blinding

## Öneri

Bu öneri, 5 yeni DatabaseEntry türünü ve bunları ağ veritabanına depolama ve ağ veritabanından alma sürecini, ayrıca bunları imzalama ve bu imzaları doğrulama yöntemini tanımlar.

### Goals

- Geriye dönük uyumlu
- LS2 eski tarz multihoming ile kullanılabilir
- Destek için yeni kripto veya primitifler gerekli değil
- Kripto ve imzalama ayrımını koru; tüm mevcut ve gelecek sürümleri destekle
- İsteğe bağlı çevrimdışı imzalama anahtarları etkinleştir
- Parmak izi bırakma riskini azaltmak için zaman damgası doğruluğunu düşür
- Hedefler için yeni kripto etkinleştir
- Büyük ölçekli multihoming etkinleştir
- Mevcut şifrelenmiş LS ile ilgili birden fazla sorunu düzelt
- floodfill'ler tarafından görünürlüğü azaltmak için isteğe bağlı kör etme
- Şifrelenmiş hem tek anahtarlı hem de birden fazla iptal edilebilir anahtarlı sistemleri destekler
- Outproxy'lerin, uygulama DHT bootstrap'ının ve diğer kullanımların daha kolay aranması için servis arama
- 32-byte ikili hedef hash'larına dayanan hiçbir şeyi bozma, örn. bittorrent
- RouterInfo'larda olduğu gibi özellikler aracılığıyla leaseSet'lere esneklik ekle
- Yayınlanan zaman damgası ve değişken süre sonu başlığa koy, böylece içerik şifrelenmiş olsa bile çalışır (zaman damgasını en erken lease'den türetme)
- Tüm yeni türler aynı DHT alanında ve mevcut leaseSet'ler ile aynı konumlarda yaşar,
  böylece kullanıcılar eski LS'den LS2'ye geçebilir,
  veya LS2, Meta ve Encrypted arasında değişiklik yapabilir,
  Destination veya hash'i değiştirmeden.
- Mevcut bir Destination, Destination veya hash'i değiştirmeden
  çevrimdışı anahtarlar kullanacak şekilde dönüştürülebilir,
  veya tekrar çevrimiçi anahtarlara geri döndürülebilir.

### Non-Goals / Out-of-scope

- Yeni DHT rotasyon algoritması veya paylaşılan rastgele üretim
- Kullanılacak spesifik yeni şifreleme türü ve bu yeni türü kullanacak uçtan uca şifreleme şeması
  ayrı bir öneride olacaktır.
  Burada hiçbir yeni kripto belirtilmemiş veya tartışılmamıştır.
- RI'lar veya tunnel oluşturma için yeni şifreleme.
  Bu ayrı bir öneride olacaktır.
- I2NP DLM / DSM / DSRM mesajlarının şifreleme, iletim ve alım yöntemleri.
  Değiştirilmiyor.
- Backend router-arası iletişim, yönetim, yük devretme ve koordinasyon dahil Meta'nın nasıl oluşturulacağı ve destekleneceği.
  Destek I2CP'ye, veya i2pcontrol'e, veya yeni bir protokole eklenebilir.
  Bu standartlaştırılabilir veya olmayabilir.
- Daha uzun süreli tunnel'ların nasıl gerçekten uygulanacağı ve yönetileceği, veya mevcut tunnel'ların iptal edilmesi.
  Bu son derece zordur ve bu olmadan makul bir zarif kapatma yapamazsınız.
- Tehdit modeli değişiklikleri
- Çevrimdışı depolama formatı veya verileri depolama/alma/paylaşma yöntemleri.
- Uygulama detayları burada tartışılmamıştır ve her projeye bırakılmıştır.

### Justification

LS2, şifreleme türünü değiştirmek ve gelecekteki protokol değişiklikleri için alanlar ekler.

Şifreli LS2, mevcut şifreli LS'deki birkaç güvenlik sorununu, tüm lease setinin asimetrik şifrelemesini kullanarak düzeltir.

Meta LS2 esnek, verimli, etkili ve büyük ölçekli multihoming sağlar.

Service Record ve Service List, isim arama ve DHT bootstrapping gibi anycast hizmetleri sağlar.

### Hedefler

Tür numaraları I2NP Database Lookup/Store Mesajlarında kullanılır.

Uçtan uca sütunu, sorguların/yanıtların bir Hedefe Garlic Message içinde gönderilip gönderilmediğini ifade eder.

Mevcut türler:

| NetDB Data | Lookup Type | Store Type |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
Yeni türler:

| NetDB Data     | Lookup Type | Store Type | Std. LS2 Header? | Sent end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | yes              | yes              |
| Encrypted LS2  | 1           | 5          | no               | no               |
| Meta LS2       | 1           | 7          | yes              | no               |
| Service Record | n/a         | 9          | yes              | no               |
| Service List   | 4           | 11         | no               | no               |
### Hedef Olmayanlar / Kapsam Dışı

- Lookup türleri şu anda Database Lookup Message'ındaki 3-2 bitleridir.
  Herhangi bir ek tür, bit 4'ün kullanılmasını gerektirir.

- Tüm store türleri tektir çünkü Database Store Message
  type alanındaki üst bitler eski router'lar tarafından göz ardı edilir.
  Parse işleminin sıkıştırılmış RI yerine LS olarak başarısız olmasını tercih ederiz.

- İmza tarafından kapsanan verilerde tür açık mı, örtük mü yoksa hiçbiri mi olmalı?

### Gerekçe

Tip 3, 5 ve 7, standart bir leaseset sorgusu (tip 1) yanıtında döndürülebilir. Tip 9 hiçbir zaman bir sorgu yanıtında döndürülmez. Tip 11, yeni bir servis sorgu tipi (tip 11) yanıtında döndürülür.

Yalnızca tip 3, client-to-client Garlic mesajında gönderilebilir.

### NetDB Veri Türleri

3, 7 ve 9 türlerinin hepsi ortak bir formata sahiptir::

Standart LS2 Başlığı   - aşağıda tanımlandığı gibi

Türe Özgü Kısım   - aşağıda her kısımda tanımlandığı gibi

Standart LS2 İmzası:   - İmzalama anahtarının imza türü tarafından belirtilen uzunluk

Tip 5 (Şifrelenmiş) bir Destination ile başlamaz ve farklı bir formata sahiptir. Aşağıya bakın.

Tip 11 (Servis Listesi) birkaç Servis Kaydının bir araya getirilmesidir ve farklı bir formata sahiptir. Aşağıya bakınız.

### Notlar

TBD

## Standard LS2 Header

Tip 3, 7 ve 9, aşağıda belirtilen standart LS2 başlığını kullanır:

### Arama/Saklama süreci

```
Standard LS2 Header:
  - Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Destination (387+ bytes)
  - Published timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Expires (2 bytes, big endian) (offset from published timestamp in seconds, 18.2 hours max)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bit 1: If 0, a standard published leaseset.
           If 1, an unpublished leaseset. Should not be flooded, published, or
           sent in response to a query. If this leaseset expires, do not query the
           netdb for a new one, unless bit 2 is set.
    Bit 2: If 0, a standard published leaseset.
           If 1, this unencrypted leaseset will be blinded and encrypted when published.
           If this leaseset expires, query the blinded location in the netdb for a new one.
           If this bit is set to 1, set bit 1 to 1 also.
           As of release 0.9.42.
    Bits 3-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type, and public key,
    by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
```
### Format

Turkish translation of the English text is not provided because the input text only contains the word "Format" which appears to be either a heading or standalone term. Since no additional context or content was provided to translate, I cannot determine the appropriate translation context. The word "Format" would typically translate to "Format" or "Biçim" in Turkish depending on the specific technical context.

- Unpublished/published: Bir veritabanı deposunu uçtan uca gönderirken kullanılmak üzere,
  gönderen router bu leaseSet'in başkalarına gönderilmemesi gerektiğini belirtmek isteyebilir. 
  Şu anda bu durumu korumak için buluşsal yöntemler kullanıyoruz.

- Published: Leaseset'in 'sürümünü' belirlemeyi gerektiren karmaşık mantığı değiştirir. Şu anda, sürüm son süresi dolan lease'in bitiş zamanıdır ve yayınlayan bir router, yalnızca eski bir lease'i kaldıran bir leaseset yayınlarken bu bitiş zamanını en az 1ms artırmalıdır.

- Expires: Bir netDb girişinin, son süresi dolan leaseset'inin süresinden daha erken sona ermesine izin verir. LS2 için kullanışlı olmayabilir, burada leaseset'lerin maksimum 11 dakikalık süre ile kalması beklenir, ancak diğer yeni türler için gereklidir (aşağıdaki Meta LS ve Service Record'a bakın).

- Çevrimdışı anahtarlar isteğe bağlıdır, başlangıç/gerekli uygulama karmaşıklığını azaltmak için.

### Gizlilik/Güvenlik Hususları

- Zaman damgası doğruluğu daha da azaltılabilir (10 dakika?) ancak sürüm numarası eklemek gerekir. Bu, sıra koruyucu şifrelemeye sahip olmadıkça multihoming'i bozabilir. Muhtemelen zaman damgaları olmadan hiç yapılamaz.

- Alternatif: 3 bayt zaman damgası (epoch / 10 dakika), 1-bayt sürüm, 2-bayt sona erme

- Veri / imzada tür açık mı yoksa örtük mü? İmza için "Domain" sabitleri?

### Notes

- Router'lar saniyede bir kereden fazla LS yayınlamamalıdır.
  Eğer yaparlarsa, yayınlanan zaman damgasını önceden yayınlanmış LS'ten 1 fazla olacak şekilde yapay olarak artırmalıdırlar.

- Router uygulamaları, her seferinde doğrulama yapmaktan kaçınmak için geçici anahtarları ve imzayı önbelleğe alabilir. Özellikle floodfill'ler ve uzun süreli bağlantıların her iki ucundaki router'lar bundan faydalanabilir.

- Offline anahtarlar ve imza yalnızca uzun ömürlü destinasyonlar için uygundur,
  yani sunucular için, istemciler için değil.

## New DatabaseEntry types

### Format

Mevcut LeaseSet'ten değişiklikler:

- Yayınlanma zaman damgası, son kullanma zaman damgası, bayraklar ve özellikler ekle
- Şifreleme türü ekle
- İptal anahtarını kaldır

Şununla ara

    Standard LS flag (1)
Şununla sakla

    Standard LS2 type (3)
Şuraya kaydet

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Tipik süre sonu

    10 minutes, as in a regular LS.
Yayınlayan

    Destination

### Gerekçe

```
Standard LS2 Header as specified above

  Standard LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of key sections to follow (1 byte, max TBD)
  - Key sections:
    - Encryption type (2 bytes, big endian)
    - Encryption key length (2 bytes, big endian)
      This is explicit, so floodfills can parse LS2 with unknown encryption types.
    - Encryption key (number of bytes specified)
  - Number of lease2s (1 byte)
  - Lease2s (40 bytes each)
    These are leases, but with a 4-byte instead of an 8-byte expiration,
    seconds since the epoch (rolls over in 2106)

  Standard LS2 Signature:
  - Signature
    If flag indicates offline keys, this is signed by the transient pubkey,
    otherwise, by the destination pubkey
    Length as implied by sig type of signing key
    The signature is of everything above.
```
### Sorunlar

- Özellikler: Gelecekteki genişleme ve esneklik.
  Kalan verilerin ayrıştırılması için gerekli olması durumunda ilk sıraya yerleştirilmiştir.

- Birden fazla şifreleme türü/açık anahtar çifti,
  yeni şifreleme türlerine geçişi kolaylaştırmak içindir. Bunu yapmanın diğer yolu,
  DSA ve EdDSA hedefleri için şu anda yaptığımız gibi,
  muhtemelen aynı tünelleri kullanarak birden fazla leaseSet yayınlamaktır.
  Bir tünelde gelen şifreleme türünün tanımlanması
  mevcut oturum etiketi mekanizması ile
  ve/veya her anahtarı kullanarak deneme şifre çözme ile yapılabilir. Gelen
  mesajların uzunlukları da bir ipucu sağlayabilir.

### Notlar

Bu öneri, uçtan uca şifreleme anahtarı için leaseset içindeki genel anahtarı kullanmaya devam eder ve şu anda olduğu gibi Destination içindeki genel anahtar alanını kullanılmamış olarak bırakır. Şifreleme türü Destination anahtar sertifikasında belirtilmez, 0 olarak kalacaktır.

Reddedilen bir alternatif, şifreleme türünü Destination anahtar sertifikasında belirtmek, Destination içindeki public key'i kullanmak ve leaseset içindeki public key'i kullanmamaktır. Bunu yapmayı planlamıyoruz.

LS2'nin Faydaları:

- Gerçek public key'in konumu değişmez.
- Encryption türü veya public key, Destination'ı değiştirmeden değişebilir.
- Kullanılmayan revocation alanını kaldırır
- Bu önerideki diğer DatabaseEntry türleriyle temel uyumluluk
- Birden fazla encryption türüne izin verir

LS2'nin Dezavantajları:

- Public key konumu ve şifreleme türü RouterInfo'dan farklıdır
- Leaseset'te kullanılmayan public key'i korur
- Ağ genelinde implementasyon gerektirir; alternatif olarak, deneysel
  şifreleme türleri floodfill'ler tarafından izin verilirse kullanılabilir
  (ancak deneysel sig türleri desteği hakkında ilgili 136 ve 137 önerilerine bakınız).
  Alternatif öneri, deneysel şifreleme türleri için implement edilmesi ve test edilmesi daha kolay olabilir.

### New Encryption Issues

Bu önerilerin bir kısmı bu teklifin kapsamı dışındadır, ancak henüz ayrı bir şifreleme teklifimiz olmadığı için notları burada tutuyoruz. Ayrıca ECIES teklifleri 144 ve 145'e bakınız.

- Şifreleme türü, eğri, anahtar uzunluğu ve uçtan uca şemanın
  kombinasyonunu temsil eder ve varsa KDF ve MAC'i de içerir.

- LS2'nin bilinmeyen şifreleme türleri için bile floodfill tarafından ayrıştırılabilir ve doğrulanabilir olması için bir anahtar uzunluğu alanı ekledik.

- Önerilecek ilk yeni şifreleme türü muhtemelen
  ECIES/X25519 olacaktır. Bunun uçtan uca nasıl kullanılacağı
  (ElGamal/AES+SessionTag'in hafifçe değiştirilmiş bir versiyonu
  ya da tamamen yeni bir şey, örneğin ChaCha/Poly) bir veya daha fazla
  ayrı öneri ile belirtilecektir.
  Ayrıca ECIES önerileri 144 ve 145'e bakın.

### LeaseSet 2

- Lease'lerdeki 8-byte süre dolumu 4 byte'a değiştirildi.

- Eğer iptal (revocation) işlevini uygularsak, bunu sıfır expires alanı, 
  sıfır lease veya her ikisi ile yapabiliriz. Ayrı bir iptal anahtarına gerek yok.

- Şifreleme anahtarları sunucu tercih sırasına göre düzenlenmiştir, en çok tercih edilen ilk sıradadır.
  Varsayılan istemci davranışı, desteklenen bir şifreleme türüne sahip
  ilk anahtarı seçmektir. İstemciler şifreleme desteği, göreli performans ve diğer faktörlere
  dayalı olarak başka seçim algoritmaları kullanabilir.

### Format

Hedefler:

- Blinding ekleme
- Birden fazla imza türüne izin verme
- Herhangi bir yeni kripto primitifi gerektirmeme
- İsteğe bağlı olarak her alıcıya şifreleme, iptal edilebilir
- Yalnızca Standard LS2 ve Meta LS2 şifrelemesini destekleme

Şifrelenmiş LS2 hiçbir zaman uçtan uca garlic mesajında gönderilmez. Yukarıdaki standart LS2'yi kullanın.

Mevcut şifreli LeaseSet'ten değişiklikler:

- Güvenlik için her şeyi şifreleyin
- Güvenli bir şekilde şifreleyin, sadece AES ile değil.
- Her alıcı için ayrı ayrı şifreleyin

ile Arama

    Standard LS flag (1)
Şununla sakla

    Encrypted LS2 type (5)
Şurada sakla

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Tipik sona erme

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Yayınlayan

    Destination

### Gerekçe

Şifreli LS2 için kullanılan kriptografik yapı taşlarına karşılık gelen aşağıdaki fonksiyonları tanımlıyoruz:

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

STREAM

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.

SIG

    The RedDSA signature scheme (corresponding to SigType 11) with key blinding.
    It has the following functions:

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    SIGN(privkey, m)
        Returns a signature by the private key privkey over the given message m.

    VERIFY(pubkey, m, sig)
        Verifies the signature sig against the public key pubkey and message m. Returns
        true if the signature is valid, false otherwise.

    It must also support the following key blinding operations:

    GENERATE_ALPHA(data, secret)
        Generate alpha for those who know the data and an optional secret.
        The result must be identically distributed as the private keys.

    BLIND_PRIVKEY(privkey, alpha)
        Blinds a private key, using a secret alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Blinds a public key, using a secret alpha.
        For a given keypair (privkey, pubkey) the following relationship holds::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.

### Tartışma

Şifrelenmiş LS2 formatı üç iç içe katmandan oluşur:

- Depolama ve erişim için gerekli düz metin bilgilerini içeren dış katman.
- İstemci kimlik doğrulamasını yöneten orta katman.
- Gerçek LS2 verilerini içeren iç katman.

Genel format şu şekildedir::

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

Şifreli LS2'nin köreltildiğini (blinded) unutmayın. Destination başlıkta bulunmaz. DHT depolama konumu SHA-256(sig type || blinded public key) şeklindedir ve günlük olarak döndürülür.

Yukarıda belirtilen standart LS2 başlığını KULLANMAZ.

#### Layer 0 (outer)

Tür

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Körleştirilmiş Açık Anahtar İmza Türü

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

Kör Edilmiş Açık Anahtar

    Length as implied by sig type

Yayınlanma zaman damgası

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Sona Erer

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Bayraklar

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Geçici anahtar verisi

    Present if flag indicates offline keys

    Expires timestamp
        4 bytes, big endian

        Seconds since epoch, rolls over in 2106

    Transient sig type
        2 bytes, big endian

    Transient signing public key
        Length as implied by sig type

    Signature
        Length as implied by blinded public key sig type

        Over expires timestamp, transient sig type, and transient public key.

        Verified with the blinded public key.

lenOuterCiphertext

    2 bytes, big endian

outerCiphertext

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

İmza

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.

#### Layer 1 (middle)

Bayraklar

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

DH istemci kimlik doğrulama verisi

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 000.

    ephemeralPublicKey
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

PSK istemci kimlik doğrulama verisi

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 001.

    authSalt
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

innerCiphertext

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.

#### Layer 2 (inner)

Tür

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

Veri

    LeaseSet2 data for the given type.

    Includes the header and signature.

### Yeni Şifreleme Sorunları

Anahtar körleme için aşağıdaki şemayı kullanıyoruz, Ed25519 ve [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) tabanlı. Re25519 imzaları Ed25519 eğrisi üzerinde, hash için SHA-512 kullanarak.

[Tor'un rend-spec-v3.txt ek A.2](https://spec.torproject.org/rend-spec-v3) bölümünü kullanmıyoruz, çünkü benzer tasarım hedeflerine sahip olmasına rağmen, kör edilmiş (blinded) public key'leri prime-order alt grubunun dışında olabilir ve bu durum bilinmeyen güvenlik sonuçları doğurabilir.

#### Goals

- Kör edilmemiş hedefte bulunan imzalama public key'i
  Ed25519 (sig type 7) veya Red25519 (sig type 11) olmalıdır;
  diğer sig type'lar desteklenmez
- İmzalama public key'i çevrimdışıysa, geçici imzalama public key'i de Ed25519 olmalıdır
- Blinding işlemi hesaplama açısından basittir
- Mevcut kriptografik primitifleri kullanır
- Blind edilmiş public key'ler unblind edilemez
- Blind edilmiş public key'ler Ed25519 eğrisi ve asal-dereceli alt grup üzerinde olmalıdır
- Blind edilmiş public key'i türetmek için hedefin imzalama public key'ini
  bilmek gerekir (tam hedef gerekli değil)
- İsteğe bağlı olarak blind edilmiş public key'i türetmek için gereken ek bir gizli anahtar sağlanabilir

#### Security

Bir blinding şemasının güvenliği, alpha'nın dağılımının köreltilmemiş özel anahtarlarla aynı olmasını gerektirir. Ancak, bir Ed25519 özel anahtarını (sig türü 7) Red25519 özel anahtarına (sig türü 11) körelttiğimizde, dağılım farklıdır. [zcash bölüm 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) gereksinimlerini karşılamak için, Red25519 (sig türü 11) köreltilmemiş anahtarlar için de kullanılmalıdır, böylece "yeniden rastgeleleştirilmiş bir açık anahtar ve bu anahtar altındaki imza(lar) kombinasyonu, yeniden rastgeleleştirme işleminin kaynaklandığı anahtarı açığa çıkarmaz." Mevcut destinasyonlar için tür 7'ye izin veriyoruz, ancak şifrelenecek yeni destinasyonlar için tür 11'i öneriyoruz.

#### Definitions

B

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

L

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

DERIVE_PUBLIC(a)

    Convert a private key to public, as in Ed25519 (mulitply by G)

alfa

    A 32-byte random number known to those who know the destination.

GENERATE_ALPHA(destination, date, secret)

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

a

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

A

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

a'

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

A'

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

LEOS2IP(x)

    Flip the order of the input bytes to little-endian

H*(x)

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce

#### Blinding Calculations

Her gün (UTC) yeni bir gizli alfa ve köreltilmiş anahtarlar üretilmelidir. Gizli alfa ve köreltilmiş anahtarlar aşağıdaki şekilde hesaplanır.

GENERATE_ALPHA(destination, date, secret), tüm taraflar için:

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret is optional, else zero-length
  A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of blinded public key A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD from the current date UTC
  secret = UTF-8 encoded string
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // treat seed as a 64 byte little-endian value
  alpha = seed mod L
```
BLIND_PRIVKEY(), leaseset'i yayınlayan sahip için:

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // If for a Ed25519 private key (type 7)
  seed = destination's signing private key
  a = left half of SHA512(seed) and clamped as usual for Ed25519
  // else, for a Red25519 private key (type 11)
  a = destination's signing private key
  // Addition using scalar arithmentic
  blinded signing private key = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  blinded signing public key = A' = DERIVE_PUBLIC(a')
```
BLIND_PUBKEY(), leaseset'i alan istemciler için:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
Her iki A' hesaplama yöntemi de gerektiği gibi aynı sonucu verir.

#### Signing

Unblinded leaseset, unblinded Ed25519 veya Red25519 imzalama özel anahtarı ile imzalanır ve her zamanki gibi unblinded Ed25519 veya Red25519 imzalama genel anahtarı (sig türleri 7 veya 11) ile doğrulanır.

İmzalama genel anahtarı çevrimdışıysa, unblinded leaseset, unblinded geçici Ed25519 veya Red25519 imzalama özel anahtarı tarafından imzalanır ve her zamanki gibi unblinded Ed25519 veya Red25519 geçici imzalama genel anahtarı (sig türleri 7 veya 11) ile doğrulanır. Şifrelenmiş leaseset'ler için çevrimdışı anahtarlarla ilgili ek notlar için aşağıya bakın.

Şifrelenmiş leaseSet'in imzalanması için, köreltilmiş anahtarlarla imzalama ve doğrulama yapmak üzere [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) tabanlı Red25519 kullanırız. Red25519 imzaları Ed25519 eğrisi üzerindedir ve hash için SHA-512 kullanır.

Red25519, aşağıda belirtilen durumlar dışında standart Ed25519 ile aynıdır.

#### Sign/Verify Calculations

Şifrelenmiş leaseset'in dış kısmı Red25519 anahtarları ve imzaları kullanır.

Red25519, Ed25519 ile neredeyse aynıdır. İki fark vardır:

Red25519 özel anahtarları rastgele sayılardan üretilir ve ardından yukarıda tanımlanan L değerine göre mod L işlemiyle indirgenir. Ed25519 özel anahtarları rastgele sayılardan üretilir ve ardından 0 ve 31. baytlara bit düzeyinde maskeleme kullanılarak "kısıtlanır". Bu işlem Red25519 için yapılmaz. Yukarıda tanımlanan GENERATE_ALPHA() ve BLIND_PRIVKEY() fonksiyonları mod L kullanarak uygun Red25519 özel anahtarları üretir.

Red25519'da, imzalama için r hesaplaması ek rastgele veri kullanır ve özel anahtarın hash'i yerine genel anahtar değerini kullanır. Rastgele veri nedeniyle, aynı veriyi aynı anahtarla imzalarken bile her Red25519 imzası farklıdır.

İmzalama:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Doğrulama:

```text
// same as in Ed25519
```
### Notlar

#### Derivation of subcredentials

Kör etme işleminin bir parçası olarak, şifrelenmiş bir LS2'nin yalnızca ilgili Destination'ın imzalama genel anahtarını bilen biri tarafından şifresinin çözülebilmesini sağlamamız gerekir. Tam Destination gerekmez. Bunu başarmak için, imzalama genel anahtarından bir kimlik bilgisi türetiriz:

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
Kişiselleştirme dizesi, credential'ın düz Destination hash'i gibi DHT arama anahtarı olarak kullanılan herhangi bir hash ile çakışmamasını sağlar.

Belirli bir kör edilmiş anahtar için, ardından bir alt kimlik bilgisi türetebiliriz:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
Alt kimlik bilgisi, aşağıdaki anahtar türetme süreçlerinde yer alır ve bu anahtarları Destination'ın imzalama genel anahtarı bilgisine bağlar.

#### Layer 1 encryption

Öncelikle, anahtar türetme sürecinin girdisi hazırlanır:

```text
outerInput = subcredential || publishedTimestamp
```
Daha sonra, rastgele bir salt oluşturulur:

```text
outerSalt = CSRNG(32)
```
Ardından katman 1'i şifrelemek için kullanılan anahtar türetilir:

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Son olarak, katman 1 düz metni şifrelenir ve serileştirilir:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Layer 1 decryption

Tuz, katman 1 şifreli metindan ayrıştırılır:

```text
outerSalt = outerCiphertext[0:31]
```
Ardından katman 1'i şifrelemek için kullanılan anahtar türetilir:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Son olarak, katman 1 şifreli metni şifre çözülür:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Layer 2 encryption

İstemci yetkilendirmesi etkinleştirildiğinde, ``authCookie`` aşağıda açıklandığı gibi hesaplanır. İstemci yetkilendirmesi devre dışı bırakıldığında, ``authCookie`` sıfır uzunluklu bayt dizisidir.

Şifreleme, katman 1'e benzer bir şekilde ilerler:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Layer 2 decryption

İstemci yetkilendirmesi etkinleştirildiğinde, ``authCookie`` aşağıda açıklandığı şekilde hesaplanır. İstemci yetkilendirmesi devre dışı bırakıldığında, ``authCookie`` sıfır uzunluklu bayt dizisidir.

Şifre çözme işlemi katman 1'e benzer bir şekilde devam eder:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### Şifrelenmiş LS2

Bir Destination için istemci yetkilendirmesi etkinleştirildiğinde, sunucu şifrelenmiş LS2 verilerinin şifresini çözmeye yetkili oldukları istemcilerin bir listesini tutar. İstemci başına saklanan veriler yetkilendirme mekanizmasına bağlıdır ve her istemcinin oluşturup güvenli bir bant-dışı mekanizma aracılığıyla sunucuya gönderdiği bir tür anahtar materyali içerir.

İstemci başına yetkilendirme uygulamak için iki alternatif bulunmaktadır:

#### DH client authorization

Her istemci bir DH anahtar çifti ``[csk_i, cpk_i]`` oluşturur ve genel anahtar ``cpk_i``'yi sunucuya gönderir.

Sunucu işleme
^^^^^^^^^^^^^^^^^

Sunucu yeni bir ``authCookie`` ve geçici bir DH anahtar çifti oluşturur:

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Ardından her yetkili istemci için, sunucu ``authCookie``'yi onun public key'ine şifreler:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Sunucu, her ``[clientID_i, clientCookie_i]`` tuple'ını ``epk`` ile birlikte şifrelenmiş LS2'nin 1. katmanına yerleştirir.

İstemci işleme
^^^^^^^^^^^^^^^^^

İstemci, beklenen istemci tanımlayıcısı ``clientID_i``, şifreleme anahtarı ``clientKey_i`` ve şifreleme IV ``clientIV_i`` değerlerini türetmek için özel anahtarını kullanır:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Ardından istemci, ``clientID_i`` içeren bir giriş için katman 1 yetkilendirme verilerini arar. Eşleşen bir giriş mevcutsa, istemci ``authCookie`` elde etmek için onu şifreler:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Pre-shared key client authorization

Her istemci gizli 32-byte'lık bir anahtar ``psk_i`` oluşturur ve bunu sunucuya gönderir. Alternatif olarak, sunucu gizli anahtarı oluşturabilir ve bir veya daha fazla istemciye gönderebilir.

Sunucu işleme
^^^^^^^^^^^^^^^^^

Sunucu yeni bir ``authCookie`` ve salt oluşturur:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Her yetkili istemci için sunucu, ``authCookie``'yi önceden paylaşılan anahtarına şifreler:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Sunucu, her ``[clientID_i, clientCookie_i]`` ikilisini ``authSalt`` ile birlikte şifrelenmiş LS2'nin 1. katmanına yerleştirir.

İstemci işleme
^^^^^^^^^^^^^^^^^

İstemci, beklenen istemci tanımlayıcısı ``clientID_i``, şifreleme anahtarı ``clientKey_i`` ve şifreleme IV ``clientIV_i`` değerlerini türetmek için önceden paylaşılmış anahtarını kullanır:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Ardından istemci, katman 1 yetkilendirme verilerinde ``clientID_i`` içeren bir girdi arar. Eşleşen bir girdi varsa, istemci ``authCookie`` elde etmek için şifreyi çözer:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Security considerations

Yukarıdaki istemci yetkilendirme mekanizmalarının her ikisi de istemci üyeliği için gizlilik sağlar. Yalnızca Destination'ı bilen bir varlık, herhangi bir zamanda kaç istemcinin abone olduğunu görebilir, ancak hangi istemcilerin eklendiğini veya iptal edildiğini takip edemez.

Sunucular, istemcilerin listede kendi konumlarını öğrenmelerini ve diğer istemcilerin ne zaman eklendiğini veya kaldırıldığını çıkarsamalarını önlemek için, şifrelenmiş bir LS2 oluşturdukları her seferde istemcilerin sırasını rastgele hale getirmelidirler.

Bir sunucu, yetkilendirme verileri listesine rastgele girdiler ekleyerek abone olan istemci sayısını gizlemeyi SEÇEBİLİR.

DH istemci yetkilendirmesinin avantajları
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Şemanın güvenliği yalnızca istemci anahtar materyalinin bant dışı değişimine bağlı değildir. İstemcinin özel anahtarının hiçbir zaman cihazından ayrılmasına gerek yoktur ve bu nedenle bant dışı değişimi engelleyebilen ancak DH algoritmasını kıramayan bir saldırgan, şifrelenmiş LS2'yi çözemez veya istemciye ne kadar süre erişim verildiğini belirleyemez.

DH istemci yetkilendirmesinin dezavantajları
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- N istemci için sunucu tarafında N + 1 DH işlemi gerektirir.
- İstemci tarafında bir DH işlemi gerektirir.
- İstemcinin gizli anahtarı oluşturmasını gerektirir.

PSK istemci yetkilendirmesinin avantajları
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- DH işlemleri gerektirmez.
- Sunucunun gizli anahtarı oluşturmasına izin verir.
- İstenirse sunucunun aynı anahtarı birden fazla istemciyle paylaşmasına izin verir.

PSK istemci yetkilendirmesinin dezavantajları
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Şemanın güvenliği, istemci anahtar materyalinin bant dışı değişimine kritik olarak bağımlıdır. Belirli bir istemci için değişimi engelleyen bir saldırgan, o istemcinin yetkilendirildiği sonraki şifrelenmiş LS2'leri çözebilir ve aynı zamanda istemcinin erişiminin ne zaman iptal edildiğini belirleyebilir.

### Tanımlar

149 numaralı öneriye bakın.

BitTorrent için şifrelenmiş bir LS2 kullanamazsınız, çünkü compact announce yanıtları 32 bayttır. Bu 32 bayt yalnızca hash'i içerir. LeaseSet'in şifrelendiğini veya imza türlerini belirten bir yer yoktur.

### Format

Çevrimdışı anahtarlara sahip şifrelenmiş leaseSets için, kör edilmiş özel anahtarlar da çevrimdışı olarak üretilmelidir, her gün için bir tane.

Şifrelenmiş leaseset'in açık metin kısmında bulunan isteğe bağlı çevrimdışı imza bloğu nedeniyle, floodfill'leri tarayan herhangi biri bunu birkaç gün boyunca leaseset'i takip etmek için kullanabilir (ancak şifrelerini çözemez). Bunu önlemek için anahtar sahibi her gün için yeni geçici anahtarlar da oluşturmalıdır. Hem geçici hem de körleştirilmiş anahtarlar önceden oluşturulabilir ve router'a toplu olarak teslim edilebilir.

Bu teklifte birden fazla geçici ve körleştirilmiş anahtarı paketlemek ve bunları istemciye veya router'a sağlamak için tanımlanmış bir dosya formatı bulunmamaktadır. Bu teklifte çevrimdışı anahtarlarla şifrelenmiş leaseSet'leri desteklemek için tanımlanmış bir I2CP protokol geliştirmesi bulunmamaktadır.

### Notes

- Şifrelenmiş leaseSet'ler kullanan bir hizmet, şifrelenmiş versiyonu
  floodfill'lere yayınlar. Ancak verimlilik için, kimlik doğrulamasından sonra
  (örneğin whitelist aracılığıyla) istemcilere sarmalanmış garlic mesajında
  şifrelenmemiş leaseSet'ler gönderir.

- Floodfill'ler kötüye kullanımı önlemek için maksimum boyutu makul bir değerle sınırlayabilir.

- Şifre çözme işleminden sonra, iç zaman damgası ve son kullanma tarihinin üst seveldekilerle eşleşmesi de dahil olmak üzere çeşitli kontroller yapılmalıdır.

- ChaCha20, AES yerine tercih edildi. AES donanım desteği mevcut olduğunda hızlar benzer olsa da, ChaCha20, düşük seviye ARM cihazları gibi AES donanım desteğinin bulunmadığı durumlarda 2.5-3 kat daha hızlıdır.

- Hızla yeterince ilgilenmediğimiz için anahtarlı BLAKE2b kullanmıyoruz. İhtiyaç duyduğumuz en büyük n değerini karşılayacak kadar büyük bir çıktı boyutuna sahip (veya sayaç argümanı ile istenen anahtar başına bir kez çağırabiliriz). BLAKE2b, SHA-256'dan çok daha hızlıdır ve anahtarlı-BLAKE2b toplam hash fonksiyonu çağrısı sayısını azaltır.
  Ancak, diğer nedenlerle BLAKE2b'ye geçmeyi önerdiğimiz 148 numaralı öneriyi görün.
  Bkz. [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Meta LS2

Bu, multihoming'i değiştirmek için kullanılır. Herhangi bir leaseset gibi, bu da yaratıcı tarafından imzalanır. Bu, hedef hash'lerin kimlik doğrulamalı bir listesidir.

Meta LS2, ağaç yapısının en üstünde ve muhtemelen ara düğümlerinde bulunur. Büyük çoklu barındırma (massive multihoming) desteği için her biri bir LS, LS2 veya başka bir Meta LS2'yi işaret eden bir dizi giriş içerir. Bir Meta LS2, LS, LS2 ve Meta LS2 girişlerinin karışımını içerebilir. Ağacın yaprakları her zaman bir LS veya LS2'dir. Ağaç bir DAG'dır; döngüler yasaklanmıştır; arama yapan istemciler döngüleri tespit etmeli ve takip etmeyi reddetmelidir.

Bir Meta LS2, standart bir LS veya LS2'den çok daha uzun bir sona erme süresine sahip olabilir. Üst düzey, yayınlama tarihinden birkaç saat sonra bir sona erme süresine sahip olabilir. Maksimum sona erme süresi floodfill'ler ve istemciler tarafından uygulanacaktır ve henüz belirlenmemiştir.

Meta LS2'nin kullanım senaryosu büyük ölçekli multihoming'dir, ancak router'ların leaseSet'lere korelasyonuna karşı (router yeniden başlatma zamanında) şu anda LS veya LS2 ile sağlanandan daha fazla koruma sunmaz. Bu, muhtemelen korelasyon korumasına ihtiyaç duymayan "facebook" kullanım senaryosuna eşdeğerdir. Bu kullanım senaryosu muhtemelen ağacın her düğümünde standart başlıkta sağlanan offline anahtarlara ihtiyaç duyar.

Yaprak router'ları, ara ve ana Meta LS imzalayıcıları arasındaki koordinasyon için arka uç protokolü burada belirtilmemiştir. Gereksinimler son derece basittir - sadece eşin çalışır durumda olduğunu doğrulayın ve birkaç saatte bir yeni bir LS yayınlayın. Tek karmaşıklık, başarısızlık durumunda üst düzey veya ara düzey Meta LS'ler için yeni yayıncıları seçmektir.

Birden fazla router'dan gelen lease'lerin birleştirildiği, imzalandığı ve tek bir leaseset içinde yayınlandığı mix-and-match leaseset'ler, 140 numaralı öneride "invisible multihoming" olarak belgelenmiştir. Bu öneri yazıldığı şekliyle uygulanamaz, çünkü streaming bağlantıları tek bir router'a "yapışkan" olmayacaktır, bakınız http://zzz.i2p/topics/2335 .

Arka uç protokolü ve router ile istemci iç yapılarıyla etkileşim, görünmez çoklu bağlantı (invisible multihoming) için oldukça karmaşık olacaktır.

Üst düzey Meta LS için floodfill'i aşırı yüklemekten kaçınmak için, son kullanma süresi en az birkaç saat olmalıdır. İstemciler üst düzey Meta LS'yi önbelleklemeli ve süresi dolmamışsa yeniden başlatmalar boyunca kalıcı hale getirmelidir.

İstemcilerin ağacı geçmesi için, yedek seçenekler dahil olmak üzere, kullanımın dağıtılması için bir algoritma tanımlamamız gerekiyor. Hash mesafesi, maliyet ve rastgelelik fonksiyonu. Bir düğümde hem LS veya LS2 hem de Meta LS varsa, bu leaseSet'leri ne zaman kullanmaya izin verildiğini ve ne zaman ağacı geçmeye devam edeceğimizi bilmemiz gerekiyor.

ile Arama

    Standard LS flag (1)
İle sakla

    Meta LS2 type (7)
Şu konumda sakla

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Tipik son kullanma süresi

    Hours. Max 18.2 hours (65535 seconds)
Yayınlayan

    "master" Destination or coordinator, or intermediate coordinators

### Format

```
Standard LS2 Header as specified above

  Meta LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of entries (1 byte) Maximum TBD
  - Entries. Each entry contains: (40 bytes)
    - Hash (32 bytes)
    - Flags (2 bytes)
      TBD. Set all to zero for compatibility with future uses.
    - Type (1 byte) The type of LS it is referencing;
      1 for LS, 3 for LS2, 5 for encrypted, 7 for meta, 0 for unknown.
    - Cost (priority) (1 byte)
    - Expires (4 bytes) (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Number of revocations (1 byte) Maximum TBD
  - Revocations: Each revocation contains: (32 bytes)
    - Hash (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
Bayraklar ve özellikler: gelecekteki kullanım için

### Körleme Anahtarı Türetimi

- Bu hizmeti kullanan dağıtık bir servis, servis hedefinin özel anahtarına sahip bir veya daha fazla "master"a sahip olacaktır. Bunlar (bant dışı) mevcut aktif hedeflerin listesini belirleyecek ve Meta LS2'yi yayınlayacaktır. Yedeklilik için, birden fazla master Meta LS2'yi multihome (yani eşzamanlı olarak yayınlama) yapabilir.

- Dağıtık bir servis tek bir destination ile başlayabilir veya eski tarz
  multihoming kullanabilir, ardından Meta LS2'ye geçiş yapabilir. Standart bir LS
  arama işlemi LS, LS2 veya Meta LS2'den herhangi birini döndürebilir.

- Bir servis Meta LS2 kullandığında, hiçbir tüneli (lease) yoktur.

### Service Record

Bu, bir hedefin (destination) bir hizmette katılım gösterdiğini belirten bireysel bir kayıttır. Katılımcıdan floodfill'e gönderilir. Bir floodfill tarafından asla tek başına gönderilmez, yalnızca Service List'in bir parçası olarak gönderilir. Service Record ayrıca, süre sonunu (expiration) sıfıra ayarlayarak bir hizmetteki katılımı iptal etmek için de kullanılır.

Bu bir LS2 değildir ancak standart LS2 başlık ve imza formatını kullanır.

ile Arama

    n/a, see Service List
Şununla depola

    Service Record type (9)
Şu konumda sakla

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Tipik sona erme süresi

    Hours. Max 18.2 hours (65535 seconds)
Yayınlayan

    Destination

### Format

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Notes

- Eğer expires tamamen sıfırlardan oluşuyorsa, floodfill kaydı iptal etmeli ve artık onu servis listesine dahil etmemelidir.

- Depolama: Floodfill bu kayıtların depolanmasını sıkı bir şekilde kısıtlayabilir ve
  hash başına depolanan kayıt sayısını ve bunların sona erme sürelerini sınırlayabilir. Ayrıca
  hash'lerin beyaz listesi de kullanılabilir.

- Aynı hash'te bulunan diğer netDb türleri önceliğe sahiptir, bu nedenle bir servis kaydı asla bir LS/RI'yi üzerine yazamaz, ancak bir LS/RI o hash'teki tüm servis kayıtlarını üzerine yazar.

### Service List

Bu bir LS2 gibi bir şey değildir ve farklı bir format kullanır.

Hizmet listesi floodfill tarafından oluşturulur ve imzalanır. Herhangi birinin bir floodfill'e Hizmet Kaydı yayınlayarak bir hizmete katılabilmesi nedeniyle kimlik doğrulaması yapılmaz.

Bir Servis Listesi, tam Servis Kayıtları değil, Kısa Servis Kayıtları içerir. Bunlar imzalar içerir ancak tam destination'lar değil, yalnızca hash'ler içerir, bu nedenle tam destination olmadan doğrulanamaz.

Hizmet listelerinin güvenliği (varsa) ve arzu edilirliği henüz belirlenmemiştir. Floodfill'ler yayınlamayı ve aramaları bir hizmet beyaz listesiyle sınırlandırabilir, ancak bu beyaz liste implementasyona veya operatör tercihine bağlı olarak değişebilir. İmplementasyonlar arasında ortak, temel bir beyaz liste üzerinde fikir birliğine varmak mümkün olmayabilir.

Yukarıdaki servis kaydında servis adı dahil edilmişse, floodfill operatörleri itiraz edebilir; sadece hash dahil edilmişse, doğrulama yoktur ve bir servis kaydı diğer herhangi bir netDb türünden önce "içeri girebilir" ve floodfill'de saklanabilir.

Şununla arama yap

    Service List lookup type (11)
Şununla sakla

    Service List type (11)
Şurada sakla

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Tipik süre sonu

    Hours, not specified in the list itself, up to local policy
Yayımlayan

    Nobody, never sent to floodfill, never flooded.

### Format

Yukarıda belirtilen standart LS2 başlığını KULLANMAZ.

```
- Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Hash of the service name (implicit, in the Database Store message)
  - Hash of the Creator (floodfill) (32 bytes)
  - Published timestamp (8 bytes, big endian)

  - Number of Short Service Records (1 byte)
  - List of Short Service Records:
    Each Short Service Record contains (90+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Expires (4 bytes, big endian) (offset from published in ms)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Number of Revocation Records (1 byte)
  - List of Revocation Records:
    Each Revocation Record contains (86+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Signature of floodfill (40+ bytes)
    The signature is of everything above.
```
Servis Listesinin imzasını doğrulamak için:

- servis adının hash'ini başa ekle
- yaratıcının hash'ini kaldır
- değiştirilmiş içeriklerin imzasını kontrol et

Her Kısa Servis Kaydının imzasını doğrulamak için:

- Hedefi getir
- İmzayı kontrol et (yayınlanan zaman damgası + sona erme + bayraklar + port + Servis adının Hash'i)

Her İptal Kaydının imzasını doğrulamak için:

- Hedef konumu getir
- İmzayı kontrol et (yayınlanan zaman damgası + 4 sıfır bayt + bayraklar + port + Servis adının hash'i)

### Notes

- Bilinmeyen imza türlerini destekleyebilmek için imza türü yerine imza uzunluğu kullanıyoruz.

- Bir hizmet listesinin son kullanma tarihi yoktur, alıcılar politikaya veya bireysel kayıtların son kullanma tarihine dayanarak kendi kararlarını verebilirler.

- Service Lists flood edilmez, sadece bireysel Service Records flood edilir. Her
  floodfill bir Service List oluşturur, imzalar ve önbelleğe alır. Floodfill,
  önbellek süresi ve maksimum service ile revocation record sayısı için kendi
  politikasını kullanır.

## Common Structures Spec Changes Required

### Şifreleme ve işleme

Bu önerinin kapsamı dışında. ECIES önerilerinden 144 ve 145'e ekleyin.

### New Intermediate Structures

Release 0.9.38 itibariyle geçerli olmak üzere Lease2, MetaLease, LeaseSet2Header ve OfflineSignature için yeni yapılar ekle.

### New NetDB Types

Yukarıdan dahil edilen her yeni leaseset türü için yapılar ekleyin. LeaseSet2, EncryptedLeaseSet ve MetaLeaseSet için 0.9.38 sürümünden itibaren geçerlidir. Service Record ve Service List için ön aşamada ve planlanmamış.

### New Signature Type

RedDSA_SHA512_Ed25519 Tip 11'i ekleyin. Public key 32 bayt; private key 32 bayt; hash 64 bayt; imza 64 bayttır.

## Encryption Spec Changes Required

Bu teklif kapsamı dışındadır. Teklifleri 144 ve 145'e bakınız.

## I2NP Changes Required

Not ekle: LS2 yalnızca minimum sürüme sahip floodfill'lere yayınlanabilir.

### Database Lookup Message

Hizmet listesi arama türünü ekleyin.

### Changes

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### İstemci başına yetkilendirme

Tüm yeni mağaza türlerini ekleyin.

### Changes

```
Type byte: Type field, currently bit 0, expands to bits 3-0.
  Type 3 is defined as a LS2 store.
  Type 5 is defined as a encrypted LS2 store.
  Type 7 is defined as a meta LS2 store.
  Type 9 is defined as a service record store.
  Type 11 is defined as a service list store.
  Other types are undefined and invalid.

  Add note: All new types may only be published to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
## I2CP Changes Required

### I2CP Options

Router tarafında yorumlanan yeni seçenekler, SessionConfig Mapping içinde gönderilir:

```

  i2cp.leaseSetType=nnn       The type of leaseset to be sent in the Create Leaseset Message
                              Value is the same as the netdb store type in the table above.
                              Interpreted client-side, but also passed to the router in the
                              SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetOfflineExpiration=nnn  The expiration of the offline signature, ASCII,
                                      seconds since the epoch.

  i2cp.leaseSetTransientPublicKey=[type:]b64  The base 64 of the transient private key,
                                              prefixed by an optional sig type number
                                              or name, default DSA_SHA1.
                                              Length as inferred from the sig type

  i2cp.leaseSetOfflineSignature=b64   The base 64 of the offline signature.
                                      Length as inferred from the destination
                                      signing public key type

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn   The type of authentication for encrypted LS2.
                              0 for no per-client authentication (the default)
                              1 for DH per-client authentication
                              2 for PSK per-client authentication

  i2cp.leaseSetPrivKey=b64    A base 64 private key for the router to use to
                              decrypt the encrypted LS2,
                              only if per-client authentication is enabled
```
İstemci tarafında yorumlanan yeni seçenekler:

```

  i2cp.leaseSetType=nnn     The type of leaseset to be sent in the Create Leaseset Message
                            Value is the same as the netdb store type in the table above.
                            Interpreted client-side, but also passed to the router in the
                            SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn       The type of authentication for encrypted LS2.
                                  0 for no per-client authentication (the default)
                                  1 for DH per-client authentication
                                  2 for PSK per-client authentication

  i2cp.leaseSetBlindedType=nnn   The sig type of the blinded key for encrypted LS2.
                                 Default depends on the destination sig type.

  i2cp.leaseSetClient.dh.nnn=b64name:b64pubkey   The base 64 of the client name (ignored, UI use only),
                                                 followed by a ':', followed by the base 64 of the public
                                                 key to use for DH per-client auth. nnn starts with 0

  i2cp.leaseSetClient.psk.nnn=b64name:b64privkey   The base 64 of the client name (ignored, UI use only),
                                                   followed by a ':', followed by the base 64 of the private
                                                   key to use for PSK per-client auth. nnn starts with 0
```
### Session Config

Çevrimdışı imzalar için i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey ve i2cp.leaseSetOfflineSignature seçeneklerinin gerekli olduğunu ve imzanın geçici imzalama özel anahtarı tarafından yapıldığını unutmayın.

### Base 32 Adresleri ile Şifrelenmiş LS

Router'dan istemciye. Değişiklik yok. Kiralamalar (lease) 8-byte zaman damgalarıyla gönderilir, döndürülen leaseSet bir LS2 olsa ve 4-byte zaman damgalarına sahip olsa bile. Yanıtın bir Create Leaseset veya Create Leaseset2 Mesajı olabileceğini unutmayın.

### Çevrimdışı Anahtarlarla Şifrelenmiş LS

Router'dan istemciye. Değişiklik yok. Kiralamalar (leases) 8-bayt zaman damgalarıyla gönderilir, döndürülen leaseSet bir LS2 olsa ve 4-bayt zaman damgalarına sahip olsa bile. Yanıtın bir Create Leaseset veya Create Leaseset2 Mesajı olabileceğini unutmayın.

### Notlar

İstemciden yönlendiriciye. Create Leaseset Mesajı yerine kullanılacak yeni mesaj.

### Meta LS2

- Router'ın depolama türünü ayrıştırabilmesi için, tür mesajda bulunmalıdır,
  ancak oturum yapılandırmasında router'a önceden aktarılmış olmadıkça.
  Ortak ayrıştırma kodu için, mesajın kendisinde bulunması daha kolaydır.

- Router'ın özel anahtarın türünü ve uzunluğunu bilmesi için,
  anahtar lease set'ten sonra olmalıdır, parser türü önceden
  oturum yapılandırmasında bilmiyor ise.
  Ortak ayrıştırma kodu için, bunu mesajın kendisinden bilmek daha kolaydır.

- İmzalama özel anahtarı, daha önce iptal için tanımlanmış ve kullanılmamış olan,
  LS2'de mevcut değildir.

### Format

Create Leaseset2 Mesajının mesaj türü 41'dir.

### Notlar

```
Session ID
  Type byte: Type of lease set to follow
             Type 1 is a LS
             Type 3 is a LS2
             Type 5 is a encrypted LS2
             Type 7 is a meta LS2
  LeaseSet: type specified above
  Number of private keys to follow (1 byte)
  Encryption Private Keys: For each public key in the lease set,
                           in the same order
                           (Not present for Meta LS2)
                           - Encryption type (2 bytes, big endian)
                           - Encryption key length (2 bytes, big endian)
                           - Encryption key (number of bytes specified)
```
### Hizmet Kaydı

- Minimum router sürümü 0.9.39'dur.
- Mesaj türü 40 ile ön sürüm 0.9.38'de mevcuttu ancak format değiştirildi.
  Tür 40 terk edildi ve desteklenmiyor.

### Format

- Şifrelenmiş ve meta LS'yi desteklemek için daha fazla değişiklik gerekli.

### Notlar

İstemciden yönlendiriciye. Yeni mesaj.

### Servis Listesi

- Router, bir destination'ın blinded olup olmadığını bilmesi gerekir.
  Eğer blinded ise ve secret veya per-client authentication kullanıyorsa,
  bu bilgilere de sahip olması gerekir.

- Yeni format b32 adresinin ("b33") Host Lookup işlemi
  router'a adresin blinded olduğunu söyler, ancak Host Lookup mesajında
  secret veya private key'i router'a iletmek için bir mekanizma yoktur.
  Host Lookup mesajını bu bilgiyi eklemek için genişletebilsek de,
  yeni bir mesaj tanımlamak daha temizdir.

- İstemcinin router'a programatik olarak bildirmesi için bir yola ihtiyacımız var.
  Aksi takdirde, kullanıcının her destination'ı manuel olarak yapılandırması gerekir.

Format

Bir istemci, körleştirilmiş bir hedefe mesaj göndermeden önce, "b33"'ü bir Host Lookup mesajında aramalı veya bir Blinding Info mesajı göndermelidir. Körleştirilmiş hedef bir gizli anahtar veya istemci başına kimlik doğrulama gerektiriyorsa, istemci bir Blinding Info mesajı göndermelidir.

Router bu mesaja yanıt göndermez.

### Notlar

Blinding Info Message için mesaj tipi 42'dir.

### Format

```
Session ID
  Flags:       1 byte
               Bit order: 76543210
               Bit 0: 0 for everybody, 1 for per-client
               Bits 3-1: Authentication scheme, if bit 0 is set to 1 for per-client, otherwise 000
                         000: DH client authentication (or no per-client authentication)
                         001: PSK client authentication
               Bit 4: 1 if secret required, 0 if no secret required
               Bits 7-5: Unused, set to 0 for future compatibility
  Type byte:   Endpoint type to follow
               Type 0 is a Hash
               Type 1 is a host name String
               Type 2 is a Destination
               Type 3 is a Sig Type and Signing Public Key
  Blind Type:  2 byte blinded sig type (big endian)
  Expiration:  4 bytes, big endian, seconds since epoch
  Endpoint:    Data as specified above
               For type 0: 32 byte binary hash
               For type 1: host name String
               For type 2: binary Destination
               For type 3: 2 byte sig type (big endian)
                           Signing Public Key (length as implied by sig type)
  Private Key: Only if flag bit 0 is set to 1
               A 32-byte ECIES_X25519 private key
  Secret:      Only if flag bit 4 is set to 1
               A secret String
```
### Anahtar Sertifikaları

- Minimum router sürümü 0.9.43'tür

### Yeni Ara Yapılar

### Yeni NetDB Türleri

"b33" hostname'lerinin sorgulanmasını desteklemek ve router'ın gerekli bilgiye sahip olmadığı durumlarda bir gösterge döndürmek için, Host Reply Message için aşağıdaki gibi ek sonuç kodları tanımlıyoruz:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
1-255 değerleri zaten hata olarak tanımlanmış durumda, bu nedenle geriye dönük uyumluluk sorunu bulunmuyor.

### Yeni İmza Türü

Router'dan istemciye. Yeni mesaj.

### Justification

Bir istemci, verilen bir Hash'in bir Meta LS'ye çözümleneceğini a priori olarak bilemez.

Bir Destination için leaseset araması Meta LS döndürürse, router özyinelemeli çözümlemeyi yapacaktır. Datagramlar için istemci tarafının bilmesine gerek yoktur; ancak protokolün SYN ACK'deki destination'ı kontrol ettiği streaming için, "gerçek" destination'ın ne olduğunu bilmesi gerekir. Bu nedenle yeni bir mesaja ihtiyacımız var.

### Usage

Router, gerçek hedef için bir önbellek tutar ve bu önbellek bir meta LS'den kullanılır. İstemci, bir meta LS'ye çözümlenen bir hedefe mesaj gönderdiğinde, router son kullanılan gerçek hedef için önbelleği kontrol eder. Önbellek boşsa, router meta LS'den bir hedef seçer ve leaseset'i arar. Leaseset arama işlemi başarılı olursa, router o hedefi önbelleğe ekler ve istemciye bir Meta Yönlendirme Mesajı gönderir. Bu işlem yalnızca bir kez yapılır, hedefin süresi dolup değiştirilmesi gerekmedikçe tekrarlanmaz. İstemci de gerektiğinde bilgiyi önbelleğe almalıdır. Meta Yönlendirme Mesajı her SendMessage'a yanıt olarak gönderilmez.

Router bu mesajı yalnızca 0.9.47 veya daha yüksek sürüme sahip istemcilere gönderir.

İstemci bu mesaja yanıt göndermez.

### Veritabanı Arama Mesajı

Meta Redirect Message için mesaj türü 43'tür.

### Değişiklikler

```
Session ID (2 bytes) The value from the Send Message.
  Message ID generated by the router (4 bytes)
  4 byte nonce previously generated by the client
               (the value from the Send Message, may be zero)
  Flags:       2 bytes, bit order 15...0
               Unused, set to 0 for future compatibility
               Bit 0: 0 - the destination is no longer meta
                      1 - the destination is now meta
               Bits 15-1: Unused, set to 0 for future compatibility
  Original Destination (387+ bytes)
  (following fields only present if flags bit 0 is 1)
  MFlags:      2 bytes
               Unused, set to 0 for future compatibility
               From the Meta Lease for the actual Destination
  Expiration:  4 bytes, big endian, seconds since epoch
               From the Meta Lease for the actual Destination
  Cost (priority) 1 byte
               From the Meta Lease for the actual Destination
  Actual (real) Destination (387+ bytes)
```
### Veritabanı Depolama Mesajı

Meta'nın nasıl oluşturulacağı ve destekleneceği, router'lar arası iletişim ve koordinasyon dahil olmak üzere, bu önerinin kapsamı dışındadır. İlgili 150 numaralı öneriye bakınız.

### Değişiklikler

Çevrimdışı imzalar, akışlı veya yanıtlanabilir datagramlarda doğrulanamaz. Aşağıdaki bölümlere bakınız.

## Private Key File Changes Required

Özel anahtar dosyası (eepPriv.dat) formatı spesifikasyonlarımızın resmi bir parçası değildir ancak [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) içinde belgelenmiştir ve diğer uygulamalar da bunu destekler. Bu, özel anahtarların farklı uygulamalara taşınabilirliğini sağlar.

Geçici genel anahtar ve çevrimdışı imzalama bilgilerini saklamak için değişiklikler gereklidir.

### Changes

```
If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key
    (length as specified by transient sig type)
```
### I2CP Seçenekleri

Aşağıdaki seçenekler için destek ekleyin:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Streaming Changes Required

Çevrimdışı imzalar şu anda streaming içinde doğrulanamıyor. Aşağıdaki değişiklik, çevrimdışı imzalama bloğunu seçeneklere ekliyor. Bu, bu bilgilerin I2CP aracılığıyla alınması gerekliliğini ortadan kaldırıyor.

### Oturum Yapılandırması

```
Add new option:
  Bit:          11
  Flag:         OFFLINE_SIGNATURE
  Option order: 4
  Option data:  Variable bytes
  Function:     Contains the offline signature section from LS2.
                FROM_INCLUDED must also be set.
                Expires timestamp
                (4 bytes, big endian, seconds since epoch, rolls over in 2106)
                Transient sig type (2 bytes, big endian)
                Transient signing public key (length as implied by sig type)
                Signature of expires timestamp, transient sig type,
                and public key, by the destination public key,
                length as implied by destination public key sig type.

  Change option:
  Bit:          3
  Flag:         SIGNATURE_INCLUDED
  Option order: Change from 4 to 5

  Add information about transient keys to the
  Variable Length Signature Notes section:
  The offline signature option does not needed to be added for a CLOSE packet if
  a SYN packet containing the option was previously acked.
  More info TODO
```
### Leaseset İstek Mesajı

- Alternatif olarak sadece bir bayrak eklemek ve geçici genel anahtarı I2CP aracılığıyla almak
  (Yukarıdaki Host Lookup / Host Reply Message bölümlerine bakın)

## Standart LS2 Başlığı

Çevrimdışı imzalar, yanıtlanabilir datagram işlemede doğrulanamaz. Çevrimdışı imzalı olduğunu belirtmek için bir flag gerekiyor ancak flag koyacak yer yok. Tamamen yeni bir protokol numarası ve format gerektirecek.

### İstek Değişken Leaseset Mesajı

```
Define new protocol 19 - Repliable datagram with options?
  - Destination (387+ bytes)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bits 1-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type,
    and public key, by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
  - Data
```
### Leaseset2 Mesajı Oluştur

- Alternatif olarak sadece bir bayrak eklemek ve geçici public key'i I2CP üzerinden almak
  (Yukarıdaki Host Lookup / Host Reply Message bölümlerine bakın)
- Artık bayrak byte'larımız olduğuna göre eklemeli miyiz başka seçenekler var mı?

## SAM V3 Changes Required

SAM, DESTINATION base 64'te çevrimdışı imzaları destekleyecek şekilde geliştirilmelidir.

### Gerekçe

```
Note that in the SESSION CREATE DESTINATION=$privkey,
  the $privkey raw data (before base64 conversion)
  may be optionally followed by the Offline Signature as specified in the
  Common Structures Specification.

  If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key (length as specified by transient sig type)
```
Çevrimdışı imzaların yalnızca STREAM ve RAW için desteklendiğini, DATAGRAM için desteklenmediğini unutmayın (yeni bir DATAGRAM protokolü tanımlayana kadar).

SESSION STATUS'un, tüm sıfırlardan oluşan bir İmzalama Özel Anahtarı ve SESSION CREATE'te sağlanan Çevrimdışı İmza verilerini tam olarak olduğu gibi döndüreceğini unutmayın.

Not: DEST GENERATE ve SESSION CREATE DESTINATION=TRANSIENT komutları, çevrimdışı imzalı bir hedef (destination) oluşturmak için kullanılamaz.

### Mesaj Türü

Sürümü 3.4'e yükselt, ya da tüm 3.2/3.3 özelliklerini gerektirmeden eklenebilsin diye 3.1/3.2/3.3'te bırak?

Diğer değişiklikler henüz belirlenmedi. Yukarıdaki I2CP Host Reply Message bölümüne bakın.

## BOB Changes Required

BOB, çevrimdışı imzaları ve/veya Meta LS'yi desteklemek için geliştirilmesi gerekecektir. Bu düşük öncelikli bir konudur ve muhtemelen hiçbir zaman belirtilmeyecek veya uygulanmayacaktır. SAM V3 tercih edilen arayüzdür.

## Publishing, Migration, Compatibility

LS2 (şifrelenmiş LS2 hariç), LS1 ile aynı DHT konumunda yayınlanır. LS2 farklı bir konumda olmadıkça, hem LS1 hem de LS2'yi yayınlamanın bir yolu yoktur.

Şifrelenmiş LS2, kör edilmiş anahtar türü ve anahtar verisinin hash'inde yayınlanır. Bu hash daha sonra LS1'deki gibi günlük "routing key" oluşturmak için kullanılır.

LS2 yalnızca yeni özellikler gerektiğinde kullanılır (yeni kripto, şifrelenmiş LS, meta, vb.). LS2 yalnızca belirtilen sürüm veya daha yüksek sürümlerde olan floodfill'lere yayınlanabilir.

LS2 yayınlayan sunucular, bağlanan istemcilerin LS2'yi desteklediğini bilirler. LS2'yi garlic içinde gönderebilirler.

İstemciler LS2'yi garlic'lerde yalnızca yeni kripto kullanıyorlarsa gönderirler. Paylaşılan istemciler LS1'i süresiz olarak mı kullanır? YAPILACAK: Hem eski hem yeni kriptoyu destekleyen paylaşılan istemciler nasıl sağlanır?

## Rollout

0.9.38, offline anahtarlar da dahil olmak üzere standart LS2 için floodfill desteği içerir.

0.9.39, LS2 ve Şifrelenmiş LS2 için I2CP desteği, sig type 11 imzalama/doğrulama, Şifrelenmiş LS2 için floodfill desteği (sig type 7 ve 11, çevrimdışı anahtarlar olmadan) ve LS2 şifreleme/şifre çözme (istemci başına yetkilendirme olmadan) içerir.

0.9.40 sürümünde müşteri başına yetkilendirme ile LS2 şifreleme/şifre çözme desteği, Meta LS2 için floodfill ve I2CP desteği, çevrimdışı anahtarlarla şifrelenmiş LS2 desteği ve şifrelenmiş LS2 için b32 desteği bulunması planlanmaktadır.

## Yeni DatabaseEntry türleri

Şifrelenmiş LS2 tasarımı, benzer tasarım hedeflerine sahip olan [Tor'un v3 gizli servis tanımlayıcıları](https://spec.torproject.org/rend-spec-v3)'ndan büyük ölçüde etkilenmiştir.
