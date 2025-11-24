---
title: "1-of-N veya N-of-N Tünellere OBEP Teslimatı"
number: "125"
author: "zzz, str4d"
created: "2016-03-10"
lastupdated: "2017-04-07"
status: "Open"
thread: "http://zzz.i2p/topics/2099"
---

## Genel Bakış

Bu öneri, ağ performansını artırmak için iki iyileştirmeyi kapsar:

- OBEP'ye tek bir seçenek yerine alternatif listesi sunarak IBGW seçimini devretmek.

- OBEP'de çoklu yayın paket yönlendirmeyi etkinleştirmek.


## Motivasyon

Doğrudan bağlantı durumunda, OBEP'ye IBGW'lere nasıl bağlanacağı konusunda esneklik vererek, bağlantı sıkışıklığını azaltmayı amaçlıyoruz. Birden fazla tünel belirtebilme yeteneği, mesajı belirtilen tüm tünellere ileterek OBEP'de çoklu yayını da uygulamamıza olanak tanır.

Bu önerinin delege etme kısmına alternatif olarak, mevcut hedef [RouterIdentity](http://localhost:63465/en/docs/specs/common-structures/#common-structure-specification) karmasını belirtme yeteneğine benzer şekilde, bir [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset) karması gönderilebilir. Bu, daha küçük bir mesaj ve potansiyel olarak daha yeni bir LeaseSet ile sonuçlanacaktır. Ancak:

1. OBEP'yi bir arama yapmaya zorlar.

2. LeaseSet bir floodfill'e yayımlanmamış olabilir, bu yüzden arama başarısız olur.

3. LeaseSet şifrelenmiş olabilir, bu yüzden OBEP kiraları alamaz.

4. Bir LeaseSet belirtmek, mesajın hedef [Destination]'ını OBEP'ye ifşa eder ki bu, ancak ağdaki tüm LeaseSet'leri tarayarak ve bir Lease eşleşmesi arayarak keşfedebilirler.


## Tasarım

Başlatıcı (OBGW), hedef [Leases](http://localhost:63465/en/docs/specs/common-structures/#lease)'lerden bazılarını (tümünü?) teslimat talimatlarına [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions) yerleştirir, sadece bir tane seçmek yerine.

OBEP bunlardan birine teslim etmek için seçecektir. OBEP mevcutsa, zaten bağlı olduğu veya bildiği birini seçecektir. Bu, OBEP-IBGW yolunu daha hızlı ve güvenilir hale getirecek ve toplam ağ bağlantılarını azaltacaktır.

Kullanılmayan bir teslimat türümüz (0x03) ve [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions) bayraklarında iki kalan bitimiz (0 ve 1) var, bu özellikleri uygulamak için bunları kullanabiliriz.


## Güvenlik Etkileri

Bu öneri, OBGW'nin hedef Destination'ı veya NetDB'ye bakış açısı hakkındaki bilgi miktarını değiştirmez:

- OBEP'yi kontrol eden ve NetDB'den LeaseSet'leri kazıyan bir saldırgan, bir mesajın belirli bir Destination'a gönderilip gönderilmediğini, [TunnelId](http://localhost:63465/en/docs/specs/common-structures/#tunnelid) / [RouterIdentity](http://localhost:63465/en/docs/specs/common-structures/#common-structure-specification) çiftini arayarak zaten belirleyebilir. En kötü ihtimalle, TMDI'deki birden fazla Lease varlığı, saldırganın veritabanında bir eşleşme bulma hızını artırabilir.

- Kötü niyetli bir Destination işleten bir saldırgan, zaten farklı floodfill'lere farklı gelen tüneller içeren LeaseSet'ler yayımlayarak ve OBGW'nin hangi tüneller aracılığıyla bağlandığını gözlemleyerek, bağlanan bir kurbanın NetDB'ye bakış açısı hakkında bilgi edinebilir. Onların bakış açısından, OBEP hangi tüneli kullanacağını seçmesi, OBGW'nin seçimi yapmasına işlevsel olarak identiktir.

Çoklu yayın bayrağı, OBGW'nin OBEP'lere çoklu yayın yaptığını ifşa eder. Bu, daha yüksek seviyeli protokolleri uygularken göz önünde bulundurulması gereken bir performans ve gizlilik değiş tokuşu yaratır. Opsiyonel bir bayrak olduğundan, kullanıcılar uygulamaları için uygun kararı verebilirler. Ancak, uyumlu uygulamalar için bu davranışın varsayılan olması geniş bir kullanım yelpazesi sağlar çünkü bu belirli bir mesajın hangi uygulamadan kaynaklandığı hakkında bilgi sızmasını azaltır.


## Spesifikasyon

İlk Parça Teslimat Talimatları [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions) şu şekilde değiştirilecektir:

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +----+----+----+
|                        |dly | Mesaj  
+----+----+----+----+----+----+----+----+
 ID (opt) |genişletilmiş seçenekler(opt)|cnt | (o)
+----+----+----+----+----+----+----+----+
 Tünel ID N   |                        |
+----+----+----+                        +
|                                       |
+                                       +
|         To Hash N (optional)          |
+                                       +
|                                       |
+              +----+----+----+----+----+
|              | Tünel ID N+1 (o) |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|         To Hash N+1 (optional)        |
+                                       +
|                                       |
+                                  +----+
|                                  | sz
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 bayt
       Bit sırası: 76543210
       bitler 6-5: teslimat türü
                 0x03 = TÜNELLER
       bit 0: çoklu yayın? Eğer 0 ise, tünellerden birine teslim et
                         Eğer 1 ise, tüm tünellere teslim et
                         Teslimat türü TÜNELLER değilse gelecekteki kullanımlar ile uyumluluk için 0'a ayarla

Count ::
       1 bayt
       Opsiyonel, teslimat türü TÜNELLER ise mevcut
       2-255 - Takip edilecek id/hash çiftlerinin sayısı

Tunnel ID :: `TunnelId`
To Hash ::
       36 bayt her biri
       Opsiyonel, teslimat türü TÜNELLER ise mevcut
       id/hash çiftleri

Toplam uzunluk: Tipik uzunluk:
       75 bayt sayı 2 TÜNELLER teslimatı için (parçalanmamış tünel mesajı);
       79 bayt sayı 2 TÜNELLER teslimatı için (ilk parça)

Teslimat talimatlarının geri kalanı değiştirilmemiştir
```


## Uyumluluk

Yeni spesifikasyonu anlaması gereken tek eşler OBGW'ler ve OBEP'lerdir. Dolayısıyla, bu değişikliği hedef I2P sürümü [VERSIONS](/en/docs/specs/i2np/#protocol-versions) üzerinden mevcut ağ ile uyumlu hale getirebiliriz:

* OBGW'ler, outbound tünelleri oluştururken advertised I2P sürümüne göre uyumlu OBEP'leri seçmeli.

* Hedef sürümü ilan eden eşler, yeni bayrakları çözmeyi desteklemeli ve talimatları geçersiz olarak reddetmemelidir.

