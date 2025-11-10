---
title: "2006-03-21자 I2P 상태 노트"
date: 2006-03-21
author: "jr"
description: "네트워크 통계를 위한 JRobin 통합, biff 및 toopie IRC 봇, 그리고 새 GPG 키 공지"
categories: ["status"]
---

안녕 여러분, 또 화요일이네

* Index

1) 네트워크 상태 2) jrobin 3) biff and toopie 4) 새 키 5) ???

* 1) Net status

지난 주는 꽤 안정적이었고, 아직 새로운 릴리스는 나오지 않았습니다.  저는 tunnel 속도 제한과 저대역폭 환경에서의 동작에 꾸준히 작업해 왔지만, 그 테스트를 돕기 위해 웹 콘솔과 통계 관리 시스템에 JRobin을 통합했습니다.

* 2) JRobin

JRobin [1]은 RRDtool [2]을 순수 Java로 포팅한 것으로, zzz가 그동안 만들어 온 것과 같은 보기 좋은 그래프를 매우 적은 메모리 오버헤드로 생성할 수 있게 해준다. 우리는 이를 완전히 메모리 내(in-memory)에서 동작하도록 구성해 두었기 때문에 파일 잠금 경합이 없고, 데이터베이스를 업데이트하는 데 걸리는 시간은 체감되지 않을 정도다. 우리가 아직 활용하지 못하고 있는 JRobin의 멋진 기능이 정말 많지만, 다음 릴리스에는 기본 기능이 포함되고 RRDtool이 이해할 수 있는 형식으로 데이터를 내보내는 방법도 제공될 것이다.

[1] http://www.jrobin.org/ [2] http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/

* 3) biff and toopie

Postman has been hacking away on some useful bots, and I'm glad to report that the lovable biff is back [3], letting you know whenever you've got (anonymous) mail while sitting on irc2p.  In addition, postman has built up a whole new bot for us - toopie - to serve as an info bot for I2P/irc2p.  We're still feeding toopie FAQs, but he'll be coming into the usual channels shortly.  Thanks postman!

[3] http://hq.postman.i2p/?page_id=15

* 4) new key

유심히 보신 분들은 제 GPG 키가 며칠 내에 만료된다는 것을 알아차리셨을 겁니다. 제 새 키 @ http://dev.i2p.net/~jrandom 의 지문(fingerprint)은 0209 9706 442E C4A9 91FA  B765 CE08 BC25 33DC 8D49이며, 키 ID는 33DC8D49입니다. 이 글은 제 예전 키로 서명되었지만, 앞으로 1년 동안의 이후 글(및 릴리스)은 새 키로 서명될 것입니다.

* 5) ???

일단 지금은 여기까지예요 - 몇 분 뒤에 #i2p에 들러서 주간 미팅에서 인사해 주세요!

=jr
