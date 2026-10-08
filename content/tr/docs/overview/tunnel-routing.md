---
title: "Tunnel Yönlendirme"
description: "I2P tunnel terminolojisi, yapısı ve işleyişine genel bakış"
slug: "tunnel-routing"
lastUpdated: "2026-03"
accurateFor: "0.9.68"
---

## Genel Bakış

Bu sayfa, daha teknik sayfalara, ayrıntılara ve spesifikasyonlara bağlantılar içeren I2P tunnel terminolojisi ve işleyişine genel bir bakış sunar.

[Girişte](/docs/overview/intro/) kısaca açıklandığı gibi, I2P sanal "tunnel'lar" oluşturur - router'ların bir dizisi üzerinden geçen geçici ve tek yönlü yollar. Bu tunnel'lar ya gelen tunnel'lar (kendisine verilen her şeyin tunnel'ı oluşturanın yönüne gittiği) ya da giden tunnel'lar (tunnel oluşturanın mesajları kendisinden uzağa ittiği) olarak sınıflandırılır. Alice, Bob'a bir mesaj göndermek istediğinde, (genellikle) mevcut giden tunnel'larından birinden mesajı gönderir ve bu tunnel'ın uç noktasına, mesajı Bob'un mevcut gelen tunnel'larından birinin ağ geçidi router'ına iletmesi talimatını verir, bu da mesajı Bob'a aktarır.

![Alice giden tunnel'ı üzerinden Bob'un gelen tunnel'ına bağlanıyor](/images/tunnelSending.svg)

```
A: Outbound Gateway (Alice)
B: Outbound Participant
C: Outbound Endpoint
D: Inbound Gateway
E: Inbound Participant
F: Inbound Endpoint (Bob)
```
---

## Tunnel Sözlüğü

- **Tunnel gateway** - bir tunnel'daki ilk router. Inbound tunnel'lar için, bu [network database](/docs/overview/network-database/)'de yayınlanan LeaseSet'te bahsedilen router'dır. Outbound tunnel'lar için, gateway kaynak router'dır. (örneğin yukarıdaki hem A hem D)

- **Tunnel uç noktası** - bir tunnel'daki son router. (örneğin yukarıdaki hem C hem de F)

- **Tunnel katılımcısı** - bir tunnel'daki gateway veya endpoint dışındaki tüm router'lar (örneğin yukarıdaki B ve E)

- **n-Hop tunnel** - belirli sayıda router arası atlama içeren tunnel, örneğin:
  - **0-hop tunnel** - gateway'in aynı zamanda endpoint olduğu tunnel
  - **1-hop tunnel** - gateway'in doğrudan endpoint ile konuştuğu tunnel
  - **2-(veya daha fazla)-hop tunnel** - en az bir ara tunnel katılımcısının bulunduğu tunnel. (yukarıdaki diyagram iki 2-hop tunnel içermektedir - biri Alice'den giden outbound, diğeri Bob'a gelen inbound)

- **Tunnel ID** - Bir tunnel'daki her hop için farklı olan ve bir router üzerindeki tüm tunnel'lar arasında benzersiz olan [4 baytlık tamsayı](/docs/specs/common-structures/#type_TunnelId). Tunnel oluşturan tarafından rastgele seçilir.

---

## Tunnel Oluşturma Bilgileri

Üç rolü (gateway, participant, endpoint) gerçekleştiren router'lar, görevlerini yerine getirmek için başlangıçtaki [Tunnel Build Message](/docs/specs/tunnel-creation/) içinde farklı veri parçaları alırlar:

**Tunnel gateway şunu alır:**

- **tunnel encryption key** - bir sonraki hop'a mesajları ve talimatları şifrelemek için bir [AES özel anahtarı](/docs/specs/common-structures/#type_SessionKey)
- **tunnel IV key** - bir sonraki hop'a IV'yi çift şifrelemek için bir [AES özel anahtarı](/docs/specs/common-structures/#type_SessionKey)
- **reply key** - tunnel oluşturma isteğine yanıtı şifrelemek için bir [AES genel anahtarı](/docs/specs/common-structures/#type_SessionKey)
- **reply IV** - tunnel oluşturma isteğine yanıtı şifrelemek için IV
- **tunnel id** - 4 bayt tam sayı (yalnızca gelen gateway'ler için)
- **next hop** - yolda bir sonraki router hangisi (bu 0-hop tunnel değilse ve gateway aynı zamanda uç nokta değilse)
- **next tunnel id** - Bir sonraki hop'taki tunnel ID'si

**Tüm ara tunnel katılımcıları şunları alır:**

- **tunnel encryption key** - bir sonraki hop'a mesajları ve talimatları şifrelemek için bir [AES özel anahtarı](/docs/specs/common-structures/#type_SessionKey)
- **tunnel IV key** - bir sonraki hop'a IV'yi çift şifrelemek için bir [AES özel anahtarı](/docs/specs/common-structures/#type_SessionKey)
- **reply key** - tunnel oluşturma isteğine verilen yanıtı şifrelemek için bir [AES genel anahtarı](/docs/specs/common-structures/#type_SessionKey)
- **reply IV** - tunnel oluşturma isteğine verilen yanıtı şifrelemek için IV
- **tunnel id** - 4 bayt tamsayı
- **next hop** - yolda bir sonraki router hangisidir
- **next tunnel id** - Bir sonraki hop'taki tunnel ID'si

**Tunnel uç noktası alır:**

- **tunnel şifreleme anahtarı** - uç noktaya (kendisine) mesaj ve talimatları şifrelemek için bir [AES özel anahtarı](/docs/specs/common-structures/#type_SessionKey)
- **tunnel IV anahtarı** - uç noktaya (kendisine) IV'yi çift şifrelemek için bir [AES özel anahtarı](/docs/specs/common-structures/#type_SessionKey)
- **yanıt anahtarı** - tunnel inşa isteğine yanıtı şifrelemek için bir [AES genel anahtarı](/docs/specs/common-structures/#type_SessionKey) (yalnızca giden uç noktalar)
- **yanıt IV'si** - tunnel inşa isteğine yanıtı şifrelemek için IV (yalnızca giden uç noktalar)
- **tunnel kimliği** - 4 bayt tam sayı (yalnızca giden uç noktalar)
- **yanıt router'ı** - yanıtı göndermek için tunnel'ın gelen ağ geçidi (yalnızca giden uç noktalar)
- **yanıt tunnel kimliği** - Yanıt router'ının tunnel ID'si (yalnızca giden uç noktalar)

Detaylar [tunnel oluşturma spesifikasyonunda](/docs/specs/tunnel-creation/) bulunmaktadır.

---

## Tunnel Havuzlama

Belirli bir amaç için birden fazla tunnel, [tunnel spesifikasyonu](/docs/specs/tunnel-implementation/#tunnel.pooling)'nda açıklandığı gibi bir "tunnel pool"'unda gruplandırılabilir. Bu, yedeklilik ve ek bant genişliği sağlar. Router'ın kendisi tarafından kullanılan pool'lar "exploratory tunnel"'lar olarak adlandırılır. Uygulamalar tarafından kullanılan pool'lar ise "client tunnel"'lar olarak adlandırılır.

---

## Tunnel Uzunluğu

Yukarıda belirtildiği gibi, her istemci router'ından belirli sayıda en az hop içeren tunnel'lar sağlamasını talep eder. Kişinin giden ve gelen tunnel'larında kaç router bulunduracağına dair karar, I2P tarafından sağlanan gecikme, aktarım hızı, güvenilirlik ve anonimlik üzerinde önemli bir etkiye sahiptir - mesajların geçmesi gereken peer sayısı ne kadar fazlaysa, varış süresi o kadar uzun olur ve bu router'lardan birinin zamanından önce arızalanma olasılığı o kadar yüksek olur. Bir tunnel'daki router sayısı ne kadar azsa, bir saldırganın trafik analizi saldırıları düzenlemesi ve birinin anonimliğini kırması o kadar kolay olur. Tunnel uzunlukları istemciler tarafından [I2CP seçenekleri](/docs/specs/i2cp/#options) ile belirtilir. Bir tunnel'daki maksimum hop sayısı 7'dir.

### 0-hop tunnel'lar

Bir tunnel'da uzak router olmadığında, kullanıcı çok temel bir makul inkar edilebilirlik (plausible deniability) sahiptir (çünkü kendilerine mesajı gönderen peer'ın sadece tunnel'ın bir parçası olarak onu iletmediğinden kimse emin olamaz). Ancak, istatistiksel analiz saldırısı düzenlemek ve belirli bir hedefe yönelik mesajların her zaman tek bir gateway üzerinden gönderildiğini fark etmek oldukça kolay olurdu. Giden 0-hop tunnel'lara karşı istatistiksel analizler daha karmaşıktır, ancak benzer bilgileri gösterebilir (gerçi düzenlemesi biraz daha zor olurdu).

### 1 atlama tunnel'ları

Tunnel içinde yalnızca bir uzak router ile kullanıcı, dahili bir düşmana karşı olmadığı sürece ([tehdit modeli](/docs/overview/threat-model/) sayfasında açıklandığı gibi) hem makul inkar edilebilirlik hem de temel anonimlik elde eder. Ancak, düşman tunnel içindeki tek uzak router'ın sık sık bu ele geçirilmiş router'lardan biri olacak kadar yeterli sayıda router çalıştırırsa, yukarıdaki istatistiksel trafik analizi saldırısını gerçekleştirebilirdi.

### 2-sıçrama tunnel'ları

Bir tunnel'da iki veya daha fazla uzak router bulunduğunda, trafik analizi saldırısı düzenlemenin maliyeti artar, çünkü bu saldırıyı gerçekleştirmek için birçok uzak router'ın ele geçirilmesi gerekir.

### 3-hop (veya daha fazla) tunnel'lar

[Bazı saldırılara](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/) karşı hassasiyeti azaltmak için en yüksek koruma düzeyi için 3 veya daha fazla zıplama önerilir. [Son yapılan çalışmalar](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/), 3'ten fazla zıplamanın ek koruma sağlamadığını da sonuca varmaktadır.

### Tunnel varsayılan uzunlukları

Router, keşif tunnel'ları için varsayılan olarak 2-hop tunnel'ları kullanır. İstemci tunnel varsayılanları [I2CP seçenekleri](/docs/specs/i2cp/#options) kullanılarak uygulama tarafından ayarlanır. Çoğu uygulama varsayılan olarak 2 veya 3 hop kullanır.

---

## Tunnel Testi

Tüm tunnel'lar, yaratıcıları tarafından periyodik olarak test edilir; bir DeliveryStatusMessage gönderilerek outbound tunnel üzerinden başka bir inbound tunnel'a yönlendirilir (her iki tunnel'ı aynı anda test eder). Eğer herhangi biri art arda birkaç testi başarısız olursa, artık işlevsel olmadığı olarak işaretlenir. Eğer bir istemcinin inbound tunnel'ı için kullanılıyorsa, yeni bir leaseSet oluşturulur. Tunnel test başarısızlıkları ayrıca [peer profildeki kapasite değerlendirmesine](/docs/overview/peer-selection/#capacity) de yansıtılır.

---

Tunnel oluşturma, bir router'a Tunnel Build Message gönderen [garlic routing](/docs/overview/garlic-routing/) tarafından ele alınır ve o router'ın tunnel'a katılmasını talep eder (yukarıda belirtildiği gibi tüm uygun bilgileri ve bir sertifika sağlar - bu sertifika şu anda 'null' sertifikadır, ancak gerektiğinde hashcash veya diğer ücretsiz olmayan sertifikaları destekleyecektir). Bu router, mesajı tunnel'daki bir sonraki hop'a iletir. Detaylar [tunnel oluşturma spesifikasyonunda](/docs/specs/tunnel-creation/) bulunabilir.

## Tunnel Oluşturma

---

Çok katmanlı şifreleme, tunnel mesajlarının [garlic encryption](/docs/overview/garlic-routing/) ile gerçekleştirilir. Detaylar [tunnel spesifikasyonunda](/docs/specs/tunnel-implementation/) bulunmaktadır. Her hop'un IV'si orada açıklandığı gibi ayrı bir anahtar ile şifrelenir.

## Tunnel Şifreleme

---

---

## Gelecekteki Çalışmalar

- Garlic encryption ile birkaç testi tek bir pakete sarmalama, bireysel tunnel katılımcılarını ayrı ayrı test etme gibi diğer tunnel test teknikleri kullanılabilir.

- 3-hop keşif tunnel'larının varsayılan ayarlarına geç.

- Uzak gelecekteki bir sürümde, havuzlama, karıştırma ve sahte trafik üretimi ayarlarını belirten seçenekler uygulanabilir.

- Uzak bir gelecek sürümünde, tunnel'ın yaşam süresi boyunca izin verilen mesaj miktarı ve boyutu üzerinde sınırlar uygulanabilir (örneğin, dakikada 300'den fazla mesaj veya 1MB'dan fazla olmayacak şekilde).

---

## Ayrıca Bakınız

- [Tunnel spesifikasyonu](/docs/specs/tunnel-implementation/)
- [Tunnel oluşturma spesifikasyonu](/docs/specs/tunnel-creation/)
- [Tek yönlü tunnel'lar](/docs/legacy/unidirectional/)
- [Tunnel mesaj spesifikasyonu](/docs/specs/tunnel-message/)
- [Garlic routing](/docs/overview/garlic-routing/)
- [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/)
- [I2CP seçenekleri](/docs/specs/i2cp/#options)
