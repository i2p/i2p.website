---
title: "Post-Kuantum Kripto Protokolleri"
aliases:
  - "/proposals/169-pq-crypto"
  - "/proposals/169-pq-crypto/"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2026-10-24"
status: "Aç"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

### Durum

| Protokol / Özellik | Durum |
|--------------------|--------|
| Ratchet | Java I2P ve i2pd'de tamamlandı |
| NTCP2 | Beta 2026 1. Çeyrek |
| SSU2 | Uygulama yakında başlıyor, Beta 2026 2-3. Çeyrek |
| MLDSA SigTypes | Düşük öncelik, muhtemelen 2027+ |
## Genel Bakış

Uygun kuantum sonrası (PQ) kriptografi için araştırma ve rekabet on yıldır devam ederken, seçenekler yakın zamana kadar netlik kazanmamıştı.

2022'de PQ kripto'nun etkilerini incelemeye başladık [zzz.i2p](http://zzz.i2p/topics/3294).

TLS standartları son iki yılda hibrit şifreleme desteği ekledi ve Chrome ve Firefox'taki destek sayesinde artık internetdeki şifrelenmiş trafiğin önemli bir bölümünde kullanılmakta [Cloudflare](https://blog.cloudflare.com/pq-2024/).

NIST yakın zamanda kuantum sonrası kriptografi için önerilen algoritmaları tamamlayıp yayınladı [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Birçok yaygın kriptografi kütüphanesi artık NIST standartlarını destekliyor veya yakın gelecekte destek yayınlayacak.

Hem [Cloudflare](https://blog.cloudflare.com/pq-2024/) hem de [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) geçişin hemen başlaması gerektiğini öneriyor. Ayrıca 2022 NSA PQ SSS'ye bakın [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P güvenlik ve kriptografide öncü olmalıdır. Önerilen algoritmaları uygulamanın zamanı geldi. Esnek kripto tipi ve imza tipi sistemimizi kullanarak, hibrit kripto ve PQ ile hibrit imzalar için tipler ekleyeceğiz.

## Hedefler

- PQ-dirençli algoritmaları seç
- Uygun yerlerde I2P protokollerine yalnızca-PQ ve hibrit algoritmaları ekle
- Birden fazla varyant tanımla
- Uygulama, test, analiz ve araştırma sonrasında en iyi varyantları seç
- Desteği aşamalı olarak ve geriye dönük uyumluluk ile ekle

## Hedef Olmayanlar

- Tek yönlü (Noise N) şifreleme protokollerini değiştirmeyin
- SHA256'dan uzaklaşmayın, yakın vadede PQ tarafından tehdit altında değil
- Şu anda nihai tercih edilen varyantları seçmeyin

## Tehdit Modeli

- OBEP veya IBGW'deki router'lar, muhtemelen işbirliği yaparak,
  garlic mesajlarını daha sonra şifrelemesini çözmek için saklama (forward secrecy)
- Ağ gözlemcilerinin
  transport mesajlarını daha sonra şifrelemesini çözmek için saklama (forward secrecy)
- Ağ katılımcılarının RI, LS, streaming, datagram'lar,
  veya diğer yapılar için imzaları taklit etmesi

## Etkilenen Protokoller

Aşağıdaki protokolleri kabaca geliştirme sırasına göre değiştireceğiz. Genel dağıtım muhtemelen 2025 sonundan 2027 ortasına kadar sürecek. Ayrıntılar için aşağıdaki Öncelikler ve Dağıtım bölümüne bakın.

| Protokol / Özellik | Durum |
|--------------------|--------|
| Hybrid MLKEM Ratchet ve LS | Onaylandı 2025-06; beta 2025-08; sürüm 2025-11 |
| Hybrid MLKEM NTCP2 | Canlı ağda test edildi, Onaylandı 2026-02; beta hedefi 2026-05; sürüm hedefi 2026-08 |
| Hybrid MLKEM SSU2 | Onaylandı 2026-02; beta hedefi 2026-08; sürüm hedefi 2026-11 |
| MLDSA SigTypes 12-14 | Öneri kararlı ancak 2027'ye kadar kesinleşmeyebilir |
| MLDSA Dests | Canlı ağda test edildi, floodfill desteği için ağ yükseltmesi gerekiyor |
| Hybrid SigTypes 15-17 | Ön aşamada |
| Hybrid Dests | |
## Tasarım

NIST FIPS 203 ve 204 standartlarını [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) destekleyeceğiz. Bu standartlar CRYSTALS-Kyber ve CRYSTALS-Dilithium (3.1, 3 ve daha eski sürümler) temel alınarak oluşturulmuştur ancak bunlarla uyumlu DEĞİLDİR.

### Anahtar Değişimi

Aşağıdaki protokollerde hibrit anahtar değişimini destekleyeceğiz:

| Proto   | Noise Türü | Sadece PQ Destekler mi? | Hibrit Destekler mi? |
|---------|------------|-------------------------|---------------------|
| NTCP2   | XK         | hayır                   | evet                |
| SSU2    | XK         | hayır                   | evet                |
| Ratchet | IK         | hayır                   | evet                |
| TBM     | N          | hayır                   | hayır               |
| NetDB   | N          | hayır                   | hayır               |
PQ KEM yalnızca geçici anahtarlar sağlar ve Noise XK ve IK gibi statik anahtar el sıkışmalarını doğrudan desteklemez.

Noise N iki yönlü anahtar değişimi kullanmaz ve bu nedenle hibrit şifreleme için uygun değildir.

Bu nedenle sadece hibrit şifrelemeyi destekleyeceğiz, NTCP2, SSU2 ve Ratchet için. [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)'te belirtildiği gibi üç ML-KEM varyantını tanımlayacağız, toplam 3 yeni şifreleme türü için. Hibrit türler sadece X25519 ile kombinasyon halinde tanımlanacak.

Yeni şifreleme türleri şunlardır:

| Type | Code |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
Ek yük önemli olacaktır. Tipik mesaj 1 ve 2 boyutları (XK ve IK için) şu anda yaklaşık 100 bayttır (herhangi bir ek yük öncesi). Bu, algoritmaya bağlı olarak 8x ile 15x arasında artacaktır.

### İmzalar

Aşağıdaki yapılarda PQ ve hibrit imzaları destekleyeceğiz:

Bu nedenle hem PQ-only hem de hibrit imzaları destekleyeceğiz. [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)'te tanımlandığı gibi üç ML-DSA varyantını, Ed25519 ile üç hibrit varyantı ve yalnızca SU3 dosyaları için prehash ile üç PQ-only varyantını tanımlayacağız, toplamda 9 yeni imza tipi. Hibrit tipler yalnızca Ed25519 ile kombinasyon halinde tanımlanacak. SU3 dosyaları hariç, pre-hash varyantları (HashML-DSA) DEĞİL standart ML-DSA kullanacağız.

| Tür | Yalnızca PQ Destekler mi? | Hibrit Destekler mi? |
|------|-------------------------|---------------------|
| RouterInfo | evet | evet |
| LeaseSet | evet | evet |
| Streaming SYN/SYNACK/Close | evet | evet |
| Yanıtlanabilir Datagramlar | evet | evet |
| Datagram2 (önerge 163) | evet | evet |
| I2CP oturum oluşturma mesajı | evet | evet |
| SU3 dosyaları | evet | evet |
| X.509 sertifikaları | evet | evet |
| Java anahtar depoları | evet | evet |
[FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) bölüm 3.4'te tanımlandığı gibi "deterministik" varyant yerine "korumalı" veya rastgele imzalama varyantını kullanacağız. Bu, aynı veri üzerinde bile her imzanın farklı olmasını sağlar ve yan kanal saldırılarına karşı ek koruma sağlar. Kodlama ve bağlam dahil algoritma seçimleri hakkında ek ayrıntılar için aşağıdaki uygulama notları bölümüne bakın.

Yeni imza türleri şunlardır:

X.509 sertifikaları ve diğer DER kodlamaları, [IETF taslağında](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) tanımlanan kompozit yapıları ve OID'leri kullanacaktır.

| Tip | Kod |
|------|------|
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |
Ek yük önemli olacaktır. Tipik Ed25519 hedef ve router kimlik boyutları 391 bayttır. Bunlar algoritmaya bağlı olarak 3,5x ila 6,8x artacaktır. Ed25519 imzaları 64 bayttır. Bunlar algoritmaya bağlı olarak 38x ila 76x artacaktır. Tipik imzalanmış RouterInfo, LeaseSet, yanıtlanabilir datagramlar ve imzalanmış akış mesajları yaklaşık 1KB'tır. Bunlar algoritmaya bağlı olarak 3x ila 8x artacaktır.

Yeni hedef ve router kimlik türleri dolgu içermediğinden, sıkıştırılabilir olmayacaktır. Aktarım sırasında gzip ile sıkıştırılan hedeflerin ve router kimliklerinin boyutları, algoritma türüne bağlı olarak 12 kat - 38 kat artacaktır.

Destination'lar için, yeni imza türleri leaseset'teki tüm şifreleme türleriyle desteklenir. Anahtar sertifikasındaki şifreleme türünü NONE (255) olarak ayarlayın.

### Yasal Kombinasyonlar

RouterIdentity'ler için ElGamal şifreleme türü artık kullanımdan kaldırılmıştır. Yeni imza türleri yalnızca X25519 (tür 4) şifrelemesi ile desteklenmektedir. Yeni şifreleme türleri RouterAddress'lerde belirtilecektir. Anahtar sertifikasındaki şifreleme türü tür 4 olmaya devam edecektir.

SHA3-256, SHAKE128 ve SHAKE256 için test vektörleri [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values) adresinde bulunmaktadır.

### Yeni Kripto Gerekli

- ML-KEM (eski adıyla CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (eski adıyla CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (eski adıyla Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Yalnızca SHAKE128 için kullanılır
- SHA3-256 (eski adıyla Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 ve SHAKE256 (SHA3-128 ve SHA3-256'nın XOF uzantıları) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Java bouncycastle kütüphanesinin yukarıdakilerin tamamını desteklediğini unutmayın. C++ kütüphane desteği OpenSSL 3.5'te mevcuttur [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

[FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+) desteğini sunmayacağız, ML-DSA'dan çok çok daha yavaş ve büyüktür. Yaklaşan FIPS206 (Falcon) desteğini sunmayacağız, henüz standartlaştırılmamıştır. NTRU veya NIST tarafından standartlaştırılmamış diğer PQ adaylarını desteklemeyeceğiz.

### Alternatifler

Wireguard'ı (IK) saf PQ kripto için uyarlama konusunda bazı araştırma [makalesi](https://eprint.iacr.org/2020/379.pdf) bulunmakta, ancak bu makalede birkaç açık soru var. Daha sonra, bu yaklaşım PQ Wireguard için Rosenpass [Rosenpass](https://rosenpass.eu/) [teknik raporu](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) olarak uygulandı.

### Rosenpass

Rosenpass, önceden paylaşılmış Classic McEliece 460896 statik anahtarları (her biri 500 KB) ve Kyber-512 (temelde MLKEM-512) geçici anahtarları ile Noise KK benzeri bir el sıkışma kullanır. Classic McEliece şifre metinleri yalnızca 188 bayt olduğu ve Kyber-512 genel anahtarları ile şifre metinleri makul boyutta olduğu için, her iki el sıkışma mesajı da standart bir UDP MTU'ya sığar. PQ KK el sıkışmasından çıkan paylaşılan anahtar (osk), standart Wireguard IK el sıkışması için girdi önceden paylaşılmış anahtar (psk) olarak kullanılır. Böylece toplamda iki tam el sıkışma vardır, biri tamamen PQ ve diğeri tamamen X25519.

XK ve IK el sıkışmalarımızı değiştirmek için bunların hiçbirini yapamayız çünkü:

Whitepaper'da çok sayıda faydalı bilgi bulunmaktadır ve bunu fikirler ve ilham için gözden geçireceğiz. TODO.

- KK yapamayız, Bob'un Alice'in statik anahtarı yok
- 500KB statik anahtarlar çok büyük
- Ekstra bir gidiş-dönüş istemiyoruz

Ortak yapılar belgesindeki [/docs/specs/common-structures/](/docs/specs/common-structures/) bölümleri ve tabloları aşağıdaki şekilde güncelleyin:

## Spesifikasyon

### Ortak Yapılar

Yeni Public Key türleri şunlardır:

#### Sorunlar

Hibrit public key'ler X25519 anahtarıdır. KEM public key'ler Alice'ten Bob'a gönderilen geçici PQ anahtarıdır. Kodlama ve byte sırası [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)'te tanımlanmıştır.

| Tip | Public Key Uzunluğu | Başlangıç | Kullanım |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | Proposal 169'a bakın, sadece Leasesets için, RI'ler veya Destinations için değil |
| MLKEM768_X25519 | 32 | 0.9.xx | Proposal 169'a bakın, sadece Leasesets için, RI'ler veya Destinations için değil |
| MLKEM1024_X25519 | 32 | 0.9.xx | Proposal 169'a bakın, sadece Leasesets için, RI'ler veya Destinations için değil |
| MLKEM512 | 800 | 0.9.xx | Proposal 169'a bakın, sadece handshake'ler için, Leasesets, RI'ler veya Destinations için değil |
| MLKEM768 | 1184 | 0.9.xx | Proposal 169'a bakın, sadece handshake'ler için, Leasesets, RI'ler veya Destinations için değil |
| MLKEM1024 | 1568 | 0.9.xx | Proposal 169'a bakın, sadece handshake'ler için, Leasesets, RI'ler veya Destinations için değil |
| MLKEM512_CT | 768 | 0.9.xx | Proposal 169'a bakın, sadece handshake'ler için, Leasesets, RI'ler veya Destinations için değil |
| MLKEM768_CT | 1088 | 0.9.xx | Proposal 169'a bakın, sadece handshake'ler için, Leasesets, RI'ler veya Destinations için değil |
| MLKEM1024_CT | 1568 | 0.9.xx | Proposal 169'a bakın, sadece handshake'ler için, Leasesets, RI'ler veya Destinations için değil |
| NONE | 0 | 0.9.xx | Proposal 169'a bakın, sadece PQ sig tipli destinations için, RI'ler veya Leasesets için değil |
MLKEM*_CT anahtarları gerçek anlamda public key değildir, bunlar Noise handshake işleminde Bob'dan Alice'e gönderilen "ciphertext" (şifreli metin) verisidir. Eksiksiz olması için burada listelenmiştir.

Yeni Private Key türleri şunlardır:

#### PrivateKey

Hibrit özel anahtarlar X25519 anahtarlarıdır. KEM özel anahtarları yalnızca Alice içindir. KEM kodlaması ve bayt sırası [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)'te tanımlanmıştır.

| Tip | Özel Anahtar Uzunluğu | Sürümden İtibaren | Kullanım |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | Öneri 169'a bakın, yalnızca Leasesetler için, RI'ler veya Destinationlar için değil |
| MLKEM768_X25519 | 32 | 0.9.xx | Öneri 169'a bakın, yalnızca Leasesetler için, RI'ler veya Destinationlar için değil |
| MLKEM1024_X25519 | 32 | 0.9.xx | Öneri 169'a bakın, yalnızca Leasesetler için, RI'ler veya Destinationlar için değil |
| MLKEM512 | 1632 | 0.9.xx | Öneri 169'a bakın, yalnızca handshake'ler için, Leaseset, RI veya Destinationlar için değil |
| MLKEM768 | 2400 | 0.9.xx | Öneri 169'a bakın, yalnızca handshake'ler için, Leaseset, RI veya Destinationlar için değil |
| MLKEM1024 | 3168 | 0.9.xx | Öneri 169'a bakın, yalnızca handshake'ler için, Leaseset, RI veya Destinationlar için değil |
Yeni İmzalama Genel Anahtarı türleri şunlardır:

#### SigningPublicKey

Hibrit imzalama public key'leri, [IETF taslağında](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) olduğu gibi Ed25519 key'ini takip eden PQ key'idir. Kodlama ve byte sırası [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)'te tanımlanmıştır.

| Tip | Uzunluk (bayt) | Sürümden İtibaren | Kullanım |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | Öneri 169'a bakın |
| MLDSA65 | 1952 | 0.9.xx | Öneri 169'a bakın |
| MLDSA87 | 2592 | 0.9.xx | Öneri 169'a bakın |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | Öneri 169'a bakın |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | Öneri 169'a bakın |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | Öneri 169'a bakın |
| MLDSA44ph | 1344 | 0.9.xx | Yalnızca SU3 dosyaları için, netDb yapıları için değil |
| MLDSA65ph | 1984 | 0.9.xx | Yalnızca SU3 dosyaları için, netDb yapıları için değil |
| MLDSA87ph | 2624 | 0.9.xx | Yalnızca SU3 dosyaları için, netDb yapıları için değil |
Yeni İmzalama Özel Anahtar türleri şunlardır:

#### SigningPrivateKey

Hibrit imzalama özel anahtarları, [IETF taslağında](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) olduğu gibi Ed25519 anahtarının ardından PQ anahtarının gelmesiyle oluşur. Kodlama ve bayt sırası [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)'te tanımlanmıştır.

| Tür | Uzunluk (bayt) | Sürümden İtibaren | Kullanım |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | Öneri 169'a bakınız |
| MLDSA65 | 4032 | 0.9.xx | Öneri 169'a bakınız |
| MLDSA87 | 4896 | 0.9.xx | Öneri 169'a bakınız |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | Öneri 169'a bakınız |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | Öneri 169'a bakınız |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | Öneri 169'a bakınız |
| MLDSA44ph | 2592 | 0.9.xx | Sadece SU3 dosyaları için, netDb yapıları için değil. Öneri 169'a bakınız |
| MLDSA65ph | 4064 | 0.9.xx | Sadece SU3 dosyaları için, netDb yapıları için değil. Öneri 169'a bakınız |
| MLDSA87ph | 4928 | 0.9.xx | Sadece SU3 dosyaları için, netDb yapıları için değil. Öneri 169'a bakınız |
Yeni imza türleri şunlardır:

Hibrit imzalar, [IETF taslağında](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) olduğu gibi Ed25519 imzasını takip eden PQ imzasıdır. Hibrit imzalar her iki imzayı da doğrulayarak ve bunlardan herhangi biri başarısız olursa başarısız olarak sonuçlanarak doğrulanır. Kodlama ve bayt sırası [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)'te tanımlanmıştır.

#### İmza

Yeni İmzalama Genel Anahtar türleri şunlardır:

| Tip | Uzunluk (bayt) | Sürümden İtibaren | Kullanım |
|-----|----------------|-------------------|----------|
| MLDSA44 | 2420 | 0.9.xx | Teklif 169'a bakın |
| MLDSA65 | 3309 | 0.9.xx | Teklif 169'a bakın |
| MLDSA87 | 4627 | 0.9.xx | Teklif 169'a bakın |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | Teklif 169'a bakın |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | Teklif 169'a bakın |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | Teklif 169'a bakın |
| MLDSA44ph | 2484 | 0.9.xx | Yalnızca SU3 dosyaları için, netDb yapıları için değil. Teklif 169'a bakın |
| MLDSA65ph | 3373 | 0.9.xx | Yalnızca SU3 dosyaları için, netDb yapıları için değil. Teklif 169'a bakın |
| MLDSA87ph | 4691 | 0.9.xx | Yalnızca SU3 dosyaları için, netDb yapıları için değil. Teklif 169'a bakın |
Yeni Crypto Public Key türleri şunlardır:

#### Anahtar Sertifikaları

Hibrit imzalama public key'leri, [IETF taslağında](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) olduğu gibi Ed25519 key'ini takip eden PQ key'idir. Kodlama ve byte sırası [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)'te tanımlanmıştır.

| Tür | Tür Kodu | Toplam Genel Anahtar Uzunluğu | Tarihinden İtibaren | Kullanım |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | Öneri 169'a bakınız |
| MLDSA65 | 13 | 1952 | 0.9.xx | Öneri 169'a bakınız |
| MLDSA87 | 14 | 2592 | 0.9.xx | Öneri 169'a bakınız |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | Öneri 169'a bakınız |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | Öneri 169'a bakınız |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | Öneri 169'a bakınız |
| MLDSA44ph | 18 | n/a | 0.9.xx | Yalnızca SU3 dosyaları için |
| MLDSA65ph | 19 | n/a | 0.9.xx | Yalnızca SU3 dosyaları için |
| MLDSA87ph | 20 | n/a | 0.9.xx | Yalnızca SU3 dosyaları için |
Hybrid veya PQ imza türlerine sahip destinasyonlar için şifreleme türü olarak NONE (tür 255) kullanın, ancak kripto anahtarı yoktur ve 384 baytlık ana bölümün tamamı imzalama anahtarı içindir.

| Tip | Tip Kodu | Toplam Genel Anahtar Uzunluğu | Sürümden İtibaren | Kullanım |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | Bkz. öneri 169, sadece Leasesets için, RI'ler veya Destinations için değil |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | Bkz. öneri 169, sadece Leasesets için, RI'ler veya Destinations için değil |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | Bkz. öneri 169, sadece Leasesets için, RI'ler veya Destinations için değil |
| NONE | 255 | 0 | 0.9.xx | Bkz. öneri 169 |
Hibrit anahtar türleri anahtar sertifikalarında ASLA bulunmaz; yalnızca leaseSet'lerde bulunur.

Dolgu yok. Toplam uzunluk 7 + toplam anahtar uzunluğudur. Anahtar sertifikası uzunluğu 4 + fazla anahtar uzunluğudur.

#### Hedef boyutları

İşte yeni Destination türleri için uzunluklar. Tümü için Enc türü NONE (tür 255)'dur ve şifreleme anahtarı uzunluğu 0 olarak kabul edilir. Tüm 384 baytlık bölüm, imzalama genel anahtarının ilk kısmı için kullanılır. NOT: Bu, ECDSA_SHA512_P521 ve RSA imza türleri için spesifikasyondan farklıdır, burada kullanılmamasına rağmen destination'da 256 baytlık ElGamal anahtarını koruduk.

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

MLDSA44 için örnek 1319 baytlık hedef bayt akışı:

MLDSA44 için örnek 1351 baytlık router kimlik bayt akışı:

| Tür | Tür Kodu | Toplam Açık Anahtar Uzunluğu | Ana | Fazla | Toplam Dest Uzunluğu |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
#### RouterIdent boyutları

İşte yeni Destination türleri için uzunluklar. Tümü için şifreleme türü X25519'dur (tür 4). X25519 genel anahtarından sonraki 352 baytlık bölümün tamamı, imzalama genel anahtarının ilk kısmı için kullanılır. Dolgu yoktur. Toplam uzunluk 39 + toplam anahtar uzunluğudur. Anahtar sertifikası uzunluğu 4 + fazla anahtar uzunluğudur.

El sıkışmalar [Noise Protocol](https://noiseprotocol.org/noise.html) el sıkışma kalıplarını kullanır.

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Tür | Tür Kodu | Toplam Genel Anahtar Uzunluğu | Ana | Fazla | Toplam RouterIdent Uzunluğu |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PublicKey

Hibrit ileri gizlilik (hfs) için XK ve IK'ye yapılan aşağıdaki değişiklikler [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) bölüm 5'te belirtildiği gibidir:

e1 deseni, [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) bölüm 4'te belirtildiği gibi şu şekilde tanımlanmıştır:

#### split() için KDF

```

  M = message
  Prefix = "CompositeAlgorithmSignatures2025" (32 bytes, not null terminated)
  Label = (30 bytes, not null terminated), one of:
          "COMPSIG-MLDSA44-Ed25519-SHA512"
          "COMPSIG-MLDSA65-Ed25519-SHA512"
          "COMPSIG-MLDSA87-Ed25519-SHA512"  // not in [COMPOSITE-SIGS]
  ctx = "" (0 bytes)
  len(ctx) = 0  (1 byte)
  PH(M) = SHA512(M) (64 bytes)


  Compute a hash of the message prepended as follows:

  M' = Prefix || Label || len(ctx) || ctx || PH( M )

  M' length is 127 bytes.

  Sign the prehashed message M':

  signature = MLDSA_SIGN(M') || Ed25519_SIGN(M')

```
#### Noise tanımlayıcıları

ekem1 deseni, [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) bölüm 4'te belirtildiği şekilde aşağıdaki gibi tanımlanmıştır:

```

  M' = as above

  signature = MLDSA_VERIFY(M') && Ed25519_VERIFY(M')


```
#### 1b) Yeni oturum formatı (bağlama ile)

Bu bölüm hem IK hem de XK protokolleri için geçerlidir.

### Handshake Kalıpları

Hibrit handshake, [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) içinde tanımlanmıştır. Alice'den Bob'a olan ilk mesaj, mesaj yükünden önce e1 olan encapsulation key'i içerir. Bu, ek bir statik anahtar olarak işlenir; bunun üzerinde (Alice olarak) EncryptAndHash() veya (Bob olarak) DecryptAndHash() çağrısı yapın. Ardından mesaj yükünü her zamanki gibi işleyin.

Aşağıdaki harf eşleştirmesi kullanılır:

- e = tek kullanımlık geçici anahtar
- s = statik anahtar
- p = mesaj yükü
- e1 = tek kullanımlık geçici PQ anahtarı, Alice'den Bob'a gönderilir
- ekem1 = KEM şifreli metni, Bob'dan Alice'e gönderilir

[FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)'te tanımlandığı gibi kullanılan kriptografik yapı taşlarına karşılık gelen aşağıdaki fonksiyonları tanımlıyoruz.

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  IK:                       IKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, s, ss, p       -> e, es, e1, s, ss, p
  <- tag, e, ee, se, p     <- tag, e, ee, ekem1, se, p
  <- p                     <- p
  p ->                     p ->

  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
(encap_key, decap_key) = PQ_KEYGEN()

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
(ciphertext, kem_shared_key) = ENCAPS(encap_key)

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### Noise Handshake KDF

#### 1b) Yeni oturum formatı (bağlama ile)

- Handshake hash fonksiyonunu değiştirmeli miyiz? [Karşılaştırmaya](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3) bakın.
  SHA256 PQ'ya karşı savunmasız değil, ancak hash fonksiyonumuzu yükseltmek istiyorsak,
  diğer şeyleri değiştirirken şimdi tam zamanı.
  Mevcut IETF SSH önerisi [IETF taslağı](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) SHA256 ile MLKEM768
  ve SHA384 ile MLKEM1024 kullanmak. Bu öneri
  güvenlik değerlendirmelerinin tartışmasını içeriyor.
- 0-RTT ratchet verisi göndermeyi (LS dışında) bırakmalı mıyız?
- 0-RTT verisi göndermiyorsak ratchet'i IK'dan XK'ya değiştirmeli miyiz?

#### Genel Bakış

kem_shared_key = DECAPS(ciphertext, decap_key)

Hem encap_key hem de ciphertext'in Noise handshake mesajları 1 ve 2'deki ChaCha/Poly blokları içinde şifrelendiğini unutmayın. Bunlar handshake işleminin bir parçası olarak şifresi çözülecektir.

İkinci mesaj, Bob'dan Alice'a, mesaj yükünden önce ekem1 şifreli metinini içerir. Bu ek bir statik anahtar olarak değerlendirilir; (Bob olarak) EncryptAndHash() veya (Alice olarak) DecryptAndHash() çağrısı yapın. Ardından, kem_shared_key'i hesaplayın ve MixKey(kem_shared_key) çağrısı yapın. Sonra mesaj yükünü her zamanki gibi işleyin.

#### Tanımlanmış ML-KEM İşlemleri

XK için: 'es' mesaj deseni sonrasında ve payload öncesinde, şunu ekleyin:

VEYA

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

IK için: 'es' mesaj deseni sonrasında ve 's' mesaj deseni öncesinde, şunu ekleyin:

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

XK için: 'es' mesaj kalıbından sonra ve yükten önce, şunu ekleyin:

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

VEYA

kem_shared_key, MixHash() ile chaining key'e karıştırılır. Ayrıntılar için aşağıya bakın.

#### Mesaj 1 için Alice KDF

XK için: 'ee' mesaj deseninden sonra ve payload'dan önce, şunu ekleyin:

VEYA

IK için: 'ee' mesaj kalıbından sonra ve 'se' mesaj kalıbından önce, şunları ekleyin:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Mesaj 1 için Bob KDF

XK için: 'ee' mesaj deseninden sonra ve payload'dan önce, şunu ekleyin:

VEYA

IK için: 'es' mesaj deseni sonrasında ve 's' mesaj deseni öncesinde, şunu ekleyin:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Mesaj 2 için Bob KDF

ECIES-Ratchet spesifikasyonunu [/docs/specs/ecies/](/docs/specs/ecies/) aşağıdaki şekilde güncelleyin:

VEYA

Şifrelenmiş format:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### Mesaj 2 için Alice KDF

'ee' mesaj deseninden sonra (ve IK için 'ss' mesaj deseninden önce), şunu ekleyin:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### Mesaj 3 için KDF (yalnızca XK)

değişmedi

#### Noise tanımlayıcıları

değişmedi

### Ratchet

Değişiklikler: Mevcut ratchet, ilk ChaCha bölümü için boş bir payload'a ve ikinci bölümde payload'a sahiptir. ML-KEM ile artık üç bölüm bulunmaktadır. İlk bölüm şifrelenmiş PQ ciphertext'ini içerir. İkinci bölümde boş bir payload bulunur. Üçüncü bölüm payload'ı içerir.

#### Uzun Başlık

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Kısa Başlık

Değişiklikler: Mevcut ratchet, statik anahtarı ilk ChaCha bölümünde ve yükü ikinci bölümde içeriyordu. ML-KEM ile artık üç bölüm bulunmakta. İlk bölüm şifreli PQ genel anahtarını içeriyor. İkinci bölüm statik anahtarı içeriyor. Üçüncü bölüm yükü içeriyor.

Şifresi çözülmüş format:

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           ML-KEM encap_key            +
  |       ChaCha20 encrypted data         |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for encap_key Section        +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           X25519 Static Key           +
  |       ChaCha20 encrypted data         |
  +             32 bytes                  +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for Static Key Section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
Şifresi çözülmüş format:

```
Payload Part 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM encap_key                +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X25519 Static Key               +
  |                                       |
  +      (32 bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Boyutlar:

| Tür | Tür Kodu | X uzn | Msg 1 uzn | Msg 1 Şif uzn | Msg 1 Çöz uzn | PQ anahtar uzn | pl uzn |
|------|----------|-------|-----------|---------------|---------------|----------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Yükün bir DateTime bloğu içermesi gerektiğini, dolayısıyla minimum yük boyutunun 7 olduğunu unutmayın. Minimum mesaj 1 boyutları buna göre hesaplanabilir.

#### 1g) Yeni Oturum Yanıt formatı

Değişiklikler: Mevcut NTCP2 sadece ChaCha bölümündeki seçenekleri içeriyor. ML-KEM ile birlikte, ChaCha bölümü ayrıca şifrelenmiş PQ public key'i de içerecek.

Şifrelenmiş format:

```
  +----+----+----+----+----+----+----+----+
  |       Session Tag   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Ephemeral Public Key           +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | ChaCha20 encrypted ML-KEM ciphertext  |
  +      (see table below for length)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for ciphertext Section         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
Şifresi çözülmüş format:

```
Payload Part 1:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM ciphertext               +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  empty

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Boyutlar:

| Tip | Tip Kodu | Y uzunluğu | Msg 2 uzunluğu | Msg 2 Şif uzunluğu | Msg 2 Çöz uzunluğu | PQ CT uzunluğu | opt uzunluğu |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Mesaj 2'nin normalde sıfır olmayan bir yüke sahip olacağını, ancak ratchet spesifikasyonunun [/docs/specs/ecies/](/docs/specs/ecies/) bunu gerektirmediğini, dolayısıyla minimum yük boyutunun 0 olduğunu unutmayın. Minimum mesaj 2 boyutları buna göre hesaplanabilir.

### NTCP2

NTCP2 spesifikasyonunu [/docs/specs/ntcp2/](/docs/specs/ntcp2/) aşağıdaki şekilde güncelleyin:

#### Noise tanımlayıcıları

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Ham içerikler:

PQ ve PQ olmayan NTCP2'nin aynı router adresi ve portu üzerinde desteklenebilmesi için, X değerinin (X25519 geçici açık anahtarı) en anlamlı bitini bunun bir PQ bağlantısı olduğunu işaretlemek için kullanırız. Bu bit, PQ olmayan bağlantılar için her zaman sıfırlanmış durumdadır.

Not: PQ bağlantıları için bile, mesaj 1 seçenekler bloğundaki sürüm alanı 2 olarak ayarlanmalıdır.

Bob için, X'in AES gizleme çözme işleminden sonra, X[31] & 0x80'i test edin. Bit ayarlanmışsa, X[31] &= 0x7f ile temizleyin ve PQ bağlantısı olarak Noise ile şifreyi çözün. Bit temizse, her zamanki gibi PQ olmayan bağlantı olarak Noise ile şifreyi çözün.

Farklı bir router adresi ve portunda tanıtılan PQ NTCP2 için bu gerekli değildir.

Ek bilgi için, aşağıdaki Yayınlanan Adresler bölümüne bakın.

Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmemiş):

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmemiştir):

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar tür 4 olarak kalacak ve destek router adreslerinde belirtilecektir.

Boyutlar:

| Tip | Tip Kodu | X uzunluğu | Msg 1 uzunluğu | Msg 1 Şif uzunluğu | Msg 1 Çöz uzunluğu | PQ anahtar uzunluğu | seçenek uzunluğu |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar tip 4 olarak kalacak ve destek router adreslerinde belirtilecektir.

#### 2) SessionCreated

Ham içerikler:

Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmemiş):

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
Boyutlar:

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Boyutlar:

| Tip | Tip Kodu | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1168+pad | 1136 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar tip 4 olarak kalacak ve destek router adreslerinde belirtilecektir.

#### 3) SessionConfirmed

Değişmemiş

#### Anahtar Türetme Fonksiyonu (KDF) (veri aşaması için)

Değişmemiş

#### Yayınlanmış Adresler

Tüm durumlarda, her zamanki gibi NTCP2 transport adını kullanın.

PQ olmayan ve güvenlik duvarı olmayan ile aynı adres/bağlantı noktasını kullanın. Yalnızca bir PQ varyantı desteklenir. Router adresinde, her zamanki gibi v=2 ve MLKEM 512/768/1024'ü belirtmek için yeni pq=[3|4|5] parametresini yayınlayın. Alice, bunun hibrit bir bağlantı olduğunu belirtmek için oturum isteğinde geçici anahtarın MSB'sini (key[31] & 0x80) ayarlar. Yukarıya bakın. Eski router'lar pq parametresini yok sayar ve her zamanki gibi non-pq şekilde bağlanır.

Firewall'lu adresler (IP yayınlanmaz): Router adresinde, v=2 yayınlayın (her zamanki gibi). Bir pq parametresi yayınlamaya gerek yoktur.

Alice, kendi router bilgilerinde pq desteğinin reklamını yapıp yapmadığına veya aynı varyantın reklamını yapıp yapmadığına bakılmaksızın, Bob'un yayınladığı PQ varyantını kullanarak PQ Bob'a bağlanabilir.

Mevcut spesifikasyonda, 1 ve 2 numaralı mesajların "makul" miktarda dolgu içermesi tanımlanmıştır, 0-31 bayt aralığı önerilmekte ve maksimum değer belirtilmemektedir.

#### Maksimum Dolgu

API 0.9.68 (sürüm 2.11.0) aracılığıyla, Java I2P, PQ olmayan bağlantılar için maksimum 256 bayt padding uyguladı, ancak bu daha önce belgelenmemişti. API 0.9.69 (sürüm 2.12.0) itibariyle, Java I2P, PQ olmayan bağlantılar için MLKEM-512 ile aynı maksimum padding'i uygular. Aşağıdaki tabloya bakın.

Tanımlanan mesaj boyutunu maksimum padding olarak kullanın, yani maksimum padding PQ bağlantıları için mesaj boyutunu ikiye katlayacaktır, şu şekilde:

Tanımlanan mesaj boyutunu maksimum dolgu olarak kullanın; yani maksimum dolgu, PQ bağlantılarında mesaj boyutunu iki katına çıkaracaktır, aşağıdaki gibi:

| Mesaj Maksimum Padding | non-PQ (0.9.68'e kadar) | non-PQ (0.9.69 itibariyle) | MLKEM-512 | MLKEM-768 | MLKEM-1024 |
|------------------------|--------------------------|----------------------------|-----------|-----------|------------|
| Session Request        |   256                    |   880                      |    880    |     1264  |    1648    |
| Session Created        |   256                    |   848                      |    848    |     1136  |    1616    |
### SSU2

MLKEM-1024'ün SSU2 için desteklenmediğini unutmayın, çünkü anahtarlar standart 1500 baytlık datagram içine sığmayacak kadar büyüktür.

#### Noise tanımlayıcıları

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

Uzun başlık 32 bayttır. Bir oturum oluşturulmadan önce Token Request, SessionRequest, SessionCreated ve Retry için kullanılır. Ayrıca oturum-dışı Peer Test ve Hole Punch mesajları için de kullanılır.

#### İleri Gizlilik

Aşağıdaki mesajlarda, MLKEM-512 veya MLKEM-768'i belirtmek için uzun başlıktaki ver (sürüm) alanını 3 veya 4 olarak ayarlayın.

Aşağıdaki mesajlarda, MLKEM-512 veya MLKEM-768 desteklense bile, uzun başlıktaki ver (version) alanını her zamanki gibi 2 olarak ayarlayın. Uygulamalar, diğer uç bunu destekliyorsa değeri 3 veya 4 olarak da ayarlayabilir, ancak bu gerekli değildir. Uygulamalar 2-4 arası herhangi bir değeri kabul etmelidir.

- (0) Oturum İsteği
- (1) Oturum Oluşturuldu
- (9) Yeniden Deneme
- (10) Token İsteği
- (11) Delik Delme

Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmemiş):

- (7) Peer Test (oturum dışı mesajlar 5-7)

IP yükü dahil olmayan boyutlar:

- Relay İsteği
- Relay Yanıtı
- Relay Tanıtımı
- Eş Testi

Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar 4 türünde kalacak ve destek router adreslerinde belirtilecektir.

değişmemiş

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Yeni Oturum Boyutu

değişmedi

#### SessionRequest (Tip 0)

Spoof Koruması için KDF Değişikliği: Proposal 165 [Prop165]_'te ortaya çıkan sorunları ele almak için, ancak farklı bir çözümle, Session Request için KDF'yi değiştiriyoruz. Bu sadece PQ oturumları içindir. PQ olmayan oturumlar için KDF değişmeden kalır.

Ham içerikler:

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmemiş):

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmemiştir):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
MLKEM768_X25519 için minimum MTU: IPv4 için yaklaşık 1316 ve IPv6 için 1336.

| Tür | Tür Kodu | X uzunluk | Msg 1 uzunluk | Msg 1 Şif uzunluk | Msg 1 Çöz uzunluk | PQ anahtar uzunluk | pl uzunluk |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | çok büyük | | | | |
Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar tip 4 olarak kalacak ve destek router adreslerinde belirtilecektir.

Değişiklikler: Mevcut SSU2, ChaCha bölümünde yalnızca blok verilerini içerir. ML-KEM ile birlikte, ChaCha bölümü ayrıca şifrelenmiş PQ public key'i de içerecektir.

Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmiyor):

#### SessionCreated (Tip 1)

Ham içerik:

Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmemiş):

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (MLKEM)     |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (payload)   |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Boyutlar:

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
IP ek yükü dahil edilmeyerek boyutlar:

| Tür | Tür Kodu | Y len | Mesaj 2 len | Mesaj 2 Şifreli len | Mesaj 2 Şifresiz len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | çok büyük | | | | |
Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar tip 4 olarak kalacak ve destek router adreslerinde belirtilecektir.

Değişiklikler: Mevcut SSU2, ChaCha bölümünde yalnızca blok verilerini içerir. ML-KEM ile birlikte, ChaCha bölümü ayrıca şifrelenmiş PQ public key'i de içerecektir.

PQ İmzalar: Relay blokları, Peer Test blokları ve Peer Test mesajları hepsi imza içerir. Ne yazık ki, PQ imzalar MTU'dan daha büyüktür. Şu anda Relay veya Peer Test bloklarını ya da mesajlarını birden fazla UDP paketine parçalamak için bir mekanizma bulunmamaktadır. Protokol, parçalamayı destekleyecek şekilde genişletilmelidir. Bu, belirlenecek ayrı bir öneride yapılacaktır. Bu tamamlanana kadar, Relay ve Peer Test desteklenmeyecektir.

#### SessionConfirmed (Tip 2)

değişmedi

#### Veri aşaması için KDF

değişmedi

#### Relay ve Peer Testi

Aşağıdaki bloklar sürüm alanları içerir. Bunlar sürüm 2'de kalacak (PQ olmayan Bob ile uyumluluk için) ve PQ için sürüm 3/4'e değişmeyecek.

- SAMv3
- Bittorrent
- Geliştirici yönergeleri
- Adlandırma / adres defteri / jump sunucuları
- Diğer belgeler

Tüm durumlarda, SSU2 transport adını her zamanki gibi kullanın. MLKEM-1024 desteklenmez.

#### Yayınlanmış Adresler

PQ olmayan, güvenlik duvarı arkasında olmayan ile aynı adres/port'u kullanın. Bir veya her iki PQ varyantı desteklenir. Router adresinde, v=2 (her zamanki gibi) ve MLKEM 512/768/her ikisini belirtmek için yeni pq=[3|4|3,4] parametresini yayınlayın. Eski router'lar pq parametresini görmezden gelecek ve her zamanki gibi PQ olmayan bağlantı kuracaktır.

MLKEM768 ile MTU'yu aşmamaya dikkat edin. SSU2 için minimum MTU 1280'dir, bu da dolgu olmadan mesaj 1'in boyutudur. Alice veya Bob'un MTU'su 1280 ise mesaj 1'e dolgu eklemeyin.

Firewallı adresler (yayınlanan IP yok): Router adresinde, v=2 yayınlayın (her zamanki gibi). Relay desteği için pq parametresi firewallı adreslerde MUTLAKA yayınlanmalıdır.

Alice, kendi router bilgisinde pq desteğinin reklamını yapıp yapmadığına veya aynı varyantın reklamını yapıp yapmadığına bakılmaksızın, Bob'un yayınladığı PQ varyantını kullanarak bir PQ Bob'a bağlanabilir.

Mevcut spesifikasyonda, 1 ve 2 numaralı mesajların "makul" miktarda dolgu içermesi tanımlanmıştır, 0-31 bayt aralığı önerilmekte ve maksimum değer belirtilmemektedir.

#### MTU

Dahili olarak sürüm alanını kullanabilir ve MLKEM512 için 3, MLKEM768 için 4 kullanabiliriz.

### Streaming

Mesaj 1 ve 2 için, MLKEM768 paket boyutlarını 1280 minimum MTU'nun ötesine çıkaracaktır. MTU çok düşükse muhtemelen bu bağlantı için desteklenmeyecektir.

### SU3 Dosyaları

Mesaj 1 ve 2 için, MLKEM1024 paket boyutlarını 1500 maksimum MTU'nun ötesine çıkaracaktır. Bu, mesaj 1 ve 2'nin parçalanmasını gerektirecek ve büyük bir komplikasyon olacaktır. Muhtemelen yapılmayacak.

Relay ve Peer Testi: Yukarıya bakınız

TODO: İmzalama/doğrulama işlemlerini imzayı kopyalamaktan kaçınacak şekilde tanımlamanın daha verimli bir yolu var mı?

YAPILACAKLAR

[IETF taslağı](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) bölüm 8.1, uygulama karmaşıklıkları ve azalmış güvenlik nedeniyle X.509 sertifikalarında HashML-DSA kullanımını yasaklamakta ve HashML-DSA için OID atamamaktadır.

### Diğer Spesifikasyonlar

Yeni maksimum Destination boyutu 2599 olacaktır (base 64'te 3468).

SU3 dosyalarının Ed25519 ile imzalanmasına izin vermediğimizi ve Ed25519ph imzalamayı tanımlamış olmamıza rağmen, bunun için hiçbir zaman bir OID üzerinde anlaşmadığımızı veya kullanmadığımızı unutmayın.

- Eğer mesaj 1, 919 bayttan küçükse, mevcut ratchet protokolüdür.
- Eğer mesaj 1, 919 bayt veya daha büyükse, muhtemelen MLKEM512_X25519'dur.
  Önce MLKEM512_X25519'u deneyin, başarısız olursa mevcut ratchet protokolünü deneyin.

## Ek Yük Analizi

### Anahtar Değişimi

Normal imza türleri SU3 dosyaları için izin verilmez; ph (prehash) varyantlarını kullanın.

| Tür | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Yeni maksimum Destination boyutu 2599 olacaktır (base 64'te 3468).

Destination boyutları hakkında rehberlik veren diğer belgeleri güncelleyin, bunlar şunlardır:

| Tür | Göreli hız |
|------|------------|
| X25519 DH/keygen | temel |
| MLKEM512 | 2.25x daha hızlı |
| MLKEM768 | 1.5x daha hızlı |
| MLKEM1024 | 1x (aynı) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = %22 daha yavaş |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = %32 daha yavaş |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = %50 daha yavaş |
Boyut artışı (bayt):

| Tip | Göreceli DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | temel | temel | temel |
| MLKEM512 | 29x daha hızlı | 22x daha hızlı | 17x daha hızlı |
| MLKEM768 | 17x daha hızlı | 14x daha hızlı | 9x daha hızlı |
| MLKEM1024 | 12x daha hızlı | 10x daha hızlı | 6x daha hızlı |
### İmzalar

#### Boyutlar

[Cloudflare](https://blog.cloudflare.com/pq-2024/) tarafından bildirilen hızlar:

| Tip | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (her mesaj) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | temel | temel |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
#### Hızlar

Destination boyutları hakkında rehberlik veren diğer belgeleri güncelleyin, bunlar şunlardır:

| Tip | Göreceli hız işareti | doğrulama |
|------|---------------------|----------|
| EdDSA_SHA512_Ed25519 | temel seviye | temel seviye |
| MLDSA44 | 5x daha yavaş | 2x daha hızlı |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Boyut artışı (bayt):

| Tür | Göreceli hız işareti | doğrulama | anahtar üretimi |
|------|---------------------|-----------|-----------------|
| EdDSA_SHA512_Ed25519 | temel | temel | temel |
| MLDSA44 | 4,6x daha yavaş | 1,7x daha hızlı | 2,6x daha hızlı |
| MLDSA65 | 8,1x daha yavaş | aynı | 1,5x daha hızlı |
| MLDSA87 | 11,1x daha yavaş | 1,5x daha yavaş | aynı |
## Güvenlik Analizi

X25519 şifreleme türünün RI'ler için kullanıldığı varsayılarak tipik anahtar, imza, RIdent, Dest boyutları veya boyut artışları (referans için Ed25519 dahil edilmiştir). Bir Router Info, LeaseSet, yanıtlanabilir datagram'lar ve listelenen iki streaming (SYN ve SYN ACK) paketinin her biri için eklenen boyut. Mevcut Destination'lar ve LeaseSet'ler tekrarlanan dolgu içerir ve transit sırasında sıkıştırılabilir. Yeni türler dolgu içermez ve sıkıştırılamaz olacak, bu da transit sırasında çok daha yüksek boyut artışına neden olur. Yukarıdaki tasarım bölümüne bakınız.

| Kategori | Güvenlik Seviyesi |
|----------|-------------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### El Sıkışmalar

[Cloudflare](https://blog.cloudflare.com/pq-2024/) tarafından bildirilen hızlar:

Java'da ön test sonuçları:

| Algoritma | Güvenlik Kategorisi |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### İmzalar

NIST güvenlik kategorileri [NIST sunumu](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) slayt 10'da özetlenmiştir. Ön kriterler: Hibrit protokoller için minimum NIST güvenlik kategorimiz 2, PQ-only için 3 olmalıdır.

Bunların hepsi hibrit protokollerdir. Uygulamalar MLKEM768'i tercih etmelidir; MLKEM512 yeterince güvenli değildir.

| Algoritma | Güvenlik Kategorisi |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Tür Tercihleri

NIST güvenlik kategorileri [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

Bu öneri hem hibrit hem de sadece PQ imza türlerini tanımlar. MLDSA44 hibrit, sadece PQ olan MLDSA65'ten daha tercih edilir. MLDSA65 ve MLDSA87 için anahtar ve imza boyutları muhtemelen bizim için çok büyük, en azından başlangıçta.

NIST güvenlik kategorileri [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

3 kripto ve 9 imza türü tanımlayıp uygulayacağımız sırada, geliştirme sürecinde performansı ölçmeyi ve artan yapı boyutlarının etkilerini daha detaylı analiz etmeyi planlıyoruz. Ayrıca diğer projelerde ve protokollerdeki gelişmeleri araştırmaya ve takip etmeye devam edeceğiz.

Bir yıl veya daha fazla geliştirme sürecinden sonra, her kullanım durumu için tercih edilen bir tür veya varsayılan ayar üzerinde karar vermeye çalışacağız. Seçim, bant genişliği, CPU ve tahmini güvenlik seviyesi arasında ödünleşimler yapmayı gerektirecektir. Tüm türler her kullanım durumu için uygun olmayabilir veya izin verilmeyebilir.

Ön tercihler aşağıdaki gibidir, değişikliğe tabidir:

Şifreleme: MLKEM768_X25519

## Uygulama Notları

### Kütüphane Desteği

İmzalar: MLDSA44_EdDSA_SHA512_Ed25519

Ön kısıtlamalar aşağıdaki gibidir, değişikliğe tabidir:

### İmzalama Varyantları

Şifreleme: MLKEM1024_X25519, SSU2 için izin verilmiyor

İmzalar: MLDSA87 ve hibrit varyantı muhtemelen çok büyük; MLDSA65 ve hibrit varyantı çok büyük olabilir

### Güvenilirlik

Bouncycastle, BoringSSL ve WolfSSL kütüphaneleri artık MLKEM ve MLDSA'yı destekliyor. OpenSSL desteği 8 Nisan 2025'teki 3.5 sürümlerinde olacak [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Yapı Boyutları

Java I2P tarafından uyarlanan southernstorm.com Noise kütüphanesi hibrit el sıkışmalar için ön destek içeriyordu, ancak kullanılmadığı için kaldırdık; bunu geri ekleyip [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) ile eşleşecek şekilde güncellememiz gerekecek.

### NetDB

[FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) bölüm 3.4'te tanımlandığı gibi, "deterministik" varyant değil, "hedge edilmiş" veya rastgeleleştirilmiş imzalama varyantını kullanacağız. Bu, aynı veri üzerinde bile her imzanın farklı olmasını sağlar ve yan kanal saldırılarına karşı ek koruma sunar. [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), "hedge edilmiş" varyantın varsayılan olduğunu belirtse de, bu çeşitli kütüphanelerde geçerli olabilir veya olmayabilir. Uygulayıcılar, imzalama için "hedge edilmiş" varyantın kullanıldığından emin olmalıdır.

### Ratchet

#### Sorunlar

Normal imzalama sürecini (Pure ML-DSA Signature Generation olarak adlandırılır) kullanıyoruz, bu süreç mesajı dahili olarak 0x00 || len(ctx) || ctx || message şeklinde kodlar, burada ctx 0x00..0xFF boyutunda isteğe bağlı bir değerdir. Herhangi bir isteğe bağlı bağlam kullanmıyoruz. len(ctx) == 0. Bu süreç [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algoritma 2 adım 10 ve Algoritma 3 adım 5'te tanımlanmıştır. Yayınlanan bazı test vektörlerinin mesajın kodlanmadığı bir mod ayarlaması gerektirebileceğini unutmayın.

Boyut artışı, NetDB depolamaları, streaming el sıkışmaları ve diğer mesajlar için çok daha fazla tunnel fragmentasyonuna neden olacaktır. Performans ve güvenilirlik değişikliklerini kontrol edin.

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Router bilgilerinin ve leaseSet'lerin bayt boyutunu sınırlayan herhangi bir kodu bulun ve kontrol edin.

RAM'de veya diskte depolanan maksimum LS/RI sayısını gözden geçir ve muhtemelen azalt, depolama artışını sınırlamak için. floodfill'ler için minimum bant genişliği gereksinimlerini artır?

- Birden fazla MLKEM
- ElG + bir veya daha fazla MLKEM
- X25519 + bir veya daha fazla MLKEM
- ElG + X25519 + bir veya daha fazla MLKEM

Aynı tunnel'lar üzerinde birden fazla protokolün otomatik sınıflandırılması/tespiti, mesaj 1'in (New Session Message) uzunluk kontrolüne dayalı olarak mümkün olmalıdır. MLKEM512_X25519 örnek olarak alındığında, mesaj 1 uzunluğu mevcut ratchet protokolünden 816 bayt daha büyüktür ve minimum mesaj 1 boyutu (yalnızca DateTime payload dahil) 919 bayttır. Mevcut ratchet ile çoğu mesaj 1 boyutu 816 bayttan daha az payload'a sahiptir, bu nedenle hibrit olmayan ratchet olarak sınıflandırılabilirler. Büyük mesajlar muhtemelen nadiren görülen POST'lardır.

- Noise Hash seçimi - SHA256 ile devam mı yoksa yükseltme mi?
  SHA256'nın 20-30 yıl daha iyi olması gerekiyor, PQ tarafından tehdit edilmiyor,
  [NIST sunumuna](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) ve [NCCOE sunumuna](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) bakın.
  Eğer SHA256 kırılırsa daha kötü sorunlarımız olur (netdb).
- NTCP2 ayrı port, ayrı router adresi
- SSU2 relay / peer test
- SSU2 sürüm alanı
- SSU2 router adres sürümü

Bu nedenle önerilen strateji şudur:

Bu, daha önce aynı hedefte ElGamal ve ratchet'i desteklediğimiz gibi, aynı hedefte standart ratchet ve hibrit ratchet'i verimli bir şekilde desteklememizi sağlamalıdır. Dolayısıyla, aynı hedef için çift protokol desteği sunamasaydık olacağından çok daha hızlı bir şekilde MLKEM hibrit protokolüne geçiş yapabiliriz, çünkü mevcut hedeflere MLKEM desteği ekleyebiliriz.

Gerekli desteklenen kombinasyonlar şunlardır:

Aşağıdaki kombinasyonlar karmaşık olabilir ve desteklenmesi ZORUNLU DEĞİLDİR, ancak implementasyon-bağımlı olarak desteklenebilir:

#### Paylaşımlı Tunnel'lar

Aynı hedef üzerinde birden fazla MLKEM algoritmasını (örneğin, MLKEM512_X25519 ve MLKEM_768_X25519) desteklemeye çalışmayabiliriz. Sadece birini seçin; ancak bu, tercih edilen bir MLKEM varyantı seçmemize bağlıdır, böylece HTTP istemci tunnel'ları birini kullanabilir. Uygulama bağımlıdır.

#### Yeni Oturum Boyutu

Aynı hedef üzerinde üç algoritmayı (örneğin X25519, MLKEM512_X25519 ve MLKEM769_X25519) desteklemeye çalışabiliriz. Sınıflandırma ve yeniden deneme stratejisi çok karmaşık olabilir. Yapılandırma ve yapılandırma arayüzü çok karmaşık olabilir. Uygulamaya bağlıdır.

### NTCP2

Muhtemelen aynı hedef üzerinde ElGamal ve hibrit algoritmaları desteklemeye ÇALIŞMAYACAĞIZ. ElGamal eskimiştir ve ElGamal + hibrit sadece (X25519 yok) pek mantıklı değildir. Ayrıca, ElGamal ve Hibrit Yeni Oturum Mesajları her ikisi de büyüktür, bu nedenle sınıflandırma stratejileri genellikle her iki şifre çözme işlemini de denemek zorunda kalacaktır, bu da verimsiz olacaktır. Uygulamaya bağlıdır.

#### Gizleme

İstemciler aynı tunnel'lar üzerinde X25519 ve hibrit protokoller için aynı veya farklı X25519 statik anahtarları kullanabilirler, bu implementasyon-bağımlıdır.

ECIES spesifikasyonu, New Session Message yükünde Garlic Messages'a izin verir, bu da ilk streaming paketinin (genellikle bir HTTP GET) istemcinin leaseset'i ile birlikte 0-RTT teslimatını sağlar. Ancak, New Session Message yükü forward secrecy'ye sahip değildir. Bu öneri ratchet için gelişmiş forward secrecy'yi vurguladığından, implementasyonlar streaming yükünü veya tam streaming mesajını ilk Existing Session Message'a kadar erteleyebilir veya ertelemelidir. Bu, 0-RTT teslimatın pahasına olacaktır. Stratejiler ayrıca trafik türüne veya tunnel türüne, ya da örneğin GET vs. POST'a bağlı olabilir. Implementasyon-bağımlıdır.

MLKEM, MLDSA veya aynı hedefte her ikisi birden, yukarıda açıklandığı gibi New Session Message boyutunu dramatik şekilde artıracaktır. Bu, 1024 bayt tunnel mesajlarına parçalanması gereken tunnel'lar aracılığıyla New Session Message teslimatının güvenilirliğini önemli ölçüde azaltabilir. Teslimat başarısı, parça sayısının üstelsel oranıyla doğru orantılıdır. Uygulamalar, 0-RTT teslimat pahasına mesaj boyutunu sınırlamak için çeşitli stratejiler kullanabilir. Uygulamaya bağlıdır.

Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar tip 4 olarak kalacak ve destek router adreslerinde belirtilecektir.

### SSU2

Bunun hibrit bir bağlantı olduğunu belirtmek için oturum isteğinde geçici anahtarın MSB'sini (key[31] & 0x80) ayarlıyoruz. Bu, aynı port üzerinde hem standart NTCP hem de hibrit NTCP çalıştırmamıza olanak tanır. Yalnızca bir hibrit varyant desteklenecek ve router adresinde duyurulacaktır. Örneğin, v=2,3 veya v=2,4 veya v=2,5.

Bob olarak, de-obfuscation (gizleme kaldırma) işleminden sonra (X[31] & 0x80) != 0 olup olmadığını test edin. Eğer öyleyse, bu bir PQ bağlantısıdır.

Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar tip 4 olarak kalacak ve destek router adreslerinde belirtilecektir.

## Router Uyumluluğu

### Transport İsimleri

NTCP2-PQ için gereken minimum router sürümü henüz belirlenmemiştir.

### Router Şifreleme Türleri

Uzun başlıkta versiyon alanını kullanıyoruz ve MLKEM512 için 3, MLKEM768 için 4 olarak ayarlıyoruz. Adreste v=2,3,4 yeterli olacaktır.

#### Gizleme

SSU2'nin MLDSA-imzalı RI'yi birden fazla pakete (6-8?) bölünmüş şekilde işleyebilidiğini kontrol edin ve doğrulayın.

#### Tip 5/6/7 Router'lar

Not: Tip kodları yalnızca dahili kullanım içindir. Router'lar tip 4 olarak kalacak ve destek router adreslerinde belirtilecektir.

#### Tip 4 Router'lar

Her durumda, NTCP2 ve SSU2 transport isimlerini her zamanki gibi kullanın.

### Router İmza Türleri

#### Öneriler

Değerlendirmemiz gereken birkaç alternatifimiz var:

Önerilmez. Yalnızca yukarıda listelenen ve router türüyle eşleşen yeni aktarımları kullanın. Eski router'lar bağlanamaz, üzerinden tunnel kuramaz veya netDb mesajları gönderemez. Varsayılan olarak etkinleştirmeden önce hata ayıklama ve destek sağlanması için birkaç sürüm döngüsü alır. Aşağıdaki alternatiflere göre kullanıma sunumunu bir yıl veya daha fazla uzatabilir.

### LS Şifreleme Türleri

#### Tip 12-17 Router'lar

Önerilen. PQ, X25519 statik anahtarını veya N handshake protokollerini etkilemediğinden, router'ları tip 4 olarak bırakabilir ve sadece yeni transport'ları duyurabiliriz. Eski router'lar yine de bağlanabilir, tunnel'lar kurabilir veya netDb mesajları gönderebilir.

MLKEM-768, güvenlik ve anahtar uzunluğu arasındaki en iyi denge olarak Ratchet, NTCP2 ve SSU2 için önerilir.

### Hedef İmza Türleri

#### Tip 5-7 LS Anahtarları

Eski router'lar RI'ları doğrular ve bu nedenle bağlanamaz, üzerinden tunnel oluşturamaz veya netDb mesajları gönderemez. Varsayılan olarak etkinleştirmeden önce hata ayıklama ve destek sağlama için birkaç sürüm döngüsü gerekir. Enc. type 5/6/7 dağıtımıyla aynı sorunlar olur; yukarıda listelenen type 4 enc. type dağıtım alternatifine göre dağıtımı bir yıl veya daha fazla uzatabilir.

Önerilmez. Yalnızca yukarıda listelenen ve router türüyle eşleşen yeni aktarımları kullanın. Eski router'lar bağlanamaz, üzerinden tunnel kuramaz veya netDb mesajları gönderemez. Varsayılan olarak etkinleştirmeden önce hata ayıklama ve destek sağlanması için birkaç sürüm döngüsü alır. Aşağıdaki alternatiflere göre kullanıma sunumunu bir yıl veya daha fazla uzatabilir.

## Öncelikler ve Dağıtım

Alternatif yok.

Hedefler birden fazla anahtar türünü destekleyebilir, ancak yalnızca her anahtarla mesaj 1'in deneme şifre çözmelerini yaparak. Ek yük, her anahtar için başarılı şifre çözme sayılarını tutarak ve en çok kullanılan anahtarı önce deneyerek hafifletilebilir. Java I2P aynı hedef üzerinde ElGamal+X25519 için bu stratejiyi kullanır.

Router'lar leaseSet imzalarını doğrular ve bu nedenle tip 12-17 hedefler için bağlantı kuramaz veya leaseSet alamaz. Varsayılan olarak etkinleştirmeden önce hata ayıklama ve destek sağlanması için birkaç sürüm döngüsü gerekir.

Alternatif yok.

En değerli veriler, ratchet ile şifrelenmiş uçtan uca trafiklerdir. Tünel atlamaları arasındaki harici bir gözlemci olarak, bu veriler iki kez daha şifrelenir: tünel şifrelemesi ve taşıma şifrelemesi ile. OBEP ve IBGW arasındaki harici bir gözlemci olarak, yalnızca bir kez daha şifrelenir: taşıma şifrelemesi ile. Bir OBEP veya IBGW katılımcısı olarak, ratchet tek şifrelemedir. Ancak, tüneller tek yönlü olduğundan, ratchet el sıkışmasındaki her iki mesajı yakalamak, tüneller aynı router üzerinde OBEP ve IBGW ile kurulmadıkça, işbirlikçi router'lar gerektirir.

Kimlik doğrulama anahtarlarını makul bir süre içinde (örneğin birkaç ay) kırma ve ardından kimliğe bürünme veya neredeyse gerçek zamanlı şifre çözme şeklindeki PQ tehdit modeli çok daha uzak bir gelecekte mi? Ve işte o zaman PQC statik anahtarlara geçiş yapmak isteyeceğiz.

I2P'de MLDSA imza desteği, standart kuruluşlarının algoritmaları seçmesi, olası olarak anahtar ve/veya imza boyutlarını azaltması ve sektör benimsemesini teşvik etmesi beklenildiği için 2027'nin sonuna veya 2028'e kadar askıya alınmıştır. Bkz. [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/), [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/), ve [PLANTS](https://datatracker.ietf.org/wg/plants/about/). Ayrıca, MLDSA'nın sektörde benimsenmesi IETF, CA/Tarayıcı Forumu ve Sertifika Yetkilileri tarafından standartlaştırılacaktır. Sertifika Yetkililerinin öncelikle donanım güvenlik modülü (HSM) desteğine ihtiyacı var, ancak bu destek şu anda mevcut değil [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). IETF ve CA/Tarayıcı Forumu'nun, bileşik imzaların desteklenip desteklenmemesi de dahil olmak üzere belirli parametre seçimleri üzerine kararlar vermesini bekliyoruz [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Kilometre Taşı | Hedef |
|-----------|--------|
| Ratchet beta | 2025 sonu |
| En iyi şifreleme türünü seç | 2026 başı |
| NTCP2 beta | 2026 başı |
| SSU2 beta | 2026 ortası |
| Ratchet üretim | 2026 ortası |
| Ratchet varsayılan | 2026 sonu |
| İmza beta | 2026 sonu |
| NTCP2 üretim | 2026 sonu |
| SSU2 üretim | 2027 başı |
| En iyi imza türünü seç | 2027 başı |
| NTCP2 varsayılan | 2027 başı |
| SSU2 varsayılan | 2027 ortası |
| İmza üretim | 2027 ortası |
## Geçiş

Ratchet en yüksek önceliğe sahiptir. Transport'lar sonraki sırada gelir. İmzalar en düşük önceliğe sahiptir.

İmza dağıtımı da şifreleme dağıtımından bir yıl veya daha fazla geç olacaktır, çünkü geriye dönük uyumluluk mümkün değildir. Ayrıca, endüstride MLDSA benimsenimesi CA/Browser Forum ve Sertifika Otoriteleri tarafından standardize edilecektir. CA'lar önce donanım güvenlik modülü (HSM) desteğine ihtiyaç duymaktadır ve bu şu anda mevcut değildir [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). CA/Browser Forum'un kompozit imzaları destekleme veya zorunlu kılma dahil olmak üzere belirli parametre seçimlerinde kararları yönlendirmesini bekliyoruz [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

## Sorunlar

SHA256, kuantum sonrası tehditlerle karşı karşıya kalmadan başka 20-30 yıl kullanılabilir olmalıdır. Bkz. [NIST sunumu](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) ve [NCCOE sunumu](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf). SHA256 kırılırsa, daha ciddi sorunlarla karşılaşırız (netDb).

## Referanslar

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
