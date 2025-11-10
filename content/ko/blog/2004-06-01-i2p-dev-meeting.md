---
title: "I2P 개발자 회의 - 2004년 6월 1일"
date: 2004-06-01
author: "duck"
description: "2004년 6월 1일자 I2P 개발 회의록."
categories: ["meeting"]
---

## 간단한 요약

<p class="attendees-inline"><strong>참석자:</strong> deer, duck, hypercubus, Masterboy, mihi, Nightblade, tessier, wilde</p>

## 회의 로그

<div class="irc-log"> [22:59] &lt;duck&gt; Tue Jun  1 21:00:00 UTC 2004 [23:00] &lt;duck&gt; 안녕하세요, 여러분! [23:00] &lt;mihi&gt; 안녕, duck [23:00] &lt;duck&gt; http://dev.i2p.net/pipermail/i2p/2004-June/000250.html [23:00] &lt;duck&gt; 내 제안: [23:00] * Masterboy가 #i2p에 입장했습니다

[23:00] &lt;duck&gt; 1) 코드 진행 상황
[23:00] &lt;duck&gt; 2) 주요 콘텐츠
[23:00] &lt;duck&gt; 3) 테스트넷 상태
[23:00] &lt;duck&gt; 4) 현상금
[23:00] &lt;duck&gt; 5) ???
[23:00] &lt;Masterboy&gt; 안녕:)
[23:00] &lt;duck&gt; .
[23:01] &lt;duck&gt; jrandom이 없으니 우리가 직접 해야겠다
[23:01] &lt;duck&gt; (그가 로그를 남기면서 우리의 독립성을 검증하고 있다는 건 알고 있어요)
[23:01] &lt;Masterboy&gt; 문제없어:P
[23:02] &lt;duck&gt; 안건에 문제가 없다면 그대로 진행하죠
[23:02] &lt;duck&gt; 그래도 여러분이 따르지 않으면 내가 할 수 있는 건 별로 없지만 :)
[23:02] &lt;duck&gt; .
[23:02] &lt;mihi&gt; ;)
[23:02] &lt;duck&gt; 1) 코드 진행 상황
[23:02] &lt;duck&gt; cvs에 제출된 코드가 별로 없네요
[23:02] &lt;duck&gt; 이번 주엔 제가 트로피를 받았어요: http://duck.i2p/duck_trophy.jpg
[23:03] * hypercubus 아직 cvs 계정이 없음
[23:03] &lt;Masterboy&gt; 그리고 누가 뭔가 제출했나요?
[23:03] &lt;duck&gt; 비밀리에 코딩하는 사람 있나요?
[23:03] * Nightblade가 #I2P에 입장했습니다

[23:03] &lt;hypercubus&gt; BrianR가 몇 가지 작업을 하고 있었어 [23:04] &lt;hypercubus&gt; 0.4 설치 프로그램은 대략 20% 정도 손봤어 [23:04] &lt;duck&gt; hypercubus: 뭔가 있으면 diffs(변경 내역)를 제공해, 그러면 $dev가 대신 커밋해 줄 거야 [23:04] &lt;duck&gt; 물론 엄격한 라이선스 계약이 적용돼 [23:05] &lt;duck&gt; hypercubus: 멋지네, 문제나 언급할 만한 거 있어? [23:06] &lt;hypercubus&gt; 아직은 없어, 하지만 아마 BSD 쓰는 사람 두어 명이 preinstaller 셸 스크립트를 테스트해 줘야 할 것 같아 [23:06] * duck 여기저기 뒤져본다 [23:06] &lt;Nightblade&gt; 텍스트 전용이야 [23:07] &lt;mihi&gt; duck: duck_trophy.jpg에서 너는 어느 쪽이야? [23:07] &lt;mihi&gt; ;) [23:07] &lt;Nightblade&gt; luckypunk은 freebsd가 있고, 내 isp도 freebsd 쓰는데 설정이 좀 꼬였어 [23:07] &lt;Nightblade&gt; 내 웹 호스팅 isp 말이야, comcast 말고 [23:08] &lt;duck&gt; mihi: 안경 쓴 왼쪽 사람이 나야. 트로피 건네주는 오른쪽 사람이 wilde야 [23:08] * wilde 손을 흔든다 [23:08] &lt;hypercubus&gt; 선택지가 있어... java가 설치돼 있으면 preinstaller를 통째로 건너뛸 수 있고...    java가 설치돼 있지 않으면 linux 바이너리나 win32 바이너리 preinstaller(콘솔 모드), 또는    일반적인 *nix 스크립트 preinstaller(콘솔 모드)를 실행할 수 있어 [23:08] &lt;hypercubus&gt; 메인 설치 프로그램은 콘솔 모드나 근사한 GUI 모드를 선택할 수 있게 해 [23:08] &lt;Masterboy&gt; 곧 freebsd를 설치할 거라 나중에 그 설치 프로그램도 한번 써 볼게 [23:09] &lt;hypercubus&gt; 좋아... jrandom 말고도 쓰는 사람이 있는지 몰랐거든 [23:09] &lt;Nightblade&gt; freebsd에서 java는 "java"가 아니라 "javavm"으로 호출해 [23:09] &lt;hypercubus&gt; Sun 소스에서 빌드된 거야? [23:09] &lt;mihi&gt; freebsd는 symlinks(심볼릭 링크)를 지원해요 ;) [23:10] &lt;hypercubus&gt; 어쨌든 바이너리 preinstaller는 100% 완성됐어 [23:10] &lt;hypercubus&gt; gcj로 네이티브로 컴파일돼 [23:11] &lt;hypercubus&gt; 설치 디렉터리(install dir)만 물어보고, JRE도 알아서 가져와 [23:11] &lt;duck&gt; w00t [23:11] &lt;Nightblade&gt; 멋지네 [23:11] &lt;hypercubus&gt; jrandom이 i2p용 커스텀 JRE를 패키징하고 있어

[23:12] <deer> <j> .
[23:12] <Nightblade> FreeBSD ports collection에서 Java를 설치하면 javavm이라는 래퍼 스크립트를 사용하게 돼요
[23:12] <deer> <r> .
[23:12] <hypercubus> 어쨌든 이 녀석은 거의 완전히 자동화될 거예요
[23:12] <deer> <r> .
[23:12] <deer> <r> .
[23:12] <deer> <r> .
[23:12] <deer> <duck> r: 그만해
[23:12] <deer> <r> .
[23:12] <deer> <m> .
[23:13] <deer> <m> 멍청한 IRC 서버, pipelining을 지원하지 않네 :(
[23:13] <duck> hypercubus: 우리한테 ETA(예상 완료 시간) 있어?
[23:14] <deer> <m> 이런, 문제는 "Nick change too fast"야 :(
[23:14] <hypercubus> 여전히 한 달 안에는 끝낼 수 있을 거라고 기대해요, 0.4가 릴리스 준비를 갖추기 전에
[23:14] <hypercubus> 지금은 개발 시스템용 새 OS를 컴파일 중이라, 인스톨러 작업으로 돌아가기까지 며칠 걸릴 거예요 ;-)
[23:14] <hypercubus> 그래도 걱정 마세요
[23:15] <duck> 좋아. 그럼 다음 주에 더 소식 전할게 :)
[23:15] <duck> 다른 코딩은 한 거 있어?
[23:15] <hypercubus> 아마요... 전력 회사가 또 나를 곤란하게 만들지 않는다면
[23:16] * duck #2로 이동
[23:16] <duck> * 2) 특집 콘텐츠
[23:16] <duck> 이번 주엔 스트리밍 오디오(ogg/vorbis) 작업을 많이 했어요
[23:16] <duck> baffled는 자기 egoplay 스트림을 돌리고 있고, 나도 스트림을 하나 돌리고 있어요
[23:16] <Masterboy> 그리고 꽤 잘 작동해요
[23:17] <duck> 우리 사이트에서 사용하는 방법에 대한 정보를 볼 수 있어요
[23:17] <hypercubus> 대략적인 통계 좀 있어요?
[23:17] <duck> 거기에 없는 플레이어를 쓰고 사용법을 알아내면, 나에게 보내 주세요. 추가할게요
[23:17] <Masterboy> duck, 네 사이트에서 baffled의 스트림 링크는 어디에 있어?
[23:17] <Masterboy> :P
[23:17] <duck> hypercubus: 4kB/s면 꽤 잘 돼요
[23:18] <duck> 그리고 ogg면 그렇게 나쁘진 않아요
[23:18] <hypercubus> 하지만 그게 여전히 평균 속도인 것 같죠?
[23:18] <duck> 내가 보기엔 그게 최대치예요
[23:18] <duck> 하지만 전부 설정을 미세하게 조정하는 문제죠
[23:19] <hypercubus> 왜 그게 최대치처럼 보이는지 짐작 가는 게 있어요?
[23:19] <hypercubus> 여기서 말하는 건 스트리밍만이 아니고
[23:19] <hypercubus> 다운로드도 포함해요
[23:20] <Nightblade> 어제 duck의 호스팅 서비스에서 큰 파일 몇 개(몇 메가바이트)를 받았는데, 속도가 4kb~5kb 정도 나오더라고요
[23:20] <duck> 원인은 rtt(왕복 지연 시간)인 것 같아요
[23:20] <Nightblade> 그 Chips 동영상들
[23:20] <hypercubus> 4~5는 내가 i2p를 쓰기 시작한 이후로 꾸준히 받았던 약 3보다 개선된 것처럼 보이네요

[23:20] &lt;Masterboy&gt; 4-5kb면 나쁘지 않네..
[23:20] &lt;duck&gt; windowsize가 1이면 그렇게 빨라지지 않아..
[23:20] &lt;duck&gt; windowsize&gt;1 현상금: http://www.i2p.net/node/view/224
[23:21] &lt;duck&gt; mihi: 코멘트 좀 해줄래?
[23:21] &lt;hypercubus&gt; 그런데 놀랄 만큼 꾸준히 3 kbps야
[23:21] &lt;mihi&gt; 무엇에 대해? ministreaming에서 windowsize&gt;1이라면: 그걸 해내면 당신은 마법사지 ;)
[23:21] &lt;hypercubus&gt; 대역폭 미터에 끊김이 없어... 꽤 매끈한 선이야
[23:21] &lt;duck&gt; mihi: 왜 4kb/s에서 그렇게 안정적인지
[23:21] &lt;mihi&gt; 모르겠어. 아무 소리도 안 들려 :(
[23:22] &lt;duck&gt; mihi: 모든 i2ptunnel 전송에서
[23:22] &lt;Masterboy&gt; mihi 너는 ogg 스트리밍 플러그인을 설정해야 해..
[23:22] &lt;mihi&gt; Masterboy:?
[23:23] &lt;mihi&gt; 아니, 속도에 관한 제한은 i2ptunnel 내부엔 없어. 그건 router에 있을 거야...
[23:23] &lt;duck&gt; 내 생각: 최대 패킷 크기: 32kB, 5초 rtt: 32kB/5s =~ 6.5kb/s
[23:24] &lt;hypercubus&gt; 그럴듯하게 들리네
[23:25] &lt;duck&gt; 오케이..
[23:25] &lt;duck&gt; 다른 내용:
[23:25] * hirvox 님이 #i2p에 입장했습니다

[23:25] <duck> Naughtious의 새로운 eepsite가 있어
[23:25] <duck> anonynanny.i2p
[23:25] <duck> 키는 CVS에 커밋됐고, 그가 ugha의 위키에도 올려놨어
[23:25] * mihi는 "sitting in the ..."가 들리는 중 - duck++
[23:25] <Nightblade> 두세 개 스트림을 4kb 속도로 열 수 있는지 확인해봐. 그러면 문제가 router에 있는지, 아니면 스트리밍 라이브러리에 있는지 알 수 있을 거야
[23:26] <duck> Naughtious: 거기 있어? 계획 좀 이야기해줘 :)
[23:26] <Masterboy> 그가 호스팅을 제공한다고 읽었어
[23:26] <duck> Nightblade: baffled에서 병렬로 3개 다운로드 해봤는데 각각 3-4kB 나오더라
[23:26] <Nightblade> ㅇㅋ
[23:27] <mihi> Nightblade: 그걸 어떻게 구분해?
[23:27] * mihi는 "stop&go" 모드로 듣는 걸 좋아함 ;)
[23:27] <Nightblade> 음, router에 한 번에 4kb만 처리하도록 하는 어떤 제한이 있다면
[23:27] <Nightblade> 아니면 다른 문제인지
[23:28] <hypercubus> 이 anonynanny 사이트가 뭔지 누가 설명해줄 수 있어? 지금은 i2p router가 돌고 있지 않아
[23:28] <mihi> hypercubus: 그냥 위키 같은 거야
[23:28] <duck> Plone CMS로 구성, 계정 자유 생성
[23:28] <duck> 파일 업로드랑 웹사이트 관련 작업 가능
[23:28] <duck> 웹 인터페이스 통해서
[23:28] <Nightblade> 또 할 수 있는 건 "repliable datagram"(응답 가능한 데이터그램)의 처리량을 테스트하는 거야. 내가 알기론 스트림과 같지만 ACK 없이 동작해
[23:28] <duck> 아마 Drupal이랑 비슷할 듯
[23:28] <hypercubus> 응, Plone 돌려본 적 있어
[23:29] <duck> Nightblade: 그걸 관리하는 데 airhook를 쓰는 걸 생각해왔어
[23:29] <duck> 근데 아직은 기초적인 생각만 했지
[23:29] <hypercubus> 위키 콘텐츠는 아무거나 올려도 돼? 아니면 특정 주제를 중심으로 해?
[23:29] <Nightblade> airhook는 GPL인 것 같아
[23:29] <duck> 프로토콜 말이야
[23:29] <duck> 코드가 아니라
[23:29] <Nightblade> 아하 :)
[23:30] <duck> hypercubus: 그는 양질의 콘텐츠를 원하고, 그걸 네가 제공하길 바래 :)
[23:30] <Masterboy> hyper, 네 자신을 찍은 최고의 포르노나 올려봐 ;P
[23:30] <duck> 오케이
[23:30] * Masterboy도 그렇게 해보려고 함
[23:30] <hypercubus> 맞아, 열린 위키 운영하면 양질의 콘텐츠만 올라오지 않겠어 ;-)
[23:31] <duck> 오케이
[23:31] * duck이 #3으로 이동함
[23:31] <duck> * 3) 테스트넷 상태
[23:31] <Nightblade> Airhook는 간헐적이거나 신뢰할 수 없거나 지연되는 네트워크를 우아하게 처리합니다  <-- ㅋㅋ I2P에 대해 그다지 낙관적인 설명은 아니네!
[23:31] <duck> 어떻게 돌아가고 있어?
[23:32] <duck> datagram over i2p 얘기는 맨 끝으로 미루자
[23:32] <tessier> 공개 위키들 돌아다니면서 이걸 링크 다는 거 좋아함: http://www.fissure.org/humour/pics/squirre   l.jpg
[23:32] <tessier> airhook 끝내줘
[23:32] <tessier> 나도 P2P 네트워크를 만들 때 쓰려고 살펴보고 있었어.
[23:32] <Nightblade> 내겐 안정적인 것 같아 (#3)
[23:32] <Nightblade> 지금까지 본 것 중 최고야
[23:33] <duck> 응
[23:33] <mihi> 잘 동작해 - 최소한 stop&go 오디오 스트리밍에는
[23:33] <duck> IRC에서 업타임이 꽤 인상적이더라
[23:33] <hypercubus> 동의... 내 router 콘솔에 파란 애들이 훨씬 많아졌어
[23:33] <Nightblade> mihi: 테크노 듣고 있어? :)
[23:33] <duck> 근데 자정(00:00)을 넘어가는 연결을 bogobot가 처리하지 못하는 것 같아서 판단하긴 어려워
[23:33] <tessier> 내겐 오디오 스트리밍은 아주 잘 되는데, 웹사이트 로딩은 종종 여러 번 시도해야 해
[23:33] <Masterboy> 내 생각엔 i2p는 6시간 정도 사용 후에 아주 잘 돌아가는 것 같아. 6번째 시간에는 IRC를 7시간 썼고, 그래서 내 router는 13시간 동안 돌아갔어
[23:33] <duck> (*힌트*)
[23:34] <hypercubus> duck: 어... 헤헷
[23:34] <hypercubus> 그건 고칠 수 있을 것 같아
[23:34] <hypercubus> 로깅을 일별로 설정해뒀어?
[23:34] <duck> hypercubus++
[23:34] <hypercubus> 로그 로테이션 말이야
[23:34] <duck> 아 맞아
[23:34] <duck> duck--
[23:34] <hypercubus> 그게 이유야
[23:34] <Nightblade> 하루 종일 일하다가 집에 와서 컴퓨터 켜고 i2p 시작했는데 몇 분 만에 duck의 IRC 서버에 접속했어
[23:35] <duck> 이상한 DNF들이 몇 번 보였어
[23:35] <duck> 내 eepsite들에 접속할 때도
[23:35] <duck> (http://dev.i2p.net/bugzilla/show_bug.cgi?id=74)
[23:35] <duck> 그게 지금 문제의 대부분 원인인 것 같아
[23:35] <hypercubus> bogoparser는 단일 로그파일 안에서 전부 발생한 업타임만 분석해... 그러니 로그파일이 24시간만 포함하면, 24시간 넘게 연결된 사람은 아무도 표시되지 않아
[23:35] <duck> Masterboy랑 ughabugha도 그랬던 것 같아...
[23:36] <Masterboy> 응
[23:36] <duck> (그거 고치면 다음 주 트로피는 네 거야!)
[23:37] <deer> <mihi> bogobot이 신났나? ;)
[23:37] <Masterboy> 내 웹사이트를 시험해봤는데, 가끔 새로고침하면 다른 경로를 타는지 로드될 때까지 기다려야 해. 근데 난 절대 안 기다려 ;P 한 번 더 누르면 바로 떠
[23:37] <deer> <mihi> 앗, 미안. 여기가 게이트로 연동된 곳인 걸 잊었네...
[23:38] <duck> Masterboy: 타임아웃이 61초 걸려?
[23:39] <duck> mihi: bogobot를 주간 로테이션으로 설정했어
[23:39] * mihi가 IRC에서 나감 ("bye, and have a nice meeting")
[23:40] <Masterboy> 미안, 내 웹사이트에선 확인 안 해봤어. 바로 안 열리면 그냥 새로고침 눌러서 바로 뜨게 해버리거든..
[23:40] <duck> 흠
[23:40] <duck> 어쨌든, 고쳐야 해
[23:41] <duck> .... #4
[23:41] <Masterboy> 경로가 매번 같게 주어지지 않는 것 같아
[23:41] <duck> * 4) 현상금(bounties)
[23:41] <duck> Masterboy: 로컬 연결은 더 짧게(단축) 처리되어야 해
[23:42] <duck> wilde가 현상금에 대해 생각 좀 했던데... 거기 있어?
[23:42] <Masterboy> 아마 피어 선택 버그일지도
[23:42] <wilde> 사실 그게 의제에 맞는 건지는 잘 모르겠어
[23:42] <duck> 오
[23:42] <wilde> 좋아, 그래도 생각은 이런 거였어:
[23:42] <Masterboy> 우리가 공개로 전환하면 현상금 시스템이 더 잘 돌아갈 것 같아
[23:43] <Nightblade> masterboy: 맞아, 연결마다 tunnel이 두 개 있어. 적어도 내가 router.config를 읽은 바로는 그렇게 이해했어
[23:43] <wilde> 이번 달에 i2p를 약간 홍보해서 현상금 풀을 조금 늘릴 수 있을 거야
[23:43] <Masterboy> Mute 프로젝트가 잘 나가더라 - 아직 많이 코딩하지도 않았는데 600달러를 받았어 ;P
[23:44] <wilde> 자유 커뮤니티, 암호(crypto) 쪽 사람들 등을 겨냥하자
[23:44] <Nightblade> jrandom은 광고를 원치 않는다고 생각해
[23:44] <wilde> 대중적인 Slashdot 관심 같은 건 아니지, 맞아
[23:44] <hypercubus> 나도 그렇게 봤어
[23:44] <Masterboy> 난 다시 밀어붙이고 싶어 - 우리가 공개하면 시스템이 훨씬 더 잘 돌아갈 거야 ;P
[23:45] <wilde> Masterboy: 예를 들어 현상금이 myi2p 개발을 가속할 수도 있어
[23:45] <Masterboy> 그리고 jr이 말했듯 1.0 전까지는 공개하지 말고, 0.4 이후엔 약간의 관심만
[23:45] <Masterboy> *썼다
[23:45] <wilde> 현상금이 500달러 이상 수준이면 사람들이 몇 주는 실제로 버틸 수 있을 거야
[23:46] <hypercubus> 어려운 점은, 규모가 작은 개발 커뮤니티(에헴, Mute 개발자들처럼)를 겨냥하더라도, 그 사람들이 우리가 바라는 것보다 더 널리 i2p 소식을 퍼뜨릴 수 있다는 거야
[23:46] <Nightblade> 누군가는 i2p 버그를 고치는 걸로 커리어를 만들 수도 있지
[23:46] <hypercubus> 그리고 너무 이르게
[23:46] <wilde> i2p 링크는 이미 많은 공개된 곳에 있어
[23:46] <Masterboy> 구글에서 검색하면 i2p를 찾을 수 있어

[23:47] <hypercubus> 잘 안 알려진 공개된 곳 ;-) (freesite에서 I2P 링크를 봤어... 그 망할 freesite가 로드되기라도 해서 다행이야!)
[23:47] <wilde> http://en.wikipedia.org/wiki/I2p
[23:47] <Masterboy> 하지만 0.4가 끝날 때까지는 홍보하지 않는 데 동의해
[23:47] <Masterboy> 뭐???????
[23:47] <wilde> http://www.ovmj.org/GNUnet/links.php3?xlang=English
[23:48] <Masterboy> protol0l은 훌륭한 일을 하고 있어;P
[23:48] <Masterboy> ;))))))
[23:48] <hypercubus> 오타 멋지네 ;-)
[23:48] <wilde> 어쨌든, 아직은 I2P를 비공개로 유지해야 한다는 데 동의해 (jr 이 로그 읽어 ;)
[23:49] <Masterboy> 누가 그랬어?
[23:49] <Masterboy> Freenet 크루의 논의가 더 많은 관심을 끈 것 같아..
[23:50] <Masterboy> 그리고 jr이 toad와 논의하면서 대중에게 많은 정보를 줬지..
[23:50] <Masterboy> 그러니 ughas 위키에 있듯이 - 우리 모두 그건 jr 탓으로 돌릴 수 있어;P
[23:50] <wilde> 어쨌든, /.을 끌어들이지 않고도 돈을 좀 들여올 수 있는지 보자.
[23:50] <Masterboy> 동의
[23:50] <hypercubus> freenet 개발자 메일링리스트를 내가 말하는 "대중"이라고 하긴 어렵지 ;-)
[23:50] <wilde> .
[23:51] <hypercubus> wilde: 생각보다 더 빨리 많은 돈을 얻게 될 거야 ;-)
[23:51] <wilde> 아 진짜, 우리 엄마도 freenet-devl을 구독해
[23:51] <duck> 우리 엄마는 gmame으로 읽어
[23:51] <deer> <clayboy> 여기서는 학교에서 freenet-devl을 가르쳐
[23:52] <wilde> .
[23:52] <Masterboy> 그러면 0.4가 안정화되면 현상금이 더 많이 나오겠지..
[23:53] <Masterboy> 그건 두 달 뒤라는 거지;P
[23:53] <wilde> 그 duck은 어디 갔지?
[23:53] <duck> 고마워 wilde
[23:53] <hypercubus> 지금까지 유일한 현상금 청구자로서 말하자면, 그 현상금은 내가 그 도전을 맡기로 한 결정에 아무 영향도 없었어
[23:54] <wilde> 헤헤, 100배였으면 달랐겠지
[23:54] <duck> 너는 세상에 너무 좋은 사람이야
[23:54] <Nightblade> 하하
[23:54] * duck #5로 이동
[23:54] <hypercubus> wilde, 100달러는 나한테 아무 의미도 없어 ;-)
[23:54] <duck> 100 * 10 = 1000
[23:55] * duck pops("5 airhook")
[23:55] <duck> tessier: 실제로 써본 경험 있어
[23:55] <duck> (http://www.airhook.org/)
[23:55] * Masterboy 이거 한번 써볼게:P
[23:56] <duck> 자바 구현(작동이나 하는지 모르겠음) http://cvs.ofb.net/airhook-j/
[23:56] <duck> 파이썬 구현(엉망, 예전에는 작동함) http://cvs.sourceforge.net/viewcvs.py/khashmir   /khashmir/airhook.py
[23:58] * duck 불평 밸브를 연다
[23:58] <Nightblade> j 것도 GPL
[23:58] <duck> 퍼블릭 도메인으로 포팅해
[23:58] <hypercubus> 아멘
[23:58] <Nightblade> 프로토콜 문서 전체가 고작 3쪽이라서 - 그렇게 어렵진 않을 거야
[23:59] <Masterboy> 어려운 건 없어
[23:59] <Masterboy> 그냥 쉬울 뿐은 아니지
[23:59] <duck> 완전히 명세가 갖춰져 있진 않은 것 같아
[23:59] * hypercubus masterboy의 포춘쿠키를 빼앗는다
[23:59] <duck> 레퍼런스 구현으로 C 코드에 파고들어야 할 수도 있어
[00:00] <Nightblade> 내가 직접 했을 텐데 지금은 다른 i2p 관련 작업으로 바빠
[00:00] <Nightblade> (그리고 본업도 있고)
[00:00] <hypercubus> duck: 그거 현상금 걸까?
[00:00] <Nightblade> 이미 있어
[00:00] <Masterboy> ?
[00:00] <Masterboy> 아아 Pseudonyms
[00:00] <duck> 두 가지 레벨에서 사용할 수 있어
[00:00] <duck> 1) TCP 외의 전송 계층으로
[00:01] <duck> 2) i2cp/sam 내부에서 데이터그램을 처리하는 프로토콜로
[00:01] <hypercubus> 그럼 진지하게 고려해볼 만하네
[00:01] <hypercubus> </obvious>

[00:02] &lt;Nightblade&gt; duck: 나는 SAM의 repliable datagram(회신 가능한 데이터그램)의 최대 크기가 31kb이고, 반면에    스트림의 최대 크기는 32kb라는 걸 알아챘어 - 그래서    repliable datagram 모드에서는 매 패킷마다 발신자의 destination(I2P 주소)가 전송되고,    스트림 모드에서는 시작할 때만 전송되는 거라고 생각하게 돼 - [00:02] &lt;Masterboy&gt; 음 airhook cvs는 별로 최신이 아니야..
[00:03] &lt;Nightblade&gt; 그래서 sam을 통해 repliable    datagram들 위에 프로토콜을 올리는 건 비효율적일 거라는 생각이 들어
[00:03] &lt;duck&gt; airhook의 메시지 크기는 256 바이트이고, i2cp의 것은 32kb라서, 적어도 조금은 바꿔야 해
[00:04] &lt;Nightblade&gt; 사실 프로토콜을 SAM에서 하고 싶다면 그냥 anonymous datagram(익명 데이터그램)을    쓰고 첫 번째 패킷에 발신자의 destination을 넣으면 돼.... 블라 블라 블라 - 아이디어는 많지만    코딩할 시간이 부족해
[00:06] &lt;duck&gt; 그런데 또 서명을 검증하는 데 문제가 있어
[00:06] &lt;duck&gt; 그래서 누군가 너에게 가짜 패키지를 보낼 수도 있어
[00:06] &lt;Masterboy&gt; 주제:::: SAM
[00:06] &lt;Masterboy&gt; ;P
[00:07] &lt;Nightblade&gt; 맞아
[00:08] &lt;Nightblade&gt; 하지만 그 destination으로 되돌려 보냈는데 확인응답이 없다면, 속임수라는 걸 알 수 있을 거야
[00:08] &lt;Nightblade&gt; 핸드셰이크가 있어야 해
[00:08] &lt;duck&gt; 하지만 그러려면 애플리케이션 레벨의 핸드셰이크가 필요해
[00:08] &lt;Nightblade&gt; 아니, 꼭 그렇진 않아
[00:09] &lt;Nightblade&gt; SAM에 접근하는 라이브러리에 넣기만 하면 돼
[00:09] &lt;Nightblade&gt; 그래도 그건 안 좋은 방식이야
[00:09] &lt;Nightblade&gt; 그렇게 하긴 하지만
[00:09] &lt;duck&gt; 분리된 tunnel들을 사용할 수도 있어
[00:09] &lt;Nightblade&gt; 그건 스트리밍 라이브러리에 있어야 해
[00:11] &lt;duck&gt; 응. 말 되네
[00:12] &lt;duck&gt; 오케이
[00:12] &lt;duck&gt; 난 지금 *baff*한 기분이야
[00:13] &lt;Nightblade&gt; 응
[00:13] * duck *baffs* </div>
