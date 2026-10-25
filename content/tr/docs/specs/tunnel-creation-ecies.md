---
title: "Tunnel Oluşturma Spesifikasyonu (ECIES-X25519)"
description: "İleri gizlilik için ECIES-X25519 kriptografik temel öğelerini kullanarak tunnel Build mesajı şifreleme."
slug: "tunnel-creation-ecies"
aliases:
  - "/tr/docs/specs/tunnel-creation-ecies-spec"
  - "/tr/docs/specs/tunnel-creation-ecies-spec/"
category: "Protokoller"
lastUpdated: "2025-06"
accurateFor: "0.9.66"
---

## Genel Bakış

Bu belge, [ECIES-X25519](/docs/specs/ecies/) tarafından tanıtılan kripto primitifleri kullanarak Tunnel Build mesaj şifrelemeyi belirtir. Bu, router'ları ElGamal'den ECIES-X25519 anahtarlarına dönüştürme için genel önerinin [Prop156](/proposals/156/) bir parçasıdır.

İki sürüm belirtilmiştir. İlki, ElGamal router'ları ile uyumluluk için mevcut build mesajlarını ve build kayıt boyutunu kullanır. Bu spesifikasyon 0.9.48 sürümünden itibaren uygulanmıştır ve artık kullanımdan kaldırılmıştır. İkincisi ise iki yeni build mesajı ve daha küçük bir build kayıt boyutu kullanır ve yalnızca ECIES router'ları ile kullanılabilir. Bu spesifikasyon 0.9.51 sürümünden itibaren uygulanmıştır.

Ağın ElGamal + AES256'dan ECIES + ChaCha20'ye geçişi amacıyla, karışık ElGamal ve ECIES router'lara sahip tunnel'ların kullanılması gereklidir. Karışık tunnel hop'larının işlenmesi için spesifikasyonlar sağlanmıştır. ElGamal hop'larının format, işleme veya şifreleme yöntemlerinde herhangi bir değişiklik yapılmayacaktır. Bu format, uyumluluk için gerekli olan tunnel build kayıtları için aynı boyutu korumaktadır.

ElGamal tunnel oluşturucuları her atlama için geçici X25519 anahtar çiftleri üretecek ve ECIES atlamaları içeren tunnel'ları oluşturmak için bu spesifikasyonu takip edecektir.

Bu belge ECIES-X25519 Tunnel Oluşturmayı belirtir. ECIES router'lar için gereken tüm değişikliklerin genel bakışı için 156 numaralı teklifi [Prop156](/proposals/156/) inceleyin. Uzun kayıt spesifikasyonunun gelişimi hakkında ek bilgi için 152 numaralı teklifi [Prop152](/proposals/152/) inceleyin. Kısa kayıt spesifikasyonunun gelişimi hakkında ek bilgi için 157 numaralı teklifi [Prop157](/proposals/157/) inceleyin.

### Kriptografik İlkeller

Bu spesifikasyonu uygulamak için gereken temel işlevler şunlardır:

- [Cryptography](/docs/specs/cryptography/) içerisindeki AES-256-CBC
- STREAM ChaCha20 fonksiyonları: ENCRYPT(k, iv, plaintext) ve DECRYPT(k, iv, ciphertext) - [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) ve [RFC-7539](https://tools.ietf.org/html/rfc7539) içerisindeki gibi
- STREAM ChaCha20/Poly1305 fonksiyonları: ENCRYPT(k, n, plaintext, ad) ve DECRYPT(k, n, ciphertext, ad) - [NTCP2](/docs/specs/ntcp2/), [ECIES-X25519](/docs/specs/ecies/) ve [RFC-7539](https://tools.ietf.org/html/rfc7539) içerisindeki gibi
- X25519 DH fonksiyonları - [NTCP2](/docs/specs/ntcp2/) ve [ECIES-X25519](/docs/specs/ecies/) içerisindeki gibi
- HKDF(salt, ikm, info, n) - [NTCP2](/docs/specs/ntcp2/) ve [ECIES-X25519](/docs/specs/ecies/) içerisindeki gibi

Başka yerde tanımlanmış diğer Noise fonksiyonları:

- MixHash(d) - [NTCP2](/docs/specs/ntcp2/) ve [ECIES-X25519](/docs/specs/ecies/)'de olduğu gibi
- MixKey(d) - [NTCP2](/docs/specs/ntcp2/) ve [ECIES-X25519](/docs/specs/ecies/)'de olduğu gibi

## Tasarım

### Noise Protocol Framework

Bu spesifikasyon, Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revizyon 34, 2018-07-11) tabanlı gereksinimleri sağlar. Noise terminolojisinde Alice başlatıcı (initiator), Bob ise yanıtlayıcı (responder) rolündedir.

Noise_N_25519_ChaChaPoly_SHA256 Noise protokolünü temel alır. Bu Noise protokolü aşağıdaki temel bileşenleri kullanır:

- Tek Yönlü El Sıkışma Deseni: N - Alice statik anahtarını Bob'a iletmez (N)
- DH Fonksiyonu: X25519 - [RFC-7748](https://tools.ietf.org/html/rfc7748)'de belirtildiği gibi 32 bayt anahtar uzunluğuna sahip X25519 DH
- Şifreleme Fonksiyonu: ChaChaPoly - [RFC-7539](https://tools.ietf.org/html/rfc7539) bölüm 2.8'de belirtildiği gibi AEAD_CHACHA20_POLY1305. İlk 4 baytı sıfır olarak ayarlanmış 12 baytlık nonce. [NTCP2](/docs/specs/ntcp2/)'dekiyle aynı
- Hash Fonksiyonu: SHA256 - I2P'de yaygın olarak kullanılan standart 32 baytlık hash

### El Sıkışma Kalıpları

El sıkışmaları [Noise](https://noiseprotocol.org/noise.html) el sıkışma desenlerini kullanır.

Aşağıdaki harf eşleştirmesi kullanılır:

- e = tek kullanımlık geçici anahtar
- s = statik anahtar
- p = mesaj yükü

Build isteği, Noise N kalıbıyla özdeştir. Bu aynı zamanda [NTCP2](/docs/specs/ntcp2/)'de kullanılan XK kalıbındaki ilk (Oturum İsteği) mesajıyla da özdeştir.

```
<- s
  ...
  e es p ->
```
### İstek Şifreleme

Yapı isteği kayıtları tunnel yaratıcısı tarafından oluşturulur ve bireysel hop'a asimetrik olarak şifrelenir. İstek kayıtlarının bu asimetrik şifrelemesi şu anda [Kriptografi](/docs/specs/cryptography/) bölümünde tanımlandığı gibi ElGamal'dir ve SHA-256 sağlama toplamı içerir. Bu tasarım forward-secret değildir.

ECIES tasarımı, ileri gizlilik, bütünlük ve kimlik doğrulama için ECIES-X25519 ephemeral-static DH, HKDF ve ChaCha20/Poly1305 AEAD ile tek yönlü Noise pattern "N" kullanır. Alice tunnel oluşturma talebinde bulunan taraftır. Tunnel'daki her hop bir Bob'dur.

### Yanıt Şifreleme

Build yanıt kayıtları, hop'ların yaratıcısı tarafından oluşturulur ve yaratıcıya simetrik olarak şifrelenir. ElGamal yanıt kayıtlarının bu simetrik şifrelemesi, öne eklenmiş SHA-256 sağlama toplamı ile birlikte AES kullanır. Bu tasarım ileri güvenlik sağlamaz.

ECIES yanıtları bütünlük ve kimlik doğrulama için ChaCha20/Poly1305 AEAD kullanır.

## Uzun Kayıt Spesifikasyonu

NOT: Kullanımdan kaldırılmış, eskimiş. Aşağıda belirtilen Kısa Kayıt formatını kullanın.

### Yapım İstek Kayıtları

Şifrelenmiş BuildRequestRecord'lar uyumluluk için hem ElGamal hem de ECIES için 528 bayttır.

#### İstek Kaydı Şifrelenmemiş

Bu, ECIES-X25519 router'ları için tunnel BuildRequestRecord spesifikasyonudur. Değişikliklerin özeti:

- Kullanılmayan 32-byte router hash'i kaldır
- İstek süresini saatten dakikaya değiştir
- Gelecekteki değişken tunnel süresi için son kullanma alanı ekle
- Flag'lar için daha fazla alan ekle
- Ek yapım seçenekleri için Mapping ekle
- AES-256 yanıt anahtarı ve IV, hop'un kendi yanıt kaydı için kullanılmaz
- Şifrelenmemiş kayıt daha uzun çünkü daha az şifreleme yükü var

İstek kaydı herhangi bir ChaCha yanıt anahtarı içermez. Bu anahtarlar bir KDF'den türetilir. Aşağıya bakın.

Tüm alanlar big-endian formatındadır.

Şifrelenmemiş boyut: 464 bayt

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40-71</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel layer key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">72-103</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel IV key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">104-135</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">136-151</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply IV</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">152</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">153-155</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">156-159</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">160-163</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">164-167</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">168-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-463</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding</td></tr>
</tbody>
</table>
flags alanı [Tunnel-Creation](/docs/specs/tunnel-creation/) bölümünde tanımlandığı gibidir ve şunları içerir:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
Bit 7, hop'un bir gelen ağ geçidi (IBGW) olacağını belirtir. Bit 6, hop'un bir giden uç nokta (OBEP) olacağını belirtir. Her iki bit de ayarlanmamışsa, hop ara bir katılımcı olacaktır. Her ikisi aynı anda ayarlanamaz.

İstek süresi, gelecekteki değişken tunnel süresi içindir. Şu an için desteklenen tek değer 600'dür (10 dakika).

Tunnel oluşturma seçenekleri, [Common](/docs/specs/common-structures/) içinde tanımlandığı şekilde bir Mapping yapısıdır. Şu anda tanımlanan tek seçenekler, API 0.9.65 itibarıyla bant genişliği parametreleri içindir, detaylar için aşağıya bakın. Mapping yapısı boşsa, bu iki bayt 0x00 0x00'dır. Mapping'in maksimum boyutu (uzunluk alanı dahil) 296 bayttır ve Mapping uzunluk alanının maksimum değeri 294'tür.

#### İstek Kaydı Şifrelenmiş

Geçici açık anahtar little-endian formatında olan dışında tüm alanlar big-endian formatındadır.

Şifrelenmiş boyut: 528 bayt

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Yanıt Kayıtlarını Oluştur

Şifreli BuildReplyRecord'lar hem ElGamal hem de ECIES için uyumluluk amacıyla 528 bayttır.

#### Yanıt Kaydı Şifrelenmemiş

Bu, ECIES-X25519 router'ları için tunnel BuildReplyRecord spesifikasyonudur. Değişikliklerin özeti:

- Build reply seçenekleri için eşleme ekle
- Şifrelenmemiş kayıt daha uzundur çünkü şifreleme ek yükü daha azdır

ECIES yanıtları ChaCha20/Poly1305 ile şifrelenir.

Tüm alanlar big-endian formatındadır.

Şifrelenmemiş boyut: 512 bayt

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-510</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
Tunnel build reply seçenekleri, [Common](/docs/specs/common-structures/) içinde tanımlandığı gibi bir Mapping yapısıdır. Şu anda tanımlanan tek seçenekler, API 0.9.65 itibarıyla bant genişliği parametreleri içindir, ayrıntılar için aşağıya bakın. Mapping yapısı boşsa, bu iki bayt 0x00 0x00'dır. Mapping'in maksimum boyutu (uzunluk alanı dahil) 511 bayttır ve Mapping uzunluk alanının maksimum değeri 509'dur.

Yanıt byte'ı, parmak izi bırakmayı önlemek için [Tunnel-Creation](/docs/specs/tunnel-creation/) içinde tanımlandığı şekilde aşağıdaki değerlerden biridir:

- 0x00 (kabul et)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Yanıt Kaydı Şifrelenmiş

Şifrelenmiş boyut: 528 bayt

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
ECIES kayıtlarına tam geçiş sonrasında, aralıklı dolgu kuralları istek kayıtları ile aynıdır.

### Kayıtların Simetrik Şifrelemesi

Karma tüneller ElGamal'dan ECIES'e geçiş için izin verilir ve gereklidir. Geçiş dönemi boyunca, artan sayıda router ECIES anahtarları altında anahtarlanacaktır.

Simetrik kriptografi ön işleme aynı şekilde çalışacaktır:

- "encryption":
  - şifre çözme modunda çalıştırılan cipher
  - ön işlemede proaktif olarak şifresi çözülen istek kayıtları (şifrelenmiş istek kayıtlarını gizler)
- "decryption":
  - şifreleme modunda çalıştırılan cipher
  - katılımcı hop'lar tarafından şifrelenen istek kayıtları (sonraki düz metin istek kaydını ortaya çıkarır)
- ChaCha20'nin "modları" yoktur, bu yüzden basitçe üç kez çalıştırılır:
  - bir kez ön işlemede
  - bir kez hop tarafından
  - bir kez son yanıt işlemede

Karışık tunnel'lar kullanıldığında, tunnel oluşturucuların BuildRequestRecord'un simetrik şifrelemesini mevcut ve önceki hop'un şifreleme türüne dayandırması gerekecektir.

Her hop, BuildReplyRecord'ları ve VariableTunnelBuildMessage (VTBM) içindeki diğer kayıtları şifrelemek için kendi şifreleme türünü kullanacaktır.

Yanıt yolunda, uç nokta (gönderen) her hop'un yanıt anahtarını kullanarak [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption)'ı geri almak zorunda kalacaktır.

Açıklayıcı bir örnek olarak, ElGamal ile çevrelenmiş ECIES'li bir giden tunnel'a bakalım:

- Gönderen (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Tüm BuildRequestRecord'lar şifrelenmiş durumlarında bulunur (ElGamal veya ECIES kullanarak).

AES256/CBC şifrelemesi kullanıldığında, her kayıt için ayrı ayrı kullanılır ve birden fazla kayıt arasında zincirleme yapılmaz.

Benzer şekilde, ChaCha20 tüm VTBM boyunca akış yapmak yerine her kaydı şifrelemek için kullanılacaktır.

İstek kayıtları Gönderici (OBGW) tarafından ön işleme tabi tutulur:

- H3'ün kaydı şunlar kullanılarak "şifrelenir":
  - H2'nin yanıt anahtarı (ChaCha20)
  - H1'in yanıt anahtarı (AES256/CBC)
- H2'nin kaydı şunlar kullanılarak "şifrelenir":
  - H1'in yanıt anahtarı (AES256/CBC)
- H1'in kaydı simetrik şifreleme olmadan gönderilir

Sadece H2 yanıt şifreleme bayrağını kontrol eder ve bunun AES256/CBC ile takip edildiğini görür.

Her hop tarafından işlendikten sonra, kayıtlar "şifresi çözülmüş" durumda bulunur:

- H3'ün kaydı şunlar kullanılarak "şifreleri çözülür":
  - H3'ün yanıt anahtarı (AES256/CBC)
- H2'nin kaydı şunlar kullanılarak "şifreleri çözülür":
  - H3'ün yanıt anahtarı (AES256/CBC)
  - H2'nin yanıt anahtarı (ChaCha20-Poly1305)
- H1'in kaydı şunlar kullanılarak "şifreleri çözülür":
  - H3'ün yanıt anahtarı (AES256/CBC)
  - H2'nin yanıt anahtarı (ChaCha20)
  - H1'in yanıt anahtarı (AES256/CBC)

Tunnel oluşturucusu, yani Inbound Endpoint (IBEP), yanıtı işler:

- H3'ün kaydı şunlar kullanılarak "şifrelenir":
  - H3'ün yanıt anahtarı (AES256/CBC)
- H2'nin kaydı şunlar kullanılarak "şifrelenir":
  - H3'ün yanıt anahtarı (AES256/CBC)
  - H2'nin yanıt anahtarı (ChaCha20-Poly1305)
- H1'in kaydı şunlar kullanılarak "şifrelenir":
  - H3'ün yanıt anahtarı (AES256/CBC)
  - H2'nin yanıt anahtarı (ChaCha20)
  - H1'in yanıt anahtarı (AES256/CBC)

### İstek Kayıt Anahtarları

Bu anahtarlar ElGamal BuildRequestRecords içinde açıkça dahil edilir. ECIES BuildRequestRecords için, tunnel anahtarları ve AES yanıt anahtarları dahil edilir, ancak ChaCha yanıt anahtarları DH değişiminden türetilir. Router statik ECIES anahtarlarının ayrıntıları için [Prop156](/proposals/156/) bölümüne bakın.

Aşağıda, daha önce istek kayıtlarında iletilen anahtarların nasıl türetileceğine dair bir açıklama bulunmaktadır.

#### Başlangıç ck ve h için KDF

Bu, "N" deseni için standart [NOISE](https://noiseprotocol.org/noise.html) protokolü ve standart protokol adıdır.

```
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

ElGamal tunnel oluşturucuları, tunnel'daki her ECIES hop'u için geçici bir X25519 anahtar çifti oluşturur ve BuildRequestRecord'larını şifrelemek için yukarıdaki şemayı kullanır. ElGamal tunnel oluşturucuları, ElGamal hop'larına şifrelemek için bu spesifikasyondan önceki şemayı kullanacaktır.

ECIES tunnel oluşturucuları, [Tunnel-Creation](/docs/specs/tunnel-creation/) bölümünde tanımlanan şemayı kullanarak her ElGamal hop'un genel anahtarına şifreleme yapması gerekecektir. ECIES tunnel oluşturucuları, ECIES hop'larına şifreleme yapmak için yukarıdaki şemayı kullanacaktır.

Bu, tunnel hoplarının yalnızca aynı şifreleme türünden gelen şifrelenmiş kayıtları göreceği anlamına gelir.

ElGamal ve ECIES tunnel oluşturucuları için, ECIES hop'larına şifreleme yapmak üzere hop başına benzersiz geçici X25519 anahtar çiftleri üreteceklerdir.

**ÖNEMLİ**: Ephemeral anahtarlar her ECIES hop'u için ve her build kaydı için benzersiz olmalıdır. Benzersiz anahtarlar kullanmamak, işbirliği yapan hop'ların aynı tunnel'da olduklarını doğrulamaları için bir saldırı vektörü oluşturur.

```
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
`replyKey`, `layerKey` ve `layerIV` hala ElGamal kayıtlarının içinde bulunmalıdır ve rastgele oluşturulabilir.

### Yanıt Kaydı Şifreleme

Yanıt kaydı ChaCha20/Poly1305 ile şifrelenmiştir.

```
// AEAD parameters
k = chainkey from build request
n = 0
plaintext = 512 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
## Kısa Kayıt Spesifikasyonu

Bu spesifikasyon iki yeni I2NP tunnel inşa mesajı kullanır: Short Tunnel Build Message (tip 25) ve Outbound Tunnel Build Reply Message (tip 26).

Tunnel yaratıcısı ve yaratılan tunnel'daki tüm atlamalar ECIES-X25519 desteklemeli ve en az 0.9.51 sürümünde olmalıdır. Yanıt tunnel'ındaki atlamalar (giden yapım için) veya giden tunnel'daki atlamalar (gelen yapım için) herhangi bir gereksinimi yoktur.

Şifrelenmiş istek ve yanıt kayıtları 218 bayt olacak, diğer tüm yapı mesajları için 528 bayta kıyasla.

Düz metin istek kayıtları 154 bayt olacak, ElGamal kayıtları için 222 bayt ve yukarıda tanımlandığı şekilde ECIES kayıtları için 464 bayt ile karşılaştırıldığında.

Düz metin yanıt kayıtları 202 bayt olacaktır, ElGamal kayıtları için 496 bayt ve yukarıda tanımlandığı gibi ECIES kayıtları için 512 bayt ile karşılaştırıldığında.

Yanıt şifrelemesi, hop'un kendi kaydı için ChaCha20/Poly1305 olacak ve build mesajındaki diğer kayıtlar için ChaCha20 (ChaCha20/Poly1305 DEĞİL) olacaktır.

İstek kayıtları, katman ve yanıt anahtarlarını oluşturmak için HKDF kullanılarak daha küçük hale getirilecektir, böylece bunlar istekte açıkça yer almayacaktır.

### Mesaj Akışı

```
STBM: Short tunnel build message (type 25)
OTBRM: Outbound tunnel build reply message (type 26)

Outbound Build A-B-C
Reply through existing inbound D-E-F


                New Tunnel
         STBM      STBM      STBM
Creator ------> A ------> B ------> C ---\
                                   OBEP   \
                                          | Garlic wrapped (optional)
                                          | OTBRM
                                          | (TUNNEL delivery)
                                          | from OBEP to
                                          | creator
              Existing Tunnel             /
Creator <-------F---------E-------- D <--/
                                   IBGW



Inbound Build D-E-F
Sent through existing outbound A-B-C


              Existing Tunnel
Creator ------> A ------> B ------> C ---\
                                  OBEP    \
                                          | Garlic wrapped (optional)
                                          | STBM
                                          | (ROUTER delivery)
                                          | from creator
                New Tunnel                | to IBGW
          STBM      STBM      STBM        /
Creator <------ F <------ E <------ D <--/
                                   IBGW
```
#### Notlar

Mesajların garlic sarmalama ile gizlenmesi onları OBEP'ten (gelen yönlü yapım için) veya IBGW'den (giden yönlü yapım için) saklar. Bu önerilir ancak zorunlu değildir. Eğer OBEP ve IBGW aynı router ise, gerekli değildir.

### Kısa Yapı İsteği Kayıtları

Kısa şifrelenmiş BuildRequestRecord'lar 218 bayttır.

#### Kısa İstek Kaydı Şifrelenmemiş

Uzun kayıtlardan değişikliklerin özeti:

- Şifrelenmemiş uzunluğu 464 bayttan 154 bayta değiştir
- Şifrelenmiş uzunluğu 528 bayttan 218 bayta değiştir
- Katman ve yanıt anahtarlarını ve IV'leri kaldır, bunlar bir KDF'den üretilecek

İstek kaydı herhangi bir ChaCha yanıt anahtarı içermez. Bu anahtarlar bir KDF'den türetilir. Aşağıya bakınız.

Tüm alanlar big-endian formatındadır.

Şifrelenmemiş boyut: 154 bayt.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">41-42</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">43</td><td style="border:1px solid var(--color-border); padding:0.6rem;">layer encryption type</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">44-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-51</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">52-55</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">56-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-153</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding (see below)</td></tr>
</tbody>
</table>
Flags alanı [Tunnel-Creation](/docs/specs/tunnel-creation/) bölümünde tanımlandığı gibidir ve aşağıdakileri içerir:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
Bit 7, hop'un bir inbound gateway (IBGW) olacağını gösterir. Bit 6, hop'un bir outbound endpoint (OBEP) olacağını gösterir. Her iki bit de ayarlanmamışsa, hop ara katılımcı olacaktır. İkisi birden ayarlanamaz.

Katman şifreleme türü: 0 AES için (mevcut tunnel'larda olduğu gibi); 1 gelecek için (ChaCha?)

İstek sona erme süresi gelecekteki değişken tunnel süresi içindir. Şu an için desteklenen tek değer 600'dür (10 dakika).

Yaratıcı geçici public key, big-endian formatında bir ECIES anahtarıdır. IBGW katmanı ve yanıt anahtarları ile IV'ler için KDF'de kullanılır. Bu yalnızca Inbound Tunnel Build mesajındaki düz metin kaydına dahil edilir. Bu katmanda build kaydı için DH bulunmadığından gereklidir.

Tunnel oluşturma seçenekleri, [Common](/docs/specs/common-structures/) bölümünde tanımlandığı şekilde bir Mapping yapısıdır. Şu anda tanımlanmış olan tek seçenekler API 0.9.65 itibariyle bant genişliği parametreleri içindir, ayrıntılar için aşağıya bakınız. Mapping yapısı boşsa, bu iki bayt 0x00 0x00'dır. Mapping'in maksimum boyutu (uzunluk alanı dahil) 98 bayttır ve Mapping uzunluk alanının maksimum değeri 96'dır.

#### Kısa İstek Kaydı Şifrelenmiş

Geçici public key little-endian olan dışında tüm alanlar big-endian'dır.

Şifrelenmiş boyut: 218 bayt

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Kısa Yapı Yanıt Kayıtları

Kısa şifrelenmiş BuildReplyRecords 218 bayttır.

#### Kısa Yanıt Kaydı Şifrelenmemiş

Uzun kayıtlardan yapılan değişikliklerin özeti:

- Şifrelenmemiş uzunluğu 512 bayttan 202 bayta değiştir
- Şifrelenmiş uzunluğu 528 bayttan 218 bayta değiştir

ECIES yanıtları ChaCha20/Poly1305 ile şifrelenir.

Tüm alanlar big-endian formatındadır.

Şifrelenmemiş boyut: 202 bayt.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-200</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding (see below)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
Tunnel build reply seçenekleri, [Common](/docs/specs/common-structures/) bölümünde tanımlandığı şekilde bir Mapping yapısıdır. Şu anda tanımlanmış olan tek seçenekler, API 0.9.65 itibariyle bant genişliği parametreleri içindir, detaylar için aşağıya bakınız. Mapping yapısı boşsa, bu iki bayt 0x00 0x00'dır. Mapping'in maksimum boyutu (uzunluk alanı dahil) 201 bayttır ve Mapping uzunluk alanının maksimum değeri 199'dur.

Yanıt baytı, parmak izi bırakmayı önlemek için [Tunnel-Creation](/docs/specs/tunnel-creation/) belgesinde tanımlanan aşağıdaki değerlerden biridir:

- 0x00 (kabul et)
- 30 (TUNNEL_REJECT_BANDWIDTH)

Desteklenmeyen seçenekler için reddetmeyi temsil etmek üzere gelecekte ek bir yanıt değeri tanımlanabilir.

#### Kısa Yanıt Kaydı Şifrelenmiş

Şifrelenmiş boyut: 218 byte

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### KDF

Tunnel inşa kaydı şifreleme/şifre çözme işleminden sonra Noise durumundan gelen zincirleme anahtarı (ck) kullanarak şu anahtarları türetiyoruz: yanıt anahtarı, AES katman anahtarı, AES IV anahtarı ve OBEP için garlic yanıt anahtarı/etiketi.

Reply anahtarları: KDF'nin OBEP ve OBEP olmayan atlamalar için biraz farklı olduğunu unutmayın. Uzun kayıtların aksine, reply anahtarı için ck'nin sol kısmını kullanamayız, çünkü bu son değil ve daha sonra kullanılacak. Reply anahtarı, AEAD/ChaCha20/Poly1305 kullanarak o kaydı şifrelemek ve diğer kayıtları yanıtlamak için ChaCha20 kullanmak üzere kullanılır. Her ikisi de aynı anahtarı kullanır. Nonce, mesajdaki kaydın 0'dan başlayarak pozisyonudur. Ayrıntılar için aşağıya bakın.

```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
replyKey = keydata[32:63]
ck = keydata[0:31]

AES Layer key:
keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
layerKey = keydata[32:63]

IV key for non-OBEP record:
ivKey = keydata[0:31]
because it's last

IV key for OBEP record:
ck = keydata[0:31]
keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
ivKey = keydata[32:63]
ck = keydata[0:31]

OBEP garlic reply key/tag:
keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
garlicReplyKey = keydata[32:63]
garlicReplyTag = keydata[0:7]
```
Not: OBEP'teki IV anahtarı için KDF, yanıt garlic encryption ile şifrelenmemiş olsa bile diğer hop'lardan farklıdır.

#### Kayıt Şifreleme

Hop'un kendi yanıt kaydı ChaCha20/Poly1305 ile şifrelenir. Bu, yukarıdaki uzun kayıt spesifikasyonu ile aynıdır, ANCAK 'n' her zaman 0 olmak yerine 0-7 arasındaki kayıt numarasıdır. Bkz. [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// AEAD parameters
k = replyKey from KDF above
n = record number 0-7
plaintext = 202 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
Diğer kayıtlar her hop'ta ChaCha20 ile yinelemeli ve simetrik olarak şifrelenir (ChaCha20/Poly1305 DEĞİL). Bu, yukarıdaki uzun kayıt spesifikasyonundan farklıdır; o spesifikasyon AES kullanır ve kayıt numarasını kullanmaz.

Kayıt numarası IV'nin 4. byte'ına konur, çünkü ChaCha20 4-11. byte'larda little-endian nonce ile 12-byte'lık bir IV kullanır. [RFC-7539](https://tools.ietf.org/html/rfc7539)'a bakın.

```
// Parameters
k = replyKey from KDF above
n = record number 0-7
iv = 12 bytes, all zeros except iv[4] = n
plaintext = 218 byte encrypted record

ciphertext = ENCRYPT(k, iv, plaintext)
```
#### Garlic Encryption

Mesajların garlic wrapping ile sarılması, bunları OBEP'ten (gelen yapı için) veya IBGW'den (giden yapı için) gizler. Bu önerilir ancak zorunlu değildir. OBEP ve IBGW aynı router ise, bu gerekli değildir.

Bir gelen Kısa Tunnel Yapı Mesajının garlic encryption ile şifrelenmesi, oluşturucu tarafından ECIES IBGW'ye şifrelenerek, [ECIES-ROUTERS](/docs/specs/ecies-routers/) belgesinde tanımlandığı gibi Noise 'N' şifrelemesi kullanır.

Bir Outbound Tunnel Build Reply Message'ın OBEP tarafından oluşturucuya şifrelenen garlic encryption'ı, yukarıdaki KDF'den gelen 32-byte garlic reply key ve 8-byte garlic reply tag ile Existing Session mesajları kullanır. Format, [I2NP](/docs/specs/i2np/), [ECIES-ROUTERS](/docs/specs/ecies-routers/), ve [ECIES-X25519](/docs/specs/ecies/) belgelerinde Database Lookup'lara verilen yanıtlar için belirtildiği gibidir.

#### Katman Şifrelemesi

Bu spesifikasyon, yapı istek kaydında bir katman şifreleme türü alanı içerir. Şu anda desteklenen tek katman şifreleme türü 0'dır ve bu AES'tir. Bu, önceki spesifikasyonlardan değişmemiştir, ancak katman anahtarı ve IV anahtarının yapı istek kaydında yer almak yerine yukarıdaki KDF'den türetilmesi dışında.

Örneğin ChaCha20 gibi yeni katman şifreleme türleri eklemek, ek araştırma konusu olup şu anda bu spesifikasyonun bir parçası değildir.

## Uygulama Notları

- Eski router'lar hop'un şifreleme türünü kontrol etmez ve ElGamal-şifrelenmiş kayıtlar gönderir. Bazı son router'lar hatalıdır ve çeşitli türlerde bozuk kayıtlar gönderir. Uygulayıcılar, CPU kullanımını azaltmak için mümkünse bu kayıtları DH işleminden önce tespit edip reddetmelidir.

### Yapı Kayıtları

Build record sırası rastgele hale getirilmelidir, böylece orta atlamalar tunnel içindeki konumlarını bilemezler.

Önerilen minimum build record sayısı 4'tür. Eğer hop sayısından daha fazla build record varsa, rastgele veya implementasyona özgü veri içeren "sahte" recordlar eklenmelidir. Gelen tunnel build işlemlerinde, kaynak router için her zaman doğru 16-byte hash öneki ve gerçek bir X25519 ephemeral key içeren bir "sahte" record bulunmalıdır, aksi takdirde en yakın hop bir sonraki hop'un kaynakçı olduğunu anlayacaktır.

"Sahte" kaydın geri kalanı rastgele veri olabilir veya yapıcının yapı hakkında kendisine veri göndermesi için herhangi bir formatta şifrelenmiş olabilir, muhtemelen bekleyen yapılar için depolama gereksinimlerini azaltmak amacıyla.

Gelen tunnel'ların başlatıcıları, "sahte" kayıtlarının önceki hop tarafından değiştirilmediğini doğrulamak için bir yöntem kullanmalıdır, çünkü bu durum anonimliği kaldırmak için de kullanılabilir. Başlatıcı, kayıtın bir checksum'ını saklayıp doğrulayabilir veya checksum'ı kayda dahil edebilir veya uygulama bağımlı olarak bir AEAD şifreleme/şifre çözme fonksiyonu kullanabilir. Eğer 16-bayt hash öneki veya diğer yapı kaydı içerikleri değiştirilmişse, router tunnel'ı atmalıdır.

Outbound tunnel'lar için sahte kayıtlar ve inbound tunnel'lar için ek sahte kayıtlar bu gereksinimlere sahip değildir ve tamamen rastgele veri olabilir, çünkü hiçbir zaman herhangi bir hop'a görünür olmayacaklardır. Yine de başlatıcının bunların değiştirilmediğini doğrulaması arzu edilebilir.

## Tunnel Bant Genişliği Parametreleri

### Genel Bakış

Son birkaç yılda yeni protokoller, şifreleme türleri ve tıkanıklık kontrolü iyileştirmeleriyle ağın performansını artırdığımız için, video akışı gibi daha hızlı uygulamalar mümkün hale geliyor. Bu uygulamalar, istemci tunnel'larındaki her hop'ta yüksek bant genişliği gerektiriyor.

Ancak katılımcı router'lar, tunnel oluşturma mesajı aldıklarında bir tunnel'ın ne kadar bant genişliği kullanacağı hakkında herhangi bir bilgiye sahip değildir. Sadece tüm katılımcı tunnel'lar tarafından kullanılan mevcut toplam bant genişliği ve katılımcı tunnel'lar için toplam bant genişliği sınırına dayanarak bir tunnel'ı kabul edebilir veya reddedebilirler.

İstek yapan router'lar ayrıca her hop'ta ne kadar bant genişliği bulunduğu konusunda hiçbir bilgiye sahip değildir.

Ayrıca, router'lar şu anda bir tunnel'da gelen trafiği sınırlamak için herhangi bir yönteme sahip değil. Bu, bir servisin aşırı yüklenme veya DDoS saldırısı yaşadığı zamanlarda oldukça faydalı olacaktır.

Tunnel inşa istek ve yanıt mesajlarındaki tunnel bant genişliği parametreleri bu özellikler için destek ekler. Ek bilgi için [Prop168](/proposals/168/) sayfasına bakın. Bu parametreler API 0.9.65 sürümünden itibaren tanımlanmıştır, ancak destek implementasyona göre değişebilir. Hem uzun hem de kısa ECIES inşa kayıtları için desteklenir.

### Yapı İsteği Seçenekleri

Aşağıdaki üç seçenek, kaydın tunnel yapı seçenekleri eşleme alanında ayarlanabilir: İstek yapan bir router bunların herhangi birini, tümünü veya hiçbirini dahil edebilir.

- m := bu tunnel için gereken minimum bant genişliği (string olarak KBps pozitif tamsayı)
- r := bu tunnel için istenen bant genişliği (string olarak KBps pozitif tamsayı)
- l := bu tunnel için bant genişliği sınırı; sadece IBGW'ye gönderilir (string olarak KBps pozitif tamsayı)

Kısıt: m <= r <= l

Katılımcı router, "m" belirtildiğinde ve en az o kadar bant genişliği sağlayamadığında tunnel'ı reddetmelidir.

İstek seçenekleri, karşılık gelen şifreli yapı isteği kaydında her katılımcıya gönderilir ve diğer katılımcılar tarafından görülemez.

### Build Reply Seçeneği

Yanıt ACCEPTED olduğunda, aşağıdaki seçenek kaydın tunnel build reply options mapping alanında ayarlanabilir:

- b := bu tunnel için mevcut bant genişliği (string olarak KBps pozitif tam sayı)

Kısıt: b >= m

Katılımcı router, yapı isteğinde "m" veya "r" belirtilmişse bunu dahil etmelidir. Değer, belirtilmişse "m" değerinden en az o kadar olmalıdır, ancak "r" değeri belirtilmişse ondan daha az veya daha fazla olabilir.

Katılan router, tunnel için en azından bu kadar bant genişliğini rezerve etmeye ve sağlamaya çalışmalıdır, ancak bu garanti edilmez. Router'lar 10 dakika sonrasındaki koşulları tahmin edemez ve katılımcı trafik, bir router'ın kendi trafiği ve tunnel'larından daha düşük önceliğe sahiptir.

Router'lar gerektiğinde mevcut bant genişliğini aşırı tahsis edebilir ve bu muhtemelen arzu edilen bir durumdur, çünkü tunnel'daki diğer atlamalar bunu reddedebilir.

Bu nedenlerle, katılımcı router'ın yanıtı en iyi çaba taahhüdü olarak değerlendirilmeli, ancak garanti olarak görülmemelidir.

Yanıt seçenekleri, talep eden router'a karşılık gelen şifrelenmiş yapı yanıt kaydında gönderilir ve diğer katılımcılar tarafından görülemez.

### Uygulama Notları

Bant genişliği parametreleri, tunnel katmanındaki katılımcı router'larda görüldüğü gibidir, yani saniye başına sabit boyutlu 1 KB tunnel mesajlarının sayısıdır. Transport (NTCP2 veya SSU2) ek yükü dahil edilmemiştir.

Bu bant genişliği, istemcide görülen bant genişliğinden çok daha fazla veya az olabilir. Tunnel mesajları, ratchet ve streaming dahil olmak üzere üst katmanlardan gelen ek yük dahil önemli ek yük içerir. Streaming ack'leri gibi aralıklı küçük mesajlar her biri 1 KB'ye genişletilecektir. Ancak, I2CP katmanındaki gzip sıkıştırması bant genişliğini önemli ölçüde azaltabilir.

İstek yapan router'da en basit uygulama, istekte kullanılacak değerleri hesaplamak için havuzdaki mevcut tunnel'ların ortalama, minimum ve/veya maksimum bant genişliklerini kullanmaktır. Daha karmaşık algoritmalar mümkündür ve bunlar uygulayıcıya bağlıdır.

İstemcinin router'a hangi bant genişliğinin gerekli olduğunu söylemesi için şu anda tanımlanmış herhangi bir I2CP veya SAM seçeneği bulunmamaktadır ve burada yeni seçenekler de önerilmemektedir. Gerekli olursa seçenekler daha sonraki bir tarihte tanımlanabilir.

Uygulamalar, build yanıtında döndürülen bant genişliği değerini hesaplamak için mevcut bant genişliğini veya herhangi bir veri, algoritma, yerel politika veya yerel yapılandırmayı kullanabilir.

## Referanslar

- [Ortak](/docs/specs/common-structures/)
- [Kriptografi](/docs/specs/cryptography/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ECIES-X25519](/docs/specs/ecies/)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)
- [I2NP](/docs/specs/i2np/)
- [Çoklu-Şifreleme](https://en.wikipedia.org/wiki/Multiple_encryption)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Öneri119](/proposals/119/)
- [Öneri143](/proposals/143/)
- [Öneri152](/proposals/152/)
- [Öneri153](/proposals/153/)
- [Öneri156](/proposals/156/)
- [Öneri157](/proposals/157/)
- [Öneri168](/proposals/168/)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [Tunnel Oluşturma](/docs/specs/tunnel-creation/)
