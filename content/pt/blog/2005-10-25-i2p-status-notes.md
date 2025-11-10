---
title: "Notas de status do I2P de 2005-10-25"
date: 2005-10-25
author: "jr"
description: "Atualização semanal abordando o crescimento da rede para 400-500 pares, integração do Fortuna PRNG, suporte à compilação nativa com GCJ, cliente de torrent leve i2psnark e análise do ataque de bootstrap ao tunnel"
categories: ["status"]
---

Oi, pessoal, mais notícias da linha de frente

* Index

1) Estado da rede 2) Integração do Fortuna 3) Estado do GCJ 4) i2psnark está de volta 5) Mais sobre o bootstrapping (processo de inicialização) 6) Investigações sobre vírus 7) ???

* 1) Net status

A semana passada foi bastante boa na rede - as coisas parecem bastante estáveis, com a taxa de transferência normal, e a rede continua a crescer para a faixa de 400–500 pares. Também houve algumas melhorias significativas desde a versão 0.6.1.3 e, como elas afetam o desempenho e a confiabilidade, espero que tenhamos uma versão 0.6.1.4 ainda esta semana.

* 2) Fortuna integration

Graças à correção rápida de Casey Marshall [1], conseguimos integrar o gerador de números pseudoaleatórios Fortuna [2] do GNU-Crypto. Isso elimina a causa de muita frustração com a Blackdown JVM e nos permite trabalhar sem problemas com o GCJ. Integrar a Fortuna ao I2P foi um dos principais motivos pelos quais smeghead desenvolveu "pants" (um 'portage' baseado em 'ant'), então agora tivemos mais um uso bem-sucedido de pants :)

[1] http://lists.gnu.org/archive/html/gnu-crypto-discuss/2005-10/msg00007.html [2] http://en.wikipedia.org/wiki/Fortuna

* 3) GCJ status

Como mencionado na lista [3], agora podemos executar o router e a maioria dos clientes de forma transparente com o GCJ [4]. O próprio console web ainda não está funcionando completamente, então você precisa fazer a configuração do seu próprio router com o router.config (embora deva simplesmente funcionar e iniciar seus tunnels após cerca de um minuto). Não tenho total certeza de como o GCJ se encaixará em nossos planos de lançamento, embora no momento eu esteja inclinado a distribuir java puro, mas dar suporte tanto a java quanto a versões compiladas nativamente. É um pouco trabalhoso ter que compilar e distribuir muitas compilações diferentes para diferentes sistemas operacionais e versões de bibliotecas, etc. Alguém tem alguma opinião forte quanto a isso?

Outra característica positiva do suporte ao GCJ é a capacidade de usar a biblioteca de streaming a partir de C/C++/Python/etc. Não sei se alguém está trabalhando nesse tipo de integração, mas provavelmente valeria a pena; então, se você estiver interessado em trabalhar nessa frente, por favor, me avise!

[3] http://dev.i2p.net/pipermail/i2p/2005-October/001021.html [4] http://gcc.gnu.org/java/

* 4) i2psnark returns

Embora o i2p-bt tenha sido o primeiro cliente bittorrent portado para o I2P a ser amplamente utilizado, o eco saiu na frente com seu port (adaptação) do snark [5] há muito tempo. Infelizmente, ele não se manteve atualizado nem manteve compatibilidade com os outros clientes bittorrent anônimos, então meio que desapareceu por um tempo. Na semana passada, porém, eu estava tendo dificuldades para lidar com problemas de desempenho em algum ponto da cadeia i2p-bt<->sam<->streaming lib<->i2cp, então passei para o código original do snark do mjw e fiz um port simples [6], substituindo quaisquer chamadas java.net.*Socket por chamadas I2PSocket*, InetAddresses por Destinations e URLs por chamadas EepGet. O resultado é um pequeno cliente bittorrent de linha de comando (cerca de 60KB compilado) que agora será distribuído com o I2P.

Ragnarok já começou a hackear o código para aprimorar seu algoritmo de seleção de blocos, e esperamos adicionar tanto uma interface web quanto suporte a multi-torrent antes do lançamento da versão 0.6.2. Se você tiver interesse em ajudar, entre em contato! :)

[5] http://klomp.org/snark/ [6] http://dev.i2p.net/~jrandom/snark_diff.txt

* 5) More on bootstrapping

A lista de discussão tem estado bastante ativa ultimamente, com as novas simulações do Michael e a análise da construção do tunnel. A discussão ainda está em andamento, com algumas boas ideias de Toad, Tom e polecat, então confira se você quiser opinar sobre os trade-offs envolvidos em algumas questões de design relacionadas ao anonimato que vamos reformular para a versão 0.6.2 [7].

Para quem se interessa por um pouco de atrativo visual, Michael também tem algo para você, com uma simulação de quão provável é que o ataque consiga identificar você - em função da porcentagem da rede que eles controlam [8], e em função de quão ativo está o seu tunnel [9]

(bom trabalho, Michael, obrigado!)

[7] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html     (consulte o tópico "i2p tunnel bootstrap attack") [8] http://dev.i2p.net/~jrandom/fraction-of-attackers.png [9] http://dev.i2p.net/~jrandom/messages-per-tunnel.png

* 6) Virus investigations

Tem havido alguma discussão sobre a possível distribuição de malware junto com um determinado aplicativo habilitado para I2P, e Complication fez um excelente trabalho investigando a fundo. Os dados estão disponíveis, então você pode tirar suas próprias conclusões. [10]

Obrigado, Complication, por toda a sua pesquisa sobre isso!

[10] http://forum.i2p.net/viewtopic.php?t=1122

* 7) ???

Tem muita coisa acontecendo, como você pode ver, mas como já estou atrasado para a reunião, acho que é melhor eu salvar isso e enviar, né? Nos vemos em #i2p :)

=jr
