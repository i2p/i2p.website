---
title: "Notas de status do I2P de 2006-08-01"
date: 2006-08-01
author: "jr"
description: "Desempenho de rede sólido, com altas taxas de transferência no I2PSnark, estabilidade do transporte NTCP e esclarecimentos sobre a alcançabilidade de eepsites"
categories: ["status"]
---

Oi, pessoal, é hora de algumas notas breves antes da reunião de hoje à noite. Sei que vocês podem ter uma variedade de perguntas ou assuntos para tratar, então vamos seguir um formato mais flexível do que o habitual. Há apenas algumas coisas que quero mencionar primeiro.

* Network status

Parece que a rede está indo muito bem, com enxames de transferências I2PSnark bastante grandes sendo concluídas, e com taxas de transferência bastante substanciais alcançadas em routers individuais - já vi 650KBytes/sec e 17,000 tunnels participantes sem nenhum problema. Routers na extremidade inferior do espectro parecem estar indo bem também, navegando em eepsites(I2P Sites) e irc com tunnels de 2 saltos usando menos de 1KByte/sec em média.

Não é um mar de rosas para todos, mas estamos trabalhando na atualização do comportamento do router para permitir um desempenho mais consistente e utilizável.

* NTCP

O novo transporte NTCP ("novo" tcp) está indo muito bem depois de resolver os problemas iniciais. Para responder a uma pergunta frequente, a longo prazo, tanto NTCP quanto SSU estarão em operação - não voltaremos a usar apenas TCP.

* eepsite(I2P Site) reachability

Lembrem-se, pessoal, que eepsites(I2P Sites) só são acessíveis quando a pessoa que os está operando os mantém no ar - se estiverem fora do ar, não há nada que você possa fazer para acessá-los ;) Infelizmente, nos últimos dias, orion.i2p não tem estado acessível, mas a rede definitivamente ainda está funcionando - talvez dê uma passada em inproxy.tino.i2p ou eepsites(I2P Sites).i2p para suas necessidades de levantamento da rede.

De qualquer forma, há muito mais acontecendo, mas seria um pouco prematuro mencionar isso aqui. Claro, se você tiver alguma dúvida ou preocupação, apareça no #i2p daqui a alguns minutos para a nossa *cof* reunião de desenvolvimento semanal.

Obrigado por nos ajudar a avançar! =jr
