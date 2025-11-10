---
title: "I2P Jpackages가 첫 업데이트를 받았습니다"
date: 2021-11-02
author: "idk"
description: "설치가 더 쉬운 새 패키지가 새로운 이정표를 달성했습니다"
categories: ["general"]
---

몇 달 전 더 많은 사람이 I2P의 설치와 구성을 더 쉽게 할 수 있도록 하여 새로운 사용자가 I2P 네트워크에 합류하는 데 도움이 되기를 바라며 새로운 패키지를 출시했습니다. 외부 JVM에서 Jpackage(Java 패키징 도구)로 전환하고, 대상 운영 체제용 표준 패키지를 빌드했으며, 운영 체제가 인식할 수 있는 방식으로 서명하여 사용자 보안을 유지함으로써 설치 과정의 수십 단계를 제거했습니다. 그 이후 jpackage router들은 새로운 이정표에 도달했으며, 곧 첫 번째 증분 업데이트를 받게 됩니다. 이번 업데이트는 JDK 16 jpackage를 업데이트된 JDK 17 jpackage로 교체하고, 릴리스 이후에 발견된 몇 가지 작은 버그에 대한 수정도 제공합니다.

## Mac OS와 Windows에 공통적인 업데이트

jpackage로 패키징된 모든 I2P 설치 프로그램은 다음 업데이트를 받습니다:

* Update the jpackaged I2P router to 1.5.1 which is built with JDK 17

가능한 한 빨리 업데이트해 주십시오.

## I2P Windows Jpackage 업데이트

Windows 전용 패키지에는 다음 업데이트가 적용됩니다:

* Updates I2P in Private Browsing, NoScript browser extensions
* Begins to phase out HTTPS everywhere on new Firefox releases
* Updates launcher script to fix post NSIS launch issue on some architectures

전체 변경 내역은 i2p.firefox의 changelog.txt를 참조하세요.

## I2P Mac OS Jpackage 업데이트

Mac OS 전용 패키지는 다음 업데이트를 받습니다:

* No Mac-Specific changes. Mac OS is updated to build with JDK 17.

개발 요약은 i2p-jpackage-mac의 체크인 내역을 참조하세요.
