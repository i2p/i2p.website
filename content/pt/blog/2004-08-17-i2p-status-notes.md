---
title: "Notas de status do I2P de 2004-08-17"
date: 2004-08-17
author: "jr"
description: "Atualização semanal de status do I2P abordando problemas de desempenho da rede, ataques de DoS e o desenvolvimento do DHT Stasher"
categories: ["status"]
---

Olá, pessoal, hora de atualizar

## Índice:

1. Network status and 0.3.4.3
2. Stasher
3. ???

## 1) Estado da rede e 0.3.4.3

Embora a rede tenha estado funcional ao longo da última semana, houve momentos com muitos problemas, levando a uma queda dramática na confiabilidade. A versão 0.3.4.2 ajudou significativamente a resolver um DoS causado por alguma incompatibilidade e problemas de sincronização de tempo - veja o gráfico de requisições ao banco de dados da rede mostrando o DoS (picos fora da escala), que foi interrompido com a introdução da 0.3.4.2. Infelizmente, isso, por sua vez, introduziu seu próprio conjunto de problemas, fazendo com que um número significativo de mensagens fosse retransmitido, como pode ser visto no gráfico de largura de banda. O aumento de carga ali também se deveu a um aumento real na atividade dos usuários, então não é /tão/ exagerado ;) Mas ainda assim, foi um problema.

Nos últimos dias, tenho sido bem egoísta. Testamos e implantamos um monte de correções de bugs em alguns routers, mas ainda não lancei, já que raramente consigo testar a interação das incompatibilidades no software quando executo minhas simulações. Então, vocês ficaram sujeitos a um funcionamento de rede excepcionalmente ruim enquanto eu ajusto as coisas para encontrar maneiras de fazer com que os routers tenham bom desempenho quando muitos routers são ruins. Estamos avançando nessa frente - fazendo perfilamento e evitando pares que exploram o network database (banco de dados da rede), gerenciando as filas de solicitações do network database de forma mais eficiente e impondo diversificação de tunnel.

Ainda não chegamos lá, mas estou otimista. Testes estão sendo executados agora na rede em produção e, quando estiver pronta, haverá uma versão 0.3.4.3 que disponibilizará os resultados.

## 2) Stasher

Aum vem fazendo um trabalho sensacional em seu DHT (tabela hash distribuída) e, embora atualmente tenha algumas limitações significativas, ela parece promissora. Definitivamente ainda não está pronta para uso geral, mas, se você topar ajudar com testes (ou programação :), confira o site e inicie um nó.

## 3) ???

É isso por enquanto. Como a reunião já deveria ter começado há um minuto, é melhor eu encerrar por aqui. Vejo vocês em #i2p!

=jr
