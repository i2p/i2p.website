---
title: "신규 개발자 가이드"
description: "I2P에 기여를 시작하는 방법: 학습 자료, 소스 코드, 빌드, 아이디어, 게시, 커뮤니티, 번역 및 도구"
slug: "new-developers"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
notes: 번역 부분 업데이트
---

I2P 작업을 시작하고 싶으신가요? 좋습니다! 여기 웹사이트나 소프트웨어에 기여하고, 개발을 하거나, 번역을 만드는 것을 시작하기 위한 간단한 가이드가 있습니다.

아직 코딩할 준비가 되지 않으셨나요? 먼저 [참여하기](/get-involved/)를 시도해 보세요.

## Java 알아보기

I2P router와 내장 애플리케이션은 Java를 주요 개발 언어로 사용합니다. Java 경험이 없다면 [Thinking in Java](https://chenweixiang.github.io/docs/Thinking_in_Java_4th_Edition.pdf)를 참고하실 수 있습니다

how intro, 다른 "how" 문서들, tech intro, 그리고 관련 문서들을 학습하세요:

- 소개 방법: [I2P 소개](/docs/overview/intro/)
- 문서 허브: [문서](/docs/)
- 기술 소개: [기술 소개](/docs/overview/tech-intro/)

이를 통해 I2P가 어떻게 구성되어 있고 어떤 다양한 기능을 수행하는지 전반적으로 잘 이해할 수 있습니다.

## I2P 코드 가져오기

I2P router 또는 내장된 애플리케이션 개발을 위해서는 소스 코드를 가져와야 합니다.

### 우리의 현재 방식: Git

I2P는 자체 GitLab에서 공식 Git 서비스를 제공하며 Git을 통한 기여를 받습니다:

- I2P 내부: <http://git.idk.i2p>
- I2P 외부: <https://i2pgit.org>

메인 저장소를 클론하세요:

```
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
```
읽기 전용 미러도 GitHub에서 이용 가능합니다:

- GitHub 미러: [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p)

```
git clone https://github.com/i2p/i2p.i2p.git
```
## I2P 빌드하기

코드를 컴파일하려면 Sun/Oracle Java Development Kit 6 이상 또는 동등한 JDK(Sun/Oracle JDK 6 강력 권장)와 Apache Ant 버전 1.7.0 이상이 필요합니다. 메인 I2P 코드 작업을 진행 중이라면 `i2p.i2p` 디렉토리로 이동하여 `ant`를 실행하면 빌드 옵션을 확인할 수 있습니다.

콘솔 번역을 빌드하거나 작업하려면 GNU gettext 패키지의 `xgettext`, `msgfmt`, `msgmerge` 도구가 필요합니다.

새로운 애플리케이션 개발에 대해서는 [애플리케이션 개발 가이드](/docs/develop/applications/)를 참조하세요.

## 개발 아이디어

아이디어를 얻으려면 프로젝트 TODO 목록이나 GitLab의 이슈 목록을 참조하세요:

- GitLab 이슈: [i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)

## 결과를 공개하기

커밋 권한 요구사항은 라이선스 페이지 하단을 참조하세요. `i2p.i2p`에 코드를 넣으려면 이 권한이 필요합니다 (웹사이트는 필요 없습니다!).

- [라이선스 페이지](/docs/develop/licenses#commit)

## 저희를 알아가세요!

개발자들은 IRC에 상주하고 있습니다. 다양한 네트워크와 I2P 내부 네트워크에서 연락할 수 있습니다. 일반적으로 `#i2p-dev` 채널을 찾아보세요. 채널에 접속해서 인사하세요! 정규 개발자를 위한 추가 [가이드라인](/docs/develop/dev-guidelines/)도 있습니다.

##

웹사이트 및 라우터 콘솔 번역가: 다음 단계는 [신규 번역가 가이드](/docs/develop/new-translators/)를 참조하세요.

## 도구

I2P는 대부분 오픈소스 툴킷을 사용하여 개발되는 오픈소스 소프트웨어입니다. I2P 프로젝트는 최근 YourKit Java Profiler 라이선스를 취득했습니다. 오픈소스 프로젝트는 프로젝트 웹사이트에서 YourKit을 언급하는 조건으로 무료 라이선스를 받을 수 있습니다. I2P 코드베이스 프로파일링에 관심이 있으시면 연락 주시기 바랍니다.

YourKit은 풀 기능 프로파일러로 오픈 소스 프로젝트를 친절하게 지원하고 있습니다. YourKit, LLC는 Java 및 .NET 애플리케이션 프로파일링을 위한 혁신적이고 지능적인 도구를 만드는 회사입니다. YourKit의 선도적인 소프트웨어 제품을 살펴보세요:

- [YourKit Java Profiler](http://www.yourkit.com/java/profiler/index.jsp)
- [YourKit .NET Profiler](http://www.yourkit.com/.net/profiler/index.jsp)
