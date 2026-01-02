---
title: "Git Bundles para I2P"
description: "Buscar e distribuir repositórios grandes com git bundle e BitTorrent"
slug: "git-bundle"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Quando as condições da rede tornam o `git clone` não confiável, você pode distribuir repositórios como **git bundles** pelo BitTorrent ou qualquer outro transporte de arquivos. Um bundle é um único arquivo contendo todo o histórico do repositório. Uma vez baixado, você faz fetch dele localmente e depois volta para o remote upstream.

## 1. Antes de Começar

Gerar um bundle requer um clone Git **completo**. Clones superficiais criados com `--depth 1` irão produzir silenciosamente bundles quebrados que parecem funcionar, mas falham quando outros tentam usá-los. Sempre busque de uma fonte confiável (GitHub em [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p), a instância Gitea do I2P em [i2pgit.org](https://i2pgit.org), ou `git.idk.i2p` sobre I2P) e execute `git fetch --unshallow` se necessário para converter qualquer clone superficial em um clone completo antes de criar bundles.

Se você está apenas consumindo um pacote existente, basta baixá-lo. Nenhuma preparação especial é necessária.

## 2. Baixando um Bundle

### Obtaining the Bundle File

Baixe o arquivo bundle via BitTorrent usando o I2PSnark (o cliente torrent integrado no I2P) ou outros clientes compatíveis com I2P como o BiglyBT com o plugin I2P.

**Importante**: I2PSnark funciona apenas com torrents especificamente criados para a rede I2P. Torrents padrão da clearnet não são compatíveis porque o I2P usa Destinations (endereços de 387+ bytes) em vez de endereços IP e portas.

A localização do arquivo bundle depende do tipo de instalação do I2P:

- **Instalações de usuário/manuais** (instaladas com instalador Java): `~/.i2p/i2psnark/`
- **Instalações de sistema/daemon** (instaladas via apt-get ou gerenciador de pacotes): `/var/lib/i2p/i2p-config/i2psnark/`

Os usuários do BiglyBT encontrarão os arquivos baixados no diretório de downloads configurado.

### Cloning from the Bundle

**Método padrão** (funciona na maioria dos casos):

```bash
git clone ~/.i2p/i2psnark/i2p.i2p.bundle
```
Se você encontrar erros `fatal: multiple updates for ref` (um problema conhecido no Git 2.21.0 e versões posteriores quando a configuração global do Git contém refspecs de fetch conflitantes), use a abordagem de inicialização manual:

```bash
mkdir i2p.i2p && cd i2p.i2p
git init
git fetch ~/.i2p/i2psnark/i2p.i2p.bundle
```
Alternativamente, você pode usar a flag `--update-head-ok`:

```bash
git fetch --update-head-ok ~/.i2p/i2psnark/i2p.i2p.bundle '*:*'
```
### Obtendo o Arquivo Bundle

Após clonar a partir do pacote, aponte o seu clone para o repositório remoto ativo para que as futuras buscas ocorram sobre I2P ou clearnet:

```bash
git remote set-url origin git@127.0.0.1:I2P_Developers/i2p.i2p
```
Ou para acesso clearnet:

```bash
git remote set-url origin https://github.com/i2p/i2p.i2p
```
Para acesso SSH via I2P, você precisa de um túnel cliente SSH configurado no console do seu roteador I2P (tipicamente porta 7670) apontando para `g6u4vqiuy6bdc3dbu6a7gmi3ip45sqwgtbgrr6uupqaaqfyztrka.b32.i2p`. Se estiver usando uma porta não padrão:

```bash
GIT_SSH_COMMAND="ssh -p 7670" git clone git@127.0.0.1:I2P_Developers/i2p.i2p
```
## 3. Creating a Bundle

### Clonando a partir do Bundle

Certifique-se de que o seu repositório está totalmente atualizado com um **clone completo** (não superficial):

```bash
git fetch --all
```
Se você tem um clone superficial, converta-o primeiro:

```bash
git fetch --unshallow
```
### Mudando para o Remoto Ativo

**Usando o target de build do Ant** (recomendado para a árvore de código-fonte do I2P):

```bash
ant git-bundle
```
Isso cria tanto `i2p.i2p.bundle` (o arquivo bundle) quanto `i2p.i2p.bundle.torrent` (metadados BitTorrent).

**Usando git bundle diretamente**:

```bash
git bundle create i2p.i2p.bundle --all
```
Para pacotes mais seletivos:

```bash
git bundle create i2p.i2p.bundle --branches --tags
```
### Verifying Your Bundle

Sempre verifique o pacote antes de distribuir:

```bash
git bundle verify i2p.i2p.bundle
```
Isto confirma que o bundle é válido e mostra quaisquer commits de pré-requisito necessários.

### Pré-requisitos

Copie o pacote e seus metadados de torrent para o seu diretório I2PSnark:

**Para instalações de usuário**:

```bash
cp i2p.i2p.bundle* ~/.i2p/i2psnark/
```
**Para instalações de sistema**:

```bash
cp i2p.i2p.bundle* /var/lib/i2p/i2p-config/i2psnark/
```
O I2PSnark detecta e carrega automaticamente arquivos .torrent em segundos. Acesse a interface web em [http://127.0.0.1:7657/i2psnark](http://127.0.0.1:7657/i2psnark) para começar a semear.

## 4. Creating Incremental Bundles

Para atualizações periódicas, crie bundles incrementais contendo apenas novos commits desde o último bundle:

```bash
git tag lastBundleTag
git bundle create update.bundle lastBundleTag..master
```
Os usuários podem buscar do pacote incremental se já tiverem o repositório base:

```bash
git fetch /path/to/update.bundle
```
Sempre verifique se os pacotes incrementais mostram os commits de pré-requisito esperados:

```bash
git bundle verify update.bundle
```
## 5. Updating After the Initial Clone

Assim que tiver um repositório funcional a partir do bundle, trate-o como qualquer outro clone Git:

```bash
git remote add upstream git@127.0.0.1:I2P_Developers/i2p.i2p
git fetch upstream
git merge upstream/master
```
Ou para fluxos de trabalho mais simples:

```bash
git fetch origin
git pull origin master
```
## 3. Criando um Pacote

- **Distribuição resiliente**: Repositórios grandes podem ser compartilhados via BitTorrent, que lida automaticamente com novas tentativas, verificação de partes e retomada.
- **Bootstrap peer-to-peer**: Novos contribuidores podem fazer bootstrap do seu clone a partir de peers próximos na rede I2P, e então buscar mudanças incrementais diretamente dos hosts Git.
- **Redução de carga no servidor**: Espelhos podem publicar pacotes periódicos para aliviar a pressão nos hosts Git ativos, especialmente útil para repositórios grandes ou condições de rede lentas.
- **Transporte offline**: Pacotes funcionam em qualquer transporte de arquivos (drives USB, transferências diretas, sneakernet), não apenas BitTorrent.

Os bundles não substituem remotes ativos. Eles simplesmente fornecem um método de bootstrapping mais resiliente para clones iniciais ou atualizações importantes.

## 7. Troubleshooting

### Gerando o Pacote

**Problema**: A criação do bundle é bem-sucedida, mas outros não conseguem clonar a partir do bundle.

**Causa**: Seu clone de origem é superficial (criado com `--depth`).

**Solução**: Converter para clone completo antes de criar bundles:

```bash
git fetch --unshallow
```
### Verificando Seu Pacote

**Problema**: `fatal: multiple updates for ref` ao clonar a partir do bundle.

**Causa**: Git 2.21.0+ entra em conflito com refspecs de fetch globais em `~/.gitconfig`.

**Soluções**: 1. Use inicialização manual: `mkdir repo && cd repo && git init && git fetch /path/to/bundle` 2. Use a flag `--update-head-ok`: `git fetch --update-head-ok /path/to/bundle '*:*'` 3. Remova a configuração conflitante: `git config --global --unset remote.origin.fetch`

### Distribuindo via I2PSnark

**Problema**: `git bundle verify` reporta pré-requisitos ausentes.

**Causa**: Bundle incremental ou clone de fonte incompleto.

**Solução**: Busque os commits de pré-requisito ou use o bundle base primeiro, depois aplique as atualizações incrementais.
