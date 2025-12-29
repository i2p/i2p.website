---
title: "I2P 네트워크 프로토콜 (I2NP)"
description: "I2P 내부의 router 간 메시지 형식, 우선순위 및 크기 제한"
slug: "i2np"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 개요

I2P 네트워크 프로토콜(I2NP)은 routers가 메시지를 교환하고, 전송 프로토콜을 선택하며, 익명성을 보존하면서 트래픽을 혼합하는 방법을 정의합니다. 이는 **I2CP** (클라이언트 API)와 전송 프로토콜(**NTCP2** 및 **SSU2**) 사이에서 동작합니다.

I2NP는 I2P 전송 프로토콜 위에 있는 계층이다. 이는 다음을 위한 router 간 프로토콜이다: - 네트워크 데이터베이스 조회 및 응답 - tunnel 생성 - 암호화된 router 및 클라이언트 데이터 메시지

I2NP 메시지는 다른 router로 점대점으로 전송되거나, tunnel을 통해 해당 router로 익명으로 전송될 수 있다.

Routers는 로컬 우선순위를 사용하여 발신 작업을 대기열에 넣습니다. 우선순위 번호가 높을수록 먼저 처리됩니다. 표준 tunnel 데이터 우선순위(400)를 초과하는 것은 긴급으로 취급됩니다.

### 현재 전송 프로토콜

I2P는 이제 IPv4와 IPv6 모두에서 **NTCP2** (TCP)와 **SSU2** (UDP)를 사용합니다. 두 전송 프로토콜 모두 다음을 사용합니다: - **X25519** 키 교환 (Noise 프로토콜 프레임워크) - **ChaCha20/Poly1305** 인증된 암호화 (AEAD) - **SHA-256** 해싱

**레거시 전송 프로토콜(transport) 제거됨:** - NTCP (원래의 TCP)는 Java router 0.9.50 릴리스(2021년 5월)에서 제거되었습니다 - SSU v1 (원래의 UDP)는 Java router 2.4.0 릴리스(2023년 12월)에서 제거되었습니다 - SSU v1은 i2pd 2.44.0 릴리스(2022년 11월)에서 제거되었습니다

2025년 기준, 네트워크는 레거시 전송을 전혀 지원하지 않고, 전부 Noise(프로토콜 프레임워크) 기반 전송으로 완전히 전환되었습니다.

---

## 버전 번호 체계

**중요:** I2P는 이중 버전 관리 시스템을 사용하며, 이를 명확히 이해해야 합니다:

### 릴리스 버전 (사용자 대상)

사용자가 보고 다운로드하는 버전은 다음과 같습니다: - 0.9.50 (2021년 5월) - 마지막 0.9.x 릴리스 - **1.5.0** (2021년 8월) - 첫 1.x 릴리스 - 1.6.0, 1.7.0, 1.8.0, 1.9.0 (2021-2022에 걸쳐) - **2.0.0** (2022년 11월) - 첫 2.x 릴리스 - 2.1.0부터 2.9.0까지 (2023-2025에 걸쳐) - **2.10.0** (2025년 9월 8일) - 현재 릴리스

### API 버전(프로토콜 호환성)

다음은 RouterInfo 속성의 "router.version" 필드에 게시되는 내부 버전 번호입니다: - 0.9.50 (2021년 5월) - **0.9.51** (2021년 8월) - 릴리스 1.5.0용 API 버전 - 0.9.52부터 0.9.66까지 (2.x 릴리스를 통해 계속됨) - **0.9.67** (2025년 9월) - 릴리스 2.10.0용 API 버전

**핵심 사항:** 0.9.51부터 0.9.67까지 번호가 매겨진 릴리스는 전혀 없었습니다. 이 번호들은 API 버전 식별자용으로만 존재합니다. I2P는 0.9.50 릴리스에서 곧바로 1.5.0으로 건너뛰었습니다.

### 버전 매핑 표

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
**예정:** 릴리스 2.11.0 (2025년 12월 예정)은 Java 17+를 요구하며 기본적으로 양자내성 암호를 활성화합니다.

---

## 프로토콜 버전

모든 router는 RouterInfo 속성의 "router.version" 필드에 자신들의 I2NP 프로토콜 버전을 게시해야 합니다. 이 버전 필드는 API 버전으로, 다양한 I2NP 프로토콜 기능에 대한 지원 수준을 나타내며, 반드시 실제 router 버전을 의미하는 것은 아닙니다.

대체(비-Java) router가 실제 router 구현에 대한 버전 정보를 공개하고자 하는 경우, 해당 정보는 다른 속성에 기재해야 한다. 아래에 나열된 것 외의 버전도 허용된다. 지원 여부는 숫자 비교를 통해 결정되며, 예를 들어 0.9.13은 0.9.12 기능 지원을 의미한다.

**참고:** "coreVersion" 속성은 더 이상 router 정보에 포함되지 않으며, I2NP 프로토콜 버전을 결정하는 데 사용된 적이 없습니다.

### API 버전별 기능 요약

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
**참고:** 전송과 관련된 기능 및 호환성 문제도 있습니다. 자세한 내용은 NTCP2 및 SSU2 전송 문서를 참조하십시오.

---

## 메시지 헤더

I2NP는 논리적인 16바이트 헤더 구조를 사용하고, 현대식 전송 프로토콜(NTCP2 및 SSU2)은 중복되는 크기와 체크섬 필드를 생략한 축약된 9바이트 헤더를 사용합니다. 필드는 개념적으로 동일하게 유지됩니다.

### 헤더 형식 비교

**표준 형식 (16바이트):**

레거시 NTCP 전송과 I2NP 메시지가 다른 메시지(TunnelData, TunnelGateway, GarlicClove) 내에 포함될 때 사용됩니다.

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
**SSU용 단축 형식(사용 중단됨, 5바이트):**

```
+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

type :: Integer (1 byte)
short_expiration :: Integer (4 bytes, seconds since epoch)
```
**NTCP2, SSU2, 및 ECIES-Ratchet(키 래칫 메커니즘) garlic 클로브의 단축 형식 (9바이트):**

최신 트랜스포트와 ECIES로 암호화된 garlic 메시지(여러 메시지를 한 덩어리로 묶는 I2P 메시지)에 사용됩니다.

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
### 헤더 필드 세부 정보

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
### 구현 참고 사항

- SSU(사용 중단됨)로 전송될 때는 유형과 4바이트 만료 시간만 포함되었습니다
- NTCP2 또는 SSU2로 전송될 때는 9바이트 짧은 형식이 사용됩니다
- 다른 메시지(Data, TunnelData, TunnelGateway, GarlicClove)에 포함된 I2NP 메시지에는 표준 16바이트 헤더가 필요합니다
- 릴리스 0.8.12부터 효율성을 위해 프로토콜 스택의 일부 지점에서 체크섬 검증이 비활성화되었지만, 호환성을 위해 체크섬 생성은 여전히 필요합니다
- 짧은 만료 값은 부호 없는 값이며 2106년 2월 7일에 순환됩니다. 그 이후에는 올바른 시간을 얻기 위해 오프셋을 추가해야 합니다
- 이전 버전과의 호환성을 위해 검증되지 않을 수 있더라도 항상 체크섬을 생성해야 합니다

---

## 크기 제약 조건

Tunnel 메시지는 I2NP 페이로드를 고정 크기의 조각으로 분할합니다: - **첫 번째 조각:** 약 956바이트 - **이후 조각들:** 각 약 996바이트 - **최대 조각 수:** 64개 (번호 0-63) - **최대 페이로드:** 약 61,200바이트 (61.2 KB)

**계산:** 956 + (63 × 996) = 63,704 바이트의 이론적 최대치이며, 오버헤드로 인해 실제 한계는 약 61,200 바이트입니다.

### 역사적 맥락

이전 전송 방식들은 프레임 크기 제한이 더 엄격했습니다: - NTCP: 16 KB 프레임 - SSU: 약 32 KB 프레임

NTCP2는 약 65 KB 크기의 프레임을 지원하지만, tunnel 단편화 제한은 여전히 적용됩니다.

### 애플리케이션 데이터 고려 사항

Garlic 메시지는 LeaseSets, Session Tags(세션 태그), 또는 암호화된 LeaseSet2 변형을 함께 묶어 포함할 수 있어 페이로드 데이터에 사용할 수 있는 공간이 줄어듭니다.

**권장 사항:** 데이터그램은 신뢰할 수 있는 전달을 보장하기 위해 ≤ 10 KB로 유지하는 것이 좋습니다. 61 KB 제한에 가까운 메시지는 다음과 같은 현상이 발생할 수 있습니다: - 조각화 재조립으로 인한 지연 증가 - 전달 실패 가능성 증가 - 트래픽 분석에 대한 노출 증가

### 단편화 기술적 세부사항

각 tunnel 메시지는 정확히 1,024바이트 (1 KB)이며 다음을 포함합니다: - 4바이트 tunnel ID - 16바이트 초기화 벡터 (IV) - 1,004바이트의 암호화된 데이터

암호화된 데이터 내부에서, tunnel 메시지는 조각 헤더를 통해 다음 정보를 나타내는 단편화된 I2NP 메시지를 포함한다: - 조각 번호 (0-63) - 이것이 첫 번째 조각인지 후속 조각인지 - 재조립을 위한 전체 메시지 ID

첫 번째 프래그먼트에는 전체 I2NP 메시지 헤더(16바이트)가 포함되어 페이로드에 대략 956바이트가 남습니다. 후속 프래그먼트에는 메시지 헤더가 포함되지 않으므로 프래그먼트당 페이로드는 대략 996바이트입니다.

---

## 일반적인 메시지 유형

router는 메시지 유형과 우선순위를 사용해 발신 작업을 스케줄링합니다. 우선순위 값이 높을수록 먼저 처리됩니다. 아래 값은 현재 Java I2P 기본값과 일치합니다(API 버전 0.9.67 기준).

**참고:** 우선순위는 구현에 따라 달라집니다. 공식 우선순위 값은 Java I2P 소스 코드의 `OutNetMessage` 클래스 문서를 참조하십시오.

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
**예약된 메시지 유형:** - 유형 0: 예약됨 - 유형 4-9: 향후 사용을 위해 예약됨 - 유형 12-17: 향후 사용을 위해 예약됨 - 유형 224-254: 실험적 메시지용으로 예약됨 - 유형 255: 향후 확장을 위해 예약됨

### 메시지 유형 참고 사항

- 제어 평면 메시지(DatabaseLookup, TunnelBuild 등)는 보통 클라이언트 tunnels가 아닌 **탐색용 tunnels**을 통해 전달되어, 우선순위를 독립적으로 지정할 수 있다
- 우선순위 값은 대략적이며 구현에 따라 달라질 수 있다
- TunnelBuild (21)와 TunnelBuildReply (22)는 더 이상 권장되지 않지만, 8 hops를 초과하는 매우 긴 tunnels와의 호환성을 위해 여전히 구현되어 있다
- 표준 tunnel 데이터 우선순위는 400이며, 이보다 높은 값은 긴급으로 취급된다
- 현재 네트워크에서 일반적인 tunnel 길이는 3-4 hops이므로, 대부분의 tunnel 빌드는 ShortTunnelBuild (218-byte records) 또는 VariableTunnelBuild (528-byte records)를 사용한다

---

## 암호화 및 메시지 래핑

Routers는 전송 전에 I2NP 메시지를 자주 캡슐화하여 여러 겹의 암호화 계층을 만듭니다. DeliveryStatus 메시지(전달 상태 확인 메시지)는 다음과 같을 수 있습니다: 1. GarlicMessage로 캡슐화됨(암호화됨) 2. DataMessage 내부 3. TunnelData 메시지 내부(다시 암호화됨)

각 hop(네트워크 경유 단계)은 자신의 계층만 복호화한다; 최종 목적지는 가장 내부의 페이로드를 드러낸다.

### 암호화 알고리즘

**레거시(단계적으로 폐지 중):** - ElGamal/AES + 세션 태그 - 비대칭 암호화를 위한 ElGamal-2048 - 대칭 암호화를 위한 AES-256 - 32바이트 세션 태그

**현재(API 0.9.48 기준 표준):** - ECIES-X25519 + ChaCha20/Poly1305 AEAD, 래칫 기반 전방 기밀성 지원 - Noise 프로토콜 프레임워크 (Noise_IK_25519_ChaChaPoly_SHA256 목적지용) - 8바이트 세션 태그 (32바이트에서 축소) - 전방 기밀성을 위한 Signal Double Ratchet algorithm(시그널 더블 래칫 알고리즘) - API 버전 0.9.46 (2020)에 도입 - API 버전 0.9.58 (2023)부터 모든 routers에 의무화

**향후(2.10.0 기준 베타):** - MLKEM (ML-KEM-768)과 X25519를 결합한 양자 내성 하이브리드 암호화 - 고전(클래식) 및 양자 내성 키 합의를 결합한 하이브리드 ratchet(세션 키를 단계적으로 갱신하는 메커니즘) - ECIES-X25519와 하위 호환 - 2.11.0 릴리스(2025년 12월)에서 기본값이 됨

### ElGamal Router 사용 중단 예정

**CRITICAL:** ElGamal routers는 API 버전 0.9.58(릴리스 2.2.0, 2023년 3월)부터 사용 중단되었습니다. 이제 조회할 권장 최소 floodfill 버전이 0.9.58이므로, 구현체는 ElGamal floodfill routers에 대한 암호화를 구현할 필요가 없습니다.

**그러나:** 하위 호환성을 위해 ElGamal 목적지는 여전히 지원됩니다. ElGamal 암호화를 사용하는 클라이언트는 ECIES(타원곡선 통합 암호체계) router를 통해서도 여전히 통신할 수 있습니다.

### ECIES-X25519-AEAD-Ratchet 세부 사항

이는 I2P의 암호화 명세에서의 암호 유형 4입니다. 다음을 제공합니다:

**핵심 기능:** - ratcheting(연쇄적 키 갱신 기법)을 통한 순방향 비밀성(각 메시지마다 새 키) - 세션 태그 저장 공간 축소(8바이트 대 32바이트) - 여러 세션 유형(New Session, Existing Session, One-Time) - Noise protocol(경량 암호 핸드셰이크 프레임워크) Noise_IK_25519_ChaChaPoly_SHA256 기반 - Signal의 Double Ratchet 알고리즘(메시지별 키 갱신 알고리즘)과 통합

**암호학 기본 구성 요소:** - 디피-헬먼 키 합의를 위한 X25519 - 스트림 암호화를 위한 ChaCha20 - 메시지 인증 (AEAD, 연관 데이터가 포함된 인증된 암호화)을 위한 Poly1305 - 해시를 위한 SHA-256 - 키 파생을 위한 HKDF

**세션 관리:** - 신규 세션: 정적 destination key(목적지 키)를 사용하는 초기 연결 - 기존 세션: session tags(세션 태그)를 사용하는 후속 메시지 - 일회성 세션: 오버헤드를 줄이기 위한 단일 메시지 세션

자세한 기술 세부사항은 [ECIES 사양](/docs/specs/ecies/) 및 [제안 144](/proposals/144-ecies-x25519-aead-ratchet/)를 참고하세요.

---

## 공통 구조

다음 구조체들은 여러 I2NP 메시지의 구성 요소입니다. 완전한 메시지는 아닙니다.

### BuildRequestRecord (빌드 요청 레코드) (ElGamal)

**사용 중단됨.** 현재 네트워크에서는 tunnel에 ElGamal router가 포함된 경우에만 사용됩니다. 최신 형식은 [ECIES Tunnel 생성](/docs/specs/implementation/)을 참조하세요.

**목적:** tunnel에서 하나의 홉 생성을 요청하기 위해 사용되는, 여러 개의 레코드로 이루어진 집합 중 하나의 레코드.

**형식:**

ElGamal과 AES로 암호화됨 (총 528바이트):

```
+----+----+----+----+----+----+----+----+
| encrypted data (528 bytes)            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
ElGamal(엘가말)로 암호화된 구조 (528바이트):

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
평문 구조 (암호화 전에 222바이트):

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
**참고:** - ElGamal-2048 암호화는 514바이트 블록을 생성하지만, 패딩 바이트 두 개(위치 0과 257)는 제거되어 최종 크기는 512바이트가 됩니다 - 필드 상세 내용은 [Tunnel 생성 사양](/docs/specs/implementation/)을 참조하세요 - 소스 코드: `net.i2p.data.i2np.BuildRequestRecord` - 상수: `EncryptedBuildRecord.RECORD_SIZE = 528`

### BuildRequestRecord(빌드 요청 레코드) (ECIES-X25519 Long)

ECIES-X25519(타원곡선 통합 암호 방식) routers용이며, API 버전 0.9.48에서 도입되었습니다. 혼합 tunnels과의 하위 호환성을 위해 528바이트를 사용합니다.

**형식:**

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
**총 크기:** 528바이트 (호환성을 위해 ElGamal과 동일)

평문 구조와 암호화 세부 정보는 [ECIES Tunnel Creation](/docs/specs/implementation/)을 참조하세요.

### BuildRequestRecord (빌드 요청 레코드) (ECIES-X25519 단축형)

ECIES-X25519(X25519 기반 ECIES 암호 방식) router에만 해당하며, API 버전 0.9.51(릴리스 1.5.0) 기준입니다. 이는 현재 표준 형식입니다.

**형식:**

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
**총 크기:** 218바이트 (528바이트 대비 59% 감소)

**핵심 차이점:** Short records(짧은 레코드 형식)는 레코드에 키를 명시적으로 포함하는 대신 HKDF (키 유도 함수)를 통해 모든 키를 유도한다. 이에는 다음이 포함된다: - 레이어 키 (tunnel 암호화용) - IV 키 (tunnel 암호화용) - 응답 키 (빌드 응답용) - 응답 IV (빌드 응답용)

모든 키는 X25519 키 교환으로부터 얻은 공유 비밀을 기반으로 Noise 프로토콜의 HKDF(해시 기반 키 유도 함수) 메커니즘을 사용해 파생됩니다.

**장점:** - 짧은 레코드 4개가 하나의 tunnel 메시지(873바이트)에 들어감 - 각 레코드마다 별도의 메시지를 보내는 대신 tunnel 빌드 메시지 3개 - 대역폭과 지연시간 감소 - 긴 형식과 동일한 보안 특성

설계 근거는 [Proposal 157](/proposals/157-new-tbm/)을 참조하고, 완전한 명세는 [ECIES Tunnel Creation](/docs/specs/implementation/)을 참조하세요.

**소스 코드:** - `net.i2p.data.i2np.ShortEncryptedBuildRecord` - 상수: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

### BuildResponseRecord (ElGamal 공개키 암호)

**사용 중단됨.** tunnel에 ElGamal router가 포함된 경우에만 사용됩니다.

**목적:** 빌드 요청에 대한 응답을 담은 여러 레코드로 구성된 집합 중 하나의 레코드.

**형식:**

암호화됨 (528바이트, BuildRequestRecord(빌드 요청 레코드)와 동일한 크기):

```
bytes 0-527 :: AES-encrypted record
```
암호화되지 않은 구조:

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
**응답 코드:** - `0` - 수락 - `30` - 거부 (대역폭 초과)

응답 필드에 대한 자세한 내용은 [Tunnel Creation Specification](/docs/specs/implementation/)을 참조하십시오.

### BuildResponseRecord (빌드 응답 레코드) (ECIES-X25519)

ECIES-X25519 router의 경우, API 버전은 0.9.48+입니다. 해당 요청과 동일한 크기입니다(긴 형식은 528, 짧은 형식은 218).

**형식:**

긴 형식(528바이트):

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
짧은 형식(218바이트):

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
**평문 구조(두 형식 모두):**

매핑 구조(I2P의 키-값 형식)에는 다음이 포함됩니다: - 응답 상태 코드(필수) - 사용 가능한 대역폭 매개변수("b")(선택적, API 0.9.65에서 추가됨) - 향후 확장을 위한 기타 선택적 매개변수

**응답 상태 코드:** - `0` - 성공 - `30` - 거부: 대역폭 초과

전체 명세는 [ECIES Tunnel 생성](/docs/specs/implementation/)을 참조하십시오.

### GarlicClove(I2P garlic encryption의 하위 메시지) (ElGamal/AES)

**경고:** 이는 ElGamal로 암호화된 garlic messages(갈릭 메시지: 여러 cloves를 한 번에 묶어 전달하는 메시지 형식) 내부의 garlic cloves(갈릭 클로브: garlic message를 구성하는 개별 하위 메시지)에 사용되는 형식입니다. ECIES-AEAD-X25519-Ratchet garlic messages 및 garlic cloves의 형식은 이와 크게 다릅니다. 최신 형식은 [ECIES Specification](/docs/specs/ecies/)을 참고하십시오.

**router에서는 더 이상 권장되지 않음 (API 0.9.58+), 목적지에서는 여전히 지원됩니다.**

**형식:**

암호화되지 않음:

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
**참고:** - clove(garlic에서 묶이는 개별 하위 메시지 단위)는 절대 단편화되지 않는다 - Delivery Instructions 플래그 바이트의 첫 번째 비트가 0이면, clove는 암호화되지 않는다 - 첫 번째 비트가 1이면, clove는 암호화된다(미구현 기능) - 최대 길이는 전체 clove 길이들의 합과 최대 GarlicMessage 길이의 함수다 - 인증서는 라우팅에 대한 "지불"을 위해 HashCash에 사용될 수도 있다(향후 가능성) - 실제로 사용되는 메시지: DataMessage, DeliveryStatusMessage, DatabaseStoreMessage - GarlicMessage는 GarlicMessage를 포함할 수 있다(중첩된 garlic), 그러나 실제로는 사용되지 않는다

개념적 개요는 [Garlic Routing(갈릭 라우팅)](/docs/overview/garlic-routing/)을 참조하세요.

### GarlicClove (ECIES-X25519-AEAD-Ratchet)

ECIES-X25519 router와 목적지의 경우, API 버전은 0.9.46+입니다. 이는 현재 표준 형식입니다.

**중요한 차이점:** ECIES garlic은 명시적인 clove(메시지 묶음 내 개별 서브메시지) 구조가 아니라 Noise 프로토콜 블록을 기반으로 한 완전히 다른 구조를 사용합니다.

**형식:**

ECIES(타원곡선 통합 암호화 방식) garlic 메시지(여러 메시지를 묶어 전송하는 I2P 방식의 메시지)에는 일련의 블록이 포함됩니다:

```
Block structure:
+----+----+----+----+----+----+----+----+
|type| length    | data ...
+----+----+----+----+----+-//-

type :: 1 byte block type
length :: 2 bytes block length
data :: variable length data
```
**블록 유형:** - `0` - Garlic Clove Block (갈릭 클로브 블록; I2NP 메시지를 포함) - `1` - DateTime Block (날짜/시간 블록; 타임스탬프) - `2` - Options Block (옵션 블록; 전달 옵션) - `3` - Padding Block (패딩 블록) - `254` - Termination Block (종료 블록; 구현되지 않음)

**Garlic Clove Block(garlic 메시지에서 각 clove를 담는 블록) (type 0):**

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
**ElGamal(엘가말) 형식과의 주요 차이점:** - 8바이트 Date 대신 4바이트 만료 시간(epoch 기준 초 단위)을 사용 - certificate 필드 없음 - type과 length를 포함하는 블록 구조로 감싸짐 - 전체 메시지는 ChaCha20/Poly1305 AEAD로 암호화됨 - ratcheting(래칫 방식)을 통한 세션 관리

Noise Protocol Framework(Noise 프로토콜 프레임워크)와 블록 구조에 대한 자세한 내용은 [ECIES Specification](/docs/specs/ecies/)을 참조하세요.

### Garlic Clove(개별 메시지 단위) 전달 지침

이 형식은 ElGamal 및 ECIES garlic cloves(마늘 메시지의 개별 구성 요소) 모두에 사용됩니다. 이는 포함된 메시지를 전달하는 방법을 지정합니다.

**중대한 경고:** 이 명세는 Garlic Cloves(garlic 메시지의 clove 단위) 내부의 Delivery Instructions(전송 지시사항)에만 해당합니다. "Delivery Instructions"는 Tunnel 메시지 내부에서도 사용되며, 그 형식은 상당히 다릅니다. Tunnel delivery instructions에 대해서는 [Tunnel Message Specification](/docs/specs/implementation/)을 참조하십시오. 이 두 형식을 혼동하지 마십시오.

**형식:**

세션 키와 지연은 사용되지 않으며 존재하지 않으므로, 가능한 길이는 다음 세 가지입니다:
- 1 바이트 (LOCAL)
- 33 바이트 (ROUTER 및 DESTINATION)
- 37 바이트 (TUNNEL)

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
**일반적인 길이:** - 로컬 전달: 1바이트 (플래그만) - ROUTER / 목적지 전달: 33바이트 (플래그 + 해시) - TUNNEL 전달: 37바이트 (플래그 + 해시 + tunnel ID)

**전송 유형 설명:**

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
**구현 참고 사항:** - 세션 키 암호화는 미구현이며 플래그 비트는 항상 0이다 - 지연은 완전히 구현되지 않았으며 플래그 비트는 항상 0이다 - TUNNEL 전달의 경우, 해시는 게이트웨이 router를 식별하며 tunnel ID는 어느 인바운드 tunnel인지를 지정한다 - DESTINATION 전달의 경우, 해시는 대상의 공개 키의 SHA-256이다 - ROUTER 전달의 경우, 해시는 router의 식별자의 SHA-256이다

---

## I2NP 메시지

모든 I2NP 메시지 유형에 대한 포괄적인 메시지 사양.

### 메시지 유형 요약

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
**예약됨:** - 유형 0: 예약됨 - 유형 4-9: 향후 사용을 위해 예약됨 - 유형 12-17: 향후 사용을 위해 예약됨 - 유형 224-254: 실험적 메시지용으로 예약됨 - 유형 255: 향후 확장을 위해 예약됨

---

### DatabaseStore (유형 1)

**Purpose:** 요청되지 않은 데이터베이스 저장, 또는 성공한 DatabaseLookup message(데이터베이스 조회 메시지)에 대한 응답.

**내용:** 압축되지 않은 LeaseSet(목적지 접속 경로 정보 집합), LeaseSet2(2세대 LeaseSet 형식), MetaLeaseSet(여러 LeaseSet을 참조하는 메타 형식), 또는 EncryptedLeaseSet(암호화된 LeaseSet), 또는 압축된 RouterInfo(router 정보).

**응답 토큰으로 포맷:**

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
**응답 토큰 == 0인 형식:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//
```

**소스 코드:** - `net.i2p.data.i2np.DatabaseStoreMessage` - `net.i2p.data.RouterInfo` (RouterInfo(router에 대한 정보) 구조체용) - `net.i2p.data.LeaseSet` (LeaseSet(임대 정보 집합) 구조체용)

---

### DatabaseLookup(데이터베이스 조회) (유형 2)

**목적:** 네트워크 데이터베이스에서 항목을 조회하기 위한 요청입니다. 응답은 DatabaseStore 또는 DatabaseSearchReply 중 하나입니다.

**형식:**

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
**응답 암호화 모드:**

**NOTE:** ElGamal router는 API 0.9.58부터 사용 중단되었습니다. 조회 시 권장되는 최소 floodfill 버전이 이제 0.9.58이므로, 구현체는 ElGamal floodfill router에 대한 암호화를 구현할 필요가 없습니다. ElGamal 목적지는 여전히 지원됩니다.

플래그 비트 4(ECIESFlag)는 비트 1(encryptionFlag)과 조합되어 응답 암호화 모드를 결정하는 데 사용된다:

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
**암호화 없음 (플래그 0,0):**

reply_key, tags, 그리고 reply_tags는 존재하지 않습니다.

**ElG에서 ElG로 (플래그 0,1) - 사용 중단됨:**

0.9.7부터 지원되며, 0.9.58부터 더 이상 권장되지 않습니다.

```
reply_key :: 32 byte SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (1-32, typically 1)
        Number of reply tags that follow

reply_tags :: One or more 32-byte SessionTags
              Each is CSRNG(32) random data
```
**ECIES에서 ElG로 (플래그 1,0) - 사용 중단됨:**

버전 0.9.46부터 지원됨, 버전 0.9.58부터 더 이상 권장되지 않음.

```
reply_key :: 32 byte ECIES SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (required value: 1)
        Number of reply tags that follow

reply_tags :: One 8-byte ECIES SessionTag
              CSRNG(8) random data
```
응답은 [ECIES 사양](/docs/specs/ecies/)에 정의된 ECIES 기존 세션 메시지입니다:

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
**ECIES(타원곡선 통합 암호체계)에서 ECIES로 (플래그 1,0) - 현재 표준:**

ECIES(타원 곡선 통합 암호화 체계) 목적지 또는 router가 ECIES router로 조회 요청을 보냅니다. 0.9.49부터 지원됩니다.

위의 "ECIES to ElG"와 동일한 형식입니다. 조회 메시지 암호화는 [ECIES Routers](/docs/specs/ecies/#routers)에 명시되어 있습니다. 요청자는 익명입니다.

**ECIES(타원곡선 통합 암호 체계)에서 ECIES로, DH(디피-헬먼 키 교환) 사용 (플래그 1,1) - 향후:**

아직 완전히 정의되지 않았습니다. [Proposal 156](/proposals/156-ecies-routers/)를 참조하십시오.

**참고:** - 0.9.16 이전에는 키가 RouterInfo 또는 LeaseSet용일 수 있었습니다(동일한 키 공간, 구분할 플래그 없음) - 암호화된 응답은 응답이 tunnel을 통해 이뤄질 때만 유용합니다 - 대체 DHT 조회 전략이 구현된 경우 포함된 태그 수는 하나보다 클 수 있습니다 - 조회 키와 제외 키는 "실제" 해시이며, 라우팅 키가 아닙니다 - 유형 3, 5, 7(LeaseSet2 variants)은 0.9.38부터 반환될 수 있습니다. [Proposal 123](/proposals/123-new-netdb-entries/)를 참조하세요 - **탐색적 조회 참고:** 탐색적 조회는 키와 가까운 non-floodfill 해시 목록을 반환하도록 정의됩니다. 그러나 구현은 다양합니다: Java는 RI(RouterInfo)에 대해 검색 키를 조회하고 존재하면 DatabaseStore를 반환하지만; i2pd는 그렇지 않습니다. 따라서 이전에 수신한 해시에 대해 탐색적 조회를 사용하는 것은 권장되지 않습니다

**소스 코드:** - `net.i2p.data.i2np.DatabaseLookupMessage` - 암호화: `net.i2p.crypto.SessionKeyManager`

---

### DatabaseSearchReply (데이터베이스 검색 응답) (유형 3)

**목적:** 실패한 DatabaseLookup 메시지에 대한 응답.

**내용:** 요청된 키에 가장 가까운 router 해시 목록.

**형식:**

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
**참고:** - 'from' 해시는 인증되지 않았으며 신뢰할 수 없다 - 반환된 피어 해시는 쿼리 중인 router보다 키에 더 가까울 필요는 없다. 일반 조회에 대한 응답의 경우, 새로운 floodfills(특수 역할의 router)를 발견하고 견고성을 위해 "역방향" 검색(키에서 더 먼 방향)을 수행하는 데 도움이 된다 - 탐색 조회의 경우, 키는 보통 무작위로 생성된다. 응답의 floodfill이 아닌 peer_hashes는 로컬 전체 데이터베이스의 비효율적인 정렬을 피하기 위해 최적화된 알고리즘(예: 가깝지만 반드시 가장 가까운 피어일 필요는 없는 피어들)을 사용해 선택될 수 있다. 캐싱 전략을 사용할 수도 있다. 이는 구현에 따라 달라진다 - **반환되는 해시의 일반적인 개수:** 3 - **반환할 해시의 권장 최대 개수:** 16 - 조회 키, 피어 해시, 그리고 from 해시는 "실제" 해시이며, 라우팅 키가 아니다 - num이 0이면, 더 가까운 피어를 찾지 못했음을 의미한다(막다른 지점)

**소스 코드:** - `net.i2p.data.i2np.DatabaseSearchReplyMessage`

---

### DeliveryStatus(전달 상태) (유형 10)

**Purpose:** 간단한 메시지 수신 확인. 일반적으로 메시지 발신자가 생성하며, 메시지 자체와 함께 Garlic Message(여러 메시지를 묶어 전달하는 I2P 메시지 형식)로 감싸 목적지에서 회신되도록 한다.

**내용:** 전달된 메시지의 ID와 생성 시간 또는 도착 시간.

**형식:**

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
**참고:** - 타임스탬프는 작성자가 항상 현재 시간으로 설정합니다. 하지만 코드에서 이 타임스탬프가 여러 용도로 사용되고 있으며, 앞으로 더 추가될 수 있습니다 - 이 메시지는 SSU에서 세션 수립 확인 용도로도 사용됩니다. 이 경우 메시지 ID는 무작위 값으로 설정되고, "도착 시간"은 현재 네트워크 전역 ID인 2로 설정됩니다(즉, `0x0000000000000002`) - DeliveryStatus(전달 상태 메시지)는 일반적으로 GarlicMessage(갈릭 메시지)에 래핑되어 tunnel을 통해 전송되며, 발신자를 드러내지 않고 수신 확인을 제공합니다 - tunnel 테스트에 사용되어 지연 시간과 신뢰성을 측정합니다

**소스 코드:** - `net.i2p.data.i2np.DeliveryStatusMessage` - 사용 위치: `net.i2p.router.tunnel.InboundEndpointProcessor` tunnel 테스트를 위해

---

### GarlicMessage(갈릭 메시지) (Type 11)

**경고:** 이것은 ElGamal로 암호화된 garlic messages(여러 메시지를 하나로 묶어 전달하는 I2P 방식)에 사용되는 형식입니다. ECIES-AEAD-X25519-Ratchet garlic messages의 형식은 현저히 다릅니다. 최신 형식은 [ECIES Specification](/docs/specs/ecies/)을 참조하세요.

**목적:** 여러 개의 암호화된 I2NP 메시지를 감싸는 데 사용됩니다.

**내용:** 복호화되면 일련의 Garlic Cloves(개별 메시지 단위)와 추가 데이터로 구성되며, Clove Set(클로브 집합)이라고도 한다.

**암호화된 형식:**

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
**복호화된 데이터 (Clove Set, 클로브 집합):**

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

**ECIES-X25519-AEAD-Ratchet 형식 (routers용 현재 표준)의 경우:**

[ECIES 명세](/docs/specs/ecies/) 및 [제안 144](/proposals/144-ecies-x25519-aead-ratchet/)를 참조하십시오.

**소스 코드:** - `net.i2p.data.i2np.GarlicMessage` - 암호화: `net.i2p.crypto.elgamal.ElGamalAESEngine` (사용 중단됨) - 최신 암호화: `net.i2p.crypto.ECIES` 패키지

---

### TunnelData (유형 18)

**목적:** tunnel의 게이트웨이 또는 참가자가 다음 참가자 또는 엔드포인트로 보내는 메시지. 데이터는 고정 길이이며, 분할·배치·패딩 처리되어 암호화된 I2NP 메시지를 포함한다.

**형식:**

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
**페이로드 구조 (1024바이트):**

```
Bytes 0-15: Initialization Vector (IV) for AES encryption
Bytes 16-1023: Encrypted tunnel message data (1008 bytes)
```
**참고:** - TunnelData에 대한 I2NP 메시지 ID는 각 홉마다 새로운 난수로 설정됩니다 - 암호화된 데이터 내부의 tunnel 메시지 형식은 [Tunnel Message Specification](/docs/specs/implementation/)에 정의되어 있습니다 - 각 홉은 CBC 모드의 AES-256을 사용해 한 겹을 복호화합니다 - 복호화된 데이터를 사용하여 각 홉에서 IV(초기화 벡터)가 갱신됩니다 - 전체 크기는 정확히 1,028 바이트입니다(4 tunnelId + 1024 data) - 이는 tunnel 트래픽의 기본 단위입니다 - TunnelData 메시지는 분할된 I2NP 메시지(GarlicMessage, DatabaseStore 등)를 운반합니다

**소스 코드:** - `net.i2p.data.i2np.TunnelDataMessage` - 상수: `TunnelDataMessage.DATA_LENGTH = 1024` - 처리: `net.i2p.router.tunnel.InboundGatewayProcessor`

---

### TunnelGateway (유형 19)

**목적:** 다른 I2NP 메시지를 감싸, 해당 tunnel의 인바운드 게이트웨이에서 tunnel로 전송되도록 한다.

**형식:**

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
**참고:** - 페이로드는 표준 16바이트 헤더를 가진 I2NP 메시지입니다 - 로컬 router에서 여러 tunnel로 메시지를 주입하는 데 사용됩니다 - 필요한 경우 게이트웨이가 포함된 메시지를 조각화합니다 - 조각화 후, 조각들은 TunnelData 메시지로 래핑됩니다 - TunnelGateway는 네트워크를 통해 전송되지 않습니다; 이는 tunnel 처리 이전에 사용되는 내부 메시지 유형입니다

**소스 코드:** - `net.i2p.data.i2np.TunnelGatewayMessage` - 처리: `net.i2p.router.tunnel.OutboundGatewayProcessor`

---

### DataMessage(데이터 메시지) (유형 20)

**목적:** Garlic Messages(갈릭 메시지)와 Garlic Cloves(갈릭 클로브)에서 임의의 데이터(보통 종단 간 암호화된 애플리케이션 데이터)를 캡슐화하는 데 사용됩니다.

**형식:**

```
+----+----+----+----+----+----+-//-+
| length (4)            | data...    |
+----+----+----+----+----+----+-//-+

length :: 4 bytes
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**참고:** - 이 메시지에는 라우팅 정보가 없으며 결코 "unwrapped" 상태로 전송되지 않습니다 - Garlic messages(갈릭 메시지, garlic encryption에서 사용되는 메시지 단위) 내부에서만 사용됩니다 - 일반적으로 종단 간 암호화된 애플리케이션 데이터(HTTP, IRC, email 등)를 포함합니다 - 데이터는 보통 ElGamal/AES 또는 ECIES로 암호화된 페이로드입니다 - tunnel 메시지 단편화 한계로 인해 실사용 가능한 최대 길이는 약 61.2 KB입니다

**소스 코드:** - `net.i2p.data.i2np.DataMessage`

---

### TunnelBuild (유형 21)

**사용 중단됨.** VariableTunnelBuild (type 23) 또는 ShortTunnelBuild (type 25)를 사용하세요.

**목적:** 8홉을 위한 고정 길이 tunnel 빌드 요청.

**형식:**

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
**참고:** - 0.9.48 기준으로 ECIES-X25519 BuildRequestRecords(tunnel 빌드 요청 레코드)를 포함할 수 있습니다. [ECIES Tunnel 생성](/docs/specs/implementation/) - 자세한 내용은 [Tunnel 생성 사양](/docs/specs/implementation/)을 참조하세요 - 이 메시지의 I2NP 메시지 ID는 tunnel 생성 사양에 따라 설정되어야 합니다 - 오늘날의 네트워크에서는 드물게 보이지만(VariableTunnelBuild(가변 길이 tunnel 빌드 메시지 유형)로 대체됨), 매우 긴 tunnel에서는 여전히 사용될 수 있으며 공식적으로 사용 중단(deprecated)되지는 않았습니다 - Routers는 호환성을 위해 여전히 이를 구현해야 합니다 - 고정 8-레코드 형식은 유연성이 떨어지며 더 짧은 tunnel에서는 대역폭을 낭비합니다

**소스 코드:** - `net.i2p.data.i2np.TunnelBuildMessage` - 상수: `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8`

---

### TunnelBuildReply (유형 22)

**사용 중단됨.** VariableTunnelBuildReply (type 24) 또는 OutboundTunnelBuildReply (type 26)를 사용하세요.

**목적:** 8 홉용 고정 길이 tunnel 구축 응답.

**형식:**

TunnelBuildMessage와 동일한 형식이며, BuildRequestRecords 대신 BuildResponseRecords를 사용합니다.

```
Total size: 8 × 528 = 4,224 bytes
```
**참고:** - 0.9.48 기준, ECIES-X25519 BuildResponseRecords(빌드 응답 레코드)를 포함할 수 있습니다. [ECIES Tunnel 생성](/docs/specs/implementation/)을 참조하세요 - 자세한 내용은 [Tunnel 생성 명세](/docs/specs/implementation/)를 참조하세요 - 이 메시지의 I2NP 메시지 ID는 tunnel 생성 명세에 따라 설정되어야 합니다 - 오늘날의 네트워크에서는 드물게 보이지만(VariableTunnelBuildReply(가변 Tunnel 빌드 응답)로 대체됨), 매우 긴 tunnel에서는 여전히 사용될 수 있으며 공식적으로 사용 중단으로 지정되지는 않았습니다 - 호환성을 위해 Routers는 여전히 이를 구현해야 합니다

**소스 코드:** - `net.i2p.data.i2np.TunnelBuildReplyMessage`

---

### VariableTunnelBuild (유형 23)

**목적:** 1~8 홉에 대한 가변 길이 tunnel 구축. ElGamal 및 ECIES-X25519 routers 모두를 지원합니다.

**형식:**

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
**참고:** - 0.9.48 기준, ECIES-X25519 BuildRequestRecords(ECIES-X25519 기반 빌드 요청 레코드)을 포함할 수 있습니다. [ECIES Tunnel 생성](/docs/specs/implementation/) - router 버전 0.7.12(2009)에서 도입 - 0.7.12 이전 버전의 tunnel 참가자에게는 전송되지 않을 수 있습니다 - 자세한 내용은 [Tunnel Creation 명세](/docs/specs/implementation/)를 참조하십시오 - I2NP 메시지 ID는 tunnel 생성 명세에 따라 설정되어야 합니다 - **일반적인 레코드 수:** 4 (4-hop tunnel의 경우) - **일반적인 총 크기:** 1 + (4 × 528) = 2,113 바이트 - 이것은 ElGamal router용 표준 tunnel 빌드 메시지입니다 - ECIES router는 일반적으로 ShortTunnelBuild(type 25)(짧은 tunnel 빌드)를 대신 사용합니다

**소스 코드:** - `net.i2p.data.i2np.VariableTunnelBuildMessage`

---

### VariableTunnelBuildReply (유형 24)

**목적:** 1~8홉용 가변 길이 tunnel 빌드 응답. ElGamal 및 ECIES-X25519 routers를 모두 지원합니다.

**형식:**

BuildRequestRecords 대신 BuildResponseRecords를 사용하는 점을 제외하면 VariableTunnelBuildMessage와 동일한 형식입니다.

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
**참고:** - 0.9.48 기준, ECIES-X25519 BuildResponseRecords(빌드 응답 레코드) 를 포함할 수 있습니다. [ECIES Tunnel Creation](/docs/specs/implementation/)을 참조하세요 - router 버전 0.7.12(2009)에서 도입됨 - 버전 0.7.12 이전의 tunnel 참가자에게는 전송되지 않을 수 있습니다 - 자세한 내용은 [Tunnel Creation Specification](/docs/specs/implementation/)을 참조하세요 - I2NP 메시지 ID는 tunnel 생성 사양에 따라 설정해야 합니다 - **일반적인 레코드 수:** 4 - **일반적인 총 크기:** 2,113 바이트

**소스 코드:** - `net.i2p.data.i2np.VariableTunnelBuildReplyMessage`

---

### ShortTunnelBuild (유형 25)

**목적:** ECIES-X25519 routers 전용의 짧은 tunnel 구축 메시지. API 버전 0.9.51(릴리스 1.5.0, 2021년 8월)에 도입됨. 이는 ECIES tunnel 구축의 현재 표준입니다.

**형식:**

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
**참고:** - router 버전 0.9.51(릴리스 1.5.0, 2021년 8월)에 도입 - API 버전 0.9.51 미만의 tunnel 참가자에게는 전송되지 않을 수 있음 - 전체 사양은 [ECIES Tunnel Creation](/docs/specs/implementation/) 참조 - 설계 근거는 [Proposal 157](/proposals/157-new-tbm/) 참조 - **일반적인 레코드 수:** 4 - **일반적인 총 크기:** 1 + (4 × 218) = 873 바이트 - **대역폭 절감:** VariableTunnelBuild 대비 59% 작음(873 대 2,113 바이트) - **성능 이점:** 짧은 레코드 4개가 하나의 tunnel 메시지에 들어감; VariableTunnelBuild는 3개의 tunnel 메시지가 필요함 - 이는 현재 순수 ECIES-X25519 tunnel에 대한 표준 tunnel 빌드 형식임 - 레코드는 키를 명시적으로 포함하는 대신 HKDF(키 파생 함수)를 통해 파생함

**소스 코드:** - `net.i2p.data.i2np.ShortTunnelBuildMessage` - 상수: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

---

### OutboundTunnelBuildReply (유형 26)

**Purpose:** 새로 생성된 tunnel의 아웃바운드 엔드포인트에서 생성자에게 전송됩니다. ECIES-X25519 routers 전용입니다. API 버전 0.9.51에서 도입되었습니다(릴리스 1.5.0, 2021년 8월).

**형식:**

ShortTunnelBuildMessage와 동일한 형식이며, ShortBuildRequestRecords 대신 ShortBuildResponseRecords를 사용합니다.

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
**참고:** - router 버전 0.9.51에 도입됨(릴리스 1.5.0, 2021년 8월) - 전체 사양은 [ECIES Tunnel 생성](/docs/specs/implementation/)을 참조하십시오 - **일반적인 레코드 수:** 4 - **일반적인 전체 크기:** 873 바이트 - 이 응답은 새로 생성된 outbound tunnel을 통해 outbound endpoint(OBEP, 아웃바운드 엔드포인트)에서 tunnel 생성자로 되돌려 전송됩니다 - 모든 홉이 tunnel 구축을 수락했음을 확인합니다

**소스 코드:** - `net.i2p.data.i2np.OutboundTunnelBuildReplyMessage`

---

## 참고 자료

### 공식 명세

- **[I2NP 사양](/docs/specs/i2np/)** - I2NP 메시지 형식의 완전한 사양
- **[공통 구조](/docs/specs/common-structures/)** - I2P 전반에서 사용되는 데이터 타입과 구조
- **[tunnel 생성](/docs/specs/implementation/)** - ElGamal tunnel 생성(사용 중단됨)
- **[ECIES tunnel 생성](/docs/specs/implementation/)** - ECIES-X25519 tunnel 생성(현재)
- **[tunnel 메시지](/docs/specs/implementation/)** - tunnel 메시지 형식 및 전달 지침
- **[NTCP2 사양](/docs/specs/ntcp2/)** - TCP 전송 프로토콜
- **[SSU2 사양](/docs/specs/ssu2/)** - UDP 전송 프로토콜
- **[ECIES 사양](/docs/specs/ecies/)** - ECIES-X25519-AEAD-Ratchet 암호화
- **[암호학 사양](/docs/specs/cryptography/)** - 저수준 암호 프리미티브
- **[I2CP 사양](/docs/specs/i2cp/)** - 클라이언트 프로토콜 사양
- **[데이터그램 사양](/docs/api/datagrams/)** - Datagram2 및 Datagram3 형식

### 제안서

- **[제안 123](/proposals/123-new-netdb-entries/)** - 새로운 netDB 항목 (LeaseSet2, EncryptedLeaseSet, MetaLeaseSet)
- **[제안 144](/proposals/144-ecies-x25519-aead-ratchet/)** - ECIES-X25519-AEAD-Ratchet 암호화
- **[제안 154](/proposals/154-ecies-lookups/)** - 암호화된 데이터베이스 조회
- **[제안 156](/proposals/156-ecies-routers/)** - ECIES routers
- **[제안 157](/proposals/157-new-tbm/)** - 더 작은 tunnel 빌드 메시지 (짧은 형식)
- **[제안 159](/proposals/159-ssu2/)** - SSU2 트랜스포트
- **[제안 161](/ko/proposals/161-ri-dest-padding/)** - 압축 가능한 패딩
- **[제안 163](/proposals/163-datagram2/)** - Datagram2 및 Datagram3
- **[제안 167](/proposals/167-service-records/)** - LeaseSet 서비스 레코드 매개변수
- **[제안 168](/proposals/168-tunnel-bandwidth/)** - tunnel 빌드 대역폭 매개변수
- **[제안 169](/proposals/169-pq-crypto/)** - 포스트-양자 하이브리드 암호기술

### 문서

- **[Garlic 라우팅](/docs/overview/garlic-routing/)** - 계층화된 메시지 번들링
- **[ElGamal/AES](/docs/legacy/elgamal-aes/)** - 사용 중단된 암호화 방식
- **[Tunnel 구현](/docs/specs/implementation/)** - 단편화 및 처리
- **[네트워크 데이터베이스](/docs/specs/common-structures/)** - 분산 해시 테이블
- **[NTCP2 전송](/docs/specs/ntcp2/)** - TCP 전송 명세
- **[SSU2 전송](/docs/specs/ssu2/)** - UDP 전송 명세
- **[기술 소개](/docs/overview/tech-intro/)** - I2P 아키텍처 개요

### 소스 코드

- **[Java I2P 저장소](https://i2pgit.org/I2P_Developers/i2p.i2p)** - 공식 Java 구현
- **[GitHub 미러](https://github.com/i2p/i2p.i2p)** - Java I2P의 GitHub 미러
- **[i2pd 저장소](https://github.com/PurpleI2P/i2pd)** - C++ 구현

### 주요 소스 코드 위치

**Java I2P (i2pgit.org/I2P_Developers/i2p.i2p):** - `core/java/src/net/i2p/data/i2np/` - I2NP 메시지 구현 - `core/java/src/net/i2p/crypto/` - 암호화 구현 - `router/java/src/net/i2p/router/tunnel/` - Tunnel 처리 - `router/java/src/net/i2p/router/transport/` - 전송 구현

**상수와 값:** - `I2NPMessage.MAX_SIZE = 65536` - I2NP 메시지 최대 크기 - `I2NPMessageImpl.HEADER_LENGTH = 16` - 표준 헤더 크기 - `TunnelDataMessage.DATA_LENGTH = 1024` - tunnel 메시지 페이로드 - `EncryptedBuildRecord.RECORD_SIZE = 528` - 긴 빌드 레코드 - `ShortEncryptedBuildRecord.RECORD_SIZE = 218` - 짧은 빌드 레코드 - `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8` - 빌드당 최대 레코드 수

---

## 부록 A: 네트워크 통계 및 현재 상태

### 네트워크 구성 (2025년 10월 기준)

- **총 routers:** 약 60,000-70,000 (변동)
- **Floodfill routers:** 약 500-700개 활성 상태
- **암호화 유형:**
  - ECIES-X25519: routers 중 >95%
  - ElGamal: routers 중 <5% (더 이상 사용되지 않음, 레거시 전용)
- **전송 채택 현황:**
  - SSU2: >60% 주요 전송
  - NTCP2: ~40% 주요 전송
  - 레거시 전송(SSU1, NTCP): 0% (제거됨)
- **서명 유형:**
  - EdDSA (Ed25519): 대다수
  - ECDSA: 소수
  - RSA: 허용되지 않음 (제거됨)

### 최소 Router 요구 사항

- **API 버전:** 0.9.16+ (네트워크와의 EdDSA 호환성 확보용)
- **권장 최소:** API 0.9.51+ (ECIES 짧은 tunnel 빌드)
- **floodfills(메타데이터를 전파하는 특수 노드)용 현재 최소:** API 0.9.58+ (ElGamal router 사용 중단)
- **예정 요구사항:** Java 17+ (릴리스 2.11.0 기준, 2025년 12월)

### 대역폭 요구 사항

- **최소:** floodfill(네트워크 데이터베이스를 유포하는 특수 노드)용 128 KBytes/sec (N 플래그 이상)
- **권장:** 256 KBytes/sec (O 플래그) 이상
- **Floodfill 요구 사항:**
  - 최소 128 KB/sec 대역폭
  - 안정적인 가동 시간(>95% 권장)
  - 낮은 지연 시간(피어까지 <500ms)
  - 상태 검사 통과(대기열 시간, 작업 지연)

### Tunnel 통계

- **일반적인 tunnel 길이:** 3-4 홉
- **최대 tunnel 길이:** 8 홉 (이론상, 거의 사용되지 않음)
- **일반적인 tunnel 수명:** 10분
- **tunnel 구축 성공률:** 연결성이 좋은 router의 경우 >85%
- **tunnel 구축 메시지 형식:**
  - ECIES(타원곡선 통합 암호화 방식) router: ShortTunnelBuild (218바이트 레코드)
  - 혼합 tunnel: VariableTunnelBuild (528바이트 레코드)

### 성능 지표

- **Tunnel 구축 시간:** 1-3초 (일반적)
- **엔드 투 엔드 지연:** 0.5-2초 (일반적, 총 6-8 홉)
- **처리량:** tunnel 대역폭에 의해 제한됨 (일반적으로 tunnel당 10-50 KB/sec)
- **최대 데이터그램 크기:** 10 KB 권장 (이론상 최대 61.2 KB)

---

## 부록 B: 사용 중단 및 제거된 기능

### 완전히 제거됨 (더 이상 지원되지 않음)

- **NTCP 전송** - 0.9.50 릴리스에서 제거됨 (2021년 5월)
- **SSU v1 전송** - Java I2P의 2.4.0 릴리스에서 제거됨 (2023년 12월)
- **SSU v1 전송** - i2pd의 2.44.0 릴리스에서 제거됨 (2022년 11월)
- **RSA 서명 유형** - API 0.9.28부터 허용되지 않음

### 사용 중단됨(지원되지만 권장하지 않음)

- **ElGamal routers** - API 0.9.58 (2023년 3월)부터 사용 중단됨
  - ElGamal 목적지는 이전 버전과의 호환성을 위해 여전히 지원됨
  - 새로운 routers는 ECIES-X25519만 사용해야 함
- **TunnelBuild (type 21)** - VariableTunnelBuild 및 ShortTunnelBuild로 대체되어 사용 중단됨
  - 매우 긴 tunnels (>8 홉)에는 여전히 구현되어 있음
- **TunnelBuildReply (type 22)** - VariableTunnelBuildReply 및 OutboundTunnelBuildReply로 대체되어 사용 중단됨
- **ElGamal/AES encryption** - ECIES-X25519-AEAD-Ratchet로 대체되어 사용 중단됨
  - 레거시 목적지에서는 여전히 사용됨
- **Long ECIES BuildRequestRecords (528 bytes)** - 짧은 형식 (218 바이트)으로 대체되어 사용 중단됨
  - ElGamal 홉이 포함된 혼합 tunnels에서는 여전히 사용됨

### 레거시 지원 일정

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

## 부록 C: 향후 개발

### 양자내성 암호

**상태:** 2.10.0 릴리스(2025년 9월) 기준 베타이며, 2.11.0(2025년 12월)부터 기본 설정이 됩니다

**구현:** - 전통적인 X25519와 포스트-양자 MLKEM (ML-KEM-768)을 결합한 하이브리드 접근 방식 - 기존 ECIES-X25519 인프라와 하위 호환 - 전통적인 및 포스트-양자(PQ) 키 자료를 모두 사용하는 Signal Double Ratchet(이중 래칫 프로토콜) 사용 - 자세한 내용은 [Proposal 169](/proposals/169-pq-crypto/)를 참조하세요

**마이그레이션 경로:** 1. 릴리스 2.10.0 (2025년 9월): 베타 옵션으로 제공 2. 릴리스 2.11.0 (2025년 12월): 기본적으로 활성화 3. 향후 릴리스: 결국 필수

### 계획된 기능

- **IPv6 개선** - 향상된 IPv6 지원과 전환 메커니즘
- **tunnel별 스로틀링** - 세밀한 tunnel별 대역폭 제어
- **향상된 메트릭** - 더 나은 성능 모니터링과 진단
- **프로토콜 최적화** - 오버헤드 감소와 효율성 향상
- **향상된 floodfill 선택** - 더 나은 네트워크 데이터베이스 분산

### 연구 분야

- **Tunnel 길이 최적화** - 위협 모델 기반의 동적 Tunnel 길이
- **고급 패딩** - 트래픽 분석 저항성 개선
- **새로운 암호화 방식** - 양자 컴퓨팅 위협 대비
- **혼잡 제어** - 네트워크 부하 처리 개선
- **모바일 지원** - 모바일 기기와 네트워크를 위한 최적화

---

## 부록 D: 구현 지침

### 새로운 구현을 위한

**최소 요구 사항:** 1. API 버전 0.9.51+ 기능 지원 2. ECIES-X25519-AEAD-Ratchet 암호화 구현 3. NTCP2 및 SSU2 transports(전송 프로토콜) 지원 4. ShortTunnelBuild 메시지 구현(218바이트 레코드) 5. LeaseSet2 변형 지원(유형 3, 5, 7) 6. EdDSA 서명 사용(Ed25519)

**권장:** 1. 포스트-양자 하이브리드 암호 지원(2.11.0 기준) 2. tunnel별 대역폭 매개변수 구현 3. Datagram2 및 Datagram3 형식 지원(개선된 I2P 데이터그램 형식 버전 2/3) 4. LeaseSets에서 서비스 레코드 옵션 구현 5. /docs/specs/의 공식 사양 준수

**필수 아님:** 1. ElGamal router 지원 (사용 중단됨) 2. 레거시 트랜스포트 지원 (SSU1, NTCP) 3. 긴 ECIES BuildRequestRecords(빌드 요청 레코드; 순수 ECIES tunnels의 경우 528바이트) 4. TunnelBuild/TunnelBuildReply 메시지 (Variable 또는 Short 변형 사용)

### 테스트 및 검증

**프로토콜 준수:** 1. 공식 Java I2P router와 상호운용성 테스트 2. i2pd C++ router와 상호운용성 테스트 3. 명세에 따른 메시지 형식 검증 4. tunnel 구축/해제 사이클 테스트 5. 테스트 벡터로 암호화/복호화 검증

**성능 테스트:** 1. tunnel 구축 성공률을 측정(85% 초과여야 함) 2. 다양한 tunnel 길이(2-8홉)로 테스트 3. 단편화와 재조립을 검증 4. 부하 상태에서 테스트(동시에 여러 개의 tunnel) 5. 종단 간 지연시간을 측정

**보안 테스트:** 1. 암호화 구현을 검증 (테스트 벡터 사용) 2. 리플레이 공격 방지 기능을 테스트 3. 메시지 만료 처리의 유효성 검증 4. 잘못 형식화된 메시지에 대한 테스트 5. 난수 생성이 적절한지 검증

### 구현 시 흔한 함정

1. **혼란스러운 전달 지시 형식** - garlic clove(garlic encryption에서 단일 메시지 조각) vs tunnel 메시지
2. **잘못된 키 도출** - 짧은 빌드 레코드를 위한 HKDF 사용
3. **메시지 ID 처리** - tunnel 빌드에서 올바르게 설정하지 않음
4. **분할 문제** - 61.2 KB의 실질적 한계를 준수하지 않음
5. **엔디언 오류** - Java는 모든 정수에 big-endian을 사용함
6. **만료 처리** - Short 형식은 2106년 2월 7일에 순환(wrap)됨
7. **체크섬 생성** - 검증하지 않더라도 여전히 필요함
