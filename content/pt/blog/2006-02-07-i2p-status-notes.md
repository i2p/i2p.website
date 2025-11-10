---
title: "Notas de status do I2P de 2006-02-07"
date: 2006-02-07
author: "jr"
description: "Progresso nos testes de rede do PRE, otimização de expoente curto para a criptografia ElGamal e I2Phex 0.1.1.37 com suporte a gwebcache"
categories: ["status"]
---

Oi, pessoal, lá vem a terça-feira de novo

* Index

1) Estado da rede
2) _PRE progresso da rede
3) I2Phex 0.1.1.37
4) ???

* 1) Net status

Não tem havido alterações substanciais na rede em produção na última semana, então o estado da rede em produção não mudou muito.  Por outro lado...

* 2) _PRE net progress

Na semana passada comecei a fazer commits de código incompatível com versões anteriores para a versão 0.6.1.10 em um ramo separado no CVS (i2p_0_6_1_10_PRE), e um grupo de voluntários tem ajudado a testar isso. Esta nova rede _PRE não consegue se comunicar com a rede ativa e não oferece anonimato significativo (já que há menos de 10 pares). Com os logs de pen register (registro de metadados de conexão) desses routers, alguns bugs substanciais, tanto no código novo quanto no antigo, foram identificados e corrigidos, embora os testes e as melhorias continuem.

Um aspecto da nova criptografia de criação de tunnel é que o criador deve realizar a pesada criptografia assimétrica para cada salto antecipadamente, enquanto a criação de tunnel antiga fazia a criptografia apenas se o salto anterior concordasse em participar no tunnel. Essa criptografia pode levar 400-1000ms ou mais, dependendo tanto do desempenho da CPU local quanto do comprimento do tunnel (ela faz uma criptografia ElGamal completa para cada salto). Uma otimização atualmente em uso na _PRE net é o uso de um expoente curto [1] - em vez de usar um 'x' de 2048bit como chave ElGamal, usamos um 'x' de 228bit, que é o comprimento sugerido para igualar o esforço do problema do logaritmo discreto. Isso reduziu o tempo de criptografia por salto em uma ordem de grandeza, embora não afete o tempo de descriptografia.

Há muitas opiniões conflitantes sobre o uso de expoentes curtos e, no caso geral, isso não é seguro; mas, pelo que pude apurar, como usamos um primo seguro fixo (Oakley group 14 [2]), a ordem de q deve ser adequada. Se alguém tiver mais considerações nesse sentido, porém, gostaria de ouvir mais.

A grande alternativa é mudar para criptografia de 1024 bits (na qual poderíamos então usar um expoente curto de 160 bits, talvez). Isso pode ser apropriado de qualquer forma e, se as coisas forem difíceis demais com criptografia de 2048 bits na rede _PRE, podemos fazer a mudança dentro da rede _PRE. Caso contrário, podemos aguardar até a versão 0.6.1.10, quando houver uma implantação mais ampla da nova criptografia, para ver se é necessário. Muito mais informações serão fornecidas se tal mudança parecer provável.

[1] "Sobre o acordo de chaves Diffie-Hellman com expoentes curtos" -     van Oorschot, Weiner no EuroCrypt 96.  espelhado em     http://dev.i2p.net/~jrandom/Euro96-DH.ps [2] http://www.ietf.org/rfc/rfc3526.txt

De qualquer forma, há muito progresso na rede _PRE, com a maior parte da comunicação sobre isso ocorrendo no canal #i2p_pre no irc2p.

* 3) I2Phex 0.1.1.37

Complication mesclou e aplicou patches ao código mais recente do I2Phex para suportar gwebcaches (caches web do Gnutella), compatíveis com o port do pycache do Rawn.  Isso significa que os usuários podem baixar o I2Phex, instalá-lo, clicar em "Conectar à rede" e, depois de um ou dois minutos, ele obterá algumas referências a pares I2Phex existentes e entrará na rede.  Acabou a dor de cabeça de gerenciar manualmente os arquivos i2phex.hosts ou compartilhar chaves manualmente (w00t)!  Há dois gwebcaches por padrão, mas eles podem ser alterados, ou um terceiro adicionado, modificando as propriedades i2pGWebCache0, i2pGWebCache1 ou i2pGWebCache2 em i2phex.cfg.

Bom trabalho Complication e Rawn!

* 4) ???

É isso por enquanto, o que também é bom, já que estou atrasado para a reunião :) Nos vemos no #i2p daqui a pouco

=jr
