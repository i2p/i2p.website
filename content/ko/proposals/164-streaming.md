---
title: "스트리밍 업데이트"
number: "164"
author: "zzz"
created: "2023-01-24"
lastupdated: "2023-10-23"
status: "Closed"
thread: "http://zzz.i2p/topics/3541"
target: "0.9.58"
implementedin: "0.9.58"
toc: true
---

## 개요

Java I2P 및 i2pd 라우터는 API 0.9.58 (2023년 3월 출시) 이전 버전에서 스트리밍 SYN 패킷 재연 공격에 취약합니다. 이는 프로토콜 설계 문제이며, 구현 버그는 아닙니다.

SYN 패킷은 서명되지만, Alice가 Bob에게 보내는 초기 SYN 패킷의 서명은 Bob의 정체성과 묶여 있지 않기 때문에 Bob은 해당 패킷을 저장하여 일부 피해자인 Charlie에게 재전송할 수 있습니다. Charlie는 그 패킷이 Alice로부터 온 것으로 착각하고 그녀에게 응답할 것입니다. 대부분의 경우 이는 해롭지 않지만, SYN 패킷은 Charlie가 즉시 처리할 수 있는 초기 데이터(예: GET 또는 POST)를 포함할 수 있습니다.


## 설계

Alice가 서명된 SYN 데이터에 Bob의 목적지 해시를 포함하도록 수정하였습니다. Bob은 수신시 해당 해시가 자신의 해시와 일치하는지 확인합니다.

잠재적 공격 피해자인 Charlie는 이 데이터를 검사하고, 자신의 해시와 일치하지 않으면 SYN을 거부합니다.

SYN에서 NACKs 옵션 필드를 사용하여 해시를 저장함으로써, 변경은 이전 버전과 호환됩니다. 현재 NACKs는 SYN 패킷에 포함되지 않으며 무시됩니다.

모든 옵션은 서명으로 포함되므로, Bob은 해시를 다시 작성할 수 없습니다.

Alice와 Charlie가 API 0.9.58 이상 버전인 경우, Bob의 재연 시도는 거부됩니다.


## 사양

[Streaming 사양](/docs/specs/streaming/)을 업데이트하여 다음 섹션을 추가합니다:

### 재연 방지

Bob이 Alice로부터 수신한 유효한 서명된 SYNCHRONIZE 패킷을 저장하고 후에 피해자인 Charlie에게 보내는 재연 공격을 방지하기 위해, Alice는 다음과 같이 SYNCHRONIZE 패킷에 Bob의 목적지 해시를 포함해야 합니다:

.. raw:: html

  {% highlight lang='dataspec' %}
Set NACK count field to 8
  Set the NACKs field to Bob's 32-byte destination hash

{% endhighlight %}

SYNCHRONIZE 수신 시, NACK 카운트 필드가 8인 경우, Bob은 NACKs 필드를 32바이트 목적지 해시로 해석해야 하며, 자신의 목적지 해시와 일치하는지 확인해야 합니다. 그는 또한 패킷의 서명을 통상적으로 확인해야 하며, 이는 NACK 카운트와 NACKs 필드를 포함한 전체 패킷을 포괄합니다. NACK 카운트가 8이고 NACKs 필드가 일치하지 않으면, Bob은 패킷을 버려야 합니다.

이는 버전 0.9.58 이상에서 필요합니다. 이는 이전 버전과 호환됩니다. SYNCHRONIZE 패킷에서 NACKs는 예상되지 않기 때문입니다. 대상은 다른 쪽에서 어떤 버전을 실행 중인지 알거나 알 수 없습니다.

Bob에서 Alice로 보내는 SYNCHRONIZE ACK 패킷에는 변경이 필요하지 않습니다; 해당 패킷에 NACKs를 포함하지 마십시오.


## 보안 분석

이 문제는 스트리밍 프로토콜이 2004년에 생성된 이후 존재해왔습니다. 이는 I2P 개발자에 의해 내부적으로 발견되었습니다. 이 문제가 악용된 증거는 없습니다. 실제 악용 성공 가능성은 응용 프로그램 계층 프로토콜 및 서비스에 따라 크게 달라질 수 있습니다. 피어 투 피어 응용 프로그램이 클라이언트/서버 응용 프로그램보다 더 영향을 받을 가능성이 높습니다.


## 호환성

문제 없음. 현재 모든 알려진 구현은 SYN 패킷의 NACKs 필드를 무시합니다. 그리고 심지어 무시하지 않고 8개의 다른 메시지에 대한 NACKs로 해석하려고 해도, 이들 메시지는 SYNCHRONIZE 핸드셰이크 동안 끊어져 있을 수 없으며 NACKs는 아무 의미가 없을 것입니다.


## 마이그레이션

구현은 언제든지 지원을 추가할 수 있으며 조정이 필요하지 않습니다. Java I2P 및 i2pd 라우터는 API 0.9.58 (2023년 3월 출시)에서 이를 구현했습니다.


