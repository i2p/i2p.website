---
title: "Çok Uyumlu İçin Meta-LeaseSet"
number: "120"
author: "zzz"
created: "2016-01-09"
lastupdated: "2016-01-11"
status: "Reddedildi"
thread: "http://zzz.i2p/topics/2045"
supercededby: "123"
---

## Genel Bakış

Bu öneri, I2P'de büyük sitelere kadar ölçeklenebilecek uygun çoklu uyum desteğini uygulamakla ilgilidir.


## Motivasyon

Çoklu uyum bir hile ve muhtemelen büyük ölçeklerde örneğin facebook.i2p için çalışmayacaktır.
Diyelim ki her biri 16 tünel olan 100 çoklu uyum var, bu her 10 dakikada bir 1600 LS yayını ya da neredeyse saniyede 3 demektir. Taşkın dolgu alanları bu yükün altında kalır ve kısıtlamalar devreye girer. Ve bu, bakış trafikinden bile bahsetmeden önce.

LS'leri listeleyen 100 gerçek LS karmasını listeleyen bir tür meta-LS'e ihtiyacımız var. Bu, 10 dakikadan çok daha uzun bir süre boyunca kalıcı olacaktır. Yani, LS için iki aşamalı bir arama olacaktır, ancak ilk aşama saatlerce önbelleğe alınabilir.


## Tanım

Meta-LeaseSet şu formatta olacaktır::

  - Hedef
  - Yayınlanma Zaman Damgası
  - Süre Dolma
  - Bayraklar
  - Özellikler
  - Giriş sayısı
  - İptal sayısı

  - Girişler. Her giriş şunları içerir:
    - Karma
    - Bayraklar
    - Süre Dolma
    - Maliyet (öncelik)
    - Özellikler

  - İptaller. Her iptal şunları içerir:
    - Karma
    - Bayraklar
    - Süre Dolma

  - İmza

Maksimum esneklik için bayraklar ve özellikler dahil edilmiştir.


## Yorumlar

Bu daha sonra, herhangi bir türde bir hizmet sorgulaması olarak genelleştirilebilir. Hizmet tanımlayıcısı bir SHA256 karmasıdır.

Daha da büyük bir ölçeklenebilirlik için birden çok seviye olabilir, yani bir meta-LS başka meta-LS'lere işaret edebilir.
