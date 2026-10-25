---
title: "I2PTunnel"
description: "I2P와 인터페이스하고 서비스를 제공하기 위한 도구"
slug: "i2ptunnel"
aliases:
  - "/ko/i2ptunnel"
  - "/ko/i2ptunnel/"
  - "/ko/i2ptunnel_migration"
  - "/ko/i2ptunnel_migration/"
  - "/ko/i2ptunnel_services"
  - "/ko/i2ptunnel_services/"
lastUpdated: "2023-10"
accurateFor: "0.9.59"
---

## 개요 {#overview}

I2PTunnel은 I2P에서 인터페이스하고 서비스를 제공하기 위한 도구입니다. I2PTunnel의 목적지는 [hostname](/docs/overview/naming), [Base32](/docs/overview/naming#base32), 또는 전체 516바이트 destination key를 사용하여 정의할 수 있습니다. 설정된 I2PTunnel은 클라이언트 머신에서 localhost:port로 사용할 수 있습니다. I2P 네트워크에서 서비스를 제공하려면, 적절한 ip_address:port로 I2PTunnel을 생성하기만 하면 됩니다. 해당 서비스를 위한 516바이트 destination key가 생성되고 I2P 전체에서 사용할 수 있게 됩니다. I2PTunnel 관리를 위한 웹 인터페이스는 [localhost:7657/i2ptunnel/](http://localhost:7657/i2ptunnel/)에서 사용할 수 있습니다.

## 기본 서비스 {#default-services}

### 서버 tunnel {#default-server-tunnels}

- **I2P Webserver** - I2P에서 편리하고 빠른 호스팅을 위해 [localhost:7658](http://localhost:7658)에서 실행되는 Jetty 웹서버를 가리키는 tunnel입니다.
  문서 루트는 다음과 같습니다:
  - **Unix** - `$HOME/.i2p/eepsite/docroot`
  - **Windows** - `%LOCALAPPDATA%\I2P\I2P Site\docroot`, 전체 경로: `C:\Users\**username**\AppData\Local\I2P\I2P Site\docroot`

### 클라이언트 터널 {#default-client-tunnels}

- **I2P HTTP Proxy** - *localhost:4444* - I2P와 일반 인터넷을 I2P를 통해 익명으로 브라우징하는 데 사용되는 HTTP 프록시입니다. I2P를 통한 인터넷 브라우징은 "Outproxies:" 옵션에서 지정된 임의의 프록시를 사용합니다.
- **Irc2P** - *localhost:6668* - 기본 익명 IRC 네트워크인 Irc2P로의 IRC tunnel입니다.
- **gitssh.idk.i2p** - *localhost:7670* - 프로젝트 Git 저장소에 대한 SSH 액세스
- **smtp.postman.i2p** - *localhost:7659* - hq.postman.i2p의 postman이 제공하는 SMTP 서비스
- **pop3.postman.i2p** - *localhost:7660* - hq.postman.i2p의 postman이 제공하는 동반 POP 서비스

## 설정 {#configuration}

[I2PTunnel 설정](/docs/specs/configuration)

## 클라이언트 모드 {#client-modes}

### 표준 {#client-modes-standard}

I2P 내부의 목적지에서 서비스(HTTP, FTP 또는 SMTP 등)에 연결하는 로컬 TCP 포트를 엽니다. tunnel은 쉼표로 구분된(", ") 목적지 목록에서 무작위 호스트로 연결됩니다.

### HTTP {#client-mode-http}

HTTP 클라이언트 tunnel입니다. 이 tunnel은 HTTP 요청의 URL에 지정된 목적지에 연결됩니다. outproxy가 제공되면 인터넷으로의 프록시를 지원합니다. HTTP 연결에서 다음 헤더들을 제거합니다:

- **Accept\*:** ("Accept"와 "Accept-Encoding"은 제외) 브라우저마다 크게 달라서 식별자로 사용될 수 있기 때문입니다.
- **Referer:**
- **Via:**
- **From:**

HTTP 클라이언트 프록시는 사용자를 보호하고 더 나은 사용자 경험을 제공하기 위해 여러 서비스를 제공합니다.

**요청 헤더 처리:** - 프라이버시 문제가 있는 헤더 제거 - 로컬 또는 원격 outproxy로 라우팅 - Outproxy 선택, 캐싱 및 접근성 추적 - 호스트명에서 목적지 조회 - 호스트 헤더를 b32로 교체 - 투명한 압축 해제 지원을 나타내는 헤더 추가 - 강제 연결 종료 - RFC 준수 프록시 지원 - RFC 준수 hop-by-hop 헤더 처리 및 제거 - 선택적 digest 및 기본 사용자명/비밀번호 인증 - 선택적 outproxy digest 및 기본 사용자명/비밀번호 인증 - 효율성을 위해 모든 헤더를 전달하기 전에 버퍼링 - Jump 서버 링크 - Jump 응답 처리 및 폼 (주소 도우미) - 블라인드 b32 처리 및 자격증명 폼 - 표준 HTTP 및 HTTPS (CONNECT) 요청 지원

**응답 헤더 처리:** - 응답 압축 해제 여부 확인 - 강제 연결: 닫기 - RFC 준수 hop-by-hop 헤더 처리 및 제거 - 효율성을 위한 모든 헤더 버퍼링 후 전달

**HTTP 오류 응답:** - 많은 일반적이고 일반적이지 않은 오류들에 대해 사용자가 무엇이 발생했는지 알 수 있도록 함 - 다양한 오류에 대한 20개 이상의 고유한 번역되고 스타일링되고 포맷된 오류 페이지 - 폼, CSS, 이미지, 오류를 제공하는 내부 웹 서버

#### 투명한 응답 압축 {#transparent-response-compression}

i2ptunnel 응답 압축은 다음 HTTP 헤더로 요청됩니다:

- **X-Accept-Encoding:** x-i2p-gzip;q=1.0, identity;q=0.5, deflate;q=0, gzip;q=0, *;q=0

서버 측은 웹 서버로 요청을 보내기 전에 이 hop-by-hop 헤더를 제거합니다. 모든 q 값이 포함된 복잡한 헤더는 필요하지 않으며, 서버는 헤더 내 어디에서든 "x-i2p-gzip"만 찾으면 됩니다.

서버 측은 웹서버로부터 받은 헤더들(Content-Type, Content-Length, Content-Encoding 포함)을 기반으로 응답을 압축할지 여부를 결정하며, 응답이 압축 가능하고 추가적인 CPU 사용량을 감수할 가치가 있는지를 평가합니다. 서버 측이 응답을 압축하면 다음과 같은 HTTP 헤더를 추가합니다:

- **Content-Encoding:** x-i2p-gzip

이 헤더가 응답에 있으면, HTTP 클라이언트 프록시가 투명하게 압축을 해제합니다. 클라이언트 측에서는 이 헤더를 제거하고 브라우저에 응답을 보내기 전에 gunzip을 실행합니다. HTTP 계층에서 응답이 압축되지 않은 경우에도 I2CP 계층의 기본 gzip 압축이 여전히 효과적이라는 점에 주목하세요.

이 설계와 현재 구현은 여러 가지 방식으로 RFC 2616을 위반합니다:

- X-Accept-Encoding은 표준 헤더가 아닙니다
- 홉별로 dechunk/chunk를 수행하지 않으며, 청킹을 종단 간 통과시킵니다
- Transfer-Encoding 헤더를 종단 간 통과시킵니다
- 홉별 인코딩을 지정하기 위해 Transfer-Encoding이 아닌 Content-Encoding을 사용합니다
- Content-Encoding이 설정되었을 때 x-i2p gzip 압축을 금지합니다 (하지만 어차피 하고 싶지 않을 것입니다)
- 서버 측에서는 dechunk-gzip-rechunk와 dechunk-gunzip-rechunk를 수행하는 대신 서버가 전송하는 청킹을 gzip 압축합니다
- gzip 압축된 콘텐츠는 이후에 청킹되지 않습니다. RFC 2616은 "identity" 이외의 모든 Transfer-Encoding이 청킹되어야 한다고 요구합니다.
- gzip 외부(이후)에 청킹이 없기 때문에 데이터의 끝을 찾기가 더 어려워져서 keepalive 구현이 더 어려워집니다.
- RFC 2616은 Transfer-Encoding이 있을 때 Content-Length를 전송하지 말아야 한다고 하지만 우리는 전송합니다. 사양에서는 Transfer-Encoding이 있으면 Content-Length를 무시하라고 하는데, 브라우저들이 그렇게 하므로 우리에게는 작동합니다.

표준을 준수하는 hop-by-hop 압축을 이전 버전과 호환되는 방식으로 구현하기 위한 변경 사항은 추가 연구 주제입니다. dechunk-gzip-rechunk에 대한 모든 변경 사항은 새로운 인코딩 타입(예: x-i2p-gzchunked)을 필요로 할 것입니다. 이는 Transfer-Encoding: gzip과 동일하지만 호환성상의 이유로 다르게 신호를 보내야 할 것입니다. 모든 변경 사항은 공식적인 제안서가 필요합니다.

#### 투명한 요청 압축 {#transparent-request-compression}

지원되지 않지만, POST는 이점을 얻을 수 있습니다. I2CP 계층에서 기본 gzip 압축은 여전히 사용하고 있다는 점을 참고하세요.

#### 지속성 {#persistence}

클라이언트와 서버 프록시는 현재 세 개의 홉(브라우저 소켓, I2P 소켓, 서버 소켓) 중 어느 곳에서도 RFC 2616 HTTP 지속적 소켓을 지원하지 않습니다. Connection: close 헤더가 모든 홉에 주입됩니다. 지속성을 구현하기 위한 변경 사항이 검토 중입니다. 이러한 변경 사항은 표준을 준수하고 하위 호환성을 유지해야 하며, 공식적인 제안서를 필요로 하지 않을 것입니다.

#### 파이프라이닝 {#pipelining}

클라이언트 및 서버 프록시는 현재 RFC 2616 HTTP 파이프라이닝을 지원하지 않으며 이를 지원할 계획도 없습니다. 최신 브라우저는 대부분의 프록시가 파이프라이닝을 올바르게 구현할 수 없기 때문에 프록시를 통한 파이프라이닝을 지원하지 않습니다.

#### 호환성 {#compatibility}

프록시 구현체들은 상대편의 다른 구현체들과 올바르게 작동해야 합니다. 클라이언트 프록시는 서버 측에 HTTP 인식 서버 프록시가 없어도 (즉, 표준 tunnel) 작동해야 합니다. 모든 구현체가 x-i2p-gzip을 지원하는 것은 아닙니다.

#### User Agent {#user-agent}

tunnel이 outproxy를 사용하는지 여부에 따라 다음 User-Agent가 추가됩니다:

- *Outproxy:* **User-Agent:** Windows의 최신 Firefox 릴리스에서 사용자 에이전트를 사용
- *Internal I2P use:* **User-Agent:** MYOB/6.66 (AN/ON)

### IRC 클라이언트 {#client-mode-irc}

쉼표로 구분된(", ") 목적지 목록에서 지정된 임의의 IRC 서버에 연결을 생성합니다. 익명성 문제로 인해 허용 목록에 있는 IRC 명령의 하위 집합만 허용됩니다.

다음 허용 목록은 IRC 서버에서 IRC 클라이언트로 들어오는 명령어에 대한 것입니다.

**허용 목록:** - AUTHENTICATE - CAP - ERROR - H - JOIN - KICK - MODE - NICK - PART - PING - PROTOCTL - QUIT - TOPIC - WALLOPS

IRC 클라이언트에서 IRC 서버로 나가는 명령어에 대한 허용 목록도 있습니다. IRC 관리 명령어의 수가 많아서 꽤 큽니다. 자세한 내용은 IRCFilter.java 소스를 참조하세요.

아웃바운드 필터는 또한 식별 정보를 제거하기 위해 다음 명령어들을 수정합니다: - NOTICE - PART - PING - PRIVMSG - QUIT - USER

### SOCKS 4/4a/5 {#client-mode-socks}

I2P router를 SOCKS 프록시로 사용할 수 있게 합니다.

### SOCKS IRC {#client-mode-socks-irc}

[IRC](#client-mode-irc) 클라이언트 모드에서 지정된 명령 화이트리스트와 함께 I2P router를 SOCKS 프록시로 사용할 수 있게 합니다.

### CONNECT {#client-mode-connect}

HTTP tunnel을 생성하고 HTTP 요청 메서드 "CONNECT"를 사용하여 일반적으로 SSL과 HTTPS에 사용되는 TCP tunnel을 구축합니다.

### Streamr {#client-mode-streamr}

Streamr 클라이언트 I2PTunnel에 연결된 UDP 서버를 생성합니다. streamr 클라이언트 tunnel은 streamr 서버 tunnel을 구독합니다.

![Streamr diagram](/images/I2PTunnel-streamr.png)

## 서버 모드 {#server-modes}

### 표준 {#server-mode-standard}

로컬 ip:port에 대한 destination을 생성하며 TCP 포트가 열려 있습니다.

### HTTP {#server-mode-http}

로컬 HTTP 서버 ip:port로의 destination을 생성합니다. Accept-encoding: x-i2p-gzip 요청에 대해 gzip을 지원하며, 이러한 요청에 대해 Content-encoding: x-i2p-gzip로 응답합니다.

HTTP 서버 프록시는 웹사이트 호스팅을 더 쉽고 안전하게 만들고, 클라이언트 측에서 더 나은 사용자 경험을 제공하기 위한 여러 서비스를 제공합니다.

**요청 헤더 처리:** - 헤더 유효성 검사 - 헤더 스푸핑 보호 - 헤더 크기 확인 - 선택적 inproxy 및 user-agent 거부 - 웹서버가 요청 출처를 알 수 있도록 X-I2P 헤더 추가 - 웹서버 vhost를 더 쉽게 만들기 위한 Host 헤더 교체 - connection: close 강제 적용 - RFC 준수 hop-by-hop 헤더 처리 및 제거 - 효율성을 위해 전달하기 전 모든 헤더 버퍼링

**DDoS 보호:** - POST 스로틀링 - 타임아웃 및 slowloris 보호 - 모든 tunnel 유형에 대해 스트리밍에서 추가 스로틀링 발생

**응답 헤더 처리:** - 일부 프라이버시 문제가 있는 헤더 제거 - 응답 압축 여부를 위한 MIME 타입 및 기타 헤더 확인 - 강제 연결 종료 - RFC 준수 hop-by-hop 헤더 처리 및 제거 - 효율성을 위해 전달하기 전 모든 헤더 버퍼링

**HTTP 오류 응답:** - 많은 일반적이고 일반적이지 않은 오류와 throttling에 대해 클라이언트 측 사용자가 무엇이 발생했는지 알 수 있도록 함

**투명한 응답 압축:** - 웹 서버 및/또는 I2CP 계층에서 압축할 수 있지만, 웹 서버는 종종 압축하지 않으며, I2CP에서도 압축하더라도 상위 계층에서 압축하는 것이 가장 효율적입니다. HTTP 서버 프록시는 클라이언트 측 프록시와 협력하여 응답을 투명하게 압축합니다.

### HTTP 양방향 {#server-mode-http-bidir}

*사용 중단됨*

I2PTunnel HTTP Server와 I2PTunnel HTTP 클라이언트 역할을 모두 수행하지만 outproxy 기능은 없습니다. 예시 애플리케이션으로는 클라이언트 타입 요청을 수행하는 웹 애플리케이션이나 진단 도구로 I2P 사이트를 루프백 테스트하는 경우가 있습니다.

### IRC 서버 {#server-mode-irc}

클라이언트의 등록 시퀀스를 필터링하고 클라이언트의 destination 키를 호스트명으로 IRC 서버에 전달하는 destination을 생성합니다.

### Streamr {#server-mode-streamr}

미디어 서버에 연결하는 UDP 클라이언트가 생성됩니다. UDP 클라이언트는 Streamr 서버 I2PTunnel과 결합됩니다.
