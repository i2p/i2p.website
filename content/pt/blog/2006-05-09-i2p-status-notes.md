---
title: "Notas de status do I2P de 2006-05-09"
date: 2006-05-09
author: "jr"
description: "Lançamento 0.6.1.18 com melhorias na estabilidade da rede, novo servidor de desenvolvimento 'baz' e desafios de compatibilidade do GCJ no Windows"
categories: ["status"]
---

Olá, pessoal, terça-feira chega mais uma vez

* Index

1) Status da rede e 0.6.1.18 2) baz 3) ???

* 1) Net status and 0.6.1.18

Depois de mais uma semana de testes e ajustes, lançamos uma nova versão no início da tarde de hoje, que deve nos colocar em um ambiente mais estável a partir do qual possamos fazer melhorias. Provavelmente não veremos muito efeito até que ela esteja amplamente implantada, então talvez tenhamos que esperar alguns dias para ver como as coisas evoluem, mas as medições, é claro, continuarão.

Um aspecto das compilações e lançamentos mais recentes que zzz mencionou outro dia foi que aumentar o número de tunnels de backup agora pode ter um impacto substancial quando feito ao mesmo tempo que se reduz o número de tunnels paralelos. Não criamos novas leases até termos um número suficiente de tunnels ativos, de modo que os tunnels de backup possam ser rapidamente implantados em caso de falha de um tunnel ativo, reduzindo a frequência de um cliente ficar sem uma lease ativa. Isso é apenas um ajuste em um sintoma, porém, e o lançamento mais recente deve ajudar a tratar a causa raiz.

* 2) baz

"baz", a nova máquina que bar doou finalmente chegou, um laptop amd64 turion (com winxp no disco de inicialização e alguns outros sistemas operacionais em preparação por meio das unidades externas). Tenho trabalhado nele nos últimos dias também, tentando testar algumas ideias de implantação nele. Um problema que estou enfrentando, porém, é fazer o gcj funcionar no Windows. Mais especificamente, um gcj com um gnu/classpath moderno. O que dizem por aí é bastante negativo: ele pode ser compilado nativamente no mingw ou cross-compilado a partir do linux, mas apresenta problemas como falhas de segmentação (segfault) sempre que uma exceção cruza o limite entre DLLs. Então, por exemplo, se java.io.File (localizado em libgcj.dll) lança uma exceção, se ela for capturada por algo em net.i2p.* (localizado em libi2p.dll ou i2p.exe), *poof*, lá se vai o aplicativo.

Pois, não parece muito promissor. O pessoal do gcj ficaria muito interessado se alguém pudesse entrar e ajudar no desenvolvimento para win32, mas um suporte viável não parece nada iminente. Então, parece que teremos de planear continuar a usar uma JVM da Sun no Windows, enquanto damos suporte a gcj/kaffe/sun/ibm/etc em *nix. Suponho que isso não seja assim tão mau, já que são os utilizadores de *nix que têm problemas ao empacotar e distribuir JVMs.

* 3) ???

Ok, já estou atrasado para a reunião, então é melhor eu encerrar isso e ir para a janela do IRC, suponho... até daqui a pouco ;)

=jr
