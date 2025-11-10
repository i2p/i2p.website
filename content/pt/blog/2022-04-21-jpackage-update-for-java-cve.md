---
title: "Atualização do Jpackage para o CVE-2022-21449 do Java"
date: 2022-04-21
author: "idk"
description: "Pacotes Jpackage lançados com correções para a CVE-2022-21449 do Java"
categories: ["release"]
---

## Detalhes da atualização

Novos pacotes I2P Easy-Install foram gerados usando a versão mais recente da Máquina Virtual Java, que contém uma correção para a CVE-2022-21449 "Psychic Signatures". Recomenda-se que os usuários dos pacotes Easy-Install atualizem o quanto antes. Usuários atuais do OSX receberão atualizações automaticamente; usuários do Windows devem baixar o instalador na nossa página de downloads e executar o instalador normalmente.

O router I2P no Linux utiliza a Máquina Virtual Java configurada pelo sistema host. Usuários nessas plataformas devem reverter para uma versão estável do Java anterior à versão 14 do Java a fim de mitigar a vulnerabilidade até que atualizações sejam lançadas pelos mantenedores dos pacotes. Outros usuários que utilizam uma JVM externa devem atualizar a JVM para uma versão corrigida o mais rápido possível.
