---
title: "Notas de status do I2P de 2004-10-12"
date: 2004-10-12
author: "jr"
description: "Atualização semanal de status do I2P abrangendo o lançamento da versão 0.4.1.2, experimentos de controle dinâmico de taxa, desenvolvimento da biblioteca de streaming para a versão 0.4.2 e discussões por e-mail"
categories: ["status"]
---

Olá, pessoal, é hora da nossa atualização semanal

## Índice:

1. 0.4.1.2
2. 0.4.1.3
3. 0.4.2
4. mail discussions
5. ???

## 1) 0.4.1.2

A nova versão 0.4.1.2 saiu há alguns dias e as coisas têm corrido mais ou menos como esperado - houve alguns percalços com o novo componente watchdog (mecanismo de supervisão), no entanto, fazendo com que ele mate o seu router quando as coisas ficam ruins em vez de reiniciá-lo. Como mencionei mais cedo hoje, estou procurando pessoas para usar a nova ferramenta de registro de estatísticas para me enviar alguns dados, então a sua ajuda nisso seria muito bem-vinda.

## 2) 0.4.1.3

Haverá outro lançamento antes de 0.4.2 sair, pois quero que a rede esteja o mais sólida possível antes de avançar. O que estou experimentando no momento é uma limitação dinâmica na participação em tunnel - dizendo aos routers para rejeitar probabilisticamente solicitações se estiverem sobrecarregados ou se seus tunnels estiverem mais lentos do que o habitual. Essas probabilidades e limites são calculados dinamicamente a partir das estatísticas mantidas - se o seu tempo de teste de tunnel de 10 minutos for maior do que o seu tempo de teste de tunnel de 60 minutos, aceite a solicitação de tunnel com uma probabilidade de 60minRate/10minRate (e, se o seu número atual de tunnels for maior do que o seu número médio de tunnels em 60 minutos, aceite com p=60mRate/curTunnels).

Outro limitador potencial é suavizar a largura de banda nesse sentido - rejeitando tunnels probabilisticamente quando o nosso uso de largura de banda atinge picos. De qualquer forma, a intenção de tudo isso é ajudar a distribuir o uso da rede e equilibrar os tunnels entre mais pessoas. O principal problema que tivemos com o balanceamento de carga tem sido um esmagador *excesso* de capacidade e, assim, nenhum dos nossos gatilhos de "droga, estamos lentos, vamos rejeitar" foi acionado. Espera-se que esses novos mecanismos probabilísticos mantenham as mudanças rápidas sob controle.

Não tenho nenhum plano específico para quando a versão 0.4.1.3 sairá - talvez no fim de semana. Os dados que as pessoas enviarem (acima) devem ajudar a determinar se isso valerá a pena, ou se há outras abordagens mais proveitosas.

## 3) 0.4.2

Como discutimos na reunião da semana passada, trocamos a ordem dos lançamentos 0.4.2 e 0.4.3 - 0.4.2 será a nova streaming lib (biblioteca de streaming), e 0.4.3 será a atualização do tunnel.

Tenho revisto a literatura sobre a funcionalidade de streaming do TCP e há algumas questões interessantes para o I2P. Especificamente, nosso tempo de ida e volta (RTT) elevado aponta para algo como XCP, e provavelmente deveríamos ser bastante agressivos com várias formas de notificação explícita de congestionamento, embora não possamos tirar proveito de algo como a opção de timestamp, já que nossos relógios podem estar defasados em até um minuto.

Além disso, vamos querer garantir que possamos otimizar a streaming lib (biblioteca de streaming) para lidar com conexões de curta duração (nas quais o TCP puro se sai muito mal) - por exemplo, quero ser capaz de ser capaz de enviar pequenas solicitações HTTP GET (<32KB) e pequenas respostas (<32KB) em literalmente três mensagens:

```
Alice-->Bob: syn+data+close
Bob-->Alice: ack+data+close (the browser gets the response now)
Alice-->Bob: ack (so he doesn't resend the payload)
```
De qualquer forma, ainda não foi escrito muito código sobre isso, com o lado do protocolo parecendo bastante semelhante ao TCP e os pacotes algo como uma fusão da proposta de human e da proposta antiga. Se alguém tiver sugestões ou ideias, ou quiser ajudar com a implementação, por favor, entre em contato.

## 4) discussão por e-mail

Tem havido algumas discussões interessantes sobre email dentro (e fora) do I2P - o postman publicou um conjunto de ideias online e está procurando sugestões. Também tem havido discussões relacionadas no #mail.i2p. Talvez possamos pedir ao postman que nos dê uma atualização?

## 5) ???

É isso por enquanto. Dê uma passada na reunião daqui a alguns minutos e traga seus comentários :)

=jr
