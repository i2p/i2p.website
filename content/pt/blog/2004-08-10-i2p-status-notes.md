---
title: "Notas de status do I2P de 2004-08-10"
date: 2004-08-10
author: "jr"
description: "Atualização semanal de status do I2P abrangendo o desempenho da versão 0.3.4.1, o balanceamento de carga do outproxy e as atualizações na documentação"
categories: ["status"]
---

Oi pessoal, hora da atualização semanal

## Índice:

1. 0.3.4.1 status
2. Updated docs
3. 0.4 progress
4. ???

## 1) 0.3.4.1 estado

Bem, lançamos a versão 0.3.4.1 no outro dia, e ela tem funcionado muito bem. Os tempos de conexão no IRC têm sido consistentemente de várias horas, e as taxas de transferência também estão muito boas (atingi 25KBps de um eepsite(site no I2P) no outro dia usando 3 fluxos paralelos).

Um recurso realmente bacana adicionado no lançamento 0.3.4.1 (que eu esqueci de incluir no anúncio de lançamento) foi o patch do mule para permitir que o eepproxy faça round-robin (distribuição cíclica) de solicitações não-I2P através de uma série de outproxies. O padrão ainda é usar apenas o squid.i2p outproxy, mas se você abrir seu router.config e alterar a linha clientApp para conter:

```
-e 'httpclient 4444 squid.i2p,www1.squid.i2p'
```
ele encaminhará aleatoriamente cada requisição HTTP por um dos dois outproxies (proxies de saída) listados (squid.i2p e www1.squid.i2p). Com isso, se houver mais algumas pessoas operando outproxies, vocês não ficarão tão dependentes do squid.i2p. Claro, todos vocês já ouviram minhas preocupações a respeito de outproxies, mas ter essa capacidade dá às pessoas mais opções.

Temos observado alguma instabilidade nas últimas horas, mas, com a ajuda de duck e cervantes, identifiquei dois bugs graves e estou testando correções no momento. As correções são significativas, então espero lançar a versão 0.3.4.2 dentro de um ou dois dias, depois de verificar os resultados.

## 2) Documentação atualizada

Temos sido um pouco negligentes em manter a documentação do site atualizada e, embora ainda haja algumas grandes lacunas (por exemplo, a documentação do netDb (banco de dados de rede do I2P) e do i2ptunnel (ferramenta de tunelamento do I2P)), atualizamos recentemente algumas delas (comparações de redes e o FAQ). À medida que nos aproximamos dos lançamentos 0.4 e 1.0, agradeceria se as pessoas pudessem percorrer o site e ver o que pode ser melhorado.

De particular destaque está um Hall da Fama atualizado — finalmente colocamos isso em dia para refletir as generosas doações que vocês fizeram (obrigado!). À medida que avançamos, usaremos esses recursos para remunerar programadores e outros colaboradores, bem como para cobrir quaisquer custos incorridos (por exemplo, provedores de hospedagem, etc.).

## 3) 0.4 progresso

Revisando as anotações da semana passada, ainda temos algumas coisas pendentes para a 0.4, mas as simulações têm corrido muito bem, e a maioria dos problemas do kaffe foi identificada. Seria ótimo, porém, se as pessoas pudessem testar exaustivamente diferentes aspectos do router ou dos aplicativos cliente e reportar quaisquer bugs que encontrarem.

## 4) ???

É tudo o que tenho para abordar no momento - agradeço o tempo que vocês estão dedicando para nos ajudar a avançar, e acho que estamos fazendo ótimo progresso. Claro, se alguém tiver mais alguma coisa sobre a qual queira falar, passem lá na reunião em #i2p às... hã... agora :)

=jr
