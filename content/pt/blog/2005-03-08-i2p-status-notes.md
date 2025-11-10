---
title: "Notas de status do I2P em 2005-03-08"
date: 2005-03-08
author: "jr"
description: "Notas semanais sobre o status do desenvolvimento do I2P abrangendo melhorias da versão 0.5.0.2, foco na confiabilidade da rede e atualizações nos serviços de e-mail e BitTorrent"
categories: ["status"]
---

Oi pessoal, é hora da atualização semanal

* Index

1) 0.5.0.2 2) atualizações do mail.i2p 3) atualizações do i2p-bt 4) ???

* 1) 0.5.0.2

Outro dia lançamos a versão 0.5.0.2 e uma boa parte da rede já atualizou (oba!). Estão chegando relatos de que os piores problemas da 0.5.0.1 foram eliminados e, no geral, as coisas parecem estar funcionando bem. Ainda há alguns problemas de confiabilidade, embora a streaming lib (biblioteca de streaming) esteja dando conta (conexões IRC durando 12-24+ horas parecem ser a norma). Tenho tentado rastrear alguns dos problemas restantes, mas seria muito, muito bom se todos se atualizassem o mais rápido possível.

Como as coisas estão para avançarmos, a confiabilidade é soberana. Só depois que uma esmagadora maioria das mensagens que deveriam ter êxito de fato tiver êxito é que haverá trabalho de melhoria da vazão. Além do pré-processador de tunnel por lotes, outra dimensão que talvez queiramos explorar é alimentar os perfis com mais dados de latência. Atualmente usamos apenas mensagens de teste e de gerenciamento de tunnel para determinar a classificação de "velocidade" de cada par, mas provavelmente deveríamos capturar quaisquer RTTs mensuráveis para outras ações, como netDb e até mensagens de cliente fim a fim. Por outro lado, teremos que ponderá-los adequadamente, já que, para uma mensagem fim a fim, não conseguimos separar as quatro parcelas do RTT mensurável (our outbound, their inbound, their outbound, our inbound). Talvez possamos fazer alguns truques com garlic para agrupar uma mensagem direcionada a um dos nossos inbound tunnels junto com algumas mensagens outbound, eliminando os tunnels do outro lado do ciclo de medição.

* 2) mail.i2p updates

Ok, não sei quais atualizações o postman tem reservadas para nós, mas haverá uma atualização durante a reunião. Veja os logs para descobrir!

* 3) i2p-bt update

Não sei que atualizações o duck & gang têm para nós, mas ouvi alguns rumores de progresso no canal.  Talvez consigamos arrancar uma atualização dele.

* 4) ???

Muita, muita coisa acontecendo, mas se houver algo específico que vocês queiram levantar e discutir, apareçam na reunião daqui a alguns minutos.  Ah, e só um lembrete, se vocês ainda não atualizaram, por favor, façam isso o quanto antes (atualizar é absurdamente simples - baixar um arquivo, clicar em um botão)

=jr
