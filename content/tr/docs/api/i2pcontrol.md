---
title: "I2PControl JSON-RPC"
description: "I2PControl webapp üzerinden uzaktan router yönetimi API'si"
slug: "i2pcontrol"
lastUpdated: "2026-07-10"
accurateFor: "2.12.0"
reviewStatus: "needs-review"
---

# I2PControl API Belgeleri

-------------ekleme kontrolü--------------

I2PControl, I2P router ile birlikte gelen (0.9.39 sürümünden itibaren) bir **JSON-RPC 2.0** API'sidir. Yapılandırılmış JSON istekleri aracılığıyla router'ın kimlik doğrulamalı izlenmesini ve kontrolünü sağlar.

> **Varsayılan şifre:** `itoopie` — bu fabrika varsayılanıdır ve güvenlik için **hemen değiştirilmelidir**.

## 1. Genel Bakış ve Erişim

| Uygulama                   | Varsayılan Uç Nokta                        | Protokol | Varsayılan olarak etkin | Notlar                 |
|----------------------------|--------------------------------------------|----------|-------------------------|------------------------|
| Java I2P (2.10.0+)         | `http://127.0.0.1:7657/jsonrpc/`           | HTTP     | ❌ WebApps üzerinden etkinleştirilmelidir (Yönetim Paneli) | Dahili web uygulaması  |
| i2pd (C++ uygulaması)      | `https://127.0.0.1:7650/`                  | HTTPS    | ✅ Varsayılan olarak etkin | Eski eklenti davranışı  |
---

Java I2P durumunda, **Router Console → WebApps → I2PControl** bölümüne gidip etkinleştirmeniz gerekir (otomatik başlatılacak şekilde ayarlayın). Etkin hale geldikten sonra, tüm yöntemler için önce kimlik doğrulaması yapmanız ve bir oturum token'ı almanız gerekir.

## 2. JSON-RPC Formatı

---

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "MethodName",
  "params": {
    /* named parameters */
  }
}
```
Tüm istekler JSON-RPC 2.0 yapısını takip eder:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": { /* data */ }
}
```
Başarılı bir yanıt `result` alanı içerir; başarısızlık durumunda ise bir `error` nesnesi döndürülür:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "error": {
    "code": -32001,
    "message": "Invalid password"
  }
}
```
veya

## 3. Kimlik Doğrulama Akışı

### İstek (Kimlik Doğrulama)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "1",
        "method": "Authenticate",
        "params": {
          "API": 1,
          "Password": "itoopie"
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
### Başarılı Yanıt

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "Token": "a1b2c3d4e5",
    "API": 1
  }
}
```
| Alan       | Yön       | Tip    | Açıklama                                                   |
|------------|-----------|--------|------------------------------------------------------------|
| `API`      | İstek     | long   | İstemci tarafından istenen I2PControl API sürümü. `1` kullanın. |
| `Password` | İstek     | String | I2PControl ile kimlik doğrulamada kullanılan parola.         |
| `API`      | Yanıt     | long   | Sunucu tarafından uygulanan birincil API sürümü.             |
| `Token`    | Yanıt     | String | Sonraki isteklerde kullanılacak kimlik doğrulama jetonu.     |
---

Bu `Token`'ı sonraki tüm isteklerde `params` içinde eklemelisiniz.

## 4. Yöntemler ve Uç Noktalar

### 4.1 RouterInfo

---

Router hakkında anahtar telemetri verilerini getirir.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "2",
        "method": "RouterInfo",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.version": "",
          "i2p.router.status": "",
          "i2p.router.net.status": "",
          "i2p.router.net.tunnels.participating": "",
          "i2p.router.net.bw.inbound.1s": "",
          "i2p.router.net.bw.outbound.1s": ""
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**İstek Örneği**

#### Durum Kodu Enum (`i2p.router.net.status`)

| Anahtar                                    | Tür    | Açıklama                                                             |
|----------------------------------------|--------|-------------------------------------------------------------------------|
| `i2p.router.status`                    | Dize | Serbest biçimli, görüntülenmek üzere çevrilmiş yönlendirici durumu.             |
| `i2p.router.uptime`                    | long   | Yönlendiricinin çalışma süresi, milisaniye cinsinden. Eski i2pd sürümleri dize döndürebilir. |
| `i2p.router.version`                   | Dize | Tam yönlendirici sürümü.                                                    |
| `i2p.router.net.status`                | long   | Ağ durum kodu; aşağıdaki tabloya bakın.                               |
| `i2p.router.net.bw.inbound.1s`         | double | Geçerli gelen bant genişliği, saniye başına bayt cinsinden.                          |
| `i2p.router.net.bw.inbound.15s`        | double | 15 saniyelik ortalama gelen bant genişliği, saniye başına bayt cinsinden.                |
| `i2p.router.net.bw.outbound.1s`        | double | Geçerli giden bant genişliği, saniye başına bayt cinsinden.                         |
| `i2p.router.net.bw.outbound.15s`       | double | 15 saniyelik ortalama giden bant genişliği, saniye başına bayt cinsinden.               |
| `i2p.router.net.tunnels.participating` | long   | Bu yönlendiricinin katıldığı tünel sayısı.                |
#### Durum Kodu Numarası (`i2p.router.net.status`)

| Kod | Anlamı                                             |
|-----|----------------------------------------------------|
| 0   | TAMAM                                               |
| 1   | TEST EDİLİYOR                                       |
| 2   | GÜVENLIK_DUVARI_ARKASINDA                           |
| 3   | GIZLI                                               |
| 4   | UYARI_GÜVENLIK_DUVARI_ARKASINDA_VE_HIZLI            |
| 5   | UYARI_GÜVENLIK_DUVARI_ARKASINDA_VE_FLOODFILL        |
| 6   | UYARI_GÜVENLIK_DUVARI_ARKASINDA_VE_ICERI_TCP_VAR    |
| 7   | UYARI_GÜVENLIK_DUVARI_ARKASINDA_VE_UDP_DEVREDISIZ   |
| 8   | HATA_I2CP                                           |
| 9   | HATA_SAAT_UYUSUZLUGU                                |
| 10  | HATA_OZEL_TCP_ADRESI                                |
| 11  | HATA_SEMETRIK_NAT                                   |
| 12  | HATA_UDP_PORTU_KULLANILIOR                          |
| 13  | HATA_ETKIN_KISI_YOK_LUTFEN_BAGLANTIYI_VE_GUVENLIK_DUVARINI_KONTROL_ET |
| 14  | HATA_UDP_DEVRE_DISI_VE_TCP_AYARLANMAMIS             |
#### NetDB ve Eş Alanları

| Anahtar                                  | Tür     | Açıklama                                               |
|------------------------------------------|---------|--------------------------------------------------------|
| `i2p.router.netdb.knownpeers`            | long    | Yerel yönlendirici hariç bilinen eşlerin sayısı.         |
| `i2p.router.netdb.activepeers`           | long    | Aktif eşlerin sayısı.                                  |
| `i2p.router.netdb.fastpeers`             | long    | Hızlı olarak sınıflandırılan eşlerin sayısı.            |
| `i2p.router.netdb.highcapacitypeers`     | long    | Yüksek kapasiteli olarak sınıflandırılan eşlerin sayısı. |
| `i2p.router.netdb.isreseeding`           | boolean | Yeniden tohumlama işlemi devam ediyor mu.               |
**Yanıt Alanları (result)** Resmi dokümanlara göre (GetI2P): - `i2p.router.status` (String) — insan tarafından okunabilir durum - `i2p.router.uptime` (long) — milisaniye (veya eski i2pd için string) :contentReference[oaicite:0]{index=0} - `i2p.router.version` (String) — sürüm dizesi :contentReference[oaicite:1]{index=1} - `i2p.router.net.bw.inbound.1s`, `i2p.router.net.bw.inbound.15s` (double) — gelen bant genişliği B/s cinsinden :contentReference[oaicite:2]{index=2} - `i2p.router.net.bw.outbound.1s`, `i2p.router.net.bw.outbound.15s` (double) — giden bant genişliği B/s cinsinden :contentReference[oaicite:3]{index=3} - `i2p.router.net.status` (long) — sayısal durum kodu (aşağıdaki enum'a bakın) :contentReference[oaicite:4]{index=4} - `i2p.router.net.tunnels.participating` (long) — katılan tunnel sayısı :contentReference[oaicite:5]{index=5} - `i2p.router.netdb.activepeers`, `fastpeers`, `highcapacitypeers` (long) — netDB peer istatistikleri :contentReference[oaicite:6]{index=6} - `i2p.router.netdb.isreseeding` (boolean) — reseed'in aktif olup olmadığı :contentReference[oaicite:7]{index=7} - `i2p.router.netdb.knownpeers` (long) — toplam bilinen peer'lar :contentReference[oaicite:8]{index=8}

### 4.2 GetRate

---

| Parametre | Tür    | Açıklama                     |
|-----------|--------|------------------------------|
| `Stat`    | Dize   | Yönlendirici RateStat adı.   |
| `Period`  | uzun   | Hız periyodu milisaniye cinsinden. |
Belirli bir zaman penceresi boyunca oran metriklerini (örneğin bant genişliği, tunnel başarı oranı) almak için kullanılır.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "3",
        "method": "GetRate",
        "params": {
          "Token": "a1b2c3d4e5",
          "Stat": "bw.combined",
          "Period": 60000
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**İstek Örneği**

```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "result": {
    "Result": 12345.67
  }
}
```
**Örnek Yanıt**

### 4.3 RouterManager

---

| Parametre            | Sonuç               | Açıklama                                                              |
|----------------------|---------------------|-----------------------------------------------------------------------|
| `Restart`            | null                | Hemen yönlendiriciyi yeniden başlatır.                                |
| `RestartGraceful`    | null                | Katılılan tünellerin süresi dolduktan sonra yeniden başlatır.         |
| `Shutdown`           | null                | Hemen yönlendiriciyi kapatır.                                         |
| `ShutdownGraceful`   | null                | Katılılan tünellerin süresi dolduktan sonra kapatır.                  |
| `Reseed`             | null                | Yönlendiriciyi yeniden başlatır.                                     |
| `FindUpdates`        | boolean veya String | Engelleme. İmzalı yönlendirici güncellemesi arar.                    |
| `Update`             | String              | Engelleme. İmzalı yönlendirici güncellemesini başlatır ve son durumunu döndürür. |
Yönetimsel işlemler gerçekleştirin.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "4",
        "method": "RouterManager",
        "params": {
          "Token": "a1b2c3d4e5",
          "Restart": true
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**İzin verilen parametreler / yöntemler**   - `Restart`, `RestartGraceful`   - `Shutdown`, `ShutdownGraceful`   - `Reseed`, `FindUpdates`, `Update` :contentReference[oaicite:10]{index=10}

```json
{
  "jsonrpc": "2.0",
  "id": "4",
  "result": {
    "Restart": null
  }
}
```
**İstek Örneği**

### 4.4 NetworkSetting

**Başarılı Yanıt**

---

| Anahtar                             | Kabul Edilen Değer                                      | Açıklama                                                  |
|---------------------------------|-----------------------------------------------------|--------------------------------------------------------------|
| `i2p.router.net.ntcp.port`      | Dize, 1–65535                                     | NTCP portu; değişiklik yapmak için yeniden başlatma gerekir.                        |
| `i2p.router.net.ntcp.hostname`  | Dize                                              | NTCP ana bilgisayar adı; değişiklik yapmak için yeniden başlatma gerekir.                    |
| `i2p.router.net.ntcp.autoip`    | `always`, `true` veya `false`                        | NTCP otomatik adres seçimi.                            |
| `i2p.router.net.ssu.port`       | Dize, 1–65535                                     | SSU portu; değişiklik yapmak için yeniden başlatma gerekir.                         |
| `i2p.router.net.ssu.hostname`   | Dize                                              | SSU dış ana bilgisayar adı; değişiklik yapmak için yeniden başlatma gerekir.            |
| `i2p.router.net.ssu.autoip`     | `ssu`, `local,ssu`, `upnp,ssu` veya `local,upnp,ssu` | SSU adres keşfi kaynakları.                               |
| `i2p.router.net.ssu.detectedip` | null                                                | Salt okunur, tespit edilen SSU adresi.                              |
| `i2p.router.net.upnp`           | Dize                                              | UPnP ayarı.                                                |
| `i2p.router.net.bw.share`       | Dize, 0–100                                       | Katılım tüneleri için kullanılabilir bant genişliğinin yüzdesi. |
| `i2p.router.net.bw.in`          | Negatif olmayan tamsayı dizesi                         | Gelen bant genişliği sınırı KiB/s cinsinden.                            |
| `i2p.router.net.bw.out`         | Negatif olmayan tamsayı dizesi                         | Giden bant genişliği sınırı KiB/s cinsinden.                           |
| `i2p.router.net.laptopmode`     | Dize                                              | Dizüstü mod ayarı.                                         |
Ağ yapılandırma parametrelerini al veya ayarla (portlar, upnp, bant genişliği paylaşımı, vb.)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "5",
        "method": "NetworkSetting",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.net.ntcp.port": null,
          "i2p.router.net.ssu.port": null,
          "i2p.router.net.bw.share": null,
          "i2p.router.net.upnp": null
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**İstek Örneği (mevcut değerleri al)**

```json
{
  "jsonrpc": "2.0",
  "id": "5",
  "result": {
    "i2p.router.net.ntcp.port": "1234",
    "i2p.router.net.ssu.port": "5678",
    "i2p.router.net.bw.share": "50",
    "i2p.router.net.upnp": "true",
    "SettingsSaved": false,
    "RestartNeeded": false
  }
}
```
**Örnek Yanıt**

> Not: 2.41'den önceki i2pd sürümleri string yerine sayısal türler döndürebilir — istemciler her ikisini de işleyebilmelidir. :contentReference[oaicite:11]{index=11}

### 4.5 Gelişmiş Ayarlar

---

| Parametre | Tür                 | Açıklama                                                              |
|-----------|---------------------|-----------------------------------------------------------------------|
| `get`     | Dize                | Bir `get` sonuç nesnesi içinde tek bir ayar döndürür.                 |
| `getAll`  | yok                 | `getAll` içinde tam yapılandırma haritasını döndürür.                 |
| `set`     | Harita<Dize, Dize>  | Diğer anahtarları kaldırmadan verilen ayarları günceller.             |
| `setAll`  | Harita<Dize, Dize>  | **Yıkıcı:** tüm ayarların yerini alır ve verilmeyen anahtarları siler.|
İç router parametrelerini düzenlemeye izin verir.

**İstek Örneği**

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "6",
        "method": "AdvancedSettings",
        "params": {
          "Token": "a1b2c3d4e5",
          "set": {
            "router.sharePercentage": "75",
            "i2np.flushInterval": "6000"
          }
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Yanıt Örneği**

```json
{
  "jsonrpc": "2.0",
  "id": "6",
  "result": {}
}
```
---

### Standart JSON-RPC2 Hata Kodları

---

| Parametre | Tür    | Açıklama                    |
|-----------|--------|-----------------------------|
| `Echo`    | Dize   | `Result` olarak döndürülen değer. |
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "method": "Echo",
  "params": {
    "Token": "a1b2c3d4e5",
    "Echo": "hello"
  }
}
```
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "result": {
    "Result": "hello"
  }
}
```
---

### I2PControl Özel Hata Kodları

I2PControl'ü kendisi yönetir. Mevcut Java işleyicisi şifre değişikliklerini destekler.

| Parametre              | Tip    | Açıklama                                                                     |
|------------------------|--------|------------------------------------------------------------------------------|
| `i2pcontrol.password`  | Dize   | Yeni bir I2PControl şifresi ayarlar ve mevcut kimlik doğrulama tokenlarını iptal eder. |
Sonuç `SettingsSaved` değerini içerir. Şifre değiştirildiyse, sonuç ayrıca `"i2pcontrol.password": null` değerini de içerir. Eski tek başına eklentinin dinleme-adresi ve dinleme-bağlantı noktası ayarları, mevcut Java işleyicisinde etkin değildir.

> **Varsayılan şifre:** `itoopie` — bu fabrika varsayılanıdır ve güvenlik için **hemen değiştirilmelidir**.

## 5. Hata Kodları

### Standart JSON-RPC2 Hata Kodları

| Kod    | Anlamı               |
|--------|----------------------|
| -32700 | JSON çözümleme hatası |
| -32600 | Geçersiz istek       |
| -32601 | Yöntem bulunamadı    |
| -32602 | Geçersiz parametreler |
| -32603 | Dahili hata          |
### I2PControl'a Özel Hata Kodları

| Kod    | Anlamı                                                                                   |
|--------|------------------------------------------------------------------------------------------|
| -32001 | Geçersiz parola sağlandı                                                                |
| -32002 | Kimlik doğrulama belirteci sunulmadı                                                    |
| -32003 | Kimlik doğrulama belirteci mevcut değil                                                 |
| -32004 | Sağlanan kimlik doğrulama belirtecinin süresi dolmuş ve kaldırılacaktır                  |
| -32005 | Kullanılan I2PControl API sürümü belirtilmedi, ancak belirtilmesi gerekiyor             |
| -32006 | Belirtilen I2PControl API sürümü I2PControl tarafından desteklenmiyor                   |
> **Varsayılan şifre:** `itoopie` — bu fabrika varsayılanıdır ve güvenlik için **hemen değiştirilmelidir**.

## 6. Kullanım ve En İyi Uygulamalar

- Her zaman `Token` parametresini dahil edin (kimlik doğrulama yaparken hariç).  
- İlk kullanımda varsayılan parolayı (`itoopie`) değiştirin.  
- Java I2P için, I2PControl webapp'inin WebApps aracılığıyla etkinleştirildiğinden emin olun.  
- Küçük farklılıklara hazır olun: bazı alanlar I2P sürümüne bağlı olarak sayı veya metin olabilir.  
- Uzun durum metinlerini görüntü dostu çıktı için sarın.

> **Varsayılan şifre:** `itoopie` — bu fabrika varsayılanıdır ve güvenlik için **hemen değiştirilmelidir**.
