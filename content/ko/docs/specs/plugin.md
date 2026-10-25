---
title: "플러그인 명세"
description: "I2P 플러그인을 위한 .xpi2p / .su3 패키징 규칙"
slug: "plugin"
aliases:
  - "/ko/plugin_spec"
  - "/ko/plugin_spec/"
lastUpdated: "2022-01"
accurateFor: "0.9.53"
type: docs
---

## 개요

이 문서는 .xpi2p 파일 형식을 명시합니다 (Firefox .xpi와 유사하지만, XML install.rdf 파일 대신 간단한 plugin.config 설명 파일을 사용). 이 파일 형식은 초기 플러그인 설치와 플러그인 업데이트 모두에 사용됩니다.

또한 이 문서는 router가 플러그인을 설치하는 방법과 플러그인 개발자를 위한 정책 및 가이드라인에 대한 간략한 개요를 제공합니다.

기본적인 .xpi2p 파일 형식은 i2pupdate.sud 파일(router 업데이트에 사용되는 형식)과 동일하지만, 설치 프로그램은 서명자의 키를 아직 알지 못하더라도 사용자가 애드온을 설치할 수 있도록 허용합니다.

릴리스 0.9.15부터 SU3 파일 형식이 지원되며 이것이 선호됩니다. 이 형식은 더 강력한 서명 키를 가능하게 합니다.

> **참고:** 더 이상 xpi2p 형식으로 플러그인을 배포하는 것을 권장하지 않습니다. su3 형식을 사용하세요.

표준 디렉토리 구조를 통해 사용자는 다음과 같은 유형의 애드온을 설치할 수 있습니다:

- Console webapp
- cgi-bin, webapp이 있는 새로운 eepsite
- Console 테마
- Console 번역
- Java 프로그램
- 별도 JVM의 Java 프로그램
- 모든 셸 스크립트 또는 프로그램

플러그인은 모든 파일을 `~/.i2p/plugins/name/`(Windows에서는 `%APPDIR%\I2P\plugins\name\`)에 설치합니다. 설치 프로그램은 다른 곳에 설치하는 것을 방지하지만, 플러그인은 실행 중에 다른 곳에 있는 라이브러리에 액세스할 수 있습니다.

이는 설치, 제거, 업그레이드를 더 쉽게 만들고 기본적인 플러그인 간 충돌을 줄이는 방법으로만 보아야 합니다.

그러나 플러그인이 실행되고 나면 본질적으로 보안 모델이 존재하지 않습니다. 플러그인은 router와 동일한 JVM에서 실행되고 동일한 권한을 가지며, 파일 시스템, router, 외부 프로그램 실행 등에 대한 모든 접근 권한을 갖습니다.

## 세부사항

foo.xpi2p는 다음을 포함하는 서명된 업데이트(sud) 파일입니다:

zip 파일에 앞서 추가되는 표준 .sud 헤더로, 다음을 포함합니다:

```text
40-byte DSA signature
16-byte plugin version in UTF-8, padded with trailing zeroes if necessary
```
다음을 포함하는 Zip 파일:

### plugin.config 파일

이 파일은 필수입니다. 다음 속성들을 포함하는 표준 I2P 설정 파일입니다:

#### 필수 속성

다음 네 가지는 필수 속성입니다. 처음 세 개는 업데이트 플러그인의 경우 설치된 플러그인의 속성과 동일해야 합니다.

-   **name** - 이 디렉토리 이름으로 설치됩니다. 네이티브 플러그인의 경우, 서로 다른 패키지에서 별도의 이름을 원할 수 있습니다 - 예를 들어 foo-windows와 foo-linux.
-   **key** - '='로 끝나는 172 B64 문자의 DSA 공개 키입니다. SU3 형식의 경우 생략하세요.
-   **signer** - yourname@mail.i2p를 권장합니다
-   **version** - VersionComparator가 파싱할 수 있는 형식이어야 합니다. 예: 1.2.3-4. 최대 16바이트 (sud 버전과 일치해야 함). 유효한 숫자 구분자는 '.', '-', '_'입니다. 업데이트 플러그인의 경우 설치된 플러그인보다 높은 버전이어야 합니다.

#### 표시 속성

다음 속성들의 값은 router console의 /configplugins에서 존재할 경우 표시됩니다:

-   **date** - Java time - long int
-   **author** - `yourname@mail.i2p` 권장
-   **websiteURL** - `http://foo.i2p/`
-   **updateURL** - `http://foo.i2p/foo.xpi2p` - 업데이트 확인기가 이 URL의 41-56바이트를 확인하여 새로운 버전이 사용 가능한지 판단합니다. 1.7.0(0.9.53)부터 URL에서 `$OS`와 `$ARCH` 변수를 사용할 수 있습니다. 권장하지 않습니다. 이전에 xpi2p 형식으로 플러그인을 배포한 경우가 아니면 사용하지 마세요.
-   **updateURL.su3** - `http://foo.i2p/foo.su3` - 0.9.15부터 su3 형식 업데이트 파일의 위치입니다. 1.7.0(0.9.53)부터 URL에서 `$OS`와 `$ARCH` 변수를 사용할 수 있습니다.
-   **description** - 영어로 작성
-   **description_xx** - xx 언어용
-   **license** - 플러그인 라이선스
-   **disableStop=true** - 기본값은 false입니다. true인 경우 중지 버튼이 표시되지 않습니다. 웹앱이 없고 stopargs가 있는 클라이언트가 없는 경우에 사용하세요.

#### 콘솔 요약 바 링크 속성

다음 속성들은 콘솔 요약 표시줄에 링크를 추가하는 데 사용됩니다:

-   **consoleLinkName** - 요약 바에 추가됩니다
-   **consoleLinkName_xx** - 언어 xx용
-   **consoleLinkURL** - /appname/index.jsp
-   **consoleLinkTooltip** - 0.7.12-6부터 지원됨
-   **consoleLinkTooltip_xx** - 0.7.12-6부터 언어 xx 지원됨

#### 콘솔 아이콘 속성

콘솔에 사용자 정의 아이콘을 추가하기 위해 다음과 같은 선택적 속성들을 사용할 수 있습니다:

-   **console-icon** - 0.9.20부터 지원됩니다. webapp 전용입니다. 32x32 이미지의 경로입니다(예: /icon.png). 1.7.0(API 0.9.53)부터는 consoleLinkURL이 지정된 경우 해당 URL을 기준으로 한 상대 경로이고, 그렇지 않으면 webapp 이름을 기준으로 한 상대 경로입니다. 플러그인의 모든 webapp에 적용됩니다.
-   **icon-code** - 0.9.25부터 지원됩니다. 웹 리소스가 없는 플러그인에 console 아이콘을 제공합니다. 32x32 png 이미지 파일에 대해 `net.i2p.data.Base64 encode FILE`을 호출하여 생성된 B64 문자열입니다.

#### 설치 프로그램 속성

다음 속성들이 플러그인 설치 프로그램에서 사용됩니다:

-   **type** - app/theme/locale/webapp/... (구현되지 않음, 아마 필요하지 않을 것)
-   **min-i2p-version** - 이 플러그인이 요구하는 I2P의 최소 버전
-   **max-i2p-version** - 이 플러그인이 실행될 수 있는 I2P의 최대 버전
-   **min-java-version** - 이 플러그인이 요구하는 Java의 최소 버전
-   **min-jetty-version** - 0.8.13부터 지원, Jetty 6 webapp의 경우 6 사용
-   **max-jetty-version** - 0.8.13부터 지원, Jetty 5 webapp의 경우 5.99999 사용
-   **required-platform-OS** - 구현되지 않음 - 검증되지 않고 표시만 될 예정
-   **other-requirements** - 구현되지 않음, 예: python x.y - 설치 프로그램에서 검증되지 않고 사용자에게만 표시됨
-   **dont-start-at-install=true** - 기본값 false. 플러그인이 설치되거나 업데이트될 때 시작하지 않음.
-   **router-restart-required=true** - 기본값 false. 업데이트 시 router나 플러그인을 재시작하지 않고, 재시작이 필요하다는 것을 사용자에게 알리기만 함.
-   **update-only=true** - 기본값 false. true인 경우, 설치가 존재하지 않으면 실패함.
-   **install-only=true** - 기본값 false. true인 경우, 설치가 존재하면 실패함.
-   **min-installed-version** - 설치가 존재하는 경우 업데이트할 최소 설치 버전
-   **max-installed-version** - 설치가 존재하는 경우 업데이트할 최대 설치 버전
-   **depends=plugin1,plugin2,plugin3** - 구현되지 않음
-   **depends-version=0.3.4,,5.6.7** - 구현되지 않음

#### 번역 속성

-   **langs=xx,yy,Klingon,...** - (구현되지 않음) (yy는 국가 플래그)

### 애플리케이션 디렉터리 및 파일

다음 디렉터리 또는 파일들은 각각 선택사항이지만, 무언가는 있어야 하며 그렇지 않으면 아무것도 실행되지 않습니다:

**console/**

-   **locale/** - 기본 I2P 설치의 앱들을 위한 새로운 리소스 번들(번역)만 포함하는 jar 파일들. 이 플러그인을 위한 번들들은 console/webapp/foo.war 또는 lib/foo.jar 내부에 위치해야 합니다
-   **themes/** - router console을 위한 새로운 테마들. 각 테마를 하위 디렉토리에 배치하세요.
-   **webapps/** - (webapps에 대한 아래 중요한 참고사항 참조) .war 파일들 - webapps.config에서 비활성화되지 않는 한 설치 시 실행됩니다. war 이름은 플러그인 이름과 동일할 필요가 없습니다. 기본 I2P 설치에서 war 이름을 중복하지 마세요.
-   **webapps.config** - router의 webapps.config와 동일한 형식. webapp classpath를 위해 $PLUGIN/lib/ 또는 $I2P/lib의 추가 jar들을 지정하는 데도 사용되며, `webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar` 형식으로 지정합니다

> **참고:** 릴리스 1.7.0 (API 0.9.53) 이전에는 warname이 플러그인 이름과 동일한 경우에만 classpath 라인이 로드되었습니다. API 0.9.53부터는 모든 warname에 대해 classpath 설정이 작동합니다.

> **참고:** router 버전 0.7.12-9 이전에는 router가 `webapps.warname.startOnLoad` 대신 `plugin.warname.startOnLoad`를 찾았습니다. 이전 router 버전과의 호환성을 위해 war를 비활성화하려는 플러그인은 두 줄 모두 포함해야 합니다.

**eepsite/**

(eepsite에 대한 아래의 중요한 참고사항을 확인하세요)

-   **cgi-bin/**
-   **docroot/**
-   **logs/**
-   **webapps/**
-   **jetty.xml** - 설치 프로그램은 경로를 설정하기 위해 여기서 변수 치환을 수행해야 합니다. 이 파일의 위치와 이름은 clients.config에서 설정되어 있는 한 실제로는 중요하지 않습니다 - 여기에서 한 단계 위 레벨에 있는 것이 더 편리할 수 있습니다.

**lib/**

여기에 jar 파일을 넣고, console/webapps.config 및/또는 clients.config의 classpath 줄에서 지정하세요

### clients.config 파일

이 파일은 선택사항이며, 플러그인이 시작될 때 실행될 클라이언트들을 지정합니다. router의 clients.config 파일과 동일한 형식을 사용합니다. 형식에 대한 자세한 정보와 클라이언트가 시작되고 중지되는 방법에 대한 중요한 세부사항은 clients.config 구성 파일 사양을 참조하세요.

-   **clientApp.0.stopargs=foo bar stop baz** - 존재하는 경우, 클라이언트를 중지하기 위해 이 인수들과 함께 클래스가 호출됩니다. 모든 중지 작업은 지연 없이 호출됩니다. 참고: router는 관리되지 않는 클라이언트가 실행 중인지 여부를 알 수 없습니다.
-   **clientApp.0.uninstallargs=foo bar uninstall baz** - 존재하는 경우, $PLUGIN을 삭제하기 직전에 이 인수들과 함께 클래스가 호출됩니다. 모든 제거 작업은 지연 없이 호출됩니다.
-   **clientApp.0.classpath=$I2P/lib/foo.bar,$PLUGIN/lib/bar.jar** - 플러그인 실행기는 args와 stopargs 행에서 다음과 같이 변수 치환을 수행합니다:
    -   `$I2P` - I2P 기본 설치 디렉토리
    -   `$CONFIG` - I2P 설정 디렉토리 (일반적으로 ~/.i2p)
    -   `$PLUGIN` - 이 플러그인의 설치 디렉토리 (일반적으로 ~/.i2p/plugins/appname)
    -   `$OS` - `windows`, `linux`, `mac` 형태의 호스트 운영체제
    -   `$ARCH` - `386`, `amd64`, `arm64` 형태의 호스트 아키텍처

(셸 스크립트나 외부 프로그램 실행에 대한 중요한 참고사항은 아래를 참조하세요)

## 플러그인 설치 프로그램 작업

이것은 I2P에 의해 플러그인이 설치될 때 발생하는 일들을 나열합니다.

1.  .xpi2p 파일이 다운로드됩니다.
2.  .sud 서명이 저장된 키와 대조하여 검증됩니다. 릴리스 0.9.14.1부터는 일치하는 키가 없으면 모든 키를 허용하는 고급 router 속성이 설정되지 않는 한 설치가 실패합니다.
3.  zip 파일의 무결성을 검증합니다.
4.  plugin.config 파일을 추출합니다.
5.  플러그인이 작동할지 확인하기 위해 I2P 버전을 검증합니다.
6.  웹앱이 기존 $I2P 애플리케이션과 중복되지 않는지 확인합니다.
7.  기존 플러그인을 중지합니다(있는 경우).
8.  update=false인 경우 설치 디렉터리가 아직 존재하지 않는지 확인하거나 덮어쓸지 묻습니다.
9.  update=true인 경우 설치 디렉터리가 존재하는지 확인하거나 생성할지 묻습니다.
10. 플러그인을 appDir/plugins/name/에 압축 해제합니다.
11. plugins.config에 플러그인을 추가합니다.

## 플러그인 시작 작업

이것은 플러그인이 시작될 때 발생하는 일들을 나열합니다. 먼저 plugins.config를 확인하여 어떤 플러그인이 시작되어야 하는지 확인합니다. 각 플러그인에 대해:

1.  clients.config를 확인하고, 각 항목을 로드하여 시작합니다 (구성된 jar들을 classpath에 추가).
2.  console/webapp과 console/webapp.config를 확인합니다. 필요한 항목들을 로드하여 시작합니다 (구성된 jar들을 classpath에 추가).
3.  console/locale/foo.jar가 있으면 번역 classpath에 추가합니다.
4.  console/theme이 있으면 테마 검색 경로에 추가합니다.
5.  요약 표시줄 링크를 추가합니다.

## Console Webapp 참고사항

백그라운드 작업이 있는 콘솔 웹앱은 ServletContextListener를 구현하거나(예시는 seedless 또는 i2pbote 참조) servlet에서 destroy()를 오버라이드하여 중지할 수 있도록 해야 합니다. router 버전 0.7.12-3부터는 콘솔 웹앱이 재시작되기 전에 항상 중지되므로, 이렇게 구현하는 한 여러 인스턴스에 대해 걱정할 필요가 없습니다. 또한 router 버전 0.7.12-3부터는 router 종료 시 콘솔 웹앱도 중지됩니다.

웹앱에 라이브러리 jar를 번들로 포함하지 마세요. lib/에 넣고 webapps.config에 classpath를 설정하세요. 그러면 별도의 설치 및 업데이트 플러그인을 만들 수 있으며, 업데이트 플러그인에는 라이브러리 jar가 포함되지 않습니다.

Jetty, Tomcat 또는 servlet jar를 플러그인에 번들로 포함하지 마세요. 이들이 I2P 설치 버전과 충돌할 수 있습니다. 충돌하는 라이브러리를 번들로 포함하지 않도록 주의하세요.

.java나 .jsp 파일은 포함하지 마세요. 그렇지 않으면 Jetty가 설치 시 이들을 재컴파일하게 되어 시작 시간이 늘어납니다. 대부분의 I2P 설치에는 classpath에 작동하는 Java와 JSP 컴파일러가 있지만, 이것이 보장되는 것은 아니며 모든 경우에 작동하지 않을 수 있습니다.

현재로서는 $PLUGIN에서 classpath 파일을 추가해야 하는 webapp은 플러그인과 동일한 이름이어야 합니다. 예를 들어, foo 플러그인의 webapp은 foo.war로 명명되어야 합니다.

I2P는 I2P 릴리스 0.9.30부터 Servlet 3.0을 지원하지만, @WebContent에 대한 어노테이션 스캐닝은 지원하지 않습니다 (web.xml 파일 없음). 여러 추가 런타임 jar 파일이 필요하지만, 표준 설치에서는 이를 제공하지 않습니다. @WebContent 지원이 필요하시면 I2P 개발자에게 문의하세요.

## Eepsite 참고사항

플러그인을 기존 eepsite에 설치하는 방법이 명확하지 않습니다. router는 eepsite에 대한 연결점이 없으며, eepsite가 실행 중일 수도 있고 아닐 수도 있으며, 여러 개가 있을 수도 있습니다. 더 나은 방법은 완전히 새로운 eepsite를 위해 자신만의 Jetty 인스턴스와 I2PTunnel 인스턴스를 시작하는 것입니다.

새로운 I2PTunnel을 인스턴스화할 수 있습니다(i2ptunnel CLI가 하는 것과 어느 정도 유사함). 하지만 당연히 i2ptunnel GUI에는 나타나지 않을 것입니다. 그것은 다른 인스턴스이기 때문입니다. 하지만 그래도 괜찮습니다. 그러면 i2ptunnel과 jetty를 함께 시작하고 중지할 수 있습니다.

따라서 router가 기존 eepsite와 자동으로 병합할 것을 기대하지 마세요. 그런 일은 아마 일어나지 않을 것입니다. clients.config에서 새로운 I2PTunnel과 Jetty를 시작하세요. 이에 대한 가장 좋은 예시는 zzzot과 pebble 플러그인입니다.

jetty.xml에 경로 치환을 어떻게 적용하나요? 예시는 zzzot과 pebble 플러그인을 참조하세요.

## 클라이언트 시작/중지 참고사항

릴리스 0.9.4부터 router는 "관리형" 플러그인 클라이언트를 지원합니다. 관리형 플러그인 클라이언트는 `ClientAppManager`에 의해 인스턴스화되고 시작됩니다. ClientAppManager는 클라이언트에 대한 참조를 유지하고 클라이언트 상태에 대한 업데이트를 받습니다. 관리형 플러그인 클라이언트가 선호되는데, 상태 추적을 구현하고 클라이언트를 시작 및 중지하기가 훨씬 쉽기 때문입니다. 또한 클라이언트가 중지된 후 과도한 메모리 사용으로 이어질 수 있는 클라이언트 코드의 정적 참조를 피하기가 훨씬 쉽습니다. 관리형 클라이언트 작성에 대한 자세한 정보는 clients.config 구성 파일 명세를 참조하세요.

"관리되지 않는" plugin 클라이언트의 경우, router는 clients.config를 통해 시작된 클라이언트의 상태를 모니터링할 방법이 없습니다. plugin 작성자는 가능한 한 정적 상태 테이블을 유지하거나 PID 파일을 사용하는 등의 방법으로 여러 번의 시작 또는 중지 호출을 우아하게 처리해야 합니다. 여러 번의 시작이나 중지 시 로깅이나 예외를 피하세요. 이는 이전 시작 없이 중지 호출이 있는 경우에도 마찬가지입니다. router 버전 0.7.12-3부터 plugin은 router 종료 시 중지되며, 이는 clients.config에 stopargs가 있는 모든 클라이언트가 이전에 시작되었는지 여부와 관계없이 호출된다는 의미입니다.

## 셸 스크립트 및 외부 프로그램 참고사항

셸 스크립트나 다른 외부 프로그램을 실행하려면, OS 타입을 확인한 후 제공된 .bat 또는 .sh 파일에서 ShellCommand를 실행하는 작은 Java 클래스를 작성하세요. 이에 대한 일반화된 솔루션이 I2P 1.7.0/0.9.53에서 추가되었습니다. 단일 명령에 대한 상태 추적을 수행하고 ClientAppManager와 통신하는 "ShellService"입니다.

외부 프로그램은 router가 중지될 때 함께 중지되지 않으며, router가 시작될 때 두 번째 복사본이 실행됩니다. 이는 일반적으로 ShellService를 사용하여 상태 추적을 수행함으로써 완화할 수 있습니다. 해당 방법이 사용 사례에 적합하지 않다면, PID 파일에 PID를 저장하고 시작 시 확인하는 일반적인 작업을 수행하는 래퍼 클래스나 셸 스크립트를 작성할 수 있습니다.

## 기타 플러그인 가이드라인

-   키 생성, plugin su3 파일 생성 및 검증을 위한 makeplugin.sh 쉘 스크립트는 i2p.scripts monotone 브랜치나 zzz 페이지의 샘플 plugin을 참고하세요. 이는 대부분의 작업을 자동화합니다. 이 스크립트를 plugin 빌드 프로세스에 통합해야 합니다.
-   jar 및 war의 Pack200 사용이 plugin에 강력히 권장되며, 일반적으로 plugin 크기를 60-65% 압축합니다. 예제는 zzz 페이지의 샘플 plugin을 참조하세요. Pack200 압축 해제는 router 0.7.11-5 이상에서 지원되며, 이는 plugin을 지원하는 모든 router입니다.
-   Plugin은 $I2P가 읽기 전용일 수 있고 좋은 정책이 아니므로 $I2P의 어느 곳에도 쓰기를 시도해서는 안 됩니다.
-   Plugin은 $CONFIG에 쓸 수 있지만 $PLUGIN에만 파일을 유지하는 것이 권장됩니다. $PLUGIN의 모든 파일은 제거 시 삭제됩니다.
-   $CWD는 어디든 될 수 있으므로 특정 위치에 있다고 가정하지 말고, $CWD를 기준으로 파일을 읽거나 쓰려고 시도하지 마세요. ShellService의 경우 항상 $PLUGIN과 동일합니다.
-   Java 프로그램은 I2PAppContext의 디렉토리 getter를 사용하여 자신의 위치를 찾아야 합니다.
-   Plugin 디렉토리는 `I2PAppContext.getGlobalContext().getAppDir().getAbsolutePath() + "/plugins/" + appname`이거나 clients.config의 args 행에 $PLUGIN 인수를 넣으세요.
-   모든 설정 파일은 UTF-8이어야 합니다.
-   별도의 JVM에서 실행하려면 `java -cp foo:bar:baz my.main.class arg1 arg2 arg3`과 함께 ShellCommand를 사용하세요.
-   clients.config의 stopargs 대신, Java 클라이언트는 `I2PAppContext.addShutdownTask()`로 종료 hook을 등록할 수 있습니다. 하지만 이는 업그레이드 시 plugin을 종료하지 않으므로 stopargs가 권장됩니다. 또한 생성된 모든 스레드를 데몬 모드로 설정하세요.
-   표준 설치에 있는 클래스를 중복으로 포함하지 마세요. 필요시 클래스를 확장하세요.
-   구 설치와 신 설치 간의 wrapper.config의 다른 classpath 정의에 주의하세요.
-   클라이언트는 다른 keyname을 가진 중복 키, 다른 키를 가진 중복 keyname, 업그레이드 패키지의 다른 키나 keyname을 거부합니다. 키를 보호하세요. 한 번만 생성하세요.
-   업그레이드 시 덮어써지므로 런타임에 plugin.config 파일을 수정하지 마세요. 런타임 설정 저장을 위해 디렉토리의 다른 설정 파일을 사용하세요.
-   일반적으로 plugin은 $I2P/lib/router.jar에 접근할 필요가 없습니다. 특별한 작업을 하지 않는 한 router 클래스에 접근하지 마세요.
-   각 버전은 이전 버전보다 높아야 하므로, 버전 끝에 빌드 번호를 추가하도록 빌드 스크립트를 개선할 수 있습니다.
-   Plugin은 절대 `System.exit()`를 호출해서는 안 됩니다.
-   번들하는 소프트웨어의 라이선스 요구사항을 충족하여 라이선스를 존중해 주세요.
-   Router는 JVM 시간대를 UTC로 설정합니다. Plugin이 사용자의 실제 시간대를 알아야 할 경우, router가 I2PAppContext 속성 `i2p.systemTimeZone`에 저장합니다.

## 클래스패스

$I2P/lib에 있는 다음 jar 파일들은 원래 설치가 얼마나 오래되었거나 새로운지에 관계없이 모든 I2P 설치에서 표준 classpath에 있다고 가정할 수 있습니다.

i2p jar의 모든 최신 공개 API는 Javadocs에 since-release 번호가 명시되어 있습니다. 플러그인이 최신 버전에서만 사용 가능한 특정 기능을 필요로 하는 경우, plugin.config 파일에서 min-i2p-version, min-jetty-version 또는 둘 다의 속성을 설정해야 합니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">addressbook.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription and blockfile support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need; use the NamingService interface</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-logging.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Apache Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since release 0.9.30</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-el.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSP Expressions Language</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with JSPs that use EL. As of release 0.9.30 (Jetty 9), this contains the EL 3.0 API.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with HTTP or other servers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-compiler.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">nothing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since Jetty 6 (release 0.9)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-runtime.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper Compiler and Runtime, and some Tomcat utils</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">javax.servlet.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs. As of release 0.9.30 (Jetty 9), this contains the Servlet 3.1 and JSP 2.3 APIs.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jbigi.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Binaries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jetty-i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Support utilities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Some plugins will need. As of release 0.9.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">mstreaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">org.mortbay.jetty.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty Base</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins starting their own Jetty instance will need. Recommended way of starting Jetty is with <code>net.i2p.jetty.JettyStart</code> in jetty-i2p.jar.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins using router context will need; most will not</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">routerconsole.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need, not a public API</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">sam.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">streaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming Implementation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">URL Launcher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins should not need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray4j.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Systray</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need. As of 0.9.26, no longer present.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">wrapper.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
  </tbody>
</table>
$I2P/lib에 있는 다음 jar 파일들은 원래 설치가 얼마나 오래되었거나 새로운지에 관계없이 모든 I2P 설치에 존재한다고 가정할 수 있지만, 반드시 classpath에 포함되어 있는 것은 아닙니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jstl.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">standard.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
  </tbody>
</table>
위에 나열되지 않은 항목들은 당신의 i2p 버전에 classpath가 있더라도 모든 사람의 classpath에 존재하지 않을 수 있습니다. 위에 나열되지 않은 jar가 필요한 경우, 플러그인의 clients.config 또는 webapps.config에 지정된 classpath에 $I2P/lib/foo.jar을 추가하세요.

이전에는 clients.config에서 지정된 classpath 항목이 전체 JVM의 classpath에 추가되었습니다. 그러나 0.7.13-3부터 class loader를 사용하여 이 문제가 수정되었고, 이제 원래 의도대로 clients.config에서 지정된 classpath는 특정 스레드에만 적용됩니다. 따라서 각 클라이언트에 대해 필요한 전체 classpath를 지정하십시오.

## Java 버전 참고사항

I2P는 0.9.24 릴리스(2016년 1월)부터 Java 7을 요구합니다. I2P는 0.9.12 릴리스(2014년 4월)부터 Java 6을 요구했습니다. 최신 릴리스를 사용하는 모든 I2P 사용자는 1.7 (7.0) JVM을 실행해야 합니다.

플러그인이 **1.7을 필요로 하지 않는 경우**:

-   모든 java 및 jsp 파일이 source="1.6" target="1.6"으로 컴파일되도록 확인하세요.
-   번들된 모든 라이브러리 jar들도 1.6 이하 버전용인지 확인하세요.

플러그인이 **1.7이 필요한** 경우:

-   다운로드 페이지에 이를 명시하세요.
-   plugin.config에 min-java-version=1.7을 추가하세요

어떤 경우든 Java 8로 컴파일할 때는 런타임 크래시를 방지하기 위해 bootclasspath를 **반드시** 설정해야 합니다.

## 업데이트 시 JVM 크래시

참고 - 이제 모든 문제가 해결되었습니다.

JVM은 I2P가 시작된 이후 플러그인이 실행되고 있었던 경우(나중에 플러그인이 중지되었더라도) 해당 플러그인의 jar 파일을 업데이트할 때 충돌하는 경향이 있습니다. 이는 0.7.13-3 버전의 클래스 로더 구현으로 수정되었을 수 있지만, 확실하지는 않습니다.

가장 안전한 방법은 플러그인을 war 내부에 jar가 포함되도록 설계하거나(웹앱의 경우), 업데이트 후 재시작을 요구하거나, 플러그인의 jar를 업데이트하지 않는 것입니다.

웹앱 내부에서 클래스 로더가 작동하는 방식으로 인해, webapps.config에서 classpath를 지정하면 외부 jar 파일을 사용하는 것이 안전할 _수도_ 있습니다. 이를 확인하려면 더 많은 테스트가 필요합니다. 웹앱에만 필요한 경우 clients.config에서 '가짜' 클라이언트로 classpath를 지정하지 말고 대신 webapps.config를 사용하세요.

가장 안전하지 않고, 대부분의 충돌의 원인으로 보이는 것은 clients.config의 classpath에 플러그인 jar가 지정된 클라이언트들입니다.

이 모든 것들은 초기 설치 시에는 문제가 되지 않아야 합니다 - 플러그인의 초기 설치 시에는 재시작이 필요하지 않아야 합니다.

## 참고 자료

-   [구성 파일 사양](/docs/specs/configuration)
-   [DSA 암호화](/docs/specs/cryptography#DSA)
-   [업데이트 사양](/docs/specs/updates)
