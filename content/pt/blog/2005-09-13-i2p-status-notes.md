---
title: "Notas de status do I2P para 2005-09-13"
date: 2005-09-13
author: "jr"
description: "Atualização semanal cobrindo as introduções do SSU para NAT hole punching (técnica para atravessar NAT), o progresso da recompensa por testes unitários, a discussão do roadmap do aplicativo cliente e a remoção do modo de entrega garantida obsoleto"
categories: ["status"]
---

Olá pessoal, é hora das atualizações semanais de status

* Index

1) Estado da rede 2) Introduções do SSU / NAT hole punching (técnica para atravessar NAT) 3) Recompensas 4) Instruções para aplicações cliente 5) ???

* 1) Net status

Continuamos avançando com a versão 0.6.0.5 na rede, e quase todos já atualizaram, com muitos executando uma das builds (compilações) desde então (CVS HEAD é 0.6.0.5-9 no momento). No geral, as coisas continuam funcionando bem, embora eu tenha observado um aumento substancial no tráfego de rede, provavelmente devido a um uso maior de i2p-bt ou i2phex. Um dos servidores irc teve um pequeno soluço ontem à noite, mas o outro aguentou bem e as coisas parecem ter se recuperado bem. No entanto, houve melhorias substanciais no tratamento de erros e em outros recursos nas builds CVS, portanto espero que tenhamos um novo lançamento ainda esta semana.

* 2) SSU introductions / NAT hole punching

As compilações mais recentes no CVS incluem suporte às há muito discutidas SSU introductions [1], permitindo-nos realizar NAT hole punching descentralizado (perfuração de NAT) para usuários atrás de um NAT ou firewall que eles não controlam. Embora não trate do NAT simétrico, cobre a maioria dos casos em uso. Os relatos do campo são positivos, embora apenas usuários com as compilações mais recentes possam entrar em contato com os usuários atrás de NAT — compilações mais antigas precisam esperar que o usuário entre em contato primeiro. Por isso, vamos disponibilizar o código em um lançamento mais cedo do que o usual, para reduzir o tempo em que temos essas rotas restritas em vigor.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#introduction

* 3) Bounties

Estava conferindo a lista de discussão i2p-cvs mais cedo e notei vários commits do Comwiz relativos ao que parece ser a fase 3 da recompensa por testes unitários [2]. Talvez o Comwiz possa nos dar uma atualização do andamento desse assunto durante a reunião de hoje à noite.

[2] http://www.i2p.net/bounty_unittests

A propósito, graças à sugestão de uma pessoa anônima, atualizei um pouco o hall da fama [3], incluindo as datas das contribuições, agrupando várias doações de uma mesma pessoa e convertendo para uma única moeda. Obrigado novamente a todos que contribuíram e, se houver informações incorretas publicadas ou se algo estiver faltando, por favor, entre em contato e isso será atualizado.

[3] http://www.i2p.net/halloffame

* 4) Client app directions

Uma das alterações mais recentes nas compilações atuais do CVS é a remoção da antiga forma de entrega mode=guaranteed. Eu não tinha percebido que alguém ainda a usava (e é totalmente desnecessária, já que temos a biblioteca de streaming completa há um ano), mas quando eu estava analisando o i2phex notei essa flag definida. Com a compilação atual (e todas as versões subsequentes), o i2phex usará apenas mode=best_effort, o que deve melhorar seu desempenho.

Meu objetivo ao trazer este assunto (além de mencioná-lo para os usuários do i2phex) é perguntar de que vocês precisam no lado cliente do I2P e se parte do meu tempo deveria ser alocada para ajudar a atender algumas dessas necessidades. De cabeça, vejo muito trabalho disponível em diferentes frentes:  = Syndie: publicação simplificada, sincronização automatizada, dados
    importação, integração com aplicativos (com i2p-bt, susimail, i2phex, etc),
    suporte a tópicos encadeados para permitir comportamento semelhante a fórum, e mais.  = eepproxy: melhoria de taxa de transferência, suporte a pipelining (encadeamento de requisições)  = i2phex: manutenção geral (não o usei o suficiente para conhecer seus
    pontos problemáticos)  = irc: resiliência aprimorada, detectar quedas recorrentes de servidores irc e
    evitar servidores fora do ar, filtrar ações CTCP localmente em vez de no
    servidor, proxy DCC  = Suporte x64 aprimorado com jbigi, jcpuid e o service wrapper (empacotador de serviço)  = integração com a bandeja do sistema (systray), e remover aquela janela do DOS  = Controles de largura de banda aprimorados para bursting (picos)  = Controle de congestionamento aprimorado para sobrecarga de rede e de CPU, bem como
    recuperação.  = Expor mais funcionalidades e documentar os recursos disponíveis do
    console do router para aplicativos de terceiros  = Documentação para desenvolvedores de clientes  = Documentação introdutória do I2P

Além disso, além de tudo isso, ainda há o restante do que está no roadmap [4] e na lista de tarefas [5]. Eu sei do que precisamos tecnicamente, mas não sei do que *você* precisa do ponto de vista do usuário. Fale comigo, o que você quer?

[4] http://www.i2p.net/roadmap [5] http://www.i2p.net/todo

* 5) ???

Há outras coisas acontecendo no núcleo do router e no lado de desenvolvimento de aplicativos além do que foi mencionado acima, mas nem tudo está pronto para uso no momento. Se alguém tiver algo que gostaria de discutir, apareça na reunião esta noite às 20h UTC em #i2p!

=jr
