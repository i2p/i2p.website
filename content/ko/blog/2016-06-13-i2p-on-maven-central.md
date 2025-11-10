---
title: "Maven Central에서의 I2P"
date: 2016-06-13
author: "str4d"
description: "I2P 클라이언트 라이브러리는 이제 Maven Central에서 이용할 수 있습니다!"
categories: ["summer-dev"]
---

Summer Dev의 API 달도 거의 절반을 지나고 있으며, 여러 측면에서 큰 진전을 이루고 있습니다. 이 가운데 첫 번째 성과가 완료되었음을 발표하게 되어 기쁩니다: I2P 클라이언트 라이브러리가 이제 Maven Central에서 제공됩니다!

이는 Java 개발자들이 애플리케이션에서 I2P를 사용하는 것을 훨씬 더 간단하게 만들어 줄 것입니다. 현재 설치에서 라이브러리를 가져올 필요 없이, 의존성에 I2P를 간단히 추가하기만 하면 됩니다. 새로운 버전으로 업그레이드하는 일도 마찬가지로 훨씬 더 쉬워질 것입니다.

## 사용 방법

알아두어야 하는 라이브러리가 두 가지 있습니다:

- `net.i2p:i2p` - The core I2P APIs; you can use these to send individual datagrams.
- `net.i2p.client:streaming` - A TCP-like set of sockets for communicating over I2P.

이 중 하나 또는 둘 다를 프로젝트의 의존성에 추가하면 바로 사용할 수 있습니다!

### Gradle

```
compile 'net.i2p:i2p:0.9.26'
compile 'net.i2p.client:streaming:0.9.26'
```
### Gradle

```xml
<dependency>
    <groupId>net.i2p</groupId>
    <artifactId>i2p</artifactId>
    <version>0.9.26</version>
</dependency>
<dependency>
    <groupId>net.i2p.client</groupId>
    <artifactId>streaming</artifactId>
    <version>0.9.26</version>
</dependency>
```
다른 빌드 시스템의 경우, 코어 및 스트리밍 라이브러리에 대한 Maven Central 페이지를 참조하세요.

Android 개발자는 동일한 라이브러리와 Android 전용 헬퍼를 포함한 I2P Android 클라이언트 라이브러리를 사용해야 합니다. 곧 이를 새로운 I2P 라이브러리에 의존하도록 업데이트하여, 크로스 플랫폼 애플리케이션이 I2P Android 또는 데스크톱 I2P 중 어느 쪽과도 네이티브로 동작할 수 있도록 할 예정입니다.

## Get hacking!

이 라이브러리를 사용하기 시작하는 데 도움이 필요하면 저희 애플리케이션 개발 가이드를 참조하세요. 또한 IRC의 #i2p-dev에서 이에 대해 저희와 대화하실 수도 있습니다. 그리고 실제로 사용을 시작하셨다면, Twitter에서 #I2PSummer 해시태그로 어떤 작업을 하고 계신지 알려 주세요!
