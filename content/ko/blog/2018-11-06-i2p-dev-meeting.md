---
title: "I2P 개발자 회의 - 2018년 11월 06일"
date: 2018-11-06
author: "eche|on"
description: "2018년 11월 6일자 I2P 개발 회의록."
categories: ["meeting"]
---

## 간단한 요약

<p class="attendees-inline"><strong>참석자:</strong> echelon, str4d, meeh, zlatinb</p>

## 회의 기록

<div class="irc-log"> &lt;eche|on&gt; 0) 안녕하세요 &lt;eche|on&gt; 1) 0.9.38 개발 상태 (echelon) &lt;eche|on&gt; 2) LS2 상태 (echelon) &lt;eche|on&gt; 3) 스크럼 상태 (zlatinb) &lt;eche|on&gt; 이전에 i2p 스레드에 다른 주제는 추가되지 않았습니다. &lt;eche|on&gt; 0) &lt;eche|on&gt; 안녕하세요! &lt;eche|on&gt; 환영합니다! &lt;zlatinb&gt; 안녕하세요 &lt;eche|on&gt; 안건에 추가할 내용 있나요? &lt;eche|on&gt; 없는 것 같네요 &lt;eche|on&gt; 1) 0.9.38 개발 상태 &lt;eche|on&gt; 0.9.38은 주로 콘솔 업데이트가 될 예정이며, Sadie와 UX, UI 팀이 열심히 작업 중입니다. 이는 금요일에 Alex가 만든 라이브 스팀에서 보셨듯이 그렇습니다 &lt;eche|on&gt; 명세를 찾기 어렵지만, 진행은 잘 되고 있습니다 &lt;eche|on&gt; 콘솔에서 무엇을 변경할 수 있는지 파악하고 있으며, 그 첫 부분을 0.9.38에 포함할 예정입니다 &lt;eche|on&gt; 모든 변경 사항이 반영되기까지는 몇 달이 걸릴 예정이며, 0.9.38에는 모두 포함되지 않습니다 &lt;str4d&gt; 안녕하세요 &lt;eche|on&gt; 현재 0.9.38 릴리스 계획은 12월로, 35c3 직전에 출시하는 것입니다 &lt;eche|on&gt; 1)와 관련해 더 있을까요 ? &lt;zlatinb&gt; 저는 0,9.38이 1월일 줄 알았는데, 괜찮습니다 &lt;eche|on&gt; 네, 작업이 너무 많으면 35c3 이후 1월로 연기하겠습니다 &lt;zlatinb&gt; 1)에 관해 저는 더 없습니다 &lt;eche|on&gt; 좋아요 &lt;eche|on&gt; 2) LS2 상태 업데이트 &lt;eche|on&gt; 여기서 특별히 업데이트할 중요한 내용은 없고, 개발 회의는 진행 중이며 주제들이 논의되고 있지만 아직 코드가 공개되지는 않았습니다 &lt;eche|on&gt; 어렵고 힘든 작업이며 주제가 많아 더 시간이 걸립니다. 추정으로는 .40 이전에는 아닐 것 같습니다 &lt;eche|on&gt; 2)에 대해 더 있을까요 &lt;eche|on&gt; ? &lt;str4d&gt; 피드백을 주고 싶은 분들은 https://geti2p.net/spec/proposals/123-new-netdb-entries 를 확인해 주세요 (현재 대부분의 변경 사항이 그 문서를 중심으로 이뤄지고 있습니다) &lt;eche|on&gt; 네, 적극적으로 참여해서 피드백을 주세요 &lt;eche|on&gt; 그럼 3) 스크럼 상태는 zlatinb에게 넘기겠습니다 &lt;zlatinb&gt; 안녕하세요.  지금 채널에는 eche|on과 meeh만 있으니, 여러분이 1-2-3을 (병렬로) 진행해서 알려주시겠어요 &lt;eche|on&gt; 1) 자금(funding), 서버 작업, 35c3 준비, 티켓 구매 완료 &lt;eche|on&gt; 2) 이 작업 계속 진행 &lt;eche|on&gt; 3) 차단 요소(blocker) 없음 &lt;eche|on&gt;  &lt;meeh&gt; 1) OSX 런처 정리 & Firefox 프로파일 &lt;meeh&gt; 2) 서버 마이그레이션 &lt;meeh&gt; 3) 테스트넷 개발 &lt;meeh&gt; 4) 차단 요소 없음 &lt;zlatinb&gt; 제 것은 다음과 같습니다: 1) 지난달에는 Sadie, Alex와 함께 UX 작업을 했고, 테스트넷 정의(게시물은 zzz.i2p 포럼에 있음), 사용자 정의 Firefox I2P 프로파일(게시물은 i2pforum에 있음) 2) 추가 UX 작업, 코드 서명 인증서 3) 차단 요소 없음 &lt;str4d&gt; ERR_OUT_OF_BOUNDS_WRITE &lt;zlatinb&gt; lol &lt;eche|on&gt; 맞아요, Firefox I2P 프로파일을 테스트해 주세요, zlatinb 링크를 공유해 주세요 &lt;zlatinb&gt; https://github.com/eyedeekay/firefox.profile.i2p/releases &lt;eche|on&gt; 감사합니다 &lt;meeh&gt; 좋네요, 감사합니다 &lt;eche|on&gt; 35c3 관련: 코어 팀은 라이프치히에서 만날 예정입니다 &lt;eche|on&gt; 다른 분들도 오고 싶으시면, 만나서 I2P 주제들을 논의하거나 커피/맥주/디저트를 함께 하면서 시간을 보내면 좋겠습니다 &lt;eche|on&gt; 좋아요, 안건은 여기까지입니다, 추가할 사항 있나요? &lt;str4d&gt; 재미있게 보내세요! 저는 올해 35c3에는 가지 못하지만 1월 RWC에는 갈 예정입니다. &lt;eche|on&gt; *me sidekick baffer를 워밍업함* &lt;eche|on&gt; 좋네요, Alex도 Sadie와 함께 참석할 계획입니다 &lt;eche|on&gt; *baffer가 휘두름* &lt;str4d&gt; Aesome &lt;str4d&gt; s/Ae/Awe/ &lt;eche|on&gt; *baff* 회의를 종료합니다. 참석해 주셔서 감사합니다. 다음 회의는 12월 4일 UTC 오후 8시에 다시 봬요 </div>
