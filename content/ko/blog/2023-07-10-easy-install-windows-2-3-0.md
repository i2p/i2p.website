---
title: "Windows용 Easy-Install 2.3.0 릴리스"
date: 2023-07-10
author: "idk"
description: "Windows용 Easy-Install 2.3.0 출시"
categories: ["release"]
---

Windows용 I2P Easy-Install 번들 2.3.0 버전이 릴리스되었습니다. 평소처럼, 이번 릴리스에는 업데이트된 I2P router 버전이 포함되어 있습니다. 이는 네트워크에서 서비스를 호스팅하는 이들에게 영향을 미치는 보안 문제까지 포함됩니다.

이번 릴리스는 I2P Desktop GUI와 호환되지 않는 Easy-Install 번들의 마지막 릴리스가 될 것입니다. 포함된 모든 웹 확장 프로그램을 최신 버전으로 갱신했습니다. 사용자 지정 테마와의 비호환을 일으키던 I2P in Private Browsing의 오래된 버그가 수정되었습니다. 사용자에게는 여전히 사용자 지정 테마를 설치하지 *말 것을* 권고합니다. Firefox에서 Snark 탭은 탭 순서의 맨 위에 자동으로 고정되지 않습니다. 대체 cookieStores(쿠키 저장소/컨테이너)를 사용하는 경우를 제외하면, Snark 탭은 이제 일반 브라우저 탭처럼 동작합니다.

**유감스럽게도 이번 릴리스는 여전히 서명되지 않은 `.exe` 설치 프로그램입니다.** 사용하기 전에 설치 프로그램의 체크섬을 확인해 주십시오. **반면 업데이트는** 제 I2P 서명 키로 서명되어 있으므로 안전합니다.

이번 릴리스는 OpenJDK 20으로 컴파일되었습니다. 브라우저 실행을 위한 라이브러리로 i2p.plugins.firefox 버전 1.1.0을 사용합니다. I2P router 및 애플리케이션 제공을 위해 i2p.i2p 버전 2.3.0을 사용합니다. 항상 그렇듯 가능한 한 빠른 시일 내에 I2P router를 최신 버전으로 업데이트할 것을 권장합니다.

- [Easy-Install Bundle Source](http://git.idk.i2p/i2p-hackers/i2p.firefox/-/tree/i2p-firefox-2.3.0)
- [Router Source](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/tree/i2p-2.3.0)
- [Profile Manager Source](http://git.idk.i2p/i2p-hackers/i2p.plugins.firefox/-/tree/1.1.0)
