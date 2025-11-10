---
title: "LeaseSet 2"
number: "110"
author: "zzz"
created: "2014-01-22"
lastupdated: "2016-04-04"
status: "Rejected"
thread: "http://zzz.i2p/topics/1560"
supercededby: "123"
---

## Genel Bakış

Bu öneri, daha yeni şifreleme türlerini destekleyen yeni bir LeaseSet formatı hakkındadır.


## Motivasyon

I2P tünelleri üzerinden kullanılan uçtan uca kriptografi, ayrı şifreleme ve imzalama anahtarlarına sahiptir. İmzalama anahtarları, daha yeni imza türlerini desteklemek için KeyCertificates ile zaten genişletilmiş olan tünel Hedefinde yer alır. Ancak, şifreleme anahtarları, herhangi bir Sertifika içermeyen LeaseSet'in bir parçasıdır. Bu nedenle, yeni bir LeaseSet formatı uygulamak ve bunu netDb'de saklama desteği eklemek gereklidir.

Iyi bir haber şu ki, LS2 uygulandığında, mevcut tüm Hedefler daha modern şifreleme türlerini kullanabilir; bir LS2'yi alabilen ve okuyabilen yönlendiriciler, onunla birlikte tanıtılan herhangi bir şifreleme türünü destekleme garantisine sahip olacaktır.


## Spesifikasyon

Temel LS2 formatı şöyle olacaktır:

- hedef
- yayımlanma zaman damgası (8 bayt)
- sona erme (8 bayt)
- alt tür (1 bayt) (normal, şifreli, meta veya hizmet)
- bayraklar (2 bayt)

- alt türüne özgü kısım:
  - normal için şifreleme türü, şifreleme anahtarı ve kiralar
  - şifreli için blob
  - hizmet için özellikler, karmalar, portlar, iptaller, vb.

- imza
