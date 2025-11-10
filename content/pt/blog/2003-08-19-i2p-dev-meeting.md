---
title: "Reunião de desenvolvedores do I2P, 19 de agosto de 2003"
date: 2003-08-19
author: "jrand0m"
description: "54ª reunião de desenvolvimento do I2P abordando atualizações do SDK, revisão do I2NP, progresso em criptografia e status do desenvolvimento"
categories: ["meeting"]
---

<h2 id="quick-recap">Recapitulação rápida</h2>

<p class="attendees-inline"><strong>Presentes:</strong> cohesion, hezekiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">Registro da reunião</h2>

<div class="irc-log"> --- Log opened Tue Aug 19 16:56:12 2003 17:00 -!- logger [logger@anon.iip] has joined #iip-dev 17:00 -!- Topic for #iip-dev: Reuniões semanais de desenvolvimento do IIP e outras 	 conversas entre desenvolvedores acontecem aqui. 17:00 [Usuários #iip-dev] 17:00 [ cohesion] [ leenookx  ] [ mihi] [ shardy_  ] [ UserXClone] 17:00 [ Ehud    ] [ logger    ] [ nop ] [ thecrypto] [ velour    ] 17:00 [ hezekiah] [ lonelynerd] [ Rain] [ UserX    ] [ WinBear   ] 17:00 -!- Irssi: #iip-dev: Total de 15 nicks [0 ops, 0 halfops, 0 voices, 15 normal] 17:00 -!- Irssi: Join to #iip-dev was synced in 7 secs 17:00 < hezekiah> Certo! :) 17:00 < hezekiah> Ambos os loggers estão no lugar. :) 17:01 < thecrypto> yah! 17:03 < hezekiah> Hmmm ... 17:03 < hezekiah> Esta reunião deveria ter começado há 3 minutos. 17:03 < hezekiah> O que será que houve. 17:04 < thecrypto> então, quem está idle 17:04 < hezekiah> jrand0m nem está online. 17:04 < hezekiah> nop está idle há 15 minutos. 17:05 < nop> oi 17:05 < nop> desculpa 17:05 < nop> Estou super ocupado no trabalho 17:05 < mihi> [22:36] * jrand0m saiu para jantar mas volto dentro 	 de meia hora para a reunião 17:05 -!- jrand0m [~jrandom@anon.iip] has joined #iip-dev 17:05 < hezekiah> Oi, jrand0m. 17:05 < nop> oi 17:05 < nop> ok, é o seguinte 17:05 < nop> Não posso ser visto no IIP no trabalho agora 17:05 < nop> então vou falar com vocês mais tarde 17:05 < nop> levei bronca por causa disso ontem 17:05 < nop> então 17:05 < hezekiah> Tchau, nop. 17:05 < thecrypto> tchau 17:06 < nop> Vou ficar no canal 17:06 < nop> só não vai ser óbvio :) 17:06 < hezekiah> jrand0m? Já que você é quem mais fala hoje em dia, tem 	 algo que queira na pauta desta reunião? 17:07 < jrand0m> voltei 17:08 < jrand0m> ok, o macarrão ao pesto estava bom. 17:08 < jrand0m> deixa eu puxar as coisas tipo agenda 17:09 -!- Lookaround [~chatzilla@anon.iip] has joined #iip-dev 17:09 < jrand0m> x.1) modificações no SDK do i2cp x.2) revisão do i2np x.3) transporte HTTP com polling 	 x.4) status de desenvolvimento x.5) a fazer x.6) plano para as próximas duas semanas 17:09 < jrand0m> (coloque o x no número da agenda que couber) 17:10 < thecrypto> você é a agencda 17:10 < hezekiah> jrand0m: Eu não tenho nada a dizer, e o nop 17:10 < hezekiah> não pode falar. 17:10 < jrand0m> lol 17:10 < hezekiah> O UserX provavelmente não vai acrescentar nada (ele geralmente 	 não acrescenta), então, da minha parte, é tudo seu. :0 17:10 < hezekiah> :) 17:10 < jrand0m> 'k.  estamos logando? 17:10 < jrand0m> heh 17:10 < hezekiah> Estou logando tudo. 17:10 < jrand0m> beleza.  ok.  0.1) bem-vindos. 17:10 < jrand0m> oi. 17:11 < jrand0m> 0.2) lista de e-mails 17:11 < jrand0m> a lista está fora do ar no momento, volta o quanto antes.  vocês saberão quando voltar :) 17:11 < jrand0m> por enquanto, usem o wiki ou o iip para conversar. 17:11 < jrand0m> 1.1) modificações no SDK do i2cp 17:12 < jrand0m> o SDK foi atualizado com algumas correções de bugs, além de algumas 	 novidades na especificação. 17:12 < jrand0m> Eu postei na lista ontem com as informações. 17:13 < jrand0m> hezekiah/thecrypto/jeremiah> alguma pergunta sobre o que eu postei, 	 ou ideias de plano para implementar as mudanças?  (ou outras alternativas que eu 	 não tenha considerado?) 17:13 < hezekiah> Estou correndo feito uma barata tonta me preparando 	 para a faculdade. 17:13 < jrand0m> pois é, entendido. 17:13 < hezekiah> Dei uma olhada por alto no que você escreveu, mas ainda não 	 vi de fato as mudanças na especificação. 17:13 < jrand0m> a gente mal tem mais tempo seu, né... 17:13 < hezekiah> Não até eu chegar na faculdade. 17:14 < hezekiah> Quando eu chegar, provavelmente vou ficar sumido por 	 pelo menos uma semana enquanto me ajusto. 17:14 < jrand0m> e quando você chegar lá vai ter muita coisa pra organizar 	 (se bem me lembro de quando fui pra faculdade ;) 17:14 < jrand0m> heh pois é. 17:14 < hezekiah> Depois disso, devo estar um pouco mais eficiente e ter 	 mais tempo pra codar. 17:14 < jrand0m> beleza 17:14 < thecrypto> eu tô só fazendo crypto, então as estruturas de dados são minha 	 preocupação real, quando eu terminar o modo CTS, vou trabalhar nisso provavelmente 17:14 < hezekiah> Enfim, é o que eu imagino. 17:14 < jrand0m> ótimo, thecrypto 17:15 < jrand0m> ok, a coisa boa é que o SDK funciona perfeitamente (com 	 os bugs que o mihi achou corrigidos [yay mihi!]) sem a atualização da spec. 17:15 -!- arsenic [~none@anon.iip] has joined #iip-dev 17:16 < jrand0m> ok, indo para 1.2) revisão do i2np 17:16 < jrand0m> alguém leu o doc? 17:16 < jrand0m> ;) 17:16 < hezekiah> Eu não, ainda. 17:16 < hezekiah> Como eu disse, atualmente sou uma barata tonta. 17:17 < hezekiah> A propósito, jrand0m, parece que você gosta de enviar PDFs. 17:17 < jrand0m> todos conseguem ler openoffice .swx? 17:17 < hezekiah> Eu consigo. 17:17 < jrand0m> [se sim, eu envio swx] 17:17 -!- abesimpson [~k@anon.iip] has joined #iip-dev 17:17 < thecrypto> eu consigo 17:17 < hezekiah> Não consigo buscar texto em um PDF com o KGhostView. 17:17 < hezekiah> Então isso atrapalha bastante. 17:17 < jrand0m> que chato, hezekiah 17:17 -!- mrflibble [mrflibble@anon.iip] has joined #iip-dev 17:17 < hezekiah> A versão para linux do Adobe Acrobat também não é muito amigável. 17:18 < jrand0m> ok, então formato openoffice em vez de pdf. 17:18 < hezekiah> Legal. 17:18 < jrand0m> hum, ok.  o i2np tem algumas mudanças menores na estrutura LeaseSet 	 (refletindo a mudança no i2cp postada antes), mas fora isso, 	 está basicamente no lugar. 17:19 < hezekiah> jrand0m: Todos esses docs estão no CVS do cathedral? 17:19 < nop> ah 17:19 < nop> posso me intrometer 17:19 < hezekiah> ou seja, cópias dos arquivos PDF que você anda enviando para a 	 lista, etc. 17:19 < hezekiah> nop: Vai em frente. 17:19 < nop> é off topic mas importante 17:19 -!- ChZEROHag [hag@anon.iip] has joined #iip-dev 17:19 < nop> IIP-dev e o mail estão meio estranhos agora 17:19 < hezekiah> Percebi. 17:19 < nop> então tenham um pouco de paciência 17:20 < nop> estamos tentando colocar isso de pé 17:20 < nop> mas tem spam assassin embutido 17:20 < nop> que é a boa notícia 17:20 < nop> :) 17:20 < nop> e um monte de outros recursos 17:20 < jrand0m> alguma previsão, nop, para a lista? 17:20  * ChZEROHag mete o nariz 17:20 < jrand0m> (sei que você está ocupado, não é cobrança, só curiosidade) 17:20 < nop> com sorte até amanhã 17:20 < jrand0m> beleza 17:20 < nop> o admin do mail está trabalhando nisso 17:21  * hezekiah observa que o jrand0m gosta _mesmo_ da lista iip-dev. ;-) 17:21 < nop> haha 17:21 < hezekiah> Vai, delta407! 17:21 < nop> enfim 17:21 < jrand0m> é melhor documentar decisões publicamente, hezekiah ;) 17:21 < nop> de volta à nossa reunião normal 17:21 < jrand0m> heh 17:21 -!- nop is now known as nop_afk 17:21 < hezekiah> jrand0m: Onde estávamos? 17:21 < jrand0m> ok, à sua pergunta hezekiah> alguns estão, mas os mais recentes 	 não.  Vou passar a colocar no formato openoffice. 17:21 < jrand0m> em vez de pdfs 17:22 < hezekiah> OK. 17:22 < hezekiah> Seria muito legal se todos os docs estivessem no CVS. 17:22 < jrand0m> com certeza, e vão estar 17:22 < hezekiah> Aí eu só dou update e sei que tenho a edição mais recente. 17:22 < jrand0m> (há três rascunhos que ainda não estão) 17:22 < hezekiah> (A propósito, um pouco off topic, mas o acesso anônimo ao 	 cathedral já está no ar?) 17:23 < jrand0m> ainda não. 17:23 < jrand0m> ok, até sexta, espero ter outro rascunho do I2NP em 	 forma completa [ou seja, nada de ... nas seções de explicação do kademlia, e detalhes 	 de implementação de exemplo] 17:24 < jrand0m> não há mudanças significativas.  só mais preenchimento 	 esclarecendo as coisas. 17:24 < hezekiah> Massa. 17:24 < hezekiah> Vai ter layout em bytes para as estruturas de dados disponível nele? 17:24 < jrand0m> 1.3) especificação do I2P Polling HTTP Transport. 17:24 < jrand0m> não, os byte layouts vão na especificação de estruturas de dados, que 	 deveria ser convertida para o formato padrão em vez de html 17:25 < jrand0m> (embora o I2NP já tenha todos os byte layouts necessários) 17:25 < jrand0m> ((se você ler *cough* ;) 17:25 < hezekiah> Bom. 17:25 < hezekiah> lol 17:25 < hezekiah> Foi mal por isso. 17:25 < hezekiah> Como eu disse, tenho estado muito ocupado. 17:25 < jrand0m> heh sem problema, você está prestes a ir para a faculdade, 	 era pra você estar festejando :) 17:25 < hezekiah> Festando? 17:25 < jrand0m> ok, 1.3) I2NP Polling HTTP Transport spec 17:25 < hezekiah> Hmmm ... acho que eu sou meio estranho. 17:25 < jrand0m> heh 17:26 < jrand0m> ok, tentei enviar isso antes, mas vou fazer commit 	 em breve.  é um protocolo de transporte rápido e sujo que se encaixa no I2NP 	 para permitir que routers enviem dados de um lado para o outro sem conexões 	 diretas (por exemplo firewalls, proxies, etc) 17:27 < jrand0m> Eu estou *esperando* que alguém veja como isso funciona e construa 	 transportes similares (por exemplo TCP bidirecional, UDP, HTTP direto, etc) 17:27 -!- mihi [none@anon.iip] has quit [Ping timeout] 17:27 < hezekiah> Hmmm, bem eu don 17:27 < jrand0m> antes de colocar o I2NP para revisão, precisamos incluir 	 transportes de exemplo para que as pessoas vejam o quadro completo 17:27 < hezekiah> não acho que _eu_ vá construir qualquer transporte tão cedo. ;-) 17:27 -!- WinBear_ [~WinBear@anon.iip] has joined #iip-dev 17:27 < hezekiah> TCP está funcionando para Java e Python. 17:27 < hezekiah> (Pelo menos client-to-router.) 17:27 < jrand0m> sem problema, só estou colocando como um a fazer para quem 	 quiser contribuir 17:28 < hezekiah> Certo. 17:28 < jrand0m> certo, client-router tem requisitos diferentes do 	 router-router. 17:28 < jrand0m> ok, enfim, 1.4) status de desenvolvimento 17:28 < jrand0m> como estamos com CBC, thecrypto? 17:28 < thecrypto> CBC foi commitado 17:28 < jrand0m> w00000t 17:28 < thecrypto> CTS está quase pronto 17:28 < hezekiah> thecrypto: O que é CTS? 17:29 < thecrypto> só tenho que descobrir como implementar isso direitinho 17:29 < jrand0m> cts é cyphertext stealing :) 17:29 < hezekiah> Ah! 17:29 < thecrypto> CipherText Stealing 17:29 -!- WinBear [WinBear@anon.iip] has quit [EOF From client] 17:29 < jrand0m> você pegou a referência do nop sobre isso? 17:29 < hezekiah> OK. Estamos usando CBC com CTS em vez de padding. 17:29 < hezekiah> Hmm. 17:29 < thecrypto> basicamente, faz a mensagem ficar exatamente do tamanho certo 17:29 < jrand0m> isso é viável do lado do python, hezekiah? 17:29 < hezekiah> Talvez eu precise dar uns tapas na lib de crypto do Python que estou 	 usando para fazê-la usar CTS direito. 17:30 < hezekiah> Sempre preferi CTS a padding, mas não sei 	 o que o PyCrypt faz. 17:30 < jrand0m> o que o python consegue fazer nativamente para permitir recuperar o 	 tamanho exato da mensagem? 17:30 < thecrypto> tudo que você precisa fazer é mudar como você processa os 	 dois últimos blocos 17:30 < hezekiah> Tenho a sensação de que essa biblioteca vai passar por uma reescrita 	 séria. 17:30 < hezekiah> jrand0m: A parte de CBC no python é transparente. Você só 	 envia o buffer para a função encrypt do objeto AES. 17:31 < hezekiah> Ela cospe o texto cifrado.

17:31 < hezekiah> Fim da história.
17:31 < jrand0m> D(E(data,key),key) == data, byte a byte, exatamente  mesmo tamanho?
17:31 < hezekiah> Então, se tiver a ideia maluca de usar padding (preenchimento) em vez de CTS,  então talvez eu precise mexer nas entranhas dele e consertar.
17:31 < jrand0m> (independentemente do tamanho da entrada?)
17:31 -!- mihi [~none@anon.iip] entrou em #iip-dev
17:31 < hezekiah> jrand0m: Sim. Deveria.
17:31 < jrand0m> hezekiah> se você puder verificar exatamente qual algoritmo ele  usa para fazer o padding, seria ótimo
17:32 < hezekiah> Certo.
17:32  * jrand0m está hesitante em exigir uma modificação em uma biblioteca de criptografia em Python se  a biblioteca já usa um mecanismo padrão e útil
17:32 < hezekiah> De um jeito ou de outro, CBC com CTS parece bom.
17:32 < hezekiah> jrand0m: Esta biblioteca de criptografia em Python é uma droga.
17:32 < jrand0m> heh 'k
17:33 < thecrypto> só preciso calcular como mexer com os dois blocos
17:33 < hezekiah> jrand0m: ElGamal vai precisar ser totalmente reescrito em  C só para ficar rápido o suficiente para usar.
17:33 < jrand0m> hezekiah> qual é o benchmark para elg em Python de 256 bytes?  isso só é feito uma vez por dest-dest comm...
17:34 < jrand0m> (se você souber de cabeça, claro)
17:34 < hezekiah> Eu teria que testar.
17:34 < hezekiah> Criptografar leva só um ou dois segundos, acho
17:34 < jrand0m> < 5 s, < 2 s, > 10 s, > 30 s?
17:34 < thecrypto> provavelmente vou mexer um pouco com isso
17:34 < hezekiah> A descriptografia pode ficar em algum ponto entre 5 e 10 segundos.
17:34 < jrand0m> legal.
17:35 < jrand0m> hezekiah> você falou com o jeremiah ou tem alguma  novidade sobre o status da API de cliente em Python?
17:35 < hezekiah> thecrypto: Tudo de que você deve precisar é escrever um módulo  em C que funcione com Python.
17:35 < hezekiah> Não faço ideia do que ele tem feito.
17:35 < hezekiah> Não falo com ele desde que voltei.
17:35 < jrand0m> 'k
17:35 < jrand0m> alguma outra atualização de status de desenvolvimento?
17:36 < hezekiah> Hã, não muito da minha parte.
17:36 < hezekiah> Já expliquei meu estado atual de tempo livre.
17:36 < jrand0m> certo.  entendido
17:36 < hezekiah> Meus únicos planos são colocar a API em C no ar e trazer o Python router  de volta em conformidade com a especificação.
17:37 < jrand0m> 'k
17:37 < hezekiah> Meu Deus!
17:37 < jrand0m> 1.4) a fazer
17:37 < jrand0m> sim sr?
17:37 < hezekiah> A biblioteca cripto em Python não implementa CTS nem padding!
17:37 < hezekiah> Vou ter que fazer isso manualmente.
17:37 < jrand0m> hmm?  ela exige que os dados sejam múltiplos de 16 bytes?
17:37 < hezekiah> Sim.
17:38 < jrand0m> heh
17:38 < jrand0m> paciência.
17:38 < hezekiah> Atualmente o Python router usa padding.
17:38 < jrand0m> ok.  aqui estão alguns itens pendentes que precisam ser feitos.
17:38 < hezekiah> Agora eu me lembrei disso.
17:38 < hezekiah> Bem, de
17:38 < hezekiah> vamos ser francos sobre uma coisa.
17:38 < hezekiah> O Python router nunca foi realmente feito para ser usado.
17:39 < hezekiah> Ele serve principalmente para eu ficar muito familiarizado com a  especificação e também cumpre outra coisa:
17:39 < hezekiah> Ele força o Java router a cumprir _exatamente_ a especificação.
17:39 < jrand0m> ambos objetivos muito importantes.
17:39 < hezekiah> Às vezes o Java router não cumpre direito, e aí  o Python router grita feito louco.
17:39 < hezekiah> Então ele não precisa realmente ser rápido ou estável.
17:39 < jrand0m> além disso, não tenho certeza de que ele nunca será usado no SDK
17:39 < jrand0m> certo.  exatamente.
17:39 < jrand0m> a API de cliente em Python é outra coisa, porém
17:39 < hezekiah> Já a API de cliente em Python precisa ser decente.
17:40 < jrand0m> exatamente.
17:40 < hezekiah> Mas isso é problema do jeremiah. :)
17:40 < hezekiah> Deixei isso com ele.
17:40 < jrand0m> os routers locais do SDK são apenas para uso de devs de cliente
17:40 < jrand0m> lol
17:40 < jrand0m> ok, como eu dizia... ;)
17:40 < hezekiah> ;-)
17:41 < jrand0m> - precisamos de alguém para começar a trabalhar numa pequena página web  para i2p que será usada para publicar as várias especificações relacionadas ao  I2P para revisão por pares.
17:41 < jrand0m> Eu gostaria que isso estivesse pronto antes de 1/9.
17:41 < hezekiah> OK. Estou dizendo agora que você não vai querer que eu faça isso.
17:41 < hezekiah> Não sou um bom designer de páginas web. :)
17:41 < jrand0m> nem eu, se alguém aqui já viu meu flog ;)
17:41 < jrand0m> cohesion?  ;)
17:41 < hezekiah> lol
17:42 < hezekiah> Coitado do cohesion, sempre ficando com o trabalho sujo. :-)
17:42  * cohesion lê o backlog
17:42 < hezekiah> ;)
17:42 < jrand0m> heh
17:42 < cohesion> jrand0m: Eu faço isso
17:42 < cohesion> me@jasonclinton.com
17:42 < cohesion> me envie as especificações
17:42 < jrand0m> 'k, obrigado.
17:42 < jrand0m> as especificações ainda não estão todas prontas.
17:43 < jrand0m> mas o conteúdo que precisará estar lá é:
17:43 < cohesion> bem, o que você tem e o que você gostaria de colocar no ar
17:43 < jrand0m> -I2CP spec, I2NP spec, especificação do Transporte HTTP com polling, TCP  Transport spec, Security analysis, Performance analysis, Data structure spec,  e um readme/intro
17:44 < jrand0m> (esses 7 documentos estarão em formato pdf e/ou texto)
17:44 < cohesion> k
17:44 < jrand0m> excetuando o readme/intro
17:45 < jrand0m> Espero que todos esses docs estejam prontos até a próxima semana  (26/8).  isso te dará tempo suficiente para montar uma pequena página para um lançamento em 1/9?
17:46 < jrand0m> ok.  outra coisa que vai precisar entrar no pipe é  um simulador de rede I2P.
17:46 < jrand0m> temos alguém procurando um projeto de Ciência da Computação?  ;)
17:46 < hezekiah> lol
17:46 < cohesion> jrand0m: sim, dá para fazer
17:47 < hezekiah> Eu, só daqui a alguns anos. ;-)
17:47 < jrand0m> legal, cohesion
17:47 < thecrypto> não por um ano
17:47  * cohesion volta ao trabalho
17:47 < jrand0m> valeu, cohesion
17:48 < jrand0m> ok, 1.6) próximas duas semanas.  na minha lista está colocar essas especificações,  docs e análises no ar.  Vou postar &amp; fazer commit assim que puder.
17:48 < jrand0m> LEIAM AS ESPECIFICAÇÕES E COMENTEM, POR FAVOR
17:48 < jrand0m> :)
17:48 < hezekiah> jrand0m: Certo. Quando eu tiver tempo, começo a ler. :)
17:48 < jrand0m> Eu preferiria que as pessoas publicassem comentários na lista, mas se  quiserem ser anônimas, me enviem comentários em particular e eu postarei respostas  na lista anonimamente.
17:49 < hezekiah> (Qual você acha que é o ETA para os arquivos do OpenOffice dos  docs estarem no CVS?)
17:49 < jrand0m> Posso fazer commit das últimas revisões em até 10 minutos após esta  reunião terminar.
17:49 < hezekiah> Ótimo. :)
17:50 < jrand0m> ok, é isso para 1.*.
17:50 < jrand0m> 2.x) comentários/perguntas/preocupações/desabafos?
17:50 < jrand0m> como está funcionando o mod do SDK, mihi?
17:51 < jrand0m> ou qualquer outra pessoa?  :)
17:51 < hezekiah> jrand0m: O que é esse mod do SDK de que você está falando?
17:52 < jrand0m> hezekiah> duas correções de bug no SDK, commitadas (&amp; postadas)  outro dia
17:52 < hezekiah> Ah
17:52 < hezekiah> Legal.
17:52 < jrand0m> (rotacionar os IDs de mensagem, sincronizar as gravações)
17:52 < hezekiah> Só no lado Java, ou no lado Python também?
17:52 < jrand0m> eu não falo python.
17:53 < hezekiah> lol
17:53 < jrand0m> não tenho certeza se os bugs existem lá.  você rotaciona os msgid a cada 255 mensagens e sincroniza suas gravações?
17:54 < hezekiah> Acho que o Python router faz ambos
17:54 < jrand0m> legal.
17:54 < jrand0m> te avisamos se não fizer ;)
17:54 < hezekiah> O que exatamente você quer dizer com "sincronizar suas gravações"?
17:55 < jrand0m> ou seja, garantir que múltiplas mensagens não sejam escritas para um cliente  ao mesmo tempo se houver vários clientes tentando enviar mensagens para  ele ao mesmo tempo.
17:55 < hezekiah> Todos os dados enviados pela conexão TCP são enviados na  ordem em que se originaram.
17:56 < hezekiah> Então você não vai receber 1/2 da mensagem A e depois 1/3 da mensagem B.
17:56 < jrand0m> 'k
17:56 < hezekiah> Você vai receber a mensagem A e depois a mensagem B.
17:56 < hezekiah> OK ... se mais ninguém for falar, sugiro que  encerremos a reunião.
17:56 < mihi> meu TCP/IP simples sobre I2p parece funcionar...
17:56 < jrand0m> niiiiice!!
17:56  * mihi estava ocioso um pouco, foi mal
17:57 < hezekiah> Mais alguém tem algo a dizer?
17:57 < jrand0m> mihi> então vamos poder rodar pserver por cima disso?
17:57 < mihi> contanto que você não tente criar muitas conexões de uma vez.
17:57 < mihi> jrand0m: acho que sim - consegui pegar o google por ele
17:57 < jrand0m> niiiice
17:57 < jrand0m> mihi++
17:57 < mihi> jrand0m-ava
17:57 < jrand0m> então você tem um outproxy e um inproxy?
17:58 < mihi> exatamente.
17:58 < jrand0m> legal
17:58 < mihi> o destination precisa de chaves, a source as gera sob demanda
17:58  * hezekiah entrega ao jrand0m o *baf*er. Arrebenta o troço quando terminar,  cara.
17:58 < jrand0m> certo.  com sorte, o serviço de nomes do co poderia ajudar com isso  quando estiver pronto.
17:59 < jrand0m> ok, legal.  mihi, avise a mim ou a qualquer outro se houver  algo em que possamos ajudar :)
17:59 < mihi> corrijam aquela coisa dos 128 msgid ou construam um suporte GUARANTEED  melhor
17:59  * jrand0m dá um *baf* na cabeça do nop_afk por ter um emprego de verdade
18:00 < mihi> jrand0m: abuso de baf custa 20 iodels
18:00 < jrand0m> lol
18:00 < jrand0m> suporte guaranteed melhor?
18:00 < jrand0m> (ou seja, melhor desempenho do que o descrito?  vamos corrigir  isso na impl)
18:00 < mihi> você testou meu caso de teste com start_thread=end_thread=300?
18:01 < mihi> ele gera muitas mensagens em uma direção, e isso faz com que  todos os msgid sejam consumidos...
18:01 < jrand0m> hmm, não, não tinha visto essa mensagem
18:01 < hezekiah> jrand0m: Seria razoável tornar o msgid de 2 bytes?
18:01  * jrand0m tentou o 200 / 201, mas isso está corrigido na última
18:01 -!- cohesion [cohesion@anon.iip] saiu [indo para a reunião do LUG]
18:01 < mihi> qual última?
18:01 < hezekiah> Então eles teriam 65535 msgid (se você não contar  o msgid 0)
18:01 < hezekiah> .
18:02 < jrand0m> IDs de mensagem de 2 bytes não fariam mal.  Estou confortável com  essa mudança.
18:02 < jrand0m> mihi> aquele que eu te enviei por e-mail
18:02 < mihi> se você tiver um mais recente do que o que me enviou, mande  (ou me dê acesso ao CVS)
18:03 < mihi> hmm, aquele falha para mim com 200/201 (assim como com 300)
18:03 < jrand0m> hmm.  vou fazer mais testes e depuração e te enviar por e-mail  o que eu encontrar.
18:03 < mihi> vlw.
18:04 < jrand0m> ok.
18:04  * jrand0m declara a reunião
18:04 < jrand0m> *baf*'ado
18:04  * hezekiah pendura o *baf*er com reverência em sua prateleira especial.
18:05  * hezekiah então gira, sai pela porta e a bate atrás de si. O baffer cai da prateleira.
18:05 < hezekiah> ;-)
--- Log fechado Ter Ago 19 18:05:36 2003 </div>
