---
title: "2004-08-31에 대한 I2P 상태 노트"
date: 2004-08-31
author: "jr"
description: "네트워크 성능 저하, 0.3.5 릴리스 계획, 문서화 필요 사항, 그리고 Stasher DHT(분산 해시 테이블) 진행 상황을 다루는 주간 I2P 상태 업데이트"
categories: ["status"]
---

자, 소년소녀 여러분, 또 화요일이네요!

## 색인:

1. 0.3.4.3
2. 0.3.5 and 0.4
3. docs
4. stasher update
5. ???

## 1) 0.3.4.3

음, 여러분도 이미 눈치채셨겠지만, 네트워크의 사용자 수는 꽤 안정적으로 유지되고 있는 반면 지난 며칠 동안 성능이 크게 저하되었습니다. 그 원인은 지난주에 소규모 DoS(서비스 거부) 공격이 있었을 때 드러난 피어 선택과 메시지 전달 코드의 일련의 버그였습니다. 그 결과 사실상 모든 사용자의 tunnels(터널)이 지속적으로 실패하는 상황이었고, 이는 약간 눈덩이 효과를 일으켰습니다. 그러니 여러분만 그런 게 아닙니다 — 우리 모두에게도 네트워크 상태가 끔찍했습니다 ;)

하지만 좋은 소식은 우리가 문제를 꽤 신속하게 고쳤고, 수정 사항은 지난주부터 CVS에 반영되어 있다는 것입니다. 다만 다음 릴리스가 나올 때까지는 사용자들에게 네트워크가 여전히 엉망일 겁니다. 그런 의미에서…

## 2) 0.3.5 및 0.4

다음 릴리스에는 0.4 릴리스를 위해 계획해 둔 모든 신기능과 개선 사항(새 설치 관리자, 새 웹 인터페이스 표준, 새 I2PTunnel 인터페이스, 시스템 트레이 및 Windows 서비스, 스레딩 개선, 버그 수정 등)이 포함되겠지만, 지난 릴리스가 시간이 지나면서 악화된 양상은 시사하는 바가 컸습니다. 이러한 릴리스를 더 천천히 진행하여, 더 충분히 배포되고 문제점들이 스스로 드러날 시간을 주고자 합니다. 시뮬레이터로 기본적인 부분은 살펴볼 수 있지만, 실제 네트워크에서 우리가 보는 자연스러운 네트워크 문제를 시뮬레이션할 방법은 없습니다(적어도 아직은).

따라서 다음 릴리스는 0.3.5가 될 것입니다 - 바라건대 0.3.* 계열의 마지막 릴리스가 되겠지만, 다른 문제가 발생한다면 그렇지 않을 수도 있습니다. 제가 6월에 오프라인이었을 때 네트워크가 어떻게 동작했는지 되돌아보면, 약 2주가 지나면서 상태가 악화되기 시작했습니다. 따라서 최소한 2주 동안 높은 수준의 신뢰성을 유지할 수 있을 때까지, 우리 버전을 다음 0.4 릴리스 단계로 상향 조정하는 것은 보류하려 합니다. 물론 그동안 작업을 안 하겠다는 뜻은 아닙니다.

어쨌든, 지난주에 말씀드린 대로 hypercubus가 새로운 설치 시스템을 꾸준히 작업하고 있고, 제가 이것저것 바꿔대고 별난 시스템들까지 지원해 달라고 요구하는 것도 처리해 주고 있습니다. 다음 며칠 안에 모든 걸 정리해서 0.3.5 릴리스를 배포할 수 있을 것입니다.

## 3) 문서

0.4 이전의 그 2주간 "testing window"에는 우리가 해야 할 중요한 일 중 하나는 문서화를 집중적으로 진행하는 것입니다. 제가 궁금한 것은 우리 문서에서 어떤 점이 빠져 있다고 느끼시는지 - 우리가 답해야 할 질문이 무엇인지입니다. 비록 제가 "좋습니다, 이제 가서 그 문서들을 작성하세요"라고 말하고 싶지만, 현실적으로는 그 문서들이 무엇을 다룰지 짚어 주실 수 있는지만 부탁드립니다.

예를 들어, 제가 지금 작업 중인 문서 중 하나는 위협 모델의 개정판이며, 저는 이를 이제 I2P가 각기 다른 개인의 요구를 어떻게 충족할 수 있는지를 설명하는 일련의 사용 사례로 설명합니다. 여기에는 기능, 해당 개인이 우려하는 공격자, 그리고 그 개인이 자신을 어떻게 방어하는지가 포함됩니다.

질문을 다루기 위해 별도의 정식 문서가 필요하지 않다고 생각하신다면, 그저 질문 형식으로 간단히 작성해 주시면 FAQ에 추가할 수 있습니다.

## 4) stasher update

Aum이 오늘 일찍 채널에 들러 업데이트 소식을 전했다(내가 그에게 질문 세례를 퍼붓는 동안):

```
<aum> quick stasher update, with apologies for tomorrow's meeting:
<aum> infinite-level splitfiles working, have successfully
      inserted and retrieved large files
<jrandom> w00t
<aum> splitfile fragmentation/reassembly transparently occuring
      within stasher
<aum> freenet interface working
<jrandom> wow
<jrandom> so FUQID/FIW works?
<aum> use of fcp splitfile commands in freenet clients strictly
      forbidden (at this stage)
<aum> most clients such as fuqid/fiw should allow setting
      extremely large splitfile sizes, which should prevent them
      trying to talk splitfiles
<aum> if not, then i can dummy up something
<jrandom> r0x0r aum, that kicks ass!
<aum> hooks are in for detailed freenet key support
<jrandom> detailed freenet key support?
<aum> yes, specific chk@, ssk@, ksk@
<jrandom> ok great, so they're all verified @ each node, etc?
<aum> no - only verifiable by the requestor
<aum> my thinking is, given KSK@fred = 'mary',
<aum> to store as SHA1(SHA1("KSK@fred")) = E(mary), where key
      for E is SHA1("KSK@fred")
<aum> ie, crypto key is SHA1(uri), and kademlia key is
      SHA1(SHA1(uri))
<jrandom> hm
<aum> so a possessor of the URI can decyrpt, but owner of a
      datastore cannot decrypt (and therefore has plausible
      deniability)
<jrandom> well, ksks are inherently insecure, so thats no big
      loss, but what about ssk?
<deer> <detonate> those keys aren't very large
<aum> SSK as for freenet
<jrandom> so the SSKs are verified at each node?
<aum> except i'm looking to use same encryption over the top
<aum> not feasible to verify SSK at the target node
<jrandom> why not?  freenet does
<aum> well maybe it is feasible,
<aum> i guess i shouldn't be so lazy
<aum> i was trying to keep the kademlia and freenet layers
      separate
<jrandom> heh, you're not being lazy, there's a truckload of
      work here, and you're doing a great job
<aum> verifying on target node will cause some pathological
      couplings between the two layers, and force deviation
      from pure kademlia
<jrandom> i dont think its possible to do SSKs or CHKs
      securely without having the node validate the key
      properties
<aum> not correct
<aum> fred asks mary, 'gimme SSK@madonna'
<aum> mary sends back what she thinks is 'SSK@madonna'
<aum> fred tests it, barfs, then goes on to ask the next node
<aum> anyway, i MUST go - but am open to continuing discussion
      over email, or tomorrow
<aum> bbl guys
<jrandom> mallory floods the net with 'SSK@madonna' ==
      'sexDrugsRockNRoll'
<jrandom> l8r aum
```
그래서 보시다시피, 진전이 엄청나게 많습니다. 설령 키가 DHT(분산 해시 테이블) 계층 위에서 검증된다 하더라도, 그건 엄청 멋져요(제 생각엔). aum, 화이팅!

## 5) ???

좋아, 내가 할 말은 여기까지야(곧 회의가 시작하니 잘됐네)... 잠깐 들러서 하고 싶은 말 해!

=jr
