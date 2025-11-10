---
title: "Notas de status do I2P de 2005-08-23"
date: 2005-08-23
author: "jr"
description: "Atualização semanal abordando melhorias da versão 0.6.0.3, status da rede Irc2P, frontend web susibt para i2p-bt e blog seguro com o Syndie"
categories: ["status"]
---

Oi, pessoal, é hora das notas de status semanais novamente

* Index

1) 0.6.0.3 estado 2) IRC estado 3) susibt 4) Syndie 5) ???

* 1) 0.6.0.3 status

Como mencionado no outro dia [1], temos uma nova versão 0.6.0.3 disponível, pronta para seu uso. É uma grande melhoria em relação à versão 0.6.0.2 (não é incomum ficar vários dias sem desconexão no irc - eu já tive tempos de atividade de 5 dias interrompidos por uma atualização), mas há algumas coisas que vale a pena observar. Ainda assim, nem sempre é assim - pessoas com conexões de Internet lentas enfrentam problemas, mas é um avanço.

Uma pergunta (muito) comum tem surgido sobre o código de teste de pares-"Por que aparece Status: Unknown?" Unknown é *perfeitamente normal* - NÃO é indicativo de um problema. Além disso, se às vezes você notar que ele alterna entre "OK" e "ERR-Reject", isso NÃO significa que está tudo certo - se você alguma vez vir ERR-Reject, isso significa que é muito provável que você tenha um problema de NAT ou de firewall. Eu sei que é confuso, e haverá uma versão depois com uma exibição de status mais clara (e resolução automática, quando possível), mas por enquanto, não fique surpreso se eu ignorar você quando você disser "omg tá quebrado!!!11 o status é Unknown!" ;)

(A causa do excesso de valores de status Unknown é que estamos ignorando testes de pares em que "Charlie" [2] é alguém com quem já temos uma sessão SSU, pois isso implica que eles conseguiriam atravessar o nosso NAT mesmo que o nosso NAT esteja com falha)

[1] http://dev.i2p.net/pipermail/i2p/2005-August/000844.html [2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#peerTesting

* 2) IRC status

Como mencionado acima, os operadores do Irc2P fizeram um ótimo trabalho com sua rede, pois a latência caiu muito e a confiabilidade aumentou bastante - faz dias que não vejo um netsplit (divisão da rede). Há também um novo servidor IRC por lá, totalizando 3 - irc.postman.i2p, irc.arcturus.i2p, e irc.freshcoffee.i2p. Talvez alguém do pessoal do Irc2P possa nos atualizar sobre o progresso deles durante a reunião?

* 3) susibt

susi23 (famosa pelo susimail) está de volta com um par de ferramentas relacionadas a bt - susibt [3] e um novo bot de rastreador [4]. susibt é uma aplicação web (facilmente implantável na sua instância jetty do i2p) para gerenciar o funcionamento do i2p-bt. Como diz o site dela:

SusiBT é uma interface web para o i2p-bt. Ela se integra ao seu router i2p e permite uploads e downloads automáticos, retoma após a reinicialização e oferece algumas funcionalidades de gerenciamento, como upload e download de arquivos. Versões posteriores do aplicativo terão suporte à criação e ao envio automáticos de arquivos .torrent.

[3] http://susi.i2p/?page_id=31 [4] http://susi.i2p/?p=33

Posso ouvir um "w00t"?

* 4) Syndie

Como mencionado na lista e no canal, temos um novo aplicativo cliente para blogging / distribuição de conteúdo com segurança e autenticação. Com o Syndie, a pergunta "o seu eepsite(I2P Site) está no ar?" deixa de existir, pois você pode ler o conteúdo mesmo quando o site está fora do ar, mas o Syndie evita todas as questões espinhosas inerentes às redes de distribuição de conteúdo ao focar no frontend. De qualquer forma, ainda está em pleno desenvolvimento, mas, se as pessoas quiserem entrar e experimentar, há um nó público do Syndie em http://syndiemedia.i2p/ (também acessível na web em http://66.111.51.110:8000/). Sinta-se à vontade para entrar lá e criar um blog ou, se estiver se sentindo aventureiro(a), publicar alguns comentários/sugestões/preocupações! Claro, patches são bem-vindos, mas sugestões de funcionalidades também, então manda ver.

* 5) ???

Dizer que há muita coisa acontecendo é até um eufemismo... além do que foi dito acima, estou trabalhando em algumas melhorias no controle de congestionamento do SSU (-1 já está no cvs), no nosso limitador de largura de banda e na netDb (para a inacessibilidade ocasional de sites), além de depurar o problema de CPU relatado no fórum. Tenho certeza de que outros também estão trabalhando em coisas bacanas para relatar, então tomara que apareçam na reunião de hoje à noite para desabafar à vontade :)

Enfim, nos vemos hoje à noite às 20h GMT no #i2p nos servidores de sempre!

=jr
