---
title: "Lançamentos do aplicativo Android"
date: 2014-12-01
author: "str4d"
description: "I2P Android 0.9.17 e Bote 0.3 foram lançados no site, no Google Play e no F-Droid."
categories: ["press"]
---

Já faz algum tempo desde a última vez que publiquei atualizações sobre nosso desenvolvimento para Android, e vários lançamentos do I2P ocorreram sem lançamentos correspondentes para Android. Finalmente, a espera acabou!

## Novas versões do aplicativo

Novas versões do I2P Android e do Bote foram lançadas! Elas podem ser baixadas a partir destes URLs:

- [I2P Android 0.9.17](https://geti2p.net/en/download#android)
- [Bote 0.3](https://download.i2p.io/android/bote/releases/0.3/Bote.apk)

A principal mudança destas versões é a transição para o novo sistema de design Material do Android. O Material Design tornou muito mais fácil para desenvolvedores de aplicativos com, digamos, habilidades de design “minimalistas” (como eu) criar aplicativos mais agradáveis de usar. O I2P Android também atualiza seu I2P router subjacente para a versão recém-lançada 0.9.17. O Bote traz vários novos recursos juntamente com muitas melhorias menores; por exemplo, agora você pode adicionar novos destinos de e-mail por meio de códigos QR.

Como mencionei na minha última atualização, a chave de assinatura de release que assina os aplicativos foi alterada. O motivo foi que precisávamos mudar o nome do pacote do I2P Android. O antigo nome do pacote (`net.i2p.android.router`) já havia sido tomado na Google Play (ainda não sabemos quem o estava usando), e queríamos usar o mesmo nome de pacote e a mesma chave de assinatura para todas as distribuições do I2P Android. Fazer isso significa que um usuário poderia inicialmente instalar o aplicativo pelo site do I2P e, depois, se o site fosse bloqueado, poderia atualizá-lo usando a Google Play. O Android OS considera um aplicativo completamente diferente quando seu nome de pacote muda, então aproveitamos para aumentar a força da chave de assinatura.

A impressão digital (SHA-256) da nova chave de assinatura é:

```
AD 1E 11 C2 58 46 3E 68 15 A9 86 09 FF 24 A4 8B C0 25 86 C2 36 00 84 9C 16 66 53 97 2F 39 7A 90
```
## Google Play

Há alguns meses, lançamos tanto o I2P Android quanto o Bote na Google Play, na Noruega, para testar o processo de publicação por lá. Temos o prazer de anunciar que ambos os aplicativos agora estão sendo lançados globalmente pela [Privacy Solutions](https://privacysolutions.no/). Os aplicativos podem ser encontrados nestas URLs:

- [I2P on Google Play](https://play.google.com/store/apps/details?id=net.i2p.android)
- [Bote on Google Play](https://play.google.com/store/apps/details?id=i2p.bote.android)

O lançamento global está sendo realizado em várias etapas, começando pelos países para os quais temos traduções. A exceção notável é a França; devido às regulamentações de importação de código criptográfico, ainda não podemos distribuir esses aplicativos na Google Play da França. Este é o mesmo problema que tem afetado outros aplicativos como TextSecure e Orbot.

## F-Droid

Não pense que nos esquecemos de vocês, usuários do F-Droid! Além dos dois locais acima, configuramos nosso próprio repositório do F-Droid. Se você estiver lendo esta postagem no seu telefone, [clique aqui](https://f-droid.i2p.io/repo?fingerprint=68E76561AAF3F53DD53BA7C03D795213D0CA1772C3FAC0159B50A5AA85C45DC6) para adicioná-lo ao F-Droid (isso só funciona em alguns navegadores Android). Ou, você pode adicionar manualmente a URL abaixo à sua lista de repositórios do F-Droid:

https://f-droid.i2p.io/repo

Se você quiser verificar manualmente a impressão digital (SHA-256) da chave de assinatura do repositório, ou digitá-la ao adicionar o repositório, aqui está:

```
68 E7 65 61 AA F3 F5 3D D5 3B A7 C0 3D 79 52 13 D0 CA 17 72 C3 FA C0 15 9B 50 A5 AA 85 C4 5D C6
```
Infelizmente, o aplicativo I2P no repositório principal do F-Droid não foi atualizado porque nosso mantenedor do F-Droid desapareceu. Esperamos que, ao manter este repositório binário, possamos dar um melhor suporte aos nossos usuários do F-Droid e mantê-los atualizados. Se você já instalou o I2P a partir do repositório principal do F-Droid, será necessário desinstalá-lo caso queira atualizar, porque a chave de assinatura será diferente. Os aplicativos no nosso repositório do F-Droid são os mesmos APKs que são fornecidos em nosso site e no Google Play, portanto, no futuro você poderá atualizar usando qualquer uma dessas fontes.
