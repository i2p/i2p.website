---
title: "I2P 개발자 회의 - 2003년 11월 11일"
date: 2003-11-11
author: "jrand0m"
description: "I2P 개발 회의: router 상태, 로드맵 업데이트, 네이티브 modPow 구현, GUI 설치 프로그램, 및 라이선스 관련 논의"
categories: ["meeting"]
---

(wayback machine http://www.archive.org/ 제공)

## 간단한 요약

<p class="attendees-inline"><strong>참석자:</strong> dish, dm, jrand0m, MrEcho, nop</p>

(회의 로그는 회의 중반에 iip가 크래시로 종료되고 핑 타임아웃이 다수 발생한 사실을 숨기기 위해 편집됨, 그러니 이를 단순한 서사로 읽으려 하지 마세요)

## 회의 기록

<div class="irc-log"> [22:02] &lt;jrand0m&gt; 안건 [22:02] &lt;jrand0m&gt; 0) 환영 [22:02] &lt;jrand0m&gt; 1) i2p router [22:02] &lt;jrand0m&gt; 1.1) 상태 [22:02] &lt;jrand0m&gt; 1.2) 로드맵 변경 사항 [22:02] &lt;jrand0m&gt; 1.3) 오픈 서브프로젝트 [22:02] &lt;jrand0m&gt; 2) 네이티브 modPow [22:03] &lt;jrand0m&gt; 2) GUI 설치 프로그램 [22:03] &lt;jrand0m&gt; 3) IM(인스턴트 메시징) [22:03] &lt;jrand0m&gt; 4) 네이밍 서비스 [22:03] &lt;MrEcho&gt; 그 .c 코드 봤어요 [22:03] &lt;jrand0m&gt; 5) 라이선스 [22:03] &lt;jrand0m&gt; 6) 기타? [22:03] &lt;jrand0m&gt; 0) 환영 [22:03] &lt;jrand0m&gt; 안녕하세요. [22:03] &lt;nop&gt; 안녕하세요 [22:03] &lt;jrand0m&gt; 회의 2^6 [22:04] &lt;jrand0m&gt; nop, 거기에 추가할 안건 있어요? [22:04] &lt;jrand0m&gt; 좋아요, 1.1) router 상태 [22:04] &lt;jrand0m&gt; 지금 0.2.0.3이고, 내가 마지막으로 들은 바로는 잘 동작해요 [22:04] &lt;MrEcho&gt; &gt; 0.2.0.3 [22:04] &lt;MrEcho&gt; 맞죠? [22:05] &lt;MrEcho&gt; 저도 돌리고 있어요 .. 괜찮아 보입니다 [22:05] &lt;nop&gt; 아니요 [22:05] &lt;jrand0m&gt; 0.2.0.3 릴리스 이후에 사소한 커밋들이 있었지만, 릴리스할 정도는 아니이에요 [22:05] &lt;nop&gt; 저는 따라잡으려고 하는 중이에요 [22:05] &lt;jrand0m&gt; 굿 [22:06] &lt;jrand0m&gt; 0.2.0.x의 경험과 피드백을 바탕으로, 실행 시 자원 소모를 줄이도록 로드맵을 업데이트했어요 [22:06] &lt;jrand0m&gt; (즉, 사람들이 웹서버 / 등을 돌려도 CPU를 잡아먹지 않도록) [22:06] &lt;jrand0m&gt; 구체적으로(안건 1.2로 이동): http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap [22:06] &lt;MrEcho&gt; 제가 본 바로는 대부분의 router가 이렇게 사용하더군요: TransportStyle: PHTTP [22:07] &lt;MrEcho&gt; 자동으로 phttp로 가나요, 아니면 먼저 tcp를 시도하나요 [22:07] &lt;jrand0m&gt; 흠, 대부분의 router는 PHTTP를 지원하고, 인바운드 연결을 받을 수 있다면 TCP도 지원해야 해요 [22:07] &lt;jrand0m&gt; 가능하기만 하면 TCP를 사용해요 [22:07] &lt;jrand0m&gt; PHTTP는 TCP보다 비용 가중치가 약 1000배 더 커요 [22:08] &lt;jrand0m&gt; (각 transport에 피어로 메시지를 보내는 비용이 얼마나 들지 묻는 GetBidsJob을 보세요) [22:08] &lt;jrand0m&gt; (그리고 사용되는 값은 TCPTransport.getBid와 PHTTPTransport.getBid를 보세요) [22:08] &lt;MrEcho&gt; 알겠어요 [22:08] &lt;jrand0m&gt; 메시지를 주고받을 때 PHTTP를 자주 쓰고 있나요? [22:09] &lt;jrand0m&gt; (당신의 TCP 리스너에 접근할 수 없다는 신호일 수도 있어요) [22:09] &lt;MrEcho&gt; 제 쪽에 URL들을 넣지 않았어요 [22:09] &lt;jrand0m&gt; 아, 오키. [22:09] &lt;MrEcho&gt; 오, 그렇군요 [22:10] &lt;jrand0m&gt; 좋아요, 네, 제 router들은 당신에게 열린 TCP 연결을 가지고 있어요 [22:10] &lt;dm&gt; 정말 친절하네요. [22:10] * jrand0m 은(는) 여러분이 routerConsole.html 구현을 하게 만들어 줘서, 이런 것 때문에 로그를 뒤질 필요가 없어서 기쁩니다 [22:11] &lt;MrEcho&gt; tcp로 연결이 안 되면 phttp로 가는 타임아웃 같은 게 있나요? 그리고 그 타이밍은 어떻게 되죠 [22:11] &lt;jrand0m&gt; 아무튼, 로드맵의 큰 변화는 0.2.1에서 AES+SessionTag 관련 기능을 구현한다는 거예요 [22:11] &lt;MrEcho&gt; 아니면 그걸 설정으로 둘 수 있나요? [22:11] &lt;jrand0m&gt; TCP connection refused / host not found /등이 나오면 그 시도는 즉시 실패 처리하고, 다음 사용 가능한 bid를 시도해요 [22:12] &lt;MrEcho&gt; 그럼 재시도는 없군요 [22:12] &lt;jrand0m&gt; 제 기억으로는 phttp는 30초 타임아웃이 있어요 [22:12] &lt;jrand0m&gt; 재시도할 필요 없어요. 열린 TCP 연결이 있어서 데이터를 보낼 수 있거나, 아니면 없는 거죠 :) [22:12] &lt;MrEcho&gt; ㅋㅋ 알겠어요 [22:13] &lt;MrEcho&gt; 그 이후에도 매번 tcp를 시도하나요, 아니면 건너뛰고 다음 연결에서는 그냥 phttp로 가나요? [22:13] &lt;jrand0m&gt; 현재로서는 매번 tcp를 시도해요. [22:13] &lt;jrand0m&gt; transport들이 아직 히스토리를 유지하지 않아요 [22:13] &lt;MrEcho&gt; 오케이, 굿 [22:14] &lt;jrand0m&gt; (하지만 피어가 4번 실패하면 8분 동안 블랙리스트에 올라요) [22:14] &lt;MrEcho&gt; 상대가 phttp 메시지를 받으면, tcp로 그 메시지를 보낸 router에 연결해야 하죠? [22:14] &lt;jrand0m&gt; 맞아요. tcp 연결이 하나라도 성립되면 그걸 사용하면 돼요. [22:14] &lt;jrand0m&gt; (하지만 양쪽 피어가 phttp만 있다면, 당연히 phttp만 쓰겠죠) [22:15] &lt;MrEcho&gt; 그건 어디에도 tcp 연결을 수립할 수 없다는 뜻이죠 [22:15] &lt;MrEcho&gt; .. 네 그렇죠 [22:16] &lt;MrEcho&gt; 그걸 우회할 방법이 있으면 좋겠네요 [22:16] &lt;jrand0m&gt; 아니요, 제 router 중 하나는 TCP 주소가 없고 PHTTP만 있어요. 하지만 TCP 주소가 있는 피어들과는 TCP 연결을 수립해요. [22:16] &lt;jrand0m&gt; (그러면 그들은 느린 PHTTP 메시지를 내게 보내는 대신, 그 TCP 연결을 통해 메시지를 되돌려 보낼 수 있죠) [22:17] &lt;jrand0m&gt; 아니면 그 말씀이 아니었나요? [22:17] &lt;MrEcho&gt; 네, 제가 헷갈렸네요 [22:17] &lt;jrand0m&gt; 오케이, 문제없어요 [22:18] &lt;jrand0m&gt; 그래서, 업데이트된 일정 정보는 업데이트된 로드맵을 참고하세요 ((Link: http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap)http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap) [22:18] &lt;jrand0m&gt; 좋아요, 1.3) 오픈 서브프로젝트 [22:19] &lt;jrand0m&gt; 드디어 제 palmpilot의 할 일 목록 중 일부를 위키에 올렸어요 (Link: http://wiki.invisiblenet.net/iip-wiki?OpenSubprojects)http://wiki.invisiblenet.net/iip-wiki?OpenSubprojects [22:19] &lt;jrand0m&gt; 그래서 심심하고 코드 프로젝트를 찾고 있다면... :) [22:19] &lt;MrEcho&gt; 헉 [22:20] &lt;MrEcho&gt; 이미 2개 있어요 [22:20] &lt;dish&gt; palmpilot이 있다니, 고급이네요 [22:20] &lt;MrEcho&gt; 제 건 죽었어요 [22:20] &lt;jrand0m&gt; mihi&gt; 거기에 I2PTunnel과 관련해 제가 얼마 전에 했던 생각을 적어둔 항목이 하나 있어요 [22:20] &lt;MrEcho&gt; 왜 그런지 모르겠어요 [22:21] &lt;jrand0m&gt; 네, 예전에 Palm들을 갖고 있었는데, 최근에 이건 프로젝트를 위해 기증받았어요 ;) [22:21] &lt;dish&gt; 회의 안건에 userX가 마지막으로 언제 무언가를 쳤는지 논의하는 걸 넣을 수 있을까요 [22:21] &lt;MrEcho&gt; 젠장, 이놈은 이제 켜지지도 않아요 [22:21] &lt;MrEcho&gt; ㅋㅋ [22:22] &lt;jrand0m&gt; UserX가 4~5개월 동안 아무 말도 안 한 것 같아요 ;) [22:22] &lt;MrEcho&gt; 그거 봇인가요, 아니면 뭐죠? [22:22] &lt;dish&gt; 5개월 전에 뭐라고 했죠? [22:22] &lt;MrEcho&gt; 아마 그가 예전에 접근하던 어떤 박스에서 돌아가는 bitchx일 거예요 .. 그리고 잊어버렸겠죠 [22:22] &lt;jrand0m&gt; 다음 주에 anonCommFramework (i2p의 옛 이름)에 대한 의견을 가져오겠다고요 ;) [22:23] &lt;dish&gt; 하하 [22:23] &lt;jrand0m&gt; 하지만 바쁘겠죠. 인생이 다 그렇죠 [22:23] &lt;jrand0m&gt; 좋아요, 2) 네이티브 modPow [22:23] &lt;MrEcho&gt; 그 C 코드 봤어요 [22:24] &lt;jrand0m&gt; GMP나 다른 MPI 라이브러리를 어떻게 통합할 수 있는지 보여주려고 스텁 .c와 java class를 만들어 뒀는데, 당연히 지금은 동작하지 않아요 [22:25] &lt;jrand0m&gt; 이상적인 건, windows, osx, *bsd, linux용으로 빌드할 수 있고 GPL로 패키징할 수 있는, C 클래스들의 작은 패키지와 그에 연결되는 단순한 Java 래퍼 클래스를 갖추는 거예요

(여기에 중대한 iip 장애를 삽입)

[22:38] &lt;MrEcho&gt; 내가 마지막으로 본 건: [13:25] &lt;jrand0m&gt; ok, 2) native modPow
[22:38] &lt;jrand0m&gt; hi MrEcho
[22:38] &lt;jrand0m&gt; 응, 메인 프록시가 크래시 난 것 같아
[22:39] &lt;jrand0m&gt; 재시작하기 전에 2분만 더 기다려 볼게
[22:39] &lt;MrEcho&gt; ㅇㅋ
[22:39] &lt;MrEcho&gt; 한 번 $25 내면 thenidus.net—내 사이트 중 하나—에 Java 풀 설치해 준대 ...
[22:40] &lt;jrand0m&gt; $25? 소프트웨어 설치해 주는 데 돈 받아?
[22:40] &lt;MrEcho&gt; 잘은 모르겠어 .. 패키지래
[22:40] &lt;MrEcho&gt; 지금 친구랑 얘기 중이야
[22:40] &lt;jrand0m&gt; 그래도 지금 당장은 router들을 올리려고 colo(콜로케이션) 자리를 잔뜩 빌릴 만큼 코드가 충분히 안정적이라고는 확신 못 하겠어. 아직은 :)
[22:41] &lt;dm&gt; 무슨 패키지?
[22:41] &lt;MrEcho&gt; java - jsp
[22:41] &lt;jrand0m&gt; 좋아, 아까 보낸 내용 다시 보낼게:
[22:41] &lt;jrand0m&gt; GMP나 다른 MPI 라이브러리를 어떻게 통합할 수 있는지 보여주려고 stub .c와 Java 클래스를 대충 묶어 봤는데, 당연히 아직은 동작하진 않아
[22:41] &lt;jrand0m&gt; 이상적으론, Windows, OSX, *BSD, Linux용으로 빌드할 수 있는 소규모 C 클래스 모음과 거기에 붙는 단순한 Java 래퍼 클래스를 만들어서, GPL(아니면 덜 제한적인 라이선스)로 패키징하면 좋겠어
[22:41] &lt;jrand0m&gt; 하지만 새로운 로드맵에서 내 현재 작업 항목이 AES+SessionTag로 잡혀서, 이건 예전만큼 시급하진 않아.
[22:42] &lt;jrand0m&gt; 그래도 누가 이걸 맡아 진행하겠다면 최고지 (우리 모두 아는 다른 프로젝트도 이런 패키징에 관심 있을 거라고 확신해)
[22:43] &lt;dm&gt; frazaa?
[22:43] &lt;jrand0m&gt; 헤헷, 어떤 면에선 ;)
[22:44] &lt;jrand0m&gt; 좋아, 3) GUI 설치 프로그램
[22:44] &lt;jrand0m&gt; MrEcho&gt; 안녕
[22:44] &lt;MrEcho&gt; :)
[22:44] &lt;MrEcho&gt; 헤헤
[22:44] &lt;MrEcho&gt; 지금 진행 중이야
[22:44] &lt;jrand0m&gt; 좋지
[22:44] &lt;MrEcho&gt; 별거 없어
[22:45] &lt;MrEcho&gt; 정말 근사하게 만들 아이디어가 있긴 한데 .. 그건 좀 더 나중 얘기야
[22:45] &lt;jrand0m&gt; 설치 프로그램에 1) http://.../i2pdb/ 에서 시드를 자동으로 받아오는 옵션, 2) http://.../i2p/squid.dest 를 자동으로 받아오고 runSquid.bat/runSquid.sh 도 만들어 주는 기능을 넣을까 고민했어. 어때?
[22:45] &lt;jrand0m&gt; 맞아
[22:46] &lt;jrand0m&gt; 응, 설치 프로그램은 최대한 단순했으면 해 - 어떤 화려한 것들을 생각했어?
[22:46] &lt;MrEcho&gt; 문제는 .. 네가 java -jar installer 를 실행하면, 지금 구조상 기본이 non GUI로 뜬다는 거야
[22:46] &lt;MrEcho&gt; jar 파일을 더블클릭하면 GUI가 뜨게 하려면 어떻게 해야 할까
[22:47] &lt;jrand0m&gt; install.jar &lt;-- nongui,  installgui.jar &lt;-- gui
[22:47] &lt;jrand0m&gt; 코드는 분리, 패키지도 분리
[22:47] &lt;MrEcho&gt; 화려하다는 건 눈에 확 띄진 않지만 .. 깔끔하고 잘 다듬어 보이게 하겠다는 뜻이야
[22:47] &lt;jrand0m&gt; 좋아
[22:47] &lt;MrEcho&gt; 아 그렇구나, 오케이
[22:48] &lt;jrand0m&gt; (혹은 install &lt;-- gui installcli &lt;-- cli.  진행 보면서 정하자)
[22:49] &lt;jrand0m&gt; GUI 관련해 더 있을까, 아니면 항목 4)로 넘어갈까?
[22:49] &lt;jrand0m&gt; (대략 일정 생각한 거 있어? 압박 주는 건 아니고, 그냥 물어봐)
[22:51] &lt;MrEcho&gt; 지금은 모르겠어
[22:51] &lt;jrand0m&gt; 굿
[22:51] &lt;jrand0m&gt; 좋아, 4) IM
[22:51] &lt;jrand0m&gt; thecrypto가 없으니, 그래서.....
[22:51] &lt;jrand0m&gt; 5) 네이밍 서비스
[22:51] &lt;jrand0m&gt; wiht도 없네...
[22:51] &lt;jrand0m&gt; 핑
[22:52] &lt;dish&gt; 의제 번호 세기가 틀렸어
[22:52] &lt;dish&gt; 3) IM
[22:52] &lt;jrand0m&gt; 맞아, 전에 의제 2번이 두 개였는데
[22:52] &lt;dish&gt; 4) 네이밍
[22:52] &lt;dish&gt; ;)
[22:52] &lt;jrand0m&gt; (native modPow와 GUI 설치 프로그램)
[22:52] &lt;jrand0m&gt; 보라구, 우리는 유연하고 뭐 그런 거야
[22:59] &lt;jrand0m&gt; 좋아, 로그를 위해서 계속할게
[22:59] &lt;jrand0m&gt; 6) 라이선스
[23:00] &lt;jrand0m&gt; GPL보다 덜 제한적인 쪽으로 가볼까 생각 중이야. 우리는 MIT 코드도 조금 쓰고 있고, 다른 파일 하나가 GPL이긴 한데(그건 그냥 base64 인코딩이라 쉽게 대체 가능해). 그 외의 코드는 전부 나나 thecrypto가 저작권을 갖고 있어.
[23:00] * dish mihi i2p tunnel 코드 부분을 살펴봄
[23:01] &lt;jrand0m&gt; 아 맞다, mihi가 그걸 GPL로 공개했지만, 원하면 다른 걸로도 내고 싶어할 수 있어
[23:01] &lt;jrand0m&gt; (하지만 i2ptunnel은 본질적으로 서드파티 앱이라, 원하는 방식으로 라이선스를 정할 수 있어)
[23:02] &lt;jrand0m&gt; (다만 i2p SDK가 GPL이라, GPL을 따를 수밖에 없었지)
[23:02] &lt;MrEcho&gt; 진작 그랬어야지
[23:02] &lt;jrand0m&gt; 글쎄. 라이선스는 내 전문이 아닌데, 최소한 LGPL로 가고 싶긴 해
[23:02] * dish I2P HTTP Client의 mihi 코드에 대한 10~20줄 정도의 변경사항은 mihi 라이선스가 뭐든 그걸로 공개함
[23:03] &lt;jrand0m&gt; 헤헤 :)
[23:06] &lt;jrand0m&gt; 어쨌든, 7) 기타?
[23:07] &lt;jrand0m&gt; i2p 관련해서 질문 / 우려 / 아이디어 있는 사람?
[23:07] &lt;dish&gt; 하나 물어볼게
[23:07] &lt;dish&gt; I2P에 그룹 이름 기능 같은 게 있나요?
[23:07] &lt;jrand0m&gt; 그룹 이름 기능?
[23:07] &lt;dm&gt; 팀 디스커버리 채널!
[23:07] &lt;MrEcho&gt; ㅋㅋ
[23:08] &lt;dish&gt; 그러니까, 사설이거나 분리된 네트워크를 원해도, 어떤 router들이 어떻게 섞여 버리면 그룹 이름이 없을 때 두 네트워크가 합쳐질 수 있잖아요
[23:08] &lt;MrEcho&gt; WASTE를 떠올리는 거야
[23:08] &lt;jrand0m&gt; 아하
[23:08] &lt;dish&gt; 그게 왜 필요할진 모르겠지만, 혹시나 해서 물어봤어요
[23:08] &lt;jrand0m&gt; 응, 네트워크 설계를 초기에 할 때 그런 걸 실험해 봤어
[23:09] &lt;jrand0m&gt; 그건 지금(또는 비교적 가까운 미래 [6~12개월])에 필요한 수준보다 더 고급이라서, 나중에 통합될 수도 있어
[23:09] &lt;dish&gt; 아니면 하나의 큰 네트워크로 유지하는 게 더 낫기 때문에 나쁜 아이디어인가요
[23:09] &lt;dm&gt; i2pisdead
[23:09] &lt;jrand0m&gt; 헤헷 dm
[23:10] &lt;nop&gt; 조용히 해
[23:10] &lt;jrand0m&gt; 아니야 dish, 좋은 아이디어야
[23:10] &lt;dm&gt; nop: 터프가이야?
[23:10] &lt;jrand0m&gt; 그게 본질적으로 릴리스 0.2.3에서 하는 거야 -- 제한된 라우트(restricted routes)
[23:10] &lt;jrand0m&gt; (즉, 소규모의 사설(신뢰된) 피어 집합이 있고, 그들이 누구인지 모두가 알게 하고 싶진 않지만, 그래도 그들과 통신은 하고 싶은 경우)
[23:15] &lt;jrand0m&gt; 좋아, 더 있을까?
[23:15] &lt;nop&gt; 아니, 그냥 장난친 거야
[23:18] &lt;dm&gt; 재밌냐?
[23:20] &lt;jrand0m&gt; 좋아, 음, 중간에 iip가 몇 번 크래시하긴 했지만 /재밌는/ 미팅이었어 ;)
[23:21] * jrand0m 미팅을 *baf* 하며 마무리함 </div>
