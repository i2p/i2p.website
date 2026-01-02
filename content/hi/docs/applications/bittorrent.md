---
title: "I2P पर BitTorrent"
description: "I2P नेटवर्क के भीतर BitTorrent के लिए विस्तृत विनिर्देश और पारिस्थितिकी तंत्र का अवलोकन"
slug: "bittorrent"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## अवलोकन

I2P पर BitTorrent, I2P की streaming layer का उपयोग करके encrypted tunnels के माध्यम से गुमनाम फ़ाइल साझाकरण सक्षम करता है। सभी peers को IP addresses के बजाय cryptographic I2P destinations द्वारा पहचाना जाता है। यह सिस्टम HTTP और UDP trackers, hybrid magnet links, और post-quantum hybrid encryption का समर्थन करता है।

---

## 1. प्रोटोकॉल स्टैक

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
सभी कनेक्शन I2P की एन्क्रिप्टेड ट्रांसपोर्ट लेयर (NTCP2 या SSU2) के माध्यम से चलते हैं। यहां तक कि UDP tracker पैकेट भी I2P streaming के भीतर encapsulate किए जाते हैं।

---

## 2. ट्रैकर्स

### HTTP ट्रैकर्स

मानक `.i2p` ट्रैकर HTTP GET अनुरोधों का जवाब देते हैं जैसे:

```
http://tracker2.postman.i2p/announce?info_hash=<20-byte>&peer_id=<20-byte>&port=6881&uploaded=0&downloaded=0&left=1234&compact=1
```
प्रतिक्रियाएं **bencoded** होती हैं और peers के लिए I2P destination hashes का उपयोग करती हैं।

### UDP ट्रैकर्स

UDP ट्रैकर्स को 2025 में मानकीकृत किया गया था (प्रस्ताव 160)।

**प्राथमिक UDP ट्रैकर्स** - `udp://tracker2.postman.i2p/announce` - `udp://opentracker.simp.i2p/a` - `http://opentracker.skank.i2p/a` - `http://opentracker.dg2.i2p/a` ---

## 3. मैग्नेट लिंक

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
Magnet links कॉन्फ़िगर किए जाने पर I2P और clearnet में hybrid swarms का समर्थन करते हैं।

---

## 4. DHT कार्यान्वयन

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

## 5. क्लाइंट कार्यान्वयन

### I2PSnark

- सभी routers के साथ बंडल किया गया
- केवल HTTP tracker समर्थन
- `http://127.0.0.1:7658/` पर अंतर्निहित tracker
- कोई UDP tracker समर्थन नहीं

### BiglyBT

- I2P plugin के साथ पूर्ण-सुविधा युक्त
- HTTP + UDP trackers का समर्थन करता है
- हाइब्रिड torrent समर्थन
- SAM v3.3 interface का उपयोग करता है

### Tixati / XD

- हल्के क्लाइंट
- SAM-आधारित tunneling
- प्रायोगिक ML-KEM हाइब्रिड एन्क्रिप्शन

---

## 6. कॉन्फ़िगरेशन

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

## 7. सुरक्षा मॉडल

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
हाइब्रिड (क्लियरनेट + I2P) टॉरेंट का उपयोग केवल तभी किया जाना चाहिए जब गुमनामी महत्वपूर्ण न हो।

---

## 8. प्रदर्शन

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
सामान्य गति **30–80 KB/s** की रेंज में होती है, जो peers और नेटवर्क स्थितियों पर निर्भर करती है।

---

## 9. ज्ञात समस्याएं

- Java I2P और i2pd के बीच आंशिक DHT अंतरसंचालनीयता
- भारी लोड के तहत Magnet मेटाडेटा प्राप्ति में देरी
- NTCP1 को पदावनत किया गया लेकिन पुराने peers द्वारा अभी भी उपयोग में
- streaming के माध्यम से अनुकरणित UDP विलंबता बढ़ाता है

---

## 10. भविष्य की योजना

- QUIC-जैसी मल्टीप्लेक्सिंग  
- पूर्ण ML-KEM एकीकरण  
- एकीकृत हाइब्रिड स्वार्म लॉजिक  
- बेहतर reseed मिरर्स  
- अनुकूली DHT पुनः प्रयास

---

## संदर्भ

- [BEP 15 – UDP Tracker Protocol](https://www.bittorrent.org/beps/bep_0015.html)
- [Proposal 160 – UDP Tracker over I2P](/proposals/160-udp-trackers/)
- [I2PSnark डॉक्स](/docs/applications/bittorrent/)
- [Streaming Library स्पेसिफिकेशन](/docs/specs/streaming/)

---
