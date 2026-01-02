---
title: "Yönetilen İstemciler"
description: "Router tarafından yönetilen uygulamaların ClientAppManager ve port mapper ile nasıl entegre olduğu"
slug: "managed-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. Genel Bakış

[`clients.config`](/docs/specs/configuration/#clients-config) dosyasındaki girişler, router'a başlangıçta hangi uygulamaların çalıştırılacağını bildirir. Her giriş **managed** client (yönetilen istemci - tercih edilen) veya **unmanaged** client (yönetilmeyen istemci) olarak çalışabilir. Managed client'lar `ClientAppManager` ile işbirliği yapar ve bu yönetici:

- Uygulama örneğini oluşturur ve yönlendirici konsolu için yaşam döngüsü durumunu takip eder
- Kullanıcıya başlatma/durdurma kontrollerini sunar ve yönlendirici çıkışında temiz kapanmayı zorlar
- Uygulamaların birbirlerinin servislerini keşfedebilmesi için hafif bir **istemci kayıt defteri** ve **port eşleyici** barındırır

Yönetilmeyen istemciler basitçe bir `main()` metodunu çağırır; bunları yalnızca modernize edilemeyen eski kod için kullanın.

## 2. Yönetilen Bir İstemci Uygulama

Yönetilen istemciler, `net.i2p.app.ClientApp` (kullanıcıya yönelik uygulamalar için) veya `net.i2p.router.app.RouterApp` (router uzantıları için) arayüzlerinden birini uygulamalıdır. Yöneticinin bağlam ve yapılandırma argümanlarını sağlayabilmesi için aşağıdaki yapıcılardan birini sağlayın:

```java
public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)
```
```java
public MyRouterApp(RouterContext context, ClientAppManager manager, String[] args)
```
`args` dizisi, `clients.config` dosyasında veya `clients.config.d/` içindeki ayrı dosyalarda yapılandırılan değerleri içerir. Varsayılan yaşam döngüsü bağlantısını miras almak için mümkün olduğunda `ClientApp` / `RouterApp` yardımcı sınıflarını genişletin.

### 2.1 Lifecycle Methods

Yönetilen istemcilerin uygulaması beklenir:

- `startup()` - başlatma işlemlerini gerçekleştir ve hızlıca geri dön. INITIALIZED durumundan geçiş yapmak için en az bir kez `manager.notify()` çağrısı yapmalıdır.
- `shutdown(String[] args)` - kaynakları serbest bırak ve arka plan iş parçacıklarını durdur. Durumu STOPPING veya STOPPED olarak değiştirmek için en az bir kez `manager.notify()` çağrısı yapmalıdır.
- `getState()` - uygulamanın çalışıyor, başlatılıyor, durduruluyor veya başarısız olduğu bilgisini konsola bildir

Yönetici, kullanıcılar konsol ile etkileşime girdikçe bu metotları çağırır.

### 2.2 Advantages

- Yönlendirici konsolunda doğru durum raporlaması
- Thread sızıntısı veya statik referans bırakmadan temiz yeniden başlatmalar
- Uygulama durduktan sonra daha düşük bellek kullanımı
- Enjekte edilen bağlam üzerinden merkezileştirilmiş günlük kaydı ve hata raporlaması

## 3. Unmanaged Clients (Fallback Mode)

Yapılandırılan sınıf yönetilen bir arayüz uygulamıyorsa, router onu `main(String[] args)` çağırarak başlatır ve ortaya çıkan süreci takip edemez. Konsol sınırlı bilgi gösterir ve kapatma kancaları çalışmayabilir. Bu modu, yönetilen API'leri benimseyemeyen betikler veya tek seferlik yardımcı programlar için ayırın.

## 4. Client Registry

Yönetilen ve yönetilmeyen istemciler, diğer bileşenlerin isme göre bir referans alabilmesi için kendilerini yönetici ile kaydedebilir:

```java
manager.register(this);
```
Kayıt, kayıt defteri anahtarı olarak istemcinin `getName()` dönüş değerini kullanır. Bilinen kayıtlar arasında `console`, `i2ptunnel`, `Jetty`, `outproxy` ve `update` bulunur. Özellikleri koordine etmek için `ClientAppManager.getRegisteredApp(String name)` ile bir istemci alın (örneğin, console'un Jetty'den durum ayrıntılarını sorgulaması).

İstemci kaydının ve port eşleyicinin ayrı sistemler olduğunu unutmayın. İstemci kaydı, ad araması yoluyla uygulamalar arası iletişimi sağlarken, port eşleyici hizmet keşfi için hizmet adlarını host:port kombinasyonlarına eşler.

## 3. Yönetilmeyen İstemciler (Yedek Mod)

Port mapper, dahili TCP servisleri için basit bir dizin sunar. İşbirlikçilerin sabit kodlanmış adreslerden kaçınması için loopback portlarını kaydedin:

```java
context.portMapper().register(PortMapper.SVC_HTTPS_PROXY, 4445);
```
Veya açık host belirtimi ile:

```java
context.portMapper().register(PortMapper.SVC_HTTP_PROXY, "127.0.0.1", 4444);
```
`PortMapper.getPort(String name)` (bulunamazsa -1 döndürür) veya `getPort(String name, int defaultPort)` (bulunamazsa varsayılan değeri döndürür) kullanarak servisleri arayın. Kayıt durumunu `isRegistered(String name)` ile kontrol edin ve kayıtlı host'u `getActualHost(String name)` ile alın.

`net.i2p.util.PortMapper`'den ortak port mapper servis sabitleri:

- `SVC_CONSOLE` - Router konsolu (varsayılan port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (varsayılan port 4444)
- `SVC_HTTPS_PROXY` - HTTPS proxy (varsayılan port 4445)
- `SVC_I2PTUNNEL` - I2PTunnel yöneticisi
- `SVC_SAM` - SAM köprüsü (varsayılan port 7656)
- `SVC_SAM_SSL` - SAM köprüsü SSL
- `SVC_SAM_UDP` - SAM UDP
- `SVC_BOB` - BOB köprüsü (varsayılan port 2827)
- `SVC_EEPSITE` - Standart eepsite (varsayılan port 7658)
- `SVC_HTTPS_EEPSITE` - HTTPS eepsite
- `SVC_IRC` - IRC tüneli (varsayılan port 6668)
- `SVC_SUSIDNS` - SusiDNS

Not: `httpclient`, `httpsclient` ve `httpbidirclient` i2ptunnel tünel tipleridir (`tunnel.N.type` yapılandırmasında kullanılır), port mapper servis sabitleri değildir.

## 4. İstemci Kaydı

### 2.1 Yaşam Döngüsü Metotları

0.9.42 sürümünden itibaren router, yapılandırmayı `clients.config.d/` dizini içindeki ayrı dosyalara bölmeyi desteklemektedir. Her dosya, tüm özellikleri `clientApp.0.` önekiyle başlayan tek bir istemci için özellikler içerir:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
```
Bu, yeni kurulumlar ve eklentiler için önerilen yaklaşımdır.

### 2.2 Avantajlar

Geriye dönük uyumluluk için, geleneksel format sıralı numaralandırma kullanır:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.1.main=net.i2p.apps.systray.UrlLauncher
clientApp.1.name=URL Launcher
clientApp.1.delay=5
```
### 6.3 Configuration Properties

**Gerekli:** - `main` - ClientApp veya RouterApp'i uygulayan veya statik `main(String[] args)` içeren tam sınıf adı

**İsteğe Bağlı:** - `name` - Router konsolu için görünen ad (varsayılan olarak sınıf adı) - `args` - Boşluk veya sekme ile ayrılmış argümanlar (tırnaklı dizileri destekler) - `delay` - Başlamadan önceki saniye (varsayılan 120) - `onBoot` - True ise `delay=0` yapar - `startOnLoad` - İstemciyi etkinleştirir/devre dışı bırakır (varsayılan true)

**Eklentiye özgü:** - `stopargs` - Kapatma sırasında geçirilen argümanlar - `uninstallargs` - Eklenti kaldırma sırasında geçirilen argümanlar - `classpath` - Virgülle ayrılmış ek classpath girdileri

**Eklentiler için değişken ikamesi:** - `$I2P` - I2P temel dizini - `$CONFIG` - Kullanıcı yapılandırma dizini (örn., ~/.i2p) - `$PLUGIN` - Eklenti dizini - `$OS` - İşletim sistemi adı - `$ARCH` - Mimari adı

## 5. Port Mapper

- Yönetilen istemcileri tercih edin; yönetilmeyen istemcilere yalnızca kesinlikle gerekli olduğunda geri dönün.
- Konsol işlemlerinin duyarlı kalması için başlatma ve kapatma işlemlerini hafif tutun.
- Kayıt defteri ve port adlarını açıklayıcı kullanın, böylece tanı araçları (ve son kullanıcılar) bir servisin ne yaptığını anlayabilir.
- Statik singleton'lardan kaçının - kaynakları paylaşmak için enjekte edilen bağlam ve yöneticiyi kullanın.
- Konsol durumunun doğru kalması için tüm durum geçişlerinde `manager.notify()` çağrısı yapın.
- Ayrı bir JVM'de çalıştırmanız gerekiyorsa, günlüklerin ve tanılamaların ana konsola nasıl yansıtıldığını belgelendirin.
- Harici programlar için, yönetilen istemci avantajlarından yararlanmak üzere ShellService (versiyon 1.7.0'da eklendi) kullanmayı düşünün.

## 6. Yapılandırma Formatı

Yönetilen istemciler **sürüm 0.9.4** ile (17 Aralık 2012) tanıtıldı ve **sürüm 2.10.0** (9 Eylül 2025) itibarıyla önerilen mimari olmaya devam etmektedir. Temel API'ler bu süre boyunca sıfır bozucu değişiklikle kararlı kalmıştır:

- Constructor imzaları değiştirilmedi
- Yaşam döngüsü metodları (startup, shutdown, getState) değiştirilmedi
- ClientAppManager kayıt metodları değiştirilmedi
- PortMapper kayıt ve arama metodları değiştirilmedi

Önemli iyileştirmeler: - **0.9.42 (2019)** - Tekil yapılandırma dosyaları için clients.config.d/ dizin yapısı - **1.7.0 (2021)** - Harici program durum takibi için ShellService eklendi - **2.10.0 (2025)** - Yönetilen istemci API değişikliği olmayan güncel sürüm

Bir sonraki büyük sürüm, minimum olarak Java 17+ gerektirecektir (altyapı gereksinimi, bir API değişikliği değildir).

## References

- [clients.config spesifikasyonu](/docs/specs/configuration/#clients-config)
- [Yapılandırma Dosyası Spesifikasyonu](/docs/specs/configuration/)
- [I2P Teknik Dokümantasyon İndeksi](/docs/)
- [ClientAppManager Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientAppManager.html) (API 0.9.66)
- [PortMapper Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/util/PortMapper.html) (API 0.9.66)
- [ClientApp arayüzü](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html) (API 0.9.66)
- [RouterApp arayüzü](https://i2p.github.io/i2p.i2p/net/i2p/router/app/RouterApp.html) (API 0.9.66)
- [Alternatif Javadoc (kararlı sürüm)](https://docs.i2p-projekt.de/javadoc/)
- [Alternatif Javadoc (clearnet yansıması)](https://eyedeekay.github.io/javadoc-i2p/)

> **Not:** I2P ağı, erişim için bir I2P router gerektiren kapsamlı belgeleri http://idk.i2p/javadoc-i2p/ adresinde barındırmaktadır. Clearnet erişimi için yukarıdaki GitHub Pages yansısını kullanın.
