---
title: "Notas de status do I2P de 2005-02-01"
date: 2005-02-01
author: "jr"
description: "Weekly I2P development status notes covering 0.5 tunnel encryption progress, new NNTP server, and technical proposals"
categories: ["status"]
---

Olá, pessoal, hora do status semanal

* Index

1) status 0.5 2) nntp 3) propostas técnicas 4) ???

* 1) 0.5 status

Houve muitos avanços no âmbito da versão 0.5, com um grande lote de commits ontem.  A maior parte do router agora usa a nova criptografia de tunnel e o tunnel pooling [1], e tem funcionado bem na rede de teste.  Ainda há algumas peças-chave por integrar, e o código obviamente não é compatível com versões anteriores, mas espero que possamos fazer uma implantação em escala mais ampla em algum momento da próxima semana.

Como mencionado anteriormente, a versão 0.5 inicial fornecerá a base sobre a qual diferentes estratégias de seleção/ordenação de pares de tunnel podem operar. Começaremos com um conjunto básico de parâmetros configuráveis para os pools exploratório e de cliente, mas versões posteriores provavelmente incluirão outras opções para diferentes perfis de usuário.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) nntp

Como mencionado no site do LazyGuy [2] e no meu blog [3], temos um novo servidor NNTP em funcionamento na rede, acessível em nntp.fr.i2p. Enquanto o LazyGuy iniciou alguns scripts do suck [4] para ler algumas listas do gmane, o conteúdo é, em grande parte, de, para e por usuários de I2P.  jdot, LazyGuy e eu pesquisamos quais leitores de notícias poderiam ser usados com segurança, e parece haver soluções bem simples. Veja meu blog para instruções sobre como executar o slrn [5] para fazer leitura e publicação anônimas de notícias.

[2] http://fr.i2p/ [3] http://jrandom.dev.i2p/ [4] http://freshmeat.net/projects/suck/ [5] http://freshmeat.net/projects/slrn/

* 3) tech proposals

Orion e outros publicaram uma série de RFCs sobre várias questões técnicas no wiki do ugha [6] para ajudar a detalhar alguns dos problemas mais difíceis no nível de cliente e de aplicação. Por favor, usem esse espaço para discutir questões de nomenclatura, atualizações do SAM, ideias de swarming (enxameamento) e afins — quando publicarem lá, todos nós poderemos colaborar em nosso próprio espaço para obter um resultado melhor.

[6] http://ugha.i2p/I2pRfc

* 4) ???

É tudo o que tenho por enquanto (ainda bem, já que a reunião começa em instantes). Como sempre, poste suas ideias quando e onde quiser :)

=jr
