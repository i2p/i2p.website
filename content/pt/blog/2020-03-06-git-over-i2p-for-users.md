---
title: "Git via I2P para Usuários"
date: 2020-03-06
author: "idk"
description: "Git via I2P"
categories: ["development"]
---

Tutorial para configurar o acesso ao git por meio de um I2P Tunnel. Este tunnel atuará como seu ponto de acesso a um único serviço git no I2P. Faz parte do esforço geral para migrar o I2P de monotone para Git.

## Antes de mais nada: Conheça as funcionalidades que o serviço oferece ao público

Dependendo de como o serviço Git está configurado, ele pode ou não disponibilizar todos os serviços no mesmo endereço. No caso de git.idk.i2p, há uma URL HTTP pública e uma URL SSH para configurar no seu cliente SSH do Git. Qualquer uma pode ser usada para push ou pull, mas recomenda-se o uso de SSH.

## Primeiro: Crie uma conta em um serviço de Git

Para criar seus repositórios em um serviço Git remoto, crie uma conta de usuário nesse serviço. É claro que também é possível criar repositórios localmente e fazer push (enviar) para um serviço Git remoto, mas a maioria exigirá uma conta e que você crie um espaço para o repositório no servidor.

## Segundo: Crie um projeto para testar

Para garantir que o processo de configuração funcione, é útil criar um repositório para testar a partir do servidor. Acesse o repositório i2p-hackers/i2p.i2p e faça um fork na sua conta.

## Terceiro: Configure o seu tunnel do cliente git

Para ter acesso de leitura e escrita a um servidor, você precisará configurar um tunnel para o seu cliente SSH. Se tudo de que você precisa é clonagem HTTP/S somente leitura, então você pode pular tudo isso e apenas usar a variável de ambiente http_proxy para configurar o git para usar o I2P HTTP Proxy pré-configurado. Por exemplo:

```
http_proxy=http://localhost:4444 git clone --depth=1 http://git.idk.i2p/youruser/i2p.i2p
git fetch --unshallow
```
Para acesso via SSH, inicie o "New Tunnel Wizard" em http://127.0.0.1:7657/i2ptunnelmgr e configure um tunnel de cliente apontando para o endereço base32 SSH do serviço Git.

## Quarto: Tente clonar

Agora que o seu tunnel está totalmente configurado, você pode tentar clonar via SSH:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone git@127.0.0.1:youruser/i2p.i2p
```
Você pode receber um erro em que o lado remoto encerra a conexão inesperadamente. Infelizmente, o Git ainda não oferece suporte a clonagem retomável. Até lá, há algumas maneiras relativamente simples de lidar com isso. A primeira e mais fácil é tentar clonar com profundidade limitada:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone --depth 1 git@127.0.0.1:youruser/i2p.i2p
```
Depois de realizar um shallow clone (clone superficial), você pode obter o restante com suporte a retomada mudando para o diretório do repositório e executando:

```
git fetch --unshallow
```
Neste ponto, você ainda não tem todos os seus ramos. Você pode obtê-los executando:

```
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
## Fluxo de trabalho sugerido para desenvolvedores

O controle de versão funciona melhor quando você o utiliza bem! Recomendamos fortemente um fluxo de trabalho fork-first (fazer um fork primeiro) e feature-branch (branch de funcionalidade):

1. **Never make changes to the Master Branch**. Use the master branch to periodically obtain updates to the official source code. All changes should be made in feature branches.

2. Set up a second remote in your local repository using the upstream source code:

```
git remote add upstream git@127.0.0.1:i2p-hackers/i2p.i2p
```
3. Pull in any upstream changes on your current master:

```
git pull upstream master
```
4. Before making any changes to the source code, check out a new feature branch to develop on:

```
git checkout -b feature-branch-name
```
5. When you're done with your changes, commit them and push them to your branch:

```
git commit -am "I added an awesome feature!"
git push origin feature-branch-name
```
6. Submit a merge request. When the merge request is approved, check out the master locally and pull in the changes:

```
git checkout master
git pull upstream master
```