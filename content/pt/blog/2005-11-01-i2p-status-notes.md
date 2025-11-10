---
title: "Notas de status do I2P de 2005-11-01"
date: 2005-11-01
author: "jr"
description: "Atualização semanal abordando o sucesso do lançamento da versão 0.6.1.4, análise de ataque de bootstrap (ataque à fase de inicialização), correções de segurança do I2Phex 0.1.1.34, desenvolvimento do aplicativo de voz voi2p e integração do feed RSS do Syndie"
categories: ["status"]
---

Oi, pessoal, chegou aquela hora da semana de novo

* Index

1) 0.6.1.4 e status da rede 2) boostraps, predecessores, adversários passivos globais, e CBR 3) i2phex 0.1.1.34 4) aplicativo voi2p 5) syndie e sucker 6) ???

* 1) 0.6.1.4 and net status

O lançamento da versão 0.6.1.4 no último sábado parece ter ocorrido de forma bastante tranquila - 75% da rede já atualizou (obrigado!), e a maioria dos demais está na 0.6.1.3 de qualquer forma. As coisas parecem estar funcionando razoavelmente bem e, embora eu não tenha recebido muito retorno sobre isso - nem positivo nem negativo, presumo que vocês reclamariam alto se fosse ruim :)

Em particular, tenho interesse em ouvir qualquer feedback de pessoas que usam conexões de modem discado (dial-up), pois os testes que realizei são apenas uma simulação básica desse tipo de conexão.

* 2) boostraps, predecessors, global passive adversaries, and CBR

Tem havido muito mais discussão na lista a respeito de algumas ideias, com um resumo dos ataques de bootstrap disponível online [1]. Fiz algum progresso especificando a criptografia para a opção 3 e, embora nada tenha sido publicado ainda, é relativamente simples.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/001146.html

Houve discussões adicionais sobre como melhorar a resistência a adversários poderosos com constant bitrate (CBR) tunnels (túneis), e, embora tenhamos a opção de explorar essa abordagem, isso está atualmente previsto para o I2P 3.0, pois seu uso adequado exige recursos significativos e provavelmente teria um impacto mensurável tanto sobre quem estaria disposto a usar o I2P com tal sobrecarga quanto sobre quais grupos sequer conseguiriam ou não usar o I2P.

* 3) I2Phex 0.1.1.34

No último sábado também tivemos uma nova versão do I2Phex [2], corrigindo um vazamento de descritor de arquivo que eventualmente faria o I2Phex falhar (obrigado, Complication!) e removendo algum código que permitiria que pessoas instruíssem remotamente a sua instância do I2Phex a baixar determinados arquivos (obrigado, GregorK!). A atualização é altamente recomendada.

Também houve uma atualização na versão CVS (ainda não lançada) que resolve alguns problemas de sincronização — o Phex pressupõe que algumas operações de rede são processadas imediatamente, enquanto o I2P pode às vezes levar um tempo para fazer as coisas :) Isso se manifesta com a GUI travando por um tempo, downloads ou uploads ficando parados, ou conexões sendo recusadas (e talvez de algumas outras formas). Ainda não foi muito testada, mas provavelmente será incluída na 0.1.1.35 esta semana. Tenho certeza de que mais novidades serão publicadas no fórum quando houver mais novidades.

[2] http://forum.i2p.net/viewtopic.php?t=1143

* 4) voi2p app

Aum está trabalhando firme no seu novo app de voz (e texto) via I2P e, embora eu ainda não o tenha visto, parece legal. Talvez o Aum possa nos dar uma atualização na reunião, ou podemos simplesmente esperar pacientemente pela primeira versão alpha :)

* 5) syndie and sucker

o dust vem trabalhando intensamente no syndie e no sucker, e o build mais recente do CVS do I2P agora permite importar automaticamente conteúdo de feeds RSS e atom e publicá-lo no seu blog do syndie. No momento, você precisa adicionar explicitamente lib/rome-0.7.jar e lib/jdom.jar ao seu wrapper.config (wrapper.java.classpath.20 and 21), mas vamos empacotar isso para que não seja necessário mais tarde. Ainda é um trabalho em andamento, e o rome 0.8 (ainda não lançado) parece oferecer coisas bem legais, como a capacidade de capturar os anexos de um feed, que o sucker poderá então importar como um anexo a uma postagem do syndie (no momento ele já lida com imagens e links também!)

Como acontece com todos os feeds RSS, parece haver algumas discrepâncias na forma como o conteúdo é incluído, então alguns feeds funcionam melhor do que outros. Acho que, se as pessoas ajudarem a testar com diferentes feeds e avisarem o dust sobre quaisquer problemas em que isso falhe, isso pode ser útil. De qualquer forma, isso tudo parece bem empolgante, bom trabalho, dust!

* 6) ???

Por enquanto é isso, mas, se alguém tiver alguma pergunta ou quiser discutir mais alguns pontos, apareçam na reunião às 20h GMT (lembrem-se do horário de verão!).

=jr
