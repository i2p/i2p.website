---
title: "애플리케이션 개발"
description: "I2P 전용 앱을 작성하는 이유, 핵심 개념, 개발 옵션 및 간단한 시작 가이드"
slug: "applications"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## 왜 I2P 전용 코드를 작성해야 하나요?

I2P에서 애플리케이션을 사용하는 방법은 여러 가지가 있습니다. [I2PTunnel](/docs/api/i2ptunnel/)을 사용하면 명시적인 I2P 지원을 프로그래밍할 필요 없이 일반 애플리케이션을 사용할 수 있습니다. 이는 단일 웹사이트에 연결해야 하는 클라이언트-서버 시나리오에서 매우 효과적입니다. 그림 1에 표시된 것처럼 I2PTunnel을 사용하여 해당 웹사이트에 연결하는 터널을 간단히 생성할 수 있습니다.

애플리케이션이 분산되어 있다면 많은 수의 peer들과의 연결이 필요합니다. I2PTunnel을 사용할 경우, 그림 2에 표시된 것처럼 연결하려는 각 peer마다 새로운 tunnel을 생성해야 합니다. 이 과정은 물론 자동화할 수 있지만, 많은 I2PTunnel 인스턴스를 실행하면 상당한 오버헤드가 발생합니다. 또한 많은 프로토콜에서는 모든 peer가 동일한 포트 집합을 사용하도록 강제해야 합니다. 예를 들어 DCC 채팅을 안정적으로 실행하려면 포트 10001은 Alice, 포트 10002는 Bob, 포트 10003은 Charlie 등으로 모두가 합의해야 합니다. 이는 프로토콜에 TCP/IP 특정 정보(호스트 및 포트)가 포함되어 있기 때문입니다.

일반적인 네트워크 애플리케이션은 사용자를 식별하는 데 사용될 수 있는 많은 추가 데이터를 전송합니다. 호스트명, 포트 번호, 시간대, 문자 집합 등이 사용자에게 알리지 않고 전송되는 경우가 많습니다. 따라서 익명성을 염두에 두고 네트워크 프로토콜을 특별히 설계하면 사용자 신원이 노출되는 것을 방지할 수 있습니다.

I2P 상에서 상호작용하는 방법을 결정할 때 검토해야 할 효율성 고려사항도 있습니다. streaming 라이브러리와 그 위에 구축된 것들은 TCP와 유사한 핸드셰이크로 작동하는 반면, 핵심 I2P 프로토콜(I2NP와 I2CP)은 엄격히 메시지 기반입니다(UDP 또는 경우에 따라 raw IP와 같이). 중요한 차이점은 I2P에서는 통신이 long fat network를 통해 작동한다는 것입니다 — 각 엔드 투 엔드 메시지는 무시할 수 없는 지연시간을 가지지만, 최대 수 KB의 페이로드를 포함할 수 있습니다. 단순한 요청과 응답이 필요한 애플리케이션은 MTU 감지나 메시지 단편화를 걱정할 필요 없이 (최선 노력) 데이터그램을 사용하여 시작 및 종료 핸드셰이크에서 발생하는 지연시간을 제거하고 모든 상태를 버릴 수 있습니다.

<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_serverclient.png" alt="Creating a server-client connection using I2PTunnel only requires creating a single tunnel." />
  <figcaption>Figure 1: Creating a server-client connection using I2PTunnel only requires creating a single tunnel.</figcaption>
</figure>
<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_peertopeer.png" alt="Setting up connections for a peer-to-peer applications requires a very large amount of tunnels." />
  <figcaption>Figure 2: Setting up connections for a peer-to-peer applications requires a very large amount of tunnels.</figcaption>
</figure>
요약하자면, I2P 전용 코드를 작성해야 하는 여러 가지 이유:

- 많은 수의 I2PTunnel 인스턴스를 생성하면 상당한 양의 리소스가 소모되며, 이는 분산 애플리케이션에 문제가 됩니다 (각 피어마다 새로운 tunnel이 필요함).
- 일반적인 네트워크 프로토콜은 사용자를 식별하는 데 사용될 수 있는 많은 추가 데이터를 전송하는 경우가 많습니다. I2P를 위해 특별히 프로그래밍하면 이러한 정보를 유출하지 않는 네트워크 프로토콜을 만들 수 있어 사용자를 익명으로 안전하게 보호할 수 있습니다.
- 일반 인터넷에서 사용하도록 설계된 네트워크 프로토콜은 훨씬 높은 지연 시간을 가진 네트워크인 I2P에서는 비효율적일 수 있습니다.

I2P는 개발자를 위한 표준 [플러그인 인터페이스](/docs/plugins/)를 지원하여 애플리케이션을 쉽게 통합하고 배포할 수 있습니다.

Java로 작성되고 표준 webapps/app.war를 통해 HTML 인터페이스를 사용하여 접근/실행 가능한 애플리케이션은 I2P 배포판에 포함되는 것을 고려할 수 있습니다.

## 중요한 개념

I2P를 사용할 때 적응해야 하는 몇 가지 변경 사항이 있습니다:

### 목적지

I2P에서 실행되는 애플리케이션은 고유한 암호학적으로 안전한 엔드포인트인 "destination"으로부터 메시지를 송수신합니다. TCP 또는 UDP 관점에서 destination은 (대체로) 호스트명과 포트 번호 쌍과 동등한 것으로 간주될 수 있지만, 몇 가지 차이점이 있습니다.

- I2P destination 자체는 암호학적 구조입니다 — 이곳으로 전송되는 모든 데이터는 IPsec이 보편적으로 배포된 것처럼 암호화되며, 엔드포인트의 (익명화된) 위치는 DNSSEC이 보편적으로 배포된 것처럼 서명됩니다.
- I2P destination은 이동 가능한 식별자입니다 — 하나의 I2P router에서 다른 router로 이동할 수 있으며 (또는 "멀티홈" 방식으로 여러 router에서 동시에 작동할 수도 있습니다). 이는 단일 엔드포인트(포트)가 단일 호스트에 고정되어야 하는 TCP 또는 UDP 환경과는 상당히 다릅니다.
- I2P destination은 보기 어렵고 크기가 큽니다 — 내부적으로 암호화를 위한 2048비트 ElGamal 공개 키, 서명을 위한 1024비트 DSA 공개 키, 그리고 작업 증명이나 블라인드 데이터를 포함할 수 있는 가변 크기의 인증서를 포함합니다.

이러한 크고 복잡한 destination을 짧고 예쁜 이름(예: "irc.duck.i2p")으로 참조하는 기존 방법들이 있지만, 이러한 기술들은 전역적 고유성을 보장하지 않으며(각 사용자의 컴퓨터에 로컬 데이터베이스로 저장되므로) 현재 메커니즘은 특별히 확장 가능하거나 안전하지 않습니다(호스트 목록 업데이트는 네이밍 서비스에 대한 "구독"을 사용하여 관리됩니다). 언젠가는 안전하고, 사람이 읽을 수 있으며, 확장 가능하고, 전역적으로 고유한 네이밍 시스템이 있을 수 있지만, 애플리케이션은 그것이 구현되어 있다는 것에 의존해서는 안 됩니다. [네이밍 시스템에 대한 추가 정보](/docs/overview/naming/)를 확인할 수 있습니다.

대부분의 애플리케이션은 프로토콜과 포트를 구분할 필요가 없지만, I2P는 이를 지원*합니다*. 복잡한 애플리케이션은 단일 destination에서 트래픽을 다중화하기 위해 메시지별로 프로토콜, 출발 포트, 도착 포트를 지정할 수 있습니다. 자세한 내용은 [datagram 페이지](/docs/api/datagrams/)를 참조하세요. 간단한 애플리케이션은 destination의 "모든 포트"에서 "모든 프로토콜"을 수신하는 방식으로 작동합니다.

### 익명성과 기밀성

I2P는 네트워크를 통해 전달되는 모든 데이터에 대해 투명한 종단 간 암호화 및 인증을 제공합니다. Bob이 Alice의 destination으로 데이터를 보내면 Alice의 destination만 이를 수신할 수 있으며, Bob이 데이터그램 또는 스트리밍 라이브러리를 사용하는 경우 Alice는 해당 데이터를 보낸 것이 Bob의 destination임을 확실하게 알 수 있습니다.

물론 I2P는 Alice와 Bob 사이에 전송되는 데이터를 투명하게 익명화하지만, 그들이 보내는 콘텐츠 자체를 익명화하지는 않습니다. 예를 들어, Alice가 Bob에게 자신의 전체 이름, 정부 발급 신분증, 신용카드 번호가 포함된 양식을 보낸다면, I2P가 할 수 있는 일은 없습니다. 따라서 프로토콜과 애플리케이션은 어떤 정보를 보호하려고 하는지, 그리고 어떤 정보를 노출할 의향이 있는지를 염두에 두어야 합니다.

### I2P 데이터그램은 최대 수 KB까지 가능합니다

I2P 데이터그램(raw 또는 repliable)을 사용하는 애플리케이션은 본질적으로 UDP 관점에서 생각할 수 있습니다 — 데이터그램은 순서가 없고, 최선 노력(best effort) 방식이며, 비연결형입니다 — 그러나 UDP와 달리 애플리케이션은 MTU 감지에 대해 걱정할 필요가 없으며 단순히 대용량 데이터그램을 전송할 수 있습니다. 명목상 상한선은 32 KB이지만, 메시지는 전송을 위해 단편화되므로 전체의 신뢰성이 떨어집니다. 현재 약 10 KB 이상의 데이터그램은 권장되지 않습니다. 자세한 내용은 [데이터그램 페이지](/docs/api/datagrams/)를 참조하세요. 많은 애플리케이션의 경우 10 KB의 데이터는 전체 요청 또는 응답에 충분하므로, 단편화, 재전송 등을 작성할 필요 없이 UDP와 유사한 애플리케이션으로 I2P에서 투명하게 작동할 수 있습니다.

## 개발 옵션

I2P를 통해 데이터를 전송하는 방법에는 여러 가지가 있으며, 각각 장단점이 있습니다. streaming lib는 대부분의 I2P 애플리케이션에서 사용되는 권장 인터페이스입니다.

### 스트리밍 라이브러리

[전체 streaming 라이브러리](/docs/specs/streaming/)가 이제 표준 인터페이스입니다. [Streaming 개발 가이드](#developing-with-the-streaming-library)에서 설명한 대로 TCP와 유사한 소켓을 사용한 프로그래밍이 가능합니다.

### BOB

BOB는 [Basic Open Bridge](/docs/legacy/bob/)로, 모든 언어로 작성된 애플리케이션이 I2P와 스트리밍 연결을 주고받을 수 있게 해줍니다. 현재 시점에서는 UDP 지원이 부족하지만, 가까운 미래에 UDP 지원이 계획되어 있습니다. BOB는 또한 destination 키 생성, 주소가 I2P 사양을 준수하는지 검증하는 등 여러 도구를 포함하고 있습니다. 최신 정보와 BOB를 사용하는 애플리케이션은 이 [I2P 사이트](http://bob.i2p/)에서 찾을 수 있습니다.

### SAM, SAM V2, SAM V3

*SAM은 권장되지 않습니다. SAM V2는 괜찮으며, SAM V3가 권장됩니다.*

SAM은 [Simple Anonymous Messaging](/docs/legacy/sam/) 프로토콜로, 어떤 언어로 작성된 애플리케이션이든 일반 TCP 소켓을 통해 SAM 브리지와 통신할 수 있게 하며, 해당 브리지가 모든 I2P 트래픽을 다중화하고 암호화/복호화 및 이벤트 기반 처리를 투명하게 조정합니다. SAM은 세 가지 작동 방식을 지원합니다:

- 스트림: Alice와 Bob이 서로에게 데이터를 안정적이고 순서대로 전송하고자 할 때 사용
- 응답 가능한 데이터그램: Alice가 Bob에게 Bob이 응답할 수 있는 메시지를 보내고자 할 때 사용
- 원시 데이터그램: Alice가 최대한의 대역폭과 성능을 확보하고자 하며, Bob이 데이터 발신자의 인증 여부를 신경 쓰지 않을 때 사용 (예: 전송되는 데이터가 자체 인증됨)

SAM V3는 SAM 및 SAM V2와 동일한 목표를 지향하지만, 멀티플렉싱/디멀티플렉싱을 필요로 하지 않습니다. 각 I2P stream은 애플리케이션과 SAM bridge 사이의 고유한 소켓으로 처리됩니다. 또한, 애플리케이션은 SAM bridge와의 데이터그램 통신을 통해 데이터그램을 송수신할 수 있습니다.

[SAM V2](/docs/legacy/samv2/)는 imule에서 사용되는 새 버전으로, [SAM](/docs/legacy/sam/)의 일부 문제점을 수정합니다.

[SAM V3](/docs/api/samv3/)는 버전 1.4.0부터 imule에서 사용됩니다.

### I2PTunnel

I2PTunnel 애플리케이션은 I2PTunnel '클라이언트' 애플리케이션(특정 포트를 리스닝하고 해당 포트에 소켓이 열릴 때마다 특정 I2P destination에 연결)이나 I2PTunnel '서버' 애플리케이션(특정 I2P destination을 리스닝하고 새로운 I2P 연결을 받을 때마다 특정 TCP 호스트/포트로 아웃프록시)을 생성하여 애플리케이션이 피어에 대한 특정 TCP-like tunnel을 구축할 수 있게 합니다. 이러한 스트림은 8비트 클린이며, SAM이 사용하는 것과 동일한 스트리밍 라이브러리를 통해 인증되고 보안됩니다. 하지만 여러 개의 고유한 I2PTunnel 인스턴스를 생성하는 데는 상당한 오버헤드가 수반되는데, 각각이 고유한 I2P destination과 자체 tunnel 세트, 키 등을 가지기 때문입니다.

### SOCKS

I2P는 SOCKS V4 및 V5 프록시를 지원합니다. 아웃바운드 연결은 잘 작동합니다. 인바운드(서버) 및 UDP 기능은 불완전하고 테스트되지 않았을 수 있습니다.

### Ministreaming

*제거됨*

예전에는 간단한 "ministreaming" 라이브러리가 있었지만, 현재 ministreaming.jar에는 전체 streaming 라이브러리의 인터페이스만 포함되어 있습니다.

### 데이터그램

*UDP와 유사한 애플리케이션에 권장됨*

[Datagram 라이브러리](/docs/api/datagrams/)를 사용하면 UDP와 유사한 패킷을 전송할 수 있습니다. 다음을 사용할 수 있습니다:

- 응답 가능한 데이터그램
- 원시 데이터그램

### I2CP

*권장하지 않음*

[I2CP](/docs/specs/i2cp/) 자체는 언어 독립적인 프로토콜이지만, Java가 아닌 다른 언어로 I2CP 라이브러리를 구현하려면 상당한 양의 코드를 작성해야 합니다(암호화 루틴, 객체 마샬링, 비동기 메시지 처리 등). 누군가 C나 다른 언어로 I2CP 라이브러리를 작성할 수도 있지만, 대신 C SAM 라이브러리를 사용하는 것이 더 유용할 것입니다.

### 웹 애플리케이션

I2P는 Jetty 웹서버와 함께 제공되며, Apache 서버를 대신 사용하도록 구성하는 것은 간단합니다. 모든 표준 웹 앱 기술이 작동해야 합니다.

## 개발 시작하기 — 간단한 가이드

I2P를 사용한 개발에는 작동하는 I2P 설치와 선택한 개발 환경이 필요합니다. Java를 사용하는 경우 [streaming library](#developing-with-the-streaming-library) 또는 datagram library로 개발을 시작할 수 있습니다. 다른 프로그래밍 언어를 사용하는 경우 SAM 또는 BOB을 사용할 수 있습니다.

### Streaming Library를 사용한 개발

아래는 원본 페이지의 예제를 축약하고 현대화한 버전입니다. 전체 예제는 레거시 페이지 또는 코드베이스의 Java 예제를 참조하세요.

```java
// Server example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
I2PServerSocket server = manager.getServerSocket();
I2PSocket socket = server.accept();
BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
String s;
while ((s = br.readLine()) != null) {
    System.out.println("Received: " + s);
}
```
*코드 예제: 데이터를 수신하는 기본 서버.*

```java
// Client example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
Destination dest = new Destination(serverDestBase64);
I2PSocket socket = manager.connect(dest);
BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
bw.write("Hello I2P!\n");
bw.flush();
```
*코드 예제: 클라이언트 연결 및 한 줄 전송.*
