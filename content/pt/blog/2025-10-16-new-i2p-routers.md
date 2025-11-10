---
title: "Novos I2P Routers"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Várias novas implementações de router I2P estão surgindo, incluindo emissary em Rust e go-i2p em Go, trazendo novas possibilidades para integração embutida e diversidade de rede."
---

Este é um momento empolgante para o desenvolvimento do I2P; nossa comunidade está crescendo e agora há vários novos protótipos de router I2P totalmente funcionais surgindo no cenário! Estamos muito empolgados com este desenvolvimento e em compartilhar as novidades com você.

## Como isso ajuda a rede?

Escrever I2P routers nos ajuda a comprovar que nossos documentos de especificação podem ser usados para produzir novos I2P routers, abre o código a novas ferramentas de análise e, de modo geral, melhora a segurança e a interoperabilidade da rede. Ter múltiplos I2P routers significa que os potenciais bugs não são uniformes; um ataque contra um router pode não funcionar em outro router, evitando um problema de monocultura. Talvez a perspectiva mais empolgante a longo prazo, no entanto, seja a incorporação (embedding).

## O que é incorporação?

No contexto do I2P, embedding (incorporação) é uma forma de incluir um I2P router em outro aplicativo diretamente, sem exigir um router autônomo em execução em segundo plano. Essa é uma maneira de tornar o I2P mais fácil de usar, o que facilita o crescimento da rede ao tornar o software mais acessível. Tanto o Java quanto o C++ sofrem por serem difíceis de usar fora de seus próprios ecossistemas, com o C++ exigindo bindings em C escritos manualmente e frágeis e, no caso do Java, a dificuldade de comunicar-se com um aplicativo da JVM a partir de um aplicativo não-JVM.

Embora, em muitos aspectos, esta situação seja bastante normal, acredito que ela pode ser melhorada para tornar o I2P mais acessível. Outras linguagens têm soluções mais elegantes para esses problemas. É claro que devemos sempre considerar e usar as diretrizes existentes para os routers Java e C++.

## o emissário surge das trevas

Totalmente independente da nossa equipe, um desenvolvedor chamado altonen desenvolveu uma implementação em Rust do I2P chamada emissary. Embora ainda seja bastante novo e Rust nos seja pouco familiar, este projeto intrigante tem grande potencial. Parabéns ao altonen pela criação do emissary, estamos bastante impressionados.

### Why Rust?

O principal motivo para usar Rust é basicamente o mesmo que o motivo para usar Java ou Go. Rust é uma linguagem de programação compilada, com gerenciamento de memória e uma comunidade enorme e altamente entusiasta. Rust também oferece recursos avançados para criar bindings (vinculações) para a linguagem de programação C, que podem ser mais fáceis de manter do que em outras linguagens e, ainda assim, herdam as fortes garantias de segurança de memória do Rust.

### Do you want to get involved with emissary?

O emissary é desenvolvido no Github por altonen. Você pode encontrar o repositório em: [altonen/emissary](https://github.com/altonen/emissary). O Rust também sofre com a falta de bibliotecas cliente SAMv3 abrangentes que sejam compatíveis com as bibliotecas populares de rede do Rust; escrever uma biblioteca SAMv3 é um ótimo ponto de partida.

## go-i2p is getting closer to completion

Há cerca de 3 anos tenho trabalhado no go-i2p, tentando transformar uma biblioteca incipiente em um I2P router completo em Go puro, outra linguagem com segurança de memória. Nos últimos 6 meses, aproximadamente, ele foi drasticamente reestruturado para melhorar o desempenho, a confiabilidade e a manutenibilidade.

### Why Go?

Embora Rust e Go partilhem muitas das mesmas vantagens, em muitos aspetos Go é muito mais simples de aprender. Há anos existem excelentes bibliotecas e aplicações para utilizar I2P na linguagem de programação Go, incluindo as implementações mais completas das bibliotecas SAMv3.3. Mas, sem um router I2P que possamos gerir automaticamente (como um router integrado), isso ainda representa uma barreira para os utilizadores. O objetivo do go-i2p é preencher essa lacuna e remover todas as dificuldades para os programadores de aplicações para I2P que trabalham em Go.

### Por que Rust?

O go-i2p é desenvolvido no Github, principalmente por eyedeekay neste momento, e está aberto a contribuições da comunidade em [go-i2p](https://github.com/go-i2p/). Dentro deste espaço de nomes existem muitos projetos, como:

#### Router Libraries

Construímos estas bibliotecas para gerar as nossas bibliotecas do I2P router. Elas estão distribuídas em vários repositórios especializados para facilitar a revisão e torná-las úteis a outras pessoas que queiram criar I2P routers experimentais e personalizados.

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

Bem, há um projeto adormecido para escrever um [I2P router in C#](https://github.com/PeterZander/i2p-cs) se você quiser executar o I2P em um XBox. Na verdade, parece bem interessante. Se essa também não for a sua preferência, você poderia fazer como o altonen fez e desenvolver um totalmente novo.

### Quer se envolver com emissary?

Você pode escrever um router I2P por qualquer motivo; é uma rede livre, mas ajuda saber por quê. Há uma comunidade que você quer fortalecer, uma ferramenta que você acha que é uma boa opção para o I2P, ou uma estratégia que você quer experimentar? Descubra qual é o seu objetivo para saber por onde começar e como será um estado "concluído".

### Decide what language you want to do it in and why

Aqui estão algumas razões pelas quais você pode escolher um idioma:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with node and deno, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

Mas aqui estão algumas razões pelas quais você talvez não escolha essas linguagens:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

Há centenas de linguagens de programação, e acolhemos bibliotecas e routers do I2P mantidos ativamente em todas elas. Escolha seus trade-offs com sabedoria e comece.

## go-i2p está cada vez mais próximo da conclusão

Quer você queira trabalhar em Rust, Go, Java, C++ ou alguma outra linguagem, entre em contato conosco no #i2p-dev no Irc2P. Comece por lá e vamos integrar você a canais específicos do router. Também estamos presentes no ramble.i2p em f/i2p, no reddit em r/i2p e no GitHub e no git.idk.i2p. Aguardamos seu contato em breve.
