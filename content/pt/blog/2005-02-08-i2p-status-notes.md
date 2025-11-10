---
title: "Notas de status do I2P de 2005-02-08"
date: 2005-02-08
author: "jr"
description: "Notas semanais sobre o status do desenvolvimento do I2P, abrangendo as atualizações 0.4.2.6, o progresso em tunnel na 0.5 com filtros de Bloom, i2p-bt 0.1.6 e Fortuna PRNG (gerador pseudoaleatório)."
categories: ["status"]
---

Oi, pessoal, chegou a hora de mais uma atualização

* Index

1) 0.4.2.6-* 2) 0.5 3) i2p-bt 0.1.6 4) fortuna 5) ???

* 1) 0.4.2.6-*

Pode não parecer, mas já faz mais de um mês desde o lançamento da 0.4.2.6 e as coisas ainda estão em muito bom estado. Houve uma série de atualizações bem úteis [1] desde então, mas nada realmente crítico que justificasse lançar uma nova versão. No entanto, no último dia ou dois recebemos algumas correções de bugs muito boas (obrigado, anon e Sugadude!), e se não estivéssemos à beira do lançamento da 0.5, eu provavelmente empacotaria e lançaria. A atualização do anon corrige uma condição de borda na biblioteca de streaming que vinha causando muitos dos timeouts vistos no BT e em outras transferências grandes, então, se você estiver se sentindo aventureiro, pegue o CVS HEAD e experimente. Ou espere pela próxima versão, claro.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) 0.5

Muito, mas muito progresso no front da versão 0.5 (como qualquer um na lista i2p-cvs [2] pode atestar). Todas as atualizações de tunnel e vários ajustes de desempenho foram testados e, embora isso não inclua muito no que diz respeito aos diversos [3] algoritmos de ordenação forçada, cobre o básico. Também integramos um conjunto de filtros de Bloom [4] (sob licença BSD) do XLattice [5], permitindo-nos detectar ataques de repetição sem exigir qualquer uso de memória por mensagem e com praticamente 0ms de sobrecarga. Para atender às nossas necessidades, os filtros foram trivialmente estendidos para decair, de modo que, após um tunnel expirar, o filtro não tenha mais os vetores de inicialização (IVs) que vimos naquele tunnel.

Embora eu esteja tentando incluir o máximo que puder na versão 0.5, também percebo que precisamos esperar o inesperado - ou seja, a melhor maneira de melhorá-la é colocá-la nas suas mãos e aprender com a forma como ela funciona (e não funciona) para você.  Para ajudar com isso, como mencionei antes, vamos lançar uma versão 0.5 (com sorte, na próxima semana), quebrando a compatibilidade com versões anteriores, e depois trabalhar para melhorá-la a partir daí, criando uma versão 0.5.1 quando estiver pronta.

Revendo o roteiro [6], a única coisa adiada para 0.5.1 é a ordenação estrita.  Haverá também melhorias no throttling (limitação de taxa) e no balanceamento de carga ao longo do tempo, tenho certeza, mas acredito que vamos ajustar isso praticamente para sempre.  Foram discutidas outras coisas que eu esperava incluir em 0.5, como a ferramenta de download e o código de atualização com um clique, mas parece que essas também serão adiadas.

[2] http://dev.i2p.net/pipermail/i2p-cvs/2005-February/thread.html [3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                     tunnel-alt.html?rev=HEAD#tunnel.selection.client [4] http://en.wikipedia.org/wiki/Bloom_filter [5] http://xlattice.sourceforge.net/index.html [6] http://www.i2p.net/roadmap

* 3) i2p-bt 0.1.6

duck corrigiu e lançou uma nova versão do i2p-bt (oba!), disponível nos locais de sempre; então baixe a sua enquanto ainda está quente [7]. Entre esta atualização e o patch da biblioteca de streaming do anon, eu praticamente saturei meu uplink (link de subida) enquanto semeava alguns arquivos, então experimente.

[7] http://forum.i2p.net/viewtopic.php?t=300

* 4) fortuna

Como mencionado na reunião da semana passada, smeghead tem trabalhado sem parar em uma série de diferentes atualizações recentemente e, enquanto lutava para fazer o I2P funcionar com o gcj, surgiram alguns problemas de PRNG (gerador de números pseudoaleatórios) realmente horríveis em algumas JVMs, praticamente nos obrigando a resolver a questão de termos um PRNG em que possamos confiar. Tendo recebido retorno do pessoal do GNU-Crypto, embora a implementação deles do Fortuna ainda não tenha sido realmente implantada, ela parece ser a que melhor se adequa às nossas necessidades. Talvez consigamos incluí-la na versão 0.5, mas é provável que seja adiada para a 0.5.1, pois vamos querer ajustá-la para que possa nos fornecer a quantidade necessária de dados aleatórios.

* 5) ???

Muitas coisas acontecendo, e tem havido um pico de atividade no fórum [8] ultimamente também, então tenho certeza de que deixei passar algumas coisas. De qualquer forma, passe na reunião daqui a alguns minutos e diga o que você tem em mente (ou só fique observando e solte uma ironia aleatória)

=jr [8] http://forum.i2p.net/
