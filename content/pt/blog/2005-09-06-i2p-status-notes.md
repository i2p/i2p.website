---
title: "Notas de status do I2P de 2005-09-06"
date: 2005-09-06
author: "jr"
description: "Atualização semanal abordando o sucesso do lançamento 0.6.0.5, o desempenho do floodfill netDb, os avanços do Syndie com RSS e pet names (sistema Petname), e o novo aplicativo de gerenciamento do addressbook do susidns"
categories: ["status"]
---

Olá, pessoal,


* Index

1) Estado da rede 2) Estado do Syndie 3) susidns 4) ???

* 1) Net status

As many have seen, the 0.6.0.5 release came out last week after a brief 0.6.0.4 rev, and so far, the reliability has been greatly improved, and the net has grown larger than ever. There is still some room for improvement, but it seems that the new netDb is performing as designed. We've even had the fallback tested out - when the floodfill peers are unreachable, routers fall back on the kademlia netDb, and the other day when that scenario occurred, irc and eepsite(I2P Site) reliability was not substantially diminished.

Recebi uma pergunta sobre como a nova netDb (banco de dados de rede do I2P) funciona e publiquei a resposta [1] no meu blog [2]. Como sempre, se alguém tiver alguma dúvida desse tipo, fique à vontade para me enviar, pela lista ou fora dela, no fórum, ou até no seu blog ;)

[1] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1125792000000&expand=true [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 2) Syndie status

Como podem ver em syndiemedia.i2p (e http://syndiemedia.i2p.net/), tem havido bastante progresso ultimamente, incluindo RSS, pet names (apelidos confiáveis), controles administrativos e os primeiros passos de um uso razoável de CSS. A maioria das sugestões do Isamoor também já foi implementada, assim como as do Adam, então, se alguém tiver algo em mente que gostaria de ver lá, por favor me envie uma mensagem!

O Syndie agora está bem próximo da fase beta; quando isso acontecer, será distribuído como um dos aplicativos padrão do I2P e também empacotado como standalone (autônomo), portanto qualquer ajuda será muito bem-vinda. Com as adições mais recentes de hoje (no cvs), fazer skinning (personalização do tema) do Syndie também ficou muito fácil - você pode simplesmente criar um novo arquivo syndie_standard.css no seu diretório i2p/docs/, e os estilos especificados substituirão as configurações padrão do Syndie. Mais informações sobre isso podem ser encontradas no meu blog [2].

* 3) susidns

Susi criou rapidamente mais um aplicativo web para nós - susidns [3]. Ele serve como uma interface simples para gerenciar o aplicativo addressbook - suas entradas, assinaturas, etc. Está com um aspecto muito bom, então, com sorte, poderemos distribuí-lo como um dos aplicativos padrão em breve, mas, por enquanto, é muito fácil obtê-lo do eepsite dela(I2P Site), salvá-lo no seu diretório webapps, reiniciar seu router, e você estará pronto para começar.

[3] http://susi.i2p/?page_id=13

* 4) ???

Embora certamente tenhamos estado focados no lado do aplicativo cliente (e continuaremos a fazê-lo), grande parte do meu tempo ainda está direcionada à operação central da rede, e há coisas empolgantes a caminho - contorno de firewall e NAT com introduções, autoconfiguração do SSU aprimorada, ordenação e seleção avançadas de pares e até um tratamento simples de rotas restritas. Quanto ao site, o HalfEmpty fez algumas melhorias nas nossas folhas de estilo (viva!).

Enfim, há muita coisa acontecendo, mas isso é tudo de que tenho tempo para mencionar no momento; apareça na reunião às 20h UTC e dê um alô :)

=jr
