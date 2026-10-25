---
title: "Garlic Routing"
description: "I2P에서 garlic routing 용어, 아키텍처 및 구현 이해하기"
slug: "garlic-routing"
aliases:
  - "/ko/how_garlicrouting"
  - "/ko/how_garlicrouting/"
lastUpdated: "2025-10"
accurateFor: "0.9.12"
---

## Garlic Routing과 "Garlic" 용어

"garlic routing"과 "garlic encryption"이라는 용어들은 I2P의 기술을 언급할 때 종종 다소 느슨하게 사용됩니다. 여기서는 이 용어들의 역사, 다양한 의미, 그리고 I2P에서 "garlic" 방식의 사용법에 대해 설명합니다.

"Garlic routing"은 [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/)이 Roger Dingledine의 Free Haven [석사 논문](https://www.freehaven.net/papers.html) 섹션 8.1.1 (2000년 6월)에서 [Onion Routing](https://www.onion-router.net/)에서 파생되어 처음 만든 용어입니다.

"Garlic"이라는 용어는 I2P가 Freedman이 설명하는 형태의 번들링을 구현하기 때문에 I2P 개발자들이 원래 사용했거나, 단순히 Tor와의 일반적인 차이점을 강조하기 위해 사용했을 수 있습니다. 구체적인 이유는 역사 속으로 사라졌을 수도 있습니다. 일반적으로 I2P를 언급할 때, "garlic"이라는 용어는 다음 세 가지 중 하나를 의미할 수 있습니다:

1. 계층화된 암호화
2. 여러 메시지를 함께 묶기
3. ElGamal/AES 암호화

불행히도 지난 몇 년 동안 I2P의 "garlic" 용어 사용이 항상 정확하지는 않았습니다. 따라서 독자는 이 용어를 접할 때 주의해야 합니다. 아래 설명이 상황을 명확하게 해줄 것입니다.

### 계층형 암호화

Onion routing은 일련의 피어들을 통해 경로나 tunnel을 구축한 다음 해당 tunnel을 사용하는 기법입니다. 메시지는 발신자에 의해 반복적으로 암호화되고, 각 홉에서 복호화됩니다. 구축 단계에서는 다음 홉에 대한 라우팅 지시만이 각 피어에게 노출됩니다. 운영 단계에서는 메시지가 tunnel을 통해 전달되며, 메시지와 그 라우팅 지시는 tunnel의 끝점에만 노출됩니다.

이는 Mixmaster([네트워크 비교](/docs/overview/comparison/) 참조)가 메시지를 전송하는 방식과 유사합니다 - 메시지를 받아서 수신자의 공개 키로 암호화하고, 그 암호화된 메시지를 (다음 홉을 지정하는 지시사항과 함께) 다시 암호화한 다음, 그 결과로 나온 암호화된 메시지를 다시 암호화하는 과정을 반복하여, 경로상의 각 홉마다 하나의 암호화 레이어를 갖게 됩니다.

이런 의미에서 일반적인 개념으로서의 "garlic routing"은 "onion routing"과 동일합니다. 물론 I2P에서 구현된 것은 Tor의 구현과는 몇 가지 차이점이 있습니다(아래 참조). 그럼에도 불구하고 상당한 유사점이 있어서 I2P는 [onion routing에 대한 대량의 학술 연구](https://www.onion-router.net/Publications.html), [Tor, 그리고 유사한 mixnet들](https://freehaven.net/anonbib/topic.html)로부터 혜택을 받고 있습니다.

### 여러 메시지 번들링

Michael Freedman은 "garlic routing"을 onion routing의 확장으로 정의했는데, 여기서는 여러 메시지가 함께 묶입니다. 그는 각 메시지를 "bulb"라고 불렀습니다. 각각 고유한 전달 지침을 가진 모든 메시지들이 종단점에서 노출됩니다. 이를 통해 onion routing "reply block"을 원본 메시지와 효율적으로 묶을 수 있습니다.

이 개념은 아래에서 설명하는 바와 같이 I2P에서 구현되어 있습니다. garlic "bulbs"에 대한 우리의 용어는 "cloves"입니다. 단일 메시지가 아닌 여러 개의 메시지가 포함될 수 있습니다. 이는 Tor에서 구현된 onion routing과는 중요한 차이점입니다. 하지만 이는 I2P와 Tor 간의 많은 주요 아키텍처 차이점 중 하나일 뿐입니다. 아마도 이것만으로는 용어 변경을 정당화하기에 충분하지 않을 수도 있습니다.

Freedman이 설명한 방법과의 또 다른 차이점은 경로가 단방향이라는 것입니다. onion routing이나 mixmaster 응답 블록에서 볼 수 있는 "전환점"이 없어서 알고리즘이 크게 단순화되고 더 유연하고 신뢰할 수 있는 전달이 가능합니다.

### ElGamal/AES 암호화

일부 경우에는 "garlic encryption"이 단순히 [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) 암호화(다중 레이어 없이)를 의미할 수 있습니다.

---

## I2P의 "Garlic" 방식

이제 다양한 "garlic" 용어들을 정의했으므로, I2P가 세 곳에서 garlic routing, 번들링 및 암호화를 사용한다고 말할 수 있습니다:

1. tunnel을 구축하고 라우팅하기 위해 (계층 암호화)
2. 종단 간 메시지 전달의 성공 또는 실패를 판단하기 위해 (번들링)
3. 일부 네트워크 데이터베이스 항목을 게시하기 위해 (성공적인 트래픽 분석 공격의 가능성을 줄임) (ElGamal/AES)

이 기법은 네트워크 성능을 향상시키는 데 중요한 방법들로도 활용될 수 있으며, 전송 지연시간/처리량 트레이드오프를 활용하고, 신뢰성을 높이기 위해 중복 경로를 통해 데이터를 분기시킬 수 있습니다.

### 터널 구축 및 라우팅

I2P에서 tunnel은 단방향입니다. 각 당사자는 두 개의 tunnel을 구축하는데, 하나는 아웃바운드용이고 다른 하나는 인바운드 트래픽용입니다. 따라서 단일 왕복 메시지와 응답에는 네 개의 tunnel이 필요합니다.

Tunnel은 계층화된 암호화를 사용하여 구축되고 사용됩니다. 이는 [tunnel 구현 페이지](/docs/specs/tunnel-implementation/)에서 설명됩니다. 암호화를 위해 [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/)를 사용합니다.

Tunnel은 모든 [I2NP 메시지](/docs/specs/i2np/)를 전송하는 범용 메커니즘이며, Garlic Message는 tunnel 구축에 사용되지 않습니다. 우리는 outbound tunnel 엔드포인트에서 풀기 위해 여러 I2NP 메시지를 단일 Garlic Message로 묶지 않습니다. tunnel 암호화만으로 충분합니다.

### End-to-End 메시지 번들링

tunnel 위의 계층에서 I2P는 [Destinations](/docs/specs/common-structures/) 간에 end-to-end 메시지를 전달합니다. 단일 tunnel 내에서와 마찬가지로 암호화를 위해 [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/)를 사용합니다. [I2CP interface](/docs/api/i2cp/)를 통해 router에 전달되는 각 클라이언트 메시지는 Garlic Message 내에서 자체 Delivery Instructions를 가진 단일 Garlic Clove가 됩니다. Delivery Instructions는 Destination, Router 또는 Tunnel을 지정할 수 있습니다.

일반적으로 Garlic Message는 하나의 clove만 포함합니다. 그러나 router는 주기적으로 Garlic Message에 두 개의 추가 clove를 번들로 묶습니다:

![Garlic Message Cloves](/images/garliccloves.svg)

1. **배송 상태 메시지**, 승인으로써 원래 router로 다시 보내도록 지정하는 배송 지침과 함께. 이는 참조 문서에 설명된 "응답 블록" 또는 "응답 어니언"과 유사합니다. 종단 간 메시지 배송의 성공 또는 실패를 판단하는 데 사용됩니다. 원래 router는 예상 시간 내에 배송 상태 메시지를 받지 못할 경우, 원격 목적지로의 라우팅을 수정하거나 다른 조치를 취할 수 있습니다.

2. **Database Store 메시지**, 원본 Destination에 대한 LeaseSet을 포함하며, 원격 destination의 router를 지정하는 전송 지침을 담고 있습니다. router가 주기적으로 LeaseSet을 번들링함으로써, 원격 측이 통신을 유지할 수 있도록 보장합니다. 그렇지 않으면 원격 측은 네트워크 데이터베이스 항목에 대해 floodfill router에 쿼리해야 하고, [네트워크 데이터베이스 페이지](/docs/specs/common-structures/)에서 설명된 바와 같이 모든 LeaseSet이 네트워크 데이터베이스에 게시되어야 합니다.

기본적으로 Delivery Status와 Database Store 메시지는 로컬 LeaseSet이 변경되거나, 추가 세션 태그가 전달되거나, 이전 1분 동안 메시지가 번들링되지 않은 경우에 번들링됩니다.

명백히, 추가 메시지들은 현재 특정 목적을 위해 번들로 묶여 있으며, 범용 라우팅 체계의 일부가 아닙니다.

릴리스 0.9.12부터 배송 상태 메시지는 발신자에 의해 다른 garlic 메시지로 래핑되어, 내용이 암호화되고 반환 경로의 router들에게 보이지 않게 됩니다.

### Floodfill Network Database로의 저장

[네트워크 데이터베이스 페이지](/docs/specs/common-structures/)에서 설명했듯이, 로컬 leaseSet은 Garlic Message로 래핑된 Database Store Message를 통해 floodfill router에 전송되므로 터널의 아웃바운드 게이트웨이에서는 보이지 않습니다.

---

## 향후 작업

Garlic Message 메커니즘은 매우 유연하며 다양한 유형의 mixnet 전달 방법을 구현하기 위한 구조를 제공합니다. tunnel 메시지 전달 지침에서 사용되지 않은 지연 옵션과 함께, 광범위한 배칭, 지연, 혼합 및 라우팅 전략이 가능합니다.

특히, 아웃바운드 tunnel 엔드포인트에서 훨씬 더 많은 유연성의 가능성이 있습니다. 메시지는 그곳에서 여러 tunnel 중 하나로 라우팅될 수 있어 (따라서 지점 간 연결을 최소화) 중복성을 위해 여러 tunnel로 멀티캐스트되거나 오디오 및 비디오 스트리밍이 가능할 수 있습니다.

이러한 실험은 특정 라우팅 경로 제한, 다양한 경로를 따라 전달될 수 있는 I2NP 메시지 유형 제한, 특정 메시지 만료 시간 강제 적용 등 보안과 익명성을 보장해야 하는 필요성과 충돌할 수 있습니다.

ElGamal/AES 암호화의 일부로서, garlic 메시지는 송신자가 지정한 양의 패딩 데이터를 포함하여, 송신자가 트래픽 분석에 대한 적극적인 대응책을 취할 수 있도록 합니다. 이는 현재 16바이트의 배수로 패딩하는 요구사항을 넘어서는 용도로는 사용되지 않습니다.

[floodfill router](/docs/specs/common-structures/)와 주고받는 추가 메시지의 암호화.

---

## 참고 자료

- garlic routing이라는 용어는 Roger Dingledine의 Free Haven [석사 논문](https://www.freehaven.net/papers.html) (2000년 6월)에서 처음 만들어졌으며, [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/)이 저술한 8.1.1 섹션을 참조하십시오.
- [Onion Router Publications](https://www.onion-router.net/Publications.html)
- [Onion Routing (Wikipedia)](https://en.wikipedia.org/wiki/Onion_routing)
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)
- [Tor Project](https://www.torproject.org/)
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)
- Onion routing은 1996년 David M. Goldschlag, Michael G. Reed, Paul F. Syverson이 작성한 [Hiding Routing Information](https://www.onion-router.net/Publications/IH-1996.pdf)에서 처음 설명되었습니다.
