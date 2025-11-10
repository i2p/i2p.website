---
title: "Notas de status do I2P de 2005-02-22"
date: 2005-02-22
author: "jr"
description: "Notas semanais sobre o status do desenvolvimento do I2P abordando o sucesso do lançamento da versão 0.5, a próxima correção de bug 0.5.0.1, estratégias de ordenação dos pares de tunnel e atualizações do azneti2p"
categories: ["status"]
---

Olá, pessoal, é hora da atualização semanal

* Index

1) 0.5 2) Próximos passos 3) azneti2p 4) ???

* 1) 0.5

Como vocês já devem ter ouvido, finalmente lançamos a versão 0.5 e, em geral, ela tem se saído muito bem. Agradeço muito a rapidez com que as pessoas atualizaram — no primeiro dia, 50–75% da rede já estava na 0.5! Graças à rápida adoção, pudemos ver mais rapidamente o impacto das várias mudanças e, por sua vez, encontramos um monte de bugs. Embora ainda haja algumas questões pendentes, vamos disponibilizar uma nova versão 0.5.0.1 ainda esta noite para corrigir as mais importantes.

Como um benefício colateral dos bugs, tem sido interessante ver que routers conseguem lidar com milhares de tunnels ;)

* 2) Next steps

Após a versão 0.5.0.1, pode haver outra compilação para experimentar algumas mudanças na construção de tunnels exploratórios (como usar apenas um ou dois pares not-failing, o restante sendo de alta capacidade, em vez de todos os pares serem not-failing).  Depois disso, avançaremos para a 0.5.1, que melhorará a vazão do tunnel (agrupando várias mensagens pequenas em uma única mensagem de tunnel) e permitirá ao usuário maior controle sobre sua suscetibilidade ao ataque do predecessor.

Esses controles assumirão a forma de estratégias de ordenação e seleção de pares por cliente, uma para o gateway de entrada e o ponto final de saída, e outra para o restante do tunnel.  Esboço preliminar das estratégias que prevejo:  = random (o que temos agora)  = balanced (tentar explicitamente reduzir a frequência com que usamos cada par)  = strict (se alguma vez usarmos A-->B-->C, eles permanecem nessa ordem
            durante tunnels subsequentes [limitado no tempo])  = loose (gerar uma chave aleatória para o cliente, calcular o XOR
            entre essa chave e cada par, e sempre ordenar os pares
            selecionados pela distância em relação a essa chave [limitado no tempo])  = fixed (sempre usar os mesmos pares por MBTF)

De qualquer forma, esse é o plano, embora eu não tenha certeza de quais estratégias serão implementadas primeiro.  Sugestões mais do que bem-vindas :)

* 3) azneti2p

O pessoal lá do azureus tem trabalhado duro em um monte de atualizações, e o snapshot (compilação de teste) b34 mais recente [1] parece trazer algumas correções de bugs relacionadas ao I2P. Embora eu não tenha tido tempo de auditar o código-fonte desde aquele último problema de anonimato que apontei, eles corrigiram aquele bug específico; então, se você estiver se sentindo aventureiro, pegue a atualização deles e experimente!

[1] http://azureus.sourceforge.net/index_CVS.php

* 4) ???

Muita, muita coisa acontecendo, e tenho certeza de que não cheguei nem perto de cobrir tudo. Dá uma passada na reunião daqui a alguns minutos e vê o que está rolando!

=jr
