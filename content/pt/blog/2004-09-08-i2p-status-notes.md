---
title: "Notas de status do I2P de 2004-09-08"
date: 2004-09-08
author: "jr"
description: "Atualização semanal de status do I2P abrangendo o lançamento da versão 0.4, problemas de capacidade da rede, atualizações do site e melhorias na interface do I2PTunnel"
categories: ["status"]
---

Olá a todos, desculpem o atraso...

## Índice:

1. 0.4
2. Capacity and overload
3. Website updates
4. I2PTunnel web interface
5. Roadmap and todo
6. ???

## 1) 0.4

Como tenho certeza de que todos vocês viram, a versão 0.4 saiu outro dia e, no geral, está indo muito bem. É difícil acreditar que já se passaram 6 meses desde o lançamento da versão 0.3 (e um ano desde que o SDK 1.0 foi lançado), mas avançamos muito, e o trabalho árduo de vocês, o entusiasmo e a paciência fizeram maravilhas. Parabéns e obrigado!

Como qualquer bom lançamento, assim que foi lançado encontramos alguns problemas e, nos últimos dias, temos recebido relatórios de bugs e estamos corrigindo-os freneticamente (você pode acompanhar as mudanças conforme são corrigidas). Ainda temos mais alguns bugs para eliminar antes de lançar a próxima revisão, mas isso deve ser concluído em um dia ou dois.

## 2) Capacidade e sobrecarga

Temos observado algumas alocações de tunnels bastante desequilibradas nas últimas versões e, embora algumas delas sejam relacionadas a erros (dois deles corrigidos desde que a 0.4 foi lançada), ainda há uma questão geral de algoritmo em aberto: quando um router deve parar de aceitar mais tunnels?

Algumas revisões atrás, adicionamos código de limitação de taxa para rejeitar solicitações para participar em um tunnel se o router estivesse sobrecarregado (o tempo local de processamento de mensagens excede 1s), e isso ajudou substancialmente. No entanto, há dois aspectos desse algoritmo simples que não são abordados: - quando nossa largura de banda está saturada, o nosso tempo local de processamento ainda pode ser rápido, então continuaríamos a aceitar mais solicitações de tunnel - quando um único par participa em "tunnels demais", quando esses falham, isso prejudica mais a rede.

A primeira questão é resolvida de forma bastante simples, bastando habilitar o limitador de largura de banda (já que a limitação de largura de banda retarda o processamento das mensagens em conformidade com o atraso de largura de banda). A segunda é mais complicada, e é necessário tanto mais pesquisa quanto mais simulação. Estou pensando em algo na linha de rejeitar, de forma probabilística, solicitações de tunnel com base na razão entre os tunnels dos quais participamos e os tunnels solicitados à rede, incluindo algum "fator de gentileza" básico, definindo P(reject) = 0 se estivermos participando de menos do que isso.

Mas, como eu disse, é necessário mais trabalho e simulação.

## 3) Atualizações do site

Agora que temos a nova interface web do I2P, praticamente toda a nossa documentação antiga para usuários finais está obsoleta. Precisamos de ajuda para revisar essas páginas e atualizá-las para descrever como as coisas são agora. Como o duck e outros sugeriram, precisamos de um novo guia de 'kickstart' além do readme de `http://localhost:7657/` — algo para ajudar as pessoas a começar e entrar no sistema.

Além disso, nossa nova interface web tem amplo espaço para a integração de ajuda sensível ao contexto. Como você pode ver no help.jsp incluído, "hmm. provavelmente deveríamos ter algum texto de ajuda aqui."

Provavelmente seria ótimo se pudéssemos adicionar links de 'sobre' e/ou 'solução de problemas' às diferentes páginas, explicando o que elas significam e como usá-las.

## 4) Interface web do I2PTunnel

Chamar a nova interface `http://localhost:7657/i2ptunnel/` de "spartan" seria um eufemismo. Precisamos fazer muito trabalho para deixá-la mais próxima de um estado utilizável - neste momento a funcionalidade existe tecnicamente, mas você realmente precisa saber o que está acontecendo nos bastidores para entendê-la. Acho que o duck pode ter mais algumas ideias sobre isso para apresentar durante a reunião.

## 5) Roteiro e tarefas a fazer

Tenho sido negligente em manter o roadmap atualizado, mas a verdade é que temos mais revisões pela frente. Para ajudar a explicar o que vejo como os "grandes problemas", reuni uma nova lista de tarefas, que entra em algum detalhe sobre cada um deles. Acho que, neste momento, devemos estar bastante abertos a rever as nossas opções e talvez retrabalhar o roadmap.

Uma coisa que esqueci de mencionar naquela lista de tarefas é que, ao adicionar o protocolo de conexão leve, podemos incluir a detecção automática (opcional) do endereço IP. Isso pode ser 'perigoso' (por isso será opcional), mas reduzirá drasticamente o número de pedidos de suporte que recebemos :)

De qualquer forma, as questões postadas na lista de tarefas são aquelas que previmos para diversas versões e, com certeza, nem todas estarão na 1.0 ou mesmo na 2.0. Esbocei algumas diferentes possíveis priorizações/lançamentos, mas ainda não estou fechado nisso. No entanto, se as pessoas puderem identificar outras coisas grandes ao longo do caminho, isso seria muito bem-vindo, já que uma questão não programada é sempre uma dor de cabeça.

## 6) ???

Ok, é tudo o que tenho por agora (ainda bem, já que a reunião começa em alguns minutos). Passe pelo #i2p em irc.freenode.net, www.invisiblechat.com, ou irc.duck.i2p às 21h GMT para continuar a conversa.
