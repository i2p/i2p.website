---
title: "Deneysel İmza Türleri için Floodfill Desteği"
number: "136"
author: "zzz"
created: "2017-03-31"
lastupdated: "2017-11-12"
status: "Açık"
thread: "http://zzz.i2p/topics/2279"
toc: true
---

## Genel Bakış

Deneysel aralıktaki imza türleri (65280-65534) için,
floodfills imzayı kontrol etmeden netdb depolamalarını kabul etmelidir.

Bu, yeni imza türlerinin test edilmesini destekleyecektir.


## Motive

GOST önerisi 134, daha önce kullanılmamış olan deneysel imza türü aralığı ile ilgili iki sorunu ortaya çıkardı.

Birincisi, deneysel aralıktaki imza türleri ayrılmaz olduğu için,
aynı anda birden fazla imza türü için kullanılabilirler.

İkincisi, deneysel bir imza türü ile bir yönlendirici bilgisi veya kira seti bir floodfill'de depolanmazsa,
yeni imza türünün tam olarak test edilmesi veya deneme amacıyla kullanılması zordur.


## Tasarım

Floodfills, imzayı kontrol etmeden,
deneysel aralıktaki imza türleri ile LS depolarını kabul etmeli ve yaymalıdır.
RI depoları için destek belirlenecek olup, daha fazla güvenlik etkisine sahip olabilir.


## Spesifikasyon


Deneysel aralıktaki imza türleri için, bir floodfill imzayı kontrol etmeden
netdb depolarını kabul edip yaymalıdır.

Deneysel olmayan yönlendiricilerin ve hedeflerin sahte olarak tanıtılmasını önlemek için,
bir floodfill asla farklı bir imza türü ile mevcut bir netdb girdisiyle hash çakışması olan
bir deneysel imza türü deposunu kabul etmemelidir.
Bu, önceki bir netdb girdisinin kaçırılmasını önler.

Ek olarak, bir floodfill, daha önce mevcut olmayan bir hash'in kaçırılmasını önlemek için,
hash çakışması olan deneysel olmayan bir imza türünün deposuyla bir deneysel netdb girdisini
üst yazmalıdır.

Floodfills, imzalama açık anahtar uzunluğunun 128 olduğunu varsaymalı veya daha uzunsa
anahtar sertifika uzunluğundan türetmelidir. Bazı uygulamalar, imza türü gayri resmi
olarak ayrılmadıkça daha uzun uzunlukları desteklemeyebilir.


## Göç

Bu özellik desteklendiğinde, bilinen bir yönlendirici sürümünde,
deneysel imza türü netdb girdileri bu sürüm veya daha yüksek bir floodfill'e depolanabilir.

Bazı yönlendirici uygulamaları bu özelliği desteklemiyorsa,
netdb deposu başarısız olacak, ancak bu, şu anki durumla aynıdır.


## Sorunlar

Daha fazla güvenlik etkisi olabilir, araştırılacak (öneri 137'yi bkz.)

Yukarıda açıklandığı gibi, bazı uygulamalar 128'den büyük anahtar uzunluklarını
desteklemeyebilir. Ek olarak, saldırganların hash çakışmaları oluşturma yeteneğini azaltmak için
maksimum 128'i zorlamak gerekebilir (diğer bir deyişle, anahtar sertifikasında fazla anahtar verisi yoktur).

Henüz resmi olarak önerilmeyen sıfır olmayan şifreleme türleriyle benzer
sorunların ele alınması gerekecektir.


## Notlar

Deneysel aralıkta olmayan bilinmeyen imza türlerinin netdb depoları,
imza doğrulanamayacağı için floodfills tarafından reddedilmeye devam edecektir.


