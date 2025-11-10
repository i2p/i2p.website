---
title: "Notas de status do I2P de 2005-06-21"
date: 2005-06-21
author: "jr"
description: "Atualização semanal abordando o retorno de viagem do desenvolvedor, o progresso do transporte SSU, a conclusão da recompensa de testes unitários e a interrupção de serviço"
categories: ["status"]
---

Olá pessoal, é hora de retomar nossas notas de status semanais

* Index

1) Status do desenvolvedor 2) Status do desenvolvimento 3) Recompensa por testes unitários 4) Interrupção do serviço 5) ???

* 1) Dev[eloper] status

Depois de 4 cidades em 4 países, finalmente estou me estabelecendo e voltando a produzir código. Na semana passada reuni as últimas peças para um laptop, não estou mais indo de sofá em sofá e, embora eu não tenha acesso à internet em casa, há muitos cibercafés por perto, então o acesso é confiável (apenas infrequente e caro).

Esse último ponto significa que não vou ficar no irc tanto quanto antes, pelo menos até o outono (tenho um subaluguel até agosto, mais ou menos, e vou procurar um lugar onde eu possa ter acesso à internet 24/7). Isso, no entanto, não significa que eu vá fazer menos - só vou trabalhar principalmente na minha própria rede de testes, disponibilizando compilações para testes na rede real (e, er, ah sim, lançamentos). Isso significa, porém, que talvez queiramos mover algumas discussões que costumavam acontecer de forma livre no #i2p para a lista [1] e/ou o fórum [2] (ainda leio o histórico do #i2p, no entanto). Ainda não encontrei um lugar razoável para onde eu possa ir para as nossas reuniões de desenvolvimento, então não estarei lá esta semana, mas talvez até a próxima semana eu já tenha encontrado um.

Enfim, já chega de falar de mim.

[1] http://dev.i2p.net/pipermail/i2p/ [2] http://forum.i2p.net/

* 2) Dev[elopment] status

Durante a mudança, tenho trabalhado em duas frentes principais - documentação e o transporte SSU (esta última apenas desde que consegui o laptop). A documentação ainda está em andamento, com um grande e assustador documento de visão geral, além de uma série de documentos menores de implementação (cobrindo coisas como a organização do código-fonte, a interação entre componentes, etc).

O progresso do SSU está indo bem - os novos campos de bits de ACK estão implementados, a comunicação está lidando de forma eficaz com perdas (simuladas), as taxas estão adequadas às várias condições, e eu corrigi alguns dos bugs mais feios que havia encontrado anteriormente. Continuo testando essas mudanças e, quando for apropriado, planejaremos uma série de testes ao vivo na rede, para os quais precisaremos de alguns voluntários para ajudar. Mais novidades nessa frente quando estiverem disponíveis.

* 3) Unit test bounty

Tenho o prazer de anunciar que Comwiz apresentou uma série de patches para reivindicar a primeira fase da recompensa por testes unitários [3]! Ainda estamos acertando alguns detalhes menores dos patches, mas já recebi as atualizações e gerei os relatórios do junit e do clover conforme necessário. Espero que tenhamos os patches no CVS em breve; nesse momento, publicaremos a documentação de testes do Comwiz.

Como o clover é um produto comercial (gratuito para desenvolvedores de OSS [4]), apenas aqueles que tiverem instalado o clover e recebido a sua licença do clover poderão gerar os relatórios do clover. De qualquer forma, publicaremos periodicamente na web os relatórios do clover, para que quem não tiver o clover instalado ainda possa ver o desempenho da nossa suíte de testes.

[3] http://www.i2p.net/bounties_unittest [4] http://www.cenqua.com/clover/

* 4) Service outage

Como muitos provavelmente já notaram, (pelo menos) um dos outproxies está offline (squid.i2p), assim como www.i2p, dev.i2p, cvs.i2p e meu blog. Não são eventos independentes - a máquina que os hospeda está avariada.

=jr
