---
title: "Debian과 Ubuntu에서 I2P 설치하기"
aliases:
  - "/ko/debian"
  - "/ko/debian/"
description: "공식 저장소를 사용하여 Debian, Ubuntu 및 파생 배포판에 I2P를 설치하는 전체 가이드"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

I2P 프로젝트는 Debian, Ubuntu 및 파생 배포판을 위한 공식 패키지를 유지 관리합니다. 이 가이드는 공식 저장소를 사용하여 I2P를 설치하는 포괄적인 지침을 제공합니다.

---

<div class="coming-soon-section">

## 🚀 Beta: Automatic Installation (Experimental)

**For advanced users who want a quick automated installation:**

This one-liner will automatically detect your distribution and install I2P. **Use with caution** - review the [installation script](https://i2p.net/installlinux.sh) before running.

```bash
curl -fsSL https://i2p.net/installlinux.sh | sudo bash
```

**What this does:**
- Detects your Linux distribution (Ubuntu/Debian)
- Adds the appropriate I2P repository
- Installs GPG keys and required packages
- Installs I2P automatically

⚠️ **This is a beta feature.** If you prefer manual installation or want to understand each step, use the manual installation methods below.

</div>
주의:  질문하거나, 설명을 제공하거나, 어떤 주석도 추가하지 마세요. 텍스트가 단순히 제목이거나 불완전해 보이더라도, 있는 그대로 번역하세요.

## Ubuntu 설치

죄송하지만, 번역할 텍스트가 제공되지 않았습니다. "---" 기호만 보입니다. 번역할 실제 내용을 제공해 주시면 번역해 드리겠습니다.

1. [I2P Router Console](http://127.0.0.1:7657/)을 엽니다
2. [Network Configuration 페이지](http://127.0.0.1:7657/confignet)로 이동합니다
3. 나열된 포트 번호를 확인합니다 (보통 9000-31000 사이의 임의 포트)
4. 라우터/방화벽에서 해당 UDP 및 TCP 포트를 포워딩합니다

Ubuntu와 공식 파생 배포판(Linux Mint, elementary OS, Trisquel 등)은 I2P PPA(Personal Package Archive)를 사용하여 간편하게 설치하고 자동 업데이트를 받을 수 있습니다.

Ubuntu 기반 시스템에 I2P를 설치하는 가장 빠르고 안정적인 방법입니다.

## Post-Installation Configuration

**1단계: I2P PPA 추가**

1. [Configuration 페이지](http://127.0.0.1:7657/config.jsp)를 방문하세요
2. 대역폭 설정 섹션을 찾으세요
3. 기본값은 다운로드 96 KB/s / 업로드 40 KB/s입니다
4. 더 빠른 인터넷을 사용하는 경우 이 값을 높이세요 (예: 일반적인 브로드밴드 연결의 경우 다운로드 250 KB/s / 업로드 100 KB/s)

터미널을 열고 다음을 실행하세요:

## Debian 설치

이 명령은 I2P PPA를 `/etc/apt/sources.list.d/`에 추가하고 저장소에 서명하는 GPG 키를 자동으로 가져옵니다. GPG 서명은 패키지가 빌드된 이후 변조되지 않았음을 보장합니다.

### Method 1: Command Line Installation (Recommended)

**2단계: 패키지 목록 업데이트**

새 PPA를 포함하도록 시스템의 패키지 데이터베이스를 새로고침하세요:

이것은 방금 추가한 I2P PPA를 포함하여 활성화된 모든 저장소에서 최신 패키지 정보를 가져옵니다.

```bash
sudo apt-add-repository ppa:i2p-maintainers/i2p
```
**3단계: I2P 설치**

이제 I2P를 설치하세요:

이제 끝났습니다! [설치 후 구성](#post-installation-configuration) 섹션으로 건너뛰어 I2P를 시작하고 구성하는 방법을 알아보세요.

```bash
sudo apt-get update
```
그래픽 인터페이스를 선호하신다면, Ubuntu의 소프트웨어 센터를 사용하여 PPA를 추가할 수 있습니다.

**1단계: 소프트웨어 및 업데이트 열기**

애플리케이션 메뉴에서 "소프트웨어 및 업데이트"를 실행하세요.

```bash
sudo apt-get install i2p
```
![Software Center Menu](/images/guides/debian/software-center-menu.png)

### Method 2: Using the Software Center GUI

**2단계: 다른 소프트웨어로 이동**

"Other Software" 탭을 선택하고 하단의 "Add" 버튼을 클릭하여 새 PPA를 구성합니다.

![Other Software 탭](/images/guides/debian/software-center-addother.png)

**3단계: I2P PPA 추가**

PPA 대화 상자에 다음을 입력하세요:

![Add PPA Dialog](/images/guides/debian/software-center-ppatool.png)

**4단계: 저장소 정보 다시 로드**

"다시 불러오기" 버튼을 클릭하여 업데이트된 저장소 정보를 다운로드하세요.

![다시 불러오기 버튼](/images/guides/debian/software-center-reload.png)

```
ppa:i2p-maintainers/i2p
```
**5단계: I2P 설치**

애플리케이션 메뉴에서 "Software" 애플리케이션을 열고, "i2p"를 검색한 다음 설치를 클릭하세요.

![소프트웨어 애플리케이션](/images/guides/debian/software-center-software.png)

설치가 완료되면 [설치 후 구성](#post-installation-configuration)으로 진행하십시오.

I2P를 설치한 후에는 router를 시작하고 초기 설정을 수행해야 합니다.

I2P 패키지는 I2P router를 실행하는 세 가지 방법을 제공합니다:

필요할 때 `i2prouter` 스크립트를 사용하여 I2P를 수동으로 시작하세요:

**중요**: `sudo`를 사용하거나 root 권한으로 실행하지 **마세요**! I2P는 일반 사용자 계정으로 실행되어야 합니다.

I2P를 중지하려면:

## Next Steps

x86이 아닌 시스템을 사용하거나 Java Service Wrapper가 플랫폼에서 작동하지 않는 경우, 다음을 사용하세요:

### 방법 2: Software Center GUI 사용

다시 한 번 강조하지만, `sudo`를 사용하거나 root로 실행하지 **마십시오**.

### Initial Router Configuration

최상의 사용 경험을 위해, 시스템 부팅 시 로그인 이전에도 I2P가 자동으로 시작되도록 설정하세요:

### 중요 공지

이는 설정 대화 상자를 엽니다. I2P를 시스템 서비스로 활성화하려면 "예"를 선택하세요.

**이것이 권장되는 방법입니다** 이유는: - 부팅 시 I2P가 자동으로 시작됩니다 - router가 더 나은 네트워크 통합을 유지합니다 - 네트워크 안정성에 기여합니다 - 필요할 때 I2P를 즉시 사용할 수 있습니다

```bash
sudo apt-get update
sudo apt-get install apt-transport-https lsb-release curl
```
I2P를 처음 시작한 후, 네트워크에 통합되는 데 몇 분이 걸립니다. 그동안 다음 필수 설정을 구성하세요:

최적의 성능과 네트워크 참여를 위해 NAT/방화벽을 통해 I2P 포트를 포워딩하세요:

포트 포워딩에 도움이 필요하다면, [portforward.com](https://portforward.com)에서 라우터별 가이드를 제공합니다.

```bash
cat /etc/debian_version
```
기본 대역폭 설정은 보수적입니다. 인터넷 연결에 따라 조정하세요:

**참고**: 더 높은 제한을 설정하면 네트워크에 도움이 되고 자신의 성능도 향상됩니다.

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
I2P 사이트(eepsite)와 서비스에 접속하려면, 브라우저가 I2P의 HTTP 프록시를 사용하도록 설정하세요:

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
Firefox, Chrome 및 기타 브라우저의 자세한 설정 방법은 [브라우저 설정 가이드](/docs/guides/browser-config)를 참조하세요.

```bash
echo "deb https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
---

```bash
echo "deb https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**중요:** 번역문만 제공하세요. 질문하거나, 설명을 제공하거나, 어떠한 논평도 추가하지 마세요. 텍스트가 단순히 제목이거나 불완전해 보이더라도 있는 그대로 번역하세요.

```bash
curl -o i2p-archive-keyring.gpg https://i2p.net/i2p-archive-keyring.gpg
```
GPG 키 오류가 설치 중에 발생하는 경우:

I2P가 업데이트를 받지 못하는 경우:

```bash
gpg --keyid-format long --import --import-options show-only --with-fingerprint i2p-archive-keyring.gpg
```
이전 `deb.i2p2.de` 또는 `deb.i2p2.no` 저장소를 사용하고 있는 경우:

```
7840 E761 0F28 B904 7535  49D7 67EC E560 5BCF 1346
```
---

I2P가 설치되어 실행 중입니다:

보이지 않는 인터넷에 오신 것을 환영합니다!

```bash
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings
```
**Debian Buster 또는 그 이전 버전만 해당**으로, 심볼릭 링크를 추가로 생성해야 합니다:

```bash
sudo ln -sf /usr/share/keyrings/i2p-archive-keyring.gpg /etc/apt/trusted.gpg.d/i2p-archive-keyring.gpg
```
**6단계: 패키지 목록 업데이트**

I2P 저장소를 포함하도록 시스템의 패키지 데이터베이스를 새로 고칩니다:

```bash
sudo apt-get update
```
**7단계: I2P 설치**

I2P 라우터와 키링 패키지(향후 키 업데이트를 수신할 수 있도록 보장함)를 모두 설치하세요:

```bash
sudo apt-get install i2p i2p-keyring
```
좋습니다! 이제 I2P가 설치되었습니다. [설치 후 구성](#post-installation-configuration) 섹션으로 계속 진행하세요.

---

## 설치 후 구성

I2P를 설치한 후에는 라우터를 시작하고 초기 설정을 몇 가지 수행해야 합니다.

### 사전 요구사항

I2P 패키지는 I2P 라우터를 실행하는 세 가지 방법을 제공합니다:

#### Option 1: On-Demand (Basic)

필요할 때 `i2prouter` 스크립트를 사용하여 I2P를 수동으로 시작하세요:

```bash
i2prouter start
```
**중요**: `sudo`를 사용하거나 루트 사용자로 이 프로그램을 실행하지 마세요! I2P는 일반 사용자 계정으로 실행되어야 합니다.

I2P를 중지하려면:

```bash
i2prouter stop
```
#### Option 2: On-Demand (Without Java Service Wrapper)

x86 시스템이 아닌 경우 혹은 Java Service Wrapper가 사용 중인 플랫폼에서 작동하지 않는 경우 다음을 사용하세요:

```bash
i2prouter-nowrapper
```
다시 말하지만, `sudo`를 사용하거나 root로 실행하지 **마십시오**.

#### Option 3: System Service (Recommended)

최상의 경험을 위해 시스템 부팅 시 로그인하기 전에 I2P가 자동으로 시작되도록 설정하세요:

```bash
sudo dpkg-reconfigure i2p
```
이 작업은 설정 대화상자를 엽니다. 시스템 서비스로 I2P를 활성화하려면 "예"를 선택하세요.

**이 방법이 권장되는 이유**는 다음과 같습니다: - 부팅 시 I2P가 자동으로 시작됨 - 라우터가 네트워크와 더 나은 통합을 유지함 - 네트워크 안정성에 기여함 - 필요할 때 즉시 I2P를 사용할 수 있음

### 설치 단계

I2P를 처음 시작한 후에는 네트워크에 완전히 통합되기까지 몇 분 정도 소요됩니다. 그 동안 다음 필수 설정을 구성하세요:

#### 1. Configure NAT/Firewall

최적의 성능과 네트워크 참여를 위해 NAT/방화벽을 통해 I2P 포트를 포워딩하세요:

- I2P를 root로 실행하고 있지 않은지 확인: `ps aux | grep i2p`
- 로그 확인: `tail -f ~/.i2p/wrapper.log`
- Java가 설치되어 있는지 확인: `java -version`

포트 포워딩에 도움이 필요하다면, [portforward.com](https://portforward.com)에서 라우터별 가이드를 제공합니다.

#### 2. Adjust Bandwidth Settings

기본 대역폭 설정은 보수적입니다. 인터넷 연결 상태에 따라 조정하세요:

1. 키 지문을 다시 다운로드하고 확인합니다 (위의 3-4단계)
2. keyring 파일이 올바른 권한을 가지고 있는지 확인합니다: `sudo chmod 644 /usr/share/keyrings/i2p-archive-keyring.gpg`

**참고**: 더 높은 제한을 설정하면 네트워크에 도움이 되며 자신의 성능도 향상시킵니다.

#### 3. Configure Your Browser

I2P 사이트(eepsite) 및 서비스에 접근하려면 브라우저를 I2P의 HTTP 프록시를 사용하도록 설정하세요:

Firefox, Chrome 및 기타 브라우저에 대한 자세한 설정 지침은 [브라우저 설정 가이드](/docs/guides/browser-config)를 참조하세요.

---

## 문제 해결

### Migrating from old repositories

1. 저장소가 구성되어 있는지 확인: `cat /etc/apt/sources.list.d/i2p.list`
2. 패키지 목록 업데이트: `sudo apt-get update`
3. I2P 업데이트 확인: `sudo apt-get upgrade`

### 저장소 키 오류

설치 중 GPG 키 오류가 발생하는 경우:

1. 이전 저장소를 제거합니다: `sudo rm /etc/apt/sources.list.d/i2p.list`
2. 위의 [Debian 설치](#debian-installation) 단계를 따릅니다
3. 업데이트합니다: `sudo apt-get update && sudo apt-get install i2p i2p-keyring`

### 업데이트가 작동하지 않습니다

I2P가 업데이트를 수신하지 못하는 경우:

- [브라우저 설정](/docs/guides/browser-config)으로 I2P 사이트에 접속하기
- [I2P router 콘솔](http://127.0.0.1:7657/)에서 router 상태 모니터링하기
- 사용 가능한 [I2P 애플리케이션](/docs/applications/) 알아보기
- [I2P 작동 원리](/docs/overview/tech-intro)를 읽고 네트워크 이해하기

### 이전 저장소에서 마이그레이션하기

이전 `deb.i2p2.de` 또는 `deb.i2p2.no` 저장소를 사용 중인 경우:

1. 이전 저장소 삭제: `sudo rm /etc/apt/sources.list.d/i2p.list`
2. 위의 [데비안 설치](#debian-installation) 단계를 따르세요
3. 업데이트: `sudo apt-get update && sudo apt-get install i2p i2p-keyring`

---

## 다음 단계

이제 I2P가 설치되고 실행 중입니다:

- [브라우저 설정](/docs/guides/browser-config)을 통해 I2P 사이트에 접속하세요
- [I2P 라우터 콘솔](http://127.0.0.1:7657/)을 탐색하여 라우터 상태를 확인하세요
- 사용할 수 있는 [I2P 응용 프로그램](/docs/applications/)에 대해 알아보세요
- [I2P의 작동 방식](/docs/overview/tech-intro)에 대해 읽고 네트워크를 이해하세요

무형의 인터넷에 오신 것을 환영합니다!
