---
title: "LeaseSet Anahtar Kalıcılığı"
number: "113"
author: "zzz"
created: "2014-12-13"
lastupdated: "2016-12-02"
status: "Kapalı"
thread: "http://zzz.i2p/topics/1770"
target: "0.9.18"
implementedin: "0.9.18"
---

## Genel Bakış

Bu öneri, şu anda geçici olan LeaseSet'te ek verilerin kalıcı hale getirilmesiyle ilgilidir.
0.9.18'de uygulanmıştır.

## Motivasyon

0.9.17 sürümünde netDb dilimleme anahtarı için kalıcılık eklendi, i2ptunnel.config içinde saklanır. Bu, aynı dilimi yeniden başlatmadan sonra koruyarak bazı saldırıları önlemeye yardımcı olur ve ayrıca bir yönlendirici yeniden başlatma ile olası ilişkilendirmeleri önler.

Yönlendiricinin yeniden başlatılmasıyla ilişkilendirilmesi daha da kolay olan iki başka şey daha vardır: leaseset şifreleme ve imzalama anahtarları. Bu anahtarlar şu anda kalıcı değildir.

## Önerilen Değişiklikler

Özel anahtarlar, i2ptunnel.config dosyasında i2cp.leaseSetPrivateKey ve i2cp.leaseSetSigningPrivateKey olarak saklanır.
