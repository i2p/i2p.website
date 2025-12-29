---
title: "Combinar OBEPs com IBGWs"
number: "138"
author: "str4d"
created: "2017-04-10"
lastupdated: "2017-04-10"
status: "Open"
thread: "http://zzz.i2p/topics/2294"
toc: true
---

## Visão Geral

Esta proposta adiciona uma opção I2CP para túneis de saída que faz com que os túneis sejam escolhidos ou construídos quando uma mensagem é enviada de forma que o OBEP corresponda a um dos IBGWs do LeaseSet para o Destination alvo.


## Motivação

A maioria dos roteadores I2P emprega uma forma de descarte de pacotes para gerenciamento de congestionamento. A implementação de referência usa uma estratégia WRED que leva em consideração tanto o tamanho da mensagem quanto a distância percorrida (veja [documentação tunnel throttling](/docs/specs/implementation/#tunnelthrottling)). Devido a essa estratégia, a principal fonte de perda de pacotes é o OBEP.


## Design

Ao enviar uma mensagem, o remetente escolhe ou constrói um túnel com um OBEP que é o mesmo roteador que um dos IBGWs do destinatário. Ao fazer isso, a mensagem irá diretamente de um túnel para o outro, sem necessidade de ser enviada pela rede entre eles.


## Implicações de Segurança

Este modo efetivamente significaria que o destinatário está selecionando o OBEP do remetente. Para manter a privacidade atual, este modo faria com que os túneis de saída fossem construídos com um salto a mais do que o especificado pela opção outbound.length do I2CP (com o salto final possivelmente estando fora do nível rápido do remetente).


## Especificação

Uma nova opção I2CP é adicionada à [especificação I2CP](/docs/specs/i2cp/):

    outbound.matchEndWithTarget
        Booleano

        Valor padrão: caso específico

        Se verdadeiro, o roteador escolherá túneis de saída para mensagens enviadas durante
        esta sessão de forma que o OBEP do túnel seja um dos IBGWs para o Destination alvo. Se tal túnel não existir, o roteador construirá um.


## Compatibilidade

A compatibilidade retroativa é assegurada, pois os roteadores sempre podem enviar mensagens para si mesmos.


## Implementação

### Java I2P

A construção de túneis e o envio de mensagens são atualmente subsistemas separados:

- BuildExecutor só conhece as opções outbound.* do pool de túneis de saída,
  e não tem visibilidade sobre seu uso.

- OutboundClientMessageOneShotJob só pode selecionar um túnel do pool existente; se uma mensagem do cliente chega e não há túneis de saída, o roteador descarta a mensagem.

Implementar esta proposta exigiria projetar uma maneira para que esses dois
sub-sistemas interajam.

### i2pd

Uma implementação de teste foi concluída.


## Desempenho

Esta proposta tem vários efeitos sobre a latência, RTT e perda de pacotes:

- É provável que na maioria dos casos, este modo exija a construção de um novo túnel
  na primeira mensagem em vez de usar um túnel existente, acrescentando latência.

- Para túneis padrão, o OBEP pode precisar encontrar e conectar-se ao IBGW,
  adicionando latência que aumenta o primeiro RTT (pois isso ocorre após o primeiro
  pacote ter sido enviado). Usando este modo, o OBEP precisaria encontrar e
  conectar-se ao IBGW durante a construção do túnel, adicionando a mesma latência mas
  reduzindo o primeiro RTT (pois isso ocorre antes do primeiro pacote ser enviado).

- O tamanho VariableTunnelBuild atualmente padrão é de 2641 bytes. Assim, é
  esperado que este modo resulte em menor perda de pacotes para tamanhos de mensagens
  médias maiores do que isso.

Mais pesquisas são necessárias para investigar esses efeitos, a fim de decidir
quais túneis padrão se beneficiariam deste modo estando habilitado por padrão.
