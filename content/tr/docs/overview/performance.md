---
title: "Performans"
description: "I2P ağ performansı: hız, bağlantılar ve kaynak yönetimi"
slug: "performance"
aliases:
  - "/tr/about/performance/future"
  - "/tr/about/performance/future/"
  - "/tr/about/performance/history"
  - "/tr/about/performance/history/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## I2P Ağ Performansı: Hız, Bağlantılar ve Kaynak Yönetimi

I2P ağı tamamen dinamiktir. Her istemci diğer düğümler tarafından bilinir ve yerel olarak bilinen düğümleri erişilebilirlik ve kapasite açısından test eder. Yalnızca erişilebilir ve yeterli kapasiteye sahip düğümler yerel NetDB'ye kaydedilir. Tunnel oluşturma süreci sırasında, tunnel'ları oluşturmak için bu havuzdan en iyi kaynaklar seçilir. Test etme süreci sürekli gerçekleştiği için, düğüm havuzu değişir. Her I2P düğümü NetDB'nin farklı bir bölümünü bilir, bu da her router'ın tunnel'lar için kullanılacak farklı bir I2P düğüm setine sahip olduğu anlamına gelir. İki router aynı bilinen düğüm alt kümesine sahip olsa bile, erişilebilirlik ve kapasite testleri muhtemelen farklı sonuçlar gösterecektir, çünkü diğer router'lar bir router test ederken yük altında olabilir, ancak ikinci router test ettiğinde serbest olabilir.

Bu, her I2P düğümünün tunnel oluşturmak için farklı düğümlere sahip olmasının nedenini açıklar. Her I2P düğümünün farklı gecikme süresi ve bant genişliği olduğu için, tunnel'lar (bu düğümler aracılığıyla oluşturulan) farklı gecikme süresi ve bant genişliği değerlerine sahiptir. Ve her I2P düğümünün farklı tunnel'ları oluşturulduğu için, hiçbir iki I2P düğümü aynı tunnel kümelerine sahip değildir.

Bir sunucu/istemci "destination" (hedef) olarak bilinir ve her destination en az bir gelen ve bir giden tunnel'a sahiptir. Varsayılan ayar tunnel başına 3 hop'tur. Bu, tam bir gidiş-dönüş istemci-sunucu-istemci bağlantısı için toplam 12 hop (yani 12 farklı I2P düğümü) yapar.

Her veri paketi sunucuya ulaşana kadar 6 başka I2P node'undan geçerek gönderilir:

```
client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - server
```
ve geri dönüş yolunda 6 farklı I2P düğümü:

```
server - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - client
```
Ağdaki trafik, yeni veri gönderilmeden önce bir ACK bekler, sunucudan bir ACK dönene kadar beklemesi gerekir: veri gönder, ACK bekle, daha fazla veri gönder, ACK bekle. RTT (RoundTripTime - gidiş-dönüş süresi) her bir I2P düğümünün ve bu gidiş-dönüşteki her bağlantının gecikmesinden oluştuğu için, bir ACK'in istemciye geri dönmesi genellikle 1-3 saniye sürer. TCP ve I2P taşıma tasarımı nedeniyle, bir veri paketinin sınırlı bir boyutu vardır. Bu koşullar birlikte tunnel başına maksimum bant genişliğini 20-50 kbyte/saniye ile sınırlar. Ancak, tunnel'daki YALNIZCA BİR hop'un harcayabileceği bant genişliği sadece 5 kb/saniye ise, gecikme ve diğer sınırlamalardan bağımsız olarak tüm tunnel 5 kb/saniye ile sınırlıdır.

Şifreleme, gecikme süresi ve bir tunnel'ın nasıl inşa edildiği, tunnel oluşturmayı CPU zamanı açısından oldukça pahalı hale getirir. Bu nedenle bir hedefin veri taşımak için maksimum 6 IN ve 6 OUT tunnel'a sahip olmasına izin verilir. Tunnel başına maksimum 50 kb/sn ile, bir hedef kabaca 300 kb/sn kombinasyon trafik kullanabilir (gerçekte düşük veya hiç anonimlik olmadan daha kısa tunnel'lar kullanılırsa daha fazla olabilir). Kullanılan tunnel'lar her 10 dakikada bir atılır ve yenileri inşa edilir. Bu tunnel değişimi ve bazen kapanan veya ağ bağlantısını kaybeden istemciler tunnel'ları ve bağlantıları bozabilir. Bunun bir örneği IRC2P Ağında bağlantı kaybında (ping timeout) veya eepget kullanırken görülebilir.

Sınırlı bir hedef kümesi ve hedef başına sınırlı tunnel kümesi ile, bir I2P düğümü diğer I2P düğümleri arasında yalnızca sınırlı bir tunnel kümesi kullanır. Örneğin, yukarıdaki küçük örnekte bir I2P düğümü "hop1" ise, istemciden kaynaklanan yalnızca 1 katılımcı tunnel görürüz. Tüm I2P ağını toplarsak, sınırlı miktarda bant genişliği ile birlikte yalnızca oldukça sınırlı sayıda katılımcı tunnel oluşturulabilir. Bu sınırlı sayıları I2P düğümlerinin sayısına dağıtırsak, kullanım için mevcut bant genişliği/kapasitenin yalnızca bir kısmı bulunur.

Anonim kalmak için tek bir router tüm ağ tarafından tunnel oluşturmak için kullanılmamalıdır. Eğer bir router TÜM I2P düğümleri için tunnel router görevi görürse, hem gerçek bir merkezi hata noktası hem de istemcilerden IP ve veri toplayan merkezi bir nokta haline gelir. Bu nedenle ağ, tunnel oluşturma sürecinde trafiği düğümler arasında dağıtır.

Performans için bir diğer husus da I2P'nin mesh ağ yapısını nasıl ele aldığıdır. Her bağlantı hop-hop, I2P düğümlerinde bir TCP veya UDP bağlantısı kullanır. 1000 bağlantı ile, 1000 TCP bağlantısı görülür. Bu oldukça fazladır ve bazı ev ve küçük ofis router'ları yalnızca az sayıda bağlantıya izin verir. I2P bu bağlantıları UDP ve TCP türü başına 1500'ün altında sınırlamaya çalışır. Bu aynı zamanda bir I2P düğümü üzerinden yönlendirilen trafik miktarını da sınırlar.

Bir düğüm erişilebilir durumdaysa ve >128 kbyte/sn paylaşılan bant genişliği ayarına sahipse ve 7/24 erişilebilir durumdaysa, bir süre sonra katılımcı trafik için kullanılmalıdır. Eğer arada çökmüşse, diğer düğümler tarafından yapılan I2P düğümü testleri onlara erişilemez olduğunu söyleyecektir. Bu, bir düğümü diğer düğümlerde en az 24 saat boyunca engeller. Yani, o düğümü çökük olarak test eden diğer düğümler, tunnel oluşturmak için o düğümü 24 saat boyunca kullanmayacaklardır. Bu nedenle I2P router'ınızı yeniden başlatma/kapatma işleminden sonra trafiğiniz minimum 24 saat boyunca düşük kalır.

Ek olarak, diğer I2P düğümlerinin bir I2P router'ını erişilebilirlik ve kapasite açısından test etmek için tanıması gerekir. Bu süreç, ağla etkileşim kurduğunuzda, örneğin uygulamaları kullanarak veya I2P sitelerini ziyaret ederek daha hızlı hale getirilebilir; bu da daha fazla tunnel oluşturulmasına ve dolayısıyla ağdaki düğümler tarafından test edilmek üzere daha fazla etkinlik ve erişilebilirliğe yol açar.

---

## Performans İyileştirmeleri

Gelecekte olası performans iyileştirmeleri için [Gelecekteki Performans İyileştirmeleri](/docs/overview/performance#future) bölümüne bakın.

Geçmiş performans iyileştirmeleri için [Performans Geçmişi](/docs/overview/performance#history) bölümüne bakın.
