---
title: "Reunião de desenvolvimento do I2P, 9 de setembro de 2003"
date: 2003-09-09
author: "jrand0m"
description: "57ª reunião de desenvolvimento do I2P abordando problemas de hospedagem de CVS, atualizações do serviço de nomes, status do desenvolvimento e questões sobre a especificação"
categories: ["meeting"]
---

<h2 id="quick-recap">Recapitulação rápida</h2>

<p class="attendees-inline"><strong>Presentes:</strong> Brownspider, co, jrand0m, mariesofie, mihi, shardy, w0rmus</p>

<h2 id="meeting-log">Registro da reunião</h2>

<div class="irc-log"> [22:57] <jrand0m> ok, boa noite srs e srtas
[22:57] <jrand0m> pauta:
[22:57] <jrand0m> 0) boas-vindas
[22:57] <jrand0m> 1) cvs
[22:57] <jrand0m> 4) serviço de nomes
[22:58] <co> Você esqueceu 5) perguntas.
[22:58] <jrand0m> 3) status do desenvolvimento
[22:58] <jrand0m> 2) perguntas sobre as especificações?
[22:58] <jrand0m> 5) outras perguntas?
[22:58] <jrand0m> ah, merda, esqueci de reordená-las.  ok.  estão numeradas errado :)  0 == 0, 1 == 1, 4 == 2, 3 == 3, 2 == 4, 5 == 5
[22:59] <jrand0m> vamos ver se consigo manter isso em ordem enquanto seguimos...
[22:59] <jrand0m> ok, 0) boas-vindas
[22:59] <shardy> viva os grupos de permutação!
[22:59] <jrand0m> bem-vindos à reunião 57
[22:59] <jrand0m> é, são todos só símbolos mesmo
[22:59] <w0rmus> maneiro, e aí ;0
[23:00] <w0rmus> Vou ajudar a compor a plateia
[23:00] <jrand0m> 1) o cvs ainda está fora do ar, após mais de 10 dias.  estamos procurando um novo host/servidor.
[23:00] <jrand0m> sf.net é uma droga, e não tenho motivo para acreditar que o nongnu da gnu seja melhor.
[23:00] <co> jrand0m: Por que não fazer esse host ter o alias "cvs.invisiblenet.net"?
[23:00] <jrand0m> nop está liderando a busca pelo novo host.
[23:01] <jrand0m> claro, co, assim que conseguirmos o servidor
[23:01] <shardy> do que vocês precisam para um host/servidor?
[23:01] <jrand0m> shardy> conexão de rede confiável, acesso ssh/cvs.  e um pouco de espaço em disco
[23:01] <shardy> vocês têm algo engatilhado?
[23:01] <shardy> porque, se não, talvez eu possa ajudar.
[23:02] <jrand0m> sensacional!  não sei o que o nop já tem engatilhado, mas vou pedir para ele falar com você (a menos que ele esteja aqui agora?)
[23:02] * w0rmus cutuca o nop
[23:03] <shardy> Tenho SDSL comercial de 1.1. Eu precisaria arrumar uma máquina. mas desde que vocês não usem quantidades absurdas de largura de banda, eu provavelmente poderia hospedar o servidor.
[23:03] <shardy> de quanto espaço em disco vocês precisariam?
[23:03] <jrand0m> o repositório atualmente tem ~ 6 Mb.  então provavelmente 50 M dariam conta do crescimento por um bom tempo
[23:04] <shardy> ah. pfft. isso não é nada.
[23:04] <shardy> e a máquina não precisaria ser super rápida?
[23:04] <shardy> vocês não fariam grandes compilações nela?
[23:04] <jrand0m> não, um 286 provavelmente daria conta.
[23:04] <jrand0m> não, estritamente cvs checking / checkout
[23:04] <jrand0m> (bem, e diff, e log, etc. ;)
[23:05] <jrand0m> "somos Java, não precisamos de fazendas de compilação" </fark>
[23:05] *** Desconexão: cohesion (class)
[23:05] <w0rmus> pessoas preocupadas com anonimato acessam o CVS usando algo como o JAP?  nunca usei CVS
[23:05] <jrand0m> w0rmus> eu uso cvs através de uma série privada de proxies ssh
[23:05] <co> jrand0m: Tenha em mente que uma implementação em C ou C++ pode ser provável no futuro.
[23:06] <mihi> pelo que eu saiba (AFAIK), o jap não permite acesso a cvs :(
[23:06] <w0rmus> tunelamento ssh
[23:06] <shardy> deixe-me ver o que posso fazer. alguém disse que ia me dar outro disco... se eu conseguir um disco eu tenho uma máquina que posso colocar no ar.
[23:06] <jrand0m> ah, claro, co.  só não espero que possamos exigir que um repositório cvs seja necessariamente também uma fazenda de compilação.
[23:07] <jrand0m> demais, shardy.  se houver algo que possamos fazer, é só falar.
[23:07] <co> jrand0m: Você está certo. Eles devem ser separados.
[23:07] <shardy> pode deixar. deixe-me catar um disco, devo conseguir um, e se conseguir eu ficaria feliz em hospedar o cvs para todos.
[23:07] <jrand0m> shardy++
[23:07] <w0rmus> viva ;0
[23:07] <jrand0m> ok, 4) serviço de nomes
[23:08] <jrand0m> co, como vai?
[23:08] <co> Ainda estou escrevendo, mas gostaria de dizer algumas palavras sobre isso.
[23:08] <co> Primeiro, para responder a uma pergunta do thecrypto durante a última reunião, o NS não fornece notificação de que alguém está online.
[23:09] <co> Ele apenas diz que uma pessoa pode ser contatada por certos métodos, como AIM.
[23:09] <co> Segundo, o lado do cliente.
[23:09] <co> Haverá uma API que os programas podem usar para fazer consultas a servidores de nomes.
[23:10] <co> O mecanismo subjacente lerá um arquivo de configuração com quais servidores consultar, usará a rede I2P para obter os resultados e repassará os resultados ao chamador.
[23:11] <co> O mecanismo subjacente também lerá, de um arquivo, o mecanismo de destino para o router local contatar.
[23:11] <jrand0m> o mecanismo de destino?
[23:11] <co> desculpe, o endereço de destino.
[23:11] <jrand0m> ah, blz
[23:12] <co> Isso é tudo por enquanto.
[23:12] <jrand0m> legal
[23:12] <w0rmus> concordo
[23:12] <w0rmus> ;)
[23:12] <jrand0m> alguma ideia aproximada de prazos para vários marcos?
[23:13] <jrand0m> obviamente nada a que alguém pudesse lhe cobrar, claro, só curiosidade
[23:13] <co> Digamos fim da semana para terminar a especificação e publicá-la e a API.
[23:14] * mariesofie chega atrasada
[23:14] <jrand0m> ah, legal, co
[23:14] <co> Depois, vou começar a implementar. Não tenho certeza de quanto tempo isso vai levar, porém.
[23:14] <jrand0m> compreensível
[23:15] <jrand0m> mais alguém tem perguntas/ideias sobre o serviço de nomes?
[23:15] <jrand0m> ok, 3) status do desenvolvimento
[23:16] <jrand0m> o desenvolvimento vai bem.
[23:16] <jrand0m> o lado Java está conforme a especificação e implementa todas as mensagens e estruturas I2CP e I2NP
[23:17] <jrand0m> a arquitetura em Java em si está funcional e vou continuar a criar stubs para os diversos subsistemas
[23:17] <co> Você testou?
[23:17] <jrand0m> as mensagens &amp; estruturas?  sim, via o harness TestData em net.invisiblenet.i2p.data.test
[23:17] <co> Quero dizer conectar dois computadores diferentes com I2P.
[23:18] <jrand0m> ah, não, isso requer a implementação completa do subsistema de comunicação
[23:18] <co> entendo.
[23:18] <jrand0m> primeiro estou construindo os vários subsistemas para operar em modo de teste, depois implementando os vários subsistemas para que possam operar isoladamente
[23:19] <jrand0m> provavelmente estamos a 2 semanas de um cliente enviar uma mensagem para um cliente em um router diferente
[23:19] * mariesofie vibra
[23:20] <jrand0m> ainda há muito trabalho a ser feito depois disso antes da versão alpha, mas é progresso
[23:21] <jrand0m> as especificações de estruturas de dados e de i2np precisam de cerca de uma dúzia de pequenas modificações que venho acumulando durante a implementação para corrigir coisas que passaram batido.  por exemplo, "datastructures p11, TunnelSigningPublic/PrivateKey should contain SIGNING Public/Private keys" e "i2np p15, TunnelCreateStatus - add hash of the replying RouterIdentity"
[23:21] <shardy> cara. eu realmente preciso estudar as especificações.
[23:22] <jrand0m> bem, em breve estarão hospedadas na sua máquina, então vai ser fácil :)
[23:22] <w0rmus> haha
[23:22] <w0rmus> eu também não terminei as especificações
[23:23] <mariesofie> imprimi as especificações, li tantas vezes que elas se desgastaram e tive que imprimir outra cópia
[23:23] <jrand0m> pelas discussões que tive com várias pessoas, percebi que as especificações não são tão boas em transmitir como a coisa realmente funciona. elas cobrem a parte nebulosa e os detalhes minuciosos, mas não o porquê desses detalhes atenderem ao porquê
[23:23] <w0rmus> heh
[23:23] <jrand0m> rofl mariesofie
[23:23] <jrand0m> ok, é isso para 3) status do desenvolvimento
[23:24] <jrand0m> agora 2) perguntas sobre as especificações
[23:24] <w0rmus> acho que vou lê-las em vez daquele cálculo idiota
[23:24] <co> estou pensando um pouco no futuro.
[23:24] <co> As implementações em Python e em C ou C++ precisarão ter dados de mensagens legíveis pela implementação em Java.
[23:24] *** Desconexão: mihi (EOF do cliente)
[23:25] <jrand0m> correto, co
[23:25] <co> Como você vai conseguir isso?
[23:25] <jrand0m> a especificação de estruturas de dados define especificamente os layouts de bytes
[23:25] <jrand0m> e tudo é big endian e todos os números são sem sinal (unsigned)
[23:25] <mariesofie> para que nível de conhecimento técnico vocês estão direcionando as especificações? qualquer pessoa com conhecimento razoável de computação? estudantes de engenharia de CS em nível universitário?
[23:25] <co> ah, certo.
[23:25] *** mihi_ (~none@anon.iip) entrou no canal #iip-dev
[23:26] <mariesofie> ou seja, qual é o público-alvo?
[23:26] *** mihi_ agora é conhecido como mihi
[23:26] <jrand0m> mariesofie> bem, aquelas especificações foram realmente direcionadas de maneira meio aleatória.  i2p_philosophy era o "ok, wtf é isso afinal", mas o resto das especificações foi direcionado a pessoas interessadas em realmente implementar o sistema
[23:26] <jrand0m> nós realmente, realmente precisamos de alguns docs que fiquem no meio-termo
[23:27] <mariesofie> entendi
[23:27] <mariesofie> achei que a documentação da API é muito fácil de entender e útil, mas ironicamente ainda me confundo ao ler as especificações de I2NP tentando entender a arquitetura central
[23:28] <mariesofie> talvez isso diga mais sobre mim do que sobre a documentação :)
[23:28] <jrand0m> heh nerd :)
[23:29] <jrand0m> ok, mais alguma pergunta sobre as especificações?  vamos passar para 5) outras perguntas
[23:29] <jrand0m> alguém tem mais alguma pergunta?  este é nosso último item na pauta da reunião
[23:30] <w0rmus> fico me perguntando onde o thecrypto está com o achat
[23:30] <jrand0m> ah, o thecrypto ficará offline pelas próximas três semanas ou algo assim
[23:30] <mihi> o que acontece com a revisão por pares?
[23:30] <w0rmus> ou atalk
[23:30] <w0rmus> uau
[23:30] <mihi> alguém está revisando?
[23:30] <mariesofie> achei que o thecrypto tinha 2 horas por dia
[23:31] <w0rmus> e eu nem consigo ver os códigos que ele tem :(
[23:31] <jrand0m> mihi> os documentos foram enviados para várias pessoas para revisão e, à medida que o feedback vier, será tratado.
[23:31] <jrand0m> w0rmus> você tem alguma pergunta sobre o ATalk?
[23:32] <shardy> vou revisar assim que tiver tempo :)
[23:32] <mihi> quis dizer, veio algum feedback até agoraß
[23:32] <w0rmus> acho que não
[23:32] <mihi> s/nowß/now?/
[23:32] <jrand0m> mihi> em grande parte na forma de discussões e esclarecimentos
[23:32] <jrand0m> sensacional, shardy :)
[23:33] <Brownspider> feliz aniversário, google
[23:33] <jrand0m> mariesofie> certo, mas isso nem é tempo suficiente para ele fazer o d/l da documentação da linguagem Java para continuar o desenvolvimento :/
[23:33] <w0rmus> ahaha wtf
[23:35] <jrand0m> ok, mais alguma pergunta / ideia?
[23:35] <w0rmus> acho que devo mencionar que nunca programei fora da escola
[23:35] <w0rmus> mas tenho que começar em algum lugar de qualquer maneira
[23:35] <jrand0m> agora é uma boa hora para começar :)
[23:35] <jrand0m> isso aí
[23:35] <w0rmus> ;0
[23:35] <mariesofie> eu tenho perguntas sobre a API, mas ainda não; em um ou dois dias, quando eu puder testá-la mais
[23:35] <w0rmus> fiz uns 2 anos de Java ou algo assim
[23:36] <jrand0m> ok, legal, mariesofie, é só mandar uma msg para a lista ou me mandar uma mensagem aqui quando quiser
[23:37] <co> mariesofie: Você leu a discussão na lista de e-mails iip-dev?
[23:37] <w0rmus> onde isso está arquivado?
[23:37] <jrand0m> http://news.gmane.org/thread.php?group=gmane.comp.security.invisiblenet.iip.devel
[23:37] <jrand0m> (tráfego relativamente baixo no momento)
[23:38] <Brownspider> jrand0m quer que você codifique algo que não pode logicamente existir, para despedaçar o mundo, para acabar com o reinado de deus.
[23:38] <shardy> meus serviços continuam à disposição se vocês precisarem de quaisquer núcleos de criptografia ou similares escritos ou depurados.
[23:39] *** M123456789 (~no@anon.iip) entrou no canal #iip-dev
[23:39] <co> Brownspider: hã?
[23:39] <Brownspider> co, isso estava no freesite dele, deixa pra lá
[23:40] <jrand0m> ótimo, shardy, tenho a sensação de que vamos precisar de alguns quando os routers estiverem em funcionamento, e especialmente quando colocarmos as APIs de C/Python novamente em conformidade com a especificação
[23:40] <mariesofie> co> eu só li até mais ou menos a edição #52
[23:42] <jrand0m> ok.  últimas palavras (enquanto eu olho para o *baf*er...)
[23:43] *** mihi_backup_ (~none@anon.iip) entrou no canal #iip-dev
[23:43] *** Desconexão: mihi_backup (EOF do cliente)
[23:43] *** mihi_backup_ agora é conhecido como mihi_backup
[23:43] <jrand0m> ok, ótimo.  semana que vem, mesmo bat-horário, mesmo bat-local.
[23:44] * jrand0m *baf*a a reunião para um fim

</div>

