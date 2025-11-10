---
title: "O Processo de Proposta do I2P"
number: "001"
author: "str4d"
created: "2016-04-10"
lastupdated: "2017-04-07"
status: "Meta"
thread: "http://zzz.i2p/topics/1980"
---

## Visão Geral

Este documento descreve como mudar as especificações do I2P, como funcionam as propostas do I2P e a relação entre as propostas do I2P e as especificações.

Este documento é adaptado do processo de proposta do Tor, e grande parte do conteúdo abaixo foi originalmente escrito por Nick Mathewson.

Este é um documento informativo.

## Motivação

Anteriormente, nosso processo para atualizar as especificações do I2P era relativamente informal: fazíamos uma proposta no fórum de desenvolvimento e discutíamos as mudanças, então alcançávamos consenso e alterávamos a especificação com rascunhos de mudanças (não necessariamente nesta ordem), e finalmente implementávamos as mudanças.

Isso tinha alguns problemas.

Primeiro, mesmo em sua forma mais eficiente, o antigo processo frequentemente deixava a especificação fora de sincronia com o código. Os piores casos eram aqueles onde a implementação era adiada: a especificação e o código poderiam permanecer fora de sincronia por várias versões.

Segundo, era difícil participar da discussão, já que nem sempre estava claro quais partes do tópico de discussão faziam parte da proposta ou quais mudanças na especificação haviam sido implementadas. Os fóruns de desenvolvimento também são acessíveis apenas dentro do I2P, significando que as propostas poderiam ser vistas apenas por pessoas que usam o I2P.

Terceiro, era muito fácil esquecer algumas propostas porque ficariam enterradas várias páginas atrás na lista de tópicos do fórum.

## Como mudar as especificações agora

Primeiro, alguém escreve um documento de proposta. Ele deve descrever a mudança que deve ser feita em detalhes, e dar alguma ideia de como implementá-la. Uma vez que esteja desenvolvida o suficiente, se torna uma proposta.

Como um RFC, cada proposta recebe um número. Diferente dos RFCs, propostas podem mudar ao longo do tempo e manter o mesmo número, até que sejam finalmente aceitas ou rejeitadas. O histórico de cada proposta será armazenado no repositório do site I2P.

Uma vez que uma proposta esteja no repositório, devemos discuti-la no tópico correspondente e melhorá-la até que tenhamos alcançado consenso de que é uma boa ideia e que está detalhada o suficiente para ser implementada. Quando isso acontece, implementamos a proposta e a incorporamos nas especificações. Assim, as especificações permanecem como a documentação canônica para o protocolo I2P: nenhuma proposta é jamais a documentação canônica para um recurso implementado.

(Este processo é bem similar ao Processo de Melhoria do Python, com a exceção principal de que as propostas do I2P são reintegradas nas especificações após a implementação, enquanto que PEPs *se tornam* a nova especificação.)

### Pequenas mudanças

Ainda é aceitável fazer pequenas mudanças diretamente na especificação se o código puder ser escrito mais ou menos imediatamente, ou mudanças cosméticas se nenhuma mudança de código for necessária. Este documento reflete a *intenção* dos desenvolvedores atuais, não uma promessa permanente de sempre usar este processo no futuro: reservamo-nos o direito de nos entusiasmar e sair correndo para implementar algo em uma sessão de hacking noturna alimentada por cafeína ou M&Ms.

## Como novas propostas são adicionadas

Para submeter uma proposta, publique-a no fórum de desenvolvimento ou entre um ticket com a proposta anexada.

Uma vez que uma ideia tenha sido proposta, um rascunho formatado adequadamente (veja abaixo) exista, e haja um consenso aproximado dentro da comunidade de desenvolvimento ativa de que esta ideia merece consideração, os editores de proposta adicionarão oficialmente a proposta.

Os editores de proposta atuais são zzz e str4d.

## O que deve ir em uma proposta

Toda proposta deve ter um cabeçalho contendo estes campos:

```
:author:
:created:
:thread:
:lastupdated:
:status:
```

- O campo `author` deve conter os nomes dos autores desta proposta.
- O campo `thread` deve ser um link para o tópico do fórum de desenvolvimento onde esta proposta foi originalmente postada, ou para um novo tópico criado para discutir esta proposta.
- O campo `lastupdated` deve ser igual ao campo `created` inicialmente, e deve ser atualizado sempre que a proposta for alterada.

Esses campos devem ser definidos quando necessário:

```
:supercedes:
:supercededby:
:editor:
```

- O campo `supercedes` é uma lista separada por vírgulas de todas as propostas que esta proposta substitui. Essas propostas devem ser Rejeitadas e ter seus campos `supercededby` definidos para o número desta proposta.
- O campo `editor` deve ser definido se mudanças significativas forem feitas nesta proposta que não alterem substancialmente seu conteúdo. Se o conteúdo estiver sendo substancialmente alterado, um autor adicional deve ser adicionado ou uma nova proposta criada substituindo esta.

Esses campos são opcionais, mas recomendados:

```
:target:
:implementedin:
```

- O campo `target` deve descrever em qual versão a proposta espera-se que seja implementada (se estiver Aberta ou Aceita).
- O campo `implementedin` deve descrever em qual versão a proposta foi implementada (se estiver Finalizada ou Fechada).

O corpo da proposta deve começar com uma seção de Visão Geral explicando sobre o que é a proposta, o que ela faz, e em que estado ela está.

Após a Visão Geral, a proposta torna-se mais livre. Dependendo de seu comprimento e complexidade, a proposta pode ser dividida em seções conforme apropriado ou seguir um formato discursivo curto. Toda proposta deve conter pelo menos as seguintes informações antes de ser Aceita, embora as informações não precisem estar em seções com esses nomes.

**Motivação**
: Qual problema a proposta está tentando resolver? Por que este problema é importante? Se várias abordagens forem possíveis, por que escolher esta?

**Design**
: Uma visão de alto nível de quais são os novos ou modificados recursos, como os novos ou modificados recursos funcionam, como eles interagem entre si e como interagem com o restante do I2P. Este é o corpo principal da proposta. Algumas propostas começarão apenas com uma Motivação e um Design, e esperarão por uma especificação até que o Design pareça aproximadamente correto.

**Implicações de segurança**
: Quais efeitos as mudanças propostas podem ter sobre o anonimato, quão bem esses efeitos são compreendidos, e assim por diante.

**Especificação**
: Uma descrição detalhada do que precisa ser adicionado às especificações do I2P para implementar a proposta. Deve ser detalhada o suficiente para que programadores independentes possam escrever implementações compatíveis entre si da proposta com base em suas especificações.

**Compatibilidade**
: As versões do I2P que seguem a proposta serão compatíveis com as versões que não a seguem? Se sim, como a compatibilidade será alcançada? Geralmente, tentamos não perder compatibilidade se possível; não fizemos uma mudança de "flag day" desde março de 2008, e não queremos fazer outra.

**Implementação**
: Se a proposta for complicada de implementar na arquitetura atual do I2P, o documento pode conter alguma discussão sobre como fazê-la funcionar. Patches reais devem ir para branches públicos do monotone, ou ser carregados no Trac.

**Notas de desempenho e escalabilidade**
: Se o recurso tiver um efeito no desempenho (em RAM, CPU, largura de banda) ou escalabilidade, deve haver alguma análise de quão significativo será esse efeito, para que possamos evitar regressões de desempenho muito caras e não perder tempo em ganhos insignificantes.

**Referências**
: Se a proposta referir-se a documentos externos, eles devem ser listados.

## Status da proposta

**Aberto**
: Uma proposta em discussão.

**Aceito**
: A proposta está completa, e pretendemos implementá-la. A partir deste ponto, mudanças substanciais na proposta devem ser evitadas e consideradas um sinal de que o processo falhou em algum lugar.

**Finalizado**
: A proposta foi aceita e implementada. Após este ponto, a proposta não deve ser alterada.

**Fechado**
: A proposta foi aceita, implementada e incorporada aos documentos principais de especificação. A proposta não deve ser alterada após este ponto.

**Rejeitado**
: Não vamos implementar o recurso conforme descrito aqui, embora possamos fazer alguma outra versão. Veja comentários no documento para detalhes. A proposta não deve ser alterada após este ponto; para trazer outra versão da ideia, escreva uma nova proposta.

**Rascunho**
: Esta ainda não é uma proposta completa; há definitivamente peças faltando. Por favor, não adicione novas propostas com este status; coloque-as no sub-diretório "ideias" em vez disso.

**Necessita de Revisão**
: A ideia da proposta é boa, mas a proposta como está tem problemas sérios que a impedem de ser aceita. Veja comentários no documento para detalhes.

**Morto**
: A proposta não foi tocada há muito tempo, e não parece que alguém vai completá-la em breve. Pode se tornar "Aberto" novamente se receber um novo proponente.

**Necessita de Pesquisa**
: Há problemas de pesquisa que precisam ser resolvidos antes que fique claro se a proposta é uma boa ideia.

**Meta**
: Esta não é uma proposta, mas um documento sobre propostas.

**Reserva**
: Esta proposta não é algo que estamos planejando implementar atualmente, mas talvez queiramos ressuscitá-la algum dia se decidirmos fazer algo como o que ela propõe.

**Informativo**
: Esta proposta é a última palavra sobre o que está fazendo. Não vai se tornar uma especificação a menos que alguém copie-e-cole em uma nova especificação para um subsistema novo.

Os editores mantêm o status correto das propostas, com base no consenso geral e em sua própria discrição.

## Numeração de propostas

Os números 000-099 são reservados para propostas especiais e meta-propostas. 100 e acima são usados para propostas reais. Os números não são reciclados.

## Referências

- [Processo de Proposta do Tor](https://gitweb.torproject.org/torspec.git/tree/proposals/001-process.txt)
