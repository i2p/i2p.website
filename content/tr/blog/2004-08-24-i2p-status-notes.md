---
title: "2004-08-24 tarihli I2P Durum Notları"
date: 2004-08-24
author: "jr"
description: "0.3.4.3 sürümü, yeni router konsolu özellikleri, 0.4 ilerlemesi ve çeşitli iyileştirmeleri kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Herkese merhaba, bugün birçok güncelleme var

## Dizin

1. 0.3.4.3 status
   1.1) timestamper
   1.2) new router console authentication
2. 0.4 status
   2.1) service & systray integration
   2.2) jbigi & jcpuid
   2.3) i2paddresshelper
3. AMOC vs. restricted routes
4. stasher
5. pages of note
6. ???

## 1) 0.3.4.3 durumu

0.3.4.3 sürümü geçen Cuma yayımlandı ve o zamandan beri işler oldukça iyi gidiyor. Yeni eklenen bazı tunnel testleri ve eş seçimi koduyla ilgili bazı sorunlar oldu, ancak sürümden sonra yapılan bazı ince ayarların ardından oldukça sağlam. IRC sunucusunun henüz yeni revizyona geçip geçmediğini bilmiyorum, bu yüzden genellikle eepsites (I2P Sites) ve http outproxies (çıkış vekil sunucuları) ile test yapmak zorunda kalıyoruz (squid.i2p ve www1.squid.i2p). 0.3.4.3 sürümündeki büyük (>5MB) dosya aktarımları hâlâ yeterince güvenilir değil, ancak kendi testlerimde, o zamandan beri yapılan değişiklikler işleri daha da iyileştirdi.

Ağ da büyüyor - bugün erken saatlerde eşzamanlı 45 kullanıcıya ulaştık ve birkaç gündür tutarlı biçimde 38-44 kullanıcı aralığındayız (w00t)! Şimdilik bu sağlıklı bir sayı ve riskleri gözlemek için genel ağ etkinliğini izliyorum. 0.4 sürümüne geçerken, kullanıcı tabanını kademeli olarak yaklaşık 100 router (yönlendirici) seviyesine kadar artırmak ve daha fazla büyümeden önce biraz daha test etmek isteyeceğiz. En azından, geliştirici bakış açısından benim hedefim bu.

### 1.1) timestamper

0.3.4.3 sürümüyle değişen ve bahsetmeyi tamamen unuttuğum gerçekten harika şeylerden biri, SNTP kodunda bir güncellemeydi. SNTP kodunu BSD lisansı altında yayınlamayı kabul eden Adam Buckley’nin cömertliği sayesinde, eski Timestamper uygulamasını I2P SDK’nin çekirdeğine dahil ettik ve saatimizle tamamen entegre ettik. Bu üç şey anlamına geliyor: 1. timestamper.jar dosyasını silebilirsiniz (kod artık i2p.jar içinde) 2. yapılandırmanızdaki ilgili clientApp satırlarını kaldırabilirsiniz 3. yeni zaman eşitleme seçeneklerini kullanmak için yapılandırmanızı güncelleyebilirsiniz

router.config içindeki yeni seçenekler basit ve varsayılan değerler yeterli olacaktır (özellikle de çoğunuzun onları farkında olmadan kullandığını düşünürsek :)

Sorgulanacak SNTP sunucuları listesini ayarlamak için:

```
time.sntpServerList=pool.ntp.org,pool.ntp.org,pool.ntp.org
```
Zaman senkronizasyonunu devre dışı bırakmak için (yalnızca bir NTP gurusuysanız ve işletim sisteminizin saatinin *her zaman* doğru olduğunu biliyorsanız - "windows time" çalıştırmak YETERLİ değildir):

```
time.disabled=true
```
Artık bir 'timestamper password' sahibi olmanıza gerek yok, çünkü her şey doğrudan koda entegre edildi (ah, BSD ile GPL'in güzellikleri :).

### 1.2) new router console authentication

Bu yalnızca yeni router konsolunu çalıştıranlar için geçerlidir; ancak onu herkese açık bir arayüzde dinlemeye ayarladıysanız, tümleşik temel HTTP kimlik doğrulamasından yararlanmak isteyebilirsiniz. Evet, temel HTTP kimlik doğrulaması saçma derecede zayıftır - ağınızı dinleyen ya da kaba kuvvetle içeri girmeye çalışanlara karşı koruma sağlamaz, ancak rastgele sızmaya çalışanları dışarıda tutar. Her neyse, bunu kullanmak için yalnızca şu satırı ekleyin

```
consolePassword=blah
```
router.config dosyanıza. Ne yazık ki, bu parametre Jetty'ye yalnızca bir kez (başlangıç sırasında) aktarıldığı için router'ı yeniden başlatmanız gerekecek.

## 2) 0.4 status

0.4 sürümü üzerinde ciddi ilerleme kaydediyoruz ve önümüzdeki hafta bazı ön sürümleri yayınlamayı umuyoruz. Yine de hâlâ bazı ayrıntıları netleştiriyoruz, bu yüzden henüz sağlam bir yükseltme süreci oluşturmadık. Yayın geriye dönük uyumlu olacak, dolayısıyla güncelleme çok sancılı olmamalı. Her neyse, gelişmeleri takipte kalın; her şey hazır olduğunda haberdar olacaksınız.

### 1.1) zaman damgalayıcı

Hypercubus, yükleyicinin, bir sistem tepsisi uygulamasının ve bazı hizmet yönetimi kodunun entegrasyonunda büyük ilerleme kaydediyor. Temelde, 0.4 sürümü için tüm Windows kullanıcılarının otomatik olarak küçük bir sistem tepsisi simgesi (Iggy!) olacak; bunu web konsolu üzerinden devre dışı bırakabilecekler (ve/veya yeniden etkinleştirebilecekler). Buna ek olarak, JavaService wrapper'ını da paketleyeceğiz; bu da bize I2P'yi sistem önyüklemesinde (ya da değil) çalıştırma, bazı koşullarda otomatik yeniden başlatma, istek üzerine JVM'i tamamen yeniden başlatma, stack trace'ler (çağrı yığını izleri) üretme ve daha birçok yararlı özellik gibi olanaklar sağlayacak.

### 1.2) yeni router konsolu kimlik doğrulaması

0.4 sürümündeki büyük güncellemelerden biri, jbigi kodunun elden geçirilmesi olacak; Iakin'in Freenet için yaptığı değişiklikler ile Iakin'in yeni "jcpuid" native library (yerel kütüphane) birleştirilecek. jcpuid kütüphanesi yalnızca x86 mimarilerinde çalışır ve bazı yeni jbigi kodlarıyla birlikte, yüklenecek 'doğru' jbigi'yi belirleyecektir. Bu nedenle, herkesin sahip olacağı tek bir jbigi.jar dağıtacağız ve mevcut makine için 'doğru' olanı bunun içinden seçeceğiz. Elbette insanlar hâlâ kendi native jbigi'lerini derleyerek jcpuid'in istediğini geçersiz kılabilecekler (sadece derleyin ve I2P kurulum dizininize kopyalayın, ya da adını "jbigi" koyup classpath'inizdeki bir .jar dosyasına yerleştirin). Ancak, güncellemeler nedeniyle, geriye dönük uyumlu *değil* - yükseltme yaparken, ya kendi jbigi'nizi yeniden derlemeli ya da mevcut native library'nizi kaldırmalısınız (yeni jcpuid kodunun doğru olanı seçmesine izin vermek için).

### 2.3) i2paddresshelper

oOo, insanların hosts.txt dosyalarını güncellemeden eepsites(I2P Sites) gezmesine olanak tanıyan gerçekten havalı bir yardımcı araç hazırladı. Bu, CVS'e işlendi ve bir sonraki sürümde dağıtılacak, ancak insanlar bağlantıları buna uygun şekilde güncellemeyi düşünebilir (cervantes, bunu desteklemek için forum.i2p'nin [i2p] bbcode'unu "Try it [i2p]" bağlantısıyla güncelledi).

Temelde, istediğiniz herhangi bir adla eepsite(I2P Site) için bir bağlantı oluşturursunuz, ardından destination (hedef adres) belirten özel bir url parametresi eklersiniz:

```
http://wowthisiscool.i2p/?i2paddresshelper=FpCkYW5pw...
```
Arka planda, oldukça güvenli - başka bir adresi sahteleyemezsiniz ve ad hosts.txt içinde kalıcı olarak yazılmış *değil*, ancak eepsite'lerde (I2P Sites) bağlantısı verilen, eski `http://i2p/base64/` numarasıyla göremeyeceğiniz görselleri / vb. görmenize izin verir. Eğer o siteye ulaşmak için her zaman "wowthisiscool.i2p" kullanmak istiyorsanız, elbette yine de hosts.txt dosyasına girişi eklemeniz gerekecek (MyI2P address book yayınlanana kadar, yani ;)

## 3) AMOC vs. restricted routes

Mule bazı fikirleri bir araya getiriyor ve bazı şeyleri açıklamam için beni dürtüklüyor; bu süreçte de, AMOC fikrinin tamamını yeniden değerlendirmeme yardımcı olacak şekilde bir miktar ilerleme sağladı. Özellikle, taşıma katmanımıza koyduğum kısıtlamalardan birini kaldırırsak - bu da çift yönlülüğü varsaymamıza izin verir - tüm AMOC taşımayı çöpe atabilir, bunun yerine bazı temel kısıtlı rota işletimini uygulayabiliriz (güvenilir eşler ve çok sıçramalı router tunnels gibi daha gelişmiş kısıtlı rota tekniklerinin temellerini de sonraya bırakarak).

Bu yolu seçersek, bu, insanların güvenlik duvarlarının, NAT'lerin vb. arkasında herhangi bir yapılandırma gerektirmeden ağa katılabilecekleri ve ayrıca kısıtlı rota anonimliği özelliklerinden bazılarını sunabileceğimiz anlamına gelirdi. Buna karşılık, büyük olasılıkla yol haritamızda kapsamlı bir revizyona yol açardı, ancak bunu güvenli bir şekilde yapabilirsek, bize çok fazla zaman kazandırırdı ve değişikliğe fazlasıyla değerdi.

Ancak, acele etmek istemiyoruz ve o yola girmeden önce anonimlik ve güvenlik açısından doğuracağı sonuçları dikkatle gözden geçirmemiz gerekecek. Bunu 0.4 yayımlandıktan ve sorunsuz bir şekilde ilerlemeye başladıktan sonra yapacağız, dolayısıyla aceleye gerek yok.

## 2) 0.4 durumu

Söylentilere göre aum iyi ilerleme kaydediyor - güncelleme vermek için toplantıda olup olmayacağını bilmiyorum, ama bu sabah #i2p'de bize kısa bir mesaj bıraktı:

```
<aum> hi all, can't talk long, just a quick stasher update - work is
      continuing on implementing freenet keytypes, and freenet FCP
      compatibility - work in progress, should have a test build
      ready to try out by the end of the week
```
Yaşasın.

## 5) pages of note

I2P kullanıcılarının göz atmak isteyebileceği iki yeni kaynağa dikkat çekmek istiyorum - DrWoo, anonim olarak gezinmek isteyenler için çok sayıda bilgi içeren bir sayfa hazırladı ve Luckypunk, FreeBSD üzerinde bazı JVM'lerle ilgili deneyimlerini anlatan bir howto (nasıl yapılır rehberi) yayınladı. Hypercubus ayrıca henüz yayımlanmamış servis ve systray (sistem tepsisi) entegrasyonunu test etmeye yönelik belgeleri de paylaştı.

## 6) ???

Tamam, şimdilik söyleyeceklerim bu kadar - başka bir şeyi gündeme getirmek isterseniz bu akşam GMT 21:00'deki toplantıya uğrayın.

=jr
