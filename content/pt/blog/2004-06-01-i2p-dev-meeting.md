---
title: "Reunião de Desenvolvedores do I2P - 01 de junho de 2004"
date: 2004-06-01
author: "duck"
description: "Registro da reunião de desenvolvimento do I2P de 01 de junho de 2004."
categories: ["meeting"]
---

## Resumo rápido

<p class="attendees-inline"><strong>Presentes:</strong> deer, duck, hypercubus, Masterboy, mihi, Nightblade, tessier, wilde</p>

## Registro da Reunião

<div class="irc-log"> [22:59] &lt;duck&gt; Ter Jun  1 21:00:00 UTC 2004 [23:00] &lt;duck&gt; oi pessoal! [23:00] &lt;mihi&gt; oi duck [23:00] &lt;duck&gt; http://dev.i2p.net/pipermail/i2p/2004-June/000250.html [23:00] &lt;duck&gt; minha proposta: [23:00] * Masterboy entrou no #i2p

[23:00] &lt;duck&gt; 1) code progress [23:00] &lt;duck&gt; 2) featured content [23:00] &lt;duck&gt; 3) testnet status [23:00] &lt;duck&gt; 4) bounties [23:00] &lt;duck&gt; 5) ??? [23:00] &lt;Masterboy&gt; hi:) [23:00] &lt;duck&gt; . [23:01] &lt;duck&gt; since jrandom is off we'll have to do it ourself [23:01] &lt;duck&gt; (I know that he is logging and verifying our independency) [23:01] &lt;Masterboy&gt; no problem:P [23:02] &lt;duck&gt; unless there are problems with the agenda I propose that we stick to it [23:02] &lt;duck&gt; though there aint much that I can do if you dont :) [23:02] &lt;duck&gt; . [23:02] &lt;mihi&gt; ;) [23:02] &lt;duck&gt; 1) code progress [23:02] &lt;duck&gt; not much code submitted to cvs [23:02] &lt;duck&gt; I did win the trophy this week: http://duck.i2p/duck_trophy.jpg [23:03] * hypercubus has no cvs account yet [23:03] &lt;Masterboy&gt; and who did submit something? [23:03] &lt;duck&gt; anybody doing any secret coding? [23:03] * Nightblade has joined #I2P

[23:03] &lt;hypercubus&gt; BrianR estava trabalhando em algumas coisas
[23:04] &lt;hypercubus&gt; talvez eu já tenha improvisado uns 20% do instalador 0.4
[23:04] &lt;duck&gt; hypercubus: se você tiver algo então forneça diffs e o $dev fará o commit por você
[23:04] &lt;duck&gt; claro que os acordos de licença rigorosos se aplicam
[23:05] &lt;duck&gt; hypercubus: legal, algum problema / algo que valha mencionar?
[23:06] &lt;hypercubus&gt; ainda não, mas provavelmente vou precisar de algumas pessoas de BSD para testar os scripts shell do pré-instalador
[23:06] * duck revira algumas pedras
[23:06] &lt;Nightblade&gt; é só texto
[23:07] &lt;mihi&gt; duck: qual deles é você em duck_trophy.jpg?
[23:07] &lt;mihi&gt; ;)
[23:07] &lt;Nightblade&gt; o luckypunk tem FreeBSD, e meu ISP também tem FreeBSD, mas a configuração deles está meio bagunçada
[23:07] &lt;Nightblade&gt; digo, o ISP do meu host web, não a Comcast
[23:08] &lt;duck&gt; mihi: o da esquerda com óculos. o wilde é o da direita me entregando o troféu
[23:08] * wilde acena
[23:08] &lt;hypercubus&gt; você tem uma escolha... se você tiver o java instalado, pode pular o pré-instalador completamente...    se você não tiver o java instalado, pode executar o pré-instalador binário do linux ou o binário win32 (modo console), ou um    pré-instalador genérico em script para *nix (modo console)
[23:08] &lt;hypercubus&gt; o instalador principal lhe dá a opção de usar o modo console ou um modo GUI bacana
[23:08] &lt;Masterboy&gt; vou instalar FreeBSD em breve, então no futuro vou experimentar o instalador também
[23:09] &lt;hypercubus&gt; ok, bom... não sabia se alguém além do jrandom estava usando-o
[23:09] &lt;Nightblade&gt; no FreeBSD, o Java é invocado como "javavm" em vez de "java"
[23:09] &lt;hypercubus&gt; compilado a partir do código-fonte da Sun?
[23:09] &lt;mihi&gt; o FreeBSD suporta links simbólicos ;)
[23:10] &lt;hypercubus&gt; de qualquer forma, o pré-instalador binário está 100% completo
[23:10] &lt;hypercubus&gt; compila com gcj para nativo
[23:11] &lt;hypercubus&gt; ele só pede o diretório de instalação e obtém um JRE para você
[23:11] &lt;duck&gt; w00t
[23:11] &lt;Nightblade&gt; legal
[23:11] &lt;hypercubus&gt; o jrandom está empacotando um JRE personalizado para o i2p

[23:12] <deer> <j> .
[23:12] <Nightblade> se você instalar o java a partir da coleção de ports do freebsd, você usa um script wrapper chamado    javavm
[23:12] <deer> <r> .
[23:12] <hypercubus> de qualquer forma, este troço vai ser quase completamente automatizado
[23:12] <deer> <r> .
[23:12] <deer> <r> .
[23:12] <deer> <r> .
[23:12] <deer> <duck> r: corta isso
[23:12] <deer> <r> .
[23:12] <deer> <m> .
[23:13] <deer> <m> servidor de irc estúpido, não suporta pipelining :(
[23:13] <duck> hypercubus: tem alguma previsão para nós?
[23:14] <deer> <m> ops, o problema é "Nick change too fast" :(
[23:14] <hypercubus> ainda espero terminar em menos de um mês, antes que a 0.4 esteja madura para lançamento
[23:14] <hypercubus> embora no momento eu esteja compilando um novo SO para meu sistema de desenvolvimento, então vai levar alguns dias    antes de eu voltar ao instalador ;-)
[23:14] <hypercubus> sem preocupações, porém
[23:15] <duck> ok. então mais notícias na próxima semana :)
[23:15] <duck> mais algum código feito?
[23:15] <hypercubus> com sorte... a menos que a companhia elétrica me ferre de novo
[23:16] * duck vai para o #2
[23:16] <duck> * 2) conteúdo em destaque
[23:16] <duck> muito streaming de áudio (ogg/vorbis) feito esta semana
[23:16] <duck> baffled está rodando sua transmissão egoplay e eu também estou rodando uma transmissão
[23:16] <Masterboy> e funciona muito bem
[23:17] <duck> no nosso site você pode obter informações de como usar
[23:17] <hypercubus> tem algumas estatísticas aproximadas para nós?
[23:17] <duck> se você usar um player não listado lá e descobrir como usar, por favor me envie e eu vou    adicionar
[23:17] <Masterboy> duck, onde está o link para a transmissão do baffled no seu site?
[23:17] <Masterboy> :P
[23:17] <duck> hypercubus: 4kB/s vai muito bem
[23:18] <duck> e com ogg não é tãããão ruim
[23:18] <hypercubus> mas isso ainda parece ser a velocidade média?
[23:18] <duck> minha observação é que esse é o máximo
[23:18] <duck> mas é tudo ajuste de configuração
[23:19] <hypercubus> alguma ideia de por que isso parece ser o máximo?
[23:19] <hypercubus> e não estou falando só de streaming aqui
[23:19] <hypercubus> mas de downloads também
[23:20] <Nightblade> eu estava baixando alguns arquivos grandes ontem (alguns megabytes) do serviço de hospedagem    do duck e eu estava obtendo cerca de 4kb-5kb também
[23:20] <duck> acho que é o RTT
[23:20] <Nightblade> aqueles filmes do Chips
[23:20] <hypercubus> 4-5 parece uma melhoria em relação aos ~3 que tenho obtido consistentemente desde que comecei a usar i2p

[23:20] &lt;Masterboy&gt; 4-5kb não é ruim.. [23:20] &lt;duck&gt; com um windowsize de 1 não se fica muito mais rápido.. [23:20] &lt;duck&gt; windowsize&gt;1 recompensa: http://www.i2p.net/node/view/224 [23:21] &lt;duck&gt; mihi: talvez possa comentar? [23:21] &lt;hypercubus&gt; mas são 3 kbps notavelmente consistentes [23:21] &lt;mihi&gt; sobre o quê? windowsize&gt;1 com ministreaming: você é um mago se conseguir isso ;) [23:21] &lt;hypercubus&gt; sem soluços no medidor de largura de banda... uma linha bastante suave [23:21] &lt;duck&gt; mihi: sobre por que é tão estável em 4kb/s [23:21] &lt;mihi&gt; nenhuma ideia. não ouço som algum :( [23:22] &lt;duck&gt; mihi: para todas as transferências do i2ptunnel [23:22] &lt;Masterboy&gt; mihi você precisa configurar o plugin de streaming OGG.. [23:22] &lt;mihi&gt; Masterboy:? [23:23] &lt;mihi&gt; não, não há limite dentro do i2ptunnel quanto à velocidade. deve estar no router... [23:23] &lt;duck&gt; minha hipótese: tamanho máximo de pacote: 32kB, rtt de 5 segundos: 32kB/5s =~ 6.5kb/s [23:24] &lt;hypercubus&gt; parece plausível [23:25] &lt;duck&gt; ok.. [23:25] &lt;duck&gt; outro conteúdo: [23:25] * hirvox entrou em #i2p

[23:25] &lt;duck&gt; há um novo eepsite do Naughtious
[23:25] &lt;duck&gt; anonynanny.i2p
[23:25] &lt;duck&gt; a chave foi submetida ao CVS e ele colocou-a no wiki do ugha
[23:25] * mihi está ouvindo "sitting in the ..." - duck++
[23:25] &lt;Nightblade&gt; veja se você consegue abrir dois ou três streams a 4kb, aí você poderá dizer se está no router ou na biblioteca de streaming
[23:26] &lt;duck&gt; Naughtious: você aí? conte algo sobre seu plano :)
[23:26] &lt;Masterboy&gt; li que ele oferece hospedagem
[23:26] &lt;duck&gt; Nightblade: Eu tentei 3 downloads paralelos do baffled e recebi 3–4 kB cada
[23:26] &lt;Nightblade&gt; entendi
[23:27] &lt;mihi&gt; Nightblade: como você consegue saber isso então?
[23:27] * mihi gosta de ouvir no modo "stop&go" ;)
[23:27] &lt;Nightblade&gt; bem, se houver algum tipo de limitação no router que só o deixa lidar com 4 kB de cada vez
[23:27] &lt;Nightblade&gt; ou se é outra coisa
[23:28] &lt;hypercubus&gt; alguém pode explicar esse site anonynanny? eu não tenho um i2p router rodando no momento
[23:28] &lt;mihi&gt; hypercubus: só um wiki ou algo assim
[23:28] &lt;duck&gt; configuração do CMS Plone, criação de contas aberta
[23:28] &lt;duck&gt; permite upload de arquivos e coisas de site
[23:28] &lt;duck&gt; pela interface web
[23:28] &lt;Nightblade&gt; outra coisa a fazer seria testar a vazão do "repliable datagram" (datagrama com possibilidade de resposta), que, pelo que eu saiba, é o mesmo que os streams, mas sem acks
[23:28] &lt;duck&gt; provavelmente muito parecido com o Drupal
[23:28] &lt;hypercubus&gt; sim, já rodei o Plone antes
[23:29] &lt;duck&gt; Nightblade: estive pensando em usar o Airhook para gerenciá-los
[23:29] &lt;duck&gt; mas até agora só algumas ideias básicas
[23:29] &lt;hypercubus&gt; vale qualquer coisa para o conteúdo do wiki, ou foca em algo específico?
[23:29] &lt;Nightblade&gt; acho que o Airhook é sob GPL
[23:29] &lt;duck&gt; o protocolo
[23:29] &lt;duck&gt; não o código
[23:29] &lt;Nightblade&gt; ah :)
[23:30] &lt;duck&gt; hypercubus: ele quer conteúdo de qualidade e deixa você fornecer isso :)
[23:30] &lt;Masterboy&gt; faça upload do melhor pr0n seu que você tiver, hyper ;P
[23:30] &lt;duck&gt; ok
[23:30] * Masterboy vai tentar fazer isso também
[23:30] &lt;hypercubus&gt; é, qualquer um tocando um wiki aberto está pedindo conteúdo de qualidade ;-)
[23:31] &lt;duck&gt; ok
[23:31] * duck se move para o #3
[23:31] &lt;duck&gt; * 3) status da testnet
[23:31] &lt;Nightblade&gt; Airhook lida graciosamente com redes intermitentes, não confiáveis ou com atraso  &lt;-- hehe não é uma descrição otimista do I2P!
[23:31] &lt;duck&gt; como tem sido?
[23:32] &lt;duck&gt; vamos deixar a discussão de datagram sobre i2p para o final
[23:32] &lt;tessier&gt; Adoro sair por aí em wikis abertos e linkar isto: http://www.fissure.org/humour/pics/squirre   l.jpg
[23:32] &lt;tessier&gt; Airhook é demais
[23:32] &lt;tessier&gt; Tenho olhado para ele para construir uma rede p2p também.
[23:32] &lt;Nightblade&gt; parece estar estável para mim (#3)
[23:32] &lt;Nightblade&gt; o melhor que vi até agora
[23:33] &lt;duck&gt; sim
[23:33] &lt;mihi&gt; funciona bem — pelo menos para streaming de áudio stop&go
[23:33] &lt;duck&gt; vejo uptimes bem impressionantes no IRC
[23:33] &lt;hypercubus&gt; concordo... estou vendo muito mais caras azuis no console do router
[23:33] &lt;Nightblade&gt; mihi: você está ouvindo techno? :)
[23:33] &lt;duck&gt; mas é difícil dizer já que o bogobot não parece lidar com conexões que passam das 00:00
[23:33] &lt;tessier&gt; streaming de áudio funciona muito bem para mim, mas carregar sites geralmente precisa de várias tentativas
[23:33] &lt;Masterboy&gt; eu tenho a opinião de que o i2p roda muito bem após 6 horas de uso; na 6ª hora usei o IRC por 7 horas e assim meu router ficou rodando por 13 horas
[23:33] &lt;duck&gt; (*dica*)
[23:34] &lt;hypercubus&gt; duck: ahm... heheh
[23:34] &lt;hypercubus&gt; acho que eu poderia consertar isso
[23:34] &lt;hypercubus&gt; você tem o logging configurado para diário?
[23:34] &lt;duck&gt; hypercubus++
[23:34] &lt;hypercubus&gt; rotação de logs, isto é
[23:34] &lt;duck&gt; ah sim
[23:34] &lt;duck&gt; duck--
[23:34] &lt;hypercubus&gt; é por isso
[23:34] &lt;Nightblade&gt; eu estava no trabalho o dia todo, liguei meu computador, iniciei o i2p e estava no servidor IRC do duck em poucos minutos
[23:35] &lt;duck&gt; tenho visto uns DNFs esquisitos
[23:35] &lt;duck&gt; mesmo ao conectar aos meus próprios eepsites
[23:35] &lt;duck&gt; (http://dev.i2p.net/bugzilla/show_bug.cgi?id=74)
[23:35] &lt;duck&gt; acho que é isso que causa a maioria dos problemas agora
[23:35] &lt;hypercubus&gt; o bogoparser só vai analisar uptimes que ocorram inteiramente dentro de um único logfile... então, se o logfile abranger apenas 24 horas, ninguém vai aparecer como conectado por mais de 24 horas
[23:35] &lt;duck&gt; Masterboy e ughabugha também tiveram isso, acho...
[23:36] &lt;Masterboy&gt; sim
[23:36] &lt;duck&gt; (conserte isso e você vai ganhar o troféu da próxima semana com certeza!)
[23:37] &lt;deer&gt; &lt;mihi&gt; o bogobot está empolgado? ;)
[23:37] &lt;Masterboy&gt; eu testei meu site e às vezes quando eu dou refresh ele pega outra rota? e eu tenho que esperar carregar, mas eu nunca espero ;P eu aperto de novo e ele aparece instantaneamente
[23:37] &lt;deer&gt; &lt;mihi&gt; opa, foi mal. esqueci que isto é gated...
[23:38] &lt;duck&gt; Masterboy: os timeouts levam 61 segundos?
[23:39] &lt;duck&gt; mihi: bogobot configurado para rotações semanais agora
[23:39] * mihi saiu do IRC ("tchau, e tenham uma boa reunião")
[23:40] &lt;Masterboy&gt; desculpe, eu não chequei isso no meu site; quando eu não consigo acessar instantaneamente eu só dou refresh e ele carrega instantaneamente..
[23:40] &lt;duck&gt; hm
[23:40] &lt;duck&gt; bem, isso precisa ser consertado
[23:41] &lt;duck&gt; .... #4
[23:41] &lt;Masterboy&gt; acho que a rota não é a mesma a cada vez
[23:41] &lt;duck&gt; * 4) recompensas
[23:41] &lt;duck&gt; Masterboy: conexões locais deveriam ser encurtadas
[23:42] &lt;duck&gt; wilde teve algumas ideias de recompensas (bounties)... você aí?
[23:42] &lt;Masterboy&gt; talvez seja um bug na seleção de pares
[23:42] &lt;wilde&gt; não tenho certeza de que isso era para a pauta, de fato
[23:42] &lt;duck&gt; ah
[23:42] &lt;wilde&gt; ok, mas os pensamentos eram algo como:
[23:42] &lt;Masterboy&gt; acho que quando formos públicos o sistema de recompensas vai funcionar melhor
[23:43] &lt;Nightblade&gt; masterboy: sim, há dois tunnels para cada conexão, ou é assim que eu entendo lendo o router.config
[23:43] &lt;wilde&gt; poderíamos usar este mês para fazer uma divulgação pequena do i2p e aumentar um pouco o fundo de recompensas
[23:43] &lt;Masterboy&gt; dá para ver que o projeto Mute está indo bem — eles conseguiram US$ 600 e ainda não codaram muito ;P
[23:44] &lt;wilde&gt; mirar nas comunidades de liberdade, pessoas de cripto, etc
[23:44] &lt;Nightblade&gt; não acho que o jrandom queira publicidade
[23:44] &lt;wilde&gt; não atenção pública tipo Slashdot, não
[23:44] &lt;hypercubus&gt; é isso que observei também
[23:44] &lt;Masterboy&gt; quero empurrar isso de novo — quando formos públicos o sistema vai funcionar muito melhor ;P
[23:45] &lt;wilde&gt; Masterboy: recompensas poderiam acelerar o desenvolvimento do myi2p, por exemplo
[23:45] &lt;Masterboy&gt; e como o jr disse, nada de público até 1.0 e só um pouco de atenção depois de 0.4
[23:45] &lt;Masterboy&gt; *escreveu
[23:45] &lt;wilde&gt; quando tivermos tipo US$ 500+ por uma recompensa, as pessoas poderiam de fato sobreviver por algumas semanas
[23:46] &lt;hypercubus&gt; a parte complicada é que, mesmo se mirarmos uma comunidade pequena de devs, tipo *cof* os devs do Mute, essa galera pode divulgar o i2p mais do que gostaríamos
[23:46] &lt;Nightblade&gt; alguém poderia fazer uma carreira consertando bugs do i2p
[23:46] &lt;hypercubus&gt; e cedo demais
[23:46] &lt;wilde&gt; links do i2p já estão em muitos lugares públicos
[23:46] &lt;Masterboy&gt; você dá um Google e encontra o i2p

[23:47] &lt;hypercubus&gt; obscure public places ;-) (i saw the i2p link on a freesite... i'm lucky the damn freesite    even loaded!) [23:47] &lt;wilde&gt; http://en.wikipedia.org/wiki/I2p [23:47] &lt;Masterboy&gt; but i agree that no advertising till 0.4 is done [23:47] &lt;Masterboy&gt; wha??????? [23:47] &lt;wilde&gt; http://www.ovmj.org/GNUnet/links.php3?xlang=English [23:48] &lt;Masterboy&gt; protol0l does a great job;P [23:48] &lt;Masterboy&gt; ;)))))) [23:48] &lt;hypercubus&gt; nice typo ;-) [23:48] &lt;wilde&gt; ok anyway, I agree we should still keep I2P private (jr read this log ;) [23:49] &lt;Masterboy&gt; who did that? [23:49] &lt;Masterboy&gt; i think the Freenet crew discussion gave more attention.. [23:50] &lt;Masterboy&gt; and jr discussing with toad give a lot info to the big public.. [23:50] &lt;Masterboy&gt; so as in ughas wiki - we can all blame jr for that;P [23:50] &lt;wilde&gt; ok anyway, we'll see if we can bring in some $ without bringing in /. [23:50] &lt;Masterboy&gt; agreed [23:50] &lt;hypercubus&gt; the freenet dev list is hardly what i call the "big public" ;-) [23:50] &lt;wilde&gt; . [23:51] &lt;hypercubus&gt; wilde: you'll have a lot of $ sooner than you think ;-) [23:51] &lt;wilde&gt; oh come on, even my mum subscribe to freenet-devl [23:51] &lt;duck&gt; my mum reads through gmame [23:51] &lt;deer&gt; &lt;clayboy&gt; freenet-devl is being taught in schools here [23:52] &lt;wilde&gt; . [23:52] &lt;Masterboy&gt; so we will see more bounties after we go 0.4 stable.. [23:53] &lt;Masterboy&gt; that is after 2 months;P [23:53] &lt;wilde&gt; where did that duck go? [23:53] &lt;duck&gt; thanks wilde  [23:53] &lt;hypercubus&gt; though as the only bounty claimant thus far, i have to say that the bounty money had no    bearing on my decision to take up the challenge [23:54] &lt;wilde&gt; hehe, it would if it been 100x [23:54] &lt;duck&gt; wyou are too good for the world [23:54] &lt;Nightblade&gt; haha [23:54] * duck moves to #5 [23:54] &lt;hypercubus&gt; wilde, $100 doesn't mean shit to me ;-) [23:54] &lt;duck&gt; 100 * 10 = 1000 [23:55] * duck pops("5 airhook") [23:55] &lt;duck&gt; tessier: got any real-world experience with it [23:55] &lt;duck&gt; (http://www.airhook.org/) [23:55] * Masterboy will try dis out:P [23:56] &lt;duck&gt; java implementation (dunno if it even works) http://cvs.ofb.net/airhook-j/ [23:56] &lt;duck&gt; python implementation (a mess, did work in the past) http://cvs.sourceforge.net/viewcvs.py/khashmir   /khashmir/airhook.py [23:58] * duck opens the rant-valve [23:58] &lt;Nightblade&gt; j one is also gpl [23:58] &lt;duck&gt; port it to pubdomain [23:58] &lt;hypercubus&gt; amen [23:58] &lt;Nightblade&gt; the entire protocol doc is only about 3 pages - it can't be that hard [23:59] &lt;Masterboy&gt; nothing is hard [23:59] &lt;Masterboy&gt; it's just not easy [23:59] &lt;duck&gt; I dont think that it is fully specced though [23:59] * hypercubus takes away masterboy's fortune cookies [23:59] &lt;duck&gt; you might need to dive into the C code for a reference implementation [00:00] &lt;Nightblade&gt; I would do it myself but I am busy with other i2p stuff right now [00:00] &lt;Nightblade&gt; (and also my full-time job) [00:00] &lt;hypercubus&gt; duck: maybe a bounty for it? [00:00] &lt;Nightblade&gt; there already is [00:00] &lt;Masterboy&gt; ? [00:00] &lt;Masterboy&gt; ahh Pseudonyms [00:00] &lt;duck&gt; it could be used at 2 levels [00:00] &lt;duck&gt; 1) as a transport besides TCP [00:01] &lt;duck&gt; 2) as a protocol to handle datagrams inside i2cp/sam [00:01] &lt;hypercubus&gt; that's worth serious consideration then [00:01] &lt;hypercubus&gt; &lt;/obvious&gt;

[00:02] &lt;Nightblade&gt; duck: i noticed that the repliable datagram in SAM has a maximum size of 31kb, whereas the    stream has a maximum size of 32kb - making me think that the sender's destination is sent with each packet in    repliable datagram mode, and only at the beginning for a stream mode - [00:02] &lt;Masterboy&gt; well airhook cvs is not very updated.. [00:03] &lt;Nightblade&gt; making me think that it would be inefficient to make a protocol on top of the repliable    datagrams through sam [00:03] &lt;duck&gt; airhooks message size is 256 bytes, i2cp's is 32kb, so you need to atleast change a bit [00:04] &lt;Nightblade&gt; actually if you wanted to do the protocol in SAM you could just use the anoymous datagram    and have the first packet contain the sender's destination.... blah blah blah - i have lots of ideas but not    enough time to code them [00:06] &lt;duck&gt; then again you have to problems to verify signatures [00:06] &lt;duck&gt; so someone could send fake packages to you [00:06] &lt;Masterboy&gt; topic:::: SAM [00:06] &lt;Masterboy&gt; ;P [00:07] &lt;Nightblade&gt; true [00:08] &lt;Nightblade&gt; but if you sent back to that destination and there was no acknowledgement you'd know it was    a faker [00:08] &lt;Nightblade&gt; there woudl have to be a handshake [00:08] &lt;duck&gt; but you'll need aapplication level handshakes for that [00:08] &lt;Nightblade&gt; no not really [00:09] &lt;Nightblade&gt; just put it in a library for accessing SAM [00:09] &lt;Nightblade&gt; that is a bad way of doing though [00:09] &lt;Nightblade&gt; doing it though [00:09] &lt;duck&gt; you could also use seperated tunnels [00:09] &lt;Nightblade&gt; it shuold be in the streaming lib [00:11] &lt;duck&gt; yup. makes sense [00:12] &lt;duck&gt; ok [00:12] &lt;duck&gt; I am feeling *baff*-y [00:13] &lt;Nightblade&gt; ja [00:13] * duck *baffs* </div>
