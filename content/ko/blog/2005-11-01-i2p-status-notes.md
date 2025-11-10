---
title: "2005-11-01자 I2P 상태 노트"
date: 2005-11-01
author: "jr"
description: "0.6.1.4 릴리스의 성공, 부트스트랩 공격 분석, I2Phex 0.1.1.34 보안 수정, voi2p 음성 앱 개발, 그리고 Syndie RSS 피드 통합을 다루는 주간 업데이트"
categories: ["status"]
---

다들 안녕하세요, 또 한 주 그 시간이 돌아왔네요

* Index

1) 0.6.1.4 및 네트워크 상태 2) boostraps, 선행 노드, 글로벌 수동 공격자, 및 CBR 3) i2phex 0.1.1.34 4) voi2p 앱 5) syndie 및 sucker 6) ???

* 1) 0.6.1.4 and net status

지난 토요일의 0.6.1.4 릴리스는 꽤 순조롭게 진행된 것 같습니다 - 네트워크의 75%가 이미 업그레이드했으며(감사합니다!), 나머지 대부분도 어차피 0.6.1.3을 사용하고 있습니다. 전반적으로 무난하게 잘 작동하는 것 같고, 이에 대해 긍정적이든 부정적이든 피드백을 많이 듣지는 못했지만, 만약 문제가 있었다면 다들 크게 불평했을 거라고 생각합니다 :)

특히 제가 수행한 테스트는 그런 종류의 연결을 기본적으로만 시뮬레이션한 것에 불과하므로, 다이얼업 모뎀 연결을 사용하는 분들로부터 어떤 피드백이든 듣고 싶습니다.

* 2) boostraps, predecessors, global passive adversaries, and CBR

몇 가지 아이디어와 관련해 메일링 리스트에서 더 많은 논의가 있었고, 부트스트랩 공격에 대한 요약이 온라인에 올라와 있습니다 [1]. 옵션 3의 암호화 사양을 구체화하는 데 약간의 진전을 이루었고, 아직 게시된 것은 없지만 상당히 간단합니다.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/001146.html

고정 비트레이트(CBR) tunnel을 사용하여 강력한 적대자에 대한 저항성을 개선하는 방법에 관해 추가 논의가 있었으며, 그러한 방향을 탐색할 선택지는 있지만, 이는 적절한 사용에 상당한 자원이 필요하고 그러한 오버헤드와 함께 I2P를 사용하려는 사람이 누구인지와 어떤 집단이 아예 사용할 수 있는지 없는지에도 측정 가능한 영향을 미칠 가능성이 높기 때문에 현재 I2P 3.0에 예정되어 있습니다.

* 3) I2Phex 0.1.1.34

지난 토요일, 새로운 I2Phex 릴리스 [2]가 나왔습니다. 이 릴리스는 결국 I2Phex가 실패하게 만들 수 있는 파일 디스크립터 누수를 수정했고(Complication에게 감사!), 사용자의 I2Phex 인스턴스에 특정 파일을 다운로드하라고 원격에서 지시할 수 있게 하던 일부 코드도 제거했습니다(GregorK에게 감사!). 업그레이드를 강력히 권장합니다.

아직 릴리스되지 않은 CVS 버전에도 몇 가지 동기화 문제를 해결하는 업데이트가 있었습니다 - Phex는 일부 네트워크 작업이 즉시 처리된다고 가정하지만, I2P는 때때로 작업을 처리하는 데 시간이 걸릴 수 있습니다 :) 이는 GUI(그래픽 사용자 인터페이스)가 잠시 멈추거나, 다운로드 또는 업로드가 멈추거나, 연결이 거부되는 형태(그리고 어쩌면 몇 가지 다른 방식)로 나타납니다. 아직 충분히 테스트되지는 않았지만, 아마 이번 주에 0.1.1.35에 포함되어 배포될 것입니다. 추가 소식이 생기면 포럼에 더 많은 공지가 올라올 것이라고 확신합니다.

[2] http://forum.i2p.net/viewtopic.php?t=1143

* 4) voi2p app

Aum은 I2P를 통한 새로운 음성(및 텍스트) 앱을 열심히 개발 중이고, 저는 아직 보지는 못했지만 꽤 멋질 것 같네요. 어쩌면 회의에서 Aum이 우리에게 업데이트를 해줄 수도 있고, 아니면 첫 알파 릴리스를 차분히 기다릴 수도 있겠죠 :)

* 5) syndie and sucker

dust가 syndie와 sucker 작업을 꾸준히 진행해 왔고, 최신 CVS 빌드의 I2P는 이제 RSS와 atom 피드에서 콘텐츠를 자동으로 가져와 당신의 syndie 블로그에 게시할 수 있게 해줍니다. 현재로서는 wrapper.config (wrapper.java.classpath.20 및 21)에 lib/rome-0.7.jar와 lib/jdom.jar를 명시적으로 추가해야 하지만, 나중에는 그럴 필요가 없도록 묶어서 제공할 예정입니다. 아직 진행 중인 작업이며, rome 0.8(아직 출시되지 않음)은 피드에서 enclosures(첨부 파일)를 가져오는 기능처럼 정말 멋진 것들을 제공할 것 같습니다. 그러면 sucker가 그것들을 syndie 게시물의 첨부 파일로 가져올 수 있게 됩니다(지금도 이미 이미지와 링크도 처리합니다!).

Like all rss feeds, there seem to be some discrepencies with how the content is included, so some feeds go in smoother than others. I think if people were to help test it out with different feeds and let dust know of any issues that it b0rks on, that might be useful. In any case, this stuff looks pretty exciting, nice work dust!

* 6) ???

우선은 이 정도입니다만, 질문이 있거나 더 논의하고 싶은 분이 계시면 GMT 기준 오후 8시에 열리는 미팅에 들러 주세요 (서머타임 잊지 마세요!).

=jr
