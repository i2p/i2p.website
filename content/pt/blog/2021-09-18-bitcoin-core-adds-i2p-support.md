---
title: "Bitcoin Core adiciona suporte a I2P!"
date: 2021-09-18
author: "idk"
description: "Um novo caso de uso e um sinal de aceitação crescente"
categories: ["general"]
---

Após meses de trabalho, o Bitcoin Core adicionou suporte oficial ao I2P! Os nós de Bitcoin sobre I2P podem interagir plenamente com o restante dos nós de Bitcoin, com a ajuda de nós que operam tanto no I2P quanto na clearnet (internet pública), tornando-os participantes de primeira classe na rede Bitcoin. É empolgante ver grandes comunidades como a do Bitcoin notarem as vantagens que o I2P pode lhes trazer, proporcionando privacidade e reachability (capacidade de ser alcançado na rede) a pessoas no mundo inteiro.

## Como Funciona

O suporte ao I2P é automático, por meio da SAM API. Isso também é uma notícia empolgante, pois destaca algumas das coisas em que o I2P é especialmente bom, como capacitar desenvolvedores de aplicativos a criar conexões I2P de forma programática e conveniente. Usuários de Bitcoin-over-I2P podem usar o I2P sem configuração manual, habilitando a SAM API e executando o Bitcoin com o I2P ativado.

## Configurando o seu I2P Router

Para configurar um I2P Router para fornecer conectividade anônima ao Bitcoin, é necessário ativar a SAM API. No Java I2P, você deve ir a http://127.0.0.1:7657/configclients e iniciar a SAM Application Bridge com o botão "Start". Você também pode habilitar a SAM Application Bridge por padrão marcando a caixa "Run at Startup" e clicando em "Save Client Configuration".

No i2pd, a SAM API normalmente está habilitada por padrão, mas, se não estiver, você deve configurar:

```
sam.enabled=true
```
no seu arquivo i2pd.conf.

## Configurando seu nó Bitcoin para anonimato e conectividade

Fazer o próprio Bitcoin iniciar em modo anônimo ainda requer editar alguns arquivos de configuração no Diretório de Dados do Bitcoin, que é %APPDATA%\Bitcoin no Windows, ~/.bitcoin no Linux e ~/Library/Application Support/Bitcoin/ no Mac OSX. Também exige, no mínimo, a versão 22.0.0 para que o suporte a I2P esteja presente.

Depois de seguir estas instruções, você deverá ter um nó privado do Bitcoin que usa I2P para conexões I2P e Tor para conexões .onion e clearnet, de modo que todas as suas conexões sejam anônimas. Para conveniência, usuários do Windows devem abrir seu Diretório de Dados do Bitcoin abrindo o Menu Iniciar e pesquisando por "Run." No prompt do Run, digite "%APPDATA%\Bitcoin" e pressione Enter.

Naquele diretório, crie um arquivo chamado "i2p.conf." No Windows, certifique-se de colocar aspas ao redor do nome do arquivo ao salvá-lo, para impedir que o Windows adicione uma extensão de arquivo padrão. O arquivo deve conter as seguintes opções de configuração do Bitcoin relacionadas ao I2P:

```
i2psam=127.0.0.1:7656
i2pacceptincoming=true
onlynet=i2p
```
Em seguida, você deve criar outro arquivo chamado "tor.conf". O arquivo deve conter as seguintes opções de configuração relacionadas ao Tor:

```
proxy=127.0.0.1:9050
onion=127.0.0.1:9050
onlynet=tor
```
Finally, you'll need to "include" these configuration options in your Bitcoin configuration file, called "bitcoin.conf" in the Data Directory. Add these two lines to your bitcoin.conf file:

```
includeconf=i2p.conf
includeconf=tor.conf
```
Agora o seu nó Bitcoin está configurado para usar apenas conexões anônimas. Para habilitar conexões diretas a nós remotos, remova as linhas que começam com:

```
onlynet=
```
Você pode fazer isso se não precisar que seu nó Bitcoin seja anônimo, e isso ajuda usuários anônimos a se conectar ao restante da rede Bitcoin.
