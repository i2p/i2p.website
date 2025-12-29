---
title: "Şifreli leaseSet'ler için B32"
description: "Şifrelenmiş LS2 leaseSet'ler için Base 32 adres biçimi"
slug: "b32-for-encrypted-leasesets"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
status: "Uygulandı"
---

## Genel Bakış

Standart Base 32 ("b32") adresleri hedefin özetini içerir. Bu, şifrelenmiş LS2 (öneri 123) için çalışmaz.

Şifrelenmiş bir LS2 (öneri 123) için geleneksel bir base 32 adresini kullanamayız, çünkü yalnızca destination'ın (hedef kimliği) özetini içerir. Bu, körleştirilmemiş açık anahtarı sağlamaz. İstemciler, leaseSet'i almak ve şifresini çözmek için destination'ın açık anahtarını, imza türünü, körleştirilmiş imza türünü ve isteğe bağlı bir gizli ya da özel anahtarı bilmek zorundadır. Bu nedenle, tek başına bir base 32 adresi yetersizdir. İstemcinin ya (açık anahtarı içeren) tam destination'a ya da yalnızca açık anahtara ihtiyacı vardır. İstemcinin bir adres defterinde tam destination'ı varsa ve adres defteri hash ile ters aramayı destekliyorsa, açık anahtar elde edilebilir.

Bu biçim, base32 adresinde özet yerine açık anahtarı kullanır. Bu biçim ayrıca açık anahtarın imza türünü ve körleme şemasının imza türünü içermelidir.

Bu belge, bu adresler için bir b32 biçimini tanımlar. Tartışmalar sırasında bu yeni formata "b33" adresi olarak atıfta bulunsak da, asıl yeni format olağan ".b32.i2p" sonekini korur.

## Uygulama Durumu

Öneri 123 (Yeni netDB Girdileri), 0.9.43 sürümünde (Ekim 2019) tam olarak uygulandı. Şifreli LS2 (LeaseSet2 — yeni LeaseSet formatı) özellik kümesi, adresleme formatı veya kriptografik spesifikasyonlarda geriye dönük uyumluluğu bozan herhangi bir değişiklik olmaksızın 2.10.0 sürümüne (Eylül 2025) kadar istikrarlı kaldı.

Başlıca uygulama kilometre taşları: - 0.9.38: Çevrimdışı anahtarlarla standart LS2 için Floodfill desteği - 0.9.39: RedDSA (dijital imza şeması) imza türü 11 ve temel şifreleme/şifre çözme - 0.9.40: Tam B32 adresleme desteği (Öneri 149) - 0.9.41: X25519 tabanlı istemci başına kimlik doğrulama - 0.9.42: Tüm körleme özellikleri çalışır durumda - 0.9.43: Tam uygulamanın tamamlandığı ilan edildi (Ekim 2019)

## Tasarım

- Yeni biçim, körlemesi kaldırılmış genel anahtar, körlemesi kaldırılmış imza türü ve körlenmiş imza türü içerir.
- İsteğe bağlı olarak özel bağlantılar için gizli ve/veya özel anahtar gereksinimlerini belirtir.
- Mevcut ".b32.i2p" sonekini kullanır, ancak daha uzundur.
- Hata tespiti için bir sağlama toplamı içerir.
- Şifrelenmiş leaseSet'ler için adresler, kodlanmış 56 veya daha fazla karakter (çözümlenmiş 35 veya daha fazla bayt) ile tanımlanır; geleneksel base 32 adreslerinde bu değer 52 karakter (32 bayt) şeklindedir.

## Teknik Şartname

### Oluşturma ve Kodlama

Aşağıdaki şekilde {56+ karakter}.b32.i2p (ikili biçimde 35+ karakter) biçiminde bir ana bilgisayar adı oluşturun:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
Son işleme ve sağlama toplamı:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
b32 (base32 kodlaması) sonunda kalan kullanılmayan bitlerin tümü 0 olmalıdır. Standart 56 karakterlik (35 bayt) bir adres için kullanılmayan bit yoktur.

### Kod Çözme ve Doğrulama

```
strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes):
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### Gizli ve Özel Anahtar Bitleri

Gizli ve özel anahtar bitleri, istemcilere, proxy'lere veya diğer istemci tarafı koda, leaseset'in şifresini çözmek için gizli ve/veya özel anahtarın gerekeceğini belirtmek için kullanılır. Belirli uygulamalar, kullanıcının gerekli verileri sağlamasını isteyebilir ya da gerekli veriler eksikse bağlantı girişimlerini reddedebilir.

Bu bitler yalnızca gösterge niteliğindedir. Gizli veya özel anahtar asla B32 adresinin kendisine dahil edilmemelidir, çünkü bu güvenliği tehlikeye atar.

## Kriptografik Ayrıntılar

### Körleme Şeması

Körleme şeması, Ed25519 ve ZCash'in tasarımını temel alan RedDSA'yı kullanarak, SHA-512 ile Ed25519 eğrisi üzerinde Red25519 imzaları üretir. Bu yaklaşım, körlenmiş açık anahtarların asal mertebeli altgrupta kalmasını sağlar ve bazı alternatif tasarımlarda mevcut olan güvenlik endişelerinden kaçınır.

Blinded keys (körleştirilmiş anahtarlar), UTC tarihine göre her gün şu formül kullanılarak yenilenir:

```
blinded_key = BLIND(unblinded_key, date, optional_secret)
```
DHT (Dağıtık Karma Tablosu) depolama konumu şu şekilde hesaplanır:

```
SHA256(type_byte || blinded_public_key)
```
### Şifreleme

Şifrelenmiş leaseset, AES donanım hızlandırması bulunmayan cihazlarda üstün performansı nedeniyle seçilen ChaCha20 akış şifresini kullanır. Spesifikasyon, anahtar türetimi için HKDF ve Diffie-Hellman işlemleri için X25519 kullanır.

Şifreli leasesets üç katmanlı bir yapıya sahiptir: - Dış katman: düz metin üstveri - Orta katman: istemci kimlik doğrulaması (DH veya PSK yöntemleri) - İç katman: lease bilgilerini içeren asıl LS2 verisi

### Kimlik Doğrulama Yöntemleri

İstemci başına kimlik doğrulama iki yöntemi destekler:

**DH Kimlik Doğrulama**: X25519 anahtar değişimini kullanır. Yetkilendirilmiş her istemci ortak anahtarını sunucuya iletir ve sunucu, ECDH'den (Eliptik Eğri Diffie-Hellman) türetilen paylaşılan bir sır kullanarak orta katmanı şifreler.

**PSK Kimlik Doğrulaması**: Şifreleme için önceden paylaşılan anahtarları doğrudan kullanır.

B32 adresindeki 2. bayrak biti, istemci başına kimlik doğrulama gerekip gerekmediğini belirtir.

## Önbellekleme

Bu belirtimin kapsamı dışında olsa da, routers ve istemciler, açık anahtar ile destination (varış noktası) arasındaki eşlemeyi ve tersini hatırlamalı ve önbelleğe almalıdır (kalıcı olarak önerilir).

blockfile naming service (blockfile adlandırma hizmeti), I2P'nin 0.9.8 sürümünden beri varsayılan adres defteri sistemi olup, karma üzerinden hızlı aramalar sağlayan özel bir ters arama eşlemesiyle birden çok adres defteri tutar. Bu işlev, başlangıçta yalnızca bir karma bilindiğinde, şifreli leaseSet çözümlemesi için kritik önem taşır.

## İmza Türleri

I2P sürüm 2.10.0 itibarıyla, 0'dan 11'e kadar olan imza türleri tanımlanmıştır. Tek baytlı kodlama standart olmaya devam eder; iki baytlı kodlama mevcut olsa da pratikte kullanılmamaktadır.

**Yaygın Olarak Kullanılan Türler:** - Tür 0 (DSA_SHA1): routers için kullanımdan kaldırılmıştır, hedefler için desteklenir - Tür 7 (EdDSA_SHA512_Ed25519): router kimlikleri ve hedefler için güncel standart - Tür 11 (RedDSA_SHA512_Ed25519): yalnızca blinding (körleme) desteğine sahip şifreli LS2 leasesets için

**Önemli Not**: Yalnızca Ed25519 (tip 7) ve Red25519 (tip 11), şifreli leaseSet'ler için gerekli körleştirmeyi destekler. Diğer imza türleri bu özellik ile birlikte kullanılamaz.

9-10 türleri (GOST algoritmaları) ayrılmıştır, ancak henüz uygulanmamıştır. 4-6 ve 8 türleri, çevrimdışı imzalama anahtarları için "yalnızca çevrimdışı" olarak işaretlenmiştir.

## Notlar

- Eski ve yeni varyantları uzunluğa göre ayırt edin. Eski b32 adresleri her zaman {52 karakter}.b32.i2p biçimindedir. Yenileri {56+ karakter}.b32.i2p biçimindedir
- base32 kodlaması, büyük/küçük harfe duyarsız çözümlemeyle RFC 4648 standartlarını izler ve çıktının küçük harf olması tercih edilir
- Daha büyük açık anahtarlara sahip imza türleri kullanıldığında adresler 200 karakteri aşabilir (örn. 132 baytlık anahtarlara sahip ECDSA P521)
- Yeni format, standart b32’de olduğu gibi istenirse jump links (adres atlama bağlantıları) içinde kullanılabilir (ve jump servers (adres atlama sunucuları) tarafından sunulabilir)
- Gizliliği artırmak için blinded keys (körleştirilmiş anahtarlar) UTC tarihine göre günlük olarak döndürülür
- Bu format, Tor'un rend-spec-v3.txt ek A.2 yaklaşımından ayrılır; off-curve blinded public keys (eğri dışında körleştirilmiş açık anahtarlar) ile potansiyel güvenlik etkileri söz konusudur

## Sürüm Uyumluluğu

Bu spesifikasyon, I2P’nin 0.9.47 (Ağustos 2020) sürümünden 2.10.0 (Eylül 2025) sürümüne kadar olan sürümler için doğrudur. Bu dönem boyunca B32 adresleme biçimi, şifrelenmiş LS2 (LeaseSet2) yapısı veya kriptografik uygulamalarda geriye dönük uyumluluğu bozan herhangi bir değişiklik yapılmamıştır. 0.9.47 ile oluşturulan tüm adresler, mevcut sürümlerle tamamen uyumludur.

## Kaynakça

**CRC-32** - [CRC-32 (Vikipedi)](https://en.wikipedia.org/wiki/CRC-32) - [RFC 3309: Akış Denetimli İletim Protokolü Sağlama Toplamı](https://tools.ietf.org/html/rfc3309)

**I2P Spesifikasyonları** - [Şifreli LeaseSet Spesifikasyonu](/docs/specs/encryptedleaseset/) - [Öneri 123: Yeni netDB Girdileri](/proposals/123-new-netdb-entries/) - [Öneri 149: Şifreli LS2 (LeaseSet 2) için B32](/proposals/149-b32-encrypted-ls2/) - [Ortak Yapılar Spesifikasyonu](/docs/specs/common-structures/) - [Adlandırma ve Adres Defteri](/docs/overview/naming/)

**Tor Karşılaştırması** - [Tor tartışma dizisi (tasarım bağlamı)](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)

**Ek Kaynaklar** - [I2P Projesi](/) - [I2P Forumu](https://i2pforum.net) - [Java API Belgeleri](http://docs.i2p-projekt.de/javadoc/)
