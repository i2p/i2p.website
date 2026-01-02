---
title: "Tünel Yapı Mesajı Seçenekleri"
number: "143"
author: "zzz"
created: "2018-01-14"
lastupdated: "2022-01-28"
status: "Reddedildi"
thread: "http://zzz.i2p/topics/2500"
toc: true
---

## Not

Bu öneri belirtildiği şekilde uygulanmamıştır,
ancak ECIES uzun ve kısa yapı mesajları (öneriler 152 ve 157)
genişletilebilir seçenekler alanı ile tasarlanmıştır.
Resmi spesifikasyon için [Tunnel Creation ECIES spesifikasyonuna](/docs/specs/implementation/#tunnel-creation-ecies) bakınız.


## Genel Bakış

Tünel Yapı ve Tünel Yapı Yanıt mesajlarında bulunan I2NP Tünel Yapı Kayıtları için esnek, genişletilebilir bir seçenek mekanizması ekleyin.


## Motivasyon

Tünel Yapı Mesajında seçenekler veya yapılandırma ayarlamak için gelen birkaç geçici, belgelenmemiş öneri var,
böylece tünelin yaratıcısı her tünel aşamasına bazı parametreler gönderebilir.

TBM'de 29 boş bayt var. Gelecekteki iyileştirmeler için esneklik sağlamalıyız, ancak aynı zamanda alanı akıllıca kullanmalıyız.
'Mapping' yapısını kullanmak her seçenek için en az 6 bayt kullanır ("1a=1b;").
Daha fazla seçenek alanını katı bir şekilde tanımlamak daha sonra sorunlara yol açabilir.

Bu belge, yeni, esnek bir seçenek haritalama şeması önerir.


## Tasarım

29 bayta birden fazla, farklı uzunlukta seçenek sığdırabilmemiz için kompakt ve esnek bir seçenek temsil sistemine ihtiyacımız var.
Bu seçenekler henüz tanımlanmamıştır ve şu anda tanımlanmaları gerekmez.
"Mapping" yapısını kullanmayın (Java Properties nesnesi kodlayan), bu çok israf edici.
Her bir seçenek ve uzunluğu belirtmek için bir sayı kullanın, bu da kompakt ve esnek bir kodlamaya neden olur.
Seçenekler, numara ile belirlenen spesifikasyonlarımıza göre kaydedilmelidir, ancak deneysel seçenekler için bir aralık da ayıracağız.


## Spesifikasyon

Ön hazırlık - aşağıda birkaç alternatif tanımlanmıştır.

Bu, bayraklardaki (bayt 184) 5. bit 1 olarak ayarlanmışsa mevcut olurdu.

Her seçenek, iki baytlık bir seçenek numarası ve uzunluğu, ardından uzunluk baytı kadar seçenek değeridir.

Seçenekler bayt 193'ten başlar ve en fazla son bayta 221'e kadar devam eder.

Seçenek numarası/uzunluğu:

İki bayt. Bitler 15-4, 12-bit seçenek numarası, 1 - 4095.
Bitler 3-0, takip edilecek seçenek değer baytlarının sayısı, 0 - 15.
Bir boolean seçeneği sıfır değer baytlarına sahip olabilir.
Özelliklerimizde bir seçenek numaraları kaydı tutacağız ve ayrıca deneysel seçenekler için bir aralık tanımlayacağız.

Seçenek değeri 0 ile 15 bayt arasında, o seçeneğe ihtiyaç duyan tarafından yorumlanacak.
Bilinmeyen seçenek numaraları göz ardı edilmelidir.

Seçenekler, iki 0 baytından oluşan 0/0 seçeneği numarası/uzunluğu ile tamamlanır.
Geri kalan 29 bayt, varsa, her zamanki gibi rastgele dolgu ile doldurulmalıdır.

Bu kodlama, bize 14 0-baytlık seçenek, ya da 9 1-baytlık seçenek ya da 7 2-baytlık seçenek için alan verir.
Bir alternatif, seçenek numarası/uzunluğu için yalnızca bir bayt kullanmak olurdu,
belki 5 bit seçenek numarası (maksimum 32) ve 3 bit uzunluğu (maksimum 7).
Bu, 28 0-baytlık seçenek, 14 1-baytlık seçenek veya 9 iki-baytlık seçenek kapasitesini artırır.
Ayrıca, değişken yapabiliriz, burada 31 seçenek numaralı 5-bit daha fazla bit okumayı gerektirir seçenek numarası olarak gösterilebilir.

Tünel aşaması yaratıcısına seçenekler geri döndürmek zorundaysa, tünel yapı yanıt mesajında
aynı formatı 'magic number' ön ekli birkaç bayt ile kullanabiliriz (çünkü seçeneklerin mevcut olduğunu gösteren tanımlı bir bayrak baytına sahip değiliz).
TBRM'de 495 boş bayt var.


## Notlar

Bu değişiklikler Tünel Yapı Kayıtlarına yöneliktir ve bu nedenle tüm Yapı Mesajı çeşitlerinde kullanılabilir -
Tünel Yapı İsteği, Değişken Tünel Yapı İsteği, Tünel Yapı Yanıtı ve Değişken Tünel Yapı Yanıtı.


## Geçiş

Tünel Yapı Kayıtlarındaki boş alan rastgele veri ile doldurulur ve şu anda göz ardı edilir.
Alan, geçiş sorunları olmadan seçenekler içerecek şekilde dönüştürülebilir.
Yapı mesajında, seçeneklerin varlığı bayrak baytında belirtilmiştir.
Yapı yanıt mesajında, seçeneklerin varlığı çok baytlı bir magic number ile belirtilmiştir.
