---
title: "2006-09-12자 I2P 상태 노트"
date: 2006-09-12
author: "jr"
description: "네트워크 안정성 개선, I2PSnark 최적화, 오프라인 분산 포럼을 포함한 Syndie의 전면적인 재설계를 수반한 0.6.1.25 릴리스"
categories: ["status"]
---

안녕하세요 여러분, 여기 우리의 *콜록* 주간 상태 노트가 있어요

* Index:

1) 0.6.1.25 및 네트워크 상태 2) I2PSnark 3) Syndie (무엇/왜/언제) 4) Syndie 암호화 관련 질문 5) ???

* 1) 0.6.1.25 and net status

며칠 전에 우리는 0.6.1.25 릴리스를 배포했으며, 지난 한 달 동안 축적된 다수의 버그 수정과 함께 I2PSnark에 대한 zzz의 작업, 그리고 시간 동기화 코드를 좀 더 견고하게 만들기 위한 Complication의 작업이 포함되었습니다. 현재 네트워크는 꽤 안정적인 것으로 보이지만, 지난 며칠 동안 IRC는 다소 불안정했습니다(I2P와 관련 없는 이유로). 네트워크의 절반가량이 최신 릴리스로 업그레이드된 상황에서, tunnel 구축 성공률은 크게 변하지 않았지만 전체 처리량은 증가한 것으로 보입니다(아마 I2PSnark를 사용하는 사람들의 증가 때문일 것입니다).

* 2) I2PSnark

히스토리 로그 [1]에 설명된 대로, zzz의 I2PSnark 업데이트에는 프로토콜 최적화뿐 아니라 웹 인터페이스 변경도 포함되었습니다. 또한 0.6.1.25 릴리스 이후에도 I2PSnark에는 몇 가지 작은 업데이트가 있었고, 아마 zzz가 오늘 밤 회의에서 최근 상황에 대한 개요를 제공해 줄 수 있을 것입니다.

[1] <http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD>

* 3) Syndie

다들 아시다시피, 그동안 저는 Syndie를 개편하는 데 주력해 왔지만 "revamp"가 꼭 맞는 표현은 아닐지도 모르겠습니다. 새로운 Syndie는 많은 개념을 유지하면서도 처음부터 다시 설계하고 재구현되었기 때문에, 현재 배포되어 있는 것은 "proof of concept"(개념 증명)으로 보셔도 될 것입니다. 아래에서 제가 Syndie라고 할 때는 새로운 Syndie를 의미합니다.

* 3.1) What is Syndie

Syndie는 가장 기본적인 수준에서 오프라인 분산 포럼을 운영하기 위한 시스템입니다. 구조상 매우 다양한 구성이 가능하지만, 아래 세 가지 기준 각각에서 하나씩 선택하면 대부분의 요구를 충족할 수 있습니다:  - 포럼 유형:    - 단일 작성자(일반적인 블로그)    - 여러 작성자(다중 작성자 블로그)**    - 개방형(뉴스그룹, 다만 제한을 두어
      권한이 있는** 사용자만 새 스레드를 게시할 수 있게 하고, 누구나 그 새 스레드에
      댓글을 달 수 있음)  - 가시성:    - 누구나 무엇이든 읽을 수 있음    - 권한이 있는* 사람만 게시물을 읽을 수 있지만, 일부 메타데이터는 노출됨    - 권한이 있는* 사람만 게시물을 읽을 수 있고, 심지어 누가 게시하는지조차 권한이 있는 사람이 알 수 있음    - 권한이 있는* 사람만 게시물을 읽을 수 있고, 아무도 누가
      게시하는지 알 수 없음  - 댓글/답장:    - 누구나 댓글을 달거나 작성자/포럼
      소유자에게 비공개 답장을 보낼 수 있음    - 권한이 있는** 사람만 댓글을 달 수 있으며, 비공개
      답장은 누구나 보낼 수 있음    - 아무도 댓글을 달 수 없지만, 비공개 답장은 누구나 보낼 수 있음    - 아무도 댓글을 달 수 없고, 아무도 비공개 답장을 보낼 수 없음

 * reading is authorized by giving people the symmetric key or passphrase
   to decrypt the post.  Alternately, the post may include a publicly
   visible prompt, where the correct answer serves to generate the
   correct decryption key.

** 게시, 업데이트 및/또는 댓글 작성은 해당 사용자에게 게시물 서명을 위한 비대칭 개인 키를 제공함으로써 허가되며, 이에 대응하는 공개 키는 포럼의 메타데이터에 포럼에서 게시, 관리 또는 댓글 작성 권한이 부여된 키로 포함됩니다.  또는 권한이 부여된 개별 사용자의 서명용 공개 키를 메타데이터에 나열할 수도 있습니다.

개별 게시물에는 여러 가지 요소가 포함될 수 있습니다:  - 페이지는 개수 제한이 없으며, 각 페이지마다 out of band 데이터(주 통신 경로와 분리된 별도 채널로 전달되는 데이터)로
    콘텐츠 유형, 언어 등을 지정합니다.  서식은 어떤 것이든 사용할 수 있으며, 이는
    콘텐츠를 안전하게 렌더링할 책임이 클라이언트 애플리케이션에 있으므로 - 일반 텍스트는
    반드시 지원되어야 하며, 가능한 클라이언트는 HTML도 지원해야 합니다.  - 첨부 파일도 개수 제한이 없으며(마찬가지로 첨부 파일을 설명하는 out of band 데이터가
    포함됨)  - 게시물용 작은 아바타(지정하지 않은 경우 작성자의
    기본 아바타가 사용됨)  - 다른 게시물, 포럼, 아카이브, URL 등에 대한 참조 목록(여기에는
    참조된 포럼에 글을 게시, 관리 또는 읽는 데 필요한 키가 포함될 수
    있습니다)

전반적으로 Syndie는 *콘텐츠 계층*에서 동작합니다 - 개별 게시물은 암호화된 zip 파일에 포함되어 있으며, 포럼에 참여한다는 것은 단순히 이 파일들을 공유하는 것을 의미합니다. 파일이 어떤 방식으로 전송되는지(I2P, Tor, Freenet, gnutella, bittorrent, RSS, usenet, email을 통해)에는 의존하지 않지만, 간단한 집계 및 배포 도구는 표준 Syndie 릴리스에 번들로 제공될 것입니다.

Syndie 콘텐츠와의 상호작용은 여러 가지 방식으로 이루어집니다. 먼저, 스크립팅 가능한 텍스트 기반 인터페이스가 있어, 기본적인 명령줄 및 대화형 방식으로 포럼을 읽고, 작성하고, 관리하고, 동기화할 수 있습니다. 예를 들어, 다음은 새로운 "message of the day"(오늘의 메시지) 게시물을 생성하는 간단한 스크립트입니다 -

login     menu post     create --channel 0000000000000000000000000000000000000000     addpage --in /etc/motd --content-type text/plain     addattachment --in ~/webcam.png --content-type image/png     listauthkeys --authorizedOnly true     authenticate 0     authorize 0     set --subject "Today's MOTD"     set --publicTags motd     execute     exit

간단히 그것을 syndie 실행 파일로 파이프로 전달하면 작업이 완료됩니다: cat motd-script | ./syndie > syndie.log

또한 Syndie용 그래픽 인터페이스에 대한 작업이 진행 중이며, 여기에는 평문 텍스트 및 HTML 페이지의 안전한 렌더링이 포함됩니다(물론 Syndie의 기능과의 원활한 통합도 지원합니다).

예전 Syndie의 'sucker' 코드에 기반한 애플리케이션은 일반 웹 페이지와 웹사이트를 스크래핑하고 재작성하여, 이미지 및 기타 리소스를 첨부 파일로 포함한 단일 또는 다중 페이지 Syndie 게시물로 사용할 수 있도록 해줍니다.

향후 firefox/mozilla 플러그인은 Syndie 형식의 파일과 Syndie 참조를 감지하여 가져올 뿐만 아니라, 특정 포럼, 주제, 태그, 작성자 또는 검색 결과에 포커스를 맞추도록 로컬 Syndie GUI에 알리는 기능도 제공할 예정입니다.

물론, Syndie는 본질적으로 정의된 파일 형식과 암호화 알고리즘을 갖춘 콘텐츠 계층이기 때문에, 시간이 지나면서 다른 애플리케이션이나 대체 구현이 등장할 가능성이 높습니다.

* 3.2) Why does Syndie matter?

지난 몇 달 동안 여러 사람이 이렇게 묻는 것을 들었다 - 왜 내가 포럼/블로깅 도구를 개발하고 있는지, 그게 강력한 익명성 제공과 무슨 관련이 있는지?

답: *모든 것*.

간략히 요약하면:  - 익명성에 민감한 클라이언트 애플리케이션으로서 Syndie의 설계는, 익명성을 염두에 두지 않고 구축된 거의 모든 애플리케이션이 피하지 못하는 복잡한 데이터 민감성 문제를 신중하게 피한다.  - 콘텐츠 계층에서 동작함으로써, Syndie는 I2P, Tor, Freenet 같은 분산 네트워크의 성능이나 신뢰성에 의존하지 않지만, 필요할 때는 이를 활용할 수 있다.  - 이렇게 함으로써, 콘텐츠 배포를 위한 소규모의 임시(ad-hoc) 메커니즘만으로도 완전하게 동작할 수 있다 - 강력한 적대자들이 이를 무력화하기 위해 들일 만한 가치가 없을 수 있는 메커니즘들이다(몇십 명만 검거하는 데서 얻는 '성과'가 공격을 수행하는 비용을 상회할 가능성이 크기 때문이다)  - 이는 수백만 명이 사용하지 않더라도 Syndie가 여전히 유용하다는 것을 의미한다 - 서로 관련 없는 소규모 사용자 집단은 다른 어떤 집단과의 상호작용이나 심지어 인지조차 필요 없이, 자신들만의 사설 Syndie 배포 체계를 구축해야 한다.  - Syndie는 실시간 상호작용에 의존하지 않으므로, 모든 저지연 시스템이 취약한 공격(예: passive intersection attacks(수동 교집합 공격), passive and active timing attacks(수동 및 능동 타이밍 공격), active blending attacks(능동 블렌딩 공격))을 피하기 위해 고지연 익명성 시스템과 기법까지도 활용할 수 있다.

전반적으로, 제 생각에는 Syndie가 router보다도 I2P의 핵심 사명(필요로 하는 이들에게 강력한 익명성을 제공하는 것)에 더 중요합니다. 모든 것을 해결하는 궁극적인 해법은 아니지만, 핵심적인 한 단계입니다.

* 3.3) When can we use Syndie?

텍스트 인터페이스의 거의 전부와 GUI(그래픽 사용자 인터페이스)의 상당 부분을 포함하여 많은 작업이 완료되었지만, 아직 해야 할 작업이 남아 있습니다. 첫 번째 Syndie 릴리스에는 다음과 같은 기본 기능이 포함됩니다:

 - Scriptable text interface, packaged up as a typical java application,
   or buildable with a modern GCJ
 - Support for all forum types, replies, comments, etc.
 - Manual syndication, transferring .snd files.
 - HTTP syndication, including simple CGI scripts to operate archives,
   controllable through the text interface.
 - Specs for the file formats, encryption algorithms, and database
   schema.

그걸 배포할 때 내가 적용할 기준은 "완전한 기능 제공"이다. 일반 사용자는 텍스트 기반 앱을 굳이 쓰려 하지는 않겠지만, 일부 기술 애호가들은 그럴 거라고 기대한다.

이후 릴리스에서는 Syndie의 기능이 여러 측면에서 개선될 것입니다:  - 사용자 인터페이스:   - SWT 기반 GUI   - 웹 브라우저 플러그인   - 웹 스크레이핑 텍스트 UI (페이지를 가져와 재작성)   - IMAP/POP3/NNTP 읽기 인터페이스  - 콘텐츠 지원   - 일반 텍스트   - HTML (GUI 내에서 안전하게 렌더링, 브라우저에서는 아님)   - BBCode (?)  - 신디케이션   - Feedspace, Feedtree 및 기타 저지연 동기화 도구   - Freenet (CHK@s에 .snd 파일을 저장하고, 아카이브는     SSK@s 및 USK@s의 .snd 파일을 참조)   - 이메일 (SMTP/mixmaster/mixminion을 통해 게시,     procmail/etc를 통해 읽기)   - Usenet (NNTP 또는 리메일러를 통해 게시, (프록시된)     NNTP를 통해 읽기)  - Lucene 통합을 통한 전체 텍스트 검색  - 전체 데이터베이스 암호화를 위한 HSQLDB 확장  - 추가 아카이브 관리 휴리스틱

무엇이 언제 나오느냐는 일이 언제 수행되느냐에 달려 있다.

* 4) Open questions for Syndie

현재 Syndie는 I2P의 표준 암호 프리미티브 - SHA256, AES256/CBC, ElGamal2048, DSA로 구현되어 있다. 그러나 마지막 것은 이질적이다. 1024비트 공개키를 사용하고 (급속히 약화되고 있는) SHA1에 의존하기 때문이다. 현장에서 들은 이야기 중 하나는 DSA에 SHA256을 보강하는 방안인데, 그것은 가능하긴 하지만(아직 표준화되지는 않았고), 여전히 1024비트 공개키만 제공한다.

아직 Syndie가 널리 배포되지 않았고 하위 호환성을 걱정할 필요가 없으므로, 우리는 암호학 기본 구성요소(primitive)를 서로 바꿔볼 여유가 있다. 한 가지 견해는 DSA 대신 ElGamal2048 또는 RSA2048 서명을 선택하자는 것이고, 또 다른 견해는 ECC(ECDSA 서명과 ECIES 비대칭 암호화)의 도입을 검토하되 보안 수준을 256비트 또는 521비트(각각 128비트 및 256비트 대칭 키 크기에 상응)로 설정하자는 것이다.

ECC(타원곡선 암호)와 관련된 특허 이슈는 특정 최적화(point compression)와 우리가 필요로 하지 않는 알고리즘(EC MQV)에만 관련되는 것으로 보입니다. Java 지원 측면에서는 마땅한 것이 많지 않지만, bouncycastle 라이브러리에 일부 코드가 있는 것으로 보입니다. 다만, libGMP에서 그랬던 것처럼(jbigi를 얻기 위해), libtomcrypt, openssl, 또는 crypto++에 작은 래퍼(wrapper)를 추가하는 것도 아마 큰 어려움은 없을 것입니다.

이에 대해 어떻게 생각하시나요?

* 5) ???

위에서 살펴볼 내용이 많아서, (cervantes의 제안에 따라) 이렇게 일찍 상태 노트를 보내드립니다. 의견, 질문, 우려, 또는 제안이 있으시다면, 오늘 UTC 기준 오후 8시에 irc.freenode.net/irc.postman.i2p/irc.freshcoffee.i2p 에 있는 #i2p로 가볍게 들러 주세요. 우리 *콜록* 주간 회의가 열립니다!

=jr
