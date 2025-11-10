---
title: "I2P 개발자 회의 - 2017년 9월 5일"
date: 2017-09-05
author: "zzz"
description: "2017년 9월 5일자 I2P 개발 회의록."
categories: ["meeting"]
---

## 간단한 요약

<p class="attendees-inline"><strong>참석자:</strong> echelon, psi, R4SAS, str4d, zzz</p>

## 회의 기록

<div class="irc-log">20:00:00 &lt;zzz&gt; 0) 안녕하세요
20:00:00 &lt;zzz&gt; 1) 0.9.32 업데이트 (zzz)
20:00:00 &lt;zzz&gt; 2) 34C3 자금 지원 이메일 리마인더 (zzz/echelon)
20:00:03 &lt;zzz&gt; 0) 안녕하세요
20:00:05 &lt;zzz&gt; 안녕하세요
20:00:44 &lt;zzz&gt; 1) 0.9.32 업데이트 (zzz)
20:00:58 &lt;R4SAS&gt; 안녕하세요
20:01:09 &lt;zzz&gt; ok, str4d가 UI 업데이트를 일부 했고, 저는 prop 141 구현을 시작했지만 아직 아무것도 체크인하지 않았습니다
20:01:37 &lt;zzz&gt; 우리는 10월 초 릴리즈를 목표대로 진행 중입니다
20:01:49 &lt;i2pr&gt; [Slack/str4d] 안녕하세요
20:02:03 &lt;zzz&gt; str4d가 그의 benchmark 브랜치를 prop 하길 원하는 것 같은데, 곧 그렇게 해야 하지 않을까요? 그의 티켓에 코멘트를 달아두었습니다
20:02:20 &lt;psi_&gt; 예
20:02:36 &lt;i2pr&gt; [Slack/str4d] 지금까지는 작은 UI 수정만 푸시했습니다; 더 많은 이슈를 해결하는 변경들이 로컬에 대기 중인데, 제 git -&gt; mtn 프로세스를 거쳐야 합니다
20:03:09 &lt;i2pr&gt; [Slack/str4d] benchmark 코멘트들을 확인하고 이번 주 말까지 마무리 / 푸시하겠습니다
20:03:57 &lt;zzz&gt; ok 언젠가 릴리즈 프로세스에 대해 당신과 얘기해야겠어요. .31에 대해 닫히지 않은 블로커 티켓들이 있었는데, 아마 릴리즈 전에 반드시 그것들이 닫히도록 해야 할 것입니다
20:04:08 &lt;zzz&gt; 아니면 블로커라는 게 무슨 의미가 있겠습니까
20:04:23 &lt;i2pr&gt; [Slack/str4d] 맞습니다
20:04:36 &lt;zzz&gt; 안건 1)에 대해 더 있을까요?
20:06:01 &lt;zzz&gt; 2) 34C3 자금 지원 이메일 리마인더 (zzz/echelon)
20:06:11 &lt;psi&gt; 이번 릴리즈에서 hostnames 제거가 필요합니까?
20:06:15 &lt;psi&gt; RI에서
20:06:25 &lt;psi&gt; 아, 랙이네
20:06:33 &lt;zzz&gt; 마이그레이션 논의는 proposal 텍스트를 참조하세요
20:06:45 &lt;psi&gt; ㅇㅋ
20:07:07 &lt;i2pr&gt; [Slack/str4d] zombie 완화책 논의 없이 이번 릴리즈에 포함하는 데에는 -1입니다
20:07:08 &lt;zzz&gt; ok 34C3 관련, 자금 지원이나 무료 티켓을 원한다면 반드시 9월 30일까지 echelon에게 이메일을 보내야 합니다
20:07:43 &lt;zzz&gt; 추가로, echelon 쪽 서버 이슈가 있었다고 하니, 여러분의 이메일을 받았다는 그의 ACK을 받지 못했다면 다시 보내세요
20:08:46 &lt;zzz&gt; 우리는 사람들을 위한 자금이 충분히 있지만, 반드시 신청해야 합니다. 이달 말 이후에 요청하는 사람들은 지원하지 않습니다
20:09:48 &lt;zzz&gt; 그러니 다시 한 번, echelon이 여러분의 요청을 수신했음을 확인받으세요
20:10:03 &lt;zzz&gt; 예산은 다음 달 미팅에서 확정하겠습니다
20:10:19 &lt;zzz&gt; 안건 2)에 대해 더 있을까요?
20:10:36 &lt;i2pr&gt; [Slack/str4d] 제 쪽에는 없습니다.
20:11:26 &lt;zzz&gt; 미팅에서 더 논의할 것 있나요?
20:11:54 &lt;psi&gt; 할 말이 하나 있어요
20:12:02 &lt;zzz&gt; psi, 말씀하세요
20:12:03 &lt;psi&gt; 하지만 길고 지루해요
20:12:09 &lt;psi&gt; 그 정렬된 아웃바운드 tunnels 아이디어예요
20:12:36 &lt;psi&gt; 원래는 OBEP 부하 감소 기법으로 당신에게 제안했었죠
20:12:45 &lt;psi&gt; 그건 좋은 부수 효과예요
20:12:53 &lt;psi&gt; 하지만 그게 원래 의도는 아닙니다
20:13:10 &lt;psi&gt; 원래 의도는 패킷 드롭을 줄이는 것이었어요
20:13:59 &lt;zzz&gt; ok, 그래서 이에 대해 무엇을 논의하고 싶으신가요?
20:14:08 &lt;psi&gt; 제 질문은: Java I2P에서 aligned outbound tunels을 구현할 의향이 있나요?
20:14:22 &lt;psi&gt; 아니면 당신들에겐 너무 실험적인가요?
20:14:53 &lt;psi&gt; i2pd 코드만큼 Java I2P의 코드에는 익숙하지 않아서요
20:14:57 &lt;zzz&gt; 지금은 세부 내용을 잊어버려서 답을 못 하겠네요. 문서로 정리해서 어딘가에 올려주시면 기꺼이 답변드리겠습니다
20:15:09 &lt;psi&gt; 오케이
20:15:15 &lt;psi&gt; 이제 미팅을 마쳐도 될 것 같아요
20:15:26 &lt;psi&gt; 아이디어는 OBEP == IBGW 입니다
20:15:35 &lt;psi&gt; OB tunnel에 hop을 하나 더 추가하는 거죠
20:15:38 &lt;eche|offf&gt; 제 쪽에서는 아직 없습니다
20:15:43 &lt;psi&gt; 즉, OBEP == IBGW가 되도록요
20:16:14 &lt;psi&gt; 패킷 드롭과 OBEP 압력을 줄이기 위해서요
20:16:30 &lt;psi&gt; (더 많은 tunnels이라는 대가로)
20:16:51 &lt;zzz&gt; ok, 이미 구현했으니 이점에 대한 데이터가 있으면 큰 도움이 될 거예요
20:17:10 &lt;zzz&gt; aligned outbound tunnels에 대해 더 있을까요?
20:17:31 &lt;psi&gt; 초기 관찰로는 초기 RTT가 이후의 RTT와 같다는 점이에요
20:17:44 &lt;psi&gt; 즉, 초기 RTT 스파이크가 없어요
20:17:57 &lt;psi&gt; 아마도 OBEP의 압력이 해소되기 때문일 수 있어요
20:18:03 &lt;psi&gt; 하지만 그건 그냥 가정일 뿐이죠
20:18:15 &lt;psi&gt; 이걸 testnet에서 테스트해보고 싶어요, 우리에겐 docker로 만든 게 있으니까요.
20:18:25 &lt;i2pr&gt; [Slack/str4d] 성능 benchmark로 만들 수 있는 게 있으면 알려주세요
20:18:25 &lt;psi&gt; 정량적 수치를 모으려고요 등등
20:19:01 &lt;psi&gt; 저도 그래요, 좋은 perf benchmark를 뭘로 해야 할지 모르겠네요
20:19:18 &lt;psi&gt; 지금은 openvpn 위에서 icmp ping을 써왔어요
20:19:23 &lt;i2pr&gt; [Slack/str4d] 사실 이건 benchmark라기보다 metric에 가깝습니다. 네트워크 성능에도 의존하고, endpoint 위치에 따라 달라질 가능성이 크거든요
20:19:27 &lt;psi&gt; 아마 최선의 방법은 아니겠죠
20:19:48 &lt;i2pr&gt; [Slack/str4d] 그래도 반복 가능하게 만들 수 있다면, 제가 수집을 시작하려는 벤치마크 모음에 추가하고 싶습니다
20:20:18 &lt;psi&gt; 지금은 dtls로 연결되는 데 걸리는 시간과, 그 다음에 ping으로 지연을 측정하는 방식을 씁니다
20:20:31 &lt;psi&gt; 그건 Java I2P에 그대로 옮기긴 어렵다고 생각해요
20:20:45 &lt;psi&gt; socks5 udp가 동작하지 않는 한요
20:20:49 &lt;psi&gt; 아니면 SAM 관련 작업을 좀 하거나요
20:21:23 &lt;zzz&gt; aligned outbound tunnels에 대해 더 있을까요?
20:21:31 &lt;psi&gt; aligned outbound tunnels는 아직 실험적이고, 늘어난 tunnel 수가 그만한 가치가 있는지 아직 모르겠어요
20:21:49 &lt;psi&gt; 그래서 더 많은 연구가 필요하고, 지금 i2pd 쪽에서 과학적으로 검증 중이에요
20:21:56 &lt;psi&gt; 알려드릴게요
20:22:12 &lt;i2pr&gt; [Slack/str4d] 좋습니다, #i2p-science에서 진행 상황을 계속 알려주세요 :slightly_smiling_face:
20:22:20 &lt;psi&gt; ㅇㅋ
20:22:21 &lt;zzz&gt; 좋습니다, 업데이트 고마워요 psi
20:22:25 &lt;zzz&gt; aligned outbound tunnels에 대해 더 있을까요?
20:22:53 &lt;psi&gt; 마지막으로 한 가지: tunnels 정렬에 더해 무언가를 더 하는 게 가치가 있을지도 모릅니다, 즉 tor의 rend 스펙 같은 것요
20:23:17 &lt;psi&gt; 그게 정확히 무엇인지는 아직 모르겠고, #i2p-science에서 큰소리로 생각해 보겠습니다
20:23:20 &lt;psi&gt; (참여해 주세요)
20:23:29 &lt;psi&gt; 이상입니다
20:23:41 &lt;i2pr&gt; [Slack/str4d] 저는 이상입니다
20:23:49 &lt;zzz&gt; 미팅에서 더 논의할 것 있나요?
20:24:28 &lt;psi&gt; 전 괯찮습니다
20:25:15 &lt;zzz&gt; 모두들 고마워요, 4주 후에 봅시다, 그때가 .32 릴리즈 시점입니다
20:26:10 * zzz ***bafffs*** 회의 종료 </div>
