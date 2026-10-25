---
title: "NTCP Tartışması"
description: "Mart 2007'den NTCP vs SSU transport protokolleri hakkında geçmiş tartışma"
slug: "ntcp-discussion"
aliases:
  - "/tr/docs/discussions/ntcp"
  - "/tr/docs/discussions/ntcp/"
  - "/tr/ntcp_discussion"
  - "/tr/ntcp_discussion/"
lastUpdated: "2007-03"
accurateFor: "historical"
---

Aşağıda Mart 2007'de gerçekleşen NTCP hakkında bir tartışma yer almaktadır. Mevcut uygulama durumunu yansıtacak şekilde güncellenmemiştir. Güncel NTCP spesifikasyonu için [NTCP2 sayfasına](/docs/specs/ntcp2) bakın.

## NTCP vs. SSU Tartışması, Mart 2007 {#ntcp-ssu}

### NTCP soruları

(zzz ve cervantes arasındaki IRC tartışmasından uyarlanmıştır)

NTCP neden SSU'ya tercih ediliyor, NTCP'nin daha yüksek ek yükü ve gecikmesi yok mu? Daha iyi güvenilirliğe sahip.

NTCP üzerinden streaming lib kullanmak klasik TCP-over-TCP sorunlarından muzdarip değil mi? Streaming-lib kaynaklı trafik için gerçekten basit bir UDP transport'u olsaydı ne olurdu? SSU'nun sözde gerçekten basit UDP transport'u olması gerekiyordu - ama çok güvenilmez olduğu kanıtlandı.

### zzz Tarafından "NTCP Zararlı Kabul Edilir" Analizi {#harmful}

Yeni Syndie'ye gönderildi, 2007-03-25. Bu tartışmayı teşvik etmek için gönderilmiştir, çok ciddiye almayın.

**Özet:** NTCP, SSU'ya göre daha yüksek gecikme süresine ve ek yüke sahiptir ve streaming lib ile kullanıldığında çökme olasılığı daha yüksektir. Ancak trafik NTCP'ye SSU'ya göre öncelik verilerek yönlendirilir ve bu şu anda sabit kodlanmıştır.

#### Tartışma

Şu anda iki transport'umuz var, NTCP ve SSU. Mevcut uygulamada, NTCP'nin SSU'dan daha düşük "teklifi" var bu nedenle tercih ediliyor, ancak bir eş için kurulmuş SSU bağlantısı olup kurulmuş NTCP bağlantısı olmadığı durumlar hariç.

SSU, onaylamalar, zaman aşımları ve yeniden iletimleri uygulaması bakımından NTCP'ye benzer. Ancak SSU, zaman aşımları üzerinde sıkı kısıtlamaları ve gidiş-dönüş süreleri, yeniden iletimler vb. konularında mevcut istatistikleri olan I2P kodudur. NTCP, kara kutu olan ve RFC standartlarını (çok uzun maksimum zaman aşımları dahil) uyguladığı varsayılan Java NIO TCP tabanlıdır.

I2P içindeki trafiğin çoğunluğu streaming-lib kaynaklıdır (HTTP, IRC, Bittorrent) ki bu bizim TCP implementasyonumuzdur. Alt seviye aktarım genellikle düşük teklifler nedeniyle NTCP olduğundan, sistem TCP-over-TCP'nin iyi bilinen ve korkulan problemine maruz kalır http://sites.inka.de/~W1011/devel/tcp-tcp.html , burada TCP'nin hem üst hem de alt katmanları aynı anda yeniden iletim yaparak çöküşe yol açar.

Yukarıdaki bağlantıda açıklanan PPP over SSH senaryosunun aksine, alt katman için her biri bir NTCP bağlantısı tarafından kapsanan birkaç hop'umuz var. Bu nedenle her NTCP gecikme süresi genellikle üst katman streaming lib gecikme süresinden çok daha azdır. Bu da çökme olasılığını azaltır.

Ayrıca, alt katman TCP'nin yüksek katmana kıyasla düşük zaman aşımları ve yeniden iletim sayıları ile sıkı bir şekilde kısıtlandığı durumlarda çökme olasılıkları azalır.

.28 sürümü streaming lib maksimum zaman aşımını 10 saniyeden 45 saniyeye çıkardı ve bu durumu büyük ölçüde iyileştirdi. SSU maksimum zaman aşımı 3 saniyedir. NTCP maksimum zaman aşımı muhtemelen en az 60 saniyedir ki bu RFC önerisidir. NTCP parametrelerini değiştirmenin veya performansı izlemenin bir yolu yoktur. NTCP katmanının çökmesi [editör: metin kayıp]. Belki tcpdump gibi harici bir araç yardımcı olabilir.

Ancak .28 sürümünü çalıştırırken, i2psnark tarafından bildirilen upstream genellikle yüksek seviyede kalmıyor. Tekrar yükselmeden önce sıklıkla 3-4 KBps'ye düşüyor. Bu, hala çöküşler yaşandığının bir işareti.

SSU ayrıca daha verimlidir. NTCP daha yüksek ek yüke ve muhtemelen daha yüksek gidiş-dönüş sürelerine sahiptir. NTCP kullanılırken (tunnel çıkışı) / (i2psnark veri çıkışı) oranı en az 3.5 : 1'dir. Kodun SSU'yu tercih edecek şekilde değiştirildiği bir deney yürütülmüş (mevcut kodda i2np.udp.alwaysPreferred yapılandırma seçeneğinin bir etkisi yoktur), oran yaklaşık 3 : 1'e düşerek daha iyi verimlilik göstermiştir.

Streaming lib istatistiklerinin bildirdiğine göre, durumlar oldukça iyileşti - yaşam süresi pencere boyutu 6.3'ten 7.5'e yükseldi, RTT 11.5s'den 10s'ye düştü, ack başına gönderimler 1.11'den 1.07'ye düştü.

Giden mesajların alacağı toplam 3 ila 5 hop'tan yalnızca ilkinin transport'unu değiştirmemize rağmen bunun oldukça etkili olması şaşırtıcıydı.

Giden i2psnark hızları üzerindeki etkisi normal değişimler nedeniyle net değildi. Ayrıca deney için, gelen NTCP devre dışı bırakıldı. i2psnark'ta gelen hızlar üzerindeki etkisi net değildi.

#### Öneriler

1. **1A)** Bu kolay -
   Eğer başka türlü sorunlara yol açmadan yapabilirsek, tüm trafik için SSU'nun tercih edilmesi için teklif önceliklerini ters çevirmeliyiz. Bu, i2np.udp.alwaysPreferred yapılandırma seçeneğinin çalışmasını sağlayacaktır (true veya false olarak).

2. **1B)** 1A)'ya alternatif, o kadar kolay değil -
   Anonimlik hedeflerimizi olumsuz etkilemeden trafiği işaretleyebilirsek,
   streaming-lib tarafından üretilen trafiği tanımlamalı ve SSU'nun bu trafik için düşük bir teklif oluşturmasını sağlamalıyız. Bu etiketin, yönlendiren router'ların da SSU tercihini onurlandırması için mesajla birlikte her hop'ta gitmesi gerekecek.

3. **2)** SSU'yu daha da sınırlandırmak (mevcut maksimum yeniden iletim sayısını 10'dan azaltmak) çökme olasılığını azaltmak için muhtemelen akıllıca olacaktır.

4. **3)** Streaming kütüphanesinin altında yarı-güvenilir bir protokolün faydaları ve zararları konusunda daha fazla çalışmaya ihtiyacımız var. Tek bir hop üzerinden yeniden iletimlerin faydalı ve büyük bir kazanım mı yoksa işe yaramazdan da kötü mü olduğunu araştırmalıyız?
   Yeni bir SUU (güvenli güvenilmez UDP) yapabiliriz ama muhtemelen buna değmez. Streaming-lib trafiğinin hiç yeniden iletilmesini istemiyorsak, belki SSU'da onay-gerekli-değil mesaj türü ekleyebiliriz. Sıkı sınırlandırılmış yeniden iletimler arzu edilir mi?

5. **4)** .28 sürümündeki öncelikli gönderim kodu sadece NTCP için geçerlidir. Şimdiye kadarki testlerim SSU önceliği için fazla bir fayda göstermedi çünkü mesajlar önceliklerin işe yarayacağı kadar uzun süre kuyrukta beklemiyorlar. Ama daha fazla test gerekiyor.

6. **5)** Yeni streaming lib maksimum 45s zaman aşımı muhtemelen hala çok düşük.
   TCP RFC 60s diyor. Muhtemelen alttaki NTCP maksimum zaman aşımından (tahminen 60s) daha kısa olmamalı.

### jrandom tarafından yanıt {#jrandom-response}

Yeni Syndie'ye gönderildi, 2007-03-27

Genel olarak, bununla deneyim yapmaya açığım, ancak NTCP'nin neden orada olduğunu hatırlayın - SSU bir tıkanıklık çöküşünde başarısız oldu. NTCP "sadece çalışır" ve normal tek-hop ağlarında %2-10 yeniden iletim oranları işlenebilirken, bu bize 2 hop tunnel'ları ile %40 yeniden iletim oranı verir. NTCP uygulanmadan önce gördüğümüz ölçülmüş SSU yeniden iletim oranlarından bazılarını (%10-30+) dahil ederseniz, bu bize %83 yeniden iletim oranı verir. Belki de bu oranlar düşük 10 saniyelik zaman aşımından kaynaklanıyordu, ancak bunu bu kadar artırmak bizi zor durumda bırakır (unutmayın, 5 ile çarpın ve yolculuğun yarısını elde edersiniz).

TCP'den farklı olarak, mesajın ulaşıp ulaşmadığını bilmek için tunnel'dan geri bildirim almıyoruz - tunnel seviyesinde onay mekanizması yok. Uçtan uca onaylarımız var, ancak yalnızca az sayıda mesajda (yeni oturum etiketleri dağıttığımızda) - router'ımın gönderdiği 1.553.591 istemci mesajından sadece 145.207'sini onaylamaya çalıştık. Diğerleri sessizce başarısız olmuş ya da mükemmel şekilde başarılı olmuş olabilir.

TCP-over-TCP argümanına bizim durumumuz için ikna olmadım, özellikle de transfer ettiğimiz çeşitli yollara bölündüğü düşünülürse. Tabii ki I2P üzerindeki ölçümler beni aksi yönde ikna edebilir.

> *NTCP maksimum zaman aşımı muhtemelen en az 60 saniyedir, bu da RFC önerisidir. NTCP parametrelerini değiştirmenin veya performansı izlemenin bir yolu yoktur.*

Doğru, ancak ağ bağlantıları yalnızca gerçekten kötü bir şey olduğunda bu seviyeye ulaşır - TCP'deki yeniden iletim zaman aşımı genellikle onlarca veya yüzlerce milisaniye mertebesindedir. foofighter'ın da belirttiği gibi, TCP yığınlarında 20+ yıllık deneyimleri ve hata düzeltmeleri var, ayrıca yaptıkları her neyse ona göre iyi performans gösterecek şekilde donanım ve yazılımı optimize eden milyar dolarlık bir endüstri mevcut.

> *NTCP daha yüksek yüke sahiptir ve muhtemelen daha yüksek gidiş-dönüş sürelerine sahiptir. NTCP kullanırken > (tunnel çıkışı) / (i2psnark veri çıkışı) oranı en az 3.5 : 1'dir. > Kodun SSU'yu tercih edecek şekilde değiştirildiği bir deney yürütüldüğünde (i2np.udp.alwaysPreferred > konfigürasyon seçeneğinin mevcut kodda hiçbir etkisi yoktur), oran > yaklaşık 3 : 1'e düştü, bu da daha iyi verimlilik göstermektedir.*

Bu çok ilginç veriler, bant genişliği verimliliğinden ziyade router tıkanıklığı açısından - 3.5*$n*$NTCPRetransmissionPct ./. 3.0*$n*$SSURetransmissionPct'yi karşılaştırmanız gerekir. Bu veri noktası, router'da zaten aktarılan mesajların aşırı yerel kuyruğa alınmasına neden olan bir şey olduğunu gösteriyor.

> *yaşam süresi pencere boyutu 6.3'ten 7.5'e çıktı, RTT 11.5s'den 10s'ye düştü, ACK başına gönderim 1.11'den 1.07'ye düştü.*

ACK başına gönderim sayısının yalnızca bir örnek olduğunu unutmayın, tam bir sayım değil (çünkü her gönderiyi ACK'lamaya çalışmıyoruz). Bu rastgele bir örnek de değil, bunun yerine hareketsizlik dönemlerini veya ani faaliyet başlangıcını daha yoğun şekilde örnekler - sürekli yük çok fazla ACK gerektirmez.

Bu aralıktaki pencere boyutları AIMD'nin gerçek faydasını elde etmek için hâlâ acıklı derecede düşük ve tek bir 32KB BT parçasını iletmek için hâlâ çok düşük (tabanı 10 veya 12'ye çıkarmak bunu karşılardı).

Yine de, wsize istatistiği umut verici görünüyor - bu ne kadar süre boyunca korundu?

Aslında test amaçları için, apps/ministreaming/java/src/net/i2p/client/streaming/ dizinindeki StreamSinkClient/StreamSinkServer veya hatta TestSwarm'a bakabilirsiniz - StreamSinkClient seçilen bir dosyayı seçilen hedef adrese gönderen bir CLI uygulamasıdır ve StreamSinkServer bir hedef adresi oluşturarak kendisine gönderilen herhangi bir veriyi yazar (boyut ve aktarım süresini gösterir). TestSwarm ikisini birleştirir - bağlandığı herkese rastgele veri yağdırır. Bu size BT choke/send'in aksine streaming lib üzerinden sürekli throughput kapasitesini ölçmek için gereken araçları sağlayacaktır.

> *1A) Bu kolay - > Tüm trafik için SSU'nun tercih edilmesi için bid önceliklerini tersine çevirmeli, eğer bunu başka türlü sorunlara yol açmadan yapabilirsek. Bu, i2np.udp.alwaysPreferred yapılandırma seçeneğini düzeltecek ve çalışmasını sağlayacak (true veya false olarak).*

i2np.udp.alwaysPreferred'ı dikkate almak her durumda iyi bir fikirdir - bu değişikliği commit etmekte çekinmeyin. Ancak tercihleri değiştirmeden önce biraz daha veri toplayalım, çünkü NTCP SSU'nun yarattığı tıkanıklık çöküşüyle başa çıkmak için eklenmişti.

> *1B) 1A)'ya alternatif, o kadar kolay değil - > Anonimlik hedeflerimizi olumsuz etkilemeden trafiği işaretleyebilirsek, > streaming-lib tarafından üretilen trafiği tanımlamalı > ve SSU'nun bu trafik için düşük bir teklif vermesini sağlamalıyız. Bu etiketin her hop boyunca > mesajla birlikte gitmesi gerekecek > böylece yönlendirme yapan router'lar da SSU tercihini onurlandırır.*

Pratikte üç tür trafik vardır - tunnel oluşturma/test etme, netDb sorgu/yanıt ve streaming lib trafiği. Ağ, bu üçünü birbirinden ayırt etmeyi çok zor hale getirecek şekilde tasarlanmıştır.

> *2) SSU'yu daha da sınırlandırmak (mevcut maksimum yeniden iletim sayısını > 10'dan azaltmak) muhtemelen çöküş riskini azaltmak için akıllıca olacaktır.*

10 yeniden iletimde, zaten çok kötü durumdayız, katılıyorum. Taşıma katmanından bakıldığında bir, belki iki yeniden iletim makul, ama karşı taraf ACK göndermek için çok yoğunsa (uygulanan SACK/NACK özelliğiyle bile), yapabileceğimiz pek bir şey yok.

Benim görüşüme göre, temel sorunu gerçekten ele almak için router'ın neden zamanında ACK göndermek için bu kadar tıkanık hale geldiğini ele almamız gerekiyor (bulgularıma göre bunun nedeni CPU çekişmesi). Belki router'ın işlemlerinde bazı şeyleri yeniden düzenleyerek mevcut bir tunnel'ın iletimini yeni bir tunnel isteğinin şifresini çözmekten daha yüksek CPU önceliğine sahip kılabiliriz? Yine de açlık (starvation) durumundan kaçınmak için dikkatli olmamız gerekiyor.

> *3) Streaming kütüphanesinin altında yarı güvenilir bir protokolün faydaları ve zararları konusunda daha fazla çalışmaya ihtiyacımız var. Tek hop üzerindeki yeniden iletimler faydalı mı ve büyük bir kazanım mı yoksa yararsızdan da mı kötü? > Yeni bir SUU (güvenli güvenilmez UDP) yapabiliriz ama muhtemelen buna değmez. Streaming-lib trafiğinde hiç yeniden iletim istemiyorsak belki de SSU'ya ACK-gerektirmeyen bir mesaj türü ekleyebiliriz. Sıkı sınırlı yeniden iletimler arzu edilir mi?*

Araştırılmaya değer - ya SSU'nun yeniden iletimlerini tamamen devre dışı bırakırsak? Bu muhtemelen streaming kütüphanesinin yeniden gönderme oranlarının çok daha yüksek olmasına yol açar, ama belki de açmaz.

> *4) .28'deki öncelik gönderme kodu yalnızca NTCP için. Şu ana kadar yaptığım testler SSU önceliği için fazla bir fayda göstermedi çünkü mesajlar önceliklerin herhangi bir yarar sağlayacağı kadar uzun süre kuyrukta kalmıyor. Ancak daha fazla test gerekli.*

UDPTransport.PRIORITY_LIMITS ve UDPTransport.PRIORITY_WEIGHT (TimedWeightedPriorityMessageQueue tarafından dikkate alınan) bulunuyor, ancak şu anda ağırlıklar neredeyse hepsi eşit, bu yüzden herhangi bir etkisi yok. Bu tabii ki ayarlanabilir (ama bahsettiğiniz gibi, eğer kuyrukta bekleme yoksa, önemi yok).

> *5) Yeni streaming kütüphanesinin 45 saniyelik maksimum zaman aşımı muhtemelen hala çok düşük. TCP RFC 60 saniye diyor. Muhtemelen alttaki NTCP maksimum zaman aşımından (tahminî 60s) daha kısa olmamalı.*

Bu 45 saniye streaming lib'in maksimum yeniden iletim zaman aşımıdır, stream zaman aşımı değil. TCP pratikte çok daha düşük büyüklük mertebesinde yeniden iletim zaman aşımlarına sahiptir, tabii ki açık kablolar veya uydu iletimlerinden geçen bağlantılarda 60 saniyeye kadar çıkabilir ;) Eğer streaming lib yeniden iletim zaman aşımını örneğin 75 saniyeye çıkarırsak, bir web sayfası yüklenmeden önce bira içmeye gidebiliriz (özellikle %98'den az güvenilir bir aktarım varsayıldığında). Bu, NTCP'yi tercih etmemizin nedenlerinden biridir.

### zzz'nin Yanıtı {#zzz-response}

Yeni Syndie'ye gönderildi, 2007-03-31

> *10 yeniden iletimde, zaten büyük dertte olduğumuzu kabul ediyorum. Bir, belki iki > yeniden iletim taşıma katmanından makul, ancak diğer taraf çok sıkışık durumda > ve zamanında ACK gönderemiyor (uygulanan SACK/NACK kapasitesi olsa bile), > yapabileceğimiz pek bir şey yok.* > > *Bence, temel sorunu gerçekten çözmek için router'ın neden zamanında ACK > göndermek için bu kadar sıkışık hale geldiğini ele almamız gerekiyor (bulduğum > kadarıyla, bu CPU çekişmesi nedeniyle). Belki de router'ın işlemesinde bazı > şeyleri ayarlayarak mevcut bir tunnel'ın iletimini yeni bir tunnel isteğinin > şifresini çözmekten daha yüksek CPU önceliğine sahip yapabiliriz? Yine de > açlıktan kaçınmak için dikkatli olmamız gerekiyor.*

Ana istatistik toplama tekniklerimden biri net.i2p.client.streaming.ConnectionPacketHandler=DEBUG'u açmak ve RTT süreleri ile pencere boyutlarını geçerken izlemektir. Bir anlığına genelleme yapacak olursak, yaygın olarak 3 tür bağlantı görmek mümkündür: ~4s RTT, ~10s RTT ve ~30s RTT. 30s RTT bağlantılarını azaltmaya çalışmak hedeftir. CPU çekişmesi nedense belki biraz dengeleme işe yarayabilir.

SSU maksimum yeniden iletim değerini 10'dan düşürmek gerçekten de karanlıkta atılan bir dart gibi çünkü çöküp çökmediğimiz, TCP-over-TCP sorunları yaşayıp yaşamadığımız veya başka ne olduğu konusunda iyi verimiz yok, bu yüzden daha fazla veriye ihtiyaç var.

> *Araştırmaya değer - SSU'nun yeniden iletimlerini devre dışı bıraksak ne olur? Muhtemelen çok daha yüksek streaming lib yeniden gönderim oranlarına yol açar, ama belki de açmaz.*

Anlamadığım ve detaylandırabilirseniz memnun olurum nokta, streaming-lib olmayan trafik için SSU yeniden iletimlerin faydaları nelerdir. Tunnel mesajlarının (örneğin) yarı-güvenilir bir aktarım kullanması gerekiyor mu yoksa güvenilmez veya kısmen-güvenilir bir aktarım (örneğin maksimum 1 veya 2 yeniden iletim) kullanabilirler mi? Başka bir deyişle, neden yarı-güvenilirlik?

> *(ama belirttiğiniz gibi, kuyruk yoksa, önemli değil).*

UDP için öncelikli gönderim uyguladım ancak NTCP tarafındaki koda göre yaklaşık 100.000 kat daha az devreye girdi. Belki bu daha fazla araştırma için bir ipucu veya ima - NTCP'de neden çok daha sık yedekleme olduğunu anlamıyorum, ama belki bu NTCP'nin neden daha kötü performans gösterdiğine dair bir ipucu.

### jrandom tarafından yanıtlanan soru {#jrandom-followup}

Yeni Syndie'ye gönderildi, 2007-03-31

> *NTCP uygulanmadan önce gördüğümüz ölçülmüş SSU yeniden iletim oranları > (10-30+%)* > > router'ın kendisi bunu ölçebilir mi? Eğer öyleyse, ölçülen performansa > dayalı olarak bir transport seçilebilir mi? (yani bir eş ile olan SSU bağlantısı > mantıksız sayıda mesajı düşürüyorsa, o eş'e gönderirken NTCP tercih edilsin)

Evet, şu anda bu istatistiği basit bir MTU algılama yöntemi olarak kullanıyor (yeniden iletim oranı yüksekse küçük paket boyutunu kullanır, ama düşükse büyük paket boyutunu kullanır). NTCP'yi ilk tanıttığımızda (ve orijinal TCP aktarımından uzaklaştığımızda) SSU'yu tercih eden ama o aktarımın bir peer için kolayca başarısız olmasına neden olan ve NTCP'ye geri dönmesini sağlayan birkaç şey denedik. Ancak, bu konuda kesinlikle daha fazla şey yapılabilir, ancak hızla karmaşıklaşıyor (tekliflerin nasıl/ne zaman ayarlanacağı/sıfırlanacağı, bu tercihlerin birden fazla peer arasında paylaşılıp paylaşılmayacağı, aynı peer ile birden fazla oturum arasında paylaşılıp paylaşılmayacağı (ve ne kadar süreyle), vb.).

### foofighter tarafından yanıt {#foofighter}

Yeni Syndie'ye gönderildi, 2007-03-26

Eğer her şeyi doğru anladıysam, TCP'nin (genel olarak, hem eski hem de yeni çeşidin) lehindeki temel neden, iyi bir TCP stack'i kodlama konusunda endişelenmemeniz gerektiğiydi. Bu doğru yapmak imkansız derecede zor değil... sadece mevcut TCP stack'lerinin 20 yıllık bir önlüğü var.

Bildiğim kadarıyla, TCP ile UDP arasındaki tercih konusunda aşağıdaki değerlendirmeler dışında pek derin bir teorik çalışma yapılmamıştır:

- Yalnızca TCP kullanan bir ağ, erişilebilir eşlere (NAT'ları üzerinden gelen bağlantıları yönlendirebilen) oldukça bağımlıdır
- Erişilebilir eşler nadir olsa bile, onların yüksek kapasiteli olması topolojik kıtlık sorunlarını bir ölçüde hafifletir
- UDP "NAT hole punching" tekniğine izin verir, bu da aksi takdirde sadece dışarıya bağlanabilen kişilerin (introducer'ların yardımıyla) "bir nevi sahte-erişilebilir" olmalarını sağlar
- "Eski" TCP transport uygulaması çok fazla thread gerektiriyordu ve bu performans katiliydi, "yeni" TCP transport ise az thread ile iyi çalışır
- A kümesi router'ları UDP ile doyurulduğunda çökerler. B kümesi router'ları TCP ile doyurulduğunda çökerler.
- A'nın B'den daha yaygın olarak dağıtıldığı "hissediliyor" (yani bazı belirtiler var ama bilimsel veri veya kaliteli istatistik yok)
- Bazı ağlar DNS olmayan UDP datagramlarını tamamen kötü kalitede taşırken, TCP akışlarını taşımak için hâlâ bir ölçüde zahmet ederler.

Bu arka plan göz önünde bulundurulduğunda, küçük bir transport çeşitliliği (ihtiyaç olduğu kadar, ancak daha fazla değil) her iki durumda da mantıklı görünüyor. Ana transport hangisi olmalı, bunun performans açısından değerlendirilmesine bağlı. UDP ile tam kapasitesini kullanmaya çalıştığımda hattımda kötü şeyler gördüm. %35 seviyesinde paket kayıpları.

UDP ve TCP öncelikleri ile oynamayı kesinlikle deneyebiliriz, ancak bu konuda dikkatli olunmasını tavsiye ediyorum. Bunların aynı anda çok radikal şekilde değiştirilmemesini tavsiye ediyorum, çünkü bu durumda işler bozulabilir.

### zzz tarafından cevap (foofighter'a) {#zzz-foofighter}

Yeni Syndie'ye gönderildi, 2007-03-27

> *Bildiğim kadarıyla, TCP'ye karşı UDP tercihi konusunda aşağıdaki hususlar dışında çok derin bir teori ortaya konulmamıştır:*

Bunların hepsi geçerli konular. Ancak iki protokolü yalıtılmış olarak değerlendiriyorsunuz, belirli bir üst düzey protokol için hangi taşıma protokolünün en iyi olduğunu düşünmek yerine (yani streaming lib olsun ya da olmasın).

Söylediğim şu ki streaming kütüphanesini dikkate almanız gerekiyor.

Bu nedenle ya herkesin tercihlerini değiştirin ya da streaming kütüphanesi trafiğini farklı şekilde ele alın.

İşte 1B) önerim bundan bahsediyor - streaming-lib trafiği için streaming-lib olmayan trafikten (örneğin tunnel yapı mesajları) farklı bir tercih belirlemek.

> *Bu bağlamda, küçük bir transport çeşitliliği (ihtiyaç kadar, ancak fazla > olmayacak şekilde) her iki durumda da mantıklı görünüyor. Hangisinin ana transport > olması gerektiği, performanslarına bağlı. UDP ile tam kapasitesini kullanmaya > çalıştığımda hattımda çirkin şeyler gördüm. %35 seviyesinde paket kayıpları.*

Katılıyorum. Yeni .28 sürümü UDP üzerinden paket kaybı konusunda işleri iyileştirmiş olabilir, ya da olmayabilir.

Önemli bir nokta - transport kodu bir transport'un başarısızlıklarını hatırlar. Bu nedenle UDP tercih edilen transport ise, önce onu dener, ancak belirli bir hedef için başarısız olursa, o hedef için bir sonraki denemede UDP'yi tekrar denemek yerine NTCP'yi dener.

> *UDP ve TCP önceliklerini oynayarak deneyebiliriz kesinlikle, ancak bu konuda dikkatli olmayı öneriyorum. Bunların hepsini bir anda çok radikal şekilde değiştirmemeleri gerektiğini öneriyorum, yoksa bazı şeyleri bozabilir.*

Dört ayar düğmemiz var - dört teklif değeri (SSU ve NTCP için, zaten bağlı olan ve henüz bağlı olmayan). Örneğin, SSU'yu NTCP'ye tercih edilir hale getirebiliriz ancak yalnızca her ikisi de bağlıysa, fakat hiçbir taşıma protokolü bağlı değilse önce NTCP'yi deneyebiliriz.

Bunu kademeli olarak yapmanın diğer yolu sadece streaming lib trafiğini kaydırmaktır (1B önerisi), ancak bu zor olabilir ve anonimlik açısından etkileri olabilir, bilmiyorum. Ya da trafiği sadece ilk giden atlama için kaydırmak (yani bayrağı bir sonraki router'a yaymamak), bu size sadece kısmi fayda sağlar ancak daha anonim ve daha kolay olabilir.

## Tartışmanın Sonuçları {#results}

... ve aynı zaman dilimindeki (2007) diğer ilgili değişiklikler:

- Streaming lib parametrelerinin önemli ayarlaması,
  giden performansı büyük ölçüde artıran, 0.6.1.28'de uygulandı
- NTCP için öncelikli gönderim 0.6.1.28'de uygulandı
- SSU için öncelikli gönderim zzz tarafından uygulandı ancak hiç kontrol edilmedi
- Gelişmiş transport teklif kontrolü
  i2np.udp.preferred 0.6.1.29'da uygulandı.
- NTCP için pushback 0.6.1.30'da uygulandı, anonimlik endişeleri nedeniyle 0.6.1.31'de devre dışı bırakıldı,
  ve bu endişeleri gidermek için iyileştirmelerle birlikte 0.6.1.32'de yeniden etkinleştirildi.
- zzz'nin 1-5 önerilerinin hiçbiri uygulanmadı.
