---
title: "소프트웨어 업데이트 사양"
description: "I2P 소프트웨어 업데이트 메커니즘, SU3 파일 형식 및 뉴스 피드 사양"
slug: "updates"
aliases:
  - "/ko/updates"
  - "/ko/updates/"
category: "설계"
lastUpdated: "2025-04"
accurateFor: "0.9.65"
---

## 개요

I2P는 자동화된 소프트웨어 업데이트를 위해 간단하면서도 안전한 시스템을 사용합니다. router 콘솔은 설정 가능한 I2P URL에서 뉴스 파일을 주기적으로 가져옵니다. 기본 프로젝트 뉴스 호스트가 다운될 경우를 대비해 프로젝트 웹사이트를 가리키는 하드코딩된 백업 URL이 있습니다.

뉴스 파일의 내용은 router 콘솔의 홈 페이지에 표시됩니다. 또한 뉴스 파일에는 소프트웨어의 최신 버전 번호가 포함되어 있습니다. 버전이 router의 버전 번호보다 높으면 사용자에게 업데이트가 가능하다는 표시를 보여줍니다.

router는 설정에 따라 선택적으로 새 버전을 다운로드하거나 다운로드 및 설치할 수 있습니다.

## 구 뉴스 파일 규격

이 형식은 릴리스 0.9.17부터 su3 뉴스 형식으로 대체되었습니다.

news.xml 파일에는 다음 요소들이 포함될 수 있습니다:

```
<i2p.news date="$Date: 2010-01-22 00:00:00 $" />
<i2p.release version="0.7.14" date="2010/01/22" minVersion="0.6" />
```
i2p.release 항목의 매개변수는 다음과 같습니다. 모든 키는 대소문자를 구분하지 않습니다. 모든 값은 큰따옴표로 묶어야 합니다.

**date** : router 버전의 릴리스 날짜입니다. 사용되지 않습니다. 형식이 지정되지 않았습니다.

**minJavaVersion** : 현재 버전을 실행하는 데 필요한 Java의 최소 버전입니다. 릴리스 0.9.9 기준입니다.

**minVersion** : 현재 버전으로 업데이트하는 데 필요한 router의 최소 버전입니다. router가 이보다 오래된 경우, 사용자는 먼저 중간 버전으로 (수동으로?) 업데이트해야 합니다. 릴리스 0.9.9 기준입니다.

**su3Clearnet** : .su3 업데이트 파일을 clearnet(비I2P 네트워크)에서 찾을 수 있는 하나 이상의 HTTP URL. 여러 URL은 공백이나 쉼표로 구분해야 함. 릴리스 0.9.9부터 제공.

**su3SSL** : .su3 업데이트 파일을 클리어넷(non-I2P)에서 찾을 수 있는 하나 이상의 HTTPS URL. 여러 URL은 공백이나 쉼표로 구분해야 합니다. 릴리스 0.9.9부터 적용됩니다.

**sudTorrent** : 업데이트의 .sud (non-pack200) torrent에 대한 magnet 링크입니다. 릴리스 0.9.4부터 제공됩니다.

**su2Torrent** : 업데이트의 .su2 (pack200) torrent에 대한 마그넷 링크입니다. 릴리스 0.9.4부터 제공됩니다.

**su3Torrent** : 업데이트의 .su3 (새 형식) torrent에 대한 마그넷 링크입니다. 릴리스 0.9.9부터 제공됩니다.

**version** : 필수. 사용 가능한 최신 현재 router 버전.

요소들은 브라우저에 의한 해석을 방지하기 위해 XML 주석 내부에 포함될 수 있습니다. i2p.release 요소와 버전은 필수입니다. 다른 모든 요소들은 선택사항입니다. 참고: 파서 제한으로 인해 전체 요소는 한 줄에 있어야 합니다.

## 업데이트 파일 명세

릴리스 0.9.9부터 i2pupdate.su3라는 이름의 서명된 업데이트 파일은 아래에 명시된 "su3" 파일 형식을 사용합니다. 승인된 릴리스 서명자는 4096비트 RSA 키를 사용합니다. 이러한 서명자들의 X.509 공개 키 인증서는 router 설치 패키지에 포함되어 배포됩니다. 업데이트에는 새로 승인된 서명자를 위한 인증서가 포함될 수 있으며, 폐기를 위해 삭제할 인증서 목록이 포함될 수도 있습니다.

## 구 업데이트 파일 사양

이 형식은 릴리스 0.9.9부터 더 이상 사용되지 않습니다.

서명된 업데이트 파일은 일반적으로 i2pupdate.sud라는 이름을 가지며, 단순히 56바이트 헤더가 앞에 붙은 zip 파일입니다. 헤더에는 다음이 포함됩니다:

- 40바이트 DSA [서명](/docs/specs/common-structures#signature)
- UTF-8로 인코딩된 16바이트 I2P 버전, 필요시 뒤쪽을 0으로 패딩

서명은 zip 아카이브만을 대상으로 하며 - 앞에 추가된 버전은 포함하지 않습니다. 서명은 router에 구성된 DSA [SigningPublicKey](/docs/specs/common-structures#signingpublickey) 중 하나와 일치해야 하며, 이는 현재 프로젝트 릴리스 관리자들의 키 목록이 하드코딩된 기본값으로 설정되어 있습니다.

버전 비교를 위해, 버전 필드는 [0-9]*를 포함하고, 필드 구분자는 '-', '_', '.'이며, 다른 모든 문자는 무시됩니다.

버전 0.8.8부터는 버전을 UTF-8로 된 zip 파일 주석으로도 지정해야 하며, 후행 0은 포함하지 않습니다. 업데이트하는 router는 헤더의 버전(서명으로 보호되지 않음)이 zip 파일 주석의 버전(서명으로 보호됨)과 일치하는지 확인합니다. 이는 헤더의 버전 번호 스푸핑을 방지합니다.

## 다운로드 및 설치

router는 먼저 설정 가능한 I2P URL 목록 중 하나에서 내장 HTTP 클라이언트와 프록시를 사용하여 업데이트 파일의 헤더를 다운로드하고, 버전이 더 새로운지 확인합니다. 이는 최신 파일을 가지지 않은 업데이트 호스트의 문제를 방지합니다. 그런 다음 router는 전체 업데이트 파일을 다운로드합니다. router는 설치 전에 업데이트 파일 버전이 더 새로운지 확인합니다. 또한 당연히 서명을 검증하고, 위에서 설명한 바와 같이 zip 파일 주석이 헤더 버전과 일치하는지 확인합니다.

zip 파일은 압축 해제되어 I2P 설정 디렉토리(Linux에서는 ~/.i2p)의 "i2pupdate.zip"으로 복사됩니다.

릴리스 0.7.12부터 router는 Pack200 압축 해제를 지원합니다. zip 아카이브 내에서 .jar.pack 또는 .war.pack 접미사를 가진 파일들은 투명하게 .jar 또는 .war 파일로 압축 해제됩니다. .pack 파일을 포함하는 업데이트 파일들은 전통적으로 '.su2' 접미사로 명명됩니다. Pack200은 업데이트 파일 크기를 약 60% 줄여줍니다.

릴리스 0.8.7부터, zip 아카이브에 lib/jbigi.jar 파일이 포함되어 있으면 router는 libjbigi.so와 libjcpuid.so 파일을 삭제하여 새로운 파일들이 jbigi.jar에서 추출되도록 합니다.

릴리스 0.8.12부터, zip 아카이브에 deletelist.txt 파일이 포함되어 있으면 router가 그곳에 나열된 파일들을 삭제합니다. 형식은 다음과 같습니다:

- 한 줄에 하나의 파일 이름
- 모든 파일 이름은 설치 디렉토리에 상대적이며, 절대 파일 이름은 허용되지 않고 ".."로 시작하는 파일도 허용되지 않음
- 주석은 '#'으로 시작

그러면 router가 deletelist.txt 파일을 삭제합니다.

## SU3 파일 사양

이 명세는 릴리스 0.9.9부터 router 업데이트에, 릴리스 0.9.14부터 reseed 데이터에, 릴리스 0.9.15부터 플러그인에, 릴리스 0.9.17부터 뉴스 파일에 사용됩니다.

### 이전 .sud/.su2 형식의 문제점

- 매직 넘버나 플래그 없음
- 압축, pack200 여부, 서명 알고리즘을 지정할 방법 없음
- 버전이 서명으로 보호되지 않으므로, zip 파일 주석(router 파일의 경우) 또는 plugin.config 파일(플러그인의 경우)에 포함하도록 요구하여 강제함
- 서명자가 지정되지 않아 검증자가 알려진 모든 키를 시도해야 함
- 서명-데이터 순서 형식으로 인해 파일 생성 시 두 번의 패스가 필요함

### 목표

- 위 문제들 수정
- 더 안전한 서명 알고리즘으로 마이그레이션
- 기존 버전 체커와의 호환성을 위해 동일한 형식과 오프셋으로 버전 정보 유지
- 원패스 서명 검증 및 파일 추출

### 명세서

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number "I2Psu3"</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">su3 file format version = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature type: 0x0000 = DSA-SHA1, 0x0001 = ECDSA-SHA256-P256, 0x0002 = ECDSA-SHA384-P384, 0x0003 = ECDSA-SHA512-P521, 0x0004 = RSA-SHA256-2048, 0x0005 = RSA-SHA384-3072, 0x0006 = RSA-SHA512-4096, 0x0008 = EdDSA-SHA512-Ed25519ph</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature length, e.g. 40 (0x0028) for DSA-SHA1. Must match that specified for the <a href="/docs/specs/common-structures#signature">Signature</a> type.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version length (in bytes not chars, including padding), must be at least 16 (0x10) for compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID length (in bytes not chars)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content length (not including header or sig)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File type: 0x00 = zip file, 0x01 = xml file (0.9.15), 0x02 = html file (0.9.17), 0x03 = xml.gz file (0.9.17), 0x04 = txt.gz file (0.9.28), 0x05 = dmg file (0.9.51), 0x06 = exe file (0.9.51)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content type: 0x00 = unknown, 0x01 = router update, 0x02 = plugin or plugin update, 0x03 = reseed data, 0x04 = news feed (0.9.15), 0x05 = blocklist feed (0.9.28)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40-55+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version, UTF-8 padded with trailing 0x00, 16 bytes minimum, length specified at byte 13. Do not append 0x00 bytes if the length is 16 or more.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ID of signer, (e.g. "zzz@mail.i2p") UTF-8, not padded, length specified at byte 15</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content: Length specified in header at bytes 16-23, Format specified in header at byte 25, Content specified in header at byte 27</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature: Length is specified in header at bytes 10-11, covers everything starting at byte 0</td>
    </tr>
  </tbody>
</table>
사용하지 않는 모든 필드는 향후 버전과의 호환성을 위해 0으로 설정해야 합니다.

### 서명 세부사항

서명은 바이트 0에서 시작하여 콘텐츠 끝까지 전체 헤더를 포함합니다. 우리는 원시 서명(raw signature)을 사용합니다. 데이터의 해시를 구한 다음(바이트 8-9의 서명 타입에 의해 암시되는 해시 타입 사용), 이를 "원시" 서명 또는 검증 함수에 전달합니다(예: Java의 "NONEwithRSA").

서명 검증과 콘텐츠 추출이 한 번의 과정으로 구현될 수 있지만, 구현체는 검증을 시작하기 전에 해시 유형을 결정하기 위해 첫 10바이트를 읽고 버퍼링해야 합니다.

다양한 서명 타입에 대한 서명 길이는 [Signature](/docs/specs/common-structures#signature) 명세에 제시되어 있습니다. 필요한 경우 서명 앞에 0을 채워 넣으십시오. 다양한 서명 타입의 매개변수에 대해서는 [암호화 세부사항 페이지](/docs/specs/cryptography#sig)를 참조하십시오.

### 참고사항

콘텐츠 유형은 신뢰 도메인을 지정합니다. 각 콘텐츠 유형에 대해, 클라이언트는 해당 콘텐츠에 서명할 권한이 있는 신뢰할 수 있는 당사자들의 X.509 공개 키 인증서 세트를 유지관리합니다. 지정된 콘텐츠 유형에 대한 인증서만 사용할 수 있습니다. 인증서는 서명자의 ID로 조회됩니다. 클라이언트는 콘텐츠 유형이 애플리케이션에서 예상하는 것과 일치하는지 확인해야 합니다.

모든 값은 네트워크 바이트 순서(빅 엔디언)로 되어 있습니다.

Java "NONEwithRSA"와 호환되는 Raw RSA 서명의 파이썬 구현에 대해서는 [이 Stack Overflow 글](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530)을 참조하세요.

## SU3 Router 업데이트 파일 명세서

### SU3 세부사항

- SU3 Content Type: 1 (ROUTER UPDATE)
- SU3 File Type: 0 (ZIP)
- SU3 Version: router 버전

zip 파일 내의 Jar와 war 파일들은 더 이상 위에서 "su2" 파일에 대해 설명한 것처럼 pack200으로 압축되지 않습니다. 최근 Java 런타임에서 더 이상 이를 지원하지 않기 때문입니다.

### 참고사항

- 릴리스의 경우, SU3 버전은 "기본" router 버전입니다. 예: "0.9.20".
- 0.9.20 릴리스부터 지원되는 개발 빌드의 경우, SU3 버전은 "전체" router 버전입니다. 예: "0.9.20-5" 또는 "0.9.20-5-rc". [I2P 소스](https://github.com/i2p/i2p.i2p)의 RouterVersion.java를 참조하세요.

## SU3 Reseed 파일 사양

0.9.14 버전부터 reseed 데이터는 "su3" 파일 형식으로 전달됩니다.

### 목표

- 중간자 공격을 방지하기 위해 강력한 서명과 신뢰할 수 있는 인증서로 서명된 파일을 사용하여, 피해자가 별도의 신뢰할 수 없는 네트워크로 부팅되는 것을 방지합니다.
- 업데이트와 플러그인에 이미 사용되고 있는 su3 파일 형식 사용
- 200개 파일을 가져오는 것이 느렸던 리시딩 속도를 높이기 위해 단일 압축 파일 사용

### 사양

1. 파일 이름은 "i2pseeds.su3"이어야 합니다. 0.9.42부터 요청자는 현재 네트워크 ID가 2라고 가정하여 요청 URL에 쿼리 문자열 "?netid=2"를 추가해야 합니다. 이는 교차 네트워크 연결을 방지하는 데 사용될 수 있습니다. 테스트 네트워크는 다른 네트워크 ID를 설정해야 합니다. 자세한 내용은 제안서 147을 참조하세요.
2. 파일은 웹 서버의 router 정보와 같은 디렉토리에 있어야 합니다.
3. router는 먼저 (인덱스 URL)/i2pseeds.su3를 가져오려고 시도합니다. 실패하면 인덱스 URL을 가져온 다음 링크에서 찾은 개별 router 정보 파일을 가져옵니다.

### SU3 세부사항

- SU3 Content Type: 3 (RESEED)
- SU3 File Type: 0 (ZIP)
- SU3 Version: 에포크 이후의 초 단위 시간, ASCII 형식 (date +%s). 2038년 또는 2106년에 롤오버되지 않음.
- zip 파일 내의 router 정보 파일들은 "최상위 레벨"에 있어야 함. zip 파일에는 디렉토리가 포함되지 않음.
- Router 정보 파일들은 기존 reseed 메커니즘에서처럼 "routerInfo-(44자리 base 64 router hash).dat" 형식으로 명명되어야 함. I2P base 64 알파벳을 사용해야 함.

### 참고 사항

- 경고: 여러 reseed가 IPv6를 통해 응답하지 않는 것으로 알려져 있습니다. IPv4를 강제하거나 우선하는 것을 권장합니다.
- 경고: 일부 reseed는 자체 서명된 CA 인증서를 사용합니다. 구현체는 reseed할 때 이러한 CA를 가져와서 신뢰하거나, reseed 목록에서 자체 서명된 reseed를 제외해야 합니다.
- Reseed 서명자 키는 RSA-4096 키를 가진 자체 서명된 X.509 인증서(서명 유형 6)로 구현체에 배포됩니다. 구현체는 인증서의 유효 날짜를 강제해야 합니다.

## SU3 플러그인 파일 사양

0.9.15부터 플러그인은 "su3" 파일 형식으로 패키징될 수 있습니다.

### SU3 세부사항

- SU3 콘텐츠 유형: 2 (PLUGIN)
- SU3 파일 유형: 0 (ZIP) - 자세한 내용은 [플러그인 사양](/docs/specs/plugin)을 참조하세요.
- SU3 버전: 플러그인 버전으로, plugin.config의 버전과 일치해야 합니다.

zip 파일 내의 Jar 및 war 파일은 위에서 "su2" 파일에 대해 문서화된 것처럼 pack200으로 압축하면 안 됩니다. 최신 Java 런타임에서 더 이상 지원하지 않기 때문입니다.

## SU3 뉴스 파일 명세

0.9.17부터 뉴스는 "su3" 파일 형식으로 전달됩니다.

### 목표

- 강력한 서명과 신뢰할 수 있는 인증서로 서명된 뉴스
- 업데이트, 리시딩 및 플러그인에 이미 사용되는 su3 파일 형식 사용
- 표준 파서와 함께 사용하기 위한 표준 XML 형식
- 표준 피드 리더 및 생성기와 함께 사용하기 위한 표준 Atom 형식
- 콘솔에 표시하기 전 HTML의 무결성 검사 및 검증
- HTML 콘솔이 없는 Android 및 기타 플랫폼에서 쉬운 구현에 적합

### SU3 세부사항

- SU3 Content Type: 4 (NEWS)
- SU3 File Type: 1 (XML) 또는 3 (XML.GZ)
- SU3 Version: epoch 이후의 초 단위 시간, ASCII 형식 (date +%s). 2038년이나 2106년에 롤오버되지 않음.
- File Format: [RFC 4287](https://tools.ietf.org/html/rfc4287) (Atom) XML 피드를 포함하는 XML 또는 gzip 압축된 XML. 문자셋은 UTF-8이어야 함.

### Atom Feed 세부사항

다음 `<feed>` 요소들이 사용됩니다:

**`<entry>`** : 뉴스 항목입니다. 아래를 참조하세요.

**`<i2p:release>`** : I2P 업데이트 메타데이터. 아래를 참조하세요.

**`<i2p:revocations>`** : 인증서 폐기. 아래를 참조하세요.

**`<i2p:blocklist>`** : 차단 목록 데이터. 아래를 참조하세요.

**`<updated>`** : 필수. 피드의 타임스탬프 ([RFC 4287](https://tools.ietf.org/html/rfc4287) 섹션 3.3 및 [RFC 3339](https://tools.ietf.org/html/rfc3339)를 준수).

### Atom 엔트리 세부사항

뉴스 피드의 각 Atom `<entry>`는 router 콘솔에서 파싱되어 표시될 수 있습니다. 다음 요소들이 사용됩니다:

**`<author>`** : 선택사항. `<name>`을 포함 - 항목 작성자의 이름.

**`<content>`** : 필수. 콘텐츠, type="xhtml"이어야 함. XHTML은 허용된 요소의 화이트리스트와 허용되지 않는 속성의 블랙리스트로 정화됩니다. 클라이언트는 화이트리스트에 없는 요소가 발견될 때 해당 요소나 포함하는 항목, 또는 전체 피드를 무시할 수 있습니다.

**`<link>`** : 선택사항. 추가 정보를 위한 링크.

**`<summary>`** : 선택사항. 툴팁에 적합한 간단한 요약.

**`<title>`** : 필수. 뉴스 항목의 제목.

**`<updated>`** : 필수. 이 항목의 타임스탬프 ([RFC 4287](https://tools.ietf.org/html/rfc4287) 섹션 3.3 및 [RFC 3339](https://tools.ietf.org/html/rfc3339)를 준수).

### Atom i2p:release 세부 정보

피드에는 최소한 하나의 `<i2p:release>` 엔터티가 있어야 합니다. 각각은 다음과 같은 속성과 엔터티를 포함합니다:

**date (속성)** : 필수. 이 항목의 타임스탬프 ([RFC 4287](https://tools.ietf.org/html/rfc4287) 섹션 3.3 및 [RFC 3339](https://tools.ietf.org/html/rfc3339)를 준수). 날짜는 또한 잘린 형식 yyyy-mm-dd ('T' 없이)일 수도 있습니다. 이는 RFC 3339의 "full-date" 형식입니다. 이 형식에서는 모든 처리에서 시간이 00:00:00 UTC로 가정됩니다.

**minJavaVersion (속성)** : 존재하는 경우, 현재 버전을 실행하는 데 필요한 최소 Java 버전입니다.

**minVersion (속성)** : 존재하는 경우, 현재 버전으로 업데이트하기 위해 필요한 router의 최소 버전입니다. router가 이보다 오래된 경우, 사용자는 먼저 중간 버전으로 (수동으로?) 업데이트해야 합니다.

**`<i2p:version>`** : 필수. 사용 가능한 최신 현재 router 버전.

**`<i2p:update>`** : 업데이트 파일 (하나 이상). 최소한 하나의 하위 요소를 포함해야 합니다.   - type (속성): "sud", "su2", 또는 "su3". 모든 `<i2p:update>` 요소들 간에 고유해야 합니다.   - `<i2p:clearnet>`: 네트워크 외부 직접 다운로드 링크 (0개 이상). href (속성): 표준 clearnet http 링크.   - `<i2p:clearnetssl>`: 네트워크 외부 직접 다운로드 링크 (0개 이상). href (속성): 표준 clearnet https 링크.   - `<i2p:torrent>`: 네트워크 내 magnet 링크. href (속성): magnet 링크.   - `<i2p:url>`: 네트워크 내 직접 다운로드 링크 (0개 이상). href (속성): 네트워크 내 http .i2p 링크.

### Atom i2p:revocations 세부 정보

이 엔티티는 선택사항이며 피드에는 최대 하나의 `<i2p:revocations>` 엔티티가 있습니다. 이 기능은 릴리스 0.9.26부터 지원됩니다.

`<i2p:revocations>` 엔티티는 하나 이상의 `<i2p:crl>` 엔티티를 포함합니다. `<i2p:crl>` 엔티티는 다음 속성들을 포함합니다:

**updated (속성)** : 필수. 이 항목의 타임스탬프 ([RFC 4287](https://tools.ietf.org/html/rfc4287) 섹션 3.3 및 [RFC 3339](https://tools.ietf.org/html/rfc3339)를 준수). 날짜는 yyyy-mm-dd의 단축된 형식으로도 사용할 수 있습니다('T' 제외); 이는 RFC 3339의 "full-date" 형식입니다. 이 형식에서는 모든 처리에서 시간이 00:00:00 UTC로 간주됩니다.

**id (속성)** : 필수. 이 CRL의 생성자에 대한 고유 id.

**(엔티티 콘텐츠)** : 필수. 줄바꿈이 포함된 표준 base 64 인코딩된 Certificate Revocation List (CRL)로, '-----BEGIN X509 CRL-----' 줄로 시작하고 '-----END X509 CRL-----' 줄로 끝납니다. CRL에 대한 자세한 정보는 [RFC 5280](https://tools.ietf.org/html/rfc5280)을 참조하세요.

### Atom i2p:blocklist 세부사항

이 엔터티는 선택사항이며 피드에는 최대 하나의 `<i2p:blocklist>` 엔터티가 있습니다. 이 기능은 릴리스 0.9.28에서 구현될 예정입니다.

`<i2p:blocklist>` 엔티티는 하나 이상의 `<i2p:block>` 또는 `<i2p:unblock>` 엔티티, "updated" 엔티티, 그리고 "signer"와 "sig" 속성을 포함합니다:

**signer (속성)** : 필수. 이 차단 목록에 서명하는 데 사용된 공개 키의 고유 ID (UTF-8).

**sig (속성)** : 필수. code:b64sig 형식의 서명으로, 여기서 code는 ASCII 서명 유형 번호이고, b64sig는 base 64로 인코딩된 서명입니다 (I2P alphabet). 서명할 데이터의 사양은 아래를 참조하세요.

**`<updated>`** : 필수. blocklist의 타임스탬프 ([RFC 4287](https://tools.ietf.org/html/rfc4287) 섹션 3.3 및 [RFC 3339](https://tools.ietf.org/html/rfc3339)를 준수). 날짜는 또한 잘린 형식 yyyy-mm-dd ('T' 없이)로 표시될 수도 있으며, 이는 RFC 3339의 "full-date" 형식입니다. 이 형식에서는 모든 처리에서 시간이 00:00:00 UTC로 간주됩니다.

**`<i2p:block>`** : 선택사항이며, 여러 엔티티가 허용됩니다. 단일 항목으로, 리터럴 IPv4 또는 IPv6 주소이거나, 44자리 base 64 router 해시(I2P 알파벳)입니다. IPv6 주소는 축약된 형식("::"을 포함)으로 표현될 수 있습니다. 넷마스크가 포함된 항목(예: x.y.0.0/16)에 대한 지원은 선택사항입니다. 호스트 이름에 대한 지원도 선택사항입니다.

**`<i2p:unblock>`** : 선택사항이며, 여러 엔티티가 허용됩니다. `<i2p:block>`과 동일한 형식입니다.

**서명 사양:** 서명하거나 검증할 데이터를 생성하려면, 다음 데이터를 ASCII 인코딩으로 연결하세요: 업데이트된 문자열 뒤에 개행 문자(ASCII 0x0a)를 붙이고, 그 다음 수신된 순서대로 각 블록 항목을 개행 문자와 함께 추가한 후, 수신된 순서대로 각 언블록 항목을 개행 문자와 함께 추가합니다.

## 차단 목록 파일 사양

TBD, 구현되지 않음, proposal 130을 참조하세요. 차단 목록 업데이트는 위에서 설명한 뉴스 파일을 통해 전달됩니다.

## 향후 작업

- router 업데이트 메커니즘은 웹 router 콘솔의 일부입니다. 현재 router 콘솔이 없는 임베디드 router의 업데이트에 대한 규정은 없습니다.

## 참고 자료

- **[CRYPTO-SIG]** [암호화 - 서명](/docs/specs/cryptography#sig)
- **[I2P-SRC]** [I2P 소스 코드](https://github.com/i2p/i2p.i2p)
- **[PLUGIN]** [플러그인 명세](/docs/specs/plugin)
- **[Python]** [Python RSA Raw 서명](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530)
- **[RFC-3339]** [RFC 3339 - 날짜 및 시간](https://tools.ietf.org/html/rfc3339)
- **[RFC-4287]** [RFC 4287 - Atom 신디케이션 형식](https://tools.ietf.org/html/rfc4287)
- **[RFC-5280]** [RFC 5280 - 인증서 폐기 목록](https://tools.ietf.org/html/rfc5280)
- **[Signature]** [서명 타입](/docs/specs/common-structures#signature)
- **[SigningPublicKey]** [SigningPublicKey 타입](/docs/specs/common-structures#signingpublickey)
