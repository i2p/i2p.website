---
title: "Notas de status do I2P de 2006-01-03"
date: 2006-01-03
author: "jr"
description: "Atualização de Ano Novo cobrindo a estabilidade do lançamento 0.6.1.8, resultados de testes de carga e perfilamento de pares para otimização da taxa de transferência, e uma revisão abrangente de 2005 com prévia do roteiro de 2006"
categories: ["status"]
---

Olá pessoal, Feliz Ano Novo! Vamos retomar nossas notas semanais de status depois de uma semana sem elas -

* Index

1) Status da rede e 0.6.1.8 2) Resultados de testes de carga e perfilamento de pares 3) Retrospectiva de 2005 / Prévia de 2006 / ???

* 1) Net status and 0.6.1.8

Na outra semana disponibilizamos a versão 0.6.1.8, e relatos da comunidade indicam que as modificações do zzz ajudaram bastante, e as coisas parecem bastante estáveis na rede, mesmo com o tráfego de rede substancialmente aumentado ultimamente (a média parece ter dobrado no último mês, de acordo com stats.i2p). I2PSnark também parece estar funcionando muito bem — embora tenhamos esbarrado em alguns percalços, rastreamos e corrigimos a maioria deles em builds (compilações) subsequentes. Não houve muito feedback a respeito da nova interface de blog do Syndie, mas houve um pequeno aumento no tráfego do Syndie (em parte devido à descoberta, pelo protocol, do importador rss/atom do dust :)

* 2) Load testing results and peer profiling

Nas últimas semanas, tenho tentado isolar nosso gargalo de vazão. Os diferentes componentes de software são todos capazes de enviar dados a taxas muito mais altas do que normalmente vemos para comunicação fim a fim sobre I2P, então tenho feito benchmarks deles na rede real com código personalizado para submetê-los a testes de estresse. A primeira bateria de testes, construindo tunnels de entrada de um salto por todos os routers na rede e transmitindo dados por esse tunnel o mais rápido possível, apresentou resultados bastante promissores, com routers lidando com taxas na faixa do que se esperaria que fossem capazes (por exemplo, a maioria lidando apenas com uma média histórica de 4-16KBps, mas outros atingindo 20-120KBps através de um único tunnel). Esse teste foi uma boa linha de base para exploração adicional e mostrou que o processamento do próprio tunnel é capaz de transferir muito mais do que normalmente observamos.

As tentativas de reproduzir aqueles resultados por meio de tunnels reais não foram tão bem-sucedidas. Ou, talvez se possa dizer que foram mais bem-sucedidas, já que mostraram uma taxa de transferência semelhante à que vemos atualmente, o que significava que estávamos no caminho certo. Voltando aos resultados do teste 1hop, modifiquei o código para selecionar pares que identifiquei manualmente como rápidos e executei novamente os testes de carga por meio de tunnels reais com essa seleção de pares "cheating", e embora não tenha chegado à marca de 120KBps, mostrou uma melhora razoável.

Infelizmente, pedir às pessoas que selecionem seus pares manualmente traz sérios problemas tanto para o anonimato quanto, bem, para a usabilidade, mas, munido dos dados de teste de carga, parece haver uma saída. Nos últimos dias tenho testado um novo método de traçar o perfil dos pares segundo a sua velocidade — essencialmente monitorando sua vazão sustentada máxima, em vez de sua latência recente. Implementações ingênuas têm sido bastante bem-sucedidas e, embora não tenha escolhido exatamente os pares que eu teria escolhido manualmente, tem feito um trabalho muito bom. Ainda há algumas arestas a aparar, porém, como garantir que sejamos capazes de promover os tunnels exploratórios para a camada rápida, mas estou realizando alguns experimentos nessa frente no momento.

No geral, acho que estamos nos aproximando do fim deste esforço de melhoria da taxa de transferência, pois estamos pressionando o menor gargalo e ampliando-o. Tenho certeza de que logo esbarraremos no próximo, e isso definitivamente não vai nos dar velocidades normais da Internet, mas deve ajudar.

* 3) 2005 review / 2006 preview / ???

Dizer que 2005 abriu muitos caminhos é um eufemismo - melhoramos o I2P de inúmeras maneiras nas 25 versões do ano passado, a rede cresceu 5 vezes, lançamos vários novos aplicativos cliente (Syndie, I2Phex, I2PSnark, I2PRufus), migramos para a nova rede IRC irc2p do postman e do cervantes, e vimos florescer algumas eepsites(I2P Sites) úteis (como a stats.i2p do zzz, a orion.i2p do orion e os serviços de proxy e monitoramento do tino, só para citar alguns). A comunidade também amadureceu um pouco mais, em grande parte graças aos esforços de suporte do Complication e de outros no fórum e nos canais, e a qualidade e a diversidade dos relatórios de bugs de todos os setores melhoraram substancialmente. O apoio financeiro contínuo daqueles dentro da comunidade tem sido impressionante e, embora ainda não esteja no nível necessário para um desenvolvimento totalmente sustentável, temos uma reserva que pode me manter alimentado durante o inverno.

A todos os que estiveram envolvidos neste último ano, seja tecnicamente, socialmente ou financeiramente, agradecemos a ajuda!

2006 vai ser um grande ano para nós, com a 0.6.2 chegando neste inverno, prevendo o lançamento 1.0 para algum momento na primavera ou no verão, com a 2.0 no outono, se não antes. Este é o ano em que veremos o que podemos fazer, e o trabalho na camada de aplicação será ainda mais crítico do que antes. Então, se você tem algumas ideias, agora é a hora de colocar mãos à obra :)

Enfim, nossa reunião semanal de status vai começar em alguns minutos, então, se houver algo que você queira discutir mais a fundo, apareça no #i2p nos locais de sempre [1] e dê um alô!

=jr [1] http://forum.i2p.net/viewtopic.php?t=952
