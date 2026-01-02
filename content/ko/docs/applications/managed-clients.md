---
title: "관리형 클라이언트"
description: "라우터 관리 애플리케이션이 ClientAppManager 및 포트 매퍼와 통합되는 방법"
slug: "managed-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. 개요

[`clients.config`](/docs/specs/configuration/#clients-config)의 항목들은 라우터가 시작 시 실행할 애플리케이션을 지정합니다. 각 항목은 **관리형** 클라이언트(권장) 또는 **비관리형** 클라이언트로 실행될 수 있습니다. 관리형 클라이언트는 `ClientAppManager`와 협력하며, 다음을 수행합니다:

- 라우터 콘솔을 위한 애플리케이션을 인스턴스화하고 생명주기 상태를 추적합니다
- 사용자에게 시작/중지 제어를 제공하고 라우터 종료 시 깨끗한 종료를 보장합니다
- 경량 **클라이언트 레지스트리** 및 **포트 매퍼**를 호스팅하여 애플리케이션들이 서로의 서비스를 발견할 수 있도록 합니다

관리되지 않는 클라이언트는 단순히 `main()` 메서드를 호출합니다. 현대화할 수 없는 레거시 코드에만 사용하세요.

## 2. Managed Client 구현

관리형 클라이언트는 `net.i2p.app.ClientApp`(사용자 대면 앱용) 또는 `net.i2p.router.app.RouterApp`(router 확장용) 중 하나를 구현해야 합니다. 관리자가 컨텍스트 및 구성 인수를 제공할 수 있도록 아래 생성자 중 하나를 제공하세요:

```java
public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)
```
```java
public MyRouterApp(RouterContext context, ClientAppManager manager, String[] args)
```
`args` 배열은 `clients.config` 또는 `clients.config.d/`의 개별 파일에 구성된 값을 포함합니다. 가능한 경우 기본 생명주기 연결을 상속받기 위해 `ClientApp` / `RouterApp` 헬퍼 클래스를 확장하세요.

### 2.1 Lifecycle Methods

관리형 클라이언트는 다음을 구현해야 합니다:

- `startup()` - 초기화를 수행하고 즉시 반환합니다. INITIALIZED 상태에서 전환하기 위해 반드시 `manager.notify()`를 최소 한 번 호출해야 합니다.
- `shutdown(String[] args)` - 리소스를 해제하고 백그라운드 스레드를 중지합니다. 상태를 STOPPING 또는 STOPPED로 변경하기 위해 반드시 `manager.notify()`를 최소 한 번 호출해야 합니다.
- `getState()` - 앱이 실행 중인지, 시작 중인지, 중지 중인지, 실패했는지 콘솔에 알립니다

관리자는 사용자가 콘솔과 상호작용할 때 이러한 메서드를 호출합니다.

### 2.2 Advantages

- 라우터 콘솔에서 정확한 상태 보고
- 스레드나 정적 참조 누수 없이 깔끔한 재시작
- 애플리케이션 중지 후 더 낮은 메모리 사용량
- 주입된 컨텍스트를 통한 중앙 집중식 로깅 및 오류 보고

## 3. Unmanaged Clients (Fallback Mode)

설정된 클래스가 managed 인터페이스를 구현하지 않는 경우, 라우터는 `main(String[] args)`를 호출하여 실행하며 결과 프로세스를 추적할 수 없습니다. 콘솔에는 제한된 정보만 표시되고 종료 훅이 실행되지 않을 수 있습니다. 이 모드는 managed API를 채택할 수 없는 스크립트나 일회성 유틸리티용으로 예약하세요.

## 4. Client Registry

관리형 및 비관리형 클라이언트는 매니저에 자신을 등록할 수 있으므로 다른 컴포넌트가 이름으로 참조를 검색할 수 있습니다:

```java
manager.register(this);
```
등록은 클라이언트의 `getName()` 반환 값을 레지스트리 키로 사용합니다. 알려진 등록에는 `console`, `i2ptunnel`, `Jetty`, `outproxy`, `update`가 포함됩니다. `ClientAppManager.getRegisteredApp(String name)`을 사용하여 클라이언트를 검색하고 기능을 조정할 수 있습니다(예: 콘솔이 Jetty에 상태 세부정보를 쿼리하는 경우).

클라이언트 레지스트리와 포트 매퍼는 별도의 시스템입니다. 클라이언트 레지스트리는 이름 조회를 통해 애플리케이션 간 통신을 가능하게 하며, 포트 매퍼는 서비스 검색을 위해 서비스 이름을 host:port 조합에 매핑합니다.

## 3. 비관리형 클라이언트 (폴백 모드)

포트 매퍼는 내부 TCP 서비스를 위한 간단한 디렉터리를 제공합니다. 협력자들이 하드코딩된 주소를 피할 수 있도록 루프백 포트를 등록하세요:

```java
context.portMapper().register(PortMapper.SVC_HTTPS_PROXY, 4445);
```
또는 명시적인 호스트 지정으로:

```java
context.portMapper().register(PortMapper.SVC_HTTP_PROXY, "127.0.0.1", 4444);
```
`PortMapper.getPort(String name)`을 사용하여 서비스를 조회하세요(찾을 수 없으면 -1을 반환) 또는 `getPort(String name, int defaultPort)`를 사용하세요(찾을 수 없으면 기본값을 반환). `isRegistered(String name)`으로 등록 상태를 확인하고 `getActualHost(String name)`으로 등록된 호스트를 가져오세요.

`net.i2p.util.PortMapper`의 일반적인 포트 매퍼 서비스 상수:

- `SVC_CONSOLE` - Router console (기본 포트 7657)
- `SVC_HTTP_PROXY` - HTTP 프록시 (기본 포트 4444)
- `SVC_HTTPS_PROXY` - HTTPS 프록시 (기본 포트 4445)
- `SVC_I2PTUNNEL` - I2PTunnel 관리자
- `SVC_SAM` - SAM bridge (기본 포트 7656)
- `SVC_SAM_SSL` - SAM bridge SSL
- `SVC_SAM_UDP` - SAM UDP
- `SVC_BOB` - BOB bridge (기본 포트 2827)
- `SVC_EEPSITE` - 표준 eepsite (기본 포트 7658)
- `SVC_HTTPS_EEPSITE` - HTTPS eepsite
- `SVC_IRC` - IRC tunnel (기본 포트 6668)
- `SVC_SUSIDNS` - SusiDNS

참고: `httpclient`, `httpsclient`, `httpbidirclient`은 i2ptunnel 터널 타입(`tunnel.N.type` 설정에서 사용됨)이며, 포트 매퍼 서비스 상수가 아닙니다.

## 4. 클라이언트 레지스트리

### 2.1 생명주기 메서드

버전 0.9.42부터 router는 `clients.config.d/` 디렉토리 내의 개별 파일로 설정을 분할하는 것을 지원합니다. 각 파일에는 모든 속성이 `clientApp.0.` 접두사로 시작하는 단일 클라이언트에 대한 속성이 포함됩니다:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
```
이것은 새로운 설치 및 플러그인에 권장되는 방법입니다.

### 2.2 장점

하위 호환성을 위해, 기존 형식은 순차적 번호 매기기를 사용합니다:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.1.main=net.i2p.apps.systray.UrlLauncher
clientApp.1.name=URL Launcher
clientApp.1.delay=5
```
### 6.3 Configuration Properties

**필수:** - `main` - ClientApp 또는 RouterApp을 구현하거나 정적 `main(String[] args)`를 포함하는 전체 클래스 이름

**선택 사항:** - `name` - router console의 표시 이름 (기본값은 클래스 이름) - `args` - 공백 또는 탭으로 구분된 인수 (따옴표로 묶인 문자열 지원) - `delay` - 시작 전 대기 시간(초) (기본값 120) - `onBoot` - true일 경우 `delay=0`으로 강제 설정 - `startOnLoad` - 클라이언트 활성화/비활성화 (기본값 true)

**플러그인 고유:** - `stopargs` - 종료 시 전달되는 인자 - `uninstallargs` - 플러그인 제거 시 전달되는 인자 - `classpath` - 쉼표로 구분된 추가 클래스패스 항목

**플러그인을 위한 변수 치환:** - `$I2P` - I2P 기본 디렉토리 - `$CONFIG` - 사용자 설정 디렉토리 (예: ~/.i2p) - `$PLUGIN` - 플러그인 디렉토리 - `$OS` - 운영 체제 이름 - `$ARCH` - 아키텍처 이름

## 5. 포트 매퍼

- 관리형 클라이언트를 우선 사용하고, 절대적으로 필요한 경우에만 비관리형으로 대체합니다.
- 초기화 및 종료를 가볍게 유지하여 콘솔 작업의 응답성을 유지합니다.
- 진단 도구(및 최종 사용자)가 서비스의 기능을 이해할 수 있도록 설명적인 레지스트리 및 포트 이름을 사용합니다.
- 정적 싱글톤을 피하고, 주입된 컨텍스트와 매니저를 활용하여 리소스를 공유합니다.
- 모든 상태 전환 시 `manager.notify()`를 호출하여 정확한 콘솔 상태를 유지합니다.
- 별도의 JVM에서 실행해야 하는 경우, 로그와 진단 정보가 메인 콘솔에 어떻게 표시되는지 문서화합니다.
- 외부 프로그램의 경우, 관리형 클라이언트의 이점을 얻기 위해 ShellService(버전 1.7.0에 추가)를 사용하는 것을 고려합니다.

## 6. 구성 형식

관리형 클라이언트는 **버전 0.9.4**(2012년 12월 17일)에 도입되었으며, **버전 2.10.0**(2025년 9월 9일) 기준으로 여전히 권장되는 아키텍처입니다. 핵심 API는 이 기간 동안 호환성을 깨뜨리는 변경 없이 안정적으로 유지되어 왔습니다:

- Constructor 시그니처는 변경되지 않음
- 라이프사이클 메서드(startup, shutdown, getState)는 변경되지 않음
- ClientAppManager 등록 메서드는 변경되지 않음
- PortMapper 등록 및 조회 메서드는 변경되지 않음

주요 개선사항: - **0.9.42 (2019)** - 개별 구성 파일을 위한 clients.config.d/ 디렉토리 구조 - **1.7.0 (2021)** - 외부 프로그램 상태 추적을 위한 ShellService 추가 - **2.10.0 (2025)** - 관리형 클라이언트 API 변경 사항 없는 현재 릴리스

다음 주요 릴리스에서는 최소 Java 17+ 버전이 필요합니다 (인프라 요구사항이며, API 변경 사항이 아닙니다).

## References

- [clients.config 명세](/docs/specs/configuration/#clients-config)
- [구성 파일 명세](/docs/specs/configuration/)
- [I2P 기술 문서 색인](/docs/)
- [ClientAppManager Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientAppManager.html) (API 0.9.66)
- [PortMapper Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/util/PortMapper.html) (API 0.9.66)
- [ClientApp 인터페이스](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html) (API 0.9.66)
- [RouterApp 인터페이스](https://i2p.github.io/i2p.i2p/net/i2p/router/app/RouterApp.html) (API 0.9.66)
- [대체 Javadoc (안정 버전)](https://docs.i2p-projekt.de/javadoc/)
- [대체 Javadoc (클리어넷 미러)](https://eyedeekay.github.io/javadoc-i2p/)

> **참고:** I2P 네트워크는 http://idk.i2p/javadoc-i2p/ 에서 포괄적인 문서를 호스팅하고 있으며, 접근하려면 I2P router가 필요합니다. clearnet 접근을 위해서는 위의 GitHub Pages 미러를 사용하세요.
