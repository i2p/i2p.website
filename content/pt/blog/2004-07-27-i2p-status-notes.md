---
title: "Notas de status do I2P para 2004-07-27"
date: 2004-07-27
author: "jr"
description: "Atualização semanal de status do I2P sobre problemas de desempenho da versão 0.3.3 e próximas otimizações"
categories: ["status"]
---

Olá, pessoal, hora da sessão semanal de desabafos

## Índice:

1. 0.3.3 & current updates
2. NativeBigInteger
3. ???

## 1) 0.3.3

Lançamos a versão 0.3.3 na sexta-feira passada e, após um ou dois dias de bastante instabilidade, parece estar funcionando razoavelmente bem. Não tão boa quanto a 0.3.2.3, mas geralmente consegui ficar no irc.duck.i2p por períodos de 2 a 7 horas. No entanto, como tenho visto muita gente com problemas, iniciei o logger e monitorei em detalhes o que estava acontecendo. A resposta curta é que estávamos simplesmente usando mais largura de banda do que o necessário, causando congestionamento e falhas de tunnel (devido a mensagens de teste com tempo esgotado, etc.).

Passei os últimos dias de volta ao simulador, enviando uma série de heartbeats (sinais periódicos de monitoramento) por uma rede para ver o que podemos melhorar, e temos um conjunto de atualizações a caminho com base nisso:

### netDb update to operate more efficiently

As mensagens de consulta do netDb existentes têm até 10+KB e, embora as respostas bem-sucedidas sejam frequentes, as respostas malsucedidas podem chegar a 30+KB (já que ambas continham estruturas RouterInfo completas (informações do router)). O novo netDb substitui essas estruturas RouterInfo completas pelo hash do router - transformando mensagens de 10KB e 30KB em mensagens de ~100 bytes.

### throw out the SourceRouteBlock and SourceRouteReplyMessage

Essas estruturas eram resquícios de uma ideia antiga, mas não agregam valor algum ao anonimato ou à segurança do sistema. Ao descartá-las em favor de um conjunto mais simples de pontos de dados de resposta, reduzimos drasticamente os tamanhos das mensagens de gerenciamento de tunnel e reduzimos pela metade o tempo de garlic encryption.

### Atualização do netDb para operar de forma mais eficiente

O código estava um pouco 'verboso' durante a criação do tunnel, então as mensagens desnecessárias foram suprimidas.

### descartar o SourceRouteBlock e o SourceRouteReplyMessage

Parte do código criptográfico para o garlic routing (roteamento com agregação de mensagens) estava usando preenchimento fixo baseado em algumas técnicas de garlic routing que não estamos usando (quando o escrevi em setembro e outubro, achei que iríamos fazer garlic routing de múltiplos saltos em vez de tunnels).

Também estou trabalhando para ver se consigo aplicar uma atualização completa ao roteamento de tunnel para adicionar os IDs de tunnel por salto.

Como se pode ver no roadmap, isso abrange grande parte da versão 0.4.1, mas, como a mudança no netDb acarretou a perda de compatibilidade com versões anteriores, podemos aproveitar para concluir de uma vez uma série de alterações incompatíveis com versões anteriores.

Ainda estou executando testes no simulador e preciso ver se consigo finalizar o recurso de ID de tunnel por salto, mas espero lançar um novo patch em um ou dois dias. Não terá compatibilidade com versões anteriores, então a atualização terá alguns percalços, mas deve valer a pena.

## 2) NativeBigInteger

Iakin vem fazendo algumas atualizações no código do NativeBigInteger para a equipe do Freenet, otimizando algumas coisas que não usamos, mas também criando um código de detecção de CPU que podemos usar para selecionar automaticamente a biblioteca nativa correta. Isso significa que poderemos distribuir o jbigi como uma única biblioteca na instalação padrão e ele escolherá a correta sem precisar pedir nada ao usuário. Ele também concordou em liberar suas modificações e o novo código de detecção de CPU para que possamos incorporá-lo ao nosso código-fonte (viva, Iakin!). Não tenho certeza de quando isso será disponibilizado, mas avisarei quando for, já que aqueles com bibliotecas jbigi existentes provavelmente precisarão de uma nova.

## 3) ???

Bem, a última semana foi de cabeça enfiada no código, hackeando, então não há muitas atualizações. Alguém tem mais alguma coisa para discutir? Se sim, apareça na reunião hoje à noite, às 21h GMT, no #i2p.

=jr
