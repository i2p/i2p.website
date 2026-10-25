---
title: "애플리케이션 개발"
description: "I2P 전용 앱을 작성하는 이유, 핵심 개념, 개발 옵션, 그리고 시작 가이드"
slug: "applications"
aliases:
  - "/ko/docs/develop/applications"
  - "/ko/docs/develop/applications/"
  - "/ko/applications"
  - "/ko/applications/"
lastUpdated: "2013-05"
accurateFor: "0.9.6"
---

## 왜 I2P 전용 코드를 작성해야 하는가?

I2P에서 애플리케이션을 사용하는 방법은 여러 가지가 있습니다. [I2PTunnel](/docs/api/i2ptunnel/)을 사용하면 명시적인 I2P 지원을 프로그래밍할 필요 없이 일반적인 애플리케이션을 사용할 수 있습니다. 이는 단일 웹사이트에 연결해야 하는 클라이언트-서버 시나리오에서 매우 효과적입니다. 그림 1에 표시된 것처럼 해당 웹사이트에 연결하기 위해 I2PTunnel을 사용하여 tunnel을 간단히 만들 수 있습니다.

애플리케이션이 분산되어 있다면, 많은 수의 피어에 대한 연결이 필요할 것입니다. I2PTunnel을 사용하면 연결하려는 각 피어마다 새로운 tunnel을 생성해야 하며, 이는 그림 2에서 보여주는 바와 같습니다. 물론 이 과정은 자동화할 수 있지만, 많은 I2PTunnel 인스턴스를 실행하는 것은 상당한 오버헤드를 발생시킵니다. 또한, 많은 프로토콜에서는 모든 피어가 동일한 포트 세트를 사용하도록 강제해야 합니다. 예를 들어, DCC 채팅을 안정적으로 실행하려면 프로토콜이 TCP/IP 특정 정보(호스트와 포트)를 포함하기 때문에, 모든 사용자가 포트 10001은 Alice, 포트 10002는 Bob, 포트 10003은 Charlie라는 식으로 합의해야 합니다.

일반적인 네트워크 애플리케이션은 사용자를 식별하는 데 사용될 수 있는 많은 추가 데이터를 전송하는 경우가 많습니다. 호스트명, 포트 번호, 시간대, 문자 집합 등이 사용자에게 알리지 않고 전송되는 경우가 많습니다. 따라서 익명성을 염두에 두고 네트워크 프로토콜을 특별히 설계하면 사용자 신원이 노출되는 것을 방지할 수 있습니다.

I2P 위에서 상호작용하는 방법을 결정할 때 검토해야 할 효율성 고려사항들도 있습니다. streaming library와 그 위에 구축된 것들은 TCP와 유사한 handshake로 작동하는 반면, 핵심 I2P 프로토콜들(I2NP와 I2CP)은 엄격히 메시지 기반입니다(UDP나 경우에 따라서는 raw IP처럼). 중요한 구별점은 I2P에서 통신은 long fat network 위에서 작동한다는 것입니다 — 각 end-to-end 메시지는 상당한 지연시간을 가지지만, 최대 수 KB의 페이로드를 포함할 수 있습니다. 단순한 요청과 응답이 필요한 애플리케이션은 MTU 탐지나 메시지 조각화에 대해 걱정할 필요 없이 (best effort) datagram을 사용하여 모든 상태를 제거하고 시작 및 종료 handshake로 인한 지연시간을 줄일 수 있습니다.

![I2PTunnel만 사용하여 서버-클라이언트 연결을 생성하려면 단일 터널만 생성하면 됩니다.](/images/i2ptunnel_serverclient.png)

*그림 1: I2PTunnel을 사용하여 서버-클라이언트 연결을 생성하는 것은 단일 tunnel 생성만 필요합니다.*

![피어 투 피어 애플리케이션의 연결 설정에는 매우 많은 수의 tunnel이 필요합니다.](/images/i2ptunnel_peertopeer.png)

*그림 2: 피어투피어 애플리케이션을 위한 연결 설정에는 매우 많은 수의 tunnel이 필요합니다.*

요약하면, I2P 전용 코드를 작성해야 하는 여러 가지 이유들:

- 대량의 I2PTunnel 인스턴스를 생성하면 상당한 양의 리소스를 소모하며, 이는 분산 애플리케이션에서 문제가 됩니다(각 피어마다 새로운 tunnel이 필요함).
- 일반적인 네트워크 프로토콜은 사용자를 식별하는 데 사용될 수 있는 많은 추가 데이터를 전송하는 경우가 많습니다. I2P를 위해 특별히 프로그래밍하면 그러한 정보를 유출하지 않는 네트워크 프로토콜을 만들 수 있어 사용자의 익명성과 보안을 유지할 수 있습니다.
- 일반 인터넷에서 사용하도록 설계된 네트워크 프로토콜은 훨씬 높은 지연 시간을 가진 네트워크인 I2P에서는 비효율적일 수 있습니다.

I2P는 개발자를 위한 표준 [플러그인 인터페이스](/docs/specs/plugin/)를 지원하여 애플리케이션을 쉽게 통합하고 배포할 수 있도록 합니다.

Java로 작성되고 표준 webapps/app.war를 통해 HTML 인터페이스를 사용하여 접근/실행 가능한 애플리케이션은 I2P 배포판에 포함될 수 있습니다.

---

## 중요한 개념

I2P를 사용할 때 적응해야 할 몇 가지 변화가 있습니다:

### Destination ~= host+port

I2P에서 실행되는 애플리케이션은 고유한 암호학적으로 안전한 엔드포인트인 "destination"으로부터 메시지를 보내고 받습니다. TCP나 UDP 측면에서 보면, destination은 (대체로) 호스트명과 포트 번호 쌍과 동등하다고 볼 수 있지만, 몇 가지 차이점이 있습니다.

- I2P destination 자체는 암호학적 구조체입니다 — 여기로 전송되는 모든 데이터는 IPsec이 범용적으로 배포된 것처럼 암호화되고, 끝점의 (익명화된) 위치는 DNSSEC이 범용적으로 배포된 것처럼 서명됩니다.
- I2P destination은 이동 가능한 식별자입니다 — 한 I2P router에서 다른 router로 이동할 수 있고(또는 "멀티홈" — 여러 router에서 동시에 작동할 수도 있습니다). 이는 단일 끝점(포트)이 단일 호스트에 머물러야 하는 TCP나 UDP 환경과는 매우 다릅니다.
- I2P destination은 복잡하고 큽니다 — 배후에서는 암호화를 위한 2048비트 ElGamal 공개키, 서명을 위한 1024비트 DSA 공개키, 그리고 작업 증명 또는 블라인딩된 데이터를 포함할 수 있는 가변 크기의 인증서를 포함합니다.

이러한 크고 복잡한 destination을 짧고 예쁜 이름(예: "irc.duck.i2p")으로 참조하는 기존 방법들이 있지만, 이러한 기법들은 전역적 고유성을 보장하지 않으며(각 개인의 머신에 로컬 데이터베이스로 저장되므로), 현재 메커니즘은 특히 확장 가능하거나 안전하지도 않습니다(호스트 목록에 대한 업데이트는 이름 지정 서비스에 대한 "구독"을 사용하여 관리됩니다). 언젠가는 안전하고, 사람이 읽을 수 있으며, 확장 가능하고, 전역적으로 고유한 이름 지정 시스템이 있을 수도 있지만, 그러한 시스템이 존재하는 것이 가능하지 않다고 생각하는 사람들이 있으므로 애플리케이션은 그러한 시스템이 구현되어 있다고 가정해서는 안 됩니다. [이름 지정 시스템에 대한 추가 정보](/docs/overview/naming/)를 확인할 수 있습니다.

대부분의 애플리케이션은 프로토콜과 포트를 구분할 필요가 없지만, I2P는 이를 *지원합니다*. 복잡한 애플리케이션은 단일 목적지에서 트래픽을 다중화하기 위해 메시지별로 프로토콜, 출발 포트, 도착 포트를 지정할 수 있습니다. 자세한 내용은 [datagram 페이지](/docs/api/datagrams/)를 참조하세요. 간단한 애플리케이션은 목적지의 "모든 포트"에서 "모든 프로토콜"을 수신하여 작동합니다.

### 익명성과 기밀성

I2P는 네트워크를 통해 전달되는 모든 데이터에 대해 투명한 종단 간 암호화와 인증을 제공합니다 — Bob이 Alice의 destination으로 보내면 Alice의 destination만이 이를 받을 수 있고, Bob이 datagram이나 streaming 라이브러리를 사용하는 경우 Alice는 Bob의 destination이 데이터를 보낸 것임을 확실히 알 수 있습니다.

물론 I2P는 Alice와 Bob 사이에 전송되는 데이터를 투명하게 익명화하지만, 그들이 보내는 콘텐츠 자체를 익명화하지는 않습니다. 예를 들어, Alice가 Bob에게 자신의 실명, 정부 발행 신분증, 신용카드 번호가 포함된 양식을 보낸다면, I2P가 할 수 있는 일은 없습니다. 따라서 프로토콜과 애플리케이션은 어떤 정보를 보호하려는지, 그리고 어떤 정보를 노출해도 되는지를 염두에 두어야 합니다.

### I2P 데이터그램은 최대 수 KB까지 가능

I2P 데이터그램(원시 또는 응답 가능한 것)을 사용하는 애플리케이션은 본질적으로 UDP 측면에서 생각할 수 있습니다. 데이터그램은 순서가 없고, 최선 노력 방식이며, 연결이 없습니다. 하지만 UDP와 달리 애플리케이션은 MTU 감지에 대해 걱정할 필요가 없고 단순히 큰 데이터그램을 전송할 수 있습니다. 상한선이 명목상 32 KB이지만, 메시지는 전송을 위해 단편화되어 전체의 신뢰성이 떨어집니다. 약 10 KB를 초과하는 데이터그램은 현재 권장되지 않습니다. 자세한 내용은 [데이터그램 페이지](/docs/api/datagrams/)를 참조하세요. 많은 애플리케이션에서 10 KB의 데이터는 전체 요청 또는 응답에 충분하므로, 단편화나 재전송 등을 작성할 필요 없이 UDP와 같은 애플리케이션으로 I2P에서 투명하게 작동할 수 있습니다.

---

## 개발 옵션

I2P를 통해 데이터를 전송하는 여러 가지 방법이 있으며, 각각 고유한 장단점이 있습니다. streaming lib은 대부분의 I2P 애플리케이션에서 사용되는 권장 인터페이스입니다.

### Streaming Lib

[전체 스트리밍 라이브러리](/docs/api/streaming/)는 이제 표준 인터페이스입니다. [스트리밍 개발 가이드](#developing-with-the-streaming-library)에서 설명하는 바와 같이 TCP와 유사한 소켓을 사용한 프로그래밍을 가능하게 합니다.

### BOB

BOB는 [Basic Open Bridge](/docs/legacy/bob/)로, 어떤 언어의 애플리케이션이든 I2P로부터 그리고 I2P로 스트리밍 연결을 만들 수 있게 해줍니다. 현재 시점에서는 UDP 지원이 부족하지만, 가까운 미래에 UDP 지원이 계획되어 있습니다. BOB에는 또한 destination 키 생성과 주소가 I2P 사양에 부합하는지 검증하는 것과 같은 여러 도구들이 포함되어 있습니다. 최신 정보와 BOB를 사용하는 애플리케이션들은 이 [I2P Site](http://bob.i2p/)에서 찾을 수 있습니다.

### SAM, SAM V2, SAM V3

*SAM은 권장되지 않습니다. SAM V2는 괜찮고, SAMv3가 권장됩니다.*

SAM은 [Simple Anonymous Messaging](/docs/legacy/sam/) 프로토콜로, 어떤 언어로 작성된 애플리케이션이든 일반 TCP 소켓을 통해 SAM 브릿지와 통신할 수 있게 해주며, 해당 브릿지가 모든 I2P 트래픽을 멀티플렉싱하고 암호화/복호화 및 이벤트 기반 처리를 투명하게 조정합니다. SAM은 세 가지 운영 방식을 지원합니다:

- streams, Alice와 Bob이 서로 데이터를 신뢰성 있고 순서대로 전송하고자 할 때 사용
- repliable datagrams, Alice가 Bob에게 Bob이 응답할 수 있는 메시지를 보내고자 할 때 사용
- raw datagrams, Alice가 최대한의 대역폭과 성능을 원하고, Bob이 데이터의 발신자가 인증되었는지 여부를 신경 쓰지 않을 때 사용 (예: 전송되는 데이터가 자체 인증됨)

SAM V3는 SAM 및 SAM V2와 동일한 목표를 지향하지만, 다중화/역다중화를 요구하지 않습니다. 각 I2P 스트림은 애플리케이션과 SAM bridge 간의 고유한 소켓으로 처리됩니다. 또한 데이터그램은 SAM bridge와의 데이터그램 통신을 통해 애플리케이션에서 송수신할 수 있습니다.

[SAM V2](/docs/legacy/samv2/)는 imule에서 사용하는 새로운 버전으로 [SAM](/docs/legacy/sam/)의 일부 문제점을 해결합니다.

[SAM V3](/docs/api/samv3/)는 imule 버전 1.4.0부터 사용됩니다.

### I2PTunnel

I2PTunnel 애플리케이션은 애플리케이션들이 I2PTunnel '클라이언트' 애플리케이션(특정 포트에서 수신 대기하고 해당 포트로 소켓이 열릴 때마다 특정 I2P destination에 연결) 또는 I2PTunnel '서버' 애플리케이션(특정 I2P destination에서 수신 대기하고 새로운 I2P 연결을 받을 때마다 특정 TCP 호스트/포트로 outproxy)을 생성하여 피어들과의 특정 TCP 유사 tunnel을 구축할 수 있게 합니다. 이러한 스트림은 8비트 클린이며, SAM이 사용하는 것과 동일한 스트리밍 라이브러리를 통해 인증되고 보안됩니다. 하지만 각각이 고유한 I2P destination과 자체 tunnel, 키 등을 가지므로 여러 고유한 I2PTunnel 인스턴스를 생성하는 데는 상당한 오버헤드가 수반됩니다.

### SOCKS

I2P는 SOCKS V4 및 V5 프록시를 지원합니다. 아웃바운드 연결은 잘 작동합니다. 인바운드(서버) 및 UDP 기능은 불완전하고 테스트되지 않았을 수 있습니다.

### Ministreaming

*제거됨*

예전에는 간단한 "ministreaming" 라이브러리가 있었지만, 이제 ministreaming.jar에는 전체 streaming 라이브러리의 인터페이스만 포함되어 있습니다.

### 데이터그램

*UDP와 같은 애플리케이션에 권장됨*

[Datagram 라이브러리](/docs/api/datagrams/)는 UDP와 유사한 패킷 전송을 가능하게 합니다. 다음을 사용할 수 있습니다:

- 응답 가능한 데이터그램
- 원시 데이터그램

### I2CP

*권장하지 않음*

[I2CP](/docs/specs/i2cp/) 자체는 언어 독립적인 프로토콜이지만, Java가 아닌 다른 언어로 I2CP 라이브러리를 구현하려면 상당한 양의 코드를 작성해야 합니다(암호화 루틴, 객체 마샬링, 비동기 메시지 처리 등). 누군가가 C나 다른 언어로 I2CP 라이브러리를 작성할 수는 있지만, 대신 C SAM 라이브러리를 사용하는 것이 더 유용할 것입니다.

### 웹 애플리케이션

I2P는 Jetty 웹서버와 함께 제공되며, 대신 Apache 서버를 사용하도록 구성하는 것은 간단합니다. 모든 표준 웹 앱 기술이 작동해야 합니다.

---

## 개발 시작하기 — 간단한 가이드

I2P를 사용한 개발에는 작동하는 I2P 설치와 원하는 개발 환경이 필요합니다. Java를 사용하는 경우 [streaming library](#developing-with-the-streaming-library) 또는 datagram library로 개발을 시작할 수 있습니다. 다른 프로그래밍 언어를 사용하는 경우 SAM 또는 BOB를 사용할 수 있습니다.

### Streaming Library를 사용한 개발

다음 예제는 스트리밍 라이브러리를 사용하여 TCP와 유사한 클라이언트 및 서버 애플리케이션을 생성하는 방법을 보여줍니다.

이를 위해서는 클래스패스에 다음 라이브러리들이 필요합니다:

- `$I2P/lib/streaming.jar`: streaming 라이브러리 자체
- `$I2P/lib/mstreaming.jar`: streaming 라이브러리용 팩토리 및 인터페이스
- `$I2P/lib/i2p.jar`: 표준 I2P 클래스, 데이터 구조, API 및 유틸리티

I2P 설치에서 이들을 가져오거나, Maven Central에서 다음 의존성을 추가할 수 있습니다:

- `net.i2p:i2p`
- `net.i2p.client:streaming`

네트워크 통신은 I2P 네트워크 소켓의 사용을 필요로 합니다. 이를 보여주기 위해, 클라이언트가 서버에 텍스트 메시지를 보낼 수 있고, 서버는 메시지를 출력하고 클라이언트에게 다시 보내는 애플리케이션을 만들어 보겠습니다. 즉, 서버는 에코 기능을 수행하게 됩니다.

서버 애플리케이션을 초기화하는 것부터 시작하겠습니다. 이를 위해서는 I2PSocketManager를 얻고 I2PServerSocket을 생성해야 합니다. 기존 Destination에 대한 저장된 키를 I2PSocketManagerFactory에 제공하지 않을 것이므로, 새로운 Destination을 생성할 것입니다. 따라서 I2PSocketManager에게 I2PSession을 요청하여 생성된 Destination을 확인할 것입니다. 클라이언트가 우리에게 연결할 수 있도록 나중에 해당 정보를 복사하여 붙여넣어야 하기 때문입니다.

```java
package i2p.echoserver;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        //Initialize application
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());
        //The additional main method code comes here...
    }

}
```
*코드 예제 1: 서버 애플리케이션 초기화.*

I2PServerSocket을 얻으면, 클라이언트로부터의 연결을 받아들이기 위해 I2PSocket 인스턴스를 생성할 수 있습니다. 이 예제에서는 한 번에 하나의 클라이언트만 처리할 수 있는 단일 I2PSocket 인스턴스를 생성할 것입니다. 실제 서버는 여러 클라이언트를 처리할 수 있어야 합니다. 이를 위해서는 각각 별도의 스레드에서 여러 I2PSocket 인스턴스를 생성해야 합니다. I2PSocket 인스턴스를 생성한 후에는 데이터를 읽고, 출력하고, 클라이언트에게 다시 전송합니다.

```java
package i2p.echoserver;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ConnectException;
import java.net.SocketTimeoutException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.util.I2PThread;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());

        //Create socket to handle clients
        I2PThread t = new I2PThread(new ClientHandler(serverSocket));
        t.setName("clienthandler1");
        t.setDaemon(false);
        t.start();
    }

    private static class ClientHandler implements Runnable {

        public ClientHandler(I2PServerSocket socket) {
            this.socket = socket;
        }

        public void run() {
            while(true) {
                try {
                    I2PSocket sock = this.socket.accept();
                    if(sock != null) {
                        //Receive from clients
                        BufferedReader br = new BufferedReader(new InputStreamReader(sock.getInputStream()));
                        //Send to clients
                        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(sock.getOutputStream()));
                        String line = br.readLine();
                        if(line != null) {
                            System.out.println("Received from client: " + line);
                            bw.write(line);
                            bw.flush(); //Flush to make sure everything got sent
                        }
                        sock.close();
                    }
                } catch (I2PException ex) {
                    System.out.println("General I2P exception!");
                } catch (ConnectException ex) {
                    System.out.println("Error connecting!");
                } catch (SocketTimeoutException ex) {
                    System.out.println("Timeout!");
                } catch (IOException ex) {
                    System.out.println("General read/write-exception!");
                }
            }
        }

        private I2PServerSocket socket;

    }

}
```
*코드 예제 2: 클라이언트로부터 연결을 수락하고 메시지를 처리하기.*

위의 서버 코드를 실행하면 다음과 같은 내용이 출력됩니다 (단, 줄 바꿈 없이 하나의 거대한 문자 블록으로 출력됩니다):

```
y17s~L3H9q5xuIyyynyWahAuj6Jeg5VC~Klu9YPquQvD4vlgzmxn4yy~5Z0zVvKJiS2Lk
poPIcB3r9EbFYkz1mzzE3RYY~XFyPTaFQY8omDv49nltI2VCQ5cx7gAt~y4LdWqkyk3au
...
```
이것은 서버 Destination의 base64 표현입니다. 클라이언트가 서버에 접근하려면 이 문자열이 필요합니다.

이제 클라이언트 애플리케이션을 만들어보겠습니다. 다시 초기화를 위해 여러 단계가 필요합니다. 다시 I2PSocketManager를 가져오는 것부터 시작해야 합니다. 이번에는 I2PSession과 I2PServerSocket을 사용하지 않습니다. 대신 서버 Destination 문자열을 사용하여 연결을 시작할 것입니다. 사용자에게 Destination 문자열을 요청하고, 이 문자열을 사용하여 I2PSocket을 생성할 것입니다. I2PSocket을 얻으면 서버와 데이터를 주고받기 시작할 수 있습니다.

```java
package i2p.echoclient;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.InterruptedIOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.ConnectException;
import java.net.NoRouteToHostException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;
import net.i2p.data.DataFormatException;
import net.i2p.data.Destination;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        System.out.println("Please enter a Destination:");
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String destinationString;
        try {
            destinationString = br.readLine();
        } catch (IOException ex) {
            System.out.println("Failed to get a Destination string.");
            return;
        }
        Destination destination;
        try {
            destination = new Destination(destinationString);
        } catch (DataFormatException ex) {
            System.out.println("Destination string incorrectly formatted.");
            return;
        }
        I2PSocket socket;
        try {
            socket = manager.connect(destination);
        } catch (I2PException ex) {
            System.out.println("General I2P exception occurred!");
            return;
        } catch (ConnectException ex) {
            System.out.println("Failed to connect!");
            return;
        } catch (NoRouteToHostException ex) {
            System.out.println("Couldn't find host!");
            return;
        } catch (InterruptedIOException ex) {
            System.out.println("Sending/receiving was interrupted!");
            return;
        }
        try {
            //Write to server
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            bw.write("Hello I2P!\n");
            //Flush to make sure everything got sent
            bw.flush();
            //Read from server
            BufferedReader br2 = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String s = null;
            while ((s = br2.readLine()) != null) {
                System.out.println("Received from server: " + s);
            }
            socket.close();
        } catch (IOException ex) {
            System.out.println("Error occurred while sending/receiving!");
        }
    }

}
```
*코드 예제 3: 클라이언트를 시작하고 서버 애플리케이션에 연결하기.*

마지막으로, 서버와 클라이언트 애플리케이션을 모두 실행할 수 있습니다. 먼저 서버 애플리케이션을 시작하세요. 서버는 Destination 문자열을 출력할 것입니다(위에 표시된 것처럼). 다음으로 클라이언트 애플리케이션을 시작하세요. Destination 문자열을 요청하면, 서버에서 출력된 문자열을 입력할 수 있습니다. 그러면 클라이언트는 'Hello I2P!'(개행 문자와 함께)를 서버에 보내고, 서버는 메시지를 출력한 후 클라이언트에게 다시 보내줍니다.

축하합니다, I2P를 통한 통신에 성공했습니다!

---

## 기존 애플리케이션

기여하고 싶으시면 저희에게 연락해 주세요.

- [I2P-Bote](http://i2pbote.i2p/) - HungryHobo에게 연락
- [Syndie](http://syndie.i2p2.de/)
- [IMule](http://www.imule.i2p/)
- [I2Phex](http://forum.i2p/viewforum.php?f=25)

[plugins.i2p](http://plugins.i2p/)의 모든 플러그인, [echelon.i2p](http://echelon.i2p/)에 나열된 애플리케이션과 소스 코드, 그리고 [git.repo.i2p](http://git.repo.i2p/)에서 호스팅되는 애플리케이션 코드도 참조하세요.

I2P 배포판에 포함된 번들 애플리케이션인 SusiMail과 I2PSnark도 참조하세요.

---

## 애플리케이션 아이디어

- NNTP 서버 - 과거에 몇 개가 있었지만, 현재는 없음
- Jabber 서버 - 과거에 몇 개가 있었고, 현재 공용 인터넷 접속이 가능한 서버가 하나 있음
- PGP 키 서버 및/또는 프록시
- 콘텐츠 배포 / DHT 애플리케이션 - feedspace 부활, dijjer 포팅, 대안 탐색
- [Syndie](http://syndie.i2p2.de/) 개발 지원
- 웹 기반 애플리케이션 - 블로그, 페이스트빈, 스토리지, 트래킹, 피드 등과 같은 웹 서버 기반 애플리케이션 호스팅에는 제한이 없습니다. Perl, PHP, Python, Ruby와 같은 모든 웹 또는 CGI 기술이 작동합니다.
- 기존 앱 부활, i2p 소스 패키지에 이전에 포함되었던 여러 앱들 - bogobot, pants, proxyscript, q, stasher, socks proxy, i2ping, feedspace
