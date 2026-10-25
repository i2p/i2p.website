---
title: "Ortak Yapılar Belirtimi"
description: "Tüm I2P protokollerinde ortak olan veri türleri"
slug: "common-structures"
aliases:
  - "/tr/common_structures_spec"
  - "/tr/common_structures_spec/"
category: "Tasarım"
lastUpdated: "2026-10"
accurateFor: "0.9.71"
---

Bu belge, [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU](/docs/legacy/ssu/) vb. gibi tüm I2P protokollerinde ortak olan bazı veri türlerini açıklar.

## Ortak tür belirtimi

### Tamsayı

#### Açıklama

Negatif olmayan bir tamsayıyı temsil eder.

#### İçindekiler

Network byte order (big endian) ile işaretsiz bir tamsayıyı temsil eden 1 ila 8 bayt.

### Tarih

#### Açıklama

GMT saat diliminde 1 Ocak 1970 gece yarısından bu yana geçen milisaniye sayısı. Sayı 0 ise, tarih tanımsız veya null'dur.

#### İçindekiler

8 bayt [Integer](#integer)

### Dize

#### Açıklama

UTF-8 kodlanmış bir dizeyi temsil eder.

#### İçindekiler

İlk baytın string'deki bayt sayısını (karakter sayısını değil!) belirttiği ve kalan 0-255 baytın null ile sonlandırılmamış UTF-8 kodlanmış karakter dizisi olduğu 1 veya daha fazla bayt. Uzunluk sınırı 255 bayttır (karakter değil). Uzunluk 0 olabilir.

### PublicKey

#### Açıklama

Bu yapı ElGamal veya diğer asimetrik şifreleme yöntemlerinde kullanılır ve yalnızca üssü temsil eder, sabit olan ve kriptografi spesifikasyonunda [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy) tanımlanan asal sayıları değil. Diğer şifreleme şemaları tanımlanma sürecindedir, aşağıdaki tabloyu görün.

#### İçindekiler

Anahtar türü ve uzunluğu bağlamdan çıkarılır veya bir Destination ya da RouterInfo'nun Key Certificate'ında veya bir [LeaseSet2](#leaseset2) ya da diğer veri yapılarındaki alanlarda belirtilir. Varsayılan tür ElGamal'dır. 0.9.38 sürümünden itibaren, bağlama bağlı olarak diğer türler de desteklenebilir. Aksi belirtilmedikçe anahtarlar big-endian formatındadır.

X25519 anahtarları, 0.9.44 sürümünden itibaren Destination'larda ve LeaseSet2'de desteklenmektedir. X25519 anahtarları, 0.9.48 sürümünden itibaren RouterIdentity'lerde desteklenmektedir.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there; discouraged for leasesets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Little-endian. See <a href="/docs/specs/ecies/">ECIES</a> and <a href="/docs/specs/ecies-routers/">ECIES-ROUTERS</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.PublicKey](http://docs.i2p-projekt.de/net/i2p/data/PublicKey.html)

### PrivateKey

#### Açıklama

Bu yapı ElGamal veya diğer asimetrik şifre çözmede kullanılır ve yalnızca üssü temsil eder, kriptografi spesifikasyonunda [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy) sabit olarak tanımlanan asal sayıları değil. Diğer şifreleme şemaları tanımlanma sürecindedir, aşağıdaki tabloya bakın.

#### İçindekiler

Anahtar tipi ve uzunluğu bağlamdan çıkarılır veya bir veri yapısında ya da özel anahtar dosyasında ayrı olarak saklanır. Varsayılan tip ElGamal'dır. 0.9.38 sürümünden itibaren, bağlama bağlı olarak diğer tipler desteklenebilir. Aksi belirtilmedikçe anahtarlar big-endian formatındadır.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there; discouraged for leasesets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">66</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Little-endian. See <a href="/docs/specs/ecies/">ECIES</a> and <a href="/docs/specs/ecies-routers/">ECIES-ROUTERS</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1632</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2400</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3168</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.PrivateKey](http://docs.i2p-projekt.de/net/i2p/data/PrivateKey.html)

### SessionKey

#### Açıklama

Bu yapı simetrik AES256 şifreleme ve şifre çözme için kullanılır.

#### İçindekiler

32 bayt

JavaDoc: [net.i2p.data.SessionKey](http://docs.i2p-projekt.de/net/i2p/data/SessionKey.html)

### SigningPublicKey

#### Açıklama

Bu yapı imzaları doğrulamak için kullanılır.

#### İçindekiler

Anahtar türü ve uzunluğu bağlamdan çıkarılır veya bir Destination'ın Key Certificate'inde belirtilir. Varsayılan tür DSA_SHA1'dir. 0.9.12 sürümünden itibaren, bağlama bağlı olarak diğer türler desteklenebilir.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### Notlar

* Bir anahtar iki elemandan oluştuğunda (örneğin X,Y noktaları), her eleman gerekirse önünde sıfırlar eklenerek uzunluk/2'ye tamamlanarak serileştirilir.

* EdDSA ve RedDSA hariç tüm türler Big Endian formatındadır; EdDSA ve RedDSA Little Endian formatında saklanır ve iletilir.

JavaDoc: [net.i2p.data.SigningPublicKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPublicKey.html)

### SigningPrivateKey

#### Açıklama

Bu yapı imza oluşturmak için kullanılır.

#### İçindekiler

Anahtar türü ve uzunluğu oluşturulurken belirtilir. Varsayılan tür DSA_SHA1'dir. 0.9.12 sürümü itibariyle, bağlama bağlı olarak diğer türler de desteklenebilir.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">66</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### Notlar

* Bir anahtar iki elementten oluştuğunda (örneğin X,Y noktaları), gerekirse her element başına sıfırlar eklenerek uzunluk/2'ye tamamlanarak serileştirilir.

* Tüm türler Big Endian formatındadır, EdDSA ve RedDSA hariç - bunlar Little Endian formatında saklanır ve iletilir.

JavaDoc: [net.i2p.data.SigningPrivateKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPrivateKey.html)

### İmza

#### Açıklama

Bu yapı, bazı verilerin imzasını temsil eder.

#### İçindekiler

İmza türü ve uzunluğu kullanılan anahtarın türünden çıkarılır. Varsayılan tür DSA_SHA1'dir. 0.9.12 sürümünden itibaren, bağlama bağlı olarak diğer türler de desteklenebilir.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### Notlar

* Bir imza iki elemandan oluştuğunda (örneğin R,S değerleri), her eleman gerekirse başına sıfırlar eklenerek length/2 uzunluğuna doldurularak serileştirilir.

* Tüm türler Big Endian formatındadır, EdDSA ve RedDSA hariç; bunlar Little Endian formatında saklanır ve iletilir.

JavaDoc: [net.i2p.data.Signature](http://docs.i2p-projekt.de/net/i2p/data/Signature.html)

### Hash

#### Açıklama

Bazı verilerin SHA256 değerini temsil eder.

#### İçindekiler

32 bayt

JavaDoc: [net.i2p.data.Hash](http://docs.i2p-projekt.de/net/i2p/data/Hash.html)

### Oturum Etiketi

Not: ECIES-X25519 hedefleri (ratchet) ve ECIES-X25519 router'ları için Session Tag'ler 8 bayttır. Bkz. [ECIES](/docs/specs/ecies/) ve [ECIES-ROUTERS](/docs/specs/ecies-routers/).

#### Açıklama

Rastgele bir sayı

#### İçindekiler

32 bayt

JavaDoc: [net.i2p.data.SessionTag](http://docs.i2p-projekt.de/net/i2p/data/SessionTag.html)

### TunnelId

#### Açıklama

Bir tunnel içindeki her router için benzersiz olan bir tanımlayıcı belirler. Tunnel ID genellikle sıfırdan büyüktür; özel durumlar dışında sıfır değeri kullanmayın.

#### İçindekiler

4 bayt [Integer](#integer)

JavaDoc: [net.i2p.data.TunnelId](http://docs.i2p-projekt.de/net/i2p/data/TunnelId.html)

### Sertifika

#### Açıklama

Sertifika, I2P ağı boyunca kullanılan çeşitli makbuzlar veya iş kanıtları için bir kapsayıcıdır.

#### İçindekiler

Sertifika türünü belirten 1 bayt [Integer](#integer), ardından sertifika yük boyutunu belirten 2 bayt [Integer](#integer), sonra o kadar bayt.

```
+----+----+----+----+----+-/
|type| length  | payload
+----+----+----+----+----+-/

type :: Integer
        length -> 1 byte

length :: Integer
          length -> 2 bytes

payload :: data
           length -> $length bytes
```
#### Notlar

* [Router Identities](#routeridentity) için, Certificate 0.9.15 sürümü dahil olmak üzere her zaman NULL'dur. 0.9.16 sürümünden itibaren, anahtar türlerini belirtmek için bir Key Certificate kullanılır. 0.9.48 sürümünden itibaren, X25519 şifreleme public key türlerine izin verilir. Aşağıya bakınız.

* [Garlic Cloves](/docs/specs/i2np/#struct-garlicclove) için, Certificate her zaman NULL'dur, şu anda başka hiçbiri uygulanmamıştır.

* [Garlic Messages](/docs/specs/i2np/#msg-garlic) için, Certificate her zaman NULL'dur, şu anda başka hiçbiri uygulanmamıştır.

* [Destinations](#destination) için, Sertifika NULL olmayabilir. 0.9.12 sürümünden itibaren, imzalama genel anahtar türünü belirtmek için bir Anahtar Sertifikası kullanılabilir. Aşağıya bakınız.

* Geliştiriciler, Sertifikalarda fazla veri bulunmasını yasaklamaları konusunda uyarılır.
  Her sertifika türü için uygun uzunluk zorlanmalıdır.

#### Sertifika Türleri

Aşağıdaki sertifika türleri tanımlanmıştır:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Null</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HashCash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains an ASCII colon-separated hashcash string.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Hidden routers generally do not announce that they are hidden.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40 or 72</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">43 or 75</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains a 40-byte DSA signature, optionally followed by the 32-byte Hash of the signing Destination.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains multiple certificates.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 0.9.12. See below for details.</td>
    </tr>
  </tbody>
</table>
#### Anahtar Sertifikaları

Key certificate'lar 0.9.12 sürümüyle tanıtıldı. Bu sürümden önce, tüm PublicKey'ler 256 baytlık ElGamal anahtarlarıydı ve tüm SigningPublicKey'ler 128 baytlık DSA-SHA1 anahtarlarıydı. Key certificate, Destination veya RouterIdentity içindeki PublicKey ve SigningPublicKey türünü belirtmek ve standart uzunlukları aşan herhangi bir anahtar verisini paketlemek için bir mekanizma sağlar.

Sertifikadan önce tam olarak 384 bayt koruyarak ve fazla anahtar verilerini sertifikanın içine koyarak, Destination'ları ve Router Identity'lerini ayrıştıran herhangi bir yazılım için uyumluluğu korumuş oluruz.

Anahtar sertifikası yükü şunları içerir:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Data</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signing Public Key Type (<a href="#integer">Integer</a>)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Crypto Public Key Type (<a href="#integer">Integer</a>)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Excess Signing Public Key Data</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0+</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Excess Crypto Public Key Data</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0+</td>
    </tr>
  </tbody>
</table>
Uyarı: Anahtar türü sırası beklediğinizin tersine; İmzalama Public Key Türü ilk sırada.

Tanımlanmış İmzalama Genel Anahtarı türleri şunlardır:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Public Key Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely if ever used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely if ever used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (GOST)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/134-gost/">Prop134</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (GOST)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/134-gost/">Prop134</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only; never used for Router Identities</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65280-65534</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for experimental use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for future expansion</td>
    </tr>
  </tbody>
</table>
Tanımlanmış Kripto Açık Anahtar türleri şunlardır:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Public Key Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies/">ECIES</a> and proposal 156</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (NONE)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65280-65534</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for experimental use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for future expansion</td>
    </tr>
  </tbody>
</table>
Key Certificate mevcut olmadığında, Destination veya RouterIdentity içindeki önceki 384 byte, 256-byte ElGamal PublicKey ve ardından 128-byte DSA-SHA1 SigningPublicKey olarak tanımlanır. Key Certificate mevcut olduğunda, önceki 384 byte aşağıdaki gibi yeniden tanımlanır:

* Crypto Public Key'in tamamı veya ilk kısmı

* İki anahtarın toplam uzunluğu 384 bayttan azsa rastgele dolgu

* İmza Public Key'inin tamamı veya ilk kısmı

Crypto Public Key başlangıçta hizalanır ve Signing Public Key sonunda hizalanır. Dolgu (varsa) ortadadır. Sertifikalardaki başlangıç anahtar verisi, dolgu ve fazla anahtar verisi bölümlerinin uzunlukları ve sınırları açıkça belirtilmez, ancak belirtilen anahtar türlerinin uzunluklarından türetilir. Crypto ve Signing Public Key'lerin toplam uzunlukları 384 baytı aşarsa, geri kalanı Key Certificate'te yer alacaktır. Crypto Public Key uzunluğu 256 bayt değilse, iki anahtar arasındaki sınırı belirleme yöntemi bu belgenin gelecekteki bir revizyonunda belirtilecektir.

Belirtilen ElGamal Crypto Public Key ve Signing Public Key türünü kullanan örnek düzenler:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Padding Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Excess Signing Key Data in Cert</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.Certificate](http://docs.i2p-projekt.de/net/i2p/data/Certificate.html)

#### Notlar

* Uygulayıcıların Key Certificate'larda fazla veri bulunmasını yasaklaması tavsiye edilir.
  Her sertifika türü için uygun uzunluk zorlanmalıdır.

* 0,0 (ElGamal,DSA_SHA1) türlerindeki bir KEY sertifikası izin veriliyor ancak önerilmiyor.
  İyi test edilmemiştir ve bazı uygulamalarda sorunlara neden olabilir.
  (ElGamal,DSA_SHA1) Destination veya RouterIdentity'nin kanonik temsilinde
  KEY sertifikası kullanmaktan 4 bayt daha kısa olacak bir NULL sertifikası kullanın.

### Eşleme

#### Açıklama

Bir anahtar/değer eşlemeleri veya özellikler kümesi

#### İçindekiler

2-byte boyutunda Integer ardından String=String; çiftleri serisi.

UYARI: Mapping kullanımlarının çoğu imzalı yapılarda olup, Mapping girdilerinin anahtar değerine göre sıralanması gerekir, böylece imza değiştirilemez hale gelir. Anahtar değerine göre sıralama yapılmaması imza hatalarına neden olacaktır!

```bytefield
size       | 4 | red    | Integer, 2 bytes
key_string | 4 | blue   | String (len + data)
val_string | 8 | green  | String (len + data)
;          | 8 | yellow | :: A single byte containing ';'
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+
```
</details>
#### Notlar

* Kodlama optimal değil - ya '=' ve ';' karakterlerine ya da string uzunluklarına ihtiyacımız var, ikisine birden değil

#### Açıklama

* Bazı belgelerde dizgelerin '=' veya ';' karakterlerini içeremeyeceği belirtilse de bu kodlama bunları destekler

* String'ler UTF-8 olarak tanımlanmıştır ancak mevcut uygulamada I2CP UTF-8 kullanır fakat I2NP kullanmaz. Örneğin, bir I2NP Database Store Message içindeki RouterInfo seçenekleri eşlemesindeki UTF-8 string'ler bozulacaktır.

* Kodlama duplicate anahtarlara izin verir, ancak eşlemenin imzalandığı herhangi bir kullanımda, duplicate'lar imza hatasına neden olabilir.

* I2NP mesajlarında bulunan eşlemeler (örneğin RouterAddress veya RouterInfo'da)
  imzanın değişmez olması için anahtara göre sıralanmalıdır. Yinelenen anahtarlara
  izin verilmez.

* Bir [I2CP SessionConfig](/docs/specs/i2cp/#struct-sessionconfig) içinde bulunan eşlemeler, imzanın değişmez olması için anahtar bazında sıralanmış olmalıdır. Yinelenen anahtarlara izin verilmez.

* Sıralama yöntemi, karakterlerin Unicode değerlerini kullanarak Java String.compareTo() metodunda olduğu gibi tanımlanır.

* Uygulamaya bağlı olmakla birlikte, anahtarlar ve değerler genellikle büyük/küçük harf duyarlıdır.

* Anahtar ve değer dizesi uzunluk limitleri her biri için 255 bayt (karakter değil) artı uzunluk baytıdır. Uzunluk baytı 0 olabilir.

* Toplam uzunluk sınırı 65535 bayt artı 2 baytlık boyut alanı, yani toplamda 65537'dir.

* X25519 şifreleme türü ve Ed25519 imza türüne sahip bir Router Identity, rastgele verinin 10 kopyasını (320 bayt) içerecektir ve sıkıştırıldığında yaklaşık 288 bayt tasarruf sağlayacaktır.

JavaDoc: [net.i2p.data.DataHelper](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)

## Ortak yapı spesifikasyonu

### KeysAndCert

#### İçindekiler

Bir şifreleme public key'i, bir imzalama public key'i ve RouterIdentity ya da Destination olarak kullanılan bir sertifika.

#### Dolgu Oluşturma Yönergeleri

Bir [PublicKey](#publickey) ardından bir [SigningPublicKey](#signingpublickey) ve sonra bir [Certificate](#certificate).

```bytefield
public_key          | 8 | blue   | PublicKey (partial or full), 256 bytes or as specified in key cert

padding (optional)  | 8 | yellow | random data, pub + pad + sig == 384 bytes

signing_key         | 8 | green  | SigningPublicKey (partial or full), 128 bytes or as specified

certificate         | 3 | purple | Certificate, >= 3 bytes
= total length: 387+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-/

public_key :: `PublicKey` (partial or full)
              length -> 256 bytes or as specified in key certificate

padding :: random data
           length -> 0 bytes or as specified in key certificate
           public_key length + padding length + signing_key length == 384 bytes

signing__key :: `SigningPublicKey` (partial or full)
                length -> 128 bytes or as specified in key certificate

certificate :: `Certificate`
               length -> >= 3 bytes

total length: 387+ bytes
```

</details>
#### Notlar

Bu kılavuzlar Öneri 161'de önerilmiş ve API sürüm 0.9.57'de uygulanmıştır. Bu kılavuzlar 0.6 (2005) sürümünden itibaren tüm sürümlerle geriye dönük uyumludur. Geçmiş bilgi ve daha fazla ayrıntı için Öneri 161'e bakınız.

ElGamal + DSA-SHA1 dışında şu anda kullanılan herhangi bir anahtar türü kombinasyonu için dolgu mevcut olacaktır. Ayrıca, hedefler için 256-bayt'lık genel anahtar alanı sürüm 0.6'dan (2005) beri kullanılmamaktadır.

Uygulayıcılar, Destination genel anahtarları ve Destination ile Router Identity dolgusu için rastgele veri üretirken, çeşitli I2P protokollerinde sıkıştırılabilir olmasını sağlamalı, güvenliği koruyarak Base 64 temsillerinin bozuk veya güvensiz görünmesini önlemelidir. Bu yaklaşım, dolgu alanlarını kaldırmanın faydalarının çoğunu disruptif protokol değişiklikleri olmadan sağlar.

Kesin olarak konuşmak gerekirse, tek başına 32-byte'lık imzalama public key'i (hem Destination'larda hem de Router Identity'lerde) ve 32-byte'lık şifreleme public key'i (sadece Router Identity'lerde) bu yapıların SHA-256 hash'lerinin kriptografik olarak güçlü olması ve network database DHT'sinde rastgele dağıtılması için gerekli tüm entropi'yi sağlayan rastgele bir sayıdır.

Ancak, aşırı ihtiyatlı olmak adına, ElG public key alanında ve padding'de minimum 32 bayt rastgele veri kullanılmasını öneriyoruz. Ayrıca, alanların hepsi sıfır olsaydı, Base 64 hedefleri uzun AAAA karakter dizileri içerecekti ve bu da kullanıcılarda alarm veya karışıklığa neden olabilirdi.

Tam KeysAndCert yapısının I2NP Database Store Message, Streaming SYN, SSU2 handshake ve yanıtlanabilir Datagrams gibi I2P protokollerinde yüksek oranda sıkıştırılabilir olması için gerektiği kadar 32 baytlık rastgele veriyi tekrarlayın.

Örnekler:

* Ed25519 imza türüne sahip bir Destination, rastgele verinin 11 kopyasını (352 bayt) içerecek ve sıkıştırıldığında yaklaşık 320 bayt tasarruf sağlayacaktır.

* Bunların her zaman 387 bayt olduğunu varsaymayın! Bunlar 387 bayt artı 385-386 baytlarında belirtilen sertifika uzunluğudur ve bu uzunluk sıfırdan farklı olabilir.

Uygulamalar, elbette, tam 387+ bayt yapısını saklamalıdır çünkü yapının SHA-256 hash'i tüm içeriği kapsar.

#### Açıklama

* 0.9.12 sürümünden itibaren, sertifika bir Key Certificate ise, anahtar alanlarının sınırları değişebilir. Ayrıntılar için yukarıdaki Key Certificate bölümüne bakın.

* Crypto Public Key başlangıçta hizalanır ve Signing Public Key sonunda hizalanır. Dolgu (varsa) ortadadır.

* RouterIdentity için sertifika 0.9.12 sürümüne kadar her zaman NULL idi.

JavaDoc: [net.i2p.data.KeysAndCert](http://docs.i2p-projekt.de/net/i2p/data/KeysAndCert.html)

### RouterIdentity

#### İçindekiler

Belirli bir router'ı benzersiz şekilde tanımlamanın yolunu belirler

#### Notlar

KeysAndCert ile aynı.

Padding alanı için rastgele veri üretme konusunda yönergeler için [KeysAndCert](#keysandcert) bölümüne bakın.

#### Açıklama

* Bunların her zaman 387 bayt olduğunu varsaymayın! Bunlar 387 bayt artı 385-386 baytlarında belirtilen sertifika uzunluğudur ve bu uzunluk sıfır olmayabilir.

* 0.9.12 sürümü itibariyle, eğer sertifika bir Key Certificate ise, anahtar alanlarının sınırları değişebilir. Ayrıntılar için yukarıdaki Key Certificate bölümüne bakın.

* Crypto Public Key başlangıçta hizalanır ve Signing Public Key sonunda hizalanır. Dolgu (varsa) ortadadır.

* Key certificate (anahtar sertifikası) ve ECIES_X25519 public key içeren RouterIdentity'ler 0.9.48 sürümünden itibaren desteklenmektedir.
  Bundan önce, tüm RouterIdentity'ler ElGamal idi.

* Hedefin public key'i, 0.6 sürümünde (2005) devre dışı bırakılan eski i2cp-to-i2cp şifrelemesi için kullanılıyordu, şu anda kullanımdan kaldırılan LeaseSet şifrelemesi için IV dışında kullanılmamaktadır. Bunun yerine LeaseSet içindeki public key kullanılır.

JavaDoc: [net.i2p.data.router.RouterIdentity](http://docs.i2p-projekt.de/net/i2p/data/router/RouterIdentity.html)

### Hedef

#### İçindekiler

Bir Destination, mesajların güvenli teslimat için yönlendirilebileceği belirli bir uç noktayı tanımlar.

#### Notlar

[KeysAndCert](#keysandcert) ile aynıdır, ancak public key hiçbir zaman kullanılmaz ve geçerli bir ElGamal Public Key yerine rastgele veri içerebilir.

Public key ve padding alanları için rastgele veri üretme yönergeleri için [KeysAndCert](#keysandcert) bölümüne bakın.

#### Açıklama

* Bunların her zaman 387 bayt olduğunu varsaymayın! Bu değerler 387 bayt artı 385-386 baytlarında belirtilen sertifika uzunluğudur ve bu uzunluk sıfır olmayabilir.

* Sürüm 0.9.12 itibariyle, sertifika bir Key Certificate ise, anahtar alanlarının sınırları değişebilir. Ayrıntılar için yukarıdaki Key Certificate bölümüne bakın.

* Crypto Public Key başlangıçta hizalanır ve Signing Public Key sonunda hizalanır. Dolgu (varsa) ortadadır.

* Hedefin genel anahtarı, sürüm 0.6'da devre dışı bırakılan eski I2CP-to-I2CP şifrelemesi için kullanılıyordu, şu anda kullanılmıyor.

JavaDoc: [net.i2p.data.Destination](http://docs.i2p-projekt.de/net/i2p/data/Destination.html)

### Lease

#### İçindekiler

KULLANIMI BIRAKILDI. LeaseSet2 ve Lease2 kullanın.

Belirli bir tünelin bir [Hedef](#destination)'e yönelik mesajları alma yetkisini tanımlar.

#### Açıklama

Ağ geçidi yönlendiricisinin [RouterIdentity](#routeridentity)'sinin SHA256 [Hash](#hash'ı), ardından [TunnelId](#tunnelid) ve son olarak bir bitiş [Date](#date).

```bytefield
tunnel_gw   | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes

tunnel_id   | 4 | green  | TunnelId, 4 bytes
end_date    | 4 | yellow | Date, 8 bytes

= Total size 44 bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway
             length -> 32 bytes

tunnel_id :: `TunnelId`
             length -> 4 bytes

end_date :: `Date`
            length -> 8 bytes
```

</details>
JavaDoc: [net.i2p.data.Lease](http://docs.i2p-projekt.de/net/i2p/data/Lease.html)

### LeaseSet

#### İçindekiler

KULLANIMI BIRAKILDI. LeaseSet2 ve Lease2 kullanın.

Belirli bir [Destination](#destination) için şu anda yetkilendirilmiş tüm [Leases](#lease) içeriğini, sarmal iletilerin şifrelenmek üzere kullanılabileceği [PublicKey](#publickey) ve bu yapının bu sürümünü iptal etmek için kullanılabilecek [SigningPublicKey](#signingpublickey) içerir. LeaseSet, ağ veritabanında depolanan iki yapıdan biridir (diğeri [RouterInfo](#routerinfo)) ve içindeki [Destination](#destination)'in SHA256 değeriyle anahtarlanır.

#### Notlar

[Destination](#destination), ardından şifreleme için bir [PublicKey](#publickey), sonra LeaseSet'in bu sürümünü iptal etmek için kullanılabilecek bir [SigningPublicKey](#signingpublickey), ardından kümede kaç tane [Lease](#lease) yapısı olduğunu belirten 1 byte'lık bir [Integer](#integer), bunu takip eden gerçek [Lease](#lease) yapıları ve son olarak [Destination](#destination)'ın [SigningPrivateKey](#signingprivatekey)'i ile imzalanmış önceki byte'ların [Signature](#signature)'ı.

```bytefield
destination     | 8 | blue   | Destination, >= 387+ bytes
encryption_key  | 8 | green  | PublicKey, 256 bytes
signing_key     | 8 | cyan   | SigningPublicKey, 128 bytes or as specified in destination's key cert
num             | 1 | red    | Integer, 1 byte, number of leases (0-16)
Lease 0         | 7 | yellow | Lease, 44 bytes
Lease 1         | 8 | yellow | Lease, 44 bytes
Lease ($num-1)  | 8 | yellow | Lease, 44 bytes
signature       | 8 | purple | Signature, 40 bytes or as specified in destination's key cert

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: `Destination`
               length -> >= 387+ bytes

encryption_key :: `PublicKey`
                  length -> 256 bytes

signing_key :: `SigningPublicKey`
               length -> 128 bytes or as specified in destination's key
                         certificate

num :: `Integer`
       length -> 1 byte
       Number of leases to follow
       value: 0 <= num <= 16

leases :: [`Lease`]
          length -> $num*44 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate
```

</details>
#### Açıklama

* Şifreleme anahtarı uçtan uca ElGamal/AES+SessionTag şifrelemesi 
  [ELGAMAL-AES](/docs/specs/elgamal-aes/) için kullanılır. Şu anda her router başlangıcında yeniden oluşturulur, 
  kalıcı değildir.

* İmza, hedefin imzalama genel anahtarı kullanılarak doğrulanabilir.

* Sıfır Lease içeren bir LeaseSet'e izin verilir ancak kullanılmaz.
  Bu, uygulanmamış olan LeaseSet iptali için tasarlanmıştı.
  Tüm LeaseSet2 varyantları en az bir Lease gerektirir.

* signing_key şu anda kullanılmamaktadır. LeaseSet iptal işlemi için tasarlanmıştı ancak bu özellik henüz uygulanmamıştır. Şu anda her router başlatılışında yeniden oluşturulur ve kalıcı değildir. Signing key türü her zaman hedefin signing key türüyle aynıdır.

* Tüm Lease'lerin en erken sona erme tarihi, LeaseSet'in zaman damgası veya sürümü olarak kabul edilir. Router'lar genellikle bir LeaseSet'in saklanmasını, mevcut olandan "daha yeni" olmadığı sürece kabul etmezler. En eski Lease'in önceki LeaseSet'teki en eski Lease ile aynı olduğu yeni bir LeaseSet yayınlarken dikkatli olun. Yayınlayan router bu durumda genellikle en eski Lease'in sona erme süresini en az 1 ms artırmalıdır.

* 0.9.7 sürümünden önce, kaynak router tarafından gönderilen bir DatabaseStore Mesajına dahil edildiğinde, router tüm yayınlanan lease'lerin sona erme sürelerini aynı değere, yani en erken lease'in süresine ayarlıyordu. 0.9.7 sürümünden itibaren, router her lease için gerçek lease sona erme süresini yayınlar. Bu bir uygulama detayıdır ve yapı spesifikasyonunun bir parçası değildir.

* Toplam boyut: 40 bayt

JavaDoc: [net.i2p.data.LeaseSet](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet.html)

### Lease2

#### İçindekiler

Belirli bir tunnel'ın bir [Destination](#destination)'ı hedefleyen mesajları alması için yetkilendirmeyi tanımlar. [Lease](#lease) ile aynıdır ancak 4-byte end_date içerir. [LeaseSet2](#leaseset2) tarafından kullanılır. 0.9.38 sürümünden itibaren desteklenir; daha fazla bilgi için proposal 123'e bakın.

#### Notlar

Ağ geçidi yönlendiricisinin [RouterIdentity](#routeridentity)'sinin [Hash](#hash) değerinin SHA256'sı, ardından [TunnelId](#tunnelid) ve son olarak 4 baytlık bir bitiş tarihi.

```bytefield
tunnel_gw   | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes

tunnel_id   | 4 | green  | TunnelId, 4 bytes
end_date    | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway
             length -> 32 bytes

tunnel_id :: `TunnelId`
             length -> 4 bytes

end_date :: 4 byte date
            length -> 4 bytes
            Seconds since the epoch, rolls over in 2106.
```

</details>
#### Açıklama

* Bu bölüm çevrimdışı oluşturulabilir ve oluşturulmalıdır.

JavaDoc: [net.i2p.data.Lease2](http://docs.i2p-projekt.de/net/i2p/data/Lease2.html)

### OfflineSignature

#### İçindekiler

Bu, [LeaseSet2Header](#leaseset2header)'ın isteğe bağlı bir parçasıdır. Akış ve I2CP'de de kullanılır. 0.9.38'den bu yana desteklenmektedir; daha fazla bilgi için öneri 123'e bakın.

#### Notlar

Bir son kullanma tarihi, bir sigtype ve geçici [SigningPublicKey](#signingpublickey) ile bir [Signature](#signature) içerir.

```bytefield
expires              | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
sigtype              | 2 | cyan   | 2 byte type of the transient_public_key
_ | 2
transient_public_key | 8 | green  | SigningPublicKey, as inferred from sigtype

signature            | 8 | purple | Signature, as inferred from sigtype of the Destination's key

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4 byte date
           length -> 4 bytes
           Seconds since the epoch, rolls over in 2106.

sigtype :: 2 byte type of the transient_public_key
           length -> 2 bytes

transient_public_key :: `SigningPublicKey`
                        length -> As inferred from the sigtype

signature :: `Signature`
             length -> As inferred from the sigtype of the signing public key
                       in the `Destination` that preceded this offline signature.
             Signature of expires timestamp, transient sig type, and public key,
             by the destination public key.
```

</details>
#### Açıklama

* **Bayraklar** (2 bayt):
  * Bit 0: Ayarlanmışsa, çevrimdışı anahtarlar mevcut ([OfflineSignature](#offlinesignature) bölümüne bakın)
  * Bit 1: Ayarlanmışsa, bu yayınlanmamış bir leaseset
  * Bit 2: Ayarlanmışsa, bu köreltilmiş bir leaseset
  * Bit 15-3: Ayrılmış, 0'a ayarlanır

### LeaseSet2Header

#### İçindekiler

Bu, [LeaseSet2](#leaseset2) ve [MetaLeaseSet](#metaleaseset) arasındaki ortak kısımdır. 0.9.38'den bu yana desteklenmektedir; daha fazla bilgi için öneri 123'e bakınız.

#### Notlar

[Destination](#destination), iki zaman damgası ve isteğe bağlı bir [OfflineSignature](#offlinesignature) içerir.

```bytefield
destination          | 8 | blue   | Destination, >= 387+ bytes

published            | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
expires              | 2 | cyan   | 2 byte time, offset from published in seconds, 18.2 hours max
flags                | 2 | red
offline_signature    | 8 | purple | OfflineSignature, varies, optional (present if flags bit 0 set

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: `Destination`
               length -> >= 387+ bytes

published :: 4 byte date
             length -> 4 bytes
             Seconds since the epoch, rolls over in 2106.

expires :: 2 byte time
           length -> 2 bytes
           Offset from published timestamp in seconds, 18.2 hours max

flags :: 2 bytes
  Bit order: 15 14 ... 3 2 1 0
  Bit 0: If 0, no offline keys; if 1, offline keys
  Bit 1: If 0, a standard published leaseset.
         If 1, an unpublished leaseset.
  Bit 2: If 0, a standard published leaseset.
         If 1, this unencrypted leaseset will be blinded and encrypted when published.
  Bits 15-3: set to 0 for compatibility with future uses

offline_signature :: `OfflineSignature`
                     length -> varies
                     Optional, only present if bit 0 is set in the flags.
```

</details>
#### Açıklama

* Toplam boyut: minimum 395 bayt

* Maksimum gerçek son kullanma süresi [LeaseSet2](#leaseset2) için yaklaşık 660 (11 dakika) ve [MetaLeaseSet](#metaleaseset) için 65535'tir (tam 18,2 saat).

* [LeaseSet](#leaseset) (1) bir 'published' alanına sahip değildi, bu nedenle sürüm kontrolü için en erken lease'in aranması gerekiyordu. LeaseSet2 bir saniyelik çözünürlüğe sahip bir 'published' alanı ekler. Router'lar yeni leaseset'leri floodfill'lere gönderme hızını saniyede bir defadan çok daha yavaş bir hızla sınırlamalıdır (her destination için). Bu uygulanmazsa, kod her yeni leaseset'in 'published' zamanının bir öncekinden en az bir saniye sonra olduğundan emin olmalıdır, aksi halde floodill'ler yeni leaseset'i saklamaz veya flood etmez.

- serviceoption := optionkey optionvalue
- optionkey := _service._proto
- service := İstenen hizmetin sembolik adı. Küçük harf olmalıdır. Örnek: "smtp".
  İzin verilen karakterler [a-z0-9-] ve '-' ile başlayamaz veya bitemez.
  [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) veya Linux /etc/services'den standart tanımlayıcılar orada tanımlanmışsa kullanılmalıdır.
- proto := İstenen hizmetin aktarım protokolü. Küçük harf olmalıdır, "tcp" veya "udp" olabilir.
  "tcp" akış demektir ve "udp" yanıtlanabilir datagram'lar demektir.
  Ham datagram'lar ve datagram2 için protokol göstergeleri daha sonra tanımlanabilir.
  İzin verilen karakterler [a-z0-9-] ve '-' ile başlayamaz veya bitemez.
- optionvalue := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priority weight port target [appoptions]
- ttl := yaşam süresi, saniye cinsinden tamsayı. Pozitif tamsayı. Örnek: "86400".
  En az 86400 (bir gün) önerilir, ayrıntılar için aşağıdaki Öneriler bölümüne bakın.
- priority := Hedef ana bilgisayarın önceliği, düşük değer daha tercih edilir demektir. Negatif olmayan tamsayı. Örnek: "0"
  Sadece birden fazla kayıt varsa yararlıdır, ancak tek kayıt olsa bile gereklidir.
- weight := Aynı önceliğe sahip kayıtlar için göreceli ağırlık. Yüksek değer seçilme şansının daha fazla olması demektir. Negatif olmayan tamsayı. Örnek: "0"
  Sadece birden fazla kayıt varsa yararlıdır, ancak tek kayıt olsa bile gereklidir.
- port := Hizmetin bulunacağı I2CP portu. Negatif olmayan tamsayı. Örnek: "25"
  Port 0 desteklenir ancak önerilmez.
- target := Hizmeti sağlayan hedefin ana bilgisayar adı veya b32'si. [NAMING](/docs/overview/naming/) bölümündeki gibi geçerli bir ana bilgisayar adı. Küçük harf olmalıdır.
  Örnek: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" veya "example.i2p".
  Ana bilgisayar adı "iyi bilinen", yani resmi veya varsayılan adres defterlerinde olmadığı sürece b32 önerilir.
- appoptions := uygulamaya özgü keyfi metin, " " veya "," içeremez. Kodlama UTF-8'dir.

### LeaseSet2

#### İçindekiler

Tür 3'ün I2NP DatabaseStore mesajında yer alır. 0.9.38'den beri desteklenir; daha fazla bilgi için öneri 123'e bakın.

Belirli bir [Destination](#destination) için şu anda yetkilendirilmiş tüm [Lease2](#lease2)'leri ve garlic mesajlarının şifrelenebileceği [PublicKey](#publickey)'i içerir. LeaseSet, ağ veritabanında saklanan iki yapıdan biridir (diğeri [RouterInfo](#routerinfo)), ve içerdiği [Destination](#destination)'ın SHA256 değeri altında anahtarlanır.

#### Şifreleme Anahtarı Tercihi

[LeaseSet2Header](#leaseset2header), ardından şifreleme için bir veya daha fazla [PublicKey](#publickey), set içinde kaç tane [Lease2](#lease2) yapısı olduğunu belirten bir [Integer](#integer), ardından bu [Lease2](#lease2) yapıları ve son olarak önceki baytların [Destination](#destination)'in [SigningPrivateKey](#signingprivatekey)'ı ya da geçici anahtar tarafından imzalanmış [Signature](#signature) yapısı.

```bytefield
ls2_header       | 8 | blue   | LeaseSet2Header, varies
options          | 8 | gray   | Mapping, varies, 2 bytes minimum
numk             | 2 | red    | Integer, 1 byte, number of encryption keys (1 <= numk <= max TBD)
keytype0         | 3 | cyan   | Encryption type of PublicKey, 2 bytes
keylen0          | 3 | cyan   | Length of PublicKey, 2 bytes
encryption_key_0 | 8 | green  | PublicKey, keylen bytes
keytypen         | 4 | cyan   | Encryption type of PublicKey, 2 bytes
keylenn          | 4 | cyan   | Length of PublicKey, 2 bytes
encryption_key_n | 8 | green  | PublicKey, keylen bytes
num              | 1 | red    | Integer, 1 byte, number of Lease2s (0-16)
Lease2 0         | 7 | yellow | Lease2, 40 bytes
Lease2 ($num-1)  | 8 | yellow | Lease2, 40 bytes
signature        | 8 | purple | Signature, 40 bytes or as specified in destination's key cert
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: `LeaseSet2Header`
             length -> varies

options :: `Mapping`
           length -> varies, 2 bytes minimum

numk :: `Integer`
        length -> 1 byte
        Number of key types, key lengths, and `PublicKey`s to follow
        value: 1 <= numk <= max TBD

keytype :: The encryption type of the `PublicKey` to follow.
           length -> 2 bytes

keylen :: The length of the `PublicKey` to follow.
          Must match the specified length of the encryption type.
          length -> 2 bytes

encryption_key :: `PublicKey`
                  length -> keylen bytes

num :: `Integer`
       length -> 1 byte
       Number of `Lease2`s to follow
       value: 0 <= num <= 16

leases :: [`Lease2`]
          length -> $num*40 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate, or by the sigtype of the transient public key,
                       if present in the header
```

</details>
#### Seçenekler

Yayınlanmış (sunucu) leaseSet'ler için, şifreleme anahtarları sunucu tercihine göre sıralanır, en tercih edilen ilk sırada yer alır. İstemciler birden fazla şifreleme türünü destekliyorsa, sunucu tercihini gözetmeleri ve sunucuya bağlanmak için destekledikleri ilk türü şifreleme yöntemi olarak seçmeleri önerilir. Genel olarak, daha yeni (daha yüksek numaralı) anahtar türleri daha güvenli veya verimlidir ve tercih edilir, bu nedenle anahtarlar anahtar türünün ters sırasına göre listelenmelidir.

Ancak istemciler, uygulamaya bağlı olarak tercihlerine göre seçim yapabilir veya "kombine" tercihi belirlemek için bazı yöntemler kullanabilir. Bu, bir yapılandırma seçeneği olarak veya hata ayıklama amacıyla faydalı olabilir.

Yayınlanmamış (istemci) leaseset'lerdeki anahtar sırası etkili bir şekilde önemli değildir, çünkü yayınlanmamış istemcilere genellikle bağlantı girişiminde bulunulmaz. Bu sıra, yukarıda açıklandığı gibi birleşik bir tercihi belirlemek için kullanılmadığı sürece.

#### Notlar

API 0.9.66 itibariyle, hizmet kaydı seçenekleri için standart bir biçim tanımlanmıştır. Ayrıntılar için öneri 167'ye bakın. Farklı bir biçim kullanan ve hizmet kayıtlarından farklı diğer seçenekler gelecekte tanımlanabilir.

LS2 seçenekleri anahtar değerine göre sıralanmalıdır, böylece imza değişmez kalır.

Hizmet kaydı seçenekleri şu şekilde tanımlanır:

* Hedefin public key'i, 0.6 sürümünde devre dışı bırakılan eski I2CP-to-I2CP şifrelemesi için kullanılıyordu, şu anda kullanılmıyor.

Örnekler:

aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p için LS2, bir SMTP sunucusunu gösteriyor:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

İki SMTP sunucusunu işaret eden aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p için LS2:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p için LS2'de, kendisini bir SMTP sunucusu olarak gösterir:

"_smtp._tcp" "0 999999 25"

#### Açıklama

* Şifreleme anahtarları uçtan uca ElGamal/AES+SessionTag şifrelemesi
  [ELGAMAL-AES](/docs/specs/elgamal-aes/) (tip 0) veya diğer uçtan uca şifreleme şemaları için kullanılır.
  [ECIES](/docs/specs/ecies/) ve 145 ve 156 numaralı tekliflere bakın.
  Her router başlangıcında yeniden oluşturulabilir
  veya kalıcı olabilirler.
  X25519 (tip 4, [ECIES](/docs/specs/ecies/) bakın) 0.9.44 sürümü itibariyle desteklenmektedir.

* İmza, yukarıdaki verinin ÖNCESİNE DatabaseStore türünü içeren tek bayt (3) EKLENMİŞ haliyle yapılır.

* İmza, hedefin imzalama genel anahtarı veya leaseset2 başlığında çevrimdışı bir imza bulunuyorsa geçici imzalama genel anahtarı kullanılarak doğrulanabilir.

* Her anahtar için anahtar uzunluğu sağlanır, böylece floodfill'ler ve istemciler tüm şifreleme türleri bilinmese veya desteklenmese bile yapıyı ayrıştırabilir.

* [LeaseSet2Header](#leaseset2header) içindeki 'published' alanıyla ilgili nota bakın

* Seçenekler eşlemesi, boyut birden büyükse, anahtar tarafından sıralanmalıdır, böylece imza değişmez olur.

* Toplam boyut: 40 bayt

JavaDoc: [net.i2p.data.LeaseSet2](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet2.html)

### MetaLease

#### İçindekiler

ÖN BILGI. Tam olarak desteklenmemektedir.

Belirli bir tunnel'ın bir [Destination](#destination)'ı hedefleyen mesajları alması için yetkilendirmeyi tanımlar. [Lease2](#lease2) ile aynıdır ancak tunnel id yerine bayraklar ve maliyet içerir. [MetaLeaseSet](#metaleaseset) tarafından kullanılır. Tip 7 I2NP DatabaseStore mesajında bulunur. 0.9.38 sürümünden itibaren desteklenir; daha fazla bilgi için proposal 123'e bakın.

#### Notlar

Ağ geçidi yönlendiricisinin [RouterIdentity](#routeridentity) değerinin SHA256 [Hash](#hash'ı), ardından bayraklar ve maliyet, ve son olarak 4 baytlık bir bitiş tarihi.

```bytefield
tunnel_gw | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes
flags     | 3 | red    | 3 bytes
cost      | 1 | green  | 1 byte
end_date  | 4 | yellow | 4 bytes, seconds since epoch
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway,
             or the hash of another `MetaLeaseSet`.
             length -> 32 bytes

flags :: 3 bytes of flags
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Type of the entry.
         If 0, unknown.
         If 1, a `LeaseSet`.
         If 3, a `LeaseSet2`.
         If 5, a `MetaLeaseSet`.
         Bits 23-4: set to 0 for compatibility with future uses
         length -> 3 bytes

cost :: 1 byte, 0-255. Lower value is higher priority.
        length -> 1 byte

end_date :: 4 byte date
            length -> 4 bytes
            Seconds since the epoch, rolls over in 2106.

```
</details>
#### Açıklama

* Hedefin genel anahtarı, 0.6 sürümünde devre dışı bırakılan eski I2CP-to-I2CP şifrelemesi için kullanılıyordu, şu anda kullanılmamaktadır.

JavaDoc: [net.i2p.data.MetaLease](http://docs.i2p-projekt.de/net/i2p/data/MetaLease.html)

### MetaLeaseSet

#### İçindekiler

ÖN BILGI. Tam olarak desteklenmemektedir.

Tür 7 olan bir I2NP DatabaseStore mesajının içinde yer alır. 0.9.38 sürümünden itibaren tanımlanmıştır; daha fazla bilgi için öneri 123'e bakınız.

Belirli bir [Destination](#destination) için şu anda yetkilendirilmiş tüm [MetaLease](#metalease) bilgilerini ve garlic mesajlarının şifrelenebileceği [PublicKey](#publickey)'i içerir. LeaseSet, ağ veritabanında (netDb) depolanan iki yapıdan biridir (diğeri [RouterInfo](#routerinfo)'dır) ve içindeki [Destination](#destination)'in SHA256 değeri ile anahtarlanır.

#### Notlar

[LeaseSet2Header](#leaseset2header), ardından bir seçenek, içinde kaç tane [Lease2](#lease2) yapısı bulunduğunu belirten bir [Integer](#integer), ardından gerçek [Lease2](#lease2) yapıları ve son olarak önceki baytların [Destination](#destination)'in [SigningPrivateKey](#signingprivatekey) veya geçici anahtarı ile imzalanmış bir [Signature](#signature) gelir.

```bytefield
ls2_header       | 8 | blue   | LeaseSet2Header, varies
options          | 8 | green  | Mapping, varies, 2 bytes minimum
num              | 1 | red    | Integer, 1 byte
MetaLease 0      | 7 | yellow | 40 bytes
MetaLease ($num-1) | 8 | yellow | 40 bytes
numr             | 1 | red    | Integer, 1 byte
revocation_0     | 8 | cyan   | Hash, 32 bytes
revocation_n     | 8 | cyan   | Hash, 32 bytes
signature        | 8 | purple | Signature, 40+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: `LeaseSet2Header`
             length -> varies

options :: `Mapping`
           length -> varies, 2 bytes minimum

num :: `Integer`
        length -> 1 byte
        Number of `MetaLease`s to follow
        value: 1 <= num <= max TBD

leases :: `MetaLease`s
          length -> $numr*40 bytes

numr :: `Integer`
        length -> 1 byte
        Number of `Hash`es to follow
        value: 0 <= numr <= max TBD

revocations :: [`Hash`]
               length -> $numr*32 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate, or by the sigtype of the transient public key,
                       if present in the header

```
</details>
#### Açıklama

* İmza, yukarıdaki verilerin üzerinde olup, DatabaseStore türünü (7) içeren tek baytın BAŞINA EKLENMESİ ile oluşturulur.

* İmza, hedefin imzalama genel anahtarı kullanılarak doğrulanabilir veya leaseset2 başlığında çevrimdışı bir imza bulunuyorsa geçici imzalama genel anahtarı kullanılarak doğrulanabilir.

* [LeaseSet2Header](#leaseset2header) içindeki 'published' alanına ilişkin nota bakın

* Hedefin genel anahtarı, 0.6 sürümünde devre dışı bırakılan eski I2CP-to-I2CP şifrelemesi için kullanılıyordu, şu anda kullanılmıyor.

JavaDoc: [net.i2p.data.MetaLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/MetaLeaseSet.html)

### EncryptedLeaseSet

#### İçindekiler

Tür 5 olan bir I2NP DatabaseStore mesajının içinde yer alır. 0.9.38'den itibaren tanımlanmıştır ve 0.9.39'dan itibaren çalışmaktadır; daha fazla bilgi için öneri 123'e bakınız.

Yalnızca körleştirilmiş anahtar ve süre sonu açık metin olarak görünür. Gerçek lease set şifrelenmiştir.

#### Notlar

İki baytlık bir imza türü, körleştirilmiş [SigningPrivateKey](#signingprivatekey), yayımlanma zamanı, sona erme süresi ve bayraklar. Ardından, iki baytlık bir uzunluk ve şifrelenmiş veri gelir. Son olarak, körleştirilmiş [SigningPrivateKey](#signingprivatekey) veya geçici anahtar tarafından önceki baytların imzalanmasıyla oluşturulan bir [Signature](#signature) bulunur.

```bytefield
sigtype            | 2 | red    | 2 bytes
blinded_public_key | 8 | blue   | SigningPublicKey, varies
published          | 4 | green  | 4 bytes, seconds since epoch
expires            | 2 | yellow | 2 bytes
flags              | 2 | red    | 2 bytes
offline_signature  | 8 | orange | OfflineSignature, optional, varies
len                | 2 | gray   | Integer, 2 bytes
encrypted_data     | 8 | cyan   | Encrypted data, len bytes
signature          | 8 | purple | Signature, varies
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### Açıklama

* İmza, yukarıdaki veriler üzerindedir ve DatabaseStore türünü (5) içeren tek bayt ile BAŞINA EKLENMİŞTİR.

* İmza, hedefin imzalama public key'i kullanılarak doğrulanabilir veya leaseset2 başlığında çevrimdışı imza bulunuyorsa geçici imzalama public key'i kullanılarak doğrulanabilir.

* Kör etme ve şifreleme [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) içinde belirtilmiştir

* Bu yapı [LeaseSet2Header](#leaseset2header) kullanmaz.

* Maksimum gerçek sona erme süresi yaklaşık 660'tır (11 dakika), şifreli bir [MetaLeaseSet](#metaleaseset) olmadığı sürece.

* Şifrelenmiş leaseSet'ler ile çevrimdışı imzaların kullanımına ilişkin notlar için 123 numaralı öneriyi inceleyin.

* [LeaseSet2Header](#leaseset2header) içindeki 'published' alanı hakkındaki nota bakın
  (aynı sorun, burada LeaseSet2Header formatını kullanmasak bile)

* Maliyet genellikle SSU için 5 veya 6, NTCP için 10 veya 11'dir.

* Expiration şu anda kullanılmamaktadır, her zaman null'dur (tüm sıfırlar). 0.9.3 sürümünden itibaren, expiration sıfır olarak varsayılır ve saklanmaz, bu nedenle sıfır olmayan herhangi bir expiration RouterInfo imza doğrulamasında başarısız olacaktır. Expiration'ın uygulanması (veya bu byte'lar için başka bir kullanım) geriye dönük uyumsuz bir değişiklik olacaktır. Router'lar bu alanı tüm sıfırlar olarak ayarlamalıdır (MUST). 0.9.12 sürümünden itibaren, sıfır olmayan expiration alanı tekrar tanınmaktadır, ancak ağın büyük çoğunluğu bunu tanıyana kadar bu alanı kullanmak için birkaç sürüm beklemeliyiz.

JavaDoc: [net.i2p.data.EncryptedLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/EncryptedLeaseSet.html)

### RouterAddress

#### İçindekiler

Bu yapı, bir yönlendiriciye bir taşıma protokolü aracılığıyla nasıl ulaşılacağını tanımlar.

#### Notlar

0 ücretsiz ve 255 çok maliyetli olmak üzere, adresin kullanımının göreceli maliyetini tanımlayan 1 bayt [Tamsayı](#integer), ardından adresin kullanılmaması gereken son kullanma [Tarihi](#date) ya da null ise adresin süresinin dolmayacağı belirtilir. Bundan sonra bu yönlendirici adresinin kullandığı taşıma protokolünü tanımlayan bir [Dize](#string) gelir. Son olarak IP adresi, port numarası, e-posta adresi, URL vb. bağlantıyı kurmak için taşıma yöntemine özgü tüm seçenekleri içeren bir [Eşleme](#mapping) bulunur.

```bytefield
cost            | 1 | green  | Integer, 1 byte
expiration      | 7 | yellow | Date, 8 bytes
transport_style | 8 | blue   | String, 1-256 bytes
options         | 8 | purple | Mapping
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-/-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### Açıklama

* Aşağıdaki seçenekler zorunlu olmamakla birlikte standart kabul edilir ve çoğu router adresinde bulunması beklenir: "host" (bir IPv4 veya IPv6 adresi ya da host adı) ve "port".

* peer_size [Integer](#integer) değerini, o kadar router hash'inin listesi takip edebilir.
  Bu şu anda kullanılmamaktadır. Henüz uygulanmamış olan kısıtlı rotalar (restricted routes) için tasarlanmıştı.
  Belirli uygulamalar, imzanın değişmez olması için listenin sıralanmasını gerektirebilir.
  Bu özelliği etkinleştirmeden önce araştırılmalıdır.

* İmza, router_ident'in imzalama genel anahtarı kullanılarak doğrulanabilir.

* Tüm router bilgilerinde bulunması beklenen standart seçenekler için network veritabanı sayfasındaki [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo) bölümüne bakın.

JavaDoc: [net.i2p.data.router.RouterAddress](http://docs.i2p-projekt.de/net/i2p/data/router/RouterAddress.html)

### RouterInfo

#### İçindekiler

Bir router'ın ağın görmesi için yayınlamak istediği tüm verileri tanımlar. [RouterInfo](#routerinfo), ağ veritabanında saklanan iki yapıdan biridir (diğeri [LeaseSet](#leaseset)) ve içerdiği [RouterIdentity](#routeridentity)'nin SHA256'sı altında anahtarlanır.

#### Notlar

Girişin yayınlandığı [Tarih](#tarih) ile birlikte [RouterKimliği](#routerkimliği)

```bytefield
router_ident           | 8 | blue   | RouterIdentity, >= 387+ bytes
published              | 8 | green  | Date, 8 bytes
size                   | 1 | red    | Integer, 1 byte
RouterAddress 0        | 7 | yellow | varies
RouterAddress 1        | 8 | yellow | varies
RouterAddress ($size-1)| 8 | yellow | varies
psiz                   | 1 | red    | Integer, 1 byte
options                | 7 | purple | Mapping
signature              | 8 | cyan   | Signature, 40+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-/-+----+----+----+
|psiz| options                          |
+----+----+----+----+-/-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### Notlar

* Çok eski router'lar, imzanın değişmez olması için adreslerin verilerinin SHA256'sına göre sıralanmasını gerektiriyordu.
  Bu artık gerekli değil ve geriye dönük uyumluluk için uygulanmaya değmez.

- [ECIES](/docs/specs/ecies/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy)
- [ELGAMAL-AES](/docs/specs/elgamal-aes/)
- [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NAMING](/docs/overview/naming/)
- [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo)
- [Prop134](/proposals/134-gost/)
- [Prop169](/proposals/169-pq-crypto/)
- [REGISTRY](http://www.dns-sd.org/ServiceTypes.html)
- [SSU](/docs/legacy/ssu/)
- [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions)

* İmza, router_ident'in imzalama ortak anahtarı kullanılarak doğrulanabilir.

* Tüm yönlendirici bilgilerinde bulunması beklenen standart seçenekler için ağ veritabanı sayfasına bakın [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo).

* Çok eski yönlendiriciler, adreslerin verilerinin SHA256'ına göre sıralanmasını gerektiriyordu
  böylece imza değişmez olurdu.
  Bu artık gerekli değildir ve geriye dönük uyumluluk için uygulamaya değmez.

JavaDoc: [net.i2p.data.router.RouterInfo](http://docs.i2p-projekt.de/net/i2p/data/router/RouterInfo.html)

### Teslimat Talimatları

Tünel Mesaj Teslim Talimatları, Tünel Mesajı Spesifikasyonu'nda [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions) olarak tanımlanmıştır.

Garlic Message Delivery Instructions, I2NP Mesaj Spesifikasyonunda [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions) tanımlanmıştır.

## Kaynaklar

- [ECIES](/docs/specs/ecies/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy)
- [ELGAMAL-AES](/docs/specs/elgamal-aes/)
- [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [İSİMLENDİRME](/docs/overview/naming/)
- [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo)
- [Prop134](/proposals/134-gost/)
- [Prop169](/proposals/169-pq-crypto/)
- [KAYIT](http://www.dns-sd.org/ServiceTypes.html)
- [SSU](/docs/legacy/ssu/)
- [TÜNEL-DAĞITIMI](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions)
