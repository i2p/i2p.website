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

Bu öneri, tanıtımların başarı oranını artırmakla ilgilidir. Bkz.
[TRAC-TICKET]_.

## Motivasyon

Tanıtıcılar belli bir süre sonra geçerliliğini yitirir, ancak bu bilgi
[RouterInfo]_ içinde yayımlanmaz. Yönlendiriciler, bir tanıtıcının artık geçerli olmadığı zamanı şu anda tahmin etmek için sezgileri kullanmalıdır.

## Tasarım

Bir SSU [RouterAddress]_'inde tanıtıcılar içeren yayımlayıcı, her bir tanıtıcı için isteğe bağlı olarak geçerlilik sürelerini ekleyebilir.

## Spesifikasyon

.. raw:: html

  {% highlight lang='dataspec' %}
iexp{X}={nnnnnnnnnn}

  X :: Tanıtıcı numarası (0-2)

  nnnnnnnnnn :: Epok zamanından bu yana saniye (ms değil).
{% endhighlight %}

Notlar
`````
* Her bir geçerlilik süresi, [RouterInfo]_ yayın tarihinden daha sonra olmalı ve RouterInfo yayın tarihinden en fazla 6 saat sonra olmalıdır.

* Yayın yapan yönlendiriciler ve tanıtıcılar, tanıtıcının süresi dolana kadar geçerli kalmasını sağlamaya çalışmalıdır, ancak bunu garanti etmelerinin bir yolu yoktur.

* Yönlendiriciler, süresinin dolmasının ardından yayımlanan bir tanıtıcıyı kullanmamalıdır.

* Tanıtıcı süre sonları [RouterAddress]_ eşleminde yer alır.
  Bunlar, (şu anda kullanılmayan) [RouterAddress]_ içindeki 8 baytlık süre alanı değildir.

Örnek: ``iexp0=1486309470``

## Geçiş

Sorun yok. Uygulama isteğe bağlıdır.
Eski yönlendiriciler bilinmeyen parametreleri göz ardı edeceklerinden geriye dönük uyum sağlanmıştır.

## Referanslar

.. [RouterAddress]
    {{ ctags_url('RouterAddress') }}

.. [RouterInfo]
    {{ ctags_url('RouterInfo') }}

.. [TRAC-TICKET]
    http://{{ i2pconv('trac.i2p2.i2p') }}/ticket/1352
