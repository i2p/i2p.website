---
title: "I2P Dokümantasyon Yazım Yönergeleri"
description: "I2P teknik dokümantasyonu genelinde tutarlılığı, doğruluğu ve erişilebilirliği sürdürün"
slug: "writing-guidelines"
lastUpdated: "2025-10"
---

**Amaç:** I2P teknik dokümantasyonu genelinde tutarlılığı, doğruluğu ve erişilebilirliği sürdürmek

---

## Temel İlkeler

### 1. Her Şeyi Doğrulayın

**Asla varsaymayın veya tahmin etmeyin.** Tüm teknik ifadeler şu kaynaklara göre doğrulanmalıdır: - Güncel I2P kaynak kodu (https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master) - Resmi API belgeleri (https://i2p.github.io/i2p.i2p/  - Yapılandırma teknik özellikleri [/docs/specs/](/docs/) - Son sürüm notları [/releases/](/categories/release/)

**Uygun doğrulama örneği:**

```markdown
❌ BAD: "The ClientApp interface probably requires three constructor parameters."
✅ GOOD: "The ClientApp interface requires this constructor signature: 
         public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)"
```
### 2. Kısalıktan ziyade açıklık

I2P ile ilk kez karşılaşabilecek geliştiricileri hedef alarak yazın. Önceden bilgi varsaymak yerine kavramları kapsamlı biçimde açıklayın.

**Örnek:**

```markdown
❌ BAD: "Use the port mapper for service discovery."
✅ GOOD: "The port mapper offers a simple directory for internal TCP services. 
         Register loopback ports so other applications can discover your service 
         without hardcoded addresses."
```
### 3. Önce Erişilebilirlik

I2P bir bindirme ağı olmasına rağmen, dokümantasyonun geliştiriciler tarafından clearnet’te (normal internet) erişilebilir olması gerekir. I2P içi kaynaklar için her zaman clearnet üzerinden erişilebilir alternatifler sağlayın.

---

## Teknik Doğruluk

### API ve Arayüz Dokümantasyonu

**Her zaman şunları dahil edin:** 1. İlk anılışında tam paket adları: `net.i2p.app.ClientApp` 2. Dönüş türlerini içeren eksiksiz metot imzaları 3. Parametre adları ve türleri 4. Zorunlu ve isteğe bağlı parametreler

**Örnek:**

```markdown
The `startup()` method has signature `void startup() throws IOException` and must 
execute without blocking. The method must call `ClientAppManager.notify()` at least 
once to transition from INITIALIZED state.
```
### Yapılandırma Özellikleri

Yapılandırma dosyalarını belgelendirirken: 1. Tam özellik adlarını gösterin 2. Dosya kodlamasını belirtin (I2P yapılandırmaları için UTF-8) 3. Eksiksiz örnekler sağlayın 4. Varsayılan değerleri belgeleyin 5. Özelliklerin eklendiği/değiştirildiği sürümü belirtin

**Örnek:**

```markdown
### clients.config Properties

**Required:**
- `clientApp.N.main` - Full class name (no default)

**Optional:**
- `clientApp.N.delay` - Seconds before starting (default: 120)
- `clientApp.N.onBoot` - Forces delay=0 if true (default: false, added in 0.9.4)
```
### Sabitler ve Numaralandırmalar

Sabitleri belgelerken asıl kod adlarını kullanın:

```markdown
❌ BAD: "Common registrations include console, i2ptunnel, Jetty, sam, and bob"

✅ GOOD: "Common port mapper service constants from `net.i2p.util.PortMapper`:
- `SVC_CONSOLE` - Router console (default port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (default port 4444)
- `SVC_SAM` - SAM bridge (default port 7656)"
```
### Benzer Kavramları Birbirinden Ayırt Et

I2P'nin birbiriyle örtüşen birkaç sistemi vardır. Hangi sistemi belgelendirdiğinizi her zaman netleştirin:

**Örnek:**

```markdown
Note that client registry and port mapper are separate systems:
- **ClientAppManager registry** enables inter-application communication by name lookup
- **PortMapper** maps service names to host:port combinations for service discovery
- **i2ptunnel tunnel types** are configuration values (tunnel.N.type), not service registrations
```
---

## Dokümantasyon URL'leri ve Kaynaklar

### URL Erişilebilirlik Kuralları

1. **Birincil referanslar** clearnet (açık internet) üzerinden erişilebilir URL'ler kullanmalıdır
2. **I2P içi URL'ler** (.i2p alan adları) erişilebilirlik notlarını içermelidir
3. **Her zaman alternatifler sağlayın** I2P içi kaynaklara bağlantı verirken

**I2P dahili URL'ler için şablon:**

```markdown
> **Note:** The I2P network hosts comprehensive documentation at http://idk.i2p/javadoc-i2p/ 
> which requires an I2P router for access. For clearnet access, use the GitHub Pages 
> mirror at https://eyedeekay.github.io/javadoc-i2p/
```
### Önerilen I2P Referans URL'leri

**Resmi spesifikasyonlar:** - [Yapılandırma](/docs/specs/configuration/) - [Eklenti](/docs/specs/plugin/) - [Belge Dizini](/docs/)

**API dokümantasyonu (en güncel olanı seçin):** - En güncel: https://i2p.github.io/i2p.i2p/ (I2P 2.10.0 itibarıyla API 0.9.66) - Clearnet (açık internet) yansısı: https://eyedeekay.github.io/javadoc-i2p/

**Kaynak kodu:** - GitLab (resmi): https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master - GitHub aynası: https://github.com/i2p/i2p.i2p

### Bağlantı Biçimi Standartları

```markdown
✅ GOOD: [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
✅ GOOD: [Configuration Specification](https://geti2p.net/spec/configuration)

❌ BAD: See the ClientApp docs at http://idk.i2p/...
❌ BAD: [link](url) with no descriptive text
```
---

## Sürüm Takibi

### Belge Üstverisi

Her teknik belge, frontmatter (belgenin başındaki meta veri bölümü) içinde sürüm meta verilerini içermelidir:

```markdown
---
title: "Document Title"
description: "Brief description"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
**Alan tanımları:** - `lastUpdated`: Belgenin en son gözden geçirildiği/güncellendiği yıl-ay - `accurateFor`: Belgenin doğrulandığı I2P sürümü - `reviewStatus`: Şunlardan biri "draft", "needs-review", "verified", "outdated"

### İçerikte Sürüm Referansları

Sürümlerden bahsederken: 1. Güncel sürüm için **kalın** kullanın: "**sürüm 2.10.0** (Eylül 2025)" 2. Geçmişe yönelik referanslarda hem sürüm numarasını hem de tarihi belirtin 3. Gerekli olduğunda API sürümünü I2P sürümünden ayrı olarak belirtin

**Örnek:**

```markdown
Managed clients were introduced in **version 0.9.4** (December 17, 2012) and 
remain the recommended architecture as of **version 2.10.0** (September 9, 2025). 
The current API version is **0.9.66**.
```
### Zaman İçindeki Değişiklikleri Belgelemek

Gelişen özellikler için:

```markdown
**Version history:**
- **0.9.4 (December 2012)** - Managed clients introduced
- **0.9.42 (2019)** - clients.config.d/ directory structure added
- **1.7.0 (2021)** - ShellService added for external program tracking
- **2.10.0 (September 2025)** - Current release, no API changes to managed clients
```
### Kullanımdan Kaldırma Bildirimleri

Kullanımdan kaldırılmış özellikleri belgeliyorsanız:

```markdown
> **Deprecated:** This feature was deprecated in version X.Y.Z and will be removed 
> in version A.B.C. Use [alternative feature](link) instead.
```
---

## Terminoloji Standartları

### Resmi I2P Terimleri

Bu terimleri aynen ve tutarlı şekilde kullanın:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct Term</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Avoid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P node, I2P client (ambiguous)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">eepsite</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P website, hidden service (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">connection, circuit (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">netDb</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">network database, DHT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lease set</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination info</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">address, endpoint</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">base64 destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P address, .i2p address</td>
    </tr>
  </tbody>
</table>
### Yönetilen İstemci Terminolojisi

Yönetilen istemcileri belgelerken:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use This</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Not This</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed application</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unmanaged client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">legacy client, static client</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ClientAppManager</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application manager, client manager</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lifecycle methods</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">state methods, control methods</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">client registry</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application registry, name service</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port mapper</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port registry, service directory</td>
    </tr>
  </tbody>
</table>
### Yapılandırma Terminolojisi

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Incorrect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.cfg, client.config</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config.d/</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.d/, config.d/</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.cfg</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel.config</td>
    </tr>
  </tbody>
</table>
### Paket ve Sınıf Adları

İlk anılışta her zaman tam nitelikli adları kullanın, sonrasında kısa adları kullanın:

```markdown
The `net.i2p.app.ClientApp` interface requires implementation of three lifecycle 
methods. When a ClientApp starts, the manager calls `startup()`...
```
---

## Kod Örnekleri ve Biçimlendirme

### Java Kod Örnekleri

Uygun sözdizimi vurgulaması ve tam örnekler kullanın:

```markdown
### Example: Registering with Port Mapper

\`\`\`java
// Register HTTP proxy service
context.portMapper().register(
    PortMapper.SVC_HTTP_PROXY, 
    "127.0.0.1", 
    4444
);

// Later, retrieve the port
int port = context.portMapper().getPort(PortMapper.SVC_HTTP_PROXY);
if (port == -1) {
    // Service not registered
}
\`\`\`
```
**Kod örneği gereksinimleri:** 1. Önemli satırları açıklayan yorumlar ekleyin 2. İlgili yerlerde hata işlemeyi gösterin 3. Gerçekçi değişken adları kullanın 4. I2P kodlama kurallarına uyun (4 boşluklu girinti) 5. Bağlamdan açıkça anlaşılmıyorsa içe aktarmaları gösterin

### Yapılandırma Örnekleri

Tam ve geçerli yapılandırma örneklerini göster:

```markdown
### Example: clients.config.d/ Entry

File: `clients.config.d/00-console.config`

\`\`\`properties
# Router console configuration
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
\`\`\`
```
### Komut Satırı Örnekleri

Kullanıcı komutları için `$`, root için `#` kullanın:

```markdown
\`\`\`bash
# Install I2P on Debian/Ubuntu
$ sudo apt-get install i2p

# Start the router
$ i2prouter start
\`\`\`
```
### Satır içi kod

Ters tırnakları şunlar için kullanın: - Yöntem adları: `startup()` - Sınıf adları: `ClientApp` - Özellik adları: `clientApp.0.main` - Dosya adları: `clients.config` - Sabitler: `SVC_HTTP_PROXY` - Paket adları: `net.i2p.app`

---

## Ton ve Üslup

### Profesyonel ama erişilebilir

Küçümseyici olmadan teknik bir kitleye yazın:

```markdown
❌ BAD: "Obviously, you should implement the startup() method."
✅ GOOD: "Managed clients must implement the startup() method to initialize resources."

❌ BAD: "Even a junior dev knows you need to call notify()."
✅ GOOD: "The manager requires at least one notify() call during startup to track state transitions."
```
### Etken Çatı

Netlik için etken çatı kullanın:

```markdown
❌ PASSIVE: "The ClientAppManager is notified by the client when state changes."
✅ ACTIVE: "The client notifies ClientAppManager when state changes."
```
### Yönergelerde emir kipi

Prosedürel içerikte doğrudan emir kipini kullanın:

```markdown
✅ "Implement these three lifecycle methods:"
✅ "Call manager.notify() after changing state."
✅ "Register services using context.portMapper().register()"
```
### Gereksiz jargondan kaçının

Terimleri ilk geçtiği yerde açıklayın:

```markdown
✅ GOOD: "The netDb (network database) stores information about I2P routers and destinations."
❌ BAD: "Query the netDb for peer info." (no explanation)
```
### Noktalama Yönergeleri

1. **Em-dash (uzun tire) kullanmayın** - bunun yerine normal tireler, virgüller veya noktalı virgüller kullanın
2. Listelerde **Oxford virgülü** kullanın: "console, i2ptunnel, and Jetty"
3. **Kod bloklarında nokta** yalnızca dilbilgisel olarak gerekli olduğunda kullanın
4. **Sıralı listelerde** öğeler virgül içeriyorsa noktalı virgül kullanın

---

## Belge Yapısı

### Standart Bölüm Sırası

API belgeleri için:

1. **Genel Bakış** - özelliğin ne yaptığı, neden var olduğu
2. **Uygulama** - nasıl uygulanacağı/kullanılacağı
3. **Yapılandırma** - nasıl yapılandırılacağı
4. **API Referansı** - ayrıntılı metot/özellik açıklamaları
5. **Örnekler** - çalışır durumdaki eksiksiz örnekler
6. **En İyi Uygulamalar** - ipuçları ve öneriler
7. **Sürüm Geçmişi** - ne zaman tanıtıldığı, zaman içindeki değişiklikler
8. **Referanslar** - ilgili belgelere bağlantılar

### Başlık Hiyerarşisi

Anlamsal başlık düzeylerini kullanın:

```markdown
# Document Title (h1 - only one per document)

## Major Section (h2)

### Subsection (h3)

#### Detail Section (h4)

**Bold text for emphasis within sections**
```
### Bilgi Kutuları

Özel notlar için alıntı bloklarını kullanın:

```markdown
> **Note:** Additional information that clarifies the main content.

> **Warning:** Important information about potential issues or breaking changes.

> **Deprecated:** This feature is deprecated and will be removed in version X.Y.Z.

> **Status:** Current implementation status or version information.
```
### Listeler ve Düzen

**Sırasız listeler** ardışık olmayan öğeler için:

```markdown
- First item
- Second item
- Third item
```
**Sıralı listeler** ardışık adımlar için:

```markdown
1. First step
2. Second step
3. Third step
```
**Tanım listeleri** terim açıklamaları için:

```markdown
**Term One**
: Explanation of term one

**Term Two**  
: Explanation of term two
```
---

## Kaçınılması Gereken Yaygın Hatalar

### 1. Benzer Sistemleri Karıştırma

**Karıştırmayın:** - ClientAppManager kaydı vs. PortMapper - i2ptunnel tunnel türleri vs. port mapper servis sabitleri - ClientApp vs. RouterApp (farklı bağlamlar) - Yönetilen vs. yönetilmeyen istemciler

**Her zaman hangi sistem** hakkında konuştuğunuzu netleştirin:

```markdown
✅ "Register with ClientAppManager using manager.register(this) for name-based lookup."
✅ "Register with PortMapper using context.portMapper().register() for port discovery."
```
### 2. Güncel Olmayan Sürüm Referansları

**Yapmayın:** - Eski sürümleri "güncel" olarak göstermek - Güncelliğini yitirmiş API dokümantasyonuna bağlantı vermek - Örneklerde deprecated (kullanımdan kaldırılmış) metot imzalarını kullanmak

**Yapın:** - Yayınlamadan önce sürüm notlarını kontrol edin - API dokümantasyonunun geçerli sürümle eşleştiğini doğrulayın - Örnekleri güncel en iyi uygulamaları kullanacak şekilde güncelleyin

### 3. Erişilemeyen URL'ler

**Yapmayın:** - clearnet alternatifleri olmayan yalnızca .i2p alan adlarına bağlantı vermek - Bozuk ya da güncelliğini yitirmiş dokümantasyon URL'lerini kullanmak - Yerel file:// yollarına bağlantı vermek

**Yapın:** - Tüm I2P içi bağlantılar için clearnet (açık internet) alternatifleri sağlayın - Yayınlamadan önce URL'lerin erişilebilir olduğunu doğrulayın - Kalıcı URL'ler kullanın (geti2p.net, geçici barındırma değil)

### 4. Eksik Kod Örnekleri

**Yapmayın:** - Bağlam olmadan kod parçaları göstermeyin - Hata işlemeyi atlamayın - Tanımlanmamış değişkenler kullanmayın - Bariz olmadığı durumlarda import deyimlerini atlamayın

**Yapın:** - Eksiksiz ve derlenebilir örnekler gösterin - Gerekli hata işlemesini dahil edin - Her önemli satırın ne yaptığını açıklayın - Yayınlamadan önce örnekleri test edin

### 5. Muğlak İfadeler

```markdown
❌ "Some applications register services."
✅ "Applications implementing ClientApp may register with ClientAppManager 
   using manager.register(this) to enable name-based lookup."

❌ "Configuration files go in the config directory."
✅ "Modern I2P installations store client configurations in 
   $I2P/clients.config.d/ as individual files."
```
---

## Markdown Kuralları

### Dosya Adlandırma

Dosya adları için kebab-case (kelimelerin küçük harfle yazılıp tirelerle ayrıldığı adlandırma biçimi) kullanın: - `managed-clients.md` - `port-mapper-guide.md` - `configuration-reference.md`

### Ön Bilgi Biçimi

Her zaman YAML frontmatter (belgenin başındaki YAML meta verisi) ekleyin:

```yaml
---
title: "Document Title"
description: "Brief description under 160 characters"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
### Bağlantı Biçimlendirme

**İç bağlantılar** (dokümantasyon içinde):

```markdown
See [clients.config specification](https://geti2p.net/spec/configuration#clients-config)
```
**Dış bağlantılar** (diğer kaynaklara):

```markdown
For more details, see [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
```
**Kod deposu bağlantıları**:

```markdown
View source: [ClientApp.java](https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master/core/java/src/net/i2p/app/ClientApp.java)
```
### Tablo Biçimlendirme

GitHub-flavored Markdown (GitHub'a özgü Markdown) tablolarını kullanın:

```markdown
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `main` | String | (required) | Full class name |
| `delay` | Integer | 120 | Seconds before start |
| `onBoot` | Boolean | false | Force immediate start |
```
### Kod Bloğu Dil Etiketleri

Sözdizimi vurgulaması için dili her zaman belirtin:

```markdown
\`\`\`java
// Java code
\`\`\`

\`\`\`bash
# Shell commands
\`\`\`

\`\`\`properties
# Configuration files
\`\`\`

\`\`\`xml
<!-- XML files -->
\`\`\`
```
---

## İnceleme Kontrol Listesi

Dokümantasyonu yayımlamadan önce şunları doğrulayın:

- [ ] Tüm teknik iddialar kaynak koda veya resmi dokümantasyona göre doğrulanmış
- [ ] Sürüm numaraları ve tarihleri güncel
- [ ] Tüm URL'lere clearnet (açık internet) üzerinden erişilebilir (veya alternatifler sağlanmıştır)
- [ ] Kod örnekleri eksiksiz ve test edilmiştir
- [ ] Terminoloji I2P konvansiyonlarını izler
- [ ] Em dash yok (normal kısa çizgi veya başka noktalama işaretleri kullanın)
- [ ] Frontmatter (belge başı meta verisi) eksiksiz ve doğru
- [ ] Başlık hiyerarşisi anlamsal (h1 → h2 → h3)
- [ ] Listeler ve tablolar düzgün biçimlendirilmiş
- [ ] Kaynakça bölümü alıntılanan tüm kaynakları içerir
- [ ] Belge yapı yönergelerini izler
- [ ] Üslup profesyonel ama anlaşılır
- [ ] Benzer kavramlar açıkça ayırt edilmiştir
- [ ] Kırık bağlantı veya referans yok
- [ ] Yapılandırma örnekleri geçerli ve güncel

---

**Geri bildirim:** Bu kılavuzlarda sorunlar bulur veya önerileriniz olursa, lütfen bunları resmi I2P geliştirme kanalları üzerinden gönderin.
