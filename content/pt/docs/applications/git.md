---
title: "Git sobre I2P"
description: "Conectando clientes Git a serviços hospedados em I2P como i2pgit.org"
slug: "git"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
reviewStatus: "needs-review"
---

Clonar e enviar repositórios dentro do I2P usa os mesmos comandos Git que você já conhece—seu cliente simplesmente conecta através de túneis I2P em vez de TCP/IP. Este guia explica como configurar uma conta, configurar túneis e lidar com conexões lentas.

> **Início rápido:** O acesso somente leitura funciona através do proxy HTTP: `http_proxy=http://127.0.0.1:4444 git clone http://example.i2p/project.git`. Siga os passos abaixo para acesso de leitura/escrita via SSH.

## 1. Criar uma Conta

Escolha um serviço Git I2P e registre-se:

- Dentro do I2P: `http://git.idk.i2p`
- Mirror clearnet: `https://i2pgit.org`

O registro pode exigir aprovação manual; verifique a página inicial para obter instruções. Após a aprovação, faça um fork ou crie um repositório para ter algo com que testar.

## 2. Configurar um Cliente I2PTunnel (SSH)

1. Abra o console do router → **I2PTunnel** e adicione um novo túnel **Client**.
2. Insira o destino do serviço (Base32 ou Base64). Para `git.idk.i2p` você encontrará ambos os destinos HTTP e SSH na página inicial do projeto.
3. Escolha uma porta local (por exemplo `localhost:7442`).
4. Ative o início automático se você planeja usar o túnel com frequência.

A interface confirmará o novo túnel e mostrará seu status. Quando estiver em execução, os clientes SSH podem se conectar a `127.0.0.1` na porta escolhida.

## 3. Clonar via SSH

Use a porta do tunnel com `GIT_SSH_COMMAND` ou um bloco de configuração SSH:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone git@127.0.0.1:your-project/example.git
```
Se a primeira tentativa falhar (os túneis podem ser lentos), tente uma clonagem superficial:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone --depth 1 git@127.0.0.1:your-project/example.git
cd example
git fetch --unshallow
```
Configure o Git para buscar todas as branches:

```bash
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
### Dicas de Desempenho

- Adicione um ou dois tunnels de backup no editor de tunnels para melhorar a resiliência.
- Para testes ou repositórios de baixo risco, você pode reduzir o comprimento do tunnel para 1 hop, mas esteja ciente do compromisso com o anonimato.
- Mantenha `GIT_SSH_COMMAND` em seu ambiente ou adicione uma entrada em `~/.ssh/config`:

```sshconfig
Host git.i2p
    HostName 127.0.0.1
    Port 7442
    User git
```
Então clone usando `git clone git@git.i2p:namespace/project.git`.

## 4. Sugestões de Fluxo de Trabalho

Adote um fluxo de trabalho de fork e branch comum no GitLab/GitHub:

1. Defina um remote upstream: `git remote add upstream git@git.i2p:I2P_Developers/i2p.i2p`
2. Mantenha seu `master` sincronizado: `git pull upstream master`
3. Crie branches de funcionalidade para alterações: `git checkout -b feature/new-thing`
4. Envie branches para seu fork: `git push origin feature/new-thing`
5. Envie um merge request e depois atualize o master do seu fork a partir do upstream.

## 5. Lembretes de Privacidade

- O Git armazena os timestamps de commit no seu fuso horário local. Para forçar timestamps em UTC:

```bash
git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'
```
Use `git utccommit` em vez de `git commit` quando a privacidade for importante.

- Evite incorporar URLs da clearnet ou IPs em mensagens de commit ou metadados do repositório se o anonimato for uma preocupação.

## 6. Resolução de Problemas

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Symptom</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Fix</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connection closed</code> during clone</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Retry with <code>--depth 1</code>, add backup tunnels, or increase tunnel quantities.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>ssh: connect to host 127.0.0.1 port …: Connection refused</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensure the I2PTunnel client is running and SAM is enabled.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Slow performance</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length, increase bandwidth limits, or schedule large fetches during off-peak hours.</td>
    </tr>
  </tbody>
</table>
Para cenários avançados (espelhamento de repositórios externos, distribuição de bundles), consulte os guias complementares: [Fluxos de trabalho com Git bundle](/docs/applications/git-bundle/) e [Hospedagem do GitLab via I2P](/docs/guides/gitlab/).
