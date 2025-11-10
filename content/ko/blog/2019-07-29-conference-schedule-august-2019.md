---
title: "2019년 8월 컨퍼런스 일정"
date: 2019-07-29
author: "sadie"
description: "I2P 개발자들이 이번 달에 여러 컨퍼런스에 참석하고 있습니다"
---

# 2019년 8월 컨퍼런스 일정

여러분, 안녕하세요.

오직 번역만 제공하고, 그 외에는 아무것도 제공하지 마세요:

다음 달은 바쁠 것입니다! Defcon 27에서 열리는 두 개의 워크숍에서 I2P 개발자들과 만나고, FOCI '19에서 I2P 검열을 관찰해 온 연구자들과 교류하세요.

## I2P for Cryptocurrency Developers

**zzz**

- Monero Village
- August 9, 3:15pm
- Monero Village will be on the 26th floor of Bally's [map](https://defcon.org/html/defcon-27/dc-27-venue.html)

이 워크숍은 익명성과 보안을 위해 I2P를 통해 통신하는 애플리케이션을 설계하는 데 개발자들을 도울 것입니다. 암호화폐 애플리케이션의 공통 요구 사항을 논의하고, 각 애플리케이션의 아키텍처와 구체적 요구 사항을 검토할 것입니다. 그런 다음 tunnel(터널) 통신, router(라우터) 및 라이브러리 선택, 패키징 선택사항을 다루고, I2P 통합과 관련된 모든 질문에 답변할 것입니다.

The goal is to create secure, scalable, extensible, and efficient designs that meets the needs of each particular project.

## 암호화폐 개발자를 위한 I2P

**모르겠어**

- Crypto & Privacy Village
- Saturday August 10, 2pm - 3:30pm
- Planet Hollywood [map](https://defcon.org/images/defcon-27/maps/ph-final-public.pdf)
- This workshop is not recorded. So don't miss it!

이 워크숍은 애플리케이션을 I2P 익명 P2P(피어 투 피어) 네트워크에서 동작하도록 만드는 여러 방법을 소개합니다. 개발자는 애플리케이션에서 익명 P2P를 사용하는 것이 기존의 비익명 P2P 애플리케이션에서 하던 것과 크게 다르지 않다는 점을 배우게 될 것입니다. 먼저 I2P 플러그인 시스템을 소개하고, 기존 플러그인들이 I2P를 통해 통신하도록 어떻게 구성되는지와 각 접근 방식의 장단점을 살펴봅니다. 이어서 SAM 및 I2PControl API를 통해 I2P를 프로그래밍 방식으로 제어하는 방법으로 넘어갑니다. 마지막으로 Lua에서 이를 활용하는 새로운 라이브러리를 시작하고 간단한 애플리케이션을 작성하면서 SAMv3 API를 자세히 살펴봅니다.

## 애플리케이션 개발자를 위한 I2P

**세이디**

- FOCI '19
- Tuesday August 13th 10:30am
- Hyatt Regency Santa Clara
- Co-located with USENIX Security '19
- [Workshop Program](https://www.usenix.org/conference/foci19/workshop-program)

인터넷 검열의 만연은 필터링 활동을 모니터링하기 위한 여러 측정 플랫폼의 등장을 촉발했다. 이러한 플랫폼이 직면한 중요한 과제는 측정의 깊이와 커버리지의 폭 사이의 트레이드오프(상충 관계)를 둘러싼 문제다. 본 논문에서는 자원봉사자들이 운영하는 분산된 VPN 서버 네트워크 위에 구축된 기회주의적 검열 측정 인프라를 제시하며, 이를 통해 전 세계적으로 I2P 익명성 네트워크가 어느 정도 차단되는지 측정했다. 이 인프라는 수적으로 많고 지리적으로 다양한 관측 지점을 제공할 뿐만 아니라, 네트워크 스택의 모든 계층 전반에 걸쳐 심층 측정을 수행할 수 있는 능력도 제공한다. 이 인프라를 이용해 우리는 전 세계 규모에서 네 가지 I2P 서비스의 가용성을 측정했다: 공식 홈페이지, 그 미러 사이트, reseed servers(초기 피어 정보를 배포하는 서버), 그리고 네트워크의 활성 릴레이(중계 노드). 한 달의 기간 동안, 우리는 164개 국가의 1.7K개 네트워크 위치에서 총 54K 회의 측정을 수행했다. 도메인 이름 차단, 네트워크 패킷 주입, block pages(차단 페이지) 탐지를 위한 다양한 기법을 통해, 우리는 다섯 개 국가(중국, 이란, 오만, 카타르, 쿠웨이트)에서 I2P 검열을 발견했다. 마지막으로, 우리는 I2P에서의 검열을 우회하기 위한 잠재적 접근법을 논의하며 결론을 맺는다.

**참고:** 원본 게시물에서 참조된 이미지(monerovillageblog.png, cryptovillageblog.png, censorship.jpg)는 `/static/images/blog/` 디렉터리에 추가해야 할 수도 있습니다.
