---
title: "I2P önerisi #166: Kimlik/Host Farkındalığı Olan Tünel Türleri"
number: "166"
author: "eyedeekay"
created: "2024-05-27"
lastupdated: "2024-08-27"
status: "Open"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.65"
toc: true
---

### Host Farkındalığı Olan HTTP Proxy Tünel Türü Önerisi

Bu, geleneksel HTTP-over-I2P kullanımında "Paylaşılan Kimlik Problemi"ni çözmek için yeni bir HTTP proxy tünel türü tanıtan bir öneridir. Bu tünel türü, potansiyel düşman gizli hizmet operatörleri tarafından hedeflenen kullanıcı ajanları (tarayıcılar) ve I2P İstemci Uygulaması'na karşı yürütülen izlemeyi önleme veya sınırlandırma amacı taşıyan ek davranışlar içerir.

#### "Paylaşılan Kimlik" problemi nedir?

"Paylaşılan Kimlik" problemi, kriptografik adreslenmiş bir üst ağında bir kullanıcı ajanının başka bir kullanıcı ajanıyla kriptografik bir kimlik paylaşması durumunda ortaya çıkar. Bu durum örneğin, Firefox ve GNU Wget'in aynı HTTP Proxy kullanacak şekilde yapılandırılması durumunda meydana gelir.

Bu senaryoda, sunucu faaliyetlere yanıt vermek için kullanılan kriptografik adresi (Hedef) toplamak ve depolamak mümkün olabilir. Bu adres, kriptografik kökenli olduğu için her zaman %100 benzersiz olan bir "Parmak İzi" olarak kabul edilebilir. Bu, Paylaşılan Kimlik probleminin gözlemlenen bağlantılılığının mükemmel olduğu anlamına gelir.

Ama bu bir problem mi?
^^^^^^^^^^^^^^^^^^^^^^

Paylaşılan kimlik problemi, aynı protokolü konuşan kullanıcı ajanları bağlantısızlığı istediklerinde bir problem olur. [Bu konu ilk olarak HTTP bağlamında şu Reddit
Konu Başlığı](https://old.reddit.com/r/i2p/comments/579idi/warning_i2p_is_linkablefingerprintable/), ve silinmiş yorumlar
[pullpush.io](https://api.pullpush.io/reddit/search/comment/?link_id=579idi) aracılığıyla erişilebilir.
*O dönemde* en aktif cevap verenlerden biriydim ve *o dönemde* bu konunun küçük olduğunu düşündüm. Geçen 8 yıl içinde, durum ve bu konudaki görüşüm değişti, şimdi kötü niyetli hedef korelasyon tehdidinin, daha fazla site kullanıcılara
özgü profiller oluşturmaya meyilli hale geldikçe, önemli ölçüde büyüdüğüne inanıyorum.

Bu saldırının engeli oldukça düşüktür. Tek gereken, bir gizli hizmet operatörünün birden fazla hizmet işletmesidir. Aynı anda yapılan ziyaretlere yönelik saldırılar için bu tek gerekliliktir. Farklı zamanlardaki bağlama gelince,
bu hizmetlerden birinin, izlenen tek bir kullanıcıya ait "hesaplar" barındıran bir hizmet olması gereklidir.

Şu anda, kullanıcı hesaplarını barındıran herhangi bir hizmet operatörü, Paylaşılan Kimlik problemini kullanarak kontrol ettikleri herhangi bir site üzerinden bu hesapları yakalayabilir.
Mastodon, Gitlab veya basit forumlar bile birden fazla hizmet işletip, kullanıcı için profil oluşturmak isteyen bir tehlike olarak saldırgan kılığına girebilir. Bu izleme, takip, finansal kazanç veya
istihbaratla ilgili nedenlerden dolayı gerçekleştirilebilir. Şu anda, bu saldırıyı yapabilecek ve anlamlı veri elde edebilecek onlarca büyük operatör bulunmaktadır. Şu an için onlara güveniyoruz ancak bizim fikirlerimizi umursamayan oyuncular kolayca ortaya çıkabilir.

Bu, şirketlerin kendi sitelerindeki etkileşimleri kontrol ettikleri ağlarla ilişkilendirebileceği, çıplak ağda oldukça temel bir profil oluşturma tekniği ile doğrudan ilgilidir. I2P'de, kriptografik hedef benzersiz olduğu için,
bu teknik bazen daha güvenilir olabilir, coğrafi konum belirleme gücü olmaksızın.

Paylaşılan Kimlik sadece coğrafi konumu gizlemek için I2P'yi kullanan bir kullanıcıya karşı faydalı değildir. Aynı zamanda I2P'nin yönlendirmesini bozmak için kullanılamaz.
Bu sadece bağlamsal kimlik yönetimi meselesidir.

-  Paylaşılan kimlik problemini kullanarak bir I2P kullanıcısını coğrafi olarak konumlandırmak imkansızdır.
-  Eş zamanlı olmayan I2P oturumlarını bağlamak Paylaşılan Kimlik problemi kullanılarak imkansızdır.

Ancak, muhtemelen çok yaygın olan koşullarda bir I2P kullanıcısının anonimliğini azaltmak için kullanılabilir.
Bunun yaygın olmasının bir nedeni, "Sekmeli" işlemeyi destekleyen bir web tarayıcısı olan Firefox'un kullanılmasını teşvik etmemizdir.

-  *Her zaman* üçüncü taraf kaynakları istemeyi destekleyen *herhangi* bir web tarayıcısındaki Paylaşılan Kimlik problemi sorununu kullanarak bir parmak izi oluşturmak mümkündür.
-  Javascript'in devre dışı bırakılması, Paylaşılan Kimlik problemi ile **hiçbir şey** başaramaz.
-  Eş zamanlı olmayan oturumlar arasında, "geleneksel" tarayıcı parmak izi ile bir bağlantı kurulabilirse, Paylaşılan Kimlik problemi geçişli olarak uygulanabilir, potansiyel olarak eş zamanlı olmayan bir bağlantı stratejisi mümkün kılınır.
-  Bir I2P kimliği ve bir açık ağ etkinliği arasında bir bağlantı kurulabilirse, örneğin hedef hem bir I2P hem de bir açık ağ varlığına giriş yapmışsa, Paylaşılan Kimlik problemi geçişli olarak uygulanabilir ve bu da potansiyel olarak tamamen
   de-anonimleştirmeyi etkinleştirebilir.

I2P HTTP proxy'sine uygulanan Paylaşılan Kimlik probleminin ciddiyetini nasıl gördüğünüz, "kullanıcının" (ya da daha doğrusu, potansiyel olarak bilgisiz beklentilere sahip bir "kullanıcının") uygulama için "bağlamsal kimliğin" nerede olduğunu düşündüğüne bağlıdır.
Birkaç olasılık vardır:

1. HTTP hem Uygulama hem de Bağlamsal Kimliktir - Bu şu anda nasıl çalıştığıdır. Tüm HTTP Uygulamaları bir kimliği paylaşır.
2. İşlem Uygulama ve Bağlamsal Kimliktir - Bir uygulama kendi kimliğini oluşturduğu ve yaşam süresini kontrol ettiği SAMv3 veya I2CP gibi bir API kullandığında bu şekilde çalışır.
3. HTTP Uygulama'dır, ancak Host Bağlamsal Kimliktir - Bu, her Host'u potansiyel bir "Web Uygulaması" olarak ele alan ve tehdit yüzeyini buna göre ele alan bu önerinin amacıdır.

Çözülebilir mi?
^^^^^^^^^^^^^^^

Muhtemelen, çalışma şeklinin bir uygulamanın anonimliğini zayıflatabileceği her olası duruma akıllıca yanıt veren bir proxy yapmak mümkün değildir. Ancak, belirli bir uygulamayı tahmin edilebilir bir şekilde davranan bir proxy yapmak mümkündür.
Örneğin, modern Web Tarayıcılarında, kullanıcıların birden çok sekme açması beklenir ve burada birden fazla web sitesi ile etkileşimde bulunacaklar, ki bu da hostname ile ayırt edilecektir.

Bu, HTTP Proxy'sinin bu tür bir HTTP kullanıcı ajanı için davranışını kullanıcı-ajanının davranışıyla eşleştirerek iyileştirmemize olanak tanır ve HTTP Proxy'si ile kullanıldığında her host'a kendi Hedefini verir. Bu değişiklik, iki host
arasında istemci etkinliğini ilişkilendirmek için kullanabilecek bir parmak izi türetmek için Paylaşılan Kimlik problemini kullanmayı imkansız kılar, çünkü iki host artık bir geri dönüş kimliği paylaşmayacaktır.

Açıklama:
^^^^^^^^^^^^

Yeni bir HTTP Proxy oluşturulacak ve Gizli Hizmetler
Yöneticisi'ne (I2PTunnel) eklenecektir. Yeni HTTP Proxy, I2PSocketManager'ların bir "çoklayıcısı" olarak çalışacaktır. Çoklayıcı'nın kendisinin bir hedefi yoktur. Çoklayıcıya dahil olan her bir bireysel I2PSocketManager'ın kendi yerel hedefi ve kendi tünel havuzu vardır.
I2PSocketManager'lar, çoklayıcı tarafından ihtiyaç doğrultusunda oluşturulur, burada "ihtiyacı" yeni host'a yapılan ilk ziyaret belirler. I2PSocketManager'ların oluşumunu, çoklayıcıya eklemeden önce bir veya daha fazlasını önceden oluşturarak optimize etmek mümkündür.
Bu performansı artırabilir.

Kendi hedefi olan ek bir I2PSocketManager, bir I2P Hedefine *sahip olmayan* herhangi bir site için, örneğin herhangi bir Clearnet sitesi için bir "Dış Erişim Proxy'si"nin taşıyıcısı olarak ayarlanır. Bu, tüm Dış Erişim Proxy'si kullanımını etkili bir şekilde tek bir Bağlamsal Kimlik yapar, 
tek fark, tünel için birden fazla Dış Erişim Proxy'si yapılandırmanın normal "Yapışkan" dış erişim rotasyonuna neden olmasıdır; burada her bir dış erişim yalnızca tek bir site için talepler alır. Bu, açık internet üzerinde
destination tarafından izole edilen HTTP-over-I2P proxy'leri olarak *neredeyse* eşdeğer bir davranıştır.

Kaynak Düşünceleri:
''''''''''''''''''''''''

Yeni HTTP proxy, mevcut HTTP proxy'den daha fazla kaynak gerektirir. Şunları yapacaktır:

-  Potansiyel olarak daha fazla tünel ve I2PSocketManager oluşturmak
-  Tünelleri daha sık oluşturmak

Her biri şunları gerektirir:

-  Yerel bilgisayar kaynakları
-  Eşlerden ağ kaynakları

Ayarlar:
'''''''''

Artan kaynak kullanımının etkisini en aza indirmek için proxy mümkün olduğunca az yer kullanacak şekilde yapılandırılmalıdır. Çoklayıcının bir parçası olan proxy'ler (ebeveyn proxy değil) aşağıdaki şekilde yapılandırılmalıdır:

-  Çoklanmış I2PSocketManager'lar, tünel havuzlarında içeri 1 tünel, dışarı 1 tünel oluşturur
-  Çoklanmış I2PSocketManager'lar varsayılan olarak 3 atlayış gerçekleştirir.
-  10 dakika süreyle hiçbir etkinlik olmaması durumunda soketleri kapatır
-  Çoklayıcı tarafından başlatılan I2PSocketManager'lar, Çoklayıcı'nın ömrünü paylaşır. Çoklanmış tüneller ebeveyn Çoklayıcı yok edilene kadar "Yıkılmaz".

Diyagramlar:
^^^^^^^^^

Aşağıdaki diyagram, HTTP proxy'sinin mevcut işleyişini temsil etmektedir ki bu, "Bir Problem mi?" bölümündeki “Olasılık 1.” ile örtüşmektedir. 
Görüldüğü gibi, HTTP proxy yalnızca bir hedef kullanarak doğrudan I2P siteleri ile etkileşime girmektedir.
Bu senaryoda, HTTP hem uygulama hem de bağlamsal kimliktir.

```text
**Mevcut Durum: HTTP Uygulama, HTTP Bağlamsal Kimliktir**
                                                          __-> Dış Erişim Proxy -> i2pgit.org
                                                         /
   Tarayıcı <-> HTTP Proxy (bir Hedef)<-> I2PSocketManager <---> idk.i2p
                                                         \__-> translate.idk.i2p
                                                          \__-> git.idk.i2p
```

Aşağıdaki diyagram, host farkındalığı olan bir HTTP proxy'sinin işleyişini temsil etmektedir ki bu, "Bir Problem mi?" bölümündeki “Olasılık 3.” ile örtüşmektedir. 
Bu senaryoda, HTTP uygulamadır, ancak Host bağlamsal kimliği tanımlar ve her I2P sitesi, host başına benzersiz bir hedefe sahip farklı bir HTTP proxy ile etkileşimde bulunur. 
Bu, aynı kişinin ziyaret ettiği birden fazla siteyi işleten operatörlerin, ziyaret edilen siteleri ayırt edememelerini engeller.

```text
**Değişiklik Sonrası: HTTP Uygulama, Host Bağlamsal Kimliktir**
                                                        __-> I2PSocketManager (Hedef A - Yalnızca Dış Erişimler) <--> i2pgit.org
                                                       /
   Tarayıcı <-> HTTP Proxy Çoklayıcı (Hedef Yok) <---> I2PSocketManager (Hedef B) <--> idk.i2p
                                                       \__-> I2PSocketManager (Hedef C) <--> translate.idk.i2p
                                                        \__-> I2PSocketManager (Hedef D) <--> git.idk.i2p
```

Durum:
^^^^^^^

Bu önerinin eski bir versiyonuna uygun çalışan bir Java uygulaması, idk'nın çatalında `i2p.i2p.2.6.0-browser-proxy-post-keepalive` dalında mevcuttur. 
Değişiklikleri daha küçük bölümlere ayırmak için yoğun bir şekilde revize edilmektedir.

Farklı yeteneklere sahip uygulamalar, SAMv3 kitaplığı kullanılarak Go dilinde yazıldı, bu uygulamalar diğer Go uygulamalarına gömülmek için veya go-i2p için yararlı olabilir
ancak Java I2P için uygun değildir. Ayrıca, şifreli leaseSet'ler ile etkileşimde iyi destekten yoksundur.

Ek: ``i2psocks``
                      

Yeni bir tünel türü uygulamadan veya mevcut I2P kodunu değiştirmeden, zaten yaygın olarak erişilebilir ve gizlilik topluluğunda test edilen I2PTunnel mevcut araçlarını birleştirerek
diğer türdeki istemcileri izole edebilmek için basit bir uygulama tabanlı yaklaşım mümkündür. Ancak, bu yaklaşım HTTP ve diğer birçok potansiyel I2P istemcisi için geçerli olmayan zorlu bir varsayım yapar.

Kabaca, aşağıdaki script, uygulama farkındalığına sahip bir SOCKS5 proxy üretir ve alttaki işlemi socksify yapar:

```sh
#! /bin/sh
proxy_yapılacak_komut="$@"
java -jar ~/i2p/lib/i2ptunnel.jar -wait -e 'sockstunnel 7695'
torsocks --port 7695 $proxy_yapılacak_komut
```

Ek: ``saldırının örnek uygulaması``
                                                  

[HTTP Kullanıcı-Ajanlarına yönelik Paylaşılan Kimlik saldırısının
bir örnek uygulaması](https://github.com/eyedeekay/colluding_sites_attack/)
birkaç yıl önce oluşturulmuştur. Ek bir örnek ``simple-colluder`` alt dizininde mevcuttur
[idk’nın prop166 deposunda](https://git.idk.i2p/idk/i2p.host-aware-proxy) Bu
örnekler, saldırının çalıştığını göstermek üzere kasıtlı olarak tasarlanmıştır ve
gerçek bir saldırıya dönüştürülmesi için modifikasyon(albeit minor) gereklidir.

