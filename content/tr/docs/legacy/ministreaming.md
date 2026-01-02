---
title: "Ministreaming Kütüphanesi"
description: "I2P'nin ilk TCP-benzeri taşıma katmanı üzerine tarihsel notlar"
slug: "ministreaming"
lastUpdated: "2025-02"
accurateFor: "historical"
---

> **Kullanımdan kaldırıldı:** ministreaming kütüphanesi, bugünkü [streaming kütüphanesinden](/docs/specs/streaming/) daha eskidir. Modern uygulamalar tam streaming API’sini veya SAM v3’ü kullanmalıdır. Aşağıdaki bilgiler, `ministreaming.jar` ile dağıtılan eski kaynak kodunu inceleyen geliştiriciler için tutulmuştur.

## Genel Bakış

Ministreaming (akış katmanı), [I2CP](/docs/specs/i2cp/)’nin üzerinde çalışarak I2P’nin mesaj katmanı genelinde güvenilir ve sıralı teslimi sağlar—tıpkı IP üzerinde TCP gibi. Alternatif taşıma yöntemlerinin bağımsız olarak gelişebilmesi için başlangıçta erken dönemdeki **I2PTunnel** uygulamasından (BSD lisanslı) ayrıştırıldı.

Temel tasarım kısıtları:

- TCP'den ödünç alınmış klasik iki aşamalı (SYN/ACK/FIN) bağlantı kurulumu
- Sabit pencere boyutu **1** paket
- Paket başına kimlikler (ID) veya seçmeli onaylar (SACK) yok

Bu seçimler uygulamayı küçük tuttu ancak aktarım verimini sınırlar—her paket, bir sonrakinin gönderilmesinden önce genellikle neredeyse iki RTT (gidiş-dönüş süresi) bekler. Uzun ömürlü akışlar için bu ek yük kabul edilebilir, ancak kısa süreli HTTP tarzı alışverişler gözle görülür biçimde olumsuz etkilenir.

## Streaming Library ile İlişkisi

Mevcut streaming kitaplığı aynı Java paketinde (`net.i2p.client.streaming`) yer alır. Kullanım dışı bırakılmış (deprecated) sınıflar ve yöntemler, geliştiricilerin ministreaming (eski akış kitaplığı) dönemi API'larını tanımlayabilmeleri için açık biçimde işaretlenmiş olarak Javadocs'ta yer almaya devam eder. Streaming kitaplığı, ministreaming'in yerini aldığında şunları ekledi:

- Daha az gidiş-dönüş ile daha akıllı bağlantı kurulumu
- Uyarlanabilir tıkanıklık pencereleri ve yeniden iletim mantığı
- Kayıplı tunnels üzerinde daha iyi performans

## Ministreaming Ne Zaman Kullanışlıydı?

Sınırlarına rağmen, ministreaming (kısıtlı özellikli akış kitaplığı) en erken dağıtımlarda güvenilir aktarım sağladı. API, alternatif akış motorları çağıranları bozmadan onun yerine geçirilebilsin diye kasten küçük ve geleceğe dönük tasarlandı. Java uygulamaları onu doğrudan bağladı; Java dışı istemciler ise aynı işlevselliğe akış oturumları için [SAM](/docs/legacy/sam/) desteği aracılığıyla erişti.

Bugün, `ministreaming.jar`'ı yalnızca bir uyumluluk katmanı olarak ele alın. Yeni geliştirmeler şunları yapmalıdır:

1. Tam akış kitaplığını (Java) veya SAM v3'ü (`STREAM` stili) hedefleyin  
2. Kodu modernleştirirken kalan sabit pencere varsayımlarını kaldırın  
3. Gecikmeye duyarlı iş yüklerini iyileştirmek için daha yüksek pencere boyutlarını ve optimize edilmiş bağlantı el sıkışmalarını tercih edin

## Referans

- [Streaming Library dokümantasyonu](/docs/specs/streaming/)
- [Streaming Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/client/streaming/package-summary.html) – kullanımdan kaldırılmış ministreaming sınıflarını içerir
- [SAM v3 spesifikasyonu](/docs/api/samv3/) – Java dışı uygulamalar için streaming desteği

Ministreaming (eski mini akış arabirimi) bağımlılığı olan bir kodla karşılaşırsanız, onu modern akış API'sine taşımayı planlayın — ağ ve araçları daha yeni davranışı bekler.
