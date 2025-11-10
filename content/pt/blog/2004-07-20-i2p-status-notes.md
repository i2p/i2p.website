---
title: "Notas de status do I2P de 2004-07-20"
date: 2004-07-20
author: "jr"
description: "Atualização semanal de status abordando o lançamento 0.3.2.3, alterações de capacidade, atualizações do site e considerações de segurança"
categories: ["status"]
---

**1) 0.3.2.3, 0.3.3, e o roteiro**

Após o lançamento da 0.3.2.3 na semana passada, vocês fizeram um ótimo trabalho de atualização - agora só temos dois resistentes (um na 0.3.2.2 e outro lá atrás na 0.3.1.4 :). Nos últimos dias, a rede tem estado mais confiável do que o normal - as pessoas estão ficando no irc.duck.i2p por horas seguidas, downloads de arquivos maiores estão sendo concluídos a partir de eepsites(I2P Sites), e a acessibilidade geral de eepsite(I2P Site) está razoavelmente boa. Como está indo bem e quero mantê-los atentos, decidi mudar alguns conceitos fundamentais e teremos isso disponível em um lançamento 0.3.3 em um dia ou dois.

Como algumas pessoas comentaram sobre o nosso cronograma, perguntando se iríamos cumprir as datas que tínhamos no ar, decidi que provavelmente deveria atualizar o site para refletir o roteiro que tenho no meu palmpilot, então o fiz [1]. As datas foram adiadas e alguns itens foram movidos, mas o plano ainda é o mesmo que foi discutido no mês passado [2].

0.4 atenderá aos quatro critérios de lançamento mencionados (funcional, seguro, anônimo e escalável), embora, antes da 0.4.2, poucas pessoas atrás de NATs e firewalls possam participar, e antes da 0.4.3 haverá um limite superior efetivo para o tamanho da rede devido à sobrecarga de manter um grande número de conexões TCP com outros routers.

[1] http://www.i2p.net/redesign/roadmap [2] http://dev.i2p.net/pipermail/i2p/2004-June/000286.html

**2) s/reliability/capacity/g**

Na última semana, mais ou menos, pessoas no #i2p me ouviram ocasionalmente desabafar sobre como nossas classificações de confiabilidade são completamente arbitrárias (e os problemas que isso causou nas últimas versões). Então eliminamos completamente o conceito de confiabilidade, substituindo-o por uma medição de capacidade - 'quanto um par pode fazer por nós?' Isso teve efeitos em cascata em todo o código de seleção de pares e de perfilamento de pares (e, obviamente, no router console), mas, fora isso, não mudou muita coisa.

Mais informações sobre essa mudança podem ser vistas na página revisada de seleção de pares [3], e quando 0.3.3 for lançada, vocês poderão ver o impacto em primeira mão (tenho mexido nisso nos últimos dias, ajustando algumas configurações, etc).

[3] http://www.i2p.net/redesign/how_peerselection

**3) atualizações do site**

Na última semana, temos feito muito progresso no redesenho do site [4] - simplificando a navegação, ajustando algumas páginas-chave, importando conteúdo antigo e redigindo algumas novas entradas [5]. Estamos quase prontos para colocar o site no ar, mas ainda há algumas coisas que precisam ser feitas.

Mais cedo hoje, duck revisou o site e fez um inventário das páginas que estão faltando e, após as atualizações desta tarde, há algumas questões pendentes que espero que possamos abordar ou conseguir alguns voluntários para assumir:

* **documentation**: hmm, do we need any content for this? or can we have it just sit as a header with no page behind it?
* **development**: I think this is in the same boat as "documentation" above
* **news**: perhaps we can remove the 'announcements' page and put that content here? or should we do as above and let news be a simple heading, with an announcements page below?
* **i2ptunnel_services, i2ptunnel_tuning, i2ptunnel_lan**: We need someone to rewrite the 'how to set up an eepsite(I2P Site)' page, as well as include answers to the two most frequently asked I2PTunnel questions (how to access it through a LAN and how to configure its tunnels - answers being: -e "listen_on 0.0.0.0" and -e 'clientoptions tunnels.numInbound=1 tunnels.depthInbound=1', respectively) Perhaps we can come up with some more comprehensive user level I2PTunnel documentation?
* **jvm**: er, I'm not sure about this page - is it 'how to tweak the JVM for optimal performance'? do we *know*?
* **config_tweaks**: other config parameters for the router (bandwidth limiting, etc). could someone go through the router.config and take a stab at what everything means? if anyone has any questions, please let me know.
* **more meeting logs**: mihi posted up an archive of some logs, perhaps a volunteer can sift through those and post them up?
* perhaps we can update the meetings.html to be date based and include a link to that week's status update along with any release announcements preceding it?

Fora isso, acho que o site está quase pronto para entrar em produção. Alguém tem sugestões ou preocupações nesse sentido?

[4] http://www.i2p.net/redesign/ [5] http://dev.i2p.net/pipermail/i2pwww/2004-July/thread.html

**4) ataques e defesas**

Connelly tem elaborado algumas novas abordagens para tentar abrir brechas na segurança e no anonimato da rede e, ao fazer isso, identificou algumas maneiras de melhorarmos as coisas. Embora alguns aspectos das técnicas que ele descreveu não se encaixem exatamente no I2P, talvez vocês consigam ver formas de levá-las mais adiante para atacar ainda mais a rede? Vamos lá, experimentem! :)

**5) ???**

É basicamente tudo de que me lembro antes da reunião de hoje à noite - por favor, fiquem à vontade para mencionar qualquer outra coisa que eu tenha deixado passar. Enfim, nos vemos no #i2p daqui a alguns minutos.

=jr
