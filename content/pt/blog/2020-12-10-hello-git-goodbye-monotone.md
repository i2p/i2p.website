---
title: "Olá Git, Adeus Monotone"
date: 2020-12-10
author: "idk"
description: "Olá git, adeus mtn"
categories: ["Status"]
---

## Olá, Git, adeus Monotone

### The I2P Git Migration is nearly concluded

Por mais de uma década, o I2P contou com o venerável serviço Monotone para suprir suas necessidades de controle de versão, mas, nos últimos anos, a maior parte do mundo migrou para o agora universal sistema de controle de versão Git. Nesse mesmo período, a Rede I2P tornou-se mais rápida e mais confiável, e foram desenvolvidas soluções alternativas acessíveis para a incapacidade do Git de retomar transferências.

Hoje marca uma ocasião significativa para o I2P, pois desativamos o antigo ramo mtn i2p.i2p e migramos oficialmente o desenvolvimento das bibliotecas principais do I2P em Java do Monotone para o Git.

Embora o nosso uso do mtn tenha sido questionado no passado, e nem sempre tenha sido uma escolha popular, gostaria de aproveitar este momento, como talvez o último projeto a usar o Monotone, para agradecer aos desenvolvedores do Monotone, atuais e antigos, onde quer que estejam, pelo software que criaram.

## GPG Signing

Check-ins nos repositórios do Projeto I2P exigem que você configure a assinatura GPG dos seus commits do git, incluindo Merge Requests (solicitações de mesclagem) e Pull Requests (solicitações de pull). Configure seu cliente git para usar assinatura GPG antes de criar um fork de i2p.i2p e efetuar qualquer commit.

## Assinatura GPG

O repositório oficial é o que está hospedado em https://i2pgit.org/i2p-hackers/i2p.i2p e em https://git.idk.i2p/i2p-hackers/i2p.i2p, mas há um "Mirror" disponível no Github em https://github.com/i2p/i2p.i2p.

Agora que estamos no git, podemos sincronizar repositórios da nossa própria instância auto-hospedada do Gitlab com o Github, e vice-versa. Isso significa que é possível criar e enviar um merge request no Gitlab e, quando ele for mesclado, o resultado será sincronizado com o Github, e um Pull Request no Github, quando for mesclado, aparecerá no Gitlab.

Isso significa que é possível enviar código para nós pela nossa instância do Gitlab ou pelo Github, dependendo do que você preferir; no entanto, mais desenvolvedores do I2P monitoram regularmente o Gitlab do que o Github. MRs (solicitações de mesclagem) para o Gitlab têm maior probabilidade de serem integradas mais rapidamente do que PRs (solicitações de pull) para o Github.

## Repositórios oficiais e sincronização entre GitLab e GitHub

Parabéns e obrigado a todos que ajudaram na migração para o Git, em especial zzz, eche|on, nextloop e os operadores dos espelhos do nosso site! Embora alguns de nós venham a sentir falta do Monotone, ele se tornou um obstáculo para novos e atuais participantes no desenvolvimento do I2P e estamos entusiasmados em nos juntar ao mundo de desenvolvedores que usam o Git para gerenciar seus projetos distribuídos.
