---
title: "Notas de status do I2P de 2006-01-17"
date: 2006-01-17
author: "jr"
description: "Estado da rede com a 0.6.1.9, melhorias na criptografia da criação de tunnel, e atualizações na interface do blog do Syndie"
categories: ["status"]
---

Oi, pessoal, é terça-feira de novo

* Index

1) Status da rede e 0.6.1.9 2) Criptografia para criação de Tunnel 3) Blogs do Syndie 4) ???

* 1) Net status and 0.6.1.9

Com a 0.6.1.9 lançada e 70% da rede atualizada, a maioria das correções de bugs incluídas parece estar funcionando como esperado, e há relatos de que o novo speed profiling (perfilamento de velocidade) tem selecionado alguns bons pares. Ouvi falar de taxa de transferência sustentada em pares rápidos excedendo 300KBps com 50-70% de uso de CPU, com outros routers na faixa de 100-150KBps, diminuindo gradualmente até aqueles atingindo 1-5KBps. Ainda há uma rotatividade substancial de identidades de router, então parece que a correção de bug que eu achava que reduziria isso não reduziu (ou a rotatividade é legítima).

* 2) Tunnel creation crypto

No outono, houve muita discussão sobre como construímos nossos tunnels, junto com os trade-offs entre a criação de tunnel telescópica no estilo Tor e a criação de tunnel exploratória no estilo I2P [1]. Ao longo do processo, chegamos a uma combinação [2] que elimina os problemas da criação telescópica no estilo Tor [3], mantém os benefícios unidirecionais do I2P e reduz as falhas desnecessárias. Como havia muitas outras coisas acontecendo na época, a implementação da nova combinação foi adiada, mas, como agora estamos nos aproximando da versão 0.6.2, durante a qual precisaremos reformular o código de criação de tunnel de qualquer maneira, é hora de acertar os detalhes.

Esbocei um rascunho de especificação para a nova criptografia do tunnel (túnel de rede) e publiquei no meu blog do Syndie outro dia e, após algumas pequenas mudanças que surgiram ao implementá-la de fato, temos uma especificação consolidada no CVS [4]. Também há no CVS [5] um código básico que a implementa, embora ainda não esteja integrado à construção real de tunnel. Se alguém estiver com tempo sobrando, adoraria receber feedback sobre a especificação. Enquanto isso, continuarei trabalhando no novo código de construção de tunnel.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html e     consulte as discussões relacionadas aos ataques de bootstrap [2] http://dev.i2p.net/pipermail/i2p/2005-October/001064.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001057.html [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD [5] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/java/src/net/                        i2p/router/tunnel/BuildMessageTest.java

* 3) Syndie blogs

Como mencionado antes, esta nova versão 0.6.1.9 traz reformulações substanciais na interface do blog do Syndie, incluindo o novo estilo do cervantes e a seleção de links do blog e do logotipo por cada usuário (por exemplo, [6]). Você pode controlar esses links à esquerda clicando no link "configure your blog" na sua página de perfil, levando você a http://localhost:7657/syndie/configblog.jsp.  Depois de fazer suas alterações ali, na próxima vez que você enviar uma postagem a um repositório, essas informações serão disponibilizadas para outras pessoas.

[6] http://syndiemedia.i2p.net/     blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 4) ???

Como já estou 20 minutos atrasado para a reunião, é melhor ser breve.  Sei que há mais algumas coisas acontecendo, mas, em vez de expô-las aqui, os desenvolvedores que quiserem discuti-las devem dar uma passada na reunião e trazê-las à tona.  Enfim, é isso por enquanto, vejo vocês no #i2p!

=jr
