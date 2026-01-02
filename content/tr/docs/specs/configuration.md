---
title: "Router Yapılandırması"
description: "I2P router'ları ve istemcileri için yapılandırma seçenekleri ve biçimleri"
slug: "configuration"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Genel Bakış

Bu belge, router ve çeşitli uygulamalar tarafından kullanılan I2P yapılandırma dosyalarının kapsamlı bir teknik şartnamesini sunar. Dosya biçimi belirtimleri, özellik tanımları ve I2P kaynak kodu ile resmi dokümantasyonla karşılaştırılarak doğrulanmış gerçekleme ayrıntılarını kapsar.

### Kapsam

- Router yapılandırma dosyaları ve biçimleri
- İstemci uygulama yapılandırmaları
- I2PTunnel tunnel yapılandırmaları
- Dosya biçimi spesifikasyonları ve uygulanması
- Sürüme özgü özellikler ve kullanımdan kaldırmalar

### Uygulama Notları

Yapılandırma dosyaları, I2P çekirdek kitaplığındaki `DataHelper.loadProps()` ve `storeProps()` yöntemleri kullanılarak okunup yazılır. Dosya biçimi, I2P protokollerinde kullanılan serileştirilmiş biçimden önemli ölçüde farklıdır (bkz. [Ortak Yapılar Belirtimi - Tür Eşlemesi](/docs/specs/common-structures/#type-mapping)).

---

## Genel Yapılandırma Dosyası Biçimi

I2P yapılandırma dosyaları, belirli istisna ve kısıtlamalar içeren değiştirilmiş bir Java Properties biçimini kullanır.

### Biçim Belirtimi

[Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) temel alınır, ancak aşağıdaki kritik farklılıklar vardır:

#### Kodlama

- **MUTLAKA** UTF-8 kodlaması kullanılmalıdır (standart Java Properties'te olduğu gibi ISO-8859-1 DEĞİL)
- Gerçekleme: Tüm dosya işlemleri için `DataHelper.getUTF8()` yardımcı işlevlerini kullanır

#### Kaçış Dizileri

- **HİÇBİR** kaçış dizisi tanınmaz (ters eğik çizgi `\` dahil)
- Satır devamı **DESTEKLENMEZ**
- Ters eğik çizgi karakterleri olduğu gibi yorumlanır

#### Yorum Karakterleri

- `#` bir satırın herhangi bir yerinde yorum başlatır
- `;` yalnızca 1. sütunda yorum başlatır
- `!` yorum **BAŞLATMAZ** (Java Properties'den farklıdır)

#### Anahtar-Değer Ayırıcıları

- `=` **YALNIZCA** geçerli anahtar-değer ayırıcısıdır
- `:` bir ayırıcı olarak **TANINMAZ**
- Boşluk karakterleri bir ayırıcı olarak **TANINMAZ**

#### Boşluk Karakterlerinin Yönetimi

- Anahtarlardaki baş ve sondaki boşluk karakterleri **KIRPILMAZ**
- Değerlerdeki baş ve sondaki boşluk karakterleri **KIRPILIR**

#### Satır İşleme

- `=` içermeyen satırlar yok sayılır (yorum veya boş satır olarak değerlendirilir)
- Boş değerler (`key=`) 0.9.10 sürümünden itibaren desteklenir
- Boş değerlere sahip anahtarlar normal şekilde depolanır ve okunur

#### Karakter Kısıtlamaları

**Anahtarlar şunları içeremez**: - `#` (kare/diyez işareti) - `=` (eşittir işareti) - `\n` (yeni satır karakteri) - `;` (noktalı virgül) ile başlayamaz

**Değerler şunları İÇEREMEZ**: - `#` (kare/diyez işareti) - `\n` (yeni satır karakteri) - Başında veya sonunda `\r` olamaz (satır başı) - Başında veya sonunda boşluk olamaz (otomatik olarak kırpılır)

### Dosya Sıralama

Yapılandırma dosyalarının anahtara göre sıralanması gerekmez. Ancak, çoğu I2P uygulaması, aşağıdakileri kolaylaştırmak için yapılandırma dosyalarını yazarken anahtarları alfabetik olarak sıralar: - Elle düzenleme - Sürüm kontrolü diff (fark karşılaştırma) işlemleri - İnsan tarafından okunabilirlik

### Uygulama Ayrıntıları

#### Yapılandırma Dosyalarını Okuma

```java
// Method signature from net.i2p.data.DataHelper
public static Properties loadProps(File file)
```
**Davranış**: - UTF-8 ile kodlanmış dosyaları okur - Yukarıda açıklanan tüm biçim kurallarını uygular - Karakter kısıtlamalarını doğrular - Dosya yoksa boş bir Properties nesnesi döndürür - Okuma hatalarında `IOException` fırlatır

#### Yapılandırma Dosyaları Yazma

```java
// Method signature from net.i2p.data.DataHelper
public static void storeProps(Properties props, File file)
```
**Davranış**: - UTF-8 ile kodlanmış dosyalar yazar - Anahtarları alfabetik olarak sıralar (OrderedProperties kullanılmadıkça) - Sürüm 0.8.1 itibarıyla dosya izinlerini 600 moduna (yalnızca kullanıcı okuma/yazma) ayarlar - Anahtar veya değerlerdeki geçersiz karakterler için `IllegalArgumentException` fırlatır - Yazma hataları için `IOException` fırlatır

#### Biçim Doğrulaması

Uygulama sıkı bir doğrulama yapar: - Anahtarlar ve değerler izin verilmeyen karakterler açısından kontrol edilir - Geçersiz girdiler yazma işlemleri sırasında istisnalara neden olur - Okuma, biçimi bozuk satırları sessizce yok sayar (`=` olmayan satırlar)

### Biçim Örnekleri

#### Geçerli Yapılandırma Dosyası

```properties
# This is a comment
; This is also a comment (column 1 only)
key.with.dots=value with spaces
another_key=value=with=equals
empty.value=
numeric.value=12345
unicode.value=こんにちは
```
#### Geçersiz Yapılandırma Örnekleri

```properties
# INVALID: Key contains equals sign
invalid=key=value

# INVALID: Key contains hash
invalid#key=value

# INVALID: Value contains newline (implicit)
key=value
continues here

# INVALID: Semicolon comment not in column 1 (treated as key)
 ; not.a.comment=value
```
---

## Çekirdek Kitaplığı ve Router Yapılandırması

### İstemci Yapılandırması (clients.config)

**Konum**: `$I2P_CONFIG_DIR/clients.config` (eski) veya `$I2P_CONFIG_DIR/clients.config.d/` (modern)   **Yapılandırma Arayüzü**: Router konsolu `/configclients` adresinde   **Biçim Değişikliği**: Sürüm 0.9.42 (Ağustos 2019)

#### Dizin Yapısı (Sürüm 0.9.42+)

0.9.42 sürümünden itibaren, varsayılan clients.config dosyası otomatik olarak ayrı yapılandırma dosyalarına ayrılır:

```
$I2P_CONFIG_DIR/
├── clients.config.d/
│   ├── 00-webConsole.config
│   ├── 01-i2ptunnel.config
│   ├── 02-i2psnark.config
│   ├── 03-susidns.config
│   └── ...
└── clients.config (legacy, auto-migrated)
```
**Geçiş Davranışı**: - 0.9.42+ sürümüne yükseltmeden sonraki ilk çalıştırmada, monolitik dosya otomatik olarak bölünür - Bölünmüş dosyalardaki özelliklerin başına `clientApp.0.` öneki eklenir - Geriye dönük uyumluluk için eski biçim hâlâ desteklenir - Bölünmüş biçim, modüler paketlemeyi ve eklenti yönetimini mümkün kılar

#### Özellik Biçimi

Satırlar `clientApp.x.prop=val` biçimindedir; burada `x` uygulama numarasıdır.

**Uygulama numaralandırma gereksinimleri**: - 0 ile başlamalıdır - Ardışık olmalıdır (atlama olmamalı) - Sıralama, başlatma sırasını belirler

#### Zorunlu Özellikler

##### ana

- **Tür**: String (tam nitelikli sınıf adı)
- **Gerekli**: Evet
- **Açıklama**: Bu sınıftaki kurucu (constructor) veya `main()` metodu, istemci türüne (yönetilen vs. yönetilmeyen) bağlı olarak çağrılacaktır
- **Örnek**: `clientApp.0.main=net.i2p.router.web.RouterConsoleRunner`

#### İsteğe Bağlı Özellikler

##### ad

- **Tür**: Dize
- **Gerekli**: Hayır
- **Açıklama**: router konsolunda gösterilen görünen ad
- **Örnek**: `clientApp.0.name=Router Console`

##### args

- **Tür**: Dize (boşluk veya sekme ile ayrılmış)
- **Gerekli**: Hayır
- **Açıklama**: Ana sınıfın kurucusuna veya main() yöntemine geçirilen argümanlar
- **Tırnak kullanımı**: Boşluk veya sekme içeren argümanlar `'` veya `"` ile tırnak içine alınabilir
- **Örnek**: `clientApp.0.args=-d $CONFIG/eepsite`

##### gecikme

- **Tür**: Tamsayı (saniye)
- **Gerekli**: Hayır
- **Varsayılan**: 120
- **Açıklama**: İstemciyi başlatmadan önce beklenecek saniye sayısı
- **Geçersiz kılmalar**: `onBoot=true` tarafından geçersiz kılınır (gecikmeyi 0'a ayarlar)
- **Özel Değerler**:
  - `< 0`: router RUNNING durumuna ulaşana kadar bekler, sonra yeni bir iş parçacığında hemen başlatır
  - `= 0`: Aynı iş parçacığında hemen çalıştırır (istisnalar konsola iletilir)
  - `> 0`: Gecikmeden sonra yeni bir iş parçacığında başlatır (istisnalar kaydedilir, iletilmez)

##### onBoot

- **Tür**: Boolean
- **Gerekli**: Hayır
- **Varsayılan**: false
- **Açıklama**: Gecikmeyi 0'a zorlar, açıkça belirtilen gecikme ayarını geçersiz kılar
- **Kullanım Durumu**: Kritik servisleri router önyüklemesinde hemen başlat

##### startOnLoad

- **Tür**: Boolean
- **Gerekli**: Hayır
- **Varsayılan**: true
- **Açıklama**: İstemcinin hiç başlatılıp başlatılmayacağı
- **Kullanım Durumu**: Yapılandırmayı kaldırmadan istemcileri devre dışı bırakma

#### Eklentiye Özel Özellikler

Bu özellikler yalnızca eklentiler tarafından kullanılır (çekirdek istemciler tarafından değil):

##### stopargs (durdurma argümanları)

- **Tür**: Dize (boşluk veya sekme ile ayrılmış)
- **Açıklama**: İstemciyi durdurmak için iletilen argümanlar
- **Değişken Yerine Koyma**: Evet (aşağıya bakın)

##### uninstallargs

- **Tür**: Dize (boşluk veya sekme ile ayrılmış)
- **Açıklama**: İstemciyi kaldırma işlemine iletilen argümanlar
- **Değişken yerine koyma**: Evet (aşağıya bakın)

##### sınıf yolu

- **Tür**: String (virgülle ayrılmış yollar)
- **Açıklama**: İstemci için ek classpath öğeleri
- **Değişken ikamesi**: Evet (aşağıya bakın)

#### Değişken Yerine Koyma (Yalnızca Eklentiler)

Aşağıdaki değişkenler, eklentiler için `args`, `stopargs`, `uninstallargs`, ve `classpath` içinde yerine konur:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P installation directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>/usr/share/i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User configuration directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p/plugins/foo</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$OS</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Operating system name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>linux</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$ARCH</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Architecture name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>amd64</code></td>
    </tr>
  </tbody>
</table>
**Not**: Değişken yerine koyma yalnızca eklentiler için uygulanır, çekirdek istemcilerde uygulanmaz.

#### İstemci Türleri

##### Yönetilen İstemciler

- Kurucu, `RouterContext` ve `ClientAppManager` parametreleriyle çağrılır
- İstemci, `ClientApp` arayüzünü uygulamalıdır
- Yaşam döngüsü router tarafından kontrol edilir
- Dinamik olarak başlatılabilir, durdurulabilir ve yeniden başlatılabilir

##### Yönetilmeyen İstemciler

- `main(String[] args)` metodu çağrılır
- Ayrı bir iş parçacığında çalıştırılır
- Yaşam döngüsü router tarafından yönetilmez
- Eski istemci türü

#### Örnek Yapılandırma

```properties
# Router Console (core client)
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=-d $CONFIG/eepsite
clientApp.0.delay=0
clientApp.0.onBoot=true
clientApp.0.startOnLoad=true

# I2PTunnel (core client)
clientApp.1.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.1.name=I2PTunnel
clientApp.1.args=
clientApp.1.delay=120
clientApp.1.startOnLoad=true

# Plugin Example
clientApp.2.main=org.example.plugin.PluginMain
clientApp.2.name=Example Plugin
clientApp.2.args=-config $PLUGIN/config.properties
clientApp.2.stopargs=-shutdown
clientApp.2.uninstallargs=-remove $PLUGIN
clientApp.2.classpath=$PLUGIN/lib/plugin.jar,$PLUGIN/lib/dep.jar
clientApp.2.delay=240
clientApp.2.startOnLoad=true
```
---

### Günlükleyici Yapılandırması (logger.config)

**Konum**: `$I2P_CONFIG_DIR/logger.config`   **Yapılandırma Arayüzü**: Router konsolunda `/configlogging`

#### Özellikler Referansı

##### Konsol Arabellek Yapılandırması

###### logger.consoleBufferSize

- **Tür**: Tamsayı
- **Varsayılan**: 20
- **Açıklama**: Konsolda arabelleğe alınacak en fazla günlük mesajı sayısı
- **Aralık**: 1-1000 önerilir

##### Tarih ve Saat Biçimlendirme

###### logger.dateFormat

- **Tür**: String (SimpleDateFormat deseni)
- **Varsayılan**: Sistem yerel ayarından
- **Örnek**: `HH:mm:ss.SSS`
- **Belgelendirme**: [Java SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)

##### Günlük Seviyeleri

###### logger.defaultLevel

- **Tür**: Enum (numaralandırma)
- **Varsayılan**: ERROR
- **Değerler**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Açıklama**: Tüm sınıflar için varsayılan günlükleme düzeyi

###### logger.minimumOnScreenLevel

- **Tür**: Enum (numaralandırma)
- **Varsayılan**: CRIT
- **Değerler**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Açıklama**: Ekranda gösterilen iletiler için en düşük düzey

###### logger.record.{class}

- **Tür**: Enum
- **Değerler**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Açıklama**: Sınıf başına günlükleme düzeyi geçersiz kılma
- **Örnek**: `logger.record.net.i2p.router.transport.udp=DEBUG`

##### Görüntüleme Seçenekleri

###### logger.displayOnScreen

- **Tür**: Boolean (mantıksal tür)
- **Varsayılan**: true
- **Açıklama**: Günlük iletilerinin konsol çıktısında gösterilip gösterilmeyeceği

###### logger.dropDuplicates

- **Tür**: Boolean (mantıksal)
- **Varsayılan**: true
- **Açıklama**: Ardışık yinelenen günlük iletilerini yoksay

###### logger.dropOnOverflow

- **Tür**: Boolean
- **Varsayılan**: false
- **Açıklama**: Arabellek dolu olduğunda mesajları düşür (bloklayıcı bekleme yerine)

##### Boşaltma Davranışı

###### logger.flushInterval

- **Tür**: Tamsayı (saniye)
- **Varsayılan**: 29
- **İtibaren**: Sürüm 0.9.18
- **Açıklama**: Günlük arabelleğinin diske ne sıklıkla yazılacağı

##### Biçim Yapılandırması

###### logger.format

- **Tür**: String (karakter dizisi)
- **Açıklama**: Günlük iletisi biçim şablonu
- **Biçim Karakterleri**:
  - `d` = tarih/saat
  - `c` = sınıf adı
  - `t` = iş parçacığı adı
  - `p` = öncelik (günlük düzeyi)
  - `m` = ileti
- **Örnek**: `dctpm` şunu üretir: `[zaman damgası] [sınıf] [iş parçacığı] [düzey] ileti`

##### Sıkıştırma (Sürüm 0.9.56+)

###### logger.gzip

- **Tür**: Boolean
- **Varsayılan**: false
- **Şu sürümden beri**: Sürüm 0.9.56
- **Açıklama**: Döndürülen günlük dosyaları için gzip sıkıştırmasını etkinleştirir

###### logger.minGzipSize

- **Tür**: Tamsayı (bayt)
- **Varsayılan**: 65536
- **Sürüm**: 0.9.56'dan beri
- **Açıklama**: Sıkıştırmayı tetiklemek için minimum dosya boyutu (varsayılan 64 KB)

##### Dosya Yönetimi

###### logger.logBufferSize

- **Tür**: Tamsayı (bayt)
- **Varsayılan**: 1024
- **Açıklama**: Boşaltmadan önce arabelleğe alınacak en fazla ileti sayısı

###### logger.logFileName

- **Tür**: Dize (dosya yolu)
- **Varsayılan**: `logs/log-@.txt`
- **Açıklama**: Günlük dosyası adlandırma deseni (`@` yerine döndürme numarası konur)

###### logger.logFilenameOverride

- **Tür**: Dize (dosya yolu)
- **Açıklama**: Günlük dosya adını geçersiz kılma (döndürme desenini devre dışı bırakır)

###### logger.logFileSize

- **Tür**: Dize (birimle birlikte boyut)
- **Varsayılan**: 10M
- **Birimler**: K (kilobayt), M (megabayt), G (gigabayt)
- **Örnek**: `50M`, `1G`

###### logger.logRotationLimit

- **Tür**: Tamsayı
- **Varsayılan**: 2
- **Açıklama**: En yüksek döndürme dosyası numarası (log-0.txt'den log-N.txt'ye kadar)

#### Örnek Yapılandırma

```properties
# Basic logging configuration
logger.consoleBufferSize=50
logger.dateFormat=yyyy-MM-dd HH:mm:ss.SSS
logger.defaultLevel=WARN
logger.displayOnScreen=true
logger.dropDuplicates=true
logger.dropOnOverflow=false

# Flushing and format
logger.flushInterval=30
logger.format=dctpm

# File management
logger.logBufferSize=2048
logger.logFileName=logs/log-@.txt
logger.logFileSize=25M
logger.logRotationLimit=5

# Compression (0.9.56+)
logger.gzip=true
logger.minGzipSize=131072

# On-screen filtering
logger.minimumOnScreenLevel=ERROR

# Per-class overrides
logger.record.net.i2p.router.transport=INFO
logger.record.net.i2p.router.tunnel=DEBUG
logger.record.net.i2p.crypto=WARN
```
---

### Eklenti Yapılandırması

#### Bireysel Eklenti Yapılandırması (plugins/*/plugin.config)

**Konum**: `$I2P_CONFIG_DIR/plugins/{plugin-name}/plugin.config`   **Biçim**: Standart I2P yapılandırma dosyası biçimi   **Belgeler**: [Eklenti Belirtimi](/docs/specs/plugin/)

##### Gerekli Özellikler

###### ad

- **Type**: Dize
- **Required**: Evet
- **Description**: Eklentinin görünen adı
- **Example**: `name=I2P Plugin Example`

###### anahtar

- **Tür**: Dize (genel anahtar)
- **Zorunlu**: Evet (SU3 ile imzalanmış eklentiler için belirtmeyin)
- **Açıklama**: İmzaları doğrulamak için eklentinin imzalama genel anahtarı
- **Biçim**: Base64 ile kodlanmış imzalama anahtarı

###### imzalayan

- **Tür**: Dize
- **Gerekli**: Evet
- **Açıklama**: Eklenti imzalayıcısının kimliği
- **Örnek**: `signer=user@example.i2p`

###### sürüm

- **Tür**: String (VersionComparator biçimi)
- **Gerekli**: Evet
- **Açıklama**: Güncelleme denetimi için eklenti sürümü
- **Biçim**: Semantik sürümleme veya özel karşılaştırılabilir biçim
- **Örnek**: `version=1.2.3`

##### Görüntü Özellikleri

###### tarih

- **Tip**: Long (Unix zaman damgası milisaniye cinsinden)
- **Açıklama**: Eklentinin yayın tarihi

###### yazar

- **Tür**: String
- **Açıklama**: Eklenti yazarının adı

###### websiteURL

- **Tür**: String (URL)
- **Açıklama**: Eklenti web sitesi URL’si

###### updateURL

- **Tür**: Dize (URL)
- **Açıklama**: Eklenti için güncelleme denetimi URL'si

###### updateURL.su3

- **Tür**: Dize (URL)
- **Sürüm**: 0.9.15'ten beri
- **Açıklama**: SU3 biçiminde güncelleme URL'si (tercih edilen)

###### açıklama

- **Tür**: String
- **Açıklama**: İngilizce eklenti açıklaması

###### description_{language}

- **Tip**: String
- **Açıklama**: Yerelleştirilmiş eklenti açıklaması
- **Örnek**: `description_de=Deutsche Beschreibung`

###### lisans

- **Tür**: Dize
- **Açıklama**: Eklenti lisans tanımlayıcısı
- **Örnek**: `license=Apache 2.0`

##### Kurulum Özellikleri

###### dont-start-at-install

- **Tür**: Boolean (mantıksal)
- **Varsayılan**: false
- **Açıklama**: Kurulumdan sonra otomatik başlamayı engeller

###### router'ın yeniden başlatılması gerekiyor

- **Tür**: Boolean (mantıksal)
- **Varsayılan**: false
- **Açıklama**: Kurulumdan sonra router’ın yeniden başlatılmasını gerektirir

###### yalnızca kurulum

- **Tür**: Boolean (mantıksal)
- **Varsayılan**: false
- **Açıklama**: Yalnızca bir kez yükle (güncelleme yok)

###### yalnızca güncelleme

- **Tür**: Boolean
- **Varsayılan**: false
- **Açıklama**: Yalnızca mevcut kurulumu güncelle (sıfırdan kurulum yok)

##### Örnek Eklenti Yapılandırması

```properties
# Required properties
name=Example I2P Plugin
signer=developer@mail.i2p
version=1.5.0

# Display properties
author=Plugin Developer
websiteURL=http://plugin.example.i2p
updateURL=http://plugin.example.i2p/update.xpi2p
updateURL.su3=http://plugin.example.i2p/update.su3
description=Example plugin demonstrating configuration
description_de=Beispiel-Plugin zur Demonstration der Konfiguration
license=MIT

# Installation behavior
dont-start-at-install=false
router-restart-required=false
```
#### Genel Eklenti Yapılandırması (plugins.config)

**Konum**: `$I2P_CONFIG_DIR/plugins.config`   **Amaç**: Yüklü eklentileri genel olarak etkinleştirmek/devre dışı bırakmak

##### Özellik Formatı

```properties
plugin.{name}.startOnLoad=true|false
```
- `{name}`: plugin.config içindeki eklenti adı
- `startOnLoad`: router (yönlendirici) başlatılırken eklentinin başlatılıp başlatılmayacağı

##### Örnek

```properties
plugin.i2psnark.startOnLoad=true
plugin.susimail.startOnLoad=true
plugin.susidns.startOnLoad=true
plugin.i2pbote.startOnLoad=false
```
---

### Web Uygulamaları Yapılandırması (webapps.config)

**Konum**: `$I2P_CONFIG_DIR/webapps.config`   **Amaç**: Web uygulamalarını etkinleştirme/devre dışı bırakma ve yapılandırma

#### Özellik Biçimi

##### webapps.{name}.startOnLoad

- **Tür**: Boolean
- **Açıklama**: router başlatıldığında web uygulamasının başlatılıp başlatılmayacağı
- **Biçim**: `webapps.{name}.startOnLoad=true|false`

##### webapps.{name}.classpath

- **Tür**: String (boşluk veya virgülle ayrılmış yollar)
- **Açıklama**: web uygulaması için ek classpath (sınıf yolu) öğeleri
- **Biçim**: `webapps.{name}.classpath=[paths]`

#### Değişken Yerine Koyma

Yollar aşağıdaki değişken ikamelerini destekler:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User config directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin webapps</td>
    </tr>
  </tbody>
</table>
#### Sınıf Yolu Çözümlemesi

- **Çekirdek web uygulamaları**: Yollar `$I2P/lib` dizinine göredir
- **Eklenti web uygulamaları**: Yollar `$CONFIG/plugins/{appname}/lib` dizinine göredir

#### Örnek Yapılandırma

```properties
# Router console
webapps.routerconsole.startOnLoad=true
webapps.routerconsole.classpath=routerconsole.jar

# I2PSnark
webapps.i2psnark.startOnLoad=true
webapps.i2psnark.classpath=i2psnark.jar

# SusiDNS
webapps.susidns.startOnLoad=true
webapps.susidns.classpath=susidns.jar

# Plugin webapp example
webapps.exampleplugin.startOnLoad=false
webapps.exampleplugin.classpath=$PLUGIN/lib/webapp.jar,$PLUGIN/lib/deps.jar
```
---

### Router Yapılandırması (router.config)

**Konum**: `$I2P_CONFIG_DIR/router.config`   **Yapılandırma Arabirimi**: router konsolu `/configadvanced` adresinde   **Amaç**: Temel router ayarları ve ağ parametreleri

#### Yapılandırma Kategorileri

##### Ağ Yapılandırması

Bant genişliği ayarları:

```properties
i2np.bandwidth.inboundKBytesPerSecond=100
i2np.bandwidth.outboundKBytesPerSecond=50
i2np.bandwidth.share.percentage=80
```
Taşıma yapılandırması:

```properties
# NTCP (TCP-based transport)
i2np.ntcp.port=8887
i2np.ntcp.enable=true
i2np.ntcp.autoip=true

# SSU (UDP-based transport)
i2np.udp.port=8887
i2np.udp.enable=true

# UPnP/NAT-PMP
i2np.upnp.enable=true
```
##### Router Davranışı

```properties
# Tunnel participation
router.maxParticipatingTunnels=200
router.sharePercentage=80

# Updates
router.updatePolicy=notify
router.updateURL=http://update.i2p2.i2p/

# Network integration
router.hiddenMode=false
router.clockSkewOffset=0
```
##### Konsol Yapılandırması

```properties
# Language and display
routerconsole.lang=en
routerconsole.country=US
routerconsole.summaryRefresh=60

# Browser
routerconsole.browser=default

# Security
routerconsole.enableCompression=true
```
##### Zaman Yapılandırması

```properties
# NTP
time.disabled=false
time.sntpServerList=0.pool.ntp.org,1.pool.ntp.org
```
**Not**: Router yapılandırması kapsamlıdır. Tam özellik başvurusu için `/configadvanced` adresindeki router konsoluna bakın.

---

## Uygulama Yapılandırma Dosyaları

### Adres Defteri Yapılandırması (addressbook/config.txt)

**Konum**: `$I2P_CONFIG_DIR/addressbook/config.txt`   **Uygulama**: SusiDNS   **Amaç**: Ana makine adı çözümleme ve adres defteri yönetimi

#### Dosya Konumları

##### router_addressbook

- **Varsayılan**: `../hosts.txt`
- **Açıklama**: Ana adres defteri (sistem genelindeki ana bilgisayar adları)
- **Biçim**: Standart hosts dosyası biçimi

##### privatehosts.txt

- **Konum**: `$I2P_CONFIG_DIR/addressbook/privatehosts.txt`
- **Açıklama**: Özel ana bilgisayar adı eşlemeleri
- **Öncelik**: En yüksek (diğer tüm kaynakları geçersiz kılar)

##### userhosts.txt

- **Konum**: `$I2P_CONFIG_DIR/addressbook/userhosts.txt`
- **Açıklama**: Kullanıcı tarafından eklenen ana bilgisayar adı eşlemeleri
- **Yönetim**: SusiDNS arayüzü üzerinden

##### hosts.txt

- **Konum**: `$I2P_CONFIG_DIR/addressbook/hosts.txt`
- **Açıklama**: İndirilen genel adres defteri
- **Kaynak**: Abonelik beslemeleri

#### Adlandırma Hizmeti

##### BlockfileNamingService (blok dosyası adlandırma hizmeti) (0.8.8'den beri varsayılan)

Depolama biçimi: - **Dosya**: `hostsdb.blockfile` - **Konum**: `$I2P_CONFIG_DIR/addressbook/` - **Performans**: hosts.txt'ye göre ~10x daha hızlı sorgular - **Biçim**: İkili veritabanı biçimi

Eski adlandırma hizmeti: - **Biçim**: Düz metin hosts.txt - **Durum**: Kullanımdan kaldırıldı ancak hâlâ destekleniyor - **Kullanım Senaryosu**: El ile düzenleme, sürüm kontrolü

#### Ana Bilgisayar Adı Kuralları

I2P ana makine adları şunlara uymalıdır:

1. **TLD (üst düzey alan adı) gereksinimi**: Sonu `.i2p` ile bitmelidir
2. **Maksimum uzunluk**: Toplam 67 karakter
3. **Karakter kümesi**: `[a-z]`, `[0-9]`, `.` (nokta), `-` (tire)
4. **Büyük/küçük harf**: Yalnızca küçük harf
5. **Başlangıç kısıtlamaları**: `.` veya `-` ile başlayamaz
6. **Yasak kalıplar**: `..`, `.-` veya `-.` içeremez (0.6.1.33 sürümünden beri)
7. **Ayrılmış**: Base32 ana bilgisayar adları `*.b32.i2p` (base32.b32.i2p'nin 52 karakteri)

##### Geçerli Örnekler

```
example.i2p
my-site.i2p
test.example.i2p
site123.i2p
```
##### Geçersiz Örnekler

```
example.com          # Wrong TLD
-invalid.i2p         # Starts with hyphen
invalid..i2p         # Contains double dot
invalid.-.i2p        # Contains dot-hyphen
UPPERCASE.I2P        # Must be lowercase
verylonghostnameover67charactersthatexceedsthemaximumlength.i2p  # Too long
```
#### Abonelik Yönetimi

##### subscriptions.txt

- **Konum**: `$I2P_CONFIG_DIR/addressbook/subscriptions.txt`
- **Biçim**: Her satırda bir URL
- **Varsayılan**: `http://i2p-projekt.i2p/hosts.txt`

##### Abonelik Besleme Biçimi (0.9.26 sürümünden beri)

Meta veriler içeren gelişmiş besleme biçimi:

```
#
# I2P Address Book Subscription Feed
# Format: hostname=destination [#property=value ...]
#

example.i2p=base64destination #added=20250101 #src=manual
another.i2p=base64destination #added=20250102 #src=feed1
```
Üstveri özellikleri: - `added`: Ana makine adının eklendiği tarih (YYYYMMDD biçimi) - `src`: Kaynak tanımlayıcısı - `sig`: İsteğe bağlı imza

**Geriye dönük uyumluluk**: Basit hostname=destination biçimi hâlâ desteklenmektedir.

#### Örnek Yapılandırma

```properties
# Address book locations
router_addressbook=../hosts.txt
privatehosts.txt=$CONFIG/addressbook/privatehosts.txt
userhosts.txt=$CONFIG/addressbook/userhosts.txt
hosts.txt=$CONFIG/addressbook/hosts.txt

# Naming service
naming.service=BlockfileNamingService
naming.service.blockfile.location=$CONFIG/addressbook/hostsdb.blockfile

# Subscriptions
subscriptions.txt=$CONFIG/addressbook/subscriptions.txt
subscriptions.schedule=daily
subscriptions.proxy=false
```
---

### I2PSnark Yapılandırması (i2psnark.config.d/i2psnark.config)

**Konum**: `$I2P_CONFIG_DIR/i2psnark.config.d/i2psnark.config`   **Uygulama**: I2PSnark BitTorrent istemcisi   **Yapılandırma Arayüzü**: http://127.0.0.1:7657/i2psnark adresindeki Web arayüzü

#### Dizin Yapısı

```
$I2P_CONFIG_DIR/i2psnark.config.d/
├── i2psnark.config
├── [torrent-hash-1]/
│   └── *.config
├── [torrent-hash-2]/
│   └── *.config
└── ...
```
#### Ana Yapılandırma (i2psnark.config)

Asgari varsayılan yapılandırma:

```properties
i2psnark.dir=i2psnark
```
Web arayüzü aracılığıyla yönetilen ek özellikler:

```properties
# Basic settings
i2psnark.dir=i2psnark
i2psnark.autoStart=false
i2psnark.openTrackers=true

# Network settings
i2psnark.uploaders=8
i2psnark.upBW=40
i2psnark.seedPct=100

# I2CP settings
i2psnark.i2cpHost=127.0.0.1
i2psnark.i2cpPort=7654
```
#### Bireysel Torrent Yapılandırması

**Konum**: `$I2P_CONFIG_DIR/i2psnark.config.d/[torrent-hash]/*.config`   **Biçim**: Torrent başına ayarlar   **Yönetim**: Otomatik (web arayüzü aracılığıyla)

Özellikler şunları içerir: - Torrent'e özgü yükleme/indirme ayarları - Dosya öncelikleri - İzleyici bilgileri - Eş sınırları

**Not**: Torrent yapılandırmaları öncelikle web arayüzü üzerinden yönetilir. Elle düzenleme önerilmez.

#### Torrent Verilerinin Düzenlenmesi

Veri depolama, yapılandırmadan ayrıdır:

```
$I2P_CONFIG_DIR/i2psnark/          # Data directory
├── *.torrent                       # Torrent metadata files
├── *.torrent.downloaded/           # Downloaded file directories
├── file1.dat                       # Direct file downloads
└── ...

$I2P_CONFIG_DIR/i2psnark.config.d/ # Configuration directory
├── i2psnark.config                 # Main config
└── [hashes]/                       # Per-torrent configs
```
---

### I2PTunnel Yapılandırması (i2ptunnel.config)

**Konum**: `$I2P_CONFIG_DIR/i2ptunnel.config` (eski) veya `$I2P_CONFIG_DIR/i2ptunnel.config.d/` (modern)   **Yapılandırma Arayüzü**: Router konsolu `/i2ptunnel` adresinde   **Biçim Değişikliği**: Sürüm 0.9.42 (Ağustos 2019)

#### Dizin Yapısı (Sürüm 0.9.42+)

0.9.42 sürümünden itibaren, varsayılan i2ptunnel.config dosyası otomatik olarak bölünür:

```
$I2P_CONFIG_DIR/
├── i2ptunnel.config.d/
│   ├── http-proxy/
│   │   └── tunnel.config
│   ├── irc-proxy/
│   │   └── tunnel.config
│   ├── ssh-service/
│   │   └── tunnel.config
│   └── ...
└── i2ptunnel.config (legacy, auto-migrated)
```
**Kritik Biçim Farkı**: - **Monolitik biçim**: Özellikler `tunnel.N.` önekiyle başlar - **Bölünmüş biçim**: Özellikler **önekli değildir** (örn., `description=`, `tunnel.0.description=` değil)

#### Geçiş Davranışı

0.9.42'ye yükselttikten sonra ilk çalıştırmada: 1. Mevcut i2ptunnel.config okunur 2. Bireysel tunnel yapılandırmaları i2ptunnel.config.d/ içinde oluşturulur 3. Özelliklerin ön ekleri ayrılmış dosyalarda kaldırılır 4. Özgün dosya yedeklenir 5. Geriye dönük uyumluluk için eski biçim hâlâ desteklenir

#### Yapılandırma Bölümleri

I2PTunnel yapılandırması, aşağıdaki [I2PTunnel Yapılandırma Başvurusu](#i2ptunnel-configuration-reference) bölümünde ayrıntılı olarak belgelenmiştir. Özellik açıklamaları hem monolitik (`tunnel.N.property`) hem de bölünmüş (`property`) biçimler için geçerlidir.

---

## I2PTunnel Yapılandırma Referansı

Bu bölüm, tüm I2PTunnel yapılandırma özellikleri için kapsamlı bir teknik başvuru sağlar. Özellikler bölünmüş biçimde (`tunnel.N.` ön eki olmadan) gösterilir. Monolitik biçim için, N'in tunnel numarası olduğu `tunnel.N.` ön ekini tüm özelliklerin başına ekleyin.

**Önemli**: `tunnel.N.option.i2cp.*` olarak tanımlanan özellikler I2PTunnel içinde uygulanır ve I2CP protokolü veya SAM API gibi diğer arayüzler üzerinden **DESTEKLENMEZ**.

### Temel Özellikler

#### tunnel.N.description (açıklama)

- **Tür**: Dize
- **Bağlam**: Tüm tunnels
- **Açıklama**: Kullanıcı arayüzünde görüntülemek için insan tarafından okunabilir tunnel açıklaması
- **Örnek**: `description=HTTP Proxy for outproxy access`

#### tunnel.N.name (ad)

- **Tür**: Dize
- **Bağlam**: Tüm tunnel'ler
- **Gerekli**: Evet
- **Açıklama**: Benzersiz tunnel tanımlayıcısı ve görünen ad
- **Örnek**: `name=I2P HTTP Proxy`

#### tunnel.N.type (tip)

- **Tür**: Enum
- **Bağlam**: Tüm tunnel'lar
- **Gerekli**: Evet
- **Değerler**:
  - `client` - Genel amaçlı istemci tunnel
  - `httpclient` - HTTP proxy istemcisi
  - `ircclient` - IRC istemci tunnel
  - `socksirctunnel` - SOCKS IRC proxy
  - `sockstunnel` - SOCKS proxy (sürüm 4, 4a, 5)
  - `connectclient` - CONNECT proxy istemcisi
  - `streamrclient` - Streamr istemcisi
  - `server` - Genel amaçlı sunucu tunnel
  - `httpserver` - HTTP sunucu tunnel
  - `ircserver` - IRC sunucu tunnel
  - `httpbidirserver` - Çift yönlü HTTP sunucusu
  - `streamrserver` - Streamr sunucusu

#### tunnel.N.interface (arayüz)

- **Tür**: Dize (IP adresi veya ana makine adı)
- **Bağlam**: Yalnızca Client tunnels (istemci tünelleri)
- **Varsayılan**: 127.0.0.1
- **Açıklama**: Gelen bağlantılar için bağlanılacak yerel arayüz
- **Güvenlik Notu**: 0.0.0.0 adresine bağlamak uzak bağlantılara izin verir
- **Örnek**: `interface=127.0.0.1`

#### tunnel.N.listenPort (listenPort)

- **Tür**: Tamsayı
- **Bağlam**: Yalnızca Client tunnels
- **Aralık**: 1-65535
- **Açıklama**: İstemci bağlantıları için dinlenecek yerel bağlantı noktası
- **Örnek**: `listenPort=4444`

#### tunnel.N.targetHost (targetHost)

- **Tür**: String (IP adresi veya ana bilgisayar adı)
- **Bağlam**: Yalnızca sunucu tunnel'ları
- **Açıklama**: Bağlantıların iletileceği yerel sunucu
- **Örnek**: `targetHost=127.0.0.1`

#### tunnel.N.targetPort (targetPort)

- **Tür**: Tamsayı
- **Bağlam**: Yalnızca sunucu tunnels
- **Aralık**: 1-65535
- **Açıklama**: Bağlanılacak targetHost üzerindeki port
- **Örnek**: `targetPort=80`

#### tunnel.N.targetDestination (targetDestination)

- **Tür**: Dize (virgül veya boşlukla ayrılmış hedefler)
- **Bağlam**: Yalnızca client tunnels
- **Biçim**: `destination[:port][,destination[:port]]`
- **Açıklama**: Bağlanılacak I2P hedef(ler)i
- **Örnekler**:
  - `targetDestination=example.i2p`
  - `targetDestination=example.i2p:8080`
  - `targetDestination=site1.i2p,site2.i2p:8080`

#### tunnel.N.i2cpHost (i2cpHost)

- **Tür**: String (IP adresi veya ana makine adı)
- **Varsayılan**: 127.0.0.1
- **Açıklama**: I2P router I2CP arayüz adresi
- **Not**: router bağlamında çalışırken yok sayılır
- **Örnek**: `i2cpHost=127.0.0.1`

#### tunnel.N.i2cpPort (i2cpPort)

- **Tür**: Tamsayı
- **Varsayılan**: 7654
- **Aralık**: 1-65535
- **Açıklama**: I2P router I2CP bağlantı noktası
- **Not**: router bağlamında çalışırken yok sayılır
- **Örnek**: `i2cpPort=7654`

#### tunnel.N.startOnLoad (startOnLoad)

- **Tür**: Boolean (mantıksal)
- **Varsayılan**: true
- **Açıklama**: I2PTunnel yüklendiğinde tunnel'in başlatılıp başlatılmayacağı
- **Örnek**: `startOnLoad=true`

### Proxy Yapılandırması

#### tunnel.N.proxyList (proxyList)

- **Tür**: String (virgülle veya boşlukla ayrılmış ana makine adları)
- **Bağlam**: Yalnızca HTTP ve SOCKS vekil sunucuları
- **Açıklama**: outproxy (dış vekil sunucu) ana makinelerinin listesi
- **Örnek**: `proxyList=outproxy.example.i2p,backup.example.i2p`

### Sunucu Yapılandırması

#### tunnel.N.privKeyFile (privKeyFile)

- **Tür**: Dize (dosya yolu)
- **Bağlam**: Sunucular ve kalıcı istemci tunnels
- **Açıklama**: Kalıcı hedefin özel anahtarlarını içeren dosya
- **Yol**: Mutlak veya I2P yapılandırma dizinine göreli
- **Örnek**: `privKeyFile=eepsite/eepPriv.dat`

#### tunnel.N.spoofedHost (spoofedHost)

- **Tür**: String (ana bilgisayar adı)
- **Bağlam**: Yalnızca HTTP sunucuları
- **Varsayılan**: Hedefin Base32 ana bilgisayar adı
- **Açıklama**: Yerel sunucuya iletilen Host başlığı değeri
- **Örnek**: `spoofedHost=example.i2p`

#### tunnel.N.spoofedHost.NNNN (spoofedHost.NNNN)

- **Tür**: Dize (ana bilgisayar adı)
- **Bağlam**: Yalnızca HTTP sunucuları
- **Açıklama**: Belirli bir gelen bağlantı noktası için sanal ana bilgisayar adını geçersiz kılma
- **Kullanım Durumu**: Birden çok siteyi farklı bağlantı noktalarında barındırma
- **Örnek**: `spoofedHost.8080=site1.example.i2p`

### İstemciye Özgü Seçenekler

#### tunnel.N.sharedClient (sharedClient)

- **Tür**: Boolean (doğru/yanlış)
- **Bağlam**: Yalnızca istemci tunnel'ları
- **Varsayılan**: false
- **Açıklama**: Birden fazla istemcinin bu tunnel'ı paylaşmasına izin verilip verilmediği
- **Örnek**: `sharedClient=false`

#### tunnel.N.option.persistentClientKey (persistentClientKey)

- **Tür**: Boolean
- **Bağlam**: Yalnızca Client tunnels
- **Varsayılan**: false
- **Açıklama**: Yeniden başlatmalar arasında hedef anahtarlarını saklayıp yeniden kullanır
- **Çakışma**: `i2cp.newDestOnResume=true` ile birlikte kullanılamaz
- **Örnek**: `option.persistentClientKey=true`

### I2CP Seçenekleri (I2PTunnel Uygulaması)

**Önemli**: Bu özellikler `option.i2cp.` önekiyle başlar, ancak **I2PTunnel içinde uygulanır**, I2CP protokol katmanında değil. I2CP veya SAM API'leri üzerinden kullanılamazlar.

#### tunnel.N.option.i2cp.delayOpen (option.i2cp.delayOpen)

- **Tür**: Boolean
- **Bağlam**: Yalnızca istemci tunnels (tünel) için
- **Varsayılan**: false
- **Açıklama**: İlk bağlantıya kadar tunnel oluşturmayı geciktir
- **Kullanım Durumu**: Seyrek kullanılan tunnels için kaynak tasarrufu
- **Örnek**: `option.i2cp.delayOpen=false`

#### tunnel.N.option.i2cp.newDestOnResume (option.i2cp.newDestOnResume)

- **Tür**: Boolean
- **Bağlam**: Yalnızca istemci tunnel'ları
- **Varsayılan**: false
- **Gerektirir**: `i2cp.closeOnIdle=true`
- **Çakışma**: `persistentClientKey=true` ile birlikte kullanılamaz
- **Açıklama**: Boşta kalma zaman aşımından sonra yeni Destination (uç nokta kimliği) oluştur
- **Örnek**: `option.i2cp.newDestOnResume=false`

#### tunnel.N.option.i2cp.leaseSetPrivateKey (option.i2cp.leaseSetPrivateKey)

- **Tür**: Dize (base64 ile kodlanmış anahtar)
- **Bağlam**: Yalnızca sunucu tunnel'ları
- **Açıklama**: Kalıcı özel leaseset (I2P'de bir hedefin erişim bilgilerini içeren kayıt) şifreleme anahtarı
- **Kullanım Senaryosu**: Yeniden başlatmalar arasında şifrelenmiş leaseset tutarlılığını sürdürmek
- **Örnek**: `option.i2cp.leaseSetPrivateKey=AAAA...base64...`

#### tunnel.N.option.i2cp.leaseSetSigningPrivateKey (option.i2cp.leaseSetSigningPrivateKey)

- **Tür**: String (sigtype:base64)
- **Bağlam**: Yalnızca sunucu tunnels
- **Biçim**: `sigtype:base64key`
- **Açıklama**: Kalıcı leaseSet (I2P'de bir destinasyonun bağlantı bilgileri kümesi) imzalama özel anahtarı
- **Örnek**: `option.i2cp.leaseSetSigningPrivateKey=7:AAAA...base64...`

### Sunucuya Özel Seçenekler

#### tunnel.N.option.enableUniqueLocal (option.enableUniqueLocal)

- **Tür**: Boolean (mantıksal)
- **Bağlam**: Yalnızca Server tunnels için
- **Varsayılan**: false
- **Açıklama**: Her uzak I2P hedefi için benzersiz yerel IP kullanın
- **Kullanım Senaryosu**: Sunucu günlüklerinde istemci IP'lerini izlemek
- **Güvenlik Notu**: Anonimliği azaltabilir
- **Örnek**: `option.enableUniqueLocal=false`

#### tunnel.N.option.targetForPort.NNNN (option.targetForPort.NNNN)

- **Tür**: String (hostname:port)
- **Bağlam**: Yalnızca sunucu tunnel'ları
- **Açıklama**: Gelen NNNN bağlantı noktası için targetHost/targetPort değerlerini geçersiz kıl
- **Kullanım Senaryosu**: Farklı yerel hizmetlere bağlantı noktası tabanlı yönlendirme
- **Örnek**: `option.targetForPort.8080=localhost:8080`

### İş Parçacığı Havuzu Yapılandırması

#### tunnel.N.option.i2ptunnel.usePool (option.i2ptunnel.usePool)

- **Tür**: Boolean
- **Bağlam**: Yalnızca sunucu tunnels
- **Varsayılan**: true
- **Açıklama**: Bağlantı işleme için iş parçacığı havuzu kullan
- **Not**: Standart sunucular için her zaman false (yok sayılır)
- **Örnek**: `option.i2ptunnel.usePool=true`

#### tunnel.N.option.i2ptunnel.blockingHandlerCount (option.i2ptunnel.blockingHandlerCount)

- **Tür**: Tamsayı
- **Bağlam**: Yalnızca sunucu tunnels
- **Varsayılan**: 65
- **Açıklama**: Maksimum iş parçacığı havuzu boyutu
- **Not**: Standart sunucular için yok sayılır
- **Örnek**: `option.i2ptunnel.blockingHandlerCount=100`

### HTTP İstemci Seçenekleri

#### tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL (option.i2ptunnel.httpclient.allowInternalSSL)

- **Tür**: Boolean
- **Bağlam**: Yalnızca HTTP istemcileri için
- **Varsayılan**: false
- **Açıklama**: .i2p adreslerine yapılan SSL bağlantılarına izin verir
- **Örnek**: `option.i2ptunnel.httpclient.allowInternalSSL=false`

#### tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper (option.i2ptunnel.httpclient.disableAddressHelper)

- **Tür**: Boolean
- **Bağlam**: Yalnızca HTTP istemcileri
- **Varsayılan**: false
- **Açıklama**: Proxy yanıtlarındaki address helper bağlantılarını (adres eklemeye yardımcı bağlantılar) devre dışı bırakır
- **Örnek**: `option.i2ptunnel.httpclient.disableAddressHelper=false`

#### tunnel.N.option.i2ptunnel.httpclient.jumpServers (option.i2ptunnel.httpclient.jumpServers)

- **Tür**: Dize (virgülle veya boşlukla ayrılmış URL'ler)
- **Bağlam**: Yalnızca HTTP istemcileri
- **Açıklama**: Ana bilgisayar adı çözümlemesi için jump server (atlama sunucusu) URL'leri
- **Örnek**: `option.i2ptunnel.httpclient.jumpServers=http://jump.i2p/jump,http://stats.i2p/jump`

#### tunnel.N.option.i2ptunnel.httpclient.sendAccept (option.i2ptunnel.httpclient.sendAccept)

- **Tür**: Boolean
- **Bağlam**: Yalnızca HTTP istemcileri
- **Varsayılan**: false
- **Açıklama**: Accept-* başlıklarını iletir (Accept ve Accept-Encoding hariç)
- **Örnek**: `option.i2ptunnel.httpclient.sendAccept=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendReferer (option.i2ptunnel.httpclient.sendReferer)

- **Tür**: Boolean (mantıksal)
- **Bağlam**: Yalnızca HTTP istemcileri
- **Varsayılan**: false
- **Açıklama**: Referer üstbilgilerini proxy üzerinden iletir
- **Gizlilik Notu**: Bilgi sızdırabilir
- **Örnek**: `option.i2ptunnel.httpclient.sendReferer=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendUserAgent (option.i2ptunnel.httpclient.sendUserAgent)

- **Tür**: Boolean
- **Bağlam**: Yalnızca HTTP istemcileri
- **Varsayılan**: false
- **Açıklama**: User-Agent başlıklarını vekil sunucu üzerinden geçirir
- **Gizlilik Notu**: Tarayıcı bilgilerini sızdırabilir
- **Örnek**: `option.i2ptunnel.httpclient.sendUserAgent=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendVia (option.i2ptunnel.httpclient.sendVia)

- **Tür**: Boolean (mantıksal)
- **Bağlam**: Yalnızca HTTP istemcileri
- **Varsayılan**: false
- **Açıklama**: Via başlıklarını proxy üzerinden geçirir
- **Örnek**: `option.i2ptunnel.httpclient.sendVia=false`

#### tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies (option.i2ptunnel.httpclient.SSLOutproxies)

- **Tür**: Dize (virgül veya boşlukla ayrılmış hedefler)
- **Bağlam**: Yalnızca HTTP istemcileri
- **Açıklama**: HTTPS için ağ içi SSL outproxy'leri
- **Örnek**: `option.i2ptunnel.httpclient.SSLOutproxies=ssl-outproxy.i2p`

#### tunnel.N.option.i2ptunnel.useLocalOutproxy (option.i2ptunnel.useLocalOutproxy)

- **Tür**: Boolean
- **Bağlam**: Yalnızca HTTP istemcileri için
- **Varsayılan**: true
- **Açıklama**: Kayıtlı yerel outproxy (çıkış vekil sunucusu) eklentilerini kullanır
- **Örnek**: `option.i2ptunnel.useLocalOutproxy=true`

### HTTP İstemci Kimlik Doğrulaması

#### tunnel.N.option.proxyAuth (option.proxyAuth)

- **Tür**: Enum (numaralandırma)
- **Bağlam**: Yalnızca HTTP istemcileri
- **Varsayılan**: false
- **Değerler**: `true`, `false`, `basic`, `digest`
- **Açıklama**: Proxy erişimi için yerel kimlik doğrulaması gerektirir
- **Not**: `true`, `basic` ile eşdeğerdir
- **Örnek**: `option.proxyAuth=basic`

#### tunnel.N.option.proxy.auth.USER.md5 (option.proxy.auth.USER.md5)

- **Tür**: String (32 karakterlik küçük harfli onaltılık)
- **Bağlam**: Yalnızca HTTP istemcileri
- **Gerektirir**: `proxyAuth=basic` veya `proxyAuth=digest`
- **Açıklama**: USER kullanıcısının parolasının MD5 özeti
- **Kullanımdan kaldırıldı**: Bunun yerine SHA-256 kullanın (0.9.56+)
- **Örnek**: `option.proxy.auth.alice.md5=5f4dcc3b5aa765d61d8327deb882cf99`

#### tunnel.N.option.proxy.auth.USER.sha256 (option.proxy.auth.USER.sha256)

- **Tür**: Dize (64 karakterlik küçük harfli onaltılık)
- **Bağlam**: Yalnızca HTTP istemcileri
- **Gerektirir**: `proxyAuth=digest`
- **İtibaren**: Sürüm 0.9.56
- **Standart**: RFC 7616
- **Açıklama**: USER kullanıcısının parolasının SHA-256 özeti
- **Örnek**: `option.proxy.auth.alice.sha256=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

### Dış Proxy Kimlik Doğrulaması

#### tunnel.N.option.outproxyAuth (option.outproxyAuth)

- **Tür**: Boolean
- **Bağlam**: Yalnızca HTTP istemcileri
- **Varsayılan**: false
- **Açıklama**: Kimlik doğrulama bilgilerini outproxy'ye (I2P dış çıkış proxy'si) gönder
- **Örnek**: `option.outproxyAuth=false`

#### tunnel.N.option.outproxyUsername (option.outproxyUsername)

- **Tür**: Dize
- **Bağlam**: Yalnızca HTTP istemcileri
- **Gerektirir**: `outproxyAuth=true`
- **Açıklama**: outproxy (harici proxy) kimlik doğrulaması için kullanıcı adı
- **Örnek**: `option.outproxyUsername=user`

#### tunnel.N.option.outproxyPassword (option.outproxyPassword)

- **Tür**: String
- **Bağlam**: Yalnızca HTTP istemcileri
- **Gerektirir**: `outproxyAuth=true`
- **Açıklama**: outproxy kimlik doğrulaması için parola (I2P’de dış ağlara erişim sağlayan vekil sunucu anlamındaki outproxy)
- **Güvenlik**: Düz metin olarak saklanır
- **Örnek**: `option.outproxyPassword=secret`

### SOCKS İstemci Seçenekleri

#### tunnel.N.option.i2ptunnel.socks.proxy.default (option.i2ptunnel.socks.proxy.default)

- **Tür**: Dize (virgülle veya boşlukla ayrılmış hedefler)
- **Bağlam**: Yalnızca SOCKS istemcileri
- **Açıklama**: Belirtilmemiş portlar için ağ içi outproxy'ler (I2P ağında erişilebilen çıkış proxy'leri)
- **Örnek**: `option.i2ptunnel.socks.proxy.default=outproxy.i2p`

#### tunnel.N.option.i2ptunnel.socks.proxy.NNNN (option.i2ptunnel.socks.proxy.NNNN)

- **Tür**: Dize (virgülle veya boşlukla ayrılmış destinations (I2P adresleri))
- **Bağlam**: Yalnızca SOCKS istemcileri
- **Açıklama**: Özellikle NNNN bağlantı noktası için ağ içi outproxies (I2P ağından açık internete çıkış sağlayan vekil sunucular)
- **Örnek**: `option.i2ptunnel.socks.proxy.443=ssl-outproxy.i2p`

#### tunnel.N.option.outproxyType (option.outproxyType)

- **Tür**: Enum (numaralandırma)
- **Bağlam**: Yalnızca SOCKS istemcileri
- **Varsayılan**: socks
- **İtibaren**: Sürüm 0.9.57
- **Değerler**: `socks`, `connect` (HTTPS)
- **Açıklama**: Yapılandırılmış outproxy (dış vekil) türü
- **Örnek**: `option.outproxyType=connect`

### HTTP Sunucusu Seçenekleri

#### tunnel.N.option.maxPosts (option.maxPosts)

- **Tür**: Tamsayı
- **Bağlam**: Yalnızca HTTP sunucuları
- **Varsayılan**: 0 (sınırsız)
- **Açıklama**: postCheckTime başına tek bir hedeften en fazla POST sayısı
- **Örnek**: `option.maxPosts=10`

#### tunnel.N.option.maxTotalPosts (option.maxTotalPosts)

- **Tür**: Tamsayı
- **Bağlam**: Yalnızca HTTP sunucuları
- **Varsayılan**: 0 (sınırsız)
- **Açıklama**: postCheckTime başına, tüm Destinations (I2P hedef kimliği) genelinde toplam en fazla POST isteği sayısı
- **Örnek**: `option.maxTotalPosts=50`

#### tunnel.N.option.postCheckTime (option.postCheckTime)

- **Tür**: Tamsayı (saniye)
- **Bağlam**: Yalnızca HTTP sunucuları
- **Varsayılan**: 300
- **Açıklama**: POST sınırlarını denetlemek için zaman aralığı
- **Örnek**: `option.postCheckTime=600`

#### tunnel.N.option.postBanTime (option.postBanTime)

- **Tür**: Tamsayı (saniye)
- **Bağlam**: Yalnızca HTTP sunucuları için
- **Varsayılan**: 1800
- **Açıklama**: Tek bir hedef için maxPosts aşıldığında yasaklama süresi
- **Örnek**: `option.postBanTime=3600`

#### tunnel.N.option.postTotalBanTime (option.postTotalBanTime)

- **Tür**: Tamsayı (saniye)
- **Bağlam**: Yalnızca HTTP sunucuları
- **Varsayılan**: 600
- **Açıklama**: maxTotalPosts sınırı aşıldığında yasaklama süresi
- **Örnek**: `option.postTotalBanTime=1200`

### HTTP Sunucusu Güvenlik Seçenekleri

#### tunnel.N.option.rejectInproxy (option.rejectInproxy)

- **Tür**: Boolean
- **Bağlam**: Yalnızca HTTP sunucuları
- **Varsayılan**: false
- **Açıklama**: Görünüşe göre bir inproxy (I2P ağına girişi sağlayan ara sunucu) üzerinden gelen bağlantıları reddet
- **Örnek**: `option.rejectInproxy=false`

#### tunnel.N.option.rejectReferer (option.rejectReferer)

- **Tür**: Mantıksal
- **Bağlam**: Yalnızca HTTP sunucuları
- **Varsayılan**: false
- **Sürüm**: 0.9.25'ten itibaren
- **Açıklama**: Referer başlığı içeren bağlantıları reddeder
- **Örnek**: `option.rejectReferer=false`

#### tunnel.N.option.rejectUserAgents (option.rejectUserAgents)

- **Tür**: Boolean
- **Bağlam**: Yalnızca HTTP sunucuları için
- **Varsayılan**: false
- **Başlangıç**: Sürüm 0.9.25
- **Gerektirir**: `userAgentRejectList` özelliği
- **Açıklama**: Eşleşen User-Agent'a sahip bağlantıları reddeder
- **Örnek**: `option.rejectUserAgents=false`

#### tunnel.N.option.userAgentRejectList (option.userAgentRejectList)

- **Tür**: Dize (virgülle ayrılmış eşleşme dizeleri)
- **Bağlam**: Yalnızca HTTP sunucuları
- **Sürüm**: Sürüm 0.9.25'ten beri
- **Büyük/küçük harf**: Büyük/küçük harfe duyarlı eşleştirme
- **Özel**: "none" (0.9.33'ten beri) boş User-Agent (kullanıcı aracısı) ile eşleşir
- **Açıklama**: Reddedilecek User-Agent kalıplarının listesi
- **Örnek**: `option.userAgentRejectList=Mozilla,Opera,none`

### IRC Sunucusu Seçenekleri

#### tunnel.N.option.ircserver.fakeHostname (option.ircserver.fakeHostname)

- **Type**: Dize (ana makine adı deseni)
- **Context**: Yalnızca IRC sunucuları için
- **Default**: `%f.b32.i2p`
- **Tokens**:
  - `%f` = Tam base32 hedef karması
  - `%c` = Gizlenmiş hedef karması (bkz. cloakKey)
- **Description**: IRC sunucusuna gönderilen ana makine adı biçimi
- **Example**: `option.ircserver.fakeHostname=%c.irc.i2p`

#### tunnel.N.option.ircserver.cloakKey (option.ircserver.cloakKey)

- **Tür**: Dize (parola tümcesi)
- **Bağlam**: Yalnızca IRC sunucuları için
- **Varsayılan**: Oturum başına rastgele
- **Kısıtlamalar**: Tırnak işareti veya boşluk içeremez
- **Açıklama**: Tutarlı ana makine adı gizlemesi için parola tümcesi
- **Kullanım Durumu**: Yeniden başlatmalar/sunucular arasında kalıcı kullanıcı takibi
- **Örnek**: `option.ircserver.cloakKey=mysecretkey`

#### tunnel.N.option.ircserver.method (option.ircserver.method)

- **Tür**: Enum (numaralandırma)
- **Bağlam**: Yalnızca IRC sunucuları için
- **Varsayılan**: user
- **Değerler**: `user`, `webirc`
- **Açıklama**: IRC sunucusu için kimlik doğrulama yöntemi
- **Örnek**: `option.ircserver.method=webirc`

#### tunnel.N.option.ircserver.webircPassword (option.ircserver.webircPassword)

- **Tür**: String (parola)
- **Bağlam**: Yalnızca IRC sunucuları
- **Gerektirir**: `method=webirc`
- **Kısıtlamalar**: Tırnak işareti veya boşluk içeremez
- **Açıklama**: WEBIRC protokolü kimlik doğrulaması için parola
- **Örnek**: `option.ircserver.webircPassword=webircpass`

#### tunnel.N.option.ircserver.webircSpoofIP (option.ircserver.webircSpoofIP)

- **Tür**: Dize (IP adresi)
- **Bağlam**: Yalnızca IRC sunucuları için
- **Gerektirir**: `method=webirc`
- **Açıklama**: WEBIRC protokolü için spoofed (sahte) IP adresi
- **Örnek**: `option.ircserver.webircSpoofIP=10.0.0.1`

### SSL/TLS Yapılandırması

#### tunnel.N.option.useSSL (option.useSSL)

- **Tür**: Boolean
- **Varsayılan**: false
- **Bağlam**: Tüm tunnels
- **Davranış**:
  - **Sunucular**: Yerel sunucu bağlantıları için SSL kullan
  - **İstemciler**: Yerel istemciler için SSL gerektir
- **Örnek**: `option.useSSL=false`

#### tunnel.N.option.keystoreFile (option.keystoreFile)

- **Tür**: Dize (dosya yolu)
- **Bağlam**: Yalnızca istemci tunnels
- **Varsayılan**: `i2ptunnel-(random).ks`
- **Yol**: Mutlak değilse `$(I2P_CONFIG_DIR)/keystore/` dizinine göre göreli
- **Otomatik oluşturulur**: Mevcut değilse oluşturulur
- **Açıklama**: SSL özel anahtarını içeren keystore dosyası
- **Örnek**: `option.keystoreFile=my-tunnel.ks`

#### tunnel.N.option.keystorePassword (option.keystorePassword)

- **Tür**: String (parola)
- **Bağlam**: Yalnızca Client tunnels
- **Varsayılan**: changeit
- **Otomatik oluşturulur**: Yeni bir keystore (anahtar deposu) oluşturulursa rastgele parola
- **Açıklama**: SSL keystore parolası
- **Örnek**: `option.keystorePassword=secretpassword`

#### tunnel.N.option.keyAlias (option.keyAlias)

- **Tür**: String (takma ad)
- **Bağlam**: Yalnızca istemci tunnels
- **Otomatik olarak oluşturulur**: Yeni bir anahtar üretildiğinde oluşturulur
- **Açıklama**: Anahtar deposundaki (keystore) özel anahtar için takma ad
- **Örnek**: `option.keyAlias=mytunnel-key`

#### tunnel.N.option.keyPassword (option.keyPassword)

- **Tür**: String (parola)
- **Bağlam**: Yalnızca istemci tunnel'ları
- **Otomatik oluşturulur**: Yeni anahtar oluşturulursa rastgele parola
- **Açıklama**: anahtar deposu (keystore) içindeki özel anahtar için parola
- **Örnek**: `option.keyPassword=keypass123`

### Genel I2CP ve Akış Seçenekleri

Tüm `tunnel.N.option.*` özellikleri (yukarıda özellikle belgelenmemiş olanlar), `tunnel.N.option.` öneki çıkarılmış olarak I2CP arayüzüne ve akış kitaplığına iletilir.

**Önemli**: Bunlar, I2PTunnel'e özgü seçeneklerden ayrıdır. Bkz: - [I2CP Spesifikasyonu](/docs/specs/i2cp/) - [Streaming Library Spesifikasyonu](/docs/specs/streaming/)

Örnek akış seçenekleri:

```properties
option.i2cp.messageReliability=BestEffort
option.i2p.streaming.connectDelay=1000
option.i2p.streaming.maxWindowSize=128
```
### Tam Tunnel Örneği

```properties
# HTTP Proxy (split format without tunnel.N. prefix)
name=I2P HTTP Proxy
description=HTTP proxy for accessing I2P sites and outproxy
type=httpclient
interface=127.0.0.1
listenPort=4444
targetDestination=
sharedClient=true
startOnLoad=true

# I2CP configuration
i2cpHost=127.0.0.1
i2cpPort=7654

# HTTP client options
option.i2ptunnel.httpclient.allowInternalSSL=false
option.i2ptunnel.httpclient.disableAddressHelper=false
option.i2ptunnel.httpclient.jumpServers=http://stats.i2p/cgi-bin/jump.cgi
option.i2ptunnel.httpclient.sendAccept=false
option.i2ptunnel.httpclient.sendReferer=false
option.i2ptunnel.httpclient.sendUserAgent=false

# Proxy authentication
option.proxyAuth=false

# Outproxy configuration
option.i2ptunnel.httpclient.SSLOutproxies=false.i2p
proxyList=false.i2p

# Client behavior
option.persistentClientKey=false
option.i2cp.delayOpen=false

# I2CP tunnel options
option.inbound.length=3
option.outbound.length=3
option.inbound.quantity=2
option.outbound.quantity=2
```
---

## Sürüm Geçmişi ve Özellik Zaman Çizelgesi

### Sürüm 0.9.10 (2013)

**Özellik**: Yapılandırma dosyalarında boş değer desteği - Boş değerlere sahip anahtarlar (`key=`) artık destekleniyor - Önceden yok sayılıyor veya ayrıştırma hatalarına neden oluyordu

### Sürüm 0.9.18 (2015)

**Özellik**: Logger tampon boşaltma aralığı yapılandırması - Özellik: `logger.flushInterval` (varsayılan 29 saniye) - Kabul edilebilir günlük gecikmesini korurken disk G/Ç'sini azaltır

### Sürüm 0.9.23 (Kasım 2015)

**Önemli Değişiklik**: En az Java 7 gereklidir - Java 6 desteği sona erdi - Güvenlik güncellemelerinin devamı için zorunludur

### Sürüm 0.9.25 (2015)

**Özellikler**: HTTP sunucusu güvenlik seçenekleri - `tunnel.N.option.rejectReferer` - Referer başlığı olan bağlantıları reddet - `tunnel.N.option.rejectUserAgents` - Belirli User-Agent başlıklarını reddet - `tunnel.N.option.userAgentRejectList` - Reddedilecek User-Agent kalıpları - **Kullanım Senaryosu**: crawler’ların (tarama botlarının) ve istenmeyen istemcilerin etkisini azaltmak

### Sürüm 0.9.33 (Ocak 2018)

**Özellik**: Geliştirilmiş User-Agent filtreleme - `userAgentRejectList` dizesi "none" boş User-Agent ile eşleşir - i2psnark, i2ptunnel, streaming, SusiMail için ek hata düzeltmeleri

### Sürüm 0.9.41 (2019)

**Kullanımdan Kaldırma**: BOB Protokolü Android'den kaldırıldı - Android kullanıcıları SAM veya I2CP'ye geçmelidir

### Sürüm 0.9.42 (Ağustos 2019)

**Önemli Değişiklik**: Yapılandırma dosyalarının bölünmesi - `clients.config` bölünerek `clients.config.d/` dizin yapısına taşındı - `i2ptunnel.config` bölünerek `i2ptunnel.config.d/` dizin yapısına taşındı - Yükseltmeden sonraki ilk çalıştırmada otomatik geçiş - Modüler paketleme ve eklenti yönetimini etkinleştirir - Eski monolitik biçim hala destekleniyor

**Ek Özellikler**: - SSU performans iyileştirmeleri - Ağlar arası geçişin önlenmesi (Proposal 147) - Şifreleme türleri için başlangıç desteği

### Sürüm 0.9.56 (2021)

**Özellikler**: Güvenlik ve günlük kaydı iyileştirmeleri - `logger.gzip` - Döndürülen günlükler için Gzip sıkıştırması (varsayılan: false) - `logger.minGzipSize` - Sıkıştırma için en düşük boyut (varsayılan: 65536 bayt) - `tunnel.N.option.proxy.auth.USER.sha256` - SHA-256 özet kimlik doğrulaması (RFC 7616) - **Güvenlik**: Özet kimlik doğrulaması için MD5'in yerini SHA-256 alır

### Sürüm 0.9.57 (Ocak 2023)

**Özellik**: SOCKS outproxy (I2P dışa çıkış vekil sunucusu) türü yapılandırması - `tunnel.N.option.outproxyType` - outproxy türünü seçin (socks|connect) - Varsayılan: socks - HTTPS outproxy'ler için HTTPS CONNECT desteği

### Sürüm 2.6.0 (Temmuz 2024)

**Geriye dönük uyumsuz değişiklik**: I2P-over-Tor engellendi (Tor üzerinden I2P kullanımı) - Tor çıkış düğümü IP adreslerinden gelen bağlantılar artık reddediliyor - **Gerekçe**: I2P performansını düşürür, Tor çıkış düğümlerinin kaynaklarını boşa harcar - **Etkisi**: Tor çıkış düğümleri üzerinden I2P'ye erişen kullanıcılar engellenecek - Çıkış olmayan röleler ve Tor istemcileri etkilenmeyecek

### Sürüm 2.10.0 (Eylül 2025 - Güncel)

**Öne Çıkan Özellikler**: - **Kuantum sonrası kriptografi** mevcut (isteğe bağlı olarak Hidden Service Manager (Gizli Servis Yöneticisi) üzerinden etkinleştirilebilir) - **UDP izleyici desteği** I2PSnark için, izleyici yükünü azaltmak üzere - **Hidden Mode (Gizli Mod) kararlılığı** iyileştirmeleri, RouterInfo tükenmesini azaltmak için - Yoğun router’lar için ağ iyileştirmeleri - Geliştirilmiş UPnP/NAT geçişi - Agresif leaseSet kaldırma ile NetDB iyileştirmeleri - router olayları için gözlemlenebilirliğin azaltılması

**Yapılandırma**: Yeni yapılandırma özellikleri eklenmedi

**Yaklaşan Kritik Değişiklik**: Bir sonraki sürüm (muhtemelen 2.11.0 veya 3.0.0) Java 17 veya daha yenisini gerektirecek

---

## Kullanımdan Kaldırmalar ve Geriye Dönük Uyumluluğu Bozan Değişiklikler

### Kritik Kullanımdan Kaldırmalar

#### I2P-over-Tor Erişimi (Sürüm 2.6.0+)

- **Durum**: Temmuz 2024'ten beri BLOKLANDI
- **Etkisi**: Tor çıkış düğümü IP'lerinden gelen bağlantılar reddediliyor
- **Gerekçe**: Anonimlik açısından bir fayda sağlamadan I2P ağının performansını düşürüyor
- **Etkiler**: Yalnızca Tor çıkış düğümleri; röleler veya normal Tor istemcileri değil
- **Alternatif**: I2P veya Tor'u ayrı ayrı kullanın, birlikte kullanmayın

#### MD5 Özet Kimlik Doğrulaması

- **Durum**: Kullanımdan kaldırıldı (SHA-256 kullanın)
- **Özellik**: `tunnel.N.option.proxy.auth.USER.md5`
- **Gerekçe**: MD5 kriptografik olarak kırıldı
- **Yerine geçen**: `tunnel.N.option.proxy.auth.USER.sha256` (0.9.56 sürümünden beri)
- **Zaman çizelgesi**: MD5 hâlâ destekleniyor ancak önerilmiyor

### Yapılandırma Mimarisindeki Değişiklikler

#### Monolitik Yapılandırma Dosyaları (Sürüm 0.9.42+)

- **Etkilenen**: `clients.config`, `i2ptunnel.config`
- **Durum**: Bölünmüş dizin yapısı lehine kullanımdan kaldırıldı
- **Geçiş**: 0.9.42 yükseltmesinden sonraki ilk çalıştırmada otomatik
- **Uyumluluk**: Eski biçim hâlâ çalışır (geriye dönük uyumlu)
- **Öneri**: Yeni yapılandırmalar için bölünmüş biçimi kullanın

### Java Sürüm Gereksinimleri

#### Java 6 Desteği

- **Sona erdi**: Sürüm 0.9.23 (Kasım 2015)
- **Asgari**: 0.9.23'ten beri Java 7 zorunlu

#### Java 17 Gereksinimi (Yakında)

- **Durum**: KRİTİK YAKLAŞAN DEĞİŞİKLİK
- **Hedef**: 2.10.0’dan sonra çıkacak bir sonraki ana sürüm (muhtemelen 2.11.0 veya 3.0.0)
- **Mevcut Minimum**: Java 8
- **Gerekli Eylem**: Java 17 geçişine hazırlanın
- **Takvim**: Sürüm notlarıyla duyurulacaktır

### Kaldırılan Özellikler

#### BOB Protokolü (Android)

- **Kaldırıldı**: Sürüm 0.9.41
- **Platform**: Yalnızca Android
- **Alternatif**: SAM veya I2CP protokolleri
- **Masaüstü**: BOB hâlâ masaüstü platformlarda mevcut

### Önerilen Geçişler

1. **Kimlik Doğrulama**: MD5'ten SHA-256 digest (özet) kimlik doğrulamaya geçiş yapın
2. **Yapılandırma Biçimi**: İstemciler ve tunnels için ayrılmış dizin yapısına geçin
3. **Java Çalışma Zamanı**: Bir sonraki ana sürümden önce Java 17 yükseltmesini planlayın
4. **Tor Entegrasyonu**: I2P'yi Tor çıkış düğümleri üzerinden yönlendirmeyin

---

## Kaynakça

### Resmi Dokümantasyon

- [I2P Yapılandırma Şartnamesi](/docs/specs/configuration/) - Yapılandırma dosyası biçimi için resmi şartname
- [I2P Eklenti Şartnamesi](/docs/specs/plugin/) - Eklenti yapılandırması ve paketleme
- [I2P Ortak Yapılar - Tür Eşlemesi](/docs/specs/common-structures/#type-mapping) - Protokol veri serileştirme biçimi
- [Java Properties Biçimi](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) - Temel biçim şartnamesi

### Kaynak Kodu

- [I2P Java Router Deposu](https://github.com/i2p/i2p.i2p) - GitHub aynası
- [I2P Geliştiricileri Gitea](https://i2pgit.org/I2P_Developers/i2p.i2p) - Resmi I2P kaynak deposu
- [DataHelper.java](https://github.com/i2p/i2p.i2p/blob/master/core/java/src/net/i2p/data/DataHelper.java) - Yapılandırma dosyası G/Ç gerçeklemesi

### Topluluk Kaynakları

- [I2P Forum](https://i2pforum.net/) - Aktif topluluk tartışmaları ve destek
- [I2P Website](/) - Resmi proje web sitesi

### API Dokümantasyonu

- [DataHelper JavaDoc](https://i2pplus.github.io/javadoc/net/i2p/data/DataHelper.html) - yapılandırma dosyası yöntemlerine ilişkin API dokümantasyonu

### Belirtim Durumu

- **Son Spesifikasyon Güncellemesi**: Ocak 2023 (Sürüm 0.9.57)
- **Güncel I2P Sürümü**: 2.10.0 (Eylül 2025)
- **Teknik Doğruluk**: Spesifikasyon 2.10.0 dahil olmak üzere doğruluğunu korumaktadır (geriye dönük uyumluluğu bozan değişiklik yok)
- **Bakım**: Yapılandırma formatı değiştirildiğinde güncellenen yaşayan bir belgedir
