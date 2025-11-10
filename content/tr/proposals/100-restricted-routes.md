---
title: "Kısıtlı Rotalar"
number: "100"
author: "zzz"
created: "2008-09-14"
lastupdated: "2008-10-13"
status: "Rezerve"
thread: "http://zzz.i2p/topics/114"
---

## Giriş


## Düşünceler

- RouterAddress yapısında bir leaseSet karma yayımlayan yeni bir "IND" (dolaylı) taşıma modu ekleyin: "IND: [key=aababababababababb]". Bu taşıma modu, hedef yönlendirici yayımladığında en düşük öncelikte teklif verir. Bu taşıma aracılığıyla bir arkadaşınıza mesaj göndermek için, lease’i doğrudan ff eşinden alarak lease'e doğrudan gönderin.

- IND’yi ilan eden bir eş, başka bir arkadaşa bir dizi tünel oluşturmalı ve bunları sürdürmelidir. Bunlar keşif tünelleri ya da istemci tünelleri değildir, aksine ikinci bir dizi yönlendirici tünelleridir.

  - 1-hop yeterli mi?
  - Bu tüneller için eşler nasıl seçilecek?
  - "Sınırsız" olmaları gerekiyor ama bunu nasıl bilebilirsiniz? Ulaşılabilirlik
    haritalaması? Grafik teorisi, algoritmalar, veri yapıları burada yardımcı olabilir. Bunun hakkında okumak gerekiyor. Tünel TODO kısmına bakın.

- Eğer IND tünelleriniz varsa, IND taşıma modunuz bu tüneller üzerinden mesaj göndermek için (düşük öncelikli) teklif vermelidir.

- Dolaylı tünel kurulumunu etkinleştirmeye nasıl karar verilir?

- Kapsamı kaybetmeden nasıl uygulanır ve test edilir?
