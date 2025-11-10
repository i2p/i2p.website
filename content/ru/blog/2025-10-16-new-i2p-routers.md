---
title: "Новые I2P Routers"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Появляются несколько новых реализаций I2P router, включая emissary на Rust и go-i2p на Go, которые открывают новые возможности для встраивания и разнообразия сети."
---

Сейчас захватывающее время для разработки I2P: наше сообщество растёт, и появляются несколько новых, полностью функционирующих прототипов I2P router! Мы очень рады такому развитию событий и тому, что можем поделиться этими новостями с вами.

## Как это помогает сети?

Написание I2P routers помогает нам доказать, что наши спецификации можно использовать для создания новых I2P routers, делает код доступным для новых инструментов анализа и в целом повышает безопасность и совместимость сети. Наличие нескольких I2P routers означает, что потенциальные ошибки не однотипны: атака на один router может не сработать против другого router, что позволяет избежать проблемы монокультуры. Однако, возможно, в долгосрочной перспективе наиболее интересным является встраивание.

## Что такое встраивание?

В контексте I2P встраивание — это способ напрямую включить I2P router в другое приложение, без необходимости запускать отдельный router, работающий в фоновом режиме. Это способ сделать I2P проще в использовании, что облегчает рост сети, делая программное обеспечение более доступным. И Java, и C++ страдают тем, что их трудно использовать вне собственных экосистем: для C++ требуются хрупкие, написанные вручную привязки на C, а в случае Java — мучительное взаимодействие с приложением на JVM из приложения, не работающего на JVM.

Хотя во многом эта ситуация вполне нормальна, я считаю, что её можно улучшить, чтобы сделать I2P более доступным. В других языках есть более изящные решения этих проблем. Разумеется, нам всегда следует учитывать и использовать существующие рекомендации для routers на Java и C++.

## Эмиссар появляется из тьмы

Полностью независимо от нашей команды разработчик под ником altonen создал реализацию I2P на Rust под названием emissary. Хотя он всё ещё довольно нов, а Rust нам незнаком, этот интригующий проект подаёт большие надежды. Поздравляем altonen с созданием emissary, мы весьма впечатлены.

### Why Rust?

Основная причина использовать Rust по сути та же, что и причина использовать Java или Go. Rust — это компилируемый язык программирования с управлением памятью и огромным, очень активным сообществом. Rust также предлагает расширенные возможности для создания биндингов к языку программирования C, которые могут быть проще в сопровождении, чем в других языках, при этом наследуют сильные гарантии Rust в отношении безопасности памяти.

### Do you want to get involved with emissary?

emissary разрабатывается на GitHub пользователем altonen. Репозиторий можно найти здесь: [altonen/emissary](https://github.com/altonen/emissary). Rust также страдает от нехватки полноценных клиентских библиотек SAMv3, совместимых с популярными сетевыми библиотеками для Rust; написание библиотеки SAMv3 — отличная отправная точка.

## go-i2p is getting closer to completion

Вот уже около трёх лет я работаю над go-i2p, пытаясь превратить молодую библиотеку в полноценный I2P router на чистом Go, ещё одном языке с безопасной работой с памятью. За последние примерно шесть месяцев она была кардинально переработана для повышения производительности, надёжности и удобства сопровождения.

### Why Go?

Хотя у Rust и Go много одинаковых преимуществ, во многом Go гораздо проще для изучения. На протяжении многих лет существуют отличные библиотеки и приложения для использования I2P на языке программирования Go, включая самые полные реализации библиотек SAMv3.3. Но без I2P router, которым можно управлять автоматически (например, встроенного router), это по‑прежнему остаётся барьером для пользователей. Цель go-i2p — устранить этот разрыв и убрать все острые углы для разработчиков приложений I2P, работающих на Go.

### Почему Rust?

go-i2p разрабатывается на Github, в настоящее время главным образом eyedeekay, и открыт для вкладов сообщества на [go-i2p](https://github.com/go-i2p/). В этом пространстве имён существует множество проектов, например:

#### Router Libraries

Мы создали эти библиотеки для разработки наших библиотек I2P router. Они распределены по нескольким узкоспециализированным репозиториям, чтобы упростить ревью и сделать их полезными другим людям, которые хотят создавать экспериментальные, настраиваемые I2P routers.

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

Ну, есть неактивный проект по написанию [I2P router на C#](https://github.com/PeterZander/i2p-cs), если вы хотите запускать I2P на XBox. Вообще-то звучит довольно здорово. Если и это вам не по душе, можете сделать как сделал altonen и разработать совершенно новый.

### Хотите принять участие в emissary?

Вы можете написать I2P router по любой причине — это свободная сеть, — но полезно понимать, зачем. Есть ли сообщество, которое вы хотите поддержать, инструмент, который, по вашему мнению, хорошо подходит для I2P, или стратегия, которую вы хотите опробовать? Определите свою цель, чтобы понять, с чего нужно начать и как будет выглядеть «завершённое» состояние.

### Decide what language you want to do it in and why

Вот несколько причин, по которым вы можете выбрать язык:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with node and deno, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

But here are some reasons why you might not choose those languages:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

Существуют сотни языков программирования, и мы приветствуем сопровождаемые библиотеки I2P и routers на любом из них. Выбирайте компромиссы с умом и приступайте.

## go-i2p все ближе к завершению

Независимо от того, хотите ли вы работать на Rust, Go, Java, C++ или на каком-то другом языке, свяжитесь с нами в #i2p-dev на Irc2P. Начните там, и мы добавим вас в каналы, связанные с router. Мы также присутствуем на ramble.i2p в f/i2p, на reddit в r/i2p, а также на GitHub и git.idk.i2p. Будем рады вашему скорому отклику.
