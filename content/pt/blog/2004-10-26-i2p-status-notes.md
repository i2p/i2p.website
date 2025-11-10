---
title: "Notas de status do I2P de 2004-10-26"
date: 2004-10-26
author: "jr"
description: "Atualização semanal de status do I2P sobre a estabilidade da rede, o desenvolvimento da biblioteca de streaming, o progresso do mail.i2p e os avanços no BitTorrent"
categories: ["status"]
---

Olá, pessoal, é hora da atualização semanal

## Índice

1. Net status
2. Streaming lib
3. mail.i2p progress
4. ???

## 1) Estado da rede

Não quero agourar, mas na última semana a rede tem estado praticamente como antes - razoavelmente estável para irc, eepsites(I2P Sites) carregando de forma confiável, embora arquivos grandes ainda frequentemente exijam retomar o download. Basicamente, nada de novo a relatar, além do fato de que não há nada de novo a relatar.

Ah, uma coisa que descobrimos é que, embora o Jetty suporte HTTP resume (retomada de download via HTTP), ele só o faz para HTTP 1.1. Isso funciona bem para a maioria dos navegadores e ferramentas de download, *exceto* wget - wget envia a requisição de retomada como HTTP 1.0. Então, para baixar arquivos grandes, use curl ou alguma outra ferramenta com suporte a retomada em HTTP 1.1 (graças a duck e ardvark por investigarem a fundo e encontrarem uma solução!)

## 2) Biblioteca de streaming

Como a rede tem estado bastante estável, tenho dedicado quase todo o meu tempo a trabalhar na nova biblioteca de streaming. Embora ainda não esteja pronta, houve muito progresso - os cenários básicos já funcionam bem, as janelas deslizantes estão a funcionar bem para self-clocking (autorregulação do ritmo), e a nova biblioteca funciona como um drop-in replacement (substituição direta) para a antiga, do ponto de vista do cliente (as duas bibliotecas de streaming não conseguem comunicar entre si, porém).

Nos últimos dias tenho trabalhado em alguns cenários mais interessantes. O mais importante é a rede com latência, que simulamos injetando atrasos nas mensagens recebidas, seja um atraso aleatório simples de 0-30s ou um atraso escalonado (80% do tempo com atraso de 0-10s, 10% @ 10-20s de atraso, 5% @ 20-30s, 3% @ 30-40s, 4% @ 40-50s). Outro teste importante tem sido a perda aleatória de mensagens — isso não deveria ser comum no I2P, mas devemos ser capazes de lidar com isso.

O desempenho geral tem sido bastante bom, mas ainda há muito trabalho a fazer antes que possamos implantar isso na rede em produção. Esta atualização será 'perigosa', no sentido de que é tremendamente poderosa - se for feita de forma terrivelmente errada, podemos lançar um DDoS contra nós mesmos num piscar de olhos, mas se for feita corretamente, bem, deixe-me apenas dizer que há muito potencial (prometer menos e entregar mais).

Então, dito isso, e como a rede está bastante estável, não tenho pressa em lançar algo que não esteja suficientemente testado. Mais novidades quando houver mais novidades.

## 3) progresso do mail.i2p

postman & sua turma têm trabalhado duro no e‑mail via I2P (veja www.postman.i2p), e há novidades empolgantes a caminho - talvez o postman tenha uma atualização para nós?

Como observação, eu entendo e me identifico com os pedidos por uma interface de webmail, mas o postman está sobrecarregado trabalhando em algumas coisas interessantes no back-end do sistema de e-mail. Uma alternativa, no entanto, é instalar uma interface de webmail *localmente* no seu próprio servidor web - existem soluções de webmail em JSP/servlet disponíveis. Isso permitiria que você executasse sua própria interface de webmail local em, por exemplo, `http://localhost:7657/mail/`

Eu sei que há alguns scripts de código aberto por aí para acessar contas POP3, o que já nos leva meio caminho andado - talvez alguém pudesse procurar por algum que suporte POP3 e SMTP autenticado? Vamos lá, você sabe que quer!

## 4) ???

Ok, é tudo o que tenho a dizer por enquanto - passa lá na reunião daqui a alguns minutos e nos avisa do que está acontecendo.

=jr
