---
title: "자주 묻는 질문"
description: "포괄적인 I2P FAQ: router 도움말, 설정, reseed, 프라이버시/안전, 성능 및 문제 해결"
slug: "faq"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## I2P Router 도움말

### I2P는 어떤 시스템에서 실행되나요? {#systems}

I2P는 Java 프로그래밍 언어로 작성되었습니다. Windows, Linux, FreeBSD 및 OSX에서 테스트되었으며, Android 포트도 사용할 수 있습니다.

메모리 사용량 측면에서 I2P는 기본적으로 128 MB의 RAM을 사용하도록 구성되어 있습니다. 이는 브라우징과 IRC 사용에 충분합니다. 그러나 다른 활동들은 더 많은 메모리 할당이 필요할 수 있습니다. 예를 들어, 고대역폭 router를 실행하거나, I2P 토렌트에 참여하거나, 트래픽이 많은 hidden service를 제공하려는 경우 더 많은 메모리가 필요합니다.

CPU 사용량 측면에서 I2P는 Raspberry Pi 시리즈의 싱글보드 컴퓨터와 같은 저사양 시스템에서도 실행되도록 테스트되었습니다. I2P는 암호화 기술을 많이 사용하기 때문에, 더 강력한 CPU가 I2P에서 생성되는 워크로드와 시스템의 나머지 작업(예: 운영 체제, GUI, 웹 브라우징과 같은 기타 프로세스)을 처리하는 데 더 적합합니다.

Sun/Oracle Java 또는 OpenJDK 사용을 권장합니다.

### I2P를 사용하려면 Java 설치가 필요한가요? {#java}

네, I2P Core를 사용하려면 Java가 필요합니다. Windows, Mac OSX, Linux용 간편 설치 프로그램에는 Java가 포함되어 있습니다. I2P Android 앱을 실행하는 경우 대부분 Dalvik 또는 ART와 같은 Java 런타임이 설치되어 있어야 합니다.

### "I2P Site"란 무엇이며 브라우저를 어떻게 설정해야 사용할 수 있나요? {#I2P-Site}

I2P 사이트는 I2P 내부에서 호스팅된다는 점을 제외하면 일반 웹사이트와 동일합니다. I2P 사이트는 사람들의 편의를 위해 사람이 읽을 수 있는 비암호화 방식으로 ".i2p"로 끝나는 일반 인터넷 주소와 유사한 주소를 가지고 있습니다. 실제로 I2P 사이트에 연결하려면 암호화가 필요하며, 이는 I2P 사이트 주소가 긴 "Base64" Destinations 및 더 짧은 "B32" 주소이기도 하다는 것을 의미합니다. 올바르게 탐색하려면 추가 구성이 필요할 수 있습니다. I2P 사이트를 탐색하려면 I2P 설치에서 HTTP 프록시를 활성화한 다음 브라우저가 이를 사용하도록 구성해야 합니다. 자세한 내용은 아래의 "Browsers" 섹션 또는 "Browser Configuration" 가이드를 참조하세요.

### 라우터 콘솔의 Active x/y 숫자는 무엇을 의미하나요? {#active}

라우터 콘솔의 Peers 페이지에서 Active x/y와 같은 두 개의 숫자를 볼 수 있습니다. 첫 번째 숫자는 지난 몇 분 동안 메시지를 주고받은 피어의 수입니다. 두 번째 숫자는 최근에 확인된 피어의 수이며, 이 값은 항상 첫 번째 숫자보다 크거나 같습니다.

### 내 라우터의 활성 피어 수가 매우 적은데, 괜찮은가요? {#peers}

네, 특히 라우터가 방금 시작되었을 때는 정상적인 현상입니다. 새로운 라우터는 시작되고 네트워크의 나머지 부분에 연결되는 데 시간이 필요합니다. 네트워크 통합, 가동 시간 및 성능을 개선하려면 다음 설정을 검토하세요:

- **대역폭 공유** - router가 대역폭을 공유하도록 설정되면 다른 router들을 위해 더 많은 트래픽을 라우팅하게 되며, 이는 네트워크의 나머지 부분과의 통합을 돕고 로컬 연결의 성능도 향상시킵니다. 이는 [http://localhost:7657/config](http://localhost:7657/config) 페이지에서 설정할 수 있습니다.
- **네트워크 인터페이스** - [http://localhost:7657/confignet](http://localhost:7657/confignet) 페이지에 특정 인터페이스가 지정되어 있지 않은지 확인하세요. 컴퓨터가 여러 외부 IP 주소를 가진 멀티홈 환경이 아니라면 성능이 저하될 수 있습니다.
- **I2NP protocol** - router가 호스트 운영 체제에 유효한 프로토콜로 연결을 기대하도록 설정되어 있고 네트워크(고급) 설정이 비어 있는지 확인하세요. 네트워크 설정 페이지의 '호스트명' 필드에 IP 주소를 입력하지 마세요. 여기서 선택한 I2NP Protocol은 이미 연결 가능한 주소가 없는 경우에만 사용됩니다. 예를 들어, 미국의 대부분의 Verizon 4G 및 5G 무선 연결은 UDP를 차단하며 UDP를 통해 연결할 수 없습니다. 다른 경우에는 UDP가 사용 가능하더라도 강제로 사용하려고 할 수 있습니다. 나열된 I2NP Protocols에서 합리적인 설정을 선택하세요.

### 특정 유형의 콘텐츠에 반대합니다. 이를 배포, 저장 또는 접근하지 않으려면 어떻게 해야 하나요? {#badcontent}

이러한 콘텐츠는 기본적으로 설치되지 않습니다. 하지만 I2P는 peer-to-peer 네트워크이기 때문에, 우연히 금지된 콘텐츠를 접할 가능성이 있습니다. 다음은 I2P가 귀하의 신념을 침해하는 사항에 불필요하게 연루되지 않도록 방지하는 방법에 대한 요약입니다.

- **배포** - 트래픽은 I2P 네트워크 내부에 한정되며, 귀하는 [exit node](#exit)(우리 문서에서는 outproxy로 지칭)가 아닙니다.
- **저장** - I2P 네트워크는 콘텐츠의 분산 저장을 수행하지 않으며, 이는 사용자가 별도로 설치하고 구성해야 합니다(예: Tahoe-LAFS 사용). 이는 다른 익명 네트워크인 [Freenet](http://freenetproject.org/)의 기능입니다. I2P router를 실행한다고 해서 다른 사람을 위해 콘텐츠를 저장하는 것은 아닙니다.
- **접근** - 귀하의 router는 귀하의 명시적인 지시 없이 어떠한 콘텐츠도 요청하지 않습니다.

### I2P를 차단할 수 있나요? {#blocking}

네, 가장 쉽고 일반적인 방법은 bootstrap 또는 "Reseed" 서버를 차단하는 것입니다. 모든 난독화된 트래픽을 완전히 차단하는 것도 효과가 있지만 (I2P가 아닌 다른 많은 것들도 중단되며, 대부분은 이 정도까지 가려 하지 않습니다). reseed 차단의 경우, Github에 reseed 번들이 있는데, 이를 차단하면 Github도 함께 차단됩니다. 프록시를 통해 reseed할 수 있으며 (Tor를 사용하고 싶지 않다면 인터넷에서 많은 프록시를 찾을 수 있습니다) 또는 오프라인으로 친구 간에 reseed 번들을 공유할 수 있습니다.

### `wrapper.log`에서 Router Console을 로드할 때 "`Protocol family unavailable`" 오류가 표시됩니다 {#protocolfamily}

이 오류는 기본적으로 IPv6를 사용하도록 구성된 일부 시스템에서 네트워크가 활성화된 Java 소프트웨어를 사용할 때 발생할 수 있습니다. 이 문제를 해결하는 몇 가지 방법이 있습니다:

- Linux 기반 시스템에서는 `echo 0 > /proc/sys/net/ipv6/bindv6only` 명령을 실행할 수 있습니다
- `wrapper.config` 파일에서 다음 라인들을 찾으세요:
  ```
  #wrapper.java.additional.5=-Djava.net.preferIPv4Stack=true
  #wrapper.java.additional.6=-Djava.net.preferIPv6Addresses=false
  ```
  해당 라인들이 있다면 "#"을 제거하여 주석을 해제하세요. 라인들이 없다면 "#" 없이 추가하세요.

다른 방법은 `~/.i2p/clients.config`에서 `::1`을 제거하는 것입니다

**경고**: `wrapper.config`에 대한 모든 변경 사항을 적용하려면 router와 wrapper를 완전히 중지해야 합니다. router 콘솔에서 *재시작*을 클릭하는 것만으로는 이 파일을 다시 읽지 않습니다! *종료*를 클릭하고 11분을 기다린 후 I2P를 시작해야 합니다.

### I2P 내의 대부분의 I2P 사이트가 다운되었나요? {#down}

지금까지 생성된 모든 I2P Site를 고려한다면, 네, 대부분은 다운되어 있습니다. 사람들과 I2P Site는 생겨났다가 사라집니다. I2P를 시작하는 좋은 방법은 현재 운영 중인 I2P Site 목록을 확인하는 것입니다. [identiguy.i2p](http://identiguy.i2p)는 활성화된 I2P Site를 추적합니다.

### 왜 I2P가 포트 32000에서 수신 대기하나요? {#port32000}

우리가 사용하는 Tanuki java 서비스 래퍼는 JVM 내부에서 실행되는 소프트웨어와 통신하기 위해 localhost에 바인딩된 이 포트를 엽니다. JVM이 실행될 때 래퍼에 연결할 수 있도록 키가 제공됩니다. JVM이 래퍼에 연결을 설정한 후, 래퍼는 추가 연결을 거부합니다.

자세한 정보는 [wrapper 문서](http://wrapper.tanukisoftware.com/doc/english/prop-port.html)에서 확인할 수 있습니다.

### 브라우저를 어떻게 설정하나요? {#browserproxy}

다양한 브라우저의 프록시 설정은 스크린샷과 함께 별도의 페이지에 있습니다. 브라우저 플러그인 FoxyProxy나 프록시 서버 Privoxy와 같은 외부 도구를 사용한 고급 설정도 가능하지만, 설정에서 정보 유출이 발생할 수 있습니다.

### I2P 내에서 IRC에 어떻게 연결하나요? {#irc}

I2P 내 메인 IRC 서버인 Irc2P로 가는 터널은 I2P 설치 시 생성되며([I2PTunnel 설정 페이지](http://localhost:7657/i2ptunnel/index.jsp) 참조), I2P router가 시작될 때 자동으로 시작됩니다. 연결하려면 IRC 클라이언트가 `localhost 6668`에 연결하도록 설정하세요. HexChat 계열 클라이언트 사용자는 서버 `localhost/6668`로 새 네트워크를 생성할 수 있습니다(프록시 서버를 설정한 경우 "프록시 서버 우회" 옵션을 체크하는 것을 잊지 마세요). Weechat 사용자는 다음 명령어를 사용하여 새 네트워크를 추가할 수 있습니다:

```
/server add irc2p localhost/6668
```
### 내 I2P 사이트를 어떻게 설정하나요? {#myI2P-Site}

가장 쉬운 방법은 router console의 [i2ptunnel](http://127.0.0.1:7657/i2ptunnel/) 링크를 클릭하고 새로운 'Server Tunnel'을 생성하는 것입니다. Tomcat이나 Jetty와 같은 기존 웹서버의 포트로 tunnel 목적지를 설정하여 동적 콘텐츠를 제공할 수 있습니다. 정적 콘텐츠도 제공할 수 있습니다. 이를 위해 tunnel 목적지를 `0.0.0.0 port 7659`로 설정하고 콘텐츠를 `~/.i2p/eepsite/docroot/` 디렉토리에 배치하세요. (Linux가 아닌 시스템에서는 다른 위치에 있을 수 있습니다. router console을 확인하세요.) 'eepsite' 소프트웨어는 I2P 설치 패키지의 일부로 제공되며 I2P가 시작될 때 자동으로 시작되도록 설정되어 있습니다. 이렇게 생성된 기본 사이트는 http://127.0.0.1:7658 에서 접근할 수 있습니다. 하지만 당신의 'eepsite'는 `~/.i2p/eepsite/i2p/eepsite.keys`에 위치한 eepsite 키 파일을 통해 다른 사람들도 접근할 수 있습니다. 자세한 내용은 `~/.i2p/eepsite/README.txt`의 readme 파일을 읽어보세요.

### 집에서 HTML과 CSS만 포함된 웹사이트를 I2P에 호스팅하면 위험한가요? {#hosting}

이는 당신의 적대자와 위협 모델에 따라 다릅니다. 기업의 "프라이버시" 침해, 일반적인 범죄자, 검열만 걱정한다면 실제로 위험하지 않습니다. 법 집행 기관은 정말로 원한다면 아마도 어쨌든 당신을 찾을 것입니다. 일반적인 (인터넷) 가정용 브라우저가 실행 중일 때만 호스팅하면 누가 해당 부분을 호스팅하는지 알아내기가 정말 어려워질 것입니다. I2P 사이트 호스팅은 다른 서비스를 호스팅하는 것과 마찬가지로 생각하세요 - 당신이 직접 구성하고 관리하는 만큼 위험하거나 안전합니다.

참고: i2p 서비스(destination)를 i2p router와 분리하여 호스팅하는 방법이 이미 존재합니다. [작동 방식을](/docs/overview/tech-intro#i2pservices) 이해하고 있다면, 공개적으로 접근 가능한 웹사이트(또는 서비스)를 위한 서버로 별도의 머신을 설정하고, [매우] 안전한 SSH 터널을 통해 웹서버로 포워딩하거나 보안이 적용된 공유 파일시스템을 사용할 수 있습니다.

### I2P는 ".i2p" 웹사이트를 어떻게 찾나요? {#addresses}

I2P 주소록 애플리케이션은 사람이 읽을 수 있는 이름을 서비스와 연결된 장기 destination에 매핑하여, 네트워크 데이터베이스나 DNS 서비스보다는 hosts 파일이나 연락처 목록에 가깝습니다. 또한 로컬 우선 방식으로 작동하며, 인정받는 전역 네임스페이스가 없어 특정 .i2p 도메인이 무엇에 매핑될지는 최종적으로 사용자가 결정합니다. 중간 단계로는 "Jump Service"라는 것이 있는데, 이는 "I2P router가 $SITE_CRYPTO_KEY를 $SITE_NAME.i2p라는 이름으로 호출하도록 허용하시겠습니까?"와 같은 내용의 페이지로 리디렉션하여 사람이 읽을 수 있는 이름을 제공합니다. 주소록에 추가되면, 다른 사람들과 사이트를 공유하는 데 도움이 되는 자체 jump URL을 생성할 수 있습니다.

### 주소록에 주소를 추가하려면 어떻게 하나요? {#addressbook}

방문하려는 사이트의 base32 또는 base64를 최소한 알지 못하면 주소를 추가할 수 없습니다. 사람이 읽을 수 있는 "호스트명"은 base32 또는 base64에 해당하는 암호화 주소의 별칭일 뿐입니다. 암호화 주소가 없으면 I2P 사이트에 접근할 방법이 없으며, 이는 의도된 설계입니다. 아직 주소를 모르는 사람들에게 주소를 배포하는 것은 일반적으로 Jump 서비스 제공자의 책임입니다. 알려지지 않은 I2P 사이트를 방문하면 Jump 서비스 사용이 트리거됩니다. stats.i2p는 가장 신뢰할 수 있는 Jump 서비스입니다.

i2ptunnel을 통해 사이트를 호스팅하는 경우, 아직 jump 서비스에 등록되어 있지 않습니다. 로컬에서 URL을 부여하려면 설정 페이지를 방문하여 "Add to Local Address Book" 버튼을 클릭하세요. 그런 다음 http://127.0.0.1:7657/dns로 이동하여 addresshelper URL을 조회하고 공유하세요.

### I2P는 어떤 포트를 사용하나요? {#ports}

I2P가 사용하는 포트는 2개 섹션으로 나눌 수 있습니다:

1. 다른 I2P router와 통신하는 데 사용되는 인터넷 연결 포트
2. 로컬 연결을 위한 로컬 포트

이는 아래에서 자세히 설명됩니다.

#### 1. 인터넷 연결 포트

참고: 0.7.8 릴리스 이후로, 새로 설치할 때 포트 8887을 사용하지 않습니다. 프로그램을 처음 실행할 때 9000에서 31000 사이의 임의의 포트가 선택됩니다. 선택된 포트는 router [설정 페이지](http://127.0.0.1:7657/confignet)에서 확인할 수 있습니다.

**아웃바운드**

- [설정 페이지](http://127.0.0.1:7657/confignet)에 나열된 임의의 포트에서 임의의 원격 UDP 포트로의 UDP 통신, 응답 허용
- 임의의 높은 포트에서 임의의 원격 TCP 포트로의 TCP 통신
- 포트 123에서의 아웃바운드 UDP 통신, 응답 허용. 이는 I2P의 내부 시간 동기화(SNTP를 통해 - pool.ntp.org의 임의의 SNTP 호스트 또는 사용자가 지정한 다른 서버에 쿼리)에 필요합니다

**인바운드**

- (선택사항, 권장) 임의의 위치에서 [설정 페이지](http://127.0.0.1:7657/confignet)에 명시된 포트로의 UDP 연결
- (선택사항, 권장) 임의의 위치에서 [설정 페이지](http://127.0.0.1:7657/confignet)에 명시된 포트로의 TCP 연결
- 인바운드 TCP는 [설정 페이지](http://127.0.0.1:7657/confignet)에서 비활성화할 수 있습니다

#### 2. 로컬 I2P 포트

로컬 I2P 포트는 별도로 명시된 경우를 제외하고 기본적으로 로컬 연결만 수신합니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PORT</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PURPOSE</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">DESCRIPTION</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1900</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UPnP SSDP UDP multicast listener</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cannot be changed. Binds to all interfaces. May be disabled on <a href="http://127.0.0.1:7657/confignet">confignet</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2827</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A higher level socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a>. May be changed in the bob.config file.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4444</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/0">I2P HTTP Proxy</a> to configure it. Include in your browser's proxy configuration for HTTP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4445</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/1">I2P HTTPS Proxy</a> to configure it. Include in your browser's proxy configuration for HTTPS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6668</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IRC proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A tunnel to the inside-the-I2P IRC network. Disabled by default. Configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/2">irc.postman.i2p (IRC proxy)</a> and may be enabled/disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7654</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2CP (client protocol) port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For advanced client usage. Do not expose to an external network.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7656</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a> and configured on <a href="http://127.0.0.1:7657/sam">sam</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7657 (or 7658 via SSL)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router console</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The router console provides valuable information about your router and the network, in addition to giving you access to configure your router and its associated applications.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7659</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">'eepsite' - an example webserver (Jetty)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Included in the <code>i2pinstall</code> and <code>i2pupdate</code> packages - may be disabled if another webserver is available. May be configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/3">eepsite</a> and disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7660</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel UDP port for SSH</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Required for Grizzled's/novg's UDP support. Instances disabled by default. May be enabled/disabled and configured to use a different port on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">123</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTP Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used by <a href="http://127.0.0.1:7657/confignet">NTP Time Sync</a>. May be disabled/changed.</td>
    </tr>
  </tbody>
</table>
### 내 주소록에 많은 호스트가 누락되어 있습니다. 좋은 구독 링크에는 어떤 것들이 있나요? {#subscriptions}

주소록은 [http://localhost:7657/dns](http://localhost:7657/dns)에 위치하며, 여기서 추가 정보를 확인할 수 있습니다.

**좋은 주소록 구독 링크에는 어떤 것들이 있나요?**

다음을 시도해 보세요:

- [http://stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
- [http://identiguy.i2p/hosts.txt](http://identiguy.i2p/hosts.txt)

### 다른 기기에서 웹 콘솔에 접근하거나 비밀번호로 보호하려면 어떻게 해야 하나요? {#remote_webconsole}

보안상의 이유로, router의 관리 콘솔은 기본적으로 로컬 인터페이스에서만 연결을 수신합니다.

콘솔에 원격으로 접근하는 두 가지 방법이 있습니다:

1. SSH Tunnel
2. 사용자 이름과 비밀번호를 사용하여 공용 IP 주소에서 콘솔을 사용할 수 있도록 구성하기

자세한 내용은 다음과 같습니다:

**방법 1: SSH 터널**

Unix 계열 운영체제를 사용하는 경우, I2P 콘솔에 원격으로 접속하는 가장 쉬운 방법입니다. (참고: SSH 서버 소프트웨어는 Windows를 실행하는 시스템에서도 사용할 수 있습니다. 예: [https://github.com/PowerShell/Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH))

시스템에 대한 SSH 접근을 설정한 후, 적절한 인수와 함께 '-L' 플래그를 SSH에 전달합니다 - 예를 들어:

```
ssh -L 7657:localhost:7657 (System_IP)
```
여기서 '(System_IP)'는 시스템의 IP 주소로 대체됩니다. 이 명령은 포트 7657(첫 번째 콜론 앞의 숫자)을 원격 시스템의(첫 번째와 두 번째 콜론 사이의 'localhost' 문자열로 지정됨) 포트 7657(두 번째 콜론 뒤의 숫자)로 전달합니다. 이제 원격 I2P 콘솔은 로컬 시스템에서 'http://localhost:7657'로 사용할 수 있으며, SSH 세션이 활성화되어 있는 동안 계속 사용할 수 있습니다.

원격 시스템에서 셸을 시작하지 않고 SSH 세션을 시작하려면 '-N' 플래그를 추가하면 됩니다:

```
ssh -NL 7657:localhost:7657 (System_IP)
```
**방법 2: 사용자 이름과 비밀번호를 사용하여 공인 IP 주소에서 콘솔을 사용할 수 있도록 구성하기**

1. `~/.i2p/clients.config`를 열고 다음을 교체하세요:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
   ```
   다음으로:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1,(System_IP) ./webapps/
   ```
   여기서 (System_IP)를 시스템의 공용 IP 주소로 교체하세요

2. [http://localhost:7657/configui](http://localhost:7657/configui)로 이동하여 원하는 경우 콘솔 사용자 이름과 비밀번호를 추가하세요 - 사용자 이름과 비밀번호를 추가하는 것은 I2P 콘솔을 변조로부터 보호하고 익명성 해제로 이어질 수 있는 상황을 방지하기 위해 강력히 권장됩니다.

3. [http://localhost:7657/index](http://localhost:7657/index)로 이동하여 "Graceful restart"를 클릭하면 JVM이 재시작되고 클라이언트 애플리케이션이 다시 로드됩니다

이 작업이 완료되면 이제 콘솔에 원격으로 접속할 수 있습니다. `http://(시스템_IP):7657`에서 router console을 열면 브라우저가 인증 팝업을 지원하는 경우 위 2단계에서 지정한 사용자 이름과 비밀번호를 입력하라는 메시지가 표시됩니다.

참고: 위 설정에서 0.0.0.0을 지정할 수 있습니다. 이것은 네트워크나 넷마스크가 아닌 인터페이스를 지정합니다. 0.0.0.0은 "모든 인터페이스에 바인딩"을 의미하므로 127.0.0.1:7657뿐만 아니라 모든 LAN/WAN IP에서도 접근할 수 있습니다. 이 옵션을 사용할 때는 주의하세요. 콘솔이 시스템에 구성된 모든 주소에서 접근 가능하게 됩니다.

### 다른 컴퓨터에서 애플리케이션을 어떻게 사용할 수 있나요? {#remote_i2cp}

SSH 포트 포워딩 사용 방법에 대한 지침은 이전 답변을 참조하시고, 콘솔의 다음 페이지도 확인하세요: [http://localhost:7657/configi2cp](http://localhost:7657/configi2cp)

### I2P를 SOCKS 프록시로 사용할 수 있나요? {#socks}

SOCKS 프록시는 0.7.1 릴리스부터 작동해 왔습니다. SOCKS 4/4a/5가 지원됩니다. I2P에는 SOCKS outproxy가 없으므로 I2P 내부에서만 사용할 수 있습니다.

많은 애플리케이션들은 인터넷에서 당신을 식별할 수 있는 민감한 정보를 유출하며, 이는 I2P SOCKS 프록시를 사용할 때 반드시 알아야 할 위험입니다. I2P는 연결 데이터만 필터링하지만, 실행하려는 프로그램이 이러한 정보를 콘텐츠로 전송하는 경우 I2P는 당신의 익명성을 보호할 방법이 없습니다. 예를 들어, 일부 메일 애플리케이션은 실행 중인 컴퓨터의 IP 주소를 메일 서버로 전송합니다. 토렌트용 [I2PSnark](http://localhost:7657/i2psnark/)와 같은 I2P 전용 도구나 애플리케이션, 또는 [Firefox](https://www.mozilla.org/)에서 찾을 수 있는 인기 플러그인을 포함하여 I2P와 함께 사용하기에 안전하다고 알려진 애플리케이션을 권장합니다.

### 일반 인터넷에서 IRC, BitTorrent 또는 기타 서비스에 어떻게 접근하나요? {#proxy_other}

I2P와 인터넷 사이를 연결하는 Outproxy라는 서비스가 있으며, 이는 Tor Exit Node와 유사합니다. HTTP와 HTTPS를 위한 기본 outproxy 기능은 `exit.stormycloud.i2p`에서 제공되며 StormyCloud Inc.에서 운영합니다. 이는 HTTP Proxy에서 설정됩니다. 또한 익명성 보호를 위해 I2P는 기본적으로 일반 인터넷에 익명 연결을 허용하지 않습니다. 자세한 내용은 [Socks Outproxy](/docs/api/socks#outproxy) 페이지를 참조하세요.

---

## Reseed

### 내 라우터가 몇 분 동안 실행되었지만 연결이 전혀 없거나 매우 적습니다 {#reseed}

먼저 라우터 콘솔의 네트워크 데이터베이스인 [http://127.0.0.1:7657/netdb](http://127.0.0.1:7657/netdb) 페이지를 확인하세요. I2P 내에서 단일 router도 표시되지 않지만 콘솔에서 방화벽이 있다고 표시되면, reseed 서버에 연결할 수 없는 것일 수 있습니다. 다른 I2P router들이 표시된다면 [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)에서 최대 연결 수를 낮춰보세요. 라우터가 많은 연결을 처리하지 못할 수 있습니다.

### 수동으로 재시드하는 방법은? {#manual_reseed}

일반적인 상황에서 I2P는 부트스트랩 링크를 사용하여 자동으로 네트워크에 연결합니다. 인터넷 연결 장애로 인해 reseed 서버로부터의 부트스트랩이 실패하는 경우, Tor 브라우저를 사용하는 것이 간편한 부트스트랩 방법입니다(기본적으로 localhost를 엽니다). 이는 [http://127.0.0.1:7657/configreseed](http://127.0.0.1:7657/configreseed)와 매우 잘 작동합니다. I2P router를 수동으로 reseed하는 것도 가능합니다.

Tor 브라우저를 사용하여 reseed할 때 여러 URL을 한 번에 선택하여 진행할 수 있습니다. 기본값인 2개(여러 URL 중)로도 작동하지만 느릴 수 있습니다.

---

## 개인정보 보호-안전

### 내 router가 일반 인터넷으로의 "exit node"(outproxy)인가요? 그렇게 되는 것을 원하지 않습니다. {#exit}

아니요, 당신의 router는 I2P 네트워크를 통해 종단간 암호화된 트래픽을 임의의 tunnel 엔드포인트로 전송하는 데 참여하며, 이는 일반적으로 outproxy가 아닙니다. 하지만 전송 계층에서 당신의 router와 인터넷 사이에 트래픽이 전달되지는 않습니다. 일반 사용자로서, 시스템 및 네트워크 관리에 능숙하지 않다면 outproxy를 운영해서는 안 됩니다.

### 네트워크 트래픽을 분석하여 I2P 사용을 탐지하는 것이 쉬운가요? {#detection}

I2P 트래픽은 일반적으로 UDP 트래픽처럼 보이며, 그 이상으로 보이지 않게 만드는 것이 목표입니다. 또한 TCP도 지원합니다. 어느 정도 노력을 기울이면 수동적 트래픽 분석을 통해 트래픽을 "I2P"로 분류할 수 있을 수 있지만, 트래픽 난독화의 지속적인 개발이 이를 더욱 줄일 수 있기를 기대합니다. obfs4와 같은 비교적 단순한 프로토콜 난독화 계층조차도 검열자가 I2P를 차단하는 것을 방지할 수 있습니다 (이는 I2P가 배포하고자 하는 목표입니다).

### I2P 사용이 안전한가요? {#safe}

이것은 개인의 위협 모델에 따라 다릅니다. 대부분의 사람들에게 I2P는 아무런 보호 장치를 사용하지 않는 것보다 훨씬 안전합니다. 일부 다른 네트워크(Tor, mixminion/mixmaster 등)는 특정 공격자에 대해 더 안전할 수 있습니다. 예를 들어, I2P 트래픽은 TLS/SSL을 사용하지 않으므로 Tor가 가진 "가장 약한 고리" 문제가 없습니다. I2P는 "아랍의 봄" 당시 시리아에서 많은 사람들이 사용했으며, 최근에는 중동 및 근동 지역의 소규모 언어권에서 I2P 설치가 더 크게 증가했습니다. 여기서 가장 중요한 점은 I2P는 기술이며, 인터넷에서 개인정보 보호/익명성을 강화하기 위한 사용 방법/가이드가 필요하다는 것입니다. 또한 브라우저를 확인하거나 핑거프린트 검색 엔진을 가져와서 매우 큰(의미: 전형적인 긴 꼬리/매우 정확한 다양한 데이터 구조) 환경 정보 데이터셋으로 핑거프린트 공격을 차단하고, VPN을 사용하지 않아 자체적으로 발생하는 모든 위험(자체 TLS 캐시 동작 및 데스크톱 시스템보다 쉽게 해킹될 수 있는 제공업체의 기술적 구조 등)을 줄이십시오. 격리된 Tor V-Browser를 우수한 안티 핑거프린트 보호 기능과 함께 사용하고, 필요한 시스템 통신만 허용하는 전반적인 앱가드 라이프타임 보호와 함께, 안티 스파이 비활성화 스크립트 및 라이브 CD를 사용하는 최종 단계 VM을 사용하여 "거의 영구적인 가능한 위험"을 제거하고 감소하는 확률로 모든 위험을 낮추는 것이 공용 네트워크와 최고 수준의 개인 위험 모델에서 좋은 옵션이 될 수 있으며, I2P 사용을 위해 이 목표로 할 수 있는 최선의 방법일 수 있습니다.

### 라우터 콘솔에서 다른 모든 I2P 노드의 IP 주소가 보입니다. 이것은 제 IP 주소도 다른 사람들에게 보인다는 뜻인가요? {#netdb_ip}

네, 당신의 router에 대해 알고 있는 다른 I2P 노드들에게는 그렇습니다. 우리는 이것을 나머지 I2P 네트워크와 연결하는 데 사용합니다. 이 주소들은 "routerInfo (키,값) 객체"에 물리적으로 위치하며, 원격으로 가져오거나 피어로부터 받습니다. "routerInfo"는 부트스트래핑을 위해 "피어가 게시한" router 자체에 대한 일부 정보(일부는 선택적으로 기회적으로 추가됨)를 보유합니다. 이 객체에는 클라이언트에 대한 데이터가 없습니다. 내부를 자세히 살펴보면 모든 사람이 "SHA-256 해시(낮음=양수 해시(-키), 높음=음수 해시(+키))"라는 최신 유형의 ID 생성 방식으로 계산되었음을 알 수 있습니다. I2P 네트워크는 업로드 및 인덱싱 중에 생성된 routerInfo의 자체 데이터베이스 데이터를 가지고 있지만, 이는 키/값 테이블과 네트워크 토폴로지, 부하 상태/대역폭 상태, 그리고 DB 컴포넌트의 저장소에 대한 라우팅 확률의 구현에 깊이 의존합니다.

### outproxy를 사용하는 것이 안전한가요? {#proxy_safe}

"안전"에 대한 정의가 무엇인지에 따라 다릅니다. Outproxy는 작동할 때는 훌륭하지만, 안타깝게도 자발적으로 운영하는 사람들이 흥미를 잃거나 24시간 365일 유지 관리할 수 있는 리소스가 없을 수 있습니다. 서비스를 사용할 수 없거나 중단되거나 신뢰할 수 없는 기간이 발생할 수 있으며, 우리는 이 서비스와 관련이 없고 이에 대한 영향력도 없다는 점을 유의하시기 바랍니다.

outproxy 자체는 엔드-투-엔드 암호화된 HTTPS/SSL 데이터를 제외하고 당신의 트래픽이 오가는 것을 볼 수 있습니다. 이는 마치 ISP가 당신의 컴퓨터에서 오가는 트래픽을 볼 수 있는 것과 같습니다. ISP를 신뢰한다면, outproxy도 그보다 나쁘지 않을 것입니다.

### "익명화 해제" 공격은 어떻습니까? {#deanon}

매우 자세한 설명은 [위협 모델](/docs/overview/threat-model)에 대한 문서를 참조하세요. 일반적으로 익명성 해제는 간단하지 않지만, 충분히 주의하지 않으면 가능합니다.

---

## 인터넷 접속/성능

### I2P를 통해 일반 인터넷 사이트에 접속할 수 없습니다. {#outproxy}

인터넷 사이트로의 프록시 접속(인터넷으로 나가는 eepsite)은 비차단 제공자들에 의해 I2P 사용자들에게 서비스로 제공됩니다. 이 서비스는 I2P 개발의 주요 초점이 아니며, 자발적으로 제공됩니다. I2P에 호스팅된 eepsite는 outproxy 없이도 항상 작동해야 합니다. Outproxy는 편의성을 제공하지만 설계상 완벽하지 않으며 프로젝트의 큰 부분도 아닙니다. Outproxy는 I2P의 다른 서비스들이 제공할 수 있는 고품질 서비스를 제공하지 못할 수 있다는 점을 유의하시기 바랍니다.

### I2P를 통해 https:// 또는 ftp:// 사이트에 접속할 수 없습니다. {#https}

기본 HTTP 프록시는 HTTP 및 HTTPS outproxy만 지원합니다.

### 왜 내 router가 너무 많은 CPU를 사용하나요? {#cpu}

먼저, 모든 I2P 관련 구성 요소가 최신 버전인지 확인하세요. 이전 버전에는 불필요하게 CPU를 소모하는 코드 섹션이 있었습니다. 시간이 지남에 따라 I2P 성능 개선 사항을 기록한 [성능 로그](/docs/overview/performance)도 있습니다.

### 내 활성 피어 / 알려진 피어 / 참여 중인 터널 / 연결 / 대역폭이 시간에 따라 급격하게 변동합니다! 문제가 있나요? {#vary}

I2P 네트워크의 전반적인 안정성은 지속적인 연구 분야입니다. 그 연구의 상당 부분은 구성 설정의 작은 변경이 router의 동작을 어떻게 바꾸는지에 초점을 맞추고 있습니다. I2P는 P2P(peer-to-peer) 네트워크이므로, 다른 peer들의 행동이 사용자 router의 성능에 영향을 미칩니다.

### 일반 인터넷과 비교했을 때 I2P에서 다운로드, 토렌트, 웹 브라우징 및 기타 모든 것이 느린 이유는 무엇인가요? {#slow}

I2P는 추가적인 라우팅과 암호화 계층을 더하는 다양한 보호 기능을 가지고 있습니다. 또한 각자의 속도와 품질을 가진 다른 피어(Tunnel)를 통해 트래픽을 전달하는데, 어떤 것은 느리고 어떤 것은 빠릅니다. 이로 인해 다양한 방향에서 서로 다른 속도로 많은 오버헤드와 트래픽이 발생합니다. 설계상 이러한 모든 요소들은 인터넷의 직접 연결에 비해 속도를 느리게 만들지만, 훨씬 더 익명성을 제공하며 대부분의 용도에는 여전히 충분히 빠릅니다.

다음은 I2P를 사용할 때 지연 시간과 대역폭 고려사항에 대한 맥락을 제공하기 위해 설명과 함께 제시된 예시입니다.

아래 다이어그램을 고려해 보세요. 이는 I2P를 통해 요청을 하는 클라이언트, I2P를 통해 요청을 받는 서버, 그리고 I2P를 통해 다시 응답하는 과정 간의 연결을 나타냅니다. 요청이 이동하는 회로도 함께 표시되어 있습니다.

다이어그램에서 'P', 'Q', 'R'로 표시된 박스들은 'A'의 아웃바운드 터널을 나타내고, 'X', 'Y', 'Z'로 표시된 박스들은 'B'의 아웃바운드 터널을 나타냅니다. 마찬가지로 'X', 'Y', 'Z'로 표시된 박스들은 'B'의 인바운드 터널을 나타내며, 'P_1', 'Q_1', 'R_1'로 표시된 박스들은 'A'의 인바운드 터널을 나타냅니다. 박스들 사이의 화살표는 트래픽의 방향을 보여줍니다. 화살표 위아래의 텍스트는 한 쌍의 홉 사이의 대역폭 예시와 지연시간 예시를 자세히 설명합니다.

클라이언트와 서버가 모두 3-hop tunnel을 사용하는 경우, 총 12개의 다른 I2P router가 트래픽 중계에 관여합니다. 6개의 피어가 클라이언트에서 서버로의 트래픽을 중계하며, 이는 'A'에서 시작하는 3-hop 아웃바운드 tunnel('P', 'Q', 'R')과 'B'로 향하는 3-hop 인바운드 tunnel('X', 'Y', 'Z')로 나뉩니다. 마찬가지로, 6개의 피어가 서버에서 클라이언트로 돌아가는 트래픽을 중계합니다.

먼저, 레이턴시(latency)를 고려할 수 있습니다 - 클라이언트의 요청이 I2P 네트워크를 통과하여 서버에 도달하고 다시 클라이언트로 돌아오는 데 걸리는 시간입니다. 모든 레이턴시를 합산하면 다음과 같습니다:

```
    40 + 100 + 20 + 60 + 80 + 10 + 30 ms        (client to server)
  + 60 + 40 + 80 + 60 + 100 + 20 + 40 ms        (server to client)
  -----------------------------------
  TOTAL:                          740 ms
```
우리 예제에서 총 왕복 시간은 740ms로 합산됩니다 - 일반적인 인터넷 웹사이트를 탐색할 때 보통 보는 것보다 확실히 훨씬 높습니다.

둘째, 사용 가능한 대역폭을 고려할 수 있습니다. 이는 클라이언트와 서버 간의 hop들 사이에서 가장 느린 링크와 서버가 클라이언트로 트래픽을 전송할 때를 통해 결정됩니다. 클라이언트에서 서버로 가는 트래픽의 경우, 예제에서 hop 'R'과 'X' 사이 및 hop 'X'와 'Y' 사이의 사용 가능한 대역폭이 32 KB/s임을 알 수 있습니다. 다른 hop들 사이에서 더 높은 대역폭을 사용할 수 있음에도 불구하고, 이러한 hop들은 병목 현상으로 작용하여 'A'에서 'B'로의 트래픽에 대한 최대 사용 가능 대역폭을 32 KB/s로 제한합니다. 마찬가지로, 서버에서 클라이언트로 가는 경로를 추적하면 hop 'Z_1'과 'Y_1' 사이, 'Y_1'과 'X_1' 사이, 그리고 'Q_1'과 'P_1' 사이에서 최대 대역폭이 64 KB/s임을 알 수 있습니다.

대역폭 제한을 늘리는 것을 권장합니다. 이는 사용 가능한 대역폭의 양을 증가시켜 네트워크에 도움이 되며, 결과적으로 I2P 사용 경험을 개선합니다. 대역폭 설정은 [http://localhost:7657/config](http://localhost:7657/config) 페이지에 있습니다. ISP가 정한 인터넷 연결 제한을 인지하고 그에 맞게 설정을 조정하시기 바랍니다.

또한 충분한 양의 공유 대역폭을 설정할 것을 권장합니다 - 이를 통해 participating tunnel들이 귀하의 I2P router를 통해 라우팅될 수 있습니다. participating 트래픽을 허용하면 귀하의 router가 네트워크에 잘 통합되고 전송 속도가 향상됩니다.

I2P는 계속 개발 중인 프로젝트입니다. 많은 개선 사항과 수정 사항이 구현되고 있으며, 일반적으로 최신 릴리스를 실행하면 성능이 향상됩니다. 아직 설치하지 않았다면 최신 릴리스를 설치하세요.

### 버그를 발견한 것 같은데, 어디에 보고할 수 있나요? {#bug}

버그나 문제를 발견하시면 일반 인터넷과 I2P 모두에서 접근 가능한 버그트래커에 보고해 주시기 바랍니다. 또한 I2P와 일반 인터넷에서 모두 이용할 수 있는 토론 포럼도 운영하고 있습니다. IRC 채널에도 참여하실 수 있습니다: IRC2P 네트워크나 Freenode를 통해 접속하실 수 있습니다.

- **버그트래커:**
  - 일반 인터넷: [https://i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)
  - I2P에서: [http://git.idk.i2p/I2P_Developers/i2p.i2p/issues](http://git.idk.i2p/I2P_Developers/i2p.i2p/issues)
- **포럼:** [i2pforum.i2p](http://i2pforum.i2p/)
- **로그 붙여넣기:** [PrivateBin 위키](https://github.com/PrivateBin/PrivateBin/wiki/PrivateBin-Directory)에 나열된 일반 인터넷 서비스나, [PrivateBin 인스턴스](http://paste.crypthost.i2p) 또는 [자바스크립트 없는 붙여넣기 서비스](http://pasta-nojs.i2p)와 같은 I2P 붙여넣기 서비스에 관심 있는 로그를 붙여넣고 IRC #i2p에서 후속 조치를 취하세요
- **IRC:** #i2p-dev에 참여하여 개발자들과 IRC에서 논의하세요

다음 주소에서 확인할 수 있는 router 로그 페이지의 관련 정보를 포함해 주세요: [http://127.0.0.1:7657/logs](http://127.0.0.1:7657/logs). 'I2P Version and Running Environment' 섹션 아래의 모든 텍스트와 페이지에 표시된 다양한 로그의 오류 또는 경고 메시지를 공유해 주시기 바랍니다.

---

### 질문이 있습니다! {#question}

좋습니다! IRC에서 저희를 찾아보세요:

- `irc.freenode.net` 채널 `#i2p`
- `IRC2P` 채널 `#i2p`

또는 [포럼](http://i2pforum.i2p/)에 게시하면 여기에 게시하겠습니다 (가능하면 답변과 함께).
