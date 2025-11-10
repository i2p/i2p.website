---
title: "2004-08-03자 I2P 상태 노트"
date: 2004-08-03
author: "jr"
description: "0.3.4 릴리스 성능, 새로운 웹 콘솔 개발, 그리고 다양한 애플리케이션 프로젝트를 다루는 주간 I2P 상태 업데이트"
categories: ["status"]
---

안녕 여러분, 이 현황 업데이트부터 먼저 끝내자

## 색인:

1. 0.3.4 status
2. On deck for 0.3.4.1
3. New web console / I2PTunnel controller
4. 0.4 stuff
5. Other development activities
6. ???

## 1) 0.3.4 상태

지난주 0.3.4 릴리스 이후, 새 네트워크는 꽤 잘 동작하고 있다 - irc 연결은 한 번에 몇 시간씩 유지되고 eepsite(I2P Site) 가져오기도 꽤 신뢰할 만해 보인다. 처리량은 여전히 전반적으로 낮지만 약간 개선되었다(예전에는 꾸준히 4-5KBps가 관측되었고, 지금은 꾸준히 5-8KBps가 관측된다). oOo는 irc 활동을 요약하는 스크립트 두 개를 게시했으며, 여기에는 왕복 메시지 시간과 연결 지속 시간이 포함된다(최근 CVS에 커밋된 hypercubus의 bogobot을 기반으로 함)

## 2) 0.3.4.1 예정

0.3.4를 사용하는 모든 분들이 눈치채셨겠지만, 제 로그가 *cough* 다소 장황했습니다만 이는 cvs에서 수정되었습니다. 또한 ministreaming 라이브러리를 스트레스 테스트하는 도구를 몇 가지 작성한 뒤, 메모리를 마구 잡아먹지 않도록 'choke'(흐름 제한)를 추가했습니다(스트림의 버퍼에 128KB를 초과하는 데이터를 추가하려 할 때 블록되어, 대용량 파일을 전송하더라도 router가 그 전체 파일을 메모리에 올려두지 않도록 합니다). 이것이 많은 분들이 겪어 온 OutOfMemory 문제를 완화하는 데 도움이 될 것이라 생각하지만, 이를 확인하기 위해 추가적인 모니터링 / 디버깅 코드를 더 넣을 예정입니다.

## 3) 새로운 웹 콘솔 / I2PTunnel 컨트롤러

0.3.4.1을 위한 위의 변경 사항들에 더해, 새로운 router console(I2P router의 웹 관리 콘솔)의 초기 버전을 일부 테스트할 수 있도록 준비했습니다. 몇 가지 이유로 아직은 기본 설치에 포함하지 않을 예정이므로, 며칠 후 0.3.4.1 리비전이 나오면 실행 방법에 대한 안내를 제공하겠습니다. 보시다시피 저는 웹 디자인에는 정말 소질이 없고, 많은 분들이 말씀하신 대로 애플리케이션 계층에서 시간을 허비하는 일을 그만두고 코어와 router를 확고히 안정화해야 합니다. 그래서 새 콘솔에는 우리가 원하던 유용한 기능이 상당수 들어가 있지만(몇 개의 간단한 웹 페이지만으로 router를 완전히 구성하고, router의 상태를 빠르고 읽기 쉬운 요약으로 제공하며, 서로 다른 I2PTunnel 인스턴스를 생성/편집/중지/시작할 수 있는 기능), 웹 쪽에 능숙한 분들의 도움이 정말로 필요합니다.

새 웹 콘솔에 사용된 기술은 표준 JSP, CSS, 그리고 router / I2PTunnels에서 데이터를 조회하고 요청을 처리하는 단순한 JavaBeans입니다. 이들은 모두 두 개의 .war files로 묶여 통합된 Jetty 웹서버에 배포되며(이는 router의 clientApp.* lines를 통해 시작되어야 합니다). 주요 router 콘솔 JSP 및 JavaBeans는 기술적으로 꽤 견고하지만, I2PTunnel 인스턴스를 관리하기 위해 내가 만든 새로운 JSP 및 JavaBeans는 다소 임시방편적입니다.

## 4) 0.4 관련 사항

새로운 웹 인터페이스 외에도 0.4 릴리스에는 hypercubus의 새로운 설치 프로그램이 포함될 예정이나, 아직 제대로 통합되지는 않았습니다. 또한 대규모 시뮬레이션(특히 IRC 및 outproxies(아웃프록시)와 같은 비대칭 애플리케이션 처리)을 더 수행할 필요가 있습니다. 아울러 오픈 소스 JVM에서 새로운 웹 인프라스트럭처를 구동할 수 있도록 kaffe/classpath에 몇 가지 업데이트가 반영되도록 추진해야 합니다. 여기에 더해 확장성에 관한 문서 하나와, 몇 가지 일반적인 시나리오에서 보안/익명성을 분석하는 문서 하나 등 문서를 더 정리해야 합니다. 마지막으로, 여러분이 제안한 모든 개선 사항을 새로운 웹 콘솔에 통합하고자 합니다.

아, 그리고 당신이 발견한 모든 버그도 고쳐 주세요 :)

## 5) 기타 개발 활동

기본 I2P 시스템에서 많은 진전이 이루어지고 있지만, 그건 이야기의 절반에 불과합니다 - 여러분 중 많은 분들이 I2P를 유용하게 만들기 위한 애플리케이션과 라이브러리 작업을 훌륭하게 진행하고 있습니다. 누가 무엇을 작업하고 있는지에 대해 대화 기록에서 몇 가지 질문을 본 적이 있어서, 그 정보를 널리 알리는 데 도움이 되도록 여기 제가 알고 있는 모든 것을 정리해 둡니다 (여기에 없는 작업을 하고 계시고 공유하고 싶으시거나, 제가 틀렸거나, 진행 상황을 논의하고 싶으시다면, 언제든 말씀해 주세요!)

### Active development:

- python SAM/I2P lib (devs: sunshine, aum)
- C SAM lib (devs: nightblade)
- python kademlia/I2P DHT (devs: aum)
- v2v - Voice over I2P (devs: aum)
- outproxy load balancing (devs: mule)

### Development I've heard about but don't know the status of:

- swarming file transfer / BT (devs: nickster)

### Paused development:

- Enclave DHT (devs: nightblade)
- perl SAM lib (devs: BrianR)
- I2PSnark / BT (devs: eco)
- i2pIM (devs: thecrypto)
- httptunnel (devs: mihi)
- MyI2P address book (devs: jrandom)
- MyI2P blogging (devs: jrandom)

## 6) ???

지금은 떠오르는 건 여기까지예요—오늘 밤 늦게 회의에 한번 들러서 이런저런 얘기 나눠요. 늘 그렇듯, GMT 기준 오후 9시에 평소 사용하는 서버의 #i2p 채널에서.

=jr
