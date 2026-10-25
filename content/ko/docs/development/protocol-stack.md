---
title: "프로토콜 스택"
description: "I2P 프로토콜 스택 계층 개요"
slug: "protocol-stack"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
aliases:
  - "/ko/docs/develop/protocol-stack"
  - "/ko/docs/develop/protocol-stack/"
---

I2P 스택은 익명 통신을 가능하게 하는 계층화된 설계입니다. 각 계층은 하위 계층 위에 특정 기능을 추가합니다. 각 구성 요소에 대한 자세한 내용은 [기술 문서 색인](/docs/develop/overview)을 참조하세요.

## 인터넷 계층 {#internet}

**IP** - Internet Protocol(인터넷 프로토콜)은 일반 인터넷에서 호스트 주소 지정과 최선 노력 전달(best-effort delivery)을 사용한 인터넷 전반의 패킷 라우팅을 허용합니다.

## 전송 계층 {#transport}

- **TCP** - 전송 제어 프로토콜로 패킷의 신뢰성 있고 순서대로 전달을 가능하게 합니다
- **UDP** - 사용자 데이터그램 프로토콜로 패킷의 비신뢰성, 순서 무관 전달을 가능하게 합니다

## I2P 전송 계층 {#i2p-transport}

암호화된 router 간 연결 (아직 익명이 아님):

- **[NTCP2](/docs/specs/ntcp2)** - NIO 기반 TCP 전송
- **[SSU2](/docs/specs/ssu2)** - 보안 반신뢰성 UDP 전송

## I2P Tunnel 계층 {#tunnels}

완전한 익명 암호화 터널 연결을 제공합니다:

- **[Tunnel 메시지](/docs/legacy/tunnel-message)** - 암호화된 I2NP 메시지와 전송을 위한 암호화된 지시사항
- **[I2NP 메시지](/docs/specs/i2np)** - 다중 홉 익명 라우팅을 위한 계층 암호화가 적용된 프로토콜 메시지

## I2P Garlic Layer {#garlic}

암호화되고 익명의 종단간 I2P 메시지 전송을 제공합니다:

- **[Garlic messages](/docs/overview/garlic-routing)** - 익명 전달을 위해 래핑된 I2NP 메시지

## I2P 클라이언트 레이어 {#client}

- **[I2CP](/docs/specs/i2cp)** - I2P Control Protocol은 애플리케이션이 router API를 직접 사용하지 않고도 I2P 네트워크에 접근할 수 있게 해줍니다

## I2P 종단간 전송 계층 {#e2e-transport}

- **[Streaming Library](/docs/api/streaming)** - TCP와 유사한 신뢰할 수 있는 순차 전송을 제공
- **[Datagram Library](/docs/api/datagrams)** - UDP와 유사한 비신뢰성 전송을 제공

## I2P 애플리케이션 인터페이스 레이어 {#app-interface}

애플리케이션 개발자를 위한 선택적 인터페이스:

- **[I2PTunnel](/docs/api/i2ptunnel)** - TCP 연결을 I2P 내외로 터널링합니다
- **[SAMv3](/docs/api/samv3)** - 비 Java 애플리케이션을 위한 Simple Anonymous Messaging 프로토콜

## I2P 애플리케이션 프록시 계층 {#app-proxy}

표준 인터넷 프로토콜용 프록시:

- **HTTP** - 웹 브라우징 프록시
- **IRC** - Internet Relay Chat 프록시
- **[SOCKS](/docs/api/socks)** - SOCKS4/4a/5 프록시
- **Streamr** - UDP 스트리밍 프록시

## 애플리케이션 {#applications}

애플리케이션은 다양한 계층에서 I2P와 인터페이스할 수 있습니다:

**Streaming/Datagram 애플리케이션:** - streaming 또는 datagram 라이브러리를 직접 사용하는 I2P 네이티브 애플리케이션

**SAM 애플리케이션:** - SAM 프로토콜을 사용하는 모든 언어의 애플리케이션

**I2P 전용 애플리케이션:** - I2P를 위해 특별히 설계된 애플리케이션들 (I2PSnark, SusiMail 등)

**표준 인터넷 애플리케이션:** - I2P 프록시를 사용하는 일반 애플리케이션 (웹 브라우저, IRC 클라이언트 등)

## 스택 다이어그램 {#diagram}

![I2P 프로토콜 스택](/images/protocol_stack.png)

참고: SAM은 스트리밍 라이브러리와 데이터그램을 모두 사용할 수 있습니다.
