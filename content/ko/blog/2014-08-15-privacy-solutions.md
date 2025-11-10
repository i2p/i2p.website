---
title: "프라이버시 솔루션의 탄생"
date: 2014-08-15
author: "Meeh"
description: "조직 출범"
categories: ["press"]
---

안녕하세요, 여러분!

오늘 우리는 I2P 소프트웨어를 개발하고 유지 관리하는 새로운 조직인 Privacy Solutions 프로젝트를 발표합니다. Privacy Solutions에는 I2P 프로토콜과 기술을 기반으로 사용자의 프라이버시, 보안 및 익명성을 강화하기 위해 설계된 여러 새로운 개발 활동이 포함됩니다.

이러한 노력에는 다음이 포함됩니다:

1. The Abscond browser bundle.
2. The i2pd C++ router project.
3. The "BigBrother" I2P network monitoring project.
4. The Anoncoin crypto-coin project.
5. The Monero crypto-coin project.

Privacy Solutions의 초기 자금은 Anoncoin 및 Monero 프로젝트의 후원자들에 의해 제공되었습니다. Privacy Solutions은 노르웨이를 기반으로 한 비영리 형태의 단체로, 노르웨이 정부 등록부에 등록되어 있습니다. (미국의 501(c)3와 유사합니다.)

Privacy Solutions은 네트워크 연구를 위해 노르웨이 정부의 자금 지원을 신청할 계획입니다. 이는 BigBrother(그게 무엇인지는 나중에 다시 설명하겠습니다)와 주요 전송 계층으로 저지연 네트워크 사용을 계획하고 있는 코인들 때문입니다. 우리의 연구는 익명성, 보안, 프라이버시를 위한 소프트웨어 기술의 발전을 뒷받침할 것입니다.

먼저 Abscond Browser Bundle에 대해 간단히 소개하겠습니다. 이 프로젝트는 처음에 Meeh가 혼자 시작했지만, 이후 친구들이 패치를 보내기 시작하면서 현재는 Tor의 브라우저 번들이 제공하는 것과 같은 수준의 손쉬운 I2P 접근성을 제공하는 것을 목표로 하고 있습니다. 첫 번째 릴리스가 멀지 않았고, Apple 툴체인 설정을 포함한 몇 가지 gitian 스크립트 작업만 남아 있습니다. 다만 안정판으로 선언하기 전에 I2P를 점검할 수 있도록 Java 인스턴스에서 PROCESS_INFORMATION (프로세스에 관한 중요한 정보를 보관하는 C 구조체)을 사용한 모니터링을 추가할 예정입니다. 또한 준비가 되는 대로 Java 버전을 I2pd로 교체할 예정이므로, 번들에 JRE를 포함할 필요도 더 이상 없습니다. Abscond Browser Bundle에 대해 더 자세히 알아보려면 https://hideme.today/dev에서 확인하실 수 있습니다.

또한 i2pd의 현재 상태를 알려 드리고자 합니다. i2pd는 이제 양방향 스트리밍을 지원하여 HTTP뿐만 아니라 장시간 유지되는 통신 채널도 사용할 수 있습니다. 즉시 사용 가능한 IRC 지원이 추가되었습니다. i2pd 사용자도 Java I2P와 동일한 방식으로 I2P IRC 네트워크에 접속할 수 있습니다. I2PTunnel은 I2P 네트워크의 핵심 기능 중 하나로, I2P가 아닌 애플리케이션이 투명하게 통신할 수 있도록 합니다. 따라서 이는 i2pd에 필수적인 기능이며 주요 이정표 중 하나입니다.

마지막으로, I2P에 익숙하시다면 아마 Meeh가 1년 이상 전에 만든 메트릭 시스템인 Bigbrother.i2p를 알고 계실 겁니다. 최근 우리는 Meeh가 초기 출시 이후 보고해 온 노드들로부터 중복되지 않은 100Gb의 데이터를 보유하고 있다는 사실을 알게 되었습니다. 이것 역시 Privacy Solutions로 이전되고, NSPOF 백엔드(단일 장애 지점 없음)로 다시 작성될 것입니다. 이와 함께 Graphite (http://graphite.wikidot.com/screen-shots)도 사용하기 시작할 것입니다. 이는 최종 사용자에게 프라이버시 문제를 일으키지 않으면서 네트워크에 대한 훌륭한 개요를 제공해 줍니다. 클라이언트는 국가, router 해시, 그리고 tunnel 구축 성공률만 남기고 나머지 모든 데이터를 필터링합니다. 이 서비스의 이름은 늘 그렇듯 Meeh의 작은 농담입니다.

여기에는 소식을 조금 간추려 담았습니다. 더 자세한 정보가 필요하시다면 https://blog.privacysolutions.no/ 에서 확인해 주세요. 아직 구축 중이며, 더 많은 콘텐츠가 곧 추가될 예정입니다!

자세한 내용은 다음으로 문의하십시오: press@privacysolutions.no

감사합니다.

미칼 "Meeh" 빌라
