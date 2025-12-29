---
title: "LS2'de Servis Kayıtları"
number: "167"
author: "zzz, orjinal, eyedeekay"
created: "2024-06-22"
lastupdated: "2025-04-03"
status: "Kapalı"
thread: "http://zzz.i2p/topics/3641"
target: "0.9.66"
toc: true
---

## Durum
2025-04-01'de ikinci incelemede onaylandı; belirtimler güncellenmiştir; henüz uygulanmadı.


## Genel Bakış

I2P'nin merkezi bir DNS sistemi yoktur.
Ancak, adres defteri ve b32 host adı sistemi ile birlikte router,
tam destinasyonları arayabilir ve kiralama setlerini çekebilir, bu setler
ağ geçitleri ve anahtarlar listesi içerir, böylece müşteriler bu destinasyona bağlanabilir.

Bu bağlamda, kiralama setleri bir nevi DNS kaydı gibidir. Ancak, şu anda bu hostun
herhangi bir hizmeti destekleyip desteklemediğini öğrenmek için bir kolaylık yoktur,
ya o destinasyonda ya da farklı bir destinasyonda, DNS SRV kayıtlarına benzer bir
biçimde [SRV](https://en.wikipedia.org/wiki/SRV_record) [RFC2782](https://datatracker.ietf.org/doc/html/rfc2782).

Bunun için ilk başvuru eşler arası e-posta olabilir.
Diğer potansiyel uygulamalar: DNS, GNS, anahtar sunucuları, sertifika yetkilileri, zaman sunucuları,
bittorrent, kripto paralar, diğer eşler arası uygulamalar.


## İlgili Öneriler ve Alternatifler

### Servis Listeleri

LS2 önerisi 123 [Prop123](/proposals/123-new-netdb-entries/) bir destinasyonun
küresel bir hizmete katıldığını belirten 'servis kayıtlarını' tanımlamıştır.
Bu kayıtları küresel 'servis listeleri' içine
toplayacaktı. Bu, karmaşıklık, kimlik doğrulama eksikliği,
güvenlik ve spam konuları nedeniyle hiç uygulanmadı.

Bu öneri, belirli bir destinasyon için bir servis araması sağladığı için farklıdır,
bazı küresel hizmetler için küresel bir destinasyon havuzu değil.

### GNS

GNS [GNS](http://zzz.i2p/topcs/1545), herkesin kendi DNS sunucusunu çalıştırması gerektiğini önermektedir.
Bu öneri tamamlayıcıdır, çünkü GNS'nin (veya DNS'nin) desteklendiğini belirtmek için
standart bir servis adı "domain" olarak 53 numaralı portta servis kayıtlarını kullanabiliriz.

### Dot well-known

[DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102) içinde, hizmetlerin bir HTTP isteği ile aranması önerilmektedir
/.well-known/i2pmail.key. Bu, her hizmetin
anahtarı barındıracak bir ilişkili web sitesi olması gerektiği anlamına gelir. Çoğu kullanıcı web sitesi çalıştırmaz.

Bir çözüm yolu, b32 adresi için bir hizmetin aslında
o b32 adresinde çalıştığını varsayabiliriz. Öyle ki, örneğin.example.i2p için hizmet aramak,
http://example.i2p/.well-known/i2pmail.key adresinden HTTP ile almak gerektirir,
ancak aaa...aaa.b32.i2p için bir hizmet bu aramayı gerektirmez, doğrudan bağlanabilir.

Ancak burada bir belirsizlik var, çünkü example.i2p de kendi b32 adresi ile adreslenebilir.

### MX Kayıtları

SRV kayıtları, herhangi bir hizmet için MX kayıtlarının genel bir versiyonudur.
"_smtp._tcp", "MX" kaydıdır.
Eğer SRV kayıtlarımız varsa MX kayıtlarına gerek yoktur, ve tek başına MX kayıtları
herhangi bir hizmet için genel bir kayıt sağlamaz.


## Tasarım

Servis kayıtları LS2 içinde seçenekler bölümüne yerleştirilir [LS2](/docs/specs/common-structures/).
LS2 seçenekler bölümü şu anda kullanılmamaktadır.
LS1 için desteklenmemektedir.
Bu, tünel bant genişliği önerisine [Prop168](/proposals/168-tunnel-bandwidth/) benzerdir,
tünel yapı kayıtları için seçenekler tanımlar.

Belirli bir hostname veya b32 için bir servis adresi aramak için, router
kiralama setini çeker ve özelliklerde servis kaydını arar.

Hizmet LS'nin kendisi ile aynı destinasyonda barındırılabilir veya farklı bir hostname/b32 referansında bulunabilir.

Hizmetin hedef destinasyonu farklıysa, hedef LS de
"hizmeti desteklediğini" belirten bir servis kayıtları içermelidir.

Tasarım, floodfill'lerde özel bir destek veya önbelleğe alma veya herhangi bir değişiklik gerektirmez.
Sadece kiralama seti yayıncısı ve bir servis kaydı arayan müşteri
bu değişiklikleri desteklemelidir.

Müşterilerin servis kayıtlarını almasını kolaylaştırmak için küçük I2CP ve SAM uzantıları önerilmektedir.


## Belirtim

### LS2 Seçenek Belirtimi

LS2 seçenekleri, imzanın değişmez olması için anahtar göre sıraya dizilmiş OLMALIDIR.

Aşağıdaki gibi tanımlanır:

- servis seçeneği := seçenek anahtarı seçenek değeri
- seçenek anahtarı := _service._proto
- hizmet := İstenen hizmetin sembolik adı. Küçük harf olmalıdır. Örnek: "smtp".
  İzin verilen karakterler [a-z0-9-] ve '-' ile başlamamalı veya bitmemelidir.
  [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) veya Linux /etc/services tanımlandığı yerlerde standart tanımlayıcılar kullanılmalıdır.
- proto := İstenen hizmetin taşıma protokolü. Küçük harf olmalı, ya "tcp" ya da "udp".
  "tcp", akış anlamına gelir ve "udp", yanıt verilebilir datagram anlamına gelir.
  Ham datagramlar ve datagram2 için protokol göstergeleri daha sonra tanımlanabilir.
  İzin verilen karakterler [a-z0-9-] ve '-' ile başlamamalıdır.
- seçenek değeri := self | srv kayıt[,srv kayıt]*
- self := "0" ttl port [app seçenekleri]
- srv kayıt := "1" ttl öncelik ağırlık port hedef [app seçenekleri]
- ttl := canlı kalma süresi, tam sayı saniyeler. Pozitif tam sayı. Örnek: "86400".
  Ayrıntılar için aşağıdaki Öneriler bölümüne bakınız, en az 86400 (bir gün) önerilir.
- öncelik := Hedef ev sahibinin önceliği, daha düşük değer, daha çok tercih edilir. Negatif olmayan bir tam sayı. Örnek: "0"
  Sadece birden fazla kayıt varsa yararlıdır, ancak tek kayıt bile olsa gereklidir.
- ağırlık := Aynı önceliğe sahip kayıtlar için nispi ağırlık. Daha yüksek değer, seçilme şansının daha fazla olması demektir. Negatif olmayan bir tam sayı. Örnek: "0"
  Sadece birden fazla kayıt varsa yararlıdır, ancak tek kayıt bile olsa gereklidir.
- port := Hizmetin bulunacağı I2CP portu. Negatif olmayan bir tam sayı. Örnek: "25"
  Port 0 desteklenir ancak önerilmez.
- hedef := Hizmeti sağlayan hedefin hostname veya b32. Geçerli bir hostname olarak [NAMING](/docs/overview/naming/) içinde tanımlanmıştır. Küçük harf olmalıdır.
  Örnek: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" ya da "example.i2p".
  b32 önerilir, hostname "iyi bilinen," yani resmi veya varsayılan adres defterlerindeyse.
- app seçenekleri := uygulamaya özgü rastgele metin, " " veya "," içeremez. Kodlama UTF-8'dir.

### Örnekler


Tek bir SMTP sunucusuna işaret eden aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p için LS2'de:

    "_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

İki SMTP sunucusuna işaret eden aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p için LS2'de:

    "_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

Kendisine bir SMTP sunucusu olarak işaret eden bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p için LS2'de:

    "_smtp._tcp" "0 999999 25"

E-posta yönlendirmesi için olası format (aşağıya bakınız):

    "_smtp._tcp" "1 86400 0 0 25 smtp.postman.i2p example@mail.i2p"


### Sınırlar


LS2 seçenekleri için kullanılan Veri Yapısı Formatı anahtarları ve değerleri maksimum 255 byte (karakter değil) ile sınırlandırır.
Bir b32 hedefi ile, bilgi değeri yaklaşık 67 byte olur, bu nedenle sadece 3 kayıt sığabilir.
Belki uzun bir app seçenekleri alanıyla sadece bir veya iki, ya da kısa bir hostname ile dört veya beş.
Bu yeterli olmalıdır; birden fazla kayıt nadir olmalıdır.


### [RFC2782] ile Farklılıklar


- Sonunda nokta yok
- Proto ardından isim yok
- Küçük harf gereklidir
- Metin formatında, virgülle ayrılmış kayıtlar, ikili DNS formatında değil
- Farklı kayıt türü göstergeleri
- Ek app seçenekleri alanı


### Notlar


(asterisk) ve (asterisk)._tcp gibi genel wildcard'lama izin verilmez.
Her desteklenen hizmetin kendi kaydı olmalıdır.


### Servis Adı Kaydı

[REGISTRY](http://www.dns-sd.org/ServiceTypes.html) veya Linux /etc/services'te listelenmeyen standart olmayan tanımlayıcılar
talep edilebilir ve ortak yapılar belirtimine [LS2](/docs/specs/common-structures/) eklenebilir.

Hizmete özgü app seçenek formatları da oraya eklenebilir.


### I2CP Belirtimi

[I2CP](/docs/specs/i2cp/) protokolü, hizmet aramalarını destekleyecek şekilde genişletilmelidir.
Servis aramasıyla ilgili ek MessageStatusMessage ve / veya HostReplyMessage hata kodları gereklidir.
Hizmet kaydı özellikli olup olmadığını belirtmek için arama kolaylığının genel olması amaçlanmıştır,
tüm LS2 seçeneklerinin alınmasını desteklemek için tasarlanmıştır.

Uygulama: HostLookupMessage'ı genişletme ile hash, hostname ve destinasyon (istek türleri 2-4)
için LS2 seçeneklerini talep etmek.
İstendiğinde HostReplyMessage'ı seçenekler haritalamasını eklemek için genişletme.
HostReplyMessage'a ek hata kodları ekleme.

Seçenek haritaları, müşteri veya router tarafında, uygulamaya bağlı olarak kısa bir süre önbelleğe alınabilir veya negatif önbelleğe alınabilir. Önerilen maksimum süre bir saattir, hizmet kaydı TTL'si daha kısa olmadıkça.
Hizmet kayıtları uygulama, müşteri veya router tarafından belirtilen TTL'ye kadar önbelleğe alınabilir.

Belirtileri aşağıdaki gibi genişletin:

### Yapılandırma seçenekleri


[I2CP-OPTIONS]'a aşağıdakileri ekleyin

i2cp.leaseSetOption.nnn

Kiralanacak seçenekler. Sadece LS2 için kullanılabilir.
nnn, 0 ile başlar. Seçenek değeri "anahtar=değer" içerir.
(tırnakları içermeyin)

Örnek:

    i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p


### HostLookup Mesajı


- Görünüm tipi 2: Hash görünümü, seçenekler haritalama talebi
- Görünüm tipi 3: Hostname görünümü, seçenekler haritalama talebi
- Görünüm tipi 4: Destinasyon görünümü, seçenekler haritalama talebi

Görünüm tipi 4 için, öğe 5 bir Destinasyondur.


### HostReply Mesajı


Görünüm türleri 2-4 için, router kiralama setini çekmelidir,
anahtar, adres defterinde olsa bile.

Başarılı olursa, HostReply, kiralama setinden gelen seçenekler Haritalamasını
içerir ve destinasyondan sonra öğe 5 olarak dahil eder.
Haritalamada seçenek yoksa, veya kiralama seti 1. versiyon ise,
hala boş bir Haritalama olarak dahil edilecektir (iki byte: 0 0).
Gelecekte tanımlanan parametreler için örneklerin bulunabileceği için
kiralama setindeki tüm örnekler dahil edilecektir, sadece hizmet kaydı örnekleri değil.

Kiralama seti görünümü başarısız olursa, yanıt, yeni hata kodu 6 (Kiralama seti görünümü başarısızlığı) içerecek
ve haritalamayı içermeyecektir.
Hata kodu 6 döndürüldüğünde, Destinasyon alanı olabilir veya olmayabilir.
Adres defterinde bir hostname görünümü başarılı olduysa, veya bir önceki görünüm başarıyla sonuçlandı ve sonuç önbelleğe alındı,
ya da Görünüm mesajında Destinasyon mevcutsa (görünüm türü 4),
bulunacaktır.

Bir görünüm türü desteklenmiyorsa,
yanıt yeni hata kodu 7 (görünüm türü desteklenmiyor) içerecektir.


### SAM Beliritimi

[SAMv3](/docs/api/samv3/) protokolü, hizmet aramaları için genişletilmelidir.

NAMING LOOKUP'ı aşağıdaki gibi genişletin:

NAMING LOOKUP NAME=example.i2p OPTIONS=true yanıt içinde seçenekler haritalaması talep eder.

NAME, OPTIONS=true olduğunda tam base64 destinasyonu olabilir.

Kiralama seti görünümü başarılı olduysa ve seçenekler kiralama setinde mevcutsa,
yanıtta, destinasyonun ardından,
bir veya daha fazla seçenek OPTION:key=value formunda olacaktır.
Her seçenek, ayrı bir OPTION: ön eki taşıyacaktır.
Gelecekte tanımlanan parametreler için seçeneklerin bulunabilir olması durumunda
kiralama setindeki tüm seçenekler dahil edilecektir, sadece hizmet kaydı seçenekleri değil.
Örnek:

    NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

'=' içeren anahtarlar ve bir yeni satır içeren anahtarlar veya değerler,
geçersiz olarak kabul edilir ve yanıt içindeki anahtar/değer çifti çıkarılır.

Kiralama setinde bulunan seçenekler yoksa veya kiralama seti 1. versiyon ise,
yanıtta herhangi bir seçenek bulunmayacaktır.

OPTIONS=true aramada varsa ve kiralama seti bulunamadıysa, yeni bir sonuç değeri olarak LEASESET_NOT_FOUND dönecektir.


## İsim Araması Alternatifi

Tam bir hostname olarak hizmet aramalarını desteklemek üzere
bir alternatif tasarım, [NAMING]'i güncelleyerek, '_'
ile başlayan hostnamelere yönelik işler tanımlamaktı.
Bu iki nedenle reddedildi:

- I2CP ve SAM değişiklikleri, TTL ve port bilgilerini
  müşteri tarafına iletmek için yine de gerekli olacaktır.
- Bu, gelecekte tanımlanacak diğer LS2
  seçeneklerini almak için genel bir olanak sağlamayacaktır.


## Öneriler

Sunucular, en az 86400 ve uygulama için standart portu belirtmelidir.


## Gelişmiş Özellikler

### Özyinelemeli Aramalar

Muhtemelen özyinelemeli aramalara destek sağlanması, her bir ardışık kiralama setinin
başka bir kiralama setine işaret eden bir hizmet kaydının, DNS tarzında kontrol edilmesi gerekir.
Bu, en azından ilk bir uygulamada muhtemelen gerekli değildir.

TODO


### Uygulamaya Özgü Alanlar

Servis kaydında uygulamaya özgü verilere sahip olmak istenebilir.
Örneğin, example.i2p operatörü, email'ın
example@mail.i2p adresine yönlendirilmesi gerektiğini belirtmek isteyebilir. "example@"
kısmı hizmet kaydının ayrı bir alanında olmalı veya hedeften çıkarılmalıdır.

Operatör kendi email hizmetini çalıştırıyor olsa bile, email'
in example@example.i2p adresine gönderilmesi gerektiğini belirtmek isteyebilir.
Çoğu I2P hizmeti tek bir kişi tarafından işletilmektedir.
Bu nedenle burada ayrı bir alan da faydalı olabilir.

Bunu nasıl genel bir şekilde yapılacağı hakkında TODO


### E-posta İçin Gerekli Değişiklikler

Bu önerinin kapsamı dışındadır. Daha fazla bilgi için [DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102) tartışmasına bakınız.


## Uygulama Notları

Hizmet kayıtları, TTL'ye kadar router veya uygulama tarafından önbelleğe alınabilir,
uygulamaya bağlı olarak. Kalıcı olarak önbelleğe alınıp alınmayacağı da uygulamaya bağlıdır.

Aramalar, hedef kiralama setini de kontrol etmeli ve "self" kaydını
içerdiğini doğrulamalıdır, hedef destinasyonu müşteriye döndürmeden önce.


## Güvenlik Analizi

Kiralama seti imzalı olduğundan, içindeki herhangi bir servis kaydı
hedefin imza anahtarı ile kimlik doğrulaması yapılmıştır.

Servis kayıtları, kiralama seti şifreli değilse, floodfill'ler için
açıktır ve görünürdedir. Kiralama setini talep eden herhangi bir router,
servis kayıtlarını görebilecektir.

"self" dışında bir SRV kaydı (yani farklı bir hostname/b32 hedefe işaret eden)
hedef hostname/b32'nin rızasını gerektirmez.
Bir hizmetin keyfi bir destinasyona yönlendirilmesinin
bir tür saldırıyı kolaylaştırıp kolaylaştıramayacağı veya
böyle bir saldırının amacının ne olacağı açık değildir.
Bununla birlikte, bu öneri, hedefin
kendisi üzerinde bir "self" SRV kaydı yayınlamasını gerektirerek
böyle bir saldırıyı önlemektedir. Uygulayıcılar hedefin
kiralama setinde bir "self" kaydını kontrol etmelidir.


## Uyumluluk

LS2: Hiçbir sorun yok. Tüm bilinen uygulamalar şu anda LS2 içindeki seçenek alanını yoksayar,
ve dolu bir seçenek alanını doğru bir şekilde atlar.
Bu, LS2'nin geliştirilmesi sırasında Java I2P ve i2pd tarafından yapılan testlerle doğrulanmıştır.
LS2, 0.9.38'de 2016 yılında uygulanmış ve tüm router uygulamaları tarafından iyi bir şekilde desteklenmiştir.
Tasarım, floodfilllerde özel bir destek veya önbelleğe alma veya herhangi bir değişiklik gerektirmez.

İsimlendirme: '_' i2p hostnamelerinde geçerli bir karakter değildir.

I2CP: Görünüm türleri 2-4, desteklendiği minimum API versiyonunun altındaki router'lara gönderilmemelidir (TBD).

SAM: Java SAM sunucusu, OPTIONS=true gibi ek anahtar/değerleri yoksayar.
i2pd'nin de aynı şekilde davranıp davranmadığı kontrol edilmelidir.
SAM istemcileri, yalnızca OPTIONS=true ile talep edildiklerinde yanıtta ek değerleri alır.
Herhangi bir sürüm artışı gerekli görünmemektedir.


