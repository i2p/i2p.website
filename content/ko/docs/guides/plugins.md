---
title: "사용자 정의 플러그인 설치"
description: "라우터 플러그인 설치, 업데이트 및 개발"
slug: "plugins"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

I2P의 플러그인 프레임워크를 사용하면 핵심 설치를 건드리지 않고도 router를 확장할 수 있습니다. 사용 가능한 플러그인은 메일, 블로그, IRC, 스토리지, 위키, 모니터링 도구 등을 포함합니다.

> **보안 참고사항:** 플러그인은 라우터와 동일한 권한으로 실행됩니다. 서드파티 다운로드는 서명된 소프트웨어 업데이트를 다루는 것과 동일하게 취급하세요—설치하기 전에 출처를 확인하십시오.

## 1. 플러그인 설치

1. 프로젝트 페이지에서 플러그인의 다운로드 URL을 복사합니다.  
   ![Copy plugin URL](/images/plugins/plugin-step-0.png)
2. router console의 [Plugin Configuration 페이지](http://127.0.0.1:7657/configplugins)를 엽니다.  
   ![Open plugin configuration](/images/plugins/plugin-step-1.png)
3. URL을 설치 필드에 붙여넣고 **Install Plugin**을 클릭합니다.  
   ![Install plugin](/images/plugins/plugin-step-2.png)

라우터는 서명된 아카이브를 가져와서 서명을 검증하고 플러그인을 즉시 활성화합니다. 대부분의 플러그인은 router 재시작 없이 콘솔 링크나 백그라운드 서비스를 추가합니다.

## 2. 플러그인이 중요한 이유

- 최종 사용자를 위한 원클릭 배포—`wrapper.config`나 `clients.config`를 수동으로 편집할 필요 없음
- 대용량 또는 특수 기능을 필요에 따라 제공하면서 핵심 `i2pupdate.su3` 번들을 작게 유지
- 필요시 프로세스 격리를 제공하는 플러그인별 선택적 JVM
- router 버전, Java 런타임, Jetty에 대한 자동 호환성 검사
- router와 동일한 업데이트 메커니즘: 서명된 패키지 및 증분 다운로드
- Console 통합, 언어팩, UI 테마, 비Java 앱(스크립트를 통한) 모두 지원
- `plugins.i2p`와 같은 큐레이션된 "앱 스토어" 디렉토리 지원

## 3. 설치된 플러그인 관리

[I2P Router Plugin](http://127.0.0.1:7657/configclients.jsp#plugin)의 컨트롤을 사용하여:

- 단일 플러그인의 업데이트 확인
- 모든 플러그인을 한 번에 확인 (라우터 업그레이드 후 자동으로 실행됨)
- 클릭 한 번으로 사용 가능한 모든 업데이트 설치  
  ![Update plugins](/images/plugins/plugin-update-0.png)
- 서비스를 등록하는 플러그인의 자동 시작 활성화/비활성화
- 플러그인 완전히 제거

## 4. 자신만의 플러그인 만들기

1. 패키징, 서명 및 메타데이터 요구사항은 [플러그인 명세](/docs/specs/plugin/)를 참고하세요.
2. [`makeplugin.sh`](https://github.com/i2p/i2p.scripts/tree/master/plugin/makeplugin.sh)를 사용하여 기존 바이너리나 웹앱을 설치 가능한 아카이브로 패키징하세요.
3. router가 최초 설치와 증분 업그레이드를 구분할 수 있도록 설치 URL과 업데이트 URL을 모두 게시하세요.
4. 사용자가 진위를 확인할 수 있도록 프로젝트 페이지에 체크섬과 서명 키를 눈에 띄게 제공하세요.

예제를 찾고 계신가요? `plugins.i2p`에서 커뮤니티 플러그인 소스를 둘러보세요 (예를 들어, `snowman` 샘플).

## 5. 알려진 제한사항

- 일반 JAR 파일을 제공하는 플러그인을 업데이트하면 Java 클래스 로더가 클래스를 캐시하기 때문에 router 재시작이 필요할 수 있습니다.
- 플러그인에 활성 프로세스가 없어도 콘솔에 **Stop** 버튼이 표시될 수 있습니다.
- 별도의 JVM에서 실행되는 플러그인은 현재 작업 디렉토리에 `logs/` 디렉토리를 생성합니다.
- 서명자 키가 처음 나타나면 자동으로 신뢰됩니다. 중앙 서명 기관은 없습니다.
- Windows에서는 플러그인 제거 후 빈 디렉토리가 남아 있는 경우가 있습니다.
- Java 5 JVM에서 Java 6 전용 플러그인을 설치하면 Pack200 압축으로 인해 "plugin is corrupt" 오류가 발생합니다.
- 테마 및 번역 플러그인은 대부분 테스트되지 않았습니다.
- 관리되지 않는 플러그인의 자동 시작 플래그가 항상 유지되지는 않습니다.

## 6. 요구사항 및 모범 사례

- 플러그인 지원은 I2P **0.7.12 이상**에서 사용할 수 있습니다.
- 보안 수정 사항을 받으려면 router와 플러그인을 최신 상태로 유지하십시오.
- 사용자가 버전 간 변경 사항을 이해할 수 있도록 간결한 릴리스 노트를 제공하십시오.
- 가능하면 클리어넷 메타데이터 노출을 최소화하기 위해 I2P 내부에서 HTTPS를 통해 플러그인 아카이브를 호스팅하십시오.

## 7. 더 읽을거리

- [플러그인 명세](/docs/specs/plugin/)
- [클라이언트 애플리케이션 프레임워크](/docs/applications/managed-clients/)
- 패키징 유틸리티를 위한 [I2P scripts 저장소](https://github.com/i2p/i2p.scripts/)
