---
title: "Hizmet Dizini"
number: "102"
author: "zzz"
created: "2009-01-01"
lastupdated: "2009-01-06"
status: "Reddedildi"
thread: "http://zzz.i2p/topics/180"
supercededby: "122"
---

## Genel Bakış

Bu öneri, uygulamaların bir dizinde hizmetleri kaydedip aramak için kullanabileceği bir protokole yöneliktir.


## Motivasyon

Onioncat'ı desteklemenin en doğrudan yolu bir hizmet dizini ile yapmaktır.

Bu, Sponge'un bir süre önce IRC'de sahip olduğu bir öneriye benziyor. Onu yazıya dökmüş olduğunu sanmıyorum, ama fikri bunu netDb'ye koymaktı. Bunun lehinde değilim, ama dizine erişmenin en iyi yönteminin ne olacağı tartışmasını (netDb aramaları, DNS-over-i2p, HTTP, hosts.txt, vb.) başka bir güne bırakacağım.

Bunu HTTP ve ekleme formu için kullandığım perl betikleri koleksiyonunu kullanarak oldukça hızlı bir şekilde uydurabilirim.


## Teknik Özellikler

Bir uygulamanın dizinle nasıl arayüz oluşturacağı:

KAYIT
  - DestKey
  - Protokol/Hizmet çiftleri listesi:

    - Protokol (isteğe bağlı, varsayılan: HTTP)
    - Hizmet (isteğe bağlı, varsayılan: web sitesi)
    - Kimlik (isteğe bağlı, varsayılan: yok)

  - Hostname (isteğe bağlı)
  - Süre sonu (varsayılan: 1 gün? silme için 0)
  - Sig (özel anahtarla imza)

  Döndürür: başarı veya başarısızlık

  Güncellemeye izin verilir

ARAMA
  - Karma veya anahtar (isteğe bağlı). BİRİ:

    - 80-bit kısmi karma
    - 256-bit tam karma
    - tam destkey

  - Protokol/hizmet çifti (isteğe bağlı)

  Döndürür: başarı, başarısızlık veya (80-bit için) çakışma.
  Başarılıysa, yukarıda imzalı tanımlayıcıyı döndürür.
