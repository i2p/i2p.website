---
title: "Expiração de Introduzer"
number: "133"
author: "zzz"
created: "2017-02-05"
lastupdated: "2017-08-09"
status: "Fechado"
thread: "http://zzz.i2p/topics/2230"
target: "0.9.30"
implementedin: "0.9.30"
---

## Visão Geral

Esta proposta visa melhorar a taxa de sucesso para introduções. Veja
[TRAC-TICKET]_.

## Motivação

Os introduzidores expiram após um certo tempo, mas essa informação não é publicada no
[RouterInfo]_. Os roteadores atualmente devem usar heurísticas para estimar quando um
introduzidor não é mais válido.

## Design

Em um [RouterAddress]_ SSU contendo introduzidores, o publicador pode opcionalmente
incluir tempos de expiração para cada introduzidor.

## Especificação

.. raw:: html

  {% highlight lang='dataspec' %}
iexp{X}={nnnnnnnnnn}

  X :: O número do introduzidor (0-2)

  nnnnnnnnnn :: O tempo em segundos (não ms) desde a época.
{% endhighlight %}

Notas
`````
* Cada expiração deve ser maior que a data de publicação do [RouterInfo]_,
  e menor que 6 horas após a data de publicação do RouterInfo.

* Roteadores publicadores e introduzidores devem tentar manter o introduzidor válido
  até a expiração, no entanto, não há maneira de garantir isso.

* Os roteadores não devem utilizar um introduzidor publicado após sua expiração.

* As expirações dos introduzidores estão no mapeamento do [RouterAddress]_.
  Elas não são o campo de expiração de 8 bytes (atualmente não usado) no [RouterAddress]_.

Exemplo: ``iexp0=1486309470``

## Migração

Sem problemas. A implementação é opcional.
A compatibilidade retroativa é assegurada, já que roteadores mais antigos irão ignorar parâmetros desconhecidos.

## Referências

.. [RouterAddress]
    {{ ctags_url('RouterAddress') }}

.. [RouterInfo]
    {{ ctags_url('RouterInfo') }}

.. [TRAC-TICKET]
    http://{{ i2pconv('trac.i2p2.i2p') }}/ticket/1352
