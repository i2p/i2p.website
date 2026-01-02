---
title: "I2PTunnel"
description: "I2P와 인터페이스하고 서비스를 제공하기 위한 도구"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 개요

I2PTunnel은 I2P 네트워크에서 서비스를 제공하고 인터페이스하기 위한 핵심 I2P 구성 요소입니다. tunnel 추상화를 통해 TCP 기반 및 미디어 스트리밍 애플리케이션이 익명으로 작동할 수 있도록 합니다. tunnel의 목적지는 [hostname](/docs/overview/naming), [Base32](/docs/overview/naming#base32) 또는 전체 destination 키로 정의할 수 있습니다.

설정된 각 tunnel은 로컬에서 수신 대기하며(예: `localhost:port`) I2P 목적지에 내부적으로 연결됩니다. 서비스를 호스팅하려면 원하는 IP와 포트를 가리키는 tunnel을 생성하세요. 해당 I2P destination 키가 생성되어 I2P 네트워크 내에서 서비스에 전역적으로 접근할 수 있게 됩니다. I2PTunnel 웹 인터페이스는 [I2P Router Tunnel Manager](http://localhost:7657/i2ptunnel/)에서 이용할 수 있습니다.

---

## 기본 서비스

### 서버 터널

- **I2P Webserver** – I2P에서 쉽게 호스팅할 수 있도록 [localhost:7658](http://localhost:7658)의 Jetty 웹서버로 연결되는 tunnel입니다.  
  - **Unix:** `$HOME/.i2p/eepsite/docroot`  
  - **Windows:** `%LOCALAPPDATA%\I2P\I2P Site\docroot` → `C:\Users\<username>\AppData\Local\I2P\I2P Site\docroot`

### 클라이언트 터널

- **I2P HTTP Proxy** – `localhost:4444` – outproxy를 통해 I2P 및 인터넷을 탐색하는 데 사용됩니다.
- **I2P HTTPS Proxy** – `localhost:4445` – HTTP proxy의 보안 버전입니다.
- **Irc2P** – `localhost:6668` – 기본 익명 IRC 네트워크 tunnel입니다.
- **Git SSH (gitssh.idk.i2p)** – `localhost:7670` – 저장소 SSH 접근을 위한 클라이언트 tunnel입니다.
- **Postman SMTP** – `localhost:7659` – 발신 메일을 위한 클라이언트 tunnel입니다.
- **Postman POP3** – `localhost:7660` – 수신 메일을 위한 클라이언트 tunnel입니다.

> 참고: I2P 웹서버만이 기본 **server tunnel**이며, 나머지는 모두 외부 I2P 서비스에 연결하는 클라이언트 터널입니다.

---

## 설정

I2PTunnel 구성 사양은 [/spec/configuration](/docs/specs/configuration/)에 문서화되어 있습니다.

---

## 클라이언트 모드

### 표준

I2P destination의 서비스에 연결하는 로컬 TCP 포트를 엽니다. 중복성을 위해 쉼표로 구분된 여러 destination 항목을 지원합니다.

### HTTP

HTTP/HTTPS 요청을 위한 프록시 터널입니다. 로컬 및 원격 outproxy, 헤더 제거, 캐싱, 인증 및 투명한 압축을 지원합니다.

**개인정보 보호 기능:**   - 헤더 제거: `Accept-*`, `Referer`, `Via`, `From`   - 호스트 헤더를 Base32 destination으로 교체   - RFC 준수 hop-by-hop 제거 강제 적용   - 투명한 압축 해제 지원 추가   - 내부 오류 페이지 및 현지화된 응답 제공

**압축 동작:**   - 요청은 커스텀 헤더 `X-Accept-Encoding: x-i2p-gzip`을 사용할 수 있습니다   - `Content-Encoding: x-i2p-gzip`이 포함된 응답은 투명하게 압축 해제됩니다   - 압축은 효율성을 위해 MIME 타입과 응답 길이로 평가됩니다

**지속성 (2.5.0부터 새로 추가):**   HTTP Keepalive와 지속 연결이 이제 Hidden Services Manager를 통해 I2P 호스팅 서비스에서 지원됩니다. 이는 지연 시간과 연결 오버헤드를 줄이지만 아직 모든 홉에서 RFC 2616 완전 준수 지속 소켓을 활성화하지는 않습니다.

**파이프라이닝:**   지원되지 않으며 불필요합니다. 최신 브라우저에서는 이미 사용 중단되었습니다.

**User-Agent 동작:**   - **Outproxy:** 최신 Firefox ESR User-Agent를 사용합니다.   - **Internal:** 익명성 일관성을 위해 `MYOB/6.66 (AN/ON)`을 사용합니다.

### IRC 클라이언트

I2P 기반 IRC 서버에 연결합니다. 프라이버시 보호를 위해 식별자를 필터링하면서 안전한 명령어 하위 집합을 허용합니다.

### SOCKS 4/4a/5

TCP 연결을 위한 SOCKS 프록시 기능을 제공합니다. UDP는 Java I2P에서 구현되지 않았습니다 (i2pd에서만 구현됨).

### 연결

SSL/TLS 연결을 위한 HTTP `CONNECT` 터널링을 구현합니다.

### Streamr

TCP 기반 캡슐화를 통해 UDP 스타일 스트리밍을 활성화합니다. 해당하는 Streamr 서버 터널과 페어링되면 미디어 스트리밍을 지원합니다.

![I2PTunnel Streamr 다이어그램](/images/I2PTunnel-streamr.png)

---

## 서버 모드

### 표준 서버

로컬 IP:포트에 매핑된 TCP destination을 생성합니다.

### HTTP 서버

로컬 웹 서버와 인터페이스하는 destination을 생성합니다. 압축(`x-i2p-gzip`), 헤더 제거 및 DDoS 보호 기능을 지원합니다. 이제 **지속 연결 지원**(v2.5.0+) 및 **스레드 풀링 최적화**(v2.7.0–2.9.0)의 이점을 제공합니다.

### HTTP 양방향

**더 이상 사용되지 않음** – 여전히 작동하지만 권장되지 않습니다. outproxy 없이 HTTP 서버와 클라이언트 역할을 모두 수행합니다. 주로 진단 루프백 테스트에 사용됩니다.

### IRC 서버

IRC 서비스를 위한 필터링된 destination을 생성하며, 클라이언트 destination 키를 호스트명으로 전달합니다.

### Streamr 서버

I2P를 통해 UDP 스타일 데이터 스트림을 처리하기 위해 Streamr 클라이언트 터널과 결합됩니다.

---

## 새로운 기능 (2.4.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Keepalive/Persistent Connections</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP tunnels now support persistent sockets for I2P-hosted services, improving performance.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling Optimization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0-2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced CPU overhead and latency by improving thread management.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-Quantum Encryption (ML-KEM)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional hybrid X25519+ML-KEM encryption to resist future quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Segmentation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Isolates I2PTunnel contexts for improved security and privacy.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Removal / SSU2 Adoption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0-2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Upgraded transport layer; transparent to users.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor Blocking</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents inefficient and unstable I2P-over-Tor routing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Browser Proxy (Proposal 166)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced identity-aware proxy mode; details pending confirmation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 Requirement (upcoming)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.11.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Future release will require Java 17+.</td>
    </tr>
  </tbody>
</table>
---

## 보안 기능

- 익명성을 위한 **헤더 제거** (Accept, Referer, From, Via)
- in/outproxy에 따른 **User-Agent 무작위화**
- **POST 속도 제한** 및 **Slowloris 보호**
- 스트리밍 하위 시스템의 **연결 조절**
- tunnel 계층의 **네트워크 혼잡 처리**
- 애플리케이션 간 유출 방지를 위한 **NetDB 격리**

---

## 기술 세부사항

- 기본 destination 키 크기: 516바이트 (확장된 LS2 인증서의 경우 초과 가능)  
- Base32 주소: `{52–56+ chars}.b32.i2p`  
- Server tunnel은 Java I2P와 i2pd 모두와 호환성 유지  
- 사용 중단된 기능: `httpbidirserver`만 해당; 0.9.59 이후 제거된 항목 없음  
- 모든 플랫폼에서 기본 포트 및 document root가 올바른지 검증 완료

---

## 요약

I2PTunnel은 I2P와 애플리케이션 통합의 핵심으로 남아 있습니다. 0.9.59와 2.10.0 사이에서 지속적 연결 지원, 포스트 양자 암호화, 그리고 주요 스레딩 개선 사항이 추가되었습니다. 대부분의 구성은 호환성을 유지하지만, 개발자는 현대적인 전송 및 보안 기본값을 준수하는지 확인하기 위해 설정을 검증해야 합니다.
