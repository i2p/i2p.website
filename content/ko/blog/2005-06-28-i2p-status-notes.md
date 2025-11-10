---
title: "2005-06-28자 I2P 상태 노트"
date: 2005-06-28
author: "jr"
description: "SSU 전송 배포 계획, 단위 테스트 바운티 완료 및 라이선스 관련 고려사항, 그리고 Kaffe Java 상태를 다루는 주간 업데이트"
categories: ["status"]
---

안녕하세요, 여러분. 또 주간 업데이트 시간이에요.

* Index

1) SSU status 2) Unit test status 3) Kaffe status 4) ???

* 1) SSU status

There has been some more progress on the SSU transport, and my current thinking will be that after some more live net testing, we'll be able to deploy as 0.6 without much delay. The first SSU release will not include support for people who cannot poke a hole in their firewall or adjust their NAT, but that will be rolled out in 0.6.1. After 0.6.1 is out, tested, and kicking ass (aka 0.6.1.42), we'll move on over to 1.0.

제 개인적인 생각으로는 SSU 트랜스포트가 도입됨에 따라 사람들이 둘 다 활성화할 필요가 없도록(TCP와 UDP 포트를 모두 포워딩하지 않아도 되도록) 그리고 개발자들이 불필요한 코드를 유지보수하지 않아도 되도록 TCP 트랜스포트 지원을 완전히 중단하는 쪽입니다. 이에 대해 강한 의견이 있으신가요?

* 2) Unit test status

지난주에 언급했듯이, Comwiz가 유닛 테스트 현상금의 1단계를 수령하겠다고 나섰습니다(만세, Comwiz! 현상금에 자금을 보태 준 duck & zab에게도 감사!). 코드는 CVS에 커밋되었고, 로컬 설정에 따라 i2p/core/java 디렉터리로 이동해 "ant test junit.report"를 실행하면(약 한 시간 정도 기다리세요...) junit 및 clover 리포트를 생성하고 i2p/reports/core/html/junit/index.html에서 볼 수 있습니다. 또 다른 방법으로 "ant useclover test junit.report clover.report"를 실행한 뒤 i2p/reports/core/html/clover/index.html을 볼 수도 있습니다.

두 테스트 세트 모두의 단점은 지배층이 "저작권법"이라고 부르는 그 어리석은 개념과 관련이 있습니다. Clover는 상용 제품이지만, cenqua 쪽에서는 오픈 소스 개발자들이 무료로 사용할 수 있도록 허용하고 있습니다(그리고 우리에게 라이선스를 부여하는 데도 친절히 동의했습니다). Clover 보고서를 생성하려면 로컬에 Clover가 설치되어 있어야 합니다 — 저는 clover.jar를 ~/.ant/lib/에 두었고, 라이선스 파일과 나란히 있습니다. 대부분의 사람들에게는 Clover가 필요하지 않으며, 우리가 보고서를 웹에 게시할 것이므로 설치하지 않더라도 기능적인 손실은 없습니다.

한편으로, 유닛 테스트 프레임워크 자체를 고려하면 저작권법의 다른 측면에 발목이 잡힙니다 — junit은 IBM Common Public License 1.0 하에 배포되는데, FSF [1]에 따르면 이는 GPL과 호환되지 않습니다. 또한, 우리 자체에는 GPL 코드가 없지만(적어도 코어나 router에는 없습니다), 우리의 라이선스 정책 [2]을 돌아보면, 라이선스를 정하는 방식의 구체적인 목표는 우리가 만드는 것을 가능한 한 많은 사람들이 사용할 수 있도록 하는 데 있으며, 이는 익명성은 이용자가 많을수록 강화되기 때문입니다.

[1] http://www.fsf.org/licensing/licenses/index_html#GPLIncompatibleLicenses [2] http://www.i2p.net/licenses

어찌 된 일인지 일부 사람들은 소프트웨어를 GPL로 배포하므로, 그들이 제약 없이 I2P를 사용할 수 있도록 노력하는 것이 이치에 맞습니다. 최소한, 이는 우리가 외부에 공개하는 실제 기능이 CPL로 라이선스된 코드(예: junit.framework.*)에 의존하도록 허용할 수 없다는 의미입니다. 이상적으로는 이를 단위 테스트에도 확대하고 싶지만, junit은 테스트 프레임워크의 사실상의 공용어처럼 보이며, 우리의 자원을 감안하면 "이봐, 우리만의 퍼블릭 도메인 단위 테스트 프레임워크를 만들자!"라고 말하는 것은 전혀 타당한 생각이라고 보지 않습니다.

이 모든 점을 고려하면, 제 생각은 이렇습니다. CVS에 junit.jar를 포함해 두고 사람들이 단위 테스트를 실행할 때 그것을 사용하겠습니다. 하지만 단위 테스트 자체는 i2p.jar나 router.jar에 빌드되지 않으며, 릴리스에 포함되어 배포되지 않습니다. 필요하다면 추가 jar 세트(i2p-test.jar 및 router-test.jar)를 공개할 수도 있겠지만, 그것들은 junit에 의존하므로 GPL 적용 애플리케이션에서는 사용할 수 없습니다.

=jr
