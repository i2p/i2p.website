---
title: "I2P 상태 노트(2006-01-03자)"
date: 2006-01-03
author: "jr"
description: "0.6.1.8 릴리스 안정성, 부하 테스트 결과와 처리량 최적화를 위한 peer profiling(피어 프로파일링), 그리고 2005년 종합 리뷰와 2006년 로드맵 미리보기를 다루는 새해 업데이트"
categories: ["status"]
---

여러분, 안녕하세요! 새해 복 많이 받으세요! 지난주에는 한 주 쉬었으니 주간 상태 노트를 다시 시작해 봅시다 -

* Index

1) 네트워크 상태 및 0.6.1.8 2) 부하 테스트 결과 및 피어 프로파일링 3) 2005년 회고 / 2006년 전망 / ???

* 1) Net status and 0.6.1.8

얼마 전 우리는 0.6.1.8을 릴리스했고, 현장 보고에 따르면 zzz의 수정들이 상당히 도움이 되었으며, 최근 네트워크 트래픽이 크게 증가했음에도 불구하고 네트워크에서 꽤 안정적인 것으로 보입니다( stats.i2p 에 따르면 지난 한 달 동안 평균이 두 배가 된 것으로 보입니다). I2PSnark도 꽤 잘 작동하는 것 같습니다 - 몇 가지 문제에 부딪히긴 했지만, 이후 빌드에서 대부분을 찾아내어 수정했습니다. Syndie의 새로운 블로그 인터페이스에 대해서는 피드백이 많지 않았지만, Syndie 트래픽은 약간 증가했습니다(부분적으로는 protocol이 dust의 rss/atom importer를 발견한 덕분 :)

* 2) Load testing results and peer profiling

지난 몇 주 동안 저는 처리량 병목을 정확히 특정하려고 노력해 왔습니다. 서로 다른 소프트웨어 구성 요소들은 I2P 상의 종단 간 통신에서 우리가 보통 보는 것보다 훨씬 높은 속도로 데이터를 전송할 수 있어서, 저는 그것들을 스트레스 테스트하기 위해 커스텀 코드로 라이브 네트워크에서 벤치마킹해 왔습니다. 첫 번째 테스트 세트에서는 네트워크의 모든 router를 대상으로 1-hop inbound tunnel을 구축하고 그 tunnel을 통해 가능한 한 빨리 데이터를 전송했는데, 결과가 꽤 유망했습니다. router의 처리 속도는 기대 가능한 능력치와 대략 비슷한 수준이었고(예: 대부분은 전체 기간 평균 4-16KBps만 처리했지만, 일부는 단일 tunnel을 통해 20-120KBps까지 처리), 이 테스트는 추가 탐색을 위한 좋은 기준선이 되었으며 tunnel 처리 자체가 우리가 보통 보는 것보다 훨씬 더 많은 데이터를 처리할 수 있음을 보여주었습니다.

그 결과를 실제 tunnel을 통해 재현하려는 시도는 그만큼 성공적이지 않았다. 혹은, 현재 우리가 보는 것과 유사한 처리량을 보여 주었으니 오히려 더 성공적이었다고도 할 수 있는데, 이는 우리가 뭔가를 제대로 짚고 있었다는 뜻이었다. 1hop 테스트 결과로 돌아가서, 내가 수동으로 빠르다고 판단한 피어를 선택하도록 코드를 수정하고, 이 "편법" 피어 선택으로 실제 tunnel을 통해 부하 테스트를 다시 실행했으며, 120KBps 수준까지 올라가지는 않았지만 유의미한 개선은 나타났다.

Unfortunately, asking people to manually select their peers has serious problems for both anonymity and, well, usability, but armed with the load test data, there seems to be a way out. For the last few days I've been testing out a new method of profiling peers for their speed - essentially monitoring their peak sustained throughput, rather than their recent latency. Naive implementations have been quite successful, and while it hasn't picked exactly the peers I would have manually, its done a pretty good job. There are still some kinks to work out with it though, such as making sure we are able to promote exploratory tunnels to the fast tier, but I'm trying out some experiments on that front currently.

전반적으로, 가장 작은 병목을 넓혀 가고 있으니 이번 처리량 개선 작업도 끝에 가까워졌다고 생각합니다. 곧 다음 병목을 만나겠지만, 이걸로 일반 인터넷 수준의 속도가 나오지는 않더라도 분명 도움이 될 것입니다.

* 3) 2005 review / 2006 preview / ???

2005년이 매우 큰 진전의 해였다고만 말하는 것은 다소 과소평가일 것입니다 - 우리는 지난해에만 25회의 릴리스를 통해 다양한 방식으로 I2P를 개선했고, 네트워크를 5배 성장시켰으며, 새로운 클라이언트 애플리케이션(Syndie, I2Phex, I2PSnark, I2PRufus)을 여러 개 배포했습니다. 또한 postman과 cervantes가 만든 새로운 irc2p IRC 네트워크로 마이그레이션했고, zzz의 stats.i2p, orion의 orion.i2p, tino의 프록시 및 모니터링 서비스 등 유용한 eepsites(I2P Sites)도 다수 등장했습니다. 커뮤니티 역시 한층 더 성숙해졌는데, 이는 포럼과 채널에서 Complication과 다른 이들이 기울인 지원 노력의 공이 적지 않습니다. 모든 부문에서 올라온 버그 리포트의 품질과 다양성도 크게 향상되었습니다. 커뮤니티 구성원들의 지속적인 재정적 지원도 인상적이었고, 아직 완전히 지속 가능한 개발에 필요한 수준에는 못 미치지만, 제가 겨울을 나는 동안 생계를 유지할 수 있게 해주는 완충 자금은 마련되어 있습니다.

지난 한 해 동안 기술적으로, 사회적으로, 또는 재정적으로 참여해 주신 모든 분들께 도움 주셔서 감사합니다!

2006년은 우리에게 중요한 해가 될 것입니다. 이번 겨울에 0.6.2를 내고, 봄이나 여름쯤 1.0 릴리스를 예정해 두었으며, 2.0은 가을(어쩌면 그보다 더 일찍) 공개할 계획입니다. 올해는 우리가 무엇을 해낼 수 있는지 확인하는 해가 될 것이고, 애플리케이션 계층에서의 작업은 이전보다 더욱 중요해질 것입니다. 그러니 아이디어가 있다면 지금 바로 시작해 주세요 :)

어쨌든 몇 분 후에 우리 주간 진행 상황 회의가 시작되니, 더 논의하고 싶은 게 있으면 평소 장소 [1]의 #i2p에 들러 인사해 주세요!

=jr [1] http://forum.i2p.net/viewtopic.php?t=952
