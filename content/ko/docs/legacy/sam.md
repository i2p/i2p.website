---
title: "SAM v1"
description: "레거시 단순 익명 메시징 프로토콜(사용 중단됨)"
slug: "sam"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **사용 중단됨:** SAM v1은 역사적 참고용으로만 유지됩니다. 새 애플리케이션은 [SAM v3](/docs/api/samv3/) 또는 [BOB](/docs/legacy/bob/)를 사용해야 합니다. 원래의 브리지는 DSA-SHA1 목적지와 제한된 옵션 집합만을 지원합니다.

## 라이브러리

Java I2P 소스 트리에는 여전히 C, C#, Perl, Python용 레거시 바인딩이 포함되어 있습니다. 이들은 더 이상 유지보수되지 않으며, 주로 아카이브 호환성을 위해 배포됩니다.

## 버전 협상

클라이언트는 TCP(기본값 `127.0.0.1:7656`)를 통해 연결하고 다음을 교환합니다:

```
Client → HELLO VERSION MIN=1 MAX=1
Bridge → HELLO REPLY RESULT=OK VERSION=1.0
```
Java I2P 0.9.14 기준으로 `MIN` 매개변수는 선택 사항이며, 업그레이드된 브리지의 경우 `MIN`/`MAX` 모두 한 자리 숫자 형태(`"3"` 등)를 허용합니다.

## 세션 생성

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]*
```
- `DESTINATION=name`은 `sam.keys`에서 항목을 로드하거나 생성합니다; `TRANSIENT`는 항상 임시 Destination(목적지)을 생성합니다.
- `STYLE`은 가상 스트림(TCP와 유사한), 서명된 데이터그램, 또는 원시 데이터그램을 선택합니다.
- `DIRECTION`은 스트림 세션에만 적용되며; 기본값은 `BOTH`입니다.
- 추가 키/값 쌍은 I2CP 옵션으로 전달됩니다(예: `tunnels.quantityInbound=3`).

브리지는 다음과 같이 응답합니다:

```
SESSION STATUS RESULT=OK DESTINATION=name
```
실패하면 `DUPLICATED_DEST`, `I2P_ERROR`, 또는 `INVALID_KEY` 중 하나와 선택적 메시지를 반환합니다.

## 메시지 형식

SAM 메시지는 공백으로 구분된 키/값 쌍으로 이루어진 단일 줄 ASCII 텍스트입니다. 키는 UTF‑8을 사용하며, 값은 공백을 포함할 경우 따옴표로 감쌀 수 있습니다. 이스케이프는 정의되어 있지 않습니다.

통신 유형:

- **스트림(Streams)** – I2P streaming library를 통해 프록시됨
- **회신 가능한 데이터그램(Repliable datagrams)** – 서명된 페이로드 (Datagram1)
- **원시 데이터그램(Raw datagrams)** – 서명되지 않은 페이로드 (Datagram RAW)

## 0.9.14에서 추가된 옵션

- `DEST GENERATE`는 `SIGNATURE_TYPE=...`를 지원합니다(예: Ed25519 등).
- `HELLO VERSION`은 `MIN`을 선택 사항으로 간주하며 한 자리 버전 문자열을 허용합니다

## SAM v1을 언제 사용해야 하나

업데이트할 수 없는 레거시 소프트웨어와의 상호 운용을 위한 경우에만 사용하십시오. 새로운 모든 개발에는 다음을 사용하십시오:

- [SAM v3](/docs/api/samv3/) 완전한 기능의 스트림/데이터그램 액세스용
- [BOB](/docs/legacy/bob/) 목적지 관리용 (아직 제한적이지만, 더 현대적인 기능을 지원)

## 참고 자료

- [SAM v2](/docs/legacy/samv2/)
- [SAM v3](/docs/api/samv3/)
- [데이터그램 사양](/docs/api/datagrams/)
- [스트리밍 프로토콜](/docs/specs/streaming/)

SAM v1은 router에 구애받지 않는 애플리케이션 개발의 토대를 마련했지만, 생태계는 이미 다음 단계로 넘어갔습니다. 이 문서는 출발점이라기보다 호환성 확보를 위한 보조 자료로 취급하십시오.
