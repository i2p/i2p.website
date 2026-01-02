---
title: "BitTorrent عبر I2P"
description: "نظرة عامة تفصيلية للمواصفات والنظام البيئي لـ BitTorrent داخل شبكة I2P"
slug: "bittorrent"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## نظرة عامة

يتيح BitTorrent عبر I2P مشاركة الملفات المجهولة من خلال tunnels مشفرة باستخدام طبقة البث المباشر في I2P. يتم تحديد جميع المشاركين بواسطة وجهات I2P تشفيرية بدلاً من عناوين IP. يدعم النظام متتبعات HTTP و UDP، وروابط magnet الهجينة، والتشفير الهجين ما بعد الكم.

---

## 1. مكدس البروتوكول

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
تعمل جميع الاتصالات عبر طبقة النقل المشفرة في I2P (NTCP2 أو SSU2). حتى حزم متتبع UDP يتم تغليفها داخل بث I2P.

---

## 2. المتتبعات

### متتبعات HTTP

متتبعات `.i2p` القياسية تستجيب لطلبات HTTP GET مثل:

```
http://tracker2.postman.i2p/announce?info_hash=<20-byte>&peer_id=<20-byte>&port=6881&uploaded=0&downloaded=0&left=1234&compact=1
```
الردود **مُشفّرة بصيغة bencoded** وتستخدم hashes وجهات I2P للأقران.

### متتبعات UDP

تم توحيد معايير متتبعات UDP في عام 2025 (الاقتراح 160).

**متتبعات UDP الأساسية** - `udp://tracker2.postman.i2p/announce` - `udp://opentracker.simp.i2p/a` - `http://opentracker.skank.i2p/a` - `http://opentracker.dg2.i2p/a` ---

## 3. روابط Magnet

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
روابط Magnet تدعم الأسراب الهجينة عبر I2P والإنترنت العادي عند تكوينها.

---

## 4. تطبيقات DHT

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

## 5. تطبيقات العميل

### I2PSnark

- مُجمّع مع جميع أجهزة الـ router
- دعم tracker عبر HTTP فقط
- tracker مدمج على `http://127.0.0.1:7658/`
- لا يوجد دعم لـ UDP tracker

### BiglyBT

- كامل المميزات مع إضافة I2P
- يدعم متتبعات HTTP + UDP
- دعم التورنت الهجين
- يستخدم واجهة SAM v3.3

### Tixati / XD

- العملاء خفيفو الوزن
- الأنفاق المعتمدة على SAM
- تشفير ML-KEM الهجين التجريبي

---

## 6. التكوين

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

## 7. نموذج الأمان

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
يجب استخدام التورنتات الهجينة (clearnet + I2P) فقط إذا لم تكن إخفاء الهوية أمرًا بالغ الأهمية.

---

## 8. الأداء

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
تتراوح السرعات النموذجية بين **30-80 كيلوبايت/ثانية**، حسب الأقران وظروف الشبكة.

---

## 9. المشاكل المعروفة

- التوافق الجزئي لـ DHT بين Java I2P و i2pd  
- تأخير جلب البيانات الوصفية للـ Magnet تحت الحمل الثقيل  
- NTCP1 مُهمَل لكن لا يزال مستخدمًا من قبل الأقران القدامى  
- UDP المحاكى عبر streaming يزيد من زمن الاستجابة

---

## 10. خارطة الطريق المستقبلية

- تعدد الإرسال شبيه بـ QUIC  
- تكامل كامل لـ ML-KEM  
- منطق سرب هجين موحد  
- تحسين مرايا إعادة البذر (reseed mirrors)  
- إعادة محاولات DHT تكيفية

---

## المراجع

- [BEP 15 – بروتوكول UDP Tracker](https://www.bittorrent.org/beps/bep_0015.html)
- [اقتراح 160 – UDP Tracker عبر I2P](/proposals/160-udp-trackers/)
- [وثائق I2PSnark](/docs/applications/bittorrent/)
- [مواصفات مكتبة Streaming](/docs/specs/streaming/)

---
