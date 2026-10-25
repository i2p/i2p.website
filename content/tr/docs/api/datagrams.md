---
title: "Datagramlar"
description: "I2CP üzerinde kimlik doğrulamalı, yanıtlanabilir ve ham mesaj formatları"
slug: "datagrams"
aliases:
  - "/tr/datagrams"
  - "/tr/datagrams/"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## Datagram Genel Bakış {#overview}

Datagramlar, standart bir formatta kimliği doğrulanmış ve yanıtlanabilir mesajlar sağlamak için temel [I2CP](/docs/specs/i2cp) üzerine inşa edilir. Bu, uygulamaların bir datagramdan "kimden" adresini güvenilir bir şekilde okuyabilmesini ve bu adresin gerçekten mesajı gönderdiğini bilmesini sağlar. Bu, bazı uygulamalar için gereklidir çünkü temel I2P mesajı tamamen ham veridir - (IP paketlerinin aksine) "kimden" adresi yoktur. Ayrıca, mesaj ve gönderen, yük imzalanarak doğrulanır.

Datagramlar, [streaming library paketleri](/docs/api/streaming) gibi, uygulama düzeyinde bir yapıdır. Bu protokoller, düşük seviyeli [transport'lardan](/docs/overview/transport) bağımsızdır; protokoller router tarafından I2NP mesajlarına dönüştürülür ve her iki protokol de her iki transport tarafından taşınabilir.

## Uygulama Kılavuzu {#application}

Java ile yazılmış uygulamalar datagram API'sini kullanabilirken, diğer dillerdeki uygulamalar [SAM](/docs/api/samv3)'in datagram desteğini kullanabilir. Ayrıca i2ptunnel'da [SOCKS proxy](/docs/api/socks), 'streamr' tunnel türleri ve udpTunnel sınıflarında sınırlı destek bulunmaktadır.

### Datagram Uzunluğu {#length}

Uygulama tasarımcısı, yanıtlanabilir ve yanıtlanamaz datagramlar arasındaki değişimi dikkatlice değerlendirmelidir. Ayrıca, datagram boyutu, tunnel'ların 1KB tunnel mesajlarına parçalanması nedeniyle güvenilirliği etkileyecektir. Mesaj parçası sayısı ne kadar fazla olursa, bunlardan birinin ara bir atlama noktasında düşürülme olasılığı o kadar yüksek olur. Birkaç KB'den büyük mesajlar önerilmez. Yaklaşık 10 KB'nin üzerinde, teslim olasılığı dramatik şekilde düşer.

[Datagram Spesifikasyonu sayfasına bakın.](/docs/specs/datagrams)

Ayrıca, alt katmanlar tarafından eklenen çeşitli ek yüklerin, özellikle garlic message'ların, Kademlia-over-UDP uygulaması tarafından kullanılan gibi aralıklı mesajlar üzerinde büyük bir yük oluşturduğunu unutmayın. Mevcut uygulamalar, streaming kütüphanesini kullanan sık trafik için optimize edilmiştir.

### I2CP Protokol Numarası ve Portları {#protocol}

İmzalı (yanıtlanabilir) datagramlar için standart I2CP protokol numarası PROTO_DATAGRAM (17)'dir. Uygulamalar I2CP başlığında protokolü ayarlamayı seçebilir veya seçmeyebilir. Varsayılan değer implementasyona bağlıdır. Aynı Destination üzerinde alınan datagram ve streaming trafiğini ayrıştırmak için ayarlanması gerekir.

Datagramlar bağlantı-odaklı olmadığından, uygulama datagramları belirli eşler veya iletişim oturumlarıyla ilişkilendirmek için port numaralarına ihtiyaç duyabilir; bu IP üzerinden UDP ile geleneksel olan bir durumdur. Uygulamalar, [I2CP sayfasında](/docs/specs/i2cp#format) açıklandığı gibi I2CP (gzip) başlığına 'from' ve 'to' portlarını ekleyebilir.

Datagram API'sinde bir datagramın yanıtlanamaz (ham) mi yoksa yanıtlanabilir mi olduğunu belirtecek bir yöntem yoktur. Uygulama uygun türü beklemeye göre tasarlanmalıdır. I2CP protokol numarası veya port, datagram türünü belirtmek için uygulama tarafından kullanılmalıdır. I2CP protokol numaraları PROTO_DATAGRAM (imzalı, Datagram1 olarak da bilinir), PROTO_DATAGRAM_RAW, PROTO_DATAGRAM2 ve PROTO_DATAGRAM3 bu amaç için I2PSession API'sinde tanımlanmıştır. İstemci/sunucu datagram uygulamalarında yaygın bir tasarım deseni, bir nonce içeren istek için imzalı datagram kullanmak ve yanıt için ham datagram kullanarak istekteki nonce'i geri döndürmektir.

**Varsayılanlar:**

- PROTO_DATAGRAM = 17
- PROTO_DATAGRAM_RAW = 18
- PROTO_DATAGRAM2 = 19
- PROTO_DATAGRAM3 = 20

### Veri Bütünlüğü {#integrity}

Veri bütünlüğü, [I2CP katmanında](/docs/specs/i2cp#format) uygulanan gzip CRC-32 sağlama toplamı ile garanti edilir. Kimlik doğrulamalı datagramlar (Datagram1 ve Datagram2) da bütünlüğü sağlar. Datagram protokolünde sağlama toplamı alanı yoktur.

### Paket Kapsülleme {#encapsulation}

Her datagram, I2P üzerinden tek bir mesaj olarak (veya bir [Garlic Message](/docs/overview/garlic-routing) içindeki ayrı bir clove olarak) gönderilir. Mesaj kapsülleme, altta yatan [I2CP](/docs/specs/i2cp), [I2NP](/docs/specs/i2np) ve [tunnel message](/docs/specs/tunnel-message) katmanlarında uygulanır. Datagram protokolünde paket ayırıcı mekanizması veya uzunluk alanı bulunmaz.

## Spesifikasyon {#spec}

[Datagram Spesifikasyonu sayfasına bakınız.](/docs/specs/datagrams)
