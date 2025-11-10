---
title: "Notas de status do I2P para 2006-05-02"
date: 2006-05-02
author: "jr"
description: "Melhorias na saúde da rede na 0.6.1.17, progresso contínuo na reformulação do Syndie, e próximas otimizações do router"
categories: ["status"]
---

Olá, pessoal, lá vem a terça-feira de novo

* Index

1) Estado da rede 2) Estado do Syndie 3) ???

* 1) Net status

Após mais uma semana com o 0.6.1.17, várias das principais métricas de saúde da rede continuam em boa forma. No entanto, estamos vendo alguns dos problemas remanescentes se propagarem até a camada de aplicação, principalmente o recente aumento de reconexões nos servidores irc2p. Postman, cervantes, Complication e eu temos investigado vários aspectos do comportamento da rede em relação ao desempenho visível ao usuário, e identificamos e implementamos algumas melhorias (o CVS HEAD atual é 0.6.1.17-4). Ainda estamos monitorando seu comportamento e experimentando alguns ajustes antes de lançá-lo como 0.6.1.18, mas isso provavelmente acontecerá em poucos dias.

* 2) Syndie status

Conforme mencionado anteriormente, o syndie está a ser profundamente reformulado. Quando digo profundamente, quero dizer quase completamente redesenhado e reimplementado ;) A framework está montada (incluindo testes contínuos com gcj), e as primeiras peças estão a ganhar forma, mas ainda está longe de estar funcional. Quando estiver numa fase em que mais pessoas possam ajudar a impulsioná-lo (e, hum, *usá-lo*), haverá mais informações disponíveis, mas, neste momento, a reformulação do syndie é basicamente algo que ficou em segundo plano enquanto trabalhamos nas melhorias do router.

* 3) ???

É basicamente isso para relatar no momento - como sempre, se tiver algo para comentar, passe na reunião daqui a alguns minutos e dê um oi!

=jr
