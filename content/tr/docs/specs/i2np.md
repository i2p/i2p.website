---
title: "I2P Ağ Protokolü (I2NP)"
description: "Router'lar arası mesaj biçimleri, öncelikler ve I2P içindeki boyut sınırları."
slug: "i2np"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Genel Bakış

I2P Ağ Protokolü (I2NP), router'ların mesajları nasıl alışveriş ettiklerini, taşıma protokollerini nasıl seçtiklerini ve anonimliği korurken trafiği nasıl karıştırdıklarını tanımlar. **I2CP** (istemci API'si) ile taşıma protokolleri (**NTCP2** ve **SSU2**) arasında çalışır.

I2NP, I2P taşıma protokollerinin üstündeki katmandır. Şu amaçlarla kullanılan router'lar arası bir protokoldür: - Ağ veritabanı sorgulamaları ve yanıtları - tunnel oluşturma - Şifrelenmiş router ve istemci veri iletileri

I2NP mesajları başka bir router'a nokta-noktaya gönderilebilir veya o router'a tunnels üzerinden anonim olarak gönderilebilir.

Routers, yerel öncelikleri kullanarak giden işleri kuyruğa alır. Daha yüksek öncelik numaraları önce işlenir. Standart tunnel veri önceliği (400) üzerindeki her şey acil olarak değerlendirilir.

### Güncel Taşıma Protokolleri

I2P artık hem IPv4 hem de IPv6 için **NTCP2** (TCP) ve **SSU2** (UDP) kullanıyor. Her iki taşıma protokolü de şunları kullanır: - **X25519** anahtar değişimi (Noise protokol çerçevesi) - **ChaCha20/Poly1305** kimliği doğrulanmış şifreleme (AEAD) - **SHA-256** özetleme

**Eski taşıma protokolleri kaldırıldı:** - NTCP (orijinal TCP) Java router'dan 0.9.50 sürümünde (Mayıs 2021) kaldırıldı - SSU v1 (orijinal UDP) Java router'dan 2.4.0 sürümünde (Aralık 2023) kaldırıldı - SSU v1, i2pd'den 2.44.0 sürümünde (Kasım 2022) kaldırıldı

2025 itibarıyla ağ, tamamen Noise tabanlı taşıma protokollerine geçmiş olup hiçbir eski (legacy) taşıma desteği bulunmamaktadır.

---

## Sürüm Numaralandırma Sistemi

**ÖNEMLİ:** I2P, net biçimde anlaşılması gereken ikili bir sürümleme sistemi kullanır:

### Yayın sürümleri (kullanıcıya yönelik)

Kullanıcıların gördüğü ve indirdiği sürümler şunlardır: - 0.9.50 (Mayıs 2021) - Son 0.9.x sürümü - **1.5.0** (Ağustos 2021) - İlk 1.x sürümü - 1.6.0, 1.7.0, 1.8.0, 1.9.0 (2021-2022 boyunca) - **2.0.0** (Kasım 2022) - İlk 2.x sürümü - 2.1.0'dan 2.9.0'a (2023-2025 boyunca) - **2.10.0** (8 Eylül 2025) - Güncel sürüm

### API Sürümleri (Protokol Uyumluluğu)

Bunlar, RouterInfo özelliklerindeki "router.version" alanında yayımlanan dahili sürüm numaralarıdır: - 0.9.50 (Mayıs 2021) - **0.9.51** (Ağustos 2021) - 1.5.0 sürümü için API sürümü - 0.9.52 ile 0.9.66 arası (2.x sürümleri boyunca devam ediyor) - **0.9.67** (Eylül 2025) - 2.10.0 sürümü için API sürümü

**Önemli Nokta:** 0.9.51 ile 0.9.67 numaraları arasında HİÇBİR sürüm yayımlanmadı. Bu numaralar yalnızca API sürüm tanımlayıcıları olarak kullanılır. I2P, 0.9.50 sürümünden doğrudan 1.5.0'a atladı.

### Sürüm Eşleme Tablosu

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Release Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Last 0.9.x release, removed NTCP1</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages (218 bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.52</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.53</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance enhancements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.54</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 introduced</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.56</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.1.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.57</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Stability improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.2.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ElGamal routers deprecated</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.61</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">December 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Removed SSU1 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.62</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.63</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network optimizations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.64</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">October 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum preparation work</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel bandwidth parameters</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (beta)</td>
    </tr>
  </tbody>
</table>
**Yakında:** Sürüm 2.11.0 (Aralık 2025 için planlanıyor) Java 17+ gerektirecek ve varsayılan olarak post-kuantum kriptografiyi etkinleştirecek.

---

## Protokol Sürümleri

Tüm router'lar I2NP protokol sürümlerini RouterInfo özelliklerindeki "router.version" alanında yayımlamalıdır. Bu sürüm alanı, çeşitli I2NP protokol özellikleri için destek düzeyini gösteren API sürümüdür ve mutlaka gerçek router sürümü olmayabilir.

Alternatif (Java dışı) router’lar, asıl router gerçekleştirimine ilişkin herhangi bir sürüm bilgisi yayımlamak isterlerse, bunu başka bir özellikte yapmalıdırlar. Aşağıda listelenenler dışındaki sürümlere izin verilir. Destek, sayısal bir karşılaştırma ile belirlenecektir; örneğin 0.9.13, 0.9.12 özelliklerine destek anlamına gelir.

**Not:** "coreVersion" özelliği artık router info içinde yayımlanmıyor ve I2NP protokol sürümünün belirlenmesi için hiçbir zaman kullanılmadı.

### API Sürümüne Göre Özellik Özeti

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Required I2NP Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (MLKEM ratchet) support (beta), UDP tracker support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 service record options (see proposal 167)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel build bandwidth parameters (see proposal 168)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.63), minimum floodfill peers will send DSM to (as of 0.9.63)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.62), <strong>ElGamal routers deprecated</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 transport support (if published in router info)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers, minimum peers will build tunnels through (as of 0.9.58), minimum floodfill peers will send DSM to (as of 0.9.58)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.49</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic messages to ECIES-X25519 routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 routers, ECIES-X25519 build request/response records</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup flag bit 4 for AEAD reply</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.44</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 keys in LeaseSet2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.40</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet may be sent in a DSM, RedDSA_SHA512_Ed25519 signature type supported</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 transport support (if published in router info), minimum peers will build tunnels through (as of 0.9.46)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.28</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signature types disallowed, minimum floodfill peers will send DSM to (as of 0.9.34)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 7-1 ignored</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RI key certs / ECDSA and EdDSA signature types, DLM lookup types (flag bits 3-2), minimum version compatible with the current network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with EdDSA Ed25519 signature type (if floodfill)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with ECDSA P-256, P-384, and P-521 signature types (if floodfill); non-zero expiration allowed in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) for floodfill routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Non-zero DLM flag bits 7-1 allowed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Requires zero expiration in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Supports up to 16 leases in a DSM LeaseSet store (previously 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">VTBM and VTBRM message support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill supports encrypted DSM stores</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBM and TBRM messages introduced; minimum version compatible with the current network</td></tr>
  </tbody>
</table>
**Not:** Taşıma ile ilgili özellikler ve uyumluluk sorunları da vardır. Ayrıntılar için NTCP2 ve SSU2 taşıma dokümantasyonuna bakın.

---

## İleti Üstbilgisi

I2NP, mantıksal bir 16 baytlık başlık yapısı kullanırken, modern taşıma protokolleri (NTCP2 ve SSU2) gereksiz boyut ve sağlama toplamı alanlarını içermeyen kısaltılmış 9 baytlık bir başlık kullanır. Alanlar kavramsal olarak özdeş kalır.

### Başlık Biçimi Karşılaştırması

**Standart Biçim (16 bayt):**

Eski NTCP (I2P'nin TCP tabanlı taşıma protokolü) taşımasında ve I2NP iletileri diğer iletilerin içine gömüldüğünde (TunnelData, TunnelGateway, GarlicClove) kullanılır.

```
Bytes 0-15:
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

type :: Integer (1 byte)
        Identifies the message type (see message type table)

msg_id :: Integer (4 bytes)
          Uniquely identifies this message (for some time at least)
          Usually a locally-generated random number, but for outgoing
          tunnel build messages may be derived from the incoming message

expiration :: Date (8 bytes)
              Unix timestamp in milliseconds when this message expires

size :: Integer (2 bytes)
        Length of the payload (0 to ~61.2 KB for tunnel messages)

chks :: Integer (1 byte)
        SHA256 hash of payload truncated to first byte
        Deprecated - NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity
```
**SSU için Kısa Biçim (Kullanımdan kaldırılmış, 5 bayt):**

```
+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

type :: Integer (1 byte)
short_expiration :: Integer (4 bytes, seconds since epoch)
```
**NTCP2, SSU2 ve ECIES-Ratchet Garlic Cloves (I2P'de 'garlic' mesajını oluşturan alt bileşenler) için Kısa Biçim (9 bayt):**

Modern taşıma protokollerinde ve ECIES ile şifrelenmiş garlic mesajlarında (I2P'de demetlemeye dayalı mesajlar) kullanılır.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer (1 byte)
msg_id :: Integer (4 bytes)
short_expiration :: Integer (4 bytes, seconds since epoch, unsigned)
```
### Başlık Alanı Ayrıntıları

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Type</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Identifies the message class (0&ndash;255, see message types below)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Unique ID</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Locally unique identifier for matching replies</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Expiration</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 (standard) / 4 (short)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Timestamp when the message expires. Routers discard expired messages. Short format uses seconds since epoch (unsigned, wraps February 7, 2106)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Payload Length</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Size in bytes (0 to ~61.2 KB for tunnel messages). NTCP2 and SSU2 encode this in their frame headers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated. First byte of SHA-256 hash of the payload. NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity</td>
    </tr>
  </tbody>
</table>
### Uygulama Notları

- SSU (kullanımdan kalkmış) üzerinden iletilirken, yalnızca tür ve 4 baytlık sona erme zamanı dahil edilirdi
- NTCP2 veya SSU2 üzerinden iletilirken, 9 baytlık kısa biçim kullanılır
- Diğer iletiler içinde yer alan I2NP iletileri için standart 16 baytlık başlık gereklidir (Data, TunnelData, TunnelGateway, GarlicClove)
- 0.8.12 sürümünden itibaren, verimlilik amacıyla protokol yığınının bazı noktalarında sağlama toplamı doğrulaması devre dışı bırakılmıştır, ancak uyumluluk için sağlama toplamının üretilmesi hâlâ gereklidir
- Kısa sona erme alanı imzasızdır ve 7 Şubat 2106'da taşma yapacaktır. Bu tarihten sonra doğru zamanı elde etmek için bir ofset eklenmelidir
- Daha eski sürümlerle uyumluluk için, doğrulanmasalar bile her zaman sağlama toplamlarını üretin

---

## Boyut Sınırları

Tunnel iletileri I2NP yüklerini sabit boyutlu parçalara böler: - **İlk parça:** yaklaşık 956 bayt - **Sonraki parçalar:** her biri yaklaşık 996 bayt - **Maksimum parça sayısı:** 64 (0-63 olarak numaralanmış) - **Maksimum yük:** yaklaşık 61,200 bayt (61.2 KB)

**Hesaplama:** 956 + (63 × 996) = 63,704 baytlık teorik maksimum; ek yük nedeniyle pratik sınır yaklaşık 61,200 bayt.

### Tarihsel Bağlam

Eski taşıma protokollerinde çerçeve boyutu sınırları daha sıkıydı: - NTCP: 16 KB'lik çerçeveler - SSU: yaklaşık 32 KB'lik çerçeveler

NTCP2 yaklaşık 65 KB boyutunda çerçeveleri destekler, ancak tunnel parçalama sınırı hâlâ geçerlidir.

### Uygulama Verilerine İlişkin Hususlar

Garlic messages (I2P'de birden çok öğeyi tek bir iletide paketleyen mesajlar) LeaseSets, Session Tags veya şifrelenmiş LeaseSet2 varyantlarını birlikte taşıyabilir ve bu da yük verisi için ayrılan alanı azaltır.

**Öneri:** Güvenilir iletimi sağlamak için datagramların ≤ 10 KB kalması gerekir. 61 KB sınırına yaklaşan iletiler şu sorunlarla karşılaşabilir: - Parçalama sonrası yeniden birleştirme nedeniyle artan gecikme - İletimin başarısız olma olasılığının artması - Trafik analizine daha fazla maruz kalma

### Parçalama Teknik Ayrıntıları

Her tunnel iletisi tam olarak 1,024 bayt (1 KB) boyutundadır ve şunları içerir: - 4 baytlık tunnel ID - 16 baytlık başlatma vektörü (IV) - 1,004 bayt şifrelenmiş veri

Şifrelenmiş verinin içinde, tunnel iletileri, parça başlıklarında şunları belirten parçalanmış I2NP iletilerini taşır: - Parça numarası (0-63) - Bunun ilk mi yoksa devam parçası mı olduğunu - Yeniden birleştirme için toplam ileti kimliği

İlk parça, tam I2NP mesaj başlığını (16 bayt) içerir ve yük için yaklaşık 956 bayt bırakır. Takip eden parçalar mesaj başlığını içermez, bu da parça başına yaklaşık 996 bayt yük sağlar.

---

## Yaygın Mesaj Türleri

Router'lar, giden işleri zamanlamak için ileti türünü ve önceliği kullanır. Daha yüksek öncelik değerleri önce işlenir. Aşağıdaki değerler, geçerli Java I2P varsayılanlarıyla eşleşir (API sürümü 0.9.67 itibarıyla).

**Not:** Öncelikler implementasyona bağlıdır. Kesin öncelik değerleri için, Java I2P kaynak kodundaki `OutNetMessage` sınıfı belgelerine bakın.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Priority</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseStore</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">460</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies (LeaseSet ≈ 898&nbsp;B, RouterInfo ≈ 2&ndash;4&nbsp;KB compressed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishes RouterInfo or LeaseSet objects. Supports LeaseSet2, EncryptedLeaseSet, and MetaLeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseLookup</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queries the network database for RouterInfo or LeaseSet entries</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseSearchReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">≈161&nbsp;B (5 hashes)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Returns candidate floodfill router hashes (typically 3&ndash;16 hashes, recommended maximum 16)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DeliveryStatus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">12&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receipts for tunnel tests or acknowledgements inside GarlicMessages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>GarlicMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">100 (local)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bundles multiple message cloves (e.g., DataMessage, LeaseSets). Supports ElGamal/AES (deprecated) and ECIES-X25519-AEAD-Ratchet encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelData</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,028&nbsp;B (fixed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted tunnel message exchanged between hops. Contains a 4-byte tunnel ID, 16-byte IV, and 1,004 bytes of encrypted data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelGateway</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300&ndash;400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encapsulates messages at the tunnel gateway before fragmentation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DataMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">425</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4&ndash;62&nbsp;KB</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Carries end-to-end garlic payloads (application traffic)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuild</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requests tunnel participation from routers (8 × 528-byte records). Replaced by VariableTunnelBuild for ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuildReply</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to TunnelBuild with accept/reject status per hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable-length tunnel build for ElGamal or ECIES-X25519 routers (1&ndash;8 records, API 0.9.12+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to VariableTunnelBuild</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ShortTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers only (1&ndash;8 × 218-byte records, API 0.9.51+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>OutboundTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sent from outbound endpoint to originator for ECIES-X25519 routers (API 0.9.51+)</td>
    </tr>
  </tbody>
</table>
**Ayrılmış mesaj türleri:** - Tür 0: Ayrılmış - Türler 4-9: Gelecekteki kullanım için ayrılmış - Türler 12-17: Gelecekteki kullanım için ayrılmış - Türler 224-254: Deneysel mesajlar için ayrılmış - Tür 255: Gelecekteki genişletme için ayrılmış

### Mesaj Türü Notları

- Kontrol düzlemi mesajları (DatabaseLookup, TunnelBuild vb.) genellikle istemci tunnel'ları üzerinden değil, **keşif tunnel'ları** üzerinden iletilir, bu da bağımsız önceliklendirmeye olanak tanır
- Öncelik değerleri yaklaşık olup uygulamaya göre değişebilir
- TunnelBuild (21) ve TunnelBuildReply (22) kullanımdan kaldırılmıştır, ancak çok uzun tunnel'larla (>8 atlama) uyumluluk için hâlâ uygulanmaktadır
- Standart tunnel verisi önceliği 400'dür; bunun üzerindeki her şey acil olarak değerlendirilir
- Günümüz ağında tipik tunnel uzunluğu 3-4 atlamadır, bu nedenle çoğu tunnel kurulumu ShortTunnelBuild (218 baytlık kayıtlar) veya VariableTunnelBuild (528 baytlık kayıtlar) kullanır

---

## Şifreleme ve Mesaj Sarmalama

Routers, iletimden önce I2NP mesajlarını sıkça kapsüller ve birden çok şifreleme katmanı oluşturur. DeliveryStatus message (teslim durumu mesajı) şunlardan biri olabilir: 1. Bir GarlicMessage içine sarılmış (şifrelenmiş) 2. Bir DataMessage'ın içinde 3. Bir TunnelData mesajının içinde (yeniden şifrelenmiş)

Her atlama yalnızca kendi katmanının şifresini çözer; son hedef en içteki veri yükünü ortaya çıkarır.

### Şifreleme Algoritmaları

**Eski (Aşamalı olarak kullanım dışı bırakılıyor):** - ElGamal/AES + SessionTags (oturum etiketleri) - asimetrik şifreleme için ElGamal-2048 - simetrik şifreleme için AES-256 - 32 baytlık oturum etiketleri

**Güncel (API 0.9.48 itibarıyla standart):** - ECIES-X25519 + ChaCha20/Poly1305 AEAD ile ratcheting (mandallamalı) ileri gizlilik - Noise protokol çerçevesi (destinasyonlar için Noise_IK_25519_ChaChaPoly_SHA256) - 8 baytlık oturum etiketleri (32 bayttan düşürüldü) - ileri gizlilik için Signal Double Ratchet algoritması - API sürümü 0.9.46'da (2020) tanıtıldı - API sürümü 0.9.58 (2023) itibarıyla tüm routers için zorunlu

**Gelecek (2.10.0 itibarıyla Beta):** - MLKEM (ML-KEM-768) kullanan ve X25519 ile birleştirilen post-kuantum hibrit kriptografi - Klasik ve post-kuantum anahtar uzlaşmasını birleştiren hibrit ratchet (kademeli anahtar yenileme mekanizması) - ECIES-X25519 ile geriye dönük uyumlu - 2.11.0 sürümünde varsayılan olacak (Aralık 2025)

### ElGamal Router Kullanımdan Kaldırma

**KRİTİK:** ElGamal router'lar API sürümü 0.9.58 (sürüm 2.2.0, Mart 2023) itibarıyla kullanımdan kaldırıldı. Artık sorgulanması önerilen asgari floodfill sürümü 0.9.58 olduğundan, gerçekleştirimlerin ElGamal floodfill router'lar için şifrelemeyi uygulaması gerekmez.

**Ancak:** Geriye dönük uyumluluk için ElGamal hedefleri hâlâ desteklenmektedir. ElGamal şifrelemesi kullanan istemciler ECIES router'lar aracılığıyla hâlâ iletişim kurabilir.

### ECIES-X25519-AEAD-Ratchet Ayrıntıları

Bu, I2P'nin kriptografi spesifikasyonundaki crypto type 4 (kripto türü 4)'tür. Şunları sağlar:

**Temel Özellikler:** - Ratcheting (kademeli anahtar yenileme) ile ileri gizlilik (her mesaj için yeni anahtarlar) - Azaltılmış oturum etiketi depolama gereksinimi (8 bayt vs. 32 bayt) - Birden çok oturum türü (Yeni Oturum, Mevcut Oturum, Tek Seferlik) - Noise protokolüne dayalı Noise_IK_25519_ChaChaPoly_SHA256 - Signal'ın Double Ratchet (çift kademeli anahtar yenileme) algoritmasıyla entegre

**Kriptografik Primitifler:** - Diffie-Hellman anahtar anlaşması için X25519 - Akış şifrelemesi için ChaCha20 - Mesaj kimlik doğrulaması (AEAD) için Poly1305 - Özetleme için SHA-256 - Anahtar türetimi için HKDF

**Oturum Yönetimi:** - Yeni Oturum: Statik hedef anahtarı kullanılarak ilk bağlantı - Mevcut Oturum: Sonraki iletiler oturum etiketleri kullanılarak - Tek Seferlik Oturum: Daha düşük ek yük için tek iletilik oturumlar

Tüm teknik ayrıntılar için [ECIES Spesifikasyonu](/docs/specs/ecies/) ve [Öneri 144](/proposals/144-ecies-x25519-aead-ratchet/) belgelerine bakın.

---

## Ortak Yapılar

Aşağıdaki yapılar, birden fazla I2NP mesajının öğeleridir. Bunlar tam mesajlar değildir.

### BuildRequestRecord (tünel kurma isteği kaydı) (ElGamal)

**KULLANIMDAN KALDIRILDI.** Bir tunnel (tünel) bir ElGamal router (yönlendirici) içerdiğinde yalnızca mevcut ağda kullanılır. Modern biçim için [ECIES Tunnel Creation](/docs/specs/implementation/) sayfasına bakın.

**Amaç:** tunnel içinde bir hop (atlama) oluşturulmasını talep etmek için, birden fazla kayıttan oluşan bir kümedeki bir kayıt.

**Biçim:**

ElGamal ve AES ile şifrelenmiş (toplam 528 bayt):

```
+----+----+----+----+----+----+----+----+
| encrypted data (528 bytes)            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
ElGamal şifrelenmiş yapı (528 bayt):

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ElGamal encrypted data (512 bytes)    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity

encrypted_data :: ElGamal-2048 encrypted (bytes 1-256 and 258-513
                  of the 514-byte ElGamal block, with padding bytes
                  at positions 0 and 257 removed)
```
Açık metin yapısı (şifrelemeden önce 222 bayt):

```
+----+----+----+----+----+----+----+----+
| receive_tunnel (4) | our_ident (32)   |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel (4)   |
+----+----+----+----+----+----+----+----+
| next_ident (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key (32 bytes)                     |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv (16 bytes)                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time (4) | send_msg_id  |
+----+----+----+----+----+----+----+----+
     (4)                | padding (29)  |
+----+----+----+----+----+              +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId (4 bytes, nonzero)
our_ident :: Hash (32 bytes)
next_tunnel :: TunnelId (4 bytes, nonzero)
next_ident :: Hash (32 bytes)
layer_key :: SessionKey (32 bytes)
iv_key :: SessionKey (32 bytes)
reply_key :: SessionKey (32 bytes)
reply_iv :: 16 bytes
flag :: Integer (1 byte)
request_time :: Integer (4 bytes, hours since epoch = time / 3600)
send_message_id :: Integer (4 bytes)
padding :: 29 bytes random data
```
**Notlar:** - ElGamal-2048 şifrelemesi 514 baytlık bir blok üretir, ancak iki doldurma baytı (0 ve 257. konumlarda) kaldırılır ve sonuçta 512 bayt kalır - Alan ayrıntıları için [Tunnel Oluşturma Spesifikasyonu](/docs/specs/implementation/) sayfasına bakın - Kaynak kodu: `net.i2p.data.i2np.BuildRequestRecord` - Sabit: `EncryptedBuildRecord.RECORD_SIZE = 528`

### BuildRequestRecord (inşa isteği kaydı) (ECIES-X25519 Long)

API sürümü 0.9.48'te tanıtılan ECIES-X25519 router'lar için. Karma tunnel'larla geriye dönük uyumluluk için 528 bayt kullanır.

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (464 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (464 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**Toplam boyut:** 528 bayt (uyumluluk için ElGamal ile aynı)

Açık metin yapısı ve şifreleme ayrıntıları için [ECIES Tunnel Creation](/docs/specs/implementation/) sayfasına bakın.

### BuildRequestRecord (ECIES-X25519 Kısa)

Yalnızca ECIES-X25519 routers için, API sürümü 0.9.51 (1.5.0 sürümü) itibarıyla. Bu, mevcut standart biçimdir.

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (154 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (154 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**Toplam boyut:** 218 bayt (528 bayta kıyasla %59 azalma)

**Temel Fark:** Kısa kayıtlar, kayıtta açıkça dahil etmek yerine TÜM anahtarları HKDF (anahtar türetme fonksiyonu) aracılığıyla türetir. Buna şunlar dahildir: - Katman anahtarları (tunnel şifrelemesi için) - IV anahtarları (tunnel şifrelemesi için) - Yanıt anahtarları (oluşturma yanıtı için) - Yanıt IV'leri (oluşturma yanıtı için)

Tüm anahtarlar, X25519 anahtar değişiminden elde edilen paylaşılan sırra dayalı olarak Noise protokolünün HKDF mekanizması kullanılarak türetilir.

**Faydalar:** - 4 kısa kayıt tek bir tunnel mesajına sığar (873 bayt) - Her bir kayıt için ayrı mesajlar yerine 3 mesajlık tunnel kurulumları - Azaltılmış bant genişliği kullanımı ve gecikme - Uzun biçimle aynı güvenlik özellikleri

Gerekçe için [Proposal 157](/proposals/157-new-tbm/), tam spesifikasyon için [ECIES Tunnel Creation](/docs/specs/implementation/) belgesine bakın.

**Kaynak kodu:** - `net.i2p.data.i2np.ShortEncryptedBuildRecord` - Sabit: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

### BuildResponseRecord (ElGamal) (oluşturma yanıt kaydı)

**KULLANIMDAN KALDIRILDI.** Yalnızca tunnel bir ElGamal router içerdiğinde kullanılır.

**Amaç:** Oluşturma isteğine verilen yanıtları içeren birden çok kayıttan oluşan kümedeki tek bir kayıt.

**Biçim:**

Şifrelenmiş (528 bayt, BuildRequestRecord ile aynı boyutta):

```
bytes 0-527 :: AES-encrypted record
```
Şifrelenmemiş yapı:

```
+----+----+----+----+----+----+----+----+
| SHA-256 hash (32 bytes)               |
+                                       +
|        (hash of bytes 32-527)         |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data (495 bytes)               |
~                                       ~
|                                  |ret |
+----+----+----+----+----+----+----+----+

bytes 0-31 :: SHA-256 hash of bytes 32-527
bytes 32-526 :: Random data (could be used for congestion info)
byte 527 :: Reply code (0 = accept, 30 = reject)
```
**Yanıt Kodları:** - `0` - Kabul - `30` - Reddet (bant genişliği aşıldı)

Yanıt alanı hakkında ayrıntılar için [Tunnel Creation Specification](/docs/specs/implementation/) bölümüne bakın.

### BuildResponseRecord (ECIES-X25519)

ECIES-X25519 routers için, API sürümü 0.9.48+. Karşılık gelen istekle aynı boyuttadır (uzun için 528, kısa için 218).

**Biçim:**

Uzun biçim (528 bayt):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (512 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Kısa biçim (218 bayt):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (202 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Açık metin yapısı (her iki formatta):**

Bir Mapping yapısı (I2P'nin anahtar-değer biçimi) içerir: - Yanıt durum kodu (zorunlu) - Kullanılabilir bant genişliği parametresi ("b") (isteğe bağlı, API 0.9.65'te eklendi) - Gelecekteki genişletmeler için diğer isteğe bağlı parametreler

**Yanıt Durum Kodları:** - `0` - Başarılı - `30` - Reddedildi: bant genişliği aşıldı

Tam spesifikasyon için [ECIES Tunnel Oluşturma](/docs/specs/implementation/) bölümüne bakın.

### GarlicClove (I2P'de garlic mesajının alt mesajı) (ElGamal/AES)

**UYARI:** Bu, ElGamal ile şifrelenmiş garlic messages (birden fazla garlic clove içeren kapsül mesaj) içindeki garlic cloves (garlic message içindeki bireysel mesaj birimi) için kullanılan formattır. ECIES-AEAD-X25519-Ratchet garlic messages ve garlic cloves için kullanılan format ise önemli ölçüde farklıdır. Güncel format için bkz. [ECIES Spesifikasyonu](/docs/specs/ecies/).

**routers için kullanımdan kaldırılmıştır (API 0.9.58+), destinasyonlar için hâlâ desteklenmektedir.**

**Biçim:**

Şifrelenmemiş:

```
+----+----+----+----+----+----+----+----+
| Delivery Instructions (variable)      |
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message (variable)               |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (8)   |Cert|
+----+----+----+----+----+----+----+----+
                                    (3) |
+----+----+----+----+----+----+----+----+

Delivery Instructions :: Variable length (typically 1, 33, or 37 bytes)
I2NP Message :: Any I2NP message
Clove ID :: 4-byte Integer (random, checked for duplicates)
Expiration :: Date (8 bytes)
Certificate :: Always NULL (3 bytes total, all zeroes)
```
**Notlar:** - Clove'lar (garlic mesajı içindeki alt-mesaj) asla parçalanmaz - Delivery Instructions bayrak baytının ilk biti 0 olduğunda, clove şifrelenmez - İlk bit 1 olduğunda, clove şifrelenir (uygulanmamış özellik) - Azami uzunluk, toplam clove uzunlukları ile azami GarlicMessage (I2P'de bir mesaj türü) uzunluğunun bir fonksiyonudur - Sertifika, yönlendirme için "ödeme" yapmak üzere HashCash ile kullanılabilir (geleceğe yönelik olasılık) - Uygulamada kullanılan mesajlar: DataMessage, DeliveryStatusMessage, DatabaseStoreMessage - GarlicMessage, GarlicMessage içerebilir (iç içe garlic), ancak bu uygulamada kullanılmaz

Kavramsal bir genel bakış için [Garlic Routing](/docs/overview/garlic-routing/) (sarımsak yönlendirme tekniği) sayfasına bakın.

### GarlicClove (ECIES-X25519-AEAD-Ratchet)

ECIES-X25519 routers ve hedefler için API sürümü 0.9.46+. Bu, güncel standart biçimdir.

**KRİTİK FARK:** ECIES garlic, açıkça tanımlı clove (I2P'de garlic mesajı içindeki alt iletiler) yapıları yerine Noise protokolü bloklarına dayanan tamamen farklı bir yapı kullanır.

**Biçim:**

ECIES (Eliptik Eğri Entegre Şifreleme Şeması) garlic mesajları bir dizi blok içerir:

```
Block structure:
+----+----+----+----+----+----+----+----+
|type| length    | data ...
+----+----+----+----+----+-//-

type :: 1 byte block type
length :: 2 bytes block length
data :: variable length data
```
**Blok Türleri:** - `0` - Garlic Clove Bloğu (bir I2NP mesajı içerir) - `1` - Tarih-Saat Bloğu (zaman damgası) - `2` - Seçenekler Bloğu (teslimat seçenekleri) - `3` - Dolgu Bloğu - `254` - Sonlandırma Bloğu (henüz uygulanmamış)

**Sarımsak Dişi Bloğu (tip 0):**

```
+----+----+----+----+----+----+----+----+
|  0 | length    | Delivery Instructions |
+----+----+----+----+                    +
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (4)        |
+----+----+----+----+----+----+----+----+
```
**ElGamal biçimine göre temel farklar:** - 8 baytlık Date yerine 4 baytlık sona erme zamanı (Unix epoch'tan bu yana geçen saniye cinsinden) kullanır - Sertifika alanı yok - Tür ve uzunluk içeren bir blok yapısı içinde sarmalanmıştır - Tüm mesaj ChaCha20/Poly1305 AEAD ile şifrelenir - Oturum yönetimi ratcheting (mandallama) ile

Noise protokol çerçevesi ve blok yapıları hakkında tüm ayrıntılar için [ECIES Specification](/docs/specs/ecies/) belgesine bakın.

### Garlic Clove (I2P'de bir garlic mesajının alt mesajı) Teslim Yönergeleri

Bu biçim, hem ElGamal hem de ECIES garlic cloves (garlic mesajı içindeki alt iletiler) için kullanılır. Ekli mesajın nasıl teslim edileceğini belirtir.

**KRİTİK UYARI:** Bu belirtim YALNIZCA Garlic Cloves (garlic mesajındaki 'clove' bileşenleri) içindeki Delivery Instructions (teslimat talimatları) için geçerlidir. "Delivery Instructions" ayrıca Tunnel Messages (tunnel mesajları) içinde de kullanılır; oradaki biçim önemli ölçüde farklıdır. tunnel teslimat talimatları için [Tunnel Message Specification](/docs/specs/implementation/) belgesine bakın. Bu iki biçimi ASLA karıştırmayın.

**Biçim:**

Oturum anahtarı ve gecikme kullanılmaz ve hiçbir zaman mevcut değildir, bu nedenle üç olası uzunluk şunlardır: - 1 bayt (LOCAL) - 33 bayt (ROUTER ve DESTINATION) - 37 bayt (TUNNEL)

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|       Session Key (optional, 32)     |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|       To Hash (optional, 32)         |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    | Tunnel ID (4, opt)| Delay (4, opt)|
+----+----+----+----+----+----+----+----+

flag :: 1 byte
        Bit order: 76543210
        bit 7: encrypted? (Unimplemented, always 0)
               If 1, a 32-byte encryption session key follows
        bits 6-5: delivery type
               0x0 = LOCAL (0)
               0x1 = DESTINATION (1)
               0x2 = ROUTER (2)
               0x3 = TUNNEL (3)
        bit 4: delay included? (Not fully implemented, always 0)
               If 1, four delay bytes are included
        bits 3-0: reserved, set to 0 for compatibility

Session Key :: 32 bytes (Optional, unimplemented)
               Present if encrypt flag bit is set

To Hash :: 32 bytes (Optional)
           Present if delivery type is DESTINATION, ROUTER, or TUNNEL
           - DESTINATION: SHA256 hash of the destination
           - ROUTER: SHA256 hash of the router identity
           - TUNNEL: SHA256 hash of the gateway router identity

Tunnel ID :: 4 bytes (Optional)
             Present if delivery type is TUNNEL
             The destination tunnel ID (nonzero)

Delay :: 4 bytes (Optional, unimplemented)
         Present if delay included flag is set
         Specifies delay in seconds
```
**Tipik Uzunluklar:** - Yerel teslimi: 1 bayt (yalnızca bayrak) - ROUTER / HEDEF teslimi: 33 bayt (bayrak + karma) - TUNNEL teslimi: 37 bayt (bayrak + karma + tunnel ID)

**Teslimat Türü Açıklamaları:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LOCAL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to the local router (this router)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DESTINATION</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a destination (client) identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ROUTER</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to another router identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TUNNEL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a tunnel gateway router</td>
    </tr>
  </tbody>
</table>
**Uygulama Notları:** - Oturum anahtarı şifrelemesi uygulanmamıştır ve bayrak biti her zaman 0 - Gecikme tam olarak uygulanmamıştır ve bayrak biti her zaman 0 - TUNNEL tesliminde, hash ağ geçidi router'ını belirtir ve tunnel ID, hangi gelen tunnel olduğunu belirtir - DESTINATION tesliminde, hash Destination (I2P adresi) açık anahtarının SHA-256'sıdır - ROUTER tesliminde, hash router kimliğinin SHA-256'sıdır

---

## I2NP Mesajları

Tüm I2NP mesaj türleri için eksiksiz mesaj spesifikasyonları.

### Mesaj Türü Özeti

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseSearchReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelData</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelGateway</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ShortTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">OutboundTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
  </tbody>
</table>
**Ayrılmış:** - Tür 0: Ayrılmış - Türler 4-9: Gelecekte kullanım için ayrılmış - Türler 12-17: Gelecekte kullanım için ayrılmış - Türler 224-254: Deneysel mesajlar için ayrılmış - Tür 255: Gelecekteki genişletme için ayrılmış

---

### DatabaseStore (Tip 1)

**Amaç:** Talep edilmemiş bir veritabanı depolaması veya başarılı bir DatabaseLookup mesajına verilen yanıt.

**İçerik:** Sıkıştırılmamış bir LeaseSet (tunnel erişim bilgileri kümesi), LeaseSet2, MetaLeaseSet veya EncryptedLeaseSet ya da sıkıştırılmış bir RouterInfo (router bilgisi).

**Yanıt belirteci içeren biçim:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token (4)   | reply_tunnelId
+----+----+----+----+----+----+----+----+
     (4)               | reply gateway  |
+----+----+----+----+----+              +
|       SHA256 hash (32 bytes)          |
+                                       +
|                                       |
+                                  +----+
|                                  |
+----+----+----+----+----+----+----+
| data ...
+----+-//

key :: 32 bytes
       SHA256 hash (the "real" hash, not routing key)

type :: 1 byte
        Type identifier
        bit 0:
            0 = RouterInfo
            1 = LeaseSet or variants
        bits 3-1: (as of 0.9.38)
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
        bits 7-4:
            Reserved, set to 0

reply token :: 4 bytes
               If greater than zero, a DeliveryStatusMessage is
               requested with the Message ID set to the reply token
               A floodfill router is also expected to flood the data
               to the closest floodfill peers

reply_tunnelId :: 4 bytes (only if reply token > 0)
                  TunnelId of the inbound gateway of the tunnel
                  for the response
                  If 0, reply is sent directly to reply gateway

reply gateway :: 32 bytes (only if reply token > 0)
                 SHA256 hash of the RouterInfo
                 If reply_tunnelId is nonzero: inbound gateway router
                 If reply_tunnelId is zero: router to send reply to

data :: Variable length
        If type == 0: 2-byte Integer length + gzip-compressed RouterInfo
        If type == 1: Uncompressed LeaseSet
        If type == 3: Uncompressed LeaseSet2
        If type == 5: Uncompressed EncryptedLeaseSet
        If type == 7: Uncompressed MetaLeaseSet
```
**Yanıt belirteci == 0 iken biçim:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//
```

**Kaynak kodu:** - `net.i2p.data.i2np.DatabaseStoreMessage` - `net.i2p.data.RouterInfo` (RouterInfo yapısı için) - `net.i2p.data.LeaseSet` (LeaseSet yapısı için)

---

### DatabaseLookup (Tip 2)

**Amaç:** Ağ veritabanında bir öğeyi sorgulama isteği. Yanıt, DatabaseStore veya DatabaseSearchReply olur.

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key (32 bytes)    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the from router (32)  |
+    or reply tunnel gateway            +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId (4)| size (2)|   |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude (32 bytes) |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude (32)       |
+                                       +
~                                       ~
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|   Session key if reply encryption     |
+       requested (32 bytes)             +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|   Session tags if reply encryption    |
+       requested (variable)             +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

key :: 32 bytes
       SHA256 hash of the object to lookup

from :: 32 bytes
        If deliveryFlag == 0: SHA256 hash of RouterInfo (sender)
        If deliveryFlag == 1: SHA256 hash of reply tunnel gateway

flags :: 1 byte
         Bit order: 76543210
         bit 0: deliveryFlag
             0 = send reply directly
             1 = send reply to some tunnel
         bit 1: encryptionFlag
             Through 0.9.5: must be 0
             As of 0.9.6: ignored
             As of 0.9.7:
                 0 = send unencrypted reply
                 1 = send AES encrypted reply using key and tag
         bits 3-2: lookup type flags
             Through 0.9.5: must be 00
             As of 0.9.6: ignored
             As of 0.9.16:
                 00 = ANY (deprecated, use LS or RI as of 0.9.16)
                 01 = LS lookup (LeaseSet or variants)
                 10 = RI lookup (RouterInfo)
                 11 = exploration lookup (RouterInfo, non-floodfill)
         bit 4: ECIESFlag
             Before 0.9.46: ignored
             As of 0.9.46:
                 0 = send unencrypted or ElGamal reply
                 1 = send ChaCha/Poly encrypted reply using key
         bits 7-5:
             Reserved, set to 0

reply_tunnelId :: 4 bytes (only if deliveryFlag == 1)
                  TunnelId of the tunnel to send reply to (nonzero)

size :: 2 bytes
        Integer (valid range: 0-512)
        Number of peers to exclude from DatabaseSearchReply

excludedPeers :: $size SHA256 hashes of 32 bytes each
                 If lookup fails, exclude these peers from the reply
                 If includes a hash of all zeroes, the request is
                 exploratory (return non-floodfill routers only)

reply_key :: 32 bytes (conditional, see encryption modes below)
reply_tags :: 1 byte count + variable length tags (conditional)
```
**Yanıt Şifreleme Modları:**

**Not:** API 0.9.58 itibarıyla ElGamal routers kullanımdan kaldırılmıştır. Artık sorgulanması önerilen asgari floodfill sürümü 0.9.58 olduğundan, gerçekleştirimlerin ElGamal floodfill router'lar için şifreleme uygulanmasına gerek yoktur. ElGamal hedefleri hâlâ desteklenmektedir.

Bayrak biti 4 (ECIESFlag), yanıt şifreleme modunu belirlemek için bit 1 (encryptionFlag) ile birlikte kullanılır:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Flag bits 4,1</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">From</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">To Router</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reply</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DH?</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.7, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.46, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.49, current standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
  </tbody>
</table>
**Şifreleme Yok (bayraklar 0,0):**

reply_key, tags ve reply_tags mevcut değil.

**ElG'den ElG'ye (bayraklar 0,1) - KULLANIMDAN KALDIRILDI:**

0.9.7 sürümünden itibaren desteklenmektedir, 0.9.58 sürümünden itibaren kullanımdan kaldırılmıştır.

```
reply_key :: 32 byte SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (1-32, typically 1)
        Number of reply tags that follow

reply_tags :: One or more 32-byte SessionTags
              Each is CSRNG(32) random data
```
**ECIES'den ElG'ye (bayraklar 1,0) - KULLANIMDAN KALDIRILDI:**

0.9.46 itibarıyla desteklenmektedir, 0.9.58 itibarıyla kullanımdan kaldırılmıştır.

```
reply_key :: 32 byte ECIES SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (required value: 1)
        Number of reply tags that follow

reply_tags :: One 8-byte ECIES SessionTag
              CSRNG(8) random data
```
Yanıt, [ECIES Spesifikasyonu](/docs/specs/ecies/)'nda tanımlandığı üzere bir ECIES Existing Session (mevcut oturum) mesajıdır:

```
+----+----+----+----+----+----+----+----+
| Session Tag (8 bytes)                 |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted payload            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

tag :: 8 byte reply_tag
k :: 32 byte session key (the reply_key)
n :: 0 (nonce)
ad :: The 8 byte reply_tag
payload :: Plaintext data (DSM or DSRM)
ciphertext = ENCRYPT(k, n, payload, ad)
```
**ECIES'den ECIES'e (bayraklar 1,0) - MEVCUT STANDART:**

ECIES hedefi veya router, bir ECIES router'a bir sorgu gönderir. 0.9.49 sürümünden itibaren desteklenir.

Yukarıdaki "ECIES to ElG" ile aynı biçimdedir. Sorgu mesajı şifrelemesi [ECIES Routers](/docs/specs/ecies/#routers) içinde tanımlanmıştır. İstekte bulunan anonimdir.

**ECIES'den DH ile ECIES'e (bayraklar 1,1) - GELECEK:**

Henüz tam olarak tanımlanmadı. Bkz. [Proposal 156](/proposals/156-ecies-routers/).

**Notlar:** - 0.9.16'dan önce, anahtar bir RouterInfo veya LeaseSet için olabilirdi (aynı anahtar alanı, ayırt etmek için bayrak yok) - Şifrelenmiş yanıtlar yalnızca yanıt bir tunnel üzerinden iletildiğinde yararlıdır - Alternatif DHT (Distributed Hash Table - Dağıtılmış Karma Tablosu) arama stratejileri uygulanırsa, dahil edilen etiketlerin sayısı birden fazla olabilir - Arama anahtarı ve hariç tutma anahtarları "gerçek" karmalardır, yönlendirme anahtarları DEĞİLDİR - 3, 5 ve 7 türleri (LeaseSet2 varyantları) 0.9.38 itibarıyla döndürülebilir. Bkz. [Proposal 123](/proposals/123-new-netdb-entries/) - **Keşif araması notları:** Bir keşif araması, anahtara yakın floodfill olmayan karmaların bir listesini döndürecek şekilde tanımlanır. Ancak uygulamalar farklılık gösterir: Java, bir RI (RouterInfo) için arama anahtarını gerçekten sorgular ve mevcutsa bir DatabaseStore döndürür; i2pd bunu yapmaz. Bu nedenle, daha önce alınmış karmalar için keşif araması kullanılması önerilmez

**Kaynak kodu:** - `net.i2p.data.i2np.DatabaseLookupMessage` - Şifreleme: `net.i2p.crypto.SessionKeyManager`

---

### DatabaseSearchReply (veritabanı arama yanıtı) (Type 3)

**Amaç:** Başarısız bir DatabaseLookup (veritabanı arama) mesajına verilen yanıt.

**İçerik:** İstenen anahtara en yakın router hash'lerinin listesi.

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key (32 bytes)  |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes (variable)           |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    | from (32 bytes)                  |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key :: 32 bytes
       SHA256 of the object being searched

num :: 1 byte Integer
       Number of peer hashes that follow (0-255)

peer_hashes :: $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
               SHA256 of the RouterIdentity that the sender thinks is
               close to the key

from :: 32 bytes
        SHA256 of the RouterInfo of the router this reply was sent from
```
**Notlar:** - 'from' karması kimlik doğrulanmamıştır ve güvenilemez - Döndürülen eş karmalarının, sorgulanan router’a kıyasla anahtara daha yakın olması şart değildir. Normal aramalara verilen yanıtlarda bu, yeni floodfill’lerin keşfini ve sağlamlık için (anahtardan daha uzak) "ters yönde" aramayı kolaylaştırır - Keşif aramalarında anahtar genellikle rastgele oluşturulur. Yanıtın floodfill olmayan peer_hashes değerleri, tüm yerel veritabanının verimsiz sıralanmasından kaçınmak için optimize edilmiş bir algoritma kullanılarak (örn. yakın ama mutlaka en yakın olmayan eşler) seçilebilir. Önbelleğe alma stratejileri de kullanılabilir. Bu, uygulamaya bağlıdır - **Döndürülen karma sayısının tipik değeri:** 3 - **Önerilen en fazla döndürülecek karma sayısı:** 16 - Arama anahtarı, eş karmaları ve 'from' karması "gerçek" karmalardır, YÖNLENDİRME ANAHTARLARI DEĞİLDİR - num 0 ise, bu daha yakın eş bulunamadığını gösterir (çıkmaz)

**Kaynak kodu:** - `net.i2p.data.i2np.DatabaseSearchReplyMessage`

---

### DeliveryStatus (Tür 10)

**Amacı:** Basit bir mesaj alındı onayı. Genellikle mesajın göndericisi tarafından oluşturulur ve mesajın kendisiyle birlikte Garlic Message (I2P’de birden fazla alt mesajı tek bir kapsülde taşıyan yapı) içinde paketlenir; hedef tarafından geri gönderilmek üzere.

**İçerik:** İletilen mesajın kimliği ve oluşturulma veya varış zamanı.

**Biçim:**

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id (4)            | time_stamp (8)                    |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer (4 bytes)
          Unique ID of the message we deliver the DeliveryStatus for
          (see I2NP Message Header for details)

time_stamp :: Date (8 bytes)
              Time the message was successfully created or delivered
```
**Notlar:** - Zaman damgası her zaman oluşturan tarafından mevcut zamana ayarlanır. Ancak bunun koddaki birkaç kullanım alanı vardır ve gelecekte daha fazlası eklenebilir - Bu ileti, SSU içinde bir oturum kurulumu onayı olarak da kullanılır. Bu durumda, ileti kimliği rastgele bir sayıya ayarlanır ve "varış zamanı" geçerli ağ genelindeki kimliğe ayarlanır; bu değer 2’dir (yani, `0x0000000000000002`) - DeliveryStatus (teslim durumu mesajı) genellikle bir GarlicMessage (I2P’de özel bir mesaj türü) içine sarılır ve göndereni açığa çıkarmadan alındı onayı sağlamak için bir tunnel üzerinden gönderilir - Gecikmeyi ve güvenilirliği ölçmek için tunnel testlerinde kullanılır

**Kaynak kodu:** - `net.i2p.data.i2np.DeliveryStatusMessage` - Kullanıldığı yer: `net.i2p.router.tunnel.InboundEndpointProcessor` tunnel testi için

---

### GarlicMessage (Sarımsak Mesajı) (Tür 11)

**UYARI:** Bu, ElGamal ile şifrelenmiş garlic messages (I2P'de birden çok mesajı tek bir pakette birleştiren yapı) için kullanılan biçimdir. ECIES-AEAD-X25519-Ratchet garlic messages için kullanılan biçim önemli ölçüde farklıdır. Güncel biçim için [ECIES Spesifikasyonu](/docs/specs/ecies/) sayfasına bakın.

**Amaç:** Birden çok şifrelenmiş I2NP mesajını sarmak için kullanılır.

**İçerik:** Şifresi çözüldüğünde, Garlic Cloves (I2P’deki tekil alt-iletiler) ve ek veriden oluşan bir dizi; Clove Set (Garlic Cloves dizisi) olarak da bilinir.

**Şifrelenmiş Format:**

```
+----+----+----+----+----+----+----+----+
| length (4)            | data          |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length :: 4 byte Integer
          Number of bytes that follow (0 to 64 KB)

data :: $length bytes
        ElGamal encrypted data
```
**Şifresi Çözülmüş Veri (Clove Set - clove kümesi):**

```
+----+----+----+----+----+----+----+----+
| num| clove 1 (variable)               |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| clove 2 (variable)                    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate (3) | Message_ID (4)  |
+----+----+----+----+----+----+----+----+
    Expiration (8)                  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Number of GarlicCloves to follow

clove :: GarlicClove (see GarlicClove structure above)

Certificate :: Always NULL (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
**Notlar:** - Şifrelenmediğinde, veri bir veya daha fazla Garlic Clove (I2P’deki garlic mesajının alt birimi) içerir - AES ile şifrelenmiş blok en az 128 bayta doldurulur; 32 baytlık oturum etiketi ile şifreli mesajın asgari boyutu 160 bayttır; 4 baytlık uzunluk alanıyla Garlic Message (birden çok Garlic Clove içeren üst mesaj) için asgari boyut 164 bayttır - Gerçek maksimum uzunluk 64 KB'den küçüktür (tunnel mesajları için pratik sınır yaklaşık 61.2 KB) - Şifreleme ayrıntıları için [ElGamal/AES Şartnamesi](/docs/legacy/elgamal-aes/) bölümüne bakın - Kavramsal genel bakış için [Garlic Routing](/docs/overview/garlic-routing/) bölümüne bakın - AES ile şifrelenmiş bloğun 128 baytlık asgari boyutu şu anda yapılandırılamaz - Mesaj kimliği genellikle gönderimde rastgele bir sayıya ayarlanır ve alımda yok sayılıyor görünür - Sertifika, yönlendirme için "ödeme" yapmak üzere HashCash ile kullanılabilir (gelecekteki olasılık) - **ElGamal şifreleme yapısı:** 32 baytlık oturum etiketi + ElGamal ile şifrelenmiş oturum anahtarı + AES ile şifrelenmiş yük

**ECIES-X25519-AEAD-Ratchet formatı için (router'lar için mevcut standart):**

Bkz. [ECIES Specification](/docs/specs/ecies/) ve [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/).

**Kaynak kodu:** - `net.i2p.data.i2np.GarlicMessage` - Şifreleme: `net.i2p.crypto.elgamal.ElGamalAESEngine` (kullanımdan kaldırılmış) - Modern şifreleme: `net.i2p.crypto.ECIES` paketleri

---

### TunnelData (Tür 18)

**Purpose:** Bir tunnel ağ geçidinden veya katılımcısından sonraki katılımcıya ya da uç noktaya gönderilen bir ileti. Veri sabit uzunluktadır; parçalanmış, toplulaştırılmış, dolgu eklenmiş ve şifrelenmiş I2NP iletilerini içerir.

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| tunnelID (4)          | data (1024)   |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

data :: 1024 bytes
        Payload data, fixed to 1024 bytes
```
**Yük Yapısı (1024 bayt):**

```
Bytes 0-15: Initialization Vector (IV) for AES encryption
Bytes 16-1023: Encrypted tunnel message data (1008 bytes)
```
**Notlar:** - TunnelData için I2NP mesaj kimliği her atlamada yeni bir rastgele sayıya atanır - tunnel mesaj biçimi (şifrelenmiş verinin içinde) [Tünel Mesajı Spesifikasyonu](/docs/specs/implementation/) içinde belirtilmiştir - Her atlama, AES-256 ile CBC modunda bir katmanı çözer - IV (ilklendirme vektörü), her atlamada çözülen veri kullanılarak güncellenir - Toplam boyut tam olarak 1.028 bayttır (4 tunnelId + 1024 veri) - Bu, tunnel trafiğinin temel birimidir - TunnelData mesajları, parçalanmış I2NP mesajlarını taşır (GarlicMessage, DatabaseStore vb.)

**Kaynak kodu:** - `net.i2p.data.i2np.TunnelDataMessage` - Sabit: `TunnelDataMessage.DATA_LENGTH = 1024` - İşleyen: `net.i2p.router.tunnel.InboundGatewayProcessor`

---

### TunnelGateway (Tünel Geçidi) (Tür 19)

**Amaç:** Başka bir I2NP mesajını, tunnel'in gelen ağ geçidinde tunnel içine iletilmek üzere paketler.

**Biçim:**

```
+----+----+----+----+----+----+----+-//
| tunnelId (4)          | length (2)| data...
+----+----+----+----+----+----+----+-//

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

length :: 2 byte Integer
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Notlar:** - Yük, standart 16 baytlık başlığa sahip bir I2NP mesajıdır - Yerel router'dan tunnel'lere mesaj enjekte etmek için kullanılır - Gerekirse ağ geçidi, içerideki mesajı parçalara böler - Parçalama sonrasında, parçalar TunnelData mesajlarının içine sarılır - TunnelGateway hiçbir zaman ağ üzerinden gönderilmez; tunnel işlemeye başlamadan önce kullanılan dahili bir mesaj türüdür

**Kaynak kodu:** - `net.i2p.data.i2np.TunnelGatewayMessage` - İşleme: `net.i2p.router.tunnel.OutboundGatewayProcessor`

---

### DataMessage (Tür 20)

**Amaç:** Her tür veriyi sarmalamak için Garlic Messages (I2P'de Garlic mesaj formatı) ve Garlic Cloves (Garlic mesajı içindeki 'clove/diş' alt birimleri) tarafından kullanılır (genellikle uçtan uca şifrelenmiş uygulama verisi).

**Biçim:**

```
+----+----+----+----+----+----+-//-+
| length (4)            | data...    |
+----+----+----+----+----+----+-//-+

length :: 4 bytes
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Notlar:** - Bu mesaj herhangi bir yönlendirme bilgisi içermez ve asla "unwrapped" olarak gönderilmez - Yalnızca Garlic messages (Garlic mesajları) içinde kullanılır - Genellikle uçtan uca şifrelenmiş uygulama verisi içerir (HTTP, IRC, e-posta vb.) - Veri genellikle ElGamal/AES ya da ECIES ile şifrelenmiş bir yükten oluşur - tunnel mesajı parçalanma sınırları nedeniyle pratikteki azami uzunluk yaklaşık 61.2 KB'dir

**Kaynak kodu:** - `net.i2p.data.i2np.DataMessage`

---

### TunnelBuild (Tür 21)

**KULLANIMDAN KALDIRILDI.** VariableTunnelBuild (tip 23) veya ShortTunnelBuild (tip 25) kullanın.

**Amaç:** Sabit uzunlukta, 8 atlamalı tunnel oluşturma isteği.

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| Record 0 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
Record size: 528 bytes
Total size: 8 × 528 = 4,224 bytes
```
**Notlar:** - 0.9.48 itibarıyla, ECIES-X25519 BuildRequestRecords (yapı istek kayıtları) içerebilir. Bkz. [ECIES Tunnel Creation](/docs/specs/implementation/) - Ayrıntılar için bkz. [Tunnel Oluşturma Spesifikasyonu](/docs/specs/implementation/) - Bu ileti için I2NP ileti kimliği, Tunnel Oluşturma Spesifikasyonu'na göre ayarlanmalıdır - Günümüz ağında nadiren görülse de (VariableTunnelBuild (değişken tunnel oluşturma) ile değiştirildi), çok uzun tunnel'lar için hâlâ kullanılabilir ve resmen kullanımdan kaldırılmamıştır - Router'lar uyumluluk için bunu hâlâ uygulamak zorundadır - Sabit 8 kayıtlı biçim esnek değildir ve daha kısa tunnel'lar için bant genişliğini israf eder

**Kaynak kodu:** - `net.i2p.data.i2np.TunnelBuildMessage` - Sabit: `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8`

---

### TunnelBuildReply (Tip 22)

**KULLANIMDAN KALDIRILDI.** VariableTunnelBuildReply (tip 24) veya OutboundTunnelBuildReply (tip 26) kullanın.

**Amaç:** 8 atlamalı sabit uzunluklu tunnel oluşturma yanıtı.

**Biçim:**

TunnelBuildMessage ile aynı biçimdedir; BuildRequestRecords yerine BuildResponseRecords içerir.

```
Total size: 8 × 528 = 4,224 bytes
```
**Notlar:** - 0.9.48 itibarıyla, ECIES-X25519 BuildResponseRecords (oluşturma yanıt kayıtları) içerebilir. Bkz. [ECIES Tunnel Oluşturma](/docs/specs/implementation/) - Ayrıntılar için [Tunnel Oluşturma Belirtimi](/docs/specs/implementation/) - Bu mesaj için I2NP mesaj kimliği, tunnel oluşturma belirtimine göre ayarlanmalıdır - Günümüz ağında nadiren görülse de (VariableTunnelBuildReply (değişken tunnel oluşturma yanıtı) ile değiştirildi), çok uzun tunnel'lar için hâlâ kullanılabilir ve resmen kullanımdan kaldırılmamıştır - Router'lar yine de uyumluluk için bunu uygulamak zorundadır

**Kaynak kodu:** - `net.i2p.data.i2np.TunnelBuildReplyMessage`

---

### VariableTunnelBuild (Tür 23)

**Amaç:** 1-8 atlama için değişken uzunluklu tunnel oluşturma. Hem ElGamal hem de ECIES-X25519 router'ları destekler.

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords (variable)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildRequestRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**Notlar:** - 0.9.48 itibarıyla, ECIES-X25519 BuildRequestRecords (inşa isteği kayıtları) içerebilir. Bkz. [ECIES Tunnel Creation](/docs/specs/implementation/) - router sürüm 0.7.12’de (2009) tanıtıldı - 0.7.12 sürümünden önceki tunnel katılımcılarına gönderilmemelidir - Ayrıntılar için bkz. [Tunnel Creation Specification](/docs/specs/implementation/) - I2NP mesaj kimliği, tunnel oluşturma teknik şartnamesine göre ayarlanmalıdır - **Tipik kayıt sayısı:** 4 (4 atlamalı bir tunnel için) - **Tipik toplam boyut:** 1 + (4 × 528) = 2,113 bayt - Bu, ElGamal routers için standart tunnel oluşturma mesajıdır - Bunun yerine ECIES routers genellikle ShortTunnelBuild (tip 25) kullanır

**Kaynak kodu:** - `net.i2p.data.i2np.VariableTunnelBuildMessage`

---

### VariableTunnelBuildReply (Tür 24)

**Amaç:** 1-8 atlama için değişken uzunluklu tunnel kurulum yanıtı. Hem ElGamal hem de ECIES-X25519 router'ları destekler.

**Biçim:**

VariableTunnelBuildMessage (değişken tunnel oluşturma mesajı) ile aynı biçimdedir; ancak BuildRequestRecords yerine BuildResponseRecords içerir.

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords (variable)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildResponseRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**Notlar:** - 0.9.48 itibarıyla, ECIES-X25519 BuildResponseRecords içerebilir. Bkz. [ECIES Tunnel Oluşturma](/docs/specs/implementation/) - router sürüm 0.7.12'de (2009) tanıtıldı - 0.7.12 sürümünden önceki tunnel katılımcılarına gönderilmeyebilir - Ayrıntılar için [Tunnel Oluşturma Spesifikasyonu](/docs/specs/implementation/) bölümüne bakın - I2NP ileti kimliği, Tunnel oluşturma spesifikasyonuna uygun olarak ayarlanmalıdır - **Tipik kayıt sayısı:** 4 - **Tipik toplam boyut:** 2,113 bayt

**Kaynak kodu:** - `net.i2p.data.i2np.VariableTunnelBuildReplyMessage`

---

### ShortTunnelBuild (Tür 25)

**Amaç:** Yalnızca ECIES-X25519 routers için kısa tunnel oluşturma iletileri. API sürümü 0.9.51'de tanıtıldı (sürüm 1.5.0, Ağustos 2021). Bu, ECIES tunnel oluşturma işlemleri için mevcut standarttır.

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords (var)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildRequestRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**Notlar:** - router sürüm 0.9.51'de tanıtıldı (sürüm 1.5.0, Ağustos 2021) - API sürümü 0.9.51'den daha eski olan tunnel katılımcılarına gönderilmeyebilir - Tam belirtim için [ECIES Tunnel Creation](/docs/specs/implementation/) bölümüne bakın - Gerekçesi için [Proposal 157](/proposals/157-new-tbm/) belgesine bakın - **Tipik kayıt sayısı:** 4 - **Tipik toplam boyut:** 1 + (4 × 218) = 873 bayt - **Bant genişliği tasarrufu:** VariableTunnelBuild'e göre 59% daha küçük (873'e karşı 2,113 bayt) - **Performans kazancı:** 4 kısa kayıt tek bir tunnel mesajına sığar; VariableTunnelBuild 3 tunnel mesajı gerektirir - Bu, artık saf ECIES-X25519 tunnel'ları için standart tunnel oluşturma biçimidir - Kayıtlar, anahtarları açıkça dahil etmek yerine HKDF (HMAC tabanlı anahtar türetme işlevi) aracılığıyla türetir

**Kaynak kodu:** - `net.i2p.data.i2np.ShortTunnelBuildMessage` - Sabit: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

---

### OutboundTunnelBuildReply (Tür 26)

**Amaç:** Yeni bir tunnel üzerindeki giden uç noktadan başlatıcıya gönderilir. Yalnızca ECIES-X25519 routers için. API sürüm 0.9.51'de tanıtıldı (sürüm 1.5.0, Ağustos 2021).

**Biçim:**

ShortTunnelBuildMessage ile aynı biçimdedir; ShortBuildRequestRecords yerine ShortBuildResponseRecords kullanır.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords (var)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildResponseRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**Notlar:** - router 0.9.51 sürümünde tanıtıldı (sürüm 1.5.0, Ağustos 2021) - Tam belirtim için [ECIES Tunnel Oluşturma](/docs/specs/implementation/) bölümüne bakın - **Tipik kayıt sayısı:** 4 - **Tipik toplam boyut:** 873 bayt - Bu yanıt, yeni oluşturulan outbound tunnel üzerinden outbound uç nokta (OBEP) tarafından tunnel oluşturucusuna geri gönderilir - Tüm hop (atlama) noktalarının tunnel kurulumunu kabul ettiğini doğrular

**Kaynak kodu:** - `net.i2p.data.i2np.OutboundTunnelBuildReplyMessage`

---

## Kaynaklar

### Resmi Spesifikasyonlar

- **[I2NP Belirtimi](/docs/specs/i2np/)** - Eksiksiz I2NP ileti biçimi belirtimi
- **[Ortak Yapılar](/docs/specs/common-structures/)** - I2P genelinde kullanılan veri türleri ve yapılar
- **[Tunnel Oluşturma](/docs/specs/implementation/)** - ElGamal tunnel oluşturma (kullanımdan kaldırıldı)
- **[ECIES Tunnel Oluşturma](/docs/specs/implementation/)** - ECIES-X25519 tunnel oluşturma (güncel)
- **[Tunnel İletisi](/docs/specs/implementation/)** - Tunnel ileti biçimi ve teslim yönergeleri
- **[NTCP2 Belirtimi](/docs/specs/ntcp2/)** - TCP taşıma protokolü
- **[SSU2 Belirtimi](/docs/specs/ssu2/)** - UDP taşıma protokolü
- **[ECIES Belirtimi](/docs/specs/ecies/)** - ECIES-X25519-AEAD-Ratchet şifreleme (ratchet: kademeli anahtar yenileme mekanizması)
- **[Kriptografi Belirtimi](/docs/specs/cryptography/)** - Düşük seviyeli kriptografik ilkeller
- **[I2CP Belirtimi](/docs/specs/i2cp/)** - İstemci protokolü belirtimi
- **[Datagram Belirtimi](/docs/api/datagrams/)** - Datagram2 ve Datagram3 biçimleri

### Öneriler

- **[Teklif 123](/proposals/123-new-netdb-entries/)** - Yeni netDB kayıtları (LeaseSet2, EncryptedLeaseSet, MetaLeaseSet)
- **[Teklif 144](/proposals/144-ecies-x25519-aead-ratchet/)** - ECIES-X25519-AEAD-Ratchet şifreleme
- **[Teklif 154](/proposals/154-ecies-lookups/)** - Şifreli veritabanı araması
- **[Teklif 156](/proposals/156-ecies-routers/)** - ECIES routers
- **[Teklif 157](/proposals/157-new-tbm/)** - Daha küçük tunnel oluşturma iletileri (kısa biçim)
- **[Teklif 159](/proposals/159-ssu2/)** - SSU2 taşıma
- **[Teklif 161](/tr/proposals/161-ri-dest-padding/)** - Sıkıştırılabilir dolgu
- **[Teklif 163](/proposals/163-datagram2/)** - Datagram2 ve Datagram3
- **[Teklif 167](/proposals/167-service-records/)** - LeaseSet hizmet kaydı parametreleri
- **[Teklif 168](/proposals/168-tunnel-bandwidth/)** - Tunnel oluşturma bant genişliği parametreleri
- **[Teklif 169](/proposals/169-pq-crypto/)** - Post-kuantum hibrit kriptografi

### Dokümantasyon

- **[Garlic Routing](/docs/overview/garlic-routing/)** - Katmanlı mesaj demetleme
- **[ElGamal/AES](/docs/legacy/elgamal-aes/)** - Kullanımdan kaldırılmış şifreleme şeması
- **[Tunnel Uygulaması](/docs/specs/implementation/)** - Parçalama ve işleme
- **[Ağ Veritabanı](/docs/specs/common-structures/)** - Dağıtık hash tablosu
- **[NTCP2 Taşıma](/docs/specs/ntcp2/)** - TCP taşıma belirtimi
- **[SSU2 Taşıma](/docs/specs/ssu2/)** - UDP taşıma belirtimi
- **[Teknik Giriş](/docs/overview/tech-intro/)** - I2P mimarisine genel bakış

### Kaynak kodu

- **[Java I2P Deposu](https://i2pgit.org/I2P_Developers/i2p.i2p)** - Resmî Java gerçekleştirmesi
- **[GitHub Yansısı](https://github.com/i2p/i2p.i2p)** - Java I2P'nin GitHub yansısı
- **[i2pd Deposu](https://github.com/PurpleI2P/i2pd)** - C++ gerçekleştirmesi

### Önemli Kaynak Kod Konumları

**Java I2P (i2pgit.org/I2P_Developers/i2p.i2p):** - `core/java/src/net/i2p/data/i2np/` - I2NP mesaj gerçeklemeleri - `core/java/src/net/i2p/crypto/` - Kriptografik gerçeklemeler - `router/java/src/net/i2p/router/tunnel/` - Tunnel işlemesi - `router/java/src/net/i2p/router/transport/` - Taşıma gerçeklemeleri

**Sabitler ve Değerler:** - `I2NPMessage.MAX_SIZE = 65536` - Maksimum I2NP mesaj boyutu - `I2NPMessageImpl.HEADER_LENGTH = 16` - Standart başlık boyutu - `TunnelDataMessage.DATA_LENGTH = 1024` - Tunnel mesaj yükü - `EncryptedBuildRecord.RECORD_SIZE = 528` - Uzun oluşturma kaydı - `ShortEncryptedBuildRecord.RECORD_SIZE = 218` - Kısa oluşturma kaydı - `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8` - Bir oluşturma başına maksimum kayıt sayısı

---

## Ek A: Ağ İstatistikleri ve Mevcut Durum

### Ağ Bileşimi (Ekim 2025 itibarıyla)

- **Toplam routers:** Yaklaşık 60,000-70,000 (değişir)
- **Floodfill routers:** Yaklaşık 500-700 aktif
- **Şifreleme türleri:**
  - ECIES-X25519: routers arasında >95%
  - ElGamal: routers arasında <5% (kullanımdan kaldırıldı, yalnızca eski)
- **Taşıma protokollerinin benimsenmesi:**
  - SSU2: >60% birincil taşıma
  - NTCP2: ~40% birincil taşıma
  - Eski taşıma protokolleri (SSU1, NTCP): 0% (kaldırıldı)
- **İmza türleri:**
  - EdDSA (Ed25519): Büyük çoğunluk
  - ECDSA: Küçük bir yüzde
  - RSA: İzin verilmiyor (kaldırıldı)

### Asgari Router Gereksinimleri

- **API sürümü:** 0.9.16+ (ağ ile EdDSA uyumluluğu için)
- **Önerilen en düşük:** API 0.9.51+ (ECIES kısa tunnel derlemeleri)
- **floodfills için mevcut en düşük:** API 0.9.58+ (ElGamal router'ın kullanımdan kaldırılması)
- **Yaklaşan gereksinim:** Java 17+ (sürüm 2.11.0 itibarıyla, Aralık 2025)

### Bant Genişliği Gereksinimleri

- **Asgari:** 128 KBytes/sn (N bayrağı veya üzeri) floodfill (I2P ağında netDb verisini tutup dağıtan özel düğüm) için
- **Önerilen:** 256 KBytes/sn (O bayrağı) veya üzeri
- **Floodfill gereksinimleri:**
  - Asgari 128 KB/sn bant genişliği
  - Kararlı çalışma süresi (> %95 önerilir)
  - Düşük gecikme (eşlere <500 ms)
  - Sağlık testlerini geçmek (kuyruk süresi, iş gecikmesi)

### Tunnel İstatistikleri

- **Tipik tunnel uzunluğu:** 3-4 atlama
- **Maksimum tunnel uzunluğu:** 8 atlama (teorik, nadiren kullanılır)
- **Tipik tunnel ömrü:** 10 dakika
- **Tunnel oluşturma başarı oranı:** iyi bağlantılı routers için >85%
- **Tunnel oluşturma mesaj biçimi:**
  - ECIES routers: ShortTunnelBuild (218 baytlık kayıtlar)
  - Karma tunnels: VariableTunnelBuild (528 baytlık kayıtlar)

### Performans Metrikleri

- **Tunnel oluşturma süresi:** 1-3 saniye (tipik)
- **Uçtan uca gecikme:** 0,5-2 saniye (tipik, toplam 6-8 atlama)
- **Aktarım hızı:** tunnel bant genişliği ile sınırlıdır (genellikle tunnel başına 10-50 KB/sn)
- **Maksimum datagram boyutu:** 10 KB önerilir (61,2 KB teorik maksimum)

---

## Ek B: Artık Önerilmeyen ve Kaldırılmış Özellikler

### Tamamen Kaldırıldı (Artık Desteklenmiyor)

- **NTCP aktarımı** - 0.9.50 sürümünde kaldırıldı (Mayıs 2021)
- **SSU v1 aktarımı** - Java I2P'den 2.4.0 sürümünde kaldırıldı (Aralık 2023)
- **SSU v1 aktarımı** - i2pd'den 2.44.0 sürümünde kaldırıldı (Kasım 2022)
- **RSA imza türleri** - API 0.9.28 itibarıyla yasaklandı

### Kullanımdan kaldırıldı (Destekleniyor ancak önerilmez)

- **ElGamal router'lar** - API 0.9.58 (Mart 2023) itibarıyla kullanımdan kaldırıldı
  - ElGamal hedefler geriye dönük uyumluluk için hâlâ desteklenmektedir
  - Yeni router'lar yalnızca ECIES-X25519 kullanmalıdır
- **TunnelBuild (type 21)** - VariableTunnelBuild ve ShortTunnelBuild lehine kullanımdan kaldırıldı
  - Çok uzun tunnel'lar (>8 atlama) için hâlâ uygulanmaktadır
- **TunnelBuildReply (type 22)** - VariableTunnelBuildReply ve OutboundTunnelBuildReply lehine kullanımdan kaldırıldı
- **ElGamal/AES şifrelemesi** - ECIES-X25519-AEAD-Ratchet lehine kullanımdan kaldırıldı
  - Eski hedefler için hâlâ kullanılmaktadır
- **Uzun ECIES BuildRequestRecords (528 bayt)** - Kısa biçimin (218 bayt) lehine kullanımdan kaldırıldı
  - ElGamal atlamaları içeren karışık tunnel'larda hâlâ kullanılmaktadır

### Eski Sürüm Desteği Zaman Çizelgesi

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Deprecated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2018 (0.9.36)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2021 (0.9.50)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by NTCP2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU v1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2022 (0.9.54)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (Java) / 2022 (i2pd)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by SSU2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal routers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (0.9.58)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations still supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017 (0.9.28)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Never widely used</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2009 (0.7.12)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Not removed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Still supported for long tunnels</td>
    </tr>
  </tbody>
</table>
---

## Ek C: Gelecekteki Gelişmeler

### Kuantum Sonrası Kriptografi

**Durum:** 2.10.0 sürümüyle birlikte (Eylül 2025) Beta, 2.11.0 sürümünde (Aralık 2025) varsayılan olacak

**Uygulama:** - Klasik X25519 ve post-quantum (kuantum-sonrası) MLKEM (ML-KEM-768) birleştiren hibrit yaklaşım - Mevcut ECIES-X25519 altyapısıyla geriye dönük uyumlu - Hem klasik hem de PQ anahtar materyali ile Signal Double Ratchet (çift mandal anahtar yenileme algoritması) kullanır - Ayrıntılar için [Proposal 169](/proposals/169-pq-crypto/) sayfasına bakın

**Geçiş Yolu:** 1. Sürüm 2.10.0 (Eylül 2025): beta seçeneği olarak sunulacak 2. Sürüm 2.11.0 (Aralık 2025): varsayılan olarak etkinleştirilecek 3. Gelecek sürümler: Zamanla zorunlu hale gelecek

### Planlanan Özellikler

- **IPv6 iyileştirmeleri** - Daha iyi IPv6 desteği ve geçiş mekanizmaları
- **Tunnel başına bant daraltma** - Her tunnel için ince ayarlı bant genişliği kontrolü
- **Geliştirilmiş metrikler** - Daha iyi performans izleme ve tanılama
- **Protokol iyileştirmeleri** - Daha az ek yük ve daha yüksek verimlilik
- **Geliştirilmiş floodfill seçimi** - Daha iyi ağ veritabanı dağıtımı

### Araştırma Alanları

- **Tunnel uzunluğu optimizasyonu** - Tehdit modeline göre dinamik tunnel uzunluğu
- **Gelişmiş padding (dolgu)** - Trafik analizine karşı dirençte iyileştirmeler
- **Yeni şifreleme şemaları** - Kuantum hesaplama tehditlerine hazırlık
- **Tıkanıklık kontrolü** - Ağ yükünün daha iyi yönetimi
- **Mobil destek** - Mobil cihazlar ve ağlar için optimizasyonlar

---

## Ek D: Uygulama Yönergeleri

### Yeni Gerçeklemeler İçin

**Asgari Gereksinimler:** 1. API sürümü 0.9.51+ özelliklerini destekleyin 2. ECIES-X25519-AEAD-Ratchet şifrelemesini uygulayın 3. NTCP2 ve SSU2 taşıma protokollerini destekleyin 4. ShortTunnelBuild mesajlarını (218 baytlık kayıtlar) uygulayın 5. LeaseSet2 varyantlarını destekleyin (türleri 3, 5, 7) 6. EdDSA imzalarını kullanın (Ed25519)

**Önerilen:** 1. Post-kuantum hibrit kriptografiyi destekleyin (2.11.0 itibarıyla) 2. tunnel başına bant genişliği parametrelerini uygulayın 3. Datagram2 ve Datagram3 formatlarını destekleyin 4. LeaseSets içinde hizmet kaydı seçeneklerini uygulayın 5. /docs/specs/ adresindeki resmi spesifikasyonlara uyun

**Gerekli Değil:** 1. ElGamal router desteği (kullanımdan kaldırıldı) 2. Eski taşıma desteği (SSU1, NTCP) 3. Uzun ECIES BuildRequestRecords (İnşa İstek Kayıtları; yalnızca ECIES tunnels için 528 bayt) 4. TunnelBuild/TunnelBuildReply mesajları (Variable veya Short varyantlarını kullanın)

### Test ve Doğrulama

**Protokol Uyumluluğu:** 1. Resmi Java I2P router ile birlikte çalışabilirliği test edin 2. i2pd C++ router ile birlikte çalışabilirliği test edin 3. İleti biçimlerinin belirtimlere uygunluğunu doğrulayın 4. tunnel oluşturma/sökme döngülerini test edin 5. Test vektörleriyle şifreleme/şifre çözmeyi doğrulayın

**Performans Testi:** 1. tunnel oluşturma başarı oranlarını ölçün (>85% olmalı) 2. çeşitli tunnel uzunluklarıyla test edin (2-8 atlama) 3. parçalama ve yeniden birleştirmeyi doğrulayın 4. yük altında test edin (eşzamanlı birden çok tunnel) 5. uçtan uca gecikmeyi ölçün

**Güvenlik Testleri:** 1. Şifreleme uygulamasını doğrulayın (test vektörlerini kullanın) 2. Yeniden oynatma saldırısının (replay attack) önlenmesini test edin 3. Mesajın zaman aşımı yönetimini doğrulayın 4. Hatalı biçimlendirilmiş mesajlara karşı test edin 5. Doğru rastgele sayı üretimini doğrulayın

### Sık Yapılan İmplementasyon Hataları

1. **Kafa karıştırıcı teslim talimatı biçimleri** - garlic clove (I2P'de tekil 'garlic' alt-ileti) vs tunnel iletisi
2. **Hatalı anahtar türetimi** - kısa build records (inşa kayıtları) için HKDF kullanımı
3. **Message ID yönetimi** - tunnel kurulumları için doğru şekilde ayarlanmaması
4. **Parçalama sorunları** - 61.2 KB'lik pratik sınıra uyulmaması
5. **Bayt sıralaması (endianness) hataları** - Java tüm tamsayılar için big-endian kullanır
6. **Sona erme yönetimi** - Kısa biçim 7 Şubat 2106'da sarar
7. **Checksum (sağlama toplamı) üretimi** - Doğrulanmasa bile hâlâ gereklidir
