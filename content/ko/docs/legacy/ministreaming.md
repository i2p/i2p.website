---
title: "Ministreaming 라이브러리"
description: "I2P의 첫 번째 TCP 유사 전송 계층에 대한 역사적 기록"
slug: "ministreaming"
aliases:
  - "/ko/ministreaming"
  - "/ko/ministreaming/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

## 참고

ministreaming 라이브러리는 "전체" [streaming library](/docs/api/streaming)에 의해 향상되고 확장되었습니다. Ministreaming은 더 이상 사용되지 않으며 오늘날의 애플리케이션과 호환되지 않습니다. 다음 문서는 오래된 것입니다. 또한 streaming이 동일한 Java 패키지(net.i2p.client.streaming)에서 ministreaming을 확장한다는 점에 유의하세요. 따라서 현재 API 문서에는 둘 다 포함되어 있습니다. 더 이상 사용되지 않는 ministreaming 클래스와 메소드는 Javadocs에서 deprecated로 명확히 표시되어 있습니다.

## Ministreaming 라이브러리

ministreaming 라이브러리는 코어 [I2CP](/docs/protocol/i2cp) 위에 구축된 계층으로, 신뢰할 수 없고 순서가 보장되지 않으며 인증되지 않은 메시지 계층 위에서 신뢰할 수 있고 순서가 보장되며 인증된 메시지 스트림이 동작할 수 있도록 합니다. TCP와 IP의 관계와 마찬가지로, 이 스트리밍 기능은 다양한 트레이드오프와 최적화 옵션을 제공하지만, 이러한 기능을 기본 I2P 코드에 포함시키는 대신 별도의 라이브러리로 분리하여 TCP와 유사한 복잡성을 분리하고 대안적인 최적화된 구현을 가능하게 했습니다.

ministreaming 라이브러리는 mihi가 그의 [I2PTunnel](/docs/api/i2ptunnel) 애플리케이션의 일부로 작성한 후 분리되어 BSD 라이선스 하에 릴리스되었습니다. 이것이 "mini"streaming 라이브러리라고 불리는 이유는 구현에서 일부 단순화를 했기 때문이며, 더 견고한 streaming 라이브러리는 I2P 상에서 동작하도록 더욱 최적화될 수 있습니다. ministreaming 라이브러리의 두 가지 주요 문제점은 기존의 TCP 2단계 연결 설정 프로토콜의 사용과 현재 고정된 윈도우 크기 1입니다. 연결 설정 문제는 장기간 유지되는 스트림에서는 사소하지만, 빠른 HTTP 요청과 같은 단기간 스트림에서는 상당한 영향을 미칠 수 있습니다. 윈도우 크기의 경우, ministreaming 라이브러리는 전송되는 메시지 내에서 어떤 ID나 순서도 유지하지 않으며(또는 애플리케이션 레벨 ACK나 SACK를 포함하지 않음), 따라서 다른 메시지를 보내기 전에 평균적으로 메시지를 보내는 데 걸리는 시간의 두 배를 기다려야 합니다.

이러한 문제들에도 불구하고, ministreaming 라이브러리는 많은 상황에서 상당히 좋은 성능을 보이며, 그 API는 매우 간단하면서도 다른 스트리밍 구현이 도입되어도 변경되지 않고 유지될 수 있는 능력을 갖추고 있습니다. 이 라이브러리는 자체 ministreaming.jar로 배포됩니다. Java 개발자들은 API에 직접 접근할 수 있으며, 다른 언어의 개발자들은 [SAM](/docs/api/samv3)의 스트리밍 지원을 통해 사용할 수 있습니다.
