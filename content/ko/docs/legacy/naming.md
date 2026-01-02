---
title: "명명에 대한 논의"
description: "I2P의 네이밍 모델을 둘러싼 역사적 논쟁과 전역 DNS 방식의 체계를 거부한 이유"
slug: "naming"
layout: "single"
lastUpdated: "2025-02"
accurateFor: "historical"
reviewStatus: "needs-review"
---

> **배경:** 이 페이지는 초기 I2P 설계 시기에 장기간 이어진 논쟁들을 아카이브합니다. 프로젝트가 DNS 방식 조회나 다수결 기반의 레지스트리보다 로컬에서 신뢰하는 주소록을 선호한 이유를 담고 있습니다. 현재 사용 지침은 [Naming documentation](/docs/overview/naming/)을 참고하세요.

## 폐기된 대안

I2P의 보안 목표는 익숙한 명명 체계를 배제한다:

- **DNS 스타일 이름 해석.** 조회 경로상의 어떤 리졸버든 응답을 위조하거나 검열할 수 있다. DNSSEC이 있어도, 침해된 등록기관이나 인증 기관(CA)은 여전히 단일 장애 지점으로 남는다. I2P에서는 목적지는 *그 자체가* 공개 키이므로—조회를 가로채면 그 신원이 완전히 손상된다.
- **투표 기반 이름 지정.** 공격자는 무한정 신원을 만들어낼 수 있어(Sybil 공격(시빌 공격)) 인기 있는 이름에 대한 투표에서 “승리”할 수 있다. 작업증명 완화책은 비용을 높이지만, 무거운 조정 오버헤드를 초래한다.

그 대신, I2P는 의도적으로 네이밍을 전송 계층 위에 둔다. 번들된 네이밍 라이브러리는 대체 스킴들이 공존할 수 있도록 service-provider interface(서비스 제공자 인터페이스, SPI)를 제공하며—어떤 주소록이나 점프 서비스를 신뢰할지는 사용자가 결정한다.

## 로컬 대 글로벌 이름 (jrandom, 2005)

- I2P의 이름은 **로컬에서 고유하지만 사람이 읽을 수 있습니다**. 당신의 `boss.i2p`가 다른 사람의 `boss.i2p`와 일치하지 않을 수 있으며, 그것은 설계상 의도된 것입니다.
- 악의적인 행위자가 이름 뒤에 있는 destination(목적지)을 바꾸도록 당신을 속인다면, 그들은 사실상 서비스를 가로채게 됩니다. 전역 고유성을 사용하지 않음으로써 그러한 유형의 공격을 예방합니다.
- 이름은 즐겨찾기나 IM 닉네임처럼 다루세요—특정 주소록을 구독하거나 키를 수동으로 추가하여 신뢰할 destinations를 직접 선택합니다.

## 흔한 반론과 답변 (zzz)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Concern</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Downloading hosts.txt is inefficient.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">At ~400&nbsp;KB for ~800 hosts the bandwidth impact is minor (~10&nbsp;B/s if refreshed twice daily). ETags already avoid unnecessary transfers. Alternate formats (for example <code>recenthosts.cgi</code>) can deliver only new entries.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“It won’t scale.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A hosts.txt entry is ~500&nbsp;bytes; storing thousands locally is practical. Real-time lookups would dramatically slow browsing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Requires trust and manual setup.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">True—and intentional. Users must choose address book providers they trust. Trust is not binary; forcing configuration encourages users to think about it.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Why not just use DNS?”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS depends on short TTLs and can be hijacked mid-path. I2P destinations are immutable public keys, so DNS semantics map poorly.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Subscriptions rely on specific servers.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscriptions are decentralised—you can add multiple providers or run your own. Completely decentralised systems struggle with conflict resolution and hijacking.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Jump services and hosts.txt feel awkward.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">They are pragmatic trade-offs. Jump services provide just-in-time lookups; subscriptions keep a local cache for performance.</td>
    </tr>
  </tbody>
</table>
## 효율 향상 아이디어 논의

- 증분 업데이트를 제공(마지막 가져오기 이후 추가된 destinations(서비스 주소 식별자)만).
- 전체 hosts 파일과 함께 보조 피드(`recenthosts.cgi`)를 제공.
- 피드를 병합하거나 신뢰 수준으로 필터링하기 위한 스크립트로 자동화 가능한 도구(예: `i2host.i2p`)를 검토.

## 핵심 요점

- 보안이 전역 합의보다 우선합니다: 로컬에서 관리되는 주소록은 하이재킹 위험을 최소화합니다.
- naming API를 통해 여러 이름 지정 방식이 공존할 수 있으며—무엇을 신뢰할지는 사용자가 결정합니다.
- 완전히 탈중앙화된 전역 이름 체계는 여전히 미해결 연구 과제로 남아 있습니다; 보안, 인간 기억 용이성, 전역적 고유성 간의 절충은 여전히 [Zooko’s triangle](https://zooko.com/distnames.html) (이름 체계에서 보안, 인간 기억 용이성, 전역적 고유성의 상충 관계를 설명하는 개념)을 반영합니다.

## 참고 자료

- [네이밍 문서](/docs/overview/naming/)
- [Zooko의 “이름: 탈중앙화, 보안성, 사람에게 의미 있는 것: 둘만 고르라”](https://zooko.com/distnames.html)
- 증분 피드 샘플: [stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
