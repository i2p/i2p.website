---
title: "Yönlendirici adreslerindeki host isimlerini kullanım dışı bırak"
number: "141"
author: "zzz"
created: "2017-08-03"
lastupdated: "2018-03-17"
status: "Kapalı"
thread: "http://zzz.i2p/topics/2363"
target: "0.9.32"
implementedin: "0.9.32"
toc: true
---

## Genel Bakış

0.9.32 sürümünden itibaren, netdb spesifikasyonunu güncelleyerek
yönlendirici bilgileri ve daha doğrusu yönlendirici adreslerindeki host isimlerini
kullanım dışı bırak. Tüm I2P uygulamalarında,
host isimleriyle yapılandırılmış yayın yapan yönlendiriciler yayınlamadan önce
host isimlerini IP'lerle değiştirmeli ve diğer yönlendiriciler host isimleriyle
adları geçen adresleri görmezden gelmelidir.
Yönlendiriciler, yayınlanan host isimlerinin DNS aramalarını yapmamalıdır.


## Gerekçe

I2P'nin başlangıcından bu yana, yönlendirici adreslerinde host isimlerine izin verilmiştir. Ancak, host isimlerini yayınlayan çok az yönlendirici bulunmaktadır,
çünkü bu hem herkese açık bir host ismi gerektirir (ki bu az sayıda kullanıcıda vardır),
hem de manuel yapılandırma gerektirir (ki kullanıcıların çoğu bunu yapmaz).
Yakın zamanda yapılan bir örneklemde, yönlendiricilerin %0.7'si bir host ismi yayınlıyordu.

Host isimlerinin orijinal amacı, sık sık değişen IP'lere ve dinamik bir DNS hizmetine sahip kullanıcıların (örneğin http://dyn.com/dns/)
IP değiştiğinde bağlantıyı kaybetmemelerine yardımcı olmaktı. Ancak o zamanlar
ağ çok küçüktü ve yönlendirici bilgi sürelerinin sona ermesi daha uzundu.
Ayrıca, Java kodu, yönlendiriciyi yeniden başlatacak
veya yerel IP değiştiğinde yönlendirici bilgisini yeniden yayınlayacak çalışır bir mantığa sahip değildi.

Ayrıca, başlangıçta I2P IPv6 desteklemiyordu,
bu yüzden bir host ismini IPv4 veya IPv6 adresine çözme karmaşıklığı yoktu.

Java I2P'de, yapılandırılmış bir host ismini hem yayınlanan iletim araçlarına
hem de IPv6 ile daha karmaşık hale gelen duruma yaymak her zaman bir zorluk olmuştur.

Çift yığınlı bir hostun hem bir host ismi hem de bir literal IPv6 adresi yayınlaması
gerekip gerekmediği net değildir. Host ismi SSU adresi için yayınlanır ama
NTCP adresi için yayınlanmaz.

Yakın zamanda, DNS sorunları Georgia Tech'deki
araştırmalar tarafından hem dolaylı olarak hem de doğrudan gündeme getirildi.
Araştırmacılar, host isimleri yayınlayarak büyük bir
sayıda floodfill yürütmüştür. Anında sorun, muhtemelen
bozuk yerel DNS'e sahip az sayıda kullanıcı için I2P'nin tamamen
kilitlenmesiydi.

Daha büyük sorun ise genel olarak DNS ve
DNS'in (etkin veya pasif) ağı çok hızlı bir şekilde
numaralandırmak için nasıl kullanılabileceğiydi,
özellikle yayın yapan yönlendiriciler floodfill ise.
Geçersiz host isimleri veya yanıt vermeyen, yavaş veya kötü niyetli
DNS yanıtlayıcılar ek saldırılar için kullanılabilir.
EDNS0 daha fazla numaralandırma veya saldırı senaryoları sağlayabilir.
DNS ayrıca, saatine göre yapılan aramalar temelinde saldırı yolları sağlayabilir,
yönlendiriciler arası bağlantı sürelerini ortaya çıkarabilir, bağlantı grafiklerini
oluşturmaya yardımcı olabilir, trafiği tahmin edebilir ve diğer çıkarımlar yapabilir.

Ayrıca, Georgia Tech grubu, David Dagon liderliğinde,
gizlilik odaklı uygulamalarda DNS ile ilgili birkaç endişe listelenmiştir.
DNS sorguları genellikle uygulama tarafından kontrol edilmeyen düşük seviyeli bir kütüphane tarafından yapılır.
Bu kütüphaneler anonimlik için özel olarak tasarlanmamıştır;
uygulama tarafından ince taneli kontrol sağlamayabilir;
ve çıkışları parmak izine maruz kalabilir.
Özellikle Java kütüphaneleri sorunlu olabilir, ancak bu sadece bir Java sorunu değildir.
Bazı kütüphaneler reddedilebilecek DNS ANY sorguları kullanır.
Tüm bunlar, çok sayıda kuruluş tarafından erişilebilir passif DNS izlemesi
ve sorgularının yaygın varlığı nedeniyle daha endişe verici hale gelir.
Tüm DNS izlemeleri ve saldırıları, I2P yönlendiricilerinin
bakış açısından bant dışıdır ve ağ içi I2P kaynaklarına çok az veya hiç gerektirmez,
ve mevcut uygulamaların değiştirilmesini gerektirmez.

Olası sorunları tamamen düşünmemiş olsak da,
saldırı yüzeyinin büyük göründüğü anlaşılmaktadır. Ağı numaralandırmanın ve ilgili verileri toplamanın
başka yolları da vardır, ancak DNS saldırıları
çok daha kolay, hızlı ve daha az tespit edilebilir olabilir.

Yönlendirici uygulamaları, teorik olarak, bir 3. parti DNS kütüphanesine geçebilir,
ancak bu oldukça karmaşık olur, bir bakım yükü getirir ve I2P geliştiricilerin
ana uzmanlık alanının oldukça dışındadır.

Java 0.9.31 için uygulanan acil çözümler, kilitlenme sorununu çözmek,
DNS önbellek sürelerini artırmak ve bir DNS negatif önbelleği uygulamaktı. Elbette,
önbellek sürelerini artırmak, başlangıç ​​olarak route bilgilerinde host isimlerine
sahip olmanın faydasını azaltır.

Ancak, bu değişiklikler yalnızca kısa vadeli hafifletmelerdir ve yukarıda belirtilen
temel sorunları çözmezler. Bu nedenle, en basit ve en eksiksiz çözüm,
yönlendirici bilgileri içinde host isimlerini yasaklamak,
böylece bunlar için DNS aramalarını ortadan kaldırmaktır.


## Tasarım

Yönlendirici bilgi yayınlama kodu için, uygulayıcılar iki seçeneğe sahiptir:
host isimleri için yapılandırma seçeneğini devre dışı bırakmak/kaldırmak veya
yayımlama sırasında yapılandırılmış host isimlerini IP'lere dönüştürmek.
Her iki durumda da, yönlendiriciler IP'leri değiştiğinde hemen yeniden yayınlamalıdır.

Yönlendirici bilgi doğrulama ve taşıma bağlantı kodu için,
uygulayıcılar host isimlerini içeren yönlendirici adreslerini görmezden gelmeli
ve varsa IP'leri içeren diğer yayınlanan adresleri kullanmalıdır.
Yönlendirici bilgisinde IP içeren adres yoksa, yönlendirici
yayınlanmış yönlendiriciye bağlanmamalıdır.
Hiçbir durumda bir yönlendirici, yayınlanmış bir host isminin DNS aramasını
doğrudan veya bir alt kütüphane aracılığıyla yapmamalıdır.


## Şartname

NTCP ve SSU taşıma spesifikasyonlarını değiştirerek
"host" parametresinin bir IP olması gerektiğini ve yönlendiricilerin
host isimlerini içeren bireysel yönlendirici adreslerini görmezden gelmesi gerektiğini belirtin.

Bu aynı zamanda bir SSU adresindeki "ihost0", "ihost1" ve "ihost2" parametreleri için de geçerlidir.
Yönlendiriciler, host isimlerini içeren tanıtıcı adresleri görmezden gelmelidir.


## Notlar

Bu öneri yeniden tohumlama sunucuları için host isimlerini ele almaz.
Yeniden tohumlama sunucuları için DNS aramaları çok daha az
sık yapılır, ancak yine de bir sorun olabilir. Gerekirse, bu sadece 
IP'lerle değiştirmek ve URL'lerin sabit kodlanmış listesinde değiştirme yaparak düzeltilebilir;
herhangi bir spesifikasyon veya kod değişiklikleri gerekmez.


## Geçiş

Bu öneri hemen uygulanabilir,
çünkü çok az yönlendirici host isimleri yayınlar
ve yayınlayanlar genellikle host ismini tüm adreslerde yayınlamazlar.

Yönlendiriciler, host isimlerini görmezden gelmeden önce
yayınlanan yönlendiricinin sürümünü kontrol etmemelidir
ve farklı yönlendirici uygulamaları arasında koordine bir sürüm veya
ortak stratejiye gerek yoktur.

Hala host isimleri yayınlayan yönlendiriciler için,
daha az gelen bağlantı alacaklar ve sonunda
gelen tüneller inşa etmede zorluk yaşayabilirler.

Etkileri daha da azaltmak için, önce sadece floodfill yönlendiriciler
için veya 0.9.32'den düşük bir sürümde yayımlanan yönlendiriciler için
host isimlerini göz ardı etmeye başlayabilir ve sonraki bir sürümde ise
tüm yönlendiriciler için host isimlerini görmezden gelebilirler.
