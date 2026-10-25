---
title: "Biblioteca Ministreaming"
description: "Notas históricas sobre a primeira camada de transporte semelhante ao TCP do I2P"
slug: "ministreaming"
aliases:
  - "/pt/ministreaming"
  - "/pt/ministreaming/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

## Nota

A biblioteca ministreaming foi aprimorada e estendida pela [biblioteca de streaming](/docs/api/streaming) "completa". O ministreaming está obsoleto e é incompatível com as aplicações atuais. A documentação a seguir é antiga. Note também que o streaming estende o ministreaming no mesmo pacote Java (net.i2p.client.streaming), então a documentação atual da API contém ambos. As classes e métodos obsoletos do ministreaming estão claramente marcados como obsoletos nos Javadocs.

## Biblioteca Ministreaming

A biblioteca ministreaming é uma camada sobre o [I2CP](/docs/protocol/i2cp) principal que permite fluxos confiáveis, ordenados e autenticados de mensagens operarem através de uma camada de mensagens não confiável, desordenada e não autenticada. Assim como a relação entre TCP e IP, esta funcionalidade de streaming tem uma série completa de compromissos e otimizações disponíveis, mas em vez de incorporar essa funcionalidade no código base do I2P, ela foi separada em sua própria biblioteca tanto para manter as complexidades similares ao TCP separadas quanto para permitir implementações alternativas otimizadas.

A biblioteca ministreaming foi escrita por mihi como parte da sua aplicação [I2PTunnel](/docs/api/i2ptunnel) e depois foi separada e lançada sob a licença BSD. É chamada de biblioteca "mini"streaming porque faz algumas simplificações na implementação, enquanto uma biblioteca de streaming mais robusta poderia ser ainda mais otimizada para operação sobre I2P. Os dois principais problemas com a biblioteca ministreaming são o uso do protocolo tradicional de estabelecimento de duas fases do TCP e o tamanho fixo atual da janela de 1. O problema do estabelecimento é menor para streams de longa duração, mas para curtos, como requisições HTTP rápidas, o impacto pode ser significativo. Quanto ao tamanho da janela, a biblioteca ministreaming não mantém nenhum ID ou ordenação dentro das mensagens enviadas (nem inclui qualquer ACK ou SACK a nível de aplicação), então deve aguardar em média duas vezes o tempo necessário para enviar uma mensagem antes de enviar outra.

Mesmo com essas questões, a biblioteca ministreaming tem um desempenho bastante bom em muitas situações, e sua API é tanto bastante simples quanto capaz de permanecer inalterada conforme diferentes implementações de streaming são introduzidas. A biblioteca é implantada em seu próprio ministreaming.jar. Desenvolvedores em Java que gostariam de usá-la podem acessar a API diretamente, enquanto desenvolvedores em outras linguagens podem usá-la através do suporte de streaming do [SAM](/docs/api/samv3).
