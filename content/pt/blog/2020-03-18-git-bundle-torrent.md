---
title: "Usando um bundle do git para obter o código-fonte do I2P"
date: 2020-03-18
author: "idk"
description: "Baixe o código-fonte do I2P via Bittorrent"
categories: ["development"]
---

Clonar repositórios de software grandes via I2P pode ser difícil, e usar o git às vezes pode tornar isso ainda mais difícil. Felizmente, às vezes também pode facilitar. O Git tem um comando `git bundle` que pode ser usado para transformar um repositório git em um arquivo do qual o git pode então clonar, fazer fetch ou importar, a partir de um local no seu disco local. Ao combinar esse recurso com downloads via BitTorrent, podemos resolver nossos problemas restantes com `git clone`.

## Antes de começar

Se você pretende gerar um git bundle, você **deve** já possuir uma cópia completa do repositório **git**, não do repositório mtn. Você pode obtê-la no github ou em git.idk.i2p, mas um clone superficial (um clone feito com --depth=1) *não funcionará*. Isso falhará silenciosamente, criando algo que parece um bundle, mas quando você tentar cloná-lo, falhará. Se você estiver apenas obtendo um git bundle pré-gerado, então esta seção não se aplica a você.

## Obtendo o código-fonte do I2P via BitTorrent

Alguém precisará fornecer a você um arquivo .torrent ou um magnet link (link magnet) correspondente a um `git bundle` (arquivo de pacote do Git) existente que essa pessoa já tenha gerado para você. Assim que você tiver um bundle obtido via BitTorrent, será necessário usar o git para criar um repositório de trabalho a partir dele.

## Usando `git clone`

Clonar a partir de um git bundle (pacote do Git) é fácil, basta:

```
git clone $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
Se você obtiver o seguinte erro, tente usar git init e git fetch manualmente em vez disso:

```
fatal: multiple updates for ref 'refs/remotes/origin/master' not allowed
```
## Usando `git init` e `git fetch`

Primeiro, crie um diretório i2p.i2p para transformá-lo em um repositório Git:

```
mkdir i2p.i2p && cd i2p.i2p
```
Em seguida, inicialize um repositório Git vazio para o qual buscar as alterações de volta:

```
git init
```
Por fim, busque o repositório a partir do bundle:

```
git fetch $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
## Substitua o remoto bundle pelo remoto upstream

Agora que você tem um bundle, você pode acompanhar as alterações configurando o remoto para a origem do repositório upstream:

```
git remote set-url origin git@127.0.0.1:i2p-hackers/i2p.i2p
```
## Gerando um pacote

Primeiro, siga o guia do Git para usuários até que você tenha um clone do repositório i2p.i2p no qual `--unshallow` tenha sido aplicado com sucesso. Se você já tiver um clone, certifique-se de executar `git fetch --unshallow` antes de gerar um pacote torrent.

Quando você tiver isso, basta executar o alvo correspondente do ant:

```
ant bundle
```
e copie o pacote resultante para o seu diretório de downloads do I2PSnark. Por exemplo:

```
cp i2p.i2p.bundle* $HOME/.i2p/i2psnark/
```
Em um ou dois minutos, o I2PSnark detectará o torrent. Clique no botão "Start" para começar a semear o torrent.
