---
title: "SSU2 Taşıma"
date: 2022-10-11
author: "zzz"
description: "SSU2 Taşıma"
categories: ["development"]
---

## Genel Bakış

I2P, 2005'ten beri sansüre dayanıklı bir UDP taşıma protokolü olan "SSU"yu kullanmaktadır. 17 yıl içinde, SSU'nun engellendiğine dair çok az, hatta varsa bile, rapor aldık. Ancak, günümüzün güvenlik, engellemeye dayanıklılık ve performans standartlarına göre, daha iyisini yapabiliriz. Çok daha iyisini.

Bu yüzden, [i2pd project](https://i2pd.xyz/) ile birlikte, güvenlik ve engellemelere karşı dayanıklılık açısından en yüksek standartlara göre tasarlanmış modern bir UDP protokolü olan "SSU2"yi oluşturup uygulamaya koyduk. Bu protokol SSU'nun yerini alacaktır.

Sektör standardı şifrelemeyi, UDP protokolleri WireGuard ve QUIC'in en iyi özellikleriyle ve TCP protokolümüz "NTCP2"nin sansüre dayanıklılık özellikleriyle birleştirdik. SSU2, şimdiye kadar tasarlanmış en güvenli taşıma protokollerinden biri olabilir.

Java I2P ve i2pd ekipleri SSU2 taşıma protokolünü tamamlıyor ve bir sonraki sürümde onu tüm router'lar için etkinleştireceğiz. Bu, 2003'e dayanan özgün Java I2P uygulamasındaki tüm kriptografiyi yükseltmeye yönelik on yıllık planımızı tamamlıyor. SSU2, ElGamal kriptografisini kullandığımız tek kalan yer olan SSU'nun yerini alacak.

- Signature types and ECDSA signatures (0.9.8, 2013)
- Ed25519 signatures and leasesets (0.9.15, 2014)
- Ed25519 routers (0.9.22, 2015)
- Destination encryption types and X25519 leasesets (0.9.46, 2020)
- Router encryption types and X25519 routers (0.9.49, 2021)

SSU2'ye geçişin ardından, kimliği doğrulanmış ve şifrelenmiş tüm protokollerimizi standart [Noise Protocol](https://noiseprotocol.org/) el sıkışmalarına taşımış olacağız:

- NTCP2 (0.9.36, 2018)
- ECIES-X25519-Ratchet end-to-end protocol (0.9.46, 2020)
- ECIES-X25519 tunnel build messages (1.5.0, 2021)
- SSU2 (2.0.0, 2022)

Tüm I2P Noise protokolleri aşağıdaki standart kriptografik algoritmaları kullanır:

- [X25519](https://en.wikipedia.org/wiki/Curve25519)
- [ChaCha20/Poly1305 AEAD](https://www.rfc-editor.org/rfc/rfc8439.html)
- [SHA-256](https://en.wikipedia.org/wiki/SHA-2)

## Hedefler


- Upgrade the asymmetric cryptography to the much faster X25519
- Use standard symmetric authenticated encryption ChaCha20/Poly1305
- Improve the obfuscation and blocking resistance features of SSU
- Improve the resistance to spoofed addresses by adapting strategies from QUIC
- Improved handshake CPU efficiency
- Improved bandwidth efficiency via smaller handshakes and acknowledgements
- Improve the security of the peer test and relay features of SSU
- Improve the handling of peer IP and port changes by adapting the "connection migration" feature of QUIC
- Move away from heuristic code for packet handling to documented, algorithmic processing
- Support a gradual network transition from SSU to SSU2
- Easy extensibility using the block concept from NTCP2

## Tasarım

I2P, trafiği saldırganlardan korumak için birden fazla şifreleme katmanı kullanır. En alt katman, iki router arasındaki nokta-nokta bağlantıları için kullanılan taşıma protokolü katmanıdır. Şu anda iki taşıma protokolümüz var: 2018'de tanıtılan modern bir TCP protokolü olan NTCP2 ve 2005'te geliştirilen bir UDP protokolü olan SSU.

SSU2, önceki I2P taşıma protokollerinde olduğu gibi, veri için genel amaçlı bir kanal değildir. Birincil görevi, I2P'nin düşük seviyeli I2NP mesajlarını bir router'dan diğerine güvenli biçimde iletmektir. Bu nokta-nokta bağlantıların her biri, bir I2P tunnel içinde tek bir hop (atlama) oluşturur. I2P'nin daha üst katman protokolleri, I2P destinasyonları arasında garlic messages (garlic mesajları)nı uçtan uca teslim etmek için bu nokta-nokta bağlantıların üzerinde çalışır.

UDP tabanlı bir aktarım tasarlamak, TCP protokollerinde bulunmayan kendine özgü ve karmaşık zorlukları beraberinde getirir. Bir UDP protokolü, adres sahteciliğinin neden olduğu güvenlik sorunlarını ele almalı ve kendi tıkanıklık kontrolünü uygulamalıdır. Ayrıca, tüm iletiler ağ yolunun azami paket boyutuna (MTU) sığacak şekilde parçalanmalı ve alıcı tarafından yeniden birleştirilmelidir.

İlk olarak, kendi NTCP2, SSU ve akış protokollerimizle ilgili önceki deneyimlerimize büyük ölçüde dayandık. Ardından, yakın zamanda geliştirilen iki UDP protokolünü dikkatle inceledik ve onlardan kapsamlı biçimde yararlandık:

- QUIC ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html), [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html), [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.html))
- [WireGuard](https://www.wireguard.com/protocol/)

Ulus-devlet güvenlik duvarları gibi hasmane yol üzerindeki saldırganlar tarafından protokollerin sınıflandırılması ve engellenmesi, bu protokollerin tehdit modeline açıkça dahil değildir. Ancak, dünya çapındaki risk altındaki kullanıcılara anonim ve sansüre dayanıklı bir iletişim sistemi sağlamak misyonumuz olduğundan, bu konu I2P'nin tehdit modelinin önemli bir parçasıdır. Bu nedenle, tasarım çalışmalarımızın önemli bir kısmı NTCP2 ve SSU'dan edinilen dersleri, QUIC ve WireGuard'ın sağladığı özellikler ve güvenlikle birleştirmeyi içeriyordu.

## Performans

I2P ağı, çeşitli router'lardan oluşan karmaşık bir bileşimdir. Dünya genelinde, yüksek performanslı veri merkezi bilgisayarlarından Raspberry Pi'lere ve Android telefonlara kadar değişen donanımlarda çalışan iki temel gerçekleme vardır. Router'lar hem TCP hem de UDP taşıma protokollerini kullanır. SSU2 iyileştirmeleri önemli olsa da, bunların kullanıcıya, ister yerel olarak ister uçtan uca aktarım hızlarında, belirgin biçimde yansımasını beklemiyoruz.

İşte SSU2 ile SSU karşılaştırmasında tahmini iyileştirmelerin bazı öne çıkanları:

- 40% reduction in total handshake packet size
- 50% or more reduction in handshake CPU
- 90% or more reduction in ACK overhead
- 50% reduction in packet fragmentation
- 10% reduction in data phase overhead

## Geçiş Planı

I2P, hem ağ kararlılığını sağlamak hem de eski router'ların kullanışlı ve güvenli olmaya devam etmesine olanak tanımak için geriye dönük uyumluluğu korumaya çalışır. Ancak bunun da sınırları vardır, çünkü uyumluluk kod karmaşıklığını ve bakım gereksinimlerini artırır.

Java I2P ve i2pd projeleri, 2022 Kasım ayının sonlarında çıkacak bir sonraki sürümlerinde (2.0.0 ve 2.44.0) SSU2’yi varsayılan olarak etkinleştirecek. Ancak, SSU’yu devre dışı bırakma konusunda farklı planlara sahipler. i2pd SSU’yu derhal devre dışı bırakacak, çünkü SSU2, i2pd’nin SSU uygulamasına kıyasla çok büyük bir iyileştirmedir. Java I2P, kademeli bir geçişi desteklemek ve eski router’ların güncelleme yapması için zaman tanımak amacıyla 2023 ortasında SSU’yu devre dışı bırakmayı planlıyor.

## Özet


I2P'nin kurucuları kriptografik algoritmalar ve protokoller için birkaç tercih yapmak zorunda kaldılar. Bu tercihlerin bazıları diğerlerinden daha iyiydi, ancak yirmi yıl sonra, çoğu artık yaşını belli ediyor. Elbette bunun geleceğini biliyorduk ve son on yılı kriptografik yükseltmeleri planlayıp uygulamakla geçirdik.

SSU2, uzun yükseltme sürecimizde geliştirdiğimiz son ve en karmaşık protokol oldu. UDP, çok zorlayıcı bir varsayımlar dizisine ve tehdit modeline sahiptir. Önce üç başka Noise protokolü varyantını tasarlayıp devreye aldık ve güvenlik ile protokol tasarımına ilişkin konularda deneyim ve daha derin bir anlayış kazandık.

SSU2'nin, 2022 Kasım ayının sonlarına doğru yayımlanması planlanan i2pd ve Java I2P sürümlerinde etkinleştirileceğini bekleyin. Güncelleme sorunsuz gerçekleşirse, hiç kimse herhangi bir değişiklik fark etmeyecek. Performans iyileştirmeleri önemli olsa da, çoğu kişi için muhtemelen ölçülebilir olmayacak.

Her zamanki gibi, yeni sürüm kullanıma sunulduğunda güncellemenizi öneriyoruz. Güvenliği korumanın ve ağa yardımcı olmanın en iyi yolu, en son sürümü çalıştırmaktır.
