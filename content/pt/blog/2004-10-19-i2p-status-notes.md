---
title: "Notas de status do I2P de 2004-10-19"
date: 2004-10-19
author: "jr"
description: "Atualização semanal do estado do I2P abrangendo o lançamento da versão 0.4.1.3, melhorias de desempenho do tunnel, progresso da biblioteca de streaming e o motor de busca do files.i2p"
categories: ["status"]
---

Oi, pessoal, é terça-feira de novo

## Índice

1. 0.4.1.3
2. Tunnel test time, and send processing time
3. Streaming lib
4. files.i2p
5. ???

## 1) 0.4.1.3

A versão 0.4.1.3 saiu há um ou dois dias e parece que a maioria das pessoas atualizou (obrigado!). A rede está funcionando razoavelmente bem, mas ainda não houve um aumento revolucionário na confiabilidade. No entanto, os bugs do watchdog da versão 0.4.1.2 desapareceram (ou pelo menos ninguém os mencionou). Meu objetivo é que esta versão 0.4.1.3 seja o último patch antes da 0.4.2, embora, é claro, se surgir algo grande que precise de correção, lançaremos outro.

## 2) Tempo de teste do Tunnel, e tempo de processamento do envio

As mudanças mais significativas na versão 0.4.1.3 foram nos testes de tunnel - em vez de termos um período de teste fixo (30 segundos!), temos tempos limite muito mais agressivos, derivados do desempenho medido. Isso é bom, pois agora marcamos os tunnels como falhos quando estão lentos demais para fazer qualquer coisa útil. No entanto, isso é ruim, pois às vezes os tunnels ficam temporariamente congestionados e, se os testarmos durante esse período, acabamos marcando como falho um tunnel que, de outra forma, funcionaria.

Um gráfico recente de quanto tempo um teste de tunnel leva em um router:

Esses são, em geral, tempos de teste de tunnel aceitáveis - os testes passam por 4 pares remotos (com tunnels de 2 saltos), o que resulta, na maioria dos casos, em ~1-200ms por salto. No entanto, isso nem sempre é o caso, como você pode ver - às vezes leva da ordem de segundos por salto.

É aí que entra este próximo gráfico - o tempo na fila desde quando um determinado router quis enviar uma mensagem até o momento em que essa mensagem foi descarregada em um socket:

Os 95% superiores, mais ou menos, estão abaixo de 50 ms, mas os picos são terríveis.

Precisamos nos livrar desses picos, bem como contornar situações com mais pares falhando. No estado atual, quando 'aprendemos' que um par está fazendo os nossos tunnels falharem, na verdade não estamos aprendendo nada específico sobre o router deles — esses picos podem fazer até pares de alta capacidade parecerem lentos se pegarmos um deles.

## 3) Biblioteca de streaming

A segunda parte de contornar tunnels com falha será realizada em parte pela streaming lib (biblioteca de streaming) - proporcionando uma comunicação de streaming fim a fim muito mais robusta. Esta discussão não é novidade - a lib fará todos os recursos avançados de que temos falado há algum tempo (e terá sua cota de bugs, é claro). Houve muito progresso nessa frente, e a implementação provavelmente já está 60% concluída.

Mais notícias quando houver mais notícias.

## 4) files.i2p

Ok, temos tido muitos novos eepsites(I2P Sites) ultimamente, o que é sensacional. Eu só queria destacar este em especial, pois ele tem um recurso bem legal para o resto de nós. Se você ainda não visitou o files.i2p, ele é basicamente um mecanismo de busca ao estilo do Google, com um cache dos sites que ele rastreia (assim você pode tanto pesquisar quanto navegar quando o eepsite(I2P Site) estiver offline). Muito legal.

## 5) ???

As notas de status desta semana são bem breves, mas há muita coisa acontecendo - - simplesmente não tenho tempo de escrever mais antes da reunião. Então, dê uma passada no #i2p em alguns minutos e podemos discutir qualquer coisa que eu tenha deixado passar estupidamente.

=jr
