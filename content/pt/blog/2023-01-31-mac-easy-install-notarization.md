---
title: "Atualização sobre a notarização do Mac Easy Install"
date: 2023-01-31
author: "idk, sadie"
description: "O Easy Install Bundle para Mac está travado"
categories: ["release"]
---

O I2P Easy-Install Bundle para Mac vem enfrentando atualizações paralisadas nas últimas 2 versões devido à saída de seu mantenedor. Recomenda-se que os usuários do Easy-Install Bundle para Mac mudem para o instalador clássico no estilo Java, que foi recentemente restaurado na página de download. A versão 1.9.0 tem problemas de segurança conhecidos e não é adequada para hospedar serviços nem para qualquer uso de longo prazo. Aconselha-se que os usuários migrem o quanto antes. Usuários avançados do Easy-Install Bundle podem contornar isso compilando o bundle a partir do código-fonte e autoassinando o software.

## O Processo de Notarização para macOS

Há muitas etapas no processo de distribuição de um aplicativo para usuários da Apple. Para distribuir um aplicativo como um .dmg com segurança, o aplicativo deve passar por um processo de notarização. Para enviar um aplicativo para notarização, o desenvolvedor deve assinar o aplicativo usando um conjunto de certificados que inclui um para assinatura de código e outro para assinar o próprio aplicativo. Essa assinatura deve ocorrer em pontos específicos durante o processo de compilação, antes que o pacote .dmg final, que é distribuído aos usuários finais, possa ser criado.

I2P Java é uma aplicação complexa e, por isso, adequar os tipos de código utilizados na aplicação aos certificados da Apple, bem como definir em que ponto a assinatura deve ocorrer para produzir um carimbo de data e hora válido, torna-se um processo de tentativa e erro. É devido a essa complexidade que a documentação existente para desenvolvedores não tem sido suficiente para ajudar a equipe a entender a combinação correta de fatores que resultará em uma notarização bem-sucedida.

Essas dificuldades tornam difícil prever o cronograma para concluir este processo. Só saberemos que terminamos quando conseguirmos limpar o ambiente de build e seguir o processo de ponta a ponta. A boa notícia é que reduzimos para apenas 4 os erros durante o processo de notarização, ante mais de 50 na primeira tentativa, e podemos prever com razoável segurança que isso estará concluído antes ou a tempo do próximo lançamento em abril.

## Opções para novas instalações e atualizações do I2P no macOS

Novos participantes do I2P ainda podem fazer download do Easy Installer para o macOS 1.9.0. Espero ter uma versão pronta perto do final de abril. As atualizações para a versão mais recente ficarão disponíveis assim que a notarização for bem-sucedida.

As opções clássicas de instalação também estão disponíveis. Isso exigirá baixar o Java e o software I2P por meio do instalador baseado em .jar.

[As instruções de instalação do Jar estão disponíveis aqui](https://geti2p.net/en/download/macos)

Os usuários do Easy-Install podem atualizar para essa versão mais recente usando uma compilação de desenvolvimento produzida localmente.

[As instruções de compilação do Easy-Install estão disponíveis aqui](https://i2pgit.org/i2p-hackers/i2p-jpackage-mac/-/blob/master/BUILD.md)

Há também a opção de desinstalar o software, remover o diretório de configuração do I2P e reinstalar o I2P usando o instalador .jar.
