---
title: "양방향 터널"
number: "119"
author: "orignal"
created: "2016-01-07"
lastupdated: "2016-01-07"
status: "Needs-Research"
thread: "http://zzz.i2p/topics/2041"
---

## 개요

이 제안서는 I2P에서 양방향 터널을 구현하는 것에 관한 것입니다.

## 동기

i2pd는 현재로서는 다른 i2pd 라우터를 통해 구축되는 양방향 터널을 도입할 예정입니다. 네트워크에 대해서는 일반적인 인바운드 및 아웃바운드 터널로 나타날 것입니다.

## 설계

### 목표

1. 터널 빌드 메시지 수를 줄여 네트워크 및 CPU 사용량 감소
2. 참가자가 떠난 즉시 알 수 있는 능력
3. 더 정확한 프로파일링 및 통계
4. 다른 다크넷을 중간 피어로 사용

### 터널 수정

TunnelBuild
```````````
터널은 인바운드 터널과 동일한 방식으로 구축됩니다. 회신 메시지는 필요하지 않습니다. "entrance"라는 특별한 유형의 참가자는 플래그로 표시되며, 동시에 IBGW 및 OBEP로 작동합니다. 메시지는 VaribaleTunnelBuild와 동일한 형식을 가지지만 ClearText는 다른 필드를 포함합니다::

    in_tunnel_id
    out_tunnel_id
    in_next_tunnel_id
    out_next_tunnel_id
    in_next_ident
    out_next_ident
    layer_key, iv_key

이 필드는 또한 다음 피어가 속하는 다크넷 및 I2P가 아닌 경우의 추가 정보를 언급합니다.

TunnelTermination
`````````````````
피어가 떠나고자 할 때, layer key로 암호화된 TunnelTermination 메시지를 생성하여 "in" 방향으로 보냅니다. 참가자가 그러한 메시지를 받으면 본인의 layer key로 다시 암호화하여 다음 피어에게 보냅니다. 메시지가 터널 소유자에게 도달하면, 논문을 해독하여 암호화되지 않은 메시지를 얻을 때까지 피어별로 메시지를 해독하기 시작합니다. 어느 피어가 떠났는지 알아내고 터널을 종료합니다.
