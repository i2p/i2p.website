---
title: "2006-09-12 tarihli I2P Durum Notları"
date: 2006-09-12
author: "jr"
description: "Ağ kararlılığı iyileştirmeleri, I2PSnark optimizasyonları ve çevrimdışı dağıtık forumlarla kapsamlı Syndie yeniden tasarımı içeren 0.6.1.25 sürümü"
categories: ["status"]
---

Selam millet, işte bizim *öhöm* haftalık durum notlarımız

* Index:

1) 0.6.1.25 ve ağ durumu 2) I2PSnark 3) Syndie (ne/neden/ne zaman) 4) Syndie kriptografi soruları 5) ???

* 1) 0.6.1.25 and net status

Geçen gün 0.6.1.25 sürümünü yayımladık; bu sürüm, son ay boyunca birikmiş birçok hata düzeltmesinin yanı sıra I2PSnark üzerindeki zzz’in çalışmaları ve zaman senkronizasyon kodumuzu biraz daha sağlamlaştırmaya yönelik Complication’ın çalışmalarını da içeriyor. Şu anda ağ oldukça kararlı görünüyor, ancak son birkaç gündür IRC biraz sorunluydu (I2P ile ilgisi olmayan nedenlerden dolayı). Ağın belki de yarısı en son sürüme yükseltildiğinden, tunnel oluşturma başarı oranları çok değişmedi; ancak genel throughput (aktarım hızı) artmış görünüyor (muhtemelen I2PSnark kullanan kişi sayısındaki artış nedeniyle).

* 2) I2PSnark

zzz'nin I2PSnark için yaptığı güncellemeler, geçmiş günlüğünde [1] açıklandığı gibi, protokol optimizasyonlarının yanı sıra web arayüzlerindeki değişiklikleri de içeriyordu. Ayrıca 0.6.1.25 sürümünden bu yana I2PSnark için birkaç küçük güncelleme daha yapıldı ve belki zzz bu akşamki toplantıda bize son duruma genel bir bakış sunabilir.

[1] <http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD>

* 3) Syndie

Hepinizin bildiği gibi, zamanım Syndie’yi elden geçirmeye odaklanmış durumda, gerçi “revamp” doğru sözcük olmayabilir. Belki de şu anda kullanıma sunulmuş olanı bir “proof of concept” (kavram kanıtı) olarak düşünebilirsiniz; çünkü yeni Syndie en baştan yeniden tasarlanıp yeniden uygulandı, ancak birçok kavram yerini koruyor. Aşağıda Syndie’den söz ettiğimde, yeni Syndie’yi kastediyorum.

* 3.1) What is Syndie

Syndie, en temel düzeyde, çevrimdışı dağıtık forumları işletmeye yarayan bir sistemdir. Yapısı çok sayıda farklı yapılandırmaya olanak tanırken, gereksinimlerin çoğu aşağıdaki üç ölçütün her biri için bir seçenek seçilerek karşılanabilir:  - Forum türleri:    - Tek yazar (tipik blog)    - Birden çok yazar (çok yazarlı blog)**    - Açık (haber grupları; yalnızca
      yetkili** kullanıcıların yeni başlıklar açabilmesi için kısıtlamalar eklenebilirken, herkes
      bu yeni başlıklar üzerine yorum yapabilir)  - Görünürlük:    - Herkes her şeyi okuyabilir    - Yalnızca yetkili* kişiler gönderileri okuyabilir, ancak bazı üstveriler görünür    - Yalnızca yetkili* kişiler gönderileri okuyabilir; hatta kimlerin gönderi yaptığını bile yalnızca onlar bilir    - Yalnızca yetkili* kişiler gönderileri okuyabilir ve kimlerin gönderi yaptığı
      hiç kimse tarafından bilinmez  - Yorumlar/yanıtlar:    - Herkes yorum yapabilir ya da yazar/forum
      sahibine özel yanıtlar gönderebilir    - Yalnızca yetkili** kişiler yorum yapabilir ve herkes özel
      yanıtlar gönderebilir    - Kimse yorum yapamaz, ancak herkes özel yanıtlar gönderebilir    - Kimse yorum yapamaz ve kimse özel yanıtlar gönderemez

 * reading is authorized by giving people the symmetric key or passphrase
   to decrypt the post.  Alternately, the post may include a publicly
   visible prompt, where the correct answer serves to generate the
   correct decryption key.

** gönderi paylaşma, güncelleme ve/veya yorum yapma yetkisi, bu kullanıcılara gönderileri imzalamaları için asimetrik özel anahtarlar sağlanarak verilir, karşılık gelen açık anahtar ise forumda gönderi paylaşma, yönetme veya yorum yapma yetkisine sahip olarak forumun üstverisine dahil edilir.  Alternatif olarak, yetkilendirilmiş bireysel kullanıcıların imzalama amaçlı açık anahtarları medtata içinde listelenebilir.

Bireysel gönderiler birçok farklı öğe içerebilir:  - Herhangi sayıda sayfa; her sayfa için içerik türünü, dili vb.    belirten bant dışı verilerle birlikte.  Herhangi bir biçim kullanılabilir;    içeriği güvenli şekilde görüntülemek istemci uygulamaya bağlıdır - düz metin    desteklenmelidir ve mümkün olan istemciler HTML'yi desteklemelidir.  - Herhangi sayıda ek (yine, eki tanımlayan bant dışı verilerle    birlikte)  - Gönderi için küçük bir avatar (ancak belirtilmemişse, yazarın    varsayılan avatarı kullanılır)  - Diğer gönderilere, forumlara, arşivlere, URL'lere vb. referanslardan    oluşan bir küme (bunlar,    atıfta bulunulan forumlara gönderi yapmak, yönetmek veya okumak için gerekli    anahtarları içerebilir)

Genel olarak, Syndie *içerik katmanı*nda çalışır - bireysel gönderiler şifrelenmiş zip dosyalarında yer alır ve foruma katılmak, basitçe bu dosyaları paylaşmak anlamına gelir. Dosyaların nasıl aktarıldığına ilişkin bir bağımlılık yoktur (I2P, Tor, Freenet, gnutella, bittorrent, RSS, usenet, email üzerinden), ancak basit toplama ve dağıtım araçları standart Syndie sürümüyle birlikte paketlenecektir.

Syndie içeriğiyle etkileşim çeşitli yollarla gerçekleşecektir. Öncelikle, betiklenebilir metin tabanlı bir arayüz vardır; bu arayüz, temel komut satırı ve etkileşimli modda forumlardan okuma, forumlara yazma, yönetme ve eşzamanlama olanağı sağlar. Örneğin, aşağıdaki, yeni bir "günün mesajı" gönderisi oluşturmak için basit bir betiktir -

login     menu post     create --channel 0000000000000000000000000000000000000000     addpage --in /etc/motd --content-type text/plain     addattachment --in ~/webcam.png --content-type image/png     listauthkeys --authorizedOnly true     authenticate 0     authorize 0     set --subject "Today's MOTD"     set --publicTags motd     execute     exit

Basitçe bunu pipe operatörüyle syndie yürütülebilir dosyasına gönderin ve iş tamamdır: cat motd-script | ./syndie > syndie.log

Ek olarak, grafiksel bir Syndie arayüzü üzerinde çalışmalar sürüyor; bu arayüz, düz metin ve HTML sayfalarının güvenli biçimde görüntülenmesini içerir (elbette, Syndie'nin özellikleriyle şeffaf entegrasyon desteğiyle).

Syndie’nin eski "sucker" koduna dayanan uygulamalar, normal web sayfalarının ve web sitelerinin içeriklerinin çekilmesini (scraping) ve yeniden yazılmasını mümkün kılarak, bunların, görseller ve diğer kaynaklar ekler olarak dahil edilerek, tek ya da çok sayfalı Syndie gönderileri olarak kullanılmasına olanak tanıyacaktır.

İleride, Firefox/Mozilla eklentilerinin hem Syndie biçimli dosyaları ve Syndie referanslarını algılayıp içe aktarması hem de belirli bir forum, konu, etiket, yazar ya da arama sonucuna odaklanılması gerektiğini yerel Syndie grafik kullanıcı arayüzüne bildirmesi planlanmaktadır.

Elbette, Syndie özünde tanımlı bir dosya biçimi ve kriptografik algoritmalara sahip bir içerik katmanı olduğundan, diğer uygulamalar veya alternatif gerçeklemeler muhtemelen zamanla ortaya çıkacaktır.

* 3.2) Why does Syndie matter?

Son birkaç ayda neden bir forum/blog aracı üzerinde çalıştığımı soran birkaç kişinin olduğunu duydum - bunun güçlü anonimlik sağlamakla ne ilgisi var?

Yanıt: *her şey*.

Kısaca özetlemek gerekirse:  - Anonimlik hassasiyetine sahip bir istemci uygulaması olarak Syndie'nin tasarımı, anonimlik gözetilerek oluşturulmamış uygulamaların neredeyse tamamının kaçınamadığı karmaşık veri hassasiyeti sorunlarından özenle kaçınır.  - İçerik katmanında çalışarak, Syndie I2P, Tor veya Freenet gibi dağıtık ağların performansına ya da güvenilirliğine bağımlı değildir; uygun olduğunda bunlardan yararlanabilir.  - Böyle yaparak, içerik dağıtımı için küçük, ad-hoc mekanizmalar (duruma özel) ile tamamen çalışabilir - ki bu mekanizmalar, güçlü saldırganların bunları karşı atakla boşa çıkarmaya uğraşmasına değmeyebilir (çünkü sadece birkaç düzine kişiyi yakalamanın 'getirisi', saldırıları gerçekleştirme maliyetini büyük olasılıkla aşacaktır)  - Bu da, Syndie'nin birkaç milyon kişi kullanmasa bile yararlı olacağını ima eder - birbiriyle ilişkisi olmayan küçük insan grupları, diğer gruplarla herhangi bir etkileşim gerektirmeden, hatta onlardan haberdar olmadan kendi özel Syndie dağıtım düzenlerini kurmalıdır.  - Syndie gerçek zamanlı etkileşime dayanmadığından, tüm düşük gecikmeli sistemlerin savunmasız olduğu saldırılardan kaçınmak için yüksek gecikmeli anonimlik sistemleri ve tekniklerini bile kullanabilir (örneğin pasif kesişim saldırıları, pasif ve aktif zamanlama saldırıları ve aktif harmanlama saldırıları).

Genel olarak, benim görüşüm, Syndie'nin, I2P'nin temel misyonu (ihtiyaç duyanlara güçlü anonimliğin sağlanması) açısından, hatta router'dan bile daha önemli olduğudur. Nihai çözüm değil, ama kilit bir adımdır.

* 3.3) When can we use Syndie?

Metin arayüzünün neredeyse tamamı ve GUI'nin (Grafik Kullanıcı Arayüzü) önemli bir bölümü dahil olmak üzere, çok sayıda çalışma tamamlanmış olsa da, yapılacak işler hâlâ var. Syndie'nin ilk sürümü aşağıdaki temel işlevselliği içerecek:

 - Scriptable text interface, packaged up as a typical java application,
   or buildable with a modern GCJ
 - Support for all forum types, replies, comments, etc.
 - Manual syndication, transferring .snd files.
 - HTTP syndication, including simple CGI scripts to operate archives,
   controllable through the text interface.
 - Specs for the file formats, encryption algorithms, and database
   schema.

Bunu kullanıma sunarken kullanacağım ölçüt "tam işlevsel" olması olacak. Sıradan kullanıcı metin tabanlı bir uygulamayla uğraşmayacak, ama bazı teknik meraklıların uğraşacağını umuyorum.

Sonraki sürümler, Syndie'nin yeteneklerini birden fazla alanda geliştirecek:  - Kullanıcı arayüzü:   - SWT tabanlı GUI   - Web tarayıcısı eklentileri   - Web kazıma metin arayüzü (sayfaları içeri alma ve yeniden yazma)   - IMAP/POP3/NNTP okuma arayüzü  - İçerik desteği   - Düz metin   - HTML (güvenli biçimde GUI içinde işleme, tarayıcıda değil)   - BBCode (?)  - Syndikasyon   - Feedspace, Feedtree ve diğer düşük gecikmeli eşzamanlama araçları   - Freenet (.snd dosyalarını CHK@s üzerinde depolama ve arşivlerin
    .snd dosyalarına SSK@s ve USK@s üzerinde atıfta bulunması)   - E-posta (SMTP/mixmaster/mixminion üzerinden gönderme, okuma
    procmail/etc aracılığıyla)   - Usenet (NNTP veya remailer'lar üzerinden gönderme, (proxy'li)
    NNTP üzerinden okuma)  - Lucene entegrasyonu ile tam metin arama  - Tam veritabanı şifrelemesi için HSQLDB'nin genişletilmesi  - Ek arşiv yönetimi sezgisel yöntemleri

Ne zaman ne çıktığı, işlerin ne zaman yapıldığına bağlıdır.

* 4) Open questions for Syndie

Şu anda, Syndie I2P'nin standart kriptografik ilkeleri - SHA256, AES256/CBC, ElGamal2048, DSA - ile uygulanmış durumda. Ancak sonuncusu aykırı duruyor, çünkü 1024bit açık anahtarlar kullanıyor ve (hızla zayıflayan) SHA1'e dayanıyor. Sahadan duyduğum söylentilerden biri DSA'nın SHA256 ile güçlendirilmesi; bu yapılabilir (her ne kadar henüz standartlaşmamış olsa da), ancak yalnızca 1024bit açık anahtarlar sunar.

Syndie henüz genel kullanıma sunulmadığı ve geri uyumluluk konusunda bir endişe bulunmadığı için, kriptografik primitifleri değiştirme lüksüne sahibiz. Bir yaklaşım, DSA yerine ElGamal2048 veya RSA2048 imzalarını tercih etmektir; başka bir yaklaşım ise ECC’ye (ECDSA imzaları ve ECIES asimetrik şifreleme ile), belki de 256bit veya 521bit güvenlik seviyelerine yönelmektir (sırasıyla 128bit ve 256bit simetrik anahtar boyutlarına karşılık gelecek şekilde).

ECC ile ilgili patent sorunlarına gelince, bunlar yalnızca belirli optimizasyonlar (point compression) ve ihtiyaç duymadığımız algoritmalar (EC MQV) için geçerli görünüyor. Java desteği açısından pek bir şey yok, ancak bouncycastle kütüphanesi bazı kodlar içeriyor gibi görünüyor. Yine de, libGMP için yaptığımız gibi (bize jbigi'yi kazandıran), libtomcrypt, openssl veya crypto++ için küçük sarmalayıcılar eklemek de muhtemelen çok zor olmayacaktır.

Bu konuda bir düşünceniz var mı?

* 5) ???

Yukarıda sindirilecek çok şey var, bu yüzden (cervantes'in önerisiyle) bu durum notlarını bu kadar erken gönderiyorum. Herhangi bir yorumunuz, sorunuz, endişeniz ya da öneriniz varsa, bu akşam UTC 20:00'de, bizim *öksürür* haftalık toplantımız için irc.freenode.net/irc.postman.i2p/irc.freshcoffee.i2p üzerindeki #i2p kanalına uğrayın!

=jr
