---
title: "SSU (레거시)"
description: "기존 Secure Semireliable UDP(보안 반신뢰성 UDP) 전송"
slug: "ssu"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
reviewStatus: "needs-review"
---

> **사용 중단됨:** SSU는 SSU2로 대체되었습니다. 지원은 i2pd 2.44.0 (API 0.9.56, 2022년 11월) 및 Java I2P 2.4.0 (API 0.9.61, 2023년 12월)에서 제거되었습니다.

SSU는 혼잡 제어, NAT 트래버설, 그리고 introducer(소개자 노드) 지원을 포함한 UDP 기반의 반신뢰성 전송을 제공했다. 이는 NAT/방화벽 뒤에 있는 router를 처리하고 IP 주소 확인을 조정함으로써 NTCP를 보완했다.

## 주소 구성 요소

- `transport`: `SSU`
- `caps`: 기능 플래그 (`B`, `C`, `4`, `6`, 등)
- `host` / `port`: IPv4 또는 IPv6 리스너(방화벽 뒤에 있을 때는 선택 사항)
- `key`: Base64 introduction key(소개 키)
- `mtu`: 선택 사항; 기본값 1484(IPv4) / 1488(IPv6)
- `ihost/ikey/iport/itag/iexp`: router가 방화벽 뒤에 있을 때의 introducer 항목(소개자)

## 기능

- introducer(소개자)를 이용한 협력적 NAT 트래버설
- 피어 테스트와 인바운드 패킷 검사를 통한 로컬 IP 감지
- 방화벽 상태를 다른 트랜스포트(전송 방식)와 router 콘솔로 자동 중계
- 준신뢰성 전달: 메시지를 한도까지 재전송한 뒤 폐기
- 가산 증가/승수 감소와 프래그먼트 ACK 비트필드를 사용하는 혼잡 제어

SSU는 타이밍 비콘과 MTU 협상과 같은 메타데이터 관련 작업도 처리했습니다. 모든 기능은 이제 (최신 암호기술을 사용하여) [SSU2](/docs/specs/ssu2/)에 의해 제공됩니다.
