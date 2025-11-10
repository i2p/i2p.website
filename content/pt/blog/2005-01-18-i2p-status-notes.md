---
title: "Notas de status do I2P de 2005-01-18"
date: 2005-01-18
author: "jr"
description: "Notas semanais sobre o status do desenvolvimento do I2P cobrindo o status da rede, o design de roteamento de tunnel 0.5, i2pmail.v2 e a correção de segurança do azneti2p_0.2"
categories: ["status"]
---

Olá, pessoal, é hora da atualização semanal

* Index

1) Status da rede 2) 0.5 3) i2pmail.v2 4) azneti2p_0.2 5) ???

* 1) Net status

Hmm, não há muito a relatar aqui - as coisas ainda funcionam como na semana passada, o tamanho da rede continua bem parecido, talvez um pouco maior.  Alguns novos sites interessantes estão surgindo - veja o fórum [1] e o orion [2] para detalhes.

[1] http://forum.i2p.net/viewforum.php?f=16 [2] http://orion.i2p/

* 2) 0.5

Graças à ajuda de postman, dox, frosk e cervantes (e de todos que encaminharam dados via tunnel através de seus routers ;), coletamos estatísticas do tamanho das mensagens de um dia inteiro [3]. Há dois conjuntos de estatísticas lá - altura e largura do zoom. Isso foi motivado pelo desejo de explorar o impacto de diferentes estratégias de preenchimento de mensagens na carga da rede, conforme explicado [4] em um dos rascunhos para o roteamento de tunnel 0.5. (ooOOoo imagens bonitas).

A parte assustadora do que encontrei ao vasculhá-los foi que, usando alguns breakpoints de padding (preenchimento) bem simples, ajustados manualmente, fazer padding até aqueles tamanhos fixos ainda resultaria em mais de 25% da largura de banda desperdiçada. É, eu sei, não vamos fazer isso. Talvez vocês consigam pensar em algo melhor vasculhando aqueles dados brutos.

[3] http://dev.i2p.net/~jrandom/messageSizes/ [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                  tunnel.html?rev=HEAD#tunnel.padding

Na verdade, esse link [4] nos leva ao estado dos planos da versão 0.5 para o roteamento de tunnel. Como Connelly publicou [5], houve muita discussão recentemente no IRC sobre alguns dos rascunhos, com polecat, bla, duck, nickster, detonate e outros contribuindo com sugestões e perguntas incisivas (ok, e alfinetadas ;). Depois de pouco mais de uma semana, deparamo-nos com uma possível vulnerabilidade em [4], envolvendo um adversário que, de alguma forma, conseguia assumir o controle do gateway do tunnel de entrada e que também controlava um dos outros pares mais adiante nesse tunnel. Embora, na maioria dos casos, isso por si só não expusesse o ponto final e fosse, probabilisticamente, difícil de fazer à medida que a rede cresce, ainda é uma droga (tm).

Então entra em cena [6]. Isso elimina esse problema, permite que tenhamos tunnels de qualquer comprimento e resolve a fome mundial [7]. Isso, no entanto, abre outro problema em que um atacante poderia construir ciclos no tunnel, mas, com base numa sugestão [8] que Taral fez no ano passado a respeito dos session tags (etiquetas de sessão) usados no ElGamal/AES, podemos minimizar o dano causado usando uma série de geradores de números pseudoaleatórios sincronizados [9].

[5] http://dev.i2p.net/pipermail/i2p/2005-January/000557.html [6] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                             tunnel-alt.html?rev=HEAD [7] adivinhe qual afirmação é falsa? [8] http://www.i2p.net/todo#sessionTag [9] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                 tunnel-alt.html?rev=HEAD#tunnel.prng

Não se preocupe se o que está acima parecer confuso - você está vendo as entranhas de alguns problemas de design bem espinhosos sendo resolvidos em público. Se o que está acima *não* parecer confuso, entre em contato, pois estamos sempre procurando mais cabeças para destrinchar esse assunto :)

De qualquer forma, como mencionei na lista [10], em seguida eu gostaria de implementar a segunda estratégia [6] para resolver os detalhes restantes.  O plano para a 0.5, no momento, é reunir todas as alterações incompatíveis com versões anteriores - a nova criptografia de tunnel, etc - e lançar isso como 0.5.0, depois, à medida que isso se estabiliza na rede, avançar para as outras partes da 0.5 [11], como ajustar a estratégia de pooling (agrupamento) conforme descrito nas propostas, lançando isso como 0.5.1.  Espero que ainda possamos lançar a 0.5.0 até o fim do mês, mas vamos ver.

[10] http://dev.i2p.net/pipermail/i2p/2005-January/000558.html [11] http://www.i2p.net/roadmap#0.5

* 3) i2pmail.v2

Outro dia o postman publicou um plano de ação preliminar para a próxima geração da infraestrutura de e-mail [12], e ficou muito legal.  Claro, sempre há ainda mais recursos e enfeites que podemos imaginar, mas a arquitetura é bem interessante em muitos aspectos.  Confira o que já foi documentado até agora [13], e entre em contato com o postman com suas ideias!

[12] http://forum.i2p.net/viewtopic.php?t=259 [13] http://www.postman.i2p/mailv2.html

* 4) azneti2p_0.2

Como publiquei na lista [14], o plugin azneti2p original para o azureus tinha uma falha grave de anonimato.  O problema era que, em torrents mistos em que alguns usuários são anônimos e outros não, os usuários anônimos contatavam os usuários não anônimos /diretamente/ em vez de por meio do I2P.  Paul Gardner e o restante dos desenvolvedores do azureus foram bastante ágeis e lançaram uma correção (patch) imediatamente.  O problema que observei não está mais presente no azureus v. 2203-b12 + azneti2p_0.2.

Ainda não analisamos nem auditamos o código para verificar eventuais problemas de anonimato, então "use por sua conta e risco" (Por outro lado, dizemos o mesmo sobre o I2P, antes do lançamento da versão 1.0). Se você estiver disposto, sei que os desenvolvedores do Azureus apreciariam mais feedback e relatórios de bugs sobre o plugin. Vamos, é claro, manter as pessoas informadas se soubermos de quaisquer outros problemas.

[14] http://dev.i2p.net/pipermail/i2p/2005-January/000553.html

* 5) ???

Há muita coisa acontecendo, como você pode ver. Acho que isso é praticamente tudo o que eu tinha para trazer à tona, mas passe na reunião daqui a 40 minutos se houver mais alguma coisa que você queira discutir (ou se só quiser desabafar sobre o que foi dito acima).

=jr
