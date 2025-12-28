---
title: "SAM v2"
description: "Eski Simple Anonymous Messaging protokolü"
slug: "samv2"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Kullanımdan kaldırıldı:** SAM v2, I2P 0.6.1.31 ile birlikte sunuldu ve artık bakımı yapılmıyor. Yeni geliştirmeler için [SAM v3](/docs/api/samv3/) kullanın. v1'e göre v2'nin tek iyileştirmesi, tek bir SAM bağlantısı üzerinden çoğullanan birden çok soket desteğiydi.

## Sürüm Notları

- Raporlanan sürüm dizesi "2.0" olarak kalır.
- 0.9.14'ten beri `HELLO VERSION` mesajı tek haneli `MIN`/`MAX` değerlerini kabul eder ve `MIN` parametresi isteğe bağlıdır.
- `DEST GENERATE`, `SIGNATURE_TYPE` için destek sağlar, bu sayede Ed25519 destinations (hedefler) oluşturulabilir.

## Oturum Temelleri

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]
```
- Her hedef yalnızca bir aktif SAM oturumuna sahip olabilir (akışlar, datagramlar veya ham).
- `STYLE` sanal akışları, imzalı datagramları veya ham datagramları seçer.
- Ek seçenekler I2CP'ye iletilir (örneğin, `tunnels.quantityInbound=3`).
- Yanıtlar v1'i yansıtır: `SESSION STATUS RESULT=OK|DUPLICATED_DEST|I2P_ERROR|INVALID_KEY`.

## Mesaj Kodlaması

Boşluklarla ayrılmış `key=value` çiftlerinden oluşan satır tabanlı ASCII (değerler tırnak içine alınabilir). İletişim türleri v1 ile aynıdır:

- I2P streaming library üzerinden akışlar
- Yanıtlanabilir datagramlar (`PROTO_DATAGRAM`)
- Ham datagramlar (`PROTO_DATAGRAM_RAW`)

## Ne Zaman Kullanılır

Yalnızca geçiş yapamayan eski istemciler için. SAM v3 şunları sunar:

- İkili hedef devri (`DEST GENERATE BASE64`)
- Alt oturumlar ve DHT desteği (v3.3)
- Daha iyi hata raporlaması ve seçenek müzakeresi

Bkz.:

- [SAM v1](/docs/legacy/sam/)
- [SAM v3](/docs/api/samv3/)
- [Datagram API'si](/docs/api/datagrams/)
- [Akış Protokolü](/docs/specs/streaming/)
