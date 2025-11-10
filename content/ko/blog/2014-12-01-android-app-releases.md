---
title: "안드로이드 앱 릴리스"
date: 2014-12-01
author: "str4d"
description: "I2P Android 0.9.17 및 Bote 0.3이 웹사이트, Google Play 및 F-Droid에서 공개되었습니다."
categories: ["press"]
---

마지막으로 우리 Android 개발에 대한 업데이트를 올린 지 꽤 시간이 흘렀고, 그 사이 I2P 릴리스가 몇 차례 있었지만 이에 맞는 Android 릴리스는 없었습니다. 드디어 기다림이 끝났습니다!

## 새 앱 버전

I2P Android와 Bote의 새 버전이 출시되었습니다! 다음 URL에서 다운로드할 수 있습니다:

- [I2P Android 0.9.17](https://geti2p.net/en/download#android)
- [Bote 0.3](https://download.i2p.io/android/bote/releases/0.3/Bote.apk)

이번 릴리스에서 가장 큰 변화는 Android의 새로운 Material 디자인 시스템으로의 전환입니다. Material 덕분에, 말하자면 '미니멀한' 디자인 실력(저처럼)을 가진 앱 개발자들도 사용하기 더 좋은 앱을 훨씬 쉽게 만들 수 있게 되었습니다. I2P Android는 또한 기반이 되는 I2P router를 방금 공개된 버전 0.9.17로 업데이트합니다. Bote는 여러 가지 작은 개선과 함께 몇 가지 새로운 기능을 도입했습니다. 예를 들어 이제 QR 코드로 새로운 email destinations(이메일 목적지 주소)를 추가할 수 있습니다.

지난 업데이트에서 말씀드렸듯이, 앱에 서명하는 릴리스 키가 변경되었습니다. 그 이유는 I2P Android의 패키지 이름을 변경할 필요가 있었기 때문입니다. 이전 패키지 이름(`net.i2p.android.router`)은 이미 Google Play에서 사용 중이었고(누가 사용했는지는 아직도 모릅니다), 우리는 I2P Android의 모든 배포 경로에서 동일한 패키지 이름과 서명 키를 사용하길 원했습니다. 이렇게 하면 사용자가 처음에는 I2P 웹사이트에서 앱을 설치하고, 나중에 웹사이트가 차단되더라도 Google Play를 통해 업그레이드할 수 있습니다. Android OS에서는 패키지 이름이 변경되면 애플리케이션을 완전히 다른 것으로 간주하므로, 이 기회에 서명 키의 강도를 높였습니다.

새로운 서명 키의 지문(SHA-256)은:

```
AD 1E 11 C2 58 46 3E 68 15 A9 86 09 FF 24 A4 8B C0 25 86 C2 36 00 84 9C 16 66 53 97 2F 39 7A 90
```
## 구글 플레이

몇 달 전 우리는 그곳의 출시 절차를 테스트하기 위해 노르웨이 지역 Google Play에 I2P Android와 Bote를 모두 출시했습니다. 이제 두 앱이 [Privacy Solutions](https://privacysolutions.no/)에 의해 전 세계적으로 출시되고 있음을 기쁘게 알려드립니다. 앱은 다음 URL에서 확인할 수 있습니다:

- [I2P on Google Play](https://play.google.com/store/apps/details?id=net.i2p.android)
- [Bote on Google Play](https://play.google.com/store/apps/details?id=i2p.bote.android)

전 세계 출시는 번역이 준비된 국가부터 시작하여 여러 단계로 진행되고 있습니다. 주목할 만한 예외는 프랑스입니다. 암호화 코드에 대한 수입 규정으로 인해 현재로서는 Google Play France에서 이러한 앱을 배포할 수 없습니다. 이는 TextSecure 및 Orbot과 같은 다른 앱에도 영향을 미쳤던 동일한 문제입니다.

## F-Droid

F-Droid 사용자 여러분을 잊은 건 아닙니다! 위의 두 위치 외에도 저희는 자체 F-Droid 저장소를 마련했습니다. 이 글을 휴대전화에서 읽고 계시다면, F-Droid에 추가하려면 [여기를 클릭하세요](https://f-droid.i2p.io/repo?fingerprint=68E76561AAF3F53DD53BA7C03D795213D0CA1772C3FAC0159B50A5AA85C45DC6) (일부 Android 브라우저에서만 작동합니다). 또는 아래 URL을 F-Droid 저장소 목록에 수동으로 추가할 수 있습니다:

https://f-droid.i2p.io/repo

저장소 서명 키의 지문(SHA-256)을 수동으로 검증하거나 저장소를 추가할 때 직접 입력하려는 경우, 다음과 같습니다:

```
68 E7 65 61 AA F3 F5 3D D5 3B A7 C0 3D 79 52 13 D0 CA 17 72 C3 FA C0 15 9B 50 A5 AA 85 C4 5D C6
```
불행히도 메인 F-Droid 저장소의 I2P 앱은 우리 F-Droid 유지관리자와의 연락이 두절되어 업데이트되지 못했습니다. 우리는 이 바이너리 저장소를 유지함으로써 F-Droid 사용자들을 더 잘 지원하고 최신 상태로 유지할 수 있기를 바랍니다. 이미 메인 F-Droid 저장소에서 I2P를 설치했다면, 서명 키가 다르기 때문에 업그레이드하려면 먼저 제거해야 합니다. 우리 F-Droid 저장소의 앱들은 우리 웹사이트와 Google Play에서 제공되는 것과 동일한 APK이므로, 앞으로는 이러한 소스 중 어느 것을 사용해도 업그레이드할 수 있습니다.
