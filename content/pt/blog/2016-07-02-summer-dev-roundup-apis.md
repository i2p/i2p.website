---
title: "Retrospectiva de desenvolvimento do verão: APIs"
date: 2016-07-02
author: "str4d"
description: "No primeiro mês do Summer Dev, melhoramos a usabilidade de nossas APIs para desenvolvedores de Java, Android e Python."
categories: ["summer-dev"]
---

Summer Dev está a todo vapor: temos estado ocupados lubrificando as engrenagens, lixando as arestas e colocando a casa em ordem. Agora é hora do nosso primeiro balanço, em que atualizamos você sobre o progresso que estamos fazendo!

## APIs month

O nosso objetivo para este mês foi "integrar-se" - fazer com que as nossas APIs e bibliotecas funcionem dentro da infraestrutura existente de várias comunidades, de modo que os desenvolvedores de aplicações possam trabalhar com o I2P de forma mais eficiente e os utilizadores não precisem de se preocupar com os detalhes.

### Java / Android

As bibliotecas de cliente do I2P agora estão disponíveis no Maven Central! Isso deve tornar muito mais simples para desenvolvedores Java usarem o I2P em suas aplicações. Em vez de precisarem obter as bibliotecas de uma instalação existente, eles podem simplesmente adicionar o I2P às suas dependências. Atualizar para novas versões também será muito mais fácil.

A biblioteca cliente do I2P Android também foi atualizada para usar as novas bibliotecas do I2P. Isso significa que aplicativos multiplataforma podem funcionar nativamente com o I2P Android ou com o I2P para desktop.

### Java / Android

#### txi2p

O plugin do Twisted `txi2p` agora oferece suporte a portas internas ao I2P e funcionará de forma transparente sobre APIs SAM locais, remotas e com redirecionamento de portas. Consulte a documentação para obter instruções de uso e relate quaisquer problemas no GitHub.

#### i2psocket

A primeira versão (beta) de `i2psocket` foi lançada! É um substituto direto para a biblioteca `socket` padrão do Python que a estende com suporte a I2P por meio da SAM API. Consulte sua página no GitHub para instruções de uso e para relatar quaisquer problemas.

### Python

- zzz has been hard at work on Syndie, getting a headstart on Plugins month
- psi has been creating an I2P test network using i2pd, and in the process has found and fixed several i2pd bugs that will improve its compatibility with Java I2P

## Coming up: Apps month!

Estamos empolgados em trabalhar com o Tahoe-LAFS em julho! Há muito tempo, o I2P abriga uma das maiores grades públicas, usando uma versão com patches do Tahoe-LAFS. Durante o mês de Apps, vamos ajudá-los em seu trabalho contínuo para adicionar suporte nativo a I2P e Tor, para que os usuários do I2P possam se beneficiar de todas as melhorias upstream (projeto principal).

Existem vários outros projetos com os quais conversaremos sobre seus planos de integração com o I2P e ajudaremos no design. Fiquem atentos!

## Take part in Summer Dev!

Temos muitas outras ideias para coisas que gostaríamos de realizar nessas áreas. Se você tem interesse em colaborar no desenvolvimento de software de privacidade e anonimato, projetar sites ou interfaces fáceis de usar, ou escrever guias para usuários, venha conversar conosco no IRC ou no Twitter! Estamos sempre felizes em receber novos integrantes em nossa comunidade.

Vamos publicar aqui à medida que avançamos, mas você também pode acompanhar nosso progresso e compartilhar suas próprias ideias e trabalhos com a hashtag #I2PSummer no Twitter. Que venha o verão!
