---
title: "Notas de status do I2P de 2006-03-21"
date: 2006-03-21
author: "jr"
description: "Integração do JRobin para estatísticas de rede, bots de IRC biff e toopie, e anúncio de nova chave GPG"
categories: ["status"]
---

Oi, pessoal, é terça-feira de novo

* Index

1) Estado da rede 2) jrobin 3) biff e toopie 4) nova chave 5) ???

* 1) Net status

A última semana tem sido bem estável, sem nenhum novo lançamento ainda. Tenho me dedicado intensamente ao controle de taxa de tunnel e à operação em baixa largura de banda, mas, para ajudar nesses testes, integrei o JRobin ao console da web e ao nosso sistema de gerenciamento de estatísticas.

* 2) JRobin

JRobin [1] é um port puro em Java do RRDtool [2], o que nos permite gerar gráficos bonitos como aqueles que zzz vem produzindo, com pouquíssima sobrecarga de memória. Nós o configuramos para funcionar inteiramente em memória, então não há contenção de bloqueio de arquivos, e o tempo para atualizar o banco de dados é imperceptível. Há muitas coisas interessantes que o JRobin pode fazer e que não estamos explorando, mas a próxima versão terá a funcionalidade básica, além de um meio de exportar os dados em um formato que o RRDtool possa entender.

[1] http://www.jrobin.org/ [2] http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/

* 3) biff and toopie

O postman tem trabalhado intensamente em alguns bots úteis, e fico feliz em informar que o adorável biff está de volta [3], avisando sempre que você tiver correio (anônimo) enquanto estiver no irc2p. Além disso, o postman criou um bot totalmente novo para nós — o toopie — para servir como um bot de informações para I2P/irc2p. Ainda estamos alimentando o toopie com FAQs (perguntas frequentes), mas ele deve entrar nos canais habituais em breve. Obrigado, postman!

[3] http://hq.postman.i2p/?page_id=15

* 4) new key

Para quem está atento, você deve ter notado que minha chave GPG expira em alguns dias.  Minha nova chave @ http://dev.i2p.net/~jrandom tem a impressão digital 0209 9706 442E C4A9 91FA  B765 CE08 BC25 33DC 8D49 e o ID da chave 33DC8D49.  Esta publicação está assinada com minha chave antiga, mas minhas publicações subsequentes (e lançamentos) durante o próximo ano serão assinadas com a nova chave.

* 5) ???

É isso por enquanto - apareça no #i2p em alguns minutos para a nossa reunião semanal e dê um alô!

=jr
