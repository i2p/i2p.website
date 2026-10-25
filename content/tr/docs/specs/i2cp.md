---
title: "I2P Client Protocol (I2CP)"
description: "Uygulamaların I2P router ile oturumları, tunnel'ları ve leaseSet'leri nasıl müzakere ettiği."
slug: "i2cp"
aliases:
  - "/tr/docs/api/i2cp"
  - "/tr/docs/api/i2cp/"
  - "/tr/docs/specs/i2cp-spec"
  - "/tr/docs/specs/i2cp-spec/"
category: "Protokoller"
lastUpdated: "2025-07"
accurateFor: "0.9.67"
---

## Genel Bakış

Bu, istemciler ve router arasındaki düşük seviye arayüz olan I2P Control Protocol (I2CP)'nin spesifikasyonudur. Java istemcileri bu protokolü uygulayan I2CP istemci API'sini kullanacaktır.

I2CP'yi uygulayan istemci taraflı bir kütüphanenin Java dışı bilinen bir uygulaması yoktur. Ayrıca, soket odaklı (streaming) uygulamalar streaming protokolünün bir uygulamasına ihtiyaç duyacaktır, ancak bunun için de Java dışı kütüphaneler mevcut değildir. Bu nedenle, Java dışı istemciler bunun yerine birkaç dilde kütüphanelerin mevcut olduğu üst seviye protokol SAM [SAMv3](/docs/api/samv3/) kullanmalıdır.

Bu, Java I2P router tarafından hem dahili hem de harici olarak desteklenen düşük seviyeli bir protokoldür. Protokol yalnızca istemci ve router aynı JVM'de değilse serialize edilir; aksi takdirde, I2CP mesaj Java nesneleri dahili bir JVM arayüzü aracılığıyla iletilir. I2CP ayrıca C++ router i2pd tarafından da harici olarak desteklenir.

Daha fazla bilgi I2CP Genel Bakış sayfasında bulunmaktadır [I2CP](/docs/specs/i2cp/).

## Oturumlar

Protokol, tek bir TCP bağlantısı üzerinde her biri 2 baytlık oturum kimliğine sahip birden fazla "oturum"u işleyecek şekilde tasarlanmıştır, ancak çoklu oturumlar 0.9.21 sürümüne kadar uygulanmamıştır. [Aşağıdaki çoklu oturum bölümüne](#multisession) bakın. 0.9.21 sürümünden eski router'lar ile tek bir I2CP bağlantısı üzerinde çoklu oturum kullanmaya çalışmayın.

Ayrıca tek bir istemcinin ayrı bağlantılar üzerinden birden fazla router ile konuşması için bazı hükümler olduğu da görünüyor. Bu da test edilmemiş ve muhtemelen yararlı değil.

Bağlantı kesildikten sonra bir oturumun sürdürülmesi veya farklı bir I2CP bağlantısında kurtarılması mümkün değildir. Soket kapatıldığında, oturum yok edilir.

## Örnek Mesaj Dizileri

Not: Aşağıdaki örnekler, istemciden router'a ilk bağlantı kurulurken gönderilmesi gereken Protokol Baytını (0x2a) göstermemektedir. Bağlantı başlatma hakkında daha fazla bilgi I2CP Genel Bakış sayfasında bulunmaktadır [I2CP](/docs/specs/i2cp/).

### Standart Oturum Kurulumu

```
  Client                                           Router

                           --------------------->  Get Date Message
        Set Date Message  <---------------------
                           --------------------->  Create Session Message
  Session Status Message  <---------------------
Request LeaseSet Message  <---------------------
                           --------------------->  Create LeaseSet Message

```
### Bant Genişliği Limitlerini Al (Basit Oturum)

```
  Client                                           Router

                           --------------------->  Get Bandwidth Limits Message
Bandwidth Limits Message  <---------------------

```
### Hedef Arama (Basit Oturum)

```
  Client                                           Router

                           --------------------->  Dest Lookup Message
      Dest Reply Message  <---------------------

```
### Giden Mesaj

Mevcut oturum, i2cp.messageReliability=none ile

```
  Client                                           Router

                           --------------------->  Send Message Message

```
Mevcut oturum, i2cp.messageReliability=none ve sıfır olmayan nonce ile

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (succeeded)

```
Mevcut oturum, i2cp.messageReliability=BestEffort ile

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (accepted)
  Message Status Message  <---------------------
  (succeeded)

```
### Gelen Mesaj

Mevcut oturum, i2cp.fastReceive=true ile (0.9.4 sürümünden itibaren)

```
  Client                                           Router

 Message Payload Message  <---------------------

```
Mevcut oturum, i2cp.fastReceive=false ile (KULLANIM DIŞI)

```
  Client                                           Router

  Message Status Message  <---------------------
  (available)
                           --------------------->  Receive Message Begin Message
 Message Payload Message  <---------------------
                           --------------------->  Receive Message End Message

```
### Çoklu Oturum Notları {#multisession}

Router sürüm 0.9.21'den itibaren tek bir I2CP bağlantısında birden fazla oturum desteklenmektedir. Oluşturulan ilk oturum "birincil oturum"dur. Ek oturumlar "alt oturum"lardır. Alt oturumlar, ortak bir tunnel kümesini paylaşan birden fazla hedefe destek sağlamak için kullanılır. İlk uygulama, birincil oturumun ECDSA imzalama anahtarlarını kullanması, alt oturumun ise eski eepsite'larla iletişim için DSA imzalama anahtarlarını kullanması içindir.

Alt oturumlar, birincil oturum ile aynı gelen ve giden tunnel havuzlarını paylaşır. Alt oturumlar, birincil oturum ile aynı şifreleme anahtarlarını kullanmalıdır. Bu hem LeaseSet şifreleme anahtarları hem de (kullanılmayan) Destination şifreleme anahtarları için geçerlidir. Alt oturumlar destination'da farklı imzalama anahtarları kullanmalıdır, böylece destination hash'i birincil oturumdan farklı olur. Alt oturumlar birincil oturum ile aynı şifreleme anahtarlarını ve tunnel'ları kullandığından, Destination'ların aynı router üzerinde çalıştığı herkesçe bilinir, bu nedenle olağan korelasyon karşıtı anonimlik garantileri geçerli olmaz.

Alt oturumlar, her zamanki gibi bir CreateSession mesajı gönderilerek ve karşılığında bir SessionStatus mesajı alınarak oluşturulur. Alt oturumlar, birincil oturum oluşturulduktan sonra oluşturulmalıdır. SessionStatus yanıtı, başarı durumunda, birincil oturumun ID'sinden farklı olan benzersiz bir Session ID içerecektir. CreateSession mesajları sıralı olarak işlenmeli olsa da, bir CreateSession mesajını yanıtla ilişkilendirmenin kesin bir yolu yoktur, bu nedenle bir istemci aynı anda birden fazla bekleyen CreateSession mesajına sahip olmamalıdır. Alt oturum için SessionConfig seçenekleri, birincil oturumdan farklı oldukları durumlarda dikkate alınmayabilir. Özellikle, alt oturumlar birincil oturumla aynı tunnel havuzunu kullandığından, tunnel seçenekleri göz ardı edilebilir.

Router, her Destination için istemciye ayrı RequestVariableLeaseSet mesajları gönderecek ve istemci her biri için CreateLeaseSet mesajı ile yanıt vermelidir. İki Destination için lease'ler aynı tunnel havuzundan seçilmiş olsalar bile mutlaka aynı olmayacaktır.

Bir alt oturum, her zamanki gibi DestroySession mesajı ile sonlandırılabilir. Bu, birincil oturumu sonlandırmaz veya I2CP bağlantısını durdurmaz. Ancak birincil oturumun sonlandırılması, tüm alt oturumları sonlandırır ve I2CP bağlantısını durdurur. Disconnect mesajı tüm oturumları sonlandırır.

Çoğu I2CP mesajının Session ID içerdiğini, ancak hepsinin içermediğini unutmayın. İçermeyenler için, istemciler router yanıtlarını düzgün şekilde işlemek için ek mantık gerektirebilir. DestLookup ve DestReply Session ID içermez; bunun yerine daha yeni HostLookup ve HostReply kullanın. GetBandwidthLimts ve BandwidthLimits session ID içermez, ancak yanıt session-spesifik değildir.

### Sürüm Notları {#notes}

İstemci tarafından gönderilen ilk protokol sürüm baytı (0x2a) değişmesi beklenmez. 0.8.7 sürümünden önce, router'ın sürüm bilgisi istemci tarafından erişilebilir değildi, bu da yeni istemcilerin eski router'larla çalışmasını engelliyordu. 0.8.7 sürümünden itibaren, iki tarafın protokol sürüm dizileri Get/Set Date Messages içinde değiştirilir. İleriye dönük olarak, istemciler bu bilgiyi eski router'larla doğru şekilde iletişim kurmak için kullanabilir. İstemciler ve router'lar karşı tarafça desteklenmeyen mesajlar göndermemelidir, çünkü genellikle desteklenmeyen bir mesaj aldıklarında oturumu keserler.

Değiştirilen sürüm bilgisi "çekirdek" API sürümü veya I2CP protokol sürümüdür ve mutlaka router sürümü değildir.

I2CP protokol sürümlerinin temel özeti aşağıdaki gibidir. Ayrıntılar için aşağıya bakın.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Required I2CP Features</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.67</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">PQ Hybrid ML-KEM (enc types 5-7) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host lookup/reply extensions (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MessageStatus message Loopback error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 (enc type 4) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BlindingInfo message supported; Additional HostReply message failure codes</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet options; MessageStatus message Meta LS error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">CreateLeaseSet2 message and options supported; Dest/LS key certs w/ RedDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Preliminary CreateLeaseSet2 message supported (abandoned)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Multiple sessions on a single I2CP connection supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional SetDate messages may be sent to the client at any time</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Authentication, if enabled, is required via GetDate before all other messages</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Per-message override of messageReliability=none with nonzero nonce</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types supported; RSA sig types also supported but currently unused</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host Lookup and Host Reply messages supported; Authentication mapping in Get Date message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Request Variable Lease Set message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional Message Status codes defined</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message nonce=0 allowed; Fast receive mode is the default</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag tag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a lease set (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Date and Set Date version strings included. If not present, the client or router is version 0.8.6 or older.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Get Bandwidth messages supported in standard session; Concurrent Dest Lookup messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability=none supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Bandwidth Limits and Bandwidth Limits messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires message supported; Reconfigure Session message supported; Ports and protocol numbers in gzip header</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Dest Reply messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
</table>
## Yaygın yapılar {#structures}

### I2CP mesaj başlığı {#struct-I2CPMessageHeader}

#### Açıklama

Mesaj uzunluğu ve mesaj türünü içeren, tüm I2CP mesajlarına ortak başlık.

#### İçindekiler

1.  Mesaj gövdesinin uzunluğunu belirten 4 byte [Integer](/docs/specs/common-structures/#integer)
2.  Mesaj türünü belirten 1 byte [Integer](/docs/specs/common-structures/#integer)
3.  I2CP mesaj gövdesi, 0 veya daha fazla byte

#### Notlar

Gerçek mesaj uzunluğu sınırı yaklaşık 64 KB'dir.

### Mesaj Kimliği {#struct-MessageId}

#### Açıklama

Belirli bir zamanda belirli bir router'da bekleyen bir mesajı benzersiz şekilde tanımlar. Bu her zaman router tarafından oluşturulur ve istemci tarafından oluşturulan nonce ile aynı DEĞİLDİR.

#### İçindekiler

1.  4 bayt [Integer](/docs/specs/common-structures/#integer)

#### Notlar

Mesaj ID'leri yalnızca bir oturum içinde benzersizdir; global olarak benzersiz değildir.

### Payload {#struct-Payload}

#### Açıklama

Bu yapı, bir Destination'dan diğerine iletilen mesajın içeriğidir.

#### İçindekiler

1.  4 bayt [Integer](/docs/specs/common-structures/#integer) uzunluğu
2.  O kadar bayt

#### Notlar

Yük, I2CP Genel Bakış sayfasında [I2CP-FORMAT](/docs/specs/i2cp/#format) belirtilen gzip formatındadır.

Gerçek mesaj uzunluğu sınırı yaklaşık 64 KB'dir.

### Oturum Yapılandırması {#struct-SessionConfig}

#### Açıklama

Belirli bir istemci oturumu için yapılandırma seçeneklerini tanımlar.

#### İçindekiler

1.  [Destination](/docs/specs/common-structures/#destination)
2.  Seçeneklerin [Mapping](/docs/specs/common-structures/#mapping)'i
3.  Oluşturma [Date](/docs/specs/common-structures/#date)'i
4.  Önceki 3 alanın [Signature](/docs/specs/common-structures/#signature)'ı,
    [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) tarafından imzalanmış

#### Notlar

- Seçenekler I2CP Genel Bakış sayfasında belirtilmiştir
  [I2CP-OPTIONS](/docs/specs/i2cp/#options).
- [Mapping](/docs/specs/common-structures/#mapping), router'da imzanın doğru şekilde doğrulanabilmesi için anahtar tarafından sıralanmış olmalıdır.
- Oluşturma tarihi, router tarafından işlendiğinde mevcut zamandan +/- 30 saniye içinde olmalıdır, aksi takdirde yapılandırma reddedilir.

#### Çevrimdışı İmzalar

- Eğer [Destination](/docs/specs/common-structures/#destination) çevrimdışı imzalanmışsa,
  [Mapping](/docs/specs/common-structures/#mapping) üç seçeneği içermelidir:
  i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, ve
  i2cp.leaseSetOfflineSignature. 
  [Signature](/docs/specs/common-structures/#signature) daha sonra geçici
  [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) tarafından oluşturulur ve
  i2cp.leaseSetTransientPublicKey içinde belirtilen
  [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) ile doğrulanır. Ayrıntılar için
  [I2CP-OPTIONS](/docs/specs/i2cp/#options) bölümüne bakın.

### Session ID {#struct-SessionId}

#### Açıklama

Belirli bir zamanda, belirli bir router üzerindeki bir oturumu benzersiz şekilde tanımlar.

#### İçindekiler

1.  2 bayt [Tamsayı](/docs/specs/common-structures/#integer)

#### Notlar

Oturum ID'si 0xffff "oturum yok" anlamında kullanılır, örneğin hostname sorgulamaları için.

## Mesajlar

Ayrıca [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html) sayfasına bakın.

### Mesaj Türleri {#types}

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Direction</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BandwidthLimitsMessage">BandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BlindingInfoMessage">BlindingInfoMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">42</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSetMessage">CreateLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSet2Message">CreateLeaseSet2Message</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateSessionMessage">CreateSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestLookupMessage">DestLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">34</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestReplyMessage">DestReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">35</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestroySessionMessage">DestroySessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DisconnectMessage">DisconnectMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetBandwidthLimitsMessage">GetBandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetDateMessage">GetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostLookupMessage">HostLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostReplyMessage">HostReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessagePayloadMessage">MessagePayloadMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">31</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessageStatusMessage">MessageStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageBeginMessage">ReceiveMessageBeginMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageEndMessage">ReceiveMessageEndMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReportAbuseMessage">ReportAbuseMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">29</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestLeaseSetMessage">RequestLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestVariableLeaseSetMessage">RequestVariableLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">37</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageMessage">SendMessageMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageExpiresMessage">SendMessageExpiresMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SessionStatusMessage">SessionStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SetDateMessage">SetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">33</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### BandwidthLimitsMessage {#BandwidthLimitsMessage}

#### Açıklama

İstemciye bant genişliği sınırlarının ne olduğunu söyle.

Router'dan Client'a [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage) yanıtı olarak gönderilir.

#### İçindekiler

1.  4 byte [Integer](/docs/specs/common-structures/#integer) İstemci gelen limit
    (KBps)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) İstemci giden limit
    (KBps)
3.  4 byte [Integer](/docs/specs/common-structures/#integer) Router gelen limit
    (KBps)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) Router gelen burst limit
    (KBps)
5.  4 byte [Integer](/docs/specs/common-structures/#integer) Router giden limit
    (KBps)
6.  4 byte [Integer](/docs/specs/common-structures/#integer) Router giden burst
    limit (KBps)
7.  4 byte [Integer](/docs/specs/common-structures/#integer) Router burst süresi
    (saniye)
8.  Dokuz 4-byte [Integer](/docs/specs/common-structures/#integer) (tanımlanmamış)

#### Notlar

İstemci sınırları ayarlanmış tek değerler olabilir ve gerçek router sınırları, router sınırlarının bir yüzdesi veya belirli istemciye özgü olabilir, uygulama bağımlıdır. Router sınırları olarak etiketlenen tüm değerler 0 olabilir, uygulama bağımlıdır. 0.7.2 sürümü itibariyle.

### BlindingInfoMessage {#BlindingInfoMessage}

#### Açıklama

Router'a bir Destination'ın gizlendiğini, isteğe bağlı arama parolası ve şifre çözme için isteğe bağlı özel anahtar ile bildirin. Detaylar için 123 ve 149 numaralı önerilere bakın.

Router'ın bir hedefin blinded (köreltilmiş) olup olmadığını bilmesi gerekir. Eğer blinded ise ve gizli ya da müşteri başına kimlik doğrulama kullanıyorsa, bu bilgilere de sahip olması gerekir.

Yeni format b32 adresinin ("b33") Host Lookup işlemi, router'a adresin köreltildiğini bildirir, ancak Host Lookup mesajında gizli anahtarı veya özel anahtarı router'a iletecek bir mekanizma yoktur. Host Lookup mesajını bu bilgiyi eklemek için genişletebilsek de, yeni bir mesaj tanımlamak daha temizdir.

Bu mesaj, istemcinin router'a söylemesi için programatik bir yol sağlar. Aksi takdirde, kullanıcının her hedefi manuel olarak yapılandırması gerekir.

#### Kullanım

Bir istemci, körleştirilmiş hedefe mesaj göndermeden önce, "b33"ü bir Host Lookup mesajında aramalı veya bir Blinding Info mesajı göndermelidir. Körleştirilmiş hedef bir sır veya istemci başına kimlik doğrulama gerektiriyorsa, istemci bir Blinding Info mesajı göndermelidir.

Router bu mesaja yanıt göndermez. İstemciden Router'a gönderilir.

#### İçindekiler

1.  [Oturum Kimliği](#struct-sessionid)
2.  1 bayt [Integer](/docs/specs/common-structures/#integer) Bayrakları

> - Bit sırası: 76543210 > - Bit 0: herkes için 0, istemci başına için 1 > - Bit 3-1: Kimlik doğrulama şeması, eğer bit 0 istemci başına için >   1'e ayarlanmışsa, aksi halde 000 >   - 000: DH istemci kimlik doğrulaması (veya istemci başına kimlik doğrulama yok) >   - 001: PSK istemci kimlik doğrulaması > - Bit 4: gizli anahtar gerekiyorsa 1, gizli anahtar gerekmiyorsa 0 > - Bit 7-5: Kullanılmamış, gelecekteki uyumluluk için 0'a ayarlanmış

3.  1 bayt [Integer](/docs/specs/common-structures/#integer) Endpoint türü

> - Tip 0 bir [Hash](/docs/specs/common-structures/#hash)'dir > - Tip 1 bir hostname [String](/docs/specs/common-structures/#string)'dir > - Tip 2 bir [Destination](/docs/specs/common-structures/#destination)'dır > - Tip 3 bir Sig Type ve >   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)'dir

4.  2 byte [Integer](/docs/specs/common-structures/#integer) Blinded İmza Türü
5.  4 byte [Integer](/docs/specs/common-structures/#integer) Epoch'tan itibaren Son Kullanma Saniyeleri
6.  Endpoint: Belirtildiği gibi veri, şunlardan biri

> - Tip 0: 32 byte [Hash](/docs/specs/common-structures/#hash) > > - Tip 1: host adı [String](/docs/specs/common-structures/#string) > > - Tip 2: ikili [Destination](/docs/specs/common-structures/#destination) > >  > >  - Tip 3: 2 byte [Integer](/docs/specs/common-structures/#integer) imza tipi, ardından > >  -   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) (uzunluk >       imza tipine göre belirlenir)

7.  [PrivateKey](/docs/specs/common-structures/#privatekey) Şifre çözme anahtarı Yalnızca
    bayrak biti 0, 1 olarak ayarlandığında mevcut. 32 baytlık ECIES_X25519 özel anahtarı,
    little-endian
8.  [String](/docs/specs/common-structures/#string) Arama Şifresi Yalnızca
    bayrak biti 4, 1 olarak ayarlandığında mevcut.

#### Notlar

- 0.9.43 sürümü itibariyle.
- Hash endpoint türü muhtemelen faydalı değildir, router adres defterinde ters arama yaparak Destination'ı alamadığı sürece.
- Hostname endpoint türü muhtemelen faydalı değildir, router adres defterinde arama yaparak Destination'ı alamadığı sürece.

### CreateLeaseSetMessage {#CreateLeaseSetMessage}

KULLANIMI TERCİH EDİLMEZ. LeaseSet2, çevrimdışı anahtarlar, ElGamal olmayan şifreleme türleri, çoklu şifreleme türleri veya şifrelenmiş LeaseSet'ler için kullanılamaz. Tüm router'larda 0.9.39 veya daha yüksek sürümlerle CreateLeaseSet2Message kullanın.

#### Açıklama

Bu mesaj bir [RequestLeaseSetMessage](#RequestLeaseSetMessage) veya [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) yanıtı olarak gönderilir ve I2NP Ağ Veritabanına yayınlanması gereken tüm [Lease](/docs/specs/common-structures/#lease) yapılarını içerir.

İstemciden Router'a gönderildi.

#### İçindekiler

1.  [Session ID](#struct-sessionid)
2.  DSA [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) veya 20
    bayt yoksayıldı
3.  [PrivateKey](/docs/specs/common-structures/#privatekey)
4.  [LeaseSet](/docs/specs/common-structures/#leaseset)

#### Notlar

SigningPrivateKey, yalnızca signing key türü DSA ise LeaseSet içindeki [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) ile eşleşir. Bu, LeaseSet iptali için kullanılır, ancak bu özellik uygulanmamıştır ve büyük olasılıkla hiçbir zaman uygulanmayacaktır. Signing key türü DSA değilse, bu alan 20 byte rastgele veri içerir. Bu alanın uzunluğu her zaman 20 byte'tır, DSA olmayan bir signing private key'in uzunluğuna hiçbir zaman eşit olmaz.

PrivateKey, LeaseSet'ten gelen [PublicKey](/docs/specs/common-structures/#publickey) ile eşleşir. PrivateKey, garlic encryption ile yönlendirilmiş mesajları şifrelemek için gereklidir.

İptal işlevi uygulanmamıştır. Herhangi bir istemci kütüphanesinde birden fazla router'a bağlantı uygulanmamıştır.

### CreateLeaseSet2Message {#CreateLeaseSet2Message}

#### Açıklama

Bu mesaj bir [RequestLeaseSetMessage](#RequestLeaseSetMessage) veya [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) yanıtı olarak gönderilir ve I2NP Ağ Veritabanına yayınlanması gereken tüm [Lease](/docs/specs/common-structures/#lease) yapılarını içerir.

Client'tan Router'a gönderilir. 0.9.39 sürümünden beri. EncryptedLeaseSet için client başına kimlik doğrulama 0.9.41 sürümünden itibaren desteklenmektedir. MetaLeaseSet henüz I2CP aracılığıyla desteklenmemektedir. Daha fazla bilgi için öneri 123'e bakınız.

#### İçindekiler

1.  [Session ID](#struct-sessionid)
2.  Takip eden lease set'in bir byte türü.

> - Tip 1 bir [LeaseSet](/docs/specs/common-structures/#leaseset)'tir (kullanımdan kaldırıldı) > - Tip 3 bir [LeaseSet2](/docs/specs/common-structures/#leaseset2)'dir > - Tip 5 bir [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)'tir > - Tip 7 bir [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)'tir

3.  [LeaseSet](/docs/specs/common-structures/#leaseset) veya
    [LeaseSet2](/docs/specs/common-structures/#leaseset2) veya
    [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) veya
    [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
4.  Takip edecek özel anahtar sayısını belirten bir bayt.
5.  [PrivateKey](/docs/specs/common-structures/#privatekey) listesi. lease set'teki her genel anahtar için bir tane, aynı sırada. (Meta LS2 için mevcut değil)

> - Şifreleme türü (2 bayt [Integer](/docs/specs/common-structures/#integer)) > - Şifreleme anahtarı uzunluğu (2 bayt [Integer](/docs/specs/common-structures/#integer)) > - Şifreleme [PrivateKey](/docs/specs/common-structures/#privatekey) (belirtilen >   bayt sayısı)

#### Notlar

PrivateKeys, LeaseSet'teki [PublicKey](/docs/specs/common-structures/#publickey)'lerin her biriyle eşleşir. PrivateKeys, garlic routed mesajların şifresini çözmek için gereklidir.

Encrypted LeaseSet'ler hakkında daha fazla bilgi için 123 numaralı öneriyi görün.

MetaLeaseSet için içerik ve format geçici niteliktedir ve değişebilir. Birden fazla router'ın yönetimi için belirlenmiş bir protokol bulunmamaktadır. Daha fazla bilgi için 123 numaralı öneriyi inceleyin.

Daha önce iptal için tanımlanmış ve kullanılmamış olan imzalama özel anahtarı, LS2'de mevcut değildir.

Mesaj tipi 40 ile ön sürüm 0.9.38'de bulunuyordu ancak format değiştirildi. Tip 40 terk edildi ve desteklenmiyor. Tip 41, 0.9.39'a kadar geçerli değil.

### CreateSessionMessage {#CreateSessionMessage}

#### Açıklama

Bu mesaj, bir oturumu başlatmak için bir istemciden gönderilir; burada oturum, tek bir Destination'ın ağa bağlantısı olarak tanımlanır ve bu Destination için tüm mesajlar bu bağlantıya teslim edilecek ve bu Destination'ın diğer herhangi bir Destination'a gönderdiği tüm mesajlar bu bağlantı üzerinden gönderilecektir.

İstemciden Router'a gönderilir. Router bir [SessionStatusMessage](#SessionStatusMessage) ile yanıtlar.

#### İçindekiler

1.  [Oturum Yapılandırması](#struct-sessionconfig)

#### Notlar

- Bu, istemci tarafından gönderilen ikinci mesajdır. Daha önce istemci
  bir [GetDateMessage](#GetDateMessage) gönderdi ve bir
  [SetDateMessage](#SetDateMessage) yanıtı aldı.
- Session Config içindeki Tarih, router'ın mevcut zamanından çok uzaksa (+/- 30
  saniyeden fazla), oturum reddedilecektir.
- Bu Destination için router'da zaten bir oturum varsa,
  oturum reddedilecektir.
- Session Config içindeki [Mapping](/docs/specs/common-structures/#mapping), imzanın
  router'da doğru şekilde doğrulanabilmesi için anahtar bazında sıralanmış olmalıdır.

### DestLookupMessage {#DestLookupMessage}

#### Açıklama

Client'tan Router'a gönderilir. Router bir [DestReplyMessage](#DestReplyMessage) ile yanıt verir.

#### İçindekiler

1.  SHA-256 [Hash](/docs/specs/common-structures/#hash)

#### Notlar

0.7 sürümü itibarıyla.

0.8.3 sürümünden itibaren, birden fazla bekleyen arama desteklenmekte ve aramalar hem I2PSimpleSession'da hem de standart oturumlarda desteklenmektedir.

[HostLookupMessage](#HostLookupMessage) 0.9.11 sürümünden itibaren tercih edilir.

### DestReplyMessage {#DestReplyMessage}

#### Açıklama

Router'dan Client'a bir [DestLookupMessage](#DestLookupMessage)'a yanıt olarak gönderilir.

#### İçindekiler

1.  Başarı durumunda [Destination](/docs/specs/common-structures/#destination), veya
    başarısızlık durumunda [Hash](/docs/specs/common-structures/#hash)

#### Notlar

0.7 sürümü itibariyle.

0.8.3 sürümünden itibaren, arama başarısız olursa istenen Hash döndürülür, böylece istemci birden fazla bekleyen arama yapabilir ve yanıtları aramalarla ilişkilendirebilir. Bir Destination yanıtını bir istekle ilişkilendirmek için Destination'ın Hash'ini alın. 0.8.3 sürümünden önce, başarısızlık durumunda yanıt boştu.

### DestroySessionMessage {#DestroySessionMessage}

#### Açıklama

Bu mesaj, bir oturumu sonlandırmak için istemciden gönderilir.

Client'tan router'a gönderilir. Router bir [SessionStatusMessage](#SessionStatusMessage) (Destroyed) ile yanıt vermelidir. Ancak, aşağıdaki önemli notlara bakın.

#### İçindekiler

1.  [Oturum ID](#struct-sessionid)

#### Notlar

Bu noktada router, oturumla ilgili tüm kaynakları serbest bırakmalıdır.

API 0.9.66 aracılığıyla, Java I2P router ve istemci kütüphaneleri bu spesifikasyondan önemli ölçüde sapma gösterir. Router hiçbir zaman SessionStatus(Destroyed) yanıtı göndermez. Hiç oturum kalmadığında, bir [DisconnectMessage](#DisconnectMessage) gönderir. Alt oturumlar varsa veya birincil oturum devam ediyorsa, yanıt vermez.

Java client kütüphanesi SessionStatus mesajına tüm oturumları yok ederek ve yeniden bağlanarak yanıt verir.

Birden fazla oturuma sahip bir bağlantıda tekil alt oturumları yok etme işlevi, çeşitli router ve istemci uygulamalarında tam olarak test edilmemiş veya çalışmıyor olabilir. Dikkatli olun.

Uygulamalar bir birincil oturum için destroy komutunu tüm alt oturumlar için destroy komutu olarak ele almalı, ancak tek bir alt oturum için destroy komutuna izin vermeli ve bağlantıyı açık tutmalıdır, fakat Java I2P şu anda bunu yapmamaktadır. Eğer Java I2P davranışı sonraki sürümlerde değiştirilirse, burada belgelenecektir.

### DisconnectMessage {#DisconnectMessage}

#### Açıklama

Diğer tarafa sorun olduğunu ve mevcut bağlantının yok edilmek üzere olduğunu bildirir. Bu, o bağlantıdaki tüm oturumları sonlandırır. Soket kısa süre içinde kapatılacaktır. Router'dan istemciye veya istemciden router'a gönderilebilir.

#### İçindekiler

1.  Sebep [String](/docs/specs/common-structures/#string)

#### Notlar

Yalnızca router-to-client yönünde uygulanmıştır, en azından Java I2P'de.

### GetBandwidthLimitsMessage {#GetBandwidthLimitsMessage}

#### Açıklama

Router'ın mevcut bant genişliği limitlerinin ne olduğunu belirtmesini talep et.

Client'tan Router'a gönderilir. Router bir [BandwidthLimitsMessage](#BandwidthLimitsMessage) ile yanıtlar.

#### İçindekiler

*Hiçbiri*

#### Notlar

0.7.2 sürümü itibarıyla.

0.8.3 sürümünden itibaren, hem I2PSimpleSession'da hem de standart oturumlarda desteklenmektedir.

### GetDateMessage {#GetDateMessage}

#### Açıklama

Client'tan Router'a gönderilir. Router bir [SetDateMessage](#SetDateMessage) ile yanıt verir.

#### İçindekiler

1.  I2CP API Sürümü [String](/docs/specs/common-structures/#string)
2.  Kimlik Doğrulama [Mapping](/docs/specs/common-structures/#mapping) (isteğe bağlı, 0.9.11 sürümünden itibaren)

#### Notlar

- Genellikle protocol sürüm byte'ını gönderdikten sonra istemci tarafından gönderilen ilk mesaj.
- Sürüm dizesi 0.8.7 sürümünden itibaren dahil edilmiştir. Bu sadece istemci ve router aynı JVM'de değilse yararlıdır. Eğer mevcut değilse, istemci 0.8.6 sürümü veya daha eskidir.
- 0.9.11 sürümünden itibaren, kimlik doğrulama [Mapping](/docs/specs/common-structures/#mapping)'i i2cp.username ve i2cp.password anahtarları ile dahil edilebilir. Bu mesaj imzalanmadığı için Mapping'in sıralanması gerekmez. 0.9.10 dahil ve öncesinde, kimlik doğrulama [Session Config](#struct-sessionconfig) Mapping'inde dahil edilir ve [GetDateMessage](#GetDateMessage), [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage) veya [DestLookupMessage](#DestLookupMessage) için hiçbir kimlik doğrulama zorlanmaz. Etkinleştirildiğinde, 0.9.16 sürümünden itibaren [GetDateMessage](#GetDateMessage) aracılığıyla kimlik doğrulama diğer tüm mesajlardan önce gereklidir. Bu sadece router bağlamı dışında yararlıdır. Bu uyumsuz bir değişikliktir, ancak sadece kimlik doğrulamalı router bağlamı dışındaki oturumları etkileyecektir ki bu nadir olmalıdır.

### HostLookupMessage {#HostLookupMessage}

#### Açıklama

Client'tan Router'a gönderilir. Router bir [HostReplyMessage](#HostReplyMessage) ile yanıtlar.

Bu, [DestLookupMessage](#DestLookupMessage) yerine geçer ve bir istek kimliği, zaman aşımı ve ana bilgisayar adı arama desteği ekler. Hash aramalarını da desteklediği için, router bunu destekliyorsa tüm aramalar için kullanılabilir. Ana bilgisayar adı aramaları için router, kendi bağlamındaki adlandırma hizmetini sorgulayacaktır. Bu yalnızca client, router bağlamının dışındaysa yararlıdır. Router bağlamının içinde, client'ın adlandırma hizmetini kendisi sorgulaması çok daha verimlidir.

#### İçindekiler

1.  [Session ID](#struct-sessionid)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) istek ID'si
3.  4 byte [Integer](/docs/specs/common-structures/#integer) zaman aşımı (ms)
4.  1 byte [Integer](/docs/specs/common-structures/#integer) istek türü
5.  SHA-256 [Hash](/docs/specs/common-structures/#hash) veya host adı
    [String](/docs/specs/common-structures/#string) veya
    [Destination](/docs/specs/common-structures/#destination)

İstek türleri:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Lookup key (item 5)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As of</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
</table>
Tip 2-4, LeaseSet'ten gelen seçenekler eşlemesinin HostReply mesajında döndürülmesini talep eder. Öneri 167'ye bakın.

#### Notlar

- 0.9.11 sürümünden itibaren. Eski router'lar için [DestLookupMessage](#DestLookupMessage) kullanın.
- Oturum ID'si ve istek ID'si [HostReplyMessage](#HostReplyMessage) içinde döndürülecektir. Oturum yoksa oturum ID'si için 0xFFFF kullanın.
- Zaman aşımı Hash aramaları için faydalıdır. Önerilen minimum 10,000 (10 saniye). Gelecekte uzak adlandırma hizmeti aramaları için de faydalı olabilir. Değer, hızlı olması gereken yerel ana bilgisayar adı aramaları için dikkate alınmayabilir.
- Base 32 ana bilgisayar adı araması desteklenir ancak önce Hash'e dönüştürmek tercih edilir.

### HostReplyMessage {#HostReplyMessage}

#### Açıklama

Router tarafından Client'a [HostLookupMessage](#HostLookupMessage) yanıtı olarak gönderilir.

#### İçindekiler

1.  [Session ID](#struct-sessionid)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) istek ID'si
3.  1 byte [Integer](/docs/specs/common-structures/#integer) sonuç kodu

> - 0: Başarılı > - 1: Başarısız > - 2: Arama parolası gerekli (0.9.43 sürümünden itibaren) > - 3: Özel anahtar gerekli (0.9.43 sürümünden itibaren) > - 4: Arama parolası ve özel anahtar gerekli (0.9.43 sürümünden itibaren) > - 5: Leaseset şifre çözme hatası (0.9.43 sürümünden itibaren) > - 6: Leaseset arama hatası (0.9.66 sürümünden itibaren) > - 7: Arama türü desteklenmiyor (0.9.66 sürümünden itibaren)

4.  [Destination](/docs/specs/common-structures/#destination), yalnızca sonuç
    kodu sıfır ise mevcut, ancak arama türleri 2-4 için de döndürülebilir. Aşağıya
    bakınız.
5.  [Mapping](/docs/specs/common-structures/#mapping), yalnızca sonuç kodu
    sıfır ise mevcut, yalnızca arama türleri 2-4 için döndürülür. 0.9.66 itibariyle. Aşağıya bakınız.

#### Arama türleri 2-4 için yanıtlar

Proposal 167, eğer varsa leaseset'ten tüm seçenekleri döndüren ek arama türlerini tanımlar. Arama türleri 2-4 için, arama anahtarı adres defterinde olsa bile router leaseset'i getirmek zorundadır.

Başarılı olması durumunda, HostReply leaseset'ten gelen Mapping seçeneklerini içerecek ve bunu destination'dan sonra 5. öğe olarak dahil edecektir. Mapping'te hiç seçenek yoksa veya leaseset sürüm 1 ise, yine de boş bir Mapping olarak dahil edilecektir (iki bayt: 0 0). Sadece hizmet kaydı seçenekleri değil, leaseset'teki tüm seçenekler dahil edilecektir. Örneğin, gelecekte tanımlanacak parametreler için seçenekler mevcut olabilir. Döndürülen Mapping sıralanmış olabilir veya olmayabilir, bu uygulama bağımlıdır.

LeaseSet arama başarısızlığında, yanıt yeni bir hata kodu 6 (LeaseSet arama başarısızlığı) içerecek ve bir eşleme içermeyecektir. Hata kodu 6 döndürüldüğünde, Destination alanı mevcut olabilir veya olmayabilir. Adres defterinde hostname araması başarılı olduğunda, önceki bir arama başarılı olup sonuç önbelleğe alındığında veya arama mesajında Destination mevcut olduğunda (arama türü 4) bu alan mevcut olacaktır.

Bir arama türü desteklenmiyorsa, yanıt yeni bir hata kodu 7 (arama türü desteklenmiyor) içerecektir.

#### Notlar

- 0.9.11 sürümü itibariyle. [HostLookupMessage](#HostLookupMessage)
  notlarına bakın.
- Session ID ve request ID, [HostLookupMessage](#HostLookupMessage)'dan
  gelenlerin aynısıdır.
- Sonuç kodu başarı için 0, başarısızlık için 1-255'tir. 1 genel bir
  başarısızlığı gösterir. 0.9.43 itibariyle, "b33" aramalar için genişletilmiş
  hataları desteklemek üzere ek başarısızlık kodları 2-5 tanımlandı. Ek
  bilgi için 123 ve 149 numaralı önerilere bakın. 0.9.66 itibariyle, tip 2-4
  aramalar için genişletilmiş hataları desteklemek üzere ek başarısızlık
  kodları 6-7 tanımlandı. Ek bilgi için 167 numaralı öneriye bakın.

### MessagePayloadMessage {#MessagePayloadMessage}

#### Açıklama

Bir mesajın yükünü istemciye ilet.

Router'dan İstemci'ye gönderilir. Eğer i2cp.fastReceive=true ise (ki bu varsayılan değil), istemci bir [ReceiveMessageEndMessage](#ReceiveMessageEndMessage) ile yanıt verir.

#### İçindekiler

1.  [Oturum Kimliği](#struct-sessionid)
2.  [Mesaj Kimliği](#struct-messageid)
3.  [Yük](#struct-payload)

#### Notlar

### MessageStatusMessage {#MessageStatusMessage}

#### Açıklama

Gelen veya giden bir mesajın teslimat durumunu istemciye bildir. Router'dan İstemciye gönderilir. Bu mesaj gelen bir mesajın mevcut olduğunu belirtiyorsa, istemci bir [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) ile yanıt verir. Giden bir mesaj için, bu bir [SendMessageMessage](#SendMessageMessage) veya [SendMessageExpiresMessage](#SendMessageExpiresMessage) için bir yanıttır.

#### İçindekiler

1.  [Session ID](#struct-sessionid)
2.  Router tarafından oluşturulan [Message ID](#struct-messageid)
3.  1 byte [Integer](/docs/specs/common-structures/#integer) durum
4.  4 byte [Integer](/docs/specs/common-structures/#integer) boyut
5.  İstemci tarafından daha önce oluşturulan 4 byte [Integer](/docs/specs/common-structures/#integer) nonce

#### Notlar

Sürüm 0.9.4'e kadar, bilinen durum değerleri şunlardır: mesaj mevcut için 0, kabul edildi için 1, en iyi çaba başarılı için 2, en iyi çaba başarısız için 3, garantili başarılı için 4, garantili başarısız için 5. Size Integer mevcut mesajın boyutunu belirtir ve yalnızca status = 0 için geçerlidir. Garantili mod henüz uygulanmamış olmasına rağmen (en iyi çaba tek hizmet olmasına rağmen), mevcut router implementasyonu en iyi çaba kodları değil, garantili durum kodlarını kullanır.

Router sürüm 0.9.5 itibariyle, ek durum kodları tanımlanmıştır, ancak bunlar mutlaka uygulanmış değildir. Ayrıntılar için [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html) sayfasına bakınız. Giden mesajlar için, 1, 2, 4 ve 6 kodları başarıyı gösterir; diğer tüm kodlar başarısızlıktır. Döndürülen başarısızlık kodları değişiklik gösterebilir ve uygulamaya özgüdür.

Tüm durum kodları:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Available</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DEPRECATED. For incoming messages only. All other status codes below are for outgoing messages. The included size is the size in bytes of the available message. This is unused in "fast receive" mode, which is the default as of release 0.9.4.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Accepted</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outgoing message accepted by the local router for delivery. The included nonce matches the nonce in the <a href="#SendMessageMessage">SendMessageMessage</a>, and the included Message ID will be used for subsequent success or failure notification.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success (unused)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable failure</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generic failure, specific cause unknown. May not really be a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery successful. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery failure. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local router is not ready, has shut down, or has major problems. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Network Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local computer apparently has no network connectivity at all. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Session</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The I2CP session is invalid or closed. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Message</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message payload is invalid or zero-length or too big. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Options</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is invalid in the message options, or the expiration is in the past or too far in the future. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">13</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Overflow Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Some queue or buffer in the router is full and the message was dropped. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Expired</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message expired before it could be sent. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Local Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The client has not yet signed a <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>, or the local keys are invalid, or it has expired, or it does not have any tunnels in it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Local Tunnels</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local problems. No outbound tunnel to send through, or no inbound tunnel if a reply is required. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unsupported Encryption</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The certs or options in the <a href="/docs/specs/common-structures/#destination">Destination</a> or its <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> indicate that it uses an encryption format that we don't support, so we can't talk to it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is wrong with the far-end <a href="/docs/specs/common-structures/#destination">Destination</a>. Bad format, unsupported options, certificates, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but something strange is wrong with it. Unsupported options or certificates, no tunnels, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expired Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but it's expired and we can't get a new one. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Could not find the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>. This is a common failure, equivalent to a DNS lookup failure. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Meta Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The far-end destination's lease set was a meta lease set, and cannot be sent to. The client should request the meta lease set's contents with a HostLookupMessage, and select one of the hashes contained within to look up and send to. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Loopback Denied</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message was attempted to be sent from and to the same destination or session. This is a guaranteed failure.</td>
</tr>
</table>
Status = 1 (kabul edildi) olduğunda, nonce [SendMessageMessage](#SendMessageMessage) içindeki nonce ile eşleşir ve dahil edilen Message ID sonraki başarı veya başarısızlık bildirimleri için kullanılacaktır. Aksi takdirde, nonce yok sayılabilir.

### ReceiveMessageBeginMessage {#ReceiveMessageBeginMessage}

KULLANIM DIŞI. i2pd tarafından desteklenmiyor.

#### Açıklama

Router'dan önceden bildirilmiş bir mesajı teslim etmesini talep et. İstemciden Router'a gönderilir. Router bir [MessagePayloadMessage](#MessagePayloadMessage) ile yanıt verir.

#### İçindekiler

1.  [Oturum Kimliği](#struct-sessionid)
2.  [Mesaj Kimliği](#struct-messageid)

#### Notlar

[ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage), yeni bir mesajın alınmaya hazır olduğunu belirten bir [MessageStatusMessage](#MessageStatusMessage)'a yanıt olarak gönderilir. Eğer [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage)'da belirtilen mesaj kimliği geçersiz veya yanlışsa, router basitçe yanıt vermeyebilir veya bir [DisconnectMessage](#DisconnectMessage) geri gönderebilir.

Bu, 0.9.4 sürümünden itibaren varsayılan olan "hızlı alma" modunda kullanılmaz.

### ReceiveMessageEndMessage {#ReceiveMessageEndMessage}

KULLANIM DIŞI. i2pd tarafından desteklenmiyor.

#### Açıklama

Router'a bir mesajın başarıyla teslim edildiğini ve router'ın mesajı silebileceğini bildirin.

İstemciden Router'a gönderilir.

#### İçindekiler

1.  [Oturum Kimliği](#struct-sessionid)
2.  [Mesaj Kimliği](#struct-messageid)

#### Notlar

[ReceiveMessageEndMessage](#ReceiveMessageEndMessage), bir [MessagePayloadMessage](#MessagePayloadMessage) bir mesajın yükünü tamamen teslim ettikten sonra gönderilir.

Bu, 0.9.4 sürümünden itibaren varsayılan olan "hızlı alma" modunda kullanılmamaktadır.

### ReconfigureSessionMessage {#ReconfigureSessionMessage}

#### Açıklama

İstemciden router'a oturum yapılandırmasını güncellemek için gönderilir. Router bir [SessionStatusMessage](#SessionStatusMessage) ile yanıt verir.

#### İçindekiler

1.  [Oturum ID](#struct-sessionid)
2.  [Oturum Yapılandırması](#struct-sessionconfig)

#### Notlar

- 0.7.1 sürümü itibariyle.
- Session Config içindeki Date, router'ın mevcut zamanından çok uzaksa (30 saniyeden fazla +/- fark), session reddedilecektir.
- Session Config içindeki [Mapping](/docs/specs/common-structures/#mapping), signature'ın router'da doğru şekilde doğrulanması için anahtara göre sıralanmış olmalıdır.
- Bazı konfigürasyon seçenekleri yalnızca [CreateSessionMessage](#CreateSessionMessage) içinde ayarlanabilir ve buradaki değişiklikler router tarafından tanınmayacaktır. tunnel seçenekleri inbound.\* ve outbound.\* değişiklikleri her zaman tanınır.
- Genel olarak, router güncellenmiş config'i mevcut config ile birleştirmeli, böylece güncellenmiş config yalnızca yeni veya değiştirilmiş seçenekleri içermesi yeterli. Ancak birleştirme nedeniyle, seçenekler bu şekilde kaldırılamaz; açıkça istenen varsayılan değere ayarlanmalıdır.

### ReportAbuseMessage {#ReportAbuseMessage}

KULLANIM DIŞI, KULLANILMIYOR, DESTEKLENMİYOR

#### Açıklama

Diğer tarafa (istemci veya router) saldırı altında olduklarını, potansiyel olarak belirli bir MessageId referansıyla birlikte bildirin. Eğer router saldırı altındaysa, istemci başka bir router'a geçmeye karar verebilir ve eğer bir istemci saldırı altındaysa, router kendi router'larını yeniden oluşturabilir veya saldırıyı ileten mesajları gönderen bazı peer'ları yasaklı listesine alabilir.

Router'dan istemciye veya istemciden router'a gönderilir.

#### İçindekiler

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) kötüye kullanım şiddeti (0 minimal kötüye kullanım, 255 son derece kötüye kullanım)
3.  Sebep [String](/docs/specs/common-structures/#string)
4.  [Message ID](#struct-messageid)

#### Notlar

Kullanılmıyor. Tam olarak uygulanmamış. Hem router hem de istemci bir [ReportAbuseMessage](#ReportAbuseMessage) oluşturabilir, ancak hiçbirinin mesaj alındığında bunu işleyecek bir işleyicisi yoktur.

### RequestLeaseSetMessage {#RequestLeaseSetMessage}

KULLANIM DIŞI. i2pd tarafından desteklenmiyor. Java I2P tarafından 0.9.7 veya daha yüksek sürümdeki istemcilere gönderilmiyor (2013-07). RequestVariableLeaseSetMessage kullanın.

#### Açıklama

Bir istemcinin belirli bir gelen tunnel kümesinin dahil edilmesini yetkilendirmesini talep eder. Router'dan İstemciye gönderilir. İstemci bir [CreateLeaseSetMessage](#CreateLeaseSetMessage) ile yanıt verir.

Bir oturum üzerinde gönderilen bu mesajların ilki, tunnel'ların oluşturulduğu ve trafik için hazır olduğuna dair istemciye bir sinyaldir. Router, en az bir gelen VE bir giden tunnel oluşturulana kadar bu mesajların ilkini göndermemelidir. İstemciler, bu mesajların ilki belirli bir süre sonra alınmadığında oturumu zaman aşımına uğratıp yok etmelidir (önerilen: 5 dakika veya daha fazla).

#### İçindekiler

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) tunnel sayısı
3.  O kadar sayıda çift:
    1.  [Hash](/docs/specs/common-structures/#hash)
    2.  [TunnelId](/docs/specs/common-structures/#tunnelid)
4.  Bitiş [Date](/docs/specs/common-structures/#date)

#### Notlar

Bu, tüm [Lease](/docs/specs/common-structures/#lease) girişleri aynı anda sona erecek şekilde ayarlanmış bir [LeaseSet](/docs/specs/common-structures/#leaseset) talep eder. İstemci sürümü 0.9.7 veya daha yüksek olan durumlar için [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) kullanılır.

### RequestVariableLeaseSetMessage {#RequestVariableLeaseSetMessage}

#### Açıklama

Bir istemcinin belirli bir gelen tunnel kümesinin dahil edilmesini yetkilendirmesini talep edin.

Router'dan Client'a gönderilir. Client bir [CreateLeaseSetMessage](#CreateLeaseSetMessage) veya [CreateLeaseSet2Message](#CreateLeaseSet2Message) ile yanıtlar.

Bir oturumda gönderilen bu mesajların ilki, tunnel'ların kurulduğunu ve trafiğe hazır olduğunu istemciye bildiren bir sinyaldir. Router, en az bir gelen VE bir giden tunnel kurulana kadar bu mesajların ilkini göndermemelidir. İstemciler, bu mesajların ilki belirli bir süre sonra alınmazsa oturumu sonlandırıp yok etmelidir (önerilen: 5 dakika veya daha fazla).

#### İçindekiler

1.  [Oturum ID'si](#struct-sessionid)
2.  1 bayt [Tamsayı](/docs/specs/common-structures/#integer) tunnel sayısı
3.  O kadar [Kira](/docs/specs/common-structures/#lease) girişi

#### Notlar

Bu, her [Lease](/docs/specs/common-structures/#lease) için ayrı bir son kullanma süresi olan bir [LeaseSet](/docs/specs/common-structures/#leaseset) talep eder.

0.9.7 sürümü itibariyle. Bu sürümden önceki istemciler için [RequestLeaseSetMessage](#RequestLeaseSetMessage) kullanın.

### SendMessageMessage {#SendMessageMessage}

#### Açıklama

Bu, bir istemcinin [Destination](/docs/specs/common-structures/#destination)'a bir mesaj (payload) gönderme şeklidir. Router varsayılan bir son kullanma tarihi kullanacaktır.

İstemciden Router'a gönderilir. Router bir [MessageStatusMessage](#MessageStatusMessage) ile yanıt verir.

#### İçindekiler

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 bayt [Integer](/docs/specs/common-structures/#integer) nonce

#### Notlar

[SendMessageMessage](#SendMessageMessage) tamamen sağlam bir şekilde ulaştığı anda, router teslim için kabul edildiğini belirten bir [MessageStatusMessage](#MessageStatusMessage) döndürmelidir. Bu mesaj burada gönderilen aynı nonce'ı içerecektir. Daha sonra, oturum yapılandırmasının teslim garantilerine bağlı olarak, router ek olarak durumu güncelleyen başka bir [MessageStatusMessage](#MessageStatusMessage) gönderebilir.

0.8.1 sürümünden itibaren, router eğer i2cp.messageReliability=none ise [MessageStatusMessage](#MessageStatusMessage) göndermez.

0.9.4 sürümünden önce, nonce değeri 0'a izin verilmiyordu. 0.9.4 sürümü itibariyle, nonce değeri 0'a izin verilmekte olup, router'a hiçbir [MessageStatusMessage](#MessageStatusMessage) göndermemesi gerektiğini bildirmektedir, yani sadece bu mesaj için i2cp.messageReliability=none ayarı varmış gibi davranır.

0.9.14 sürümünden önce, i2cp.messageReliability=none ayarlı bir oturumda mesaj bazında geçersiz kılma yapılamıyordu. 0.9.14 sürümü itibariyle, i2cp.messageReliability=none ayarlı bir oturumda, istemci nonce değerini sıfır olmayan bir değere ayarlayarak teslimat başarısı veya başarısızlığı ile birlikte bir [MessageStatusMessage](#MessageStatusMessage) teslimi talep edebilir. Router "kabul edildi" [MessageStatusMessage](#MessageStatusMessage) göndermeyecek ancak daha sonra istemciye aynı nonce ile birlikte başarı veya başarısızlık değeri içeren bir [MessageStatusMessage](#MessageStatusMessage) gönderecektir.

### SendMessageExpiresMessage {#SendMessageExpiresMessage}

#### Açıklama

Client'tan Router'a gönderilir. [SendMessageMessage](#SendMessageMessage) ile aynı, ancak sona erme süresi ve seçenekleri içerir.

#### İçindekiler

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) nonce
5.  2 byte bayrak (seçenekler)
6.  8 byte'tan 6 byte'a kısaltılmış Sona Erme [Date](/docs/specs/common-structures/#date)

#### Notlar

0.7.1 sürümü itibariyle.

"Best effort" modunda, SendMessageExpiresMessage tamamen bozulmadan ulaştığı anda, router bunun teslimat için kabul edildiğini belirten bir MessageStatusMessage döndürmelidir. Bu mesaj burada gönderilen aynı nonce'u içerecektir. Daha sonra, oturum yapılandırmasının teslimat garantilerine bağlı olarak, router ek olarak durumu güncelleyen başka bir MessageStatusMessage gönderebilir.

0.8.1 sürümünden itibaren, router i2cp.messageReliability=none olduğunda Message Status Message göndermiyor.

0.9.4 sürümünden önce, 0 nonce değerine izin verilmiyordu. 0.9.4 sürümü itibariyle, 0 nonce değerine izin verilmekte olup, bu değer router'a herhangi bir Message Status Message göndermemesi gerektiğini bildirir, yani sadece bu mesaj için i2cp.messageReliability=none ayarı gibi davranır.

0.9.14 sürümünden önce, i2cp.messageReliability=none olan bir oturum mesaj bazında geçersiz kılınamazdı. 0.9.14 sürümü itibariyle, i2cp.messageReliability=none olan bir oturumda, istemci nonce değerini sıfırdan farklı bir değere ayarlayarak teslimat başarısı veya başarısızlığı ile birlikte bir Message Status Message teslimini talep edebilir. Router "kabul edildi" Message Status Message göndermeyecektir ancak daha sonra istemciye aynı nonce ile birlikte başarı veya başarısızlık değeri içeren bir Message Status Message gönderecektir.

#### Flags Alanı

0.8.4 sürümü itibarıyla, Date'in üst iki baytı bayrakları içerecek şekilde yeniden tanımlanmıştır. Bayraklar geriye dönük uyumluluk için varsayılan olarak tüm sıfırlar olmalıdır. Date, 10889 yılına kadar bayraklar alanına müdahale etmeyecektir. Bayraklar, uygulama tarafından router'a LeaseSet ve/veya ElGamal/AES Session Tags'ların mesajla birlikte teslim edilip edilmeyeceği konusunda ipuçları sağlamak için kullanılabilir. Ayarlar, protokol ek yükü miktarını ve mesaj teslim güvenilirliğini önemli ölçüde etkileyecektir. Bireysel bayrak bitleri, 0.9.2 sürümü itibarıyla aşağıdaki gibi tanımlanmıştır. Tanımlar değişebilir. Bayrakları oluşturmak için SendMessageOptions sınıfını kullanın.

Bit sırası: 15...0

Bit 15-11

:   Kullanılmaz, sıfır olmalıdır

Bitler 10-9

:   Mesaj Güvenilirlik Geçersiz Kılma (Uygulanmamış, kaldırılacak).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">00</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use session setting i2cp.messageReliability (default)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">01</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "best effort" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "guaranteed" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unused. Use a nonce value of 0 to force "none" and override a session setting of "best effort" or "guaranteed".</td>
</tr>
</table>
Bit 8

:   Eğer 1 ise, bu mesajla birlikte garlic içinde bir leaseSet paketleme. Eğer

    0, the router may bundle a lease set at its discretion.

Bit 7-4

:   Düşük etiket eşiği. Bu kadar sayıdan az etiket mevcut ise,

    send more. This is advisory and does not force tags to be delivered.
    For ElGamal only. Ignored for ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tag threshold</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">3</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">9</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">14</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">20</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">27</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">35</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">45</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">57</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">72</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">92</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">117</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">147</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">192</td></tr>
</table>
Bit 3-0

:   Gerektiğinde gönderilecek etiket sayısı. Bu tavsiye niteliğindedir ve

    force tags to be delivered. For ElGamal only. Ignored for
    ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tags to send</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">4</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">8</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">12</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">16</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">24</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">32</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">40</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">51</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">64</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">80</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">100</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">125</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">160</td></tr>
</table>
### SessionStatusMessage {#SessionStatusMessage}

#### Açıklama

İstemciyi oturumunun durumu hakkında bilgilendir.

Router'dan Client'a gönderilir, bir [CreateSessionMessage](#CreateSessionMessage), [ReconfigureSessionMessage](#ReconfigureSessionMessage) veya [DestroySessionMessage](#DestroySessionMessage)'a yanıt olarak. [CreateSessionMessage](#CreateSessionMessage)'a yanıt dahil olmak üzere tüm durumlarda, router derhal yanıt vermelidir (tunnel'ların oluşturulmasını beklememelidir).

#### İçindekiler

1.  [Session ID](#struct-sessionid)
2.  1 bayt [Integer](/docs/specs/common-structures/#integer) durumu

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Definition</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destroyed</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The session with the given ID is terminated. May be a response to a <a href="#DestroySessionMessage">DestroySessionMessage</a>.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, a new session with the given ID is now active.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Updated</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, an existing session with the given ID has been reconfigured.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Invalid</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the configuration is invalid. The included session ID should be ignored. In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, the new configuration is invalid for the session with the given ID.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Refused</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the router was unable to create the session, perhaps due to limits being exceeded. The included session ID should be ignored.</td>
</tr>
</table>
#### Notlar

Durum değerleri yukarıda tanımlanmıştır. Durum Created ise, Session ID oturumun geri kalanında kullanılacak tanımlayıcıdır.

### SetDateMessage {#SetDateMessage}

#### Açıklama

Mevcut tarih ve saat. İlk handshake'in bir parçası olarak Router'dan Client'a gönderilir. 0.9.20 sürümünden itibaren, client'ı saat kayması konusunda bilgilendirmek için handshake'den sonra herhangi bir zamanda da gönderilebilir.

#### İçindekiler

1.  [Tarih](/docs/specs/common-structures/#date)
2.  I2CP API Sürümü [String](/docs/specs/common-structures/#string)

#### Notlar

Bu genellikle router tarafından gönderilen ilk mesajdır. Versiyon dizesi 0.8.7 sürümünden itibaren dahil edilmiştir. Bu, yalnızca istemci ve router aynı JVM'de değilse yararlıdır. Mevcut değilse, router 0.8.6 veya daha eski bir sürümdür.

Aynı JVM içindeki istemcilere ek SetDate mesajları gönderilmeyecektir.

## Referanslar

- [Date](/docs/specs/common-structures/#date)
- [Destination](/docs/specs/common-structures/#destination)
- [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Hash](/docs/specs/common-structures/#hash)
- [I2CP Genel Bakış](/docs/specs/i2cp/)
- [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)
- [Integer](/docs/specs/common-structures/#integer)
- [Lease](/docs/specs/common-structures/#lease)
- [LeaseSet](/docs/specs/common-structures/#leaseset)
- [LeaseSet2](/docs/specs/common-structures/#leaseset2)
- [Mapping](/docs/specs/common-structures/#mapping)
- [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
- [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)
- [PrivateKey](/docs/specs/common-structures/#privatekey)
- [PublicKey](/docs/specs/common-structures/#publickey)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SAMv3](/docs/api/samv3/)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [String](/docs/specs/common-structures/#string)
- [TunnelId](/docs/specs/common-structures/#tunnelid)
