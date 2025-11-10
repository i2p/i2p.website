---
title: "2004-09-21 tarihli I2P Durum Notları"
date: 2004-09-21
author: "jr"
description: "Geliştirme ilerlemesini, TCP aktarım iyileştirmelerini ve yeni userhosts.txt özelliğini kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Selam millet, bu hafta kısa bir güncelleme

## Dizin

1. Dev status
2. New userhosts.txt vs. hosts.txt
3. ???

## 1) Geliştirme durumu

Ağ son bir hafta içinde oldukça istikrarlıydı, bu sayede zamanımı 0.4.1 sürümüne odaklayabildim - TCP taşıma altyapısını elden geçirmek, IP adreslerini algılama desteği eklemek ve o eski "target changed identities" olayını kaldırmak. Bu aynı zamanda dyndns kayıtlarına duyulan ihtiyacı da ortadan kaldırmalı.

NAT'lerin veya güvenlik duvarlarının arkasındaki kişiler için ideal bir sıfır tıklamalı kurulum olmayacak - gelen TCP bağlantılarını alabilmeleri için yine de port yönlendirme yapmaları gerekecek. Yine de hata yapmaya daha az açık olmalı. Geriye dönük uyumluluğu korumak için elimden geleni yapıyorum, ancak bu konuda hiçbir söz vermiyorum. Hazır olduğunda daha fazla haber olacak.

## 2) Yeni userhosts.txt ile hosts.txt karşılaştırması

Bir sonraki sürümde, sıkça talep edilen iki hosts.txt dosyası desteğine sahip olacağız - biri yükseltmeler sırasında (veya `http://dev.i2p.net/i2p/hosts.txt` adresinden) üzerine yazılan ve diğeri kullanıcının yerel olarak bakımını yapabileceği. Bir sonraki sürümde (veya CVS HEAD) herhangi bir kayıt için hosts.txt'den önce kontrol edilen "userhosts.txt" dosyasını düzenleyebilirsiniz - lütfen yerel değişikliklerinizi oraya yapın, çünkü güncelleme işlemi hosts.txt'nin üzerine yazacaktır (userhosts.txt'nin değil).

## 3) ???

Belirttiğim gibi, bu hafta yalnızca kısa bir not seti var. Başka gündeme getirmek istediği bir şey olan var mı? Birkaç dakika içinde toplantıya uğrayın.

=jr
