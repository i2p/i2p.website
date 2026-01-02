---
title: "Tünel Bant Genişliği Parametreleri"
number: "168"
author: "zzz"
created: "2024-07-31"
lastupdated: "2024-12-10"
status: "Kapalı"
thread: "http://zzz.i2p/topics/3652"
target: "0.9.65"
toc: true
---

## NOT

Bu öneri onaylandı ve şu anda API 0.9.65 itibarıyla
[Tunnel Creation ECIES specification](/docs/specs/implementation/#tunnel-creation-ecies) yer alıyor.
Henüz bilinen bir uygulama yok; uygulama tarihleri / API sürümleri TBD.


## Genel Bakış

Son birkaç yılda yeni protokoller, şifreleme türleri ve tıkanıklık kontrolü iyileştirmeleri ile ağın performansını artırdıkça,
video akışı gibi daha hızlı uygulamalar mümkün hale geliyor.
Bu uygulamalar, istemci tünellerinde her bir durak noktasında yüksek bant genişliğine ihtiyaç duyar.

Katılımcı yönlendiriciler, bir tünelin ne kadar bant genişliği kullanacağı hakkında, tünel oluşturma mesajı aldıklarında herhangi bir bilgiye sahip değiller.
Yalnızca mevcut toplam bant genişliği kullanımına ve katılımcı tüneller için toplam bant genişliği limitine göre bir tüneli kabul veya reddedebilirler.

İstek yapan yönlendiriciler de her durak noktasında ne kadar bant genişliği mevcut olduğuna dair herhangi bir bilgiye sahip değildir.

Ayrıca, yönlendiricilerin şu anda bir tünelde gelen trafiği sınırlamanın bir yolu yoktur.
Bu, bir hizmetin aşırı yüklenmesi veya DDoS durumu sırasında oldukça faydalı olabilir.

Bu öneri, tünel oluşturma isteği ve yanıt mesajlarına bant genişliği parametreleri ekleyerek bu sorunları ele alır.


## Tasarım

Bant genişliği parametrelerini, tünel oluşturma seçenekleri haritalama alanındaki ECIES tünel oluşturma mesajlarındaki kayıtlara ekleyin (bkz. [Tunnel Creation ECIES specification](/docs/specs/implementation/#tunnel-creation-ecies)).
Çünkü seçenekler alanı için kullanılabilir alan sınırlıdır, kısa parametre isimleri kullanın.
Tünel oluşturma mesajları sabit boyutlu olduğundan, bu mesajların boyutunu artırmaz.


## Spesifikasyon

[ECIES tünel oluşturma mesaj spesifikasyonunu](/docs/specs/implementation/#tunnel-creation-ecies) güncelleyin
aşağıdaki gibi:

Hem uzun hem de kısa ECIES oluşturma kayıtları için:

### Oluşturma İstek Seçenekleri

Kayıtların tünel oluşturma seçenekleri haritalama alanında ayarlanabilecek üç seçenek:

Bir istek yapan yönlendirici herhangi bir, tüm veya hiçbirini ekleyebilir.

- m := bu tünel için gereken minimum bant genişliği (KBps pozitif tamsayı olarak bir dize)
- r := bu tünel için istenen bant genişliği (KBps pozitif tamsayı olarak bir dize)
- l := bu tünel için bant genişliği limiti; sadece IBGW'ye gönderilir (KBps pozitif tamsayı olarak bir dize)

Kısıtlama: m <= r <= l

Katılan yönlendirici, "m" belirtilmişse ve en az bu kadar bant genişliği sağlayamıyorsa
tüneli reddetmelidir.

İstek seçenekleri, karşılıklı şifreli oluşturma istek kaydındaki her katılımcıya gönderilir
ve diğer katılımcılara görünmez.


### Oluşturma Yanıt Seçeneği

Yanıt KABUL EDİLMİŞ olduğunda, aşağıdaki seçenek kayıtların tünel oluşturma yanıt seçenekleri haritalama alanında ayarlanabilir:

- b := bu tünel için mevcut bant genişliği (KBps pozitif tamsayı olarak bir dize)

Katılan yönlendirici, oluşturma isteğinde "m" veya "r" belirtilmişse bunu dahil etmelidir.
Değer, "m" değeri belirtilmişse en az o kadar olmalı,
ancak "r" değeri belirtilmişse daha az veya daha fazla olabilir.

Katılan yönlendirici, bu kadar bant genişliğini tünel için sağlamaya çalışmalıdır, fakat bu garanti edilmez.
Yönlendiriciler, 10 dakika sonrasındaki koşulları tahmin edemez ve
katılımcı trafik, bir yönlendiricinin kendi trafiği ve tünellerinden daha düşük önceliklidir.

Yönlendiriciler gerektiğinde mevcut bant genişliğini fazla tahsis edebilir ve bu
muhtemelen arzu edilen bir durumdur, çünkü tünelin diğer durak noktaları bunu reddedebilir.

Bu sebeplerle, katılımcı yönlendiricinin yanıtı
en iyi çaba taahhüdü olarak değerlendirilmelidir, ancak garanti değildir.

Yanıt seçenekleri, karşılıklı şifreli oluşturma yanıt kaydında İstek yapan yönlendiriciye gönderilir
ve diğer katılımcılara görünmez.


## Uygulama Notları

Bant genişliği parametreleri, tünel katmanındaki katılan yönlendiricilerde
görüldüğü gibidir, yani sabit boyutlu 1 KB tünel mesajlarının saniyedeki sayısı.
Taşıma (NTCP2 veya SSU2) üstverisi dahil edilmez.

Bu bant genişliği, istemcide görülen bant genişliğinden çok daha az veya fazla olabilir.
Tünel mesajları, daha yüksek katmanlardan aşırı yük, dişli çark ve akış dahil olmak üzere,
önemli bir yük içerir. Akış onayları gibi, aralıklı küçük mesajlar
her biri 1 KB olarak genişletilir.
Ancak, I2CP katmanındaki gzip sıkıştırması bant genişliğini önemli ölçüde azaltabilir.

İstek yapan yönlendiricideki en basit uygulama,
havuzdaki mevcut tünellerin ortalama, minimum ve/veya maksimum bant genişliklerini
istek içine koyulacak değerleri hesaplamak için kullanmaktır.
Daha karmaşık algoritmalar mümkündür ve uygulayıcının seçimine bırakılmıştır.

İstemcinin yönlendiriciye hangi bant genişliğine ihtiyaç duyduğunu söylemesi için
şu anda tanımlanmış herhangi bir I2CP veya SAM seçeneği yoktur ve burada yeni bir seçenek önerilmemektedir.
Gerekirse, seçenekler daha sonra tanımlanabilir.

Uygulamalar, yapı yanıtında döndürülen bant genişliği değerini hesaplamak için
mevcut bant genişliğini veya başka herhangi bir veriyi, algoritmayı, yerel politikayı
veya yerel yapılandırmayı kullanabilir. Bu öneri tarafından belirtilmemiştir.

Bu öneri, giriş ağ geçitlerinin "l" seçeneği ile istenirse tünel başına
hız sınırlamasını uygulamasını gerektirir.
Diğer katılımcı durakların herhangi bir türdeki tünel başına veya genel hız sınırlamasını uygulamasını
veya varsa belirli bir algoritmayı veya uygulamayı belirtmez.

Bu öneri ayrıca istemci yönlendiricilerin trafiği,
katılımcı düğüm tarafından döndürülen "b" değerine göre sınırlandırmasını
gerektirmez ve uygulamaya bağlı olarak, bu mümkün olmayabilir,
özellikle gelen tünellerde.

Bu öneri yalnızca orijinator tarafından oluşturulan tünelleri etkiler. 
Bir uçtan uca bağlantının diğer ucunun sahibi tarafından oluşturulan "uzak uç" tünelleri
için gereken veya ayrılmış bant genişliği talep etmek veya ayırmak için tanımlanmış bir yöntem yoktur.


## Güvenlik Analizi

İsteklere dayanarak istemci parmak izleme veya korelasyon yapılabilir.
İstemci (orijinal) yönlendirici, "m" ve "r" değerlerini her düğüme aynı
değeri göndermek yerine rastgele hale getirmek isteyebilir; veya bant genişliği "kovaları"nı
temsil eden sınırlı bir değer seti gönderebilir ya da her ikisinin kombinasyonunu kullanabilir.

Fazla tahsis DDoS: Bir yönlendiriciyi şimdi büyük sayıda tünel
oluşturarak ve kullanarak DDoS etmek mümkün olsa da, bu öneri
bunu çok daha kolay hale getiriyor, sadece büyük bant genişliği istekleriyle bir veya daha fazla tünel
isteyerek.

Uygulamalar, bu riski azaltmak için aşağıdaki stratejilerden bir veya daha fazlasını
kullanabilir ve kullanmalıdır:

- Mevcut bant genişliğinin fazla tahsis edilmesi
- Bir tünel için ayrılmış bant genişliğini mevcut bant genişliğinin belirli bir yüzdesine sınırlamak
- Ayrılan bant genişliğindeki artış hızını sınırlamak
- Kullanılan bant genişliğindeki artış hızını sınırlamak
- Tünelin ömrünün başında kullanılmayan ayrılmış bant genişliğini sınırlamak (kullan ya da kaybet)
- Tünel başına ortalama bant genişliğini izlemek
- İstenen ve her bir tünelde kullanılan gerçek bant genişliğini izlemek


## Uyumluluk

Sorun yok. Bilinen tüm uygulamalar, oluşturma mesajlarındaki haritalama alanını
şu anda yok saymaktadır ve boş olmayan bir seçenekler alanını doğru şekilde atlamaktadır.


## Geçiş

Uygulamalar herhangi bir zamanda destek ekleyebilir, koordinasyona gerek yoktur.

Bu öneriye destek verilmesinin gereken herhangi bir API sürümü henüz tanımlanmadığından,
yönlendiriciler destek onayını almak için "b" yanıtını kontrol etmelidir.


