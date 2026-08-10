---
title: "대상 해시 피어 식별자를 사용하는 빠른 확장(BEP 6) 허용"
number: "172"
author: "dr|z3d"
created: "2026-08-10"
lastupdated: "2026-08-10"
status: "초안"
toc: true
---

## 개요

BEP 6(패스트 확장)은 **Have All / Have None**, **요청 거부**, **제안**, 그리고 **허용된 빠른 전송**(Allowed Fast)이라는 다섯 가지 기능을 포함한다. 와이어 프로토콜 — 즉, 협상 비트, 메시지 ID, 그리고 체크 의미 체계 — 는 전송 방식에 독립적이며 I2P 스트리밍 위에서도 그대로 동작한다. 그러나 BEP 6 중에서 I2P로 직접 매핑할 수 없는 유일한 부분은 **허용된 빠른 전송 세트 생성**(Allowed Fast set generation)인데, 이는 피어의 IPv4 주소를 기준으로 정의되기 때문이다. I2P 피어는 IP 주소를 가지지 않으며, 32바이트의 목적지 해시로 식별된다.

이 제안은 모든 I2P 토렌트 클라이언트가 동일한 피어와 토렌트에 대해 동일한 allowed fast 집합을 생성하도록 I2P 네이티브 allowed fast 집합 생성 방식을 표준화함으로써, 해당 기능이 다양한 구현 간에 유용하고 검증 가능하도록 합니다.

## 동기

새로운 피어들은 비트토런트의 티포탯(tit-for-tat) 방식이 본격화되기 전에 처음 몇 개의 조각을 받아야 합니다. I2P에서는 일반 인터넷(clearnet)보다 이 과정이 더 느립니다. 연결 설정과 조각 전달이 지연 시간이 큰 여러 개의 튜널 홉(hop)을 거쳐야 하기 때문에, 연결 후 처음으로 상호적으로 언촉(unchoke)되는 시점까지의 시간이 더 길어집니다. '허용된 빠른 전송'(Allowed Fast)은 바로 이 시간 창을 직접적으로 해결합니다. 즉, 시작하는 피어가 여전히 촉(choked) 상태일지라도 소수의 조각을 받을 수 있도록 허용되어 즉시 데이터를 수신하고, 더 빨리 상호 교환을 시작할 수 있게 됩니다.

참조 BEP 6은 피어의 IPv4 주소로부터 허용 가능한 빠른 세트를 계산하여 *송신자*가 *수신자*만 가진 조각들을 선택할 수 있도록 보장한다(여러 IP를 가진 한 사용자가 여러 세트를 수집하는 것을 방지). I2P에서는 피어의 목적지 해시가 동일한 결합 역할을 하며 모든 연결의 양 끝에서 사용 가능하므로, 이 세트는 결정적이며 로컬에서 검증 가능하다 — 이것은 IP 기반 방식이 제공할 수 없는 특성이다.

## BEP 6 수정

빠른 확장 협상과 네 가지 메시지 유형은 변경되지 않은 채 채택된다:

- 협상: 마지막 예약된 바이트의 세 번째로 낮은 중요 비트, `reserved[7] |= 0x04`, 양쪽 모두
- 모두 있음 `<len=0x0001><op=0x0E>`, 모두 없음 `<len=0x0001><op=0x0F>`
- 조각 제안 `<len=0x0005><op=0x0D><index>`
- 요청 거부 `<len=0x000D><op=0x10><index><begin><length>`
- 허용된 빠른 요청 `<len=0x0005><op=0x11><index>`
- 모든 요청은 정확히 하나의 응답(조각 또는 거부)을 생성함; 더 이상 요청이 보류 중일 때 자동 거부되지 않음

유일한 차이점은 허용된 빠른(Fast) 집합 생성 과정에서 IP 바이트를 피어의 대상 해시(destination hash) 바이트로 대체한다는 것이다.

### 편차: 마스킹된 IP 대신 해시 바이트 사용

BEP 6 참조, 단계 (1):

```
x = 0xFFFFFF00 & ip
```
이는 피어의 IPv4 주소에서 세 바이트를 사용하고 **4번째 바이트를 0으로 설정**합니다. 이는 서브넷 휴리스틱 방식입니다: 동일한 /24 서브넷 내에서 여러 IP를 확보할 수 있는 사용자는 여러 개의 허용된 고속 집합을 얻을 수 없어야 합니다.

우리의 I2P 버전은 이를 상대방의 32바이트 목적지 해시의 처음 네 바이트로 대체합니다:

```
x = first 4 bytes of peer destination hash
```
기준 구현과의 차이점:

> "그것은 IP의 3바이트 다음에 0이 오는 것입니다. 당신은 해시의 4바이트입니다. IP가 없고 4번째 바이트를 0으로 만들지 않기 때문에 BEP 6과 다릅니다."

I2P 연결의 양쪽 끝점은 이미 상대방의 대상 해시를 알고 있습니다(이는 연결이 생성된/생성된 주소이기 때문입니다). 따라서 추가적인 교환이나 NAT 탐지, 외부 IP 감지가 필요하지 않으며, 이러한 기능은 I2P에서 아예 존재하지 않습니다.

### 허용된 빠른 생성 알고리즘

`hash`를 수신 피어의 32바이트 목적지 해시, `infohash`를 토렌트의 20바이트 infohash, `sz`를 토렌트의 조각 수, `k`를 허용된 빠른 설정의 최종 조각 수(BEP 6에 따라 10)라고 하고, `a`를 출력 세트라고 하자:

```
x = hash[0:4]  ++  infohash        (1)
while |a| < k:
    x = SHA1(x)                    (2)
    for i in [0:5] and |a| < k:    (3)
        y = x[i*4 : i*4+4]         (4)
        index = y % sz             (5)
        if index not in a:         (6)
            add index to a         (7)
```
참고:

- 대상 해시의 4바이트가 마스킹된 IP 바이트 3개를 대체한다. 네 바이트 모두 해시 엔트로피를 포함하며, 어떤 바이트도 0으로 설정되지 않는다.
- BEP 6과 마찬가지로, SHA1 체인이 긴 의사 난수열을 생성하며, 이를 조각 인덱스로 분할한다. `k = 10`은 참조 기본값과 일치한다.
- 허용된 Fast 메시지는 참고용이다: 수신 측은 이를 발신 측이 해당 조각을 보유하고 있다고 해석해서는 안 되며, 오직 발신 측이 통제 상태에서도 해당 조각을 제공할 것임을 의미할 뿐이다.

## 장점

| 영역             | 이점                                                                                                                                                                                       |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 시작 대기 시간  | 새로운 피어는 choked 상태에서도 첫 번째 조각을 가져오므로, 다중 홉 I2P 터널에서 더 느린 tit-for-tat 초기화 과정을 단축시킵니다.                                                              |
| 결정성           | 이 집합은 대상 해시와 infohash의 순수 함수이므로, 모든 구현체가 동일한 집합을 계산할 수 있습니다. 반면 IP 기반 BEP 6에서는 발신자의 수신자 IP 인식이 (NAT로 인해) 다를 수 있습니다.         |
| 검증 가능성      | 수신 피어는 자신의 대상 해시를 알고 있으며, 해당 집합을 로컬에서 다시 계산하고 유효성을 검사함으로써 잘못된 동작을 하는 송신자를 탐지할 수 있습니다.                                             |
| IP 메커니즘 없음 | NAT 통과, 외부 IP 탐지, 서브넷 휴리스틱 등이 필요하지 않으며, 이러한 기법들은 I2P 상에서는 불가능하거나 의미가 없습니다.                                                                     |
| 신원 바인딩      | 목적지당 하나의 빠른 집합만 허용됩니다. 여러 목적지를 가진 사용자는 각각 하나의 집합만 받게 되며, 이는 일반 인터넷에서 IP 마스크가 제공하는 것과 동일한 게임 방지 특성을 제공합니다.        |
| 개인정보 보호    | 계산 과정에서 IP 주소가 전송되거나 암시되지 않습니다.                                                                                                                                         |
| 대역폭           | 대용량 트래커에서는 전체 비트필드 대신 Have All / Have None을 사용하며, Reject 명령어는 중복된 재요청을 제거합니다.                                                                           |
## 구현 고려 사항

- **피어 식별**: 스트리밍 연결(세션의 목적지)에서 피어의 목적지 해시를 가져오며, 이 값은 양쪽 끝에서 동일하게 사용됩니다. 아웃바운드 연결의 경우 연결한 목적지를 사용하고, 인바운드 연결의 경우 연결이 수신된 목적지를 사용합니다.
- **협상**: 핸드셰이크 중 `reserved[7] |= 0x04`를 전송합니다. 상대방 핸드셰이크에서도 해당 비트가 설정된 경우에만 Fast Extension 메시지를 전송합니다. 피어가 협상 없이 Fast Extension 메시지를 보내는 경우 연결을 종료합니다.
- **Have All / Have None**: 핸드셰이크 직후 bitfield / Have All / Have None 중 정확히 하나만 전송합니다. 시드의 경우 Have All을, 첫 번째 조각을 받기 전까지는 Have None을 사용합니다.
- **Allowed Fast 송신 측**: 실제로 소유한 조각만 광고해야 합니다. 수신 측은 차단된 상태에서도 해당 조각을 요청할 수 있습니다. *제공된* 조각 집합의 크기를 제한하세요 (예: BEP 6 권고에 따라, 이미 `k`개 이상의 조각을 보유한 피어의 allowed-fast 요청을 거부).
- **Allowed Fast 수신 측**: 집합을 저장하고, 차단된 상태에서도 해당 조각에 대한 요청을 허용합니다. 선택적으로, 자신의 목적지 해시와 infohash를 사용해 집합을 다시 계산하여 검증하고, 계산된 집합에 없는 조각은 무시합니다.
- **Reject**: 모든 요청은 정확히 하나의 응답을 받아야 합니다. 차단 시, 피어를 조용히 침묵시키는 대신 allowed fast 집합에 없는 모든 요청을 거부해야 합니다.
- **집합 크기**: 호환성을 위해 `k = 10`을 사용하세요. 부하 상황에서 피어는 더 낮은 `k`를 선택할 수 있지만, 양쪽 모두 실제로 제공할 수 있는 것만 광고해야 합니다.
- **조각 범위 제한**: `index = y % sz`는 토렌트의 전체 조각 수 `sz`를 사용해야 합니다. 해시 체인은 조각 범위에 따라 절단되지 않으므로, `sz` 이상의 인덱스는 무시합니다(방어적 처리).
- **하위 호환성**: fast 비트를 협상하지 않은 클라이언트는 이러한 메시지를 전혀 수신하지 않으며, 추가 프로토콜 변경은 필요 없습니다.

## 참조 구현

이 알고리즘은 작고 독립적이며, 어떤 언어로 구현하더라도 수십 줄 정도로 간단하다. 아래의 세 가지 예시는 동일한 입력(`hash[0:4] ++ infohash`, SHA1 체인, `y % sz`, `k = 10`으로 제한)에 대해 동일한 집합을 계산한다.

### 자바

```java
// I2P: peer.getPeerID().getDestHash() is the 32-byte destination hash.
// Big-endian word reads build each candidate piece index from the SHA1 chain.
import java.security.MessageDigest;
import java.util.HashSet;
import java.util.Set;

public static Set<Integer> generateAllowedFastSet(byte[] destHash, byte[] infohash, int pieces) {
    Set<Integer> rv = new HashSet<>(10);
    if (destHash == null || infohash == null || pieces <= 0) {
        return rv;
    }
    byte[] x = new byte[24];
    System.arraycopy(destHash, 0, x, 0, 4);          // 4 hash bytes, no IP, no zeroed 4th byte
    System.arraycopy(infohash, 0, x, 4, Math.min(20, infohash.length));
    MessageDigest md = MessageDigest.getInstance("SHA-1");
    while (rv.size() < 10) {
        x = md.digest(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            long y = ((x[i * 4] & 0xFFL) << 24) | ((x[i * 4 + 1] & 0xFFL) << 16)
                   | ((x[i * 4 + 2] & 0xFFL) << 8) | (x[i * 4 + 3] & 0xFFL);
            rv.add((int) (y % pieces));
        }
    }
    return rv;
}
```
### C++

```cpp
// Peer identity input is the 32-byte destination hash available on the connection.
#include <cstdint>
#include <set>
#include <vector>

extern std::vector<uint8_t> sha1(const std::vector<uint8_t>& in); // e.g. OpenSSL SHA1()

std::set<int> generate_allowed_fast_set(const std::vector<uint8_t>& dest_hash,
                                        const std::vector<uint8_t>& infohash,
                                        int pieces) {
    std::set<int> rv;
    if (dest_hash.size() < 4 || infohash.size() < 20 || pieces <= 0) { return rv; }
    std::vector<uint8_t> x(dest_hash.begin(), dest_hash.begin() + 4); // 4 hash bytes,
                                                                      // no IP mask
    x.insert(x.end(), infohash.begin(), infohash.begin() + 20);
    while (rv.size() < 10) {
        x = sha1(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            uint32_t y = (uint32_t(x[i * 4]) << 24) | (uint32_t(x[i * 4 + 1]) << 16) |
                         (uint32_t(x[i * 4 + 2]) << 8) | uint32_t(x[i * 4 + 3]);
            rv.insert(int(y % uint32_t(pieces)));
        }
    }
    return rv;
}
```
### 파이썬

```python
import hashlib

def generate_allowed_fast_set(dest_hash: bytes, infohash: bytes, pieces: int) -> set:
    """4 bytes of the destination hash stand in for the masked IP; no byte is zeroed."""
    rv = set()
    if len(dest_hash) < 4 or len(infohash) < 20 or pieces <= 0:
        return rv
    x = dest_hash[:4] + infohash[:20]
    while len(rv) < 10:
        x = hashlib.sha1(x).digest()
        for i in range(5):
            if len(rv) >= 10:
                break
            y = int.from_bytes(x[i * 4 : i * 4 + 4], "big")
            rv.add(y % pieces)
    return rv
```
## 호환성

- **와이어 호환 가능**: 협상 비트 및 메시지 형식은 평문 네트워크 BEP 6과 바이트 단위로 동일하며, 세트 생성 입력만 다릅니다.
- **네트워크 간 비상호 운용 가능**: I2P 클라이언트와 평문 네트워크 클라이언트는 어차피 서로 연결할 수 없으며, 이 차이는 피어 식별자 바이트에만 영향을 미치고 결코 와이어 형식에는 영향을 주지 않습니다.
- **I2P 내부에서**: 이 제안을 구현한 모든 클라이언트는 동일한 허용 고속 세트를 계산하며, 이를 상호 교환 가능하게 제공하고 검증할 수 있습니다. 허용 고속(Allowed Fast)을 무시하는 클라이언트는 이를 단순한 권고 사항으로 간주하여 시작 이점만 상실할 뿐입니다.

## 열린 질문들

1. 집합 크기 `k`를 10으로 고정해야 하는가, 아니면 BEP 6에서 허용하는 것처럼 요청 부하가 클 때 줄이는 등의 부하 적응형으로 해야 하는가?
2. 수신 측에서 수신한 집합을 자신의 대상 해시와 비교하여 일치하지 않는 인덱스는 폐기해야 하는가? (버그가 있거나 악의적인 송신자에 대한 방어) 권장되는 답은 '예'이다.
3. 아래와 같이 4바이트 *접두사* (바이트 0-3)를 선택할 것인지, 혹은 마지막 4바이트를 선택할 것인지 — 임의의 고정된 4바이트 구간은 동일한 성질을 제공하며, 접두사를 사용하면 참조 코드의 바이트 순서가 자연스럽게 유지된다 (`hash[0:4]`).

## 기존 기술

- 참고: [BEP 6 Fast Extension](https://www.bittorrent.org/beps/bep_0006.html)
- I2PSnark 참조 구현: `apps/i2psnark/java/src/org/klomp/snark/PeerState.java` 내 `PeerState.sendAllowedFast()` / `generateAllowedFastSet()` (@since 0.9.71+)
- BEP 40 (표준 피어 우선순위) 및 BEP 21 (부분 시드), 즉 I2PSnark에서 지원하는 두 가지 기능과 함께 작동함
