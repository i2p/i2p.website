---
title: "v3dgsend"
description: "SAM v3 üzerinden I2P datagram gönderimi için CLI aracı"
slug: "v3dgsend"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> Durum: Bu, `v3dgsend` yardımcı programı için özet bir referanstır. [Datagram API](/docs/api/datagrams/) ve [SAM v3](/docs/api/samv3/) belgelerini tamamlar.

## Genel Bakış

`v3dgsend`, SAMv3 arayüzünü kullanarak I2P datagram'ları göndermek için bir komut satırı yardımcı aracıdır. Datagram teslimini test etmek, hizmet prototipleri oluşturmak ve tam bir istemci yazmadan uçtan uca davranışı doğrulamak için kullanışlıdır.

Tipik kullanımlar şunları içerir:

- Bir Hedef'e datagram erişilebilirliğinin basit testini yapma
- Güvenlik duvarı ve adres defteri yapılandırmasını doğrulama
- Ham ve imzalı (yanıtlanabilir) datagram'lar ile deneyler yapma

## Kullanım

Temel çağrı şekli, platforma ve paketlemeye göre değişir. Yaygın seçenekler şunlardır:

- Destination: base64 Destination veya `.i2p` adı
- Protocol: raw (PROTOCOL 18) veya signed (PROTOCOL 17)
- Payload: satır içi metin veya dosya girişi

Tam bayraklar için dağıtımınızın paketlemesine veya `--help` çıktısına bakın.

## Ayrıca Bakınız

- [Datagram API](/docs/api/datagrams/)
- [SAM v3](/docs/api/samv3/)
- [Streaming Kütüphanesi](/docs/api/streaming/) (datagram'lara alternatif)
