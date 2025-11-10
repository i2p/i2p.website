---
title: "Notas de status do I2P para 2005-01-04"
date: 2005-01-04
author: "jr"
description: "Primeiras notas semanais de status de 2005, cobrindo o crescimento da rede até 160 routers, as funcionalidades da 0.4.2.6 e o desenvolvimento da 0.5"
categories: ["status"]
---

Olá, pessoal, é hora das nossas primeiras atualizações semanais de status de 2005

* Index

1) Status da rede 2) 0.4.2.6 3) 0.5 4) jabber @ chat.i2p 5) ???

* 1) Net status

Ao longo da última semana, as coisas têm sido bastante interessantes na rede — na véspera de Ano-Novo, foram publicados alguns comentários em um site popular falando sobre o i2p-bt e tivemos um pequeno pico de novos usuários. No momento, há entre 120 e 150 routers na rede, embora isso tenha atingido um pico de 160 há alguns dias. Ainda assim, a rede se manteve firme, com pares de alta capacidade absorvendo a carga excedente sem muita interrupção para os outros pares. Alguns usuários operando sem limites de largura de banda em conexões muito rápidas relataram taxa de transferência de 2-300KBps, enquanto aqueles com menos capacidade usam os habituais valores baixos de 1-5KBps.

Acho que me lembro de Connelly mencionar que estava vendo mais de 300 routers diferentes ao longo de alguns dias após o ano-novo, então houve uma rotatividade significativa. Por outro lado, agora temos um número estável de 120-150 usuários online, ao contrário dos 80-90 anteriores, o que é um aumento razoável. Ainda *não* queremos que isso cresça demais por enquanto, porém, pois há problemas de implementação conhecidos que ainda precisam ser resolvidos. Especificamente, até a versão 0.6 [1], vamos querer ficar abaixo de 2-300 pares para manter o número de threads em um nível razoável. No entanto, se alguém quiser ajudar na implementação do transporte UDP, podemos chegar lá muito mais rápido.

Na última semana, acompanhei as estatísticas divulgadas pelos trackers i2p-bt e foram transferidos gigabytes de arquivos grandes, com alguns relatos de 80-120KBps. O IRC teve mais instabilidades do que o habitual desde que aqueles comentários foram publicados naquele site, mas o intervalo entre desconexões ainda é da ordem de horas. (pelo que posso perceber, o router onde o irc.duck.i2p está vem operando bem próximo ao seu limite de banda, o que explicaria isso)

[1] http://www.i2p.net/roadmap#0.6

* 2) 0.4.2.6

Desde a versão 0.4.2.5, foram adicionadas algumas correções e novos recursos ao CVS que pretendemos disponibilizar em breve, incluindo correções de confiabilidade para a biblioteca de streaming, maior resiliência a mudanças de endereço IP e a inclusão da implementação do addressbook (livro de endereços) do ragnarok.

Se você não ouviu falar do addressbook (livro de endereços) ou não o utilizou, resumindo: ele atualizará automaticamente seu arquivo hosts.txt, buscando periodicamente e mesclando alterações a partir de alguns locais hospedados anonimamente (por padrão, http://dev.i2p/i2p/hosts.txt e http://duck.i2p/hosts.txt). Você não precisará alterar nenhum arquivo, mexer em nenhuma configuração ou executar nenhum aplicativo extra - ele será implantado dentro do I2P router como um arquivo .war padrão.

Claro, se você *realmente* quiser colocar a mão na massa com o addressbook (livro de endereços), fique à vontade - veja o site do Ragnarok [2] para os detalhes. As pessoas que já têm o addressbook implantado no router vão precisar fazer um pequeno malabarismo durante a atualização para a 0.4.2.6, mas ele vai funcionar com todas as suas configurações antigas.

[2] http://ragnarok.i2p/

* 3) 0.5

Números, números, números! Bem, como eu já disse antes, a versão 0.5 vai reformular como o roteamento de tunnel funciona, e há progresso nessa frente. Nos últimos dias tenho implementado o novo código de criptografia (e testes unitários) e, assim que estiverem funcionando, vou publicar um documento descrevendo minhas ideias atuais sobre como, o que e por que o novo roteamento de tunnel vai funcionar. Estou implementando a criptografia para isso agora, em vez de depois, para que as pessoas possam avaliar o que isso significa de forma concreta, bem como identificar áreas problemáticas e apresentar sugestões de melhoria. Espero ter o código funcionando até o fim da semana, então talvez haja mais documentos publicados neste fim de semana. Sem promessas, porém.

* 4) jabber @ chat.i2p

jdot colocou no ar um novo servidor jabber, e ele parece funcionar muito bem tanto para conversas individuais quanto para bate-papo em grupo. Confira as informações no fórum [3]. O canal de discussão dos desenvolvedores do i2p continuará sendo o irc #i2p, mas é sempre bom ter alternativas.

[3] http://forum.i2p.net/viewtopic.php?t=229

* 5) ???

Ok, isso é basicamente tudo que tenho para mencionar no momento - tenho certeza de que há muito mais acontecendo que outras pessoas querem comentar, então passe na reunião em 15m @ o lugar de sempre [4] e nos diga o que está acontecendo!

=jr
