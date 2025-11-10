---
title: "Notas de status do I2P de 2004-08-03"
date: 2004-08-03
author: "jr"
description: "Atualização semanal do status do I2P abrangendo o desempenho da versão 0.3.4, o desenvolvimento do novo console da web e vários projetos de aplicações"
categories: ["status"]
---

Oi, pessoal, vamos tirar esta atualização de status da frente

## Índice:

1. 0.3.4 status
2. On deck for 0.3.4.1
3. New web console / I2PTunnel controller
4. 0.4 stuff
5. Other development activities
6. ???

## 1) 0.3.4 estado

Com o lançamento da versão 0.3.4 na semana passada, a nova rede está com desempenho bem satisfatório - conexões de irc estão durando várias horas por vez e a obtenção de eepsite(site I2P) parece ser bastante confiável. A taxa de transferência ainda é geralmente baixa, embora tenha melhorado um pouco (eu costumava ver de forma consistente 4-5KBps; agora vejo consistentemente 5-8KBps). oOo publicou dois scripts resumindo a atividade de irc, incluindo o tempo de ida e volta das mensagens e o tempo de vida da conexão (com base no bogobot do hypercubus, que foi recentemente integrado ao CVS)

## 2) Previsto para 0.3.4.1

Como todos na 0.3.4 já notaram, eu estava *cof* um pouco verboso nos meus logs, o que foi corrigido no cvs. Além disso, depois de escrever algumas ferramentas para fazer testes de estresse na ministreaming lib (biblioteca de mini-streaming), adicionei um 'choke' para que ela não consuma quantidades enormes de memória (vai bloquear ao tentar adicionar mais de 128KB de dados ao buffer de um stream, de modo que, ao enviar um arquivo grande, seu router não carregue esse arquivo inteiro na memória). Acho que isso vai ajudar com os problemas de OutOfMemory que as pessoas têm observado, mas vou adicionar algum código adicional de monitoramento / depuração para verificar isso.

## 3) Novo console web / controlador do I2PTunnel

Além das modificações acima para a 0.3.4.1, temos a primeira versão do novo console do router pronta para alguns testes. Por alguns motivos, ainda não vamos incluí-lo como parte da instalação padrão, então haverá instruções sobre como colocá-lo para rodar quando a revisão 0.3.4.1 sair daqui a alguns dias. Como vocês viram, eu sou realmente péssimo em web design e, como muitos de vocês têm dito, eu deveria parar de ficar brincando com a camada de aplicação e deixar o núcleo e o router bem sólidos. Assim, embora o novo console tenha grande parte das funcionalidades que queremos (configurar o router inteiramente por meio de algumas páginas web simples, oferecer um resumo rápido e legível do estado do router, expor a capacidade de criar / editar / parar / iniciar diferentes instâncias de I2PTunnel), eu realmente preciso de ajuda de pessoas que entendem bem da parte web.

As tecnologias usadas no novo console web são JSP e CSS padrão e JavaBeans simples que consultam o router / I2PTunnels por dados e processam requisições. Todos eles são empacotados em um par de arquivos .war e implantados em um servidor web Jetty integrado (que precisa ser iniciado por meio das linhas clientApp.* do router). Os JSPs e beans do console principal do router são bastante sólidos tecnicamente, embora os novos JSPs e beans que eu desenvolvi para gerenciar instâncias de I2PTunnel sejam um tanto improvisados.

## 4) Coisas da 0.4

Além da nova interface web, a versão 0.4 incluirá o novo instalador do hypercubus, que ainda não integramos de fato. Também precisamos fazer mais algumas simulações em grande escala (especialmente o tratamento de aplicações assimétricas como IRC e outproxies (proxies de saída)). Além disso, há algumas atualizações que preciso fazer passar no kaffe/classpath para que possamos colocar a nova infraestrutura web para funcionar em JVMs de código aberto. Também preciso preparar mais alguns documentos (um sobre escalabilidade e outro analisando a segurança/anonimato em alguns cenários comuns). Também queremos ter todas as melhorias que vocês propuserem integradas ao novo console web.

Ah, e corrija quaisquer bugs que você ajudar a encontrar :)

## 5) Outras atividades de desenvolvimento

Embora tenha havido muito progresso no sistema I2P base, isso é apenas metade da história — muitos de vocês estão fazendo um ótimo trabalho em aplicações e bibliotecas para tornar o I2P útil. Vi algumas perguntas no histórico de mensagens sobre quem está trabalhando em quê, então, para ajudar a divulgar essas informações, aqui está tudo de que eu tenho conhecimento (se você estiver trabalhando em algo que não está listado e quiser compartilhar, se eu estiver enganado, ou se quiser discutir seu progresso, por favor, manifeste-se!).

### Active development:

- python SAM/I2P lib (devs: sunshine, aum)
- C SAM lib (devs: nightblade)
- python kademlia/I2P DHT (devs: aum)
- v2v - Voice over I2P (devs: aum)
- outproxy load balancing (devs: mule)

### Development I've heard about but don't know the status of:

- swarming file transfer / BT (devs: nickster)

### Paused development:

- Enclave DHT (devs: nightblade)
- perl SAM lib (devs: BrianR)
- I2PSnark / BT (devs: eco)
- i2pIM (devs: thecrypto)
- httptunnel (devs: mihi)
- MyI2P address book (devs: jrandom)
- MyI2P blogging (devs: jrandom)

## 6) ???

Thats all I can think of for now - swing on by the meeting later tonight to chat 'bout stuff. As always, 9p GMT on #i2p on the usual servers.

=jr
