---
title: "Notas de status do I2P de 2005-02-15"
date: 2005-02-15
author: "jr"
description: "Notas semanais sobre o estado do desenvolvimento do I2P, cobrindo o crescimento da rede até 211 routers, os preparativos para a versão 0.5 e i2p-bt 0.1.7"
categories: ["status"]
---

Olá, é aquela hora da semana de novo,

* Index

1) Status da rede
2) Status da versão 0.5
3) i2p-bt 0.1.7
4) ???

* 1) Net status

Embora nenhum novo bug tenha aparecido na rede, na semana passada ganhamos alguma visibilidade em um site p2p francês popular, o que levou a um aumento tanto no número de usuários quanto na atividade de BitTorrent. No pico, chegamos a 211 routers na rede, embora ultimamente esteja oscilando entre 150 e 180. O uso de largura de banda relatado também aumentou, embora, infelizmente, a confiabilidade do IRC tenha sido reduzida, com um dos servidores reduzindo seus limites de largura de banda devido à carga. Houve várias melhorias na biblioteca de streaming para ajudar com isso, mas elas ficaram no ramo 0.5-pre, então ainda não estão disponíveis para a rede em produção.

Outro problema transitório foi a indisponibilidade de um dos HTTP outproxies (www1.squid.i2p), causando a falha de 50% das requisições ao outproxy (proxy de saída). Você pode remover temporariamente esse outproxy abrindo a sua configuração do I2PTunnel [1], editando o eepProxy e alterando a linha "Outproxies:" para conter apenas "squid.i2p". Esperamos colocar o outro novamente online em breve para aumentar a redundância.

[1] http://localhost:7657/i2ptunnel/index.jsp

* 2) 0.5 status

Houve muitos avanços nesta última semana na versão 0.5 (aposto que você já está cansado de ouvir isso, né?).  Graças à ajuda de postman, cervantes, duck, spaetz e uma pessoa não identificada, estamos rodando uma rede de testes com o novo código há quase uma semana e já resolvemos um bom número de bugs que eu não tinha visto na minha rede de testes local.

Nas últimas 24 horas, mais ou menos, as alterações têm sido menores, e não prevejo nenhum trabalho de código substancial restante antes do lançamento da 0.5. Ainda há alguma limpeza adicional, documentação e integração a fazer, e não custa deixar a rede de testes da 0.5 continuar rodando, caso bugs adicionais sejam revelados com o tempo. Como este será um LANÇAMENTO INCOMPATÍVEL COM VERSÕES ANTERIORES, para dar tempo de planejar a atualização, vou fixar um prazo simples: ESTA SEXTA-FEIRA, quando a 0.5 será lançada.

Como bla mencionou no irc, os hosts de eepsite(I2P Site) podem querer tirar seus sites do ar na quinta ou na sexta e mantê-los fora do ar até sábado, quando muitos usuários já terão atualizado. Isso ajudará a reduzir o efeito de um ataque de interseção (por exemplo, se 90% da rede migrou para 0.5 e você ainda está na versão 0.4, se alguém acessar seu eepsite(I2P Site), saberá que você é um dos 10% de routers restantes na rede).

Eu poderia começar a falar sobre o que foi atualizado na 0.5, mas acabaria me estendendo por páginas e páginas, então talvez eu deva adiar e colocar isso na documentação, que eu deveria redigir :)

* 3) i2p-bt 0.1.7

duck preparou uma versão de correção de bugs para a atualização 0.1.6 da semana passada, e dizem por aí que está sensacional (talvez /sensacional demais/, dado o aumento no uso da rede ;)  Mais informações no fórum i2p-bt [2]

[2] http://forum.i2p.net/viewtopic.php?t=300

* 4) ???

Muitas outras coisas acontecendo nas discussões no IRC e no fórum [3], coisas demais para resumir brevemente.  Talvez as partes interessadas possam passar pela reunião e nos trazer atualizações e ideias? De qualquer forma, nos vemos em breve

=jr
