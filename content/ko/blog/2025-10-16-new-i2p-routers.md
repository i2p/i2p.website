---
title: "새로운 I2P router들"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Rust로 작성된 emissary와 Go로 작성된 go-i2p를 포함해 여러 새로운 I2P router 구현이 등장하면서, 임베딩과 네트워크 다양성에 새로운 가능성을 열고 있습니다."
---

I2P 개발이 매우 흥미로운 시기를 맞이했습니다. 우리 커뮤니티는 성장하고 있으며, 이제 새롭고 완전한 기능을 갖춘 I2P router 프로토타입들이 여러 개 등장하고 있습니다! 우리는 이러한 발전과 이 소식을 여러분과 공유하게 되어 매우 기쁩니다.

## 이것이 네트워크에 어떻게 도움이 되나요?

I2P router를 구현하는 것은 우리의 사양 문서가 새로운 I2P router를 만드는 데 사용될 수 있음을 입증하는 데 도움이 되며, 새로운 분석 도구가 코드를 분석할 수 있도록 하고, 전반적으로 네트워크의 보안성과 상호운용성을 향상시킵니다. 여러 I2P router의 존재는 잠재적 버그가 획일화되지 않음을 의미하며, 한 router에서 통하는 공격이 다른 router에서는 통하지 않을 수 있어 모노컬처 문제를 피할 수 있습니다. 그러나 장기적으로 가장 흥미로운 가능성은 아마도 임베딩입니다.

## 임베딩이란 무엇입니까?

I2P 맥락에서 임베딩(embedding)은 백그라운드에서 독립 실행형 router가 실행될 필요 없이 I2P router를 다른 앱에 직접 포함하는 방식입니다. 이는 I2P를 더 쉽게 사용할 수 있게 만들어 소프트웨어의 접근성을 높이고, 그 결과 네트워크가 더 쉽게 성장하도록 합니다. Java와 C++는 모두 자체 생태계 밖에서 사용하기 어렵다는 한계를 갖고 있으며, C++의 경우 깨지기 쉬운 수작업 C 바인딩을 요구하고, Java의 경우에는 비‑JVM 앱에서 JVM 앱과 통신해야 하는 고통이 있습니다.

While in many ways this situation is quite normal, I believe it can be improved to make I2P more accessible. Other languages have more elegant solutions to these problems. Of course, we should always consider and use the existing guidelines for the Java and C++ routers.

## 사절이 어둠 속에서 나타난다

우리 팀과는 완전히 별개로, altonen이라는 개발자가 emissary라는 I2P의 Rust 구현을 개발했습니다. 아직은 꽤 새롭고 Rust가 우리에게 익숙하지는 않지만, 이 흥미로운 프로젝트는 큰 가능성을 보여줍니다. emissary를 만든 altonen에게 축하를 전하며, 우리는 매우 깊은 인상을 받았습니다.

### Why Rust?

Rust를 사용해야 하는 주된 이유는 기본적으로 Java나 Go를 사용하는 이유와 같습니다. Rust는 메모리 관리 기능을 갖춘 컴파일형 프로그래밍 언어이며, 방대하고 매우 열정적인 커뮤니티를 보유하고 있습니다. 또한 Rust는 C 프로그래밍 언어에 대한 바인딩을 생성하기 위한 고급 기능을 제공하여, 다른 언어보다 유지보수가 더 쉬울 수 있으면서도 Rust의 강력한 메모리 안전성 특성을 그대로 이어받습니다.

### Do you want to get involved with emissary?

emissary는 altonen이 GitHub에서 개발하고 있습니다. 저장소는 다음에서 확인할 수 있습니다: [altonen/emissary](https://github.com/altonen/emissary). 또한 Rust는 인기 있는 Rust 네트워킹 생태계와 호환되는 포괄적인 SAMv3 클라이언트 라이브러리가 부족한 상황이므로, SAMv3 라이브러리부터 작성해 보는 것이 시작하기에 좋은 방법입니다.

## go-i2p is getting closer to completion

약 3년 동안 go-i2p를 개발해 오며, 초기 단계의 라이브러리를 메모리 안전한 또 다른 언어인 Go로 순수 구현된 완전한 기능의 I2P router로 탈바꿈시키기 위해 노력해 왔습니다. 지난 6개월가량 동안에는 성능, 신뢰성, 유지보수성을 개선하기 위해 대대적으로 재구성되었습니다.

### Why Go?

Rust와 Go는 많은 장점을 공유하지만, 여러 면에서 Go가 배우기 훨씬 더 쉽습니다. 수년간 Go 프로그래밍 언어에서는 I2P를 사용하기 위한 뛰어난 라이브러리와 애플리케이션이 존재해 왔으며, SAMv3.3 라이브러리의 가장 완전한 구현도 포함되어 있습니다. 하지만 자동으로 관리할 수 있는 I2P router(예: embedded router(애플리케이션에 내장된 router))가 없다면, 이는 여전히 사용자에게 장벽이 됩니다. go-i2p의 목적은 그 격차를 메우고, Go에서 작업하는 I2P 애플리케이션 개발자들을 위해 남아 있는 모든 불편함을 없애는 것입니다.

### 왜 Rust인가?

현재 go-i2p는 Github에서 주로 eyedeekay가 개발하고 있으며, 커뮤니티의 기여를 [go-i2p](https://github.com/go-i2p/)에서 받고 있습니다. 이 네임스페이스에는 다음과 같은 여러 프로젝트가 있습니다:

#### Router Libraries

우리는 우리의 I2P router 라이브러리를 만들기 위해 이 라이브러리들을 구축했습니다. 검토를 용이하게 하고 실험적·맞춤형 I2P router를 구축하려는 다른 사람들에게 유용하게 만들기 위해, 이 라이브러리들은 여러 개의 특화된 리포지토리로 나뉘어 있습니다.

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### Client libraries

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## If you don't like Go or Rust and are thinking of writing an I2P Router, what should you do?

XBox에서 I2P를 실행하고 싶다면, [C#로 작성하는 I2P router](https://github.com/PeterZander/i2p-cs) 프로젝트가 휴면 상태로 있습니다. 사실 꽤 흥미롭습니다. 그것도 선호하지 않는다면, altonen이 했던 것처럼 완전히 새로운 router를 개발할 수도 있습니다.

### emissary에 참여하고 싶으신가요?

어떤 이유에서든 I2P router를 구현할 수 있습니다. I2P는 자유로운 네트워크이지만, 왜 그렇게 하려는지 아는 것이 도움이 됩니다. 역량을 강화하고 싶은 커뮤니티, I2P에 잘 맞는다고 생각하는 도구, 또는 시도해 보고 싶은 전략이 있나요? 자신의 목표가 무엇인지 파악하여 어디에서 시작해야 하는지, 그리고 "finished" 상태가 어떤 모습일지 정하세요.

### Decide what language you want to do it in and why

언어를 선택할 때 고려할 수 있는 몇 가지 이유는 다음과 같습니다:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with node and deno, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

하지만 그 언어들을 선택하지 않을 수 있는 몇 가지 이유는 다음과 같습니다:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

프로그래밍 언어는 수백 가지가 있으며, 우리는 그 모든 언어로 구현된, 활발히 유지·관리되는 I2P 라이브러리와 routers(라우터)를 환영합니다. 트레이드오프를 신중하게 선택하고 시작하세요.

## go-i2p는 완성에 점점 가까워지고 있습니다

Rust, Go, Java, C++ 또는 다른 어떤 언어로 작업하고 싶으시든, Irc2P의 #i2p-dev에서 저희에게 연락해 주세요. 그곳에서 시작하시면, router 전용 채널로 안내해 드리겠습니다. ramble.i2p의 f/i2p, reddit의 r/i2p, 그리고 GitHub와 git.idk.i2p에서도 활동하고 있습니다. 곧 연락을 기다리고 있겠습니다.
