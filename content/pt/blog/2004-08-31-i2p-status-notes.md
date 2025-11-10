---
title: "Notas de status do I2P de 2004-08-31"
date: 2004-08-31
author: "jr"
description: "Atualização semanal de status do I2P abrangendo a degradação do desempenho da rede, o planejamento do lançamento da versão 0.3.5, as necessidades de documentação e o progresso do Stasher DHT (Tabela Hash Distribuída)"
categories: ["status"]
---

Bem, meninos e meninas, é terça-feira de novo!

## Índice:

1. 0.3.4.3
2. 0.3.5 and 0.4
3. docs
4. stasher update
5. ???

## 1) 0.3.4.3

Bem, como vocês todos já notaram, embora o número de usuários na rede tenha se mantido bastante estável, o desempenho se degradou significativamente nos últimos dias. A origem disso foi uma série de bugs no código de seleção de pares e de entrega de mensagens, expostos quando houve um pequeno DoS na semana passada. O resultado foi que, essencialmente, os tunnels de todos têm falhado constantemente, o que gera um certo efeito bola de neve. Então, não, não é só com você - a rede tem estado horrível para o resto de nós também ;)

Mas a boa notícia é que corrigimos os problemas bem rapidamente, e as correções estão no CVS desde a semana passada, mas a rede ainda continuará ruim para as pessoas até que a próxima versão seja lançada. Dito isso...

## 2) 0.3.5 e 0.4

Embora a próxima versão traga todas as novidades que planejamos para a versão 0.4 (novo instalador, novo padrão de interface web, nova interface do i2ptunnel, bandeja do sistema & serviço do Windows, melhorias no gerenciamento de threads, correções de bugs, etc.), a forma como a última versão se deteriorou ao longo do tempo foi reveladora. Quero que avancemos mais lentamente com esses lançamentos, dando-lhes tempo para se disseminarem mais amplamente e para que os problemas se revelem. Embora o simulador possa explorar o básico, ele não tem como simular os problemas naturais de rede que vemos na rede real (pelo menos, ainda não).

Assim, a próxima versão será a 0.3.5 - com sorte, a última versão 0.3.*, mas talvez não, se surgirem outros problemas. Olhando para trás, para como a rede operava quando eu estava offline em junho, as coisas começaram a se degradar após cerca de duas semanas. Assim, minha ideia é adiar a promoção para o próximo nível de versão 0.4 até que possamos sustentar um alto grau de confiabilidade por pelo menos duas semanas. Isso não significa que não estaremos trabalhando nesse meio tempo, é claro.

De qualquer forma, como mencionado na semana passada, o hypercubus está trabalhando firme no novo sistema de instalação, lidando com eu ficar mudando as coisas e exigindo suporte para sistemas esquisitos. Devemos ter tudo acertado nos próximos dias para lançar uma versão 0.3.5 nos próximos dias.

## 3) documentação

Uma das coisas importantes que precisamos fazer durante aquela "janela de testes" de duas semanas antes da 0.4 é documentar intensamente. O que me pergunto é quais coisas vocês acham que estão faltando na nossa documentação - que perguntas vocês têm que precisamos responder? Embora eu quisesse dizer "ok, agora, vão escrever esses documentos", sou realista, então tudo o que peço é que vocês identifiquem quais assuntos esses documentos abordariam.

Por exemplo, um dos documentos em que estou trabalhando agora é uma revisão do modelo de ameaças, que eu descreveria agora como uma série de casos de uso explicando como o I2P pode atender às necessidades de diferentes pessoas, incluindo a funcionalidade, os atacantes que preocupam essa pessoa e como ela se defende.

Se você não acha que sua pergunta exige um documento completo para ser abordada, simplesmente formule-a como uma pergunta e podemos adicioná-la à FAQ.

## 4) stasher update

Aum apareceu no canal mais cedo hoje com uma atualização (enquanto eu o bombardeava com perguntas):

```
<aum> quick stasher update, with apologies for tomorrow's meeting:
<aum> infinite-level splitfiles working, have successfully
      inserted and retrieved large files
<jrandom> w00t
<aum> splitfile fragmentation/reassembly transparently occuring
      within stasher
<aum> freenet interface working
<jrandom> wow
<jrandom> so FUQID/FIW works?
<aum> use of fcp splitfile commands in freenet clients strictly
      forbidden (at this stage)
<aum> most clients such as fuqid/fiw should allow setting
      extremely large splitfile sizes, which should prevent them
      trying to talk splitfiles
<aum> if not, then i can dummy up something
<jrandom> r0x0r aum, that kicks ass!
<aum> hooks are in for detailed freenet key support
<jrandom> detailed freenet key support?
<aum> yes, specific chk@, ssk@, ksk@
<jrandom> ok great, so they're all verified @ each node, etc?
<aum> no - only verifiable by the requestor
<aum> my thinking is, given KSK@fred = 'mary',
<aum> to store as SHA1(SHA1("KSK@fred")) = E(mary), where key
      for E is SHA1("KSK@fred")
<aum> ie, crypto key is SHA1(uri), and kademlia key is
      SHA1(SHA1(uri))
<jrandom> hm
<aum> so a possessor of the URI can decyrpt, but owner of a
      datastore cannot decrypt (and therefore has plausible
      deniability)
<jrandom> well, ksks are inherently insecure, so thats no big
      loss, but what about ssk?
<deer> <detonate> those keys aren't very large
<aum> SSK as for freenet
<jrandom> so the SSKs are verified at each node?
<aum> except i'm looking to use same encryption over the top
<aum> not feasible to verify SSK at the target node
<jrandom> why not?  freenet does
<aum> well maybe it is feasible,
<aum> i guess i shouldn't be so lazy
<aum> i was trying to keep the kademlia and freenet layers
      separate
<jrandom> heh, you're not being lazy, there's a truckload of
      work here, and you're doing a great job
<aum> verifying on target node will cause some pathological
      couplings between the two layers, and force deviation
      from pure kademlia
<jrandom> i dont think its possible to do SSKs or CHKs
      securely without having the node validate the key
      properties
<aum> not correct
<aum> fred asks mary, 'gimme SSK@madonna'
<aum> mary sends back what she thinks is 'SSK@madonna'
<aum> fred tests it, barfs, then goes on to ask the next node
<aum> anyway, i MUST go - but am open to continuing discussion
      over email, or tomorrow
<aum> bbl guys
<jrandom> mallory floods the net with 'SSK@madonna' ==
      'sexDrugsRockNRoll'
<jrandom> l8r aum
```
Então, como você pode ver, muito, mas muito progresso. Mesmo que as chaves sejam validadas acima da camada DHT, isso é irado demais (na minha humilde opinião). Vai, aum!

## 5) ???

Ok, é tudo que eu tenho a dizer (o que é bom, já que a reunião começa daqui a alguns instantes)... passa lá e diz o que quiser!

=jr
