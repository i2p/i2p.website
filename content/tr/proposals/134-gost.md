---
title: "GOST Sig Tipi"
number: "134"
author: "orignal"
created: "2017-02-18"
lastupdated: "2017-03-31"
status: "Open"
thread: "http://zzz.i2p/topics/2239"
---

## Genel Bakış

GOST R 34.10 eliptik eğri imzası Rusya'daki resmi yetkililer ve işletmeler tarafından kullanılmaktadır.
Bu imzanın desteklenmesi, mevcut uygulamaların entegrasyonunu (genellikle CryptoPro tabanlı) kolaylaştırabilir.
Hash fonksiyonu 32 veya 64 bayt olan GOST R 34.11'dir.
Temel olarak EcDSA ile aynı şekilde çalışır, imza ve genel anahtar boyutu 64 veya 128 bayttır.

## Motivasyon

Eliptik eğri kriptografisi asla tam olarak güvenilmemiştir ve olası arka kapılar hakkında birçok spekülasyon üretmiştir. 
Bu nedenle, herkes tarafından güvenilen nihai bir imza türü yoktur.
Bir imza türü daha eklenmesi, insanların daha fazla güven duydukları şeyi seçmelerine olanak tanır.

## Tasarım

GOST R 34.10, kendi parametre setleriyle standart eliptik eğri kullanır.
Mevcut grupların matematiği tekrar kullanılabilir.
Ancak, imzalama ve doğrulama farklıdır ve uygulanması gerekir.
RFC'ye bakınız: https://www.rfc-editor.org/rfc/rfc7091.txt
GOST R 34.10, GOST R 34.11 hash ile birlikte çalışacak şekilde tasarlanmıştır.
256 veya 512 bit olan GOST R 34.10-2012'yi (aka steebog) kullanacağız.
RFC'ye bakınız: https://tools.ietf.org/html/rfc6986

GOST R 34.10 parametreleri belirtmez ancak herkes tarafından kullanılan bazı iyi parametre setleri vardır.
64 bayt genel anahtarlara sahip GOST R 34.10-2012, GOST R 34.10-2001'den CryptoPro'nun parametre setlerini devralır.
RFC'ye bakınız: https://tools.ietf.org/html/rfc4357

Ancak 128 baytlık anahtarlar için daha yeni parametre setleri, özel bir teknik komite olan tc26 (tc26.ru) tarafından oluşturulmuştur.
RFC'ye bakınız: https://www.rfc-editor.org/rfc/rfc7836.txt

I2pd'deki openssl tabanlı uygulama P256'dan daha hızlı ve 25519'dan daha yavaş olduğunu göstermektedir.

## Spesifikasyon

Sadece GOST R 34.10-2012 ve GOST R 34.11-2012 desteklenmektedir.
İki yeni imza türü:
9 - GOSTR3410_GOSTR3411_256_CRYPTO_PRO_A, 64 baytlık genel anahtar ve imza türü, 32 baytlık hash boyutu ve CryptoProA (aka CryptoProXchA) parametre seti için kullanılır.
10 - GOSTR3410_GOSTR3411_512_TC26_A, 128 baytlık genel anahtar ve imza türü, 64 baytlık hash boyutu ve TC26'dan A parametre seti için kullanılır.

## Geçiş

Bu imza türlerinin sadece isteğe bağlı imza türü olarak kullanılması planlanmaktadır.
Göç gerekmez. i2pd bunu zaten desteklemektedir.
