---
title: "Notas de Status do I2P de 2005-05-03"
date: 2005-05-03
author: "jr"
description: "Atualização semanal abordando a estabilidade da rede, o sucesso dos testes em tempo real do transporte UDP do SSU, o progresso no compartilhamento de arquivos do i2phex e uma ausência prevista de 3 a 4 semanas"
categories: ["status"]
---

Oi, pessoal, muita coisa para tratar esta semana

* Index

1) Estado da rede 2) Estado do SSU 3) i2phex 4) desaparecido 5) ???

* 1) Net status

Sem grandes mudanças na saúde geral da rede - as coisas parecem bastante estáveis e, embora tenhamos alguns solavancos ocasionais, os serviços parecem estar funcionando bem. Houve muitas atualizações no CVS desde a última versão, mas nenhuma correção de bug crítica que impeça o lançamento. Podemos ter mais uma versão antes da minha mudança, apenas para disponibilizar mais amplamente o que há de mais recente no CVS, mas ainda não tenho certeza.

* 2) SSU status

Você está cansado de me ouvir dizer que houve muitos avanços no transporte UDP? Pois é, paciência — houve muitos avanços no transporte UDP. No fim de semana, saímos dos testes em rede privada e passamos para a rede pública, e cerca de uma dúzia de routers se atualizaram e expuseram os seus endereços SSU — permitindo que fossem alcançáveis via transporte TCP pela maioria dos usuários, mas possibilitando que routers com SSU habilitado se comunicassem via UDP.

Os testes ainda estão em uma fase muito inicial, mas correram muito melhor do que eu esperava. O controle de congestionamento se comportou muito bem e tanto a vazão quanto a latência foram bastante adequadas - conseguiu identificar corretamente os limites reais de largura de banda e compartilhar esse link de forma eficaz com fluxos TCP concorrentes.

Com as estatísticas coletadas pelos voluntários prestativos, ficou claro quão importante é o código de reconhecimento seletivo para o correto funcionamento em redes altamente congestionadas. Passei os últimos dias implementando e testando esse código e atualizei a especificação do SSU [1] para incluir uma nova técnica SACK eficiente. Isso não será retrocompatível com o código SSU anterior, portanto as pessoas que têm ajudado nos testes devem desativar o transporte SSU até que uma nova compilação esteja pronta para testes (com sorte, nos próximos um ou dois dias).

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 3) i2phex

sirup tem se dedicado intensamente a um port (adaptação) do phex para i2p, e embora ainda haja muito trabalho a fazer antes de estar pronto para o usuário comum, mais cedo esta noite consegui iniciá-lo, navegar pelos arquivos compartilhados do sirup, obter alguns dados e usar sua interface de chat *cof* "instantâneo".

Há muito mais informações no eepsite do sirup (Site I2P) [2], e a ajuda com testes por pessoas que já fazem parte da comunidade i2p seria ótima (mas, por favor, até que o sirup o aprove como um lançamento público, e o i2p esteja pelo menos na versão 0.6, se não 1.0, vamos manter isso dentro da comunidade i2p). Acredito que o sirup estará por perto na reunião desta semana, então talvez possamos obter mais informações na ocasião!

[2] http://sirup.i2p/

* 4) awol

Falando em estar por aqui, provavelmente não estarei na reunião da próxima semana e ficarei offline pelas próximas 3-4 semanas. Embora isso provavelmente signifique que não haverá novos lançamentos, ainda há uma série de coisas realmente interessantes para as pessoas trabalharem:  = aplicações como feedspace, i2p-bt/ducktorrent, i2phex, fire2pe,     o addressbook, susimail, q, ou algo totalmente novo.  = o eepproxy - seria ótimo ter filtragem, suporte a     conexões HTTP persistentes, ACLs de 'listen on', e talvez um     backoff exponencial para lidar com timeouts do outproxy (em vez de     round robin simples)  = o PRNG (como discutido na lista)  = uma biblioteca de PMTU (em Java ou em C com JNI)  = a recompensa de testes unitários e a recompensa de GCJ  = perfilamento e ajuste de memória do router  = e muito mais.

Então, se você estiver entediado e quiser ajudar, mas estiver precisando de inspiração, talvez uma das opções acima ajude você a começar. Provavelmente vou passar por um cibercafé de vez em quando, então estarei acessível por e-mail, mas o tempo de resposta será O(dias).

* 5) ???

Ok, isso é praticamente tudo o que eu tenho para abordar por enquanto. Para quem quiser ajudar nos testes do SSU durante a próxima semana, fiquem atentos às informações no meu blog [3]. Para o restante de vocês, nos vemos na reunião!

=jr [3] http://jrandom.dev.i2p/
