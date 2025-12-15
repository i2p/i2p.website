---
title: "ECDSA anahtarı körleştirme"
number: "151"
author: "orignal"
created: "2019-05-21"
lastupdated: "2019-05-29"
status: "Açık"
thread: "http://zzz.i2p/topics/2717"
toc: true
---

## Motivasyon

Bazı insanlar EdDSA veya RedDSA'yı sevmiyor. Onlara bazı alternatifler sunmalıyız ve ECDSA imzalarını körleştirmelerine izin vermeliyiz.

## Genel Bakış

Bu öneri, ECDSA imza türleri 1, 2, 3 için anahtar körleştirmesini açıklar.

## Öneri

RedDSA ile aynı şekilde çalışır, ancak her şey Big Endian şeklindedir.
Sadece aynı imza türlerine izin verilir, örneğin 1->1, 2->2, 3->3.

### Tanımlar

B
    Eğrinin temel noktası

L
    Eliptik eğrinin grup düzeni. Eğrinin özelliği.

DERIVE_PUBLIC(a)
    B'yi bir eliptik eğri üzerinden çarparak bir özel anahtarı halka çevirin

alpha
    Hedefi bilenlerce bilinen 32 baytlık rastgele sayı.

GENERATE_ALPHA(destination, date, secret)
    Hedefi ve sırrı bilenler için geçerli tarih için alpha üretin.

a
    Hedefi imzalamak için kullanılan körleşmemiş 32 baytlık imzalama özel anahtarı

A
    Hedefteki körleşmemiş 32 baytlık imzalama halka anahtarı,
    = DERIVE_PUBLIC(a), ilgili eğride olduğu gibi

a'
    Şifreli kiralama setini imzalamak için kullanılan körleşmiş 32 baytlık imzalama özel anahtarı
    Bu geçerli bir ECDSA özel anahtarıdır.

A'
    Hedefteki körleşmiş 32 baytlık ECDSA imzalama halka anahtarı,
    DERIVE_PUBLIC(a') ile veya A ve alpha'dan üretilebilir.
    Bu eğride geçerli bir ECDSA halka anahtarıdır.

H(p, d)
    Hedef kelime öbeği p ve veri d'yi alan ve
    32 bayt uzunluğunda bir çıktı üreten SHA-256 hash fonksiyonu.

    SHA-256 aşağıdaki gibi kullanılır::

        H(p, d) := SHA-256(p || d)

HKDF(salt, ikm, info, n)
    İyi bir entropiye sahip olması gereken bazı giriş anahtar materyallerini ikm (yerine tekdüze rastgele bir dize olmak zorunda değildir), 32 bayt uzunluğunda bir tuz ve bağlama özgü bir 'info' değerini alan
    ve anahtar materyali olarak kullanım için uygun n baytlık bir çıktı üreten kriptografik anahtar türetme fonksiyonu.

    [RFC-5869](https://tools.ietf.org/html/rfc5869)'da belirtilen şekilde, [RFC-2104](https://tools.ietf.org/html/rfc2104)'te belirtilen HMAC hash fonksiyonu SHA-256 kullanarak hesaplarsanız. Bu, SALT_LEN'in maksimum 32 bayt olduğu anlamına gelir.


### Körleştirme Hesaplamaları

Her gün (UTC) yeni bir gizli alpha ve körleşmiş anahtarlar üretilmelidir.
Gizli alpha ve körleşmiş anahtarlar aşağıdaki gibi hesaplanır.

GENREATE_ALPHA(destination, date, secret), tüm taraflar için:

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret isteğe bağlıdır, aksi takdirde sıfır uzunluğunda
  A = hedefin imzalama halka anahtarı
  stA = A'nın imza tipi, 2 baytlık big endian (0x0001, 0x0002 veya 0x0003)
  stA' = körleşmiş halka anahtar A'nın imza tipi, 2 baytlık big endian, her zaman stA ile aynı
  keydata = A || stA || stA'
  datestring = geçerli tarihten UTC 8 baytlık ASCII YYYYMMDD
  secret = UTF-8 kodlanmış dize
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // seed'i 64 baytlık big-endian değer olarak ele alın
  alpha = seed mod L
```


BLIND_PRIVKEY(), kira setini yayımlayan sahip için:

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  a = hedefin imzalama özel anahtarı
  // Skalare aritmetik kullanılarak toplama
  körleşmiş imzalama özel anahtarı = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  körleşmiş imzalama halka anahtarı = A' = DERIVE_PUBLIC(a')
```


BLIND_PUBKEY(), kira setini alan istemciler için:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = hedefin imzalama halka anahtarı
  // Grup elemanları (eğri üzerindeki noktalar) kullanılarak toplama
  körleşmiş halka anahtarı = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```


Her iki A' hesaplama yöntemi de gerektiği gibi aynı sonucu verir.

## b33 adresi

ECDSA'nın halka anahtarı (X,Y) çifti olduğu için, örneğin P256 için 32 değil 64 bayttır.
Ya b33 adresi daha uzun olacak ya da halka anahtar bitcoin cüzdanlarındaki gibi sıkıştırılmış formatta saklanabilir.


## Referanslar

* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
