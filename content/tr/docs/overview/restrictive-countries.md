---
title: "Katı/Kısıtlayıcı Ülkeler"
description: "I2P'nin yönlendirme veya anonimlik araçlarına kısıtlama getiren yetki alanlarında nasıl davrandığı (Gizli Mod ve katı liste)"
slug: "restrictive-countries"
lastUpdated: "2024-07"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

I2P'nin bu uygulaması (bu sitede dağıtılan Java uygulaması), başkaları için yönlendirmeye katılımın yasalarla kısıtlanmış olabileceği bölgelerde router davranışını ayarlamak için kullanılan bir "Katı Ülkeler Listesi" içerir. I2P kullanımını yasaklayan yargı bölgeleri bilmiyoruz ancak birçoğu trafik aktarımı üzerinde geniş yasaklamalara sahiptir. "Katı" ülkelerde olduğu görünen router'lar otomatik olarak Gizli moda alınır.

Proje bu kararları verirken sivil ve dijital haklar örgütlerinin araştırmalarına atıfta bulunur. Özellikle Freedom House tarafından yürütülen devam eden araştırmalar seçimlerimizi bilgilendirir. Genel yönerge, Sivil Özgürlükler (CL) puanı 16 veya daha düşük olan veya İnternet Özgürlüğü puanı 39 veya daha düşük (özgür değil) olan ülkeleri dahil etmektir.

## Gizli Mod Özeti

Bir router Gizli moda alındığında, davranışı hakkında üç önemli şey değişir:

- netDb'ye bir RouterInfo yayınlamaz.
- Katılımcı tünelleri kabul etmez.
- Aynı ülkedeki router'lara doğrudan bağlantıları reddeder.

Bu savunmalar, yönlendiricilerin güvenilir bir şekilde listelenmesini zorlaştırır ve başkaları için trafik aktarma konusundaki yerel yasakların ihlal edilme riskini azaltır.

## Katı Ülkeler Listesi (2024 itibariyle)

```
/* Afghanistan */ "AF",
/* Azerbaijan */ "AZ",
/* Bahrain */ "BH",
/* Belarus */ "BY",
/* Brunei */ "BN",
/* Burundi */ "BI",
/* Cameroon */ "CM",
/* Central African Republic */ "CF",
/* Chad */ "TD",
/* China */ "CN",
/* Cuba */ "CU",
/* Democratic Republic of the Congo */ "CD",
/* Egypt */ "EG",
/* Equatorial Guinea */ "GQ",
/* Eritrea */ "ER",
/* Ethiopia */ "ET",
/* Iran */ "IR",
/* Iraq */ "IQ",
/* Kazakhstan */ "KZ",
/* Laos */ "LA",
/* Libya */ "LY",
/* Myanmar */ "MM",
/* North Korea */ "KP",
/* Palestinian Territories */ "PS",
/* Pakistan */ "PK",
/* Rwanda */ "RW",
/* Saudi Arabia */ "SA",
/* Somalia */ "SO",
/* South Sudan */ "SS",
/* Sudan */ "SD",
/* Eswatini (Swaziland) */ "SZ",
/* Syria */ "SY",
/* Tajikistan */ "TJ",
/* Thailand */ "TH",
/* Turkey */ "TR",
/* Turkmenistan */ "TM",
/* Venezuela */ "VE",
/* United Arab Emirates */ "AE",
/* Uzbekistan */ "UZ",
/* Vietnam */ "VN",
/* Western Sahara */ "EH",
/* Yemen */ "YE"
```
Bir ülkenin katı listeye eklenmesi veya listeden çıkarılması gerektiğini düşünüyorsanız, lütfen bir issue açın: https://i2pgit.org/i2p/i2p.i2p/

Referans: Freedom House – https://freedomhouse.org/
