---
title: "I2NP 개요"
description: "I2P 네트워크 프로토콜(I2NP) 개요 - 메시지 형식, 유형, 우선순위 및 크기 제한."
slug: "i2np-overview"
aliases:
  - "/ko/docs/protocol/i2np"
  - "/ko/docs/protocol/i2np/"
  - "/ko/i2np"
  - "/ko/i2np/"
category: "프로토콜"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## 개요

I2CP와 다양한 I2P 전송 프로토콜 사이에 위치한 I2P 네트워크 프로토콜(I2NP)은 라우터 간 메시지의 라우팅 및 믹싱을 관리하며, 여러 공통 전송 방식을 지원하는 피어와 통신할 때 어떤 전송 방식을 사용할지 선택하는 기능도 담당합니다.

## I2NP 정의

I2NP(I2P 네트워크 프로토콜) 메시지는 원-홉(one-hop), 라우터 간, 점대점(point-to-point) 메시지에 사용할 수 있습니다. 메시지를 암호화하고 다른 메시지 안에 래핑함으로써 여러 홉을 거쳐 최종 목적지까지 안전하게 전송할 수 있습니다. 우선순위는 출발지에서만 로컬로 사용되며, 외부 전송을 위해 대기열에 들어갈 때 적용됩니다.

아래 나열된 우선순위는 최신이 아닐 수 있으며 변경될 수 있습니다. 우선순위 큐 구현 방식은 달라질 수 있습니다.

## 메시지 형식 {#format}

다음 표는 NTCP에서 사용하는 기존의 16바이트 헤더를 명시합니다. SSU 및 NTCP2 전송 방식은 수정된 헤더를 사용합니다.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Bytes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Type</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unique ID</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expiration</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Payload Length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Checksum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Payload</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 - 61.2KB</td>
</tr>
</table>
최대 페이로드 크기는 명목상 64KB이지만, [터널 구현 페이지](/docs/specs/tunnel-implementation/)에 설명된 대로 I2NP 메시지를 여러 개의 1KB 터널 메시지로 분할하는 방식에 의해 실제 크기가 추가로 제한된다.

최대 조각 수는 64개이며, 메시지가 완벽하게 정렬되지 않을 수 있으므로 메시지는 명목상 63개의 조각 안에 들어가야 합니다.

초기 조각의 최대 크기는 956바이트(TUNNEL 전달 모드 가정 시)이며, 후속 조각의 최대 크기는 996바이트입니다. 따라서 최대 크기는 약 956 + (62 × 996) = 62708바이트, 즉 61.2KB입니다.

또한 전송 방식마다 추가적인 제한이 있을 수 있습니다. NTCP의 제한은 16KB - 6 = 16378바이트입니다. SSU의 제한은 약 32KB 정도이며, NTCP2의 제한은 약 64KB - 20 = 65516바이트로, 터널이 지원할 수 있는 크기보다 더 큽니다.

클라이언트가 보는 데이터그램의 한계치는 아님에 유의하세요. 라우터는 클라이언트 메시지와 함께 응답용 leaseSet 및/또는 세션 태그를 마늘(garlic) 메시지 안에 묶어 전송할 수 있기 때문입니다. leaseSet과 태그는 함께 약 5.5KB 정도를 추가할 수 있습니다. 따라서 현재 데이터그램 한계치는 약 10KB 정도입니다. 이 한계치는 향후 릴리스에서 증가될 예정입니다.

## 메시지 유형 {#types}

번호가 높은 우선순위일수록 더 높은 우선순위를 가진다. 대부분의 트래픽은 TunnelDataMessage(우선순위 400)이므로, 400보다 높은 값은 본질적으로 높은 우선순위이며, 400보다 낮은 값은 낮은 우선순위이다. 또한 많은 메시지들이 클라이언트 튜널이 아닌 탐사용 튜널(exploratory tunnel)을 통해 일반적으로 라우팅되므로, 첫 번째 홉(first hop)이 운 좋게 동일한 피어에 있지 않는 한 동일한 큐에 있지 않을 수 있다는 점에도 유의해야 한다.

또한 모든 메시지 유형이 암호화되지 않은 상태로 전송되는 것은 아닙니다. 예를 들어 터널을 테스트할 때, 라우터는 DeliveryStatusMessage를 감싸고, 이는 다시 GarlicMessage에 감싸지며, 최종적으로 DataMessage에 감싸집니다.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Length</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Priority</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Comments</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookupMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">May vary</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseSearchReplyMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">Typ. 161</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Size is 65 + 32*(number of hashes) where typically, the hashes for three floodfill routers are returned.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseStoreMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">Varies</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">460</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority may vary. Size is 898 bytes for a typical 2-lease leaseSet. RouterInfo structures are compressed, and size varies; however there is a continuing effort to reduce the amount of data published in a RouterInfo.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DataMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4 - 62080</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">425</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority may vary on a per-destination basis</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DeliveryStatusMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Used for message replies, and for testing tunnels - generally wrapped in a GarlicMessage</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/overview/garlic-routing/">GarlicMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generally wrapped in a DataMessage - but when unwrapped, given a priority of 100 by the forwarding router</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/specs/tunnel-creation/">TunnelBuildMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4224</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/specs/tunnel-creation/">TunnelBuildReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4224</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">TunnelDataMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1028</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">400</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The most common message. Priority for tunnel participants, outbound endpoints, and inbound gateways was reduced to 200 as of release 0.6.1.33. Outbound gateway messages (i.e. those originated locally) remains at 400.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">TunnelGatewayMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300/400</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">VariableTunnelBuildMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1057 - 4225</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Shorter TunnelBuildMessage as of 0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">VariableTunnelBuildReplyMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1057 - 4225</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Shorter TunnelBuildReplyMessage as of 0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Others (Types 0, 4-9, 12)</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">0, 4-9, 12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Obsolete, Unused</td>
</tr>
</table>
## 터널 테스트

API 버전 0.9.68 2026-02부터 터널 테스트가 필수입니다. 라우터는 처음 두 분 동안 트래픽을 수신하지 않은 참여 터널을 삭제할 수 있습니다.

## 완전한 프로토콜 사양

전체 프로토콜 사양은 [I2NP 사양 페이지](/docs/specs/i2np/)를 참조하세요. 또한 [공용 데이터 구조 사양 페이지](/docs/specs/common-structures/)도 함께 참조하세요.

## 향후 작업

현재의 우선순위 체계가 일반적으로 효과적인지 여부와 다양한 메시지의 우선순위를 추가로 조정해야 할지 여부는 명확하지 않습니다. 이는 추가 연구, 분석 및 테스트가 필요한 주제입니다.
