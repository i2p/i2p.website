---
title: "I2P proposal #165: SSU2 수정"
number: "165"
author: "weko, orignal, the Anonymous, zzz"
created: "2024-01-19"
lastupdated: "2024-11-17"
status: "Open"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.62"
---

weko, orignal, the Anonymous 그리고 zzz에 의해 제안됨.

### 개요

이 문서는 SSU2의 취약점을 악용한 I2P에 대한 공격에 대응하여 SSU2에 대한 변경 사항을 제안합니다. 주요 목표는 보안을 강화하고 분산 서비스 거부(DDoS) 공격과 익명성 해제 시도를 방지하는 것입니다.

### 위협 모델

공격자가 새로운 가짜 RI를 만듭니다(라우터가 존재하지 않음): 이는 일반 RI이지만, 실제 Bob의 라우터에서 주소, 포트, s 및 i 키를 가져와 네트워크에 범람시킵니다. 우리가 이 (실제라고 생각하는) 라우터와 연결을 시도할 때, 우리는 Alice로서 이 주소에 연결할 수 있지만, 실제 Bob의 RI로 수행했는지 확신할 수 없습니다. 이는 가능하며 분산 서비스 거부 공격(대량의 RI를 만들어 네트워크에 범람시키기)에도 사용되었습니다. 또한, 많은 RI를 가진 IP를 차단하면 공격자의 라우터를 프레이밍하지 않고 좋은 라우터를 프레이밍하여 비익명 공격을 쉽게 할 수 있습니다(이 RI를 하나의 라우터처럼 터널 빌딩을 효과적으로 분배하는 대신).

### 잠재적 해결책

#### 1. 이전(변경 전) 라우터 지원과 함께 수정

.. _overview-1:

개요
^^^^^^^^

기존 라우터와의 SSU2 연결을 지원하기 위한 해결책.

동작
^^^^^^^^^

Bob의 라우터 프로필에 '확인됨' 플래그가 있어야 하며, 이는 모든 신규 라우터에 대해 기본값으로 false입니다 (아직 프로필이 없는 경우). '확인됨' 플래그가 false일 때, 우리는 절대 Alice로서 Bob에게 SSU2 연결을 시도하지 않습니다 - RI를 확신할 수 없기 때문입니다. Bob이 NTCP2 또는 SSU2로 우리(Alice)에게 연결하거나, 우리가 (Alice) NTCP2로 Bob에게 한 번 연결하면(이 경우 Bob의 RouterIdent를 확인할 수 있음) 플래그가 true로 설정됩니다.

문제점
^^^^^^^^

그래서, 가짜의 SSU2-전용 RI 범람 문제: 우리는 이것을 직접 확인할 수 없으며, 실제 라우터가 우리와 연결할 때까지 기다려야만 합니다.

#### 2. 연결 생성 중에 RouterIdent 확인

.. _overview-2:

개요
^^^^^^^^

SessionRequest 및 SessionCreated에 "RouterIdent" 블록 추가.

RouterIdent 블록의 가능한 형식
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1 바이트 플래그, 32 바이트 RouterIdent. Flag_0: 수신자의 RouterIdent면 0, 발신자의 RouterIdent면 1

동작
^^^^^^^^

Alice는 (해야 함(1), 할 수 있음(2)) 페이로드에 RouterIdent 블록 Flag_0 = 0과 Bob의 RouterIdent를 보냅니다. Bob은 (해야 함(3), 할 수 있음(4)) 자신의 RouterIdent인지 확인하고, 아니면 "잘못된 RouterIdent" 이유로 세션을 종료합니다. 맞다면, 1의 Flag_0과 Bob의 RouterIdent를 포함한 RI 블록을 보냅니다.

(1)의 경우, Bob은 이전 라우터를 지원하지 않습니다. (2)의 경우, Bob은 이전 라우터를 지원하지만 가짜 RI로 연결하려는 라우터로부터 DDoS의 피해자가 될 수 있습니다. (3)의 경우, Alice는 이전 라우터를 지원하지 않습니다. (4)의 경우, Alice는 이전 라우터를 지원하고 하이브리드 스킴: 구 버전의 라우터를 위한 수정 1과 신규 라우터를 위한 수정 2를 사용합니다. 만약 RI가 새 버전이라고 말하지만 연결 중 RouterIdent 블록을 수신하지 못했다면 - 종료하고 RI를 제거합니다.

.. _problems-1:

문제점
^^^^^^^^

공격자는 자신의 가짜 라우터를 오래된 라우터로 위장할 수 있으며, (4)의 경우 어쨌든 수정 1처럼 '확인됨'을 기다리고 있습니다.

참고
^^^^^

32 바이트 RouterIdent 대신, 아마도 4 바이트 해시의 siphash, 어떤 HKDF 또는 다른 것을 사용할 수 있으며, 이는 충분해야 합니다.

#### 3. Bob은 i = RouterIdent로 설정

.. _overview-3:

개요
^^^^^^^^

Bob은 자신의 RouterIdent를 i 키로 사용합니다.

.. _behavior-1:

동작
^^^^^^^^

Bob은 (해야 함(1), 할 수 있음(2)) 자신의 RouterIdent를 SSU2의 i 키로 사용합니다.

(1)의 Alice는 i = Bob의 RouterIdent일 때만 연결합니다. (2)의 Alice는 하이브리드 방식(수정 3과 1)을 사용합니다: i = Bob의 RouterIdent일 때는 연결할 수 있고, 그렇지 않으면 먼저 확인해야 합니다(수정 1 참조).

(1)의 경우, Alice는 오래된 라우터를 지원하지 않습니다. (2)의 경우, Alice는 오래된 라우터를 지원합니다.

.. _problems-2:

문제점
^^^^^^^^

공격자는 자신의 가짜 라우터를 오래된 라우터로 위장할 수 있으며, (2)의 경우 어쨌든 수정 1처럼 '확인됨'을 기다리고 있습니다.

.. _notes-1:

참고
^^^^^

RI 크기를 절약하기 위해, i 키가 지정되지 않은 경우에 대한 처리를 추가하는 것이 좋습니다. 만약 그렇다면, i = RouterIdent입니다. 이 경우, Bob은 오래된 라우터를 지원하지 않습니다.

#### 4. SessionRequest의 KDF에 MixHash 추가

.. _overview-4:

개요
^^^^^^^^

MixHash(Bob의 식별 해시)를 "SessionRequest" 메시지의 NOISE 상태에 추가합니다, 예: 
h = SHA256 (h || Bob의 식별 해시).
이것은 ENCRYPT 또는 DECRYPT에 대한 마지막 MixHash로 사용되어야 합니다.
추가적인 SSU2 헤더 플래그 "Verify Bob의 식별" = 0x02가 도입되어야 합니다.

.. _behavior-4:

동작
^^^^^^^^

- Alice는 Bob의 RouterInfo에서 Bob의 식별 해시로 MixHash를 추가하고 ENCRYPT의 ad로 사용하며 "Verify Bob의 식별" 플래그를 설정합니다.
- Bob은 "Verify Bob의 식별" 플래그를 확인하고 자신의 식별 해시로 MixHash를 추가하며 DECRYPT의 ad로 사용합니다. AEAD/Chacha20/Poly1305가 실패하면, Bob은 세션을 닫습니다.

이전 라우터와의 호환성
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Alice는 Bob의 라우터 버전을 확인하고 제안서를 지원하는 최소 버전이 충족되면 이 MixHash를 추가하고 "Verify Bob의 식별" 플래그를 설정해야 합니다. 라우터가 오래된 경우, Alice는 MixHash를 추가하지 않고 "Verify Bob의 식별" 플래그를 설정하지 않습니다.
- Bob은 "Verify Bob의 식별" 플래그를 확인하고 이것이 설정된 경우 MixHash를 추가합니다. 이전 라우터는 이 플래그를 설정하지 않으며 이 MixHash가 추가되지 않아야 합니다.

.. _problems-4:

문제점
^^^^^^^^

- 공격자는 자신의 가짜 라우터를 오래된 버전으로 주장할 수 있습니다. 어느 시점에서 오래된 라우터는 주의해서 사용되어야 하며 다른 방법으로 확인된 후 사용되어야 합니다.

### 역호환성

수정사항에 설명되어 있습니다.

### 현재 상태

i2pd: 수정 1.
