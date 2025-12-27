---
title: "웹 브라우저 설정"
description: "데스크톱과 Android에서 I2P의 HTTP/HTTPS 프록시를 사용하도록 인기 있는 브라우저 설정하기"
slug: "browser-config"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

이 가이드는 일반적인 브라우저에서 I2P의 내장 HTTP 프록시를 통해 트래픽을 전송하도록 설정하는 방법을 보여줍니다. Safari, Firefox, Chrome/Chromium 브라우저에 대한 자세한 단계별 지침을 다룹니다.

**중요 사항**:

- I2P의 기본 HTTP 프록시는 `127.0.0.1:4444`에서 수신 대기합니다.
- I2P는 I2P 네트워크 내부의 트래픽(.i2p 사이트)을 보호합니다.
- 브라우저를 구성하기 전에 I2P router가 실행 중인지 확인하세요.

## Safari (macOS)

Safari는 macOS의 시스템 전체 프록시 설정을 사용합니다.

### Step 1: Open Network Settings

1. **Safari**를 열고 **Safari → 설정**(또는 **환경설정**)으로 이동
2. **고급** 탭 클릭
3. **프록시** 섹션에서 **설정 변경...** 클릭

이렇게 하면 Mac의 시스템 네트워크 설정이 열립니다.

![Safari 고급 설정](/images/guides/browser-config/accessi2p_1.png)

### 1단계: 네트워크 설정 열기

1. 네트워크 설정에서 **웹 프록시(HTTP)** 확인란을 선택합니다
2. 다음 정보를 입력합니다:
   - **웹 프록시 서버**: `127.0.0.1`
   - **포트**: `4444`
3. **확인**을 클릭하여 설정을 저장합니다

![Safari 프록시 설정](/images/guides/browser-config/accessi2p_2.png)

이제 Safari에서 `.i2p` 사이트를 탐색할 수 있습니다!

**참고**: 이러한 프록시 설정은 macOS 시스템 프록시를 사용하는 모든 애플리케이션에 영향을 미칩니다. I2P 브라우징을 격리하려면 별도의 사용자 계정을 생성하거나 I2P 전용 브라우저를 사용하는 것을 고려하세요.

## Firefox (Desktop)

Firefox는 시스템과 독립적인 자체 프록시 설정을 가지고 있어 I2P 전용 브라우징에 이상적입니다.

### 2단계: HTTP 프록시 설정

1. 오른쪽 상단의 **메뉴 버튼**(☰)을 클릭합니다
2. **설정**을 선택합니다

![Firefox 설정](/images/guides/browser-config/accessi2p_3.png)

### Step 2: Find Proxy Settings

1. 설정 검색창에 **"proxy"**를 입력하세요
2. **네트워크 설정**으로 스크롤하세요
3. **설정...** 버튼을 클릭하세요

![Firefox Proxy Search](/images/guides/browser-config/accessi2p_4.png)

### 1단계: 설정 열기

1. **수동 프록시 구성** 선택
2. 다음을 입력:
   - **HTTP 프록시**: `127.0.0.1` **포트**: `4444`
3. **SOCKS 호스트**는 비워둠 (SOCKS 프록시가 특별히 필요한 경우가 아니라면)
4. SOCKS 프록시를 사용하는 경우에만 **SOCKS 사용 시 DNS 프록시** 체크
5. **확인**을 클릭하여 저장

![Firefox 수동 프록시 설정](/images/guides/browser-config/accessi2p_5.png)

이제 Firefox에서 `.i2p` 사이트를 탐색할 수 있습니다!

**팁**: I2P 브라우징 전용 Firefox 프로필을 별도로 생성하는 것을 고려하세요. 이렇게 하면 I2P 브라우징을 일반 브라우징과 분리할 수 있습니다. 프로필을 생성하려면 Firefox 주소 표시줄에 `about:profiles`를 입력하세요.

## Chrome / Chromium (Desktop)

Chrome 및 Chromium 기반 브라우저(Brave, Edge 등)는 일반적으로 Windows와 macOS에서 시스템 프록시 설정을 사용합니다. 이 가이드는 Windows 구성을 보여줍니다.

### 2단계: 프록시 설정 찾기

1. 오른쪽 상단의 **세 점 메뉴** (⋮)를 클릭합니다
2. **Settings**를 선택합니다

![Chrome 설정](/images/guides/browser-config/accessi2p_6.png)

### 3단계: 수동 프록시 설정

1. 설정 검색 상자에 **"proxy"** 입력
2. **컴퓨터의 프록시 설정 열기** 클릭

![Chrome 프록시 검색](/images/guides/browser-config/accessi2p_7.png)

### Step 3: Open Manual Proxy Setup

Windows 네트워크 및 인터넷 설정이 열립니다.

1. **수동 프록시 설정**까지 아래로 스크롤합니다
2. **설정**을 클릭합니다

![Windows Proxy 설정](/images/guides/browser-config/accessi2p_8.png)

### 1단계: Chrome 설정 열기

1. **프록시 서버 사용**을 **켜짐**으로 전환
2. 다음을 입력:
   - **프록시 IP 주소**: `127.0.0.1`
   - **포트**: `4444`
3. 선택 사항으로 **"다음으로 시작하는 주소에는 프록시 서버 사용 안 함"**에 예외를 추가 (예: `localhost;127.*`)
4. **저장** 클릭

![Chrome 프록시 설정](/images/guides/browser-config/accessi2p_9.png)

이제 Chrome에서 `.i2p` 사이트를 탐색할 수 있습니다!

**참고**: 이 설정은 Windows의 모든 Chromium 기반 브라우저와 일부 다른 애플리케이션에 영향을 미칩니다. 이를 방지하려면 전용 I2P 프로필을 사용하는 Firefox를 사용하는 것을 고려하십시오.

### 2단계: 프록시 설정 열기

Linux에서는 시스템 설정을 변경하지 않고 프록시 플래그를 사용하여 Chrome/Chromium을 실행할 수 있습니다:

```bash
chromium \
  --proxy-server="http=127.0.0.1:4444 \
  --proxy-bypass-list="<-loopback>"
```
또는 데스크톱 실행 스크립트를 생성합니다:

```bash
#!/bin/bash
chromium --proxy-server="http=127.0.0.1:4444" --user-data-dir="$HOME/.config/chromium-i2p"
```
`--user-data-dir` 플래그는 I2P 브라우징을 위한 별도의 Chrome 프로필을 생성합니다.

## Firefox (데스크톱)

최신 "Fenix" Firefox 빌드는 기본적으로 about:config와 확장 기능을 제한합니다. IceRaven은 선별된 확장 기능 세트를 활성화하는 Firefox 포크로, 프록시 설정을 간단하게 만들어줍니다.

확장 기능 기반 설정 (IceRaven):

1) 이미 IceRaven을 사용 중이라면 먼저 브라우징 기록을 삭제하는 것을 고려하세요 (메뉴 → 기록 → 기록 삭제). 2) 메뉴 → 부가 기능 → 부가 기능 관리자를 여세요. 3) "I2P Proxy for Android and Other Systems" 확장 프로그램을 설치하세요. 4) 이제 브라우저가 I2P를 통해 프록시됩니다.

이 확장 프로그램은 [AMO](https://addons.mozilla.org/en-US/android/addon/i2p-proxy/)에서 설치하는 경우 Fenix 이전 Firefox 기반 브라우저에서도 작동합니다.

Firefox Nightly에서 광범위한 확장 기능 지원을 활성화하려면 [Mozilla에서 문서화한](https://blog.mozilla.org/addons/2020/09/29/expanded-extension-support-in-firefox-for-android-nightly/) 별도의 프로세스가 필요합니다.

## Internet Explorer / Windows System Proxy

Windows에서는 시스템 프록시 대화 상자가 IE에 적용되며, Chromium 기반 브라우저가 시스템 설정을 상속받을 때 사용할 수 있습니다.

1) "네트워크 및 인터넷 설정" → "프록시"를 엽니다. 2) "LAN에 프록시 서버 사용"을 활성화합니다. 3) HTTP에 대해 주소 `127.0.0.1`, 포트 `4444`를 설정합니다. 4) 선택 사항으로 "로컬 주소에 대해 프록시 서버 사용 안 함"을 선택합니다.
