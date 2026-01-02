---
title: "Usando uma IDE com I2P"
description: "Configurar o Eclipse e o NetBeans para desenvolver o I2P com Gradle e arquivos de projeto incluídos"
slug: "ides"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

<p> O branch principal de desenvolvimento do I2P (<code>i2p.i2p</code>) foi configurado para permitir que os desenvolvedores configurem facilmente duas das IDEs mais comumente usadas para desenvolvimento Java: Eclipse e NetBeans. </p>

<h2>Eclipse</h2>

<p> Os principais ramos de desenvolvimento do I2P (<code>i2p.i2p</code> e ramos derivados dele) contêm <code>build.gradle</code> para permitir que o ramo seja facilmente configurado no Eclipse. </p>

<ol> <li> Certifique-se de ter uma versão recente do Eclipse. Qualquer versão mais recente que 2017 deve funcionar. </li> <li> Faça o checkout do branch I2P em algum diretório (por exemplo, <code>$HOME/dev/i2p.i2p</code>). </li> <li> Selecione "File → Import..." e então sob "Gradle" selecione "Existing Gradle Project". </li> <li> Para "Project root directory:" escolha o diretório onde o branch I2P foi baixado. </li> <li> No diálogo "Import Options", selecione "Gradle Wrapper" e pressione Continue. </li> <li> No diálogo "Import Preview" você pode revisar a estrutura do projeto. Múltiplos projetos devem aparecer sob "i2p.i2p". Pressione "Finish". </li> <li> Pronto! Seu workspace agora deve conter todos os projetos dentro do branch I2P, e suas dependências de build devem estar configuradas corretamente. </li> </ol>

<h2>NetBeans</h2>

<p> Os principais branches de desenvolvimento do I2P (<code>i2p.i2p</code> e branches derivados dele) contêm arquivos de projeto do NetBeans. </p>

<!-- Mantenha o conteúdo mínimo e próximo ao original; atualizaremos mais tarde. -->
