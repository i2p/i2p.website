---
title: "Notas de status do I2P de 2005-08-16"
date: 2005-08-16
author: "jr"
description: "Atualização breve abordando o status do PeerTest, a transição da rede Irc2P, o progresso da GUI do Feedspace e a mudança do horário da reunião para as 20:00 GMT"
categories: ["status"]
---

Olá, pessoal, notas breves hoje

* Index:

1) Estado do PeerTest 2) Irc2P 3) Feedspace 4) meta 5) ???

* 1) PeerTest status

Como mencionado anteriormente, a próxima versão 0.6.1 incluirá uma série de testes para configurar o router de forma mais cuidadosa e verificar se é alcançável (ou indicar o que precisa ser feito) e, embora já tenhamos algum código no CVS há duas builds, ainda faltam alguns ajustes para que funcione tão suavemente quanto o necessário. No momento, estou fazendo algumas pequenas modificações no fluxo de testes documentado [1], adicionando um pacote adicional para verificar se o Charlie é alcançável e adiando a resposta do Bob à Alice até que o Charlie tenha respondido. Isso deve reduzir o número de valores de status "ERR-Reject" desnecessários que as pessoas veem, já que Bob não responderá a Alice até ter um Charlie disponível para testes (e, quando Bob não responde, Alice vê "Unknown" como o status).

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html#peerTesting

Enfim, pois é, é isso - deve sair a versão 0.6.0.2-3 amanhã, publicada como lançamento quando estiver exaustivamente testada.

* 2) Irc2P

Como mencionado no fórum [2], os usuários do I2P que usam IRC precisam atualizar suas configurações para migrar para a nova rede de IRC. Duck ficará offline temporariamente para [redacted], e, em vez de torcer para que o servidor não tenha problemas nesse período, postman e smeghead se prontificaram e construíram uma nova rede de IRC para seu uso. Postman também fez um espelho do tracker do duck e do site i2p-bt em [3], e acho que vi algo na nova rede de IRC sobre a susi iniciando uma nova instância do IdleRPG (consulte a lista de canais para mais informações).

Meus agradecimentos vão para os responsáveis pela antiga rede i2pirc (duck, baffled, the metropipe crew, postman) e para os responsáveis pela nova rede irc2p (postman, arcturus)! Serviços e conteúdo interessantes fazem o I2P valer a pena, e cabe a vocês criá-los!

[2] http://forum.i2p.net/viewtopic.php?t=898 [3] http://hq.postman.i2p/

* 3) Feedspace

Falando nisso, eu estava lendo o blog do frosk outro dia e parece que houve mais progresso no Feedspace — em particular, numa interface gráfica bem legal. Sei que talvez ainda não esteja pronta para testes, mas tenho certeza de que o frosk vai nos mandar algum código quando chegar a hora. Aliás, também ouvi um boato sobre outra ferramenta de blog baseada na web, com foco em anonimato, que está a caminho e que poderá se integrar ao Feedspace quando estiver pronta, mas, de novo, tenho certeza de que ouviremos mais informações sobre isso quando estiver pronta.

* 4) meta

Sendo o bastardo ganancioso que sou, eu gostaria de adiantar um pouco as reuniões - em vez de 9PM GMT, vamos tentar 8PM GMT. Por quê? Porque isso se encaixa melhor no meu horário ;) (os cibercafés mais próximos não ficam abertos até muito tarde).

* 5) ???

Por enquanto é isso - vou tentar estar perto de um cibercafé para a reunião desta noite, então fiquem à vontade para passar no #i2p às *8*P GMT nos servidores irc /new/ {irc.postman.i2p, irc.arcturus.i2p}. Talvez tenhamos um bot changate conectado ao irc.freenode.net - alguém quer executar um?

tchau, =jr
