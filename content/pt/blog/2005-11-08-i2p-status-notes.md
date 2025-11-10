---
title: "Notas de status do I2P de 2005-11-08"
date: 2005-11-08
author: "jr"
description: "Atualização semanal abrangendo estabilidade da versão 0.6.1.4, roteiro de otimização de desempenho, lançamento do I2Phex 0.1.1.35, desenvolvimento do cliente BitTorrent I2P-Rufus, progresso do I2PSnarkGUI e reformulações da interface do usuário do Syndie"
categories: ["status"]
---

Olá, pessoal, terça-feira de novo

* Index

1) Estado da rede / roteiro de curto prazo 2) I2Phex 3) I2P-Rufus 4) I2PSnarkGUI 5) Syndie 6) ???

* 1) Net status / short term roadmap

A 0.6.1.4 ainda parece bastante sólida, embora tenha havido algumas correções de bugs no CVS desde então. Também adicionei algumas otimizações para o SSU transferir dados de forma mais eficiente, o que espero que tenha um impacto perceptível na rede assim que estiver amplamente implantado. Estou adiando a 0.6.1.5 por enquanto, porém, pois há algumas outras coisas que quero incluir na próxima versão. O plano atual é lançá-la neste fim de semana, então fiquem atentos às últimas novidades.

A versão 0.6.2 incluirá muitas melhorias para enfrentar adversários ainda mais fortes, mas uma coisa que não será afetada é o desempenho. Embora o anonimato seja certamente o objetivo central do I2P, se a taxa de transferência e a latência forem ruins, não teremos usuários. Assim, meu plano é levar o desempenho ao nível necessário antes de prosseguir com a implementação das estratégias de ordenação de pares da 0.6.2 e das novas técnicas de criação de tunnel.

* 2) I2Phex

Ultimamente também tem havido muita atividade no âmbito do I2Phex, com uma nova versão 0.1.1.35 [1]. Também houve mais alterações no CVS (obrigado, Legion!), então eu não ficaria surpreso em ver uma 0.1.1.36 ainda esta semana.

Também houve bons progressos no âmbito do gwebcache (consulte http://awup.i2p/), embora, até onde sei, ninguém tenha começado a trabalhar na modificação do I2Phex para usar um gwebcache com suporte a I2P (interessado? avise-me!).

[1] http://forum.i2p.net/viewtopic.php?t=1157

* 3) I2P-Rufus

Dizem por aí que defnax e Rawn andam fazendo algum hacking no cliente Rufus BT, mesclando algum código relacionado ao I2P proveniente do I2P-BT. Não sei o status atual do port (adaptação de software), mas parece que ele terá alguns recursos interessantes. Tenho certeza de que saberemos mais quando houver mais a ser divulgado.

* 4) I2PSnarkGUI

Outro rumor que está circulando é que Markus tem feito alguns hacks numa nova GUI em C#... as capturas de tela no PlanetPeer parecem bem legais [2]. Ainda há planos para uma interface web independente de plataforma, mas isso parece muito bom. Tenho certeza de que ouviremos mais do Markus à medida que a GUI avança.

[2] http://board.planetpeer.de/index.php?topic=1338

* 5) Syndie

Também tem havido algumas discussões sobre as reformulações da interface do usuário (UI) do Syndie [3], e espero que vejamos algum progresso nessa frente em breve. dust também está trabalhando intensamente no Sucker, adicionando melhor suporte para agregar mais feeds RSS/Atom ao Syndie, bem como alguns aprimoramentos no próprio SML.

[3] http://syndiemedia.i2p.net:8000/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1131235200000&expand=true

* 6) ???

Muita coisa acontecendo, como sempre. Dê uma passada no #i2p daqui a alguns minutos para a nossa reunião semanal de desenvolvimento.

=jr
