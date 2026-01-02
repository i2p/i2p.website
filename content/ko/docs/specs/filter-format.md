---
title: "접근 필터 형식"
description: "tunnel 접근 제어 필터 파일의 구문"
slug: "filter-format"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

액세스 필터는 I2PTunnel 서버 운영자가 원본 Destination(목적지 식별자)과 최근 연결 빈도에 따라 들어오는 연결을 허용, 차단, 또는 제한할 수 있도록 합니다. 필터는 규칙들로 이루어진 일반 텍스트 파일입니다. 파일은 위에서 아래로 읽히며, **처음 일치하는 규칙이 우선합니다**.

> 필터 정의 변경 사항은 **tunnel 재시작 시** 적용됩니다. 일부 빌드는 런타임에 파일 기반 목록을 다시 읽을 수 있지만, 변경 사항이 확실히 적용되도록 재시작을 계획해 두십시오.

## 파일 형식

- 한 줄에 하나의 규칙.  
- 빈 줄은 무시됩니다.  
- `#` 는 줄 끝까지 이어지는 주석을 시작합니다.  
- 규칙은 순서대로 평가되며, 처음 일치하는 항목이 사용됩니다.

## 임계값

**임계값**은 슬라이딩 시간 창 내에서 단일 Destination(I2P의 목적지 식별자)로부터 허용되는 연결 시도 횟수를 정의합니다.

- **수치:** `N/S`는 `S`초 동안 `N`개의 연결을 허용함을 의미합니다. 예: `15/5`는 5초 동안 최대 15개의 연결을 허용합니다. 해당 window(시간 창) 내에서 `N+1`번째 시도는 거부됩니다.  
- **키워드:** `allow`는 제한 없음(무제한)을 의미합니다. `deny`는 항상 거부함을 의미합니다.

## 규칙 구문

규칙의 형식은 다음과 같습니다:

```
<threshold> <scope> <target>
```
여기서:

- `<threshold>`는 `N/S`, `allow`, 또는 `deny`입니다  
- `<scope>`는 `default`, `explicit`, `file`, 또는 `record` 중 하나입니다(아래 참조)  
- `<target>`는 스코프에 따라 달라집니다

### 기본 규칙

다른 규칙이 일치하지 않을 때 적용됩니다. 기본 규칙은 **하나**만 허용됩니다. 이를 생략하면, 알 수 없는 목적지(Destination)는 제한 없이 허용됩니다.

```
15/5 default
allow default
deny default
```
### 명시적 규칙

Base32 주소(예: `example1.b32.i2p`) 또는 전체 키로 특정 Destination(목적지)을 지정합니다.

```
15/5 explicit example1.b32.i2p
deny explicit example2.b32.i2p
allow explicit example3.b32.i2p
```
### 파일 기반 규칙

외부 파일에 나열된 **모든** Destinations(I2P 목적지)를 대상으로 합니다. 각 줄에는 하나의 Destination이 포함되며, `#` 주석과 빈 줄이 허용됩니다.

```
15/5 file /var/i2p/throttled.txt
deny file /var/i2p/blocked.txt
allow file /var/i2p/trusted.txt
```
> 운영 참고: 일부 구현은 파일 목록을 주기적으로 다시 읽습니다. tunnel이 실행 중일 때 목록을 편집하면 변경 사항이 감지되기까지 짧은 지연이 있을 수 있습니다. 즉시 적용하려면 재시작하세요.

### 레코더(점진적 제어)

**recorder**(기록기)는 연결 시도를 모니터링하고, 임계값을 초과한 Destination(목적지 식별자)을 파일에 기록합니다. 그런 다음 해당 파일을 `file` 규칙에서 참조하여 이후 시도에 제한이나 차단을 적용할 수 있습니다.

```
# Start permissive
allow default

# Record Destinations exceeding 30 connections in 5 seconds
30/5 record /var/i2p/aggressive.txt

# Apply throttling to recorded Destinations
15/5 file /var/i2p/aggressive.txt
```
> 사용 중인 빌드에서 recorder 지원을 확인한 뒤에만 이에 의존하세요. 보장된 동작을 위해 `file` 목록을 사용하세요.

## 평가 순서

구체적인 규칙을 먼저, 일반적인 규칙을 나중에 배치하세요. 흔한 패턴:

1. 신뢰된 피어에 대한 명시적 허용 규칙  
2. 알려진 악성 사용자에 대한 명시적 차단 규칙  
3. 파일 기반 허용/차단 목록  
4. 점진적 대역폭 제한을 위한 로거  
5. 모든 경우를 포괄하는 기본 규칙

## 전체 예제

```
# Moderate limits by default
30/10 default

# Always allow trusted peers
allow explicit friend1.b32.i2p
allow explicit friend2.b32.i2p

# Block known bad actors
deny file /var/i2p/blocklist.txt

# Throttle aggressive sources
15/5 file /var/i2p/throttle.txt

# Automatically populate the throttle list
60/5 record /var/i2p/throttle.txt
```
## 구현 참고 사항

- 액세스 필터는 애플리케이션 처리 이전에 tunnel 계층에서 동작하므로 남용 트래픽을 조기에 거부할 수 있습니다.  
- 필터 파일을 I2PTunnel 구성 디렉터리에 배치하고 변경 사항을 적용하려면 tunnel을 재시작하십시오.  
- 서비스 전반에 일관된 정책을 원한다면 여러 tunnel에서 파일 기반 목록을 공유하십시오.
