---
title: "I2P를 통한 IRC"
description: "I2P IRC 네트워크, 클라이언트, tunnel, 서버 설정 완벽 가이드 (2025년 업데이트)"
slug: "irc"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 개요

**핵심 사항**

- I2P는 터널을 통해 IRC 트래픽에 대한 **종단간 암호화**를 제공합니다. clearnet으로 outproxy하는 경우가 아니라면 IRC 클라이언트에서 **SSL/TLS를 비활성화**하세요.
- 사전 구성된 **Irc2P** 클라이언트 터널은 기본적으로 **127.0.0.1:6668**에서 수신 대기합니다. IRC 클라이언트를 해당 주소와 포트로 연결하세요.
- "router‑provided TLS"라는 용어를 사용하지 마세요. "I2P's native encryption" 또는 "end‑to‑end encryption"을 사용하세요.

## 빠른 시작 (Java I2P)

1. `http://127.0.0.1:7657/i2ptunnel/`에서 **Hidden Services Manager**를 열고 **Irc2P** tunnel이 **실행 중**인지 확인하세요.
2. IRC 클라이언트에서 **server** = `127.0.0.1`, **port** = `6668`, **SSL/TLS** = **off**로 설정하세요.
3. 연결한 후 `#i2p`, `#i2p-dev`, `#i2p-help`와 같은 채널에 참여하세요.

**i2pd** 사용자(C++ router)의 경우, `tunnels.conf`에 client tunnel을 생성하세요(아래 예시 참조).

## 네트워크와 서버

### IRC2P (main community network)

- 연합 서버: `irc.postman.i2p:6667`, `irc.echelon.i2p:6667`, `irc.dg.i2p:6667`.
- `127.0.0.1:6668`의 **Irc2P** tunnel은 이들 중 하나에 자동으로 연결됩니다.
- 주요 채널: `#i2p`, `#i2p-chat`, `#i2p-dev`, `#i2p-help`.

### Ilita network

- 서버: `irc.ilita.i2p:6667`, `irc.r4sas.i2p:6667`, `irc.acetone.i2p:6667`, `rusirc.ilita.i2p:6667`.
- 주요 언어: 러시아어 및 영어. 일부 호스트에서 웹 프론트엔드를 제공합니다.

## Client setup

### Recommended, actively maintained

- **WeeChat (터미널)** — 강력한 SOCKS 지원; 스크립팅이 용이함.
- **Pidgin (데스크톱)** — 여전히 유지보수 중; Windows/Linux에서 잘 작동함.
- **Thunderbird Chat (데스크톱)** — ESR 128+ 버전부터 지원됨.
- **The Lounge (자체 호스팅 웹)** — 최신 웹 클라이언트.

### IRC2P (메인 커뮤니티 네트워크)

- **LimeChat** (무료, 오픈 소스).
- **Textual** (App Store에서 유료 판매, 직접 빌드 가능한 소스 제공).

### Ilita 네트워크

#### WeeChat via SOCKS5

```
/proxy add i2p socks5 127.0.0.1 4447
/set irc.server.i2p.addresses "127.0.0.1/6668"
/set irc.server.i2p.proxy "i2p"
/connect i2p
```
#### Pidgin

- 프로토콜: **IRC**
- 서버: **127.0.0.1**
- 포트: **6668**
- 암호화: **off**
- 사용자명/닉네임: 아무거나

#### Thunderbird Chat

- 계정 유형: **IRC**
- 서버: **127.0.0.1**
- 포트: **6668**
- SSL/TLS: **off**
- 선택사항: 연결 시 채널 자동 참가

#### Dispatch (SAM v3)

`config.toml` 기본값 예시:

```
[defaults]
name = "Irc2P"
host = "irc.postman.i2p"
port = 6667
channels = ["#i2p","#i2p-dev"]
ssl = false
```
## Tunnel configuration

### Java I2P defaults

- Irc2P 클라이언트 터널: **127.0.0.1:6668** → **포트 6667**의 업스트림 서버.
- Hidden Services Manager: `http://127.0.0.1:7657/i2ptunnel/`.

### 권장됨, 활발히 유지 관리됨

`~/.i2pd/tunnels.conf`:

```
[IRC-IRC2P]
type = client
address = 127.0.0.1
port = 6668
destination = irc.postman.i2p
destinationport = 6667
keys = irc-keys.dat
```
Ilita용 별도 터널 (예시):

```
[IRC-ILITA]
type = client
address = 127.0.0.1
port = 6669
destination = irc.ilita.i2p
destinationport = 6667
keys = irc-ilita-keys.dat
```
### macOS 옵션

- Java I2P에서 **SAM 활성화** (기본적으로 비활성화됨) - `/configclients` 또는 `clients.config`에서 설정.
- 기본값: **127.0.0.1:7656/TCP** 및 **127.0.0.1:7655/UDP**.
- 권장 암호화: `SIGNATURE_TYPE=7` (Ed25519) 및 `i2cp.leaseSetEncType=4,0` (ECIES‑X25519 + ElGamal 폴백) 또는 최신 버전 전용인 경우 `4`만 사용.

### 예제 구성

- Java I2P 기본값: **인바운드 2개 / 아웃바운드 2개**.
- i2pd 기본값: **인바운드 5개 / 아웃바운드 5개**.
- IRC의 경우: **각각 2–3개**면 충분하며, 라우터 간 일관된 동작을 위해 명시적으로 설정하세요.

## 클라이언트 설정

- **내부 I2P IRC 연결에는 SSL/TLS를 활성화하지 마세요**. I2P는 이미 종단 간 암호화를 제공합니다. 추가 TLS는 익명성 향상 없이 오버헤드만 증가시킵니다.
- 안정적인 신원 유지를 위해 **영구 키**를 사용하세요. 테스트 중이 아니라면 재시작할 때마다 키를 재생성하지 마세요.
- 여러 앱에서 IRC를 사용하는 경우, 서비스 간 상관관계를 줄이기 위해 **별도 tunnel**(비공유)을 사용하는 것이 좋습니다.
- 원격 제어(SAM/I2CP)를 허용해야 하는 경우, localhost에 바인딩하고 SSH tunnel 또는 인증된 리버스 프록시로 접근을 보호하세요.

## Alternative connection method: SOCKS5

일부 클라이언트는 I2P의 SOCKS5 프록시를 통해 연결할 수 있습니다: **127.0.0.1:4447**. 최상의 결과를 위해서는 6668 포트의 전용 IRC 클라이언트 tunnel을 사용하는 것이 좋습니다. SOCKS는 애플리케이션 계층 식별자를 제거할 수 없으며, 클라이언트가 익명성을 위해 설계되지 않은 경우 정보가 유출될 수 있습니다.

## Troubleshooting

- **연결할 수 없음** — Irc2P tunnel이 실행 중이고 router가 완전히 부트스트랩되었는지 확인하세요.
- **resolve/join에서 멈춤** — SSL이 **비활성화**되어 있고 클라이언트가 **127.0.0.1:6668**을 가리키는지 다시 확인하세요.
- **높은 지연시간** — I2P는 설계상 지연시간이 높습니다. tunnel 수량을 적절하게 유지하고(2–3개) 빠른 재연결 루프를 피하세요.
- **SAM 앱 사용** — SAM이 활성화되어 있는지(Java) 또는 방화벽에 차단되지 않았는지(i2pd) 확인하세요. 장시간 유지되는 세션을 권장합니다.

## Appendix: Ports and naming

- 일반적인 IRC 터널 포트: **6668** (Irc2P 기본값), **6667** 및 **6669** (대체 포트).
- `.b32.i2p` 호스트명: 52자 표준 형식; LS2/고급 인증서용 56자 이상 확장 형식도 존재. 명시적으로 b32 주소가 필요한 경우가 아니면 `.i2p` 호스트명을 사용하세요.
