---
title: "Router 설정"
description: "I2P routers 및 클라이언트를 위한 구성 옵션과 형식"
slug: "configuration"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## 개요

이 문서는 router와 다양한 애플리케이션에서 사용되는 I2P 구성 파일에 대한 포괄적인 기술 사양을 제공합니다. 또한 파일 형식 사양, 속성 정의, 그리고 I2P 소스 코드와 공식 문서를 대조하여 검증된 구현 세부사항을 다룹니다.

### 범위

- router 구성 파일 및 형식
- 클라이언트 애플리케이션 구성
- I2PTunnel tunnel 구성
- 파일 형식 사양 및 구현
- 버전별 기능 및 사용 중단 항목

### 구현 참고 사항

구성 파일은 I2P 코어 라이브러리의 `DataHelper.loadProps()` 및 `storeProps()` 메서드를 사용하여 읽고 저장됩니다. 파일 형식은 I2P 프로토콜에서 사용하는 직렬화 형식과 상당히 다릅니다(자세한 내용은 [공통 구조 사양 - 타입 매핑](/docs/specs/common-structures/#type-mapping)을 참조하세요).

---

## 일반 구성 파일 형식

I2P 구성 파일은 특정 예외와 제약이 적용된 수정된 Java Properties 형식을 따릅니다.

### 형식 사양

[Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)에 기반하되, 다음과 같은 중대한 차이가 있습니다:

#### 인코딩

- **반드시** UTF-8 인코딩을 사용해야 합니다 (표준 Java Properties에서 사용하는 ISO-8859-1이 아님)
- 구현: 모든 파일 작업에 `DataHelper.getUTF8()` 유틸리티를 사용합니다

#### 이스케이프 시퀀스

- 이스케이프 시퀀스는 **인식되지 않습니다**(백슬래시 `\` 포함)
- 줄 연속(line continuation)은 **지원되지 않습니다**
- 백슬래시 문자는 리터럴로 취급됩니다

#### 주석 문자

- `#`는 줄의 어느 위치에서든 주석을 시작합니다
- `;`는 **오직** 1열에 있을 때에만 주석을 시작합니다
- `!`는 주석을 시작하지 **않습니다** (Java Properties와 다릅니다)

#### 키-값 구분자

- `=`는 유효한 키-값 구분자 중 **유일한** 것입니다
- `:`는 구분자로 **인식되지 않습니다**
- 공백은 구분자로 **인식되지 않습니다**

#### 공백 처리

- 키의 앞뒤 공백은 **제거되지 않습니다**
- 값의 앞뒤 공백은 **제거됩니다**

#### 라인 처리

- `=`가 없는 줄은 무시됩니다(주석이나 빈 줄로 간주됨)
- 빈 값(`key=`)은 버전 0.9.10부터 지원됩니다
- 빈 값을 가진 키는 정상적으로 저장되고 읽어올 수 있습니다

#### 문자 제한 사항

**키에는 다음이 포함되면 안 됩니다**: - `#` (해시/파운드 기호) - `=` (등호) - `\n` (줄바꿈 문자) - `;` (세미콜론)로 시작할 수 없습니다

**값에는 다음이 포함될 수 없습니다**: - `#` (해시/파운드 기호) - `\n` (줄바꿈 문자) - `\r` (캐리지 리턴)로 시작하거나 끝날 수 없음 - 공백으로 시작하거나 끝날 수 없음 (자동으로 제거됨)

### 파일 정렬

구성 파일은 키 기준으로 정렬할 필요는 없습니다. 그러나 대부분의 I2P 애플리케이션은 구성 파일을 작성할 때 다음을 쉽게 하기 위해 키를 알파벳순으로 정렬합니다: - 수동 편집 - 버전 관리 시스템의 diff(차이 비교) 작업 - 가독성

### 구현 세부 사항

#### 구성 파일 읽기

```java
// Method signature from net.i2p.data.DataHelper
public static Properties loadProps(File file)
```
**동작**: - UTF-8로 인코딩된 파일을 읽습니다 - 위에서 설명한 모든 형식 규칙을 강제합니다 - 문자 제한을 검증합니다 - 파일이 없으면 비어 있는 Properties 객체를 반환합니다 - 읽기 오류가 발생하면 `IOException`을 던집니다

#### 구성 파일 작성

```java
// Method signature from net.i2p.data.DataHelper
public static void storeProps(Properties props, File file)
```
**동작**: - UTF-8로 인코딩된 파일을 작성함 - 키를 알파벳 순으로 정렬함 (OrderedProperties를 사용하지 않는 한) - 버전 0.8.1부터 파일 권한을 모드 600(사용자 읽기/쓰기만)으로 설정함 - 키 또는 값에 잘못된 문자가 있을 경우 `IllegalArgumentException`을 던짐 - 쓰기 오류 시 `IOException`을 던짐

#### 형식 검증

이 구현은 엄격한 검증을 수행합니다: - 키와 값에 금지된 문자가 있는지 검사합니다 - 잘못된 항목은 쓰기 작업 중 예외를 발생시킵니다 - 읽기 시 형식이 잘못된 줄(`=` 없는 줄)은 조용히 무시됩니다

### 형식 예제

#### 유효한 구성 파일

```properties
# This is a comment
; This is also a comment (column 1 only)
key.with.dots=value with spaces
another_key=value=with=equals
empty.value=
numeric.value=12345
unicode.value=こんにちは
```
#### 잘못된 구성 예시

```properties
# INVALID: Key contains equals sign
invalid=key=value

# INVALID: Key contains hash
invalid#key=value

# INVALID: Value contains newline (implicit)
key=value
continues here

# INVALID: Semicolon comment not in column 1 (treated as key)
 ; not.a.comment=value
```
---

## 코어 라이브러리 및 Router 구성

### 클라이언트 구성 (clients.config)

**위치**: `$I2P_CONFIG_DIR/clients.config` (레거시) 또는 `$I2P_CONFIG_DIR/clients.config.d/` (현대식)   **구성 인터페이스**: Router 콘솔의 `/configclients`   **형식 변경**: 버전 0.9.42 (2019년 8월)

#### 디렉터리 구조 (버전 0.9.42+)

릴리스 0.9.42부터 기본 clients.config 파일이 자동으로 개별 구성 파일로 분할됩니다:

```
$I2P_CONFIG_DIR/
├── clients.config.d/
│   ├── 00-webConsole.config
│   ├── 01-i2ptunnel.config
│   ├── 02-i2psnark.config
│   ├── 03-susidns.config
│   └── ...
└── clients.config (legacy, auto-migrated)
```
**마이그레이션 동작**: - 0.9.42+로 업그레이드한 뒤 첫 실행 시, monolithic file(모놀리식, 단일 구조의 파일)이 자동으로 분할됩니다 - 분리된 파일의 속성에는 `clientApp.0.` 접두사가 붙습니다 - 하위 호환성을 위해 레거시 형식도 계속 지원됩니다 - 분할 형식은 모듈식 패키징과 플러그인 관리를 가능하게 합니다

#### 속성 형식

각 줄은 `clientApp.x.prop=val` 형식을 따르며, 여기서 `x`는 앱 번호입니다.

**앱 번호 매기기 요구사항**: - 반드시 0부터 시작해야 함 - 반드시 연속적이어야 함 (누락 없음) - 나열 순서가 시작 순서를 결정함

#### 필수 속성

##### 메인

- **유형**: String (정규화된 클래스 이름)
- **필수**: 예
- **설명**: 클라이언트 유형(관리형 vs. 비관리형)에 따라 이 클래스의 생성자 또는 `main()` 메서드가 호출됩니다
- **예**: `clientApp.0.main=net.i2p.router.web.RouterConsoleRunner`

#### 선택적 속성

##### 이름

- **유형**: 문자열
- **필수**: 아니오
- **설명**: router console에 표시되는 이름
- **예시**: `clientApp.0.name=Router Console`

##### 인수

- **Type**: 문자열(공백 또는 탭으로 구분됨)
- **Required**: 아니오
- **Description**: 메인 클래스의 생성자 또는 main() 메서드에 전달되는 인자
- **Quoting**: 공백 또는 탭이 포함된 인자는 `'` 또는 `"`로 감싸서 사용할 수 있음
- **Example**: `clientApp.0.args=-d $CONFIG/eepsite`

##### 지연

- **유형**: 정수(초)
- **필수**: 아니오
- **기본값**: 120
- **설명**: 클라이언트를 시작하기 전에 대기할 시간(초)
- **재정의**: `onBoot=true`에 의해 재정의됨(지연을 0으로 설정)
- **특수 값**:
  - `< 0`: router가 RUNNING 상태에 도달할 때까지 대기한 후 새 스레드에서 즉시 시작
  - `= 0`: 같은 스레드에서 즉시 실행(예외가 콘솔로 전파됨)
  - `> 0`: 지연 후 새 스레드에서 시작(예외는 로그에 기록되고 전파되지 않음)

##### onBoot

- **유형**: 불리언
- **필수**: 아니요
- **기본값**: false
- **설명**: 지연 시간을 0으로 강제하며, 명시적으로 지정한 지연 설정을 재정의합니다
- **사용 사례**: router 부팅 시 핵심 서비스를 즉시 시작

##### startOnLoad

- **유형**: Boolean
- **필수**: 아니오
- **기본값**: true
- **설명**: 클라이언트를 아예 시작할지 여부
- **사용 사례**: 구성을 제거하지 않고 클라이언트를 비활성화

#### 플러그인별 속성

이 속성들은 플러그인에서만 사용됩니다(코어 클라이언트에서는 사용되지 않습니다):

##### stopargs

- **유형**: 문자열 (공백 또는 탭으로 구분)
- **설명**: 클라이언트를 중지시키는 데 전달되는 인수
- **변수 치환**: 예 (아래 참조)

##### uninstallargs

- **Type**: 문자열(공백 또는 탭으로 구분됨)
- **Description**: 클라이언트를 제거할 때 전달되는 인수
- **Variable Substitution**: 예(아래 참조)

##### 클래스패스

- **유형**: 문자열 (쉼표로 구분된 경로)
- **설명**: 클라이언트용 추가 classpath 요소
- **변수 치환**: 예 (아래 참조)

#### 변수 치환 (플러그인 전용)

플러그인의 `args`, `stopargs`, `uninstallargs`, 그리고 `classpath`에서 다음 변수들이 치환됩니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P installation directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>/usr/share/i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User configuration directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p/plugins/foo</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$OS</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Operating system name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>linux</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$ARCH</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Architecture name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>amd64</code></td>
    </tr>
  </tbody>
</table>
**참고**: 변수 치환은 플러그인에서만 수행되며, 코어 클라이언트에는 적용되지 않습니다.

#### 클라이언트 유형

##### 관리형 클라이언트

- 생성자는 `RouterContext` 및 `ClientAppManager` 매개변수와 함께 호출됩니다
- 클라이언트는 `ClientApp` 인터페이스를 구현해야 합니다
- 수명 주기는 router에 의해 제어됩니다
- 동적으로 시작, 중지 및 재시작할 수 있습니다

##### 비관리형 클라이언트

- `main(String[] args)` 메서드가 호출됨
- 별도의 스레드에서 실행
- 라이프사이클은 router에서 관리되지 않음
- 레거시 클라이언트 유형

#### 구성 예제

```properties
# Router Console (core client)
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=-d $CONFIG/eepsite
clientApp.0.delay=0
clientApp.0.onBoot=true
clientApp.0.startOnLoad=true

# I2PTunnel (core client)
clientApp.1.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.1.name=I2PTunnel
clientApp.1.args=
clientApp.1.delay=120
clientApp.1.startOnLoad=true

# Plugin Example
clientApp.2.main=org.example.plugin.PluginMain
clientApp.2.name=Example Plugin
clientApp.2.args=-config $PLUGIN/config.properties
clientApp.2.stopargs=-shutdown
clientApp.2.uninstallargs=-remove $PLUGIN
clientApp.2.classpath=$PLUGIN/lib/plugin.jar,$PLUGIN/lib/dep.jar
clientApp.2.delay=240
clientApp.2.startOnLoad=true
```
---

### 로거 구성 (logger.config)

**위치**: `$I2P_CONFIG_DIR/logger.config`   **설정 인터페이스**: Router 콘솔의 `/configlogging`

#### 속성 참조

##### 콘솔 버퍼 설정

###### logger.consoleBufferSize

- **유형**: 정수
- **기본값**: 20
- **설명**: 콘솔에서 버퍼링할 로그 메시지의 최대 개수
- **범위**: 1-1000 권장

##### 날짜와 시간 형식

###### logger.dateFormat

- **유형**: 문자열(SimpleDateFormat 패턴)
- **기본값**: 시스템 로케일에서 가져옴
- **예시**: `HH:mm:ss.SSS`
- **문서**: [Java SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)

##### 로그 레벨

###### logger.defaultLevel

- **유형**: 열거형
- **기본값**: ERROR
- **값**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **설명**: 모든 클래스에 대한 기본 로그 수준

###### logger.minimumOnScreenLevel

- **Type**: 열거형
- **Default**: CRIT
- **Values**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Description**: 화면에 표시되는 메시지의 최소 레벨

###### logger.record.{class}

- **유형**: Enum(열거형)
- **값**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **설명**: 클래스별 로그 레벨 재정의
- **예시**: `logger.record.net.i2p.router.transport.udp=DEBUG`

##### 표시 옵션

###### logger.displayOnScreen

- **유형**: 불리언
- **기본값**: true
- **설명**: 콘솔 출력에 로그 메시지를 표시할지 여부

###### logger.dropDuplicates

- **유형**: 불리언
- **기본값**: true
- **설명**: 연속된 중복 로그 메시지를 제거합니다

###### logger.dropOnOverflow

- **유형**: 불리언
- **기본값**: false
- **설명**: 버퍼가 가득 찼을 때 메시지를 버립니다(블로킹 대신)

##### 플러시 동작 방식

###### logger.flushInterval

- **유형**: 정수 (초)
- **기본값**: 29
- **도입 버전**: 0.9.18
- **설명**: 로그 버퍼를 디스크에 플러시하는 주기

##### 형식 설정

###### logger.format

- **유형**: 문자열 (문자 시퀀스)
- **설명**: 로그 메시지 형식 템플릿
- **형식 문자**:
  - `d` = 날짜/시간
  - `c` = 클래스 이름
  - `t` = 스레드 이름
  - `p` = 우선순위(로그 레벨)
  - `m` = 메시지
- **예시**: `dctpm`은 `[타임스탬프] [클래스] [스레드] [레벨] 메시지`를 생성합니다

##### 압축 (버전 0.9.56+)

###### logger.gzip

- **유형**: Boolean
- **기본값**: false
- **도입 버전**: 0.9.56
- **설명**: 로테이션된 로그 파일에 대해 gzip 압축을 활성화합니다

###### logger.minGzipSize

- **유형**: 정수(바이트)
- **기본값**: 65536
- **도입**: 버전 0.9.56
- **설명**: 압축을 트리거하는 최소 파일 크기(기본값 64 KB)

##### 파일 관리

###### logger.logBufferSize

- **유형**: 정수 (바이트)
- **기본값**: 1024
- **설명**: 플러시하기 전에 버퍼링할 최대 메시지 수

###### logger.logFileName

- **유형**: 문자열 (파일 경로)
- **기본값**: `logs/log-@.txt`
- **설명**: 로그 파일 명명 패턴 (`@`은 로테이션 번호로 대체됨)

###### logger.logFilenameOverride

- **Type**: 문자열 (파일 경로)
- **Description**: 로그 파일 이름 재정의(로그 로테이션 패턴 비활성화)

###### logger.logFileSize

- **유형**: 문자열(단위가 포함된 크기)
- **기본값**: 10M
- **단위**: K (킬로바이트), M (메가바이트), G (기가바이트)
- **예시**: `50M`, `1G`

###### logger.logRotationLimit

- **유형**: 정수
- **기본값**: 2
- **설명**: 순환 로그 파일의 최대 번호 (log-0.txt부터 log-N.txt까지)

#### 구성 예제

```properties
# Basic logging configuration
logger.consoleBufferSize=50
logger.dateFormat=yyyy-MM-dd HH:mm:ss.SSS
logger.defaultLevel=WARN
logger.displayOnScreen=true
logger.dropDuplicates=true
logger.dropOnOverflow=false

# Flushing and format
logger.flushInterval=30
logger.format=dctpm

# File management
logger.logBufferSize=2048
logger.logFileName=logs/log-@.txt
logger.logFileSize=25M
logger.logRotationLimit=5

# Compression (0.9.56+)
logger.gzip=true
logger.minGzipSize=131072

# On-screen filtering
logger.minimumOnScreenLevel=ERROR

# Per-class overrides
logger.record.net.i2p.router.transport=INFO
logger.record.net.i2p.router.tunnel=DEBUG
logger.record.net.i2p.crypto=WARN
```
---

### 플러그인 구성

#### 개별 플러그인 구성 (plugins/*/plugin.config)

**위치**: `$I2P_CONFIG_DIR/plugins/{plugin-name}/plugin.config`   **형식**: 표준 I2P 구성 파일 형식   **문서**: [플러그인 사양](/docs/specs/plugin/)

##### 필수 속성

###### 이름

- **유형**: 문자열
- **필수**: 예
- **설명**: 플러그인 표시 이름
- **예시**: `name=I2P Plugin Example`

###### 키

- **유형**: 문자열(공개 키)
- **필수 여부**: 예(SU3로 서명된 플러그인의 경우 생략)
- **설명**: 검증을 위한 플러그인 서명 공개 키
- **형식**: Base64로 인코딩된 서명 키

###### 서명자

- **유형**: 문자열
- **필수**: 예
- **설명**: 플러그인 서명자 식별자
- **예시**: `signer=user@example.i2p`

###### 버전

- **유형**: 문자열 (VersionComparator 형식)
- **필수**: 예
- **설명**: 업데이트 확인을 위한 플러그인 버전
- **형식**: Semantic versioning(시맨틱 버저닝) 또는 사용자 정의 비교 가능한 형식
- **예시**: `version=1.2.3`

##### 표시 속성

###### 날짜

- **유형**: Long (Unix 타임스탬프 밀리초)
- **설명**: 플러그인 릴리스 날짜

###### 저자

- **유형**: 문자열
- **설명**: 플러그인 작성자 이름

###### websiteURL

- **유형**: 문자열 (URL)
- **설명**: 플러그인 웹사이트 URL

###### updateURL

- **유형**: 문자열 (URL)
- **설명**: 플러그인 업데이트 확인용 URL

###### updateURL.su3

- **유형**: 문자열 (URL)
- **도입 버전**: 버전 0.9.15
- **설명**: SU3 형식(I2P 업데이트 패키지 파일 형식) 업데이트 URL (권장)

###### 설명

- **유형**: 문자열
- **설명**: 영문 플러그인 설명

###### 설명_{language}

- **유형**: 문자열
- **설명**: 현지화된 플러그인 설명
- **예시**: `description_de=Deutsche Beschreibung`

###### 라이선스

- **유형**: 문자열
- **설명**: 플러그인 라이선스 식별자
- **예**: `license=Apache 2.0`

##### 설치 속성

###### 설치 시 자동 시작 안 함

- **유형**: 불리언
- **기본값**: false
- **설명**: 설치 후 자동 시작을 방지합니다

###### router 재시작 필요

- **유형**: 불리언
- **기본값**: false
- **설명**: 설치 후 router 재시작이 필요함

###### 설치 전용

- **유형**: 부울
- **기본값**: false
- **설명**: 한 번만 설치(업데이트 없음)

###### 업데이트 전용

- **Type**: Boolean
- **Default**: false
- **Description**: 기존 설치만 업데이트합니다(새로 설치하지 않음)

##### 플러그인 설정 예제

```properties
# Required properties
name=Example I2P Plugin
signer=developer@mail.i2p
version=1.5.0

# Display properties
author=Plugin Developer
websiteURL=http://plugin.example.i2p
updateURL=http://plugin.example.i2p/update.xpi2p
updateURL.su3=http://plugin.example.i2p/update.su3
description=Example plugin demonstrating configuration
description_de=Beispiel-Plugin zur Demonstration der Konfiguration
license=MIT

# Installation behavior
dont-start-at-install=false
router-restart-required=false
```
#### 전역 플러그인 구성 (plugins.config)

**위치**: `$I2P_CONFIG_DIR/plugins.config`   **목적**: 설치된 플러그인을 전역적으로 활성화/비활성화

##### 속성 형식

```properties
plugin.{name}.startOnLoad=true|false
```
- `{name}`: plugin.config의 플러그인 이름
- `startOnLoad`: router 실행 시 플러그인을 시작할지 여부

##### 예시

```properties
plugin.i2psnark.startOnLoad=true
plugin.susimail.startOnLoad=true
plugin.susidns.startOnLoad=true
plugin.i2pbote.startOnLoad=false
```
---

### 웹 애플리케이션 설정 (webapps.config)

**위치**: `$I2P_CONFIG_DIR/webapps.config`   **목적**: 웹 애플리케이션을 활성화/비활성화하고 구성

#### 속성 형식

##### webapps.{name}.startOnLoad

- **유형**: Boolean
- **설명**: router 시작 시 웹앱을 시작할지 여부
- **형식**: `webapps.{name}.startOnLoad=true|false`

##### webapps.{name}.classpath

- **유형**: String(문자열) (공백 또는 쉼표로 구분된 경로)
- **설명**: 웹앱용 추가 클래스패스 요소
- **형식**: `webapps.{name}.classpath=[paths]`

#### 변수 치환

경로는 다음과 같은 변수 치환을 지원합니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User config directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin webapps</td>
    </tr>
  </tbody>
</table>
#### 클래스패스 해석

- **코어 웹앱**: `$I2P/lib`를 기준으로 한 상대 경로
- **플러그인 웹앱**: `$CONFIG/plugins/{appname}/lib`를 기준으로 한 상대 경로

#### 구성 예제

```properties
# Router console
webapps.routerconsole.startOnLoad=true
webapps.routerconsole.classpath=routerconsole.jar

# I2PSnark
webapps.i2psnark.startOnLoad=true
webapps.i2psnark.classpath=i2psnark.jar

# SusiDNS
webapps.susidns.startOnLoad=true
webapps.susidns.classpath=susidns.jar

# Plugin webapp example
webapps.exampleplugin.startOnLoad=false
webapps.exampleplugin.classpath=$PLUGIN/lib/webapp.jar,$PLUGIN/lib/deps.jar
```
---

### Router 설정 (router.config)

**위치**: `$I2P_CONFIG_DIR/router.config`   **구성 인터페이스**: `/configadvanced`의 Router 콘솔   **용도**: 핵심 router 설정 및 네트워크 매개변수

#### 설정 범주

##### 네트워크 설정

대역폭 설정:

```properties
i2np.bandwidth.inboundKBytesPerSecond=100
i2np.bandwidth.outboundKBytesPerSecond=50
i2np.bandwidth.share.percentage=80
```
전송 구성:

```properties
# NTCP (TCP-based transport)
i2np.ntcp.port=8887
i2np.ntcp.enable=true
i2np.ntcp.autoip=true

# SSU (UDP-based transport)
i2np.udp.port=8887
i2np.udp.enable=true

# UPnP/NAT-PMP
i2np.upnp.enable=true
```
##### Router 동작 방식

```properties
# Tunnel participation
router.maxParticipatingTunnels=200
router.sharePercentage=80

# Updates
router.updatePolicy=notify
router.updateURL=http://update.i2p2.i2p/

# Network integration
router.hiddenMode=false
router.clockSkewOffset=0
```
##### 콘솔 설정

```properties
# Language and display
routerconsole.lang=en
routerconsole.country=US
routerconsole.summaryRefresh=60

# Browser
routerconsole.browser=default

# Security
routerconsole.enableCompression=true
```
##### 시간 설정

```properties
# NTP
time.disabled=false
time.sntpServerList=0.pool.ntp.org,1.pool.ntp.org
```
**참고**: Router 설정은 방대합니다. 전체 속성 레퍼런스는 `/configadvanced`의 router 콘솔에서 확인하세요.

---

## 애플리케이션 구성 파일

### 주소록 설정 (addressbook/config.txt)

**위치**: `$I2P_CONFIG_DIR/addressbook/config.txt`   **애플리케이션**: SusiDNS   **목적**: 호스트 이름 해석 및 주소록 관리

#### 파일 위치

##### router_addressbook

- **기본값**: `../hosts.txt`
- **설명**: 마스터 주소록(시스템 전역 호스트 이름)
- **형식**: 표준 hosts 파일 형식

##### privatehosts.txt

- **위치**: `$I2P_CONFIG_DIR/addressbook/privatehosts.txt`
- **설명**: 개인용 호스트 이름 매핑
- **우선순위**: 최상위 (다른 모든 소스를 덮어씀)

##### userhosts.txt

- **위치**: `$I2P_CONFIG_DIR/addressbook/userhosts.txt`
- **설명**: 사용자가 추가한 호스트명 매핑
- **관리**: SusiDNS 인터페이스를 통해

##### hosts.txt

- **위치**: `$I2P_CONFIG_DIR/addressbook/hosts.txt`
- **설명**: 다운로드된 공개 주소록
- **출처**: 구독 피드

#### 네이밍 서비스

##### BlockfileNamingService (0.8.8부터 기본)

저장 형식: - **파일**: `hostsdb.blockfile` - **위치**: `$I2P_CONFIG_DIR/addressbook/` - **성능**: hosts.txt 대비 ~10배 더 빠른 조회 - **형식**: 이진 데이터베이스 형식

레거시 네이밍 서비스: - **형식**: 평문 텍스트 hosts.txt - **상태**: 더 이상 권장되지 않지만 여전히 지원됨 - **사용 사례**: 수동 편집, 버전 관리

#### 호스트 이름 규칙

I2P 호스트명은 다음을 준수해야 합니다:

1. **TLD 요구 사항**: `.i2p`로 끝나야 함
2. **최대 길이**: 총 67자
3. **문자 집합**: `[a-z]`, `[0-9]`, `.` (마침표), `-` (하이픈)
4. **대소문자**: 소문자만
5. **시작 제한**: `.` 또는 `-`로 시작할 수 없음
6. **금지된 패턴**: `..`, `.-`, `-.` 포함 불가 (0.6.1.33부터)
7. **예약됨**: Base32 호스트명 `*.b32.i2p` (base32.b32.i2p는 52자)

##### 유효한 예시

```
example.i2p
my-site.i2p
test.example.i2p
site123.i2p
```
##### 잘못된 예제

```
example.com          # Wrong TLD
-invalid.i2p         # Starts with hyphen
invalid..i2p         # Contains double dot
invalid.-.i2p        # Contains dot-hyphen
UPPERCASE.I2P        # Must be lowercase
verylonghostnameover67charactersthatexceedsthemaximumlength.i2p  # Too long
```
#### 구독 관리

##### subscriptions.txt

- **위치**: `$I2P_CONFIG_DIR/addressbook/subscriptions.txt`
- **형식**: 한 줄에 하나의 URL
- **기본값**: `http://i2p-projekt.i2p/hosts.txt`

##### 구독 피드 형식 (0.9.26부터)

메타데이터가 포함된 고급 피드 형식:

```
#
# I2P Address Book Subscription Feed
# Format: hostname=destination [#property=value ...]
#

example.i2p=base64destination #added=20250101 #src=manual
another.i2p=base64destination #added=20250102 #src=feed1
```
메타데이터 속성: - `added`: 호스트명이 추가된 날짜(YYYYMMDD 형식) - `src`: 소스 식별자 - `sig`: 선택적 서명

**하위 호환성**: 간단한 hostname=destination 형식은 여전히 지원됩니다.

#### 구성 예시

```properties
# Address book locations
router_addressbook=../hosts.txt
privatehosts.txt=$CONFIG/addressbook/privatehosts.txt
userhosts.txt=$CONFIG/addressbook/userhosts.txt
hosts.txt=$CONFIG/addressbook/hosts.txt

# Naming service
naming.service=BlockfileNamingService
naming.service.blockfile.location=$CONFIG/addressbook/hostsdb.blockfile

# Subscriptions
subscriptions.txt=$CONFIG/addressbook/subscriptions.txt
subscriptions.schedule=daily
subscriptions.proxy=false
```
---

### I2PSnark 구성 (i2psnark.config.d/i2psnark.config)

**위치**: `$I2P_CONFIG_DIR/i2psnark.config.d/i2psnark.config`   **애플리케이션**: I2PSnark BitTorrent 클라이언트   **설정 인터페이스**: http://127.0.0.1:7657/i2psnark 의 웹 GUI

#### 디렉터리 구조

```
$I2P_CONFIG_DIR/i2psnark.config.d/
├── i2psnark.config
├── [torrent-hash-1]/
│   └── *.config
├── [torrent-hash-2]/
│   └── *.config
└── ...
```
#### 주요 설정 (i2psnark.config)

최소한의 기본 구성:

```properties
i2psnark.dir=i2psnark
```
웹 인터페이스를 통해 관리되는 추가 속성:

```properties
# Basic settings
i2psnark.dir=i2psnark
i2psnark.autoStart=false
i2psnark.openTrackers=true

# Network settings
i2psnark.uploaders=8
i2psnark.upBW=40
i2psnark.seedPct=100

# I2CP settings
i2psnark.i2cpHost=127.0.0.1
i2psnark.i2cpPort=7654
```
#### 개별 토렌트 설정

**위치**: `$I2P_CONFIG_DIR/i2psnark.config.d/[torrent-hash]/*.config`   **형식**: 토렌트별 설정   **관리**: 자동 (웹 GUI를 통해)

속성에는 다음이 포함됩니다: - 토렌트별 업로드/다운로드 설정 - 파일 우선순위 - 트래커 정보 - 피어 제한

**참고**: 토렌트 구성은 주로 웹 인터페이스를 통해 관리됩니다. 수동으로 편집하는 것은 권장되지 않습니다.

#### 토렌트 데이터 구성

데이터 저장소는 설정과 분리되어 있습니다:

```
$I2P_CONFIG_DIR/i2psnark/          # Data directory
├── *.torrent                       # Torrent metadata files
├── *.torrent.downloaded/           # Downloaded file directories
├── file1.dat                       # Direct file downloads
└── ...

$I2P_CONFIG_DIR/i2psnark.config.d/ # Configuration directory
├── i2psnark.config                 # Main config
└── [hashes]/                       # Per-torrent configs
```
---

### I2PTunnel 설정 (i2ptunnel.config)

**위치**: `$I2P_CONFIG_DIR/i2ptunnel.config` (레거시) 또는 `$I2P_CONFIG_DIR/i2ptunnel.config.d/` (최신)   **구성 인터페이스**: Router 콘솔의 `/i2ptunnel`   **형식 변경**: 버전 0.9.42 (2019년 8월)

#### 디렉터리 구조 (버전 0.9.42+)

0.9.42 릴리스부터 기본 i2ptunnel.config 파일이 자동으로 나뉩니다:

```
$I2P_CONFIG_DIR/
├── i2ptunnel.config.d/
│   ├── http-proxy/
│   │   └── tunnel.config
│   ├── irc-proxy/
│   │   └── tunnel.config
│   ├── ssh-service/
│   │   └── tunnel.config
│   └── ...
└── i2ptunnel.config (legacy, auto-migrated)
```
**중요한 형식 차이**: - **모놀리식 형식**: 속성 앞에 `tunnel.N.` 접두사가 붙음 - **분리형 형식**: 속성에는 접두사가 **없음** (예: `description=`, `tunnel.0.description=`가 아님)

#### 마이그레이션 동작

0.9.42로 업그레이드 후 첫 실행 시:
1. 기존 i2ptunnel.config 파일을 읽습니다
2. 개별 tunnel 설정이 i2ptunnel.config.d/ 디렉터리에 생성됩니다
3. 분리된 파일에서 속성의 접두사가 제거됩니다
4. 원본 파일이 백업됩니다
5. 하위 호환성을 위해 이전 형식도 계속 지원됩니다

#### 구성 섹션

I2PTunnel 구성은 아래의 [I2PTunnel 구성 참조](#i2ptunnel-configuration-reference) 섹션에서 자세히 설명되어 있습니다. 속성 설명은 모놀리식(`tunnel.N.property`) 형식과 분리(`property`) 형식 모두에 적용됩니다.

---

## I2PTunnel 설정 참조

이 섹션에서는 모든 I2PTunnel 구성 속성에 대한 포괄적인 기술 참조를 제공합니다. 속성은 `tunnel.N.` 접두사 없이 분리 형식으로 표시됩니다. 모놀리식 형식의 경우 모든 속성 앞에 `tunnel.N.` 접두사를 붙이며, 여기서 N은 tunnel 번호입니다.

**중요**: `tunnel.N.option.i2cp.*`로 기술된 속성은 I2PTunnel(트래픽 경로를 구성·관리하는 도구)에서 구현되어 있으며, I2CP 프로토콜(I2P router와 애플리케이션 간 제어 프로토콜)이나 SAM API(I2P용 Simple Anonymous Messaging 인터페이스)와 같은 다른 인터페이스를 통해서는 **지원되지 않습니다**.

### 기본 속성

#### tunnel.N.description (설명)

- **유형**: 문자열
- **적용 범위**: 모든 tunnel(터널, I2P의 통신 경로)
- **설명**: UI 표시용 사람이 읽을 수 있는 tunnel 설명
- **예시**: `description=HTTP Proxy for outproxy access`

#### tunnel.N.name (이름)

- **유형**: 문자열
- **컨텍스트**: 모든 tunnel(트래픽을 전달하는 I2P 경로)
- **필수**: 예
- **설명**: 고유한 tunnel 식별자 및 표시 이름
- **예시**: `name=I2P HTTP Proxy`

#### tunnel.N.type (유형)

- **유형**: 열거형
- **컨텍스트**: 모든 tunnel
- **필수**: 예
- **값**:
  - `client` - 일반적인 클라이언트 tunnel
  - `httpclient` - HTTP 프록시 클라이언트
  - `ircclient` - IRC 클라이언트 tunnel
  - `socksirctunnel` - SOCKS IRC 프록시
  - `sockstunnel` - SOCKS 프록시(버전 4, 4a, 5)
  - `connectclient` - CONNECT 프록시 클라이언트
  - `streamrclient` - Streamr 클라이언트
  - `server` - 일반적인 서버 tunnel
  - `httpserver` - HTTP 서버 tunnel
  - `ircserver` - IRC 서버 tunnel
  - `httpbidirserver` - 양방향 HTTP 서버
  - `streamrserver` - Streamr 서버

#### tunnel.N.interface (인터페이스)

- **유형**: 문자열(IP 주소 또는 호스트명)
- **컨텍스트**: 클라이언트 tunnel에만 해당
- **기본값**: 127.0.0.1
- **설명**: 수신 연결을 위해 바인딩할 로컬 인터페이스
- **보안 참고**: 0.0.0.0에 바인딩하면 원격 연결을 허용합니다
- **예시**: `interface=127.0.0.1`

#### tunnel.N.listenPort (listenPort)

- **유형**: 정수
- **적용 범위**: 클라이언트 tunnel 전용
- **범위**: 1-65535
- **설명**: 클라이언트 연결을 수신 대기할 로컬 포트
- **예시**: `listenPort=4444`

#### tunnel.N.targetHost (targetHost)

- **유형**: 문자열(IP 주소 또는 호스트 이름)
- **적용 대상**: 서버 tunnel에서만 사용
- **설명**: 연결을 전달할 로컬 서버
- **예**: `targetHost=127.0.0.1`

#### tunnel.N.targetPort (targetPort)

- **유형**: 정수
- **적용 대상**: 서버 tunnels에만 해당
- **범위**: 1-65535
- **설명**: 연결할 targetHost의 포트
- **예**: `targetPort=80`

#### tunnel.N.targetDestination (targetDestination)

- **유형**: 문자열(쉼표 또는 공백으로 구분된 Destination(목적지 주소) 목록)
- **컨텍스트**: 클라이언트 tunnels에만 해당
- **형식**: `destination[:port][,destination[:port]]`
- **설명**: 연결할 I2P Destination
- **예시**:
  - `targetDestination=example.i2p`
  - `targetDestination=example.i2p:8080`
  - `targetDestination=site1.i2p,site2.i2p:8080`

#### tunnel.N.i2cpHost (i2cpHost)

- **유형**: 문자열(IP 주소 또는 호스트 이름)
- **기본값**: 127.0.0.1
- **설명**: I2P router의 I2CP 인터페이스 주소
- **참고**: router 컨텍스트에서 실행 중에는 무시됩니다
- **예**: `i2cpHost=127.0.0.1`

#### tunnel.N.i2cpPort (i2cpPort)

- **유형**: 정수
- **기본값**: 7654
- **범위**: 1-65535
- **설명**: I2P router의 I2CP 포트
- **참고**: router 컨텍스트에서 실행 중일 때 무시됨
- **예시**: `i2cpPort=7654`

#### tunnel.N.startOnLoad (startOnLoad)

- **유형**: Boolean
- **기본값**: true
- **설명**: I2PTunnel이 로드될 때 tunnel을 시작할지 여부
- **예**: `startOnLoad=true`

### 프록시 구성

#### tunnel.N.proxyList (proxyList)

- **유형**: 문자열 (쉼표 또는 공백으로 구분된 호스트 이름)
- **적용 범위**: HTTP 및 SOCKS 프록시에만 해당
- **설명**: outproxy(외부로 나가는 프록시) 호스트 목록
- **예**: `proxyList=outproxy.example.i2p,backup.example.i2p`

### 서버 구성

#### tunnel.N.privKeyFile (privKeyFile)

- **유형**: 문자열 (파일 경로)
- **컨텍스트**: 서버 및 지속형 클라이언트 tunnels
- **설명**: 지속형 목적지의 개인 키를 포함하는 파일
- **경로**: I2P 설정 디렉터리를 기준으로 하는 절대 경로 또는 상대 경로
- **예시**: `privKeyFile=eepsite/eepPriv.dat`

#### tunnel.N.spoofedHost (spoofedHost)

- **유형**: 문자열 (호스트명)
- **컨텍스트**: HTTP 서버에만 해당
- **기본값**: 대상의 Base32 호스트명
- **설명**: 로컬 서버로 전달되는 Host 헤더 값
- **예**: `spoofedHost=example.i2p`

#### tunnel.N.spoofedHost.NNNN (spoofedHost.NNNN)

- **유형**: 문자열(호스트명)
- **컨텍스트**: HTTP 서버에만 해당
- **설명**: 특정 수신 포트에 대한 가상 호스트 재정의
- **사용 사례**: 서로 다른 포트에서 여러 사이트를 호스팅
- **예시**: `spoofedHost.8080=site1.example.i2p`

### 클라이언트별 옵션

#### tunnel.N.sharedClient (sharedClient)

- **유형**: 불리언
- **컨텍스트**: Client tunnels 전용
- **기본값**: false
- **설명**: 여러 클라이언트가 이 tunnel을 공유할 수 있는지 여부
- **예시**: `sharedClient=false`

#### tunnel.N.option.persistentClientKey (persistentClientKey)

- **Type**: 불리언
- **Context**: 클라이언트 tunnel(터널) 전용
- **Default**: false
- **Description**: 재시작 간에도 destination keys(목적지 키)를 저장하고 재사용
- **Conflict**: `i2cp.newDestOnResume=true`와 상호 배타적
- **Example**: `option.persistentClientKey=true`

### I2CP 옵션 (I2PTunnel 구현)

**중요**: 이 속성들은 `option.i2cp.` 접두사가 붙어 있지만, I2CP 프로토콜 계층이 아니라 **I2PTunnel에서 구현됩니다**. I2CP 또는 SAM API를 통해서는 사용할 수 없습니다.

#### tunnel.N.option.i2cp.delayOpen (option.i2cp.delayOpen)

- **유형**: 부울
- **컨텍스트**: 클라이언트 tunnels 전용
- **기본값**: false
- **설명**: 첫 연결이 이루어질 때까지 tunnel 생성 지연
- **사용 사례**: 드물게 사용되는 tunnels에 대한 리소스 절약
- **예시**: `option.i2cp.delayOpen=false`

#### tunnel.N.option.i2cp.newDestOnResume (option.i2cp.newDestOnResume)

- **유형**: 불리언
- **적용 범위**: 클라이언트 tunnel에만 해당
- **기본값**: false
- **필수 조건**: `i2cp.closeOnIdle=true`
- **충돌**: `persistentClientKey=true`와 상호 배타적임
- **설명**: 유휴 시간 초과 후 새 destination(목적지) 생성
- **예시**: `option.i2cp.newDestOnResume=false`

#### tunnel.N.option.i2cp.leaseSetPrivateKey (option.i2cp.leaseSetPrivateKey)

- **유형**: 문자열 (base64로 인코딩된 키)
- **컨텍스트**: 서버 tunnel 전용
- **설명**: 지속적으로 사용하는 leaseset(목적지 연결 정보 데이터 구조) 암호화용 개인 키
- **사용 사례**: 재시작 간에도 암호화된 leaseset을 일관되게 유지
- **예시**: `option.i2cp.leaseSetPrivateKey=AAAA...base64...`

#### tunnel.N.option.i2cp.leaseSetSigningPrivateKey (option.i2cp.leaseSetSigningPrivateKey)

- **유형**: 문자열 (sigtype:base64)
- **컨텍스트**: 서버 tunnel 전용
- **형식**: `sigtype:base64key`
- **설명**: 영구적인 leaseset 서명용 개인 키
- **예**: `option.i2cp.leaseSetSigningPrivateKey=7:AAAA...base64...`

### 서버별 옵션

#### tunnel.N.option.enableUniqueLocal (option.enableUniqueLocal)

- **유형**: 불리언(Boolean)
- **컨텍스트**: Server tunnels에만 해당
- **기본값**: false
- **설명**: 원격 I2P 목적지마다 고유한 로컬 IP 사용
- **사용 사례**: 서버 로그에서 클라이언트 IP를 추적
- **보안 참고**: 익명성이 낮아질 수 있음
- **예시**: `option.enableUniqueLocal=false`

#### tunnel.N.option.targetForPort.NNNN (option.targetForPort.NNNN)

- **유형**: 문자열 (hostname:port)
- **컨텍스트**: 서버 tunnels(I2P의 통신 경로) 전용
- **설명**: 수신 포트 NNNN에 대해 targetHost/targetPort를 재정의합니다
- **사용 사례**: 서로 다른 로컬 서비스로의 포트 기반 라우팅
- **예**: `option.targetForPort.8080=localhost:8080`

### 스레드 풀 구성

#### tunnel.N.option.i2ptunnel.usePool (option.i2ptunnel.usePool)

- **유형**: Boolean
- **컨텍스트**: 서버 tunnels 전용
- **기본값**: true
- **설명**: 연결 처리를 위해 스레드 풀 사용
- **비고**: 표준 서버에서는 항상 false(무시됨)
- **예시**: `option.i2ptunnel.usePool=true`

#### tunnel.N.option.i2ptunnel.blockingHandlerCount (option.i2ptunnel.blockingHandlerCount)

- **유형**: 정수
- **적용 범위**: 서버 tunnel 전용
- **기본값**: 65
- **설명**: 최대 스레드 풀 크기
- **참고**: 표준 서버에서는 무시됨
- **예시**: `option.i2ptunnel.blockingHandlerCount=100`

### HTTP 클라이언트 옵션

#### tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL (option.i2ptunnel.httpclient.allowInternalSSL)

- **유형**: Boolean
- **컨텍스트**: HTTP 클라이언트 전용
- **기본값**: false
- **설명**: .i2p 주소에 대한 SSL 연결을 허용
- **예시**: `option.i2ptunnel.httpclient.allowInternalSSL=false`

#### tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper (option.i2ptunnel.httpclient.disableAddressHelper)

- **유형**: 부울
- **컨텍스트**: HTTP 클라이언트 전용
- **기본값**: false
- **설명**: 프록시 응답에서 address helper 링크를 비활성화합니다
- **예시**: `option.i2ptunnel.httpclient.disableAddressHelper=false`

#### tunnel.N.option.i2ptunnel.httpclient.jumpServers (option.i2ptunnel.httpclient.jumpServers)

- **Type**: 문자열 (쉼표 또는 공백으로 구분된 URL)
- **Context**: HTTP 클라이언트 전용
- **Description**: 호스트명 해석을 위한 Jump server(점프 서버) URL
- **Example**: `option.i2ptunnel.httpclient.jumpServers=http://jump.i2p/jump,http://stats.i2p/jump`

#### tunnel.N.option.i2ptunnel.httpclient.sendAccept (option.i2ptunnel.httpclient.sendAccept)

- **유형**: Boolean
- **컨텍스트**: HTTP 클라이언트 전용
- **기본값**: false
- **설명**: Accept 및 Accept-Encoding을 제외한 Accept-* 헤더를 전달합니다
- **예**: `option.i2ptunnel.httpclient.sendAccept=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendReferer (option.i2ptunnel.httpclient.sendReferer)

- **유형**: 부울
- **컨텍스트**: HTTP 클라이언트 전용
- **기본값**: false
- **설명**: 프록시를 통해 Referer 헤더 전달
- **개인정보 보호 참고**: 개인정보가 유출될 수 있음
- **예시**: `option.i2ptunnel.httpclient.sendReferer=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendUserAgent (option.i2ptunnel.httpclient.sendUserAgent)

- **유형**: Boolean
- **컨텍스트**: HTTP 클라이언트 전용
- **기본값**: false
- **설명**: User-Agent 헤더를 프록시를 통해 전달
- **프라이버시 주의**: 브라우저 정보가 유출될 수 있음
- **예**: `option.i2ptunnel.httpclient.sendUserAgent=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendVia (option.i2ptunnel.httpclient.sendVia)

- **유형**: Boolean
- **컨텍스트**: HTTP 클라이언트 전용
- **기본값**: false
- **설명**: 프록시를 통해 Via 헤더를 전달
- **예시**: `option.i2ptunnel.httpclient.sendVia=false`

#### tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies (option.i2ptunnel.httpclient.SSLOutproxies)

- **Type**: 문자열(쉼표 또는 공백으로 구분된 destination(목적지) 목록)
- **Context**: HTTP 클라이언트 전용
- **Description**: HTTPS를 위한 I2P 네트워크 내 SSL outproxies(외부 프록시)
- **Example**: `option.i2ptunnel.httpclient.SSLOutproxies=ssl-outproxy.i2p`

#### tunnel.N.option.i2ptunnel.useLocalOutproxy (option.i2ptunnel.useLocalOutproxy)

- **유형**: 불리언
- **컨텍스트**: HTTP 클라이언트 전용
- **기본값**: true
- **설명**: 등록된 로컬 outproxy(외부 프록시) 플러그인 사용
- **예시**: `option.i2ptunnel.useLocalOutproxy=true`

### HTTP 클라이언트 인증

#### tunnel.N.option.proxyAuth (option.proxyAuth)

- **유형**: 열거형(Enum)
- **적용 범위**: HTTP 클라이언트 전용
- **기본값**: false
- **값**: `true`, `false`, `basic`, `digest`
- **설명**: 프록시에 접근하려면 로컬 인증이 필요합니다
- **참고**: `true`는 `basic`과 동일합니다
- **예시**: `option.proxyAuth=basic`

#### tunnel.N.option.proxy.auth.USER.md5 (option.proxy.auth.USER.md5)

- **형식**: 문자열(소문자 16진수 32자)
- **적용 대상**: HTTP 클라이언트만
- **필수 조건**: `proxyAuth=basic` 또는 `proxyAuth=digest`
- **설명**: 사용자 USER의 비밀번호에 대한 MD5 해시
- **사용 중단**: 대신 SHA-256을 사용하세요 (0.9.56+)
- **예시**: `option.proxy.auth.alice.md5=5f4dcc3b5aa765d61d8327deb882cf99`

#### tunnel.N.option.proxy.auth.USER.sha256 (option.proxy.auth.USER.sha256)

- **유형**: 문자열(소문자 16진수 64자)
- **적용 대상**: HTTP 클라이언트 전용
- **요구 사항**: `proxyAuth=digest`
- **도입 버전**: 버전 0.9.56
- **표준**: RFC 7616
- **설명**: 사용자 USER의 비밀번호에 대한 SHA-256 해시
- **예시**: `option.proxy.auth.alice.sha256=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

### Outproxy(외부 프록시) 인증

#### tunnel.N.option.outproxyAuth (option.outproxyAuth)

- **유형**: 불리언
- **적용 범위**: HTTP 클라이언트 전용
- **기본값**: false
- **설명**: outproxy(외부 인터넷 접속을 위한 프록시)로 인증 정보를 전송
- **예시**: `option.outproxyAuth=false`

#### tunnel.N.option.outproxyUsername (option.outproxyUsername)

- **유형**: 문자열
- **컨텍스트**: HTTP 클라이언트 전용
- **요구 사항**: `outproxyAuth=true`
- **설명**: outproxy(I2P에서 일반 인터넷으로 나가기 위한 프록시) 인증에 사용할 사용자 이름
- **예**: `option.outproxyUsername=user`

#### tunnel.N.option.outproxyPassword (option.outproxyPassword)

- **유형**: 문자열
- **컨텍스트**: HTTP 클라이언트 전용
- **요구 사항**: `outproxyAuth=true`
- **설명**: outproxy(외부 프록시) 인증용 비밀번호
- **보안**: 평문으로 저장됨
- **예**: `option.outproxyPassword=secret`

### SOCKS 클라이언트 옵션

#### tunnel.N.option.i2ptunnel.socks.proxy.default (option.i2ptunnel.socks.proxy.default)

- **유형**: 문자열 (쉼표 또는 공백으로 구분된 목적지)
- **컨텍스트**: SOCKS 클라이언트에만 해당
- **설명**: 지정되지 않은 포트를 위한 I2P 네트워크 내 아웃프록시(outproxy)
- **예시**: `option.i2ptunnel.socks.proxy.default=outproxy.i2p`

#### tunnel.N.option.i2ptunnel.socks.proxy.NNNN (option.i2ptunnel.socks.proxy.NNNN)

- **유형**: 문자열(쉼표 또는 공백으로 구분된 대상 목록)
- **컨텍스트**: SOCKS 클라이언트에만 해당
- **설명**: 포트 NNNN 전용 네트워크 내 outproxy(외부 인터넷으로 나가기 위한 프록시)
- **예**: `option.i2ptunnel.socks.proxy.443=ssl-outproxy.i2p`

#### tunnel.N.option.outproxyType (option.outproxyType)

- **유형**: 열거형
- **적용 대상**: SOCKS 클라이언트 전용
- **기본값**: socks
- **도입**: 버전 0.9.57
- **값**: `socks`, `connect` (HTTPS)
- **설명**: 구성된 outproxy(외부 프록시)의 유형
- **예시**: `option.outproxyType=connect`

### HTTP 서버 옵션

#### tunnel.N.option.maxPosts (option.maxPosts)

- **유형**: 정수
- **적용 범위**: HTTP 서버 전용
- **기본값**: 0 (무제한)
- **설명**: postCheckTime마다 단일 destination(목적지 식별자)에서 오는 POST 요청의 최대 수
- **예**: `option.maxPosts=10`

#### tunnel.N.option.maxTotalPosts (option.maxTotalPosts)

- **유형**: 정수
- **적용 범위**: HTTP 서버 전용
- **기본값**: 0 (제한 없음)
- **설명**: postCheckTime마다 모든 Destination(목적지)에서 오는 POST 요청의 최대 개수
- **예시**: `option.maxTotalPosts=50`

#### tunnel.N.option.postCheckTime (option.postCheckTime)

- **유형**: 정수(초)
- **컨텍스트**: HTTP 서버 전용
- **기본값**: 300
- **설명**: POST 제한을 확인하는 시간 범위
- **예시**: `option.postCheckTime=600`

#### tunnel.N.option.postBanTime (option.postBanTime)

- **유형**: 정수(초)
- **컨텍스트**: HTTP 서버 전용
- **기본값**: 1800
- **설명**: 단일 목적지에 대해 maxPosts 초과 시 적용되는 차단 기간
- **예시**: `option.postBanTime=3600`

#### tunnel.N.option.postTotalBanTime (option.postTotalBanTime)

- **유형**: 정수(초)
- **적용 범위**: HTTP 서버 전용
- **기본값**: 600
- **설명**: maxTotalPosts 초과 시 차단 기간
- **예시**: `option.postTotalBanTime=1200`

### HTTP 서버 보안 옵션

#### tunnel.N.option.rejectInproxy (option.rejectInproxy)

- **유형**: Boolean
- **컨텍스트**: HTTP 서버에만 해당
- **기본값**: false
- **설명**: inproxy(인바운드 프록시)를 통해 온 것으로 보이는 연결을 거부합니다
- **예시**: `option.rejectInproxy=false`

#### tunnel.N.option.rejectReferer (option.rejectReferer)

- **유형**: 불리언
- **컨텍스트**: HTTP 서버 전용
- **기본값**: false
- **도입**: 버전 0.9.25
- **설명**: Referer 헤더가 있는 연결을 거부합니다
- **예시**: `option.rejectReferer=false`

#### tunnel.N.option.rejectUserAgents (option.rejectUserAgents)

- **유형**: 불리언
- **컨텍스트**: HTTP 서버에만 해당
- **기본값**: false
- **도입 버전**: 0.9.25
- **요구 사항**: `userAgentRejectList` 속성
- **설명**: User-Agent가 일치하는 연결을 거부합니다
- **예**: `option.rejectUserAgents=false`

#### tunnel.N.option.userAgentRejectList (option.userAgentRejectList)

- **유형**: 문자열(쉼표로 구분된 일치 문자열)
- **컨텍스트**: HTTP 서버에서만
- **도입**: 버전 0.9.25
- **대소문자**: 대소문자 구분 일치
- **특이사항**: "none"(0.9.33부터) 는 빈 User-Agent와 일치
- **설명**: 거부할 User-Agent 패턴 목록
- **예시**: `option.userAgentRejectList=Mozilla,Opera,none`

### IRC 서버 옵션

#### tunnel.N.option.ircserver.fakeHostname (option.ircserver.fakeHostname)

- **유형**: 문자열 (hostname 패턴)
- **컨텍스트**: IRC 서버 전용
- **기본값**: `%f.b32.i2p`
- **토큰**:
  - `%f` = 전체 base32 destination(목적지) 해시
  - `%c` = 클로킹된 destination 해시 (cloakKey 참조)
- **설명**: IRC 서버로 전송되는 호스트명 형식
- **예시**: `option.ircserver.fakeHostname=%c.irc.i2p`

#### tunnel.N.option.ircserver.cloakKey (option.ircserver.cloakKey)

- **유형**: 문자열(패스프레이즈)
- **컨텍스트**: IRC 서버에만 해당
- **기본값**: 세션마다 무작위
- **제한 사항**: 따옴표 또는 공백 사용 금지
- **설명**: 일관된 호스트명 클로킹을 위한 패스프레이즈
- **사용 사례**: 재시작/서버 간 지속적인 사용자 추적
- **예**: `option.ircserver.cloakKey=mysecretkey`

#### tunnel.N.option.ircserver.method (option.ircserver.method)

- **유형**: Enum(열거형)
- **컨텍스트**: IRC 서버 전용
- **기본값**: user
- **값**: `user`, `webirc`
- **설명**: IRC 서버용 인증 방법
- **예시**: `option.ircserver.method=webirc`

#### tunnel.N.option.ircserver.webircPassword (option.ircserver.webircPassword)

- **유형**: 문자열(비밀번호)
- **대상**: IRC 서버 전용
- **필수 조건**: `method=webirc`
- **제한 사항**: 따옴표 또는 공백 금지
- **설명**: WEBIRC 프로토콜(웹 기반 IRC 클라이언트를 위한 프록시 연동 프로토콜) 인증용 비밀번호
- **예시**: `option.ircserver.webircPassword=webircpass`

#### tunnel.N.option.ircserver.webircSpoofIP (option.ircserver.webircSpoofIP)

- **유형**: 문자열 (IP 주소)
- **적용 대상**: IRC 서버 전용
- **필요 조건**: `method=webirc`
- **설명**: WEBIRC protocol(웹 IRC 프록시 인증 프로토콜)에서 사용할 스푸핑된 IP 주소
- **예시**: `option.ircserver.webircSpoofIP=10.0.0.1`

### SSL/TLS 구성

#### tunnel.N.option.useSSL (option.useSSL)

- **유형**: Boolean
- **기본값**: false
- **적용 범위**: 모든 tunnel
- **동작**:
  - **서버**: 로컬 서버와의 연결에 SSL 사용
  - **클라이언트**: 로컬 클라이언트의 SSL 사용을 요구
- **예**: `option.useSSL=false`

#### tunnel.N.option.keystoreFile (option.keystoreFile)

- **유형**: 문자열 (파일 경로)
- **컨텍스트**: 클라이언트 tunnel 전용
- **기본값**: `i2ptunnel-(random).ks`
- **경로**: 절대 경로가 아니면 `$(I2P_CONFIG_DIR)/keystore/` 기준 상대 경로
- **자동 생성**: 존재하지 않으면 생성됨
- **설명**: SSL 개인 키를 포함하는 키 저장소(keystore) 파일
- **예시**: `option.keystoreFile=my-tunnel.ks`

#### tunnel.N.option.keystorePassword (option.keystorePassword)

- **유형**: String (비밀번호)
- **컨텍스트**: 클라이언트 tunnels 전용
- **기본값**: changeit
- **자동 생성**: 새 키스토어가 생성되면 무작위 비밀번호
- **설명**: SSL 키스토어의 비밀번호
- **예제**: `option.keystorePassword=secretpassword`

#### tunnel.N.option.keyAlias (option.keyAlias)

- **유형**: String (별칭)
- **컨텍스트**: 클라이언트 tunnel 전용
- **자동 생성**: 새 키가 생성되면 자동으로 생성됨
- **설명**: 키 저장소(keystore)의 개인 키에 대한 별칭
- **예시**: `option.keyAlias=mytunnel-key`

#### tunnel.N.option.keyPassword (option.keyPassword)

- **유형**: 문자열(비밀번호)
- **컨텍스트**: 클라이언트 tunnels 전용
- **자동 생성**: 새 키를 생성하면 임의의 비밀번호가 생성됨
- **설명**: keystore(키 저장소)에 있는 개인 키의 비밀번호
- **예**: `option.keyPassword=keypass123`

### 일반 I2CP 및 스트리밍 옵션

모든 `tunnel.N.option.*` 속성(위에서 명시적으로 문서화되지 않은)은 `tunnel.N.option.` 접두사를 제거한 상태로 I2CP 인터페이스와 스트리밍 라이브러리로 그대로 전달됩니다.

**중요**: 이는 I2PTunnel 전용 옵션과는 별개입니다. 참조: - [I2CP 명세서](/docs/specs/i2cp/) - [스트리밍 라이브러리 명세서](/docs/specs/streaming/)

스트리밍 옵션 예시:

```properties
option.i2cp.messageReliability=BestEffort
option.i2p.streaming.connectDelay=1000
option.i2p.streaming.maxWindowSize=128
```
### 완전한 Tunnel 예제

```properties
# HTTP Proxy (split format without tunnel.N. prefix)
name=I2P HTTP Proxy
description=HTTP proxy for accessing I2P sites and outproxy
type=httpclient
interface=127.0.0.1
listenPort=4444
targetDestination=
sharedClient=true
startOnLoad=true

# I2CP configuration
i2cpHost=127.0.0.1
i2cpPort=7654

# HTTP client options
option.i2ptunnel.httpclient.allowInternalSSL=false
option.i2ptunnel.httpclient.disableAddressHelper=false
option.i2ptunnel.httpclient.jumpServers=http://stats.i2p/cgi-bin/jump.cgi
option.i2ptunnel.httpclient.sendAccept=false
option.i2ptunnel.httpclient.sendReferer=false
option.i2ptunnel.httpclient.sendUserAgent=false

# Proxy authentication
option.proxyAuth=false

# Outproxy configuration
option.i2ptunnel.httpclient.SSLOutproxies=false.i2p
proxyList=false.i2p

# Client behavior
option.persistentClientKey=false
option.i2cp.delayOpen=false

# I2CP tunnel options
option.inbound.length=3
option.outbound.length=3
option.inbound.quantity=2
option.outbound.quantity=2
```
---

## 버전 이력 및 기능 연대표

### 버전 0.9.10 (2013)

**Feature**: 구성 파일에서 빈 값 지원 - 빈 값을 가진 키(`key=`)가 이제 지원됩니다 - 이전에는 무시되거나 구문 분석 오류를 일으켰습니다

### 버전 0.9.18 (2015)

**기능**: 로거 플러시 간격 설정 - 속성: `logger.flushInterval` (기본값 29초) - 허용 가능한 로그 지연을 유지하면서 디스크 I/O를 줄입니다

### 버전 0.9.23 (2015년 11월)

**주요 변경**: Java 7이 최소 요구 사항 - Java 6 지원 종료 - 지속적인 보안 업데이트를 받기 위해 필요

### 버전 0.9.25 (2015)

**기능**: HTTP 서버 보안 옵션 - `tunnel.N.option.rejectReferer` - Referer 헤더가 있는 연결 거부 - `tunnel.N.option.rejectUserAgents` - 특정 User-Agent 헤더 거부 - `tunnel.N.option.userAgentRejectList` - 거부할 User-Agent 패턴 - **사용 사례**: 크롤러 및 원치 않는 클라이언트 차단

### 버전 0.9.33 (2018년 1월)

**기능**: 향상된 User-Agent(사용자 에이전트) 필터링 - `userAgentRejectList` 문자열 "none"은 빈 User-Agent와 일치 - i2psnark, i2ptunnel, streaming, SusiMail에 대한 추가 버그 수정

### 버전 0.9.41 (2019)

**사용 중단**: Android에서 BOB Protocol이 제거됨 - Android 사용자는 SAM 또는 I2CP로 마이그레이션해야 합니다

### 버전 0.9.42 (2019년 8월)

**주요 변경**: 구성 파일 분리 - `clients.config`를 `clients.config.d/` 디렉터리 구조로 분리 - `i2ptunnel.config`를 `i2ptunnel.config.d/` 디렉터리 구조로 분리 - 업그레이드 후 첫 실행 시 자동 마이그레이션 - 모듈식 패키징 및 플러그인 관리를 가능하게 함 - 기존 monolithic(단일형) 형식도 계속 지원

**추가 기능**: - SSU 성능 개선 - 교차 네트워크 연결 방지 (Proposal 147) - 초기 암호화 유형 지원

### 버전 0.9.56 (2021)

**기능**: 보안 및 로깅 개선 - `logger.gzip` - 로테이션된 로그에 대한 Gzip 압축 (기본값: false) - `logger.minGzipSize` - 압축 최소 크기 (기본값: 65536 바이트) - `tunnel.N.option.proxy.auth.USER.sha256` - SHA-256 다이제스트 인증 (RFC 7616) - **보안**: 다이제스트 인증에서 MD5가 SHA-256으로 대체됨

### 버전 0.9.57 (2023년 1월)

**기능**: SOCKS outproxy(외부 프록시) 유형 구성 - `tunnel.N.option.outproxyType` - outproxy 유형 선택 (socks|connect) - 기본값: socks - HTTPS outproxies에 대한 HTTPS CONNECT 지원

### 버전 2.6.0 (2024년 7월)

**파괴적 변경**: I2P-over-Tor 차단됨 - Tor 출구 노드 IP 주소에서 오는 연결은 이제 거부됩니다 - **이유**: I2P 성능을 저하시키고 Tor 출구 노드 리소스를 낭비함 - **영향**: Tor 출구 노드를 통해 I2P에 접근하는 사용자는 차단됩니다 - 출구가 아닌 릴레이와 Tor 클라이언트에는 영향이 없습니다

### 버전 2.10.0 (2025년 9월 - 현재)


**구성**: 새로운 구성 속성이 추가되지 않았습니다

**중요한 예정 변경 사항**: 다음 릴리스(아마 2.11.0 또는 3.0.0)는 Java 17 이상이 필요합니다

---

## 사용 중단 및 호환성 파괴 변경

### 중대한 사용 중단 사항

#### I2P-over-Tor 접속 (버전 2.6.0+)

- **상태**: 2024년 7월부터 차단됨
- **영향**: Tor 출구 노드 IP에서 오는 연결이 거부됨
- **이유**: 익명성 이점 없이 I2P 네트워크 성능을 저하시킴
- **대상**: Tor 출구 노드만 해당되며, 릴레이나 일반 Tor 클라이언트는 해당되지 않음
- **대안**: I2P 또는 Tor를 별도로 사용하고, 결합하지 말 것

#### MD5 다이제스트 인증

- **상태**: 사용 중단됨 (SHA-256 사용)
- **속성**: `tunnel.N.option.proxy.auth.USER.md5`
- **이유**: MD5는 암호학적으로 안전하지 않음
- **대체**: `tunnel.N.option.proxy.auth.USER.sha256` (0.9.56부터)
- **현황**: MD5는 여전히 지원되지만 권장되지 않음

### 구성 아키텍처 변경 사항

#### 모놀리식 구성 파일(버전 0.9.42+)

- **영향 대상**: `clients.config`, `i2ptunnel.config`
- **상태**: 분할된 디렉터리 구조를 채택함에 따라 사용 중단됨
- **마이그레이션**: 0.9.42로 업그레이드 후 첫 실행 시 자동
- **호환성**: 레거시 형식도 계속 작동함(하위 호환)
- **권장 사항**: 새 구성에는 분할 형식 사용 권장

### Java 버전 요구사항

#### Java 6 지원

- **종료됨**: 버전 0.9.23 (2015년 11월)
- **최소**: 0.9.23부터 Java 7 필요

#### Java 17 요구 사항 (예정)

- **상태**: 중대한 예정 변경
- **목표**: 2.10.0 이후 다음 메이저 릴리스(가능성: 2.11.0 또는 3.0.0)
- **현재 최소 요구 버전**: Java 8
- **조치 필요**: Java 17로 마이그레이션을 준비
- **일정**: 릴리스 노트와 함께 공지 예정

### 제거된 기능

#### BOB 프로토콜(안드로이드)

- **제거됨**: 버전 0.9.41
- **플랫폼**: Android 전용
- **대안**: SAM 또는 I2CP 프로토콜
- **데스크톱**: 데스크톱 플랫폼에서는 여전히 BOB을 사용할 수 있음

### 권장 마이그레이션

1. **인증**: MD5에서 SHA-256 다이제스트 인증으로 마이그레이션
2. **구성 형식**: 클라이언트와 tunnels를 위한 분리된 디렉터리 구조로 마이그레이션
3. **Java 런타임**: 다음 메이저 릴리스 이전에 Java 17 업그레이드를 계획
4. **Tor 통합**: Tor 종료 노드(Exit node)를 통해 I2P를 라우팅하지 말 것

---

## 참고 자료

### 공식 문서

- [I2P 설정 명세](/docs/specs/configuration/) - 공식 설정 파일 형식 명세
- [I2P 플러그인 명세](/docs/specs/plugin/) - 플러그인 설정 및 패키징
- [I2P 공통 구조 - 타입 매핑](/docs/specs/common-structures/#type-mapping) - 프로토콜 데이터 직렬화 형식
- [Java Properties 형식](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) - 기본 형식 명세

### 소스 코드

- [I2P Java Router 저장소](https://github.com/i2p/i2p.i2p) - GitHub 미러
- [I2P 개발자 Gitea](https://i2pgit.org/I2P_Developers/i2p.i2p) - 공식 I2P 소스 저장소
- [DataHelper.java](https://github.com/i2p/i2p.i2p/blob/master/core/java/src/net/i2p/data/DataHelper.java) - 구성 파일 I/O 구현

### 커뮤니티 자료

- [I2P Forum](https://i2pforum.net/) - 활발한 커뮤니티 토론과 지원
- [I2P Website](/) - 공식 프로젝트 웹사이트

### API 문서

- [DataHelper JavaDoc](https://i2pplus.github.io/javadoc/net/i2p/data/DataHelper.html) - 설정 파일 메서드용 API 문서

### 명세 상태

- **최신 명세 업데이트**: 2023년 1월 (버전 0.9.57)
- **현재 I2P 버전**: 2.10.0 (2025년 9월)
- **기술적 정확성**: 명세는 2.10.0까지 유효함(호환성을 깨는 변경 사항 없음)
- **유지 관리**: 구성 형식이 수정될 때 업데이트되는 living document(수시로 갱신되는 문서)
