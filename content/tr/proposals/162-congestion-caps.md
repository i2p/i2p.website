---
title: "Tıkanıklık Sınırları"
number: "162"
author: "dr|z3d, idk, orijinal, zzz"
created: "2023-01-24"
lastupdated: "2023-02-01"
status: "Açık"
thread: "http://zzz.i2p/topics/3516"
target: "0.9.59"
toc: true
---

## Genel Bakış

Yayınlanan Yönlendirici Bilgisine (RI) tıkanıklık göstergeleri ekleyin.




## Motivasyon

Bant genişliği "sınırları" (yetkinlikler) paylaşım bant genişliği limitlerini ve erişilebilirliği belirtir, ancak tıkanıklık durumunu belirtmez.
Bir tıkanıklık göstergesi, yönlendiricilerin tıkanmış bir yönlendirici üzerinden tünel inşa etme girişiminde bulunmaktan kaçınmalarına yardımcı olur,
bu da daha fazla tıkanıklık ve azalan tünel inşa başarısına katkı sağlar.



## Tasarım

Farklı tıkanıklık seviyelerini veya kapasite sorunlarını belirtmek için yeni sınırlar tanımlayın.
Bunlar, üst düzey RI sınırlarında olacak, adres sınırlarında değil.


### Tıkanıklık Tanımı

Genel olarak tıkanıklık, eşin
bir tünel inşa isteğini alması ve kabul etmesi olası olmadığını ifade eder.
Tıkanıklık seviyelerini tanımlamak veya sınıflandırmak uygulamaya özeldir.

Uygulamalar aşağıdakilerden bir veya daha fazlasını dikkate alabilir:

- Bant genişliği sınırlarında veya yakınında
- Maksimum katılımcı tünellerde veya yakınında
- Bir veya daha fazla taşıma aracında maksimum bağlantılarda veya yakınında
- Kuyruk derinliği, gecikme veya CPU kullanımı eşiği üzerinde; dahili kuyruk taşması
- Temel platform / İşletim Sistemi CPU ve bellek yetenekleri
- Algılanan ağ tıkanıklığı
- Güvenlik duvarı veya simetrik NAT veya gizli veya proxylenmiş gibi ağ durumu
- Tünelleri kabul etmeyecek şekilde yapılandırılmış

Tıkanıklık durumu, birkaç dakika boyunca koşulların ortalamasına dayanmalıdır, anlık ölçüm değil.



## Spesifikasyon

[NETDB](/docs/how/network-database/)'yi aşağıdaki gibi güncelleyin:


```text
D: Orta düzeyde tıkanıklık veya düşük performanslı bir yönlendirici (örneğin Android, Raspberry Pi)
     Diğer yönlendiriciler bu yönlendiricinin
     görünen tünel kapasitesini profilinde düşürmeli veya sınırlamalıdır.

  E: Yüksek tıkanıklık, bu yönlendirici bir sınırda veya sınırda,
     ve çoğu tünel taleplerini reddediyor veya düşürüyor.
     Bu RI son 15 dakika içinde yayınlandıysa, diğer yönlendiriciler
     bu yönlendiricinin kapasitesini ciddi şekilde düşürmeli veya sınırlamalıdır.
     Bu RI 15 dakikadan daha eskiyse, 'D' olarak işlem yapılmalıdır.

  G: Bu yönlendirici geçici veya kalıcı olarak tüm tünelleri reddediyor.
     Bu yönlendirici üzerinden tünel inşa etmeye çalışmayın,
     yeni bir RI 'G'siz alınana kadar.
```

Tutarlılık için, uygulamalar herhangi bir tıkanıklık sınırını
sonunda (R veya U'dan sonra) eklemelidir.



## Güvenlik Analizi

Yayınlanmış herhangi bir eş bilgisine güvenilemez.
Sınırlar, Yönlendirici Bilgisindeki diğer her şey gibi, taklit edilebilir.
Yönlendiricinin algılanan kapasitesini yükseltmek için Yönlendirici Bilgisindeki hiçbir şeyi kullanmayız.

Tıkanıklık göstergeleri yayınlamak ve eşlere bu yönlendiriciden kaçınmalarını söylemek,
daha fazla tünel talep eden kapsüllerden veya kapasite göstergelerinden doğal olarak
daha güvenlidir.

Mevcut bant genişliği kapasitesi göstergeleri (L-P, X) yalnızca
çok düşük bant genişliği yönlendiricilerinden kaçınmak için güvenilmektedir. "U" (erişilemez) sınırı benzer bir etkiye sahiptir.

Yayınlanan herhangi bir tıkanıklık göstergesi, bir tünel inşa talebini
reddetme veya düşürmeye benzer bir etkiye sahip olmalıdır, benzer güvenlik özellikleri ile.



## Notlar

Eşler 'D' yönlendiricilerinden tamamen kaçınmamalı, sadece derecelerini düşürmelidir.

Bütün ağ tıkanıklık içindeyken ve 'E' yayınlarken, durumun tamamen kırılmaması için
'E' yönlendiricilerden tamamen kaçınmamaya dikkat edilmelidir.

Yönlendiriciler 'D' ve 'E' yönlendiriciler üzerinden
hangi tip tünellerin inşa edileceği konusunda farklı stratejiler kullanabilir,
örneğin keşif ve istemci veya yüksek ve düşük bant genişliği istemci tünelleri.

Yönlendiriciler muhtemelen başlangıçta veya kapatmada
tıkanıklık sınırını varsayılan olarak yayınlamamalıdır,
ağ durumları bilinmiyorsa bile, eşler tarafından yeniden başlatma tespiti önlemek için.




## Uyumluluk

Hiçbir sorun yok, tüm uygulamalar bilinmeyen sınırları yok sayar.


## Geçiş

Uygulamalar herhangi bir zamanda destek ekleyebilir, koordinasyon gerekmez.

Ön plan:
Sınırlar 0.9.58'de yayınlanacak (Nisan 2023);
yayımlanan sınırlar üzerinde 0.9.59'da (Temmuz 2023) işlem yapılacak.



## Referanslar

* [NETDB](/docs/how/network-database/)
