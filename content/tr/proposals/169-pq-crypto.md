---
title: "Post-Quantum Kripto Protokolleri"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Aç"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

## Genel Bakış

Uygun kuantum sonrası (PQ) kriptografi için araştırma ve rekabet on yıldır sürmekte olmasına rağmen, seçimler yakın zamana kadar net hale gelmemişti.

2022 yılında PQ kriptografisinin etkilerini incelemeye başladık [zzz.i2p](http://zzz.i2p/topics/3294).

TLS standartları son iki yılda hibrit şifreleme desteği ekledi ve Chrome ve Firefox'taki destek sayesinde artık internetteki şifreli trafiğin önemli bir bölümü için kullanılıyor [Cloudflare](https://blog.cloudflare.com/pq-2024/).

NIST yakın zamanda kuantum sonrası kriptografi için önerilen algoritmaları kesinleştirdi ve yayınladı [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Birçok yaygın kriptografi kütüphanesi artık NIST standartlarını destekliyor veya yakın gelecekte destek yayınlayacak.

Hem [Cloudflare](https://blog.cloudflare.com/pq-2024/) hem de [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) göçün derhal başlamasını öneriyor. Ayrıca 2022 NSA PQ SSS [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF) dokümanına da bakın. I2P güvenlik ve kriptografi alanında lider olmalıdır. Önerilen algoritmaları uygulamanın zamanı gelmiştir. Esnek kripto türü ve imza türü sistemimizi kullanarak, hibrit kripto için ve PQ ve hibrit imzalar için türler ekleyeceğiz.

## Hedefler

- PQ-dirençli algoritmaları seç
- Uygun yerlerde I2P protokollerine yalnızca-PQ ve hibrit algoritmaları ekle
- Birden fazla varyant tanımla
- Uygulama, test, analiz ve araştırma sonrasında en iyi varyantları seç
- Desteği aşamalı olarak ve geriye dönük uyumlulukla ekle

## Hedef Olmayanlar

- Tek yönlü (Noise N) şifreleme protokollerini değiştirmeyin
- SHA256'dan uzaklaşmayın, yakın vadede PQ tarafından tehdit edilmiyor
- Şu anda nihai tercih edilen varyantları seçmeyin

## Tehdit Modeli

- OBEP veya IBGW'deki router'lar, muhtemelen işbirliği yaparak,
  garlic mesajlarını daha sonra şifresini çözmek için saklama (forward secrecy)
- Ağ gözlemcileri
  aktarım mesajlarını daha sonra şifresini çözmek için saklama (forward secrecy)
- RI, LS, streaming, datagram'lar
  veya diğer yapılar için sahte imzalar üreten ağ katılımcıları

## Etkilenen Protokoller

Aşağıdaki protokolleri kabaca geliştirme sırasına göre değiştireceğiz. Genel dağıtım muhtemelen 2025 sonlarından 2027 ortalarına kadar sürecek. Ayrıntılar için aşağıdaki Öncelikler ve Dağıtım bölümüne bakın.

| Protocol / Feature | Status |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | Approved 2026-06; beta target 2025-08; release target 2025-11 |
| Hybrid MLKEM NTCP2 | Some details to be finalized |
| Hybrid MLKEM SSU2 | Some details to be finalized |
| MLDSA SigTypes 12-14 | Proposal is stable but may not be finalized until 2026 |
| MLDSA Dests | Tested on live net, requires net upgrade for floodfill support |
| Hybrid SigTypes 15-17 | Preliminary |
| Hybrid Dests | |
## Tasarım

NIST FIPS 203 ve 204 standartlarını destekleyeceğiz [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) - bunlar CRYSTALS-Kyber ve CRYSTALS-Dilithium'a (sürüm 3.1, 3 ve daha eskiler) dayanmakla birlikte bunlarla uyumlu DEĞİLDİR.

### Key Exchange

Aşağıdaki protokollerde hibrit anahtar değişimini destekleyeceğiz:

| Proto   | Noise Type | Support PQ only? | Support Hybrid? |
|---------|------------|------------------|-----------------|
| NTCP2   | XK         | no               | yes             |
| SSU2    | XK         | no               | yes             |
| Ratchet | IK         | no               | yes             |
| TBM     | N          | no               | no              |
| NetDB   | N          | no               | no              |
PQ KEM yalnızca geçici anahtarlar sağlar ve Noise XK ve IK gibi statik anahtar el sıkışmalarını doğrudan desteklemez.

Noise N iki yönlü anahtar değişimi kullanmaz ve bu nedenle hibrit şifreleme için uygun değildir.

Bu nedenle yalnızca hibrit şifrelemeyi destekleyeceğiz, NTCP2, SSU2 ve Ratchet için. [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) adresinde belirtildiği gibi üç ML-KEM varyantını tanımlayacağız, toplamda 3 yeni şifreleme türü için. Hibrit türler yalnızca X25519 ile kombinasyon halinde tanımlanacak.

Yeni şifreleme türleri şunlardır:

| Type | Code |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
Ek yük önemli ölçüde olacaktır. Tipik mesaj 1 ve 2 boyutları (XK ve IK için) şu anda yaklaşık 100 bayt civarındadır (herhangi bir ek payload öncesi). Bu, algoritmaya bağlı olarak 8x ila 15x artacaktır.

### Signatures

Aşağıdaki yapılarda PQ ve hibrit imzaları destekleyeceğiz:

| Type | Support PQ only? | Support Hybrid? |
|------|------------------|-----------------|
| RouterInfo | yes | yes |
| LeaseSet | yes | yes |
| Streaming SYN/SYNACK/Close | yes | yes |
| Repliable Datagrams | yes | yes |
| Datagram2 (prop. 163) | yes | yes |
| I2CP create session msg | yes | yes |
| SU3 files | yes | yes |
| X.509 certificates | yes | yes |
| Java keystores | yes | yes |
Bu nedenle hem PQ-only hem de hibrit imzaları destekleyeceğiz. [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) adresinde belirtildiği gibi üç ML-DSA varyantını, Ed25519 ile üç hibrit varyantı ve sadece SU3 dosyaları için prehash ile üç PQ-only varyantı tanımlayacağız, toplamda 9 yeni imza tipi olacak. Hibrit tipler yalnızca Ed25519 ile kombinasyon halinde tanımlanacak. SU3 dosyaları hariç, pre-hash varyantları (HashML-DSA) değil, standart ML-DSA kullanacağız.

[FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) bölüm 3.4'te tanımlandığı şekilde "deterministik" varyant değil, "hedged" veya rastgele imzalama varyantını kullanacağız. Bu, aynı veri üzerinde olsa bile her imzanın farklı olmasını sağlar ve yan kanal saldırılarına karşı ek koruma sunar. Kodlama ve bağlam dahil olmak üzere algoritma seçimleri hakkında ek ayrıntılar için aşağıdaki uygulama notları bölümüne bakın.

Yeni imza türleri şunlardır:

| Type | Code |
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
X.509 sertifikaları ve diğer DER kodlamaları, [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) adresinde tanımlanan bileşik yapıları ve OID'leri kullanacaktır.

Ek yük önemli ölçüde olacaktır. Tipik Ed25519 hedef ve router kimlik boyutları 391 bayttır. Bunlar algoritmaya bağlı olarak 3,5x ile 6,8x arasında artacaktır. Ed25519 imzaları 64 bayttır. Bunlar algoritmaya bağlı olarak 38x ile 76x arasında artacaktır. Tipik imzalı RouterInfo, LeaseSet, yanıtlanabilir datagramlar ve imzalı akış mesajları yaklaşık 1KB'dir. Bunlar algoritmaya bağlı olarak 3x ile 8x arasında artacaktır.

Yeni destination ve router kimlik türleri padding içermeyeceğinden, sıkıştırılabilir olmayacaklardır. Aktarım sırasında gzip ile sıkıştırılan destination'ların ve router kimliklerinin boyutları, algoritmaya bağlı olarak 12x - 38x artacaktır.

### Legal Combinations

Destination'lar için, yeni imza türleri leaseset'teki tüm şifreleme türleriyle desteklenir. Anahtar sertifikasındaki şifreleme türünü NONE (255) olarak ayarlayın.

RouterIdentities için ElGamal şifreleme türü kullanımdan kaldırılmıştır. Yeni imza türleri yalnızca X25519 (tür 4) şifrelemesi ile desteklenmektedir. Yeni şifreleme türleri RouterAddresses içinde belirtilecektir. Anahtar sertifikasındaki şifreleme türü tür 4 olmaya devam edecektir.

### New Crypto Required

- ML-KEM (eski adıyla CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (eski adıyla CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (eski adıyla Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Yalnızca SHAKE128 için kullanılır
- SHA3-256 (eski adıyla Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 ve SHAKE256 (SHA3-128 ve SHA3-256'nın XOF uzantıları) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

SHA3-256, SHAKE128 ve SHAKE256 için test vektörleri [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values) adresinde bulunmaktadır.

Java bouncycastle kütüphanesinin yukarıdakilerin tümünü desteklediğini unutmayın. C++ kütüphane desteği OpenSSL 3.5'te mevcuttur [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Alternatives

[FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+) desteklemeyeceğiz, ML-DSA'dan çok çok daha yavaş ve büyük. Yakında çıkacak olan FIPS206 (Falcon) desteklemeyeceğiz, henüz standartlaştırılmadı. NIST tarafından standartlaştırılmamış NTRU veya diğer PQ adaylarını desteklemeyeceğiz.

### Rosenpass

Wireguard'ı (IK) saf PQ kriptografiye uyarlama konusunda bazı araştırmalar [paper](https://eprint.iacr.org/2020/379.pdf) bulunmakta, ancak bu makalede çeşitli açık sorular var. Daha sonra, bu yaklaşım PQ Wireguard için Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) olarak uygulandı.

Rosenpass, önceden paylaşılmış Classic McEliece 460896 statik anahtarları (her biri 500 KB) ve Kyber-512 (esasen MLKEM-512) geçici anahtarları ile Noise KK benzeri bir el sıkışma kullanır. Classic McEliece şifreli metinleri yalnızca 188 bayt olduğundan ve Kyber-512 genel anahtarları ile şifreli metinleri makul boyutta olduğundan, her iki el sıkışma mesajı da standart bir UDP MTU'ya sığar. PQ KK el sıkışmasından çıkan paylaşılan anahtar (osk), standart Wireguard IK el sıkışması için giriş önceden paylaşılmış anahtar (psk) olarak kullanılır. Böylece toplamda iki tam el sıkışma vardır, biri tamamen PQ ve diğeri tamamen X25519.

XK ve IK el sıkışmalarımızı değiştirmek için bunların hiçbirini yapamayız çünkü:

- KK yapamayız, Bob'un Alice'in statik anahtarı yok
- 500KB statik anahtarlar çok büyük
- Ekstra bir round-trip istemiyoruz

Whitepaper'da çok fazla iyi bilgi var ve fikirlere ve ilhama kavuşmak için onu gözden geçireceğiz. TODO.

## Specification

### Anahtar Değişimi

Ortak yapılar belgesindeki [/docs/specs/common-structures/](/docs/specs/common-structures/) bölümleri ve tabloları aşağıdaki şekilde güncelleyin:

### İmzalar

Yeni Açık Anahtar türleri şunlardır:

| Type | Public Key Length | Since | Usage |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 800 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 1184 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM512_CT | 768 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| NONE | 0 | 0.9.xx | See proposal 169, for destinations with PQ sig types only, not for RIs or Leasesets |
Hibrit genel anahtarlar X25519 anahtarıdır. KEM genel anahtarları Alice'ten Bob'a gönderilen geçici PQ anahtarıdır. Kodlama ve bayt sırası [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) adresinde tanımlanmıştır.

MLKEM*_CT anahtarları gerçekte public anahtarlar değildir, bunlar Noise handshake'inde Bob'dan Alice'e gönderilen "ciphertext"lerdir. Eksiksizlik için burada listelenmiştir.

### Yasal Kombinasyonlar

Yeni Private Key türleri şunlardır:

| Type | Private Key Length | Since | Usage |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 1632 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 2400 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 3168 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
Hibrit özel anahtarlar X25519 anahtarlarıdır. KEM özel anahtarlar yalnızca Alice içindir. KEM kodlaması ve bayt sırası [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) adresinde tanımlanmıştır.

### Yeni Kripto Gerekli

Yeni İmzalama Genel Anahtarı türleri şunlardır:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 1344 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA65ph | 1984 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA87ph | 2624 | 0.9.xx | Only for SU3 files, not for netdb structures |
Hibrit imzalama genel anahtarları, [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) adresinde belirtildiği gibi, Ed25519 anahtarının ardından PQ anahtarının gelmesiyle oluşur. Kodlama ve bayt sırası [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) adresinde tanımlanmıştır.

### Alternatifler

Yeni İmzalama Özel Anahtar türleri şunlardır:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | See proposal 169 |
| MLDSA65 | 4032 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4896 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2592 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 4064 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4928 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
Hibrit imzalama özel anahtarları, [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) adresinde belirtildiği gibi Ed25519 anahtarını takip eden PQ anahtarıdır. Kodlama ve bayt sırası [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) adresinde tanımlanmıştır.

### Rosenpass

Yeni imza türleri şunlardır:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | See proposal 169 |
| MLDSA65 | 3309 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4627 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2484 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 3373 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4691 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
Hibrit imzalar, [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) adresinde belirtildiği gibi Ed25519 imzasının ardından PQ imzasının gelmesiyle oluşur. Hibrit imzalar her iki imzayı da doğrulayarak ve bunlardan herhangi biri başarısız olursa başarısız olarak sonuçlanır şekilde doğrulanır. Kodlama ve bayt sırası [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) adresinde tanımlanmıştır.

### Key Certificates

Yeni İmzalama Genel Anahtar türleri şunlardır:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA65ph | 19 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA87ph | 20 | n/a | 0.9.xx | Only for SU3 files |
Yeni Crypto Public Key türleri şunlardır:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| NONE | 255 | 0 | 0.9.xx | See proposal 169 |
Hibrit anahtar türleri anahtar sertifikalarına ASLA dahil edilmez; sadece leaseSet'lerde bulunur.

Hybrid veya PQ imza türlerine sahip hedefler için şifreleme türü olarak NONE (tip 255) kullanın, ancak kripto anahtarı yoktur ve 384 baytlık ana bölümün tamamı imzalama anahtarı içindir.

### Ortak Yapılar

Yeni Destination türleri için uzunluklar şunlardır. Tümü için Enc türü NONE (tür 255)'dir ve şifreleme anahtarı uzunluğu 0 olarak kabul edilir. Tüm 384-baytlık bölüm, imzalama public anahtarının ilk kısmı için kullanılır. NOT: Bu, kullanılmasa bile destination'da 256-baytlık ElGamal anahtarını koruduğumuz ECDSA_SHA512_P521 ve RSA imza türleri için belirtimden farklıdır.

Dolgu yok. Toplam uzunluk 7 + toplam anahtar uzunluğu. Anahtar sertifikası uzunluğu 4 + fazla anahtar uzunluğu.

MLDSA44 için örnek 1319-baytlık destination bayt akışı:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total Dest Length |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
### PublicKey

Yeni Destination türleri için uzunluklar aşağıdadır. Tümü için şifreleme türü X25519'dur (tür 4). X28819 genel anahtarından sonraki 352 baytlık bölümün tamamı, imzalama genel anahtarının ilk kısmı için kullanılır. Dolgu yoktur. Toplam uzunluk 39 + toplam anahtar uzunluğudur. Key certificate uzunluğu 4 + fazla anahtar uzunluğudur.

MLDSA44 için örnek 1351 baytlık router kimlik bayt akışı:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total RouterIdent Length |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PrivateKey

El sıkışmalar [Noise Protocol](https://noiseprotocol.org/noise.html) handshake kalıplarını kullanır.

Aşağıdaki harf eşleştirmesi kullanılmaktadır:

- e = tek kullanımlık geçici anahtar
- s = statik anahtar
- p = mesaj yükü
- e1 = tek kullanımlık geçici PQ anahtarı, Alice'den Bob'a gönderilen
- ekem1 = KEM şifreli metin, Bob'dan Alice'e gönderilen

Hibrit ileri gizlilik (hfs) için XK ve IK'ye yapılan aşağıdaki değişiklikler [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) bölüm 5'te belirtildiği gibidir:

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
e1 kalıbı, [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) bölüm 4'te belirtildiği üzere şu şekilde tanımlanır:

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
ekem1 deseni aşağıdaki gibi tanımlanmıştır, [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) bölüm 4'te belirtildiği üzere:

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
### SigningPublicKey

#### Issues

- Handshake hash fonksiyonunu değiştirmeli miyiz? Bkz. [comparison](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3).
  SHA256, PQ'ya karşı savunmasız değil, ancak hash fonksiyonumuzu yükseltmek istiyorsak,
  diğer şeyleri değiştirirken şimdi tam zamanı.
  Mevcut IETF SSH önerisi [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) SHA256 ile MLKEM768
  ve SHA384 ile MLKEM1024 kullanmak. Bu öneri
  güvenlik hususlarının tartışmasını da içeriyor.
- 0-RTT ratchet verisini (leaseSet dışında) göndermeyi bırakmalı mıyız?
- 0-RTT verisi göndermiyorsak ratchet'i IK'den XK'ya geçirmeli miyiz?

#### Overview

Bu bölüm hem IK hem de XK protokolleri için geçerlidir.

Hibrit el sıkışma [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) adresinde tanımlanmıştır. Alice'den Bob'a gönderilen ilk mesaj, mesaj yükünden önce e1 enkapsülasyon anahtarını içerir. Bu ek bir statik anahtar olarak ele alınır; (Alice olarak) EncryptAndHash() veya (Bob olarak) DecryptAndHash() çağrısı yapın. Ardından mesaj yükünü her zamanki gibi işleyin.

Bob'dan Alice'e gönderilen ikinci mesaj, mesaj yükünden önce ekem1 ve ciphertext'i içerir. Bu, ek bir statik anahtar olarak ele alınır; (Bob olarak) EncryptAndHash() veya (Alice olarak) DecryptAndHash() çağırın. Ardından, kem_shared_key'i hesaplayın ve MixKey(kem_shared_key) çağırın. Daha sonra mesaj yükünü her zamanki gibi işleyin.

#### Defined ML-KEM Operations

[FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) adresinde tanımlandığı şekilde kullanılan kriptografik yapı taşlarına karşılık gelen aşağıdaki fonksiyonları tanımlarız.

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

encap_key ve ciphertext'in her ikisinin de Noise handshake mesajları 1 ve 2'deki ChaCha/Poly blokları içinde şifrelendiğini unutmayın. Bunlar handshake işleminin bir parçası olarak şifresi çözülecektir.

kem_shared_key, MixHash() ile chaining key'e karıştırılır. Ayrıntılar için aşağıya bakın.

#### Alice KDF for Message 1

XK için: 'es' mesaj deseninden sonra ve yükten önce şunu ekle:

VEYA

IK için: 'es' mesaj kalıbından sonra ve 's' mesaj kalıbından önce şunları ekleyin:

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
#### Bob KDF for Message 1

XK için: 'es' mesaj deseninden sonra ve payload'dan önce, şunu ekle:

VEYA

IK için: 'es' mesaj deseninden sonra ve 's' mesaj deseninden önce, şunu ekleyin:

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
#### Bob KDF for Message 2

XK için: 'ee' mesaj deseninden sonra ve payload'dan önce, şunu ekle:

VEYA

IK için: 'ee' mesaj deseninden sonra ve 'se' mesaj deseninden önce, şunları ekleyin:

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
```
#### Alice KDF for Message 2

'ee' mesaj kalıbından sonra ('ss' mesaj kalıbından önce IK için), şunu ekleyin:

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
```
#### KDF for Message 3 (XK only)

değişmemiş

#### KDF for split()

değişmemiş

### SigningPrivateKey

ECIES-Ratchet spesifikasyonunu [/docs/specs/ecies/](/docs/specs/ecies/) aşağıdaki şekilde güncelleyin:

#### Noise identifiers

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1b) New session format (with binding)

Değişiklikler: Mevcut ratchet, statik anahtarı ilk ChaCha bölümünde ve payload'ı ikinci bölümde içeriyordu. ML-KEM ile artık üç bölüm var. İlk bölüm şifrelenmiş PQ public key'ini içeriyor. İkinci bölüm statik anahtarı içeriyor. Üçüncü bölüm payload'ı içeriyor.

Şifrelenmiş format:

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

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Payload'ın bir DateTime bloğu içermesi gerektiğini, dolayısıyla minimum payload boyutunun 7 olduğunu unutmayın. Minimum mesaj 1 boyutları buna göre hesaplanabilir.

#### 1g) New Session Reply format

Değişiklikler: Mevcut ratchet, ilk ChaCha bölümü için boş bir payload ve ikinci bölümde payload içerir. ML-KEM ile artık üç bölüm bulunmaktadır. İlk bölüm şifrelenmiş PQ ciphertext içerir. İkinci bölüm boş bir payload içerir. Üçüncü bölüm payload içerir.

Şifreli format:

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

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Mesaj 2'nin normalde sıfır olmayan bir payload'a sahip olacağını, ancak ratchet spesifikasyonunun [/docs/specs/ecies/](/docs/specs/ecies/) bunu gerektirmediğini, dolayısıyla minimum payload boyutunun 0 olduğunu unutmayın. Minimum mesaj 2 boyutları buna göre hesaplanabilir.

### İmza

NTCP2 spesifikasyonunu [/docs/specs/ntcp2/](/docs/specs/ntcp2/) aşağıdaki şekilde güncelleyin:

#### Noise identifiers

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Değişiklikler: Mevcut NTCP2 yalnızca ChaCha bölümündeki seçenekleri içerir. ML-KEM ile birlikte, ChaCha bölümü aynı zamanda şifrelenmiş PQ public key'i de içerecektir.

Ham içerikler:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly frame (options)          |
  +         32 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmedi):

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
Boyutlar:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | opt len |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar tür 4 olarak kalacak ve destek router adreslerinde belirtilecektir.

#### 2) SessionCreated

Değişiklikler: Mevcut NTCP2 yalnızca ChaCha bölümündeki seçenekleri içerir. ML-KEM ile birlikte, ChaCha bölümü ayrıca şifrelenmiş PQ public key'ini de içerecektir.

Ham içerikler:

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
  |   ChaChaPoly frame (MLKEM)            |
  +   Encrypted and authenticated data    +
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (options)          |
  +   Encrypted and authenticated data    +
  -           32 bytes                    -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Şifrelenmemiş veri (Poly1305 auth etiketi gösterilmemiş):

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

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |
Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar tip 4 olarak kalacak ve destek router adreslerinde belirtilecektir.

#### 3) SessionConfirmed

Değişmemiş

#### Key Derivation Function (KDF) (for data phase)

Değişmeden

### Anahtar Sertifikaları

SSU2 spesifikasyonunu [/docs/specs/ssu2/](/docs/specs/ssu2/) aşağıdaki şekilde güncelleyin:

#### Noise identifiers

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Long Header

Uzun başlık 32 bayttır. Bir oturum oluşturulmadan önce Token Request, SessionRequest, SessionCreated ve Retry için kullanılır. Ayrıca oturum-dışı Peer Test ve Hole Punch mesajları için de kullanılır.

TODO: Dahili olarak version alanını kullanabilir ve MLKEM512 için 3, MLKEM768 için 4 kullanabiliriz. Bunu sadece tip 0 ve 1 için mi yoksa tüm 6 tip için mi yapacağız?

Header şifrelemesinden önce:

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

  ver :: The protocol version, equal to 2
         TODO We could internally use the version field and use 3 for MLKEM512 and 4 for MLKEM768.

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Short Header

değişmemiş

#### SessionRequest (Type 0)

Değişiklikler: Mevcut SSU2, ChaCha bölümünde yalnızca blok verilerini içerir. ML-KEM ile ChaCha bölümü ayrıca şifrelenmiş PQ genel anahtarını da içerecektir.

Ham içerikler:

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
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Şifrelenmemiş veri (Poly1305 doğrulama etiketi gösterilmiyor):

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
Boyutlar, IP overhead dahil değil:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar 4 tipinde kalacak ve destek router adreslerinde belirtilecektir.

MLKEM768_X25519 için minimum MTU: IPv4 için yaklaşık 1316 ve IPv6 için 1336.

#### SessionCreated (Type 1)

Değişiklikler: Mevcut SSU2, ChaCha bölümünde yalnızca blok verisini içerir. ML-KEM ile birlikte, ChaCha bölümü ayrıca şifrelenmiş PQ public key'ini de içerecektir.

Ham içerikler:

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
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Şifrelenmemiş veri (Poly1305 auth tag gösterilmedi):

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
Boyutlar, IP ek yükü dahil değil:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar tip 4 olarak kalacak ve destek router adreslerinde belirtilecektir.

MLKEM768_X25519 için minimum MTU: IPv4 için yaklaşık 1316 ve IPv6 için 1336.

#### SessionConfirmed (Type 2)

değişmemiş

#### KDF for data phase

değişmedi

#### Sorunlar

Relay blokları, Peer Test blokları ve Peer Test mesajlarının hepsi imzalar içerir. Ne yazık ki, PQ imzaları MTU'dan daha büyüktür. Relay veya Peer Test bloklarını ya da mesajlarını birden fazla UDP paketine bölmek için şu anda bir mekanizma yoktur. Protokol, bölümleme (fragmentation) desteğini sağlamak için genişletilmelidir. Bu, ayrı bir öneride (TBD) yapılacaktır. Bu tamamlanana kadar, Relay ve Peer Test desteklenmeyecektir.

#### Genel Bakış

Dahili olarak version alanını kullanabilir ve MLKEM512 için 3, MLKEM768 için 4 değerlerini kullanabiliriz.

1 ve 2 numaralı mesajlar için, MLKEM768 paket boyutlarını 1280 minimum MTU'nun ötesinde artıracaktır. MTU çok düşükse muhtemelen o bağlantı için bunu desteklemeyecektir.

Mesaj 1 ve 2 için, MLKEM1024 paket boyutlarını 1500 maksimum MTU'nun ötesine çıkaracaktır. Bu, mesaj 1 ve 2'nin parçalanmasını gerektirecek ve büyük bir komplikasyon olacaktır. Muhtemelen yapmayacağız.

Relay ve Peer Test: Yukarıya bakın

### Hedef boyutları

TODO: İmzalama/doğrulama işlemlerini imzayı kopyalamaktan kaçınacak şekilde tanımlamanın daha verimli bir yolu var mı?

### RouterIdent boyutları

YAPILACAKLAR

[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) bölüm 8.1, uygulama karmaşıklıkları ve azaltılmış güvenlik nedeniyle HashML-DSA'nın X.509 sertifikalarında kullanılmasını yasaklar ve HashML-DSA için OID atamaz.

SU3 dosyalarının PQ-only imzaları için, sertifikalarda non-prehash varyantlarının [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) adresinde tanımlanan OID'lerini kullanın. SU3 dosyalarının hibrit imzalarını tanımlamıyoruz, çünkü dosyaları iki kez hash'lememiz gerekebilir (HashML-DSA ve X2559 aynı hash fonksiyonu SHA512'yi kullansa da). Ayrıca, X.509 sertifikasında iki anahtarı ve imzayı birleştirmek tamamen standart dışı olurdu.

SU3 dosyalarının Ed25519 imzalanmasına izin vermediğimizi ve Ed25519ph imzalamayı tanımlamış olmamıza rağmen, bunun için hiçbir zaman bir OID üzerinde anlaşmaya varmadığımızı veya kullanmadığımızı unutmayın.

Normal sig türleri SU3 dosyaları için izin verilmiyor; ph (prehash) varyantlarını kullanın.

### Handshake Kalıpları

Yeni maksimum Destination boyutu 2599 olacak (base 64'te 3468).

Destination boyutları hakkında rehberlik sağlayan diğer belgeleri güncelleyin, bunlar:

- SAMv3
- Bittorrent
- Geliştirici yönergeleri
- Adlandırma / adres defteri / atlama sunucuları
- Diğer belgeler

## Overhead Analysis

### Noise Handshake KDF

Boyut artışı (bayt):

| Type | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Hız:

[Cloudflare](https://blog.cloudflare.com/pq-2024/) tarafından bildirilen hızlar:

| Type | Relative speed |
|------|----------------|
| X25519 DH/keygen | baseline |
| MLKEM512 | 2.25x faster |
| MLKEM768 | 1.5x faster |
| MLKEM1024 | 1x (same) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower |
Java'da ön test sonuçları:

| Type | Relative DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | baseline | baseline | baseline |
| MLKEM512 | 29x faster | 22x faster | 17x faster |
| MLKEM768 | 17x faster | 14x faster | 9x faster |
| MLKEM1024 | 12x faster | 10x faster | 6x faster |
### Signatures

Boyut:

Tipik anahtar, imza, RIdent, Dest boyutları veya boyut artışları (Ed25519 referans için dahil edilmiştir) RI'ler için X25519 şifreleme türü varsayılarak. Router Info, LeaseSet, yanıtlanabilir datagramlar ve listelenen iki akış (SYN ve SYN ACK) paketinin her biri için eklenen boyut. Mevcut Destination'lar ve LeaseSet'ler tekrarlanan dolgu içerir ve transit sırasında sıkıştırılabilir. Yeni türler dolgu içermez ve sıkıştırılamaz olacak, bu da transit sırasında çok daha yüksek boyut artışı ile sonuçlanır. Yukarıdaki tasarım bölümüne bakın.

| Type | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (each msg) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
Hız:

[Cloudflare](https://blog.cloudflare.com/pq-2024/) tarafından bildirilen hızlar:

| Type | Relative speed sign | verify |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline |
| MLDSA44 | 5x slower | 2x faster |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Java'da ön test sonuçları:

| Type | Relative speed sign | verify | keygen |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline | baseline |
| MLDSA44 | 4.6x slower | 1.7x faster | 2.6x faster |
| MLDSA65 | 8.1x slower | same | 1.5x faster |
| MLDSA87 | 11.1x slower | 1.5x slower | same |
## Security Analysis

NIST güvenlik kategorileri [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) slayt 10'da özetlenmiştir. Ön kriterler: Hibrit protokoller için minimum NIST güvenlik kategorimiz 2, yalnızca PQ için 3 olmalıdır.

| Category | As Secure As |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

Bunların hepsi hibrit protokollerdir. Muhtemelen MLKEM768'i tercih etmek gerekir; MLKEM512 yeterince güvenli değildir.

NIST güvenlik kategorileri [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Signatures

Bu öneri hem hibrit hem de yalnızca PQ imza türlerini tanımlar. MLDSA44 hibrit, yalnızca PQ olan MLDSA65'ten daha tercih edilebilirdir. MLDSA65 ve MLDSA87 için anahtar ve imza boyutları bizim için muhtemelen çok büyük, en azından başlangıçta.

NIST güvenlik kategorileri [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Type Preferences

3 kriptografi türü ve 9 imza türü tanımlayıp uygulayacak olmamıza rağmen, geliştirme sürecinde performansı ölçmeyi ve artan yapı boyutlarının etkilerini daha ayrıntılı analiz etmeyi planlıyoruz. Ayrıca diğer projeler ve protokollerdeki gelişmeleri araştırmaya ve izlemeye devam edeceğiz.

Bir yıl veya daha fazla geliştirme sürecinden sonra, her kullanım durumu için tercih edilen bir tür veya varsayılan ayar belirlemeye çalışacağız. Seçim, bant genişliği, CPU ve tahmini güvenlik seviyesi arasında ödünleşimler yapmayı gerektirecektir. Tüm türler, her kullanım durumu için uygun olmayabilir veya izin verilmeyebilir.

Ön tercihler aşağıdaki gibidir ve değişikliğe tabidir:

Şifreleme: MLKEM768_X25519

İmzalar: MLDSA44_EdDSA_SHA512_Ed25519

Ön kısıtlamalar aşağıdaki gibidir, değişikliğe tabidir:

Şifreleme: MLKEM1024_X25519 SSU2 için izin verilmiyor

İmzalar: MLDSA87 ve hibrit varyantı muhtemelen çok büyük; MLDSA65 ve hibrit varyantı çok büyük olabilir

## Implementation Notes

### Library Support

Bouncycastle, BoringSSL ve WolfSSL kütüphaneleri artık MLKEM ve MLDSA'yı destekliyor. OpenSSL desteği 8 Nisan 2025'teki 3.5 sürümlerinde olacak [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

Java I2P tarafından uyarlanan southernstorm.com Noise kütüphanesi hibrit handshake'ler için ön destek içeriyordu, ancak kullanılmadığı için kaldırdık; bunu geri eklemek ve [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) ile eşleşecek şekilde güncellemek zorunda kalacağız.

### Signing Variants

[FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) bölüm 3.4'te tanımlandığı gibi "deterministik" varyant değil, "hedged" veya randomize edilmiş imzalama varyantını kullanacağız. Bu, aynı veri üzerinde olsa bile her imzanın farklı olmasını sağlar ve yan kanal saldırılarına karşı ek koruma sağlar. [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) "hedged" varyantının varsayılan olduğunu belirtse de, bu durum çeşitli kütüphanelerde geçerli olabilir veya olmayabilir. Geliştiriciler imzalama için "hedged" varyantının kullanıldığından emin olmalıdır.

Normal imzalama sürecini (Pure ML-DSA Signature Generation olarak adlandırılır) kullanıyoruz, bu süreç mesajı dahili olarak 0x00 || len(ctx) || ctx || message şeklinde kodlar, burada ctx 0x00..0xFF boyutunda isteğe bağlı bir değerdir. Herhangi bir isteğe bağlı bağlam kullanmıyoruz. len(ctx) == 0. Bu süreç [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algorithm 2 adım 10 ve Algorithm 3 adım 5'te tanımlanmıştır. Yayımlanmış bazı test vektörlerinin mesajın kodlanmadığı bir mod ayarlama gerektirebileceğini unutmayın.

### Reliability

Boyut artışı NetDB store'ları, streaming handshake'leri ve diğer mesajlar için çok daha fazla tunnel fragmentasyonuna neden olacaktır. Performans ve güvenilirlik değişikliklerini kontrol edin.

### Structure Sizes

Router info'ların ve leaseSet'lerin bayt boyutunu sınırlayan herhangi bir kodu bulun ve kontrol edin.

### NetDB

RAM'de veya diskte saklanan maksimum LS/RI sayısını gözden geçirin ve muhtemelen azaltın, depolama artışını sınırlamak için. Floodfill'ler için minimum bant genişliği gereksinimlerini artırın?

### Ratchet

#### Tanımlanmış ML-KEM İşlemleri

Aynı tüneller üzerinde birden fazla protokolün otomatik sınıflandırılması/tespiti, mesaj 1'in (Yeni Oturum Mesajı) uzunluk kontrolüne dayalı olarak mümkün olmalıdır. MLKEM512_X25519'u örnek olarak kullanırsak, mesaj 1 uzunluğu mevcut ratchet protokolünden 816 bayt daha büyüktür ve minimum mesaj 1 boyutu (yalnızca bir DateTime payload'u dahil edilmiş) 919 bayttır. Mevcut ratchet ile mesaj 1 boyutlarının çoğu 816 baytten küçük bir payload'a sahiptir, bu nedenle hibrit olmayan ratchet olarak sınıflandırılabilirler. Büyük mesajlar muhtemelen nadir olan POST'lardır.

Bu nedenle önerilen strateji şudur:

- Mesaj 1, 919 bayttan azsa, mevcut ratchet protokolüdür.
- Mesaj 1, 919 bayt veya daha fazlaysa, muhtemelen MLKEM512_X25519'dur.
  Önce MLKEM512_X25519'u deneyin ve başarısız olursa, mevcut ratchet protokolünü deneyin.

Bu, daha önce aynı hedef üzerinde ElGamal ve ratchet'i desteklediğimiz gibi, aynı hedef üzerinde standart ratchet ve hibrit ratchet'i verimli bir şekilde desteklememizi sağlamalıdır. Bu nedenle, aynı hedef için çift protokol desteği sağlayamazsak olacağından çok daha hızlı bir şekilde MLKEM hibrit protokolüne geçiş yapabiliriz, çünkü mevcut hedeflere MLKEM desteği ekleyebiliriz.

Desteklenmesi gereken kombinasyonlar şunlardır:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Aşağıdaki kombinasyonlar karmaşık olabilir ve desteklenmeleri zorunlu DEĞİLDİR, ancak uygulama-bağımlı olarak desteklenebilirler:

- Birden fazla MLKEM
- ElG + bir veya daha fazla MLKEM
- X25519 + bir veya daha fazla MLKEM
- ElG + X25519 + bir veya daha fazla MLKEM

Aynı hedef üzerinde birden fazla MLKEM algoritmasını (örneğin, MLKEM512_X25519 ve MLKEM_768_X25519) desteklemeye çalışmayabiliriz. Sadece birini seçin; ancak bu, tercih edilen bir MLKEM varyantını seçmemize bağlıdır, böylece HTTP istemci tünelleri birini kullanabilir. Uygulama-bağımlı.

Aynı hedef üzerinde üç algoritmayı (örneğin X25519, MLKEM512_X25519 ve MLKEM769_X25519) desteklemeye ÇALIŞABİLİRİZ. Sınıflandırma ve yeniden deneme stratejisi çok karmaşık olabilir. Yapılandırma ve yapılandırma arayüzü çok karmaşık olabilir. Uygulama-bağımlı.

Muhtemelen aynı hedef üzerinde ElGamal ve hibrit algoritmaları desteklemeye çalışmayacağız. ElGamal eskimiş durumda ve ElGamal + hibrit yalnız (X25519 yok) pek mantıklı değil. Ayrıca, ElGamal ve Hybrid New Session Messages'lar büyük olduğu için sınıflandırma stratejileri genellikle her iki şifre çözmeyi de denemek zorunda kalacak, bu da verimsiz olacaktır. Uygulama-bağımlı.

İstemciler, aynı tünellerde X25519 ve hibrit protokoller için aynı veya farklı X25519 statik anahtarlarını kullanabilir, uygulama bağımlıdır.

#### Alice KDF Mesaj 1 için

ECIES spesifikasyonu, New Session Message payload'ında Garlic Message'lara izin verir, bu da genellikle bir HTTP GET olan ilk streaming paketinin, istemcinin leaseset'i ile birlikte 0-RTT teslimatına olanak tanır. Ancak, New Session Message payload'ı forward secrecy'ye sahip değildir. Bu öneri ratchet için gelişmiş forward secrecy'yi vurguladığından, implementasyonlar streaming payload'ını veya tam streaming mesajını ilk Existing Session Message'a kadar erteleyebilir veya ertelemelidir. Bu, 0-RTT teslimatın pahasına olacaktır. Stratejiler ayrıca trafik türüne veya tunnel türüne, ya da örneğin GET'e karşı POST'a bağlı olabilir. Implementasyona bağlı.

#### Bob KDF Mesaj 1 için

MLKEM, MLDSA, veya her ikisinin aynı hedefte kullanılması, yukarıda açıklandığı gibi New Session Message'ın boyutunu önemli ölçüde artıracaktır. Bu, mesajların birden fazla 1024 baytlık tunnel mesajına bölünmesi gereken tüneller aracılığıyla New Session Message teslimatının güvenilirliğini önemli ölçüde azaltabilir. Teslimat başarısı, fragment sayısının üstel olarak artmasıyla ters orantılıdır. Uygulamalar, 0-RTT teslimatı pahasına mesaj boyutunu sınırlamak için çeşitli stratejiler kullanabilir. Uygulamaya bağlı.

### Ratchet

Oturum isteğinde geçici anahtarın MSB'sini (key[31] & 0x80) ayarlayarak bunun hibrit bir bağlantı olduğunu belirtebiliriz. Bu, aynı port üzerinde hem standart NTCP hem de hibrit NTCP çalıştırmamızı sağlayacaktır. Yalnızca bir hibrit varyantı desteklenecek ve router adresinde tanıtılacaktır. Örneğin, v=2,3 veya v=2,4 veya v=2,5.

Bunu yapmazsak, farklı transport adresi/portu ve "NTCP1PQ1" gibi yeni bir protokol adına ihtiyacımız olur.

Not: Tip kodları yalnızca dahili kullanım içindir. Router'lar tip 4 olarak kalacak ve destek router adreslerinde belirtilecektir.

YAPILACAKLAR

### SSU2

Farklı transport adresi/portu gerekebilir, ama umarım gerekmez, mesaj 1 için bayrakları olan bir header'ımız var. Dahili olarak version alanını kullanabilir ve MLKEM512 için 3, MLKEM768 için 4 kullanabiliriz. Belki adreste sadece v=2,3,4 yeterli olabilir. Ama her iki yeni algoritma için de tanımlayıcılara ihtiyacımız var: 3a, 3b?

SSU2'nin RI'nin birden fazla paket boyunca fragmente edilmesini (6-8?) işleyip işleyemediğini kontrol edin ve doğrulayın. i2pd şu anda maksimum sadece 2 fragment'i destekliyor mu?

Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar tip 4 olarak kalacak ve destek router adreslerinde belirtilecektir.

YAPILACAKLAR

## Router Compatibility

### Transport Names

Aynı port üzerinde hem standart hem de hibrit çalıştırabiliyorsak, versiyon bayrakları ile birlikte, muhtemelen yeni transport isimlerine ihtiyaç duymayacağız.

Yeni taşıma adlarına ihtiyaç duyarsak, bunlar şöyle olacaktır:

| Transport | Type |
|-----------|------|
| NTCP2PQ1 | MLKEM512_X25519 |
| NTCP2PQ2 | MLKEM768_X25519 |
| NTCP2PQ3 | MLKEM1024_X25519 |
| SSU2PQ1 | MLKEM512_X25519 |
| SSU2PQ2 | MLKEM768_X25519 |
SSU2'nin MLKEM1024'ü destekleyemeyeceğini unutmayın, çok büyük.

### Router Enc. Types

Değerlendirmemiz gereken birkaç alternatif bulunmaktadır:

#### Bob KDF for Mesaj 2

Önerilmez. Yalnızca yukarıda listelenen ve router türüyle eşleşen yeni aktarım protokollerini kullanın. Eski router'lar bağlanamaz, tunnel oluşturamaz veya netdb mesajları gönderemez. Varsayılan olarak etkinleştirmeden önce hata ayıklama ve destek sağlama için birkaç sürüm döngüsü gerekir. Aşağıdaki alternatiflere kıyasla kullanıma sunumu bir yıl veya daha fazla uzatabilir.

#### Alice KDF Mesaj 2 için

Önerilen. PQ, X25519 statik anahtarını veya N handshake protokollerini etkilemediğinden, router'ları tip 4 olarak bırakabilir ve sadece yeni transport'ları duyurabiliriz. Eski router'lar yine de bağlanabilir, tunnel oluşturabilir veya netDb mesajları gönderebilir.

#### Mesaj 3 için KDF (yalnızca XK)

Tip 4 router'lar hem NTCP2 hem de NTCP2PQ* adreslerini duyurabilir. Bunlar aynı statik anahtarı ve diğer parametreleri kullanabilir veya kullanmayabilir. Bunların muhtemelen farklı portlarda olması gerekecek; aynı portta hem NTCP2 hem de NTCP2PQ* protokollerini desteklemek çok zor olurdu, çünkü Bob'un gelen Session Request mesajını sınıflandırmasına ve çerçevelemesine izin verecek herhangi bir başlık veya çerçeveleme yoktur.

Ayrı portlar ve adresler Java için zor olacak ancak i2pd için basit olacak.

#### split() için KDF

Type 4 router'lar hem SSU2 hem de SSU2PQ* adreslerini duyurabilir. Eklenen başlık bayrakları ile Bob, ilk mesajda gelen taşıma türünü tanımlayabilir. Bu nedenle, aynı port üzerinde hem SSU2 hem de SSUPQ*'ı destekleyebiliriz.

Bunlar ayrı adresler olarak yayınlanabilir (i2pd'nin önceki geçişlerde yaptığı gibi) veya PQ desteğini belirten bir parametre ile aynı adres içinde yayınlanabilir (Java i2p'nin önceki geçişlerde yaptığı gibi).

Aynı adresteyse veya farklı adreslerde aynı porttaysa, bunlar aynı statik anahtarı ve diğer parametreleri kullanır. Farklı adresler ve farklı portlardaysa, bunlar aynı statik anahtarı ve diğer parametreleri kullanabilir veya kullanmayabilir.

Ayrı portlar ve adresler Java için zor olacak ancak i2pd için basit olacak.

#### Recommendations

YAPILACAKLAR

### NTCP2

#### Noise tanımlayıcıları

Eski router'lar RI'ları doğrular ve bu nedenle bağlanamaz, tunnel kuramaz veya netDb mesajları gönderemez. Varsayılan olarak etkinleştirmeden önce hata ayıklama ve destek sağlama için birkaç sürüm döngüsü gerekir. Enc. type 5/6/7 kullanıma sunumundaki ile aynı sorunlar olacaktır; yukarıda listelenen type 4 enc. type kullanıma sunumu alternatifine göre kullanıma sunumu bir yıl veya daha fazla uzatabilir.

Alternatif yok.

### LS Enc. Types

#### 1b) Yeni oturum formatı (bağlama ile)

Bunlar, eski tip 4 X25519 anahtarları ile leaseSet'te bulunabilir. Eski router'lar bilinmeyen anahtarları yok sayar.

Hedefler birden fazla anahtar türünü destekleyebilir, ancak yalnızca her anahtar ile mesaj 1'in deneme çözümlemeleri yaparak. Bu ek yük, her anahtar için başarılı çözümlemelerin sayısı tutularak ve en çok kullanılan anahtar önce denenerek azaltılabilir. Java I2P, aynı hedef üzerinde ElGamal+X25519 için bu stratejiyi kullanır.

### Dest. Sig. Types

#### 1g) Yeni Oturum Yanıt formatı

Router'lar leaseSet imzalarını doğrular ve bu nedenle tip 12-17 hedefler için bağlantı kuramaz veya leaseSet'ler alamaz. Varsayılan olarak etkinleştirmeden önce hata ayıklamak ve desteği sağlamak için birkaç sürüm döngüsü gerekir.

Alternatif yok.

## Spesifikasyon

En değerli veriler, ratchet ile şifrelenmiş uçtan uca trafiklerdir. Tunnel atlamaları arasındaki harici bir gözlemci olarak, bu veriler iki kez daha şifrelenir: tunnel şifrelemesi ve transport şifrelemesi ile. OBEP ve IBGW arasındaki harici bir gözlemci olarak, sadece bir kez daha transport şifrelemesi ile şifrelenir. Bir OBEP veya IBGW katılımcısı olarak, tek şifreleme ratchet'tir. Ancak, tunnel'lar tek yönlü olduğundan, ratchet el sıkışmasında her iki mesajı da yakalamak, OBEP ve IBGW'nin aynı router üzerinde inşa edilmiş tunnel'lar olmadığı sürece, işbirlikçi router'ları gerektirir.

Şu anda en endişe verici PQ tehdit modeli, trafiği bugün depolayıp çok çok yıl sonra şifresini çözmektir (forward secrecy). Hibrit bir yaklaşım bunu koruyabilir.

PQ tehdit modelinin kimlik doğrulama anahtarlarını makul bir süre içinde (diyelim ki birkaç ay) kırması ve ardından kimlik doğrulamayı taklit etmesi veya neredeyse gerçek zamanlı olarak şifre çözmesi çok daha uzak bir ihtimal mi? Ve işte o zaman PQC statik anahtarlara geçmek isteyeceğimiz zaman olacak.

Dolayısıyla, en erken PQ tehdit modeli OBEP/IBGW'nin trafiği daha sonra şifresini çözmek için depolamasıdır. Önce hybrid ratchet'ı uygulamamız gerekir.

Ratchet en yüksek önceliktir. Transport'lar bir sonrakidir. İmzalar en düşük önceliktir.

İmza dağıtımı da şifreleme dağıtımından bir yıl veya daha fazla sonra olacak, çünkü geriye dönük uyumluluk mümkün değil. Ayrıca, endüstride MLDSA benimsenmesi CA/Browser Forum ve Sertifika Otoriteleri tarafından standartlaştırılacak. CA'ların önce donanım güvenlik modülü (HSM) desteğine ihtiyacı var, bu da şu anda mevcut değil [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). CA/Browser Forum'un kompozit imzaların desteklenmesi veya zorunlu kılınması da dahil olmak üzere belirli parametre seçimlerinde kararları yönlendirmesini bekliyoruz [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Milestone | Target |
|-----------|--------|
| Ratchet beta | Late 2025 |
| Select best enc type | Early 2026 |
| NTCP2 beta | Early 2026 |
| SSU2 beta | Mid 2026 |
| Ratchet production | Mid 2026 |
| Ratchet default | Late 2026 |
| Signature beta | Late 2026 |
| NTCP2 production | Late 2026 |
| SSU2 production | Early 2027 |
| Select best sig type | Early 2027 |
| NTCP2 default | Early 2027 |
| SSU2 default | Mid 2027 |
| Signature production | Mid 2027 |
## Migration

Eğer aynı tunnel'larda hem eski hem de yeni ratchet protokollerini destekleyemezsek, geçiş çok daha zor olacaktır.

X25519'da yaptığımız gibi, kanıtlanması için sadece birini-sonra-diğerini deneyebilmeliyiz.

## Issues

- Noise Hash seçimi - SHA256 ile devam et mi yoksa yükseltme yapılsın mı?
  SHA256 20-30 yıl daha iyi olmalı, PQ tarafından tehdit edilmiyor,
  Bkz. [NIST presentation](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) ve [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  SHA256 kırılırsa daha kötü sorunlarımız var (netdb).
- NTCP2 ayrı port, ayrı router adresi
- SSU2 relay / peer test
- SSU2 sürüm alanı
- SSU2 router adres sürümü
