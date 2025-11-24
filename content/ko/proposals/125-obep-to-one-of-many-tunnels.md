---
title: "OBEP의 1-of-N 또는 N-of-N 터널로의 전달"
number: "125"
author: "zzz, str4d"
created: "2016-03-10"
lastupdated: "2017-04-07"
status: "Open"
thread: "http://zzz.i2p/topics/2099"
---

## 개요

이 제안서는 네트워크 성능을 개선하기 위한 두 가지 개선점을 다룹니다:

- 하나의 옵션 대신 대안을 제공하여 OBEP에 IBGW 선택을 위임합니다.

- OBEP에서 멀티캐스트 패킷 라우팅을 가능하게 합니다.


## 동기

직접 연결의 경우, OBEP가 IBGWs와 연결하는 방식에 유연성을 줌으로써 연결 혼잡을 줄이는 것이 아이디어입니다. 여러 터널을 명시할 수 있는 능력은 또한 메시지를 명시된 모든 터널로 전달하여 OBEP에서 멀티캐스트를 구현할 수 있게 합니다.

이 제안서의 위임 부분에 대한 대안은 [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset) 해시를 통해 메시지를 보내는 것이며, 이는 기존에 타겟 [RouterIdentity](http://localhost:63465/en/docs/specs/common-structures/#common-structure-specification) 해시를 지정할 수 있는 능력과 유사합니다. 이것은 더 작은 메시지와 잠재적으로 더 새로운 LeaseSet을 생성하지만:

1. OBEP가 조회를 해야 합니다.

2. LeaseSet이 플러드필(floodfill)에 게시되지 않을 수 있어 조회가 실패할 수 있습니다.

3. LeaseSet이 암호화되어 있을 수 있어 OBEP가 리스를 얻지 못할 수 있습니다.

4. LeaseSet을 지정하면 OBEP에게 메시지의 [Destination]을 공개하게 되며, 이는 OBEP가 네트워크의 모든 LeaseSet을 긁어서 Lease를 찾지 않는 한 알 수 없는 정보입니다.


## 디자인

발신자(OBGW)는 타겟 [Leases]의 일부(또는 전부)를 전달 지침 [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions)에 배치할 것입니다.

OBEP는 그 중 하나를 선택하여 전달합니다. OBEP는 이미 연결되었거나 알고 있는 터널을 선택합니다. 이것은 OBEP-IBGW 경로를 빠르고 신뢰성 있게 만들며, 전체 네트워크 연결을 줄입니다.

우리는 [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions)의 플래그에서 하나의 사용되지 않은 전달 유형(0x03)과 두 개의 남은 비트(0과 1)를 사용하여 이 기능을 구현할 수 있습니다.


## 보안 고려

이 제안서는 OBGW의 타겟 목적지 또는 NetDB에 대한 시각에서 유출되는 정보 양을 변경하지 않습니다:

- OBEP를 제어하고 NetDB에서 LeaseSets를 긁어모으는 적은 [TunnelId](http://localhost:63465/en/docs/specs/common-structures/#tunnelid) / [RouterIdentity](http://localhost:63465/en/docs/specs/common-structures/#common-structure-specification) 쌍을 검색함으로써 특정 목적지로 메시지가 보내지는지 이미 결정할 수 있습니다. 최악의 경우, TMDI에 여러 개의 리스가 존재하면 적의 데이터베이스에서 일치 항목을 찾는 속도가 더 빨라질 수 있습니다.

- 악의적인 목적지를 운영하는 적은 서로 다른 인바운드 터널을 서로 다른 플러드필에 포함하는 LeaseSets를 게시하고, OBGW가 고객의 NetDB 시각에 대한 정보를 수집할 수 있습니다. OBEP가 사용할 터널을 선택하는 것은 OBGW가 선택하는 것과 기능적으로 동일합니다.

멀티캐스트 플래그는 OBGW가 OBEP에 멀티캐스트하고 있다는 사실을 유출합니다. 이는 더 높은 수준의 프로토콜을 구현할 때 고려해야 하는 성능 대 프라이버시 간의 절충을 생성합니다. 선택적인 플래그로서, 사용자는 그들의 응용 프로그램에 적합한 결정을 할 수 있습니다. 이러한 동작이 호환 가능한 응용 프로그램의 기본 동작이 된다면 모든 응용 프로그램에서 널리 사용된다면 메시지를 특정 응용 프로그램의 것으로 파악하는 정보 유출이 줄어들 것입니다.


## 명세

첫 번째 프래그먼트 전달 지침 [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions)은 다음과 같이 수정됩니다:

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +----+----+----+
|                        |dly | Message  
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|cnt | (o)
+----+----+----+----+----+----+----+----+
 Tunnel ID N   |                        |
+----+----+----+                        +
|                                       |
+                                       +
|         To Hash N (optional)          |
+                                       +
|                                       |
+              +----+----+----+----+----+
|              | Tunnel ID N+1 (o) |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|         To Hash N+1 (optional)        |
+                                       +
|                                       |
+                                  +----+
|                                  | sz
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 바이트
       비트 순서: 76543210
       비트 6-5: 전달 유형
                 0x03 = TUNNELS
       비트 0: 멀티캐스트? 0이면 터널 중 하나에 전달
                         1이면 모든 터널에 전달
                         전달 유형이 TUNNELS가 아니라면 미래 사용과의 호환성을 위해 0으로 설정

Count ::
       1 바이트
       선택적, 전달 유형이 TUNNELS인 경우에 존재
       2-255 - 뒤따를 id/hash 쌍의 수

Tunnel ID :: `TunnelId`
To Hash ::
       각 36 바이트
       선택적, 전달 유형이 TUNNELS인 경우에 존재
       id/hash 쌍

총 길이: 일반적인 길이는:
       75 바이트 (unfragmented tunnel message)의 count 2 TUNNELS 전달;
       79 바이트 (첫 번째 프래그먼트)의 count 2 TUNNELS 전달

나머지 전달 지침은 변경 없음
```


## 호환성

새로운 명세를 이해해야 하는 유일한 피어는 OBGWs와 OBEPs입니다. 대상 I2P 버전 [VERSIONS](/en/docs/specs/i2np/#protocol-versions)에 대한 정보를 기반으로 하는 아웃바운드 터널을 구축할 때, OBGWs는 호환 가능한 OBEPs를 선택해야 합니다:

* 호환되는 버전을 홍보하는 피어는 새로운 플래그를 해석하는 것을 지원해야 하며, 지침을 유효하지 않은 것으로 거부해서는 안됩니다.

