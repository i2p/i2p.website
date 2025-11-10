---
title: "Notas de status do I2P de 2005-10-18"
date: 2005-10-18
author: "jr"
description: "Atualização semanal abordando o sucesso do lançamento da versão 0.6.1.3, a discussão sobre colaboração com o Freenet, a análise de ataques de bootstrap de tunnel, o progresso em relação ao bug de upload do I2Phex e a recompensa por NAT simétrico"
categories: ["status"]
---

Oi, pessoal, é terça-feira de novo

* Index

1) 0.6.1.3 2) Freenet, I2P e darknets (redes escuras) (oh céus) 3) Ataques ao bootstrap de tunnel 4) I2Phex 5) Syndie/Sucker 6) ??? [500+ recompensa por NAT simétrico]

* 1) 0.6.1.3

Na sexta-feira passada lançamos uma nova versão 0.6.1.3 e, com 70% da rede atualizada, os relatos têm sido muito positivos. As novas melhorias no SSU parecem ter reduzido retransmissões desnecessárias, permitindo uma vazão mais eficiente em taxas de transferência mais altas e, até onde sei, não houve quaisquer problemas graves com o proxy de IRC ou com as melhorias do Syndie.

Uma coisa que vale mencionar é que o Eol ofereceu uma recompensa para suporte a NAT simétrico no rentacoder[1], então, com sorte, teremos algum progresso nesse sentido!

[1] http://rentacoder.com/RentACoder/misc/BidRequests/ShowBidRequest.asp?lngBidRequestId=349320

* 2) Freenet, I2P, and darknets (oh my)

Finalmente encerramos aquela thread com mais de 100 mensagens, com uma visão mais clara das duas redes, de como elas se encaixam e de quanto espaço temos para avançar na colaboração. Não vou entrar aqui em quais topologias ou modelos de ameaça elas são mais adequadas, mas você pode consultar as listas se quiser saber mais. No âmbito da colaboração, enviei ao toad alguns exemplos de código para reutilizar nosso transporte SSU, o que pode ser útil para o pessoal do Freenet no curto prazo, e, mais adiante, talvez trabalhemos juntos para oferecer premix routing (roteamento de pré-mistura) aos usuários do Freenet em ambientes onde o I2P é viável. À medida que o Freenet avança, talvez também consigamos fazer o Freenet funcionar sobre o I2P como uma aplicação cliente, permitindo a distribuição automatizada de conteúdo entre os usuários que o executam (por exemplo, circulando arquivos e publicações do Syndie), mas vamos ver primeiro como funcionam os sistemas planejados de carga e distribuição de conteúdo do Freenet.

* 3) Tunnel bootstrap attacks

Michael Rogers entrou em contato a respeito de alguns novos ataques interessantes à criação de tunnel (túnel) do I2P [2][3][4]. O ataque principal (montar com sucesso um ataque de predecessor durante todo o processo de bootstrap) é interessante, mas não é realmente prático - a probabilidade de sucesso é (c/n)^t, com c atacantes, n pares na rede e t tunnels construídos pelo alvo (ao longo da vida útil) - menor do que a probabilidade de um adversário assumir o controle de todos os h saltos em um tunnel (P(sucesso) = (c/n)^h) depois que o router (roteador) tiver construído h tunnels.

Michael publicou outro ataque na lista, que estamos analisando no momento, então você poderá acompanhá-lo por lá também.

[2] http://dev.i2p.net/pipermail/i2p/2005-October/001005.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001008.html [4] http://dev.i2p.net/pipermail/i2p/2005-October/001006.html

* 4) I2Phex

Striker está fazendo mais progresso no bug de upload, e há relatos de que ele já o isolou. Com sorte, entrará no CVS esta noite e será lançado como 0.1.1.33 logo depois. Fique de olho no fórum [5] para mais informações.

[5] http://forum.i2p.net/viewforum.i2p?f=25

Dizem por aí que o redzara está fazendo um ótimo progresso ao se reintegrar ao ramo principal do Phex, então, com sorte e com a ajuda do Gregor, vamos deixar tudo atualizado em breve!

* 5) Syndie/Sucker

dust também tem trabalhado bastante com o Sucker, com código que está inserindo mais dados RSS/Atom no Syndie. Talvez possamos integrar ainda mais o Sucker e o post CLI ao Syndie, talvez até um controle baseado na web para agendar importações de diferentes feeds RSS/Atom em vários blogs. Veremos...

* 6) ???

Há muita coisa acontecendo além do que foi dito acima, mas esse é o essencial do que tenho conhecimento. Se alguém tiver perguntas ou preocupações, ou quiser trazer outros assuntos, apareça na reunião hoje às 20h UTC em #i2p!

=jr
