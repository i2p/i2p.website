---
title: "Notas de status do I2P de 2005-04-12"
date: 2005-04-12
author: "jr"
description: "Atualização semanal cobrindo correções no netDb da versão 0.5.0.6, progresso do transporte UDP do SSU, resultados do perfilamento bayesiano de pares e desenvolvimento do Q"
categories: ["status"]
---

Olá, pessoal, hora de atualizar novamente

* Index

1) Estado da rede 2) Estado do SSU 3) Perfilamento Bayesiano de pares 4) Estado do Q 5) ???

* 1) Net status

A versão 0.5.0.6 da semana passada parece ter corrigido os problemas de netDb que vínhamos observando (viva). Sites e serviços estão muito mais confiáveis do que estavam na 0.5.0.5, embora tenha havido alguns relatos de problemas em que um site ou serviço se tornaria inacessível após alguns dias de tempo de atividade.

* 2) SSU status

Tem havido muito progresso no código UDP 0.6, com o primeiro lote de commits já aplicados no CVS. Ainda não é algo que se possa realmente usar, mas os fundamentos já estão estabelecidos. A negociação de sessão funciona bem e a entrega de mensagens semi-confiável funciona como esperado. Ainda há muito trabalho a fazer, casos de teste para escrever e situações fora do comum para depurar, mas é progresso.

Se tudo correr bem, poderemos ter alguns testes alfa na próxima semana, apenas para pessoas que consigam configurar explicitamente seus firewalls/NATs. Gostaria de acertar primeiro a operação geral antes de adicionar o relay handler (manipulador de retransmissão), ajustar o netDb para uma expiração mais rápida de routerInfo e selecionar relays para publicar. Também vou aproveitar esta oportunidade para fazer uma bateria de testes, pois há vários fatores críticos de enfileiramento sendo abordados.

* 3) Bayesian peer profiling

bla tem trabalhado intensamente em algumas revisões sobre como decidimos por quais pares o tunnel passa, e embora bla não tenha conseguido comparecer à reunião, há alguns dados interessantes a relatar:

<+bla> Fiz medições diretas de velocidade de nós: tracei o perfil de cerca de 150 nós usando tunnels OB de comprimento 0, tunnels IB de comprimento 1, batching-interval = 0ms
<+bla> Além disso, acabei de fazer uma estimativa de velocidade _muito_ básica e _preliminar_ usando classificação bayesiana ingênua
<+bla> A última foi feita usando os comprimentos padrão de tunnels expl.
<+bla> A interseção entre o conjunto de nós para os quais tenho "ground truth" (valor de referência), e o conjunto de nós nas medições atuais, é de 117 nós
<+bla> Os resultados não estão _tão_ ruins, mas também não são muito impressionantes
<+bla> Veja http://theland.i2p/estspeed.png
<+bla> A separação básica entre muito lentos/rápidos está mais ou menos ok, mas a separação de maior granularidade entre os pares mais rápidos poderia ser bem melhor
<+jrandom2p> hmm, como os valores reais foram calculados - isso é RTT total ou é RTT/comprimento ?
<+bla> Usando os tunnels expl. normais, é praticamente impossível evitar atrasos de batching.
<+bla> Os valores reais são os de ground-truth: aqueles obtidos usando OB=0 e IB=1
<+bla> (e variance=0, e sem atraso de batching)
<+jrandom2p> os resultados parecem bem bons daqui, porém
<+bla> Os tempos estimados são os obtidos usando inferência bayesiana a partir de tunnels expl. _reais_ de comprimento 2 +/- 1
<+bla> Isso é obtido a partir de 3000 RTTs, registrados ao longo de um período de cerca de 3 horas (isso é bastante tempo)
<+bla> Pressupõe (por enquanto) que a velocidade dos pares é estática. Ainda preciso implementar a ponderação
<+jrandom2p> parece sensacional.  bom trabalho, bla
<+jrandom2p> hmm, então a estimativa deveria ser igual a 1/4 do valor real
<+bla> jrandom: Não: Todos os RTTs medidos (usando os tunnels expl. normais), são corrigidos pelo número de saltos no percurso de ida e volta
<+jrandom2p> ah ok
<+bla> Só depois disso o classificador bayesiano é treinado
<+bla> Por ora, eu agrupo os tempos por salto medidos em 10 classes: 50, 100, ..., 450 ms, e uma classe adicional >500 ms
<+bla> Por exemplo, pequenos atrasos por salto poderiam ser ponderados usando um fator maior, assim como falhas completas (>60000 ms).
<+bla> Embora... 65% dos tempos estimados ficam dentro de 0.5 desvios-padrão do tempo real do nó
<+bla> No entanto, isso precisa ser refeito, já que o desvio-padrão é fortemente influenciado pelas falhas (>60000 ms)

Após discussão adicional, bla apresentou uma comparação com a calculadora de velocidade existente, publicada @ http://theland.i2p/oldspeed.png Espelhos desses pngs estão disponíveis em http://dev.i2p.net/~jrandom/estspeed.png e http://dev.i2p.net/~jrandom/oldspeed.png

(quanto à terminologia, IB = saltos de tunnel de entrada, OB = saltos de tunnel de saída, e, após algum esclarecimento, as medições "ground truth" (de referência) foram obtidas com 1 salto de saída e 0 de entrada, e não o inverso)

* 4) Q status

Aum tem feito muitos progressos no Q também, recentemente trabalhando em uma interface de cliente baseada na web. A próxima versão do Q não será compatível com versões anteriores, pois inclui uma série de novos recursos, mas tenho certeza de que ouviremos mais informações do Aum quando houver mais novidades para compartilhar :)

* 5) ???

É isso por enquanto (preciso finalizar isso antes da hora da reunião). Ah, aliás, parece que vou me mudar mais cedo do que o planejado, então talvez algumas das datas no cronograma mudem enquanto eu estiver em trânsito para onde quer que eu vá parar. Enfim, dá uma passada no canal daqui a alguns minutos para nos bombardear com novas ideias!

=jr
