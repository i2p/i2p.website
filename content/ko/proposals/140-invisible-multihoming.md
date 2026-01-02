---
title: "보이지 않는 멀티호밍"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "열기"
thread: "http://zzz.i2p/topics/2335"
toc: true
---

## 개요

이 제안서는 I2P 클라이언트, 서비스 또는 외부 밸런서 프로세스가 단일 [Destination](http://localhost:63465/docs/specs/common-structures/#destination)을 투명하게 호스팅하는 여러 router들을 관리할 수 있도록 하는 프로토콜 설계를 개요합니다.

이 제안은 현재 구체적인 구현을 명시하지 않습니다. [I2CP](/docs/specs/i2cp/)의 확장으로 구현되거나 새로운 프로토콜로 구현될 수 있습니다.

## 동기

멀티호밍은 동일한 Destination을 호스팅하기 위해 여러 router를 사용하는 것입니다. I2P에서 멀티호밍을 하는 현재 방식은 각 router에서 동일한 Destination을 독립적으로 실행하는 것이며, 특정 시점에 클라이언트가 사용하게 되는 router는 마지막으로 LeaseSet을 게시한 것입니다.

이것은 해킹이며 대규모 웹사이트에서는 확장성 있게 작동하지 않을 것으로 추정됩니다. 각각 16개의 터널을 가진 100개의 멀티호밍 라우터가 있다고 가정해봅시다. 그러면 10분마다 1600개의 LeaseSet 게시가 이루어지며, 이는 거의 초당 3개에 해당합니다. floodfill들이 과부하에 걸리고 스로틀이 작동할 것입니다. 그리고 이는 조회 트래픽을 언급하기도 전의 이야기입니다.

Proposal 123은 100개의 실제 LeaseSet 해시를 나열하는 meta-LeaseSet으로 이 문제를 해결합니다. 조회는 2단계 프로세스가 됩니다: 먼저 meta-LeaseSet을 조회하고, 그 다음 명명된 LeaseSet 중 하나를 조회합니다. 이는 조회 트래픽 문제에 대한 좋은 해결책이지만, 그 자체로는 심각한 프라이버시 누출을 야기합니다: 각 실제 LeaseSet이 단일 router에 대응되기 때문에, 게시된 meta-LeaseSet을 모니터링하여 어떤 multihoming router들이 온라인 상태인지 확인할 수 있습니다.

I2P 클라이언트나 서비스가 단일 Destination을 여러 router에 분산시킬 수 있는 방법이 필요합니다. 이는 LeaseSet 자체의 관점에서 볼 때 단일 router를 사용하는 것과 구별되지 않는 방식이어야 합니다.

## 설계

### Definitions

    User
        The person or organisation wanting to multihome their Destination(s). A
        single Destination is considered here without loss of generality (WLOG).

    Client
        The application or service running behind the Destination. It may be a
        client-side, server-side, or peer-to-peer application; we refer to it as
        a client in the sense that it connects to the I2P routers.

        The client consists of three parts, which may all be in the same process
        or may be split across processes or machines (in a multi-client setup):

        Balancer
            The part of the client that manages peer selection and tunnel
            building. There is a single balancer at any one time, and it
            communicates with all I2P routers. There may be failover balancers.

        Frontend
            The part of the client that can be operated in parallel. Each
            frontend communicates with a single I2P router.

        Backend
            The part of the client that is shared between all frontends. It has
            no direct communication with any I2P router.

    Router
        An I2P router run by the user that sits at the boundary between the I2P
        network and the user's network (akin to an edge device in corporate
        networks). It builds tunnels under the command of a balancer, and routes
        packets for a client or frontend.

### High-level overview

다음과 같은 원하는 구성을 상상해보십시오:

- 하나의 Destination을 가진 클라이언트 애플리케이션.
- 각각 3개의 인바운드 터널을 관리하는 4개의 router.
- 모든 12개의 터널은 단일 LeaseSet에 게시되어야 함.

### Single-client

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]-----
                 |-{ [Tunnel 3]===/               \
                 |                                 \
                 |-{ [Tunnel 4]===\                 \
  [Destination]  |-{ [Tunnel 5]====[Router 2]-----   \
    \            |-{ [Tunnel 6]===/               \   \
     [LeaseSet]--|                               [Client]
                 |-{ [Tunnel 7]===\               /   /
                 |-{ [Tunnel 8]====[Router 3]-----   /
                 |-{ [Tunnel 9]===/                 /
                 |                                 /
                 |-{ [Tunnel 10]==\               /
                 |-{ [Tunnel 11]===[Router 4]-----
                  -{ [Tunnel 12]==/
```
### 정의

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]---------[Frontend 1]
                 |-{ [Tunnel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Tunnel 4]===\            \                    \
  [Destination]  |-{ [Tunnel 5]====[Router 2]---\-----[Frontend 2]   \
    \            |-{ [Tunnel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Balancer]            [Backend]
                 |-{ [Tunnel 7]===\          /   /                /   /
                 |-{ [Tunnel 8]====[Router 3]---/-----[Frontend 3]   /
                 |-{ [Tunnel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Tunnel 10]==\          /                    /
                 |-{ [Tunnel 11]===[Router 4]---------[Frontend 4]
                  -{ [Tunnel 12]==/
```
### 고수준 개요

- Destination을 로드하거나 생성합니다.

- 각 라우터와 Destination에 연결된 세션을 엽니다.

- 주기적으로 (약 10분마다, 하지만 tunnel 활성도에 따라 더 길거나 짧을 수 있음):

- 각 라우터에서 fast tier를 획득합니다.

- 각 router로/로부터 tunnel을 구축하기 위해 피어들의 상위 집합을 사용합니다.

    - By default, tunnels to/from a particular router will use peers from
      that router's fast tier, but this is not enforced by the protocol.

- 모든 활성 router에서 활성 인바운드 터널 집합을 수집하고 LeaseSet을 생성합니다.

- 하나 이상의 라우터를 통해 LeaseSet을 게시합니다.

### 단일 클라이언트

이 구성을 생성하고 관리하기 위해, 클라이언트는 현재 [I2CP](/docs/specs/i2cp/)에서 제공하는 것 이상의 다음과 같은 새로운 기능이 필요합니다:

- LeaseSet을 생성하지 않고 router에게 터널을 구축하도록 지시합니다.
- 인바운드 풀에 있는 현재 터널 목록을 가져옵니다.

또한 다음 기능들은 클라이언트가 tunnel을 관리하는 방식에서 상당한 유연성을 제공할 것입니다:

- router의 fast tier 내용을 가져옵니다.
- 주어진 peer 목록을 사용하여 inbound 또는 outbound tunnel을 구축하도록 router에 지시합니다.

### 멀티 클라이언트

```
         Client                           Router

                    --------------------->  Create Session
   Session Status  <---------------------
                    --------------------->  Get Fast Tier
        Peer List  <---------------------
                    --------------------->  Create Tunnel
    Tunnel Status  <---------------------
                    --------------------->  Get Tunnel Pool
      Tunnel List  <---------------------
                    --------------------->  Publish LeaseSet
                    --------------------->  Send Packet
      Send Status  <---------------------
  Packet Received  <---------------------
```
### 일반 클라이언트 프로세스

**세션 생성** - 주어진 Destination에 대한 세션을 생성합니다.

**세션 상태** - 세션이 설정되었음을 확인하며, 클라이언트가 이제 tunnel 구축을 시작할 수 있습니다.

**Get Fast Tier** - router가 현재 터널 구축을 고려할 피어들의 목록을 요청합니다.

**피어 목록** - router에게 알려진 피어들의 목록입니다.

**터널 생성** - router가 지정된 피어들을 통해 새로운 터널을 구축하도록 요청합니다.

**Tunnel 상태** - 특정 tunnel 구축의 결과로, 사용 가능해진 후의 상태입니다.

**터널 풀 가져오기** - Destination에 대한 인바운드 또는 아웃바운드 풀의 현재 tunnel 목록을 요청합니다.

**Tunnel 목록** - 요청된 풀에 대한 tunnel들의 목록입니다.

**LeaseSet 게시** - router가 목적지에 대한 아웃바운드 터널 중 하나를 통해 제공된 LeaseSet을 게시하도록 요청합니다. 응답 상태는 필요하지 않습니다. router는 LeaseSet이 게시되었다고 만족할 때까지 계속 재시도해야 합니다.

**Send Packet** - 클라이언트로부터 나가는 패킷입니다. 선택적으로 패킷이 전송되어야 하는(해야 하는?) 아웃바운드 tunnel을 지정합니다.

**Send Status** - 패킷 전송의 성공 또는 실패를 클라이언트에게 알려줍니다.

**패킷 수신됨** - 클라이언트를 위한 수신 패킷입니다. 선택적으로 패킷이 수신된 인바운드 tunnel을 지정합니다(?)

## Security implications

router의 관점에서 보면, 이 설계는 기능적으로 현재 상태와 동일합니다. router는 여전히 모든 터널을 구축하고, 자체 피어 프로필을 유지하며, router와 클라이언트 운영 간의 분리를 시행합니다. 기본 구성에서는 해당 router에 대한 터널이 자체 fast tier에서 구축되기 때문에 완전히 동일합니다.

netDB의 관점에서, 이 프로토콜을 통해 생성된 단일 LeaseSet은 기존 기능을 활용하기 때문에 현재 상태와 동일합니다. 하지만 16개의 Lease에 근접한 더 큰 LeaseSet의 경우, 관찰자가 해당 LeaseSet이 multihomed임을 판단할 수 있을 가능성이 있습니다:

- 현재 고속 계층의 최대 크기는 75개 피어입니다. Inbound Gateway
  (IBGW, Lease에 게시된 노드)는 계층의 일부분에서 선택됩니다
  (터널 풀별로 개수가 아닌 해시로 무작위 분할됨):

      1 hop
          The whole fast tier

      2 hops
          Half of the fast tier
          (the default until mid-2014)

      3+ hops
          A quarter of the fast tier
          (3 being the current default)

이는 평균적으로 IBGW들이 20-30개의 피어 집합에서 선택된다는 의미입니다.

- 단일 홈 설정에서 전체 16개 터널 LeaseSet은 최대 (예를 들어) 20개 피어 세트에서 무작위로 선택된 16개의 IBGW를 가질 것입니다.

- 기본 구성을 사용하는 4개 router 멀티홈 설정에서, 전체 16-tunnel LeaseSet은 최대 80개의 피어 집합에서 무작위로 선택된 16개의 IBGW를 가지게 되며, router들 사이에는 공통 피어의 일부가 있을 가능성이 높습니다.

따라서 기본 설정으로는 통계 분석을 통해 LeaseSet이 이 프로토콜에 의해 생성되고 있다는 것을 알아낼 수 있을 가능성이 있습니다. 또한 router가 몇 개나 있는지 파악하는 것도 가능할 수 있지만, 빠른 계층에서의 이탈(churn) 효과가 이러한 분석의 효과를 감소시킬 것입니다.

클라이언트가 어떤 peer를 선택할지 완전히 제어할 수 있으므로, 제한된 peer 집합에서 IBGW를 선택함으로써 이러한 정보 누출을 줄이거나 제거할 수 있습니다.

## Compatibility

이 설계는 LeaseSet 형식에 변경사항이 없기 때문에 네트워크와 완전히 하위 호환됩니다. 모든 router들이 새로운 프로토콜을 인식해야 하지만, 모두 동일한 주체에 의해 제어될 것이므로 이는 문제가 되지 않습니다.

## Performance and scalability notes

LeaseSet당 16개의 Lease라는 상한선은 이 제안에 의해 변경되지 않습니다. 이보다 더 많은 터널이 필요한 Destination의 경우, 두 가지 가능한 네트워크 수정 방법이 있습니다:

- LeaseSet 크기의 상한선을 늘립니다. 이것이 구현하기에는 가장 간단하지만 (광범위하게 사용되기 전에 전반적인 네트워크 지원이 여전히 필요하지만), 더 큰 패킷 크기로 인해 조회 속도가 느려질 수 있습니다. 실현 가능한 최대 LeaseSet 크기는 기본 전송의 MTU에 의해 정의되므로 약 16kB입니다.

- 계층화된 LeaseSet을 위한 제안 123을 구현합니다. 이 제안과 함께, 하위 LeaseSet들의 Destination들을 여러 router들에 분산시킬 수 있으며, 이는 일반 인터넷 서비스의 여러 IP 주소처럼 효과적으로 작동합니다.

## Acknowledgements

이 제안으로 이어진 토론에 대해 psi에게 감사드립니다.
