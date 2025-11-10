---
title: "Agrupar Múltiplos Dentes de Dados em Alho"
number: "115"
author: "orignal"
created: "2015-01-22"
lastupdated: "2015-01-22"
status: "Necessita-Pesquisa"
thread: "http://zzz.i2p/topics/1797"
---

## Visão Geral

Esta proposta trata de enviar múltiplos Dentes de Dados de Alho dentro de uma Mensagem de Alho de ponta a ponta, em vez de apenas um.


## Motivação

Não está claro.


## Alterações Necessárias

As alterações seriam em OCMOSJ e classes auxiliares relacionadas, e em ClientMessagePool. Como não há fila agora, uma nova fila e algum atraso seriam necessários. Qualquer agrupamento teria que respeitar um tamanho máximo de alho para minimizar quedas. Talvez 3KB? Seria interessante instrumentar coisas primeiro para medir com que frequência isso seria utilizado.


## Reflexões

Não está claro se isso terá algum efeito útil, já que o streaming já faz agrupamento e seleciona o MTU ideal. O agrupamento aumentaria o tamanho da mensagem e a probabilidade de queda exponencial.

A exceção é conteúdo não comprimido, comprimido em gzip na camada I2CP. Contudo, o tráfego HTTP já é comprimido em uma camada superior, e os dados do Bittorrent geralmente são incomprimíveis. O que isso deixa? Atualmente, o I2pd não faz a compressão x-i2p-gzip, portanto, isso pode ajudar muito mais lá. Mas o objetivo declarado de não ficar sem tags é melhor resolvido com uma implementação adequada de janelamento em sua biblioteca de streaming.


## Compatibilidade

Isso é compatível com versões anteriores, pois o receptor de alho já processará todos os dentes que receber.
