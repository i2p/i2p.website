```markdown
---
title: "Post-Kuantum Kripto Protokolleri"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Açık"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
---

## Genel Bakış

Uygun post-kuantum (PQ) kriptografisi için araştırma ve rekabet on yılı aşkın süredir devam etmekte olsa da, seçimler ancak son zamanlarda netleşmiştir.

PQ kriptosunun etkilerine 2022 yılında bakmaya başladık [FORUM](http://zzz.i2p/topics/3294).

TLS standartları son iki yılda hibrit şifreleme desteği ekledi ve şu anda internetteki şifreli trafiğin önemli bir kısmında Chrome ve Firefox desteği sayesinde kullanılmaktadır [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/).

NIST, kısa süre önce post-kuantum kriptografisi için önerilen algoritmaları nihayetlendirdi ve yayınladı [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards).
Birkaç ortak kriptografi kütüphanesi artık NIST standartlarını desteklemekte veya yakında destek vereceklerdir.

Hem [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/) hem de [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) göçün hemen başlamasını öneriyor. Ayrıca 2022 NSA PQ SSS'e bakınız [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF).
I2P güvenlik ve kriptografide öncü olmalıdır.
Tavsiye edilen algoritmaları uygulamanın zamanı geldi.
Esnek kripto tipi ve imza tipi sistemimizi kullanarak, hibrit kripto ve PQ ile hibrit imzalar için tipler ekleyeceğiz.

## Hedefler

- PQ'ye dayanıklı algoritmaları seçme
- Uygun yerlerde I2P protokollerine sadece PQ ve hibrit algoritmaları ekleme
- Birden fazla varyant tanımlama
- Uygulama, test, analiz ve araştırmadan sonra en iyi varyantları seçme
- Geriye dönük uyumluluk ile kademeli destek ekleme

## Hedef Olmayanlar

- Tek yönlü (Noise N) şifreleme protokollerini değiştirmemek
- SHA256'dan uzaklaşmamak, kısa vadede PQ tarafından tehdit edilemez
- Şu anda nihai tercihi belirlememek

## Tehdit Modeli

- OBEP veya IBGW'deki yönlendiriciler, muhtemelen işbirliği yapanlar,
  doğru gizlilik için daha sonra şifre çözmek üzere sarımsak mesajlarını saklama (ileri gizlilik)
- Ağ gözlemcileri
  taşıma mesajlarını daha sonra şifre çözmek üzere saklama (ileri gizlilik)
- Ağ katılımcıları RI, LS, akış, datagramlar,
  veya diğer yapılar için imza sahteciliği

## Etkilenen Protokoller

Aşağıdaki protokolleri, gelişim sırasına göre değiştirileceğiz.
Genel dağıtım muhtemelen 2025 sonundan 2027 ortalarına kadar sürecektir.
Detaylar için aşağıdaki Öncelikler ve Dağıtım bölümüne bakınız.

```
| Protokol / Özellik | Durum |
| ------------------ | ----- |
| Hibrit MLKEM Ratchet ve LS | 2026-0 |
| Hibrit MLKEM NTCP2 | Bazı d |
| Hibrit MLKEM SSU2 | Bazı d |
| MLDSA İmzalı Tipler 12-14 | Teklif |
| MLDSA Hedefler | Canlı |
| Hibrit İmzalı Tipler 15-17 | İlk |
| Hibrit Hedefler |  |

```

## Tasarım

NIST FIPS 203 ve 204 standartlarını destekleyeceğiz [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
ki bunlar baz alınmış ancak
CRYSTALS-Kyber ve CRYSTALS-Dilithium ile uyumlu DEĞİLDİR (sürümler 3.1, 3 ve eski).

### Anahtar Değişimi

Aşağıdaki protokollerde hibrit anahtar değişimini destekleyeceğiz:

```
| Protoko | Gürültü | ürü  Yalnızca PQ | estekler mi?  H |
| ------- | ------- | ---------------- | --------------- |
| NTCP2 | XK | hayır | evet |
| SSU2 | XK | hayır | evet |
| Ratchet | IK | hayır | evet |
| TBM | N | hayır | hayır |
| NetDB | N | hayır | hayır |

```

PQ KEM yalnızca geçici anahtarlar sağlar ve statik anahtar el sıkışmalarını doğrudan desteklemez
Noise XK ve IK gibi.

Noise N iki yönlü anahtar değişimi kullanmaz ve bu nedenle hibrit şifreleme için uygun değildir.

Bu yüzden sadece NTCP2, SSU2 ve Ratchet için hibrit şifreleme destekleyeceğiz.
[FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) gibi üç yeni şifreleme türü için üç ML-KEM varyantını tanımlayacağız.
Hibrit türler yalnızca X25519 ile kombinasyon halinde tanımlanacak.

Yeni şifreleme türleri şunlardır:

```
| Tip | Kod |
| --- | --- |
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |

```

Aşırı yük önemli ölçüde artacaktır. Tipik mesaj 1 ve 2 boyutları (XK ve IK için)
şu anda yaklaşık 100 bayttır (herhangi bir ek yüklemeden önce).
Bu, algoritmaya bağlı olarak 8x ila 15x artacaktır.

### İmzalar

Aşağıdaki yapılarda PQ ve hibrit imzaları destekleyeceğiz:

```
| Tür | Yalnızca PQ D | tekler mi?  Hib |
| --- | ------------- | --------------- |
| Yönlendirme Bilgileri | evet | evet |
| LeaseSet | evet | evet |
| Akış SYN/SYNACK/Kapat | evet | evet |
| Cevaplanabilir Datagramlar | evet | evet |
| Datagram2 (öneri 163) | evet | evet |
| I2CP oturum oluşturma mesa | evet | evet |
| SU3 dosyaları | evet | evet |
| X.509 sertifikaları | evet | evet |
| Java anahtar depoları | evet | evet |

```

Bu yüzden hem yalnızca PQ hem de hibrit imzaları destekleyeceğiz.
[FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) gibi üç ML-DSA varyantını tanımlayacağız,
Ed25519 ile üç hibrit varyant ve yalnızca SU3 dosyaları için ön hash ile üç yalnızca PQ varyantı,
toplamda 9 yeni imza türü için.
Hibrit türler yalnızca Ed25519 ile kombinasyon halinde tanımlanacak.
SU3 dosyaları hariç standart ML-DSA'yı, ön-hash (HashML-DSA) varyantlarını KULLANMAYACAĞIZ.

```
| Tip | od |
| --- | --- |
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |

```

X.509 sertifikaları ve diğer DER kodlamaları
[COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/) 'de tanımlanan bileşik yapıları ve OID'leri kullanacaktır.

Aşırı yük önemli ölçüde artacaktır. Tipik Ed25519 hedef ve yönlendirici kimliği boyutları 391 bayttır.
Bunlar algoritmaya bağlı olarak 3,5x ila 6,8x artacaktır.
Ed25519 imzaları 64 bayttır.
Bunlar algoritmaya bağlı olarak 38x ila 76x artacaktır.
Tipik imzalanmış RouterInfo, LeaseSet, cevaplanabilir datagramlar ve imzalanmış akış mesajları yaklaşık 1KB'tır.
Bunlar algoritmaya bağlı olarak 3x ila 8x artacaktır.

Yeni hedef ve yönlendirici kimlik türleri padding içermeyeceğinden,
sıkıştırılamayacaktır. Hedef ve yönlendirici kimliklerinin
gzipped olarak taşınırken boyutları algoritmaya bağlı olarak 12x - 38x artacaktır.

### Yasal Kombinasyonlar

Hedefler için, yeni imza türleri mosok işn tüm kripto türleri ile desteklenir.
Anahtar sertifikasında şifreleme türünü YOK (255) olarak ayarlayın.

Yönlendirici Kimlikleri için, ElGamal şifreleme türü kullanımdan kaldırılmıştır.
Yeni imza türleri yalnızca X25519 (tür 4) şifreleme ile desteklenir.
Yeni şifreleme türleri Yönlendirici Adreslerinde belirtilecektir.
Anahtar sertifikasındaki şifreleme türü tür 4 olarak kalacaktır.

### Yeni Kripto Gereklilikleri

- ML-KEM (eski adıyla CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (eski adıyla CRYSTALS-Dilithium) [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (eski adıyla Keccak-256) [FIPS202]_ yalnızca SHAKE128 için kullanılır
- SHA3-256 (eski adıyla Keccak-512) [FIPS202]_
- SHAKE128 ve SHAKE256 (SHA3-128 ve SHA3-256'nın XOF uzantıları) [FIPS202]_

SHA3-256, SHAKE128 ve SHAKE256 için test vektörleri [NIST-VECTORS]_'te bulunmaktadır.

Java bouncycastle kütüphanesinin yukarıdakilerin tümünü desteklediğine dikkat edin.
C++ kütüphane desteği OpenSSL 3.5 [OPENSSL]_ 'de bulunmaktadır.

### Alternatifler

[FIPS205]_ (Sphincs+) desteklenmeyecek, ML-DSA'dan çok daha yavaş ve büyüktür.
Yaklaşan FIPS206 (Falcon) desteklenmeyecek, henüz standartlaştırılmamıştır.
NTRU veya NIST tarafından standartlaştırılmayan diğer PQ adayları desteklenmeyecek.

Rosenpass
`````````
Bazı araştırmalar [PQ-WIREGUARD]_ Wireguard (IK) için saf PQ kriptografisi uyarlamasını öneriyor, ancak makalede birkaç açık soru bulunmaktadır.
Daha sonra, Rosenpass [Rosenpass]_ [Rosenpass-Whitepaper]_ olarak PQ Wireguard için uygulandı.

Rosenpass, öntanımlı Classic McEliece 460896 statik anahtarlar (her biri 500 KB) ve Kyber-512 (esas olarak MLKEM-512) geçici anahtarlarla Noise KK benzeri bir el sıkışması kullanır.
Classic McEliece şifrelemeleri yalnızca 188 bayt olduğundan ve Kyber-512
açık anahtarları ve şifrelemeleri makul olduğundan, her iki el sıkışma mesajı standart bir UDP MTU'ya sığmaktadır.
PQ KK el sıkışmasından çıkan paylaşılan anahtar (osk) standart Wireguard IK el sıkışması için
girdi önceden paylaşılan anahtar (psk) olarak kullanılır.
Bu yüzden toplamda iki tam el sıkışması vardır, biri saf PQ ve biri saf X25519.

XK ve IK el sıkışmalarımızı değiştirmek için bunlardan hiçbirini yapamayız çünkü:

- KK yapamıyoruz, Bob Alice'in statik anahtarına sahip değil
- 500 KB statik anahtarlar çok büyük
- Ekstra bir gidiş-gelişe ihtiyacımız yok

Makale'de iyi bilgiler var,
ve biz de fikir ve ilham almak için gözden geçireceğiz. TODO.

## Özellikler

### Genel Yapılar

[COMMON](https://geti2p.net/spec/common-structures)'daki bölümleri ve tabloları şu şekilde güncelleyin:

Genel Anahtar
````````````````

Yeni Genel Anahtar türleri şunlardır:

```
| Tür | Genel Anahtar Uzu | luğu O | u Tar |
| --- | ----------------- | ------ | ----- |
| MLKEM512_X25519 | 32 | 0.9. | Tek |
| MLKEM768_X25519 | 32 | 0.9. | Tek |
| MLKEM1024_X25519 | 32 | 0.9. | Tek |
| MLKEM512 | 800 | 0.9. | Tek |
| MLKEM768 | 1184 | 0.9. | Tek |
| MLKEM1024 | 1568 | 0.9. | Tek |
| MLKEM512_CT | 768 | 0.9. | Tek |
| MLKEM768_CT | 1088 | 0.9. | Tek |
| MLKEM1024_CT | 1568 | 0.9. | Tek |
| YOK | 0 | 0.9.x | Tekl |

```

Hibrit genel anahtarlar X25519 anahtarıdır.
KEM genel anahtarları Alice'ten Bob'a gönderilen geçici PQ anahtarıdır.
Kodlama ve bayt sırası [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) 'de tanımlanmıştır.

MLKEM*_CT anahtarları gerçekten genel anahtarlar değil, Noise el sıkışmasında Bob'dan Alice'e gönderilen "şifreli metin" dir.
Tamlık için burada listelenmiştir.

Özel Anahtar
````````````````

Yeni Özel Anahtar türleri şunlardır:

```
| Tür | Özel Anahtar Uzunl | ğu  O | Tari |
| --- | ------------------ | ----- | ---- |
| MLKEM512_X25519 | 32 | 0.9.xx | Tekli |
| MLKEM768_X25519 | 32 | 0.9.xx | Tekli |
| MLKEM1024_X25519 | 32 | 0.9.xx | Tekli |
| MLKEM512 | 1632 | 0.9.xx | Tekli |
| MLKEM768 | 2400 | 0.9.xx | Tekli |
| MLKEM1024 | 3168 | 0.9.xx | Tekli |

```

Hibrit özel anahtarlar X25519 anahtarlarıdır.
KEM özel anahtarları yalnızca Alice içindir.
KEM kodlaması ve bayt sırası [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) 'de tanımlanmıştır.

İmza Genel Anahtar
````````````````

Yeni İmza Genel Anahtar türleri şunlardır:

```
| Tür | Uzunluk (bayt) | O Şu | rihte |
| --- | -------------- | ---- | ----- |
| MLDSA44 | 1312 | 0.9.xx | Tekli |
| MLDSA65 | 1952 | 0.9.xx | Tekli |
| MLDSA87 | 2592 | 0.9.xx | Tekli |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | Tekli |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | Tekli |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | Tekli |
| MLDSA44ph | 1344 | 0.9.xx | Yalnı |
| MLDSA65ph | 1984 | 0.9.xx | Yalnı |
| MLDSA87ph | 2624 | 0.9.xx | Yalnı |

```

Hibrit imza genel anahtarları [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/) 'de tanımlandığı gibi Ed25519 anahtarı ardından PQ anahtarıdır.
Kodlama ve bayt sırası [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 'de tanımlanmıştır.

İmza Özel Anahtar
````````````````

Yeni İmza Özel Anahtar türleri şunlardır:

```
| Tür | Uzunluk (bayt) | O Şu | rihte |
| --- | -------------- | ---- | ----- |
| MLDSA44 | 2560 | 0.9.xx | Tekli |
| MLDSA65 | 4032 | 0.9.xx | Tekli |
| MLDSA87 | 4896 | 0.9.xx | Tekli |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | Tekli |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | Tekli |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | Tekli |
| MLDSA44ph | 2592 | 0.9.xx | Yalnı |
| MLDSA65ph | 4064 | 0.9.xx | Yalnı |
| MLDSA87ph | 4928 | 0.9.xx | Yalnı |

```

Hibrit imza özel anahtarları [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/) 'de tanımlandığı gibi Ed25519 anahtarı ardından PQ anahtarıdır.
Kodlama ve bayt sırası [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 'de tanımlanmıştır.

İmza
``````````

Yeni İmza türleri şunlardır:

```
| Tür | Uzunluk (bayt) | O Şu | rihte |
| --- | -------------- | ---- | ----- |
| MLDSA44 | 2420 | 0.9.xx | Tekli |
| MLDSA65 | 3309 | 0.9.xx | Tekli |
| MLDSA87 | 4627 | 0.9.xx | Tekli |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | Tekli |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | Tekli |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | Tekli |
| MLDSA44ph | 2484 | 0.9.xx | Yalnı |
| MLDSA65ph | 3373 | 0.9.xx | Yalnı |
| MLDSA87ph | 4691 | 0.9.xx | Yalnı |

```

Hibrit imzalar, [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/) 'de olduğu gibi Ed25519 imzası ardından PQ imzasıdır.
Hibrit imzalar, her iki imza doğrulanarak doğrulanır ve biri başarısız olursa başarısız olur.
Kodlama ve bayt sırası [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 'de tanımlanmıştır.

Anahtar Sertifikaları
``````````````````````

Yeni İmza Genel Anahtar türleri şunlardır:

```
| Tür | ür Kodu | plam Genel Anahtar Uzun | ğu  O | Tari |
| --- | ------- | ----------------------- | ----- | ---- |
| MLDSA44 | 12 | 1312 | 0.9.xx | Tekli |
| MLDSA65 | 13 | 1952 | 0.9.xx | Tekli |
| MLDSA87 | 14 | 2592 | 0.9.xx | Tekli |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | Tekli |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | Tekli |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | Tekli |
| MLDSA44ph | 18 | n/a | 0.9.xx | Yalnı |
| MLDSA65ph | 19 | n/a | 0.9.xx | Yalnı |
| MLDSA87ph | 20 | n/a | 0.9.xx | Yalnı |

```

Yeni Kripto Genel Anahtar türleri şunlardır:

```
| Tür | Tür Kodu | Toplam Genel Anahtar Uz | luğu | Şu Ta |
| --- | -------- | ----------------------- | ---- | ----- |
| MLKEM512_X25519 | 5 | 32 | .9.xx | eklif |
| MLKEM768_X25519 | 6 | 32 | .9.xx | eklif |
| MLKEM1024_X25519 | 7 | 32 | .9.xx | eklif |
| YOK | 255 | 0 | 9.xx | klif |

```

Hibrit anahtar türleri asla anahtar sertifikalarında dahil edilmez; yalnızca leaseset'lerde.

Hibrit veya PQ imza türleri olan hedefler için,
şifreleme türü YOK (tür 255) kullanın,
ancak kripto anahtarı yoktur ve
tüm 384 baytlık ana bölüm imza anahtarı içindir.

Hedef boyutları
``````````````````

Yeni Hedef türleri için uzunluklar burada.
Tüm şifreleme türü YOK (tür 255) ve şifreleme anahtarı uzunluğu 0 olarak kabul edilir.
384 baytlık tüm bölüm imza genel anahtarının ilk bölümü için kullanılır.
NOT: Kullanılmayan 256 baytlık ElGamal anahtarını
konum koruma için tutan ECDSA_SHA512_P521 ve RSA imza türlerinin spesifikasyonundan farklıdır.

Yastık yok.
Toplam uzunluk 7 + toplam anahtar uzunluğudur.
Anahtar sertifikası uzunluğu 4 + fazla anahtar uzunluğudur.

Örnek 1319 bayt uzunluğunda MLDSA44 hedef bayt akımı:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

```
| Tür | ür Kodu | plam Genel Anahtar Uzun | ğu  An | Faz | Top |
| --- | ------- | ----------------------- | ------ | --- | --- |
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |

```

Yönlendirici Kimlik boyutları
````````````````````````````

Yeni Hedef türlerinin uzunlukları burada.
Tüm şifreleme türü X25519 (tür 4).
X28819 genel anahtardan sonraki 352 baytlık tüm bölüm imza genel anahtarının ilk bölümü için kullanılır.
Yastık yok.
Toplam uzunluk 39 + toplam anahtar uzunluğudur.
Anahtar sertifikası uzunluğu 4 + fazla anahtar uzunluğudur.

Örnek 1351 bayt uzunluğunda yönlendirici kimlik bayt akımı için MLDSA44:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

```
| Tür | ür Kodu | plam Genel Anahtar Uzun | ğu  An | Faz | Top |
| --- | ------- | ----------------------- | ------ | --- | --- |
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |

```
### Tokalaşma Modelleri

Tokalaşmalar [Noise]_ tokalaşma modelleri kullanır.

Aşağıdaki harf eşlemesi kullanılır:

- e = tek seferlik geçici anahtar
- s = statik anahtar
- p = mesaj yükü
- e1 = Alice'ten Bob'a gönderilen geçici PQ anahtarı
- ekem1 = Tokalaşmada Bob'dan Alice'e gönderilen KEM şifreli metni

XK ve IK için hibrit forward gizliliği (hfs) için aşağıdaki modifikasyonlar
[Noise-Hybrid]_ bölüm 5'de belirtildiği gibi yapılmaktadır:

```dataspec

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

e1 ve ekem1 şifrelidir. Aşağıdaki model tanımlamalarına bakınız.
NOT: e1 ve ekem1 farklı büyüklüklerdedir (X25519'dan farklı olarak)

```

e1 modeli aşağıdaki gibi tanımlanmıştır ve [Noise-Hybrid]_ bölüm 4'te belirtilmiştir:

```dataspec

Alice için:
   (encap_key, decap_key) = PQ_KEYGEN()

   // EncryptAndHash(encap_key)
   şifreli metin = ENCRYPT(k, n, encap_key, ek)
   n++
   MixHash(şifreli metin)

Bob için:

   // DecryptAndHash(şifreli metin)
   encap_key = DECRYPT(k, n, şifreli metin, ek)
   n++
   MixHash(şifreli metin)

```

ekem1 modeli aşağıdaki gibi tanımlanmıştır ve [Noise-Hybrid]_ bölüm 4'te belirtilmiştir:

```dataspec

Bob için:

   (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

   // EncryptAndHash(kem şifreli metin)
   şifreli metin = ENCRYPT(k, n, kem_ciphertext, ek)
   MixHash(şifreli metin)

   // MixKey
   MixKey(kem_shared_key)

Alice için:

   // DecryptAndHash(şifreli metin)
   kem_ciphertext = DECRYPT(k, n, şifreli metin, ek)
   MixHash(şifreli metin)

   // MixKey
   kem_shared_key = DECAPS(kem_ciphertext, decap_key)
   MixKey(kem_shared_key)

```

### Noise Tokalaşma KDF

Sorunlar
``````

- Tokalaşma hash fonksiyonumuzu değiştirmeli miyiz? [Choosing-Hash]_ bakınız.
  SHA256 PQ'den etkilenmez, ancak hash fonksiyonumuzu yükseltmek istiyorsak,
  şimdi değiştirirken yapmamız gereken zaman.
  Mevcut IETF SSH önerisi [SSH-HYBRID]_ MLKEM768'i SHA256 ile,
  MLKEM1024'ü SHA384 ile kullanmayı öneriyor. O öneri,
  güvenlik değerlendirmeleri hakkında bir tartışma içeriyor.
- 0-RTT ratchet verisi göndermeyi durdurmalı mıyız (LS dışındaki)?
- 0-RTT veri göndermiyorsak ratchet'ı XK'ye geçirmeli miyiz?

Genel Bakış
````````

Bu bölüm hem IK hem de XK protokolleri için geçerlidir.

Hibrit tokalaşma [Noise-Hybrid]_ 'de tanımlanmıştır.
İlk mesaj, Alice'ten Bob'a, e1 içerir, kaplama anahtarı,
mesaj yükünden önce. Ek bir statik anahtar olarak kabul edilir; Unity'ye EncryptAndHash() (Alice olarak) çağrısını yapın
veya DecryptAndHash() (Bob olarak).
Daha sonra mesaj yükünü her zamanki gibi işle.

İkinci mesaj, Bob'dan Alice'e, e1'den önce ekem1 olan şifreli metni içerir.
Ek bir statik anahtar olarak kabul edilir; Unity'ye EncryptAndHash() (Bob olarak)
veya DecryptAndHash() (Alice olarak) çağrısını yapın.
Daha sonra kem_shared_key'i hesaplayın ve MixKey(kem_shared_key) çağrısını yapın.
Sonra mesaj yükünü her zamanki gibi işle.

Tanımlı ML-KEM Operasyonları
```````````````````````````

Kullanılan kriptografik yapı taşlarına karşı gelen aşağıdaki işlevleri tanımlıyoruz
[FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) 'de tanımlandığı gibi.

(encap_key, decap_key) = PQ_KEYGEN()
Alice kaplama ve ayırma anahtarlarını oluşturur
Kaplama anahtarı mesaj 1'de gönderilir.
encap_key ve decap_key boyutları ML-KEM varyantına bağlı olarak değişir.

(şifreli metin, kem_shared_key) = ENCAPS(encap_key)
Bob, mesaj 1'de aldığı şifreli metni kullanarak
şifreli metni ve paylaşılan anahtarı hesaplar.
Şifreli metin mesaj 2'de gönderilir.
Şifreli metin boyutu ML-KEM varyantına bağlı olarak değişir.
kem_shared_key her zaman 32 bayttır.

kem_shared_key = DECAPS(şifreli metin, decap_key)
Alice, mesaj 2'de aldığı şifreli metni kullanarak
paylaşılan anahtarı hesaplar.
kem_shared_key her zaman 32 bayttır.

Not: Kaplama anahtarı ve şifreli metin, Noise tokalaşması mesajlarında ChaCha/Poly blokları içinde şifrelenmiştir.
Tokalaşma işleminin bir parçası olarak şifresi çözülecektir.

kem_shared_key, zincirleme anahtarına MixHash() ile karıştırılır.
Detaylar için aşağıya bakınız.

Alice KDF Mesaj 1
````````````````````

XK için: 'es' mesaj modelinden sonra ve yükten önce ekleyin:

VEYA

IK için: 'es' mesaj modelinden sonra ve 's' mesaj modelinden önce ekleyin:

```text
Bu "e1" mesaj modeli:
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
// AEAD parametreleri
k = keydata[32:63]
n = 0
ad = h
şifreli metin = ENCRYPT(k, n, encap_key, ad)
n++

// MixHash(şifreli metin)
h = SHA256(h || şifreli metin)

"e1" mesaj modelinin sonu.

NOT: Bir sonraki bölüm için (XK için yük veya IK için statik anahtar),
keydata ve zincir anahtarı aynı kalır,
ve n artık 1'e eşittir (hibrit olmayan için 0 yerine).

```

Bob KDF için Mesaj 1
````````````````````

XK için: 'es' mesaj modelinden sonra ve yükten önce ekleyin:

VEYA

IK için: 'es' mesaj modelinden sonra ve 's' mesaj modelinden önce ekleyin:

```text
Bu "e1" mesaj modeli:

// DecryptAndHash(encap_key_bölümü)
// AEAD parametreleri
k = keydata[32:63]
n = 0
ad = h
encap_key = DECRYPT(k, n, encap_key_bölümü, ad)
n++

// MixHash(encap_key_bölümü)
h = SHA256(h || encap_key_bölümü)

"e1" mesaj modelinin sonu.

NOT: Bir sonraki bölüm için (XK için yük veya IK için statik anahtar),
keydata ve zincir anahtarı aynı kalır,
ve n artık 1'e eşittir (hibrit olmayan için 0 yerine).

```

Bob KDF için Mesaj 2
````````````````````

XK için: 'ee' mesaj modelinden sonra ve yükten önce ekleyin:

VEYA

IK için: 'ee' mesaj modelinden sonra ve 'se' mesaj modelinden önce ekleyin:

```text
Bu "ekem1" mesaj modeli:

(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem şifreli metin)
// AEAD parametreleri
k = keydata[32:63]
n = 0
ad = h
şifreli metin = ENCRYPT(k, n, kem_ciphertext, ad)

// MixHash(şifreli metin)
h = SHA256(h || şifreli metin)

// MixKey(kem_shared_key)
keydata = HKDF(chainKey, kem_shared_key, "", 64)
chainKey = keydata[0:31]

"ekem1" mesaj modelinin sonu.

```

Alice KDF Mesaj 2
````````````````````

'ee' mesaj modelinden sonra (IK için 'ss' mesaj modelinden önce):

```text
Bu "ekem1" mesaj modeli:

// DecryptAndHash(kem_ciphertext_section)
// AEAD parametreleri
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

"ekem1" mesaj modelinin sonu.

```

KDF Mesaj 3 (sadece XK)
```````````````````````
değişmeden

KDF için böl(split)
```````````````````
değişmeden

### Ratchet

ECIES-Ratchet spesifikasyonunu [ECIES](https://geti2p.net/spec/ecies) olarak güncelleyin:

Gürültü tanımlayıcıları
```````````````````

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

1b) Yeni oturum formatı (bağlama ile)
`````````````````````````````````````

Değişiklikler: Mevcut ratchet, ilk ChaCha bölümünde statik anahtarı içeriyordu,
ve ikinci bölümde yük.
ML-KEM ile artık üç bölüm var.
İlk bölüm şifreli PQ genel anahtarını içerir.
İkinci bölüm statik anahtar içerir.
Üçüncü bölüm yükü içerir.

Şifrelenmiş format:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Yeni Oturum Geçici Genel Anahtar    |
  +             32 bayt                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           ML-KEM encap_key            +
  |       ChaCha20 şifreli veri           |
  +      (aşağıdaki tabloya bakın)        +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Kimlik Doğrulama Kodu |
  +    encap_key Bölümü için (MAC)        +
  |             16 bayt                   |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           X25519 Statik Anahtar       +
  |       ChaCha20 şifreli veri           |
  +             32 bayt                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Kimlik Doğrulama Kodu |
  +    Statik Anahtar Bölümü için (MAC)   +
  |             16 bayt                   |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Yük Bölümü                 +
  |       ChaCha20 şifreli veri           |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Kimlik Doğrulama Kodu |
  +         Yük Bölümü için (MAC)         +
  |             16 bayt                   |
  +----+----+----+----+----+----+----+----+
```

Şifre çözülmüş format:

```dataspec
Yük Bölüm 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM encap_key                +
  |                                       |
  +      (aşağıdaki tabloya bakın)        +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Yük Bölüm 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X25519 Statik Anahtar           +
  |                                       |
  +      (32 bayt)                        +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Yük Bölüm 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Yük Bölümü                 +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```

Boyutlar:

```
| Tür | Tür Kodu | X len | Mesaj 1 L | g  Mesaj 1 Şi | eli Long Mesa | 1 Şifre Çö | ü Long |
| --- | -------- | ----- | --------- | ------------- | ------------- | ---------- | ------ |
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |

```

Not: yük mutlaka DateTime blok içermelidir, bu yüzden minimum yük boyutu 7'dir.
Minimum mesaj 1 boyutları buna göre hesaplanabilir.

1g) Yeni Oturum Yanıtı formatı
``````````````````````````````

Değişiklikler: Mevcut ratchet, ilk ChaCha bölümünde boş bir yük içeriyordu,
ve ikinci bölümde yük.
ML-KEM ile artık üç bölüm var.
İlk bölüm şifreli PQ şifreli metnini içerir.
İkinci bölümde boş yük vardır.
Üçüncü bölüm yükü içerir.

Şifreli format:

```dataspec
+----+----+----+----+----+----+----+----+
  |       Oturum Etiketi 8 bayt          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Geçici Genel Anahtar           +
  |                                       |
  +            32 bayt                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | ChaCha20 şifreli ML-KEM şifreli metni |
  +      (aşağıdaki tabloya bakın)        +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Kimlik Doğrulama Kodu |
  +  şifreli metni Bölümü için (MAC)      +
  |             16 bayt                   |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Kimlik Doğrulama Kodu |
  +  anahtar Bölümü için (MAC) (veri yok) +
  |             16 bayt                   |
  +----+----+----
  ```
  
Şifre çözülmüş format:

.. raw:: html

{% highlight lang='dataspec' %}
Yük Bölüm 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM şifreli metni            +
  |                                       |
  +      (aşağıdaki tabloya bakın)        +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Yük Bölüm 2:

  boş

  Yük Bölüm 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Yük Bölümü                 +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```

Boyutlar:

```
| Tür | Tür Kodu | Y len | Mesaj 2 L | g  Mesaj 2 Şi | eli Long Mesa | 2 Şifre Çö | ü Long |
| --- | -------- | ----- | --------- | ------------- | ------------- | ---------- | ------ |
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |

```

Not: ikinci mesaj genellikle boş olmayan bir yükleme sahiptir,
ratchet spesifikasyonu ise [ECIES](https://geti2p.net/spec/ecies) gerekli olmadığını belirtir, bu yüzden minimum yük büyüklüğü 0'dır.
İkinci mesajın minimum uzunlukları buna göre hesaplanabilir.

### NTCP2

NTCP2 spesifikasyonunu [NTCP2](https://geti2p.net/spec/ntcp2) olarak güncelleyin:

Gürültü tanımlayıcıları
```````````````````

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

1) Oturum İsteği
``````````````````

Değişiklikler: Mevcut NTCP2 yalnızca ChaCha bölümünde seçenekleri içerir.
ML-KEM ile, ChaCha bölümü ayrıca şifreli PQ genel anahtarını içerecektir.

Ham içerik:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +        RH_B ile gizlenmiş             +
  |       AES-CBC-256 şifreli X           |
  +             (32 bayt)                 +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly çerçeve (MLKEM)          |
  +      (aşağıdaki tabloya bakın)        +
  |   Mesaj 1 için KDF'de tanımlanan k    |
  +   n = 0                               +
  |   ilişkili veri için KDF'ye bakın     |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly çerçeve (seçenekler)     |
  +         32 bayt                       +
  |   Mesaj 1 için KDF'de tanımlanan k    |
  +   n = 0                               +
  |   ilişkili veri için KDF'ye bakın     |
  +----+----+----+----+----+----+----+----+
  |     şifrelenmemiş kimlik doğrulamalı  |
  ~         dolgu (isteğe bağlı)          ~
  |     seçenekler bloğunda tanımlanan    |
  |     uzunluk                           |
  +----+----+----+----+----+----+----+----+

  Öncekinin aynısı, sadece ikinci bir ChaChaPoly çerçeve ekleyin

```

Şifre çözülmüş veri (Poly1305 otantifikasyon etiketi gösterilmemiştir):

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bayt)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (aşağıdaki tabloya bakın)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               seçenekler              |
  +              (16 bayt)                +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     şifrelenmemiş kimlik doğrulamalı  |
  +         dolgu (isteğe bağlı)          +
  |     seçenekler bloğunda tanımlanan    |
  ~              .   .   .                ~
  |     uzunluk                           |
  +----+----+----+----+----+----+----+----+
```

Boyutlar:

```
| Tür | Tür Kodu | X len | Mesaj 1 L | g  Mesaj 1 Şi | eli Long Mesa | 1 Şifre Çö | ü Long |
| --- | -------- | ----- | --------- | ------------- | ------------- | ---------- | ------ |
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |

```

Not: Tür kodları sadece dahili kullanım içindir. Yönlendiriciler tür 4 olarak kalacak,
ve destek yönlendirici adreslerinde belirtilecektir.

2) Oturum Oluşturuldu
``````````````````

Değişiklikler: Mevcut NTCP2 yalnızca ChaCha bölümünde seçenekleri içerir.
ML-KEM ile, ChaCha bölümü ayrıca şifreli PQ genel anahtarını içerecektir.

Ham içerik:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +        RH_B ile gizlenmiş             +
  |       AES-CBC-256 şifreli Y           |
  +              (32 bayt)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly çerçeve (MLKEM)          |
  +   Şifrelenmiş ve kimlik doğrulamalı   +
  -      (aşağıdaki tabloya bakın)        -
  +   Mesaj 2 için KDF'de tanımlanan k    +
  |   n = 0; ilişkili veri için KDF'ye    |
  |   bakın                               |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly çerçeve (seçenekler)     |
  +   Şifrelenmiş ve kimlik doğrulamalı   +
  -           32 bayt                    -
  +   Mesaj 2 için KDF'de tanımlanan k    +
  |   n = 0; ilişkili veri için KDF'ye    |
  |   bakın                               |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     şifrelenmemiş kimlik doğrulamalı  |
  +         dolgu (isteğe bağlı)          +
  |     seçenekler bloğunda tanımlanan    |
  ~              .   .   .                ~
  |     uzunluk                           |
  +----+----+----+----+----+----+----+----+

  Öncekinin aynısı, sadece ikinci bir ChaChaPoly çerçeve ekleyin

```

Şifre çözülmüş veri (Poly1305 otantifikasyon etiketi gösterilmemiştir):

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Şifreli Metni        |
  +      (aşağıdaki tabloya bakın)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |              Seçenekler               |
  +              (16 bayt)                +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     şifrelenmemiş kimlik doğrulamalı  |
  +         dolgu (isteğe bağlı)          +
  |     seçenekler bloğunda tanımlanan    |
  ~              .   .   .                ~
  |     uzunluk                           |
  +----+----+----+----+----+----+----+----+
```

Boyutlar:

```
| Tür | Tür Kodu | Y len | Mesaj 2 L | g  Mesaj 2 Şi | eli Long Mesa | 2 Şifre Çö | ü Long |
| --- | -------- | ----- | --------- | ------------- | ------------- | ---------- | ------ |
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1072 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1552 | 1568 | 16 |

```

Not: Tür kodları sadece dahili kullanım içindir. Yönlendiriciler tür 4 olarak kalacak,
ve destek yönlendirici adreslerinde belirtilecektir.

3) Oturum Doğrulandı
`````````````````

Değişmeden

Veri Aşaması için Anahtar Türetim Fonksiyonu (KDF)
``````````````````````````````````````````````

Değişmeden

### SSU2

SSU2 spesifikasyonunu [SSU2](https://geti2p.net/spec/ssu2) olarak güncelleyin:

Gürültü tanımlayıcıları
```````````````````

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

Uzun Başlık
````````````

Uzun başlık 32 bayttır. Oturum kurulmadan önce, Token İsteği, Oturum İsteği, Oturum Oluşturuldu ve Yeniden Dene için kullanılır.
Ayrıca oturum dışı Peer Test ve Hole Punch mesajları için de kullanılır.

TODO: Dahili olarak sürüm alanını kullanabiliriz ve MLKEM512 için 3 ve MLKEM768 için 4 kullanabiliriz.
Bunu sadece tür 0 ve 1 için mi, yoksa tüm 6 tür için mi yapıyoruz?

Başlık şifrelemesi öncesi:

```dataspec

+----+----+----+----+----+----+----+----+
  |      Hedef Bağlantı Kimliği           |
  +----+----+----+----+----+----+----+----+
  |   Paket Numarası   |tür| versiyon| id |bayrak|
  +----+----+----+----+----+----+----+----+
  |         Kaynak Bağlantı Kimliği       |
  +----+----+----+----+----+----+----+----+
  |                  Token                |
  +----+----+----+----+----+----+----+----+

  Hedef Bağlantı Kimliği :: 8 bayt, imzasız büyük endian tamsayı

  Paket Numarası :: 4 bayt, imzasız büyük endian tamsayı

  tür :: Mesaj türü = 0, 1, 7, 9, 10 veya 11

  versiyon :: Protokol versiyonu, 2'ye eşit
         TODO Dahili olarak sürüm alanını kullanabiliriz ve MLKEM512 için 3, MLKEM768 için 4 kullanabiliriz.

  id :: 1 bayt, ağ kimliği (şu anda 2, test ağları dışında)

  bayrak :: 1 bayt, kullanılmaz, ileride uyumluluk için 0 olarak ayarlanır

  Kaynak Bağlantı Kimliği :: 8 bayt, imzasız büyük endian tamsayı

  Token :: 8 bayt, imzasız büyük endian tamsayı

```

Kısa Başlık
````````

Değişmeden

Oturum İsteği (Tür 0)
``````````````````

Değişiklikler: Mevcut SSU2 yalnızca ChaCha bölümünde blok verilerini içerir.
ML-KEM ile ChaCha bölümü ayrıca şifreli PQ genel anahtarını içerecektir.

Ham içerik:

```dataspec
+----+----+----+----+----+----+----+----+
  |  Uzun Başlık bayt 0-15, ChaCha20 ile |
  +  Bob giriş anahtarı ile şifrelenmiş  +
  |    Başlık Şifreleme KDF'sine bakın   |
  +----+----+----+----+----+----+----+----+
  |  Uzun Başlık bayt 16-31, ChaCha20 ile|
  +  Bob giriş anahtarı n=0 ile          +
  |  şifrelenmiş                         |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 ile şifrelenmiş     +
  |       Bob giriş anahtarı n=0 ile      |
  +              (32 bayt)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 şifreli veri (MLKEM)       |
  +          (uzunluk değişir)            +
  |  Oturum İsteği KDF'sinde tanımlanan k |
  +  n = 0                                +
  |  ilişkili veri için KDF'ye bakın      |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 şifreli veri (yük)         |
  +          (uzunluk değişir)            +
  |  Oturum İsteği KDF'sinde tanımlanan k |
  +  n = 0                                +
  |  ilişkili veri için KDF'ye bakın      |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bayt)         +
  |                                       |
  +----+----+----+----+----+----+----+----+
```

Şifre çözülmüş veri (Poly1305 kimlik doğrulama etiketi gösterilmemiştir):

```dataspec
+----+----+----+----+----+----+----+----+
  |      Hedef Bağlantı Kimliği           |
  +----+----+----+----+----+----+----+----+
  |   Paket Numarası   |tür| versiyon| id |bayrak|
  +----+----+----+----+----+----+----+----+
  |         Kaynak Bağlantı Kimliği       |
  +----+----+----+----+----+----+----+----+
  |                  Token                |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bayt)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (aşağıdaki tabloya bakın)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Gürültü yükü (blok verisi)        |
  +          (uzunluk değişir)            +
  |     aşağıdaki izin verilen bloklara   |
  |     bakın                             |
  +----+----+----+----+----+----+----+----+
```

Boyutlar, IP yükü dahil değildir:

```
| Tür | Tür Kodu | X len | Mesaj 1 L | g  Mesaj 1 Şi | eli Long Mesa | 1 Şifre Çö | ü Long |
| --- | -------- | ----- | --------- | ------------- | ------------- | ---------- | ------ |
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | çok büyük |  |  |  |  |

```

Not: Tür kodları sadece dahili kullanım içindir. Yönlendiriciler tür 4 olarak kalacak,
ve destek yönlendirici adreslerinde belirtilecektir.

MLKEM768_X25519 için minimum MTU:
Yaklaşık 1316 IPv4 için ve 1336 IPv6 için.

Oturum Oluşturuldu (Tür 1)
`````````````````

Değişiklikler: Mevcut SSU2 yalnızca ChaCha bölümünde blok verilerini içerir.
ML-KEM ile, ChaCha bölümü ayrıca şifreli PQ genel anahtarını içerecektir.

Ham içerik:

```dataspec
+----+----+----+----+----+----+----+----+
  |  Uzun Başlık bayt 0-15, ChaCha20 ile |
  +  Bob giriş anahtarı ve               +
  | türetilmiş anahtar ile, bakın SU2    |
  +----+----+----+----+----+----+----+----+
  |  Uzun Başlık bayt 16-31, ChaCha20 ile|
  +  türetilmiş anahtar n=0 ile          +
  |                                      |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 ile şifrelenmiş     +
  |       türetilmiş anahtar n=0 ile      |
  +              (32 bayt)                +
  |       Başlık Şifreleme KDF'sine       +
  |       bakın                           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +   ChaCha20 verisi (MLKEM)             +
  +   Şifrelenmiş ve kimlik doğrulamalı   +
  |   veriler                            +
  +   uzunluk değişir                    +
  |  Oturum Oluşturuldu KDF'sinde         |
  |  tanımlanan k                         +
  |  n = 0; ilişkili veri için KDF'ye     |
  |  bakın                               +
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +   ChaCha20 verisi (yük)               +
  +   Şifrelenmiş ve kimlik doğrulamalı   +
  |   veriler                            +
  +  uzunluk değişir                     +
  |  Oturum Oluşturuldu KDF'sinde         |
  |  tanımlanan k                         +
  |  n = 0; ilişkili veri için KDF'ye     |
  |  bakın                               +
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bayt)          +
  |                                       |
  +----+----+----+----+----+----+----+----+
```

Şifre çözülmüş veri (Poly1305 kim
