---
title: "Notas de status do I2P de 2006-10-10"
date: 2006-10-10
author: "jr"
description: "lançamento 0.6.1.26 com feedback positivo, Syndie 0.910a aproximando-se da versão 1.0 e avaliação de controle de versão distribuído para o Syndie"
categories: ["status"]
---

Olá pessoal, breves notas de status desta semana

* Index

1) 0.6.1.26 e status da rede 2) Status do desenvolvimento do Syndie 3) Controle de versão distribuído revisitado 4) ???

* 1) 0.6.1.26 and network status

Há alguns dias lançamos uma nova versão 0.6.1.26, incluindo muitas melhorias no i2psnark feitas pelo zzz e algumas novas verificações de segurança de NTP do Complication, e os relatos têm sido positivos. A rede parece estar a crescer ligeiramente, sem novos efeitos estranhos, embora algumas pessoas ainda tenham dificuldades em construir os seus tunnels (como sempre foi o caso).

* 2) Syndie development status

Vêm surgindo cada vez mais melhorias, com a versão alfa atual em 0.910a. A lista de recursos para a 1.0 está praticamente fechada, então, neste momento, é basicamente correções de bugs e documentação. Passe no #i2p se quiser ajudar a testar :)

Além disso, houve algumas discussões no canal sobre os projetos da GUI (interface gráfica) do Syndie - meerboop teve algumas ideias bacanas e está trabalhando para documentá-los. A GUI do Syndie é o principal componente do lançamento do Syndie 2.0, então, quanto mais cedo colocarmos isso em andamento, mais cedo dominamos o mund^W^W^W^W podemos lançar o Syndie para as massas desavisadas.

Há também uma nova proposta no meu blog no Syndie sobre o acompanhamento de erros e de pedidos de funcionalidades usando o próprio Syndie. Para facilitar o acesso, publiquei na web uma exportação em texto simples daquela postagem - a página 1 está em <http://dev.i2p.net/~jrandom/bugsp1.txt> e a página 2 está em <http://dev.i2p.net/~jrandom/bugsp2.txt>

* 3) Distributed version control revisited

Uma das coisas que ainda precisam ser definidas para o Syndie é qual sistema público de controle de versão usar e, como mencionado antes, é necessária funcionalidade distribuída e offline. Tenho analisado a meia dúzia, mais ou menos, de opções de código aberto disponíveis (darcs, mercurial, git/cogito, monotone, arch, bzr, codeville), vasculhando a documentação deles, experimentando-as e conversando com seus desenvolvedores. No momento, o monotone e o bzr parecem ser os melhores em termos de funcionalidade e segurança (com repositórios não confiáveis, precisamos de criptografia forte para garantir que estamos obtendo apenas alterações autênticas), e a integração estreita com criptografia do monotone parece muito atraente. Ainda estou avançando pelas várias centenas de páginas da documentação, mas, pelo que discuti com os desenvolvedores do monotone, parece que eles estão fazendo tudo do jeito certo.

Claro que, independentemente de qual dvcs acabarmos adotando, todos os lançamentos serão disponibilizados em formato tarball simples, e correções serão aceitas para revisão em formato diff -uw simples. Ainda assim, para quem considerar se envolver no desenvolvimento, eu adoraria ouvir suas opiniões e preferências.

* 4) ???

Como pode ver, há muita coisa acontecendo, como sempre. Também tem havido mais discussões naquele tópico "resolver a fome mundial" no fórum, então confira em <http://forum.i2p.net/viewtopic.php?t=1910>

Se você tiver algo mais para discutir, por favor apareça no #i2p para nossa reunião de desenvolvimento hoje à noite, ou publique no fórum ou na lista!

=jr
