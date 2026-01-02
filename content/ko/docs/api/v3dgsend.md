---
title: "v3dgsend"
description: "SAM v3를 통해 I2P 데이터그램을 전송하는 CLI 유틸리티"
slug: "v3dgsend"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> 상태: 이 문서는 `v3dgsend` 유틸리티에 대한 간결한 참조 문서입니다. [Datagram API](/docs/api/datagrams/) 및 [SAM v3](/docs/api/samv3/) 문서를 보완합니다.

## 개요

`v3dgsend`는 SAMv3 인터페이스를 사용하여 I2P 데이터그램을 전송하는 명령줄 도우미입니다. 데이터그램 전달 테스트, 서비스 프로토타이핑, 완전한 클라이언트를 작성하지 않고 종단 간 동작을 검증하는 데 유용합니다.

일반적인 사용 사례:

- Destination에 대한 데이터그램 도달 가능성 스모크 테스트
- 방화벽 및 주소록 구성 검증
- 원시(raw) 데이터그램과 서명된(응답 가능한) 데이터그램 실험

## 사용법

기본 실행 방법은 플랫폼과 패키징 방식에 따라 다릅니다. 일반적인 옵션은 다음과 같습니다:

- Destination: base64 Destination 또는 `.i2p` 이름
- Protocol: raw (PROTOCOL 18) 또는 signed (PROTOCOL 17)
- Payload: 인라인 문자열 또는 파일 입력

정확한 플래그는 배포판의 패키징 또는 `--help` 출력을 참조하세요.

## 참고 자료

- [Datagram API](/docs/api/datagrams/)
- [SAM v3](/docs/api/samv3/)
- [Streaming Library](/docs/api/streaming/) (datagram의 대안)
