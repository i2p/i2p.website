---
title: "데이터그램"
description: "I2CP 위의 인증된, 응답 가능한, 그리고 원시 메시지 형식들"
slug: "datagrams"
aliases:
  - "/ko/datagrams"
  - "/ko/datagrams/"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## 데이터그램 개요 {#overview}

Datagram은 기본 [I2CP](/docs/specs/i2cp)를 기반으로 하여 표준 형식으로 인증되고 응답 가능한 메시지를 제공합니다. 이를 통해 애플리케이션은 datagram에서 "발신자" 주소를 안정적으로 읽고 해당 주소가 실제로 메시지를 보냈다는 것을 알 수 있습니다. 기본 I2P 메시지는 완전히 원시 형태이므로 "발신자" 주소가 없기 때문에(IP 패킷과 달리) 일부 애플리케이션에는 이것이 필요합니다. 또한 페이로드에 서명함으로써 메시지와 발신자가 인증됩니다.

Datagram은 [streaming library 패킷](/docs/api/streaming)과 마찬가지로 애플리케이션 레벨 구조입니다. 이러한 프로토콜들은 저수준 [transport](/docs/overview/transport)와 독립적입니다. 프로토콜들은 router에 의해 I2NP 메시지로 변환되며, 어느 프로토콜이든 어느 transport에 의해서도 전송될 수 있습니다.

## 애플리케이션 가이드 {#application}

Java로 작성된 애플리케이션은 datagram API를 사용할 수 있으며, 다른 언어로 작성된 애플리케이션은 [SAM](/docs/api/samv3)의 datagram 지원을 사용할 수 있습니다. [SOCKS proxy](/docs/api/socks), 'streamr' tunnel 유형, udpTunnel 클래스에서 i2ptunnel의 제한적인 지원도 있습니다.

### 데이터그램 길이 {#length}

애플리케이션 설계자는 응답 가능한 데이터그램과 응답 불가능한 데이터그램 간의 트레이드오프를 신중히 고려해야 합니다. 또한 데이터그램 크기는 1KB tunnel 메시지로의 tunnel 분할로 인해 신뢰성에 영향을 미칩니다. 메시지 조각이 많을수록 중간 홉에서 그 중 하나가 드롭될 가능성이 높아집니다. 몇 KB보다 큰 메시지는 권장되지 않습니다. 약 10KB를 초과하면 전달 확률이 급격히 떨어집니다.

[데이터그램 사양 페이지를 참조하세요.](/docs/specs/datagrams)

또한 하위 계층에서 추가되는 다양한 오버헤드, 특히 garlic 메시지는 Kademlia-over-UDP 애플리케이션에서 사용하는 것과 같은 간헐적인 메시지에 큰 부담을 준다는 점을 유의하십시오. 현재 구현은 스트리밍 라이브러리를 사용하는 빈번한 트래픽에 맞춰 조정되어 있습니다.

### I2CP 프로토콜 번호와 포트 {#protocol}

서명된(응답 가능한) 데이터그램에 대한 표준 I2CP 프로토콜 번호는 PROTO_DATAGRAM (17)입니다. 애플리케이션은 I2CP 헤더에서 프로토콜을 설정하도록 선택할 수도 있고 그렇지 않을 수도 있습니다. 기본값은 구현에 따라 다릅니다. 동일한 Destination에서 수신된 데이터그램과 스트리밍 트래픽을 역다중화하려면 이를 설정해야 합니다.

데이터그램은 연결 지향적이지 않기 때문에, IP over UDP의 전통적인 방식처럼 애플리케이션은 데이터그램을 특정 피어나 통신 세션과 연관시키기 위해 포트 번호가 필요할 수 있습니다. 애플리케이션은 [I2CP 페이지](/docs/specs/i2cp#format)에 설명된 대로 I2CP (gzip) 헤더에 'from' 및 'to' 포트를 추가할 수 있습니다.

datagram API 내에서 비응답 가능(raw) 또는 응답 가능 여부를 지정하는 방법은 없습니다. 애플리케이션은 적절한 유형을 기대하도록 설계되어야 합니다. I2CP 프로토콜 번호나 포트는 datagram 유형을 나타내기 위해 애플리케이션에서 사용되어야 합니다. I2CP 프로토콜 번호 PROTO_DATAGRAM (서명됨, Datagram1로도 알려짐), PROTO_DATAGRAM_RAW, PROTO_DATAGRAM2, PROTO_DATAGRAM3이 이 목적을 위해 I2PSession API에서 정의되어 있습니다. 클라이언트/서버 datagram 애플리케이션의 일반적인 설계 패턴은 nonce를 포함한 요청에 서명된 datagram을 사용하고, 응답에는 raw datagram을 사용하여 요청의 nonce를 반환하는 것입니다.

**기본값:**

- PROTO_DATAGRAM = 17
- PROTO_DATAGRAM_RAW = 18
- PROTO_DATAGRAM2 = 19
- PROTO_DATAGRAM3 = 20

### 데이터 무결성 {#integrity}

데이터 무결성은 [I2CP 레이어](/docs/specs/i2cp#format)에 구현된 gzip CRC-32 체크섬에 의해 보장됩니다. 인증된 데이터그램(Datagram1 및 Datagram2)도 무결성을 보장합니다. datagram 프로토콜에는 체크섬 필드가 없습니다.

### 패킷 캡슐화 {#encapsulation}

각 datagram은 단일 메시지(또는 [Garlic Message](/docs/overview/garlic-routing)의 개별 clove)로 I2P를 통해 전송됩니다. 메시지 캡슐화는 기본 [I2CP](/docs/specs/i2cp), [I2NP](/docs/specs/i2np), 및 [tunnel message](/docs/specs/tunnel-message) 계층에서 구현됩니다. datagram 프로토콜에는 패킷 구분 메커니즘이나 길이 필드가 없습니다.

## 명세서 {#spec}

[데이터그램 사양 페이지를 참조하세요.](/docs/specs/datagrams)
