---
title: "Performans"
description: "I2P ağ performansı: bugün nasıl davranıyor, geçmişteki iyileştirmeler ve gelecekteki ayarlamalar için fikirler"
slug: "performance"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## I2P Ağ Performansı: Hız, Bağlantılar ve Kaynak Yönetimi

I2P ağı tamamen dinamiktir. Her istemci diğer düğümler tarafından bilinir ve yerel olarak bilinen düğümleri erişilebilirlik ve kapasite açısından test eder. Yalnızca erişilebilir ve yeterli kapasiteye sahip düğümler yerel NetDB'ye kaydedilir. Tünel oluşturma süreci sırasında, tünelleri oluşturmak için bu havuzdan en iyi kaynaklar seçilir. Test işlemi sürekli gerçekleştiğinden, düğüm havuzu değişir. Her I2P düğümü NetDB'nin farklı bir bölümünü bilir, bu da her router'ın tüneller için kullanılacak farklı bir I2P düğüm kümesine sahip olduğu anlamına gelir. İki router aynı bilinen düğüm alt kümesine sahip olsa bile, erişilebilirlik ve kapasite testleri muhtemelen farklı sonuçlar gösterecektir, çünkü diğer router'lar bir router test ederken yük altında olabilir ancak ikinci router test ettiğinde boşta olabilir.

Bu, her I2P düğümünün tüneller oluşturmak için farklı düğümlere sahip olmasının nedenini açıklar. Her I2P düğümü farklı gecikme ve bant genişliğine sahip olduğundan, tüneller (bu düğümler aracılığıyla oluşturulur) farklı gecikme ve bant genişliği değerlerine sahiptir. Ve her I2P düğümü farklı tüneller oluşturduğundan, hiçbir iki I2P düğümü aynı tünel kümelerine sahip değildir.

Bir sunucu/istemci "destination" (varış noktası) olarak bilinir ve her destination en az bir gelen ve bir giden tunnel'a sahiptir. Varsayılan değer tunnel başına 3 hopdur. Bu, tam bir gidiş-dönüş istemci → sunucu → istemci için toplam 12 hop (12 farklı I2P düğümü) anlamına gelir.

Her veri paketi sunucuya ulaşana kadar 6 farklı I2P düğümünden geçer:

client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - server

ve dönüş yolunda 6 farklı I2P düğümü:

server - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - client

Ağdaki trafik, yeni veri gönderilmeden önce bir ACK gerektirir; bir sunucudan ACK dönene kadar beklemek zorundadır: veri gönder, ACK bekle, daha fazla veri gönder, ACK bekle. RTT (Round Trip Time - Gidiş Dönüş Süresi) her bir I2P düğümünün gecikmesinden ve bu gidiş dönüş yolundaki her bir bağlantıdan biriktiği için, bir ACK'nin istemciye geri dönmesi genellikle 1–3 saniye sürer. TCP ve I2P aktarım tasarımı nedeniyle, bir veri paketinin sınırlı bir boyutu vardır. Bu koşullar birlikte, tünel başına kabaca 20–50 kB/s maksimum bant genişliği limiti belirler. Ancak, tüneldeki sadece bir atlama 5 kB/s bant genişliğine sahipse, tünelin tamamı gecikme ve diğer sınırlamalardan bağımsız olarak 5 kB/s ile sınırlıdır.

Şifreleme, gecikme süresi ve bir tünelin nasıl inşa edildiği, bir tünel oluşturmayı CPU zamanı açısından oldukça maliyetli hale getirir. Bu nedenle bir destination'ın veri taşımak için maksimum 6 gelen (inbound) ve 6 giden (outbound) tünele sahip olmasına izin verilir. Tünel başına maksimum 50 kB/s ile bir destination toplam yaklaşık 300 kB/s trafik kullanabilir (gerçekte düşük veya hiç anonimlik olmadan daha kısa tüneller kullanılırsa daha fazla olabilir). Kullanılan tüneller her 10 dakikada bir atılır ve yenileri oluşturulur. Bu tünel değişimi ve bazen kapanan veya ağ bağlantısını kaybeden istemciler, zaman zaman tünelleri ve bağlantıları bozar. Bunun bir örneği IRC2P Network'te bağlantı kaybında (ping timeout) veya eepget kullanırken görülebilir.

Sınırlı sayıda hedef ve hedef başına sınırlı sayıda tünel ile, bir I2P düğümü diğer I2P düğümleri üzerinden yalnızca sınırlı sayıda tünel kullanır. Örneğin, yukarıdaki küçük örnekte bir I2P düğümü "hop1" ise, istemciden kaynaklanan yalnızca bir katılımcı tünel görür. Tüm I2P ağını toplarsak, toplamda sınırlı miktarda bant genişliği ile yalnızca oldukça sınırlı sayıda katılımcı tünel oluşturulabilir. Bu sınırlı sayıları I2P düğümlerinin sayısına dağıtırsak, kullanılabilir bant genişliği/kapasitenin yalnızca bir kısmı kullanılabilir durumda olur.

Anonim kalmak için, tek bir router tüm ağ tarafından tünel oluşturmak için kullanılmamalıdır. Eğer bir router tüm I2P düğümleri için tünel router'ı olarak görev yaparsa, hem çok gerçek bir merkezi arıza noktası hem de istemcilerden IP'leri ve verileri toplayan merkezi bir nokta haline gelir. Bu nedenle ağ, tünel oluşturma sürecinde trafiği düğümler arasında dağıtır.

Performans için bir başka husus, I2P'nin mesh ağ yapısını ele alış biçimidir. Her bağlantı atlama‑atlama (hop‑to‑hop) I2P düğümlerinde bir TCP veya UDP bağlantısı kullanır. 1000 bağlantıda, 1000 TCP bağlantısı görülür. Bu oldukça fazladır ve bazı ev ve küçük ofis yönlendiricileri yalnızca az sayıda bağlantıya izin verir. I2P bu bağlantıları UDP ve TCP türü başına 1500'ün altında tutmaya çalışır. Bu, bir I2P düğümü üzerinden yönlendirilen trafik miktarını da sınırlar.

Bir düğüm erişilebilir durumdaysa ve >128 kB/s paylaşımlı bant genişliği ayarına sahipse ve 7/24 erişilebilir durumdaysa, bir süre sonra katılımcı trafik için kullanılmalıdır. Arada çevrimdışı olursa, diğer düğümler tarafından yapılan I2P düğüm testleri onlara erişilebilir olmadığını söyleyecektir. Bu, bir düğümü diğer düğümlerde en az 24 saat boyunca engeller. Dolayısıyla, o düğümü çevrimdışı olarak test eden diğer düğümler, tunnel oluşturmak için o düğümü 24 saat boyunca kullanmayacaktır. Bu nedenle, I2P router'ınızı yeniden başlattıktan/kapattıktan sonra trafiğiniz minimum 24 saat boyunca daha düşük olur.

Ek olarak, diğer I2P düğümlerinin bir I2P router'ı erişilebilirlik ve kapasite açısından test edebilmesi için onu bilmeleri gerekir. Bu süreç, ağ ile etkileşime girdiğinizde, örneğin uygulamalar kullanarak veya I2P sitelerini ziyaret ederek hızlandırılabilir; bu da daha fazla tunnel oluşturulmasına ve dolayısıyla ağdaki düğümler tarafından test için daha fazla aktivite ve erişilebilirliğe yol açar.

## Performans Geçmişi (seçili)

Yıllar içinde I2P, birçok önemli performans iyileştirmesi görmüştür:

### Native math

GNU MP kütüphanesi (GMP) ile JNI bağlantıları üzerinden, daha önce CPU zamanına hâkim olan BigInteger `modPow` işlemini hızlandırmak için uygulandı. İlk sonuçlar, açık anahtarlı kriptografide çarpıcı hız artışları gösterdi. Bakınız: /misc/jbigi/

### Garlic wrapping a "reply" LeaseSet (tuned)

Daha önce, yanıtlar genellikle gönderenin LeaseSet'i için bir ağ veritabanı sorgusu gerektiriyordu. Gönderenin LeaseSet'ini ilk garlic içinde paketlemek yanıt gecikmesini iyileştirir. Bu artık (bir bağlantının başlangıcında veya LeaseSet değiştiğinde) ek yükü azaltmak için seçici olarak yapılmaktadır.

### Yerel matematik

Bazı doğrulama adımları transport el sıkışmasında daha erken bir aşamaya taşındı; böylece hatalı eşler (yanlış saatler, hatalı NAT/firewall, uyumsuz sürümler) daha erken reddedilerek CPU ve bant genişliği tasarrufu sağlanıyor.

### Bir "yanıt" LeaseSet'ini Garlic sarmalama (ayarlanmış)

Bağlam farkında tünel testi kullanın: zaten veri geçirdiği bilinen tünelleri test etmekten kaçının; boşta iken test etmeyi tercih edin. Bu, ek yükü azaltır ve başarısız tünellerin tespitini hızlandırır.

### Daha verimli TCP reddetme

Belirli bir bağlantı için seçimlerin kalıcı hale getirilmesi, sıra dışı teslimi azaltır ve streaming kütüphanesinin pencere boyutlarını artırmasına izin vererek verimliliği artırır.

### Tünel test ayarlamaları

GZip veya benzer araçlar ayrıntılı yapılar için (örn. RouterInfo seçenekleri) uygun olduğu durumlarda bant genişliğini azaltır.

### Kalıcı tünel/lease seçimi

Basit "ministreaming" protokolünün yerine geçen çözüm. Modern streaming, I2P'nin anonim, mesaj odaklı altyapısına özel olarak tasarlanmış seçici ACK'ler ve tıkanıklık kontrolü içerir. Bakınız: /docs/api/streaming/

## Future Performance Improvements (historical ideas)

Aşağıda, potansiyel iyileştirmeler olarak tarihsel olarak belgelenmiş fikirler yer almaktadır. Birçoğu artık modası geçmiş, uygulanmış veya mimari değişiklikler tarafından geride bırakılmıştır.

### Seçili veri yapılarını sıkıştır

Yönlendiricilerin tünel oluşturma için eş seçimini iyileştirerek yavaş veya aşırı yüklü olanlardan kaçınmalarını sağlarken, güçlü saldırganlara karşı Sybil saldırılarına dirençli kalmak.

### Tam streaming protokolü

Anahtar uzayı kararlı olduğunda gereksiz keşfi azaltın; aramalarda kaç peer'ın döndürüleceğini ve kaç eşzamanlı aramanın gerçekleştirileceğini ayarlayın.

### Session Tag tuning and improvements (legacy)

Eski ElGamal/AES+SessionTag şeması için, daha akıllı son kullanma ve yenileme stratejileri ElGamal geri dönüşlerini ve boşa harcanan etiketleri azaltır.

### Daha iyi eş profilleme ve seçimi

Yeni bir oturum kurulumu sırasında tohumlanan senkronize bir PRNG'den etiketler üretin, önceden teslim edilen etiketlerden kaynaklanan mesaj başına ek yükü azaltarak.

### Ağ veritabanı ayarlama

Daha uzun tunnel ömürleri, iyileştirme ile birleştiğinde yeniden oluşturma maliyetlerini azaltabilir; anonimlik ve güvenilirlik ile dengeleyin.

### Session Tag ayarlama ve iyileştirmeleri (eski)

Geçersiz eşleri daha erken reddet ve çekişmeyi ve gecikmeyi azaltmak için tünel testlerini daha bağlama duyarlı hale getir.

### SessionTag'i senkronize PRNG'ye taşıma (eski)

Seçici LeaseSet paketleme, sıkıştırılmış RouterInfo seçenekleri ve tam streaming protokolünün benimsenmesi, algılanan performansın iyileşmesine katkıda bulunur.

---

IMPORTANT: Sadece çeviriyi sağlayın. Soru sormayın, açıklama yapmayın veya herhangi bir yorum eklemeyin. Metin sadece bir başlık veya eksik görünse bile, olduğu gibi çevirin.

Ayrıca bakınız:

- [Tunnel Yönlendirme](/docs/overview/tunnel-routing/)
- [Eş Seçimi](/docs/overview/tunnel-routing/)
- [Taşıma Katmanları](/docs/overview/transport/)
- [SSU2 Spesifikasyonu](/docs/specs/ssu2/) ve [NTCP2 Spesifikasyonu](/docs/specs/ntcp2/)
