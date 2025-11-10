---
title: "'Şifreli' Akış Bayrağı"
number: "114"
author: "orignal"
created: "2015-01-21"
lastupdated: "2015-01-21"
status: "Araştırma Gerekiyor"
thread: "http://zzz.i2p/topics/1795"
---

## Genel Bakış

Bu öneri, kullanılan uçtan uca şifreleme türünü belirten bir bayrağın akışa eklenmesiyle ilgilidir.

## Motivasyon

Yüksek yüke sahip uygulamalar, ElGamal/AES+OturumEtiketleri etiketlerinin yetersizliği ile karşılaşabilir.

## Tasarım

Akış protokolü içinde bir yere yeni bir bayrak ekleyin. Eğer bir paket bu bayrakla gelirse, yükün özel anahtar ve eşin açık anahtarı ile AES şifrelenmiş olduğunu ifade eder. Bu, garlic (ElGamal/AES) şifrelemesini ortadan kaldırmayı ve etiketlerin yetersizliği sorununu çözmeyi sağlayacaktır.

Her paket için veya SYN üzerinden her akış için ayarlanabilir.
