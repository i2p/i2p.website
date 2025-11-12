---
title: "I2P'yi İndir"
description: "Windows, macOS, Linux, Android ve daha fazlası için I2P'nin en son sürümünü indirin"
type: "indirilenler"
layout: "downloads"
current_version: "2.10.0"
android_version: "2.10.1"
downloads: I2P, kullanıcıların internet üzerinde anonim olarak iletişim kurmasını sağlayan bir gizlilik ağıdır. I2P ağı, kullanıcıların kimliklerini gizleyerek güvenli ve özel bir iletişim sağlar. Bu, özellikle sansürden kaçınmak veya gizliliği korumak isteyen kullanıcılar için önemlidir.

## I2P Nasıl Çalışır?

I2P, verileri "tüneller" aracılığıyla yönlendirerek çalışır. Her kullanıcı, verilerini göndermek ve almak için kendi tünellerini oluşturur. Bu tüneller, verilerin birkaç farklı yönlendirici üzerinden geçmesini sağlayarak izlenmeyi zorlaştırır. Ayrıca, I2P ağı "garlic encryption" kullanarak verilerin güvenliğini artırır.

### I2P'nin Temel Bileşenleri

- **Router**: I2P ağının temel yapı taşıdır. Verileri tüneller arasında yönlendirir.
- **Tunnel**: Verilerin gönderildiği ve alındığı sanal yollar.
- **LeaseSet**: Bir kullanıcının tünel bilgilerini içeren veri yapısı.
- **NetDb**: Ağ veritabanı, yönlendirici ve tünel bilgilerini saklar.
- **Floodfill**: Ağın veritabanını güncel tutan özel yönlendiriciler.

### I2P Kullanmanın Avantajları

- **Anonimlik**: Kullanıcıların kimliklerini gizler.
- **Güvenlik**: Veriler "garlic encryption" ile korunur.
- **Özgürlük**: Sansürden kaçınmayı sağlar.

I2P, internet gizliliği ve güvenliği konusunda güçlü bir araçtır. Kullanıcılar, I2P'nin sunduğu anonimlik ve güvenlik özelliklerinden yararlanarak daha güvenli bir çevrimiçi deneyim yaşayabilirler.
windows: ### I2P Router Configuration

I2P router'ınızı yapılandırmak, ağ performansını ve güvenliğini optimize etmek için önemlidir. Aşağıda, temel yapılandırma adımlarını bulabilirsiniz:

1. **Router Konsolu**: I2P router'ınızın web tabanlı yönetim arayüzüne erişmek için `http://127.0.0.1:7657` adresini kullanın. Burada, router durumunu izleyebilir ve ayarları değiştirebilirsiniz.

2. **Tünel Yönetimi**: Tüneller, I2P ağında veri iletimi için kullanılır. Yeni bir tünel oluşturmak veya mevcut tünelleri yönetmek için "Tünel Yapılandırması" bölümüne gidin.

3. **Güvenlik Ayarları**: Router'ınızın güvenliğini artırmak için güçlü bir parola belirleyin ve mümkünse iki faktörlü kimlik doğrulama kullanın.

4. **Ağ Ayarları**: Bağlantı türünüzü (örneğin, NTCP2 veya SSU) ve bant genişliği sınırlarını yapılandırarak ağ performansını optimize edin.

5. **Yedekleme ve Geri Yükleme**: Router yapılandırmalarınızı düzenli olarak yedekleyin. Bu, veri kaybı durumunda hızlı bir geri yükleme yapmanıza olanak tanır.

Daha fazla bilgi için [I2P Resmi Belgeleri](https://geti2p.net) adresini ziyaret edin.
file: "i2pinstall_2.10.0-0_windows.exe"
size: "~24M"
requirements: "Java gerekli"
sha256: "f96110b00c28591691d409bd2f1768b7906b80da5cab2e20ddc060cbb4389fbf"
links: I2P, kullanıcıların internette anonim olarak gezinmelerine olanak tanıyan bir gizlilik ağıdır. I2P, kullanıcıların kimliklerini gizleyerek, çevrimiçi etkinliklerini izlenemez hale getirir. Bu, özellikle sansürden kaçınmak veya gizliliklerini korumak isteyen kullanıcılar için faydalıdır.

## I2P Nasıl Çalışır?

I2P, kullanıcıların verilerini "tüneller" aracılığıyla yönlendirir. Her tünel, verilerin şifrelenmiş bir şekilde bir dizi "router" üzerinden geçmesini sağlar. Bu süreç, verilerin kaynağını ve hedefini gizler.

### Temel Bileşenler

- **Router**: I2P ağında veri paketlerini yönlendiren cihaz veya yazılım.
- **Tunnel**: Verilerin şifrelenmiş bir şekilde yönlendirildiği yol.
- **LeaseSet**: Bir kullanıcının I2P ağında erişilebilir olduğu tünellerin listesi.
- **NetDb**: I2P ağındaki router'ların ve diğer bileşenlerin bilgilerini depolayan dağıtılmış veritabanı.
- **Floodfill**: NetDb'yi güncel tutmak için verileri diğer router'lara yayma işlemi.

### İletişim Protokolleri

I2P, çeşitli iletişim protokollerini destekler. Bunlar arasında NTCP2 ve SSU bulunur. NTCP2, TCP üzerinden güvenli iletişim sağlarken, SSU UDP üzerinden çalışır ve daha düşük gecikme süresi sunar.

### Uygulamalar ve Araçlar

I2P, çeşitli uygulamaları ve araçları destekler. Örneğin, **I2PTunnel** kullanıcıların HTTP ve diğer protokoller üzerinden anonim olarak iletişim kurmasına olanak tanır. **SAMv3** ve **I2CP**, geliştiricilerin I2P ağı ile etkileşimde bulunmasını sağlayan API'lerdir.

### Eepsite'lar

Eepsite'lar, I2P ağı üzerinde barındırılan web siteleridir. Bu siteler, kullanıcıların kimliklerini gizleyerek güvenli bir şekilde bilgi paylaşmasına olanak tanır. Eepsite'lar, I2P'nin sağladığı garlic encryption (sarımsak şifreleme) ile korunur.
primary: "https://i2p.net/files/2.10.0/i2pinstall_2.10.0-0_windows.exe"
mirror: "https://mirror.stormycloud.org/2.10.0/i2pinstall_2.10.0-0_windows.exe"
torrent: "magnet:?xt=urn:btih:75d8c74e9cc52f5cb4982b941d7e49f9f890c458&dn=i2pinstall_2.10.0-0_windows.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0-0_windows.exe"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0-0_windows.exe"
windows_easy_installer: I2P, kullanıcıların internet üzerinde anonim olarak iletişim kurmalarını sağlayan bir gizlilik ağıdır. I2P, kullanıcıların kimliklerini ve konumlarını gizleyerek güvenli ve özel bir iletişim sağlar. 

## I2P Nasıl Çalışır?

I2P, verileri "tüneller" aracılığıyla yönlendirir. Her kullanıcı, gelen ve giden trafiği için kendi tünellerini oluşturur. Bu tüneller, verilerin bir dizi router üzerinden geçmesini sağlar ve böylece kaynak ve hedef arasında doğrudan bir bağlantı kurulmaz. Bu yöntem, kullanıcıların kimliklerini gizler ve izlenmelerini zorlaştırır.

### I2P'nin Temel Bileşenleri

- **Router**: I2P ağına bağlı her cihaz bir router'dır. Router'lar, verileri tüneller aracılığıyla iletir.
- **Tunnel**: Verilerin yönlendirildiği sanal yollar. Her kullanıcı, anonim kalmak için kendi tünellerini oluşturur.
- **LeaseSet**: Bir kullanıcının tünel yapılandırmasını ve iletişim bilgilerini içeren veri yapısı.
- **NetDb**: Router'ların ve tünellerin bilgilerini depolayan dağıtılmış veritabanı.

### İletişim Protokolleri

I2P, farklı iletişim protokollerini destekler:

- **NTCP2**: TCP tabanlı bir protokol, güvenli ve kararlı bağlantılar sağlar.
- **SSU**: UDP tabanlı bir protokol, düşük gecikme süresi ve yüksek performans sunar.
- **SAMv3**: Uygulamaların I2P ağı ile etkileşime girmesini sağlayan bir API.
- **I2PTunnel**: HTTP ve diğer protokoller için tünel hizmetleri sunar.

I2P, kullanıcıların internet üzerinde daha güvenli ve özel bir şekilde gezinmelerine olanak tanır. Anonimlik ve gizlilik arayanlar için güçlü bir araçtır.
file: "I2P-Kolay-Kurulum-Paketi-2.10.0-imzalı.exe"
size: "~162M"
requirements: "Java gerekmez - Java çalışma zamanı içerir"
sha256: "afcc937004bcf41d4dd2e40de27f33afac3de0652705aef904834fd18afed4b6"
beta: doğru
links: I2P, kullanıcıların internet üzerinde anonim olarak iletişim kurmasına olanak tanıyan bir gizlilik ağıdır. Kullanıcılar, I2P ağı üzerinden veri gönderip alırken kimliklerini gizli tutabilirler. Bu, özellikle sansürden kaçınmak veya gizliliklerini korumak isteyenler için faydalıdır.

## I2P Nasıl Çalışır?

I2P, kullanıcıların verilerini bir dizi şifreli tünel üzerinden yönlendirerek çalışır. Her kullanıcı, verilerini göndermek ve almak için kendi tünellerini oluşturur. Bu tüneller, kullanıcıların kimliklerini gizli tutar ve verilerin güvenli bir şekilde iletilmesini sağlar.

### Router ve Tunnel

I2P ağında, her kullanıcı bir "router" çalıştırır. Router, verileri şifreler ve tüneller üzerinden gönderir. Tüneller, verilerin yönlendirildiği sanal yollar gibidir. Her tünel, bir dizi "hop" içerir ve her hop, verileri bir sonraki hop'a iletir.

### LeaseSet ve netDb

Bir kullanıcı bir tünel oluşturduğunda, bu tünelin bilgileri bir "leaseSet" içinde saklanır. LeaseSet, tünelin nasıl erişileceğini tanımlar ve "netDb" (ağ veritabanı) içinde depolanır. NetDb, tüm I2P ağındaki tünel bilgilerini saklayan dağıtılmış bir veritabanıdır.

### Floodfill Router

Floodfill router'lar, netDb'yi güncel tutmak için özel bir rol oynar. Bu router'lar, leaseSet bilgilerini diğer router'lara yayar ve ağın verimli çalışmasını sağlar.

## I2P'nin Avantajları

- **Anonimlik**: I2P, kullanıcıların kimliklerini gizli tutarak anonim iletişim sağlar.
- **Güvenlik**: Veriler, tüneller üzerinden şifrelenerek iletilir, bu da güvenliği artırır.
- **Sansür Direnci**: I2P, kullanıcıların sansürden kaçınmasına yardımcı olur.

I2P, internet gizliliği ve güvenliği konusunda güçlü bir araçtır. Kullanıcılar, bu ağı kullanarak çevrimiçi etkinliklerini gizli tutabilir ve sansürden kaçınabilirler.
primary: "https://i2p.net/files/2.10.0/I2P-Kolay-Kurulum-Paketi-2.10.0-imzalı.exe"
mirror: "https://mirror.stormycloud.org/2.10.0/I2P-Kolay-Kurulum-Paketi-2.10.0-imzalı.exe"
torrent: "magnet:?xt=urn:btih:79e1172aaa21e5bd395a408850de17eff1c5ec24&dn=I2P-Easy-Install-Bundle-2.10.0-signed.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/I2P-Kolay-Kurulum-Paketi-2.10.0-imzalı.exe"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/I2P-Kolay-Kurulum-Paketi-2.10.0-imzalı.exe"
mac_linux: I2P, kullanıcıların internet üzerinde anonim kalmalarını sağlayan bir gizlilik ağıdır. I2P, kullanıcıların kimliklerini ve konumlarını gizleyerek güvenli iletişim kurmalarına olanak tanır. Bu, özellikle sansürden kaçınmak veya gizliliği korumak isteyenler için önemlidir.

## I2P Nasıl Çalışır?

I2P, verileri "tüneller" aracılığıyla yönlendirerek çalışır. Her kullanıcı, verilerini göndermek ve almak için bir dizi tünel oluşturur. Bu tüneller, verilerin kaynağını ve hedefini gizlemek için kullanılır. I2P ağı, verileri şifreleyerek ve bir dizi ara düğüm üzerinden yönlendirerek anonimlik sağlar.

### Temel Bileşenler

- **Router**: I2P ağında veri paketlerini yönlendiren bir yazılım bileşenidir.
- **Tunnel**: Verilerin anonim olarak iletilmesini sağlayan sanal bir yol.
- **LeaseSet**: Bir kullanıcının tünel bilgilerini içeren veri yapısı.
- **netDb**: Ağ veritabanı, I2P ağındaki diğer router'ların ve tünellerin bilgilerini saklar.
- **Floodfill**: Ağ veritabanını güncelleyen ve dağıtan özel router'lar.

### İletişim Protokolleri

I2P, NTCP2 ve SSU gibi çeşitli iletişim protokollerini destekler. Bu protokoller, verilerin güvenli ve anonim bir şekilde iletilmesini sağlar. NTCP2, TCP tabanlı bir protokoldür ve güvenli bağlantılar kurmak için kullanılır. SSU ise UDP tabanlıdır ve daha hızlı veri iletimi sağlar.

### Uygulama Entegrasyonu

I2P, SAMv3 ve I2CP gibi API'ler aracılığıyla uygulama entegrasyonunu destekler. Bu API'ler, geliştiricilerin I2P ağını uygulamalarına entegre etmelerine olanak tanır. Örneğin, bir geliştirici I2PTunnel kullanarak bir eepsite (I2P ağı üzerinde barındırılan web sitesi) oluşturabilir.

I2P'nin sağladığı anonimlik ve gizlilik özellikleri, kullanıcıların internet üzerindeki etkinliklerini gizli tutmalarına yardımcı olur. Bu, özellikle gizlilik odaklı kullanıcılar için önemli bir avantajdır.
file: "i2pinstall_2.10.0.jar"
size: "~30M"
requirements: "Java 8 veya daha yüksek"
sha256: "76372d552dddb8c1d751dde09bae64afba81fef551455e85e9275d3d031872ea"
links: ### I2P Ağının Temelleri

I2P, kullanıcıların internet üzerinde anonim olarak iletişim kurmalarını sağlayan bir gizlilik ağıdır. Bu ağ, kullanıcıların kimliklerini ve çevrimiçi aktivitelerini korumak için tasarlanmıştır. I2P, kullanıcıların verilerini şifreleyerek ve bir dizi anonimleştirilmiş "tünel" üzerinden yönlendirerek çalışır.

#### Router ve Tüneller

I2P ağı, router adı verilen yazılım bileşenleri tarafından desteklenir. Her kullanıcı, I2P ağına bağlanmak için kendi router'ını çalıştırır. Router, verileri alır ve gönderir, ayrıca diğer kullanıcıların verilerini anonimleştirilmiş tüneller aracılığıyla yönlendirir. Bu tüneller, verilerin kaynağını ve hedefini gizler.

#### LeaseSet ve netDb

I2P'de, bir LeaseSet, bir kullanıcının tünellerinin adres bilgilerini içerir. Bu bilgiler, netDb (ağ veritabanı) adı verilen dağıtılmış bir veritabanında saklanır. NetDb, kullanıcıların birbirleriyle iletişim kurabilmesi için gerekli olan adres bilgilerini sağlar.

#### Floodfill Router'lar

Floodfill router'lar, netDb'yi güncel tutmak için özel bir rol oynar. Bu router'lar, diğer router'lardan gelen verileri toplar ve dağıtır, böylece ağın veritabanı güncel kalır.

#### NTCP2 ve SSU

I2P, verileri iletmek için NTCP2 ve SSU adlı iki ana protokol kullanır. NTCP2, TCP tabanlı bir protokoldür ve güvenilir veri iletimi sağlar. SSU ise UDP tabanlıdır ve daha düşük gecikme süresi sunar, bu da onu ses ve video gibi gerçek zamanlı uygulamalar için ideal kılar.

#### SAMv3 ve I2PTunnel

SAMv3 ve I2PTunnel, geliştiricilerin I2P ağı üzerinde uygulamalar oluşturmasına olanak tanıyan API'lerdir. SAMv3, basit bir mesajlaşma protokolü sunarken, I2PTunnel, HTTP ve diğer protokoller için tünel oluşturmayı sağlar.

#### I2CP ve I2NP

I2CP, I2P router'ları ile uygulamalar arasında iletişimi sağlayan bir protokoldür. I2NP ise I2P ağı içinde veri paketlerinin iletiminden sorumlu protokoldür.

#### Eepsite ve Sarımsak Şifreleme

Eepsite, I2P ağı üzerinde barındırılan web siteleridir. Bu siteler, kullanıcıların kimliklerini gizli tutarak erişim sağlar. I2P, verileri korumak için sarımsak şifreleme kullanır, bu da birden fazla mesajın tek bir şifreli paket içinde birleştirilmesini içerir.
primary: "https://i2p.net/files/2.10.0/i2pinstall_2.10.0.jar"
mirror: "https://mirror.stormycloud.org/2.10.0/i2pinstall_2.10.0.jar"
torrent: "magnet:?xt=urn:btih:20ce01ea81b437ced30b1574d457cce55c86dce2&dn=i2pinstall_2.10.0.jar&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0.jar"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0.jar"
source: I2P, kullanıcıların internet üzerinde anonim olarak iletişim kurmasını sağlayan bir gizlilik ağıdır. I2P ağı, kullanıcıların kimliklerini ve konumlarını gizleyerek güvenli bir şekilde veri alışverişi yapmalarına olanak tanır. Bu, özellikle sansürden kaçınmak veya gizliliklerini korumak isteyen kullanıcılar için faydalıdır.

### I2P'nin Temel Bileşenleri

- **Router**: I2P ağına bağlanmak ve veri paketlerini yönlendirmek için kullanılan yazılım bileşeni.
- **Tunnel**: Verilerin anonim olarak iletilmesi için kullanılan sanal yollar.
- **LeaseSet**: Bir kullanıcının I2P ağı üzerindeki varlığını temsil eden veri yapısı.
- **NetDb**: I2P ağındaki diğer router'ların ve hizmetlerin bilgilerini depolayan dağıtılmış veritabanı.
- **Floodfill**: NetDb'yi güncel tutmak için özel bir router türü.

### İletişim Protokolleri

I2P, çeşitli iletişim protokollerini destekler:

- **NTCP2** ve **SSU**: Router'lar arasında veri iletimi için kullanılan protokoller.
- **SAMv3**: Harici uygulamaların I2P ağına bağlanmasını sağlayan bir API.
- **I2PTunnel**: HTTP ve diğer protokoller üzerinden anonim iletişim sağlamak için kullanılan araç.
- **I2CP**: I2P uygulamaları ile router arasında iletişim kurmak için kullanılan protokol.
- **I2NP**: I2P ağında veri paketlerinin iletilmesi için kullanılan protokol.

### Eepsite'lar

Eepsite, I2P ağı üzerinde barındırılan web siteleridir. Kullanıcılar, eepsite'lara erişerek anonim olarak bilgi alabilir veya paylaşabilirler. Eepsite'lar, geleneksel web sitelerine benzer şekilde çalışır ancak I2P ağı üzerinden erişilir.

### Güvenlik ve Gizlilik

I2P, kullanıcıların gizliliğini korumak için **garlic encryption** (sarımsak şifreleme) kullanır. Bu yöntem, verileri birden fazla katmanda şifreleyerek izlenmeyi zorlaştırır. Ayrıca, I2P ağı merkezi olmayan bir yapıya sahiptir, bu da tek bir başarısızlık noktasını ortadan kaldırır ve sansüre karşı dirençli hale getirir.
file: "i2psource_2.10.0.tar.bz2"
size: "~33M"
sha256: "3b651b761da530242f6db6536391fb781bc8e07129540ae7e96882bcb7bf2375"
links: I2P, kullanıcıların internet üzerinde anonim olarak iletişim kurmasını sağlayan bir gizlilik ağıdır. I2P, kullanıcıların kimliklerini ve konumlarını gizleyerek, sansürden kaçınmalarına ve çevrimiçi gizliliklerini korumalarına yardımcı olur. 

## I2P Nasıl Çalışır?

I2P, kullanıcıların verilerini bir dizi şifreli tünel üzerinden yönlendirerek çalışır. Bu tüneller, kullanıcıların kimliklerini gizler ve verilerin güvenli bir şekilde iletilmesini sağlar. I2P ağı, router'lar arasında veri paketlerini ileterek çalışır ve her router, verileri bir sonraki router'a iletmeden önce şifreler. 

### Temel Bileşenler

- **Router**: I2P ağının temel yapı taşıdır ve verilerin yönlendirilmesinden sorumludur.
- **Tunnel**: Verilerin şifreli olarak iletildiği sanal yollar.
- **LeaseSet**: Bir hizmetin veya kullanıcının I2P ağı üzerindeki varlığını tanımlayan veri yapısı.
- **NetDb**: I2P ağındaki router'ların ve diğer bileşenlerin bilgilerini depolayan dağıtılmış veritabanı.

### İletişim Protokolleri

I2P, NTCP2 ve SSU gibi çeşitli iletişim protokollerini kullanır. Bu protokoller, verilerin güvenli ve anonim bir şekilde iletilmesini sağlar. NTCP2, TCP tabanlı bir protokoldür ve daha güvenli bir bağlantı sunar. SSU ise UDP tabanlıdır ve daha hızlı veri iletimi sağlar.

### Uygulamalar ve Kullanım Alanları

I2P, çeşitli uygulamalar ve hizmetler için kullanılabilir. Örneğin, bir **eepsite** (I2P ağı üzerinde barındırılan web sitesi) oluşturabilir veya SAMv3 protokolü aracılığıyla uygulamalarınızı I2P ağına entegre edebilirsiniz. I2PTunnel, kullanıcıların HTTP ve diğer protokoller üzerinden anonim olarak iletişim kurmasını sağlar.

I2P, çevrimiçi gizliliği korumak isteyen kullanıcılar için güçlü bir araçtır. Anonimlik ve güvenlik sağlamak için gelişmiş şifreleme teknikleri kullanır ve kullanıcıların internet üzerinde özgürce iletişim kurmasına olanak tanır.
primary: "https://i2p.net/files/2.10.0/i2psource_2.10.0.tar.bz2"
torrent: "magnet:?xt=urn:btih:f62f519204abefb958d553f737ac0a7e84698f35&dn=i2psource_2.10.0.tar.bz2&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
github: "https://github.com/i2p/i2p.i2p"
android: I2P, kullanıcıların internet üzerindeki gizliliklerini korumalarına yardımcı olan bir anonim iletişim ağıdır. I2P, kullanıcıların kimliklerini gizleyerek güvenli ve özel bir şekilde iletişim kurmalarını sağlar. Bu, kullanıcıların çevrimiçi etkinliklerini izlenemez hale getirir ve sansürü aşmalarına yardımcı olur.

### I2P Nasıl Çalışır?

I2P, kullanıcıların verilerini şifreleyerek ve bir dizi anonim router üzerinden yönlendirerek çalışır. Her kullanıcı, I2P ağına katıldığında bir router çalıştırır. Bu router, verileri diğer router'lara ileterek anonimliği sağlar. Veriler, hedefe ulaşmadan önce birçok router üzerinden geçer, bu da izlenmeyi zorlaştırır.

#### Temel Bileşenler

- **Router**: I2P ağının temel yapı taşıdır. Her kullanıcı bir router çalıştırır.
- **Tunnel**: Verilerin şifrelenmiş bir şekilde iletildiği yoldur.
- **leaseSet**: Bir router'ın diğer router'larla iletişim kurmak için kullandığı bilgileri içerir.
- **netDb**: Ağın yönlendirme bilgilerini saklayan veritabanıdır.
- **floodfill**: Ağın yönlendirme bilgilerini dağıtan özel bir router türüdür.

### I2P'nin Avantajları

- **Gizlilik**: Kullanıcıların kimliklerini ve çevrimiçi etkinliklerini gizler.
- **Güvenlik**: Veriler, garlic encryption kullanılarak şifrelenir.
- **Sansür Direnci**: Kullanıcıların sansürü aşmasına yardımcı olur.

I2P, kullanıcıların internet üzerinde daha güvenli ve özel bir deneyim yaşamalarını sağlayan güçlü bir araçtır.
file: "I2P.apk"
version: "2.10.1"
size: "~28 MB"
requirements: "Android 4.0+, minimum 512MB RAM"
sha256: "c3d4e5f6789012345678901234567890123456789012345678901234abcdef"
links: I2P, kullanıcıların internet üzerinde anonim bir şekilde iletişim kurmasını sağlayan bir gizlilik ağıdır. I2P, kullanıcıların kimliklerini ve konumlarını gizleyerek güvenli ve özel bir iletişim sağlar. Bu, özellikle sansürden kaçınmak veya çevrimiçi gizliliği korumak isteyenler için önemlidir.

## I2P Nasıl Çalışır?

I2P, kullanıcıların verilerini bir dizi şifreli tünel üzerinden yönlendirerek çalışır. Her kullanıcı, verilerini göndermek ve almak için kendi tünel setini oluşturur. Bu tüneller, verilerin bir dizi ara düğüm üzerinden geçmesini sağlayarak göndericinin ve alıcının kimliğini gizler.

### Router ve Tüneller

I2P ağı, router adı verilen yazılım bileşenlerinden oluşur. Her router, verileri göndermek ve almak için bir dizi tünel kurar. Tüneller, verilerin bir dizi ara router üzerinden geçmesini sağlar, bu da göndericinin ve alıcının kimliğini gizler.

### LeaseSet ve netDb

Her router, diğer router'larla iletişim kurmak için bir leaseSet oluşturur. LeaseSet, bir router'ın tünel uç noktalarını ve diğer önemli bilgileri içeren bir veri yapısıdır. Bu bilgiler, netDb (ağ veritabanı) adı verilen dağıtılmış bir veritabanında saklanır. NetDb, router'ların birbirlerini bulmasına ve iletişim kurmasına olanak tanır.

### Floodfill Router'lar

Floodfill router'lar, netDb'nin güncellenmesinden ve diğer router'lara dağıtılmasından sorumlu özel router'lardır. Bu router'lar, ağın verimli bir şekilde çalışmasını sağlamak için kritik bir rol oynar.

## I2P'nin Avantajları

- **Anonimlik:** I2P, kullanıcıların kimliklerini ve konumlarını gizleyerek anonim bir iletişim sağlar.
- **Güvenlik:** I2P, verileri şifreleyerek ve tüneller üzerinden yönlendirerek güvenli bir iletişim sağlar.
- **Sansür Direnci:** I2P, kullanıcıların sansürü aşmasına ve engellenmiş içeriğe erişmesine olanak tanır.

I2P, kullanıcıların çevrimiçi gizliliklerini korumalarına ve güvenli bir şekilde iletişim kurmalarına yardımcı olan güçlü bir araçtır.
primary: "https://download.i2p.io/android/I2P.apk"
torrent: "magnet:?xt=urn:btih:android_example"
i2p: "http://stats.i2p/android/I2P.apk"
mirrors: I2P, kullanıcıların internet üzerinde anonim olarak iletişim kurmasını sağlayan bir gizlilik ağıdır. I2P, kullanıcıların kimliklerini ve çevrimiçi etkinliklerini korumak için çeşitli teknikler kullanır. Bu teknikler arasında "garlic encryption" (sarımsak şifreleme) ve "tunnel" (tünel) kullanımı yer alır. I2P ağı, "router" (yönlendirici) adı verilen yazılım bileşenleri tarafından yönetilir ve bu yönlendiriciler, verileri güvenli bir şekilde iletmek için "leaseSet" (kira seti) ve "netDb" (ağ veritabanı) gibi yapı taşlarını kullanır.

I2P'nin temel bileşenlerinden biri olan "floodfill" (taşma doldurma), ağın dağıtık yapısını korumak ve verilerin doğru bir şekilde yönlendirilmesini sağlamak için kullanılır. I2P, "NTCP2" ve "SSU" gibi protokoller aracılığıyla veri iletimini gerçekleştirir. Kullanıcılar, "SAMv3" ve "I2PTunnel" gibi araçlar sayesinde I2P ağına kolayca bağlanabilirler.

I2P, kullanıcıların kendi "eepsite" (I2P web sitesi) oluşturmasına ve bu siteleri anonim olarak barındırmasına olanak tanır. "I2CP" ve "I2NP" gibi protokoller, I2P ağında veri iletimi ve iletişim için kullanılır. Bu sayede, kullanıcılar internet üzerinde gizliliklerini koruyarak güvenli bir şekilde iletişim kurabilirler.
primary: I2P, kullanıcıların internet üzerinde anonim olarak iletişim kurmasını sağlayan bir gizlilik ağıdır. I2P, kullanıcıların kimliklerini gizleyerek güvenli ve özel bir iletişim sağlar. Bu, özellikle sansürden kaçınmak veya gizliliği korumak isteyenler için önemlidir.

## I2P Nasıl Çalışır?

I2P, kullanıcıların verilerini şifreleyerek ve bir dizi anonim router üzerinden yönlendirerek çalışır. Bu router'lar, verilerin kaynağını ve hedefini gizler, böylece kullanıcıların kimlikleri korunur. I2P, verileri "tüneller" aracılığıyla iletir ve her tünel, yalnızca belirli bir süre için geçerlidir, bu da güvenliği artırır.

### I2P'nin Bileşenleri

- **Router**: I2P ağının temel yapı taşıdır. Verileri alır, şifreler ve diğer router'lara iletir.
- **Tunnel**: Verilerin yönlendirildiği şifreli yol. Her kullanıcı, hem giriş hem de çıkış tünellerine sahiptir.
- **LeaseSet**: Bir kullanıcının tünel bilgilerini içeren veri yapısı. Diğer kullanıcıların bu tünellere nasıl erişeceğini belirtir.
- **NetDb**: I2P ağı içindeki router'ların ve tünellerin bilgilerini depolayan dağıtık veritabanı.
- **Floodfill**: NetDb'yi güncel tutmak için kullanılan özel router'lar. Bu router'lar, ağın verimliliğini artırır.

### I2P Kullanım Alanları

I2P, çeşitli amaçlar için kullanılabilir:

- **Anonim Tarama**: Kullanıcılar, kimliklerini gizleyerek web sitelerine erişebilir.
- **Eepsite Barındırma**: Kullanıcılar, I2P ağı üzerinden kendi web sitelerini (eepsite) barındırabilir.
- **Güvenli Mesajlaşma**: Kullanıcılar, mesajlarını şifreleyerek güvenli bir şekilde iletişim kurabilir.

I2P, kullanıcıların çevrimiçi gizliliğini korumak için güçlü bir araçtır ve internet üzerinde daha güvenli bir deneyim sunar.
name: "StormyCloud"
location: "Amerika Birleşik Devletleri"
url: "https://stormycloud.org"
resources: I2P, kullanıcıların internet üzerinde anonim olarak iletişim kurmasını sağlayan bir gizlilik ağıdır. I2P ağı, kullanıcıların kimliklerini ve konumlarını gizleyerek güvenli ve özel bir iletişim sağlar. 

## I2P Nasıl Çalışır?

I2P, kullanıcıların verilerini "tüneller" aracılığıyla yönlendirir. Her tünel, verilerin şifrelenmiş bir şekilde iletilmesini sağlar. Bu tüneller, kullanıcıların kimliklerini gizler ve iletişimin izlenmesini zorlaştırır.

### Temel Bileşenler

- **Router**: I2P ağındaki her katılımcı, bir router çalıştırır. Router, verileri tüneller üzerinden yönlendirir.
- **Tunnel**: Verilerin şifrelenmiş olarak iletildiği sanal yollar.
- **LeaseSet**: Bir kullanıcının tünel uç noktalarını tanımlayan veri yapısı.
- **NetDb**: Router'ların ve tünellerin bilgilerini saklayan dağıtık veritabanı.
- **Floodfill**: NetDb'yi güncelleyen ve dağıtan özel router'lar.

### İletişim Protokolleri

I2P, çeşitli iletişim protokollerini destekler:

- **NTCP2**: TCP tabanlı bir iletişim protokolü.
- **SSU**: UDP tabanlı bir iletişim protokolü.
- **SAMv3**: Uygulamaların I2P ağına bağlanmasını sağlayan bir API.

### Güvenlik ve Gizlilik

I2P, verileri "garlic encryption" (sarımsak şifreleme) kullanarak korur. Bu yöntem, verileri birden fazla katmanda şifreleyerek güvenliği artırır. Ayrıca, I2P ağında kimliklerin ve konumların gizliliği korunur.

### Eepsite'lar

I2P, kullanıcıların anonim web siteleri (eepsite) barındırmasına olanak tanır. Bu siteler, yalnızca I2P ağı üzerinden erişilebilir ve kullanıcıların kimliklerini gizler.

I2P ağı, kullanıcıların güvenli ve anonim bir şekilde iletişim kurmasını sağlayarak internet gizliliğini artırır.
archive: "https://download.i2p.io/archive/"
pgp_keys: "/downloads/pgp-keys"
---
