---
title: "NTCP2 Uygulama Ayrıntıları"
date: 2018-08-20
author: "villain"
description: "I2P'nin yeni taşıma protokolünün gerçekleştirim ayrıntıları ve teknik spesifikasyonları"
categories: ["development"]
---

I2P'nin taşıma protokolleri ilk olarak yaklaşık 15 yıl önce geliştirildi. O zamanlar, başlıca amaç aktarılan veriyi gizlemekti; protokolün kullanıldığı gerçeğini gizlemek değildi. Kimse DPI (derin paket incelemesi) ve protokollerin sansürlenmesine karşı korumayı ciddi biçimde düşünmüyordu. Zaman değişti ve orijinal taşıma protokolleri hâlâ güçlü güvenlik sağlıyor olsa da, yeni bir taşıma protokolüne ihtiyaç vardı. NTCP2, güncel sansür tehditlerine karşı koymak üzere tasarlanmıştır; özellikle paket uzunluklarının DPI ile analizine karşı dayanıklıdır. Ayrıca, yeni protokol kriptografideki en modern gelişmeleri kullanır. NTCP2, [Noise Protocol Framework](https://noiseprotocol.org/noise.html) üzerine kuruludur; hash fonksiyonu olarak SHA256 ve eliptik eğri Diffie-Hellman (DH) anahtar değişimi olarak x25519 kullanır.

NTCP2 protokolünün tam belirtimi [burada bulunabilir](/docs/specs/ntcp2/).

## Yeni Kriptografi

NTCP2, bir I2P gerçekleştirmesine aşağıdaki kriptografik algoritmaların eklenmesini gerektirir:

- x25519
- HMAC-SHA256
- Chacha20
- Poly1305
- AEAD
- SipHash

Orijinal protokolümüz olan NTCP ile karşılaştırıldığında, NTCP2, DH işlevi için ElGamal yerine x25519, AES-256-CBC/Adler32 yerine de AEAD/Chaha20/Poly1305 kullanır ve paketin uzunluk bilgisini gizlemek için SipHash kullanır. NTCP2'de kullanılan anahtar türetme işlevi daha karmaşıktır; artık çok sayıda HMAC-SHA256 çağrısı kullanmaktadır.

*i2pd (C++) uygulama notu: Yukarıda bahsedilen algoritmaların tümü, SipHash hariç, OpenSSL 1.1.0'da uygulanmıştır. SipHash, yakında çıkacak OpenSSL 1.1.1 sürümüne eklenecektir. Güncel sistemlerin çoğunda kullanılan OpenSSL 1.0.2 ile uyumluluk için, i2pd çekirdek geliştiricisi [Jeff Becker](https://github.com/majestrate) eksik kriptografik algoritmaların bağımsız gerçeklemelerine katkıda bulunmuştur.*

## RouterInfo Değişiklikleri

NTCP2, mevcut iki anahtara (şifreleme ve imza anahtarları) ek olarak üçüncü bir (x25519) anahtarın bulunmasını gerektirir. Buna statik anahtar denir ve RouterInfo içindeki adreslere "s" parametresi olarak eklenmelidir. Bu, hem NTCP2 başlatıcı (Alice) hem de yanıtlayıcı (Bob) için gereklidir. Birden fazla adres NTCP2'yi destekliyorsa, örneğin IPv4 ve IPv6, "s" parametresinin tümü için aynı olması zorunludur. Alice'in adresinde "host" ve "port" ayarlanmadan yalnızca "s" parametresinin bulunmasına izin verilir. Ayrıca bir "v" parametresi gereklidir; bu da şu anda her zaman "2" olarak ayarlanır.

NTCP2 adresi, ya ayrı bir NTCP2 adresi olarak ya da ek parametrelerle eski tarz bir NTCP adresi olarak belirtilebilir; bu durumda hem NTCP hem de NTCP2 bağlantılarını kabul eder. Java I2P uygulaması ikinci yaklaşımı kullanır, i2pd (C++ uygulaması) ise birincisini kullanır.

Bir düğüm NTCP2 bağlantılarını kabul ediyorsa, o düğüm yeni bağlantılar kurduğunda açık şifreleme anahtarı için bir başlatma vektörü (IV) olarak kullanılan "i" parametresiyle RouterInfo’sunu yayımlamak zorundadır.

## Bağlantı Kurulması

Bağlantı kurmak için her iki tarafın da geçici x25519 anahtar çiftleri oluşturması gerekir. Bu anahtarlara ve "statik" anahtarlara dayanarak veri aktarımı için bir anahtar kümesi türetirler. Her iki taraf da, diğer tarafın gerçekten o statik anahtara karşılık gelen bir özel anahtara sahip olduğunu ve o statik anahtarın RouterInfo’dakiyle aynı olduğunu doğrulamalıdır.

Bir bağlantı kurmak için üç mesaj gönderiliyor:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Her mesaj için «input key material» (girdi anahtar malzemesi) olarak adlandırılan paylaşılan bir x25519 anahtarı hesaplanır; ardından mesaj şifreleme anahtarı bir MixKey fonksiyonu ile üretilir. Mesajlar alışverişi sırasında ck (chaining key, zincirleme anahtarı) değeri tutulur. Veri aktarımı için anahtarlar üretilirken bu değer son girdi olarak kullanılır.

MixKey işlevi I2P'nin C++ gerçeklemesinde yaklaşık olarak şöyle görünür:

```cpp
void NTCP2Establisher::MixKey (const uint8_t * inputKeyMaterial, uint8_t * derived)
{
    // temp_key = HMAC-SHA256(ck, input_key_material)
    uint8_t tempKey[32]; unsigned int len;
    HMAC(EVP_sha256(), m_CK, 32, inputKeyMaterial, 32, tempKey, &len);
    // ck = HMAC-SHA256(temp_key, byte(0x01))
    static uint8_t one[1] =  { 1 };
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_CK, &len);
    // derived = HMAC-SHA256(temp_key, ck || byte(0x02))
    m_CK[32] = 2;
    HMAC(EVP_sha256(), tempKey, 32, m_CK, 33, derived, &len);
}
```
**SessionRequest** mesajı şunlardan oluşur: bir x25519 Alice açık anahtarı (32 bayt), AEAD/Chacha20/Poly1305 ile şifrelenmiş bir veri bloğu (16 bayt), bir özet (16 bayt) ve sonda biraz rastgele veri (dolgu). Dolgu uzunluğu, şifrelenmiş veri bloğunda tanımlanır. Şifrelenmiş blok ayrıca **SessionConfirmed** mesajının ikinci bölümünün uzunluğunu da içerir. Bir veri bloğu, Alice'in geçici anahtarından ve Bob'un statik anahtarından türetilen bir anahtarla şifrelenir ve imzalanır. MixKey fonksiyonu için başlangıç ck değeri SHA256 olarak ayarlanır (Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256).

Açık x25519 anahtarının 32 baytı DPI (Derin Paket İnceleme) tarafından tespit edilebildiğinden, Bob'un adresinin hash'ini (özetini) anahtar olarak ve RouterInfo'daki "i" parametresini ilklendirme vektörü (IV) olarak kullanarak AES-256-CBC algoritmasıyla şifrelenir.

**SessionCreated** mesajı, anahtarın her iki tarafın geçici anahtarlarına göre hesaplanması dışında, **SessionRequest** ile aynı yapıya sahiptir. **SessionRequest** mesajındaki açık anahtarın şifrelenmesi/şifre çözülmesinden sonra üretilen IV (başlatma vektörü), geçici açık anahtarın şifrelenmesi/şifre çözülmesi için IV olarak kullanılır.

**SessionConfirmed** mesajı 2 parçadan oluşur: statik açık anahtar ve Alice'e ait RouterInfo. Önceki mesajlardan farkı, geçici (ephemeral) açık anahtarın **SessionCreated** ile aynı anahtar kullanılarak AEAD/Chaha20/Poly1305 ile şifrelenmiş olmasıdır. Bu, mesajın ilk kısmının 32 bayttan 48 bayta çıkarılmasına yol açar. İkinci kısım da AEAD/Chaha20/Poly1305 ile şifrelenir, ancak Bob'un geçici anahtarı ve Alice'in statik anahtarından hesaplanan yeni bir anahtar kullanılarak. RouterInfo bölümü ayrıca rastgele veri dolgusu ile genişletilebilir, ancak gerekli değildir; çünkü RouterInfo genellikle değişken uzunluktadır.

## Veri Aktarım Anahtarlarının Oluşturulması

Eğer tüm hash ve anahtar doğrulamaları başarılı olduysa, her iki tarafta da son MixKey işleminin ardından ortak bir ck değeri mevcut olmalıdır. Bu değer, bir bağlantının her bir tarafı için iki anahtar kümesi <k, sipk, sipiv> oluşturmak üzere kullanılır. "k" bir AEAD/Chaha20/Poly1305 anahtarıdır, "sipk" bir SipHash anahtarıdır, "sipiv" ise SipHash IV (başlatma vektörü) için bir başlangıç değeridir ve her kullanımından sonra değiştirilir.

Anahtarları üretmek için kullanılan kod, I2P'nin C++ gerçekleştirmesinde şu şekildedir:

```cpp
void NTCP2Session::KeyDerivationFunctionDataPhase ()
{
    uint8_t tempKey[32]; unsigned int len;
    // temp_key = HMAC-SHA256(ck, zerolen)
    HMAC(EVP_sha256(), m_Establisher->GetCK (), 32, nullptr, 0, tempKey, &len);
    static uint8_t one[1] =  { 1 };
    // k_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Kab, &len);
    m_Kab[32] = 2;
    // k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Kab, 33, m_Kba, &len);
    static uint8_t ask[4] = { 'a', 's', 'k', 1 }, master[32];
    // ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, ask, 4, master, &len);
    uint8_t h[39];
    memcpy (h, m_Establisher->GetH (), 32);
    memcpy (h + 32, "siphash", 7);
    // temp_key = HMAC-SHA256(ask_master, h || "siphash")
    HMAC(EVP_sha256(), master, 32, h, 39, tempKey, &len);
    // sip_master = HMAC-SHA256(temp_key, byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, one, 1, master, &len);
    // temp_key = HMAC-SHA256(sip_master, zerolen)
    HMAC(EVP_sha256(), master, 32, nullptr, 0, tempKey, &len);
   // sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Sipkeysab, &len);
    m_Sipkeysab[32] = 2;
     // sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Sipkeysab, 33, m_Sipkeysba, &len);
}
```
*i2pd (C++) gerçekleme notu: "sipkeys" dizisinin ilk 16 baytı bir SipHash anahtarıdır, son 8 bayt ise IV'dir (başlatma vektörü). SipHash iki adet 8 baytlık anahtar gerektirir, ancak i2pd bunları tek bir 16 baytlık anahtar olarak ele alır.*

## Veri Aktarımı

Veri çerçeveler halinde aktarılır, her çerçeve 3 bölümden oluşur:

- 2 bytes of frame length obfuscated with SipHash
- data encrypted with Chacha20
- 16 bytes of Poly1305 hash value

Tek bir çerçevede aktarılan verinin azami uzunluğu 65519 bayttır.

Mesaj uzunluğu, geçerli SipHash IV'nin ilk iki baytıyla XOR işlemi uygulanarak maskelenir.

Şifrelenmiş veri bölümü, veri blokları içerir. Her bloğun başına, blok türünü ve blok uzunluğunu tanımlayan 3 baytlık bir başlık eklenir. Genellikle I2NP türü bloklar aktarılır; bunlar, başlığı değiştirilmiş I2NP iletileridir. Bir NTCP2 çerçevesi birden fazla I2NP bloğunu aktarabilir.

Diğer önemli veri bloğu türü rastgele veri bloğudur. Her NTCP2 çerçevesine bir rastgele veri bloğu eklenmesi önerilir. Yalnızca bir rastgele veri bloğu eklenebilir ve bu son blok olmalıdır.

Mevcut NTCP2 uygulamasında kullanılan diğer veri blokları şunlardır:

- **RouterInfo** — usually contains Bob's RouterInfo after the connection has been established, but it can also contain RouterInfo of a random node for the purpose of speeding up floodfills (there is a flags field for that case).
- **Termination** — is used when a host explicitly terminates a connection and specifies a reason for that.
- **DateTime** — a current time in seconds.

## Özet

Yeni I2P taşıma protokolü NTCP2, DPI (Derin Paket İncelemesi) sansürüne karşı etkili direnç sağlar. Kullanılan daha hızlı, modern kriptografi sayesinde CPU yükünü de azaltır. Bu, I2P'nin akıllı telefonlar ve ev router'ları gibi düşük özellikli cihazlarda çalışmasını daha olası kılar. Her iki büyük I2P uygulaması da NTCP2'yi tam olarak destekler ve 0.9.36 (Java) ile 2.20 (i2pd, C++) sürümlerinden itibaren NTCP2'nin kullanılmasını sağlar.
