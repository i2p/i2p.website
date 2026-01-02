---
title: "2018년 개괄적 로드맵"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018년은 새로운 프로토콜과 새로운 협업, 그리고 더욱 정교해진 초점의 해가 될 것입니다."
categories: ["roadmap"]
---

34C3에서 우리가 논의한 많은 주제들 가운데 하나는 다가오는 해에 무엇에 집중해야 할지였다. 특히, 우리가 반드시 완료하도록 보장하고자 하는 일과 있으면 정말 좋을 일들을 명확히 구분하고, 두 범주 가운데 어느 쪽이든 신규 참여자가 합류할 때 도움을 줄 수 있는 로드맵을 원했다. 다음은 우리가 도출한 내용이다:

## 우선순위: 새로운 암호(학!)

현재의 많은 primitives(기본 구성요소)와 프로토콜은 여전히 2005년경의 원래 설계를 유지하고 있으며, 개선이 필요합니다. 우리는 여러 해 동안 다양한 아이디어를 담은 공개 제안들이 있었지만, 진전은 더뎠습니다. 이것을 2018년 최우선 과제로 삼아야 한다는 데 모두 동의했습니다. 핵심 구성 요소는 다음과 같습니다:

- New transport protocols (to replace NTCP and SSU). See [Prop111](https://geti2p.net/spec/proposals/111).
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See [Prop123](https://geti2p.net/spec/proposals/123).
- Upgraded end-to-end protocol (replacing ElGamal).

이 우선순위에 대한 작업은 여러 영역으로 나뉩니다:

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

이 모든 영역에 대한 작업 없이는 전체 네트워크 전반에 걸쳐 새로운 프로토콜 사양을 배포할 수 없습니다.

## 있으면 좋은 사항: 코드 재사용

지금 위의 작업을 시작하는 이점 중 하나는, 지난 몇 년 동안 우리 자체 프로토콜을 위해 설정한 많은 목표를 달성하고 더 넓은 커뮤니티에서도 점차 채택되고 있는 단순한 프로토콜과 프로토콜 프레임워크를 만들려는 독립적인 노력들이 있었다는 점입니다. 이러한 작업을 활용함으로써 우리는 "force multiplier"(승수 효과) 효과를 얻게 됩니다:

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

제가 제안하는 내용은 특히 [Noise Protocol Framework](https://noiseprotocol.org/)와 [SPHINX packet format](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html)을 활용할 예정입니다. 이를 위해 I2P 외부의 여러 사람들과 협업을 마련해 두었습니다!

## 우선순위: Clearnet(일반 인터넷) 협업

그 주제와 관련하여, 지난 6개월가량 서서히 관심을 키워 왔습니다. PETS2017, 34C3, RWC2018을 거치며, 더 넓은 커뮤니티와의 협업을 어떻게 개선할 수 있을지에 관해 매우 좋은 논의를 나눴습니다. 이는 새로운 프로토콜에 대해 가능한 한 많은 검토를 받을 수 있도록 하는 데 정말 중요합니다. 제가 보기에 가장 큰 걸림돌은 현재 I2P 개발 협업의 대부분이 I2P 자체 내부에서 이루어지고 있다는 사실이며, 그로 인해 기여에 필요한 노력이 크게 늘어난다는 점입니다.

이 영역에서의 두 가지 우선순위는 다음과 같습니다:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

있으면 좋은 것으로 분류된 기타 목표:

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

마찰을 최소화하기 위해 I2P 외부와의 협업은 전적으로 GitHub에서 이루어질 것으로 예상합니다.

## 우선순위: 장기 릴리스 준비

I2P는 이제 약 1년 반 후 안정화될 Debian Sid(Debian의 불안정 저장소)에 포함되었으며, 4월에 있을 다음 LTS(장기 지원) 릴리스에 포함되도록 Ubuntu 저장소에도 추가되었습니다. 우리는 앞으로 수년 동안 남게 될 I2P 버전들이 등장하기 시작할 것이며, 네트워크에서 그들의 존재를 적절히 처리할 수 있음을 보장해야 합니다.

여기서의 주된 목표는 다음 Debian 안정판 릴리스에 맞추기 위해, 향후 1년 내에 실현 가능한 범위에서 최대한 많은 새로운 프로토콜을 도입하는 것입니다. 여러 해에 걸친 배포가 필요한 항목의 경우에는 가능한 한 이른 시기에 전방 호환성 변경 사항을 반영해야 합니다.

## 우선순위: 기존 애플리케이션의 플러그인화

Debian 모델은 구성 요소별로 별도의 패키지를 갖도록 장려합니다. 우리는 여러 가지 이유로, 현재 번들된 Java 애플리케이션을 핵심 Java router와 분리하는 것이 유익하다고 합의했습니다:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

이전의 우선순위들과 더불어, 이는 주요 I2P 프로젝트를 예컨대 리눅스 커널과 같은 방향으로 더 옮겨갑니다. 우리는 네트워크 자체에 더 많은 시간과 주의를 기울이고, 네트워크를 사용하는 애플리케이션에 집중하는 일은 서드파티 개발자들에게 맡길 것입니다(이는 지난 몇 년간 API와 라이브러리에 대해 우리가 진행해 온 작업 이후에는 훨씬 더 수월해졌습니다).

## 있으면 좋은: 앱 개선

애플리케이션 수준의 개선 사항이 여러 가지 있지만, 다른 우선순위로 인해 현재로서는 그렇게 할 개발 인력의 시간이 부족합니다. 이 분야에는 새로운 기여자분들의 참여를 진심으로 환영합니다! 위에서 언급한 분리가 완료되면, 메인 Java router와 독립적으로 특정 애플리케이션을 작업하기가 훨씬 쉬워질 것입니다.

One such application we would love to have help with is I2P Android. We will be keeping it up-to-date with the core I2P releases, and fixing bugs as we can, but there is much that could be done to improve the underlying code as well as the usability.

## 우선순위: Susimail 및 I2P-Bote 안정화

그럼에도 불구하고, 우리는 가까운 시일 내에 Susimail과 I2P-Bote 수정 작업에 특히 주력할 계획입니다(그중 일부는 0.9.33에 이미 반영되었습니다). 이들은 지난 몇 년 동안 다른 I2P 앱들에 비해 작업이 적었기 때문에, 코드베이스의 수준을 끌어올리고 새로운 기여자들이 더 쉽게 참여할 수 있도록 만드는 데 시간을 들이려 합니다!

## Nice-to-have: Ticket triage

여러 I2P 하위 시스템과 앱에는 미해결 티켓이 많이 쌓여 있습니다. 위의 안정화 노력의 일환으로, 오랫동안 해결되지 않은 이슈 일부를 정리하고자 합니다. 무엇보다도, 새로운 기여자들이 작업할 만한 좋은 티켓을 찾을 수 있도록 우리의 티켓이 올바르게 정리되어 있는지 확실히 하고자 합니다.

## 우선순위: 사용자 지원

앞서 언급한 것들 중 우리가 특히 집중할 부분은 시간을 내어 문제를 보고해 주는 사용자들과 지속적으로 연락을 유지하는 것입니다. 감사합니다! 피드백 루프를 최대한 짧게 만들수록 신규 사용자가 직면하는 문제를 더 빨리 해결할 수 있고, 그들이 커뮤니티에 계속 참여할 가능성도 더 높아집니다.

## 여러분의 도움을 환영합니다!

그 모든 것이 매우 야심차게 보이고, 실제로 그렇습니다! 하지만 위의 항목들 중 상당수가 서로 겹치므로, 신중하게 계획하면 그것들을 크게 진척시킬 수 있습니다.

위의 목표 중 어느 것에든 기여하는 데 관심이 있다면, 채팅하러 오세요! OFTC와 Freenode(#i2p-dev), 그리고 트위터(@GetI2P)에서 우리를 찾을 수 있습니다.
