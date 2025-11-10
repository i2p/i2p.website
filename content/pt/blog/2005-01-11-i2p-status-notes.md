---
title: "Notas de status do I2P de 2005-01-11"
date: 2005-01-11
author: "jr"
description: "Notas semanais sobre o status do desenvolvimento do I2P, cobrindo o status da rede, o progresso do 0.5, o status do 0.6, azneti2p, o port do FreeBSD e hosts.txt como Rede de Confiança"
categories: ["status"]
---

Olá, pessoal, é hora da atualização semanal

* Index

1) Status da rede
2) Progresso da 0.5
3) Status da 0.6
4) azneti2p
5) fbsd
6) hosts.txt como WoT (Rede de Confiança)
7) ???

* 1) Net status

De modo geral, a rede está a comportar-se bem, embora tenhamos tido alguns problemas com um dos servidores IRC estar offline e com o meu outproxy (proxy de saída) a dar problemas. No entanto, o outro servidor IRC estava (e ainda está) disponível (embora, no momento, não tenha o CTCP desativado - ver [1]), então conseguimos saciar a nossa necessidade de IRC :)

[1] http://ugha.i2p/HowTo/IrcAnonymityGuide

* 2) 0.5 progress

Há progresso, sempre em frente!  Ok, acho que devo entrar em um pouco mais de detalhes do que isso.  Finalmente consegui implementar e testar a nova criptografia de roteamento de tunnel (yay!), mas durante algumas discussões encontramos um ponto onde poderia haver um nível de vazamento de anonimato, então isso está sendo revisado (o primeiro salto saberia que era o primeiro salto, o que é Ruim.  mas realmente muito fácil de corrigir).  Enfim, espero atualizar e publicar em breve a documentação e o código sobre isso, e a documentação sobre o restante da operação de tunnel 0.5 / pooling (agrupamento) / etc será publicada depois.  Mais novidades quando houver mais novidades.

* 3) 0.6 status

(o quê!?)

Mule iniciou investigações sobre o transporte UDP, e temos consultado o zab sobre suas experiências com o código UDP do LimeWire. Está tudo muito promissor, mas ainda há muito trabalho a ser feito (e ainda faltam vários meses no cronograma [2]). Tem alguma inspiração ou sugestão? Participe e ajude a direcionar o esforço para o que precisa ser feito!

[2] http://www.i2p.net/roadmap#0.6

* 4) azneti2p

Quase molhei as calças quando recebi a notícia, mas parece que o pessoal do azureus escreveu um plugin para I2P, permitindo tanto o uso anônimo de trackers quanto comunicação de dados anônima! Múltiplos torrents funcionam dentro de um único destino I2P também, e ele usa o I2PSocket diretamente, permitindo integração estreita com a streaming lib (biblioteca de streaming). O plugin azneti2p ainda está nos estágios iniciais com esta versão 0.1, e há muitas otimizações e melhorias de usabilidade a caminho, mas, se você topa pôr a mão na massa, passe no i2p-bt nas redes IRC da I2P e entre na diversão :)

Para os mais aventureiros, obtenha o azureus mais recente [3], consulte o tutorial de I2P deles [4] e baixe o plugin [5].

[3] http://azureus.sourceforge.net/index_CVS.php [4] http://azureus.sourceforge.net/doc/AnonBT/i2p/I2P_howto.htm [5] http://azureus.sourceforge.net/plugin_details.php?plugin=azneti2p

duck vem tomando medidas heroicas para manter a compatibilidade com o i2p-bt, e há programação frenética em #i2p-bt enquanto escrevo isto, então fique de olho em um novo lançamento do i2p-bt muito em breve.

* 5) fbsd

Graças ao trabalho do lioux, agora há uma entrada no ports do FreeBSD para o i2p [6]. Embora não estejamos realmente procurando ter muitas instalações específicas de distribuição por aí, ele promete mantê-la atualizada quando dermos aviso suficiente sobre um novo lançamento. Isso deve ser útil para o pessoal do fbsd-current - obrigado, lioux!

[6] http://www.freshports.org/net/i2p/

* 6) hosts.txt as WoT

Agora que a versão 0.4.2.6 passou a incluir o addressbook (livro de endereços) do Ragnarok, o processo de manter o seu hosts.txt preenchido com novas entradas está sob o controle de cada usuário.  Além disso, você pode encarar as assinaturas do addressbook como uma versão simplificada de uma rede de confiança - você importa novas entradas de um site em que confia para apresentar você a novos destinos (por padrão, dev.i2p e duck.i2p).

Com essa capacidade surge uma nova dimensão — a possibilidade de as pessoas escolherem para quais sites desejam, essencialmente, apontar no seu hosts.txt e para quais não. Embora haja lugar para o vale-tudo público que ocorria no passado, agora que o sistema de nomes não é apenas teórico, mas, na prática, totalmente distribuído, as pessoas precisarão definir suas próprias políticas sobre a publicação dos destinos de outras pessoas.

A parte importante nos bastidores aqui é que isto é uma oportunidade de aprendizado para a comunidade do I2P.  Antes, tanto o gott quanto eu estávamos tentando ajudar a impulsionar a questão de nomenclatura publicando o site do gott como jrandom.i2p (ele pediu esse site primeiro - eu não, e não tenho qualquer controle sobre o conteúdo desse URL).  Agora podemos começar a explorar como vamos lidar com sites que não estão listados em http://dev.i2p.net/i2p/hosts.txt ou em forum.i2p.  Não estar publicado nesses locais não impede de forma alguma que um site funcione - o seu hosts.txt é apenas o seu livro de endereços local.

Enfim, chega de papo, eu só queria deixar as pessoas cientes para que todos possamos ver o que precisa ser feito.

* 7) ???

Uau, é muita coisa. Semana corrida, e não prevejo que as coisas desacelerem tão cedo. Então, aparece na reunião daqui a alguns minutos e podemos conversar sobre isso.

=jr
