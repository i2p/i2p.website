---
title: "Notas de status do I2P de 2005-03-22"
date: 2005-03-22
author: "jr"
description: "Notas semanais sobre o status do desenvolvimento do I2P cobrindo o lançamento da versão 0.5.0.3, a implementação de agrupamento de mensagens no tunnel e ferramentas de atualização automática"
categories: ["status"]
---

Oi, pessoal, rápida atualização de status

* Index

1) 0.5.0.3 2) processamento em lotes 3) atualização 4) ???

* 0.5.0.3

A nova versão foi lançada e já está por aí, e a maioria de vocês atualizou bem rapidamente - obrigado! Houve algumas correções de bugs em vários problemas, mas nada revolucionário - a maior parte foi remover os usuários das versões 0.5 e 0.5.0.1 da rede. Desde então venho acompanhando o comportamento da rede, investigando o que está acontecendo e, embora tenha havido alguma melhora, ainda há algumas coisas que precisam ser resolvidas.

Haverá uma nova versão em um dia ou dois com uma correção de bug para um problema que ninguém encontrou até agora, mas que quebra o novo código de processamento em lotes. Também haverá algumas ferramentas para automatizar o processo de atualização de acordo com as preferências do usuário, junto com outras pequenas coisas.

* batching

Como mencionei no meu blog, há espaço para reduzir dramaticamente a largura de banda e a contagem de mensagens necessárias na rede fazendo um agrupamento em lotes (batching) muito simples de mensagens de tunnel - em vez de colocar cada mensagem I2NP, independentemente do tamanho, em uma mensagem de tunnel própria, ao adicionar um pequeno atraso podemos agrupar até 15 ou mais delas em uma única mensagem de tunnel. Os maiores ganhos ocorrerão em serviços que usam mensagens pequenas (como IRC), enquanto transferências de arquivos grandes não serão tão afetadas. O código para realizar o agrupamento em lotes foi implementado e testado, mas, infelizmente, há um bug na rede em produção que faria com que todas as mensagens I2NP dentro de uma mensagem de tunnel, exceto a primeira, fossem perdidas. É por isso que teremos um lançamento intermediário com essa correção, seguido pelo lançamento com o agrupamento em lotes cerca de uma semana depois.

* updating

Nesta versão intermediária, vamos incluir parte do tão discutido código de "autoupdate". Temos as ferramentas para verificar periodicamente se há anúncios de atualização autênticos, baixar a atualização de forma anônima ou não e, em seguida, instalá-la ou simplesmente exibir um aviso no console do router informando que ela está pronta e aguardando instalação. A própria atualização agora usará o novo formato de atualização assinada do smeghead, que é essencialmente a atualização mais uma assinatura DSA. As chaves usadas para verificar essa assinatura serão fornecidas junto com o I2P, bem como configuráveis no console do router.

O comportamento padrão será apenas verificar periodicamente anúncios de atualização, mas não tomar nenhuma ação - apenas exibir um recurso "Atualizar agora" com um clique no console do router. Haverá muitos outros cenários para diferentes necessidades dos usuários, mas espera-se que todos sejam contemplados por meio de uma nova página de configuração.

* ???

Estou me sentindo um pouco indisposto, então o texto acima não entra em todos os detalhes sobre o que está acontecendo. Apareça na reunião e preencha as lacunas :)

Ah, a propósito, vou publicar uma nova chave PGP para mim nos próximos um ou dois dias também (já que esta expira em breve...), então fiquem atentos.

=jr
