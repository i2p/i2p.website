---
title: "Reunião de Desenvolvedores do I2P - 11 de novembro de 2003"
date: 2003-11-11
author: "jrand0m"
description: "Reunião de desenvolvimento do I2P abordando status do router, atualizações do roteiro, implementação nativa de modPow, instalador gráfico (GUI) e discussões sobre licenciamento"
categories: ["meeting"]
---

(Cortesia da Wayback Machine http://www.archive.org/)

## Recapitulação rápida

<p class="attendees-inline"><strong>Presentes:</strong> dish, dm, jrand0m, MrEcho, nop</p>

(registro da reunião editado para encobrir o fato de que iip caiu no meio da reunião e houve muitos timeouts de ping, então não tente ler isto como uma narrativa linear)

## Registro de Reunião

<div class="irc-log"> [22:02] &lt;jrand0m&gt; pauta [22:02] &lt;jrand0m&gt; 0) boas-vindas [22:02] &lt;jrand0m&gt; 1) i2p router [22:02] &lt;jrand0m&gt; 1.1) status [22:02] &lt;jrand0m&gt; 1.2) mudanças no roadmap [22:02] &lt;jrand0m&gt; 1.3) subprojetos em aberto [22:02] &lt;jrand0m&gt; 2) modPow nativo [22:03] &lt;jrand0m&gt; 2) instalador GUI [22:03] &lt;jrand0m&gt; 3) IM [22:03] &lt;jrand0m&gt; 4) serviço de nomes [22:03] &lt;MrEcho&gt; eu vi aquele código .c [22:03] &lt;jrand0m&gt; 5) licenciamento [22:03] &lt;jrand0m&gt; 6) outros? [22:03] &lt;jrand0m&gt; 0) boas-vindas [22:03] &lt;jrand0m&gt; oi. [22:03] &lt;nop&gt; oi [22:03] &lt;jrand0m&gt; reunião 2^6 [22:04] &lt;jrand0m&gt; tem algum item de pauta para adicionar aí, nop? [22:04] &lt;jrand0m&gt; ok, 1.1) status do router [22:04] &lt;jrand0m&gt; estamos na 0.2.0.3 e, pelo que ouvi por último, está funcional [22:04] &lt;MrEcho&gt; &gt; 0.2.0.3 [22:04] &lt;MrEcho&gt; certo? [22:05] &lt;MrEcho&gt; estou executando .. parece ok [22:05] &lt;nop&gt; não [22:05] &lt;jrand0m&gt; houve commits menores após o lançamento 0.2.0.3, nada que valha um novo release [22:05] &lt;nop&gt; Só estou tentando me atualizar [22:05] &lt;jrand0m&gt; beleza [22:06] &lt;jrand0m&gt; dadas as experiências e o feedback da 0.2.0.x, o roadmap foi atualizado para deixar as coisas menos intensivas em recursos para rodar [22:06] &lt;jrand0m&gt; (ou seja, para que as pessoas possam rodar servidores web / etc. e isso não devore a CPU delas) [22:06] &lt;jrand0m&gt; especificamente (indo para a pauta 1.2): http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap [22:06] &lt;MrEcho&gt; o que notei é que a maioria dos routers usa: TransportStyle: PHTTP [22:07] &lt;MrEcho&gt; ele vai automaticamente para phttp ou chega a tentar tcp primeiro [22:07] &lt;jrand0m&gt; hmm, a maioria dos routers deve suportar PHTTP e, se puder aceitar conexões de entrada, deve suportar TCP também [22:07] &lt;jrand0m&gt; sempre que possível usa TCP [22:07] &lt;jrand0m&gt; PHTTP é ponderado como cerca de 1000 vezes mais caro do que TCP [22:08] &lt;jrand0m&gt; (veja GetBidsJob, que pergunta a cada transporte quanto acha que custaria enviar uma mensagem para um par) [22:08] &lt;jrand0m&gt; (e veja TCPTransport.getBid e PHTTPTransport.getBid para os valores usados) [22:08] &lt;MrEcho&gt; ok [22:08] &lt;jrand0m&gt; você está usando PHTTP com frequência para enviar e receber mensagens? [22:09] &lt;jrand0m&gt; (isso pode ser um sinal de que seu listener TCP não está acessível) [22:09] &lt;MrEcho&gt; eu não coloquei as URLs do meu lado [22:09] &lt;jrand0m&gt; ah, ok. [22:09] &lt;MrEcho&gt; ohh, está sim [22:10] &lt;jrand0m&gt; ok, sim, meus routers têm conexões TCP abertas com você [22:10] &lt;dm&gt; que hospitaleiros. [22:10] * jrand0m está feliz que vocês me fizeram implementar routerConsole.html para que não tenhamos que vasculhar os logs por esta porcaria [22:11] &lt;MrEcho&gt; existe algum timeout que, se não conectar ao tcp, vá para phttp? e qual é o tempo disso [22:11] &lt;jrand0m&gt; mas enfim, a grande mudança no roadmap é que a 0.2.1 vai implementar o esquema AES+SessionTag [22:11] &lt;MrEcho&gt; ou poderíamos ter isso em uma configuração? [22:11] &lt;jrand0m&gt; se receber um TCP connection refused / host not found /etc, falha essa tentativa imediatamente e tenta o próximo bid disponível [22:12] &lt;MrEcho&gt; então sem novas tentativas [22:12] &lt;jrand0m&gt; phttp tem um timeout de 30 s, se não me engano [22:12] &lt;jrand0m&gt; não há necessidade de retry.  você ou tem uma conexão TCP aberta e pode enviar os dados, ou não :) [22:12] &lt;MrEcho&gt; lol ok [22:13] &lt;MrEcho&gt; ele vai tentar tcp toda vez depois disso ou pular e ir direto para phttp na próxima conexão? [22:13] &lt;jrand0m&gt; no momento, ele tentará tcp a cada vez. [22:13] &lt;jrand0m&gt; os transportes ainda não mantêm histórico [22:13] &lt;MrEcho&gt; ok, legal [22:14] &lt;jrand0m&gt; (mas se um peer falhar 4 vezes, ele entra na lista negra por 8 minutos) [22:14] &lt;MrEcho&gt; bem, assim que o outro lado receber a mensagem phttp, deve se conectar ao router que enviou a mensagem via tcp, certo? [22:14] &lt;jrand0m&gt; correto.  assim que qualquer conexão tcp for estabelecida, pode usá-la. [22:14] &lt;jrand0m&gt; (mas se ambos os peers tiverem apenas phttp, obviamente só usarão phttp) [22:15] &lt;MrEcho&gt; isso significaria que não conseguiu est. uma conexão tcp com nada [22:15] &lt;MrEcho&gt; .. mas é [22:16] &lt;MrEcho&gt; queria que houvesse um jeito de contornar isso [22:16] &lt;jrand0m&gt; não, um dos meus routers não tem um endereço TCP - apenas PHTTP.  mas eu estabeleço conexões TCP com peers que têm endereços TCP. [22:16] &lt;jrand0m&gt; (e então eles podem enviar mensagens de volta por aquela conexão TCP em vez de me enviar mensagens PHTTP mais lentas) [22:17] &lt;jrand0m&gt; ou não era isso que você quis dizer? [22:17] &lt;MrEcho&gt; é, me confundi [22:17] &lt;jrand0m&gt; valeu, sem problema [22:18] &lt;jrand0m&gt; então, veja o roadmap atualizado para informações atualizadas de cronograma ((Link: http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap)http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap) [22:18] &lt;jrand0m&gt; ok, 1.3) subprojetos em aberto [22:19] &lt;jrand0m&gt; Finalmente coloquei um monte da minha lista de tarefas do meu palmpilot no wiki em (Link: http://wiki.invisiblenet.net/iip-wiki?OpenSubprojects)http://wiki.invisiblenet.net/iip-wiki?OpenSubprojects [22:19] &lt;jrand0m&gt; então, se você estiver entediado e procurando projetos de código... :) [22:19] &lt;MrEcho&gt; puxa [22:20] &lt;MrEcho&gt; já tenho 2 [22:20] &lt;dish&gt; Você tem um palmpilot, isso é elite [22:20] &lt;MrEcho&gt; o meu morreu [22:20] &lt;jrand0m&gt; mihi&gt; há um item lá sobre o I2PTunnel descrevendo uma ideia que tive há um tempinho [22:20] &lt;MrEcho&gt; não sei o que há com ele [22:21] &lt;jrand0m&gt; sim, eu costumava ter palms, mas recentemente este foi doado para a causa ;) [22:21] &lt;dish&gt; Poderia haver um item de pauta na reunião para discutir quando foi a última vez que userX digitou algo [22:21] &lt;MrEcho&gt; essa droga nem liga mais [22:21] &lt;MrEcho&gt; lol [22:22] &lt;jrand0m&gt; Não acho que UserX tenha dito qualquer coisa em 4 ou 5 meses ;) [22:22] &lt;MrEcho&gt; isso é um bot ou algo assim? [22:22] &lt;dish&gt; O que ele disse há 5 meses? [22:22] &lt;MrEcho&gt; aposto que é um bitchx rodando em alguma máquina à qual ele tinha acesso .. e esqueceu [22:22] &lt;jrand0m&gt; que voltariam com comentários sobre o anonCommFramework (nome antigo do i2p) na semana seguinte ;) [22:23] &lt;dish&gt; haha [22:23] &lt;jrand0m&gt; mas suponho que ele esteja ocupado.  é a vida [22:23] &lt;jrand0m&gt; ok, 2) modPow nativo [22:23] &lt;MrEcho&gt; eu vi aquele código em C [22:24] &lt;jrand0m&gt; eu montei um .c de stub e uma classe Java para mostrar como algo como GMP ou outra biblioteca MPI poderia ser integrada, mas obviamente isso não funciona [22:25] &lt;jrand0m&gt; o ideal seria se tivéssemos um pequeno pacote de classes em C e aquela classe wrapper Java trivial associada que pudéssemos compilar para windows, osx, *bsd, linux e empacotar sob GPL

(insira aqui uma falha grave no iip)

[22:38] &lt;MrEcho&gt; a última coisa que vi foi: [13:25] &lt;jrand0m&gt; ok, 2) modPow nativo
[22:38] &lt;jrand0m&gt; oi, MrEcho
[22:38] &lt;jrand0m&gt; sim, parece que um proxy principal caiu
[22:39] &lt;jrand0m&gt; vou dar mais 2 minutos antes de reiniciar
[22:39] &lt;MrEcho&gt; ok
[22:39] &lt;MrEcho&gt; por US$ 25, uma vez, eu consigo Java completo no thenidus.net ... um dos meus sites
[22:40] &lt;jrand0m&gt; US$ 25? cobram para instalar software?
[22:40] &lt;MrEcho&gt; não faço ideia, na verdade... é um pacote
[22:40] &lt;MrEcho&gt; estou falando com um amigo agora
[22:40] &lt;jrand0m&gt; não tenho certeza de que o código esteja estável o suficiente para sair por aí e alugar um monte de espaços de colocation (hospedagem em datacenter compartilhado) para colocar routers. ainda :)
[22:41] &lt;dm&gt; pacote de quê?
[22:41] &lt;MrEcho&gt; Java - JSP
[22:41] &lt;jrand0m&gt; ok, reenviando o que mandei antes:
[22:41] &lt;jrand0m&gt; juntei um stub .c e uma classe Java para mostrar como algo como o GMP ou outra biblioteca MPI poderia ser integrado, mas obviamente isso não funciona
[22:41] &lt;jrand0m&gt; o ideal seria termos um pequeno pacote de classes em C e aquela classe encapsuladora (wrapper) Java trivial associada, que pudéssemos compilar para windows, osx, *bsd, linux e empacotar sob a GPL (ou uma licença menos restritiva)
[22:41] &lt;jrand0m&gt; porém, com o novo roadmap colocando AES+SessionTag como meu item de ação atual, isso não é tão crítico quanto era
[22:41] &lt;jrand0m&gt; se alguém quiser tocar isso, seria ótimo (e tenho certeza de que outro projeto com o qual todos estamos familiarizados teria interesse nesse empacotamento)
[22:43] &lt;dm&gt; frazaa?
[22:43] &lt;jrand0m&gt; hehe, de certa forma ;)
[22:44] &lt;jrand0m&gt; ok, 3) instalador com GUI
[22:44] &lt;jrand0m&gt; MrEcho&gt; oi
[22:44] &lt;MrEcho&gt; :)
[22:44] &lt;MrEcho&gt; hehe
[22:44] &lt;MrEcho&gt; está caminhando
[22:44] &lt;jrand0m&gt; legal
[22:44] &lt;MrEcho&gt; nada sofisticado
[22:45] &lt;MrEcho&gt; tenho umas ideias bem legais para deixá-lo bem caprichado... mas isso ainda vai demorar
[22:45] &lt;jrand0m&gt; eu estava pensando se o instalador deveria acrescentar 1) uma opção para obter automaticamente os seeds (nós de arranque) de http://.../i2pdb/ 2) obter automaticamente o http://.../i2p/squid.dest e criar também um runSquid.bat/runSquid.sh?
[22:45] &lt;jrand0m&gt; isso
[22:46] &lt;jrand0m&gt; sim, queremos que o instalador seja o mais simples possível — que coisas sofisticadas você estava pensando?
[22:46] &lt;MrEcho&gt; a questão é... quando você roda java -jar installer ele vai para o modo sem GUI por padrão por causa do jeito que você tem as coisas
[22:46] &lt;MrEcho&gt; como vamos fazer para, quando você der duplo clique no arquivo JAR, ele carregar a GUI
[22:47] &lt;jrand0m&gt; install.jar &lt;-- sem GUI,  installgui.jar &lt;-- com GUI
[22:47] &lt;jrand0m&gt; código separado, pacotes separados
[22:47] &lt;MrEcho&gt; "sofisticado" no sentido de coisas que você talvez nem note... mas vai ficar bonito e limpo
[22:47] &lt;jrand0m&gt; legal
[22:47] &lt;MrEcho&gt; ah ok
[22:48] &lt;jrand0m&gt; (ou install &lt;-- GUI installcli &lt;-- CLI. vamos ver como as coisas evoluem)
[22:49] &lt;jrand0m&gt; mais algo sobre a GUI, ou pulamos para o item 4)?
[22:49] &lt;jrand0m&gt; (alguma estimativa de prazo? sem pressão, só para saber)
[22:51] &lt;MrEcho&gt; sem ideia no momento
[22:51] &lt;jrand0m&gt; show
[22:51] &lt;jrand0m&gt; ok, 4) IM (mensageria instantânea)
[22:51] &lt;jrand0m&gt; thecrypto não tá aqui, então.....
[22:51] &lt;jrand0m&gt; 5) serviço de nomes
[22:51] &lt;jrand0m&gt; wiht também não está aqui...
[22:51] &lt;jrand0m&gt; ping
[22:52] &lt;dish&gt; você se perdeu na contagem dos itens da pauta
[22:52] &lt;dish&gt; 3) IM
[22:52] &lt;jrand0m&gt; sim, eu costumava ter dois itens 2 na pauta
[22:52] &lt;dish&gt; 4) Nomes
[22:52] &lt;dish&gt; ;)
[22:52] &lt;jrand0m&gt; (modPow nativo e instalador com GUI)
[22:52] &lt;jrand0m&gt; viu, somos dinâmicos e tal
[22:59] &lt;jrand0m&gt; ok, para os logs acho que vou continuar
[22:59] &lt;jrand0m&gt; 6) licenciamento
[23:00] &lt;jrand0m&gt; estou pensando em algo menos restritivo que a GPL. estamos usando algum código sob licença MIT, além de que um outro arquivo é GPL (mas é só a codificação base64 e pode ser substituída facilmente). fora isso, todo o código tem direitos autorais meus ou do thecrypto.
[23:00] * dish olha a parte do código de tunnel do I2P do mihi
[23:01] &lt;jrand0m&gt; ah, verdade, o mihi lançou isso como GPL mas ele também pode querer lançar sob outra coisa, se quiser
[23:01] &lt;jrand0m&gt; (mas o i2ptunnel é essencialmente um app de terceiros e pode licenciar como quiser)
[23:02] &lt;jrand0m&gt; (embora, como o I2P SDK é GPL, ele tenha sido forçado a ser GPL)
[23:02] &lt;MrEcho&gt; já estava na hora
[23:02] &lt;jrand0m&gt; não sei. licenciamento não é meu forte, mas estou inclinado pelo menos a ir para LGPL
[23:02] * dish libera as 10–20 linhas de alteração no código do I2P HTTP Client do mihi sob seja lá qual for a licença do mihi
[23:03] &lt;jrand0m&gt; hehe :)
[23:06] &lt;jrand0m&gt; de qualquer forma, 7) outros?
[23:07] &lt;jrand0m&gt; alguém tem perguntas / preocupações / ideias em relação ao I2P?
[23:07] &lt;dish&gt; Deixa eu perguntar
[23:07] &lt;dish&gt; O I2P tem algum recurso de nome de grupo?
[23:07] &lt;jrand0m&gt; recurso de nome de grupo?
[23:07] &lt;dm&gt; equipe Discovery Channel!
[23:07] &lt;MrEcho&gt; lol
[23:08] &lt;dish&gt; Tipo, se você quiser ter uma rede privada ou separada, mas algum router se misturar de alguma forma, sem um nome de grupo as duas redes acabariam se fundindo
[23:08] &lt;MrEcho&gt; ele está pensando no waste
[23:08] &lt;jrand0m&gt; ah
[23:08] &lt;dish&gt; não sei por que você ia querer isso, mas só estou perguntando, por via das dúvidas
[23:08] &lt;jrand0m&gt; sim, no começo do design da rede eu estava brincando com isso
[23:09] &lt;jrand0m&gt; é mais avançado do que precisamos por enquanto (ou para um futuro relativamente próximo [6–12 meses]), mas pode ser integrado depois
[23:09] &lt;dish&gt; Ou isso é uma má ideia porque é melhor manter uma rede única e grande
[23:09] &lt;dm&gt; i2pisdead
[23:09] &lt;jrand0m&gt; hehe dm
[23:10] &lt;nop&gt; cala a boca
[23:10] &lt;jrand0m&gt; não, dish, é uma boa ideia
[23:10] &lt;dm&gt; nop: valentão?
[23:10] &lt;jrand0m&gt; é essencialmente o que a versão 0.2.3 é — rotas restritas
[23:10] &lt;jrand0m&gt; (ou seja, você tem um pequeno conjunto privado (confiável) de pares e não quer que todos saibam quem são, mas ainda quer poder se comunicar com eles)
[23:15] &lt;jrand0m&gt; ok, mais alguma coisa?
[23:15] &lt;nop&gt; não, só estou sendo engraçadinho
[23:18] &lt;dm&gt; engraçadinho?
[23:20] &lt;jrand0m&gt; ok, bem, reunião /interessante/, com alguns travamentos do iip no meio ;)
[23:21] * jrand0m dá um *baf* e encerra a reunião </div>
