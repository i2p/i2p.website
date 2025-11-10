---
title: "Notas de status do I2P de 2006-01-31"
date: 2006-01-31
author: "jr"
description: "Desafios de confiabilidade da rede, próximo lançamento 0.6.1.10 com nova criptografia para criação de tunnel (túnel), e mudanças incompatíveis com versões anteriores"
categories: ["status"]
---

Oi, pessoal, terça-feira chega mais uma vez,

* Index

1) Estado da rede 2) estado 0.6.1.10 3) ???

* 1) Net status

Na última semana, tenho testado alguns ajustes diferentes para aumentar a confiabilidade da criação de tunnels na rede em produção, mas ainda não houve um avanço significativo. No entanto, houve algumas mudanças substanciais no CVS, mas não são o que eu chamaria de... estáveis. Então, de modo geral, eu recomendaria que as pessoas usassem a versão mais recente (0.6.1.9, marcada no CVS como i2p_0_6_1_9), ou no máximo tunnels de 1 salto com os builds mais recentes. Por outro lado...

* 2) 0.6.1.10 status

Em vez de lutar indefinidamente com pequenos ajustes, tenho trabalhado na minha rede de testes local para migrar para a nova criptografia e o processo de criação de tunnel [1]. Isso deve resolver grande parte das falhas na criação de tunnel; depois disso, poderemos fazer ajustes adicionais, se necessário.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD

Um efeito colateral infeliz é que a 0.6.1.10 não será compatível com versões anteriores.  Faz tempo que não temos um lançamento incompatível com versões anteriores, mas nos primeiros tempos fizemos isso várias vezes, então não deve ser um grande problema.  Basicamente, depois que funcionar muito bem na minha rede de testes local, vamos implantá-lo em paralelo para algumas almas corajosas para testes iniciais, depois, quando estiver pronto para lançamento, vamos apenas trocar as referências de seed para os seeds da nova rede e botar no ar.

Não tenho previsão para a versão 0.6.1.10, mas, no momento, tudo parece estar indo muito bem (a maioria dos comprimentos de tunnel está funcionando, mas há algumas ramificações que ainda não submeti a testes de estresse).  Mais novidades quando houver mais novidades, claro.

* 3) ???

É basicamente tudo o que tenho para mencionar no momento, embora eu saiba que há coisas em que outros estão trabalhando e eu tenha alguns truques na manga para mais tarde, mas vamos descobrir mais quando for a hora certa. Enfim, até daqui a alguns minutos!

=jr
