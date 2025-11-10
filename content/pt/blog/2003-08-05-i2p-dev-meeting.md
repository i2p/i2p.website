---
title: "Reunião de desenvolvedores do I2P, 5 de agosto de 2003"
date: 2003-08-05
author: "nop"
description: "52ª reunião de desenvolvedores do I2P abordando o status do desenvolvimento em Java, as atualizações de criptografia e o progresso do SDK"
categories: ["meeting"]
---

<h2 id="quick-recap">Resumo rápido</h2>

<p class="attendees-inline"><strong>Presentes:</strong> hezekiah, jeremiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">Registro da Reunião</h2>

<div class="irc-log"> <nop>	ok, reunião iniciada <nop>	o que está na pauta -->	logger (logger@anon.iip) entrou em #iip-dev -->	Anon02 (~anon@anon.iip) entrou em #iip-dev <hezekiah>	Tue Aug  5 21:03:10 UTC 2003 <hezekiah>	Bem-vindos à enésima reunião do iip-dev. <hezekiah>	O que está na pauta? <thecrypto>	Tue Aug  5 21:02:44 UTC 2003 <thecrypto>	sincronizado com um servidor NTP stratum 2 :) <hezekiah>	Tue Aug  5 21:03:13 UTC 2003 -->	ptm (~ptm@anon.iip) entrou em #iip-dev <hezekiah>	Acabei de sincronizar com o NIST. :) <mihi>	essa sincronização não ajuda com os atrasos do iip ;) <jrand0m>	nop: coisas que quero ver abordadas: status do dev em java, status da cripto 	  em java, status do dev em python, status do sdk, serviço de nomes <hezekiah>	(Vamos entrar no serviço de nomes _já_?) <jrand0m>	não é sobre design, seu idiota, isso é o papo do co.  apenas fale sobre 	  coisas se houver coisas sobre as quais falar. <hezekiah>	Ah *	jrand0m guarda o LART <jrand0m>	mais alguma coisa na pauta? <jrand0m>	ou vamos começar? <hezekiah>	Bem, não consigo pensar em mais nada para acrescentar. <hezekiah>	Ah! <hezekiah>	Oh! <jrand0m>	ok.  status do dev em java: <hezekiah>	Bom. <--	mrflibble saiu (tempo limite de ping) <nop>	ok <nop>	pauta <nop>	1) Boas-vindas <jrand0m>	a partir de hoje, há uma API de cliente em java com um router java stub 	  que podem se comunicar entre si.  além disso, há um aplicativo chamado ATalk 	  que permite IM (mensagens instantâneas) anônimas + transferência de arquivos. <nop>	2) apagões do IIP 1.1 <nop>	3) I2P <nop>	4) O Fim com comentários e outras coisas *	jrand0m volta para o canto <nop>	desculpe 	  joeyo jrand0m Aug 05 17:08:24 * hezekiah dá a jrand0m um chapéu de burro para usar 	  no canto. ;-) <nop>	desculpem por isso <nop>	não vi que você tinha começado aí <nop>	talvez eu devesse ir para o canto <hezekiah>	lol <jrand0m>	sem problema.  item 1) *	hezekiah entrega um chapéu de burro ao nop também. :) <nop>	ok bem-vindos todos <nop>	blá blá <nop>	2) apagões do IIP 1.1 -->	mrflibble (mrflibble@anon.iip) entrou em #iip-dev <hezekiah>	52ª reunião do iip-dev e todo esse besteirol bom! <nop>	o servidor recentemente teve alguns problemas com setores do disco rígido e foi 	  substituído <nop>	planejo mover o maldito servidor para um ambiente mais estável, com 	  redundância <nop>	e possivelmente ceder o controle de múltiplos servidores ircd <nop>	não sei <nop>	isso é algo a ser discutido <--	Anon02 saiu (EOF do cliente) <nop>	com sorte nossos servidores devem ficar no ar agora, já que o disco rígido foi substituído <nop>	desculpem pelo inconveniente, pessoal <nop>	3) I2P - Jrand0m, é com você <nop>	saia do canto, jrand0m *	hezekiah vai até o canto, puxa jrand0m da cadeira, arrasta-o 	  para o púlpito, tira-lhe o chapéu de burro e entrega-lhe o microfone. *	nop vai para aquele canto para ocupar o lugar dele <hezekiah>	lol! <jrand0m>	foi mal, voltei *	nop pega o chapéu de burro do hezekiah *	nop coloca-o na cabeça *	nop aplaude o jrand0m *	jrand0m apenas assiste ao show <jrand0m>	er... hum ok <hezekiah>	jrand0m: i2p, status do java, etc. Fala, cara! <jrand0m>	então, a partir de hoje, há uma API de cliente em java com um router java 	  stub que podem se comunicar entre si.  além disso, há um aplicativo chamado 	  ATalk que permite IM (mensagens instantâneas) anônimas + transferência de arquivos. <hezekiah>	Transferência de arquivos já!? <jrand0m>	sim, sr <hezekiah>	Uau. <hezekiah>	Estou claramente por fora. <jrand0m>	mas não é dos mais elegantes <hezekiah>	lol <jrand0m>	ele pega um arquivo e o joga dentro de uma mensagem <hezekiah>	Ai. <nop>	quanto tempo levou a transferência local de 1.8 mb? <jrand0m>	eu testei com um arquivo de 4K e um arquivo de 1.8Mb <jrand0m>	alguns segundos <nop>	legal <nop>	:) <hezekiah>	As coisas em java já fazem criptografia de verdade, ou ainda 	  fingem isso? <nop>	fingem <nop>	até eu sei disso <nop>	:) <jrand0m>	eu dei uma aquecida falando comigo mesmo primeiro [ex.: uma janela para 	  outra, dizendo oi], assim não lidou com a sobrecarga do primeiro elg <jrand0m>	isso, é em grande parte falso <thecrypto>	a maior parte da criptografia é falsa <thecrypto>	mas isso está sendo trabalhado <hezekiah>	Claro. :) <jrand0m>	com certeza. <jrand0m>	nesse aspecto, quer nos dar uma atualização, thecrypto? <thecrypto>	bem, por enquanto terminei ElGamal e SHA256 <thecrypto>	agora estou trabalhando na geração de primos para DSA <thecrypto>	vou enviar 5 e então podemos simplesmente escolher um <hezekiah>	nop: você não tinha primos prontos para uso com DSA? <thecrypto>	também temos alguns benchmarks de ElGamal e SHA256 <thecrypto>	e todos são rápidos <jrand0m>	benchmarks mais recentes com elg: <jrand0m>	Tempo médio de geração de chave: 4437	total: 443759	mín: 	  872	   máx: 21110	   Geração de chaves/segundo: 0 <jrand0m>	Tempo médio de criptografia    : 356	total: 35657	mín: 	  431	   máx: 611	   Criptografia Bps: 179 <jrand0m>	Tempo médio de descriptografia    : 983	total: 98347	mín: 	  881	   máx: 2143	   Descriptografia Bps: 65

<hezekiah>	min e max: são em segundos?
<jrand0m>	observe que o Bps não é realmente útil, já que só criptografamos/descriptografamos 64 bytes
<thecrypto>	ms
<jrand0m>	não, desculpa, são todos milissegundos
<hezekiah>	Legal. :)
<hezekiah>	E isso é feito em java?
<thecrypto>	sim
<thecrypto>	java puro
<hezekiah>	OK. Estou oficialmente impressionado. :)
<jrand0m>	100%.  P4 1.8
<thecrypto>	são mais ou menos iguais no meu 800 Mhz
<hezekiah>	Como posso fazer os mesmos testes?
<jrand0m>	benchmark de sha256:
<jrand0m>	Short Message Time Average  : 0 total: 0	min: 0	max: 	  0  Bps: NaN
<jrand0m>	Medium Message Time Average : 1 total: 130	min: 0	max: 	  10 Bps: 7876923
<jrand0m>	Long Message Time Average   : 146	total: 14641	min: 	  130	   max: 270	   Bps: 83037
<thecrypto>	execute o programa ElGamalBench
<hezekiah>	OK.
<hezekiah>	Vou procurá-lo.
<jrand0m>	(tamanho curto: ~10 bytes, médio ~10KB, longo ~ 1MB)
<jrand0m>	java -cp i2p.jar ElGamalBench
<jrand0m>	(depois de executar "ant all")
<hezekiah>	jrand0m: Obrigado. :)
<jrand0m>	sem problema
<thecrypto>	Essa coisa de NaN significa que é tão rápido que acabamos dividindo por 0 — é tão rápido :)
<hezekiah>	Qual é o benchmark de sha?
<jrand0m>	java -cp i2p.jar SHA256Bench -->	Neo (anon@anon.iip) entrou em #iip-dev
<hezekiah>	OK.
<jrand0m>	provavelmente vamos querer mover isso para serem métodos main() dos mecanismos associados, mas estão bons onde estão por enquanto
<hezekiah>	Vamos ver quão rápido tudo isso é em um AMD K6-2 333MHz (que é um chip não muito conhecido por sua aritmética de inteiros.)
<jrand0m>	hehe
<jrand0m>	ok, então faltam DSA e AES, certo?
<jrand0m>	isso tudo está incrível, thecrypto.  bom trabalho.
<thecrypto>	sim
<jrand0m>	posso te importunar por um ETA dos outros dois?  ;)
<hezekiah>	Se isso for perto de tão rápido na minha máquina quanto é na sua, você tem que me mostrar como você faz isso. ;-)
<thecrypto>	DSA deve ficar pronto quase assim que eu tiver os primos prontos
<nop>	hezekiah, você já tentou o sslcrypto para python
<thecrypto>	copiando algum código do gerador de primos e coisas assim e fica pronto
<nop>	aquele do link
<hezekiah>	nop: sslcrypto não vai nos servir de nada.
<hezekiah>	nop: ele não implementa ElGamal _ou_ AES _ou_ sha256.
<thecrypto>	AES está quase pronto, exceto que há algum erro em algum lugar que ainda estou tentando identificar e eliminar; assim que resolver isso, estará pronto
<jrand0m>	thecrypto> então até sexta, DSA keygen, sign, verify, e AES encrypt, decrypt para entradas de tamanho arbitrário?
<nop>	aquele no site do McNab não?
<thecrypto>	sim
<nop>	droga
<thecrypto>	deve ser sexta
<thecrypto>	mais provavelmente quinta
<jrand0m>	thecrypto> isso inclui as coisas de UnsignedBigInteger?
<thecrypto>	vou perder a reunião da próxima semana por causa do acampamento de verão, e volto depois disso
<thecrypto>	jrand0m: provavelmente não
<jrand0m>	ok.
<jrand0m>	então, por enquanto, a interoperabilidade entre java e python está b0rked.
<jrand0m>	para crypto, isto é.
---	Notificação: jeremiah está online (anon.iip).
-->	jeremiah (~chatzilla@anon.iip) entrou em #iip-dev
<jrand0m>	(ou seja, para assinaturas, chaves, criptografia e descriptografia)

<nop>	hmm talvez devêssemos focar mais em C/C++
<thecrypto>	bem, uma vez que tivermos isso funcionando completamente, podemos então garantir 	  que tanto Java quanto Python consigam se comunicar entre si
<jrand0m>	enquanto você estiver fora, vou analisar a parte sem sinal.
<jeremiah>	alguém pode me enviar por e-mail um backlog? jeremiah@kingprimate.com
<hezekiah>	jeremiah: Me dá um minuto. :)
<jrand0m>	nop> temos devs para C/C++?
<nop>	Tenho um cara, sim
<nop>	e sabemos que o Hezekiah poderia fazer isso
<jrand0m>	ou talvez possamos obter uma atualização do status do dev de python do hezekiah + 	  jeremiah para ver quando teremos mais gente para o dev em c/c++
<jrand0m>	certo, claro.  mas hez+jeremiah estão trabalhando em python no momento 	  (certo?)
<hezekiah>	Sim.
<--	mrflibble saiu (Tempo limite de ping)
<hezekiah>	Estou meio que dando muito trabalho para o pobre jeremiah.
<nop>	Eu só estava dizendo que se python não tiver altas velocidades
<hezekiah>	Python é principalmente para eu entender esta rede.
<nop>	ahh
<hezekiah>	Assim que eu fizer com que ele basicamente siga a especificação completa, pretendo 	  repassar para o jeremiah fazer como achar melhor.
<hezekiah>	Não é para ser uma implementação de ponta da especificação.
<hezekiah>	(Se eu quisesse isso, usaria C++.)
<jeremiah>	bem, não há partes realmente intensivas de processador no app, 	  se bem me lembro, além de criptografia, e idealmente isso será tratado em C de qualquer forma, certo?
<jrand0m>	claro jeremiah.tudo depende do app
-->	mrflibble (mrflibble@anon.iip) entrou em #iip-dev
<hezekiah>	jeremiah: Em teoria.
<jrand0m>	então, onde estamos no lado python?  API do cliente, router apenas local 	  , etc?
<jeremiah>	a implementação em python também vai nos permitir saber quais otimizações 	  poderíamos fazer desde o início... Eu gostaria de mantê-la atualizada ou, possivelmente, 	  à frente da implementação em C, na medida do possível
<hezekiah>	jrand0m: OK. Eis o que eu tenho.
<hezekiah>	Em _teoria_ o router deve ser capaz de lidar com todas as mensagens não administrativas 	  de um cliente.
<hezekiah>	No entanto, ainda não tenho cliente, então não consegui depurar 	  isso (ou seja, ainda há bugs.)
<hezekiah>	Estou trabalhando no cliente agora.
<jrand0m>	'k.  se você puder desativar a verificação de assinatura, devemos conseguir 	  rodar o cliente Java contra isso agora
<hezekiah>	Espero ter isso pronto, exceto pelas mensagens de admin, em um dia 	  ou dois.
<jrand0m>	podemos testar isso depois da reunião
<hezekiah>	jrand0m: OK.
<jeremiah>	Tenho lidado com coisas do mundo real desde a última 	  reunião, posso trabalhar na API do cliente, só tenho tentado sincronizar meu pensamento 	  com o do hezekiah
<jrand0m>	legal
<hezekiah>	jeremiah: Quer saber, só espera.
<hezekiah>	jeremiah: Provavelmente estou jogando coisas novas demais para você 	  lidar agora.
<jeremiah>	hezekiah: certo, o que eu ia dizer é que você 	  provavelmente deveria simplesmente seguir em frente e implementar o básico
<hezekiah>	jeremiah: Em pouco tempo, isso vai estar estabilizado e você pode 	  começar a refinar. (Há muitos comentários TODO que precisam de ajuda.)
<jeremiah>	e então eu posso estendê-lo depois, assim que entender o todo
<hezekiah>	Exatamente.
<hezekiah>	Você é quem vai manter todo esse código. :)
<jrand0m>	legal.  então ETA de 1–2 semanas para um router python funcionando + API do cliente?
<hezekiah>	Vou sair de férias na próxima semana, então provavelmente.
<hezekiah>	Vamos ter mais detalhes de router para router em breve?
<jrand0m>	não.
<jrand0m>	bem, sim.
<jrand0m>	mas não.
<hezekiah>	lol
<jeremiah>	hezekiah: quanto tempo são as férias?
<hezekiah>	1 semana.
<jeremiah>	ok
<jrand0m>	(aka assim que o SDK sair, 100% do meu tempo vai para I2NP)
<hezekiah>	Espero ter toda a funcionalidade não administrativa escrita antes de eu 	  sair de férias
<hezekiah>	.
<jrand0m>	mas então, pouco depois de você voltar, você vai para a faculdade, certo?
<hezekiah>	I2NP?
<hezekiah>	Certo.
<jrand0m>	proto de rede
<hezekiah>	Tenho cerca de 1 semana depois das férias.
<hezekiah>	Depois disso, eu vou embora.
<hezekiah>	E meu tempo livre despenca como uma pedra.
<jrand0m>	então essa 1 semana deve ser só depuração
<jeremiah>	Posso trabalhar no código enquanto o hez estiver fora, porém
<jrand0m>	isso aí
<jrand0m>	como vai ser seu verão, jeremiah?
<hezekiah>	jeremiah: Talvez você consiga colocar essas funções de admin para funcionar?

<thecrypto>	ainda vou ter um mês depois que eu voltar das minhas férias para trabalhar 	  nas coisas
<jrand0m>	ter uma vida, ou ser como o resto de nós l00sers?  :)
<jeremiah>	talvez
<hezekiah>	100sers?
<hezekiah>	O que é um 100ser?
<jeremiah>	eu vou para a faculdade no dia 22; fora isso eu posso desenvolver
<mihi>	hezekiah: um perdedor
<jeremiah>	e na última semana antes de eu ir, todos os meus amigos vão ter ido embora... então 	  posso entrar em modo hyperdev
<hezekiah>	mihi: Ah!
<jrand0m>	hehe
<hezekiah>	OK. Então, onde estávamos na pauta?
<hezekiah>	isto é, o que vem agora?
<jrand0m>	status do SDK
<jrand0m>	sdk == uma impl de cliente, uma impl de router apenas local, um app e docs.
<jrand0m>	Eu gostaria de lançar isso até a próxima terça.
<hezekiah>	jeremiah: Esse backlog está a caminho. Desculpa, esqueci de você ali. :)
<jeremiah>	obrigado
<jrand0m>	ok, o co não está por aqui, então a parada do serviço de nomes provavelmente está meio 	  fora de base
<jrand0m>	podemos discutir o serviço de nomes depois que ele soltar as especificações ou 	  quando ele estiver por aqui
<jrand0m>	ok, isso é tudo de coisas do I2P
<jrand0m>	mais alguém tem coisas de I2P, ou vamos para:
<nop> 4) O Fim com 	  comentários e tal
<hezekiah>	Não consigo pensar em nada.
<jrand0m>	Presumo que todo mundo viu 	  http://www.cnn.com/2003/TECH/internet/08/05/anarchist.prison.ap/index.html ?
<thecrypto>	aqui não
<jrand0m>	(nop postou aqui mais cedo)
<hezekiah>	Aquilo do cara que foi preso por colocar link para um site de construção de bombas?
<jrand0m>	sim
<jrand0m>	A relevância para a necessidade de colocar o I2P no ar ASAP deve estar aparente ;)
<hezekiah>	OK! jeremiah, aqueles logs foram enviados agora.
<jeremiah>	obrigado
<jrand0m>	alguém tem perguntas / comentários / ideias / frisbees, 	  ou estamos tendo uma reunião curta recorde?
*	thecrypto arremessa um frisbee
<--	logger saiu (Ping timeout)
<jrand0m>	caramba, vocês estão quietos hoje ;)
<mihi>	pergunta:
<mihi>	onde os não-devs podem conseguir seu código Java?
<jrand0m>	sim sr?
<thecrypto>	ainda não
<mihi>	404
<jrand0m>	isso vai ficar disponível quando estivermos prontos para o release.  aka o 	  código-fonte vai sair junto com o SDK
<jrand0m>	heh
<jrand0m>	é, a gente não usa SF
<hezekiah>	nop: É possível conseguirmos um CVS anônimo funcionando alguma hora?
<hezekiah>	tempo?
<--	mrflibble saiu (Ping timeout)
<nop>	bem, eu abriria uma porta não padrão
<jrand0m>	hezekiah> teremos isso assim que o código tiver a licença GPL lá
<nop>	mas eu estou trabalhando no viewcvs
<jrand0m>	aka não agora, já que o doc da gpl ainda não foi adicionado ao código
<hezekiah>	jrand0m: Está em todos os diretórios de código python e todos os arquivos 	  fonte python especificam licenciamento sob GPL-2.
<jrand0m>	hezekiah> isso está no cathedral?
<hezekiah>	Sim.
<jrand0m>	ah, saquei.  i2p/core/code/python ?  ou um módulo diferente?
*	jrand0m não viu isso lá
<hezekiah>	Cada diretório de código python tem um arquivo COPYING nele com a 	  GPL-2 e cada arquivo fonte tem a licença definida como GPL-2
<hezekiah>	É i2p/router/python e i2p/api/python
<jrand0m>	'k
<jrand0m>	então, é, até terça que vem teremos o SDK + acesso público ao código-fonte.
<hezekiah>	Legal.
<hezekiah>	Ou como você gosta de dizer, wikked. ;-)
<jrand0m>	heh
<jrand0m>	nada mas?
<hezekiah>	nada mas? O que isso significa!?
<jeremiah>	nada mais
*	jrand0m sugere que você aprenda um pouco de espanol en universidad
-->	mrflibble (mrflibble@anon.iip) entrou em #iip-dev
<hezekiah>	Perguntas, alguém?
<hezekiah>	Uma vez!
<--	ptm (~ptm@anon.iip) saiu de #iip-dev (ptm)
<hezekiah>	Duas vezes!
<--	mrflibble saiu (mr. flibble diz "game over boys")
<hezekiah>	Falem agora .. ou esperem até terem vontade de falar depois!
<thecrypto>	ok, vou otimizar o ElGamal ainda mais, então esperem 	  benchmarks de ElGamal ainda mais rápidos no futuro
<jrand0m>	por favor, foque em DSA e AES antes de otimizar... por favoooor :)
<thecrypto>	vou sim
<hezekiah>	A razão de ele estar fazendo isso é porque eu estou causando problemas para 	  as pessoas de novo. ;-)
<thecrypto>	estou fazendo números primos para DSA
-->	mrflibble (mrflibble@anon.iip) entrou em #iip-dev
<thecrypto>	bem, pelo menos fazendo o programa para gerar números primos para DSA agora
<hezekiah>	O ElGamal em Java não gosta de um AMD K-6 II 333MHz.
<hezekiah>	OK.
<hezekiah>	A rodada de perguntas acabou!
<jrand0m>	ok hez, terminamos.  você quer fazer um powow para fazer o cliente Java 	  e o router em Python funcionarem?
<hezekiah>	Até a próxima semana, cidadãos!
*	hezekiah bate o martelo *baf*er
</div>
