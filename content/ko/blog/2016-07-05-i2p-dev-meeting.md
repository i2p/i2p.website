---
title: "I2P 개발자 회의 - 2016년 7월 5일"
date: 2016-07-05
author: "zzz"
description: "2016년 7월 5일자 I2P 개발 회의 기록."
categories: ["meeting"]
---

## 간단 요약

<p class="attendees-inline"><strong>참석자:</strong> dg, psi, sadie, str4d, Zerolag, zzz</p>

## 회의 기록

<div class="irc-log">21:00:23 &lt;zzz&gt; 0) 안녕
21:00:23 &lt;zzz&gt; 1) HOPE 업데이트 (zzz) http://zzz.i2p/topics/1968
21:00:23 &lt;zzz&gt; 2) 0.9.27 업데이트 (zzz)
21:00:23 &lt;zzz&gt; 3) Summer of X 업데이트 (sadie/str4d)
21:00:27 &lt;zzz&gt; 0) 안녕
21:00:29 &lt;zzz&gt; 안녕
21:00:47 &lt;psi&gt; 안녕
21:00:48 &lt;zzz&gt; 1) HOPE 업데이트 (zzz) http://zzz.i2p/topics/1968
21:00:48 &lt;i2pr&gt; [Slack/str4d] 안녕
21:01:13 &lt;zzz&gt; 좋아요, HOPE까지 2주 반 남았습니다. 금요일에 Lance와의 점심 미팅은 아직 미정(TBD)입니다
21:01:42 &lt;zzz&gt; 금요일 점심은 비워두세요. 그 주가 되어야 취소인지 진행인지 알 수 있을 것 같아요
21:01:49 &lt;zzz&gt; 그곳에서 모두 뵙길 기대합니다
21:01:54 &lt;zzz&gt; 1) 관련해서 더 있을까요?
21:02:06 &lt;i2pr&gt; [Slack/str4d] 이제 확실히 못 가게 되었어요
21:02:20 &lt;i2pr&gt; [Slack/str4d] 타이밍이 제 편이 아니었네요 ;_;
21:02:51 &lt;psi&gt; 올해는 HOPE에 못 갈 것 같네요
21:03:14 &lt;i2pr&gt; [Slack/sadie] 저는 HOPE에 갈 거예요
21:03:38 &lt;zzz&gt; 2) 0.9.27 업데이트 (zzz)
21:04:13 &lt;zzz&gt; .27은 예상대로 천천히 진행 중입니다. 이 속도라면 .27 릴리스는 8월에서 9월로 미뤄질 겁니다
21:04:31 &lt;zzz&gt; 우리가 X 관련 작업과, 아마도 NTCP2에 집중하는 동안에는요
21:04:47 &lt;i2pr&gt; [Slack/str4d] 저는 괜찮습니다
21:04:50 &lt;zzz&gt; 다들 괜찮을까요?
21:05:02 &lt;dg&gt; 서두를 건 없으니 괜찮습니다
21:05:09 &lt;dg&gt; 결국 필요할 때 릴리스하면 됩니다
21:05:28 &lt;zzz&gt; 26은 정말 안정적인 것 같습니다. 유일한 문제는 bote class not found 건이고, 이에 대해서는 trac에서 추가 정보를 기다리고 있습니다
21:05:52 &lt;dg&gt; Debian 패키지 관련해서 문제라고 생각되는 게 하나 있었습니다
21:05:56 &lt;i2pr&gt; [Slack/str4d] 그리고 그 덕분에 8월에 플러그인을 .27에 넣는 작업을 진행할 기회가 생깁니다
21:05:57 &lt;zzz&gt; 제 생각대로라면 간단한 변경과 deb/ubuntu 리빌드만으로 고칠 수 있을 겁니다
21:06:00 &lt;dg&gt; 티켓으로 남겨두겠습니다. 
21:06:12 &lt;zzz&gt; 2) 관련해서 더 있을까요?
21:06:38 &lt;psi&gt; .27이 i2pd에 영향을 주나요?
21:07:19 &lt;zzz&gt; IPv6 피어 테스트가 있습니다, 맞아요. 지원되기 전까지는 i2pd를 27로 올리면 안 됩니다
21:07:39 &lt;psi&gt; 알겠어요
21:07:50 &lt;zzz&gt; 자바 일정에 맞출 필요는 없지만요
21:07:53 &lt;zzz&gt; 2) 관련해서 더 있을까요?
21:08:42 &lt;zzz&gt; 3) Summer of X 업데이트 (sadie/str4d)
21:08:51 &lt;zzz&gt; sadie, str4d, 어떻게 돼가고 있나요?
21:08:52 &lt;i2pr&gt; [Slack/str4d] 아직 아닌 것 같아요?
21:08:55 &lt;i2pr&gt; [Slack/str4d] 아, 맞네요
21:08:55 &lt;i2pr&gt; [Slack/str4d] 아니요
21:10:30 &lt;zzz&gt; 회의에 릴레이를 쓰는 것의 위험일까요?
21:10:40 &lt;i2pr&gt; [Slack/str4d] 지금까지 잘 진행되어 왔다고 생각해요
21:10:55 &lt;i2pr&gt; [Slack/str4d] 벌써 한 달이 되었고, 이에 대해 블로그 글을 세 개(IIRC) 올렸습니다
21:11:46 &lt;zzz&gt; 좋아요, 7월에는 무엇을 하나요?
21:12:02 &lt;i2pr&gt; [Slack/str4d] 앱
21:12:05 &lt;i2pr&gt; [Slack/str4d] 대외 홍보
21:12:15 &lt;i2pr&gt; [Slack/str4d] 그래서 저는 Tahoe-LAFS와 함께 작업할 예정입니다
21:12:29 &lt;i2pr&gt; [Slack/str4d] 그들의 I2P 통합 작업을요
21:13:12 &lt;zzz&gt; Transmission 및/또는 libtorrent 작업을 할 자원봉사자 있나요? 지금은 고장 천지의 늪처럼 보이네요
21:13:14 &lt;i2pr&gt; [Slack/str4d] 그리고 Lightning Browser의 I2P 라이브러리를 업데이트하는 PR(풀 리퀘스트)도 제출할 예정입니다
21:13:45 &lt;i2pr&gt; [Slack/str4d] 네, 다른 API를 익히기에 절대 늦지 않았죠
21:13:59 &lt;i2pr&gt; [Slack/str4d] 이번 달에 우리가 도와봤으면 하는 다른 프로젝트들:
21:14:02 &lt;zzz&gt; 홍보가 핵심이니, Twitter와 이메일로 널리 알립시다
21:14:08 &lt;psi&gt; 예전에 Transmission에서는 무엇을 했었죠?
21:14:31 &lt;zzz&gt; Transmission용 I2P 포크가 있어요, zzz.i2p의 스레드를 보세요
21:14:33 &lt;i2pr&gt; [Slack/str4d] psi, SAM 지원이요
21:14:52 &lt;i2pr&gt; [Slack/str4d] libtorrent에서요
21:14:54 &lt;psi&gt; 그건 libsam3 이전이었죠, 그렇죠?
21:14:58 &lt;psi&gt; 완전히 썩어버렸을 것 같네요
21:15:09 &lt;i2pr&gt; [Slack/str4d] (Transmission이 그걸 사용하지 않는다는 걸 자꾸 잊네요)
21:15:23 &lt;zzz&gt; sadie, 7월 PR(풀 리퀘스트) 계획은 뭐가 있나요?
21:15:31 &lt;i2pr&gt; [Slack/str4d] 음, 새로 깔끔히 포크하는 게 더 쉬울 수도 있겠네요
21:15:58 &lt;i2pr&gt; [Slack/str4d] 말씀드렸듯, 제가 구상 중인 다른 프로젝트들:
21:16:01 &lt;i2pr&gt; [Slack/str4d] - IPFS(Go와 Python 구현체)
21:16:27 &lt;i2pr&gt; [Slack/str4d] - OpenBazaar(곧 IPFS 사용 예정)
21:16:34 &lt;i2pr&gt; [Slack/str4d] - ZeroNet
21:17:02 &lt;i2pr&gt; [Slack/str4d] 이 중 무엇이든 누군가가 도와보기 좋은 후보예요
21:17:33 &lt;villain&gt; 안녕하세요 i2p 여러분 :) zzz: 방금 웹사이트용 패치를 보냈어요, 전달되길 바랍니다 
21:17:38 &lt;psi&gt; 아직 IPFS의 기여 가이드를 파악하지 못했어요
21:17:45 &lt;zzz&gt; 좋아요, 훌륭해요. 3) 관련해서 더 있을까요? Sadie?
21:18:05 &lt;zzz&gt; 고마워요 villain, 지금 회의 중이라 나중에 확인할게요
21:18:06 &lt;psi&gt; IPFS에 참여하고 싶은데 방법을 아직 못 찾았어요.
21:18:25 &lt;Zerolag&gt; ZeroNet을 한번 직접 다뤄보고 싶네요. I2P 위에서 얼마나 잘 돌아가는지 보고 싶습니다.
21:18:28 &lt;i2pr&gt; [Slack/str4d] Psi, 이번 주말에 그들의 온보딩이 어떻게 되는지 살펴볼게요
21:19:08 &lt;psi&gt; Zerolag: 마지막으로 확인했을 때 ZeroNet에 I2P를 추가하는 건 꽤 쉬울 거예요. 이미 Tor용 보일러플레이트가 있어서요
21:19:11 &lt;i2pr&gt; [Slack/str4d] Zerolag, 좋아요! 그들은 토렌트 기반이라, 우리의 토렌트 사양에 맞게 수정이 필요할 거예요
21:19:21 &lt;psi&gt; 그리고 i2p.socket도 점점 준비되어 가고 있어요
21:19:33 &lt;i2pr&gt; [Slack/str4d] (클리어넷과 I2P 토렌트를 나란히 지원하기 위해)
21:19:54 &lt;psi&gt; ZeroNet이 메인라인 비트토렌트를 씀?
21:20:01 &lt;i2pr&gt; [Slack/str4d] 잘 모르겠어요
21:20:17 &lt;psi&gt; 안 쓰는 걸로 꽤 확신하지만, 뭐…
21:20:22 &lt;i2pr&gt; [Slack/str4d] (어떤 구현체를 쓰는지)
21:20:36 &lt;zzz&gt; 3) 관련해서 더 있을까요? Sadie?
21:20:58 &lt;i2pr&gt; [Slack/str4d] psi, 그들은 비트코인의 암호 기술과 BitTorrent 네트워크를 사용합니다
21:21:39 &lt;i2pr&gt; [Slack/str4d] Sadie가 이 회의를 겹치게 잡았을지도 모르겠네요
21:21:49 &lt;zzz&gt; 그럼 넘어가죠. 회의에서 더 다룰 사항 있나요?
21:22:21 &lt;zzz&gt; 다시 오후 9시로 괜찮나요? echelon이 없는 걸 보니 시간 변경 때문일 수도, 아닐 수도 있겠네요
21:22:46 &lt;psi&gt; 오후 9시는 괜찮아요
21:22:46 &lt;Zerolag&gt; str4d 좋아요, 토렌트에 대한 I2P 사양은 무엇인가요?
21:23:09 * zzz baffer를 예열한다
21:23:12 &lt;i2pr&gt; [Slack/str4d] 저는 더 없습니다. 프로젝트 하나 골라서 도와주세요! :-)
21:23:31 &lt;i2pr&gt; [Slack/str4d] 오후 9시는 제겐 딱 좋아요
21:24:05 &lt;Zerolag&gt; 오후 9시에 꼭 여기 있을게요
21:24:15 &lt;i2pr&gt; [Slack/str4d] Zerolag, I2P 웹사이트를 보세요 (Docs -&gt; Apps -&gt; BitTorrent)
21:24:19 * zzz *baffffs* 회의 종료 </div>
