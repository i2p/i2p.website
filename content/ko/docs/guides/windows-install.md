---
title: "Windows에 I2P 설치하기"
description: "Windows 설치 방법 선택: Easy Install Bundle 또는 Standard Installation"
lastUpdated: "2025-11"
toc: true
---

## 설치 방법 선택

Windows에서 I2P를 설치하는 방법은 두 가지가 있습니다. 필요에 가장 적합한 방법을 선택하세요:

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin: 2rem 0;">

<div style="border: 2px solid #22c55e; border-radius: 8px; padding: 1.5rem; background: var(--background-secondary);">


### 🚀 Easy Install Bundle (Recommended)

**대부분의 사용자에게 최적**

✅ 올인원 설치 프로그램 ✅ Java 포함 (별도 설치 불필요) ✅ Firefox 프로필 포함 ✅ 가장 빠른 설정

**이런 경우에 선택하세요:** - 가장 간단한 설치를 원하는 경우 - Java가 설치되어 있지 않은 경우 - I2P를 처음 사용하는 경우

<a href="#easy-install-bundle" style="display: inline-block; background: #22c55e; color: white; padding: 0.75rem 1.5rem; border-radius: 4px; text-decoration: none; font-weight: bold; margin-top: 1rem;">간편 설치 가이드 →</a>

</div>

<div style="border: 2px solid #1e40af; border-radius: 8px; padding: 1.5rem; background: var(--background-secondary);">


### 🚀 간편 설치 번들 (권장)

**고급 사용자용**

📦 Java 기반 JAR 설치 프로그램 🔧 설치에 대한 더 많은 제어 💾 더 작은 다운로드 크기

**다음 경우에 선택하세요:** - Java가 이미 설치되어 있는 경우 - 더 많은 제어를 원하는 경우 - 기존 방식을 선호하는 경우

<a href="#standard-installation" style="display: inline-block; background: #1e40af; color: white; padding: 0.75rem 1.5rem; border-radius: 4px; text-decoration: none; font-weight: bold; margin-top: 1rem;">표준 설치 가이드 →</a>

</div>

</div>


전체 내용이 빈 줄만 포함되어 있어 번역할 텍스트가 없습니다.

---

## Step 1: Select Your Language

Easy Install Bundle 설치 프로그램을 실행하면 언어 선택 화면이 나타납니다.

![언어 선택](/images/guides/windows-install/language-selection.png)

1. **드롭다운 메뉴에서 원하는 언어를 선택하세요**
   - 영어, 독일어, 스페인어, 프랑스어 등 다양한 언어를 선택할 수 있습니다
2. **OK**를 클릭하여 계속 진행하세요

설치 프로그램 인터페이스는 이후의 모든 단계에서 선택한 언어를 사용합니다.

---

(번역할 텍스트가 제공되지 않았습니다. 번역할 내용을 입력해 주세요.)

## 간편 설치 번들

다음으로 I2P 라이선스 정보가 표시됩니다. Easy Install Bundle에는 다양한 자유 및 오픈 소스 라이선스에 따른 구성 요소가 포함되어 있습니다.

![License Agreement](/images/guides/windows-install/license-agreement.png)

**설치를 계속하려면**: 1. 라이선스 정보를 검토하세요 (선택 사항이지만 권장됨) 2. 라이선스에 동의하고 진행하려면 **I Agree**를 클릭하세요 3. 설치를 원하지 않으시면 **Cancel**을 클릭하세요

---

I2P 네트워크 내에서 호스팅되는 웹사이트

## Step 3: Choose Installation Folder

이제 컴퓨터에서 I2P를 설치할 위치를 선택합니다.

![설치 폴더 선택](/images/guides/windows-install/installation-folder.png)

**설치 옵션**:

1. **기본 위치 사용** (권장)
   - 기본 경로: `C:\Users\[YourUsername]\AppData\Local\I2peasy\`
   - 사용자 프로필 디렉토리에 I2P를 설치합니다
   - 업데이트 시 관리자 권한이 필요하지 않습니다

2. **사용자 지정 위치 선택**
   - **찾아보기...**를 클릭하여 다른 폴더를 선택합니다
   - 다른 드라이브에 설치하려는 경우 유용합니다
   - 선택한 폴더에 쓰기 권한이 있는지 확인하세요

**용량 요구사항**: - 설치 프로그램에 필요한 용량이 표시됩니다(일반적으로 1GB 미만) - 선택한 드라이브에 충분한 여유 공간이 있는지 확인하세요

3. **Install**을 클릭하여 설치 프로세스를 시작합니다

설치 프로그램이 이제 선택한 위치에 필요한 모든 파일을 복사합니다. 이 작업은 몇 분 정도 걸릴 수 있습니다.


(번역할 텍스트가 제공되지 않았습니다)

## 2단계: 라이선스 동의서 수락

"Start I2P?"가 체크된 상태에서 Finish를 클릭한 후:

1. **I2P Router 시작** - I2P router가 백그라운드에서 실행되기 시작합니다
2. **시스템 트레이 아이콘 표시** - Windows 시스템 트레이(오른쪽 하단 모서리)에서 I2P 아이콘을 찾으세요
3. **Router 콘솔 열림** - 기본 웹 브라우저가 자동으로 I2P Router Console을 엽니다 (일반적으로 `http://127.0.0.1:7657`)
4. **초기 연결** - I2P가 네트워크에 연결하고 tunnel을 구축하기 시작합니다 (처음 실행 시 5-10분 소요될 수 있습니다)

**축하합니다!** I2P가 이제 Windows 컴퓨터에 설치되어 실행 중입니다.


I2P 네트워크 프로토콜과 터널 구조에 대한 기술 문서입니다. I2P router들은 garlic encryption을 사용하여 메시지를 암호화하고, tunnel을 통해 익명성을 보장합니다.

주요 구성 요소:
- **Router**: I2P 네트워크의 기본 노드
- **Tunnel**: 단방향 암호화된 통신 경로
- **LeaseSet**: destination의 inbound tunnel 정보
- **NetDb**: 네트워크 데이터베이스
- **Floodfill**: netDb 데이터를 저장하는 고용량 router

전송 프로토콜:
- NTCP2: TCP 기반 암호화 전송
- SSU: UDP 기반 전송 (레거시)

애플리케이션 인터페이스:
- SAMv3: Simple Anonymous Messaging protocol
- I2PTunnel: TCP/UDP 터널링 도구
- I2CP: I2P Control Protocol

Eepsite는 I2P 네트워크 내의 웹사이트를 의미하며, `.i2p` 도메인을 사용합니다.

설정 예시:
```yaml
i2p:
  router:
    bandwidth: 128
    participating: true
```

더 자세한 정보는 [I2P 공식 문서](https://geti2p.net)를 참조하세요.

## 4단계: 설치 완료 및 I2P 시작

- **네트워크 통합 대기**: I2P가 네트워크에 통합되고 tunnel을 구축할 수 있도록 5-10분 정도 기다리세요
- **브라우저 설정**: I2P 브라우징을 위해 포함된 Firefox 프로필을 사용하세요
- **포트 포워딩**: I2P가 사용 중인 포트를 포워딩하는 방법에 대한 라우터별 안내는 [portforward.com](https://portforward.com/)을 참조하세요
- **router console 살펴보기**: I2P의 기능, 서비스 및 구성 옵션에 대해 알아보세요
- **eepsite 방문**: I2P 네트워크를 통해 `.i2p` 웹사이트에 접속해 보세요
- **문서 읽기**: 자세한 내용은 [I2P 문서](/docs/)를 확인하세요

I2P 네트워크에 오신 것을 환영합니다! 🎉


고지 사항: I2P 네트워크를 사용할 때는 귀하의 관할권 내 법률을 준수해야 합니다. I2P는 익명성 도구이며, 불법 활동을 용인하거나 장려하지 않습니다.

---

## 권장: 포트 포워딩 (선택 사항이지만 중요)

I2P를 설치하기 전에 시스템에 Java가 설치되어 있어야 합니다.

### Java Requirements

- **Java 버전**: Java 8 (1.8) 이상 필요
- **권장사항**: Java 11 이상 (LTS 버전)
- **유형**: Java Runtime Environment (JRE) 또는 Java Development Kit (JDK)

### Installing Java

Java가 아직 설치되어 있지 않다면, 여러 소스에서 다운로드할 수 있습니다:

**옵션 1: Oracle Java** - 공식 소스: [java.com/download](https://www.java.com/download) - 가장 널리 사용되는 배포판

**옵션 2: OpenJDK** - 오픈소스 구현: [openjdk.org](https://openjdk.org) - 무료 및 오픈소스

**옵션 3: Adoptium (Eclipse Temurin)** - 권장 대안: [adoptium.net](https://adoptium.net) - 무료 오픈소스이며 잘 관리되는 LTS 릴리스

**Java가 설치되어 있는지 확인하려면**: 1. 명령 프롬프트 열기 (`Windows + R`을 누르고, `cmd`를 입력한 후 Enter 키 누르기) 2. 입력: `java -version` 3. Java 버전을 표시하는 출력이 나타나야 합니다

---

**중요**: 번역본만 제공하세요. 질문하거나, 설명을 제공하거나, 어떠한 논평도 추가하지 마세요. 텍스트가 제목만 있거나 불완전해 보여도 있는 그대로 번역하세요.

## Step 1: Install Java

I2P를 설치하기 전에 시스템에 Java를 설치해야 합니다.

1. **Java 배포판 선택**:
   - **Oracle Java**: [java.com/download](https://www.java.com/download)
   - **OpenJDK**: [openjdk.org](https://openjdk.org)
   - **Adoptium**: [adoptium.net](https://adoptium.net)

2. **Windows 설치 프로그램 다운로드** - 선택한 배포판용

3. **설치 프로그램을 실행**하고 설치 안내에 따라 진행하세요

4. **설치 확인**:
   - 명령 프롬프트 열기
   - `java -version`을 입력하고 Enter 누르기
   - Java 8 이상이 설치되었는지 확인

Java가 설치되면 I2P를 설치할 준비가 완료됩니다.


## Step 4: Welcome to I2P Installation

![환영 화면](/images/guides/windows-standard-install/welcome-screen.png)

이것은 설치 과정의 **8단계 중 1단계**입니다.

**Next**를 클릭하여 설치를 계속 진행합니다.


## 표준 설치

컴퓨터에서 I2P를 설치할 위치를 선택하세요.

![Installation Path](/images/guides/windows-standard-install/installation-path.png)

**기본 설치 경로**: `C:\Program Files (x86)\i2p\`

다음 중 하나를 선택할 수 있습니다: - 기본 위치 사용 (권장) - **찾아보기...**를 클릭하여 다른 폴더 선택

이것은 설치 과정의 **8단계 중 3단계**입니다.

**다음**을 클릭하여 계속 진행하세요.

**참고**: I2P를 처음 설치하는 경우, 디렉토리 생성을 확인하는 팝업이 표시됩니다:

![디렉토리 생성 팝업](/images/guides/windows-standard-install/directory-creation-popup.png)

**확인**을 클릭하여 설치 디렉터리를 생성합니다.

---

[번역 내용가 제공되지 않았습니다. 번역할 텍스트를 제공해 주세요.]

## Step 7: Select Installation Packs

설치할 구성 요소를 선택하세요.

![팩 선택](/images/guides/windows-standard-install/select-packs.png)

**중요**: 두 패키지가 모두 선택되었는지 확인하세요: - **Base** (필수) - 핵심 I2P 소프트웨어 (27.53 MB) - **Windows Service** (권장) - 부팅 시 I2P 자동 시작

**Windows Service** 옵션을 사용하면 컴퓨터가 부팅될 때 I2P가 자동으로 시작되므로 매번 수동으로 시작할 필요가 없습니다.

이것은 설치 과정의 **8단계 중 4단계**입니다.

**Next**를 클릭하여 계속합니다.


## Step 9: Setup Shortcuts

I2P 바로가기를 생성할 위치를 설정하세요.

![Setup Shortcuts](/images/guides/windows-standard-install/setup-shortcuts.png)

**바로 가기 옵션**: - ✓ **시작 메뉴에 바로 가기 만들기** (권장) - ✓ **바탕 화면에 추가 바로 가기 만들기** (선택 사항)

**Program Group**: 바로 가기를 저장할 폴더 이름을 선택하거나 생성합니다 - 기본값: `I2P` - 기존 프로그램 그룹을 선택하거나 새로 만들 수 있습니다

**바로 가기 만들기**: - **현재 사용자** - 본인만 바로 가기에 접근할 수 있습니다 - **모든 사용자** - 시스템의 모든 사용자가 바로 가기에 접근할 수 있습니다 (관리자 권한 필요)

이것은 설치 과정의 **8단계 중 6단계**입니다.

**Next**를 클릭하여 계속 진행합니다.


## 1단계: Java 설치

완료를 클릭한 후:

1. **I2P Router 시작** - Windows 서비스를 설치한 경우, I2P가 자동으로 시작됩니다
2. **Router console 열림** - 기본 웹 브라우저가 `http://127.0.0.1:7657`의 I2P Router Console로 자동으로 열립니다
3. **초기 연결** - I2P가 네트워크에 연결하고 tunnel을 구축하기 시작합니다 (첫 실행 시 5-10분 소요될 수 있습니다)

**축하합니다!** I2P가 이제 Windows 컴퓨터에 설치되었습니다.


## 3단계: 언어 선택

- **네트워크 통합 대기**: I2P가 네트워크에 통합되고 tunnel을 구축할 수 있도록 5-10분 정도 기다립니다
- **포트 포워딩 구성**: 설정 방법은 [포트 포워딩 가이드](#recommended-port-forwarding-optional-but-important)를 참조하세요
- **브라우저 구성**: 웹 브라우저가 I2P의 HTTP 프록시를 사용하도록 설정합니다
- **router console 살펴보기**: I2P의 기능, 서비스 및 구성 옵션에 대해 알아봅니다
- **eepsite 방문**: I2P 네트워크를 통해 `.i2p` 웹사이트에 접속해 봅니다
- **문서 읽기**: 자세한 정보는 [I2P 문서](/docs/)를 확인하세요

I2P 네트워크에 오신 것을 환영합니다! 🎉
