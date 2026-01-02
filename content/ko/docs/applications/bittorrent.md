---
title: "I2P를 통한 BitTorrent"
description: "I2P 네트워크 내 BitTorrent에 대한 상세 사양 및 생태계 개요"
slug: "bittorrent"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 개요

I2P 기반 BitTorrent는 I2P의 스트리밍 계층을 사용하여 암호화된 tunnel을 통해 익명 파일 공유를 가능하게 합니다. 모든 피어는 IP 주소 대신 암호화된 I2P destination으로 식별됩니다. 이 시스템은 HTTP 및 UDP 트래커, 하이브리드 마그넷 링크, 양자내성 하이브리드 암호화를 지원합니다.

---

## 1. 프로토콜 스택

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
모든 연결은 I2P의 암호화된 전송 계층(NTCP2 또는 SSU2)을 통해 실행됩니다. UDP 트래커 패킷도 I2P 스트리밍 내에 캡슐화됩니다.

---

## 2. 트래커

### HTTP 트래커

표준 `.i2p` 트래커는 다음과 같은 HTTP GET 요청에 응답합니다:

```
http://tracker2.postman.i2p/announce?info_hash=<20-byte>&peer_id=<20-byte>&port=6881&uploaded=0&downloaded=0&left=1234&compact=1
```
응답은 **bencoded** 형식이며 피어에 대해 I2P destination 해시를 사용합니다.

### UDP 트래커

UDP 트래커는 2025년에 표준화되었습니다 (제안 160).

**주요 UDP 트래커** - `udp://tracker2.postman.i2p/announce` - `udp://opentracker.simp.i2p/a` - `http://opentracker.skank.i2p/a` - `http://opentracker.dg2.i2p/a` ---

## 3. 마그넷 링크

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
마그넷 링크는 구성 시 I2P와 일반 인터넷(clearnet)에 걸친 하이브리드 스웜을 지원합니다.

---

## 4. DHT 구현

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

## 5. 클라이언트 구현

### I2PSnark

- 모든 라우터에 번들로 포함됨
- HTTP 전용 트래커 지원
- `http://127.0.0.1:7658/`에 내장 트래커 제공
- UDP 트래커 미지원

### BiglyBT

- I2P 플러그인이 포함된 모든 기능 지원
- HTTP + UDP tracker 지원
- 하이브리드 토렌트 지원
- SAM v3.3 인터페이스 사용

### Tixati / XD

- 경량 클라이언트
- SAM 기반 터널링
- 실험적 ML-KEM 하이브리드 암호화

---

## 6. 설정

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

## 7. 보안 모델

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
하이브리드(일반 인터넷 + I2P) 토렌트는 익명성이 중요하지 않은 경우에만 사용해야 합니다.

---

## 8. 성능

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
일반적인 속도는 피어 및 네트워크 상태에 따라 **30–80 KB/s** 범위입니다.

---

## 9. 알려진 문제

- Java I2P와 i2pd 간 부분적인 DHT 상호 운용성  
- 높은 부하 상태에서 마그넷 메타데이터 가져오기 지연  
- NTCP1은 더 이상 권장되지 않지만 여전히 오래된 피어에서 사용됨  
- 스트리밍을 통한 UDP 시뮬레이션으로 지연 시간 증가

---

## 10. 향후 로드맵

- QUIC와 유사한 멀티플렉싱  
- 완전한 ML-KEM 통합  
- 통합된 하이브리드 스웜 로직  
- 개선된 재시드 미러  
- 적응형 DHT 재시도

---

## 참고 자료

- [BEP 15 – UDP Tracker Protocol](https://www.bittorrent.org/beps/bep_0015.html)
- [Proposal 160 – UDP Tracker over I2P](/proposals/160-udp-trackers/)
- [I2PSnark 문서](/docs/applications/bittorrent/)
- [Streaming Library 사양](/docs/specs/streaming/)

---
