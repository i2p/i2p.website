---
title: "Tanıtıcı Süresi Dolma"
number: "133"
author: "zzz"
created: "2017-02-05"
lastupdated: "2017-08-09"
status: "Kapalı"
thread: "http://zzz.i2p/topics/2230"
target: "0.9.30"
implementedin: "0.9.30"
---

## Genel Bakış

Bu öneri, tanıtımların başarı oranını artırmakla ilgilidir.

## Motivasyon

Tanıtıcılar belli bir süre sonra geçerliliğini yitirir, ancak bu bilgi
RouterInfo içinde yayımlanmaz. Yönlendiriciler, bir tanıtıcının artık geçerli olmadığı zamanı şu anda tahmin etmek için sezgileri kullanmalıdır.

## Tasarım

Bir SSU RouterAddress'inde tanıtıcılar içeren yayımlayıcı, her bir tanıtıcı için isteğe bağlı olarak geçerlilik sürelerini ekleyebilir.

## Spesifikasyon

```
iexp{X}={nnnnnnnnnn}

X :: Tanıtıcı numarası (0-2)

nnnnnnnnnn :: Epok zamanından bu yana saniye (ms değil).
```

### Notlar
* Her bir geçerlilik süresi, RouterInfo yayın tarihinden daha sonra olmalı ve RouterInfo yayın tarihinden en fazla 6 saat sonra olmalıdır.

* Yayın yapan yönlendiriciler ve tanıtıcılar, tanıtıcının süresi dolana kadar geçerli kalmasını sağlamaya çalışmalıdır, ancak bunu garanti etmelerinin bir yolu yoktur.

* Yönlendiriciler, süresinin dolmasının ardından yayımlanan bir tanıtıcıyı kullanmamalıdır.

* Tanıtıcı süre sonları RouterAddress eşleminde yer alır.
  Bunlar, (şu anda kullanılmayan) RouterAddress içindeki 8 baytlık süre alanı değildir.

**Örnek:** `iexp0=1486309470`

## Geçiş

Sorun yok. Uygulama isteğe bağlıdır.
Eski yönlendiriciler bilinmeyen parametreleri göz ardı edeceklerinden geriye dönük uyum sağlanmıştır.
