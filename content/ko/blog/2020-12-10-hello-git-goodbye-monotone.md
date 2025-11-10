---
title: "안녕 Git, 잘 가 Monotone"
date: 2020-12-10
author: "idk"
description: "git, 환영합니다; mtn, 작별을 고합니다"
categories: ["Status"]
---

## 안녕, Git. 잘 가, Monotone

### The I2P Git Migration is nearly concluded

10여 년 동안 I2P는 버전 관리 요구를 지원하기 위해 오랜 기간 신뢰받아 온 Monotone 서비스에 의존해 왔지만, 지난 몇 년 사이 전 세계의 대다수는 이제 사실상 표준이 된 Git 버전 관리 시스템으로 옮겨갔습니다.
같은 기간 동안 I2P 네트워크는 더 빨라지고 더 신뢰할 수 있게 되었으며, Git의 non-resumability(중단된 전송을 재개할 수 없는 특성)에 대응하기 위한 손쉽게 사용할 수 있는 우회책도 개발되었습니다.

오늘은 I2P에 의미 있는 날입니다. 우리는 오래된 mtn i2p.i2p branch를 종료하고, 핵심 Java I2P 라이브러리의 개발을 Monotone에서 Git으로 공식적으로 이전했습니다.

과거에 우리가 mtn을 사용한 것에 대해 의문이 제기된 적도 있었고, 그것이 항상 인기 있는 선택이었던 것도 아니지만, 아마도 Monotone을 사용하는 마지막 프로젝트로서 이 순간을 빌려, 그들이 어디에 있든 현재와 이전의 Monotone 개발자들에게 그들이 만든 소프트웨어에 대해 감사의 뜻을 전하고자 합니다.

## GPG Signing

I2P Project 저장소에 변경 사항을 반영하려면 Merge Requests와 Pull Requests를 포함한 모든 git 커밋에 대해 GPG 서명을 구성해야 합니다. i2p.i2p를 포크하고 어떤 내용을 제출하기 전에 git 클라이언트를 GPG 서명으로 설정해 주세요.

## GPG 서명

공식 저장소는 https://i2pgit.org/i2p-hackers/i2p.i2p 및 https://git.idk.i2p/i2p-hackers/i2p.i2p 에 호스팅되어 있지만, Github의 https://github.com/i2p/i2p.i2p 에서는 "Mirror"(미러)도 제공됩니다.

이제 우리가 Git을 사용하므로, 자가 호스팅된 Gitlab 인스턴스와 Github 간에 저장소를 양방향으로 동기화할 수 있습니다. 즉, Gitlab에서 Merge Request(병합 요청)를 생성하여 제출하면 병합 시 그 결과가 Github와 동기화되고, Github의 Pull Request(풀 리퀘스트)도 병합되면 Gitlab에 반영됩니다.

이는 선호에 따라 우리의 Gitlab 인스턴스 또는 Github를 통해 코드를 제출할 수 있다는 의미입니다. 다만 I2P 개발자들은 Github보다 Gitlab을 더 자주 모니터링합니다. Gitlab로 제출된 MR이 Github로 제출된 PR보다 더 빨리 병합될 가능성이 높습니다.

## Thanks

Git 마이그레이션에 도움을 주신 모든 분들께 축하와 감사를 전합니다. 특히 zzz, eche|on, nextloop, 그리고 우리 사이트 미러 운영자 여러분께 감사드립니다! 우리 중 일부는 Monotone을 아쉬워하겠지만, 그것은 I2P 개발에 새로 참여하는 이들과 기존 참여자들에게 장벽이 되어 왔고, 우리는 분산형 프로젝트를 관리하는 데 Git을 사용하는 개발자들의 세계에 합류하게 되어 기쁘게 생각합니다.
