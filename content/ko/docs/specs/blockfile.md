---
title: "Blockfile 및 호스트 데이터베이스 사양"
description: "Blockfile Naming Service에서 사용되는 I2P blockfile 파일 형식과 hostsdb.blockfile의 테이블에 대한 사양"
slug: "blockfile"
aliases:
  - "/ko/blockfile"
  - "/ko/blockfile/"
category: "형식"
lastUpdated: "2023-11"
accurateFor: "0.9.59"
---

## 개요

이 문서는 I2P blockfile 파일 형식과 Blockfile Naming Service [NAMING](/docs/overview/naming/)에서 사용하는 hostsdb.blockfile의 테이블들을 명세합니다.

blockfile은 컴팩트한 형식으로 빠른 Destination 조회를 제공합니다. blockfile 페이지 오버헤드가 상당하지만, destination들은 hosts.txt 형식의 Base 64가 아닌 바이너리로 저장됩니다. 또한 blockfile은 각 항목에 대해 임의의 메타데이터 저장(추가 날짜, 소스, 코멘트 등) 기능을 제공합니다. 메타데이터는 향후 고급 주소록 기능을 제공하는 데 사용될 수 있습니다. blockfile 저장 요구사항은 hosts.txt 형식에 비해 약간 증가하지만, blockfile은 조회 시간을 약 10배 단축시킵니다.

blockfile은 단순히 정렬된 여러 맵(키-값 쌍)을 디스크에 저장하는 것으로, skiplist로 구현됩니다. blockfile 형식은 Metanotion Blockfile Database [METANOTION](http://www.metanotion.net/software/sandbox/block.html)에서 채택되었습니다. 먼저 파일 형식을 정의한 다음, BlockfileNamingService에서 해당 형식을 사용하는 방법을 설명하겠습니다.

## 블록파일 형식

원래의 blockfile 스펙은 각 페이지에 매직 넘버를 추가하도록 수정되었습니다. 파일은 1024바이트 페이지로 구조화됩니다. 페이지는 1부터 시작하여 번호가 매겨집니다. "superblock"은 항상 페이지 1에 위치하며, 즉 파일의 바이트 0부터 시작합니다. metaindex skiplist는 항상 페이지 2에 위치하며, 즉 파일의 바이트 1024부터 시작합니다.

모든 2바이트 정수 값은 부호 없는 정수입니다. 모든 4바이트 정수 값(페이지 번호)은 부호 있는 정수이며 음수 값은 허용되지 않습니다. 모든 정수 값은 네트워크 바이트 순서(빅 엔디안)로 저장됩니다.

데이터베이스는 단일 스레드에서 열리고 접근되도록 설계되었습니다. BlockfileNamingService가 동기화를 제공합니다.

### Superblock 형식

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x3141de493250 ("1A" 0xde "I2P")</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Major version</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x01</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Minor version</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x02</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">File length</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total length in bytes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First free list page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">20-21</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Mounted flag</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x01 = yes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">22-23</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Span size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Max number of key/value pairs per span (16 for hostsdb). Used for new skip lists.</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Page size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">As of version 1.2. Prior to 1.2, 1024 is assumed.</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">28-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### Skip list 블록 페이지 형식

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x536b69704c697374 "SkipList"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First level page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total number of keys - may only be valid at startup</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">20-23</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Spans</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total number of spans - may only be valid at startup</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Levels</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total number of levels - may only be valid at startup</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">28-29</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Span size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">As of version 1.2. Max number of key/value pairs per span. Prior to that, specified for all skiplists in the superblock. Used for new spans in this skip list.</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">30-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### 건너뛰기 레벨 블록 페이지 형식

모든 레벨은 스팬을 가집니다. 모든 스팬이 레벨을 가지는 것은 아닙니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x42534c6576656c73 "BSLevels"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Max height</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Current height</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next level pages</td><td style="border:1px solid var(--color-border); padding:0.6rem;">'current height' entries, 4 bytes each, lowest first</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">remaining</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### 스팬 블록 페이지 형식 건너뛰기

키/값 구조는 각 스팬 내에서 그리고 모든 스팬에 걸쳐 키를 기준으로 정렬됩니다. 키/값 구조는 각 스팬 내에서 키를 기준으로 정렬됩니다. 첫 번째 스팬이 아닌 다른 스팬들은 비어있을 수 없습니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x5370616e "Span"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First continuation page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Previous span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-17</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Max keys</td><td style="border:1px solid var(--color-border); padding:0.6rem;">16 for hostsdb</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">18-19</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Current number of keys</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">20-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key/value structures</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### Span Continuation 블록 페이지 형식

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x434f4e54 "CONT"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next continuation page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key/value structures</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### 키/값 구조 형식

키와 값의 길이는 페이지를 넘나들어 분할되어서는 안 됩니다. 즉, 4바이트 모두가 동일한 페이지에 있어야 합니다. 공간이 충분하지 않으면 페이지의 마지막 1-3바이트는 사용되지 않고, 길이는 연속 페이지의 오프셋 8에 위치하게 됩니다. 키와 값 데이터는 페이지를 넘나들어 분할될 수 있습니다. 최대 키와 값 길이는 65535바이트입니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key length in bytes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">2-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">value length in bytes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key data</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;"></td><td style="border:1px solid var(--color-border); padding:0.6rem;">value data</td></tr>
</tbody>
</table>
### 프리 리스트 블록 페이지 형식

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x2366724c69737423 "#frList#"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next free list block</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0 if none</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Number of valid free pages</td><td style="border:1px solid var(--color-border); padding:0.6rem;">in this block (0 - 252)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Free pages</td><td style="border:1px solid var(--color-border); padding:0.6rem;">4 bytes each, only the first (valid number) are valid</td></tr>
</tbody>
</table>
### 프리 페이지 블록 형식

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x7e2146524545217e "~!FREE!~"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
메타인덱스(페이지 2에 위치)는 US-ASCII 문자열을 4바이트 정수에 매핑하는 것입니다. 키는 skiplist의 이름이고 값은 skiplist의 페이지 인덱스입니다.

## Blockfile 네이밍 서비스 테이블

BlockfileNamingService에서 생성되고 사용되는 테이블은 다음과 같습니다. 스팬당 최대 항목 수는 16개입니다.

### 속성 스킵리스트

`%%__INFO__%%`는 하나의 항목만 포함하는 String/Properties 키/값 항목들이 있는 주요 데이터베이스 skiplist입니다:

**info** - Properties (UTF-8 문자열/문자열 맵), [매핑](/docs/specs/common-structures/#type-mapping)으로 직렬화됨:

- **version** - "4"
- **created** - Java long 시간 (ms)
- **upgraded** - Java long 시간 (ms) (데이터베이스 버전 2부터)
- **lists** - 조회 시 순서대로 검색할 호스트 데이터베이스의 쉼표로 구분된 목록. 거의 항상 "privatehosts.txt,userhosts.txt,hosts.txt"입니다.
- **listversion_*** - lists에 있는 각 데이터베이스의 버전, 예: listversion_hosts.txt=4. 개별 목록의 부분적이거나 중단된 업그레이드를 식별하는 데 사용됩니다. (데이터베이스 버전 4부터)

### 역방향 조회 스킵리스트

`%%__REVERSE__%%`는 정수/속성 키/값 항목을 가진 역방향 조회 skiplist입니다 (데이터베이스 버전 2 기준):

- skiplist 키는 4바이트 정수로, [Destination](/docs/specs/common-structures/#struct-destination)의 해시 중 첫 4바이트입니다.
- skiplist 값은 각각 [Mapping](/docs/specs/common-structures/#type-mapping)으로 직렬화된 Properties(UTF-8 문자열/문자열 맵)입니다
  - properties에는 여러 항목이 있을 수 있으며, 각각은 역방향 매핑입니다. 주어진 destination에 대해 두 개 이상의 호스트명이 있을 수 있거나, 해시의 동일한 첫 4바이트로 인한 충돌이 있을 수 있기 때문입니다.
  - 각 property 키는 호스트명입니다.
  - 각 property 값은 빈 문자열입니다.

### hosts.txt, userhosts.txt, 그리고 privatehosts.txt 건너뛰기 목록

각 호스트 데이터베이스에 대해 해당 데이터베이스의 호스트들을 포함하는 skiplist가 있습니다. 버전 4 형식은 호스트명당 여러 Destination을 지원한다는 점에 주목하세요. 이 형식은 I2P 릴리스 0.9.26에서 도입되었습니다. 버전 3 데이터베이스는 자동으로 버전 4로 마이그레이션됩니다.

이러한 skiplist의 키/값은 다음과 같습니다:

**key** - UTF-8 문자열 (호스트명)

**value** - - 데이터베이스 버전 4: DestEntry로, 뒤따를 Properties/Destination 쌍의 개수를 나타내는 1바이트 숫자입니다. 그 개수만큼의 쌍들: [Mapping](/docs/specs/common-structures/#type-mapping)으로 직렬화된 Properties (UTF-8 문자열/문자열 맵)와 그 뒤에 바이너리 [Destination](/docs/specs/common-structures/#struct-destination) (일반적인 방식으로 직렬화됨). - 데이터베이스 버전 3: DestEntry로, [Mapping](/docs/specs/common-structures/#type-mapping)으로 직렬화된 Properties (UTF-8 문자열/문자열 맵)와 그 뒤에 바이너리 [Destination](/docs/specs/common-structures/#struct-destination) (일반적인 방식으로 직렬화됨).

DestEntry Properties는 일반적으로 다음을 포함합니다:

- **"a"** - 추가된 시간 (Java long time in ms)
- **"m"** - 마지막 수정 시간 (Java long time in ms)
- **"notes"** - 사용자 제공 주석
- **"s"** - 항목의 원본 소스 (일반적으로 파일명 또는 구독 URL)
- **"v"** - 항목의 서명이 검증된 경우, "true" 또는 "false"

호스트명 키는 소문자로 저장되며 항상 ".i2p"로 끝납니다.

## 참고 문헌

- [Destination](/docs/specs/common-structures/#struct-destination)
- [Mapping](/docs/specs/common-structures/#type-mapping)
- [METANOTION](http://www.metanotion.net/software/sandbox/block.html)
- [NAMING](/docs/overview/naming/)
