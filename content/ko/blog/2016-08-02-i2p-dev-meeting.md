---
title: "I2P 개발자 회의 - 2016년 8월 2일"
date: 2016-08-02
author: "zzz"
description: "2016년 8월 2일자 I2P 개발 회의록."
categories: ["meeting"]
---

## 간단한 요약

<p class="attendees-inline"><strong>Present:</strong> nextloop, psi, poneyhot, sadie, str4d, trolly, xmpre, zzz</p>

## 회의 기록

<div class="irc-log">21:00:01 &lt;zzz&gt; 0) 안녕
21:00:01 &lt;zzz&gt; 1) HOPE 보고 (zzz/sadie) http://zzz.i2p/topics/2152
21:00:01 &lt;zzz&gt; 2) 0.9.27 업데이트 (zzz) http://zzz.i2p/topics/2132
21:00:01 &lt;zzz&gt; 3) Summer of X 업데이트 (sadie/str4d)
21:00:05 &lt;zzz&gt; 0) 안녕
21:00:07 &lt;zzz&gt; 안녕
21:00:38 &lt;xmpre&gt; 안녕하세요
21:00:44 &lt;i2pr&gt; [Slack/str4d] 안녕하세요
21:00:56 &lt;zzz&gt; 1) HOPE 보고 (zzz/sadie) http://zzz.i2p/topics/2152
21:01:32 &lt;zzz&gt; 그 링크에 간단한 방문 보고를 올렸습니다. sadie, comraden1, gravy, 아니면 영상을 좀 보신 분들, 추가할 내용 있나요?
21:02:30 &lt;i2pr&gt; [Slack/str4d] 아직 영상은 보지 못했습니다. Tor 관련 영상 말고도 표시해 두면 좋을 것들이 있나요?
21:03:01 &lt;zzz&gt; 저는 그 외에는 많이 보지 못했습니다. 사람들이 zzz.i2p 쓰레드에 추천을 추가해 주길 바랍니다
21:03:13 &lt;xmpre&gt; 혹시 모르는 분들을 위해, 영상은 어디에 있나요?
21:03:27 &lt;zzz&gt; 아마 hope.net일 겁니다
21:03:56 &lt;zzz&gt; 1) 관련해 다른 것 있나요?
21:03:59 &lt;xmpre&gt; https://hope.net/watch.html
21:04:54 &lt;zzz&gt; 2) 0.9.27 업데이트 (zzz) http://zzz.i2p/topics/2132
21:05:57 &lt;zzz&gt; 빨라도 9월 중순을 보고 있습니다. mtn 활동이나 큰 기능은 많지 않아요. i2p 여름 활동을 마친 뒤에는 NTCP2로 넘어가고 싶습니다. 그래서 지금은 .27을 서두를 필요는 없고, 꽤 안정적입니다
21:06:26 &lt;zzz&gt; .27 일정이나 내용에 대해 의견 있나요?
21:06:39 &lt;i2pr&gt; [Slack/str4d] 저도 비슷한 시기에 NTCP2에 주의를 돌릴 예정입니다
21:06:49 &lt;xmpre&gt; 멀티호밍을 더 쉽게 만드는 제안이 있는데, 그걸 trac에 올릴까요?
21:06:59 &lt;xmpre&gt; 요는 내보내기/가져오기 기능입니다
21:07:11 &lt;zzz&gt; 좋아요. 여전히 새로운 Tails 담당자도 필요하니, 우리 모두 그에 대해 트윗해야 합니다
21:07:19 &lt;i2pr&gt; [Slack/str4d] SAM을 기본으로 활성화하는 것도 고려하고 싶습니다.
21:07:43 &lt;zzz&gt; xmpre, 명확하다면 trac도 괜찮고, 논의가 필요하면 zzz.i2p가 더 나을 수 있어요
21:07:48 &lt;i2pr&gt; [Slack/str4d] 최소한 그렇게 했을 때의 파급효과는 논의해 봅시다
21:08:06 &lt;xmpre&gt; 알겠습니다, zzz 
21:08:27 &lt;zzz&gt; sam-by-default는 다음 달 안건에 올립시다. 여름 앱 활동 이후이면서 .27 이전으로요
21:08:40 &lt;i2pr&gt; [Slack/str4d] ACK
21:08:53 &lt;i2pr&gt; [Slack/str4d] 그동안은 각자 생각해 보면 좋겠습니다
21:09:21 &lt;i2pr&gt; [Slack/str4d] 예를 들어 Tor의 컨트롤 포트 정책과 비교해 보는 것도 좋겠죠
21:09:38 &lt;zzz&gt; http://zzz.i2p/topics/2149 에 추가했습니다
21:10:03 &lt;zzz&gt; 기본으로 켜진다면 인증(auth)이나 SSL도 함께 켜는 게 좋을까요? 잘 모르겠습니다. 생각해 보겠습니다
21:10:11 &lt;zzz&gt; 2) 관련해 다른 것 있나요?
21:10:58 &lt;psi&gt; (안녕)
21:11:10 &lt;zzz&gt; 다음 회의 얘기가 나온 김에, CCC 예산이 안건에 올라갈 예정이니 위 링크를 보시고, 그 회의까지 요구 사항을 준비해 주세요
21:11:13 &lt;i2pr&gt; [Slack/sadie] 안녕 - 지금 일이 너무 많아요 여러분
21:11:33 &lt;zzz&gt; 그럼 3)로...
21:11:43 &lt;zzz&gt; 3) Summer of X 업데이트 (sadie/str4d)
21:11:50 &lt;zzz&gt; sadie, str4d, 최신 소식은요?
21:12:10 &lt;i2pr&gt; [Slack/str4d] 괜찮아요 Sadie, 잠깐이라도 들러줘서 기쁩니다 :)
21:12:22 &lt;i2pr&gt; [Slack/str4d] Summer Dev는 정말 잘 진행되고 있다고 생각합니다
21:12:47 &lt;i2pr&gt; [Slack/str4d] 이번 달은 우리가 다른 애플리케이션과 함께한 작업에 공개적으로 초점을 맞췄습니다
21:13:11 &lt;i2pr&gt; [Slack/str4d] (그동안 일반적으로 함께 작업하지 않았던 앱들)
21:13:47 &lt;i2pr&gt; [Slack/str4d] Tahoe-LAFS에서 사용하는 통신 라이브러리인 Foolscap에 I2P 클라이언트 지원을 넣는 데 성공했습니다
21:14:29 &lt;i2pr&gt; [Slack/str4d] 그래서 가까운 미래에는 적어도 클라이언트 측에서 I2P의 그리드와 함께 업스트림을 사용할 수 있을 것으로 기대합니다
21:14:57 &lt;i2pr&gt; [Slack/str4d] I2P와 Tor에 대한 서버 측 지원은 이후 릴리스에 예정되어 있습니다
21:15:31 &lt;i2pr&gt; [Slack/str4d] 또한 개념 증명으로 I2P 위에서 ZeroNet이 동작하도록 거의 마무리했습니다
21:16:01 &lt;i2pr&gt; [Slack/str4d] (이 과정에서 psi와 제가 i2p.socket을 크게 개선하기도 했습니다)
21:16:22 &lt;zzz&gt; ++psi
21:17:15 &lt;zzz&gt; 제 쪽에서는 i2phex, jwebcache, orchid용 플러그인 릴리스를 했습니다. 약 일주일 후에는 syndie 릴리스가 있을 예정이고(번역을 업데이트해 주세요!) orchid 릴리스도 하나 더 있을 겁니다
21:17:34 &lt;i2pr&gt; [Slack/str4d] 우와
21:17:45 &lt;zzz&gt; 그리고 아마 jircii도요. 최소 한 명이 요청하고 있으니, 더 원하시는 분 있으면 알려주세요
21:17:45 &lt;xmpre&gt; 독립 실행형 i2psnark 작업에 감사드립니다, i2pd와 함께 동작하는 인스턴스 하나를 구동 중입니다
21:17:58 &lt;psi&gt; i2p.socket에는 여전히 개발자 피드백이 필요합니다, 아 맞다 그리고 IPFS 티켓도 확인하라고 스스로에게 상기해야겠네요
21:18:44 &lt;i2pr&gt; [Slack/str4d] 다음 달은 우리 자체 앱을 작업하는 시간으로 지정되어 있지만, 외부 개발자들과의 협업도 더 보고 싶습니다
21:18:59 &lt;zzz&gt; 또 한 가지, 이 라이브러리와 독립 실행형 앱들을 i2pd에서도 테스트해 보시길 바랍니다
21:19:02 &lt;i2pr&gt; [Slack/str4d] 예: psi가 IPFS 개발자들과 함께 작업하는 것 :)
21:19:15 &lt;i2pr&gt; [Slack/str4d] :+1:
21:19:47 &lt;nextloop&gt; 안녕하세요. 대부분의 플러그인이 GitHub에 없네요. 거기로 옮길까요?
21:19:54 &lt;i2pr&gt; [Slack/str4d] 아이디어가 없으면 저에게 핑 주세요. 할 일 목록을 드리겠습니다.
21:20:23 &lt;i2pr&gt; [Slack/str4d] 좋은 생각일 수 있겠네요
21:20:29 &lt;zzz&gt; 지금 인력이 없는 일 중 하나가 독립 실행형 패키지 빌드/서명인데, 그게 반드시 필요할지 확신은 없습니다. kytv와 ech가 일부 하긴 했지만, 많은 것들의 패키징이나 호스팅이 일관되지 않습니다
21:20:57 &lt;zzz&gt; 어떤 것들은 코드에 정돈된 빌드 타깃조차 없습니다
21:21:21 &lt;i2pr&gt; [Slack/str4d] 음
21:21:56 &lt;i2pr&gt; [Slack/str4d] 이번 달에는 I2P-Bote를 Gradle로 마이그레이션하면서 전체 빌드 프로세스를 개편할 예정입니다
21:22:10 &lt;xmpre&gt; i2psnark 독립 실행형 패키지를 빌드/서명하기 시작할 수 있습니다, 저는 bobthebuilder.i2p를 통해 Java I2P를 빌드하고 있습니다
21:22:18 &lt;zzz&gt; 저는 그중 어떤 것의 메인테이너도 하고 싶지 않습니다. 많아야 다른 사람이 나머지를 끝내면 빠르게 플러그인 빌드만 하려 합니다. 하지만 별로 진행이 없었는데, 그게 아마 i2psummer의 취지겠죠.
21:22:19 &lt;trolly&gt; gradle?
21:23:26 &lt;zzz&gt; 아 맞다, bobthebuilder를 가동시켜 준 xmpre에게 감사합니다. 어제는 조금 과하게 돌아가고 있었고... 몇 시간 전에 -8을 푸시했는데 아직 여기서는 빌드를 못 봤네요. 곧 매끄럽게 돌아가게 해 주실 거라 믿습니다
21:23:49 &lt;zzz&gt; 3) 관련해서 더 있나요?
21:24:08 &lt;i2pr&gt; [Slack/str4d] 현재 웹사이트 개편에서 우리가 보유한 앱을 barter advertise하고, 자원봉사자가 어디서 기여하면 좋을지 명확히 표시하고 싶습니다
21:24:13 &lt;xmpre&gt; 흠, zzz 확인해 볼게요 
21:24:16 &lt;i2pr&gt; [Slack/str4d] Better*
21:24:41 &lt;zzz&gt; 우선은 i2pwiki에 무엇이 있는지 확인해 보세요
21:24:55 &lt;i2pr&gt; [Slack/str4d] 그걸 Summer Dev와도 연결할 수 있겠습니다
21:25:14 &lt;poneyhot&gt; 몇 가지 제안해도 될까요... 알파벳 순으로 올리지 말아 주세요, anoncoin이 맨 앞에 올 이유는 없죠 
21:25:20 &lt;poneyhot&gt; 아니면 anonymous git hosting ..
21:25:22 &lt;zzz&gt; 회의에 더 논의할 것 있나요?
21:25:30 &lt;i2pr&gt; [Slack/str4d] 그건 다음 달 블로그 글의 일부로 하겠습니다
21:25:45 &lt;zzz&gt; str4d, 7월 블로그 글 곧 올라오나요?
21:25:47 &lt;i2pr&gt; [Slack/str4d] 4) 웹사이트 레이아웃 개편
21:26:06 &lt;i2pr&gt; [Slack/str4d] zzz, 곧요. 며칠 내로
21:26:09 &lt;zzz&gt; 좋아요 4) 웹사이트 레이아웃 str4d 진행해 주세요
21:26:49 &lt;i2pr&gt; [Slack/str4d] Elio Qoshi가 웹사이트 레이아웃 개편을 잘 진행하고 있습니다
21:27:47 &lt;i2pr&gt; [Slack/str4d] 참고로, 그는 Whonix 웹사이트를 재구성했고 현재 Tor와 함께 브랜딩과 스타일 가이드를 작업하고 있습니다
21:28:15 &lt;i2pr&gt; [Slack/str4d] (Mozilla에서도 일했습니다)
21:29:08 &lt;zzz&gt; 좋네요
21:29:20 &lt;i2pr&gt; [Slack/str4d] 현재 목표는 텍스트 벽을 줄이고(제가 줄였던 것보다 더), 랜딩 페이지와 내부 페이지 간에 일관된 디자인을 갖추는 것입니다(현재 디자인에 부족한 부분)
21:30:27 &lt;i2pr&gt; [Slack/str4d] 참고로 현재 와이어프레임은 가운데에 단일 열의 콘텐츠를 두고 양옆에 동일한 여백 구터를 두는 형태이며(현재처럼 페이지 내 내비게이션과 메타데이터가 들어갑니다)
21:30:45 &lt;zzz&gt; 좋아요. 지난번 로고와 관련해 논의했듯이, 디자이너에게 어떤 목표를 제시하고 있는지 알아야 그 맥락에서 결과물을 평가할 수 있습니다
21:31:06 &lt;zzz&gt; 4) 관련해 다른 것 있나요?
21:31:24 &lt;i2pr&gt; [Slack/str4d] 첫 페이지 중앙 열의 (꽤 끔찍한) 목록은 특정 앱과 작업으로 유도하는 더 친근한 콜아웃으로 대체될 예정입니다
21:31:25 &lt;poneyhot&gt; 4)에 127.0.0.1 홈 페이지도 포함되나요?
21:31:37 &lt;i2pr&gt; [Slack/str4d] honeypot, 아니요
21:31:52 &lt;zzz&gt; 회의에 더 논의할 것 있나요?
21:32:05 &lt;i2pr&gt; [Slack/str4d] 오, 방금 제안된 프런트 페이지 디자인의 첫 스크린샷을 저에게 보냈네요
21:32:26 &lt;i2pr&gt; [Slack/str4d] 그런데 IRC에 바로 공유할 수는 없어서, 컴퓨터로 돌아가면 공유하겠습니다
21:32:41 &lt;i2pr&gt; [Slack/str4d] router 콘솔 관련해서:
21:32:57 &lt;zzz&gt; 좋아요 5) router 콘솔 str4d 진행해 주세요
21:33:03 &lt;i2pr&gt; [Slack/str4d] 진행 상황은 i2p.i2p.str4d.ui 브랜치를 보세요
21:33:27 &lt;i2pr&gt; [Slack/str4d] CSS는 이제 backbend 변경사항에 맞추어 업데이트되었고, 초안 1차 버전입니다
21:33:45 &lt;zzz&gt; poneyhot, 콘솔 관련해서 회의 안건으로 추가할 게 있었나요?
21:34:18 &lt;i2pr&gt; [Slack/str4d] (시간이 나면 이번 주말 전에 몇 가지 로컬 변경을 푸시하겠습니다)
21:34:18 &lt;i2pr&gt; [Slack/str4d] 피드백 환영합니다
21:34:18 &lt;i2pr&gt; [Slack/str4d] 다만, 이것은 중간 단계일 뿐입니다
21:34:30 &lt;zzz&gt; 5) 관련해 다른 것 있나요?
21:34:37 &lt;i2pr&gt; [Slack/str4d] 현재 변경 사항은 구조적인 부분에는 영향을 미치지 않습니다
21:34:48 &lt;poneyhot&gt; 우선 변경사항을 확인해야겠어요, 저는 알파벳 정렬이 마음에 들지 않습니다
21:34:49 &lt;i2pr&gt; [Slack/str4d] 그건 아마 10월에 할 계획입니다
21:35:09 &lt;zzz&gt; 아, anoncoin 얘기하신 게 그거였군요, 이해했습니다
21:35:17 &lt;zzz&gt; 회의에 더 논의할 것 있나요?
21:35:29 &lt;poneyhot&gt; 그게 i2p에서 가장 중요한 것처럼 보입니다
21:35:35 &lt;i2pr&gt; [Slack/str4d] poneyhot, 그 부분은 완전히 바뀔 수도 있습니다
21:35:51 &lt;i2pr&gt; [Slack/str4d] 아니면 아닐 수도요 ^^
21:36:25 * zzz 가 Negan 스타일로 baffer를 집어 듭니다
21:36:26 &lt;i2pr&gt; [Slack/str4d] 제 목표는 CCC에 맞춰 개선된 router 콘솔을 준비하는 것입니다
21:36:58 &lt;xmpre&gt; 새 router 콘솔 테스트를 기꺼이 돕겠습니다
21:37:09 &lt;xmpre&gt; (그리고 성가신 쿠키 오류도 고쳐지길 바랍니다 :p)
21:37:24 * zzz *bafs* 회의를 종료 </div>
