---
title: "Lançamento do pacote de instalação fácil do Windows 1.9.0"
date: 2022-08-28
author: "idk"
description: "Windows Easy-Install Bundle 1.9.0 - Melhorias importantes de estabilidade/compatibilidade"
categories: ["release"]
---

## Esta atualização inclui o novo router 1.9.0 e grandes melhorias na experiência de uso para os usuários do pacote

Esta versão inclui o novo router I2P 1.9.0 e é baseada em Java 18.02.1.

Os antigos scripts em lote foram descontinuados gradualmente em favor de uma solução mais flexível e estável no próprio jpackage. Isso deve corrigir todos os erros relacionados à localização de caminhos e à colocação de aspas em caminhos que estavam presentes nos scripts em lote. Após a atualização, os scripts em lote podem ser removidos com segurança. Eles serão removidos pelo instalador na próxima atualização.

Um subprojeto para gerenciar ferramentas de navegação foi iniciado: i2p.plugins.firefox, que possui amplos recursos para configurar navegadores I2P de forma automática e estável em muitas plataformas. Isso foi usado para substituir os scripts em lote, mas também funciona como uma ferramenta de gerenciamento do I2P Browser multiplataforma. Contribuições são bem-vindas aqui: http://git.idk.i2p/idk/i2p.plugins.firefox no repositório de código-fonte.

Esta versão melhora a compatibilidade com routers I2P executados externamente, como os fornecidos pelo instalador IzPack e por implementações de router de terceiros, como i2pd. Ao melhorar a descoberta de routers externos, passa a exigir menos recursos do sistema, melhora o tempo de inicialização e evita que ocorram conflitos de recursos.

Além disso, o perfil foi atualizado para a versão mais recente do perfil do Arkenfox. I2P in Private Browsing e NoScript foram ambos atualizados. O perfil foi reestruturado para permitir a avaliação de diferentes configurações para diferentes modelos de ameaça.
