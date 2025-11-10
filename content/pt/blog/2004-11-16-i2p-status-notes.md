---
title: "Notas de status do I2P de 2004-11-16"
date: 2004-11-16
author: "jr"
description: "Atualização semanal de status do I2P abordando problemas de congestionamento na rede, avanços na biblioteca de streaming, progresso do BitTorrent e planos de lançamento futuros"
categories: ["status"]
---

Olá, pessoal, é terça-feira de novo

## Índice

1. Congestion
2. Streaming
3. BT
4. ???

## 1) Congestionamento

Eu sei, estou quebrando o hábito de chamar o ponto 1 de "Status da rede", mas esta semana "congestionamento" parece apropriado. A própria rede tem se saído bem, mas, à medida que o uso de bittorrent aumentou, as coisas começaram a ficar cada vez mais congestionadas, levando, essencialmente, a um colapso por congestionamento.

Isto era esperado, e apenas reforça o nosso plano - lançar a nova biblioteca de streaming e reformular a nossa gestão de tunnel para termos dados suficientes sobre os pares a usar quando os nossos pares rápidos falharem. Houve alguns outros fatores em jogo nos problemas recentes da rede, mas a maior parte pode ser atribuída ao aumento do congestionamento e às falhas de tunnel resultantes (o que, por sua vez, causou todo o tipo de seleção de pares caótica).

## 2) Streaming

Tem havido muito progresso com a biblioteca de streaming, e montei um proxy Squid ligado a ela, através da live net (rede real), e tenho usado isso com frequência para a minha navegação normal na web. Com a ajuda do mule, também temos submetido os fluxos a cargas bem pesadas, encaminhando o frost e o FUQID pela rede (meu Deus, eu nunca tinha percebido o quão agressivo o frost era antes de fazer isso!). Dessa forma, alguns bugs antigos e significativos foram localizados, e foram adicionados alguns ajustes para ajudar a controlar quantidades enormes de conexões.

Bulk streams (fluxos em massa) também estão funcionando muito bem, com início lento e evitação de congestionamento, e as conexões de envio/resposta rápidas (à la HTTP get+response) estão fazendo exatamente o que deveriam.

Acho que vamos recrutar alguns voluntários para tentar ampliar a implantação nos próximos dias e, com sorte, nos levar ao nível 0.4.2 em breve. Não quero dizer que vai ser tão bom que até lava a louça, e tenho certeza de que haverá erros que escapem, mas parece promissor.

## 3) BT

Tirando os recentes problemas na rede, a adaptação i2p-bt tem avançado a passos largos. Sei que algumas pessoas já baixaram mais de 1 GB de dados por meio dela, e o desempenho tem sido o esperado (devido à antiga biblioteca de streaming, ~4KBps por par no enxame). Eu tento acompanhar o trabalho que está sendo discutido no canal #i2p-bt - talvez o duck possa nos dar um resumo na reunião?

## 4) ???

É isso da minha parte por enquanto. Nos vemos na reunião daqui a alguns minutos.

=jr
