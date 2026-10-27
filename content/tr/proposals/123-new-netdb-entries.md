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

Bu teklifin bazı bölümleri tamamlanmış olup 0.9.38 ve 0.9.39 sürümlerinde uygulanmıştır.   Ortak Yapılar, I2CP, I2NP ve diğer spesifikasyonlar   şimdi desteklenen değişiklikleri yansıtacak şekilde güncellenmiştir.

Tamamlanan bölümler hâlâ küçük revizyonlara tabidir.   Bu teklifin diğer bölümleri hâlâ geliştirme aşamasındadır   ve önemli revizyonlara tabidir.

Hizmet Arama (tür 9 ve 11) düşük önceliklidir ve   planlanmamıştır, ayrıca ayrı bir teklife ayrılabilir.

## Genel Bakış

Bu, aşağıdaki 4 teklifin bir güncellenmesi ve birleştirilmesidir:

- 110 LS2
- 120 Meta LS2 for massive multihoming
- 121 Encrypted LS2
- 122 Unauthenticated service lookup (anycasting)

Bu teklifler çoğunlukla bağımsızdır, ancak sağduyu açısından birkaç tanesi için   ortak bir biçim tanımlıyoruz ve kullanıyoruz.

Aşağıdaki teklifler kısmen ilişkilidir:

- 140 Invisible Multihoming (bu teklifle uyumsuz)
- 142 New Crypto Template (yeni simetrik şifreleme için)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 for Encrypted LS2
- 150 Garlic Farm Protocol
- 151 ECDSA Blinding

## Teklif

Bu teklif 5 yeni DatabaseEntry türü ve bunların   ağ veritabanına nasıl kaydedileceğini ve oradan nasıl alınacağını tanımlar,   ayrıca nasıl imzalanacaklarını ve bu imzaların nasıl doğrulanacağını da belirtir.

### Amaçlar

- Geriye dönük uyumlu
- LS2 eski tarz çoklu barındırmayla (multihoming) kullanılabilir
- Desteğin sağlanması için yeni şifreleme veya temel işlemler gerekmez
- Şifreleme ve imzalama arasındaki ayrımı koru; tüm mevcut ve gelecekteki sürümleri destekle
- İsteğe bağlı çevrimdışı imza anahtarlarını etkinleştir
- Parmak izini azaltmak için zaman damgalarının doğruluğunu azalt
- Hedefler için yeni şifreleme türlerini etkinleştir
- Büyük ölçekli çoklu barındırmayı (massive multihoming) etkinleştir
- Mevcut şifreli LS ile ilgili birçok sorunu düzelt
- Floodfill'ler tarafından görünürlüğü azaltmak için isteğe bağlı gizleme (blinding)
- Şifreleme, tek anahtarlı ve birden fazla iptal edilebilir anahtarlı modelleri destekler
- Çıkış vekilleri (outproxies), uygulama DHT önyüklemesi ve diğer kullanım alanları için hizmet arama
- 32 baytlık ikili hedef karmalarına (hash) dayanan hiçbir şeyi bozma, örneğin bittorrent
- Routerinfo'larda olduğu gibi, lease set'lere esneklik sağlamak için özellikler (properties) ekle
- Yayınlanan zaman damgasını ve değişken sona ermeyi başlığa koy, böylece içerik şifrelenmiş olsa bile çalışır (en erken lease'ten zaman damgası türetilmez)
- Tüm yeni türler mevcut lease set'lerle aynı DHT alanında ve aynı konumlarda yer alır, böylece kullanıcılar eski LS'den LS2'ye geçiş yapabilir veya LS2, Meta ve Şifreli arasında değişiklik yapabilir, hedefi veya karmayı değiştirmeden.
- Mevcut bir Hedef, hedefi veya karmayı değiştirmeden çevrimdışı anahtarlarla kullanılacak şekilde dönüştürülebilir veya çevrimiçi anahtarlara geri dönebilir.

### Amaçlar Dışı / Kapsam Dışı

- Yeni DHT döndürme algoritması veya paylaşılan rastgele sayı üretimi
- Yeni şifreleme türü ve bu yeni türü kullanan uçtan uca şifreleme şeması ayrı bir teklifte olur. Burada yeni bir şifreleme türü belirtilmez veya tartışmaz.
- Rİ'ler veya tünel oluşturma için yeni şifreleme. Bu ayrı bir teklifte olur.
- I2NP DLM / DSM / DSRM mesajlarının şifrelenmesi, iletilmesi ve alınması yöntemleri. Değişmiyor.
- Meta'nın nasıl üretileceği ve destekleneceği, dahil olmak üzere arka uç iç-router iletişimi, yönetimi, devreye alma ve koordinasyonu. Desteği I2CP'ye, i2pcontrol'e veya yeni bir protokole eklenebilir. Bu standartlaştırılmış olabilir veya olmayabilir.
- Daha uzun süreli tünellerin nasıl uygulanacağı ve yönetileceği veya mevcut tünellerin nasıl iptal edileceği. Bu son derece zordur ve bunu yapmadan makul bir şekilde kapatma mümkün değildir.
- Tehdit modeli değişiklikleri
- Çevrimdışı depolama biçimi veya verinin depolanması/alınması/paylaşılması yöntemleri.
- Uygulama ayrıntıları burada tartışılmaz ve her projeye bırakılır.

### Gerekçe

LS2, şifreleme türünü değiştirme ve gelecekteki protokol değişiklikleri için alanlar ekler.

Şifreli LS2, tüm lease'lerin asimetrik şifrelenmesini kullanarak mevcut şifreli LS ile ilgili birkaç güvenlik sorununu düzeltir.

Meta LS2, esnek, verimli, etkili ve büyük ölçekli çoklu barındırma sağlar.

Hizmet Kaydı ve Hizmet Listesi, ad arama ve DHT önyüklemesi gibi herhangi bir yere yayın (anycast) hizmetleri sağlar.

### NetDB Veri Türleri

Tür numaraları I2NP Veritabanı Arama/Depolama Mesajlarında kullanılır.

Uçtan uca sütunu, sorguların/yanıtların bir Hedefe Sarımsak Mesajında gönderilip gönderilmeyeceğini belirtir.

Mevcut türler:

| NetDB Veri | Arama Türü | Depolama Türü |
|------------|-------------|------------|
| herhangi | 0           | herhangi        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| keşif | 3           | DSRM       |
Yeni türler:

| NetDB Veri     | Arama Türü | Depolama Türü | Standart LS2 Başlığı? | Uçtan uca gönderildi mi? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | evet              | evet              |
| Şifreli LS2  | 1           | 5          | hayır               | hayır               |
| Meta LS2       | 1           | 7          | evet              | hayır               |
| Hizmet Kaydı | yok         | 9          | evet              | hayır               |
| Hizmet Listesi   | 4           | 11         | hayır               | hayır               |
### Notlar

- Arama türleri şu anda Veritabanı Arama Mesajında 3-2 bitleridir.  
  Ek türler 4. bitin kullanımını gerektirir.

- Eski yönlendiriciler tarafından Veritabanı Depolama Mesajı tür alanındaki üst bitlerin  
  dikkate alınmadığından, tüm depolama türleri tektir.  
  Bunu bir sıkıştırılmış RI yerine LS olarak ayrıştırılması başarısız olmasından ziyade LS olarak ayrıştırılmasını tercih ederiz.

- Tür, imza altındaki veride açık mı, örtük mü yoksa ikisi de değil mi olmalıdır?

### Arama/Depolama işlemi

Tür 3, 5 ve 7, standart lease set aramasına (tür 1) yanıt olarak döndürülebilir.   Tür 9, bir arama sonucunda asla döndürülmez.   Tür 11, yeni bir hizmet arama türüne (tür 11) yanıt olarak döndürülür.

Yalnızca tür 3, istemci-istemci Sarımsak mesajında gönderilebilir.

### Biçim

Tür 3, 7 ve 9 ortak bir biçime sahiptir::

```text
Standard LS2 Header
- as defined below

Type-Specific Part
- as defined below in each part

Standard LS2 Signature:
- Length as implied by sig type of signing key
```
Standart LS2 Başlığı

Tür Özel Bölüm

### Gizlilik/Güvenlik Hususları

Standart LS2 İmzası:

## Standart LS2 Başlığı

Tür 5 (Şifreli), bir Hedefle başlamaz ve farklı bir biçimdedir. Aşağıya bakın.

### Biçim

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
### Gerekçe

  - aşağıda tanımlandığı gibi

  - aşağıda her bölümde tanımlandığı gibi

  - İmza türüne göre dolaylı olarak belirlenen uzunlukta

- Yayınlanmamış/yayınlanmış: Veritabanı deposunu uçtan uca gönderirken,
  gönderen yönlendirici bu lease set'in başkalarına gönderilmemesini isteyebilir. Şu anda bu durumu korumak için sezgisel yöntemler kullanıyoruz.

### Sorunlar

- Yayınlanmış: Lease set'in 'sürümünü' belirlemek için gereken karmaşık mantığı değiştirir. Şu anda sürüm, en geç süresi dolan lease'in sona erme zamanıdır ve bir yayınlayıcı, yalnızca eski bir lease'i kaldıran bir lease set'i yayınlarken bu sona erme süresini en az 1ms artırması gerekir.

- Sona erer: Bir netdb girdisinin sona erme süresinin, son süresi dolan lease set'inden daha erken olmasını sağlar. LS2 için faydalı olmayabilir, çünkü lease set'lerin 11 dakikalık maksimum sona erme süresiyle kalması beklenir, ancak diğer yeni türler için gereklidir (aşağıdaki Meta LS ve Hizmet Kaydı'na bakın).

- Çevrimdışı anahtarlar, başlangıç/uygulama karmaşıklığını azaltmak için isteğe bağlıdır.

### Notlar

- Zaman damgası doğruluğunu daha da azaltabiliriz (10 dakika?) ancak sürüm numarası eklememiz gerekir. Bu çoklu barındırmayı bozabilir, sıra koruyan şifreleme yapmazsak? Muhtemelen zaman damgaları olmadan yapamayız.

- Alternatif: 3 baytlık zaman damgası (epoch / 10 dakika), 1 baytlık sürüm, 2 baytlık sona erme

- Tür veri/imza içinde açık mı yoksa örtük müdür? İmza için "Alan" sabitleri?

## Yeni DatabaseEntry türleri

### LeaseSet 2

Tür 11 (Hizmet Listesi), birkaç Hizmet Kaydının bir araya getirilmesidir ve farklı bir biçimdedir. Aşağıya bakın.

- Yönlendiriciler bir LS'yi saniyede birden fazla kez yayınlamamalıdır.  
  Yaparlarsa, daha önce yayınlanan LS'den 1 saniye daha fazla yapay olarak  
  yayınlanan zaman damgasını artırmalıdırlar.

TBD

    Standard LS flag (1)
Tür 3, 7 ve 9 standart LS2 başlığını kullanır, aşağıda belirtilmiştir:

    Standard LS2 type (3)
Mevcut LeaseSet'ten değişiklikler:

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Arama ile

    10 minutes, as in a regular LS.
Depolama ile

    Destination

### Biçim

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
### Gerekçe

- Yönlendirici uygulamaları, her seferinde doğrulamayı önlemek için geçici anahtarları ve imzayı önbelleğe alabilir. Özellikle floodfill'ler ve uzun süreli bağlantıların her iki ucundaki yönlendiriciler bundan faydalanabilir.

- Çevrimdışı anahtarlar ve imza yalnızca uzun ömürlü hedefler için uygundur,  
  yani sunucular, istemciler değil.

### Tartışma

Şurada depolama

Tipik sona erme

Yayınlayan

- Yayınlanan zaman damgası, sona erme zaman damgası, bayraklar ve özellikler ekle
- Şifreleme türünü ekle
- İptal anahtarını kaldır

Bu teklif, uçtan uca şifreleme anahtarı olarak lease set'teki ortak anahtarı kullanmaya devam eder ve   ortak anahtar alanını hedefte kullanmaz, şu an olduğu gibi. Şifreleme türü   hedef anahtar sertifikasında belirtilmez, 0 olarak kalır.

- Özellikler: Gelecekteki genişleme ve esneklik.  
  Kalan verinin ayrıştırılması için gerekli olabileceği için ilk sırada yer alır.

### Yeni Şifreleme Sorunları

Reddedilen alternatif, şifreleme türünü hedef anahtar sertifikasında belirtmektir,   hedefteki ortak anahtarı kullanmak ve lease set'teki ortak anahtarı   kullanmamak. Bunu yapmayı planlamıyoruz.

- Birden fazla şifreleme türü/ortak anahtar çifti  
  yeni şifreleme türlerine geçişi kolaylaştırmak içindir. Diğer yol  
  birden fazla lease set yayınlamaktır, muhtemelen aynı tünelleri kullanarak,  
  şu an DSA ve EdDSA hedefleri için yaptığımız gibi.  
  Bir tüneldeki gelen şifreleme türünün tanımlanması  
  mevcut oturum etiketi mekanizmasıyla yapılabilir,  
  ve/veya her anahtarla deneme şifre çözme. Gelen  
  mesajların uzunluğu da bir ipucu sağlayabilir.

- Gerçek ortak anahtarın konumu değişmez.
- Şifreleme türü veya ortak anahtar, Hedefi değiştirmeden değiştirilebilir.
- Kullanılmayan iptal alanını kaldırır
- Bu teklifteki diğer DatabaseEntry türleriyle temel uyumluluk
- Birden fazla şifreleme türünü destekler

- Ortak anahtarın ve şifreleme türünün konumu RouterInfo'dan farklıdır
- Lease set'te kullanılmayan ortak anahtarı korur
- Ağ genelinde uygulama gerektirir; alternatif olarak, deneysel  
  şifreleme türleri kullanılabilir, eğer floodfill'ler izin veriyorsa  
  (ancak deneysel imza türleri için destekle ilgili ilgili tekliflere 136 ve 137 bakın).  
  Alternatif teklif, deneysel şifreleme türleri için uygulamak ve test etmek daha kolay olabilir.

### Notlar

- Şifreleme türü, eğri, anahtar uzunluğu ve uçtan uca şemayı,  
  varsa KDF ve MAC'ı birlikte temsil eder.

- LS2'nin floodfill tarafından bilinmeyen şifreleme türleri için bile  
  ayrıştırılabilir ve doğrulanabilir olması için bir anahtar uzunluğu alanı ekledik.

- Önerilecek ilk yeni şifreleme türü  
  muhtemelen ECIES/X25519 olacaktır. Nasıl kullanılacağı uçtan uca  
  (ElGamal/AES+SessionTag'ın biraz değiştirilmiş bir versiyonu  
  veya tamamen yeni bir şey, örneğin ChaCha/Poly) bir veya daha fazla ayrı teklifte  
  belirtilecektir.  
  Ayrıca ECIES tekliflerine 144 ve 145 bakın.

### Şifreli LS2

LS2'nin faydaları:

- Lease'lerdeki 8 baytlık sona erme 4 bayta değiştirildi.

LS2'nin dezavantajları:

Bunun bir kısmı bu teklifin kapsamı dışındadır,   ancak henüz ayrı bir şifreleme teklifi olmadığından   şimdilik buraya notlar ekliyoruz.   Ayrıca ECIES tekliflerine 144 ve 145 bakın.

- Eğer iptal uygulamayı gerçekleştirirsek, bunu sıfır olan bir sona erme alanı veya sıfır lease'lerle yapabiliriz veya ikisiyle. Ayrı bir iptal anahtarı gerekmez.

Amaçlar:

    Standard LS flag (1)
Şifreli LS2, asla uçtan uca sarımsak mesajında gönderilmez.   Yukarıdaki gibi standart LS2'yi kullanın.

    Encrypted LS2 type (5)
Mevcut şifreli LeaseSet'ten değişiklikler:

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Arama ile

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Depolama ile

    Destination


### Tanımlar

Depolama konumu

Tipik sona erme

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

Yayınlayan

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

Şifreli LS2 için kullanılan kriptografik yapı taşlarına karşılık gelen aşağıdaki fonksiyonları tanımlıyoruz:

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


CSRNG(n)

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

H(p, d)

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

STREAM

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### Biçim

SIG

- Şifreleme anahtarları, sunucunun tercihine göre sıraya dizilir, en çok tercih edilen ilk sırada. Varsayılan istemci davranışı, desteklenen bir şifreleme türüne sahip ilk anahtarı seçmektir. İstemciler şifreleme desteği, göreli performans ve diğer faktörlere dayalı olarak başka seçim algoritmaları kullanabilirler.

DH

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

HKDF(salt, ikm, info, n)

Şifreli LS2 biçimi üç iç içe katmandan oluşur:

#### Katman 0 (dış)

Genel biçim şöyle görünür::

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Şifreli LS2'nin gizlendiğini unutmayın. Hedef başlıkta değildir. DHT depolama konumu SHA-256(imza türü || gizlenmiş ortak anahtar)'dır ve günlük olarak döner.

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

Yukarıda belirtilen standart LS2 başlığını KULLANMAZ.

    Length as implied by sig type

Tür

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Gizlenmiş Ortak Anahtar İmza Türü

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Gizlenmiş Ortak Anahtar

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Yayınlanan zaman damgası

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

Sona erer

    2 bytes, big endian

Bayraklar

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Geçici anahtar verisi

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Katman 1 (orta)

lenOuterCiphertext

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

outerCiphertext

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

İmza

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


Bayraklar

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Katman 2 (iç)

DH istemci kimlik doğrulama verisi

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

PSK istemci kimlik doğrulama verisi

    LeaseSet2 data for the given type.

    Includes the header and signature.


### Anahtar Gizleme Türetimi

innerCiphertext

Tür

#### Amaçlar

- Gizleme ekle
- Birden fazla imza türüne izin ver
- Yeni şifreleme temel işlemlerini gerektirme
- İsteğe bağlı olarak her alıcıya şifrele, iptal edilebilir
- Yalnızca Standart LS2 ve Meta LS2'nin şifrelenmesini destekle

#### Güvenlik

Veri

#### Tanımlar

Aşağıdaki şemayı anahtar gizleme için kullanıyoruz,   Ed25519 ve [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)'ya dayanır.   Re25519 imzaları Ed25519 eğrisi üzerinde, hash için SHA-512 kullanılarak yapılır.

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

Benzer tasarım hedeflerine sahip olsa da [Tor'un rend-spec-v3.txt ek A.2](https://spec.torproject.org/rend-spec-v3)'sini kullanmıyoruz, çünkü gizlenmiş ortak anahtarları asal-sıra alt grubunun dışında olabilir ve güvenlik etkileri bilinmiyor.

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

Bir gizleme şemasının güvenliği, alpha'nın dağılımının gizlenmemiş özel anahtarlarla aynı olması gerektiğini gerektirir. Ancak, bir Ed25519 özel anahtarını (imza türü 7) bir Red25519 özel anahtarına (imza türü 11) gizlerken dağılım farklıdır. [zcash bölüm 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) gereksinimlerini karşılamak için, "yeniden rastgeleleştirilmiş bir ortak anahtar ve bu anahtar altındaki imza(lar)ın, yeniden rastgeleleştirildiği anahtarı ortaya çıkarmaması" için Red25519 (imza türü 11) gizlenmemiş anahtarlar için de kullanılmalıdır. Mevcut hedefler için tür 7'yi kabul ediyoruz, ancak yeni şifrelenecek hedefler için tür 11 öneriyoruz.

    Convert a private key to public, as in Ed25519 (mulitply by G)

B

    A 32-byte random number known to those who know the destination.

L

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

DERIVE_PUBLIC(a)

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

alpha

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

GENERATE_ALPHA(destination, date, secret)

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

a

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

A

    Flip the order of the input bytes to little-endian

a'

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Gizleme Hesaplamaları

A'

LEOS2IP(x)

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
H*(x)

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
Her gün (UTC) yeni bir gizli alpha ve gizlenmiş anahtarlar oluşturulmalıdır.   Gizli alpha ve gizlenmiş anahtarlar aşağıdaki gibi hesaplanır.

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
GENERATE_ALPHA(destination, date, secret), tüm taraflar için:

#### İmzalama

BLIND_PRIVKEY(), lease set'i yayınlayan sahip için:

BLIND_PUBKEY(), lease set'i alan istemciler için:

A' hesaplamasının her iki yöntemi de aynı sonucu verir, gerektiği gibi.

Gizlenmemiş lease set, gizlenmemiş Ed25519 veya Red25519 imza özel anahtarıyla imzalanır ve gizlenmemiş Ed25519 veya Red25519 imza ortak anahtarıyla (imza türleri 7 veya 11) normal şekilde doğrulanır.

#### İmzalama/Doğrulama Hesaplamaları

İmza ortak anahtarı çevrimdışıysa, gizlenmemiş lease set, gizlenmemiş geçici Ed25519 veya Red25519 imza özel anahtarıyla imzalanır ve gizlenmemiş Ed25519 veya Red25519 geçici imza ortak anahtarıyla (imza türleri 7 veya 11) normal şekilde doğrulanır. Şifreli lease set'ler için çevrimdışı anahtarlar hakkında ek notlar için aşağıya bakın.

Şifreli lease set'in imzalanması için, gizlenmiş anahtarlarla imzalama ve doğrulama yapmak üzere [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)'ya dayanan Red25519 kullanıyoruz. Red25519 imzaları Ed25519 eğrisi üzerinde, hash için SHA-512 kullanılarak yapılır.

Red25519, aşağıda belirtilenler dışında standart Ed25519 ile aynıdır.

Şifreli lease set'in dış kısmı Red25519 anahtarlarını ve imzalarını kullanır.

Red25519, neredeyse Ed25519 ile aynıdır. İki fark vardır:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Red25519 özel anahtarları rastgele sayıdan üretilir ve ardından yukarıda tanımlandığı gibi L modunda azaltılmalıdır. Ed25519 özel anahtarları rastgele sayıdan üretilir ve ardından bayt 0 ve 31 için bit maskesi kullanılarak "kısaltılır". Bu, Red25519 için yapılmaz. Yukarıda tanımlanan GENERATE_ALPHA() ve BLIND_PRIVKEY() fonksiyonları mod L kullanarak uygun Red25519 özel anahtarlarını üretir.

```text
// same as in Ed25519
```
### Şifreleme ve İşleme

#### Alt kimlik bilgilerinin türetilmesi

Red25519'de, imzalama için r'nin hesaplanması ek rastgele veri kullanır ve özel anahtarın hash'i yerine ortak anahtar değerini kullanır. Rastgele veri nedeniyle, her Red25519 imzası farklıdır, aynı veriyle aynı anahtarla imzalansa bile.

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
İmzalama:

Doğrulama:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
Gizleme sürecinin bir parçası olarak, şifreli bir LS2'nin yalnızca karşılık gelen Hedefin imza ortak anahtarını bilen biri tarafından şifresinin çözülebileceğinden emin olmamız gerekir. Tam Hedef gerekli değildir. Bunu başarmak için, imza ortak anahtarından bir kimlik bilgisi türetiriz:

#### Katman 1 şifreleme

Kişiselleştirme dizesi, kimlik bilgisinin düz Hedef karması gibi bir DHT arama anahtarı olarak kullanılan herhangi bir hash ile çakışmadığından emin olur.

```text
outerInput = subcredential || publishedTimestamp
```
Verilen gizlenmiş anahtar için, ardından bir alt kimlik bilgisi türetebiliriz:

```text
outerSalt = CSRNG(32)
```
Alt kimlik bilgisi, aşağıdaki anahtar türetme süreçlerine dahil edilir, bu da bu anahtarları Hedefin imza ortak anahtarının bilinmesine bağlar.

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
İlk olarak, anahtar türetme sürecine girdi hazırlanır:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Katman 1 şifre çözme

Ardından, rastgele bir tuz oluşturulur:

```text
outerSalt = outerCiphertext[0:31]
```
Ardından, katman 1'i şifrelemek için kullanılan anahtar türetilir:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Son olarak, katman 1 düz metni şifrelenir ve serileştirilir:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Katman 2 şifreleme

Tuz, katman 1 şifreli metninden ayrıştırılır:

Ardından, katman 1'i şifrelemek için kullanılan anahtar türetilir:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Katman 2 şifre çözme

Son olarak, katman 1 şifreli metni şifresi çözülür:

İstemci yetkilendirmesi etkinleştirildiğinde, ``authCookie`` aşağıda açıklandığı gibi hesaplanır. İstemci yetkilendirmesi devre dışı bırakıldığında, ``authCookie`` sıfır uzunluklu bayt dizisidir.

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### İstemci bazında yetkilendirme

Şifreleme, katman 1'e benzer şekilde devam eder:

İstemci yetkilendirmesi etkinleştirildiğinde, ``authCookie`` aşağıda açıklandığı gibi hesaplanır. İstemci yetkilendirmesi devre dışı bırakıldığında, ``authCookie`` sıfır uzunluklu bayt dizisidir.

#### DH istemci yetkilendirmesi

Şifre çözme, katman 1'e benzer şekilde devam eder:

Bir Hedef için istemci yetkilendirmesi etkinleştirildiğinde, sunucu şifreli LS2 verisinin şifresini çözmek için yetkilendirdiği istemcilerin bir listesini tutar. İstemci başına depolanan veri, yetkilendirme mekanizmasına bağlıdır ve her istemcinin güvenli bir dış bant mekanizmasıyla sunucuya gönderdiği bazı anahtar malzemesi biçimini içerir.

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
İstemci bazında yetkilendirme için iki alternatif vardır:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Her istemci bir DH anahtar çifti ``[csk_i, cpk_i]`` üretir ve ortak anahtar ``cpk_i``'yi sunucuya gönderir.

Sunucu işleme ^^^^^^^^^^^^^^^^^ Sunucu yeni bir ``authCookie`` ve geçici bir DH anahtar çifti üretir:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Ardından her yetkili istemci için, sunucu ``authCookie``'yi ortak anahtarına şifreler:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Paylaşılan gizli anahtar istemci yetkilendirmesi

Sunucu her ``[clientID_i, clientCookie_i]`` ikilisini katman 1'e yerleştirir, ``epk`` ile birlikte.

İstemci işleme ^^^^^^^^^^^^^^^^^ İstemci özel anahtarını kullanarak beklenen istemci tanımlayıcısı ``clientID_i``, şifreleme anahtarı ``clientKey_i`` ve şifreleme IV'si ``clientIV_i``'yi türetir:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Ardından istemci, ``clientID_i`` içeren bir giriş aramak için katman 1 yetkilendirme verisini tarar. Eşleşen bir giriş varsa, istemci şifresini çözerek ``authCookie``'yi elde eder:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Her istemci 32 baytlık gizli bir anahtar ``psk_i`` üretir ve sunucuya gönderir. Alternatif olarak, sunucu gizli anahtarı üretebilir ve bir veya daha fazla istemciye gönderebilir.

Sunucu işleme ^^^^^^^^^^^^^^^^^ Sunucu yeni bir ``authCookie`` ve tuz üretir:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Ardından her yetkili istemci için, sunucu ``authCookie``'yi paylaşılan gizli anahtarına şifreler:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Güvenlik hususları

Sunucu her ``[clientID_i, clientCookie_i]`` ikilisini katman 1'e yerleştirir, ``authSalt`` ile birlikte.

İstemci işleme ^^^^^^^^^^^^^^^^^ İstemci paylaşılan gizli anahtarını kullanarak beklenen istemci tanımlayıcısı ``clientID_i``, şifreleme anahtarı ``clientKey_i`` ve şifreleme IV'si ``clientIV_i``'yi türetir:

Ardından istemci, ``clientID_i`` içeren bir giriş aramak için katman 1 yetkilendirme verisini tarar. Eşleşen bir giriş varsa, istemci şifresini çözerek ``authCookie``'yi elde eder:

Yukarıdaki istemci yetkilendirme mekanizmalarının her ikisi de istemci üyeliği için gizlilik sağlar. Yalnızca Hedefi bilen bir varlık, herhangi bir anda kaç istemcinin abone olduğunu görebilir, ancak hangi istemcilerin eklendiğini veya iptal edildiğini izleyemez.

- Güvenlik için her şeyi şifrele
- Sadece AES ile değil, güvenli şifrele
- Her alıcıya şifrele

Sunucular, istemcilerin listedeki konumlarını öğrenmelerini ve diğer istemcilerin ne zaman eklendiğini veya iptal edildiğini çıkarsamalarını önlemek için her seferinde şifreli LS2 oluşturduklarında istemcilerin sırasını rastgeleleştirmelidir.

- Depolama ve alım için gerekli düz metin bilgilerini içeren dış katman.
- İstemci kimlik doğrulamasını işleyen orta katman.
- Gerçek LS2 verisini içeren iç katman.

Bir sunucu, yetkilendirme verisi listesine rastgele girişler ekleyerek abone olan istemci sayısını gizlemeyi seçebilir.

- Gizlenmemiş hedefteki imza ortak anahtarı  
  Ed25519 (imza türü 7) veya Red25519 (imza türü 11) olmalıdır;  
  başka imza türleri desteklenmez
- İmza ortak anahtarı çevrimdışıysa, geçici imza ortak anahtarı da Ed25519 olmalıdır
- Gizleme hesapsal olarak basit olmalıdır
- Mevcut kriptografik temel işlemleri kullan
- Gizlenmiş ortak anahtarlar geri gizlenemez olmalıdır
- Gizlenmiş ortak anahtarlar Ed25519 eğrisi üzerinde ve asal-sıra alt grubunda olmalıdır
- Gizlenmiş ortak anahtarı türetmek için hedefin imza ortak anahtarını bilmek gerekir  
  (tam hedef gerekli değildir)
- İsteğe bağlı olarak gizlenmiş ortak anahtarı türetmek için ek bir gizli anahtar sağla

DH istemci yetkilendirmesinin avantajları ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Şemanın güvenliği, istemci anahtar malzemesinin dış bant değiş tokuşuna tamamen bağlı değildir. İstemcinin özel anahtarı cihazından asla çıkmaz, bu nedenle dış bant değiş tokuşunu ele geçirebilen ancak DH algoritmasını kıramayan bir düşman, şifreli LS2'yi çözemeyecek veya istemcinin erişiminin ne kadar süreyle verildiğini belirleyemeyecektir.

### Base 32 Adreslerle Şifreli LS

DH istemci yetkilendirmesinin dezavantajları ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PSK istemci yetkilendirmesinin avantajları ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

### Çevrimdışı Anahtarlarla Şifreli LS

PSK istemci yetkilendirmesinin dezavantajları ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Teklif 149'a bakın.

Compact announce yanıtları 32 bayt olduğu için bittorrent için şifreli LS2 kullanamazsınız. 32 bayt sadece karmayı içerir. Lease set'in şifreli olduğunu veya imza türlerini belirten bir alan yoktur.

### Notlar

- N istemci için sunucu tarafında N + 1 DH işlemi gerektirir.
- İstemci tarafında bir DH işlemi gerektirir.
- İstemcinin gizli anahtarı üretmesini gerektirir.

- DH işlemi gerektirmez.
- Sunucunun gizli anahtarı üretmesine izin verir.
- İstendiği takdirde sunucunun aynı anahtarı birden fazla istemciyle paylaşmasına izin verir.

- Şemanın güvenliği, istemci anahtar malzemesinin dış bant değiş tokuşuna kritik olarak bağlıdır. Belirli bir istemci için değiş tokuşu ele geçiren bir düşman, istemcinin yetkilendirildiği herhangi bir sonraki şifreli LS2'yi çözebilir ve ayrıca istemcinin erişiminin ne zaman iptal edildiğini belirleyebilir.

- Şifreli lease set'ler kullanan bir hizmet, şifreli sürümü floodfill'lere yayınlar. Ancak verimlilik için, kimlik doğrulamasından sonra (örneğin beyaz liste ile) istemcilere sarılmış sarımsak mesajında şifrelenmemiş lease set'ler gönderir.

- Floodfill'ler, kötüye kullanımı önlemek için maksimum boyutu makul bir değere sınırlayabilir.

### Meta LS2

Çevrimdışı anahtarlarla şifreli lease set'ler için, gizlenmiş özel anahtarlar da her gün için çevrimdışı oluşturulmalıdır.

İsteğe bağlı çevrimdışı imza bloğu şifreli lease set'in açık metin kısmında olduğundan, floodfill'eri tarayan herkes bu lease set'i (ancak şifresini çözmeden) birkaç gün boyunca izlemek için kullanabilir. Bunu önlemek için, anahtar sahibi her gün için yeni geçici anahtarlar üretmelidir. Hem geçici hem de gizlenmiş anahtarlar önceden üretilebilir ve toplu olarak yönlendiriciye teslim edilebilir.

Bu teklifte, birden fazla geçici ve gizlenmiş anahtarı paketlemek ve istemciye veya yönlendiriciye sağlamak için bir dosya biçimi tanımlanmamıştır. Çevrimdışı anahtarlarla şifreli lease set'leri desteklemek için bu teklifte bir I2CP protokolü geliştirilmesi tanımlanmamıştır.

Bu, çoklu barındırmayı değiştirmek için kullanılır. Herhangi bir lease set gibi, bu da oluşturucusu tarafından imzalanır. Bu, hedef karmalarının kimliği doğrulanmış bir listesidir.

Meta LS2, bir ağaç yapısının en üstü ve olası ara düğümleridir. Bir LS, LS2 veya başka bir Meta LS2'ye işaret eden bir dizi girdi içerir ve büyük ölçekli çoklu barındırmayı destekler. Bir Meta LS2, LS, LS2 ve Meta LS2 girişlerinin karışımını içerebilir. Ağacın yaprakları her zaman bir LS veya LS2'dir. Ağaç bir DAG'dır; döngülere izin verilmez; aramalar yapan istemciler döngüleri tespit etmeli ve takip etmeyi reddetmelidir.

Meta LS2'nin standart bir LS veya LS2'den çok daha uzun bir sona erme süresi olabilir. En üst seviyenin yayın tarihinden birkaç saat sonra sona ermesi olabilir. Maksimum sona erme süresi floodfill'ler ve istemciler tarafından zorlanır ve TBD'dir.

Meta LS2'nin kullanım durumu büyük ölçekli çoklu barındırmadır, ancak LS veya LS2 ile şu anda sağlanandan daha fazla, yönlendiricilerin lease set'lerle korelasyonunu (yönlendirici yeniden başlatma zamanında) koruma sağlamaz. Bu, muhtemelen korelasyon korumasına ihtiyaç duymayan "facebook" kullanım durumuyla eşdeğerdir. Bu kullanım durumu muhtemelen çevrimdışı anahtarlara ihtiyaç duyar, bu anahtarlar ağaçtaki her düğümde standart başlıkta sağlanır.

Yaprak yönlendiriciler, ara ve ana Meta LS imzalayanlar arasındaki arka uç protokolü burada belirtilmemiştir. Gereksinimler son derece basittir - sadece eşin çalışır durumda olduğunu doğrulamak ve birkaç saatte bir yeni bir LS yayınlamak. Tek karmaşıklık, başarısızlık durumunda en üst seviye veya ara seviye Meta LS'ler için yeni yayıncılar seçmektir.

Birden fazla yönlendiriciden lease'lerin birleştirilip, imzalanıp, tek bir lease set'te yayınlandığı karışık lease set'ler, teklif 140, "görünmez çoklu barındırma"da belgelenmiştir. Bu teklif, akış bağlantılarının tek bir yönlendiriciye "sıkı" olmayacağı için yazılı olduğu gibi uygulanamaz, http://zzz.i2p/topics/2335 adresine bakın.

Görünmez çoklu barındırma için arka uç protokolü ve yönlendirici ile istemci iç yapısıyla etkileşim oldukça karmaşık olacaktır.

    Standard LS flag (1)
En üst seviye Meta LS için floodfill'in aşırı yüklenmesini önlemek için, sona erme süresi en az birkaç saat olmalıdır. İstemciler en üst seviye Meta LS'yi önbelleğe almalı ve süresi dolmamışsa yeniden başlatmalarda kalıcı hale getirmelidir.

    Meta LS2 type (7)
Ağaçta dolaşmak için bazı algoritmalar tanımlamamız gerekiyor, dahil olmak üzere yedekleme, böylece kullanım dağıtılmış olur. Karma mesafesi, maliyeti ve rastgelelik fonksiyonu. Bir düğümde hem LS veya LS2 hem de Meta LS varsa, bu lease set'lerin ne zaman kullanılmasına izin verildiğini ve ne zaman ağaçta dolaşmaya devam edilmesi gerektiğini bilmemiz gerekir.

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Arama ile

    Hours. Max 18.2 hours (65535 seconds)
Depolama ile

    "master" Destination or coordinator, or intermediate coordinators

### Biçim

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
Depolama konumu

### Notlar

- Şifre çözmeden sonra, iç zaman damgasının ve sona ermenin üst düzeydekilerle eşleştiğinden emin olmak için birkaç kontrol yapılmalıdır.

- ChaCha20, AES yerine seçildi. AES donanım desteği mevcutsa hızlar benzer olsa da, düşük uç ARM cihazlarında olduğu gibi AES donanım desteği mevcut olmadığında ChaCha20 2.5-3 kat daha hızlıdır.

- Hız konusunda keyed BLAKE2b kullanmak kadar endişelenmiyoruz. En büyük n ihtiyacımızı karşılayacak kadar büyük bir çıktı boyutuna sahiptir (veya istenen anahtar başına bir kez çağrılabilir bir sayaç argümanı ile). BLAKE2b SHA-256'dan çok daha hızlıdır ve keyed-BLAKE2b toplam hash fonksiyonu çağrı sayısını azaltır. Ancak, diğer nedenlerle BLAKE2b'ye geçmeyi öneren teklif 148'e bakın. [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html) bölümüne bakın.

### Hizmet Kaydı

Tipik sona erme

Yayınlayan

TBD

    n/a, see Service List
Tür 3, 7 ve 9 standart LS2 başlığını kullanır, aşağıda belirtilmiştir:

    Service Record type (9)
Mevcut LeaseSet'ten değişiklikler:

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Arama ile

    Hours. Max 18.2 hours (65535 seconds)
Depolama ile

    Destination

### Biçim

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Notlar

- expires tamamen sıfırsa, floodfill kaydı iptal etmeli ve artık hizmet listesine dahil etmemelidir.

- Depolama: floodfill bu kayıtların depolanmasını sıkı biçimde sınırlandırabilir ve hash başına depolanan kayıt sayısını ve bunların sona erme süresini kısıtlayabilir. Hash'lerin bir izin listesi de kullanılabilir.

Aynı hash'teki başka bir netdb tipi önceliğe sahiptir; bu nedenle bir service record, bir LS/RI'ı asla geçersiz hale getiremez, ancak bir LS/RI, o hash'taki tüm service record'ları geçersiz hale getirir.

### Hizmet Listesi

Bu, bir LS2'ye hiç benzemiyor ve farklı bir format kullanıyor.

Service list, floodfill tarafından oluşturulur ve imzalanır. Kimlik doğrulaması yapılmamıştır, çünkü herhangi biri bir Service Record'u floodfill'a yayınlayarak bir service'e katılabilir.

Bir Service List, tam Service Records değil, Short Service Records içerir. Bunlar imzalar içerir ancak tam destination'lar değil yalnızca hash'ler içerir; bu nedenle tam destination olmadan doğrulanamazlar.

Hizmet listelerinin güvenliği (varsa) ve arzu edilirliği henüz belirlenmemiştir. Floodfill'ler yayını ve sorguları bir hizmet beyaz listesiyle sınırlayabilir, ancak bu beyaz liste uygulamaya veya operatör tercihine göre değişebilir. Uygulamalar arasında ortak, temel bir beyaz liste üzerinde uzlaşmaya varmak mümkün olmayabilir.

Hizmet adı yukarıdaki hizmet kaydına dahil edilirse, floodfill operatörleri itiraz edebilir; yalnızca hash dahil edilirse doğrulama olmaz ve bir hizmet kaydı diğer herhangi bir netdb türünün önüne "geçebilir" ve floodfill içinde saklanabilir.

TBD

    Service List lookup type (11)
Tür 3, 7 ve 9 standart LS2 başlığını kullanır, aşağıda belirtilmiştir:

    Service List type (11)
Mevcut LeaseSet'ten değişiklikler:

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Arama ile

    Hours, not specified in the list itself, up to local policy
Depolama ile

    Nobody, never sent to floodfill, never flooded.

### Biçim

Şifreli LS2 biçimi üç iç içe katmandan oluşur:

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
Service List'in imzasını doğrulamak için:

- hizmet adının hash'ini başa ekle
- oluşturucunun hash'ini kaldır
- Değiştirilmiş içeriğin imzasını kontrol et

Her Short Service Record'un imzasını doğrulamak için:

- Hedefi getir
- (yayınlanan zaman damgası + expires + flags + port + hizmet adının hash'i) imzasını kontrol et

Her İptal Kaydının imzasını doğrulamak için:

- Destination getir
- (yayınlanan timestamp + 4 sıfır bayt + flags + port + hizmet adının Hash'i) imzasını kontrol et

### Notlar

- Bilinmeyen imza türlerini destekleyebilmek için sig type yerine imza uzunluğunu kullanıyoruz.

- Bir hizmet listesinin son kullanma tarihi yoktur; alıcılar politikaya veya bireysel kayıtların sona ermesine dayanarak kendi kararlarını verebilir.

- Service List'ler flood edilmez, yalnızca tek tek Service Record'lar flood edilir. Her floodfill bir Service List oluşturur, imzalar ve önbelleğe alır. Floodfill, önbellek süresi ile hizmet ve iptal kayıtlarının maksimum sayısı için kendi politikasını kullanır.

## Ortak Yapılar Spesifikasyonunda Gerekli Değişiklikler

### Anahtar Sertifikaları

Bu önerinin kapsamı dışındadır. ECIES 144 ve 145 numaralı önerilere ekleyin.

### Yeni Ara Yapılar

Lease2, MetaLease, LeaseSet2Header ve OfflineSignature için yeni yapılar eklendi. 0.9.38 sürümünden itibaren geçerlidir.

### Yeni NetDB Türleri

Her yeni leaseset türü için yukarıdakilerden alınan yapıları ekleyin. LeaseSet2, EncryptedLeaseSet ve MetaLeaseSet için 0.9.38 sürümünden itibaren geçerlidir. Service Record ve Service List için ise ön hazırlık aşamasındadır ve planlanmamıştır.

### Yeni İmza Türü

RedDSA_SHA512_Ed25519 Tip 11'i ekleyin. Açık anahtar 32 bayttır; özel anahtar 32 bayttır; hash 64 bayttır; imza 64 bayttır.

## Şifreleme Spesifikasyonunda Değişiklikler Gerekli

Bu önerinin kapsamı dışındadır. 144 ve 145 numaralı önerilere bakın.

## Gerekli I2NP Değişiklikleri

Not ekleyin: LS2 yalnızca minimum sürüme sahip floodfill'lere yayınlanabilir.

### Veritabanı Arama Mesajı

Servis listesi arama türünü ekleyin.

### Değişiklikler

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Veritabanı Saklama Mesajı

Tüm yeni store türlerini ekleyin.

### Değişiklikler

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
## I2CP Değişiklikleri Gerekli

### I2CP Seçenekleri

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
### Oturum Yapılandırması

Çevrimdışı imzalar için i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey ve i2cp.leaseSetOfflineSignature seçeneklerinin gerekli olduğunu ve imzanın geçici imzalama özel anahtarıyla atıldığını unutmayın.

### Leaseset İstek Mesajı

Router'dan istemciye. Değişiklik yok. Lease'ler, döndürülen leaseSet 4 baytlık zaman damgalarına sahip bir LS2 olsa bile 8 baytlık zaman damgalarıyla gönderilir. Yanıtın bir Create Leaseset veya Create Leaseset2 Message olabileceği unutulmamalıdır.

### Değişken Leaseset Mesajı Talebi

Router'dan istemciye. Değişiklik yok. Lease'ler, döndürülen leaseSet 4 baytlık zaman damgalarına sahip bir LS2 olsa bile 8 baytlık zaman damgalarıyla gönderilir. Yanıtın bir Create Leaseset veya Create Leaseset2 Message olabileceği unutulmamalıdır.

### Leaseset2 Mesajı Oluştur

İstemciden router'a. Create Leaseset Message yerine kullanılacak yeni mesaj.

### Gerekçe

- Router'ın store türünü ayrıştırabilmesi için, oturum yapılandırmasında önceden router'a iletilmedikçe türün mesajda olması gerekir.
  Ortak ayrıştırma kodu için türün mesajın kendisinde olması daha kolaydır.

- router'ın private key'in türünü ve uzunluğunu bilmesi için,
  private key lease set'ten sonra olmalıdır; ancak parser türü session config içinde önceden biliyorsa bu gerekmez.
  Ortak ayrıştırma kodu için bunu mesajın kendisinden bilmek daha kolaydır.

- Daha önce iptal için tanımlanmış ve kullanılmamış olan imzalama özel anahtarı LS2'de yer almaz.

### Mesaj Türü

Create Leaseset2 Message için mesaj türü 41'dir.

### Biçim

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
### Notlar

- Minimum router sürümü 0.9.39'dur.
- Mesaj tipi 40 içeren ön sürüm 0.9.38'deydi ancak format değiştirildi.
  Tip 40 terk edildi ve desteklenmiyor.

### Sorunlar

- Şifrelenmiş ve meta LS desteği için daha fazla değişiklik gereklidir.

### Blinding Bilgi Mesajı

İstemciden router'a. Yeni mesaj.

### Gerekçe

- Router, bir hedefin blinded olup olmadığını bilmelidir.
  Blinded ise ve bir secret veya istemci başına kimlik doğrulama kullanıyorsa,
  bu bilgiye de sahip olması gerekir.

- Yeni formatlı bir b32 adresinin ("b33") Host Lookup işlemi,
  router'a adresin blinded olduğunu söyler, ancak Host Lookup mesajında
  secret veya private key'i router'a aktaracak bir mekanizma yoktur.
  Host Lookup mesajını bu bilgiyi ekleyecek şekilde genişletebilsek de,
  yeni bir mesaj tanımlamak daha temizdir.

- Client'ın router'a bildirmesi için programatik bir yola ihtiyacımız var.
  Aksi takdirde kullanıcı her destination'ı manuel olarak yapılandırmak zorunda kalırdı.

### Kullanım

Bir istemci körleştirilmiş bir hedefe mesaj göndermeden önce, "b33"ü bir Host Lookup mesajında aramalı ya da bir Blinding Info mesajı göndermelidir. Körleştirilmiş hedef bir sır veya istemci başına kimlik doğrulama gerektiriyorsa, istemci bir Blinding Info mesajı göndermelidir.

Router bu mesaja yanıt göndermez.

### Mesaj Türü

Blinding Info Message için mesaj türü 42'dir.

### Biçim

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
### Notlar

- Minimum router sürümü 0.9.43

### Sorunlar

### Host Yanıt Mesajı (enc)

b33 hostname aramalarını desteklemek ve router gerekli bilgiye sahip değilse bir gösterge döndürmek için Host Reply Message için ek sonuç kodlarını şu şekilde tanımlıyoruz:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
1-255 arasındaki değerler zaten hata olarak tanımlandığından geriye dönük uyumluluk sorunu yoktur.

### Meta Yönlendirme Mesajı

Router'dan client'a. Yeni mesaj.

### Gerekçe

Bir istemci, belirli bir Hash'in bir Meta LS'ye çözümleneceğini önceden bilemez.

Bir Destination için leaseset araması bir Meta LS döndürürse, router özyinelemeli çözümlemeyi yapacaktır. Datagramlar için istemci tarafının bilmesi gerekmez; ancak protokolün SYN ACK içindeki hedefi kontrol ettiği streaming için "gerçek" hedefin ne olduğu bilinmelidir. Bu nedenle yeni bir mesaja ihtiyaç vardır.

### Kullanım

Router, bir meta LS üzerinden kullanılan gerçek destination için bir önbellek tutar. İstemci, bir meta LS'ye çözümlenen bir destination'a mesaj gönderdiğinde, router önbellekte en son kullanılan gerçek destination'ı kontrol eder. Önbellek boşsa, router meta LS'den bir destination seçer ve leaseSet'i arar. leaseSet araması başarılı olursa, router bu destination'ı önbelleğe ekler ve istemciye bir Meta Redirect Message gönderir. Destination'ın süresi dolup değiştirilmesi gerekmediği sürece bu yalnızca bir kez yapılır. İstemci de gerekirse bilgiyi önbelleğe almalıdır. Meta Redirect Message, her SendMessage'a yanıt olarak GÖNDERİLMEZ.

Router bu mesajı yalnızca 0.9.47 veya daha yüksek sürüme sahip istemcilere gönderir.

İstemci bu mesaja bir yanıt göndermez.

### Mesaj Türü

Meta Redirect Message için mesaj türü 43'tür.

### Biçim

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
### Meta desteği için değişiklikler

Meta'nın nasıl oluşturulacağı ve destekleneceği, router'lar arası iletişim ve koordinasyon dahil olmak üzere, bu önerinin kapsamı dışındadır. İlgili 150 numaralı öneriye bakın.

### Offline Keys desteği için değişiklikler

Offline imzalar streaming veya repliable datagramlarda doğrulanamaz. Aşağıdaki bölümlere bakın.

## Private Key File Değişiklikleri Gereklidir

Özel anahtar dosyası (eepPriv.dat) biçimi spesifikasyonlarımızın resmî bir parçası değildir, ancak [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) içinde belgelenmiştir ve diğer uygulamalar da bunu destekler. Bu, özel anahtarların farklı uygulamalara taşınabilir olmasını sağlar.

Geçici açık anahtarı ve çevrimdışı imzalama bilgilerini saklamak için değişiklikler gereklidir.

### Değişiklikler

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
### Özel Anahtar Dosyası CLI Değişiklikleri Gerekli

Aşağıdaki seçenekler için destek ekleyin:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Akışta Yapılması Gereken Değişiklikler

Çevrimdışı imzalar şu anda streaming içinde doğrulanamaz. Aşağıdaki değişiklik, seçeneklere çevrimdışı imzalama bloğunu ekler. Bu, bu bilginin I2CP üzerinden alınması gerekliliğini ortadan kaldırır.

### Değişiklikler

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
### Notlar

- Alternatif olarak yalnızca bir bayrak eklemek ve geçici açık anahtarı I2CP aracılığıyla almak da mümkündür
  (Yukarıdaki Host Lookup / Host Reply Message bölümlerine bakın)

## Yanıtlanabilir Datagramlarda Gerekli Değişiklikler

Çevrimdışı imzalar, yanıtlanabilir datagram işlemesinde doğrulanamaz. Çevrimdışı imzalandığını belirtmek için bir flag gerekir ancak flag'in konulacağı bir yer yok. Tamamen yeni bir protokol numarası ve biçimi gerektirecektir.

### Değişiklikler

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
### Notlar

- Alternatif olarak yalnızca bir flag eklenebilir ve geçici açık anahtar I2CP üzerinden alınabilir
  (Yukarıdaki Host Lookup / Host Reply Message bölümlerine bakınız)
- Artık flag baytlarımız olduğuna göre eklememiz gereken başka seçenekler var mı?

## SAM V3 İçin Gerekli Değişiklikler

SAM, DESTINATION base 64 içindeki çevrimdışı imzaları desteklemek üzere geliştirilmelidir.

### Değişiklikler

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
Çevrimdışı imzaların yalnızca STREAM ve RAW için desteklendiğine, DATAGRAM için desteklenmediğine dikkat edilmelidir (yeni bir DATAGRAM protokolü tanımlanana kadar).

SESSION STATUS'un, tümü sıfırlardan oluşan bir Signing Private Key ve SESSION CREATE içinde sağlanan Offline Signature verisini tam olarak aynı şekilde döndüreceğini unutmayın.

DEST GENERATE ve SESSION CREATE DESTINATION=TRANSIENT'ın çevrimdışı imzalanmış bir destination oluşturmak için kullanılamayacağını unutmayın.

### Sorunlar

Sürüm 3.4'e mi yükseltilsin, yoksa tüm 3.2/3.3 unsurlarını gerektirmeden eklenebilmesi için 3.1/3.2/3.3 olarak mı bırakılsın?

Diğer değişiklikler TBD. Yukarıdaki I2CP Host Reply Message bölümüne bakın.

## Gerekli BOB Değişiklikleri

BOB'un offline imzaları ve/veya Meta LS'yi desteklemesi için geliştirilmesi gerekir. Bu düşük önceliklidir ve muhtemelen hiçbir zaman belirtilmeyecek veya uygulanmayacaktır. SAM V3 tercih edilen arayüzdür.

## Yayınlama, Geçiş, Uyumluluk

LS2 (şifrelenmiş LS2 dışında), LS1 ile aynı DHT konumunda yayımlanır. LS2 farklı bir konumda olmadığı sürece hem bir LS1 hem de bir LS2 yayımlamanın bir yolu yoktur.

Şifrelenmiş LS2, blinded key type ve key data'nın hash'i üzerinde yayımlanır. Bu hash daha sonra, LS1'de olduğu gibi, günlük "routing key"i oluşturmak için kullanılır.

LS2 yalnızca yeni özellikler gerektiğinde (yeni kripto, şifrelenmiş LS, meta vb.) kullanılır. LS2 yalnızca belirtilen sürüm veya daha yüksek sürümdeki floodfill'lara yayımlanabilir.

LS2 yayınlayan sunucular, bağlanan tüm istemcilerin LS2'yi desteklediğini bilirdi. LS2'yi garlic içinde gönderebilirlerdi.

Clients, sadece yeni crypto kullanılıyorsa garlic'lerde LS2 göndermiş olacaktır. Shared clients LS1'i süresiz kullanacak mı? TODO: Hem eski hem de yeni crypto'yu destekleyen shared clients nasıl elde edilir?

## Kullanıma sunma

0.9.38, offline anahtarlar da dahil olmak üzere standart LS2 için floodfill desteği içerir.

0.9.39, LS2 ve Encrypted LS2 için I2CP desteği, sig tipi 11 imzalama/doğrulama, Encrypted LS2 için floodfill desteği (sig tipi 7 ve 11, çevrimdışı anahtarlar olmadan) ve LS2'yi şifreleme/şifre çözme (istemci başına yetkilendirme olmadan) içerir.

0.9.40 sürümünün, istemci başına yetkilendirme ile LS2'yi şifreleme/şifresini çözme desteğini, Meta LS2 için floodfill ve I2CP desteğini, çevrimdışı anahtarlarla şifrelenmiş LS2 desteğini ve şifrelenmiş LS2 için b32 desteğini içermesi planlanıyor.

## Teşekkürler

Şifrelenmiş LS2 tasarımı, benzer tasarım hedeflerine sahip olan [Tor'un v3 gizli servis tanımlayıcılarından](https://spec.torproject.org/rend-spec-v3) büyük ölçüde etkilenmiştir.

## Kaynakça

* ["Yüksek hızlı, yüksek güvenlikli imzalar", Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe ve Bo-Yin Yang](https://ed25519.cr.yp.to/)
* [KEYBLIND-PROOF](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)
* [KEYBLIND-REFS](https://gitlab.torproject.org/tpo/core/tor/-/issues/8106)
* [PRNG-REFS](http://projectbullrun.org/dual-ec/ext-rand.html)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
* [RFC-7539-S2.4](https://tools.ietf.org/html/rfc7539#section-2.4)
* [TOR-REND-SPEC-V3](https://spec.torproject.org/rend-spec-v3)
* [UNSCIENTIFIC-KDF-SPEEDS](https://www.lvh.io/posts/secure-key-derivation-performance.html)
* [ZCASH](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)
