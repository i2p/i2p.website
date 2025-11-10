---
title: "2005-03-08 tarihli I2P Durum Notları"
date: 2005-03-08
author: "jr"
description: "0.5.0.2 sürümü iyileştirmeleri, ağ güvenilirliğine odak ve e-posta ile BitTorrent hizmetlerindeki güncellemeleri kapsayan haftalık I2P geliştirme durumu notları"
categories: ["status"]
---

Herkese selam, haftalık güncelleme zamanı

* Index

1) 0.5.0.2 2) mail.i2p güncellemeleri 3) i2p-bt güncellemeleri 4) ???

* 1) 0.5.0.2

Geçen gün 0.5.0.2 sürümünü yayımladık ve ağın hatırı sayılır bir kısmı güncelledi (yaşasın!). 0.5.0.1’deki en büyük sorunların giderildiğine dair raporlar geliyor ve genel olarak her şeyin düzgün çalışıyor gibi görünüyor. Yine de bazı güvenilirlik sorunları var, ama streaming lib (streaming kitaplığı) bununla başa çıkıyor (12–24+ saat süren irc bağlantıları artık norm gibi görünüyor). Kalan bazı sorunların izini sürmeye çalışıyorum, ancak herkesin mümkün olan en kısa sürede güncel hale gelmesi gerçekten, gerçekten iyi olur.

Bundan sonraki adımlar açısından, güvenilirlik her şeyden önce gelir. Başarılı olması gereken mesajların ezici çoğunluğu gerçekten başarılı olduktan sonra ancak throughput (aktarım verimi) iyileştirilmeye yönelik çalışmalar yapılacaktır. Toplu işleme yapan tunnel ön işleyicisinin ötesinde, keşfetmek isteyebileceğimiz bir diğer boyut da profillere daha fazla gecikme verisi aktarmaktır. Halihazırda her bir eşin "hız" derecelendirmesini belirlemek için yalnızca test ve tunnel yönetim mesajlarını kullanıyoruz, ancak netDb ve hatta uçtan uca istemci mesajları gibi diğer işlemler için ölçülebilir herhangi bir RTT (gidiş-dönüş süresi) değerini de toplamamız gerekir. Öte yandan, bunlara uygun şekilde ağırlık vermemiz gerekecek; çünkü uçtan uca bir mesajda, ölçülebilir RTT’nin dört bileşenini (bizim giden, onların gelen, onların giden, bizim gelen) birbirinden ayıramayız. Belki de bazı giden mesajlarla birlikte bizim gelen tunnel’larımızdan birini hedefleyen bir mesajı paketlemek için biraz garlic kurnazlığı yapabiliriz; böylece karşı tarafın tunnel’larını ölçüm döngüsünün dışında bırakmış oluruz.

* 2) mail.i2p updates

Tamam, postman'ın bizim için ne gibi güncellemeler hazırladığını bilmiyorum, ama toplantı sırasında bir güncelleme olacak. Öğrenmek için günlükleri inceleyin!

* 3) i2p-bt update

duck & gang'in bizim için ne gibi güncellemeleri olduğunu bilmiyorum, ama kanalda ilerleme olduğuna dair bazı konuşmalar duydum. Belki ondan bir güncelleme koparabiliriz.

* 4) ???

Bir sürü şey oluyor, ama gündeme getirip tartışmak istediğiniz özel bir konu varsa, birkaç dakika içinde toplantıya uğrayın. Bu arada, küçük bir hatırlatma: Henüz güncellemediyseniz, lütfen bunu en kısa sürede yapın (güncellemek inanılmaz derecede basit - bir dosya indirin, bir düğmeye tıklayın)

=jr
