---
title: "Teste de Pares IPv6"
number: "126"
author: "zzz"
created: "2016-05-02"
lastupdated: "2018-03-19"
status: "Fechado"
thread: "http://zzz.i2p/topics/2119"
target: "0.9.27"
implementedin: "0.9.27"
---

## Visão Geral

Esta proposta é para implementar Teste de Pares SSU para IPv6.
Implementado na versão 0.9.27.

## Motivação

Não podemos determinar e rastrear de forma confiável se nosso endereço IPv6 está atrás de um firewall.

Quando adicionamos suporte para IPv6 anos atrás, presumimos que o IPv6 nunca estava atrás de firewalls.

Mais recentemente, na versão 0.9.20 (maio de 2015), dividimos internamente o status de alcançabilidade para v4/v6 (ticket #1458).
Confira esse ticket para informações extensivas e links.

Se você tem tanto v4 quanto v6 atrás de firewalls, pode simplesmente forçar essa configuração de firewall na seção de configuração TCP em /confignet.

Não temos teste de pares para v6. É proibido na especificação SSU.
Se não podemos testar regularmente a alcançabilidade v6, não podemos fazer a transição sensata de/para o estado alcançável v6.
O que resta é supor que somos alcançáveis se recebermos uma conexão de entrada,
e supor que não somos se não recebermos uma conexão de entrada por um tempo.
O problema é que, uma vez que você declara que não é alcançável, você não publica seu IP v6,
e então você não receberá mais (depois que o RI expirar no netdb de todos).

## Design

Implementar Teste de Pares para IPv6,
removendo as restrições anteriores de que o teste de pares era permitido apenas para IPv4.
A mensagem de teste de pares já possui um campo para o comprimento do IP.

## Especificação

Na seção de Capacidades da visão geral do SSU, faça a seguinte adição:

Até a versão 0.9.26, o teste de pares não era suportado para endereços IPv6, e
a capacidade 'B', se presente para um endereço IPv6, deve ser ignorada.
A partir da versão 0.9.27, o teste de pares é suportado para endereços IPv6, e
a presença ou ausência da capacidade 'B' em um endereço IPv6
indica suporte real (ou falta de suporte).

Nas seções de Teste de Pares da visão geral do SSU e da especificação SSU, faça as seguintes alterações:

Notas sobre IPv6:
Até a versão 0.9.26, apenas o teste de endereços IPv4 era suportado.
Portanto, toda comunicação Alice-Bob e Alice-Charlie deve ser via IPv4.
A comunicação Bob-Charlie, no entanto, pode ser via IPv4 ou IPv6.
O endereço de Alice, quando especificado na mensagem PeerTest, deve ter 4 bytes.
A partir da versão 0.9.27, o teste de endereços IPv6 é suportado, e a comunicação Alice-Bob e Alice-Charlie pode ser via IPv6,
se Bob e Charlie indicarem suporte com uma capacidade 'B' em seu endereço IPv6 publicado.

Alice envia a solicitação para Bob usando uma sessão existente sobre o transporte (IPv4 ou IPv6) que ela deseja testar.
Quando Bob recebe uma solicitação de Alice via IPv4, Bob deve selecionar um Charlie que anuncie um endereço IPv4.
Quando Bob recebe uma solicitação de Alice via IPv6, Bob deve selecionar um Charlie que anuncie um endereço IPv6.
A comunicação real Bob-Charlie pode ser via IPv4 ou IPv6 (ou seja, independente do tipo de endereço de Alice).

## Migração

Os roteadores podem:

1) Não incrementar sua versão para 0.9.27 ou superior

2) Remover a capacidade 'B' de quaisquer endereços SSU IPv6 publicados

3) Implementar teste de pares IPv6
