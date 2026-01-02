---
title: "I2P Üzerinden BitTorrent"
description: "I2P ağı içindeki BitTorrent için detaylı teknik özellik ve ekosistem genel bakışı"
slug: "bittorrent"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Genel Bakış

I2P üzerinden BitTorrent, I2P'nin akış katmanını kullanarak şifrelenmiş tüneller aracılığıyla anonim dosya paylaşımını sağlar. Tüm eşler, IP adresleri yerine kriptografik I2P hedefleri ile tanımlanır. Sistem, HTTP ve UDP tracker'ları, hibrit magnet bağlantılarını ve kuantum sonrası hibrit şifrelemeyi destekler.

---

## 1. Protokol Yığını

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Function</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Application</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BitTorrent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2psnark, BiglyBT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming / SAM v3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2CP, NTCP2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Network</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Garlic routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2NP</td>
    </tr>
  </tbody>
</table>
Tüm bağlantılar I2P'nin şifrelenmiş aktarım katmanı (NTCP2 veya SSU2) üzerinden çalışır. UDP tracker paketleri bile I2P streaming içinde kapsüllenir.

---

## 2. İzleyiciler

### HTTP İzleyiciler

Standart `.i2p` tracker'lar şu şekildeki HTTP GET isteklerine yanıt verir:

```
http://tracker2.postman.i2p/announce?info_hash=<20-byte>&peer_id=<20-byte>&port=6881&uploaded=0&downloaded=0&left=1234&compact=1
```
Yanıtlar **bencoded** formatındadır ve eşler (peers) için I2P destination hash'leri kullanır.

### UDP İzleyiciler

UDP tracker'lar 2025 yılında standartlaştırıldı (Öneri 160).

**Birincil UDP Tracker'lar** - `udp://tracker2.postman.i2p/announce` - `udp://opentracker.simp.i2p/a` - `http://opentracker.skank.i2p/a` - `http://opentracker.dg2.i2p/a` ---

## 3. Magnet Bağlantıları

```
magnet:?xt=urn:btih:<infohash>&dn=<name>&tr=http://tracker2.postman.i2p/announce&tr=udp://denpa.i2p/announce&xs=i2p:<destination.b32.i2p>
```
<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>xs=i2p:&lt;dest&gt;</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Explicit I2P destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>tr=</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tracker URLs (HTTP or UDP)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>dn=</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Display name</td>
    </tr>
  </tbody>
</table>
Magnet linkleri yapılandırıldığında I2P ve clearnet üzerinden hibrit swarm'ları destekler.

---

## 4. DHT Uygulamaları

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental overlay</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP-based internal overlay</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Active</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BiglyBT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM v3.3-based</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fully supported</td>
    </tr>
  </tbody>
</table>
---

## 5. İstemci Uygulamaları

### I2PSnark

- Tüm router'larla birlikte gelir
- Yalnızca HTTP tracker desteği
- `http://127.0.0.1:7658/` adresinde yerleşik tracker
- UDP tracker desteği yok

### BiglyBT

- I2P eklentisi ile tam özellikli
- HTTP + UDP tracker'ları destekler
- Hibrit torrent desteği
- SAM v3.3 arayüzünü kullanır

### Tixati / XD

- Hafif istemciler
- SAM tabanlı tünelleme
- Deneysel ML-KEM hibrit şifreleme

---

## 6. Yapılandırma

### I2PSnark

```
i2psnark.dir=/home/user/torrents
i2psnark.autostart=true
i2psnark.maxUpBW=128
i2psnark.maxDownBW=256
i2psnark.enableDHT=false
```
### BiglyBT

```
SAMHost=127.0.0.1
SAMPort=7656
SAMNickname=BiglyBT-I2P
SAMAutoStart=true
DHTEnabled=true
```
---

## 7. Güvenlik Modeli

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encryption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2 / SSU2 with X25519+ML-KEM hybrid</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Identity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P destinations replace IP addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Anonymity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Peer info hidden; traffic multiplexed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Leak Prevention</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Remove headers (X-Forwarded-For, Client-IP, Via)</td>
    </tr>
  </tbody>
</table>
Hibrit (clearnet + I2P) torrentler yalnızca anonimliğin kritik olmadığı durumlarda kullanılmalıdır.

---

## 8. Performans

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Factor</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Impact</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommendation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adds latency</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1-hop client, 2-hop server</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Peers</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Boosts speed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20+ active peers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Compression</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal gain</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Usually off</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router-limited</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default settings optimal</td>
    </tr>
  </tbody>
</table>
Tipik hızlar, eş sayısına ve ağ koşullarına bağlı olarak **30–80 KB/s** arasında değişir.

---

## 9. Bilinen Sorunlar

- Java I2P ve i2pd arasında kısmi DHT birlikte çalışabilirliği  
- Yüksek yük altında Magnet metadata getirme gecikmesi  
- NTCP1 kullanımdan kaldırıldı ancak eski eşler tarafından hala kullanılıyor  
- Streaming üzerinden simüle edilen UDP gecikmeyi artırıyor

---

## 10. Gelecek Yol Haritası

- QUIC benzeri çoklama  
- Tam ML-KEM entegrasyonu  
- Birleşik hibrit swarm mantığı  
- İyileştirilmiş reseed yansıları  
- Uyarlanabilir DHT yeniden denemeleri

---

## Referanslar

- [BEP 15 – UDP Tracker Protocol](https://www.bittorrent.org/beps/bep_0015.html)
- [Öneri 160 – I2P Üzerinden UDP Tracker](/proposals/160-udp-trackers/)
- [I2PSnark Belgeleri](/docs/applications/bittorrent/)
- [Streaming Kütüphanesi Spesifikasyonu](/docs/specs/streaming/)

---
