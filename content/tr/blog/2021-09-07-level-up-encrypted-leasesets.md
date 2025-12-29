---
title: "I2P becerilerinizi Şifrelenmiş LeaseSets (gelen tünel kümeleri) ile bir üst seviyeye taşıyın"
date: 2021-09-07
slug: "level-up-your-i2p-skills-with-encrypted-leasesets"
author: "idk"
description: "I2P'nin Gizli Servisleri vurguladığı söylenir; bunun bir yorumunu inceliyoruz."
categories: ["general"]
API_Translate: doğru
---

## Şifreli LeaseSets ile I2P becerilerinizi bir üst seviyeye taşıyın

Geçmişte, I2P'nin Gizli Hizmetleri desteklemeye odaklandığı söylenmiştir; bu, birçok bakımdan doğrudur. Ancak bunun kullanıcılar, geliştiriciler ve gizli hizmet yöneticileri için ne anlama geldiği her zaman aynı değildir. Şifrelenmiş LeaseSets ve bunların kullanım senaryuları, I2P'nin gizli hizmetleri nasıl daha esnek, yönetimi nasıl daha kolay hâle getirdiğine ve I2P'nin Gizli Hizmet kavramını potansiyel olarak ilginç kullanım senaryoları için güvenlik faydaları sağlayacak şekilde nasıl genişlettiğine dair benzersiz, pratik bir pencere sunar.

## LeaseSet nedir?

Bir gizli servis oluşturduğunuzda, I2P NetDB’ye "LeaseSet" (erişim kayıtları kümesi) adı verilen bir şeyi yayımlarsınız. En basit ifadeyle "LeaseSet", diğer I2P kullanıcılarının gizli servisinizin I2P Ağında "nerede" olduğunu keşfetmek için ihtiyaç duyduğu şeydir. İçinde, gizli servisinize ulaşmak için kullanılabilecek "tunnel"ları belirleyen "Leases" ve istemcilerin mesajları şifrelerken kullandığı "destination" (hedef adres) açık anahtarı bulunur. Bu tür bir gizli servis, adresi olan herkes tarafından erişilebilir; ki bu, şimdilik muhtemelen en yaygın kullanım senaryosudur.

Bazen gizli hizmetlerinizin herkes tarafından erişilebilir olmasını istemeyebilirsiniz. Bazı kişiler gizli hizmetleri, evdeki bir PC’deki bir SSH sunucusuna erişmenin bir yolu olarak veya IoT cihazlarından oluşan bir ağı birbirine bağlamak için kullanır. Bu durumlarda, gizli hizmetinizi I2P Ağı üzerindeki herkesin erişimine açmanız gerekli değildir ve hatta ters etki yaratabilir. İşte tam burada "Şifrelenmiş LeaseSets" devreye girer.

## Şifrelenmiş LeaseSets: ÇOK Gizli Servisler

Encrypted LeaseSets, NetDB'ye şifrelenmiş biçimde yayımlanan LeaseSets'tir; istemci, içindeki LeaseSet'in şifresini çözmek için gerekli anahtarlara sahip değilse, hiçbir Lease veya açık anahtar görünür değildir. Anahtarları paylaştığınız istemciler(PSK Encrypted LeaseSets için) ya da anahtarlarını sizinle paylaşanlar(DH Encrypted LeaseSets için) destination'ı görebilir; başka hiç kimse göremez.

I2P, Encrypted LeaseSets için çeşitli stratejileri destekler. Hangi stratejiyi kullanacağınıza karar verirken, her bir stratejinin temel özelliklerini anlamak önemlidir. Bir Encrypted LeaseSet "Önceden Paylaşılan Anahtar (PSK)" stratejisini kullanıyorsa, sunucu bir anahtar (veya anahtarlar) üretir ve sunucu işletmecisi bunu her istemciyle paylaşır. Elbette, bu alışveriş bant dışı gerçekleşmelidir; örneğin IRC üzerinden bir paylaşım yoluyla. Encrypted LeaseSets’in bu sürümü, bir parolayla Wi‑Fi’ye giriş yapmaya benzer. Ancak giriş yaptığınız şey bir Gizli Servis’tir.

Bir Encrypted LeaseSet (şifrelenmiş LeaseSet) bir Diffie-Hellman (DH) stratejisi kullanıyorsa, anahtarlar bunun yerine istemci üzerinde oluşturulur. Bir Diffie-Hellman istemcisi, Encrypted LeaseSet’e sahip bir hedefe bağlandığında, önce anahtarlarını sunucu işletmecisiyle paylaşmalıdır. Sunucu işletmecisi daha sonra DH istemcisini yetkilendirip yetkilendirmemeye karar verir. Encrypted LeaseSets’in bu sürümü, `authorized_keys` dosyasıyla SSH’ye biraz benzer. Ancak, oturum açtığınız şey bir Gizli Servis.

LeaseSet'inizi şifreleyerek, yalnızca yetkisiz kullanıcıların destination'ınıza (hedef) bağlanmasını imkânsız kılmakla kalmaz, aynı zamanda yetkisiz ziyaretçilerin I2P Gizli Servisi'nin gerçek destination'ını keşfetmesini dahi imkânsız hâle getirirsiniz. Bazı okuyucular muhtemelen kendi Encrypted LeaseSet'leri için bir kullanım senaryosunu şimdiden düşünmüştür.

## Şifreli LeaseSets Kullanarak Router Konsoluna Güvenli Erişim

Genel bir kural olarak, bir hizmetin cihazınız hakkında erişebildiği bilgi ne kadar karmaşıksa, o hizmeti İnternet'e, hatta I2P gibi bir Gizli Servis ağına açmak o kadar tehlikelidir. Böyle bir hizmeti açmak istiyorsanız, onu bir parola gibi bir şeyle korumanız gerekir; I2P söz konusu olduğunda ise, çok daha kapsamlı ve güvenli bir seçenek Encrypted LeaseSet olabilir.

**Devam etmeden önce, lütfen şunu okuyup anlayın: aşağıdaki işlemi Encrypted LeaseSet olmadan yaparsanız, I2P router'ınızın güvenliğini ortadan kaldırmış olursunuz. Encrypted LeaseSet olmadan I2P üzerinden router konsolunuza erişimi yapılandırmayın. Ayrıca, Encrypted LeaseSet PSK'lerinizi kontrol etmediğiniz cihazlarla paylaşmayın.**

I2P üzerinden paylaşılması faydalı olan, ancak SADECE Encrypted LeaseSet ile yapılması gereken hizmetlerden biri, I2P router konsolunun kendisidir. Bir makinedeki I2P router konsolunu Encrypted LeaseSet ile I2P’ye açmak, bir tarayıcıya sahip başka bir makinenin uzaktaki I2P örneğini yönetmesine olanak tanır. Bunu, düzenli olarak kullandığım I2P hizmetlerimi uzaktan izlemek için yararlı buluyorum. Ayrıca, I2PSnark’e erişmek için, uzun süreli torrent paylaşımı (seed) yapan bir sunucuyu izlemek amacıyla da kullanılabilir.

Anlatması ne kadar uzun sürerse sürsün, Şifrelenmiş LeaseSet'i Hidden Services Manager UI aracılığıyla yapılandırmak oldukça basittir.

## "Sunucu"da

Önce http://127.0.0.1:7657/i2ptunnelmgr adresindeki Hidden Services Manager (Gizli Hizmetler Yöneticisi) sayfasını açın ve "I2P Hidden Services." yazan bölümün en altına kadar inin. Ana makine "127.0.0.1" ve bağlantı noktası "7657" olacak şekilde, bu "Tunnel Cryptography Options" ile yeni bir gizli hizmet oluşturun ve gizli hizmeti kaydedin.

Then, select your new tunnel from the Hidden Services Manager main page. The Tunnel Cryptography Options should now include your first Pre-Shared Key. Copy this down for the next step, along with the Encrypted Base32 Address of your tunnel.

## "Client" üzerinde

Şimdi, gizli servise bağlanacak olan istemci bilgisayara geçin ve önceki anahtarları eklemek için http://127.0.0.1:7657/configkeyring adresindeki Keyring Configuration sayfasını ziyaret edin. Başlangıç olarak, Sunucu’dan Base32’yi şu etiketli alana yapıştırın: "Full destination, name, Base32, or hash." Ardından, sunucudaki Pre-Shared Key (önceden paylaşılan anahtar) değerini "Encryption Key" alanına yapıştırın. Kaydet’e tıklayın ve Encrypted LeaseSet kullanarak gizli servisi güvenli bir şekilde ziyaret etmeye hazırsınız.

## Artık I2P'yi uzaktan yönetmeye hazırsınız

Görebileceğiniz gibi, I2P, Gizli Servis Yöneticilerine dünyanın her yerinden I2P bağlantılarını güvenli bir şekilde yönetmelerine olanak tanıyan benzersiz yetenekler sunar. Aynı nedenle aynı cihazda tuttuğum diğer Encrypted LeaseSets, SSH sunucusunu, servis konteynerlerimi yönetmek için kullandığım Portainer örneğini ve kişisel NextCloud örneğimi işaret eder. I2P ile, gerçekten özel ve her zaman erişilebilir kendi barındırma, ulaşılabilir bir hedeftir; hatta Encrypted LeaseSets sayesinde bunun benzersiz biçimde uygun olduğumuz alanlardan biri olduğunu düşünüyorum. Onlar sayesinde, I2P kendi barındırmalı ev otomasyonunu güvence altına almanın anahtarı olabilir ya da sadece daha özel bir peer-to-peer (eşler arası) webin omurgası haline gelebilir.
