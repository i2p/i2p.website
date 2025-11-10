---
title: "ElGamal/AES+SessionTags için Sıfırlama Mesajı"
number: "124"
author: "orignal"
created: "2016-01-24"
lastupdated: "2016-01-26"
status: "Açık"
thread: "http://zzz.i2p/topics/2056"
---

## Genel Bakış

Bu öneri, iki Hedef arasında oturum etiketlerini sıfırlamak için kullanılabilecek bir I2NP mesajı içindir.

## Motivasyon

Bir hedefin başka bir hedefe ait bir sürü onaylanmış etiketi olduğunu hayal edin. Ancak, bu hedef yeniden başlatıldı veya bu etiketleri başka bir şekilde kaybetti. İlk hedef, etiketlerle mesaj göndermeye devam eder ve ikinci hedef şifreyi çözemiyor. İkinci hedefin, tıpkı güncellenmiş LeaseSet gönderdiği gibi, ilk hedefe sıfırlama (yeniden başlama) yapması gerektiğini söylemenin bir yolu olmalıdır.

## Tasarım

### Önerilen Mesaj

Bu yeni karanfil, "destination" (hedef) türünde bir teslimat türü içermeli ve göndericinin ident hash'ini içeren yeni bir I2NP mesajı olarak "Etiketler sıfırlama" şeklinde adlandırılmalıdır. Zaman damgası ve imza içermelidir.

Bir hedefin mesajları çözememesi durumunda herhangi bir zamanda gönderilebilir.

### Kullanım

Eğer yönlendiricimi yeniden başlatır ve başka bir hedefe bağlanmaya çalışırsam, yeni LeaseSet'im ile bir karanfil gönderirim ve adresimi içeren bu mesajla birlikte ek bir karanfil gönderirim. Uzak hedef bu mesajı aldığında, bana giden tüm etiketleri siler ve ElGamal'dan yeniden başlar.

Genellikle bir hedefin yalnızca bir uzak hedefle iletişim halinde olduğu bir durum yaygındır. Yeniden başlatma durumunda, bu mesajı ilk akış veya datagram mesajıyla birlikte herkese göndermelidir.
