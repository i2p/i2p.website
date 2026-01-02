---
title: "2018년을 위한 상위 수준 로드맵"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018년은 새로운 프로토콜, 새로운 협력, 그리고 더욱 정교해진 초점의 해가 될 것입니다."
categories: ["roadmap"]
---

34C3에서 논의한 많은 주제들 가운데 하나는 다가오는 한 해에 무엇에 집중해야 하는가였습니다. 특히, 반드시 해내야 할 일과 있으면 정말 좋을 일을 명확히 구분한 로드맵을 원했고, 두 범주 모두에 신규 참여자들이 쉽게 참여할 수 있도록 돕고자 했습니다. 우리가 도출한 내용은 다음과 같습니다:

## 우선순위: 새로운 암호학!

현재의 많은 primitives(기본 구성 요소)와 프로토콜은 여전히 2005년경의 원래 설계를 유지하고 있으며, 개선이 필요합니다. 우리는 여러 해 동안 다양한 아이디어를 담은 공개 제안들을 가지고 있었지만, 진척은 더뎠습니다. 우리 모두는 2018년에 이것을 최우선 과제로 삼아야 한다는 데 동의했습니다. 핵심 구성 요소는 다음과 같습니다:

- New transport protocols (to replace NTCP and SSU). See Prop111.
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See Prop123.
- Upgraded end-to-end protocol (replacing ElGamal).

이 우선순위를 위한 작업은 여러 영역으로 나뉩니다:

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

이 모든 영역에서의 작업 없이는 네트워크 전체에 걸쳐 새로운 프로토콜 사양을 배포할 수 없습니다.

## 있으면 좋은 사항: 코드 재사용

위의 작업을 지금 시작하는 이점 중 하나는, 지난 몇 년간 우리 자체 프로토콜을 위한 많은 목표를 달성하는 데 적합한 단순한 프로토콜과 프로토콜 프레임워크를 만들려는 독립적인 노력들이 있었고, 그것들이 더 넓은 커뮤니티에서 입지를 다져 왔다는 점입니다. 이러한 작업을 활용하면 우리는 "시너지 효과"를 얻을 수 있습니다:

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

특히 제 제안들은 [Noise Protocol Framework](https://noiseprotocol.org/) 및 [SPHINX packet format](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html)을 활용할 것입니다. 이들 제안을 위해 I2P 외부의 여러 사람들과 협업을 준비해 두었습니다!

## 우선순위: 클리어넷 협력

그 주제와 관련해, 지난 6개월가량에 걸쳐 우리는 서서히 관심을 키워 왔습니다. PETS2017, 34C3, RWC2018을 거치며 더 넓은 커뮤니티와의 협업을 어떻게 개선할 수 있을지에 대해 매우 좋은 논의를 나눴습니다. 이는 새로운 프로토콜에 대해 가능한 한 많은 검토를 받아낼 수 있도록 하는 데 정말로 중요합니다. 제가 보기에 가장 큰 걸림돌은 현재 I2P 개발 협업의 대다수가 I2P 내부에서 이루어지고 있다는 사실이며, 그로 인해 기여에 필요한 노력이 크게 늘어난다는 점입니다.

이 분야에서의 두 가지 우선순위는 다음과 같습니다:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

‘있으면 좋은’ 범주로 분류되는 기타 목표:

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

마찰을 최소화하기 위해 I2P 외부의 사람들과의 협업은 전적으로 GitHub에서 진행될 것으로 예상합니다.

## 우선순위: 장기 릴리스를 위한 준비

I2P는 이제 약 1년 반 후에 안정화될 Debian Sid(불안정 저장소)에 포함되었으며, 4월의 다음 LTS(장기 지원) 릴리스에 포함되도록 Ubuntu 저장소에도 포함되었습니다. 앞으로 수년간 남아 있게 될 I2P 버전들이 나오기 시작할 것이며, 네트워크에서 해당 버전들의 존재를 적절히 처리할 수 있음을 보장해야 합니다.

여기에서의 주요 목표는 다음 1년 동안 현실적으로 가능한 한 많은 새로운 프로토콜을 도입하여 다음 Debian 안정 릴리스에 맞추는 것입니다. 수년에 걸친 도입이 필요한 항목의 경우, 가능한 한 이른 시점에 forward-compatibility(전방 호환성) 변경 사항을 포함해야 합니다.

## 우선순위: 기존 앱의 플러그인화

Debian 모델은 구성 요소별로 별도의 패키지를 두는 것을 장려합니다. 우리는 현재 번들된 Java 애플리케이션을 핵심 Java router와 분리하는 것이 여러 가지 이유로 유익하다는 데 동의했습니다:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

이전의 우선순위들과 결합하면, 이는 주요 I2P 프로젝트를 예를 들어 Linux kernel과 같은 방향으로 더 나아가게 합니다. 우리는 네트워크 그 자체에 더 많은 시간을 들여 집중하고, 네트워크를 사용하는 애플리케이션에 집중하는 일은 서드파티 개발자들에게 맡길 것입니다(이는 지난 몇 년 동안 API와 라이브러리에 대해 우리가 진행한 작업 이후로 수행하기가 훨씬 쉬워졌습니다).

## 있으면 좋을 사항: 앱 개선

앱 수준의 개선 사항들이 여러 가지 있지만, 다른 우선순위들로 인해 이를 진행할 개발 리소스가 현재는 부족합니다. 이 분야에는 새로운 기여자가 참여해 주시면 정말 반갑겠습니다! 위의 디커플링이 완료되면, 주요 Java router와 독립적으로 특정 애플리케이션을 작업하기가 훨씬 쉬워질 것입니다.

여러분의 도움을 받고 싶은 애플리케이션 중 하나는 I2P Android입니다. 우리는 핵심 I2P 릴리스에 맞춰 이를 최신 상태로 유지하고 가능한 한 버그를 수정하겠지만, 기반 코드와 사용성을 개선하기 위해 할 수 있는 일이 아직 많이 남아 있습니다.

## Priority: Susimail and I2P-Bote stabilisation

그럼에도 불구하고, 우리는 단기적으로 Susimail과 I2P-Bote의 수정 작업에 특히 집중하고자 합니다(그중 일부는 0.9.33에 반영되었습니다). 지난 몇 년간 이들은 다른 I2P 앱들보다 작업이 덜 이루어졌기 때문에, 코드베이스를 동등한 수준으로 끌어올리고 새로운 기여자들이 쉽게 참여할 수 있도록 만드는 데 시간을 들이려 합니다!

## 있으면 좋은: 티켓 트리아지(우선순위 분류)

여러 I2P 서브시스템과 앱에서 티켓이 대거 백로그로 쌓여 있습니다. 위에서 언급한 안정화 노력의 일환으로, 장기화된 이슈들 중 일부를 정리하고자 합니다. 더 중요한 것은, 새로운 기여자들이 작업할 만한 좋은 티켓을 찾을 수 있도록 우리의 티켓을 올바르게 정리해 두는 것입니다.

## 우선순위: 사용자 지원


위에서 우리가 특히 집중할 측면 중 하나는 시간을 내어 문제를 보고해 주는 사용자들과 계속 연락을 유지하는 것입니다. 감사합니다! 피드백 루프를 짧게 만들수록 신규 사용자가 겪는 문제를 더 빨리 해결할 수 있고, 그들이 커뮤니티에 계속 참여할 가능성도 높아집니다.

## 도움을 주시면 정말 감사하겠습니다!

모두 매우 야심차게 보이는데, 실제로도 그렇습니다! 하지만 위에 나열된 항목들 중 상당수는 서로 겹치므로, 신중하게 계획하면 상당한 진전을 이룰 수 있습니다.

위의 목표들에 기여하는 데 관심이 있다면, 저희와 채팅하러 오세요! OFTC와 Freenode(#i2p-dev), 그리고 Twitter(@GetI2P)에서 저희를 찾을 수 있습니다.
