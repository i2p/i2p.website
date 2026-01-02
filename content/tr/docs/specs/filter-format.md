---
title: "Erişim Filtresi Biçimi"
description: "tunnel erişim denetimi filtre dosyaları için söz dizimi"
slug: "filter-format"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Erişim filtreleri, I2PTunnel sunucu işletmecilerinin, kaynak Destination (I2P'de hedef kimliği) ve yakın zamandaki bağlantı sıklığına göre gelen bağlantılara izin vermesine, bunları reddetmesine veya kısıtlamasına olanak tanır. Filtre, kurallardan oluşan düz metin bir dosyadır. Dosya yukarıdan aşağıya okunur ve **ilk eşleşen kural geçerlidir**.

> Filtre tanımındaki değişiklikler, **tunnel yeniden başlatıldığında** yürürlüğe girer. Bazı sürümler çalışma sırasında dosya tabanlı listeleri yeniden okuyabilir, ancak değişikliklerin uygulandığını garanti etmek için bir yeniden başlatmayı planlayın.

## Dosya biçimi

- Her satırda bir kural.  
- Boş satırlar dikkate alınmaz.  
- `#`, satırın sonuna kadar devam eden bir yorum başlatır.  
- Kurallar sırayla değerlendirilir; ilk eşleşme kullanılır.

## Eşikler

Bir **eşik**, kayan bir zaman penceresi içinde tek bir Destination (uç nokta) için izin verilen bağlantı denemesi sayısını tanımlar.

- **Sayısal:** `N/S`, `S` saniye başına `N` bağlantıya izin verir. Örnek: `15/5`, her 5 saniyede en fazla 15 bağlantıya izin verir. Pencere içinde yapılan `N+1`'inci deneme reddedilir.  
- **Anahtar kelimeler:** `allow` herhangi bir sınır olmadığı anlamına gelir. `deny` her zaman reddet anlamına gelir.

## Kural sözdizimi

Kurallar şu biçimdedir:

```
<threshold> <scope> <target>
```
Burada:

- `<threshold>` `N/S`, `allow` veya `deny` olabilir  
- `<scope>`, `default`, `explicit`, `file` veya `record` değerlerinden biridir (aşağıya bakın)  
- `<target>` kapsama bağlıdır

### Varsayılan kural

Başka hiçbir kural eşleşmediğinde uygulanır. Yalnızca **bir** varsayılan kurala izin verilir. Belirtilmezse, bilinmeyen Destinations (Hedefler) herhangi bir kısıtlama olmaksızın izin verilir.

```
15/5 default
allow default
deny default
```
### Açık kural

Base32 adresi (örneğin `example1.b32.i2p`) veya tam anahtar ile belirli bir hedefi hedefler.

```
15/5 explicit example1.b32.i2p
deny explicit example2.b32.i2p
allow explicit example3.b32.i2p
```
### Dosya tabanlı kural

Harici bir dosyada listelenen Destinations'ın **tümünü** hedefler. Her satır bir Destination içerir; `#` yorumları ve boş satırlara izin verilir.

```
15/5 file /var/i2p/throttled.txt
deny file /var/i2p/blocked.txt
allow file /var/i2p/trusted.txt
```
> İşletim notu: Bazı gerçeklemeler dosya listelerini periyodik olarak yeniden okur. tunnel çalışırken bir listeyi düzenlerseniz, değişikliklerin fark edilmesinden önce kısa bir gecikme bekleyin. Hemen uygulanması için yeniden başlatın.

### Kaydedici (kademeli kontrol)

Bir **recorder** (kaydedici) bağlantı denemelerini izler ve eşik değerini aşan hedefleri bir dosyaya yazar. Daha sonra, gelecekteki denemelere hız sınırlamaları veya engellemeler uygulamak için o dosyaya bir `file` kuralında referans verebilirsiniz.

```
# Start permissive
allow default

# Record Destinations exceeding 30 connections in 5 seconds
30/5 record /var/i2p/aggressive.txt

# Apply throttling to recorded Destinations
15/5 file /var/i2p/aggressive.txt
```
> Ona güvenmeden önce derlemenizde kaydedici desteğini doğrulayın. Garanti edilen davranış için `file` listelerini kullanın.

## Değerlendirme sırası

Önce özel kuralları, ardından genel olanları yazın. Yaygın bir kalıp:

1. Güvenilir eşler için açık izinler  
2. Bilinen kötüye kullananlar için açık retler  
3. Dosya tabanlı izin/ret listeleri  
4. Kademeli hız kısma için kaydediciler  
5. Her şeyi kapsayan bir varsayılan kural

## Tam örnek

```
# Moderate limits by default
30/10 default

# Always allow trusted peers
allow explicit friend1.b32.i2p
allow explicit friend2.b32.i2p

# Block known bad actors
deny file /var/i2p/blocklist.txt

# Throttle aggressive sources
15/5 file /var/i2p/throttle.txt

# Automatically populate the throttle list
60/5 record /var/i2p/throttle.txt
```
## Uygulama notları

- Erişim filtresi, uygulama tarafından işlenmeden önce, tunnel katmanında çalışır; böylece kötüye kullanım amaçlı trafik erken reddedilebilir.  
- Filtre dosyasını I2PTunnel yapılandırma dizinine yerleştirin ve değişikliklerin uygulanması için tunnel'i yeniden başlatın.  
- Hizmetler genelinde tutarlı bir ilke istiyorsanız, dosya tabanlı listeleri birden fazla tunnel arasında paylaşın.
