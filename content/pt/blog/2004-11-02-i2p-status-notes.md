---
title: "Notas de status do I2P de 2004-11-02"
date: 2004-11-02
author: "jr"
description: "Atualização semanal de status do I2P cobrindo o estado da rede, otimizações de memória do núcleo, correções de segurança no roteamento de tunnel (túnel), progresso da biblioteca de streaming e desenvolvimentos em e-mail/BitTorrent"
categories: ["status"]
---

Oi, pessoal, é hora da atualização semanal

## Índice:

1. Net status
2. Core updates
3. Streaming lib
4. mail.i2p progress
5. BT progress
6. ???

## 1) Status da rede

Praticamente como antes - um número estável de pares, eepsites(I2P Sites) razoavelmente acessíveis, e irc por horas a fio. Você pode dar uma olhada na acessibilidade de vários eepsites(I2P Sites) por meio de algumas páginas diferentes: - `http://gott.i2p/sites.html` - `http://www.baffled.i2p/links.html` - `http://thetower.i2p/pings.txt`

## 2) Atualizações do núcleo

Para quem frequenta o canal (ou lê os logs do CVS), muita coisa vem acontecendo, embora já faça algum tempo desde o último lançamento. Uma lista completa de alterações desde a versão 0.4.1.3 pode ser encontrada online, mas há duas modificações importantes, uma boa e uma ruim:

A parte boa é que reduzimos drasticamente o churn de memória (alta rotatividade de alocações) causado por todo tipo de criação insana de objetos temporários. Eu finalmente me cansei de ver o GC (garbage collector) enlouquecer enquanto depurava a nova biblioteca de streaming, então, depois de alguns dias de profilagem, ajustes e otimização, as partes mais feias foram limpas.

A má notícia é uma correção de bug relacionada à forma como algumas mensagens roteadas via tunnel são tratadas - havia algumas situações em que uma mensagem era enviada diretamente ao router de destino em vez de ser roteada via tunnel antes da entrega, o que poderia ser explorado por um adversário com alguma habilidade de programação. Agora, em caso de dúvida, roteamos corretamente via tunnel.

Isso pode parecer bom, mas a parte 'ruim' é que isso significa que haverá um aumento na latência devido aos saltos adicionais, embora esses sejam saltos que precisavam ser usados de qualquer maneira.

Também há outras atividades de depuração ocorrendo no núcleo, então ainda não houve um lançamento oficial - o CVS HEAD está em 0.4.1.3-8. Nos próximos dias provavelmente teremos uma versão 0.4.1.4, apenas para resolver tudo isso. Ela não conterá a nova biblioteca de streaming, é claro.

## 3) Biblioteca de streaming

Falando da biblioteca de streaming, tem havido bastante progresso por aqui, e a comparação lado a lado entre as bibliotecas antiga e nova está muito boa. No entanto, ainda há trabalho a fazer e, como eu disse da última vez, não vamos lançar isso às pressas. Isso significa que o cronograma atrasou, provavelmente na faixa de 2–3 semanas. Mais detalhes quando estiverem disponíveis.

## 4) progresso do mail.i2p

Muitas novidades esta semana - proxies de entrada e saída funcionando! Veja www.postman.i2p para mais informações.

## 5) progresso do BT

Tem havido uma intensa atividade recentemente relacionada ao trabalho de portar um cliente BitTorrent, bem como à atualização de algumas configurações do tracker. Talvez possamos obter algumas atualizações dos envolvidos durante a reunião.

## 6) ???

Da minha parte, é isso. Desculpem o atraso, esqueci daquele negócio de horário de verão. Enfim, vejo vocês daqui a pouco.

=jr
