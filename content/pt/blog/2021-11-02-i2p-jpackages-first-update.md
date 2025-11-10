---
title: "I2P Jpackages recebem a primeira atualização"
date: 2021-11-02
author: "idk"
description: "Novos pacotes mais fáceis de instalar atingem um novo marco"
categories: ["general"]
---

Há alguns meses, lançamos novos pacotes que esperávamos que ajudassem a integrar novas pessoas à rede I2P, tornando a instalação e a configuração do I2P mais fáceis para mais pessoas. Removemos dezenas de etapas do processo de instalação ao mudar de uma JVM externa para um Jpackage, criamos pacotes padrão para os sistemas operacionais de destino e os assinamos de uma forma que o sistema operacional reconhecesse para manter o usuário em segurança. Desde então, os routers jpackage alcançaram um novo marco: eles estão prestes a receber suas primeiras atualizações incrementais. Essas atualizações substituirão o JDK 16 jpackage por um JDK 17 jpackage atualizado e fornecerão correções para alguns pequenos bugs que detectamos após o lançamento.

## Atualizações comuns ao Mac OS e Windows

Todos os instaladores jpackaged do I2P recebem as seguintes atualizações:

* Update the jpackaged I2P router to 1.5.1 which is built with JDK 17

Por favor, atualize o mais rápido possível.

## Atualizações do Jpackage do I2P para Windows

Somente os pacotes para Windows recebem as seguintes atualizações:

* Updates I2P in Private Browsing, NoScript browser extensions
* Begins to phase out HTTPS everywhere on new Firefox releases
* Updates launcher script to fix post NSIS launch issue on some architectures

Para uma lista completa de alterações, consulte o changelog.txt em i2p.firefox

## Atualizações do Jpackage do I2P para Mac OS

Somente os pacotes do Mac OS recebem as seguintes atualizações:

* No Mac-Specific changes. Mac OS is updated to build with JDK 17.

Para um resumo do desenvolvimento, consulte os checkins em i2p-jpackage-mac
