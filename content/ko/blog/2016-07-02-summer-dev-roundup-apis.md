---
title: "여름 개발 총정리: API"
date: 2016-07-02
author: "str4d"
description: "In the first month of Summer Dev, we have improved the usability of our APIs for Java, Android, and Python developers."
categories: ["summer-dev"]
---

Summer Dev가 한창입니다: 우리는 바퀴에 기름칠하고, 모난 부분을 다듬고, 곳곳을 정돈하느라 분주했습니다. 이제 우리가 진행 중인 작업의 최신 상황을 알려드리는 첫 번째 요약 시간입니다!

## API의 달

이번 달 우리의 목표는 "자연스럽게 녹아드는 것" - 우리 API와 라이브러리가 다양한 커뮤니티의 기존 인프라 내에서 동작하도록 함으로써 애플리케이션 개발자들이 I2P를 더 효율적으로 활용하고, 사용자들은 세부 사항을 걱정하지 않아도 되도록 하는 것이었습니다.

### Java / Android

이제 I2P 클라이언트 라이브러리를 Maven Central에서 사용할 수 있습니다! 이로써 Java 개발자들은 애플리케이션에서 I2P를 훨씬 더 간편하게 사용할 수 있습니다. 더 이상 현재 설치본에서 라이브러리를 가져올 필요 없이, 의존성에 I2P만 추가하면 됩니다. 새 버전으로의 업그레이드도 마찬가지로 훨씬 쉬워집니다.

I2P Android 클라이언트 라이브러리도 새로운 I2P 라이브러리를 사용하도록 업데이트되었습니다. 이는 크로스 플랫폼 애플리케이션이 I2P Android 또는 데스크톱 I2P와 네이티브로 동작할 수 있음을 의미합니다.

### 자바 / 안드로이드

#### txi2p

Twisted 플러그인 `txi2p`는 이제 I2P 내부 포트(in-I2P ports)를 지원하며, 로컬, 원격, 그리고 포트 포워딩된 SAM API를 통해 원활하게 동작합니다. 사용 방법은 해당 문서를 참조하시고, 문제가 있으면 GitHub에 보고해 주십시오.

#### i2psocket

`i2psocket`의 첫 번째(베타) 버전이 릴리스되었습니다! 이는 SAM API를 통해 I2P 지원을 추가하여 표준 Python `socket` 라이브러리를 확장한, 그대로 대체해 사용할 수 있는 라이브러리입니다. 사용 방법 안내 및 이슈 보고는 해당 GitHub 페이지를 참조하세요.

### 파이썬

- zzz has been hard at work on Syndie, getting a headstart on Plugins month
- psi has been creating an I2P test network using i2pd, and in the process has found and fixed several i2pd bugs that will improve its compatibility with Java I2P

## Coming up: Apps month!

우리는 7월에 Tahoe-LAFS와 함께 협업하게 되어 매우 기쁩니다! I2P는 오랫동안 패치된 Tahoe-LAFS 버전을 사용하여 최대 규모의 공개 그리드 중 하나를 운영해 왔습니다. 앱의 달 동안 우리는 그들이 I2P와 Tor에 대한 네이티브 지원을 추가하는 지속적인 작업을 돕고, 이를 통해 I2P 사용자들이 업스트림(상위 프로젝트)의 모든 개선 사항을 누릴 수 있도록 하겠습니다.

여러 다른 프로젝트와 I2P 통합 계획을 논의하고 설계에도 협력할 예정입니다. 계속 지켜봐 주세요!

## Take part in Summer Dev!

이러한 분야에서 우리가 해내고 싶은 일들에 대한 아이디어가 더 많이 있습니다. 프라이버시 및 익명성 소프트웨어에 기여하거나, 사용하기 쉬운 웹사이트나 인터페이스를 설계하거나, 사용자 가이드를 작성하는 데 관심이 있다면 IRC 또는 Twitter에서 우리와 대화해 보세요! 우리 커뮤니티는 새로 오시는 분들을 언제나 환영합니다.

우리는 진행하는 대로 이곳에 계속 게시하겠지만, 트위터에서 해시태그 #I2PSummer를 통해 우리의 진행 상황을 확인하고 여러분의 아이디어와 작업도 공유하실 수 있습니다. 여름을 맞이합시다!
