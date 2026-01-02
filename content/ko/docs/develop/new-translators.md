---
title: "새로운 번역자 안내서"
description: "Transifex 또는 수동 방식을 사용하여 I2P 웹사이트 및 router console 번역에 기여하는 방법"
slug: "new-translators"
lastUpdated: "2025-10"
type: docs
---

전 세계 더 많은 사람들이 I2P에 접근할 수 있도록 돕고 싶으신가요? 번역은 프로젝트에 기여할 수 있는 가장 가치 있는 방법 중 하나입니다. 이 가이드는 router console을 번역하는 과정을 안내합니다.

## 번역 방법

번역에 기여하는 방법은 두 가지가 있습니다:

### 방법 1: Transifex (권장)

**이것은 I2P를 번역하는 가장 쉬운 방법입니다.** Transifex는 번역을 간단하고 접근하기 쉽게 만드는 웹 기반 인터페이스를 제공합니다.

1. [Transifex](https://www.transifex.com/otf/I2P/)에 가입하세요
2. I2P 번역 팀 가입을 요청하세요
3. 브라우저에서 직접 번역을 시작하세요

기술적 지식이 필요하지 않습니다 - 지금 가입하고 번역을 시작하세요!

### 방법 2: 수동 번역

git과 로컬 파일 작업을 선호하는 번역가나 Transifex에 아직 설정되지 않은 언어를 위한 방법입니다.

**요구 사항:** - git 버전 관리에 대한 이해 - 텍스트 편집기 또는 번역 도구 (POEdit 권장) - 명령줄 도구: git, gettext

**설정:** 1. [IRC의 #i2p-dev](/contact/#irc)에 참여하여 자신을 소개하세요 2. 위키에서 번역 상태를 업데이트하세요 (IRC에서 접근 권한 요청) 3. 적절한 저장소를 클론하세요 (아래 섹션 참조)

---

## 라우터 콘솔 번역

router console은 I2P를 실행할 때 보이는 웹 인터페이스입니다. 이를 번역하면 영어가 익숙하지 않은 사용자들에게 도움이 됩니다.

### Transifex 사용하기 (권장)

1. [Transifex의 I2P](https://www.transifex.com/otf/I2P/)로 이동하세요
2. router console 프로젝트를 선택하세요
3. 언어를 선택하세요
4. 번역을 시작하세요

### 수동 라우터 콘솔 번역

**전제 조건:** - 웹사이트 번역과 동일 (git, gettext) - GPG 키 (커밋 접근 권한용) - 서명된 개발자 동의서

**메인 I2P 저장소 복제하기:**

```bash
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
cd i2p.i2p
```
**번역할 파일:**

router console에는 번역이 필요한 약 15개의 파일이 있습니다:

1. **핵심 인터페이스 파일:**
   - `apps/routerconsole/locale/messages_*.po` - 메인 콘솔 메시지
   - `apps/routerconsole/locale-news/messages_*.po` - 뉴스 메시지

2. **프록시 파일:**
   - `apps/i2ptunnel/locale/messages_*.po` - 터널 구성 인터페이스

3. **애플리케이션 로케일:**
   - `apps/susidns/locale/messages_*.po` - 주소록 인터페이스
   - `apps/susimail/locale/messages_*.po` - 이메일 인터페이스
   - 기타 앱별 로케일 디렉토리

4. **문서 파일:**
   - `installer/resources/readme/readme_*.html` - 설치 안내문
   - 다양한 앱의 도움말 파일

**번역 작업 흐름:**

```bash
# Update .po files from source
ant extractMessages

# Edit .po files with POEdit or text editor
poedit apps/routerconsole/locale/messages_es.po

# Build and test
ant updaters
# Install the update and check translations in the console
```
**작업 제출하기:** - [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p)에서 병합 요청 생성 - 또는 IRC에서 개발 팀과 파일 공유

---

## 번역 도구

### POEdit (강력 권장)

[POEdit](https://poedit.net/)는 .po 번역 파일 전용 편집기입니다.

**기능:** - 번역 작업을 위한 시각적 인터페이스 - 번역 컨텍스트 표시 - 자동 검증 - Windows, macOS, Linux에서 사용 가능

### 텍스트 편집기

다음과 같은 텍스트 편집기를 사용할 수도 있습니다: - VS Code (i18n 확장 프로그램 포함) - Sublime Text - vim/emacs (터미널 사용자용)

### 품질 검사

제출하기 전에: 1. **형식 확인:** `%s` 및 `{0}`와 같은 플레이스홀더가 변경되지 않았는지 확인 2. **번역 테스트:** I2P를 설치하고 실행하여 번역이 어떻게 표시되는지 확인 3. **일관성:** 파일 전체에서 용어를 일관되게 유지 4. **길이:** 일부 문자열은 UI에서 공간 제약이 있음

---

## 번역자를 위한 팁

### 일반 지침

- **일관성 유지:** 문서 전체에서 일반적인 용어에 대해 동일한 번역을 사용하세요
- **형식 유지:** HTML 태그, 플레이스홀더(`%s`, `{0}`), 줄 바꿈을 그대로 유지하세요
- **맥락이 중요합니다:** 맥락을 이해하기 위해 원본 영어를 주의 깊게 읽으세요
- **질문하기:** 불확실한 사항이 있으면 IRC나 포럼을 이용하세요

### 일반적인 I2P 용어

일부 용어는 영어로 유지하거나 신중하게 음역해야 합니다:

- **I2P** - Keep as is
- **eepsite** - I2P 웹사이트 (I2P 네트워크 내의 웹사이트)
- **tunnel** - 연결 경로 (Tor 용어인 "circuit"과 혼동 방지)
- **netDb** - 네트워크 데이터베이스
- **floodfill** - 라우터 유형
- **destination** - I2P 주소 엔드포인트

### 번역 테스트하기

1. 번역을 포함하여 I2P를 빌드합니다
2. router console 설정에서 언어를 변경합니다
3. 모든 페이지를 탐색하여 다음을 확인합니다:
   - UI 요소에 텍스트가 적절히 표시되는지
   - 깨진 문자가 없는지 (인코딩 문제)
   - 문맥상 번역이 자연스러운지

---

## 자주 묻는 질문

### 왜 번역 과정이 그렇게 복잡한가요?

이 프로세스는 버전 관리(git)와 표준 번역 도구(.po 파일)를 사용합니다. 그 이유는:

1. **책임성:** 누가 무엇을 언제 변경했는지 추적
2. **품질:** 변경 사항이 적용되기 전에 검토
3. **일관성:** 적절한 파일 형식과 구조 유지
4. **확장성:** 여러 언어에 걸친 번역을 효율적으로 관리
5. **협업:** 여러 번역자가 동일한 언어 작업 가능

### 프로그래밍 기술이 필요한가요?

**아니오!** Transifex를 사용하는 경우, 다음만 있으면 됩니다: - 영어와 목표 언어 모두에 대한 유창함 - 웹 브라우저 - 기본적인 컴퓨터 사용 능력

수동 번역의 경우 기본적인 명령줄 지식이 필요하지만 코딩은 필요하지 않습니다.

### 얼마나 걸리나요?

- **Router console:** 모든 파일에 대해 약 15-20시간
- **유지보수:** 새로운 문자열을 업데이트하는 데 월 몇 시간

### 여러 사람이 하나의 언어를 함께 작업할 수 있나요?

네! 조율이 핵심입니다: - 자동 조율을 위해 Transifex를 사용하세요 - 수동 작업의 경우 #i2p-dev IRC 채널에서 소통하세요 - 섹션 또는 파일별로 작업을 분담하세요

### 내 언어가 목록에 없으면 어떻게 하나요?

Transifex에서 요청하거나 IRC로 팀에 연락하세요. 개발팀이 새로운 언어를 빠르게 설정할 수 있습니다.

### 제출하기 전에 번역을 어떻게 테스트하나요?

- 번역된 파일로 I2P를 소스에서 빌드하기
- 로컬에 설치하고 실행하기
- 콘솔 설정에서 언어 변경하기

---

## 도움 받기

### IRC 지원

다음을 위해 [IRC의 #i2p-dev](/contact/#irc)에 참여하세요: - 번역 도구 관련 기술 지원 - I2P 용어에 대한 질문 - 다른 번역자들과의 협업 - 개발자로부터 직접 지원받기

### 포럼

- [I2P Forums](http://i2pforum.net/)의 번역 논의
- Inside I2P: zzz.i2p의 번역 포럼 (I2P router 필요)

### 문서

- [Transifex 문서](https://docs.transifex.com/)
- [POEdit 문서](https://poedit.net/support)
- [gettext 매뉴얼](https://www.gnu.org/software/gettext/manual/)

---

## 인정

모든 번역자는 다음에 표시됩니다: - I2P router 콘솔 (정보 페이지) - 웹사이트 크레딧 페이지 - Git 커밋 히스토리 - 릴리스 공지사항

당신의 작업은 전 세계 사람들이 I2P를 안전하고 사적으로 사용하는 데 직접적인 도움이 됩니다. 기여해 주셔서 감사합니다!

---

## 다음 단계

번역을 시작할 준비가 되셨나요?

1. **방법을 선택하세요:**
   - 빠른 시작: [Transifex에서 가입하기](https://www.transifex.com/otf/I2P/)
   - 수동 방식: [IRC의 #i2p-dev](/contact/#irc)에 참여하기

2. **작게 시작하세요:** 프로세스에 익숙해지기 위해 몇 개의 문자열을 번역하세요

3. **도움 요청하기:** IRC나 포럼에서 주저하지 말고 연락하세요

**I2P를 모두가 접근할 수 있도록 만드는 데 도움을 주셔서 감사합니다!**
