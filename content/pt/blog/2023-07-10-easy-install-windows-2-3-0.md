---
title: "Easy-Install para Windows 2.3.0 lançado"
date: 2023-07-10
author: "idk"
description: "Easy-Install para Windows 2.3.0 lançado"
categories: ["release"]
---

O I2P Easy-Install bundle para Windows, versão 2.3.0, já foi lançado. Como de costume, este lançamento inclui uma versão atualizada do I2P router. Isso também abrange questões de segurança que afetam pessoas que hospedam serviços na rede.

Esta será a última versão do pacote Easy-Install incompatível com o I2P Desktop GUI. Ele foi atualizado para incluir novas versões de todas as webextensions incluídas. Um bug de longa data no I2P em navegação privativa que o tornava incompatível com temas personalizados foi corrigido. Ainda assim, recomenda-se aos usuários que *não* instalem temas personalizados. As abas do Snark não são fixadas automaticamente no topo da ordem das abas no Firefox. Exceto por usarem cookieStores alternativos (containers de cookies), as abas do Snark agora se comportam como abas normais do navegador.

**Infelizmente, esta versão ainda é um instalador `.exe` não assinado.** Verifique o checksum (soma de verificação) do instalador antes de o utilizar. **As atualizações, por outro lado** são assinadas pelas minhas chaves de assinatura do I2P e, portanto, seguras.

Esta versão foi compilada com o OpenJDK 20. Usa i2p.plugins.firefox versão 1.1.0 como biblioteca para iniciar o navegador. Usa i2p.i2p versão 2.3.0 como um I2P router e para fornecer aplicações. Como sempre, recomenda-se atualizar para a versão mais recente do I2P router na primeira oportunidade conveniente.

- [Easy-Install Bundle Source](http://git.idk.i2p/i2p-hackers/i2p.firefox/-/tree/i2p-firefox-2.3.0)
- [Router Source](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/tree/i2p-2.3.0)
- [Profile Manager Source](http://git.idk.i2p/i2p-hackers/i2p.plugins.firefox/-/tree/1.1.0)
