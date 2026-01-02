---
title: "SSU Taşıması (Kullanımdan kaldırıldı)"
description: "SSU2'den önce kullanılan ilk UDP taşıma protokolü"
slug: "ssu"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
type: docs
reviewStatus: "needs-review"
---

> **Kullanımdan kaldırıldı:** SSU (Güvenli Yarı-Güvenilir UDP) [SSU2](/docs/specs/ssu2/)'nin yerini aldı. Java I2P, SSU'yu 2.4.0 sürümünde (API 0.9.61) kaldırdı ve i2pd ise onu 2.44.0'da (API 0.9.56) kaldırdı. Bu belge yalnızca tarihsel referans amacıyla saklanmaktadır.

## Öne çıkanlar

- I2NP iletilerinin şifreli, kimliği doğrulanmış nokta-nokta teslimini sağlayan UDP tabanlı taşıma.
- 2048 bitlik Diffie–Hellman el sıkışmasına dayanıyordu (ElGamal ile aynı asal sayı).
- Her datagram, 16 baytlık HMAC-MD5 (standart dışı kısaltılmış varyant) + 16 baytlık IV (başlatma vektörü) ve ardından AES-256-CBC ile şifrelenmiş yük taşıyordu.
- Yeniden oynatma önleme ve oturum durumu, şifrelenmiş yük içinde izleniyordu.

## İleti Üstbilgisi

```
[16-byte MAC][16-byte IV][encrypted payload]
```
Kullanılan MAC hesaplaması: `HMAC-MD5(ciphertext || IV || (len ^ version ^ ((netid-2)<<8)))`. 32 baytlık bir MAC anahtarı kullanıldı. payload (veri yükü) uzunluğu, MAC hesaplamasına eklenen big-endian 16 bitlik bir değerdi. Protokol sürümü varsayılan olarak `0` idi; netId varsayılan olarak `2` idi (ana ağ).

## Oturum ve MAC Anahtarları

DH paylaşılan sırrından türetilen:

1. Paylaşılan değeri big-endian (yüksek anlamlı bayt önce) bir bayt dizisine dönüştürün (yüksek bit ayarlıysa başına `0x00` ekleyin).
2. Oturum anahtarı: ilk 32 bayt (daha kısaysa sıfırlarla doldurun).
3. MAC anahtarı: 33–64. baytlar; yetersizse, paylaşılan değerin SHA-256 özetini kullanın.

## Durum

Router'lar artık SSU adreslerini duyurmuyor. İstemciler SSU2 veya NTCP2 taşıma protokollerine geçmelidir. Tarihsel gerçeklemeler eski sürümlerde bulunabilir:

- `router/transport/udp` altında 2.4.0'dan önceki Java kaynak kodları
- 2.44.0'dan önceki i2pd kaynak kodları

Güncel UDP taşıma davranışı için [SSU2 belirtimine](/docs/specs/ssu2/) bakın.
