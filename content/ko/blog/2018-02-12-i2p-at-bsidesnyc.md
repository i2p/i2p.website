---
title: "BSidesNYC에서의 I2P"
date: 2018-02-12
author: "sadie, str4d"
description: "BSidesNYC에서 열린 I2P 밋업 참가 보고서"
categories: ["Meetup"]
---

Sadie와 str4d는 1월 20일 토요일에 BSidesNYC에 참석했습니다. 이렇게 훌륭한 컨퍼런스를 주최해 주신 BSides 팀께 감사드립니다!

몇몇 발표를 제외하면, 우리는 오후에 John Jay College의 공용 공간에서 그날 세운 몇 가지 목표를 달성하기 위한 작업을 주로 진행했다.

가장 시급한 과제는 34C3에서의 논의를 바탕으로 2018년을 위한 상위 수준 로드맵을 작성하는 것이었습니다. 이는 [이제 게시되었습니다](/blog/2018/02/11/high-level-roadmap-for-2018/) - 확인해 보세요! 또한 연휴 기간 동안 미뤄두었던, 막 시작된 Vulnerability Response Process(취약점 대응 프로세스)를 둘러싼 몇 가지 소통 관련 논의를 다시 이어받아, 이를 "production use"(운영 환경에서의 실제 사용)로 전환하는 작업도 진행했습니다.

가장 크고 가장 고된 작업은 새로운 I2P 웹사이트의 정보 아키텍처를 설계하는 것이었습니다. 우리는 [Ura Design](https://ura.design) 팀이 우리를 위해 디자인해 준 새로운 로고와 프런트 페이지를 갖추었지만, 더 사용자 친화적인 온보딩 경험을 만들기 위해 콘텐츠 내비게이션을 어떻게 구성할지 결정하지 못해 진행이 막혀 있었습니다. 이에 대한 초기 초안을 마쳤고, 남은 디자인 작업을 시작하기 전에 이를 최종 확정하기 위해 현재 Ura와 함께 작업하고 있습니다.

마지막으로, 올해의 참여와 대외 홍보 방안에 대해 논의했습니다. 기존 스티커를 하위 등급 보상으로 두고, 더 큰 기부에는 다른 보상을 제공하는 등 구체적인 기부 등급을 마련하는 것이 좋다는 데 의견을 모았습니다. 가능한 보상 아이디어는 다음과 같습니다:

- More sticker variants (e.g. tesselating sticker)
- T-shirts printed with our new logo
- Other kinds of merch (hoodies, scarves)
- Extension idea: Raspberry Pis in custom 3D-printed cases, pre-loaded with I2P!
  This would require ironing out things like:

  - Having sufficient randomness at boot for generating key material.
  - Ensuring the hardware can handle sufficient network traffic to be a useful network participant (older Pis had restricted network interface speeds).
  - Actually making them!

이번 밋업은 34C3에서 논의했던 아이디어, 즉 연중 내내 보다 비공식적인 I2P 중심의 밋업을 열자는 취지의 시범 운영이었습니다. 그리고 잘 되었습니다! 앞으로의 밋업을 조직하는 데 도움을 주고 싶으시다면 우리에게 연락해 주세요. 올해 I2P 개발자들과 커뮤니티 구성원들은 FOSDEM, HOPE, Citizen Lab, BSidesTO 등 여러 행사에 참석할 예정이며, 아마 다른 행사에도 참여할 것입니다 - 그래서 새 스티커가 많이 필요합니다!
