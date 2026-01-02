---
title: "I2P 문서 작성 지침"
description: "I2P 기술 문서 전반에 걸쳐 일관성, 정확성, 접근성을 유지합니다"
slug: "writing-guidelines"
lastUpdated: "2025-10"
---

**목적:** I2P 기술 문서 전반에 걸쳐 일관성, 정확성, 접근성을 유지합니다

---

## 핵심 원칙

### 1. 모든 것을 검증하세요

**절대 가정하거나 추측하지 마십시오.** 모든 기술적 내용은 다음과 대조하여 검증해야 합니다: - 최신 I2P 소스 코드 (https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master) - 공식 API 문서 (https://i2p.github.io/i2p.i2p/  - 구성 사양 [/docs/specs/](/docs/) - 최근 릴리스 노트 [/releases/](/categories/release/)

**올바른 검증의 예:**

```markdown
❌ BAD: "The ClientApp interface probably requires three constructor parameters."
✅ GOOD: "The ClientApp interface requires this constructor signature: 
         public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)"
```
### 2. 간결성보다 명확성

I2P(익명 네트워크 프로젝트인 The Invisible Internet Project)를 처음 접할 수도 있는 개발자를 대상으로 작성하세요. 독자의 사전 지식을 가정하지 말고 개념을 충분히 설명하세요.

**예시:**

```markdown
❌ BAD: "Use the port mapper for service discovery."
✅ GOOD: "The port mapper offers a simple directory for internal TCP services. 
         Register loopback ports so other applications can discover your service 
         without hardcoded addresses."
```
### 3. 접근성 우선

I2P가 오버레이 네트워크임에도 불구하고, 문서는 clearnet(일반 인터넷)에서도 개발자가 접근할 수 있어야 합니다. I2P 내부 리소스에는 항상 clearnet에서 접근 가능한 대안을 제공해야 합니다.

---

## 기술적 정확성

### API 및 인터페이스 문서

**항상 포함할 것:** 1. 최초 언급 시 전체 패키지 이름: `net.i2p.app.ClientApp` 2. 반환 타입을 포함한 완전한 메서드 시그니처 3. 매개변수 이름과 타입 4. 필수 매개변수와 선택 매개변수 구분

**예시:**

```markdown
The `startup()` method has signature `void startup() throws IOException` and must 
execute without blocking. The method must call `ClientAppManager.notify()` at least 
once to transition from INITIALIZED state.
```
### 구성 속성

구성 파일을 문서화할 때: 1. 정확한 속성 이름을 그대로 명시한다 2. 파일 인코딩을 지정한다(I2P 구성 파일은 UTF-8) 3. 완전한 예제를 제공한다 4. 기본값을 문서화한다 5. 속성이 도입되었거나 변경된 버전을 명시한다

**예시:**

```markdown
### clients.config Properties

**Required:**
- `clientApp.N.main` - Full class name (no default)

**Optional:**
- `clientApp.N.delay` - Seconds before starting (default: 120)
- `clientApp.N.onBoot` - Forces delay=0 if true (default: false, added in 0.9.4)
```
### 상수와 열거형

상수를 문서화할 때는 실제 코드 이름을 사용하세요:

```markdown
❌ BAD: "Common registrations include console, i2ptunnel, Jetty, sam, and bob"

✅ GOOD: "Common port mapper service constants from `net.i2p.util.PortMapper`:
- `SVC_CONSOLE` - Router console (default port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (default port 4444)
- `SVC_SAM` - SAM bridge (default port 7656)"
```
### 유사한 개념을 구별하기

I2P에는 서로 겹치는 시스템이 여럿 있습니다. 어떤 시스템을 문서화하는지 항상 분명히 하세요:

**예시:**

```markdown
Note that client registry and port mapper are separate systems:
- **ClientAppManager registry** enables inter-application communication by name lookup
- **PortMapper** maps service names to host:port combinations for service discovery
- **i2ptunnel tunnel types** are configuration values (tunnel.N.type), not service registrations
```
---

## 문서 URL 및 참고 자료

### URL 접근성 규칙

1. **주요 참고 자료**는 clearnet(일반 인터넷)에서 접근 가능한 URL을 사용하는 것이 권장됩니다
2. **I2P 내부 URL**(.i2p 도메인)에는 접근성 안내를 반드시 포함해야 합니다
3. **항상 대체 링크를 제공하세요** I2P 내부 리소스에 링크할 때에는

**I2P 내부 URL용 템플릿:**

```markdown
> **Note:** The I2P network hosts comprehensive documentation at http://idk.i2p/javadoc-i2p/ 
> which requires an I2P router for access. For clearnet access, use the GitHub Pages 
> mirror at https://eyedeekay.github.io/javadoc-i2p/
```
### 권장 I2P 참고용 URL

**공식 명세:** - [구성](/docs/specs/configuration/) - [플러그인](/docs/specs/plugin/) - [문서 색인](/docs/)

**API 문서 (가장 최신 문서를 선택):** - 가장 최신: https://i2p.github.io/i2p.i2p/ (I2P 2.10.0 기준 API 0.9.66) - 클리어넷 미러: https://eyedeekay.github.io/javadoc-i2p/

**소스 코드:** - GitLab (공식): https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master - GitHub 미러: https://github.com/i2p/i2p.i2p

### 링크 형식 표준

```markdown
✅ GOOD: [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
✅ GOOD: [Configuration Specification](https://geti2p.net/spec/configuration)

❌ BAD: See the ClientApp docs at http://idk.i2p/...
❌ BAD: [link](url) with no descriptive text
```
---

## 버전 추적

### 문서 메타데이터

모든 기술 문서의 frontmatter(문서 상단의 메타데이터 블록)에는 버전 메타데이터가 포함되어야 합니다:

```markdown
---
title: "Document Title"
description: "Brief description"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
**필드 정의:** - `lastUpdated`: 문서가 마지막으로 검토/업데이트된 연-월 - `accurateFor`: 문서 검증 대상 I2P 버전 - `reviewStatus`: 다음 중 하나: "draft", "needs-review", "verified", "outdated"

### 콘텐츠의 버전 참조

버전을 언급할 때:
1. 현재 버전에는 **굵게**를 사용하세요: "**버전 2.10.0** (2025년 9월)"
2. 과거를 참조할 때는 버전 번호와 날짜를 모두 명시하세요
3. 필요할 경우 API 버전은 I2P 버전과 구분하여 명시하세요

**예시:**

```markdown
Managed clients were introduced in **version 0.9.4** (December 17, 2012) and 
remain the recommended architecture as of **version 2.10.0** (September 9, 2025). 
The current API version is **0.9.66**.
```
### 시간에 따른 변경 사항 문서화

진화한 기능의 경우:

```markdown
**Version history:**
- **0.9.4 (December 2012)** - Managed clients introduced
- **0.9.42 (2019)** - clients.config.d/ directory structure added
- **1.7.0 (2021)** - ShellService added for external program tracking
- **2.10.0 (September 2025)** - Current release, no API changes to managed clients
```
### 사용 중단 공지

사용 중단된 기능을 문서화할 때:

```markdown
> **Deprecated:** This feature was deprecated in version X.Y.Z and will be removed 
> in version A.B.C. Use [alternative feature](link) instead.
```
---

## 용어 표준

### I2P 공식 용어

다음의 정확한 용어를 일관되게 사용하세요:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct Term</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Avoid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P node, I2P client (ambiguous)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">eepsite</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P website, hidden service (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">connection, circuit (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">netDb</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">network database, DHT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lease set</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination info</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">address, endpoint</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">base64 destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P address, .i2p address</td>
    </tr>
  </tbody>
</table>
### 관리형 클라이언트 용어

관리형 클라이언트를 문서화할 때:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use This</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Not This</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed application</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unmanaged client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">legacy client, static client</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ClientAppManager</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application manager, client manager</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lifecycle methods</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">state methods, control methods</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">client registry</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application registry, name service</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port mapper</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port registry, service directory</td>
    </tr>
  </tbody>
</table>
### 구성 용어

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Incorrect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.cfg, client.config</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config.d/</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.d/, config.d/</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.cfg</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel.config</td>
    </tr>
  </tbody>
</table>
### 패키지 및 클래스 이름

처음 언급할 때는 항상 완전히 한정된 이름을 사용하고, 그 이후에는 약칭을 사용하십시오:

```markdown
The `net.i2p.app.ClientApp` interface requires implementation of three lifecycle 
methods. When a ClientApp starts, the manager calls `startup()`...
```
---

## 코드 예제와 서식

### Java 코드 예제

적절한 구문 하이라이팅과 완전한 예제를 사용하세요:

```markdown
### Example: Registering with Port Mapper

\`\`\`java
// Register HTTP proxy service
context.portMapper().register(
    PortMapper.SVC_HTTP_PROXY, 
    "127.0.0.1", 
    4444
);

// Later, retrieve the port
int port = context.portMapper().getPort(PortMapper.SVC_HTTP_PROXY);
if (port == -1) {
    // Service not registered
}
\`\`\`
```
**코드 예제 요구 사항:** 1. 핵심 코드 줄을 설명하는 주석을 포함할 것 2. 관련된 곳에서는 오류 처리를 보여줄 것 3. 현실적인 변수 이름을 사용할 것 4. I2P 코딩 규약을 따를 것 (4칸 들여쓰기) 5. 문맥상 분명하지 않은 경우 import를 명시할 것

### 구성 예제

완전하고 유효한 구성 예제를 보여 주세요:

```markdown
### Example: clients.config.d/ Entry

File: `clients.config.d/00-console.config`

\`\`\`properties
# Router console configuration
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
\`\`\`
```
### 명령줄 예제

사용자 명령에는 `$`를, root에는 `#`를 사용:

```markdown
\`\`\`bash
# Install I2P on Debian/Ubuntu
$ sudo apt-get install i2p

# Start the router
$ i2prouter start
\`\`\`
```
### 인라인 코드

다음 항목에는 백틱을 사용하세요: - 메서드 이름: `startup()` - 클래스 이름: `ClientApp` - 프로퍼티 이름: `clientApp.0.main` - 파일 이름: `clients.config` - 상수: `SVC_HTTP_PROXY` - 패키지 이름: `net.i2p.app`

---

## 톤과 보이스

### 전문적이면서도 이해하기 쉬운

기술 독자를 대상으로 하되, 가르치려 드는 어투는 피하십시오:

```markdown
❌ BAD: "Obviously, you should implement the startup() method."
✅ GOOD: "Managed clients must implement the startup() method to initialize resources."

❌ BAD: "Even a junior dev knows you need to call notify()."
✅ GOOD: "The manager requires at least one notify() call during startup to track state transitions."
```
### 능동태

명확성을 위해 능동태로 작성하세요:

```markdown
❌ PASSIVE: "The ClientAppManager is notified by the client when state changes."
✅ ACTIVE: "The client notifies ClientAppManager when state changes."
```
### 지침 작성 시 명령형 사용

절차형 콘텐츠에서는 직접 명령형을 사용하라:

```markdown
✅ "Implement these three lifecycle methods:"
✅ "Call manager.notify() after changing state."
✅ "Register services using context.portMapper().register()"
```
### 불필요한 전문 용어를 피하세요

용어는 처음 사용할 때 설명하세요:

```markdown
✅ GOOD: "The netDb (network database) stores information about I2P routers and destinations."
❌ BAD: "Query the netDb for peer info." (no explanation)
```
### 문장 부호 지침

1. **em dash(긴 대시) 금지** - 대신 일반 대시, 쉼표, 또는 세미콜론을 사용하세요
2. 목록에서는 **옥스퍼드 쉼표**를 사용하세요: "console, i2ptunnel, and Jetty"
3. **코드 블록 내부의 마침표**는 문법상 필요한 경우에만 사용하세요
4. **열거 목록**에서는 항목에 쉼표가 포함될 때 세미콜론을 사용하세요

---

## 문서 구조

### 표준 섹션 순서

API 문서는 다음을 참조하세요:

1. **개요** - 이 기능이 무엇을 하는지, 왜 존재하는지
2. **구현** - 어떻게 구현하거나 사용하는지
3. **구성** - 어떻게 설정하는지
4. **API 참조** - 메서드/속성에 대한 상세 설명
5. **예제** - 완전한 실행 가능한 예제
6. **모범 사례** - 팁과 권장 사항
7. **버전 이력** - 도입 시점과 시간에 따른 변경 사항
8. **참고 자료** - 관련 문서 링크

### 제목 계층 구조

의미에 맞는 제목 수준을 사용하세요:

```markdown
# Document Title (h1 - only one per document)

## Major Section (h2)

### Subsection (h3)

#### Detail Section (h4)

**Bold text for emphasis within sections**
```
### 정보 상자

특별 공지에는 인용문을 사용하세요:

```markdown
> **Note:** Additional information that clarifies the main content.

> **Warning:** Important information about potential issues or breaking changes.

> **Deprecated:** This feature is deprecated and will be removed in version X.Y.Z.

> **Status:** Current implementation status or version information.
```
### 목록 및 구성

**순서 없는 목록** 비순차적 항목용:

```markdown
- First item
- Second item
- Third item
```
**순서 있는 목록**은 순차적인 단계용:

```markdown
1. First step
2. Second step
3. Third step
```
**정의 목록** 용어 설명용:

```markdown
**Term One**
: Explanation of term one

**Term Two**  
: Explanation of term two
```
---

## 피해야 할 흔한 함정

### 1. 혼동되는 유사 시스템

**혼동하지 마세요:** - ClientAppManager 레지스트리 vs. PortMapper - i2ptunnel tunnel 유형 vs. 포트 매퍼 서비스 상수 - ClientApp vs. RouterApp (다른 컨텍스트) - 관리형 vs. 비관리형 클라이언트

**항상 어떤 시스템을** 논의하는지:

```markdown
✅ "Register with ClientAppManager using manager.register(this) for name-based lookup."
✅ "Register with PortMapper using context.portMapper().register() for port discovery."
```
### 2. 구버전 참조

**하지 마세요:** - 구버전을 "최신"으로 표기 - 오래된 API 문서에 링크 - 예제에서 사용 중단된 메서드 시그니처 사용

**해야 할 일:** - 게시하기 전에 릴리스 노트를 확인하세요 - API 문서가 현재 버전과 일치하는지 확인하세요 - 예제를 최신 모범 사례에 맞게 업데이트하세요

### 3. 접속할 수 없는 URL

**하지 말 것:** - 클리어넷 대체 링크가 없는 .i2p 도메인에만 링크하지 말 것 - 작동하지 않거나 오래된 문서 URL을 사용하지 말 것 - 로컬 file:// 경로로 링크하지 말 것

**해야 할 일:** - 모든 I2P 내부 링크에 대해 clearnet(일반 인터넷) 대안을 제공 - 게시하기 전에 URL이 접근 가능한지 확인 - 영속적인 URL을 사용(geti2p.net, 임시 호스팅이 아님)

### 4. 불완전한 코드 예제

**하지 말 것:** - 맥락 없이 코드 조각만 보여주기 - 오류 처리를 생략하기 - 정의되지 않은 변수를 사용하기 - 명확하지 않을 때 import 문을 생략하기

**해야 할 일:** - 완전하고 컴파일 가능한 예제를 제시하세요 - 필요한 오류 처리를 포함하세요 - 중요한 각 줄이 무엇을 하는지 설명하세요 - 게시하기 전에 예제를 테스트하세요

### 5. 모호한 진술

```markdown
❌ "Some applications register services."
✅ "Applications implementing ClientApp may register with ClientAppManager 
   using manager.register(this) to enable name-based lookup."

❌ "Configuration files go in the config directory."
✅ "Modern I2P installations store client configurations in 
   $I2P/clients.config.d/ as individual files."
```
---

## Markdown 관례

### 파일 명명

파일 이름에는 kebab-case(단어를 소문자와 하이픈(-)으로 연결하는 표기)를 사용하세요: - `managed-clients.md` - `port-mapper-guide.md` - `configuration-reference.md`

### 프론트매터 형식

항상 YAML frontmatter(문서 맨 위에 위치한 YAML 형식의 메타데이터 블록)을 포함하세요:

```yaml
---
title: "Document Title"
description: "Brief description under 160 characters"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
### 링크 서식 지정

**내부 링크** (문서 내):

```markdown
See [clients.config specification](https://geti2p.net/spec/configuration#clients-config)
```
**외부 링크** (다른 리소스로 연결):

```markdown
For more details, see [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
```
**코드 저장소 링크**:

```markdown
View source: [ClientApp.java](https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master/core/java/src/net/i2p/app/ClientApp.java)
```
### 표 서식

GitHub-flavored Markdown(확장된 GitHub 마크다운) 표를 사용하세요:

```markdown
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `main` | String | (required) | Full class name |
| `delay` | Integer | 120 | Seconds before start |
| `onBoot` | Boolean | false | Force immediate start |
```
### 코드 블록 언어 태그

구문 강조를 위해 항상 언어를 명시하세요:

```markdown
\`\`\`java
// Java code
\`\`\`

\`\`\`bash
# Shell commands
\`\`\`

\`\`\`properties
# Configuration files
\`\`\`

\`\`\`xml
<!-- XML files -->
\`\`\`
```
---

## 검토 체크리스트

문서를 게시하기 전에 다음을 확인하세요:

- [ ] 모든 기술적 주장은 소스 코드 또는 공식 문서와 대조하여 검증됨
- [ ] 버전 번호와 날짜가 최신 상태임
- [ ] 모든 URL이 clearnet(일반 인터넷)에서 접근 가능함(또는 대안이 제공됨)
- [ ] 코드 예제가 완전하고 테스트됨
- [ ] 용어가 I2P 관례를 따름
- [ ] em-dash(긴 대시) 사용 금지(일반 대시나 다른 문장부호 사용)
- [ ] Frontmatter(문서 머리말 메타데이터)가 완전하고 정확함
- [ ] 제목 계층이 의미론적임 (h1 → h2 → h3)
- [ ] 목록과 표가 올바르게 형식화됨
- [ ] 참고 문헌 섹션에 인용된 모든 출처가 포함됨
- [ ] 문서가 구조 지침을 따름
- [ ] 문체가 전문적이면서도 이해하기 쉬움
- [ ] 유사한 개념이 명확히 구분됨
- [ ] 끊어진 링크나 참조 없음
- [ ] 구성 예제가 유효하며 최신 상태임

---

**피드백:** 이 지침에 문제가 있거나 제안할 사항이 있다면, 공식 I2P 개발 채널을 통해 제출해 주세요.
