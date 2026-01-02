---
title: "플러그인 패키지 형식"
description: "I2P 플러그인을 위한 .xpi2p / .su3 패키징 규칙"
slug: "plugin"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## 개요

I2P 플러그인은 router 기능을 확장하는 서명된 아카이브입니다. 이들은 `.xpi2p` 또는 `.su3` 파일 형태로 배포되며, `~/.i2p/plugins/<name>/`(Windows에서는 `%APPDIR%\I2P\plugins\<name>\`)에 설치되고, 샌드박싱 없이 router의 전체 권한으로 실행됩니다.

### 지원되는 플러그인 유형

- 콘솔 웹앱
- cgi-bin, webapps가 포함된 새로운 eepsites
- 콘솔 테마
- 콘솔 번역
- Java 프로그램(프로세스 내 또는 별도의 JVM)
- 셸 스크립트 및 네이티브 바이너리

### 보안 모델

**중요:** 플러그인은 I2P router와 동일한 권한으로 동일한 JVM에서 실행됩니다. 다음에 무제한으로 접근할 수 있습니다: - 파일 시스템(읽기 및 쓰기) - router API 및 내부 상태 - 네트워크 연결 - 외부 프로그램 실행

플러그인은 완전히 신뢰할 수 있는 코드로 취급해야 합니다. 사용자는 설치 전에 플러그인의 출처와 서명을 검증해야 합니다.

---

## 파일 형식

### SU3 형식(강력히 권장)

**상태:** 활성, I2P 0.9.15 (2014년 9월)부터 권장 형식

`.su3` 형식은 다음을 제공합니다: - **RSA-4096 서명 키** (xpi2p의 DSA-1024와 비교) - 서명은 파일 헤더에 저장 - 매직 넘버: `I2Psu3` - 더 나은 전방 호환성

**구조:**

```
[SU3 Header with RSA-4096 signature]
[ZIP Archive]
  ├── plugin.config (required)
  ├── console/
  ├── lib/
  ├── webapps/
  └── [other plugin files]
```
### XPI2P 형식 (레거시, 사용 중단됨)

**상태:** 하위 호환성을 위해 지원되지만, 새 플러그인에는 권장되지 않습니다

`.xpi2p` 형식은 오래된 암호학적 서명을 사용합니다: - **DSA-1024 서명**(DSA: 디지털 서명 알고리즘 1024비트) (NIST-800-57(미국표준기술연구소 지침)에 따라 더 이상 권장되지 않음) - ZIP 앞에 40바이트 DSA 서명이 붙음 - plugin.config에 `key` 필드가 필요함

**구조:**

```
[40-byte DSA signature]
[16-byte version string (UTF-8, zero-padded)]
[ZIP Archive]
```
**마이그레이션 경로:** xpi2p(구형 업데이트 형식)에서 su3(서명된 업데이트 파일 형식)로 마이그레이션하는 전환 기간에는 `updateURL`과 `updateURL.su3`를 모두 제공하십시오. 최신 router(0.9.15+)는 SU3를 자동으로 우선시합니다.

---

## 아카이브 구조 및 plugin.config

### 필수 파일

**plugin.config** - 키-값 쌍을 사용하는 표준 I2P 구성 파일

### 필수 속성

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Installation directory name, must match for updates</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Alphanumeric, no spaces</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>signer</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Developer contact information</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>user@mail.i2p</code> format recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>version</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Plugin version for update comparison</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Max 16 bytes, parsed by VersionComparator</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>key</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA public key (172 B64 chars ending with '=')</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Omit for SU3 format</strong></td></tr>
  </tbody>
</table>
**버전 형식 예시:** - `1.2.3` - `1.2.3-4` - `2.0.0-beta.1`

허용되는 구분자: `.` (점), `-` (하이픈), `_` (밑줄)

### 선택적 메타데이터 속성

#### 정보 표시

- `date` - 릴리스 날짜 (Java long 타임스탬프)
- `author` - 개발자 이름 (`user@mail.i2p` 권장)
- `description` - 영어 설명
- `description_xx` - 현지화된 설명 (xx = 언어 코드)
- `websiteURL` - 플러그인 홈페이지 (`http://foo.i2p/`)
- `license` - 라이선스 식별자 (예: "Apache-2.0", "GPL-3.0")

#### 업데이트 설정

- `updateURL` - XPI2P 업데이트 위치 (레거시)
- `updateURL.su3` - SU3 업데이트 위치 (권장)
- `min-i2p-version` - 최소 필요 I2P 버전
- `max-i2p-version` - 호환되는 최대 I2P 버전
- `min-java-version` - 최소 Java 버전 (예: `1.7`, `17`)
- `min-jetty-version` - 최소 Jetty 버전 (Jetty 6+의 경우 `6` 사용)
- `max-jetty-version` - 최대 Jetty 버전 (Jetty 5의 경우 `5.99999` 사용)

#### 설치 동작

- `dont-start-at-install` - 기본값 `false`. `true`인 경우 수동으로 시작해야 함
- `router-restart-required` - 기본값 `false`. 업데이트 후 재시작이 필요함을 사용자에게 알림
- `update-only` - 기본값 `false`. 플러그인이 이미 설치되어 있지 않으면 실패
- `install-only` - 기본값 `false`. 플러그인이 이미 존재하면 실패
- `min-installed-version` - 업데이트에 필요한 최소 설치 버전
- `max-installed-version` - 업데이트 가능한 최대 설치 버전
- `disableStop` - 기본값 `false`. `true`인 경우 중지 버튼을 숨김

#### 콘솔 통합

- `consoleLinkName` - 콘솔 요약 표시줄 링크에 표시할 텍스트
- `consoleLinkName_xx` - 현지화된 링크 텍스트 (xx = 언어 코드)
- `consoleLinkURL` - 링크 대상 (예: `/appname/index.jsp`)
- `consoleLinkTooltip` - 마우스오버 텍스트 (0.7.12-6부터 지원)
- `consoleLinkTooltip_xx` - 현지화된 툴팁
- `console-icon` - 32x32 아이콘의 경로 (0.9.20부터 지원)
- `icon-code` - 웹 리소스가 없는 플러그인을 위한 Base64로 인코딩된 32x32 PNG (0.9.25부터)

#### 플랫폼 요구 사항(표시 전용)

- `required-platform-OS` - 운영 체제 요구 사항(강제되지 않음)
- `other-requirements` - 추가 요구 사항(예: "Python 3.8+")

#### 의존성 관리 (미구현)

- `depends` - 쉼표로 구분된 플러그인 의존성
- `depends-version` - 의존성에 대한 버전 요구 사항
- `langs` - 언어 팩 내용
- `type` - 플러그인 유형 (app/theme/locale/webapp)

### 업데이트 URL 변수 치환

**기능 상태:** I2P 1.7.0 (0.9.53)부터 사용 가능

`updateURL` 및 `updateURL.su3` 모두 플랫폼별 변수를 지원합니다:

**변수:** - `$OS` - 운영 체제: `windows`, `linux`, `mac` - `$ARCH` - 아키텍처: `386`, `amd64`, `arm64`

**예시:**

```properties
updateURL.su3=http://foo.i2p/downloads/foo-$OS-$ARCH.su3
```
**Windows AMD64에서의 결과:**

```
http://foo.i2p/downloads/foo-windows-amd64.su3
```
이는 플랫폼별 빌드에서 단일 plugin.config 파일을 사용할 수 있게 합니다.

---

## 디렉터리 구조

### 표준 레이아웃

```
plugins/
└── pluginname/
    ├── plugin.config (required)
    ├── console/
    │   ├── locale/          # Translation JARs
    │   ├── themes/          # Console themes
    │   ├── webapps/         # Web applications
    │   └── webapps.config   # Webapp configuration
    ├── eepsite/
    │   ├── cgi-bin/
    │   ├── docroot/
    │   ├── logs/
    │   ├── webapps/
    │   └── jetty.xml
    ├── lib/
    │   └── *.jar            # Plugin libraries
    └── clients.config       # Client startup configuration
```
### 디렉터리의 목적

**console/locale/** - I2P 기본 번역을 위한 리소스 번들이 포함된 JAR 파일 - 플러그인별 번역은 `console/webapps/*.war` 또는 `lib/*.jar`에 있어야 합니다

**console/themes/** - 각 하위 디렉터리에는 완전한 콘솔 테마가 들어 있습니다 - 테마 검색 경로에 자동으로 추가됩니다

**console/webapps/** - 콘솔 통합용 `.war` 파일 - `webapps.config`에서 비활성화하지 않으면 자동으로 시작됨 - WAR 이름은 플러그인 이름과 일치할 필요가 없음

**eepsite/** - 자체 Jetty 인스턴스를 갖춘 완전한 eepsite - 변수 치환을 사용하는 `jetty.xml` 구성 필요 - zzzot 및 pebble 플러그인 예제 참고

**lib/** - 플러그인 JAR 라이브러리 - `clients.config` 또는 `webapps.config`를 통해 classpath에 지정합니다

---

## 웹앱 구성

### webapps.config 형식

웹앱의 동작을 제어하는 표준 I2P 구성 파일.

**구문:**

```properties
# Disable autostart
webapps.warname.startOnLoad=false

# Add classpath JARs (as of API 0.9.53, works for any warname)
webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar
```
**중요 사항:** - router 0.7.12-9 이전에는 호환성을 위해 `plugin.warname.startOnLoad`를 사용하세요 - API 0.9.53 이전에는 클래스패스는 warname이 플러그인 이름과 일치할 때만 동작했습니다 - 0.9.53+부터는 클래스패스가 어떤 웹앱 이름에서도 동작합니다

### 웹앱 모범 사례

1. **ServletContextListener(서블릿 컨텍스트 리스너) 구현**
   - 정리를 위해 `javax.servlet.ServletContextListener`를 구현
   - 또는 서블릿에서 `destroy()`를 재정의
   - 업데이트 진행 중 및 router 중지 시 올바르게 종료되도록 보장

2. **라이브러리 관리**
   - 공유 JAR 파일은 `lib/`에 두고, WAR 내부에는 넣지 마세요
   - `webapps.config` 클래스패스를 통해 참조
   - 플러그인을 별도로 설치/업데이트할 수 있게 함

3. **충돌하는 라이브러리를 피하십시오**
   - Jetty, Tomcat 또는 서블릿 JAR은 절대 번들하지 마십시오
   - 표준 I2P 설치에 포함된 JAR은 절대 번들하지 마십시오
   - 표준 라이브러리에 대해서는 classpath 섹션을 확인하십시오

4. **컴파일 요구 사항**
   - `.java` 또는 `.jsp` 소스 파일을 포함하지 마십시오
   - 시작 지연을 피하기 위해 모든 JSP를 사전 컴파일하십시오
   - Java/JSP 컴파일러가 사용 가능한 환경이라고 가정할 수 없습니다

5. **서블릿 API 호환성**
   - I2P는 서블릿 3.0을 지원합니다 (0.9.30부터)
   - **애너테이션 스캐닝은 지원되지 않습니다** (@WebContent)
   - 기존의 `web.xml` 배포 서술자를 제공해야 합니다

6. **Jetty(자바 서블릿 컨테이너) 버전**
   - 현재: Jetty 9 (I2P 0.9.30+)
   - 추상화를 위해 `net.i2p.jetty.JettyStart`를 사용합니다
   - Jetty API 변경으로부터 보호합니다

---

## 클라이언트 구성

### clients.config 형식

플러그인과 함께 시작되는 클라이언트(서비스)를 정의합니다.

**기본 클라이언트:**

```properties
clientApp.0.main=com.example.PluginMain
clientApp.0.name=Example Plugin Service
clientApp.0.delay=30
clientApp.0.args=arg1 arg2 $PLUGIN/config.properties
```
**중지/제거 기능이 있는 클라이언트:**

```properties
clientApp.0.stopargs=stop
clientApp.0.uninstallargs=uninstall
clientApp.0.classpath=$PLUGIN/lib/plugin.jar,$I2P/lib/i2p.jar
```
### 속성 참조

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>main</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fully qualified class name implementing ClientApp interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Display name for user interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>delay</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Startup delay in seconds (default: 0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>args</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Space-separated arguments passed to constructor</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>stopargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments for shutdown (must handle gracefully)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>uninstallargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments called before plugin deletion</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>classpath</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated JAR paths</td></tr>
  </tbody>
</table>
### 변수 치환

다음 변수들은 `args`, `stopargs`, `uninstallargs`, 그리고 `classpath`에서 치환됩니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Replacement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$I2P</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P base installation directory</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$CONFIG</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P configuration directory (typically <code>~/.i2p</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$PLUGIN</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">This plugin's directory (<code>$CONFIG/plugins/name</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$OS</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Operating system: <code>windows</code>, <code>linux</code>, <code>mac</code></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$ARCH</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Architecture: <code>386</code>, <code>amd64</code>, <code>arm64</code></td></tr>
  </tbody>
</table>
### 관리형 vs. 비관리형 클라이언트

**관리형 클라이언트(권장, 0.9.4부터):** - ClientAppManager에 의해 인스턴스화됨 - 참조를 보유하고 상태를 추적함 - 라이프사이클 관리가 더 용이함 - 더 나은 메모리 관리

**비관리형 클라이언트:** - router에 의해 시작되며, 상태 추적 없음 - 여러 번의 start/stop 호출을 원활하게 처리해야 함 - 조정을 위해 정적 상태 또는 PID 파일을 사용 - router 종료 시 호출됨 (0.7.12-3 기준)

### ShellService(셸 서비스) (0.9.53 / 1.7.0부터)

자동 상태 추적을 지원하는 외부 프로그램 실행용 일반화된 솔루션.

**기능:** - 프로세스 수명 주기 관리 - ClientAppManager와 통신 - 자동 PID 관리 - 크로스 플랫폼 지원

**사용법:**

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myservice.sh
```
플랫폼별 스크립트의 경우:

```properties
clientApp.0.args=$PLUGIN/bin/myservice-$OS.$ARCH
```
**대안(레거시):** OS 유형을 확인하는 Java 래퍼를 작성하고, 적절한 `.bat` 또는 `.sh` 파일과 함께 `ShellCommand`를 호출합니다.

---

## 설치 절차

### 사용자 설치 흐름

1. 사용자가 플러그인 URL을 Router 콘솔 플러그인 구성 페이지(`/configplugins`)에 붙여넣기
2. Router가 플러그인 파일 다운로드
3. 서명 검증(키가 알려지지 않았고 엄격 모드가 활성화된 경우 실패)
4. ZIP 무결성 검사
5. `plugin.config` 압축 해제 및 파싱
6. 버전 호환성 검증(`min-i2p-version`, `min-java-version` 등)
7. 웹앱 이름 충돌 감지
8. 업데이트인 경우 기존 플러그인 중지
9. 디렉터리 유효성 검사(`plugins/` 하위여야 함)
10. 모든 파일을 플러그인 디렉터리로 압축 해제
11. `plugins.config` 업데이트
12. 플러그인 시작(`dont-start-at-install=true`가 아닌 경우)

### 보안과 신뢰

**키 관리:** - 신규 서명자를 위한 First-key-seen 신뢰 모델(처음 본 키를 신뢰하는 모델) - jrandom 및 zzz 키만 미리 번들됨 - 0.9.14.1 기준으로, 기본적으로 알 수 없는 키는 거부됨 - 개발을 위해 고급 속성으로 재정의 가능

**설치 제한 사항:** - 아카이브는 플러그인 디렉터리에만 압축이 풀려야 함 - 설치 프로그램은 `plugins/` 바깥 경로를 거부함 - 설치 후 플러그인은 다른 위치의 파일에 접근할 수 있음 - sandboxing(샌드박싱)이나 권한 분리 없음

---

## 업데이트 메커니즘

### 업데이트 확인 절차

1. Router가 plugin.config에서 `updateURL.su3`(권장) 또는 `updateURL`을 읽습니다
2. 바이트 41-56을 가져오기 위해 HTTP HEAD 또는 부분 GET 요청을 수행합니다
3. 원격 파일에서 버전 문자열을 추출합니다
4. VersionComparator를 사용하여 설치된 버전과 비교합니다
5. 더 최신이면 설정에 따라 사용자에게 확인을 요청하거나 자동으로 다운로드합니다
6. 플러그인을 중지합니다
7. 업데이트를 설치합니다
8. 사용자 기본 설정이 변경되지 않았다면 플러그인을 시작합니다

### 버전 비교

버전은 점/대시/밑줄로 구분된 구성 요소로 해석됩니다: - `1.2.3` < `1.2.4` - `1.2.3` < `1.2.3-1` - `2.0.0` > `1.9.9`

**최대 길이:** 16바이트 (SUD/SU3 헤더와 일치해야 함)

### 업데이트 모범 사례

1. 릴리스에서는 항상 버전을 증가시키기
2. 이전 버전에서 업데이트 경로를 테스트하기
3. 주요 변경 사항에 대해 `router-restart-required`를 고려하기
4. 마이그레이션 중에는 `updateURL`과 `updateURL.su3`를 모두 제공하기
5. 테스트용으로 빌드 번호 접미사 사용하기 (`1.2.3-456`)

---

## 클래스패스와 표준 라이브러리

### 클래스패스에서 항상 사용 가능

I2P 0.9.30+에서는 `$I2P/lib`의 다음 JAR 파일들이 항상 classpath(클래스패스)에 포함됩니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Plugin Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Required for all plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>mstreaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>streaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming implementation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2ptunnel.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP/server plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>router.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Router internals</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed, avoid if possible</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>javax.servlet.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet 3.1, JSP 2.3 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with servlets/JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jasper-runtime.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper compiler/runtime</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>commons-el.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">EL 3.0 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSPs using expression language</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jetty-i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty utilities</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins starting Jetty</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>org.mortbay.jetty.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty 9 base</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Custom Jetty instances</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>sam.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>addressbook.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription/blockfile</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Use NamingService instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>routerconsole.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Not public API, avoid</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jbigi.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Native crypto</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>systray.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">URL launcher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>wrapper.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Service wrapper</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
  </tbody>
</table>
### 특별 참고 사항

**commons-logging.jar:** - 0.9.30부터 비어 있음 - 0.9.30 이전: Apache Tomcat JULI - 0.9.24 이전: Commons Logging + JULI - 0.9 이전: Commons Logging만

**jasper-compiler.jar:** - Jetty 6 (0.9)부터 비어 있음

**systray4j.jar:** - 0.9.26에서 제거됨

### 클래스패스에 없음 (지정해야 함)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jstl.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>standard.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
  </tbody>
</table>
### 클래스패스 명세

**clients.config에서:**

```properties
clientApp.0.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/i2p.jar
```
**webapps.config에서:**

```properties
webapps.mywebapp.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/jstl.jar
```
**중요:** 0.7.13-3부터 classpaths(클래스패스)는 JVM 전역이 아니라 스레드별입니다. 각 클라이언트마다 전체 classpath를 지정하십시오.

---

## Java 버전 요구사항

### 현재 요구 사항 (2025년 10월)

**I2P 2.10.0 및 이전:** - 최소: Java 7 (0.9.24(2016년 1월)부터 필요) - 권장: Java 8 이상

**I2P 2.11.0 및 이후(예정):** - **최소 요구사항: Java 17+** (2.9.0 릴리스 노트에서 공지) - 두 릴리스에 걸친 사전 공지 제공 (2.9.0 → 2.10.0 → 2.11.0)

### 플러그인 호환성 전략

**최대 호환성을 위해 (I2P 2.10.x까지):**

```xml
<javac source="1.7" target="1.7" />
```
```properties
min-java-version=1.7
```
**Java 8+ 기능용:**

```xml
<javac source="1.8" target="1.8" />
```
```properties
min-java-version=1.8
```
**Java 11+ 기능의 경우:**

```xml
<javac source="11" target="11" />
```
```properties
min-java-version=11
```
**2.11.0+ 준비:**

```xml
<javac source="17" target="17" />
```
```properties
min-java-version=17
min-i2p-version=2.11.0
```
### 컴파일 모범 사례

**더 새로운 JDK로 구버전 타깃용으로 컴파일할 때:**

```xml
<javac source="1.7" target="1.7" 
       bootclasspath="${java7.home}/jre/lib/rt.jar"
       includeantruntime="false" />
```
대상 Java 버전에서 지원되지 않는 API 사용을 방지합니다.

---

## Pack200 압축 - 더 이상 사용되지 않음

### 중요 공지: Pack200을 사용하지 마십시오

**상태:** 사용 중단 및 제거됨

원래 사양에서는 60-65% 용량 감소를 위해 Pack200 압축을 강력히 권장했습니다. **이는 더 이상 유효하지 않습니다.**

**타임라인:** - **JEP 336:** Pack200은 Java 11에서 사용 중단으로 표시됨 (2018년 9월) - **JEP 367:** Pack200은 Java 14에서 제거됨 (2020년 3월)

**공식 I2P 업데이트 명세서는 다음과 같이 명시합니다:** > "zip 내의 JAR 및 WAR 파일은 위에서 'su2' 파일에 대해 문서화된 대로 pack200으로 더 이상 압축되지 않으며, 이는 최신 Java 런타임이 이를 더 이상 지원하지 않기 때문입니다."

**해야 할 일:**

1. **빌드 프로세스에서 pack200(자바 JAR 전용 압축 포맷)을 즉시 제거하십시오**
2. **표준 ZIP 압축을 사용하십시오**
3. **대안을 고려하십시오:**
   - 코드 축소를 위한 ProGuard/R8
   - 네이티브 바이너리용 UPX
   - 커스텀 언패커를 제공하는 경우 최신 압축 알고리즘(zstd, brotli)

**기존 플러그인용:** - 구형 routers(0.7.11-5부터 Java 10까지)는 여전히 pack200(자바 JAR 압축 형식)을 압축 해제할 수 있음 - 신형 routers(Java 11+)는 pack200을 압축 해제할 수 없음 - pack200 압축 없이 플러그인을 재배포하세요

---

## 서명 키와 보안

### 키 생성 (SU3 형식)

i2p.scripts 저장소의 `makeplugin.sh` 스크립트를 사용하세요:

```bash
# Generate new signing key
./makeplugin.sh keygen

# Keys stored in ~/.i2p-plugin-keys/
```
**주요 세부 사항:** - 알고리즘: RSA_SHA512_4096 - 형식: X.509 인증서 - 저장소: Java 키스토어 형식

### 플러그인 서명

```bash
# Create signed su3 file
./makeplugin.sh sign myplugin.zip myplugin.su3 keyname

# Verify signature
./makeplugin.sh verify myplugin.su3
```
### 키 관리 모범 사례

1. **한 번 생성하고, 영구적으로 보호**
   - Routers는 다른 키와 연결된 중복 키 이름을 거부합니다
   - Routers는 다른 키 이름과 연결된 중복 키를 거부합니다
   - 키/이름이 일치하지 않으면 업데이트가 거부됩니다

2. **안전한 보관**
   - keystore(키 저장소)를 안전하게 백업
   - 강력한 passphrase(문장형 비밀번호) 사용
   - 버전 관리 시스템에 절대 커밋하지 말 것

3. **키 회전**
   - 현재 아키텍처에서는 지원되지 않음
   - 장기적인 키 사용에 대한 계획 수립
   - 팀 개발을 위한 다중 서명 방식 고려

### 레거시 DSA 서명 (XPI2P)

**상태:** 작동하지만 구식임

xpi2p format에서 사용하는 DSA-1024 서명: - 40바이트 서명 - base64로 표현된 172자 길이의 공개 키 - NIST-800-57은 최소 (L=2048, N=224)를 권고 - I2P는 더 약한 (L=1024, N=160)을 사용

**권장 사항:** 대신 RSA-4096과 함께 SU3(서명된 업데이트 파일 형식)을 사용하십시오.

---

## 플러그인 개발 지침

### 필수 모범 사례

1. **문서화**
   - 설치 지침이 포함된 명확한 README 제공
   - 설정 옵션과 기본값 문서화
   - 각 릴리스마다 변경 로그 포함
   - 필요한 I2P/Java 버전 명시

2. **용량 최적화**
   - 필요한 파일만 포함
   - router JAR 파일은 절대 번들하지 않기
   - 설치 패키지와 업데이트 패키지 분리 (라이브러리는 lib/에)
   - ~~Pack200 압축 사용~~ **더 이상 사용하지 않음 - 표준 ZIP 사용**

3. **구성**
   - 런타임 중에는 `plugin.config`를 절대 수정하지 마십시오
   - 런타임 설정에는 별도의 구성 파일을 사용하십시오
   - 필요한 router 설정(SAM 포트, tunnels 등)을 문서화하십시오
   - 사용자의 기존 구성을 존중하십시오

4. **리소스 사용**
   - 과도한 기본 대역폭 소모를 피할 것
   - 합리적인 CPU 사용 한도를 구현할 것
   - 종료 시 리소스를 정리할 것
   - 적절한 경우 데몬 스레드를 사용할 것

5. **테스트**
   - 모든 플랫폼에서 설치/업그레이드/제거를 테스트
   - 이전 버전에서 업데이트를 테스트
   - 업데이트 중 웹앱 중지/재시작을 확인
   - 최소 지원 I2P 버전으로 테스트

6. **파일 시스템**
   - `$I2P`에 절대 쓰지 말 것(읽기 전용일 수 있음)
   - 런타임 데이터는 `$PLUGIN` 또는 `$CONFIG`에 저장할 것
   - 디렉터리 검색에는 `I2PAppContext`를 사용할 것
   - `$CWD` 위치를 가정하지 말 것

7. **호환성**
   - 표준 I2P 클래스를 중복 구현하지 마십시오
   - 필요하다면 클래스를 확장하되, 대체하지 마십시오
   - plugin.config에서 `min-i2p-version`, `min-jetty-version`을 확인하십시오
   - 구버전 I2P를 지원한다면 해당 버전으로 테스트하십시오

8. **종료 처리**
   - clients.config에 적절한 `stopargs`를 설정
   - shutdown hook(종료 훅) 등록: `I2PAppContext.addShutdownTask()`
   - 여러 차례의 시작/중지 호출을 원활하게 처리
   - 모든 스레드를 데몬 모드로 설정

9. **보안**
   - 모든 외부 입력을 검증하세요
   - `System.exit()`를 절대 호출하지 마세요
   - 사용자 프라이버시를 존중하세요
   - 보안 코딩 모범 사례를 따르세요

10. **라이선스**
    - 플러그인 라이선스를 명확히 명시
    - 번들된 라이브러리의 라이선스를 준수
    - 필요한 출처 표기를 포함
    - 요구되는 경우 소스 코드 접근을 제공

### 고급 고려사항

**시간대 처리:** - Router는 JVM 시간대를 UTC로 설정 - 사용자의 실제 시간대: `I2PAppContext` 속성 `i2p.systemTimeZone`

**디렉터리 발견:**

```java
// Plugin directory
String pluginDir = I2PAppContext.getGlobalContext()
    .getAppDir().getAbsolutePath() + "/plugins/" + pluginName;

// Or use $PLUGIN variable in clients.config args
```
**버전 번호 체계:** - 시맨틱 버저닝(major.minor.patch) 사용 - 테스트를 위해 빌드 번호 추가 (1.2.3-456) - 업데이트 시 버전이 단조 증가하도록 보장

**Router 클래스 액세스:** - 일반적으로 `router.jar`에 대한 종속성은 피하세요 - 대신 `i2p.jar`의 공개 API를 사용하세요 - 향후 I2P에서는 Router 클래스 액세스가 제한될 수 있습니다

**JVM 크래시 방지(과거 이슈):** - 0.7.13-3에서 수정됨 - 클래스 로더를 올바르게 사용 - 실행 중인 플러그인에서 JAR 업데이트를 피함 - 필요하다면 업데이트 시 재시작하도록 설계

---

## Eepsite 플러그인

### 개요

플러그인은 자체 Jetty(자바 기반 웹 서버)와 I2PTunnel 인스턴스를 포함한 완전한 eepsites를 제공할 수 있습니다.

### 아키텍처

**다음을 시도하지 마십시오:** - 기존 eepsite(익명 웹사이트)에 설치 - router의 기본 eepsite와 병합 - 단일 eepsite만 사용 가능하다고 가정

**대신:** - 새 I2PTunnel 인스턴스를 시작합니다(CLI 방식으로) - 새 Jetty 인스턴스를 시작합니다 - `clients.config`에서 둘 다 구성합니다

### 예제 구조

```
plugins/myeepsite/
├── plugin.config
├── clients.config          # Starts Jetty + I2PTunnel
├── eepsite/
│   ├── jetty.xml          # Requires variable substitution
│   ├── docroot/
│   ├── webapps/
│   └── logs/
└── lib/
    └── [dependencies]
```
### jetty.xml에서의 변수 치환

경로에는 `$PLUGIN` 변수를 사용하세요:

```xml
<Set name="resourceBase">$PLUGIN/eepsite/docroot</Set>
```
Router는 플러그인 시작 시 치환을 수행합니다.

### 예시

참조 구현: - **zzzot 플러그인** - 토렌트 트래커 - **pebble 플러그인** - 블로그 플랫폼

둘 다 zzz의 플러그인 페이지(I2P-internal, I2P 내부 전용)에서 이용할 수 있습니다.

---

## 콘솔 통합

### 요약 표시줄 링크

router 콘솔 요약 표시줄에 클릭 가능한 링크 추가:

```properties
consoleLinkName=My Plugin
consoleLinkURL=/myplugin/
consoleLinkTooltip=Open My Plugin Interface
```
현지화된 버전:

```properties
consoleLinkName_de=Mein Plugin
consoleLinkTooltip_de=Öffne Mein Plugin Schnittstelle
```
### 콘솔 아이콘

**이미지 파일(0.9.20부터):**

```properties
console-icon=/myicon.png
```
`consoleLinkURL`이 지정된 경우(0.9.53부터) 그 값을 기준으로 한 경로이며, 그렇지 않으면 웹앱 이름을 기준으로 한 경로입니다.

**내장 아이콘(0.9.25부터):**

```properties
icon-code=iVBORw0KGgoAAAANSUhEUgAAA...Base64EncodedPNG...
```
다음을 사용하여 생성:

```bash
base64 -w 0 icon-32x32.png
```
또는 Java:

```bash
java -cp i2p.jar net.i2p.data.Base64 encode icon.png
```
요구 사항: - 32x32 픽셀 - PNG 형식 - Base64로 인코딩(줄바꿈 없음)

---

## 국제화

### 번역 번들

**I2P 기본 번역용:** - JAR 파일을 `console/locale/`에 배치 - 기존 I2P 앱용 리소스 번들을 포함 - 이름 지정: `messages_xx.properties` (xx = 언어 코드)

**플러그인별 번역의 경우:** - `console/webapps/*.war`에 포함 - 또는 `lib/*.jar`에 포함 - 표준 Java ResourceBundle(리소스 번들) 방식을 사용

### plugin.config의 현지화된 문자열

```properties
description=My awesome plugin
description_de=Mein tolles Plugin
description_fr=Mon plugin génial
description_es=Mi plugin increíble
```
지원되는 필드: - `description_xx` - `consoleLinkName_xx` - `consoleLinkTooltip_xx`

### 콘솔 테마 번역

`console/themes/`에 있는 테마는 테마 검색 경로에 자동으로 추가됩니다.

---

## 플랫폼별 플러그인

### 별도 패키지 접근 방식

각 플랫폼별로 다른 플러그인 이름을 사용하세요:

```properties
# Windows package
name=myplugin-windows

# Linux package  
name=myplugin-linux

# macOS package
name=myplugin-mac
```
### 변수 치환 접근법

플랫폼 변수를 사용하는 단일 plugin.config:

```properties
name=myplugin
updateURL.su3=http://myplugin.i2p/downloads/myplugin-$OS-$ARCH.su3
```
clients.config에서:

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myapp-$OS-$ARCH
```
### 런타임 OS 감지

조건부 실행을 위한 Java 접근 방식:

```java
String os = System.getProperty("os.name").toLowerCase();
if (os.contains("win")) {
    // Windows-specific code
} else if (os.contains("nix") || os.contains("nux")) {
    // Linux-specific code
} else if (os.contains("mac")) {
    // macOS-specific code
}
```
---

## 문제 해결

### 일반적인 문제

**플러그인이 시작되지 않음:** 1. I2P 버전 호환성 확인 (`min-i2p-version`) 2. Java 버전 확인 (`min-java-version`) 3. router 로그에서 오류 확인 4. 필요한 모든 JAR 파일이 클래스패스에 있는지 확인

**웹앱에 접근할 수 없음:** 1. `webapps.config`에서 비활성화되어 있지 않은지 확인 2. Jetty 버전 호환성 확인 (`min-jetty-version`) 3. `web.xml`이 존재하는지 확인 (애노테이션 스캔은 지원되지 않음) 4. 충돌하는 웹앱 이름이 있는지 확인

**업데이트 실패:** 1. 버전 문자열이 증가했는지 확인 2. 서명이 서명 키와 일치하는지 확인 3. 플러그인 이름이 설치된 버전과 일치하는지 확인 4. `update-only`/`install-only` 설정을 검토

**외부 프로그램이 종료되지 않음:** 1. 자동 라이프사이클 관리를 위해 ShellService(자동 실행/중지 관리 서비스) 사용 2. 적절한 `stopargs` 처리 구현 3. PID 파일 정리 확인 4. 프로세스 종료 확인

### 디버그 로깅

router에서 디버그 로깅 활성화:

```
logger.record.net.i2p.router.web.ConfigPluginsHandler=DEBUG
```
로그를 확인하십시오:

```
~/.i2p/logs/log-router-0.txt
```
---

## 참고 정보

### 공식 명세

- [플러그인 사양](/docs/specs/plugin/)
- [구성 형식](/docs/specs/configuration/)
- [업데이트 사양](/docs/specs/updates/)
- [암호학](/docs/specs/cryptography/)

### I2P 버전 이력

**현재 릴리스:** - **I2P 2.10.0** (2025년 9월 8일)

**0.9.53 이후의 주요 릴리스:** - 2.10.0 (2025년 9월) - Java 17+ 발표 - 2.9.0 (2025년 6월) - Java 17+ 경고 - 2.8.0 (2024년 10월) - 포스트양자 암호 테스트 - 2.6.0 (2024년 5월) - I2P-over-Tor 차단 - 2.4.0 (2023년 12월) - NetDB 보안 개선 - 2.2.0 (2023년 3월) - 혼잡 제어 - 2.1.0 (2023년 1월) - 네트워크 개선 - 2.0.0 (2022년 11월) - SSU2 전송 프로토콜 - 1.7.0/0.9.53 (2022년 2월) - ShellService, 변수 치환 - 0.9.15 (2014년 9월) - SU3 형식 도입

**버전 번호 체계:** - 0.9.x 시리즈: 0.9.53 버전까지 - 2.x 시리즈: 2.0.0부터 (SSU2 도입)

### 개발자 리소스

**소스 코드:** - 메인 저장소: https://i2pgit.org/I2P_Developers/i2p.i2p - GitHub 미러: https://github.com/i2p/i2p.i2p

**플러그인 예시:** - zzzot (BitTorrent 트래커) - pebble (블로그 플랫폼) - i2p-bote (서버리스 이메일) - orchid (Tor 클라이언트) - seedless (피어 교환)

**빌드 도구:** - makeplugin.sh - 키 생성 및 서명 - i2p.scripts 저장소에 있음 - su3(서명된 업데이트 파일 형식) 생성 및 검증을 자동화

### 커뮤니티 지원

**포럼:** - [I2P Forum](https://i2pforum.net/) - [zzz.i2p](http://zzz.i2p/) (I2P 내부)

**IRC/채팅:** - OFTC의 #i2p-dev - 네트워크 내 I2P IRC

---

## 부록 A: 전체 plugin.config 예제

```properties
# Required fields
name=example-plugin
signer=developer@mail.i2p
version=1.2.3

# Update configuration
updateURL.su3=http://example.i2p/plugins/example-$OS-$ARCH.su3
min-i2p-version=2.0.0
min-java-version=17

# Display information
date=1698796800000
author=Example Developer <developer@mail.i2p>
websiteURL=http://example.i2p/
license=Apache-2.0

description=An example I2P plugin demonstrating best practices
description_de=Ein Beispiel-I2P-Plugin zur Demonstration bewährter Praktiken
description_es=Un plugin I2P de ejemplo que demuestra las mejores prácticas

# Console integration
consoleLinkName=Example Plugin
consoleLinkName_de=Beispiel-Plugin
consoleLinkURL=/example/
consoleLinkTooltip=Open the Example Plugin control panel
consoleLinkTooltip_de=Öffne das Beispiel-Plugin-Kontrollfeld
console-icon=/icon.png

# Installation behavior
dont-start-at-install=false
router-restart-required=false

# Platform requirements (informational)
required-platform-OS=All platforms supported
other-requirements=Requires 512MB free disk space
```
---

## 부록 B: 완전한 clients.config 예제

```properties
# Main service client (managed)
clientApp.0.main=com.example.plugin.MainService
clientApp.0.name=Example Plugin Main Service
clientApp.0.delay=30
clientApp.0.args=$PLUGIN/config.properties --port=7656
clientApp.0.stopargs=shutdown
clientApp.0.uninstallargs=cleanup
clientApp.0.classpath=$PLUGIN/lib/example.jar,$I2P/lib/i2p.jar,$I2P/lib/mstreaming.jar

# External program via ShellService
clientApp.1.main=net.i2p.apps.ShellService
clientApp.1.name=Example Native Helper
clientApp.1.delay=35
clientApp.1.args=$PLUGIN/bin/helper-$OS-$ARCH --config $PLUGIN/helper.conf
clientApp.1.classpath=$I2P/lib/i2p.jar

# Jetty eepsite
clientApp.2.main=net.i2p.jetty.JettyStart
clientApp.2.name=Example Eepsite
clientApp.2.delay=40
clientApp.2.args=$PLUGIN/eepsite/jetty.xml
clientApp.2.stopargs=$PLUGIN/eepsite/jetty.xml stop
clientApp.2.classpath=$PLUGIN/lib/example-web.jar,$I2P/lib/i2p.jar

# I2PTunnel for eepsite
clientApp.3.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.3.name=Example Eepsite Tunnel
clientApp.3.delay=45
clientApp.3.args=$PLUGIN/eepsite/i2ptunnel.config
```
---

## 부록 C: 전체 webapps.config 예제

```properties
# Disable autostart for admin webapp
webapps.example-admin.startOnLoad=false

# Main webapp with classpath
webapps.example.startOnLoad=true
webapps.example.classpath=$PLUGIN/lib/example-core.jar,$PLUGIN/lib/commons-utils.jar,$I2P/lib/jstl.jar,$I2P/lib/standard.jar

# Legacy support (pre-0.7.12-9)
plugin.example.startOnLoad=true
```
---

## 부록 D: 마이그레이션 체크리스트 (0.9.53에서 2.10.0으로)

### 필요한 변경 사항

- [ ] **빌드 프로세스에서 Pack200 압축 제거**
  - Ant/Maven/Gradle 스크립트에서 pack200 작업 제거
  - pack200 없이 기존 플러그인을 재배포

- [ ] **Java 버전 요구 사항 검토**
  - 새 기능에 대해 Java 11+를 요구하는 방안 고려
  - I2P 2.11.0에서 Java 17+ 요구 사항 도입 계획 수립
  - plugin.config의 `min-java-version` 업데이트

- [ ] **문서 업데이트**
  - Pack200 참조 제거
  - Java 버전 요구 사항 업데이트
  - I2P 버전 참조 업데이트 (0.9.x → 2.x)

### 권장 변경 사항

- [ ] **암호학적 서명 강화**
  - 아직 완료하지 않았다면 XPI2P에서 SU3로 마이그레이션하세요
  - 새 플러그인에는 RSA-4096 키를 사용하세요

- [ ] **새 기능 활용 (0.9.53+ 사용 시)**
  - 플랫폼별 업데이트에 `$OS` / `$ARCH` 변수를 사용
  - 외부 프로그램에는 ShellService(셸 서비스)를 사용
  - 개선된 웹앱 클래스패스를 사용 (모든 WAR 이름에 대해 동작)

- [ ] **호환성 테스트**
  - I2P 2.10.0에서 테스트
  - Java 8, 11, 17에서 검증
  - Windows, Linux, macOS에서 확인

### 선택적 개선 사항

- [ ] 제대로 된 ServletContextListener 구현
- [ ] 현지화된 설명 추가
- [ ] 콘솔 아이콘 제공
- [ ] 종료 처리 개선
- [ ] 포괄적인 로깅 추가
- [ ] 자동화된 테스트 작성
