---
title: "Tunnel Mesajı Spesifikasyonu"
description: "I2P'de tunnel mesajlarının formatı için spesifikasyon"
slug: "tunnel-message"
aliases:
  - "/tr/docs/legacy/tunnel-message"
  - "/tr/docs/legacy/tunnel-message/"
  - "/tr/tunnel_message_spec"
  - "/tr/tunnel_message_spec/"
category: "Tasarım"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## Genel Bakış

Bu belge tunnel mesajlarının formatını belirtir. Tunnel'lar hakkında genel bilgi için [tunnel dokümantasyonuna](/docs/specs/tunnel-implementation) bakın.

## Mesaj Ön İşleme

Bir *tunnel gateway* (tünel ağ geçidi), bir tünelin girişi veya ilk adımıdır. Giden tünel için gateway, tüneli oluşturan taraftır. Gelen tünel için ise gateway, tüneli oluşturan tarafın karşı ucundadır.

Bir gateway, [I2NP](/docs/specs/i2np) mesajlarını parçalara ayırarak ve tunnel mesajları halinde birleştirerek *ön işleme* tabi tutar.

I2NP mesajları 0'dan neredeyse 64 KB'ye kadar değişken boyutta olsa da, tunnel mesajları sabit boyuttadır ve yaklaşık 1 KB'dir. Sabit mesaj boyutu, mesaj boyutunu gözlemleyerek gerçekleştirilebilecek çeşitli saldırı türlerini kısıtlar.

Tunnel mesajları oluşturulduktan sonra, [tunnel dokümantasyonunda](/docs/specs/tunnel-implementation) açıklandığı şekilde şifrelenir.

### Tunnel Mesajı (Şifrelenmiş)

Bunlar şifreleme sonrasında bir tunnel veri mesajının içeriğidir.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |                   |
+----+----+----+----+                   +
|                                       |
+           Encrypted Data              +
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 bayt. Bir sonraki hop'un ID'si, sıfır olmayan.

**IV** :: : 16 bayt. Başlatma vektörü.

**Şifrelenmiş Veri** :: : 1008 bayt. Şifrelenmiş tunnel mesajı.

**Toplam boyut: 1028 bayt**

### Tunnel Mesajı (Şifresi Çözülmüş)

Bunlar şifrelenmiş tunnel veri mesajının içeriğidir.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |     Checksum      |
+----+----+----+----+----+----+----+----+
|          nonzero padding...           |
~                                       ~
|                                       |
+                                  +----+
|                                  |zero|
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions  1        |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 1         +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions 2...      |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 2...      +
|                                       |
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 bayt. Bir sonraki hop'un ID'si, sıfır olmayan.

**IV** :: : 16 bayt. Başlatma vektörü.

**Checksum** :: : 4 bayt. (mesajın içeriği (sıfır baytından sonra) + IV)'nin SHA256 hash'inin ilk 4 baytı.

**Sıfır olmayan dolgu** :: : 0 veya daha fazla bayt. Dolgu için rastgele sıfır olmayan veri.

**Zero** :: : 1 bayt. 0x00 değeri.

**Teslimat Talimatları** :: TunnelMessageDeliveryInstructions : Uzunluk değişkendir ancak genellikle 7, 39, 43 veya 47 bayttır. Parçayı ve parça için yönlendirmeyi belirtir.

**Mesaj Parçası** :: : 1 ila 996 bayt, gerçek maksimum teslimat talimatı boyutuna bağlıdır. Kısmi veya tam bir I2NP Mesajı.

**Toplam boyut: 1028 bayt**

#### Notlar

- Dolgu varsa, talimat/mesaj çiftlerinden önce olmalıdır. Sonunda dolgu için herhangi bir hüküm yoktur.
- Sağlama toplamı dolguyu veya sıfır baytını kapsamaz. İlk teslimat talimatlarından başlayan mesajı alın, IV'yi birleştirin ve bunun Hash'ini alın.

## Tunnel Mesaj Teslim Talimatları

Talimatlar tek bir kontrol baytı ile kodlanır ve ardından gerekli ek bilgiler gelir. Bu kontrol baytındaki ilk bit (MSB), başlığın geri kalanının nasıl yorumlanacağını belirler - eğer ayarlanmamışsa, mesaj ya parçalanmamıştır ya da bu mesajdaki ilk parçadır. Eğer ayarlanmışsa, bu bir takip eden parçadır.

Bu özellik yalnızca Tunnel Mesajları içindeki Delivery Instructions için geçerlidir. "Delivery Instructions"ların Garlic Cloves içinde de kullanıldığını, ancak formatının önemli ölçüde farklı olduğunu unutmayın. Ayrıntılar için [I2NP belgelerine](/docs/specs/i2np#garlicclovedeliveryinstructions) bakın. Garlic Clove Delivery Instructions için aşağıdaki özellikleri KULLANMAYIN!

### İlk Fragment Teslimat Talimatları

İlk baytın MSB'si 0 ise, bu bir başlangıç I2NP mesaj parçası veya tam (parçalanmamış) bir I2NP mesajıdır ve talimatlar şunlardır:

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +--------------+
|                        |dly | Message
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|  size   |
+----+----+----+----+----+----+----+----+
```
**flag** :: : 1 bayt. Bit sırası: 76543210   - bit 7: başlangıç parçasını veya parçalanmamış mesajı belirtmek için 0   - bit 6-5: teslimat türü

    - 0x0 = LOCAL
    - 0x01 = TUNNEL
    - 0x02 = ROUTER
    - 0x03 = unused, invalid
    - Note: LOCAL is used for inbound tunnels only, unimplemented for outbound tunnels
- bit 4: gecikme dahil mi? Uygulanmamış, her zaman 0. Eğer 1 ise, bir gecikme byte'ı dahil edilir.
  - bit 3: parçalanmış mı? Eğer 0 ise, mesaj parçalanmamıştır, takip eden tüm mesajdır. Eğer 1 ise, mesaj parçalanmıştır ve talimatlar bir Message ID içerir.
  - bit 2: genişletilmiş seçenekler? Uygulanmamış, her zaman 0. Eğer 1 ise, genişletilmiş seçenekler dahil edilir.
  - bit 1-0: ayrılmış, gelecekteki kullanımlarla uyumluluk için 0 olarak ayarlanır

**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 bayt. İsteğe bağlı, teslimat türü TUNNEL ise mevcut. Hedef tunnel ID'si, sıfırdan farklı.

**To Hash** :: : 32 bayt. İsteğe bağlı, teslimat türü ROUTER veya TUNNEL ise mevcut. Eğer ROUTER ise, router'ın SHA256 Hash'i. Eğer TUNNEL ise, gateway router'ın SHA256 Hash'i.

**Gecikme** :: : 1 bayt. İsteğe bağlı, gecikme dahil edildi bayrağı ayarlanmışsa mevcut. Tunnel mesajlarında: Uygulanmamış, hiçbir zaman mevcut değil; orijinal spesifikasyon: bit 7: tip (0 = katı, 1 = rastgele), bit 6-0: gecikme üssü (2^değer dakika).

**Message ID** :: : 4 bayt. İsteğe bağlı, bu mesaj 2 veya daha fazla parçanın ilkiyse mevcut (yani fragmented bit 1 ise). Tüm parçaları tek bir mesaja ait olarak benzersiz şekilde tanımlayan bir ID (mevcut uygulama I2NPMessageHeader.msg_id kullanır).

**Genişletilmiş Seçenekler** :: : 2 veya daha fazla bayt. İsteğe bağlı, genişletilmiş seçenekler bayrağı ayarlanmışsa mevcut. Uygulanmamış, hiçbir zaman mevcut değil; orijinal spesifikasyon: Bir bayt uzunluğu ve ardından o kadar bayt.

**size** :: : 2 bayt. Takip eden parçanın uzunluğu. Geçerli değerler: tunnel mesajında 1 ile yaklaşık 960 arası.

**Toplam uzunluk:** Tipik uzunluk: - LOCAL teslimat için 3 bayt (tunnel mesajı) - ROUTER teslimatı için 35 bayt veya TUNNEL teslimatı için 39 bayt (parçalanmamış tunnel mesajı) - ROUTER teslimatı için 39 bayt veya TUNNEL teslimatı için 43 bayt (ilk parça)

### Takip Eden Parça Teslimat Talimatları

İlk baytın MSB'si 1 ise, bu bir devam parçasıdır ve talimatlar şunlardır:

```
+----+----+----+----+----+----+----+
|frag|     Message ID    |  size   |
+----+----+----+----+----+----+----+
```
**frag** :: : 1 byte. Bit sırası: 76543210. Binary 1nnnnnnd:   - bit 7: bunun takip eden bir fragment olduğunu belirtmek için 1   - bit 6-1: nnnnnn, 1'den 63'e kadar 6 bitlik fragment numarası   - bit 0: d, son fragment'ı belirtmek için 1, aksi halde 0

**Message ID** :: : 4 bayt. Bu parçanın ait olduğu parça dizisini tanımlar. Bu, bir başlangıç parçasının message ID'si ile eşleşecektir (bayrak biti 7'si 0'a ve bayrak biti 3'ü 1'e ayarlanmış bir parça).

**size** :: : 2 bayt. Takip eden parçanın uzunluğu. Geçerli değerler: 1 ile 996 arası.

**Toplam uzunluk: 7 bayt**

## Notlar

### I2NP Mesaj Maksimum Boyutu

Maksimum I2NP mesaj boyutu nominal olarak 64 KB olsa da, I2NP mesajlarının birden fazla 1 KB tunnel mesajına bölünme yöntemi ile boyut daha da kısıtlanır. Maksimum fragment sayısı 64'tür ve ilk fragment bir tunnel mesajının başlangıcında mükemmel şekilde hizalanmayabilir. Bu nedenle mesaj nominal olarak 63 fragment'e sığmalıdır.

İlk fragmanın maksimum boyutu 956 bayttır (TUNNEL teslimat modu varsayılarak); takip eden fragmanların maksimum boyutu 996 bayttır. Bu nedenle maksimum boyut yaklaşık olarak 956 + (62 * 996) = 62708 bayt veya 61.2 KB'dir.

### Sıralama, Toplu İşleme, Paketleme

Tunnel mesajları düşürülebilir veya yeniden sıralanabilir. Tunnel mesajlarını oluşturan tunnel gateway, I2NP mesajlarını parçalamak ve parçaları tunnel mesajlarına verimli bir şekilde paketlemek için herhangi bir toplu işleme, karıştırma veya yeniden sıralama stratejisi uygulayabilir. Genel olarak, optimal bir paketleme mümkün değildir ("paketleme problemi"). Gateway'ler çeşitli gecikme ve yeniden sıralama stratejileri uygulayabilir.

### Gizleme Trafiği

Tunnel mesajları, gizleme trafiği için yalnızca dolgu içerebilir (yani hiçbir teslimat talimatı veya mesaj parçası olmadan). Bu henüz uygulanmamıştır.

## Referanslar

- **[I2NP]** [I2NP Protokolü](/docs/specs/i2np)
- **[I2NP-GC]** [GarlicClove](/docs/specs/i2np#garlicclove)
- **[I2NP-GCDI]** [GarlicCloveDeliveryInstructions](/docs/specs/i2np#garlicclovedeliveryinstructions)
- **[TUNNEL-IMPL]** [Tunnel Uygulaması](/docs/specs/tunnel-implementation)
