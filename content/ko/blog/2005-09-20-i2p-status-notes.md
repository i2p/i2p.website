---
title: "I2P 상태 노트 2005-09-20자"
date: 2005-09-20
author: "jr"
description: "SSU introductions이 포함된 0.6.0.6 릴리스 성공, I2Phex 0.1.1.27 보안 업데이트, 코로케이션(colo) 마이그레이션 완료를 다루는 주간 업데이트"
categories: ["status"]
---

여러분 안녕하세요, 또 화요일이네요

* Index:

1) 0.6.0.6 2) I2Phex 0.1.1.27 3) 마이그레이션 4) ???

* 1) 0.6.0.6

지난 토요일의 0.6.0.6 릴리스와 함께 라이브 네트워크에서 여러 새로운 구성 요소가 가동되고 있으며, 여러분이 업그레이드를 정말 훌륭하게 진행해 주셨습니다—몇 시간 전 기준으로 거의 250개의 routers가 업그레이드되었습니다! 네트워크도 잘 동작하는 것으로 보이며, 지금까지 소개(introductions)가 정상적으로 작동하고 있습니다. http://localhost:7657/oldstats.jsp 에서 자신의 소개 활동을 추적할 수 있으며, udp.receiveHolePunch 및 udp.receiveIntroRelayResponse(또한 NAT 뒤에 있는 경우 udp.receiveRelayIntro) 항목을 확인해 보세요.

그런데 이제 "Status: ERR-Reject"는 실제로 오류가 아니므로, "Status: OK (NAT)"로 바꾸는 게 어떨까요?

Syndie에 몇 가지 버그 보고가 있었습니다. 가장 최근에는, 한 번에 너무 많은 게시물을 다운로드하도록 요청하면 원격 피어와 동기화에 실패하는 버그가 있습니다(어리석게도 POST 대신 HTTP GET을 사용했기 때문입니다). EepGet에 POST 지원을 추가할 예정이지만, 그때까지는 한 번에 20~30개 게시물만 가져오도록 해보세요. 참고로, remote.jsp 페이지에서 "이 사용자의 모든 게시물을 가져오기"라고 하여 해당 블로그의 체크박스를 자동으로 모두 선택해 주는 JavaScript를 누가 만들어 줄 수 있을까요?

들리는 바에 따르면 이제 OSX는 별다른 설정 없이 바로 잘 동작하고, 0.6.0.6-1에서는 Windows와 Linux 모두에서 x86_64도 정상적으로 동작합니다. 새로운 .exe 설치 프로그램에 대해서는 문제 보고를 아직 듣지 못했으니, 잘 진행되고 있거나 아예 완전히 망하고 있거나 둘 중 하나겠죠 :)

* 2) I2Phex 0.1.1.27

소스와 legion이 패키징한 0.1.1.26에 번들된 내용 간에 차이가 있다는 일부 보고와, 소스가 공개되지 않은 네이티브 런처(native launcher)의 안전성에 대한 우려를 계기로, 저는 launch4j [1]로 빌드한 새로운 i2phex.exe를 cvs에 추가했고, cvs 최신 소스로 빌드한 결과물을 i2p file archive [2]에 올려두었습니다. legion이 릴리스 전에 자신의 소스 코드에 다른 변경을 가했는지, 또는 그가 공개한 소스 코드가 실제로 그가 빌드한 것과 동일한지는 알 수 없습니다.

보안상의 이유로, legion의 클로즈드 소스 런처와 0.1.1.26 릴리스 중 어느 것도 사용을 권장할 수 없습니다. I2P 웹사이트 [2]에 있는 릴리스는 수정 없이 cvs에서 가져온 최신 코드를 포함합니다.

먼저 I2P 코드를 체크아웃하여 빌드하고, 이어서 I2Phex 코드를 체크아웃한 뒤, 마지막으로 "ant makeRelease"를 실행하면 빌드를 재현할 수 있습니다:   mkdir ~/devi2p ; cd ~/devi2p/   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot login

# (비밀번호: anoncvs)

cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2p   cd i2p ; ant build ; cd ..   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2phex   cd i2phex/build ; ant makeRelease ; cd ../..   ls -l i2phex/release/i2phex-0.1.1.27.zip

해당 zip 안의 i2phex.exe는 Windows에서는 그냥 실행하면 사용할 수 있고, *nix/osx에서는 "java -jar i2phex.exe"로 사용할 수 있습니다. I2P의 일부 jar 파일을 참조하므로, I2Phex가 I2P와 나란한 디렉터리에 설치되어 있어야 합니다 - (예: C:\Program Files\i2phex\ and C:\Program Files\i2p\).

저는 I2Phex를 유지보수하겠다고 나서지는 않지만, cvs에 업데이트가 있을 때마다 향후 I2Phex 릴리스를 웹사이트에 올리겠습니다. 우리가 게시할 수 있도록 이를 설명하고 소개하는 웹페이지를 작업해 주실 분이 있다면(sirup, 계신가요?), sirup.i2p, 유용한 포럼 게시물, legion의 활성 피어 목록에 대한 링크를 포함해 주시면 정말 좋겠습니다.

[1] http://launch4j.sourceforge.net/ [2] http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip 및     http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip.sig (내 키로 서명됨)

* 3) migration

I2P 서비스용 콜로케이션 서버를 교체했으며, 이제 새 머신에서 모든 것이 완전히 정상 작동 중이어야 합니다 - 뭔가 이상한 점이 보이면 알려주세요!

* 4) ???

요즘 i2p 리스트에서 흥미로운 논의가 많이 있었습니다. Adam이 만든 멋진 새 SMTP 프록시/필터 얘기도 있었고, syndie에 올라온 좋은 글들도 있었죠( http://gloinsblog.i2p 에서 gloin의 스킨 보셨나요?). 저는 현재 오랫동안 이어져 온 몇 가지 이슈를 해결하기 위한 변경 작업을 진행 중이지만, 당장 적용될 예정은 아닙니다. 다른 안건이나 논의하고 싶은 것이 있으면 GMT 기준 오후 8시에 #i2p에서 열리는 회의에 들러 주세요(약 10분 후쯤).

=jr
