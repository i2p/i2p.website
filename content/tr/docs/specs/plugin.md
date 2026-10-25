---
title: "Eklenti Spesifikasyonu"
description: "I2P eklentileri için .xpi2p / .su3 paketleme kuralları"
slug: "plugin"
aliases:
  - "/tr/plugin_spec"
  - "/tr/plugin_spec/"
lastUpdated: "2022-01"
accurateFor: "0.9.53"
type: docs
---

## Genel Bakış

Bu belge, .xpi2p dosya formatını belirtir (Firefox .xpi gibi), ancak XML install.rdf dosyası yerine basit bir plugin.config açıklama dosyası ile. Bu dosya formatı hem ilk eklenti kurulumları hem de eklenti güncellemeleri için kullanılır.

Ayrıca bu belge, router'ın eklentileri nasıl yüklediğine dair kısa bir genel bakış ve eklenti geliştiricileri için politikalar ve yönergeler sağlar.

Temel .xpi2p dosya formatı, i2pupdate.sud dosyası ile aynıdır (router güncellemeleri için kullanılan format), ancak yükleyici, imzalayanın anahtarını henüz bilmese bile kullanıcının eklentiyi yüklemesine izin verecektir.

0.9.15 sürümünden itibaren, SU3 dosya formatı desteklenmekte ve tercih edilmektedir. Bu format daha güçlü imzalama anahtarları sağlar.

> **Not:** Artık xpi2p formatında eklenti dağıtmayı önermiyoruz. su3 formatını kullanın.

Standart dizin yapısı, kullanıcıların aşağıdaki eklenti türlerini yüklemesine olanak tanır:

- Konsol web uygulamaları
- cgi-bin, webapp'li yeni eepsite
- Konsol temaları
- Konsol çevirileri
- Java programları
- Ayrı JVM'de Java programları
- Herhangi bir kabuk betiği veya program

Bir eklenti tüm dosyalarını `~/.i2p/plugins/name/` dizinine (`%APPDIR%\I2P\plugins\name\` Windows'ta) kurar. Yükleyici başka bir yere kurulumu engelleyecektir, ancak eklenti çalışırken başka yerlerdeki kütüphanelere erişebilir.

Bu, yalnızca kurulum, kaldırma ve yükseltme işlemlerini kolaylaştırmanın ve temel plugin çakışmalarını azaltmanın bir yolu olarak görülmelidir.

Ancak plugin çalışmaya başladığında temelde hiçbir güvenlik modeli yoktur. Plugin aynı JVM'de ve router ile aynı izinlerle çalışır ve dosya sistemine, router'a, harici programları çalıştırmaya vb. tam erişime sahiptir.

## Ayrıntılar

foo.xpi2p, aşağıdakileri içeren imzalı bir güncelleme (sud) dosyasıdır:

Zip dosyasının başına eklenen standart .sud başlığı, aşağıdakileri içerir:

```text
40-byte DSA signature
16-byte plugin version in UTF-8, padded with trailing zeroes if necessary
```
Aşağıdakileri içeren zip dosyası:

### plugin.config dosyası

Bu dosya gereklidir. Aşağıdaki özellikleri içeren standart bir I2P yapılandırma dosyasıdır:

#### Gerekli Özellikler

Aşağıdaki dört özellik gereklidir. İlk üçü, bir güncelleme eklentisi için kurulu eklentideki özelliklerle aynı olmalıdır.

-   **name** - Bu dizin adında kurulacak. Native eklentiler için, farklı paketlerde ayrı adlar isteyebilirsiniz - örneğin foo-windows ve foo-linux.
-   **key** - '=' ile biten 172 B64 karakter olarak DSA public key. SU3 formatı için atla.
-   **signer** - yourname@mail.i2p önerilir
-   **version** - VersionComparator'ın ayrıştırabileceği bir formatta olmalı, örneğin 1.2.3-4. Maksimum 16 bayt (sud versiyonu ile eşleşmeli). Geçerli sayı ayırıcıları '.', '-', ve '_'dir. Güncelleme eklentisi için bu, kurulu eklentidekinden büyük olmalıdır.

#### Görüntü Özellikleri

Aşağıdaki özelliklerin değerleri, mevcut olmaları durumunda router konsolunda /configplugins sayfasında görüntülenir:

-   **date** - Java time - long int
-   **author** - `yourname@mail.i2p` önerilir
-   **websiteURL** - `http://foo.i2p/`
-   **updateURL** - `http://foo.i2p/foo.xpi2p` - Güncelleme denetleyicisi, daha yeni bir sürümün mevcut olup olmadığını belirlemek için bu URL'deki 41-56 baytları kontrol edecektir. 1.7.0 (0.9.53) sürümünden itibaren, URL'de `$OS` ve `$ARCH` değişkenlerini kullanmak mümkündür. Önerilmez. Daha önce xpi2p formatında plugin dağıtmadıysanız kullanmayın.
-   **updateURL.su3** - `http://foo.i2p/foo.su3` - 0.9.15 sürümünden itibaren su3 formatındaki güncelleme dosyasının konumu. 1.7.0 (0.9.53) sürümünden itibaren, URL'de `$OS` ve `$ARCH` değişkenlerini kullanmak mümkündür.
-   **description** - İngilizce olarak
-   **description_xx** - xx dili için
-   **license** - Plugin lisansı
-   **disableStop=true** - Varsayılan false. True ise durdur butonu gösterilmeyecektir. Webapp yoksa ve stopargs'lı istemci yoksa bunu kullanın.

#### Konsol Özet Çubuğu Bağlantı Özellikleri

Aşağıdaki özellikler konsol özet çubuğuna bir bağlantı eklemek için kullanılır:

-   **consoleLinkName** - özet çubuğuna eklenecek
-   **consoleLinkName_xx** - xx dili için
-   **consoleLinkURL** - /appname/index.jsp
-   **consoleLinkTooltip** - 0.7.12-6 sürümünden itibaren desteklenir
-   **consoleLinkTooltip_xx** - 0.7.12-6 sürümünden itibaren xx dili

#### Konsol Simgesi Özellikleri

Konsola özel bir simge eklemek için aşağıdaki isteğe bağlı özellikler kullanılabilir:

-   **console-icon** - 0.9.20 sürümünden itibaren desteklenir. Yalnızca webapps için. 32x32 görüntüye giden yol, örneğin /icon.png. 1.7.0 sürümünden itibaren (API 0.9.53), consoleLinkURL belirtilmişse, yol o URL'ye göreli olur. Aksi takdirde webapp adına görelidir. Plugin'deki tüm webapps için geçerlidir.
-   **icon-code** - 0.9.25 sürümünden itibaren desteklenir. Web kaynakları olmayan plugin'ler için konsol simgesi sağlar. 32x32 png görüntü dosyasında `net.i2p.data.Base64 encode FILE` çağrılarak üretilen B64 dizesi.

#### Yükleyici Özellikleri

Aşağıdaki özellikler eklenti yükleyicisi tarafından kullanılır:

-   **type** - app/theme/locale/webapp/... (uygulanmamış, muhtemelen gerekli değil)
-   **min-i2p-version** - Bu eklentinin gerektirdiği minimum I2P sürümü
-   **max-i2p-version** - Bu eklentinin çalışacağı maksimum I2P sürümü
-   **min-java-version** - Bu eklentinin gerektirdiği minimum Java sürümü
-   **min-jetty-version** - 0.8.13 sürümünden itibaren desteklenir, Jetty 6 webapp'leri için 6 kullanın
-   **max-jetty-version** - 0.8.13 sürümünden itibaren desteklenir, Jetty 5 webapp'leri için 5.99999 kullanın
-   **required-platform-OS** - uygulanmamış - belki sadece görüntülenecek, doğrulanmayacak
-   **other-requirements** - uygulanmamış, örn. python x.y - yükleyici tarafından doğrulanmaz, sadece kullanıcıya gösterilir
-   **dont-start-at-install=true** - Varsayılan false. Eklenti yüklendiğinde veya güncellendiğinde başlatmaz.
-   **router-restart-required=true** - Varsayılan false. Bu, güncelleme sırasında router'ı veya eklentiyi yeniden başlatmaz, sadece kullanıcıyı yeniden başlatmanın gerekli olduğu konusunda bilgilendirir.
-   **update-only=true** - Varsayılan false. True ise, mevcut bir kurulum yoksa başarısız olur.
-   **install-only=true** - Varsayılan false. True ise, mevcut bir kurulum varsa başarısız olur.
-   **min-installed-version** - mevcut bir kurulum varsa, üzerine güncellenecek minimum sürüm
-   **max-installed-version** - mevcut bir kurulum varsa, üzerine güncellenecek maksimum sürüm
-   **depends=plugin1,plugin2,plugin3** - uygulanmamış
-   **depends-version=0.3.4,,5.6.7** - uygulanmamış

#### Çeviri Özellikleri

-   **langs=xx,yy,Klingon,...** - (uygulanmamış) (yy ülke bayrağıdır)

### Uygulama Dizinleri ve Dosyaları

Aşağıdaki dizinlerin veya dosyaların her biri isteğe bağlıdır, ancak bir şeyler orada bulunmalıdır yoksa hiçbir işe yaramaz:

**console/**

-   **locale/** - Yalnızca temel I2P kurulumundaki uygulamalar için yeni kaynak paketleri (çeviriler) içeren jar dosyaları. Bu eklenti için paketler console/webapp/foo.war veya lib/foo.jar içine yerleştirilmelidir
-   **themes/** - Router konsolu için yeni temalar. Her temayı bir alt dizine yerleştirin.
-   **webapps/** - (webapps hakkında aşağıdaki önemli notlara bakın) .war dosyaları - Bunlar webapps.config'de devre dışı bırakılmadığı sürece kurulum zamanında çalıştırılacaktır. War adının eklenti adıyla aynı olması gerekmez. Temel I2P kurulumunda war adlarını tekrarlamayın.
-   **webapps.config** - Router'ın webapps.config'i ile aynı format. Ayrıca webapp classpath'i için $PLUGIN/lib/ veya $I2P/lib'de ek jar dosyalarını belirtmek için kullanılır: `webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar`

> **Not:** 1.7.0 sürümünden önce (API 0.9.53), classpath satırı yalnızca warname plugin adıyla aynı olduğunda yükleniyordu. API 0.9.53 itibariyle, classpath ayarı herhangi bir warname için çalışacaktır.

> **Not:** Router sürüm 0.7.12-9'dan önce, router `webapps.warname.startOnLoad` yerine `plugin.warname.startOnLoad` aradı. Eski router sürümleri ile uyumluluk için, bir war'ı devre dışı bırakmak isteyen bir eklenti her iki satırı da içermelidir.

**eepsite/**

(Eepsite'lar hakkında aşağıdaki önemli notlara bakın)

-   **cgi-bin/**
-   **docroot/**
-   **logs/**
-   **webapps/**
-   **jetty.xml** - Kurulum programının yolu ayarlamak için burada değişken değişimi yapması gerekecek. Bu dosyanın konumu ve adı, clients.config içinde ayarlandığı sürece gerçekten önemli değil - buradan bir seviye yukarıda olması daha uygun olabilir.

**lib/**

Herhangi bir jar dosyasını buraya koyun ve console/webapps.config ve/veya clients.config dosyalarındaki classpath satırında belirtin

### clients.config dosyası

Bu dosya isteğe bağlıdır ve bir plugin başlatıldığında çalıştırılacak istemcileri belirtir. Router'ın clients.config dosyasıyla aynı formatı kullanır. Format hakkında daha fazla bilgi ve istemcilerin nasıl başlatılıp durdurulduğu konusundaki önemli ayrıntılar için clients.config yapılandırma dosyası spesifikasyonuna bakın.

-   **clientApp.0.stopargs=foo bar stop baz** - Mevcutsa, sınıf bu argümanlarla çağrılarak istemciyi durdurur. Tüm durdurma görevleri sıfır gecikmeyle çağrılır. Not: Router yönetilmeyen istemcilerinizin çalışıp çalışmadığını bilemez.
-   **clientApp.0.uninstallargs=foo bar uninstall baz** - Mevcutsa, sınıf $PLUGIN silinmeden hemen önce bu argümanlarla çağrılır. Tüm kaldırma görevleri sıfır gecikmeyle çağrılır.
-   **clientApp.0.classpath=$I2P/lib/foo.bar,$PLUGIN/lib/bar.jar** - Plugin çalıştırıcısı args ve stopargs satırlarında aşağıdaki şekilde değişken değiştirimi yapacaktır:
    -   `$I2P` - I2P temel kurulum dizini
    -   `$CONFIG` - I2P yapılandırma dizini (genellikle ~/.i2p)
    -   `$PLUGIN` - bu plugin'in kurulum dizini (genellikle ~/.i2p/plugins/appname)
    -   `$OS` - `windows`, `linux`, `mac` biçiminde ana işletim sistemi
    -   `$ARCH` - `386`, `amd64`, `arm64` biçiminde ana mimarisi

(Kabuk betikleri veya harici programlar çalıştırma hakkındaki önemli notları aşağıda görün)

## Eklenti Yükleyici Görevleri

Bu, I2P tarafından bir eklenti kurulduğunda neler olduğunu listeler.

1.  .xpi2p dosyası indirilir.
2.  .sud imzası saklanan anahtarlara karşı doğrulanır. 0.9.14.1 sürümü itibariyle, eşleşen anahtar yoksa, tüm anahtarlara izin veren gelişmiş router özelliği ayarlanmadıkça kurulum başarısız olur.
3.  Zip dosyasının bütünlüğünü doğrula.
4.  plugin.config dosyasını çıkart.
5.  Eklentinin çalışacağından emin olmak için I2P sürümünü doğrula.
6.  Webappların mevcut $I2P uygulamalarını kopyalamadığını kontrol et.
7.  Mevcut eklentiyi durdur (varsa).
8.  update=false ise kurulum dizininin henüz mevcut olmadığını doğrula, veya üzerine yazma izni iste.
9.  update=true ise kurulum dizininin mevcut olduğunu doğrula, veya oluşturma izni iste.
10. Eklentiyi appDir/plugins/name/ konumuna unzip et.
11. Eklentiyi plugins.config dosyasına ekle.

## Plugin Başlatıcı Görevleri

Bu, eklentiler başlatıldığında ne olduğunu listeler. İlk olarak, hangi eklentilerin başlatılması gerektiğini görmek için plugins.config kontrol edilir. Her eklenti için:

1.  clients.config dosyasını kontrol et ve her öğeyi yükleyip başlat (yapılandırılmış jar dosyalarını classpath'e ekle).
2.  console/webapp ve console/webapp.config dosyalarını kontrol et. Gerekli öğeleri yükle ve başlat (yapılandırılmış jar dosyalarını classpath'e ekle).
3.  Eğer mevcutsa console/locale/foo.jar dosyasını çeviri classpath'ine ekle.
4.  Eğer mevcutsa console/theme dizinini tema arama yoluna ekle.
5.  Özet çubuğu bağlantısını ekle.

## Konsol Webapp Notları

Arka plan görevleri olan konsol webappları bir ServletContextListener implement etmelidir (örnekler için seedless veya i2pbote'ye bakın), ya da servlet içinde destroy() methodunu override etmelidir, böylece durdurulabilirler. Router sürüm 0.7.12-3 itibariyle, konsol webappları yeniden başlatılmadan önce her zaman durdurulacaktır, bu nedenle bunu yaptığınız sürece birden fazla instance konusunda endişelenmenize gerek yoktur. Ayrıca router sürüm 0.7.12-3 itibariyle, konsol webappları router kapatılırken durdurulacaktır.

Kütüphane jar dosyalarını webapp içine dahil etmeyin; bunları lib/ dizinine koyun ve webapps.config dosyasına bir classpath ekleyin. Bu şekilde ayrı kurulum ve güncelleme eklentileri oluşturabilirsiniz; burada güncelleme eklentisi kütüphane jar dosyalarını içermez.

Plugin'inizde Jetty, Tomcat veya servlet jar'larını asla paketlemeyin, çünkü bunlar I2P kurulumundaki sürümle çakışabilir. Çakışan kütüphaneleri paketlememeye dikkat edin.

.java veya .jsp dosyalarını dahil etmeyin; aksi takdirde Jetty bunları kurulum sırasında yeniden derleyecektir, bu da başlatma süresini artıracaktır. Çoğu I2P kurulumunda classpath'te çalışan bir Java ve JSP derleyicisi bulunsa da, bu garanti edilmez ve tüm durumlarda çalışmayabilir.

Şu anda, $PLUGIN içine classpath dosyaları eklemesi gereken bir webapp'in plugin ile aynı adı taşıması gerekir. Örneğin, foo plugin'i içindeki bir webapp foo.war olarak adlandırılmalıdır.

I2P, 0.9.30 sürümünden beri Servlet 3.0'ı desteklese de, @WebContent için annotation taramasını DESTEKLEMEZ (web.xml dosyası yok). Birkaç ek çalışma zamanı jar dosyası gerekli olacaktır ve bunları standart kurulumda sağlamıyoruz. @WebContent desteğine ihtiyacınız varsa I2P geliştiricileri ile iletişime geçin.

## Eepsite Notları

Bir eklentinin mevcut bir eepsite'a nasıl kurulacağı net değil. Router'ın eepsite'a herhangi bir bağlantısı yok ve çalışıyor olabilir ya da olmayabilir, ayrıca birden fazla olabilir. Daha iyisi, yepyeni bir eepsite için kendi Jetty örneğinizi ve I2PTunnel örneğinizi başlatmaktır.

Yeni bir I2PTunnel örneği oluşturabilir (i2ptunnel CLI'sının yaptığına benzer şekilde), ancak tabii ki i2ptunnel arayüzünde görünmeyecektir, çünkü bu farklı bir örnektir. Ama bu sorun değil. Sonra i2ptunnel ve jetty'yi birlikte başlatıp durdurabilirsiniz.

Bu nedenle router'ın bunu mevcut bir eepsite ile otomatik olarak birleştirmesine güvenmeyin. Muhtemelen olmayacaktır. clients.config'den yeni bir I2PTunnel ve Jetty başlatın. Bunun en iyi örnekleri zzzot ve pebble eklentileridir.

jetty.xml dosyasına yol ikamesi nasıl yapılır? Örnekler için zzzot ve pebble eklentilerine bakın.

## İstemci Başlatma/Durdurma Notları

0.9.4 sürümünden itibaren, router "yönetilen" plugin istemcilerini desteklemektedir. Yönetilen plugin istemcileri `ClientAppManager` tarafından başlatılır ve çalıştırılır. ClientAppManager, istemciye bir referans tutar ve istemcinin durumu hakkında güncellemeler alır. Yönetilen plugin istemcileri tercih edilir, çünkü durum takibi yapmak ve bir istemciyi başlatıp durdurmak çok daha kolaydır. Ayrıca, bir istemci durdurulduktan sonra aşırı bellek kullanımına yol açabilecek statik referanslardan kaçınmak da çok daha kolaydır. Yönetilen istemci yazma hakkında daha fazla bilgi için clients.config yapılandırma dosyası spesifikasyonuna bakın.

"Yönetilmeyen" plugin istemcileri için, router'ın clients.config aracılığıyla başlatılan istemcilerin durumunu izleme yolu yoktur. Plugin yazarı, mümkün olduğunca, statik durum tablosu tutarak veya PID dosyaları kullanarak vb. birden fazla başlatma veya durdurma çağrısını zarif bir şekilde ele almalıdır. Birden fazla başlatma veya durdurmada loglama veya istisna atmaktan kaçının. Bu aynı zamanda önceki bir başlatma olmadan yapılan durdurma çağrısı için de geçerlidir. Router sürüm 0.7.12-3 itibariyle, plugin'ler router kapatılırken durdurulacaktır, bu da clients.config'de stopargs olan tüm istemcilerin daha önce başlatılıp başlatılmadığına bakılmaksızın çağrılacağı anlamına gelir.

## Shell Script ve Harici Program Notları

Shell script'leri veya diğer harici programları çalıştırmak için, işletim sistemi türünü kontrol eden ve ardından sağladığınız .bat veya .sh dosyası üzerinde ShellCommand çalıştıran küçük bir Java sınıfı yazın. Bunun için genelleştirilmiş bir çözüm I2P 1.7.0/0.9.53 sürümünde eklendi: tek bir komut için durum takibi yapan ve ClientAppManager ile iletişim kuran "ShellService".

Router durduğunda harici programlar durdurulmayacak ve router başladığında ikinci bir kopya çalışmaya başlayacaktır. Bu durum genellikle durum takibi yapmak için bir ShellService kullanılarak hafifletilebilir. Bu, kullanım durumunuz için uygun değilse, PID'yi bir PID dosyasında saklama işlemini yapan ve başlangıçta kontrol eden bir wrapper sınıfı veya shell scripti yazabilirsiniz.

## Diğer Eklenti Yönergeleri

-   Anahtar üretimi, plugin su3 dosya oluşturma ve doğrulama için makeplugin.sh shell script'i için i2p.scripts monotone branch'ına veya zzz'nin sayfasındaki örnek pluginlerden herhangi birine bakın. Bu, görevlerin çoğunu otomatikleştirir. Bu scripti plugin oluşturma sürecinize dahil etmelisiniz.
-   Plugin'ler için jar ve war dosyalarının Pack200 ile sıkıştırılması şiddetle önerilir, genellikle plugin'leri %60-65 oranında küçültür. Örnek için zzz'nin sayfasındaki örnek pluginlerden herhangi birine bakın. Pack200 açma işlemi, pluginleri destekleyen hemen hemen tüm router'lar olan 0.7.11-5 ve üzeri versiyonlarda desteklenir.
-   Plugin'ler $I2P dizinine yazmaya çalışmamalıdır çünkü salt okunur olabilir ve bu zaten iyi bir politika değildir.
-   Plugin'ler $CONFIG dizinine yazabilir ancak dosyaları sadece $PLUGIN dizininde tutmak önerilir. $PLUGIN dizinindeki tüm dosyalar kaldırma işleminde silinecektir.
-   $CWD herhangi bir yerde olabilir; belirli bir yerde olduğunu varsaymayın, $CWD'ye göre dosya okuma veya yazma girişiminde bulunmayın. ShellService için her zaman $PLUGIN ile aynıdır.
-   Java programları I2PAppContext içindeki dizin getirici fonksiyonlarla nerede olduklarını bulmalıdır.
-   Plugin dizini `I2PAppContext.getGlobalContext().getAppDir().getAbsolutePath() + "/plugins/" + appname`'dir, veya clients.config içindeki args satırına $PLUGIN argümanı ekleyin.
-   Tüm yapılandırma dosyaları UTF-8 olmalıdır.
-   Ayrı bir JVM'de çalıştırmak için ShellCommand'ı `java -cp foo:bar:baz my.main.class arg1 arg2 arg3` şeklinde kullanın.
-   clients.config içindeki stopargs'a alternatif olarak, Java istemcisi `I2PAppContext.addShutdownTask()` ile shutdown hook kaydedebilir. Ancak bu, yükseltme sırasında plugin'i kapatmaz, bu yüzden stopargs önerilir. Ayrıca, oluşturulan tüm thread'leri daemon moduna ayarlayın.
-   Standart kurulumda bulunanların aynısı olan sınıfları dahil etmeyin. Gerekirse sınıfları genişletin.
-   Eski ve yeni kurulumlar arasında wrapper.config'teki farklı classpath tanımlarına dikkat edin.
-   İstemciler farklı keyname'ler ile duplikate anahtarları, farklı anahtarlar ile duplikate keyname'leri ve yükseltme paketlerinde farklı anahtarları veya keyname'leri reddedecektir. Anahtarlarınızı koruyun. Sadece bir kez oluşturun.
-   Yükseltme sırasında üzerine yazılacağı için plugin.config dosyasını çalışma zamanında değiştirmeyin. Çalışma zamanı yapılandırmasını saklamak için dizinde farklı bir yapılandırma dosyası kullanın.
-   Genel olarak, plugin'ler $I2P/lib/router.jar'a erişim gerektirmemelidir. Özel bir şey yapmadığınız sürece router sınıflarına erişmeyin.
-   Her versiyonun öncekinden yüksek olması gerektiği için, versiyonun sonuna bir build numarası eklemek üzere build scriptinizi geliştirebilirsiniz.
-   Plugin'ler asla `System.exit()` çağırmamalıdır.
-   Lütfen paketlediğiniz herhangi bir yazılım için lisans gereksinimlerini karşılayarak lisanslara saygı gösterin.
-   router JVM zaman dilimini UTC olarak ayarlar. Eğer bir plugin kullanıcının gerçek zaman dilimini bilmesi gerekiyorsa, bu bilgi router tarafından I2PAppContext özelliği `i2p.systemTimeZone` içinde saklanır.

## Sınıf Yolları

$I2P/lib dizinindeki aşağıdaki jar dosyaları, orijinal kurulumun ne kadar eski veya yeni olduğuna bakılmaksızın, tüm I2P kurulumları için standart classpath'te bulunduğu varsayılabilir.

i2p jar'larındaki tüm güncel genel API'ler, Javadocs'ta belirtilen sürüm-sonrası numarasına sahiptir. Plugin'iniz yalnızca güncel sürümlerde mevcut olan belirli özellikler gerektiriyorsa, plugin.config dosyasında min-i2p-version, min-jetty-version özelliklerini veya her ikisini birden ayarladığınızdan emin olun.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">addressbook.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription and blockfile support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need; use the NamingService interface</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-logging.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Apache Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since release 0.9.30</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-el.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSP Expressions Language</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with JSPs that use EL. As of release 0.9.30 (Jetty 9), this contains the EL 3.0 API.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with HTTP or other servers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-compiler.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">nothing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since Jetty 6 (release 0.9)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-runtime.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper Compiler and Runtime, and some Tomcat utils</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">javax.servlet.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs. As of release 0.9.30 (Jetty 9), this contains the Servlet 3.1 and JSP 2.3 APIs.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jbigi.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Binaries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jetty-i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Support utilities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Some plugins will need. As of release 0.9.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">mstreaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">org.mortbay.jetty.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty Base</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins starting their own Jetty instance will need. Recommended way of starting Jetty is with <code>net.i2p.jetty.JettyStart</code> in jetty-i2p.jar.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins using router context will need; most will not</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">routerconsole.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need, not a public API</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">sam.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">streaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming Implementation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">URL Launcher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins should not need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray4j.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Systray</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need. As of 0.9.26, no longer present.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">wrapper.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
  </tbody>
</table>
$I2P/lib dizinindeki aşağıdaki jar dosyalarının, orijinal kurulumun ne kadar eski ya da yeni olduğuna bakılmaksızın tüm I2P kurulumlarında mevcut olduğu varsayılabilir, ancak bu dosyalar mutlaka classpath'te bulunmaz:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jstl.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">standard.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
  </tbody>
</table>
Yukarıda listelenmemiş herhangi bir şey, SİZİN i2p sürümünüzde classpath'te olsa bile, herkesin classpath'inde bulunmayabilir. Yukarıda listelenmemiş herhangi bir jar'a ihtiyacınız varsa, eklentinizde clients.config veya webapps.config dosyasında belirtilen classpath'e $I2P/lib/foo.jar ekleyin.

Daha önce, clients.config dosyasında belirtilen classpath girişi tüm JVM için classpath'e eklenmekteydi. Ancak 0.7.13-3 sürümünden itibaren bu durum class loader'lar kullanılarak düzeltildi ve artık, başlangıçta amaçlandığı gibi, clients.config dosyasında belirtilen classpath sadece o belirli thread için geçerli olmaktadır. Bu nedenle, her istemci için gereken tam classpath'i belirtin.

## Java Sürümü Notları

I2P, 0.9.24 sürümünden (Ocak 2016) bu yana Java 7 gerektirmektedir. I2P, 0.9.12 sürümünden (Nisan 2014) bu yana Java 6 gerektirmektedir. En son sürümü kullanan I2P kullanıcıları 1.7 (7.0) JVM çalıştırıyor olmalıdır.

Eklentiniz **1.7 gerektirmiyorsa**:

-   Tüm java ve jsp dosyalarının source="1.6" target="1.6" ile derlendiğinden emin olun.
-   Paketlenmiş tüm kütüphane jar dosyalarının da 1.6 veya daha düşük sürümler için olduğundan emin olun.

Eklentiniz **1.7 sürümünü gerektiriyorsa**:

-   İndirme sayfanızda bunu belirtin.
-   plugin.config dosyanıza min-java-version=1.7 ekleyin

Her durumda, çalışma zamanı çökmelerini önlemek için Java 8 ile derlerken **mutlaka** bir bootclasspath ayarlamalısınız.

## Güncellerken JVM Çöküyor

Not - bunların hepsi artık düzeltilmiş olmalı.

JVM, I2P başlatıldığından beri çalışan bir eklentide jar dosyalarını güncellerken çökme eğilimindedir (eklenti daha sonra durdurulmuş olsa bile). Bu durum 0.7.13-3 sürümündeki class loader uygulamasıyla düzeltilmiş olabilir, ancak kesin değildir.

En güvenli yöntem, plugin'inizi war içinde jar ile tasarlamak (bir webapp için), ya da güncelleme sonrası yeniden başlatma gerektirmek, veya plugin'inizdeki jar'ları güncellememektir.

Bir webapp içinde class loader'ların çalışma şekli nedeniyle, classpath'i webapps.config'de belirtirseniz harici jar'ları bulundurmanız _güvenli olabilir_. Bunu doğrulamak için daha fazla test gereklidir. Eğer sadece bir webapp için gerekiyorsa, classpath'i clients.config'de 'sahte' bir client ile belirtmeyin - bunun yerine webapps.config kullanın.

En az güvenli olan ve görünüşe göre çoğu çökmenin kaynağı, clients.config dosyasında classpath'te belirtilen plugin jar'ları olan istemcilerdir.

Bunların hiçbiri ilk kurulumda sorun olmamalı - bir eklentinin ilk kurulumu için hiçbir zaman yeniden başlatma gerektirmemelisiniz.

## Referanslar

-   [Yapılandırma Dosyası Spesifikasyonu](/docs/specs/configuration)
-   [DSA Kriptografisi](/docs/specs/cryptography#DSA)
-   [Güncellemeler Spesifikasyonu](/docs/specs/updates)
