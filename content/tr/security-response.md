---
title: "Zafiyet Yanıt Süreci"
description: "I2P'nin güvenlik açığı bildirim ve yanıt süreci"
layout: "guvenlik-yaniti"
aliases:
  - /en/research/vrp
---

<div id="contact"></div>

## Bir Güvenlik Açığı Bildirin

Bir güvenlik sorunu mu keşfettiniz? Bunu **security@i2p.net** adresine bildirin (PGP teşvik edilir)

<a href="/keys/i2p-security-public.asc" download class="pgp-key-btn">PGP Anahtarını İndir</a> | GPG Anahtarı parmak izi: `40DF FE20 7D79 9BEC 3AE8 7DEA 5F98 BE91 176E 1941`

<div id="guidelines"></div>

## Araştırma Rehberleri

**Lütfen ŞUNLARI YAPMAYIN:**
- Canlı I2P ağına saldırı yapmayın
- Sosyal mühendislik veya I2P altyapısına saldırı düzenlemeyin
- Diğer kullanıcılar için hizmetlerin kesilmesine neden olmayın

**Lütfen ŞUNLARI YAPIN:**
- Mümkünse izole test ağları kullanın
- Koordineli ifşa uygulamalarını takip edin
- Canlı ağ testlerinden önce bizimle iletişime geçin

<div id="process"></div>

## Yanıt Süreci

### 1. Bildirim Alındı
- **3 iş günü** içinde yanıt
- Yanıt Yöneticisi atanır
- Ciddiyet sınıflandırması (YÜKSEK/ORTA/DÜŞÜK)

### 2. Araştırma ve Geliştirme
- Şifreli kanallar üzerinden özel yama geliştirilmesi
- İzole ağda testler
- **YÜKSEK ciddiyet:** 3 gün içinde kamuya bildirim (hiçbir istismar detayı olmadan)

### 3. Yayınlama ve İfşa
- Güvenlik güncellemesi dağıtılır
- Tam ifşaya kadar maksimum **90 gün** zaman çizelgesi
- Duyurularda isteğe bağlı olarak araştırmacı kredisi

### Ciddiyet Seviyeleri

**YÜKSEK** - Tüm ağ üzerinde etkisi var, hemen müdahale gerekiyor
**ORTA** - Bireysel yönlendiriciler, hedefli istismar
**DÜŞÜK** - Sınırlı etki, teorik senaryolar

<div id="communication"></div>

## Güvenli İletişim

Tüm güvenlik bildirimleri için PGP/GPG şifrelemesi kullanın:

```
Parmak izi: 40DF FE20 7D79 9BEC 3AE8 7DEA 5F98 BE91 176E 1941
```

Raporunuzda dahil edin:
- Ayrıntılı teknik açıklama
- Yeniden üretme adımları
- Kanıt kavram kodu (varsa)

<div id="timeline"></div>

## Zaman Çizelgesi

| Aşama | Zaman Dilimi |
|-------|--------------|
| İlk Yanıt | 0-3 gün |
| Araştırma | 1-2 hafta |
| Geliştirme ve Test | 2-6 hafta |
| Yayınlama | 6-12 hafta |
| Tam İfşa | Maksimum 90 gün |

<div id="faq"></div>

## SSS

**Bildirdiğim için başım belaya girer mi?**
Hayır. Sorumlu ifşa takdir edilmekte ve korunmaktadır.

**Canlı ağda test yapabilir miyim?**
Hayır. Yalnızca izole test ağlarını kullanın.

**Anonim kalabilir miyim?**
Evet, ancak bu iletişimi zorlaştırabilir.

**Bir ödül programınız var mı?**
Şu anda yok. I2P, gönüllü çalışmalarla yürütülüyor ve sınırlı kaynaklara sahip.

<div id="examples"></div>

## Neyi Bildirmelisiniz

**Kapsam Dahilinde:**
- I2P yönlendirici zafiyetleri
- Protokol veya kriptografi kusurları
- Ağ düzeyinde saldırılar
- Anonimlik bozma teknikleri
- Hizmet reddi sorunları

**Kapsam Dışında:**
- Üçüncü taraf uygulamalar (geliştiricilerle iletişime geçin)
- Sosyal mühendislik veya fiziksel saldırılar
- Bilinen/açıklanmış zafiyetler
- Tamamen teorik sorunlar

---

**I2P'yi güvende tutmaya yardımcı olduğunuz için teşekkür ederiz!**