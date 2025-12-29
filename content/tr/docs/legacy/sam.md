---
title: "SAM v1"
description: "Eski Simple Anonymous Messaging (Basit Anonim Mesajlaşma) protokolü (kullanımdan kaldırılmış)"
slug: "sam"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Kullanımdan kaldırıldı:** SAM v1 yalnızca tarihsel referans amaçlı tutulmaktadır. Yeni uygulamalar [SAM v3](/docs/api/samv3/) veya [BOB](/docs/legacy/bob/) kullanmalıdır. Orijinal köprü yalnızca DSA-SHA1 hedeflerini ve sınırlı bir seçenek kümesini destekler.

## Kütüphaneler

Java I2P kaynak ağacı hâlâ C, C#, Perl ve Python için eski dil bağlayıcılarını içeriyor. Bunlar artık bakımı yapılmıyor ve çoğunlukla arşivsel uyumluluk amacıyla dağıtılıyor.

## Sürüm Müzakeresi

İstemciler TCP üzerinden (varsayılan `127.0.0.1:7656`) bağlanır ve şunları değiş tokuş eder:

```
Client → HELLO VERSION MIN=1 MAX=1
Bridge → HELLO REPLY RESULT=OK VERSION=1.0
```
Java I2P 0.9.14 itibarıyla `MIN` parametresi isteğe bağlıdır ve güncellenmiş köprülerde hem `MIN` hem de `MAX` tek haneli biçimleri (`"3"` vb.) kabul eder.

## Oturum Oluşturma

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]*
```
- `DESTINATION=name`, `sam.keys` içinde bir kayıt yükler veya oluşturur; `TRANSIENT` her zaman geçici bir Destination (hedef kimliği) oluşturur.
- `STYLE`, sanal akışları (TCP benzeri), imzalı datagramları veya ham datagramları seçer.
- `DIRECTION` yalnızca akış oturumları için geçerlidir; varsayılan olarak `BOTH`'tur.
- Ek anahtar/değer çiftleri I2CP seçenekleri olarak iletilir (örneğin, `tunnels.quantityInbound=3`).

Köprü şu şekilde yanıt verir:

```
SESSION STATUS RESULT=OK DESTINATION=name
```
Hata durumları, `DUPLICATED_DEST`, `I2P_ERROR` veya `INVALID_KEY` değerlerinden birini ve isteğe bağlı bir mesaj döndürür.

## Mesaj Formatları

SAM mesajları, anahtar/değer çiftleri boşlukla ayrılmış, tek satırlı ASCII biçimindedir. Anahtarlar UTF‑8 kodlamasındadır; değerler boşluk içeriyorsa tırnak içine alınabilir. Kaçış (escaping) tanımlı değildir.

İletişim türleri:

- **Akışlar** – I2P akış kütüphanesi aracılığıyla proxy edilir
- **Yanıtlanabilir datagramlar** – imzalı yükler (Datagram1)
- **Ham datagramlar** – imzasız yükler (Datagram RAW)

## 0.9.14'te Eklenen Seçenekler

- `DEST GENERATE` `SIGNATURE_TYPE=...` değerini kabul eder (Ed25519 vb.ne izin verir)
- `HELLO VERSION` `MIN`'i isteğe bağlı olarak değerlendirir ve tek basamaklı sürüm dizelerini kabul eder

## SAM v1 ne zaman kullanılmalı

Yalnızca güncellenemeyen eski yazılımlarla birlikte çalışabilirlik amacıyla. Tüm yeni geliştirmeler için şunu kullanın:

- [SAM v3](/docs/api/samv3/) tam özellikli akış/datagram erişimi için
- [BOB](/docs/legacy/bob/) hedef yönetimi için (hala sınırlı, ancak daha modern özellikleri destekler)

## Kaynakça

- [SAM v2](/docs/legacy/samv2/)
- [SAM v3](/docs/api/samv3/)
- [Datagram Belirtimi](/docs/api/datagrams/)
- [Akış Protokolü](/docs/specs/streaming/)

SAM v1, router'dan bağımsız uygulama geliştirme için temeli attı, ancak ekosistem ilerledi. Bu belgeyi bir başlangıç noktası olarak değil, uyumluluğa yönelik bir yardımcı kaynak olarak değerlendirin.
