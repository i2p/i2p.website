---
title: "SAM v3"
description: "비-Java I2P 애플리케이션을 위한 안정적인 브리지 프로토콜"
slug: "samv3"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

SAM v3("Simple Anonymous Messaging")는 현재 **안정적이고 라우터 독립적인 API**로, 외부 애플리케이션이 라우터 자체를 내장하지 않고도 I2P 네트워크와 통신할 수 있게 해줍니다. **스트림**, **데이터그램**, **원시 메시지**에 대한 통합 접근을 제공하며, 비Java 소프트웨어를 위한 정식 브리지 레이어로 남아 있습니다.

## 1. 개요 및 목적

SAM v3는 개발자들이 경량 TCP/UDP 프로토콜을 사용하여 어떤 언어로든 I2P 인식 소프트웨어를 구축할 수 있게 합니다. router 내부 구조를 추상화하여 TCP(7656)와 UDP(7655)를 통해 최소한의 명령어 집합을 노출합니다. **Java I2P**와 **i2pd** 모두 SAM v3 사양의 하위 집합을 구현하지만, i2pd는 2025년 현재 대부분의 3.2 및 3.3 확장 기능이 여전히 부족합니다.

## 2. 버전 이력

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.7.3 (May 2009)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Streams + Datagrams; binary destinations; `SESSION CREATE STYLE=` parameter.</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.1</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.14 (Jul 2014)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature type negotiation via `SIGNATURE_TYPE`; improved `DEST GENERATE`.</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.24 (Jan 2016)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per session encryption + tunnel options; `STREAM CONNECT ID` support.</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.3</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.25 (Mar 2016)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PRIMARY / SUBSESSION architecture; multiplexing; improved datagrams.</td></tr>
  </tbody>
</table>
### 명명 참고사항

- **Java I2P**는 `PRIMARY/SUBSESSION`을 사용합니다.
- **i2pd**와 **I2P+**는 하위 호환성을 위해 레거시 `MASTER/SUBSESSION` 용어를 계속 사용합니다.

## 3. 핵심 워크플로우

### 버전 협상

```
HELLO VERSION MIN=3.1 MAX=3.3
HELLO REPLY RESULT=OK VERSION=3.3
```
### 목적지 생성

```
DEST GENERATE SIGNATURE_TYPE=7
```
- `SIGNATURE_TYPE=7` → **Ed25519 (EdDSA SHA512)**. I2P 0.9.15 이후 강력히 권장됩니다.

### 세션 생성

```
SESSION CREATE STYLE=STREAM DESTINATION=NAME     OPTION=i2cp.leaseSetEncType=4,0     OPTION=inbound.quantity=3     OPTION=outbound.quantity=3
```
- `i2cp.leaseSetEncType=4,0` → `4`는 X25519 (ECIES X25519 AEAD Ratchet)이고 `0`은 호환성을 위한 ElGamal 폴백입니다.
- 일관성을 위한 명시적 tunnel 수량: Java I2P 기본값 **2**, i2pd 기본값 **5**.

### 프로토콜 작동

```
STREAM CONNECT ID=1 DESTINATION=b32address.i2p
STREAM SEND ID=1 SIZE=128
STREAM CLOSE ID=1
```
핵심 메시지 유형에는 다음이 포함됩니다: `STREAM CONNECT`, `STREAM ACCEPT`, `STREAM FORWARD`, `DATAGRAM SEND`, `RAW SEND`, `NAMING LOOKUP`, `DEST LOOKUP`, `PING`, `QUIT`.

### 정상 종료

```
QUIT
```
## 4. 구현 차이점 (Java I2P vs i2pd)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Java I2P 2.10.0</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">i2pd 2.58.0 (Sept&nbsp;2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SAM enabled by default</td><td style="border:1px solid var(--color-border); padding:0.5rem;">❌ Requires manual enable in router console</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✅ Enabled via `enabled=true` in `i2pd.conf`</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Default ports</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP 7656 / UDP 7655</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Same</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">AUTH / USER / PASSWORD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PING / PONG keepalive</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">QUIT / STOP / EXIT commands</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">FROM_PORT / TO_PORT / PROTOCOL</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PRIMARY/SUBSESSION support</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ (since 0.9.47)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Absent</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SESSION ADD / REMOVE</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2 / Datagram3 support</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ (since 2.9.0)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSL/TLS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Optional</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ None</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Default tunnel quantities</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Inbound/outbound=2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Inbound/outbound=5</td></tr>
  </tbody>
</table>
**권장 사항:** 라우터 간 일관성을 보장하기 위해 항상 터널 수량을 명시적으로 지정하십시오.

## 5. 지원되는 라이브러리 (2025년 현황)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maintenance Status (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">libsam3</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">C</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Maintained by I2P Project (eyedeekay)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">i2psam</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal updates since 2019</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/go-i2p/sam3">sam3</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active; migrated from `eyedeekay/sam3`</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/go-i2p/onramp">onramp</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actively maintained (2025)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2plib">i2plib</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Modern async replacement for `i2p.socket`</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">i2p.socket</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Abandoned (last release 2017)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://i2pgit.org/robin/Py2p">Py2p</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unverified/inactive</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">i2p-rs</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental; unstable API</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">@diva.exchange/i2p-sam</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">TypeScript / JS</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Most actively maintained (2024–2025)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/I2PSharp">I2PSharp</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Functional; light maintenance</td></tr>
  </tbody>
</table>
## 6. 다가오는 기능 및 새로운 기능 (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NAMING LOOKUP `OPTIONS=true`</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2 / Datagram3 formats</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✓ (Java only)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid crypto (ML KEM)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Optional</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java 17+ runtime requirement</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Planned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.11.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P over Tor blocking</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Active</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Improved floodfill selection</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Active</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0+</td></tr>
  </tbody>
</table>
## 7. 보안 및 구성 참고사항

- SAM을 `127.0.0.1`에만 바인딩하세요.
- 지속적인 서비스의 경우, 정적 키와 함께 **PRIMARY** 세션을 사용하세요.
- 기능 지원을 테스트하려면 `HELLO VERSION`을 사용하세요.
- router 활성 상태를 확인하려면 `PING` 또는 `NAMING LOOKUP`을 사용하세요.
- 인증되지 않은 원격 SAM 연결을 피하세요 (i2pd에는 TLS가 없음).

## 8. 참고 자료 및 사양

- [SAM v3 사양](/docs/api/samv3/)
- [SAM v2 (레거시)](/docs/legacy/samv2/)
- [Streaming 사양](/docs/specs/streaming/)
- [데이터그램](/docs/api/datagrams/)
- [문서 허브](/docs/)
- [i2pd 문서](https://i2pd.website/docs)

## 9. 요약

SAM v3는 모든 비 Java I2P 애플리케이션을 위한 **권장 브리지 프로토콜**입니다. 안정성, 크로스 언어 바인딩, 그리고 라우터 유형에 관계없이 일관된 성능을 제공합니다.

SAM을 사용하여 개발할 때: - **Ed25519** 서명과 **X25519** 암호화를 사용하세요. - `HELLO VERSION`을 통해 기능 지원을 동적으로 확인하세요. - 특히 Java I2P와 i2pd router를 모두 지원할 때 호환성을 고려하여 설계하세요.
