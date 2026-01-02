---
title: "I2P Eepsite(I2P 전용 익명 웹사이트) 만들기"
description: "내장된 Jetty 웹 서버를 사용하여 I2P 네트워크에서 나만의 웹사이트를 만들고 호스팅하는 방법을 알아보세요"
lastUpdated: "2025-11"
toc: true
---

## Eepsite(I2P 내부 익명 웹사이트)란 무엇인가요?

**eepsite**(I2P 네트워크 전용 웹사이트)는 I2P 네트워크에서만 존재하는 웹사이트입니다. clearnet(일반 인터넷)을 통해 접속할 수 있는 전통적인 웹사이트와 달리, eepsites는 오직 I2P를 통해서만 접속할 수 있어 사이트 운영자와 방문자 모두의 익명성과 프라이버시를 보호합니다. Eepsites는 `.i2p` 의사 최상위 도메인을 사용하며, 특수한 `.b32.i2p` 주소 또는 I2P address book(I2P 주소록)에 등록된 사람이 읽을 수 있는 이름을 통해 접속할 수 있습니다.

모든 Java I2P 배포판에는 경량의 Java 기반 웹서버인 [Jetty](https://jetty.org/index.html)가 사전 설치되고 사전 구성된 상태로 포함되어 있습니다. 덕분에 몇 분 안에 자신의 eepsite(I2P 내부 웹사이트)를 호스팅하기 시작할 수 있으며 - 추가 소프트웨어 설치가 필요 없습니다.

이 가이드는 I2P의 내장 도구를 사용하여 첫 번째 eepsite를 생성하고 설정하는 과정을 단계별로 안내합니다.

---

## 1단계: 숨은 서비스 관리자 열기

Hidden Services Manager(I2P Tunnel Manager라고도 함)은 HTTP 서버(eepsites)를 포함하여 모든 I2P 서버 및 클라이언트 tunnels을 설정하는 곳입니다.

1. [I2P Router Console](http://127.0.0.1:7657)을 엽니다
2. [Hidden Services Manager](http://127.0.0.1:7657/i2ptunnelmgr)로 이동합니다

Hidden Services Manager 인터페이스에 다음이 표시되어야 합니다: - **상태 메시지** - 현재 tunnel 및 클라이언트 상태 - **전역 tunnel 제어** - 모든 tunnel을 한 번에 관리하는 버튼 - **I2P Hidden Services** - 구성된 서버 tunnel 목록

![숨겨진 서비스 관리자](/images/guides/eepsite/hidden-services-manager.png)

기본적으로, 설정되어 있지만 아직 시작되지 않은 기존의 **I2P 웹서버** 항목이 보일 것입니다. 이는 바로 사용하실 수 있도록 사전 구성된 Jetty 웹서버입니다.

---

## 2단계: Eepsite 서버 설정 구성

Hidden Services 목록에서 **I2P webserver** 항목을 클릭하여 서버 설정 페이지를 엽니다. 여기에서 eepsite의 설정을 맞춤설정할 수 있습니다.

![Eepsite 서버 설정](/images/guides/eepsite/webserver-settings.png)

### 구성 옵션 설명

**이름** - 귀하의 tunnel에 대한 내부 식별자입니다 - 여러 eepsites를 운영하는 경우 어느 것이 어느 것인지 추적하는 데 유용합니다 - 기본값: "I2P webserver"

**설명** - 참고용으로 자신의 eepsite에 대한 간단한 설명 - Hidden Services Manager(숨은 서비스 관리자)에서 본인에게만 표시됨 - 예: "내 eepsite" 또는 "개인 블로그"

**자동 시작 Tunnel** - **중요**: I2P router가 시작될 때 eepsite를 자동으로 시작하려면 이 확인란을 선택하세요 - router가 다시 시작된 후에도 수동 개입 없이 사이트가 계속 접속 가능하도록 보장합니다 - 권장: **활성화**

**대상(호스트와 포트)** - **호스트**: 웹 서버가 실행 중인 로컬 주소(기본값: `127.0.0.1`) - **포트**: 웹 서버가 수신 대기하는 포트(기본값: Jetty의 경우 `7658`) - 사전 설치된 Jetty 웹 서버를 사용 중이라면, **이 값들을 기본값으로 그대로 두세요** - 다른 포트에서 사용자 정의 웹 서버를 실행 중인 경우에만 변경하세요

**웹사이트 호스트 이름** - 이는 eepsite의 사람이 읽기 쉬운 `.i2p` 도메인 이름입니다 - 기본값: `mysite.i2p` (자리표시자) - `stormycloud.i2p` 또는 `myblog.i2p` 같은 사용자 지정 도메인을 등록할 수 있습니다 - 자동 생성되는 `.b32.i2p` 주소만 사용하려면 비워 두세요 (outproxy(아웃프록시)용) - 사용자 지정 호스트 이름을 등록하는 방법은 아래의 [I2P 도메인 등록](#registering-your-i2p-domain)을 참조하세요

**Local Destination** - 이는 귀하의 eepsite의 고유한 암호학적 식별자(destination address, 목적지 주소)입니다 - tunnel이 처음 생성될 때 자동으로 생성됩니다 - I2P에서 귀하의 사이트의 영구적인 "IP address"라고 생각하면 됩니다 - 긴 영숫자 문자열은 귀하의 사이트 `.b32.i2p` 주소를 인코딩한 형태입니다

**개인 키 파일** - 귀하의 eepsite의 개인 키가 저장되는 위치 - 기본값: `eepsite/eepPriv.dat` - **이 파일을 안전하게 보호하십시오** - 이 파일에 접근할 수 있는 사람은 누구나 귀하의 eepsite를 사칭할 수 있습니다 - 이 파일을 절대 공유하거나 삭제하지 마십시오

### 중요 참고 사항

QR 코드 생성 또는 등록 인증 기능을 사용하려면 `.i2p` 접미사가 붙은 웹사이트 호스트 이름을 구성해야 한다는 점을 노란색 경고 상자가 상기시켜 줍니다(예: `mynewsite.i2p`).

---

## 3단계: 고급 네트워킹 옵션(선택 사항)

설정 페이지에서 아래로 스크롤하면 고급 네트워크 옵션을 찾을 수 있습니다. **이 설정은 선택 사항입니다** - 기본 설정은 대부분의 사용자에게 잘 동작합니다. 그러나 보안 요구 사항과 성능 요구 사항에 따라 조정할 수 있습니다.

### Tunnel 길이 옵션

![Tunnel 길이 및 수량 옵션](/images/guides/eepsite/tunnel-options.png)

**Tunnel 길이** - **기본값**: 3홉 tunnel (높은 익명성) - 요청이 eepsite에 도달하기 전에 몇 개의 router 홉을 경유할지 제어합니다 - **홉이 많을수록 = 익명성은 높지만 성능은 느려집니다** - **홉이 적을수록 = 성능은 빨라지지만 익명성은 낮아집니다** - 옵션은 variance 설정(변동 설정)과 함께 0-3 홉 범위로 제공됩니다 - **권장 사항**: 특별한 성능 요구가 없다면 3홉으로 유지하세요

**Tunnel 변동폭** - **기본값**: 0 홉 변동폭 (무작위화 없음, 일관된 성능) - 보안을 강화하기 위해 tunnel 길이에 무작위성을 추가 - 예: "0-1 홉 변동폭"은 tunnel이 무작위로 3 또는 4 홉이 됨을 의미 - 예측 불가능성이 증가하지만 로드 시간이 일관되지 않을 수 있음

### Tunnel 수량 옵션

**개수 (인바운드/아웃바운드 tunnel)** - **기본값**: 인바운드 tunnel 2개, 아웃바운드 tunnel 2개 (표준 대역폭 및 안정성) - eepsite에 할당되는 병렬 tunnel 수를 제어합니다 - **더 많은 tunnel = 더 나은 가용성과 부하 처리 능력, 하지만 더 높은 자원 사용량** - **더 적은 tunnel = 더 낮은 자원 사용량, 하지만 중복성 감소** - 대부분의 사용자에게 권장: 2/2 (기본값) - 트래픽이 많은 eepsite는 3/3 이상이 도움이 될 수 있습니다

**백업 개수** - **기본값**: 백업 tunnels 0개 (중복 없음, 추가 리소스 사용량 없음) - 주요 tunnels가 실패하면 활성화되는 대기용 tunnels - 신뢰성을 높이지만 더 많은 대역폭과 CPU를 소모 - 대부분의 개인용 eepsites에는 백업 tunnels가 필요하지 않음

### POST 제한

![POST 제한 설정](/images/guides/eepsite/post-limits.png)

eepsite에 양식(문의 양식, 댓글 섹션, 파일 업로드 등)이 포함되어 있다면, 남용을 방지하기 위해 POST 요청 제한을 설정할 수 있습니다:

**클라이언트별 제한** - **기간당**: 단일 클라이언트로부터의 최대 요청 수 (기본값: 5분당 6회) - **차단 기간**: 남용하는 클라이언트를 얼마나 오래 차단할지 (기본값: 20분)

**Total Limits** - **Total**: 모든 클라이언트 합산 기준 최대 POST 요청 수(기본값: 5분당 20회) - **Ban Duration**: 제한 초과 시 모든 POST 요청을 거부하는 기간(기본값: 10분)

**POST 제한 기간** - 요청 빈도를 측정하는 시간 창(기본값: 5분)

이러한 제한은 스팸, 서비스 거부(DoS) 공격, 그리고 자동화된 폼 제출의 악용으로부터 보호하는 데 도움이 됩니다.

### 고급 설정을 조정해야 할 때

- **트래픽이 많은 커뮤니티 사이트**: tunnel 개수를 늘리세요(인바운드/아웃바운드 각각 3-4)
- **성능이 중요한 애플리케이션**: tunnel 길이를 2홉으로 줄이세요(익명성 감소라는 트레이드오프가 있음)
- **최대 수준의 익명성이 필요한 경우**: 3홉을 유지하고, 길이 변동(variance) 0-1을 추가하세요
- **정상적으로 사용량이 많은 양식**: POST 제한을 그에 맞게 늘리세요
- **개인 블로그/포트폴리오**: 모든 기본값을 사용하세요

---

## 4단계: 귀하의 Eepsite에 콘텐츠 추가

이제 eepsite 설정을 마쳤으므로 웹서버의 문서 루트 디렉터리에 웹사이트 파일(HTML, CSS, 이미지 등)을 추가해야 합니다. 해당 위치는 사용하는 운영 체제, 설치 유형, 그리고 I2P 구현에 따라 달라집니다.

### 문서 루트 찾기

**문서 루트**(일반적으로 `docroot`라고도 합니다)는 웹사이트의 모든 파일을 두는 디렉터리입니다. `index.html` 파일은 직접 이 디렉터리에 놓아야 합니다.

#### Java I2P (표준 배포판)

**리눅스** - **표준 설치**: `~/.i2p/eepsite/docroot/` - **패키지 설치 (서비스로 실행)**: `/var/lib/i2p/i2p-config/eepsite/docroot/`

**Windows** - **표준 설치**: `%LOCALAPPDATA%\I2P\eepsite\docroot\`   - 일반적인 경로: `C:\Users\YourUsername\AppData\Local\I2P\eepsite\docroot\` - **Windows 서비스 설치**: `%PROGRAMDATA%\I2P\eepsite\docroot\`   - 일반적인 경로: `C:\ProgramData\I2P\eepsite\docroot\`

**macOS** - **표준 설치**: `/Users/YourUsername/Library/Application Support/i2p/eepsite/docroot/`

#### I2P+ (향상된 I2P 배포판)

I2P+는 Java I2P와 동일한 디렉터리 구조를 사용합니다. 운영 체제에 따라 위에 제시된 경로를 따르십시오.

#### i2pd (C++ 구현체)

**Linux/Unix** - **기본값**: `/var/lib/i2pd/eepsite/` 또는 `~/.i2pd/eepsite/` - HTTP 서버 tunnel 아래의 실제 `root` 설정은 `i2pd.conf` 구성 파일에서 확인하세요

**Windows** - i2pd 설치 디렉터리의 `i2pd.conf`를 확인하세요

**macOS** - 일반적으로: `~/Library/Application Support/i2pd/eepsite/`

### 웹사이트 파일 추가하기

1. **문서 루트로 이동** 파일 관리자 또는 터미널을 사용하여
2. **웹사이트 파일을 생성하거나 복사** `docroot` 폴더에
   - 최소한 `index.html` 파일을 만듭니다(홈페이지입니다)
   - 필요에 따라 CSS, JavaScript, 이미지 및 기타 리소스를 추가합니다
3. **하위 디렉터리를 구성** 일반적인 웹사이트와 마찬가지로:
   ```
   docroot/
   ├── index.html
   ├── about.html
   ├── css/
   │   └── style.css
   ├── images/
   │   └── logo.png
   └── js/
       └── script.js
   ```

### 빠른 시작: 간단한 HTML 예제

이제 막 시작하는 경우, `docroot` 폴더에 기본 `index.html` 파일을 만드세요:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My I2P Eepsite</title>
</head>
<body>
    <h1>Welcome to My Eepsite!</h1>
    <p>This is my first website on the I2P network.</p>
    <p>Privacy-focused and decentralized!</p>
</body>
</html>
```
### 권한 (Linux/Unix/macOS)

I2P를 서비스로 실행하거나 다른 사용자 계정으로 실행 중이라면, I2P 프로세스가 귀하의 파일에 대한 읽기 권한을 가지고 있는지 확인하세요:

```bash
# Set appropriate ownership (if running as i2p user)
sudo chown -R i2p:i2p /var/lib/i2p/i2p-config/eepsite/docroot/

# Or set readable permissions for all users
chmod -R 755 ~/.i2p/eepsite/docroot/
```
### 팁

- **기본 콘텐츠**: I2P를 처음 설치하면 `docroot` 폴더에 이미 샘플 콘텐츠가 들어 있습니다 - 원하시면 자유롭게 교체하세요
- **정적 사이트가 가장 적합합니다**: Jetty는 서블릿과 JSP를 지원하지만, 단순한 HTML/CSS/JavaScript 사이트가 유지 관리하기 가장 쉽습니다
- **외부 웹 서버**: 고급 사용자는 다른 포트에서 사용자 지정 웹 서버(Apache, Nginx, Node.js 등)를 실행하고 I2P tunnel을 해당 서버로 가리키도록 설정할 수 있습니다

---

## 5단계: Eepsite 시작하기

이제 eepsite가 구성되었고 콘텐츠도 준비되었으니, 이를 시작해 I2P 네트워크에서 접근 가능하도록 만들 차례입니다.

### Tunnel 시작

1. **[Hidden Services Manager](http://127.0.0.1:7657/i2ptunnelmgr)로 돌아가세요**
2. 목록에서 **I2P webserver** 항목을 찾으세요
3. Control 열에서 **Start** 버튼을 클릭하세요

![Eepsite 실행](/images/guides/eepsite/eepsite-running.png)

### Tunnel 수립 대기

Start를 클릭하면, 사용자의 eepsite tunnel이 구축되기 시작합니다. 이 과정은 보통 **30-60초** 정도 걸립니다. 상태 표시기를 확인하세요:

- **빨간 표시등** = Tunnel 시작/구축 중
- **노란 표시등** = Tunnel이 부분적으로 설정됨
- **초록 표시등** = Tunnel이 완전히 정상 작동하며 준비됨

**녹색 표시등**이 보이면, 귀하의 eepsite가 I2P 네트워크에서 온라인 상태입니다!

### 내 Eepsite에 접속하기

실행 중인 eepsite 옆에 있는 **Preview** 버튼을 클릭하세요. 그러면 eepsite의 주소가 표시된 새 브라우저 탭이 열립니다.

사용자의 eepsite에는 두 가지 유형의 주소가 있습니다:

1. **Base32 주소 (.b32.i2p)**: 다음과 같은 긴 암호학적 주소:
   ```
   http://fcyianvr325tdgiiueyg4rsq4r5iuibzovl26msox5ryoselykpq.b32.i2p
   ```
   - 이는 eepsite(익명 웹사이트)의 영구적이며 암호학적으로 파생된 주소입니다
   - 변경할 수 없으며 개인 키와 연계되어 있습니다
   - 도메인 등록이 없어도 항상 유효합니다

2. **사람이 읽기 쉬운 도메인(.i2p)**: 웹사이트 호스트명을 설정하면 (예: `testwebsite.i2p`)
   - 도메인 등록 후에만 작동함 (다음 섹션 참조)
   - 기억하고 공유하기 쉬움
   - 귀하의 .b32.i2p 주소로 매핑됨

**호스트명 복사** 버튼을 사용하면 공유를 위해 전체 `.b32.i2p` 주소를 빠르게 복사할 수 있습니다.

---

## ⚠️ 중요: 개인 키를 백업하세요

더 진행하기 전에, eepsite(I2P 내 웹사이트)의 개인 키 파일을 **반드시 백업**해야 합니다. 이는 여러 가지 이유로 매우 중요합니다:

### 왜 키를 백업해야 하나요?

**귀하의 개인 키(`eepPriv.dat`)는 귀하의 eepsite(I2P 네트워크 전용 웹사이트)의 정체성입니다.** 이는 귀하의 `.b32.i2p` 주소를 결정하고 eepsite에 대한 소유권을 증명합니다.

- **키 = .b32 주소**: 개인 키는 수학적으로 고유한 .b32.i2p 주소를 생성합니다
- **복구할 수 없음**: 키를 잃으면 eepsite 주소를 영구적으로 잃게 됩니다
- **변경할 수 없음**: .b32 주소를 가리키는 도메인을 등록했다면, **이를 업데이트할 방법이 없습니다** - 등록은 영구적입니다
- **마이그레이션에 필요**: 새 컴퓨터로 이동하거나 I2P를 재설치할 때 동일한 주소를 유지하려면 이 키가 필요합니다
- **멀티호밍 지원**: 여러 위치에서 eepsite를 운영하려면 각 서버에 동일한 키가 필요합니다

### 개인 키는 어디에 있나요?

기본적으로 개인 키는 다음 위치에 저장됩니다: - **Linux**: `~/.i2p/eepsite/eepPriv.dat` (서비스로 설치한 경우 또는 `/var/lib/i2p/i2p-config/eepsite/eepPriv.dat`) - **Windows**: `%LOCALAPPDATA%\I2P\eepsite\eepPriv.dat` 또는 `%PROGRAMDATA%\I2P\eepsite\eepPriv.dat` - **macOS**: `/Users/YourUsername/Library/Application Support/i2p/eepsite/eepPriv.dat`

또한 tunnel 설정의 "Private Key File"에서 이 경로를 확인하거나 변경할 수 있습니다.

### 백업하는 방법

1. **tunnel을 중지하세요** (선택 사항이지만 더 안전합니다)
2. **`eepPriv.dat`을 복사하세요** 안전한 위치로:
   - 외장 USB 드라이브
   - 암호화된 백업 드라이브
   - 비밀번호로 보호된 아카이브
   - 보안 클라우드 스토리지(암호화됨)
3. **여러 개의 백업을 보관하세요** 서로 다른 물리적 위치에
4. **이 파일을 절대 공유하지 마세요** - 이 파일을 가진 사람은 누구나 귀하의 eepsite를 사칭할 수 있습니다

### 백업에서 복원

새 시스템에서 또는 재설치한 후 eepsite를 복원하려면:

1. I2P를 설치하고 tunnel 설정을 생성/구성하세요
2. 키를 복사하기 전에 **tunnel을 중지하세요**
3. 백업해 둔 `eepPriv.dat`를 올바른 위치로 복사하세요
4. tunnel을 시작하세요 - 기존 .b32 주소를 사용합니다

---

## 도메인을 등록하지 않을 경우

**축하합니다!** 사용자 지정 `.i2p` 도메인 이름을 등록할 계획이 없다면, 이제 귀하의 eepsite(I2P 내 웹사이트)는 완성되어 정상적으로 운영됩니다.

다음을 수행할 수 있습니다: - 자신의 `.b32.i2p` 주소를 다른 사람들과 공유 - 어떤 I2P 지원 브라우저를 사용해 I2P 네트워크를 통해 사이트에 접속 - 언제든지 `docroot` 폴더의 웹사이트 파일을 업데이트 - Hidden Services Manager(숨겨진 서비스 관리자)에서 tunnel 상태를 모니터링

**사람이 읽기 쉬운 도메인을 원한다면** (`mysite.i2p`처럼 긴 .b32 주소가 아닌), 다음 섹션으로 이동하세요.

---

## 자신의 I2P 도메인 등록하기

사람이 읽기 쉬운 `.i2p` 도메인(예: `testwebsite.i2p`)은 긴 `.b32.i2p` 주소보다 기억하고 공유하기가 훨씬 쉽습니다. 도메인 등록은 무료이며 선택한 이름을 eepsite의 암호학적 주소에 연결합니다.

### 사전 요구 사항

- 사용자의 eepsite가 녹색 표시로 실행 중이어야 합니다
- tunnel 구성에서 **Website Hostname**을 설정했어야 합니다(2단계)
- 예: `testwebsite.i2p` 또는 `myblog.i2p`

### 1단계: 인증 문자열 생성

1. **tunnel 구성으로 돌아가세요** Hidden Services Manager(숨김 서비스 관리자)에서
2. 설정을 열려면 자신의 **I2P 웹서버** 항목을 클릭하세요
3. 아래로 스크롤하여 **Registration Authentication** 버튼(등록 인증)을 찾으세요

![등록 인증](/images/guides/eepsite/registration-authentication.png)

4. **Registration Authentication**을 클릭합니다
5. "Authentication for adding host [yourdomainhere]"에 표시된 **전체 인증 문자열을 복사합니다**

인증 문자열은 다음과 같습니다:

```
testwebsite.i2p=I8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1uNxFZ0HN7tQbbVj1pmbahepQZNxEW0ufwnMYAoFo8opBQAEAAcAAA==#!date=1762104890#sig=9DjEfrcNRxsoSxiE0Mp0-7rH~ktYWtgwU8c4J0eSo0VHbGxDxdiO9D1Cvwcx8hkherMO07UWOC9BWf-1wRyUAw==
```
이 문자열에는 다음이 포함됩니다: - 귀하의 도메인 이름 (`testwebsite.i2p`) - 귀하의 Destination(목적지) 주소 (길이가 긴 암호학적 식별자) - 타임스탬프 - 개인 키를 소유하고 있음을 증명하는 암호학적 서명

**이 인증 문자열을 보관해 두세요** - 두 등록 서비스 모두에 필요합니다.

### 2단계: stats.i2p에 등록하기

1. **다음 위치로 이동** [stats.i2p Add Key](http://stats.i2p/i2p/addkey.html) (I2P 내에서)

![stats.i2p 도메인 등록](/images/guides/eepsite/stats-i2p-add.png)

2. **인증 문자열을 붙여넣으세요** "Authentication String" 필드에
3. **이름을 추가하세요** (선택 사항) - 기본값은 "Anonymous"
4. **설명을 추가하세요** (권장) - eepsite가 무엇에 관한 것인지 간단히 설명하세요
   - 예: "새 I2P Eepsite", "개인 블로그", "파일 공유 서비스"
5. **"HTTP Service?"을 선택하세요** 웹사이트인 경우 (대부분의 eepsite는 선택 상태로 두세요)
   - IRC, NNTP, 프록시, XMPP, git 등에는 선택을 해제하세요
6. **Submit**을 클릭하세요

성공하면 도메인이 stats.i2p 주소록에 추가되었다는 확인 메시지가 표시됩니다.

### 3단계: reg.i2p에서 등록하기

최대 가용성을 확보하려면 reg.i2p 서비스에도 등록하는 것이 좋습니다:

1. **다음으로 이동하세요** [reg.i2p Add Domain](http://reg.i2p/add) (I2P 내에서)

![reg.i2p 도메인 등록](/images/guides/eepsite/reg-i2p-add.png)

2. **동일한 인증 문자열을 붙여넣으세요** "Auth string" 필드에
3. **설명을 추가하세요** (선택 사항이지만 권장됩니다)
   - 이는 다른 I2P 사용자가 사이트에서 제공하는 내용을 이해하는 데 도움이 됩니다
4. **Submit**을 클릭하세요

도메인이 등록되었다는 확인을 받게 됩니다.

### 4단계: 전파 대기

두 서비스 모두에 제출한 후, 도메인 등록이 I2P 네트워크의 주소록 시스템을 통해 전파됩니다.

**전파 타임라인**: - **초기 등록**: 등록 서비스에서 즉시 - **네트워크 전체 전파**: 수 시간에서 24시간 이상 - **완전한 이용 가능**: 모든 routers가 업데이트되기까지 최대 48시간이 걸릴 수 있습니다

**정상입니다!** I2P 주소록 시스템은 즉시가 아니라 주기적으로 업데이트됩니다. 귀하의 eepsite(익명 웹사이트)는 정상적으로 작동하고 있습니다 - 다른 사용자들이 업데이트된 주소록을 받기만 하면 됩니다.

### 도메인 확인

몇 시간이 지나면 도메인을 테스트할 수 있습니다:

1. I2P 브라우저에서 **새 브라우저 탭을 여세요**
2. 도메인에 직접 접속해 보세요: `http://yourdomainname.i2p`
3. 열리면, 도메인이 등록되어 전파 중입니다!

아직 작동하지 않으면: - 좀 더 기다리세요(주소록은 자체 일정에 따라 업데이트됩니다) - router의 주소록이 동기화되는 데 시간이 필요할 수 있습니다 - 주소록 업데이트를 강제로 수행하려면 I2P router를 다시 시작해 보세요

### 중요 참고 사항

- **등록은 영구적입니다**: 등록되어 전파되면, 도메인은 영구적으로 자신의 `.b32.i2p` 주소를 가리키게 됩니다
- **목적지는 변경할 수 없습니다**: 도메인이 가리키는 `.b32.i2p` 주소는 업데이트할 수 없습니다 - 따라서 `eepPriv.dat`를 백업하는 것이 매우 중요합니다
- **도메인 소유권**: 개인 키 보유자만 도메인을 등록하거나 업데이트할 수 있습니다
- **무료 서비스**: I2P에서의 도메인 등록은 무료이며, 커뮤니티가 운영하고, 탈중앙화되어 있습니다
- **여러 등록기관**: stats.i2p와 reg.i2p 모두에 등록하면 신뢰성과 전파 속도가 향상됩니다

---

## 축하합니다!

귀하의 I2P eepsite(I2P 전용 웹사이트)가 이제 등록된 도메인과 함께 완전히 운영 중입니다!

**다음 단계**: - `docroot` 폴더에 더 많은 콘텐츠를 추가하세요 - I2P 커뮤니티와 도메인을 공유하세요 - `eepPriv.dat` 백업을 안전하게 보관하세요 - tunnel 상태를 정기적으로 모니터링하세요 - 사이트를 홍보하기 위해 I2P 포럼이나 IRC(인터넷 릴레이 채팅)에 참여하는 것을 고려하세요

I2P 네트워크에 오신 것을 환영합니다! 🎉
