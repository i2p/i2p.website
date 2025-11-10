---
title: "'Flag de Transmissão 'Criptografada'"
number: "114"
author: "orignal"
created: "2015-01-21"
lastupdated: "2015-01-21"
status: "Needs-Research"
thread: "http://zzz.i2p/topics/1795"
---

## Visão Geral

Esta proposta é sobre adicionar um flag à transmissão que especifica o tipo de
criptografia de ponta a ponta sendo usada.


## Motivação

Aplicativos com alta carga podem enfrentar uma escassez de tags ElGamal/AES+SessionTags.


## Design

Adicionar um novo flag em algum lugar dentro do protocolo de transmissão. Se um pacote vier com
este flag, significa que o payload está criptografado com AES pela chave da chave privada e chave pública do peer. Isso permitiria eliminar a criptografia garlic (ElGamal/AES) e o problema de escassez de tags.

Pode ser configurado por pacote ou por fluxo através de SYN.
