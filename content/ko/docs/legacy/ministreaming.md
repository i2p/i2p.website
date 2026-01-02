---
title: "미니스트리밍 라이브러리"
description: "I2P의 최초 TCP 유사 전송 계층에 대한 역사적 기록"
slug: "ministreaming"
lastUpdated: "2025-02"
accurateFor: "historical"
---

> **사용 중단됨:** ministreaming 라이브러리(과거의 경량 스트리밍 라이브러리)는 오늘날의 [스트리밍 라이브러리](/docs/specs/streaming/)보다 먼저 만들어졌습니다. 최신 애플리케이션은 정식 스트리밍 API 또는 SAM v3를 사용해야 합니다. 아래 정보는 `ministreaming.jar`에 포함되어 배포되던 레거시 소스 코드를 검토하는 개발자들을 위해 보존되어 있습니다.

## 개요

Ministreaming(경량 스트리밍 계층)은 [I2CP](/docs/specs/i2cp/) 위에서 동작하여 I2P의 메시지 계층 전반에 걸쳐 신뢰할 수 있으면서 순서가 보장되는 전달을 제공하며—IP 위의 TCP와 마찬가지입니다. 대체 전송 프로토콜들이 독립적으로 발전할 수 있도록, 이는 초기 **I2PTunnel** 애플리케이션(BSD 라이선스)에서 원래 분리되었습니다.

핵심 설계 제약 조건:

- TCP에서 차용한 고전적인 2단계(SYN/ACK/FIN) 연결 설정
- **1** 패킷의 고정 윈도우 크기
- 패킷별 ID나 선택적 확인 응답이 없음

이러한 선택은 구현을 단순하게 유지하는 데는 도움이 되었지만 처리량을 제한한다—보통 다음 패킷을 보내기까지 거의 두 RTT(왕복 지연 시간)가 걸린다. 장기간 지속되는 스트림에는 이러한 비용이 감내할 만하지만, HTTP 스타일의 짧은 요청-응답 교환에서는 뚜렷한 성능 저하가 나타난다.

## Streaming Library와의 관계

현재 스트리밍 라이브러리는 동일한 Java 패키지(`net.i2p.client.streaming`)를 그대로 사용합니다. 사용 중단(deprecated)된 클래스와 메서드는 Javadoc 문서에 남아 있으며, 개발자가 ministreaming(이전 경량 스트리밍 구현) 시대의 API를 식별할 수 있도록 명확히 주석으로 표시되어 있습니다. 스트리밍 라이브러리가 ministreaming을 대체했을 때 다음이 추가되었습니다:

- 왕복 횟수를 줄인 더 스마트한 연결 설정
- 적응형 혼잡 윈도우와 재전송 로직
- 패킷 손실이 발생하는 tunnels에서 더 나은 성능

## Ministreaming(경량 스트리밍 라이브러리)은 언제 유용했나요?

제한점에도 불구하고, ministreaming(경량 스트리밍 계층)은 초기 배포에서 신뢰할 수 있는 전송을 제공했다. API는 의도적으로 작고 미래 호환성을 갖추도록 설계되어, 호출자에 영향을 주지 않고 대체 스트리밍 엔진으로 교체할 수 있었다. Java 애플리케이션은 이를 직접 연동했고, Java가 아닌 클라이언트는 스트리밍 세션에 대한 [SAM](/docs/legacy/sam/) 지원을 통해 동일한 기능에 접근했다.

현재는 `ministreaming.jar`를 호환성 레이어로만 취급하십시오. 새로운 개발은 다음을 수행해야 합니다:

1. 전체 스트리밍 라이브러리(Java) 또는 SAM v3(`STREAM` 스타일)을 대상으로 하십시오  
2. 코드를 현대화할 때 남아 있는 fixed-window(고정 윈도우) 가정을 모두 제거하십시오  
3. 지연 시간에 민감한 워크로드의 성능을 향상시키기 위해 더 높은 윈도우 크기와 최적화된 연결 핸드셰이크를 우선 적용하십시오

## 참고

- [스트리밍 라이브러리 문서](/docs/specs/streaming/)
- [스트리밍 Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/client/streaming/package-summary.html) – 사용 중단된 ministreaming 클래스 포함
- [SAM v3 명세](/docs/api/samv3/) – 비-Java 애플리케이션을 위한 스트리밍 지원

여전히 ministreaming(레거시 스트리밍 API)에 의존하는 코드를 발견하면, 최신 스트리밍 API로 포팅할 계획을 세우십시오—네트워크와 그 도구들은 최신 동작을 전제로 합니다.
