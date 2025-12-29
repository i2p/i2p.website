---
title: "SAM v2"
description: "레거시 간단한 익명 메시징 프로토콜"
slug: "samv2"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **사용 중단됨:** I2P 0.6.1.31에 함께 제공된 SAM v2는 더 이상 유지보수되지 않습니다. 새로운 개발에는 [SAM v3](/docs/api/samv3/)를 사용하세요. v2가 v1에 비해 유일하게 개선된 점은 단일 SAM 연결에서 멀티플렉싱된 여러 소켓을 지원한 것이었습니다.

## 버전 노트

- 보고된 버전 문자열은 "2.0"으로 유지됩니다.
- 0.9.14 이후로 `HELLO VERSION` 메시지는 한 자리 `MIN`/`MAX` 값을 허용하며 `MIN` 매개변수는 선택 사항입니다.
- `DEST GENERATE`가 `SIGNATURE_TYPE`을 지원하므로 Ed25519 목적지를 생성할 수 있습니다.

## 세션 기본 사항

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]
```
- 각 destination(목적지 주소)은 활성 SAM 세션을 하나만 가질 수 있습니다(스트림, 데이터그램, 또는 원시).
- `STYLE`은 가상 스트림, 서명된 데이터그램, 또는 원시 데이터그램을 선택합니다.
- 추가 옵션은 I2CP로 전달됩니다(예: `tunnels.quantityInbound=3`).
- 응답은 v1을 따릅니다: `SESSION STATUS RESULT=OK|DUPLICATED_DEST|I2P_ERROR|INVALID_KEY`.

## 메시지 인코딩

공백으로 구분된 `key=value` 쌍으로 구성된 줄 단위 ASCII 형식입니다(값은 따옴표로 감쌀 수 있습니다). 통신 유형은 v1과 동일합니다:

- I2P streaming library를 통한 스트림
- 회신 가능한 데이터그램 (`PROTO_DATAGRAM`)
- 원시 데이터그램 (`PROTO_DATAGRAM_RAW`)

## 사용 시기

마이그레이션할 수 없는 레거시 클라이언트 전용입니다. SAM v3는 다음을 제공합니다:

- 이진 목적지 인계 (`DEST GENERATE BASE64`)
- 하위 세션 및 DHT(분산 해시 테이블) 지원 (v3.3)
- 향상된 오류 보고 및 옵션 협상

참고:

- [SAM v1](/docs/legacy/sam/)
- [SAM v3](/docs/api/samv3/)
- [데이터그램 API](/docs/api/datagrams/)
- [스트리밍 프로토콜](/docs/specs/streaming/)
