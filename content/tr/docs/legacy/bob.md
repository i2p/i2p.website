---
title: "BOB - Temel Açık Köprü"
description: "Hedef yönetimi için kullanımdan kaldırılmış API"
slug: "bob"
aliases:
  - "/tr/docs/api/bob"
  - "/tr/docs/api/bob/"
  - "/tr/bob"
  - "/tr/bob/"
lastUpdated: "2025-05"
accurateFor: "0.9.8"
---

## Uyarı - Kullanımdan Kaldırıldı

Yeni uygulamalar tarafından kullanılmak için değil. Burada belirtildiği gibi BOB, yalnızca DSA-SHA1 imza türünü destekler. BOB, yeni imza türlerini veya diğer gelişmiş özellikleri destekleyecek şekilde genişletilmeyecektir. Yeni uygulamalar [SAMv3](/docs/api/samv3) kullanmalıdır.

BOB desteği, 1.7.0 sürümü (2022-02) itibarıyla Java I2P yeni kurulumlarından kaldırıldı. 1.6.1 veya daha önceki sürüm olarak kurulmuş Java I2P'de güncellemelerden sonra bile çalışmaya devam edecektir, ancak desteklenmemektedir ve herhangi bir zamanda bozulabilir. BOB, 2025-05 itibarıyla i2pd tarafından hâlâ desteklenmektedir, ancak yukarıdaki nedenlerle uygulamalar yine de SAMv3'e geçiş yapmalıdır. Burada belgelenen API'ye i2pd tarafından desteklenen herhangi bir uzantı için [i2pd belgelerine](https://i2pd.readthedocs.io/en/latest/devs/i2pd-specifics/) bakınız.

Bu noktada, BOB'tan gelen iyi fikirlerin çoğu SAMv3'e dahil edilmiştir ve SAMv3 daha fazla özellik ve gerçek dünya kullanımına sahiptir. BOB bazı kurulumlarda hala çalışabilir (yukarıya bakınız), ancak SAMv3'te bulunan gelişmiş özellikleri kazanmamaktadır ve i2pd dışında temelde desteklenmemektedir.

## BOB API için Dil Kütüphaneleri

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python - i2py-bob (git.repo.i2p)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## Genel Bakış

`KEYS` = anahtar çifti public+private, bunlar BASE64 formatındadır

`KEY` = açık anahtar, ayrıca BASE64

`ERROR` adından da anlaşılacağı gibi `"ERROR "+DESCRIPTION+"\n"` mesajını döndürür, burada `DESCRIPTION` neyin yanlış gittiğini belirtir.

`OK` `"OK"` döndürür ve eğer veri döndürülecekse, aynı satırda yer alır. `OK` komutun tamamlandığı anlamına gelir.

`DATA` satırları talep ettiğiniz bilgileri içerir. Her istek için birden fazla `DATA` satırı olabilir.

**NOT:** Help komutu, kurallara istisna olan TEK komuttur... aslında hiçbir şey döndürmeyebilir! Bu kasıtlıdır, çünkü help bir İNSAN komutu olup UYGULAMA komutu değildir.

## Bağlantı ve Sürüm

Tüm BOB durum çıktısı satırlar halindedir. Satırlar sisteme bağlı olarak \\n veya \\r\\n ile sonlandırılabilir. Bağlantı kurulduğunda, BOB iki satır çıktı verir:

```
BOB version
OK
```
Mevcut sürüm: 00.00.10

Önceki sürümlerin büyük harf onaltılık rakamlar kullandığını ve I2P sürüm standartlarına uymadığını unutmayın. Sonraki sürümlerin yalnızca 0-9 rakamlarını kullanması önerilir.

### Sürüm Geçmişi

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">I2P Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">current version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 - 00.00.0F</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&nbsp;</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">development versions</td>
    </tr>
  </tbody>
</table>
## Komutlar

**LÜTFEN DİKKAT:** Komutlarla ilgili GÜNCEL ayrıntılar için LÜTFEN yerleşik yardım komutunu kullanın. Sadece localhost 2827'ye telnet bağlantısı yapın ve help yazın, böylece her komut için tam dokümantasyon alabilirsiniz.

Komutlar hiçbir zaman eski hale getirilmez veya değiştirilmez, ancak zaman zaman yeni komutlar eklenir.

```
COMMAND     OPERAND                             RETURNS
help        (optional command to get help on)   NOTHING or OK and description of the command
clear                                           ERROR or OK
getdest                                         ERROR or OK and KEY
getkeys                                         ERROR or OK and KEYS
getnick     tunnelname                          ERROR or OK
inhost      hostname or IP address              ERROR or OK
inport      port number                         ERROR or OK
list                                            ERROR or DATA lines and final OK
lookup      hostname                            ERROR or OK and KEY
newkeys                                         ERROR or OK and KEY
option      key1=value1 key2=value2...          ERROR or OK
outhost     hostname or IP address              ERROR or OK
outport     port number                         ERROR or OK
quiet                                           ERROR or OK
quit                                            OK and terminates the command connection
setkeys     KEYS                                ERROR or OK and KEY
setnick     tunnel nickname                     ERROR or OK
show                                            ERROR or OK and information
showprops                                       ERROR or OK and information
start                                           ERROR or OK
status      tunnel nickname                     ERROR or OK and information
stop                                            ERROR or OK
verify      KEY                                 ERROR or OK
visit                                           OK, and dumps BOB's threads to the wrapper.log
zap                                             nothing, quits BOB
```
Kurulum tamamlandığında, tüm TCP soketleri gerektiğinde bloklanabilir ve bloklanacaktır, ve komut kanalına/kanalından ek mesajlara gerek kalmayacaktır. Bu, router'ın akışı tempolu bir şekilde yönetmesine olanak tanır ve SAM'in yaptığı gibi OOM ile patlamaz - SAM bir soketten birçok akışı içeri veya dışarı sokmaya çalışırken boğulur -- bu, çok sayıda bağlantınız olduğunda ölçeklenemez!

Bu özel arayüzün güzel yanı, onunla etkileşim kurmak için herhangi bir şey yazmanın SAM'den çok çok daha kolay olmasıdır. Kurulumdan sonra yapılacak başka bir işlem yoktur. Konfigürasyonu o kadar basittir ki, nc (netcat) gibi çok basit araçlar bile bazı uygulamalara yönlendirme yapmak için kullanılabilir. Buradaki değer, bir uygulama için açılış ve kapanış zamanlarını programlayabilmeniz ve bunu yapmak için uygulamayı değiştirmeniz veya hatta o uygulamayı durdurmanız gerekmemesidir. Bunun yerine, hedefi tam anlamıyla "fişten çekebilir" ve tekrar "takabilirsiniz". Bridge'i açarken aynı IP/port adresleri ve hedef anahtarları kullanıldığı sürece, normal TCP uygulaması umursamayacak ve fark etmeyecektir. Basitçe aldatılacaktır -- hedefler erişilebilir değildir ve hiçbir şey gelmemektedir.

## Örnekler

Aşağıdaki örnek için, iki hedefli çok basit bir yerel loopback bağlantısı kuracağız. "mouth" hedefi, INET superserver daemon'ındaki CHARGEN servisi olacak. "ear" hedefi ise telnet ile bağlanabileceğiniz yerel bir port olacak ve güzel ASCII test çıktılarını izleyebileceksiniz.

### Örnek Oturum Diyalogu

Basit telnet 127.0.0.1 2827 çalışır.

- A = Uygulama
- C = BOB'un Komut yanıtı.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick mouth
C       A       OK Nickname set to mouth
A       C       newkeys
C       A       OK ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
```
**YUKARIDAKI HEDEF ANAHTARINI NOT EDİN, SİZİNKİ FARKLI OLACAK!**

```
FROM    TO      DIALOGUE
A       C       outhost 127.0.0.1
C       A       OK outhost set
A       C       outport 19
C       A       OK outbound port set
A       C       start
C       A       OK tunnel starting
```
Bu noktada herhangi bir hata yoktu, "mouth" takma adıyla bir destination kuruldu. Sağlanan destination ile iletişime geçtiğinizde, aslında `19/TCP` üzerindeki `CHARGEN` servisine bağlanıyorsunuz.

Şimdi diğer yarısı için, böylece bu hedefe gerçekten ulaşabilelim.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick ear
C       A       OK Nickname set to ear
A       C       newkeys
C       A       OK 8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg~3eXtL-7S-qU-wdP-6VF~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J~flAvF4wrbF-LfVpMdg~tjtns6fA~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f~dzoRCapAGDDTTnvjXuLrZ-vN-orT~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A       C       inhost 127.0.0.1
C       A       OK inhost set
A       C       inport 37337
C       A       OK inbound port set
A       C       start
C       A       OK tunnel starting
A       C       quit
C       A       OK Bye!
```
Şimdi tek yapmamız gereken 127.0.0.1 adresine, 37337 portuna telnet ile bağlanmak, iletişim kurmak istediğimiz hedef anahtarını veya adres defterinden host adresini göndermek. Bu durumda "mouth" ile iletişim kurmak istiyoruz, tek yapmamız gereken anahtarı yapıştırmak ve çalışır.

**NOT:** Komut kanalındaki "quit" komutu SAM'deki gibi tunnel'ları BAĞLANTISINI kesmez.

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefg
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh
"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijk
...
```
Bu çıktının birkaç sanal mil devam etmesinden sonra, `Control-]` tuşlarına basın

```
...
cdefghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=
telnet> c
Connection closed.
```
İşte olan şey...

```
telnet -> ear -> i2p -> mouth -> chargen -.
telnet <- ear <- i2p <- mouth <-----------'
```
I2P SİTELERİNE de bağlanabilirsiniz!

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
i2host.i2p
GET / HTTP/1.1

HTTP/1.1 200 OK
Date: Fri, 05 Dec 2008 14:20:28 GMT
Connection: close
Content-Type: text/html
Content-Length: 3946
Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT
Accept-Ranges: bytes

<html>
<head>
  <title>I2HOST</title>
  <link rel="shortcut icon" href="favicon.ico">
</head>
...
<a href="http://sponge.i2p/">--Sponge.</a></pre>
<img src="/counter.gif" alt="!@^7A76Z!#(*&%"> visitors. </body>
</html>
Connection closed by foreign host.
$
```
Oldukça harika değil mi? İstersen bazı diğer bilinen I2P SITES'ları, var olmayan olanları vb. deneyin, farklı durumlarda ne tür çıktı bekleyeceğinizi hissetmek için. Çoğunlukla, hata mesajlarının herhangi birini görmezden gelmeniz önerilir. Bunlar uygulama için anlamsız olurdu ve yalnızca insan hata ayıklaması için sunulur.

### Temizlik

Artık hepsiyle işimiz bittiğine göre destination'larımızı kapatalım.

Öncelikle, hangi hedef takma adlarına sahip olduğumuzu görelim.

```
FROM    TO      DIALOGUE
A       C       list
C       A       DATA NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST: 127.0.0.1
C       A       DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT: not_set OUTHOST: localhost
C       A       OK Listing done
```
Tamam, işte oradalar. Önce "mouth"u kaldıralım.

```
FROM    TO      DIALOGUE
A       C       getnick mouth
C       A       OK Nickname set to mouth
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       OK cleared
```
Şimdi "ear"ı kaldırmak için, bunun çok hızlı yazdığınızda olan şey olduğunu ve tipik HATA mesajlarının nasıl göründüğünü size gösterdiğini unutmayın.

```
FROM    TO      DIALOGUE
A       C       getnick ear
C       A       OK Nickname set to ear
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       ERROR tunnel is active
A       C       clear
C       A       OK cleared
A       C       quit
C       A       OK Bye!
```
## Sessiz Mod

Köprünün alıcı ucuna örnek göstermekle uğraşmayacağım çünkü çok basit. Bunun için iki olası ayar var ve "quiet" komutuyla değiştiriliyor.

Varsayılan sessiz DEĞİLDİR ve dinleme soketinize gelen ilk veri, bağlantı kuran destination'dır. Bu, BASE64 adresinden ve ardından bir yeni satırdan oluşan tek bir satırdır. Bundan sonraki her şey, uygulamanın gerçekten tüketmesi içindir.

Sessiz modda, bunu normal bir İnternet bağlantısı gibi düşünün. Hiçbir ekstra veri gelmez. Sanki normal İnternet'e doğrudan bağlıymışsınız gibidir. Bu mod, router konsolu tunnel ayarları sayfalarında mevcut olana benzer bir şeffaflık biçimi sağlar, böylece BOB'u örneğin bir web sunucusuna yönlendirmek için kullanabilirsiniz ve web sunucusunda hiçbir değişiklik yapmanız gerekmez.

## BOB'un Avantajları

BOB'u bunun için kullanmanın avantajı daha önce tartışıldığı gibidir. Uygulama için rastgele çalışma zamanları planlayabilir, farklı bir makineye yönlendirebilir, vb. yapabilirsiniz. Bunun bir kullanımı, router'dan hedefe kadar olan erişilebilirlik tahminini karıştırmaya çalışmak gibi bir şey olabilir. Hizmetlerde rastgele açık ve kapalı zamanlar oluşturmak için destination'ı tamamen farklı bir süreçle durdurabilir ve başlatabilirsiniz. Bu şekilde yalnızca böyle bir hizmete ulaşma yeteneğini durdurmuş olursunuz ve onu kapatıp yeniden başlatmakla uğraşmanıza gerek kalmaz. Güncellemeler yaparken LAN'ınızdaki farklı bir makineye yönlendirebilir ve işaret edebilir, ya da çalışan duruma bağlı olarak bir dizi yedek makineye işaret edebilirsiniz, vb. vb. BOB ile yapabileceklerinizi yalnızca hayal gücünüz sınırlar.
