---
title: "I2P no Maven Central"
date: 2016-06-13
author: "str4d"
description: "As bibliotecas de cliente do I2P agora estão disponíveis no Maven Central!"
categories: ["summer-dev"]
---

Estamos quase na metade do mês de APIs do Summer Dev, e fazendo grandes progressos em várias frentes. Tenho o prazer de anunciar que o primeiro deles está concluído: as bibliotecas cliente do I2P agora estão disponíveis no Maven Central!

Isto deve tornar muito mais simples para desenvolvedores Java usarem o I2P em suas aplicações. Em vez de precisarem obter as bibliotecas a partir de uma instalação atual, eles podem simplesmente adicionar o I2P às suas dependências. Da mesma forma, atualizar para novas versões será muito mais fácil.

## Como usá-los

Há duas bibliotecas que você precisa conhecer:

- `net.i2p:i2p` - The core I2P APIs; you can use these to send individual datagrams.
- `net.i2p.client:streaming` - A TCP-like set of sockets for communicating over I2P.

Adicione um ou ambos destes às dependências do seu projeto e está pronto para começar!

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
Para outros sistemas de build, consulte as páginas no Maven Central das bibliotecas core e streaming.

Os desenvolvedores para Android devem usar a biblioteca cliente do I2P para Android, que contém as mesmas bibliotecas, além de utilitários específicos do Android. Em breve vou atualizá-la para que passe a depender das novas bibliotecas do I2P, de modo que as aplicações multiplataforma possam funcionar nativamente com o I2P para Android ou com o I2P para desktop.

## Get hacking!

Consulte nosso guia de desenvolvimento de aplicativos para obter ajuda para começar a usar essas bibliotecas. Você também pode conversar conosco sobre elas no #i2p-dev, no IRC. E, se você começar a usá-las, conte-nos no que você está trabalhando usando a hashtag #I2PSummer no Twitter!
