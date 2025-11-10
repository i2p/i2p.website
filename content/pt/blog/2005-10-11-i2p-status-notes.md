---
title: "Notas de status do I2P para 2005-10-11"
date: 2005-10-11
author: "jr"
description: "Atualização semanal abordando o sucesso do lançamento da versão 0.6.1.2, novo proxy I2PTunnelIRCClient para filtrar mensagens IRC inseguras, Syndie CLI (interface de linha de comando) e conversão de RSS para SML, e planos de integração do I2Phex"
categories: ["status"]
---

Oi, pessoal, é terça-feira de novo

* Index

1) 0.6.1.2 2) I2PTunnelIRCClient 3) Syndie 4) I2Phex 5) Esteganografia e darknets (re: flamewar) 6) ???

* 1) 0.6.1.2

O lançamento da versão 0.6.1.2 da semana passada tem corrido muito bem até agora - 75% da rede já atualizou, HTTP POST está funcionando bem, e a biblioteca de streaming está enviando dados de forma razoavelmente eficiente (a resposta completa a uma requisição HTTP é frequentemente recebida em uma única ida e volta de ponta a ponta). A rede também cresceu um pouco - os números estáveis parecem ser de cerca de 400 pares, embora tenha subido um pouco mais para 600–700 com rotatividade durante o pico da referência no digg/gotroot [1] no fim de semana.

[1] http://gotroot.com/tiki-read_article.php?articleId=195     (sim, um artigo muito antigo, eu sei, mas alguém o encontrou de novo)

Desde que o 0.6.1.2 foi lançado, foram adicionadas ainda mais melhorias — a causa dos recentes irc2p netsplits (partições da rede) foi encontrada (e corrigida), assim como melhorias bem significativas na transmissão de pacotes do SSU (economizando acima de 5% dos pacotes). Não tenho certeza de quando exatamente o 0.6.1.3 será lançado, mas talvez ainda esta semana. Veremos.

* 2) I2PTunnelIRCClient

Outro dia, após alguma discussão, dust criou rapidamente uma nova extensão para o I2PTunnel - o proxy "ircclient". Ela funciona filtrando o conteúdo enviado e recebido entre o cliente e o servidor pela rede I2P, removendo mensagens IRC inseguras e reescrevendo aquelas que precisam ser ajustadas. Depois de alguns testes, ela parece estar muito boa, e dust contribuiu com ela para o I2PTunnel, e agora ela é oferecida aos usuários pela interface web. Tem sido ótimo que o pessoal do irc2p tenha ajustado seus servidores IRC para descartar mensagens inseguras, mas agora não precisamos mais confiar neles para fazer isso - o usuário local tem controle sobre a própria filtragem.

Usá-lo é bem simples - em vez de criar um "Client proxy" para IRC como antes, basta criar um "IRC proxy". Se você quiser converter seu "Client proxy" existente em um "IRC proxy", você pode (com um certo constrangimento) editar o arquivo i2ptunnel.config, alterando "tunnel.1.type=client" para "tunnel.1.ircclient" (ou qualquer número que seja apropriado para o seu proxy).

Se tudo correr bem, este será adotado como o tipo de proxy padrão do I2PTunnel para conexões de IRC na próxima versão.

Bom trabalho, dust, obrigado!

* 3) Syndie

O recurso de sindicação agendada do Ragnarok parece estar indo bem, e desde que a versão 0.6.1.2 foi lançada, surgiram dois novos recursos - eu adicionei uma nova CLI (linha de comando) simplificada para publicar no Syndie [2], e o dust (viva o dust!) preparou rapidamente algum código para extrair conteúdo de um feed RSS/Atom, obter quaisquer enclosures (anexos) ou imagens referenciados nele e converter o conteúdo do RSS para SML (!!!) [3][4].

As implicações de ambas, em conjunto, devem ser claras. Mais novidades quando houver mais novidades.

[2] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000000&expand=true [3] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000001&expand=true [4] http://dust.i2p/Sucker.java     (vamos integrá-lo ao CVS em breve)

* 4) I2Phex

Dizem por aí que o I2Phex está funcionando muito bem, mas que problemas ao longo do tempo ainda persistem. Tem havido alguma discussão no fórum [5] sobre como proceder, e GregorK, o desenvolvedor líder do Phex, chegou até a se manifestar em apoio à integração da funcionalidade do I2Phex de volta ao Phex (ou, pelo menos, permitir que a versão principal do Phex ofereça uma interface de plugin simples para a camada de transporte).

Isso seria realmente incrível, pois significaria muito menos código para manter, além de nos beneficiarmos do trabalho da equipe do Phex na melhoria da base de código. No entanto, para que isso funcione, precisamos que alguns hackers se apresentem e assumam a liderança da migração. O código do I2Phex deixa bem claro onde o sirup fez alterações, então não deve ser muito difícil, mas provavelmente também não é exatamente trivial ;)

Realmente não tenho tempo para cuidar disso agora, mas passe no fórum se quiser ajudar.

[5] http://forum.i2p.net/viewforum.php?f=25

* 5) Stego and darknets (re: flamewar)

A lista de discussão [6] tem estado bastante ativa ultimamente com a discussão sobre esteganografia e darknets (redes ocultas). O tópico migrou em grande parte para a lista técnica do Freenet [7], sob o assunto "I2P conspiracy theories flamewar", mas ainda está em andamento.

Não tenho certeza de que eu tenha muito a acrescentar que não esteja nos próprios posts, mas algumas pessoas mencionaram que a discussão ajudou no entendimento de I2P e Freenet, então talvez valha a pena dar uma olhada. Ou talvez não ;)

[6] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html [7] nttp://news.gmane.org/gmane.network.freenet.technical

* 6) ???

Como você pode ver, há muita coisa empolgante acontecendo, e tenho certeza de que deixei algumas de fora. Dê uma passada no #i2p em alguns minutos para a nossa reunião semanal e dê um alô!

=jr
