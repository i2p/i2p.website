---
title: "Eklenti Paket Biçimi"
description: ".xpi2p / .su3 I2P eklentileri için paketleme kuralları"
slug: "plugin"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Genel Bakış

I2P eklentileri, router işlevselliğini genişleten imzalı arşivlerdir. Bunlar `.xpi2p` veya `.su3` dosyaları olarak dağıtılır, `~/.i2p/plugins/<name>/` (Windows'ta `%APPDIR%\I2P\plugins\<name>\`) dizinine kurulur ve herhangi bir korumalı alan olmadan tam router izinleriyle çalışır.

### Desteklenen Eklenti Türleri

- Konsol web uygulamaları
- cgi-bin ve web uygulamaları içeren yeni eepsites (I2P içindeki gizli web siteleri)
- Konsol temaları
- Konsol çevirileri
- Java programları (aynı süreç içinde veya ayrı bir JVM)
- Kabuk betikleri ve yerel ikili dosyalar

### Güvenlik Modeli

**KRİTİK:** Eklentiler, I2P router ile aynı izinlere sahip olarak aynı JVM (Java Sanal Makinesi) içinde çalışır. Şunlara sınırsız erişimleri vardır: - Dosya sistemi (okuma ve yazma) - Router API'leri ve iç durum - Ağ bağlantıları - Harici programların çalıştırılması

Eklentiler tamamen güvenilir kod olarak ele alınmalıdır. Kullanıcılar, kurulumdan önce eklenti kaynaklarını ve imzalarını doğrulamalıdır.

---

## Dosya Biçimleri

### SU3 Formatı (Şiddetle Önerilir)

**Durum:** Aktif, I2P 0.9.15'ten (Eylül 2014) beri tercih edilen biçim

The `.su3` biçimi şunları sağlar: - **RSA-4096 imzalama anahtarları** (xpi2p'deki DSA-1024'e kıyasla) - İmza dosya başlığında saklanır - Sihirli sayı: `I2Psu3` - Geleceğe dönük daha iyi uyumluluk

**Yapı:**

```
[SU3 Header with RSA-4096 signature]
[ZIP Archive]
  ├── plugin.config (required)
  ├── console/
  ├── lib/
  ├── webapps/
  └── [other plugin files]
```
### XPI2P Biçimi (Eski, kullanımdan kaldırılmış)

**Durum:** Geriye dönük uyumluluk için destekleniyor, yeni eklentiler için önerilmez

`.xpi2p` biçimi daha eski kriptografik imzalar kullanır:
- **DSA-1024 imzaları** (NIST-800-57'ye göre kullanım dışı)
- ZIP'in başına eklenen 40 baytlık DSA imzası
- plugin.config dosyasında `key` alanını gerektirir

**Yapı:**

```
[40-byte DSA signature]
[16-byte version string (UTF-8, zero-padded)]
[ZIP Archive]
```
**Geçiş Yolu:** xpi2p'den su3'e geçişte, geçiş süresince hem `updateURL` hem de `updateURL.su3` sağlayın. Modern routers (0.9.15+) SU3'e otomatik olarak öncelik verir.

---

## Arşiv Düzeni ve plugin.config

### Gerekli Dosyalar

**plugin.config** - Anahtar-değer çiftleri içeren standart bir I2P yapılandırma dosyası

### Gerekli Özellikler

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Installation directory name, must match for updates</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Alphanumeric, no spaces</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>signer</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Developer contact information</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>user@mail.i2p</code> format recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>version</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Plugin version for update comparison</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Max 16 bytes, parsed by VersionComparator</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>key</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA public key (172 B64 chars ending with '=')</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Omit for SU3 format</strong></td></tr>
  </tbody>
</table>
**Sürüm Biçimi Örnekleri:** - `1.2.3` - `1.2.3-4` - `2.0.0-beta.1`

Geçerli ayırıcılar: `.` (nokta), `-` (tire), `_` (alt çizgi)

### İsteğe bağlı meta veri özellikleri

#### Bilgileri Görüntüle

- `date` - Sürüm tarihi (Java long timestamp - Java 'long' veri türünde zaman damgası)
- `author` - Geliştirici adı (`user@mail.i2p` önerilir)
- `description` - İngilizce açıklama
- `description_xx` - Yerelleştirilmiş açıklama (xx = dil kodu)
- `websiteURL` - Eklenti ana sayfası (`http://foo.i2p/`)
- `license` - Lisans tanımlayıcısı (örn., "Apache-2.0", "GPL-3.0")

#### Güncelleme Ayarları

- `updateURL` - XPI2P güncelleme konumu (eski)
- `updateURL.su3` - SU3 güncelleme konumu (tercih edilen)
- `min-i2p-version` - Gerekli minimum I2P sürümü
- `max-i2p-version` - Uyumlu maksimum I2P sürümü
- `min-java-version` - Minimum Java sürümü (örn. `1.7`, `17`)
- `min-jetty-version` - Minimum Jetty sürümü (Jetty 6+ için `6` kullanın)
- `max-jetty-version` - Maksimum Jetty sürümü (Jetty 5 için `5.99999` kullanın)

#### Kurulum Davranışı

- `dont-start-at-install` - Varsayılan `false`. `true` ise manuel başlatma gerekir
- `router-restart-required` - Varsayılan `false`. Güncellemeden sonra yeniden başlatma gerektiğini kullanıcıya bildirir
- `update-only` - Varsayılan `false`. Eklenti zaten kurulu değilse başarısız olur
- `install-only` - Varsayılan `false`. Eklenti zaten mevcutsa başarısız olur
- `min-installed-version` - Güncelleme için gereken asgari sürüm
- `max-installed-version` - Güncellenebilecek azami sürüm
- `disableStop` - Varsayılan `false`. `true` ise Durdur düğmesini gizler

#### Konsol Entegrasyonu

- `consoleLinkName` - Konsol özet çubuğu bağlantısı için metin
- `consoleLinkName_xx` - Yerelleştirilmiş bağlantı metni (xx = dil kodu)
- `consoleLinkURL` - Bağlantı hedefi (örn. `/appname/index.jsp`)
- `consoleLinkTooltip` - Üzerine gelindiğinde görünen metin (0.7.12-6 sürümünden beri desteklenir)
- `consoleLinkTooltip_xx` - Yerelleştirilmiş araç ipucu
- `console-icon` - 32x32 simge yolu (0.9.20 sürümünden beri desteklenir)
- `icon-code` - Web kaynakları olmayan eklentiler için Base64 ile kodlanmış 32x32 PNG (0.9.25'ten beri)

#### Platform Gereksinimleri (Yalnızca Görüntüleme)

- `required-platform-OS` - İşletim sistemi gereksinimi (zorunlu değildir)
- `other-requirements` - Ek gereksinimler (örn. "Python 3.8+")

#### Bağımlılık Yönetimi (Uygulanmadı)

- `depends` - Virgülle ayrılmış eklenti bağımlılıkları
- `depends-version` - Bağımlılıklar için sürüm gereksinimleri
- `langs` - Dil paketi içeriği
- `type` - Eklenti türü (app/theme/locale/webapp)

### Güncelleme URL'sinde Değişken Yerine Koyma

**Özellik Durumu:** I2P 1.7.0 (0.9.53) sürümünden beri kullanılabilir

Hem `updateURL` hem de `updateURL.su3` platforma özel değişkenleri destekler:

**Değişkenler:** - `$OS` - İşletim sistemi: `windows`, `linux`, `mac` - `$ARCH` - Mimari: `386`, `amd64`, `arm64`

**Örnek:**

```properties
updateURL.su3=http://foo.i2p/downloads/foo-$OS-$ARCH.su3
```
**Windows AMD64 üzerinde sonuç:**

```
http://foo.i2p/downloads/foo-windows-amd64.su3
```
Bu, platforma özgü derlemelerde tek bir plugin.config dosyası kullanılmasına olanak tanır.

---

## Dizin Yapısı

### Standart Düzen

```
plugins/
└── pluginname/
    ├── plugin.config (required)
    ├── console/
    │   ├── locale/          # Translation JARs
    │   ├── themes/          # Console themes
    │   ├── webapps/         # Web applications
    │   └── webapps.config   # Webapp configuration
    ├── eepsite/
    │   ├── cgi-bin/
    │   ├── docroot/
    │   ├── logs/
    │   ├── webapps/
    │   └── jetty.xml
    ├── lib/
    │   └── *.jar            # Plugin libraries
    └── clients.config       # Client startup configuration
```
### Dizin Amaçları

**console/locale/** - I2P temel çevirileri için resource bundles (kaynak demetleri) içeren JAR dosyaları - Eklentiye özel çeviriler `console/webapps/*.war` veya `lib/*.jar` içinde olmalıdır

**console/themes/** - Her alt dizin tam bir konsol teması içerir - Tema arama yoluna otomatik olarak eklenir

**console/webapps/** - konsol entegrasyonu için `.war` dosyaları - `webapps.config` içinde devre dışı bırakılmadıkça otomatik olarak başlatılır - .war dosya adının eklenti adıyla eşleşmesi gerekmez

**eepsite/** - Kendi Jetty örneğine sahip eksiksiz bir eepsite - Değişken ikamesi içeren `jetty.xml` yapılandırması gerektirir - zzzot ve pebble eklenti örneklerine bakın

**lib/** - Eklenti JAR kitaplıkları - `clients.config` veya `webapps.config` aracılığıyla classpath (sınıf yolu) içinde belirtin

---

## Web uygulaması yapılandırması

### webapps.config Biçimi

Web uygulamasının davranışını kontrol eden standart I2P yapılandırma dosyası.

**Sözdizimi:**

```properties
# Disable autostart
webapps.warname.startOnLoad=false

# Add classpath JARs (as of API 0.9.53, works for any warname)
webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar
```
**Önemli Notlar:** - router 0.7.12-9 öncesinde, uyumluluk için `plugin.warname.startOnLoad` kullanın - API 0.9.53'ten önce, classpath (sınıf yolu) yalnızca warname eklenti adıyla eşleştiğinde çalışıyordu - 0.9.53+ itibarıyla, classpath herhangi bir web uygulaması adıyla çalışır

### Web Uygulamaları için En İyi Uygulamalar

1. **ServletContextListener Uygulaması**
   - Kaynak temizliği için `javax.servlet.ServletContextListener`'ı uygulayın
   - Veya servlet içinde `destroy()` yöntemini geçersiz kılın
   - Güncellemeler sırasında ve router durdurulurken doğru şekilde kapanmayı sağlar

2. **Kütüphane Yönetimi**
   - Paylaşılan JAR dosyalarını `lib/` içine yerleştirin, WAR dosyasının içine değil
   - `webapps.config` classpath (sınıf yolu) üzerinden referans verin
   - Eklentilerin ayrı ayrı kurulup/güncellenmesini sağlar

3. **Çakışan Kütüphanelerden Kaçının**
   - Jetty, Tomcat veya servlet JAR'larını asla paketlemeyin
   - Standart I2P kurulumundaki JAR'ları asla paketlemeyin
   - Standart kütüphaneler için classpath bölümünü kontrol edin

4. **Derleme Gereksinimleri**
   - `.java` veya `.jsp` kaynak dosyalarını dahil etmeyin
   - Başlangıç gecikmelerini önlemek için tüm JSP'leri önceden derleyin
   - Java/JSP derleyicisinin mevcut olduğunu varsaymayın

5. **Servlet API Uyumluluğu**
   - I2P, Servlet 3.0'ı destekler (0.9.30'dan beri)
   - **Annotation taraması DESTEKLENMEZ** (@WebContent)
   - Geleneksel `web.xml` dağıtım tanımlayıcısı sağlanmalıdır

6. **Jetty Sürümü**
   - Güncel: Jetty 9 (I2P 0.9.30+)
   - Soyutlama için `net.i2p.jetty.JettyStart` kullanın
   - Jetty API değişikliklerine karşı korur

---

## İstemci Yapılandırması

### clients.config Biçimi

Eklenti tarafından başlatılan istemcileri (servisleri) tanımlar.

**Temel İstemci:**

```properties
clientApp.0.main=com.example.PluginMain
clientApp.0.name=Example Plugin Service
clientApp.0.delay=30
clientApp.0.args=arg1 arg2 $PLUGIN/config.properties
```
**Durdur/Kaldır özelliği olan İstemci:**

```properties
clientApp.0.stopargs=stop
clientApp.0.uninstallargs=uninstall
clientApp.0.classpath=$PLUGIN/lib/plugin.jar,$I2P/lib/i2p.jar
```
### Özellik Referansı

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>main</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fully qualified class name implementing ClientApp interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Display name for user interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>delay</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Startup delay in seconds (default: 0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>args</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Space-separated arguments passed to constructor</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>stopargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments for shutdown (must handle gracefully)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>uninstallargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments called before plugin deletion</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>classpath</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated JAR paths</td></tr>
  </tbody>
</table>
### Değişken Yerine Koyma

Aşağıdaki değişkenler, `args`, `stopargs`, `uninstallargs` ve `classpath` içinde yerine konur:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Replacement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$I2P</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P base installation directory</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$CONFIG</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P configuration directory (typically <code>~/.i2p</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$PLUGIN</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">This plugin's directory (<code>$CONFIG/plugins/name</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$OS</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Operating system: <code>windows</code>, <code>linux</code>, <code>mac</code></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$ARCH</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Architecture: <code>386</code>, <code>amd64</code>, <code>arm64</code></td></tr>
  </tbody>
</table>
### Yönetilen ve Yönetilmeyen İstemciler

**Yönetilen İstemciler (Önerilir, 0.9.4'ten itibaren):** - ClientAppManager tarafından örneklenir - Referans ve durum takibini sürdürür - Daha kolay yaşam döngüsü yönetimi - Daha iyi bellek yönetimi

**Yönetilmeyen İstemciler:** - router tarafından başlatılır, durum takibi yok - Birden fazla başlat/durdur çağrısını sorunsuz şekilde ele almalıdır - Koordinasyon için statik durum veya PID dosyaları kullanın - router kapatılırken çağrılır (0.7.12-3 itibarıyla)

### ShellService (0.9.53 / 1.7.0 sürümlerinden itibaren)

Harici programları otomatik durum takibiyle çalıştırmaya yönelik genelleştirilmiş bir çözüm.

**Özellikler:** - Süreç yaşam döngüsünü yönetir - ClientAppManager ile iletişim kurar - Otomatik PID (süreç kimliği) yönetimi - Çapraz platform desteği

**Kullanım:**

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myservice.sh
```
Platforma özgü komut dosyaları için:

```properties
clientApp.0.args=$PLUGIN/bin/myservice-$OS.$ARCH
```
**Alternatif (Eski):** İşletim sistemi türünü kontrol eden bir Java sarmalayıcı yazın, uygun `.bat` veya `.sh` dosyasıyla `ShellCommand`'u çağırın.

---

## Kurulum Süreci

### Kullanıcı Kurulum Akışı

1. Kullanıcı eklenti URL’sini Router Konsolu Eklenti Yapılandırma Sayfası'na (`/configplugins`) yapıştırır
2. Router eklenti dosyasını indirir
3. İmza doğrulaması (anahtar bilinmiyorsa ve katı mod etkinse başarısız olur)
4. ZIP bütünlük denetimi
5. `plugin.config` dosyasını çıkar ve ayrıştır
6. Sürüm uyumluluğunun doğrulanması (`min-i2p-version`, `min-java-version`, vb.)
7. Web uygulaması adı çakışmasının tespiti
8. Güncelleme ise mevcut eklentiyi durdur
9. Dizin doğrulaması (`plugins/` altında olmalı)
10. Tüm dosyaları eklenti dizinine çıkar
11. `plugins.config` dosyasını güncelle
12. Eklentiyi başlat (`dont-start-at-install=true` değilse)

### Güvenlik ve Güven

**Anahtar Yönetimi:** - Yeni imzalayanlar için ilk görülen anahtara dayalı güven modeli - Yalnızca jrandom ve zzz anahtarları önceden paketlenmiş - 0.9.14.1 itibarıyla bilinmeyen anahtarlar varsayılan olarak reddedilir - Geliştirme için gelişmiş bir özellik ile geçersiz kılınabilir

**Kurulum Kısıtlamaları:** - Arşivler yalnızca eklenti dizinine açılmalıdır - Yükleyici `plugins/` dışındaki yolları reddeder - Eklentiler kurulumdan sonra başka yerlerdeki dosyalara erişebilir - Sandboxing (izole çalışma ortamı) veya ayrıcalık izolasyonu yoktur

---

## Güncelleme Mekanizması

### Güncelleme Kontrol Süreci

1. Router, plugin.config dosyasından `updateURL.su3` (tercih edilen) veya `updateURL` değerini okur
2. Bayt 41-56'yı almak için HTTP HEAD veya kısmi GET isteği yapılır
3. Uzak dosyadan sürüm dizesi çıkarılır
4. VersionComparator (sürüm karşılaştırma sınıfı) kullanılarak yüklü sürümle karşılaştırılır
5. Daha yeniyse, kullanıcının onayı istenir veya otomatik indirilir (ayarlara bağlı olarak)
6. Eklenti durdurulur
7. Güncelleme yüklenir
8. Eklenti başlatılır (kullanıcı tercihi değişmediyse)

### Sürüm Karşılaştırması

Sürümler nokta/tire/alt çizgi ile ayrılmış bileşenler olarak ayrıştırılır: - `1.2.3` < `1.2.4` - `1.2.3` < `1.2.3-1` - `2.0.0` > `1.9.9`

**Maksimum uzunluk:** 16 bayt (SUD/SU3 başlığıyla eşleşmelidir)

### Güncelleme En İyi Uygulamaları

1. Yayınlar için her zaman sürümü artırın
2. Önceki sürümden güncelleme yolunu test edin
3. Büyük değişikliklerde `router-restart-required` seçeneğini göz önünde bulundurun
4. Geçiş sırasında hem `updateURL` hem de `updateURL.su3` sağlayın
5. Test için derleme numarası soneki kullanın (`1.2.3-456`)

---

## Classpath (sınıf yolu) ve Standart Kitaplıklar

### Classpath (sınıf yolu) içinde her zaman mevcut

I2P 0.9.30+ sürümlerinde `$I2P/lib` içindeki aşağıdaki JAR'lar her zaman sınıf yolunda (classpath) bulunur:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Plugin Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Required for all plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>mstreaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>streaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming implementation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2ptunnel.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP/server plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>router.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Router internals</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed, avoid if possible</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>javax.servlet.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet 3.1, JSP 2.3 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with servlets/JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jasper-runtime.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper compiler/runtime</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>commons-el.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">EL 3.0 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSPs using expression language</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jetty-i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty utilities</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins starting Jetty</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>org.mortbay.jetty.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty 9 base</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Custom Jetty instances</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>sam.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>addressbook.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription/blockfile</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Use NamingService instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>routerconsole.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Not public API, avoid</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jbigi.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Native crypto</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>systray.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">URL launcher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>wrapper.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Service wrapper</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
  </tbody>
</table>
### Özel Notlar

**commons-logging.jar:** - 0.9.30'dan beri boş - 0.9.30'dan önce: Apache Tomcat JULI - 0.9.24'ten önce: Commons Logging + JULI - 0.9'dan önce: yalnızca Commons Logging

**jasper-compiler.jar:** - Jetty 6'dan beri boş (0.9)

**systray4j.jar:** - 0.9.26 sürümünde kaldırıldı

### Classpath'ta değil (belirtmelisiniz)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jstl.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>standard.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
  </tbody>
</table>
### Classpath (sınıf yolu) Belirtimi

**clients.config dosyasında:**

```properties
clientApp.0.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/i2p.jar
```
**webapps.config dosyasında:**

```properties
webapps.mywebapp.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/jstl.jar
```
**Önemli:** 0.7.13-3 sürümünden itibaren, classpath'ler iş parçacığına özgüdür; JVM genelinde değildir. Her istemci için tam classpath belirtin.

---

## Java Sürüm Gereksinimleri

### Güncel Gereksinimler (Ekim 2025)

**I2P 2.10.0 ve önceki sürümler:** - En az: Java 7 (0.9.24'ten beri gerekli, Ocak 2016) - Önerilen: Java 8 veya daha yenisi

**I2P 2.11.0 ve sonrası (YAKINDA):** - **En az: Java 17+** (2.9.0 sürüm notlarında duyuruldu) - İki sürüm önceden uyarı verildi (2.9.0 → 2.10.0 → 2.11.0)

### Eklenti Uyumluluk Stratejisi

**Maksimum uyumluluk için (I2P 2.10.x'e kadar):**

```xml
<javac source="1.7" target="1.7" />
```
```properties
min-java-version=1.7
```
**Java 8+ özellikleri için:**

```xml
<javac source="1.8" target="1.8" />
```
```properties
min-java-version=1.8
```
**Java 11+ özellikleri için:**

```xml
<javac source="11" target="11" />
```
```properties
min-java-version=11
```
**2.11.0+ için hazırlıklar:**

```xml
<javac source="17" target="17" />
```
```properties
min-java-version=17
min-i2p-version=2.11.0
```
### Derleme için En İyi Uygulamalar

**Daha eski bir hedef sürümü için daha yeni bir JDK ile derleme yaparken:**

```xml
<javac source="1.7" target="1.7" 
       bootclasspath="${java7.home}/jre/lib/rt.jar"
       includeantruntime="false" />
```
Bu, hedef Java sürümünde bulunmayan API'lerin kullanılmasını engeller.

---

## Pack200 Sıkıştırması - KULLANIM DIŞI

### Kritik Güncelleme: Pack200'u Kullanmayın

**Durum:** KULLANIMDAN KALDIRILDI VE ÇIKARILDI

Orijinal spesifikasyon, boyutu %60-65 oranında azaltmak için Pack200 sıkıştırmasını kuvvetle tavsiye ediyordu. **Bu artık geçerli değil.**

**Zaman çizelgesi:** - **JEP 336:** Pack200, Java 11'de eskimiş (deprecated) olarak işaretlendi (Eylül 2018) - **JEP 367:** Pack200, Java 14'te kaldırıldı (Mart 2020)

**Resmi I2P Güncellemeler Spesifikasyonu şöyle der:** > "zip içindeki Jar ve war dosyaları, yukarıda 'su2' dosyaları için belgelendiği gibi artık pack200 ile sıkıştırılmıyor, çünkü güncel Java çalışma zamanları artık bunu desteklemiyor."

**Ne yapılmalı:**

1. **pack200'ü derleme süreçlerinden derhal kaldırın**
2. **Standart ZIP sıkıştırmasını kullanın**
3. **Alternatifleri değerlendirin:**
   - Kod küçültme için ProGuard/R8
   - Yerel ikili dosyalar için UPX
   - Özel bir açıcı sağlanıyorsa güncel sıkıştırma algoritmaları (zstd, brotli)

**Mevcut Eklentiler için:** - Eski routers (0.7.11-5, Java 10'a kadar) hâlâ pack200'u açabilir - Yeni routers (Java 11+) pack200'u açamaz - Eklentileri pack200 sıkıştırması olmadan yeniden yayımlayın

---

## İmzalama Anahtarları ve Güvenlik

### Anahtar Üretimi (SU3 Format (I2P'de kullanılan imzalı güncelleme dosya biçimi))

i2p.scripts deposundaki `makeplugin.sh` betiğini kullanın:

```bash
# Generate new signing key
./makeplugin.sh keygen

# Keys stored in ~/.i2p-plugin-keys/
```
**Önemli Ayrıntılar:** - Algoritma: RSA_SHA512_4096 - Biçim: X.509 sertifikası - Depolama: Java anahtar deposu biçimi

### Eklentilerin İmzalanması

```bash
# Create signed su3 file
./makeplugin.sh sign myplugin.zip myplugin.su3 keyname

# Verify signature
./makeplugin.sh verify myplugin.su3
```
### Anahtar Yönetimi için En İyi Uygulamalar

1. **Bir kez üret, sonsuza dek koru**
   - Routers, anahtarı farklı olan aynı anahtar adlarını reddeder
   - Routers, anahtar adı farklı olan aynı anahtarları reddeder
   - Anahtar/ad uyuşmazlığı varsa güncellemeler reddedilir

2. **Güvenli depolama**
   - Keystore (anahtar deposu) yedeğini güvenli şekilde alın
   - Güçlü bir passphrase (parola öbeği) kullanın
   - Asla sürüm kontrolüne eklemeyin

3. **Anahtar rotasyonu**
   - Mevcut mimari tarafından desteklenmiyor
   - Uzun vadeli anahtar kullanımını planlayın
   - Ekip geliştirmesi için çoklu imza şemalarını değerlendirin

### Eski DSA İmzalama (XPI2P)

**Durum:** Çalışır durumda ancak eskimiş

xpi2p biçimi (I2P eklenti paket biçimi) tarafından kullanılan DSA-1024 imzaları: - 40 baytlık imza - 172 base64 karakterli açık anahtar - NIST-800-57 asgari olarak (L=2048, N=224) değerlerini önerir - I2P daha zayıfını kullanır (L=1024, N=160)

**Öneri:** Bunun yerine RSA-4096 ile SU3 (I2P’de kullanılan imzalı güncelleme dosyası biçimi) kullanın.

---

## Eklenti Geliştirme Yönergeleri

### Temel En İyi Uygulamalar

1. **Dokümantasyon**
   - Kurulum talimatlarını içeren anlaşılır bir README (Benioku dosyası) sağlayın
   - Yapılandırma seçeneklerini ve varsayılanları belgeleyin
   - Her sürümle birlikte bir değişiklik günlüğü ekleyin
   - Gerekli I2P/Java sürümlerini belirtin

2. **Boyut Optimizasyonu**
   - Yalnızca gerekli dosyaları ekleyin
   - Asla router JAR'larını paketlemeyin
   - Kurulum ve güncelleme paketlerini ayırın (kütüphaneler lib/ içinde)
   - ~~Pack200 sıkıştırmasını kullanın~~ **KULLANIMDAN KALKTI - Standart ZIP kullanın**

3. **Yapılandırma**
   - Çalışma zamanında `plugin.config` dosyasını asla değiştirmeyin
   - Çalışma zamanı ayarları için ayrı bir yapılandırma dosyası kullanın
   - Gerekli router ayarlarını belgelendirin (SAM portları, tunnels vb.)
   - Kullanıcının mevcut yapılandırmasına saygı gösterin

4. **Kaynak Kullanımı**
   - Varsayılan bant genişliği tüketimini aşırıya kaçırmaktan kaçının
   - Makul CPU kullanım sınırları uygulayın
   - Kapatma sırasında kaynakları temizleyin
   - Uygun olduğunda daemon threads (arka planda çalışan iş parçacıkları) kullanın

5. **Test**
   - Tüm platformlarda kurulum/yükseltme/kaldırmayı test edin
   - Önceki sürümden güncellemeleri test edin
   - Güncellemeler sırasında web uygulamasının durdurulmasını/yeniden başlatılmasını doğrulayın
   - Desteklenen en düşük I2P sürümüyle test edin

6. **Dosya Sistemi**
   - Asla `$I2P` içine yazmayın (salt okunur olabilir)
   - Çalışma zamanı verilerini `$PLUGIN` veya `$CONFIG` içine yazın
   - Dizin keşfi için `I2PAppContext` kullanın
   - `$CWD` konumunu varsaymayın

7. **Uyumluluk**
   - Standart I2P sınıflarını çoğaltmayın
   - Gerekirse sınıfları genişletin, değiştirmeyin
   - plugin.config içindeki `min-i2p-version`, `min-jetty-version` değerlerini kontrol edin
   - Destekliyorsanız daha eski I2P sürümleriyle test edin

8. **Kapatma Yönetimi**
   - clients.config içinde uygun `stopargs` uygulayın
   - Kapatma kancalarını kaydedin: `I2PAppContext.addShutdownTask()`
   - Birden çok başlatma/durdurma çağrısını sorunsuz şekilde yönetin
   - Tüm iş parçacıklarını daemon (arka plan) moduna ayarlayın

9. **Güvenlik**
   - Tüm dış girdileri doğrulayın
   - `System.exit()` asla çağırmayın
   - Kullanıcı gizliliğine saygı gösterin
   - Güvenli kodlama uygulamalarına uyun

10. **Lisanslama**
    - Eklenti lisansını açıkça belirtin
    - Birlikte paketlenen kütüphanelerin lisanslarına saygı gösterin
    - Gerekli atıfları ekleyin
    - Gerekirse kaynak koda erişim sağlayın

### Gelişmiş Hususlar

**Saat Dilimi Yönetimi:** - Router JVM saat dilimini UTC olarak ayarlar - Kullanıcının gerçek saat dilimi: `I2PAppContext` özelliği `i2p.systemTimeZone`

**Dizin Keşfi:**

```java
// Plugin directory
String pluginDir = I2PAppContext.getGlobalContext()
    .getAppDir().getAbsolutePath() + "/plugins/" + pluginName;

// Or use $PLUGIN variable in clients.config args
```
**Sürüm Numaralandırma:** - Anlamsal sürümleme kullanın (major.minor.patch) - Test için derleme numarası ekleyin (1.2.3-456) - Güncellemelerde monotonik artışı sağlayın

**Router Sınıf Erişimi:** - Genel olarak `router.jar` bağımlılıklarından kaçının - Bunun yerine `i2p.jar` içindeki public API'leri kullanın - Gelecekte I2P, router sınıfına erişimi kısıtlayabilir

**JVM Çökme Önleme (Tarihsel):** - 0.7.13-3'te düzeltildi - Sınıf yükleyicilerini doğru şekilde kullanın - Çalışan eklentide JAR'ları güncellemekten kaçının - Gerekirse güncellemeden sonra yeniden başlatmayı destekleyecek şekilde tasarlayın

---

## Eepsite Eklentileri

### Genel Bakış

Eklentiler, kendi Jetty (Java servlet konteyneri) ve I2PTunnel örneklerine sahip, tam özellikli eepsites sağlayabilir.

### Mimari

**Şunları yapmaya çalışmayın:** - Mevcut bir eepsite (I2P üzerindeki site) içine kurmak - Router'ın varsayılan eepsite'i ile birleştirmek - Tek bir eepsite'in mevcut olduğunu varsaymak

**Bunun yerine:** - Yeni bir I2PTunnel örneği başlat (CLI yaklaşımıyla) - Yeni bir Jetty örneği başlat - Her ikisini de `clients.config` içinde yapılandır

### Örnek Yapı

```
plugins/myeepsite/
├── plugin.config
├── clients.config          # Starts Jetty + I2PTunnel
├── eepsite/
│   ├── jetty.xml          # Requires variable substitution
│   ├── docroot/
│   ├── webapps/
│   └── logs/
└── lib/
    └── [dependencies]
```
### jetty.xml'de Değişken Yerine Koyma

Yollar için `$PLUGIN` değişkenini kullanın:

```xml
<Set name="resourceBase">$PLUGIN/eepsite/docroot</Set>
```
Router, eklenti başlatılırken ikame işlemi yapar.

### Örnekler

Referans gerçeklemeler: - **zzzot eklentisi** - Torrent izleyici - **pebble eklentisi** - Blog platformu

Her ikisi de zzz'nin eklenti sayfasında (I2P içi) bulunabilir.

---

## Konsol Entegrasyonu

### Özet Çubuğu Bağlantıları

Router konsolu özet çubuğuna tıklanabilir bağlantı ekle:

```properties
consoleLinkName=My Plugin
consoleLinkURL=/myplugin/
consoleLinkTooltip=Open My Plugin Interface
```
Yerelleştirilmiş sürümler:

```properties
consoleLinkName_de=Mein Plugin
consoleLinkTooltip_de=Öffne Mein Plugin Schnittstelle
```
### Konsol Simgeleri

**Görüntü Dosyası (0.9.20'den beri):**

```properties
console-icon=/myicon.png
```
`consoleLinkURL` belirtilmişse (0.9.53'ten beri) yol buna göre görelidir, aksi takdirde web uygulaması adına görelidir.

**Gömülü Simge (0.9.25 sürümünden beri):**

```properties
icon-code=iVBORw0KGgoAAAANSUhEUgAAA...Base64EncodedPNG...
```
Şununla oluşturun:

```bash
base64 -w 0 icon-32x32.png
```
Ya da Java:

```bash
java -cp i2p.jar net.i2p.data.Base64 encode icon.png
```
Gereksinimler: - 32x32 piksel - PNG formatı - Base64 ile kodlanmış (satır sonu olmadan)

---

## Uluslararasılaştırma

### Çeviri Paketleri

**I2P Temel Çevirileri için:** - JAR'ları `console/locale/` dizinine yerleştirin - Mevcut I2P uygulamaları için kaynak demetlerini içerir - Adlandırma: `messages_xx.properties` (xx = dil kodu)

**Eklentiye Özel Çeviriler İçin:** - `console/webapps/*.war` içine dahil edin - Veya `lib/*.jar` içine dahil edin - Standart Java ResourceBundle (kaynak paketi) yaklaşımını kullanın

### plugin.config içindeki yerelleştirilmiş dizeler

```properties
description=My awesome plugin
description_de=Mein tolles Plugin
description_fr=Mon plugin génial
description_es=Mi plugin increíble
```
Desteklenen alanlar: - `description_xx` - `consoleLinkName_xx` - `consoleLinkTooltip_xx`

### Konsol Tema Çevirisi

`console/themes/` içindeki temalar, tema arama yoluna otomatik olarak eklenir.

---

## Platforma Özgü Eklentiler

### Ayrı Paketler Yaklaşımı

Her platform için farklı eklenti adları kullanın:

```properties
# Windows package
name=myplugin-windows

# Linux package  
name=myplugin-linux

# macOS package
name=myplugin-mac
```
### Değişken Yerine Koyma Yaklaşımı

Platform değişkenleri içeren tek bir plugin.config:

```properties
name=myplugin
updateURL.su3=http://myplugin.i2p/downloads/myplugin-$OS-$ARCH.su3
```
clients.config dosyasında:

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myapp-$OS-$ARCH
```
### Çalışma Zamanı İşletim Sistemi Tespiti

Koşullu yürütme için Java yaklaşımı:

```java
String os = System.getProperty("os.name").toLowerCase();
if (os.contains("win")) {
    // Windows-specific code
} else if (os.contains("nix") || os.contains("nux")) {
    // Linux-specific code
} else if (os.contains("mac")) {
    // macOS-specific code
}
```
---

## Sorun Giderme

### Yaygın Sorunlar

**Eklenti Başlatılmıyor:** 1. I2P sürüm uyumluluğunu kontrol edin (`min-i2p-version`) 2. Java sürümünü doğrulayın (`min-java-version`) 3. Hatalar için router günlüklerini kontrol edin 4. classpath (sınıf yolu) içindeki gerekli tüm JAR'ları doğrulayın

**Web uygulamasına erişilemiyor:** 1. `webapps.config` tarafından devre dışı bırakılmadığını doğrulayın 2. Jetty sürüm uyumluluğunu kontrol edin (`min-jetty-version`) 3. `web.xml` dosyasının mevcut olduğunu doğrulayın (annotation scanning [annotasyon taraması] desteklenmez) 4. Çakışan web uygulaması adlarını kontrol edin

**Güncelleme Başarısız:** 1. Sürüm dizesinin artırıldığını doğrulayın 2. İmzanın imzalama anahtarıyla eşleştiğini kontrol edin 3. Eklenti adının yüklü sürümle eşleştiğinden emin olun 4. `update-only`/`install-only` ayarlarını gözden geçirin

**Harici Program Durmuyor:** 1. Otomatik yaşam döngüsü için ShellService kullanın 2. Uygun `stopargs` işleme mantığını uygulayın 3. PID dosyası temizliğini kontrol edin 4. Sürecin sonlandığını doğrulayın

### Hata Ayıklama Günlüğü

router'da hata ayıklama günlüğünü etkinleştir:

```
logger.record.net.i2p.router.web.ConfigPluginsHandler=DEBUG
```
Günlükleri kontrol edin:

```
~/.i2p/logs/log-router-0.txt
```
---

## Referans Bilgileri

### Resmi Spesifikasyonlar

- [Eklenti Belirtimi](/docs/specs/plugin/)
- [Yapılandırma Biçimi](/docs/specs/configuration/)
- [Güncelleme Belirtimi](/docs/specs/updates/)
- [Kriptografi](/docs/specs/cryptography/)

### I2P Sürüm Geçmişi

**Güncel Sürüm:** - **I2P 2.10.0** (8 Eylül 2025)

**0.9.53'ten beri önemli sürümler:** - 2.10.0 (Eylül 2025) - Java 17+ duyurusu - 2.9.0 (Haziran 2025) - Java 17+ uyarısı - 2.8.0 (Ekim 2024) - Kuantum sonrası kriptografi testleri - 2.6.0 (Mayıs 2024) - I2P-over-Tor engellemesi - 2.4.0 (Aralık 2023) - NetDB güvenlik iyileştirmeleri - 2.2.0 (Mart 2023) - Tıkanıklık kontrolü - 2.1.0 (Ocak 2023) - Ağ iyileştirmeleri - 2.0.0 (Kasım 2022) - SSU2 taşıma protokolü - 1.7.0/0.9.53 (Şubat 2022) - ShellService, değişken ikamesi - 0.9.15 (Eylül 2014) - SU3 formatı tanıtıldı

**Sürüm Numaralandırma:** - 0.9.x serisi: 0.9.53 sürümüne kadar - 2.x serisi: 2.0.0 ile başlar (SSU2'nin tanıtımı)

### Geliştirici Kaynakları

**Kaynak Kodu:** - Ana depo: https://i2pgit.org/I2P_Developers/i2p.i2p - GitHub aynası: https://github.com/i2p/i2p.i2p

**Eklenti Örnekleri:** - zzzot (BitTorrent izleyici) - pebble (Blog platformu) - i2p-bote (Sunucusuz e-posta) - orchid (Tor istemcisi) - seedless (Eş değişimi)

**Derleme Araçları:** - makeplugin.sh - Anahtar üretimi ve imzalama - i2p.scripts deposunda bulunur - su3 (imzalı güncelleme dosyası formatı) oluşturma ve doğrulamayı otomatikleştirir

### Topluluk Desteği

**Forumlar:** - [I2P Forumu](https://i2pforum.net/) - [zzz.i2p](http://zzz.i2p/) (I2P içi)

**IRC/Sohbet:** - #i2p-dev OFTC'de - I2P ağı içinde IRC

---

## Ek A: Tam plugin.config Örneği

```properties
# Required fields
name=example-plugin
signer=developer@mail.i2p
version=1.2.3

# Update configuration
updateURL.su3=http://example.i2p/plugins/example-$OS-$ARCH.su3
min-i2p-version=2.0.0
min-java-version=17

# Display information
date=1698796800000
author=Example Developer <developer@mail.i2p>
websiteURL=http://example.i2p/
license=Apache-2.0

description=An example I2P plugin demonstrating best practices
description_de=Ein Beispiel-I2P-Plugin zur Demonstration bewährter Praktiken
description_es=Un plugin I2P de ejemplo que demuestra las mejores prácticas

# Console integration
consoleLinkName=Example Plugin
consoleLinkName_de=Beispiel-Plugin
consoleLinkURL=/example/
consoleLinkTooltip=Open the Example Plugin control panel
consoleLinkTooltip_de=Öffne das Beispiel-Plugin-Kontrollfeld
console-icon=/icon.png

# Installation behavior
dont-start-at-install=false
router-restart-required=false

# Platform requirements (informational)
required-platform-OS=All platforms supported
other-requirements=Requires 512MB free disk space
```
---

## Ek B: Eksiksiz clients.config örneği

```properties
# Main service client (managed)
clientApp.0.main=com.example.plugin.MainService
clientApp.0.name=Example Plugin Main Service
clientApp.0.delay=30
clientApp.0.args=$PLUGIN/config.properties --port=7656
clientApp.0.stopargs=shutdown
clientApp.0.uninstallargs=cleanup
clientApp.0.classpath=$PLUGIN/lib/example.jar,$I2P/lib/i2p.jar,$I2P/lib/mstreaming.jar

# External program via ShellService
clientApp.1.main=net.i2p.apps.ShellService
clientApp.1.name=Example Native Helper
clientApp.1.delay=35
clientApp.1.args=$PLUGIN/bin/helper-$OS-$ARCH --config $PLUGIN/helper.conf
clientApp.1.classpath=$I2P/lib/i2p.jar

# Jetty eepsite
clientApp.2.main=net.i2p.jetty.JettyStart
clientApp.2.name=Example Eepsite
clientApp.2.delay=40
clientApp.2.args=$PLUGIN/eepsite/jetty.xml
clientApp.2.stopargs=$PLUGIN/eepsite/jetty.xml stop
clientApp.2.classpath=$PLUGIN/lib/example-web.jar,$I2P/lib/i2p.jar

# I2PTunnel for eepsite
clientApp.3.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.3.name=Example Eepsite Tunnel
clientApp.3.delay=45
clientApp.3.args=$PLUGIN/eepsite/i2ptunnel.config
```
---

## Ek C: Eksiksiz webapps.config Örneği

```properties
# Disable autostart for admin webapp
webapps.example-admin.startOnLoad=false

# Main webapp with classpath
webapps.example.startOnLoad=true
webapps.example.classpath=$PLUGIN/lib/example-core.jar,$PLUGIN/lib/commons-utils.jar,$I2P/lib/jstl.jar,$I2P/lib/standard.jar

# Legacy support (pre-0.7.12-9)
plugin.example.startOnLoad=true
```
---

## Ek D: Geçiş Kontrol Listesi (0.9.53'ten 2.10.0'a)

### Gerekli Değişiklikler

- [ ] **Derleme sürecinden Pack200 sıkıştırmasını kaldırın**
  - Ant/Maven/Gradle betiklerinden pack200 görevlerini kaldırın
  - Mevcut eklentileri pack200 olmadan yeniden yayımlayın

- [ ] **Java sürüm gereksinimlerini gözden geçirin**
  - Yeni özellikler için Java 11+ gerektirmeyi değerlendirin
  - I2P 2.11.0'da Java 17+ gereksinimi için plan yapın
  - plugin.config dosyasındaki `min-java-version` ayarını güncelleyin

- [ ] **Dokümantasyonu güncelle**
  - Pack200 referanslarını kaldır
  - Java sürüm gereksinimlerini güncelle
  - I2P sürüm referanslarını güncelle (0.9.x → 2.x)

### Önerilen Değişiklikler

- [ ] **Kriptografik imzaları güçlendirin**
  - Henüz yapılmadıysa XPI2P'den SU3'e geçin
  - Yeni eklentiler için RSA-4096 anahtarları kullanın

- [ ] **Yeni özelliklerden yararlanın (0.9.53+ kullanıyorsanız)**
  - Platforma özel güncellemeler için `$OS` / `$ARCH` değişkenlerini kullanın
  - Harici programlar için ShellService kullanın
  - Geliştirilmiş web uygulaması classpath'ini kullanın (herhangi bir war adıyla çalışır)

- [ ] **Uyumluluğu test edin**
  - I2P 2.10.0 üzerinde test edin
  - Java 8, 11, 17 ile doğrulayın
  - Windows, Linux, macOS üzerinde kontrol edin

### İsteğe Bağlı Geliştirmeler

- [ ] Uygun bir ServletContextListener (Servlet bağlamı dinleyicisi) uygulayın
- [ ] Yerelleştirilmiş açıklamalar ekleyin
- [ ] Konsol simgesi ekleyin
- [ ] Kapatma işlemi yönetimini iyileştirin
- [ ] Kapsamlı günlükleme ekleyin
- [ ] Otomatikleştirilmiş testler yazın
