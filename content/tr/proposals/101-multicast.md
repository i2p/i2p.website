---
title: "Çoklu Yayın"
number: "101"
author: "zzz"
created: "2008-12-08"
lastupdated: "2009-03-25"
status: "Ölü"
thread: "http://zzz.i2p/topics/172"
---

## Genel Bakış

Temel fikir: Çıkış tünelinizden bir kopya gönderin, çıkış uç noktası tüm giriş yönlendiricilerine dağıtsın. Uçtan uca şifreleme önlenmiştir.

## Tasarım

- Yeni çoklu yayın tüneli mesaj türü (teslimat türü = 0x03)
- Çıkış uç noktası çoklu yayını dağıtır
- Yeni I2NP Çoklu Yayın Mesaj türü?
- Yeni I2CP Çoklu Yayın SendMessageMessage Mesaj türü
- OutNetMessageOneShotJob içinde router-router şifreleme yapma (sarımsak?)

Uygulama:

- RTSP Proxy?

Streamr:

- MTU'yu ayarla? Yoksa sadece uygulamada mı yap?
- İsteğe bağlı alım ve iletim
