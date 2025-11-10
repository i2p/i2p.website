---
title: "PT Taşıma"
number: "109"
author: "zzz"
created: "2014-01-09"
lastupdated: "2014-09-28"
status: "Açık"
thread: "http://zzz.i2p/topics/1551"
---

## Genel Bakış

Bu öneri, diğer yönlendiricilere Takılabilir Taşıma üzerinden bağlanan bir I2P taşıma sistemi oluşturmayı amaçlamaktadır.

## Motivasyon

Takılabilir Taşıma (PT'ler), Tor köprülerine modüler bir şekilde örtmece taşıma eklemek için Tor tarafından geliştirilmiştir.

I2P zaten alternatif taşıma sistemleri ekleme engelini azaltan modüler bir taşıma sistemine sahiptir. PT'leri desteklemek, I2P'nin alternatif protokolleri denemek ve engelleme direncine hazır hale gelmek için kolay bir yol sağlayacaktır.

## Tasarım

Uygulamanın birkaç olası katmanı vardır:

1. SOCKS ve ExtORPort'u uygulayan, giriş ve çıkış süreçlerini yapılandırıp fork eden ve iletişim sistemi ile kaydolan bir genel PT. Bu katman, NTCP hakkında hiçbir şey bilmez ve NTCP kullanabilir veya kullanmayabilir. Test için iyidir.

2. 1) üzerine inşa edilen bir genel NTCP PT, NTCP kodu üzerinde inşa edilir ve 1)'e NTCP yönlendirir.

3. 2) üzerine inşa edilen, belirli bir harici giriş ve çıkış süreci çalıştıracak şekilde yapılandırılmış spesifik bir NTCP-xxxx PT.
